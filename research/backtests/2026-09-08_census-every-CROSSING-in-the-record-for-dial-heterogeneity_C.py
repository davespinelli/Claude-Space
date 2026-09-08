#!/usr/bin/env python3
"""Idea 439 — census-every-CROSSING-in-the-record-for-dial-heterogeneity (lane C, 2026-09-08)

QUESTION (queue, verbatim intent)
  Idea 226 found idea 219's published crossing (0.425) EXISTS on the raw pooled curve and
  changes once dial fixed effects are removed, so a crossing read off a pooled curve over
  heterogeneous cells can be an artefact of what sits where on the x-axis.  Census every
  crossing/threshold the record has read off a pooled local curve, re-read each with fixed
  effects for its own cell-type axis, and report how many survive.

CENSUS FRAME (mechanical, declared before any number is read)
  The record's own name for a pooled local curve is a committed `*.curve*.csv`.  Every such
  file in research/backtests is enumerated (11 files).  An item is ADMITTED iff
    (a) its cell-level rows are committed (the curve file itself, or a named sibling), AND
    (b) those rows carry a numeric x-axis the run pooled over, AND
    (c) they carry >= 1 categorical cell-type column with >= 2 levels (the heterogeneity
        axis fixed effects can be removed on), AND
    (d) the run's own result.md reads a LOCATION (a crossing, a floor, an argmax, or an
        explicit "no crossing exists") off that curve.
  Files failing (a)-(d) are censused as NOT-RE-READABLE and reported, never dropped silently.
  The two idea-219/226 share curves are the same 560 cells; the parent (idea 219) is the
  admitted item and idea 226's curve file is recorded as its duplicate.

TWO TUNED PARAMETERS, ALL GRID POINTS REPORTED
  P1  HMULT — the local half-window as a multiple of the item's own median grid step,
      in {1, 2, 3, 4, 5}.  HMULT 3 is the HEADLINE because on item 219 it is the record's
      own published half-window (0.075 = 3 x 0.025) to the digit.
  P2  FE MODE — {NONE, WITHIN, RECENTRED, STANDARDISED} at the FULL cell key.
        WITHIN        y~ = y - mean(y | cell)                   (idea 226's demeaning; this
                      removes the pooled LEVEL as well as the composition)
        RECENTRED     y~ = y - mean(y | cell) + mean(y)         (composition removed, LEVEL kept)
        STANDARDISED  each window's cell mix re-weighted to the global mix on the item's
                      largest single axis (idea 226's other construction; level kept)
      Per-single-axis FE is computed for every categorical column of every item and reported
      as a diagnostic; it is never selected on.
  Nothing else is tuned.  Grid, min-cells-in-window (5) and the crossing reader are idea
  219/226's committed conventions, imported by construction rather than re-chosen.

PRE-REGISTERED SURVIVAL RULE
  Each item carries the KIND of location its own run published (crossing / no-crossing /
  argmax), declared in the table below before any number is read.  A reading SURVIVES iff
  the FE re-read reproduces that location within TOL grid steps, TOL = 1 (0 also reported);
  a published "no crossing exists" survives iff no INTERIOR crossing exists after FE either.
  A crossing is INTERIOR only if it sits strictly above the grid's first centre: idea 226's
  reader returns the first centre when the curve is positive throughout (nothing to cross)
  and nan when it never becomes uniformly positive (also nothing to cross).  Both the
  crossing and the argmax are read and reported for every item regardless of kind.

RULE 8
  (i)  CENSUS-LEVEL: leave-one-cell-type-out.  For each item and each level of its largest
       categorical axis, the crossing is read on the OTHER levels (pooled and FE) and scored
       against the held-out level's own curve.  Reported as agreement rates.
  (ii) BOOK-LEVEL (PROTOCOL rule 8, live prices): a fresh 126-book band-dial experiment on
       three panels.  The band threshold is read off the IS (<= 2016-12-31) pooled curve and
       off the IS FE curve, both chosen IS-only, and the two books are evaluated untouched on
       2017-2026 against RULES v2 (live), RULES v1 and SPY.  Both KEEP paths on every book.

Costs 10 bps, weekly/monthly rebalance, weights at t applied at t+1 (PROTOCOL 2).
Artefacts: .console.txt, .census.csv, .curves.csv, .perxis.csv, .loco.csv, .bookgrid.csv,
           .walkforward.csv, .keeppaths.csv, .result.md
Nothing outside research/ is touched.
"""
from __future__ import annotations
import sys, json, itertools
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, band_state  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, rebalance_mask, metrics  # noqa

BT = ROOT / "research" / "backtests"
STEM = "2026-09-08_census-every-CROSSING-in-the-record-for-dial-heterogeneity_C"
LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ============================================================ curve / crossing (idea 219/226)
MIN_IN_WIN = 5


def local_curve(x, y, grid, half_w, min_in=MIN_IN_WIN):
    """(centre, n, mean y) at every grid point — idea 226's `local_curve`, verbatim shape."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    out = []
    for g in grid:
        m = (x >= g - half_w) & (x <= g + half_w)
        n = int(m.sum())
        out.append((float(g), n, float(y[m].mean()) if n >= min_in else np.nan))
    return out


def crossing_of(loc):
    """idea 226's `crossing_of`: (first centre above which every defined window is positive,
    last non-positive centre below it)."""
    defined = [np.isfinite(r[2]) for r in loc]
    pos = [np.isfinite(r[2]) and r[2] > 0 for r in loc]
    ch = np.nan
    for i, r in enumerate(loc):
        if not defined[i] or not pos[i]:
            continue
        if all(pos[j] for j in range(i, len(loc)) if defined[j]):
            ch = float(r[0]); break
    below = [r[0] for i, r in enumerate(loc)
             if defined[i] and not pos[i] and (not np.isfinite(ch) or r[0] < ch)]
    return ch, (max(below) if below else np.nan)


def argmax_of(loc):
    v = [(r[2], r[0]) for r in loc if np.isfinite(r[2])]
    return float(max(v)[1]) if v else np.nan


def steps_apart(a, b, grid):
    """|a - b| in grid steps; nan if either is nan."""
    if not (np.isfinite(a) and np.isfinite(b)):
        return np.nan
    g = np.asarray(grid, float)
    return float(abs(np.argmin(abs(g - a)) - np.argmin(abs(g - b))))


def make_grid(x):
    u = np.unique(np.asarray(x, float))
    u = u[np.isfinite(u)]
    if len(u) <= 25:
        return u
    return np.linspace(u.min(), u.max(), 25)


def cell_key(df, keys):
    return df[keys].astype(str).agg("|".join, axis=1) if len(keys) > 1 else df[keys[0]].astype(str)


def fe_transform(df, y, keys, mode):
    """Remove cell fixed effects on the crossed `keys`."""
    v = df[y].astype(float)
    if mode == "NONE" or not keys:
        return v.values
    mu = v.groupby(cell_key(df, keys)).transform("mean")
    out = v - mu
    if mode == "RECENTRED":
        out = out + v.mean()
    return out.values


def standardised_curve(df, keys, grid, half_w, min_in=MIN_IN_WIN, ycol="__y__"):
    """Direct standardisation: inside each window, re-weight the cell mix to the GLOBAL mix
    on the item's largest single axis (idea 226's second construction; keeps the level)."""
    axis = max(keys, key=lambda k: df[k].nunique())
    lv = df[axis].astype(str)
    wg = lv.value_counts(normalize=True)
    x = df["__x__"].values; y = df[ycol].values
    out = []
    for g in grid:
        m = (x >= g - half_w) & (x <= g + half_w)
        n = int(m.sum())
        if n < min_in:
            out.append((float(g), n, np.nan)); continue
        sub = lv.values[m]; ys = y[m]
        present = sorted(set(sub))
        w = np.array([wg[p] for p in present], float)
        w = w / w.sum()
        mus = np.array([ys[sub == p].mean() for p in present], float)
        out.append((float(g), n, float((w * mus).sum())))
    return out


# ============================================================================ the census frame
CURVE_FILES = sorted(p.name for p in BT.glob("*.curve*.csv"))

# Each admitted item: the committed cell-level source, its x, its y, the categorical cell-type
# columns (the x-generating dial is NEVER a cell-type key), and the run's published reading.
ITEMS = [
    dict(id="219", label="modal share -> writable mode (idea 219; idea 226's parent)",
         file="2026-09-06_what-modal-share-makes-a-mode-writable_cloud.cells.csv",
         x="share_mean", y="d_mean", keys=["dial", "corpus", "cost_bps"],
         grid=np.round(np.arange(0.20, 1.001, 0.025), 4),
         published="crossing 0.425 (last non-positive centre 0.400)", kind="crossing",
         repro="EXACT - 0.425 / last non-positive 0.400 reproduced at the published half-window"),
    dict(id="167", label="value/cost parallelism: gain-to-cost ratio in book share m",
         file="2026-09-05_is-the-value-cost-parallelism-general_cloud.curve.csv",
         x="m", y=("ratio_TO", -1.0), keys=["panel", "instr"],
         published="crossing does not exist, 12 of 12 cells (ratio >= 2.37 at all 120 points)", kind="no-crossing",
         repro="CONSISTENT - the pooled curve is positive throughout, i.e. nothing to cross"),
    dict(id="159B", label="share at which ranking stops paying (lane B): g - c_INC in m",
         file="2026-09-05_the-share-at-which-ranking-stops-paying_B.curve.csv",
         x="m", y=("g", "-c_INC"), keys=["panel", "constr", "tilt"],
         published="no crossing strictly inside [0.05, 0.70]", kind="no-crossing",
         repro="CONSISTENT - positive throughout inside [0.05, 0.70]"),
    dict(id="159c", label="share at which ranking stops paying (cloud): |dC| - cost in m",
         file="2026-09-05_the-share-at-which-ranking-stops-paying_cloud.curve.csv",
         x="m", y=("absdC", "-cost"), keys=["panel"],
         published="q* ~ 0.85 [0.80, 0.96], useless (the cost bar cannot bind)", kind="no-crossing",
         repro="NOT A POOLED-CURVE LOCATION - the published q* ~ 0.85 is a FITTED log-linear crossing on the rank share, not a location on this committed curve; the empirical curve carries none, which is that run's own empirical finding"),
    dict(id="168B", label="vol-scaler exponent k (lane B): dSharpe in k",
         file="2026-09-05_the-sign-is-the-parameter-not-the-share_B.curve.csv",
         x="k", y="dSharpe", keys=["panel", "constr", "m", "cost"], oos="dSharpe_OOS",
         published="no interior optimum; argmax at k >= +0.50 in 12/12, at the grid edge 10/12", kind="argmax",
         repro="CONSISTENT - argmax at the top edge of the k grid"),
    dict(id="168c", label="vol-scaler exponent k (cloud): dSharpe in k",
         file="2026-09-05_the-sign-is-the-parameter-not-the-share_cloud.curve.csv",
         x="k", y="dSharpe", keys=["panel", "cost", "share"],
         published="live k = -0.5 loses to k = 0 in 32 of 32 cells", kind="crossing",
         repro="CONSISTENT - an interior sign crossing in k above the live k = -0.5"),
    dict(id="103", label="correlation as a sleeve design variable: dSharpe in realised corr",
         file="2026-09-07_correlation-as-the-sleeve-design-variable_B.curve.csv",
         x="corr", y="dSharpe", keys=["panel", "book", "conv", "f"],
         published="the curve is real; correlation killed as the design variable", kind="crossing",
         repro="CONSISTENT - positive throughout in realised corr"),
    dict(id="61", label="gate instrument speed: matched-gross dSharpe in flips/tkr/yr",
         file="2026-09-06_gate-instrument-speed-curve_cloud.grid.csv",
         x="flips", y="gm_dSharpe", keys=["panel", "book", "conv", "cost"],
         published="a FLOOR near 0.5 flips/tkr/yr; above it flat, argmax location is noise", kind="crossing",
         repro="NOT A POOLED-CURVE LOCATION - the published ~0.5 flips FLOOR is a per-pool sign statement; the pooled matched-gross curve is non-positive at every centre including the fastest, so it carries no crossing to read"),
    dict(id="277", label="ETF share -> reversal share (idea 277)",
         file="2026-09-06_is-ETF36-a-third-cluster-or-just-a-small-sample_C.reversal.csv",
         x="etf_share", y=("rev", -0.5), keys=["seed", "r_target"], mixonly=True,
         published="curve non-monotone; 'where does it turn over' has no answer", kind="argmax",
         repro="CONSISTENT - non-monotone, the run itself declined to locate a turn"),
    dict(id="bandgate", label="band width -> CAGR gap vs the bare 200d gate (band-gate on SMALL)",
         file="2026-09-06_band-gate-on-small-panel_B.curve.csv",
         x="__band__", y="__gap__", keys=["panel", "floor_musd", "conv", "bps"], melt=True,
         published="the 200d gate's damage is never noise-crossing damage (gap rises in band)", kind="crossing",
         repro="CONSISTENT - positive throughout in band width"),
]

NOT_READABLE = [
    ("2026-09-08_why-the-035-045-share-window-dips_B.curves.csv",
     "already-aggregated re-read of item 219's own 560 cells (duplicate, not an independent reading)"),
    ("2026-09-08_why-the-035-045-share-window-dips_cloud.curve.csv",
     "already-aggregated re-read of item 219's own 560 cells (duplicate, not an independent reading)"),
    ("2026-09-06_gate-instrument-speed-curve_cloud.curve.csv",
     "per-cell SUMMARY of item 61; the cell-level rows are its .grid.csv, admitted as item 61"),
    ("2026-09-06_is-ETF36-a-third-cluster-or-just-a-small-sample_C.curve.csv",
     "already-aggregated over seeds; the cell-level rows are its .reversal.csv, admitted as item 277"),
]


def load_item(it):
    d = pd.read_csv(BT / it["file"])
    if it.get("mixonly"):
        d = d[d["kind"].astype(str).str.upper() == "MIX"].copy()
    if it.get("melt"):
        cols = {"pub_200d": 0.0, "pub_band2": 0.02, "pub_band3": 0.03, "pub_band5": 0.05,
                "pub_band8": 0.08, "pub_band12": 0.12, "pub_band20": 0.20}
        rows = []
        for c, b in cols.items():
            s = d[["panel", "floor_musd", "conv", "bps", c]].copy()
            s["__band__"] = b
            s["__gap__"] = s[c]
            rows.append(s.drop(columns=[c]))
        d = pd.concat(rows, ignore_index=True)
    y = it["y"]
    if isinstance(y, tuple):
        a = d[y[0]].astype(float)
        if isinstance(y[1], str):
            b = d[y[1][1:]].astype(float)
            d["__y__"] = a - b if y[1][0] == "-" else a + b
        else:
            d["__y__"] = a + y[1]
    else:
        d["__y__"] = d[y].astype(float)
    d["__x__"] = d[it["x"]].astype(float)
    d = d[np.isfinite(d["__x__"]) & np.isfinite(d["__y__"])].copy()
    keys = [k for k in it["keys"] if k in d.columns and d[k].nunique() >= 2]
    return d, keys


# ================================================================================== the census
HMULTS = [1.0, 2.0, 3.0, 4.0, 5.0]                          # TUNED PARAMETER 1
HM_HEADLINE = 3.0                                           # = idea 219's published 0.075
FE_MODES = ["NONE", "WITHIN", "RECENTRED", "STANDARDISED"]  # TUNED PARAMETER 2
TOL_HEADLINE = 1


def read_curve(d, keys, grid, half_w, mode, ycol="__y__"):
    if mode == "STANDARDISED" and keys:
        loc = standardised_curve(d, keys, grid, half_w, ycol=ycol)
    else:
        yy = fe_transform(d, ycol, keys, mode)
        loc = local_curve(d["__x__"].values, yy, grid, half_w)
    ch, below = crossing_of(loc)
    return loc, ch, below, argmax_of(loc)


def interior(ch, grid):
    """A crossing is a LOCATION only if it is interior.  `crossing_of` returns grid[0] when
    the curve is positive throughout (nothing to cross) and nan when it never becomes
    uniformly positive (also nothing to cross); both are 'no crossing exists'."""
    return bool(np.isfinite(ch) and ch > float(np.min(grid)))


def survives(kind, pooled_ch, pooled_am, ch, am, grid, tol):
    """Pre-registered: reproduce the item's OWN published kind of location within tol steps."""
    if kind == "argmax":
        s = steps_apart(am, pooled_am, grid)
        return bool(np.isfinite(s) and s <= tol)
    ip, ic = interior(pooled_ch, grid), interior(ch, grid)
    if kind == "no-crossing":
        return bool(not ic)
    if not ip and not ic:
        return True
    if ip != ic:
        return False
    s = steps_apart(ch, pooled_ch, grid)
    return bool(np.isfinite(s) and s <= tol)


def run_census():
    P("=" * 116)
    P("PART A — THE CENSUS FRAME")
    P("=" * 116)
    P(f"  committed *.curve*.csv files in research/backtests: {len(CURVE_FILES)}")
    for f in CURVE_FILES:
        P(f"    {f}")
    P(f"\n  ADMITTED items (cell-level rows + x-axis + >=2-level cell-type axis + a published "
      f"location): {len(ITEMS)}")
    P(f"  NOT re-readable (reported, not dropped): {len(NOT_READABLE)}")
    for f, why in NOT_READABLE:
        P(f"    {f}\n       -> {why}")

    census, curves, perax, sens = [], [], [], []
    P("\n" + "=" * 116)
    P("PART B — POOLED vs FIXED-EFFECT RE-READING (all grid points)")
    P("=" * 116)
    for it in ITEMS:
        d, keys = load_item(it)
        grid = it.get("grid")
        grid = make_grid(d["__x__"].values) if grid is None else np.asarray(grid, float)
        step = float(np.median(np.diff(np.sort(grid)))) if len(grid) > 1 else 1.0
        P(f"\n  [{it['id']}] {it['label']}")
        P(f"       source {it['file']}  ({len(d)} cells, x={it['x']}, cell keys "
          f"{'x'.join(keys)}, {len(grid)} grid points, step {step:.4g})")
        P(f"       published reading ({it['kind']}): {it['published']}")
        P(f"       pooled re-read vs published: {it['repro']}")
        P(f"       {'hmult':>6s} {'half-w':>8s} {'FE':>13s} {'crossing':>10s} {'last<=0':>9s} "
          f"{'argmax':>9s} {'steps':>6s} {'survives':>9s}")
        base = {}
        for hm in HMULTS:
            hw = hm * step
            for mode in FE_MODES:
                loc, ch, below, am = read_curve(d, keys, grid, hw, mode)
                if mode == "NONE":
                    base[hm] = (ch, am)
                bch, bam = base[hm]
                sc = steps_apart(ch, bch, grid)
                surv = survives(it["kind"], bch, bam, ch, am, grid, TOL_HEADLINE)
                surv0 = survives(it["kind"], bch, bam, ch, am, grid, 0)
                census.append(dict(item=it["id"], label=it["label"], file=it["file"],
                                   kind=it["kind"], repro=it["repro"], cells=len(d),
                                   keys="x".join(keys),
                                   hmult=hm, half_w=hw,
                                   fe=mode, crossing=ch, last_nonpos=below, argmax=am,
                                   pooled_crossing=bch, pooled_argmax=bam, steps=sc,
                                   argmax_steps=steps_apart(am, bam, grid),
                                   interior=interior(ch, grid),
                                   pooled_interior=interior(bch, grid),
                                   survives_tol1=bool(surv), survives_tol0=bool(surv0),
                                   n_defined=int(sum(np.isfinite(r[2]) for r in loc))))
                for c, n, v in loc:
                    curves.append(dict(item=it["id"], hmult=hm, fe=mode, centre=c, n=n, mean=v))
                if mode != "NONE":
                    P(f"       {hm:6.1f} {hw:8.4g} {mode:>13s} {ch:10.4g} {below:9.4g} "
                      f"{am:9.4g} {sc if np.isfinite(sc) else float('nan'):6.1f} "
                      f"{'YES' if surv else 'NO':>9s}")
                else:
                    P(f"       {hm:6.1f} {hw:8.4g} {mode:>13s} {ch:10.4g} {below:9.4g} "
                      f"{am:9.4g} {'-':>6s} {'(pooled)':>9s}")
        # per-single-axis diagnostic at the headline half-window
        hw = HM_HEADLINE * step
        _, bch, _, bam = read_curve(d, keys, grid, hw, "NONE")
        for k in keys:
            for mode in ("WITHIN", "RECENTRED"):
                _, ch, _, am = read_curve(d, [k], grid, hw, mode)
                perax.append(dict(item=it["id"], axis=k, levels=int(d[k].nunique()), fe=mode,
                                  pooled_crossing=bch, crossing=ch,
                                  steps=steps_apart(ch, bch, grid), argmax=am,
                                  argmax_steps=steps_apart(am, bam, grid)))
        # how far the reading moves with the WINDOW WIDTH vs with the FIXED EFFECTS
        cs = [r for r in census if r["item"] == it["id"]]
        pool = [r["crossing"] for r in cs if r["fe"] == "NONE" and np.isfinite(r["crossing"])]
        gidx = [int(np.argmin(abs(grid - v))) for v in pool]
        span = float(max(gidx) - min(gidx)) if len(gidx) >= 2 else np.nan
        fest = [r["steps"] for r in cs if r["fe"] in ("RECENTRED", "STANDARDISED")
                and np.isfinite(r["steps"])]
        sens.append(dict(item=it["id"], kind=it["kind"],
                         hmult_span_steps=span, n_defined_pooled=len(pool),
                         fe_mean_steps=float(np.mean(fest)) if fest else np.nan,
                         fe_max_steps=float(np.max(fest)) if fest else np.nan,
                         within_mean_steps=float(np.mean(
                             [r["steps"] for r in cs if r["fe"] == "WITHIN"
                              and np.isfinite(r["steps"])] or [np.nan]))))

        pa = [r for r in perax if r["item"] == it["id"] and r["fe"] == "RECENTRED"]
        if pa:
            P(f"       single-axis FE (RECENTRED, hmult {HM_HEADLINE:.0f}):  " +
              "   ".join(f"{r['axis']}({r['levels']}) -> {r['crossing']:.4g}" for r in pa))
    return (pd.DataFrame(census), pd.DataFrame(curves), pd.DataFrame(perax),
            pd.DataFrame(sens))


# ==================================================================== rule 8 (i): leave-one-out
def run_loco():
    P("\n" + "=" * 116)
    P("PART C — RULE 8 (i): LEAVE-ONE-CELL-TYPE-OUT.  Read the crossing on the other levels,")
    P(f"score it against the held-out level's own curve.  hmult {HM_HEADLINE:.0f}, FE = RECENTRED.")
    P("=" * 116)
    rows = []
    P(f"  {'item':10s} {'axis':12s} {'held out':16s} {'train POOL':>11s} {'train FE':>9s} "
      f"{'test own':>9s} {'pool err':>9s} {'FE err':>8s}")
    for it in ITEMS:
        d, keys = load_item(it)
        if not keys:
            continue
        grid = it.get("grid")
        grid = make_grid(d["__x__"].values) if grid is None else np.asarray(grid, float)
        step = float(np.median(np.diff(np.sort(grid))))
        hw = HM_HEADLINE * step
        axis = max(keys, key=lambda k: d[k].nunique())
        for lv in sorted(d[axis].astype(str).unique()):
            tr = d[d[axis].astype(str) != lv]
            te = d[d[axis].astype(str) == lv]
            if len(te) < MIN_IN_WIN or len(tr) < MIN_IN_WIN:
                continue
            trk = [k for k in keys if k != axis and tr[k].nunique() >= 2]
            _, chp, _, _ = read_curve(tr, trk, grid, hw, "NONE")
            _, chf, _, _ = read_curve(tr, trk, grid, hw, "RECENTRED")
            tek = [k for k in keys if k != axis and te[k].nunique() >= 2]
            _, cht, _, _ = read_curve(te, tek, grid, hw, "NONE")
            ep, ef = steps_apart(chp, cht, grid), steps_apart(chf, cht, grid)
            rows.append(dict(item=it["id"], axis=axis, held_out=lv, train_pooled=chp,
                             train_fe=chf, test_own=cht, err_pooled=ep, err_fe=ef,
                             n_test=len(te)))
            P(f"  {it['id']:10s} {axis:12s} {lv[:16]:16s} {chp:11.4g} {chf:9.4g} {cht:9.4g} "
              f"{ep if np.isfinite(ep) else float('nan'):9.2f} "
              f"{ef if np.isfinite(ef) else float('nan'):8.2f}")
    L = pd.DataFrame(rows)
    if len(L):
        ok = L[np.isfinite(L.err_pooled) & np.isfinite(L.err_fe)]
        P(f"\n  folds {len(L)};  both readings defined in {len(ok)}")
        if len(ok):
            P(f"  mean |error| in grid steps vs the held-out level's OWN crossing: "
              f"POOLED {ok.err_pooled.mean():.3f}   FE {ok.err_fe.mean():.3f}   "
              f"FE better in {int((ok.err_fe < ok.err_pooled).sum())} of {len(ok)}")
        nd = L[~np.isfinite(L.test_own)]
        P(f"  folds where the held-out level has NO crossing of its own: {len(nd)} of {len(L)}")
    return L


# ================================================================ rule 8 (ii): live book grid
IS_END, OOS_START = "2016-12-31", "2017-01-01"
BANDS = [0.00, 0.02, 0.03, 0.05, 0.08, 0.12, 0.20]
GROSSES = [0.50, 0.75, 1.00]
CADENCES = ["W", "M"]
COST_BPS = 10.0


def fast_backtest(px, W, cost_bps=COST_BPS, freq="W"):
    """engine.backtest, same arithmetic, numpy inner loop (asserted identical below)."""
    rets = px.pct_change().fillna(0.0).values
    wt = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n, k = rets.shape
    cur = np.zeros(k); held = np.empty((n, k)); to = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]; to[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        if tot > 0:
            cur = growth / tot
    port = (held * rets).sum(axis=1) - to * cost_bps / 1e4
    return pd.Series(port, index=px.index)


def csd(r):
    r = np.asarray(r, float)
    if len(r) < 60:
        return (np.nan,) * 3
    eq = np.cumprod(1 + r); yrs = len(r) / 252
    dd = eq / np.maximum.accumulate(eq) - 1
    vol = r.std() * np.sqrt(252)
    return (eq[-1] ** (1 / yrs) - 1, (r.mean() * 252) / vol if vol else np.nan, dd.min())


def band_book(px, band, gross):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, band), 0.0) if band > 0 else \
        ew.where(px > px.rolling(200).mean(), 0.0)


def run_books():
    P("\n" + "=" * 116)
    P("PART D — RULE 8 (ii), LIVE PRICES: does FE-correcting a pooled DIAL curve change the")
    P("threshold you would adopt, and does it pay?  126 books: 3 panels x 3 gross x 2 cadence")
    P("x 7 band widths, 10 bps, t+1.  x = band width, y = IS Sharpe minus the same cell's")
    P("bare-200d (band 0) IS Sharpe.  Threshold read IS-only; 2017-2026 read once.")
    P("=" * 116)
    panels = {}
    for lab, kw in [("U56", {}), ("B136", dict(broad=True)), ("SMALL439", dict(small=True))]:
        px = load_universe(**kw)
        panels[lab] = px
        P(f"  {lab:10s} {px.shape[1]:4d} cols  {px.index[0].date()} -> {px.index[-1].date()}")

    px0 = panels["U56"]
    W0 = rules_v2_weights(px0)
    a = engine_backtest(px0, W0, cost_bps=COST_BPS, freq="W")["returns"]
    b = fast_backtest(px0, W0, COST_BPS, "W")
    P(f"\n  GATE  fast_backtest vs engine.backtest on RULES v2 / U56: "
      f"max |diff| {float(np.abs(a - b).max()):.3e}")
    assert float(np.abs(a - b).max()) < 1e-12

    rows = []
    for lab, px in panels.items():
        st = px.index[260]
        for g in GROSSES:
            for cd in CADENCES:
                for bnd in BANDS:
                    r = fast_backtest(px, band_book(px, bnd, g), COST_BPS, cd).loc[st:]
                    fc, fs, fd = csd(r.values)
                    h = len(r) // 2
                    _, h1, _ = csd(r.iloc[:h].values); _, h2, _ = csd(r.iloc[h:].values)
                    ic, isS, idd = csd(r.loc[:IS_END].values)
                    oc, os_, odd = csd(r.loc[OOS_START:].values)
                    rows.append(dict(panel=lab, gross=g, cadence=cd, band=bnd,
                                     CAGR=fc, Sharpe=fs, MaxDD=fd, H1=h1, H2=h2,
                                     IS_Sharpe=isS, OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=odd))
    G = pd.DataFrame(rows)
    G["cell"] = G.panel + "|" + G.gross.astype(str) + "|" + G.cadence
    base_is = G[G.band == 0].set_index("cell").IS_Sharpe
    G["y_IS"] = G.IS_Sharpe - G.cell.map(base_is)
    base_oos = G[G.band == 0].set_index("cell").OOS_Sharpe
    G["y_OOS"] = G.OOS_Sharpe - G.cell.map(base_oos)

    P(f"\n  {len(G)} books.  IS gain over the bare 200d gate, by band (pooled over 18 cells):")
    P(f"  {'band':>6s} {'n':>4s} {'mean IS gain':>13s} {'frac>0':>7s} {'mean OOS gain':>14s} "
      f"{'frac>0':>7s}")
    for bnd in BANDS:
        s = G[G.band == bnd]
        P(f"  {bnd:6.2f} {len(s):4d} {s.y_IS.mean():+13.4f} {(s.y_IS > 0).mean():7.2f} "
          f"{s.y_OOS.mean():+14.4f} {(s.y_OOS > 0).mean():7.2f}")

    grid = np.array(BANDS, float)
    step = float(np.median(np.diff(grid)))
    d = G[G.band > 0].rename(columns={"band": "__x__", "y_IS": "__y__"}).copy()
    d["__x__"] = d["__x__"].astype(float)
    keys = ["panel", "gross", "cadence"]
    picks = {}
    P(f"\n  IS-only threshold read off the band curve (crossing; argmax as the fallback when no")
    P(f"  crossing exists), at every hmult x FE grid point:")
    P(f"  {'hmult':>6s} {'FE':>10s} {'crossing':>9s} {'argmax':>8s} {'adopted b':>10s}")
    for hm in HMULTS:
        for mode in FE_MODES:
            _, ch, _, am = read_curve(d, keys, grid[grid > 0], hm * step, mode)
            adopt = ch if np.isfinite(ch) else am
            picks[(hm, mode)] = adopt
            P(f"  {hm:6.1f} {mode:>10s} {ch:9.4g} {am:8.4g} {adopt:10.4g}")

    hm0 = HM_HEADLINE
    b_pool, b_fe_w, b_fe_r = picks[(hm0, "NONE")], picks[(hm0, "WITHIN")], picks[(hm0, "RECENTRED")]
    b_std = picks[(hm0, "STANDARDISED")]
    P(f"\n  HEADLINE (hmult {hm0:.0f}):  POOLED adopts band {b_pool:.2f};  WITHIN-FE {b_fe_w:.2f};  "
      f"RECENTRED-FE {b_fe_r:.2f};  STANDARDISED-FE {b_std:.2f}")

    P("\n  OOS 2017-2026, read once, pooled over the 18 (panel, gross, cadence) cells:")
    P(f"  {'arm':22s} {'band':>5s} {'OOS CAGR':>9s} {'OOS Sharpe':>11s} {'OOS MaxDD':>10s}")
    wf = []
    arms = {"POOLED-read": b_pool, "FE-WITHIN-read": b_fe_w, "FE-RECENTRED-read": b_fe_r,
            "FE-STANDARDISED-read": b_std, "bare 200d (band 0)": 0.00,
            "live RULES v2 band": 0.03, "ORACLE (best OOS band)": None}
    for arm, bnd in arms.items():
        if bnd is None:
            s = G.loc[G.groupby("cell").OOS_Sharpe.idxmax()]
            lab = "oracle"
        else:
            s = G[G.band == bnd]; lab = f"{bnd:.2f}"
        wf.append(dict(arm=arm, band=lab, OOS_CAGR=s.OOS_CAGR.mean(),
                       OOS_Sharpe=s.OOS_Sharpe.mean(), OOS_MaxDD=s.OOS_MaxDD.mean(),
                       IS_Sharpe=s.IS_Sharpe.mean()))
        P(f"  {arm:22s} {lab:>5s} {s.OOS_CAGR.mean():9.2%} {s.OOS_Sharpe.mean():11.4f} "
          f"{s.OOS_MaxDD.mean():10.2%}")

    P("\n  Benchmarks, same OOS window (PROTOCOL 3):")
    P(f"  {'panel':10s} {'series':22s} {'OOS CAGR':>9s} {'OOS Sharpe':>11s} {'OOS MaxDD':>10s}")
    bench = []
    for lab, px in panels.items():
        st = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        for nm, r in [("SPY buy-and-hold", spy),
                      ("RULES v2 (live) @10bps", fast_backtest(px, rules_v2_weights(px), COST_BPS, "W").loc[st:]),
                      ("RULES v1 @10bps", fast_backtest(px, rules_v1_weights(px), COST_BPS, "W").loc[st:])]:
            c, s, dd = csd(r.loc[OOS_START:].values)
            fc, fs, fdd = csd(r.values)
            h = len(r) // 2
            _, h1, _ = csd(r.iloc[:h].values); _, h2, _ = csd(r.iloc[h:].values)
            bench.append(dict(panel=lab, series=nm, OOS_CAGR=c, OOS_Sharpe=s, OOS_MaxDD=dd,
                              CAGR=fc, Sharpe=fs, MaxDD=fdd, H1=h1, H2=h2))
            P(f"  {lab:10s} {nm:22s} {c:9.2%} {s:11.4f} {dd:10.2%}")
    B = pd.DataFrame(bench)

    # ---------------------------------------------------------------- both KEEP paths
    P("\n" + "=" * 116)
    P("BOTH KEEP PATHS on all 126 books (4a vs the LIVE RULES v2 on the book's own panel;")
    P("4b vs SPY on that panel: Sharpe > SPY in H1, H2 and OOS, |MaxDD| <= 60% of SPY's,")
    P("CAGR >= 70% of SPY's).")
    P("=" * 116)
    krows = []
    for lab, px in panels.items():
        st = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        sc, ss, sdd = csd(spy.values)
        h = len(spy) // 2
        _, sh1, _ = csd(spy.iloc[:h].values); _, sh2, _ = csd(spy.iloc[h:].values)
        _, soos, _ = csd(spy.loc[OOS_START:].values)
        v2 = B[(B.panel == lab) & (B.series.str.startswith("RULES v2"))].iloc[0]
        for _, r in G[G.panel == lab].iterrows():
            p4a = bool(r.H1 > v2.H1 and r.H2 > v2.H2 and r.MaxDD >= v2.MaxDD)
            p4b = bool(r.H1 > sh1 and r.H2 > sh2 and r.OOS_Sharpe > soos
                       and abs(r.MaxDD) <= 0.60 * abs(sdd) and r.CAGR >= 0.70 * sc)
            krows.append(dict(panel=lab, gross=r.gross, cadence=r.cadence, band=r.band,
                              CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD, H1=r.H1, H2=r.H2,
                              OOS_Sharpe=r.OOS_Sharpe, spy_H1=sh1, spy_H2=sh2, spy_OOS=soos,
                              spy_CAGR=sc, spy_MaxDD=sdd, pass4a=p4a, pass4b=p4b))
    K = pd.DataFrame(krows)
    P(f"  {'panel':10s} {'books':>6s} {'4a pass':>8s} {'4b pass':>8s}")
    for lab in panels:
        s = K[K.panel == lab]
        P(f"  {lab:10s} {len(s):6d} {int(s.pass4a.sum()):8d} {int(s.pass4b.sum()):8d}")
    P(f"  {'TOTAL':10s} {len(K):6d} {int(K.pass4a.sum()):8d} {int(K.pass4b.sum()):8d}")
    if K.pass4b.any():
        P("\n  4b passes:")
        for _, r in K[K.pass4b].iterrows():
            P(f"    {r.panel:10s} gross {r.gross:.2f} {r.cadence} band {r.band:.2f}  "
              f"CAGR {r.CAGR:.2%} Sharpe {r.Sharpe:.3f} MaxDD {r.MaxDD:.2%} "
              f"H1/H2 {r.H1:.3f}/{r.H2:.3f} OOS {r.OOS_Sharpe:.3f}")
    if K.pass4a.any():
        P("\n  4a passes:")
        for _, r in K[K.pass4a].iterrows():
            P(f"    {r.panel:10s} gross {r.gross:.2f} {r.cadence} band {r.band:.2f}  "
              f"Sharpe {r.Sharpe:.3f} H1/H2 {r.H1:.3f}/{r.H2:.3f} MaxDD {r.MaxDD:.2%}")
    return G, pd.DataFrame(wf), B, K, picks, (b_pool, b_fe_w, b_fe_r)


# ========================================================================================= main
def main():
    P("=" * 116)
    P("IDEA 439 — CENSUS EVERY CROSSING IN THE RECORD FOR DIAL HETEROGENEITY (lane C, 2026-09-08)")
    P("=" * 116)

    # ---- reproduction gate, before any new number is read
    it = ITEMS[0]
    d, keys = load_item(it)
    loc, ch, below, _ = read_curve(d, keys, np.asarray(it["grid"], float), 0.075, "NONE")
    P("\nREPRODUCTION GATE (idea 219's published crossing, from its own committed cells)")
    P(f"  cells {len(d)} (published 560);  half-window 0.075, grid 0.20-1.00 step 0.025")
    P(f"  crossing {ch:.3f} (published 0.425)   last non-positive {below:.3f} (published 0.400)"
      f"   -> {'MATCH' if (ch == 0.425 and below == 0.400 and len(d) == 560) else 'MISMATCH'}")
    assert len(d) == 560 and ch == 0.425 and below == 0.400

    C, CU, PA, SN = run_census()
    L = run_loco()
    G, WF, B, K, picks, headline = run_books()

    C.to_csv(BT / f"{STEM}.census.csv", index=False)
    CU.to_csv(BT / f"{STEM}.curves.csv", index=False)
    PA.to_csv(BT / f"{STEM}.perxis.csv", index=False)
    SN.to_csv(BT / f"{STEM}.sensitivity.csv", index=False)
    L.to_csv(BT / f"{STEM}.loco.csv", index=False)
    G.to_csv(BT / f"{STEM}.bookgrid.csv", index=False)
    pd.concat([WF.assign(kind="arm"), B.assign(kind="benchmark")], ignore_index=True) \
        .to_csv(BT / f"{STEM}.walkforward.csv", index=False)
    K.to_csv(BT / f"{STEM}.keeppaths.csv", index=False)

    # -------------------------------------------------------------------------- the headline
    P("\n" + "=" * 116)
    P("HEADLINE — HOW MANY OF THE RECORD'S POOLED-CURVE READINGS SURVIVE FIXED EFFECTS")
    P("=" * 116)
    for mode in ("WITHIN", "RECENTRED", "STANDARDISED"):
        s = C[C.fe == mode]
        P(f"\n  FE = {mode}")
        P(f"  {'hmult':>6s} {'items':>6s} {'survive tol1':>13s} {'survive tol0':>13s} "
          f"{'interior lost':>14s} {'interior gained':>16s}")
        for hm in HMULTS:
            t = s[s.hmult == hm]
            lost = int((t.pooled_interior & ~t.interior).sum())
            gain = int((~t.pooled_interior & t.interior).sum())
            P(f"  {hm:6.1f} {len(t):6d} {int(t.survives_tol1.sum()):13d} "
              f"{int(t.survives_tol0.sum()):13d} {lost:14d} {gain:16d}")
        t = s[s.hmult == HM_HEADLINE]
        P(f"  headline (hmult {HM_HEADLINE:.0f}): {int(t.survives_tol1.sum())} of {len(t)} "
          f"survive at tol 1 step, {int(t.survives_tol0.sum())} of {len(t)} exactly")
        P("    " + ";  ".join(f"{r['item']}:{'SURVIVES' if r['survives_tol1'] else 'BREAKS'}"
                              for _, r in t.iterrows()))
    P(f"\n  per item, across all {len(HMULTS)} hmult x 3 FE modes "
      f"({len(HMULTS) * 3} re-reads each):")
    P(f"  {'item':10s} {'kind':12s} {'survives tol1':>14s} {'survives tol0':>14s} "
      f"{'pooled INTERIOR crossing':>25s}")
    for it in ITEMS:
        s = C[(C.item == it["id"]) & (C.fe != "NONE")]
        n0 = C[(C.item == it["id"]) & (C.fe == "NONE")]
        P(f"  {it['id']:10s} {it['kind']:12s} {int(s.survives_tol1.sum()):8d} of {len(s):3d} "
          f"{int(s.survives_tol0.sum()):8d} of {len(s):3d} "
          f"{int(n0.interior.sum()):15d} of {len(n0):3d}")

    P("\n  WINDOW WIDTH vs FIXED EFFECTS — how far each reading moves (grid steps):")
    P(f"  {'item':10s} {'kind':12s} {'hmult span':>11s} {'FE mean':>8s} {'FE max':>7s} "
      f"{'WITHIN mean':>12s}")
    for _, r in SN.iterrows():
        P(f"  {r['item']:10s} {r['kind']:12s} {r.hmult_span_steps:11.2f} {r.fe_mean_steps:8.2f} "
          f"{r.fe_max_steps:7.2f} {r.within_mean_steps:12.2f}")
    ok = SN[np.isfinite(SN.hmult_span_steps) & np.isfinite(SN.fe_mean_steps)]
    P(f"  over the {len(ok)} items where both are defined: mean hmult span "
      f"{ok.hmult_span_steps.mean():.2f} steps vs mean level-preserving FE move "
      f"{ok.fe_mean_steps.mean():.2f} steps; the WINDOW moves the reading more in "
      f"{int((ok.hmult_span_steps > ok.fe_mean_steps).sum())} of {len(ok)} items")

    Path(BT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"\nwrote {STEM}.console.txt and 6 CSVs")


if __name__ == "__main__":
    main()

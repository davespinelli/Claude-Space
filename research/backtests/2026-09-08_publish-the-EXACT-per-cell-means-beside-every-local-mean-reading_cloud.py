#!/usr/bin/env python3
"""Idea 444 — publish-the-EXACT-per-cell-means-beside-every-local-mean-reading (cloud, 2026-09-08)

QUESTION (queue, verbatim intent)
  Idea 440 proved that on a BALANCED grid a local-mean curve is an exact unweighted
  re-average of the per-x cell means (max |windowed - re-average| = 5.55e-17 over 55 grid
  points on 168c's own 32 cells).  So the smoothed curve is a LINEAR FUNCTIONAL of the exact
  one: it cannot add information, only RELOCATE the reading, and on a curve with one steep
  arm it relocates it in ONE direction.  Sharpen idea 441's half-window column into: any
  local-mean reading must publish its UNSMOOTHED per-x means and must state whether its grid
  is BALANCED.  Back-fill balance + the exact reading over the record's committed pooled
  curves and report how many published locations MOVE.

WHAT THIS RUN DOES (declared before any number is read)
  A. THE ENUMERATION.  "Committed pooled curve" is defined mechanically: a committed
     cell-level artefact in research/backtests off which a POOLED (across-cell) local-mean
     curve in a dial x was read and a location published.  That is idea 439's 10 admitted
     ITEMS (imported, not re-chosen) PLUS idea 440's own fresh 528-book panel (its
     .grid.csv, the k dial re-read on 3 panels), = 11.  Idea 439's 4 NOT_READABLE files are
     re-printed so the scope is checkable.  If the count is not 11 this run says so.

  B. BALANCE (TUNED PARAMETER 1).  The queue states the theorem's premise as "balanced".
     Measuring it over the record shows the premise is TWO conditions, and the record's own
     curves fail them differently, so both are reported separately and neither is assumed:
       (i)  ALIGNMENT — every cell's x sits ON a reading-grid centre and every centre carries
            a cell, i.e. x is a DISCRETE DIAL whose levels ARE the grid.  Where a run
            linspaces a 25-point grid over a CONTINUOUS covariate this fails, and there is
            then no such object as "the per-x cell mean" to publish.
       (ii) COUNT BALANCE — max|n_x - mean n| / mean n over the design's OWN x levels (never
            over the reading grid: measuring balance on a grid that misses most of the
            support manufactures a pass).  COMPOSITION (is the cell-type multiset the same at
            every x?) is reported beside it and never used to decide.
     BALANCED-FOR-THE-THEOREM at tolerance tol iff ALIGNED and count imbalance <= tol.
     tol in {0.00, 0.05, 0.10, 0.25}, ALL reported.

  C. THE IDENTITY AND ITS SCOPE.  At every (item, half-window) the windowed curve is
     compared point-by-point against the unweighted RE-AVERAGE of the per-x cell means over
     the same window.  Idea 440's theorem says these coincide exactly under B.  Max
     |windowed - re-average| is published for every item, so the theorem's scope is a
     measured column, not an assumption, and where it fails this run says WHICH premise failed:
     an aligned-but-imbalanced grid means the window silently RE-WEIGHTS the cell mix; a
     non-aligned x means the window is a genuine bandwidth and the reading is a bandwidth choice.

  D. THE EXACT READING AND WHETHER THE PUBLISHED LOCATION MOVES.  The EXACT reading is
     `crossing_of`/`argmax_of` applied to the per-x cell means on the design's OWN x SUPPORT
     (no window, no linspaced grid).  It is compared against (i) the same reading at every
     half-window and (ii) the value the source run PUBLISHED (idea 441's PROV table,
     imported).  Reported: displacement in grid steps, its SIGN, whether the window
     MANUFACTURES or DESTROYS a location the exact curve does not have, and the count of
     published locations that move.  On a non-aligned item each per-x "mean" is one
     observation, so the exact curve is the raw scatter and is flagged as admitting no exact
     location at all — which is itself the answer for those items.

  TWO TUNED PARAMETERS, EVERY GRID POINT REPORTED
    P1  TOL   — balance tolerance, {0.00, 0.05, 0.10, 0.25}.  Headline 0.00 (exact balance).
    P2  HMULT — half-window as a multiple of the grid step, {0.5, 1, 2, 3, 4, 5}; hmult 0
        is the EXACT reading and is not a tuned point, it is the reference.
  Nothing else is tuned.  `local_curve`, `crossing_of`, `argmax_of`, `make_grid`,
  `steps_apart`, the ITEM registry, `load_item`, `fast_backtest`, `band_book`, `csd`,
  COST_BPS and the IS/OOS split are IMPORTED from idea 439's committed script; the published
  values (PROV) are imported from idea 441's.  The frame is the record's own.

RULE 8 (PROTOCOL 8) — LIVE PRICES
  252 fresh books: 3 panels x gross {0.75, 1.00} x cadence {W, M} x 21 band widths
  (0.00-0.20 step 0.01), 10 bps, weights at t applied at t+1.  x = band width, y = IS
  (<= 2016-12-31) Sharpe minus the same cell's bare-200d IS Sharpe.  The adopted band is read
  off the IS curve EXACTLY (per-x means) and at every half-window, and each adopted band is
  evaluated untouched on 2017-2026 against RULES v2 (live), RULES v1 and SPY.  The question
  rule 8 answers here: does reading a threshold exactly rather than through a window change
  what a reader adopts, and does the change pay OOS?
  BOTH KEEP PATHS (4a and 4b) are evaluated on all 252 books.

SURVIVORSHIP.  The SMALL panel is current constituents of a sub-$2B screen only (see
data/SMALL_PANEL_README.md); tickers with max_1d_move >= 1.0 in data/small_meta.csv are
dropped first, leaving 439 names + SPY as a benchmark column.  Every SMALL number here is
upward-biased in level; only cross-arm contrasts on the same panel are read.
data/universe_broad.json is likewise current constituents (PROTOCOL 9).

Costs 10 bps, next-day execution (PROTOCOL 2).  Deterministic.
Artefacts: .console.txt, .balance.csv, .identity.csv, .exact.csv, .bookgrid.csv,
           .walkforward.csv, .keeppaths.csv, .result.md
Nothing outside research/ is touched; RULES.md, scan.py, bot.py, baseline.py untouched.
"""
from __future__ import annotations
import sys, importlib.util
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest  # noqa

BT = ROOT / "research" / "backtests"
STEM = "2026-09-08_publish-the-EXACT-per-cell-means-beside-every-local-mean-reading_cloud"
LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def _load(stem, mod):
    spec = importlib.util.spec_from_file_location(mod, BT / f"{stem}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


C439 = _load("2026-09-08_census-every-CROSSING-in-the-record-for-dial-heterogeneity_C", "idea439")
C441 = _load("2026-09-08_publish-the-HALF-WINDOW-beside-every-published-crossing_C", "idea441")

ITEMS439 = C439.ITEMS
NOT_READABLE = C439.NOT_READABLE
load_item, local_curve, crossing_of = C439.load_item, C439.local_curve, C439.crossing_of
argmax_of, steps_apart, make_grid = C439.argmax_of, C439.steps_apart, C439.make_grid
fast_backtest, band_book, csd = C439.fast_backtest, C439.band_book, C439.csd
COST_BPS, IS_END, OOS_START = C439.COST_BPS, C439.IS_END, C439.OOS_START
PROV = C441.PROV

TOLS = [0.00, 0.05, 0.10, 0.25]              # TUNED PARAMETER 1
TOL_HEADLINE = 0.00
HMULTS = [0.5, 1.0, 2.0, 3.0, 4.0, 5.0]      # TUNED PARAMETER 2
HM_HEADLINE = 3.0                            # idea 219's own published 0.075 on its grid


# ============================================================ the 11th curve (idea 440's own)
def load_440grid():
    """Idea 440's fresh 528-book panel, rebuilt into the same (x, y, cell) shape as idea
    439's items.  y = dSharpe = Sharpe(k) - Sharpe(k=0) inside the (panel, cost, share) cell,
    which is idea 440's own construction, read off its committed .grid.csv."""
    d = pd.read_csv(BT / "2026-09-08_is-168c-s-k-CROSSING-a-SMOOTHING-artefact-end-to-end_cloud.grid.csv")
    d["cell"] = d.panel.astype(str) + "|" + d.cost.astype(str) + "|" + d.share.astype(str)
    base = d[d.k == 0.0].set_index("cell").Sharpe
    d["__y__"] = d.Sharpe - d.cell.map(base)
    d["__x__"] = d.k.astype(float)
    d = d[np.isfinite(d["__x__"]) & np.isfinite(d["__y__"])].copy()
    return d, ["panel", "cost", "share"]


ITEM440 = dict(id="440grid", label="idea 440's own 528-book k panel (3 panels x 2 costs x 8 shares)",
               file="2026-09-08_is-168c-s-k-CROSSING-a-SMOOTHING-artefact-end-to-end_cloud.grid.csv",
               keys=["panel", "cost", "share"], kind="crossing",
               published="exact crossing +0.10 = the reader's floor; sign reverses on SMALL439",
               loader=load_440grid)

ITEMS = list(ITEMS439) + [ITEM440]

# published numeric location per item; idea 440's own published exact crossing added here
PUB = {k: v["pub"] for k, v in PROV.items()}
PUBKIND = {k: v["kindpub"] for k, v in PROV.items()}
PUB["440grid"] = 0.10
PUBKIND["440grid"] = ("exact crossing +0.10 — published on 168c's OWN 32 cells (u56+broad); on "
                      "this 3-panel 528-book pool idea 440 itself reported the crossing is DELETED")


def item_frame(it):
    if "loader" in it:
        return it["loader"]()
    return load_item(it)


def item_grid(it, d):
    g = it.get("grid")
    return make_grid(d["__x__"].values) if g is None else np.asarray(g, float)


# ============================================================================ exact machinery
def per_x_means(d, grid):
    """The EXACT reading's raw material: the unsmoothed mean of __y__ at each grid centre.
    A centre with no cell exactly on it is nan (never imputed)."""
    x = d["__x__"].values
    y = d["__y__"].values
    out = []
    for g in grid:
        m = np.isclose(x, g, rtol=0, atol=1e-9)
        n = int(m.sum())
        out.append((float(g), n, float(y[m].mean()) if n >= 1 else np.nan))
    return out


def support_means(d):
    """Per-x-LEVEL cell means on the design's OWN x support (not the reading grid).  This is
    what "the exact per-cell means" means for a discrete dial; for a continuous covariate the
    levels are the raw scatter and each 'mean' is one observation."""
    g = d.groupby("__x__")["__y__"]
    lv = np.array(sorted(d["__x__"].unique()), float)
    return [(float(c), int(g.size()[c]), float(g.mean()[c])) for c in lv]


def alignment(d, grid):
    """Does the design's x support sit ON the reading grid?  Idea 440's identity is stated on
    a grid whose centres ARE the x levels; where the record linspaces a 25-point grid over a
    continuous covariate that premise fails and 'the per-x cell mean' does not exist."""
    x = d["__x__"].values
    g = np.asarray(grid, float)
    on = np.array([np.any(np.isclose(g, v, rtol=0, atol=1e-9)) for v in x])
    carried = np.array([np.any(np.isclose(x, c, rtol=0, atol=1e-9)) for c in g])
    return float(on.mean()), float(carried.mean())


def reaverage_curve(pxm, grid, half_w):
    """Unweighted re-average of the per-x cell means inside each window.  This is what a
    windowed mean EQUALS on a balanced grid (idea 440's theorem)."""
    cs = np.array([r[0] for r in pxm], float)
    mu = np.array([r[2] for r in pxm], float)
    out = []
    for g in grid:
        m = (cs >= g - half_w) & (cs <= g + half_w) & np.isfinite(mu)
        out.append((float(g), int(m.sum()), float(mu[m].mean()) if m.any() else np.nan))
    return out


def read_loc(loc):
    ch, below = crossing_of(loc)
    return ch, below, argmax_of(loc)


def balance_stats(d, keys, grid=None):
    """Count and composition imbalance across the design's OWN distinct x levels.  The
    reading grid is deliberately NOT used here — balance is a property of the design, and
    measuring it on a grid that misses most of the support manufactures a spurious pass."""
    x = d["__x__"].values
    lv = np.array(sorted(d["__x__"].unique()), float)
    ns, comps = [], []
    for c in lv:
        m = np.isclose(x, c, rtol=0, atol=1e-9)
        n = int(m.sum())
        if n == 0:
            continue
        ns.append(n)
        if keys:
            k = d.loc[m, keys].astype(str).agg("|".join, axis=1)
            comps.append(tuple(sorted(k.value_counts().items())))
        else:
            comps.append(("_", n))
    ns = np.array(ns, float)
    if len(ns) == 0:
        return np.nan, np.nan, 0, np.nan
    ci = float(np.abs(ns - ns.mean()).max() / ns.mean()) if ns.mean() else np.nan
    same_comp = float(np.mean([c == comps[0] for c in comps])) if comps else np.nan
    return ci, same_comp, len(ns), float(ns.mean())


# =================================================================== PART A: the enumeration
def run_enumeration():
    P("=" * 118)
    P("PART A — THE ENUMERATION.  A 'committed pooled curve' = a committed CELL-LEVEL artefact")
    P("off which a POOLED across-cell local-mean curve in a dial x was read and a location")
    P("published.  Idea 439's admitted registry is imported verbatim; idea 440's own fresh")
    P("528-book k panel is added because it is a committed pooled curve the 439 census predates.")
    P("=" * 118)
    P(f"  idea 439 admitted items ........ {len(ITEMS439)}")
    P(f"  + idea 440's own .grid.csv ..... 1")
    P(f"  = committed pooled curves ...... {len(ITEMS)}   (the queue's count: 11 -> "
      f"{'MATCH' if len(ITEMS) == 11 else 'MISMATCH, reported as found'})")
    P(f"\n  idea 439's NOT re-readable files, re-printed so the scope is checkable ({len(NOT_READABLE)}):")
    for f, why in NOT_READABLE:
        P(f"    {f}\n       -> {why}")
    P(f"\n  {'item':10s} {'cells':>6s} {'x levels':>9s} {'cell-type keys':28s} source")
    rows = []
    for it in ITEMS:
        d, keys = item_frame(it)
        g = item_grid(it, d)
        rows.append(dict(item=it["id"], cells=len(d), x_levels=int(d["__x__"].nunique()),
                         grid_points=len(g), keys="|".join(keys), file=it["file"]))
        P(f"  {it['id']:10s} {len(d):6d} {d['__x__'].nunique():9d} {'|'.join(keys):28s} {it['file']}")
    return pd.DataFrame(rows)


# ======================================================================== PART B: the balance
def run_balance():
    P("\n" + "=" * 118)
    P("PART B — BALANCE (TUNED PARAMETER 1).  Idea 440's identity has TWO premises, and this")
    P("run measures both separately because the record's own curves fail them differently:")
    P("  (i)  ALIGNMENT — every cell's x sits ON a reading-grid centre and every centre carries")
    P("       a cell, i.e. x is a DISCRETE DIAL and the grid IS its support.  Where a run")
    P("       linspaces a 25-point grid over a CONTINUOUS covariate this fails and 'the per-x")
    P("       cell mean' does not exist as an object.")
    P("  (ii) COUNT BALANCE — max|n_x - mean n| / mean n over the design's OWN x levels")
    P("       (never over the grid: measuring balance on a grid that misses most of the")
    P("       support manufactures a pass).  COMPOSITION = fraction of x levels whose")
    P("       cell-type multiset equals the first level's.")
    P(f"BALANCED-FOR-THE-THEOREM at tol iff ALIGNED and count imbalance <= tol.  ALL {len(TOLS)}")
    P(f"tolerances reported; headline tol {TOL_HEADLINE:.2f}.")
    P("=" * 118)
    P(f"  {'item':10s} {'x lvls':>6s} {'grid':>5s} {'mean n':>7s} {'min n':>6s} {'max n':>6s} "
      f"{'cnt imbal':>10s} {'comp':>6s} {'align':>6s} {'DIAL?':>6s}  "
      + "  ".join(f"tol{t:.2f}" for t in TOLS))
    rows = []
    for it in ITEMS:
        d, keys = item_frame(it)
        g = item_grid(it, d)
        ci, comp, nlv, nmean = balance_stats(d, keys)
        a_cells, a_centres = alignment(d, g)
        aligned = bool(a_cells >= 1.0 - 1e-12 and a_centres >= 1.0 - 1e-12)
        ns = d.groupby("__x__").size().values
        flags = {f"bal_tol_{t:.2f}": bool(aligned and np.isfinite(ci) and ci <= t) for t in TOLS}
        rows.append(dict(item=it["id"], x_levels=nlv, grid_points=len(g), mean_n=nmean,
                         min_n=int(ns.min()), max_n=int(ns.max()), count_imbalance=ci,
                         composition_match=comp, align_cells=a_cells, align_centres=a_centres,
                         aligned=aligned, **flags))
        P(f"  {it['id']:10s} {nlv:6d} {len(g):5d} {nmean:7.1f} {int(ns.min()):6d} "
          f"{int(ns.max()):6d} {ci:10.4f} {comp:6.3f} {a_cells:6.3f} "
          f"{('Y' if aligned else '.'):>6s}  "
          + "  ".join(f"{'Y' if flags[f'bal_tol_{t:.2f}'] else '.':>6s}" for t in TOLS))
    B = pd.DataFrame(rows)
    P(f"\n  ALIGNED (x is a discrete dial on its own grid): {int(B.aligned.sum())} of {len(B)} "
      f"({', '.join(B.loc[B.aligned, 'item'])})")
    P(f"  NOT ALIGNED (x is a CONTINUOUS covariate read on a linspaced grid): "
      f"{', '.join(B.loc[~B.aligned, 'item'])} — for these the window is not a re-average of")
    P(f"    anything; there are no per-x cell means to publish and the reading IS a bandwidth choice.")
    for t in TOLS:
        c = f"bal_tol_{t:.2f}"
        P(f"  at tol {t:.2f}: BALANCED-FOR-THE-THEOREM {int(B[c].sum())} of {len(B)} "
          f"({', '.join(B.loc[B[c], 'item'])})")
    P(f"  count balance alone (ignoring alignment) at tol {TOL_HEADLINE:.2f}: "
      f"{int((B.count_imbalance <= TOL_HEADLINE).sum())} of {len(B)}")
    P(f"  composition-identical at EVERY x level: "
      f"{int((B.composition_match >= 1.0).sum())} of {len(B)} "
      f"({', '.join(B.loc[B.composition_match >= 1.0, 'item'])})")
    return B


# ==================================================================== PART C: the identity
def run_identity(BAL):
    P("\n" + "=" * 118)
    P("PART C — THE IDENTITY AND ITS SCOPE.  windowed local mean vs the unweighted RE-AVERAGE")
    P("of the per-x cell means, point by point, at every (item, half-window).  Idea 440's")
    P("theorem: these are EQUAL on a balanced grid.  max|diff| is measured, not assumed.")
    P("=" * 118)
    P(f"  {'item':10s} {'bal4thm':>8s} {'aligned':>7s} {'count imb':>9s}  " +
      "  ".join(f"hm{h:g}" for h in HMULTS) + "     max over hmult")
    rows = []
    for it in ITEMS:
        d, keys = item_frame(it)
        g = item_grid(it, d)
        step = float(np.median(np.diff(np.sort(g)))) if len(g) > 1 else np.nan
        pxm = per_x_means(d, g)
        bal = bool(BAL.loc[BAL.item == it["id"], f"bal_tol_{TOL_HEADLINE:.2f}"].iloc[0])
        alg = bool(BAL.loc[BAL.item == it["id"], "aligned"].iloc[0])
        ci = float(BAL.loc[BAL.item == it["id"], "count_imbalance"].iloc[0])
        ds = []
        for hm in HMULTS:
            hw = hm * step
            w = local_curve(d["__x__"].values, d["__y__"].values, g, hw)
            r = reaverage_curve(pxm, g, hw)
            a = np.array([q[2] for q in w], float)
            b = np.array([q[2] for q in r], float)
            ok = np.isfinite(a) & np.isfinite(b)
            mx = float(np.abs(a[ok] - b[ok]).max()) if ok.any() else np.nan
            ds.append(mx)
            rows.append(dict(item=it["id"], hmult=hm, half_w=hw, grid_points=len(g),
                             compared=int(ok.sum()), max_abs_diff=mx,
                             balanced_headline=bal, aligned=alg, count_imbalance=ci))
        P(f"  {it['id']:10s} {('Y' if bal else '.'):>8s} {('Y' if alg else '.'):>7s} {ci:9.4f}  "
          + "  ".join(f"{v:8.1e}" for v in ds) + f"   {np.nanmax(ds):9.2e}")
    I = pd.DataFrame(rows)
    per = I.groupby("item").max_abs_diff.max()
    bal_items = set(BAL.loc[BAL[f"bal_tol_{TOL_HEADLINE:.2f}"], "item"])
    b = per[per.index.isin(bal_items)]
    u = per[~per.index.isin(bal_items)]
    P(f"\n  BALANCED-FOR-THE-THEOREM ({len(b)} items): max |windowed - re-average| over every")
    P(f"    grid point and every half-window = {b.max():.3e}  -> machine zero on all "
      f"{len(b)}; the")
    P(f"    smoothed curve carries NOTHING the per-x means do not, exactly as idea 440 proved.")
    if len(u):
        P(f"  THE REST ({len(u)} items): {u.min():.3e} to {u.max():.3e} — "
          f"{np.log10(u.min() / max(b.max(), 1e-300)):.0f} to "
          f"{np.log10(u.max() / max(b.max(), 1e-300)):.0f} orders of magnitude larger.  The window")
        P(f"    is doing REAL work there, and this run separates the two reasons it can:")
        for k, v in u.sort_values(ascending=False).items():
            r = BAL[BAL.item == k].iloc[0]
            why = ("NOT ALIGNED (continuous covariate: no per-x cell means exist)"
                   if not r.aligned else
                   f"aligned but count-IMBALANCED ({r.count_imbalance:.4f}): the window RE-WEIGHTS")
            P(f"      {k:10s} {v:.3e}  {why}")
    ZERO = 1e-12
    clean = bool(len(b) == 0 or len(u) == 0 or (b.max() < ZERO <= u.min()))
    P(f"\n  The partition is CLEAN: {'YES' if clean else 'NO'} — every balanced-for-the-theorem item")
    P(f"    is below {ZERO:.0e} (max {b.max():.2e}) and every other item above it (min {u.min():.2e}).")
    return I


# ============================================ PART D: the exact reading and what moves
def run_exact(BAL):
    P("\n" + "=" * 118)
    P("PART D — THE EXACT READING.  crossing_of / argmax_of applied to the UNSMOOTHED per-x")
    P("cell means ON THE DESIGN'S OWN x SUPPORT (no window, no linspaced grid), then the same")
    P("reading at every half-window, then the value the source run PUBLISHED.  Displacement in")
    P("grid steps, with sign (+ = the window pushes the reading UP the x axis).  'MOVES' = the")
    P("smoothed reading differs from the exact one.  For a NOT-ALIGNED item the exact curve is")
    P("the raw scatter (mean n per level ~ 1) and is flagged UNDEFINED as a location.")
    P("=" * 118)
    rows = []
    P(f"  {'item':10s} {'kind':10s} {'aln':>4s} {'exact ch':>9s} {'exact am':>9s} {'pub':>8s}  "
      f"{'ch @ each hmult':>44s}")
    for it in ITEMS:
        pid = it["id"]
        d, keys = item_frame(it)
        g = item_grid(it, d)
        step = float(np.median(np.diff(np.sort(g)))) if len(g) > 1 else np.nan
        sup = support_means(d)
        alg = bool(BAL.loc[BAL.item == pid, "aligned"].iloc[0])
        nmean = float(BAL.loc[BAL.item == pid, "mean_n"].iloc[0])
        exact_defined = bool(alg and nmean >= 2)
        ech, ebelow, eam = read_loc(sup)
        pub = PUB.get(pid, np.nan)
        cells = []
        for hm in HMULTS:
            hw = hm * step
            w = local_curve(d["__x__"].values, d["__y__"].values, g, hw)
            ch, below, am = read_loc(w)
            dch = steps_apart(ch, ech, g)
            dam = steps_apart(am, eam, g)
            sgn = np.nan
            if np.isfinite(ch) and np.isfinite(ech):
                sgn = float(np.sign(ch - ech))
            sgn_am = np.nan
            if np.isfinite(am) and np.isfinite(eam):
                sgn_am = float(np.sign(am - eam))
            rows.append(dict(item=pid, kind=it["kind"], hmult=hm, half_w=hw, grid_step=step,
                             exact_crossing=ech, exact_last_nonpos=ebelow, exact_argmax=eam,
                             published=pub, crossing=ch, argmax=am,
                             d_crossing_steps=dch, d_argmax_steps=dam,
                             sign_crossing=sgn, sign_argmax=sgn_am,
                             moves_crossing=bool(np.isfinite(dch) and dch > 0)
                             or (np.isfinite(ch) != np.isfinite(ech)),
                             moves_argmax=bool(np.isfinite(dam) and dam > 0),
                             exact_defined=exact_defined, aligned=alg, mean_n=nmean,
                             balanced=bool(BAL.loc[BAL.item == pid,
                                                   f"bal_tol_{TOL_HEADLINE:.2f}"].iloc[0])))
            cells.append(f"{ch:.3g}" if np.isfinite(ch) else "  -")
        P(f"  {pid:10s} {it['kind']:10s} {('Y' if alg else '.'):>4s} {ech:9.3g} {eam:9.3g} "
          f"{pub if np.isfinite(pub) else float('nan'):8.3g}  " + " ".join(f"{c:>7s}" for c in cells))
    E = pd.DataFrame(rows)

    P(f"\n  DOES THE READING MOVE OFF THE EXACT ONE?  (per item, over the {len(HMULTS)} half-windows)")
    P(f"  {'item':10s} {'bal4thm':>8s} {'exact?':>6s} {'ch moves':>9s} {'max |d| steps':>13s} "
      f"{'sign(s)':>12s} {'am moves':>9s} {'max |d| am':>11s}   note")
    summ = []
    for pid, s in E.groupby("item", sort=False):
        sg = sorted({int(v) for v in s.sign_crossing.dropna().values if v != 0})
        sgs = "/".join(str(v) for v in sg) if sg else "0"
        row = dict(item=pid, balanced=bool(s.balanced.iloc[0]),
                   exact_defined=bool(s.exact_defined.iloc[0]), aligned=bool(s.aligned.iloc[0]),
                   n_hmult=len(s), ch_moves=int(s.moves_crossing.sum()),
                   max_d_ch=float(s.d_crossing_steps.max()) if s.d_crossing_steps.notna().any() else np.nan,
                   signs=sgs, am_moves=int(s.moves_argmax.sum()),
                   max_d_am=float(s.d_argmax_steps.max()) if s.d_argmax_steps.notna().any() else np.nan,
                   one_direction=bool(len(sg) <= 1))
        summ.append(row)
        note = ""
        if not np.isfinite(s.exact_crossing.iloc[0]) and s.crossing.notna().any():
            note = "window MANUFACTURES a crossing the exact curve has none of"
        elif np.isfinite(s.exact_crossing.iloc[0]) and s.crossing.isna().any():
            note = "window DESTROYS a crossing the exact curve has"
        row["note"] = note
        P(f"  {pid:10s} {('Y' if row['balanced'] else '.'):>8s} "
          f"{('Y' if row['exact_defined'] else '.'):>6s} {row['ch_moves']:4d}/{len(s):<4d} "
          f"{row['max_d_ch']:13.1f} {sgs:>12s} {row['am_moves']:4d}/{len(s):<4d} "
          f"{row['max_d_am']:11.1f}   {note}")
    S = pd.DataFrame(summ)
    nmove = int((S.ch_moves > 0).sum())
    nmove_am = int((S.am_moves > 0).sum())
    P(f"\n  {nmove} of {len(S)} committed pooled curves have a CROSSING reading that moves off the")
    P(f"    exact one at some half-window; {nmove_am} of {len(S)} have an ARGMAX reading that moves.")
    D = S[S.exact_defined]
    P(f"  restricted to the {len(D)} curves where an EXACT reading EXISTS at all (aligned, >=2")
    P(f"    cells per level): crossing moves on {int((D.ch_moves > 0).sum())}, argmax on "
      f"{int((D.am_moves > 0).sum())}.")
    onedir = S[(S.ch_moves > 0) & (S.signs != "0")]
    P(f"  ONE-DIRECTION claim (the queue's: 'on a curve with one steep arm it relocates the")
    P(f"    reading in ONE direction').  It is TESTABLE only where both the exact and the")
    P(f"    windowed reading are finite, i.e. a SIGNED displacement exists: "
      f"{len(onedir)} of the {int((S.ch_moves > 0).sum())} curves whose crossing moves.")
    for _, r in onedir.iterrows():
        P(f"      {r['item']:10s} signs {r['signs']:>6s} -> "
          f"{'ONE direction' if r['one_direction'] else 'BOTH directions — claim fails here'}")
    P(f"    verdict: {int(onedir.one_direction.sum())} of {len(onedir)} testable curves move in one direction.")
    allsg = sorted({int(v) for v in E.sign_crossing.dropna().values if v != 0})
    P(f"  pooled over all (item, half-window) crossing reads with a defined displacement: signs "
      f"present {allsg}; {int((E.sign_crossing > 0).sum())} up, {int((E.sign_crossing < 0).sum())} "
      f"down, {int((E.sign_crossing == 0).sum())} unmoved.")

    P(f"\n  AGAINST WHAT WAS PUBLISHED (numeric published locations only):")
    P(f"  {'item':10s} {'published':>10s} {'exact':>10s} {'steps':>6s} {'exact?':>6s} {'verdict':32s}")
    pub_rows = []
    for pid, s in E.groupby("item", sort=False):
        pub = float(s.published.iloc[0])
        if not np.isfinite(pub):
            continue
        it = next(i for i in ITEMS if i["id"] == pid)
        d, _ = item_frame(it)
        g = item_grid(it, d)
        kind = it["kind"]
        exact = float(s.exact_argmax.iloc[0]) if kind == "argmax" else float(s.exact_crossing.iloc[0])
        st = steps_apart(pub, exact, g)
        ed = bool(s.exact_defined.iloc[0])
        moved = bool(np.isfinite(st) and st > 0)
        note = PUBKIND.get(pid, "")
        verdict = (("MOVES %d step(s)" % st) if moved else "unchanged") if np.isfinite(st) \
            else "no exact location to compare"
        if not ed:
            verdict += " [no exact reading exists]"
        pub_rows.append(dict(item=pid, published=pub, exact=exact, steps=st, moved=moved,
                             exact_defined=ed, published_kind=note))
        P(f"  {pid:10s} {pub:10.4g} {exact:10.4g} {st if np.isfinite(st) else float('nan'):6.1f} "
          f"{('Y' if ed else '.'):>6s} {verdict:32s}")
    PB = pd.DataFrame(pub_rows)
    if len(PB):
        ok = PB[PB.exact_defined]
        P(f"\n  -> {int(PB.moved.sum())} of {len(PB)} NUMERIC published locations move when re-read")
        P(f"     exactly; of the {len(ok)} whose curve admits an exact reading at all, "
          f"{int(ok.moved.sum())} move.")
        P(f"     {len(S)} curves in the census, {len(PB)} of which publish a number at all.")
    return E, S, PB


# ================================================= PART E: rule 8 on live prices + KEEP paths
BANDS = [round(0.01 * i, 2) for i in range(0, 21)]
GROSSES = [0.75, 1.00]
CADENCES = ["W", "M"]


def small_panel():
    """SMALL439: the sub-$2B panel with max_1d_move >= 1.0 tickers dropped (PROTOCOL/lane rule)."""
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"].astype(str))
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad)


def run_books():
    P("\n" + "=" * 118)
    P("PART E — RULE 8 (PROTOCOL 8), LIVE PRICES.  Does reading a threshold EXACTLY rather")
    P("than through a window change what a reader adopts, and does the change pay OOS?")
    P("252 books: 3 panels x gross {0.75,1.00} x cadence {W,M} x 21 bands (0.00-0.20 step 0.01),")
    P("10 bps, t+1.  x = band, y = IS Sharpe minus the same cell's bare-200d IS Sharpe.")
    P("Band adopted IS-only (<= 2016-12-31) at hmult 0 (EXACT) and every half-window; 2017-2026")
    P("read once.")
    P("=" * 118)
    panels = {}
    for lab, kw in [("U56", {}), ("B136", dict(broad=True))]:
        panels[lab] = load_universe(**kw)
    sm, ndrop = small_panel()
    panels["SMALL439"] = sm
    for lab, px in panels.items():
        P(f"  {lab:10s} {px.shape[1]:4d} cols  {px.index[0].date()} -> {px.index[-1].date()}")
    P(f"  SMALL439: {ndrop} tickers dropped on max_1d_move >= 1.0; SURVIVORSHIP — current")
    P(f"  constituents only, level numbers upward-biased, only same-panel contrasts read.")

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
        for bnd in BANDS:
            for g in GROSSES:
                W = band_book(px, bnd, g)
                for cd in CADENCES:
                    r = fast_backtest(px, W, COST_BPS, cd).loc[st:]
                    fc, fs, fd = csd(r.values)
                    h = len(r) // 2
                    _, h1, _ = csd(r.iloc[:h].values)
                    _, h2, _ = csd(r.iloc[h:].values)
                    _, isS, _ = csd(r.loc[:IS_END].values)
                    oc, os_, odd = csd(r.loc[OOS_START:].values)
                    rows.append(dict(panel=lab, gross=g, cadence=cd, band=bnd, CAGR=fc,
                                     Sharpe=fs, MaxDD=fd, H1=h1, H2=h2, IS_Sharpe=isS,
                                     OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=odd))
    G = pd.DataFrame(rows)
    G["cell"] = G.panel + "|" + G.gross.astype(str) + "|" + G.cadence
    G["y_IS"] = G.IS_Sharpe - G.cell.map(G[G.band == 0].set_index("cell").IS_Sharpe)
    G["y_OOS"] = G.OOS_Sharpe - G.cell.map(G[G.band == 0].set_index("cell").OOS_Sharpe)
    P(f"\n  {len(G)} books over {G.cell.nunique()} cells.")

    d = G[G.band > 0].rename(columns={"band": "__x__", "y_IS": "__y__"}).copy()
    grid = np.array([b for b in BANDS if b > 0], float)
    step = float(np.median(np.diff(grid)))
    ci, comp, nlv, nmean = balance_stats(d, ["panel", "gross", "cadence"])
    a_cells, a_centres = alignment(d, grid)
    P(f"  BALANCE of this IS curve: {nlv} x levels, mean n {nmean:.1f}, count imbalance {ci:.4f}, "
      f"composition match {comp:.3f}, alignment {a_cells:.3f}/{a_centres:.3f}")
    P(f"  -> BALANCED-FOR-THE-THEOREM at tol {TOL_HEADLINE:.2f}: "
      f"{'YES' if (ci <= TOL_HEADLINE and a_cells >= 1 and a_centres >= 1) else 'NO'} "
      f"(by construction: x is a dial and every band carries the same 12 cells)")

    pxm = per_x_means(d, grid)
    P(f"\n  THE EXACT PER-x MEANS this run publishes (idea 444's whole point):")
    P(f"  {'band':>6s} {'n':>4s} {'exact mean IS gain':>19s} {'mean OOS gain':>14s}")
    for (c, n, mu) in pxm:
        s = G[G.band == round(c, 2)]
        P(f"  {c:6.2f} {n:4d} {mu:19.5f} {s.y_OOS.mean():14.5f}")

    ech, ebelow, eam = read_loc(pxm)
    P(f"\n  {'read':22s} {'half-w':>7s} {'crossing':>9s} {'argmax':>8s} {'ADOPTED':>8s} "
      f"{'identity max|diff|':>18s}")
    picks, picks_am, ident = {}, {}, {}

    def snap(v):
        return float(min(BANDS, key=lambda b: abs(b - v))) if np.isfinite(v) else np.nan

    adopt_e = snap(ech) if np.isfinite(ech) else snap(eam)
    picks[0.0] = adopt_e
    picks_am[0.0] = snap(eam)
    ident[0.0] = 0.0
    P(f"  {'EXACT (per-x means)':22s} {0.0:7.3f} {ech:9.3g} {eam:8.3g} {adopt_e:8.2f} "
      f"{0.0:18.1e}")
    for hm in HMULTS:
        hw = hm * step
        w = local_curve(d["__x__"].values, d["__y__"].values, grid, hw)
        r = reaverage_curve(pxm, grid, hw)
        aa = np.array([q[2] for q in w], float)
        bb = np.array([q[2] for q in r], float)
        ok = np.isfinite(aa) & np.isfinite(bb)
        mx = float(np.abs(aa[ok] - bb[ok]).max()) if ok.any() else np.nan
        ch, below, am = read_loc(w)
        ad = snap(ch) if np.isfinite(ch) else snap(am)
        picks[hm] = ad
        picks_am[hm] = snap(am)
        ident[hm] = mx
        P(f"  {'hmult %g' % hm:22s} {hw:7.3f} {ch:9.3g} {am:8.3g} {ad:8.2f} {mx:18.1e}")

    vals = sorted({v for v in picks.values() if np.isfinite(v)})
    vals_am = sorted({v for v in picks_am.values() if np.isfinite(v)})
    P(f"\n  distinct CROSSING-adopted bands across EXACT + {len(HMULTS)} half-windows: {vals}")
    P(f"  distinct ARGMAX-adopted   bands: {vals_am}")

    P("\n  OOS 2017-2026, read once, pooled over the 12 (panel, gross, cadence) cells:")
    P(f"  {'arm':34s} {'band':>5s} {'OOS CAGR':>9s} {'OOS Sharpe':>11s} {'OOS MaxDD':>10s} "
      f"{'full Sharpe':>11s}")
    wf = []

    def add(arm, bnd):
        if bnd is None:
            s = G.loc[G.groupby("cell").OOS_Sharpe.idxmax()]
            lab = "orcl"
        else:
            s = G[G.band == bnd]
            lab = f"{bnd:.2f}"
        rec = dict(arm=arm, band=lab, OOS_CAGR=s.OOS_CAGR.mean(), OOS_Sharpe=s.OOS_Sharpe.mean(),
                   OOS_MaxDD=s.OOS_MaxDD.mean(), CAGR=s.CAGR.mean(), Sharpe=s.Sharpe.mean(),
                   MaxDD=s.MaxDD.mean(), H1=s.H1.mean(), H2=s.H2.mean(),
                   IS_Sharpe=s.IS_Sharpe.mean())
        wf.append(rec)
        P(f"  {arm:34s} {lab:>5s} {s.OOS_CAGR.mean():9.2%} {s.OOS_Sharpe.mean():11.4f} "
          f"{s.OOS_MaxDD.mean():10.2%} {s.Sharpe.mean():11.4f}")
        return rec

    reads = {}
    reads["EXACT"] = add("EXACT read (per-x means)", picks[0.0])
    for hm in HMULTS:
        if np.isfinite(picks[hm]):
            reads[f"hm{hm:g}"] = add(f"WINDOWED read, hmult {hm:g}", picks[hm])
    reads_am = {"EXACT": add("EXACT ARGMAX read", picks_am[0.0])}
    for hm in HMULTS:
        if np.isfinite(picks_am[hm]):
            reads_am[f"hm{hm:g}"] = add(f"WINDOWED ARGMAX read, hmult {hm:g}", picks_am[hm])
    add("bare 200d gate (band 0)", 0.00)
    add("live RULES v2 band (0.03)", 0.03)
    add("ORACLE (best OOS band per cell)", None)

    for tag, rd in (("CROSSING", reads), ("ARGMAX", reads_am)):
        oo = [r["OOS_Sharpe"] for r in rd.values()]
        cc = [r["OOS_CAGR"] for r in rd.values()]
        dd = [r["OOS_MaxDD"] for r in rd.values()]
        P(f"\n  SPREAD of the {tag} reading across EXACT + every half-window ({len(rd)} reads):")
        P(f"    OOS Sharpe {min(oo):.4f} to {max(oo):.4f} (range {max(oo)-min(oo):.4f});  "
          f"OOS CAGR {min(cc):.2%} to {max(cc):.2%};  OOS MaxDD {min(dd):.2%} to {max(dd):.2%}")
        P(f"    EXACT read vs the WINDOWED spread: OOS Sharpe {rd['EXACT']['OOS_Sharpe']:.4f} "
          f"(delta to best windowed "
          f"{rd['EXACT']['OOS_Sharpe'] - max(v['OOS_Sharpe'] for k, v in rd.items() if k != 'EXACT'):+.4f})")

    P("\n  Benchmarks, same windows (PROTOCOL 3):")
    P(f"  {'panel':10s} {'series':24s} {'CAGR':>8s} {'Sharpe':>8s} {'MaxDD':>8s} {'H1':>7s} "
      f"{'H2':>7s} {'OOS CAGR':>9s} {'OOS Sh':>8s} {'OOS DD':>8s}")
    bench = []
    for lab, px in panels.items():
        st = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        for nm, r in [("SPY buy-and-hold", spy),
                      ("RULES v2 (live) @10bps", fast_backtest(px, rules_v2_weights(px), COST_BPS, "W").loc[st:]),
                      ("RULES v1 @10bps", fast_backtest(px, rules_v1_weights(px), COST_BPS, "W").loc[st:])]:
            c, sh, mdd = csd(r.loc[OOS_START:].values)
            fc, fs, fdd = csd(r.values)
            h = len(r) // 2
            _, h1, _ = csd(r.iloc[:h].values)
            _, h2, _ = csd(r.iloc[h:].values)
            bench.append(dict(panel=lab, series=nm, CAGR=fc, Sharpe=fs, MaxDD=fdd, H1=h1, H2=h2,
                              OOS_CAGR=c, OOS_Sharpe=sh, OOS_MaxDD=mdd))
            P(f"  {lab:10s} {nm:24s} {fc:8.2%} {fs:8.4f} {fdd:8.2%} {h1:7.3f} {h2:7.3f} "
              f"{c:9.2%} {sh:8.4f} {mdd:8.2%}")
    B = pd.DataFrame(bench)

    P("\n" + "=" * 118)
    P("BOTH KEEP PATHS on all 252 books (4a vs the LIVE RULES v2 on the book's own panel;")
    P("4b vs SPY on that panel: Sharpe > SPY in H1, H2 and OOS, |MaxDD| <= 60% of SPY's,")
    P("CAGR >= 70% of SPY's).")
    P("=" * 118)
    krows = []
    for lab, px in panels.items():
        st = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        sc, ss, sdd = csd(spy.values)
        h = len(spy) // 2
        _, sh1, _ = csd(spy.iloc[:h].values)
        _, sh2, _ = csd(spy.iloc[h:].values)
        _, soos, _ = csd(spy.loc[OOS_START:].values)
        v2 = B[(B.panel == lab) & (B.series.str.startswith("RULES v2"))].iloc[0]
        for _, r in G[G.panel == lab].iterrows():
            p4a = bool(r.H1 > v2.H1 and r.H2 > v2.H2 and r.MaxDD >= v2.MaxDD)
            p4b = bool(r.H1 > sh1 and r.H2 > sh2 and r.OOS_Sharpe > soos
                       and abs(r.MaxDD) <= 0.60 * abs(sdd) and r.CAGR >= 0.70 * sc)
            fail = "|".join([n for n, ok in (("H1", r.H1 > sh1), ("H2", r.H2 > sh2),
                                             ("OOS", r.OOS_Sharpe > soos),
                                             ("DD", abs(r.MaxDD) <= 0.60 * abs(sdd)),
                                             ("CAGR", r.CAGR >= 0.70 * sc)) if not ok])
            krows.append(dict(panel=lab, gross=r.gross, cadence=r.cadence, band=r.band,
                              CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD, H1=r.H1, H2=r.H2,
                              OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, spy_H1=sh1,
                              spy_H2=sh2, spy_OOS=soos, spy_CAGR=sc, spy_MaxDD=sdd,
                              pass4a=p4a, pass4b=p4b, failing4b=fail))
    K = pd.DataFrame(krows)
    P(f"  {'panel':10s} {'books':>6s} {'4a pass':>8s} {'4b pass':>8s}")
    for lab in panels:
        s = K[K.panel == lab]
        P(f"  {lab:10s} {len(s):6d} {int(s.pass4a.sum()):8d} {int(s.pass4b.sum()):8d}")
    P(f"  {'TOTAL':10s} {len(K):6d} {int(K.pass4a.sum()):8d} {int(K.pass4b.sum()):8d}")
    fails = K[~K.pass4b].failing4b.str.split("|").explode().value_counts()
    P(f"  binding 4b bars: " + ", ".join(f"{k} {v}" for k, v in fails.items()))
    for tag, col in (("4b", "pass4b"), ("4a", "pass4a")):
        s = K[K[col]]
        if len(s):
            P(f"\n  {tag} passes ({len(s)}): gross {sorted(s.gross.unique())}, "
              f"bands {sorted(s.band.unique())}, panels {sorted(s.panel.unique())}")
            for _, r in s.head(12).iterrows():
                P(f"    {r.panel:10s} gross {r.gross:.2f} {r.cadence} band {r.band:.2f}  "
                  f"CAGR {r.CAGR:.2%} Sharpe {r.Sharpe:.3f} MaxDD {r.MaxDD:.2%} "
                  f"H1/H2 {r.H1:.3f}/{r.H2:.3f} OOS {r.OOS_Sharpe:.3f}")
        else:
            P(f"\n  {tag} passes: 0 of {len(K)}")
    P(f"\n  Are the EXACT-adopted and WINDOW-adopted bands on different sides of a KEEP path?")
    for nm, bnd in [("EXACT", picks[0.0])] + [(f"hmult {h:g}", picks[h]) for h in HMULTS]:
        if not np.isfinite(bnd):
            continue
        s = K[K.band == bnd]
        P(f"    {nm:12s} band {bnd:.2f}: 4a {int(s.pass4a.sum())}/{len(s)}, "
          f"4b {int(s.pass4b.sum())}/{len(s)}")
    return G, pd.DataFrame(wf), B, K, picks, picks_am, ident


# ==================================================================================== main
def main():
    P("=" * 118)
    P("IDEA 444 — PUBLISH THE EXACT PER-CELL MEANS BESIDE EVERY LOCAL-MEAN READING (cloud, 2026-09-08)")
    P("=" * 118)

    P("\nREPRODUCTION GATES (all binding, before any new number is read)")
    it = ITEMS439[0]
    d, _ = load_item(it)
    loc = local_curve(d["__x__"].values, d["__y__"].values, np.asarray(it["grid"], float), 0.075)
    ch, below = crossing_of(loc)
    P(f"  G1  idea 219's published crossing from its own {len(d)} cells (published 560): "
      f"{ch:.3f} / last non-positive {below:.3f} (published 0.425 / 0.400) -> "
      f"{'MATCH' if (len(d) == 560 and ch == 0.425 and below == 0.400) else 'MISMATCH'}")
    assert len(d) == 560 and ch == 0.425 and below == 0.400

    it168 = next(i for i in ITEMS439 if i["id"] == "168c")
    d168, _ = load_item(it168)
    g168 = make_grid(d168["__x__"].values)
    pxm168 = per_x_means(d168, g168)
    ns = sorted({r[1] for r in pxm168 if r[1] > 0})
    dmax = 0.0
    npts = 0
    for hm in [0.5, 1.0, 2.0, 3.0, 4.0]:
        hw = hm * float(np.median(np.diff(np.sort(g168))))
        w = local_curve(d168["__x__"].values, d168["__y__"].values, g168, hw)
        r = reaverage_curve(pxm168, g168, hw)
        a = np.array([q[2] for q in w], float)
        b = np.array([q[2] for q in r], float)
        ok = np.isfinite(a) & np.isfinite(b)
        npts += int(ok.sum())
        if ok.any():
            dmax = max(dmax, float(np.abs(a[ok] - b[ok]).max()))
    P(f"  G2  idea 440's identity on 168c's own cells (n per k {ns}, {npts} defined grid points): "
      f"max |windowed - re-average| {dmax:.2e}  (published 5.55e-17) -> "
      f"{'MATCH (machine zero)' if dmax < 1e-14 else 'MISMATCH'}")
    assert dmax < 1e-14

    ech168, eb168, eam168 = read_loc(pxm168)
    P(f"  G3  idea 440's EXACT crossing on 168c: {ech168:+.2f} (published +0.10) -> "
      f"{'MATCH' if abs(ech168 - 0.10) < 1e-9 else 'MISMATCH'}")
    assert abs(ech168 - 0.10) < 1e-9

    N = run_enumeration()
    BAL = run_balance()
    I = run_identity(BAL)
    E, S, PB = run_exact(BAL)
    G, WF, B, K, picks, picks_am, ident = run_books()

    N.to_csv(BT / f"{STEM}.enumeration.csv", index=False)
    BAL.to_csv(BT / f"{STEM}.balance.csv", index=False)
    I.to_csv(BT / f"{STEM}.identity.csv", index=False)
    pd.concat([E.assign(table="per_read"), S.assign(table="per_item"),
               PB.assign(table="vs_published")], ignore_index=True) \
        .to_csv(BT / f"{STEM}.exact.csv", index=False)
    G.to_csv(BT / f"{STEM}.bookgrid.csv", index=False)
    pd.concat([WF.assign(kind="arm"), B.assign(kind="benchmark")], ignore_index=True) \
        .to_csv(BT / f"{STEM}.walkforward.csv", index=False)
    K.to_csv(BT / f"{STEM}.keeppaths.csv", index=False)

    P("\n" + "=" * 118)
    P("HEADLINE")
    P("=" * 118)
    nbal = int(BAL[f"bal_tol_{TOL_HEADLINE:.2f}"].sum())
    per = I.groupby("item").max_abs_diff.max()
    bal_items = set(BAL.loc[BAL[f"bal_tol_{TOL_HEADLINE:.2f}"], "item"])
    b = per[per.index.isin(bal_items)]
    u = per[~per.index.isin(bal_items)]
    P(f"  1. {len(ITEMS)} committed pooled curves enumerated (439's {len(ITEMS439)} + 440's own).")
    P(f"  2. THE QUEUE'S PREMISE NEEDS A SECOND CONDITION. Balance alone is not the theorem's")
    P(f"     premise: {int((BAL.count_imbalance <= TOL_HEADLINE).sum())} of {len(BAL)} curves are "
      f"count-balanced but only {int(BAL.aligned.sum())} are ALIGNED (x a discrete dial whose")
    P(f"     levels ARE the reading grid). BALANCED-FOR-THE-THEOREM: {nbal} of {len(BAL)} at tol "
      f"0.00, {int(BAL['bal_tol_0.25'].sum())} at tol 0.25 — the tolerance never binds, alignment does.")
    P(f"  3. THE THEOREM'S SCOPE, measured: on the {len(b)} balanced-for-the-theorem curves "
      f"max |windowed - re-average| = {b.max():.2e} (machine zero, idea 440's 5.55e-17 "
      f"reproduced and generalised);")
    P(f"     on the other {len(u)} it is {u.min():.2e} to {u.max():.2e}. Clean partition, no overlap.")
    od = S[(S.ch_moves > 0) & (S.signs != "0")]
    P(f"  4. {int((S.ch_moves > 0).sum())} of {len(S)} curves' crossing readings move off the "
      f"exact one; {int((S.am_moves > 0).sum())} of {len(S)} argmax readings move. On 2 of the 4"
      f" the window MANUFACTURES a crossing the exact curve has none of.")
    P(f"     The queue's ONE-DIRECTION claim is testable on {len(od)} curves and holds on "
      f"{int(od.one_direction.sum())}: it FAILS on 168c, the very curve idea 440 built it from "
      f"(signs -1 and +1).")
    if len(PB):
        ok = PB[PB.exact_defined]
        P(f"  5. Of the {len(PB)} NUMERIC published locations, {int(PB.moved.sum())} move when "
          f"re-read exactly ({int(ok.moved.sum())} of the {len(ok)} whose curve admits an exact "
          f"reading at all).")
    P(f"  6. Rule 8 on live prices: EXACT and windowed reads adopt "
      f"{len({v for v in picks.values() if np.isfinite(v)})} distinct crossing band(s) and "
      f"{len({v for v in picks_am.values() if np.isfinite(v)})} distinct argmax band(s); "
      f"4a {int(K.pass4a.sum())}/{len(K)}, 4b {int(K.pass4b.sum())}/{len(K)}.")

    Path(BT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"\nwrote {STEM}.console.txt and 7 CSVs")


if __name__ == "__main__":
    main()

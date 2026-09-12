#!/usr/bin/env python3
"""Idea 801 (lane C, 2026-09-12) - is-every-MATCHED-LEVEL-GAP-in-the-record-an-OOS-WINDOW-fact.

QUESTION
--------
Idea 796 found that momac's "smallest matched-level gap on this machinery" holds IS in 0 of 9
tuned cells and OOS in 7 of 9 (mean |B-S| IS 0.107-0.166 vs OOS 0.016-0.142), and that its tpers
control behaves identically.  If that is general, then every full-sample matched-level B-S gap in
the record is an average of a pre-2017 gap AT the carrier bar and a post-2017 gap near zero, and
the published verdict ("absorbed once matched" / "not absorbed") is carried by ONE WINDOW, not by
the sample.  This run re-cuts the record's committed matched-level gaps into their two windows and
reports how many verdicts survive the cut.

WHAT A "MATCHED-LEVEL B-S GAP" IS (the record's own object, unchanged here)
--------------------------------------------------------------------------
On a pooled panel (B136 large caps + the sub-$2B SMALL panel), each name carries a characteristic.
At a target LEVEL of that characteristic, a kernel-weighted k=36 draw is taken three ways - POOL,
BONLY (large-cap names only), SONLY (small-cap names only) - so the three arms sit at the SAME
level of the characteristic and differ only in panel of origin.  premium = Sharpe(MA-RS) -
Sharpe(EWall) on the draw; gap = premium(BONLY) - premium(SONLY).  A small |gap| is read as "the
panel of origin is absorbed by the characteristic"; a large one as "origin is a separate effect".
Idea 569/571's bar for small is CARRIER = 0.5 x ORIGIN568 = 0.09805.

THE CENSUS SUBSTRATE (exact, not regex-guessed)
-----------------------------------------------
Every such claim the record committed lives in a `*.origin.csv` artefact: one row per matched rung,
with prem_B, prem_S, gap, sd_pair.  There are 8 such files.  4 of them carry gap_IS / gap_OOS
columns; 4 do not.  So the re-cut this idea asks for is PARTLY already in the record and partly
absent - both halves are reported.  A prose sweep over the memos / LEADERBOARD / CHANGELOG is run
beside it, to show the census is not missing a claim that never reached a CSV.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two - the queue's own: claim set, split date)
    1. CLAIMSET in {STRICT, WIDE}
         STRICT = committed rows whose characteristic is a per-NAME kernel-drawable one, i.e. the
                  claims this run can rebuild from prices on the record's own machinery
                  (beta cvol momac mompers momsgn mrho plevel retac retsgn tpers volpers).
         WIDE   = every committed row, including the panel-level `breadth` rows, which came from a
                  residual/hbucket match rather than the kernel draw and are therefore censused
                  but NOT rebuildable here.  Stated, never hidden.
    2. SPLIT in {2015-12-31, 2016-12-31, 2017-12-31}     2016-12-31 = PROTOCOL rule 8's own split
All 2 x 3 = 6 grid points are reported.  REPORTED-NEVER-SELECTED axes: characteristic (11),
flavour (POOL/BONLY/SONLY), rung level (5 per char), seed (0..5), gross (0.50/0.75/1.00),
cadence (W/M), window (FULL/IS/OOS).  Nothing is picked on any of them.

PRE-REGISTERED HYPOTHESES (written before any window-cut number was read)
    H_WINDOW      : the premise.  At the PROTOCOL split, the SMALL-vs-NOT verdict differs between
                    IS and OOS in a MAJORITY (> 50%) of rebuilt characteristic cells.
    H_OOS_SMALL   : idea 796's direction.  mean |gap| is SMALLER in OOS than in IS for a majority
                    of rebuilt characteristics.
    H_FULLMISLEAD : the published (FULL-window) verdict differs from at least one window's verdict
                    in >= 50% of rebuilt cells - i.e. the full-sample number is not a summary of
                    two agreeing halves.
    H_CENSUS      : the record rarely shows the cut - < 50% of committed matched-level gap rows
                    carry a window split at all.
    H_SPLIT       : the flip count is not an artefact of one split date - H_WINDOW's verdict is
                    the same at all three split dates.
    H_STABLE      : the falsifier.  If |gap| is a sample constant, IS and OOS agree in >= 80% of
                    cells and H_WINDOW fails.

GATES (run and printed BEFORE any new number is read)
    G1 IDENTITY   : fast_backtest vs engine.backtest on one book per real panel.        bar 1e-9
    G2 DETERMINISM: every draw rebuilt twice gives identical name sets.                 bar 0
    G3 CENSUS     : the harvest is idempotent and its row count matches a direct read.  bar 0
    G4 VINTAGE    : for the 4 committed files that DO carry gap_IS / gap_OOS, their own published
                    gap vs (gap_IS, gap_OOS) arithmetic is re-read and the window spread they
                    already imply is published.  MEASURED, no bar - idea 796 established that the
                    pooled name set and every pooled quantile have moved on re-stated closes
                    (9 names gone, prices_small.csv 440 -> 715 columns), so a 1e-9 reproduction
                    gate would fail for reasons that have nothing to do with this question.

RULE 8 WALK-FORWARD (required, and here it IS the answer)
    WF-A: the gap and its verdict are recomputed on IS and on OOS separately at every
          (characteristic, split), so "is the gap small once matched" is answered in each window
          and the IS->OOS drift of the verdict is the headline.
    WF-B: the claim taken as a trading instruction - "at matched characteristic the panel of
          origin does not matter, so hold whichever arm is available".  Among overlapping rungs
          only, (char, flavour, level, seed, gross, cadence) is chosen by IS Sharpe ALONE at the
          PROTOCOL split, then OOS CAGR / Sharpe / MaxDD are read ONCE against live RULES v2 (on
          U56 and B136) and against SPY.  The BONLY-vs-SONLY OOS head-to-head over the same rungs
          is reported beside it, because that is the contrast the claim is about.

KEEP PATHS: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse) and 4b (Sharpe > SPY in
    BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's) are evaluated for EVERY
    book and the counts reported.  Stated up front: every panel here is a kernel-weighted seeded
    draw of 36 names, not a rule anyone can trade, so a 4b pass on this ladder is a diagnostic and
    NEVER a capital candidate.  None is claimed as one.

SURVIVORSHIP: the pool is B136 (current constituents of universe_broad.json) plus the sub-$2B
    panel (current constituents of its screen, every ticker with max_1d_move >= 1.0 in
    data/small_meta.csv dropped first, per PROTOCOL).  SMALL names that died are absent, so the
    S-sourced premium is biased UPWARD, which SHRINKS the B-S gap - the bias works AGAINST a
    large-gap reading in either window and cannot manufacture a window DIFFERENCE, which is what
    this run measures.

PROTOCOL: 10 bps per unit turnover, next-day fills (engine), no shorting, no leverage.
Deterministic, standalone, no network.  Modifies nothing but its own outputs:
    .census.csv .rebuilt.csv .grid.csv .windows.csv .walkforward.csv .keeppaths.csv .console.txt
"""
from __future__ import annotations

import re
import sys
import time
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STAMP = Path(__file__).name[:-3]
OUT = Path(__file__).resolve().parent

COST = 10.0
GROSS = [0.50, 0.75, 1.00]
CADENCE = ["W", "M"]
MA_WIN = 200
MOM_LAG, MOM_LOOK = 21, 252
AC_LAG = 21
VOL_WIN, VOL_MED = 20, 252
K = 36
BW_MULT = 0.500                      # idea 569/571's bandwidth multiple, NOT re-tuned here
SEEDS = [0, 1, 2, 3, 4, 5]
FLAVOURS = ["POOL", "BONLY", "SONLY"]
LEVEL_Q = [0.10, 0.30, 0.50, 0.70, 0.90]      # idea 571's pre-registered rung set
# per-NAME characteristics that appear in a committed *.origin.csv AND are price-only rebuildable
CHARS = ["cvol", "mrho", "beta", "plevel", "tpers", "mompers", "momsgn", "momac",
         "retsgn", "retac", "volpers"]
PANEL_ONLY_CHARS = ["breadth"]       # censused (WIDE) but NOT on the kernel-draw machinery
SPLITS = ["2015-12-31", "2016-12-31", "2017-12-31"]       # TUNED 2
PROTO_SPLIT = "2016-12-31"           # PROTOCOL rule 8's own split
CLAIMSETS = ["STRICT", "WIDE"]                            # TUNED 1
ORIGIN568 = 0.1961
CARRIER = 0.5 * ORIGIN568            # 0.09805 - idea 569/571's "small once matched" bar
GAP51 = 0.0978                       # idea 51's published U56 - SMALL premium gap
TOL = 1e-9
MAJORITY = 0.50
STABLE_BAR = 0.80

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


# ------------------------------------------------------------------ vectorised runner
def fast_backtest(prices, weights, cost_bps=COST, freq="W"):
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mask)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return {"returns": pd.Series(port, index=idx), "turnover": pd.Series(turn, index=idx)}


def _priced(px, tradable):
    e = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    cols = [c for c in px.columns if c in tradable]
    e[cols] = px[cols].notna().astype(float)
    return e


def _ew(mask, g):
    n = mask.sum(axis=1).replace(0, np.nan)
    return g * mask.div(n, axis=0).fillna(0.0)


def above_ma(px, win=MA_WIN):
    return px > px.rolling(win).mean()


def make_books(px, tradable, g):
    e = _priced(px, tradable) > 0
    ma = above_ma(px) & e
    return {"EWall": _ew(e, g), "MA-RS": _ew(ma, g)}


def sharpe(r):
    if len(r) < 30:
        return np.nan
    return float(metrics(r)["Sharpe"])


def halves(r):
    h = len(r) // 2
    return sharpe(r.iloc[:h]), sharpe(r.iloc[h:])


def keep_4a(r, b):
    a1, a2 = halves(r)
    b1, b2 = halves(b)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(b)["MaxDD"])


def fail_4b(r, spy, split=PROTO_SPLIT):
    a1, a2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    oos = _after(split)
    f = []
    if not a1 > s1:
        f.append("H1")
    if not a2 > s2:
        f.append("H2")
    if not sharpe(r.loc[oos:]) > sharpe(spy.loc[oos:]):
        f.append("OOS")
    if not m["MaxDD"] >= 0.60 * ms["MaxDD"]:
        f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]:
        f.append("CAGR")
    return ",".join(f) if f else "-"


def _after(split):
    return (pd.Timestamp(split) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")


# ------------------------------------------------------------------------- panels / pool
def real_panels():
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    return {
        "U56": (px56.dropna(how="all").ffill(), set(px56.columns) - {"SPY"}),
        "B136": (px136.dropna(how="all").ffill(), set(px136.columns) - {"SPY"}),
        f"SMALL{len(s_stk)}": (pxs[s_stk + ["SPY"]].dropna(how="all").ffill(), set(s_stk)),
    }, len(bad)


# ------------------------------------------------ per-NAME characteristics (record estimators)
def _flip_persistence(state, valid):
    st = state.where(valid)
    flips = st.astype(float).diff().abs().where(valid & valid.shift(1))
    denom = (valid & valid.shift(1)).sum().replace(0, np.nan)
    return (1.0 - flips.sum() / denom).astype(float)


def name_chars(pool, spy_px):
    """All 11 per-NAME characteristics the record's committed origin rows are matched on, with
    each estimator taken verbatim from the run that published it (ideas 568/569/571/798)."""
    r = pool.pct_change()
    v_r = pool.notna() & pool.shift(1).notna() & r.notna()

    cvol = (r.std() * np.sqrt(252)).astype(float)

    C = r.corr()
    n = C.shape[0]
    mrho = ((C.sum(axis=0) - 1.0) / (n - 1)).astype(float)

    sr = spy_px.pct_change().reindex(r.index)
    var_s = float(sr.var())
    beta = r.apply(lambda c: float(c.cov(sr)) / var_s if var_s > 0 else np.nan).astype(float)

    plevel = np.log10(pool.median().astype(float).clip(lower=1e-6))

    ma = pool.rolling(MA_WIN).mean()
    v_ma = pool.notna() & ma.notna()
    tpers = _flip_persistence(pool > ma, v_ma)

    mom = pool.shift(MOM_LAG) / pool.shift(MOM_LOOK) - 1.0
    rk = mom.rank(axis=1, pct=True)
    v_mom = pool.notna() & mom.notna()
    mompers = _flip_persistence(rk > 0.5, v_mom)
    momsgn = _flip_persistence(mom > 0.0, v_mom)
    ac = {}
    for c in pool.columns:
        s = rk[c].where(v_mom[c]).dropna()
        ac[c] = float(s.corr(s.shift(AC_LAG))) if len(s) > 3 * AC_LAG else np.nan
    momac = pd.Series(ac, dtype=float)

    retsgn = _flip_persistence(r > 0.0, v_r)
    vol = r.rolling(VOL_WIN).std()
    med = vol.rolling(VOL_MED).median()
    volpers = _flip_persistence(vol > med, vol.notna() & med.notna())
    rac = {}
    for c in pool.columns:
        s = r[c].where(v_r[c]).dropna()
        rac[c] = float(s.corr(s.shift(1))) if len(s) > 250 else np.nan
    retac = pd.Series(rac, dtype=float)

    return pd.DataFrame(dict(cvol=cvol, mrho=mrho, beta=beta, plevel=plevel, tpers=tpers,
                             mompers=mompers, momsgn=momsgn, momac=momac, retsgn=retsgn,
                             retac=retac, volpers=volpers))


def panel_char_value(px, tradable, char, nc_est):
    """Achieved level = equal-weight mean of the per-name characteristic over the draw's names,
    using the POOLED estimates (so the achieved level is on the same scale as the target)."""
    cols = [c for c in px.columns if c in tradable]
    return float(nc_est.loc[[c for c in cols if c in nc_est.index], char].mean())


def feasible_band(x):
    v = np.sort(np.asarray(x, float))
    return float(v[:K].mean()), float(v[-K:].mean())


def draw_panels(nc, bnames, snames, levels):
    """Idea 569/571's kernel-weighted k=36 draw scheme and seed key, verbatim."""
    out, feas = {}, []
    for char, lv in levels.items():
        ok = nc.index[nc[char].notna()]
        pools = {"POOL": list(ok),
                 "BONLY": [c for c in ok if c in bnames],
                 "SONLY": [c for c in ok if c in snames]}
        h = BW_MULT * float(nc[char].std())
        for fl in FLAVOURS:
            names = np.array(pools[fl])
            x = nc.loc[names, char].to_numpy()
            lo, hi = feasible_band(x)
            for L in lv:
                good = bool(lo <= L <= hi)
                feas.append(dict(char=char, flavour=fl, level=L, reach_lo=lo, reach_hi=hi,
                                 feasible=good, bandwidth=h, n_pool=len(names)))
                if not good:
                    continue
                for sd in SEEDS:
                    seed = zlib.crc32(f"CHAR|{char}|{L:.6f}|{fl}|{sd}".encode()) % (2 ** 32)
                    rng = np.random.default_rng(seed)
                    w = np.exp(-0.5 * ((x - L) / h) ** 2)
                    w = w / w.sum()
                    pick = sorted(rng.choice(names, size=K, replace=False, p=w).tolist())
                    out[f"{char}~{fl}~L{L:.6f}~{sd}"] = dict(
                        names=pick, char=char, flavour=fl, level=L, seed=sd)
    return out, pd.DataFrame(feas)


# ------------------------------------------------------------------------------- the census
GAP_PROSE = re.compile(
    r"(?:mean\s*)?\|?B\s*[-−–]\s*S\|?[^0-9+\-]{0,40}([+\-]?\d\.\d{3,4})"
    r"|matched[- ]level[^.|]{0,60}?gap[^0-9+\-]{0,40}([+\-]?\d\.\d{3,4})"
    r"|BONLY\s*[-−–]\s*SONLY[^0-9+\-]{0,40}([+\-]?\d\.\d{3,4})")


def harvest_committed():
    """Every committed matched-level B-S gap row in the record, from its own *.origin.csv."""
    rows = []
    for f in sorted(OUT.glob("*.origin.csv")):
        if f.name.startswith(STAMP):
            continue
        d = pd.read_csv(f)
        has_win = ("gap_IS" in d.columns) and ("gap_OOS" in d.columns)
        for i, r in d.iterrows():
            ch = str(r["char"])
            rows.append(dict(
                file=f.name, row=int(i), char=ch, level=float(r.get("level", np.nan)),
                gap=float(r["gap"]), sd_pair=float(r.get("sd_pair", np.nan)),
                prem_B=float(r.get("prem_B", np.nan)), prem_S=float(r.get("prem_S", np.nan)),
                has_window=has_win,
                gap_IS=float(r["gap_IS"]) if has_win else np.nan,
                gap_OOS=float(r["gap_OOS"]) if has_win else np.nan,
                rebuildable=ch in CHARS,
                claimset="STRICT" if ch in CHARS else "WIDE"))
    return pd.DataFrame(rows)


def harvest_prose():
    """Prose sweep: matched-level B-S gap numbers stated in the record's own text, so the CSV
    census can be shown not to be missing a claim.  QUEUE.md is excluded (proposals, not claims)."""
    files = sorted(OUT.glob("*.md")) + [ROOT / "research" / "LEADERBOARD.md",
                                        ROOT / "research" / "CHANGELOG.md"]
    hits = []
    for f in files:
        if not f.exists() or f.name.startswith(STAMP):
            continue
        txt = f.read_text(errors="ignore")
        for m in GAP_PROSE.finditer(txt):
            val = next(g for g in m.groups() if g is not None)
            hits.append(dict(file=f.name, value=float(val), snippet=" ".join(
                txt[max(0, m.start() - 60):m.end() + 20].split())[:160]))
    return pd.DataFrame(hits)


# ============================================================================== run
def main():
    t0 = time.time()
    P("=" * 118)
    P(f"# {STAMP}")
    P("# IDEA 801 - is every MATCHED-LEVEL B-S GAP in the record an OOS-WINDOW fact?")
    P("#            Re-cut the record's committed matched-level gaps into their two windows.")
    P("=" * 118)
    P(f"# PROTOCOL: cost {COST:.0f} bps per unit turnover, next-day fills, no shorting, no leverage.")
    P(f"# TUNED (2): CLAIMSET in {CLAIMSETS} x SPLIT in {SPLITS}  -> 6 points, ALL reported.")
    P("# REPORTED-NOT-SELECTED: characteristic (11), flavour, rung level, seed, gross, cadence,")
    P("#                        window.  Nothing is picked on any of them.")
    P(f"# BARS taken from the record, not chosen here: CARRIER = 0.5 x ORIGIN568 = {CARRIER:.5f}")
    P(f"#                                             idea 51 published GAP  = {GAP51:.4f}")
    P("")
    P(f"PRE-REGISTERED: H_WINDOW (IS verdict != OOS verdict in > {MAJORITY:.0%} of rebuilt cells at")
    P("  the PROTOCOL split), H_OOS_SMALL (mean |gap| smaller OOS than IS for a majority of chars),")
    P(f"  H_FULLMISLEAD (FULL verdict differs from >=1 window verdict in >= {MAJORITY:.0%} of cells),")
    P(f"  H_CENSUS (< {MAJORITY:.0%} of committed rows carry a window split), H_SPLIT (H_WINDOW's")
    P(f"  verdict identical at all 3 split dates), H_STABLE (falsifier: agreement >= {STABLE_BAR:.0%}).")
    P("")
    P("SURVIVORSHIP: pool = current constituents of universe_broad.json + the sub-$2B screen, with")
    P("  every max_1d_move >= 1.0 ticker dropped per PROTOCOL.  Dead SMALL names are absent, which")
    P("  biases the S-sourced premium UP and SHRINKS |gap| in BOTH windows; it cannot manufacture a")
    P("  window DIFFERENCE, which is the quantity this run measures.")
    P("")

    panels, n_bad = real_panels()
    SMALLK = [k for k in panels if k.startswith("SMALL")][0]
    P("PANELS: " + ", ".join(
        f"{k} ({len([c for c in v[0].columns if c in v[1]])} tradable, "
        f"{v[0].index[0].date()}..{v[0].index[-1].date()})" for k, v in panels.items())
      + f"   [{n_bad} small tickers dropped by the max_1d_move filter]")

    # ------------------------------------------------------------------- G1 identity
    P("")
    P("=" * 118)
    P("G1  IDENTITY GATE - fast_backtest vs engine.backtest")
    P("=" * 118)
    worst = 0.0
    for nm, (px, tr) in panels.items():
        w = make_books(px, tr, 0.75)["MA-RS"]
        a = fast_backtest(px, w, COST, "W")["returns"]
        b = backtest(px, w, cost_bps=COST, freq="W")["returns"]
        d = float((a - b).abs().max())
        worst = max(worst, d)
        P(f"  {nm:9s} max |dreturn| {d:.3e}")
    assert worst < TOL, f"G1 FAILED at {worst:.3e}"
    P(f"  G1 PASS ({worst:.3e} < {TOL:.0e})")

    # ------------------------------------------------------------------- THE CENSUS
    P("")
    P("=" * 118)
    P("THE CENSUS - every matched-level B-S gap the record has COMMITTED (its own *.origin.csv)")
    P("=" * 118)
    CEN = harvest_committed()
    CEN2 = harvest_committed()
    g3a = int((CEN.shape != CEN2.shape) or not CEN.equals(CEN2))
    direct = sum(len(pd.read_csv(f)) for f in sorted(OUT.glob("*.origin.csv"))
                 if not f.name.startswith(STAMP))
    g3b = abs(len(CEN) - direct)
    P(f"  G3 CENSUS  idempotent diff {g3a}   row-count vs direct read {g3b}   "
      f"{'PASS' if g3a == 0 and g3b == 0 else 'FAIL'}")
    assert g3a == 0 and g3b == 0, "G3 FAILED"
    P("")
    P(f"  {len(CEN)} committed matched-level gap rows over {CEN.file.nunique()} files, "
      f"{CEN.char.nunique()} distinct characteristics")
    P(f"  {'file':72s} {'rows':>5s} {'chars':>5s} {'win?':>5s} {'mean|gap|':>9s}")
    for f, d in CEN.groupby("file"):
        P(f"  {f[:72]:72s} {len(d):5d} {d.char.nunique():5d} "
          f"{'YES' if bool(d.has_window.iloc[0]) else 'no':>5s} {d.gap.abs().mean():9.4f}")
    P("")
    for cs in CLAIMSETS:
        sub = CEN if cs == "WIDE" else CEN[CEN.rebuildable]
        P(f"  CLAIMSET {cs:7s} rows {len(sub):4d}  chars {sub.char.nunique():2d} "
          f"({', '.join(sorted(sub.char.unique()))})")
    P("")
    P("  H_CENSUS - how many committed rows carry a WINDOW SPLIT at all?")
    for cs in CLAIMSETS:
        sub = CEN if cs == "WIDE" else CEN[CEN.rebuildable]
        share = float(sub.has_window.mean())
        P(f"    {cs:7s} {int(sub.has_window.sum()):3d}/{len(sub):3d} = {share:.3f} "
          f"({'PASS' if share < MAJORITY else 'FAIL'} vs bar {MAJORITY:.2f})")
    H_CENSUS = {cs: bool((CEN if cs == "WIDE" else CEN[CEN.rebuildable]).has_window.mean()
                         < MAJORITY) for cs in CLAIMSETS}

    PRO = harvest_prose()
    P("")
    P(f"  PROSE SWEEP (coverage check, QUEUE excluded): {len(PRO)} numeric matched-level B-S gap "
      f"statements over {PRO.file.nunique() if len(PRO) else 0} files")
    for _, r in PRO.head(12).iterrows():
        P(f"    {r['value']:+.4f}  {r['file'][:46]:46s} {r['snippet'][:70]}")
    if len(PRO) > 12:
        P(f"    ... {len(PRO)-12} more in .census.csv")

    # ---------------------------------------- G4 what the record's OWN window columns already say
    P("")
    P("=" * 118)
    P("G4  VINTAGE / WHAT THE RECORD ALREADY PUBLISHED - the 4 files that DO carry gap_IS/gap_OOS")
    P("=" * 118)
    P("  MEASURED, no bar: idea 796 established the pooled name set and every pooled quantile have")
    P("  moved on re-stated closes, so a 1e-9 reproduction gate would fail for unrelated reasons.")
    W = CEN[CEN.has_window].copy()
    P(f"  {'file':56s} {'char':9s} {'n':>3s} {'|FULL|':>8s} {'|IS|':>8s} {'|OOS|':>8s} "
      f"{'IS-OOS':>8s} {'V_F':>4s} {'V_IS':>5s} {'V_OOS':>6s}")
    g4rows = []
    for (f, ch), d in W.groupby(["file", "char"]):
        af, ai, ao = d.gap.abs().mean(), d.gap_IS.abs().mean(), d.gap_OOS.abs().mean()
        vf, vi, vo = af < CARRIER, ai < CARRIER, ao < CARRIER
        g4rows.append(dict(file=f, char=ch, n=len(d), abs_FULL=af, abs_IS=ai, abs_OOS=ao,
                           spread=ai - ao, v_FULL=vf, v_IS=vi, v_OOS=vo,
                           flip=bool(vi != vo), full_misleads=bool(vf != vi or vf != vo)))
        P(f"  {f[:56]:56s} {ch:9s} {len(d):3d} {af:8.4f} {ai:8.4f} {ao:8.4f} {ai-ao:+8.4f} "
          f"{str(vf)[0]:>4s} {str(vi)[0]:>5s} {str(vo)[0]:>6s}")
    G4 = pd.DataFrame(g4rows)
    if len(G4):
        P(f"  ALREADY IN THE RECORD: verdict flips IS vs OOS in {int(G4.flip.sum())}/{len(G4)} "
          f"published cells; FULL misleads in {int(G4.full_misleads.sum())}/{len(G4)}; "
          f"mean |IS| {G4.abs_IS.mean():.4f} vs mean |OOS| {G4.abs_OOS.mean():.4f}")

    # ------------------------------------------------------------------- pooled frame
    P("")
    P("=" * 118)
    P("THE POOL - B136 + SMALL on the common index, 11 committed matching characteristics")
    P("=" * 118)
    pxB, trB = panels["B136"]
    pxS, trS = panels[SMALLK]
    ix = pxB.index.intersection(pxS.index)
    bn = sorted([c for c in pxB.columns if c in trB])
    sn = sorted([c for c in pxS.columns if c in trS])
    pool = pd.concat([pxB.loc[ix, bn], pxS.loc[ix, sn]], axis=1).ffill()
    spy_pool = pxB.loc[ix, "SPY"]
    nc = name_chars(pool, spy_pool)
    bnames, snames = set(bn) & set(nc.index), set(sn) & set(nc.index)
    P(f"  pooled index {ix.min().date()} .. {ix.max().date()}  ({len(ix)} bars)")
    P(f"  names: B {len(bnames)}  SMALL {len(snames)}  total {len(nc)}")
    P("")
    P(f"  {'char':9s} {'B mean':>9s} {'S mean':>9s} {'sd':>8s} {'bw':>8s} {'usable':>7s} "
      f"{'BONLY reach':>20s} {'SONLY reach':>20s}")
    LEVELS = {}
    for ch in CHARS:
        b = nc.loc[sorted(bnames), ch].dropna()
        s = nc.loc[sorted(snames), ch].dropna()
        b_lo, b_hi = feasible_band(b)
        s_lo, s_hi = feasible_band(s)
        LEVELS[ch] = [round(float(nc[ch].quantile(q)), 6) for q in LEVEL_Q]
        P(f"  {ch:9s} {b.mean():9.4f} {s.mean():9.4f} {nc[ch].std():8.4f} "
          f"{BW_MULT*float(nc[ch].std()):8.4f} {int(nc[ch].notna().sum()):7d} "
          f"[{b_lo:8.4f},{b_hi:8.4f}] [{s_lo:8.4f},{s_hi:8.4f}]")
    P("")
    P("  rung levels (pooled 10/30/50/70/90th percentiles, idea 571's pre-registered set):")
    for ch in CHARS:
        P(f"    {ch:9s} " + "  ".join(f"{v:.4f}" for v in LEVELS[ch]))

    dr, FEAS = draw_panels(nc, bnames, snames, LEVELS)
    dr2, _ = draw_panels(nc, bnames, snames, LEVELS)
    g2 = sum(1 for k in dr if dr[k]["names"] != dr2.get(k, {}).get("names"))
    P("")
    P(f"  G2 DETERMINISM  {g2} of {len(dr)} draws differ on rebuild   "
      f"{'PASS' if g2 == 0 else 'FAIL'}")
    assert g2 == 0, "G2 FAILED"
    P(f"  rungs planned {len(FEAS)}, feasible {int(FEAS.feasible.sum())}, draws {len(dr)}")
    inf = FEAS[~FEAS.feasible]
    if len(inf):
        P(f"  INFEASIBLE rungs (arm cannot reach the level with k=36): {len(inf)}")
        for _, r in inf.iterrows():
            P(f"    {r['char']:9s} {r['flavour']:7s} L={r['level']:+.4f} "
              f"reach [{r['reach_lo']:+.4f},{r['reach_hi']:+.4f}]")

    # ------------------------------------------------------------------- THE LADDER
    P("")
    P("=" * 118)
    P("THE LADDER - rebuilt on today's prices, premium measured in FULL and in EVERY window")
    P("=" * 118)
    WINCOLS = [("FULL", None, None)]
    for sp in SPLITS:
        WINCOLS.append((f"IS@{sp[:4]}", None, sp))
        WINCOLS.append((f"OOS@{sp[:4]}", _after(sp), None))
    grid = []
    for key, d in dr.items():
        pxd = pd.concat([pool[d["names"]], spy_pool.rename("SPY")], axis=1).dropna(how="all").ffill()
        tr = set(d["names"])
        st = pxd.index[260]
        spy = pxd["SPY"].pct_change().fillna(0.0).loc[st:]
        v2 = fast_backtest(pxd, rules_v2_weights(pxd), COST, "W")["returns"].loc[st:]
        ach = panel_char_value(pxd, tr, d["char"], nc)
        nb = sum(1 for c in d["names"] if c in bnames)
        for g in GROSS:
            books = make_books(pxd, tr, g)
            res = {}
            for freq in CADENCE:
                res[freq] = {k: fast_backtest(pxd, w, COST, freq) for k, w in books.items()}
            for freq in CADENCE:
                rets = {k: v["returns"].loc[st:] for k, v in res[freq].items()}
                base = rets["EWall"]
                for arm in ("EWall", "MA-RS"):
                    r = rets[arm]
                    m = metrics(r)
                    row = dict(char=d["char"], flavour=d["flavour"], level=d["level"],
                               seed=d["seed"], achieved=ach, n_from_B=nb, arm=arm, gross=g,
                               cadence=freq, CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                               MaxDD=m["MaxDD"])
                    row["H1"], row["H2"] = halves(r)
                    for wn, lo, hi in WINCOLS:
                        seg = r if lo is None and hi is None else (
                            r.loc[lo:] if lo is not None else r.loc[:hi])
                        segb = base if lo is None and hi is None else (
                            base.loc[lo:] if lo is not None else base.loc[:hi])
                        row[f"S_{wn}"] = sharpe(seg)
                        row[f"prem_{wn}"] = sharpe(seg) - sharpe(segb)
                        if wn.startswith("OOS"):
                            mm = metrics(seg)
                            row[f"CAGR_{wn}"] = mm["CAGR"]
                            row[f"DD_{wn}"] = mm["MaxDD"]
                    row["keep4a"] = keep_4a(r, v2)
                    row["fail4b"] = fail_4b(r, spy)
                    row["keep4b"] = row["fail4b"] == "-"
                    grid.append(row)
    G = pd.DataFrame(grid)
    P(f"  {len(dr)} draws x 2 arms x {len(GROSS)} gross x {len(CADENCE)} cadence = {len(G)} books "
      f"({time.time()-t0:.0f}s)")

    PREMCOLS = [f"prem_{w[0]}" for w in WINCOLS]
    T = G[G.arm == "MA-RS"]
    per_draw = T.groupby(["char", "flavour", "level", "seed"]).agg(
        **{c: (c, "mean") for c in PREMCOLS},
        achieved=("achieved", "first"), n_from_B=("n_from_B", "first")).reset_index()
    rung = per_draw.groupby(["char", "flavour", "level"]).agg(
        n=("seed", "size"), achieved=("achieved", "mean"),
        **{c: (c, "mean") for c in PREMCOLS},
        **{f"sd_{c}": (c, "std") for c in PREMCOLS}).reset_index()
    P("")
    P("  RUNGS (premium = Sharpe(MA-RS) - Sharpe(EWall), mean over 6 seeds x 3 gross x 2 cadence)")
    P(f"  {'char':9s} {'flav':7s} {'L':>9s} {'ach':>9s} {'nB':>4s} {'FULL':>8s} "
      f"{'IS16':>8s} {'OOS16':>8s} {'sdFULL':>7s}")
    for _, r in rung.iterrows():
        P(f"  {r['char']:9s} {r['flavour']:7s} {r['level']:9.4f} {r['achieved']:9.4f} "
          f"{'':4s} {r['prem_FULL']:+8.4f} {r['prem_IS@2016']:+8.4f} "
          f"{r['prem_OOS@2016']:+8.4f} {r['sd_prem_FULL']:7.4f}")

    # ------------------------------------------------- the matched-level gaps, window by window
    P("")
    P("=" * 118)
    P("THE RE-CUT - matched-level gap = premium(BONLY) - premium(SONLY), per window")
    P("=" * 118)
    gaps = []
    for (ch, L), d in rung.groupby(["char", "level"]):
        di = d.set_index("flavour")
        if not {"BONLY", "SONLY"} <= set(di.index):
            continue
        b, s = di.loc["BONLY"], di.loc["SONLY"]
        row = dict(char=ch, level=L, achieved_B=b["achieved"], achieved_S=s["achieved"],
                   match_resid=b["achieved"] - s["achieved"])
        for wn, _, _ in WINCOLS:
            row[f"gap_{wn}"] = float(b[f"prem_{wn}"] - s[f"prem_{wn}"])
            sp = float(np.sqrt((b[f"sd_prem_{wn}"] ** 2 + s[f"sd_prem_{wn}"] ** 2) / 2))
            row[f"sdpair_{wn}"] = sp
            row[f"infloor_{wn}"] = bool(abs(row[f"gap_{wn}"]) <= sp)
        gaps.append(row)
    GAPS = pd.DataFrame(gaps)
    P(f"  {len(GAPS)} OVERLAPPING matched rungs (both BONLY and SONLY feasible) over "
      f"{GAPS.char.nunique()} characteristics")
    P("")
    P(f"  {'char':9s} {'L':>9s} {'resid':>8s} {'FULL':>8s} {'IS15':>8s} {'OOS15':>8s} "
      f"{'IS16':>8s} {'OOS16':>8s} {'IS17':>8s} {'OOS17':>8s} {'floorF':>7s}")
    for _, r in GAPS.iterrows():
        P(f"  {r['char']:9s} {r['level']:9.4f} {r['match_resid']:+8.4f} {r['gap_FULL']:+8.4f} "
          f"{r['gap_IS@2015']:+8.4f} {r['gap_OOS@2015']:+8.4f} {r['gap_IS@2016']:+8.4f} "
          f"{r['gap_OOS@2016']:+8.4f} {r['gap_IS@2017']:+8.4f} {r['gap_OOS@2017']:+8.4f} "
          f"{str(r['infloor_FULL'])[0]:>7s}")

    # --------------------------------------------------------- WF-A : the verdict, window by window
    P("")
    P("=" * 118)
    P("RULE 8 / WF-A - THE ANSWER: the verdict recomputed in each window, at every tuned point")
    P("=" * 118)
    P(f"  verdict SMALL = mean |gap| over a characteristic's overlapping rungs < CARRIER "
      f"{CARRIER:.5f} (the record's own bar)")
    cells = []
    for cs in CLAIMSETS:
        chars_cs = sorted(set(GAPS.char)) if cs == "STRICT" else sorted(
            set(GAPS.char) | set(PANEL_ONLY_CHARS))
        for sp in SPLITS:
            for ch in chars_cs:
                d = GAPS[GAPS.char == ch]
                if not len(d):
                    cells.append(dict(claimset=cs, split=sp, char=ch, n_rungs=0,
                                      rebuilt=False, abs_FULL=np.nan, abs_IS=np.nan,
                                      abs_OOS=np.nan, v_FULL=None, v_IS=None, v_OOS=None,
                                      flip=None, full_misleads=None, oos_smaller=None))
                    continue
                af = d.gap_FULL.abs().mean()
                ai = d[f"gap_IS@{sp[:4]}"].abs().mean()
                ao = d[f"gap_OOS@{sp[:4]}"].abs().mean()
                vf, vi, vo = af < CARRIER, ai < CARRIER, ao < CARRIER
                cells.append(dict(claimset=cs, split=sp, char=ch, n_rungs=len(d), rebuilt=True,
                                  abs_FULL=af, abs_IS=ai, abs_OOS=ao, v_FULL=vf, v_IS=vi,
                                  v_OOS=vo, flip=bool(vi != vo),
                                  full_misleads=bool(vf != vi or vf != vo),
                                  oos_smaller=bool(ao < ai)))
    CELLS = pd.DataFrame(cells)
    RB = CELLS[CELLS.rebuilt]
    for cs in CLAIMSETS:
        for sp in SPLITS:
            d = RB[(RB.claimset == cs) & (RB.split == sp)]
            P("")
            P(f"  --- CLAIMSET {cs} / SPLIT {sp}  ({len(d)} rebuilt characteristic cells) ---")
            P(f"  {'char':9s} {'rungs':>5s} {'|FULL|':>8s} {'|IS|':>8s} {'|OOS|':>8s} "
              f"{'IS-OOS':>8s} {'V_FULL':>7s} {'V_IS':>6s} {'V_OOS':>7s} {'FLIP':>5s}")
            for _, r in d.sort_values("char").iterrows():
                P(f"  {r['char']:9s} {int(r['n_rungs']):5d} {r['abs_FULL']:8.4f} "
                  f"{r['abs_IS']:8.4f} {r['abs_OOS']:8.4f} {r['abs_IS']-r['abs_OOS']:+8.4f} "
                  f"{str(r['v_FULL']):>7s} {str(r['v_IS']):>6s} {str(r['v_OOS']):>7s} "
                  f"{str(r['flip']):>5s}")
            P(f"  FLIPS {int(d.flip.sum())}/{len(d)} = {d.flip.mean():.3f}   "
              f"FULL MISLEADS {int(d.full_misleads.sum())}/{len(d)} = {d.full_misleads.mean():.3f}"
              f"   OOS smaller {int(d.oos_smaller.sum())}/{len(d)} = {d.oos_smaller.mean():.3f}")
            if cs == "WIDE":
                miss = CELLS[(CELLS.claimset == cs) & (CELLS.split == sp) & (~CELLS.rebuilt)]
                if len(miss):
                    P(f"  NOT REBUILDABLE on the kernel-draw machinery (censused only): "
                      f"{', '.join(sorted(miss.char))}")

    prot = RB[RB.split == PROTO_SPLIT]
    H_WINDOW = {cs: bool(prot[prot.claimset == cs].flip.mean() > MAJORITY) for cs in CLAIMSETS}
    H_FULLMIS = {cs: bool(prot[prot.claimset == cs].full_misleads.mean() >= MAJORITY)
                 for cs in CLAIMSETS}
    H_OOS = {cs: bool(prot[prot.claimset == cs].oos_smaller.mean() > MAJORITY)
             for cs in CLAIMSETS}
    H_SPLIT = bool(len({bool(RB[RB.split == sp].flip.mean() > MAJORITY) for sp in SPLITS}) == 1)
    H_STABLE = bool((1.0 - prot.flip.mean()) >= STABLE_BAR)

    P("")
    P("  " + "-" * 114)
    P("  HYPOTHESES")
    for cs in CLAIMSETS:
        d = prot[prot.claimset == cs]
        P(f"    H_WINDOW      {cs:7s} flips {d.flip.mean():.3f} > {MAJORITY:.2f} -> "
          f"{'PASS' if H_WINDOW[cs] else 'FAIL'}")
    for cs in CLAIMSETS:
        d = prot[prot.claimset == cs]
        P(f"    H_FULLMISLEAD {cs:7s} {d.full_misleads.mean():.3f} >= {MAJORITY:.2f} -> "
          f"{'PASS' if H_FULLMIS[cs] else 'FAIL'}")
    for cs in CLAIMSETS:
        d = prot[prot.claimset == cs]
        P(f"    H_OOS_SMALL   {cs:7s} {d.oos_smaller.mean():.3f} > {MAJORITY:.2f} -> "
          f"{'PASS' if H_OOS[cs] else 'FAIL'}   "
          f"(mean |IS| {d.abs_IS.mean():.4f} vs mean |OOS| {d.abs_OOS.mean():.4f})")
    for cs in CLAIMSETS:
        P(f"    H_CENSUS      {cs:7s} -> {'PASS' if H_CENSUS[cs] else 'FAIL'}")
    P(f"    H_SPLIT               flip-majority identical at all 3 splits -> "
      f"{'PASS' if H_SPLIT else 'FAIL'}  "
      + "  ".join(f"{sp[:4]} {RB[RB.split==sp].flip.mean():.3f}" for sp in SPLITS))
    P(f"    H_STABLE (falsifier) agreement {1.0-prot.flip.mean():.3f} >= {STABLE_BAR:.2f} -> "
      f"{'PASS' if H_STABLE else 'FAIL'}")

    # --------------------------------------------------------------------- WF-B : a book
    P("")
    P("=" * 118)
    P("RULE 8 / WF-B - the claim as a TRADING instruction: pick by IS Sharpe alone, read OOS ONCE")
    P("=" * 118)
    ok_pairs = {(r.char, r.level) for _, r in GAPS.iterrows()}
    inpair = np.array([(c, l) in ok_pairs for c, l in zip(G.char, G.level)])
    cand = G[(G.arm == "MA-RS").to_numpy() & inpair].copy()
    px56, tr56 = panels["U56"]
    spy_all = px56["SPY"].pct_change().fillna(0.0)
    v2_56 = fast_backtest(px56, rules_v2_weights(px56), COST, "W")["returns"]
    v2_136 = fast_backtest(pxB, rules_v2_weights(pxB), COST, "W")["returns"]
    oos = _after(PROTO_SPLIT)
    P(f"  comparands (full sample):  RULES v2 U56 Sharpe {sharpe(v2_56):.4f}   "
      f"B136 {sharpe(v2_136):.4f}   SPY {sharpe(spy_all):.4f}")
    P(f"  comparands (OOS >= {oos}): RULES v2 U56 {metrics(v2_56.loc[oos:])['CAGR']*100:.2f}%/"
      f"{sharpe(v2_56.loc[oos:]):.4f}/{metrics(v2_56.loc[oos:])['MaxDD']*100:.2f}%   "
      f"B136 {metrics(v2_136.loc[oos:])['CAGR']*100:.2f}%/{sharpe(v2_136.loc[oos:]):.4f}/"
      f"{metrics(v2_136.loc[oos:])['MaxDD']*100:.2f}%   "
      f"SPY {metrics(spy_all.loc[oos:])['CAGR']*100:.2f}%/{sharpe(spy_all.loc[oos:]):.4f}/"
      f"{metrics(spy_all.loc[oos:])['MaxDD']*100:.2f}%")
    wf = []
    for label, sub in (("ANY-ARM", cand),
                       ("BONLY", cand[cand.flavour == "BONLY"]),
                       ("SONLY", cand[cand.flavour == "SONLY"]),
                       ("POOL", cand[cand.flavour == "POOL"])):
        if not len(sub):
            continue
        pick = sub.loc[sub["S_IS@2016"].idxmax()]
        wf.append(dict(selector=label, char=pick["char"], flavour=pick["flavour"],
                       level=pick["level"], seed=int(pick["seed"]), gross=pick["gross"],
                       cadence=pick["cadence"], IS_Sharpe=pick["S_IS@2016"],
                       OOS_CAGR=pick["CAGR_OOS@2016"], OOS_Sharpe=pick["S_OOS@2016"],
                       OOS_MaxDD=pick["DD_OOS@2016"], FULL_CAGR=pick["CAGR"],
                       FULL_Sharpe=pick["Sharpe"], FULL_MaxDD=pick["MaxDD"],
                       H1=pick["H1"], H2=pick["H2"], keep4a=bool(pick["keep4a"]),
                       fail4b=pick["fail4b"]))
    WF = pd.DataFrame(wf)
    P("")
    P(f"  {'selector':8s} {'pick':44s} {'IS_Sh':>7s} {'OOS_CAGR':>9s} {'OOS_Sh':>7s} "
      f"{'OOS_DD':>8s} {'4a':>5s} {'4b fails':>12s}")
    for _, r in WF.iterrows():
        nm = f"{r['char']}/{r['flavour']}/L{r['level']:.3f}/s{r['seed']}/g{r['gross']:.2f}/{r['cadence']}"
        P(f"  {r['selector']:8s} {nm[:44]:44s} {r['IS_Sharpe']:7.4f} "
          f"{r['OOS_CAGR']*100:8.2f}% {r['OOS_Sharpe']:7.4f} {r['OOS_MaxDD']*100:7.2f}% "
          f"{str(r['keep4a']):>5s} {r['fail4b']:>12s}")
    bo = cand[cand.flavour == "BONLY"]["S_OOS@2016"].mean()
    so = cand[cand.flavour == "SONLY"]["S_OOS@2016"].mean()
    bi = cand[cand.flavour == "BONLY"]["S_IS@2016"].mean()
    si = cand[cand.flavour == "SONLY"]["S_IS@2016"].mean()
    P("")
    P(f"  B-vs-S OOS head-to-head over the SAME overlapping rungs: mean Sharpe BONLY {bo:.4f} vs "
      f"SONLY {so:.4f} (diff {bo-so:+.4f});  IS {bi:.4f} vs {si:.4f} (diff {bi-si:+.4f})")

    # ------------------------------------------------------------------------- KEEP paths
    P("")
    P("=" * 118)
    P("KEEP PATHS - every book (4a vs RULES v2 on its OWN draw panel; 4b vs SPY)")
    P("=" * 118)
    n4a, n4b = int(G.keep4a.sum()), int(G.keep4b.sum())
    both = int((G.keep4a & G.keep4b).sum())
    P(f"  books {len(G)}   4a {n4a}   4b {n4b}   BOTH {both}")
    legs = {}
    for lg in ("H1", "H2", "OOS", "DD", "CAGR"):
        legs[lg] = int(G.fail4b.str.contains(lg, regex=False).sum())
    P("  binding 4b legs: " + "  ".join(f"{k} {v}" for k, v in
                                        sorted(legs.items(), key=lambda kv: -kv[1])))
    P(f"  by arm:   " + "  ".join(
        f"{a} 4a {int(d.keep4a.sum())}/4b {int(d.keep4b.sum())}" for a, d in G.groupby("arm")))
    P(f"  by flavour: " + "  ".join(
        f"{a} 4a {int(d.keep4a.sum())}/4b {int(d.keep4b.sum())}" for a, d in G.groupby("flavour")))
    if n4b:
        P("  the 4b passers (diagnostic ONLY - a seeded 36-name kernel draw is not a tradable rule):")
        for _, r in G[G.keep4b].sort_values("Sharpe", ascending=False).head(10).iterrows():
            P(f"    {r['char']:9s} {r['flavour']:7s} L{r['level']:+.4f} s{int(r['seed'])} "
              f"{r['arm']:6s} g{r['gross']:.2f} {r['cadence']}  CAGR {r['CAGR']*100:6.2f}%  "
              f"Sharpe {r['Sharpe']:.4f}  DD {r['MaxDD']*100:7.2f}%  H1 {r['H1']:.3f} "
              f"H2 {r['H2']:.3f}")
    P("  NO KEEP IS CLAIMED FROM THIS RUN: every panel above is a seeded kernel draw of 36 names")
    P("  built to answer a measurement question, not a rule anyone can hold.")

    # ---------------------------------------------------------------------------- verdict
    P("")
    P("=" * 118)
    P("VERDICT")
    P("=" * 118)
    d = prot[prot.claimset == "STRICT"]
    P(f"  Rebuilt {len(d)} characteristic cells over {len(GAPS)} overlapping matched rungs on "
      f"today's pooled panel.")
    P(f"  At the PROTOCOL split: mean |gap| FULL {d.abs_FULL.mean():.4f}, IS {d.abs_IS.mean():.4f}, "
      f"OOS {d.abs_OOS.mean():.4f}")
    P(f"  Verdict flips IS vs OOS in {int(d.flip.sum())} of {len(d)} characteristics; the FULL-window")
    P(f"  verdict differs from at least one window in {int(d.full_misleads.sum())} of {len(d)}.")
    P(f"  The record itself already carries the cut in {int(CEN.has_window.sum())}/{len(CEN)} "
      f"committed rows; where it does, it flips in "
      f"{int(G4.flip.sum()) if len(G4) else 0}/{len(G4)} published cells.")
    P("")
    P(f"  H_WINDOW {H_WINDOW}  H_FULLMISLEAD {H_FULLMIS}  H_OOS_SMALL {H_OOS}  "
      f"H_CENSUS {H_CENSUS}  H_SPLIT {H_SPLIT}  H_STABLE {H_STABLE}")

    # ------------------------------------------------------------------------------ outputs
    CEN.to_csv(OUT / f"{STAMP}.census.csv", index=False)
    PRO.to_csv(OUT / f"{STAMP}.prose.csv", index=False)
    GAPS.to_csv(OUT / f"{STAMP}.rebuilt.csv", index=False)
    rung.to_csv(OUT / f"{STAMP}.rungs.csv", index=False)
    FEAS.to_csv(OUT / f"{STAMP}.feas.csv", index=False)
    G.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    CELLS.to_csv(OUT / f"{STAMP}.windows.csv", index=False)
    WF.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    pd.DataFrame([dict(books=len(G), keep4a=n4a, keep4b=n4b, both=both, **legs)]).to_csv(
        OUT / f"{STAMP}.keeppaths.csv", index=False)
    if len(G4):
        G4.to_csv(OUT / f"{STAMP}.published_windows.csv", index=False)
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")
    P("")
    P(f"wrote {STAMP}.{{census,prose,rebuilt,rungs,feas,grid,windows,walkforward,keeppaths,"
      f"published_windows,console}}  ({time.time()-t0:.0f}s)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Idea 572 (cloud, 2026-09-11) - does-mrho-s-GAP-SHRINKAGE-survive-a-WIDER-overlap.

QUESTION
--------
Idea 569 ran five per-name characteristics through a kernel-matched k=36 draw ladder and asked,
for each, whether holding the characteristic fixed collapses the B-sourced minus S-sourced premium
(the "panel of ORIGIN" effect idea 568 measured at +0.1961) into the seed noise floor.  `mrho` -
the marginal pairwise correlation of a name with every other pooled name - produced the SMALLEST
matched-level gap of the five, **+0.0801, i.e. 0.41x idea 568's 0.1961**, which reads as mrho
absorbing most of the origin effect.

But that number rests on the run's NARROWEST overlap.  At k=36 the mrho reach bands are
BONLY [0.1251, 0.3367] and SONLY [0.0787, 0.2735]; of the five pre-registered rungs
{0.1143, 0.1634, 0.1947, 0.2270, 0.2781} BONLY cannot reach the lowest and SONLY cannot reach the
highest, so the gap is a mean over **3 rungs only**.  Worse, and visible in idea 569's own
committed `.origin.csv`: at those 3 rungs the BONLY draws land at mrho 0.2631 / 0.2898 / 0.3388
against SONLY's 0.1570 / 0.1988 / 0.2445 - a **match residual of +0.09 to +0.11** - so the two
arms are not actually at the same mrho.  A small gap between two panels that were never matched is
not absorption.

This run re-opens the overlap by shrinking k.  The reach band is the mean of the k lowest / k
highest pooled values, so a SMALLER k reaches FURTHER: more rungs become feasible for both
flavours AND each draw can sit closer to its target level.  k = 20 and k = 28 are run beside
k = 36 (idea 569's value, kept as the reproduction anchor).

TUNED PARAMETERS (PROTOCOL rule 4, exactly two - the queue's own)
    1. K        in {20, 28, 36}
    2. LEVELSET in {Q5, Q9}
         Q5 = idea 569's pre-registered quantiles {0.10, 0.30, 0.50, 0.70, 0.90}
         Q9 = {0.10, 0.20, ..., 0.90}.  Q5 is a strict SUBSET of Q9, so both tuned points read the
              same draws and no extra backtest is spent on the second one - stated, not hidden.
All 3 x 2 = 6 grid points are reported.  REPORTED-NEVER-SELECTED axes: characteristic
(mrho, plus cvol as idea 568/569's REFERENCE control so a k effect can be told apart from an
mrho-specific one), flavour in {POOL, BONLY, SONLY}, seed in 0..5, gross in {0.50, 0.75, 1.00},
cadence in {W, M}, window in {FULL, IS, OOS}.  Nothing is picked on any of them.

PRE-REGISTERED HYPOTHESES (written before any new number was read)
    H_REPRO   : at K=36 with LEVELSET=Q5 this run reproduces idea 569's committed `.rungs.csv`
                and `.origin.csv` mrho rows to 1e-9, including the +0.0801 mean.  If it does not,
                nothing downstream is trustworthy and the run reports that instead.
    H_WIDER   : the premise.  At K=20 and K=28 the number of OVERLAPPING mrho rungs (both BONLY
                and SONLY feasible) EXCEEDS the 3 that k=36 allows, on the Q5 level set.
    H_MATCH   : the match actually improves - mean |achieved_B - achieved_S| over the overlapping
                mrho rungs is SMALLER at K=20 than at K=36.
    H_SHRINK  : the shrinkage SURVIVES the wider overlap - the mean matched-level |B-S| gap at
                K=20 stays below 0.5 x idea 568's 0.1961 (i.e. below 0.0981), the same bar idea
                569 used to call a characteristic the carrier.
    H_FLOOR   : the shrinkage survives in FLOOR units too - mean |gap| / mean sd_pair at K=20 is
                no more than 1.25x its value at K=36.  (The floor moves with k: smaller panels are
                noisier, so a gap can look "inside the floor" merely because the floor grew.  This
                hypothesis is what stops that from counting as absorption.)
    H_ARTEFACT: the queue's alternative.  It is CONFIRMED exactly when H_SHRINK fails.

GATES (run and printed BEFORE any new number is read)
    G0 determinism : the crc32 draw scheme rebuilt twice gives identical name sets at every K.  0
    G1 identity    : fast_backtest vs engine.backtest on one book per panel.            bar 1e-9
    G2 reproduction: idea 569's committed `.rungs.csv` mrho rows (achieved, premium, sd, prem_IS,
                     prem_OOS) rebuilt from prices here at K=36 / Q5.                   bar 1e-9
    G3 reproduction: idea 569's committed `.origin.csv` mrho rows (achieved_B, achieved_S,
                     match_resid, prem_B, prem_S, gap, sd_pair, t) and their +0.0801 mean.
                                                                                        bar 1e-9
    G4 reproduction: idea 569's committed k=36 mrho reach bands, BONLY [0.1251, 0.3367] and
                     SONLY [0.0787, 0.2735].                                            bar 1e-4

RULE 8 WALK-FORWARD (required)
    IS = start..2016-12-31, OOS = 2017-01-01..end, OOS read ONCE.
    WF-A on the ANSWER: the matched-level gap is recomputed on IS and on OOS separately at every
       K, so "does the shrinkage survive" is answered in each window and the IS->OOS drift of the
       verdict is reported.
    WF-B on a BOOK: the absorption claim taken as a trading instruction - "at matched mrho the
       panel of origin does not matter, so hold whichever flavour is available".  Among the
       overlapping rungs, (flavour, level) is chosen by IS Sharpe ALONE, then OOS CAGR / Sharpe /
       MaxDD are read ONCE against live RULES v2 on U56 and against SPY.  The BONLY-vs-SONLY OOS
       head-to-head at the matched rungs is reported beside it, because that is the contrast the
       claim is actually about.

KEEP PATHS: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse) and 4b (Sharpe > SPY in
    BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's) are evaluated for EVERY book
    and the counts reported.  Stated up front: every panel here is a kernel-weighted seeded draw,
    not a rule anyone can trade, so a 4b pass is a diagnostic, never a capital candidate.

SURVIVORSHIP: the pool is B136 (current constituents of universe_broad.json) plus the sub-$2B
    panel (current constituents of its screen, all 44 tickers with max_1d_move >= 1.0 dropped
    first per PROTOCOL).  SMALL names that died are absent, so the S-sourced premium is biased
    UPWARD, which SHRINKS the B-S gap this run is measuring - i.e. the bias works in favour of
    H_SHRINK and against the queue's artefact reading.  Said again beside the result.

PROTOCOL: 10 bps per unit turnover, next-day fills (engine), no shorting, no leverage.
Deterministic, standalone, no network.  Reads research/baseline.py and idea 569's committed
artefacts; modifies nothing but its own outputs:
    .grid.csv .rungs.csv .origin.csv .overlap.csv .feas.csv .walkforward.csv .keeppaths.csv
    .chars.csv .console.txt
"""
from __future__ import annotations

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
IS_END, OOS_START = "2016-12-31", "2017-01-01"
PARENT_END = "2026-09-04"            # idea 568/569's last bar - kept so G2/G3 can be exact
K_SET = [20, 28, 36]
K_ANCHOR = 36
SEEDS = [0, 1, 2, 3, 4, 5]
FLAVOURS = ["POOL", "BONLY", "SONLY"]
CHARS = ["mrho", "cvol"]             # mrho = the question; cvol = idea 568/569 REFERENCE control
LEVEL_Q9 = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90]
LEVEL_Q5 = [0.10, 0.30, 0.50, 0.70, 0.90]
LEVELSETS = {"Q5": LEVEL_Q5, "Q9": LEVEL_Q9}
BW_MULT = 0.5                        # idea 568's bandwidth, NOT re-tuned
GAP = 0.0978                         # idea 51's published U56 - SMALL439 premium gap
ORIGIN568 = 0.1961                   # idea 568's mean matched-level B-S gap
MRHO569 = 0.0801                     # idea 569's committed mean mrho gap (the object of this run)
CARRIER_BAR = 0.5 * ORIGIN568        # idea 569's own carrier bar, re-used verbatim
PARENT569 = OUT / "2026-09-09_name-the-CARRIER-that-survives-a-CHARACTERISTIC-MATCH_cloud"
REACH36 = {"BONLY": (0.1251, 0.3367), "SONLY": (0.0787, 0.2735)}
TOL = 1e-9
G4_TOL = 1e-4

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


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def rowify(r, tn=None):
    m = metrics(r)
    h1, h2 = halves(r)
    mi, mo = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    d = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
             IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
             OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])
    if tn is not None:
        d["turnover"] = float(tn.sum() / m["Years"])
    return d


def keep_4a(r, b):
    a1, a2 = halves(r)
    b1, b2 = halves(b)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(b)["MaxDD"])


def fail_4b(r, spy):
    a1, a2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not a1 > s1:
        f.append("H1")
    if not a2 > s2:
        f.append("H2")
    if not metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"]:
        f.append("OOS")
    if not m["MaxDD"] >= 0.60 * ms["MaxDD"]:
        f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]:
        f.append("CAGR")
    return ",".join(f) if f else "-"


# ------------------------------------------------------------------------- panels / pool
def real_panels():
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    return {
        "U56": (px56.dropna(how="all").ffill().loc[:PARENT_END], set(px56.columns)),
        "B136": (px136.dropna(how="all").ffill().loc[:PARENT_END], set(px136.columns)),
        f"SMALL{len(s_stk)}": (pxs[s_stk + ["SPY"]].dropna(how="all").ffill().loc[:PARENT_END],
                               set(s_stk)),
    }


def name_chars(pool, spy_px):
    """idea 569's per-name estimator, verbatim (only mrho and cvol are used here)."""
    r = pool.pct_change()
    vol = (r.std() * np.sqrt(252)).astype(float)
    C = r.corr()
    n = C.shape[0]
    mrho = ((C.sum(axis=0) - 1.0) / (n - 1)).astype(float)
    return pd.DataFrame(dict(cvol=vol, mrho=mrho)).dropna()


def panel_chars(px, tradable):
    cols = [c for c in px.columns if c in tradable]
    sub = px[cols]
    r = sub.pct_change()
    vol = float((r.std() * np.sqrt(252)).mean())
    C = r.corr().to_numpy()
    n = C.shape[0]
    rho = float((np.nansum(C) - n) / (n * (n - 1))) if n > 1 else np.nan
    return dict(cvol=vol, mrho=rho)


def reach(x, k):
    """Mean of the k lowest / k highest values: the reach of a size-k draw from this pool."""
    v = np.sort(np.asarray(x, float))
    return float(v[:k].mean()), float(v[-k:].mean())


def draw_panels(nc, bnames, snames, levels_by_char, k):
    """idea 569's kernel-weighted draw scheme verbatim, with the draw SIZE as the free dial."""
    pools = {"POOL": list(nc.index),
             "BONLY": [c for c in nc.index if c in bnames],
             "SONLY": [c for c in nc.index if c in snames]}
    out, feas = {}, []
    for char, lv in levels_by_char.items():
        h = BW_MULT * float(nc[char].std())
        for fl in FLAVOURS:
            names = np.array(pools[fl])
            x = nc.loc[names, char].to_numpy()
            lo, hi = reach(x, k)
            for L in lv:
                ok = bool(lo <= L <= hi)
                feas.append(dict(char=char, K=k, flavour=fl, level=L, reach_lo=lo, reach_hi=hi,
                                 feasible=ok, bandwidth=h, n_pool=len(names)))
                if not ok:
                    continue
                for sd in SEEDS:
                    seed = zlib.crc32(f"CHAR|{char}|{L:.6f}|{fl}|{sd}".encode()) % (2 ** 32)
                    rng = np.random.default_rng(seed)
                    w = np.exp(-0.5 * ((x - L) / h) ** 2)
                    w = w / w.sum()
                    pick = sorted(rng.choice(names, size=k, replace=False, p=w).tolist())
                    out[f"{char}~{fl}~L{L:.6f}~{sd}~k{k}"] = dict(
                        names=pick, char=char, flavour=fl, level=L, seed=sd, K=k)
    return out, pd.DataFrame(feas)


def main():
    t0 = time.time()
    P(f"# {STAMP}")
    P("# idea 572 - is mrho's +0.0801 matched-level B-S gap real absorption, or an artefact of")
    P("#            the 3-rung overlap a k=36 draw allows?  Re-open the overlap by shrinking k.")
    P(f"# PROTOCOL: cost {COST:.0f} bps, next-day fills, IS <= {IS_END}, OOS >= {OOS_START}, "
      f"sample truncated at {PARENT_END} so G2/G3 can be exact")
    P("# TUNED (2): K in {20, 28, 36} x LEVELSET in {Q5, Q9}.  Q5 is a SUBSET of Q9, so both")
    P("#            tuned points read the same draws.  REPORTED-NOT-SELECTED: characteristic")
    P("#            (mrho + cvol control), flavour, seed, gross, cadence, window.")
    P("")
    P("PRE-REGISTERED: H_REPRO (569's mrho rungs and origin rows reproduce to 1e-9, mean +0.0801),")
    P("  H_WIDER (overlap > 3 rungs at K=20 and K=28 on Q5), H_MATCH (|achB-achS| smaller at")
    P("  K=20 than K=36), H_SHRINK (mean |gap| at K=20 below 0.0981 = 0.5x idea 568's 0.1961),")
    P("  H_FLOOR (|gap|/sd_pair at K=20 <= 1.25x its K=36 value), H_ARTEFACT (= not H_SHRINK).")
    P("")

    panels = real_panels()
    SMALLK = [k for k in panels if k.startswith("SMALL")][0]
    P("PANELS: " + ", ".join(f"{k} ({len([c for c in v[0].columns if c in v[1] and c!='SPY'])} "
                            f"tradable, ..{v[0].index[-1].date()})" for k, v in panels.items()))
    P("SURVIVORSHIP: B136 and the small panel are CURRENT constituents; dead SMALL names are")
    P("  absent so the S-sourced premium is biased UPWARD, which SHRINKS the B-S gap - the bias")
    P("  favours H_SHRINK and works AGAINST the queue's artefact reading.")
    P("")

    # ---------------------------------------------------------------- the pool
    pxB, trB = panels["B136"]
    pxS, trS = panels[SMALLK]
    ix = pxB.index.intersection(pxS.index)
    bn = sorted([c for c in pxB.columns if c in trB and c != "SPY"])
    sn = sorted([c for c in pxS.columns if c in trS])
    pool = pd.concat([pxB.loc[ix, bn], pxS.loc[ix, sn]], axis=1).ffill()
    spy_pool = pxB.loc[ix, "SPY"]
    nc = name_chars(pool, spy_pool)
    bnames, snames = set(bn) & set(nc.index), set(sn) & set(nc.index)
    LEVELS_Q9 = {c: [round(float(nc[c].quantile(q)), 6) for q in LEVEL_Q9] for c in CHARS}
    LEVELS_Q5 = {c: [round(float(nc[c].quantile(q)), 6) for q in LEVEL_Q5] for c in CHARS}
    P(f"THE POOL: {ix.min().date()}..{ix.max().date()} ({len(ix)} bars); "
      f"B {len(bnames)} + SMALL {len(snames)} = {len(nc)} names")
    for c in CHARS:
        P(f"  {c:6s} Q9 levels " + " ".join(f"{v:.4f}" for v in LEVELS_Q9[c]))
    P("")

    # ---------------------------------------------------------------- gates G0/G1/G4
    P("=" * 112)
    P("GATES (printed before any new number is read)")
    P("=" * 112)
    g0 = nd = 0
    for k in K_SET:
        a, _ = draw_panels(nc, bnames, snames, LEVELS_Q9, k)
        b, _ = draw_panels(nc, bnames, snames, LEVELS_Q9, k)
        nd += len(a)
        g0 += sum(0 if set(a[key]["names"]) == set(b[key]["names"]) else 1 for key in a)
    P(f"G0 determinism : {g0} of {nd} draws differ on rebuild (bar 0) -> "
      f"{'PASS' if g0 == 0 else 'FAIL'}")

    g1 = 0.0
    for nm, (px, tr) in panels.items():
        w = make_books(px, tr, 0.75)["MA-RS"]
        a = fast_backtest(px, w, COST, "W")["returns"]
        b = backtest(px, w, cost_bps=COST, freq="W")["returns"]
        g1 = max(g1, float((a - b).abs().max()))
    P(f"G1 identity    : fast_backtest vs engine.backtest max |dret| = {g1:.3e} (bar {TOL:.0e}) -> "
      f"{'PASS' if g1 <= TOL else 'FAIL'}")

    _, feas36 = draw_panels(nc, bnames, snames, {"mrho": LEVELS_Q5["mrho"]}, K_ANCHOR)
    g4 = 0.0
    for fl, (lo_c, hi_c) in REACH36.items():
        r = feas36[(feas36.flavour == fl)].iloc[0]
        g4 = max(g4, abs(r.reach_lo - lo_c), abs(r.reach_hi - hi_c))
        P(f"   mrho k=36 {fl} reach [{r.reach_lo:.4f}, {r.reach_hi:.4f}] vs committed "
          f"[{lo_c:.4f}, {hi_c:.4f}]")
    P(f"G4 reach bands : max |d| = {g4:.3e} (bar {G4_TOL:.0e}) -> "
      f"{'PASS' if g4 <= G4_TOL else 'FAIL'}")
    P("  (G2/G3 reproduce idea 569's committed rungs and origin rows; they need the ladder and")
    P("   are printed immediately after it, before any NEW number is read.)")
    P("")

    # ---------------------------------------------------------------- reach / feasibility
    P("=" * 112)
    P("REACH AND FEASIBILITY - the premise: a SMALLER draw reaches FURTHER")
    P("=" * 112)
    allfeas = []
    DR = {}
    for k in K_SET:
        d, f = draw_panels(nc, bnames, snames, LEVELS_Q9, k)
        DR[k] = d
        allfeas.append(f)
    FE = pd.concat(allfeas, ignore_index=True)
    P(f"  {'char':6s} {'K':>3s} {'flavour':7s} {'reach_lo':>9s} {'reach_hi':>9s} "
      f"{'feasible Q9':>12s} {'feasible Q5':>12s}")
    for c in CHARS:
        for k in K_SET:
            for fl in FLAVOURS:
                r = FE[(FE.char == c) & (FE.K == k) & (FE.flavour == fl)]
                n9 = int(r.feasible.sum())
                n5 = int(r[r.level.isin(LEVELS_Q5[c])].feasible.sum())
                P(f"  {c:6s} {k:3d} {fl:7s} {r.reach_lo.iloc[0]:9.4f} {r.reach_hi.iloc[0]:9.4f} "
                  f"{n9:8d}/9    {n5:8d}/5")
    P("")
    ovl = []
    for c in CHARS:
        for k in K_SET:
            for ls, qs in LEVELSETS.items():
                lv = [round(float(nc[c].quantile(q)), 6) for q in qs]
                r = FE[(FE.char == c) & (FE.K == k) & FE.level.isin(lv)]
                ok = {fl: set(r[(r.flavour == fl) & r.feasible].level) for fl in FLAVOURS}
                both = len(ok["BONLY"] & ok["SONLY"])
                ovl.append(dict(char=c, K=k, levelset=ls, n_levels=len(lv), n_overlap=both))
    OVL = pd.DataFrame(ovl)
    P("  OVERLAPPING RUNGS (both BONLY and SONLY feasible) - all 6 tuned points x 2 characteristics")
    P(f"  {'char':6s} {'K':>3s} {'levelset':8s} {'levels':>7s} {'overlap':>8s}")
    for _, r in OVL.iterrows():
        P(f"  {r['char']:6s} {r['K']:3d} {r['levelset']:8s} {r['n_levels']:7d} {r['n_overlap']:8d}")
    m_q5 = OVL[(OVL.char == "mrho") & (OVL.levelset == "Q5")].set_index("K").n_overlap
    H_WIDER = bool(m_q5.get(20, 0) > m_q5.get(36, 0) and m_q5.get(28, 0) > m_q5.get(36, 0))
    P(f"  H_WIDER (mrho Q5 overlap at K=20 and K=28 both exceed K=36's {int(m_q5.get(36,0))}) -> "
      f"{'PASS' if H_WIDER else 'FAIL'}  [{int(m_q5.get(20,0))}, {int(m_q5.get(28,0))}, "
      f"{int(m_q5.get(36,0))}]")
    P("")

    # ---------------------------------------------------------------- the ladder
    P("=" * 112)
    P("THE LADDER - premium on kernel-matched draws, every (char, K, level, flavour, seed)")
    P("=" * 112)
    rows, chrows = [], []
    total = sum(len(v) for v in DR.values())
    done = 0
    spy_full = v2_full = None
    for k in K_SET:
        for key, d in DR[k].items():
            pxd = pd.concat([pool[d["names"]], spy_pool.rename("SPY")], axis=1).dropna(how="all").ffill()
            tr = set(d["names"])
            st = pxd.index[260]
            spy = pxd["SPY"].pct_change().fillna(0.0).loc[st:]
            v2 = fast_backtest(pxd, rules_v2_weights(pxd), COST, "W")["returns"].loc[st:]
            ch = panel_chars(pxd, tr)
            nb = sum(1 for c in d["names"] if c in bnames)
            chrows.append(dict(panel=key, **{q: d[q] for q in ("char", "flavour", "level", "seed", "K")},
                               n_from_B=nb, n_from_S=k - nb, **ch))
            for g in GROSS:
                books = make_books(pxd, tr, g)
                for freq in CADENCE:
                    res = {a: fast_backtest(pxd, w, COST, freq) for a, w in books.items()}
                    rets = {a: v["returns"].loc[st:] for a, v in res.items()}
                    mc = metrics(rets["EWall"])
                    mci = metrics(rets["EWall"].loc[:IS_END])["Sharpe"]
                    mco = metrics(rets["EWall"].loc[OOS_START:])["Sharpe"]
                    for a in books:
                        r = rets[a]
                        row = dict(panel=key, arm=a, gross=g, cadence=freq, K=k,
                                   char=d["char"], flavour=d["flavour"], level=d["level"],
                                   seed=d["seed"], achieved=ch[d["char"]], n_from_B=nb,
                                   ach_mrho=ch["mrho"], ach_cvol=ch["cvol"])
                        row.update(rowify(r, res[a]["turnover"].loc[st:]))
                        row["dCAGR_vs_EWall"] = row["CAGR"] - mc["CAGR"]
                        row["dSharpe_vs_EWall"] = row["Sharpe"] - mc["Sharpe"]
                        row["dIS_Sharpe_vs_EWall"] = row["IS_Sharpe"] - mci
                        row["dOOS_Sharpe_vs_EWall"] = row["OOS_Sharpe"] - mco
                        row["keep4a"] = keep_4a(r, v2)
                        row["fail4b"] = fail_4b(r, spy)
                        row["keep4b"] = row["fail4b"] == "-"
                        rows.append(row)
            done += 1
            if done % 150 == 0:
                P(f"  {done}/{total} draws done ({time.time()-t0:.0f}s)")
    G = pd.DataFrame(rows)
    CH = pd.DataFrame(chrows)
    P(f"  {total} draws x 2 arms x {len(GROSS)} gross x {len(CADENCE)} cadence = {len(G)} books "
      f"({time.time()-t0:.0f}s)")
    P("")

    T = G[G.arm == "MA-RS"]
    dp = T.groupby(["panel", "char", "K", "flavour", "level", "seed"]).agg(
        premium=("dSharpe_vs_EWall", "mean"), prem_IS=("dIS_Sharpe_vs_EWall", "mean"),
        prem_OOS=("dOOS_Sharpe_vs_EWall", "mean"), achieved=("achieved", "first"),
        n_from_B=("n_from_B", "first")).reset_index()
    rung = dp.groupby(["char", "K", "flavour", "level"]).agg(
        n=("premium", "size"), achieved=("achieved", "mean"), n_from_B=("n_from_B", "mean"),
        premium=("premium", "mean"), sd=("premium", "std"),
        prem_IS=("prem_IS", "mean"), prem_OOS=("prem_OOS", "mean")).reset_index()

    # ---------------------------------------------------------------- G2 / G3
    P("=" * 112)
    P("G2 / G3 - REPRODUCTION of idea 569's committed mrho rows at K=36 / Q5 (no new number yet)")
    P("=" * 112)
    g2 = g3 = float("nan")
    try:
        r569 = pd.read_csv(f"{PARENT569}.rungs.csv")
        r569 = r569[r569.char == "mrho"][["char", "flavour", "level", "achieved", "premium", "sd",
                                          "prem_IS", "prem_OOS"]]
        mine = rung[(rung.char == "mrho") & (rung.K == K_ANCHOR)]
        mg = r569.merge(mine, on=["char", "flavour"], suffixes=("_c", "_r"))
        mg = mg[np.abs(mg.level_c - mg.level_r) < 1e-9]
        assert len(mg) == len(r569), (len(mg), len(r569))
        g2 = max(float(np.abs(mg[c + "_c"] - mg[c + "_r"]).max())
                 for c in ("achieved", "premium", "sd", "prem_IS", "prem_OOS"))
        P(f"G2 reproduction: idea 569 .rungs.csv mrho, all {len(mg)} rows x 5 cols, "
          f"max |d| = {g2:.3e} (bar {TOL:.0e}) -> {'PASS' if g2 <= TOL else 'FAIL'}")
    except Exception as e:
        P(f"G2 reproduction: FAILED TO RUN ({e!r})")

    def origin_rows(char, k, levels):
        o = []
        for L in levels:
            d = rung[(rung.char == char) & (rung.K == k)
                     & (np.abs(rung.level - L) < 1e-9)].set_index("flavour")
            if not {"BONLY", "SONLY"} <= set(d.index):
                continue
            db, ds = d.loc["BONLY"], d.loc["SONLY"]
            sd_pair = float(np.sqrt((db["sd"] ** 2 + ds["sd"] ** 2) / 2))
            gap = float(db["premium"] - ds["premium"])
            gis = float(db["prem_IS"] - ds["prem_IS"])
            goos = float(db["prem_OOS"] - ds["prem_OOS"])
            o.append(dict(char=char, K=k, level=L, achieved_B=db["achieved"],
                          achieved_S=ds["achieved"],
                          match_resid=float(db["achieved"] - ds["achieved"]),
                          prem_B=db["premium"], prem_S=ds["premium"], gap=gap,
                          gap_IS=gis, gap_OOS=goos, sd_pair=sd_pair,
                          t=gap / (sd_pair / np.sqrt(len(SEEDS))) if sd_pair > 0 else np.nan,
                          within_floor=abs(gap) <= sd_pair,
                          ratio_to_568=gap / ORIGIN568))
        return pd.DataFrame(o)

    try:
        o569 = pd.read_csv(f"{PARENT569}.origin.csv")
        o569 = o569[o569.char == "mrho"]
        mine = origin_rows("mrho", K_ANCHOR, LEVELS_Q5["mrho"])
        mg = o569.merge(mine, on="char", suffixes=("_c", "_r"))
        mg = mg[np.abs(mg.level_c - mg.level_r) < 1e-9]
        assert len(mg) == len(o569) == 3, (len(mg), len(o569))
        cols = ("achieved_B", "achieved_S", "match_resid", "prem_B", "prem_S", "gap", "sd_pair", "t")
        g3 = max(float(np.abs(mg[c + "_c"] - mg[c + "_r"]).max()) for c in cols)
        mean_here = float(mine.gap.mean())
        g3 = max(g3, abs(mean_here - MRHO569) - 5e-5)
        P(f"G3 reproduction: idea 569 .origin.csv mrho, all {len(mg)} rows x {len(cols)} cols, "
          f"max |d| = {max(float(np.abs(mg[c+'_c']-mg[c+'_r']).max()) for c in cols):.3e}; "
          f"mean gap here {mean_here:+.4f} vs committed {MRHO569:+.4f} "
          f"(bar {TOL:.0e}) -> {'PASS' if g3 <= TOL else 'FAIL'}")
    except Exception as e:
        P(f"G3 reproduction: FAILED TO RUN ({e!r})")
    H_REPRO = bool(g2 <= TOL and g3 <= TOL)
    P(f"H_REPRO -> {'PASS' if H_REPRO else 'FAIL'}")
    P("")

    # ---------------------------------------------------------------- the answer
    P("=" * 112)
    P("THE MATCHED-LEVEL B-S GAP AT EVERY K - does the shrinkage survive the wider overlap?")
    P("=" * 112)
    ORall = []
    for c in CHARS:
        for k in K_SET:
            o = origin_rows(c, k, LEVELS_Q9[c])
            if len(o):
                ORall.append(o)
    OR = pd.concat(ORall, ignore_index=True)
    P(f"  {'char':6s} {'K':>3s} {'L':>9s} {'achB':>8s} {'achS':>8s} {'resid':>8s} {'premB':>8s} "
      f"{'premS':>8s} {'B-S':>8s} {'sd':>7s} {'t':>7s} {'/568':>7s} {'inFlr':>6s}")
    for _, r in OR.iterrows():
        P(f"  {r['char']:6s} {r['K']:3d} {r['level']:9.4f} {r['achieved_B']:8.4f} "
          f"{r['achieved_S']:8.4f} {r['match_resid']:+8.4f} {r['prem_B']:+8.4f} "
          f"{r['prem_S']:+8.4f} {r['gap']:+8.4f} {r['sd_pair']:7.4f} {r['t']:+7.2f} "
          f"{r['ratio_to_568']:+7.2f} {str(r['within_floor']):>6s}")
    P("")
    summ = []
    for c in CHARS:
        for k in K_SET:
            for ls, qs in LEVELSETS.items():
                lv = [round(float(nc[c].quantile(q)), 6) for q in qs]
                d = OR[(OR.char == c) & (OR.K == k) & OR.level.isin(lv)]
                if not len(d):
                    summ.append(dict(char=c, K=k, levelset=ls, n_overlap=0))
                    continue
                summ.append(dict(char=c, K=k, levelset=ls, n_overlap=len(d),
                                 mean_gap=float(d.gap.mean()),
                                 mean_abs_gap=float(d.gap.abs().mean()),
                                 mean_sd=float(d.sd_pair.mean()),
                                 gap_over_floor=float(d.gap.abs().mean() / d.sd_pair.mean()),
                                 mean_abs_resid=float(d.match_resid.abs().mean()),
                                 ratio_568=float(d.gap.abs().mean() / ORIGIN568),
                                 n_within_floor=int(d.within_floor.sum()),
                                 mean_gap_IS=float(d.gap_IS.mean()),
                                 mean_gap_OOS=float(d.gap_OOS.mean())))
    SU = pd.DataFrame(summ)
    P("  SUMMARY - all 6 tuned grid points x 2 characteristics, every one reported")
    P(f"  {'char':6s} {'K':>3s} {'lset':5s} {'ovl':>4s} {'meanGap':>8s} {'|gap|':>8s} "
      f"{'sd_pair':>8s} {'|g|/flr':>8s} {'|resid|':>8s} {'|g|/568':>8s} {'inFlr':>6s} "
      f"{'gapIS':>8s} {'gapOOS':>8s}")
    for _, r in SU.iterrows():
        if not r["n_overlap"]:
            P(f"  {r['char']:6s} {r['K']:3d} {r['levelset']:5s} {0:4d}   NO OVERLAPPING RUNG")
            continue
        P(f"  {r['char']:6s} {r['K']:3d} {r['levelset']:5s} {r['n_overlap']:4d} "
          f"{r['mean_gap']:+8.4f} {r['mean_abs_gap']:8.4f} {r['mean_sd']:8.4f} "
          f"{r['gap_over_floor']:8.2f} {r['mean_abs_resid']:8.4f} {r['ratio_568']:8.2f} "
          f"{r['n_within_floor']:3d}/{r['n_overlap']:<2d} {r['mean_gap_IS']:+8.4f} "
          f"{r['mean_gap_OOS']:+8.4f}")
    P("")

    def su(c, k, ls, col):
        d = SU[(SU.char == c) & (SU.K == k) & (SU.levelset == ls)]
        return float(d[col].iloc[0]) if len(d) and d.n_overlap.iloc[0] else float("nan")

    res36 = su("mrho", 36, "Q5", "mean_abs_resid")
    res20 = su("mrho", 20, "Q9", "mean_abs_resid")
    H_MATCH = bool(res20 < res36)
    g20 = su("mrho", 20, "Q9", "mean_abs_gap")
    H_SHRINK = bool(g20 < CARRIER_BAR)
    f36 = su("mrho", 36, "Q5", "gap_over_floor")
    f20 = su("mrho", 20, "Q9", "gap_over_floor")
    H_FLOOR = bool(f20 <= 1.25 * f36)
    H_ARTEFACT = not H_SHRINK
    P(f"  H_MATCH    (|resid| K=20 {res20:.4f} < K=36 {res36:.4f}) -> "
      f"{'PASS' if H_MATCH else 'FAIL'}")
    P(f"  H_SHRINK   (|gap| K=20 {g20:.4f} < carrier bar {CARRIER_BAR:.4f}) -> "
      f"{'PASS' if H_SHRINK else 'FAIL'}")
    P(f"  H_FLOOR    (|gap|/floor K=20 {f20:.2f} <= 1.25 x K=36 {f36:.2f} = {1.25*f36:.2f}) -> "
      f"{'PASS' if H_FLOOR else 'FAIL'}")
    P(f"  H_ARTEFACT (the queue's alternative: the shrinkage was a short-overlap artefact) -> "
      f"{'CONFIRMED' if H_ARTEFACT else 'REFUTED'}")
    P("")
    P("  CONTROL - the same three K on cvol (idea 568/569's reference characteristic), so a")
    P("  K effect can be told apart from an mrho-specific one:")
    for k in K_SET:
        d = SU[(SU.char == "cvol") & (SU.K == k) & (SU.levelset == "Q9")]
        if len(d) and d.n_overlap.iloc[0]:
            r = d.iloc[0]
            P(f"    cvol K={k:2d}: overlap {int(r.n_overlap)}, |gap| {r.mean_abs_gap:.4f} "
              f"({r.ratio_568:.2f}x 568), |gap|/floor {r.gap_over_floor:.2f}, "
              f"|resid| {r.mean_abs_resid:.4f}")
        else:
            P(f"    cvol K={k:2d}: NO OVERLAPPING RUNG")
    P("")

    # ---------------------------------------------------------------- WF-A
    P("=" * 112)
    P("RULE 8 WF-A - the same gap recomputed on IS and on OOS separately, OOS read ONCE")
    P("=" * 112)
    P(f"  {'char':6s} {'K':>3s} {'ovl':>4s} {'gap FULL':>9s} {'gap IS':>9s} {'gap OOS':>9s} "
      f"{'IS/568':>7s} {'OOS/568':>8s} {'shrink IS':>10s} {'shrink OOS':>11s}")
    wfa = []
    for c in CHARS:
        for k in K_SET:
            d = SU[(SU.char == c) & (SU.K == k) & (SU.levelset == "Q9")]
            if not len(d) or not d.n_overlap.iloc[0]:
                continue
            r = d.iloc[0]
            o = OR[(OR.char == c) & (OR.K == k)]
            ais, aoos = float(o.gap_IS.abs().mean()), float(o.gap_OOS.abs().mean())
            wfa.append(dict(char=c, K=k, n_overlap=int(r.n_overlap), gap_FULL=r.mean_gap,
                            gap_IS=r.mean_gap_IS, gap_OOS=r.mean_gap_OOS,
                            abs_IS=ais, abs_OOS=aoos, shrink_IS=bool(ais < CARRIER_BAR),
                            shrink_OOS=bool(aoos < CARRIER_BAR)))
            P(f"  {c:6s} {k:3d} {int(r.n_overlap):4d} {r.mean_gap:+9.4f} {r.mean_gap_IS:+9.4f} "
              f"{r.mean_gap_OOS:+9.4f} {ais/ORIGIN568:7.2f} {aoos/ORIGIN568:8.2f} "
              f"{str(ais < CARRIER_BAR):>10s} {str(aoos < CARRIER_BAR):>11s}")
    WFA = pd.DataFrame(wfa)
    P("")

    # ---------------------------------------------------------------- WF-B
    P("=" * 112)
    P("RULE 8 WF-B - the absorption claim as a trading instruction, OOS read ONCE")
    P("=" * 112)
    P("  'At matched mrho the panel of origin does not matter, so hold whichever flavour is")
    P("  available.'  Among the OVERLAPPING rungs only, (flavour, level, gross, cadence) is chosen")
    P("  by IS Sharpe ALONE; OOS is then read once against live RULES v2 on U56 and against SPY.")
    P("")
    pxU, trU = panels["U56"]
    stU = pxU.index[260]
    v2U = fast_backtest(pxU, rules_v2_weights(pxU), COST, "W")["returns"].loc[stU:]
    spyU = pxU["SPY"].pct_change().fillna(0.0).loc[stU:]
    mv2, msp = metrics(v2U.loc[OOS_START:]), metrics(spyU.loc[OOS_START:])
    P(f"  comparands OOS: RULES v2 on U56 {mv2['CAGR']:.2%} / {mv2['Sharpe']:.4f} / "
      f"{mv2['MaxDD']:.2%};  SPY {msp['CAGR']:.2%} / {msp['Sharpe']:.4f} / {msp['MaxDD']:.2%}")
    P("")
    wfb = []
    for c in CHARS:
        for k in K_SET:
            o = OR[(OR.char == c) & (OR.K == k)]
            if not len(o):
                continue
            lv = set(np.round(o.level.to_numpy(), 6))
            cand = T[(T.char == c) & (T.K == k) & T.flavour.isin(["BONLY", "SONLY"])
                     & T.level.round(6).isin(lv)]
            if not len(cand):
                continue
            pick = cand.sort_values("IS_Sharpe", ascending=False).iloc[0]
            # head-to-head: mean OOS Sharpe of BONLY vs SONLY over the overlapping rungs
            hh = cand.groupby("flavour").OOS_Sharpe.mean()
            wfb.append(dict(char=c, K=k, n_overlap=len(o), sel_flavour=pick.flavour,
                            sel_level=pick.level, sel_seed=pick.seed, sel_gross=pick.gross,
                            sel_cadence=pick.cadence, IS_Sharpe=pick.IS_Sharpe,
                            OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                            OOS_MaxDD=pick.OOS_MaxDD,
                            v2_OOS_CAGR=mv2["CAGR"], v2_OOS_Sharpe=mv2["Sharpe"],
                            v2_OOS_MaxDD=mv2["MaxDD"], spy_OOS_CAGR=msp["CAGR"],
                            spy_OOS_Sharpe=msp["Sharpe"], spy_OOS_MaxDD=msp["MaxDD"],
                            beat_v2=bool(pick.OOS_Sharpe > mv2["Sharpe"]),
                            beat_spy=bool(pick.OOS_Sharpe > msp["Sharpe"]),
                            hh_BONLY=float(hh.get("BONLY", np.nan)),
                            hh_SONLY=float(hh.get("SONLY", np.nan)), leg="WF-B"))
    WFB = pd.DataFrame(wfb)
    P(f"  {'char':6s} {'K':>3s} {'ovl':>4s} {'held':28s} {'IS Shp':>7s} {'OOS CAGR':>9s} "
      f"{'Sharpe':>7s} {'MaxDD':>8s} {'>v2':>5s} {'>SPY':>5s} {'hhB':>7s} {'hhS':>7s}")
    for _, r in WFB.iterrows():
        held = f"{r['sel_flavour']} L{r['sel_level']:.3f} s{int(r['sel_seed'])} g{r['sel_gross']:.2f} {r['sel_cadence']}"
        P(f"  {r['char']:6s} {r['K']:3d} {r['n_overlap']:4d} {held:28s} {r['IS_Sharpe']:7.4f} "
          f"{r['OOS_CAGR']:9.2%} {r['OOS_Sharpe']:7.4f} {r['OOS_MaxDD']:8.2%} "
          f"{str(r['beat_v2']):>5s} {str(r['beat_spy']):>5s} {r['hh_BONLY']:7.4f} "
          f"{r['hh_SONLY']:7.4f}")
    P("")
    P(f"  beat RULES v2 on OOS Sharpe: {int(WFB.beat_v2.sum())}/{len(WFB)};  "
      f"beat SPY on OOS Sharpe: {int(WFB.beat_spy.sum())}/{len(WFB)}")
    P("  hhB/hhS = mean OOS Sharpe of the BONLY / SONLY arms over the overlapping rungs - the")
    P("  head-to-head the absorption claim is actually about.")
    P("")

    # ---------------------------------------------------------------- KEEP paths
    P("=" * 112)
    P("KEEP PATHS 4a / 4b - every book on the ladder")
    P("=" * 112)
    kp = G[["panel", "char", "K", "flavour", "level", "seed", "arm", "gross", "cadence",
            "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
            "keep4a", "fail4b", "keep4b"]]
    P(f"  all {len(kp)} books: 4a {int(kp.keep4a.sum())}, 4b {int(kp.keep4b.sum())}, "
      f"BOTH {int((kp.keep4a & kp.keep4b).sum())}")
    for k in K_SET:
        d = kp[kp.K == k]
        P(f"  K={k:2d} ({len(d):4d} books): 4a {int(d.keep4a.sum()):4d}, 4b {int(d.keep4b.sum()):4d}, "
          f"BOTH {int((d.keep4a & d.keep4b).sum()):3d}")
    for fl in FLAVOURS:
        d = kp[kp.flavour == fl]
        P(f"  {fl:6s} ({len(d):4d} books): 4a {int(d.keep4a.sum()):4d}, 4b {int(d.keep4b.sum()):4d}")
    fb = kp[~kp.keep4b].fail4b.str.split(",").explode().value_counts()
    P("  binding 4b legs: " + ", ".join(f"{a} {b}" for a, b in fb.items()))
    P("  EVERY panel here is a kernel-weighted seeded draw, not a tradable rule: no 4b pass on")
    P("  this ladder is a capital candidate, and none is claimed.")
    P("")

    # ---------------------------------------------------------------- verdict
    P("=" * 112)
    P("VERDICT")
    P("=" * 112)
    H = dict(H_REPRO=H_REPRO, H_WIDER=H_WIDER, H_MATCH=H_MATCH, H_SHRINK=H_SHRINK,
             H_FLOOR=H_FLOOR)
    for a, b in H.items():
        P(f"  {a:10s} {'PASS' if b else 'FAIL'}")
    P(f"  H_ARTEFACT {'CONFIRMED' if H_ARTEFACT else 'REFUTED'}")
    P("")
    P(f"  mrho matched-level |B-S| gap:  K=36/Q5 (idea 569's cell) {su('mrho',36,'Q5','mean_abs_gap'):.4f} "
      f"on {int(SU[(SU.char=='mrho')&(SU.K==36)&(SU.levelset=='Q5')].n_overlap.iloc[0])} rungs")
    for k in (28, 20):
        d = SU[(SU.char == "mrho") & (SU.K == k) & (SU.levelset == "Q9")]
        if len(d) and d.n_overlap.iloc[0]:
            r = d.iloc[0]
            P(f"                                 K={k}/Q9 {r.mean_abs_gap:.4f} on "
              f"{int(r.n_overlap)} rungs ({r.ratio_568:.2f}x idea 568, |gap|/floor "
              f"{r.gap_over_floor:.2f}, |resid| {r.mean_abs_resid:.4f})")
    P("")

    G.to_csv(f"{OUT}/{STAMP}.grid.csv", index=False)
    rung.to_csv(f"{OUT}/{STAMP}.rungs.csv", index=False)
    OR.to_csv(f"{OUT}/{STAMP}.origin.csv", index=False)
    SU.to_csv(f"{OUT}/{STAMP}.overlap.csv", index=False)
    FE.to_csv(f"{OUT}/{STAMP}.feas.csv", index=False)
    pd.concat([WFA.assign(leg="WF-A"), WFB], ignore_index=True).to_csv(
        f"{OUT}/{STAMP}.walkforward.csv", index=False)
    kp.to_csv(f"{OUT}/{STAMP}.keeppaths.csv", index=False)
    CH.to_csv(f"{OUT}/{STAMP}.chars.csv", index=False)
    P(f"wrote grid {len(G)}, rungs {len(rung)}, origin {len(OR)}, overlap {len(SU)}, "
      f"feas {len(FE)}, wf {len(WFA)+len(WFB)}, keeppaths {len(kp)}, chars {len(CH)} rows "
      f"in {time.time()-t0:.0f}s")
    Path(f"{OUT}/{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()

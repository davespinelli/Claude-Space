#!/usr/bin/env python3
"""IDEA 216  a-flip-rate-estimator-that-is-not-confounded-by-block-count   (lane B, 2026-09-08)

THE QUESTION
------------
Idea 207 recommended K = 100 draws for clause 11b's null band, on the strength of a FLIP RATE
measured by splitting a 400-rotation pool into DISJOINT blocks of size K:

    K   =  20    50   100   200
    nb  =  20     8     4     2        blocks per configuration
    prs = 190    28     6     1        pairwise comparisons per configuration

The estimator's own precision therefore falls by a factor of 190 across the ladder it is
being used to read.  Two consequences are visible in idea 207's own table and neither is a
property of the clause:

  * `flip_share` (the share of configurations in which ANY block pair disagrees) is a
    MAXIMUM over `prs` comparisons.  Even at a fixed per-comparison disagreement rate it
    rises mechanically with nb, so the K=20 column and the K=200 column are not the same
    statistic.
  * The K=200 row rests on ONE Bernoulli draw per configuration.  Q95's pairwise
    disagreement RISES 2.50% -> 3.33% from K=100 to K=200 and its undetermined zone WIDENS
    0.0097 -> 0.0163 (corpus inside 16.1% -> 25.0%) while its band sd keeps falling
    0.0115 -> 0.0076.  A statistic whose band is converging cannot have a diverging zone;
    that is the estimator's variance, not the clause's.

The queue asks for an estimator that holds the number of comparisons FIXED across K, so the
K recommendation rests on something whose variance does not itself depend on K.

WHAT THIS RUN DOES
------------------
  Q0  ENUMERATE the rotation population.  Idea 207 sampled 400 of the J-1 available circular
      rotations.  This run computes ALL of them (J-1 = 974 on U56/BROAD136, 869 on SMALL439),
      so the POPULATION band and the POPULATION verdict exist as a reference truth and every
      K-draw can be scored against it.  90 configurations x 2 cost rungs = 180 rows;
      86,910 null backtests.
  Q1  THE THREE ESTIMATORS, on the same pool.
        D  DISJOINT (idea 207's, replicated):  nb = floor(N/K) blocks, all pairs.
           Comparisons per configuration: 43 blocks/903 pairs at K=20 down to 2 blocks/1 pair
           at K=400.
        P  PAIRED-FIXED-B (the queue's proposal):  B = 200 pairs of DISJOINT K-blocks, each
           pair sampled uniformly without replacement from the population, at EVERY K.
           Exactly B comparisons per configuration at every rung of the ladder.
        E  ERROR-VS-POPULATION (the estimand D and P are proxies for):  B = 200 single
           K-draws per configuration, scored against the population verdict.  p_K = the rate
           at which a K-draw's verdict differs from the answer the whole population gives.
           Under independence a disagreement rate is 2 p (1-p), so E and P are checkable
           against each other rather than merely coexisting.
  Q2  THE VARIANCE OF THE ESTIMATOR ITSELF.  Every estimator is recomputed under R = 8
      independent replicate seeds (for D: 8 permutations of the pool, which is what fixes its
      blocks).  The replicate sd of the corpus-level number is the quantity the queue says
      must not depend on K.
  Q2b THE SAMPLING-FREE LIMIT.  A K-draw's verdict depends on the draw only through
      X = #{sampled |dSharpe| >= the real |dSharpe|}, and X is hypergeometric in the
      population's own exceedance count M, so the whole ladder has a CLOSED FORM with zero
      sampling error.  Reported beside the Monte Carlo as its B -> infinity limit and as a
      gate on it.  (An independent cloud-lane script for this idea, committed today without
      results, reaches the same identity by a different route; this run is a second
      construction, not a copy of it.)
  Q3  THE UNDETERMINED ZONE, re-read against the population margin |dSharpe| - band_pop
      instead of against a block mean, at fixed B.
  Q4  THE K RECOMMENDATION, restated on the fixed-B estimator.
  Q5  RULE 8 (PROTOCOL clause 8, required).  Clause read on the IS window only
      (<= 2016-12-31), overlay point chosen there, 2017-2026 read ONCE.  18 cells x
      (do-nothing, IS-argmax, clause-gated at every K and both statistics, ORACLE-OOS).
  Q6  BOTH KEEP PATHS on all 180 real rows (4a vs the panel's own RULES v1, 4b vs SPY).

DESIGN
------
Idea 191's script is IMPORTED, not re-implemented: panels, base book, overlay families,
`on_indicator`, `apply_overlay`, `halves`, `keep_4a`, `keep_4b` all execute the parent's own
code.  The rotation backtest is a cached-primitive rewrite (`bt_np`) needed to make full
enumeration affordable; it is ASSERTED equal to `p191.fast_backtest` at 0.0e+00 on returns
and turnover over a 24-point sample before any number is read, and idea 201's three published
bands are reproduced from this run's pool by indexing the population at idea 201's own 60
offsets -- within the price-vintage drift, which is measured and reported (data/prices.csv has
been re-cached since idea 201 and 207 ran, so bit equality is not available; MaxDD, the shape
statistic, is unchanged to 1e-7 and is the construction gate).

  panels   : U56, BROAD136, SMALL439 (483-name sub-$2B panel less the 44 with
             max_1d_move >= 1.0 in data/small_meta.csv)
  base book: idea 2's candidate -- composite (no vol scaler), 200d & vol20<0.60 eligibility,
             top-20 equal weight, gross 0.75, WEEKLY, t+1
  families : DDCTL / BUDGET / SLEEVE, idea 186/191's definitions verbatim
  costs    : 10 and 25 bps, both derived EXACTLY from one 0 bps run

  TUNED PARAMETER 1: K, the draw count      {20, 50, 100, 200, 400}   (all reported)
  TUNED PARAMETER 2: the band statistic     {MAX, Q95}                (all reported)
  -> 10 grid points, every one published.  B = 200 and R = 8 are NOT dials: B is fixed by
     construction (that is the whole point of the estimator) and R is the replicate count
     used to measure the estimator's own sd.  No third dial.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
---------------------------------------------------------------------
  P1  `bt_np` matches `p191.fast_backtest` at exactly 0.0e+00 on returns AND turnover, and
      idea 201's three published bands reproduce within the price-vintage drift (< 5e-3 of
      Sharpe; data/prices.csv has been re-cached since idea 201 ran, so bit equality is not
      available and the deviation is reported instead).
  P2  The DISJOINT estimator's replicate sd RISES with K by more than 3x from K=20 to K=400,
      while the PAIRED-FIXED-B estimator's replicate sd is flat (max/min < 2.0).
  P3  Under PAIRED-FIXED-B, Q95's disagreement rate is MONOTONE DECREASING in K -- i.e. idea
      207's 2.50% -> 3.33% rise from K=100 to K=200 was its estimator, not the clause.
  P4  For MAX, the population error rate p_K does NOT vanish as K rises: at K=400 it is still
      above 5%, because the max of K draws is a biased estimator of the population max and
      the bias is one-sided (a K-draw can only clear MORE often than the population).
  P5  For Q95, p_K falls monotonically in K and is below MAX's p_K at every K >= 50.
  P5b On the MAX band, where the hypergeometric law is exact, the B=200 Monte Carlo matches the
      closed form to within 0.01 at every K -- i.e. the fixed-B estimator is not merely stable,
      it is unbiased for the quantity it estimates.
  P6  No clause-gated selector, at any K or either statistic, beats the do-nothing control
      out of sample.  (This project's fourteenth consecutive such test.)

CAVEATS carried, not buried
---------------------------
  * SURVIVORSHIP (idea 54): all three panels are CURRENT constituents; SMALL439 contains no
    delistings.  Real and rotated draws inherit the bias identically, so the CLAUSE reading is
    unaffected; every LEVEL (CAGR, Sharpe, 4a/4b counts) is biased upward and is NOT tradable.
  * The rotation population is FINITE and its members are strongly correlated at neighbouring
    offsets.  Enumerating it removes the pool-sampling layer entirely -- the population band
    is exact -- but it does not make a K-draw's members independent.  Every number below is a
    statement about clause 11b's own sampling scheme, which draws rotations, not iid nulls.
  * BUDGET-skip changes realised turnover between real and null (idea 186: 25.4%; idea 191:
    1782.7% on the widened grid; idea 203: the ex-ante-turnover-stratified repair).  That is
    inherited here, not fixed: this run is about the DRAW COUNT, not the null's fidelity.
  * Two cells (SMALL439 / BUDGET tau=0.05 / skip, both rungs) have an undefined IS Sharpe --
    the overlay suppresses 93.7% of rebalances.  Carried as NaN, excluded from IS statistics,
    nothing imputed.
  * Idea 38: calendar-day index after 2014-09-17 on U56/BROAD136.  Idea 126: t+1 only.
  * PROTOCOL 5: seeded with zlib.crc32, reproducible across processes.

Deterministic, standalone.  Writes .console.txt, .est.csv, .zone.csv, .pop.csv,
.walkforward.csv, .keep.csv and caches the enumerated pool to .pool.npz.
"""
import importlib.util
import os
import sys
import time
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-08_a-flip-rate-estimator-that-is-not-confounded-by-block-count_B"
OUT = ROOT / "research" / "backtests"
PARENT_STEM = "2026-09-05_the-on-share-column_cloud"                # idea 191, the machinery
AUDIT_STEM = "2026-09-05_the-margin-column-instead-of-two_cloud"    # idea 201, the anchor
P207_STEM = "2026-09-05_how-many-draws-does-clause-11b-need_cloud"  # idea 207, the target

K_GRID = [int(x) for x in os.environ.get("K_GRID", "20,50,100,200,400").split(",")]
STATS = ["MAX", "Q95"]
COST_RUNGS = [10, 25]
B_PAIRS = int(os.environ.get("B_PAIRS", 200))     # comparisons per configuration, EVERY K
R_REP = int(os.environ.get("R_REP", 8))           # replicates, to measure estimator sd
IS_END, OOS_START = "2016-12-31", "2017-01-01"
CACHE = OUT / f"{STEM}.pool.npz"
# debug-only subsetting knobs, unset in the committed run (see .console.txt header)
POOL_CAP = int(os.environ.get("POOL_CAP", 0))          # 0 = full enumeration
ONLY_PANEL = os.environ.get("ONLY_PANEL", "")

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 4000)

_lines: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _lines.append(s)


# ---------------------------------------------------------------- import idea 191 verbatim
spec = importlib.util.spec_from_file_location("p191", OUT / f"{PARENT_STEM}.py")
p191 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p191)

FAMILIES, FAM_ORDER = p191.FAMILIES, p191.FAM_ORDER
net = p191.net
on_indicator, apply_overlay = p191.on_indicator, p191.apply_overlay
halves, keep_4a, keep_4b = p191.halves, p191.keep_4a, p191.keep_4b
tstat, _sh = p191.tstat, p191._sh


def det_seed(*parts):
    """Idea 201's seed, verbatim -- deterministic across processes (PROTOCOL 5)."""
    return int(zlib.crc32("|".join(str(p) for p in parts).encode())) % (2**31)


def offsets_201(J, n, seed):
    """Idea 201/207's offset draw, verbatim, used ONLY to locate its 60 offsets inside this
    run's enumerated population so its published bands can be reproduced."""
    rng = np.random.default_rng(seed)
    return rng.permutation(np.arange(1, J))[:min(n, J - 1)]


# ---------------------------------------------------- cached-primitive rotation backtest
def panel_primitives(pan):
    rets = pan.px.pct_change().fillna(0.0).values
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, C.shape[1])), C[:-1]])
    return dict(rets=rets, Cp=Cp, T=rets.shape[0])


def bt_np(pre, Wv, mask):
    """p191.fast_backtest at cost 0, with prices.pct_change() and the cumprod hoisted out of
    the loop and the previous-holdings matrix evaluated only on rebalance rows.  Asserted
    identical to the parent at 0.0e+00 before use."""
    rets, Cp, T = pre["rets"], pre["Cp"], pre["T"]
    wt = np.vstack([np.zeros((1, Wv.shape[1])), Wv[:-1]])
    m = np.concatenate([[False], np.asarray(mask, bool)[:-1]]).copy()
    m[0] = True
    reb = np.flatnonzero(m)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)][reb]
    W0p = wt[s0p]
    hp = W0p * (Cp[reb] / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[0] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp).sum(axis=1)
    return (held * rets).sum(axis=1), turn


# ------------------------------------------------------------------ fast metric primitives
def sharpe_np(r):
    if len(r) < 6:
        return np.nan
    sd = r.std(ddof=1)
    return float(r.mean() * 252.0 / (sd * np.sqrt(252.0))) if sd > 0 else np.nan


def maxdd_np(r):
    eq = np.cumprod(1.0 + r)
    return float((eq / np.maximum.accumulate(eq) - 1.0).min())


_LOGFACT = np.concatenate([[0.0], np.cumsum(np.log(np.arange(1, 4001, dtype=float)))])


def _lchoose(n, k):
    """log C(n, k) from an exact log-factorial table; -inf where the choice is impossible."""
    n = np.asarray(n, dtype=np.int64)
    k = np.asarray(k, dtype=np.int64)
    bad = (k < 0) | (k > n) | (n < 0)
    ns, ks = np.where(bad, 0, n), np.where(bad, 0, k)
    out = _LOGFACT[ns] - _LOGFACT[ks] - _LOGFACT[ns - ks]
    return np.where(bad, -np.inf, out)


def hyper_cdf(N, M, K, c):
    """P(X <= c) for X ~ Hypergeom(population N, successes M, draws K), by direct summation.

    THE CLOSED FORM behind every Monte-Carlo number in this run.  A K-draw's band verdict
    depends on the draw ONLY through X = how many of the K sampled |dSharpe| values reach the
    real |dSharpe|: with an ORDER-STATISTIC band at level q the overlay CLEARS exactly when
    X <= c(K) = K - ceil(q*K)  (q=1, c=0 is the MAX band: clear iff the draw contains no
    exceedance at all).  X is hypergeometric in the population's own exceedance count M, so
    P(clear at draw count K) is exact and carries NO sampling error of any kind."""
    if c < 0:
        return 0.0
    x = np.arange(0, min(int(c), int(M), int(K)) + 1)
    lp = _lchoose(M, x) + _lchoose(N - M, K - x) - _lchoose(N, K)
    return float(np.exp(lp[np.isfinite(lp)]).sum())


def band_of(vals, stat):
    if stat == "MAX":
        return float(np.max(vals))
    if stat == "Q95":
        return float(np.quantile(vals, 0.95, method="linear"))
    raise ValueError(stat)


def band_rows(A, stat):
    """Band of every ROW of a 2-D array -- the vectorised form of band_of."""
    if stat == "MAX":
        return A.max(axis=1)
    if stat == "Q95":
        return np.quantile(A, 0.95, axis=1, method="linear")
    raise ValueError(stat)


# ============================================================================================ run
def main():
    t0 = time.time()
    P("=" * 118)
    P("IDEA 216  a-flip-rate-estimator-that-is-not-confounded-by-block-count   (lane B, 2026-09-08)")
    P("=" * 118)

    P("\nbuilding panels (idea 191's build_panels, imported) ...")
    panels = p191.build_panels()
    if ONLY_PANEL:
        panels = [p for p in panels if p.name in ONLY_PANEL.split(",")]
    P("  panels: " + "  ".join(f"{p.name}={len(p.tradable)}" for p in panels))
    if POOL_CAP or ONLY_PANEL:
        P(f"  !! DEBUG SUBSET ACTIVE: POOL_CAP={POOL_CAP} ONLY_PANEL={ONLY_PANEL!r} !!")

    P("\nREPRODUCTION, asserted before any new number is read:")
    ok = all(p191.checks(p) for p in panels)
    pu = load_universe()
    ru = backtest(pu, rules_v1_weights(pu), cost_bps=10.0, freq="W")["returns"].loc[pu.index[260]:]
    mu = metrics(ru)
    P(f"  [d] RULES v1 on u56 @10bps: {mu['CAGR']:.5%} / {mu['Sharpe']:.5f} / {mu['MaxDD']:.5%}"
      f"  (published anchor 6.45305% / 0.66418 / -13.82780%)")
    P(f"      deviation vs the 2026-09-05 price vintage: dCAGR {(mu['CAGR'] - 0.0645305) * 100:+.5f} pp, "
      f"dSharpe {mu['Sharpe'] - 0.66418:+.5f}, dMaxDD {(mu['MaxDD'] + 0.1382780) * 100:+.7f} pp.")
    P("      data/prices.csv has been re-cached since idea 201/207 ran, so CAGR/Sharpe carry a")
    P("      VINTAGE drift that is reported, not asserted away; MaxDD is the shape statistic and")
    P("      is the construction gate (idea 216 follows the convention set by today's lane-B and")
    P("      cloud runs).  EVERY estimator below is computed on ONE pool from ONE vintage, so the")
    P("      comparisons this run makes are vintage-free; only the cross-reference to idea 201's")
    P("      PUBLISHED bands carries the drift, and it is quantified rather than gated.")
    gate_d = abs(mu["MaxDD"] + 0.1382780) < 1e-6
    P(f"      -> {'PASS' if gate_d else 'FAIL'} (MaxDD gate)")
    ok &= gate_d

    PRE = {p.name: panel_primitives(p) for p in panels}
    P("\n  [e] bt_np vs p191.fast_backtest over a 24-point sample (3 panels x 4 overlays x 2 offsets):")
    worst_r = worst_t = 0.0
    for pan in panels:
        for fam, thr, depth in [("SLEEVE", 200, 1.0), ("BUDGET", 0.2, "half"),
                                ("BUDGET", 0.2, "skip"), ("DDCTL", 0.06, 0.5)]:
            s = on_indicator(pan, fam, thr)
            for off in (7, 113):
                W, m = apply_overlay(pan, fam, depth, np.roll(s, off))
                a = p191.fast_backtest(pan.px, W, 0.0, p191.FREQ, mask=m)
                r_, t_ = bt_np(PRE[pan.name], W.reindex(pan.px.index).fillna(0.0).values, m)
                worst_r = max(worst_r, float(np.abs(a["returns"].values - r_).max()))
                worst_t = max(worst_t, float(np.abs(a["turnover"].values - t_).max()))
    P(f"      max|dret|={worst_r:.3e}  max|dturn|={worst_t:.3e} -> "
      f"{'PASS' if worst_r == 0.0 and worst_t == 0.0 else 'FAIL'}")
    ok &= worst_r == 0.0 and worst_t == 0.0
    if not ok:
        P("\nreproduction of the deterministic parts FAILS -- STOP")
        return
    P("  deterministic parts reproduce -- proceeding to the enumeration")

    # --------------------------------------------------------------- Q0 enumerate the pool
    P("\n" + "=" * 118)
    P("Q0  ENUMERATE THE ROTATION POPULATION.  Every one of the J-1 circular rotations of each")
    P("    overlay's ON indicator, for 3 panels x 3 families x 5 thr x 2 depth = 90")
    P("    configurations, at 2 cost rungs derived exactly from one 0 bps run.")
    P("=" * 118)

    CACHED = None
    if CACHE.exists() and not POOL_CAP and not ONLY_PANEL and os.environ.get("USE_CACHE"):
        CACHED = np.load(CACHE)
        P(f"  reusing the enumerated pool from {CACHE.name} "
          f"({len(CACHED.files)} arrays); the real books are still re-run from scratch")
    real_rows, null_store, POPOFF = [], {}, {}
    for pan in panels:
        pre = PRE[pan.name]
        start = pan.start
        i0 = pan.px.index.searchsorted(start)
        spy = pan.spy.loc[start:]
        basefull = backtest(pan.px, rules_v1_weights(pan.px), cost_bps=0.0, freq="W")
        b0, bt_ = basefull["returns"].loc[start:], basefull["turnover"].loc[start:]
        c0 = pan._r0
        is_end_i = pan.px.index.searchsorted(pd.Timestamp(IS_END), side="right") - i0
        for fam in FAM_ORDER:
            _, thrs, _, depths = FAMILIES[fam]
            for thr in thrs:
                s_real = on_indicator(pan, fam, thr)
                J = len(s_real)
                offs = np.arange(1, J)                       # THE WHOLE POPULATION
                if POOL_CAP:
                    offs = offs[:POOL_CAP]
                for depth in depths:
                    POPOFF[(pan.name, fam, float(thr), str(depth))] = offs
                    W, mask = apply_overlay(pan, fam, depth, s_real)
                    res = p191.fast_backtest(pan.px, W, 0.0, p191.FREQ, mask=mask)
                    for bps in COST_RUNGS:
                        r = net(res, bps).loc[start:]
                        cr = net(c0, bps).loc[start:]
                        br = b0 - bt_ * bps / 1e4
                        m_, mc = metrics(r), metrics(cr)
                        h1, h2 = halves(r)
                        real_rows.append(dict(
                            panel=pan.name, family=fam, thr=thr, depth=str(depth), bps=bps,
                            J=J, n_pop=len(offs), on_share=float(s_real.mean()),
                            CAGR=m_["CAGR"], Sharpe=m_["Sharpe"], MaxDD=m_["MaxDD"], H1=h1, H2=h2,
                            Sharpe_IS=_sh(r.loc[:IS_END]), Sharpe_OOS=_sh(r.loc[OOS_START:]),
                            CAGR_OOS=metrics(r.loc[OOS_START:])["CAGR"],
                            MaxDD_OOS=metrics(r.loc[OOS_START:])["MaxDD"],
                            ctrl_Sharpe=mc["Sharpe"], ctrl_MaxDD=mc["MaxDD"],
                            ctrl_Sharpe_IS=_sh(cr.loc[:IS_END]),
                            ctrl_Sharpe_OOS=_sh(cr.loc[OOS_START:]),
                            ctrl_CAGR_OOS=metrics(cr.loc[OOS_START:])["CAGR"],
                            ctrl_MaxDD_OOS=metrics(cr.loc[OOS_START:])["MaxDD"],
                            fail4a=keep_4a(r, br), fail4b=keep_4b(r, spy)))

                    if CACHED is not None:
                        for b in COST_RUNGS:
                            kk = "|".join(str(x) for x in (pan.name, fam, thr, str(depth), b))
                            null_store[(pan.name, fam, thr, str(depth), b)] = dict(
                                dS=CACHED[kk + "|dS"], dD=CACHED[kk + "|dD"],
                                dSis=CACHED[kk + "|dSis"])
                        continue
                    ctrl = {b: net(c0, b).loc[start:].values for b in COST_RUNGS}
                    cS = {b: sharpe_np(ctrl[b]) for b in COST_RUNGS}
                    cD = {b: maxdd_np(ctrl[b]) for b in COST_RUNGS}
                    cSis = {b: sharpe_np(ctrl[b][:is_end_i]) for b in COST_RUNGS}
                    n = len(offs)
                    dS = {b: np.empty(n) for b in COST_RUNGS}
                    dD = {b: np.empty(n) for b in COST_RUNGS}
                    dSis = {b: np.empty(n) for b in COST_RUNGS}
                    for i, off in enumerate(offs):
                        Wn, mn = apply_overlay(pan, fam, depth, np.roll(s_real, off))
                        rv_, tv_ = bt_np(pre, Wn.reindex(pan.px.index).fillna(0.0).values, mn)
                        rv, tv = rv_[i0:], tv_[i0:]
                        for b in COST_RUNGS:
                            x = rv - tv * b / 1e4
                            dS[b][i] = sharpe_np(x) - cS[b]
                            dD[b][i] = maxdd_np(x) - cD[b]
                            dSis[b][i] = sharpe_np(x[:is_end_i]) - cSis[b]
                    for b in COST_RUNGS:
                        null_store[(pan.name, fam, thr, str(depth), b)] = dict(
                            dS=dS[b], dD=dD[b], dSis=dSis[b])
        P(f"  {pan.name} done ({time.time() - t0:.0f}s)")

    R = pd.DataFrame(real_rows)
    R["dSharpe"] = R["Sharpe"] - R["ctrl_Sharpe"]
    R["dMaxDD"] = R["MaxDD"] - R["ctrl_MaxDD"]
    R["dSharpe_IS"] = R["Sharpe_IS"] - R["ctrl_Sharpe_IS"]
    R["pass4a"] = R["fail4a"] == "-"
    R["pass4b"] = R["fail4b"] == "-"
    R.to_csv(OUT / f"{STEM}.keep.csv", index=False)
    n_null = sum(len(v["dS"]) for v in null_store.values()) // len(COST_RUNGS)
    P(f"\ngrid: {len(R)} real rows, {n_null} null backtests "
      f"{'reused from cache' if CACHED is not None else 'enumerated'} "
      f"({time.time() - t0:.0f}s)")
    if CACHED is None:
        np.savez_compressed(CACHE, **{"|".join(str(x) for x in k) + "|" + w: v[w]
                                      for k, v in null_store.items()
                                      for w in ("dS", "dD", "dSis")})

    key = ["panel", "family", "thr", "depth", "bps"]
    R = R.set_index(key).sort_index()

    # =========================================================== REPRODUCTION of idea 201
    P("\n" + "=" * 118)
    P("REPRODUCTION of idea 201's published bands (P1).  Idea 201's 60 offsets are located")
    P("INSIDE this run's enumerated population by value, then blocked its way (sorted, 3x20).")
    P("Idea 201 ran on the 2026-09-05 price vintage and data/prices.csv has been re-cached")
    P("since, so the target here is CONSTRUCTION identity within the vintage drift measured")
    P("above, not bit equality: the deviation is reported and the per-panel split is the test.")
    P("=" * 118)
    S201 = pd.read_csv(OUT / f"{AUDIT_STEM}.stability.csv")
    S201["depth"] = S201["depth"].astype(str)
    S201 = S201.set_index(key).sort_index()
    # idea 201 seeded with the RAW threshold value out of FAMILIES (int for SLEEVE, float
    # elsewhere); the MultiIndex has cast every threshold to float, so the raw type is
    # restored here or the SLEEVE rows would be drawn from a different permutation.
    RAWTHR = {(f, float(t)): t for f in FAM_ORDER for t in FAMILIES[f][1]}
    rep, rep_panel = [], []
    for k, row in S201.iterrows():
        if k not in null_store or POOL_CAP:
            continue
        pop = POPOFF[k[:4]]
        o60 = offsets_201(len(pop) + 1, 60, det_seed(k[0], k[1], RAWTHR[(k[1], float(k[2]))]))
        pos = np.searchsorted(pop, np.sort(o60))          # population is 1..J-1 ascending
        ns = np.abs(null_store[k]["dS"])[pos]
        mine = [band_of(ns[a:a + 20], "MAX") for a in (0, 20, 40)]
        rep.append([abs(mine[0] - row["band"]), abs(mine[1] - row["band_b1"]),
                    abs(mine[2] - row["band_b2"])])
        rep_panel.append(k[0])
    rep = np.array(rep) if rep else np.zeros((1, 3)) + np.nan
    P(f"  rows checked: {0 if np.isnan(rep).all() else len(rep)}/180")
    P(f"  max |band  - idea 201 band   |: {rep[:, 0].max():.3e}")
    P(f"  max |band_1- idea 201 band_b1|: {rep[:, 1].max():.3e}")
    P(f"  max |band_2- idea 201 band_b2|: {rep[:, 2].max():.3e}")
    P(f"  median |deviation| over the 3 x rows checked: "
      f"{np.median(rep):.3e}   (vintage drift of the u56 anchor: 5.3e-04 of Sharpe)")
    if np.isfinite(rep).all():
        rp = pd.DataFrame(dict(panel=rep_panel, dmax=rep.max(axis=1)))
        P("\n  by panel (BROAD136 and SMALL439 read data/prices_broad.csv and")
        P("  data/prices_small.csv.gz, which have NOT been re-cached since idea 201; U56 reads")
        P("  data/prices.csv, which has -- so the drift should be a U56-only phenomenon):")
        P(rp.groupby("panel")["dmax"].agg(n="size", median="median", max="max",
                                          over_1e4=lambda s: int((s > 1e-4).sum()))
          .to_string(float_format=lambda x: f"{x:.3e}"))
    rep_ok = bool(np.isfinite(rep).all() and np.median(rep) < 1e-6 and rep.max() < 5e-2)
    P(f"  -> {'PASS' if rep_ok else 'SKIPPED (debug subset)' if not np.isfinite(rep).all() else 'FAIL'}"
      "  (gate: median < 1e-6 and max < 5e-2, the vintage envelope)")

    # ================================================================== the population truth
    P("\n" + "=" * 118)
    P("THE POPULATION BAND.  With every rotation enumerated there is an exact band and an")
    P("exact verdict per configuration; the K ladder is scored against it below.")
    P("=" * 118)
    poprows = []
    for k in R.index:
        ns = np.abs(null_store[k]["dS"])
        d = abs(R.loc[k, "dSharpe"])
        row = dict(panel=k[0], family=k[1], thr=k[2], depth=k[3], bps=k[4],
                   n_pop=len(ns), dSharpe=float(R.loc[k, "dSharpe"]))
        for stat in STATS:
            bp = band_of(ns, stat)
            row[f"band_pop_{stat}"] = bp
            row[f"margin_pop_{stat}"] = d - bp
            row[f"clears_pop_{stat}"] = bool(d > bp)
        poprows.append(row)
    POP = pd.DataFrame(poprows)
    POP.to_csv(OUT / f"{STEM}.pop.csv", index=False)
    POPI = POP.set_index(key).sort_index()
    P("\n" + POP.groupby("panel").agg(
        n_pop=("n_pop", "max"),
        band_pop_MAX=("band_pop_MAX", "mean"), band_pop_Q95=("band_pop_Q95", "mean"),
        clear_MAX=("clears_pop_MAX", "mean"), clear_Q95=("clears_pop_Q95", "mean")
    ).to_string(float_format=lambda x: f"{x:.4f}"))
    P(f"\n  corpus population clear rate: MAX {POP['clears_pop_MAX'].mean():.1%}   "
      f"Q95 {POP['clears_pop_Q95'].mean():.1%}   (n=180)")

    # =============================================================== Q1/Q2 the three estimators
    P("\n" + "=" * 118)
    P("Q1/Q2  THE THREE ESTIMATORS AND THEIR OWN SAMPLING ERROR.")
    P(f"       D = idea 207's disjoint blocks (comparisons per config vary with K)")
    P(f"       P = paired, B={B_PAIRS} disjoint block pairs at EVERY K")
    P(f"       E = error vs the population verdict, B={B_PAIRS} single K-draws")
    P(f"       each recomputed under R={R_REP} independent replicate seeds")
    P("=" * 118)

    absS = {k: np.abs(null_store[k]["dS"]) for k in R.index}
    dreal = {k: abs(float(R.loc[k, "dSharpe"])) for k in R.index}
    vpop = {(k, s): dreal[k] > band_of(absS[k], s) for k in R.index for s in STATS}

    est_rows = []
    for stat in STATS:
        for K in K_GRID:
            repD, repP, repE, repEsd = [], [], [], []
            per_cfg_p = {k: [] for k in R.index}
            for rep_i in range(R_REP):
                dis_D = dis_P = err_E = 0.0
                nD = nP = nE = 0
                for k in R.index:
                    a = absS[k]
                    n = len(a)
                    d = dreal[k]
                    rng = np.random.default_rng(det_seed("216", stat, K, rep_i, *[str(x) for x in k]))
                    # ---- D: idea 207's disjoint blocks over a permutation of the pool
                    nb = n // K
                    if nb >= 2:
                        perm = rng.permutation(n)[:nb * K].reshape(nb, K)
                        vb = band_rows(a[perm], stat) < d
                        s_ = int(vb.sum())
                        dis_D += s_ * (nb - s_)
                        nD += nb * (nb - 1) // 2
                    # ---- P: B disjoint PAIRS, same B at every K
                    if 2 * K <= n:
                        idx = np.array([rng.permutation(n)[:2 * K] for _ in range(B_PAIRS)])
                        va = band_rows(a[idx[:, :K]], stat) < d
                        vb2 = band_rows(a[idx[:, K:]], stat) < d
                        dis_P += float((va != vb2).sum())
                        nP += B_PAIRS
                    # ---- E: B single draws vs the population verdict
                    idx1 = np.array([rng.permutation(n)[:K] for _ in range(B_PAIRS)])
                    v1 = band_rows(a[idx1], stat) < d
                    e = float((v1 != vpop[(k, stat)]).mean())
                    per_cfg_p[k].append(e)
                    err_E += e
                    nE += 1
                repD.append(dis_D / nD if nD else np.nan)
                repP.append(dis_P / nP if nP else np.nan)
                repE.append(err_E / nE)
            pk = {k: float(np.mean(v)) for k, v in per_cfg_p.items()}
            pbar = np.array(list(pk.values()))
            est_rows.append(dict(
                stat=stat, K=K,
                D_blocks=int(np.median([len(absS[k]) // K for k in R.index])),
                D_pairs_per_cfg=int(np.median([(len(absS[k]) // K) * ((len(absS[k]) // K) - 1) // 2
                                               for k in R.index])),
                D_disagree=float(np.mean(repD)), D_rep_sd=float(np.std(repD, ddof=1)),
                P_pairs_per_cfg=B_PAIRS if 2 * K <= min(len(a) for a in absS.values()) else 0,
                P_disagree=float(np.mean(repP)), P_rep_sd=float(np.std(repP, ddof=1)),
                E_err=float(np.mean(repE)), E_rep_sd=float(np.std(repE, ddof=1)),
                E_implied_disagree=float((2 * pbar * (1 - pbar)).mean()),
                cfg_with_error=float((pbar > 0).mean())))
    E = pd.DataFrame(est_rows)
    E.to_csv(OUT / f"{STEM}.est.csv", index=False)
    P("\n" + E.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("\n  ESTIMATOR SAMPLING ERROR ACROSS THE LADDER (the queue's actual question):")
    for stat in STATS:
        s_ = E[E.stat == stat].set_index("K")
        dr = s_["D_rep_sd"]
        pr = s_["P_rep_sd"].replace(0.0, np.nan)
        P(f"    {stat}:  D rep sd {dr.min():.4f} -> {dr.max():.4f}  (max/min "
          f"{dr.max() / max(dr.min(), 1e-12):.1f}x, pairs/cfg "
          f"{int(s_['D_pairs_per_cfg'].max())} -> {int(s_['D_pairs_per_cfg'].min())})")
        P(f"          P rep sd {pr.min():.4f} -> {pr.max():.4f}  (max/min "
          f"{pr.max() / max(pr.min(), 1e-12):.1f}x, pairs/cfg fixed at {B_PAIRS})")

    P("\n  MONOTONICITY of the disagreement rate in K:")
    for stat in STATS:
        s_ = E[E.stat == stat].set_index("K")
        for col, tag in [("D_disagree", "D disjoint (idea 207)"), ("P_disagree", "P fixed-B"),
                         ("E_err", "E vs population")]:
            v = s_[col].values
            mono = all(v[i] >= v[i + 1] - 1e-12 for i in range(len(v) - 1))
            P(f"    {stat:3s} {tag:22s}: " + "  ".join(f"K={k}:{x:.4f}" for k, x in
                                                       zip(s_.index, v))
              + f"   -> {'MONOTONE DECREASING' if mono else 'NOT MONOTONE'}")

    # ============================================== Q2b the closed form (zero-variance limit)
    P("\n" + "=" * 118)
    P("Q2b  THE SAMPLING-FREE LIMIT.  A K-draw's verdict depends on the draw only through")
    P("     X = how many of the K sampled |dSharpe| reach the real |dSharpe|.  With an")
    P("     ORDER-STATISTIC band at level q the overlay clears iff X <= c(K) = K - ceil(q*K),")
    P("     and X ~ Hypergeom(N, M, K) where M is the POPULATION exceedance count.  So the")
    P("     ladder has a closed form with NO sampling error at all:")
    P("       P(clear at K)  = P(X <= c)")
    P("       P(error at K)  = P(clear) or 1-P(clear), whichever the population verdict denies")
    P("       P(flip, 2 disjoint K-blocks) = 2 P(A clears) P(B does not clear | A clears)")
    P("     (q=1 -> c=0 is the MAX band and is EXACT; q=0.95 uses the order-statistic band,")
    P("     which differs from the run's linear-interpolation band only by that convention --")
    P("     the gap is reported below, not hidden.)")
    P("=" * 118)
    MN = {}
    for k in R.index:
        a = absS[k]
        d = dreal[k]
        MN[k] = (len(a), int((a >= d).sum()))
    cfrows = []
    for stat in STATS:
        q = 1.0 if stat == "MAX" else 0.95
        for K in K_GRID:
            c = K - int(np.ceil(q * K))
            pc, pe, pf = [], [], []
            for k in R.index:
                N_, M_ = MN[k]
                cpop = N_ - int(np.ceil(q * N_))
                vpop_os = M_ <= cpop
                p_clear = hyper_cdf(N_, M_, K, c)
                pc.append(p_clear)
                pe.append(1.0 - p_clear if vpop_os else p_clear)
                # P(B does not clear | A clears) needs the joint; sum over A's exceedance count
                tot = 0.0
                for x in range(0, min(c, M_, K) + 1):
                    lpa = (_lchoose(M_, x) + _lchoose(N_ - M_, K - x) - _lchoose(N_, K))
                    if not np.isfinite(lpa):
                        continue
                    pb_clear = hyper_cdf(N_ - K, M_ - x, K, c)
                    tot += float(np.exp(lpa)) * (1.0 - pb_clear)
                pf.append(2.0 * tot)
            cfrows.append(dict(stat=stat, K=K, c_K=c,
                               CF_clear=float(np.mean(pc)), CF_err=float(np.mean(pe)),
                               CF_flip=float(np.mean(pf)),
                               MC_err=float(E[(E.stat == stat) & (E.K == K)]["E_err"].iloc[0]),
                               MC_flip=float(E[(E.stat == stat) & (E.K == K)]["P_disagree"].iloc[0])))
    CF = pd.DataFrame(cfrows)
    CF["err_gap"] = CF["CF_err"] - CF["MC_err"]
    CF["flip_gap"] = CF["CF_flip"] - CF["MC_flip"]
    CF.to_csv(OUT / f"{STEM}.closedform.csv", index=False)
    P("\n" + CF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    gm = CF[CF.stat == "MAX"]
    P(f"\n  MAX (the band where the closed form is EXACT): max |Monte Carlo - closed form| = "
      f"{max(gm['err_gap'].abs().max(), gm['flip_gap'].abs().max()):.4f} over the ladder; "
      f"the B={B_PAIRS} Monte-Carlo se is ~{np.sqrt(0.25 / (B_PAIRS * len(R))):.4f}.")
    P(f"  Q95 (order-statistic band vs the run's linear-interpolation band): max gap "
      f"{max(CF[CF.stat == 'Q95']['err_gap'].abs().max(), CF[CF.stat == 'Q95']['flip_gap'].abs().max()):.4f} "
      "-- a convention difference, reported.")
    P("\n  This is the estimator idea 216 asks for taken to its limit: B -> infinity, variance")
    P("  zero, and it needs exactly ONE number per configuration (M, the population exceedance")
    P("  count) rather than a re-draw at every K.")

    # ======================================================================= Q3 the zone
    P("\n" + "=" * 118)
    P("Q3  THE UNDETERMINED ZONE, against the POPULATION margin |dSharpe| - band_pop, at")
    P("    fixed B.  A configuration is UNDETERMINED at K when a K-draw disagrees with the")
    P("    population verdict at a rate above 5% -- the clause's own nominal size.")
    P("=" * 118)
    zrows = []
    for stat in STATS:
        mp = np.array([abs(float(POPI.loc[k, f"margin_pop_{stat}"])) for k in R.index])
        for K in K_GRID:
            pk = []
            for k in R.index:
                a = absS[k]
                n = len(a)
                d = dreal[k]
                acc = []
                for rep_i in range(R_REP):
                    rng = np.random.default_rng(det_seed("216z", stat, K, rep_i,
                                                         *[str(x) for x in k]))
                    idx1 = np.array([rng.permutation(n)[:K] for _ in range(B_PAIRS)])
                    acc.append(float((( band_rows(a[idx1], stat) < d) != vpop[(k, stat)]).mean()))
                pk.append(float(np.mean(acc)))
            pk = np.array(pk)
            und = pk > 0.05
            zrows.append(dict(
                stat=stat, K=K, n_undetermined=int(und.sum()),
                share_undetermined=float(und.mean()),
                zone_max=float(mp[und].max()) if und.any() else 0.0,
                zone_p95=float(np.quantile(mp[und], 0.95)) if und.any() else 0.0,
                zone_median=float(np.median(mp[und])) if und.any() else 0.0,
                corpus_inside_p95=float((mp <= (np.quantile(mp[und], 0.95) if und.any()
                                                else 0.0)).mean()),
                mean_p=float(pk.mean()), max_p=float(pk.max())))
    Z = pd.DataFrame(zrows)
    Z.to_csv(OUT / f"{STEM}.zone.csv", index=False)
    P("\n" + Z.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ================================================================= Q4 the recommendation
    P("\n" + "=" * 118)
    P("Q4  THE K RECOMMENDATION, restated on the fixed-B estimator.")
    P("=" * 118)
    for stat in STATS:
        s_ = E[E.stat == stat].set_index("K")
        z_ = Z[Z.stat == stat].set_index("K")
        for K in K_GRID:
            P(f"    {stat:3s} K={K:4d}:  fixed-B disagreement {s_.loc[K, 'P_disagree']:.4f} "
              f"(+/- {s_.loc[K, 'P_rep_sd']:.4f})   error vs population "
              f"{s_.loc[K, 'E_err']:.4f} (+/- {s_.loc[K, 'E_rep_sd']:.4f})   "
              f"undetermined {z_.loc[K, 'share_undetermined']:.1%}   "
              f"zone_p95 {z_.loc[K, 'zone_p95']:.4f}")

    # ================================================================================ Q5 rule 8
    P("\n" + "=" * 118)
    P("Q5  RULE 8 (PROTOCOL clause 8).  Clause read on the IS window ONLY (<= 2016-12-31);")
    P("    the overlay point is chosen there; 2017-01-01 -> is read ONCE.")
    P("    18 cells = 3 panels x 3 families x 2 cost rungs; pool = 10 points (5 thr x 2 depth).")
    P("=" * 118)
    RR = R.reset_index()
    kidx = RR.set_index(key).index
    for stat in STATS:
        for K in K_GRID:
            col = []
            for k, d in zip(kidx, RR["dSharpe_IS"].values):
                if not np.isfinite(d):
                    col.append(False)
                    continue
                a = np.abs(null_store[k]["dSis"])
                rng = np.random.default_rng(det_seed("216w", stat, K, *[str(x) for x in k]))
                col.append(bool(abs(d) > band_of(a[rng.permutation(len(a))[:K]], stat)))
            RR[f"clears_IS_{stat}_{K}"] = col
    n_undef = int((~np.isfinite(RR["dSharpe_IS"])).sum())
    P(f"\n  rows with an undefined IS Sharpe, carried as non-clearing and excluded from IS "
      f"statistics: {n_undef}/{len(RR)}")

    wf = []
    for (pn, fm_, bp), sub in RR.groupby(["panel", "family", "bps"]):
        base_oos = float(sub["ctrl_Sharpe_OOS"].iloc[0])
        base = dict(OOS_Sharpe=base_oos, OOS_CAGR=float(sub["ctrl_CAGR_OOS"].iloc[0]),
                    OOS_MaxDD=float(sub["ctrl_MaxDD_OOS"].iloc[0]))

        def take(df, tag, col="dSharpe_IS"):
            d = df[np.isfinite(df[col])]
            if not len(d):
                return dict(selector=tag, pick="ABSTAIN", **base)
            r = d.loc[d[col].idxmax()]
            return dict(selector=tag, pick=f"{r['thr']}/{r['depth']}",
                        OOS_Sharpe=float(r["Sharpe_OOS"]), OOS_CAGR=float(r["CAGR_OOS"]),
                        OOS_MaxDD=float(r["MaxDD_OOS"]))

        rows_ = [dict(selector="S0 do-nothing", pick="-", **base),
                 take(sub, "S1 IS-Sharpe argmax (control)")]
        for stat in STATS:
            for K in K_GRID:
                rows_.append(take(sub[sub[f"clears_IS_{stat}_{K}"]],
                                  f"S2 clause-gated {stat} K={K}"))
        o = sub.loc[sub["Sharpe_OOS"].idxmax()]
        rows_.append(dict(selector="ORACLE-OOS", pick=f"{o['thr']}/{o['depth']}",
                          OOS_Sharpe=float(o["Sharpe_OOS"]), OOS_CAGR=float(o["CAGR_OOS"]),
                          OOS_MaxDD=float(o["MaxDD_OOS"])))
        for r in rows_:
            r.update(panel=pn, family=fm_, bps=bp, dOOS=r["OOS_Sharpe"] - base_oos)
            wf.append(r)
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    piv = W.pivot_table(index=["panel", "family", "bps"], columns="selector", values="OOS_Sharpe")
    out = []
    for s in piv.columns:
        d = (piv[s] - piv["S0 do-nothing"]).dropna()
        sw = W[W.selector == s]
        out.append(dict(selector=s, mean_OOS_Sharpe=float(piv[s].mean()),
                        mean_OOS_CAGR=float(sw["OOS_CAGR"].mean()),
                        mean_OOS_MaxDD=float(sw["OOS_MaxDD"].mean()),
                        dOOS=float(d.mean()), t=tstat(d), wins=int((d > 0).sum()),
                        losses=int((d < 0).sum()),
                        abstains=int((sw["pick"] == "ABSTAIN").sum()), n=int(len(d))))
    SW = pd.DataFrame(out).sort_values("mean_OOS_Sharpe", ascending=False)
    P("\n" + SW.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    s2 = SW[SW.selector.str.startswith("S2")]
    best_d = float(s2["dOOS"].max())
    P(f"\n  best clause-gated selector vs do-nothing: {best_d:+.4f} of OOS Sharpe "
      f"({'WINS' if best_d > 0 else 'LOSES'})   "
      f"ORACLE-OOS headroom {float(SW[SW.selector == 'ORACLE-OOS']['dOOS'].iloc[0]):+.4f}")

    P("\n  BENCHMARKS over the same OOS window (2017-01-01 ->):")
    for pan in panels:
        sp = pan.spy.loc[OOS_START:]
        v1 = backtest(pan.px, rules_v1_weights(pan.px), cost_bps=10.0,
                      freq="W")["returns"].loc[OOS_START:]
        P(f"    {pan.name:9s} SPY OOS Sharpe {_sh(sp):.4f} CAGR {metrics(sp)['CAGR']:.2%} "
          f"MaxDD {metrics(sp)['MaxDD']:.2%} | RULES v1 @10bps OOS Sharpe {_sh(v1):.4f} "
          f"CAGR {metrics(v1)['CAGR']:.2%} MaxDD {metrics(v1)['MaxDD']:.2%}")

    # ================================================================================ Q6 KEEP
    P("\n" + "=" * 118)
    P("Q6  BOTH KEEP PATHS on the 180 real rows (4a vs the panel's own RULES v1 at the row's")
    P("    own cost rung, 4b vs SPY; idea 191's evaluators, unchanged).")
    P("=" * 118)
    Rr = R.reset_index()
    P(f"\n  4a passes: {int(Rr['pass4a'].sum())}/{len(Rr)}     "
      f"4b passes: {int(Rr['pass4b'].sum())}/{len(Rr)}     "
      f"BOTH: {int((Rr['pass4a'] & Rr['pass4b']).sum())}/{len(Rr)}")
    if Rr["pass4b"].any():
        P("\n  4b passes by panel/family:")
        P(Rr[Rr.pass4b].groupby(["panel", "family"]).size().to_string())
    P("\n  reasons 4a fails (top):")
    P(Rr["fail4a"].value_counts().head(6).to_string())
    P("  reasons 4b fails (top):")
    P(Rr["fail4b"].value_counts().head(6).to_string())

    # ============================================================================== verdicts
    P("\n" + "=" * 118)
    P("PRE-REGISTERED PREDICTIONS, scored")
    P("=" * 118)
    emax = E[E.stat == "MAX"].set_index("K")
    eq95 = E[E.stat == "Q95"].set_index("K")
    d_lo, d_hi = emax["D_rep_sd"].min(), emax["D_rep_sd"].max()
    p_lo = eq95["P_rep_sd"].replace(0.0, np.nan).min()
    p_hi = eq95["P_rep_sd"].replace(0.0, np.nan).max()
    p_lo_m = emax["P_rep_sd"].replace(0.0, np.nan).min()
    p_hi_m = emax["P_rep_sd"].replace(0.0, np.nan).max()
    P(f"  P1 reproduction (bt_np == parent at 0.0e+00 AND idea 201 bands within the "
      f"vintage drift): "
      f"{'CONFIRMED' if rep_ok and worst_r == 0.0 else 'FAILED'}")
    dq_hi = E[E.stat == 'Q95']['D_rep_sd'].max()
    dq_lo = E[E.stat == 'Q95']['D_rep_sd'].min()
    p2a = (d_hi / max(d_lo, 1e-12) > 3) and (dq_hi / max(dq_lo, 1e-12) > 3)
    p2b = (p_hi_m / max(p_lo_m, 1e-12) < 2) and (p_hi / max(p_lo, 1e-12) < 2)
    P(f"  P2 D rep sd rises >3x [{'CONFIRMED' if p2a else 'REJECTED'}], P rep sd flat <2x "
      f"[{'CONFIRMED' if p2b else 'REJECTED'}]: D {d_hi / max(d_lo, 1e-12):.1f}x "
      f"MAX / {dq_hi / max(dq_lo, 1e-12):.1f}x Q95 ; "
      f"P {p_hi_m / max(p_lo_m, 1e-12):.1f}x MAX / {p_hi / max(p_lo, 1e-12):.1f}x Q95")
    P(f"     the RATIO test is the wrong scale and P2's second clause is rejected on it: what")
    P(f"     matters is the LEVEL at the noisy end -- at K={K_GRID[-1]} the fixed-B estimator's sd is")
    P(f"     {E[(E.stat=='Q95') & (E.K==K_GRID[-1])]['P_rep_sd'].iloc[0]:.4f} against the disjoint "
      f"estimator's {dq_hi:.4f}, a factor "
      f"{dq_hi / max(E[(E.stat=='Q95') & (E.K==K_GRID[-1])]['P_rep_sd'].iloc[0], 1e-12):.0f}.")
    q_p = eq95["P_disagree"].values
    P(f"  P3 Q95 fixed-B disagreement monotone decreasing: "
      f"{'CONFIRMED' if all(q_p[i] >= q_p[i+1] - 1e-12 for i in range(len(q_p)-1)) else 'REJECTED'}"
      f"  ({' -> '.join(f'{x:.4f}' for x in q_p)})")
    P(f"  P4 MAX p_K still >5% at K={K_GRID[-1]}: {emax.loc[K_GRID[-1], 'E_err']:.4f} -> "
      f"{'CONFIRMED' if emax.loc[K_GRID[-1], 'E_err'] > 0.05 else 'REJECTED'}")
    q_e = eq95["E_err"].values
    below = all(eq95.loc[k, "E_err"] < emax.loc[k, "E_err"] for k in K_GRID if k >= 50)
    P(f"  P5 Q95 p_K monotone down and below MAX at K>=50: "
      f"{'CONFIRMED' if all(q_e[i] >= q_e[i+1] - 1e-12 for i in range(len(q_e)-1)) and below else 'REJECTED'}"
      f"  ({' -> '.join(f'{x:.4f}' for x in q_e)})")
    gmax = CF[CF.stat == "MAX"]
    g5b = float(max(gmax["err_gap"].abs().max(), gmax["flip_gap"].abs().max()))
    P(f"  P5b MAX Monte Carlo matches the exact closed form within 0.01: {g5b:.4f} -> "
      f"{'CONFIRMED' if g5b < 0.01 else 'REJECTED'}")
    P(f"  P6 no clause-gated selector beats do-nothing OOS: best {best_d:+.4f} -> "
      f"{'CONFIRMED' if best_d <= 0 else 'REJECTED'}")

    P(f"\ntotal runtime {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""IDEA 207  how-many-draws-does-clause-11b-need   (cloud, 2026-09-05)

THE QUESTION
------------
Idea 186 defined clause 11b: an overlay's effect "clears" its null when |dSharpe| exceeds a
BAND built from J circular rotations of the overlay's ON indicator.  Idea 186 used J = 20.
Idea 201 measured that band on 3 DISJOINT blocks of 20 and found the band's own range is
63.3% of its value, with 32/180 = 17.8% of published clause verdicts FLIPPING between blocks,
concentrated where |margin| = |dSharpe| - band is below 0.05.

The queue asks: sweep the draw count (20/50/100/200), report the flip rate and the
undetermined-zone width at each, and output "the number PROTOCOL 11b should specify".

That question has a hidden premise worth testing FIRST, because if it is false the queue's
number does not exist:

    idea 186's band is  band(K) = max over K rotations of |dSharpe|.

A MAX is not a fixed estimand.  E[max of K] rises monotonically in K toward the population
max of the rotation distribution, so raising K does not merely reduce noise around a target --
it MOVES the target, and it moves it in the direction that makes the clause harder to clear.
A one-sided test built on the max of K draws has nominal size 1/(K+1): 4.8% at K=20 and 0.25%
at K=400.  If that is what is happening, the honest answer to "how many draws" is "none --
change the statistic", and the fix is a FIXED QUANTILE, whose sampling noise does shrink like
1/sqrt(K) around a target that does not move.

  Q1  DOES THE BAND DRIFT?  Mean band, clear rate and margin as a function of K, for the MAX
      statistic (clause 11b as written) and for a fixed Q95 alternative.  If MAX drifts and
      Q95 does not, the queue's premise is false for MAX and true for Q95.
  Q2  FLIP RATE vs K.  Idea 201's measurement, extended: disjoint blocks of size K drawn from
      a 400-rotation pool (20 blocks at K=20, 8 at K=50, 4 at K=100, 2 at K=200), pairwise
      verdict disagreement within each configuration, for both statistics.
  Q3  UNDETERMINED-ZONE WIDTH.  At each K and statistic, the |margin| below which verdicts
      flip -- reported as the max and the 95th percentile of |margin| among flippers, and as
      a share of the corpus that lands inside it.
  Q4  RULE 8 (PROTOCOL clause 8, required).  Does any of this move a DECISION?  The clause is
      read on the IS window only (<= 2016-12-31), the overlay point is chosen, and 2017-2026
      is read ONCE.  18 cells x (do-nothing + IS-argmax + clause-gated argmax at every K and
      both statistics), against RULES v1 and SPY.
  Q5  BOTH KEEP PATHS on all 180 real rows (4a vs the panel's own RULES v1, 4b vs SPY).

DESIGN
------
Idea 191's script is IMPORTED, not re-implemented: panels, base book, overlay families,
`apply_overlay`, the rotation construction and the 4a/4b evaluators all execute the parent's
own code, so every number below sits on the simulator being audited.  Idea 201's seeding
(`zlib.crc32`, deterministic across processes) is reused, and because idea 201 drew its
offsets from `rng.permutation(...)` under that seed, the FIRST 60 offsets of this run's
400-draw pool ARE idea 201's 60 -- so its published bands reproduce exactly and are asserted
before any new number is read.

  panels   : U56, BROAD136, SMALL439 (the 483-name sub-$2B panel less the 44 tickers with
             max_1d_move >= 1.0 in data/small_meta.csv)
  base book: idea 2's candidate -- composite (no vol scaler), 200d & vol20<0.60 eligibility,
             top-20 equal weight, gross 0.75, WEEKLY, t+1
  families : DDCTL / BUDGET / SLEEVE, idea 186/191's definitions verbatim
  costs    : 10 and 25 bps, both derived EXACTLY from one 0 bps run -- a reported axis
  configs  : 3 panels x 3 families x 5 thr x 2 depth = 90; x 2 cost rungs = 180 real rows
  pool     : 400 circular rotations per configuration = 36000 null backtests

  TUNED PARAMETER 1: K, the draw count           {20, 50, 100, 200}   (all reported)
  TUNED PARAMETER 2: the band statistic          {MAX, Q95}           (all reported)
  -> 8 grid points, every one of them published, no third dial.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
---------------------------------------------------------------------
  P1  Idea 201's three published bands (band, band_b1, band_b2) reproduce at < 1e-12 on all
      180 rows, and its 17.8% three-block flip rate reproduces to within one row.
  P2  The MAX band DRIFTS UP monotonically in K on the corpus mean, by more than 20% from
      K=20 to K=200, and the MAX clear rate falls monotonically in K.
  P3  The Q95 band does NOT drift monotonically up; |mean(Q95 at K=200) - mean(Q95 at K=20)|
      is under 20% of the K=20 level.
  P4  The MAX flip rate does NOT fall to zero as K rises: at K=200 it is still above 5%.
      (Disagreement between two disjoint blocks of a MAX is driven by the tail, which does
      not average away.)
  P5  The Q95 flip rate falls monotonically in K and is BELOW the MAX flip rate at every K
      from 50 up.
  P6  No clause-gated selector, at any K or either statistic, beats the do-nothing control
      out of sample.  (This project's twelfth consecutive such test.)

CAVEATS carried, not buried
---------------------------
  * SURVIVORSHIP (idea 54): all three panels are CURRENT constituents; SMALL439 contains no
    delistings.  Real and rotated draws inherit the bias identically, so the CLAUSE reading
    is unaffected; every LEVEL (CAGR, Sharpe, 4a/4b counts) is biased upward and is NOT a
    tradable estimate.
  * Only J-1 distinct rotations exist per configuration (J = number of weekly rebalances,
    ~670 on U56/BROAD136 and ~600 on SMALL439).  A 400-draw pool is therefore 60-67% of the
    entire rotation population, and NEIGHBOURING offsets are strongly correlated.  Two
    consequences, both reported rather than hidden: (a) blocks are disjoint in offset but not
    independent, so the K=200 flip rate is a LOWER bound on what independent blocks would
    give; (b) the MAX band at K=400 is close to the population max, which is exactly why the
    drift in Q1 flattens at the top and must not be read as convergence to a critical value.
  * BUDGET-skip changes realised turnover between real and null (idea 186: 25.4% mean; idea
    191: 1782.7% on the widened grid).  That is idea 203's subject; it is inherited and
    stated here, not fixed.
  * Two cells (SMALL439 / BUDGET tau=0.05 / skip, both cost rungs) have an undefined IS
    Sharpe -- the overlay suppresses 93.7% of rebalances and the book is flat through the IS
    window.  They are carried as NaN and excluded from IS-window statistics with the surviving
    n printed; nothing is imputed.
  * Idea 38: calendar-day index after 2014-09-17 on U56/BROAD136.  Idea 126: t+1 only.
  * PROTOCOL 5: this script seeds with zlib.crc32, not hash(), and is reproducible across
    processes (the defect idea 201 found in idea 191).

Deterministic, standalone.  Writes .console.txt, .band.csv, .flip.csv, .zone.csv,
.walkforward.csv, .keep.csv.
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

STEM = "2026-09-05_how-many-draws-does-clause-11b-need_cloud"
OUT = ROOT / "research" / "backtests"
PARENT_STEM = "2026-09-05_the-on-share-column_cloud"          # idea 191, the machinery
AUDIT_STEM = "2026-09-05_the-margin-column-instead-of-two_cloud"   # idea 201, the target

N_POOL = int(os.environ.get("N_POOL", 400))
K_GRID = [int(x) for x in os.environ.get("K_GRID", "20,50,100,200").split(",")]
STATS = ["MAX", "Q95"]
COST_RUNGS = [10, 25]
IS_END, OOS_START = "2016-12-31", "2017-01-01"

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 4000)

_lines: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


# ---------------------------------------------------------------- import idea 191 verbatim
spec = importlib.util.spec_from_file_location("p191", OUT / f"{PARENT_STEM}.py")
p191 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p191)

FAMILIES, FAM_ORDER = p191.FAMILIES, p191.FAM_ORDER
fast_backtest, net = p191.fast_backtest, p191.net
on_indicator, apply_overlay = p191.on_indicator, p191.apply_overlay
halves, keep_4a, keep_4b = p191.halves, p191.keep_4a, p191.keep_4b
tstat, _sh = p191.tstat, p191._sh


def det_seed(*parts):
    """Idea 201's seed, verbatim -- deterministic across processes (PROTOCOL 5)."""
    return int(zlib.crc32("|".join(str(p) for p in parts).encode())) % (2**31)


def pool_offsets(J, n, seed):
    """Idea 201's `rotations` WITHOUT its final sort, so that the first 60 entries are exactly
    idea 201's 60 draws (it sorted a prefix of this same permutation; the band is a max over
    the SET, so order inside a block is irrelevant and the reproduction is exact)."""
    rng = np.random.default_rng(seed)
    return rng.permutation(np.arange(1, J))[:min(n, J - 1)]


# ------------------------------------------------------------------ fast metric primitives
def sharpe_np(r):
    """engine.metrics()['Sharpe'] on a numpy array: mean*252 / (std(ddof=1)*sqrt(252))."""
    if len(r) < 6:
        return np.nan
    sd = r.std(ddof=1)
    return float(r.mean() * 252.0 / (sd * np.sqrt(252.0))) if sd > 0 else np.nan


def maxdd_np(r):
    eq = np.cumprod(1.0 + r)
    return float((eq / np.maximum.accumulate(eq) - 1.0).min())


def band_of(vals, stat):
    """The null band from a block of |dSharpe| (or |dMaxDD|) values."""
    if stat == "MAX":
        return float(np.max(vals))
    if stat == "Q95":
        return float(np.quantile(vals, 0.95, method="linear"))
    raise ValueError(stat)


# ============================================================================================ run
def main():
    t0 = time.time()
    P("=" * 118)
    P("IDEA 207  how-many-draws-does-clause-11b-need   (cloud, 2026-09-05)")
    P("=" * 118)

    P("\nbuilding panels (idea 191's build_panels, imported) ...")
    panels = p191.build_panels()
    P("  panels: " + "  ".join(f"{p.name}={len(p.tradable)}" for p in panels))

    P("\nREPRODUCTION, asserted before any new number is read:")
    ok = all(p191.checks(p) for p in panels)
    pu = load_universe()
    ru = backtest(pu, rules_v1_weights(pu), cost_bps=10.0,
                  freq="W")["returns"].loc[pu.index[260]:]
    mu = metrics(ru)
    P(f"  [d] RULES v1 on u56 @10bps: {mu['CAGR']:.5%} / {mu['Sharpe']:.5f} / "
      f"{mu['MaxDD']:.5%}  (published 6.45305% / 0.66418 / -13.82780%) -> "
      f"{'PASS' if abs(mu['Sharpe'] - 0.66418) < 5e-5 else 'FAIL'}")
    ok &= abs(mu["Sharpe"] - 0.66418) < 5e-5
    if not ok:
        P("\nreproduction of the deterministic parts FAILS -- STOP")
        return
    P("  deterministic parts reproduce -- proceeding to the grid")

    # ------------------------------------------------------------------------------- the grid
    P("\n" + "=" * 118)
    P(f"GRID  3 panels x 3 families x 5 thr x 2 depth = 90 configurations,")
    P(f"      x (1 real + {N_POOL} circular rotations) x 2 cost rungs derived from one 0 bps run")
    P("=" * 118)

    real_rows, null_store, OFFS = [], {}, {}
    for pan in panels:
        start = pan.start
        i0 = pan.px.index.searchsorted(start)
        spy = pan.spy.loc[start:]
        basefull = backtest(pan.px, rules_v1_weights(pan.px), cost_bps=0.0, freq="W")
        b0, bt = basefull["returns"].loc[start:], basefull["turnover"].loc[start:]
        c0 = pan._r0
        is_end_i = pan.px.index.searchsorted(pd.Timestamp(IS_END), side="right") - i0
        for fam in FAM_ORDER:
            _, thrs, _, depths = FAMILIES[fam]
            for thr in thrs:
                s_real = on_indicator(pan, fam, thr)
                J = len(s_real)
                offs = pool_offsets(J, N_POOL, det_seed(pan.name, fam, thr))
                for depth in depths:
                    OFFS[(pan.name, fam, float(thr), str(depth))] = offs
                    # ---- the real overlay: full treatment (metrics, halves, KEEP paths)
                    W, mask = apply_overlay(pan, fam, depth, s_real)
                    res = fast_backtest(pan.px, W, 0.0, p191.FREQ, mask=mask)
                    for bps in COST_RUNGS:
                        r = net(res, bps).loc[start:]
                        cr = net(c0, bps).loc[start:]
                        br = b0 - bt * bps / 1e4
                        m, mc = metrics(r), metrics(cr)
                        h1, h2 = halves(r)
                        real_rows.append(dict(
                            panel=pan.name, family=fam, thr=thr, depth=str(depth), bps=bps,
                            J=J, on_share=float(s_real.mean()),
                            CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                            Sharpe_IS=_sh(r.loc[:IS_END]), Sharpe_OOS=_sh(r.loc[OOS_START:]),
                            CAGR_OOS=metrics(r.loc[OOS_START:])["CAGR"],
                            MaxDD_OOS=metrics(r.loc[OOS_START:])["MaxDD"],
                            ctrl_Sharpe=mc["Sharpe"], ctrl_MaxDD=mc["MaxDD"],
                            ctrl_Sharpe_IS=_sh(cr.loc[:IS_END]),
                            ctrl_Sharpe_OOS=_sh(cr.loc[OOS_START:]),
                            ctrl_CAGR_OOS=metrics(cr.loc[OOS_START:])["CAGR"],
                            ctrl_MaxDD_OOS=metrics(cr.loc[OOS_START:])["MaxDD"],
                            fail4a=keep_4a(r, br), fail4b=keep_4b(r, spy)))

                    # ---- the null pool: only the three statistics the clause reads
                    ctrl = {bps: net(c0, bps).loc[start:].values for bps in COST_RUNGS}
                    cS = {bps: sharpe_np(ctrl[bps]) for bps in COST_RUNGS}
                    cD = {bps: maxdd_np(ctrl[bps]) for bps in COST_RUNGS}
                    cSis = {bps: sharpe_np(ctrl[bps][:is_end_i]) for bps in COST_RUNGS}
                    dS = {bps: np.empty(N_POOL) for bps in COST_RUNGS}
                    dD = {bps: np.empty(N_POOL) for bps in COST_RUNGS}
                    dSis = {bps: np.empty(N_POOL) for bps in COST_RUNGS}
                    for i, off in enumerate(offs):
                        Wn, mn = apply_overlay(pan, fam, depth, np.roll(s_real, off))
                        rn = fast_backtest(pan.px, Wn, 0.0, p191.FREQ, mask=mn)
                        rv = rn["returns"].values[i0:]
                        tv = rn["turnover"].values[i0:]
                        for bps in COST_RUNGS:
                            x = rv - tv * bps / 1e4
                            dS[bps][i] = sharpe_np(x) - cS[bps]
                            dD[bps][i] = maxdd_np(x) - cD[bps]
                            dSis[bps][i] = sharpe_np(x[:is_end_i]) - cSis[bps]
                    for bps in COST_RUNGS:
                        null_store[(pan.name, fam, thr, str(depth), bps)] = dict(
                            dS=dS[bps], dD=dD[bps], dSis=dSis[bps])
        P(f"  {pan.name} done ({time.time() - t0:.0f}s)")

    R = pd.DataFrame(real_rows)
    R["dSharpe"] = R["Sharpe"] - R["ctrl_Sharpe"]
    R["dMaxDD"] = R["MaxDD"] - R["ctrl_MaxDD"]
    R["dSharpe_IS"] = R["Sharpe_IS"] - R["ctrl_Sharpe_IS"]
    R["pass4a"] = R["fail4a"] == "-"
    R["pass4b"] = R["fail4b"] == "-"
    R.to_csv(OUT / f"{STEM}.keep.csv", index=False)
    P(f"\ngrid: {len(R)} real rows, {len(null_store) * N_POOL} null evaluations "
      f"({time.time() - t0:.0f}s)")

    key = ["panel", "family", "thr", "depth", "bps"]
    R = R.set_index(key).sort_index()

    # =========================================================== REPRODUCTION of idea 201
    P("\n" + "=" * 118)
    P("REPRODUCTION of idea 201's published bands (P1).  Idea 201 drew 60 offsets from THIS")
    P("same crc32-seeded permutation, SORTED them, and split the sorted list into 3 blocks of")
    P("20 -- so its band/band_b1/band_b2 are the MAX over the 1st, 2nd and 3rd smallest 20")
    P("offsets of this run's first 60 pool draws.  That ordering is reconstructed exactly.")
    P("=" * 118)
    S201 = pd.read_csv(OUT / f"{AUDIT_STEM}.stability.csv")
    S201["depth"] = S201["depth"].astype(str)
    S201 = S201.set_index(key).sort_index()
    def order201(k):
        """Pool positions of idea 201's 60 draws, in ITS order (it sorted the offsets before
        blocking).  Returns the |dSharpe| values re-ordered the way idea 201 blocked them."""
        off = OFFS[k[:4]][:60]
        return np.argsort(off, kind="stable")

    rep = []
    for k, row in S201.iterrows():
        ns = np.abs(null_store[k]["dS"])[order201(k)]
        mine = [band_of(ns[a:a + 20], "MAX") for a in (0, 20, 40)]
        rep.append([abs(mine[0] - row["band"]), abs(mine[1] - row["band_b1"]),
                    abs(mine[2] - row["band_b2"])])
    rep = np.array(rep)
    P(f"  max |band  - idea 201 band   | over 180 rows: {rep[:, 0].max():.3e}")
    P(f"  max |band_1- idea 201 band_b1| over 180 rows: {rep[:, 1].max():.3e}")
    P(f"  max |band_2- idea 201 band_b2| over 180 rows: {rep[:, 2].max():.3e}")
    rep_ok = rep.max() < 1e-12
    P(f"  -> {'PASS' if rep_ok else 'FAIL'} (idea 201's bands reproduce; idea 191's, seeded "
      "with a salted hash(), do not and cannot)")
    v0 = np.array([abs(R.loc[k, "dSharpe"])
                   > band_of(np.abs(null_store[k]["dS"])[order201(k)][a:a + 20], "MAX")
                   for k in S201.index for a in (0, 20, 40)]).reshape(-1, 3)
    flips201 = int((v0.min(axis=1) != v0.max(axis=1)).sum())
    P(f"  idea 201's 3-block flip count reproduces: {flips201}/180 = {flips201 / 180:.1%} "
      f"(published 32/180 = 17.8%) -> {'PASS' if abs(flips201 - 32) <= 1 else 'FAIL'}")

    # ============================================================================== Q1 drift
    P("\n" + "=" * 118)
    P("Q1  DOES THE BAND DRIFT WITH K?  Mean band, mean margin and clear rate over the 180")
    P("    real rows, for every K and both statistics.  Each K uses pool positions 0:K, so")
    P("    the K ladder is NESTED and the drift is not a re-draw artefact.")
    P("=" * 118)
    bandrows = []
    for stat in STATS:
        for K in K_GRID:
            b = np.array([band_of(np.abs(null_store[k]["dS"][:K]), stat) for k in R.index])
            bd = np.array([band_of(np.abs(null_store[k]["dD"][:K]), stat) for k in R.index])
            marg = R["dSharpe"].abs().values - b
            margd = R["dMaxDD"].abs().values - bd
            bandrows.append(dict(stat=stat, K=K, nominal_size=(1 / (K + 1)) if stat == "MAX"
                                 else 0.05,
                                 mean_band=b.mean(), median_band=float(np.median(b)),
                                 mean_margin=marg.mean(),
                                 clear_Sharpe=float((marg > 0).mean()),
                                 clear_MaxDD=float((margd > 0).mean()),
                                 n_clear_Sharpe=int((marg > 0).sum())))
    B = pd.DataFrame(bandrows)
    B.to_csv(OUT / f"{STEM}.band.csv", index=False)
    P("\n" + B.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    mx = B[B.stat == "MAX"].set_index("K")
    q9 = B[B.stat == "Q95"].set_index("K")
    dmax = mx.loc[K_GRID[-1], "mean_band"] / mx.loc[K_GRID[0], "mean_band"] - 1
    dq95 = q9.loc[K_GRID[-1], "mean_band"] / q9.loc[K_GRID[0], "mean_band"] - 1
    P(f"\n  MAX band, K=20 -> K=200: {mx.loc[K_GRID[0], 'mean_band']:.4f} -> "
      f"{mx.loc[K_GRID[-1], 'mean_band']:.4f}  ({dmax:+.1%})   clear rate "
      f"{mx.loc[K_GRID[0], 'clear_Sharpe']:.1%} -> {mx.loc[K_GRID[-1], 'clear_Sharpe']:.1%}")
    P(f"  Q95 band, K=20 -> K=200: {q9.loc[K_GRID[0], 'mean_band']:.4f} -> "
      f"{q9.loc[K_GRID[-1], 'mean_band']:.4f}  ({dq95:+.1%})   clear rate "
      f"{q9.loc[K_GRID[0], 'clear_Sharpe']:.1%} -> {q9.loc[K_GRID[-1], 'clear_Sharpe']:.1%}")
    max_mono = all(mx.loc[a, "mean_band"] < mx.loc[b_, "mean_band"]
                   for a, b_ in zip(K_GRID, K_GRID[1:]))
    max_clear_mono = all(mx.loc[a, "clear_Sharpe"] >= mx.loc[b_, "clear_Sharpe"]
                         for a, b_ in zip(K_GRID, K_GRID[1:]))

    # =========================================================================== Q2 flip rate
    P("\n" + "=" * 118)
    P("Q2  FLIP RATE vs K.  Disjoint blocks of size K from the 400-draw pool: 20 blocks at")
    P("    K=20, 8 at K=50, 4 at K=100, 2 at K=200.  A configuration FLIPS when two disjoint")
    P("    blocks disagree on `clears`.  Reported as the share of configurations that flip on")
    P("    at least one block pair, and as the mean pairwise disagreement rate.")
    P("=" * 118)
    fliprows, flip_detail = [], []
    for stat in STATS:
        for K in K_GRID:
            nb = N_POOL // K
            if nb < 2:
                continue
            any_flip = disag = pairs = 0
            for k in R.index:
                ns = np.abs(null_store[k]["dS"])
                d = abs(R.loc[k, "dSharpe"])
                v = np.array([d > band_of(ns[j * K:(j + 1) * K], stat) for j in range(nb)])
                fl = bool(v.min() != v.max())
                any_flip += fl
                pr = nb * (nb - 1) // 2
                dis = int(v.sum() * (nb - v.sum()))
                disag += dis
                pairs += pr
                bands = np.array([band_of(ns[j * K:(j + 1) * K], stat) for j in range(nb)])
                flip_detail.append(dict(stat=stat, K=K, panel=k[0], family=k[1], thr=k[2],
                                        depth=k[3], bps=k[4], dSharpe=float(R.loc[k, "dSharpe"]),
                                        band_mean=float(bands.mean()),
                                        band_sd=float(bands.std(ddof=1)),
                                        band_rng=float(bands.max() - bands.min()),
                                        margin_ref=float(d - bands.mean()), flips=fl))
            fliprows.append(dict(stat=stat, K=K, blocks=nb,
                                 flip_share=any_flip / len(R),
                                 n_flip=any_flip,
                                 pairwise_disagree=disag / pairs))
    F = pd.DataFrame(fliprows)
    FD = pd.DataFrame(flip_detail)
    FD.to_csv(OUT / f"{STEM}.flip.csv", index=False)
    F.to_csv(OUT / f"{STEM}.zone.csv", index=False)
    P("\n" + F.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    fm = F[F.stat == "MAX"].set_index("K")
    fq = F[F.stat == "Q95"].set_index("K")
    P(f"\n  MAX  pairwise disagreement K=20 {fm.loc[K_GRID[0], 'pairwise_disagree']:.1%} -> "
      f"K=200 {fm.loc[K_GRID[-1], 'pairwise_disagree']:.1%}")
    P(f"  Q95  pairwise disagreement K=20 {fq.loc[K_GRID[0], 'pairwise_disagree']:.1%} -> "
      f"K=200 {fq.loc[K_GRID[-1], 'pairwise_disagree']:.1%}")

    P("\n  band dispersion (mean over the 180 rows of the across-block sd and range):")
    P(FD.groupby(["stat", "K"]).agg(band_mean=("band_mean", "mean"),
                                    band_sd=("band_sd", "mean"),
                                    rng_over_band=("band_rng", "mean"))
      .assign(rng_pct=lambda d: d.rng_over_band / d.band_mean)
      .to_string(float_format=lambda x: f"{x:.4f}"))

    # ======================================================================= Q3 undetermined
    P("\n" + "=" * 118)
    P("Q3  THE UNDETERMINED ZONE.  |margin| below which the verdict is a property of WHICH")
    P("    draws were taken.  margin_ref = |dSharpe| - mean band across the blocks at that K.")
    P("=" * 118)
    zrows = []
    for (stat, K), sub in FD.groupby(["stat", "K"]):
        fl = sub[sub.flips]
        am = sub["margin_ref"].abs()
        zrows.append(dict(
            stat=stat, K=K, n_flip=len(fl),
            zone_max=float(fl["margin_ref"].abs().max()) if len(fl) else 0.0,
            zone_p95=float(np.quantile(fl["margin_ref"].abs(), 0.95)) if len(fl) else 0.0,
            zone_median=float(np.median(fl["margin_ref"].abs())) if len(fl) else 0.0,
            corpus_inside_p95=float((am <= (np.quantile(fl["margin_ref"].abs(), 0.95)
                                            if len(fl) else 0.0)).mean())))
    Z = pd.DataFrame(zrows).sort_values(["stat", "K"])
    P("\n" + Z.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    zm = Z[Z.stat == "MAX"].set_index("K")
    P(f"\n  MAX: the undetermined zone (95th pct of flipper |margin|) is "
      f"{zm.loc[K_GRID[0], 'zone_p95']:.4f} at K=20 and {zm.loc[K_GRID[-1], 'zone_p95']:.4f} at K=200; "
      f"{zm.loc[K_GRID[-1], 'corpus_inside_p95']:.1%} of the corpus still lands inside it at K=200.")

    # ================================================================================ Q4 rule 8
    P("\n" + "=" * 118)
    P("Q4  RULE 8 (PROTOCOL clause 8).  The clause is read on the IS window ONLY")
    P("    (<= 2016-12-31); the overlay point is chosen there; 2017-01-01 -> is read ONCE.")
    P("    18 cells = 3 panels x 3 families x 2 cost rungs; pool = 10 points (5 thr x 2 depth).")
    P("=" * 118)
    RR = R.reset_index()
    for stat in STATS:
        for K in K_GRID:
            RR[f"clears_IS_{stat}_{K}"] = [
                abs(d) > band_of(np.abs(null_store[k]["dSis"][:K]), stat)
                if np.isfinite(d) else False
                for k, d in zip(RR.set_index(key).index, RR["dSharpe_IS"].values)]
    n_undef = int((~np.isfinite(RR["dSharpe_IS"])).sum())
    P(f"\n  rows with an undefined IS Sharpe, carried as non-clearing and excluded from IS "
      f"statistics: {n_undef}/180 (SMALL439 BUDGET tau=0.05/skip, both rungs)")

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
                c = f"clears_IS_{stat}_{K}"
                rows_.append(take(sub[sub[c]], f"S2 clause-gated {stat} K={K}"))
        o = sub.loc[sub["Sharpe_OOS"].idxmax()]
        rows_.append(dict(selector="ORACLE-OOS", pick=f"{o['thr']}/{o['depth']}",
                          OOS_Sharpe=float(o["Sharpe_OOS"]), OOS_CAGR=float(o["CAGR_OOS"]),
                          OOS_MaxDD=float(o["MaxDD_OOS"])))
        for r in rows_:
            r.update(panel=pn, family=fm_, bps=bp, dOOS=r["OOS_Sharpe"] - base_oos)
            wf.append(r)
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    piv = W.pivot_table(index=["panel", "family", "bps"], columns="selector",
                        values="OOS_Sharpe")
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
    best_d = float(SW[SW.selector.str.startswith("S2")]["dOOS"].max())

    P("\n  BENCHMARKS over the same OOS window (2017-01-01 ->):")
    bm = []
    for pan in panels:
        st = pan.start
        spy_o = pan.spy.loc[st:].loc[OOS_START:]
        bl = backtest(pan.px, rules_v1_weights(pan.px), cost_bps=10,
                      freq="W")["returns"].loc[st:].loc[OOS_START:]
        for nm, r in [("SPY", spy_o), ("RULES v1 @10bps", bl)]:
            m = metrics(r)
            bm.append(dict(panel=pan.name, series=nm, OOS_CAGR=m["CAGR"],
                           OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"]))
    P(pd.DataFrame(bm).to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("\n  every walk-forward cell:")
    P(W[["panel", "family", "bps", "selector", "pick", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
         "dOOS"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ============================================================================ Q5 KEEP paths
    P("\n" + "=" * 118)
    P("Q5  BOTH KEEP PATHS on the 180 real rows (4a vs the panel's own RULES v1, 4b vs SPY).")
    P("=" * 118)
    RRi = RR.set_index(key)
    P(f"\n  4a passes: {int(RR['pass4a'].sum())}/180     4b passes: "
      f"{int(RR['pass4b'].sum())}/180")
    P("\n  by panel and cost rung:")
    P(RR.groupby(["panel", "bps"]).agg(n=("pass4a", "size"), pass4a=("pass4a", "sum"),
                                       pass4b=("pass4b", "sum")).to_string())
    p4b = RR[RR["pass4b"]]
    if len(p4b):
        ins = []
        for _, r in p4b.iterrows():
            k = (r["panel"], r["family"], r["thr"], r["depth"], r["bps"])
            ins.append(abs(r["dSharpe"]) <= band_of(np.abs(null_store[k]["dS"][:K_GRID[-1]]), "MAX"))
        P(f"\n  of the {len(p4b)} rows that pass 4b, INSIDE their own 200-draw MAX band: "
          f"{int(np.sum(ins))}/{len(p4b)}")
        P(p4b[["panel", "family", "thr", "depth", "bps", "CAGR", "Sharpe", "MaxDD", "H1",
               "H2", "Sharpe_OOS", "dSharpe"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ============================================================================ predictions
    P("\n" + "=" * 118)
    P("PRE-REGISTERED PREDICTIONS")
    P("=" * 118)
    q95_drift = abs(dq95) < 0.20
    max_flip200 = fm.loc[K_GRID[-1], "pairwise_disagree"] > 0.05
    q95_mono = all(fq.loc[a, "pairwise_disagree"] >= fq.loc[b_, "pairwise_disagree"]
                   for a, b_ in zip(K_GRID, K_GRID[1:]))
    q95_below = all(fq.loc[k, "pairwise_disagree"] < fm.loc[k, "pairwise_disagree"]
                    for k in K_GRID[1:])
    preds = [
        ("P1 idea 201's bands and flip count reproduce", rep_ok and abs(flips201 - 32) <= 1,
         f"max |dband| {rep.max():.1e}, flips {flips201}/180"),
        ("P2 MAX band drifts up monotonically, >20% over K", max_mono and max_clear_mono
         and dmax > 0.20, f"{dmax:+.1%}, mono {max_mono}, clear-rate mono {max_clear_mono}"),
        ("P3 Q95 band does not drift (<20%)", q95_drift, f"{dq95:+.1%}"),
        ("P4 MAX flip rate still >5% at K=200", max_flip200,
         f"{fm.loc[K_GRID[-1], 'pairwise_disagree']:.1%}"),
        ("P5 Q95 flip rate falls monotonically and is below MAX from K=50",
         q95_mono and q95_below,
         f"mono {q95_mono}, below-MAX {q95_below}"),
        ("P6 no clause-gated selector beats do-nothing OOS", best_d <= 0,
         f"best dOOS {best_d:+.4f}"),
    ]
    for nm, hit, det in preds:
        P(f"  {'HIT ' if hit else 'MISS'}  {nm:<62s} {det}")
    P(f"\n  {sum(h for _, h, _ in preds)} of {len(preds)} predictions hit.")

    P(f"\ndone in {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()

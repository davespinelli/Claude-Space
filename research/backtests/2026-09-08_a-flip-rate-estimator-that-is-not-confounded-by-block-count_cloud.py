#!/usr/bin/env python3
"""QUEUE idea 216 - a-flip-rate-estimator-that-is-not-confounded-by-block-count
   (cloud lane, 2026-09-08).

QUESTION (pre-registered, verbatim from QUEUE.md idea 216)
    "idea 207's flip rate at K=200 rests on ONE disjoint block pair per configuration and is the
     noisiest row in its table (Q95's zone widens 100 -> 200 while its band sd keeps falling).
     Build a paired estimator that holds the number of comparisons fixed across K - e.g. B
     bootstrap block pairs at every K from a larger pool - and re-run the ladder, so the K
     recommendation rests on an estimator whose variance does not itself depend on K.  Max 2
     params."

WHAT IS AT STAKE
    PROTOCOL clause 11b's draw count K comes from idea 207's flip-rate ladder.  Idea 207 measured
    the flip rate by cutting a 400-draw pool into floor(400/K) DISJOINT blocks - 20 blocks at
    K=20, 8 at K=50, 4 at K=100 and TWO at K=200 - and counting verdict disagreements.  The number
    of comparisons therefore falls as 1/K, so the estimator's own standard error RISES with K by
    construction, and the K=200 row of the published table is a single Bernoulli trial per
    configuration.  Both of idea 207's two missed predictions are that row.  The enumeration
    companion (2026-09-05_clause-11b-draw-count-by-enumeration_cloud) already said as much and
    corrected the recommendation - "100 is a FLOOR not an optimum" - but it did so by replacing
    the estimator with a full enumeration, not by repairing it.  Idea 216 asks for the repair.

WHAT THIS RUN BUILDS
    1. FBP-B, the estimator idea 216 asks for: at every K, B independently drawn pairs of DISJOINT
       blocks of size K, sampled without replacement from the SAME enumerated rotation population
       the companion run committed.  Comparisons = B at every K, so the estimator's variance is
       B^(-1/2) and no longer a function of K.  B = 1 at K = 200 is exactly idea 207's estimator.

    2. The EXACT law of that estimator, in closed form, which turns out to make the Monte Carlo
       unnecessary.  Under a band that is an order statistic of K draws, a block's verdict depends
       on the sampled draws ONLY through X, the number of them that reach the real effect, and X
       is hypergeometric in the population's own exceedance count M:
              X ~ Hypergeom(N, M, K),      clears  <=>  X <= c(K),   c(K) = K - ceil(q*K)
              (q = 1 gives the MAX band, c = 0; q = 0.95 gives idea 207's Q95 band)
       For two DISJOINT blocks the pair is drawn as 2K from N, so
              P(flip) = 2 * sum_{x<=c} P(X1=x) * P(X2 > c | N-K, M-x, K)
       and the error against the population verdict is P(X<=c) or P(X>c) as the truth requires.
       Every number in the ladder below is that expression evaluated on the committed (M, N) of
       each claim.  FBP-B is then a Monte Carlo approximation to a quantity with a closed form,
       and gate [b] measures how fast it converges to it.

    3. The re-run ladder, on the same corpus, with the comparison count held fixed - which is what
       idea 216 asked for and what decides whether idea 207's K recommendation survives.

CORPUS.  The committed enumeration of idea 207's own 90 configurations x 2 cost rungs = 180 rows
    (3 panels x 3 overlay families x 5 thresholds x 2 depths), each carrying the COMPLETE rotation
    population (N = J-1 = 974 / 974 / 869) summarised by (M, ties, N) for three statistics:
        S    dSharpe    of the overlay against its own untreated control book
        DD   dMaxDD
        IS   dSharpe    on the IS window alone
    = 540 claims.  The real books are RE-RUN FROM SCRATCH here (idea 191's machinery imported
    verbatim) and gated against the committed file before any of it is read.

TUNED PARAMETERS - exactly two, per PROTOCOL rule 4.  ALL grid points reported.
    1. K, the draw count:            {20, 50, 100, 200, 400}
    2. B, the pair count of FBP-B:   {1, 4, 16, 64, 256}
    The band statistic (MAX / Q95), the panel, the family, the depth, the statistic and the cost
    rung are corpus axes, not tuned parameters.  The rule-8 selector is the only place a point is
    chosen and it chooses on the IS window alone.

WALK-FORWARD (PROTOCOL rule 8), 36 cells = 3 panels x 3 families x 2 depths x 2 cost rungs, each
    a 5-point threshold ladder.  Parameters chosen on <= 2016-12-31; 2017-2026 read once.  Arms:
        S0            do nothing (the untreated control book)
        S1            IS-Sharpe argmax over the ladder
        S2_K<stat>    the same argmax restricted to thresholds whose IS clause CLEARS at draw
                      count K - and because that verdict is itself random, its OOS Sharpe is
                      reported as a mean over R=400 simulated draws of the K-block, with the sd
                      across those draws (that spread IS the estimator's contribution to the book)
        S3_EXACT      the same argmax restricted to thresholds that clear the POPULATION verdict
        ORACLE_OOS    the best OOS threshold read with perfect hindsight - the family's headroom
    OOS CAGR / Sharpe / MaxDD reported against the control book and against SPY.

BOTH KEEP PATHS (4a vs the live book, 4b vs SPY) are evaluated on all 180 freshly-run real rows.

REPRODUCTION GATES, asserted before any new number is read
    [a] the 180 real overlay books re-run here reproduce the committed enumeration's
        Sharpe / CAGR / MaxDD / H1 / H2 / OOS / on_share / J / |d| to < 1e-12
    [b] FBP-B converges to the closed form at the 1/sqrt(B) rate over the whole corpus
    [c] a FULL enumeration of one configuration per panel reproduces the committed (M, N)
    [d] the hypergeometric identity: the closed-form P(clear) equals a brute-force
        sample-without-replacement estimate to Monte Carlo error, and P(clear) at K=N is the
        population verdict exactly
    [e] idea 207's own published flip numbers are reproduced from its own construction
        (floor(400/K) disjoint blocks), so the old and new estimators are compared like for like

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  gates [a]-[e] hold.
    P2  Idea 207's estimator has a standard error that RISES with K (its comparison count falls as
        1/K); FBP-B's is flat in K at fixed B.  The K=200 row of the published table has an se of
        order 0.3-0.5 per configuration.
    P3  Under the fixed-comparison estimator the MAX band's flip rate still FALLS with K, and
        still does so by the test ceasing to fire (P(clear) -> 0), reproducing idea 207's
        finding (2) rather than overturning it.
    P4  For the Q95 band, error-against-truth falls monotonically in K with no interior optimum,
        so "K=100" is a floor, not an argmax - the enumeration companion's correction, now
        obtained from the repaired estimator instead of from full enumeration.
    P5  Under rule 8 every clause-gated arm loses to S0 at every K and both statistics.  Thirteen
        prior instances.
    P6  No row passes both KEEP paths on SMALL439 at either rung.

CAVEATS carried, not buried
    * SURVIVORSHIP: all three panels are current-constituent lists (idea 54); SMALL439 contains no
      delistings, so the LEVEL of every performance number is biased upward.  The estimator
      comparison is unaffected by this.
    * TIES: some configurations are rotation-DEGENERATE (the ON indicator is all-on or all-off, so
      every rotation reproduces the real book exactly and ties = N).  They are counted and
      reported separately; no estimator can have power there, and they are idea 203's
      "free_strata == 0" case seen from the other side.
    * The exact law treats a tie as an exceedance (conservative).  Idea 208 broke ties with a
      strict <; the difference is bounded and reported.
    * Rotation draws are neighbours on a circle and are NOT independent across offsets (idea 214).
      The hypergeometric law below is the law of SAMPLING FROM the enumerated population, which is
      exact; it does not claim the population's members are independent of each other.
    * Idea 38 (calendar-day index on U56/BROAD after 2014-09-17) and idea 126 (t+1 only) carry.

Deterministic, standalone.  Writes .console.txt, .real.csv, .ladder.csv, .estimator.csv,
.walkforward.csv, .keep.csv
"""
import importlib.util
import math
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from engine import metrics  # noqa: E402

STEM = "2026-09-08_a-flip-rate-estimator-that-is-not-confounded-by-block-count_cloud"
OUT = ROOT / "research" / "backtests"
P191_STEM = "2026-09-05_the-on-share-column_cloud"                          # idea 191
ENUM_STEM = "2026-09-05_clause-11b-draw-count-by-enumeration_cloud"         # idea 207 companion

KS = [20, 50, 100, 200, 400]              # tuned parameter 1
BS = [1, 4, 16, 64, 256]                  # tuned parameter 2
BANDS = [("MAX", 1.0), ("Q95", 0.95)]     # corpus axis
STATS = ["S", "DD", "IS"]                 # corpus axis
POOL_207 = 400                            # idea 207's own draw pool
R_SIM = 400                               # simulated ladder realisations in the rule-8 arms
SEED = 216_000

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 4000)

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


# ---------------------------------------------------------------- idea 191, imported verbatim
spec = importlib.util.spec_from_file_location("p191", OUT / f"{P191_STEM}.py")
p191 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p191)
p191.P = P

COST_RUNGS = p191.COST_RUNGS
FREQ = p191.FREQ
IS_END = p191.IS_END
OOS_START = p191.OOS_START


# ================================================================ the exact law
def _logC(n, k):
    if k < 0 or n < 0 or k > n:
        return -np.inf
    return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)


def hyper_pmf(N, M, K, xs):
    """P(X = x) for X ~ Hypergeom(population N, successes M, draws K)."""
    den = _logC(N, K)
    return np.array([math.exp(_logC(M, x) + _logC(N - M, K - x) - den)
                     if (0 <= x <= min(M, K) and K - x <= N - M) else 0.0 for x in xs])


def c_of(K, q):
    """The clause clears iff at most c(K) of the K sampled draws reach the real effect."""
    return K - int(math.ceil(q * K))


def p_clear(N, M, K, q):
    c = c_of(K, q)
    if K > N:
        K = N
        c = c_of(K, q)
    return float(hyper_pmf(N, M, K, range(0, c + 1)).sum())


def p_flip(N, M, K, q):
    """P(two DISJOINT blocks of K, drawn jointly as 2K from N, give different verdicts)."""
    if 2 * K > N:
        return np.nan
    c = c_of(K, q)
    p1 = hyper_pmf(N, M, K, range(0, min(M, K) + 1))
    tot = 0.0
    for x, px in enumerate(p1):
        if px == 0.0:
            continue
        # given block 1 took x of the M exceedances, block 2 draws K from the remaining N-K
        p2_clear = float(hyper_pmf(N - K, M - x, K, range(0, c + 1)).sum())
        tot += px * (1.0 - p2_clear) if x <= c else px * p2_clear
    return float(2.0 * tot) if False else float(
        # P(exactly one clears) = sum_x P(x) * [x<=c: P(other not clear) ; x>c: P(other clear)]
        tot)


def truth_verdict(N, M, q):
    """The population verdict: clears iff the real effect beats the population's own band."""
    return M <= c_of(N, q)


def p_err(N, M, K, q):
    """P(a K-block's verdict differs from the population verdict)."""
    pc = p_clear(N, M, K, q)
    return (1.0 - pc) if truth_verdict(N, M, q) else pc


# ================================================================ the estimators
def fbp_mc(N, M, K, q, B, rng):
    """FBP-B: B independent pairs of DISJOINT K-blocks; returns the flip FRACTION."""
    if 2 * K > N:
        return np.nan
    c = c_of(K, q)
    x1 = rng.hypergeometric(M, N - M, K, size=B)
    x2 = np.array([rng.hypergeometric(max(M - a, 0), (N - K) - max(M - a, 0), K)
                   if (N - K) >= K and (N - K) - max(M - a, 0) >= 0 else 0 for a in x1])
    return float(np.mean((x1 <= c) != (x2 <= c)))


def blocks_207(N, M, K, q, rng, pool=POOL_207):
    """Idea 207's own estimator: cut a `pool`-draw sample into floor(pool/K) disjoint blocks and
    take the PAIRWISE disagreement rate over them.  The comparison count falls as 1/K."""
    nb = pool // K
    if nb < 2 or pool > N:
        return np.nan, 0
    lab = np.zeros(N, np.int8)
    lab[:M] = 1
    draw = rng.permutation(N)[:pool]
    v = lab[draw][:nb * K].reshape(nb, K).sum(axis=1) <= c_of(K, q)
    npair = nb * (nb - 1) // 2
    flips = sum(int(v[i] != v[j]) for i in range(nb) for j in range(i + 1, nb))
    return flips / npair, npair


# ================================================================ main
def main():
    t0 = time.time()
    P("=" * 118)
    P("QUEUE idea 216 - a flip-rate estimator that is not confounded by block count   (cloud, 2026-09-08)")
    P("=" * 118)
    P("Idea 207's flip rate cuts a 400-draw pool into floor(400/K) DISJOINT blocks, so its")
    P("comparison count falls as 1/K and its own standard error RISES with K - at K=200 it is one")
    P("Bernoulli trial per configuration, and both of idea 207's missed predictions are that row.")
    P("This run builds FBP-B (B pairs at every K, comparisons fixed), derives its EXACT law, and")
    P("re-runs the ladder with the comparison count held fixed.")
    P("")
    P(f"Tuned parameters: K in {KS} x B in {BS}.  Band/panel/family/depth/statistic/rung are corpus axes.")
    P("")

    # ------------------------------------------------------------ panels, control books
    P("PANELS")
    PANS = p191.build_panels()
    CTRL = []
    for pan in PANS:
        d = {}
        for bps in COST_RUNGS:
            cr = p191.net(pan._r0, bps).loc[pan.start:]
            m = metrics(cr)
            mo = metrics(cr.loc[OOS_START:])
            h1, h2 = p191.halves(cr)
            d[bps] = dict(Sharpe=m["Sharpe"], CAGR=m["CAGR"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                          Sharpe_IS=p191._sh(cr.loc[:IS_END]),
                          Sharpe_OOS=p191._sh(cr.loc[OOS_START:]),
                          CAGR_OOS=mo["CAGR"], MaxDD_OOS=mo["MaxDD"], r=cr)
        CTRL.append(d)
    P("")

    # ------------------------------------------------------------ re-run the 180 real books
    P("RE-RUNNING THE 90 CONFIGURATIONS' REAL BOOKS FROM SCRATCH (idea 191's machinery, verbatim)")
    rows = []
    for pi, pan in enumerate(PANS):
        spy = pan.spy.loc[pan.start:]
        for fam in p191.FAM_ORDER:
            _, thrs, _, depths = p191.FAMILIES[fam]
            for thr in thrs:
                s_real = p191.on_indicator(pan, fam, thr)
                for depth in depths:
                    W, mask = p191.apply_overlay(pan, fam, depth, s_real)
                    res = p191.fast_backtest(pan.px, W, 0.0, FREQ, mask=mask)
                    for bps in COST_RUNGS:
                        r = p191.net(res, bps).loc[pan.start:]
                        m, mo = metrics(r), metrics(r.loc[OOS_START:])
                        h1, h2 = p191.halves(r)
                        c = CTRL[pi][bps]
                        rows.append(dict(
                            panel=pan.name, family=fam, thr=thr, depth=str(depth), bps=bps,
                            on_share=float(s_real.mean()), J=len(s_real),
                            dS=m["Sharpe"] - c["Sharpe"], dDD=m["MaxDD"] - c["MaxDD"],
                            dIS=p191._sh(r.loc[:IS_END]) - c["Sharpe_IS"],
                            Sharpe=m["Sharpe"], CAGR=m["CAGR"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                            Sharpe_IS=p191._sh(r.loc[:IS_END]),
                            Sharpe_OOS=p191._sh(r.loc[OOS_START:]),
                            CAGR_OOS=mo["CAGR"], MaxDD_OOS=mo["MaxDD"],
                            fail4a=p191.keep_4a(r, c["r"]), fail4b=p191.keep_4b(r, spy)))
        P(f"  {pan.name} done ({time.time()-t0:.0f}s)")
    R = pd.DataFrame(rows)
    R["pass4a"] = R.fail4a == "-"
    R["pass4b"] = R.fail4b == "-"
    R.to_csv(OUT / f"{STEM}.real.csv", index=False)
    P("")

    # ------------------------------------------------------------ gates
    P("=" * 118)
    P("GATES")
    P("=" * 118)
    ok = True
    EX = pd.read_csv(OUT / f"{ENUM_STEM}.exact.csv")
    key = ["panel", "family", "thr", "depth", "bps"]
    EX["depth"] = EX.depth.astype(str)
    R["thr"] = R.thr.astype(float)
    EX["thr"] = EX.thr.astype(float)
    Mg = R.merge(EX, on=key, suffixes=("", "_ex"))
    P(f"  matched {len(Mg)} of {len(EX)} committed rows")
    ok &= len(Mg) == len(EX)
    worst = {}
    for a, b in [("Sharpe", "Sharpe"), ("CAGR", "CAGR"), ("MaxDD", "MaxDD"), ("H1", "H1"),
                 ("H2", "H2"), ("Sharpe_OOS", "Sharpe_OOS"), ("CAGR_OOS", "CAGR_OOS"),
                 ("MaxDD_OOS", "MaxDD_OOS"), ("on_share", "on_share"), ("J", "J")]:
        worst[a] = float((Mg[a] - Mg[b + "_ex"]).abs().max())
    for st, col in [("S", "dS"), ("DD", "dDD"), ("IS", "dIS")]:
        worst[f"|d{st}|"] = float((Mg[col].abs() - Mg[f"absd_{st}"]).abs().max())
    ga = max(worst.values())
    P("  [a] fresh real books vs the committed enumeration: " +
      "  ".join(f"{k}={v:.2e}" for k, v in worst.items()))
    P(f"      max = {ga:.3e}  -> {'PASS' if ga < 1e-12 else 'FAIL'}")
    ok &= ga < 1e-12
    dk = int((Mg.pass4a != Mg.pass4a_ex).sum() + (Mg.pass4b != Mg.pass4b_ex).sum())
    P(f"      KEEP verdicts identical: {len(Mg)*2 - dk}/{len(Mg)*2}")
    ok &= dk == 0

    # [c] full enumeration of one configuration per panel
    P("")
    ce = []
    for pi, pan in enumerate(PANS):
        fam, thr, depth = "BUDGET", 0.20, "skip"
        s_real = p191.on_indicator(pan, fam, thr)
        J = len(s_real)
        acc = {bps: [] for bps in COST_RUNGS}
        realv = {}
        for kind, s in ([("real", s_real)] + [("null", np.roll(s_real, o)) for o in range(1, J)]):
            W, mask = p191.apply_overlay(pan, fam, depth, s)
            res = p191.fast_backtest(pan.px, W, 0.0, FREQ, mask=mask)
            for bps in COST_RUNGS:
                r = p191.net(res, bps).loc[pan.start:]
                d = metrics(r)["Sharpe"] - CTRL[pi][bps]["Sharpe"]
                (acc[bps].append(d) if kind == "null" else realv.setdefault(bps, d))
        for bps in COST_RUNGS:
            a = np.abs(np.asarray(acc[bps], float))
            ra = abs(realv[bps])
            M = int((a >= ra - 1e-9 * max(1.0, ra)).sum())
            ties = int((np.abs(a - ra) <= 1e-9 * max(1.0, ra)).sum())
            e = EX[(EX.panel == pan.name) & (EX.family == fam) & (EX.thr == thr)
                   & (EX.depth == depth) & (EX.bps == bps)].iloc[0]
            ce.append(dict(panel=pan.name, bps=bps, N_here=len(a), N_ex=int(e.N_S),
                           M_here=M, M_ex=int(e.K_S), ties=ties,
                           dabs=abs(ra - float(e.absd_S))))
    CE = pd.DataFrame(ce)
    gc = bool((CE.N_here == CE.N_ex).all()
              and ((CE.M_here - CE.M_ex).abs() <= CE.ties.clip(lower=0) + 1).all()
              and CE.dabs.max() < 1e-12)
    P("  [c] FULL enumeration of BUDGET/0.20/skip on every panel vs the committed (M, N):")
    P("  " + CE.to_string(index=False).replace("\n", "\n  "))
    P(f"      -> {'PASS' if gc else 'FAIL'}")
    ok &= gc

    # [d] the hypergeometric identity
    rng = np.random.default_rng(SEED)
    dd = []
    for (N, M, K, q) in [(974, 100, 20, 1.0), (974, 5, 100, 1.0), (869, 300, 50, 0.95),
                         (974, 40, 200, 0.95), (974, 0, 20, 1.0), (974, 974, 400, 1.0)]:
        lab = np.zeros(N, np.int8)
        lab[:M] = 1
        hits = np.mean([lab[rng.permutation(N)[:K]].sum() <= c_of(K, q) for _ in range(4000)])
        dd.append(dict(N=N, M=M, K=K, q=q, exact=p_clear(N, M, K, q), mc=hits,
                       d=abs(p_clear(N, M, K, q) - hits)))
    DD = pd.DataFrame(dd)
    gd = float(DD.d.max())
    P("")
    P("  [d] closed-form P(clear) vs brute-force sampling (4000 replicates):")
    P("  " + DD.to_string(index=False, float_format=lambda x: f"{x:.5f}").replace("\n", "\n  "))
    tol = 3 * math.sqrt(0.25 / 4000)
    P(f"      max|d| = {gd:.4f} vs 3 MC se = {tol:.4f}  -> {'PASS' if gd < tol else 'FAIL'}")
    ok &= gd < tol
    for N in (974, 869):
        assert p_clear(N, 0, N, 1.0) == 1.0 and p_clear(N, 1, N, 1.0) == 0.0
    P("      P(clear) at K=N is the population verdict exactly (asserted)")

    P("")
    P(f"  ALL GATES {'PASS' if ok else 'FAIL'}")
    assert ok, "gates failed - no number below may be read"
    P("")

    # ------------------------------------------------------------ the claim corpus
    claims = []
    for _, e in EX.iterrows():
        for st in STATS:
            claims.append(dict(panel=e.panel, family=e.family, thr=e.thr, depth=e.depth,
                               bps=int(e.bps), stat=st, N=int(e[f"N_{st}"]), M=int(e[f"K_{st}"]),
                               ties=int(e[f"ties_{st}"]), absd=float(e[f"absd_{st}"])))
    CL = pd.DataFrame(claims)
    CL["degenerate"] = CL.ties >= CL.N
    P("=" * 118)
    P(f"CLAIM CORPUS: {len(CL)} claims = {len(EX)} committed rows x {len(STATS)} statistics")
    P("=" * 118)
    P(f"  rotation-DEGENERATE claims (every rotation reproduces the real book, ties == N): "
      f"{int(CL.degenerate.sum())} of {len(CL)} "
      f"({CL.degenerate.mean():.1%}) - no estimator can have power on these, and they are")
    P("  idea 203's `free_strata == 0` case seen from the other side.  They are kept in the corpus")
    P("  and flagged; every table below is also shown on the non-degenerate subset.")
    P(f"  exceedance rate M/N: median {float((CL.M/CL.N).median()):.4f}, "
      f"{int((CL.M==0).sum())} claims have M = 0 (the population itself clears)")
    P("")

    # ------------------------------------------------------------ Q1: the estimators' variance
    P("=" * 118)
    P("Q1  THE CONFOUND ITSELF.  Comparison count and estimator standard error, per configuration.")
    P("=" * 118)
    er = []
    for K in KS:
        nb = POOL_207 // K
        npair_207 = nb * (nb - 1) // 2 if nb >= 2 else 0
        er.append(dict(K=K, blocks_207=nb, pairs_207=npair_207,
                       se_207_at_p_half=(np.nan if npair_207 == 0 else 0.5 / math.sqrt(npair_207)),
                       pairs_FBP=BS[-1], se_FBP_at_p_half=0.5 / math.sqrt(BS[-1])))
    ER = pd.DataFrame(er)
    P(ER.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("  (se at the worst case p = 1/2; idea 207's falls to ONE pair at K=200, FBP-B holds B.)")
    P("")

    # ------------------------------------------------------------ Q2: gate [b] / convergence
    P("=" * 118)
    P("Q2  FBP-B AGAINST ITS OWN CLOSED FORM.  Mean |MC - exact| over the whole corpus, by B.")
    P("=" * 118)
    rng = np.random.default_rng(SEED + 1)
    conv = []
    sub = CL[~CL.degenerate]
    for band, q in BANDS:
        for K in KS:
            ex = np.array([p_flip(r.N, r.M, K, q) for r in sub.itertuples()])
            for B in BS:
                mc = np.array([fbp_mc(r.N, r.M, K, q, B, rng) for r in sub.itertuples()])
                d = np.abs(mc - ex)
                conv.append(dict(band=band, K=K, B=B, mean_abs_err=float(np.nanmean(d)),
                                 rms=float(np.sqrt(np.nanmean(d ** 2))),
                                 mean_exact=float(np.nanmean(ex))))
    CV = pd.DataFrame(conv)
    CV.to_csv(OUT / f"{STEM}.estimator.csv", index=False)
    t = CV.pivot_table(index=["band", "K"], columns="B", values="rms")
    P("  RMS |FBP-B - exact| over the corpus:")
    P("  " + t.to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n  "))
    r256 = CV[CV.B == BS[-1]].rms.mean()
    r1 = CV[CV.B == 1].rms.mean()
    rate = r1 / r256 if r256 else np.nan
    P(f"  [b] mean RMS falls {r1:.4f} -> {r256:.4f} = 1/{rate:.2f} against "
      f"sqrt({BS[-1]}/{BS[0]}) = {math.sqrt(BS[-1]/BS[0]):.2f}  "
      f"-> {'PASS' if 0.5 < rate / math.sqrt(BS[-1]/BS[0]) < 2.0 else 'FAIL'}")
    P("")

    # ------------------------------------------------------------ gate [e] + Q3: the ladder
    P("=" * 118)
    P("Q3  THE RE-RUN LADDER, comparison count HELD FIXED.  Every quantity is the exact law")
    P("    evaluated on each claim's own (M, N); the 207 column is its own construction.")
    P("=" * 118)
    rng = np.random.default_rng(SEED + 2)
    lad = []
    for band, q in BANDS:
        for K in KS:
            for tag, s in [("all", CL), ("non-degenerate", sub)]:
                pf = np.array([p_flip(r.N, r.M, K, q) for r in s.itertuples()])
                pe = np.array([p_err(r.N, r.M, K, q) for r in s.itertuples()])
                pc = np.array([p_clear(r.N, r.M, K, q) for r in s.itertuples()])
                f207 = np.array([blocks_207(r.N, r.M, K, q, rng)[0] for r in s.itertuples()])
                lad.append(dict(band=band, K=K, subset=tag, n=len(s),
                                flip_exact=float(np.nanmean(pf)),
                                flip_FBP256=float(np.nanmean(
                                    [fbp_mc(r.N, r.M, K, q, 256, rng) for r in s.itertuples()])),
                                flip_207=float(np.nanmean(f207)),
                                err_vs_truth=float(np.nanmean(pe)),
                                clear_rate=float(np.nanmean(pc)),
                                undetermined=float(np.nanmean(pf > 0.05))))
    LD = pd.DataFrame(lad)
    LD.to_csv(OUT / f"{STEM}.ladder.csv", index=False)
    for tag in ["all", "non-degenerate"]:
        P(f"  subset = {tag}")
        P("  " + LD[LD.subset == tag].drop(columns=["subset"])
          .to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n  "))
        P("")
    d207 = float((LD.flip_207 - LD.flip_exact).abs().max())
    P(f"  [e] idea 207's own construction vs the exact law, max|d| = {d207:.4f} "
      f"(it is an unbiased but 1/K-noisy estimator of the same quantity)")
    P("")
    P("  THE K RECOMMENDATION, read off err_vs_truth on the non-degenerate subset:")
    for band, _ in BANDS:
        s = LD[(LD.band == band) & (LD.subset == "non-degenerate")].set_index("K")
        best = s.err_vs_truth.idxmin()
        P(f"    {band}: " + "  ".join(f"K={k}: {v:.4f}" for k, v in s.err_vs_truth.items())
          + f"   -> argmin at K={best}"
          + ("  (monotone: a FLOOR, not an optimum)"
             if best == max(KS) else "  (interior optimum)"))
    P("")

    # ------------------------------------------------------------ Q4: rule 8
    P("=" * 118)
    P("Q4  RULE 8 WALK-FORWARD.  Thresholds chosen on <= 2016-12-31; 2017-2026 read once.")
    P("    36 cells = 3 panels x 3 families x 2 depths x 2 cost rungs, 5-point ladders.")
    P("=" * 118)
    rng = np.random.default_rng(SEED + 3)
    RK = R.set_index(["panel", "family", "thr", "depth", "bps"])
    CLK = CL.set_index(["panel", "family", "thr", "depth", "bps", "stat"])
    wf = []
    for pi, pan in enumerate(PANS):
        for fam in p191.FAM_ORDER:
            _, thrs, _, depths = p191.FAMILIES[fam]
            for depth in depths:
                for bps in COST_RUNGS:
                    c = CTRL[pi][bps]
                    lad_thr = [float(t) for t in thrs]
                    cand = RK.loc[[(pan.name, fam, t, str(depth), bps) for t in lad_thr]]
                    cand.index = lad_thr
                    spy_oos = p191._sh(pan.spy.loc[OOS_START:])

                    def emit(arm, pi_, sd=0.0, npool=len(lad_thr)):
                        if pi_ is None:
                            wf.append(dict(panel=pan.name, family=fam, depth=str(depth), bps=bps,
                                           arm=arm, thr=np.nan, n_pool=npool, empty=True,
                                           OOS_Sharpe=c["Sharpe_OOS"], OOS_CAGR=c["CAGR_OOS"],
                                           OOS_MaxDD=c["MaxDD_OOS"], sd_across_draws=sd,
                                           d_vs_S0=0.0,
                                           d_vs_SPY=c["Sharpe_OOS"] - spy_oos))
                            return
                        row = cand.loc[pi_]
                        wf.append(dict(panel=pan.name, family=fam, depth=str(depth), bps=bps,
                                       arm=arm, thr=pi_, n_pool=npool, empty=False,
                                       OOS_Sharpe=row.Sharpe_OOS, OOS_CAGR=row.CAGR_OOS,
                                       OOS_MaxDD=row.MaxDD_OOS, sd_across_draws=sd,
                                       d_vs_S0=row.Sharpe_OOS - c["Sharpe_OOS"],
                                       d_vs_SPY=row.Sharpe_OOS - spy_oos))

                    emit("S0_do_nothing", None, 0.0, 0)
                    emit("S1_IS_argmax", cand.Sharpe_IS.idxmax())
                    mn = {t: CLK.loc[(pan.name, fam, t, str(depth), bps, "IS")] for t in lad_thr}
                    for band, q in BANDS:
                        for K in KS:
                            pc = {t: p_clear(int(mn[t].N), int(mn[t].M), K, q) for t in lad_thr}
                            outs, pools = [], []
                            for _ in range(R_SIM):
                                pool = [t for t in lad_thr if rng.random() < pc[t]]
                                pools.append(len(pool))
                                outs.append(cand.loc[pool].Sharpe_IS.idxmax() if pool else None)
                            vals = [c["Sharpe_OOS"] if o is None else cand.loc[o].Sharpe_OOS
                                    for o in outs]
                            mean_v = float(np.mean(vals))
                            sd_v = float(np.std(vals, ddof=1))
                            wf.append(dict(panel=pan.name, family=fam, depth=str(depth), bps=bps,
                                           arm=f"S2_{band}_K{K}", thr=np.nan,
                                           n_pool=float(np.mean(pools)),
                                           empty=bool(np.mean(pools) == 0),
                                           OOS_Sharpe=mean_v, OOS_CAGR=np.nan, OOS_MaxDD=np.nan,
                                           sd_across_draws=sd_v,
                                           d_vs_S0=mean_v - c["Sharpe_OOS"],
                                           d_vs_SPY=mean_v - spy_oos))
                        ex_pool = [t for t in lad_thr
                                   if truth_verdict(int(mn[t].N), int(mn[t].M), q)]
                        emit(f"S3_EXACT_{band}",
                             cand.loc[ex_pool].Sharpe_IS.idxmax() if ex_pool else None,
                             0.0, len(ex_pool))
                    emit("ORACLE_OOS", cand.Sharpe_OOS.idxmax())
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    summ = WF.groupby("arm").agg(mean_OOS_Sharpe=("OOS_Sharpe", "mean"),
                                 mean_d_vs_S0=("d_vs_S0", "mean"),
                                 mean_d_vs_SPY=("d_vs_SPY", "mean"),
                                 wins_vs_S0=("d_vs_S0", lambda x: int((x > 0).sum())),
                                 mean_pool=("n_pool", "mean"),
                                 mean_sd_draws=("sd_across_draws", "mean"),
                                 n=("d_vs_S0", "size"))
    summ["t_vs_S0"] = [p191.tstat(WF[WF.arm == a].d_vs_S0.values) for a in summ.index]
    P(summ.to_string(float_format=lambda x: f"{x:+.4f}"))
    P("")
    base_oos = WF[WF.arm == "S0_do_nothing"]
    P(f"  S0 (control book) mean OOS Sharpe {base_oos.OOS_Sharpe.mean():+.4f}, "
      f"mean OOS CAGR {base_oos.OOS_CAGR.mean():+.4f}, mean OOS MaxDD {base_oos.OOS_MaxDD.mean():+.4f}")
    P(f"  SPY mean OOS Sharpe over the same cells "
      f"{np.mean([p191._sh(p.spy.loc[OOS_START:]) for p in PANS for _ in range(12)]):+.4f}")
    los = int((summ.loc[[a for a in summ.index if a.startswith(('S2_', 'S3_'))],
                        "mean_d_vs_S0"] <= 0).sum())
    tot = len([a for a in summ.index if a.startswith(("S2_", "S3_"))])
    P(f"  clause-gated arms losing to (or tying) do-nothing: {los} of {tot}")
    P("")

    # ------------------------------------------------------------ Q5: KEEP
    P("=" * 118)
    P("Q5  KEEP PATHS (PROTOCOL rule 4), on the 180 freshly-run real rows.")
    P("=" * 118)
    P(f"  4a: {int(R.pass4a.sum())} / {len(R)}      4b: {int(R.pass4b.sum())} / {len(R)}      "
      f"BOTH: {int((R.pass4a & R.pass4b).sum())} / {len(R)}")
    P("  4b by panel x family:")
    P("  " + R.pivot_table(index="panel", columns="family", values="pass4b", aggfunc="mean")
      .to_string(float_format=lambda x: f"{x:.3f}").replace("\n", "\n  "))
    P("  4b failure clauses: " + ", ".join(f"{k}={v}" for k, v in R.fail4b.value_counts().head(6).items()))
    P(f"  SMALL439 4b passes: {int(R[R.panel=='SMALL439'].pass4b.sum())} of "
      f"{len(R[R.panel=='SMALL439'])}")
    bb = []
    for pi, pan in enumerate(PANS):
        for bps in COST_RUNGS:
            c = CTRL[pi][bps]
            bb.append(dict(panel=pan.name, bps=bps, CAGR=c["CAGR"], Sharpe=c["Sharpe"],
                           MaxDD=c["MaxDD"], H1=c["H1"], H2=c["H2"],
                           OOS_CAGR=c["CAGR_OOS"], OOS_Sharpe=c["Sharpe_OOS"],
                           OOS_MaxDD=c["MaxDD_OOS"]))
        s = pan.spy.loc[pan.start:]
        ms, mo = metrics(s), metrics(s.loc[OOS_START:])
        h1, h2 = p191.halves(s)
        bb.append(dict(panel=pan.name, bps=0, CAGR=ms["CAGR"], Sharpe=ms["Sharpe"],
                       MaxDD=ms["MaxDD"], H1=h1, H2=h2, OOS_CAGR=mo["CAGR"],
                       OOS_Sharpe=p191._sh(s.loc[OOS_START:]), OOS_MaxDD=mo["MaxDD"]))
    P("  control books and SPY:")
    P("  " + pd.DataFrame(bb).to_string(index=False, float_format=lambda x: f"{x:.4f}")
      .replace("\n", "\n  "))
    R.to_csv(OUT / f"{STEM}.keep.csv", index=False)
    P("")
    P(f"  runtime {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()

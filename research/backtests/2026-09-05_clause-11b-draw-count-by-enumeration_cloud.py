#!/usr/bin/env python3
"""IDEA 207  how-many-draws-does-clause-11b-need   (cloud lane, 2026-09-05)

QUESTION (QUEUE.md).  Idea 201 measured the 20-rotation band on 3 disjoint blocks and found
mean(range/band) = 63.3% with 17.8% of 180 clause verdicts flipping between blocks.  Idea 208
then enumerated the COMPLETE rotation population for the 30 U56 configurations and found 83.3%
of those cells UNDETERMINED at 20 draws.  Sweep the draw count on the SAME 90 configurations
(3 panels x 30) and report the flip rate and the undetermined-zone width at each; the output is
the number PROTOCOL clause 11b should specify.

WHAT THIS RUN DOES THAT ITS PARENTS DID NOT.  Idea 208 enumerated ONE panel.  This run
enumerates ALL THREE -- every circular rotation of every overlay ON-series, 3 panels x 30
configurations x (1 real + J-1 rotations) x 2 cost rungs -- so every draw-count statement below
is a closed-form property of a fully known finite population, not itself a sample.

THE DISTINCTION THE IDEA'S OWN WORDING HIDES, and the run's main result:
  * clause 11b as WRITTEN ("clears iff |d_real| > max of n draws") is a hypothesis test whose
    SIZE is 1/(n+1).  Raising n from 20 to 200 does not make the same clause more accurate, it
    silently replaces a 4.76% clause with a 0.50% one.  "How many draws" is therefore not
    answerable while the rule is phrased as a max.
  * phrased at a FIXED LEVEL -- the standard Monte-Carlo permutation p-value
    p_hat = (#draws >= |d_real| + 1) / (n + 1), clears iff p_hat <= alpha -- the level is held
    at alpha for every n and the draw count controls only PRECISION.  At alpha = 0.05 and
    n = 20 this rule IS the incumbent max-of-20, so the repair is backward-compatible at the
    incumbent point and the sweep becomes meaningful.
  Both rules are reported at every draw count.  Which one is reported is a carried axis, not a
  tuned parameter.

TUNED PARAMETERS (exactly 2, all grid points reported):
  1. n_draw   in {20, 50, 100, 200}          -- the idea's own parameter
  2. epsilon  in {0.05, 0.10, 0.20}          -- the undetermined band, P(clears) in [eps, 1-eps]
  Carried axes (not tuned): 3 panels, 3 overlay families, 5 thresholds, 2 depths, 2 cost rungs,
  2 clause forms (MAXN incumbent / PVAL level-alpha), statistic (Sharpe / MaxDD / IS-Sharpe).

PROTOCOL.
  * 2 (execution/costs): t+1 via the engine's own convention; cost rungs 10 and 25 bps derived
    exactly from a single 0 bps run through the engine's turnover series (identity asserted).
  * 3 (baseline): RULES v1 and SPY reported per panel, full sample / halves / OOS window.
  * 4 (KEEP paths): 4a and 4b evaluated on all 180 real overlay rows and cross-tabulated with
    the clause verdict at every draw count.  This idea proposes NO book, so it claims neither
    path; the KEEP columns are reported because the sprint requires them.
  * 5: one idea, one script, deterministic.  All seeds via zlib.crc32 -- NO hash() of a str
    anywhere (the defect idea 208 found and this run must not repeat).
  * 8 (walk-forward): the clause is used as a rule-8 SELECTION GATE -- pick within
    (panel, family, cost rung) on IS <= 2016-12-31 by largest IS dSharpe among configs whose IS
    effect clears the clause, read 2017-2026 ONCE -- at every draw count, against the
    do-nothing control, RULES v1 and SPY.
  * 9: BROAD136 and SMALL439 are current constituents -- SURVIVORSHIP bias is one-directional
    and stated.  SMALL439 = the 483-name sub-$2B panel with the 44 max_1d_move >= 1.0 tickers
    dropped, per data/small_meta.csv.
  * Idea 38's calendar-day index and idea 126's t+1 are inherited unchanged from the parents.

Imports idea 191's machinery verbatim (panels, overlays, rotations, fast_backtest, KEEP bars)
so that the enumerated population is literally the population its published bands were drawn
from.  Reproduction of idea 191's 180 real rows and of idea 208's 60 exact K/N counts is
asserted BEFORE any new number is read.

Writes .console.txt, .exact.csv, .grid.csv, .walkforward.csv.gz, .keep.csv.
"""
import importlib.util
import pickle
import sys
import tempfile
import time
import zlib
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_clause-11b-draw-count-by-enumeration_cloud"
OUT = ROOT / "research" / "backtests"
P191_STEM = "2026-09-05_the-on-share-column_cloud"                 # idea 191
P208_STEM = "2026-09-05_audit-every-committed-null-for-a-salted-seed_C"   # idea 208

KAPPAS = [20, 50, 100, 200]          # tuned parameter 1
EPSILONS = [0.05, 0.10, 0.20]        # tuned parameter 2
ALPHA = 0.05                         # the level the repaired clause holds fixed
N_SEEDS = 200                        # independent draw regimes for the rule-8 spread
IS_END, OOS_START = "2016-12-31", "2017-01-01"
SEED = zlib.crc32(b"idea-207-how-many-draws") % (2 ** 31)
# The enumeration is ~28 minutes of CPU and is a pure function of the committed parents, so it
# is cached OUTSIDE the repository (temp dir) purely as a re-run accelerator.  Delete the file
# and the script reproduces it from scratch; nothing downstream reads anything else.
CACHE = Path(tempfile.gettempdir()) / f"{STEM}.population.pkl"

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)

_lines: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _lines.append(s)


# ---------------------------------------------------------------- idea 191, imported verbatim
spec = importlib.util.spec_from_file_location("p191", OUT / f"{P191_STEM}.py")
p191 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p191)
p191.P = P                                    # redirect its printing into this console log

COST_RUNGS = p191.COST_RUNGS
FREQ = p191.FREQ

PANS: list = []
CTRL: dict = {}
BASE_RV: dict = {}

_LOGFACT = np.concatenate([[0.0], np.cumsum(np.log(np.arange(1, 4001, dtype=float)))])


# =========================================================== the exact draw laws (closed form)
def p_clear_maxn(K, N, k):
    """Incumbent clause: clears iff |d_real| > max of k draws, i.e. ALL k draws fall below.
    P = C(K,k)/C(N,k).  Vectorised over K via log-factorials; exact to double precision."""
    K = np.asarray(K)
    okm = K >= k
    lognum = _LOGFACT[np.where(okm, K, k)] - _LOGFACT[np.where(okm, K - k, 0)]
    logden = _LOGFACT[N] - _LOGFACT[N - k]
    v = np.exp(np.clip(lognum - logden, -700, 0.0))
    return float(np.where(okm, v, 0.0)) if K.ndim == 0 else np.where(okm, v, 0.0)


def _logC(n, m):
    n = np.asarray(n)
    m = np.asarray(m)
    bad = (m < 0) | (m > n) | (n < 0)
    ns, ms = np.where(bad, 0, n), np.where(bad, 0, m)
    v = _LOGFACT[ns] - _LOGFACT[ms] - _LOGFACT[ns - ms]
    return np.where(bad, -np.inf, v)


def p_clear_pval(K, N, k, alpha=ALPHA):
    """Level-alpha clause: p_hat = (R+1)/(k+1) <= alpha, R = #draws >= |d_real|.
    Clears iff R <= r_max = floor(alpha(k+1)) - 1.  R ~ Hypergeometric(N, A=N-K, k).
    Vectorised over K.  At alpha=0.05, k=20 this is exactly the incumbent max-of-20."""
    r_max = int(np.floor(alpha * (k + 1) - 1 + 1e-12))
    K = np.asarray(K)
    if r_max < 0:
        return np.zeros(K.shape) if K.ndim else 0.0
    A = N - K
    ld = _logC(N, k)
    tot = np.zeros(K.shape, float) if K.ndim else np.float64(0.0)
    for r in range(0, r_max + 1):
        tot = tot + np.exp(np.clip(_logC(A, r) + _logC(K, k - r) - ld, -700, 0.0))
    tot = np.clip(tot, 0.0, 1.0)
    return float(tot) if K.ndim == 0 else tot


def k_and_ties(null_abs, real_abs, rtol=1e-9):
    """K = #rotations STRICTLY below the real effect, with exact ties resolved conservatively
    (a tie is not 'below', so it cannot help the real effect clear).  Ties are real and common
    on the drawdown statistic -- a rotation that leaves the worst episode untouched reproduces
    |MaxDD| to machine precision -- so the boundary is set by a relative tolerance rather than
    by float noise.  Returns (K, n_ties, N)."""
    a = np.abs(np.asarray(null_abs, float))      # accepts signed or absolute null values
    tol = rtol * max(abs(real_abs), 1e-12)
    ties = int((np.abs(a - real_abs) <= tol).sum())
    K = int((a < real_abs - tol).sum())
    return K, ties, len(a)


def truth_pval(K, N, alpha=ALPHA):
    """Exact permutation verdict from the WHOLE population: p = (#{null >= real} + 1)/(N+1)."""
    return ((N - K) + 1) / (N + 1) <= alpha


def _pcurve(N, k, rule):
    """P(clears) as a function of K = 0..N, cached: monotone non-decreasing in K."""
    key = (N, k, rule)
    if key not in _PCACHE:
        f = p_clear_maxn if rule == "MAXN" else p_clear_pval
        _PCACHE[key] = np.asarray(f(np.arange(N + 1), N, k), float)
    return _PCACHE[key]


_PCACHE: dict = {}


def zone_bounds(sorted_abs, k, eps, rule):
    """Interval of |d_real| values whose P(clears) lies in [eps, 1-eps], in effect units.
    P is a non-decreasing step function of K, so invert it by searching the curve."""
    N = len(sorted_abs)
    cur = _pcurve(N, k, rule)
    lo = int(np.searchsorted(cur, eps, side="left"))
    hi = int(np.searchsorted(cur, 1 - eps, side="left"))
    a = sorted_abs[min(max(lo - 1, 0), N - 1)]
    b = sorted_abs[min(max(hi - 1, 0), N - 1)]
    return float(a), float(b), float(b - a)


# ============================================================================ enumeration job
def job(args):
    pi, fam, thr, depth = args
    pan = PANS[pi]
    s_real = p191.on_indicator(pan, fam, thr)
    J = len(s_real)
    start = pan.start
    spy = pan.spy.loc[start:]
    b0, bt = BASE_RV[pi]
    acc = {bps: {"dS": [], "dD": [], "dIS": []} for bps in COST_RUNGS}
    real = {}
    for kind, s in ([("real", s_real)]
                    + [("null", np.roll(s_real, o)) for o in range(1, J)]):
        W, mask = p191.apply_overlay(pan, fam, depth, s)
        res = p191.fast_backtest(pan.px, W, 0.0, FREQ, mask=mask)
        for bps in COST_RUNGS:
            r = p191.net(res, bps).loc[start:]
            m = metrics(r)
            dS = m["Sharpe"] - CTRL[pi][bps]["Sharpe"]
            dD = m["MaxDD"] - CTRL[pi][bps]["MaxDD"]
            dIS = p191._sh(r.loc[:IS_END]) - CTRL[pi][bps]["Sharpe_IS"]
            if kind == "null":
                acc[bps]["dS"].append(dS)
                acc[bps]["dD"].append(dD)
                acc[bps]["dIS"].append(dIS)
            else:
                mo = metrics(r.loc[OOS_START:])
                h1, h2 = p191.halves(r)
                br = b0 - bt * bps / 1e4
                real[bps] = dict(
                    panel=pan.name, family=fam, thr=thr, depth=str(depth), bps=bps,
                    on_share=float(s_real.mean()), switches=p191.circ_switches(s_real),
                    J=J, dSharpe=dS, dMaxDD=dD, dSharpe_IS=dIS,
                    Sharpe=m["Sharpe"], CAGR=m["CAGR"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                    Sharpe_OOS=p191._sh(r.loc[OOS_START:]), CAGR_OOS=mo["CAGR"],
                    MaxDD_OOS=mo["MaxDD"],
                    fail4a=p191.keep_4a(r, br), fail4b=p191.keep_4b(r, spy))
    nulls = {bps: {k: np.asarray(v, float) for k, v in acc[bps].items()}
             for bps in COST_RUNGS}
    return (pi, fam, thr, str(depth)), real, nulls


# ============================================================================================
def main():
    t0 = time.time()
    P("=" * 118)
    P("IDEA 207  how-many-draws-does-clause-11b-need   (cloud, 2026-09-05)")
    P("=" * 118)
    P(__doc__.split("Writes ")[0].strip()[:0] or "")

    global PANS, CTRL
    PANS = p191.build_panels()
    for pi, pan in enumerate(PANS):
        start = pan.start
        bf = backtest(pan.px, rules_v1_weights(pan.px), cost_bps=0.0, freq=FREQ)
        BASE_RV[pi] = (bf["returns"].loc[start:], bf["turnover"].loc[start:])
        CTRL[pi] = {}
        for bps in COST_RUNGS:
            cr = p191.net(pan._r0, bps).loc[start:]
            m = metrics(cr)
            mo = metrics(cr.loc[OOS_START:])
            h1, h2 = p191.halves(cr)
            CTRL[pi][bps] = dict(Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], CAGR=m["CAGR"],
                                 H1=h1, H2=h2, Sharpe_IS=p191._sh(cr.loc[:IS_END]),
                                 Sharpe_OOS=p191._sh(cr.loc[OOS_START:]),
                                 CAGR_OOS=mo["CAGR"], MaxDD_OOS=mo["MaxDD"])

    # ------------------------------------------------------------------ reproduction, first
    P("\n" + "=" * 118)
    P("REPRODUCTION, asserted before any new number is read")
    P("=" * 118)
    ok = True
    for pan in PANS:
        ok &= p191.checks(pan)

    P("\n  PROTOCOL 3 baselines (RULES v1 and SPY), per panel, on each panel's own sample:")
    brows = []
    for pan in PANS:
        start = pan.start
        rv = backtest(pan.px, rules_v1_weights(pan.px), cost_bps=10.0,
                      freq=FREQ)["returns"].loc[start:]
        for nm, r in (("RULES v1 @10bps", rv), ("SPY", pan.spy.loc[start:])):
            m, mo = metrics(r), metrics(r.loc[OOS_START:])
            h1, h2 = p191.halves(r)
            brows.append(dict(panel=pan.name, name=nm, CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                              MaxDD=m["MaxDD"], H1=h1, H2=h2, CAGR_OOS=mo["CAGR"],
                              Sharpe_OOS=p191._sh(r.loc[OOS_START:]), MaxDD_OOS=mo["MaxDD"]))
        for bps in (10, 25):
            c = CTRL[PANS.index(pan)][bps]
            brows.append(dict(panel=pan.name, name=f"control book @{bps}bps",
                              CAGR=c["CAGR"], Sharpe=c["Sharpe"], MaxDD=c["MaxDD"],
                              H1=c["H1"], H2=c["H2"], CAGR_OOS=c["CAGR_OOS"],
                              Sharpe_OOS=c["Sharpe_OOS"], MaxDD_OOS=c["MaxDD_OOS"]))
    BASE = pd.DataFrame(brows)
    P(BASE.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    u = BASE[(BASE.panel == "U56") & (BASE.name == "RULES v1 @10bps")].iloc[0]
    d = abs(u.Sharpe - 0.66418)
    P(f"\n  [d] RULES v1 on U56 @10bps Sharpe {u.Sharpe:.5f} vs idea 208's published 0.66418 "
      f"-> {'PASS' if d < 5e-5 else 'FAIL'}")
    ok &= d < 5e-5
    if not ok:
        P("\nreproduction FAILS -- STOP")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        return

    # ------------------------------------------------------------------ the enumeration
    JOBS = []
    for pi, pan in enumerate(PANS):
        for fam in p191.FAM_ORDER:
            _, thrs, _, depths = p191.FAMILIES[fam]
            for thr in thrs:
                for depth in depths:
                    JOBS.append((pi, fam, thr, depth))
    JOBS.sort(key=lambda j: -PANS[j[0]].px.shape[1])          # heaviest panel first
    tot_bt = sum(len(p191.on_indicator(PANS[j[0]], j[1], j[2])) for j in JOBS)
    P("\n" + "=" * 118)
    P(f"ENUMERATION -- the COMPLETE rotation population of all {len(JOBS)} configurations")
    P(f"    {len(JOBS)} configs x (1 real + J-1 rotations) = {tot_bt:,} genuine backtests, "
      f"x {len(COST_RUNGS)} cost rungs = {tot_bt * 2:,} rows")
    P("=" * 118)
    REAL, NULL = {}, {}
    if CACHE.exists():
        with CACHE.open("rb") as fh:
            REAL, NULL = pickle.load(fh)
        P(f"  population restored from the local cache {CACHE.name} "
          f"({len(REAL)} real rows) -- delete it to force a fresh enumeration")
    else:
        done = 0
        with Pool(4) as pool:
            for key, real, nulls in pool.imap_unordered(job, JOBS):
                for bps in COST_RUNGS:
                    REAL[key + (bps,)] = real[bps]
                    NULL[key + (bps,)] = nulls[bps]
                done += 1
                if done % 10 == 0 or done == len(JOBS):
                    P(f"  {done:3d}/{len(JOBS)} configs   ({time.time() - t0:.0f}s)")
        with CACHE.open("wb") as fh:
            pickle.dump((REAL, NULL), fh)
    P(f"\n  enumeration complete: {len(REAL)} real rows, "
      f"{sum(len(v['dS']) for v in NULL.values()):,} null rows ({time.time() - t0:.0f}s)")

    # ---------------------------------------- reproduce idea 191's 180 published real rows
    PC = pd.read_csv(OUT / f"{P191_STEM}.clause.csv")
    pidx = {p.name: i for i, p in enumerate(PANS)}
    dif = {c: [] for c in ["dSharpe", "dSharpe_IS", "dMaxDD", "on_share"]}
    nmat = 0
    for _, r in PC.iterrows():
        if r.panel not in pidx:
            continue
        k = (pidx[r.panel], r.family, r.thr, str(r.depth), int(r.bps))
        if k not in REAL:
            continue
        nmat += 1
        for c in dif:
            dif[c].append(abs(REAL[k][c] - r[c]))
    P(f"\n  [e] vs idea 191's published clause.csv: matched {nmat}/{len(PC)} rows")
    for c, v in dif.items():
        dd = float(np.nanmax(v))
        P(f"      max|d {c:<11s}| = {dd:.3e}  -> {'PASS' if dd < 1e-12 else 'FAIL'}")
        ok &= dd < 1e-12

    # ---------------------------------------- reproduce idea 208's 60 exact K/N counts
    EX = pd.read_csv(OUT / f"{P208_STEM}.exact.csv")
    bad, tied, ncmp, det = 0, 0, 0, []
    for _, r in EX.iterrows():
        if r.panel not in pidx:
            continue
        k = (pidx[r.panel], r.family, r.thr, str(r.depth), int(r.bps))
        if k not in REAL:
            continue
        for tag, col, rv in (("S", "dS", "dSharpe"), ("DD", "dD", "dMaxDD"),
                             ("IS", "dIS", "dSharpe_IS")):
            K, ties, N = k_and_ties(NULL[k][col], abs(REAL[k][rv]))
            ncmp += 1
            tied += ties > 0
            K8 = int(r[f"K_{tag}"])
            if N != int(r[f"N_{tag}"]) or abs(K - K8) > ties:
                bad += 1
                a = np.sort(np.abs(NULL[k][col]))
                real_abs = abs(REAL[k][rv])
                lo, hi = min(K, K8), max(K, K8)
                gap = float(np.max(np.abs(a[lo:hi] - real_abs))) if hi > lo else 0.0
                det.append(dict(cell=f"{r.family}/{r.thr}/{r.depth}/{r.bps}", stat=tag,
                                K_here=K, K_208=K8, ties=ties, N=N,
                                absd_here=real_abs, absd_208=float(r[f"absd_{tag}"]),
                                d_absd=abs(real_abs - float(r[f"absd_{tag}"])),
                                max_gap_over_disputed_rotations=gap))
    P(f"  [f] vs idea 208's exact.csv, {len(EX)} U56 cells x 3 statistics ({ncmp} comparisons): "
      f"{bad} (K, N) pairs outside their own 1e-9 tie count")
    P(f"      ({tied} of {ncmp} comparisons have >=1 exact tie between a rotation and the real "
      "effect; idea 208 broke those with a strict <, this run with a 1e-9 relative tolerance)")
    if det:
        D = pd.DataFrame(det)
        P("\n      every disputed comparison, with the actual distance between the disputed "
          "rotations and the real effect:")
        P(D.to_string(index=False))
        worst = float(D.max_gap_over_disputed_rotations.max())
        P(f"\n      largest |rotation - real| among ALL disputed rotations: {worst:.3e}")
        P("      -> the dispute is a tie-breaking convention at float precision, not a "
          "different population" if worst < 1e-9 else
          "      -> NOT float noise: the two enumerations disagree on real values")
        ok &= worst < 1e-9
    P(f"      verdict: {'PASS' if (not det or float(pd.DataFrame(det).max_gap_over_disputed_rotations.max()) < 1e-9) else 'FAIL'}")
    P(f"\n  REPRODUCTION: {'ALL PASS' if ok else 'FAILURE -- results below are not trusted'}")
    if not ok:
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        return

    # ============================================================ the population, per cell
    P("\n" + "=" * 118)
    P("THE ENUMERATED POPULATION -- K (rotations below the real effect) and N, per cell")
    P("=" * 118)
    rows = []
    for k, rv in REAL.items():
        pi, fam, thr, depth, bps = k
        rec = dict(panel=PANS[pi].name, family=fam, thr=thr, depth=depth, bps=bps,
                   on_share=rv["on_share"], J=rv["J"])
        for tag, col, rc in (("S", "dS", "dSharpe"), ("DD", "dD", "dMaxDD"),
                             ("IS", "dIS", "dSharpe_IS")):
            a = np.sort(np.abs(NULL[k][col]))
            real_abs = abs(rv[rc])
            K, ties, N = k_and_ties(a, real_abs)
            rec[f"absd_{tag}"] = real_abs
            rec[f"K_{tag}"] = K
            rec[f"ties_{tag}"] = ties
            rec[f"N_{tag}"] = N
            rec[f"truth_{tag}"] = truth_pval(K, N)
            for kap in KAPPAS:
                rec[f"pMAXN{kap}_{tag}"] = p_clear_maxn(K, N, kap)
                rec[f"pPVAL{kap}_{tag}"] = p_clear_pval(K, N, kap)
        rec.update({c: rv[c] for c in ["Sharpe", "CAGR", "MaxDD", "H1", "H2", "Sharpe_OOS",
                                       "CAGR_OOS", "MaxDD_OOS", "fail4a", "fail4b"]})
        rec["pass4a"] = rv["fail4a"] == "-"
        rec["pass4b"] = rv["fail4b"] == "-"
        rows.append(rec)
    EXACT = pd.DataFrame(rows).sort_values(["panel", "family", "thr", "depth", "bps"])
    EXACT.to_csv(OUT / f"{STEM}.exact.csv", index=False)
    P(f"  {len(EXACT)} cells written to {STEM}.exact.csv")
    P("\n  K/N by panel and family (Sharpe statistic), mean of K/N and count at the extremes:")
    g = EXACT.assign(frac=EXACT.K_S / EXACT.N_S).groupby(["panel", "family"])
    P(g.agg(n=("frac", "size"), mean_KoverN=("frac", "mean"),
            frac_ge_0p95=("frac", lambda x: float((x >= 0.95).mean())),
            frac_le_0p50=("frac", lambda x: float((x <= 0.50).mean())),
            mean_absd=("absd_S", "mean")).to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n  exact ties between a rotation and the real effect (the clause's own resolution "
      "limit),\n  mean number of tied rotations out of N, by statistic:")
    P("    dSharpe %.2f   dMaxDD %.2f   dSharpe_IS %.2f   |  cells with >=1 tie: "
      "S %d/%d, DD %d/%d, IS %d/%d"
      % (EXACT.ties_S.mean(), EXACT.ties_DD.mean(), EXACT.ties_IS.mean(),
         int((EXACT.ties_S > 0).sum()), len(EXACT), int((EXACT.ties_DD > 0).sum()), len(EXACT),
         int((EXACT.ties_IS > 0).sum()), len(EXACT)))

    # ============================================================ Q0  the size of the clause
    P("\n" + "=" * 118)
    P("Q0  WHAT THE DRAW COUNT ACTUALLY DOES TO THE INCUMBENT CLAUSE (the sweep's precondition)")
    P("=" * 118)
    P("  Under the null the real effect is exchangeable with the rotations, so the probability")
    P("  that a rotation used as a pseudo-real clears a max-of-n band drawn from the others is")
    P("  1/(n+1) EXACTLY.  Measured by enumeration: every rotation in turn is treated as the")
    P("  real and priced against the remaining N-1.")
    srows = []
    for kap in KAPPAS:
        vals = []
        ncell = 0
        for k in NULL:                            # ALL 180 cells, every rotation in each
            a = np.abs(NULL[k]["dS"])
            N = len(a)
            order = np.argsort(a)
            ranks = np.empty(N, int)
            ranks[order] = np.arange(N)           # #others strictly below (ties -> lower)
            vals.append(p_clear_maxn(ranks, N - 1, kap))
            ncell += 1
        v = np.concatenate(vals)
        srows.append(dict(n_draw=kap, nominal_1_over_np1=1.0 / (kap + 1),
                          measured_size=float(v.mean()), cells=ncell, pseudo_reals=len(v)))
    SZ = pd.DataFrame(srows)
    P("\n" + SZ.to_string(index=False, float_format=lambda x: f"{x:.5f}"))
    P("\n  -> the incumbent clause is NOT one clause evaluated more precisely at larger n; it is")
    P("     a DIFFERENT clause at every n, four times stricter at n=100 than at n=20.  Every")
    P("     number below is therefore reported for BOTH the incumbent max-of-n rule and the")
    P(f"     level-alpha p-value rule (alpha = {ALPHA}), which is the max-of-n rule at n=20.")

    # ============================================================ Q1  flip rate vs the truth
    P("\n" + "=" * 118)
    P("Q1  FLIP RATE -- expected disagreement between an n-draw verdict and the enumerated truth")
    P("=" * 118)
    frows = []
    for rule in ("MAXN", "PVAL"):
        for kap in KAPPAS:
            for tag in ("S", "DD", "IS"):
                pc = EXACT[f"p{rule}{kap}_{tag}"].values
                tr = EXACT[f"truth_{tag}"].values.astype(float)
                flip_truth = float(np.mean(pc * (1 - tr) + (1 - pc) * tr))
                selfdis = float(np.mean(2 * pc * (1 - pc)))
                frows.append(dict(rule=rule, n_draw=kap, stat=tag,
                                  E_clears=float(pc.mean()),
                                  truth_clears=float(tr.mean()),
                                  flip_vs_truth=flip_truth,
                                  two_seed_disagree=selfdis,
                                  P_eq_0=float((pc < 1e-12).mean()),
                                  P_eq_1=float((pc > 1 - 1e-12).mean())))
    FLIP = pd.DataFrame(frows)
    for tag, nm in (("S", "Sharpe"), ("DD", "MaxDD"), ("IS", "IS-Sharpe")):
        P(f"\n  statistic = {nm}   (180 cells)")
        P(FLIP[FLIP.stat == tag].drop(columns=["stat"])
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---- flip rate against idea 191's own PUBLISHED 20-draw verdict, the idea's literal ask
    P("\n  the idea's literal question -- expected disagreement with idea 191's PUBLISHED")
    P("  20-draw verdict (the verdicts actually committed to the LEADERBOARD):")
    prows = []
    PUB = {}
    for _, r in PC.iterrows():
        if r.panel not in pidx:
            continue
        PUB[(pidx[r.panel], r.family, float(r.thr), str(r.depth), int(r.bps))] = (
            float(bool(r.clears)), float(bool(r.clearsDD)))
    for rule in ("MAXN", "PVAL"):
        for kap in KAPPAS:
            dS, dD = [], []
            for _, r in EXACT.iterrows():
                key = (pidx[r.panel], r.family, float(r.thr), str(r.depth), int(r.bps))
                pubS, pubD = PUB[key]
                for tag, pubv, acc in (("S", pubS, dS), ("DD", pubD, dD)):
                    pp = r[f"p{rule}{kap}_{tag}"]
                    acc.append(pp * (1 - pubv) + (1 - pp) * pubv)
            prows.append(dict(rule=rule, n_draw=kap, cells=len(dS) ,
                              flip_vs_published_Sharpe=float(np.mean(dS)),
                              flip_vs_published_MaxDD=float(np.mean(dD))))
    PUBF = pd.DataFrame(prows)
    P("\n" + PUBF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ============================================================ Q2  undetermined zone width
    P("\n" + "=" * 118)
    P("Q2  UNDETERMINED-ZONE WIDTH -- the band of true effect sizes the clause cannot resolve")
    P("=" * 118)
    P("  For each cell the zone is the interval of |d_real| values with P(clears) in [eps,1-eps],")
    P("  read off the cell's own enumerated population.  Width is in dSharpe units; the ratio")
    P("  column divides it by the mean |dSharpe| actually being tested across the 180 cells.")
    mean_eff = float(EXACT.absd_S.mean())
    zrows = []
    for rule in ("MAXN", "PVAL"):
        for kap in KAPPAS:
            for eps in EPSILONS:
                w, undet = [], []
                for k in NULL:
                    a = np.sort(np.abs(NULL[k]["dS"]))
                    _, _, ww = zone_bounds(a, kap, eps, rule)
                    w.append(ww)
                pc = EXACT[f"p{rule}{kap}_S"].values
                undet = float(np.mean((pc >= eps) & (pc <= 1 - eps)))
                zrows.append(dict(rule=rule, n_draw=kap, eps=eps,
                                  mean_zone_width=float(np.mean(w)),
                                  median_zone_width=float(np.median(w)),
                                  zone_over_mean_effect=float(np.mean(w)) / mean_eff,
                                  frac_cells_undetermined=undet))
    ZONE = pd.DataFrame(zrows)
    P(f"\n  mean |dSharpe| under test across the 180 cells = {mean_eff:.4f}")
    P("\n" + ZONE.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    GRID = FLIP.merge(ZONE, on=["rule", "n_draw"], how="outer")
    GRID.to_csv(OUT / f"{STEM}.grid.csv", index=False)

    # ============================================================ Q3  rule 8, the clause as gate
    P("\n" + "=" * 118)
    P("Q3  RULE 8 -- the clause as a SELECTION GATE at each draw count")
    P("=" * 118)
    P("  Cell = (panel, family, cost rung) = 18.  Menu = the 10 (threshold, depth) configs.")
    P("  Pick on IS <= 2016-12-31 by largest IS dSharpe among configs whose IS effect CLEARS")
    P("  the clause; if none clears, ABSTAIN and hold the control book (idea 194's convention).")
    P(f"  {N_SEEDS} independent draw regimes per (cell, rule, n); ENUM = the exact population.")
    rng = np.random.default_rng(SEED)
    cells = sorted({(k[0], k[1], k[4]) for k in REAL})
    wrows = []

    def read_oos(key):
        rv = REAL[key]
        return rv["Sharpe_OOS"], rv["CAGR_OOS"], rv["MaxDD_OOS"]

    for (pi, fam, bps) in cells:
        menu = [k for k in REAL if k[0] == pi and k[1] == fam and k[4] == bps]
        c = CTRL[pi][bps]
        s0 = (c["Sharpe_OOS"], c["CAGR_OOS"], c["MaxDD_OOS"])
        # unfiltered argmax on IS margin (no clause at all)
        best = max(menu, key=lambda k: REAL[k]["dSharpe_IS"])
        wrows.append(dict(panel=PANS[pi].name, family=fam, bps=bps, rule="NONE", n_draw=0,
                          seed=-1, abstain=False, pick=f"{REAL[best]['thr']}/"
                          f"{REAL[best]['depth']}",
                          Sharpe_OOS=read_oos(best)[0], CAGR_OOS=read_oos(best)[1],
                          MaxDD_OOS=read_oos(best)[2],
                          ctrl_Sharpe_OOS=s0[0], ctrl_CAGR_OOS=s0[1], ctrl_MaxDD_OOS=s0[2]))
        # do-nothing control
        wrows.append(dict(panel=PANS[pi].name, family=fam, bps=bps, rule="S0", n_draw=0,
                          seed=-1, abstain=True, pick="-",
                          Sharpe_OOS=s0[0], CAGR_OOS=s0[1], MaxDD_OOS=s0[2],
                          ctrl_Sharpe_OOS=s0[0], ctrl_CAGR_OOS=s0[1], ctrl_MaxDD_OOS=s0[2]))
        # exact-population gate
        for rule in ("MAXN", "PVAL", "ENUM"):
            kaps = [0] if rule == "ENUM" else KAPPAS
            for kap in kaps:
                for sd in range(1 if rule == "ENUM" else N_SEEDS):
                    adm = []
                    for k in menu:
                        a = np.abs(NULL[k]["dIS"])
                        real_abs = abs(REAL[k]["dSharpe_IS"])
                        N = len(a)
                        if rule == "ENUM":
                            clears = truth_pval(int((a < real_abs).sum()), N)
                        else:
                            dr = a[rng.choice(N, size=kap, replace=False)]
                            if rule == "MAXN":
                                clears = real_abs > dr.max()
                            else:
                                R = int((dr >= real_abs).sum())
                                clears = (R + 1) / (kap + 1) <= ALPHA
                        if clears:
                            adm.append(k)
                    if adm:
                        pk = max(adm, key=lambda k: REAL[k]["dSharpe_IS"])
                        so, co, do = read_oos(pk)
                        lab = f"{REAL[pk]['thr']}/{REAL[pk]['depth']}"
                    else:
                        so, co, do = s0
                        lab = "-"
                    wrows.append(dict(panel=PANS[pi].name, family=fam, bps=bps, rule=rule,
                                      n_draw=kap, seed=sd, abstain=not adm, pick=lab,
                                      Sharpe_OOS=so, CAGR_OOS=co, MaxDD_OOS=do,
                                      ctrl_Sharpe_OOS=s0[0], ctrl_CAGR_OOS=s0[1],
                                      ctrl_MaxDD_OOS=s0[2]))
    WF = pd.DataFrame(wrows)
    WF["dOOS"] = WF.Sharpe_OOS - WF.ctrl_Sharpe_OOS
    WF.to_csv(OUT / f"{STEM}.walkforward.csv.gz", index=False)   # 29k rows: gzipped
    agg = (WF.groupby(["rule", "n_draw"])
             .agg(n=("dOOS", "size"), abstain_rate=("abstain", "mean"),
                  mean_Sharpe_OOS=("Sharpe_OOS", "mean"), mean_CAGR_OOS=("CAGR_OOS", "mean"),
                  mean_MaxDD_OOS=("MaxDD_OOS", "mean"), mean_dOOS=("dOOS", "mean"),
                  t_dOOS=("dOOS", lambda x: p191.tstat(list(x))),
                  win_rate=("dOOS", lambda x: float((np.asarray(x) > 1e-12).mean())))
             .reset_index())
    P("\n  OOS window 2017-2026, mean across 18 cells (x seeds):")
    P(agg.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("\n  per-seed spread of the mean OOS Sharpe (how much the DRAW alone moves the answer):")
    sp = (WF[WF.rule.isin(["MAXN", "PVAL"])].groupby(["rule", "n_draw", "seed"])
            .Sharpe_OOS.mean().groupby(level=[0, 1])
            .agg(["min", "median", "max", "std"]).reset_index())
    sp["range"] = sp["max"] - sp["min"]
    P(sp.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("\n  reference OOS (2017-2026), per panel:")
    P(BASE[["panel", "name", "CAGR_OOS", "Sharpe_OOS", "MaxDD_OOS"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ============================================================ KEEP paths
    P("\n" + "=" * 118)
    P("PROTOCOL 4 -- KEEP paths on the 180 real overlay rows, crossed with the clause verdict")
    P("=" * 118)
    K4 = EXACT.copy()
    P(f"  4a passes: {int(K4.pass4a.sum())}/{len(K4)}    "
      f"4b passes: {int(K4.pass4b.sum())}/{len(K4)}")
    krows = []
    for rule in ("MAXN", "PVAL"):
        for kap in KAPPAS:
            p = K4[f"p{rule}{kap}_S"]
            for path, msk in (("4a", K4.pass4a), ("4b", K4.pass4b)):
                sub = p[msk]
                krows.append(dict(rule=rule, n_draw=kap, path=path, passes=int(msk.sum()),
                                  clear_with_P1=int((sub > 1 - 1e-12).sum()),
                                  never_clear=int((sub < 1e-12).sum()),
                                  undetermined=int(((sub >= 0.10) & (sub <= 0.90)).sum()),
                                  E_clearing=float(sub.sum())))
    KEEP = pd.DataFrame(krows)
    P("\n" + KEEP.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    KEEP.to_csv(OUT / f"{STEM}.keep.csv", index=False)
    P("\n  4b passes by panel/family:")
    P(K4[K4.pass4b].groupby(["panel", "family"]).size().to_string())
    P("\n  4b failure reasons across all 180 rows:")
    P(str(K4.fail4b.value_counts().to_dict()))
    P("\n  This idea proposes NO book: it is a PROTOCOL measurement, so neither KEEP path is")
    P("  claimable by it.  The 180 real rows are idea 191's, re-priced against a fully")
    P("  enumerated null.")

    # ============================================================ predictions
    P("\n" + "=" * 118)
    P("PRE-REGISTERED PREDICTIONS")
    P("=" * 118)
    m20 = float(SZ[SZ.n_draw == 20].measured_size.iloc[0])
    m200 = float(SZ[SZ.n_draw == 200].measured_size.iloc[0])
    p1 = bool(np.all(np.abs(SZ.measured_size - SZ.nominal_1_over_np1) < 0.005))
    fp = FLIP[(FLIP.rule == "PVAL") & (FLIP.stat == "S")].set_index("n_draw")
    p2 = bool(fp.flip_vs_truth.is_monotonic_decreasing and fp.loc[200, "flip_vs_truth"] >= 0.02)
    z = ZONE[(ZONE.rule == "PVAL") & (ZONE.eps == 0.10)].set_index("n_draw")
    p3 = bool(z.loc[20, "mean_zone_width"] / max(z.loc[200, "mean_zone_width"], 1e-12) >= 3.0
              and z.loc[200, "zone_over_mean_effect"] >= 0.50)
    gate = agg[agg.rule.isin(["MAXN", "PVAL", "ENUM", "NONE"])]
    p4 = bool((gate.mean_dOOS <= 1e-12).all())
    u20 = float(ZONE[(ZONE.rule == "MAXN") & (ZONE.n_draw == 20)
                     & (ZONE.eps == 0.10)].frac_cells_undetermined.iloc[0])
    p5 = bool(u20 >= 0.80)
    for tag, hit, note in (
        ("P1 incumbent clause size == 1/(n+1) at every n (+-0.005)", p1,
         f"n=20 {m20:.5f} vs {1/21:.5f}; n=200 {m200:.5f} vs {1/201:.5f}"),
        ("P2 level-alpha flip rate falls in n but is >= 2% at n=200", p2,
         f"n=20 {fp.loc[20,'flip_vs_truth']:.4f} -> n=200 {fp.loc[200,'flip_vs_truth']:.4f}"),
        ("P3 zone width shrinks >=3x from n=20 to 200, still >=50% of effect", p3,
         f"{z.loc[20,'mean_zone_width']:.4f} -> {z.loc[200,'mean_zone_width']:.4f} "
         f"({z.loc[200,'zone_over_mean_effect']:.1%} of the effect)"),
        ("P4 no clause-gated selector beats do-nothing OOS", p4,
         f"best mean dOOS {gate.mean_dOOS.max():+.4f}"),
        ("P5 >=80% of the 180 cells UNDETERMINED at n=20, eps=0.10", p5,
         f"{u20:.1%}")):
        P(f"  {'HIT ' if hit else 'MISS'}  {tag:<62s} {note}")
    P(f"\n  {sum([p1, p2, p3, p4, p5])} of 5 predictions hit.")
    P(f"\ndone in {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()

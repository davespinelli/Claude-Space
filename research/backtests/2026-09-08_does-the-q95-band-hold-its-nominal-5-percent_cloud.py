#!/usr/bin/env python3
"""Idea 214 — does the Q95 band hold its nominal 5 percent?

QUESTION (queue 214, following ideas 191/207/216)
    Idea 207 recommends replacing clause 11b's MAX band with a Q95 band at 100 draws.  A
    quantile's NOMINAL size is only its REALISED size if the draws are exchangeable with the
    real arm, and neighbouring circular rotations are strongly correlated.  Run idea 191's
    known-null NOISE arm — an episodic Bernoulli ON series with ZERO information — through
    the Q95/K=100 band on all three panels and report the realised false-positive rate
    against 5%.  If it is not 5%, clause 11b needs a CALIBRATED quantile, not a nominal one.

TWO THINGS ARE BEING SEPARATED, AND THE RECORD HAS ONLY EVER MEASURED ONE
    (1) COMBINATORIAL size.  Under exact exchangeability the rank of the real statistic
        among {real} U {K rotations} is uniform on 1..K+1, so a band set at the r-th order
        statistic of the K draws has size EXACTLY
              size_exch(band, K) = (K + 1 - r) / (K + 1),      r = ceil(0.95 K) for Q95.
        At K=100 that is 6/101 = 5.94%, NOT 5%; at K=20 (r=19) it is 2/21 = 9.52%.  So the
        name "Q95" already misstates the target by 19% at K=100 and by 90% at K=20, before
        any data is seen.  This is arithmetic and needs no run.
    (2) REALISED size.  Rotating an ON indicator moves which market episodes it covers, so
        exchangeability holds only if the return process is stationary.  It is not.  This
        run measures the realised rate on books with a known-zero effect.

METHOD
    For each (panel, target on-share, replicate) a zero-information NOISE overlay is built
    with idea 191's `noise_state` (episode length matched to the real overlays' median) and
    priced with idea 191's machinery, verbatim.  A POOL of D=200 distinct circular rotations
    of that same ON series is priced too.  Then, for every (band, K), the realised size is
    EXACT given the pool: a uniformly random K-subset of a uniformly random D-subset of the
    N rotations is a uniformly random K-subset of the N, so
        P(clears | band, K) = HypergeomCDF(K - r ; D, M, K),
        M = #{pool draws at least as extreme as the real}
    and no subset resampling is needed.  Sizes are reported against BOTH the combinatorial
    size_exch above and the 5% target the clause names.

PARAMETERS (2, swept, ALL grid points reported)
    p1  K      in {20, 50, 100, 200}
    p2  share  in {0.15, 0.30, 0.50, 0.70}   (target on-share of the null overlay)
    Bands MAX and Q95 are both reported at every point; depth (0.5), cost rung (10 bps,
    PROTOCOL), episode length (matched to the real overlays) and D=200 are FIXED, not tuned.

RULE 8 (required)  The proposed fix is a CALIBRATED quantile.  Calibrate it: on the IS
    window (<= 2016-12-31) find, for each K, the smallest order statistic r* whose realised
    size is <= 5%; then apply that r* to the 2017-2026 window, read once, and report whether
    the calibrated band holds 5% out of sample and whether it beats the nominal Q95 there.

BOTH KEEP PATHS are reported for every NOISE arm and every panel control — a known-null
    book's 4a/4b pass rate is the cleanest available reading of what those bars measure.

SURVIVORSHIP: idea 191's build_panels drops SMALL439 names with max_1d_move >= 1.0 and the
panel is current constituents of a sub-$2B screen only; BROAD136 is current constituents of
a large-cap list.

Outputs (committed): .console.txt .arms.csv .pool.csv .size.csv .autocorr.csv
                     .walkforward.csv .keep.csv .result.md
Deterministic (no hash()-seeded RNG); no network; no scipy.
"""
import sys, time, importlib.util
from math import lgamma
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import metrics  # noqa

STAMP = "2026-09-08_does-the-q95-band-hold-its-nominal-5-percent_cloud"
P191_STEM = "2026-09-05_the-on-share-column_cloud"

SHARES = [0.15, 0.30, 0.50, 0.70]          # p2
KS = [20, 50, 100, 200]                    # p1
BANDS = ["MAX", "Q95"]
D_POOL = 200                               # rotations priced per arm (fixed, not tuned)
N_REP = 8                                  # replicate noise series per (panel, share)
DEPTH = 0.5
BPS = 10                                   # PROTOCOL rung
SEED = 214_000

_LOG: list[str] = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); _LOG.append(s)


# ============================================================ exact hypergeometric law
_LG = {}
def _lgam(n):
    v = _LG.get(n)
    if v is None:
        v = lgamma(n + 1.0); _LG[n] = v
    return v

def logC(n, k):
    if k < 0 or k > n or n < 0: return -np.inf
    return _lgam(n) - _lgam(k) - _lgam(n - k)

def hyp_cdf(x, N, M, K):
    N, M, K = int(N), int(M), int(K)
    if x < 0: return 0.0
    hi = int(min(x, M, K))
    if hi < 0: return 0.0
    lden = logC(N, K)
    if not np.isfinite(lden): return np.nan
    tot = 0.0
    for i in range(hi + 1):
        tot += np.exp(logC(M, i) + logC(N - M, K - i) - lden)
    return float(min(max(tot, 0.0), 1.0))

def r_of(band, K):
    return K if band == "MAX" else int(np.ceil(0.95 * K))

def size_exch(band, K):
    """Size under EXACT exchangeability: P(rank of the real among K+1 exceeds r)."""
    return (K + 1 - r_of(band, K)) / (K + 1)

def p_clears(band, K, D, M):
    return hyp_cdf(K - r_of(band, K), D, M, K)


# ============================================================ light-weight metrics
def sharpe(r):
    v = r.std()
    return float(r.mean() * 252 / (v * np.sqrt(252))) if v > 0 else np.nan

def maxdd(r):
    eq = (1.0 + r).cumprod()
    return float((eq / np.maximum.accumulate(eq) - 1.0).min())


def main():
    t0 = time.time()
    spec = importlib.util.spec_from_file_location("p191", OUT / f"{P191_STEM}.py")
    p191 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(p191)
    p191.P = P
    FREQ, IS_END, OOS_START = p191.FREQ, p191.IS_END, p191.OOS_START
    from baseline import rules_v2_weights

    P("=" * 100)
    P("IDEA 214 — realised size of the Q95 band on a KNOWN-NULL (zero-information) overlay")
    P("=" * 100)
    P("\nPART 0 — the COMBINATORIAL size, which is arithmetic and already off the stated target")
    P(f"{'band':>5} {'K':>5} {'r':>5} {'size_exch':>10}  {'vs the 5% the clause names':>28}")
    for band in BANDS:
        for K in KS:
            se = size_exch(band, K)
            P(f"{band:>5} {K:>5} {r_of(band,K):>5} {se:>10.4f}  {se/0.05:>27.2f}x")

    PANS = p191.build_panels()

    # episode length matched to the real overlays, exactly as idea 191 does
    ep_lens = []
    for pan in PANS:
        for fam in p191.FAM_ORDER:
            _, thrs, _, _ = p191.FAMILIES[fam]
            for thr in thrs:
                s = np.asarray(p191.on_indicator(pan, fam, thr))
                sw = p191.circ_switches(s)
                if sw > 0 and s.sum() > 0:
                    ep_lens.append(2.0 * s.sum() / sw)
    EP = float(np.median(ep_lens))
    P(f"\nnoise episode length matched to the real overlays' median: {EP:.2f} rebalances "
      f"(from {len(ep_lens)} real ON series)")

    # panel-level comparands
    CTRL, SPY, V2 = {}, {}, {}
    for pan in PANS:
        cr = p191.net(pan._r0, BPS).loc[pan.start:]
        CTRL[pan.name] = cr
        SPY[pan.name] = pan.spy.loc[pan.start:]
        v2 = p191.fast_backtest(pan.px, rules_v2_weights(pan.px), 0.0, FREQ)
        V2[pan.name] = p191.net(v2, BPS).loc[pan.start:]
        P(f"  {pan.name}: control {sharpe(cr):.4f}/{maxdd(cr):.4f} | SPY "
          f"{sharpe(SPY[pan.name]):.4f}/{maxdd(SPY[pan.name]):.4f} | RULES v2 "
          f"{sharpe(V2[pan.name]):.4f}/{maxdd(V2[pan.name]):.4f}")

    # ------------------------------------------------------------------ price the corpus
    P(f"\nPRICING {len(PANS)*len(SHARES)*N_REP} known-null arms x (1 real + {D_POOL} rotations)")
    arms, pool_rows = [], []
    for pan in PANS:
        J = len(pan.reb)
        cr = CTRL[pan.name]
        c_full, c_is, c_oos = (sharpe(cr), sharpe(cr.loc[:IS_END]), sharpe(cr.loc[OOS_START:]))
        c_dd = maxdd(cr)
        for tgt in SHARES:
            for rep in range(N_REP):
                sd = SEED + int(tgt * 1000) * 97 + rep * 7 + {"U56": 1, "BROAD136": 2,
                                                              "SMALL439": 3}[pan.name] * 100003
                rng = np.random.default_rng(sd)
                s_real = p191.noise_state(J, tgt, EP, rng)
                offs = np.random.default_rng(sd + 1).permutation(np.arange(1, J))[:D_POOL]
                stats = []
                for kind, off, s in ([("real", 0, s_real)]
                                     + [("null", int(o), np.roll(s_real, int(o))) for o in offs]):
                    W, mask = p191.apply_overlay(pan, "NOISE", DEPTH, s)
                    res = p191.fast_backtest(pan.px, W, 0.0, FREQ, mask=mask)
                    r = p191.net(res, BPS).loc[pan.start:]
                    st = dict(kind=kind, offset=off, on_share=float(s.mean()),
                              dS=sharpe(r) - c_full,
                              dS_IS=sharpe(r.loc[:IS_END]) - c_is,
                              dS_OOS=sharpe(r.loc[OOS_START:]) - c_oos,
                              dDD=maxdd(r) - c_dd)
                    if kind == "real":
                        m = metrics(r)
                        st.update(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                  OOS_Sharpe=sharpe(r.loc[OOS_START:]),
                                  OOS_CAGR=metrics(r.loc[OOS_START:])["CAGR"],
                                  OOS_MaxDD=maxdd(r.loc[OOS_START:]),
                                  fail4a=p191.keep_4a(r, V2[pan.name]),
                                  fail4b=p191.keep_4b(r, SPY[pan.name]))
                    stats.append(st)
                real = stats[0]; nulls = stats[1:]
                a = dict(panel=pan.name, share=tgt, rep=rep, seed=sd, J=J, D=len(nulls),
                         on_share=real["on_share"],
                         switches=p191.circ_switches(s_real),
                         dS=real["dS"], dS_IS=real["dS_IS"], dS_OOS=real["dS_OOS"],
                         dDD=real["dDD"], CAGR=real["CAGR"], Sharpe=real["Sharpe"],
                         MaxDD=real["MaxDD"], OOS_Sharpe=real["OOS_Sharpe"],
                         OOS_CAGR=real["OOS_CAGR"], OOS_MaxDD=real["OOS_MaxDD"],
                         fail4a=real["fail4a"], fail4b=real["fail4b"])
                for lab, key in [("S", "dS"), ("IS", "dS_IS"), ("OOS", "dS_OOS"), ("DD", "dDD")]:
                    nv = np.abs([n[key] for n in nulls])
                    a[f"M_{lab}"] = int((nv >= abs(real[key])).sum())
                    a[f"nullmed_{lab}"] = float(np.median(nv))
                arms.append(a)
                for n in nulls:
                    pool_rows.append(dict(panel=pan.name, share=tgt, rep=rep, offset=n["offset"],
                                          dS=n["dS"], dS_IS=n["dS_IS"], dS_OOS=n["dS_OOS"],
                                          dDD=n["dDD"]))
        P(f"    {pan.name} done ({time.time()-t0:.0f}s)")
    A = pd.DataFrame(arms); PL = pd.DataFrame(pool_rows)
    A.to_csv(OUT / f"{STAMP}.arms.csv", index=False)
    PL.to_csv(OUT / f"{STAMP}.pool.csv", index=False)
    P(f"  {len(A)} known-null arms, {len(PL)} priced rotations, {time.time()-t0:.0f}s")

    # ------------------------------------------------------------------ realised size
    P("\n" + "=" * 100)
    P("PART 1 — REALISED SIZE of the clause on a ZERO-EFFECT overlay (ALL grid points)")
    P("=" * 100)
    rows = []
    for band in BANDS:
        for K in [k for k in KS if k <= D_POOL]:
            for lab in ["S", "DD", "IS", "OOS"]:
                p = np.array([p_clears(band, K, d, m) for d, m in zip(A.D, A[f"M_{lab}"])])
                rows.append(dict(band=band, K=K, stat=lab, arms=len(A),
                                 realised=float(p.mean()), se=float(p.std(ddof=1)/np.sqrt(len(p))),
                                 size_exch=size_exch(band, K), target=0.05,
                                 ratio_vs_exch=float(p.mean()) / size_exch(band, K),
                                 ratio_vs_target=float(p.mean()) / 0.05))
    SZ = pd.DataFrame(rows)
    SZ.to_csv(OUT / f"{STAMP}.size.csv", index=False)
    P(SZ.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    q = SZ[(SZ.band == "Q95") & (SZ.K == 100) & (SZ.stat == "S")].iloc[0]
    P(f"\n>>> HEADLINE: Q95/K=100 on the full-sample Sharpe statistic — realised "
      f"{q.realised:.4f} (se {q.se:.4f}) against a combinatorial {q.size_exch:.4f} and the "
      f"clause's stated {0.05:.4f}: {q.ratio_vs_target:.2f}x the target, "
      f"{q.ratio_vs_exch:.2f}x its own exchangeability size")
    m20 = SZ[(SZ.band == "MAX") & (SZ.K == 20) & (SZ.stat == "S")].iloc[0]
    P(f">>> the incumbent MAX/K=20: realised {m20.realised:.4f} against exchangeability "
      f"{m20.size_exch:.4f} ({m20.ratio_vs_exch:.2f}x)")
    P("\nby panel (Q95/K=100, full-sample Sharpe):")
    for pn, g in A.groupby("panel"):
        p = np.array([p_clears("Q95", 100, d, m) for d, m in zip(g.D, g.M_S)])
        P(f"  {pn:9s} realised {p.mean():.4f} over {len(g)} arms")
    P("\nby target on-share (Q95/K=100, full-sample Sharpe):")
    for sh, g in A.groupby("share"):
        p = np.array([p_clears("Q95", 100, d, m) for d, m in zip(g.D, g.M_S)])
        P(f"  share {sh:.2f}  realised on-share {g.on_share.mean():.3f}  size {p.mean():.4f} "
          f"over {len(g)} arms")

    # ------------------------------------------------- mechanism: rotation autocorrelation
    P("\n" + "=" * 100)
    P("PART 2 — MECHANISM: are neighbouring rotations exchangeable draws?")
    P("=" * 100)
    ac = []
    for (pn, sh, rep), g in PL.groupby(["panel", "share", "rep"]):
        o = g.offset.values.astype(float); v = g.dS.values
        J = int(A[(A.panel == pn) & (A.share == sh) & (A.rep == rep)].J.iloc[0])
        i, jx = np.triu_indices(len(o), 1)
        dist = np.abs(o[i] - o[jx]); dist = np.minimum(dist, J - dist)     # circular distance
        prod = (v[i] - v.mean()) * (v[jx] - v.mean())
        var = v.var()
        for lo, hi in [(0, 5), (5, 10), (10, 25), (25, 50), (50, 100), (100, 250), (250, 1e9)]:
            m = (dist >= lo) & (dist < hi)
            if m.sum() >= 5:
                ac.append(dict(panel=pn, share=sh, rep=rep, lo=lo, hi=hi, n=int(m.sum()),
                               rho=float(prod[m].mean() / var) if var > 0 else np.nan))
    AC = pd.DataFrame(ac)
    AC.to_csv(OUT / f"{STAMP}.autocorr.csv", index=False)
    P("correlation of the null statistic between two rotations, by circular offset distance:")
    P(AC.groupby(["lo", "hi"]).agg(mean_rho=("rho", "mean"), pairs=("n", "sum"),
                                   cells=("rho", "size")).to_string(
        float_format=lambda x: f"{x:+.4f}"))
    P("per panel (distance >= 250 rebalances, i.e. 'far apart' draws):")
    P(AC[AC.lo == 250].groupby("panel").rho.agg(["mean", "size"]).to_string(
        float_format=lambda x: f"{x:+.4f}"))
    P("\nposition of the REAL arm's |dS| inside its own pool (uniform under exchangeability):")
    for lab in ["S", "IS", "OOS", "DD"]:
        u = 1.0 - A[f"M_{lab}"] / A.D                        # empirical rank in [0,1]
        P(f"  {lab:>4}: mean {u.mean():.4f} (0.500 under exchangeability), "
          f"sd {u.std(ddof=1):.4f} (0.289), share above 0.95 {float((u > 0.95).mean()):.4f} "
          f"(0.050)")

    # ------------------------------------------------------------------- KEEP paths
    P("\n" + "=" * 100)
    P("BOTH KEEP PATHS on the known-null books")
    P("=" * 100)
    A["pass4a"] = A.fail4a == "-"; A["pass4b"] = A.fail4b == "-"
    P(f"  a ZERO-INFORMATION overlay clears 4a in {int(A.pass4a.sum())}/{len(A)} and 4b in "
      f"{int(A.pass4b.sum())}/{len(A)}; BOTH {int((A.pass4a & A.pass4b).sum())}/{len(A)}")
    P(A.groupby("panel").agg(arms=("pass4b", "size"), pass4a=("pass4a", "sum"),
                             pass4b=("pass4b", "sum"), CAGR=("CAGR", "mean"),
                             Sharpe=("Sharpe", "mean"), MaxDD=("MaxDD", "mean"),
                             OOS_Sharpe=("OOS_Sharpe", "mean")).to_string(
        float_format=lambda x: f"{x:.4f}"))
    P("binding 4b bars on the null books:")
    P(A[~A.pass4b].fail4b.value_counts().head(8).to_string())
    for pan in PANS:
        c = CTRL[pan.name]
        P(f"  {pan.name} untreated control: 4a {p191.keep_4a(c, V2[pan.name])} | "
          f"4b {p191.keep_4b(c, SPY[pan.name])}")
    A.to_csv(OUT / f"{STAMP}.keep.csv", index=False)

    # ------------------------------------------------------------------- rule 8
    P("\n" + "=" * 100)
    P(f"RULE 8 — CALIBRATE the quantile on IS (<= {IS_END}) and read {OOS_START}+ ONCE")
    P("=" * 100)
    wf = []
    for K in [k for k in KS if k <= D_POOL]:
        # IS: smallest r whose IS realised size is <= 5%
        r_star, is_at_star = None, None
        for r in range(1, K + 1):
            p = np.array([hyp_cdf(K - r, d, m, K) for d, m in zip(A.D, A.M_IS)]).mean()
            if p <= 0.05:
                r_star, is_at_star = r, float(p); break
        r_nom = r_of("Q95", K)
        is_nom = float(np.array([hyp_cdf(K - r_nom, d, m, K)
                                 for d, m in zip(A.D, A.M_IS)]).mean())
        oos_nom = float(np.array([hyp_cdf(K - r_nom, d, m, K)
                                  for d, m in zip(A.D, A.M_OOS)]).mean())
        oos_cal = (float(np.array([hyp_cdf(K - r_star, d, m, K)
                                   for d, m in zip(A.D, A.M_OOS)]).mean())
                   if r_star else np.nan)
        wf.append(dict(K=K, r_nominal_Q95=r_nom, IS_size_nominal=is_nom,
                       r_calibrated=r_star, IS_size_calibrated=is_at_star,
                       OOS_size_nominal=oos_nom, OOS_size_calibrated=oos_cal,
                       OOS_err_nominal=abs(oos_nom - 0.05),
                       OOS_err_calibrated=abs(oos_cal - 0.05) if r_star else np.nan))
        if r_star is None:
            P(f"  K={K}: NO order statistic of {K} draws attains 5% on IS — even the MAX band "
              f"over-fires; the pool cannot calibrate this rung.")
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    P(WF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    ok = WF.dropna(subset=["OOS_err_calibrated"])
    if len(ok):
        P(f"\n  the IS-calibrated quantile beats the nominal Q95 out of sample in "
          f"{int((ok.OOS_err_calibrated < ok.OOS_err_nominal).sum())}/{len(ok)} of the K rungs; "
          f"mean OOS error {ok.OOS_err_calibrated.mean():.4f} (calibrated) vs "
          f"{ok.OOS_err_nominal.mean():.4f} (nominal)")
    P("\n  OOS performance of the corpus (mean over the known-null arms, 10 bps):")
    P(f"    NOISE arms   OOS CAGR {A.OOS_CAGR.mean():.2%}  Sharpe {A.OOS_Sharpe.mean():.4f}  "
      f"MaxDD {A.OOS_MaxDD.mean():.2%}")
    for pan in PANS:
        c = CTRL[pan.name].loc[OOS_START:]; s = SPY[pan.name].loc[OOS_START:]
        v = V2[pan.name].loc[OOS_START:]
        P(f"    {pan.name:9s} control OOS {metrics(c)['CAGR']:.2%}/{sharpe(c):.4f}/{maxdd(c):.2%}"
          f" | SPY {metrics(s)['CAGR']:.2%}/{sharpe(s):.4f}/{maxdd(s):.2%}"
          f" | RULES v2 {metrics(v)['CAGR']:.2%}/{sharpe(v):.4f}/{maxdd(v):.2%}")

    P(f"\ntotal runtime {time.time()-t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()

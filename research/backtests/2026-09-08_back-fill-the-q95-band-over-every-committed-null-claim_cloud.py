#!/usr/bin/env python3
"""Idea 215 — back-fill the Q95 band over every committed rotation-null claim.

QUESTION (queue 215, following ideas 181/186/190/191/192/201/207/211/216)
    Idea 207 showed the MAX band at K=20 and a Q95 band at K=100 disagree on 26.7% of
    configurations.  Every rotation-null verdict the record has ever published was formed
    with the MAX band at whatever K its parent happened to draw.  This run re-reads those
    verdicts under Q95/K=100 and counts how many MOVE and IN WHICH DIRECTION.  The output
    is the size of the record's exposure to the statistic it happened to pick.

WHAT IS NEW HERE
    Idea 211 already re-read 1090 published verdicts under Q95 AT THE PUBLISHED K (216 ->
    300 clears).  That leaves the draw-count half of the question unanswered, because a
    Q95 band at K=20 and a Q95 band at K=100 are different estimators of different
    population quantiles: E[U_(r)] = r/(K+1), so the nominal-95% band sits at population
    quantile 0.905 at K=20 and 0.941 at K=100 — the smaller K CLEARS MORE OFTEN.  Going to
    K=100 therefore predicts REVOCATIONS among idea 211's grants, and this run measures the
    size of that correction exactly.

METHOD — NO MONTE CARLO IS NEEDED FOR THE BACK-FILL
    A rotation null's verdict depends on the K drawn rotations only through
        X = #{drawn rotations at least as extreme as the real effect}  ~  Hypergeom(N, M, K)
    where N is the number of non-identity rotations and M the number of them at least as
    extreme.  With the Q95 band defined as the r-th order statistic, r = ceil(0.95 K)
    (numpy's method="higher"; the MAX band is the same rule at r = K):
        clears(band, K)   <=>   X <= K - r
        P(clears | band, K) = HypergeomCDF(K - r; N, M, K)                       [exact]
    The committed enumeration of idea 207 (research/backtests/2026-09-05_clause-11b-draw-
    count-by-enumeration_cloud.exact.csv, 84,600 backtests) carries N and K_stat per claim,
    and idea 216 established M = N - K_stat.  So every (band, K) verdict is a computable
    probability, not a re-draw, and the back-fill is exact rather than sampled.

LEGS
    A  EXACT BACK-FILL (540 claims = idea 207's 180 committed rows x {Sharpe, MaxDD, IS}).
       Published verdict = idea 191's committed clause.csv (MAX band, K=20), joined on
       (panel, family, thr, depth, bps).  Reported against the record's own truth column
       (the exact permutation verdict at level 0.05).
    B  ARCHIVAL BACK-FILL AT PUBLISHED K (1090 claims from idea 211's committed reread.csv,
       covering ideas 181/190/201).  Only the published K is recoverable there; the K=100
       half is NOT, and the uncovered share is reported rather than guessed.
    C  COVERAGE CENSUS over every committed CSV: how many rotation-null claim rows the
       record holds and what share legs A and B reach.

PARAMETERS (2, swept, ALL grid points reported)
    p1  band in {MAX, Q95}
    p2  K    in {20, 50, 100, 200, 400}

RULE 8 (required) — clause-as-gate walk-forward on this run's OWN fresh numbers.
    The 180 real books are re-run from idea 191's machinery (reproduction gate against the
    committed columns).  In each cell the clause under (band, K) is applied to the IS
    window only, arms that fail it are dropped, the IS-Sharpe argmax of the survivors is
    taken, and 2017-2026 is read once.  Admission is drawn from the EXACT hypergeometric
    law above (R seeds), so the gate's randomness is the real one.  Comparands: S0
    do-nothing (the untreated control book), the UNGATED IS-argmax, ORACLE-OOS, RULES v2
    and SPY.

BOTH KEEP PATHS (4a vs the live book, 4b vs SPY) are reported for all 180 real arms.

SURVIVORSHIP: SMALL439 is current constituents of a sub-$2B screen only, with
max_1d_move >= 1.0 names dropped (idea 191's build_panels does this); BROAD136 is current
constituents of a large-cap list.  Panel orderings inherit that bias.

Outputs (committed): .console.txt .claims.csv .ladder.csv .archival.csv .census.csv
                     .walkforward.csv .keep.csv .result.md
Deterministic; no network; no scipy.
"""
import sys, re, glob, time, importlib.util
from math import lgamma
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import metrics  # noqa

STAMP = "2026-09-08_back-fill-the-q95-band-over-every-committed-null-claim_cloud"
ENUM = OUT / "2026-09-05_clause-11b-draw-count-by-enumeration_cloud.exact.csv"   # idea 207
PUB191 = OUT / "2026-09-05_the-on-share-column_cloud.clause.csv"                 # idea 191
REREAD = OUT / "2026-09-06_re-read-every-published-clause-on-the-signed-statistic_C.reread.csv"
P191_STEM = "2026-09-05_the-on-share-column_cloud"
KEYS = ["panel", "family", "thr", "depth", "bps"]
STATS = [("S", "clears", "Sharpe"), ("DD", "clearsDD", "MaxDD"), ("IS", "clears_IS", "IS Sharpe")]
BANDS = ["MAX", "Q95"]
KS = [20, 50, 100, 200, 400]
R_SEEDS = 200          # admission draws for the rule-8 gate (not a tuned parameter)
PUBLISHED_K = 20       # idea 191's committed N_NULL

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
    """P(X <= x) for X ~ Hypergeom(population N, successes M, draws K)."""
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
    """Order statistic used as the band: MAX = K-th, Q95 = ceil(0.95 K)-th (numpy 'higher')."""
    return K if band == "MAX" else int(np.ceil(0.95 * K))

def p_clears(band, K, N, M):
    """Exact probability that a K-draw `band` band is exceeded by the real effect."""
    return hyp_cdf(K - r_of(band, K), N, M, K)


# ==================================================================== LEG A: exact back-fill
def leg_a():
    P("=" * 100)
    P("LEG A — EXACT BACK-FILL over idea 207's committed enumeration (180 rows x 3 statistics)")
    P("=" * 100)
    EX = pd.read_csv(ENUM)
    PU = pd.read_csv(PUB191)
    P(f"  enumeration rows {len(EX)} | idea 191 published rows {len(PU)}")
    j = EX.merge(PU[KEYS + [c for _, c, _ in STATS]], on=KEYS, how="inner", validate="1:1")
    P(f"  joined on {KEYS}: {len(j)} rows -> {len(j)*len(STATS)} claims")

    rows = []
    for st, pubcol, label in STATS:
        for _, r in j.iterrows():
            N, Kstat = int(r[f"N_{st}"]), int(r[f"K_{st}"])
            M = N - Kstat                                   # idea 216's gate; re-checked below
            rows.append(dict(panel=r.panel, family=r.family, thr=r.thr, depth=r.depth,
                             bps=r.bps, stat=st, label=label, N=N, M=M, absd=r[f"absd_{st}"],
                             ties=r[f"ties_{st}"], truth=bool(r[f"truth_{st}"]),
                             published=bool(r[pubcol]), on_share=r.on_share,
                             degenerate=(M == 0 or M == N)))
    CL = pd.DataFrame(rows)
    P(f"  claims {len(CL)} | degenerate (M=0 or M=N; no draw count can move them) "
      f"{int(CL.degenerate.sum())} ({CL.degenerate.mean():.1%})")

    # ---- reproduction gate [g]: the closed form must reproduce the committed MAX-band p's
    errs = []
    for K in [20, 50, 100, 200]:
        for st, _, _ in STATS:
            sub = CL[CL.stat == st]
            got = np.array([p_clears("MAX", K, n, m) for n, m in zip(sub.N, sub.M)])
            want = EX.merge(PU[KEYS], on=KEYS)[f"pMAXN{K}_{st}"].values
            errs.append(np.nanmax(np.abs(got - want)))
    P(f"  [g] closed form vs idea 207's committed pMAXN{{20,50,100,200}}: max|d| {max(errs):.3e}"
      f"  (M = N - K_stat)")
    alt = []
    for st, _, _ in STATS:
        sub = CL[CL.stat == st]
        got = np.array([p_clears("MAX", 20, n, n - m) for n, m in zip(sub.N, sub.M)])
        want = EX.merge(PU[KEYS], on=KEYS)[f"pMAXN20_{st}"].values
        alt.append(np.nanmax(np.abs(got - want)))
    P(f"      the opposite convention (M = K_stat) is off by {max(alt):.3e} — the gate that "
      "fixes the sign")

    # ---- the (band, K) ladder
    P("\nALL GRID POINTS — P(clears) is exact, so every count below is an expectation over the "
      "draw, with the CERTAIN sub-count (p < 1e-9 or p > 1-1e-9) beside it")
    lad = []
    for band in BANDS:
        for K in KS:
            p = np.array([p_clears(band, K, n, m) for n, m in zip(CL.N, CL.M)])
            pub = CL.published.values.astype(float)
            tru = CL.truth.values.astype(float)
            certain_yes = p > 1 - 1e-9; certain_no = p < 1e-9
            grants = float(p[pub == 0].sum())                    # published NO  -> clears
            revoc = float((1 - p)[pub == 1].sum())               # published YES -> fails
            cert_grant = int(((pub == 0) & certain_yes).sum())
            cert_revoc = int(((pub == 1) & certain_no).sum())
            lad.append(dict(band=band, K=K, r=r_of(band, K), claims=len(CL),
                            E_clears=float(p.sum()), clear_rate=float(p.mean()),
                            E_moves=grants + revoc, E_grants=grants, E_revocations=revoc,
                            certain_grants=cert_grant, certain_revocations=cert_revoc,
                            undetermined=float(((p > 1e-9) & (p < 1 - 1e-9)).mean()),
                            err_vs_truth=float(np.abs(p - tru).mean()),
                            err_vs_truth_nondeg=float(
                                np.abs(p - tru)[~CL.degenerate.values].mean()),
                            agree_with_published=float((p * pub + (1 - p) * (1 - pub)).mean())))
    LAD = pd.DataFrame(lad)
    LAD.to_csv(OUT / f"{STAMP}.ladder.csv", index=False)
    P(LAD.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    pub_rate = CL.published.mean()
    P(f"\npublished reading (MAX band, K={PUBLISHED_K}): {int(CL.published.sum())}/{len(CL)} "
      f"clear ({pub_rate:.1%});  exact permutation truth at level 0.05: "
      f"{int(CL.truth.sum())}/{len(CL)} ({CL.truth.mean():.1%})")
    q100 = LAD[(LAD.band == "Q95") & (LAD.K == 100)].iloc[0]
    P(f">>> UNDER Q95/K=100: E[clears] {q100.E_clears:.1f}/{len(CL)} ({q100.clear_rate:.1%}), "
      f"E[moves vs published] {q100.E_moves:.1f} ({q100.E_moves/len(CL):.1%} of claims) = "
      f"{q100.E_grants:.1f} GRANTS + {q100.E_revocations:.1f} REVOCATIONS")
    q20 = LAD[(LAD.band == "Q95") & (LAD.K == 20)].iloc[0]
    P(f">>> the DRAW-COUNT half alone (Q95/K=20 -> Q95/K=100): E[clears] "
      f"{q20.E_clears:.1f} -> {q100.E_clears:.1f}, i.e. the record's exposure to K is "
      f"{q20.E_clears - q100.E_clears:+.1f} claims on top of the band change")

    # per-corpus split
    P("\nby panel and family (Q95/K=100 vs published MAX/K=20):")
    CL["p_q95_100"] = [p_clears("Q95", 100, n, m) for n, m in zip(CL.N, CL.M)]
    CL["p_max_20"] = [p_clears("MAX", 20, n, m) for n, m in zip(CL.N, CL.M)]
    CL["E_move"] = np.where(CL.published, 1 - CL.p_q95_100, CL.p_q95_100)
    g = CL.groupby(["panel", "family"]).agg(
        claims=("E_move", "size"), published=("published", "sum"), truth=("truth", "sum"),
        E_q95_100=("p_q95_100", "sum"), E_moves=("E_move", "sum"),
        degenerate=("degenerate", "sum"))
    P(g.to_string(float_format=lambda x: f"{x:.2f}"))
    P("\nby statistic:")
    P(CL.groupby("stat").agg(claims=("E_move", "size"), published=("published", "sum"),
                             truth=("truth", "sum"), E_q95_100=("p_q95_100", "sum"),
                             E_moves=("E_move", "sum"), degenerate=("degenerate", "sum")
                             ).to_string(float_format=lambda x: f"{x:.2f}"))
    CL.to_csv(OUT / f"{STAMP}.claims.csv", index=False)
    return CL, LAD


# ============================================================ LEG B: archival, published K
def leg_b():
    P("\n" + "=" * 100)
    P("LEG B — ARCHIVAL BACK-FILL at the PUBLISHED K (idea 211's committed 1090 verdicts)")
    P("=" * 100)
    if not REREAD.exists():
        P("  idea 211's reread.csv is not committed — leg skipped, 0 claims covered.")
        return pd.DataFrame()
    RR = pd.read_csv(REREAD)
    P(f"  rows {len(RR)}; corpora " + ", ".join(
        f"{c}({r},K={sorted(set(k))})" for (c, r), k in
        RR.groupby(["corpus", "ref"]).K.apply(list).items()))
    rep = int((RR.ABS_MAX.astype(bool) == RR.published.astype(bool)).sum())
    P(f"  [g] reproduction: ABS_MAX == published on {rep}/{len(RR)} rows")
    pub = RR.published.astype(bool); q95 = RR.ABS_Q95.astype(bool)
    mv = pub != q95
    P(f"  published clears {int(pub.sum())} ({pub.mean():.1%});  ABS_Q95 at the published K "
      f"{int(q95.sum())} ({q95.mean():.1%})")
    P(f"  >>> {int(mv.sum())} of {len(RR)} verdicts MOVE ({mv.mean():.1%}): "
      f"{int((~pub & q95).sum())} GRANTED, {int((pub & ~q95).sum())} REVOKED")
    tab = RR.assign(move=mv, grant=(~pub & q95), revoke=(pub & ~q95)).groupby(
        ["corpus", "ref", "stat_kind", "K"]).agg(
        claims=("move", "size"), published=("published", "sum"), q95=("ABS_Q95", "sum"),
        moves=("move", "sum"), granted=("grant", "sum"), revoked=("revoke", "sum"))
    P(tab.to_string())
    P("\n  K=100 IS NOT RECOVERABLE for these rows: only the band's max and the published-K "
      "verdicts are committed, not the draws.  Direction of the missing correction is taken "
      "from leg A, where both halves are exact.")
    RR.assign(move=mv).to_csv(OUT / f"{STAMP}.archival.csv", index=False)
    return RR


# ================================================================= LEG C: coverage census
CLEARS_PAT = re.compile(r"^(clears|p_?clears|clear|OOS_clears|clears_[A-Za-z0-9_]+|"
                        r"clears[A-Z][A-Za-z0-9_]*)$")
BANDCOL_PAT = re.compile(r"(band|null_max|null_absmax|null_q95|null_p95|q95)", re.I)

def leg_c():
    P("\n" + "=" * 100)
    P("LEG C — COVERAGE CENSUS: every committed CSV that publishes a rotation-null verdict")
    P("=" * 100)
    rows = []
    for f in sorted(glob.glob(str(OUT / "*.csv")) + glob.glob(str(OUT / "*.csv.gz"))):
        name = Path(f).name
        if name.startswith(STAMP):
            continue
        try:
            df = pd.read_csv(f, nrows=0)
        except Exception:
            continue
        cl = [c for c in df.columns if CLEARS_PAT.match(str(c))]
        bd = [c for c in df.columns if BANDCOL_PAT.search(str(c))]
        if not cl or not bd:
            continue
        try:
            n = len(pd.read_csv(f, usecols=[cl[0]]))
        except Exception:
            n = np.nan
        rows.append(dict(file=name, rows=n, n_clears_cols=len(cl),
                         clears_cols="|".join(map(str, cl[:6])),
                         band_cols="|".join(map(str, bd[:6])),
                         claims=n * len(cl) if np.isfinite(n) else np.nan))
    CS = pd.DataFrame(rows)
    CS.to_csv(OUT / f"{STAMP}.census.csv", index=False)
    tot = float(CS.claims.sum())
    P(f"  files publishing a rotation-null verdict beside a band: {len(CS)}")
    P(f"  published verdict cells in those files (rows x clears-columns): {tot:.0f}")
    P(f"  leg A reaches 540 exactly (the enumerated corpus); leg B reaches 1090 at the "
      f"published K -> {540 + 1090} of {tot:.0f} = {(540+1090)/tot:.1%} of the record's "
      "verdict cells, and only leg A's 540 can be moved to K=100 at all")
    P("\n  ten largest files by verdict cells:")
    P(CS.sort_values("claims", ascending=False).head(10)[
        ["file", "rows", "n_clears_cols", "claims"]].to_string(index=False))
    return CS


# ======================================================================= rule 8 + KEEP paths
def rule8_and_keep(CL):
    P("\n" + "=" * 100)
    P("FRESH RE-RUN of the 180 real books (idea 191's machinery), then RULE 8 clause-as-gate")
    P("=" * 100)
    spec = importlib.util.spec_from_file_location("p191", OUT / f"{P191_STEM}.py")
    p191 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(p191)
    p191.P = P
    FREQ, IS_END, OOS_START = p191.FREQ, p191.IS_END, p191.OOS_START
    COST_RUNGS = p191.COST_RUNGS
    t0 = time.time()
    PANS = p191.build_panels()

    CTRL, SPYS, V2 = [], [], []
    from baseline import rules_v2_weights
    for pan in PANS:
        d = {}
        for bps in COST_RUNGS:
            cr = p191.net(pan._r0, bps).loc[pan.start:]
            d[bps] = dict(r=cr, Sharpe=p191._sh(cr), IS=p191._sh(cr.loc[:IS_END]),
                          OOS=p191._sh(cr.loc[OOS_START:]),
                          OOS_CAGR=metrics(cr.loc[OOS_START:])["CAGR"],
                          OOS_MaxDD=metrics(cr.loc[OOS_START:])["MaxDD"])
        CTRL.append(d)
        SPYS.append(pan.spy.loc[pan.start:])
        v2 = p191.fast_backtest(pan.px, rules_v2_weights(pan.px), 0.0, FREQ)
        V2.append({b: p191.net(v2, b).loc[pan.start:] for b in COST_RUNGS})

    rows = []
    for pi, pan in enumerate(PANS):
        spy = SPYS[pi]
        for fam in p191.FAM_ORDER:
            _, thrs, _, depths = p191.FAMILIES[fam]
            for thr in thrs:
                s_real = p191.on_indicator(pan, fam, thr)
                for depth in depths:
                    W, mask = p191.apply_overlay(pan, fam, depth, s_real)
                    res = p191.fast_backtest(pan.px, W, 0.0, FREQ, mask=mask)
                    for bps in COST_RUNGS:
                        r = p191.net(res, bps).loc[pan.start:]
                        c = CTRL[pi][bps]
                        m, mo = metrics(r), metrics(r.loc[OOS_START:])
                        rows.append(dict(
                            panel=pan.name, family=fam, thr=thr, depth=str(depth), bps=bps,
                            Sharpe=m["Sharpe"], CAGR=m["CAGR"], MaxDD=m["MaxDD"],
                            IS_Sharpe=p191._sh(r.loc[:IS_END]),
                            OOS_Sharpe=p191._sh(r.loc[OOS_START:]),
                            OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"],
                            dS=m["Sharpe"] - c["Sharpe"],
                            fail4a=p191.keep_4a(r, V2[pi][bps]),
                            fail4b=p191.keep_4b(r, spy)))
    RB = pd.DataFrame(rows)
    RB["pass4a"] = RB.fail4a == "-"; RB["pass4b"] = RB.fail4b == "-"
    P(f"  re-ran {len(RB)} real arms in {time.time()-t0:.0f}s")

    # reproduction gate against idea 191's committed performance columns
    PU = pd.read_csv(PUB191)
    cmp_ = RB.merge(PU[KEYS + ["Sharpe", "dSharpe", "MaxDD"]], on=KEYS, suffixes=("", "_pub"))
    P(f"  [a] reproduction vs idea 191's committed columns: max|dSharpe| "
      f"{np.nanmax(np.abs(cmp_.Sharpe - cmp_.Sharpe_pub)):.3e}, max|dMaxDD| "
      f"{np.nanmax(np.abs(cmp_.MaxDD - cmp_.MaxDD_pub)):.3e} on {len(cmp_)} rows")

    P(f"\nBOTH KEEP PATHS on the 180 fresh real arms: 4a {int(RB.pass4a.sum())}/{len(RB)}, "
      f"4b {int(RB.pass4b.sum())}/{len(RB)}, BOTH "
      f"{int((RB.pass4a & RB.pass4b).sum())}/{len(RB)}")
    P(RB.groupby(["panel", "family"]).agg(arms=("pass4b", "size"), pass4a=("pass4a", "sum"),
                                          pass4b=("pass4b", "sum")).to_string())
    P("\nbinding 4b bars:")
    P(RB[~RB.pass4b].fail4b.value_counts().head(10).to_string())
    RB.to_csv(OUT / f"{STAMP}.keep.csv", index=False)

    # -------- how many of the 4b passes does the clause flag, under each (band, K)?
    IS_CL = CL[CL.stat == "IS"].set_index(KEYS)
    P("\n4b passes flagged by the IS-window clause under each (band, K)  "
      "[E = expectation over the draw]:")
    fl = []
    good = RB[RB.pass4b]
    for band in BANDS:
        for K in KS:
            e = 0.0
            for _, a in good.iterrows():
                k = (a.panel, a.family, a.thr, a.depth, a.bps)
                if k in IS_CL.index:
                    row = IS_CL.loc[k]
                    e += p_clears(band, K, row.N, row.M)
            fl.append(dict(band=band, K=K, pass4b=len(good), E_flagged=e))
    FL = pd.DataFrame(fl)
    P(FL.to_string(index=False, float_format=lambda x: f"{x:.2f}"))

    # ------------------------------------------------------------------- rule 8
    P("\nRULE 8 — clause-as-gate: admission drawn from the exact hypergeometric law, "
      f"{R_SEEDS} seeds; IS window <= {IS_END}, {OOS_START}+ read once")
    cells = RB.groupby(["panel", "family", "depth", "bps"])
    out = []
    rng_master = np.random.default_rng(215_000)
    for (pan, fam, depth, bps), g in cells:
        g = g.reset_index(drop=True)
        ctrl = CTRL[[p.name for p in PANS].index(pan)][bps]
        ps = {}
        for band in BANDS:
            for K in KS:
                pr = []
                for _, a in g.iterrows():
                    k = (a.panel, a.family, a.thr, a.depth, a.bps)
                    pr.append(p_clears(band, K, IS_CL.loc[k].N, IS_CL.loc[k].M)
                              if k in IS_CL.index else 0.0)
                ps[(band, K)] = np.array(pr)
        ung = g.loc[g.IS_Sharpe.idxmax()]
        orac = g.loc[g.OOS_Sharpe.idxmax()]
        row = dict(panel=pan, family=fam, depth=depth, bps=bps, arms=len(g),
                   S0_OOS=ctrl["OOS"], S0_OOS_CAGR=ctrl["OOS_CAGR"],
                   S0_OOS_MaxDD=ctrl["OOS_MaxDD"],
                   UNGATED_OOS=ung.OOS_Sharpe, ORACLE_OOS=orac.OOS_Sharpe)
        for (band, K), pr in ps.items():
            rng = np.random.default_rng(rng_master.integers(1 << 30))
            acc, absten = [], 0
            for _ in range(R_SEEDS):
                adm = rng.random(len(pr)) < pr
                if not adm.any():
                    acc.append(ctrl["OOS"]); absten += 1        # abstain -> do nothing
                else:
                    sub = g[adm]
                    acc.append(sub.loc[sub.IS_Sharpe.idxmax()].OOS_Sharpe)
            row[f"{band}{K}_OOS"] = float(np.mean(acc))
            row[f"{band}{K}_abstain"] = absten / R_SEEDS
        out.append(row)
    WF = pd.DataFrame(out)
    WF.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    P(f"  cells (panel x family x depth x cost rung): {len(WF)}")
    tab = []
    for band in BANDS:
        for K in KS:
            d = WF[f"{band}{K}_OOS"] - WF.S0_OOS
            n = len(d); sd = d.std(ddof=1)
            tab.append(dict(band=band, K=K, mean_OOS=WF[f"{band}{K}_OOS"].mean(),
                            d_vs_do_nothing=d.mean(),
                            t=d.mean() / (sd / np.sqrt(n)) if sd else np.nan,
                            wins=int((d > 0).sum()), cells=n,
                            mean_abstain=WF[f"{band}{K}_abstain"].mean(),
                            d_vs_ungated=(WF[f"{band}{K}_OOS"] - WF.UNGATED_OOS).mean()))
    T = pd.DataFrame(tab)
    P(T.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    du = WF.UNGATED_OOS - WF.S0_OOS; do = WF.ORACLE_OOS - WF.S0_OOS
    P(f"  do-nothing S0 mean OOS Sharpe {WF.S0_OOS.mean():.4f}; UNGATED IS-argmax "
      f"{du.mean():+.4f} (t {du.mean()/(du.std(ddof=1)/np.sqrt(len(du))):+.2f}); "
      f"ORACLE-OOS headroom {do.mean():+.4f}")
    spy_oos = {p.name: p191._sh(p.spy.loc[OOS_START:]) for p in PANS}
    P(f"  SPY OOS Sharpe by panel: " + ", ".join(f"{k} {v:.4f}" for k, v in spy_oos.items()))
    v2_oos = {p.name: p191._sh(V2[i][10].loc[OOS_START:]) for i, p in enumerate(PANS)}
    P(f"  RULES v2 OOS Sharpe by panel @10bps: " + ", ".join(f"{k} {v:.4f}" for k, v in v2_oos.items()))
    return RB, WF, T


# ========================================================================= main
def main():
    t0 = time.time()
    CL, LAD = leg_a()
    RR = leg_b()
    CS = leg_c()
    RB, WF, T = rule8_and_keep(CL)
    P(f"\ntotal runtime {time.time()-t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()

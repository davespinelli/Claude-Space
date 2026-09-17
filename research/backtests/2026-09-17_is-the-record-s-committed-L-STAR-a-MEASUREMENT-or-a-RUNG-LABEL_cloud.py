#!/usr/bin/env python3
"""Idea 1178 — is the record's committed L* a MEASUREMENT or a RUNG LABEL?

THE QUEUE'S PREMISE, QUOTED.  Idea 1170 found the ladder crossing L* seed-stable at
only 89 of 132 cells (0.674) while the LEVEL phi at the same frozen L is estimable at
0.811, and that only 0.172 of committed L* rows publish a denominator at all.  The
queue asks whether the 0.326 instability is the CROSSING (a threshold on a noisy curve)
or the LADDER (8 coarse rungs spanning three orders of magnitude), by re-running L* on
a log-dense rung set.

THE OBJECT.  For a book's realised daily return path r (length T) the moving-block
bootstrap null at block length L has median |MaxDD| = N(L).  N(1) is the iid null,
N(T) is (essentially) the observed path.  The record defines
    phi(L) = (N(L) - N(1)) / (OBSERVED - N(1)),
    L*     = the FIRST RUNG of the published ladder at which N(L) reaches OBSERVED.
L* is therefore a threshold crossing read off a ladder, and a threshold crossing read
off a ladder can only ever return a LADDER RUNG.  That is the whole question.

WHY THE RECORD'S OWN STATISTIC CANNOT SETTLE IT.  "L* identical at all S seeds" is a
statistic on RUNG LABELS.  Making the ladder denser strictly increases the number of
labels the crossing can land on, so exact-label agreement must FALL with density even
if the underlying crossing does not move at all.  Any honest test therefore needs a
density-INVARIANT reading of the same crossing.  This run publishes three, side by side:
    A  EXACT      the record's statistic: identical rung between two independent seed
                  groups (and identical rung at all S seeds, the 1170 form).
    B  COARSE-BIN both groups' L* fall in the same interval of the RECORD'S OWN coarse
                  ladder — density-invariant by construction.
    C  CONTINUOUS L*_cont, the crossing of phi(L) = 1 by log-linear interpolation
                  between the bracketing rungs.  This is a MEASUREMENT, not a label;
                  its dispersion across seed groups is reported in log units so it is
                  comparable across densities.
If the instability is the LADDER, A falls with density while B and C hold.  If it is
the CROSSING, C stays wide and no amount of density helps.

TUNED DIALS (2, PROTOCOL rule 4), every grid point reported:
  P1 RUNG DENSITY  D_COARSE (the record's [1,5,21,63,126,252,504,1008]+T, 9 rungs)
                   D_MED    (log ladder, ratio 2)
                   D_DENSE  (log ladder, ratio sqrt(2)) -- the queue's "log-dense" set
  P2 SEED COUNT    3 (the record's), 9, 27
Rung pools are computed ONCE on the union ladder, so the three densities and the three
seed counts read the SAME draws; nothing is re-randomised between grid points.

Seeds: a SEED is one independent ensemble of BDRAWS moving-block resamples at a rung.
A POOL of 54 seeds per (cell, rung) lets every seed count S be read as TWO DISJOINT
groups of S seeds, so agreement is measured between genuinely independent experiments.

Cells: 3 panels (MEGA/ETF 56, BROAD 136, SMALL sub-$2B) x 3 books = 9.  SMALL is
current-constituents only -> SURVIVORSHIP BIAS.

PROTOCOL compliance: 10 bps, weekly cadence, next-day execution (engine); ARM E runs
the rule-8 walk-forward on the same books and evaluates BOTH KEEP paths against the
live baseline and SPY.  Deterministic (fixed seed base).
"""
import sys, zlib
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score, compare  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics  # noqa

COST_BPS, FREQ = 10.0, "W"
BDRAWS, NPOOL = 300, 54
SEED_COUNTS = [3, 9, 27]
SEED_BASE = 11781178
L_COARSE = [1, 5, 21, 63, 126, 252, 504, 1008]      # the record's published ladder (+T)
COMMITTED_STABLE = 0.674                             # 1170: 89 of 132
pd.set_option("display.width", 220)
OUT = ROOT / "research" / "backtests"
STEM = "2026-09-17_is-the-record-s-committed-L-STAR-a-MEASUREMENT-or-a-RUNG-LABEL_cloud"
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# ------------------------------------------------------------------ panels & books
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    return px[[c for c in px.columns if c == "SPY" or c not in bad]]


def book_v2band(px):
    return rules_v2_weights(px, band=0.03, gross=0.75)


def book_top20(px):
    s, above, _ = score(px, vol_scale=False)
    cols = [c for c in px.columns if c != "SPY"]
    s = s[cols].where(above[cols])
    w = (s.rank(axis=1, ascending=False) <= 20).astype(float) * (0.75 / 20.0)
    return w.reindex(columns=px.columns).fillna(0.0)


def book_v1(px):
    return rules_v1_weights(px, n=5, w=0.15)


BOOKS = {"V2BAND": book_v2band, "TOP20EW": book_top20, "V1TOP5": book_v1}


# ------------------------------------------------------------------ null machinery
def maxdd_batch(a, L, n, rng, chunk=1500):
    """n moving-block resamples of the return array a at block length L -> |MaxDD| each.
    Chunked so the index matrix never exceeds a few hundred MB."""
    T = len(a)
    if L >= T:
        return np.full(n, _maxdd(a))
    nb = int(np.ceil(T / L))
    off = np.arange(L, dtype=np.int32)[None, None, :]
    out = np.empty(n)
    for lo in range(0, n, chunk):
        k = min(chunk, n - lo)
        st = rng.integers(0, T - L + 1, size=(k, nb)).astype(np.int32)
        idx = (st[:, :, None] + off).reshape(k, -1)[:, :T]
        eq = np.cumprod(1.0 + a[idx], axis=1)
        dd = eq / np.maximum.accumulate(eq, axis=1) - 1.0
        out[lo:lo + k] = -dd.min(axis=1)
    return out


def _maxdd(a):
    eq = np.cumprod(1.0 + a)
    return float(-(eq / np.maximum.accumulate(eq) - 1.0).min())


def log_ladder(T, ratio):
    """Log-spaced integer rungs from 1 to T at the given ratio, deduplicated."""
    L, x = [], 1.0
    while x < T:
        L.append(int(round(x)))
        x *= ratio
    return sorted(set(L + [T]))


def lstar_from(meds, rungs, obs, niid):
    """(rung L*, continuous L*) from one experiment's rung medians."""
    if abs(obs - niid) < 1e-12:
        return np.nan, np.nan
    # phi carries the sign of the denominator, so the record's reach condition
    #   sign(obs-niid) * (N(L)-niid) >= |obs-niid|
    # is exactly phi >= 1 on EITHER side.  (Multiplying by sign(obs-niid) a second
    # time would make phi(1)=0 "reach" whenever the iid null is the deeper one.)
    phi = [(m - niid) / (obs - niid) for m in meds]
    star = np.nan
    for L, p in zip(rungs, phi):
        if p >= 1.0 - 1e-12:
            star = float(L)
            break
    if not np.isfinite(star):
        return np.nan, np.nan
    i = rungs.index(int(star))
    if i == 0 or phi[i] == phi[i - 1]:
        return star, float(star)
    lo, hi = rungs[i - 1], rungs[i]
    f = (1.0 - phi[i - 1]) / (phi[i] - phi[i - 1])
    f = min(max(f, 0.0), 1.0)
    cont = float(np.exp(np.log(lo) + f * (np.log(hi) - np.log(lo))))
    return star, cont


def coarse_bin(L, T):
    """Which interval of the RECORD'S coarse ladder a value of L falls in."""
    edges = [x for x in L_COARSE if x < T] + [T]
    return int(np.searchsorted(edges, L, side="right"))


# ------------------------------------------------------------------ main
def main():
    panels = {"MEGA": load_universe(), "BROAD": load_universe(broad=True), "SMALL": small_panel()}
    series, cells = {}, []
    for pn, px in panels.items():
        start = px.index[260]
        for bn, fn in BOOKS.items():
            r = backtest(px, fn(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
            key = f"{pn}/{bn}"
            series[key] = r.values.astype(float)
            cells.append(dict(cell=key, panel=pn, book=bn, T=len(r), observed=_maxdd(r.values)))
    C = pd.DataFrame(cells)
    P("=" * 112)
    P("IDEA 1178 — is the record's committed L* a MEASUREMENT or a RUNG LABEL?")
    P(f"  cells {len(C)} (3 panels x 3 books)  |  seeds pooled {NPOOL} x {BDRAWS} draws "
      f"per rung  |  seed counts {SEED_COUNTS}  |  densities D_COARSE / D_MED / D_DENSE")
    P(f"  1170's committed statistic to beat: L* seed-stable at {COMMITTED_STABLE:.3f} "
      f"(89 of 132), i.e. 0.326 unstable")
    P("=" * 112)
    P(C.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---- rung pools: union ladder, one pool of NPOOL seed-medians per (cell, rung)
    P("\n## ARM A — building the seed pools on the UNION ladder (one draw set, all densities)")
    DENS, pools, ladders, denom_rows = {}, {}, {}, []
    for _, cr in C.iterrows():
        T = int(cr["T"])
        d = {"D_COARSE": sorted(set([L for L in L_COARSE if L < T] + [T])),
             "D_MED": log_ladder(T, 2.0),
             "D_DENSE": log_ladder(T, np.sqrt(2.0))}
        ladders[cr["cell"]] = d
        union = sorted(set(sum(d.values(), [])))
        a = series[cr["cell"]]
        M = np.empty((len(union), NPOOL))
        for i, L in enumerate(union):
            rng = np.random.default_rng(SEED_BASE + zlib.crc32(cr["cell"].encode()) % 10_000 + 7919 * L)
            draws = maxdd_batch(a, L, NPOOL * BDRAWS, rng).reshape(NPOOL, BDRAWS)
            M[i] = np.median(draws, axis=1)
        pools[cr["cell"]] = (union, M)
        niid, se = float(np.median(M[0])), float(np.std(M[0], ddof=1))
        den = float(cr["observed"]) - niid
        denom_rows.append(dict(cell=cr["cell"], T=T, observed=float(cr["observed"]),
                               N_IID=niid, denom=den, seed_SE=se,
                               denom_over_SE=abs(den) / se if se > 0 else np.nan,
                               iid_deeper=bool(den < 0)))
        P(f"  {cr['cell']:<14s} T={T:<5d} union rungs {len(union):>3d} "
          f"(coarse {len(d['D_COARSE'])}, med {len(d['D_MED'])}, dense {len(d['D_DENSE'])})"
          f"  observed {cr['observed']:.4f}  N_IID {niid:.4f}  denom {den:+.4f}  "
          f"seed SE {se:.4f}  |denom|/SE {abs(den)/se if se>0 else float('nan'):.2f}")
    DENS = ["D_COARSE", "D_MED", "D_DENSE"]
    DN = pd.DataFrame(denom_rows)
    DN.to_csv(OUT / f"{STEM}.denominator.csv", index=False)
    P(f"\n  DENOMINATOR RESOLUTION: |obs - N_IID| / seed SE — "
      f"min {DN.denom_over_SE.min():.2f}, median {DN.denom_over_SE.median():.2f}, "
      f"max {DN.denom_over_SE.max():.2f};  cells under 3 SE (1164's bar): "
      f"{int((DN.denom_over_SE < 3).sum())} of {len(DN)};  "
      f"cells where the IID null is DEEPER than the observed path: {int(DN.iid_deeper.sum())} of {len(DN)}")

    # ---- ARM B: the three readings at every (density, seed count)
    P("\n" + "=" * 112)
    P("## ARM B — EXACT rung agreement vs COARSE-BIN agreement vs the CONTINUOUS crossing")
    P("=" * 112)
    rows, cellrows = [], []
    for _, cr in C.iterrows():
        key, T, obs = cr["cell"], int(cr["T"]), float(cr["observed"])
        union, M = pools[key]
        for dn in DENS:
            rungs = ladders[key][dn]
            ix = [union.index(L) for L in rungs]
            for S in SEED_COUNTS:
                gA, gB = slice(0, S), slice(NPOOL // 2, NPOOL // 2 + S)
                res = {}
                for tag, g in (("A", gA), ("B", gB)):
                    meds = [float(np.median(M[i, g])) for i in ix]
                    niid = meds[0]
                    res[tag] = lstar_from(meds, rungs, obs, niid)
                # 1170's own form: identical rung at ALL S seeds (per-seed experiments)
                per_seed = []
                for s in range(S):
                    meds = [float(M[i, s]) for i in ix]
                    per_seed.append(lstar_from(meds, rungs, obs, meds[0])[0])
                allagree = (len(set(per_seed)) == 1) and np.isfinite(per_seed[0])
                (ra, ca), (rb, cb) = res["A"], res["B"]
                reach = np.isfinite(ra) and np.isfinite(rb)
                lr_rung = abs(np.log(ra / rb)) if reach else np.nan
                lr_cont = abs(np.log(ca / cb)) if reach and np.isfinite(ca) and np.isfinite(cb) else np.nan
                rows.append(dict(cell=key, panel=cr["panel"], book=cr["book"], density=dn,
                                 n_rungs=len(rungs), S=S, reached=reach,
                                 Lstar_A=ra, Lstar_B=rb, cont_A=ca, cont_B=cb,
                                 exact=bool(reach and ra == rb),
                                 same_coarse_bin=bool(reach and coarse_bin(ra, T) == coarse_bin(rb, T)),
                                 logratio_rung=lr_rung, logratio_cont=lr_cont,
                                 within_sqrt2=bool(np.isfinite(lr_cont) and lr_cont <= np.log(np.sqrt(2))),
                                 within_2x=bool(np.isfinite(lr_cont) and lr_cont <= np.log(2)),
                                 within_4x=bool(np.isfinite(lr_cont) and lr_cont <= np.log(4)),
                                 allseed_exact=bool(allagree)))
    R = pd.DataFrame(rows)
    R.to_csv(OUT / f"{STEM}.grid.csv", index=False)

    P("\nFULL GRID (every P1 x P2 point, all 9 cells):")
    P(R[["cell", "density", "n_rungs", "S", "reached", "Lstar_A", "Lstar_B", "cont_A", "cont_B",
         "exact", "same_coarse_bin", "logratio_cont", "allseed_exact"]]
      .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    P("\nSUMMARY over cells (fraction of the 9 cells):")
    agg = R.groupby(["density", "S"]).agg(
        n_rungs=("n_rungs", "max"), reach=("reached", "mean"),
        EXACT=("exact", "mean"), ALLSEED=("allseed_exact", "mean"),
        COARSE_BIN=("same_coarse_bin", "mean"),
        med_logratio_cont=("logratio_cont", "median"),
        CONT_within_sqrt2=("within_sqrt2", "mean"), CONT_within_2x=("within_2x", "mean"),
        CONT_within_4x=("within_4x", "mean")).reset_index()
    P(agg.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    agg.to_csv(OUT / f"{STEM}.summary.csv", index=False)

    # ---- ARM C: the verdict on the 0.326
    P("\n" + "=" * 112)
    P("## ARM C — HOW MUCH OF 1170's 0.326 INSTABILITY SURVIVES?")
    P("=" * 112)
    base = agg[(agg.density == "D_COARSE") & (agg.S == 3)].iloc[0]
    P(f"  reference point, the record's own setting (D_COARSE, S=3):")
    P(f"     EXACT rung agreement (2 groups)     {base.EXACT:.3f}   -> instability {1-base.EXACT:.3f}")
    P(f"     1170's form (identical at all 3)    {base.ALLSEED:.3f}   -> instability {1-base.ALLSEED:.3f}"
      f"   [1170 committed {COMMITTED_STABLE:.3f} / 0.326 on 132 cells]")
    P(f"     COARSE-BIN agreement                {base.COARSE_BIN:.3f}")
    P(f"     CONTINUOUS crossing within 2x       {base.CONT_within_2x:.3f}"
      f"   median |log ratio| {base.med_logratio_cont:.4f}")
    for dn in DENS:
        d = agg[(agg.density == dn) & (agg.S == 3)].iloc[0]
        P(f"  {dn:<9s} ({int(d.n_rungs):>3d} rungs, S=3): EXACT {d.EXACT:.3f}  "
          f"ALLSEED {d.ALLSEED:.3f}  COARSE-BIN {d.COARSE_BIN:.3f}  "
          f"CONT<=2x {d.CONT_within_2x:.3f}  median|log| {d.med_logratio_cont:.4f}")
    dc = agg[(agg.density == "D_COARSE")]
    dd = agg[(agg.density == "D_DENSE")]
    P(f"\n  DENSITY EFFECT at S=3: rungs {int(dc[dc.S==3].n_rungs.iloc[0])} -> "
      f"{int(dd[dd.S==3].n_rungs.iloc[0])};  EXACT {dc[dc.S==3].EXACT.iloc[0]:.3f} -> "
      f"{dd[dd.S==3].EXACT.iloc[0]:.3f};  COARSE-BIN {dc[dc.S==3].COARSE_BIN.iloc[0]:.3f} -> "
      f"{dd[dd.S==3].COARSE_BIN.iloc[0]:.3f};  median |log ratio| of the CONTINUOUS crossing "
      f"{dc[dc.S==3].med_logratio_cont.iloc[0]:.4f} -> {dd[dd.S==3].med_logratio_cont.iloc[0]:.4f}")
    P(f"  SEED EFFECT on D_DENSE: " + "; ".join(
        f"S={int(x.S)} EXACT {x.EXACT:.3f} CONT<=2x {x.CONT_within_2x:.3f} "
        f"median|log| {x.med_logratio_cont:.4f}" for _, x in dd.iterrows()))

    # ---- ARM D: phi(L) curves, published in full
    P("\n" + "=" * 112)
    P("## ARM D — the phi(L) curve on the dense ladder (S=27 pooled), published per cell")
    P("=" * 112)
    curves = []
    for _, cr in C.iterrows():
        key, obs = cr["cell"], float(cr["observed"])
        union, M = pools[key]
        rungs = ladders[key]["D_DENSE"]
        ix = [union.index(L) for L in rungs]
        meds = [float(np.median(M[i, :27])) for i in ix]
        niid = meds[0]
        for L, m in zip(rungs, meds):
            curves.append(dict(cell=key, L=L, null_median=m, observed=obs, N_IID=niid,
                               phi=(m - niid) / (obs - niid) if abs(obs - niid) > 1e-12 else np.nan))
    CV = pd.DataFrame(curves)
    CV.to_csv(OUT / f"{STEM}.phi_curve.csv", index=False)
    pv = CV.pivot_table(index="L", columns="cell", values="phi")
    P(pv.to_string(float_format=lambda x: f"{x:.3f}"))
    flat = CV.groupby("cell").phi.agg(lambda s: float(s.max() - s.min()))
    P("\n  phi range over the dense ladder per cell: " +
      "; ".join(f"{k} {v:.3f}" for k, v in flat.items()))

    # ---- ARM E: PROTOCOL rule 8 walk-forward + both KEEP paths on the same books
    P("\n" + "=" * 112)
    P("## ARM E — PROTOCOL rule 8 walk-forward and BOTH KEEP paths on the 9 books")
    P("=" * 112)
    wf = []
    for pn, px in panels.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        live = backtest(px, book_v2band(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        h = len(live) // 2
        rs = {bn: pd.Series(series[f"{pn}/{bn}"], index=live.index) for bn in BOOKS}
        pick = max(BOOKS, key=lambda b: metrics(rs[b].iloc[:h])["Sharpe"])
        for bn in BOOKS:
            r = rs[bn]
            m, mo = metrics(r), metrics(r.iloc[h:])
            s1, s2 = metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]
            b1, b2 = metrics(live.iloc[:h])["Sharpe"], metrics(live.iloc[h:])["Sharpe"]
            p1, p2 = metrics(spy.iloc[:h])["Sharpe"], metrics(spy.iloc[h:])["Sharpe"]
            ms = metrics(spy)
            wf.append(dict(panel=pn, book=bn, IS_pick=(bn == pick),
                           CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=s1, H2=s2,
                           OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                           base_OOS_CAGR=metrics(live.iloc[h:])["CAGR"],
                           base_OOS_Sharpe=metrics(live.iloc[h:])["Sharpe"],
                           base_OOS_MaxDD=metrics(live.iloc[h:])["MaxDD"],
                           SPY_OOS_CAGR=metrics(spy.iloc[h:])["CAGR"],
                           SPY_OOS_Sharpe=metrics(spy.iloc[h:])["Sharpe"],
                           SPY_OOS_MaxDD=metrics(spy.iloc[h:])["MaxDD"],
                           p4a=bool(s1 > b1 and s2 > b2 and m["MaxDD"] >= metrics(live)["MaxDD"]),
                           p4b=bool(s1 > p1 and s2 > p2 and m["MaxDD"] >= 0.60 * ms["MaxDD"]
                                    and m["CAGR"] >= 0.70 * ms["CAGR"])))
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n  4a PASS {int(W.p4a.sum())} of {len(W)};  4b PASS {int(W.p4b.sum())} of {len(W)}")

    P("\n" + "=" * 112)
    P("## ARM F — leaderboard compare() for the IS-chosen book on each panel")
    P("=" * 112)
    for pn, px in panels.items():
        pick = W[(W.panel == pn) & W.IS_pick].book.iloc[0]
        compare(f"1178 L* cells — IS-pick {pick} [{pn}]", BOOKS[pick], px, freq=FREQ, cost_bps=COST_BPS)

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

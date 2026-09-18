#!/usr/bin/env python3
"""Idea 1147 — are the record's H and CADENCE argmaxes WAITING ON DATA THAT CANNOT HELP?

1140's bycatch found that on the mover ladders the non-path statistics' realised rung gaps
shrink at n^-0.58 while their sampling SD falls at only n^-0.44, so the resolution ratio
gets WORSE with a longer tape (b(ratio) -0.1251).  If that holds on the record's own H and
CADENCE ladders, then every committed 'under-powered at this sample length' argmax is not
waiting on data at all: the rung effect is ~0 and no attainable tape resolves it.

This run tests that DIRECTLY rather than as a census of prose.  It builds the two ladders as
REAL BOOKS on three panels and measures, at every subsample length:

  GAP(n)   = max over rungs of the statistic  -  min over rungs      (the realised effect)
  SD(n)    = circular block-bootstrap SD of the statistic at a rung  (the sampling width)
  RATIO(n) = GAP(n) / SD(n)                                          (the resolution)

and fits log-log slopes b(GAP), b(SD), b(RATIO) against n.  b(RATIO) <= 0 means a longer tape
does NOT resolve the argmax.  G2 then tests the zero reading head-on: a block-bootstrap null
of 'all rungs identical' against the observed gap.

CAPITAL ARM (PROTOCOL rule 8) — 'price what changes if the correct reading is zero'.  An
argmax chooser picks the best H rung and the best cadence rung on 2009-2016; a ZERO chooser
ignores the ladder and takes the record's standing default (H=1, weekly).  Both are read ONCE
on 2017-2026 against the RULES v2 baseline and SPY, with both KEEP paths (4a, 4b).

TUNED PARAMETERS (max 2, all grid points reported): LADDER (H or CADENCE) and STAT
(Sharpe / CAGR / MaxDD).  Nothing else is searched.

Run: python3 research/backtests/2026-09-18_H-and-cadence-argmax-waiting-on-data_cloud.py
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics  # noqa

pd.set_option("display.width", 220)
COST_BPS = 10                     # PROTOCOL rule 2
WARMUP   = 260
SPLIT    = "2017-01-01"           # rule 8 boundary
H_GRID   = [1, 21, 42, 63, 126, 252]        # ladder 1: overlapping hold length, trading days
C_GRID   = ["D", "W", "M", "Q"]             # ladder 2: rebalance cadence
STATS    = ["Sharpe", "CAGR", "MaxDD"]      # param 2
N_GRID   = [252, 504, 1008, 2016, None]     # subsample lengths (None = full tape)
BLOCK    = 63                     # block length for the circular block bootstrap
NBOOT    = 400
SEED     = 1147

# ----------------------------------------------------------------------------- panels
def small_panel():
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad  = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    px   = load_universe(small=True)
    return px[[c for c in px.columns if c == "SPY" or c not in bad]], len(bad)

def panels():
    s, nd = small_panel()
    return {"U56": load_universe(), "B136": load_universe(broad=True), f"SMALL{s.shape[1]-1}": s}, nd

# ----------------------------------------------------------------------------- the H ladder
def mom_topn_H(px, n=20, H=1, gross=1.0):
    """The 2026-09-04 KEEP-4b candidate (top-n equal weight, NO vol scaler, trend-gated) held
    as H OVERLAPPING tranches: the target book is the average of the last H daily selections,
    which is the standard overlapping-portfolio construction of a hold length.  H=1 is the
    base book."""
    s, above, _ = score(px, vol_scale=False)
    s  = s.drop(columns=["SPY"], errors="ignore")
    ab = above.drop(columns=["SPY"], errors="ignore")
    rank = s.where(ab).rank(axis=1, ascending=False)
    sel  = (rank <= n).astype(float)
    w    = gross * sel.div(sel.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    if H > 1:
        w = w.rolling(H, min_periods=1).mean()
    return w.reindex(columns=px.columns).fillna(0.0)

def run(px, H, freq):
    res = backtest(px, mom_topn_H(px, H=H), cost_bps=COST_BPS, freq=freq)
    return res["returns"].loc[px.index[WARMUP]:], res["turnover"].loc[px.index[WARMUP]:]

# ----------------------------------------------------------------------------- statistics
def stat(r, which):
    m = metrics(r)
    return m[which]

def boot_sd(r, which, rng, nboot=NBOOT, block=BLOCK):
    """Circular block bootstrap SD of the statistic."""
    x = r.values; T = len(x)
    if T < 2 * block: return np.nan
    nb = int(np.ceil(T / block))
    out = np.empty(nboot)
    for b in range(nboot):
        st = rng.integers(0, T, nb)
        idx = (st[:, None] + np.arange(block)[None, :]).ravel()[:T] % T
        out[b] = stat(pd.Series(x[idx]), which)
    return float(np.nanstd(out, ddof=1))

def loglog_slope(ns, ys):
    ok = np.isfinite(ns) & np.isfinite(ys) & (np.asarray(ys) > 0)
    if ok.sum() < 3: return np.nan
    return float(np.polyfit(np.log(np.asarray(ns)[ok]), np.log(np.asarray(ys)[ok]), 1)[0])

def fmt(df): return df.to_string(float_format=lambda x: f"{x:.4f}")

# =============================================================================== main
def main():
    rng = np.random.default_rng(SEED)
    P, nd = panels()
    print("# Idea 1147 — are the H and CADENCE argmaxes waiting on data that cannot help?")
    print(f"# cost {COST_BPS} bps, next-day execution, warm-up {WARMUP} rows dropped, "
          f"SMALL dropped {nd} names on max_1d_move >= 1.0")
    print(f"# block bootstrap: block {BLOCK}d, {NBOOT} reps, seed {SEED}")
    for k, v in P.items():
        print(f"#   {k}: {v.shape[1]-1} names + SPY, {v.index[0].date()} .. {v.index[-1].date()}, {len(v)} rows")

    # ---- every rung of both ladders, once
    R = {}
    for pn, px in P.items():
        for H in H_GRID:
            R[(pn, "H", H)] = run(px, H, "W")[0]          # H ladder read at the standing cadence
        for c in C_GRID:
            R[(pn, "CADENCE", c)] = run(px, 1, c)[0]      # cadence ladder read at the standing H
        R[(pn, "SPY")]  = px["SPY"].pct_change().fillna(0).loc[px.index[WARMUP]:]
        R[(pn, "BASE")] = backtest(px, rules_v2_weights(px), cost_bps=COST_BPS,
                                   freq="W")["returns"].loc[px.index[WARMUP]:]

    # =================== G0: the two ladders, full tape, every rung ====================
    print("\n## G0 — the ladders themselves (full tape, every rung, ALL grid points)")
    rows = []
    for pn in P:
        for lad, grid in (("H", H_GRID), ("CADENCE", C_GRID)):
            for rung in grid:
                r = R[(pn, lad, rung)]
                m = metrics(r)
                rows.append(dict(panel=pn, ladder=lad, rung=rung, CAGR=m["CAGR"],
                                 Sharpe=m["Sharpe"], MaxDD=m["MaxDD"]))
    L0 = pd.DataFrame(rows)
    print(fmt(L0.set_index(["panel", "ladder", "rung"])))
    L0.to_csv(ROOT / "research" / "backtests" / "2026-09-18_ladder_rungs_cloud.csv", index=False)

    # =================== G1: does a longer tape RESOLVE the argmax? ====================
    print("\n## G1 — GAP(n), SD(n), RATIO(n) = GAP/SD against subsample length n. "
          "b(RATIO) <= 0 means a longer tape does NOT resolve the argmax.")
    g1 = []
    for pn in P:
        for lad, grid in (("H", H_GRID), ("CADENCE", C_GRID)):
            for st in STATS:
                for n in N_GRID:
                    vals, sds = [], []
                    for rung in grid:
                        r = R[(pn, lad, rung)]
                        rr = r if n is None else r.iloc[-n:]
                        if len(rr) < 2 * BLOCK: vals, sds = [], []; break
                        vals.append(stat(rr, st))
                        sds.append(boot_sd(rr, st, rng))
                    if not vals: continue
                    gap = float(np.nanmax(vals) - np.nanmin(vals))
                    sd  = float(np.nanmean(sds))
                    g1.append(dict(panel=pn, ladder=lad, stat=st, n=(len(r) if n is None else n),
                                   GAP=gap, SD=sd, RATIO=gap / sd if sd else np.nan,
                                   argmax=grid[int(np.nanargmax(vals))]))
    G1 = pd.DataFrame(g1)
    G1.to_csv(ROOT / "research" / "backtests" / "2026-09-18_resolution_scaling_cloud.csv", index=False)
    print(fmt(G1.set_index(["panel", "ladder", "stat", "n"])))

    print("\n### G1a — log-log slopes b against n.  1140's bycatch read b(GAP) -0.58, "
          "b(SD) -0.44, b(RATIO) -0.1251 on the MOVER ladders.")
    sl = []
    for (pn, lad, st), d in G1.groupby(["panel", "ladder", "stat"]):
        d = d.sort_values("n")
        sl.append(dict(panel=pn, ladder=lad, stat=st,
                       b_GAP=loglog_slope(d["n"], d["GAP"]),
                       b_SD=loglog_slope(d["n"], d["SD"]),
                       b_RATIO=loglog_slope(d["n"], d["RATIO"]),
                       RATIO_full=d["RATIO"].iloc[-1]))
    SL = pd.DataFrame(sl)
    print(fmt(SL.set_index(["panel", "ladder", "stat"])))
    print("\n### G1b — how many of the 18 (panel, ladder, stat) cells have b(RATIO) <= 0 "
          "(a longer tape makes the argmax HARDER to resolve)?")
    print(f"  b(RATIO) <= 0 at {(SL['b_RATIO'] <= 0).sum()} of {len(SL)} cells; "
          f"median b(RATIO) {SL['b_RATIO'].median():+.4f}; "
          f"median b(GAP) {SL['b_GAP'].median():+.4f}; median b(SD) {SL['b_SD'].median():+.4f}")
    print(f"  RATIO at the FULL tape <= 2 (the record's own decisiveness bar) at "
          f"{(SL['RATIO_full'] <= 2).sum()} of {len(SL)} cells; median {SL['RATIO_full'].median():.4f}")

    # =================== G2: is the rung effect ZERO? =================================
    print("\n## G2 — the ZERO reading tested head-on.  Block-bootstrap null of 'every rung is "
          "the same book': resample the POOLED rungs and read the gap the null produces.")
    g2 = []
    for pn in P:
        for lad, grid in (("H", H_GRID), ("CADENCE", C_GRID)):
            for st in STATS:
                obs = [stat(R[(pn, lad, rung)], st) for rung in grid]
                gap_obs = float(np.nanmax(obs) - np.nanmin(obs))
                T = len(R[(pn, lad, grid[0])]); nb = int(np.ceil(T / BLOCK))
                pool = np.column_stack([R[(pn, lad, g)].values for g in grid])
                null = np.empty(NBOOT)
                for b in range(NBOOT):
                    st_i = rng.integers(0, T, nb)
                    idx = (st_i[:, None] + np.arange(BLOCK)[None, :]).ravel()[:T] % T
                    v = [stat(pd.Series(pool[idx, j]), st) for j in range(len(grid))]
                    null[b] = np.nanmax(v) - np.nanmin(v)
                g2.append(dict(panel=pn, ladder=lad, stat=st, gap_obs=gap_obs,
                               null_med=float(np.nanmedian(null)),
                               null_p95=float(np.nanpercentile(null, 95)),
                               p_value=float(np.mean(null >= gap_obs)),
                               decisive=bool(np.mean(null >= gap_obs) < 0.05)))
    G2 = pd.DataFrame(g2)
    print(fmt(G2.set_index(["panel", "ladder", "stat"])))
    print(f"\n  DECISIVE (p < 0.05) at {G2['decisive'].sum()} of {len(G2)} cells. "
          f"A non-decisive cell is NOT under-powered — it is a rung effect the tape "
          f"cannot separate from zero, and G1 says more tape will not separate it either.")

    # =================== G3: CAPITAL ARM — rule 8 ======================================
    print("\n## G3 — CAPITAL ARM (PROTOCOL rule 8).  'Price what changes if the correct reading "
          "is ZERO.'  ARGMAX chooser picks the best H rung and the best cadence rung on "
          "2009-2016; ZERO chooser ignores both ladders and takes the standing default (H=1, "
          "weekly).  Each is read ONCE on 2017-2026.")
    cap = []
    for pn, px in P.items():
        is_end = pd.Timestamp(SPLIT)
        spy_o, base_o = R[(pn, "SPY")].loc[is_end:], R[(pn, "BASE")].loc[is_end:]
        ms, mb = metrics(spy_o), metrics(base_o)
        for st in STATS:
            isv = {}
            for lad, grid in (("H", H_GRID), ("CADENCE", C_GRID)):
                isv[lad] = {g: stat(R[(pn, lad, g)].loc[:is_end], st) for g in grid}
            pick_H = max(isv["H"], key=isv["H"].get)
            pick_C = max(isv["CADENCE"], key=isv["CADENCE"].get)
            print(f"  {pn:10s} {st:7s} IS H rungs: " +
                  " ".join(f"{k}={v:+.4f}" for k, v in isv['H'].items()) + f"  -> H*={pick_H}")
            print(f"  {pn:10s} {st:7s} IS C rungs: " +
                  " ".join(f"{k}={v:+.4f}" for k, v in isv['CADENCE'].items()) + f"  -> C*={pick_C}")
            # the ARGMAX chooser buys the joint pick; the ZERO chooser buys the default
            for label, (H, c) in (("ARGMAX", (pick_H, pick_C)), ("ZERO", (1, "W"))):
                r = run(px, H, c)[0].loc[is_end:]
                m = metrics(r); h = len(r) // 2
                m1, m2 = metrics(r.iloc[:h]), metrics(r.iloc[h:])
                s1, s2 = metrics(spy_o.iloc[:h]), metrics(spy_o.iloc[h:])
                b1, b2 = metrics(base_o.iloc[:h]), metrics(base_o.iloc[h:])
                cap.append(dict(panel=pn, IS_stat=st, chooser=label, H=H, cadence=c,
                                OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"],
                                SPY_CAGR=ms["CAGR"], SPY_Sharpe=ms["Sharpe"], SPY_MaxDD=ms["MaxDD"],
                                BASE_Sharpe=mb["Sharpe"], BASE_MaxDD=mb["MaxDD"],
                                L_H1=m1["Sharpe"] > s1["Sharpe"], L_H2=m2["Sharpe"] > s2["Sharpe"],
                                L_DD=m["MaxDD"] >= 0.60 * ms["MaxDD"],
                                L_CAGR=m["CAGR"] >= 0.70 * ms["CAGR"],
                                pass_4b=(m1["Sharpe"] > s1["Sharpe"] and m2["Sharpe"] > s2["Sharpe"]
                                         and m["MaxDD"] >= 0.60 * ms["MaxDD"]
                                         and m["CAGR"] >= 0.70 * ms["CAGR"]),
                                pass_4a=(m1["Sharpe"] > b1["Sharpe"] and m2["Sharpe"] > b2["Sharpe"]
                                         and m["MaxDD"] >= mb["MaxDD"])))
    CAP = pd.DataFrame(cap)
    print("\n### G3a — OOS 2017-2026, every (panel, IS_stat, chooser) cell")
    print(CAP.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    CAP.to_csv(ROOT / "research" / "backtests" / "2026-09-18_argmax_vs_zero_cloud.csv", index=False)

    print("\n### G3b — WHAT THE ARGMAX BUYS OVER THE ZERO READING (ARGMAX minus ZERO, OOS)")
    piv = CAP.pivot_table(index=["panel", "IS_stat"], columns="chooser",
                          values=["OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD"])
    d = pd.DataFrame({k: piv[(k, "ARGMAX")] - piv[(k, "ZERO")]
                      for k in ("OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD")})
    print(fmt(d))
    n = len(d)
    print(f"\n  d(OOS Sharpe): mean {d['OOS_Sharpe'].mean():+.4f}, SE "
          f"{d['OOS_Sharpe'].std(ddof=1)/np.sqrt(n):.4f}, t "
          f"{d['OOS_Sharpe'].mean()/(d['OOS_Sharpe'].std(ddof=1)/np.sqrt(n)):+.2f}, n={n}")
    print(f"  d(OOS CAGR)  : mean {d['OOS_CAGR'].mean():+.4f}, "
          f"d(OOS MaxDD): mean {d['OOS_MaxDD'].mean():+.4f}")
    print(f"  argmax pick == default (H=1, W) in {((CAP['chooser']=='ARGMAX') & (CAP['H']==1) & (CAP['cadence']=='W')).sum()} "
          f"of {(CAP['chooser']=='ARGMAX').sum()} argmax cells")
    print(f"\n### G3c — KEEP paths over ALL {len(CAP)} grid points: "
          f"4b {CAP['pass_4b'].sum()}, 4a {CAP['pass_4a'].sum()}")
    if CAP["pass_4b"].any():
        print(CAP[CAP["pass_4b"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("  binding 4b legs (failure counts): " +
          ", ".join(f"{k} {int((~CAP[k]).sum())}" for k in ("L_H1", "L_H2", "L_DD", "L_CAGR")))

    print("\n## SURVIVORSHIP (PROTOCOL rule 9): U56 and B136 are CURRENT-CONSTITUENT lists; the "
          "SMALL panel is a current sub-$2B screen with names dropped on max_1d_move >= 1.0. Every "
          "LEVEL (CAGR, Sharpe, 4b count) is an UPPER bound. G1/G2 are gaps and ratios BETWEEN "
          "rungs of the same panel, so a level bias moves every rung together and they are "
          "first-order immune; G3's OOS levels are not, and are quoted as upper bounds.")

if __name__ == "__main__":
    main()

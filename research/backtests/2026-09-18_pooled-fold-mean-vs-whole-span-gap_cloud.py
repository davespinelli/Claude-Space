#!/usr/bin/env python3
"""Idea 1278 — is the POOLED-FOLD-MEAN vs WHOLE-SPAN gap a GENERAL PROPERTY of every
fold-averaged figure the record publishes?

1276 measured the gap on ONE statistic (Sharpe) on ONE object (chooser comparisons) and
found +0.0202 at 0 bps, an order of magnitude larger than the 0-50 bps cost ladder moves
the same numbers (+0.0017..+0.0071).  This run measures the same AGGREGATION gap

    GAP(stat) = mean_over_K_folds( stat(fold_k) )  -  stat(whole span)

on REAL books over THREE panels, for the statistic set the record actually fold-averages:
turnover/yr, cost drag/yr, mean daily return, CAGR, vol, Sharpe, MaxDD, plus the 4b
per-leg pass counts.  It separates the statistics that are SHAPE-INVARIANT (exactly linear
in the return series, so equal-length folds give GAP == 0 to floating point) from the ones
that are not, and it prices the non-invariant gaps against the cost ladder.

CAPITAL ARM (PROTOCOL rule 8).  The gap only matters if it changes what you BUY.  A chooser
picks one of the candidate books on the FIRST half by (a) whole-span Sharpe and (b) fold-mean
Sharpe, and each pick is read ONCE on the untouched second half, reported against the RULES v2
baseline and SPY with both KEEP paths (4a, 4b).

TUNED PARAMETERS (max 2, all grid points reported): FOLD_LEN (fold length in trading days),
STAT_SET (the statistic family). Nothing else is searched.

Run: python3 research/backtests/2026-09-18_pooled-fold-mean-vs-whole-span-gap_cloud.py
"""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights, score  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics  # noqa

pd.set_option("display.width", 200)
COST_BPS   = 10          # PROTOCOL rule 2
FOLD_GRID  = [126, 189, 252, 378]      # param 1: fold length in trading days (~0.5y..1.5y)
STAT_SETS  = ["LEVEL", "RATIO"]        # param 2: statistic family (see STATS below)
WARMUP     = 260
SPLIT      = "2017-01-01"              # rule 8 boundary

# ----------------------------------------------------------------------------- panels
def small_panel():
    """483-name sub-$2B panel, max_1d_move >= 1.0 names DROPPED (mandated)."""
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad  = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    px   = load_universe(small=True)
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad)

def panels():
    u = load_universe()
    b = load_universe(broad=True)
    s, ndrop = small_panel()
    return {"U56": u, "B136": b, f"SMALL{s.shape[1]-1}": s}, ndrop

# ----------------------------------------------------------------------------- books
def mom_topn_weights(px, n=20, gross=1.0):
    """The 2026-09-04 KEEP-4b candidate: top-n equal weight on the composite WITHOUT the
    vol scaler, trend-gated (above 200d), gross spread over the n names."""
    s, above, _ = score(px, vol_scale=False)
    s = s.drop(columns=["SPY"], errors="ignore")
    ab = above.drop(columns=["SPY"], errors="ignore")
    elig = s.where(ab)
    rank = elig.rank(axis=1, ascending=False)
    sel  = (rank <= n).astype(float)
    cnt  = sel.sum(axis=1).replace(0, np.nan)
    w    = gross * sel.div(cnt, axis=0).fillna(0.0)
    return w.reindex(columns=px.columns).fillna(0.0)

BOOKS = {
    "MOM20":   lambda px: mom_topn_weights(px, n=20),
    "MOM10":   lambda px: mom_topn_weights(px, n=10),
    "MOM40":   lambda px: mom_topn_weights(px, n=40),
    "RULESv2": rules_v2_weights,
    "RULESv1": rules_v1_weights,
}

def run_book(px, fn, cost_bps=COST_BPS, freq="W"):
    res = backtest(px, fn(px), cost_bps=cost_bps, freq=freq)
    start = px.index[WARMUP]
    return res["returns"].loc[start:], res["turnover"].loc[start:]

# ----------------------------------------------------------------------------- statistics
def stat_turnover(r, to):  return to.sum() / (len(r) / 252)                 # units/yr  LINEAR in `to`
def stat_drag(r, to):      return to.sum() * COST_BPS / 1e4 / (len(r) / 252)  # /yr      LINEAR
def stat_meanret(r, to):   return r.mean() * 252                            # /yr       LINEAR in r
def stat_cagr(r, to):      return (1 + r).prod() ** (252 / len(r)) - 1      # NON-linear
def stat_vol(r, to):       return r.std() * np.sqrt(252)                    # NON-linear
def stat_sharpe(r, to):
    v = r.std() * np.sqrt(252)
    return (r.mean() * 252) / v if v else np.nan                            # NON-linear
def stat_maxdd(r, to):
    eq = (1 + r).cumprod(); return (eq / eq.cummax() - 1).min()             # NON-linear, PATH

STATS = {
    "LEVEL": {"turnover/yr": stat_turnover, "drag/yr": stat_drag, "meanret/yr": stat_meanret,
              "CAGR": stat_cagr, "MaxDD": stat_maxdd},
    "RATIO": {"vol": stat_vol, "Sharpe": stat_sharpe},
}
LINEAR = {"turnover/yr", "drag/yr", "meanret/yr"}   # exactly linear in the per-day series

def folds(idx, L):
    """Equal-length non-overlapping folds; the trailing remainder (< L days) is DROPPED so
    the fold mean is an unweighted mean of equal-length windows (the record's convention)."""
    K = len(idx) // L
    return [slice(k * L, (k + 1) * L) for k in range(K)], K

def gap_table(r, to, L, stats):
    """GAP decomposes exactly into
         GAP        = foldmean - whole
         GAP_shape  = foldmean - stat(TRUNCATED span, the same K*L rows the folds cover)
         GAP_trunc  = stat(truncated) - stat(whole)      [pure sample-length artefact]
    A statistic that is linear in the per-day series has GAP_shape == 0 to floating point."""
    out = {}
    fs, K = folds(r.index, L)
    tr = slice(0, K * L)
    rt, tot = r.iloc[tr], to.iloc[tr]
    for nm, f in stats.items():
        whole = f(r, to); trunc = f(rt, tot)
        per   = [f(r.iloc[s], to.iloc[s]) for s in fs]
        fm    = float(np.nanmean(per))
        out[nm] = dict(whole=whole, trunc=trunc, foldmean=fm, gap=fm - whole,
                       gap_shape=fm - trunc, gap_trunc=trunc - whole, K=K,
                       fold_sd=float(np.nanstd(per, ddof=1)) if K > 1 else np.nan)
    return out

# ----------------------------------------------------------------------------- 4b legs
def legs_4b(r, spy):
    h = len(r) // 2
    m, ms = metrics(r), metrics(spy)
    m1, m2 = metrics(r.iloc[:h]), metrics(r.iloc[h:])
    s1, s2 = metrics(spy.iloc[:h]), metrics(spy.iloc[h:])
    return dict(L_H1=m1["Sharpe"] > s1["Sharpe"], L_H2=m2["Sharpe"] > s2["Sharpe"],
                L_DD=m["MaxDD"] >= 0.60 * ms["MaxDD"], L_CAGR=m["CAGR"] >= 0.70 * ms["CAGR"])

def fmt(x, n=4):
    return "nan" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:+.{n}f}"

# =============================================================================== main
def main():
    P, ndrop = panels()
    print(f"# Idea 1278 — pooled-fold-mean vs whole-span AGGREGATION GAP")
    print(f"# cost {COST_BPS} bps, weekly cadence, warm-up {WARMUP} rows dropped, "
          f"SMALL dropped {ndrop} names on max_1d_move >= 1.0")
    for k, v in P.items():
        print(f"#   {k}: {v.shape[1]-1} names + SPY, {v.index[0].date()} .. {v.index[-1].date()}, {len(v)} rows")

    # ---- run every book on every panel once
    R = {}
    for pn, px in P.items():
        for bn, fn in BOOKS.items():
            r, to = run_book(px, fn)
            R[(pn, bn)] = (r, to)
        R[(pn, "SPY")] = (px["SPY"].pct_change().fillna(0).loc[px.index[WARMUP]:],
                          pd.Series(0.0, index=px.index).loc[px.index[WARMUP]:])

    # =========================== G1: the gap, every grid point ===========================
    print("\n## G1 — GAP = mean-of-K-fold(stat) - whole-span(stat).  ALL grid points.")
    rows = []
    for setname in STAT_SETS:
        for L in FOLD_GRID:
            for (pn, bn), (r, to) in R.items():
                g = gap_table(r, to, L, STATS[setname])
                for st, d in g.items():
                    rows.append(dict(set=setname, L=L, panel=pn, book=bn, stat=st,
                                     whole=d["whole"], trunc=d["trunc"], foldmean=d["foldmean"],
                                     gap=d["gap"], gap_shape=d["gap_shape"], gap_trunc=d["gap_trunc"],
                                     K=d["K"], fold_sd=d["fold_sd"]))
    G = pd.DataFrame(rows)
    G.to_csv(ROOT / "research" / "backtests" / "2026-09-18_gap_grid_cloud.csv", index=False)
    print(f"({len(G)} grid points written to 2026-09-18_gap_grid_cloud.csv)")

    print("\n### G1a — max |gap| per statistic, over every (panel, book, L). "
          "SHAPE-INVARIANT statistics must read ~0.")
    agg = (G.groupby("stat")["gap"].agg(max_abs=lambda s: s.abs().max(),
                                        median_abs=lambda s: s.abs().median(),
                                        mean=lambda s: s.mean(), n="size"))
    agg["linear_in_r"] = [s in LINEAR for s in agg.index]
    print(agg.to_string(float_format=lambda x: f"{x:.3e}"))

    print("\n### G1a2 — the SAME gap DECOMPOSED. GAP_shape is the aggregation effect proper "
          "(fold mean vs the SAME rows read whole); GAP_trunc is the dropped-remainder artefact.")
    dec = G.groupby("stat")[["gap", "gap_shape", "gap_trunc"]].agg(lambda s: s.abs().max())
    dec.columns = ["max|gap|", "max|shape|", "max|trunc|"]
    dec["linear_in_r"] = [x in LINEAR for x in dec.index]
    print(dec.to_string(float_format=lambda x: f"{x:.3e}"))

    print("\n### G1b — GAP_shape by fold length L (non-linear statistics): does it shrink with L?")
    nl = G[~G["stat"].isin(LINEAR)]
    piv = nl.pivot_table(index="stat", columns="L", values="gap_shape", aggfunc=lambda s: s.abs().median())
    print(piv.to_string(float_format=lambda x: f"{x:.4f}"))

    print("\n### G1c — gap by panel (non-linear statistics, median |gap| over books and L)")
    print(nl.pivot_table(index="stat", columns="panel", values="gap_shape",
                         aggfunc=lambda s: s.abs().median()).to_string(float_format=lambda x: f"{x:.4f}"))

    print("\n### G1d — SIGN consistency of GAP_shape: share of grid points with gap_shape > 0")
    print(G.groupby("stat")["gap_shape"].apply(lambda s: (s > 0).mean()).to_string(float_format=lambda x: f"{x:.3f}"))

    # =================== G2: gap vs the 0-50 bps cost ladder (1276's yardstick) ==========
    print("\n## G2 — is the AGGREGATION gap larger than the 0-50 bps COST LADDER moves the "
          "same statistic?  (1276 found +0.0202 vs +0.0017..+0.0071 on Sharpe.)")
    lad = []
    for pn, px in P.items():
        for bn, fn in BOOKS.items():
            base = None
            for c in (0, 10, 25, 50):
                r, to = run_book(px, fn, cost_bps=c)
                row = {st: f(r, to) for st, f in {**STATS["LEVEL"], **STATS["RATIO"]}.items()}
                row["drag/yr"] = to.sum() * c / 1e4 / (len(r) / 252)   # at the rung CHARGED
                if c == 0: base = row
                lad.append(dict(panel=pn, book=bn, cost=c,
                                **{f"d_{k}": row[k] - base[k] for k in row}))
    LAD = pd.DataFrame(lad)
    cl = LAD[LAD["cost"] == 50].set_index(["panel", "book"])
    print("### G2a — |0 -> 50 bps| move vs median |aggregation gap| at L=252, per statistic")
    cmp_rows = []
    for st in list(STATS["LEVEL"]) + list(STATS["RATIO"]):
        cost_move = cl[f"d_{st}"].abs().median()
        agg_gap   = G[(G["stat"] == st) & (G["L"] == 252)]["gap_shape"].abs().median()
        cmp_rows.append(dict(stat=st, cost_0_50=cost_move, agg_gap_L252=agg_gap,
                             ratio=agg_gap / cost_move if cost_move else np.inf))
    C = pd.DataFrame(cmp_rows).set_index("stat")
    print(C.to_string(float_format=lambda x: f"{x:.4f}"))

    # =================== G3: 4b per-leg counts, whole-span vs fold-mean =================
    print("\n## G3 — 4b PER-LEG counts.  Whole-span legs vs the share of folds passing each leg.")
    l_rows = []
    for pn, px in P.items():
        spy = R[(pn, "SPY")][0]
        for bn in BOOKS:
            r = R[(pn, bn)][0]
            w = legs_4b(r, spy)
            for L in FOLD_GRID:
                fs, K = folds(r.index, L)
                fr = [legs_4b(r.iloc[s], spy.iloc[s]) for s in fs]
                for leg in w:
                    l_rows.append(dict(panel=pn, book=bn, L=L, leg=leg,
                                       whole=float(w[leg]),
                                       foldshare=float(np.mean([x[leg] for x in fr])), K=K))
    LG = pd.DataFrame(l_rows)
    print(LG.pivot_table(index="leg", columns="L", values=["whole", "foldshare"],
                         aggfunc="mean").to_string(float_format=lambda x: f"{x:.3f}"))
    print("\n### G3a — how often does the fold-share DISAGREE with the whole-span leg "
          "(fold-share on the wrong side of 0.5)?")
    LG["disagree"] = ((LG["foldshare"] > 0.5) != (LG["whole"] > 0.5))
    print(LG.groupby(["leg", "L"])["disagree"].mean().unstack().to_string(float_format=lambda x: f"{x:.3f}"))

    # =================== G4: CAPITAL ARM — rule 8 walk-forward =========================
    print("\n## G4 — CAPITAL ARM (PROTOCOL rule 8).  A chooser picks ONE book on 2009-2016 by "
          "(a) WHOLE-SPAN Sharpe and (b) FOLD-MEAN Sharpe (L=252); each pick is read ONCE on "
          "2017-2026.  Does the aggregation convention change what you BUY, and what does it cost?")
    cap = []
    for pn, px in P.items():
        spy_full = R[(pn, "SPY")][0]
        is_end = pd.Timestamp(SPLIT)
        picks = {}
        for conv in ("WHOLE", "FOLDMEAN"):
            sc = {}
            for bn in BOOKS:
                r = R[(pn, bn)][0]
                ris = r.loc[:is_end]
                if len(ris) < 300: continue
                if conv == "WHOLE":
                    sc[bn] = stat_sharpe(ris, None)
                else:
                    fs, K = folds(ris.index, 252)
                    sc[bn] = float(np.nanmean([stat_sharpe(ris.iloc[s], None) for s in fs]))
            picks[conv] = max(sc, key=sc.get)
            print(f"  {pn:10s} {conv:9s} IS scores: " +
                  "  ".join(f"{k}={v:+.4f}" for k, v in sorted(sc.items(), key=lambda kv: -kv[1])) +
                  f"   -> PICK {picks[conv]}")
        for conv, bn in picks.items():
            r_oos = R[(pn, bn)][0].loc[is_end:]
            s_oos = spy_full.loc[is_end:]
            b_oos = R[(pn, "RULESv2")][0].loc[is_end:]
            m, ms, mb = metrics(r_oos), metrics(s_oos), metrics(b_oos)
            lg = legs_4b(r_oos, s_oos)
            cap.append(dict(panel=pn, conv=conv, pick=bn,
                            OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"],
                            SPY_CAGR=ms["CAGR"], SPY_Sharpe=ms["Sharpe"], SPY_MaxDD=ms["MaxDD"],
                            BASE_Sharpe=mb["Sharpe"], BASE_MaxDD=mb["MaxDD"],
                            **{k: bool(v) for k, v in lg.items()},
                            pass_4b=all(lg.values()),
                            pass_4a=(metrics(r_oos.iloc[:len(r_oos)//2])["Sharpe"] > metrics(b_oos.iloc[:len(b_oos)//2])["Sharpe"]
                                     and metrics(r_oos.iloc[len(r_oos)//2:])["Sharpe"] > metrics(b_oos.iloc[len(b_oos)//2:])["Sharpe"]
                                     and m["MaxDD"] >= mb["MaxDD"])))
    CAP = pd.DataFrame(cap)
    print("\n### G4a — OOS 2017-2026, the pick each convention hands you, vs baseline and SPY")
    print(CAP.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dis = CAP.pivot_table(index="panel", columns="conv", values="pick", aggfunc="first")
    dis["picks_differ"] = dis["WHOLE"] != dis["FOLDMEAN"]
    print("\n### G4b — does the convention change the PICK?")
    print(dis.to_string())

    # =================== G5: full / halves table for the incumbent book ================
    print("\n## G5 — full sample and halves, incumbent MOM20 vs RULES v2 vs SPY (PROTOCOL rule 3/4)")
    ft = []
    for pn in P:
        for bn in ("MOM20", "RULESv2", "SPY"):
            r = R[(pn, bn)][0]; h = len(r) // 2
            m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
            ft.append(dict(panel=pn, book=bn, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                           H1=m1["Sharpe"], H2=m2["Sharpe"]))
    print(pd.DataFrame(ft).to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n## SURVIVORSHIP (PROTOCOL rule 9): U56 and B136 are CURRENT-CONSTITUENT lists; the "
          "SMALL panel is a current sub-$2B screen. Every level (CAGR, Sharpe, 4b count) is an "
          "UPPER bound. The GAP is a difference of the SAME statistic on the SAME book under two "
          "aggregations, so a level bias moves both terms together and G1-G3 are first-order "
          "immune; G4's OOS levels are not, and are quoted as upper bounds.")

if __name__ == "__main__":
    main()

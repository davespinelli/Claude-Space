#!/usr/bin/env python3
"""IDEA 2244 (lane cloud, 2026-09-22): is the SHIPPED n = 5 DOMINATED BY ITS OWN LADDER?

Idea 953 found the v1 ranked book's shipped `n = 5` beaten OUT OF SAMPLE by every rung
n >= 10 on U56 and B136, while on SMALL the ladder runs the other way.  A default that
most of its own ladder dominates on two panels and inverts on the third is an UNPRICED
DIAL, not a default.

This run walks n at a FIXED GROSS on all three panels, publishes ALL grid points, scores
BOTH KEEP paths at every rung, and runs the rule-8 walk-forward (n chosen on 2009-2016
only, 2017-2026 read ONCE).

Two tuned dials and no more:  n  and  PANEL.
Reported, not tuned: cost rung {0,10,25,50} bps, cadence {W,M}, gross (fixed 0.75).

Book:  baseline.rules_v1_weights(px, n=n, w=gross/n, max_vol=0.60, vol_scale=True)
       i.e. the SHIPPED v1 composite/eligibility, with the per-name weight solved so that
       TARGET GROSS IS CONSTANT across the ladder.  Without that solve, walking n walks
       gross too and the ladder is a sizing ladder, not a breadth ladder.

Survivorship caveat: the SMALL panel is CURRENT constituents of a sub-$2B screen
(data/SMALL_PANEL_README.md); U56/B136 are current constituents likewise.  Every
SMALL number below is survivorship-inflated and is reported, never adopted alone.

Deterministic, standalone: python3 research/backtests/2026-09-22_shipped-n5-vs-its-own-ladder_cloud.py
"""
import sys, json, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, rebalance_mask, metrics  # noqa

OUT = Path(__file__).with_suffix("")
COSTS = [0, 10, 25, 50]
CADENCES = ["W", "M"]
NLADDER = [3, 5, 10, 15, 20, 30, 40]
GROSS = 0.75                 # the live book's gross; fixed, not tuned
SHIPPED_N = 5
IS_END = "2016-12-31"        # PROTOCOL rule 8
OOS_START = "2017-01-01"

# ---------------------------------------------------------------- fast engine
def fast_backtest(px: pd.DataFrame, w: pd.DataFrame, cost_bps: float, freq: str):
    """numpy re-implementation of engine.backtest, gate-verified below to ~1e-16."""
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).fillna(0.0).shift(1).values   # row 0 is NaN, exactly as engine leaves it
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n = len(px.index); k = px.shape[1]
    held = np.empty((n, k)); turn = np.zeros(n); cur = np.zeros(k)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]; turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    port = np.nansum(held * rets, axis=1) - turn * cost_bps / 1e4   # pandas .sum(axis=1) skips NaN
    return pd.Series(port, index=px.index), pd.Series(turn, index=px.index)

def m3(r):
    m = metrics(r); return m["CAGR"], m["Sharpe"], m["MaxDD"]

def legs(r, spy, base, start):
    """Both KEEP paths for one return stream over [start:]."""
    r, spy, base = r.loc[start:], spy.loc[start:], base.loc[start:]
    h = len(r) // 2
    C, S, D = m3(r); bC, bS, bD = m3(base); sC, sS, sD = m3(spy)
    H1, H2 = metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]
    bH1, bH2 = metrics(base.iloc[:h])["Sharpe"], metrics(base.iloc[h:])["Sharpe"]
    sH1, sH2 = metrics(spy.iloc[:h])["Sharpe"], metrics(spy.iloc[h:])["Sharpe"]
    keep4a = (H1 > bH1) and (H2 > bH2) and (D >= bD)
    dd_cap = 0.60 * sD                    # sD is negative; cap is 60% of SPY's depth
    cagr_floor = 0.70 * sC
    keep4b_full = (H1 > sH1) and (H2 > sH2) and (D >= dd_cap) and (C >= cagr_floor)
    return dict(CAGR=C, Sharpe=S, MaxDD=D, H1=H1, H2=H2,
                base_CAGR=bC, base_Sharpe=bS, base_MaxDD=bD, base_H1=bH1, base_H2=bH2,
                spy_CAGR=sC, spy_Sharpe=sS, spy_MaxDD=sD, spy_H1=sH1, spy_H2=sH2,
                dd_cap=dd_cap, cagr_floor=cagr_floor,
                keep4a=keep4a, keep4b_full=keep4b_full,
                turn_yr=np.nan)

def oos_legs(r, spy, base):
    """4b on the OOS window alone (2017-2026), plus the 4a comparison there."""
    r, spy, base = r.loc[OOS_START:], spy.loc[OOS_START:], base.loc[OOS_START:]
    C, S, D = m3(r); bC, bS, bD = m3(base); sC, sS, sD = m3(spy)
    return dict(oos_CAGR=C, oos_Sharpe=S, oos_MaxDD=D,
                oos_base_CAGR=bC, oos_base_Sharpe=bS, oos_base_MaxDD=bD,
                oos_spy_CAGR=sC, oos_spy_Sharpe=sS, oos_spy_MaxDD=sD,
                oos_4b=(S > sS) and (D >= 0.60 * sD) and (C >= 0.70 * sC))

# ---------------------------------------------------------------- panels
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    dropped = [c for c in px.columns if c != "SPY" and c in bad]
    px = px[keep]
    print(f"  SMALL: dropped {len(dropped)} names with max_1d_move >= 1.0; "
          f"{px.shape[1]-1} names remain (SURVIVORSHIP: current constituents only)")
    return px

def get_panels():
    return {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL": small_panel()}

def book(px, n, gross=GROSS):
    return rules_v1_weights(px, n=n, w=gross / n, max_vol=0.60, vol_scale=True)

# ---------------------------------------------------------------- run
def main():
    t0 = time.time()
    panels = get_panels()
    log = []

    # ---- GATES: the fast engine must reproduce engine.backtest exactly
    gates = []
    for pname, px in panels.items():
        w = book(px, 20)
        for freq in ("W", "M"):
            ref = engine_backtest(px, w, cost_bps=10, freq=freq)["returns"]
            fast, _ = fast_backtest(px, w, 10, freq)
            d = (ref - fast).values
            gates.append(dict(gate=f"G1 fast==engine {pname}/{freq}",
                              max_abs_diff=float(np.abs(d[~np.isnan(d)]).max()),
                              nan_rows_both=int((ref.isna() & fast.isna()).sum()),
                              nan_rows_disagree=int((ref.isna() ^ fast.isna()).sum())))
    # G2: the shipped book at w=0.15,n=5 is reproduced by the solve at gross=0.75
    for pname, px in panels.items():
        a = rules_v1_weights(px, n=5, w=0.15)
        b = book(px, 5, 0.75)
        gates.append(dict(gate=f"G2 shipped n=5 == gross-solved {pname}",
                          max_abs_diff=float(np.abs((a - b).values).max())))
    gdf = pd.DataFrame(gates); gdf.to_csv(f"{OUT}.gates.csv", index=False)
    print("\n=== GATES ===\n" + gdf.to_string(index=False))
    assert gdf["max_abs_diff"].max() < 1e-12, "gate failed"

    # ---- GRID: every (panel, n, cadence, cost) point published
    rows = []
    for pname, px in panels.items():
        start = px.index[260]                       # warm-up, same convention as baseline.compare
        spy = px["SPY"].pct_change().fillna(0.0)
        wv2 = rules_v2_weights(px)                  # live RULES v2, weekly, same panel
        base_by_cost = {}
        for c in COSTS:
            base_by_cost[c], _ = fast_backtest(px, wv2, c, "W")
        for n in NLADDER:
            w = book(px, n)
            for freq in CADENCES:
                for c in COSTS:
                    r, turn = fast_backtest(px, w, c, freq)
                    d = legs(r, spy, base_by_cost[c], start)
                    d.update(oos_legs(r, spy, base_by_cost[c]))
                    yrs = len(r.loc[start:]) / 252
                    d["turn_yr"] = float(np.nansum(turn.loc[start:].values) / yrs)
                    d.update(panel=pname, n=n, cadence=freq, cost_bps=c, gross=GROSS)
                    rows.append(d)
        print(f"  {pname}: {len(NLADDER)*len(CADENCES)*len(COSTS)} cells  [{time.time()-t0:.0f}s]")
    g = pd.DataFrame(rows)
    front = ["panel", "n", "cadence", "cost_bps", "gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
             "turn_yr", "keep4a", "keep4b_full", "oos_CAGR", "oos_Sharpe", "oos_MaxDD", "oos_4b"]
    g = g[front + [c for c in g.columns if c not in front]]
    g.to_csv(f"{OUT}.grid.csv", index=False)
    print(f"\nGRID: {len(g)} cells -> {OUT.name}.grid.csv")

    # ---- HEADLINE LADDER at the live rung (W, 10 bps)
    hl = g[(g.cadence == "W") & (g.cost_bps == 10)].copy()
    print("\n=== LADDER at the LIVE rung (weekly, 10 bps, gross 0.75) ===")
    for pname in panels:
        sub = hl[hl.panel == pname].sort_values("n")
        print(f"\n-- {pname} --   RULES v2 {sub.base_CAGR.iloc[0]:.2%}/{sub.base_Sharpe.iloc[0]:.4f}/"
              f"{sub.base_MaxDD.iloc[0]:.2%}   SPY {sub.spy_CAGR.iloc[0]:.2%}/"
              f"{sub.spy_Sharpe.iloc[0]:.4f}/{sub.spy_MaxDD.iloc[0]:.2%}  "
              f"(4b caps: DD {sub.dd_cap.iloc[0]:.2%}, CAGR {sub.cagr_floor.iloc[0]:.2%})")
        print(sub[["n", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "turn_yr",
                   "oos_CAGR", "oos_Sharpe", "oos_MaxDD", "keep4a", "keep4b_full", "oos_4b"]]
              .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---- DOMINANCE of the shipped n=5 by its own ladder, at every (panel,cadence,cost)
    dom = []
    for (pname, freq, c), sub in g.groupby(["panel", "cadence", "cost_bps"]):
        s = sub.set_index("n")
        for col, lbl in [("oos_Sharpe", "OOS Sharpe"), ("Sharpe", "full Sharpe"),
                         ("CAGR", "full CAGR"), ("MaxDD", "full MaxDD")]:
            v5 = s.loc[SHIPPED_N, col]
            better = [int(k) for k in s.index if k != SHIPPED_N and s.loc[k, col] > v5]
            dom.append(dict(panel=pname, cadence=freq, cost_bps=c, statistic=lbl,
                            shipped_n5=v5, n_rungs=len(s) - 1, n_beating_shipped=len(better),
                            best_rung=int(s[col].idxmax()), best_value=s[col].max(),
                            rungs_beating=";".join(map(str, better))))
    dd = pd.DataFrame(dom); dd.to_csv(f"{OUT}.dominance.csv", index=False)
    print("\n=== DOMINANCE of the shipped n=5 (how many of its own 6 sibling rungs beat it) ===")
    piv = dd[dd.statistic == "OOS Sharpe"].pivot_table(index=["panel", "cadence"],
                                                       columns="cost_bps", values="n_beating_shipped")
    print("OOS Sharpe, count of rungs beating n=5, by cost rung:\n" + piv.to_string())
    piv2 = dd[dd.statistic == "OOS Sharpe"].pivot_table(index=["panel", "cadence"],
                                                        columns="cost_bps", values="best_rung")
    print("\nOOS-Sharpe argmax n, by cost rung:\n" + piv2.to_string())

    # ---- KEEP counts
    print("\n=== KEEP PATH COUNTS over all %d cells ===" % len(g))
    print("4a           : %d" % int(g.keep4a.sum()))
    print("4b (full)    : %d" % int(g.keep4b_full.sum()))
    print("4b (OOS leg) : %d" % int(g.oos_4b.sum()))
    print("4b FULL+OOS  : %d" % int((g.keep4b_full & g.oos_4b).sum()))
    print("BOTH 4a+4b   : %d" % int((g.keep4a & g.keep4b_full & g.oos_4b).sum()))
    pas = g[g.keep4b_full & g.oos_4b]
    if len(pas):
        print("\n4b FULL+OOS passing cells:")
        print(pas[["panel", "n", "cadence", "cost_bps", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                   "oos_CAGR", "oos_Sharpe", "oos_MaxDD", "turn_yr", "keep4a"]]
              .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    pas.to_csv(f"{OUT}.passes.csv", index=False)

    # ---- RULE 8 walk-forward: n chosen on IS (2009-2016) by IS Sharpe, OOS read once
    wf = []
    for pname, px in panels.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0)
        wv2 = rules_v2_weights(px)
        for freq in CADENCES:
            for c in COSTS:
                base, _ = fast_backtest(px, wv2, c, "W")
                is_sh = {}
                streams = {}
                for n in NLADDER:
                    r, _ = fast_backtest(px, book(px, n), c, freq)
                    streams[n] = r
                    is_sh[n] = metrics(r.loc[start:IS_END])["Sharpe"]
                pick = max(is_sh, key=is_sh.get)
                for tag, n in [("CHOSEN(IS-Sharpe)", pick), ("SHIPPED n=5", SHIPPED_N),
                               ("ORACLE(best OOS)", None)]:
                    if n is None:
                        n = max(NLADDER, key=lambda k: metrics(streams[k].loc[OOS_START:])["Sharpe"])
                    r = streams[n]
                    C, S, D = m3(r.loc[OOS_START:])
                    bC, bS, bD = m3(base.loc[OOS_START:])
                    sC, sS, sD = m3(spy.loc[OOS_START:])
                    wf.append(dict(panel=pname, cadence=freq, cost_bps=c, arm=tag, n=n,
                                   IS_Sharpe=is_sh[n], OOS_CAGR=C, OOS_Sharpe=S, OOS_MaxDD=D,
                                   base_OOS_CAGR=bC, base_OOS_Sharpe=bS, base_OOS_MaxDD=bD,
                                   spy_OOS_CAGR=sC, spy_OOS_Sharpe=sS, spy_OOS_MaxDD=sD,
                                   beats_base_Sharpe=S > bS, beats_spy_Sharpe=S > sS,
                                   oos_4b=(S > sS) and (D >= 0.60 * sD) and (C >= 0.70 * sC)))
    w8 = pd.DataFrame(wf); w8.to_csv(f"{OUT}.walkforward.csv", index=False)
    print("\n=== RULE 8 WALK-FORWARD (n chosen on 2009-2016 IS Sharpe; 2017-2026 read ONCE) ===")
    print(w8[w8.cost_bps == 10].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    ch = w8[w8.arm == "CHOSEN(IS-Sharpe)"]; sh = w8[w8.arm == "SHIPPED n=5"]
    mg = ch.merge(sh, on=["panel", "cadence", "cost_bps"], suffixes=("_ch", "_sh"))
    print("\nCHOSEN vs SHIPPED n=5, OOS: chooser wins Sharpe in %d of %d families; "
          "median dOOS Sharpe %+.4f; median dOOS CAGR %+.2f pp; median dOOS MaxDD %+.2f pp"
          % (int((mg.OOS_Sharpe_ch > mg.OOS_Sharpe_sh).sum()), len(mg),
             (mg.OOS_Sharpe_ch - mg.OOS_Sharpe_sh).median(),
             100 * (mg.OOS_CAGR_ch - mg.OOS_CAGR_sh).median(),
             100 * (mg.OOS_MaxDD_ch - mg.OOS_MaxDD_sh).median()))
    print("Chooser's pick n by (panel,cadence,cost):")
    print(ch.pivot_table(index=["panel", "cadence"], columns="cost_bps", values="n").to_string())
    print("\n4b-OOS pass counts by arm: " +
          ", ".join(f"{a} {int(w8[w8.arm==a].oos_4b.sum())}/{len(w8[w8.arm==a])}"
                    for a in w8.arm.unique()))

    # ---- IS/OOS RANK PERSISTENCE of the n dial (is n learnable at all?)
    per = []
    for (pname, freq, c), sub in g.groupby(["panel", "cadence", "cost_bps"]):
        pass  # persistence computed from walkforward streams below
    for pname, px in panels.items():
        start = px.index[260]
        for freq in CADENCES:
            for c in COSTS:
                iss, oss = [], []
                for n in NLADDER:
                    r, _ = fast_backtest(px, book(px, n), c, freq)
                    iss.append(metrics(r.loc[start:IS_END])["Sharpe"])
                    oss.append(metrics(r.loc[OOS_START:])["Sharpe"])
                # Spearman = Pearson on ranks (scipy is not installed in the sandbox)
                rho = pd.Series(iss).rank().corr(pd.Series(oss).rank())
                per.append(dict(panel=pname, cadence=freq, cost_bps=c, spearman_IS_OOS=rho))
    pdf = pd.DataFrame(per); pdf.to_csv(f"{OUT}.persistence.csv", index=False)
    print("\n=== IS->OOS rank persistence of the n ladder (spearman over 7 rungs) ===")
    print(pdf.pivot_table(index=["panel", "cadence"], columns="cost_bps",
                          values="spearman_IS_OOS").to_string())
    print(f"\nmedian spearman {pdf.spearman_IS_OOS.median():+.3f} over {len(pdf)} families")
    print(f"\ntotal {time.time()-t0:.0f}s")

if __name__ == "__main__":
    main()

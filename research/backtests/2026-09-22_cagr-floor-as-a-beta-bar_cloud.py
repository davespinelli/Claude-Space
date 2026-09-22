#!/usr/bin/env python3
"""IDEA 955 (lane cloud, 2026-09-22): is the 4b CAGR FLOOR a BETA BAR in disguise?

PROTOCOL rule 4b's CAGR leg is `CAGR >= 0.70 * CAGR(SPY)`.  Idea 944 found it the record's
largest binding leg (68.8% of FAIL rows, 16.9% as the SOLE binder) and found BAND03 / BAND06 /
RULESV2 failing on it at ALL 21 rebalance phases with drawdowns nowhere near the DD cap.  A floor
set as a fraction of SPY's CAGR may be rejecting books purely for carrying LESS EQUITY BETA
rather than less skill.

This run prices the floor against a BETA-MATCHED COMPARAND on a gross ladder, publishes every
grid point, scores BOTH KEEP paths at every cell under EVERY floor definition, and runs the
rule-8 walk-forward (gross chosen on 2009-2016 only, 2017-2026 read ONCE).

Two tuned dials and no more:  GROSS LADDER  and  FLOOR DEFINITION.
Reported, not tuned: panel {U56,B136,SMALL}, book {RULESV2 band .03, BAND06, V1N20},
cadence {W,M}, cost rung {0,10,25,50} bps.

FLOOR DEFINITIONS (the dial under test)
  F_SPY70   CAGR >= 0.70 * CAGR(SPY)                      -- the INCUMBENT
  F_BETA    CAGR >= 0.70 * beta * CAGR(SPY)               -- beta-matched comparand
  F_GROSS   CAGR >= 0.70 * mean_realised_gross * CAGR(SPY)-- exposure-matched comparand
  F_NONE    no floor                                      -- zero-information control, bounds
                                                             how much of 4b the floor IS

LEGALITY: beta and mean gross are IN-SAMPLE statistics of the book itself, so under rule 8 the
floor is rebuilt from the 2009-2016 half alone (`beta_is`, `gross_is`) and the OOS half is read
once.  The full-sample arm is reported as a measurement, never as a rule-8 result.

LEVERAGE: PROTOCOL rule 2 forbids leverage unless the idea says so.  Gross rungs 1.25 and 1.50
are priced and published as an UNFINANCED, NOT-ADOPTABLE arm (`levered=True`) and are EXCLUDED
from every KEEP count below.

Survivorship caveat: all three panels are CURRENT constituents; SMALL is the sub-$2B screen with
the 54 names whose max_1d_move >= 1.0 dropped.  Every SMALL number is survivorship-inflated.

Deterministic, standalone: python3 research/backtests/2026-09-22_cagr-floor-as-a-beta-bar_cloud.py
"""
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, band_state  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, rebalance_mask, metrics  # noqa

OUT = Path(__file__).with_suffix("")
COSTS = [0, 10, 25, 50]
CADENCES = ["W", "M"]
GROSS = [0.25, 0.50, 0.75, 1.00, 1.25, 1.50]
LEVERED = {1.25, 1.50}
FLOORS = ["F_SPY70", "F_BETA", "F_GROSS", "F_NONE"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

def fast_backtest(px, w, cost_bps, freq):
    """numpy re-implementation of engine.backtest, gate-verified to 0.000000 below."""
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).fillna(0.0).shift(1).values      # row 0 NaN, exactly as engine
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n, k = rets.shape
    held = np.empty((n, k)); turn = np.zeros(n); cur = np.zeros(k); g = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]; turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur; g[i] = np.nansum(cur)
        growth = cur * (1.0 + rets[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    port = np.nansum(held * rets, axis=1) - turn * cost_bps / 1e4
    return (pd.Series(port, index=px.index), pd.Series(turn, index=px.index),
            pd.Series(g, index=px.index))

def beta(r, spy):
    a, b = r.values, spy.values
    m = ~(np.isnan(a) | np.isnan(b))
    a, b = a[m], b[m]
    v = np.var(b, ddof=1)          # match np.cov's ddof=1, else beta(SPY,SPY) != 1 exactly
    return float(np.cov(a, b, ddof=1)[0, 1] / v) if v > 0 else np.nan

def m3(r):
    m = metrics(r); return m["CAGR"], m["Sharpe"], m["MaxDD"]

def floor_value(kind, spy_cagr, bta, gr):
    if kind == "F_SPY70": return 0.70 * spy_cagr
    if kind == "F_BETA":  return 0.70 * bta * spy_cagr
    if kind == "F_GROSS": return 0.70 * gr * spy_cagr
    return -np.inf

# ------------------------------------------------------------------ books
def bk_rulesv2(px, g): return rules_v2_weights(px, band=0.03, gross=g)
def bk_band06(px, g):  return rules_v2_weights(px, band=0.06, gross=g)
def bk_v1n20(px, g):   return rules_v1_weights(px, n=20, w=g / 20, max_vol=0.60, vol_scale=True)
BOOKS = {"RULESV2": bk_rulesv2, "BAND06": bk_band06, "V1N20": bk_v1n20}

def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    print(f"  SMALL: dropped {px.shape[1]-len(keep)} names with max_1d_move >= 1.0; "
          f"{len(keep)-1} remain (SURVIVORSHIP: current constituents only)")
    return px[keep]

def main():
    t0 = time.time()
    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL": small_panel()}

    # ---------------- GATES
    gates = []
    for pn, px in panels.items():
        w = bk_rulesv2(px, 0.75)
        for freq in ("W", "M"):
            ref = engine_backtest(px, w, cost_bps=10, freq=freq)["returns"]
            fast, _, _ = fast_backtest(px, w, 10, freq)
            d = (ref - fast).values
            gates.append(dict(gate=f"G1 fast==engine {pn}/{freq}",
                              max_abs_diff=float(np.abs(d[~np.isnan(d)]).max())))
        gates.append(dict(gate=f"G2 bk_rulesv2(0.75)==baseline.rules_v2_weights {pn}",
                          max_abs_diff=float(np.abs((w - rules_v2_weights(px)).values).max())))
        # G3: beta of SPY on itself is 1 to machine precision
        spy = px["SPY"].pct_change().fillna(0.0).loc[px.index[260]:]
        gates.append(dict(gate=f"G3 beta(SPY,SPY)==1 {pn}", max_abs_diff=abs(beta(spy, spy) - 1.0)))
    gdf = pd.DataFrame(gates); gdf.to_csv(f"{OUT}.gates.csv", index=False)
    print("\n=== GATES ===\n" + gdf.to_string(index=False))
    assert gdf.max_abs_diff.max() < 1e-12, "gate failed"

    # ---------------- GRID
    rows = []
    for pn, px in panels.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0)
        spy_f, spy_is, spy_o = spy.loc[start:], spy.loc[start:IS_END], spy.loc[OOS_START:]
        sC, sS, sD = m3(spy_f); sCo, sSo, sDo = m3(spy_o)
        h = len(spy_f) // 2
        sH1, sH2 = metrics(spy_f.iloc[:h])["Sharpe"], metrics(spy_f.iloc[h:])["Sharpe"]
        for bn, bf in BOOKS.items():
            for g in GROSS:
                w = bf(px, g)
                for freq in CADENCES:
                    for c in COSTS:
                        r, turn, gs = fast_backtest(px, w, c, freq)
                        rf, ris, ro = r.loc[start:], r.loc[start:IS_END], r.loc[OOS_START:]
                        C, S, D = m3(rf); Co, So, Do = m3(ro)
                        H1 = metrics(rf.iloc[:h])["Sharpe"]; H2 = metrics(rf.iloc[h:])["Sharpe"]
                        b_f, b_is = beta(rf, spy_f), beta(ris, spy_is)
                        gr_f = float(gs.loc[start:].mean()); gr_is = float(gs.loc[start:IS_END].mean())
                        d = dict(panel=pn, book=bn, gross=g, cadence=freq, cost_bps=c,
                                 levered=g in LEVERED,
                                 CAGR=C, Sharpe=S, MaxDD=D, H1=H1, H2=H2,
                                 beta_full=b_f, beta_is=b_is, mean_gross=gr_f, mean_gross_is=gr_is,
                                 turn_yr=float(np.nansum(turn.loc[start:].values) / (len(rf) / 252)),
                                 oos_CAGR=Co, oos_Sharpe=So, oos_MaxDD=Do,
                                 spy_CAGR=sC, spy_Sharpe=sS, spy_MaxDD=sD,
                                 spy_H1=sH1, spy_H2=sH2,
                                 spy_oos_CAGR=sCo, spy_oos_Sharpe=sSo, spy_oos_MaxDD=sDo,
                                 dd_cap=0.60 * sD, dd_cap_oos=0.60 * sDo,
                                 leg_sharpe=(H1 > sH1) and (H2 > sH2),
                                 leg_dd=D >= 0.60 * sD,
                                 leg_oos_sharpe=So > sSo, leg_oos_dd=Do >= 0.60 * sDo)
                        for k in FLOORS:
                            fv = floor_value(k, sC, b_f, gr_f)
                            fo = floor_value(k, sCo, b_is, gr_is)   # OOS floor uses IS-only beta/gross
                            d[f"floor_{k}"] = fv
                            d[f"leg_cagr_{k}"] = C >= fv
                            d[f"leg_oos_cagr_{k}"] = Co >= fo
                            d[f"keep4b_{k}"] = (d["leg_sharpe"] and d["leg_dd"] and (C >= fv))
                            d[f"keep4b_oos_{k}"] = (d["leg_oos_sharpe"] and d["leg_oos_dd"]
                                                    and (Co >= fo))
                        rows.append(d)
        print(f"  {pn}: done [{time.time()-t0:.0f}s]")
    g = pd.DataFrame(rows)
    # 4a against live RULES v2 on the same panel/cost (weekly, gross 0.75 = the live book)
    base = (g[(g.book == "RULESV2") & (g.gross == 0.75) & (g.cadence == "W")]
            .set_index(["panel", "cost_bps"])[["Sharpe", "H1", "H2", "MaxDD", "CAGR"]])
    g["base_H1"] = [base.loc[(p, c), "H1"] for p, c in zip(g.panel, g.cost_bps)]
    g["base_H2"] = [base.loc[(p, c), "H2"] for p, c in zip(g.panel, g.cost_bps)]
    g["base_MaxDD"] = [base.loc[(p, c), "MaxDD"] for p, c in zip(g.panel, g.cost_bps)]
    g["base_Sharpe"] = [base.loc[(p, c), "Sharpe"] for p, c in zip(g.panel, g.cost_bps)]
    g["base_CAGR"] = [base.loc[(p, c), "CAGR"] for p, c in zip(g.panel, g.cost_bps)]
    g["keep4a"] = (g.H1 > g.base_H1) & (g.H2 > g.base_H2) & (g.MaxDD >= g.base_MaxDD)
    g.to_csv(f"{OUT}.grid.csv", index=False)
    print(f"\nGRID: {len(g)} cells ({int((~g.levered).sum())} unlevered) -> {OUT.name}.grid.csv")

    U = g[~g.levered]

    # ---------------- A. IS THE CAGR MARGIN A BETA OBJECT?
    print("\n=== A. IS THE CAGR LEG A BETA BAR? (unlevered cells) ===")
    art = []
    for (pn, freq, c), sub in U.groupby(["panel", "cadence", "cost_bps"]):
        x, y = sub.beta_full, sub.CAGR
        rho = x.rank().corr(y.rank())
        pear = x.corr(y)
        # R^2 of CAGR on beta
        r2 = pear ** 2
        # residual spread of CAGR once beta is charged
        fit = np.polyfit(x, y, 1)
        resid = y - np.polyval(fit, x)
        art.append(dict(panel=pn, cadence=freq, cost_bps=c, n=len(sub), spearman=rho,
                        pearson=pear, r2=r2, slope=fit[0], resid_sd=resid.std(),
                        cagr_sd=y.std(), beta_lo=x.min(), beta_hi=x.max()))
    adf = pd.DataFrame(art); adf.to_csv(f"{OUT}.betafit.csv", index=False)
    print(adf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"\npooled: median spearman(beta, CAGR) {adf.spearman.median():+.4f}, median R^2 "
          f"{adf.r2.median():.4f}, median residual sd {adf.resid_sd.median():.4f} against a CAGR "
          f"sd of {adf.cagr_sd.median():.4f} -> beta explains "
          f"{100*(1-(adf.resid_sd/adf.cagr_sd).median()**2):.1f}% of the CAGR spread")

    # ---------------- B. WHICH CAGR-LEG FAILURES SURVIVE A BETA-MATCHED FLOOR?
    print("\n=== B. CENSUS OF CAGR-LEG FAILURES (unlevered, %d cells) ===" % len(U))
    fail = U[~U.leg_cagr_F_SPY70]
    surv = fail[fail.leg_cagr_F_BETA]
    real = surv[surv.leg_sharpe & surv.leg_dd]
    realo = real[real.keep4b_oos_F_BETA]
    cen = dict(cells=len(U),
               fail_incumbent=len(fail),
               survive_beta_floor=len(surv),
               survive_and_clear_other_legs=len(real),
               survive_and_clear_OOS_too=len(realo),
               survive_gross_floor=int(fail.leg_cagr_F_GROSS.sum()))
    print(pd.Series(cen).to_string())
    print("\n4b pass counts by FLOOR DEFINITION (unlevered):")
    cnt = pd.DataFrame({k: dict(full=int(U[f"keep4b_{k}"].sum()),
                                oos=int(U[f"keep4b_oos_{k}"].sum()),
                                full_and_oos=int((U[f"keep4b_{k}"] & U[f"keep4b_oos_{k}"]).sum()))
                        for k in FLOORS}).T
    print(cnt.to_string())
    cnt.to_csv(f"{OUT}.floorcounts.csv")
    print("\n4a (vs live RULES v2, same panel and cost): %d of %d unlevered cells"
          % (int(U.keep4a.sum()), len(U)))
    print("BOTH 4a and 4b(incumbent floor) full+OOS: %d"
          % int((U.keep4a & U.keep4b_F_SPY70 & U.keep4b_oos_F_SPY70).sum()))
    print("BOTH 4a and 4b(BETA floor) full+OOS:      %d"
          % int((U.keep4a & U.keep4b_F_BETA & U.keep4b_oos_F_BETA).sum()))
    surv.to_csv(f"{OUT}.survivors.csv", index=False)
    if len(real):
        print("\nCells the INCUMBENT floor rejects that clear EVERY OTHER 4b leg under the "
              "beta-matched floor (full sample):")
        print(real[["panel", "book", "gross", "cadence", "cost_bps", "CAGR", "Sharpe", "MaxDD",
                    "H1", "H2", "beta_full", "floor_F_SPY70", "floor_F_BETA", "keep4a",
                    "keep4b_oos_F_BETA"]]
              .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    real.to_csv(f"{OUT}.survivors_allelegs.csv", index=False)

    # ---------------- C. WHAT THE BETA FLOOR COSTS: how far it moves the bar
    print("\n=== C. HOW MUCH THE BETA FLOOR LOWERS THE BAR (unlevered, 10 bps) ===")
    s10 = U[U.cost_bps == 10]
    mv = (s10.floor_F_SPY70 - s10.floor_F_BETA) * 100
    print(f"median bar reduction {mv.median():+.2f} pp of CAGR, IQR "
          f"[{mv.quantile(.25):+.2f}, {mv.quantile(.75):+.2f}] pp; the incumbent bar itself is "
          f"{100*s10.floor_F_SPY70.median():.2f} pp")
    print(s10.groupby(["panel", "book"]).apply(
        lambda d: pd.Series({"median_beta": d.beta_full.median(),
                             "median_bar_cut_pp": ((d.floor_F_SPY70 - d.floor_F_BETA) * 100).median(),
                             "cagr_fail_incumbent": int((~d.leg_cagr_F_SPY70).sum()),
                             "cagr_fail_beta": int((~d.leg_cagr_F_BETA).sum()),
                             "n": len(d)}), include_groups=False
    ).to_string(float_format=lambda x: f"{x:.4f}"))

    # ---------------- D. RULE 8 WALK-FORWARD
    print("\n=== D. RULE 8 (gross chosen on 2009-2016 IS Sharpe among cells the floor admits "
          "IN SAMPLE; 2017-2026 read ONCE) ===")
    wf = []
    for pn, px in panels.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0)
        spy_is, spy_o = spy.loc[start:IS_END], spy.loc[OOS_START:]
        sC_is = metrics(spy_is)["CAGR"]; sD_is = metrics(spy_is)["MaxDD"]
        sCo, sSo, sDo = m3(spy_o)
        for bn, bf in BOOKS.items():
            for freq in CADENCES:
                for c in COSTS:
                    cand = {}
                    for gg in GROSS:
                        if gg in LEVERED: continue
                        r, _, gs = fast_backtest(px, bf(px, gg), c, freq)
                        ris = r.loc[start:IS_END]
                        cand[gg] = dict(r=r, is_S=metrics(ris)["Sharpe"],
                                        is_C=metrics(ris)["CAGR"], is_D=metrics(ris)["MaxDD"],
                                        b_is=beta(ris, spy_is),
                                        gr_is=float(gs.loc[start:IS_END].mean()))
                    for k in FLOORS:
                        adm = [gg for gg, v in cand.items()
                               if v["is_C"] >= floor_value(k, sC_is, v["b_is"], v["gr_is"])
                               and v["is_D"] >= 0.60 * sD_is]
                        pool = adm if adm else list(cand)
                        pick = max(pool, key=lambda gg: cand[gg]["is_S"])
                        ro = cand[pick]["r"].loc[OOS_START:]
                        C, S, D = m3(ro)
                        fo = floor_value(k, sCo, cand[pick]["b_is"], cand[pick]["gr_is"])
                        wf.append(dict(panel=pn, book=bn, cadence=freq, cost_bps=c, floor=k,
                                       admitted_IS=len(adm), abstained=len(adm) == 0, pick=pick,
                                       OOS_CAGR=C, OOS_Sharpe=S, OOS_MaxDD=D,
                                       spy_OOS_CAGR=sCo, spy_OOS_Sharpe=sSo, spy_OOS_MaxDD=sDo,
                                       oos_floor=fo,
                                       oos_4b=(S > sSo) and (D >= 0.60 * sDo) and (C >= fo),
                                       oos_4b_incumbent_floor=(S > sSo) and (D >= 0.60 * sDo)
                                       and (C >= 0.70 * sCo)))
    w8 = pd.DataFrame(wf); w8.to_csv(f"{OUT}.walkforward.csv", index=False)
    print(w8[w8.cost_bps == 10].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\nBy floor: picks, abstentions, and OOS 4b pass rate (all %d families):" % (len(w8) // 4))
    summ = w8.groupby("floor").apply(
        lambda d: pd.Series({"median_pick_gross": d["pick"].median(),
                             "abstained": int(d.abstained.sum()),
                             "oos_4b_own_floor": int(d.oos_4b.sum()),
                             "oos_4b_INCUMBENT_floor": int(d.oos_4b_incumbent_floor.sum()),
                             "median_OOS_Sharpe": d.OOS_Sharpe.median(),
                             "median_OOS_CAGR_pp": 100 * d.OOS_CAGR.median(),
                             "median_OOS_MaxDD_pp": 100 * d.OOS_MaxDD.median(),
                             "n": len(d)}), include_groups=False)
    print(summ.to_string(float_format=lambda x: f"{x:.4f}"))
    print(f"\ntotal {time.time()-t0:.0f}s")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Idea 290 - "is-the-de-gross-cost-a-cash-drag-identity" (lane B, 2026-09-06).

The question
------------
Idea 52 (lane B, 2026-09-06) found that on the 439-name sub-$2B panel the 200d gate's cost
under DE-GROSSING is 4.78-8.33 pp/yr of CAGR and moves only 6.45 -> 5.61 pp across a band
dial that removes ~76% of the SAME gate's cost under constant exposure (RESPREAD: 2.82 ->
0.69 pp at weekly, through zero at slower cadence).  A cost that is near-invariant to a churn
dial is not a churn cost.  The QUEUE's hypothesis: the de-gross cost is just

        (1 - mean exposure)  x  the panel's own compounding,

i.e. cash drag, and every de-gross number in the record is a re-pricing of EXPOSURE rather
than of the gate.  QUEUE wording: "regress the DEGROSS-minus-RESPREAD CAGR gap on mean gross
across the 36 band x cadence x gate cells and report the residual."

Three pre-registered tests (bars fixed before any number was read)
------------------------------------------------------------------
P1  ALGEBRAIC EXACTNESS.  Idea 52's two constructions share one gate mask g and differ only
    in the denominator:  RESPREAD w = g/k_t * G  (k_t = names gated IN),  DEGROSS
    w = g/n_t * G  (n_t = names LIVE).  So at every rebalance w_dg = (k_t/n_t) * w_rs, and
    the engine's between-rebalance drift preserves proportionality (both books renormalise
    the SAME growth vector against their own total, so held_dg,t = c_t * held_rs,t for a
    scalar c_t at every t).  If that is right the gross return streams satisfy
    r_dg,t = c_t * r_rs,t EXACTLY.  BAR: max_t |r_dg,t - c_t * r_rs,t| < 1e-12 at 0 bps.
    P1 is a claim about the CONSTRUCTION, not about the market; it either holds or the rest
    of this script is measuring something else.

P2  THE QUEUE'S REGRESSION.  gap_pp = CAGR_dg - CAGR_rs (pp/yr) on mean realised gross, OLS
    across the 36 band x cadence x gate cells, at 10 bps and at 0 bps.
    BAR for "identity": R^2 >= 0.95 AND residual sd <= 0.25 pp.

P3  THE STRUCTURAL DECOMPOSITION (the sharper form of the same question).  P1 makes the
    de-gross book a time-varying-leverage version of the respread book, so its CAGR gap
    splits exactly into
        gap(0 bps) = [ constant-leverage cash drag at c_bar ]      <- pure exposure
                   + [ residual from the TIMING of c_t ]           <- the gate's own content
    computed by replaying r_A,t = c_bar * r_rs,t (one number, the cell's own mean leverage)
    and reading its CAGR.  BAR for "the de-gross cost is exposure and nothing else":
    mean |residual| <= 0.25 pp AND mean |residual| <= 10% of mean |gap|.
    A LARGE residual would refute the identity and say de-gross carries real timing.

Tuned parameters (PROTOCOL rule 4: at most two)
------------------------------------------------
    band b   in {0.00, 0.02, 0.03, 0.05, 0.08, 0.12}   (baseline.band_state, RULES v2 form)
    cadence  in {W, M, Q}
Reported at every value, selected at none except inside the rule-8 walk-forward.  Gate form
(MA / MAVOL) and construction (RESPREAD / DEGROSS) are REPORTED dimensions, not tuned: the
whole point is the contrast between them.

Grid: 6 bands x 3 cadences x 2 gates x 2 constructions = 72 cells, each at 10 bps and 0 bps
= 144 backtests, plus 3 cadence-matched no-filter controls x 2 rungs.  Every cell printed.

Walk-forward (PROTOCOL rule 8)
-------------------------------
(band, cadence) chosen on 2010-2016 by in-sample Sharpe INSIDE each of the 4 gate x
construction arms; 2017-2026 read once.  OOS CAGR/Sharpe/MaxDD reported against the LIVE
book (RULES v2 on research/universe.json, same window), SPY, and the no-filter control.

Both KEEP paths evaluated on all 72 cells (4a vs the live book, 4b vs SPY).

SURVIVORSHIP: data/prices_small.csv.gz is a screen of CURRENT sub-$2B constituents - no
delistings.  Every number here is an arm-minus-arm contrast on the SAME names and days
(DEGROSS vs RESPREAD share one gate mask), so the bias very largely cancels out of the
headline; it does not cancel out of the 4a/4b columns, which are levels.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, band_state, rules_v2_weights
from engine import backtest, metrics

COST_BPS = 10
GROSS = 0.75
MAX_VOL = 0.60
BANDS = [0.00, 0.02, 0.03, 0.05, 0.08, 0.12]
CADENCES = ["W", "M", "Q"]
GATES = ["MA", "MAVOL"]
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SCRIPT = Path(__file__).name
OUT = Path(__file__).with_suffix("")

# pre-registered bars
P1_TOL = 1e-12
P2_R2, P2_RESID_SD = 0.95, 0.25          # pp
P3_ABS, P3_FRAC = 0.25, 0.10             # pp, and fraction of the mean gap

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 300)


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.4f}")


# ---------------------------------------------------------------- universe (idea 52's panel)
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv = [c for c in px.columns if c != "SPY" and c not in bad]
    return px[inv], px["SPY"], sorted(bad)


def live_mask(px):
    return px.notna() & px.shift(1).notna()


def gate_mask(px, gate, band):
    g = band_state(px, band)
    if gate == "MAVOL":
        vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        g = g & (vol20 < MAX_VOL)
    return g & px.notna() & px.shift(1).notna()


def book(px, gate, band, construction):
    g = gate_mask(px, gate, band)
    if construction == "RESPREAD":
        k = g.sum(axis=1).clip(lower=1)
        return g.astype(float).div(k, axis=0) * GROSS
    live = live_mask(px)
    n = live.sum(axis=1).clip(lower=1)
    return (g & live).astype(float).div(n, axis=0) * GROSS


def control_book(px):
    live = live_mask(px)
    n = live.sum(axis=1).clip(lower=1)
    return live.astype(float).div(n, axis=0) * GROSS


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def stat(r, r_is, r_oos):
    m, mo, mi = metrics(r), metrics(r_oos), metrics(r_is)
    h1, h2 = halves(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                isCAGR=mi["CAGR"], isSharpe=mi["Sharpe"], isMaxDD=mi["MaxDD"],
                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"])


def fail_4b(s, spy_s):
    t = {"H1": s["H1"] > spy_s["H1"], "H2": s["H2"] > spy_s["H2"],
         "OOS": s["oSharpe"] > spy_s["oSharpe"],
         "DD": abs(s["MaxDD"]) <= 0.60 * abs(spy_s["MaxDD"]),
         "CAGR": s["CAGR"] >= 0.70 * spy_s["CAGR"]}
    f = [k for k, v in t.items() if not v]
    return ",".join(f) if f else "-"


def verdict_4a(s, b):
    return bool(s["H1"] > b["H1"] and s["H2"] > b["H2"] and s["MaxDD"] >= b["MaxDD"])


def ols(x, y):
    """Plain OLS with intercept; returns slope, intercept, R2, residuals."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    X = np.column_stack([np.ones_like(x), x])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    fit = X @ beta
    res = y - fit
    ss_tot = ((y - y.mean()) ** 2).sum()
    r2 = 1 - (res ** 2).sum() / ss_tot if ss_tot > 0 else np.nan
    return beta[1], beta[0], r2, res


def cagr_of(r):
    return metrics(r)["CAGR"]


# ---------------------------------------------------------------- main
def main():
    px, spy_px, bad = small_panel()
    start = px.index[260]
    years = len(px.loc[start:]) / 252
    yrs = px.index.to_series().groupby(px.index.year).count()

    print("=" * 170)
    print(f"Idea 290 is-the-de-gross-cost-a-cash-drag-identity (lane B) | {SCRIPT}")
    print("=" * 170)
    print(f"Panel {px.shape[1]} investable tickers ({len(bad)} excluded, max_1d_move>=1.0); "
          f"{px.index[0].date()} -> {px.index[-1].date()}; evaluation from {start.date()} "
          f"({years:.2f} yrs)")
    print(f"Index sanity (must be ~252/yr): 2013 {yrs.get(2013)}, 2018 {yrs.get(2018)}, 2024 {yrs.get(2024)}")
    if yrs.loc[2013:2024].max() > 300:
        print("!! CALENDAR-DAY INDEX - aborting."); sys.exit(1)
    print(f"Costs {COST_BPS} bps (and a 0 bps rung), gross {GROSS}, next-day execution.")
    print(f"Pre-registered bars: P1 max|r_dg - c_t r_rs| < {P1_TOL:g};  "
          f"P2 R2 >= {P2_R2} and resid sd <= {P2_RESID_SD} pp;  "
          f"P3 mean|resid| <= {P3_ABS} pp AND <= {P3_FRAC:.0%} of mean|gap|.")

    def slices(r):
        r = r.loc[start:]
        return r, r.loc[:IS_END], r.loc[OOS_START:]

    spy_r, spy_is, spy_oos = slices(spy_px.pct_change().fillna(0.0))
    spy_s = stat(spy_r, spy_is, spy_oos)

    # ---------------- reference books -----------------------------------
    print("\n" + "-" * 170)
    print("REFERENCE BOOKS")
    print("-" * 170)
    ctrl, ctrl0 = {}, {}
    for cad in CADENCES:
        rc = backtest(px, control_book(px), cost_bps=COST_BPS, freq=cad)
        ctrl[cad] = stat(*slices(rc["returns"]))
        ctrl0[cad] = cagr_of(backtest(px, control_book(px), cost_bps=0, freq=cad)["returns"].loc[start:])

    px_u = load_universe()
    rv2 = backtest(px_u, rules_v2_weights(px_u), cost_bps=COST_BPS, freq="W")
    live_s = stat(*slices(rv2["returns"].reindex(px.index).fillna(0.0)))

    refs = {f"CONTROL EWall {c} (no filter, {GROSS} gross)": ctrl[c] for c in CADENCES}
    refs["RULES v2 on universe.json (LIVE BOOK, 4a comparand)"] = live_s
    refs["SPY (4b comparand)"] = spy_s
    print(fmt(pd.DataFrame(refs).T))
    print(f"\nREPRODUCTION GATE (idea 49/52's no-filter control, weekly, 10 bps): "
          f"CAGR {ctrl['W']['CAGR']:.1%} (published 10.2%), Sharpe {ctrl['W']['Sharpe']:.3f} (0.677/0.679), "
          f"MaxDD {ctrl['W']['MaxDD']:.1%} (-36.2%); at 0 bps CAGR {ctrl0['W']:.1%}")
    print(f"4b bars from SPY: H1>{spy_s['H1']:.3f}, H2>{spy_s['H2']:.3f}, OOS Sharpe>{spy_s['oSharpe']:.3f}, "
          f"MaxDD>=-{0.60 * abs(spy_s['MaxDD']):.1%}, CAGR>={0.70 * spy_s['CAGR']:.2%}")

    # ---------------- the grid ------------------------------------------
    print("\n" + "-" * 170)
    print("GRID - all 72 cells (6 bands x 3 cadences x 2 gates x 2 constructions), 10 bps and 0 bps")
    print("-" * 170)
    rows, ret10, ret0, held = {}, {}, {}, {}
    for con in CONSTRUCTIONS:
        for gate in GATES:
            for cad in CADENCES:
                for b in BANDS:
                    w = book(px, gate, b, con)
                    res = backtest(px, w, cost_bps=COST_BPS, freq=cad)
                    res0 = backtest(px, w, cost_bps=0, freq=cad)
                    key = (con, gate, cad, b)
                    r, r_is, r_oos = slices(res["returns"])
                    s = stat(r, r_is, r_oos)
                    ret10[key] = r
                    ret0[key] = res0["returns"].loc[start:]
                    held[key] = res["weights"].loc[start:].sum(axis=1)   # realised gross, daily
                    rows[key] = dict(con=con, gate=gate, cad=cad, band=b, **s,
                                     CAGR0=cagr_of(ret0[key]),
                                     gross_mean=held[key].mean(), gross_min=held[key].min(),
                                     turn_yr=res["turnover"].loc[start:].sum() / years,
                                     dCAGR_ctrl=s["CAGR"] - ctrl[cad]["CAGR"],
                                     dSharpe_ctrl=s["Sharpe"] - ctrl[cad]["Sharpe"],
                                     p4a=verdict_4a(s, live_s), f4b=fail_4b(s, spy_s))
    G = pd.DataFrame(rows.values())
    G["p4b"] = G.f4b == "-"
    cols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "oCAGR", "oSharpe", "oMaxDD", "CAGR0",
            "gross_mean", "turn_yr", "dCAGR_ctrl", "dSharpe_ctrl", "p4a", "f4b"]
    for con in CONSTRUCTIONS:
        for gate in GATES:
            sub = G[(G.con == con) & (G.gate == gate)].set_index(["cad", "band"])[cols]
            print(f"\n--- {con} / gate {gate} ---")
            print(fmt(sub))
    G.to_csv(f"{OUT}.grid.csv", index=False)

    # ---------------- P1: algebraic exactness ---------------------------
    print("\n" + "-" * 170)
    print("P1 - IS THE DE-GROSS BOOK EXACTLY THE RESPREAD BOOK AT TIME-VARYING LEVERAGE?")
    print("-" * 170)
    p1_rows = []
    for gate in GATES:
        for cad in CADENCES:
            for b in BANDS:
                kd, kr = ("DEGROSS", gate, cad, b), ("RESPREAD", gate, cad, b)
                c_t = (held[kd] / held[kr].replace(0, np.nan)).fillna(0.0)
                err = (ret0[kd] - c_t * ret0[kr]).abs().max()
                p1_rows.append(dict(gate=gate, cad=cad, band=b, c_mean=c_t.mean(),
                                    c_min=c_t.min(), c_max=c_t.max(), c_sd=c_t.std(),
                                    max_abs_err=err))
    P1 = pd.DataFrame(p1_rows)
    print(fmt(P1.set_index(["gate", "cad", "band"])))
    p1_worst = P1.max_abs_err.max()
    p1_pass = p1_worst < P1_TOL
    print(f"\nP1: worst max_t |r_dg,t - c_t*r_rs,t| across the 36 cells = {p1_worst:.3e} "
          f"(bar {P1_TOL:g}) -> {'HOLDS' if p1_pass else 'FAILS'}")
    print("    c_t = realised gross(DEGROSS)/realised gross(RESPREAD) = the share of live names gated IN.")

    # ---------------- P2: the QUEUE's regression ------------------------
    print("\n" + "-" * 170)
    print("P2 - THE QUEUE'S REGRESSION: DEGROSS-minus-RESPREAD CAGR gap on mean realised gross (36 cells)")
    print("-" * 170)
    gap_rows = []
    for gate in GATES:
        for cad in CADENCES:
            for b in BANDS:
                kd, kr = ("DEGROSS", gate, cad, b), ("RESPREAD", gate, cad, b)
                d, r_ = rows[kd], rows[kr]
                c_t = (held[kd] / held[kr].replace(0, np.nan)).fillna(0.0)
                c_bar = c_t.mean()
                # constant-leverage counterfactual: the SAME respread stream at fixed c_bar
                cf = cagr_of(c_bar * ret0[kr])
                gap_rows.append(dict(
                    gate=gate, cad=cad, band=b,
                    gross_dg=d["gross_mean"], gross_rs=r_["gross_mean"], c_bar=c_bar,
                    CAGR_dg=d["CAGR"], CAGR_rs=r_["CAGR"],
                    gap_pp=100 * (d["CAGR"] - r_["CAGR"]),
                    CAGR_dg0=d["CAGR0"], CAGR_rs0=r_["CAGR0"],
                    gap0_pp=100 * (d["CAGR0"] - r_["CAGR0"]),
                    cf_CAGR0=cf,
                    pred0_pp=100 * (cf - r_["CAGR0"]),
                    turn_dg=d["turn_yr"], turn_rs=r_["turn_yr"]))
    Gap = pd.DataFrame(gap_rows)
    Gap["resid0_pp"] = Gap.gap0_pp - Gap.pred0_pp          # timing-of-exposure component
    Gap["cost_wedge_pp"] = Gap.gap_pp - Gap.gap0_pp        # cost component of the 10 bps gap
    print(fmt(Gap.set_index(["gate", "cad", "band"])[
        ["gross_dg", "c_bar", "CAGR_dg", "CAGR_rs", "gap_pp", "gap0_pp", "pred0_pp",
         "resid0_pp", "cost_wedge_pp", "turn_dg", "turn_rs"]]))
    Gap.to_csv(f"{OUT}.identity.csv", index=False)

    reg = {}
    for tag, ycol in (("10 bps", "gap_pp"), ("0 bps", "gap0_pp")):
        sl, ic, r2, res = ols(Gap.gross_dg, Gap[ycol])
        reg[tag] = dict(slope=sl, intercept=ic, R2=r2, resid_sd=res.std(ddof=2),
                        resid_maxabs=np.abs(res).max())
        print(f"\nOLS  {ycol} ~ mean realised gross   ({tag}, n={len(Gap)})")
        print(f"    slope {sl:+.3f} pp per unit gross | intercept {ic:+.3f} pp | R2 {r2:.4f} | "
              f"resid sd {res.std(ddof=2):.4f} pp | max|resid| {np.abs(res).max():.4f} pp")
    p2 = reg["10 bps"]
    p2_pass = (p2["R2"] >= P2_R2) and (p2["resid_sd"] <= P2_RESID_SD)
    print(f"\nP2 (judged at PROTOCOL's 10 bps): R2 {p2['R2']:.4f} vs bar {P2_R2}, resid sd "
          f"{p2['resid_sd']:.4f} pp vs bar {P2_RESID_SD} pp -> {'HOLDS' if p2_pass else 'FAILS'}")

    # ---------------- P3: structural decomposition ----------------------
    print("\n" + "-" * 170)
    print("P3 - STRUCTURAL DECOMPOSITION: how much of the 0-bps gap is EXPOSURE (constant leverage")
    print("     at the cell's own mean gross) and how much is the TIMING of that exposure?")
    print("-" * 170)
    dec = Gap[["gate", "cad", "band", "c_bar", "gap0_pp", "pred0_pp", "resid0_pp"]].copy()
    dec["exposure_share"] = dec.pred0_pp / dec.gap0_pp
    print(fmt(dec.set_index(["gate", "cad", "band"])))
    mean_abs_gap = dec.gap0_pp.abs().mean()
    mean_abs_res = dec.resid0_pp.abs().mean()
    p3_pass = (mean_abs_res <= P3_ABS) and (mean_abs_res <= P3_FRAC * mean_abs_gap)
    print(f"\nmean |gap0| {mean_abs_gap:.4f} pp | mean |resid0| {mean_abs_res:.4f} pp "
          f"({100 * mean_abs_res / mean_abs_gap:.2f}% of the gap) | max |resid0| "
          f"{dec.resid0_pp.abs().max():.4f} pp")
    print(f"exposure_share: mean {dec.exposure_share.mean():.4f}, min {dec.exposure_share.min():.4f}, "
          f"max {dec.exposure_share.max():.4f}")
    print(f"P3: mean|resid| {mean_abs_res:.4f} pp vs bars {P3_ABS} pp AND "
          f"{P3_FRAC:.0%} x {mean_abs_gap:.4f} = {P3_FRAC * mean_abs_gap:.4f} pp -> "
          f"{'HOLDS' if p3_pass else 'FAILS'}")

    # ---------------- the invariance that motivated the idea ------------
    print("\n" + "-" * 170)
    print("THE MOTIVATING FACT RE-READ: gate cost vs the matched-cadence control, by construction")
    print("-" * 170)
    inv = []
    for con in CONSTRUCTIONS:
        for gate in GATES:
            for cad in CADENCES:
                sub = [rows[(con, gate, cad, b)] for b in BANDS]
                c0 = [100 * (ctrl0[cad] - s["CAGR0"]) for s in sub]
                inv.append(dict(con=con, gate=gate, cad=cad,
                                cost0_b000=c0[0], cost0_b012=c0[-1],
                                span_pp=max(c0) - min(c0),
                                pct_removed=100 * (c0[0] - c0[-1]) / c0[0] if c0[0] else np.nan))
    INV = pd.DataFrame(inv)
    print(fmt(INV.set_index(["con", "gate", "cad"])))
    print("\ncost0 = the control's 0-bps CAGR minus the cell's, in pp/yr; the band dial runs 0.00 -> 0.12.")
    print(f"Idea 52's published DEGROSS range 4.78-8.33 pp; here "
          f"{INV[INV.con == 'DEGROSS'][['cost0_b000', 'cost0_b012']].min().min():.2f}-"
          f"{INV[INV.con == 'DEGROSS'][['cost0_b000', 'cost0_b012']].max().max():.2f} pp.")

    # ---------------- rule 8 walk-forward -------------------------------
    print("\n" + "-" * 170)
    print("RULE 8 WALK-FORWARD - (band, cadence) chosen on 2010-2016 by IS Sharpe inside each arm;")
    print("2017-2026 read once.  Ties -> larger band, then slower cadence.")
    print("-" * 170)
    order = {"W": 0, "M": 1, "Q": 2}
    wf = []
    for con in CONSTRUCTIONS:
        for gate in GATES:
            arm = G[(G.con == con) & (G.gate == gate)].copy()
            arm["tb"] = arm.band
            arm["tc"] = arm.cad.map(order)
            pick = arm.sort_values(["isSharpe", "tb", "tc"], ascending=[False, False, False]).iloc[0]
            best = arm.sort_values("oSharpe", ascending=False).iloc[0]
            wf.append(dict(con=con, gate=gate, pick_band=pick.band, pick_cad=pick.cad,
                           isSharpe=pick.isSharpe, oCAGR=pick.oCAGR, oSharpe=pick.oSharpe,
                           oMaxDD=pick.oMaxDD,
                           regret_oSharpe=pick.oSharpe - best.oSharpe,
                           best_band=best.band, best_cad=best.cad,
                           vs_ctrlW=pick.oSharpe - ctrl["W"]["oSharpe"],
                           vs_SPY=pick.oSharpe - spy_s["oSharpe"],
                           vs_LIVE=pick.oSharpe - live_s["oSharpe"]))
    WF = pd.DataFrame(wf)
    print(fmt(WF.set_index(["con", "gate"])))
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    print(f"\nOOS comparands: control EWall W {ctrl['W']['oCAGR']:.2%}/{ctrl['W']['oSharpe']:.4f}/"
          f"{ctrl['W']['oMaxDD']:.1%} | SPY {spy_s['oCAGR']:.2%}/{spy_s['oSharpe']:.4f}/{spy_s['oMaxDD']:.1%} "
          f"| LIVE RULES v2 {live_s['oCAGR']:.2%}/{live_s['oSharpe']:.4f}/{live_s['oMaxDD']:.1%}")
    print(f"Picks beating SPY OOS on Sharpe: {(WF.vs_SPY > 0).sum()} of {len(WF)}; "
          f"beating the no-filter control: {(WF.vs_ctrlW > 0).sum()} of {len(WF)}; "
          f"beating the LIVE book: {(WF.vs_LIVE > 0).sum()} of {len(WF)}")

    # ---------------- KEEP paths ----------------------------------------
    print("\n" + "-" * 170)
    print("KEEP PATHS - both evaluated on all 72 cells")
    print("-" * 170)
    print(f"4a (Sharpe > LIVE RULES v2 in both halves AND MaxDD no worse): {int(G.p4a.sum())} of {len(G)}")
    print(f"4b (Sharpe > SPY H1, H2 and OOS; MaxDD <= 60% of SPY's; CAGR >= 70% of SPY's): "
          f"{int(G.p4b.sum())} of {len(G)}")
    binding = pd.Series([b for f in G.f4b for b in (f.split(",") if f != "-" else [])]).value_counts()
    print("Binding 4b bars (count of cells failing each):")
    print(binding.to_string())
    if G.p4b.any():
        print(fmt(G[G.p4b].set_index(["con", "gate", "cad", "band"])[cols]))

    # ---------------- verdict -------------------------------------------
    print("\n" + "=" * 170)
    print("VERDICT")
    print("=" * 170)
    for tag, ok in (("P1 algebraic exactness", p1_pass), ("P2 queue regression", p2_pass),
                    ("P3 structural decomposition", p3_pass)):
        print(f"  {tag}: {'HOLDS' if ok else 'FAILS'}")
    verdict = ("IDENTITY CONFIRMED" if (p1_pass and p3_pass) else "IDENTITY REFUTED")
    print(f"\n{verdict}")
    print(f"No new book, no KEEP-candidate (4a {int(G.p4a.sum())}/72, 4b {int(G.p4b.sum())}/72).")

    summary = pd.DataFrame([dict(
        p1_worst_err=p1_worst, p1=p1_pass,
        p2_R2_10bps=reg["10 bps"]["R2"], p2_resid_sd_10bps=reg["10 bps"]["resid_sd"],
        p2_slope_10bps=reg["10 bps"]["slope"], p2_R2_0bps=reg["0 bps"]["R2"],
        p2_resid_sd_0bps=reg["0 bps"]["resid_sd"], p2=p2_pass,
        mean_abs_gap0_pp=mean_abs_gap, mean_abs_resid0_pp=mean_abs_res,
        resid_share=mean_abs_res / mean_abs_gap, p3=p3_pass,
        pass4a=int(G.p4a.sum()), pass4b=int(G.p4b.sum()), n_cells=len(G), verdict=verdict)])
    summary.to_csv(f"{OUT}.summary.csv", index=False)
    print(f"\nWrote {Path(f'{OUT}.grid.csv').name}, {Path(f'{OUT}.identity.csv').name}, "
          f"{Path(f'{OUT}.walkforward.csv').name}, {Path(f'{OUT}.summary.csv').name}")


if __name__ == "__main__":
    main()

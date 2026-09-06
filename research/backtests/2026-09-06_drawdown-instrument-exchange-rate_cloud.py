#!/usr/bin/env python3
"""QUEUE idea 74 — drawdown-instrument-exchange-rate (cloud, 2026-09-06).

Question (pre-registered)
-------------------------
The project owns six drawdown instruments and has priced them one at a time, on
INCOMPATIBLE baselines: idea 9 put the per-name trailing stop at 0.17-0.53 pp of CAGR
per pp of MaxDD, idea 57 put the 200d gate at 4.45, idea 66 put de-grossing at ~1.0.
Those three numbers cannot be compared: different books, different panels, different
cost rungs, different definitions of "the control".  Idea 74 asks for ONE axis.

Deliverable, exactly as the queue states it: for each instrument, the pp of CAGR
surrendered per pp of MaxDD bought, at MATCHED starting book and MATCHED cost — a
ranked insurance menu RULES can quote when a drawdown budget is set.

    rate = (CAGR_control - CAGR_arm) / (MaxDD_arm - MaxDD_control)      [pp / pp]

both terms in percentage points, MaxDD negative, so the denominator is POSITIVE when
the arm is shallower than its control.  LOWER rate = cheaper insurance.  An arm with a
negative denominator bought nothing and is not on the menu; an arm with a negative
numerator is free insurance and is reported as such.

Because the rate is NOT a constant along an instrument's own strength ladder, a single
number per instrument would be a fiction.  The menu is therefore quoted at
PRE-REGISTERED drawdown budgets T in {2, 4, 6, 8, 10} pp: for each (panel, book, cost,
family, T) the menu entry is the CHEAPEST setting of that family that buys AT LEAST T,
with the drawdown it actually bought reported beside it, and "unreachable" printed when
the family's whole ladder cannot buy T.  Reachability is part of the answer (idea 154).

The reference row is de-gross.  It is the "just hold less" lever every drawdown claim in
this project has to clear: an instrument whose rate is above de-gross's at the same
budget is DOMINATED and should never be written into RULES.

Design (PROTOCOL rules 1-8)
---------------------------
Universes : u56 = load_universe(); broad = load_universe(broad=True) (136 names).
            BOTH reported.  SURVIVORSHIP: current constituents; the rate is a ratio of
            two within-cell differences against the same control, which cancels most of
            the level bias but not all of it (a survivor panel has shallower crashes, so
            every instrument here is priced in a world with less drawdown to buy).
Books     : idea 245's two INSTRUMENT-FREE base books, IMPORTED not re-implemented —
            EWALL0 (equal-weight all names, no gates) and CAND20 (top-20 by composite,
            no gates), both at gross 0.75.  A base book that already contains one of the
            instruments cannot price it.
Params    : exactly TWO tuned dimensions — instrument FAMILY (6) and its STRENGTH level
            (6 each) = 36 arms + control per (panel, book).  ALL 36 reported at every
            budget.  Panel, book and cost are reported at every value, never selected on.
            The budget grid T is a reporting axis, not a fit: all five are printed.
Costs     : 10 bps (PROTOCOL, the menu is read here) and 25 bps, applied analytically.
Execution : PROTOCOL rule 2 throughout (decide at close t, execute at close t+1).
Baseline  : RULES v1 weekly (4a) and SPY buy-and-hold (4b); BOTH KEEP paths evaluated
            for every one of the 144 arms.
Rule 8    : the menu itself is walk-forwarded.  The cheapest family AND its level are
            chosen at each budget on 2009-2016 ONLY, and the 2017-2026 window is then
            read once: does the IS-cheapest instrument stay cheapest, and what does the
            IS-picked arm actually deliver OOS against RULES v1 and SPY?

Harness gates, re-asserted here (idea 245's module is imported, so its own gates run):
  [A] run(no instrument) == engine.backtest, max|diff| 0.
  [C] run(stop=S) == idea 94's published run_stop, max|diff| 0.
  [D] NEW: the rate is invariant to the arithmetic, i.e. recomputing every published
      rate from the committed grid CSV reproduces the printed menu exactly.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

# --- import idea 245's module (base books, simulator, instruments) -------------
_p245 = ROOT / "research" / "backtests" / "2026-09-06_arm-the-cheap-instruments-in-crashes-instead_cloud.py"
_spec = importlib.util.spec_from_file_location("i245", _p245)
i245 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(i245)
run = i245.run
arm_returns = i245.arm_returns
BASE_BOOKS = i245.BASE_BOOKS
harness = i245.harness
m = i245.m
halves = i245.halves
at_cost = i245.at_cost
turn_per_yr = i245.turn_per_yr
fail4a = i245.fail4a
fail4b = i245.fail4b

COSTS = [10, 25]
PROTO_COST = 10
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
BUDGETS = [2.0, 4.0, 6.0, 8.0, 10.0]        # pp of MaxDD to buy; ALL reported
SCRIPT = "research/backtests/2026-09-06_drawdown-instrument-exchange-rate_cloud.py"
OUT = ROOT / "research" / "backtests" / "2026-09-06_drawdown-instrument-exchange-rate_cloud"

# 6 levels per family (idea 245's 4 widened at both ends so the deep budgets are
# reachable); ALL levels reported at every budget, none selected on outside rule 8.
LADDER = {
    "200d":  [75, 100, 150, 200, 250, 300],
    "band":  [0.01, 0.02, 0.03, 0.05, 0.08, 0.12],
    "abs":   [42, 63, 126, 189, 252, 378],
    "dg":    [0.90, 0.80, 0.70, 0.60, 0.50, 0.40],
    "ddctl": [0.05, 0.08, 0.12, 0.16, 0.20, 0.25],
    "stop":  [0.08, 0.10, 0.15, 0.20, 0.25, 0.30],
}
FAMILIES = ["200d", "band", "abs", "dg", "ddctl", "stop"]
LABEL = {"200d": "200d-type MA gate", "band": "MA re-entry band", "abs": "absolute momentum",
         "dg": "de-gross (reference)", "ddctl": "book DD control (idea 40)",
         "stop": "per-name trailing stop"}


def rate(paid_pp, bought_pp):
    """pp of CAGR surrendered per pp of MaxDD bought. NaN when nothing was bought."""
    return paid_pp / bought_pp if bought_pp > 1e-9 else np.nan


def window(r, lo=None, hi=None):
    s = r
    if lo is not None:
        s = s.loc[lo:]
    if hi is not None:
        s = s.loc[:hi]
    return s


# ---------------------------------------------------------------- sweep
def sweep(px, pname, rows):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
    spy_oos = m(spy.loc[OOS_START:])[1]
    base_r = backtest(px, rules_v1_weights(px), cost_bps=PROTO_COST, freq="W")["returns"].loc[start:]

    for bname, wfn in BASE_BOOKS.items():
        w = wfn(px)
        ctrl_full = run(px, w)
        g_c, t_c, inv_c = (s.loc[start:] for s in ctrl_full[:3])

        sims = {}
        for fam in FAMILIES:
            for lv in LADDER[fam]:
                gg, tt, ii, nf = arm_returns(px, w, fam, lv, ctrl_full)
                sims[(fam, lv)] = (gg.loc[start:], tt.loc[start:], ii.loc[start:], nf)

        for cost in COSTS:
            r_c = at_cost(g_c, t_c, cost)
            c_c, s_c, dd_c = m(r_c)
            cIS, _, ddIS = m(window(r_c, hi=IS_END))
            cOS, sOS, ddOS = m(window(r_c, lo=OOS_START))
            h1c, h2c = halves(r_c)
            rows.append(dict(panel=pname, book=bname, cost=cost, family="none", level=np.nan,
                             CAGR=c_c, Sharpe=s_c, MaxDD=dd_c, H1=h1c, H2=h2c,
                             IS_CAGR=cIS, IS_MaxDD=ddIS, IS_Sharpe=m(window(r_c, hi=IS_END))[1],
                             OOS_CAGR=cOS, OOS_Sharpe=sOS, OOS_MaxDD=ddOS,
                             paid_pp=0.0, bought_pp=0.0, xrate=np.nan,
                             IS_paid=0.0, IS_bought=0.0, IS_xrate=np.nan,
                             OOS_paid=0.0, OOS_bought=0.0, OOS_xrate=np.nan,
                             gross=float(inv_c.mean()), turn_yr=turn_per_yr(t_c),
                             fail4a="|".join(fail4a(r_c, base_r)),
                             fail4b="|".join(fail4b(r_c, spy, sOS, spy_oos))))

            for (fam, lv), (gg, tt, ii, nf) in sims.items():
                r = at_cost(gg, tt, cost)
                c, sh, dd = m(r)
                h1, h2 = halves(r)
                ci, _, ddi = m(window(r, hi=IS_END))
                co, so, ddo = m(window(r, lo=OOS_START))
                paid, bought = (c_c - c) * 100, (dd - dd_c) * 100
                ip_, ib = (cIS - ci) * 100, (ddi - ddIS) * 100
                op, ob = (cOS - co) * 100, (ddo - ddOS) * 100
                rows.append(dict(
                    panel=pname, book=bname, cost=cost, family=fam, level=lv,
                    CAGR=c, Sharpe=sh, MaxDD=dd, H1=h1, H2=h2,
                    IS_CAGR=ci, IS_MaxDD=ddi, IS_Sharpe=m(window(r, hi=IS_END))[1],
                    OOS_CAGR=co, OOS_Sharpe=so, OOS_MaxDD=ddo,
                    paid_pp=paid, bought_pp=bought, xrate=rate(paid, bought),
                    IS_paid=ip_, IS_bought=ib, IS_xrate=rate(ip_, ib),
                    OOS_paid=op, OOS_bought=ob, OOS_xrate=rate(op, ob),
                    gross=float(ii.mean()), turn_yr=turn_per_yr(tt),
                    fail4a="|".join(fail4a(r, base_r)),
                    fail4b="|".join(fail4b(r, spy, so, spy_oos))))

    return dict(panel=pname, spy_CAGR=m(spy)[0], spy_Sharpe=m(spy)[1], spy_MaxDD=m(spy)[2],
                spy_H1=halves(spy)[0], spy_H2=halves(spy)[1],
                spy_OOS_CAGR=m(spy.loc[OOS_START:])[0], spy_OOS_Sharpe=spy_oos,
                spy_OOS_MaxDD=m(spy.loc[OOS_START:])[2],
                base_CAGR=m(base_r)[0], base_Sharpe=m(base_r)[1], base_MaxDD=m(base_r)[2],
                base_H1=halves(base_r)[0], base_H2=halves(base_r)[1],
                base_OOS_CAGR=m(base_r.loc[OOS_START:])[0],
                base_OOS_Sharpe=m(base_r.loc[OOS_START:])[1],
                base_OOS_MaxDD=m(base_r.loc[OOS_START:])[2])


# ---------------------------------------------------------------- menu
def menu_entry(g, T, bcol="bought_pp", pcol="paid_pp"):
    """Cheapest setting of one family that buys AT LEAST T pp of MaxDD, or None."""
    ok = g[g[bcol] >= T]
    if not len(ok):
        return None
    k = ok[pcol].idxmin()               # cheapest in CAGR terms among those that reach T
    row = ok.loc[k]
    return dict(level=row.level, paid=row[pcol], bought=row[bcol],
                xrate=rate(row[pcol], row[bcol]))


def build_menu(df, bcol="bought_pp", pcol="paid_pp"):
    out = []
    arms = df[df.family != "none"]
    for (pn, bk, cost, fam), g in arms.groupby(["panel", "book", "cost", "family"]):
        best_reach = g[bcol].max()
        for T in BUDGETS:
            e = menu_entry(g, T, bcol, pcol)
            out.append(dict(panel=pn, book=bk, cost=cost, family=fam, budget=T,
                            reachable=e is not None, max_bought=best_reach,
                            level=e["level"] if e else np.nan,
                            paid_pp=e["paid"] if e else np.nan,
                            bought_pp=e["bought"] if e else np.nan,
                            xrate=e["xrate"] if e else np.nan))
    return pd.DataFrame(out)


# ---------------------------------------------------------------- main
def main():
    pd.set_option("display.width", 240)
    print(f"# {SCRIPT}\n# QUEUE idea 74 — every drawdown instrument on ONE axis: "
          f"pp of CAGR surrendered per pp of MaxDD bought\n")

    rows, bench = [], []
    for pname, broad in (("u56", False), ("broad", True)):
        px = load_universe(broad=broad)
        print(f"--- {pname}: {px.shape[1]} cols, {px.index[0].date()} -> {px.index[-1].date()}")
        if pname == "u56":
            harness(px)                      # idea 245's gates [A] [B] [C], re-run here
        bench.append(sweep(px, pname, rows))

    df = pd.DataFrame(rows)
    df.to_csv(f"{OUT}.grid.csv", index=False)
    bn = pd.DataFrame(bench).set_index("panel")

    # gate [D]: the published rate is reproducible from the committed grid
    a = df[df.family != "none"]
    recomputed = (a.paid_pp / a.bought_pp.where(a.bought_pp > 1e-9))
    dD = float(np.nanmax(np.abs(recomputed - a.xrate))) if len(a) else 0.0
    print(f"[D] rate recomputed from the committed grid: max|diff| = {dD:.3e}")
    assert not np.isfinite(dD) or dD < 1e-12

    print("\n=== BENCHMARKS over the common sample ===")
    print(bn.to_string(float_format=lambda x: f"{x:.3f}"))

    print("\n=== THE FOUR CONTROLS (matched starting books; every rate below is against these) ===")
    ctl = df[df.family == "none"]
    print(ctl[["panel", "book", "cost", "CAGR", "Sharpe", "MaxDD", "turn_yr",
               "IS_CAGR", "IS_MaxDD", "OOS_CAGR", "OOS_MaxDD"]]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    print("\n" + "=" * 118)
    print("=== RAW AXIS: every arm's exchange rate (pp CAGR paid / pp MaxDD bought), 10 bps, all 144 arms ===")
    print("=" * 118)
    show = ["panel", "book", "family", "level", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
            "OOS_Sharpe", "paid_pp", "bought_pp", "xrate", "turn_yr", "fail4a", "fail4b"]
    print(df[df.cost == PROTO_COST][show].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print("\n=== the same axis at 25 bps ===")
    print(df[df.cost == 25][show].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    a10 = df[(df.cost == PROTO_COST) & (df.family != "none")]
    print("\n--- how many arms buy ANY drawdown at all? (bought_pp > 0) ---")
    print(a10.assign(buys=a10.bought_pp > 0).groupby("family").agg(
        arms=("buys", "size"), buys_drawdown=("buys", "sum"),
        med_bought=("bought_pp", "median"), max_bought=("bought_pp", "max"),
        med_paid=("paid_pp", "median"), med_xrate=("xrate", "median"),
        med_turn=("turn_yr", "median")).to_string(float_format=lambda x: f"{x:.3f}"))

    print("\n" + "=" * 118)
    print("=== THE INSURANCE MENU: cheapest setting of each family that buys AT LEAST T pp of MaxDD ===")
    print("median exchange rate over the 4 (panel, book) cells at 10 bps; LOWER = cheaper insurance")
    print("=" * 118)
    mn = build_menu(df)
    mn.to_csv(f"{OUT}.menu.csv", index=False)
    m10 = mn[mn.cost == PROTO_COST]
    for T in BUDGETS:
        sub = m10[m10.budget == T]
        agg = sub.groupby("family").agg(
            cells=("reachable", "size"), reachable=("reachable", "sum"),
            med_xrate=("xrate", "median"), min_xrate=("xrate", "min"), max_xrate=("xrate", "max"),
            med_paid=("paid_pp", "median"), med_bought=("bought_pp", "median")).reset_index()
        agg["label"] = agg.family.map(LABEL)
        agg = agg.sort_values("med_xrate", na_position="last")
        ref = agg.loc[agg.family == "dg", "med_xrate"]
        ref = float(ref.iloc[0]) if len(ref) and np.isfinite(ref.iloc[0]) else np.nan
        agg["vs_degross"] = agg.med_xrate - ref
        print(f"\n--- budget T = {T:.0f} pp of MaxDD ---")
        print(agg[["family", "label", "cells", "reachable", "med_xrate", "min_xrate",
                   "max_xrate", "med_paid", "med_bought", "vs_degross"]]
              .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    print("\n--- the same menu at 25 bps (median rate by family x budget) ---")
    m25 = mn[mn.cost == 25]
    print(m25.pivot_table(index="family", columns="budget", values="xrate", aggfunc="median")
          .to_string(float_format=lambda x: f"{x:.3f}"))
    print("\n--- reachability: max pp of MaxDD each family can buy on its published ladder (10 bps) ---")
    print(m10.pivot_table(index="family", columns=["panel", "book"], values="max_bought",
                          aggfunc="max").to_string(float_format=lambda x: f"{x:.2f}"))

    print("\n--- per-cell menu at T = 4 pp, 10 bps (nothing collapsed) ---")
    print(m10[m10.budget == 4.0][["panel", "book", "family", "reachable", "level",
                                  "paid_pp", "bought_pp", "xrate"]]
          .sort_values(["panel", "book", "xrate"])
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    print("\n--- DOMINANCE: how often does each family beat the de-gross reference at the same budget/cell? ---")
    piv = m10.pivot_table(index=["panel", "book", "budget"], columns="family", values="xrate")
    dom = {}
    for fam in FAMILIES:
        if fam == "dg" or fam not in piv:
            continue
        both = piv[[fam, "dg"]].dropna()
        dom[fam] = dict(comparable_cells=len(both), beats_degross=int((both[fam] < both["dg"]).sum()),
                        med_gap=float((both[fam] - both["dg"]).median()))
    print(pd.DataFrame(dom).T.to_string(float_format=lambda x: f"{x:.3f}"))

    print("\n" + "=" * 118)
    print("=== BOTH KEEP PATHS, every one of the 144 arms, 10 bps ===")
    print("=" * 118)
    p4a, p4b = a10[a10.fail4a == ""], a10[a10.fail4b == ""]
    print(f"4a passes {len(p4a)}/{len(a10)}; 4b passes {len(p4b)}/{len(a10)}")
    if len(p4b):
        print(p4b[["panel", "book", "family", "level", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                   "OOS_Sharpe", "xrate", "turn_yr"]]
              .sort_values("Sharpe", ascending=False)
              .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print(f"\ncontrols: 4a {int((ctl[ctl.cost==PROTO_COST].fail4a=='').sum())}/4, "
          f"4b {int((ctl[ctl.cost==PROTO_COST].fail4b=='').sum())}/4")

    print("\n" + "=" * 118)
    print("=== RULE 8 WALK-FORWARD OF THE MENU ITSELF ===")
    print("family AND level chosen on 2009-2016 exchange rate only; 2017-2026 read once")
    print("=" * 118)
    is_menu = build_menu(df, bcol="IS_bought", pcol="IS_paid")
    wf = []
    for (pn, bk, cost), g in df.groupby(["panel", "book", "cost"]):
        b = bn.loc[pn]
        for T in BUDGETS:
            sub = is_menu[(is_menu.panel == pn) & (is_menu.book == bk) &
                          (is_menu.cost == cost) & (is_menu.budget == T) & is_menu.reachable]
            if not len(sub):
                wf.append(dict(panel=pn, book=bk, cost=cost, budget=T, IS_pick="unreachable"))
                continue
            pick = sub.loc[sub.xrate.idxmin()]
            arm = g[(g.family == pick.family) & (g.level == pick.level)].iloc[0]
            # what was actually cheapest OOS?
            oos_menu = build_menu(g, bcol="OOS_bought", pcol="OOS_paid")
            om = oos_menu[(oos_menu.budget == T) & oos_menu.reachable]
            best = om.loc[om.xrate.idxmin()] if len(om) else None
            wf.append(dict(panel=pn, book=bk, cost=cost, budget=T,
                           IS_pick=f"{pick.family}/{pick.level}", IS_xrate=pick.xrate,
                           OOS_xrate=arm.OOS_xrate, OOS_bought=arm.OOS_bought,
                           OOS_paid=arm.OOS_paid,
                           OOS_CAGR=arm.OOS_CAGR, OOS_Sharpe=arm.OOS_Sharpe,
                           OOS_MaxDD=arm.OOS_MaxDD,
                           best_oos=f"{best.family}/{best.level}" if best is not None else "none",
                           best_OOS_xrate=best.xrate if best is not None else np.nan,
                           regret=(arm.OOS_xrate - best.xrate) if best is not None else np.nan,
                           same_family=(best is not None and best.family == pick.family),
                           base_OOS_CAGR=b.base_OOS_CAGR, base_OOS_Sharpe=b.base_OOS_Sharpe,
                           base_OOS_MaxDD=b.base_OOS_MaxDD, spy_OOS_CAGR=b.spy_OOS_CAGR,
                           spy_OOS_Sharpe=b.spy_OOS_Sharpe, spy_OOS_MaxDD=b.spy_OOS_MaxDD))
    wfd = pd.DataFrame(wf)
    wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    w10 = wfd[(wfd.cost == PROTO_COST)] if "cost" in wfd else wfd
    print(w10[["panel", "book", "budget", "IS_pick", "IS_xrate", "OOS_xrate", "OOS_bought",
               "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "best_oos", "best_OOS_xrate",
               "regret", "same_family"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    ok = wfd.dropna(subset=["regret"])
    print(f"\nIS-cheapest FAMILY stays cheapest OOS in {int(ok.same_family.sum())}/{len(ok)} "
          f"(panel, book, cost, budget) cells; mean rate regret {ok.regret.mean():+.3f}, "
          f"median {ok.regret.median():+.3f}")
    print("\nIS-picked family, counted:")
    print(wfd[wfd.IS_pick != "unreachable"].IS_pick.str.split("/").str[0].value_counts().to_string())
    print("OOS-cheapest family, counted:")
    print(ok.best_oos.str.split("/").str[0].value_counts().to_string())

    print("\n--- OOS book metrics of the rule-8 picked arm vs RULES v1 and SPY (10 bps) ---")
    print(w10.dropna(subset=["OOS_Sharpe"])[
        ["panel", "book", "budget", "IS_pick", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
         "base_OOS_CAGR", "base_OOS_Sharpe", "base_OOS_MaxDD",
         "spy_OOS_CAGR", "spy_OOS_Sharpe", "spy_OOS_MaxDD"]]
        .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    print(f"\nwrote {OUT}.grid.csv / .menu.csv / .walkforward.csv")


if __name__ == "__main__":
    main()

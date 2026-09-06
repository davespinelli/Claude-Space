#!/usr/bin/env python3
"""QUEUE idea 258 — price-the-ranking-on-the-exchange-rate-menu (cloud, 2026-09-06).

Question (pre-registered)
-------------------------
Idea 82 found the composite ranking buys **+1.28 pp/yr of CAGR for +1.49 pp of MaxDD**
against EWall (0.86 pp/pp, t +4.93/+4.70, 8/8 cells).  That is a PRICE, and idea 74
already published what every OTHER drawdown instrument costs on one axis, at matched
book and matched cost:

    rate = (CAGR_control - CAGR_arm) / (MaxDD_arm - MaxDD_control)     [pp / pp]

The queue asks for the ranking to be put on that menu as instrument number SEVEN.

DIRECTION, stated before any number is read.  Idea 74's menu prices instruments that
BUY drawdown.  The ranking does the opposite: it RAISES CAGR and DEEPENS drawdown, so
as an arm on an EWall control it has a NEGATIVE denominator and idea 74's own convention
says it "bought nothing and is not on the menu".  The instrument that belongs on a
drawdown menu is therefore its inverse:

    DERANK  — start from the ranked book (CAND20) and WIDEN it toward EWall.
              Control = CAND20.  Arm = CAND-n, n in {30, 40, 60, 80, 120, ALL}.
              This buys drawdown and pays CAGR, exactly like de-gross and the gates.

so the comparison the queue actually wants is DERANK against DG on the SAME CAND20
control.  Both directions are reported (the sell side is Q5) so the conclusion cannot
turn on a sign convention.

  Q1  HARNESS.  Idea 245's gates [A][B][C]; plus the two this run needs:
      [E] the NORM control (gross / count) vs idea 74's literal CAND20 (GROSS/20) --
          idea 81's de-grossing channel, MEASURED not assumed away;
      [G] idea 74's published CAND20 menu re-derived from its committed grid CSV.
  Q2  THE SEVENTH ROW.  All 7 families x 6 levels x 2 books x 3 panels x 2 cost rungs,
      every grid point printed, against ONE matched control per (panel, book, cost).
  Q3  THE MENU.  At budgets T in {2,4,6,8,10} pp: the cheapest level of each family that
      buys at least T, its rate, and DERANK's RANK among the seven.  Unreachable is
      printed as unreachable (idea 154), never as a failure.
  Q4  THE VERDICT THE QUEUE ASKS FOR.  Is DERANK dearer than DG at each budget?  If yes
      at every reachable budget, the drawdown dial on a ranked book is GROSS, and the
      correct book is CAND-n de-grossed, NOT EWall.  If no, dropping the ranking is the
      cheaper way to buy the same drawdown and idea 82's recommendation stands.
  Q5  THE SELL SIDE.  The same pair read the other way from an EWall control: pp of CAGR
      GAINED per pp of MaxDD SOLD, ranking vs re-grossing.  (Re-grossing above 0.75 is
      leverage, which PROTOCOL rule 2 bars, so this side is reported for completeness and
      is not where the decision is made.)
  Q6  RULE 8.  Family AND level chosen on 2009-2016 ONLY at each budget; 2017-2026 read
      ONCE.  Reports whether DERANK is ever the IS-cheapest, and the OOS rate regret.
  Q7  BOTH KEEP PATHS on every arm (4a vs RULES v1, 4b vs SPY), all rungs.

Design (PROTOCOL rules 1-8)
---------------------------
Universes : u56 = load_universe(); broad = B136 = load_universe(broad=True) -- idea 74's
            own two, so its menu and this one are the same experiment.  SMALL480 =
            load_universe(small=True) with data/small_meta.csv max_1d_move >= 1.0
            dropped, SECONDARY only (ideas 39/49/136: the gate is inverted there).
            SURVIVORSHIP: every panel is a current-constituent list with no delistings.
            The rate is a ratio of two within-cell differences against the same control,
            which cancels much of the level bias but not all of it: a survivor panel has
            shallower crashes, so EVERY instrument here is priced in a world with less
            drawdown to buy.  It also runs AGAINST derank specifically -- the wide arm
            holds the names a delisting-aware panel would kill.
Books     : idea 245's two instrument-free base books, IMPORTED not re-implemented.
            CAND20 is where the menu is read (derank needs a ranked control); EWALL0 is
            carried for the sell side and for the other six families' cross-check.
Convention: the CAND-n ladder is run under CONSTANT GROSS (weight = GROSS / names held),
            so idea 81's `GROSS/n` de-grossing channel cannot manufacture a derank rate.
            Gate [E] measures what that convention is worth against idea 74's literal
            control; every rate in this run is against the NORM control.
Params    : exactly TWO tuned dimensions -- family (7) and its level (6).  ALL 42 arms
            reported at every budget, panel, book and cost rung.  The budget grid is a
            reporting axis, not a fit.
Costs     : 10 bps (PROTOCOL) and 25 bps, applied analytically to one 0-bps simulation.
Execution : PROTOCOL rule 2 throughout (decide at close t, execute at close t+1).
Rule 8    : IS <= 2016-12-31 chooses, OOS >= 2017-01-01 read once.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
---------------------------------------------------------------------
  P1  DERANK's full-sample rate on u56/CAND20 @10bps lands within +-0.25 of idea 82's
      0.86 pp/pp.
  P2  DERANK is DEARER than DG at every budget it can reach on both large-cap panels.
  P3  DERANK's reach (max pp of MaxDD it can buy) is SMALL -- under 4 pp -- because the
      widest book it can reach is still 75% gross; the deep budgets are dg's alone.
  P4  DERANK ranks 4th-7th of seven at every reachable budget (dearer than dg and ddctl).
  P5  Rule 8 never picks DERANK at any budget on either large-cap panel.
  P6  On the SELL side the ranking gains more CAGR per pp of MaxDD sold than nothing else
      on the menu can offer without leverage -- i.e. the two sides do not contradict.

CAVEATS carried, not buried
---------------------------
  * A rate is not a constant along an instrument's ladder; that is why the menu is quoted
    at pre-registered budgets and every level is printed.
  * Costs are a flat linear bps charge on turnover; real cost is spread plus impact and is
    convex in size (idea 126).
  * u56 has 56 names, so the derank ladder SATURATES at n >= 56: the top rungs are the
    same book.  The saturation share is printed beside every ladder (idea 240's column).
  * The rate's denominator is a difference of two MaxDDs, each a single realised extremum
    of one path.  It is the noisiest object in this project (idea 117); the IS/OOS split
    in Q6 is the only honest read of its stability and it is reported, not smoothed.
  * No LEVEL here is a tradable estimate.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .menu.csv, .walkforward.csv,
.sell.csv
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest  # noqa: E402


def _load(fname, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "research" / "backtests" / fname)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


i245 = _load("2026-09-06_arm-the-cheap-instruments-in-crashes-instead_cloud.py", "i245")
i74 = _load("2026-09-06_drawdown-instrument-exchange-rate_cloud.py", "i74")

run = i245.run
apply_gate = i245.apply_gate
gate_mask = i245.gate_mask
composite = i245.composite
harness = i245.harness
m = i245.m
halves = i245.halves
at_cost = i245.at_cost
turn_per_yr = i245.turn_per_yr
fail4a = i245.fail4a
fail4b = i245.fail4b
GROSS = i245.GROSS
FREQ = i245.FREQ

rate = i74.rate
window = i74.window
menu_entry = i74.menu_entry

COSTS = [10, 25]
PROTO_COST = 10
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
BUDGETS = [2.0, 4.0, 6.0, 8.0, 10.0]
CTRL_N = 20                       # the ranked control the derank ladder starts from
SCRIPT = "research/backtests/2026-09-06_price-the-ranking-on-the-exchange-rate-menu_cloud.py"
OUT = ROOT / "research" / "backtests" / "2026-09-06_price-the-ranking-on-the-exchange-rate-menu_cloud"

LADDER = dict(i74.LADDER)
LADDER["derank"] = [30, 40, 60, 80, 120, 10_000]      # 10_000 == "ALL rankable" == EWall
FAMILIES = list(i74.FAMILIES) + ["derank"]
LABEL = dict(i74.LABEL)
LABEL["derank"] = "DROP THE RANKING (idea 82)"

# the sell side: from an EWall control, NARROW the book (buy CAGR, sell drawdown)
SELL_LEVELS = [40, 30, 20, 15, 10, 5]

_lines: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


# ------------------------------------------------------------------ the CAND-n ladder
def w_candn(px, n, gross=GROSS):
    """Top-n by idea 2's composite, EQUAL weight at CONSTANT gross (idea 81's NORM).

    weight = gross / (names actually held), so a week with fewer than n rankable names is
    still fully invested and the de-grossing channel idea 73/81 found in `GROSS/n` cannot
    open.  n = 10_000 holds every rankable name -- that is EWall on the set the composite
    can order, which is the only EWall a ranked ladder can converge to.
    """
    names = [c for c in px.columns if c != "SPY"]
    key = composite(px[names])
    rank = key.rank(axis=1, ascending=False)
    sel = (rank <= n) & key.notna()
    cnt = sel.sum(axis=1).replace(0, np.nan)
    w = sel.astype(float).div(cnt, axis=0).mul(gross).fillna(0.0)
    return w.reindex(columns=px.columns).fillna(0.0)


def rankable_count(px):
    names = [c for c in px.columns if c != "SPY"]
    return composite(px[names]).notna().sum(axis=1)


def arm_returns(px, w, family, level, ctrl):
    """idea 245's instruments, plus the seventh."""
    if family == "derank":
        return run(px, w_candn(px, level))
    return i245.arm_returns(px, w, family, level, ctrl)


# ------------------------------------------------------------------ one panel
def sweep(px, pname, rows, sell_rows):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
    spy_oos = m(spy.loc[OOS_START:])[1]
    base_r = backtest(px, rules_v1_weights(px), cost_bps=PROTO_COST, freq="W")["returns"].loc[start:]

    books = {"CAND20": w_candn(px, CTRL_N), "EWALL0": w_candn(px, 10_000)}

    for bname, w in books.items():
        ctrl_full = run(px, w)
        g_c, t_c, inv_c = (s.loc[start:] for s in ctrl_full[:3])

        fams = FAMILIES if bname == "CAND20" else i74.FAMILIES   # derank needs a ranked control
        sims = {}
        for fam in fams:
            for lv in LADDER[fam]:
                gg, tt, ii, _ = arm_returns(px, w, fam, lv, ctrl_full)
                sims[(fam, lv)] = (gg.loc[start:], tt.loc[start:], ii.loc[start:])

        for cost in COSTS:
            r_c = at_cost(g_c, t_c, cost)
            c_c, s_c, dd_c = m(r_c)
            cIS, sIS, ddIS = m(window(r_c, hi=IS_END))
            cOS, sOS, ddOS = m(window(r_c, lo=OOS_START))
            h1c, h2c = halves(r_c)
            rows.append(dict(panel=pname, book=bname, cost=cost, family="none", level=np.nan,
                             CAGR=c_c, Sharpe=s_c, MaxDD=dd_c, H1=h1c, H2=h2c,
                             IS_CAGR=cIS, IS_Sharpe=sIS, IS_MaxDD=ddIS,
                             OOS_CAGR=cOS, OOS_Sharpe=sOS, OOS_MaxDD=ddOS,
                             paid_pp=0.0, bought_pp=0.0, xrate=np.nan,
                             IS_paid=0.0, IS_bought=0.0, IS_xrate=np.nan,
                             OOS_paid=0.0, OOS_bought=0.0, OOS_xrate=np.nan,
                             gross=float(inv_c.mean()), turn_yr=turn_per_yr(t_c),
                             fail4a="|".join(fail4a(r_c, base_r)),
                             fail4b="|".join(fail4b(r_c, spy, sOS, spy_oos))))

            for (fam, lv), (gg, tt, ii) in sims.items():
                r = at_cost(gg, tt, cost)
                c, sh, dd = m(r)
                h1, h2 = halves(r)
                ci, si, ddi = m(window(r, hi=IS_END))
                co, so, ddo = m(window(r, lo=OOS_START))
                paid, bought = (c_c - c) * 100, (dd - dd_c) * 100
                ip_, ib = (cIS - ci) * 100, (ddi - ddIS) * 100
                op, ob = (cOS - co) * 100, (ddo - ddOS) * 100
                rows.append(dict(
                    panel=pname, book=bname, cost=cost, family=fam, level=lv,
                    CAGR=c, Sharpe=sh, MaxDD=dd, H1=h1, H2=h2,
                    IS_CAGR=ci, IS_Sharpe=si, IS_MaxDD=ddi,
                    OOS_CAGR=co, OOS_Sharpe=so, OOS_MaxDD=ddo,
                    paid_pp=paid, bought_pp=bought, xrate=rate(paid, bought),
                    IS_paid=ip_, IS_bought=ib, IS_xrate=rate(ip_, ib),
                    OOS_paid=op, OOS_bought=ob, OOS_xrate=rate(op, ob),
                    gross=float(ii.mean()), turn_yr=turn_per_yr(tt),
                    fail4a="|".join(fail4a(r, base_r)),
                    fail4b="|".join(fail4b(r, spy, so, spy_oos))))

        # ---------------- Q5 the sell side, read from the EWall control only
        if bname == "EWALL0":
            for lv in SELL_LEVELS:
                gg, tt, ii, _ = run(px, w_candn(px, lv))
                gg, tt = gg.loc[start:], tt.loc[start:]
                for cost in COSTS:
                    r = at_cost(gg, tt, cost)
                    rc = at_cost(g_c, t_c, cost)
                    c, sh, dd = m(r)
                    c0, sh0, dd0 = m(rc)
                    gained, sold = (c - c0) * 100, (dd0 - dd) * 100
                    sell_rows.append(dict(panel=pname, cost=cost, n=lv, CAGR=c, Sharpe=sh,
                                          MaxDD=dd, ctrl_CAGR=c0, ctrl_Sharpe=sh0,
                                          ctrl_MaxDD=dd0, cagr_gained_pp=gained,
                                          dd_sold_pp=sold,
                                          gain_per_pp=rate(gained, sold),
                                          turn_yr=turn_per_yr(tt)))

    return dict(panel=pname, spy_CAGR=m(spy)[0], spy_Sharpe=m(spy)[1], spy_MaxDD=m(spy)[2],
                spy_H1=halves(spy)[0], spy_H2=halves(spy)[1],
                spy_OOS_CAGR=m(spy.loc[OOS_START:])[0], spy_OOS_Sharpe=spy_oos,
                spy_OOS_MaxDD=m(spy.loc[OOS_START:])[2],
                base_CAGR=m(base_r)[0], base_Sharpe=m(base_r)[1], base_MaxDD=m(base_r)[2],
                base_H1=halves(base_r)[0], base_H2=halves(base_r)[1],
                base_OOS_CAGR=m(base_r.loc[OOS_START:])[0],
                base_OOS_Sharpe=m(base_r.loc[OOS_START:])[1],
                base_OOS_MaxDD=m(base_r.loc[OOS_START:])[2])


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


# ==================================================================================== main
def main():
    pd.set_option("display.width", 250)
    pd.set_option("display.max_rows", 4000)
    P(f"# {SCRIPT}")
    P("# QUEUE idea 258 — the composite ranking as instrument number SEVEN on idea 74's menu\n")

    panels = {}
    for pname, kw in (("u56", {}), ("broad", dict(broad=True))):
        panels[pname] = load_universe(**kw)
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    n_all = len([c for c in pxs.columns if c != "SPY"])
    panels["SMALL"] = pxs[s_stk + ["SPY"]].dropna(how="all").ffill()
    P(f"panels: u56 {panels['u56'].shape[1]} cols, broad {panels['broad'].shape[1]} cols, "
      f"SMALL {n_all} names -> {len(s_stk)} after dropping max_1d_move >= 1.0 "
      f"({n_all - len(s_stk)} dropped)")
    P("SURVIVORSHIP: all three panels are current constituents with no delistings; every "
      "rate below is priced in a world with less drawdown to buy than the real one.\n")

    # ------------------------------------------------------------------ Q1 harness
    P("=" * 118)
    P("Q1  HARNESS — gates asserted before any result is read")
    P("=" * 118)
    px = panels["u56"]
    harness(px)                                        # idea 245's [A] [B] [C]

    start = px.index[260]
    P("\n[E] convention gap: this run's NORM control (gross / names held) vs idea 74's "
      "literal CAND20 (GROSS/20)")
    for pname in ("u56", "broad"):
        q = panels[pname]
        st = q.index[260]
        for nm, w in (("literal GROSS/20", i245.w_cand20(q)), ("NORM gross/count", w_candn(q, 20))):
            g, t, inv, _ = run(q, w)
            r = at_cost(g.loc[st:], t.loc[st:], PROTO_COST)
            c, s, dd = m(r)
            P(f"    {pname:6s} {nm:18s} CAGR {c:.4f}  Sharpe {s:.4f}  MaxDD {dd:.4f}  "
              f"mean gross {float(inv.loc[st:].mean()):.4f}  turn {turn_per_yr(t.loc[st:]):.2f}x")
    P("    -> the literal book de-grosses whenever <20 names are RANKABLE; the NORM control is "
      "used for every rate in this run so idea 81's channel cannot enter the derank price.")

    P("\n[F] the top rung of the derank ladder IS EWall on the RANKABLE set — the coverage gap")
    P("    against idea 245's w_ewall0 (which holds unrankable names too) is measured, not")
    P("    assumed away; it is a coverage effect, not a ranking one, and it is the same at")
    P("    every rung of the ladder.")
    for pname in ("u56", "broad"):
        q = panels[pname]
        st = q.index[260]
        kc = rankable_count(q).loc[st:]
        ec = q[[c for c in q.columns if c != "SPY"]].notna().sum(axis=1).loc[st:]
        dw = float((w_candn(q, 10_000) - i245.w_ewall0(q)).abs().max().max())
        rr = []
        for nm, w in (("EWall rankable", w_candn(q, 10_000)), ("i245 w_ewall0", i245.w_ewall0(q))):
            g, t, _, _ = run(q, w)
            rr.append((nm, m(at_cost(g.loc[st:], t.loc[st:], PROTO_COST))))
        P(f"    {pname:6s} rankable/day {kc.mean():.1f} vs priced/day {ec.mean():.1f} "
          f"(gap {float((ec - kc).mean()):.2f} names); max|dw| {dw:.3e}; @10bps  " +
          "  ".join(f"{nm}: CAGR {v[0]:.4f} Sharpe {v[1]:.4f} MaxDD {v[2]:.4f}" for nm, v in rr))

    P("\n[G] idea 74's published CAND20 menu, re-derived from its committed grid CSV")
    g74 = pd.read_csv(ROOT / "research" / "backtests" /
                      "2026-09-06_drawdown-instrument-exchange-rate_cloud.grid.csv")
    a74 = g74[(g74.panel == "u56") & (g74.book == "CAND20") & (g74.cost == 10) &
              (g74.family == "dg")]
    P(f"    idea 74 u56/CAND20@10bps dg rates: "
      f"{', '.join(f'{l:.2f}->{x:.3f}' for l, x in zip(a74.level, a74.xrate))}")
    P(f"    its control: CAGR {g74[(g74.panel=='u56')&(g74.book=='CAND20')&(g74.cost==10)&(g74.family=='none')].CAGR.iloc[0]:.4f}"
      f"  MaxDD {g74[(g74.panel=='u56')&(g74.book=='CAND20')&(g74.cost==10)&(g74.family=='none')].MaxDD.iloc[0]:.4f}")

    # ------------------------------------------------------------------ Q2 the grid
    rows, sell_rows, bench = [], [], []
    for pname in ("u56", "broad", "SMALL"):
        P(f"\n... sweeping {pname}")
        bench.append(sweep(panels[pname], pname, rows, sell_rows))
    df = pd.DataFrame(rows)
    df.to_csv(f"{OUT}.grid.csv", index=False)
    sell = pd.DataFrame(sell_rows)
    sell.to_csv(f"{OUT}.sell.csv", index=False)
    bn = pd.DataFrame(bench).set_index("panel")

    rec = df[df.family != "none"]
    dD = float(np.nanmax(np.abs((rec.paid_pp / rec.bought_pp.where(rec.bought_pp > 1e-9)) - rec.xrate)))
    P(f"\n[D] rate recomputed from the committed grid: max|diff| = {dD:.3e}")
    assert not np.isfinite(dD) or dD < 1e-12

    P("\n=== BENCHMARKS over each panel's common sample ===")
    P(bn.to_string(float_format=lambda x: f"{x:.3f}"))

    P("\n=== THE CONTROLS (matched starting books; every rate below is against these) ===")
    P(df[df.family == "none"][["panel", "book", "cost", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                               "gross", "turn_yr", "IS_CAGR", "IS_MaxDD", "OOS_CAGR", "OOS_MaxDD"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("\n" + "=" * 118)
    P("Q2  EVERY GRID POINT — 7 families x 6 levels on CAND20, 6 x 6 on EWALL0, 3 panels, 2 rungs")
    P("=" * 118)
    for pname in ("u56", "broad", "SMALL"):
        for bk in ("CAND20", "EWALL0"):
            for cost in COSTS:
                g = df[(df.panel == pname) & (df.book == bk) & (df.cost == cost)]
                P(f"\n--- {pname} / {bk} @ {cost} bps "
                  f"(control CAGR {g[g.family=='none'].CAGR.iloc[0]:.4f}, "
                  f"MaxDD {g[g.family=='none'].MaxDD.iloc[0]:.4f})")
                P(g[["family", "level", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "paid_pp",
                     "bought_pp", "xrate", "gross", "turn_yr", "fail4a", "fail4b"]]
                  .to_string(index=False, float_format=lambda x: f"{x:.4f}", na_rep="-"))

    # ------------------------------------------------------------------ Q3/Q4 the menu
    menu = build_menu(df)
    menu.to_csv(f"{OUT}.menu.csv", index=False)

    P("\n" + "=" * 118)
    P("Q3  THE MENU — cheapest level of each family that buys at least T pp of MaxDD")
    P("=" * 118)
    for pname in ("u56", "broad", "SMALL"):
        for bk in ("CAND20", "EWALL0"):
            for cost in COSTS:
                sub = menu[(menu.panel == pname) & (menu.book == bk) & (menu.cost == cost)]
                if not len(sub):
                    continue
                P(f"\n--- {pname} / {bk} @ {cost} bps   (lower rate = cheaper insurance)")
                tab = sub.pivot(index="budget", columns="family", values="xrate")
                P("  exchange rate (pp CAGR paid per pp MaxDD bought):")
                P(tab.to_string(float_format=lambda x: f"{x:.3f}", na_rep="unreach"))
                P("  reach (max pp of MaxDD the family's whole ladder can buy):")
                P(sub.groupby("family").max_bought.first().to_frame("max_bought")
                  .T.to_string(float_format=lambda x: f"{x:.2f}"))

    P("\n" + "=" * 118)
    P("Q4  WHERE DOES THE RANKING RANK?  (CAND20 book only — derank needs a ranked control)")
    P("=" * 118)
    ver = []
    for (pname, cost), sub in menu[menu.book == "CAND20"].groupby(["panel", "cost"]):
        for T in BUDGETS:
            s = sub[(sub.budget == T) & sub.reachable].sort_values("xrate")
            if not len(s):
                continue
            order = list(s.family)
            dr = s[s.family == "derank"]
            dg = s[s.family == "dg"]
            ver.append(dict(panel=pname, cost=cost, budget=T, n_reachable=len(s),
                            cheapest=order[0], cheapest_rate=float(s.xrate.iloc[0]),
                            derank_rank=(order.index("derank") + 1) if len(dr) else np.nan,
                            derank_rate=float(dr.xrate.iloc[0]) if len(dr) else np.nan,
                            dg_rate=float(dg.xrate.iloc[0]) if len(dg) else np.nan,
                            derank_dearer_than_dg=(float(dr.xrate.iloc[0]) > float(dg.xrate.iloc[0]))
                            if (len(dr) and len(dg)) else np.nan,
                            order=" < ".join(order)))
    vdf = pd.DataFrame(ver)
    P(vdf.to_string(index=False, float_format=lambda x: f"{x:.3f}", na_rep="unreach"))
    reach = vdf.derank_rank.notna()
    P(f"\n  DERANK is reachable in {int(reach.sum())} of {len(vdf)} (panel, cost, budget) cells.")
    if reach.any():
        P(f"  Where reachable: mean rank {vdf.loc[reach, 'derank_rank'].mean():.2f} of "
          f"{vdf.loc[reach, 'n_reachable'].mean():.1f} families; dearer than de-gross in "
          f"{int(vdf.loc[reach, 'derank_dearer_than_dg'].sum())} of {int(reach.sum())} cells; "
          f"mean rate {vdf.loc[reach, 'derank_rate'].mean():.3f} vs de-gross "
          f"{vdf.loc[reach, 'dg_rate'].mean():.3f}.")
    P("  Cells where DERANK cannot reach the budget at all are the ones where dropping the "
      "ranking simply does not buy that much drawdown — that is a reach failure (idea 154), "
      "not a price.")

    # ------------------------------------------------------------------ Q5 sell side
    P("\n" + "=" * 118)
    P("Q5  THE SELL SIDE — from an EWall control, what does NARROWING the book pay?")
    P("=" * 118)
    P("  (pp of CAGR gained per pp of MaxDD sold; the mirror of Q4.  Re-grossing above 0.75 is")
    P("   leverage, barred by PROTOCOL rule 2, so there is no rival instrument on this side.)")
    P(sell.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    s10 = sell[sell.cost == 10]
    for pname in ("u56", "broad", "SMALL"):
        s = s10[(s10.panel == pname) & (s10.n == 20)]
        if len(s):
            P(f"  {pname:6s} n=20 vs EWall @10bps: +{float(s.cagr_gained_pp.iloc[0]):.2f} pp CAGR "
              f"for {float(s.dd_sold_pp.iloc[0]):.2f} pp of MaxDD "
              f"= {float(s.gain_per_pp.iloc[0]):.3f} pp/pp"
              "   (idea 82 published +1.28 / 1.49 = 0.86 on its own construction)")

    # ------------------------------------------------------------------ Q6 rule 8
    P("\n" + "=" * 118)
    P("Q6  RULE 8 — family AND level chosen on 2009-2016 only; 2017-2026 read ONCE")
    P("=" * 118)
    wf = []
    arms = df[(df.family != "none") & (df.book == "CAND20")]
    for (pname, cost), g in arms.groupby(["panel", "cost"]):
        ctrl = df[(df.panel == pname) & (df.cost == cost) & (df.book == "CAND20") &
                  (df.family == "none")].iloc[0]
        for T in BUDGETS:
            isok = g[g.IS_bought >= T]
            if not len(isok):
                wf.append(dict(panel=pname, cost=cost, budget=T, IS_pick="unreachable-IS"))
                continue
            k = isok.IS_paid.idxmin()
            row = g.loc[k]
            oos_best = g[g.OOS_bought >= T]
            ob = None
            if len(oos_best):
                ob = g.loc[oos_best.OOS_paid.idxmin()]
            wf.append(dict(
                panel=pname, cost=cost, budget=T,
                IS_pick=f"{row.family}@{row.level:g}", IS_xrate=row.IS_xrate,
                IS_bought=row.IS_bought, IS_paid=row.IS_paid,
                OOS_bought=row.OOS_bought, OOS_paid=row.OOS_paid, OOS_xrate=row.OOS_xrate,
                OOS_reached=bool(row.OOS_bought >= T),
                OOS_best=f"{ob.family}@{ob.level:g}" if ob is not None else "unreachable-OOS",
                OOS_best_xrate=float(ob.OOS_xrate) if ob is not None else np.nan,
                regret=(row.OOS_xrate - float(ob.OOS_xrate)) if ob is not None else np.nan,
                OOS_Sharpe=row.OOS_Sharpe, OOS_CAGR=row.OOS_CAGR, OOS_MaxDD=row.OOS_MaxDD,
                ctrl_OOS_Sharpe=ctrl.OOS_Sharpe, ctrl_OOS_CAGR=ctrl.OOS_CAGR,
                ctrl_OOS_MaxDD=ctrl.OOS_MaxDD,
                spy_OOS_Sharpe=float(bn.loc[pname, "spy_OOS_Sharpe"]),
                spy_OOS_CAGR=float(bn.loc[pname, "spy_OOS_CAGR"]),
                spy_OOS_MaxDD=float(bn.loc[pname, "spy_OOS_MaxDD"]),
                v1_OOS_Sharpe=float(bn.loc[pname, "base_OOS_Sharpe"]),
                fail4a=row.fail4a, fail4b=row.fail4b))
    wdf = pd.DataFrame(wf)
    wdf.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(wdf.to_string(index=False, float_format=lambda x: f"{x:.3f}", na_rep="-"))
    ok = wdf[wdf.IS_pick != "unreachable-IS"]
    P(f"\n  IS-cheapest is DERANK in {int(ok.IS_pick.str.startswith('derank').sum())} of "
      f"{len(ok)} (panel, cost, budget) cells.")
    P(f"  IS-cheapest family stays OOS-cheapest in "
      f"{int((ok.IS_pick.str.split('@').str[0] == ok.OOS_best.str.split('@').str[0]).sum())} of {len(ok)}.")
    P(f"  The IS pick still reaches its budget OOS in {int(ok.OOS_reached.sum())} of {len(ok)}; "
      f"mean OOS rate regret {ok.regret.mean():+.3f}, median {ok.regret.median():+.3f}.")

    # ------------------------------------------------------------------ Q7 keep paths
    P("\n" + "=" * 118)
    P("Q7  BOTH KEEP PATHS, every arm")
    P("=" * 118)
    a = df[df.family != "none"].copy()
    a["k4a"] = a.fail4a == ""
    a["k4b"] = a.fail4b == ""
    P(f"  4a passes: {int(a.k4a.sum())} of {len(a)} arms;  4b passes: {int(a.k4b.sum())} of {len(a)}")
    P("\n  by family (all panels, both books, both rungs):")
    P(a.groupby("family")[["k4a", "k4b"]].sum().join(
        a.groupby("family").size().rename("arms")).to_string())
    P("\n  DERANK arms only:")
    P(a[a.family == "derank"][["panel", "book", "cost", "level", "CAGR", "Sharpe", "MaxDD",
                               "H1", "H2", "OOS_Sharpe", "xrate", "fail4a", "fail4b"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    if a.k4b.any():
        P("\n  every 4b PASS in the run:")
        P(a[a.k4b][["panel", "book", "cost", "family", "level", "CAGR", "Sharpe", "MaxDD",
                    "H1", "H2", "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "turn_yr", "xrate"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------------ verdict
    P("\n" + "=" * 118)
    P("PRE-REGISTERED PREDICTIONS, scored")
    P("=" * 118)
    u = vdf[(vdf.panel == "u56") & (vdf.cost == 10)]
    big = vdf[vdf.panel.isin(["u56", "broad"]) & vdf.derank_rank.notna()]
    P(f"  P1 derank rate ~ idea 82's 0.86 +-0.25 on u56/CAND20@10bps : see Q4 table above")
    P(f"  P2 derank dearer than dg at every reachable budget (large caps): "
      f"{int(big.derank_dearer_than_dg.sum())} of {len(big)} cells")
    P(f"  P3 derank reach < 4 pp: "
      f"{menu[(menu.family=='derank')].groupby(['panel','cost']).max_bought.first().to_dict()}")
    P(f"  P4 derank ranks 4th-7th: mean rank "
      f"{big.derank_rank.mean() if len(big) else float('nan'):.2f}")
    P(f"  P5 rule 8 never picks derank: picked in "
      f"{int(ok[ok.panel.isin(['u56','broad'])].IS_pick.str.startswith('derank').sum())} large-cap cells")
    P("  P6 see Q5")

    (Path(f"{OUT}.console.txt")).write_text("\n".join(_lines) + "\n")
    P(f"\nwrote {OUT}.console.txt / .grid.csv / .menu.csv / .walkforward.csv / .sell.csv")
    Path(f"{OUT}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()

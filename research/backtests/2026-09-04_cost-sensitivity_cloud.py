#!/usr/bin/env python3
"""Idea 11 - "cost-sensitivity": v1 at 5/10/25/50 bps.  At what cost does the edge die?

The question
------------
Every leaderboard row in this repo is quoted at 10 bps per unit turnover (PROTOCOL rule 2).
That number was chosen once and never stress-tested for the LIVE book.  Idea 68 measured
cost sensitivity for idea 8's ranked lookback variants and idea 45 is queued for idea 2's
candidate, but RULES v1 itself - the book that is actually paper-traded - has never been
run at any cost other than 10 bps.  This run answers the queued question directly and
reports the *breakeven cost* rather than only a handful of grid points.

Exact cost algebra (why the answer can be given to the basis point)
------------------------------------------------------------------
In products/backtester/engine.py the held-weight path drifts on ASSET returns
(`growth = cur*(1+rets)`, renormalised) and the target weights come from a cost-free
signal, so neither the held book nor the turnover series depends on `cost_bps`.  Therefore

    r_t(c) = r_t(0) - turnover_t * c/1e4                       exactly, for every c.

The script asserts this against the engine at 5/10/25/50 bps (max |diff| printed; it must
be 0) and then evaluates a 0.5 bp grid from 0 to 300 bps analytically.  Every breakeven
below is a solved crossing, not an interpolation between reported points.

Books - structural variants, all reported, none picked on its own result
    v1     RULES v1 exactly as live: top 5 eligible by the composite WITH /sqrt(vol20),
           15% each (75% gross), weekly.  THE BOOK THE IDEA ASKS ABOUT.
    CAND20 idea 2's standing 4b KEEP: top-20 eligible by the composite WITHOUT the vol
           scaler, equal weight, 75% gross, weekly.  Included so v1's cost tolerance can
           be read against the book that would replace it.
    EWall  equal-weight ALL eligible names at 75% gross, no ranking (idea 10's `B136/EWall`,
           the project's simplest 4b-passing book and its standard no-ranking control).

Tuned parameters (PROTOCOL rule 4: at most two)
    NONE are tuned in this run.  v1's (n=5, w=0.15) are the live rules; CAND20's n=20 and
    75% gross are idea 2's already-published choices; EWall has no parameter.  Cost is the
    sensitivity axis, not a fitted quantity, and the whole 0-300 bp curve is reported.

Grid = 2 universes x 3 books x {0, 5, 10, 15, 25, 50, 100} bps = 42 reported points,
plus the continuous breakeven curve for each of the 6 (universe, book) pairs.

Verdicts (both KEEP paths, every point)
    4a  Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than RULES v1.  The v1
        baseline is taken at the SAME cost as the point (the honest comparison: a cost
        regime hits both books).  v1-at-10bps is also printed for reference.
    4b  Sharpe > SPY in BOTH halves AND out-of-sample (rule 8), MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.  SPY is buy-and-hold, so its bars do not move with cost -
        which is exactly why cost is a one-directional threat to 4b.

Walk-forward (PROTOCOL rule 8) - selection rules fixed before any OOS number was read
    S1  over the 21 (book, cost) points per universe, the one with the highest 2009-2016
        Sharpe; ties -> v1, then CAND20, then lower cost.
    S2  the same, restricted to points whose in-sample MaxDD is within 60% of SPY's
        in-sample MaxDD (the 4b-aware rule used by ideas 13/68).
    The pre-registered cost question for rule 8 is separate and stated up front: is the
    in-sample breakeven cost an unbiased estimate of the out-of-sample one?  Both are
    computed on the same 0.5 bp grid and compared for all 6 pairs.

Survivorship: current constituents of both lists, one-directional.  For a COST study the
bias direction is worth naming: a survivor panel understates the turnover a live book
would have incurred rotating out of names that later delisted, so the breakeven costs
below are, if anything, optimistic.

Deterministic, standalone.  Reads baseline.py; modifies nothing.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, score, rules_v1_weights
from engine import backtest, metrics

FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
N_CAND = 20
REPORT_COSTS = [0, 5, 10, 15, 25, 50, 100]
VERIFY_COSTS = [5, 10, 25, 50]
FINE = np.round(np.arange(0.0, 300.5, 0.5), 1)
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
BOOKS = ["v1", "CAND20", "EWall"]
SCRIPT = Path(__file__).name

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 400)


# ---------------------------------------------------------------- books
def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def weights(px, book):
    if book == "v1":
        return rules_v1_weights(px)
    elig = eligible_mask(px)
    if book == "EWall":
        cnt = elig.sum(axis=1).replace(0, np.nan)
        return elig.astype(float).div(cnt, axis=0).mul(GROSS).fillna(0.0)
    s = score(px, vol_scale=False)[0]
    rank = s.where(elig).rank(axis=1, ascending=False)
    return (rank <= N_CAND).astype(float) * (GROSS / N_CAND)


# ---------------------------------------------------------------- metric helpers
def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.3f}")


def net(r0, to, c):
    """Net daily returns at c bps, from the cost-free series and the turnover series."""
    return r0 - to * c / 1e4


def pass_4a(r, base):
    h1, h2 = half_sharpes(r)
    b1, b2 = half_sharpes(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def fail_4b(r, spy, spy_oos, ms):
    h1, h2 = half_sharpes(r)
    s1, s2 = half_sharpes(spy)
    m = metrics(r)
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy_oos)["Sharpe"]: f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def last_true_cost(flags):
    """Highest cost on FINE at which `flags` is still True from c=0 without a prior break.
    Returns (breakeven, monotone_flag).  monotone False means the test re-passes above the
    first failure, which is reported rather than hidden."""
    if not flags[0]:
        return np.nan, True
    i = 0
    while i + 1 < len(flags) and flags[i + 1]:
        i += 1
    mono = not any(flags[i + 1:])
    return FINE[i], mono


# ---------------------------------------------------------------- one universe
def run_universe(uname, px):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
    ms, mso = metrics(spy), metrics(spy_oos)

    print("\n" + "=" * 170)
    print(f"UNIVERSE {uname}: {px.shape[1]} names, {px.index[0].date()} -> {px.index[-1].date()}")
    print("=" * 170)
    print(f"Eval sample: {start.date()} -> {px.index[-1].date()} | IS <= {IS_END}, OOS >= {OOS_START}")
    print(f"SPY: CAGR {ms['CAGR']:.1%}  Sharpe {ms['Sharpe']:.3f}  MaxDD {ms['MaxDD']:.1%}  "
          f"halves {half_sharpes(spy)[0]:.3f}/{half_sharpes(spy)[1]:.3f}  OOS Sharpe {mso['Sharpe']:.3f}")
    print(f"4b bars (cost-invariant): Sharpe > SPY halves & OOS, MaxDD <= {0.60*abs(ms['MaxDD']):.2%}, "
          f"CAGR >= {0.70*ms['CAGR']:.3%}")

    # ---- cost-free series + turnover, once per book
    r0, to, yrs = {}, {}, {}
    for b in BOOKS:
        res = backtest(px, weights(px, b), cost_bps=0.0, freq=FREQ)
        r0[b] = res["returns"].loc[start:]
        to[b] = res["turnover"].loc[start:]
        yrs[b] = metrics(r0[b])["Years"]

    # ---- the linearity assertion the whole analytic curve rests on
    print("\nCOST-MODEL VERIFICATION (analytic r(c) = r(0) - turnover*c/1e4 vs the engine)")
    worst = 0.0
    for b in BOOKS:
        for c in VERIFY_COSTS:
            eng = backtest(px, weights(px, b), cost_bps=float(c), freq=FREQ)["returns"].loc[start:]
            d = float((eng - net(r0[b], to[b], c)).abs().max())
            worst = max(worst, d)
    print(f"  max |analytic - engine| over {len(BOOKS)}x{len(VERIFY_COSTS)} runs = {worst:.3e}  "
          f"({'EXACT' if worst < 1e-12 else 'NOT EXACT - analytic curve below is unsafe'})")

    print("\nTURNOVER (the whole cost story; annualised sum of |dw|)")
    for b in BOOKS:
        print(f"  {b:<7} {to[b].sum()/yrs[b]:6.2f}x/yr   "
              f"IS {to[b].loc[:IS_END].sum()/(len(to[b].loc[:IS_END])/252):6.2f}x   "
              f"OOS {to[b].loc[OOS_START:].sum()/(len(to[b].loc[OOS_START:])/252):6.2f}x   "
              f"cost drag @10bps = {to[b].sum()/yrs[b]*10/1e4:.2%}/yr")

    # ---- the reported grid
    rows = []
    for b in BOOKS:
        for c in REPORT_COSTS:
            r = net(r0[b], to[b], c)
            base = net(r0["v1"], to["v1"], c)          # same-cost v1 for 4a
            m = metrics(r)
            h1, h2 = half_sharpes(r)
            r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
            rows.append(dict(
                book=b, cost=c, CAGR=m["CAGR"], Vol=m["Vol"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=h1, H2=h2, IS_Sharpe=metrics(r_is)["Sharpe"], IS_MaxDD=metrics(r_is)["MaxDD"],
                OOS_CAGR=metrics(r_oos)["CAGR"], OOS_Sharpe=metrics(r_oos)["Sharpe"],
                OOS_MaxDD=metrics(r_oos)["MaxDD"],
                exCAGR_SPY=m["CAGR"] - ms["CAGR"],
                p4a=pass_4a(r, base), f4b=fail_4b(r, spy, spy_oos, ms)))
    df = pd.DataFrame(rows)
    df["p4b"] = df["f4b"] == "-"

    print(f"\nFULL GRID {uname} - {len(df)} points, ALL reported "
          f"(4a vs v1 at the SAME cost; f4b lists which 4b tests fail)")
    print(fmt(df.set_index(["book", "cost"])[
        ["CAGR", "Vol", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
         "exCAGR_SPY", "p4a", "p4b", "f4b"]]))

    print("\n  Sharpe decay per 10 bps (OLS slope over 0-100 bps, and the 5->50 bp drop):")
    for b in BOOKS:
        s = df[df.book == b].set_index("cost")["Sharpe"]
        sl = np.polyfit(s.index.values.astype(float), s.values, 1)[0] * 10
        print(f"    {b:<7} dSharpe/10bps = {sl:+.4f}   Sharpe(5)={s[5]:.3f} -> Sharpe(50)={s[50]:.3f} "
              f"({s[50]-s[5]:+.3f})   CAGR(5)={df[(df.book==b)&(df.cost==5)].CAGR.iloc[0]:.2%} -> "
              f"CAGR(50)={df[(df.book==b)&(df.cost==50)].CAGR.iloc[0]:.2%}")

    # ---- continuous breakeven curve
    print(f"\nBREAKEVEN COSTS {uname} (0.5 bp grid, 0-300 bps; 'dies at' = first cost at which "
          f"the test fails)")
    be = []
    for b in BOOKS:
        series = {c: net(r0[b], to[b], c) for c in FINE}
        base_s = {c: net(r0["v1"], to["v1"], c) for c in FINE}
        f_sh = [metrics(series[c])["Sharpe"] > ms["Sharpe"] for c in FINE]
        f_cg = [metrics(series[c])["CAGR"] > ms["CAGR"] for c in FINE]
        f_pos = [metrics(series[c])["CAGR"] > 0 for c in FINE]
        f_4b = [fail_4b(series[c], spy, spy_oos, ms) == "-" for c in FINE]
        f_4a = [pass_4a(series[c], base_s[c]) for c in FINE]
        d = dict(book=b)
        for lab, fl in [("Sharpe>SPY", f_sh), ("CAGR>SPY", f_cg), ("CAGR>0", f_pos),
                        ("4b", f_4b), ("4a_samecost", f_4a)]:
            v, mono = last_true_cost(fl)
            d[lab] = v
            d[lab + "_mono"] = mono
        be.append(d)
    bedf = pd.DataFrame(be).set_index("book")
    print(fmt(bedf[["Sharpe>SPY", "CAGR>SPY", "CAGR>0", "4b", "4a_samecost"]]))
    print("  (NaN = fails already at 0 bps, i.e. cost is not what kills it)")
    nonmono = [(b, k) for b in BOOKS for k in ["Sharpe>SPY", "CAGR>SPY", "CAGR>0", "4b", "4a_samecost"]
               if not bedf.loc[b, k + "_mono"]]
    print(f"  non-monotone tests (test re-passes above its first failure): "
          f"{nonmono if nonmono else 'none'}")

    # ---- which 4b clause binds first as cost rises
    print(f"\n  WHICH 4b CLAUSE BINDS FIRST as cost rises ({uname}):")
    for b in BOOKS:
        seen, msgs = set(), []
        for c in FINE[::2]:
            f = fail_4b(net(r0[b], to[b], c), spy, spy_oos, ms)
            if f != "-":
                for k in f.split(","):
                    if k not in seen:
                        seen.add(k); msgs.append(f"{k}@{c:g}bps")
        print(f"    {b:<7} {' -> '.join(msgs) if msgs else 'no 4b clause fails up to 300 bps'}")

    # ---- walk-forward
    print(f"\nWALK-FORWARD ({uname}, rule 8): chosen on 2009-2016, evaluated on 2017-2026")
    cap = 0.60 * abs(metrics(spy_is)["MaxDD"])
    print(f"  In-sample SPY: Sharpe {metrics(spy_is)['Sharpe']:.3f}, MaxDD {metrics(spy_is)['MaxDD']:.1%} "
          f"-> S2 admits IS MaxDD shallower than {-cap:.1%}")
    print("  In-sample table (the only numbers either rule may look at):")
    print(fmt(df.set_index(["book", "cost"])[["IS_Sharpe", "IS_MaxDD"]]))
    print(f"  OOS bars: Sharpe > {mso['Sharpe']:.3f}, MaxDD <= {0.60*abs(mso['MaxDD']):.1%}, "
          f"CAGR >= {0.70*mso['CAGR']:.2%}   (SPY OOS {mso['CAGR']:.1%}/{mso['Sharpe']:.3f}/{mso['MaxDD']:.1%})")

    order = {"v1": 0, "CAND20": 1, "EWall": 2}

    def pick(sub, label):
        if sub.empty:
            print(f"  {label}: none qualify"); return
        s = sub.copy(); s["_o"] = s.book.map(order)
        s = s.sort_values(["IS_Sharpe", "_o", "cost"], ascending=[False, True, True])
        row = s.iloc[0]
        ok = (row.OOS_Sharpe > mso["Sharpe"] and abs(row.OOS_MaxDD) <= 0.60 * abs(mso["MaxDD"])
              and row.OOS_CAGR >= 0.70 * mso["CAGR"])
        print(f"  {label}: {row.book}@{row.cost:g}bps -> OOS CAGR {row.OOS_CAGR:.1%}  "
              f"Sharpe {row.OOS_Sharpe:.3f}  MaxDD {row.OOS_MaxDD:.1%}   clears all OOS 4b bars? {ok}")

    pick(df, "S1 plain-Sharpe")
    pick(df[df.IS_MaxDD >= -cap], "S2 4b-aware   ")
    rho = df["IS_Sharpe"].rank().corr(df["OOS_Sharpe"].rank())
    print(f"  Spearman(IS Sharpe, OOS Sharpe) over the {len(df)} points = {rho:+.3f}")

    # ---- the pre-registered rule-8 cost question
    print(f"\n  IS-vs-OOS BREAKEVEN ({uname}) - is in-sample cost tolerance an unbiased estimate?")
    print("    per book: cost at which Sharpe(book) <= Sharpe(SPY) within each window")
    rr = []
    for b in BOOKS:
        def be_win(sl_r, sl_t, sl_spy):
            f = [metrics(net(sl_r, sl_t, c))["Sharpe"] > metrics(sl_spy)["Sharpe"] for c in FINE]
            return last_true_cost(f)[0]
        i = be_win(r0[b].loc[:IS_END], to[b].loc[:IS_END], spy_is)
        o = be_win(r0[b].loc[OOS_START:], to[b].loc[OOS_START:], spy_oos)
        rr.append(dict(book=b, IS_breakeven=i, OOS_breakeven=o, diff=o - i if pd.notna(i) and pd.notna(o) else np.nan))
    print(fmt(pd.DataFrame(rr).set_index("book")))

    # ---- calendar years at 10 vs 50 bps
    print(f"\nCALENDAR YEARS ({uname}, %) - each book at 10 bps and at 50 bps")
    yr = pd.DataFrame({f"{b}@10": net(r0[b], to[b], 10) for b in BOOKS})
    for b in BOOKS:
        yr[f"{b}@50"] = net(r0[b], to[b], 50)
    yr["SPY"] = spy
    print(fmt(yr.groupby(yr.index.year).apply(lambda x: (1 + x).prod() - 1) * 100))

    df["universe"] = uname
    bedf["universe"] = uname
    return df, bedf


# ---------------------------------------------------------------- main
def main():
    print("=" * 170)
    print(f"Idea 11  cost-sensitivity (cloud) | {SCRIPT} | weekly, next-day execution, "
          f"costs {REPORT_COSTS} bps")
    print("=" * 170)

    px = load_universe()
    pxb = load_universe(broad=True)
    yrs = px.index.to_series().groupby(px.index.year).count()
    print(f"Index sanity (must be ~252 rows/yr; the calendar-day bug gave 365): "
          f"2013 {yrs.get(2013)}, 2018 {yrs.get(2018)}, 2024 {yrs.get(2024)}")
    if yrs.loc[2015:2024].max() > 300:
        print("!! CALENDAR-DAY INDEX DETECTED - aborting."); sys.exit(1)

    start = px.index[260]
    chk = backtest(px, weights(px, "CAND20"), cost_bps=10.0, freq=FREQ)["returns"].loc[start:]
    mc = metrics(chk)
    print("\nHARNESS CHECK vs idea 2's published KEEP row (12.7% / 1.093 / -18.3%, halves 1.088/1.103):")
    print(f"  reproduced: {mc['CAGR']:.1%} / {mc['Sharpe']:.3f} / {mc['MaxDD']:.1%}, "
          f"halves {half_sharpes(chk)[0]:.3f}/{half_sharpes(chk)[1]:.3f}")
    chk1 = backtest(px, weights(px, "v1"), cost_bps=10.0, freq=FREQ)["returns"].loc[start:]
    m1 = metrics(chk1)
    print(f"  RULES v1 live book @10bps: {m1['CAGR']:.1%} / {m1['Sharpe']:.3f} / {m1['MaxDD']:.1%}, "
          f"halves {half_sharpes(chk1)[0]:.3f}/{half_sharpes(chk1)[1]:.3f}  "
          f"(published idea-13 row: 6.5% / 0.67 / -13.8%, halves 0.64/0.69)")

    d1, b1 = run_universe("universe.json", px)
    d2, b2 = run_universe("universe_broad.json", pxb)

    print("\n" + "=" * 170)
    print("CROSS-UNIVERSE 4b (a (book, cost) point passes only if it passes on BOTH lists)")
    print("=" * 170)
    a = d1.set_index(["book", "cost"])["p4b"]
    b = d2.set_index(["book", "cost"])["p4b"]
    both = pd.DataFrame({"universe.json": a, "broad": b})
    both["both"] = both["universe.json"] & both["broad"]
    print(both.to_string())
    print(f"  points passing on both lists: {int(both['both'].sum())} of {len(both)}")
    if both["both"].any():
        surv = both[both["both"]].reset_index()
        for bk, g in surv.groupby("book"):
            print(f"    {bk}: cross-universe 4b survives to {g['cost'].max():g} bps "
                  f"(of the reported grid {REPORT_COSTS})")

    print("\nBREAKEVEN SUMMARY, both universes (bps):")
    print(fmt(pd.concat([b1.assign(u="u56"), b2.assign(u="broad")])
              .reset_index().set_index(["u", "book"])[["Sharpe>SPY", "CAGR>SPY", "CAGR>0", "4b", "4a_samecost"]]))

    print("\nLEADERBOARD rows:")
    for d, tag in ((d1, "u56"), (d2, "broad")):
        for _, r in d.iterrows():
            v = "KEEP 4b" if r.p4b else f"KILL 4b ({r.f4b})"
            if r.p4a: v = "4a-pass, " + v
            print(f"| 2026-09-04 | 11 {tag}/{r.book}@{r.cost:g}bps | {r.CAGR:.1%} | {r.Sharpe:.2f} | "
                  f"{r.MaxDD:.1%} | {r.H1:.2f} / {r.H2:.2f} | see v1 row | {v} | {SCRIPT} |")


if __name__ == "__main__":
    main()

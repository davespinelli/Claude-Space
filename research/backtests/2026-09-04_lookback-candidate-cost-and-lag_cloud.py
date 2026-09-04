#!/usr/bin/env python3
"""QUEUE idea 68 — lookback-candidate-cost-and-lag (cloud lane, 2026-09-04).

Question
--------
Idea 8 found exactly one grid point that passes 4b on BOTH large-cap universes:
**pure 12-1 momentum, top-30, equal weight at 75% gross** (universe.json
10.9%/1.097/-15.8%, broad 13.0%/1.004/-20.2%).  It turns over 6.7x/yr against the
incumbent blend-v1 n=20 candidate's 9.6x, so the pre-registered expectation is that it
should be *less* cost-sensitive than the incumbent — but its broad drawdown sits exactly
on 4b's -20.2% cap, so it has no room on the other axis.  This run applies idea 45's
protocol: 5/10/15/25/50 bps crossed with a 1-day vs 1-week execution lag, both universes,
and reports where the cross-universe 4b pass is lost.

Design (PROTOCOL rules 1-8)
---------------------------
Universe : research/universe.json (56 names) and universe_broad.json (136 names), both
           reported as primary — a cross-universe pass is the thing under test.
Books    : signal in {12-1, blend-v1} x n in {20, 30}, so the candidate (12-1 n=30) is
           measured against the incumbent candidate (blend-v1 n=20) and against both
           matched controls.  Construction is idea 8's, unchanged: rank the signal among
           eligible names (px > 200d MA & vol20 < 0.60), hold the top n at 0.75/n.
Params   : exactly 2 tuned — signal and n.  Cost and lag are stress axes, not choices:
           every one of the 5 x 2 = 10 (cost, lag) cells is reported for every book.
Lag      : the engine already applies weights decided at close t on t+1 (the 1-day arm).
           The 1-week arm shifts the weight matrix a further 4 trading days, so a signal
           formed at Friday's close is executed at the following Friday's close.
Costs    : held weights and turnover do not depend on cost_bps, so the five cost levels
           are computed analytically from a single backtest per (book, lag, universe):
           r_c = gross_return - turnover * c/1e4.  The 10 bps arm is checked against the
           engine to machine precision below.
Rule 8   : at each (cost, lag) cell independently, choose (signal, n) on 2009-2016 only
           under two rules fixed in advance — plain IS Sharpe, and IS Sharpe subject to
           the IS 4b bars — then evaluate that pick untouched on 2017-2026.  This asks
           the question that matters: does a walk-forward run at realistic costs ever
           select the candidate?

SURVIVORSHIP: both lists are current constituents, so absolute CAGRs are optimistic.
The cost/lag comparisons hold names, days, gate and gross fixed and are far less exposed.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

FREQ = "W"
GROSS = 0.75
MAX_VOL = 0.60
COSTS = [5, 10, 15, 25, 50]
LAGS = {"1d": 0, "1w": 4}          # extra trading days on top of the engine's own t+1
BOOKS = [("12-1", 30), ("12-1", 20), ("blend-v1", 30), ("blend-v1", 20)]
CAND = ("12-1", 30)
INCUMBENT = ("blend-v1", 20)
IS_END, OOS_START = "2016-12-31", "2017-01-01"
SCRIPT = "research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py"


# ---------------------------------------------------------------- construction
def _pr(x):
    return x.rank(axis=1, pct=True)


def signal(px, s):
    if s == "12-1":
        return px.shift(21) / px.shift(252) - 1
    if s == "blend-v1":
        return (_pr(px.shift(21) / px.shift(252) - 1) + _pr(px / px.shift(126) - 1)
                + _pr(px / px.shift(63) - 1)) / 3
    raise ValueError(s)


def vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def eligible(px):
    return (px > px.rolling(200).mean()) & (vol20(px) < MAX_VOL)


def weights(px, s, n, extra_lag=0):
    rank = signal(px, s).where(eligible(px)).rank(axis=1, ascending=False)
    w = (rank <= n).astype(float) * (GROSS / n)
    return w.shift(extra_lag) if extra_lag else w


# ---------------------------------------------------------------- metrics
def m(r):
    d = metrics(r)
    return d["CAGR"], d["Sharpe"], d["MaxDD"]


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def fail4b(r, spy, oos_sh, spy_oos_sh):
    c, s, dd = m(r); h1, h2 = halves(r)
    sc, ss, sdd = m(spy); s1, s2 = halves(spy)
    bad = []
    if h1 <= s1: bad.append("H1")
    if h2 <= s2: bad.append("H2")
    if oos_sh <= spy_oos_sh: bad.append("OOS")
    if dd < 0.60 * sdd: bad.append("DD")
    if c < 0.70 * sc: bad.append("CAGR")
    return bad


def fail4a(r, base):
    _, _, dd = m(r); h1, h2 = halves(r)
    _, _, bdd = m(base); b1, b2 = halves(base)
    bad = []
    if h1 <= b1: bad.append("H1")
    if h2 <= b2: bad.append("H2")
    if dd < bdd: bad.append("DD")
    return bad


def bname(key):
    return f"{key[0]} n={key[1]}"


# ---------------------------------------------------------------- one universe
def sweep(px, tag):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    base = backtest(px, rules_v1_weights(px), cost_bps=10, freq=FREQ)["returns"].loc[start:]
    sc, ss, sdd = m(spy); s1, s2 = halves(spy)
    _, ss_o, _ = m(spy.loc[OOS_START:])

    yrs = px.index.to_series().groupby(px.index.year).count()
    if yrs.loc[2015:2024].max() > 300:
        sys.exit("!! CALENDAR-DAY INDEX DETECTED — results not comparable. Aborting.")

    print(f"\n{'=' * 128}")
    print(f"{tag}: {px.shape[1]} tickers, eval {start.date()} -> {px.index[-1].date()} "
          f"(index sanity: 2018 {yrs.get(2018)} rows, 2024 {yrs.get(2024)} rows)")
    print(f"SPY {sc:.1%}/{ss:.3f}/{sdd:.1%} halves {s1:.3f}/{s2:.3f} OOS Sharpe {ss_o:.3f}  |  "
          f"RULES v1 @10bps {m(base)[0]:.1%}/{m(base)[1]:.3f}/{m(base)[2]:.1%}")
    print(f"4b bars: H1>{s1:.3f}  H2>{s2:.3f}  OOS>{ss_o:.3f}  MaxDD>={0.60 * sdd:.1%}  "
          f"CAGR>={0.70 * sc:.1%}")
    print("=" * 128)

    # one engine run per (book, lag); costs applied analytically afterwards
    raw = {}
    for key in BOOKS:
        for lag, k in LAGS.items():
            res = backtest(px, weights(px, key[0], key[1], k), cost_bps=0.0, freq=FREQ)
            g, t = res["returns"].loc[start:], res["turnover"].loc[start:]
            raw[(key, lag)] = (g, t)

    # analytic cost model vs the engine, at the candidate, 10 bps, 1d
    g, t = raw[(CAND, "1d")]
    an = g - t * 10 / 1e4
    eng = backtest(px, weights(px, *CAND), cost_bps=10, freq=FREQ)["returns"].loc[start:]
    print(f"\nCOST-MODEL CHECK  max |analytic - engine| at {bname(CAND)}, 10 bps, 1d lag: "
          f"{np.abs(an - eng).max():.2e}   "
          f"{'PASS' if np.abs(an - eng).max() < 1e-12 else '*** MISMATCH ***'}")

    # harness sanity vs idea 8's published rows
    c, s_, dd = m(an)
    ref = {"universe.json": (0.109, 1.097, -0.158), "universe_broad.json": (0.130, 1.004, -0.202)}[tag]
    ok = abs(c - ref[0]) < 0.002 and abs(s_ - ref[1]) < 0.01 and abs(dd - ref[2]) < 0.005
    print(f"HARNESS CHECK  {bname(CAND)} @10bps/1d -> {c:.1%}/{s_:.3f}/{dd:.1%}   "
          f"(idea 8 published {ref[0]:.1%}/{ref[1]:.3f}/{ref[2]:.1%})  "
          f"{'PASS' if ok else '*** MISMATCH ***'}")

    print("\nTurnover (annualised, x of book) by book and execution lag:")
    for key in BOOKS:
        line = "  ".join(f"{lag} {raw[(key, lag)][1].sum() / (len(raw[(key, lag)][0]) / 252):5.2f}x"
                         for lag in LAGS)
        print(f"  {bname(key):<16} {line}")

    grid, rows = {}, []
    print(f"\n{'book':<16}{'lag':<5}{'bps':>5}{'CAGR':>8}{'Sharpe':>8}{'MaxDD':>8}   "
          f"{'H1':>5}/{'H2':>5}{'OOS':>7}   verdict")
    print("-" * 128)
    for key in BOOKS:
        for lag in LAGS:
            g, t = raw[(key, lag)]
            for c_bps in COSTS:
                r = g - t * c_bps / 1e4
                grid[(key, lag, c_bps)] = r
                oos = m(r.loc[OOS_START:])[1]
                a, b = fail4a(r, base), fail4b(r, spy, oos, ss_o)
                v = ("KEEP 4a" if not a else "KILL 4a") + " / " + \
                    ("KEEP 4b" if not b else "KILL 4b (" + ",".join(b) + ")")
                cg, sh, dd = m(r); h1, h2 = halves(r)
                print(f"{bname(key):<16}{lag:<5}{c_bps:5d}{cg:8.1%}{sh:8.3f}{dd:8.1%}   "
                      f"{h1:5.3f}/{h2:5.3f}{oos:7.3f}   {v}")
                rows.append((f"68 {tag} {bname(key)} {lag} {c_bps}bps", cg, sh, dd, h1, h2, oos,
                             t.sum() / (len(g) / 252), v))
        print("-" * 128)

    # cost decay slope and the price of the week's delay
    print("\nCost sensitivity (Sharpe per +10 bps, from the 5-25 bps span) and the cost of the lag:")
    for key in BOOKS:
        out = []
        for lag in LAGS:
            s5 = m(grid[(key, lag, 5)])[1]; s25 = m(grid[(key, lag, 25)])[1]
            out.append(f"{lag} {10 * (s25 - s5) / 20:+.3f}")
        d = (grid[(key, "1w", 10)] - grid[(key, "1d", 10)]).dropna()
        t_ = d.mean() / d.std() * np.sqrt(len(d))
        print(f"  {bname(key):<16} dSharpe/10bps: {'  '.join(out)}    "
              f"1w minus 1d @10bps: {d.mean() * 252:+6.2%}/yr  t {t_:+5.2f}  "
              f"dSharpe {m(grid[(key, '1w', 10)])[1] - m(grid[(key, '1d', 10)])[1]:+.3f}")

    # candidate vs incumbent, paired, at every cell
    print(f"\nCandidate ({bname(CAND)}) minus incumbent ({bname(INCUMBENT)}), paired daily:")
    for lag in LAGS:
        for c_bps in COSTS:
            d = (grid[(CAND, lag, c_bps)] - grid[(INCUMBENT, lag, c_bps)]).dropna()
            t_ = d.mean() / d.std() * np.sqrt(len(d))
            print(f"  {lag} {c_bps:3d} bps  {d.mean() * 252:+6.2%}/yr  t {t_:+5.2f}   "
                  f"dSharpe {m(grid[(CAND, lag, c_bps)])[1] - m(grid[(INCUMBENT, lag, c_bps)])[1]:+.3f}")

    return dict(grid=grid, rows=rows, spy=spy, base=base, start=start, ss_o=ss_o, raw=raw)


def cross_universe(main_res, broad_res):
    """Where is the cross-universe 4b pass lost?  One table, both lists, every cell."""
    print(f"\n{'=' * 128}")
    print("CROSS-UNIVERSE 4b — the test idea 68 exists to run. 'both' = passes 4b on "
          "universe.json AND universe_broad.json.")
    print("=" * 128)
    print(f"{'book':<16}{'lag':<5}" + "".join(f"{c:>12}bps" for c in COSTS))
    for key in BOOKS:
        for lag in LAGS:
            cells = []
            for c_bps in COSTS:
                out = []
                for res, nm in ((main_res, "u"), (broad_res, "b")):
                    r = res["grid"][(key, lag, c_bps)]
                    oos = m(r.loc[OOS_START:])[1]
                    bad = fail4b(r, res["spy"], oos, res["ss_o"])
                    out.append("." if not bad else nm + ":" + ",".join(bad))
                cells.append("BOTH" if out == [".", "."] else "/".join(x for x in out if x != "."))
            print(f"{bname(key):<16}{lag:<5}" + "".join(f"{c:>15}" for c in cells))
    print("\n(a cell shows which universe fails and on which 4b test; BOTH = passes on both)")


def walk_forward(res, tag):
    """Rule 8 at every (cost, lag) cell: choose (signal, n) on 2009-2016, evaluate 2017-2026."""
    grid, spy, base = res["grid"], res["spy"], res["base"]
    spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
    sc_i, ss_i, sdd_i = m(spy_is)
    sc_o, ss_o, sdd_o = m(spy_oos)
    print(f"\nWalk-forward ({tag}): IS <= {IS_END}, OOS >= {OOS_START}; selection re-run "
          f"independently inside every (cost, lag) cell")
    print(f"  IS 4b bars: Sharpe>{ss_i:.3f}  MaxDD>={0.60 * sdd_i:.1%}  CAGR>={0.70 * sc_i:.1%}"
          f"   |   OOS SPY {sc_o:.1%}/{ss_o:.3f}/{sdd_o:.1%}"
          f"   RULES v1 {m(base.loc[OOS_START:])[0]:.1%}/{m(base.loc[OOS_START:])[1]:.3f}")
    out = []
    for lag in LAGS:
        for c_bps in COSTS:
            cand = []
            for key in BOOKS:
                r = grid[(key, lag, c_bps)]
                c, s_, dd = m(r.loc[:IS_END])
                cand.append(dict(key=key, sh=s_, cagr=c, dd=dd))
            picks = {"plain-Sharpe": max(cand, key=lambda x: x["sh"])["key"]}
            ok = [c for c in cand if c["sh"] > ss_i and c["dd"] >= 0.60 * sdd_i
                  and c["cagr"] >= 0.70 * sc_i]
            picks["4b-aware"] = max(ok, key=lambda x: x["sh"])["key"] if ok else None
            for rule, key in picks.items():
                if key is None:
                    print(f"  {lag} {c_bps:3d} bps  [{rule:<12}] NOTHING — no IS point met the 4b bars")
                    out.append((f"68 {tag} WF {rule} {lag} {c_bps}bps: picks NOTHING", None))
                    continue
                c, s_, dd = m(grid[(key, lag, c_bps)].loc[OOS_START:])
                flag = "beats SPY OOS" if s_ > ss_o else "loses to SPY OOS"
                p4b = "clears OOS 4b" if (s_ > ss_o and dd >= 0.60 * sdd_o
                                          and c >= 0.70 * sc_o) else "misses OOS 4b"
                star = " <- the candidate" if key == CAND else ""
                print(f"  {lag} {c_bps:3d} bps  [{rule:<12}] {bname(key):<16} "
                      f"OOS {c:6.1%}/{s_:.3f}/{dd:6.1%}  ({flag}; {p4b}){star}")
                out.append((f"68 {tag} WF {rule} {lag} {c_bps}bps: {bname(key)} OOS",
                            (c, s_, dd, f"{flag}; {p4b}")))
    return out


def years(res, tag):
    print(f"\nCalendar-year returns ({tag}) at 10 bps — candidate vs incumbent, 1d vs 1w lag:")
    spy = res["spy"]
    d = {"SPY": spy.groupby(spy.index.year).apply(lambda x: (1 + x).prod() - 1)}
    for key in (CAND, INCUMBENT):
        for lag in LAGS:
            r = res["grid"][(key, lag, 10)]
            d[f"{bname(key)} {lag}"] = r.groupby(r.index.year).apply(lambda x: (1 + x).prod() - 1)
    print(pd.DataFrame(d).to_string(float_format=lambda x: f"{x:+.1%}"))


# ---------------------------------------------------------------- main
def main():
    print("=" * 128)
    print(f"Idea 68 lookback-candidate-cost-and-lag (cloud) | {SCRIPT}")
    print("Grid: signal in {12-1, blend-v1} x n in {20,30} (2 tuned params) x cost in "
          "{5,10,15,25,50} bps x lag in {1d, 1w} = 40 points per universe, all reported.")
    print("=" * 128)

    main_res = sweep(load_universe(), "universe.json")
    broad_res = sweep(load_universe(broad=True), "universe_broad.json")
    cross_universe(main_res, broad_res)
    wf_main = walk_forward(main_res, "universe.json")
    wf_broad = walk_forward(broad_res, "universe_broad.json")
    years(main_res, "universe.json")
    years(broad_res, "universe_broad.json")

    bl = m(main_res["base"]); b1, b2 = halves(main_res["base"])
    print("\nLEADERBOARD rows:")
    for tagrows in (main_res["rows"], broad_res["rows"]):
        for lbl, c, s_, dd, h1, h2, oos, t, v in tagrows:
            print(f"| 2026-09-04 | {lbl} | {c:.1%} | {s_:.2f} | {dd:.1%} | {h1:.2f} / {h2:.2f} | "
                  f"{bl[1]:.2f} ({b1:.2f}/{b2:.2f}) | {v} | {SCRIPT} |")
    for lbl, r in [("68 SPY buy & hold (universe.json sample) - reference", main_res["spy"]),
                   ("68 RULES v1 live @10bps (universe.json) - baseline", main_res["base"])]:
        c, s_, dd = m(r); h1, h2 = halves(r)
        print(f"| 2026-09-04 | {lbl} | {c:.1%} | {s_:.2f} | {dd:.1%} | {h1:.2f} / {h2:.2f} | "
              f"{bl[1]:.2f} ({b1:.2f}/{b2:.2f}) | - | {SCRIPT} |")
    for lbl, v in wf_main + wf_broad:
        if v is None:
            print(f"| 2026-09-04 | {lbl} | - | - | - | - / - | {bl[1]:.2f} ({b1:.2f}/{b2:.2f}) | "
                  f"no IS point met the 4b bars | {SCRIPT} |")
        else:
            c, s_, dd, flag = v
            print(f"| 2026-09-04 | {lbl} | {c:.1%} | {s_:.2f} | {dd:.1%} | - / - | "
                  f"{bl[1]:.2f} ({b1:.2f}/{b2:.2f}) | {flag} | {SCRIPT} |")


if __name__ == "__main__":
    main()

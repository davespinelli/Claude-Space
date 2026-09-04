#!/usr/bin/env python3
"""QUEUE idea 55 — trend-gate-lookback-primary (cloud lane, 2026-09-04).

Question
--------
The 200d-MA gate is the load-bearing assumption of RULES v1 and of idea 2's 4b
KEEP-candidate: "the gate is the edge" on `universe.json`.  Two runs have measured it
*elsewhere* and found it costly — idea 39 at -1.7pp CAGR on small caps, idea 27 at
-6.4pp on QQQ — but **nobody has varied the lookback on the primary universe**, where it
is supposed to work.  This run does exactly that, at the KEEP-candidate's own
construction, and includes the `none` arm so the gate's own contribution is measured
rather than assumed.

Design (PROTOCOL rules 1-8)
---------------------------
Universe : research/universe.json via load_universe() (56 names incl. SPY, ETFs +
           mega caps).  Secondary robustness pass on universe_broad.json (136 names).
Book     : idea 2's candidate construction, unchanged — top-n by the v1 composite
           WITHOUT `/sqrt(vol20)` (mean pct-rank of 12-1, 6m, 3m), among eligible names,
           equal weight 0.75/n (75% gross).  If fewer than n are eligible the book holds
           all of them and de-grosses into cash (idea 2's clause, worth +0.02 Sharpe).
Gate     : eligible = (px > px.rolling(K).mean()) & (vol20 < 0.60), with
           **K in {200, 100, 50, none}**.  The vol20 < 0.60 half is held FIXED at v1's
           value throughout — varying it is queued separately as idea 56.
Params   : exactly 2 — K and n in {5, 10, 20, 30}.  All 16 points reported.
Execution: weekly rebalance, weights at close t applied at t+1, 10 bps per unit turnover.
Rule 8   : parameters chosen on 2009-2016 only, evaluated untouched on 2017-2026, with
           two selection rules fixed BEFORE any OOS number is read.

Note on the composite: v1's `score()` multiplies the rank blend by (0.5 + 0.5*above200).
Every eligible name is above its MA by construction, so that factor is identically 1.0
within the selected set and the ranking is the pure rank blend.  The harness check below
confirms K=200/n=20 reproduces idea 2's KEEP row exactly.

SURVIVORSHIP: both lists are current constituents, so absolute CAGRs are optimistic; a
20-name book holds over half of the 56-name list.  The K-vs-K comparison is much less
exposed, since every arm draws from the same names.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

COST = 10
FREQ = "W"
GROSS = 0.75
MAX_VOL = 0.60
KS = [200, 100, 50, None]
NS = [5, 10, 20, 30]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
SCRIPT = "research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py"


# ---------------------------------------------------------------- construction
def composite(px):
    """v1's rank blend WITHOUT the /sqrt(vol20) term (idea 2's candidate scorer)."""
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def eligible(px, k):
    """v1's eligibility with the trend lookback swapped. k=None drops the trend half only."""
    m = vol20(px) < MAX_VOL
    if k is not None:
        m = m & (px > px.rolling(k).mean())
    return m


def weights_fn(k, n):
    def f(px):
        rank = composite(px).where(eligible(px, k)).rank(axis=1, ascending=False)
        return (rank <= n).astype(float) * (GROSS / n)
    return f


def ew_eligible(k):
    """Equal-weight ALL eligible names at 75% gross (idea 28's book) — gate-only diagnostic."""
    def f(px):
        e = eligible(px, k).astype(float)
        return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0) * GROSS
    return f


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


def run(px, fn, start, cost=COST):
    res = backtest(px, fn(px), cost_bps=cost, freq=FREQ)
    r = res["returns"].loc[start:]
    return r, res["turnover"].loc[start:].sum() / (len(r) / 252)


def kname(k):
    return "none" if k is None else f"{k}d"


# ---------------------------------------------------------------- one universe
def sweep(px, tag, verbose=True):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    spy_oos = spy.loc[OOS_START:]
    base = backtest(px, rules_v1_weights(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
    sc, ss, sdd = m(spy); s1, s2 = halves(spy)
    _, ss_o, _ = m(spy_oos)

    yrs = px.index.to_series().groupby(px.index.year).count()
    if yrs.loc[2015:2024].max() > 300:
        sys.exit("!! CALENDAR-DAY INDEX DETECTED — results not comparable. Aborting.")

    print(f"\n{'=' * 124}")
    print(f"{tag}: {px.shape[1]} tickers, eval {start.date()} -> {px.index[-1].date()} "
          f"(index sanity: 2018 {yrs.get(2018)} rows, 2024 {yrs.get(2024)} rows)")
    print(f"SPY {sc:.1%}/{ss:.3f}/{sdd:.1%} halves {s1:.3f}/{s2:.3f} OOS Sharpe {ss_o:.3f}  |  "
          f"RULES v1 {m(base)[0]:.1%}/{m(base)[1]:.3f}/{m(base)[2]:.1%}")
    print(f"4b bars: H1>{s1:.3f}  H2>{s2:.3f}  OOS>{ss_o:.3f}  MaxDD>={0.60 * sdd:.1%}  "
          f"CAGR>={0.70 * sc:.1%}")
    print("=" * 124)

    # how much does the gate actually exclude, by lookback?
    print("\nEligible names per day by lookback (of "
          f"{px.shape[1]}), and days with fewer than 20 eligible:")
    for k in KS:
        e = eligible(px, k).loc[start:].sum(axis=1)
        print(f"  K={kname(k):<5} mean {e.mean():5.1f}  median {e.median():5.0f}  "
              f"min {e.min():3.0f}  max {e.max():3.0f}   days<20: {(e < 20).mean():5.1%}   "
              f"days=0: {(e == 0).mean():4.1%}")

    print(f"\n{'K':<6}{'n':<5}{'CAGR':>7}{'Sharpe':>8}{'MaxDD':>8}   {'H1':>5}/{'H2':>5}"
          f"{'OOS':>7}{'turn':>7}   verdict")
    print("-" * 124)
    grid, rows = {}, []
    for k in KS:
        for n in NS:
            r, t = run(px, weights_fn(k, n), start)
            grid[(k, n)] = (r, t)
            oos = m(r.loc[OOS_START:])[1]
            a, b = fail4a(r, base), fail4b(r, spy, oos, ss_o)
            v = ("KEEP 4a" if not a else "KILL 4a") + " / " + \
                ("KEEP 4b" if not b else "KILL 4b (" + ",".join(b) + ")")
            c, s_, dd = m(r); h1, h2 = halves(r)
            print(f"{kname(k):<6}{n:<5}{c:7.1%}{s_:8.3f}{dd:8.1%}   {h1:5.3f}/{h2:5.3f}"
                  f"{oos:7.3f}{t:7.1f}x   {v}")
            rows.append((f"55 {tag} K={kname(k)} n={n}", c, s_, dd, h1, h2, oos, t, v))

    # gate-only diagnostic: equal-weight every eligible name (no ranking at all)
    print("\nGate-only control — equal-weight ALL eligible names @75% gross (no ranking):")
    for k in KS:
        r, t = run(px, ew_eligible(k), start)
        c, s_, dd = m(r); h1, h2 = halves(r)
        oos = m(r.loc[OOS_START:])[1]
        print(f"  K={kname(k):<5} {c:6.1%} / {s_:.3f} / {dd:6.1%}  halves {h1:.3f}/{h2:.3f}  "
              f"OOS {oos:.3f}  turn {t:.1f}x")
        rows.append((f"55 {tag} EW-all-eligible K={kname(k)} [diag]", c, s_, dd, h1, h2, oos, t, "-"))

    # the number the idea asks for: what does the trend half of the gate cost, at matched n?
    print("\nTrend-gate contribution at matched n (arm minus the K=none arm):")
    for n in NS:
        base_c, base_s, base_dd = m(grid[(None, n)][0])
        for k in (200, 100, 50):
            c, s_, dd = m(grid[(k, n)][0])
            print(f"  n={n:<3} K={k:<4} {100 * (c - base_c):+6.1f}pp CAGR  {s_ - base_s:+.3f} Sharpe  "
                  f"{100 * (dd - base_dd):+6.1f}pp MaxDD")

    # is the gate's effect distinguishable from zero?  paired t on the daily difference.
    print("\nPaired significance of dropping the trend gate (K=none minus K, same names, same days):")
    for n in NS:
        for k in (200, 100, 50):
            d = (grid[(None, n)][0] - grid[(k, n)][0]).dropna()
            t = d.mean() / d.std() * np.sqrt(len(d))
            print(f"  n={n:<3} vs K={k:<4} {d.mean() * 252:+6.2%}/yr  t {t:+5.2f}")
    ew_none, _ = run(px, ew_eligible(None), start)
    ew_200, _ = run(px, ew_eligible(200), start)
    d = (ew_none - ew_200).dropna()
    print(f"  EW-all-eligible: none minus 200d  {d.mean() * 252:+6.2%}/yr  "
          f"t {d.mean() / d.std() * np.sqrt(len(d)):+5.2f}")

    return dict(grid=grid, rows=rows, spy=spy, base=base, start=start, ss_o=ss_o)


def walk_forward(res, tag):
    """PROTOCOL rule 8: choose on 2009-2016, evaluate untouched on 2017-2026."""
    grid, spy, base = res["grid"], res["spy"], res["base"]
    spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
    sc_i, ss_i, sdd_i = m(spy_is)
    sc_o, ss_o, sdd_o = m(spy_oos)
    print(f"\nWalk-forward ({tag}): IS <= {IS_END}, OOS >= {OOS_START}")
    print(f"  IS 4b bars: Sharpe>{ss_i:.3f}  MaxDD>={0.60 * sdd_i:.1%}  CAGR>={0.70 * sc_i:.1%}")
    cand = []
    for key, (r, t) in grid.items():
        c, s_, dd = m(r.loc[:IS_END])
        cand.append(dict(key=key, sh=s_, cagr=c, dd=dd))
    for c in sorted(cand, key=lambda x: -x["sh"])[:6]:
        print(f"  IS  K={kname(c['key'][0]):<5} n={c['key'][1]:<3} Sharpe {c['sh']:6.3f}  "
              f"CAGR {c['cagr']:6.1%}  MaxDD {c['dd']:6.1%}")
    picks = {"plain-Sharpe": max(cand, key=lambda x: x["sh"])["key"]}
    ok = [c for c in cand if c["sh"] > ss_i and c["dd"] >= 0.60 * sdd_i and c["cagr"] >= 0.70 * sc_i]
    picks["4b-aware"] = max(ok, key=lambda x: x["sh"])["key"] if ok else None
    print(f"  OOS SPY {sc_o:.1%}/{ss_o:.3f}/{sdd_o:.1%}  |  "
          f"RULES v1 {m(base.loc[OOS_START:])[0]:.1%}/{m(base.loc[OOS_START:])[1]:.3f}/"
          f"{m(base.loc[OOS_START:])[2]:.1%}")
    out = []
    for rule, key in picks.items():
        if key is None:
            print(f"  OOS pick[{rule}]: NOTHING — no in-sample point met the 4b bars")
            out.append((f"55 {tag} walk-forward {rule}: picks NOTHING", None))
            continue
        c, s_, dd = m(grid[key][0].loc[OOS_START:])
        flag = "beats SPY OOS" if s_ > ss_o else "loses to SPY OOS"
        pass4b = "clears" if (s_ > ss_o and dd >= 0.60 * sdd_o and c >= 0.70 * sc_o) else "misses"
        print(f"  OOS pick[{rule}] = K={kname(key[0])} n={key[1]}: {c:.1%}/{s_:.3f}/{dd:.1%}  "
              f"({flag}; {pass4b} the OOS 4b bars)")
        out.append((f"55 {tag} walk-forward {rule}: K={kname(key[0])} n={key[1]} OOS",
                    (c, s_, dd, flag)))
    return out


# ---------------------------------------------------------------- main
def main():
    print("=" * 124)
    print(f"Idea 55 trend-gate-lookback-primary (cloud) | {SCRIPT}")
    print("Grid: K in {200d,100d,50d,none} x n in {5,10,20,30} = 16 points, all reported. "
          "2 tuned params. vol20<0.60 held fixed.")
    print("=" * 124)

    px = load_universe()

    # ---- harness sanity: K=200, n=20 must reproduce idea 2's KEEP row (12.7%/1.093/-18.3%)
    start = px.index[260]
    r20, _ = run(px, weights_fn(200, 20), start)
    c, s_, dd = m(r20); h1, h2 = halves(r20)
    print(f"\nHARNESS CHECK  K=200d n=20 -> {c:.1%}/{s_:.3f}/{dd:.1%} halves {h1:.3f}/{h2:.3f}"
          f"   (idea 2's KEEP row: 12.7%/1.093/-18.3%, halves 1.088/1.103)")
    ok = abs(c - 0.127) < 0.002 and abs(s_ - 1.093) < 0.01 and abs(dd + 0.183) < 0.005
    print(f"HARNESS CHECK  {'PASS — construction reproduces the candidate' if ok else '*** MISMATCH ***'}")

    main_res = sweep(px, "universe.json")
    wf_main = walk_forward(main_res, "universe.json")

    # ---- where does the lookback matter? calendar-year decomposition at the candidate n=20
    print("\nCalendar-year returns at n=20 by lookback (universe.json), vs SPY:")
    spy = main_res["spy"]
    yr = {"SPY": spy.groupby(spy.index.year).apply(lambda x: (1 + x).prod() - 1)}
    for k in KS:
        r = main_res["grid"][(k, 20)][0]
        yr[f"K={kname(k)}"] = r.groupby(r.index.year).apply(lambda x: (1 + x).prod() - 1)
    ydf = pd.DataFrame(yr)
    print(ydf.to_string(float_format=lambda x: f"{x:+.1%}"))

    # ---- robustness: same grid on the broad list
    pxb = load_universe(broad=True)
    broad_res = sweep(pxb, "universe_broad.json")
    wf_broad = walk_forward(broad_res, "universe_broad.json")

    # ---- leaderboard
    bl = m(main_res["base"]); b1, b2 = halves(main_res["base"])
    print("\nLEADERBOARD rows:")
    for tagrows in (main_res["rows"], broad_res["rows"]):
        for lbl, c, s_, dd, h1, h2, oos, t, v in tagrows:
            print(f"| 2026-09-04 | {lbl} | {c:.1%} | {s_:.2f} | {dd:.1%} | {h1:.2f} / {h2:.2f} | "
                  f"{bl[1]:.2f} ({b1:.2f}/{b2:.2f}) | {v} | {SCRIPT} |")
    for lbl, r in [("55 SPY buy & hold (universe.json sample) - reference", main_res["spy"]),
                   ("55 RULES v1 live (universe.json) - baseline", main_res["base"])]:
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

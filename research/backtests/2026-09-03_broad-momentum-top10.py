#!/usr/bin/env python3
"""Idea 17 - broad-momentum-top10.

RULES v1 selection logic (baseline.score composite, price>200dma filter, vol20<0.60)
applied to the BROAD universe (research/universe_broad.json, ~136 names), equal-weight
top N. Grid:
    A: N=10, w=10.0%  -> 100% gross
    B: N=20, w=5.0%   -> 100% gross
    C: N=10, w=7.5%   ->  75% gross (apples-to-apples exposure vs RULES v1)
Weekly rebalance, 10 bps, next-day execution (engine).

Also prints the LIVE baseline (RULES v1 on the standard universe) for reference, because
compare() computes its baseline on whatever px it is handed - the v1 row inside the broad
runs is v1-on-broad, not the live book.

Walk-forward per PROTOCOL rule 8: pick the grid point on 2009-2016 by Sharpe, report
2017-2026 out-of-sample vs both baselines.
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))

import numpy as np, pandas as pd
from baseline import load_universe, rules_v1_weights, compare, score  # noqa
from engine import backtest, metrics  # noqa

pd.set_option("display.width", 200)

IS_END = "2016-12-31"
OOS_START = "2017-01-01"

GRID = [("broad-top10 100% gross (N=10,w=10%)", 10, 0.10),
        ("broad-top20 100% gross (N=20,w=5%)",  20, 0.05),
        ("broad-top10 75% gross (N=10,w=7.5%)", 10, 0.075)]


def wfn(n, w):
    return lambda px: rules_v1_weights(px, n=n, w=w)


def sub(r, a=None, b=None):
    return r.loc[a:b]


def main():
    px_b = load_universe(broad=True)
    px_s = load_universe()
    print(f"broad px: {px_b.shape[1]} tickers, {px_b.index[0].date()} -> {px_b.index[-1].date()}")
    print(f"std   px: {px_s.shape[1]} tickers, {px_s.index[0].date()} -> {px_s.index[-1].date()}")

    # ---------- 1. LIVE baseline on the standard universe (reference only) ----------
    print("\n" + "=" * 100)
    print("REFERENCE: live baseline -- RULES v1 on the STANDARD universe")
    print("=" * 100)
    live = compare("RULES v1 LIVE (standard universe)", rules_v1_weights, px_s)

    # ---------- 2. the three grid points on the broad universe ----------
    rows = []
    for name, n, w in GRID:
        print("\n" + "=" * 100)
        print(f"{name}   [broad universe; the 'RULES v1 baseline' row below is v1-on-broad, NOT the live book]")
        print("=" * 100)
        rows.append(compare(name, wfn(n, w), px_b))

    # ---------- 3. diagnostics ----------
    print("\n" + "=" * 100)
    print("DIAGNOSTICS (broad universe)")
    print("=" * 100)
    s, above, vol20 = score(px_b)
    elig = (above & (vol20 < 0.60)).sum(axis=1).loc["2009-01-01":]
    print(f"eligible names per day: mean {elig.mean():.1f}  min {elig.min()}  max {elig.max()}  "
          f"days with <10 eligible: {(elig < 10).mean():.1%}  <20: {(elig < 20).mean():.1%}")
    for name, n, w in GRID:
        res = backtest(px_b, wfn(n, w)(px_b), cost_bps=10, freq="W")
        st = px_b.index[260]
        r = res["returns"].loc[st:]
        gross = res["weights"].loc[st:].sum(axis=1)
        print(f"{name:42s} avg gross {gross.mean():.1%}  ann.turnover {res['turnover'].loc[st:].sum()/(len(r)/252):.1f}x")

    # ---------- 4. walk-forward (rule 8) ----------
    print("\n" + "=" * 100)
    print("WALK-FORWARD: choose grid point on 2009-2016, evaluate 2017-2026")
    print("=" * 100)
    st = px_b.index[260]
    series = {}
    for name, n, w in GRID:
        series[name] = backtest(px_b, wfn(n, w)(px_b), cost_bps=10, freq="W")["returns"].loc[st:]
    series["RULES v1 on broad universe"] = backtest(px_b, rules_v1_weights(px_b), cost_bps=10, freq="W")["returns"].loc[st:]
    st_s = px_s.index[260]
    series["RULES v1 LIVE (standard universe)"] = backtest(px_s, rules_v1_weights(px_s), cost_bps=10, freq="W")["returns"].loc[st_s:]
    series["SPY"] = px_b["SPY"].pct_change().fillna(0).loc[st:]

    wf = []
    for k, r in series.items():
        i, o = sub(r, None, IS_END), sub(r, OOS_START, None)
        wf.append(dict(name=k, IS_Sharpe=metrics(i)["Sharpe"], IS_MaxDD=metrics(i)["MaxDD"],
                       IS_CAGR=metrics(i)["CAGR"], OOS_Sharpe=metrics(o)["Sharpe"],
                       OOS_MaxDD=metrics(o)["MaxDD"], OOS_CAGR=metrics(o)["CAGR"]))
    wfdf = pd.DataFrame(wf).set_index("name")
    print(f"IS window: {series['SPY'].loc[:IS_END].index[0].date()} -> {series['SPY'].loc[:IS_END].index[-1].date()}")
    print(f"OOS window: {series['SPY'].loc[OOS_START:].index[0].date()} -> {series['SPY'].loc[OOS_START:].index[-1].date()}")
    print(wfdf.to_string(float_format=lambda x: f"{x:.3f}"))

    cand = wfdf.loc[[g[0] for g in GRID], "IS_Sharpe"].idxmax()
    print(f"\nSelected on 2009-2016 IS Sharpe only: {cand} (IS Sharpe {wfdf.loc[cand,'IS_Sharpe']:.3f})")
    print(f"  OOS Sharpe {wfdf.loc[cand,'OOS_Sharpe']:.3f}  MaxDD {wfdf.loc[cand,'OOS_MaxDD']:.1%}")
    for b in ("RULES v1 on broad universe", "RULES v1 LIVE (standard universe)", "SPY"):
        print(f"  vs {b:36s} OOS Sharpe {wfdf.loc[b,'OOS_Sharpe']:.3f}  MaxDD {wfdf.loc[b,'OOS_MaxDD']:.1%}")

    print("\n=== LEADERBOARD rows ===")
    for r in rows:
        print(r["row"].rsplit("|", 2)[0] + "| research/backtests/2026-09-03_broad-momentum-top10.py |")
    print("\n(live baseline row for reference)")
    print(live["row"].rsplit("|", 2)[0] + "| research/backtests/2026-09-03_broad-momentum-top10.py |")


if __name__ == "__main__":
    main()

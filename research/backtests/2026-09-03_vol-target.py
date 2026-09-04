#!/usr/bin/env python3
"""Idea 12 — "vol-target": scale RULES v1 weights toward a constant portfolio volatility.

Construction
------------
1. Start from baseline.rules_v1_weights (equal-weight top 5 @ 15% each = 75% gross).
2. Run the *unscaled* v1 book through engine.backtest(freq="W", cost_bps=10) to get its own
   daily return series.
3. Realized portfolio vol = trailing 20-day std of those returns * sqrt(252), lagged one day
   (shift(1)) so the scale used on day t only sees returns through t-1 -> no look-ahead.
4. Scale the whole weight row by target_vol / realized_vol, capped so that gross exposure
   never exceeds 100% (no leverage). Warm-up days (no vol estimate) use scale = 1.0.

The scaling factor moves daily, but the engine only rebalances weekly (freq="W"), so the book
actually takes on the scale in force at each weekly rebalance date and then drifts. That is
realistic (you do not trade every day) and is stated in the write-up.

Grid: target vol in {10%, 14%} — 2 points, reported both.
Deterministic, standalone. Costs 10 bps, freq="W".
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, rules_v1_weights, compare
from engine import backtest

COST_BPS = 10
FREQ = "W"
GROSS_CAP = 1.00          # no leverage
VOL_LOOKBACK = 20


def v1_daily_returns(px, w1):
    """Unscaled RULES v1 daily return series under the real execution assumptions."""
    return backtest(px, w1, cost_bps=COST_BPS, freq=FREQ)["returns"]


def vol_target_weights(target_vol):
    def _fn(px):
        w1 = rules_v1_weights(px)
        r1 = v1_daily_returns(px, w1)
        # trailing 20d annualized vol of the strategy's OWN returns, lagged 1 day
        rv = (r1.rolling(VOL_LOOKBACK).std() * np.sqrt(252)).shift(1)
        gross = w1.sum(axis=1)
        raw = target_vol / rv.replace(0.0, np.nan)
        # cap so gross * scale <= GROSS_CAP; scale is irrelevant where gross == 0
        cap = (GROSS_CAP / gross.replace(0.0, np.nan)).reindex(raw.index)
        scale = raw.clip(upper=cap).fillna(1.0).clip(lower=0.0)
        return w1.mul(scale, axis=0)
    return _fn


def exposure_stats(px, wfn, start):
    w = wfn(px)
    w1 = rules_v1_weights(px)
    g, g1 = w.sum(axis=1).loc[start:], w1.sum(axis=1).loc[start:]
    live = g1 > 1e-9                       # days the baseline is actually invested
    at_cap = (g[live] >= GROSS_CAP - 1e-9)
    return dict(avg_gross=g.mean(), avg_gross_invested=g[live].mean(),
                pct_days_at_cap=at_cap.mean(), max_gross=g.max(), min_gross=g[live].min(),
                base_avg_gross=g1.mean(), base_avg_gross_invested=g1[live].mean())


def main():
    px = load_universe()
    start = px.index[260]
    print(f"Universe: {px.shape[1]} tickers, {px.index[0].date()} -> {px.index[-1].date()}")
    print(f"Eval sample starts {start.date()} (260-day warm-up skipped by compare())\n")

    for tv in (0.10, 0.14):
        name = f"vol-target {tv:.0%}"
        wfn = vol_target_weights(tv)
        print("=" * 78)
        print(f"### {name}")
        out = compare(name, wfn, px, freq=FREQ, cost_bps=COST_BPS)
        e = exposure_stats(px, wfn, start)
        print(f"Avg gross exposure (all days): {e['avg_gross']:.1%}   "
              f"(baseline {e['base_avg_gross']:.1%})")
        print(f"Avg gross exposure (invested days only): {e['avg_gross_invested']:.1%}   "
              f"(baseline {e['base_avg_gross_invested']:.1%})")
        print(f"Days at the 100% gross cap (invested days): {e['pct_days_at_cap']:.1%}   "
              f"min/max gross on invested days: {e['min_gross']:.1%} / {e['max_gross']:.1%}")
        print()


if __name__ == "__main__":
    main()

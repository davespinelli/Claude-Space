#!/usr/bin/env python3
"""Idea 5: dual-momentum-classes (Antonacci-style Global Equities / Dual Momentum).

Universe of risky asset classes: SPY (US eq), EFA (dev intl eq), EEM (EM eq),
TLT (long UST), GLD (gold), DBC (broad commodities). SHY = risk-free proxy.

Each rebalance:
  1. Relative momentum: rank the 6 risky sleeves by 12-month total return.
  2. Take the top K (K = 1 or 2), equal weight 1/K each.
  3. Absolute momentum: a selected sleeve is held only if its 12m return exceeds
     SHY's 12m return; otherwise that 1/K slice is parked in SHY.
  So for K=1 this is exactly canonical dual momentum (hold winner or SHY).

12m return is measured as px / px.shift(252) - 1 on adjusted closes (daily bars,
252 trading days ~ 12 months). Weights are computed every day; the engine only
acts on them on the rebalance schedule, and applies them at the NEXT close.

Two tuned parameters: lookback (252d, fixed at the canonical 12m, not searched)
and K (tested at 1 and 2, both reported). Costs 10 bps per unit turnover.

Run: .venv/bin/python research/backtests/2026-09-03_dual-momentum-classes.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
from baseline import load_universe, compare, backtest  # noqa: E402

RISKY = ["SPY", "EFA", "EEM", "TLT", "GLD", "DBC"]
SAFE = "SHY"
LOOKBACK = 252  # ~12 months of trading days


def dual_momentum_weights(px: pd.DataFrame, k: int = 1, lookback: int = LOOKBACK) -> pd.DataFrame:
    """Target weights: 1/k in each of the top-k risky sleeves that beat SHY, rest in SHY.

    Returns a full-universe frame; every ticker outside RISKY+[SAFE] is exactly 0.
    """
    r12 = px / px.shift(lookback) - 1.0
    risky = r12[RISKY]
    safe = r12[SAFE]

    # Relative momentum: rank risky sleeves, best = 1. Assets with no history rank last.
    rank = risky.rank(axis=1, ascending=False, na_option="bottom")
    selected = (rank <= k) & risky.notna()

    # Absolute momentum: keep the slice only if it beats the risk-free proxy.
    beats_safe = risky.gt(safe, axis=0).fillna(False)
    hold = selected & beats_safe

    w = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    w.loc[:, RISKY] = hold.astype(float).values / float(k)
    # Everything not deployed into risky sleeves sits in SHY (also covers the
    # warm-up period, where risky weights are all zero -> 100% SHY).
    w.loc[:, SAFE] = 1.0 - w[RISKY].sum(axis=1)
    # No trades until both the risky and the safe lookback exist.
    warm = safe.isna()
    w.loc[warm, :] = 0.0
    return w


def main() -> None:
    px = load_universe()
    missing = [t for t in RISKY + [SAFE] if t not in px.columns]
    if missing:
        raise SystemExit(f"missing tickers in universe: {missing}")
    print(f"sample: {px.index[0].date()} -> {px.index[-1].date()}  ({px.shape[1]} tickers)")

    results = {}
    for k in (1, 2):
        for freq, label in (("M", "monthly"), ("W", "weekly")):
            name = f"dual-momentum-classes K={k} {label}"
            print("\n" + "=" * 78 + f"\n{name}\n" + "=" * 78)
            fn = (lambda p, _k=k: dual_momentum_weights(p, k=_k))
            out = compare(name, fn, px, freq=freq, cost_bps=10)
            # Turnover context (not part of compare's table).
            res = backtest(px, fn(px), cost_bps=10, freq=freq)
            start = px.index[260]
            to = res["turnover"].loc[start:]
            yrs = len(to) / 252.0
            print(f"avg annual turnover: {to.sum() / yrs:.2f}x")
            results[name] = out

    print("\n\nAll LEADERBOARD rows:")
    for name, out in results.items():
        print(out["row"])


if __name__ == "__main__":
    main()

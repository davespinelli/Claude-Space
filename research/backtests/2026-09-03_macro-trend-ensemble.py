#!/usr/bin/env python3
"""Idea 18 — "macro-trend-ensemble": time-series momentum across 9 macro ETFs
(Moskowitz-Ooi-Pedersen 2012 / Hurst-Ooi-Pedersen style), sized by inverse-vol risk parity.

Universe (9): SPY QQQ IWM EFA EEM TLT GLD DBC UUP. Everything outside these 9 gets weight 0,
but the price panel is the standard research universe (baseline.load_universe()) so that the
comparison baseline printed by compare() is the live RULES v1 book on its own universe.

Construction (identical for both variants except the vote inputs)
-----------------------------------------------------------------
1. Trend vote v_i(t) in {0, 1/3, 2/3, 1} = fraction of three trend tests that are ON.
     Variant A (moving averages):   price > 50d MA, price > 100d MA, price > 200d MA
     Variant B (momentum signs):    12-1 momentum > 0  (px.shift(21)/px.shift(252) - 1),
                                    6m return > 0      (px/px.shift(126) - 1),
                                    3m return > 0      (px/px.shift(63) - 1)
2. Risk-parity weight rp_i(t) = (1/vol_i) / sum_j (1/vol_j) over the 9 assets, where vol is the
   trailing 60-day std of daily returns (annualization cancels in the normalization). The rp
   row sums to 1.0, so a fully-long book (every vote = 1) has exactly 100% gross.
3. Position w_i(t) = v_i(t) * rp_i(t). Anything not voted long is cash; gross <= 100%,
   long-only, no leverage.

No look-ahead: every input at date t uses data through t only, and engine.backtest applies the
row decided at t to the t+1 close. Weekly rebalance (freq="W"), 10 bps per unit turnover.

Walk-forward (PROTOCOL rule 8): the construction has NO tuned parameters — the lookbacks are the
canonical TSMOM set (50/100/200 MA; 12-1/6m/3m; 60d vol) taken from the source papers, not chosen
on this data — so there is nothing to fit on 2009-2016. The script therefore reports the
2009-2016 vs 2017-2026 split straight, for both variants, the RULES v1 baseline and SPY.

Deterministic, standalone.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, rules_v1_weights, compare
from engine import backtest, metrics

COST_BPS = 10
FREQ = "W"
MACRO = ["SPY", "QQQ", "IWM", "EFA", "EEM", "TLT", "GLD", "DBC", "UUP"]
MA_WINDOWS = (50, 100, 200)
MOM_LAGS = (252, 126, 63)      # 12-1 (with 21d skip), 6m, 3m
VOL_WINDOW = 60
SPLIT = "2017-01-01"


def _risk_parity(sub: pd.DataFrame) -> pd.DataFrame:
    """Inverse trailing-60d-vol weights over the 9 macro assets, rows normalized to 1.0."""
    vol = sub.pct_change().rolling(VOL_WINDOW).std()
    inv = 1.0 / vol.replace(0.0, np.nan)
    return inv.div(inv.sum(axis=1), axis=0)


def _vote_ma(sub: pd.DataFrame) -> pd.DataFrame:
    votes = [(sub > sub.rolling(n).mean()).astype(float).where(sub.rolling(n).mean().notna())
             for n in MA_WINDOWS]
    return sum(votes) / len(votes)


def _vote_mom(sub: pd.DataFrame) -> pd.DataFrame:
    signals = [sub.shift(21) / sub.shift(MOM_LAGS[0]) - 1,   # 12-1 momentum
               sub / sub.shift(MOM_LAGS[1]) - 1,             # 6m
               sub / sub.shift(MOM_LAGS[2]) - 1]             # 3m
    votes = [(s > 0).astype(float).where(s.notna()) for s in signals]
    return sum(votes) / len(votes)


def macro_trend_weights(vote_fn):
    def _fn(px: pd.DataFrame) -> pd.DataFrame:
        sub = px[MACRO]
        w = (vote_fn(sub) * _risk_parity(sub)).fillna(0.0)
        out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
        out[MACRO] = w                                   # zero weight outside the 9
        return out
    return _fn


VARIANTS = {
    "macro-trend-ensemble A (MA votes)": macro_trend_weights(_vote_ma),
    "macro-trend-ensemble B (momentum votes)": macro_trend_weights(_vote_mom),
}


def period_row(label, r):
    m = metrics(r)
    return dict(period=label, start=str(r.index[0].date()), end=str(r.index[-1].date()),
                CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], Vol=m["Vol"])


def main():
    px = load_universe()
    missing = [t for t in MACRO if t not in px.columns]
    if missing:
        raise SystemExit(f"missing tickers in universe panel: {missing}")
    start = px.index[260]
    print(f"Price panel: {px.shape[1]} tickers, {px.index[0].date()} -> {px.index[-1].date()}")
    print(f"Macro sleeve: {MACRO}")
    print(f"Eval sample starts {start.date()} (260-day warm-up skipped by compare())\n")

    series = {}
    for name, wfn in VARIANTS.items():
        print("=" * 90)
        print(f"### {name}")
        compare(name, wfn, px, freq=FREQ, cost_bps=COST_BPS)
        res = backtest(px, wfn(px), cost_bps=COST_BPS, freq=FREQ)
        series[name] = res["returns"].loc[start:]
        w = wfn(px).loc[start:]
        g = w.sum(axis=1)
        vote_mean = (w[MACRO] > 0).sum(axis=1)
        print(f"Avg gross exposure: {g.mean():.1%}  (min {g.min():.1%}, max {g.max():.1%}, "
              f"median {g.median():.1%}, 100% gross = fully long)")
        print(f"Avg # of the 9 assets with any weight: {vote_mean.mean():.2f}")
        print(f"Annual turnover: {res['turnover'].loc[start:].sum() / (len(series[name]) / 252):.1f}x\n")

    base = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
    series["RULES v1 baseline"] = base
    series["SPY"] = px["SPY"].pct_change().fillna(0).loc[start:]

    print("=" * 90)
    print("### Walk-forward split (PROTOCOL rule 8): 2009-2016 vs 2017-2026, no parameters tuned\n")
    rows = []
    for name, r in series.items():
        for label, seg in (("2009-2016", r.loc[:"2016-12-31"]), ("2017-2026", r.loc[SPLIT:])):
            rows.append(dict(strategy=name, **period_row(label, seg)))
    df = pd.DataFrame(rows).set_index(["strategy", "period"])
    print(df.to_string(float_format=lambda x: f"{x:.3f}"))

    print("\nAverage gross exposure by period:")
    for name, wfn in VARIANTS.items():
        g = wfn(px).loc[start:].sum(axis=1)
        print(f"  {name}: full {g.mean():.1%} | 2009-2016 {g.loc[:'2016-12-31'].mean():.1%} "
              f"| 2017-2026 {g.loc[SPLIT:].mean():.1%}")
    gb = rules_v1_weights(px).loc[start:].sum(axis=1)
    print(f"  RULES v1 baseline: full {gb.mean():.1%} | 2009-2016 {gb.loc[:'2016-12-31'].mean():.1%} "
          f"| 2017-2026 {gb.loc[SPLIT:].mean():.1%}")


if __name__ == "__main__":
    main()

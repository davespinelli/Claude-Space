#!/usr/bin/env python3
"""Reusable daily-bar backtester (long-only or long/short weights), with costs,
rebalance schedules, metrics, and a markdown+PNG report.

A strategy is any function f(prices: DataFrame[date x ticker]) -> DataFrame of target
weights (same index/columns, rows sum to <=1 for long-only). Weights are applied at the
NEXT day's close (no look-ahead). See run_samples.py for examples.
"""
from __future__ import annotations
import datetime as dt
from pathlib import Path
import numpy as np, pandas as pd

def load_prices(tickers, start="2010-01-01", end=None) -> pd.DataFrame:
    import yfinance as yf
    px = yf.download(list(tickers), start=start, end=end, auto_adjust=True, progress=False)["Close"]
    if isinstance(px, pd.Series): px = px.to_frame(tickers[0])
    return px.dropna(how="all").ffill()

def rebalance_mask(idx: pd.DatetimeIndex, freq: str) -> pd.Series:
    """True on the last trading day of each period. freq in {'D','W','M','Q'}."""
    if freq == "D": return pd.Series(True, index=idx)
    key = {"W": idx.to_period("W"), "M": idx.to_period("M"), "Q": idx.to_period("Q")}[freq]
    s = pd.Series(key, index=idx)
    return s != s.shift(-1)

def backtest(prices: pd.DataFrame, weights: pd.DataFrame, cost_bps=5.0, freq="M") -> dict:
    """Hold target weights, rebalancing only on schedule; drift between rebalances."""
    rets = prices.pct_change().fillna(0.0)
    w_target = weights.reindex(prices.index).fillna(0.0).shift(1)  # decided at t, applied at t+1
    mask = rebalance_mask(prices.index, freq).shift(1, fill_value=False)
    held = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
    cur = np.zeros(len(prices.columns)); turnover = pd.Series(0.0, index=prices.index)
    for i, d in enumerate(prices.index):
        if mask.iloc[i] or i == 0:
            new = w_target.iloc[i].values
            turnover.iloc[i] = np.abs(new - cur).sum(); cur = new
        held.iloc[i] = cur
        growth = cur * (1 + rets.iloc[i].values)                  # drift
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    port = (held * rets).sum(axis=1) - turnover * cost_bps / 1e4
    equity = (1 + port).cumprod()
    return {"returns": port, "equity": equity, "weights": held, "turnover": turnover}

def metrics(r: pd.Series, rf=0.0) -> dict:
    eq = (1 + r).cumprod(); yrs = len(r) / 252
    cagr = eq.iloc[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan
    dd = eq / eq.cummax() - 1
    vol = r.std() * np.sqrt(252)
    down = r[r < 0].std() * np.sqrt(252)
    return {"CAGR": cagr, "Vol": vol, "Sharpe": (r.mean() * 252 - rf) / vol if vol else np.nan,
            "Sortino": (r.mean() * 252 - rf) / down if down else np.nan, "MaxDD": dd.min(),
            "Calmar": cagr / abs(dd.min()) if dd.min() else np.nan,
            "WinRate": (r > 0).mean(), "BestDay": r.max(), "WorstDay": r.min(),
            "Total": eq.iloc[-1] - 1, "Years": yrs}

def split_metrics(r: pd.Series) -> pd.DataFrame:
    h = len(r) // 2
    return pd.DataFrame({"Full": metrics(r), "1st half": metrics(r.iloc[:h]), "2nd half": metrics(r.iloc[h:])})

def report(name: str, res: dict, bench: pd.Series, out_dir: Path, notes: str = "") -> Path:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    out_dir.mkdir(parents=True, exist_ok=True)
    r, b = res["returns"], bench.reindex(res["returns"].index).fillna(0.0)
    m = pd.DataFrame({name: metrics(r), "Benchmark": metrics(b)})
    fmt = lambda k, v: f"{v:.2%}" if k in ("CAGR","Vol","MaxDD","WinRate","BestDay","WorstDay","Total") else f"{v:.2f}"
    tbl = "| Metric | " + " | ".join(m.columns) + " |\n|---|" + "---|" * len(m.columns) + "\n"
    tbl += "\n".join(f"| {k} | " + " | ".join(fmt(k, m.loc[k, c]) for c in m.columns) + " |" for k in m.index)
    sm = split_metrics(r)
    sub = "| Metric | Full | 1st half | 2nd half |\n|---|---|---|---|\n" + "\n".join(
        f"| {k} | " + " | ".join(fmt(k, sm.loc[k, c]) for c in sm.columns) + " |" for k in ("CAGR","Sharpe","MaxDD"))
    yearly = pd.DataFrame({name: r, "Benchmark": b}).groupby(r.index.year).apply(lambda x: (1 + x).prod() - 1)
    ytbl = "| Year | " + " | ".join(yearly.columns) + " |\n|---|---|---|\n" + "\n".join(
        f"| {y} | " + " | ".join(f"{v:+.1%}" for v in row) + " |" for y, row in yearly.iterrows())
    fig, ax = plt.subplots(2, 1, figsize=(10, 7), sharex=True, gridspec_kw={"height_ratios": [3, 1]})
    res["equity"].plot(ax=ax[0], label=name, logy=True); (1 + b).cumprod().plot(ax=ax[0], label="Benchmark", alpha=.7)
    ax[0].legend(); ax[0].set_title(f"{name} — growth of $1 (log)"); ax[0].grid(alpha=.3)
    (res["equity"] / res["equity"].cummax() - 1).plot(ax=ax[1], color="firebrick"); ax[1].set_title("Drawdown"); ax[1].grid(alpha=.3)
    slug = name.lower().replace(" ", "_"); png = out_dir / f"{slug}.png"; fig.tight_layout(); fig.savefig(png, dpi=110); plt.close(fig)
    md = out_dir / f"{slug}.md"
    md.write_text(f"# Backtest: {name}\n\n{notes}\n\n**Period:** {r.index[0].date()} → {r.index[-1].date()} · **Costs:** modeled per rebalance · **Avg annual turnover:** {res['turnover'].sum()/metrics(r)['Years']:.1f}x\n\n"
                  f"![equity]({png.name})\n\n## Summary\n{tbl}\n\n## Robustness (sample halves)\n{sub}\n\n## Calendar-year returns\n{ytbl}\n\n"
                  f"_Generated {dt.date.today()} by Claude Space backtester. Past performance is not indicative of future results. Research, not investment advice._\n")
    return md

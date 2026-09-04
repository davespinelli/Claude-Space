#!/usr/bin/env python3
"""Three sample strategies -> products/backtester/samples/*.md (+png). Also the portfolio pieces for the gig."""
import json, sys
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).parent))
from engine import load_prices, backtest, report

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "products" / "backtester" / "samples"
U = json.loads((ROOT / "research" / "universe.json").read_text())

def momentum_topn(px, n=5, lookback=252, skip=21, trend=True):
    mom = px.shift(skip) / px.shift(lookback) - 1
    ok = (px > px.rolling(200).mean()) if trend else pd.DataFrame(True, index=px.index, columns=px.columns)
    ranked = mom.where(ok).rank(axis=1, ascending=False)
    w = (ranked <= n).astype(float); return w.div(w.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)

def trend_filter(px, ticker="SPY", ma=200):
    w = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    w[ticker] = (px[ticker] > px[ticker].rolling(ma).mean()).astype(float); return w

def rsi_meanrev(px, n=2, buy=10, sell=70):
    d = px.diff(); up = d.clip(lower=0).ewm(alpha=1/n, adjust=False).mean(); dn = (-d.clip(upper=0)).ewm(alpha=1/n, adjust=False).mean()
    rsi = 100 - 100 / (1 + up / dn.replace(0, np.nan)); above = px > px.rolling(200).mean()
    pos = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
    pos[(rsi < buy) & above] = 1.0; pos[rsi > sell] = 0.0; pos = pos.ffill().fillna(0.0)
    return pos.div(pos.sum(axis=1).clip(lower=1), axis=0)

if __name__ == "__main__":
    sectors = U["sectors"]; px = load_prices(sorted(set(sectors + ["SPY", "TLT", "GLD"])), start="2008-01-01")
    spy = px["SPY"].pct_change().fillna(0.0)
    r1 = backtest(px[sectors], momentum_topn(px[sectors], n=3), cost_bps=5, freq="M")
    p1 = report("Sector Momentum Top3", r1, spy, OUT, "Monthly rotation into the 3 sector ETFs with the highest 12-1 month momentum, only if above their 200-day average; equal weight; cash otherwise. 5 bps cost per unit turnover.")
    r2 = backtest(px[["SPY"]], trend_filter(px[["SPY"]]), cost_bps=5, freq="D")
    p2 = report("SPY 200d Trend Filter", r2, spy, OUT, "Hold SPY when its close is above the 200-day moving average, otherwise cash. Checked daily.")
    r3 = backtest(px[sectors], rsi_meanrev(px[sectors]), cost_bps=5, freq="D")
    p3 = report("Sector RSI2 Mean Reversion", r3, spy, OUT, "Buy sector ETFs when 2-day RSI < 10 while above the 200-day average; exit when RSI2 > 70. Equal-weight across open positions. Daily.")
    for p in (p1, p2, p3): print("wrote", p.relative_to(ROOT))

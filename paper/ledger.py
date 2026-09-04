#!/usr/bin/env python3
"""Paper-trading ledger. Positions live in paper/portfolio.json; every run marks to
market and appends a NAV row to paper/nav.csv. Trades are appended to paper/trades.csv.
Usage:
  .venv/bin/python paper/ledger.py mark                     # mark-to-market, append NAV
  .venv/bin/python paper/ledger.py trade BUY SPY 10 "reason" # record a trade at last close
"""
import sys, json, datetime as dt
from pathlib import Path
import pandas as pd, yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
PF = ROOT / "paper" / "portfolio.json"
NAV = ROOT / "paper" / "nav.csv"
TRADES = ROOT / "paper" / "trades.csv"

def load():
    if PF.exists(): return json.loads(PF.read_text())
    return {"start_date": str(dt.date.today()), "start_cash": 100000.0, "cash": 100000.0, "positions": {}}

def save(p): PF.write_text(json.dumps(p, indent=2))

def last_prices(tickers):
    if not tickers: return {}
    d = yf.download(list(tickers), period="5d", auto_adjust=True, progress=False)["Close"].ffill()
    return {t: float(d[t].iloc[-1]) for t in d.columns} if len(tickers) > 1 else {tickers[0]: float(d.iloc[-1].item() if hasattr(d.iloc[-1], "item") else d.iloc[-1])}

def mark(p):
    px = last_prices(list(p["positions"]))
    equity = p["cash"] + sum(q * px[t] for t, q in p["positions"].items())
    bench = last_prices(["SPY"])["SPY"]
    row = pd.DataFrame([{"date": dt.date.today(), "nav": round(equity, 2), "cash": round(p["cash"], 2), "spy": round(bench, 2)}])
    row.to_csv(NAV, mode="a", header=not NAV.exists(), index=False)
    ret = equity / p["start_cash"] - 1
    print(f"NAV ${equity:,.2f} ({ret:+.2%} since {p['start_date']}), cash ${p['cash']:,.2f}, {len(p['positions'])} positions")
    for t, q in p["positions"].items(): print(f"  {t}: {q} @ {px[t]:.2f} = ${q*px[t]:,.2f}")

def trade(p, side, t, qty, reason):
    qty = float(qty); px = last_prices([t])[t]; cost = qty * px
    if side == "BUY":
        if cost > p["cash"]: sys.exit(f"insufficient cash: need {cost:.2f}, have {p['cash']:.2f}")
        p["cash"] -= cost; p["positions"][t] = p["positions"].get(t, 0) + qty
    elif side == "SELL":
        if p["positions"].get(t, 0) < qty: sys.exit("insufficient position")
        p["cash"] += cost; p["positions"][t] -= qty
        if p["positions"][t] == 0: del p["positions"][t]
    pd.DataFrame([{"date": dt.date.today(), "side": side, "ticker": t, "qty": qty, "price": round(px, 4), "reason": reason}]).to_csv(TRADES, mode="a", header=not TRADES.exists(), index=False)
    print(f"{side} {qty} {t} @ {px:.2f} — {reason}")

if __name__ == "__main__":
    p = load(); cmd = sys.argv[1] if len(sys.argv) > 1 else "mark"
    if cmd == "mark": mark(p)
    elif cmd == "trade": trade(p, sys.argv[2].upper(), sys.argv[3].upper(), sys.argv[4], " ".join(sys.argv[5:]) or "n/a")
    save(p)

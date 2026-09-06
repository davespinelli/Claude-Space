#!/usr/bin/env python3
"""Alpaca PAPER execution for RULES.md (v2). Takes trade prices from the newest
reports/<date>.csv (research/scan.py) and the held set from the 200d +/-3% band computed over
data/prices.csv, reconciles against the Alpaca paper account, and submits market orders.
Never touches a live endpoint: ALPACA_BASE_URL is forced to the paper host.

Usage:
  .venv/bin/python products/bot/bot.py --dry-run      # show intended orders only
  .venv/bin/python products/bot/bot.py                # submit paper orders
Keys: .env in repo root (gitignored): ALPACA_API_KEY, ALPACA_SECRET_KEY
"""
import argparse, datetime as dt, json, os, sys
from functools import lru_cache
from pathlib import Path
import numpy as np, pandas as pd
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")
PAPER_URL = "https://paper-api.alpaca.markets"
EXCLUDE = {"BTC-USD", "ETH-USD"}
PRICES = ROOT / "data" / "prices.csv"
# RULES.md v2: hold every name inside the 200d +/-band, gross/N each, rest in cash, weekly.
# min_trade is a fraction of ONE full position (a v1-style 2%-of-NAV band would suppress every
# 1.34%-of-NAV order).
RULES = dict(version="v2", band=0.03, gross=0.75, min_trade=0.10)
LOG = ROOT / "products" / "bot" / "orders.csv"

def latest_scan() -> pd.DataFrame:
    csvs = sorted((ROOT / "reports").glob("????-??-??.csv"))
    if not csvs: sys.exit("no scan csv; run research/scan.py first")
    df = pd.read_csv(csvs[-1], index_col=0); df = df[~df.index.isin(EXCLUDE)]
    df.index = df.index.str.replace("-", ".")      # BRK-B -> BRK.B for Alpaca
    return df.sort_values("score", ascending=False)

def _norm(s: str) -> str:
    """Alpaca 'BRK.B' and yfinance 'BRK-B' onto one key."""
    return s.replace(".", "-")

@lru_cache(maxsize=1)
def band_state(band: float = 0.03):
    """RULES v2 clause 2, from the full-history cache: ({names IN}, N, asof_date).

    The band is path-dependent, so it must be computed over the whole history — the 15-month
    window in reports/<date>.csv is not enough. data/prices.csv is refreshed by
    research/cache_prices.py earlier in the same daily job.
    """
    if not PRICES.exists(): sys.exit(f"RULES v2 needs {PRICES}; run research/cache_prices.py")
    px = pd.read_csv(PRICES, index_col=0, parse_dates=True).sort_index()
    px = px.drop(columns=[c for c in px.columns if c in EXCLUDE], errors="ignore")
    px = px.dropna(how="all").ffill()
    ma = px.rolling(200).mean()
    raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
    raw = raw.mask(px > ma * (1 + band), 1.0).mask(px < ma * (1 - band), 0.0)
    st = (raw.ffill().fillna(0.0) > 0.5).iloc[-1]
    last, ma_last = px.iloc[-1], ma.iloc[-1]
    d200 = {_norm(c): (last[c] / ma_last[c] - 1) for c in px.columns if pd.notna(ma_last[c])}
    return {_norm(c) for c in px.columns if st[c]}, int(last.notna().sum()), px.index[-1].date(), d200

def unit_dollars(nav: float) -> float:
    """RULES v2 clause 4: one full position = gross/N of NAV."""
    return RULES["gross"] / band_state(RULES["band"])[1] * nav

def targets(df: pd.DataFrame, nav: float, held: dict, is_rebalance_day: bool) -> dict:
    """Return {symbol: target_dollars}. Implements RULES.md v2."""
    in_names, n_univ, asof, _ = band_state(RULES["band"])
    if not is_rebalance_day:
        return dict(held)                          # clause 6: no intra-week trading
    unit = RULES["gross"] / n_univ * nav           # clause 4
    tgt = {sym: 0.0 for sym in held}               # clause 5: sell anything not re-bought
    for sym in df.index:
        if _norm(sym) in in_names: tgt[sym] = unit
    return tgt

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--force-rebalance", action="store_true")
    a = ap.parse_args()
    key, sec = os.getenv("ALPACA_API_KEY", ""), os.getenv("ALPACA_SECRET_KEY", "")
    have_keys = key and sec and "PASTE" not in key
    df = latest_scan(); today = dt.date.today()
    is_reb = a.force_rebalance or today.weekday() == 4
    if not have_keys:
        print("No Alpaca keys in .env — offline dry run with $100k notional and no positions.")
        nav, held, prices = 100_000.0, {}, df.close.to_dict()
    else:
        from alpaca.trading.client import TradingClient
        tc = TradingClient(key, sec, paper=True, url_override=PAPER_URL)
        acct = tc.get_account(); nav = float(acct.equity)
        held = {p.symbol: float(p.market_value) for p in tc.get_all_positions()}
        prices = {p.symbol: float(p.current_price) for p in tc.get_all_positions()}; prices.update({s: c for s, c in df.close.items() if s not in prices})
        print(f"Paper account: equity ${nav:,.2f}, cash ${float(acct.cash):,.2f}, {len(held)} positions; rebalance day={is_reb}")
    in_names, n_univ, asof, d200 = band_state(RULES["band"])
    if asof < today - dt.timedelta(days=5):
        print(f"WARNING: {PRICES.name} is stale (last {asof}); run research/cache_prices.py first.")
    print(f"RULES v2: {len(in_names)}/{n_univ} names inside the 200d +/-{RULES['band']:.0%} band as of {asof}; "
          f"one position = ${unit_dollars(nav):,.0f}")
    tgt = targets(df, nav, held, is_reb)
    orders = []
    for sym, dollars in tgt.items():
        if sym not in prices: print(f"  skip {sym}: no price in the report"); continue
        cur = held.get(sym, 0.0); delta = dollars - cur
        if dollars > 0 and abs(delta) < RULES["min_trade"] * unit_dollars(nav): continue   # drift band
        qty = int(abs(delta) // prices[sym])
        if qty == 0: continue
        orders.append(dict(date=today, symbol=sym, side="buy" if delta > 0 else "sell", qty=qty, ref_price=round(prices[sym], 2),
                           reason=f"RULES {RULES['version']}: {'rebalance' if dollars > 0 else 'exit'} "
                                  f"band={'in' if _norm(sym) in in_names else 'out'} d200={d200.get(_norm(sym), float('nan')):+.1%}"))
    if not orders: print("No orders."); return
    print(pd.DataFrame(orders).to_string(index=False))
    if a.dry_run or not have_keys: print("(dry run — nothing submitted)"); return
    from alpaca.trading.requests import MarketOrderRequest
    from alpaca.trading.enums import OrderSide, TimeInForce
    for o in sorted(orders, key=lambda x: x["side"] != "sell"):          # sells first to free cash
        r = tc.submit_order(MarketOrderRequest(symbol=o["symbol"], qty=o["qty"], side=OrderSide.BUY if o["side"] == "buy" else OrderSide.SELL, time_in_force=TimeInForce.DAY))
        o["order_id"] = str(r.id); print("submitted", o["side"], o["qty"], o["symbol"], r.id)
    pd.DataFrame(orders).to_csv(LOG, mode="a", header=not LOG.exists(), index=False)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Alpaca PAPER execution for RULES.md. Reads the newest reports/<date>.csv from
research/scan.py, computes target positions per the rules, reconciles against the
Alpaca paper account, and submits market orders. Never touches a live endpoint:
ALPACA_BASE_URL is forced to the paper host.

Usage:
  .venv/bin/python products/bot/bot.py --dry-run      # show intended orders only
  .venv/bin/python products/bot/bot.py                # submit paper orders
Keys: .env in repo root (gitignored): ALPACA_API_KEY, ALPACA_SECRET_KEY
"""
import argparse, datetime as dt, json, os, sys
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")
PAPER_URL = "https://paper-api.alpaca.markets"
EXCLUDE = {"BTC-USD", "ETH-USD"}
RULES = dict(version="v1", n_select=5, n_hold=8, weight=0.15, max_w=0.22, min_w=0.08, max_vol=0.60)
LOG = ROOT / "products" / "bot" / "orders.csv"

def latest_scan() -> pd.DataFrame:
    csvs = sorted((ROOT / "reports").glob("????-??-??.csv"))
    if not csvs: sys.exit("no scan csv; run research/scan.py first")
    df = pd.read_csv(csvs[-1], index_col=0); df = df[~df.index.isin(EXCLUDE)]
    df.index = df.index.str.replace("-", ".")      # BRK-B -> BRK.B for Alpaca
    return df.sort_values("score", ascending=False)

def targets(df: pd.DataFrame, nav: float, held: dict, is_rebalance_day: bool) -> dict:
    """Return {symbol: target_dollars}. Implements RULES.md v1."""
    elig = df[(df.above_200 == True) & (df.vol20 < RULES["max_vol"])]
    top_sel = list(elig.head(RULES["n_select"]).index); top_hold = set(elig.head(RULES["n_hold"]).index)
    tgt = {}
    for sym, mv in held.items():                   # existing positions
        row = df.loc[sym] if sym in df.index else None
        hard_exit = row is None or not bool(row.above_200)          # rule 6, any day
        if hard_exit: tgt[sym] = 0.0; continue
        if not is_rebalance_day: tgt[sym] = mv; continue
        if sym not in top_hold: tgt[sym] = 0.0; continue             # rule 5 sell
        w = mv / nav
        tgt[sym] = RULES["weight"] * nav if (w > RULES["max_w"] or w < RULES["min_w"]) else mv
    if is_rebalance_day:
        slots = max(0, RULES["n_select"] - sum(1 for v in tgt.values() if v > 0))
        for sym in top_sel:
            if slots == 0: break
            if sym not in tgt: tgt[sym] = RULES["weight"] * nav; slots -= 1
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
    tgt = targets(df, nav, held, is_reb)
    orders = []
    for sym, dollars in tgt.items():
        cur = held.get(sym, 0.0); delta = dollars - cur
        if abs(delta) < 0.02 * nav and dollars > 0: continue      # ignore tiny drifts
        qty = int(abs(delta) // prices[sym])
        if qty == 0: continue
        orders.append(dict(date=today, symbol=sym, side="buy" if delta > 0 else "sell", qty=qty, ref_price=round(prices[sym], 2),
                           reason=f"RULES {RULES['version']}: {'rebalance' if is_reb else 'hard exit'} score={df.score.get(sym, float('nan')):.3f}"))
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

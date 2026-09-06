#!/usr/bin/env python3
"""Deterministic application of research/RULES.md to the paper ledger (no LLM).
Reuses the target logic from products/bot/bot.py. Usage: python paper/apply_rules.py [--dry-run] [--force-rebalance]"""
import sys, json, argparse, datetime as dt, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "products" / "bot")); sys.path.insert(0, str(ROOT / "paper"))
from bot import latest_scan, targets, band_state, unit_dollars, RULES, _norm
import ledger

ap = argparse.ArgumentParser(); ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--force-rebalance", action="store_true"); a = ap.parse_args()
p = ledger.load(); df = latest_scan(); df.index = df.index.str.replace(".", "-")   # back to yfinance symbols
today = dt.date.today(); is_reb = a.force_rebalance or today.weekday() == 4
prices = df.close.to_dict()
held = {t: q * prices[t] for t, q in p["positions"].items() if t in prices}
nav = p["cash"] + sum(held.values())
in_names, n_univ, asof, d200 = band_state(RULES["band"])
print(f"RULES v2: {len(in_names)}/{n_univ} names in-band as of {asof}; one position = ${unit_dollars(nav):,.0f} of ${nav:,.0f} NAV")
tgt = targets(df, nav, held, is_reb)
orders = []
for sym, dollars in tgt.items():
    if sym not in prices: print(f"skip {sym}: no price in the report"); continue
    cur = held.get(sym, 0.0); delta = dollars - cur
    if dollars > 0 and abs(delta) < RULES["min_trade"] * unit_dollars(nav): continue
    qty = int(abs(delta) // prices[sym]) if dollars > 0 else p["positions"][sym]
    if qty <= 0: continue
    orders.append(("SELL" if delta < 0 else "BUY", sym, qty,
                   f"RULES v2: {'rebalance' if dollars > 0 else 'exit'} "
                   f"band={'in' if _norm(sym) in in_names else 'out'} d200={d200.get(_norm(sym), float('nan')):+.1%}"))
if not orders: print("apply_rules: no trades"); sys.exit(0)
for side, sym, qty, reason in sorted(orders, key=lambda o: o[0] != "SELL"):
    print(("DRY " if a.dry_run else "") + f"{side} {qty} {sym} — {reason}")
    if not a.dry_run: ledger.trade(p, side, sym, qty, reason)
if not a.dry_run: ledger.save(p)

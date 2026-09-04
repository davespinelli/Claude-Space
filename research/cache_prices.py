#!/usr/bin/env python3
"""Cache 15y of adjusted daily closes for the universe to data/prices.csv so cloud
routines (no outbound network) can backtest offline."""
import json
from pathlib import Path
import yfinance as yf
import sys; sys.path.insert(0, str(Path(__file__).resolve().parent)); from scan import download_aligned
ROOT = Path(__file__).resolve().parents[1]
U = json.loads((ROOT / "research" / "universe.json").read_text())
T = sorted({t for g in U.values() for t in g})
px = download_aligned(T, start="2008-01-01")
(ROOT / "data").mkdir(exist_ok=True); px.round(4).to_csv(ROOT / "data" / "prices.csv")
print(f"cached {px.shape[0]} rows x {px.shape[1]} tickers to data/prices.csv")

import datetime as _dt
if _dt.date.today().weekday() == 4 or not (ROOT / "data" / "prices_broad.csv").exists():
    B = json.loads((ROOT / "research" / "universe_broad.json").read_text())
    pb = yf.download(B, start="2008-01-01", auto_adjust=True, progress=False)["Close"].dropna(how="all").ffill()
    pb.round(2).to_csv(ROOT / "data" / "prices_broad.csv"); print(f"cached broad {pb.shape}")

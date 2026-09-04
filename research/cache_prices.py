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

# Small-cap sub-$2B panel (485 names): refresh on Fridays or if the file is missing.
# Guarded so the daily pipeline never fails on it (485 downloads, several minutes).
try:
    _small = (ROOT / "data" / "prices_small.csv").exists() or (ROOT / "data" / "prices_small.csv.gz").exists()
    if _dt.date.today().weekday() == 4 or not _small:
        from cache_small import build as _build_small
        _ps, _vs, _ms = _build_small(verbose=True)
        print(f"cached small {_ps.shape} (survivorship: current constituents only)")
except Exception as _e:
    print(f"small-cap cache skipped ({type(_e).__name__}: {_e})")

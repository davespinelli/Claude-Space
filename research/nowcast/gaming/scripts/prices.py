#!/usr/bin/env python3
"""Daily prices from Yahoo (yfinance) for the casino companies and SPY.

Cached per ticker in cache/prices/<TICKER>.csv (re-run with --refresh to re-download).
Throttled (1.5 s between tickers), retried 4 times with back-off; an empty result is treated as
possible rate limiting and retried before the ticker is declared unavailable.

Output data/prices.csv.gz: ticker, date, close (split-adjusted, not dividend-adjusted, for market
cap), adj_close (split + dividend adjusted, for returns), volume.
Also data/price_availability.csv.gz: ticker, first/last date, n rows, or 'unavailable';
and data/splits.csv.gz (Yahoo split history, used to turn split-adjusted closes into raw prices).
NYNY on Yahoo from 2026-05 is an unrelated company re-using the symbol: not used.

Ticker mapping (Yahoo keeps one history per listed security):
  CZR  = Eldorado Resorts (ERI) history, renamed Caesars Entertainment Inc on 2020-07-21 (checked
         by price level in the run log); the old Caesars Entertainment Corp (CZR before 2020-07-20)
         has no separate Yahoo history.
  BALY = Yahoo's history starts only on 2024-12-06 (around the Standard General merger); the
         Twin River / Bally's history from the March 2019 listing to Dec 2024 is missing.
  GDEN = unavailable: Golden Entertainment deregistered in May 2026 after being taken private and
         Yahoo dropped the symbol.  ISLE, PNK, TPCA, DDE, NYNY (Empire Resorts), ERI, TRWH, MNTG,
         AFFI, CACQ, UWN, LACO: no Yahoo history.
"""
import sys, time
from pathlib import Path
import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "cache" / "prices"
DATA = ROOT / "data"

TICKERS = ["SPY", "PENN", "BYD", "CZR", "BALY", "GDEN", "RRR", "MCRI", "CNTY", "FLL", "CHDN", "MGM",
           "WYNN",
           # delisted / renamed: tried, usually absent from Yahoo
           "ISLE", "PNK", "TPCA", "DDE", "NYNY", "ERI", "TRWH", "MNTG", "AFFI", "CACQ", "UWN", "LACO"]


def fetch(t: str, refresh=False) -> pd.DataFrame | None:
    p = CACHE / f"{t}.csv"
    if p.exists() and not refresh:
        df = pd.read_csv(p, parse_dates=["date"])
        return df if len(df) else None
    for attempt in range(4):
        try:
            h = yf.Ticker(t).history(start="2011-01-01", end="2026-09-24", auto_adjust=False,
                                     actions=False)
        except Exception as e:
            print("  error", t, e)
            h = None
        if h is not None and len(h):
            h = h.reset_index()
            h["date"] = pd.to_datetime(h["Date"]).dt.tz_localize(None).dt.normalize()
            df = pd.DataFrame(dict(ticker=t, date=h["date"], close=h["Close"], adj_close=h["Adj Close"],
                                   volume=h["Volume"]))
            CACHE.mkdir(parents=True, exist_ok=True)
            df.to_csv(p, index=False)
            return df
        time.sleep(3 * (attempt + 1))  # empty: maybe rate limited, back off and retry
    CACHE.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(columns=["ticker", "date", "close", "adj_close", "volume"]).to_csv(p, index=False)
    return None


def main(refresh=False):
    frames, avail = [], []
    for t in TICKERS:
        df = fetch(t, refresh)
        if df is None:
            avail.append(dict(ticker=t, status="unavailable"))
            print(t, "unavailable")
        else:
            frames.append(df)
            avail.append(dict(ticker=t, status="ok", first=df.date.min().date(), last=df.date.max().date(),
                              n=len(df)))
            print(t, df.date.min().date(), df.date.max().date(), len(df))
        time.sleep(1.5)
    pd.concat(frames).to_csv(DATA / "prices.csv.gz", index=False)
    pd.DataFrame(avail).to_csv(DATA / "price_availability.csv.gz", index=False)
    # split history (Yahoo 'Close' is split-adjusted; market cap needs the raw price)
    rows = []
    for a in avail:
        if a["status"] != "ok" or a["ticker"] == "SPY":
            continue
        for d, v in yf.Ticker(a["ticker"]).splits.items():
            rows.append(dict(ticker=a["ticker"], date=pd.Timestamp(d).tz_localize(None).normalize().date(), ratio=v))
        time.sleep(1)
    pd.DataFrame(rows, columns=["ticker", "date", "ratio"]).to_csv(DATA / "splits.csv.gz", index=False)


if __name__ == "__main__":
    main("--refresh" in sys.argv)

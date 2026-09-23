#!/usr/bin/env python3
"""Historical consensus EPS estimates and reported EPS from Yahoo (yfinance get_earnings_dates),
for the 'versus analyst estimates' secondary test in PREREG.md.

Alpha Vantage (the source named in PREREG) needs a key that lives only in GitHub Actions secrets;
Yahoo's earnings calendar is a free alternative with history back to the early 2000s. Caveats: the
estimate is Yahoo's consensus (adjusted/"street" EPS basis) as currently stored, not a
point-in-time snapshot, and the reported figure is adjusted EPS, not GAAP.

Output data/eps_surprise.csv.gz: ticker, earn_datetime, earn_date, eps_est, eps_rep, surprise_pct.
Cached raw per ticker in cache/eps/<TICKER>.csv.
"""
import sys, time
from pathlib import Path
import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "cache" / "eps"
DATA = ROOT / "data"
TICKERS = ["PENN", "BYD", "CZR", "BALY", "RRR", "MCRI", "CNTY", "FLL", "CHDN", "MGM", "WYNN"]


def fetch(t, refresh=False):
    p = CACHE / f"{t}.csv"
    if p.exists() and not refresh:
        return pd.read_csv(p)
    for attempt in range(4):
        try:
            ed = yf.Ticker(t).get_earnings_dates(limit=100)
        except Exception as e:
            print("  err", t, e); ed = None
        if ed is not None and len(ed):
            ed = ed.reset_index()
            ed.columns = ["earn_datetime", "eps_est", "eps_rep", "surprise_pct"]
            ed["ticker"] = t
            CACHE.mkdir(parents=True, exist_ok=True)
            ed.to_csv(p, index=False)
            return ed
        time.sleep(4 * (attempt + 1))
    return None


def main(refresh=False):
    out = []
    for t in TICKERS:
        ed = fetch(t, refresh)
        if ed is None:
            print(t, "none"); continue
        ed["earn_date"] = pd.to_datetime(ed["earn_datetime"].astype(str).str[:10])
        out.append(ed)
        print(t, len(ed), ed["earn_date"].min().date(), ed["earn_date"].max().date())
        time.sleep(2)
    df = pd.concat(out, ignore_index=True)
    df[["ticker", "earn_datetime", "earn_date", "eps_est", "eps_rep", "surprise_pct"]].to_csv(
        DATA / "eps_surprise.csv.gz", index=False)


if __name__ == "__main__":
    main("--refresh" in sys.argv)

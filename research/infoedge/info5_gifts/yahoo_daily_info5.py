#!/usr/bin/env python3
"""INFO-5 step 3: daily Yahoo prices (yfinance, throttled) for every mapped ticker + IWM, SPY.

Stores long-format parquet chunks in cache/prices/ (gitignored): date, ticker, close (Yahoo's
split-adjusted close), adj (split + dividend adjusted), split (split ratio on that day).
Resumable: finished tickers are listed in cache/prices/status.csv and skipped on rerun.
Throttle: chunks of 40 tickers, 5 s pause. A Yahoo rate-limit error (detected from yfinance's log
records) -> wait 90 s, 180 s, ... and retry the chunk. A ticker that comes back empty is retried once
more on the next run (status "empty" -> "empty2", final).
"""
from __future__ import annotations

import logging
import sys
import time
from pathlib import Path

import pandas as pd
import yfinance as yf

HERE = Path(__file__).resolve().parent
CACHE = HERE / "cache"
PX = CACHE / "prices"
PX.mkdir(parents=True, exist_ok=True)
STATUS = PX / "status.csv"
START, END = "2005-01-01", "2026-09-26"
CHUNK, PAUSE = 40, 5.0


class RateLimited(Exception):
    pass


class _RLFlag(logging.Handler):
    """yfinance keeps per-call errors in a local context and only logs them, so rate limiting is
    detected from its log records."""
    hit = False

    def emit(self, record):
        m = record.getMessage()
        if "Rate limited" in m or "Too Many Requests" in m or "RateLimit" in m:
            _RLFlag.hit = True


logging.getLogger("yfinance").addHandler(_RLFlag())


def get(tickers):
    _RLFlag.hit = False
    df = yf.download(tickers, start=START, end=END, auto_adjust=False, actions=True,
                     progress=False, group_by="ticker", threads=True)
    if _RLFlag.hit:
        raise RateLimited("yfinance reported rate limiting")
    out = []
    for t in tickers:
        if df is None or df.empty or t not in df.columns.get_level_values(0):
            continue
        x = df[t].dropna(subset=["Close"])
        if x.empty:
            continue
        out.append(pd.DataFrame({"date": x.index.tz_localize(None) if x.index.tz else x.index,
                                 "ticker": t, "close": x["Close"].to_numpy(),
                                 "adj": x["Adj Close"].to_numpy(),
                                 "split": x["Stock Splits"].fillna(0).to_numpy()}))
    return pd.concat(out, ignore_index=True) if out else pd.DataFrame()


def main():
    m = pd.read_csv(CACHE / "ticker_map.csv", dtype=str, keep_default_na=False)
    tickers = sorted(set(m[m.source.isin(["sec_current", "symbol"])].ticker) | {"IWM", "SPY"})
    st0 = pd.read_csv(STATUS) if STATUS.exists() else pd.DataFrame(columns=["ticker", "status"])
    last = st0.drop_duplicates("ticker", keep="last").set_index("ticker").status
    # "empty" can be rate limiting (the first run hit Yahoo's limit), so each empty ticker
    # gets one more try; after that it is "empty2" and final.
    todo = [t for t in tickers if last.get(t) not in ("ok", "empty2")]
    retry = {t for t in todo if last.get(t) == "empty"}
    # never-tried tickers (incl. SPY / IWM) first, then the one retry of the empties
    todo = [t for t in todo if t not in retry] + [t for t in todo if t in retry]
    print(f"{len(tickers)} tickers, {len(todo)} to fetch", flush=True)
    n0 = len(list(PX.glob("chunk_*.parquet")))
    for i in range(0, len(todo), CHUNK):
        chunk = todo[i:i + CHUNK]
        for attempt in range(6):
            try:
                d = get(chunk)
            except Exception as e:  # rate limit / network error: back off and retry
                print(f"  {type(e).__name__}: {str(e)[:100]} -> wait", file=sys.stderr, flush=True)
                d = None
            if d is not None:      # no rate-limit record from yfinance: empty means empty
                break
            time.sleep(90 * (attempt + 1))
        if d is None:
            print("  giving up on chunk for now (rate limited)", file=sys.stderr, flush=True)
            continue
        got = set(d.ticker) if len(d) else set()
        if len(d):
            d.to_parquet(PX / f"chunk_{n0:04d}.parquet", index=False)
            n0 += 1
        st = pd.DataFrame({"ticker": chunk, "status": ["ok" if t in got else
                                                       ("empty2" if t in retry else "empty")
                                                       for t in chunk]})
        st.to_csv(STATUS, mode="a", header=not STATUS.exists(), index=False)
        print(f"  {i + len(chunk)}/{len(todo)}: {len(got)}/{len(chunk)} ok", flush=True)
        time.sleep(PAUSE)


if __name__ == "__main__":
    main()

"""
Monthly Yahoo prices for INFO-1.

Reads research/oplev/cache/prices/monthly_long.parquet (read-only) and fetches only the
tickers it lacks into cache/prices/monthly_long.parquet, same layout
(date, ticker, close = split-adjusted close, adj = split+dividend-adjusted close,
split = split ratio in that month). A sentinel (SPY) is added to every request: if it
comes back empty the call was rate limited and is retried instead of being recorded
as "no data".
"""
from __future__ import annotations

import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
OPLEV_PX = HERE.parents[1] / "oplev" / "cache" / "prices" / "monthly_long.parquet"
OPLEV_ST = HERE.parents[1] / "oplev" / "cache" / "prices" / "status.csv"
PX_DIR = HERE / "cache" / "prices"
PX_DIR.mkdir(parents=True, exist_ok=True)
PX_LONG = PX_DIR / "monthly_long.parquet"
PX_STATUS = PX_DIR / "status.csv"
PRICE_START = "2009-12-01"
SENTINEL = "SPY"


def _download(tickers):
    import yfinance as yf
    req = list(dict.fromkeys(list(tickers) + [SENTINEL]))
    try:
        df = yf.download(req, interval="1mo", start=PRICE_START, auto_adjust=False, actions=True,
                         progress=False, threads=True, group_by="column", multi_level_index=True)
    except Exception:  # noqa: BLE001
        return None, False
    ok = (df is not None and not df.empty and ("Adj Close", SENTINEL) in df.columns
          and df[("Adj Close", SENTINEL)].notna().sum() > 100)
    return df, ok


def ensure(tickers, chunk: int = 80) -> dict:
    """Make sure every ticker has been tried once (oplev cache or ours)."""
    have_op = set()
    if OPLEV_ST.exists():
        st = pd.read_csv(OPLEV_ST).drop_duplicates("ticker", keep="last")
        have_op = set(st.loc[st.status.isin(["ok", "nodata"]), "ticker"])
    mine = pd.read_csv(PX_STATUS) if PX_STATUS.exists() else pd.DataFrame(columns=["ticker", "status"])
    mine = mine.drop_duplicates("ticker", keep="last")
    done = have_op | set(mine.loc[mine.status.isin(["ok", "nodata"]), "ticker"])
    todo = [t for t in dict.fromkeys(tickers) if t and t not in done]
    have = pd.read_parquet(PX_LONG) if PX_LONG.exists() else pd.DataFrame(columns=["date", "ticker", "close", "adj", "split"])
    print(f"prices: {len(set(tickers))} tickers wanted, {len(todo)} to fetch from Yahoo", flush=True)
    new_f, new_s, rl = [], [], 0
    for i in range(0, len(todo), chunk):
        part = todo[i:i + chunk]
        for attempt in range(8):
            df, ok = _download(part)
            if not ok:
                rl += 1
                print(f"  chunk {i}: sentinel missing, backing off ({attempt+1})", flush=True)
                time.sleep(45 * (attempt + 1))
                continue
            got = []
            for t in part:
                if ("Adj Close", t) not in df.columns:
                    continue
                sub = pd.DataFrame({"close": df[("Close", t)] if ("Close", t) in df.columns else np.nan,
                                    "adj": df[("Adj Close", t)],
                                    "split": df[("Stock Splits", t)] if ("Stock Splits", t) in df.columns else 0.0})
                sub = sub.dropna(subset=["adj"])
                if len(sub):
                    sub = sub.reset_index().rename(columns={"Date": "date"})
                    sub["ticker"] = t
                    new_f.append(sub[["date", "ticker", "close", "adj", "split"]])
                    got.append(t)
            new_s += [(t, "ok") for t in got] + [(t, "nodata") for t in part if t not in got]
            break
        else:
            new_s += [(t, "failed") for t in part]
        print(f"  prices {min(i + chunk, len(todo))}/{len(todo)}", flush=True)
        time.sleep(1.5)
    if new_f:
        have = pd.concat([have] + new_f, ignore_index=True)
    have["date"] = pd.to_datetime(have["date"])
    have.to_parquet(PX_LONG, index=False)
    mine = pd.concat([mine, pd.DataFrame(new_s, columns=["ticker", "status"])], ignore_index=True)
    mine.to_csv(PX_STATUS, index=False)
    return {"requested": len(set(tickers)), "fetched_now": len(todo), "rate_limited_retries": rl,
            "new_status": pd.Series([s for _, s in new_s]).value_counts().to_dict() if new_s else {}}


def load(tickers=None) -> pd.DataFrame:
    """Long price table from oplev cache + ours (ours wins on overlap)."""
    parts = []
    if OPLEV_PX.exists():
        parts.append(pd.read_parquet(OPLEV_PX))
    if PX_LONG.exists():
        parts.append(pd.read_parquet(PX_LONG))
    px = pd.concat(parts, ignore_index=True)
    px["date"] = pd.to_datetime(px["date"]).dt.to_period("M").dt.to_timestamp()
    if tickers is not None:
        px = px[px.ticker.isin(set(tickers))]
    return px.drop_duplicates(["date", "ticker"], keep="last")


def monthly_returns(px: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """(total-return matrix from adj, split-adjusted close matrix). Month-start index; the
    value for month m is the return from the end of m-1 to the end of m."""
    adj = px.pivot(index="date", columns="ticker", values="adj").sort_index()
    close = px.pivot(index="date", columns="ticker", values="close").sort_index()
    adj = adj.where(adj > 0)
    close = close.where(close > 0)
    ret = adj / adj.shift(1) - 1
    return ret, close

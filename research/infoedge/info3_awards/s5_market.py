#!/usr/bin/env python3
"""Stage 5: daily prices (Yahoo) and SEC share counts for every mapped company.

Prices: yfinance daily, auto_adjust=False, actions=True, from 2009-06-01.
  close = split-adjusted close, adj = split+dividend adjusted close,
  split = Yahoo split ratio on that day. A sentinel symbol (SPY) rides along in
  every request; if it comes back empty the request is treated as rate limited
  and retried after a pause, instead of recording "no data".
  A formerly listed company's old symbol is not requested when SEC now assigns
  it to a different company (recycled symbol).
Shares: SEC XBRL companyconcept, dei:EntityCommonStockSharesOutstanding (cover
  page), us-gaap:CommonStockSharesOutstanding (balance sheet), and
  dei:EntityPublicFloat, each with its 'end' (as-of) and 'filed' dates.

Writes cache/prices/daily.parquet, cache/prices/status.csv,
cache/sec/concepts/*.json.gz and data/shares_long.parquet.
"""
from __future__ import annotations

import sys
import time

import numpy as np
import pandas as pd

from common import CACHE, DATA, log, sec_json

PX = CACHE / "prices"
PX.mkdir(exist_ok=True)
PX_LONG = PX / "daily.parquet"
PX_STATUS = PX / "status.csv"
SENTINEL = "SPY"
START = "2009-06-01"
BENCH = ["IWM", "SPY"]
CONCEPTS = [("dei", "EntityCommonStockSharesOutstanding", "shares"),
            ("us-gaap", "CommonStockSharesOutstanding", "shares"),
            ("dei", "EntityPublicFloat", "USD")]


def yf_ticker(t: str) -> str:
    return str(t).strip().upper().replace(".", "-")


def _dl(tickers):
    import yfinance as yf
    req = list(dict.fromkeys(tickers + [SENTINEL]))
    try:
        df = yf.download(req, start=START, interval="1d", auto_adjust=False, actions=True,
                         progress=False, threads=True, group_by="column", multi_level_index=True)
    except Exception:  # noqa: BLE001
        return None, False
    ok = (df is not None and not df.empty and ("Adj Close", SENTINEL) in df.columns
          and df[("Adj Close", SENTINEL)].notna().sum() > 3000)
    return df, ok


def fetch_prices(tickers: list[str], chunk: int = 40):
    have = pd.read_parquet(PX_LONG) if PX_LONG.exists() else pd.DataFrame(
        columns=["date", "ticker", "close", "adj", "split"])
    status = pd.read_csv(PX_STATUS) if PX_STATUS.exists() else pd.DataFrame(columns=["ticker", "status"])
    done = set(status.loc[status.status.isin(["ok", "nodata"]), "ticker"])
    status = status[status.ticker.isin(done)].drop_duplicates("ticker", keep="last")
    todo = [t for t in dict.fromkeys(tickers) if t not in done]
    log(f"prices: {len(tickers)} requested, {len(todo)} to fetch")
    new, new_st = [], []
    for i in range(0, len(todo), chunk):
        part = todo[i:i + chunk]
        for attempt in range(8):
            df, healthy = _dl(part)
            if not healthy:
                log(f"  chunk {i}: sentinel missing, backing off (attempt {attempt + 1})")
                time.sleep(45 * (attempt + 1))
                continue
            got = []
            for t in part:
                if ("Adj Close", t) not in df.columns:
                    continue
                sub = pd.DataFrame({"close": df[("Close", t)], "adj": df[("Adj Close", t)],
                                    "split": df[("Stock Splits", t)] if ("Stock Splits", t) in df.columns else 0.0})
                sub = sub.dropna(subset=["adj"])
                if len(sub):
                    sub = sub.reset_index().rename(columns={"Date": "date"})
                    sub["ticker"] = t
                    new.append(sub[["date", "ticker", "close", "adj", "split"]])
                    got.append(t)
            new_st += [(t, "ok" if t in got else "nodata") for t in part]
            break
        else:
            new_st += [(t, "failed") for t in part]
        time.sleep(2.0)
        if (i // chunk) % 10 == 9 or i + chunk >= len(todo):
            if new:
                have = pd.concat([have] + new, ignore_index=True)
                new = []
            status = pd.concat([status, pd.DataFrame(new_st, columns=["ticker", "status"])], ignore_index=True)
            new_st = []
            have["date"] = pd.to_datetime(have["date"])
            have.to_parquet(PX_LONG, index=False)
            status.to_csv(PX_STATUS, index=False)
            log(f"  prices {min(i + chunk, len(todo))}/{len(todo)}")
    return status.status.value_counts().to_dict()


def fetch_concepts(ciks: list[int]) -> pd.DataFrame:
    rows = []
    for j, cik in enumerate(ciks, 1):
        for tax, tag, unit in CONCEPTS:
            js = sec_json(f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik:010d}/{tax}/{tag}.json",
                          CACHE / "sec" / "concepts" / f"{cik}_{tag}.json.gz")
            if not isinstance(js, dict):
                continue
            for u, vals in (js.get("units") or {}).items():
                if u != unit:
                    continue
                for v in vals:
                    rows.append(dict(cik=cik, tag=tag, end=v.get("end"), filed=v.get("filed"),
                                     val=v.get("val"), form=v.get("form"), accn=v.get("accn")))
        if j % 100 == 0:
            log(f"  concepts {j}/{len(ciks)}")
    S = pd.DataFrame(rows)
    if len(S):
        S["end"] = pd.to_datetime(S.end, errors="coerce")
        S["filed"] = pd.to_datetime(S.filed, errors="coerce")
        S["val"] = pd.to_numeric(S.val, errors="coerce")
        S = S.dropna(subset=["end", "filed", "val"]).drop_duplicates(["cik", "tag", "end", "filed", "val"])
    return S


def main():
    M = pd.read_parquet(CACHE / "mapped.parquet", columns=["cik", "ticker", "listing", "in_universe", "alive",
                                                          "amount", "action_date"])
    M = M[M.in_universe & M.alive & (M.amount > 0) & (M.action_date >= "2009-10-01")]
    # a company whose largest award is below 2% of its smallest reported public
    # float (XBRL cover pages 2009-2025) cannot pass the 2% screen (market value
    # >= float), so it is not priced; the list is saved for stage 6
    mx = M.groupby("cik").amount.max()
    fm = pd.read_csv(DATA / "universe_scope.csv").set_index("cik").float_min.reindex(mx.index)
    possible = mx.index[fm.isna() | (mx >= 0.02 * fm)]
    pd.DataFrame({"cik": possible}).to_csv(DATA / "possible_ciks.csv", index=False)
    log(f"{len(mx)} companies with mapped awards; {len(possible)} could reach 2% of market cap")
    M = M[M.cik.isin(possible)].drop_duplicates("cik")
    U = pd.read_csv(DATA / "universe_all.csv").set_index("cik")
    # symbols SEC currently assigns (any exchange, incl. OTC), to catch recycled symbols
    import gzip, json  # noqa: E401
    with gzip.open(CACHE / "sec" / "company_tickers_exchange.json.gz", "rt") as fh:
        ex = json.loads(fh.read())
    holder = {}
    for cik, name, tk, exch in ex["data"]:
        holder.setdefault(yf_ticker(tk), set()).add(int(cik))
    req, skipped = [], []
    for r in M.itertuples():
        if not isinstance(r.ticker, str) or not r.ticker:
            continue
        t = yf_ticker(r.ticker)
        if r.listing == "former" and t in holder and int(r.cik) not in holder[t]:
            skipped.append((int(r.cik), t))
            continue
        req.append(t)
    pd.DataFrame(skipped, columns=["cik", "ticker"]).to_csv(DATA / "recycled_symbols_skipped.csv", index=False)
    log(f"{len(req)} tickers to price, {len(skipped)} recycled former symbols skipped")
    if "--no-prices" not in sys.argv:
        st = fetch_prices(BENCH + sorted(set(req)))
        log(f"price status: {st}")
    if "--no-shares" not in sys.argv:
        S = fetch_concepts(sorted(int(c) for c in M.cik))
        # multi-class companies tag cover-page counts by class, which the concept API
        # omits: fall back to weighted-average basic shares (research/oplev's 4th source)
        need = sorted(int(c) for c in M.cik)     # all: class-tagged years leave gaps in any company
        rows = []
        for cik in need:
            js = sec_json(f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik:010d}/us-gaap/"
                          "WeightedAverageNumberOfSharesOutstandingBasic.json",
                          CACHE / "sec" / "concepts" / f"{cik}_WANSO.json.gz")
            if not isinstance(js, dict):
                continue
            for v in (js.get("units") or {}).get("shares", []):
                rows.append(dict(cik=cik, tag="WeightedAverageNumberOfSharesOutstandingBasic", end=v.get("end"),
                                 filed=v.get("filed"), val=v.get("val"), form=v.get("form"), accn=v.get("accn")))
        if rows:
            W = pd.DataFrame(rows)
            W["end"] = pd.to_datetime(W.end, errors="coerce")
            W["filed"] = pd.to_datetime(W.filed, errors="coerce")
            W["val"] = pd.to_numeric(W.val, errors="coerce")
            S = pd.concat([S, W.dropna(subset=["end", "filed", "val"])], ignore_index=True)
        log(f"weighted-average share fallback fetched for {len(need)} companies")
        S.to_parquet(DATA / "shares_long.parquet", index=False)
        log(f"share/float facts: {len(S)} rows for {S.cik.nunique()} CIKs")


if __name__ == "__main__":
    main()

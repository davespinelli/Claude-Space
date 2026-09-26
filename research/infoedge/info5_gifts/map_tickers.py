#!/usr/bin/env python3
"""INFO-5 step 2: map issuer CIKs to Yahoo tickers.

Two sets of CIKs need tickers:
  * event issuers: every issuer with a code-G disposal on a Form 4 / 4/A filed by an officer or
    director (before the $1M / 1% filter, which needs a price);
  * benchmark universe: every issuer that appears in the Form 4/5 data sets 2006-2026 AND is on
    the SEC's current NYSE / Nasdaq / CBOE ticker list (company_tickers_exchange.json).

Mapping rules (care for reused tickers):
  1. CIK on the SEC's current ticker list -> that ticker ("sec_current"). If the CIK has several
     (share classes), take the one its Form 4s use most as ISSUERTRADINGSYMBOL, else the first.
  2. CIK not on the current list (delisted, acquired, deregistered) -> the ISSUERTRADINGSYMBOL
     it used most in its last two filing years ("symbol"), UNLESS that symbol is now assigned to a
     different CIK on the current list (a reused ticker -> no mapping, reason "reused").
  3. Every mapping is later checked against the insiders' own open-market prices (validate step
     in event_study.py); "symbol" mappings must pass that check to be used at all.

Writes cache/ticker_map.csv and cache/universe_ciks.csv.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "cache"
BAD_SYM = {"", "NONE", "NA", "N/A", "NOTAPPLICABLE", "NOT-APPLICABLE", "NOSYMBOL", "N-A", "NULL",
           "TBD", "PRIVATE", "NOTLISTED"}


def norm(s) -> str:
    if not isinstance(s, str):
        return ""
    s = s.strip().upper()
    if ":" in s:
        s = s.split(":")[-1]
    s = s.replace(".", "-").replace(" ", "-").replace("/", "-")
    return s


def main():
    d = json.load(open(CACHE / "company_tickers_exchange.json"))
    ct = pd.DataFrame(d["data"], columns=d["fields"])
    ct["cik10"] = ct.cik.map(lambda c: f"{int(c):010d}")
    ct["ticker"] = ct.ticker.map(norm)
    ct["rank"] = range(len(ct))
    owner_of = ct.groupby("ticker").cik10.first().to_dict()

    sym = pd.read_parquet(CACHE / "symbols.parquet")
    sym["sym"] = sym.ISSUERTRADINGSYMBOL.map(norm)

    g = pd.read_parquet(CACHE / "gift_lines.parquet")
    o = pd.read_parquet(CACHE / "owners.parquet")
    od = set(o[o.RPTOWNER_RELATIONSHIP.fillna("").str.contains("Director|Officer")].ACCESSION_NUMBER)
    ev = g[g.DOCUMENT_TYPE.isin(["4", "4/A"]) & (g.TRANS_ACQUIRED_DISP_CD == "D")
           & g.ACCESSION_NUMBER.isin(od)]
    event_ciks = set(ev.ISSUERCIK)

    listed = ct[ct.exchange.isin(["NYSE", "Nasdaq", "CBOE"])]
    filers = set(sym.ISSUERCIK)
    bench_ciks = set(listed.cik10) & filers

    rows = []
    for cik in sorted(event_ciks | bench_ciks):
        s = sym[sym.ISSUERCIK == cik] if cik in event_ciks else None
        cur = ct[ct.cik10 == cik]
        if len(cur):
            tk = cur.sort_values("rank").ticker.tolist()
            pick = tk[0]
            if s is not None and len(tk) > 1:
                used = s.groupby("sym").n.sum().sort_values(ascending=False)
                for u in used.index:
                    if u in tk:
                        pick = u
                        break
            rows.append((cik, pick, "sec_current", cur.exchange.iloc[0], "", cik in event_ciks,
                         cik in bench_ciks))
            continue
        # not on the current list: most-used symbol in its last two filing years
        s = s[~s.sym.isin(BAD_SYM) & s.sym.str.fullmatch(r"[A-Z]{1,5}(-[A-Z]{1,2})?")]
        if s.empty:
            rows.append((cik, "", "none", "", "no_symbol", True, False))
            continue
        last = s.year.max()
        u = (s[s.year >= last - 1].groupby("sym").n.sum().sort_values(ascending=False).index[0])
        if u in owner_of and owner_of[u] != cik:
            rows.append((cik, u, "reused", "", f"now {owner_of[u]}", True, False))
            continue
        rows.append((cik, u, "symbol", "", "", True, False))
    m = pd.DataFrame(rows, columns=["cik", "ticker", "source", "exchange", "note", "event", "bench"])
    m.to_csv(CACHE / "ticker_map.csv", index=False)
    print(m.groupby(["event", "source"]).size())
    print("tickers to download:", m[m.source.isin(["sec_current", "symbol"])].ticker.nunique())


if __name__ == "__main__":
    main()

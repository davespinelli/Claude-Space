"""CIK -> Yahoo ticker for every 10-Q/10-K filer in the notes data sets.
Order of preference: SEC company_tickers.json (current), then the dei:TradingSymbol on the company's
most recent filing (common stock only). Writes data/tickers.csv."""
import json
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sec

REPO = sec.ROOT.parents[2]
BAD_CLASS = re.compile(r"warrant|note|debenture|preferred|pref|unit|right|depositary|bond|senior|subordinat|trust"
                       r"|series[a-z]*preferred|percent|pct|due", re.I)


def yahoo(sym: str) -> str:
    return sym.strip().upper().replace(".", "-").replace("/", "-").replace(" ", "")


def build():
    f = pd.read_csv(sec.ROOT / "data" / "filings.csv.gz", low_memory=False)
    ciks = f.groupby("cik").agg(company=("name", "last"), last_filed=("filed", "max"), sic=("sic", "last")).reset_index()
    # SEC current map (refresh once into our cache, fall back to the repo copy)
    try:
        ct = sec.get_json("https://www.sec.gov/files/company_tickers.json", "misc")
    except Exception:
        ct = json.loads((REPO / "data" / "sec_cache" / "company_tickers.json").read_text())
    cur = {}
    for v in ct.values():
        cur.setdefault(int(v["cik_str"]), v["ticker"])
    # dei trading symbols
    d = pd.read_parquet(sec.CACHE / "dei_all.parquet")
    ts = d[(d.tag == "TradingSymbol") & (d.value.str.len().between(1, 7))].copy()
    ts = ts[~ts.segments.str.contains(BAD_CLASS)]
    ts = ts.merge(f[["adsh", "cik", "filed"]], on="adsh")
    ts["pri"] = (ts.segments == "").astype(int) * 2 + ts.segments.str.contains("Common", case=False).astype(int)
    ts = ts.sort_values(["cik", "filed", "pri"]).groupby("cik").tail(1)
    dei_sym = dict(zip(ts.cik, ts.value))
    ciks["ticker_sec"] = ciks.cik.map(cur)
    ciks["ticker_dei"] = ciks.cik.map(dei_sym)
    ciks["ticker"] = ciks.ticker_sec.fillna(ciks.ticker_dei)
    ciks["yahoo"] = ciks.ticker.map(lambda s: yahoo(s) if isinstance(s, str) else None)
    alt = ciks.ticker_dei.map(lambda s: yahoo(s) if isinstance(s, str) else None)
    ciks["yahoo_alt"] = alt.where(alt != ciks.yahoo)
    ciks.to_csv(sec.ROOT / "data" / "tickers.csv", index=False)
    return ciks


if __name__ == "__main__":
    c = build()
    print(len(c), "ciks;", c.yahoo.notna().sum(), "with a ticker;", c.yahoo_alt.notna().sum(), "with an alternative")

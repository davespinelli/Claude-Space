#!/usr/bin/env python3
"""Fetch 8-K Item 2.02 (Results of Operations) filing dates from SEC EDGAR for the
broad universe, and cache them to data/earnings_dates.csv.

Rate-limited to <=8 req/s per SEC fair-access policy. Idempotent: re-running rebuilds
the cache from scratch (deterministic given EDGAR's contents).
"""
import json, time, sys
from pathlib import Path
import requests, pandas as pd

ROOT = Path(__file__).resolve().parents[1]
UA = {"User-Agent": "ClaudeSpace research dspinjr@gmail.com"}
OUT = ROOT / "data" / "earnings_dates.csv"
SINCE = "2012-01-01"

# company_tickers.json maps a few tickers to a NEWLY re-registered CIK whose submissions
# history starts only at the reorganisation, losing a decade of 8-Ks. Add the predecessor
# CIK by hand (verified against EDGAR company search).
EXTRA_CIKS = {"XOM": [34088], "BLK": [1364742]}

_last = [0.0]
def get(url):
    dt = time.time() - _last[0]
    if dt < 0.13: time.sleep(0.13 - dt)          # <= ~7.7 req/s
    for attempt in range(4):
        try:
            r = requests.get(url, headers=UA, timeout=30)
            _last[0] = time.time()
            if r.status_code == 200: return r.json()
            if r.status_code == 404: return None
            time.sleep(1.5 * (attempt + 1))
        except Exception:
            time.sleep(1.5 * (attempt + 1))
        _last[0] = time.time()
    return None

def rows_from(f):
    """f is a dict-of-lists (recent) or the shard file format; both share column names."""
    out = []
    forms, items = f.get("form", []), f.get("items", [])
    dates, accs = f.get("filingDate", []), f.get("accessionNumber", [])
    for i in range(len(forms)):
        if not forms[i].startswith("8-K"): continue
        it = items[i] if i < len(items) else ""
        if "2.02" not in (it or ""): continue
        if dates[i] < SINCE: continue
        out.append((dates[i], accs[i]))
    return out

def main():
    tickers = json.loads((ROOT / "research" / "universe_broad.json").read_text())
    print(f"universe: {len(tickers)} tickers")
    cmap = get("https://www.sec.gov/files/company_tickers.json")
    t2cik = {}
    for v in cmap.values():
        t2cik.setdefault(v["ticker"].upper(), int(v["cik_str"]))
    # yfinance uses '-' where EDGAR uses '.' for share classes
    def cik_for(t):
        for k in (t.upper(), t.upper().replace("-", "."), t.upper().replace("-", "")):
            if k in t2cik: return t2cik[k]
        return None

    recs, missing = [], []
    for n, t in enumerate(tickers, 1):
        ciks = [c for c in ([cik_for(t)] + EXTRA_CIKS.get(t.upper(), [])) if c]
        if not ciks:
            missing.append(t); continue
        found = []
        for cik in ciks:
            sub = get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json")
            if sub is None: continue
            found += rows_from(sub.get("filings", {}).get("recent", {}))
            for shard in sub.get("filings", {}).get("files", []):
                nm = shard.get("name")
                if not nm: continue
                if shard.get("filingTo", "9999") < SINCE: continue   # shard entirely pre-2012
                sh = get(f"https://data.sec.gov/submissions/{nm}")
                if sh: found += rows_from(sh)
        if not found: missing.append(t)
        for d, a in found:
            recs.append((t, d, a))
        print(f"[{n:3d}/{len(tickers)}] {t:6s} CIK {'+'.join(map(str,ciks)):>18s}  8-K/2.02 since {SINCE}: {len(found)}", flush=True)

    df = pd.DataFrame(recs, columns=["ticker", "filing_date", "accession"])
    df = df.drop_duplicates().sort_values(["ticker", "filing_date"]).reset_index(drop=True)
    OUT.parent.mkdir(exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"\nwrote {OUT} : {len(df)} filings, {df.ticker.nunique()} tickers")
    print(f"no CIK / no 8-K-2.02 data ({len(missing)}): {sorted(missing)}")

if __name__ == "__main__":
    main()

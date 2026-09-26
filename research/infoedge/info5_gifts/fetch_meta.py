#!/usr/bin/env python3
"""INFO-5 step 4: shares outstanding (for market cap) and SIC codes (for industry).

  * Shares: SEC XBRL frames API, dei:EntityCommonStockSharesOutstanding (cover-page shares) and
    us-gaap:CommonStockSharesOutstanding (balance-sheet shares), every calendar quarter instant
    CY2009Q1I..CY2026Q2I. research/oplev/cache/frames is read first (read-only); anything not there
    is fetched into cache/frames/.
  * SIC: research/oplev/cache/subs.parquet and research/oplev/cache/submissions/ first (read-only),
    then data.sec.gov/submissions/CIK##########.json for the rest -> cache/sic.csv.

SEC: <= 2 requests a second (0.6 s apart), User-Agent "Claude Space research dspinjr@gmail.com".
Writes cache/shares.parquet (cik, end, val, concept) and cache/sic.csv (cik, sic, name).
"""
from __future__ import annotations

import gzip
import json
import time
from pathlib import Path

import pandas as pd
import requests

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
CACHE = HERE / "cache"
FR = CACHE / "frames"
SUBS = CACHE / "submissions"
OPL = REPO / "research" / "oplev" / "cache"
for d in (FR, SUBS):
    d.mkdir(parents=True, exist_ok=True)
UA = "Claude Space research dspinjr@gmail.com"
GAP = 0.6
S = requests.Session()
S.headers.update({"User-Agent": UA, "Accept-Encoding": "gzip, deflate"})
_last = [0.0]


def sec_get(url):
    for attempt in range(4):
        w = GAP - (time.time() - _last[0])
        if w > 0:
            time.sleep(w)
        _last[0] = time.time()
        try:
            r = S.get(url, timeout=60)
        except requests.RequestException:
            time.sleep(5 * (attempt + 1))
            continue
        if r.status_code == 200:
            return r.json()
        if r.status_code == 404:
            return None
        time.sleep(5 * (attempt + 1))
    return None


def frames():
    rows = []
    for tax, tag in (("dei", "EntityCommonStockSharesOutstanding"),
                     ("us-gaap", "CommonStockSharesOutstanding")):
        for y in range(2009, 2027):
            for q in range(1, 5):
                if (y, q) > (2026, 2):
                    break
                name = f"{tax}_{tag}_shares_CY{y}Q{q}I.json.gz"
                d = None
                for p in (OPL / "frames" / name, FR / name):
                    if p.exists():
                        d = json.load(gzip.open(p))
                        break
                if d is None:
                    d = sec_get(f"https://data.sec.gov/api/xbrl/frames/{tax}/{tag}/shares/CY{y}Q{q}I.json")
                    if d is None:
                        print("  no frame", name, flush=True)
                        continue
                    with gzip.open(FR / name, "wt") as fh:
                        json.dump(d, fh)
                for r in d["data"]:
                    rows.append((f"{int(r['cik']):010d}", r["end"], r["val"], tag))
    sh = pd.DataFrame(rows, columns=["cik", "end", "val", "concept"])
    sh["end"] = pd.to_datetime(sh["end"])
    sh = sh[sh.val > 0].drop_duplicates()
    sh.to_parquet(CACHE / "shares.parquet", index=False)
    print("shares rows", len(sh), "ciks", sh.cik.nunique(), flush=True)


def sic():
    m = pd.read_csv(CACHE / "ticker_map.csv", dtype=str, keep_default_na=False)
    need = set(m[m.source.isin(["sec_current", "symbol"])].cik)
    out = {}
    sp = pd.read_parquet(OPL / "subs.parquet")
    for cik, r in sp.iterrows():
        k = f"{int(cik):010d}"
        if k in need and pd.notna(r.sic):
            out[k] = (int(r.sic), r["name"])
    for k in sorted(need - set(out)):
        for p in (OPL / "submissions" / f"CIK{k}.json.gz", SUBS / f"CIK{k}.json.gz"):
            if p.exists():
                d = json.load(gzip.open(p))
                break
        else:
            d = sec_get(f"https://data.sec.gov/submissions/CIK{k}.json")
            if d is None:
                continue
            d = {kk: d.get(kk) for kk in ("cik", "sic", "sicDescription", "name", "tickers",
                                          "exchanges", "entityType")}
            with gzip.open(SUBS / f"CIK{k}.json.gz", "wt") as fh:
                json.dump(d, fh)
        try:
            out[k] = (int(d.get("sic")), d.get("name"))
        except (TypeError, ValueError):
            pass
    pd.DataFrame([(k, v[0], v[1]) for k, v in out.items()], columns=["cik", "sic", "name"]) \
        .to_csv(CACHE / "sic.csv", index=False)
    print("sic for", len(out), "of", len(need), flush=True)


if __name__ == "__main__":
    frames()
    sic()

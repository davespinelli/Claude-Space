#!/usr/bin/env python3
"""
H5/H6 data step 1: SEC companyfacts for every candidate company.

Candidates = every CIK in research/oplev/cache/subs.parquet (the annual study's
set: filed revenue > $10M and assets > 0 in some fiscal year 2010-2024) whose
current SIC is not financial (6000-6999) or utility (4900-4999) and that is not
a foreign private issuer. Same filters as H1-H3.

For each CIK the companyfacts JSON is fetched (at most 7.5 requests a second,
descriptive User-Agent), or read from research/oplev/cache/companyfacts/ when the
annual study already cached it (read-only). Only the tags this study needs are
kept, as one compact parquet per CIK in quarterly/cache/cf/, plus the full list
of filings (accession, form, filed date) seen anywhere in the company's facts.

Run: .venv/bin/python research/oplev/quarterly/fetch_facts.py
"""
from __future__ import annotations

import gzip
import json
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd
import requests

HERE = Path(__file__).resolve().parent
OPLEV = HERE.parent
CACHE = HERE / "cache"
CF = CACHE / "cf"
CF.mkdir(parents=True, exist_ok=True)
OLD_CF = OPLEV / "cache" / "companyfacts"      # read-only

UA = "ClaudeSpace research (oplev quarterly study) dspinjr@gmail.com"
HEADERS = {"User-Agent": UA, "Accept-Encoding": "gzip, deflate", "Host": "data.sec.gov"}
MIN_INTERVAL = 1.0 / 7.5

TAGS = {
    "us-gaap": ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet",
                "RevenueFromContractWithCustomerIncludingAssessedTax", "SalesRevenueGoodsNet",
                "SalesRevenueServicesNet", "OperatingIncomeLoss", "Assets",
                "RevenueRemainingPerformanceObligation", "CommonStockSharesOutstanding",
                "WeightedAverageNumberOfSharesOutstandingBasic"],
    "dei": ["EntityCommonStockSharesOutstanding", "EntityPublicFloat"],
}

_lock = threading.Lock()
_last = [0.0]
_sess = requests.Session()


def throttle():
    with _lock:
        w = MIN_INTERVAL - (time.time() - _last[0])
        if w > 0:
            time.sleep(w)
        _last[0] = time.time()


def fetch(cik: int):
    old = OLD_CF / f"CIK{cik:010d}.json.gz"
    if old.exists():
        with gzip.open(old, "rt") as fh:
            return json.loads(fh.read()), "old_cache"
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
    for attempt in range(6):
        try:
            throttle()
            r = _sess.get(url, headers=HEADERS, timeout=120)
            if r.status_code == 404:
                return None, "404"
            if r.status_code in (403, 429, 500, 502, 503, 504):
                raise RuntimeError(f"HTTP {r.status_code}")
            r.raise_for_status()
            return r.json(), "fetched"
        except Exception as exc:  # noqa: BLE001
            if attempt == 5:
                return None, f"failed: {exc}"
            time.sleep(3.0 * (attempt + 1) ** 2)
    return None, "failed"


def extract(js: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    filings = {}
    facts = js.get("facts", {})
    for tax, tags in facts.items():
        for tag, body in tags.items():
            keep = tag in TAGS.get(tax, [])
            for unit, lst in body.get("units", {}).items():
                for u in lst:
                    a = u.get("accn")
                    if a and a not in filings:
                        filings[a] = (u.get("form"), u.get("filed"))
                    if keep:
                        rows.append((tax, tag, unit, u.get("start"), u.get("end"), u.get("val"), a,
                                     u.get("fy"), u.get("fp"), u.get("form"), u.get("filed"), u.get("frame")))
    f = pd.DataFrame(rows, columns=["tax", "tag", "unit", "start", "end", "val", "accn", "fy", "fp",
                                    "form", "filed", "frame"])
    f["val"] = pd.to_numeric(f["val"], errors="coerce").astype("float64")
    f["fy"] = pd.to_numeric(f["fy"], errors="coerce").astype("float64")
    for c in ("tax", "tag", "unit", "start", "end", "accn", "fp", "form", "filed", "frame"):
        f[c] = f[c].astype("string")
    fl = pd.DataFrame([(a, fm, fd) for a, (fm, fd) in filings.items()], columns=["accn", "form", "filed"])
    fl = fl.astype("string")
    return f, fl


def one(cik: int):
    out = CF / f"CIK{cik:010d}.parquet"
    outf = CF / f"CIK{cik:010d}.filings.parquet"
    if out.exists() and outf.exists():
        return cik, "cached"
    js, status = fetch(cik)
    if js is None:
        return cik, status
    f, fl = extract(js)
    f.to_parquet(out, index=False)
    fl.to_parquet(outf, index=False)
    return cik, status


def main():
    subs = pd.read_parquet(OPLEV / "cache" / "subs.parquet")
    ok = subs[subs.sic.notna() & ~subs.sic.between(6000, 6999) & ~subs.sic.between(4900, 4999)]
    ok = ok[~((ok.n_20f > 0) & (ok.n_10k == 0))]
    ciks = sorted(int(c) for c in ok.index)
    print(f"{len(ciks)} candidate CIKs", flush=True)
    stat = {}
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=6) as ex:
        for i, (cik, s) in enumerate(ex.map(one, ciks), 1):
            key = s if not s.startswith("failed") else "failed"
            stat[key] = stat.get(key, 0) + 1
            if s.startswith("failed"):
                print(f"  ! CIK {cik}: {s}", flush=True)
            if i % 250 == 0:
                print(f"  {i}/{len(ciks)} {stat} {time.time()-t0:.0f}s", flush=True)
    print(f"done {stat}", flush=True)
    (CACHE / "fetch_log.json").write_text(json.dumps({"n_ciks": len(ciks), "status": stat}, indent=1))


if __name__ == "__main__":
    sys.exit(main())

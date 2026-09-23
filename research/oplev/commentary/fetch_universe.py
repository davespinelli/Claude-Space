#!/usr/bin/env python
"""
Denominator for the descriptive stats: how many distinct companies (CIKs) filed a 10-K,
10-Q or 8-K in each calendar year / quarter (plus a CIK x quarter presence table),
from the EDGAR quarterly master index
(https://www.sec.gov/Archives/edgar/full-index/YYYY/QTRn/master.gz). Cached under
cache/full-index/. Writes filer_universe_by_year.csv, filer_universe_by_quarter.csv and
filer_presence_by_cik_quarter.csv.gz (cik, cal_quarter, n_10k, n_10q, n_8k).

Caveat: the universe includes blank-check SPACs, which ballooned in 2021-2022 and file
10-Ks/10-Qs but never talk about operating leverage, so share-of-filers dips in those years.
"""
from __future__ import annotations

import gzip
import io
import time
from pathlib import Path

import pandas as pd
import requests

HERE = Path(__file__).resolve().parent
CACHE = HERE / "cache" / "full-index"
UA = "ClaudeSpace research dspinjr@gmail.com"
FIRST, LAST = (2010, 1), (2026, 3)
ROOT = {"10-K": "10-K", "10-K405": "10-K", "10-KT": "10-K", "10-Q": "10-Q", "10-QT": "10-Q", "8-K": "8-K"}


def get_master(y: int, q: int) -> bytes:
    p = CACHE / f"{y}_QTR{q}_master.gz"
    if p.exists() and p.stat().st_size > 0:
        return p.read_bytes()
    url = f"https://www.sec.gov/Archives/edgar/full-index/{y}/QTR{q}/master.gz"
    for attempt in range(6):
        r = requests.get(url, headers={"User-Agent": UA}, timeout=120)
        if r.status_code == 200:
            CACHE.mkdir(parents=True, exist_ok=True)
            p.write_bytes(r.content)
            time.sleep(0.5)
            return r.content
        time.sleep(2 ** attempt)
    raise RuntimeError(f"{url}: HTTP {r.status_code}")


def main():
    frames = []
    y, q = FIRST
    while (y, q) <= LAST:
        raw = gzip.decompress(get_master(y, q)).decode("latin-1")
        lines = raw.splitlines()
        start = next(i for i, l in enumerate(lines) if l.startswith("-----")) + 1
        df = pd.read_csv(io.StringIO("\n".join(lines[start:])), sep="|", header=None,
                         names=["cik", "name", "form", "date", "path"], dtype=str)
        df = df[df.form.isin(ROOT)]
        df["root"] = df.form.map(ROOT)
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])
        frames.append(df[["cik", "root", "date"]])
        print(y, q, len(df), flush=True)
        q += 1
        if q == 5:
            y, q = y + 1, 1
    u = pd.concat(frames)
    u["year"] = u.date.dt.year
    u["cal_quarter"] = u.year.astype(str) + "Q" + u.date.dt.quarter.astype(str)
    u["cik"] = u.cik.astype(int)
    pres = (u.groupby(["cik", "cal_quarter", "root"]).size().unstack("root").fillna(0).astype(int)
            .rename(columns={"10-K": "n_10k", "10-Q": "n_10q", "8-K": "n_8k"}).reset_index())
    pres.to_csv(HERE / "filer_presence_by_cik_quarter.csv.gz", index=False)
    print(f"filer_presence_by_cik_quarter.csv.gz: {len(pres):,} rows, {pres.cik.nunique():,} CIKs")
    for key, fname in [("year", "filer_universe_by_year.csv"), ("cal_quarter", "filer_universe_by_quarter.csv")]:
        out = pd.DataFrame({
            "n_ciks_10k": u[u.root == "10-K"].groupby(key).cik.nunique(),
            "n_ciks_10q": u[u.root == "10-Q"].groupby(key).cik.nunique(),
            "n_ciks_10k_or_10q": u[u.root != "8-K"].groupby(key).cik.nunique(),
            "n_ciks_8k": u[u.root == "8-K"].groupby(key).cik.nunique(),
            "n_ciks_any": u.groupby(key).cik.nunique(),
            "n_filings_10k": u[u.root == "10-K"].groupby(key).size(),
            "n_filings_10q": u[u.root == "10-Q"].groupby(key).size(),
            "n_filings_8k": u[u.root == "8-K"].groupby(key).size(),
        }).fillna(0).astype(int)
        out.index.name = key
        out.to_csv(HERE / fname)
        print(out.to_string() if key == "year" else f"{fname}: {len(out)} rows")


if __name__ == "__main__":
    main()

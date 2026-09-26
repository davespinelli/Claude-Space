#!/usr/bin/env python3
"""INFO-5: fetch the SEC Form 3/4/5 quarterly data sets missing from data/sec_cache/form345/.

The shared cache holds 2012q1..2026q1. The pre-registration says "from 2006 on", so this pulls
2006q1..2011q4 plus any newer quarter (2026q2) into research/infoedge/info5_gifts/cache/form345/
(gitignored). SEC rate limit for this test: <= 2 requests a second (sequential, 0.6 s apart).
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SHARED = REPO / "data" / "sec_cache" / "form345"
OUT = HERE / "cache" / "form345"
OUT.mkdir(parents=True, exist_ok=True)
UA = "Claude Space research dspinjr@gmail.com"
BASES = ["https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/",
         # 2026q2 is published under a different folder (found on the SEC page link)
         "https://www.sec.gov/files/datastandardsinnovation/data/insider-transactions-data-sets/"]
GAP = 0.6  # seconds between SEC requests -> < 2 per second


def wanted():
    for y in range(2006, 2027):
        for q in range(1, 5):
            if (y, q) > (2026, 2):
                return
            yield f"{y}q{q}"


def main():
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Accept-Encoding": "gzip, deflate"})
    last = 0.0
    for tag in wanted():
        name = f"{tag}_form345.zip"
        if (SHARED / name).exists() or (OUT / name).exists():
            continue
        for attempt in range(4):
            wait = GAP - (time.time() - last)
            if wait > 0:
                time.sleep(wait)
            last = time.time()
            r = s.get(BASES[attempt % 2] + name, timeout=120)
            if r.status_code == 200 and r.content[:2] == b"PK":
                (OUT / name).write_bytes(r.content)
                print(f"{tag}: {len(r.content)/1e6:.1f} MB", flush=True)
                break
            print(f"{tag}: HTTP {r.status_code}, retry {attempt}", file=sys.stderr, flush=True)
            time.sleep(5 * (attempt + 1))
        else:
            print(f"{tag}: FAILED", file=sys.stderr)


if __name__ == "__main__":
    main()

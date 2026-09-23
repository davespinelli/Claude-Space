#!/usr/bin/env python3
"""Download Cal-Maine Foods (CALM, CIK 16160) earnings releases and periodic reports from SEC EDGAR.

What it downloads (cached under cache/sec/, never re-downloaded unless --refresh):
  * submissions JSON (filing list)            https://data.sec.gov/submissions/CIK0000016160.json
  * for every 8-K with Item 2.02 since 2015-06: the filing index and the EX-99.1 press release
  * for every 10-Q / 10-K since 2015-06: the filing index and the primary document
  * companyfacts JSON (XBRL)                   https://data.sec.gov/api/xbrl/companyfacts/CIK0000016160.json

Writes cache/sec/filings_manifest.csv: form, filing date, acceptance time (UTC), report period,
accession, and the local + remote path of the document kept.

User-Agent carries dspinjr@gmail.com; requests are throttled to <= ~6.5 per second (SEC limit is 10).
"""
import json, sys, time
from pathlib import Path
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "cache" / "sec"
CACHE.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "ClaudeSpace research dspinjr@gmail.com", "Accept-Encoding": "gzip, deflate"}
CIK = 16160
START = "2015-06-01"
REFRESH = "--refresh" in sys.argv
_last = [0.0]


def get(url, dest: Path, binary=False):
    if dest.exists() and not REFRESH:
        return dest.read_bytes() if binary else dest.read_text(errors="replace")
    wait = 0.155 - (time.time() - _last[0])
    if wait > 0:
        time.sleep(wait)
    for attempt in range(5):
        r = requests.get(url, headers=UA, timeout=60)
        _last[0] = time.time()
        if r.status_code < 500:
            break
        time.sleep(2 * (attempt + 1))
    r.raise_for_status()
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(r.content)
    return r.content if binary else r.text


def main():
    sub = json.loads(get(f"https://data.sec.gov/submissions/CIK{CIK:010d}.json", CACHE / "submissions.json"))
    get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{CIK:010d}.json", CACHE / "companyfacts.json")
    r = sub["filings"]["recent"]
    rows = []
    for i in range(len(r["form"])):
        form, fd = r["form"][i], r["filingDate"][i]
        if fd < START:
            continue
        items = r["items"][i] or ""
        want = (form == "8-K" and "2.02" in items) or form in ("10-Q", "10-K")
        if not want:
            continue
        acc = r["accessionNumber"][i]
        accnd = acc.replace("-", "")
        base = f"https://www.sec.gov/Archives/edgar/data/{CIK}/{accnd}/"
        idx = json.loads(get(base + "index.json", CACHE / accnd / "index.json"))
        names = [it["name"] for it in idx["directory"]["item"]]
        if form == "8-K":
            # EX-99.1 press release: an .htm that is not the 8-K cover, not an index page, not an XBRL R-file.
            # Prefer names with "99"/"press"; otherwise the largest remaining .htm.
            import re as _re
            items_ = [it for it in idx["directory"]["item"]
                      if it["name"].lower().endswith((".htm", ".html")) and it["name"] != r["primaryDocument"][i]
                      and "index" not in it["name"].lower() and not _re.fullmatch(r"r\d+\.htm", it["name"].lower())]
            pref = [it for it in items_ if ("99" in it["name"].lower() or "press" in it["name"].lower())
                    and "992" not in it["name"].lower() and "99-2" not in it["name"].lower()]
            pool = pref or items_
            pool.sort(key=lambda it: -int(it.get("size") or 0))
            doc = pool[0]["name"] if pool else r["primaryDocument"][i]
        else:
            doc = r["primaryDocument"][i]
        local = CACHE / accnd / doc
        get(base + doc, local)
        rows.append(dict(form=form, filing_date=fd, accepted_utc=r["acceptanceDateTime"][i],
                         report_date=r["reportDate"][i], accession=acc, items=items, doc=doc,
                         url=base + doc, local=str(local.relative_to(ROOT))))
        print(form, fd, doc, flush=True)
    m = pd.DataFrame(rows).sort_values("filing_date")
    m.to_csv(CACHE / "filings_manifest.csv", index=False)
    print(len(m), "documents")


if __name__ == "__main__":
    main()

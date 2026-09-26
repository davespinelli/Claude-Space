"""List every 10-Q / 10-K primary document that mentions "10b5-1", month by month, from EDGAR
full-text search. Used only to find the filings that lack ecd XBRL tags so their Item 5 / Item 9B
text can be parsed. Writes cache/fts_10b51_docs.csv.gz."""
import datetime as dt
import sys
import urllib.parse
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sec

BASE = "https://efts.sec.gov/LATEST/search-index"
CAP = 10_000


def months(a: dt.date, b: dt.date):
    cur = dt.date(a.year, a.month, 1)
    while cur <= b:
        nxt = dt.date(cur.year + (cur.month == 12), cur.month % 12 + 1, 1)
        yield cur, min(nxt - dt.timedelta(days=1), b)
        cur = nxt


def page(q, forms, a, b, frm):
    u = (f"{BASE}?q={urllib.parse.quote(q)}&forms={urllib.parse.quote(forms)}&dateRange=custom"
         f"&startdt={a:%Y-%m-%d}&enddt={b:%Y-%m-%d}")
    if frm:
        u += f"&from={frm}"
    return sec.get_json(u, "fts")


def run(start=dt.date(2023, 7, 1), end=dt.date(2026, 6, 30), q='"10b5-1"', forms="10-Q,10-K,10-KT,10-QT"):
    rows = []
    for a, b in months(start, end):
        d = page(q, forms, a, b, 0)
        tot = d["hits"]["total"]["value"]
        if tot >= CAP:
            raise RuntimeError(f"{a} hits {tot} at cap; split further")
        hits = list(d["hits"]["hits"])
        frm = len(hits)
        while frm < tot:
            dd = page(q, forms, a, b, frm)
            h = dd["hits"]["hits"]
            if not h:
                break
            hits += h
            frm += len(h)
        for h in hits:
            s = h["_source"]
            adsh, fn = h["_id"].split(":", 1)
            rows.append({"adsh": adsh, "file": fn, "form": s.get("form"), "file_type": s.get("file_type"),
                         "file_date": s.get("file_date"), "period_ending": s.get("period_ending"), "ciks": ";".join(s.get("ciks") or []),
                         "sics": ";".join(s.get("sics") or []), "names": " | ".join(s.get("display_names") or [])})
        print(a, tot, len(hits), flush=True)
    df = pd.DataFrame(rows).drop_duplicates(["adsh", "file"])
    df.to_csv(sec.CACHE / "fts_10b51_docs.csv.gz", index=False)
    return df


if __name__ == "__main__":
    run()

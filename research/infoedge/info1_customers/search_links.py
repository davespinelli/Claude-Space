#!/usr/bin/env python3
"""
INFO-1 step 2: find and parse every 10-K (filed 2010-01-01 .. 2026-09-25) that names
an alias-list customer in a customer-share phrase.

Stages
  fts     For each customer in aliases.py, one EDGAR full-text-search OR-query (split
          into chunks of <= 40 phrases) over 10-K forms of phrase templates such as
          "sales to <name>", "<name> accounted", "revenues from <name>",
          "<name> Inc accounted", "largest customer <name>" (TEMPLATES below).
          -> data/alias_hits.csv.gz (one row per matched file and customer query)
  index   EDGAR full-index form.idx 2010Q1..2026Q3: every 10-K / 10-KT / 10-K405 filing
          (CIK, date, accession) -> data/tenk_index.csv.gz; used for "until the next 10-K".
  docs    Fetch every matched original-10-K document (main document or EX-13), plus the
          1,500 discovery-sample documents, run extract.extract() on each.
          -> data/mentions.csv.gz (one row per customer mention) and
             data/docs_processed.csv.gz (one row per document, incl. zero-mention ones)

Run: .venv/bin/python research/infoedge/info1_customers/search_links.py --stage fts|index|docs
"""
from __future__ import annotations

import argparse
import datetime as dt
import gzip
import json
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import edgar  # noqa: E402
from aliases import C as CUSTOMERS  # noqa: E402
from discover import doc_ok, hit_row  # noqa: E402

DATA = HERE / "data"
START = dt.date(2010, 1, 1)
END = dt.date(2026, 9, 25)
TEMPLATES = [
    "sales to {N}", "revenue from {N}", "revenues from {N}", "shipments to {N}", "sold to {N}",
    "{N} accounted", "{N} represented", "{N} comprised", "{N} constituted", "{N} accounting for",
    "{N} which accounted", "{N} and its affiliates", "{N} and its subsidiaries", "{N} together with",
    "{N} was our largest", "{N} is our largest", "{N} our largest", "{N} our single largest",
    "largest customer {N}", "largest customers {N}", "largest customer was {N}", "largest customers were {N}",
    "customers were {N}", "customer was {N}",
    "{N} Inc accounted", "{N} Inc represented", "{N} Inc and its", "{N} Inc which", "{N} Inc our largest",
    "{N} Corporation accounted", "{N} Corporation represented", "{N} Corporation and its",
    "{N} Corp accounted", "{N} Company accounted", "{N} Co accounted", "{N} LLC accounted",
    "{N} Stores Inc", "{N} Inc collectively",
]
# second pass (added after the recall check on the discovery sample showed misses such as
# "one customer, BP plc, accounted", "Texas Instruments Incorporated accounted", "Cisco ... generated")
TEMPLATES2 = [
    "customer {N}", "customers {N}", "client {N}", "clients {N}", "purchaser {N}", "purchasers {N}",
    "{N} Incorporated accounted", "{N} Incorporated represented", "{N} who accounted", "{N} which represented",
    "{N} generated", "{N} contributed", "{N} plc accounted", "{N} plc and",
]
CHUNK = 40


def fts_spellings(c: dict) -> list[str]:
    out = []
    for s in c["fts"]:
        out.append(s)
        if "'" in s:
            out.append(s.replace("'", " "))
            out.append(s.replace("'", ""))
    return list(dict.fromkeys(out))


COMMON_WORDS = {"Target", "Shell", "Sprint"}   # "customers target ..." is ordinary English


def queries_for(c: dict, templates=None) -> list[str]:
    phrases = []
    for n in fts_spellings(c):
        if templates is not None and n in COMMON_WORDS:
            continue
        for t in (templates or TEMPLATES):
            phrases.append('"' + t.format(N=n).replace('"', "") + '"')
    phrases = list(dict.fromkeys(phrases))
    return [" OR ".join(phrases[i:i + CHUNK]) for i in range(0, len(phrases), CHUNK)]


def stage_fts(second: bool = False):
    jobs = []
    for c in CUSTOMERS:
        for k, q in enumerate(queries_for(c, TEMPLATES2 if second else None)):
            jobs.append((c["id"], k, q))
    prefix = "alias2" if second else "alias"
    out_name = "alias_hits2" if second else "alias_hits"
    print(f"{len(jobs)} queries for {len(CUSTOMERS)} customers", flush=True)
    rows, audit = [], []
    lock = threading.Lock()

    def one(job):
        cid, k, q = job
        hits, au = edgar.fts_all(q, f"{prefix}/{cid}_{k}", START, END)
        return cid, k, hits, au

    done = 0
    with ThreadPoolExecutor(max_workers=10) as ex:
        for cid, k, hits, au in ex.map(one, jobs):
            with lock:
                for h in hits:
                    r = hit_row(h)
                    r["customer_query"] = cid
                    rows.append(r)
                for a in au:
                    a["customer_query"] = cid
                audit += au
                done += 1
                if done % 20 == 0:
                    print(f"  {done}/{len(jobs)} queries  hits so far {len(rows)}  net={edgar.STATS['network']}", flush=True)
    df = pd.DataFrame(rows)
    df["doc_ok"] = doc_ok(df)
    df.to_csv(DATA / f"{out_name}.csv.gz", index=False)
    pd.DataFrame(audit).to_csv(DATA / f"{out_name}_audit.csv", index=False)
    u = df[df.doc_ok].drop_duplicates(["adsh", "file_name"])
    print(f"alias hits: {len(df)} rows, {df[['adsh','file_name']].drop_duplicates().shape[0]} files, "
          f"doc_ok files {len(u)}, filers {u.cik.nunique()}")


IDX_LINE = re.compile(r"^(?P<form>\S+(?: \S+)?)\s+(?P<name>.+?)\s+(?P<cik>\d{1,10})\s+(?P<date>\d{4}-\d{2}-\d{2})\s+(?P<fn>edgar/\S+)\s*$")


def stage_index():
    rows = []
    for y in range(2009, 2027):
        for q in (1, 2, 3, 4):
            if (y, q) > (2026, 3):
                break
            txt = edgar.full_index(y, q)
            for line in txt.splitlines():
                if not line.startswith(("10-K ", "10-K405 ", "10-KT ", "10-K/A ", "10-KT/A ")):
                    continue
                mm = IDX_LINE.match(line)
                if not mm:
                    continue
                m = re.search(r"(\d{10}-\d{2}-\d{6})", mm.group("fn"))
                rows.append(dict(form=mm.group("form").strip(), name=mm.group("name").strip(), cik=int(mm.group("cik")),
                                 date=mm.group("date"), adsh=m.group(1) if m else None))
            print(f"  index {y}Q{q}: {len(rows)} rows so far", flush=True)
    df = pd.DataFrame(rows).drop_duplicates()
    df.to_csv(DATA / "tenk_index.csv.gz", index=False)
    print(f"10-K index: {len(df)} filings, {df.cik.nunique()} CIKs")


# --------------------------------------------------------------------------- docs
def _fetch(row) -> str:
    raw = edgar.fetch_doc(int(row["cik"]), row["adsh"], row["file_name"])
    return "missing" if raw is None else "ok"


def _extract(row) -> dict:
    """CPU step (separate process): cached raw document -> mentions."""
    import edgar as E
    from extract import extract
    from textutil import html_to_text
    E.OFFLINE = True
    raw = E.fetch_doc(int(row["cik"]), row["adsh"], row["file_name"])
    if raw is None:
        return {"status": "missing", "n_chars": 0, "mentions": []}
    text = html_to_text(raw)
    return {"status": "ok", "n_chars": len(text), "mentions": extract(text, str(row.get("display_name") or ""))}


def doc_list() -> pd.DataFrame:
    ah = pd.read_csv(DATA / "alias_hits.csv.gz")
    if (DATA / "alias_hits2.csv.gz").exists():
        ah2 = pd.read_csv(DATA / "alias_hits2.csv.gz")
        ah2["customer_query"] = ah2.customer_query + "#2"
        ah = pd.concat([ah, ah2], ignore_index=True)
    ah["doc_ok"] = doc_ok(ah)
    ah = ah[ah.doc_ok]
    src = ah.groupby(["adsh", "file_name"]).customer_query.apply(lambda s: ";".join(sorted(set(s)))).rename("queries")
    docs = ah.drop_duplicates(["adsh", "file_name"]).set_index(["adsh", "file_name"])
    docs = docs.join(src).reset_index()
    docs["in_alias_search"] = True
    ds = pd.read_csv(DATA / "discovery_sample_docs.csv")
    ds["in_alias_search"] = False
    ds["queries"] = ""
    ds["in_discovery"] = True
    key = lambda d: d.set_index(["adsh", "file_name"]).index  # noqa: E731
    docs["in_discovery"] = key(docs).isin(key(ds))
    extra = ds[~key(ds).isin(key(docs))]
    docs = pd.concat([docs, extra], ignore_index=True)
    return docs.sort_values("file_date").reset_index(drop=True)


def stage_docs(workers: int = 8, limit: int | None = None, fetch_only: bool = False):
    from concurrent.futures import ProcessPoolExecutor
    docs = doc_list()
    if limit:
        docs = docs.head(limit)
    rows = docs.to_dict("records")
    print(f"{len(docs)} documents ({int(docs.in_alias_search.sum())} from alias search, "
          f"{int((~docs.in_alias_search).sum())} discovery-only)", flush=True)
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for i, st in enumerate(ex.map(_fetch, rows), 1):
            if i % 500 == 0:
                el = time.time() - t0
                print(f"  fetched {i}/{len(rows)}  net={edgar.STATS['network']}  {el/60:.1f} min, "
                      f"eta {(len(rows)-i)*el/i/60:.0f} min", flush=True)
    if fetch_only:
        return
    recs, drecs = [], []
    keys = ("cid", "alias", "pct", "pcts", "role", "combined", "list_items", "years", "snippet", "offset")
    with ProcessPoolExecutor(max_workers=8) as ex:
        for i, (r, out) in enumerate(zip(rows, ex.map(_extract, rows, chunksize=20)), 1):
            drecs.append(dict(cik=r["cik"], adsh=r["adsh"], file_name=r["file_name"], file_date=r["file_date"],
                              form=r["form"], file_type=r["file_type"], period_ending=r["period_ending"],
                              display_name=r["display_name"], sic=r["sic"], queries=r["queries"],
                              in_alias_search=r["in_alias_search"], in_discovery=r["in_discovery"],
                              status=out["status"], n_chars=out["n_chars"], n_mentions=len(out["mentions"])))
            for m in out["mentions"]:
                recs.append(dict(cik=r["cik"], adsh=r["adsh"], file_name=r["file_name"], file_date=r["file_date"],
                                 period_ending=r["period_ending"], display_name=r["display_name"], sic=r["sic"],
                                 **{k: m.get(k) for k in keys}))
            if i % 2000 == 0:
                print(f"  extracted {i}/{len(rows)}  mentions {len(recs)}", flush=True)
    pd.DataFrame(drecs).to_csv(DATA / "docs_processed.csv.gz", index=False)
    pd.DataFrame(recs).to_csv(DATA / "mentions.csv.gz", index=False)
    print(f"docs {len(drecs)}, mentions {len(recs)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True, choices=["fts", "fts2", "index", "docs"])
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--fetch-only", action="store_true")
    a = ap.parse_args()
    {"fts": stage_fts, "fts2": lambda: stage_fts(True), "index": stage_index}.get(
        a.stage, lambda: stage_docs(a.workers, a.limit, a.fetch_only))()

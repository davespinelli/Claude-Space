#!/usr/bin/env python3
"""
INFO-1 step 1: the universe of 10-Ks that talk about customer concentration, and a
random discovery sample used to build the customer alias list.

Stages
  hits    EDGAR full-text search, 10-K forms filed 2010-01-01 .. END, one query per
          calendar year (split to months if a year reaches the 10,000-hit cap):
            "customer accounted" OR "customers accounted" OR "largest customer" OR
            "largest customers" OR "major customer" OR "major customers" OR
            "significant customer" OR "significant customers" OR "one customer" OR
            "two customers"
          -> data/generic_hits.csv.gz  (one row per matched file)
  sample  random 1,500 original-10-K files (main document or EX-13) from those hits,
          stratified by filing year, fetched and scanned with a generic
          named-customer pattern -> data/discovery_names.csv (name, n filers, n docs,
          example sentence) and data/discovery_sample_docs.csv

Run: .venv/bin/python research/infoedge/info1_customers/discover.py --stage hits|sample
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import edgar  # noqa: E402
from textutil import html_to_text, sentences  # noqa: E402

DATA = HERE / "data"
DATA.mkdir(exist_ok=True)
START = dt.date(2010, 1, 1)
END = dt.date(2026, 9, 25)
GENERIC = ['"customer accounted"', '"customers accounted"', '"largest customer"', '"largest customers"',
           '"major customer"', '"major customers"', '"significant customer"', '"significant customers"',
           '"one customer"', '"two customers"']
GENERIC_Q = " OR ".join(GENERIC)


def hit_row(h: dict) -> dict:
    s = h["_source"]
    adsh, _, fname = h["_id"].partition(":")
    ciks = s.get("ciks") or []
    names = s.get("display_names") or []
    sics = s.get("sics") or []
    return dict(cik=int(ciks[0]) if ciks else None, n_ciks=len(ciks), adsh=s.get("adsh") or adsh,
                file_name=fname, file_date=s.get("file_date"), form=s.get("form"),
                root_form=";".join(s.get("root_forms") or []), file_type=s.get("file_type"),
                file_description=s.get("file_description"), period_ending=s.get("period_ending"),
                display_name=names[0] if names else None, sic=sics[0] if sics else None)


def doc_ok(df: pd.DataFrame) -> pd.Series:
    """Original annual reports only: the 10-K / 10-KT document itself or its EX-13."""
    ft = df.file_type.fillna("").str.upper()
    form = df.form.fillna("").str.upper()
    orig = form.isin(["10-K", "10-KT", "10-K405"])
    main = ft.isin(["10-K", "10-KT", "10-K405"]) | ft.str.startswith("EX-13")
    textual = df.file_name.fillna("").str.lower().str.contains(r"\.(?:htm|html|txt)$")
    return orig & main & textual


def stage_hits():
    from concurrent.futures import ThreadPoolExecutor
    rows, audit = [], []
    with ThreadPoolExecutor(max_workers=4) as ex:
        futs = {ex.submit(edgar.fts_all, GENERIC_Q, "generic", a, b): a for a, b in edgar.year_slices(START, END)}
        for f, a in futs.items():
            hits, au = f.result()
            rows += [hit_row(h) for h in hits]
            audit += au
            print(f"{a.year}: {len(hits)} files  net={edgar.STATS['network']} cache={edgar.STATS['cache']}", flush=True)
    df = pd.DataFrame(rows).drop_duplicates(["adsh", "file_name"])
    df["doc_ok"] = doc_ok(df)
    df.to_csv(DATA / "generic_hits.csv.gz", index=False)
    pd.DataFrame(audit).to_csv(DATA / "generic_hits_audit.csv", index=False)
    print(f"generic hits: {len(df)} files, {df.adsh.nunique()} filings, doc_ok {int(df.doc_ok.sum())}")


# ----------------------------------------------------------------------------- discovery extraction
TOK = r"(?:[A-Z][A-Za-z0-9&'.\-]*|&)"
NAME = rf"({TOK}(?:\s+(?:{TOK}|and|of|de|the|du)){{0,6}})"
SUFFIX = r"(?:,?\s+(?:Incorporated|Inc|Corporation|Corp|Company|Co|L\.L\.C|LLC|Limited|Ltd|L\.P|LP|plc|N\.V|S\.A|AG|SE)\.?(?![A-Za-z]))*"
PAT_A = re.compile(rf"\b(?:sales|revenues?|shipments)\s+(?:to|from)\s+{NAME}")
PAT_B = re.compile(rf"{NAME}{SUFFIX}(?:\s*\([^)]{{1,80}}\))?,?\s+(?:and its (?:affiliates|subsidiaries)\s+|together with its [a-z]+\s+)?"
                   r"(?:accounted for|represented|comprised|constituted)")
PAT_C = re.compile(rf"\blargest customers?,?\s+(?:was|were|is|are)?\s*{NAME}")
PCT = re.compile(r"\d{1,3}(?:\.\d+)?\s?(?:%|percent\b)")
REVW = re.compile(r"(?i)\b(?:net sales|sales|revenues?|net revenues?)\b")
STOP = {"the", "we", "our", "sales", "revenue", "revenues", "net", "customer", "customers", "one", "two", "three",
        "no", "each", "these", "this", "such", "in", "during", "for", "fiscal", "total", "company", "the company",
        "a", "an", "its", "their", "other", "all", "approximately", "product", "products", "domestic",
        "international", "u", "us", "united", "government", "federal"}


def norm_name(n: str) -> str:
    n = re.sub(r"[,.]+$", "", n.strip())
    n = re.sub(r"^(?:The|Our|and|of)\s+", "", n)
    n = re.sub(SUFFIX + r"$", "", n).strip(" ,.")
    return n


def generic_names(text: str) -> list[tuple[str, str]]:
    out = []
    for _, s in sentences(text):
        if len(s) > 1500 or not PCT.search(s) or not REVW.search(s):
            continue
        for pat in (PAT_A, PAT_B, PAT_C):
            for m in pat.finditer(s):
                n = norm_name(m.group(1))
                if not n or n.lower() in STOP or len(n) < 2:
                    continue
                first = n.split()[0].lower()
                if first in STOP:
                    continue
                out.append((n, s[:400]))
    return out


def stage_sample(n: int = 1500, seed: int = 11):
    df = pd.read_csv(DATA / "generic_hits.csv.gz")
    df = df[df.doc_ok].copy()
    df["year"] = pd.to_datetime(df.file_date).dt.year
    rng = np.random.default_rng(seed)
    per = max(1, n // df.year.nunique())
    samp = (df.groupby("year", group_keys=False)
            .apply(lambda g: g.iloc[rng.choice(len(g), size=min(per, len(g)), replace=False)]))
    samp = samp.reset_index(drop=True)
    samp.to_csv(DATA / "discovery_sample_docs.csv", index=False)
    cnt_f, cnt_d, ex = defaultdict(set), Counter(), {}
    from concurrent.futures import ThreadPoolExecutor

    def fetch(r):
        raw = edgar.fetch_doc(int(r.cik), r.adsh, r.file_name)
        return None if raw is None else generic_names(html_to_text(raw))

    with ThreadPoolExecutor(max_workers=8) as pool:
        found = list(pool.map(fetch, [r for _, r in samp.iterrows()]))
    for (i, r), names in zip(samp.iterrows(), found):
        if names is None:
            continue
        seen = set()
        for nm, s in names:
            k = nm.lower()
            cnt_f[k].add(int(r.cik))
            if k not in seen:
                cnt_d[k] += 1
                seen.add(k)
            ex.setdefault(k, (nm, s))
        if (i + 1) % 100 == 0:
            print(f"  {i+1}/{len(samp)} docs  net={edgar.STATS['network']}", flush=True)
    out = pd.DataFrame([dict(name=ex[k][0], key=k, n_filers=len(cnt_f[k]), n_docs=cnt_d[k], example=ex[k][1])
                        for k in cnt_d]).sort_values(["n_filers", "n_docs"], ascending=False)
    out.to_csv(DATA / "discovery_names.csv", index=False)
    print(out.head(80).to_string())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True, choices=["hits", "sample"])
    ap.add_argument("--n", type=int, default=1500)
    a = ap.parse_args()
    if a.stage == "hits":
        stage_hits()
    else:
        stage_sample(a.n)

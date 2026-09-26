#!/usr/bin/env python3
"""Stage 2: which candidate companies have any federal contract actions at all?

For every alias of every candidate company we build search phrases
(common.search_phrases: broad first word, then the SEC name core) and ask
USAspending how many contract transactions (types A-D, action dates FY2010
onward) have that phrase inside the recipient name or the recipient's parent
name (the API matches substrings). The broad phrase is kept when it has
1..MAX_BROAD hits; if it has none, the company has no contract actions (the core
contains it); if it has more, the core phrase is counted and kept when it has
at most MAX_CORE hits.

Scope (the brief: focus on companies that are real federal contractors):
  * non-financial candidates from stage 1;
  * industries excluded: SIC 0100-1499 (agriculture, mining, oil and gas
    production), 2000-2199 (food, tobacco), 5200-5999 (retail), 7000-7299
    (hotels, personal services), 7500-7999 (auto repair, film, recreation);
  * companies whose public float was >= $2B at every XBRL cover date 2009-2025
    (always too large) are skipped;
  * former names are used only if they were still in use on or after 2008-01-01.

Writes data/scan.csv; raw responses cached in cache/scan/.
"""
from __future__ import annotations

import gzip
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor

import pandas as pd

from common import CACHE, CONTRACT_TYPES, DATA, ROOT, log, search_phrases, usas_post

START, END = "2009-10-01", "2026-09-30"
MAX_BROAD = 30_000
MAX_CORE = 250_000
SCAN = CACHE / "scan"
SCAN.mkdir(exist_ok=True)
EXCLUDED_SIC = [(100, 1499), (2000, 2199), (5200, 5999), (7000, 7299), (7500, 7999)]


def count(phrase: str):
    key = hashlib.md5(phrase.encode()).hexdigest()
    p = SCAN / f"{key}.json.gz"
    if p.exists():
        with gzip.open(p, "rt") as fh:
            return json.loads(fh.read())["n"]
    js = usas_post("/search/spending_by_transaction_count/", {"filters": {
        "award_type_codes": CONTRACT_TYPES,
        "time_period": [{"start_date": START, "end_date": END}],
        "recipient_search_text": [phrase]}}, timeout=45, max_slow=1)
    if js is None:
        return None
    # a count that takes over 45 seconds twice is a very broad phrase: treated as too wide
    n = -1 if "__error__" in js else 10 ** 9 if "__timeout__" in js else int(js["results"]["contracts"])
    with gzip.open(p, "wt") as fh:
        fh.write(json.dumps({"phrase": phrase, "n": n}))
    return n


def float_min() -> pd.Series:
    vals = []
    for f in sorted((ROOT / "research/oplev/cache/frames").glob("dei_EntityPublicFloat_USD_*.json.gz")):
        with gzip.open(f, "rt") as fh:
            js = json.loads(fh.read())
        if not js or not isinstance(js, dict):
            continue
        for r in js.get("data", []):
            vals.append((int(r["cik"]), float(r["val"])))
    d = pd.DataFrame(vals, columns=["cik", "val"])
    return d.groupby("cik").val.min()


def scope() -> pd.DataFrame:
    U = pd.read_csv(DATA / "universe.csv")
    excl = pd.Series(False, index=U.index)
    for a, b in EXCLUDED_SIC:
        excl |= U.sic.between(a, b)
    fm = float_min()
    U["float_min"] = U.cik.map(fm)
    U["always_large"] = U.float_min >= 2e9
    U["excluded_industry"] = excl
    U["in_scope"] = ~excl & ~U.always_large & U.sic.notna()      # no SIC: funds, trusts
    U.to_csv(DATA / "universe_scope.csv", index=False)
    A = pd.read_csv(DATA / "aliases.csv")
    A = A[A.cik.isin(U.loc[U.in_scope, "cik"])]
    A = A[(A.src == "current") | (pd.to_datetime(A.name_to, errors="coerce", utc=True)
                                  >= pd.Timestamp("2008-01-01", tz="UTC"))]
    log(f"scope: {int(U.in_scope.sum())} companies in scope (excluded industry {int(excl.sum())}, "
        f"always >= $2B {int(U.always_large.sum())}); {len(A)} aliases")
    return A


def run_all(phrases, workers=3):
    res = {}
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for i, (ph, n) in enumerate(zip(phrases, ex.map(count, phrases)), 1):
            res[ph] = n
            if i % 500 == 0:
                log(f"  counted {i}/{len(phrases)}")
    return res


def main():
    A = scope()
    A["phrases"] = A.name.map(search_phrases)
    A = A[A.phrases.map(len) > 0]
    first = sorted({ps[0] for ps in A.phrases})
    log(f"round 1: {len(first)} phrases")
    res = run_all(first)
    second = sorted({ps[1] for ps in A.phrases if len(ps) > 1
                     and (res.get(ps[0]) is None or res[ps[0]] > MAX_BROAD or res[ps[0]] < 0)} - set(res))
    log(f"round 2: {len(second)} core phrases (broad phrase too wide or failed)")
    res.update(run_all(second))
    rows = []
    for a in A.itertuples():
        chosen, n = None, None
        p0 = a.phrases[0]
        c0 = res.get(p0)
        if c0 is not None and 0 <= c0 <= (MAX_BROAD if len(a.phrases) > 1 else MAX_CORE):
            chosen, n = p0, c0
        elif len(a.phrases) > 1:
            c1 = res.get(a.phrases[1])
            if c1 is not None and 0 <= c1 <= MAX_CORE:
                chosen, n = a.phrases[1], c1
        rows.append(dict(cik=a.cik, name=a.name, src=a.src, phrase=chosen, n=n,
                         all_phrases="|".join(a.phrases),
                         counts="|".join(str(res.get(p)) for p in a.phrases)))
    S = pd.DataFrame(rows)
    S.to_csv(DATA / "scan.csv", index=False)
    hit = S[S.n.fillna(0) > 0]
    log(f"scan: {S.cik.nunique()} companies, {hit.cik.nunique()} with contract hits; "
        f"{hit.phrase.nunique()} phrases, {int(hit.drop_duplicates('phrase').n.sum())} rows expected; "
        f"aliases unresolved (failed or too wide) {int(S.phrase.isna().sum())}")


if __name__ == "__main__":
    main()

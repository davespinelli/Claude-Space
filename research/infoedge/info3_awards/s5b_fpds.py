#!/usr/bin/env python3
"""Stage 5b: FPDS record dates for every candidate action.

Input: cache/all_priced_actions.parquet and cache/all_missing_actions.parquet
from a first stage-6 pass on the pre-registered rule dates (--rule-only).
Actions with size ratio >= 1.5% (a margin below the 2% screen, because the
refined public date moves day 0 and therefore the market cap) are looked up in
the FPDS ATOM feed by PIID + modification number + referenced IDV PIID.

Writes data/fpds_dates.parquet: key, n_entries, signed, created, approved,
last_modified (first matching entry whose signed date equals the action date,
else the first entry).
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

import pandas as pd

from common import CACHE, DATA, log
from fpds import fetch, parse

MARGIN = 0.015


def one(r):
    ref = r.ref_idv if isinstance(r.ref_idv, str) and r.ref_idv.strip() else None
    x = fetch(r["piid"], r["mod"], ref)
    if not x:
        return dict(key=r.key, n_entries=None)
    es = parse(x)
    if not es:
        return dict(key=r.key, n_entries=0)
    ad = pd.Timestamp(r.action_date).strftime("%Y-%m-%d")
    pick = [e for e in es if e.get("signedDate", "")[:10] == ad] or es
    e = pick[0]
    return dict(key=r.key, n_entries=len(es), n_same_date=len([z for z in es if z.get("signedDate", "")[:10] == ad]),
                signed=e.get("signedDate"), created=e.get("createdDate"), approved=e.get("approvedDate"),
                last_modified=e.get("lastModifiedDate"), fpds_amount=e.get("obligatedAmount"),
                fpds_parent=e.get("ultimateParentUEIName"), fpds_vendor=e.get("vendorName"))


def main():
    C = pd.read_parquet(CACHE / "all_priced_actions.parquet")
    X = pd.read_parquet(CACHE / "all_missing_actions.parquet")
    C = C[(C.ratio >= MARGIN) & (C.mcap < 2e9)]
    X = X[(X.ratio_float >= MARGIN) & (X.pfloat < 2e9)]
    D = pd.concat([C, X], ignore_index=True).drop_duplicates("key")
    D["mod"] = D["mod"].fillna("0").astype(str)
    log(f"FPDS lookups for {len(D)} actions")
    rows = []
    with ThreadPoolExecutor(max_workers=3) as ex:
        for i, res in enumerate(ex.map(one, [r for _, r in D.iterrows()]), 1):
            rows.append(res)
            if i % 200 == 0:
                log(f"  {i}/{len(D)}")
    F = pd.DataFrame(rows)
    for c in ("signed", "created", "approved", "last_modified"):
        if c in F:
            F[c] = pd.to_datetime(F[c], errors="coerce")
    F = F.rename(columns={"key": "contract_transaction_unique_key"})
    F.to_parquet(DATA / "fpds_dates.parquet", index=False)
    ok = F.approved.notna()
    log(f"FPDS: {int(ok.sum())} of {len(F)} found")


if __name__ == "__main__":
    main()

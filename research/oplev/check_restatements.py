#!/usr/bin/env python3
"""
Diagnostic (not a test): how different are the frames API's "last filed" values
from the values a company first reported?

The frames API returns, for each company and period, the value from the most
recent filing that reported that period. Revenue for fiscal 2015 is usually
taken from the 2017 10-K (three-year income statement), so a later restatement
or discontinued-operations reclassification leaks into the 2016 formation.
This script draws a fixed random sample of universe firm-years (seed 7), pulls
each company's full fact history (companyfacts API, cached), and compares the
frames value with the value in the earliest filing that reported the same
period. Writes cache/restatement_check.json; run_tests.py folds it into
results.json if present.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

import build_panel as B

HERE = Path(__file__).resolve().parent
OUT = B.CACHE / "restatement_check.json"
CF = B.CACHE / "companyfacts"
CF.mkdir(exist_ok=True)
N_SAMPLE = 150


def first_filed(facts: dict, tag: str, end: str, start: str | None):
    try:
        units = facts["facts"]["us-gaap"][tag]["units"]["USD"]
    except KeyError:
        return None
    c = [u for u in units if u.get("end") == end and (start is None or u.get("start") == start)
         and u.get("form", "").startswith("10-K")]
    if not c:
        return None
    c.sort(key=lambda u: u.get("filed", ""))
    return c[0]


def main():
    P = pd.read_parquet(HERE / "panel.parquet")
    U = P[P.in_univ & P.opinc.notna()]
    samp = U.sample(n=N_SAMPLE, random_state=7)
    rows = []
    for _, r in samp.iterrows():
        cik = int(r.cik)
        js = B.get_json(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json",
                        CF / f"CIK{cik:010d}.json.gz")
        if not js or js == "FAILED":
            continue
        end = pd.Timestamp(r.rev_end).strftime("%Y-%m-%d")
        fy = int(r.year) - 1
        fr_rev = B.load_frame("us-gaap", r.rev_tag, "USD", f"CY{fy}") if r.rev_tag in B.REV_TAGS else None
        start = None
        if fr_rev is not None:
            m = fr_rev[fr_rev.cik == cik]
            if len(m) and pd.notna(m.start.iloc[0]):
                start = m.start.iloc[0].strftime("%Y-%m-%d")
        # earliest 10-K reporting this period under ANY total-revenue tag: what an
        # investor could have read, even if the company later switched tags
        cands = [first_filed(js, tg, end, start) for tg in B.REV_TAGS]
        cands = [c for c in cands if c]
        ff_rev = min(cands, key=lambda u: u.get("filed", "")) if cands else None
        ff_oi = first_filed(js, "OperatingIncomeLoss", end, start)
        rows.append(dict(
            cik=cik, year=int(r.year), rev_tag=r.rev_tag,
            rev_frames=r.revenue, rev_first=(ff_rev or {}).get("val"),
            rev_first_filed=(ff_rev or {}).get("filed"),
            oi_frames=r.opinc, oi_first=(ff_oi or {}).get("val"),
            oi_first_filed=(ff_oi or {}).get("filed"),
        ))
    d = pd.DataFrame(rows)
    d["rev_diff"] = (d.rev_frames / d.rev_first - 1).abs()
    d["oi_diff_pct_rev"] = (d.oi_frames - d.oi_first).abs() / d.rev_first
    d["first_filed_before_formation"] = pd.to_datetime(d.rev_first_filed) < pd.to_datetime(
        d.year.astype(str) + "-06-30")
    rv = d.dropna(subset=["rev_first"])
    ov = d.dropna(subset=["oi_first"])
    out = {
        "n_sampled": N_SAMPLE, "n_companyfacts_ok": int(len(d)),
        "n_rev_compared": int(len(rv)), "n_oi_compared": int(len(ov)),
        "rev_share_differs_gt_1pct": float((rv.rev_diff > 0.01).mean()),
        "rev_share_differs_gt_5pct": float((rv.rev_diff > 0.05).mean()),
        "rev_median_abs_diff": float(rv.rev_diff.median()),
        "oi_share_differs_gt_1pct_of_rev": float((ov.oi_diff_pct_rev > 0.01).mean()),
        "oi_share_differs_gt_0p1pct_of_rev": float((ov.oi_diff_pct_rev > 0.001).mean()),
        "share_first_10k_filed_before_formation": float(rv.first_filed_before_formation.mean()),
        "note": "first-filed = earliest 10-K reporting the same period under any total-revenue tag",
    }
    OUT.write_text(json.dumps(out, indent=1))
    d.to_csv(B.CACHE / "restatement_check_rows.csv", index=False)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()

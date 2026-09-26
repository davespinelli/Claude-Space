#!/usr/bin/env python3
"""Mapping precision: draw 50 event actions at random (seed fixed) from all
priced candidate actions (>= 2% of market cap, market cap < $2B) and list what
is needed to judge each by hand: was the recipient owned by the mapped listed
company on the action date?

  python spotcheck.py draw      -> data/spotcheck_sample.csv
  python spotcheck.py summarize -> reads data/spotcheck_judged.csv (the same
                                   rows plus columns correct (1/0) and note),
                                   writes data/spotcheck_summary.json
"""
from __future__ import annotations

import json
import sys

import numpy as np
import pandas as pd

from common import DATA

SEED = 20260926
N = 50


def draw():
    C = pd.read_parquet(DATA / "candidates.parquet")
    S = C.sample(n=min(N, len(C)), random_state=SEED).sort_values(["company", "action_date"])
    cols = ["key", "company", "ticker", "cik", "recipient", "parent", "match", "action_date", "amount", "mcap",
            "ratio", "agency", "subagency", "desc"]
    S[cols].to_csv(DATA / "spotcheck_sample.csv", index=False)
    print(S[cols[:9]].to_string())


def summarize():
    J = pd.read_csv(DATA / "spotcheck_judged.csv")
    n = len(J)
    k = int(J.correct.sum())
    by = J.groupby("match").correct.agg(["size", "sum"])
    # Wilson 95% interval
    p = k / n
    z = 1.96
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    lines = [f"{k} of {n} randomly drawn event actions were mapped to the right listed company "
             f"(precision {100 * p:.0f}%, 95% interval {100 * (c - h):.0f}-{100 * (c + h):.0f}%).",
             "By match type: " + "; ".join(f"{m} {int(r['sum'])}/{int(r['size'])}" for m, r in by.iterrows()) + "."]
    wrong = J[J.correct == 0]
    for r in wrong.itertuples():
        lines.append(f"Wrong: {r.recipient} (parent '{r.parent}') mapped to {r.company}, {str(r.action_date)[:10]}: {r.note}")
    out = {"n": n, "correct": k, "precision": p, "wilson_lo": c - h, "wilson_hi": c + h, "lines": lines}
    (DATA / "spotcheck_summary.json").write_text(json.dumps(out, indent=2))
    print("\n".join(lines))


if __name__ == "__main__":
    {"draw": draw, "summarize": summarize}[sys.argv[1]]()

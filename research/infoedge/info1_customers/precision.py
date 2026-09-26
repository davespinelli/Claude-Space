#!/usr/bin/env python3
"""
INFO-1 extraction precision: 50 random links (round 1: seed 2026, before the stale-year fix; round 2: seed 2027, final rules) from data/links.csv, read by
hand. Labels live in data/precision_labels.csv (written after reading each snippet):

  customer_ok  the named company really is a customer of the filer (not a supplier,
               competitor, licensor, parent, or a different company with a similar name)
  share_ok     the percentage is that customer's share of the filer's total sales or
               revenue for the most recent fiscal year shown, and is >= 10%
  correct      customer_ok and share_ok (the headline precision)

Run: .venv/bin/python research/infoedge/info1_customers/precision.py sample|score
"""
from __future__ import annotations

import sys
import textwrap
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"


def sample(n=50, seed=2027):
    L = pd.read_csv(DATA / "links.csv")
    s = L.sample(n=n, random_state=seed).reset_index(drop=True)
    s.index.name = "k"
    s[["supplier_cik", "display_name", "adsh", "file_name", "file_date", "cid", "alias", "pct", "pcts", "role",
       "combined", "snippet"]].to_csv(DATA / "precision_sample.csv")
    lines = []
    for k, r in s.iterrows():
        lines.append(f"### {k}. {r.display_name} ({r.file_date[:10]}) -> {r.cid} ({r.alias}) pct={r.pct} [{r.pcts}] role={r.role}")
        lines.append(textwrap.fill(str(r.snippet), 160))
        lines.append("")
    (DATA / "precision_sample.md").write_text("\n".join(lines))
    print("\n".join(lines))


def score():
    lab = pd.read_csv(DATA / "precision_labels.csv")
    lab["correct"] = lab.customer_ok & lab.share_ok
    out = {"n": len(lab), "customer_ok": int(lab.customer_ok.sum()), "share_ok": int(lab.share_ok.sum()),
           "correct": int(lab.correct.sum()), "precision": float(lab.correct.mean()),
           "customer_precision": float(lab.customer_ok.mean())}
    print(out)
    return out


if __name__ == "__main__":
    {"sample": sample, "score": score}[sys.argv[1]]()

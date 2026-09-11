#!/usr/bin/env python3
"""Idea 790 addendum (lane C, 2026-09-11) - the EXACT-only verification leg.

The main run's G4 calibration read PLANT-FALSE at 46.0%: a random 4-dp token of the right
shape matches SOME committed value within its own rounding tolerance about half the time,
because a run's artefacts hold millions of numbers.  That floor sits under every ROUND match,
so the ROUND-inclusive shares (core 93.5% vs base 89.4% at the headline point) are a weak
test.  The EXACT leg - the headline token present VERBATIM in the run's own committed data -
has no such floor: a 4-significant-digit string is not hit by accident at that rate.

This addendum re-reads the main run's own committed artefacts (.graph.csv, .verify.csv) and
restates the 25 tuned points on the EXACT leg alone.  No new data, no new parameters, nothing
re-tuned; it is arithmetic on what the main run already committed.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent
MAIN = OUT / "2026-09-11_does-the-RECORD-S-RELIANCE-GRAPH-have-a-LOAD-BEARING-CORE-worth-re-verifying_C"
STAMP = Path(__file__).name[:-3]
RANK_STATS = ["NAMED", "ECHOED", "SUM", "MAXLEG", "CTRL"]
SHARES = [0.02, 0.05, 0.10, 0.20, 0.25]
N_CONTROL = 120
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def main():
    g = pd.read_csv(f"{MAIN}.graph.csv").set_index("run")
    v = pd.read_csv(f"{MAIN}.verify.csv").set_index("run")
    v["ANY_exact_share"] = v.ANY_exact / v.n_head.replace(0, np.nan)
    v["DATA_exact_share"] = v.DATA_exact / v.n_head.replace(0, np.nan)

    # the main run's control sample is whatever it verified OUTSIDE every top-25% core
    sel = set()
    for s in RANK_STATS:
        k = max(1, int(round(max(SHARES) * len(g))))
        sel |= set(g.sort_values(s, ascending=False).index[:k])
    base = [r for r in v.index if r not in sel]
    P(f"# {STAMP}")
    P("# EXACT-only restatement of idea 790's 25 tuned points (no ROUND matches, so the "
      "46.0% PLANT-FALSE floor does not apply)")
    P(f"runs verified {len(v)}, non-core control sample {len(base)} "
      f"(the main run drew {N_CONTROL})")
    P("")
    rows = []
    for s in RANK_STATS:
        for sh in SHARES:
            k = max(1, int(round(sh * len(g))))
            core = [r for r in g.sort_values(s, ascending=False).index[:k] if r in v.index]
            d = dict(statistic=s, share=sh, n_core=len(core))
            for leg in ("ANY_exact_share", "DATA_exact_share"):
                d["core_" + leg[:-6]] = float(v.loc[core, leg].mean())
                d["base_" + leg[:-6]] = float(v.loc[base, leg].mean())
                d["lift_" + leg[:-6]] = d["core_" + leg[:-6]] - d["base_" + leg[:-6]]
            rows.append(d)
    t = pd.DataFrame(rows)
    P(t.set_index(["statistic", "share"]).to_string(float_format=lambda x: f"{x:.4f}"))
    h = t[(t.statistic == "SUM") & (t.share == 0.10)].iloc[0]
    n = t[(t.statistic == "NAMED") & (t.share == 0.02)].iloc[0]
    P("")
    P(f"headline (SUM @ 10%): core EXACT-in-own-data {h.core_DATA_exact:.1%} vs non-core "
      f"{h.base_DATA_exact:.1%}, lift {h.lift_DATA_exact:+.1%}")
    P(f"NAMED @ 2% (the 14 most-NAMED runs): core EXACT-in-own-data {n.core_DATA_exact:.1%} "
      f"vs non-core {n.base_DATA_exact:.1%}, lift {n.lift_DATA_exact:+.1%}")
    P(f"console-inclusive EXACT leg at the headline: core {h.core_ANY_exact:.1%} vs "
      f"{h.base_ANY_exact:.1%}; the ANY-minus-DATA gap is the share of headline numbers "
      "that exist ONLY in a run's own printout.")
    t.to_csv(OUT / f"{STAMP}.exactleg.csv", index=False)
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

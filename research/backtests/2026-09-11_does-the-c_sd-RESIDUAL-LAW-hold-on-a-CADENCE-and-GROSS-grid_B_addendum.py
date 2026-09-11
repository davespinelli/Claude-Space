#!/usr/bin/env python3
"""Idea 539 ADDENDUM (lane B, 2026-09-11) - two DESCRIPTIVE splits demanded by the main run's
own output.  No new books are run: this reads the main run's committed .decomp.csv and
.slope.csv only, so it is exactly reproducible from the artefacts.

Neither split was pre-registered; both are reported as DESCRIPTIVE, not as bars.

A. G2 BY FAMILY.  The main run's G2 failed BOTH readings at once (median c_sd ratio 0.9994 /
   1.0008 -- nowhere near the queue's 0.667 / 1.333 -- but max |r-1| 0.335 / 0.340, far past
   the 0.05 invariance bar).  Both numbers cannot describe one population, so the ratio is
   re-cut by gate family.

B. THE CADENCE SPREAD OF beta/gross.  B2 passed on the pooled {W,M,Q} population and B3
   failed on daily.  Print beta/gross within each cadence at all three grosses so the two
   results can be read together: is the gross-normalisation that B2 vindicated stable INSIDE
   each cadence, and how far apart are the cadences themselves?

C. WHY WF-C CHANGED NO DECISION.  Count the OOS cells whose true 0-bps gap is positive.

Outputs: ._addendum.console.txt, ._addendum.g2family.csv, ._addendum.cadence.csv
"""
from pathlib import Path
import numpy as np
import pandas as pd

MAIN = Path(__file__).with_name(
    "2026-09-11_does-the-c_sd-RESIDUAL-LAW-hold-on-a-CADENCE-and-GROSS-grid_B")
OUT = Path(__file__).with_suffix("")
REF_GROSS = 0.75
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def fmt(df, p=6):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


def main():
    D = pd.read_csv(f"{MAIN}.decomp.csv")
    S = pd.read_csv(f"{MAIN}.slope.csv")
    key = ["panel", "family", "level", "cad"]
    IS = D[D.window == "IS"]
    base = IS[IS.gross == REF_GROSS].set_index(key)

    P("=" * 120)
    P("Idea 539 ADDENDUM - descriptive splits (NOT pre-registered bars)")
    P("=" * 120)
    P("\nA. G2 BY FAMILY: r_g = c_sd(gross=g) / c_sd(gross=0.75), per cell")
    rows = []
    for fam in ["MA-THRESH", "QUANTILE"]:
        for g in sorted(IS.gross.unique()):
            cur = IS[IS.gross == g].set_index(key)
            idx = [i for i in cur.index if i[1] == fam]
            r = cur.loc[idx].c_sd / base.loc[idx].c_sd
            rows.append(dict(family=fam, gross=g, n=len(r), c_sd_at_075=base.loc[idx].c_sd.mean(),
                             med_ratio=float(r.median()), max_abs_dev_from_1=float((r - 1).abs().max()),
                             expected_if_SCALES=g / REF_GROSS,
                             INVARIANT_at_0p05=bool((r - 1).abs().max() < 0.05),
                             SCALES_at_0p10=bool(abs(r.median() - g / REF_GROSS) <= 0.10)))
    A = pd.DataFrame(rows).set_index(["family", "gross"])
    P(fmt(A, 6))
    A.to_csv(f"{OUT}.g2family.csv")
    P("\n  READING: the MA-THRESH family -- the one that carries the whole residual (mean c_sd")
    P("  0.1213) -- is INVARIANT in gross to 1.1e-02 at both off-grosses, exactly as the")
    P("  construction c_t = k_t/n_t says.  The QUANTILE family -- whose c_t is near-constant by")
    P("  construction (mean c_sd 0.0047) and whose resid0 is ~0 by identity -- moves toward the")
    P("  queue's g/0.75 without reaching it (median 0.862 vs 0.667, 1.170 vs 1.333).  The main")
    P("  run's joint G2 failure is therefore entirely a QUANTILE artefact: the queue's premise")
    P("  is FALSE where the residual lives and only PARTLY true where c_sd is negligible.")

    P("\n" + "=" * 120)
    P("B. beta/gross WITHIN each cadence (from the main run's .slope.csv)")
    cad = S[S.cadset.isin(["W", "M", "Q", "D", "WMQ(535 population)"])]
    piv = cad.pivot(index="cadset", columns="gross", values="slope_over_gross")
    piv["span"] = piv.max(axis=1) - piv.min(axis=1)
    piv["rel_span"] = (piv["span"] / piv[[0.5, 0.75, 1.0]].mean(axis=1)).abs()
    P(fmt(piv, 4))
    piv.to_csv(f"{OUT}.cadence.csv")
    P("\n  READING: gross-normalisation holds INSIDE every cadence (relative span 0.7%-7.2%),")
    P("  but the cadences themselves are 15x apart: MONTHLY has essentially NO c_sd slope")
    P("  (beta/gross -0.235, t -0.42, R2 0.003) while W/D sit at -3.43/-3.35 and Q at -2.50.")
    P("  The pooled -1.5722 is an average over a population that is not homogeneous in the")
    P("  dial the queue asked about.")

    P("\n" + "=" * 120)
    P("C. WHY WF-C CHANGED NO DECISION")
    O = D[D.window == "OOS"]
    P(f"  OOS cells with a POSITIVE 0-bps gap (DEGROSS CAGR > RESPREAD CAGR): "
      f"{int((O.gap0_pp > 0).sum())} of {len(O)}")
    P(f"  max gap0_pp over all OOS cells: {O.gap0_pp.max():.4f} pp/yr   "
      f"median {O.gap0_pp.median():.4f}   min {O.gap0_pp.min():.4f}")
    P("  The sign the predictor is asked for is CONSTANT over the whole population, so any")
    P("  estimator with a negative fitted mean picks RESPREAD everywhere and scores exactly")
    P("  ALWAYS_RESPREAD.  WF-C's hit rate of 1.0000 is that identity, not skill.")

    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Addendum to idea 733-SIGNFLIP (lane B, 2026-09-11) -- the GROUP-COUNT confound in B2.

B2 compared the CANCEL rate on the record's real strata against ROWHALF/RANDOM2 controls that
always cut into EXACTLY TWO groups, while a real stratum can carry up to 12.  More groups means
more chances for two of them to disagree in sign, so part of the 1.28x could be arithmetic
rather than structure.  This addendum re-reads the committed quad table three ways:

  (1) k-MATCHED      restrict BOTH sides to quads whose stratum produced exactly 2 groups
                     (n_strata == 2).  The clean apples-to-apples ratio.
  (2) k-LADDER       CANCEL rate by number of groups, real vs control, so the arithmetic
                     component is visible rather than assumed.
  (3) PER-STRATUM k-MATCHED  the same ratio per stratum column, with n stated beside each --
                     the queue's own proposed reporting rule, applied to this run's numbers.

Reads only the committed artefacts of the main run; no prices, no backtests, deterministic.
Tunes nothing: the dials, flags and constants are the main run's.
Outputs: _addendum.kmatch.csv _addendum.controls.csv _addendum.console.txt
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

pd.set_option("display.width", 220)
pd.set_option("display.max_rows", 200)

MAIN = Path(__file__).resolve().parent / (
    "2026-09-11_is-the-c_sd-vs-TURNOVER-correlation-SIGN-FLIP-a-property-of-every-published-"
    "pooled-rho_B")
OUT = Path(__file__).with_suffix("")
CLAIMSETS = ["QUEUE", "CANON", "ALL"]
CONTROLS = ["ROWHALF", "RANDOM2"]
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


def main():
    Q = pd.read_csv(f"{MAIN}.pairs.csv.gz")
    P("=" * 150)
    P("ADDENDUM  idea 733-SIGNFLIP: is the real-vs-control CANCEL ratio a GROUP-COUNT artefact?")
    P("=" * 150)
    P(f"  quad table: {len(Q)} rows (the committed QUEUE+CANON subset), "
      f"{Q.block.nunique()} blocks.")
    rows = []
    for cs in CLAIMSETS:
        sel = Q[Q.claimsets.str.contains(cs, regex=False)].copy()
        if not len(sel):
            continue
        sel["side"] = np.where(sel.stratum.isin(CONTROLS), "control", "real")
        for me in sorted(sel.method.unique()):
            s = sel[sel.method == me]
            k2 = s[s.n_strata == 2]
            r_all = s[s.side == "real"].CANCEL.mean()
            c_all = s[s.side == "control"].CANCEL.mean()
            r_k2 = k2[k2.side == "real"].CANCEL.mean()
            c_k2 = k2[k2.side == "control"].CANCEL.mean()
            rows.append(dict(claimset=cs, method=me,
                             n_real=int((s.side == "real").sum()),
                             n_ctrl=int((s.side == "control").sum()),
                             CANCEL_real=r_all, CANCEL_ctrl=c_all,
                             ratio_raw=(r_all / c_all if c_all > 0 else np.nan),
                             n_real_k2=int(((k2.side == "real")).sum()),
                             n_ctrl_k2=int(((k2.side == "control")).sum()),
                             CANCEL_real_k2=r_k2, CANCEL_ctrl_k2=c_k2,
                             ratio_kmatched=(r_k2 / c_k2 if c_k2 > 0 else np.nan)))
    K = pd.DataFrame(rows)
    K.to_csv(f"{OUT}.kmatch.csv", index=False)
    P("\n(1) k-MATCHED RATIO (both sides restricted to stratifications with exactly 2 groups):")
    P(fmt(K.set_index(["claimset", "method"])))

    P("\n(2) k-LADDER -- CANCEL rate by number of groups the stratification produced:")
    Q2 = Q.copy()
    Q2["side"] = np.where(Q2.stratum.isin(CONTROLS), "control", "real")
    lad = Q2.groupby(["side", "n_strata"]).agg(n=("CANCEL", "size"), CANCEL=("CANCEL", "mean"),
                                               FLIP=("FLIP", "mean")).reset_index()
    P(fmt(lad[lad.n <= 10**9].set_index(["side", "n_strata"])))

    P("\n(3) PER-STRATUM, k-MATCHED (n_strata == 2 only), n stated beside every rate:")
    k2 = Q2[Q2.n_strata == 2]
    per = k2.groupby("stratum").agg(n=("CANCEL", "size"), blocks=("block", "nunique"),
                                    CANCEL=("CANCEL", "mean"), FLIP=("FLIP", "mean"),
                                    SIMPSON=("SIMPSON", "mean")).sort_values("CANCEL",
                                                                             ascending=False)
    P(fmt(per))
    ctrl_k2 = float(k2[k2.side == "control"].CANCEL.mean())
    P(f"\n  control (ROWHALF+RANDOM2) k-matched CANCEL rate = {ctrl_k2:.4f}; strata above it: "
      f"{int((per.CANCEL > ctrl_k2).sum())} of {len(per)}")

    P("\n(4) A CORRECTION TO THIS RUN'S OWN B2.  B2 pooled ROWHALF and RANDOM2 into one "
      "'control'.  They are not the same thing: rows inside a .grid.csv are written in DIAL "
      "ORDER, so ROWHALF is itself a real (ordinal) stratification, not a null.  RANDOM2 is the "
      "only true null here.  Both are quoted separately below, k-matched.")
    r4 = []
    for cs in CLAIMSETS:
        sel = Q[Q.claimsets.str.contains(cs, regex=False)].copy()
        sel = sel[sel.n_strata == 2]
        for me in sorted(sel.method.unique()):
            s = sel[sel.method == me]
            real = s[~s.stratum.isin(CONTROLS)].CANCEL.mean()
            rnd = s[s.stratum == "RANDOM2"].CANCEL.mean()
            rh = s[s.stratum == "ROWHALF"].CANCEL.mean()
            r4.append(dict(claimset=cs, method=me,
                           n_real=int((~s.stratum.isin(CONTROLS)).sum()),
                           CANCEL_real=real, CANCEL_RANDOM2=rnd, CANCEL_ROWHALF=rh,
                           ratio_vs_RANDOM2=(real / rnd if rnd > 0 else np.nan),
                           ratio_vs_ROWHALF=(real / rh if rh > 0 else np.nan)))
    R4 = pd.DataFrame(r4)
    P(fmt(R4.set_index(["claimset", "method"])))
    R4.to_csv(f"{OUT}.controls.csv", index=False)
    P("\n  READING: (a) the raw B2 ratio is part group-count arithmetic -- at matched k the "
      "real-vs-pooled-control ratio collapses to ~1.0 and goes BELOW 1 on Spearman; (b) against "
      "the TRUE null (RANDOM2) real strata do carry structure, several times the null rate; "
      "(c) but an arbitrary ordinal cut of the file (ROWHALF) finds MORE cancellation than the "
      "named strata do, so 'which stratum' is not a principled choice; and (d) the absolute rate "
      "is small on every reading.")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

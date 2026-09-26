#!/usr/bin/env python3
"""Plain-English facts about how events were dated, for RESULTS.md
(data/dating_summary.json). Reads data/events.parquet and data/candidates.parquet."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from common import DATA


def main():
    C = pd.read_parquet(DATA / "candidates.parquet")
    C["lag"] = (C.public_date - C.action_date).dt.days
    civ, dod = C[~C.dod], C[C.dod]
    src = C.date_src.value_counts().to_dict()
    lines = [
        "DoD awards (awarding agency Department of Defense) are dated action date + 90 days, the pre-registered rule, "
        "after checking that USAspending really holds DoD records back 90 days from the action date (on 2026-09-26 it had "
        "~11,000-15,000 DoD actions for each of 25-26 June 2026 and none for 27-29 June). "
        f"Of {len(dod):,} qualifying DoD actions, {int((dod.date_src == 'dod_late_entry').sum()):,} were entered into FPDS "
        "even later than that and are dated by their FPDS approval instead.",
        f"Civilian awards are dated by their FPDS approval date + 1 business day ({int((civ.date_src == 'fpds_approved').sum()):,} "
        f"of {len(civ):,} qualifying civilian actions; {int((civ.date_src == 'rule_no_fpds').sum()):,} not found in FPDS use the "
        "pre-registered action date + 5 business days). Median lag from signing to public date: "
        f"{np.median(civ.lag):.0f} days; {100 * (civ.lag > 10).mean():.0f}% took more than 10 days and "
        f"{100 * (civ.lag > 30).mean():.0f}% more than 30, because agencies report late. The pre-registered +5 business "
        "days would have used those before they were public.",
        "Caveat 1: DoD itself announces contracts of about $7M and up (currently $7.5M) on defense.gov on the award day, so many "
        "large DoD awards are public long before USAspending shows them. The DoD test therefore measures the reaction "
        "three months after awards that were often already public; it cannot say whether the first announcement moved the stock.",
        "Caveat 2: 'no 8-K within 5 trading days' is the pre-registered filter, but companies also announce awards by press "
        "release without an 8-K, and in the next 10-Q; neither is checked, so 'unannounced' overstates how hidden an award was.",
        "Caveat 3: USAspending labels each recipient and parent identifier with its current name. A parent's point-in-time "
        "identity is kept, but where the parent is the recipient itself only exact name matches to a listed company are used.",
    ]
    out = {"date_src_counts": src, "civ_lag_median": float(np.median(civ.lag)) if len(civ) else None,
           "civ_share_lag_gt10": float((civ.lag > 10).mean()) if len(civ) else None,
           "civ_share_lag_gt30": float((civ.lag > 30).mean()) if len(civ) else None, "lines": lines}
    (DATA / "dating_summary.json").write_text(json.dumps(out, indent=2))
    print("\n".join(lines))


if __name__ == "__main__":
    main()

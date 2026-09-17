#!/usr/bin/env python3
"""Companion to idea 1180's main script — reads its committed B_count_spread.csv and
answers the one question the measured ladder (S = 3..33) cannot answer directly:

    what seed count WOULD fix the published verdict count to within ONE cell?

Method, and its limits, stated plainly: fit log(spread) = a + b*log(S) over the five
measured seed counts and solve for spread = 1.  This is an EXTRAPOLATION, not a
measurement.  It is only credible where b is near the sqrt-N law (-0.5); where b is
flat the implied S is meaningless and is reported as such rather than quoted.
Deterministic; no backtest is re-run.
"""
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "research" / "backtests" / "2026-09-17_estimability-verdict-seed-stable_cloud.B_count_spread.csv"
S = np.array([3, 5, 9, 17, 33], float)

sp = pd.read_csv(SRC, index_col=[0, 1])
rows = []
print("fit log(spread) = a + b*log(S) over S = 3, 5, 9, 17, 33; solve spread = 1")
print("b near -0.5 is the sqrt-N law and the extrapolation is credible; b near 0 means")
print("the spread does not shrink with seeds at all and NO seed count fixes the verdict.\n")
for idx, row in sp.iterrows():
    y = np.log(row.values.astype(float)); b, a = np.polyfit(np.log(S), y, 1)
    need = float(np.exp(-a / b))
    credible = b <= -0.35
    rows.append(dict(verdict_set=idx[0], stat=idx[1], b=b, spread_at_33=int(row.values[-1]),
                     implied_S_for_1_cell=need if credible else np.nan, sqrtN_like=credible))
    print(f"  {idx[0]:10s} {idx[1]:7s} b = {b:+.3f}  spread(S=33) = {int(row.values[-1]):3d}  "
          + (f"implied S for <= 1 cell: {need:,.0f}" if credible
             else "NOT sqrt-N-like: the spread barely decays, no seed count fixes it"))
F = pd.DataFrame(rows)
F.to_csv(SRC.with_name(SRC.name.replace("B_count_spread", "B_seedcount_fit")), index=False)
cred = F[F.sqrtN_like]
print(f"\n  {len(cred)} of {len(F)} (verdict set, statistic) pairs decay like sqrt-N; for those the")
print(f"  implied seed count runs {cred.implied_S_for_1_cell.min():,.0f} to "
      f"{cred.implied_S_for_1_cell.max():,.0f}, against the record's 3 and idea 1170's 5.")

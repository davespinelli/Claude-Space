# PARK memo — idea 2237, exit-threshold band (lane C, 2026-09-22).  NOT RECOMMENDED FOR ADOPTION.

1. **The cell.** U56, 200d band with SPLIT edges `b_in = 0.03` (unchanged, the live entry edge) and
   `b_out = 0.20`, equal weight, gross 0.75, weekly, gated-out weight to CASH.  FULL 10.91% / 1.1553 /
   -17.50%; OOS (2017-2026) **11.04% / 1.1382 / -17.50%** vs SPY OOS 15.29% / 0.8751 / -33.72%.
   4b PASS in FULL and OOS at 0/10/25 bps (fails at 50); binding leg `none`.  4a FAIL everywhere.
2. **Why it is PARKed and not proposed.** At the same 10 bps rung, gross 1.00 on the LIVE symmetric
   band gives FULL 11.53% / 1.2009 / -15.91% and OOS 12.67% / 1.2760 / -15.91% — strictly better on
   CAGR, Sharpe AND drawdown in both windows, with no new parameter.  A dial that is dominated by an
   existing dial is not a finding.
3. **Chooser dependence.** Only 2 of 10 legal IS-only (panel, chooser) pairs reach a 4b-OOS cell, and
   0 of 5 on B136.  The record's habitual chooser (IS_SHARPE) misses on both panels.
4. **The one live qualification.** b_out is a TURNOVER dial: turnover falls 2.46 -> 0.85 turns/yr
   across the ladder, so at 25 and 50 bps `b_out = 0.25` is the only 4b cell left in the run.
5. **Exact RULES wording, IF a Sunday review ever adopts it (it should not on this evidence):**
   > **2. Band (v2.1).** Hold a name while its close is inside the 200-day moving-average band.
   > ENTER when the close is **above** `ma * 1.03`; EXIT only when the close is **below**
   > `ma * 0.80`; between the two edges, keep the previous state.  Before 200 closes exist the name
   > is OUT.  Gated-out weight goes to CASH and is never re-spread.
6. **What would have to be true first.** (a) the gross 1.00 comparand must be ruled out on a ground
   this run does not test (a real leverage/margin or capacity constraint), and (b) the 25/50 bps
   survival must be shown to be the deciding rung for real capital, not a tie-break.
7. **Survivorship (rule 9).** U56 and B136 are current-constituent lists.  A deep exit edge is
   exactly the dial such a panel flatters most — holding through a dip pays when the name is known
   to have survived.  Every level above is an upper bound.
8. **What this run cannot do (stated, not repaired).** One cadence (weekly), one entry edge (0.03),
   one gross for arm A (0.75), one sleeve composition (SPY).  The b_in x b_out interaction is idea
   2241's (lane B), not priced here.
9. **Grid.** All 176 (panel, arm, dial, cost) points are published in
   `2026-09-22_exit-threshold-dd-budget_C.grid.csv`; the walk-forward picks in `.walkforward.csv`.
10. **Status.** PARK.  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are untouched (rule 6).

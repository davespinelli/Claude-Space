# MEMO — 4b PARK candidate: top-20 with a rank no-trade band (idea 325, 2026-09-07 cloud)

1. **Cell.** U56 (research/universe.json), top-20 by the v1 composite with the vol scaler OFF,
   RULES v1 eligibility, NORM 75% gross, weekly, next-day execution, **no-trade band m = 20**.
2. **Numbers @10 bps.** 12.87% CAGR / Sharpe **1.112** / MaxDD **−17.22%**, H1/H2 **1.144/1.093**,
   OOS 2017– **1.187**, turnover **5.26x/yr** (vs 11.00x for the same book with m = 0).
3. **4b margins.** H1 +0.187, H2 +0.259, OOS +0.305, DD +3.01 pp, CAGR +2.21 pp — all five clear.
4. **Cost.** Still clears every 4b bar at **47 bps** (CAGR floor binds first); 25 bps reads
   11.98% / 1.043 / −17.32%.
5. **Why PARK not KEEP.** One panel (fails 4b on B136 on H2, 0.817 vs 0.834; fails everything on
   SMALL439); Sharpe monotone in m to the widest point tested; rule 8's IS chooser picks a
   different cell (n=5, m=10) at −0.122 regret.
6. **RULES wording if it is ever promoted — insert as clause 3 and amend clause 5:**
7. `3. **Selection:** rank every eligible name by the v1 composite (vol scaler off). A name is
   BOUGHT when its rank is 20 or better. A held name is SOLD only when its rank passes 40 or it
   leaves the eligible set; a rank between 21 and 40 is held, not sold. Free slots are refilled on
   the rebalance day by the best-ranked eligible name not already held, up to 20 names.`
8. `5. **Rebalance:** on the last trading day of each week only, apply clause 3, then reset every
   held position to 0.75/20 of NAV. Gate exits are not banded: a name that leaves the eligible set
   is sold in full that day regardless of rank.`
9. **Before promotion, required:** a second panel clearing 4b at the same (n, m), and an m sweep
   past 40 to show the argmax is interior rather than the grid edge (queued as idea 328).
10. **Do not promote at Sunday review on this evidence.** It is a one-panel PARK, filed for the
    record's cost-robustness column, not a capital candidate.

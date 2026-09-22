# KEEP-4b candidate memo — MONTHLY MADIST TOP-5 AT GROSS 0.50, idea 2109, 2026-09-22 cloud

1. **What it is.** Monthly: rank every eligible name by its distance to its own 200-day moving
   average, hold the top **5** at **0.10 of NAV each** (gross 0.50), the rest in cash. Eligible =
   close above the 200d MA and 20-day annualised vol below 0.60. No ranking on momentum, no band
   hysteresis, no vol scaler.
2. **Reached under rule 8** by 2 of the 7 legal IS-only choosers — IS_LEGS and IS_MINMARG, the
   two with the highest pooled reach in this very run — on U56 monthly; IS 2009–2016 chose,
   2017–2026 read exactly once. IS_SHARPE/IS_CALMAR/IS_CAGRSLACK pick 5|1.00 instead and fail.
3. **U56 FULL (10 bps):** 15.03% / 1.1966 / −16.62%, halves 1.2284 / 1.1768.
   **U56 OOS 2017–2026:** 16.11% / 1.2049 / −16.62% vs SPY 15.29% / 0.875 / −33.72%.
4. **B136 FULL (10 bps):** 17.87% / 1.2682 / −17.32%, halves 1.2172 / 1.3194.
   **B136 OOS:** 20.20% / 1.3341 / −17.32% vs SPY 15.26% / 0.874 / −33.72%. **It replicates.**
5. **4b legs (U56):** H1 1.2284 > 0.957, H2 1.1768 > 0.826, OOS 1.2049 > 0.875, MaxDD −16.62%
   inside the −20.23% cap (**margin +3.61 pp**), CAGR 15.03% above the 10.60% floor (**+4.43 pp**;
   OOS +5.41 pp). PASS on FULL and on OOS, on both panels.
6. **Cost-robust:** clears 4b FULL+OOS at **0, 10, 25 and 50 bps on both panels**. Idea 921 (same
   lane, same day, independent script) bisects its five-leg cost closing price at **76.9 bps
   (U56) / 68.7 bps (B136)** — 7x the protocol rung. The WEEKLY twin dies at 25 bps; cadence is
   load-bearing, so monthly is the candidate, not the family.
7. **4a FAILS** at every rung (MaxDD −16.6% against the live book's −12.1%, Sharpe 1.197 vs
   1.201): a 4b capital-path candidate only, per PROTOCOL rule 4's note that 4a kills growth.
8. **Known weaknesses.** It is a **5-name book** on a current-constituent panel: concentration
   risk is real and survivorship (rule 9) makes both LEVELS optimistic. Idea 914's clause (a DD or
   CAGR margin must exceed the book's own rebalance-offset spread) is **not tested here** — the
   DD margin is +3.61 pp against offset spreads the record has measured at ~3 pp on other books,
   so the clause is plausibly met but unproven for this one.
9. **RECORDED, NOT ADOPTED.** Rule 6: the live rules change only at a Sunday review, one change a
   week. Nothing in RULES.md, PROTOCOL.md, scan.py, bot.py or baseline.py was modified.
10. **Exact RULES wording if a Sunday review ever promotes it:**
    *"Clause 2 (selection): on the last trading day of each month, rank every instrument whose
    close is above its 200-day moving average and whose 20-day annualised volatility is below
    0.60 by the ratio of its close to that same 200-day moving average, highest first. Hold the
    top 5 at 0.10 of NAV each; hold no other instrument. If fewer than 5 qualify, hold those that
    do at 0.10 of NAV each. The remainder of NAV is cash and is never re-spread. Fill at the next
    close. Rebalance monthly."*

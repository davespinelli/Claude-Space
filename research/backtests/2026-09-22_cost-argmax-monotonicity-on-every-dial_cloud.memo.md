# MEMO — 4b KEEP-CANDIDATE, RECORDED NOT RECOMMENDED (idea 1621, lane cloud, 2026-09-22)

1. **Book.** U56 (research/universe.json), weekly, 200d-MA band with hysteresis at c = 0.12,
   equal weight over in-band names, total gross 0.75, out-of-band weight to CASH (never re-spread).
2. **Reached how.** It is the full-sample Sharpe argmax of the BAND ladder at 10 bps AND the rung a
   legal IS-only chooser (max 2009-2016 Sharpe) picks — the two agree, so rule 8 is satisfied.
3. **FULL (2009-01-13 -> 2026-09-18, 10 bps, t+1):** CAGR 13.95%, Sharpe 1.2218, MaxDD -19.42%,
   halves 1.2617 / 1.1959, turnover 1.93x/yr.
4. **OOS (2017-2026, read ONCE):** CAGR 15.03%, Sharpe 1.2581, MaxDD -19.42%.
5. **vs SPY:** FULL 15.14% / 0.8851 / -33.72%; OOS 15.29% / 0.8751 / -33.72%.  4b legs: Sharpe >
   SPY in both halves and OOS; MaxDD -19.42% <= 0.60 x -33.72% = -20.23%; CAGR 13.95% >= 0.70 x
   15.14% = 10.60%.  **All five legs clear.**
6. **vs live RULES v2 (weekly, 10 bps):** 8.62% / 1.2010 / -12.05%.  Path **4a FAILS** — the live
   book's MaxDD is shallower, and 4a is 0 of 24 across this whole run.
7. **Why NOT recommended.** It does not replicate off U56: on B136 the same rung gives 13.53% /
   1.1690 / -21.74% and fails 4b FULL; on SMALL the BAND argmax (c = 0.16) gives Sharpe 0.7882
   against SPY 0.8851 and fails every leg.
8. **And it is not new.** It is the band x gross family already priced by ideas 2119 and 923; 923
   found 112 of 810 U56 fine-grid points clearing 4b FULL and **0 of 2,430 clearing 4a**.  This run
   adds only that the rung is cost-invariant from 0 to 50 bps.
9. **Exact RULES wording IF a Sunday review ever adopts it** (it is not proposed here):
   *"Clause 2 (band). A name is IN when its close exceeds its 200-day moving average by more than
   12%, and OUT when its close falls more than 12% below that average; between those lines the
   previous state is held, and OUT applies until 200 closes exist. Hold every IN name at 0.75/N of
   NAV, N = the number of instruments priced that day; the weight of every OUT name is held in
   CASH and is never re-spread. Rebalance weekly, at the last trading day of each week, filled at
   the next close."*
10. **RULES.md, scan.py, bot.py and baseline.py were NOT modified.**  Survivorship: U56 is a
    current-constituent panel, so the CAGR and MaxDD levels above are optimistic.

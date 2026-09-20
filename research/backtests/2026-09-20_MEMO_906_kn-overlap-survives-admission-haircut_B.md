# MEMO — idea 906 (slug `...ADMISSION-HAIRCUT`), 4b KEEP-candidate REAFFIRMED: MEMO_887's U56 k/n book (lane B, 2026-09-20)

1. **The book is unchanged from MEMO_887** — this run adds a stress it had never faced, not a new
   book. U56 (`research/universe.json`), monthly, fills t+1, 10 bps, cash never respread.
2. **Exact RULES wording, if a Sunday review adopts it (verbatim from MEMO_887, g = 0.75):**
   *"Each month end, score every instrument by the mean of the cross-sectional percentile ranks of
   (t−21/t−252 − 1), (t/t−126 − 1) and (t/t−63 − 1), multiplied by 1.0 if the close is above its
   200-day mean and 0.5 if not, divided by the square root of its 20-day annualised volatility
   floored at 0.08. An instrument is ELIGIBLE if its close is above its 200-day mean and its 20-day
   annualised volatility is below 0.60. Hold the top k eligible names by score at GROSS/k of NAV
   each, where k = min(max(5, round(0.35 × n_eligible)), n_eligible). Any shortfall stays in CASH
   and is never respread. Rebalance monthly, fill next day."*
3. **Reproduction gate.** MEMO_887's committed numbers reproduce on today's tape to
   max |published − reproduced| **0.0037**: 11.65% / 1.1468 / −12.92% (g = 0.75) and
   15.60% / 1.1483 / −16.87% (g = 1.00), halves 1.241 / 1.070 and 1.243 / 1.071.
4. **What is NEW — it survives a point-in-time-shaped admission haircut.** Exiling names for a full
   year at 5% and 10% a year, with admitted breadth held flat, leaves 4b FULL **and** OOS passing at
   5 of 5 seeds for all three cut kinds, including the adversarial one that exiles the ex-post
   winners: WINNERCUT d = 0.10 reads **10.73% / 1.0873 / −12.78%**, OOS Sharpe **1.0856**.
5. **Rule 8 (params on 2009–2016 only, 2017–2026 read once).** Pooled over every breadth-matched
   haircut, the frozen cell clears 4b OOS on **0.867** of cells and the three IS-only choosers on
   0.689–0.844, against do-nothing RULES v2 at 0.111. Uncut OOS: **11.95% / 1.1291 / −12.92%**
   (g = 0.75) against SPY OOS 15.26% / 0.8737 / −33.72% and live RULES v2 OOS 9.46% / 1.2766 / −12.05%.
6. **The one NEW fragility, stated up front.** At a **20%/yr** winner exile the g = 0.75 rung falls
   through the 4b **CAGR floor** (9.73% against 10.59%) while g = 1.00 holds (12.99%). The 4b margin
   that dies first under this stress is CAGR, not drawdown.
7. **Breadth, not survivorship, is the binding dial.** Drop-only haircuts (admitted 55 → 15) take the
   ladder's 4b rate 0.750 → 0.100 and the frozen cell's rule-8 OOS pass rate to 0.333; the DD cap is
   the leg that goes. Any live sizing of this book must state the admitted-name count it assumes.
8. **Not a cross-panel fact.** The same stress KILLS the B136 arm: breadth-matched WINNERCUT clears
   0 of 120 book-cells at every rate. Adopt on U56 or not at all.
9. **SURVIVORSHIP, still open in one direction.** This haircut can only remove observed names; it
   cannot add index members deleted before today, whose series are not in `data/`. `universe.json`
   is a CURRENT constituent list, so every level here is optimistic and both 4b bars are easier than
   on a point-in-time panel. 2020 and 2022 are the only stress episodes in the window.
10. **Rule 6.** This is not a rules change. MEMO_887's candidate stands, at **g = 0.75**, with this
    run's fragility (item 6) and breadth caveat (item 7) attached to it.

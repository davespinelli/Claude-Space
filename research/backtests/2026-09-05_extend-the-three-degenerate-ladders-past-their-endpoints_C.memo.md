# Memo — idea 218 by-product, NOT proposed (Sunday review, 2026-09-05, lane C)

1. **The by-product.** U56 + a 12% re-entry band on the 200d gate (BAND=0.12, an ADDED ladder
   point) passes 4a **and** 4b: full 13.8% / 1.149 / −18.2%, halves 1.138 / 1.162, OOS 1.223 /
   15.5% / −18.2%, turnover 7.7×/yr vs the incumbent band-0 book's 9.5×.
2. **Why it is not proposed (1):** it is single-universe. B136 and BSTK100 produce no 4b-passing
   BAND row at any width — idea 53's failure mode exactly, and idea 44's.
3. **Why it is not proposed (2):** 0.12 is the argmax of the very 8-point ladder this run says
   should not be fitted; the honest arm is the corpus mode, which is also 0.12 but at a 30.2%
   modal share — below the concentration idea 219 is queued to floor.
4. **Why it is not proposed (3):** idea 58 already killed the band gate between 10 and 25 bps.
   No cost ladder was run here, so its survival at 15/20/25 bps is unmeasured.
5. **Exact RULES wording IF a future run clears 2–4** (cross-universe, cost ladder, modal-share
   floor), for the eligibility clause only — nothing else in RULES v1 changes:

   > **Eligibility.** A name is eligible when its close is above its 200-day moving average by
   > more than 12%, and becomes ineligible only when its close falls more than 12% below that
   > average; between those thresholds the previous eligibility state is carried forward. The
   > 20-day annualised volatility gate (`vol20 < 0.60`) is unchanged.

6. This replaces the bare `close > 200d MA` test with a symmetric ±12% band and a carried state.
   It is **one** new constant, not a per-book fit.
7. It cuts flips (turnover 9.5 → 7.7×/yr) and is the mechanism idea 57/61 measured, at a width
   two steps beyond where idea 171 stopped looking.
8. **GROSS must not follow it into RULES at any level above 1.00.** A 2%/yr borrow charge moves
   100% of the levered picks back to 1.00 and improves the OOS Sharpe of the pick.
9. **SLEEVE must not follow it either:** f ≥ 0.35 buys Sharpe and loses 4b's CAGR floor in 52 of
   53 books.
10. Action requested at Sunday review: **none.** Recorded so a later cross-universe + cost-ladder
    run has the wording and the three blockers already written down.

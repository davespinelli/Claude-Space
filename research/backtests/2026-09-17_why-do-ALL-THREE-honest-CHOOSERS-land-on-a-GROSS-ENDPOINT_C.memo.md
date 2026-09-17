# MEMO — 4b KEEP-candidate, idea 1154, lane C, 2026-09-17 (proposed for Sunday review, NOT enacted)

1. **What passes.** The standing top-20 / W / min-hold-126 book at **gross 0.625 (U56)** and
   **0.575 (B136)** clears PROTOCOL path **4b on the full sample AND out of sample** at 10 bps:
   U56 12.96% / 1.1393 / −16.12%, halves 1.2034 / 1.0966, OOS 14.10% / 1.1639 / −16.12%, 2.43x/yr;
   B136 12.29% / 1.0620 / −16.18%, halves 1.2884 / 0.8829, OOS 12.30% / 1.0084 / −16.18%, 2.52x/yr.
   Bars: SPY halves 0.9588 / 0.8207, OOS 0.8711, MaxDD cap −20.23%, CAGR floor 10.57%. **4a fails (0 of 132).**
2. **What is actually new is the SELECTOR, not the book.** The book is the family the record
   already holds and PARKED; 1150 showed the whole 0.525..0.775 window passes and is one book scaled.
   What 1154 adds is that the gross can be **chosen IS-only (2009..2016) and still pass OOS**, which
   1150 reported as impossible for its three choosers (0 of 48).
3. **Exact RULES wording, if the Sunday review wants the selector** (clause added, nothing replaced):
   > *"GROSS is not asserted. Once a year on the first rebalance of January, set gross to the rung of
   > {0.20, 0.225, ... 1.00} that maximises, over the trailing history ending on the prior 31 December,
   > the MINIMUM of the three 4b margins: (Sharpe − SPY Sharpe)/|SPY Sharpe|, (0.60·|SPY MaxDD| − |MaxDD|)/(0.60·|SPY MaxDD|),
   > and (CAGR − 0.70·SPY CAGR)/|0.70·SPY CAGR|. Hold that gross for the year; the remainder is cash."*
4. **Why it reaches the interior when the other four choosers cannot.** Over the gross ladder the IS
   Sharpe margin is flat (0.2353 → 0.2377), the drawdown margin falls monotonically (+0.7127 → −0.3903)
   and the CAGR margin rises monotonically (−0.6485 → +0.7738). A **min of two oppositely-sloped monotone
   legs is a tent**, and a tent peaks in the interior: need = −0.496 = **−3.04 paired-bootstrap SD** (U56),
   −0.606 = −3.43 SD (B136). A ratio is not enough — C_ISMAR is still monotone and still picks 1.00.
5. **The honest discount.** C_IS4B maximises IS versions of the very legs 4b later tests, so the
   full-sample pass is partly tautological. The non-tautological part is the OOS pass, which the
   chooser could not see, and B136, where the incumbent 0.75 **fails** 4b (−20.74% against the −20.23% cap)
   while the selected 0.575 passes.
6. **The size of the prize is small and must not be oversold.** U56 full Sharpe at gross 0.575 / 0.625 / 0.750
   reads 1.1391 / 1.1393 / 1.1397 and OOS Sharpe 1.1637 / 1.1639 / 1.1644. The selector buys **drawdown
   headroom, not return per unit risk**: it trades CAGR for MaxDD one-for-one along 1150's identity.
7. **Rule 8 status: satisfied by construction.** Every parameter is read on 2009-01..2016-12-31 and the
   2017-01..2026-09-15 window is untouched. 50 such picks were made across 5 choosers x 5 dials x 2 panels
   and all 50 are published, passing and failing alike (5 pass 4b, 0 pass 4a).
8. **Survivorship (rule 9).** U56 and B136 are current-constituent panels; both 4b exposure legs are
   measured against an inflated book and the bias does **not** cancel out of the pass/fail table.
   Treat the LEVELS as optimistic and the rung-to-rung comparisons as sound.
9. **Cost and capacity.** 10 bps, next-day execution, 2.43x/yr turnover, no shorting, no leverage,
   20 names equal-weight, cash remainder uninvested (no financing or cash yield modelled either way).
10. **Recommendation: PARK, do not promote this week.** The book is not new, the selector's edge over the
    asserted 0.75 is one drawdown leg on one panel, and rule 6 allows one change per week decided on Sunday.
    The selector is worth re-testing on a third panel and on a rolling (not one-shot) IS window first.

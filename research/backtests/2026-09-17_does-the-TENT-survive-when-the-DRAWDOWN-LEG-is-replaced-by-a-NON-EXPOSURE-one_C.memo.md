# MEMO — 4b KEEP-candidate, idea 1166, lane C, 2026-09-17 (proposed for Sunday review, NOT enacted)

1. **What passes.** The standing top-20 / W / min-hold-126 book with gross chosen IS-only by the
   **VOL-TARGET** variant of 1154's tent chooser — min(M_S, **M_VOLTGT**, M_CAGR), M_VOLTGT =
   (SPY IS vol − book IS vol)/SPY IS vol — picks **gross 0.775 (U56)** and **0.675 (B136)** and clears
   PROTOCOL path **4b on the full sample AND out of sample** at 10 bps: U56 16.10% / 1.1398 / −19.72%,
   halves 1.2038 / 1.0972, OOS 17.54% / 1.1645 / −19.72%, 2.99x/yr; B136 14.43% / 1.0628 / −18.81%,
   halves 1.2893 / 0.8838, OOS 14.43% / 1.0093 / −18.81%, 2.93x/yr. Bars: SPY halves 0.9588 / 0.8207
   (U56) and 0.9596 / 0.8259 (B136), OOS Sharpe 0.8711 / 0.8767, MaxDD cap −20.23%, CAGR floor 10.57%
   (U56) / 10.61% (B136). **4a fails, 0 of 132 cells and 0 of 40 picks.**
2. **Exact RULES wording, if the Sunday review wants it** (a clause added; nothing replaced):
   > *"GROSS is not asserted. Once a year, on the first rebalance of January, set gross to the rung of
   > {0.20, 0.225, … 1.00} that maximises, over the trailing history ending on the prior 31 December, the
   > MINIMUM of these three margins: (Sharpe − SPY Sharpe)/|SPY Sharpe|, (SPY annualised vol − annualised
   > vol)/SPY annualised vol, and (CAGR − 0.70·SPY CAGR)/|0.70·SPY CAGR|. Hold that gross for the year;
   > the remainder of NAV is cash."*
3. **It is the same object as 1154's, one leg over.** Swapping the drawdown cap for a vol target moves
   the pick from 0.625/0.575 to 0.775/0.675 and buys CAGR (16.10% vs 12.96% on U56) at a deeper but still
   compliant drawdown (−19.72% vs −16.12%, cap −20.23%). Both legs are **degree-1 exposure objects**
   (measured slopes in gross: |MaxDD| +0.979, vol +1.001), which is why both give a **resolvable** tent:
   the peak stands +2.15 / +2.66 SD above the far endpoint (L_DD: +2.81 / +3.52 SD).
4. **This run's own reason not to prefer it.** The vol-target pick sits **one rung inside the top of
   1150's passing window (0.525..0.775 on U56)**, so it has the least headroom of any passing rung: at mult
   1.25 of the same clause the pick walks to 0.975 and fails. The drawdown-cap version picks mid-window.
   Prefer 1154's L_DD wording if either is ever enacted; this one is reported because it passes, not
   because it is better.
5. **The honest discount, restated from 1154 and still binding.** The chooser maximises IS versions of
   the very legs 4b then tests, so the full-sample pass is partly tautological. The non-tautological parts
   are (i) the OOS pass, which the chooser could not see, and (ii) **B136, where the asserted incumbent
   0.750 fails 4b (−20.74% against the −20.23% cap) while the selected 0.675 passes**.
6. **The prize is small and must not be oversold.** U56 full Sharpe across the whole 33-rung gross ladder
   runs 1.1391 → 1.1398 and OOS Sharpe 1.1637 → 1.1645. On U56 the **frozen live gross 0.750 already clears
   4b full+OOS** and 11 of 33 rungs do, so the selector buys **nothing on U56**; it trades CAGR for MaxDD
   one-for-one along 1150's exposure identity.
7. **Rule 8: satisfied by construction.** Every parameter is read on 2009-01..2016-12-31 and the
   2017-01..2026-09-15 window is untouched. 40 such picks were made across 4 legs × 5 dials × 2 panels and
   all 40 are published, passing and failing alike (7 clear 4b full+OOS, 0 clear 4a).
8. **Survivorship (rule 9).** U56 and B136 are current-constituent panels; the exposure legs are measured
   against an inflated book and the bias does not cancel out of the pass/fail table. Treat the LEVELS as
   optimistic and the rung-to-rung comparisons as sound. Price vintage pinned at 2026-09-15; the same
   reproduction gate reads 39.4x worse unpinned, off one extra bar.
9. **Cost and capacity.** 10 bps, next-day execution, 2.99x/yr turnover (U56) and 2.93x/yr (B136), no
   shorting, no leverage, 20 names equal-weight, cash remainder uninvested — no financing cost and no cash
   yield modelled in either direction.
10. **Recommendation: PARK, do not promote this week.** The book is not new, the selector is 1154's with a
    different degree-1 leg, its edge over the asserted 0.750 is one drawdown leg on one panel, and it is the
    least robust member of the family to its own threshold. 1161 has already tested the rolling-window
    version of 1154's clause; the open question for either wording is a **third panel**, not another leg.

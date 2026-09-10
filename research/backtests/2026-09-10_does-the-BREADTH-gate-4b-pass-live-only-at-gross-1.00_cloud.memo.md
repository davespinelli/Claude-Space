# Memo — idea 585: BREADTH-DG q=0.20 on U56 (4b KEEP-candidate, 2026-09-10, cloud)

1. **Candidate:** idea 581's PARKed book, now priced on its exposure dial. Equal-weight every
   priced name in `research/universe.json` at gross g/N; send the whole book to cash when market
   breadth is in its bad tail. Weekly, t+1, 10 bps.
2. **What this run adds:** the 4b pass is **not** the single point g = 1.00 that idea 581
   published. On a 17-rung ladder (0.20..1.00) it is a **contiguous band [0.70, 1.00], 7 rungs**
   on U56 and [0.75, 1.00], 6 rungs on B136. Idea 311's g-band loophole does **not** apply.
3. **The gate, not the gross, makes the band.** The gate-less equal-weight control at matched
   gross clears 4b at **1 of 17** rungs on U56 and **0 of 17** on B136.
4. **Numbers, 10 bps, weekly, t+1, U56, q = 0.20** — g 1.00: 15.99% / 1.257 / −16.48%, halves
   1.187 / 1.354, OOS 16.35% / 1.453 / −14.16%. g 0.75: 11.92% / 1.256 / −12.57%, halves
   1.186 / 1.356, OOS 12.16% / 1.455 / −10.76%. vs **SPY** 15.15% / 0.886 / −33.72% (halves
   0.959 / 0.826, OOS 0.876) and **RULES v2** 8.63% / 1.202 / −12.05% (OOS 1.279).
5. **4b passes on all five legs at every rung in the band; 4a fails at every rung** (U56 0/68) —
   the book's MaxDD is worse than RULES v2's −12.05% inside the band, and its H1 Sharpe is below
   v2's at the rungs where the drawdown would clear.
6. **Rule 8 was run properly** and both pre-stated conventions pick **q = 0.20** on both panels:
   max-IS-Sharpe picks g = 1.00 (U56 OOS 1.453, B136 OOS 1.155), an IS-only 4b screen picks
   g = 0.75 on U56 (OOS 1.455, still 4b PASS). Both U56 picks land inside the band.
7. **The one real weakness:** on B136 the IS-4b-screen convention picks g = 0.60, one rung below
   that panel's band, and it fails the 4b CAGR floor. The U56 result does not depend on the
   convention; the B136 result does. **B136 stays PARK.**
8. **Why it is not a level artefact:** Sharpe is flat in g (1.255 → 1.257) because de-grossed cash
   is held at 0%, so all three Sharpe legs clear by wide, g-invariant margins (OOS +0.58). Only
   the CAGR floor and DD cap move with g, and the band is exactly where they overlap.
9. **Survivorship:** `universe.json` is a current-constituent list, so the LEVELS — including the
   CAGR margin, which is the binding leg — are biased up. The band's SHAPE is within-panel and is
   not. Cash is credited at 0%, which understates CAGR at every rung below 1.00.
10. **Exact RULES wording if a Sunday review promotes it** (do NOT apply now; PROTOCOL rule 6):
    *"Hold every name priced today at gross 0.75 / N of NAV, N = names priced that day. Compute
    breadth as the fraction of those names trading above their own 200-day moving average. If
    breadth is below its trailing 5-year 20th percentile (1260 trading days, minimum 504) at
    today's close, hold no equities and stay in cash; otherwise hold the equal-weight book.
    Rebalance weekly on the last trading day of the week, executed at the next close."*
    (g = 0.75 is the rung the conservative rule-8 convention selects and sits inside the band on
    both panels; g = 1.00 is the higher-CAGR end of the same band and clears 4b identically.)

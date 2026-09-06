# Idea 273 — turnover-budget-the-broad-ranked-book (lane B, 2026-09-06)

**ANSWERED — the queued test passes, and in the STRONGER direction than it was asked. No KEEP: 4a 0 of 135, 4b 4 of 90 on the broad panel and all four are islands the rule-8 selector does not pick. PARK.**

Script `2026-09-06_turnover-budget-the-broad-ranked-book_B.py`; console `.console.txt`; every grid point in
`.grid.csv` (135 rows), the H2 attribution per cell in `.split.csv`, the walk-forward in `.walkforward.csv`.

## Three reproduction gates, all passed before any new number was read

1. **idea 66's published broad `top20-200d`, 6/6 EXACT**: 13.11% / 0.9581 / -20.05%, halves 1.1246 / 0.8135, SPY H2 0.8366.
2. **The state machine nests the parent**: at (m=0, j=uncapped) `max|weight diff|` on rebalance rows and
   `max|daily return diff|` are both **0.0e+00**. This required carrying one parent quirk verbatim — on 7 of 975
   rebalance dates a 3-way tie at rank 20.0 makes `rank <= 20` select 21 names at gross 0.7875 — so the target book
   size on a date is the parent's own `|{rank <= NPOS}|`, not the constant 20.
3. **idea 70's H2 split, 4/4 MATCH**: SEL +0.1144 (pub +0.1145), BILL -0.0979 (pub -0.0979), UND -0.0395
   (pub -0.0395), dS -0.0231 (pub -0.0231), identity residual 8.3e-17, k = 1.2888. Idea 70's boundary prices
   underinvestment at the STATIC mean gross; the exact time-varying boundary moves 0.0456 from UND into SEL
   (SEL +0.1600 / UND -0.0851) with BILL and dS unchanged. Both are reported; the queued question is worded in
   idea 70's, so that is the one the pass/fail bar uses.

## The queued test: can -0.0979 be halved for less than +0.05 of lost selection? YES, 24 of 45 cells

| | parent | m=0,j=1 | m=15,j=5 | m=999 (hold till ineligible) |
|---|---|---|---|---|
| turnover/yr | 13.78x | 6.27x | 6.19x | **3.46x** |
| H2 BILL | -0.0979 | -0.0443 | -0.0440 | -0.0291 |
| H2 SEL | +0.1144 | +0.1078 | +0.1136 | -0.0584 |
| full Sharpe @10bps | 0.958 | 1.033 | 1.032 | **1.061** |
| full Sharpe @25bps | 0.809 | 0.967 | 0.966 | **1.020** |
| MaxDD | -20.05% | -20.47% | -19.73% | **-17.57%** |

The bill is halved in **30/45** cells and 24 of those cost **≤ 0.05** of selection. The stronger fact is the sign:
the slope `d(SEL)/d(BILL saved)` across the 44 budgeted cells has **median -0.399, mean -0.949** — selection mostly
*improves* as churn is removed, so the weekly re-ranking was not buying alpha, it was paying to shed it.
`corr(turnover, full Sharpe) = -0.946` @10bps and **-0.986** @25bps, monotone in the right direction at both rungs,
across a realised-gross span of only 0.0028 (0.7390-0.7418), so this is not a gross comparison (idea 274's test).
H2 dSharpe vs SPY turns positive in 17/45 cells (best +0.0307 at m=30, j=5) against the parent's -0.0231.
Max identity residual over all cells 3.5e-16.

## Why it is still PARK, not KEEP

* **4a: 0 of 135.** Every cell is a -18% to -21% drawdown book against the live RULES v2's -12.2%, and none reaches
  v2's 1.107 Sharpe. The turnover budget does not touch the live book.
* **4b: 4 of 90 on broad** (m=5/j=2 and m=15/j={3,5,uncapped}, all @10bps, 0 of 45 @25bps) — and each is an
  **island**: H2 margins of **+0.002 to +0.014** over SPY, MaxDD margins of **+0.07 to +0.50 pp** under the
  20.23% bar, and **0-2 of 8 grid neighbours pass**. Idea 171's disqualification pattern exactly.
* **Rule 8 does not land on them.** Fitted on 2009-2016 alone the IS pick is **m=999, j=1** at both rungs
  (IS Sharpe 1.2580 vs the parent's 1.0438). Its 2017-2026: 11.97% / **0.918** / -17.57% against the parent's
  12.52% / 0.894 / -20.05%, RULES v2's 8.01% / **1.122** / -12.24% and SPY's 15.50% / 0.884 / -33.72%. So
  dOOS is **+0.024 vs the parent and +0.034 vs SPY, but -0.203 vs the live book**, and at 25 bps it is -0.009 vs
  SPY. The IS pick **fails 4b on H2** (0.775 vs 0.837): the honest chooser buys the turnover cut and misses the
  4b island. Spearman(IS, OOS) over the 45 cells is +0.330 @10bps / +0.547 @25bps, and IS-best is never OOS-best.
* **The transfer panel is not the confirmation it looks like.** On u56 all 45 cells clear 4b — but so does the
  **un-budgeted parent** (m=0, j=uncapped: 12.67% / 1.093 / -18.31%), so 4b passage there is a property of
  `top20-200d` on u56, already in the record, not of the budget. The budget still improves that book materially
  (m=999: 11.90% / **1.142** / **-12.79%** at 3.49x/yr, OOS 1.210 vs SPY's 0.884), and rule 8 on u56 picks
  m=30/j=1 (OOS 13.26% / 1.199 / -14.78%, +0.314 vs SPY, -0.090 vs v2, clears 4b) — but **Spearman(IS, OOS) is
  +0.010** there, i.e. the selector carries no information and the pass is the plateau's, not the pick's.
* Pre-registered caveat, restated: 2017-2026 is ~H2, so the rule-8 OOS bar and the 4b H2 bar overlap almost
  completely (idea 111). That weakens every OOS number above rather than strengthening it.
* SURVIVORSHIP: both panels are current constituents, so absolute CAGR/Sharpe are optimistic. Every comparison
  here is between arms on the same panel and the same days.

## Exact wording, if a future Sunday review ever revisits this (NOT proposed for adoption)

> Ranked books rebalance on a **buffer**, not on the rank: a name enters only in the top 20 of the composite, and
> a held name is sold only when it leaves the 200d/vol eligibility gate or its composite rank passes **20 + m**.
> At most **j** rank-driven replacements per rebalance; gate-driven exits are never capped.

## What this does hand the record

A general, cheap screening result rather than a book: on the ranked family, **turnover and Sharpe are strongly
negatively related at both cost rungs and on both panels** (-0.946 / -0.986 broad, -0.668 u56), and the mechanism
is not the cost bill alone — cutting churn recovers selection too. Any ranked candidate the record has priced at
its natural cadence has been priced at the *wrong* end of that curve.

## Follow-ups queued

* 275 — does the buffer beat the cadence dial at the same realised turnover?
* 276 — is the m=999 u56 book (11.90% / 1.142 / -12.79% at 3.49x/yr) a 4b candidate in its own right?
* 277 — re-price every ranked KEEP-candidate in the record at its Sharpe-maximising turnover.

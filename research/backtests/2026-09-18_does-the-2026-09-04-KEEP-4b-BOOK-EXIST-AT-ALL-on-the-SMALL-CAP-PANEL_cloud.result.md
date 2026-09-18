# Idea 1288 (lane cloud, 2026-09-18) — does the 2026-09-04 KEEP-4b BOOK EXIST AT ALL on the SMALL-CAP PANEL?

**ANSWERED: (B) PANEL FACT. KILL on SMALL.** The 2026-09-04 recipe clears 4b at **0 of 42**
(N, gross) cells on the 663-name sub-$2B panel, while clearing at **21 of 42** on U56 and
**19 of 42** on B136. The incumbent is a property of the mega-cap/ETF tape it was found on.

## What was run
126 real books: N {5,10,15,20,25,30} x GROSS {0.55..0.85 step 0.05} on three panels, every
cell published in `.grid.csv`. Frozen at the committed construction: H=126-row min hold,
weekly Fri decision applied t+1, 10 bps, above-200d & vol20<0.60 eligibility, 3-leg composite,
equal weights, 260-row warm-up, cash at 0%. Two dials, no more (rule 4).

**ANCHOR REPRODUCED.** U56 / N=20 / g=0.65 reads 13.66% / 1.1526 / -16.73%, OOS 14.95% /
1.1833 — idea 1293's certified uncapped cell to **max |d| 4.8e-05** across all five committed
figures. Every panel comparison below sits on that check.

## The numbers
| panel | best full Sharpe | SPY (same days) | best J_FULL | 4b PASS | 4a PASS |
|---|---|---|---|---|---|
| U56 | 1.1712 (N=15, g=0.60) | 0.8848 | +3.05 pp | 21/42 | 0/42 |
| B136 | 1.0990 (N=25, g=0.85) | 0.8861 | +3.82 pp | 19/42 | 0/42 |
| **SMALL** | **0.5246** (N=25/30) | **0.8581** | **-6.79 pp** | **0/42** | **0/42** |

## It is not a sizing problem, and that is the point
On U56 and B136 the 4b failures are a **drawdown** story: the MaxDD cap binds on 21/21 and
23/23 failures and is the **SOLE** binder on 21 and 16 of them — de-gross and the cell passes.
On SMALL **all five legs fail at all 42 cells**: H1 Sharpe, H2 Sharpe, OOS Sharpe, the MaxDD
cap and the CAGR floor, simultaneously, at every N and every gross. No leg is ever a sole
binder because none of them is ever the only one broken. There is no rung of size that repairs
this; outcome (C) RESIZABLE is refuted, not merely unselected.

## Rule 8, 2017-2026 read once
Both dials chosen on warm-up..2016-12-31 only by IS joint margin (idea 1290's chooser, ties to
lower gross then lower N). SMALL picks **N=30 / g=0.55**: full 5.97% / 0.5245 / -27.72%,
halves 0.7564 / 0.3519, **OOS 5.22% / 0.4517 / -27.72%** against SMALL-panel SPY OOS 15.33% /
0.8767 / -33.72% and live RULES v2 OOS 4.47% / 0.6516 / -12.18%. It loses to SPY on every leg
and loses to the live book on Sharpe and drawdown while barely beating it on CAGR. U56 picks
N=15 / g=0.60 (OOS 15.14% / 1.1952 / -16.38%, 4b PASS) and B136 picks N=25 / g=0.60 (OOS
13.39% / 1.0629 / -17.56%, 4b PASS) — both 4b passes, neither promoted here (rule 6, and
neither is stress-run).

## Corroboration, stated as such
Idea 1215 (lane C, same day) read SMALL 0 of 66 on an overlapping grid with a wider gross
ladder. This run is an independent build of the same recipe and agrees; the new content is the
**per-leg** decomposition above, which says the SMALL failure is not the drawdown leg the
U56/B136 failures are.

## Not claimed
That any cell here is a new candidate book (the recipe is the committed one, re-priced, never
re-tuned); that the small-cap panel is untradeable for some other rule; that anything in
RULES.md changes (rule 6).

## Survivorship (rule 9)
Current constituents only on all three panels; SMALL additionally drops 52 tickers with
`max_1d_move >= 1.0` from `data/small_meta.csv`, leaving 663. The bias is **worst on SMALL** —
small caps delist and go bankrupt far more often than mega caps — so SMALL's readings here are
an **upper bound** on what the recipe would have earned, and a KILL on SMALL is the stronger
reading, not the weaker one. Nothing here is a live expectancy.

Script: `research/backtests/2026-09-18_does-the-2026-09-04-KEEP-4b-BOOK-EXIST-AT-ALL-on-the-SMALL-CAP-PANEL_cloud.py`

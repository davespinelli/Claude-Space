# Idea 1203 (lane cloud, 2026-09-18) — does the TIE-BREAK STATISTIC matter once the TIE is DECLARED?

**ANSWERED: YES, AND MORE THAN THE BOUND FORM DOES. A PUBLISHING CLAUSE MUST *NAME* THE
TIE-BREAK, NOT MERELY REQUIRE ONE. CAPITAL VERDICT: KILL — no new book, nothing enacted.**

## What was run
The frozen bound form is **B_ONE** (gate G6a: B_ONE and B_CP declare a bit-identical tie set at
all 4,320 rows, so the result transfers to both). Dial 1 = tie-break statistic, 8 rungs; dial 2 =
K in {10, 25, 50, 100, 200, 400}. Three panels, 1199's own 36 books (N in {5,10,15,20,30,40} x
cadence {W,M}), 20 seeds per cell, 162 published picks. Every rung decides on
warm-up..2016-12-31 only; 2017-2026 read once. `.walkforward.csv`, `.books.csv`, `.grid.csv`,
`.tiesets.csv`, `.decomposition.csv`, `.mechanism.csv`, `.gates.csv`, `.console.txt`.

"First-wins" here means 1199's own order, `sort_values(["cadence","N"])` — cadence ascending as
a string (M before W), then N ascending. Getting that order wrong changes B_POINT's pick from
N=5/M to N=5/W and moves the gap; it is stated because it is inherited, not chosen (idea 1202
asks whether it is really the record's habit and this run does not settle that).

## The numbers (pooled mean OOS Sharpe of the pick, 18 (panel, K) cells)
| rung | pooled | gap vs B_POINT | mean N of pick |
|---|---|---|---|
| T_HOLD (largest N) | 0.9995 | **+0.1086** | 34.7 |
| T_LAST (order only) | 0.9968 | +0.1059 | 34.7 |
| T_IS4B (IS 4b margin) | 0.9818 | +0.0909 | 28.9 |
| T_CH_Z (**1199's choice**) | 0.9592 | +0.0683 | 21.1 |
| T_RANDOM ("merely require one") | 0.9362 | +0.0453 | 19.4 |
| T_FIRST = B_POINT | 0.8909 | +0.0000 | 8.9 |
| T_ISSHARPE | 0.8902 | -0.0006 | 10.0 |
| T_NULLGAP | 0.8793 | **-0.0116** | 10.8 |

- The reference gap is replayed at **+0.0683** (1199 committed +0.0671; the difference is the
  U56 tape vintage, below).
- **The worst legal choice reverses it**: T_NULLGAP is -0.0116, i.e. **-16.9%** of the gap. Two
  of the five *informative* statistics the queue named (T_ISSHARPE, T_NULLGAP) destroy it.
- The **spread across the eight rungs is 0.1201 — 1.76x the gap it decomposes.** Outcome (C) of
  the four pre-declared outcomes fires, with (B) partially: the choice of tie-break is a larger
  free parameter than the convention it was introduced to repair.
- Declaring the tie and breaking it at random buys +0.0453, i.e. two thirds of CH_Z's gap. So a
  clause that merely *requires* a tie-break captures most of the average but leaves the author
  a +/-0.12 range it cannot police.

## The mechanism — the winning rungs are not reading the tie, they are holding more names
rank corr(mean N of the rung's pick, its gap vs B_POINT) = **+0.844** over the 9 rungs. T_LAST
carries *zero* information (it is a position in a sort order) and picks the same book as T_HOLD
at **15 of 18** (panel, K) cells, scoring +0.1059 against +0.1086. Both land on the largest-N
weekly book, and U56's OOS Sharpe rises monotonically in N (1.0519 / 1.0506 / 1.1870 / 1.1769 /
1.2358 / 1.2499 at N=5..40, cadence W) — the record's own N-ladder fact (idea 1081). The gap is a
proxy for "hold a broader book", smuggled in through whichever tie-break happens to point there.
The tie set is wide enough for that to matter: mean 10.95 of 12 books tied on U56 at K=10 and
still 6.00 of 12 at K=400. On SMALL it collapses to 0.00 at K=400 and all eight rungs become
identical, which is why SMALL's rows are flat.

## Capital and rule 8 (the verdict)
- **4a: 0 of 36 books and 0 of 162 picks.** 4b: 6 of 36 books (U56 5, B136 1, SMALL 0; the
  binding leg is the DD cap at 6 / 8 / 12 of the fails) and 36 of 162 picks.
- **Rule 8 on the dials**: (tie-break, K) chosen on warm-up..2016-12-31 by IS Sharpe alone,
  2017-2026 read once. U56 picks T_FIRST/K=10 -> OOS Sharpe 0.9143 / CAGR 19.99% / MaxDD -28.73%
  against do-nothing (N=20/W held throughout) 1.1769 / 15.76% / -19.09%, **delta -0.2626**. B136
  picks T_FIRST/K=10, +0.0401. SMALL picks T_ISSHARPE/K=10, +0.0013. **Mean delta -0.0737.**
- IS/OOS rank correlation over the 48 cells: **-0.95 (U56) / -0.65 (B136) / +0.65 (SMALL)**. On
  both large-cap panels the IS ordering of the tie-break rungs is *anti-correlated* with the OOS
  ordering, so the two rungs that win (T_HOLD, T_IS4B) are precisely the ones no honest
  in-sample procedure reaches.
- **0 of 3 rule-8 picks clear either KEEP path.** SPY OOS 15.28% / 0.8747 / -33.72%; live RULES
  v2 OOS Sharpe 1.2781 (U56). Nothing here is a candidate for capital.

## Gates: 16 of 16
G4a CH_PCT replays 1199's grid **exactly** (0.000e+00, 4,320 rows) — the tie set is the same
object. G5c B_POINT and CH_Z replay 1199's per-panel means on the vintage-free panels to
0.000e+00 (B136 0.954362 / 0.962579; SMALL 0.759910 / 0.751443). G4d 719 of 720 decisions
identical, the single flip named (U56/K=100/seed=18: CH_Z argmax 9 -> 8). G4b/G4c/G4e the drift
is **confined to U56**: `data/prices.csv` is refreshed daily and its adjusted closes are restated
retroactively, so U56 IS Sharpe moves 2.9e-04 and OOS Sharpe 7.5e-03, while B136 and SMALL are
bit-identical (2.2e-16). This is published, not toleranced. G6a B_ONE == B_CP tie set at every
row. G6b the one B_ONE/B_TWO difference is a FLOOR row (SMALL N=5/M, K=25, seed 9) — B_TWO's
design, not a defect. G1 fast runner == `engine.backtest` 2.78e-17. G8 the IS-truncated null
runner equals the full-tape runner on IS rows exactly (0.000e+00). G7 null gross 0.75 at every
rebalance row. G3 live RULES v2 U56 MaxDD -12.05%. G2 determinism 0.000e+00.

## Survivorship (rule 9)
U56 and B136 are current-constituent lists; SMALL is a current sub-$2B screen (52 of 715 dropped
for max_1d_move >= 1.0 -> 663 investable). Every level is optimistic and every 4b pass is an
upper bound. The headline is a contrast between eight choosers picking from the **same 12 books
on the same panel over the same tape**, so it is first-order immune to a level bias that moves
all cells together. One direction is not neutral and is stated: a current-constituent panel
flatters momentum books, raising every book's IS Sharpe and so making the null percentile *more*
saturated than it would be live. The tie sets here are therefore **wider** than a real
implementer's, which makes the measured sensitivity to the tie-break an **upper** bound.

## What the record should carry forward
1199's +0.0671 is a measurement of **CH_Z**, not of the bound form. Any clause that adopts a
bound form must name the tie-break statistic with it; and when the named statistic correlates
with book breadth, what is being published is the breadth prior, not the bound.

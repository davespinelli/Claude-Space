# Idea 929 — where does the BOOK SIZE axis TURN OVER at fixed q and k?  (cloud, 2026-09-15)

**ANSWER: at n = 50 → 60 in the POOLED pass rate, but the turnover is NOT a cell-confirmed fact —
it is one of the two cells that carry any 4b pass at all. KILL for an interior book-size optimum;
the axis is a DD-CAP-vs-CAGR-FLOOR CROSSING, not a Sharpe optimum.**

Script `2026-09-15_where-does-the-BOOK-SIZE-axis-TURN-OVER-at-fixed-q-and-k_cloud.py`.
28 panels = idea 686's own ladder restricted to k >= 100 (so max n = 60 < k), 10 (q,k) cells,
8 book sizes + EWall = 252 scored book rows. 10 bps, weekly, gross 0.75, t+1, warm-up 260.
Gates **5 of 5**, including **G3 an EXACT cross-run reproduction** of all 168 of idea 686's
committed k >= 100 rows (worst |delta| 2.8e-14 on CAGR/Sharpe/MaxDD/Ebar/breadth, 4a/4b identical).

## The n axis, every grid point (pooled over the 28 panels)

| n | 4b | 4a | Sharpe | CAGR | MaxDD | OOS_S | IS_S | L1_H1 | L2_H2 | L3_OOS | L4_DD | L5_CAGR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 | 0.000 | 0.000 | 0.462 | 7.77% | -38.04% | 0.437 | 0.512 | 0.036 | 0.000 | 0.000 | 0.000 | 0.250 |
| 10 | 0.000 | 0.000 | 0.523 | 7.58% | -30.64% | 0.481 | 0.605 | 0.143 | 0.000 | 0.000 | 0.000 | 0.286 |
| 15 | 0.000 | 0.000 | 0.563 | 7.50% | -27.20% | 0.529 | 0.630 | 0.286 | 0.000 | 0.036 | 0.000 | 0.321 |
| 20 | 0.000 | 0.000 | 0.582 | 7.33% | -25.75% | 0.550 | 0.645 | 0.286 | 0.036 | 0.071 | 0.071 | 0.250 |
| 30 | 0.071 | 0.000 | 0.630 | 7.37% | -23.70% | 0.594 | 0.700 | 0.357 | 0.071 | 0.071 | 0.250 | 0.250 |
| 40 | 0.107 | 0.000 | 0.651 | 7.16% | -22.16% | 0.599 | 0.751 | 0.393 | 0.107 | 0.143 | 0.321 | 0.214 |
| 50 | **0.143** | 0.000 | 0.671 | 6.98% | -21.00% | 0.614 | 0.785 | 0.429 | 0.143 | 0.143 | 0.429 | 0.179 |
| 60 | 0.036 | 0.000 | 0.673 | 6.58% | -19.68% | 0.611 | 0.802 | 0.357 | 0.107 | 0.143 | **0.571** | **0.036** |
| EWall | 0.000 | 0.000 | 0.657 | 7.36% | -31.31% | 0.575 | 0.830 | 0.500 | 0.071 | 0.143 | **0.000** | 0.179 |

SPY on the shared column: FULL 14.06% / 0.858 / -33.72%, OOS Sharpe 0.877. 4b bars: MaxDD ≥
-20.23%, CAGR ≥ 9.84%. RULES v2 on these panels: Sharpe mean 0.828, OOS mean 0.767.

## What the axis actually is

The pass rate rises 0.000 → 0.143 from n = 5 to n = 50 and falls to 0.036 at n = 60, so a
turnover EXISTS in the pooled reading — and the leg columns say exactly what it is made of. Two
legs move monotonically in OPPOSITE directions across the whole ladder:

* **L4_DD (MaxDD ≤ 60% of SPY's)** 0.000 → 0.571. Book size BUYS the drawdown cap: mean MaxDD
  -38.04% at n = 5 against -19.68% at n = 60.
* **L5_CAGR (CAGR ≥ 70% of SPY's)** 0.321 (n = 15) → 0.036 at n = 60. Book size SPENDS the CAGR
  floor: mean CAGR 7.77% → 6.58%.

The 4b footprint is the region where both hold, and it closes at n = 60 because the CAGR floor
runs out one rung before the DD cap stops paying. Sharpe itself does **not** turn over — it is
still rising at n = 60 (0.673, the ladder max) and its per-cell argmax is n = 60 in 4 of 10 cells
(H_SHARPE FAIL, interior in only 6 of 10, need 8). So "where the book-size axis turns over" has
two different answers depending on which quantity is asked about, and the record's n* = 30 is
neither of them.

**EWall is the decisive control.** As the n → limit point it has the ladder's best IS Sharpe
(0.830) and a respectable full Sharpe (0.657) and yet clears 4b on **0 of 28 panels**, because
its L4_DD rate is **0.000**: holding the whole eligible set gives back every bit of the drawdown
that concentration-plus-size buys (-31.31% against CAND60's -19.68%). Book size is therefore not
monotone-good up to the limit either; H_EW FAILS at 3 of 10 cells.

## Hypotheses (all pre-registered in the script docstring)

| bar | result | reading |
|---|---|---|
| H_TURN | **FAIL** | pooled 4b n=5 0.000 / best interior n=50 0.143 / n=60 0.036, so the pooled shape turns over — but per-cell confirmation is 1 of 2 (need 2). Only 2 of 10 cells carry ANY pass, and the two disagree: q=0.00/k=100 is flat at 1.00 from n=30 to n=60, q=0.25/k=100 turns over hard (0.33/0.67/1.00 → 0.00). |
| H_MONO_N | **FAIL** | min step -0.107 at n = 60. 686's monotone reading does not extend past its own ladder. |
| H_N | **PASS** | mean within-cell rho(pass4b, n) **+0.6674**, sign 2 of 2 — book size is still the axis, and more strongly than the +0.3125 686 read on n ≤ 30. |
| H_SHARPE | **FAIL** | Sharpe argmax interior in 6 of 10 cells (need 8); argmax n = 60 in 4 cells. |
| H_EW | **FAIL** | EWall beats max_n CAND-n in 3 of 10 cells. |
| H_WF | **PASS** | one rule-8 pick reaches OOS 4b — see below. |

## Rule 8 (2009–2016 only for the choice, 2017–2026 read once)

| selector | panel | book | IS Sharpe | OOS CAGR / Sharpe / MaxDD | vs SPY OOS | vs v2 OOS | FULL 4a/4b | OOS-WINDOW 4a/4b |
|---|---|---|---|---|---|---|---|---|
| PICK_ISSHARPE_ALL | q0.00_k100 | CAND15 | 1.089 | 13.79% / 0.921 / -21.15% | 15.33% / 0.877 / -33.72% | 8.69% / 1.127 / -12.76% | 0/0 | 0/0 |
| PICK_ISSHARPE_CAND_ONLY | q0.00_k100 | CAND15 | 1.089 | 13.79% / 0.921 / -21.15% | same | same | 0/0 | 0/0 |
| PICK_ISSHARPE_BIG_N_ONLY | q0.00_k100 | **CAND60** | 1.076 | **11.68% / 1.121 / -17.07%** | 15.33% / 0.877 / -33.72% | 8.69% / 1.127 / -12.76% | 0/**1** | 0/**1** |
| PICK_ISSHARPE_K100 | q0.00_k100 | CAND15 | 1.089 | 13.79% / 0.921 / -21.15% | same | same | 0/0 | 0/0 |
| PICK_KMAX_N60 (3 draws) | q0.75_k400 | CAND60 | 0.719 | 6.24–8.11% / 0.527–0.656 / -21.5 to -23.9% | same | 4.80–5.38% / 0.729–0.807 | 0/0 | 0/0 |

**OOS-WINDOW 4b 1 of 7 picks, 4a 0 of 7.** The unrestricted IS chooser picks CAND15 and fails
4b on the DD cap ALONE (-21.15% against the -20.23% bar) — a 0.92 pp miss, and exactly the leg
the n axis is made of. Only the selector RESTRICTED to n > 30 reaches 4b, and that restriction is
this idea's own axis, not something the in-sample data chose: stated, not hidden.

## By-product worth a memo (not a promotion)

`BSTK100 / CAND60` — the q = 0.00, k = 100 cell is not a synthetic draw at all; it is the whole
BSTK100 large-cap pool, so this is a nameable rule. It clears 4b on the FULL sample **and** on
the OOS window: FULL **11.35% / 1.104 / -17.07%**, halves **1.206 / 1.006** against SPY's
0.914 / 0.834; OOS **11.68% / 1.121 / -17.07%** against SPY's 15.33% / 0.877 / -33.72%. It fails
4a (RULES v2 full Sharpe 1.121 against 1.104). CAND30/40/50 on the same panel also clear 4b
(1.007 / 1.022 / 1.059), so the pass is a REGION of the axis, not one rung. Memo:
`2026-09-15_bstk100-cand60.memo.md`. **SURVIVORSHIP: BSTK100 is a current-constituent list, so
every level above is optimistic and the 4b bars are easier here than on a point-in-time panel.**

## Verdict

**KILL** for the queue's premise as stated. There is no cell-confirmed interior optimum in book
size: the pooled pass rate does turn over at n = 50 → 60, but 8 of 10 cells never pass at any n,
the two that do disagree about the shape, and Sharpe keeps rising to the ladder's end. What the
extension DID establish is the mechanism — the 4b footprint in n is the crossing of a
monotonically-won DD cap against a monotonically-lost CAGR floor — plus an EWall control showing
the far limit is not the optimum either. Nothing promoted; one memo filed for Sunday review.

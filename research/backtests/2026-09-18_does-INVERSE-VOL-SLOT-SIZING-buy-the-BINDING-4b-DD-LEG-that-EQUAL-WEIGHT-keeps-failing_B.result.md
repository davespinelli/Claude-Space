# 1264 (lane B, 2026-09-18) — does INVERSE-VOL SLOT SIZING buy the BINDING 4b DD LEG that EQUAL WEIGHT keeps failing?

**VERDICT: KILL (capital).** No RULES change, no book promoted, no PROTOCOL edit, no memo.
**7 of 7 gates, 126 cells all published, 21s, offline, deterministic.**

## The one-sentence answer
**THE DRAWDOWN LEG IS BUYABLE — inverse-vol sizing converts three committed 4b FAILS into PASSES, including 1257's higher-return M12_1 book — BUT IT IS PAID FOR IN RETURN AT EVERY SINGLE RUNG ON ALL SIX ARMS, AND RULE 8 PICKS EQUAL WEIGHT (ALPHA = 0, the incumbent's own sizing) AT 4 OF 4 LARGE-CAP CELLS WITH A DELTA OF EXACTLY +0.0000.**

## What was run
The frozen 2026-09-04 candidate with **only its slot weighting replaced**. Everything else held: eligibility (above own 200d MA AND vol20 < 0.60), N = 20, H = 126, GROSS = 0.75, weekly Fri-decide / Mon-trade, gated-out weight to cash via the committed 1/len(held) spread convention, 10 bps, t+1, 260-row warm-up, ranking on the RAW composite.

**THE TWO DIALS AND NO MORE (rule 4):** `ALPHA` {0.00, 0.25, 0.50, 0.75, 1.00, 1.50, 2.00} (slot weight ∝ vol^-ALPHA; **0.00 IS EXACTLY EQUAL WEIGHT, i.e. THE COMMITTED ANCHOR**) × `LOOK` {20, 60, 126} days = 21 cells per arm. NOT dials, reported at every value: PANEL {U56, B135, SMALL663} × SIGNAL {COMPOSITE3 = the committed three legs, M12_1 = 1257's single 21/252 leg} = 6 arms, **126 cells, EVERY ONE in `.grid.csv`**. Frozen constant, not a dial: VOL_FLOOR = 0.08; **no max-slot cap** (a cap would be a third parameter) — realised max and effective slot weight are published instead.

**SELECTION IS IDENTICAL AT EVERY ALPHA BY CONSTRUCTION.** The dials touch weights only, never the holdings, which is what makes the ladder a clean read on sizing alone.

## A tape-vintage fact the gates found, published rather than toleranced away
The committed anchor triples were produced on 2026-09-17 when the cache ended **2026-09-16**; today's cache carries one more trading day. That single day moves the committed U56 composite triple from 15.71% / 1.1480 to **15.78% / 1.1522** and SPY's from 15.06% / 0.8815 to **15.13% / 0.8849**. A naive replay gate misses by 4.2e-03 for reasons that are **not** construction. The gates were therefore **pinned to the vintage, not loosened**: **G1** truncates U56 at 2026-09-16 and replays the committed 15.7147% / 1.1480 / -19.1276% to **5.97e-05**; **G4** replays 1257's M12_1 16.7116% / 1.1893 / -20.5813% to **2.26e-05**. **G6** publishes the drift (+0.0668% CAGR, +0.0042 Sharpe, +0.0000% MaxDD). Every grid number below is on the FULL current tape, with SPY and LIVE v2 recomputed on that same tape. **G2** ALPHA 0 is bit-identical across all three LOOK values (0.000e+00). **G3** slot weights sum to 1 (4.44e-16). **G5** determinism, whole U56 grid re-run (0.000e+00).

## Benchmarks on this tape (all recomputed, never carried forward)
| panel | SPY full | SPY halves | SPY OOS | LIVE v2 full | LIVE v2 OOS | 4b DD cap | 4b CAGR floor |
|---|---|---|---|---|---|---|---|
| U56 | 15.13% / 0.8849 / -33.72% | 0.9600 / 0.8236 | 15.28% / 0.8747 | 8.62% / 1.2018 / -12.05% | 9.47% / 1.2781 | -20.23% | 10.59% |
| B135 | 15.16% / 0.8862 / -33.72% | 0.9598 / 0.8261 | 15.33% / 0.8769 | 7.98% / 1.0994 / -12.24% | 7.88% / 1.1061 | -20.23% | 10.61% |
| SMALL663 | 14.06% / 0.8582 / -33.72% | 0.9140 / 0.8346 | 15.33% / 0.8769 | 4.64% / 0.7130 / -12.18% | 4.47% / 0.6518 | -20.23% | 9.84% |

## (1) THE PREMISE IS CONFIRMED: THE DD LEG IS REAL, CHEAP-LOOKING, AND CONVERTS FAILS
MaxDD improves in ALPHA at **every rung of 5 of 6 arms** (B135/COMPOSITE3 is the exception and is non-monotone, which is stated rather than smoothed). On U56/COMPOSITE3 the ladder walks **-19.13% → -14.60%, 4.53pp of drawdown**. Three committed FAILs are converted:

| arm | ALPHA 0 (the committed sizing) | first 4b PASS | what the DD cost |
|---|---|---|---|
| **U56 / M12_1** (1257's better book) | **FAIL on DD** -20.58%, CAGR 16.79%, Sh 1.1941, turn 2.51 | **a 0.25 / L 20** -19.95%, 15.73%, 1.1761, turn 2.94 | **+0.64pp DD for -1.06pp CAGR, -0.0180 Sharpe, +0.43/yr turnover** |
| B135 / COMPOSITE3 | FAIL on DD -20.74%, 16.18%, 1.0715, turn 3.11 | a 0.25 / L 20 -19.64%, 15.54%, 1.0607, turn 3.57 | +1.10pp DD for -0.65pp CAGR, -0.0108 Sharpe, +0.46/yr |
| B135 / M12_1 | FAIL on DD -21.73%, 16.06%, 1.0412, turn 2.86 | a 1.50 / L 20 -19.96%, 13.23%, 0.9881, turn 7.97 | +1.77pp DD for **-2.83pp CAGR, -0.0532 Sharpe, +5.11/yr turnover** |

So the answer to the literal question is **YES** — and 1257's finding that M12_1 was "disqualified solely by drawdown" is now priced: **that disqualification costs 1.06pp of CAGR to remove.**

## (2) BUT THE RETURN IS SOLD AT EVERY RUNG, AND FULL SHARPE FALLS MONOTONICALLY ON ALL SIX ARMS
CAGR falls monotonically in ALPHA on all four large-cap arms; full Sharpe falls monotonically on **all six**. On U56/COMPOSITE3, ALPHA 0 → 2.0 buys 4.53pp of MaxDD for **-6.30pp of CAGR, -0.109 of full Sharpe and +5.87/yr of turnover** (2.75 → 8.62). The mechanism is not subtle: inverse-vol sizing on a momentum book systematically underweights exactly the high-volatility names the momentum screen selected it for, and the effective breadth collapses (N_eff 19.79 → 11.20, max slot weight 0.125 → 0.703 — **at ALPHA 2 / LOOK 20 a single name is 70% of the book**, which is a concentration risk the drawdown number does not show).

## (3) RULE 8 IS DECISIVE AND IT SAYS DO NOTHING WHEREVER A 4b PASS IS AVAILABLE
(ALPHA, LOOK) chosen on warm-up..2016-12-31 by IS Sharpe ALONE; 2017-2026 read ONCE; do-nothing control = ALPHA 0.

| panel / signal | IS pick | pick OOS | do-nothing OOS | **delta** | cell mean | best cell | rank corr IS/OOS |
|---|---|---|---|---|---|---|---|
| U56 / COMPOSITE3 | **a 0.00** / L 20 | 1.1832 | 1.1832 | **+0.0000** | 1.1856 | 1.2046 | +0.22 |
| U56 / M12_1 | **a 0.00** / L 20 | 1.1626 | 1.1626 | **+0.0000** | 1.1574 | 1.1792 | +0.32 |
| B135 / COMPOSITE3 | **a 0.00** / L 20 | 1.0240 | 1.0240 | **+0.0000** | 1.0098 | 1.0349 | +0.65 |
| B135 / M12_1 | **a 0.00** / L 20 | 1.0004 | 1.0004 | **+0.0000** | 1.0320 | 1.0841 | **-0.88** |
| SMALL663 / COMPOSITE3 | a 2.00 / L 20 | 0.5210 | 0.4534 | +0.0676 | 0.4702 | 0.5210 | +0.89 |
| SMALL663 / M12_1 | a 1.50 / L 20 | 0.6091 | 0.4875 | +0.1215 | 0.5249 | 0.6363 | +0.46 |

**THE CHOOSER PICKS EQUAL WEIGHT AT 4 OF 4 LARGE-CAP CELLS.** It gains only on SMALL663 — the one panel where **nothing passes anything**: 0 of 42 SMALL663 cells pass 4b, and every one fails **all five legs**. Where the dial pays, no book is investable; where books are investable, the dial is exactly free. That is the capital verdict.

**AND THE GAIN THAT EXISTS IS UNREACHABLE.** U56/COMPOSITE3's best OOS cell is a 0.75 / L 20 at **1.2046 (+0.0214 over do-nothing)** — but IS Sharpe peaks at ALPHA 0, so in-sample selection never reaches it (rank corr +0.22). On B135/M12_1 the IS/OOS rank correlation is **-0.88**: the in-sample ordering of this dial is actively misleading out of sample.

## (4) A PROTOCOL FACT THIS LADDER DEMONSTRATES MORE CLEANLY THAN ANYTHING IN THE RECORD — **4b IS A FILTER, NOT A RANKING**
**4a passes 0 of 126** (live v2's -12.05% MaxDD is not beatable by a growth book — rule 4b's own reason for existing). **4b passes 51 of 126.** On U56/COMPOSITE3 alone, **18 of 21 cells are "4b PASS", and they span 10.70% to 15.78% CAGR (5.08pp), 1.0291 to 1.1522 of full Sharpe, and 2.75 to 7.15/yr of turnover.** Every one of those 18 books carries the identical verdict string while being ordered strictly worst-to-best in the direction 4b cannot see. **A 4b PASS is a floor test, and this run shows the floor can be walked down 5 percentage points of CAGR without the verdict noticing.** This is *filed as idea 1265 and PROPOSED for the Sunday review (rule 6) as a reporting line only — a published 4b PASS should carry its CAGR and Sharpe distance from the best cell in its own grid — **never as a chooser**.*

## Pre-declared outcomes, scored as they fell
- **(A) INERT — FALSE.** MaxDD moves 4.53pp on U56/COMPOSITE3, twenty times the 0.20pp inertness clause.
- **(B) THE DD LEG IS BOUGHT — HALF TRUE, AND THE HALF THAT FAILS IS THE ONE THAT DECIDES.** The conversion clause fires (three FAIL→PASS conversions above). **The rule-8 clause does not: the walk-forward does not reach it at 4 of 4 large-cap cells.** (B) as written required both.
- **(C) BOUGHT AND OVERPAID — TRUE.** Full Sharpe falls monotonically on all six arms; the cheapest conversion still costs 1.06pp of CAGR and 0.43/yr of extra turnover, and B135/M12_1's costs 2.83pp and 5.11/yr.
- **(D) DD GETS WORSE — FALSE** on every arm; the stale-price worry did not materialise even on SMALL663.
- **(B) and (C) both firing means this run's outcome set was not mutually exclusive.** That is stated rather than resolved by choosing the flattering reading — the same defect 1257 published in its own pre-registration. The capital verdict follows rule 8, i.e. (C).

## Survivorship (rule 9)
U56 and B135 are CURRENT-constituent lists; SMALL663 is a current sub-$2B screen (52 of 715 dropped for max_1d_move ≥ 1.0 before anything was computed). Every absolute level is optimistic and every 4b pass is an **upper bound**. The headline is a DIFFERENCE between sizing rules over the **identical holdings** on the same panel, first-order immune to a level bias moving all cells together. One direction is **not** neutral and is stated: a current-constituent list is **kind to the high-vol winners a momentum screen piles into**, because the high-vol names that did not survive are absent — so the **equal-weight (low-ALPHA) arm is the more flattered of the two**, and **the inverse-vol arm's loss reported here is an UPPER bound on its loss**. Even granting that, rule 8 picks ALPHA 0 at every large-cap cell. Per 1255's clause: the U56 committed pass dies at k ≈ 12 deleted ex-post winners.

## What the record should take, in one sentence
**THE 2026-09-04 BOOK'S EQUAL WEIGHTING IS NOT A DEFECT: THE ONLY LEG IT EVER FAILS IS PURCHASABLE BY INVERSE-VOL SIZING, BUT THE PRICE IS PAID IN CAGR, SHARPE AND TURNOVER AT EVERY RUNG, AND OUT OF SAMPLE THE CHOOSER DECLINES TO PAY IT ON EVERY PANEL WHERE A BOOK IS INVESTABLE AT ALL — THE FIFTH DIAL RUNNING ON WHICH THE COMMITTED PASS IS A STATEMENT ABOUT THE DRAWDOWN LEG AND NOTHING ELSE.**
NO NEW BOOK, NO MEMO, NO RULES CHANGE; THE INCUMBENT STANDS.

Script: `research/backtests/2026-09-18_does-INVERSE-VOL-SLOT-SIZING-buy-the-BINDING-4b-DD-LEG-that-EQUAL-WEIGHT-keeps-failing_B.py`
Artifacts: `.grid.csv` (126 cells), `.walkforward.csv` (6 rule-8 rows), `.gates.csv` (7), `.console.txt`

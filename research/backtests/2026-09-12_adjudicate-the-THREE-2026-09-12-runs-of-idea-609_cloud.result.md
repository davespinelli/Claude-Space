# Idea 826 — adjudicate-the-THREE-2026-09-12-runs-of-idea-609-against-each-other (cloud, 2026-09-12)

**ANSWERED = ALL THREE RUNS ARE RIGHT AND ONLY ONE NUMBER IS REAL. The record should quote
FULLMATCH 0.32; WINMATCH's 0.0847 is 99.1% a tie-handling count, not a re-ranking.**
Script: `2026-09-12_adjudicate-the-THREE-2026-09-12-runs-of-idea-609_cloud.py`. **KILL for capital.**

## Gates (all printed before any new number was read)

| gate | what | result |
|---|---|---|
| G1 | `fast_backtest` == `engine.backtest`, returns AND turnover, 3 real books × 3 rungs | 4.996e-16 **PASS** |
| G2 | fast CAGR/Sharpe/MaxDD == `engine.metrics`, 200 real series | 2.220e-16 **PASS** |
| G3 | O(1) sums-ladder window Sharpe == direct Sharpe on the same slice, 144 samples | 2.154e-14 **PASS** |
| G4 | derived cost ladder == live backtest through the gate, all 15 rungs | 3.469e-18 **PASS** |
| G5 | idea 84's committed EWALL U56 g=0.85 @10bps | 11.75% / 1.046 / −17.89% vs 11.8 / 1.05 / −17.9 **PASS** |
| G6 | `GrossGrid` (O(T) per gross) == `fast_backtest`, 4 grid points × 3 panels | 4.441e-16 **PASS** |
| G7 | panel vintage stamp | today's cache = 664 cols → drop 52 (`max_1d_move ≥ 1.0`) → **SMALL663**; ideas 605/609 read SMALL439 |

## The reconciliation table (the deliverable)

Share of rolling 756-day windows showing idea 605's published order **QROLL > QEXP > ABS**,
pooled over U56 / B136 / SMALL663, rung 10 bps, published tie rule (a tie is a LOSS):

| convention | step 21 | step 63 | step 126 |
|---|---|---|---|
| **FULLMATCH** | 0.3125 | 0.3220 | 0.3000 |
| **WINMATCH**  | 0.0909 | 0.1017 | 0.0667 |
| *n windows* | 176 | 59 | 30 |

Every committed headline lands in its own cell:

| committed | source | this run | \|diff\| |
|---|---|---|---|
| 0.3125 | `_B2` lane B2, FULLMATCH step 21 | 0.3125 | 0.0000 |
| 0.3220 | `2c96cad` cloud + `_B2` 0.322034, FULLMATCH step 63 | 0.3220 | 0.0000 |
| 0.0847 | `aa87884` lane B, WINMATCH step 63 | 0.1017 | 0.0170 |

**H1 PASS.** The cloud run and `_B2` are ONE number to 4 dp, not two. `aa87884` differs by
**exactly one window of 59** (5/59 vs 6/59) — the only population difference between the runs is
the SMALL panel vintage (SMALL439 → SMALL663, G7), so the residual is the nightly cache, not a
disagreement about the census.

## Why the two conventions differ — the deciding test

* **Q2 axis sizes (H2 PASS).** Convention moves `share_exact` by up to **0.2333**; step by
  **0.0350**. The queue's premise — matching sample is the big axis, step is sampling density —
  is **confirmed**, and step 63/126 are *exact subsamples* of step 21 here, so the step column is
  pure resolution.
* **Q3 mechanism (H3 PASS).** 235,615 win-sign flips of 1,642,680 comparisons (0.1434), of which
  **234,666 = 99.60%** are cells whose gate **never fires inside that window**. There WINMATCH
  sets the twin's gross to the arm's own gross, the twin becomes the arm **bit for bit**,
  dSharpe ≡ 0, and `win = dSharpe > 0` books it a LOSS. 19.2% / 20.9% / 17.4% of all
  (cell, window) pairs on U56 / B136 / SMALL663 are never-firing.
* **The gap, decomposed.** Step-63 convention gap **0.2203** under the published tie rule →
  **0.0019** once exact ties leave the denominator. **99.1% of the gap is tie handling.**

  | tie rule | FULLMATCH 21/63/126 | WINMATCH 21/63/126 |
  |---|---|---|
  | LOSS (published) | 0.3125 / 0.3220 / 0.3000 | 0.0909 / 0.1017 / 0.0667 |
  | EXCLUDE | 0.3409 / 0.3390 / 0.3333 | 0.3258 / 0.3409 / 0.2727 |
  | WIN | 0.3523 / 0.3559 / 0.4000 | 0.1761 / 0.1525 / 0.1667 |

  *(decomposition only — no verdict in this file is read off the EXCLUDE/WIN rows)*
* **Q4 invariance (H4 PASS).** On the 88,422 (cell, window) pairs whose gate **does** fire, and
  over gross mismatches as large as **0.3434**, re-matching the twin's gross moves its Sharpe by
  at most **3.231e-03** (median of panel medians 6.8e-05). A static long-only book's Sharpe is
  gross-invariant to ~1e-3; the convention cannot re-rank anything.

## Rule 8 on the claim (PROTOCOL 8)

Choose the convention on the first half of the window population, read the second half untouched:

| convention | IS share | OOS share |
|---|---|---|
| FULLMATCH | 0.2949 | 0.3283 |
| WINMATCH | 0.0038 | 0.1702 |

**H5 PASS** — the IS-chosen convention (FULLMATCH) is also the OOS-best. But the *level* does not
walk forward under either: WINMATCH reads 0.0000 on the IS half at steps 63/126 and 0.13–0.21 on
the OOS half, i.e. it is a window statement about how often the gate is idle, not about ordering.

## Which headline the record should quote

**FULLMATCH, and with its step stated: 0.3220 at step 63 / 0.3125 at step 21.** Not because
FULLMATCH is more realistic — WINMATCH's "a reader holding only this window" motivation is sound —
but because under WINMATCH the statistic stops measuring what it is quoted for. In a window where
the gate is idle, WINMATCH's twin *is* the arm, so the comparison is vacuous and the published rule
silently records a loss; 99.6% of the convention's effect is that bookkeeping. Either quote
FULLMATCH, or quote WINMATCH **with never-firing cells excluded from the denominator**, where the
two conventions agree to **0.0019**. Idea 605's underlying caveat is untouched by any of this:
the published order is seen in **under a third** of windows on every convention, step and rung.

## Capital (PROTOCOL 4, both paths, all 9,720 grid points, never selected on)

* At 10 bps, pooled: **4a 0 of 648**, **4b 141 of 648**.
* The 4b passes are a **gross** statement, as the record has repeatedly found: 119 of 141 sit at
  g = 1.00 (U56 65/108, B136 54/108 at g=1.00 against 2/108 and 20/108 at g=0.75), and
  **SMALL663 passes 0 of 216 at every rung**. Idea 502's zero-cost base-rate control already puts
  gross-matched coin flips at a 78.1% 4b pass rate on U56, so a bare 4b pass on this family
  carries no information; nothing here is promoted.
* **Rule 8 book leg** — pick one arm per panel on IS Sharpe alone (≤2016) at 10 bps, read once on
  OOS (2017+):

| panel | IS pick | OOS CAGR | OOS Sharpe | OOS MaxDD | RULES v2 OOS Sharpe | SPY OOS | 4a | 4b |
|---|---|---|---|---|---|---|---|---|
| U56 | QROLL q0.17 w504 d1.00 D g1.00 | 13.46% | 1.2322 | −17.86% | 1.2782 | 15.33% / 0.8767 / −33.72% | no | yes |
| B136 | QROLL q0.17 w504 d0.50 W g1.00 | 12.86% | 1.1075 | −17.20% | 1.1059 | same | no | yes |
| SMALL663 | ABS B0.40 d1.00 W g1.00 | 3.81% | 0.3545 | −25.28% | 0.5600 | same | no | no (H1,H2,OOS,DD,CAGR) |

Both large-cap picks beat SPY out of sample and clear 4b on the letter; neither beats the live book
on 4a, and both are ungated-EWALL-at-g=1.00 in all but name (their gates fire rarely — that is the
same fact that produced the tie count above). **Verdict: KILL for capital.** This idea is a
bookkeeping adjudication and it is answered; no RULES change, no book promoted.

*Survivorship: SMALL663 and B136 are current constituents only; both bias upward. Research, not
investment advice.*

# Idea 761 — is the SMALL439-only predictive correlation a BREADTH effect?

**Cloud lane, 2026-09-11.** Script `2026-09-11_is-the-SMALL439-ONLY-predictive-correlation-a-BREADTH-effect_cloud.py`.
10 bps / unit turnover, next-day execution, gross 0.75, weekly, RESPREAD. IS = start..2016-12-31,
OOS = 2017-01-01..end read once. 2 tuned params: subset size {55, 135} and draws (30, seed 761).
Statistic {DROP, SPREAD} × window {FULL_IS, TRAIL3Y, TRAIL1Y} reported in full, never selected over.

## Verdict: **ANSWERED / SPLIT — the LEVEL is mostly BREADTH, the PANEL GAP is CONTENT, and at U56's size the screen is a KILL.**

Idea 560's headline (+0.48 to +0.65 on SMALL439, ~0 on U56 and B136) survives size-matching as a
**panel difference** but not as a **number**. Cut SMALL439 to 55 random names — U56's size — and the
same correlation reads **+0.15 / +0.17 / +0.19** (DROP × FULL_IS / TRAIL3Y / TRAIL1Y medians of 30
draws), a **68% / 74% / 67%** fall, with a median per-draw t of **0.78–0.95** and only **17–30%** of
draws reaching |t| > 2. A correlation that small over 27 points is not a screen anyone can act on.

## What was measured

| statistic × window | U56 (55) | B136 (135) | SMALL439 (439) | SMALL@135 med | SMALL@55 med [p10, p90] | **B136@55 med** (placebo) |
|---|---|---|---|---|---|---|
| DROP × FULL_IS | −0.0330 | +0.0026 | **+0.4815** | +0.3058 | **+0.1535** [−0.058, +0.408] | **−0.1300** |
| DROP × TRAIL3Y | +0.1169 | +0.0859 | **+0.6505** | +0.4646 | **+0.1663** [−0.049, +0.499] | **−0.0198** |
| DROP × TRAIL1Y | +0.0510 | +0.1893 | **+0.5564** | +0.4474 | **+0.1863** [+0.006, +0.520] | **+0.0101** |
| SPREAD × FULL_IS | +0.0164 | −0.0516 | +0.5642 | +0.3647 | +0.1054 | −0.1329 |
| SPREAD × TRAIL3Y | +0.0038 | +0.1305 | +0.6155 | +0.4213 | +0.2250 | −0.0903 |
| SPREAD × TRAIL1Y | −0.2847 | +0.3367 | +0.4994 | +0.3412 | +0.1830 | +0.0327 |

All 90 draws × 6 grid points are in `.draws.csv`; the full-panel rebuilds reproduce idea 560's
committed `.census.csv` per-panel columns to **2.220e-16** (G2).

## The two readings, separated

**BREADTH carries the level.** The attenuation model — noise variance of a cell's OOS advantage
estimated *across draws at the same size*, signal variance from the cross-cell spread of the draw
mean — gives λ(55) = **0.6061** and λ(135) = **0.7952**. Predicted r for SMALL@55 is 0.29 / 0.39 /
0.34 against **observed 0.15 / 0.17 / 0.19**: the observed correlation is **below** what pure
measurement attenuation predicts (mean signed residual **−0.1206**, mean |residual| 0.1211 over 18
points). Nothing in the decline needs a small-cap story.

**CONTENT carries the panel gap.** At matched size 55, SMALL@55 − B136@55 = **+0.2835 / +0.1861 /
+0.1762**, against a multiplicative-attenuation prediction of +0.2901 / +0.3341 / +0.2046 — the
small-minus-large difference survives size-matching (FULL_IS at 0.98× its predicted value), and the
placebo confirms the mechanism is not "small numbers make r bigger": shrinking B136 from 135 to 55
moves its r **down**, to −0.13 / −0.02 / +0.01, with **0 of 90** draws reaching t > 2 on any window.

So idea 560's panel ordering is real; its magnitude is an artefact of counting 439 names.

## Does anything survive as a decision or a book? No.

* **DECISION leg** (pick the threshold by the IS statistic, score its OOS advantage): full SMALL439
  beats its own cell median **77.8%** of the time (mean rank 4.33 of 9); at SMALL@55 that is
  **50.0% — exactly a coin toss** (mean rank 4.60), and at B136@55 **50.0% / 41.9%**.
* **BOOK leg, rule 8** (threshold chosen on IS alone, OOS read once): **837 books, 4a 0, 4b 10.**
  On every small-cap support the books lose to SPY out of sample **0 of 270**; the statistic-based
  selectors (IS_DROP / IS_SPREAD) beat RULES v2 OOS in **2.2% / 4.4%** of B136@55 books against
  **47.8%** for the plain IS-Sharpe selector — the statistic is worse than the incumbent selector
  wherever both can be run.
* The one full-panel 4b passer (U56 / MA-DIST / IS_SHARPE / th −0.12: CAGR 12.11%, Sharpe 1.1325,
  MaxDD −20.10%, H1/H2 1.2641/1.0248, OOS Sharpe 1.1020) **reproduces idea 560's committed grid row
  to the digit** (0.121065 / 1.132470 / −0.200998 / 1.102038). It is not new and gets **no memo**; it
  clears the DD cap by 0.13 pp (−20.10% against −20.23%) and the CAGR floor by 1.5 pp.
* The other nine 4b passers are **random 55-name subsets of B136 under an IS-picked LOWVOL gate —
  9 of 90 draws (10%)**. A base rate, in the spirit of idea 502, not a rule.

## Gates (pre-registered)

| gate | result |
|---|---|
| G0 `fast_run` vs `engine.backtest` on a 55-name subset | **0.000e+00** PASS (bar 1e-12) |
| G1 three-leg identity \|ADD+DROP+BOTH − gap\| | **1.284e-16** PASS (bar 1e-12) |
| G2 reproduction of idea 560's `.census.csv` per-panel columns, 18 points | **2.220e-16** PASS (bar 1e-6) |
| G3 depth match \|breadth(gate) − breadth(control)\| | 1.923e-02 (reported; ceil-rounding of the matched depth, idea 560's own construction) |
| G4 draw determinism, 90 draws re-generated from seed 761 | **PASS** |

## Survivorship

B136 and SMALL439 are **current constituents only**; the 44 SMALL names with `max_1d_move >= 1.0`
are dropped first (`data/small_meta.csv`). Every CAGR level above is inflated and neither KEEP column
is immune. The census leg is an arm-minus-arm difference inside one support, where the bias very
largely cancels; the book leg is not protected, which is one more reason the 10 4b passes are
reported as a base rate rather than as candidates.

## Follow-ups proposed

* Does the same size-matched collapse apply to **every per-panel correlation the record quotes on
  SMALL439**? This run only re-read idea 560's.
* λ is estimable **before** a panel claim is published (draws at the claimed size cost one run each);
  propose quoting λ and the size-matched median beside any cross-panel correlation.

# Idea 2071 (lane cloud, 2026-09-21) — CAN THE TARGET `t` BE SET WITHOUT THE IS WINDOW?
**ANSWER: YES on the large panels, and the zero-chooser rule is a KEEP-candidate on path 4b.
NO on SMALL665. And the de-grossing-only control (CASHSHARE) fails everywhere on drawdown, so the
vol target itself — not the lower gross — is what earns the 4b pass.**

## Setup
Book inherited verbatim from the standing KEEP-4b candidate (VOLTGT-DRIFT, `h = 0.08`, trade W,
10 bps, t+1, gross ≤ 1.00, sigma = 20d realised vol of the unlevered equal-weight panel).
**Two tuned parameters and no more:** the TARGET-RULE FAMILY x that family's own single dial.
All 20 rungs x 3 panels x 4 cost rungs = **240 cells published** in `.grid.csv`.

| family | target rule | dial ladder | reads 2009-2016? |
|---|---|---|---|
| FIXED | `t` constant | 0.08 / 0.10 / 0.12 / 0.16 / 0.20 | **yes** (incumbent; needs a chooser) |
| SELFQ | `t` = q-quantile of the panel's trailing 3y sigma | 0.10 / 0.20 / 0.30 / 0.40 / 0.50 | no |
| MEDMULT | `t` = m x expanding median sigma | 0.50 / 0.70 / 0.85 / 1.00 / 1.20 | no |
| CASHSHARE | no target: gross set directly at `1 - c` | 0.10 / 0.20 / 0.25 / 0.30 / 0.40 | no |

**Zero-chooser arms PRE-STATED in the script docstring before compute:** SELFQ q=0.50,
MEDMULT m=1.00, CASHSHARE c=0.25 (the live book's own cash share). Gates 6/6, including a
no-look-ahead gate (the SELFQ target on a tape truncated at the halfway date equals the full-tape
target to 0.0e+00) and reproduction of the standing memo's cell to max abs d **3.15e-05**.

## 1. The headline: the pre-stated zero-IS arms, 10 bps, t+1

| panel | arm | CAGR | Sharpe | MaxDD | halves | OOS 2017-26 | 4b | 4a |
|---|---|---|---|---|---|---|---|---|
| B136 | FIXED 0.10 *(IS-chosen incumbent)* | 12.51% | 1.2286 | -11.81% | 1.3171 / 1.1415 | 13.01% / 1.2928 | PASS | PASS |
| B136 | **MEDMULT 1.00 [0-IS]** | **15.98%** | **1.2464** | -16.79% | 1.3297 / 1.1569 | **14.80% / 1.2845** | **PASS** | fail |
| B136 | **SELFQ 0.50 [0-IS]** | 14.90% | 1.2180 | -16.24% | 1.2939 / 1.1370 | 13.86% / 1.2601 | **PASS** | fail |
| B136 | CASHSHARE 0.25 [0-IS] | 14.03% | 1.1136 | -25.37% | 1.2327 / 1.0067 | 13.70% / 1.0870 | fail (L4_DD) | fail |
| U56 | FIXED 0.10 | 12.52% | 1.2434 | -13.49% | 1.2521 / 1.2358 | 13.65% / 1.3450 | PASS | fail |
| U56 | **MEDMULT 1.00 [0-IS]** | 14.94% | **1.2557** | -16.43% | 1.2878 / 1.2226 | 14.89% / 1.3272 | **PASS** | fail |
| U56 | **SELFQ 0.50 [0-IS]** | 14.63% | 1.2459 | -16.53% | 1.2478 / 1.2443 | 15.03% / 1.3415 | **PASS** | fail |
| U56 | CASHSHARE 0.25 [0-IS] | 13.19% | 1.1189 | -22.53% | 1.1925 / 1.0603 | 13.67% / 1.1266 | fail (L4_DD) | fail |
| SMALL665 | all four arms | 3.92-11.84% | 0.53-0.70 | -16.5 to -40.8% | — | — | **0 of 20 cells** | 0 of 20 |

SPY over the same window: 15.12% / 0.8844 / -33.72% (bars: CAGR floor 10.59%, DD cap -20.23%);
OOS SPY 15.26% / 0.8737. Live RULES v2: B136 7.96% / 1.0972 / -12.24%, U56 8.62% / 1.2010 / -12.05%.

**Zero-IS 4b pass count: 4 of 9 pre-stated arms (2 families x 2 large panels), and 4 of 4 of
those also pass on the OOS window read alone.** Cost is not the binding axis: both passing arms
hold 4b at **0 / 10 / 25 / 50 bps**, 2 of 2 at every rung, on both large panels.

## 2. Whole-grid pass counts (full sample, 15 cells per family = 5 dials x 3 panels)

| family | 4b @0 | @10 | @25 | @50 | 4a @0 | @10 | @25 | @50 |
|---|---|---|---|---|---|---|---|---|
| FIXED | 8/15 | 6/15 | 6/15 | 6/15 | 3/15 | 3/15 | 2/15 | 0/15 |
| **SELFQ** | 10/15 | **10/15** | 9/15 | 7/15 | 1/15 | 1/15 | 1/15 | 0/15 |
| **MEDMULT** | 8/15 | 8/15 | 8/15 | **8/15** | 1/15 | 1/15 | 1/15 | 0/15 |
| CASHSHARE | 1/15 | **0/15** | 0/15 | 0/15 | 0/15 | 0/15 | 0/15 | 0/15 |

The self-scaling families are **not worse than the fitted one and are flatter in cost** — SELFQ
passes 4b at more cells than FIXED at every rung ≤25 bps, and MEDMULT loses nothing from 0 to 50 bps
(turnover 2.25/yr vs FIXED's 3.13/yr, refreshes 11.4/yr vs 21.0/yr).

## 3. The control that matters: de-grossing alone does NOT do it
CASHSHARE holds gross flat at `1 - c` with the same drift machinery and the same panel, and it is
**0 of 15 at 10 bps with `L4_DD` binding at 14 of 15 cells** (B136 c=0.25: MaxDD -25.37% against
the -20.23% cap). Full gross-matching: CASHSHARE c=0.25 runs mean gross 0.750 against FIXED 0.10's
0.777 and still gives up 5.6 pp of drawdown and 0.115 of Sharpe. **The 4b pass is bought by
CONDITIONING the gross on volatility, not by holding less of the panel.**

## 4. Rule 8 (dial chosen on 2009-2016 only, 2017-2026 read once) — reported, not needed
| panel | family | IS pick | OOS read once | 4b OOS | 4a OOS | pre-stated rung agrees? |
|---|---|---|---|---|---|---|
| B136 | FIXED | t=0.10 | 13.01% / 1.2928 / -11.81% | PASS | PASS | n/a |
| B136 | SELFQ | q=0.20 | 11.76% / 1.3270 / -10.68% | PASS | **PASS** | no (pre-stated 0.50 also PASS 4b) |
| B136 | MEDMULT | m=0.70 | 11.79% / 1.2689 / -11.35% | PASS | **PASS** | no (pre-stated 1.00 also PASS 4b) |
| B136 | CASHSHARE | c=0.30 | 12.75% / 1.1267 / -21.15% | fail | fail | no |
| U56 | SELFQ | q=0.20 | 12.44% / 1.3870 / -11.29% | PASS | PASS | no (pre-stated 0.50 also PASS 4b) |
| U56 | MEDMULT | m=0.70 | 12.26% / 1.3567 / -12.13% | PASS | fail | no |
| SMALL665 | all four | — | 5.84-7.40% / 0.44-0.60 | 0 of 4 | 0 of 4 | — |

An IS chooser on a self-scaling family lands on a **tighter** rung than the pre-stated one at 5 of 6
large-panel arms and buys drawdown with it — SELFQ q=0.20 on B136 is the only cell in this run that
clears **both** paths out of sample. That is an IS-chosen result and is NOT the zero-IS claim; it is
logged for a future run, not promoted here.

## 5. What this does NOT show
* It is **not a dominance claim over the standing cell**: the zero-IS rule moves the thin 4b leg
  from CAGR (+1.92 pp there) to drawdown (+3.44 pp here) while widening the other (+5.39 pp CAGR).
  Idea 2060 showed the DD leg is the worst-resolved of the five; **this candidate has no error bar
  yet** and must not be quoted as more robust than the incumbent.
* Path **4a fails at every zero-IS cell** — the higher mean gross (0.900 vs 0.777) costs drawdown
  against the live book. 4b only.
* The FAMILY set is a choice of this run even though no dial was tuned: 4 of 9 pre-stated arms pass.
* SMALL665 is a clean **0 of 20 at every cost rung** (eighth confirmation for this family).
* SURVIVORSHIP: B136/U56 are current-constituent lists and SMALL665 is a current screen (54 tickers
  with `max_1d_move >= 1.0` dropped first); all levels are optimistic and both 4b bars are easier
  than on a point-in-time panel.

## Verdict
**ANSWERED + KEEP-candidate (4b, zero-chooser).** The vol target can be set with no in-sample
window at all, and the resulting rule clears 4b on both large panels, in both halves, out of
sample, and at 0-50 bps. Memo: `research/backtests/2026-09-21_zero-IS-target_KEEP4b_MEMO.md`.

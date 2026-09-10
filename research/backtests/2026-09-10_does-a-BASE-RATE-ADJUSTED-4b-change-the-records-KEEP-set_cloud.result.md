# Idea 481 — does a BASE-RATE-ADJUSTED 4b change the record's KEEP set? — **KILL** (2026-09-10, cloud)

Script: `research/backtests/2026-09-10_does-a-BASE-RATE-ADJUSTED-4b-change-the-records-KEEP-set_cloud.py`
Outputs: `.null.csv` (2,700 draws), `.census.csv` (34,382 recovered passes), `.floor.csv`,
`.candidate.csv`, `.walkforward.csv`, `.console.txt`.
Two tuned parameters and no more: FLOORQ (0.50/0.75/0.90/0.95/0.99, headline 0.90) and PANEL.
Sub-panel size k, null book, cost rung and every bar are reported at every point, never chosen.
Costs 10/25 bps, weekly, next-day execution (PROTOCOL 1-2).

## 1. Answer

**Yes — it removes 89.6% of it, and it rejects the project's only live 4b candidate.**
A pre-registered base-rate floor is a bar the record cannot pay, and idea 247's arm is the first
thing it kills. No KEEP.

## 2. The rule, pre-registered

BRA-4b: with `sd_null(bar | panel)` the sd of that 4b bar's slack across the panel's random
sub-panel draws, `z_bar = slack_bar / sd_null`, `min_z = min` over the five bars. A candidate
passes iff it passes 4b **and** `min_z > z*(panel, q)`, where `z*` is the q-th quantile of
`min_z` over the random draws that **themselves cleared 4b** on that panel. Plainly: beat the
q-th percentile of the coin flips that also cleared the bar.

## 3. The null reproduces idea 253's (GATE A)

3 panels x 3 k x 2 books x 150 seeded draws. Pooled 4b base rate **U56 28.2% (254/900)**,
**B136 23.0% (207/900)**, **SMALL 0.0% (0/900)** against idea 253's published 28.1% / 23.0% /
0.0% — |d| 0.1 pp and 0.0 pp. One deliberate deviation, stated up front: SMALL drops the 44
`max_1d_move >= 1.0` names first, so the gate is read on the two untouched panels. Base rate is
strongly k-dependent and reported at every point (U56 EWall 10.7% at k=14 -> 42.0% at k=42;
CAND20 0.0% -> 76.0%). `fast_backtest` matches `engine.backtest` to 1e-16; idea 247's ISFIX
threshold re-derives at **theta = 0.2125 exactly** (published 0.2125) with OOS armed share
16.4% (published 16.4%). Its IS armed share reads 19.9% here against a published 15.5% because
this run measures the armed share over the whole index and idea 247 measured it over the
post-warm-up evaluated window; the arm's headline metrics reproduce (section 5), so the
difference is a reporting window, not a different arm.

Floors: **U56** z*(q90) = +0.587 (254 random passes, median min-z +0.289); **B136** +0.508 (207,
+0.203); **SMALL** has fewer than 10 random passes so its floor is read on all 900 draws
(q90 = -3.196) and is not load-bearing.

## 4. The restatement — the record's KEEP set

294 committed CSVs yield 34,382 published 4b passes with recoverable metrics; **34,213 (99.5%)**
re-derive as passes against this run's panel SPY reference and the other 169 are excluded.

| q | U56 (N=22,533) | B136 (N=11,680) | pooled |
|---|---|---|---|
| 0.50 | 49.2% | 59.0% | 52.5% |
| 0.75 | 18.6% | 42.7% | 26.8% |
| **0.90** | **7.7%** | **15.6%** | **10.4%** (3,563/34,213) |
| 0.95 | 4.4% | 7.9% | 5.6% |
| 0.99 | 0.7% | 2.2% | 1.2% |

**At the headline q=0.90 the base-rate adjustment removes 89.6% of the record's reproduced 4b
passes.** Of the 3,563 survivors the binding bar is DD 2,065 and CAGR 1,326; the three Sharpe
legs bind on only 172 (4.8%) — the surviving margin is a drawdown and return margin, not a
Sharpe one. (SMALL contributes 14 recovered rows, 0 of which reproduce, so the panel is absent
from the restatement.)

## 5. Idea 247's live candidate

ISFIX(0.80) re-run rather than read off the record. U56 @10bps: CAGR 11.07% / Sharpe 1.2238 /
MaxDD -15.49%, halves 1.351/1.114, OOS Sharpe 1.212 — reproducing idea 247's published
11.05%/1.2201/-15.49% to rounding. It passes plain 4b in **4/6** panel-rung cells and BRA-4b in
**0/6 at every quantile from q=0.50 up**:

| panel | bps | min_z | binding | floor q90 | BRA-4b | percentile within the record's own passes |
|---|---|---|---|---|---|---|
| U56 | 10 | +0.183 | CAGR | +0.587 | FAIL | 32.6% |
| U56 | 25 | +0.068 | CAGR | +0.587 | FAIL | 10.3% |
| B136 | 10 | +0.366 | CAGR | +0.508 | FAIL (passes q50, q75) | 66.5% |
| B136 | 25 | +0.217 | CAGR | +0.508 | FAIL (passes q50) | 43.1% |
| SMALL | 10/25 | -2.79 / -3.08 | OOS | -3.196 | FAIL (fails plain 4b too) | — |

The binding bar is **CAGR in every cell**, with raw slack +0.0046 (10 bps) and +0.0017 (25 bps)
on U56 — 0.18 and 0.07 of one panel noise unit. This is the same thin CAGR floor idea 247 itself
flagged (+0.42 pp / +0.13 pp); the base-rate adjustment prices it and finds it inside the noise.
**4a 0/6.**

## 6. Rule 8 — the floor re-fitted on IS alone, OOS read once

| panel | raw base rate IS -> OOS | q90 floor (IS-fitted) | admits IS | admits the SAME draws OOS |
|---|---|---|---|---|
| U56 | 4.3% -> **51.8%** | +0.612 | 0.4% | **21.8%** |
| B136 | 21.4% -> 21.9% | +0.526 | 2.2% | **2.1%** |
| SMALL | 0.0% -> 0.0% | -2.220 | 0.0% | 0.0% |

**The floor is calibration-stable on B136 (2.2% -> 2.1%) and not on U56 (0.4% -> 21.8%)** —
because U56's own raw base rate moves 12x between the windows, confirming and sharpening idea
253's non-transfer finding. A base-rate floor is therefore a per-panel, per-window object: it
cannot be published as one number.

The candidate under the IS-fitted floor, OOS read once: IS-admitted on B136 only (min_z 0.784
vs floor 0.526), **OOS-admitted nowhere**. Its OOS numbers are nonetheless real — U56 @10bps OOS
CAGR 11.21% / Sharpe 1.2122 / MaxDD -15.49% against RULES v2 9.48% / 1.2788 / -12.05% and SPY
15.32% / 0.8758 / -33.72%: it beats SPY on OOS Sharpe by +0.34 and loses to the live book by
-0.067, and its CAGR is 73% of SPY's, which is exactly why the CAGR floor is the bar it cannot
clear with margin.

## 7. Verdict and what it implies

**KILL.** 4a 0/6; the candidate passes 4b in 4/6 cells and BRA-4b in 0/6; no arm in this run is
capital-worthy, so RULES.md is untouched and no memo is written.

For Sunday review, not adopted here: PROTOCOL 4b currently has no noise scale, and 89.6% of the
passes the record has published on it sit inside their own panel's coin-flip null at q=0.90. The
cheapest honest repair is not a floor constant — rule 8 shows the floor does not transfer on U56
— but a **required column**: every 4b pass should publish its `min_z` against its own panel's
random-sub-panel null, so a reader can see the margin in noise units beside the raw one.

SURVIVORSHIP (PROTOCOL 9, idea 54): B136 and SMALL are current-constituent lists, so their
levels are biased upward and unequally so. Every statistic here is a within-panel contrast (an
arm against its own panel's null), which is what a base-rate adjustment is; U56 is a fixed
ETF/mega-cap list and is least biased. SMALL drops the 44 names with `max_1d_move >= 1.0`.

# Idea 239 — publish EWall beside every panel claim (cloud, 2026-09-08)

**SPLIT. The column is BUILT and back-filled over 1.33 million published claim rows, and it
answers the queue's question — but the premise that motivated it is FALSIFIED: over the record,
EWall is a WORSE predictor of a book's OOS Sharpe than the book's own IS Sharpe, and it is a
PANEL CONSTANT with exactly three distinct values in the whole corpus.** No RULES change, no
KEEP, no memo; `RULES.md`, `scan.py`, `bot.py`, `baseline.py` and `PROTOCOL.md` untouched.

Two tuned parameters and nothing else: the control's GROSS `g ∈ {0.50, 0.75, 1.00}` and its
CADENCE `∈ {W, M}`. All 6 points are reported at both cost rungs.

## The queue's question, answered three ways

| reading | share with **zero or negative excess** over its own un-ranked control |
|---|---|
| per CLAIM ROW (1,331,568 rows, 676 files) | **83.7%** (83.4–85.3% across all 6 conventions at 10 bps) |
| per FILE, mean claim | **91.9%** |
| per FILE, **best** claim | **5.0%** |

Read all three together, because they are the finding. The typical published panel claim does
not clear the panel's own un-ranked equal-weight book: mean excess **−0.19** Sharpe, median
**−0.15**. But almost every file contains *some* row that does — only 5% of files fail to
produce one — which is what a published grid is for. **The record's panel claims are grids
whose winners clear the un-ranked bar and whose bodies do not**, so a claim quoted without its
own grid's un-ranked control is uninterpretable.

Panel-by-panel at the record's own convention (g 0.75, weekly, 10 bps):

| panel | control Sharpe | claim rows | zero-excess | mean excess | best excess |
|---|---|---|---|---|---|
| u56 | **+1.1240** | 540,882 | **76.2%** | −0.1417 | +0.5543 |
| broad136 | **+1.1220** | 503,317 | **90.0%** | −0.2147 | +0.7101 |
| small439 | **+0.6781** | 287,369 | **86.7%** | −0.2494 | **+1.6303** |

R2 is **refuted on the share and confirmed on the tail**, which is the more useful reading.
small439's control has by far the lowest Sharpe (0.678 against ~1.12) yet its claims clear it
*less* often than u56's clear a bar 0.45 higher (86.7% vs 76.2% zero-excess) and by a worse
average margin (−0.2494 vs −0.1417). What the low bar does buy is the tail: small439 carries
the record's single largest excess at **+1.63**, more than double either large-cap panel's
best. On the weakest panel the un-ranked control is easy to beat *occasionally* and hard to
beat *typically* — the opposite of what a low bar is usually taken to mean.

## The premise: idea 77's predictor claim does not survive being stated over the record

4,507 cells over 82 files carry a matched (IS_Sharpe, OOS_Sharpe) pair *and* a resolvable panel.

| convention | distinct EWall values | ρ(EWall, OOS) cells / units | ρ(own IS, OOS) cells / units |
|---|---|---|---|
| any of the 6 | **3** | +0.638 / +0.795…+0.801 | **+0.742 / +0.802** |

Two things kill the claim, and the second is the one that matters:

1. **It loses.** The book's own IS Sharpe is the better predictor of its OOS Sharpe on both
   units — +0.742 vs +0.638 per cell, +0.802 vs +0.801 per (file, panel). Idea 77's ordering
   (+0.857 EWall vs +0.821 own-IS) **reverses** when the same comparison is made over the
   record rather than over idea 77's own seven-point panel set.
2. **It cannot separate anything.** EWall Sharpe takes **one value per panel** — three values
   in the entire corpus — so ρ(EWall, OOS) *within* a panel is undefined by construction, for
   every panel. A predictor constant across every book on a panel cannot rank two books on that
   panel; the correlation it earns across panels is a **three-point statistic**, and the
   between-panel ordering it encodes (u56 ≈ broad136 > small439) is already published as the
   panel's own name. R3 confirmed.

That is the honest reason the column should be published as a **bar**, not as a **predictor**.

## The back-fill's own error (gate G2), reported not buried

153,444 of the record's own rows carry a labelled un-ranked arm beside a panel column. This
run's back-filled column against them:

| convention | mean abs diff | median | p90 | corr |
|---|---|---|---|---|
| g 0.50 W | 0.1001 | 0.0648 | 0.222 | +0.808 |
| g 1.00 W (closest) | **0.0999** | 0.0647 | 0.222 | +0.808 |
| worst (g 0.50 M) | 0.1025 | 0.0659 | 0.222 | +0.809 |

**Mean absolute error ≈ 0.10 Sharpe, and it is flat across all six conventions.** Two readings
follow, and the second is a caveat the run refuses to hide: (a) the two tuned dials barely move
the column at all — Sharpe is close to scale-free in gross, so `g` changes u56's control Sharpe
by 0.0007 across the whole 0.50→1.00 ladder — which is why the rule-8 spread below is tiny;
(b) the record's own "control" rows are **not all plain EWall** — many are a dial's declared
incumbent (a gated or de-grossed book wearing the label), so 0.10 **bounds the back-fill's
error from above and does not measure it.** Excesses within ±0.10 Sharpe of zero should not be
read as signed.

## Coverage limit, stated up front

1,984 committed CSVs scanned → **683 carry a panel column and a Sharpe** (718 no panel column,
583 panel but no Sharpe). Of their 1,390,645 claim rows, **1,331,568 (95.8%) map** to one of the
three priceable panels through a fully published alias table. The remaining **59,077 rows over
72 files do not and are not guessed**: `bstk100` (5,610), `BSTK100` (5,200), `B80held` (2,415),
`ETF36` (1,751), `STK20` (505), `ETF24` (492), plus 882 seeded sub-universe labels
(`B136k80d23`, …) — sub-panels and draws this run cannot price exactly. Every one is listed with
its row count in `.aliases.csv`.

## Rule 8 on both dials

| convention | IS zero-excess (files < 2026-09-06) | **OOS zero-excess** (files ≥) |
|---|---|---|
| g 0.50 W | 84.8% | 83.3% |
| g 0.50 M | 85.9% | 85.0% |
| g 0.75 W | 84.7% | 83.3% |
| g 0.75 M | 85.6% | 84.8% |
| **g 1.00 W** (chosen in sample) | **84.2%** | **83.1%** |
| g 1.00 M | 85.2% | 84.4% |

20 seeded FILE splits pick g 1.00 W in **20/20**; held-out zero-excess share mean **83.0%**
(min 80.0%, max 85.3%) against 83.6% in sample. **The headline moves by 0.6 pp out of sample
and by at most 1.9 pp across the entire parameter grid**, so the two tuned dials are not where
this number comes from — which is the strongest thing that can be said for a back-filled column
and is exactly what a reporting column needs to be.

## Both KEEP paths on the 36 control books

The un-ranked controls are books, so they are priced as books (10 and 25 bps, next-day
execution, full sample + halves + OOS):

| panel | book | CAGR | Sharpe | MaxDD | H1 / H2 | OOS Sharpe | 4a | 4b |
|---|---|---|---|---|---|---|---|---|
| u56 | EWall g0.50 W | 8.81% | 1.1233 | −15.46% | 1.188 / 1.072 | 1.1359 | ✗ | ✗ |
| u56 | EWall g1.00 W | 17.74% | 1.1245 | −29.18% | 1.192 / 1.072 | 1.1353 | ✗ | ✗ |
| broad136 | EWall g1.00 W | 18.92% | 1.1220 | −32.72% | 1.233 / 1.023 | 1.1006 | ✗ | ✗ |
| small439 | EWall g1.00 W | 13.12% | 0.6770 | −46.03% | 0.797 / 0.612 | 0.6351 | ✗ | ✗ |
| — | RULES v2 (live) | 8.66% | 1.2056 | −12.05% | 1.226 / 1.191 | 1.2851 | — | — |
| — | SPY | 15.23% | 0.8890 | −33.72% | 0.957 / 0.834 | 0.8820 | — | — |

**36 control books: 4a 0/36, 4b 0/36, 4b(OOS) 0/36, BOTH 0/36. No KEEP-candidate, no memo.**
The failures are informative and come from opposite directions: on u56 the g 0.50 rung clears
the drawdown cap (−15.5% vs the −20.2% bar) and misses the CAGR floor (8.81% vs 10.66%), while
g 0.75 and g 1.00 clear the CAGR floor and miss the drawdown cap (−22.5%, −29.2%). If a 4b
window in gross exists on u56 it lies strictly inside (0.50, 0.75), which this run's 3-rung
ladder cannot resolve — consistent with idea 439's reading of 4b as a window in gross.

## Pre-registered predictions vs outcome

| | prediction | outcome |
|---|---|---|
| R1 | a large minority, plausibly a majority, of claims have zero excess | **CONFIRMED, at the high end** — 83.7% of rows, 91.9% of files by mean claim |
| R2 | the zero-excess share is panel-dependent, worst on small439 | **REFUTED on the share** — small439 (86.7%) sits between broad136 (90.0%) and u56 (76.2%), so the lowest bar is not the easiest to clear; **confirmed on the tail** — small439 carries the record's largest single excess (+1.63) |
| R3 | idea 77's predictor claim will not survive: EWall is a panel constant | **CONFIRMED** — 3 distinct values corpus-wide, within-panel ρ undefined, and it loses to own-IS (+0.638 vs +0.742) |
| R4 | the back-filled column agrees with files' own un-ranked arms | **QUALIFIED** — corr +0.81, mean abs diff 0.0999 Sharpe, which is an upper bound because the record's `control` label is not always plain EWall |

## Survivorship

small439 is current constituents of a sub-$2B screen (tickers with `max_1d_move >= 1.0` in
`data/small_meta.csv` dropped first, 439 remaining) and broad136 is current constituents
(PROTOCOL 9). The EXCESS column is a same-panel, same-window, same-cost contrast, so the bias
is common to both of its sides; the **absolute** control Sharpes in the tables above are
upward-biased on those two panels and should not be read as investable levels.

## What the queue should take from this

1. **239 is answered: 83.7% of published panel claim rows, and 91.9% of files by mean claim,
   have zero or negative excess over their own un-ranked control** — but only 5.0% of files
   fail to produce at least one row that clears it. Publish the bar per *file*, not per row.
2. **Idea 77's motivating comparison should be marked corrected.** Over the record, the
   un-ranked control is a worse OOS predictor than the book's own IS Sharpe, and it is a panel
   constant that cannot rank two books on the same panel at all.
3. The column is cheap, insensitive to both of its free parameters (1.9 pp across the whole
   grid, 0.6 pp out of sample) and bounded in error by ~0.10 Sharpe. It is worth publishing as
   a **reference bar beside every panel claim**; it is not worth publishing as a predictor, and
   no excess inside ±0.10 Sharpe should be read as signed.

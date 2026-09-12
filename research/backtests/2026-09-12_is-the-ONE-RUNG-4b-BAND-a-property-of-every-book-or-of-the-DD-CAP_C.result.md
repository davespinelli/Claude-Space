# Idea 804 — is-the-ONE-RUNG-4b-BAND-a-property-of-every-book-or-of-the-DD-CAP (lane C, 2026-09-12)

**ANSWERED = IT IS THE DD CAP, AND IT IS ARITHMETIC. The 4b gross band is the DD cap's upper edge
meeting the CAGR floor's lower edge with LITERALLY nothing else in play: over 60 pre-declared books
x 17 gross rungs, the band equals (DD set) ∩ (CAGR set) in 29 of 29 banded books, every uncensored
lower edge is bound by CAGR alone (29/29) and every uncensored upper edge by DD alone (20/20), and
the three Sharpe legs are slack in 100% of cases. All 6 pre-registered hypotheses PASS, including
the strong one: the band is predictable in CLOSED FORM from a single g=1.00 backtest in 47 of 60
books, every miss by at most one rung. Idea 574's "one rung" is therefore not a property of any
book — it is a property of the 4b bar. KEEP-candidate (4b), path 4b only: the IS-only band-midpoint
selector's one-shot OOS read, B136/R620/g0.65/W — but see the caveat, it is a gross-rung restatement
of the standing 2026-09-04 top-20 equal-weight candidate, not an independent discovery. 4a: 0 of
1,020 cells.**

Script: `2026-09-12_is-the-ONE-RUNG-4b-BAND-a-property-of-every-book-or-of-the-DD-CAP_C.py`
Artefacts: `.grid.csv .legs.csv .bands.csv .arith.csv .walkforward.csv .wfb.csv .keeppaths.csv
.console.txt`

## Gates (printed before any band number)

| gate | reading | bar | verdict |
|---|---|---|---|
| G1 engine | `fast_backtest` vs `engine.backtest`, U56/CAND20/g0.75 | 1.388e-17 | 1e-9 **PASS** |
| G2 linearity | max \|w(g) − g·w(1)\| over 6 forms x 3 grosses | 6.939e-18 | 1e-12 **PASS** |
| G3 comparands | printed as numbers, below | — | — |
| G4 continuity | 574's five banded books, re-read here | measured, not gated | see below |

Window 2009-01-13..2026-09-11, 4,443 bars. **RULES v2 (U56, live)** 8.63% / 1.2018 / −12.05%
(halves 1.2349/1.1757; OOS 9.47% / 1.2782 / −12.05%). **SPY** 15.16% / 0.8861 / −33.72%
(halves 0.9595/0.8259; OOS 15.33% / 0.8767 / −33.72%).

**The five 4b bars, as numbers:** H1 Sharpe > 0.9595 · H2 Sharpe > 0.8259 · OOS Sharpe > 0.8767 ·
MaxDD ≥ −20.23% · CAGR ≥ 10.61%. (Each book is judged against SPY on its own panel's window.)

## The mechanism, in one table

Every leg's admissible gross set, classified mechanically over all 60 books:

| leg | ALL | LOWER | UPPER | NONE | reading |
|---|---|---|---|---|---|
| H1 | 43 | 0 | 0 | 17 | **gross-invariant in 60 of 60** |
| H2 | 36 | 0 | 2 | 22 | gross-invariant in 58 of 60 |
| OOS | 41 | 0 | 0 | 19 | **gross-invariant in 60 of 60** |
| DD | 18 | **42** | 0 | 0 | falls as gross rises, 60 of 60 |
| CAGR | 0 | 0 | **42** | 18 | rises with gross, 60 of 60 |

A Sharpe leg is `ALL` or `NONE` in 178 of 180 book-legs: **it either admits the whole ladder or
kills the book outright, and in neither case can it cut a band edge.** The two LEVEL legs are the
only ones that move with the dial, and they move in opposite directions. That is the whole
mechanism, and B136/R620/W shows it bare — across a 5x range of gross its Sharpe moves 1.1217 →
1.1296 (0.008) while CAGR moves 4.56% → 23.18% and MaxDD moves −6.28% → −28.75%.

## The answer

| | reading | |
|---|---|---|
| books with a non-empty band | 29 of 60 | |
| band width (rungs of 17) | median **2.0**, mean 2.34, min 1, max 4 | H_NARROW **PASS** |
| contiguous in g | 29 of 29 | |
| **band == DD ∩ CAGR** | **29 of 29 (100%)** | H_SUFF **PASS** (bar 70%) |
| uncensored lower edges bound by CAGR alone | **29 of 29** | H_LOWER **PASS** |
| uncensored upper edges bound by DD alone | **20 of 20** (9 censored at g=1.00) | H_UPPER **PASS** |
| DD LOWER-shaped / CAGR UPPER-shaped | 60 of 60 / 60 of 60 | H_SHAPE **PASS** |

Per-leg slack rate among the 29 banded books (1.00 = the leg never changes the band):
**H1 1.00 · H2 1.00 · OOS 1.00 · DD 0.31 · CAGR 0.00.** Removing all three Sharpe legs from
PROTOCOL 4b would not move a single band endpoint in this book set.

## H_ARITH — the band from one backtest

If the Sharpe legs are gross-invariant and the level legs are proportional to gross, then from the
g = 1.00 cell alone plus SPY:

    g_lo* = 0.70 · CAGR_SPY / CAGR(1.00)        g_hi* = 0.60 · MaxDD_SPY / MaxDD(1.00)

**Exact band match in 47 of 60 books (78%) — PASS (bar 70%)**, consuming 1 of 17 rungs and
predicting the other 16. Over the 29 books non-empty in both, the edge error is 0.0 rungs at the
median and **|error| ≤ 1 rung at BOTH edges in 29 of 29**. Every miss is in the same direction —
the closed form predicts a band one rung too WIDE — because CAGR is slightly convex and MaxDD
slightly sub-linear in gross, not because another leg intervened.

**A 17-rung gross sweep of a 4b claim is therefore 16 rungs of wasted compute.** One run at g=1.00
plus SPY gives the band to within a rung.

## Rule 8 (run whatever the verdict)

IS ≤ 2016-12-31, OOS ≥ 2017-01-01, read once. Inside a window the OOS leg *is* that window's own
H2 — stated, not hidden — so a window band is four distinct legs, not five.

**WF-A (the answer walked forward).** 33 of 60 books carry an IS band, 27 an OOS band, 23 both.
The **binding-leg pair agrees IS vs OOS in 22 of 23 (96%) — H_WF PASS (bar 60%)**, and the one
disagreement (BSTK100/BAND3/M) is a censoring change, not a change of leg: CAGR/CENSORED → CAGR/DD.
DD∩CAGR sufficiency holds in 58 of 60 inside IS and 58 of 60 inside OOS. **The decomposition is the
same object out of sample; the band's LOCATION is not** — IS bands are systematically wider (e.g.
B136/R620/W 9 rungs IS vs 4 OOS), so an IS-fitted band over-states its own admissible range.

**WF-B (a book walked forward).** Both selectors fitted on IS alone, OOS read ONCE, 10 bps.
Comparands OOS: RULES v2 9.47% / 1.2782 / −12.05%; SPY 15.33% / 0.8767 / −33.72%.

| selector | book | g | OOS CAGR | OOS Sharpe | OOS MaxDD | 4a | 4b legs failing OOS |
|---|---|---|---|---|---|---|---|
| **IS-BAND-MIDPOINT** | B136/R620/W | 0.65 | **14.52%** | **1.0400** | **−19.43%** | False | **none** |
| IS-SHARPE | U56/R620/M | 1.00 | 22.30% | 1.1152 | −30.59% | False | **DD** |

This is the practical consequence of the decomposition and it reproduces idea 574's WF-B finding
from the other side: **the IS-Sharpe selector walks straight past the band to g = 1.00 and dies on
the drawdown cap, because Sharpe cannot see the dial it is turning.** A selector that reads the
band instead lands inside it and clears all five legs out of sample.

## KEEP paths (both evaluated at every cell)

| cost | cells | 4a | 4b | BOTH |
|---|---|---|---|---|
| 10 bps | 1,020 | **0** | **68** | **0** |
| 25 bps | 1,020 | 0 | 40 | 0 |

Fail-4b leg census at 10 bps: CAGR alone 354, DD alone 151, H1+H2+OOS+CAGR 127, **PASS 68**,
H2+OOS+CAGR 68, all five 54, H1+CAGR 51, … — **the two level legs alone account for 505 of the 952
failures**, and no cell anywhere passes 4a.

**KEEP-candidate (4b), path 4b only: `B136/R620/g0.65/W`.** Full sample 14.99% / 1.1264 / −19.43%,
halves 1.3425 / 0.9558, against SPY 15.16% / 0.8861 / −33.72% — all five legs clear (CAGR 14.99% ≥
10.61% floor, MaxDD −19.43% ≥ −20.23% cap). It survives the 25 bps rung (band 0.55–0.65 there), its
band is the widest in the set (4 rungs), and it was selected on IS alone and read once on OOS.

## Caveats — read these before the memo

* **This is not an independent discovery.** `B136/R620/W` is top-20-by-6-month-return, equal
  weight, weekly — a broad-panel cousin of the standing 2026-09-04 KEEP 4b (top-20 equal-weight, no
  vol scaler). It is best read as that candidate's gross rung being *located* rather than guessed.
* **The selector searched this run's own grid.** "IS-only" constrains the window, not the 60 x 17
  space it chose from. One OOS read of one cell is weak evidence next to 1,020 cells of IS freedom.
* **Survivorship.** All five panels are CURRENT constituents (SMALL is its screen's current list
  with the 52 `max_1d_move ≥ 1.0` tickers dropped per PROTOCOL). Dead names are absent, so every
  CAGR is biased upward — which makes the CAGR floor **easier** than on a point-in-time panel and
  therefore makes the lower edge look **less** binding than it truly is. The bias works against this
  run's finding, not for it.
* **G4 continuity.** 574's five banded books re-read here give widths 2 / 1 / 1 / 0 / 0 against the
  2 / 1 / 1 / 0 / 0 it published — agreement on all five, though 574 pinned its books from
  leaderboard prose and this run declares them, so this is corroboration, not reproduction.
* The upper edge is CENSORED at g = 1.00 for 9 of 29 banded books; those are counted as censored
  and never as "bound by" anything. PROTOCOL forbids leverage, so the ladder cannot be extended.

## Consequence for the record

The queue asked whether the one-rung band is a property of every book or of the DD cap. **It is
neither a book property nor even a DD-cap property alone: it is the width of the interval between
two straight lines**, one set by 0.70·CAGR_SPY and one by 0.60·MaxDD_SPY, and a book's only input is
its return-per-unit-gross and drawdown-per-unit-gross. Two consequences the record should act on:

1. **Every 4b claim quoted at one gross should publish `g_lo*` and `g_hi*` beside it.** They cost
   nothing — the numbers are already in the run that produced the claim.
2. **The three Sharpe legs of PROTOCOL 4b did no work in 29 of 29 bands here.** They still screen
   books (they kill 17–22 of 60 outright), but they never choose a gross. Any future selector that
   picks gross by Sharpe is picking blind, and will land at g = 1.00 on the wrong side of the cap.

No RULES, PROTOCOL, scan.py, bot.py or baseline.py edit; nothing outside this run's own outputs was
touched.

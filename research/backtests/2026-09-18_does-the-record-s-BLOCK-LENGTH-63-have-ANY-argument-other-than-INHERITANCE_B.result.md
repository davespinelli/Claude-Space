# Idea 1241 (lane B, 2026-09-18) — does the record's BLOCK LENGTH 63 have ANY argument other than INHERITANCE?

**VERDICT: NO. 63 has no argument on this tape. KILL (capital) — no new book, no RULES change.
PUBLISHING NOTE EARNED (rule 6, Sunday review).** 15 of 15 gates, 86s, offline, deterministic.

Dials (PROTOCOL rule 4, max 2): **ESTIMATOR** {PW_SB, PW_CB, HHJ, VMATCH} and **PANEL** {U56,
B135, SMALL663, SPY}. All 16 cells published at each of 3 SERIES kinds x 2 WINDOWS in
`.blocklen.csv` (928 estimates including every S_DIFF pair). SERIES and WINDOW are controls,
reported at every value, never chosen on.

## 1. The tape asks for a block length near 3, not 63 (ARM A)

Politis-White plug-in (Patton-Politis-White 2009 constants) on the frozen 2026-09-04 book's
**Sharpe influence function**, full sample:

| panel | n | PW_SB | **PW_CB** | HHJ | VMATCH | 63 / PW_CB |
|---|---|---|---|---|---|---|
| U56 | 4,447 | 3.05 | **3.49** | 12.72 | 13 | **18.1x** |
| B135 | 4,443 | 2.23 | **2.55** | 5.09 | 21 | **24.7x** |
| SMALL663 | 3,938 | 2.49 | **2.85** | 12.55 | 5 | **22.1x** |
| SPY | 4,447 | 5.66 | **6.47** | 12.72 | 8 | **9.7x** |

Median PW_CB over all 11 full-sample (panel x series) cells **3.46**; 63 is **18.2x** it.
Over all 928 published estimates the median is **4.52** and **0.9601 sit below 63**; the 37 at or
above it are the VMATCH ladder's own top rungs on single difference series, not panel-level
answers. **H_FAR HELD.** The estimator is sound on known inputs: seeded iid noise returns
**1.21**, a seeded AR(1) with phi = 0.8 returns **42.92** (gates G3/G4).

## 2. But "the tape's optimal L" is not a sharp quantity either — H_AGREE FAILED

The four estimators span **10.35x** over the full-sample cells (min 2.09, max 21.66) and only
**2 of 11** cells have all four within 3x (median spread **4.96x**, worst 9.43x). VMATCH is at
least *identified* — the bootstrap SD spread over the 1..504 ladder is 1.38-1.88 at 8 of 8 cells,
so the rungs are distinguishable — but the rungs **within 5% of the HAC target** run [1, 42] on
U56 and [1, 63] on B135. So the honest finding is two-sided and both halves matter:
**no principled estimate is anywhere near 63, and no principled estimate is a point either.**
63 is not merely unargued; the class of arguments that could support it does not resolve to a
number on ~4,400 rows of daily data.

## 3. It is NOT harmless: 63 inflates the record's own resolved count — H_NOCHANGE FAILED

Read off idea 1208's committed `.Ldependence.csv` — **the same 72 decisions, re-read, not
re-derived** (gate G6 reproduces its 16/72 at L=63 and 14/72 at L=21):

| L-hat | value | brackets on 1208's ladder | resolved of 72 | vs L=63's 16 |
|---|---|---|---|---|
| PW_CB median (all cells) | 3.46 | [2, 5] | **12** | **-4** |
| PW_CB U56 S_PSI | 3.49 | [2, 5] | **12** | **-4** |
| VMATCH median | 13.00 | [10, 21] | 13..14 | -3..-2 |
| HHJ median | 12.55 | [10, 21] | 13..14 | -3..-2 |

At the block length the tape actually asks for, **4 of the record's 16 "resolved" verdicts stop
being resolved — a 25% inflation** carried entirely by the inherited rung. The ladder is
monotone (11/12/12/13/14/16/16/17/20/23/34 at L = 1..1008), so this is a one-directional bias:
**every committed decisiveness claim written at L=63 is quoted from a rung more generous than the
tape's own.**

## 4. And none of it is worth money (ARM C, rule 8) — H_CAPITAL failed on a single cell

108 books (N {10,12,16,20,25,30} x H {21,42,63,126,189,252} on 3 panels), 10 bps, t+1, 260-row
warm-up, both KEEP paths at every cell, parameters chosen on warm-up..2016-12-31 and **2017-2026
read once**. **4a 0 of 108** (A_DD fails at 108 of 108 against live RULES v2's -12.05% MaxDD).
**4b 11 of 108** — U56 9, B135 2, SMALL663 0; binding leg the DD cap (fails 97 of 97 failures),
then H2 40, OOS 38, H1 29, CAGR 21. Every 4b pass is prior art: the incumbent's own family.

The decisiveness bar as a chooser, pooled over 3 panels:

| chooser | mean OOS Sharpe | delta vs do-nothing | moves | 4b passes among picks |
|---|---|---|---|---|
| C_ANCHOR (do nothing) | 0.8869 | +0.0000 | 0 | **1 of 3** |
| C_ISSHARPE (no bar) | 0.9831 | +0.0962 | 3 | 0 of 3 |
| C_DEC_L21 | 0.8869 | +0.0000 | 0 | 1 of 3 |
| C_DEC_L63 (inherited) | 0.8406 | **-0.0463** | 1 | 0 of 3 |
| C_DEC_LHAT | 1.0168 | +0.1299 | 1 | 1 of 3 |
| C_DEC_L252 | 0.8406 | -0.0463 | 1 | 0 of 3 |
| C_DEC_L504 | 0.7975 | -0.0894 | 2 | 0 of 3 |
| C_RANDOM | 0.8727 | -0.0141 | 1 | 0 of 3 |

H_CAPITAL is **FAILED by the letter and empty on inspection, and it is reported that way.**
The bar fires **8 times in 525 pair-tests (0.0152)**. C_DEC_LHAT's +0.1299 is a mean of three
numbers of which two are exactly 0.0000: the whole of it is **one decision on SMALL663**, where
L-hat = 1 (an iid redraw, the most generous possible SE) made 2 pairs decisive and picked
(N=12, H=252) — **the identical cell C_ISSHARPE picks with no bar at all**, so the bar
contributed nothing beyond moving, and the pick fails 4b with an OOS MaxDD of **-41.35%** on the
panel with **0 of 36** 4b passes. On U56, the only panel carrying a 4b-passing book, every bar
that fires **loses** (-0.1389, and it picks the same cell C_ISSHARPE does). The inherited L=63
bar is **-0.0463**, worse than doing nothing and worse than a count-matched random move.

## 5. Benchmarks and the incumbent (unchanged, replayed)

U56 SPY full 15.13% / 0.8849 / -33.72% (halves 0.9600 / 0.8236), OOS 15.28% / 0.8747 / -33.72%;
live RULES v2 @ 10 bps 8.62% / 1.2018 / -12.05%, OOS 9.47% / 1.2781. The frozen 2026-09-04 U56
anchor (N=20, H=126, G=0.75, weekly) replays **15.78% / 1.1522 / -19.13%**, halves 1.2127 /
1.1128, **OOS 17.28% / 1.1832 / -19.13%**, turnover 2.75/yr — 4b PASS, prior art, not promoted.
Gate G1 pins it to the 2026-09-16 vintage the committed triple was produced on (max dev < 1e-4).

## 6. For the Sunday review — PUBLISHING NOTE ONLY (rule 6, no RULES/PROTOCOL change here)

> A committed decisiveness or resolution claim must state its block length L **and** the fact
> that L = 63 is an inherited convention, not a fitted one. Where the claim is load-bearing it
> should quote the count at a plug-in L as well: on this tape the Politis-White circular-block
> optimum is **2.5-6.5** across panels and 63 resolves **4 more of 72** decisions than it does.

## 7. Caveats

**SURVIVORSHIP (rule 9):** U56 and B135 are current-constituent lists; SMALL663 is a current
sub-$2B screen (52 of 715 names dropped on `max_1d_move >= 1.0`). Every ARM C level is an upper
bound. ARM A is a question about dependence structure, not level, so a common level bias does not
move an autocorrelation — but the series are still the *surviving* names' series, so even the
block lengths are the survivors'. ARM B re-reads committed numbers and changes none of them.
**The plug-in is a plug-in.** PW is derived for a sample mean; S_PSI is the correct input for a
Sharpe and is reported beside the naive S_RAW, but a plug-in optimal for estimating a *variance*
is not automatically optimal for a *decision rule*, and section 2 is the reason not to over-read
the point. **HHJ carries a pilot:** its target is the full-sample bootstrap SD at the PW_CB rung,
stated rather than hidden, so HHJ is not independent evidence of PW's level.
**n = 3 panels** in the rule-8 table; the per-panel decomposition is printed precisely because
the pooled mean of three numbers is not a sample.

Script: `2026-09-18_does-the-record-s-BLOCK-LENGTH-63-have-ANY-argument-other-than-INHERITANCE_B.py`
Artefacts: `.blocklen.csv` (928 estimates), `.grid.csv` (108 books x both KEEP paths),
`.walkforward.csv` (24 rule-8 picks), `.pairs.csv` (525 pair-tests), `.resolution.csv`,
`.gates.csv`, `.console.txt`.

# Idea 1254 (lane B, 2026-09-17) — is the 2026-09-04 KEEP 4b book's OOS pass carried by a handful of years?

**VERDICT: KILL (capital) — no new book. The premise is HALF-CONFIRMED, and the half that
confirms is the OPPOSITE of the one the idea guessed. The RETURN side of the 4b pass is not
year-carried at all. The DRAWDOWN side is carried by exactly ONE year — 2020 — and not because
2020 was good for the book, but because 2020 was bad for SPY, and 4b's drawdown cap is
60% of SPY's own MaxDD.**

## What was run
The frozen 2026-09-04 candidate (U56 / 3-leg composite 21-252, 0-126, 0-63 / **no vol scaler** /
above-own-200d and vol20 < 0.60 / top **N=20** equal weight / min hold **H=126** / **gross 0.75**
of NAV, gated-out weight to CASH / calendar-weekly = the Monday-execution book, 1253 G9), 10 bps,
decide-at-t / apply-at-t+1, 260-row warm-up. The book is **not rebuilt** — positions are history.
What is deleted is the **scoring window**: the days of a set of calendar years are removed from
the daily return stream of the book, of SPY and of LIVE RULES v2 **identically**, and every leg
(full / H1 / H2 / OOS) is recomputed on the surviving days. Dials: **k = deletion count 0..5,
EXHAUSTIVE over every subset** x **PANEL {U56, B136, SMALL663}**. Arena {OOS 2017-26, IS 2009-16}
is reported at both values, not a dial. **2,571 grid points, all published** in `.grid.csv`;
3 rule-8 rows in `.walkforward.csv`; 6 kill-depth rows in `.kill.csv`. **4 of 4 gates pass**,
33s, offline, deterministic.

**A METHOD ERROR FOUND AND PUBLISHED RATHER THAN QUIETLY FIXED (rule 7).** This script's first
draft asserted that spliced MaxDD is biased *toward* the book (a deleted year removes its own
trough). That is wrong, and the tape says so: deleting 2019 concatenates the Q4-2018 and
Q1-2020 troughs into a **-27.24%** drawdown *that never happened* (true -19.13%), and the first
draft scored that as a 4b failure. Every DD verdict is therefore published under **two**
conventions at every grid point: `DD_SPLICE` (naive, contaminated) and **`DD_SEG`** (worst
drawdown *within* a contiguous surviving segment, never spanning a cut) — the headline. The
spliced convention manufactures 2 of 10 single-year failures on U56; the splice-immune one
leaves 1. All numbers below are DD_SEG.

## The numbers (U56 — the only panel where the question has content)
Window 2009-01-13..2026-09-16, 4,446 days. **SPY 15.06% / 0.8815 / -33.72%, halves 0.9600/0.8171,
OOS 15.15% / 0.8686 / -33.72%. LIVE RULES v2 8.60% / 1.1982 / -12.05%, OOS 9.42% / 1.2717.
BOOK k=0 15.71% / 1.1480 / -19.13%, halves 1.2127/1.1050, OOS 17.16% / 1.1759 / -19.13%** —
G1/G2/G3 replay the committed triple and both benchmarks to <5e-3. 4b PASSES at k=0
(margins H1 +0.2527, H2 +0.2879, **OOS +0.3074**, **DD +0.0110**, CAGR +0.0517); 4a fails, as the
record already holds.

### The return side is NOT year-carried
| k | subsets | 4b pass | book OOS Sharpe range | **OOS-leg failures** | worst OOS margin |
|---|---|---|---|---|---|
| 0 | 1 | 1 | 1.1759 | 0 | +0.3074 |
| 1 | 10 | **9** | 1.0594..1.3762 | **0** | +0.2251 |
| 2 | 45 | 36 | 0.9784..1.5454 | **0** | +0.0673 |
| 3 | 120 | 85 | 0.8917..1.6817 | 2 | -0.0089 |
| 4 | 210 | 132 | 0.7994..1.8003 | 5 | -0.1379 |
| 5 | 252 | 141 | 0.6880..1.8961 | 15 | -0.2662 |

The leg the idea actually asked about — *book OOS Sharpe > SPY OOS Sharpe on the same surviving
days* — **survives every single-year deletion and every one of the 45 pairs**, and first fails on
2 of 120 triples. The worst single year to lose is **2024** (OOS Sharpe 1.1759 -> 1.0594) against
a matched SPY of 0.7988 — still +0.2251 of slack. Deleting the *best* years does not kill it:
drop 2022 and it rises to 1.3762 (SPY rises to 1.1295 with it, because the same days leave both).

### The drawdown side is carried by exactly one year, and it is 2020
**All 234 failing subsets on U56 contain 2020. All 382 subsets that do not contain 2020 pass 4b
— including every way of deleting 5 of the other 9 years.** Deleting 2020 is the *only* single
deletion that kills the pass, and the mechanism is not the book:

> drop 2020 -> book full MaxDD_seg **-19.13% -> -19.10%** (unchanged), SPY full MaxDD_seg
> **-33.72% -> -24.50%**, so 4b's cap tightens **-20.23% -> -14.70%** and the DD margin goes
> **+0.0110 -> -0.0441**.

The book's drawdown did not get worse. The bar moved, because **4b's DD leg is 60% of SPY's own
worst crash**, and SPY's worst crash in this window *is* March 2020. The committed +0.0110 of DD
slack is therefore a statement about the benchmark's path, not the book's risk: it says the
window contained a -33.72% crash, and the book's capital case inherits a bet that the next
decade contains one too. On a -24.50% benchmark decade this book does not clear 4b.

### The other two panels never had the pass to lose
**B136** fails 4b at k=0 already (DD margin **-0.0051** — the broad-panel book draws -20.74%
against the same -20.23% cap) and 0 of 10 single-year deletions recover it. **SMALL663** fails
all five legs at k=0 (7.87% / 0.5073 / -35.81%). The question is a U56 question.

## Rule 8 (walk-forward)
**R8a** — every grid point is an out-of-sample report; the book's dials were frozen pre-2017 and
2017-2026 is read once. Headline OOS at k=0: **book 17.16% / 1.1759 / -19.13%** vs **LIVE v2
9.42% / 1.2717 / -12.05%** vs **SPY 15.15% / 0.8686 / -33.72%**. The book beats SPY on Sharpe and
CAGR OOS and loses to the live book on Sharpe, unchanged from the record.
**R8b (the matched control)** — the identical jackknife on the IS window. Worst single-year
Sharpe drop, IS vs OOS: U56 **0.1588 vs 0.1165** (ratio 0.734), B136 0.2261 vs 0.1200 (0.531),
SMALL663 0.2162 vs 0.0968 (0.448). **The OOS window is LESS year-fragile in Sharpe than the IS
window on all three panels**, so "the OOS decade is an unusually lucky sample" is refuted on the
return side. The IS arena's own 4b first dies at k=3 (2009+2012+2015, via H1), never via DD.
**R8c** — the fragility diagnostic does not transfer: the IS-window worst year is 2013 on all
three panels, which cannot name an OOS year. Only the direct OOS reading counts, and it is the
reading above.

## Pre-declared outcomes, scored honestly
(A) "the pass is broad" **FAILS** two of its three clauses (some single deletion kills 4b; the
k=1 OOS Sharpe spread is 0.3168, over the 0.15 bar). (B) "the pass is year-carried, k_first = 1"
**LANDS ON THE LETTER** — but through the DD leg and through 2020, not through the melt-up years
the idea suspected; on (B)'s implied reading (a *return* year carrying the pass) it is refuted.
(C) does not apply. Reported as it fell, not moved.

## What this does NOT license
No new book. No rules change. The incumbent's OOS return case stands and is *more* robust than
this run went looking for. What moves is the **confidence interval on its 4b DD leg**, which is
+0.0110 wide on a bar whose denominator is one crash.

## WHAT THE RECORD SHOULD TAKE, IN ONE SENTENCE
**4b's drawdown leg is a RELATIVE cap denominated in the benchmark's worst crash, so it is
EASIEST to pass in exactly the windows that contain one** — every 4b DD pass in the record
should quote SPY's MaxDD over its own window beside it, and a candidate whose DD slack is
smaller than the cap's own sensitivity to deleting one benchmark crash year should be recorded
as CRASH-CONTINGENT. PROPOSED for the Sunday review (rule 6) as a PROTOCOL reporting line only,
never as a chooser; RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are untouched here.

## Survivorship (rule 9)
U56 and B136 are CURRENT-constituent lists; SMALL663 is a current sub-$2B screen (52 of 715 names
dropped for max_1d_move >= 1.0). Every absolute level is optimistic and every 4b pass is an upper
bound. This run's headline is a **difference between scorings of the same book on the same panel**
(with and without a year), which is first-order immune to a common level bias; 1255 prices the
panel bias itself. The 2020 finding is a property of the BAR, not of the panel, and survives any
level bias that moves book and benchmark together.

## Files
`2026-09-17_..._B.py` (script) / `.console.txt` / `.grid.csv` (2,571 points) /
`.walkforward.csv` / `.kill.csv` / `.gates.csv`

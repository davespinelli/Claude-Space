# Idea 553 — how many of the record's POOLED-ACROSS-CADENCE bars clear a band their own cells fail?

Lane B, 2026-09-09. Script: `2026-09-09_how-many-of-the-records-POOLED-ACROSS-CADENCE-bars-clear-a-band-their-own-CELLS-fail_B.py`
Artefacts: `.census.csv` (81 bars), `.grids.csv.gz` (55,048 triples), `.ladder.csv`,
`.ladder_record.csv.gz` (130,713 rows), `.walkforward.csv` (869 IS/OOS triples), `.books.csv`
(270 books), `.wfbook.csv`, `.console.txt`. Re-run twice: console output byte-identical.

## Verdict — **ANSWERED, and it re-reads the queue's own premise. No KEEP candidate, no memo, no RULES change.**

**"How many pooled PASSes are level FAILs" has no answer until you say how deep you cut. It is not a
property of the bar; it is a property of the cut.** On the anchor's own 135 cells, one band, one
statistic, cut deeper each rung:

| cut | levels | FAIL | fail rate | min | max |
|---|---|---|---|---|---|
| POOLED (no cut) | 1 | 0 | 0.0% | -0.2852 | -0.2852 |
| panel | 3 | 0 | 0.0% | -0.3463 | -0.2407 |
| cadence | 5 | **1** | 20.0% | -0.4628 | -0.0398 |
| panel x cadence | 15 | **4** | 26.7% | -0.6871 | +0.0727 |
| panel x cadence x theta (cells) | 135 | **78** | 57.8% | -1.2816 | +0.7655 |

## G3 FAILS, and that is the first finding

Pre-registered: pooled -0.2852 inside `[-0.70,-0.20]` **and D and A outside**. Pooled reproduces to
the digit and is inside; **D does not fail** — pooled over the three panels the daily level is
-0.2438, comfortably inside. Only ANNUAL (-0.0398) fails. The queue's "its own D and A cells fail"
is idea 551's **SMALL439 row** (D -0.0904, A -0.1078), i.e. a panel x cadence statement quoted as a
cadence statement — the same substitution the idea was written to catch, one rung up.

| pp/yr | D | W | M | Q | A |
|---|---|---|---|---|---|
| B136 | -0.3776 | -0.4688 | -0.3723 | -0.4284 | **-0.0843** |
| SMALL439 | **-0.0904** | -0.2164 | -0.2416 | -0.6871 | **-0.1078** |
| U56 | -0.2636 | -0.4439 | -0.2957 | -0.2728 | **+0.0727** |

## (a) The census — the literal bars

The extractor re-finds **all 80** of idea 554's committed census rows with matching arity (G2 PASS);
the one extra row is `BAR_MA_RESID` in the lane-B script committed after 554 ran. Of 81 eligible
bars, **8 are POOLED over a dial** (1 GRID + 7 REPRO constant gates) — the record's bars are
overwhelmingly hand-copied single numbers, not pooled means, so the literal-bar population is too
thin to carry the answer. **STRICT re-priceability 0/8, RELAXED 5/8**; the only GRID pooled bar
(`ratio` in the turnover-matched-null script) cannot be re-priced from its own artefacts at all.
H_CENSUS "holds" only on the relaxed link and only on REPRO gates.

## (c) The base rate — the record's grids

55,048 (file, statistic, dial) triples from 1,862 committed grids. Bar = pooled mean ± k pooled SD,
so the pooled PASS is true **by construction**; the number measured is P(some level fails | pooled
passes). The anchor band's nearer edge sits at **k = 0.28** of its own cells' SD.

| k | 0.25 | 0.5 | 0.75 | 1.0 | 1.5 | 2.0 | 3.0 |
|---|---|---|---|---|---|---|---|
| ≥1 level outside | **57.9%** | 38.3% | 26.9% | 18.5% | 3.9% | 1.0% | 0.2% |
| mean cell coverage | 16.8% | 34.8% | 53.1% | 69.1% | 89.0% | 96.4% | 99.4% |

**H_COMMON HOLDS** at the anchor's own width (57.9% > 50%); H_OUTLIER fails. On the anchor's own dial
(cadence/freq, 2,112 triples) the rate is 54.7%.

Worst dials at k=0.25 / k=0.5: variant 96.7% / 93.4%, pick 90.9% / 81.5%, theta 88.2% / 61.1%,
**panel 76.8% / 61.6%** (n = 13,478, by far the largest), dial 76.0% / 54.1%, q 74.8% / 61.6%.
Safest: uni 28.6% / 8.1%, cost_bps 33.1% / 10.2%, conv 34.6% / 17.4%, cost 36.6% / 9.5%,
phase 38.7% / 8.1%.
**Pooling over PANEL is the record's most dangerous pooling** — mean spread of level means 1.23
pooled SDs, max 10.3 — which is the same fact this week's replication failures keep printing.

The record-wide ladder reproduces the anchor's ladder exactly in shape (130,713 rows):

| depth | k=0.25 | k=0.5 | k=1.0 | k=2.0 |
|---|---|---|---|---|
| one dial | 58.0% | 38.4% | 18.5% | 1.0% |
| a dial PAIR | 86.4% | 71.5% | 44.8% | 5.3% |
| raw cells | 100.0% | 100.0% | 100.0% | 72.9% |

## Rule 8

**WF-CENSUS** (k chosen on IS levels, read once on untouched OOS levels, 869 triples with the
record's own IS/OOS split): the IS-fitted bar holds at **every** OOS level in **423 of 869 =
48.7%** — worse than a coin flip. By dial: family 66.7%, theta 57.6%, cad 52.3%, panel 51.3%,
conv 34.8%, arm/strata 32.1%, band 8.0%, **gate 0.0%**. A width fitted at the level of a dial in the
first half does not transfer to the second.

**WF-BOOK** (270 real books: 3 panels x 9 thetas x 5 cadences x 2 constructions, MA-THRESH, gross
0.75, 10 bps, next-day execution; IS ≤ 2016 chooses, 2017-2026 read once). Two selection rules:
POOLED (best mean IS Sharpe over the cadence dial) vs CELL (best among (theta, construction) pairs
beating SPY at **every** cadence in-sample).

| panel | POOLED pick | CELL pick | OOS CAGR | OOS Sharpe | OOS MaxDD | RULES v2 OOS | SPY OOS |
|---|---|---|---|---|---|---|---|
| U56 | θ-0.12 RESPREAD | same | 12.71% | 1.1209 | -21.33% | 9.36% / 1.2904 / -11.69% | 15.38% / 0.8786 / -33.72% |
| B136 | θ-0.25 DEGROSS | same | 13.14% | 1.1052 | -24.14% | 7.92% / 1.1206 / -12.09% | 15.45% / 0.8820 / -33.72% |
| SMALL439 | θ-0.40 RESPREAD | **no pick** | 8.56% | **0.5755** | -35.25% | 3.83% / 0.5665 / -14.66% | 15.45% / 0.8820 / -33.72% |

**H_BOOK FAILS, in the direction that matters.** Where the CELL rule makes a pick it is the *same*
book as POOLED (18 candidates -> 10 survive the per-level requirement, and the winner is unchanged);
where it makes none it refuses **SMALL439**, the one panel whose pooled pick goes on to earn OOS
Sharpe **0.5755 against SPY's 0.8820**. Per-level qualification cost nothing on the two panels it
cleared and screened out the only loser. That is the capital-relevant content of this idea.

## KEEP paths (all 270 books, no selection)

**4a 4/270, 4b 10/270, BOTH 0/270.** The four 4a passers are all SMALL439 DEGROSS at M cadence
(θ +0.30/+0.20/+0.12/+0.06; CAGR 1.9-3.8%, Sharpe 0.67-0.76, MaxDD -3.9 to -11.9%) — they clear a
low-return baseline by being lower-return still, and every one fails 4b on CAGR. The ten 4b passers
are 8 U56 + 2 B136, all fail 4a. 4b failing legs: **DD 182**, CAGR 147, OOS 124, H2 121, H1 120 —
the drawdown cap is the binding leg again (ideas 500/527/550). No KEEP candidate; a census cannot
produce one and none is claimed.

## Gates

- **G1 PASS** `fast_backtest` == `engine.backtest`, 3 panels x 4 cadences, worst abs diff 1.94e-15.
- **G2 PASS** all 80 of idea 554's census rows re-found with matching arity; 1 extra row, from the
  only `*.py` committed after 554's run.
- **G3 FAIL** (see above) — the pre-registered clause "D and A outside" is false at the cadence cut.
- **G4 FAIL** pooled mean vs mean of level means on 40,245 balanced triples: max abs diff 1.53e-05
  against a 1e-10 **absolute** tolerance. Max **relative** diff 1.05e-05; the worst triple is
  `relative-priceability-floor_C.walkforward.csv / IS_rate / cost` whose pooled mean is -8.65e+10.
  The gate was written absolute and is reported as it fell, not repaired.
- **G5 PASS** 1,862 grids, 55,048 triples (bars 300 / 1,000).
- **G6 FAIL** live RULES v2 on U56 reads 8.50% / 1.2109 / -11.69% vs the published 8.66% / 1.2056 /
  -12.05%. This reproduces the failure ideas 550 and 551 already recorded — `data/prices.csv` runs to
  2026-09-08 while the weekly caches stop 2026-09-04 (idea 514's vintage split). Pre-existing
  condition, not this script.

## Caveats

**SURVIVORSHIP:** B136 and SMALL439 are current constituents; every CAGR/Sharpe/MaxDD level and both
KEEP columns in the book leg are optimistic, and the census legs read numbers other scripts computed
on the same panels.
**SCOPE LIMIT:** the extractor reads `*.py` through five syntactic patterns, so the 81-bar population
is a LOWER BOUND — a bar living only as prose in a `.result.md` is outside the denominator. The grid
scan skips artefacts above 30 MB (17 files) and reads at most 200k rows per file. The base rate's
"pooled PASS" is true by construction and must never be quoted as a finding.

## What the record should do with this

The bar is not the unit. **A published band is only interpretable with the cut depth it was measured
at.** At this record's own band width, a band measured on a pooled mean is outside at least one
single-dial level 58% of the time, outside at least one dial-pair cell 86% of the time, and outside
at least one raw cell essentially always — and an IS-fitted width holds at every OOS level less than
half the time. Quoting a pooled band forward as a cell expectation is not a rare accident here; it is
the majority case.

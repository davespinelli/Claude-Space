# Idea 439 — census-every-CROSSING-in-the-record-for-dial-heterogeneity (lane C, 2026-09-08)

**ANSWERED, and the queue's generalisation does NOT hold: 9 of 10 of the record's pooled-curve
readings survive their own cell-type fixed effects, and 10 of 10 survive mix standardisation.
The disappearance idea 226 reported is a property of the TRANSFORM, not of the record — plain
within-cell demeaning removes the pooled LEVEL as well as the composition, and a crossing is a
statement about the level. Under that transform survival falls to 6 of 10 and, worse, it
FABRICATES interior crossings in 4 of 10 items whose pooled curve has none. The larger census
finding is that the record has far fewer crossings than the queue assumes: only 2 of the 10
committed pooled local curves carry an interior crossing at all.** No RULES change, no KEEP
claimed; `RULES.md`, `scan.py`, `bot.py` and `baseline.py` untouched.

Script: `research/backtests/2026-09-08_census-every-CROSSING-in-the-record-for-dial-heterogeneity_C.py`
Artefacts: `.console.txt`, `.census.csv` (200 re-reads), `.curves.csv` (every grid point of
every curve), `.perxis.csv`, `.sensitivity.csv`, `.loco.csv`, `.bookgrid.csv` (126 books),
`.walkforward.csv`, `.keeppaths.csv`.

## Reproduction gate — before any new number was read

| check | published | this run | |
|---|---|---|---|
| idea 219's cells | 560 | 560 | MATCH |
| its crossing at its own half-window (0.075, grid 0.20–1.00 step 0.025) | 0.425 | 0.425 | MATCH |
| its last non-positive centre | 0.400 | 0.400 | MATCH |
| `fast_backtest` vs `engine.backtest`, RULES v2 / U56 @10 bps | — | max abs diff **0.000e+00** | MATCH |

## The census frame (mechanical, declared before any number was read)

The record's own name for a pooled local curve is a committed `*.curve*.csv`: there are **11**.
An item is admitted iff its cell-level rows are committed, they carry the numeric x-axis the run
pooled over, they carry ≥1 categorical cell-type column with ≥2 levels, and the run's result.md
reads a location off that curve. **10 items admitted, 4 files reported as not-re-readable**
(2 are idea 226's re-reads of item 219's own 560 cells; 2 are per-cell summaries whose cell-level
rows are admitted under their own id). Nothing was dropped silently.

**Two tuned parameters, all 200 grid points published.** P1 the half-window as a multiple of the
item's own median grid step, `hmult ∈ {1,2,3,4,5}` (**3 is the headline because on item 219 it is
the record's published 0.075 to the digit**). P2 the FE mode ∈ {NONE, WITHIN, RECENTRED,
STANDARDISED}. Grid, min-cells-in-window (5) and the crossing reader are idea 219/226's committed
conventions, imported rather than re-chosen.

## (1) The record has 2 crossings, not 10

`crossing_of` returns the grid's first centre when the curve is **positive throughout** (nothing
to cross) and `nan` when it never becomes uniformly positive (also nothing to cross). Counting
only INTERIOR crossings:

| item | source run | published reading | pooled re-read |
|---|---|---|---|
| 219 | modal share → writable mode | crossing 0.425 | **interior crossing, 4 of 5 windows** |
| 168c | vol-scaler exponent k (cloud) | live k = −0.5 on the wrong side of zero | **interior crossing, 5 of 5 windows** |
| 167 | value/cost parallelism | "crossing does not exist, 12/12" | positive throughout — consistent |
| 159B | share at which ranking stops paying (B) | "no crossing inside [0.05, 0.70]" | positive throughout — consistent |
| 103 | correlation as a sleeve variable | curve real, correlation killed | positive throughout — consistent |
| bandgate | band width → gap vs bare 200d | gap rises in band | positive throughout — consistent |
| 168B | vol-scaler exponent k (B) | argmax at the grid edge, 10/12 | argmax at the top edge — consistent |
| 277 | ETF share → reversal share | non-monotone, no turn to locate | argmax reproduced — consistent |
| 159c | share at which ranking stops paying (cloud) | q\* ≈ 0.85 | **not a pooled-curve location** — q\* is a FITTED log-linear crossing on the rank share; the committed empirical curve carries none, which is that run's own finding |
| 61 | gate instrument speed | a FLOOR near 0.5 flips/tkr/yr | **not a pooled-curve location** — the pooled matched-gross curve is non-positive at every centre including the fastest, so there is no crossing on it to read; the floor is a per-pool sign statement |

**8 of 10 published "thresholds" are edge readings, argmaxes, or statements the pooled curve
cannot carry.** Idea 439 was written as though the record were full of pooled-curve crossings;
it has two.

## (2) How many survive — the answer depends entirely on whether the transform keeps the level

At the headline half-window (hmult 3), over 10 items:

| FE mode | survives (tol 1 step) | survives exactly | interior crossings LOST | interior crossings FABRICATED |
|---|---|---|---|---|
| **RECENTRED** (composition removed, level kept) | **9 of 10** | 9 of 10 | 0 | 0 |
| **STANDARDISED** (window mix → global mix, level kept) | **10 of 10** | 9 of 10 | 0 | 0 |
| **WITHIN** (plain demeaning, idea 226's construction) | **6 of 10** | 6 of 10 | 1 | **4** |

Stable across the whole window grid: RECENTRED 9/10/9/9/9 and STANDARDISED 10/10/10/10/10 at
hmult 1–5, WITHIN 8/6/6/6/6 with 2/3/4/4/4 fabricated crossings.

**The one item that moves is the seed.** Item 219 at hmult 3: pooled 0.425 → RECENTRED 0.350
(3 steps, BREAKS) → **STANDARDISED 0.400 — one step, and exactly the number idea 226 published
for its own standardised version.** At hmult 2 (half-window 0.05) RECENTRED returns 0.425 exactly.
Its single-axis diagnostic says which axis does it: `dial(7) → 0.350`, `corpus(2) → 0.425`,
`cost_bps(5) → 0.425` — the dial axis alone, as idea 226 said.

**What WITHIN does is not a correction, it is a different question.** Demeaning forces the pooled
mean to zero, so a curve that is positive everywhere is guaranteed to straddle zero somewhere:
item 167 (ratio ≥ 2.37 at all 120 published points, i.e. an instrument that never costs more than
it moves) acquires a crossing at 0.400–0.530 under WITHIN, and `bandgate` (0.120), `277` (0.125)
and `168B` (0.000) acquire one each — four fabrications at hmult 3, against the one real crossing
(item 219's) it deletes. Four fabricated crossings in a census of ten is a higher error rate than
the artefact the census was written to find.

## (3) Window width moves these readings as much as heterogeneity does

| item | crossing span across the 5 window widths | mean move under level-preserving FE |
|---|---|---|
| 168c | **4.00 grid steps** (k = 0.10 → 1.00) | 0.00 |
| 219 | 3.00 steps | 2.12 (max 7.00) |
| every other defined item | 0.00 | 0.00 |

Pooled over the 8 items where both are defined: mean window span **0.88 steps** vs mean
level-preserving FE move **0.27 steps**. Item 168c's crossing in the vol-scaler exponent is a
pure smoothing artefact — it is fixed-effect-proof and window-width-fragile, the exact opposite
of the failure mode idea 439 was written about.

## (4) Rule 8 (i) — leave-one-cell-type-out: FE does not transfer better

45 folds (each level of each item's largest cell-type axis held out), both readings defined in 28.
Mean |error| against the held-out level's own crossing: **POOLED 1.571 grid steps, FE 1.714 —
FE better in 0 of 28.** 12 of 45 held-out levels have no crossing of their own at all. Removing
fixed effects makes a pooled crossing no more portable to a cell type it was not fitted on; it is
a description of the pooled cells, not a transferable constant.

## (5) Rule 8 (ii) — the same question priced, on live prices

126 fresh books: 3 panels (U56 56, B136 136, SMALL439 484 names) × gross {0.50, 0.75, 1.00} ×
cadence {W, M} × band width {0, 0.02, 0.03, 0.05, 0.08, 0.12, 0.20}, 10 bps, t+1. x = band width,
y = IS (≤ 2016-12-31) Sharpe minus the same cell's bare-200d IS Sharpe. The threshold is read off
the IS curve only; 2017-2026 is read once.

The pooled read and both level-preserving FE reads adopt **band 0.02** at every one of the 5
window widths; **WITHIN-FE adopts 0.12** at hmult 1–3 (no crossing survives its demeaning, so the
argmax is the fallback). Untouched OOS, pooled over the 18 cells:

| arm | band | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|
| POOLED-read | 0.02 | 7.49% | **1.0267** | −13.24% |
| FE-RECENTRED-read | 0.02 | 7.49% | **1.0267** | −13.24% |
| FE-STANDARDISED-read | 0.02 | 7.49% | **1.0267** | −13.24% |
| FE-WITHIN-read | 0.12 | 7.63% | **0.9726** | **−16.03%** |
| bare 200d (band 0) | 0.00 | 7.30% | 1.0193 | −12.74% |
| live RULES v2 band | 0.03 | 7.49% | 1.0135 | −13.68% |
| ORACLE (best OOS band per cell) | — | 7.61% | 1.0457 | −13.09% |

**Adopting the demeaned reading costs 0.054 of OOS Sharpe and 2.8 pp of OOS drawdown against
adopting the pooled one.** The correction the queue proposes, done the level-destroying way, is
not neutral out of sample — it is negative.

Benchmarks, same OOS window: SPY 15.45% / 0.8822 / −33.72%. RULES v2 (live) @10 bps: U56 9.53% /
1.2853 / −12.05%, B136 7.98% / 1.1187 / −12.24%, SMALL439 4.55% / 0.6630 / −12.09%. RULES v1
@10 bps: U56 7.73% / 0.7472 / −13.83%, B136 5.94% / 0.5764 / −21.19%, SMALL439 17.15% / 0.5542 /
−44.83%.

## (6) Both KEEP paths on all 126 books

| panel | books | 4a pass | 4b pass |
|---|---|---|---|
| U56 | 42 | 0 | 12 |
| B136 | 42 | 1 | 7 |
| SMALL439 | 42 | 3 | 0 |
| **total** | **126** | **4** | **19** |

**All 19 4b passes are gross 1.00** — the cash carve-out removed from the live book's own family,
not a new book. Per idea 144 a re-dialled book is the same book, so **no KEEP is claimed**; the
grid also runs three dials (gross, cadence, band), above a KEEP's two-parameter budget, because
it is the census's instrument and not a book search. The 4a passes are all de-grossed
(gross 0.50) books, the record's standing pattern.

## Verdict

**ANSWERED / KILL of the generalisation.** The record's pooled-curve readings are robust to their
own cell-type fixed effects (9 of 10, and 10 of 10 under mix standardisation); the "it disappears"
result is produced by demeaning, which deletes the level a crossing is a statement about and
manufactures crossings where the curve never changes sign. Two second-order results are worth
more than the census itself: **only 2 of the record's 10 pooled local curves carry an interior
crossing at all**, and where a crossing does exist the **window width moves it as much as the
heterogeneity does** (168c: 4 grid steps from smoothing, 0 from fixed effects). Priced on live
prices, the demeaned reading is the one that loses money out of sample.

**If PROTOCOL ever adopts a heterogeneity check for published crossings, the wording should be:**
*"a crossing read off a pooled local curve must be re-read with the cell mix standardised to the
global mix (or with cell fixed effects removed and the pooled level added back), and the reading
must be published at ≥2 half-windows; a within-cell demeaned curve may not be used to locate a
crossing, because demeaning forces the curve through zero."* This run does not amend PROTOCOL —
that is a Sunday-review change and is offered as wording only.

# Idea 311 — does-4b-discriminate-ANYTHING-on-gross-scalar-books (cloud, 2026-09-09)

**VERDICT: KILL of idea 51's "non-empty in 20, passing in 20/20, the EWall control included"
reading — it does not replicate on a pre-registered 6-form menu with a fine g grid. The real
answer is two-sided: 4b DOES discriminate a little (the ungated control's band is EMPTY in
5 of 6 panel×cadence cells), but every 4b pass is a knife-edge DIAL PLACEMENT — the median
admissible g-band is ONE grid step of seventeen, and it walks forward in only 9 of 20 cells.**

**And the census settles the second half of the question: 98.1% of the record's committed 4b
passes were never swept in gross at all inside their own file; of the ones that were, 97.6%
flip verdict somewhere on their own gross ladder. PROTOCOL 4b should quote the admissible
g-BAND and its width, not a ladder point.**

Script `research/backtests/2026-09-09_does-4b-discriminate-ANYTHING-on-gross-scalar-books_cloud.py`
(310 s, 612 ladder books + a 2,476-file census).

## Gates

* **G1 PASS** — idea 312's committed 36 REAL rows reproduce at **2.2e-16 / 2.2e-16 / 4.4e-16**
  (B136 / SMALL439 / U56) over 13 columns.
* **G2 PASS** — `fast_backtest` vs `engine.backtest` max |dreturn| **1.39e-17**.
* **G3 PASS** — the invariance claim re-checked against `engine.backtest` directly, not the
  fast runner: B136 MA-RS/W Sharpe **1.05552 / 1.05636 / 1.05701** at g = 0.20 / 0.60 / 1.00
  (span **0.00149**) while CAGR runs 3.09% → 15.53% and MaxDD −5.65% → −26.20%.

## Design

Six pre-registered unlevered book-forms whose only free dial is the gross scalar g — `EWall`
(the no-edge control), `MA-RS`, `MA-DG`, `TOP20`, `TOP10`, `MA20` — on U56 / B136 / SMALL439,
cadence {W, M}, **g = 0.20 … 1.00 step 0.05 (17 points)**. 10 bps, t+1 fills, no shorting, no
leverage. Two tuned parameters: **form** and **g**. Every one of the 612 grid points is in
`.grid.csv`. **SURVIVORSHIP:** B136 and the small panel are today's constituents; small-panel
names with `max_1d_move >= 1.0` dropped first.

## H_INVAR — FAIL at the strict bar, but the qualitative claim is overwhelming

Max Sharpe span across the 17 grosses is **0.02648** (SMALL439 TOP10 M) against a pre-registered
0.0100 bar, so **H_INVAR FAILS**: idea 51's "span ≤ 0.0050" does not hold on a fine grid.
**29 of 36 cells are inside 0.0100** and the failures are all concentrated books (TOP10, MA20,
TOP20) at monthly cadence, where rebalancing drift makes the engine's re-normalisation
non-linear. The magnitude comparison is what matters:

| | span across g | median R² in g | median slope per unit g |
|---|---|---|---|
| Sharpe | ≤ **0.0265** | 0.9983 | **+0.0065** |
| CAGR | up to **21.44 pp** | 1.0000 | +0.1785 |
| MaxDD | up to **38.62 pp** | 0.9993 | −0.3021 |

Median |MaxDD span| / |Sharpe span| = **55×**. **H_LINEAR PASS: 100% of cells on both CAGR and
MaxDD** (bar was 90%). Sharpe is not *invariant* in g — it drifts gently upward as the zero-
return cash drag shrinks — but its slope is 27–46× smaller than the two scaling legs'.

## The admissible 4b g-band

**20 of 36 cells have a non-empty band, and all 20 are contiguous (H_BAND PASS).** Widths:

| statistic | value |
|---|---|
| median band width | **0.05** (= ONE grid step) |
| mean / max width | 0.075 / **0.20** |
| median / max admissible grid points | **2 / 5** out of 17 |

Empty bands split **13 SHARPE-leg kills vs 3 DD/CAGR-cannot-coexist (H_SHARPE PASS)**. The
three Sharpe legs are g-invariant, so they are all-or-nothing: they pass at every g in 23/36
cells and at no g in 13/36 — **the entire SMALL439 panel is killed by a Sharpe leg at every
gross, on every form.** Once the Sharpe legs pass, the band is decided *entirely* by the DD cap
and the CAGR floor, and the "4b band" column equals the "DD+CAGR only" column in every
non-empty cell.

## H_NODISC — FAIL, i.e. 4b does discriminate, weakly

| panel | cad | EWall band | median treatment band | best treatment | treatments non-empty |
|---|---|---|---|---|---|
| U56 | M | [0.65, 0.65] (w 0.00) | 0.15 | 0.20 (MA20/TOP20) | 5/5 |
| U56 | W | [0.65, 0.65] (w 0.00) | 0.10 | 0.10 | 5/5 |
| B136 | M | **EMPTY** | 0.05 | 0.05 | 5/5 |
| B136 | W | **EMPTY** | 0.05 | 0.05 | 3/5 |
| SMALL439 | M | **EMPTY** | 0.00 | 0.00 | 0/5 |
| SMALL439 | W | **EMPTY** | 0.00 | 0.00 | 0/5 |

The control's band is non-empty and at least as wide as the median treatment in **0 of 6**
cells. **Idea 51's "20/20 including the no-filter control" does not replicate here.** The
mechanism is worth stating plainly: with the Sharpe legs g-invariant, the DD+CAGR pair reduces
to a *ratio* test — a book is admissible at some g iff its CAGR-per-unit-drawdown clears
(0.70·CAGR_SPY)/(0.60·|MaxDD_SPY|). That is a Calmar-like edge statistic, not nothing. But the
discrimination it buys is small (0.05 vs 0.00 of band width on B136) and it costs a knife edge.

## Rule 8 walk-forward (band solved on ≤2016-12-31, 2017-2026 read once)

**WF-A** — of the 20 cells with a non-empty IS band, the IS band's midpoint g\* is inside the
OOS band in **9/20**. Six IS-admissible cells have an EMPTY OOS band; three cells that are
empty IS become non-empty OOS. **The admissible band does not walk forward.**

**WF-B** — form picked by IS Sharpe (g-invariant, so the form is the only real choice), g set
to the IS band midpoint, B136 / W, OOS read once. IS pick **TOP10 at g=0.50** (IS Sharpe
+1.1968); the OOS winner was MA-DG (+1.1264).

| book | CAGR | Sharpe | MaxDD | H1 | H2 | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|---|---|
| WF-B TOP10 g=0.50 | 11.61% | 0.969 | −17.95% | 1.266 | 0.765 | **10.79%** | **0.835** | **−17.95%** |
| RULES v2 (B136) | 8.03% | 1.106 | −12.24% | 1.229 | 0.984 | 7.98% | 1.119 | −12.24% |
| SPY | 15.23% | 0.889 | −33.72% | 0.957 | 0.834 | 15.45% | 0.882 | −33.72% |

**4a False**; 4b fails **H2, OOS** on the full sample and **H1, OOS, CAGR** in the OOS window
read alone.

## The census — 2,476 committed CSVs

186 files carry both a `gross` column and a 4b verdict; 170 contribute at least one committed
4b pass. Identity for grouping = every column that is not `gross`, not a 4a/4b verdict, and not
a known OUTCOME name — **float dials (level, band, lam, q, …) count as identity, which splits
groups and biases the census AGAINST the DIAL classification on purpose.**

| class | book-groups | committed 4b passes |
|---|---|---|
| **UNSWEPT** (one gross only) | **21,273** | **23,015 (98.1%)** |
| **DIAL** (flips verdict on its own gross ladder) | **430 (98.9% of swept)** | **440 (97.6% of swept)** |
| ROBUST (passes at every gross the file ran) | 5 (1.1%) | 11 (2.4%) |

**H_CENSUS PASS.** Almost the whole record's 4b evidence is unswept in gross; where a file did
sweep, the verdict flips 97.6% of the time. Biggest DIAL contributors are this week's
kernel-draw runs (idea 569 63, idea 312 56, idea 568 35) — the same files whose 4b counts the
record has been quoting.

## KEEP paths over the 612 ladder books

**4a 34/612 (5.6%) · 4b 50/612 (8.2%) · BOTH 0/612.** Binding legs: CAGR 336 · DD 271 · H2 221
· OOS 221 · H1 204. 4b passers by panel U56 35 / B136 15 / **SMALL439 0**; by form TOP20 12,
MA20 12, MA-RS 10, TOP10 8, MA-DG 6, **EWall 2** (both U56, a single grid point each). Best is
`U56 TOP20 M` whose Sharpe is **1.231–1.232 at every g in [0.50, 0.70]** while CAGR moves
11.06% → 15.61% and MaxDD −14.75% → −20.15% — the cleanest single illustration in the run that
the 4b verdict on such a book is a placement, not a finding. **No BOTH-path book, no capital
candidate, no memo.**

## PROTOCOL proposal (for Sunday review — PROTOCOL.md NOT edited by this run)

> **4b (amended reporting):** on any book whose exposure is a scalar multiple of a fixed
> weight path, a 4b verdict must be quoted as the **admissible gross band [g_lo, g_hi] and its
> width in grid steps**, not as a pass at one g. A band of width 0 (a single grid point) is
> reported as PARK, never KEEP. Where the three Sharpe legs pass at every g, state that the
> verdict rests on the DD cap and CAGR floor alone.

## Artefacts

`.grid.csv` (612 rows, every grid point) · `.bands.csv` · `.discrimination.csv` ·
`.census.csv` · `.walkforward.csv` · `.keeppaths.csv` · `.console.txt`.

## Follow-ups proposed

1. 23,015 of the record's 4b passes are gross-UNSWEPT — re-run the ten highest-cited of them
   on a 17-point g grid and report how many keep their verdict.
2. Every SMALL439 cell is killed by a Sharpe leg at every gross, on all six forms — test
   whether the small panel can clear a Sharpe leg under ANY unlevered book-form.
3. Sharpe's slope in g is +0.0065/unit, small but systematic and positive — price the
   zero-return cash convention (idea 406's question) against this ladder directly.

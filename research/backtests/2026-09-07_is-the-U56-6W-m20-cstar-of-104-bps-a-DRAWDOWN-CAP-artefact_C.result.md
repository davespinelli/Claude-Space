# idea 348 — is the U56 6W m=20 c* of 104 bps a DRAWDOWN-CAP artefact?

**Lane C, 2026-09-07. Verdict: KILL of the queue's premise — on family A the DD cap never binds
at a breakeven, and the c* column is NOT mislabelled within a panel. One AMENDMENT proposed.**

Script `2026-09-07_is-the-U56-6W-m20-cstar-of-104-bps-a-DRAWDOWN-CAP-artefact_C.py`; console in
`.console.txt`; per-cell numbers in `.familyA.csv` (36 cells x 58 cols), `.familyB.csv` (64),
`.decomp.csv`, `.walkforward.csv`, `.keeppaths.csv`. No new book: idea 331's own committed module
is imported, so its two tuned parameters (cadence x m) are re-priced, not re-searched.

## What c* is, before it is measured

`r(c) = r0 - turnover * c/1e4`, so every 4b bar margin `m_k(c)` falls near-linearly in cost
(measured: the average slope to the crossing differs from the local slope at 0 bps by a median of
**0.7%**). Per bar the breakeven is therefore the exact root

    croot_k = slack_k / sens_k ,   slack_k = m_k(0),   sens_k = average consumption per bp

and the published number is `c* = min_k croot_k`. c* is a RATIO: **slack** is the book's edge over
the bar at zero cost (not a cost quantity at all); **sens** is the turnover term, the only genuine
cost tolerance in it. `log croot = log slack - log sens` holds to 8.9e-16 by construction, so the
spread of the column can be split exactly.

## H-A (the title): REFUTED

| bar | slack @0 | sens /bp | its own c* |
|---|---|---|---|
| **H1** | 0.2184 | 0.002080 | **104** |
| CAGR | 0.0391 | 0.000258 | 151 |
| DD | 0.0086 | 0.000049 | 174 |
| H2 | 0.3590 | 0.001819 | 197 |
| OOS | 0.3855 | 0.001758 | 219 |

U56 6W m=20 fails on **H1 at 104 bps**; the DD cap would not bind until **174 bps**, 70 bps later.
Removing the cap moves that c* by **+0**. Across all 8 family-A cells that have a breakeven, DD is
the binding bar in **0/8**, dropping the cap moves c* on **0/8**, dropping the CAGR floor on
**1/8**, dropping both on **1/8**. The binding-bar census is H1 5, CAGR 1, H2 1, H2+CAGR 1.

**What the cap actually does is CENSOR the column, not set it.** 13 of the 28 cells with no
published c* acquire one the moment the cap is dropped (U56 2W m=0 → 17 bps, 2W m=20 → 44,
6W m=0 → 42, Q m=0 → 89, Q m=20 → 88; B136 D m=0 → 0, D m=20 → 11, W m=20 → 6, M m=0 → 39,
M m=20 → 73, 6W m=0 → 46, 6W m=20 → 91, Q m=20 → 0). **The c* column's holes are the DD cap's;
its values are the Sharpe bars'.**

## H-B (mislabelled column): REFUTED within a panel, CONFIRMED across panels

Var(log c*) = Var(log slack) + Var(log sens) - 2Cov:

| target | scope | n | slack | sens | -2cov | spearman(c*, turnover) | log-log slope (R²) |
|---|---|---|---|---|---|---|---|
| c*_FULL (the published column) | pooled | 8 | +72% | **+196%** | -168% | **-0.976** | -1.21 (0.90) |
| c*_FULL | U56 | 7 | +98% | **+254%** | -252% | **-1.000** | -1.11 (0.94) |
| c*_noDD (13 censored cells restored) | pooled | 21 | +78% | +58% | -36% | -0.705 | -1.16 (0.35) |
| c*_noDD | U56 | 12 | +117% | +251% | -268% | -0.888 | -1.01 (0.88) |
| c*_noDD | B136 | 9 | **+82%** | +18% | -1% | -0.433 (slack **+0.983**) | -1.05 (0.18) |

Counterfactual IQR of c* on the published column: actual 6.52x, **slack varying alone 3.61x, sens
varying alone 7.74x**. Within a panel the column is a cost measurement — on U56 it ranks the 7
cells by inverse turnover with spearman **-1.000** and a log-log slope of -1.11, i.e. c* ≈ K/turnover.
Across panels it stops being one: on B136 the noDD column ranks almost perfectly by **slack**
(+0.983) and barely by turnover (-0.433), because the H2 edge differs far more between panels than
the cost structure does.

## Second family: idea 82's 64 committed cells (gate: `be` reproduced 64/64 exactly)

27 have a breakeven; **13 of those are right-censored at that run's 30 bps grid ceiling** (their
published 29.5 / 30.0 are floors, not breakevens). Of the 14 uncensored, the binding bar is CAGR 7,
DD 3, H2 3, H1 1 — so **DD does bind there**, and the family-A reading ("a Sharpe bar always
binds") does not generalise. Dropping bars moves be on 3/27 (noDD), 7/27 (noCAGR), 10/27 (Sharpe only).

## Rule 8 walk-forward (c* measured on 2009-2016 only, read once on 2017-2026)

| panel | bar subset used by the chooser | pick | IS c* | OOS CAGR / Sharpe / MaxDD @10bps | 4b | 4a |
|---|---|---|---|---|---|---|
| U56 | FULL, noCAGR | M m=20 | 53 | 14.15% / **1.124** / -18.73% | Y | n |
| U56 | noDD, SHARPEONLY | Q m=20 | 87 | 14.60% / 1.030 / -24.51% | n | n |
| B136 | FULL, noCAGR | 6W m=20 | 74 | 17.90% / 1.085 / -25.91% | n | n |
| B136 | noDD, SHARPEONLY | Q m=20 | 97 | 15.06% / 0.921 / -27.38% | n | n |
| SMALL439 | all four | Q m=20 | -1 | 1.87% / 0.193 / -44.34% | n | n |

Comparands OOS: SPY 15.45% / **0.882** / -33.72%; RULES v2 U56 9.53% / **1.285** / -12.05%,
B136 7.98% / 1.119, SMALL439 3.85% / 0.568. **8 of 12 picks beat SPY's OOS Sharpe, 0 of 12 beat
RULES v2's.** Dropping the DD cap from the *chooser* is strictly harmful even though it never binds
at c*: U56 1.124 → 1.030 and the pick stops passing 4b; B136 1.085 → 0.921. The cap earns its place
in selection, not in the breakeven.

Column stability IS → OOS (spearman over each panel's 12 cells; both-defined n in brackets):
U56 FULL +0.746 (+0.800, n=4), U56 noDD +0.142 (+0.900, n=5), B136 noDD +0.214 (+0.793, n=7),
B136 FULL -0.280 (n=0), SMALL439 undefined (no cell passes 4b in either window). The ranking is
stable where it exists, but it exists for very few cells per window.

## Both KEEP paths (all 36 cells, reproduced not proposed)

4b **8 / 6 / 4 of 36** at 0 / 10 / 25 bps (all U56); 4a **0/36 at every rung** (0 of 108 cell-rungs).
Best 10-bps cell is idea 331's own U56 M m=0: 15.30% / 1.213 / -19.51%, H1/H2 1.200/1.232, OOS 1.307.
**Nothing here is new** — this run re-prices the c* column, not the book, so it proposes no KEEP.

## Reproduction gates (5/5)

1. c*_FULL vs idea 331's committed `breakeven_bps`: **36/36 exact**.
2. Bar margins vs its committed `m4b_*` at 0/10/25 bps, 540 values: **max|d| 2.15e-16**.
3. Binding bar vs its committed `breakeven_first_fail`: **8/8 agree**.
4. Full 4a/4b metric block vs its committed grid (18 columns x 36 cells): **max|d| 2.22e-16**;
   KEEP counts reproduce its published 8/6/4 and 0/0/0.
5. Family B: `be_FULL` vs idea 82's committed `be`: **64/64 exact**.

## AMENDMENT proposed (not applied — PROTOCOL/RULES are not touched by this run)

A published `c*` is only interpretable with three things next to it, all already computable:

1. **its binding bar** (idea 331 publishes `breakeven_first_fail`; make it record-wide), because
   c* is that bar's slack divided by that bar's cost sensitivity, not a property of the book alone;
2. **its censoring flag** — a `-1` means a bar (here the DD cap, in 13 of 28 cases) rejects the cell
   at zero cost and says nothing about cost; a value at the scan ceiling (13 of 27 family-B cells)
   is a floor, not a breakeven;
3. **the panel**, because c* ranks by turnover only within one (U56 spearman -1.000) and by edge
   across them (B136 slack spearman +0.983). Cross-panel c* comparisons in the record are not
   cost comparisons.

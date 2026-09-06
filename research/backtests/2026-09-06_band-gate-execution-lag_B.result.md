# Idea 58 — band-gate-execution-lag (lane B, 2026-09-06)

**Verdict: ANSWERED / conditional KILL.** The cross-universe 4b pass of idea 57's standing
candidate is lost on the **execution-lag axis, not the cost axis**. At PROTOCOL's 1-day
execution it survives every rung the queue entry doubted; at a 1-week execution lag it
fails 4b on B136 at **every** cost rung, 5 through 25 bps. No new KEEP; no RULES change.

Script `research/backtests/2026-09-06_band-gate-execution-lag_B.py`.
Outputs: `.console.txt`, `.grid.csv` (260 rows), `.lagprice.csv`, `.walkforward.csv`,
`.crossuniverse.csv`.

## Design

6 books (band ∈ {0%, 3%, 6%} × gate composition ∈ {TREND = band only, FULL = band &
`vol20 < 0.60`}) — **exactly two tuned parameters** — each run under both de-grossing
conventions (`rw` gross re-spread over survivors / `dg` gated weight to cash), plus a
NOGATE always-invested control. Gross pinned at idea 57's 0.75, weekly cadence, neither
swept. The convention is **not** a tuned dial: idea 82 established this book's verdict
flips with it, so both readings are carried in full and neither is selected over the
other. Stress axes: cost {5, 10, 15, 20, 25} bps × lag {1d, 1w}, where `1w` shifts the
weight matrix 4 extra trading days so a Friday-close signal executes the *following*
Friday. Universes u56 and B136, **both primary**. All 260 grid points reported.

## An identity problem found in flight

The record quotes **two different books** as "idea 57's ew-band3". Both reproduce here to
the published digits (u56, 10 bps, 1d, weekly, gross 0.75, `rw`):

| reading | CAGR / Sharpe / MaxDD | record row |
|---|---|---|
| `band3-T-rw` band only | 12.25% / 1.1609 / −17.71% | idea 94 `u56 EWall + band3-rw` (12.2 / 1.160 / −17.7) |
| `band3-F-rw` band & vol20 | 11.26% / 1.1348 / −15.14% | idea 66/268 `ew-band3 g=0.75` (11.3 / 1.136 / −15.1) |

So the book the queue calls "ew-all + 3% band" — the one carrying the standing 4b
KEEP-candidate numbers — **still carries RULES v1's `vol20 < 0.60` leg**. Both are
carried through every cell below. A third reading, `band3-T-dg`, is byte-identical to the
live RULES v2 book.

**Reproduction gates, all four binding:**

| gate | result |
|---|---|
| [a] `fast_bt` + analytic cost vs `engine.backtest` (10 bps, 1d) | max\|diff\| **0.000e+00** |
| [b] `band3-T-rw` vs idea 94's published row | 12.25%/1.1609/−17.71% **PASS** |
| [b] `band3-F-rw` vs idea 66/268's published row | 11.26%/1.1348/−15.14% **PASS** |
| [b] `band3-T-dg` vs idea 60's LIVE RULES v2 gate | 8.66%/1.2056/−12.05% **PASS** |
| [c] `weights(band3-T-dg)` vs `baseline.rules_v2_weights` elementwise | max\|diff\| **0.000e+00** |

## The answer: where the cross-universe 4b pass is lost

A cell passes cross-universe iff it passes 4b on u56 **and** B136. **18 of 120** gated
cells do.

**The standing candidate (`band3-F-rw`)**

| | 5 bps | 10 | 15 | 20 | 25 |
|---|---|---|---|---|---|
| u56, 1d | PASS | PASS | PASS | PASS | fail(CAGR) |
| u56, 1w | PASS | PASS | PASS | fail(CAGR) | fail(CAGR) |
| B136, 1d | PASS | PASS | PASS | fail(CAGR) | fail(CAGR) |
| B136, 1w | fail(DD) | fail(DD,CAGR) | fail(DD,CAGR) | fail(H2,DD,CAGR) | fail(H2,DD,CAGR) |

Cross-universe: **1d passes at 5/10/15 bps and dies at 20; 1w never passes, at any cost.**

**The band-only reading (`band3-T-rw`, idea 94/82's book)**

| | 5 bps | 10 | 15 | 20 | 25 |
|---|---|---|---|---|---|
| u56, 1d | PASS | PASS | PASS | PASS | PASS |
| u56, 1w | PASS | PASS | PASS | PASS | PASS |
| B136, 1d | PASS | PASS | PASS | PASS | PASS |
| B136, 1w | fail(DD) | fail(DD) | fail(DD) | fail(DD) | fail(DD) |

Cross-universe: **10/10 at 1-day (confirming idea 82's ≥25–30 bps breakeven), 0/10 at
1-week.** The entire cost robustness idea 82 celebrated is erased by four days of
execution staleness, and the bar it breaks is drawdown, not cost.

So the queue's premise — "dies between 10 and 25 bps" — is **right for the FULL-gate
candidate (dies at 20) and wrong for the band-only one (survives 25)**, and both are
strictly dominated by the lag axis, which the record had never priced for this book.

## Mechanism: the lag is a drawdown tax, not a return tax

Over all 24 gated (universe × book) pairs, 1w minus 1d at 10 bps, paired daily:

- **Return effect ≈ zero:** mean ΔCAGR **+0.082%/yr**, max \|t\| over the 24 books **0.95**,
  **0 of 24** significant at 5%.
- **Drawdown effect systematic:** MaxDD **deepens in 23 of 24** books, mean **−1.35pp**
  (worst −3.98pp); Sharpe falls in 22 of 24.
- **Placebo:** NOGATE — no gate to be stale about — has ΔMaxDD **+0.00% on both universes**
  and ΔSharpe +0.0016 / −0.0005.

Concretely, `band3-T-rw` on B136 goes −18.53% → **−21.38%** MaxDD, straight through 4b's
−20.23% cap (60% of SPY's −33.72%), while its CAGR moves −0.01%/yr. Waiting a week to
execute a *gate* means you are still holding what the gate told you to sell, exactly when
selling was the point — the loss is invisible in the average and lands in the tail.

## Both KEEP paths

- **4a: 2 of 260 cells.** Both are `band3-T-dg` at 5 bps / 1d — i.e. the live RULES v2 book
  itself, undercharged. At PROTOCOL's 10 bps nothing beats the live book. Idea 136's
  finding a further time.
- **4b: 61 of 240 gated cells** (u56 24 at 1d / 18 at 1w; B136 18 at 1d / **1** at 1w).
- First-failing 4b bar across all cells: **CAGR 151**, DD 36, H2 7, H1 2, OOS 2 — the CAGR
  floor kills the de-grossed (`dg`) books wholesale, the drawdown cap kills the lagged ones.

## Rule 8 walk-forward (2009–2016 → 2017–2026, selection run inside each convention)

| universe / conv | IS-Sharpe pick | mean OOS Sharpe | mean OOS CAGR | mean OOS MaxDD |
|---|---|---|---|---|
| u56 rw | `band3-T-rw` 10/10 | 1.1712 | 13.12% | −18.18% |
| u56 dg | `band3-T-dg` 10/10 | 1.2610 | 9.49% | −12.38% |
| B136 rw | `band3-T-rw` 4/10 | 1.0666 | 12.19% | −20.62% |
| B136 dg | `band6-T-dg` 6/10 | 1.0692 | 7.97% | −14.17% |
| SPY | — | 0.8820 | 15.45% | −33.72% |
| RULES v2 | — | 1.2851 (u56) / 1.1185 (B136) | — | — |

Every IS-Sharpe pick beats SPY OOS **40/40**, and the 3% band is the IS pick in 24 of 40
cells, so rule 8 does select this family — but it never selects it *over the live book*
(RULES v2's OOS Sharpe is higher in both universes), and the IS-4b-constrained selector
finds **no eligible book at all** under `dg` in 20/20 cells.

## Verdict and scope

**Conditional KILL, recorded not promoted.** Idea 57's candidate keeps its cross-universe
4b pass only under PROTOCOL's own next-day execution and only to 15 bps (FULL gate) or
25 bps (band-only). Under a 1-week execution lag it fails cross-universe at every cost
rung tested, on drawdown. Since the book is already the standing candidate, this narrows
its scope rather than adding one: **any RULES wording for it must name both the
de-grossing convention (idea 82) and next-day execution**, because both are load-bearing.

No new KEEP-candidate, so no memo with RULES wording is proposed.

**SURVIVORSHIP:** both lists are current constituents, so absolute CAGRs are optimistic.
The lag and cost comparisons hold names, days, gate, gross and cadence fixed and are far
less exposed than the levels are.

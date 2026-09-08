# Idea 444 — publish the EXACT per-cell means beside every local-mean reading (cloud, 2026-09-08)

Script: `2026-09-08_publish-the-EXACT-per-cell-means-beside-every-local-mean-reading_cloud.py`
Console: `.console.txt` · CSVs: `.enumeration .balance .identity .exact .bookgrid .walkforward .keeppaths`

**Verdict: SPLIT.** Idea 440's identity is CONFIRMED and generalised from 1 curve to 8; the
queue's statement of its premise is FALSIFIED (balance is not the premise, alignment is);
the queue's ONE-DIRECTION corollary is FALSIFIED on the very curve it was drawn from. No new
capital candidate; the rule-8 book replicates the standing gross-1.00 4b family exactly.

## Reproduction gates (binding, before any new number)
| gate | published | here |
|---|---|---|
| idea 219 crossing from its own 560 cells | 0.425 / last non-pos 0.400 | 0.425 / 0.400, 560 cells — MATCH |
| idea 440 identity on 168c's 32 cells, 55 grid points | 5.55e-17 | 5.55e-17 — MATCH |
| idea 440 EXACT crossing on 168c | +0.10 | +0.10 — MATCH |
| `fast_backtest` vs `engine.backtest`, RULES v2 / U56 | — | max abs diff 0.000e+00 |

## A. Enumeration — 11 committed pooled curves
Idea 439's 10 admitted items (registry imported verbatim) + idea 440's own 528-book k panel
(`.grid.csv`, the 11th, which the 439 census predates). The queue's count of 11 is confirmed.
Idea 439's 4 NOT-re-readable files are re-printed in the console so the scope is checkable.

## B. THE PREMISE IS TWO CONDITIONS, NOT ONE (the queue says only "balanced")
| item | x lvls | grid | mean n | count imbal | comp | align | ALIGNED | bal-for-theorem |
|---|---|---|---|---|---|---|---|---|
| 219 | 242 | 33 | 2.4 | 41.01 | 0.021 | 0.295 | . | . |
| 167 | 10 | 10 | 12 | 0.0000 | 1.000 | 1.000 | Y | Y |
| 159B | 10 | 10 | 12 | 0.0000 | 1.000 | 1.000 | Y | Y |
| 159c | 14 | 14 | 3 | 0.0000 | 1.000 | 1.000 | Y | Y |
| 168B | 9 | 9 | 54 | 0.0000 | 1.000 | 1.000 | Y | Y |
| 168c | 11 | 11 | 32 | 0.0000 | 1.000 | 1.000 | Y | Y |
| 103 | 192 | 25 | 6 | 0.0000 | 0.167 | 0.010 | . | . |
| 61 | 48 | 25 | 8.5 | 0.8824 | 0.312 | 0.059 | . | . |
| 277 | 8 | 8 | 42 | 0.0000 | 1.000 | 1.000 | Y | Y |
| bandgate | 7 | 7 | 24 | 0.0000 | 1.000 | 1.000 | Y | Y |
| 440grid | 11 | 11 | 48 | 0.0000 | 1.000 | 1.000 | Y | Y |

**9 of 11 are count-balanced but only 8 are ALIGNED**, and alignment is the binding condition:
the balance TOLERANCE (P1) never changes the answer at 0.00, 0.05, 0.10 or 0.25 — 8 of 11 at
every tolerance. Item 103 is count-balanced (exactly 6 cells at each of its 192 x levels) and
still fails the theorem, because its x is a CONTINUOUS covariate (realised correlation) read
on a 25-point linspaced grid: only 1.0% of its cells sit on a grid centre. Measuring balance
on the reading grid rather than on the design's own support manufactures a pass — that is why
this run measures counts on the support and alignment against the grid, separately.

## C. THE IDENTITY, MEASURED — max |windowed − re-average of per-x means|
| | items | range over all grid points and all 6 half-windows |
|---|---|---|
| BALANCED-FOR-THE-THEOREM | 8 | 0.0 to **2.84e-14** (machine zero) |
| the rest | 3 | **5.17e-02 to 1.18e-01** (103, 61, 219) |

Clean partition, no overlap, 12 orders of magnitude. Idea 440's 5.55e-17 on 168c is reproduced
to the digit and now holds on 8 curves, not 1. Where it fails, this run names WHICH premise
failed: all 3 failures are NON-ALIGNMENT (a continuous covariate), not imbalance — so on those
curves the window is a genuine bandwidth doing real work and the reading IS a bandwidth choice.
Item 61 is additionally count-imbalanced (0.88), 219 severely so (41.0).

## D. WHAT MOVES
- **4 of 11** crossing readings move off the exact one at some half-window; **9 of 11** argmax
  readings move (up to 18 grid steps, item 61).
- Restricted to the 8 curves where an exact reading exists at all: crossing moves on 3, argmax on 6.
- On **2 of the 4** (219, 277) the window **MANUFACTURES a crossing the exact curve has none of**.
  That is a stronger failure than relocation and the queue does not name it.
- **The ONE-DIRECTION corollary FAILS.** It is testable only where both readings are finite:
  2 curves. `bandgate` moves in one direction (−1); **168c moves in BOTH (−1 and +1)** —
  exact +0.10, hmult 0.5 reads 0.00, then 0.10 / 0.10 / 0.50 / 0.75 / 1.00. The curve idea 440
  drew the corollary from is the one that refutes it.
- Against what was published: 4 of 11 curves publish a NUMBER at all; **1 of 4 moves**
  (159c, 0.85 → 0.03, 12 grid steps — already flagged by idea 439 as a fitted, not a
  pooled-curve, location). 219's 0.425 and 61's 0.5 have **no exact reading to compare** —
  their curves admit none.

## E. Rule 8 (PROTOCOL 8), live prices — 252 books, 10 bps, t+1
3 panels × gross {0.75, 1.00} × cadence {W, M} × 21 bands (0.00–0.20 step 0.01). x = band,
y = IS (≤2016-12-31) Sharpe minus the same cell's bare-200d IS Sharpe. This curve is
balanced-for-the-theorem by construction (20 levels × 12 cells, alignment 1.000) and the
identity holds at 1.4e-17. **The exact per-x means are published in the console — the column
this idea exists to require.**

| read | adopted band | OOS CAGR | OOS Sharpe | OOS MaxDD | full Sharpe |
|---|---|---|---|---|---|
| EXACT (per-x means), crossing | 0.01 | 8.44% | **1.0043** | −15.49% | 0.9723 |
| windowed crossing, hmult 0.5–5 | 0.01 (all) | 8.44% | 1.0043 | −15.49% | 0.9723 |
| EXACT argmax | 0.10 | 8.71% | 0.9574 | −18.80% | 0.9721 |
| windowed argmax, hmult 4 / 5 | 0.12 / 0.13 | 8.73% / 8.63% | 0.9533 / 0.9509 | −18.79% / −18.20% | — |
| bare 200d gate (band 0) | 0.00 | 8.29% | 0.9930 | −15.32% | 0.9651 |
| live RULES v2 band | 0.03 | 8.51% | 0.9871 | −16.52% | 0.9701 |
| ORACLE (best OOS band per cell) | — | 8.83% | 1.0325 | −16.24% | 1.0050 |

**The exact and windowed CROSSING reads adopt the same band 0.01 at every half-window: OOS
Sharpe spread 0.0000.** The ARGMAX read spreads 0.0065 of OOS Sharpe (0.9509–0.9574) and
0.60 pp of drawdown across the same reads — consistent with idea 441's finding that the columns
earn their place on the argmax, not the crossing. Publishing the per-x means costs nothing and
removes the ambiguity for the crossing entirely.

Benchmarks (full / OOS): SPY 15.23% / 0.8891 / −33.72%, OOS 15.45% / 0.8822; RULES v2 (live)
U56 8.66% / 1.2058 / −12.05%, OOS 9.53% / 1.2853; B136 8.03% / 1.1059, OOS 1.1187; SMALL439
3.81% / 0.5725, OOS 0.5682. RULES v1 U56 6.46% / 0.6648, OOS 0.7472.

## Both KEEP paths, all 252 books
**4a 2/252** (SMALL439 gross 0.75 W, bands 0.04 and 0.05 — 0.587/0.618 vs v2's 0.5725).
**4b 54/252**, all at gross 1.00, U56 34 + B136 20, every band 0.00–0.20 — an exact replication
of idea 441's 54, i.e. the already-committed cash-carve-out-removed family (ideas 439/441/144),
not a new object. Binding 4b bars: CAGR 170, H1/H2/OOS 84 each, DD 62.
The EXACT-adopted and every WINDOW-adopted band land on the same side of both paths
(4a 0/12, 4b 3/12 at band 0.01) — **the reading convention does not move a KEEP verdict here.**
**No memo and no new candidate.**

Difference from idea 441 worth recording: this run drops the 44 SMALL tickers with
max_1d_move ≥ 1.0 (439 names + SPY); idea 441 ran the unfiltered 483. That accounts for the
4a count 2 here vs 1 there. All other counts match.

## SURVIVORSHIP
SMALL439 and B136 are current constituents only; level numbers are upward-biased and only
same-panel contrasts are read. Every census number in A–D is a re-read of committed artefacts
and carries whatever bias the source run carried.

## Proposed PROTOCOL wording (supersedes idea 441's half-window column)
> Any published location on a pooled curve must state (a) whether its x is a DISCRETE DIAL
> whose levels are the reading grid or a CONTINUOUS covariate read through a bandwidth;
> (b) if a dial, the unsmoothed per-x cell means and the per-x cell counts, since the windowed
> curve is then an exact unweighted re-average of them and carries no information they do not;
> (c) if a continuous covariate, the half-window, because there the reading is irreducibly a
> bandwidth choice and no exact reading exists.

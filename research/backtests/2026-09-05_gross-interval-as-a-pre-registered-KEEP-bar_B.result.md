# Idea 90 — gross-interval-as-a-pre-registered-KEEP-bar (lane B, 2026-09-05)

**ANSWERED — KILL of the proposal as written; the object survives, the WIDTH does not, and the
statistic that actually carries the information is the CELL COUNT, which is already a pass/fail.**

Script `2026-09-05_gross-interval-as-a-pre-registered-KEEP-bar_B.py`; console
`...console.txt`; data `...family.csv.gz` (7,650 rows), `...intervals.csv`, `...is_oos.csv`,
`...bargrid.csv`, `...walkforward.csv`.

## Harness (run before any new number is read)
Idea 94's simulator imported; idea 144's gross family rebuilt and compared cell-by-cell against
its committed `family.csv.gz`: **7,650 of 7,650 rows, index identical, max|diff| = 5.0e-7 on
IS_Sharpe** — which is that file's own 6-decimal rounding, not a harness difference — and **0 of
7,650 `pass4a` disagreements**. Idea 144's census comes back exactly: FAMILY-4b **72** at
m ≤ 1.30, **58** at m ≤ 1.00, POINT-4b **29** at m = 1.00 (published 72 / 58 / 29).
4a: 97 books at m = 1.00, 184 somewhere in their family.

Corpus: 3 panels × 3 books × 17 arms × 2 cost rungs = **306 books**, each swept over
m ∈ {0.10, 0.15, …, 1.30} = 25 points → **7,650 backtests**. Weekly, t+1, 75% target gross at
m = 1.00, 10 and 25 bps, IS ≤ 2016-12-31, OOS ≥ 2017-01-01, bars held at the published
φ = 0.70 / δ = 0.60. Tuned parameters: exactly two — w\* (width threshold, 13 values) and k
(cells required, 4 values); **all 52 grid points printed**. The gross ceiling m_max ∈ {1.00, 1.30}
is an arm, reported everywhere, not tuned.

## Q1 — the object is real: the passing set IS an interval
**100% contiguous.** Full-sample bars: 72 of 72 non-empty books are a single run at m ≤ 1.30,
58 of 58 at m ≤ 1.00, `n_runs` max **1**, and there are **no exceptions to list**. IS bars 66/67
and OOS bars 70/71 (one book each with two runs, both at the 1.30 ceiling). Contiguity holds for
the four arms idea 144 flagged as *not* scale-free too (`bud` 9/9, `dd` 8/8), so the interval is
a well-defined object for the whole corpus, not only for pure exposure rescales. Idea 90's
premise passes.

## Q2 — census
Non-empty intervals by cell (m ≤ 1.30): u56@10 **31 of 51**, u56@25 **23**, broad@10 **14**,
broad@25 **4**, **small@10 0 and small@25 0**. Widths over non-empty books: median **0.15**,
quartiles 0.10 / 0.21, max **0.40** (`u56|TOP20|10|vol60-dg`, m ∈ [0.85, 1.20]). By kind, mean
width is 0.047 (gate) / 0.038 (dd) / 0.031 (bud) / 0.028 (ctl) / 0.010 (stop).
**The small panel has no interval at any gross level, on either cost rung, for any of its 102
books** — direct support for queue idea 136's framing.

The queue's own operational KEEP (non-empty on BOTH large-cap universes at BOTH cost rungs)
admits **4 of 51 (book, arm) pairs at m ≤ 1.30** and 3 at m ≤ 1.00, and in all four the
**intersection is non-empty** — a single gross level clears all four cells:

| book\|arm | broad@10 | broad@25 | u56@10 | u56@25 | intersection |
|---|---|---|---|---|---|
| EWall\|vol60-dg | 0.20 | 0.20 | 0.30 | 0.30 | **m ∈ [0.95, 1.05], width 0.15** |
| EWall\|vol60-rw | 0.15 | 0.15 | 0.25 | 0.20 | m ∈ [0.90, 0.95], width 0.10 |
| EWall\|band3-rw | 0.15 | 0.10 | 0.30 | 0.20 | m ∈ [1.00, 1.05], width 0.10 |
| EWall\|ddctl-8/.5/recover | 0.15 | 0.15 | 0.20 | 0.20 | m = 1.15, width 0.05 |

The first and third are the project's two standing cross-cell 4b passers (idea 127), recovered
here independently and now with an explicit sizing range rather than a point.

## Q3 — the decisive test: the width adds nothing to the pass/fail it refines
**(a) Cross-cell portability.** Spearman(width in a cell, number of the other three cells
non-empty) = +0.596 / +0.405 / +0.712 / +0.758 against the **binary** pass/fail's +0.594 /
+0.405 / +0.741 / +0.733 — the graded statistic is *worse* in two cells, tied in one, better in
one by 0.002. The lowest non-zero width is 0.05, so the w\* = 0.05 row of the conditional table
**is** the pass/fail row (identical n and lift in 4 of 4 cells). The one place grading looks
better is a mid threshold read in-sample — at w\* = 0.15 the lift over the base rate goes
0.207 → 0.422 (broad@10), 0.051 → 0.112 (u56@10), 0.095 → 0.285 (u56@25) — and that is a
threshold chosen after seeing 51 books; it is not confirmed by either rank correlation or Q4.

**(b) In-sample → out-of-sample, the test that matters.**
| statistic measured on 2009-2016 | Spearman vs OOS width | Spearman vs OOS Sharpe @ m=1 |
|---|---|---|
| IS interval **width** | **+0.307** | **+0.540** |
| IS **pass/fail** (non-empty at all) | +0.296 | **+0.546** |
| IS **Sharpe** @ m=1 (the incumbent selector) | — | **+0.902** |

The width buys **+0.011** of rank correlation over a binary on OOS width and **loses 0.006** on
OOS Sharpe; the incumbent IS-Sharpe carries 1.7× either signal. Conditioning on books that pass
at all, the grade collapses to +0.177 (OOS width) and **+0.055** (OOS Sharpe) over 67 books —
i.e. **once a book has an interval, how wide it is says essentially nothing about what happens
next.** P(OOS non-empty | IS width ≥ w) is also non-monotone: 0.478 (w = 0.05) → 0.512 (0.20) →
0.656 (0.25) → **0.444** (0.30) → 0.000 (0.45, one book). Base rate 0.232; P(·|IS pass) 0.478;
P(·|not IS pass) 0.163.

## Q4 — as a bar (52 grid points, all printed)
Admitted-set mean OOS Sharpe / CAGR / MaxDD on the four large-cap cells:

| bar | admits | OOS Sharpe | OOS CAGR | OOS MaxDD |
|---|---|---|---|---|
| no bar (whole large-cap corpus) | 51 | 0.827 | 9.4% | -19.9% |
| w\* = 0.05, k = 1 (= "non-empty somewhere") | 31 | 1.022 | 12.3% | -20.0% |
| w\* = 0.30, k = 1 | 11 | **0.989** | 12.6% | -19.4% |
| w\* = 0.05, k = 3 | 12 | 1.039 | 13.3% | -20.8% |
| w\* = 0.05, k = 4 | 4 | **1.126** | 11.8% | -18.0% |
| POINT-4b in ≥ 3 of 4 cells | 2 | 1.126 | 12.1% | -18.0% |

**All of the improvement is k, none of it is w\*.** Holding k = 1, pushing the width threshold
from 0.05 to 0.30 discards 20 of 31 books and *lowers* mean OOS Sharpe (1.022 → 0.989). Holding
w\* at its floor, raising k from 1 to 4 lifts it 1.022 → 1.126. And plain POINT-4b in ≥ 3 cells
already reaches 1.126 with 2 books. A width bar buys nothing a cell count does not already buy.

## Q5 — rule 8 walk-forward (screens read 2009-2016 only; OOS read once)
S0 no screen · S1 IS-POINT-4b (incumbent) · S2 IS-FAMILY-4b (idea 144) · S3 widest IS interval,
traded at its midpoint m · S4 widest IS interval, traded at the published m = 1.00.

Cells entered, of 18: S0 18, **S1/S2/S3/S4 all 7** (every screen declines all 6 small-panel cells
and all 4 V1u cells — idea 132's "abstention is the screen", reproduced on a sixth bar).
Picks that move vs S0: **S1 0, S2 0, S3 2, S4 2.**

Paired on the 7 cells every selector enters (mean of per-cell OOS statistics):

| | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|
| S0 / S1 | 12.70% | 1.0219 | -21.14% |
| S2 (family) | 13.79% | 1.0192 | -22.81% |
| **S3 (width, midpoint m)** | 13.06% | **1.0397** | -20.98% |
| **S4 (width, m = 1.00)** | 12.90% | **1.0397** | -20.80% |
| SPY | 15.45% | 0.882 | -33.72% |
| RULES v1 | 4.77% | 0.480 | -19.67% |

The width selector is the **second non-inert screen the project has** and the first that does not
lose Sharpe: +0.018 over the incumbent, 0.2-0.3pp shallower drawdown, +0.2-0.4pp CAGR. But it is
**two moved picks in seven cells** — `band3-rw` for `abs12-rw` on u56/EWall@10 (+0.171) and
`band3-rw` for `vol60-dg` on broad/EWall@10 (-0.046) — one win and one loss, i.e. the paired
gain is one substitution. That is not evidence. All four screens beat SPY in 5 of 7 cells and
RULES v1 in 7 of 7; unscreened S0 beats SPY in 6 of 18 and RULES v1 in 12 of 18.

## Verdict
**KILL of idea 90 as written.** The interval is a real object (Q1) and its census is worth having
(Q2), but the *width* is not a robustness statistic: it does not beat the binary it refines on
either cross-cell portability or out-of-sample rank correlation, it adds nothing once a book
passes, and as a bar it strictly destroys admitted-set OOS quality while the cell count creates
it. No new book, no KEEP, nothing promoted. Two things do survive and go to the Sunday review as
an amended PROTOCOL proposal (memo `...memo.md`): report the **number of cells** in which the
interval is non-empty, and report the **intersection** [m_lo, m_hi] — the range of gross a
candidate could actually be sized at — instead of a single m.

## Caveats carried, not buried
Survivorship on all three current-constituent panels (idea 54); the IS window's shallower SPY
drawdown biases every Q5 selector identically (idea 128); the calendar-day index (idea 38) and
t+1-only execution (idea 126) carry over; 7 paired walk-forward cells and 11 of 18 cells entered
by no screen at all; the small panel contributes zero intervals, so every Q3/Q4 statistic is a
large-cap statistic; and the `ebud`/`ddctl` arms are not scale-free (idea 144), so their
"interval" mixes exposure with instrument strength even though it is contiguous.

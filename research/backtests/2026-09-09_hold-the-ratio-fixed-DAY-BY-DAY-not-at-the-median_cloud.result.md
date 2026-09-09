# Idea 272 — hold the ratio fixed DAY BY DAY, not at the median (cloud, 2026-09-09)

**Verdict: ANSWERED. Both of idea 269C's structural findings SURVIVE the day-by-day fix —
the reversal-share curve still rises before it falls (2 direction changes, Spearman −0.375
collapsing to −0.124 once the r=1 identity cell is dropped, against the parent's −0.386 →
−0.181) and the five panels still disagree at matched ratio in 6 of 7 rows. The queue's
premise about the CONSTRUCTION is nonetheless confirmed and it matters somewhere else:
fixing n at the median realises a mean ratio 1.53× its own label and saturates up to 53.8%
of rebalance days, and correcting that DELETES 6 of the 8 published 4b passes on this grid
(FIXED 8/35 → DYN 2/35 at 10 bps). No KEEP-candidate, no memo, no RULES change; RULES.md,
PROTOCOL.md, scan.py, bot.py and baseline.py untouched.**

Script `2026-09-09_hold-the-ratio-fixed-DAY-BY-DAY-not-at-the-median_cloud.py`; outputs
`.grid.csv` (240 rows — ALL grid points), `.reversal.csv`, `.drift.csv`,
`.walkforward.csv`, `.console.txt`. Runtime 310 s. Idea 269C's five panels and seven
pre-registered ratios unchanged; key = composite WITHOUT the vol scaler; gate = above-200d
AND vol20 < 0.60; equal weight at gross 0.75; weekly; t+1 execution. 10 bps headline with
0 bps (the parent's diagnostic) and 25 bps beside it. Tuned parameters: **two, the queue's
own** — construction ∈ {FIXED, DYN} and the target ratio r*. Panel and cost rung are
enumerated axes and every point is reported.

* **FIXED** — `n = max(1, round(r* × median n_elig))`, idea 269C verbatim.
* **DYN** — `n_t = clip(round(r* × n_elig,t), 1, n_elig,t)`, recomputed every day.

## Reproduction gate — the FIXED arm reproduces idea 269C

| | here | 269C |
|---|---|---|
| reversal share by r* (10 bps) | **0.60 / 0.60 / 0.80 / 0.80 / 0.40 / 0.40 / 0.00** | 0.60 / 0.60 / 0.80 / 0.80 / 0.40 / 0.40 / 0.00 |
| per-panel counts | **B136 6/7, BSTK100 6/7, U56 4/7, ETF36 2/7, SMALL439 0/7** | identical |
| B136/EWall | **0.107162 / 1.026118 / −0.176879, OOS 1.018548** | 0.107162 / 1.026118 / −0.176879, OOS 1.018548 |
| KEEP @0 bps (45-row denominator) | **4a(v1) 3, 4b 12** | 3, 12 |
| KEEP @10 bps | 4a(v1) **6**, 4b **9** | 6, **8** |

**One row differs and it is a data-vintage effect, stated rather than smoothed over.**
`data/prices.csv` has advanced from 2026-09-04 to 2026-09-08 since the parent ran, so the
U56 panel carries two extra trading days; `data/prices_broad.csv` and the small panel are
unchanged, which is why B136/EWall reproduces to six decimals and U56 moves in the fourth.
The single flipped verdict is **U56/FWD41 (r\* = 1.00)**, which failed the parent's 4b CAGR
floor by **−0.000076** of CAGR and clears it here by **+0.000024** — a published KEEP/KILL
decided by 7.6 bps of annual return, i.e. a live instance of idea 408's "publish the margin
beside the verdict". Every other published number reproduces.

## The queue's premise, measured

| | FIXED | DYN |
|---|---|---|
| mean realised ratio ÷ target | **1.529** (1.081 – 1.960) | **1.022** (0.997 – 1.275) |
| mean sd of the realised ratio (finite panels) | **1.455** | **0.022** |
| max `sat_share` (rebalance days holding every eligible name) | **0.538** | **0.010** at r\* < 1 |

The premise is correct and understated. Because `n_elig,t` moves 18 → 48 on U56 and
48 → 116 on B136, a *fixed* n realises `n/n_elig,t` well above its label on low-breadth
days — the parent's "r = 0.35" cell actually runs at a mean realised ratio of 0.47 (U56) to
0.68 (SMALL439). The day-by-day construction pins it: realised/target 1.022, and the only
departures are the r\* = 0.05 cells on the two panels where the `n_t ≥ 1` floor binds.
Under DYN the r\* = 1.00 cell becomes an **exact identity with EWall** (`n_t = n_elig,t`
every day), where the parent's r = 1 cell saturated only 50–54% of days — so the reversal
grid now terminates on a genuine identity rather than an approximation of one.
(`.drift.csv` reports `inf` for BSTK100 because that panel has rebalance days with
`n_elig = 0`; the summary above is computed on the four panels where the ratio is finite,
and BSTK100's `sat_share` column is unaffected.)

## Q1 — the NON-MONOTONICITY survives

Reversal share by r\* = 0.05 … 1.00:

| rung | construction | curve | turns | Spearman | t | Spearman w/o r=1 | t |
|---|---|---|---|---|---|---|---|
| 10 bps | FIXED | 0.60 / 0.60 / 0.80 / 0.80 / 0.40 / 0.40 / 0.00 | 1 | −0.372 | −2.30 | −0.159 | −0.85 |
| 10 bps | **DYN** | **0.80 / 0.60 / 0.60 / 0.80 / 0.80 / 0.40 / 0.00** | **2** | **−0.375** | **−2.33** | **−0.124** | **−0.66** |
| 0 bps | FIXED | 0.80 / 0.60 / 0.80 / 0.60 / 0.40 / 0.40 / 0.00 | 2 | −0.457 | −2.95 | −0.279 | −1.54 |
| 0 bps | DYN | 0.60 / 0.60 / 0.40 / 0.60 / 0.40 / 0.40 / 0.00 | 2 | −0.318 | −1.92 | −0.137 | −0.73 |
| 25 bps | FIXED | 0.60 / 0.60 / 0.60 / 0.60 / 0.60 / 0.40 / 0.00 | 0 | −0.314 | −1.90 | −0.099 | −0.52 |
| 25 bps | DYN | 0.60 / 0.60 / 0.60 / 0.20 / 0.60 / 0.60 / 0.00 | 2 | −0.258 | −1.53 | −0.039 | −0.21 |

The parent's exact shape reappears: a curve that **rises before it falls**, a nominally
significant pooled Spearman, and a **collapse to insignificance once the r = 1 identity
cell is dropped** (parent −0.386 → −0.181; DYN here −0.375 → −0.124). Holding the ratio
genuinely fixed does not rescue the width predictor — if anything it weakens it further,
and it does so with the identity cell now exact rather than approximate. **Idea 269C's KILL
of "reversal share is a monotone function of n / n_elig" stands, and is now stated on a
construction where the ratio really is the ratio.**

## Q2 — the PANEL DISAGREEMENT survives

Reversal count out of 7 ratios, 10 bps:

| panel | FIXED (= 269C) | DYN |
|---|---|---|
| B136 | 6 | **6** |
| BSTK100 | 6 | **5** |
| U56 | 4 | **6** |
| ETF36 | 2 | **2** |
| SMALL439 | 0 | **1** |

Rows where the five panels split (0 < share < 1): **6/7 under DYN, 6/7 under FIXED, 6/7
published**. The family ordering (large-cap panels high, ETF36 middling, SMALL439 lowest)
is unchanged. The one claim that softens is the parent's strongest single sentence —
SMALL439 reversing at **no** ratio — which becomes 1 of 7 once the ratio is held day by day;
ideas 271 and 277 both lean on that 0/7, so it should be quoted as "0/7 at fixed n, 1/7 at
fixed ratio" from here on.

Cell by cell the two constructions agree on **29 of 35** reversal flags. The six flips are
concentrated exactly where the queue said the drift would be worst: four of them (U56
r = 0.50 and 0.75, ETF36 r = 0.50, BSTK100 r = 0.75) are cells whose FIXED `sat_share` is
0.12 – 0.22 against a DYN `sat_share` of 0.000 – 0.010. The fix changes the answer where,
and essentially only where, the construction was actually drifting.

## Rule 8 walk-forward (r\* chosen on IS 2009–2016, OOS 2017+ read once, pooled over the 5 panels)

| book | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|---|
| FIXED r\*=1.00 (IS-argmax) | 8.67% | 0.8767 | −21.0% | 0.985 / 0.788 | 8.91% | 0.8689 | −21.0% |
| **DYN r\*=1.00 (IS-argmax)** | 8.48% | 0.8729 | −20.6% | 0.988 / 0.778 | 8.60% | 0.8563 | −20.6% |
| EWall (do nothing) | 8.49% | 0.8737 | −20.6% | 0.989 / 0.779 | 8.60% | 0.8567 | −20.6% |
| RULES v2 (live) | 6.82% | **1.0422** | **−11.2%** | 1.112 / 0.979 | 7.15% | **1.0761** | **−11.2%** |
| RULES v1 | 6.58% | 0.7379 | −17.3% | 0.904 / 0.601 | 6.41% | 0.6894 | −17.3% |
| SPY | 14.70% | 0.8870 | −33.7% | 0.968 / 0.831 | **15.43%** | 0.8812 | −33.7% |

Both constructions' IS-argmax lands on r\* = 1.00, i.e. **the selector chooses do-nothing**,
and under DYN that pick is EWall by identity (0.8563 vs 0.8567 OOS Sharpe is float noise in
the `n_t` rounding). As a decision the grid buys nothing: it trails the live book by 0.21 of
OOS Sharpe and 9.4 pp of drawdown, and SPY by 6.8 pp of OOS CAGR. **KILL as a book.**

## Both KEEP paths, all 210 arm rows

| rung | construction | 4a vs live RULES v2 | 4a vs RULES v1 | 4b |
|---|---|---|---|---|
| 0 bps | FIXED | **0/35** | 2/35 | 10/35 |
| 0 bps | DYN | **0/35** | 1/35 | **3/35** |
| 10 bps | FIXED | **0/35** | 5/35 | 8/35 |
| 10 bps | **DYN** | **0/35** | 2/35 | **2/35** |
| 25 bps | FIXED | **0/35** | 11/35 | 0/35 |
| 25 bps | DYN | **0/35** | 5/35 | 0/35 |

**This is the run's capital-relevant number.** The eight FIXED 4b passes at 10 bps are
exactly the record's published set (U56 FWD 14 / 20 / 31 / 41 and B136 FWD 35 / 50 / 74 / 99,
plus B136 EWall as a control). Under the day-by-day construction **only two survive** —
U56 r\* = 0.75 (11.38% / 1.0240 / −17.2%, halves 1.010 / 1.040, OOS 1.1106) and B136
r\* = 1.00, which is the EWall identity. Six of the eight were passing on a book that, on
low-breadth days, had quietly collapsed toward the wider EWall book the ratio label said it
was not. Nothing here is a new candidate: the two survivors are a known U56 arm and a
control. **4a against the live RULES v2 book is 0/35 in every construction and at every
rung** — the 4a pathology of ideas 136 / 482 again. Binding 4b bar over the failures at
10 bps: DD 62, H2 50, OOS 49, H1 38, CAGR 37.

## Caveats

SURVIVORSHIP: B136 / BSTK100 / ETF36 are current constituents of `universe_broad.json` and
SMALL439 is the 483-name sub-$2B screen with the 44 tickers whose `max_1d_move ≥ 1.0`
dropped first (`data/small_meta.csv`, `data/SMALL_PANEL_README.md`). Every panel is a
current-constituent list and the un-ranked EWall side takes the full survivorship premium,
so the bias runs **toward** reversals: the "still not monotone, still panel-dependent"
verdict is conservative, and the 4b counts on both constructions are upper bounds. Five
panels × seven ratios is 35 cells, a small denominator for a share; the per-panel counts are
7-cell binomials and idea 290's warning about ranking those applies here too. The data
vintage caveat above applies to every U56 number. No network was used.

## Proposed follow-ups

1. Re-read every committed matched-ratio result in the record under the DYN construction —
   this run says the ratio label and the realised ratio differ by a mean factor of 1.53.
2. Back-fill the CAGR-floor margin beside every published 4b verdict on this grid; U56/FWD41
   flipped on 7.6 bps of annual return between two data vintages four days apart.
3. Restate ideas 271 and 277's "SMALL439 reverses at no ratio (0/7)" as construction-
   dependent (0/7 fixed-n, 1/7 fixed-ratio).

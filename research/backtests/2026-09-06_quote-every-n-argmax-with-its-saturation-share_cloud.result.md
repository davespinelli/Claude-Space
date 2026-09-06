# Idea 242 — quote-every-n-argmax-with-its-saturation-share (cloud, 2026-09-06)

**Verdict: ANSWERED. The back-fill is done and the column is real but NARROW — 10 of 175
published argmax cells (5.7%) are at or past saturation, and all 10 sit on the two smallest
panels. As a *decision* rule the column is a KILL: the saturation cap never binds on any of
the 14 live IS argmaxes, so `SATARGMAX` is byte-identical to `ISARGMAX` in 14/14 cells. And
idea 240's headline correlation does not survive the record: Spearman(mean eligible count,
published n argmax) = +0.926 on its own 7 cells, +0.132 over the record's 175.**

Script: `2026-09-06_quote-every-n-argmax-with-its-saturation-share_cloud.py`
(10 bps, weekly, next-day execution; common window 2011-01-13 → 2026-09-04).
Harness sanity: reproduces idea 2's KEEP (U56/CAND20 12.7% / 1.092 / -18.3%, halves
1.088/1.102) and live v1 (6.5% / 0.664 / -13.8%) to the third decimal.
Small panel: 44 of 483 tickers with `max_1d_move >= 1.0` dropped per `data/small_meta.csv`;
439 tradable remain.

## 1. The saturation table (the deliverable column)

`u(P, n) = P(n_elig < n)` on weekly rebalance dates; `n_sat50` = widest `n` the panel fills
in a majority of weeks.

| panel | tradable | mean elig | n_sat25 | n_sat50 | n_sat75 | u at n=20 |
|---|---|---|---|---|---|---|
| U56 | 56 | 35.4 | 30 | 40 | 40 | 0.155 |
| ETF36 | 36 | 23.0 | 15 | 25 | 30 | 0.258 |
| ETF24 | 24 | 16.2 | 12 | 15 | 20 | **0.509** |
| STK20 | 20 | 12.4 | 10 | 12 | 15 | **0.994** |
| B136 | 136 | 86.5 | 60 | 80 | 100 | 0.078 |
| BSTK100 | 100 | 63.5 | 50 | 60 | 80 | 0.084 |
| SMALL | 439 | 135.0 | 100 | 120 | 150 | 0.056 |

Idea 240's two anchor numbers reproduce: STK20 u(20) = 0.994 (it published 99.3%),
SMALL u(20) = 0.056 (it published 0.9% on its 484-name variant; the difference is the 44
bad-print tickers this run drops). Full curve over 20 values of `n`: `.ucurve.csv`.

## 2. The census — how many published argmaxes are at or past saturation

Mechanical, not read out of prose: all 648 committed CSVs in `research/backtests/` were
scanned; 28 files carry a position-count sweep (≥3 distinct integer counts in [2,500],
beside a Sharpe column, from a script that actually ranks on that count), giving **184
argmax cells, 175 on a mappable panel**. 114 candidate columns were rejected with a logged
reason (`.census_rejects.csv`: 48 too few distinct values, 47 no Sharpe column, 13 whose
parent never ranks on a count, 6 out of range) so the denominator is auditable.

**10 of 175 (5.7%) are at or past their panel's saturation point.** They are not spread:

| panel | cells | mean n_argmax | mean under-fill | at/past saturation |
|---|---|---|---|---|
| B136 | 51 | 33.5 | 0.132 | 0 |
| SMALL | 44 | 21.3 | 0.059 | 0 |
| U56 | 48 | 18.3 | 0.170 | 0 |
| ETF36 | 8 | 20.0 | 0.258 | 0 |
| BSTK100 | 8 | 28.8 | 0.138 | 0 |
| **ETF24** | 8 | 17.5 | 0.435 | **6** |
| **STK20** | 8 | 15.0 | 0.609 | **4** |

All 10 are on the two panels with fewer than 25 tradable names. **55 of 175 cells sit at
their own grid top** — grid-edge argmaxes are 5.5× more common in the record than
saturated ones, so the edge problem idea 240 found is the larger one.

**Idea 240's correlation does not generalise.** Spearman(panel mean eligible count,
published n argmax) = **+0.132 (N=175)** over the record, against **+0.926 (N=7)** on idea
240's own cells. Idea 240's 7 cells were one sweep run on 7 panels with a shared grid; the
record's 175 cells carry 20 different grids, and the grid, not the panel, is what mostly
sets the argmax.

## 3. Saturation duplicates books (the one place the column changes a count)

Under NORM a saturated cell is byte-identical to the widest unsaturated one. **6 of 84 CAND
points are exact duplicates of a narrower `n`, and 3 of the 24 CAND 4b passes are such
duplicates** (STK20 NORM n=30/40/60 are all the n=20 book, Sharpe 1.341 each). Collapsing
them: NORM 4b goes from **13/42 raw to 10/36 distinct books**; FIXED is unaffected (11/42,
because under FIXED a saturated cell de-grosses instead of duplicating). Any pass-count
quoted over a saturating grid is inflated.

## 4. Rule 8 walk-forward — IS ≤ 2016-12-31, OOS ≥ 2017-01-01 read once

Pooled OOS Sharpe, equal weight over the 7 panels:

| rule | FIXED | NORM | OOS CAGR (F/N) | OOS MaxDD (F/N) |
|---|---|---|---|---|
| **NOTHING** (U56/n=20) | **1.168** | **1.131** | 14.4% / 14.5% | -18.3% / -18.3% |
| WIDEST (n=60) | 1.012 | 0.916 | 6.6% / 11.0% | -12.5% / -23.8% |
| RANDOM | 0.927 | 0.868 | 10.1% / 12.0% | -17.8% / -24.5% |
| ISARGMAX | 0.885 | 0.891 | 12.4% / 12.1% | -20.8% / -24.5% |
| **SATARGMAX** | **0.885** | **0.891** | 12.4% / 12.1% | -20.8% / -24.5% |
| NARROWEST (n=5) | 0.761 | 0.763 | 13.3% / 13.7% | -24.5% / -26.8% |

SPY OOS 15.5% / 0.882 / -33.7%; RULES v1 OOS 7.7% / 0.747 / -13.8%.

**SATARGMAX − ISARGMAX = +0.0000 in 14/14 cells; the picks differ in 0/7 panels on both
conventions.** Every IS argmax on this grid was already unsaturated (max under-fill at a
pick 0.205), so the constraint is inert. This is also the **13th** instance in the record of
a dial rule losing to doing nothing: NOTHING beats ISARGMAX by +0.283/+0.240 pooled OOS
Sharpe and beats a coin flip on the dial by +0.241/+0.263.

Q2 (does under-fill predict the argmax's OOS shortfall?) — the sign is **wrong for the
hypothesis**: Spearman(under-fill at pick, regret) = **+0.724 (N=14)**, i.e. the *more*
under-filled picks had *smaller* regret, not larger. With 0 saturated picks in the sample
there is no test of the actual claim; this is a null, not support.

## 5. KEEP paths, all 98 grid points

4a: **28/98** (CAND FIXED 23/42, CAND NORM 4/42). 4b: **28/98** (CAND FIXED 11/42, CAND NORM
13/42 raw → 10/36 distinct). SPY 14.1% / 0.862 / -33.7%, halves 0.891/0.858; 4b bars are
MaxDD ≤ 20.2% and CAGR ≥ 9.9%. Best 4b rows are the known ones — U56/CAND20 FIXED
12.5% / 1.092 / -18.3% (halves 1.059/1.127, OOS 1.168) and STK20/CAND10 NORM 21.6% / 1.344 /
-20.1% (halves 1.275/1.413, OOS 1.410) — **nothing new is promoted**; STK20 is the
20-mega-cap panel idea 10 already flagged as selection, and its two 4a passes (CAND10/CAND20
FIXED) are both on that panel.

## 6. What goes in the record

Publish `mean eligible count` and `under-fill share at the quoted n` beside any position-count
argmax **on a panel with fewer than ~25 tradable names**, where it is load-bearing; elsewhere
it is a constant near zero and costs a column for nothing. Do **not** promote it to a chooser
constraint — it never binds. The more valuable flag, on this evidence, is the one idea 240
already found: 55/175 published argmaxes sit at their own grid top.

**SURVIVORSHIP:** every panel is current constituents, one-directional, hardest on
STK20 / BSTK100 / SMALL. Widening `n` on such a list adds names known ex post to have
survived, so any "wider is better" reading — including the width premia this run re-prices —
is partly manufactured. The census inherits the bias of every parent script it reads.

Artefacts: `.grid.csv` (98), `.ucurve.csv`, `.panels.csv`, `.census.csv` (184),
`.census_rejects.csv` (114), `.duplicates.csv`, `.q2.csv`, `.walkforward.csv`, `.console.txt`.

# Idea 454 — are-the-record's-7-rung-ladders-two-rung-ladders (cloud lane, 2026-09-08)

**Verdict: SPLIT.** The deletion is safe for everything the queue asked about — the re-rank
verdict (33/33), the Sharpe LEVEL (max residual 0.0020 over the whole corpus) and the rule-8
chooser (33/33 identical picks, **0.0000** OOS Sharpe cost) — but it is *not* safe for the 4b
FAILING BAR (undetermined on **184 of 256 arms**), and it buys **14.1% of a 44-second run**.
The deletion is therefore admissible as a reporting convention and worthless as a compute
saving. No RULES change, no new book, no KEEP candidate. RULES.md, scan.py, bot.py and
baseline.py untouched.

## Corpus and gate

The record's own cost-ladder census, rebuilt end to end from prices: **3 panels x 3 books x
their dials = 33 cells, 256 arms, 1,792 grid points** — the same construction idea 228 used and
idea 230 published. Rungs are the record's standard 0/5/10/15/20/25/30 bps. Every grid point of
both tuned parameters (**rung pair**, **tolerance**) is reported; panels, books, dials, dial
grids and the two KEEP paths are the record's, not this run's.

**Gate:** the ladder identity `net(c) = gross - turnover*c/1e4` against `engine.backtest` at
10 bps, on both live baselines and all three panels: max abs daily difference
**6.9e-18 / 2.4e-17 / 1.9e-17** (RULES v2) and **6.9e-18 / 6.9e-18 / 1.4e-17** (RULES v1).

## (1) The verdict survives — but it is a property of the SPAN, not of "two rungs"

| pair | cells | reproduces the 7-rung re-rank verdict |
|---|---|---|
| **0-30 (endpoints)** | 33 | **33** |
| 0-20 | 33 | **33** |
| 5-25 | 33 | 31 (misses U56/TOPN/K, B136/V1C/K) |
| 0-10 | 33 | 30 (misses B136/EWALL/V, SMALL439/V1C/N, SMALL439/EWALL/K) |
| 10-30 | 33 | 27 (misses 6, all of them re-ranks that happen at or below 10 bps) |

11 of 33 cells are re-rankable. Idea 231's result is confirmed **for the endpoint pair only**:
drop to any interior pair and the verdict starts breaking, at up to 6 of 33 cells. The right
statement is "the ladder's ENDPOINTS carry the verdict", not "seven rungs are two rungs".
**Interior-only argmaxes: 0 of 33 cells here** — the 35 idea 231 found are not in this corpus.

## (2) The LEVEL is linear to within 0.002 Sharpe

`net(c)` is exactly linear in `c`, so any residual is the curvature of `Sharpe = mean/std`, and
it is tiny. Interior Sharpe vs the straight line between the 0 and 30 bps endpoints: **mean
0.00038, max 0.00199** over 33 cells; at PROTOCOL's binding 10 bps rung, **mean 0.00030, max
0.00148**. By dial (0-30): V 0.00071 / N 0.00043 / K 0.00021 / G 0.00018 — the worst-bending
cell in the record is SMALL439/EWALL/V at 0.00199. The interpolated 10-bps **argmax equals the
true 10-bps argmax in 33 of 33 cells, for all five pairs**.

Tolerance grid (cells whose whole interior is reproduced):

| tol | 0-10 | 0-20 | 0-30 | 10-30 | 5-25 |
|---|---|---|---|---|---|
| 0.000 | 0 | 0 | 0 | 0 | 0 |
| 0.001 | 33 | 33 | **29** | 32 | 33 |
| 0.005 and up | 33 | 33 | **33** | 33 | 33 |

## (3) Where an interior rung IS load-bearing: the 4b failing bar

At the binding 10 bps rung, with the 0 and 30 bps endpoints as the only evidence:

| quantity | recovered | undetermined (endpoints disagree) | recovered WRONG |
|---|---|---|---|
| 4a pass (vs RULES v2) | 256/256 | 0 | 0 |
| 4b pass (vs SPY) | 247/256 | **9** | 0 |
| **which 4b bar fails** | 72/256 | **184** | 0 |

The endpoints are never *wrong* — they are silent. 4a is recovered trivially because **4a passes
nowhere in the corpus vs the live RULES v2 book (0 of 1,792; 245 of 1,792 against the retired
v1)**. The 9 undetermined 4b arms are real: e.g. U56/EWALL/G=0.01, 0.02 and K=2 and TOPN/V=0.30
pass 4b at 0 and at 10 bps but fail on DD at 30, while U56/V1C/N=10 passes at 0, fails on H2 at
10 and fails on five bars at 30. **The failing-bar column that the LEADERBOARD publishes is not
a two-rung readable quantity** — it turns over on 72% of arms between 0 and 30 bps.

## (4) The compute the deletion buys: 14.1% of 44 seconds

Measured, not assumed: **simulation 35.5s + 7-rung scoring 8.7s = 44.2s** over 232 simulations
and 1,792 grid points. All seven rungs share ONE simulation under the net identity, so deleting
5 of 7 rungs saves **6.2s = 71.4% of the scoring but 0% of the simulation = 14.1% of the run**.
Per panel the simulation dominates by 1.5x (U56) to 7.7x (SMALL439). **There is no compute case
for the deletion.**

## (5) Rule 8 walk-forward (dial chosen on 2009-2016, 2017-2026 read once)

The 2-rung chooser — IS Sharpe read only at the pair's two rungs, linearly interpolated to
10 bps — picks the **same arm as the true 10-bps chooser in 33 of 33 cells, for all 5 pairs**;
mean/min/max OOS Sharpe difference **0.0000 / 0.0000 / 0.0000**.

OOS at 10 bps, means over the 33 cells:

| | OOS Sharpe | OOS CAGR | OOS MaxDD |
|---|---|---|---|
| true 10-bps chooser | 0.7836 | 13.00% | -31.60% |
| 2-rung chooser | **0.7836** | **13.00%** | **-31.60%** |
| do-nothing (dial default) | 0.7887 | 11.97% | -29.06% |
| RULES v2 (live baseline) | **0.9905** | 7.12% | -12.99% |
| RULES v1 (continuity) | 0.6052 | — | — |
| SPY | 0.8820 | 15.45% | -33.72% |

By panel (0-30): true/2-rung OOS Sharpe **U56 1.0788, B136 0.8416, SMALL439 0.4304** vs SPY
0.8820 and RULES v2 1.2851 / 1.1185 / 0.5680. The chooser loses to SPY on 2 of 3 panels and to
RULES v2 on all 3 — the 15th-odd reproduction of the record's standing result, and the reason
this idea produces no candidate.

## (6) Both KEEP paths on all 1,792 grid points

**4a: 0/1,792** against the live RULES v2 (245/1,792 against the retired v1). **4b: 49/1,792**
(12 at 0 bps, 10 at 5, **8 at 10**, 8 at 15, 5 at 20, 3 at 25, 3 at 30). The 8 passers at
PROTOCOL's rung are all U56 and all already-published shapes — TOPN N=40 (12.95%, 1.1236,
-18.38%, OOS 1.2656), V1C N=40 (12.68%, 1.1242, OOS 1.2491), EWALL G=0.01/0.02/**0.03**
(15.05%, **1.1348**, H1 1.1131 / H2 1.1576, -19.95%, **OOS 1.2314**, 6.41 turns/yr), EWALL
V=0.40, EWALL K=2, TOPN V=0.30. Nothing new; no memo.

## What this licenses

A ladder may be published at its two **endpoint** rungs when what is being claimed is a
re-rank verdict, a Sharpe level (to 0.002) or a rule-8 pick. It may **not** be published at two
rungs when the claim is a 4b failing bar, and the endpoints must be the *outer* rungs — an
interior pair loses the verdict on up to 6 of 33 cells. Offered to Sunday review as a reporting
clause only; no RULES change.

## Caveats

SURVIVORSHIP: B136 and SMALL439 are current constituents of their screens only
(data/SMALL_PANEL_README.md, idea 54) — the bias runs in favour of every long book quoted here.
SMALL439 = the sub-$2B panel with the 44 tickers whose `max_1d_move >= 1.0` dropped per
data/small_meta.csv. The corpus is the record's *cost* ladders; ladders over other dials were
not re-costed. The 33 cells are not independent — three books share one eligible set.

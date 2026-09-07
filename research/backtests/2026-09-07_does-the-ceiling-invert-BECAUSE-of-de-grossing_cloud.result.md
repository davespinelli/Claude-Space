# Idea 354 — does-the-ceiling-invert-BECAUSE-of-de-grossing (cloud, 2026-09-07)

**Verdict: KILL.** Gross is not the confounder. The inversion is real and reproduces on a
de-duplicated census, but it is a *file*-level Simpson reversal, not a gross-level one — and
gross's own associations point the *wrong way* to have produced it.

Script: `2026-09-07_does-the-ceiling-invert-BECAUSE-of-de-grossing_cloud.py`
Tuned parameters: 2 — gross split point `G*` (9 values) and cost rung `c` (4 values). All 36
combinations reported.

---

## 0. A census defect found and fixed first

Idea 352's census pooled 183,829 rows from `research/backtests/*.csv`. Re-globbing that
directory today re-ingests **31 prior census dumps** — including idea 352's own 183,828-row
`.census.csv`, whose header (`turnover`, `pass4b`) parses as a record row. Pooling a census
dump double-counts every row it already pooled and lets one script outvote the whole record.

With dumps excluded: **137 CSVs, 70,411 rows** (26,950 of them, 38.3%, carry a gross column;
22,615 nominal / 4,335 realised). Idea 352's headline survives de-duplication:
10-bps median turnover **9.16x/yr for 4b passes vs 5.57x for fails, delta +3.59** (their
9.11 vs 4.95, +4.16). The inversion is not an artefact of the double-count.

## 1. S1/S2 — gross cannot be the confounder, by sign

A Simpson explanation needs gross associated with *both* passing and turnover, in directions
that manufacture the pooled inversion. At 10 bps (n=6,893 rows carrying gross):

| | low gross (<0.90) | high gross (≥0.90) | gap |
|---|---|---|---|
| 4b pass rate | 0.2713 | 0.1582 | **+0.1131** |
| median turnover x/yr | 7.95 | 10.95 | **−3.01** |

spearman(gross, 4b) −0.052; spearman(gross, turnover) **+0.238**.

Low-gross books pass **more** *and* trade **less**. That is exactly the configuration that
makes a turnover ceiling *work*; it predicts a **negative** pooled delta. Gross as a
confounder gets the sign of the anomaly backwards.

## 2. S3 — there is nothing left to explain inside the gross subsample

| slice (10 bps) | n | rate | med pass | med fail | delta | inverted |
|---|---|---|---|---|---|---|
| ALL rows | 26,915 | 0.167 | 9.16 | 5.57 | **+3.59** | **yes** |
| rows WITH gross, pooled | 6,893 | 0.249 | 8.27 | 9.33 | −1.06 | no |
| gross < 0.90 | 5,515 | 0.271 | 7.95 | 7.96 | −0.02 | no |
| gross ≥ 0.90 | 1,378 | 0.158 | 10.86 | 11.18 | −0.32 | no |

The inversion is **already gone before any split is applied**. The queue's specific claim —
"the inversion is entirely the low-gross stratum" — is falsified twice over: the low-gross
stratum is the one slice with delta ≈ 0 (−0.02), and the *high*-gross stratum is not inverted
either. Across the full 9-point `G*` sweep at 10 bps, only 2 of 18 strata invert at all
(G*=0.75 low, +0.27; G*=0.95 low, +0.02), both trivially. At 25 bps nothing inverts anywhere
(pooled −1.49). At 0 bps the low stratum *does* invert (+3.74, n=1,338) — the one point that
matches the hypothesis, and it is the rung the PROTOCOL does not trade at.

## 3. What the confounder actually is: the file

A committed CSV is one script's own grid — one panel family, one turnover scale, one 4b base
rate (observed range 0.031–0.667) and one row count (22–6,670). Pooling those is the textbook
setting for a reversal.

| rung | pooled delta | files inverted | mean within-file delta | median | n-weighted |
|---|---|---|---|---|---|
| 0 bps | +0.25 (inverted) | 10/24 | −0.38 | −0.50 | +0.02 |
| **10 bps** | **+3.59 (inverted)** | **18/69** | **−1.60** | **−1.63** | **−0.19** |
| 25 bps | −1.49 | 16/37 | −1.32 | −0.76 | −1.10 |

The pooled sign flips inside strata; only ~26% of files carry it individually. Three files
supply it: a 6,670-row grid at 6.7% base rate (delta +2.71) and a 2,185-row grid at 7.8%
(+3.68) **committed twice under two filenames** (`.keep.csv` and `.arms.csv` are identical) —
so one script contributes 4,370 of the pool's rows. Low-base-rate, high-turnover grids pooled
against high-base-rate, low-turnover ones produce the inversion without any book-level
mechanism.

## 4. The constructed control (180 books, gross MEASURED not parsed)

3 panels × 5 shapes (TOP5/10/20/40 + EWALL) × 3 nominal gross × {gated, ungated} × {W, M}.
Cost-identity gate `max|direct − (r₀ − τc/10⁴)| ≈ 1e-17` on all three panels.

Delta at 10 bps: **pooled −3.34**, low(<0.90) −4.08, high(≥0.90) −1.56. Holding *nominal*
gross and the gate fixed, every readable cell is negative (−5.4 to −7.3). **The inversion
never appears on a grid that was constructed rather than pooled** — at any rung, any stratum,
any control. It is a property of how the record was assembled, not of books.

## 5. Both KEEP paths

| rung | 4a (vs RULES v2) | 4b (vs SPY) |
|---|---|---|
| 0 bps | **0/180** | 30/180 (U56 24, B136 6, SMALL 0) |
| 10 bps | **0/180** | 17/180 (U56 14, B136 3, SMALL 0) |
| 25 bps | **0/180** | 5/180 (U56 5) |

First failing 4b bar at 10 bps: low-gross books die on `H1` 48 / `CAGR` 37; high-gross on
`H1` 24 / `DD` 20 — the two strata fail for *different* reasons, which is the one real thing
gross does here. All 4b passes sit at nominal gross 0.75 (11) or 1.00 (6); **g=0.50 passes
0/60 at every rung** (CAGR floor). 14 of 17 are monthly.

**Independent reproduction of idea 352's PARK:** U56 TOP40 g0.75 raw monthly clears 4b at
both 10 and 25 bps (CAGR 12.04%, Sharpe 1.140/1.088, MaxDD −18.00%, halves 1.142/1.143,
OOS 1.219, 3.67x/yr turnover). U56 EWALL g0.75 raw M is marginally better on Sharpe (1.143,
MaxDD −17.01%). Not proposed as a KEEP: it is an argmax of a 180-point grid on the panel the
record has mined hardest, 4a is 0/180, and it is already in the record as a PARK.

## 6. Rule 8 walk-forward (G* and T* chosen on ≤2016 only; OOS 2017– read once)

| panel | rung | menu | n | G* | T* | pick | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|---|---|---|
| U56 | 10 | unscreened | 60 | — | — | TOP20 g1.00 raw M | 16.38% | 1.0778 | −23.64% |
| U56 | 10 | ceiling only | 10 | — | 4.0 | TOP20 g0.50 raw M | 8.16% | 1.0781 | −12.45% |
| U56 | 10 | **gross-strat + ceiling** | 10 | 0.80 | 4.0 | TOP20 g0.50 raw M | 8.16% | **1.0781** | −12.45% |
| U56 | 10 | RULES v2 (live) | — | — | — | — | 9.53% | **1.2851** | −12.05% |
| U56 | 10 | SPY | — | — | — | — | **15.45%** | 0.8820 | −33.72% |
| B136 | 10 | unscreened | 60 | — | — | TOP40 g1.00 gate M | 14.79% | 0.9662 | −29.50% |
| B136 | 10 | ceiling only | 6 | — | 4.0 | TOP40 g0.50 gate M | 7.39% | 0.9656 | −15.52% |
| B136 | 10 | **gross-strat + ceiling** | 5 | 0.75 | 4.0 | TOP40 g0.50 gate M | 7.39% | **0.9656** | −15.52% |
| B136 | 10 | RULES v2 (live) | — | — | — | — | 7.98% | 1.1185 | −12.24% |
| SMALL439 | 10 | all three menus | 60 | — | — | TOP10 g1.00 gate M | 6.93% | 0.4482 | −42.27% |

**The gross split buys nothing out of sample.** It picks the identical book to the plain
turnover ceiling in 6/6 panel × rung cells (OOS Sharpe equal to 4 dp); on SMALL439 no (G*, T*)
pair is even admissible and the screen degenerates to the full menu. The ceiling itself
reproduces idea 352 exactly: it changes the *pick*'s OOS Sharpe by +0.0003 while raising the
admitted menu's mean OOS Sharpe (U56 1.045→1.198, B136 0.818→1.044) — it improves the average
candidate and not the chosen one. No arm beats RULES v2's OOS Sharpe, and none beats SPY's
OOS CAGR, on any panel or rung.

## 7. What this means for the queue

- Idea 352's inversion should be **retired as a book-level fact**. It is a pooling artefact of
  heterogeneous committed grids plus at least one duplicated file. Any future census of the
  record must (a) exclude prior `.census.csv` dumps and (b) report the within-file statistic
  beside the pooled one; the two disagree in sign at the trading rung.
- Gross is not a confounder of turnover-vs-4b, but it **is** a selector of *which bar kills a
  book* (H1/CAGR when de-grossed, H1/DD when not), and nominal g=0.50 is uniformly fatal.

**SURVIVORSHIP:** the SMALL panel is current constituents of a sub-$2B screen only
(`data/SMALL_PANEL_README.md`); 44 of 483 tickers with `max_1d_move ≥ 1.0` dropped first.
Every SMALL439 number above is an upper bound on what was tradeable — it contributes 0 of 180
4b passes at every rung, so it changes no conclusion here.

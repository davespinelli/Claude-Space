# Idea 453 — does-the-MATCHED-margin-hold-off-the-Sharpe-statistic (cloud, 2026-09-08)

**Verdict: SPLIT — the question is ANSWERED and the queue's premise is CONFIRMED. The MATCHED
identity holds on every statistic the record sweeps EXCEPT MaxDD, where it breaks at 48 of
6,084 cells (0.79%), and the breakage is quantitatively predicted by the statistic's own
curvature in the cost rung. No rules change; this is a reporting clause, not a book.**

Script: `2026-09-08_does-the-MATCHED-margin-hold-off-the-Sharpe-statistic_cloud.py`
Console: `..._cloud.console.txt` · Data: `.census.csv` `.breakage.csv` `.affinity.csv`
`.grid.csv` `.walkforward.csv` `.keep.csv`

Two tuned parameters, both fully reported: **p1 = statistic** {Sharpe, CAGR, MaxDD, OOS_Sharpe,
M4B}, **p2 = detection rule** {STRICT, LOOSE}. The MATCHED margin itself is parameter-free —
its sign is the prediction, there is no threshold to pick.

## 1. Reproduction gate

The scanner re-derives idea 231's arithmetic before any new number is read. Joining cell-for-cell
against idea 231's own committed census: **6,090 matched cells, max |gap diff| 9.9e-17, max
|tilt diff| 9.9e-17, max |matched-margin diff| 8.9e-16, actual re-rank agrees 6,090 / 6,090.**

Corpus caveat, stated plainly: this scanner detects **6,102** Sharpe/STRICT cells where idea 231
committed 8,529. The arithmetic is identical (above); the difference is the row filter — idea 231
drops rows with a non-numeric Sharpe *before* dial detection, which changes each id column's
cardinality and therefore which columns qualify as dials. This run's corpus is a strictly
verified subset (6,090 of 6,102 join exactly; 12 are cells idea 231 did not detect). The
per-statistic comparison below is internally matched — all five statistics are read off the
**same** detected rectangles — so the cross-statistic contrast is unaffected by the corpus size.

## 2. The answer — where the identity breaks (archive, 1,829 CSVs scanned)

MATCHED as an argmax reader, `pred = matched > 0` vs `actual = the argmax moves at any rung`:

| p1 statistic | p2 | cells | files | re-rank rate | TP | FP | FN | TN | errors | accuracy | endpoint-blind re-ranks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Sharpe | STRICT | 6,102 | 78 | 0.201 | 1,222 | 1 | 2 | 4,877 | **3** | 0.9995 | 0 |
| CAGR | STRICT | 6,123 | 78 | 0.076 | 465 | 0 | 0 | 5,658 | **0** | 1.0000 | 0 |
| MaxDD | STRICT | 6,084 | 76 | 0.122 | 717 | 22 | 26 | 5,319 | **48** | 0.9921 | 11 |
| OOS_Sharpe | STRICT | 7,169 | 83 | 0.153 | 1,096 | 0 | 3 | 6,070 | **3** | 0.9996 | 0 |
| M4B | STRICT | 5,126 | 16 | 0.098 | 501 | 1 | 2 | 4,622 | **3** | 0.9994 | 2 |
| Sharpe | LOOSE | 6,313 | 83 | 0.203 | 1,282 | 1 | 2 | 5,028 | 3 | 0.9995 | 0 |
| CAGR | LOOSE | 6,334 | 83 | 0.084 | 532 | 0 | 1 | 5,801 | 1 | 0.9998 | 1 |
| MaxDD | LOOSE | 6,295 | 81 | 0.131 | 798 | 23 | 28 | 5,446 | **51** | 0.9919 | 13 |
| OOS_Sharpe | LOOSE | 8,462 | 92 | 0.143 | 1,203 | 0 | 4 | 7,255 | 4 | 0.9995 | 1 |
| M4B | LOOSE | 5,574 | 17 | 0.103 | 569 | 3 | 5 | 4,997 | 8 | 0.9986 | 3 |

* **Sharpe, CAGR, OOS_Sharpe and the 4b margins: the identity survives.** Every one of the 3
  Sharpe errors is a machine-epsilon tie — `gap = 0.000e+00`, `tilt ≈ 4.4e-16`,
  `matched ≈ 1e-18`, interior residual `0.000e+00` — i.e. cells where all arms are bit-identical
  and "the argmax" is a float coin flip. **Outside ties the Sharpe error count is 0**, exactly as
  idea 231 published. CAGR is *cleaner* than Sharpe (0 errors of 6,123): it is not affine in the
  rung, but over 0–30 bps the compounding curvature is far too small to flip an argmax.
* **MaxDD is the break.** 48 errors (STRICT) / 51 (LOOSE), **16x every other family's rate**, and
  they are not ties: mean interior residual on error cells `3.05e-03` vs `1.50e-03` on the rest.
  They are also not one bad file — 8 files contribute; dropping the heaviest
  (`a-turnover-matched-null-for-suppressing-overlays_B.keep.csv`, 25) still leaves
  **23 errors in 5,178 cells (0.44%), ~9x Sharpe's tie-inclusive rate and infinitely more than
  its genuine rate of zero.**
* The breakage is **two-sided**: 22 FP (fires, nothing moves) and 26 FN (silent, the argmax
  moved anyway). 11 of the misses are re-ranks the two endpoint rungs cannot see at all — an
  interior rung wins and neither `c_lo` nor `c_hi` ever knows. MATCHED is built from the two
  endpoints, so those are structurally unreachable, not a tuning failure.

## 3. Why — the curvature, measured on live books (Part B)

For each of 96 live `(panel, dial, value)` books, the maximum deviation of an interior rung from
that book's own two-endpoint line, absolute and relative to the endpoint span:

| statistic | mean abs | max abs | mean / span | max / span |
|---|---|---|---|---|
| Sharpe | 1.51e-04 | 1.44e-03 | 6.11e-04 | 2.12e-03 |
| CAGR | 4.95e-04 | 2.39e-03 | 6.69e-03 | 1.74e-02 |
| OOS_Sharpe | 1.56e-04 | 2.11e-03 | 5.94e-04 | 2.77e-03 |
| M4B (`m4b_CAGR`) | 4.95e-04 | 2.39e-03 | 6.69e-03 | 1.74e-02 |
| **MaxDD** | **5.35e-03** | **5.17e-02** | **1.40e-01** | **3.50e+00** |

Sharpe's curvature is 6e-4 of its own span — the affine model is right to four digits, so the
identity is arithmetic. CAGR carries 10x that and still never flips a published argmax. **MaxDD
carries 230x Sharpe's relative curvature and a maximum of 3.5 spans**, because it is not merely
non-affine but non-smooth: raising the cost rung can move *which drawdown episode* is the
deepest, and the statistic then jumps rather than bends. That is the mechanism, and the ordering
of the residual column reproduces the ordering of the error column exactly.

Cost identity `|engine@10bps − (gross − turn·c/1e4)|`: U56 6.9e-18, B136 6.9e-18, SMALL439 1.4e-17.

## 4. Live cells and PROTOCOL rule 8 (2009–2016 chooses, 2017–2026 read once)

12 live `(panel, dial)` cells per statistic, full sample: **0 MATCHED errors on all five** — 12
cells is far too small to catch a 0.8% break rate, and this is reported as a null result, not as
support. On the IS window the MaxDD gate does break: **MaxDD TP 5 / FP 0 / FN 1 / TN 6 (1 error
of 12), Sharpe and CAGR 0 of 12**, with mean IS interior residual 8.8e-03 (MaxDD) against
2.5e-04 (Sharpe) and 7.4e-04 (CAGR).

OOS means over 84 `(panel × dial × rung)` cells, by which statistic does the IS choosing:

| IS selector | rung-aware OOS Sharpe / CAGR / MaxDD | naive 0-bps | do-nothing | random | oracle |
|---|---|---|---|---|---|
| Sharpe | **+0.8243** / 16.27% / −32.83% | +0.7855 / 15.61% | +0.7998 / 13.81% | +0.7685 | +0.8861 |
| CAGR | +0.7992 / 16.40% / −34.96% | +0.8046 / 16.54% | +0.7998 / 13.81% | +0.7685 | +0.8861 |
| MaxDD | +0.7005 / 10.92% / −29.48% | +0.6937 / 10.68% | +0.7998 / 13.81% | +0.7685 | +0.8861 |

Headline at PROTOCOL's own 10 bps (12 cells, Sharpe selector): rung-aware OOS Sharpe **0.8656**,
CAGR 17.58%, MaxDD −32.50%; naive 0.8312 / 16.67% / −31.47%; do-nothing 0.8500 / 14.92% /
−28.85%. Benchmarks OOS: **SPY 0.8820 (CAGR 15.45%, MaxDD −33.72%)**; RULES v1 0.7471 (U56) /
0.5763 (B136) / 0.4923 (SMALL439); RULES v2 1.2851 / 1.1185 / 0.5680. **Selecting on MaxDD is the
worst of the three selectors and loses to do-nothing by −0.0993 OOS Sharpe and −2.9 pp CAGR** —
the statistic whose identity breaks is also the statistic you should not select on.

## 5. Both KEEP paths, all 665 Part B grid points

**4a 80 / 665** (U56 0/217, B136 44/224, SMALL439 36/224) · **4b 12 / 665, all on U56**
(B136 0/224, SMALL439 0/224). 4b failing bars: DD 639, H2 404, OOS 378, H1 312, CAGR 198. The 12
passes are the already-PARKed `U56 N=40` arm (all 7 rungs) plus `U56 V=0.30` at 0–20 bps — e.g.
N=40 at 10 bps: CAGR 12.9%, Sharpe 1.124 (H1 1.073 / H2 1.172), MaxDD −18.4%, OOS Sharpe 1.266,
OOS CAGR 15.2%, against SPY full 0.889 / 15.23% / −33.72%. **Nothing new clears; no KEEP is
claimed by this idea.** Best full-sample Sharpe at 10 bps per panel: U56 `V=5.0` 1.147 (4a fails
DD, 4b fails DD), B136 `K=4` 1.057 (DD / DD), SMALL439 `V=5.0` 0.749 (DD / H1,H2,OOS,DD).

SURVIVORSHIP: SMALL439 is current constituents of a sub-$2B screen with the 44 `max_1d_move ≥ 1.0`
tickers dropped from 483; its numbers are upper bounds and no verdict here rests on them.

## 6. What to do with it

Offered to Sunday review as a **one-line PROTOCOL reporting clause, not a rules change**: *the
endpoint-pair reading of a cost ladder (gap / tilt / MATCHED margin) may be published in place of
the full ladder for Sharpe, CAGR and OOS-Sharpe columns, but **never for MaxDD or a MaxDD-bearing
4b margin**, where it is wrong in ~0.8% of cells in both directions and blind to interior-rung
re-ranks entirely.* Idea 454 ("are-the-record's-7-rung-ladders-two-rung-ladders") should be read
under this restriction: the deletion it prices is safe on three of the record's statistics and
unsafe on the fourth.

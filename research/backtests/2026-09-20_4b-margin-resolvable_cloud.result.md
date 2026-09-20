# Idea 2042 (lane cloud, 2026-09-20) — is the standing KEEP-4b margin resolvable, or is it a point estimate?

**Verdict: ANSWERED / HALF. The four RETURN-AND-SHARPE legs of rule 4b are real — 88 of 187 point-passing cells resolve all four at 95% (126 at 90%). The DRAWDOWN-CAP leg resolves at 0 of 187 at every block length and every confidence level, and a block bootstrap cannot honestly certify it anyway. No cell, and no rule-8-reached cell, clears all five legs with a confidence interval. PARK the bare "4b pass" wording; nothing is killed and nothing new is kept.**

Script `2026-09-20_4b-margin-resolvable_cloud.py`; gates **10/10**, including G5 (reproduces the standing KEEP-4b cell to 1.0e-05) and G7 (the bootstrap is genuinely paired: the shared SPY leg cancels exactly, 1.5e-14, in a cell-vs-cell difference).

## 1. What was measured

The book family is idea 1799's, inherited unchanged and never re-tuned: equal-weight panel at `gross_t = min(1, t / sigma20_t)`, refreshed on a calendar (`R in {D,W,M,Q}`) or on a drift threshold (`|g_t - gross_held_t| > h`), traded weekly or monthly, decided at close t and applied at t+1, 10 bps. 420 cells; both KEEP paths scored at 0/10/25/50 bps.

Rule 4b is five inequalities against SPY. Each gets a **paired moving-block bootstrap** in which the BOOK and SPY are resampled on the **same** day blocks, so the common market factor is differenced out. Segments are resampled independently — FULL (for L4/L5), H1, H2, OOS — so "first half" keeps meaning the first half of the sample. The two tuned dials are BLOCK LENGTH {21, 63} and CONFIDENCE {90, 95, 99}%; neither ever selects a book. B = 500 (2,000 for the deep read), seed 20260924.

## 2. The headline count, and why it is not the whole story

At every one of the six (block, confidence) settings: **187 of 420 cells pass 4b FULL on point estimates; 0 resolve on all five legs.** 4b FULL+OOS is likewise 187 -> 0. The count is carried by one leg, and that leg is a path statistic, so the run decomposes it rather than reporting "0 of 187" as a clean fact.

## 3. Which leg fails (block 21, 95%, over the 187 point-passing cells)

| leg | CI covers 0 | mean point | mean SE | mean t |
|---|---|---|---|---|
| L1_H1 (H1 Sharpe vs SPY) | 45/187 | +0.3257 | 0.1320 | +2.56 |
| L2_H2 (H2 Sharpe vs SPY) | 49/187 | +0.3374 | 0.1435 | +2.38 |
| L3_OOS (OOS Sharpe vs SPY) | **1/187** | +0.4018 | 0.1433 | +2.83 |
| **L4_DD (MaxDD vs 0.60x SPY)** | **187/187** | +0.0416 | 0.0353 | **+1.14** |
| L5_CAGR (CAGR vs 0.70x SPY) | 65/187 | +0.0358 | 0.0132 | +2.85 |

The Sharpe and CAGR legs carry real margin. **The drawdown cap never does** — mean t 1.14, CI covering zero at every single cell.

## 4. The four non-path legs alone

| block | conf | 4b FULL passes resolving all 4 non-path legs | 4b OOS resolving its 2 non-path legs |
|---|---|---|---|
| 21 | 90% | **126/187 (67.4%)** | 122/225 (54.2%) |
| 21 | 95% | **88/187 (47.1%)** | 114/225 (50.7%) |
| 21 | 99% | 3/187 (1.6%) | 69/225 (30.7%) |
| 63 | 90% | 118/187 (63.1%) | 119/225 (52.9%) |
| 63 | 95% | 100/187 (53.5%) | 108/225 (48.0%) |
| 63 | 99% | 65/187 (34.8%) | 72/225 (32.0%) |

**Caveat stated, not buried:** at B = 500 a 99% two-sided CI is set by the ~2.5th draw in each tail, which is why block 21 gives 3 and block 63 gives 65 at that level — the 99% row is bootstrap noise, not a finding. The 90% and 95% rows are stable across both block lengths (63-67% and 47-54%). **The headline reading is 88 of 187 at block 21 / 95%.**

## 5. Why the DD leg cannot be certified this way — measured, not asserted

A moving-block resample breaks the serial dependence that produces long drawdowns, so it is a biased estimator for MaxDD. The run measures the bias directly, as the gap between each leg's CI midpoint and its point estimate:

| leg | mean point | mean CI-mid | shift | as % of the point margin |
|---|---|---|---|---|
| L1_H1 | +0.3257 | +0.3159 | -0.0097 | -3.0% |
| L2_H2 | +0.3374 | +0.3280 | -0.0095 | -2.8% |
| L3_OOS | +0.4018 | +0.3934 | -0.0084 | -2.1% |
| **L4_DD** | +0.0416 | +0.0080 | **-0.0336** | **-80.8%** |
| L5_CAGR | +0.0358 | +0.0352 | -0.0006 | -1.7% |

Gate **G9 PASS**: the bias is 27x the largest shift on any non-path leg. The four non-path legs' bootstrap distributions sit on their point estimates; the DD leg's does not. So the correct statement is **not** "the drawdown margin is zero" — it is "the drawdown cap is the one 4b clause that neither the data nor a resampling test can certify, and even taken at face value its mean t is 1.14."

## 6. Rule 8 and the reached cells

(t,h) or (t,R) chosen on 2009-2016 alone; 2017-2026 read exactly once. 48 legal IS-only picks at 10 bps; **10 clear 4b FULL+OOS on point estimates, 0 resolve at 95%.**

| panel / T | chooser | pick | OOS CAGR / Sharpe / MaxDD | weakest leg | t |
|---|---|---|---|---|---|
| B136/M | C_ISLEGS | R=M, t=0.10 | 13.05% / 1.2000 / -19.87% | L4_DD | +0.12 |
| B136/M | C_ISSHARPE | h=0.16, t=0.20 | 16.63% / 1.1957 / -19.42% | L4_DD | +0.24 |
| B136/M | C_ISCALMAR / C_ISLEGS | h=0.25, t=0.16 | 14.06% / 1.1944 / -17.85% | L4_DD | +0.84 |
| B136/W | C_ISSHARPE / C_ISCALMAR / C_ISLEGS | h=0.25, t=0.16 | 14.08% / 1.1888 / -17.93% | L4_DD | +0.81 |
| U56/M | C_ISDD | R=M, t=0.08 | 11.87% / 1.2780 / -16.13% | L5_CAGR | +0.47 |
| **U56/M** | **C_ISSHARPE** | **h=0.12, t=0.16** | **16.36% / 1.2810 / -18.16%** | **L4_DD** | **+0.66** |
| U56/W | C_ISDD | R=M, t=0.08 | 11.74% / 1.2561 / -16.28% | L5_CAGR | +0.42 |

**Eight of the ten are blocked by the DD cap, two by the CAGR floor.** SMALL665 reaches nothing (0 of 140 cells pass 4b on points). Path 4a: 5 of 48 reached picks, 40 of 420 grid cells at 10 bps — also point-estimate-only.

## 7. The standing KEEP-4b cell, deep read (B = 2,000, block 21)

U56, T=M, `t=0.16, h=0.12` — FULL 15.62% / 1.2451 / -18.16% (H1/H2 1.29/1.20), OOS 16.36% / 1.2810 / -18.16%, vs SPY 15.12% / 0.8843 / -33.72% (OOS 15.26% / 0.8737 / -33.72%) and live RULES v2 8.62% / 1.2010 / -12.05% (OOS 9.46% / 1.2766 / -12.05%).

| leg | point | SE | t | P(>0) | 95% CI |
|---|---|---|---|---|---|
| L1_H1 | +0.3374 | 0.1293 | **+2.61** | 0.996 | [+0.076, +0.573] |
| L2_H2 | +0.3787 | 0.1244 | **+3.04** | 1.000 | [+0.134, +0.631] |
| L3_OOS | +0.4073 | 0.1211 | **+3.36** | 1.000 | [+0.164, +0.635] |
| L4_DD | +0.0207 | 0.0324 | +0.64 | **0.352** | [-0.072, +0.054] |
| L5_CAGR | +0.0503 | 0.0117 | **+4.29** | 1.000 | [+0.026, +0.073] |
| O2_DD (OOS) | +0.0207 | 0.0317 | +0.65 | 0.366 | [-0.064, +0.058] |
| O3_CAGR (OOS) | +0.0568 | 0.0164 | **+3.46** | 0.999 | [+0.024, +0.089] |

**The candidate's return and Sharpe advantage over SPY is strongly resolvable (t = +2.6 to +4.3 on four legs). Its claim to beat 60% of SPY's drawdown is not** — t = +0.64, and under the block bootstrap the margin is negative more often than positive, which is the path-statistic bias of section 5 rather than evidence that the book is riskier than it looks.

## 8. What this means, and what it does not

- The candidate is **not killed**: a 4b pass on the realised tape is still a 4b pass, and four of its five legs survive a paired SE with room to spare.
- The candidate is **not upgraded**: it cannot be described as "clears 4b" without saying that one of the five clauses is uncertifiable at t = 1.14.
- The general lesson, bigger than this book: **rule 4b's DD cap is the binding clause at 49 of 420 cells on points, and the unresolvable clause at 187 of 187 passes.** Every capital verdict the record has issued turns partly on a number that has never carried a standard error and cannot be given an honest one by resampling. A path-aware test (stationary bootstrap with a fitted dependence length, or a parametric drawdown model) is the missing tool.
- **Proposed PROTOCOL clause, drafted here and NOT applied** (rule 6: rules change only at Sunday review): *any published 4b pass must quote the paired-bootstrap t of its narrowest leg beside the verdict, and a pass whose narrowest leg is the DD cap must be labelled "4b (DD leg uncertified)".*

## Census (all 420 cells published in `.grid.csv.gz`)

| cost | 4b FULL | 4b OOS | 4b FULL+OOS (CAL / DRIFT) | 4a | 4a OOS |
|---|---|---|---|---|---|
| 0 bps | 217 | 230 | 217 (41 / 176) | 41 | 55 |
| 10 bps | 187 | 225 | 187 (35 / 152) | 40 | 54 |
| 25 bps | 166 | 186 | 165 (32 / 133) | 26 | 44 |
| 50 bps | 128 | 153 | 128 (21 / 107) | 6 | 28 |

## Survivorship

U56 / B136 are CURRENT-constituent lists; SMALL665 is a CURRENT sub-$2B screen with 54 tickers (`max_1d_move >= 1.0`) dropped first. Levels are optimistic and both 4b bars are easier here than on a point-in-time panel. **A bootstrap resamples the tape it is given; it cannot put a confidence interval on survivorship**, so even a resolvable margin here is a margin measured on a favourable panel. SMALL numbers are not comparable with pre-2026-09-20 SMALL results (cache grew 439 -> 665 names).

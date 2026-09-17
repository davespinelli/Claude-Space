# Idea 1218 (lane B, 2026-09-17) — what IS the right null for a ladder if rung dispersion is half a rung's own sampling SE

**ANSWERED = THE CORRECTION IS ARITHMETICALLY RIGHT AND PRACTICALLY USELESS. `d2_corr(k, rho) =
d2(k) * sqrt(1-rho)` reproduces the realised range on every ladder whose rho is known (pooled
mean R_corr **0.9858**, z **-0.21**, on 18 synthetic rungs; **0.9333**, z -0.98, on 18 real
independent-null rungs), and it does turn 1205's unreachable bar into a reachable one — R >= 1
clears at **0 of 12** real ladders, R_corr >= 1 at **5 of 12**. But the same division destroys
exactly what the statistic was detecting: separation of the degenerate dial (GROSS) from the
live ones collapses from **AUC 1.0000** under the raw R to **0.5185** under R_corr, because
GROSS's degeneracy IS its correlation (rho_S 0.99996), and at k <= 9 a single ladder's R_corr
carries a null SD of 0.27-0.52, so **0 of 12** real ladders differ from the corrected null at
|z| > 1.96.** Verdict **KILL (capital)**: no new book, no RULES change, no PROTOCOL edit.

## The two dials and no more (rule 4, and the queue names both)

`CORR DRIVER` {D_N, D_POOL, D_SYNTH} x `PANEL` {U56, B136, SMALL} = **9 cells, every one
published** in `.dialgrid.csv`; all 54 driver rungs x 2 SD bases x 2 k values (216 rows) are in
`.corrladder.csv` regardless of what any cell did with them. NOT dials, reported at every value:
the rung ladders (N {2,3,5,10,20,40}; q {0.02,...,1.00}; imposed rho {0.00,...,0.95}); k {4, 8};
SD BASIS {S_IID, S_BLOCK(63)}; the record's four committed ladders {N, H, GROSS, CADENCE}; the
4a and 4b legs; the rule-8 walk-forward arm.

## The arithmetic, declared before any number

For k exchangeable draws with common sampling SD s and pairwise correlation rho, the common
factor cancels out of every difference, so `E[max - min] = sqrt(1-rho) * d2(k) * s`, i.e.
`R_corr = R / sqrt(1-rho)`. The rho that matters is **not** the daily-return correlation but the
cross-book correlation of the **Sharpe estimator**, measured by a PAIRED bootstrap (one resampled
day index applied to all k books at once). Both are published at every rung; they differ by at
most 0.03 in this run.

## Q1 — the ratio as a function of correlation

| driver | what moves | rho_S span (min -> max over 3 panels) | raw R | pooled R_corr |
|---|---|---|---|---|
| D_N | names per null book, 2 -> 40 | 0.33 -> 0.997 | 0.076 -> 0.903 | 0.9333 (z -0.98) |
| D_POOL | draw pool, top-2% -> all eligible | 0.835 -> 1.0000 | 0.000 -> 0.630 | 0.6704 (z -4.84); 1.2068 excluding the 8 rungs where the pool is smaller than N and all k books are literally the same book |
| D_SYNTH | rho imposed, 0.00 -> 0.95 | 0.005 -> 0.956 | 0.173 -> 1.333 | 0.9858 (z -0.21) |

R falls with rho_S at 6 of 6 real (driver, panel) cells (Spearman -0.60 to -1.00). **1205's
CTRL_LIVE re-measured**: rho_S 0.9582 / 0.9261 / 0.8350 on U56 / B136 / SMALL against the 0.8248
that its R = 0.4186 implies if correlation is the whole story — supported on all three panels at
the pre-registered 0.15 tolerance, and the reading it supports is that 1205's shortfall is
correlation, not a defect of d2.

## Q2 — can a real ladder clear the corrected bar? Yes, and that is the problem

| statistic | GROSS (degenerate by 1189) | live dials (N, H, CADENCE) | AUC |
|---|---|---|---|
| raw range | 0.0038 | 0.1428 | **1.0000** |
| R | 0.0055 | 0.2458 | **1.0000** |
| R_corr | 0.8334 | 0.8775 | **0.5185** |
| rho_S | 1.0000 | 0.9176 | 0.0000 |

The correction multiplies the raw R by 1/sqrt(1-rho_S): **x167.5 / x157.5 / x129.0** on the three
GROSS ladders against x2.7-x5.5 on the live dials. At rho_S = 0.999964 a rho error of **2.7e-05**
doubles R_corr, so the corrected statistic on a degenerate ladder is a ratio of two numbers that
are both ~0 and is dominated by the bootstrap's own error.

## The power fact (POST-HOC arm 1c, declared as post-hoc)

R is a ONE-DRAW range statistic, so its own null SD is d3(k)/d2(k): **0.75 (k=2), 0.52 (k=3),
0.43 (k=4), 0.29 (k=8), 0.27 (k=9)**. A single true-null R_corr at k=8 sits inside [0.434, 1.566]
95% of the time. That is why the pre-registered per-rung bar H_LAW (+-0.15) was REFUTED while
G_LAW passes at 3.4e-03 over 20,000 replications — the law is right, one rung cannot see it. On
the record's twelve committed ladders, **|z| > 1.96 at 0 of 12**: the corrected null rejects
nothing anyone has published.

## Pre-registered hypotheses (4 of 6 as declared)

| hypothesis | verdict | measured |
|---|---|---|
| H_LAW (per-rung +-0.15 on D_SYNTH) | **REFUTED** | worst \|R_corr - 1\| = 0.7007; refuted on POWER, not on the law (see arm 1c) |
| H_MONO (Spearman <= -0.8 on all 6 real cells) | **REFUTED** | -0.829 / -0.898 / **-0.600** / -1.000 / -0.886 / -0.943 — 5 of 6 |
| H_DRIVER (each driver moves rho_S >= 0.20 per panel) | **REFUTED** | D_N 0.528 / 0.502 / 0.582 PASS; D_POOL 0.042 / 0.074 / 0.165 FAIL — D_POOL is a degeneracy driver, not a correlation driver |
| H_1205 (rho_S ~ 0.825 on CTRL_LIVE) | SUPPORTED | 0.9582 / 0.9261 / 0.8350 |
| H_REAL (corrected bar clearable by >= 1 real ladder) | SUPPORTED | 5 of 12 (raw bar: 0 of 12) |
| H_USEFUL (bar separates, 1..11 of 12 above) | SUPPORTED | 5 of 12 above — but see the AUC table: it separates the wrong thing |

## Rule 8 (mandatory) and both KEEP paths

Parameters chosen on warm-up..2016-12-31 ONLY; 2017-2026 read once. Five move-or-stay rules x 12
(panel, ladder) decisions = 60 rule-8 rows in `.walkforward.csv`.

| rule | move rate | mean OOS Sharpe | mean OOS CAGR | mean OOS MaxDD | 4a | 4b full |
|---|---|---|---|---|---|---|
| C_STAY (do nothing) | 0.0000 | **0.8750** | 13.34% | -25.23% | 0/12 | 4/12 |
| C_ALWAYS (IS argmax) | 0.9167 | 0.8453 | 13.95% | -28.88% | 0/12 | 1/12 |
| C_RAW (IS R >= panel median) | 0.4167 | 0.8496 | 12.98% | -26.26% | 0/12 | 3/12 |
| C_CORR (IS R_corr >= 1) | 0.1667 | 0.8676 | 13.64% | -25.95% | 0/12 | 4/12 |
| C_CORRBAND (+ rho_S <= 0.99) | 0.0833 | 0.8675 | 13.20% | -25.44% | 0/12 | 4/12 |

Benchmarks, same windows: SPY OOS Sharpe 0.8684 / 0.8767 / 0.8767 (U56 / B136 / SMALL, OOS CAGR
15.15% / 15.33% / 15.33%, OOS MaxDD -33.72%); live RULES v2 OOS 1.2714 / 1.1059 / 0.5600 (OOS
CAGR 9.42% / 7.88% / 3.75%, MaxDD -12.05% / -12.24% / -13.89%); frozen anchor OOS 1.1615 /
1.0100 / 0.4533. Gating moves on the corrected bar recovers most of what always-moving loses
(0.8676 against 0.8453) and still **loses to doing nothing** (0.8750). Best rule-8 book anywhere
in the run: U56 GROSS -> g 1.00, full 20.79% / 1.1387 / -24.93% (halves 1.2054 / 1.0940), OOS
22.65% / 1.1623 / -24.93% — it fails 4b on the drawdown cap (-24.93% against SPY's -33.72% x 0.60
= -20.23%). **4a passes 0 of 60. 4b passes 16 of 60 rows, which collapse to 4 DISTINCT books
(rule 1211's lesson), and all four are the frozen U56 ANCHOR re-selected by a do-nothing rule on
four different ladders — no new book.** Neither R nor R_corr predicts what moving is worth:
Spearman(move value, IS_R) -0.27, (move value, IS_R_corr) +0.15 over 12 ladders, mean move value
-0.0296 Sharpe, positive at 5 of 12.

## Gates, all 9 pass, printed before any result

G_D2 d2(2) == 2/sqrt(pi) to 0; G_D2b d2(8) == 2.847 to 2.0e-04; G_D3 d3(2) == 0.8525 to 2e-03;
G_LAW E[range]/d2 == sqrt(1-rho) on equicorrelated normals to 3.4e-03 at the worst rho; G1 fast
runner == engine.backtest to 1.4e-17; G2 book() == that path to 2.8e-17; G3 determinism exactly
0; G4 two null books are not the same path (|corr| 0.954); G5 a paired bootstrap of a book
against itself reads rho_S == 1 exactly.

## What this run does not show

The correction assumes EXCHANGEABLE rungs (one common rho); a real ladder's pairwise correlations
are not equal, and only their mean is used, so R_corr on a real ladder is an approximation whose
error is not quantified here. rho_S is a bootstrap estimate and at rho -> 1 its error dominates
the corrected statistic, as the amplification table shows. Everything is one construction on one
tape, 12 real ladders and 54 driver rungs; the k ladder stops at 12. SURVIVORSHIP (rule 9): U56
and B136 are current-constituent lists and SMALL is the current output of a sub-$2B screen less
the documented max_1d_move >= 1.0 exclusion (52 of 715 dropped), so every CAGR and drawdown LEVEL
and every 4b count is an upper bound; R, R_corr and rho are ratios of one construction against
itself and the bias very largely cancels out of them.

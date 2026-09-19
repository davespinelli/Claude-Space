# Idea 1664 (lane cloud, 2026-09-19) — is the 27-of-27 MIXTURE CONVEXITY a DIVERSIFICATION fact or a SHARPE-ALGEBRA fact?

**VERDICT: BOTH, and the record should stop quoting the COUNT. The SIGN (27 of 27) is pure
Sharpe algebra — a random split of ONE panel, which crosses no panel at all, reproduces it in
99.9% of 3,240 null cells and in 120 of 120 draws. The MAGNITUDE (+0.0536) does separate from
the null (0 of 120 draw-means reach it) but it separates as a function of rho, not of
panel-crossing: corr(C, 1-rho) = +0.9528, and the cross-panel U56xB136 pair (rho 0.964) yields
LESS convexity (+0.0088) than a random split of U56 alone (rho 0.865, +0.0352). KILL stands for
the blend as a book: 0 of 9 blend cells clear 4a or 4b FULL, and reaching for one on IS rows
costs -0.107 of OOS Sharpe. No KEEP, no memo, no RULES change.**

Script: `2026-09-19_mixture-convexity-vs-within-panel-null_cloud.py`.
Outputs: `.console.txt .cells.csv .null.csv .keeppaths.csv .walkforward.csv`.

## Construction

Two dials and no more: **w (NAV share to the FIRST book) {0.25, 0.50, 0.75}** x **G (total
target gross) {0.50, 0.75, 1.00}**. Not dials, all published: PAIR {U56xSMALL, U56xB136,
B136xSMALL} x SLICE {FULL, IS, OOS} — 81 cross-panel cells, every one in `.cells.csv`.

Book at every cell: live RULES v2 band 0.03, equal weight at gross/N of priced names, gated-out
weight to 0%-yielding cash, weekly, t+1, 10 bps. Tape: U56/B136 2008-2026, SMALL 2010-2026,
warm-up 260 rows dropped, IS 2010-2016, OOS 2017-2026 read once.

The statistic is 1649's own: `C = Sharpe(blend) - [w*S_A + (1-w)*S_B]`.

## The algebra, asserted numerically rather than in prose

C decomposes **exactly** into two terms:

```
C   = MIX + DIV
MIX = (S_A - S_B) * w(1-w)(sigma_A - sigma_B) / (w*sigma_A + (1-w)*sigma_B)
DIV = (w*mu_A + (1-w)*mu_B) * (1/sigma_w - 1/sigma_lin),   sigma_lin = w*sigma_A + (1-w)*sigma_B
```

MIX is vol-mismatch re-weighting (zero iff the two books have equal vol; either sign). DIV is
variance sub-additivity — **non-negative for ANY rho < 1 whenever the blend's mean return is
positive**, which is to say for essentially every pair of long books ever built. Gate G1/G2:
`|C - MIX - DIV| <= 5.1e-16` at all 81 cross-panel cells and all 3,240 null cells.

## (A) Replication — exact

| pair | C > 0 | mean C | mean MIX | mean DIV | mean rho |
|---|---|---|---|---|---|
| **U56xSMALL** (1649's own) | **27 of 27** | **+0.0536** | +0.0037 (6.9%) | **+0.0500 (93.1%)** | 0.760 |
| B136xSMALL | 27 of 27 | +0.0450 | +0.0032 | +0.0419 | 0.785 |
| U56xB136 | 27 of 27 | +0.0088 | +0.0002 | +0.0087 | 0.964 |

1649 published **+0.0535**; this run reads **+0.0536** on the same 27-cell shape. **93.1% of it
is the sub-additivity term**, i.e. the part that is arithmetic.

Against the **better** corner — the only benchmark that would justify moving capital — the blend
wins 3 of 27 on U56xSMALL, 6 of 27 on U56xB136 and **0 of 27** on B136xSMALL, as 1649 found.

## (C) The null — random disjoint halves of ONE panel, same book, same w, same G

40 draws per panel, seed 20260919, 3 panels x 3 G x 3 w x 3 slices = **3,240 null cells**.

| null | mean rho | mean C | % of observed | P(cell >= +0.0536) | P(draw-mean >= +0.0536) |
|---|---|---|---|---|---|
| within-U56 | 0.865 | **+0.0352** | **65.6%** | 0.053 | 0.000 (0 of 40) |
| within-B136 | 0.944 | +0.0129 | 24.0% | 0.000 | 0.000 (0 of 40) |
| within-SMALL | 0.955 | +0.0067 | 12.4% | 0.000 | 0.000 (0 of 40) |
| pooled | — | +0.0182 | 34.0% | 0.018 | 0.000 (0 of 120) |

**The SIGN is algebra.** Null C > 0 in **99.9% of 3,240 cells** and in **120 of 120 draw-means
(100.0%)**. A count of "27 of 27" is therefore uninformative at any sample size: two random
halves of one panel — same names, same gate, same regime, no panel crossed — produce it just as
reliably. The record should never again quote a convexity COUNT as evidence.

**The MAGNITUDE does separate**, on the shape-matched read (each draw's own mean over its 27
cells, exactly the observed statistic's shape): **0 of 120 draws reach +0.0536**.

## But what it separates on is rho, not panel-crossing

Pooling all 1,107 even-split cells this run priced, cross-panel and within-panel together:

**corr(C, 1 - rho) = +0.9528.**

And the ordering is decisive against the "cross-panel" framing:

| pair | crosses a panel? | rho | mean C |
|---|---|---|---|
| within-U56 random halves | **no** | 0.865 | **+0.0352** |
| U56 x B136 | **yes** | 0.964 | **+0.0088** |

**A random split of one panel diversifies four times as much as two of the record's three panels
do.** "Cross-panel" is not the operative property; decorrelation is, and U56 and B136 share 55
of 56 names (idea 536), so they are barely two books at all.

## The capital arm — 15 cells on 1649's pair, every one published (`.keeppaths.csv`)

Benchmarks on the shared calendar: **SPY 14.01% / 0.8561 / -33.72%** (H1 0.9026, H2 0.8391);
**live RULES v2 8.14% / 1.1636 / -12.05%** (H1 1.0661, H2 1.2534).

**4a: 0 of 15. 4b FULL: 1 of 15. 4b OOS: 2 of 15. 4b FULL-and-OOS: 1 of 15** — and that one is
**w = 1.00, G = 1.00**, the pure U56 corner at full gross, i.e. **no blend at all** (already
committed by ideas 1498 / 1649, reported here, not proposed). **Of the 9 BLEND cells: 4a 0, 4b
FULL 0, 4b OOS 1.**

## Rule 8 — 2010-2016 only, 2017-2026 read ONCE

| chooser | pick | OOS CAGR / Sharpe / MaxDD | vs anchor |
|---|---|---|---|
| C_SHARPE (argmax IS Sharpe) | G=1.00, w=0.75 | 10.70% / 1.1694 / -14.71% | **-0.1072** |
| C_CALMAR (argmax IS Calmar) | G=1.00, w=0.75 | 10.70% / 1.1694 / -14.71% | **-0.1072** |
| C_CONVEX (argmax IS convexity C) | G=1.00, w=0.50 | 8.72% / 1.0014 / -13.51% | **-0.2752** |
| ANCHOR: U56 corner, G=0.75 (live RULES v2) | — | **9.46% / 1.2766 / -12.05%** | — |

SPY OOS 15.26% / 0.8737 / -33.72%. **0 of 3 choosers stay at the corner, and every one of them
is negative-value OOS.** Choosing the blend by its own convexity statistic is the worst of the
three, which is the practical form of this run's finding: C is not a selection criterion.

## Gates

| Gate | What | Result |
|---|---|---|
| G1 | `C == MIX + DIV` at all 81 cross-panel cells | max \|resid\| **5.100e-16** |
| G2 | same identity at all 3,240 null cells | **PASS** |
| G3 | the (U56, G=0.75) corner replays `baseline.rules_v2_weights` bit-for-bit | max \|d\| **< 1e-15** |
| G4 | `DIV >= 0` at every even-split cross-panel cell (sub-additivity) | **PASS** |
| G5 | 40 draws/panel, seed 20260919, deterministic | **PASS** |

## What the record should do

1. **Retire the convexity COUNT.** "Blend Sharpe above the NAV-weighted average of its corner
   Sharpes in k of k cells" is an algebraic near-certainty (99.9% under a null that crosses
   nothing) and must not be published as evidence of diversification again.
2. **If a convexity magnitude is quoted, quote its rho beside it** and price it against a
   within-panel split at the same rho. C is a decorrelation statistic; the panel label is noise.
3. **No RULES change.** 0 of 9 blend cells clear either KEEP path and every IS-only chooser that
   reaches for one loses OOS Sharpe against doing nothing.

## Survivorship (rule 9)

U56 and B136 are current-constituent lists; SMALL is a current sub-$2B screen carried back to
2010 with 54 tickers dropped for `max_1d_move >= 1.0` (665 names remain). Every panel therefore
flatters the long book, and the null inherits exactly the same bias — which is a point in the
null's favour: it is biased the same way the statistic it is testing is.

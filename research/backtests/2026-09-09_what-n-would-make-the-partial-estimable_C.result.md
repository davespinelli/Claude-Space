# Idea 547 — what-n-would-make-the-partial-estimable (lane C, 2026-09-09)

**ANSWERED / KILL of the named mechanism, and there is no single n. Collinearity does NOT
inflate the rank-partial's sampling SD — the observed sd(PARTIAL)/sd(MARGINAL) is 0.983–1.102
(mean 1.046) in 32 of 32 cells against the 1/sqrt(1−R²) prediction of 1.396–1.579 for `disp`
and `evol`. The control does not add noise, it removes signal, so n* scales as 1/|rho|² and is
characteristic-specific: independent-block n* median 1,160 for the partial vs 112 for the
marginal (primary stratum), 110 for `corr`/CAND20 but 44,820 for `disp`/CAND10. KILL for
capital: 0 of 2,880 panel-books clear 4a, 0 clear BOTH paths, and the walk-forward picks lose
to SPY and to RULES v2 at both strata, at every n, on both statistics.**

## Design

Idea 284/293's panel builder **verbatim** (seed key `zlib.crc32("STRAT|{q:.3f}|{sd}")`), run
further: **480 draws at each of two strata = 960 constructed panels**, four books each
(CAND10 / CAND20 / EWall + RULES v2 on the same panel). Seeds 0–59 are idea 293's committed
panels bit-for-bit (120 rows), seeds 100–159 coincide with lane B's idea-310 block B (120 rows),
720 rows are fresh; the block is stamped in `.panels.csv`.

Two dials only, as the queue specifies: **n ∈ {30, 60, 120, 240}** × **stratum ∈
{(q 0.500, k 40) PRIMARY, (q 0.250, k 40)}**. The primary stratum is idea 284's own and is the
*hard* case — its corr(disp, evol) = +0.7757 on seeds 0–59 is above idea 310's +0.6909 median;
the second is the easy case at +0.5474. Everything else is fixed at the record's values:
4 characteristics × 3 books × 2 statistics (MARGINAL = Spearman, idea 546's statistic;
PARTIAL = rank-partial on the other three, idea 284/293's estimator) = **192 curve points, all
reported**, from 400 disjoint block pairs each.

**Gates.** G1 the rebuild reproduces idea 293's committed `.panels.csv` on 60 × 7 = 420 cells to
**1.110e-16**. G2 idea 284's published within-stratum `corr` rho −0.3648 / −0.4815 / −0.4708
reproduces to **2e-05**. G3 idea 310's premise — lane B's committed rank corr(disp, evol) —
reproduces to **2e-05** (+0.7757) and **3e-05** (+0.5474).

## What the numbers say

### The named mechanism is refuted (B4)

| stratum | char | R² on other three | predicted sd inflation | **observed sd(PART)/sd(MARG)**, n = 30 / 60 / 120 / 240 |
|---|---|---|---|---|
| q 0.500 | disp | 0.5987 | **1.579** | **1.082 / 1.102 / 0.994 / 1.068** |
| q 0.500 | evol | 0.5340 | **1.465** | **1.054 / 1.073 / 0.983 / 1.030** |
| q 0.250 | disp | 0.5959 | **1.573** | **1.099 / 1.031 / 1.040 / 1.000** |
| q 0.250 | evol | 0.4866 | **1.396** | **1.080 / 1.044 / 1.045 / 0.995** |

The rank-partial's SE is the same 1/√n as the marginal's: the finite-pool-corrected constant
`c_inf = sd_block·√n / √(1 − n/N)` is **0.990–1.041 with SD 0.025–0.042** across all four rungs
and both statistics. What the control actually does is delete the estimand — pooled |rho| at
(q 0.500, k 40) / CAND20: `disp` **+0.1478 → −0.0378**, `evol` +0.1746 → +0.1268, `corr`
−0.1970 → −0.1601, `breadth` −0.0668 → −0.0408.

### The answer: n* is per-characteristic, not per-statistic (B3, B7c)

Independent-block n* = (c_inf · 1.6187 / |rho|)², the n at which a block's sign replicates 90%
of the time against an independent block:

| stratum | statistic | median n* | range | ≤ 240 | ≤ 60 |
|---|---|---|---|---|---|
| q 0.500, k 40 | MARGINAL | **112** | 65 – 693 | 9/12 | **0/12** |
| q 0.500, k 40 | PARTIAL | **1,160** | 110 – 44,820 | 5/12 | **0/12** |
| q 0.250, k 40 | MARGINAL | **97** | 47 – 3,527 | 9/12 | 1/12 |
| q 0.250, k 40 | PARTIAL | **938** | 255 – 255,873 | 0/12 | **0/12** |

Per characteristic on the primary stratum (PARTIAL): `corr` **110 / 128 / 187**, `evol`
**167 / 225 / 1,217**, `breadth` 1,104 / 1,846 / 2,453, `disp` **1,873 / 10,566 / 44,820**. So
the partial *is* estimable — for `corr` at n ≈ 110–190 and for `evol` on two of three books at
n ≈ 170–225 — and for `disp` it effectively never is, because the control drives its estimand to
zero, not because it makes it noisy. The raw ladder agrees: the empirical curve reaches the 0.90
bar in 5/12 partial points at q 0.500 and 4/12 at q 0.250, all of them `corr` or `evol`.

**A correction that also lands on idea 546's premise: the marginal is not estimable at n = 60
either.** Its own median n* is 97–112, and **0 of 24 (stratum × char × book) marginal points
clear the 90% bar at the record's n = 60** (1 of 24 at q 0.250). "The marginal keeps its sign
21–26 of 27" is sign consistency of *pooled* estimates across strata, which is a different
statistic from 90% block replication and should not be read as the latter.

### The block device itself is biased (B7, declared post-hoc)

The first run produced two things independent blocks cannot do: `c` fell monotonically with n
(1.006 → 0.717), and agreement fell **below 0.50** and kept falling (disp/CAND10/PARTIAL
0.460 → 0.110). Cause: two disjoint blocks of n from a fixed pool of N are negatively dependent,
corr = −n/(N − n), reaching **−1 at n = N/2** where they are exact complements. The analytic
same-sign probability of a bivariate normal at that correlation tracks the observed rate to a
**median |error| of 0.022 (mean 0.036) over all 192 points**, which validates the whole model.

What it costs the record — same-sign rate by effect size a = |mu|/se:

| a | independent | n = N/3 (r = −1/3) | **complement (r = −1)** |
|---|---|---|---|
| 0.00 | 0.500 | 0.392 | **0.000** |
| 0.50 | 0.573 | 0.494 | **0.383** |
| 1.00 | 0.733 | 0.701 | 0.683 |
| 2.00 | 0.956 | 0.955 | 0.955 |

**Idea 310's own split-half device — seeds 0–29 vs 30–59 — is n = 30 of N = 60, i.e. r = −1
exactly.** Its published counts ("evol 18–20/27, disp 13–19/27, near a coin") are therefore
biased *toward* disagreement in precisely the small-effect regime it was used to diagnose, and
can print below a coin flip mechanically. Any future sign-replication claim should draw its two
blocks from a pool of at least 4n, or quote the r = −n/(N−n) correction.

### Rule 8 (PROTOCOL 8) and both KEEP paths

Out of sample in two directions: characteristics IS-only (≤ 2016-12-31), every book metric read
OOS (≥ 2017-01-01); and the direction fitted on block A applied **once** to the disjoint block B
(4,800 picks).

| stratum | statistic | pick OOS Sharpe | pick OOS CAGR | pick OOS MaxDD | anchor | RULES v2 OOS | SPY OOS |
|---|---|---|---|---|---|---|---|
| q 0.500 | MARGINAL | 0.7129 | 9.54% | −27.64% | 0.6998 | **0.8527** | **0.8820** |
| q 0.500 | PARTIAL | 0.7111 | 9.41% | −27.41% | 0.6998 | **0.8527** | **0.8820** |
| q 0.250 | MARGINAL | 0.9014 | 12.27% | −26.41% | 0.8438 | **1.0025** | 0.8820 |
| q 0.250 | PARTIAL | 0.8800 | 11.82% | −26.21% | 0.8438 | **1.0025** | 0.8820 |

(SPY OOS CAGR 15.45%, OOS MaxDD −33.72%.) The picks beat their do-nothing anchor by +0.0113 to
+0.0576 of Sharpe and **lose to SPY on CAGR at every stratum and to RULES v2 on Sharpe at both**.
More draws buy a better direction only where the panel is already the story: at q 0.250 the edge
rises with n (+0.0185 → +0.1090 marginal, −0.0015 → +0.0884 partial), at q 0.500 it does not
(+0.0195 → +0.0019). **KEEP paths: 0 of 2,880 panel-books clear 4a, 170 clear 4b, BOTH 0**; of
the 4,800 picks, 0 clear 4a and 541 clear 4b. Every 4b pass sits on a panel whose un-ranked book
also passes — the same footprint idea 309 published.

## Verdict

**ANSWERED / KILL.** The queue's premise — that collinearity is what makes the partial's sign
noise at n = 60 — is refuted: the partial is no noisier than the marginal. The partial is
estimable at n ≈ 110–225 for `corr` and `evol`, and at no feasible n for `disp` and `breadth`,
because the control removes their estimand. No RULES change, no memo, no KEEP candidate.

**SURVIVORSHIP:** panels are drawn from SMALL439 and BSTK100, both *current* constituents of
their screens, so every panel's return level is inflated and the KEEP columns inherit that
whole. This run measures how many draws an estimator needs before its sign replicates, which the
bias does not create; but "estimable" here is a statement about the estimator inside this
corpus, never a tradable edge.

# Idea 800 — is the MATCH RESIDUAL of a kernel draw a POOL-SIZE law?

**Run:** lane C, 2026-09-12 UTC.
**Script:** `2026-09-12_is-the-MATCH-RESIDUAL-of-a-kernel-draw-a-POOL-SIZE-law_C.py`

**STATUS: INDEPENDENT CONCURRENT REPLICATION.** A cloud lane claimed and ran idea 800 in parallel
with this one (`..._cloud.py`, commit 0e8eb3d); neither run saw the other, and the collision was
discovered only at push time. This file is committed as a replication, not as the claim. **The two
runs agree on the headline** — no pool-size law, premise killed, no KEEP — from different designs:
the cloud run added an **SS same-distribution null** arm pair (min n up to 330) and a fourth draw
size k=48; this one adds an **exact reproduction of idea 796's Q5 anchor cell** (momac |d|
2.776e-17 with its verbatim seed keys), the **40-fold re-draw distribution of that cell**, the
**re-estimation decomposition**, a common-rung control and a 29,808-book KEEP/WF-B sweep.

**The cross-check that matters:** the cloud run independently reports **0.0056** for the full-pool
momac residual where this run's verbatim-key reproduction of idea 796 reads **0.00271**. Those are
not in conflict — 0.0056 sits inside this run's 40-re-draw band for *that same cell* (mean 0.00682,
median 0.00677, range 0.00228–0.01106). Two honest runs of this machinery disagreeing by 2x on
"match tightness" for identical inputs is exactly the finding both runs report. The cloud run reads
idea 796's 430→663 move at 0.83x / 0.48x against its published 4.90x; this run attributes that move
to characteristic re-estimation (9.49x vs 1.75x frozen). Same conclusion from both sides.
**Verdict: ANSWERED — THERE IS NO POOL-SIZE LAW. The residual is flat in BOTH arms over a 3.7x
range of pool size; what actually moves it is RE-ESTIMATING the characteristic, and the record's
tightest published residuals are ~2.5th-percentile draws of their own machinery. KILL for capital;
no RULES change. The entitlement table is the deliverable.**

## The answer in one line

Over N = 36…134 names per arm at k = 12/24/36, momac's mean |match residual| is **monotone
decreasing in N in 0 of 9 curves** (1 of 18 including the tpers control, 0 of 18 on the
common-rung control), the pooled log-log fit on the draw fraction k/N has **slope −0.142 with
R² 0.071** — wrong sign, no explanatory power — and the **median replicate sd is 0.43x the
residual itself**, with the mean replicate sd running **0.33x–1.29x the entire span of the N × k
grid**. The queue's premise is refuted: |resid| is draw noise around a level set by the
characteristic, not a function of pool density.

## H_THIN and H_FAT: neither arm

| leg | what moves | momac k=36, FULL | verdict |
|---|---|---|---|
| ASYM_S | n_S 134 → 657, n_B full | 0.00612 → 0.00690 (move 0.00078 vs replicate sd 0.00313) | FLAT |
| ASYM_B | n_B 48 → 134 (the whole big arm), n_S full | 0.00660 → 0.00619 (move 0.00042 vs sd 0.00567) | FLAT |

Fat arm flat in **16/18** curves, thin arm flat in **16/18**. H_THIN as pre-registered demanded all
18 flat past the thin arm and so reads FAIL at its own bar, but the informative fact is the pair:
raising either arm moves nothing. `min(n_B, n_S)` does not govern the residual and neither does
`max`. Idea 796's own 5x was produced by changing the **fat** arm (134 was the thin arm in both its
vintages), which was already the wrong shape for a thin-arm law; this run shows it was not a
density effect at all.

## What DOES move it — H_REEST PASS

Repeating the identical sub-samples with the characteristic, rungs and bandwidth **re-estimated on
the sub-sample** — which is exactly what idea 796's 430 → 663 vintage change performed — moves
|resid| by **9.49x** across N against **1.75x** with the characteristic frozen (FULL, momac, k=36).
At N=48 the re-estimated cell reads **0.00084** against the frozen **0.00670** (0.12x), while
sd(momac) collapses **0.0909 → 0.0519**: momac is a *within-pool* rank autocorrelation, so changing
the pool changes the variable, the rung levels and the bandwidth together. **A momac-style
characteristic is not comparable across panel vintages at all**, and idea 796's 5x is that
re-estimation, not pool density.

## The record's tight residuals are low-tail draws

At idea 796's own cell (n_B 134, n_S 657, k 36, BW 0.500, Q5) the pools, characteristic, rungs,
bandwidth, k and seed count are all held fixed and **only the draw key is re-rolled, 40 times**:

| char | committed | 40 re-draws: mean ± sd | range | position of the committed value |
|---|---|---|---|---|
| momac | **0.00271** | 0.00682 ± 0.00187 | 0.00228–0.01106 | **1/40 below (2.5%)**, 0.40x the mean, −2.20 sd |
| tpers | **0.00106** | 0.00149 ± 0.00025 | 0.00104–0.00199 | **1/40 below (2.5%)**, 0.71x the mean, −1.71 sd |

Idea 796's headline — momac matched "5.6x tighter than idea 571's 0.0152" — is a 2.5th-percentile
re-draw of its own estimator. So is idea 571's tpers 0.0017. The residual reported by any single
seeded draw is not a measurement of matching quality.

## The entitlement table (the deliverable)

FULL window, SYM leg, frozen characteristic, mean / p90 over 6 sub-sample replicates:

| char | k | N=36 | N=64 | N=110 | N=134 | p90 at N=134 | worst single rung |
|---|---|---|---|---|---|---|---|
| momac | 12 | 0.00899 | 0.00643 | 0.00857 | 0.00587 | 0.00864 | 0.02497 |
| momac | 24 | 0.00335 | 0.00782 | 0.00595 | 0.00616 | 0.00904 | 0.01566 |
| momac | 36 | — (N=k) | 0.00755 | 0.00845 | **0.00493** | **0.00766** | 0.01227 |
| tpers | 36 | — (N=k) | 0.00170 | 0.00147 | **0.00168** | **0.00202** | 0.00262 |

**Rule any future matched-level claim can quote:** on this machinery at k=36 a claim is entitled to
|resid| of about **0.005 (p90 0.008)** on momac and **0.0017 (p90 0.0020)** on tpers *at every
pool size this machinery can reach* — 36–134 names on the big arm, 36–657 on the small one. A residual below its cell's p90 is a draw, not evidence.
Residuals must be quoted with the replicate band beside them or not quoted at all. **H_ENTITLE
PASS:** the entitled p90 (0.0077) exceeds the record's tightest published readings — tpers 0.0017
(idea 571) and volpers 0.0007 (idea 798) — by 4.5x and 11x.

## Why the all-rung mean looked like it might fall (mechanism, added after a pilot)

The k-name **reach band widens with N** (momac k=36: 0.0626 → 0.0836 as N goes 84 → 134 on the B
arm, 0.1018 → 0.1472 on S), so a bigger pool unlocks *harder* rungs: the number of overlapping
rungs runs 1.0 → 3.7 across the grid. The pre-registered all-rung mean is therefore taken over a
different rung set at each N. Fixing the rung set (`.commonrung.csv`) leaves monotonicity at
**0/18**. What pool size buys on this machinery is REACH — which rungs can be addressed at all —
not tightness.

## Rule 8

**WF-A** rebuilds the whole law inside each window (characteristic, rungs, bandwidth and draws all
re-estimated on that window's bars). momac: IS slope **+0.020, R² 0.002**; OOS own slope −0.054,
R² 0.014; FULL −0.142, R² 0.071. The IS exponent predicts the OOS cells to a mean |log ratio| of
**0.264** (median pred/actual 0.83x) — which is *not* a transportable law but the opposite: a fit
with no slope predicts as well as a constant does, because the thing being predicted is flat. H_LAW
fails in every window separately (0/3 momac k-curves monotone in each of FULL, IS, OOS).

**WF-B** takes the ladder as a trading instruction (hold whichever flavour is available at a matched
level) and picks (flavour, level, seed, arm, gross, cadence) by IS Sharpe alone at each of the 18
tuned cells, OOS read once. **0 of 18 picks beat RULES v2 on OOS Sharpe** (comparand 1.285 on U56),
9 of 18 beat SPY (0.882), 4a 1/18, 4b 1/18. The global pick (k=12, N=48, SONLY/EWall/g0.50/W) has
the highest IS Sharpe in the file at **1.820** and collapses to **OOS Sharpe 0.416, CAGR 4.23%** —
an IS-selection failure, not an edge.

## KEEP paths — 29,808 books at all 18 tuned cells

**4a 310 (1.0%) / 4b 563 (1.9%) / BOTH 16 (0.05%).** The DD leg binds nearly everywhere (`DD` or
`H1,H2,OOS,DD,CAGR` are the top failure signatures in all 18 cells). Stated before the run and
repeated here: every panel is a kernel-weighted seeded draw from a randomly sub-sampled pool — two
layers of randomisation away from anything a person can trade — so these counts are diagnostics.
**No book is claimed as a capital candidate, and no RULES change is proposed.**

## Gates

G0 determinism 0/72 draws differ · G1 this file's fast characteristic estimator vs idea 796's
verbatim `panel_chars` **2.220e-16** (bar 1e-12) · G2 `fast_backtest` vs `engine.backtest`
**2.776e-17** (bar 1e-9) · G3 ANCHOR reproduces idea 796's committed LIVE/BW0.500/Q5 residuals —
momac |d| **2.776e-17** (exact), tpers 1.578e-07 (bar 1e-4) → **H_PARENT PASS**.

## Hypotheses

| | result |
|---|---|
| H_LAW (monotone decreasing in N) | **FAIL** — momac 0/9 curves, 1/18 overall, 0/18 common-rung |
| H_RATIO (k/N collapse, R² ≥ 0.70) | **FAIL** — momac FULL slope −0.142, R² 0.071 |
| H_THIN (flat past the thin arm, all curves) | **FAIL** at its bar — 16/18 flat; but the thin arm is 16/18 flat too |
| H_FAT (fat arm still moves it) | PASS at the bar, **substantively no** — both arms flat |
| H_PARENT (reproduce idea 796 to 1e-4) | **PASS** — momac exact to 2.8e-17 |
| H_REEST (re-estimation moves it more) | **PASS** — 9.49x vs 1.75x |
| H_ENTITLE (entitled resid > the record's tightest) | **PASS** — p90 0.0077 vs 0.0017 / 0.0007 |

## Survivorship

Both arms are current constituents (broad panel; sub-$2B screen with every `max_1d_move ≥ 1.0`
ticker dropped, 52 names). Dead small names are absent. For this question the bias is second-order —
the residual is a matching diagnostic, not a return, and both arms are drawn from survivor pools —
but every absolute residual here is an estimate **for a survivor pool of that size**.

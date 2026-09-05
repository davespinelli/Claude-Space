# Idea 114 — IS-Sharpe-margin-as-the-reportable-selector-statistic (cloud, 2026-09-05)

**Verdict: PARTIAL** — the margin predicts the selector's *internal* stability and nothing about
its *out-of-sample* payoff. Adopt it as a stability flag, not as a confidence interval.

## What was run
Idea 99/109/112's harness verbatim: 6 overlay grids × 2 base books × 2 universes × 2 cost rungs =
**44 cells**, 178 grid points, weekly rebalance, next-day execution, 10 and 25 bps. IS = ..2016-12-31,
OOS = 2017-01-01.. (never used for any pick). Harness cross-check: pooled LOYO pick-change rate
reproduces idea 112 exactly (72/352 = 20.5%).

Per cell, four statistics, all declared before any number was computed:
- **M** = IS Sharpe(best) − IS Sharpe(runner-up) at the rule-8 pick. **M_norm** = M / sd(IS Sharpe over the grid).
- **S** = fraction of the 8 leave-one-IS-year-out windows whose argmax differs from the full-IS argmax.
- **R** = OOS regret = max_p OOS Sharpe(p) − OOS Sharpe(pick) ≥ 0.
- **C** = mean OOS Sharpe cost of the LOYO swaps (0 for years that do not swap).

Pre-registered bar: ADOPT iff Spearman(M,S) ≤ −0.30 **and** Spearman(M,R) ≤ −0.30, each with
one-sided permutation p < 0.05 on the 22 primary (10 bps) cells, and both signs replicating at 25 bps.

## Results

| test (22 primary cells, 10 bps) | rho | perm p | 25 bps replication | bar |
|---|---|---|---|---|
| **H1** M → S (LOYO pick-change rate) | **−0.368** | **0.046** | −0.240 (same sign) | **PASS** |
| **H2** M → R (OOS regret) | +0.119 | 0.705 | +0.143 (wrong sign) | **FAIL** |
| M → \|C\| (swap cost) | −0.022 | 0.464 | −0.118 | — |
| M_norm → S | **−0.548** | **0.005** | −0.652 (p 0.001) | (secondary) |
| M_norm → \|C\| | **−0.461** | **0.017** | −0.609 (p 0.002) | (secondary) |
| M_norm → R | +0.059 | 0.613 | −0.264 | (secondary) |

Use test, primary cells split at the median margin (0.008 Sharpe):

| half | n | mean M | mean S | mean R | frac pick = OOS-best |
|---|---|---|---|---|---|
| high margin | 11 | 0.036 | **0.125** | 0.018 | 0.455 |
| low margin | 11 | 0.002 | **0.330** | 0.014 | 0.182 |

Margin by instrument (10 bps): band 0.044, crypto 0.036, sleeve 0.034, breadth 0.004, stop 0.004,
gross 0.001 — the two grids with the flattest surfaces (gross, breadth) carry mean S of 0.375 and
0.469, i.e. rule 8's pick there is close to a coin flip between IS-equivalent points.

## Why H2 fails, and it is not the margin's fault
**There is almost no regret to predict.** Mean R across the 44 cells is **0.015 Sharpe** (median 0.005,
max 0.072), and rule 8's pick is *already* the OOS-best point in 16/44 cells. The pooled LOYO swap
cost C is −0.0029. The IS surface is flat (mean M = 0.019, median 0.006 Sharpe) *and* the OOS surface
is flat over the same points, so the selector's choice barely matters either way — which is idea 112's
"flat and noisy rather than wrong" finding, now measured on the OOS side. A statistic cannot predict
a quantity whose whole cross-cell range is 0.07 Sharpe.

## Walk-forward (PROTOCOL rule 8, all 44 cells, picks made on IS only)

| cost | n | 4a passes | 4b passes | 4b-OOS passes | mean OOS Sharpe |
|---|---|---|---|---|---|
| 10 bps | 22 | 9 | 13 | 15 | 1.115 |
| 25 bps | 22 | 8 | 7 | 7 | 0.982 |

Headline cell (sleeve / u56 / top20 / 10 bps — the standing KEEP-4b candidate): pick f=0.50 with
**M = 0.018**, S = 0.250, **R = 0.000**; full 12.3% / 1.180 / −14.3%, halves 1.161 / 1.200;
OOS 13.6% / **1.261** / −14.3% vs RULES v1 OOS Sharpe 0.699 and SPY OOS 15.5% / 0.882 / −33.7%.
**4b PASS, 4a fail** — unchanged from ideas 101/112. Its margin is *below* the 44-cell mean, and its
regret is zero: further evidence that margin says nothing about OOS quality.

Margin does not separate the cells that pass 4b either (10 bps: pass mean M 0.021 / S 0.308,
fail mean M 0.016 / S 0.111) — if anything the 4b passers are the *less* stable picks.

## Recommendation to the Sunday review (no file was modified)
Quote the margin, but say what it is. Proposed PROTOCOL rule 8 sentence:

> Every walk-forward must also report the **IS Sharpe margin** M = IS Sharpe(pick) − IS Sharpe(runner-up)
> and the normalised margin M/sd(IS Sharpe over the grid). The margin is a **selector-stability**
> statistic only: on 44 cells it predicts leave-one-IS-year-out pick instability (Spearman −0.37 raw,
> −0.55 normalised) but has **no relationship to out-of-sample regret** (+0.12, p 0.71). A pick with
> M < 0.01 Sharpe is a tie, and the walk-forward must be read as a statement about the grid, not the point.

M_norm is the better stability predictor (−0.55 vs −0.37, and it is the only variant that also prices
the swap cost, −0.46), but M is in Sharpe units and is what a reader can compare to the OOS gap, so
report both.

## Caveats
Survivorship: both equity panels are current constituents (levels biased up; identical across every
cell compared here). Crypto's IS window starts 2014-09-17 — crypto cells are shown in and out of every
pooled statistic (ex-crypto: M→S rho −0.368, p 0.058). 22 points is a small sample for a correlation
and the permutation p prices exactly that; H1 clears its bar at p = 0.046, which is not a wide margin
in itself. Calendar-day index (queue idea 38) affects every cell identically.

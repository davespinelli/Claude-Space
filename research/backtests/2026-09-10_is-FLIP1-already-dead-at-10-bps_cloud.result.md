# Idea 633 — is-FLIP1-already-dead-at-10-bps (cloud, 2026-09-10)

**Filed as an INDEPENDENT CONCURRENT REPLICATION (record convention 320R).** A lane C run
answered idea 633 the same day while this one was in flight; the two were written independently
and **agree on the headline** — the queue's premise is killed, FLIP1 is a pass-boundary count,
and its fall across the cost ladder is depopulation of the pass region rather than smoothing —
and on gate G0's exact reproduction of idea 408R and on the derived-rung identity (1.041e-17).
They differ in census scope: lane C reads 149 files / 86,859 points restricted to sweeps with a
**declared** rung and publishes the like-for-like fall 7.98% → 5.87% → 3.89% with the mixed leg
carrying 72% of it; this run reads 208 files / 154,829 points, reports the 7,269 no-rung blocks
as their own row, and adds the exact random-arrangement null (§2) plus the fresh-grid fact that
FLIP1 is **1.73% at every rung from 0 to 50 bps** (§3). Both find 4b passing only at the top of
the gross ladder and claim no KEEP.

**ANSWERED / KILL of FLIP1-as-published, and a KILL of the queue's own premise.** No RULES
change, no book promoted, no KEEP claimed, no memo. RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py untouched.

Script `2026-09-10_is-FLIP1-already-dead-at-10-bps_cloud.py`; outputs `.txt .census.csv
.census_by_rung.csv .inventory.csv .fragility_files.csv .grid.csv .blocks.csv .wf.csv`.
Two tuned parameters, exactly the queue's: **RUNG** ∈ {0, 5, 10, 15, 25, 50} bps and
**GRID FAMILY** ∈ {band, gross, K, n, f, vol}. Panel is a reported axis.

## Gates (all pass)

| gate | result |
|---|---|
| G0 | idea 408R's published FLIP1 reproduces **exactly** from its own committed `.cols.csv`: 0.1600 / 0.0667 / 0.0000 at 0 / 10 / 25 bps (published 0.160 / 0.067 / 0.000) |
| G1 | `fast_backtest` vs `engine.backtest` **1.041e-17** returns / **2.220e-16** turnover |
| G2 | host books nest `baseline.rules_v2_weights` and `rules_v1_weights` at **0.000e+00** |
| G3 | derived rung `r(c) = r(0) − turn·c/1e4` vs `engine.backtest` at all six rungs **1.041e-17** — the six rungs share one book by construction |
| G4 | the analytic random-arrangement null equals a seeded Monte-Carlo to **0.0035** over 5 sweep lengths × every pass count |

## 1. The premise is a denominator artefact, and idea 408's own file says so

FLIP1 is a rate **over all grid points**, so it is bounded above by the 4b pass rate: a sweep on
which nothing passes cannot contain a flip. From idea 408R's own committed file, at the same
three rungs it published FLIP1 for:

| rung | 4b pass rate | FLIP1 | **flips per PASSING point** |
|---|---|---|---|
| 0 bps | 20.67% | 16.0% | **0.774** |
| 10 bps | 3.33% | 6.7% | **2.000** |
| 25 bps | 0.00% | 0.0% | undefined (nothing passes) |

The numerator fell 2.4×; the denominator fell 6.2×. **Conditional on a verdict existing at all,
idea 408's corpus is 2.6× MORE marginal at the protocol rung than at zero cost**, not less. The
queue's sentence — "costs have already removed the phenomenon" — is true of the printed rate and
false of the thing the rate is meant to measure.

## 2. Census of the record: 208 files, 19,950 sweeps, 154,829 points

Every committed `research/backtests/*.csv` that publishes a 4b verdict column and a swept dial
(detection rule and per-file outcome in `.inventory.csv`; 2,919 CSVs scanned in 468 s).

| rung | blocks | points | 4b pass | FLIP1 | flips/pass | random-null FLIP1 | **obs / null** |
|---|---|---|---|---|---|---|---|
| 0 | 967 | 8,342 | 19.25% | 11.68% | 0.606 | 15.87% | **0.736** |
| 5 | 541 | 4,711 | 19.51% | 15.24% | 0.781 | 20.82% | **0.732** |
| 10 | 5,739 | 53,008 | 15.35% | 7.99% | 0.521 | 11.60% | **0.689** |
| 25 | 4,415 | 34,341 | 7.66% | 2.84% | 0.371 | 3.70% | **0.768** |
| all | 19,950 | 154,829 | 12.37% | 8.15% | 0.659 | 10.83% | **0.753** |

Across the twelve published rungs with ≥50 points, Spearman ρ(rung, FLIP1) = **−0.615** and
ρ(rung, pass rate) = **−0.636** — the same number twice. ρ(rung, flips per pass) = **+0.136**:
no decline. And once each block is divided by what its own pass **count** would produce under a
random re-arrangement on the same sweep, **the ratio is flat at 0.69–0.77 over a 25× range of
cost**. Verdict clustering on a sweep is a property of the sweep, not of the cost rung.

Two further facts the record should carry: 40.6% of blocks that contain any pass have a widest
contiguous pass-run of **exactly one point** (18.2% at 10 bps, 53.5% at 15, 54.2% at 20, 50.0%
at 50), and among blocks that are mixed at all the flip rate is **20.0%** at 10 bps against
41.6% at 0 — with a median pass window of **1 point** at both 10 and 25 bps.

## 3. Fresh grid, where this file controls the spacing (231 points × 6 rungs, all committed)

Idea 408's six adopted constants, three panels, the rung derived from one no-cost run per book
(gate G3), so the only thing that changes between rungs is the cost:

| rung | 4b pass | FLIP1 | flips/pass | null | obs/null | widest pass window |
|---|---|---|---|---|---|---|
| 0 | 5.19% | **1.73%** | 0.333 | 10.72% | 0.162 | 6.0 pts |
| 10 | 4.76% | **1.73%** | 0.364 | 10.30% | 0.168 | 5.5 pts |
| 25 | 4.33% | **1.73%** | 0.400 | 9.61% | 0.180 | 5.0 pts |
| 50 | 2.60% | **1.73%** | 0.667 | 6.54% | 0.265 | 3.0 pts |

**FLIP1 is identical at every rung from 0 to 50 bps.** It does not die at 10 bps; on a grid whose
spacing and dial set are controlled here it does not move at all, while flips per passing point
**doubles**. Idea 408R's 16.0 → 6.7 → 0.0 is a fact about its 150-point corpus's pass rate, not a
fact about cost. All twelve of the fresh grid's 4b passes at any rung sit on the `gross` dial
(the U56/B136 ladder idea 585 already owns); `band`, `K`, `n`, `f` and `vol` pass 0/6 at every
rung, so their FLIP1 is structurally 0 and carries no information either way.

## 4. Which published fragility claims can even be located on the cost ladder

302 committed CSVs publish at least one fragility-family column (`thin`, `plateau`, `window`,
`width`, `step*`, `flip*`). **Only 99 (32.8%) state a cost rung anywhere in the file**; 41
contain 0-bps rows, 96 contain 10-bps rows, and **39 carry both and can be re-read inside their
own file**. So for roughly two-thirds of the record's fragility columns the queue's question —
"is this a 0-bps artefact?" — is *not answerable from the committed artefact*. That is the
reportable defect here, and it is cheaper to fix than to litigate: state the rung beside the
statistic.

## 5. Rule 8 and both KEEP paths (PROTOCOL 4, 8)

Choice on 2008–2016 by IS Sharpe, 2017–2026 read once, 18 (panel × dial) cells per rung, both
with and without the record's own fragility screen (refuse a point flagged FLIP1):

* **The screen changes 0 of 18 picks at every one of the six rungs**, mean ΔOOS Sharpe
  **+0.0000** everywhere. As a chooser, the fragility column is inert.
* Comparands OOS @10 bps — U56: RULES v2 9.51% / **1.2876** / −11.90%, SPY 15.32% / 0.8758 /
  −33.72%. B136: v2 7.98% / **1.1206** / −12.18%. SMALL439: v2 3.84% / **0.5665** / −14.70%.
* Best pick per panel OOS: U56 `gross=1.20` 15.35% / 1.2862 / −18.69%; B136 `gross=1.20` 12.80%
  / 1.1185 / −19.14%; SMALL439 `band=0.12` 4.53% / 0.6355 / −15.98%. **0 of 18 picks beat their
  own panel's RULES v2 on OOS Sharpe on U56 or B136** (U56 short by 0.0014, B136 by 0.0021), and
  every U56/B136 pick that gets near it does so by carrying 6–7 pp more drawdown.
* KEEP paths on all 231 points: **4b 12 / 11 / 10 / 10 / 6 at 0 / 10 / 25 / 50 bps** (11 at the
  headline rung), **4a 3/231**, **BOTH 0/231**. The eleven headline 4b passes are `U56 gross
  0.95–1.20` and `B136 gross 1.00–1.20`, binding bar CAGR (or DD at the top of the ladder), each
  losing to its own panel's RULES v2 OOS. **No new KEEP-candidate, no memo.**

## Recommendation (report-only, no PROTOCOL edit made)

1. **Do not publish FLIP1 as a rate over all points.** Publish it as *flips per passing point*,
   or beside the pass count, or not at all: as published it is a monotone function of the 4b
   pass rate and carries no independent information (obs/null flat at 0.69–0.77 over 0–25 bps).
2. **State the cost rung beside every fragility statistic.** Two-thirds of the record's 302
   fragility-bearing CSVs cannot be placed on the cost ladder at all.
3. Idea 408R's conclusion — "STEP does not earn a third column at the protocol rung" — **stands
   on its own AUC evidence** and is not disturbed here; what does not stand is the reading that
   fragility itself has been removed by costs. It has not: per passing point it roughly doubles
   between 0 and 50 bps.

## Caveats

* **SURVIVORSHIP (PROTOCOL 9).** B136 and SMALL439 are current-constituent lists, so their
  levels are biased upward; SMALL439 drops the 44 names with `max_1d_move ≥ 1.0`. Every claim
  above is a within-panel contrast between cost rungs on identical books, which the bias cannot
  move. SMALL439 passes 4b 0/462 at every rung, so it contributes no flips at all.
* The census's dial detection is a **heuristic** (documented in the script and audited per file
  in `.inventory.csv`): the block key is every non-dial axis column, the dial is the numeric
  column that yields the most usable sweep rows, and `n` is deliberately excluded from the dial
  allowlist because in this record it is a sample count far more often than the holdings dial.
  208 of 2,919 CSVs qualify; the other 2,711 either publish no 4b column, no sweep, or a sweep
  this rule cannot identify. Files above 40 MB or 200k rows are skipped.
* 7,269 of the 19,950 blocks (46,848 points) come from files that state **no** cost rung; they
  are reported as their own row and excluded from every rung-conditional statement.
* The random-arrangement null is exact (closed form, gate G4), but it is a null about the
  *arrangement* of a fixed number of passes on a sweep, not about the sweep's length or spacing;
  a publisher who chooses both can still move FLIP1, which is exactly idea 409's point.

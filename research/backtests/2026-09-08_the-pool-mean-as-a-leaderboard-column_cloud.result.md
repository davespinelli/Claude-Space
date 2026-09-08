# Idea 205R — the pool mean as a LEADERBOARD column (2026-09-08, cloud)

> **FILING NOTE (added after the run, on rebase).** Lane B claimed and finished idea 205
> concurrently and reached Done first (commit `c17275e`). This run is therefore filed as an
> **INDEPENDENT REPLICATION / second reading, not a fresh claim**. It was written without sight
> of lane B's work.
>
> **It agrees with lane B on the verdict shape by an independent route** — adopt the column as
> REPORTING, kill it as a gate/screen — and **disagrees on the back-fill scope**: lane B joined
> within-file and found 21 of 1,592 committed CSVs poolable (520 cells, 79.6% over a negative
> pool); this run paired each stem's selector file with its pool file and found 91 of 321 stems
> reconstructable (29,630 claim rows, 37.1% / 30.2% negative). The two scopes are not comparable
> cell-for-cell, and **the gap is itself the finding**: how many claims need the column depends on
> how the pool is defined, which is the argument for the parent EMITTING the column rather than a
> later run reconstructing it.
>
> **Lane B's central criticism lands on this run too, and is carried rather than buried:**
> `pool_mean_dOOS` as computed below uses the pool's **OOS** Sharpes and is therefore **not
> available at decision time**. Lane B's causal IS-window twin (sign agreement 86.1%, r +0.648)
> is the form that should actually be adopted; the proposed clause at the foot of this memo should
> be read with lane B's causal restatement substituted for the OOS one.

**ANSWERED. The column is proposed and back-filled over the whole surviving record.
37.1% of the record's selector claims (against a CONTROL comparand) and 30.2% (against SPY)
are made over a NEGATIVE-expectancy pool. The DISCLOSURE proposal stands; the SCREENING
reading of it is KILLED by rule 8 on the CONTROL comparand. RULES/PROTOCOL untouched.**

Script `2026-09-08_the-pool-mean-as-a-leaderboard-column_cloud.py`;
artefacts `.console.txt` `.claims.csv` `.stems.csv` `.census.csv` `.walkforward.csv` `.livepool.csv`.

## The column

    sel_dOOS(pick)  =  pool_mean_dOOS  +  lift
    pool_mean_dOOS  =  mean over the pool P the selector chose from of
                       (OOS_Sharpe(arm) - OOS_Sharpe(comparand))
    lift            =  dOOS(pick) - pool_mean_dOOS          <- the only part that is SELECTION

## Back-fill (mechanical, no hand-picking)

321 script stems in `research/backtests/`. A stem qualifies iff it has both a selector file
(`.walkforward/.picks/.choices.csv`, carrying the pick's own `OOS_Sharpe` and a published
comparand column) and a pool file (`.grid/.arms/.ladder/.corpus/.sweep/.cells/.points.csv`).
Pool membership = pool rows agreeing on every shared cell key from a fixed allowlist.

| status | stems |
|---|---|
| OK | **91** |
| no `OOS_Sharpe` column | 93 |
| no sel/pool pair | 63 |
| no comparand column | 57 |
| no usable claim rows | 17 |

91 stems yield **29,630** (claim x comparand x pool_def) rows; 3,236 claim rows dropped for
pool < 3. Two parameters swept, all 4 points reported: comparand {CONTROL, SPY} x
pool_def {ALL, LIVE}.

## Q1 — how many claims sit over a negative-expectancy pool

| comparand | pool | n claims | stems | pool<0 | share | mean pool | mean sel | mean lift | t(lift) |
|---|---|---|---|---|---|---|---|---|---|
| CONTROL | ALL | 6656 | 83 | 2467 | **37.1%** | +0.2346 | +0.2794 | +0.0449 | +30.35 |
| CONTROL | LIVE | 6653 | 83 | 2467 | 37.1% | +0.2360 | +0.2796 | +0.0436 | +29.31 |
| SPY | ALL | 8328 | 90 | 2517 | **30.2%** | +0.0497 | +0.0863 | +0.0366 | +28.35 |
| SPY | LIVE | 7993 | 90 | 2516 | 31.5% | +0.0465 | +0.0830 | +0.0365 | +27.26 |

The pool's sign predicts the claim's sign in **76.5%** (CONTROL) / **89.8%** (SPY) of claims;
P(sel<0 | pool<0) = 46.9% / 76.6% against P(sel<0 | pool>=0) = 4.1% / 4.5%. The pool term
carries **72-79%** of a published claim's magnitude (|pool| / (|pool| + |lift|)); picking
skill carries the rest. `pool_def` (ALL vs LIVE) moves nothing: the record's null/control
rows are too few to shift a pool mean.

## Q2 — idea 204's regression, reported and explicitly NOT adjudicated

`sel_dOOS ~ a + b*pool_mean` gives b = +0.9503 (t +201), R2 0.859 (CONTROL/ALL) and
b = +0.9575, R2 0.796 (SPY/ALL); intercept a = +0.0565 / +0.0387 (t +30.8 / +29.5).
**This regression is near-ARITHMETIC and settles nothing on 204**: `sel_dOOS` and
`pool_mean_dOOS` subtract the same comparand by construction, so b = 1 + cov(lift, pool)/var(pool)
and R2 is high whenever lift is small relative to the spread of pool means. The informative
readings are the SIGN table and the |pool|/(|pool|+|lift|) share above, not the R2. Books inside
one stem are overlapping draws from one pool, so every pooled t here OVERSTATES significance.
Idea 204 remains OPEN and unrun.

## Q3 — RULE 8 / W1: the corpus walk-forward (this is what kills the screening reading)

Claims split by parent-script date; IS = dates < 2026-09-06 fitted, OOS = dates >= 2026-09-06
read once.

| comparand | pool | n IS | n OOS | IS agree | **OOS agree** | IS P(sel<0\|pool<0) | OOS same | IS b | OOS b |
|---|---|---|---|---|---|---|---|---|---|
| CONTROL | ALL | 4595 | 2061 | 85.6% | **56.1%** | 49.3% | 45.2% | +0.990 | +0.791 |
| CONTROL | LIVE | 4595 | 2058 | 85.6% | 56.1% | 49.2% | 45.2% | +0.977 | +0.788 |
| SPY | ALL | 5151 | 3177 | 88.7% | **91.6%** | 73.6% | 82.2% | +0.994 | +0.891 |
| SPY | LIVE | 5151 | 2842 | 88.7% | 91.2% | 73.6% | 82.2% | +0.979 | +0.898 |

Against SPY the sign relation is stable OOS (88.7% -> 91.6%). **Against a do-nothing CONTROL —
the comparand that actually matters for "does selection help" — it collapses from 85.6% to
56.1%, barely above a coin.** So "pool_mean < 0 therefore the claim will be negative" is NOT a
usable screening rule; the column's value is DISCLOSURE, not prediction. Limitation carried, not
buried: only **5 distinct parent dates** survive in `research/backtests/` (2026-09-04..08), so
this split is 2 days IS vs 3 days OOS, not a long record.

## Q4 — RULE 8 / W2: the column on a pool built fresh this run

u56, top-n equal-weight, no vol scaler, weekly, 10 bps, t+1; n in {10,15,20,25,30} x
g in {0.50,0.625,0.75,0.875,1.00} = 25 arms, all reported in `.livepool.csv`.
References from 2009-01-13: SPY 15.23% / 0.889 / -33.72% (OOS 15.45% / 0.882 / -33.72%);
RULES v2 8.66% / 1.206 / -12.05% (OOS 9.53% / 1.285 / -12.05%).
**KEEP paths over the pool: 4a 0/25, 4b 8/25** (all at g <= 0.75; the 4b passes are the gross
ladder's, consistent with idea 206 A).

IS-Sharpe selector picks n=15, g=0.875 -> OOS 20.90% / 1.169 / -23.21%. The SAME pick:

| comparand | comparand OOS Sharpe | sel_dOOS | **pool_mean_dOOS** | lift |
|---|---|---|---|---|
| do-nothing (n=20, g=0.75) | 1.120 | +0.0495 | **+0.0098** | +0.0397 |
| SPY | 0.882 | +0.2874 | **+0.2477** | +0.0397 |
| RULES v2 | 1.285 | -0.1156 | **-0.1553** | +0.0397 |

**One pick, one selector, one pool — and the published headline swings from +0.29 to -0.12
purely with the comparand, while the actual selection content (`lift = +0.0397`) is identical
in all three rows.** That is the case for the column in one table.

## Proposed clause (wording only; PROTOCOL.md and RULES.md untouched by this run)

> **PROTOCOL 10.** Any published claim that an IS selector's OOS result beats a comparand C MUST
> report, in the same row: `n(pool)`, `pool_mean_dOOS` = mean over the pool of
> `OOS_Sharpe(arm) - OOS_Sharpe(C)`, and `lift = dOOS(pick) - pool_mean_dOOS`. A claim with
> `pool_mean_dOOS < 0` is reported as an INSTRUMENT result; only `lift` may be described as
> selection. LEADERBOARD gains one column: `pool_mean_dOOS (n_pool)`.

Adoption is a Sunday-review decision (PROTOCOL 6), not this run's.

## Caveats carried

- The back-fill reads only what each parent COMMITTED. 230 of 321 stems cannot be back-filled
  at all (no pool file, no comparand column, or no `OOS_Sharpe`), so the 37.1% / 30.2% figures
  describe the reconstructable 91-stem subset, not the whole record.
- Cell-key matching is an allowlist join. Where a parent's pool file carries a grouping column
  the selector file does not, the pool is WIDER than the selector's true choice set and
  `pool_mean_dOOS` is biased toward the panel mean. `.stems.csv` publishes the join keys used
  for every stem so any single row can be checked.
- Claims within a stem are not independent; every pooled t-stat above overstates significance.
- The live pool (Q4) inherits the u56 current-constituent survivorship of `universe.json`;
  it is a demonstration of the column, not a capital claim.

# Idea 430 — back-fill `lift` beside every published selector claim (cloud, 2026-09-08)

**Verdict: ANSWERED / SPLIT.** The queue's count comes back **98.4–99.1%**: essentially every
published "selection helps" sentence in the record has a lift that is **indistinguishable from
zero** against the only null the object supplies. `lift` + `n_pool` + `p_two` are **ADOPTED as
report-only columns** (they are free — every input already sits in the parent script's own CSV).
The *screen* built on those columns is **KILLED**: it is an algebraic re-statement of `|lift|`, not
a filter. No book is promoted; **4a 0/25 arms, 4b 8/25 arms, and the walk-forward pick fails both.**

## What was actually new here
The back-fill itself was already committed — idea 205's census computes
`lift = sel_dOOS − pool_mean_dOOS` for every claim it recovers, and this run reproduces that column
to **4.441e-16 on 13,482 unambiguous shared keys (gate G1)**. What no script in the record had is a
**null**: "indistinguishable from zero" is undefined for a single number. This run supplies the one
null the object itself provides —

    RANDOM-PICK-FROM-THE-SAME-POOL.  Pool P = {a_1..a_n}, metrics M_i, mean mbar.  A selector
    picking a* has lift = M(a*) − mbar.  A selector picking UNIFORMLY AT RANDOM has lift
    distributed exactly as {M_i − mbar}, mean 0 by construction.  So

        p_two = (1/n) · #{ i : |M_i − mbar| ≥ |lift_obs| }      p_one = (1/n) · #{ M_i ≥ M(a*) }

    Exact, finite-population, zero fitted parameters, zero resampling.

**The consequence is arithmetic and it is the headline.** The pick is a member of its own pool, so
`p_two ≥ 1/n` always. A claim drawn from a pool of `n < 20` arms **cannot reach p < 0.05 whatever
its lift** — its falsifiability is decided by pool size before any performance number is read.

## Corpus
325 script stems in `research/backtests/`; 92 yield claims (94 lack an OOS_Sharpe column, 65 have no
selector/pool file pair, 57 no comparand column, 17 no usable rows). 4,168 (claim × pool_def) rows at
`MIN_POOL=3`, 3,236 dropped as thinner. **Median pool size 9 arms** (min 3, max 1,224).

## Gates
| gate | measure | result |
|---|---|---|
| G1 | `lift` vs idea 205's committed column, 13,482 unambiguous shared keys | max abs diff **4.441e-16** — PASS |
| G2 | comparand invariance, 5,969 rows carrying both comparands | `max \|lift(CONTROL) − lift(SPY)\|` = **0.000e+00**; `max \|sel_d(CONTROL) − sel_d(SPY)\|` = **1.2073** — PASS |

G2 is the premise idea 430 rests on, re-measured on a corpus 5× the size of idea 204's: the comparand
is worth up to **1.21 of Sharpe** and `lift` is worth **exactly none** of it.

## Q1/Q2 — the count the queue asked for (all 8 grid points; p1 pool_def, p2 MIN_POOL)
Of claims the record published as wins (`sel_dOOS > 0`):

| pool_def | MIN_POOL | n wins | lift ≤ 0 | **p₂ ≥ .05 (indistinguishable)** | unfalsifiable (n_pool < 20) |
|---|---|---|---|---|---|
| ALL | 3 | 3415 | 27.8% | **99.1%** | 54.5% |
| ALL | 5 | 3262 | 27.1% | **99.0%** | 52.3% |
| ALL | 8 | 2347 | 27.9% | **98.7%** | 33.7% |
| ALL | 12 | 2143 | 26.9% | **98.6%** | 27.4% |
| LIVE | 3 | 3231 | 28.4% | **96.6%** | 57.2% |
| LIVE | 5 | 2692 | 26.4% | **98.8%** | 48.6% |
| LIVE | 8 | 2163 | 27.0% | **98.5%** | 36.1% |
| LIVE | 12 | 1959 | 25.8% | **98.4%** | 29.4% |

Two further readings, stable across every grid point:

* **27–28% of published wins have `lift ≤ 0`.** The selector picked at or below its own pool's mean:
  the win belongs entirely to the instrument, and the sentence is an instrument result wearing a
  selector's clothes. This is idea 205's finding restated on the residual it left behind.
* **27–57% are unfalsifiable by construction.** Their pools are too small for any lift to reach
  p < 0.05. Only 1.4–3.3% of all claims actually clear it.

## Q3 — the pooled reading (the other half of the answer)
An individually-unfalsifiable corpus can still carry a jointly measurable mean, and it does:
**mean lift +0.0414 to +0.0501 of Sharpe, t +15.5 to +19.6**, positive in 66–69% of claims, at every
grid point. So the honest two-sentence verdict is: *selection helps in aggregate, and cannot be
demonstrated on any single published claim.* (The wins/losses split — +0.070/+0.092 vs
−0.017/−0.029 — is partly mechanical, since `sel_d ≡ pool + lift` and the split conditions on
`sel_d`; it is reported for completeness, not as evidence.)

## Q4 — rule 8, corpus walk-forward (split by parent script date, cut 2026-09-06, read once)
**W1a, the non-circular reading — the level persists.** Mean lift IS +0.0407 → OOS **+0.0421**
(ALL/3); LIVE/12 +0.0499 → **+0.0502**; win rate 66–69% → 65–67%. Every one of the 8 grid points
walks forward with essentially no decay.

**W1b, the screen — killed.** The screen "admit a claim iff p₂ < .05" shows an OOS admitted-minus-
rejected gap of **+0.1920 to +0.2884**. But `p₂` is a monotone function of `|lift|` *within a pool*,
so that gap is expected by construction, and the controls confirm it: admitting the same **number**
of claims on `|lift|` alone gives a **larger** gap (**+0.5514 to +0.6332**), and admitting the same
number at random gives **+0.000 ± 0.023** (200 seeded draws). The screen knows nothing `|lift|` does
not; it is a reporting convention and must not be sold as an out-of-sample filter.

**Stated limitation.** The corpus spans only **5 distinct parent dates (2026-09-04 … 2026-09-08)**,
so W1's "walk-forward" is a two-day split of the record's own recent output, not a decade. It tests
whether the statistic is stable across independently-written scripts, which is what it can test, and
nothing about market regimes. W2 below carries the market-time walk-forward.

## Q5/Q6 — rule 8 on fresh books, and both KEEP paths
u56, top-n equal-weight, no vol scaler, weekly, t+1, 10 bps; n {10,15,20,25,30} × g {0.50…1.00} =
**25 arms, all reported in `.arms.csv`**; arms fitted on 2010–2016 by IS Sharpe, 2017–2026 read once.

| book | full CAGR / Sharpe / MaxDD | H1 / H2 | OOS CAGR / Sharpe / MaxDD |
|---|---|---|---|
| IS-Sharpe pick **n=15, g=0.875** | 18.85% / 1.1508 / −23.21% | 1.215 / 1.117 | **20.90% / 1.1695 / −23.21%** |
| SPY | 15.23% / 0.8890 / −33.72% | 0.957 / 0.834 | 15.45% / 0.8820 / −33.72% |
| RULES v2 (live) | 8.66% / 1.2056 / −12.05% | 1.226 / 1.191 | 9.53% / 1.2851 / −12.05% |
| RULES v1 | 6.46% / 0.6647 / −13.83% | — | 7.73% / 0.7471 / −13.83% |

The pick with the proposed column attached: pool mean OOS Sharpe 1.1297 over n_pool 25,
**lift +0.0397, p_one 0.0800, p_two 0.2800 → INDISTINGUISHABLE** from a random draw of its own pool.
Its published `sel_d` is **+0.2874 vs SPY, −0.1156 vs RULES v2, +0.4224 vs RULES v1** — three
different sentences from one pick, and `lift` is the same number under all three. The pool is one of
the few in the record where p < 0.05 is even attainable (1/25 = 0.0400), and the pick still does not
reach it. Idea 204's K_MEDIAN arm (n=10, g=0.750) posts lift −0.0946, p_two 0.1200.

**KEEP paths: arms 4a 0/25, 4b 8/25. The walk-forward pick fails BOTH** — 4a on Sharpe against the
live book in both halves, 4b on drawdown (−23.21% against SPY's 60% bar of −20.23%). Idea 430 is a
reporting proposal and nominates no book; the paths are scored because PROTOCOL rule 4 requires it.

## Proposed wording (report-only; NOT a RULES change, for Sunday review)
> Beside any published selector claim, report `n_pool`, `lift = M(pick) − mean_P M(a)`, and the
> exact within-pool p-value `p_two = (1/n)·#{|M_i − mbar| ≥ |lift|}`. A claim with `n_pool < 20`
> is not falsifiable at α=0.05 and must not be written up as "selection helps"; a claim with
> `lift ≤ 0` is an instrument result and must not be written up as a selector result at all.
> `p_two` is a reporting column, never an admission filter.

Outputs: `.console.txt` `.claims.csv` (4,168 rows) `.stems.csv` `.census.csv` `.wins.csv`
`.walkforward.csv` `.arms.csv`.

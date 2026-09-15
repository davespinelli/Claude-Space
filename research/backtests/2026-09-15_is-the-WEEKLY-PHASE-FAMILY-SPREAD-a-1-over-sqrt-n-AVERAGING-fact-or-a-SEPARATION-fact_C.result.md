# Idea 975 (lane C, 2026-09-15) — is the WEEKLY PHASE FAMILY SPREAD small because of AVERAGING or because WEEKDAYS ARE ALIKE?

**ANSWERED = NEITHER STORY AS THE QUEUE PUT THEM. The spread is a SEPARATION × PHASE-COUNT
object and it does NOT scale as 1/sqrt(n_rebalances). KILL for the 1/sqrt(n) law.** Two books
that rebalance on calendars *s* trading days apart differ by an amount that depends on *s* and
**not** on how often they rebalance: at matched separation, a grid that rebalances **4× more
often** produces **1.053×** the dissimilarity, where averaging predicts 0.577. Once the phase
count and the available separation are both held fixed, the weekly family is **not small at
all** — every one of the eight grids lands in **1.51–1.83 pp**, a 1.21× spread against the
3.73× the record publishes. No RULES change, no KEEP, no book promoted; `RULES.md`,
`PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched (rule 6).

Script:
`2026-09-15_is-the-WEEKLY-PHASE-FAMILY-SPREAD-a-1-over-sqrt-n-AVERAGING-fact-or-a-SEPARATION-fact_C.py`
(`.grid.csv` 34,500 rows · `.pairs.csv` 78,780 · `.families.csv` 1,200 · `.windows.csv` 240 ·
`.matched.csv` 34 · `.walkforward.csv` 750 · `.hypotheses.csv` · `.console.txt`), 334.7 s.

## Gates — nine, all PASS, run before any hypothesis number was read
| gate | what | result |
|---|---|---|
| G0 | `offset_mask(·,per,0)` == `engine.rebalance_mask` on W/M/Q | 0 differing rows |
| G1 | `Ctx.run` == `engine.backtest` @10 bps, worst of W/M/Q | 2.082e-17 |
| G2 | BAND03 @0.75 == `rules_v2_weights` (the LIVE rules) | 0.000e+00 |
| G3 | **965's committed `grid.csv` replayed on 13,350 of 13,350 calendar rows**, 13 columns | max abs 3.553e-15 |
| G4 | determinism (TOP20 / K21 / phase 3 re-derived twice) | 0.000e+00 |
| G5 | RULES v2 weekly 8.6227%/1.2014/−12.0549% == `engine.backtest(freq='W')` | 2.220e-16 |
| G6 | **the fixed-interval grids partition the tape, equal rebalance counts, exact one-day translates** | clean on all 5 |
| G7 | pairwise tracking error via the covariance shortcut == direct `std(r_i − r_j)` | 3.469e-18 |
| G8 | Monte-Carlo phase-count factor `c_k` == the published SPC `d2` constants, k = 2…10 | max abs 0.0049 |

REPORTED, not a gate: today's cache differs from the record's published RULES v2 / SPY constants
by up to 1.494e-03 (data-cache drift); G3 pins the machinery, not the cache. **965's headline is
re-derived to the digit: median OOS CAGR family RANGE W 1.75 / M 3.09 / Q 6.53 pp** against its
published 1.75 / 3.09 / 6.53.

## The design (PROTOCOL rule 4: two tuned parameters)
TUNED 1 **grid**, 8 levels, all reported: the record's calendar `W` (5 phases) / `M` (21) / `Q`
(63), plus **fixed-interval** `K05` / `K10` / `K21` / `K42` / `K63` — rebalance every *K* trading
days, phase *d* ∈ 0…*K*−1. TUNED 2 **book set**, 2 levels: `RANKED` (TOP05/TOP10/TOP20) and
`SPREAD` (EWELIG/BAND03; BAND03 @0.75 **is** the live RULES v2 book), every book also reported on
its own. Reported axes, nothing fitted: panel U56 / B136 / SMALL, gross CORE 0.75 / EXT 1.00, cost
0/5/10/25/50 bps, window FULL / IS 2009–2016 / OOS 2017–2026.

**Why the fixed-interval grids exist.** In the record's three grids the two candidate causes are
perfectly confounded — W has both the most rebalances *and* the smallest possible separation. The
fixed-K grids break it: the matched-separation ratio D(K=5,*s*) / D(K=21,*s*) is **≈0.488 under
averaging and ≈1.00 under separation**, at the same *s*.

## The five bars
| bar | result | number |
|---|---|---|
| `H_SQRT` spread ∝ 1/√n_reb | **FAIL** | OLS slope of log SD on log n_reb = **−0.3366** (bar [−0.60, −0.40]) |
| `H_COUNT` the record's RANGE is SD × the phase-count factor | **PASS** | median (RANGE/SD)/c_k = **1.000** (bar [0.85, 1.15]) |
| `H_SEP` matched-separation ratio ≥ 0.85 | **PASS** | **1.0534** (\|ΔCAGR\| twin 1.0152); averaging predicted 0.5774 |
| `H_FLAT` D flat in separation | **FAIL** | D(K21, s=10)/D(K21, s=1) = **2.0199** (bar ≤1.25) |
| `H_TRUNC` weekly RANGE from the monthly D(s≤2) curve | **FAIL** | 57.7% error (bar 25%) — **its estimator is itself count-confounded, see below** |

## The record's own statistic would have "confirmed" the law, for the wrong reason
| grid | phases | rebal/yr | **RANGE** pp | **SD** pp | IQR pp | c_k | RANGE/SD |
|---|---|---|---|---|---|---|---|
| K63 | 63 | 4.0 | 6.677 | 1.746 | 2.555 | 4.681 | 3.905 |
| Q | 63 | 4.0 | **6.528** | 1.602 | 2.422 | 4.681 | 4.076 |
| K42 | 42 | 6.0 | 4.264 | 0.965 | 1.370 | 4.363 | 4.228 |
| K21 | 21 | 12.0 | 3.233 | 0.880 | 1.157 | 3.782 | 3.672 |
| M | 21 | 12.1 | **3.087** | 0.812 | 0.957 | 3.782 | 3.852 |
| K10 | 10 | 25.2 | 2.623 | 0.849 | 1.071 | 3.080 | 3.083 |
| K05 | 5 | 50.4 | 1.815 | 0.743 | 1.006 | 2.327 | 2.481 |
| W | 5 | 52.4 | **1.750** | 0.731 | 0.907 | 2.327 | 2.491 |

On the **RANGE** the slope is **−0.5346** — dead on the 1/√n law, and it is an artefact.
`H_COUNT` passes at **1.000**: the RANGE is the SD times the expected range of *k* draws and
nothing else. Of the 3.73× W→Q RANGE ratio the **phase count alone accounts for 2.01×**
(c₆₃/c₅ = 4.681/2.327) and the dispersion for 2.19×. **Any 1/√n test run on a RANGE compared
across grids with 12.6× different phase counts is testing two things at once.**

## The matched-separation cut settles it
Median pairwise OOS tracking error, same separation, grids whose rebalance counts differ 3–4×
(17 matched points, 15 families each, all published in `.matched.csv`):

| pair | rebal ratio | s | ratio observed | averaging predicts |
|---|---|---|---|---|
| K05/K21 | 4.2× | 1, 2 | 1.053, 0.948 | 0.488 |
| K10/K42 | 4.2× | 1…5 | 1.085, 1.088, 1.025, 0.975, 0.928 | 0.488 |
| K21/K63 | 3.0× | 1…10 | 1.100, 1.128, 1.133, 1.119, 1.137, 1.099, 1.039, 1.038, 0.993, 0.975 | 0.577 |

Median **1.0534**. Distance to the separation story **0.053**; to the averaging story **0.476**.
And averaging's second prediction — flatness in *s* — fails on **every** grid: D(s_max)/D(s=1) =
1.15 (K05) · 1.55 (K10) · **2.02** (K21) · 2.71 (K42) · **3.05** (K63). The horse race on all
**46,185** pairs:

| model | n_reb coefficient | separation coefficient | R² |
|---|---|---|---|
| log TE ~ log n_reb | **−0.2142** | — | 0.0106 |
| log TE ~ log separation | — | **+0.3177** | 0.1233 |
| log TE ~ both | **+0.0865** | **+0.3326** | 0.1247 |

Control for separation and the n_reb coefficient **changes sign**. The apparent 1/√n is the
separation axis written in the wrong variable: a *K*-day grid can only offer separations up to
*K*/2, so more rebalances mechanically means less reachable separation.

## The count-matched truncation test (POST-HOC, declared as post-hoc)
`H_TRUNC` failed as pre-registered (57.7%), and its estimator is a MAX over **41** monthly pairs
at *s* ≤ 2 against **10** weekly ones — the very inflation `H_COUNT` just measured, so that
failure is evidence about the estimator, not the question. The count-matched form: take every
window of *L* **consecutive** phases inside each family (L draws, ≤ L−1 days of separation, on
every grid) and measure its OOS CAGR range.

| grid | rebal/yr | L=3 window | L=5 window | full family RANGE |
|---|---|---|---|---|
| K63 | 4.0 | 1.094 | 1.578 | 6.677 |
| Q | 4.0 | 0.970 | 1.776 | 6.528 |
| K42 | 6.0 | 1.227 | 1.801 | 4.264 |
| K21 | 12.0 | 1.163 | 1.807 | 3.233 |
| M | 12.1 | 0.746 | 1.505 | 3.087 |
| K10 | 25.2 | 1.184 | 1.826 | 2.623 |
| K05 | 50.4 | 1.399 | 1.815 | 1.815 |
| W | 52.4 | 1.184 | 1.750 | 1.750 |

At L=5 the eight grids span **1.505–1.826 pp — a 1.21× spread against the record's 3.73×** — and
the slope on log n_reb is **+0.0186 (R² 0.0004)**. Held at equal draws and equal separation, a
quarterly family is no wider than a weekly one. **The weekly spread is not small; the weekly
family is just short.**

## Rule 8 walk-forward — grid and phase chosen on 2009–2016 only, 2017–2026 read once
| chooser | cells | OOS 4b | 4b pure | OOS 4a | OOS CAGR | OOS Sharpe | OOS MaxDD | turnover | rebal/yr |
|---|---|---|---|---|---|---|---|---|---|
| CANON_W (the live cadence) | 30 | 3 | 4 | 0 | 11.70% | 0.813 | −26.31% | 16.08× | 52.4 |
| IS_PHASE_W (1 free param) | 30 | 5 | 5 | 0 | 11.65% | 0.811 | −25.49% | 15.76× | 52.4 |
| IS_GRID_CANON (1 free param) | 30 | 3 | 3 | 0 | 12.26% | 0.807 | −31.37% | 4.87× | 10.3 |
| IS_GRIDPHASE (2 free params) | 30 | 1 | 1 | 0 | 13.13% | 0.790 | −31.87% | 4.06× | 4.8 |
| **MAXREB_CANON** (this idea's rule, no IS read) | 30 | **6** | 8 | **2** | 12.58% | **0.853** | **−24.68%** | 15.58× | 50.4 |

SPY OOS **15.27% / 0.874 / −33.72%**; live RULES v2 OOS (mean over panels) **7.03% / 0.981 /
−12.73%**. Choosing *more* in sample buys *less* out of sample — the two-parameter chooser lands
at **1 of 30**, the parameter-free maximum-rebalance control at 6 — which is 953's and 962's
result reproduced on a new dial. **0 of 150 picks clear BOTH KEEP paths.** Best pick by OOS
Sharpe, `U56/BAND03/CORE → K05 phase 0`: OOS **9.56% / 1.283 / −12.06%** vs SPY OOS 15.27% /
0.874 / −33.72% and live RULES v2 OOS 9.46% / 1.277 / −12.05% — **fails 4b on `L5_CAGR` alone**
(full 8.64% / 1.199 / −12.06%, halves 1.217 / 1.187), on a family where **0 of 5 phases** pass.

Per 965's standing requirement, the 18 picks that do clear 4b are quoted with their own family's
blind base rate: **median 0.900**, and **14 of 18 (0.778)** sit on a family a coin clears at least
a quarter of the time (nine at 1.000). Across the whole grid at 10 bps the 4b pass rate rises
monotonically with cadence — K63 0.035 · K42 0.038 · K21 0.078 · M 0.081 · K10 0.160 · K05 0.167 ·
W 0.147 — and **inverts by 50 bps** (K05 0.033 against M 0.044) as turnover climbs 3.5 → 15.6 ×/yr.
That is 943's turnover rebate, not an edge.

## Capital verdict
**KILL** for "the phase-family spread scales as 1/√n_rebalances". It scales with the **separation
the grid can reach** and with the **number of phases the family contains**, and neither is an
averaging effect. Nothing here is capital-worthy: 0 of 150 rule-8 picks clear both paths, the best
fails 4b's CAGR floor, and the one cadence that looks better at 10 bps loses at 50.

**One standing fact for the record, proposed for Sunday review and NOT written into
`PROTOCOL.md` (rule 6):** *"A phase-family spread is quoted as an SD, or as a RANGE beside its own
phase count. A bare RANGE compared across grids with different phase counts is not a comparison:
of the record's published 1.75 / 3.09 / 6.53 pp, a factor of 2.01× is the phase count alone."*
This touches every committed claim that reads a spread across cadences — 963's required-companion
statistic and 965's "W is the one steerable dial" among them, the latter of which reads, after
correction, as **"W is the one truncated dial."**

SURVIVORSHIP (rule 9): U56 / B136 / SMALL are current-constituent lists (SMALL additionally drops
every ticker with `max_1d_move` ≥ 1.0 per `data/small_meta.csv`); every CAGR / Sharpe / DD level
above is optimistic. Every contrast here is same-tape, same-universe, same-weights and differs
only in which day the identical book rebalances, so the spread, ratio and scaling statistics are
unaffected by panel composition; the 4b levels are read against SPY, so a survivor panel makes 4b
failures RARER — every failure reported here is, if anything, understated.

# Idea 147 — scale-free-as-a-corpus-eligibility-rule (lane C, 2026-09-05)

**ANSWERED — KILL of the pre-registered hypothesis; a clean POSITIVE for one of the two
instruments.** Relative units do **not** make the corpus rescale-safe. They fully repair the
turnover budget and only half-repair the drawdown trigger, because the residual is not a units
problem at all — it is a threshold-crossing problem, and no change of units removes it.

Script: `2026-09-05_scale-free-as-a-corpus-eligibility-rule_C.py`
(`--panel u56|broad|small` computes and caches one panel's grid; no argument runs the analysis).
14,400 backtests = 18 cells (3 panels x 3 books x 2 cost rungs) x 32 arms x 25 gross points.

## Reproduction (all four pass before any new number is read)

| check | result |
|---|---|
| (a) `run2` vs idea 94's `H.run`, 6 instrument settings at m=0.55 | max\|diff\| **0.00e+00** |
| (b) `run2` control vs `engine.backtest`, ungated EWall u56 | max\|diff\| **0.00e+00** |
| (c) idea 144's Q1 census on the ABS arms | n=**72**, CAGR monotone **27/72**, \|MaxDD\| monotone **35/72**, max Sharpe range **0.2924** — all exact |
| (d) REL-M == ABS at m=1.00, 4 pairs x 4 metrics x 18 cells | max\|diff\| **0.00e+00** |

PURE yardstick on this run's 4 scale-free arms (n=72): CAGR monotone 70/72, \|MaxDD\| monotone
72/72, max Sharpe range **0.0126** (idea 144's full 234-book PURE class: 228/234, 234/234, 0.0130).

## Q1 — the answer: the repair is real but partial, and it splits by instrument

Pre-registered bar (fixed before any number was read): **(S1)** max Sharpe range over the gross
family < 0.05 **and** **(S2)** both monotonicity counts >= 90% of books.

| family | n | median range | max range | CAGR monotone | \|MaxDD\| monotone | S1 | S2 |
|---|---|---|---|---|---|---|---|
| **PURE** (yardstick) | 72 | 0.0024 | **0.0126** | 70/72 (97%) | 72/72 (100%) | — | — |
| **ABS** (published) | 72 | 0.1306 | **0.2924** | 27/72 (38%) | 35/72 (49%) | FAIL | FAIL |
| **REL-M** (analytic `D x m`, `B x m`) | 72 | 0.0086 | **0.1325** | 63/72 (88%) | 71/72 (99%) | **FAIL** | **FAIL** |
| **REL-V** (`D_t = c x vol_L`, all 10 grid points) | 360 | 0.0280 | **0.1461** | 295/360 (82%) | 338/360 (94%) | **FAIL** | **FAIL** |

**The split by instrument is the result**, and it is unambiguous:

| instrument | units | median range | max range | CAGR mono | \|MaxDD\| mono |
|---|---|---|---|---|---|
| `ebud` turnover budget | absolute | 0.0160 | 0.1722 | 27/36 | 30/36 |
| `ebud` turnover budget | **fraction of gross** | **0.0029** | **0.0100** | **35/36** | **36/36** |
| `ddctl` drawdown trigger | absolute 8% | 0.1924 | 0.2924 | **0/36** | 5/36 |
| `ddctl` drawdown trigger | **relative (`D x m`)** | 0.0293 | 0.1325 | 28/36 | 35/36 |

The budget lands **inside the PURE yardstick on every statistic** (max 0.0100 vs PURE's 0.0126;
median 0.0029 vs 0.0024). It is repaired, completely. The trigger's median damage falls 85%
(0.1924 -> 0.0293) and CAGR monotonicity goes from 0/36 to 28/36, but its worst case stays
**10x the PURE yardstick**, and the same is true at every one of the 10 `c x L` grid points.

Matched pairs, the same rule in two unit systems (18 cells each):

| rule | max range abs -> rel | CAGR mono abs -> rel | \|MaxDD\| mono abs -> rel |
|---|---|---|---|
| `ddctl-8/recover` | 0.2664 -> 0.1325 | 0 -> 14 | 2 -> 17 |
| `ddctl-8/high` | 0.2924 -> 0.0703 | 0 -> 14 | 3 -> 18 |
| `ebud-0.10` | 0.1722 -> **0.0089** | 12 -> **18** | 14 -> **18** |
| `ebud-0.20` | 0.1479 -> **0.0100** | 15 -> 17 | 16 -> **18** |

**Why the trigger cannot be fixed by units.** Both parameterisations remove the *systematic*
part of the failure (an 8% trigger on a half-gross book is unreachable; a vol-scaled or
m-scaled trigger is reached at the same point of the same drawdown). What survives is the
*threshold-crossing* part: `run()`'s drift renormalisation shares the book with cash, so a
rescaled book is not exactly `m x` the original path, and a state machine amplifies an
arbitrarily small path difference into a whole episode fired or not fired. The `c` sweep is the
direct evidence — the residual tracks firing frequency, not units:

| c | mean episodes/book | max Sharpe range | median range |
|---|---|---|---|
| 0.4 | 15.0 | 0.1220 | 0.0305–0.0426 |
| 0.7 | 6.3 | 0.1083 | 0.0336–0.0595 |
| 1.0 | 3.0 | 0.0933 | 0.0186–0.0426 |
| 1.3 | 1.7 | 0.1461 | 0.0089–0.0262 |
| 1.6 | 1.1 | 0.0942 | **0.0050–0.0100** |

At c=1.6 the instrument fires about once in 17 years, the *typical* book is inside the PURE
yardstick (median 0.005–0.010) and the worst one still swings 0.094 — i.e. the only drawdown
trigger that approaches scale-freedom is one that barely triggers, and even that leaves a tail.
All 20 REL-V arms (5 c x 2 L x 2 resets) are reported in `.cLgrid.csv`; none clears S1.

## Q2 — the corpus consequence: the repair changes essentially nothing

| family | books | POINT-4b | POINT-4a | FAMILY-4b m<=1.00 | FAMILY-4b m<=1.30 |
|---|---|---|---|---|---|
| PURE | 72 | 4 | 25 | 13 | 16 |
| ABS | 72 | 1 | 26 | 10 | 17 |
| REL-M | 72 | 1 | 26 | 10 | 16 |
| REL-V | 360 | 10 | 125 | 41 | 66 |

Across the 144 matched pair-verdicts (4 rules x 2 ceilings x 18 cells) the repair flips
**1 to pass and 2 to fail** — all three on `ddctl` at m<=1.30, none on `ebud`. Admitted-set OOS
quality is indistinguishable: mean OOS Sharpe **1.118 (ABS)** vs **1.096 (REL-M)** vs 1.107
(PURE), MaxDD -18.5% vs -19.3% vs -19.0%. **No book is promoted by this run** — it
re-parameterises an existing corpus; the object adjudicated is the eligibility rule.

## Q3 — rule 8 walk-forward (params on 2009–2016 only; OOS 2017–2026 read once)

Three matched selectors, each over 4 arms x 25 m, IS-4b screen then argmax IS Sharpe:

| selector | OOS CAGR | OOS Sharpe | OOS MaxDD | m-regret | paired (7 cells) CAGR / Sharpe / MaxDD | beat SPY | beat v1 |
|---|---|---|---|---|---|---|---|
| A ABS | 8.4% | **0.709** | -21.2% | 0.097 | 12.9% / **1.030** / -22.7% | 6/18 | 12/18 |
| B REL-M | 9.4% | 0.682 | -25.8% | 0.095 | 13.8% / **1.033** / -23.8% | 6/18 | 12/18 |
| C REL-V (c=1.0, L=60) | 9.7% | 0.671 | -26.6% | 0.092 | 13.8% / 1.000 / -25.2% | 6/18 | 12/18 |

Controls on the same 18 cells: no-instrument `control` at m=1.00 **10.65% / 0.762 / -27.4%**;
live RULES v1 **4.86% / 0.451 / -25.3%**; SPY **15.45% / 0.882 / -33.7%**.

**Relative units buy nothing out of sample.** The three selectors are within 0.033 of OOS Sharpe
of each other and all three sit below the no-instrument control (0.762) and below SPY. Paired
m-pick regret does fall (0.066 -> 0.043) — the one place closure pays, and it is bought back by
1.1pp of extra drawdown. IS->OOS Spearman across the 25 m of the picked arm is **negative** for
every selector (-0.36 / -0.11 / -0.12), and mean \|m error\| is 0.56–0.60 of gross: choosing m in
sample is worthless under either unit system, which is the fourth independent confirmation of
idea 66's Sharpe-neutral-gross finding.

## Verdict and PROTOCOL consequence

**KILL** of "relative units make the whole corpus rescale-safe". The corpus goes from
**234/306 (76%)** rescale-safe to **270/306 (88%)** — the 36 `ebud` books join, the 36 `ddctl`
books do not. Idea 144's restriction has to stay in the convention's wording, but it can be
stated far more precisely and it now costs 12% of the corpus rather than 24%:

> PROTOCOL (proposed amendment to idea 144's convention, one clause): a static rescaling of a
> book counts as the same book only where every instrument's parameters are stated in units
> that scale with the book AND no instrument carries a **path-dependent state** (a trigger,
> stop or regime latch). Budgets, caps and fractions qualify once written as a fraction of
> gross; drawdown triggers never do, whatever their units, and books carrying one must be
> scored at their published gross only.

No RULES change. No new KEEP. Nothing promoted.

## Caveats

Survivorship (idea 54): all three panels are current-constituent lists. Idea 128: the IS
window's SPY MaxDD is shallower than the OOS window's, so every IS drawdown cap admits too much
— this biases all three selectors identically. Ideas 38 (calendar-day index on u56/broad) and
126 (t+1 only) carry over. `stop15` is in the PURE yardstick here and is itself a per-name state
machine; it is scale-free in *units* (a 15% per-name price stop does not depend on book gross),
which is why it closes (0.0094) where `ddctl` does not — the state that matters is the one read
off **book equity**, the quantity the rescale changes.

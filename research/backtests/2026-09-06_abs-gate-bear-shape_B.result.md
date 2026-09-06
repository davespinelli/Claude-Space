# Idea 62 — abs-gate-bear-shape — **KILL** (lane B, 2026-09-06)

**Question.** Idea 4 saw the `abs` (12-1 > 0) gate cut 2022 by ~2.3pp vs the `200d` gate
in the ranked book while giving 1.3-3.6pp back in 2020. Is that the *shape* of the two
instruments — `abs` for the SLOW bear, `200d` for the FAST crash?

**Answer: no. It was one episode, not a class.** The queued claim (d(abs-200d) > 0 in
SLOW and < 0 in FAST) holds in **7 of 36** (threshold x split x panel x book) cells, and
in **0 of 4** at the point the queue names (>10% episodes, 60-day split). All 7 passes sit
at the 15% threshold, which leaves only 5 episodes, and 6 of the 7 are on `broad`.
No KEEP-candidate, no RULES change: **4a 0 of 56 grid points, 4b 42 of 56** (shared by
almost every arm including the un-gated control, so it separates nothing).

Script `2026-09-06_abs-gate-bear-shape_B.py`; harness analytic-cost identity **0.000e+00**
against a real `cost_bps=10` run. Universe.json (56) and universe_broad.json (136), both
fully reported; weekly, 75% gross, next-day execution, 5/10/25/50 bps, verdicts at 10.
SURVIVORSHIP: current constituents on both lists, so absolute CAGR/Sharpe are optimistic;
the gate-vs-gate contrasts here are far less exposed (same names, same days, every arm).

## PART 1 — the descriptive test the queue asked for

Nine SPY peak-to-trough episodes deeper than 10% since 2009. `abs` minus `200d` on
peak-to-trough return, pooled over the 4 panel x book cells (positive = `abs` loses less):

| peak | dur (d) | class | mean d | min | max |
|---|---|---|---|---|---|
| 2009-01-06 | 42 | FAST | **+1.83%** | +0.47% | +4.54% |
| 2010-04-23 | 49 | FAST | -0.51% | -1.47% | +0.00% |
| 2011-04-29 | 108 | SLOW | -0.78% | -2.00% | -0.20% |
| 2015-07-20 | 143 | SLOW | **-2.38%** | -2.88% | -1.79% |
| 2018-01-26 | 9 | FAST | +0.27% | +0.00% | +0.75% |
| 2018-09-20 | 65 | SLOW | -1.50% | -2.56% | -0.25% |
| 2020-02-19 | 23 | FAST | **-2.67%** | -4.04% | -1.57% |
| 2022-01-03 | 195 | SLOW | **+1.13%** | +0.35% | +1.73% |
| 2025-02-19 | 34 | FAST | -0.17% | -0.77% | +0.15% |

`abs` wins **3 of 9** episodes, and only **1 of 4** SLOW ones — the 2022 episode idea 4
started from. The other three SLOW bears run the other way, 2015 hardest. The FAST half
is likewise mixed: 2020 is the claim's best evidence (-2.67pp) but 2009 is its worst
counterexample (+1.83pp). At the queued point the u56 sign is **inverted**: d_FAST
+0.00%/+0.08% and d_SLOW **-1.32%/-1.59%**, i.e. `abs` is worse in slow bears there.
(Caveat: the 2009-01-06 peak is a sample-start artefact — the true GFC peak is 2007,
before the panel — so that episode's duration and depth are truncated. Dropping it makes
the SLOW half worse for `abs`, not better; it is the claim's single best FAST result.)

Per-class means for all five gates at every grid point are in `.classes.csv`; the
per-episode x per-arm returns in `.episodes.csv`; console in `.console.txt`.

## PART 2 — the actionable version, and why it was needed

An episode's peak-to-trough duration is only known at the trough, so a class-conditional
rule cannot be traded. The only real-time form is a **speed switch**: run `abs`, flip to
`200d` while SPY's drawdown-to-date exceeds DEPTH and has accrued faster than SPEED per
day since the running peak (SPY-only, lagged one day). Exactly 2 tuned params, 3x3 grid,
all 36 cells x 4 panel-book combinations reported in `.grid.csv`.

It is worth roughly nothing. Best switch cell vs its best parent gate, @10bps Sharpe:
broad/top20 **+0.008** (9/9 cells beat both parents), broad/ew-all **+0.003** (3/9),
u56/ew-all **+0.001** (2/9), u56/top20 **-0.033** (0/9). On u56/top20 the switch's MaxDD
is worse than *both* parents in 9/9 cells (-18.53% vs -18.31% / -18.42%): blending on the
fast/slow axis buys neither parent's drawdown. The switch fires on 0.6%-9.8% of days
depending on the dial; the tightest cell (0.12/0.0060) fires on 25 days, all in 2020, and
is a 2020 overlay rather than a rule. Cost ladder: the ordering is unchanged at 5/25/50
bps, and every switch cell decays with cost at its parents' rate.

## Rule 8 walk-forward (both dials on 2009-2016 by IS Sharpe, 2017-2026 read once)

| panel/book | IS pick | OOS Sharpe | plain `abs` | plain `band3` | SPY | RULES v2 |
|---|---|---|---|---|---|---|
| u56/top20 | `200d` | 1.168 | 1.144 | **1.215** | 0.882 | 1.285 |
| u56/ew-all | switch 0.05/0.0030 | 1.088 | 1.111 | **1.232** | 0.882 | 1.285 |
| broad/top20 | `200d` | 0.892 | 0.888 | **0.900** | 0.882 | 1.119 |
| broad/ew-all | `band3` | 1.071 | 1.082 | 1.071 | 0.882 | 1.119 |

The chooser picks a switch cell in **1 of 4** cells and there it **loses -0.023 OOS Sharpe
to plain `abs`**. Mean OOS of the IS pick 1.055 vs **1.105 for always holding `band3`** and
1.056 for always holding `abs` — selection over this arm set loses to doing nothing, the
12th such instance in the record. Spearman(IS,OOS) +0.922 / +0.299 / +0.244 / +0.560.

## What to take from it

The 2022-vs-2020 pattern idea 4 flagged is real but is two episodes, not an instrument
property; there is no duration class in which one gate reliably dominates. Nothing here
argues for changing which gate the live rules hold — and the OOS table says the incumbent
band gate (RULES v2's clause 2) beats both instruments in 3 of 4 cells anyway. Do not
re-open the fast/slow axis without a longer episode sample than 9.

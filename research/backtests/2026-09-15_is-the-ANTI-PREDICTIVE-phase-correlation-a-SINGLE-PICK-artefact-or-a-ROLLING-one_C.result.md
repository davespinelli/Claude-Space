# Idea 965 (lane C, 2026-09-15) — is the ANTI-PREDICTIVE phase correlation a SINGLE-PICK artefact or a ROLLING one?

**ANSWERED = IT IS A SINGLE-PICK ARTEFACT IN ITS *SIGN* AND A PROPERTY OF THE DIAL IN ITS
*MAGNITUDE*. Re-choosing the rebalance phase every January moves the one-year-ahead rank
correlation from −0.057 to −0.028 (EXPAND) / +0.000 (ROLL8) — it removes the anti-prediction
and buys NOTHING in its place. KILL for annual phase re-choice.** No RULES change, no KEEP,
no memo, no book promoted; `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py`
untouched (rule 6).

Script: `2026-09-15_is-the-ANTI-PREDICTIVE-phase-correlation-a-SINGLE-PICK-artefact-or-a-ROLLING-one_C.py`
(`.grid.csv` 13,350 rows · `.walkforward.csv` 1,890 · `.prediction.csv` 1,350 · `.families.csv` 45
· `.hypotheses.csv` · `.console.txt`), 204.9 s.

## Gates — eight, all PASS, run before any hypothesis number was read
| gate | what | result |
|---|---|---|
| G0 | `offset_mask(·,per,0)` == `engine.rebalance_mask` on W/M/Q | 0 differing rows |
| G1 | `Ctx.run` == `engine.backtest` @10 bps, worst of W/M/Q | 2.082e-17 |
| G2 | BAND03 @0.75 == `rules_v2_weights` (the LIVE rules) | 0.000e+00 |
| G3 | **962's committed `grid.csv` replayed on 12,600 of 12,600 rows**, 13 columns | max abs 1.776e-15 |
| G4 | determinism (TOP20 / M / phase 3 re-derived twice) | 0.000e+00 |
| G5 | RULES v2 weekly 8.6227%/1.2014/−12.0549% == `engine.backtest(freq='W')` | 2.220e-16 |
| G6 | **causality**: 0 choosing-window days on/after their own cut; 0 of 8 pick sequences moved when the post-cut tape was permuted | 0 / 0 |
| G7 | **the composite machinery with a CONSTANT sequence reproduces its own phase-0 grid row** on 135 cells | 0.000e+00 |

REPORTED, not a gate: today's cache differs from the record's published RULES v2 / SPY constants
by up to 1.494e-03 (data-cache drift); G3 pins the machinery, not the cache.

## The design (PROTOCOL rule 4: two tuned parameters)
TUNED 1 **re-choice cadence**, 3 levels, all reported: `STATIC` (962's single 2009–2016 pick),
`EXPAND` (re-pick each January on everything up to that January), `ROLL8` (same, on the trailing
8 years only — separating *fresher* from *longer*). TUNED 2 **grid**, 3 levels: `W` (5 phases,
never read before), `M` (21), `Q` (63). Reported axes, nothing fitted: chooser C_CAGR / C_SHARPE /
C_CALMAR / C_DDMIN, book TOP05 / TOP10 / TOP20 / EWELIG / BAND03, panel U56 / B136 / SMALL, gross
CORE 0.75 / EXT 1.00, cost 0/5/10/25/50 bps (grid) and 0/10/25 (re-choice machinery). Controls:
CANONICAL (phase 0), FAMILY mean, ORACLE_ANNUAL (hindsight-best phase *each year* — the ceiling of
the annual dial). **The rolling book is run as a book**: one composite rebalance mask trades phase
p(Y) on the days of year Y, through the engine-verified runner, so every switch pays its real
turnover (G7). Rule 8 throughout: before 2017 the composite trades the canonical phase, and every
pick for year Y is made on days that end before 1 January Y (G6).

## The answer: freshness removes the minus sign and adds no plus
Median within-family Spearman(window CAGR rank, **NEXT-YEAR** CAGR rank), 450 (family, year) pairs
at 10 bps — all three estimators scored against the **same** target:

| grid | STATIC (stale) | EXPAND (freshest) | ROLL8 (fresh, fixed memory) |
|---|---|---|---|
| M | −0.042 | −0.097 | −0.110 |
| Q | −0.038 | −0.021 | **+0.044** |
| W | −0.100 | **+0.100** | **+0.100** |
| **pooled** | **−0.057** | **−0.028** | **+0.000** |

**H_FRESH FAILS** at −0.028 against its +0.30 bar. **H_STALE FAILS**: on the same year target a
fresh window beats the stale one in only **0.427** of pairs (ROLL8 0.462, bar 0.60), and at the
**book** level the rolling book beats its own stale pick in **0.467** of 360 pairs, worth
**+0.029 pp** of OOS CAGR and +0.0123 of OOS Sharpe. Interquartile range of the fresh correlation
is [−0.300, +0.258] and 36.2% of pairs sit inside ±0.20: this is a **zero**, measured ten different
ways, not a positive number waiting for a better window.

962's own statistic is **reproduced exactly** — median ρ(IS CAGR, OOS CAGR) = **−0.153** on M+Q
over 45 families here vs its published −0.153 over 30. Extending it to the weekly grid for the
first time: **W = +0.100** (Sharpe +0.200), the only non-negative grid — but W's median OOS CAGR
family spread is **1.75 pp** against M's 3.09 and Q's 6.53, so the one steerable-looking dial is
also the one with almost nothing on it. **H_WEEK FAILS** at +0.100 against +0.30.

## Does re-choosing pay? (verdict rung 10 bps, CORE gross)
| source | cells | OOS 4b PASS | OOS 4a | mean OOS CAGR | vs CANONICAL | vs FAMILY MEAN | turnover |
|---|---|---|---|---|---|---|---|
| CANONICAL | 45 | 4 (0.089) | 0 | 10.56% | — | −0.581 pp | 7.70×/yr |
| STATIC (962's pick) | 180 | 15 (0.083) | 1 | 10.74% | +0.181 pp | −0.400 pp | 7.64×/yr |
| EXPAND | 180 | 19 (0.106) | 1 | 10.62% | +0.058 pp | −0.523 pp | 7.64×/yr |
| ROLL8 | 180 | 28 (0.156) | 0 | 10.92% | +0.362 pp | −0.219 pp | 7.64×/yr |
| ORACLE_ANNUAL (hindsight) | 45 | 12 (0.267) | 4 | **18.89%** | **+8.332 pp** | +7.751 pp | 7.51×/yr |

**H_ROLLPAY FAILS**: the rolling book's OOS CAGR beats the canonical's in **0.489** of 360 cells
(bar 0.60) and beats the **family mean** in only 0.464, mean −0.371 pp. Re-choosing costs nothing
in turnover (7.64 vs 7.70 ×/yr) — the failure is informational, not frictional. The grid split is
the tell: rolling "wins" +2.77 pp on Q and loses −1.48 pp on M, exactly tracking where the canonical
phase sits low inside its own family (942's quarter-end result), not where the chooser found
anything. The annual dial is worth **+8.33 pp of OOS CAGR** in hindsight and **no causal rule
collects any of it**.

## The one supported bar is a null draw
**H_ROLL4B is SUPPORTED, and should not be believed.** Rolling clears 4b in 47 of 360 cells
(0.131) against the canonical's 0.089 — but a coin picking phases blindly on those same cells
clears it **41.19 times (sd 3.71)**: observed 47 is **+1.57 sd**, `P(X ≥ 47 | blind) = 0.0780`.
The null-draw audit finishes it: of the 47 passing cells, the **median own-family base rate is
0.600** and **37 of 47 (0.787)** sit on a family whose own coin flip clears 4b at least a quarter
of the time (29 at least half; U56/TOP20/W and U56/EWELIG/W pass at **every** one of their 5
phases). The best rolling cell by OOS Sharpe — U56/BAND03/Q/C_DDMIN/ROLL8, seq
`40,40,40,19,15×6`, OOS **10.74% / 1.306 / −13.98%** vs SPY OOS 15.27% / 0.874 / −33.72% and live
RULES v2 OOS 9.46% / 1.277 / −12.05% — clears 4b on both conventions with a **CAGR-floor margin of
+0.153 pp** on a family where 16 of 63 phases pass anyway. That is a lottery ticket, not a book.

## 4a, and the one thing the weekly grid did add
4a is dead as usual: **0 of 45** canonical and **0 of 180** ROLL8 cells at 10 bps; the only two
rule-8-reachable 4a passes in the whole run are **B136/BAND03/W/C_DDMIN** (STATIC phase 3 and
EXPAND 3→2) — i.e. the *live rules traded on a different weekday* — beating the same book's
canonical twin by **+0.030 / +0.060** of OOS half-Sharpe on a family whose entire OOS CAGR spread
is **0.49 pp**, and **all 5 of its phases fail 4b's CAGR floor** by ~2.6 pp. Across all rungs:
19 of 1,890 composite cells and 37 of 13,350 grid rows pass 4a, 12 of the 19 belonging to the
hindsight oracle. Nothing here is capital-worthy, and **no cell passes 4a and 4b together**.

## Capital verdict
**KILL.** Annual re-choice of the rebalance phase is not a repair to 962's finding — it removes the
anti-prediction and replaces it with nothing, at a coin-flip hit rate against the canonical and a
below-family-mean CAGR. 962's operational convention stands **unchanged and now on firmer ground**:
trade the canonical period-end phase and publish the family spread beside every phase-sensitive
claim. One new standing fact for the record: **a 4b pass produced by any phase-choosing rule must
be quoted with its family's own blind base rate** — 78.7% of the passes this run generated are
draws from families a coin clears just as often.

SURVIVORSHIP (rule 9): U56 / B136 / SMALL are current-constituent lists; every level above is
optimistic. Every contrast here (rolling vs static vs canonical vs family mean) is same-tape,
same-universe, same-weights and differs only in which day the identical book trades, so the
correlation and pass-rate comparisons are unaffected; the 4b levels are read against SPY, so a
survivor panel makes 4b failures RARER — every failure reported here is, if anything, understated.

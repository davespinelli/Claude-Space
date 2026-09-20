# Idea 2054 (lane cloud, 2026-09-20) — DOES THE DUAL-PATH KEEP-CANDIDATE SURVIVE THE SPRINT'S FOUR STANDING STRESS AXES AT ONCE?

**ANSWERED — SPLIT. The 4b leg is ROBUST (36 of 36 stress points, 100.0%). The 4a leg is a
DISCOVERY-SETTINGS ARTEFACT (8 of 36, 22.2%): it dies at 0 of 18 under one extra day of execution
latency, 0 of 12 at 50 bps, and 0 of 12 at two of the five weekday phases. Idea 2034's "dual-path"
claim is hereby RESTATED as a 4b KEEP-candidate with a fragile 4a leg.**

Script `research/backtests/2026-09-20_dualpath-four-axis-stress_cloud.py`; evidence
`.grid.csv.gz` (15,120 scored rows over 5,040 books), `.candidate.csv`, `.axes.csv`,
`.axes_corpus.csv`, `.census.csv`, `.walkforward.csv`, `.gates.csv`, `.log.txt`, `.console.txt`.

## What was priced

The vol-target corpus on the FULL cross of the four standing stress axes:

| axis | rungs | status |
|---|---|---|
| PANEL | U56, B136, SMALL665 | reported |
| TARGET `t` | 0.08, 0.10, 0.12, 0.16, 0.20 | **tuned dial 1** (inherited from 1799/2022/2034) |
| DIAL | DRIFT `h` in 10 rungs + CALENDAR `R` in {D, W, M, Q} | **tuned dial 2** (inherited) |
| CADENCE `T` | W, M | reported |
| PHASE | ENGINE (`engine.rebalance_mask`, the convention every committed book was run on) + five rungs moving only the day you LOOK: weekday p for W, the {1,5,10,15,20}-th trading day of the month for M/Q | reported |
| DELAY | t+1 (protocol base), t+2 | reported |
| COST | 10, 25, 50 bps | reported |

3 x 5 x 14 x 2 x 6 x 2 = **5,040 books**, x 3 cost rungs = **15,120 scored cells**. Nothing new is
tuned. Baselines are held at the LIVE convention throughout (RULES v2 weekly t+1 at 10 bps, and
SPY buy-and-hold), because a delayed, expensive idea must beat the undelayed, live book to be
worth switching to.

## Gates — 8 of 8 pass

| Gate | Value |
|---|---|
| G0 sample >= 10y | 18.7y |
| G1 the ENG phase rung IS `engine.rebalance_mask('W')` on every panel | 0.000e+00 |
| G2 DRIFT h=0 == CALENDAR R=D at every (t, cadence, phase, delay) | 0.000e+00 |
| G3 the four-axis grid is complete | 5,040 books / 15,120 rows |
| G4 gross never levered | max 1.000000 |
| G5 reproduces idea 2034's candidate at its discovery settings | max abs d = 8.327e-17 |
| G6 reproduces the standing VOLTGT memo (U56 + B136) at the discovery phase | max abs d = 4.605e-05 |
| G7 the DELAY axis actually moves the book | mean abs dSharpe t+1 -> t+2 = 0.0136 |

The PHASE axis is real, not five copies of one mask: weekly trade days per rung on U56 are
ENGINE 977, MON 882, TUE 969, WED 967, THU 948, FRI 942.

## V1 / V2 — THE CANDIDATE AT ALL 36 (COST x DELAY x PHASE) POINTS

| | 4a kept | 4b kept |
|---|---|---|
| **all 36 points** | **8 / 36 = 22.2% -> ARTEFACT** | **36 / 36 = 100.0% -> ROBUST** |
| weekday rungs only (ENGINE excluded) | 6 / 30 | 30 / 30 |
| by cost: 10 / 25 / 50 bps | 4/12, 4/12, **0/12** | 12/12, 12/12, 12/12 |
| by delay: t+1 / t+2 | 8/18, **0/18** | 18/18, 18/18 |
| by phase: ENGINE / FRI / MON / THU / TUE / WED | 2/6, 2/6, 2/6, 2/6, **0/6**, **0/6** | 6/6 each |

**The 4b leg never fails anywhere** — the binding-leg column reads `none` at all 36 points.
The 4a leg fails 28 times, by H1 at 15 and by MaxDD at 13; **not once by H2**. Three of the four
axes can kill it on their own:

* **Latency alone.** One extra day of execution (t+1 -> t+2) takes the candidate from 8/18 to
  **0/18**, and it does so entirely through DRAWDOWN: at 10 bps / ENGINE the delay costs 1.01 pp
  of MaxDD (-11.81% -> -12.82%) and pushes it through the live book's -12.24%, while both Sharpe
  halves still clear (H1 1.2841 > 1.2296, H2 1.1224 > 0.9669).
* **Cost alone.** At 50 bps the 4a leg is 0/12 while 4b is still 12/12.
* **Phase alone.** At t+1 and 10 bps the 4a pass holds on ENGINE / FRI / MON / THU and fails on
  TUE and WED, purely through MaxDD (-11.81% -> -12.87% / -13.32%, against the live book's
  -12.24%).

The candidate's own numbers at the discovery point and at the worst point on each axis:

| point | CAGR | Sharpe | MaxDD | H1 | H2 | 4a | 4b |
|---|---|---|---|---|---|---|---|
| 10 bps, t+1, ENGINE (discovery) | 12.51% | 1.2286 | -11.81% | 1.3171 | 1.1415 | **PASS** | PASS |
| 10 bps, t+1, WED/D10 | 12.34% | 1.2152 | -13.32% | 1.3099 | 1.1229 | FAIL (MaxDD) | PASS |
| 10 bps, t+2, ENGINE | 12.36% | 1.2027 | -12.82% | 1.2841 | 1.1224 | FAIL (MaxDD) | PASS |
| 50 bps, t+1, ENGINE | 11.11% | 1.1020 | -12.71% | 1.1917 | 1.0137 | FAIL (H1, MaxDD) | PASS |
| 50 bps, t+2, WED/D10 (worst) | 10.78% | 1.0618 | -13.77% | 1.1490 | 0.9761 | FAIL | PASS |

Even at the WORST of the 36 points the 4b legs are all positive: CAGR 10.78% against the
`0.70 x SPY` floor of 10.59%, MaxDD -13.77% against the `0.60 x SPY` cap of -20.23%.

## V3 — WHICH AXIS OWNS THE SPREAD (range of the axis-conditional means)

| metric | cost | delay | phase | winner |
|---|---|---|---|---|
| Sharpe | **0.1257** | 0.0310 | 0.0143 | COST |
| oos Sharpe | **0.1211** | 0.0219 | 0.0195 | COST |
| CAGR | **0.0140** | 0.0021 | 0.0017 | COST |
| MaxDD | 0.0051 | 0.0064 | **0.0095** | **PHASE** |
| L4_DD leg margin | 0.0051 | 0.0064 | **0.0095** | **PHASE** |

**Idea 1694's expectation is half-right and the half matters.** On Sharpe and CAGR the cost rung
dominates by 4-9x. On DRAWDOWN, phase beats both cost and delay — and drawdown is exactly the leg
that kills 4a. Over the whole corpus at 10 bps the phase spread of mean Sharpe exceeds the delay
spread on 5 of 6 (panel x cadence) arms (e.g. U56/W phase 0.0179 vs delay 0.0064; SMALL665/W
0.0150 vs 0.0006), so PHASE is a bigger dial than LATENCY almost everywhere.

## CENSUS — the whole corpus, by (delay, cost)

| delay | cost | n | 4b | 4a |
|---|---|---|---|---|
| t+1 | 10 | 2,520 | 1,130 | **236** |
| t+1 | 25 | 2,520 | 991 | 44 |
| t+1 | 50 | 2,520 | 784 | **0** |
| t+2 | 10 | 2,520 | 1,022 | 126 |
| t+2 | 25 | 2,520 | 961 | 2 |
| t+2 | 50 | 2,520 | 771 | **0** |

4b degrades gracefully (1,130 -> 771, -32% over the worst corner). 4a collapses (236 -> 0). The
4a path is a knife-edge across this whole family, not just at the candidate.

## V4 — RULE 8 (parameters chosen on 2009-2016 ONLY; 2017-2026 read ONCE)

864 picks (3 panels x 2 cadences x 6 phases x 2 delays x 3 costs x 2 families x 2 legal IS-only
choosers). **8 of 864 clear BOTH paths** — every one of them on B136, at t+1, via `CH_ISMINLEG`,
and 7 of 8 at 10 bps:

| panel | T | phase | delay | cost | family | pick | OOS CAGR / Sharpe / MaxDD |
|---|---|---|---|---|---|---|---|
| B136 | W | ENGINE | t+1 | 10 | DRIFT | t=0.10, h=0.08 | 13.01% / 1.2928 / -11.81% |
| B136 | W | FRI/D20 | t+1 | 10 | DRIFT | t=0.10, h=0.08 | 13.00% / 1.2923 / -11.81% |
| B136 | W | THU/D15 | t+1 | 10 | DRIFT | t=0.10, h=0.08 | 13.06% / 1.2991 / -11.65% |
| B136 | W | THU/D15 | t+1 | 25 | DRIFT | t=0.10, h=0.08 | 12.56% / 1.2537 / -12.03% |
| B136 | W | MON/D1 | t+1 | 10 | CAL | t=0.10, R=D | 13.00% / 1.2923 / -11.64% |
| B136 | W | WED/D10 | t+1 | 10 | CAL | t=0.10, R=D | 12.99% / 1.2917 / -11.66% |
| B136 | M | MON/D1 | t+1 | 10 | CAL | t=0.10, R=D | 12.95% / 1.2897 / -11.62% |
| B136 | M | WED/D10 | t+1 | 10 | CAL | t=0.10, R=D | 12.96% / 1.2904 / -11.72% |

(SPY OOS Sharpe 0.8737; live RULES v2 OOS Sharpe 1.1017.) Two things follow. First, `t = 0.10` is
picked at **8 of 8** — the TARGET is stable under the IS-only chooser across phase, cadence and
family; only the REFRESH mechanism moves. Second, a **daily-calendar refresh `R=D` reaches the
same place as the drift trigger `h=0.08`** at four of the eight, which is the same
"drift-vs-calendar is not separable at matched turnover" finding ideas 1799 / 2022 kept hitting.

**SMALL665 clears 4b at 0 of 288 picks and 4a at 0 of 288**, at every cost, delay and phase — the
sixth independent confirmation that this family does not work on small caps.

## What it changes

1. **Idea 2034's dual-path claim is RESTATED, not withdrawn.** The cell stays a 4b KEEP-candidate
   with the strongest stress record in the file (36 of 36); its 4a leg is downgraded to
   "passes only at t+1 and <= 25 bps and at 4 of 6 phase rungs". An addendum is filed on its memo.
2. **A new standing requirement:** any future 4a claim in this record must publish the (delay x
   cost x phase) survival share, because 4a is a knife-edge path — 236 of 2,520 at the best corner
   and 0 at the worst, while 4b moves only 1,130 -> 771.
3. **PHASE owns drawdown.** Where a verdict turns on MaxDD, the phase rung must be reported; on
   Sharpe it is the smallest of the three axes and the cost rung dominates.

**Survivorship.** U56 / B136 are CURRENT-constituent lists and SMALL665 a CURRENT sub-$2B screen
(54 tickers with `max_1d_move >= 1.0` in `data/small_meta.csv` dropped first). Every CAGR and
drawdown LEVEL is optimistic and both 4b bars are easier here than on a point-in-time panel. The
STRESS contrasts (same cell, one axis moved) are same-tape / same-names / same-grid and
first-order immune; the PASS COUNTS are not. The SMALL cache grew 439 -> 665 names on 2026-09-20,
so SMALL counts are not comparable with earlier SMALL numbers.

RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are untouched.

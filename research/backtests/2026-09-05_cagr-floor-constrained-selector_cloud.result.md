# Idea 109 (filed as a second "104") — CAGR-floor-constrained rule-8 selector (cloud, 2026-09-05)

**Verdict: KILL.** The pre-registered constraint *"maximise IS Sharpe subject to IS CAGR ≥ 70% of
SPY's IS CAGR"* should not replace PROTOCOL rule 8's selector. It is a third dial: it changes the
pick in 8 of 44 cells and is **worse out of sample in 8 of those 8**, for no net gain in 4b passes.

## Design

Four selectors, all pre-registered before any number was computed, applied to the same grids:

| | rule |
|---|---|
| `S_sharpe` | argmax IS Sharpe — PROTOCOL rule 8 as written |
| `S_floor` | argmax IS Sharpe s.t. IS CAGR ≥ 0.70 × SPY IS CAGR — the queue's proposal |
| `S_cagr` | argmax IS CAGR — control: is `S_floor` just a CAGR tilt? |
| `S_null` | the no-overlay point — control: does *any* selection beat not selecting? |

IS = 2009–2016; OOS = 2017–2026, untouched. Tie-break in every selector: smallest overlay
parameter. Six overlay grids (the five the queue names plus the leaderboard's gross lever):
sleeve f, band width, breadth cut depth at B = 30%, per-name trailing stop, BTC/ETH carve-out,
static gross. Two base books (top20, ewall) × two universes (u56, broad) × two cost rungs
(10, 25 bps), weekly. 176 grid points, 44 cells, all reported in `.grid.csv` / `.picks.csv`.

## Result

**Out of sample (2017–2026), mean over all 44 cells:**

| selector | OOS Sharpe | OOS CAGR | OOS MaxDD | regret vs best point | full-sample 4b | OOS-only 4b |
|---|---|---|---|---|---|---|
| `S_sharpe` | **1.048** | 13.32% | −19.7% | −0.015 | 20/44 | **22/44** |
| `S_floor` | 1.038 | 13.50% | −20.1% | −0.025 | **21/44** | 21/44 |
| `S_cagr` | 1.023 | **14.35%** | −21.6% | −0.040 | 15/44 | 16/44 |
| `S_null` | 0.993 | 12.35% | −19.2% | −0.070 | 19/44 | 19/44 |

Excluding the crypto grid (whose IS window is short — see caveat) the ordering is unchanged:
1.025 / 1.013 / 0.997 / 0.984.

**Paired, cell by cell.** `S_floor` picks the same point as rule 8 in **36/44 cells (82%)**. In the
8 cells where it differs it is worse on OOS Sharpe in **8/8** (mean −0.057), buying +0.95pp of OOS
CAGR at the cost of **2.53pp of extra OOS drawdown**. That is the wrong side of 4b, which caps
drawdown as well as flooring CAGR. Net movement in 4b passes across those 8 cells: **+1 full
sample, −1 OOS-only** — zero.

**It is a partial step toward the CAGR-maximiser, and the CAGR-maximiser is worse.** The ordering
`S_sharpe > S_floor > S_cagr` is monotone in how much CAGR weight the selector carries, on OOS
Sharpe, on regret and on OOS-only 4b passes. `S_floor` sits between rule 8 and the control it was
meant not to be.

**The constraint does not fire on the case that motivated it.** On the sleeve grid at
u56/top20/10 bps — idea 100's exact setting, re-run at idea 101's fixed gross — `f = 0.50` has an
IS CAGR of 10.8% against a floor of 10.47%, so it clears and `S_floor` picks the same `f = 0.50`
as rule 8. Idea 100's selector/4b mismatch was a consequence of letting gross float (idea 101
resolved it by fixing gross ex ante), not of the selector's objective.

**The constraint is infeasible in 27% of cells.** In 12 of 44 cells no grid point clears the IS
CAGR floor, and the selector silently degenerates to `argmax IS CAGR` — i.e. to `S_cagr`, the
worst-performing rule tested. Grids affected: breadth, stop, crypto, and band on u56/top20. A
selector that becomes its own worst control in a quarter of its applications is not a bar.

**What the run does confirm:** selection itself earns its keep. `S_null` is last on OOS Sharpe
(0.993 vs 1.048) and worst on regret (−0.070 vs −0.015). Rule 8 as written is doing real work;
the queue's question was whether the constraint improves it, and it does not.

## Caveats

- **Crypto grid.** BTC-USD begins 2014-09-17, so the crypto grid's IS window holds barely two
  years of crypto. That is a property of the grid the leaderboard actually ran, not a choice made
  here; results are shown both including and excluding it and the conclusion is identical.
- **Survivorship.** Both equity panels are current constituents; levels are biased up. The bias is
  identical across the four selectors, which is what this run compares, so the comparison is clean.
- **Calendar-day index (queue idea 38).** Hits every grid point and every selector identically.
- **Scope.** This kills the constraint as a general replacement for rule 8's objective. It says
  nothing about 4b's CAGR floor itself, which remains the binding bar on most candidate books
  (idea 101 found it binds first at 20 bps).

## Follow-up added to the queue

- 110 — selection-vs-no-selection as the real question (S_null loses 0.055 of mean OOS Sharpe to
  rule 8 across 44 cells; measure whether that gap survives the grids being pre-registered, or is
  itself a multiple-comparisons artefact of having six grids to choose from).

Script: `research/backtests/2026-09-05_cagr-floor-constrained-selector_cloud.py`
Console: `.console.txt` · Grid: `.grid.csv` · Picks: `.picks.csv` · Paired: `.paired.csv`

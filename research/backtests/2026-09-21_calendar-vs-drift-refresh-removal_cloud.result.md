# Idea 2056 (lane cloud, 2026-09-21) — CAN THE DRIFT THRESHOLD `h` BE REMOVED ENTIRELY FROM THE STANDING KEEP-4b CELL?

**ANSWER: YES, BUT ONLY IF WHAT REPLACES IT IS PRE-STATED. A plain calendar refresh keeps the 4b
verdict at every cell where the drift trigger has it — 16 of 16 — provided the refresh clock is
DAILY or WEEKLY. At MONTHLY it loses 7 of 8 and at QUARTERLY 8 of 8, always through the same leg
(`L4_DD`). And a legal IS-only chooser given the refresh axis lands on MONTHLY at 3 of 3 panels.
So `h` is not free to delete: deleting it swaps a threshold dial for a CADENCE dial, and the
cadence dial is the one the walk-forward chooser gets wrong.**

Gates 6/6. The standing cell reproduces the memo to max abs d **3.15e-05**; idea 2071's zero-IS
`MEDMULT m=1.00` rung reproduces cross-run to **4.87e-05**; `refresh=W` fires on exactly the 977
weekly trade dates (one clock, verified by count).

## Setup
Book inherited verbatim from the standing KEEP-4b candidate (equal-weight panel, gross scalar
capped at 1.00, trade W, t+1, 10 bps, sigma = 20d realised vol of the unlevered equal-weight panel).
**Two tuned parameters:** REFRESH RULE x TARGET. 5 x 6 x 3 panels x 4 cost rungs = **360 rows
published** in `.grid.csv`.

* REFRESH RULE `{DRIFT (h = 0.08, the incumbent), D, W, M, Q}` — when the gross scalar is re-read.
* TARGET `{0.08, 0.10, 0.12, 0.16, 0.20, MEDMULT_1.00}` — what it aims at. `MEDMULT_1.00` is idea
  2071's ZERO-IS rung (the expanding point-in-time median of the panel's own sigma), a rung of the
  target axis, not a third dial.

The book has two clocks: NAME weights always trade weekly; the GROSS SCALAR is re-read on the
refresh clock, and on a refresh that is not a trade day the book rescales holdings pro rata only.
`refresh = W` makes the two clocks identical — the "one-clock" book the idea asks about.

## 1. The direct question, 10 bps, full sample

| refresh | cells where DRIFT passes 4b | kept by the calendar rule | lost | gained | mean dSharpe | mean dTurnover |
|---|---|---|---|---|---|---|
| **D** | 8 | **8** | 0 | **+2** | -0.0130 | **+1.21/yr** |
| **W** | 8 | **8** | 0 | 0 | -0.0236 | -0.16/yr |
| M | 8 | 1 | **7** | +2 | -0.0118 | -0.44/yr |
| Q | 8 | **0** | **8** | 0 | **-0.1647** | -1.17/yr |

Every one of the 15 lost cells is lost on **`L4_DD`** (14 on drawdown alone, 1 with H2). The
mechanism is visible at the quarterly rung: MaxDD pins at exactly **-32.72%** at all six targets on
B136 — SPY's own drawdown to within 1 pp — i.e. a quarterly gross clock does not de-gross inside a
crash at all, whatever the target is.

## 2. The headline cell, B136, target 0.10, 10 bps

| refresh | CAGR | Sharpe | MaxDD | halves | OOS Sharpe | turnover/yr | refreshes/yr | 4b | 4a |
|---|---|---|---|---|---|---|---|---|---|
| **DRIFT h=0.08** (incumbent) | 12.51% | **1.2286** | **-11.81%** | 1.3171 / 1.1415 | 1.2928 | 3.13 | 21.0 | PASS | PASS |
| **D** | 12.24% | 1.2059 | -11.79% | 1.2819 / 1.1314 | 1.2830 | 4.64 | 266.7 | **PASS** | **PASS** |
| **W** (one clock) | 12.20% | 1.1820 | -13.46% | 1.2796 / 1.0872 | 1.2380 | 3.10 | 55.4 | **PASS** | fail |
| M | 13.20% | 1.1959 | **-20.27%** | 1.3523 / 1.0478 | 1.1884 | 2.71 | 12.7 | fail (L4_DD) | fail |
| Q | 12.17% | 0.9820 | **-32.72%** | 1.2187 / 0.8046 | 0.9257 | 1.67 | 4.2 | fail | fail |

SPY 15.12% / 0.8844 / -33.72% (bars: CAGR floor 10.59%, DD cap -20.23%); live RULES v2 7.96% /
1.0972 / -12.24%. **What `h` actually buys is turnover, not the verdict:** it reaches daily-like
drawdown control (-11.81% vs -11.79%) at weekly-like turnover (3.13 vs 4.64 turns/yr), worth
+0.0228 of Sharpe over D and +0.0467 over W at this cell.

## 3. Whole-grid pass counts (18 cells per refresh rule = 6 targets x 3 panels)

| refresh | 4b @0 bps | @10 | @25 | @50 | 4a @10 | mean Sharpe @10 | mean turnover |
|---|---|---|---|---|---|---|---|
| DRIFT | 9/18 | 8/18 | 8/18 | 8/18 | 3/18 | 1.0205 | 2.85/yr |
| **D** | 10/18 | **10/18** | 10/18 | 8/18 | 2/18 | 1.0075 | 4.06/yr |
| W | 8/18 | 8/18 | 8/18 | 8/18 | 1/18 | 0.9969 | 2.70/yr |
| M | 4/18 | 3/18 | 3/18 | 2/18 | 0/18 | 1.0088 | 2.41/yr |
| Q | 0/18 | **0/18** | 0/18 | 0/18 | 0/18 | 0.8559 | 1.68/yr |

A DAILY refresh passes 4b at **more** cells than the drift trigger (10 vs 8): it rescues the wide
targets the trigger drops (`t = 0.20` on both large panels, where DRIFT fails on `L4_DD`), because a
threshold of 0.08 is a large fraction of the gross move a wide target ever makes.

## 4. Rule 8 — this is where removing `h` costs something
Both dials chosen on 2009-2016 only (argmax min IS 4b-leg slack), 2017-2026 read exactly once:

| panel | IS pick (both dials free) | OOS read once | 4b OOS | 4a OOS |
|---|---|---|---|---|
| B136 | **refresh=M**, t=0.10 | 13.05% / 1.1884 / -20.27% | **fail** | fail |
| U56 | **refresh=M**, t=0.10 | 13.67% / 1.2605 / -19.62% | PASS | fail |
| SMALL665 | **refresh=M**, t=0.10 | 3.28% / 0.3351 / -35.63% | fail | fail |

The chooser lands on MONTHLY at **3 of 3** panels — the cadence that loses the drawdown leg — and
restricting it to calendar rules changes nothing (M wins there too). The IS window is 2009-2016,
which contains no 2020-scale crash, so a slow gross clock looks free in sample and is not out of
sample. **Pre-stating the refresh cadence at D or W, rather than choosing it, is what makes `h`
removable.** Held at `refresh = D`, every target rung that DRIFT clears 4b on out of sample also
clears it (B136 6/6, U56 6/6 at the OOS window; see `.walkforward.csv`).

## 5. The zero-dial corner
Calendar refresh x the zero-IS target = a book with no tuned dial anywhere: **16 of 32 large-panel
cells pass 4b, and all 16 are at D or W** (B136 D @10 bps: 15.98% / 1.2406 / -16.82%, OOS 14.77% /
1.2855; U56 D: 15.30% / 1.2607 / -15.94%, OOS 15.18% / 1.3440). At M and Q it is 0 of 16, `L4_DD`
binding at every one. SMALL665 is **0 of 16** at every cost rung.

## 6. What this does NOT show
* Not a promotion. No book here beats the standing cell on Sharpe at the same target; the calendar
  rules cost 0.005-0.047 of Sharpe at every large-panel cell but one.
* 4a is not rescued: 6 of 90 cells at 10 bps, all at t <= 0.10, and the addenda to the standing
  memo already downgraded that leg to a t+1 / <=25 bps / exact-name-list artefact.
* SMALL665 stays **0 of 24 at every cost rung and every refresh rule** (ninth confirmation that this
  family is a large-panel object).
* No bootstrap: idea 2060 showed the 4b legs of this family carry SEs of 1.1-1.5 pp and that the DD
  leg is the worst-resolved of the five. Every `L4_DD` verdict above is a point estimate.
* SURVIVORSHIP: B136/U56 are current-constituent lists, SMALL665 a current screen (54 tickers with
  `max_1d_move >= 1.0` dropped first). Levels are optimistic and both 4b bars easier than on a
  point-in-time panel; the refresh-rule CONTRAST is same-tape and same-names, so it is first-order
  immune.

## Verdict
**ANSWERED — PARTIAL YES. Memo clause 5 is removable machinery, but only against a PRE-STATED
daily or weekly gross clock; it is NOT removable if the replacement cadence is chosen on the IS
window, which picks monthly at 3 of 3 panels and fails 4b out of sample on 2 of them.** The drift
trigger's measured worth is a turnover saving (3.13 vs 4.64 turns/yr) and ~0.02 of Sharpe, not the
verdict. Logged as an addendum to
`research/backtests/2026-09-20_voltgt-drift-b136_KEEP4b_MEMO.md`; no new candidate promoted.

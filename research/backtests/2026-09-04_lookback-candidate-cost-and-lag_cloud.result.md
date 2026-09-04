# Idea 68 — lookback-candidate-cost-and-lag: KILL the `12-1 n=30` PARK (cloud lane, 2026-09-04)

**Script:** `research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py` ·
**Console:** `2026-09-04_lookback-candidate-cost-and-lag_cloud.console.txt`

## Verdict

**KILL.** Idea 8's `12-1 n=30` — the only grid point in that run to pass 4b on both
large-cap universes — **holds its cross-universe pass only at 5 and 10 bps with next-day
execution, and loses it at every cost level if execution slips by one week.** 80 points
(2 universes x 2 signals x n in {20,30} x 5 costs x 2 lags), all reported. The harness
reproduces idea 8's published rows to the decimal on both lists (u.json
10.9%/1.097/-15.8%, broad 13.0%/1.004/-20.2%) and the analytic cost model is bit-identical
to the engine (max |diff| = 0.00e+00).

## Where the cross-universe pass is lost

| lag | 5 bps | 10 bps | 15 bps | 25 bps | 50 bps |
|---|---|---|---|---|---|
| 1 day | **BOTH** | **BOTH** | u:CAGR / b:H2 | u:CAGR / b:H2,OOS,DD | fails everything |
| 1 week | b:H2,DD | b:H2,OOS,DD | b:H2,OOS,DD | u:CAGR / b:H2,OOS,DD | fails everything |

The break is **between 10 and 15 bps** at 1-day execution, and it breaks on *both*
universes at once but for different reasons: universe.json runs out of CAGR (the 4b floor
is 10.68%/yr) while the broad list runs out of H2 Sharpe.

## The pass at 10 bps was never real

At the protocol's own 10 bps / 1-day setting, the candidate clears 4b on margins of:

| bar | universe.json | universe_broad.json |
|---|---|---|
| CAGR ≥ 10.680% | 10.868% — **+0.188pp** | 13.042% — +2.362pp |
| MaxDD ≥ -20.230% | -15.816% — +4.414pp | -20.171% — **+0.059pp** |
| H2 Sharpe > 0.837 | 1.094 — +0.258 | 0.875 — +0.038 |

Each universe passes with one margin of a rounding error: six hundredths of a percentage
point of drawdown on the broad list, nineteen hundredths of a point of CAGR on the primary
one. This is not a robust pass that costs eventually erode — it is a tie that a half
basis point of cost, or a week's delay, converts into a failure.

## The pre-registered hypothesis is confirmed, and it does not save the candidate

The idea's premise was that 6.7x/yr turnover should decay more slowly than the incumbent
blend-v1 n=20's 9.6x. It does, on both lists:

| book | turnover (u.json) | dSharpe per +10 bps (u.json) | (broad) |
|---|---|---|---|
| 12-1 n=30 (candidate) | 6.70x | **-0.068** | -0.083 |
| blend-v1 n=30 | 6.98x | -0.070 | -0.093 |
| 12-1 n=20 | 9.24x | -0.080 | -0.086 |
| blend-v1 n=20 (incumbent) | 9.63x | **-0.084** | -0.099 |

The candidate decays ~19% more slowly on universe.json and ~16% more slowly on broad, and
by 50 bps it beats the incumbent on Sharpe by +0.066 (u.json) and +0.110 (broad) despite
losing to it by -1.94%/yr at 5 bps (t -2.62). So the turnover argument is right — but it
buys exactly **one cost step**: the incumbent's cross-universe pass dies at 10 bps, the
candidate's at 15. Neither has room at the 25 bps level that idea 63's core-sleeve arm
reached.

## The week's delay costs risk, not return

This is the run's non-obvious result. Deferring execution by a full week changes mean
return by **+0.18 to +0.47%/yr, all four books, both universes — every paired t between
+0.27 and +0.55, and every sign positive.** Momentum at these horizons genuinely does not
care about a week. What it costs is drawdown and second-half Sharpe:

- candidate, broad: MaxDD -20.17% -> **-22.70%** (2.5pp deeper, straight through the cap),
  H2 Sharpe 0.875 -> 0.787, OOS 0.971 -> 0.883.
- candidate, universe.json: MaxDD -15.82% -> -17.33%, H2 1.094 -> 1.052.
- incumbent, broad: MaxDD -20.1% -> -22.9%, H2 0.814 -> 0.735.

A stale book takes the same crashes a week later and larger. Any implementation that
cannot execute within a day of the signal should be assumed to lose ~2.5pp of drawdown,
not ~0pp of return.

## Walk-forward (rule 8), re-run inside every (cost, lag) cell

**Rule 8 selects the candidate only in cells where it fails out of sample.** On
universe.json it is picked in 0 of 20 selections (plain-Sharpe takes 12-1 n=20 in all 10
cells; the 4b-aware rule takes 12-1 n=20 once, blend-v1 n=20 in 3, and finds nothing in
6). On broad, plain-Sharpe picks the candidate in 6 of 10 cells — every one of them a
1-week-lag cell or the 50 bps cell — and **all 6 miss the OOS 4b bars** (OOS drawdown
-22.6% to -23.6%); the 4b-aware rule picks it 0 times, taking blend-v1 n=30 in 4 cells
and finding nothing in the other 6. This reproduces
idea 8's core finding on a different axis: the walk-forward cannot select this book.

## Honest limits

Survivorship: both lists are current constituents, so absolute CAGRs are optimistic; the
cost/lag comparisons hold names, days, gate and gross fixed and are far less exposed. The
cost model is linear in turnover and makes no allowance for market impact, which would
penalise the higher-turnover books further and therefore, if anything, strengthens the
candidate's relative-decay result while leaving its absolute failure untouched. The 1-week
arm models pure delay (signal at Friday close, traded the following Friday close), not
partial fills.

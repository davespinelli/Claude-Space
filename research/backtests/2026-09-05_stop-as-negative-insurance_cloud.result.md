# Idea 96 — stop-as-negative-insurance (cloud, 2026-09-05)

**Verdict: ANSWERED — idea 94's KILL STANDS, and the queue's hypothesis is refuted twice over.
The negative sign is neither the instrument nor the weekly grid: it is the ONE-DAY EXECUTION
CONVENTION. Idea 94's stop is already checked daily and is already protocol-conformant (a
trigger at close t flattens the name for day t+1's return, exactly PROTOCOL rule 2), and under
that convention it destroys drawdown in 12 of 12 cells at 15% and 8 of 12 at 25%. Delaying the
exit by ONE further day flips median dMaxDD from -0.69 pp to +2.44 pp and manufactures 9
apparent 4b passes — but test H shows why: the day after a stop fires, the triggering name
earns +0.57% to +2.21% against an unconditional +0.06%/day (t +2.70 to +10.37). The slower arm
is not better insurance, it is a short-term-reversal harvest, it violates rule 2, rule 8 picks
the no-stop control in all four cells where it appears, and it exists on one universe only.**

Script: `2026-09-05_stop-as-negative-insurance_cloud.py`. 144 stop arms + 12 matched controls +
132 static-gross ladder points + 12 reversal cells, all reported. Two tuned parameters: stop
CHECK frequency {daily, weekly-grid} and execution LAG {same, next, rebal}. Stop depth
{15%, 25%}, book {V1u, TOP20, EWall}, universe {u56, broad} and cost {10, 25 bps} are reported
at every value, never selected on. Idea 94's module is imported, not re-implemented.

## 0. Reproduction — exact
This run's generalised stop simulator at (check=daily, lag=same) equals idea 94's
`run(stop=...)` at **max|diff| = 0.000e+00** across all 24 arms, with **zero** firing-count
differences, and its no-stop control equals idea 94's `run()` at 0.000e+00 across 12 cells.
Idea 94's published stop row re-derives:

| depth | median dMaxDD | published | median dSharpe | published | median turnover | published |
|---|---|---|---|---|---|---|
| 15% | **-0.69 pp** | -0.69 | -0.036 | -0.033 | 12.5x | 12.5x |
| 25% | **-1.32 pp** | -1.25 | -0.007 | -0.006 | 11.3x | 11.3x |

(Negative in 12/12 and 8/12 cells here against idea 94's pooled "10 of 12"; 0/12 priceable at
either depth, as published.)

## 1. The queue's premise was wrong about the code (and so was this run's first audit)
The queue supposed idea 94 used "the weekly-grid exit". It does not: its step 5 evaluates the
trigger on **every row**, unconditional on the rebalance mask. The weekly grid governs
**re-entry** only — which is what idea 94's own mechanism sentence says.

This run's docstring then made the opposite error, claiming idea 94's stop was one bar *faster*
than PROTOCOL rule 2 allows. It is not, and the correction is recorded in the script rather
than edited out because two predictions were written on top of it. `engine.backtest` holds
`w.shift(1)`: a weight computed through close t-1 earns day t's return, i.e. "decided at t,
applied at t+1". Idea 94's stop fires from close i and the name is flat for day i+1's return —
**exactly that convention**. So `lag=same` is the conformant arm and this run's `lag=next` is
one day **slower** than the protocol permits. That single fact decides which column below may
be quoted.

## 2. The queue's question, answered: the sign is the execution lag (P2, P3 REFUTED)
dMaxDD over the 12 matched cells, by implementation (arm minus its own control):

| check | lag | depth | dMaxDD<0 | med dMaxDD | med dCAGR | med dSharpe | priceable (abs / rel) |
|---|---|---|---|---|---|---|---|
| daily | **same** | 0.15 | **12/12** | **-0.69 pp** | -1.19 | -0.036 | 0/12 / 0/12 |
| daily | **same** | 0.25 | 8/12 | **-1.32 pp** | -0.33 | -0.007 | 0/12 / 0/12 |
| daily | next | 0.15 | 4/12 | **+2.44 pp** | -0.49 | -0.004 | 8/12 / 6/12 |
| daily | next | 0.25 | 0/12 | +1.42 pp | 0.00 | +0.012 | 8/12 / 2/12 |
| daily | rebal | 0.15 | 8/12 | -0.25 pp | -0.62 | -0.038 | 0/12 / 0/12 |
| daily | rebal | 0.25 | 8/12 | -0.13 pp | -0.13 | -0.008 | 0/12 / 0/12 |
| weekly | same | 0.15 | 4/12 | +0.31 pp | -1.38 | -0.047 | 8/12 / 0/12 |
| weekly | same | 0.25 | 0/12 | +0.40 pp | -0.27 | -0.006 | 7/12 / 0/12 |
| weekly | next | 0.15 | 4/12 | **+2.54 pp** | -0.43 | -0.004 | 8/12 / 8/12 |
| weekly | next | 0.25 | 0/12 | +1.65 pp | -0.00 | +0.009 | 8/12 / 6/12 |
| weekly | rebal | 0.15 | 8/12 | -0.17 pp | -0.39 | -0.024 | 0/12 / 0/12 |
| weekly | rebal | 0.25 | 8/12 | -0.05 pp | -0.09 | -0.005 | 0/12 / 0/12 |

**P2 REFUTED** — the sign is not invariant across implementations (minimum negative count 0/12).
**P3 REFUTED, and informatively so** — dMaxDD is *not* monotone in exit speed. Ordered by
speed the medians run -0.95 (daily/same), +2.16 (daily/next), -0.17 (daily/rebal), +0.31
(weekly/same), +2.45 (weekly/next), -0.11 (weekly/rebal). The one axis that moves the sign is
`same` -> `next`; going slower still (`rebal`) puts it back negative. **The check frequency
does almost nothing** (daily vs weekly at matched lag moves the median by 0.1-1.3 pp and never
flips a sign); the queue's "intra-week vs weekly-grid" axis, its actual question, is the axis
that does not matter.

## 3. Why one day matters — the reversal (test H, the decisive number)
Mean return of the triggering name on the day AFTER the stop fires, against the same panel's
unconditional daily mean:

| panel / book | depth | firings | E[r] at t+1 | uncond | t | E[r] over t+1..5 | uncond x5 |
|---|---|---|---|---|---|---|---|
| u56 / TOP20 | 15% | 436 | **+0.673%** | +0.061% | **+3.04** | +2.120% | +0.306% |
| u56 / TOP20 | 25% | 93 | **+1.589%** | +0.061% | +2.73 | +1.540% | +0.306% |
| u56 / EWall | 15% | 1926 | **+0.587%** | +0.061% | **+5.70** | +1.289% | +0.306% |
| u56 / EWall | 25% | 684 | +0.566% | +0.061% | +2.70 | +1.215% | +0.306% |
| broad / TOP20 | 15% | 460 | **+0.902%** | +0.066% | **+3.96** | +2.645% | +0.329% |
| broad / TOP20 | 25% | 82 | **+2.211%** | +0.066% | +3.24 | +1.795% | +0.329% |
| broad / EWall | 15% | 4889 | **+0.685%** | +0.066% | **+10.37** | +1.487% | +0.329% |
| broad / EWall | 25% | 1673 | +0.746% | +0.066% | +5.25 | +1.593% | +0.329% |

(The four `V1u` rows have 0-7 firings and are noise; they are reported, not read.) Excess over
unconditional in 9/12 cells, median **+0.615 pp/day**, and it persists over five days
(+1.2 to +2.6% vs +0.31% unconditional). **A trailing stop fires exactly into a short-term
reversal.** That is idea 94's "sells into the drawdown" claim measured rather than asserted,
and it is the whole of the `same` -> `next` effect: the slower arm's 2-4 pp of "bought"
drawdown is one day of bounce it did not sell into, harvested ~15-280 times a year.

## 4. The 9 apparent 4b passes are not candidates
All 9 sit on `lag=next`, all on **u56 only**, all on `TOP20`/`EWall`, all at stop15/25. Four
independent reasons not to quote them:

1. **They violate PROTOCOL rule 2.** `next` is one day slower than the protocol's execution
   convention (section 1). The conformant column is `same`, where 0 arms pass.
2. **All 12 controls fail 4b on the drawdown cap alone** (u56 TOP20 -22.2%, EWall -22.5% vs the
   -20.2% cap; their Sharpe, halves, OOS and CAGR all clear). The stop buys 2.2-3.9 pp of MaxDD
   and lands at -18.6% to -20.1% — margins of **0.15 to 1.6 pp** on a single-path extremum.
3. **Rule 8 cannot see them.** In all four cells where a 4b pass exists, the walk-forward
   selector picks the **no-stop control** (IS Sharpe differences <= 0.001). The selector takes a
   stop in 5/12 cells with mean OOS regret **+0.002** — indistinguishable from zero. Under
   PROTOCOL rule 8 an unselectable in-sample winner is PARK at best; this is not even an
   in-sample winner.
4. **Cross-universe: 0 of 9 are on `broad`.**

dSharpe on those 9 arms is +0.001 to +0.025 with dCAGR -0.00 to -1.01 pp — the book is
unchanged; only its worst single path moved.

## 5. Mechanism and the lever it must beat
The stop is a de-grossing of about 1 pp: realised invested gross 0.739-0.750 against the
control's 0.748-0.750, at 1.5-3.8x/yr of extra turnover (EWall 3.4x vs 0.9x). Firing rates
span 0.0-277/yr, essentially all of it in the wide books. Each cell's own static-gross lever
prices drawdown at **0.05-0.74 pp of CAGR per pp of MaxDD** (median ~0.59); the conformant stop
buys negative drawdown and is therefore off that menu entirely — idea 94's ranking, on a
harness that reproduces it to zero.

## 6. Walk-forward (rule 8), all 12 cells
Selector picks the control in 7/12, `daily/same/stop15` in 4 (all `V1u`, regret -0.002 to
-0.005), `daily/next/stop25` in 1 (broad/EWall@10, regret +0.040). Mean regret **+0.002**. OOS
Sharpe beats SPY (0.882) in 7/12 cells — but that is the control books' property, not the
stop's. Live RULES v1 OOS on these panels: 0.714 (u56) / 0.573 (broad).

## 7. What this changes
- **Idea 94's stop KILL is confirmed and strengthened**, on a harness reproducing it exactly.
  "The per-name trailing stop is the dearest instrument" (idea 97's C3, the one clause that
  survived every panel) is untouched.
- **New, and it is the finding worth carrying:** every drawdown price in this project is
  quoted without an execution lag, and for a fast instrument the lag moves the price by more
  than the instrument does. That is a PROTOCOL gap, not a stop result — memo has wording.
- **A separate, live-looking observation is deliberately NOT pursued here:** a +0.6-0.9%/day
  post-trigger reversal at t +3 to +10 is a short-term-reversal signal in its own right, on
  both panels. It is a statement about the panels, not about stops, and it belongs on the queue
  as its own idea with its own pre-registration and cost test rather than being smuggled in as
  a stop result.

## Caveats
Current-constituent survivorship on both panels flatters the always-invested control and so
makes a protective instrument look worse; that bias runs *with* this run's conclusion, making
it a lower bound on the stop's value, not an upper one. MaxDD is one number off one path, which
is exactly why section 4's 0.15-1.6 pp margins are not treated as passes. The reversal in test
H is measured on the triggering names only and is not a tradeable return — it ignores costs,
borrow, and the fact that acting on it means holding a name that just broke 15% off its high.
Idea 38's calendar-day index is still unfixed for `u56`/`broad`; it applies identically to arm
and control in every comparison here. Stop depths, book definitions and the 2009-2016/2017-2026
split are inherited from idea 94 on overlapping data, so the walk-forward validates the
IMPLEMENTATION comparison, not those constants. No file outside `research/backtests/` was
modified.

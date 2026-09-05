# Idea 95 — vol-threshold-sweep-on-ewall (lane B, 2026-09-05)

**Verdict: KILL of `0.60` as a *derived* threshold — the surface is flat, the gate loses CAGR at
every value of it, and rule 8 selects 0.60 in 0 of 8 cells with a sign-flipping IS/OOS
correlation. The incumbent BOOK survives the sweep unbeaten: `theta=0.60/dg` is one of only two
points in the grid passing 4b on BOTH universes at BOTH cost rungs. No new KEEP-candidate; the
adoption block idea 95 was filed to clear is LIFTED on the numbers and REPLACED by a wording
constraint — RULES may not call 0.60 a volatility threshold.**

Script: `research/backtests/2026-09-05_vol-threshold-sweep-on-ewall_B.py`
Console: `.console.txt` · Grid: `.grid.csv` (44 rows) · Walk-forward: `.walkforward.csv`
Memo with exact RULES wording: `.memo.md`

## What was asked

Idea 94's 4b KEEP-candidate `EWall + vol60-dg` — equal-weight EVERY name in the panel at 75%
gross, no ranking, names with `vol20 >= 0.60` zeroed into cash — inherits `0.60` verbatim from
RULES v1 and has never been re-derived. Idea 98 then made this book the project's most
year-robust candidate (17/18 LOYO on u56, **18/18** on broad, at both cost rungs) and one of only
two still passing 4b on both universes at 25 bps. An unexamined constant had become load-bearing
for an adoption decision. Sweep it: `theta ∈ {0.40, 0.50, 0.60, 0.80, 1.00}` × convention
`{dg, rw}`, both large-cap universes, 10 and 25 bps. **Exactly two tuned parameters (theta,
convention); all 5 × 2 × 2 × 2 = 40 grid points reported, plus the 4 ungated controls.**

## Harness

Idea 94's script is **imported, not re-implemented**, so every number sits on the simulator that
produced the row being audited; `theta` is injected into that module's `MAX_VOL` and nothing else
is touched. Three checks ran before any new number was read:

| check | result |
|---|---|
| (a) engine-equivalence, ungated `EWall` vs `engine.backtest` @10bps | `max|diff| = 0.000e+00` **EXACT**, both universes |
| (b) idea 94's published `EWall+vol60-dg` u56 @10bps | **11.6% / 1.133 / -16.9%** vs published 11.6% / 1.133 / -16.9% |
| (c) `theta=0.60/dg` in *this* grid vs (b) | `max|diff| = 0.000e+00` |

Weekly, t+1, long-only, 75% gross, no leverage, eval `2009-01-13 → 2026-09-04`,
IS ≤ 2016-12-31, OOS ≥ 2017-01-01. `dg` = gated-out names go to cash (the book de-grosses);
`rw` = the book is rebuilt at full 75% gross among the gated-in names (composition change only).

Benchmarks on the eval window: **SPY 15.23% / 0.889 / -33.72%**, halves 0.957 / 0.834, OOS 0.882.
4b bars: Sharpe > 0.957 (H1) / 0.834 (H2) / 0.882 (OOS), MaxDD ≤ 20.23%, CAGR ≥ 10.66%.
Live RULES v1 @10bps: u56 6.45% / 0.664 / -13.83% (OOS 0.747); broad 6.39% / 0.635 / -21.19%
(OOS 0.576).

## (1) The surface is FLAT in Sharpe and MONOTONE in CAGR and drawdown

Sharpe across the whole 5-point theta sweep, by (universe, cost, convention):

| cell | 0.40 | 0.50 | 0.60 | 0.80 | 1.00 | range | ungated control |
|---|---|---|---|---|---|---|---|
| u56 @10 dg | 1.130 | **1.138** | 1.133 | 1.103 | 1.118 | 0.035 | 1.124 |
| u56 @10 rw | 1.101 | 1.123 | **1.125** | 1.106 | 1.123 | 0.025 | 1.124 |
| u56 @25 dg | 1.093 | 1.112 | **1.113** | 1.088 | 1.105 | 0.024 | 1.113 |
| u56 @25 rw | 1.046 | 1.088 | 1.099 | 1.088 | **1.109** | 0.063 | 1.113 |
| broad @10 dg | **1.190** | 1.149 | 1.138 | 1.116 | 1.117 | 0.074 | 1.122 |
| broad @10 rw | **1.128** | 1.127 | 1.120 | 1.119 | 1.127 | **0.009** | 1.122 |
| broad @25 dg | **1.151** | 1.124 | 1.119 | 1.102 | 1.105 | 0.050 | 1.112 |
| broad @25 rw | 1.046 | 1.094 | 1.096 | 1.102 | **1.114** | 0.040 | 1.112 |

The whole axis moves Sharpe by **0.009 to 0.074**, and **the ungated control sits inside the
sweep's own range in 7 of 8 cells** (the exception is broad @10 dg, where the control is below
every arm). The argmax wanders across the axis with no stable location: 0.40 four times, 0.50
once, 0.60 twice, 1.00 twice — including 0.40 and 1.00, the two ENDPOINTS, in the same universe
at different cost rungs (broad @10 dg picks 0.40, broad @25 rw picks 1.00).

What theta *does* move, monotonically and without exception in all 8 cells, is exposure and its
two consequences. u56 @10 dg: CAGR 9.4% → 10.8% → 11.6% → 12.1% → 12.7% against the control's
13.3%, MaxDD -13.7% → -16.1% → -16.9% → -18.9% → -20.9% against -22.5%, mean names held 47.2 →
50.2 → 51.9 → 53.3 → 53.8 of 54.1. Turnover falls monotonically too, 2.05× → 0.93×/yr against
0.83×.

**Every one of the 40 arms loses CAGR to its own ungated control** — paired daily differences
run **-0.25 to -4.04 pp/yr**, negative in **40 of 40**, monotone in theta, and significant
(|t| ≥ 2) in only 13 of 40, all of them the tight thetas. At the published 0.60 the loss is
-1.05 to -1.87 pp/yr at **|t| 1.53 to 2.00**. So the vol20 gate on this book is a de-risking
dial, not a signal: it buys drawdown with return, and at the incumbent threshold its
risk-adjusted contribution is statistically indistinguishable from zero.

## (2) 0.60 is not chosen by an edge — it is where 4b's two ABSOLUTE bars bracket

18 of 40 grid points pass 4b; 19 of 40 pass 4a; the ungated controls pass 4b 0/4 (drawdown) and
4a 1/4. The failure column splits perfectly along the axis:

- **theta = 0.40** fails **the CAGR floor** (9.0-10.5% against a 10.66% floor) — 0/4 for `dg`,
  3/4 for `rw`;
- **theta = 0.80 and 1.00** fail **the MaxDD cap** (-18.9% to -25.2% against a -20.23% cap) —
  2/4, 0/4, 0/4, 0/4;
- **theta = 0.50 and 0.60** pass — `0.50/rw` **4/4**, `0.60/dg` **4/4**, `0.50/dg` 3/4,
  `0.60/rw` 2/4.

Neither H1, H2 nor OOS Sharpe is ever the binding bar anywhere in the grid. The 4b window in
theta is an interval, closed on the left by a return floor and on the right by a drawdown cap,
with the incumbent near its middle — this is idea 84/90's gross-interval result reproduced on a
new axis, and it says the published threshold is a *risk-budget location*, not a discovered
constant. `theta=0.50/rw` (u56 @10bps 11.7% / 1.123 / -18.2%, halves 1.144/1.105, OOS 1.185;
broad 12.5% / 1.127 / -19.5%, halves 1.248/1.010, OOS 1.107) passes the same 4/4 as the
incumbent and is a genuine co-equal, at 2.4×/yr turnover against 1.4×.

## (3) Rule 8 cannot pick theta, and its selectability FLIPS SIGN between the two universes

Both selection rules were fixed in writing before any OOS number was read: **S1** argmax IS
Sharpe; **S2** argmax IS Sharpe among points meeting 4b's two absolute bars computed on the IS
window alone (MaxDD ≤ 13.24%, CAGR ≥ 10.47%).

| universe | cost | rule | pick | OOS CAGR/Sharpe/MaxDD | OOS rank | beats ungated control? | ρ(IS, OOS Sharpe) |
|---|---|---|---|---|---|---|---|
| u56 | 10 | S1 = S2 | **theta=1.00/rw** | 13.5% / 1.133 / -21.9% | 7 of 10 | **no** (ctl 1.136) | **-0.697** |
| u56 | 25 | S1 = S2 | **theta=1.00/dg** | 12.9% / 1.111 / -21.0% | 8 of 10 | **no** (ctl 1.125) | **-0.636** |
| broad | 10 | S1 = S2 | **theta=0.40/dg** | 10.2% / 1.195 / -12.6% | **1 of 10** | yes (ctl 1.102) | **+0.588** |
| broad | 25 | S1 | **theta=0.40/dg** | 9.8% / 1.154 / -12.7% | **1 of 10** | yes (ctl 1.091) | **+0.939** |
| broad | 25 | S2 | theta=0.50/dg | 11.0% / 1.104 / -17.8% | 2 of 10 | yes | +0.939 |

SPY OOS 15.5% / 0.882 / -33.7%; RULES v1 OOS 7.7% / 0.747 / -13.8% (u56 @10) and
5.9% / 0.576 / -21.2% (broad @10).

Three things follow, and they are the run's core result.
**(a) The published 0.60 is selected by neither universe, under neither rule, at neither cost
rung — 0 of 8 walk-forward selections.**
**(b) The two universes pick OPPOSITE ENDPOINTS of the axis** (1.00 on u56, 0.40 on broad), which
is the same universe-fragility signature ideas 2/55 found on the position-count and lookback axes.
**(c) The IS→OOS rank correlation itself flips sign, -0.70/-0.64 on u56 against +0.59/+0.94 on
broad.** On u56 in-sample Sharpe is *anti*-informative about the threshold: the walk-forward
picks the 7th and 8th best of 10 and loses to doing nothing at all. A parameter whose
selectability reverses between two heavily-overlapping large-cap lists is not a parameter the
data can set.

## (4) The gate does beat the static-gross lever at matched drawdown — the one thing it earns

The reference price is idea 94's 19-point static-gross ladder on the ungated book: slope
**0.595 / 0.588** pp CAGR per pp MaxDD on u56 @10/@25 and **0.565 / 0.558** on broad. Comparing
each arm against the ladder interpolated to **that arm's own MaxDD**, the gate reaches the same
drawdown at a **higher** CAGR in **38 of 40 points**, by +0.11 to **+3.85 pp** (the two losses are
broad `rw` at theta=1.00, -0.12 and -0.19 pp, where the gate barely does anything). Arm prices run
**0.257 to 1.513** pp/pp against those ladder slopes; at the incumbent 0.60 the price is
0.257-0.318, i.e. roughly **half** the cost of simply holding less.

That is a real and useful property — and it points *away* from the incumbent, because the lever
edge is largest at the tight thetas (broad `0.40/dg`: +3.85 pp, best Sharpe in the entire run at
1.190, best drawdown at -12.6%) which is exactly where 4b's absolute CAGR floor kills the arm.
The most efficient insurance in the grid is disqualified by a return bar, reproducing ideas
100/117's finding that 4b's *absolute* bars, not its risk-adjusted ones, decide these cases.

**Priceability, per open ideas 122/123.** Under idea 94's absolute floor (dMaxDD > 0.10 pp) all
40 arms are priceable. Under idea 123's proposed RELATIVE floor (dMaxDD ≥ 10% of the control's
own |MaxDD|) **12 of 40 stop being priceable** — every one of them theta ∈ {0.80, 1.00}, where the
gate moves drawdown by 0.21-1.69 pp against a control drawing down 22-25%. The two ratios above
1.0 (broad `1.00/rw`, 1.079 and 1.513) are both in that unpriceable set, so no headline here rests
on them. Idea 123's floor is doing real work on this grid and this run supports it.

## Recorded against our own reading

- The incumbent is **not** beaten. `theta=0.60/dg` is one of only two points passing 4b on both
  universes at both cost rungs, and it is the cheaper of the two in turnover (1.36-1.39×/yr
  against `0.50/rw`'s 2.37-2.41×). Nothing here says to change the number.
- The flatness result is strongest exactly where it is least flattering to us: on `broad @10 rw`
  the entire axis spans **0.009** of Sharpe, which is a cleaner "this dial does nothing" than any
  argument about significance.
- A parameter that cannot be selected is not thereby *harmful* — the sweep shows a wide
  plateau, which is the benign form of unselectability (idea 66's gross result). The correct
  reading is that theta is a risk-budget dial to be **declared**, not fitted; the wrong reading
  would be to treat the walk-forward's failure as evidence against the book.

## Caveats

**Survivorship** (idea 54): both panels are current-constituent lists, and a vol20 gate is
precisely the instrument that bias flatters — names that blew up and delisted are absent, so a
LOOSE threshold is flattered more than a tight one. The bias therefore runs *toward* this run's
"the gate does nothing" finding, which is stated, not adjusted. **Calendar-day index** (idea 38)
is still unfixed for u56 and broad. **Two universes are one replication**, not two (ideas 39/49):
they overlap heavily, which makes the sign flip in (3c) more striking, not less. The theta grid
is 5 points on a bounded axis; a finer grid could locate an interior optimum, but (3) says such a
point could not be selected out of sample even if it existed. MaxDD is a single-path extremum
throughout.

## Recommendation to the Sunday review

No file modified. Do not re-tune the threshold. If `EWall + vol60-dg` is adopted, adopt it with
the exact wording in `.memo.md`, which states 0.60 as a **declared risk-budget constant with its
measured plateau**, and forbids RULES from describing it as a volatility threshold or as
optimised. Ideas 128-130 queued.

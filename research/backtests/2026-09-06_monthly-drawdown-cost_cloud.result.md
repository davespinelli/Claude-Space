# Idea 64 — monthly-drawdown-cost (cloud, 2026-09-06)

**ANSWERED. Part 1: the monthly book's extra drawdown is 2020 COVID and almost nothing else — in
8 of 8 (panel x book) cells 2020 IS the global MaxDD and carries -1.14 to -6.05pp of the M-vs-W
gap, while 2022 runs the OTHER way (+0.38 to +2.39pp SHALLOWER monthly). Part 2: KILL of the
queued proposition. The weekly exit-only check drops the drawdown in 8 of 8 cells (+3.4 to
+9.8pp) but does NOT keep the return — dCAGR is negative in 32 of 32 cells (-0.39 to -2.56pp) and
mean dSharpe is -0.016 @10bps / -0.032 @25bps. 4a 0 of 48 at both rungs. The rule-8 chooser buys
the repair in 2 of 16 cells and is worth +0.000 OOS Sharpe in the other 14. No RULES change.**

Script `2026-09-06_monthly-drawdown-cost_cloud.py`; console `.console.txt`; all 96 arm points in
`.grid.csv`; the episode decomposition in `.episodes.csv`; rule 8 in `.walkforward.csv`.
Panels broad (136) and u56 (56), 4 books, weekly/monthly/hybrid, t+1, 10 and 25 bps.

## Gates, passed before any number was read

* `backtest_hybrid` with an empty exit mask is **bit-identical** to `engine.backtest(freq='M')`:
  max|daily return diff| **0.0e+00** on both panels. The exit machinery adds nothing when unarmed.
* Idea 66's published broad `top20-200d` WEEKLY @10bps reproduces **3/3**: 13.11% / 0.9581 /
  -20.05% (published 13.1% / 0.958 / -20.1%).

## Idea 3's claim, reproduced on this grid (8 cells per rung)

@10bps, monthly minus weekly: **dCAGR +1.41pp (8/8), dSharpe +0.0681 (7/8), dMaxDD -2.99pp
(deeper in 8/8)**. @25bps: +2.14pp (8/8), +0.1307 (8/8), -2.81pp (8/8). The trade idea 3
described is real and it is one-directional.

## PART 1 — the extra drawdown is ONE episode

Broad panel, M minus W MaxDD inside each pre-registered window (@10bps, negative = monthly deeper):

| book | 2010 | 2011 | 2015-16 | 2018Q4 | **2020** | 2022 | 2025 | global MaxDD W -> M |
|---|---|---|---|---|---|---|---|---|
| top20 | +1.19 | +0.24 | -1.09 | +0.09 | **-6.05** | +1.36 | -1.12 | -20.05% -> -26.10% |
| frac85 | +0.01 | +0.37 | -1.20 | +0.04 | **-4.05** | +1.37 | +0.13 | -18.58% -> -22.62% |
| ew-all | +0.21 | +0.34 | -0.85 | +0.57 | **-3.97** | +2.39 | +0.09 | -17.69% -> -21.66% |
| ew-band3 | -0.50 | -0.54 | -0.17 | +0.40 | **-3.95** | +2.00 | +0.22 | -18.53% -> -22.48% |

Every book's global MaxDD, weekly and monthly, is the same drawdown — peak **2020-02-19** in 8/8
cells, trough between 2020-03-12 and 2020-03-31 — and the monthly arm's trough sits at 03-16..03-23
against the weekly arm's 03-12..03-31, i.e. the two arms are drawing down the same episode and the
monthly one simply cannot act inside it. The per-calendar-year table says the same thing: outside 2020 the largest |M - W| in any
year is 2.4pp and the sign is mixed, and 2016 (-1.1 to -2.0pp) is the only other year where the
monthly book is consistently deeper. **2022 is not the culprit — the monthly book is shallower
there in 8/8 cells**, and 2025 is ±1.2pp with no consistent sign. u56 shows the identical shape at
a third of the magnitude (2020: -1.14 to -2.17pp).

So the monthly penalty is a **timeliness** cost concentrated in the one episode where the gate
flipped inside a month, not a general property of the cadence. That is exactly the hypothesis the
queued repair was built on — which is why the repair's failure is informative.

## PART 2 — the weekly exit-only check: drawdown yes, return no

Deltas vs the plain monthly arm of the same book, all 8 cells per arm, @10bps:

| arm | dSharpe (wins) | dCAGR (wins) | dMaxDD (shallower) | dturn |
|---|---|---|---|---|
| M+W-cash | **-0.0162** (2/8) | **-1.67pp** (0/8) | **+4.25pp** (8/8) | +0.56x |
| M+W-spread | -0.0166 (2/8) | -0.74pp (0/8) | +2.79pp (8/8) | +2.29x |
| M+D-cash | **+0.0030** (5/8) | -2.08pp (0/8) | **+7.53pp** (8/8) | +0.85x |
| M+D-spread | -0.0138 (2/8) | -0.87pp (0/8) | +2.50pp (8/8) | +3.49x |

At 25 bps every arm is negative on Sharpe (-0.021 to -0.066) and CAGR. The drawdown half of the
queued claim is **confirmed and then some** — the daily exit check gives back the whole 2020 gap
and more (broad ew-band3 2020: weekly -18.53%, monthly -22.48%, M+D-cash **-16.29%**). The return
half is **false in every one of the 32 cells**: the exit sells into the drawdown and the monthly
schedule will not re-enter until month-end, so the book misses the rebound it was holding for.

**4b movement is a swap of failure clauses, not a repair.** @10bps: W ref 6/8, plain M 4/8,
M+W-cash 4/8, M+W-spread 6/8, M+D-cash 5/8, M+D-spread 6/8; @25bps M stays best at 4/8 and the
cash arms drop to 2/8. Where a monthly book failed 4b on `DD`, the exit check fixes DD and the
book then fails on `CAGR` in **6 of the 16 broad exit-arm cells** @10bps. **4a is 0 of 48 at both rungs** — RULES v2 is
beaten nowhere in this family, consistent with the standing 4a census (idea 65, 0/192).

The one book where the repair works on every axis is the RULES v2 SHAPE, `ew-band3`: all four exit
arms improve Sharpe (+0.005..+0.022), OOS Sharpe (+0.011..+0.071) and MaxDD, and flip 4b
KILL(DD) -> KEEP on broad. Its best cell, **broad `ew-band3` monthly + DAILY exit-to-cash @10bps:
10.74% / 1.111 / -15.13%, halves 1.162/1.064, OOS 1.172, 3.38x/yr, 4b KEEP** — but it fails 4b on
the CAGR floor at 25 bps, fails 4a, is not the rule-8 pick, and is a monthly variant of a book the
live rules already run WEEKLY (which posts 11.8% / 1.070 / -18.5% here). PARK, not KEEP.

## Rule 8 — the honest chooser does not buy the repair

Both dials fitted on 2009-2016 by IS Sharpe alone: the pick is the **plain monthly arm in 14 of 16
(panel x book x rung) cells**, worth **+0.0000 OOS Sharpe**. The two exceptions are both
`ew-band3` @10bps (broad picks M+W-spread, +0.0106 OOS; u56 picks M+D-spread, +0.0115). Spearman
(IS, OOS) across the 5 arms is negative in 9 of 16 cells (as low as -0.900). This is another
instance of the record's standing pattern: an IS chooser over a small arm set is worth ~zero.

Pre-registered caveat (idea 111): 2017-2026 is very nearly H2 on this sample, so the rule-8 OOS
bar and 4b's H2 bar overlap. SURVIVORSHIP: both panels are current constituents, so absolute
CAGR/Sharpe are optimistic for every arm; every comparison here is between arms on the same panel
and the same days.

## Follow-ups worth queueing

* The exit sells into the drawdown and cannot re-enter until month-end. Price the symmetric
  repair — a monthly book with a weekly **re-entry** check as well (gate ON any week, at the
  month's own target weights) — and see whether the +4.25pp of drawdown survives with the CAGR.
* The monthly penalty is one episode. Re-run the M-vs-W comparison with 2020-02-01..2020-04-30
  excluded and report how much of idea 3's -3pp MaxDD claim survives; if it is ~0, the record's
  cadence-drawdown rows are a COVID statistic, not a cadence statistic.

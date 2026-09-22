# Idea 1545 — does DE-GROSSING dominate every DEVICE on the DRAWDOWN axis too?
*(2026-09-22, lane cloud, run 17.  Script: `research/backtests/2026-09-22_degross-frontier-on-the-drawdown-axis_cloud.py`)*

## ANSWER = NO, AND THE EXCEPTION IS ONE NAMED FAMILY, ON TWO PANELS, IN BOTH WINDOWS

Idea 1534 priced 90 (device, matched-exposure de-gross) pairs on Sharpe, found pooled
dMaxDD = **-1.55 pp (device DEEPER)**, and the record has been carrying that as "de-gross is
the efficient frontier for drawdown as well as for return".  This run traced the frontier
itself — a constant de-gross ladder, f = 0.02..1.00 in 0.02 steps, 50 rungs x 3 panels —
and placed all 90 device books against it.  **The blanket claim is false.**

* **50 of 90** device books are STRICTLY Pareto-dominated by at least one constant de-gross
  rung (better CAGR *and* shallower MaxDD at once) — **61.0%** once the 8 identity rungs are
  removed.  Not 90 of 90.  The available simultaneous improvement on a dominated book
  averages **+1.92 pp/yr of CAGR and +6.59 pp of MaxDD** (max +6.78 / +38.29).
* **VOLTGT (constant-volatility targeting) sits STRICTLY OUTSIDE the frontier on 10 of 10
  large-cap cells** (U56 and B136, all five rungs each), full sample **and** on 2017-2026
  read alone — vertical gap +0.93 to +2.70 pp/yr of CAGR at the device's own MaxDD, and
  **+1.29 to +3.61 pp of MaxDD at the device's own CAGR**.  All 15 VOLTGT cells give the
  same verdict in both windows.  On SMALL it is inside the frontier 5 of 5, both windows.
* **STOP is the carrier of 1534's pooled effect and it is the worst family here too**: 13 of
  15 dominated, mean vertical gap **-2.29 pp/yr**, mean horizontal gap **-13.07 pp** of
  drawdown.  A trailing-equity stop on this book buys nothing and costs a great deal.
* **33 of 90 device books end up DEEPER than the un-overlaid BASE book they overlay**, so no
  de-gross rung reaches their drawdown at all; 25 of those 33 are dominated outright.  An
  overlay that withdraws exposure made the drawdown worse in more than a third of cells.

## Numbers the record should carry

| statistic | full sample | 2017-2026 alone |
|---|---|---|
| strictly dominated by the de-gross frontier | 50 of 90 (55.6%) | 39 of 90 (43.3%) |
| … agreement between the two windows | — | **77 of 90 (85.6%)** |
| vertical CAGR gap at matched MaxDD (pp/yr) | n 57, mean -0.32, median +0.00 | n 62, mean +0.04, median +0.00 |
| horizontal MaxDD gap at matched CAGR (pp) | n 74, mean **-4.25**, median -1.05, 67.6% negative | — |
| VOLTGT vertical gap (pp/yr) | mean **+0.90**, median +1.39 | mean **+0.85**, median +1.26 |
| STOP vertical gap (pp/yr) | mean **-2.29** | mean **-2.55** |

**1534 RESTATED EXACTLY** (matched-gross anchor re-run on this ladder, one backtest per
device at the interpolated f): d_Sharpe **-0.0787**, d_CAGR **-0.82 pp**, d_MaxDD
**-1.43 pp** — replicating 1534's -0.0727 / -0.69 / -1.55 to within a tenth of a pp.  New
caveat for the record: **8 of 1534's 90 pairs are IDENTITY rungs** (MAXVOL m=0.60, MADIST
k=0.00, STOP d=0.20 on the panels where the stop never fires) whose paired difference is
**0 by construction**, shrinking any pooled mean toward zero.  Ex-identity the effect is
LARGER, not smaller: d_Sharpe -0.0869, d_CAGR -0.91 pp, d_MaxDD -1.58 pp (n 77).

## Gates (all asserted with their realised value)
13 of 13 pass.  G0 SMALL blow-up screen: **54 tickers with `max_1d_move >= 1.0` dropped**
before anything else (666 columns priced).  G1 MaxDD monotone deeper in f on all three
panels (max violation -0.0034 / -0.0037 / -0.0050, all <= 0, so the ladder is invertible on
drawdown).  G2 gross strictly increasing in f.  G4 ladder top reproduces the base book
exactly (|delta gross| = 0.00e+00).

## KEEP paths — 334 published books
**4a: 0 of 334.**  The thirteenth consecutive zero in this record; no book on this shape has
ever cleared the live RULES v2 drawdown at a higher Sharpe in both halves.
**4b (FULL and OOS): 90 of 334**, of which **18 are device books the frontier does NOT
dominate** — 12 on U56, 6 on B136, none on SMALL.

## RULE 8 (parameters chosen on 2009-2016 ONLY, 2017-2026 read ONCE)
Two rulers published side by side, IS Sharpe and IS Calmar, over two pools:

| | U56 | B136 | SMALL |
|---|---|---|---|
| de-gross chooser, OOS Sharpe | 1.1131 / 1.1133 | 0.9498 | **0.4669 / 0.4632** |
| device chooser, OOS Sharpe | 1.1113 / 1.1094 | **1.0124** | **-0.0199** |
| de-gross minus device | +0.0018 / +0.0039 | -0.0626 | **+0.4867 / +0.4831** |

De-gross wins **4 of 6** (panel x ruler) families, mean **+0.1417** of OOS Sharpe — but the
pooled win is carried entirely by SMALL, where the device chooser picks `MAXVOL m=0.25` and
that book goes **negative out of sample (-0.81%/yr, Sharpe -0.0199, MaxDD -33.54%)**.  On
U56 the two pools are a tie to three decimals; on B136 the device pool wins.  **The frontier
is not a better chooser; it is a safer one.**

## Verdict: **KILL of the general law, KEEP-4b candidate recorded and NOT recommended**
KILL: "de-gross dominates every device on the drawdown axis" is refused — it holds for five
families of six and fails on VOLTGT at 10 of 10 large-cap cells in both windows.
The rule-8-reachable candidate is **U56 VOLTGT v = 0.20** (IS Sharpe AND IS Calmar both pick
it, on all three panels): full 12.25% / 1.0741 / -16.70%, halves 1.0937 / 1.0609, OOS
13.39% / 1.1238 / **-16.70%** against SPY's 15.14% / 0.8851 / -33.72% and OOS 15.29% /
0.8751 / -33.72%.  It clears every 4b leg with margin (CAGR +1.65 pp over the 10.60% floor,
MaxDD +3.53 pp inside the -20.23% cap).  **NOT recommended**, for two disclosed reasons:
(1) **grid-edge** — v = 0.20 is the loosest rung offered, the record's standing flag for a
chooser that is really declining to act; (2) **it barely binds** — realised gross 0.7174
against the base book's 0.7196, i.e. 0.3% of exposure withdrawn, so almost all of its 4b
pass is the frozen anchor's, already in the record.  The interesting VOLTGT rungs
(v = 0.08-0.15, which genuinely de-risk to -10.8% .. -15.1% MaxDD) are **not** rule-8
reachable: no legal IS-only ruler picks them.

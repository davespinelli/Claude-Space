# Idea 44 — position-count-broad-confirm: does idea 2's 4b KEEP survive a universe change?

**Verdict: KILL as a KEEP. The published n=20 cell does NOT survive the move to B136, the cells that
do clear 4b there are reachable only by widening to n>=40, and every pass on both panels evaporates
at 25 bps. 4b 11/128, 4a 0/128.**
Script `research/backtests/2026-09-07_position-count-broad-confirm_B.py`
(+ `.grid.csv`, `.walkforward.csv`, `.console.txt`). 2 panels x 2 cost rungs x 2 weighting
conventions x gross x n = 128 cells, all reported. Two tuned parameters: **n** in
{5,10,20,30,40,60,80,ALL} and **gross** in {0.50,0.75,1.00}. Pre-registered anchor = idea 2's own
cell, n=20 / g=0.75. Weekly, next-day execution, RULES v1 eligibility, vol scaler OFF.

## 1. The answer to the question as asked

**No.** Idea 2's published cell reproduces exactly and fails: on B136 at 10 bps,
`FIXED n=20 g=0.75` = **13.09% / 0.957 / -20.05%**, halves 1.125 / 0.811, against SPY's H2 of 0.834
— **4b fails on H2 by -0.0227**, which is the 0.02 gap the queue recorded. On U56 the same cell
passes (12.66% / 1.092 / -18.31%, halves 1.088 / 1.102), so the published KEEP is a **home-universe
result**. Mean Sharpe across the 64 matched (convention, gross, n, cost) cells is 0.898 on B136
against 0.970 on U56, and **B136 is the lower of the two in 64 of 64**.

## 2. Where 4b does clear on B136 — and what it costs to get there

At 10 bps and g=0.75 only: **n = 40, 60, 80, ALL** (NORM), and n = 40, 60 under idea 2's own FIXED
weighting. The best is `n=80, g=0.75`: 11.20% / **1.0245** / -18.44%, halves 1.112 / 0.943, OOS
Sharpe 1.045 vs SPY's 0.882. So the KEEP's *form* survives the universe change but its *parameter*
does not: the fix is the width dial, moving n from 20 to >=40, which is ideas 46/318/320's territory,
not a confirmation of idea 2.

The margins are thin. Tightest bar per pass: DD +0.0112 (n=40), CAGR +0.0072 (n=60), CAGR +0.0054
(n=80), **CAGR +0.0004** (n=ALL — four basis points of CAGR). None of these is a comfortable pass.

## 3. Everything dies at 25 bps — queue idea 323's premise, confirmed on a third grid

**0 of 64 cells pass 4b at 25 bps**, on either panel, at any n or gross. At that rung B136 fails a
Sharpe bar in 24/24 cells and U56 in 24/24; even idea 2's own U56 KEEP fails (H1 -0.0031). Every 4b
pass this grid produces lives at PROTOCOL's own 10 bps anchor. That is the same wall idea 45 hit
(breakevens 24.7 bps on U56, 7.7 bps on B136) reached from a different axis.

## 4. The gross band is one rung wide, and idea 326's mechanism holds with the opposite verdict

Sharpe is gross-invariant as idea 326 derived: the span over a 2x gross range is <= **0.0096** in
96/96 NORM cells (median 0.0021), while Calmar moves 0.000-0.031. Consequently `g=0.50` fails the
**CAGR floor** in 16/16 B136 cells and `g=1.00` fails the **DD cap** in 16/16 — only g=0.75 admits
anything, and it was the pre-registered value. But unlike SMALL439, B136 **clears** idea 326's
gross-invariant Calmar bar (1.1667 x Calmar_SPY = 0.5270) in 24/24 cells at 10 bps, best 0.708. On
this panel the DD cap is satisfiable and the binding bar is **H2 Sharpe** — so the 326 caveat should
be stated as *check the Calmar bar before blaming DD*, not as *DD is never the real bar*.

## 5. The convention matters, as idea 244 said

Idea 2's FIXED `gross/n` weight silently de-grosses wide books: realised gross falls 0.745 -> 0.504
on B136 and 0.741 -> **0.351** on U56 as n goes 5 -> 80. Holding realised gross at 0.75 (NORM)
removes up to 0.12 of Sharpe from the wide U56 cells (n=80 @25bps: FIXED 1.047 vs NORM 0.924) and
adds up to 3.8 pp of CAGR. The n dial under FIXED is **partly a gross dial**; the passes reported
above under NORM are the honest ones.

## 6. Rule 8: the passing arms are not selectable

(n, gross) chosen on 2008-2016 by IS Sharpe, 2017-2026 read once. On **B136 @10 bps the chooser
picks n=10 / g=1.00 and gets OOS 16.72% / 0.785 / -27.95%** — below SPY (0.882), below the n=20
anchor (-0.0986), and **0.261 of regret** behind the OOS-best cell (n=80 / g=0.50, 1.046). It picks
the anchor exactly on U56 @10 bps. Across the four (panel, rung) cells the chooser beats the anchor
**1/4**, the pool mean 3/4, SPY 3/4 and RULES v2 **0/4**. The wide arms that clear 4b are found by
looking at the whole sample; nothing in the record's own selection machinery finds them prospectively.

## 7. 4a

**0 of 128.** RULES v2 live is 8.03% / 1.106 / -12.24% on B136 (halves 1.229/0.984) and
1.206 on U56; no cell beats both half-Sharpes with a no-worse drawdown. Consistent with the record.

## Caveats
- Both universes are **current-constituent lists** (survivorship): CAGR levels are optimistic, so the
  CAGR-floor passes at n=60/80/ALL (margins 0.0072 / 0.0054 / 0.0004) are the least trustworthy
  numbers here and would likely flip on a point-in-time list.
- `data/prices*.csv` are still on a **calendar-day index** (queue idea 38, unfixed): equities are
  ffilled across weekends, so vol20 and the weekly mask run on a 7-day week. It hits both panels
  identically and is a level effect, not an n effect.
- The 25-bps column is a reporting rung, not a third tuned parameter; the tuned pair is (n, gross).

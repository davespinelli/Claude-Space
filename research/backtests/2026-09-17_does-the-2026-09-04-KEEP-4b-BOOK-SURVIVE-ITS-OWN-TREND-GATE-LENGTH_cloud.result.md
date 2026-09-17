# 1256 (lane cloud, 2026-09-17) — does the 2026-09-04 KEEP 4b book survive its own trend gate length?

**ANSWER: NO — THE 4b VERDICT IS A PROPERTY OF THE INHERITED 200, NOT OF THE BOOK.**
Pre-declared outcome (B) lands; (A) and (C) both fail.

## What was run
The frozen 2026-09-04 candidate (U56, composite 21/252 + 0/126 + 0/63, no vol scaler,
vol20 < 0.60, N = 20 equal weight, H = 126, GROSS = 0.75, cash for gated-out weight, weekly,
10 bps, t+1) with its trend gate replaced by the hysteresis state G(L, b) — IN above
MA_L*(1+b), OUT below MA_L*(1-b), previous state in between. Two dials and no more:
L ∈ {50, 100, 150, 200, 250}, b ∈ {0.00, 0.01, 0.03, 0.05, 0.10} = 25 cells per panel,
75 in all, **every one published** (`.grid.csv`). Anchor = (200, 0.00), which replays the
committed U56 triple to 4.65e-05.

## The five numbers that decide it (U56)
| cell | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR / Sharpe / MaxDD | 4b |
|---|---|---|---|---|---|---|
| **200 / 0.00 (anchor)** | 15.71% | 1.1480 | -19.13% | 1.2127 / 1.1050 | 17.16% / 1.1759 / -19.13% | **PASS** |
| 250 / 0.00 | 15.41% | 1.1226 | **-21.55%** | 1.2165 / 1.0651 | 17.23% / 1.1529 / -21.55% | FAIL (DD) |
| 150 / 0.00 | 15.50% | 1.1332 | -19.84% | 1.2542 / 1.0514 | 16.94% / 1.1464 / -19.84% | PASS |
| 100 / 0.00 | 14.55% | 1.0992 | -19.67% | 1.3684 / 0.8987 | 14.15% / 1.0052 / -19.67% | PASS |
| 50 / 0.00 | 13.09% | 1.0358 | -19.23% | 1.2333 / 0.8946 | 13.43% / 0.9927 / -19.23% | PASS |
SPY on the same window: 15.06% / 0.8815 / -33.72%, halves 0.9600 / 0.8171, OOS 15.15% / 0.8686.
LIVE RULES v2: 8.60% / 1.1982 / -12.05%, OOS 9.42% / 1.2717.

## Headline
- **U56: 4b passes 12 of 25 cells, fails 13. B136: 13 of 25. SMALL663: 0 of 25.**
  The verdict flips inside the dial the record never walked.
- **EVERY U56 AND B136 FAILURE FAILS ON THE DRAWDOWN LEG AND ONLY THE DRAWDOWN LEG**
  (H1 = H2 = OOS = CAGR fail 0 of 25 on both panels). The return case is gate-length-free;
  the risk case is not. 4b's DD cap is -20.23% and the grid runs -18.90% .. -23.41%.
- **L = 250 fails 4b at every band on U56; L = 200 fails at every band on B136.** A longer
  gate is not a safer gate: the book's own MaxDD worsens with L while CAGR barely moves.
- **A WIDER BAND IS STRICTLY WORSE ON THE COMMITTED RUNG.** At L = 200 the OOS Sharpe falls
  monotonically 1.1759 → 1.1440 → 1.1247 → 1.0659 → 1.0364 as b goes 0.00 → 0.10, and 4b
  fails from b = 0.05 up. The live RULES v2 ±3% clause is not free on this book.
- **THE ANCHOR IS NOT TYPICAL, IT IS NEAR THE TOP.** 200/0.00 sits at the 84th percentile of
  its own grid on full Sharpe and the 88th on OOS Sharpe (median cell 1.1190 / 1.1193). It is
  inside its local neighbourhood (150/250 × 0.00/0.01 spans 1.1126..1.1524), so outcome (C)
  fails — but a committed number drawn from the top sixth of a 25-cell grid nobody walked is
  a selection the record never priced.

## Rule 8 (walk-forward), the part that matters
(L, b) chosen on warm-up..2016-12-31 by IS Sharpe alone; 2017-2026 read ONCE.
| panel | IS argmax | IS Sharpe | OOS Sharpe | grid-mean | worst | anchor | IS/OOS rank corr |
|---|---|---|---|---|---|---|---|
| U56 | L=100, b=0.01 | 1.2722 | 1.0567 | 1.1037 | 0.9298 | **1.1759** | **-0.3746** |
| B136 | L=200, b=0.10 | 1.3828 | 1.1497 | 1.0583 | 0.9886 | 1.0240 | +0.1877 |
| SMALL663 | L=100, b=0.00 | 0.6896 | 0.4030 | 0.4391 | 0.4030 | 0.4534 | **-0.5404** |
Pooled: IS-chosen OOS Sharpe 0.8698 vs grid mean 0.8670 (**+0.0028**) vs anchor 0.8845
(**-0.0146**). **CHOOSING THE GATE LENGTH IN-SAMPLE IS WORTH NOTHING AND LOSES TO DOING
NOTHING**; on U56 it picks the single worst-transferring rung in the grid and the IS/OOS rank
correlation is negative on two of three panels. The spread across rungs is implementation
risk, not an opportunity.

## Both KEEP paths
- **4a: 0 of 75 grid points.** Unchanged from the record — every cell's MaxDD is worse than
  live RULES v2's -12.05%.
- **4b: 12 / 13 / 0 of 25 (U56 / B136 / SMALL663).** The anchor passes on U56 only.
- **NO NEW BOOK, NO MEMO, NO RULES CHANGE.** Nothing here beats the incumbent; the finding is
  that the incumbent's own margin is thinner than the record states.

## Survivorship (rule 9)
U56 and B136 are CURRENT-constituent lists; SMALL663 is a current sub-$2B screen (52 of 715
dropped for max_1d_move ≥ 1.0 before anything was computed). Every level is optimistic and
every 4b pass is an upper bound. The headline is a SPREAD ACROSS GATE RUNGS of the same book
on the same panel, first-order immune to a common level bias; the levels are not.

## What the record should take, in one sentence
**A 4b VERDICT SHOULD QUOTE THE GATE LENGTH IT WAS DECIDED AT, AND A CANDIDATE WHOSE PASS
DOES NOT SURVIVE ±50 DAYS OF ITS OWN INHERITED TREND WINDOW SHOULD BE RECORDED AS
GATE-CONTINGENT** — proposed for the Sunday review (rule 6) as a PROTOCOL reporting line
only, never as a chooser (rule 8 shows choosing on this dial is negative-value).

Script: `research/backtests/2026-09-17_does-the-2026-09-04-KEEP-4b-BOOK-SURVIVE-ITS-OWN-TREND-GATE-LENGTH_cloud.py`
Console: `..._cloud.console.txt` · Grid: `..._cloud.grid.csv` · Walk-forward: `..._cloud.walkforward.csv`

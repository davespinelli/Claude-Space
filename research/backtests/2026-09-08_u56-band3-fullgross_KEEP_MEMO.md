# KEEP-candidate memo — U56, RULES v2 gate at FULL gross (path 4b, u56 only) — AND ITS PRICE

1. **Origin:** idea 423, pre-registered 2 dials only (gross x cadence; band FIXED at v2's 3%),
   90 grid points reported. Replaces the 30-arm menu that produced the 2026-09-08 memo.
   Not adopted — Sunday review decides. Gates: vectorised twin vs `engine.backtest` **1.3e-16**;
   `(gross=0.75, W)` reproduces `baseline.rules_v2_weights` **weight-for-weight at 0.000e+00**;
   idea 420's by-product headline reproduces **exactly** (11.96%/1.2126/-15.49%, OOS 12.72%/1.2750).
2. **Book:** RULES v2 verbatim with ONE clause deleted — the 0.75 de-gross. Hold every instrument
   priced that day inside/above its 200d MA **3% hysteresis band**, equally weighted at 100% of NAV,
   gated-out weight to CASH. Panel = `research/universe.json` (U56). No ranking, no vol filter.
3. **Full sample (2009-01-13..2026-09-04, 10 bps, t+1), weekly:** CAGR **11.59%**, Sharpe **1.2055**,
   MaxDD **-15.91%**, halves 1.226/1.190. Monthly: 11.96% / 1.1781 / -18.81%. At 25 bps: 11.19% /
   1.1681 / -15.96% (W) and 11.68% / 1.1536 / -18.84% (M).
4. **Rule 8 (dials on IS <= 2016-12-31 by IS Sharpe, 2017-.. read once):** the chooser picks
   **gross=1.00, monthly** at both rungs — OOS **12.93% / 1.2336 / -18.81%** (10 bps), 12.65% /
   1.2095 / -18.84% (25 bps). The weekly arm it passed over is better OOS (12.78% / 1.2844 /
   -15.91%): the IS chooser gave up **0.051 OOS Sharpe and 2.9 pp of drawdown** — the record's
   n-th "selection loses to doing nothing" instance.
5. **4b bars (SPY OOS 15.45% / 0.8820 / -33.72%):** Sharpe > SPY both halves and OOS ✓;
   CAGR 12.93% >= 10.82% floor ✓; MaxDD -18.81% <= -20.23% cap ✓. **PASSES 4b on the full sample
   and OOS at 10 and 25 bps, u56 only.** Headroom on the binding bar (MaxDD) is only **1.4 pp**,
   against 4.7 pp for the un-banded memo book: fixing the band at v2's own 3% costs 3.3 pp of
   drawdown, so the 2026-09-08 memo's cushion was a property of the plain-MA gate, not of gross.
6. **4a: FAILS everywhere** (0/90 grid points on u56/broad136; the only 4a passes in the whole grid
   are 4 small439 arms at gross 0.50-0.625 monthly). Full-sample BOTH-PATHS = **0/90**.
7. **THE PRICE — the deleted clause is 100% EXPOSURE (ideas 296/304 decomposition).** Against the
   zero-parameter constant-leverage replay `c x r(gross=0.75)`, c = 1.00/0.75, over 18
   (panel x cadence x rung) cells: exposure explains **99.6%** of dCAGR [98.4-102.1%] and **97.6%**
   of dMaxDD [92.1-100.9%]; daily-return corr >= **0.99978**; **dSharpe = -0.0006 mean, |max| 0.0051,
   positive in 9/18** — a coin. Deleting the de-gross clause buys **no risk-adjusted return at all**.
8. **What that means for the 4b verdict:** this book is not better than the live book, it is the
   live book held at **1.333x**. It clears 4b only because 4b's CAGR floor is clearable by exposure
   alone, which is also why nothing in the grid passes both paths. Any adoption should be argued as
   a **gross decision** (75% -> 100% of NAV), not as a new strategy.
9. **Scope limits and caveats:** on broad136 the same arm clears 4b full-sample at 10 bps but FAILS
   OOS (10.66% CAGR < 10.82% floor) and fails at 25 bps; on SMALL439 it fails at every rung
   (5.76% / 0.6222 / -21.86% OOS). U56 is a fixed current list and broad/small carry survivorship
   (`data/SMALL_PANEL_README.md`); the grid is 90 points, so the u56 pass is 1 of 3 panels.
10. **Exact RULES wording if adopted:** *"Each week, hold every instrument in the universe whose
    close is inside or above its 200-day moving-average band (IN above ma x 1.03, OUT below
    ma x 0.97, previous state in between), equally weighted, investing 100% of NAV across those
    names; hold the remainder in cash. No ranking, no volatility filter, no de-grossing. Rebalance
    weekly at the next close after the signal date."* This is RULES v2 with clause "gross = 75%"
    replaced by "gross = 100%" and nothing else.

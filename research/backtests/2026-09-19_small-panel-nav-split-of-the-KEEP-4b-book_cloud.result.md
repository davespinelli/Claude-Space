# Idea 1645 (lane cloud, 2026-09-19) — does the SMALL-PANEL BOOK ADD ANYTHING to the U56 BOOK at CONSTANT TOTAL GROSS?

**VERDICT: KILL.** Not one of the 30 interior NAV splits beats its own constant-gross U56 corner
on anything, at any cost rung, on any window. dSharpe > 0 in **0 of 30** at 0/10/25/50 bps
(mean −0.3265 / −0.3288 / −0.3322 / −0.3380), OOS dSharpe > 0 in **0 of 30** (mean −0.3995 at
10 bps), dCAGR **−4.11 pp/yr** and dMaxDD **−8.61 pp (DEEPER)**. 4b clears at 2 of 33 cells and
both are the **w = 1 corner** (i.e. the incumbent U56 book itself, at G = 0.50 and G = 0.75);
**0 of the 33 interior cells clear 4b**, 4a clears **0 of 33**, and **0 of 8** legal IS-only
choosers picks any w < 1.0 at any cost rung.

## What was asked, and what this is not a re-run of
Lane B's idea **1653** is 1645's full capital arm; it split the **LIVE RULES v2 BAND book** across
U56 × SMALL at constant total gross and KILLed it (dSharpe > 0 in 0 of 30 paired cells). It did
**not** split the book that matters for real capital — the **2026-09-04 KEEP-4b candidate**
(top-N equal weight, no vol scaler, 126-row min hold, weekly, t+1). This run asks 1645's question
of that book. The two answers agree, which is the point: the cross-panel-reallocation family is
retired on both of the record's live books, not just one.

## Construction (no convention invented)
Each sleeve is the 2026-09-04 recipe at **N = 20** built on its own panel's full price history;
the two unit-gross **held frames** are reindexed onto the common trading-day index and combined
into ONE target weight matrix `W(t) = w·G·W_U56(t) + (1−w)·G·W_SMALL(t)`, run through ONE engine
pass over the union of the two panels' weekly application rows with drift in between. Turnover is
therefore the portfolio's own Σ|dw| — no sleeve-rebalancing convention is assumed. Total target
gross is **G at every w by construction**, so the **w = 1 corner IS the realised-gross-matched
de-gross twin** of every interior cell: measured |Δ mean realised gross| across all 30 pairs is
**≤ 2.69e-04**. Any gain at w < 1 would have been pure reallocation and could not have been a
re-gross. There was no gain.

**Two dials and no more (rule 4):** `w ∈ {0.0 … 1.0}` (11 rungs) × `G ∈ {0.50, 0.75, 1.00}`
(3 rungs) = 33 cells, every one published at four cost rungs (132 readings, `.grid.csv`).
Cost rung and window are published axes, not dials. Frozen: N = 20, H = 126 min hold, weekly Fri
decision, t+1 (rule 2), above-200d & vol20 < 0.60, 3-leg composite, equal weights, cash at 0%.

## Sample and benchmarks (common index 2011-01-13 … 2026-09-18, 3943 rows, 15.6y)
| series | CAGR | Sharpe | MaxDD | H1 | H2 | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|---|---|
| SPY buy & hold | 14.03% | 0.8567 | −33.72% | 0.9041 | 0.8391 | 15.26% | 0.8737 | −33.72% |
| RULES v2 (live, 10 bps) | 8.14% | 1.1636 | −12.05% | 1.0661 | 1.2534 | 9.46% | 1.2766 | −12.05% |

4b bars: FULL MaxDD cap −20.23%, CAGR floor 9.82%; OOS cap −20.23%, floor 10.68%.

## The corners, at the binding 10 bps rung
| G | w | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR | OOS Sharpe | J_FULL | J_OOS | 4a | 4b |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.75 | 0.0 (pure SMALL) | 7.85% | 0.5112 | −36.49% | 0.683 / 0.383 | 6.72% | 0.4407 | −16.26 | −16.26 | no | no |
| 0.75 | 0.5 | 11.75% | 0.8330 | −26.63% | 0.936 / 0.758 | 12.15% | 0.8278 | −6.40 | −6.40 | no | no |
| 0.75 | 1.0 (pure U56) | 15.38% | 1.1271 | −19.13% | 1.137 / 1.130 | 17.34% | 1.1862 | +1.10 | +1.10 | no | **yes** |

Every column is **monotone in w** on all three axes at every G: moving capital toward the small
panel costs Sharpe, costs CAGR *and* deepens drawdown. The SMALL sleeve is not weakly-correlated
diversification that pays for itself — on this tape it is strictly dominated.

## Rule 8 (dials chosen on IS ≤ 2016-12-31 only; 2017-2026 read once)
| cost | chooser | pick (w, G) | IS Sharpe | OOS CAGR | OOS Sharpe | OOS MaxDD | dOOS Sharpe vs own corner | 4b |
|---|---|---|---|---|---|---|---|---|
| 10 | IS_SHARPE | (1.0, 1.00) | 1.0246 | 23.23% | 1.1870 | −24.93% | +0.0000 | no |
| 10 | IS_J | (1.0, 0.50) | 1.0232 | 11.48% | 1.1852 | −13.05% | +0.0000 | **yes** |
| 25 | IS_J | (1.0, 0.50) | 0.9885 | 11.16% | 1.1548 | −13.12% | +0.0000 | **yes** |
| 50 | IS_J | (1.0, 0.50) | 0.9306 | 10.63% | 1.1041 | −13.23% | +0.0000 | no |

Both declared choosers pick **w = 1.0 at every one of the four cost rungs** — the pure U56 corner,
i.e. no split at all. `dOOS = +0.0000` because the pick *is* its own comparand. The pre-registered
pass for this idea (chosen cell beats its own corner OOS on Sharpe AND CAGR) fires **0 of 8**.

## Caveats, stated rather than buried
- **Survivorship (rule 9).** Both panels are current-constituent lists. SMALL is a current
  constituent sub-$2B screen (665 investable after dropping 54 tickers with `max_1d_move ≥ 1.0`
  per `data/small_meta.csv`), so its delisted, acquired and bankrupt names are absent. The bias is
  **worst on the small panel**, so the SMALL sleeve's numbers here are an **upper bound**. A KILL
  of the split is therefore the **stronger** reading, not the weaker one.
- **Window.** The common index starts 2011-01-13 (SMALL's cache plus warm-up), 15.6y, so the U56
  corner readings here are **not** comparable to the record's certified anchor (idea 1293, N = 20,
  g = 0.65: 13.66% / 1.1526 / −16.73% on U56's own longer history). Nothing here re-certifies the
  incumbent; the corners are comparands, not results.
- The two 4b passes at the w = 1 corner are the incumbent candidate at G = 0.50 and G = 0.75 on
  this shorter window. They are **not a new book** and no memo is written for them.

Artifacts: `.grid.csv` (132 cost readings), `.twins.csv` (120 interior-vs-corner pairs),
`.walkforward.csv` (8 rule-8 picks), `.console.txt`.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

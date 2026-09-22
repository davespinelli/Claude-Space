# idea 2315 (lane cloud, 2026-09-22) — WHEN does the BAND GATE pay for itself?

**ANSWERED = IN A MINORITY OF YEARS, AND THE SAVING IS CRISIS-CONCENTRATED. The queue's own
characterisation ("a device that earns its keep in 3 of 18 years is a crash hedge priced as a
strategy") is CONFIRMED at the neutral exchange rate — the live cell earns its keep in 6 of 18
years, and 46.7% of every point of drawdown it ever saved comes from 2009 / 2020 / 2022.
NO NEW KEEP: 4a 0 of 168 rows at every rung above zero, and the 34 4b passes are all the already
committed gross-1.00 gated family, reproduced in place.**

## The two books
`GATED(c, g)` = the live RULES v2 book (`baseline.rules_v2_weights`, gated weight stays in cash).
`UNGATED(g)` = the same equal-weight book with clause 2 deleted: `g / N_t` on every priced name,
every day. Identical names, gross, weekly cadence, t+1 execution and cost rung. Two tuned dials
and no more: **band width c {0.00, 0.02, 0.03 live, 0.05, 0.08, 0.10} and gross {0.75, 1.00}**.
Panels (U56 / B136 / SMALL), the four rungs {0, 10, 25, 50} bps and the cadence are REPORTED,
never selected on. 14 books x 3 panels x 4 rungs = 168 published rows.

## The pre-declared price (stated before any number was read)
For each calendar year `y`: `DRAG_y = ret_UNGATED_y - ret_GATED_y`;
`SAVED_y = mdd_GATED_y - mdd_UNGATED_y` (within-year MaxDD, both negative, so + = DD saved);
the gate is **worth its price** iff `lam * SAVED_y >= DRAG_y`, with `lam = 1.0` (one pp of
drawdown avoided is worth one pp of return given up) as the headline and {0.5, 1, 2, 3} reported.

## The ledger (U56, live cell c = 0.03 / gross 0.75, 10 bps, 2009-01-13 .. 2026-09-22)
| | |
|---|---|
| years the gate is worth its price, lam = 0.5 / **1.0** / 2.0 / 3.0 | 4 / **6** / 10 / 11 of 18 |
| total drag paid | **+85.59%** (mean +4.75%/yr) |
| total within-year drawdown saved | **+64.39%** (mean +3.58%/yr) |
| years the gate COST return | **16 of 18** (+93.47% total); it added return in 2 (2018, 2022) |
| share of all DD saved from 2009 / 2020 / 2022 | **46.7%** (3 of 18 years) |
| the 3 best years for the gate | 2022 +11.00%, 2020 +10.47%, 2009 +8.59% — the same 3 years |
| mechanism split of the daily difference | PROT (ungated-down days) **+397.9%**, DRAGUP (up days) **-478.7%** |
| OOS leg (2017-2026 only, read once) | worth its price in **3 of 10** years; drag +44.63%, saved +37.52% |

The count is stable across the grid and never reaches half at lam = 1.0 on either large-cap panel:
U56 5/5/**6**/5/5/7 of 18 and B136 5/5/**5**/5/4/4 of 18 across c = 0.00 .. 0.10 (identical at
both gross rungs — the year-level verdict is a band-width object, not a gross object). SMALL is
the only panel where it climbs, to 8 of 16.

## Books, at the headline rung (U56, 10 bps)
| book | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR / Sharpe | 4a | 4b |
|---|---|---|---|---|---|---|---|
| GATED c=0.03 g=0.75 (the live rule) | 8.65% | 1.2052 | -12.05% | 1.23 / 1.19 | 9.51% / 1.2839 | . | . (L_CAGR) |
| UNGATED g=0.75 | 13.24% | 1.1228 | -22.53% | 1.19 / 1.07 | 13.76% / 1.1334 | . | . (L_DD) |
| GATED c=0.03 g=1.00 | 11.57% | 1.2050 | -15.91% | 1.23 / 1.19 | 12.75% / 1.2832 | . | **Y** |
| UNGATED g=1.00 | 17.70% | 1.1232 | -29.18% | 1.19 / 1.07 | 18.40% / 1.1330 | . | . (L_DD) |
| SPY | 15.23% | 0.8897 | -33.72% | — | 15.45% / 0.8831 | — | — |

So the gate buys **+0.08 Sharpe and 10.5 pp of MaxDD for 4.6 pp of CAGR** at gross 0.75, and the
whole of that Sharpe gain survives only because the drawdown saving lands in three years. The
4b ledger over all 168 rows: **4b 34, 4a 8 (all 8 at the zero-cost rung, 0 at 10/25/50 bps),
UNGATED 0 of 24 on both paths** — every ungated row fails on `L_DD` and every gated-0.75 row
fails on `L_CAGR`.

## Rule 8 (dials fitted on <= 2016-12-31, 2017-2026 read once)
24 picks (3 panels x 4 rungs x {C_ISSHARPE, C_ISCALMAR}). **0 of 24 land on the live cell** —
every pick takes gross 1.00 and a WIDER band (c = 0.10 at 14 of 24, c = 0.02/0.03/0.08 elsewhere).
The picks beat the ungated book's OOS Sharpe at **14 of 24**, i.e. the gate's out-of-sample
Sharpe edge is close to a coin flip once the band width has to be chosen without hindsight. Every
pick still loses to the ungated book on OOS CAGR, at 24 of 24.

## Gates — 11 of 11 pass
G0 >= 10y per panel (17.7 / 17.7 / 15.7y). G1 the per-column replica equals `engine.backtest`
(max|d| 0.00e+00). G2 the band dial bites (mean IN share 0.6499 at c=0 -> 0.6298 at c=0.10).
G3 UNGATED carries no band dependence. G4 no leverage (max row sum 1.000000000). G5 exactly two
tuned parameters. G6 SMALL dropped-ticker rule bit (54 names dropped at max_1d_move >= 1.0).
**G7 reproduces RULES.md's committed v2 acceptance row** (8.66%/1.2056/-12.05%, 1.2259/1.1908,
OOS 1.2851) to max|d| 1.16e-04. G8 the year partition is exhaustive (|d| 2.8e-14 over 18 years).

## Caveats, stated not buried
- **The 2008 leg of the GFC is outside this sample.** The panels start 2008-01-01 and the 260-row
  warm-up puts the first scored day at 2009-01-13, so "2009" here is the tail of the crash plus
  the recovery. The gate's best single crisis is therefore almost certainly UNDERSTATED, and the
  concentration finding is if anything conservative.
- **Survivorship.** U56 and B136 are current-constituent lists; SMALL is a current screen (665
  names after dropping 54 at `max_1d_move >= 1.0`). Absolute CAGRs are optimistic on all three.
  The gated-minus-ungated difference is a same-names, same-days object and is far less exposed.
- The within-year MaxDD is not the book's lifetime MaxDD; a multi-year drawdown is split across
  its calendar years by construction. That is the price of a year-by-year ledger and it is why
  the aggregate MaxDD column is published beside it.

Script: `research/backtests/2026-09-22_band-gate-year-by-year-decomposition_cloud.py`
Outputs: `.grid.csv` (168 rows) `.yearly.csv` (624 year-rows) `.counts.csv` `.exposure.csv`
`.walkforward.csv` `.gates.csv` `.log.txt`

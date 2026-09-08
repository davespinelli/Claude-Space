# Idea 51 — cash-secured put-writing, forward paper book

Generated 2026-09-07 by `research/putwrite_paper.py` from the `data/options/iv_panel.csv` snapshot of the same date. Book $100,000 notional, cash-secured, max 8 positions, one per ticker, held to expiry. Entries filled at the **bid** (seller crosses the spread) less $0.65/contract.

**Day 1 of the >= 60 trading days idea 51 requires before a verdict.** Nothing here is a result yet.

## Cumulative

| Stat | Value |
|---|---|
| Trading days recorded | 1 |
| Positions opened, all time | 0 |
| Open now | 0 |
| Expired | 0 |
| Assigned | 0 |
| Premium collected (net of commission) | $0.00 |
| Realized P&L | $0.00 |
| Unrealized (open marked to mid) | $0.00 |
| Marked P&L (realized + unrealized) | $0.00 |
| Max drawdown of marked equity | $0.00 |
| Notional deployed | $0 of $100,000 |

## Current book

_No open positions._

## Candidate funnel, 2026-09-07

| Gate | Rows surviving |
|---|---|
| snapshot rows | 186 |
| triage score >= 5 | 34 |
| monthly, 30-45 DTE | 17 |
| iv_src != 'yahoo' | 17 |
| ATM IV - RV20 >= 8 vp | 11 |
| skew > 0 | 5 |
| stale_days <= 2 | 0 |

Opened today: 0.

Nothing qualified, so the rows that pass every gate **except** quote freshness were probed against the live chain:

| Ticker | stale_days | Strikes 10-15% OTM | With a two-sided quote |
|---|---|---|---|
| SBH | 7.3 | 1 | 0 |
| EMBC | 6.4 | 1 | 0 |
| SMPL | 5.8 | 1 | 0 |
| UPBD | 8.8 | 0 | 0 |
| DXC | 5.2 | 1 | 0 |

## Does 'reads well' predict overpriced puts?

Cross-section of every 30-45 DTE monthly row in `iv_panel.csv` with a non-Yahoo IV, bucketed by Deep Value triage score. Positive IV-RV means the option market charges more vol than the stock has recently realised.

| Triage score | Rows | Tickers | Median ATM IV | Median RV20 | Median IV-RV | % with IV-RV >= 8vp | % skew > 0 |
|---|---|---|---|---|---|---|---|
| 3-4 | 9 | 5 | 51.9 | 31.7 | +20.3 | 100% | 44% |
| 5-6 | 22 | 12 | 55.3 | 45.8 | +10.9 | 68% | 59% |
| 7-8 | 10 | 5 | 49.0 | 55.0 | +9.0 | 50% | 20% |
| no triage | 144 | 72 | 26.9 | 21.5 | +3.0 | 19% | 81% |

Spearman rho(triage score, IV-RV spread) = -0.264 over 41 scored rows. Units are vol points.

## Daily series

`research/backtests/putwrite_paper_daily.csv`; positions in `research/backtests/putwrite_paper_positions.csv`.

| Date | Open | Premium to date | Marked P&L | Realized | Max DD |
|---|---|---|---|---|---|
| 2026-09-07 | 0 | $0.00 | $0.00 | $0.00 | $0.00 |

## Log

- near miss SBH: stale_days 7.3, 1 strike(s) 10-15% OTM, 0 two-sided
- near miss EMBC: stale_days 6.4, 1 strike(s) 10-15% OTM, 0 two-sided
- near miss SMPL: stale_days 5.8, 1 strike(s) 10-15% OTM, 0 two-sided
- near miss UPBD: stale_days 8.8, 0 strike(s) 10-15% OTM, 0 two-sided
- near miss DXC: stale_days 5.2, 1 strike(s) 10-15% OTM, 0 two-sided


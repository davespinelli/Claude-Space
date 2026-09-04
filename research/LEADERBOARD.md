# Backtest Leaderboard (10 bps costs, next-day execution; see PROTOCOL.md)
| Date | Idea | CAGR | Sharpe | MaxDD | Sharpe H1 / H2 | Baseline Sharpe (H1/H2) | Verdict | Script |
|---|---|---|---|---|---|---|---|---|
| 2026-09-03 | dual-momentum-classes K=1 monthly | 8.7% | 0.54 | -33.8% | 0.36 / 0.69 | 0.67 (0.64/0.69) | KILL | 2026-09-03_dual-momentum-classes.py |
| 2026-09-03 | dual-momentum-classes K=1 weekly | 5.7% | 0.40 | -36.1% | 0.13 / 0.61 | 0.67 (0.64/0.69) | KILL | 2026-09-03_dual-momentum-classes.py |
| 2026-09-03 | dual-momentum-classes K=2 monthly | 7.1% | 0.57 | -24.1% | 0.39 / 0.72 | 0.67 (0.64/0.69) | KILL | 2026-09-03_dual-momentum-classes.py |
| 2026-09-03 | dual-momentum-classes K=2 weekly | 6.9% | 0.56 | -25.7% | 0.29 / 0.80 | 0.67 (0.64/0.69) | KILL | 2026-09-03_dual-momentum-classes.py |
| 2026-09-03 | inv-vol 75% gross | 5.0% | 0.57 | -14.4% | 0.60 / 0.54 | 0.67 (0.64/0.69) | KILL | research/backtests/2026-09-03_inverse-vol-weights.py |
| 2026-09-03 | inv-vol 100% gross | 6.5% | 0.57 | -19.1% | 0.60 / 0.54 | 0.67 (0.64/0.69) | KILL | research/backtests/2026-09-03_inverse-vol-weights.py |
| 2026-09-03 | equal-weight 100% gross (diagnostic) | 8.5% | 0.67 | -18.2% | 0.65 / 0.69 | 0.67 (0.64/0.69) | KILL | research/backtests/2026-09-03_inverse-vol-weights.py |
| 2026-09-03 | vol-target 10% | 5.8% | 0.59 | -14.9% | 0.59 / 0.58 | 0.67 (0.64/0.69) | KILL | research/backtests/2026-09-03_vol-target.py |
| 2026-09-03 | vol-target 14% | 6.9% | 0.60 | -15.3% | 0.60 / 0.61 | 0.67 (0.64/0.69) | KILL | research/backtests/2026-09-03_vol-target.py |
| 2026-09-03 | broad-top10 100% gross (N=10,w=10%) | 8.6% | 0.67 | -22.1% | 0.86 / 0.51 | 0.64 (0.78/0.53) | KILL | research/backtests/2026-09-03_broad-momentum-top10.py |
| 2026-09-03 | broad-top20 100% gross (N=20,w=5%) | 11.5% | 0.86 | -22.9% | 1.09 / 0.66 | 0.64 (0.78/0.53) | KILL | research/backtests/2026-09-03_broad-momentum-top10.py |
| 2026-09-03 | broad-top10 75% gross (N=10,w=7.5%) | 6.6% | 0.67 | -16.8% | 0.86 / 0.51 | 0.64 (0.78/0.53) | KILL | research/backtests/2026-09-03_broad-momentum-top10.py |
| 2026-09-03 | RULES v1 LIVE (standard universe) — reference, not a new idea | 6.4% | 0.66 | -13.8% | 0.65 / 0.68 | 0.66 (0.65/0.68) | — | research/backtests/2026-09-03_broad-momentum-top10.py |
| 2026-09-03 | macro-trend-ensemble A (MA votes) | 4.7% | 0.83 | -9.2% | 0.69 / 0.98 | 0.66 (0.65/0.68) | KEEP-candidate | research/backtests/2026-09-03_macro-trend-ensemble.py |
| 2026-09-03 | macro-trend-ensemble B (momentum votes) | 5.0% | 0.87 | -10.1% | 0.75 / 0.98 | 0.66 (0.65/0.68) | KEEP-candidate | research/backtests/2026-09-03_macro-trend-ensemble.py |
| 2026-09-03 | A full-exposure 100% gross | 8.4% | 0.66 | -18.2% | 0.65 / 0.68 | 0.66 (0.65/0.68) | KILL | 2026-09-03_full-exposure-v1.py |
| 2026-09-03 | B full-exposure + SPY-200d half | 7.9% | 0.65 | -17.6% | 0.65 / 0.66 | 0.66 (0.65/0.68) | KILL | 2026-09-03_full-exposure-v1.py |
| 2026-09-03 | C full-exposure + SPY-200d cash | 7.3% | 0.62 | -17.6% | 0.64 / 0.61 | 0.66 (0.65/0.68) | KILL | 2026-09-03_full-exposure-v1.py |
| 2026-09-03 | D full-exposure no per-name 200d | 8.2% | 0.66 | -20.4% | 0.69 / 0.64 | 0.66 (0.65/0.68) | KILL | 2026-09-03_full-exposure-v1.py |
| 2026-09-03 | D2 no 200d gate, tilt kept (diagnostic) | 8.5% | 0.67 | -18.2% | 0.65 / 0.68 | 0.66 (0.65/0.68) | KILL | 2026-09-03_full-exposure-v1.py |
| 2026-09-03 | core-plus-sleeve A (60% SPY>200d + 40% sleeve) | 7.8% | 0.86 | -14.7% | 0.80 / 0.92 | 0.66 (0.65/0.68) | KILL | research/backtests/2026-09-03_core-plus-trend-sleeve.py |
| 2026-09-03 | core-plus-sleeve B (60% QQQ>200d + 40% sleeve) | 10.8% | 0.95 | -18.9% | 0.84 / 1.04 | 0.66 (0.65/0.68) | KILL | research/backtests/2026-09-03_core-plus-trend-sleeve.py |
| 2026-09-03 | core-plus-sleeve C (50% SPY>200d + 50% sleeve) | 7.3% | 0.88 | -13.0% | 0.81 / 0.94 | 0.66 (0.65/0.68) | KEEP-candidate | research/backtests/2026-09-03_core-plus-trend-sleeve.py |
| 2026-09-03 | core-plus-sleeve D (60% SPY no filter + 40% sleeve) | 11.3% | 0.93 | -24.1% | 0.97 / 0.90 | 0.66 (0.65/0.68) | KILL | research/backtests/2026-09-03_core-plus-trend-sleeve.py |
| 2026-09-03 | qqq-trend-only A (QQQ/SHY, 200d, weekly) | 14.4% | 0.91 | -27.5% | 0.80 / 1.01 | 0.66 (0.65/0.68) | KILL | research/backtests/2026-09-03_qqq-trend-only.py |
| 2026-09-03 | qqq-trend-only B (A + 12-1 mom>0, weekly) | 12.5% | 0.83 | -28.3% | 0.64 / 0.99 | 0.66 (0.65/0.68) | KILL | research/backtests/2026-09-03_qqq-trend-only.py |
| 2026-09-03 | qqq-trend-only C (50/50 QQQ+SPY core, weekly) | 12.3% | 0.88 | -26.5% | 0.75 / 1.00 | 0.66 (0.65/0.68) | KILL | research/backtests/2026-09-03_qqq-trend-only.py |
| 2026-09-03 | qqq-trend-only D (QQQ/SHY, 200d, monthly) | 14.7% | 0.88 | -28.6% | 0.85 / 0.91 | 0.66 (0.65/0.68) | KILL | research/backtests/2026-09-03_qqq-trend-only.py |
| 2026* | +10.1% | +10.1% | +9.0% | -0.2% | -3.6% | +12.8% | +15.7% |
| 2026* | 1.0 | 1.0 | 1.0 | 1.0 |
| 2026-09-03 | A equal-weight all eligible 75% gross | 10.4% | 1.05 | -15.9% | 1.07 / 1.03 | 0.66 (0.65/0.68) | KILL 4a / PARK 4b | 2026-09-03_composite-vs-equal-weight.py |
| 2026-09-03 | B equal-weight all eligible 100% gross | 13.9% | 1.05 | -20.9% | 1.07 / 1.03 | 0.66 (0.65/0.68) | KILL 4a / PARK 4b | 2026-09-03_composite-vs-equal-weight.py |
| 2026-09-03 | C v1 top-5 by score 75% (= baseline) | 6.4% | 0.66 | -13.8% | 0.65 / 0.68 | 0.66 (0.65/0.68) | KILL (is the baseline) | 2026-09-03_composite-vs-equal-weight.py |
| 2026-09-03 | D BOTTOM-5 by score 75% | 7.4% | 0.59 | -23.9% | 0.51 / 0.65 | 0.66 (0.65/0.68) | KILL | 2026-09-03_composite-vs-equal-weight.py |
| 2026-09-03 | E top-5 by 12-1 momentum only 75% | 19.9% | 1.06 | -24.1% | 1.05 / 1.08 | 0.66 (0.65/0.68) | KILL 4a / PARK 4b | 2026-09-03_composite-vs-equal-weight.py |
| 2026-09-03 | C2 top-5 by composite, no vol-scaling (diagnostic) | 16.5% | 0.95 | -21.6% | 0.90 / 1.00 | 0.66 (0.65/0.68) | KILL | 2026-09-03_composite-vs-equal-weight.py |
| 2026-09-04 | no-vol-scaling ON  n=3 gross=75% | 6.4% | 0.63 | -13.6% | 0.66 / 0.61 | 0.67 (0.64/0.69) | KILL | 2026-09-04_no-vol-scaling.py |
| 2026-09-04 | no-vol-scaling ON  n=3 gross=100% | 8.3% | 0.63 | -17.9% | 0.66 / 0.61 | 0.67 (0.64/0.69) | KILL | 2026-09-04_no-vol-scaling.py |
| 2026-09-04 | no-vol-scaling ON  n=5 gross=75% (= baseline) | 6.5% | 0.67 | -13.8% | 0.64 / 0.69 | 0.67 (0.64/0.69) | KILL (is the baseline) | 2026-09-04_no-vol-scaling.py |
| 2026-09-04 | no-vol-scaling ON  n=5 gross=100% | 8.5% | 0.67 | -18.2% | 0.64 / 0.69 | 0.67 (0.64/0.69) | KILL | 2026-09-04_no-vol-scaling.py |
| 2026-09-04 | no-vol-scaling ON  n=8 gross=75% | 8.0% | 0.82 | -16.4% | 0.87 / 0.77 | 0.67 (0.64/0.69) | KILL | 2026-09-04_no-vol-scaling.py |
| 2026-09-04 | no-vol-scaling ON  n=8 gross=100% | 10.6% | 0.81 | -21.5% | 0.88 / 0.76 | 0.67 (0.64/0.69) | KILL | 2026-09-04_no-vol-scaling.py |
| 2026-09-04 | no-vol-scaling OFF n=3 gross=75% | 21.9% | 1.04 | -25.8% | 1.01 / 1.06 | 0.67 (0.64/0.69) | KILL (DD) | 2026-09-04_no-vol-scaling.py |
| 2026-09-04 | no-vol-scaling OFF n=3 gross=100% (walk-forward pick) | 29.0% | 1.04 | -33.1% | 1.02 / 1.07 | 0.67 (0.64/0.69) | KILL (DD) | 2026-09-04_no-vol-scaling.py |
| 2026-09-04 | no-vol-scaling OFF n=5 gross=75% | 16.5% | 0.95 | -21.6% | 0.90 / 1.00 | 0.67 (0.64/0.69) | KILL (DD) | 2026-09-04_no-vol-scaling.py |
| 2026-09-04 | no-vol-scaling OFF n=5 gross=100% | 21.9% | 0.95 | -28.0% | 0.90 / 1.01 | 0.67 (0.64/0.69) | KILL (DD) | 2026-09-04_no-vol-scaling.py |
| 2026-09-04 | no-vol-scaling OFF n=8 gross=75% (nearest miss) | 13.8% | 0.93 | -17.9% | 0.92 / 0.95 | 0.67 (0.64/0.69) | KILL 4a / PARK 4b (fails H1 only, 0.92 vs SPY 0.96) | 2026-09-04_no-vol-scaling.py |
| 2026-09-04 | no-vol-scaling OFF n=8 gross=100% | 18.3% | 0.93 | -23.4% | 0.92 / 0.95 | 0.67 (0.64/0.69) | KILL (DD) | 2026-09-04_no-vol-scaling.py |
| 2026-09-04 | SPY reference on corrected trading-day index | 15.3% | 0.89 | -33.7% | 0.96 / 0.84 | 0.67 (0.64/0.69) | — | 2026-09-04_no-vol-scaling.py |

**2026-09-04 (lane A) — read before comparing rows across dates.** `data/prices.csv` is on a
CALENDAR-day index from 2014-09-17 (BTC-USD's first date), so any backtest run in the
no-internet sandbox off the cache understates CAGR/Sharpe in the second half of the sample.
The 2026-09-04 rows above are on a corrected trading-day index and are comparable with the
2026-09-03 rows (which were run locally on live yfinance data). See
`2026-09-04_no-vol-scaling.result.md` for the size of the distortion and its effect on live
signals. Fix pending Sunday review.

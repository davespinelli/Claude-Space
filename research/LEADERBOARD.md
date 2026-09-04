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

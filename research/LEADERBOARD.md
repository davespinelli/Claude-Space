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

**2026-09-04 (lane B, idea 40 vol-scaler-replacement).** Base book = lane A's no-scaler
book (top-n by the v1 composite without `/sqrt(vol20)`, eligible only, 75% gross, weekly).
Treatment = a BOOK-LEVEL risk control in place of the per-name scaler. All 21 grid points
reported. Corrected trading-day index (verified in-script).

| 2026-09-04 | 40 NONE    n=3 | 21.9% | 1.04 | -25.8% | 1.01 / 1.06 | 0.67 (0.64/0.69) | KILL 4b (MaxDD -25.8% vs cap -20.2%) — lane A's OFF book, control | 2026-09-04_vol-scaler-replacement_B.py |
| 2026-09-04 | 40 DD      n=3 D=6% | 11.8% | 0.89 | -16.6% | 0.74 / 1.02 | 0.67 (0.64/0.69) | KILL 4a/4b | 2026-09-04_vol-scaler-replacement_B.py |
| 2026-09-04 | 40 DD      n=3 D=8% | 12.0% | 0.86 | -15.8% | 0.77 / 0.94 | 0.67 (0.64/0.69) | KILL 4a/4b | 2026-09-04_vol-scaler-replacement_B.py |
| 2026-09-04 | 40 DD      n=3 D=12% | 13.5% | 0.89 | -18.5% | 0.88 / 0.90 | 0.67 (0.64/0.69) | KILL 4a/4b | 2026-09-04_vol-scaler-replacement_B.py |
| 2026-09-04 | 40 BREADTH n=3 B=30% | 21.0% | 1.03 | -20.6% | 0.96 / 1.09 | 0.67 (0.64/0.69) | KILL 4a / PARK 4b — NEAREST MISS: fails MaxDD by 0.4pp (-20.6% vs cap -20.2%); passes H1/H2/OOS/CAGR; walk-forward pick | 2026-09-04_vol-scaler-replacement_B.py |
| 2026-09-04 | 40 BREADTH n=3 B=40% | 19.9% | 1.00 | -20.9% | 0.95 / 1.05 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1, MaxDD) | 2026-09-04_vol-scaler-replacement_B.py |
| 2026-09-04 | 40 BREADTH n=3 B=50% | 19.4% | 0.99 | -21.4% | 0.95 / 1.04 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1, MaxDD) | 2026-09-04_vol-scaler-replacement_B.py |
| 2026-09-04 | 40 NONE    n=5 | 16.5% | 0.95 | -21.6% | 0.90 / 1.00 | 0.67 (0.64/0.69) | KILL 4b (MaxDD, H1) — control | 2026-09-04_vol-scaler-replacement_B.py |
| 2026-09-04 | 40 DD      n=5 D=6% | 9.0% | 0.81 | -14.3% | 0.73 / 0.87 | 0.67 (0.64/0.69) | KILL 4a/4b | 2026-09-04_vol-scaler-replacement_B.py |
| 2026-09-04 | 40 DD      n=5 D=8% | 8.0% | 0.70 | -15.5% | 0.68 / 0.72 | 0.67 (0.64/0.69) | KILL 4a/4b | 2026-09-04_vol-scaler-replacement_B.py |
| 2026-09-04 | 40 DD      n=5 D=12% | 8.7% | 0.70 | -15.7% | 0.67 / 0.74 | 0.67 (0.64/0.69) | KILL 4a/4b | 2026-09-04_vol-scaler-replacement_B.py |
| 2026-09-04 | 40 BREADTH n=5 B=30% | 16.0% | 0.95 | -17.8% | 0.86 / 1.03 | 0.67 (0.64/0.69) | KILL 4a / PARK 4b — fails H1 only (0.865 vs 0.957) | 2026-09-04_vol-scaler-replacement_B.py |
| 2026-09-04 | 40 BREADTH n=5 B=40% | 15.5% | 0.94 | -17.2% | 0.89 / 0.99 | 0.67 (0.64/0.69) | KILL 4a / PARK 4b — fails H1 only (0.893 vs 0.957) | 2026-09-04_vol-scaler-replacement_B.py |
| 2026-09-04 | 40 BREADTH n=5 B=50% | 15.0% | 0.93 | -17.9% | 0.90 / 0.97 | 0.67 (0.64/0.69) | KILL 4a / PARK 4b — fails H1 only (0.896 vs 0.957) | 2026-09-04_vol-scaler-replacement_B.py |
| 2026-09-04 | 40 NONE    n=8 | 13.8% | 0.93 | -17.9% | 0.92 / 0.95 | 0.67 (0.64/0.69) | KILL 4b (H1 0.918 vs SPY 0.957) — control, = lane A nearest miss | 2026-09-04_vol-scaler-replacement_B.py |
| 2026-09-04 | 40 DD      n=8 D=6% | 7.1% | 0.72 | -12.1% | 0.69 / 0.75 | 0.67 (0.64/0.69) | KEEP 4a (marginal) / KILL 4b (H1, H2, OOS, CAGR all fail) — do NOT adopt, see memo | 2026-09-04_vol-scaler-replacement_B.py |
| 2026-09-04 | 40 DD      n=8 D=8% | 7.4% | 0.70 | -13.8% | 0.71 / 0.69 | 0.67 (0.64/0.69) | KEEP 4a (marginal) / KILL 4b (H1, H2, OOS, CAGR all fail) — do NOT adopt, see memo | 2026-09-04_vol-scaler-replacement_B.py |
| 2026-09-04 | 40 DD      n=8 D=12% | 8.2% | 0.71 | -15.4% | 0.69 / 0.73 | 0.67 (0.64/0.69) | KILL 4a/4b | 2026-09-04_vol-scaler-replacement_B.py |
| 2026-09-04 | 40 BREADTH n=8 B=30% | 13.4% | 0.93 | -19.1% | 0.88 / 0.98 | 0.67 (0.64/0.69) | KILL 4a / PARK 4b — fails H1 only | 2026-09-04_vol-scaler-replacement_B.py |
| 2026-09-04 | 40 BREADTH n=8 B=40% | 13.0% | 0.93 | -16.8% | 0.92 / 0.94 | 0.67 (0.64/0.69) | KILL 4a / PARK 4b — fails H1 only (0.915 vs 0.957) | 2026-09-04_vol-scaler-replacement_B.py |
| 2026-09-04 | 40 BREADTH n=8 B=50% | 12.4% | 0.90 | -18.1% | 0.90 / 0.91 | 0.67 (0.64/0.69) | KILL 4a / PARK 4b — fails H1 only | 2026-09-04_vol-scaler-replacement_B.py |

**2026-09-04 (lane A, idea 2 position-count).** All 30 grid points. Arms: FIXEDW = v1's own
construction (w=15% each, gross=0.15n, n<=6 to avoid leverage); EQW = equal weight at a CONSTANT
75% gross (w=0.75/n) — the arm in which n is purely a diversification choice. ON/OFF = v1
composite with / without the `/sqrt(vol20)` term. Only n is tuned. Corrected trading-day index.
`ON */n=5` reproduces the RULES v1 baseline exactly (0.75/5 = 0.15), and `OFF */n=5` reproduces
idea 1's row. **5 of 30 pass 4b, 2 of 30 pass 4a.** The `OFF FIXEDW n=3/n=4` passes clear 4b's
drawdown cap only because 45%/60% gross scales the n=3/n=4 drawdown under it (same Sharpe as the
EQW versions) — a leverage lever, not a position-count edge. See
`2026-09-04_position-count.result.md` and the KEEP memo `2026-09-04_position-count.md`.

| 2026-09-04 | 2 ON  FIXEDW n=2  | 2.3% | 0.52 | -7.5% | 0.51 / 0.52 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_position-count.py |
| 2026-09-04 | 2 ON  FIXEDW n=3  | 3.9% | 0.63 | -8.3% | 0.66 / 0.62 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_position-count.py |
| 2026-09-04 | 2 ON  FIXEDW n=4  | 5.2% | 0.65 | -11.7% | 0.64 / 0.66 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_position-count.py |
| 2026-09-04 | 2 ON  FIXEDW n=5  | 6.5% | 0.67 | -13.8% | 0.64 / 0.69 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_position-count.py |
| 2026-09-04 | 2 ON  FIXEDW n=6  | 8.3% | 0.72 | -17.4% | 0.81 / 0.66 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_position-count.py |
| 2026-09-04 | 2 ON  EQW    n=2  | 5.4% | 0.52 | -18.0% | 0.52 / 0.52 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_position-count.py |
| 2026-09-04 | 2 ON  EQW    n=3  | 6.4% | 0.63 | -13.6% | 0.66 / 0.61 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_position-count.py |
| 2026-09-04 | 2 ON  EQW    n=4  | 6.4% | 0.65 | -14.6% | 0.64 / 0.65 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_position-count.py |
| 2026-09-04 | 2 ON  EQW    n=5  | 6.5% | 0.67 | -13.8% | 0.64 / 0.69 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_position-count.py |
| 2026-09-04 | 2 ON  EQW    n=6  | 7.0% | 0.72 | -14.6% | 0.81 / 0.66 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_position-count.py |
| 2026-09-04 | 2 ON  EQW    n=8  | 8.0% | 0.82 | -16.4% | 0.87 / 0.77 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_position-count.py |
| 2026-09-04 | 2 ON  EQW    n=10 | 8.9% | 0.91 | -12.9% | 0.99 / 0.84 | 0.67 (0.64/0.69) | KEEP 4a | 2026-09-04_position-count.py |
| 2026-09-04 | 2 ON  EQW    n=12 | 9.5% | 0.95 | -13.9% | 1.09 / 0.85 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (CAGR) | 2026-09-04_position-count.py |
| 2026-09-04 | 2 ON  EQW    n=15 | 9.0% | 0.91 | -15.9% | 1.05 / 0.79 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H2,OOS,CAGR) | 2026-09-04_position-count.py |
| 2026-09-04 | 2 ON  EQW    n=20 | 9.9% | 1.00 | -17.4% | 1.05 / 0.95 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (CAGR) | 2026-09-04_position-count.py |
| 2026-09-04 | 2 OFF FIXEDW n=2  | 8.1% | 0.85 | -11.1% | 0.89 / 0.82 | 0.67 (0.64/0.69) | KEEP 4a | 2026-09-04_position-count.py |
| 2026-09-04 | 2 OFF FIXEDW n=3  | 13.2% | 1.03 | -16.2% | 1.01 / 1.06 | 0.67 (0.64/0.69) | KEEP 4b | 2026-09-04_position-count.py |
| 2026-09-04 | 2 OFF FIXEDW n=4  | 16.0% | 1.05 | -19.5% | 1.09 / 1.02 | 0.67 (0.64/0.69) | KEEP 4b | 2026-09-04_position-count.py |
| 2026-09-04 | 2 OFF FIXEDW n=5  | 16.5% | 0.95 | -21.6% | 0.90 / 1.00 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,DD) | 2026-09-04_position-count.py |
| 2026-09-04 | 2 OFF FIXEDW n=6  | 18.3% | 0.94 | -23.0% | 0.89 / 0.99 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,DD) | 2026-09-04_position-count.py |
| 2026-09-04 | 2 OFF EQW    n=2  | 19.5% | 0.86 | -26.5% | 0.89 / 0.83 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,DD) | 2026-09-04_position-count.py |
| 2026-09-04 | 2 OFF EQW    n=3  | 21.9% | 1.04 | -25.8% | 1.01 / 1.06 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (DD) | 2026-09-04_position-count.py |
| 2026-09-04 | 2 OFF EQW    n=4  | 20.0% | 1.05 | -23.8% | 1.09 / 1.03 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (DD) | 2026-09-04_position-count.py |
| 2026-09-04 | 2 OFF EQW    n=5  | 16.5% | 0.95 | -21.6% | 0.90 / 1.00 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,DD) | 2026-09-04_position-count.py |
| 2026-09-04 | 2 OFF EQW    n=6  | 15.3% | 0.94 | -19.4% | 0.89 / 0.99 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1) | 2026-09-04_position-count.py |
| 2026-09-04 | 2 OFF EQW    n=8  | 13.8% | 0.93 | -17.9% | 0.92 / 0.95 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1) | 2026-09-04_position-count.py |
| 2026-09-04 | 2 OFF EQW    n=10 | 12.9% | 0.93 | -17.5% | 0.92 / 0.95 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1) | 2026-09-04_position-count.py |
| 2026-09-04 | 2 OFF EQW    n=12 | 12.7% | 0.96 | -17.8% | 0.98 / 0.95 | 0.67 (0.64/0.69) | KEEP 4b | 2026-09-04_position-count.py |
| 2026-09-04 | 2 OFF EQW    n=15 | 13.2% | 1.04 | -19.2% | 1.07 / 1.03 | 0.67 (0.64/0.69) | KEEP 4b | 2026-09-04_position-count.py |
| 2026-09-04 | 2 OFF EQW    n=20 | 12.7% | 1.09 | -18.3% | 1.09 / 1.10 | 0.67 (0.64/0.69) | KEEP 4b | 2026-09-04_position-count.py |
| 2026-09-04 | 31 PEAD tercile h=40 (broad, 2012-26) | 16.8% | 0.96 | -34.7% | 1.11 / 0.87 | 0.67 (0.86/0.50) | KILL 4a / KILL 4b | research/backtests/2026-09-04_small-cap-pead.py |
| 2026-09-04 | 31 PEAD tercile h=60 (broad, 2012-26) | 18.9% | 1.07 | -33.5% | 1.29 / 0.93 | 0.67 (0.86/0.50) | KILL 4a / KILL 4b | research/backtests/2026-09-04_small-cap-pead.py |
| 2026-09-04 | 31 PEAD quintile h=40 (broad, 2012-26) | 16.8% | 0.92 | -36.0% | 1.13 / 0.78 | 0.67 (0.86/0.50) | KILL 4a / KILL 4b | research/backtests/2026-09-04_small-cap-pead.py |
| 2026-09-04 | 31 PEAD quintile h=60 (broad, 2012-26) | 19.4% | 1.05 | -35.0% | 1.35 / 0.84 | 0.67 (0.86/0.50) | KILL 4a / KILL 4b | research/backtests/2026-09-04_small-cap-pead.py |
| 2026-09-04 | 31 PEAD CONTROL bottom-tercile h=60 (sort reversed — beats the signal) | 20.7% | 1.16 | -32.1% | 1.30 / 1.09 | 0.67 (0.86/0.50) | diagnostic | research/backtests/2026-09-04_small-cap-pead.py |

### Idea 46 — eligible-fraction-vs-n (lane B, 2026-09-04)

Should the book pin the position COUNT (`top n`) or the FRACTION of eligible names (`top f x E_t`)?
Arms: **N** = top n at 0.75/n (idea 2's KEEP construction, de-grosses to cash when E_t < n);
**NF** = same count cap renormalised to 75% gross (a decomposition arm, isolates the cash sleeve);
**F** = top ceil(f x E_t) at 0.75/ceil(f x E_t). Scorer fixed at the candidate's own (no
`/sqrt(vol20)`); one tuned parameter per arm; all 24 points below. Sanity: `N n=20` reproduces idea
2's KEEP row and `N n=5` reproduces idea 1's `OFF EQW n=5` row exactly.
**KILL for the fraction rule as an improvement** — at matched average book size it beats the
gross-matched count arm on Sharpe at 3 of 8 pairs (mean dSharpe -0.002), and its walk-forward pick
loses OOS to fixed-n's (12.4%/1.132 vs 14.4%/1.170). **But f=0.85 is a 4b KEEP-candidate in its own
right**: it is the only setting in the study that passes 4b on BOTH universe.json (11.3%/1.072/
-16.7%) and universe_broad.json (11.2%/1.024/-18.6%), where idea 2's n=20 fails H2 by 0.02. Also
found: idea 2's "leave the remainder in cash when fewer than n are eligible" clause is worth +0.02
Sharpe at n=20 / +0.05 at n=30 and should be kept deliberately. 14 of 24 pass 4b, 0 of 24 pass 4a.
See `2026-09-04_eligible-fraction-vs-n_B.result.md` and memo `..._B.memo.md`.

| 2026-09-04 | 46 N  n=5 | 16.5% | 0.95 | -21.6% | 0.90 / 1.00 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,DD) | 2026-09-04_eligible-fraction-vs-n_B.py |
| 2026-09-04 | 46 N  n=8 | 13.8% | 0.93 | -17.9% | 0.92 / 0.95 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1) | 2026-09-04_eligible-fraction-vs-n_B.py |
| 2026-09-04 | 46 N  n=10 | 12.9% | 0.93 | -17.5% | 0.92 / 0.95 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1) | 2026-09-04_eligible-fraction-vs-n_B.py |
| 2026-09-04 | 46 N  n=12 | 12.7% | 0.96 | -17.8% | 0.98 / 0.95 | 0.67 (0.64/0.69) | KEEP 4b | 2026-09-04_eligible-fraction-vs-n_B.py |
| 2026-09-04 | 46 N  n=15 | 13.2% | 1.04 | -19.2% | 1.07 / 1.03 | 0.67 (0.64/0.69) | KEEP 4b | 2026-09-04_eligible-fraction-vs-n_B.py |
| 2026-09-04 | 46 N  n=20 | 12.7% | 1.09 | -18.3% | 1.09 / 1.10 | 0.67 (0.64/0.69) | KEEP 4b | 2026-09-04_eligible-fraction-vs-n_B.py |
| 2026-09-04 | 46 N  n=25 | 11.8% | 1.09 | -17.7% | 1.05 / 1.14 | 0.67 (0.64/0.69) | KEEP 4b | 2026-09-04_eligible-fraction-vs-n_B.py |
| 2026-09-04 | 46 N  n=30 | 11.0% | 1.10 | -16.6% | 1.03 / 1.17 | 0.67 (0.64/0.69) | KEEP 4b | 2026-09-04_eligible-fraction-vs-n_B.py |
| 2026-09-04 | 46 NF n=5 | 16.6% | 0.95 | -21.2% | 0.90 / 1.00 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,DD) | 2026-09-04_eligible-fraction-vs-n_B.py |
| 2026-09-04 | 46 NF n=8 | 14.0% | 0.94 | -17.9% | 0.92 / 0.97 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1) | 2026-09-04_eligible-fraction-vs-n_B.py |
| 2026-09-04 | 46 NF n=10 | 13.0% | 0.94 | -17.5% | 0.91 / 0.96 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1) | 2026-09-04_eligible-fraction-vs-n_B.py |
| 2026-09-04 | 46 NF n=12 | 12.8% | 0.96 | -17.8% | 0.97 / 0.96 | 0.67 (0.64/0.69) | KEEP 4b | 2026-09-04_eligible-fraction-vs-n_B.py |
| 2026-09-04 | 46 NF n=15 | 13.3% | 1.04 | -19.2% | 1.06 / 1.03 | 0.67 (0.64/0.69) | KEEP 4b | 2026-09-04_eligible-fraction-vs-n_B.py |
| 2026-09-04 | 46 NF n=20 | 12.8% | 1.07 | -18.3% | 1.08 / 1.07 | 0.67 (0.64/0.69) | KEEP 4b | 2026-09-04_eligible-fraction-vs-n_B.py |
| 2026-09-04 | 46 NF n=25 | 12.1% | 1.07 | -17.6% | 1.04 / 1.09 | 0.67 (0.64/0.69) | KEEP 4b | 2026-09-04_eligible-fraction-vs-n_B.py |
| 2026-09-04 | 46 NF n=30 | 11.5% | 1.05 | -17.5% | 1.02 / 1.09 | 0.67 (0.64/0.69) | KEEP 4b | 2026-09-04_eligible-fraction-vs-n_B.py |
| 2026-09-04 | 46 F  f=0.15 | 16.8% | 0.98 | -27.8% | 1.05 / 0.93 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (DD) | 2026-09-04_eligible-fraction-vs-n_B.py |
| 2026-09-04 | 46 F  f=0.25 | 14.8% | 1.00 | -25.0% | 0.94 / 1.06 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,DD) | 2026-09-04_eligible-fraction-vs-n_B.py |
| 2026-09-04 | 46 F  f=0.35 | 13.6% | 1.01 | -21.5% | 0.96 / 1.05 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (DD) | 2026-09-04_eligible-fraction-vs-n_B.py |
| 2026-09-04 | 46 F  f=0.45 | 13.6% | 1.06 | -19.7% | 1.00 / 1.12 | 0.67 (0.64/0.69) | KEEP 4b | 2026-09-04_eligible-fraction-vs-n_B.py |
| 2026-09-04 | 46 F  f=0.55 | 12.2% | 1.01 | -18.0% | 0.96 / 1.05 | 0.67 (0.64/0.69) | KEEP 4b | 2026-09-04_eligible-fraction-vs-n_B.py |
| 2026-09-04 | 46 F  f=0.70 | 11.6% | 1.04 | -17.1% | 1.00 / 1.07 | 0.67 (0.64/0.69) | KEEP 4b | 2026-09-04_eligible-fraction-vs-n_B.py |
| 2026-09-04 | 46 F  f=0.85 | 11.3% | 1.07 | -16.7% | 1.09 / 1.06 | 0.67 (0.64/0.69) | KEEP 4b | 2026-09-04_eligible-fraction-vs-n_B.py |
| 2026-09-04 | 46 F  f=1.00 | 10.4% | 1.05 | -15.9% | 1.07 / 1.04 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (CAGR) | 2026-09-04_eligible-fraction-vs-n_B.py |
| 2026-09-04 | 36 spinoff INVESTABLE daily-EW | 32.1% | 1.11 | -45.3% | 0.70 / 1.41 | IWM 0.51 (0.50/0.52) | PARK (5-name result; sign test p 0.12; DD 1.8x IWM) | 2026-09-04_spinoff-calendar.py |
| 2026-09-04 | 36 spinoff INVESTABLE drift | 33.7% | 1.08 | -49.1% | 0.70 / 1.41 | IWM 0.51 (0.50/0.52) | PARK | 2026-09-04_spinoff-calendar.py |
| 2026-09-04 | 36 spinoff INVESTABLE ex top-5 | 20.7% | 0.82 | -49.4% | n/a | IWM 0.51 (0.50/0.52) | PARK (robustness arm) | 2026-09-04_spinoff-calendar.py |
| 2026-09-04 | 36 spinoff ALL daily-EW | 24.6% | 0.74 | -46.3% | 0.77 / 1.30 | IWM 0.51 (0.50/0.52) | KILL (raw 10-12B list; mean log return negative) | 2026-09-04_spinoff-calendar.py |
| 2026-09-04 | 36 spinoff ALL drift | 47.4% | 1.05 | -46.3% | 0.77 / 1.30 | IWM 0.51 (0.50/0.52) | KILL (one OTC shell, LDSN +5850%) | 2026-09-04_spinoff-calendar.py |
| 2026-09-04 | insider-cluster-buying hold=6m (broad universe, 2012+) | 21.2% | 0.97 | -39.8% | 0.96 / 1.01 | 0.66 (0.86/0.49) | KILL | research/backtests/2026-09-04_insider-cluster-buying.py |
| 2026-09-04 | insider-cluster-buying hold=12m (broad universe, 2012+) | 26.6% | 1.27 | -39.7% | 1.31 / 1.28 | 0.66 (0.86/0.49) | PARK (4b: Sharpe yes, MaxDD no) | research/backtests/2026-09-04_insider-cluster-buying.py |
| 2026-09-04 | RULES v1 baseline, 2012+ broad-universe sample - reference | 6.8% | 0.66 | -21.2% | 0.86 / 0.49 | 0.66 (0.86/0.49) | - | research/backtests/2026-09-04_insider-cluster-buying.py |
| 2026-09-04 | SPY buy & hold, 2012+ sample - reference | 15.2% | 0.94 | -33.7% | 1.13 / 0.85 | 0.66 (0.86/0.49) | - | research/backtests/2026-09-04_insider-cluster-buying.py |
| 2026-09-04 | 50 insider-cluster-smallcap ALL hold=6m EW100% | 18.8% | 0.83 | -49.4% | 1.08 / 0.69 | 0.57 (0.60/0.54) | KILL 4a (DD) / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_insider-cluster-smallcap.py |
| 2026-09-04 | 50 insider-cluster-smallcap ALL hold=6m cap5% | 18.0% | 0.80 | -49.4% | 1.03 / 0.69 | 0.57 (0.60/0.54) | KILL 4a (DD) / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_insider-cluster-smallcap.py |
| 2026-09-04 | 50 insider-cluster-smallcap ALL hold=12m EW100% | 16.0% | 0.75 | -49.1% | 0.96 / 0.63 | 0.57 (0.60/0.54) | KILL 4a (DD) / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_insider-cluster-smallcap.py |
| 2026-09-04 | 50 insider-cluster-smallcap ALL hold=12m cap5% | 15.2% | 0.72 | -49.1% | 0.91 / 0.63 | 0.57 (0.60/0.54) | KILL 4a (DD) / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_insider-cluster-smallcap.py |
| 2026-09-04 | 50 insider-cluster-smallcap OPP hold=6m EW100% (best arm) | 19.2% | 0.84 | -48.7% | 1.09 / 0.70 | 0.57 (0.60/0.54) | KILL 4a (DD) / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_insider-cluster-smallcap.py |
| 2026-09-04 | 50 insider-cluster-smallcap OPP hold=6m cap5% | 18.3% | 0.82 | -48.7% | 1.04 / 0.70 | 0.57 (0.60/0.54) | KILL 4a (DD) / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_insider-cluster-smallcap.py |
| 2026-09-04 | 50 insider-cluster-smallcap OPP hold=12m EW100% | 16.1% | 0.75 | -49.1% | 0.96 / 0.63 | 0.57 (0.60/0.54) | KILL 4a (DD) / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_insider-cluster-smallcap.py |
| 2026-09-04 | 50 insider-cluster-smallcap OPP hold=12m cap5% | 15.3% | 0.72 | -49.1% | 0.91 / 0.63 | 0.57 (0.60/0.54) | KILL 4a (DD) / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_insider-cluster-smallcap.py |
| 2026-09-04 | 50 RULES v1 on the small panel, 2012+ - reference | 7.6% | 0.57 | -32.8% | 0.60 / 0.54 | 0.57 (0.60/0.54) | - | research/backtests/2026-09-04_insider-cluster-smallcap.py |
| 2026-09-04 | 50 SPY buy & hold, 2012+ - reference | 15.2% | 0.94 | -33.7% | 1.12 / 0.85 | 0.57 (0.60/0.54) | - | research/backtests/2026-09-04_insider-cluster-smallcap.py |
| 2026-09-04 | 50 EW all 439 small caps, 2012+ - CONTROL (no insider signal) | 14.3% | 0.74 | -46.0% | 0.99 / 0.63 | 0.57 (0.60/0.54) | - | research/backtests/2026-09-04_insider-cluster-smallcap.py |
| 2026-09-04 | 49 N  n=5 (small panel) | 4.8% | 0.31 | -40.2% | 0.44 / 0.21 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_third-universe-portability_B.py |
| 2026-09-04 | 49 N  n=8 (small panel) | 5.2% | 0.35 | -37.5% | 0.45 / 0.27 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_third-universe-portability_B.py |
| 2026-09-04 | 49 N  n=10 (small panel) | 7.8% | 0.48 | -29.1% | 0.55 / 0.42 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_third-universe-portability_B.py |
| 2026-09-04 | 49 N  n=12 (small panel) | 9.4% | 0.57 | -27.3% | 0.63 / 0.53 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_third-universe-portability_B.py |
| 2026-09-04 | 49 N  n=15 (small panel) | 7.5% | 0.50 | -27.7% | 0.63 / 0.39 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_third-universe-portability_B.py |
| 2026-09-04 | 49 N  n=20 (small panel) | 6.7% | 0.47 | -27.4% | 0.61 / 0.35 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_third-universe-portability_B.py |
| 2026-09-04 | 49 N  n=25 (small panel) | 5.8% | 0.43 | -27.6% | 0.53 / 0.36 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_third-universe-portability_B.py |
| 2026-09-04 | 49 N  n=30 (small panel) | 5.4% | 0.41 | -24.7% | 0.49 / 0.36 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_third-universe-portability_B.py |
| 2026-09-04 | 49 N  n=40 (small panel) [diag] | 5.2% | 0.42 | -24.1% | 0.44 / 0.40 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_third-universe-portability_B.py |
| 2026-09-04 | 49 N  n=60 (small panel) [diag] | 4.5% | 0.39 | -25.7% | 0.43 / 0.36 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_third-universe-portability_B.py |
| 2026-09-04 | 49 N  n=90 (small panel) [diag] | 3.9% | 0.37 | -26.3% | 0.43 / 0.33 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_third-universe-portability_B.py |
| 2026-09-04 | 49 N  n=120 (small panel) [diag] | 3.5% | 0.35 | -26.9% | 0.42 / 0.31 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_third-universe-portability_B.py |
| 2026-09-04 | 49 NF n=5 (small panel) | 4.9% | 0.32 | -40.2% | 0.44 / 0.21 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_third-universe-portability_B.py |
| 2026-09-04 | 49 NF n=8 (small panel) | 5.3% | 0.35 | -37.5% | 0.45 / 0.28 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_third-universe-portability_B.py |
| 2026-09-04 | 49 NF n=10 (small panel) | 7.8% | 0.48 | -31.4% | 0.55 / 0.42 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_third-universe-portability_B.py |
| 2026-09-04 | 49 NF n=12 (small panel) | 9.3% | 0.57 | -31.1% | 0.63 / 0.52 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_third-universe-portability_B.py |
| 2026-09-04 | 49 NF n=15 (small panel) | 7.4% | 0.49 | -31.0% | 0.63 / 0.37 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_third-universe-portability_B.py |
| 2026-09-04 | 49 NF n=20 (small panel) | 6.5% | 0.46 | -32.4% | 0.61 / 0.33 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_third-universe-portability_B.py |
| 2026-09-04 | 49 NF n=25 (small panel) | 5.7% | 0.42 | -34.9% | 0.53 / 0.33 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_third-universe-portability_B.py |
| 2026-09-04 | 49 NF n=30 (small panel) | 5.2% | 0.40 | -32.8% | 0.49 / 0.33 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_third-universe-portability_B.py |
| 2026-09-04 | 49 F  f=0.15 (small panel) | 5.2% | 0.37 | -40.4% | 0.51 / 0.27 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_third-universe-portability_B.py |
| 2026-09-04 | 49 F  f=0.25 (small panel) | 6.0% | 0.44 | -40.8% | 0.44 / 0.44 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_third-universe-portability_B.py |
| 2026-09-04 | 49 F  f=0.35 (small panel) | 6.2% | 0.47 | -40.8% | 0.52 / 0.43 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_third-universe-portability_B.py |
| 2026-09-04 | 49 F  f=0.45 (small panel) | 5.7% | 0.45 | -40.7% | 0.51 / 0.41 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_third-universe-portability_B.py |
| 2026-09-04 | 49 F  f=0.55 (small panel) | 5.2% | 0.42 | -40.2% | 0.49 / 0.37 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_third-universe-portability_B.py |
| 2026-09-04 | 49 F  f=0.70 (small panel) | 4.6% | 0.39 | -38.6% | 0.48 / 0.33 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_third-universe-portability_B.py |
| 2026-09-04 | 49 F  f=0.85 (small panel) | 4.3% | 0.37 | -40.9% | 0.47 / 0.30 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_third-universe-portability_B.py |
| 2026-09-04 | 49 F  f=1.00 (small panel) | 3.5% | 0.33 | -40.2% | 0.43 / 0.25 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_third-universe-portability_B.py |
| 2026-09-04 | 49 SPY buy & hold, 2011+ sample - reference | 14.2% | 0.86 | -33.7% | 0.89 / 0.86 | 0.65 (0.66/0.65) | - | research/backtests/2026-09-04_third-universe-portability_B.py |
| 2026-09-04 | 49 RULES v1 live (universe.json), 2011+ - baseline | 6.3% | 0.65 | -13.8% | 0.66 / 0.65 | 0.65 (0.66/0.65) | - | research/backtests/2026-09-04_third-universe-portability_B.py |
| 2026-09-04 | 49 RULES v1 on the small panel, 2011+ - reference | 8.1% | 0.60 | -32.8% | 0.70 / 0.52 | 0.65 (0.66/0.65) | - | research/backtests/2026-09-04_third-universe-portability_B.py |
| 2026-09-04 | 49 EW all 439 small caps @75% gross - CONTROL (no filter, no ranking) | 10.2% | 0.68 | -36.2% | 0.80 / 0.61 | 0.65 (0.66/0.65) | - | research/backtests/2026-09-04_third-universe-portability_B.py |

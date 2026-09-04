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
| 2026-09-04 | 39 F f=0.45 g=0.75 | 5.7% | 0.45 | -40.7% | 0.51 / 0.41 | 0.60 (0.70/0.52) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_smallcap-eligible-equal-weight_C.py |
| 2026-09-04 | 39 F f=0.45 g=1.00 | 7.2% | 0.45 | -51.4% | 0.51 / 0.40 | 0.60 (0.70/0.52) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_smallcap-eligible-equal-weight_C.py |
| 2026-09-04 | 39 F f=0.85 g=0.75 | 4.3% | 0.37 | -40.9% | 0.47 / 0.30 | 0.60 (0.70/0.52) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_smallcap-eligible-equal-weight_C.py |
| 2026-09-04 | 39 F f=0.85 g=1.00 | 5.3% | 0.37 | -51.2% | 0.47 / 0.30 | 0.60 (0.70/0.52) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_smallcap-eligible-equal-weight_C.py |
| 2026-09-04 | 39 F f=1.0 g=0.75 | 3.5% | 0.33 | -40.2% | 0.43 / 0.25 | 0.60 (0.70/0.52) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_smallcap-eligible-equal-weight_C.py |
| 2026-09-04 | 39 F f=1.0 g=1.00 | 4.4% | 0.33 | -50.4% | 0.44 / 0.25 | 0.60 (0.70/0.52) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_smallcap-eligible-equal-weight_C.py |
| 2026-09-04 | 39 N n=20 g=0.75 | 6.7% | 0.47 | -27.4% | 0.61 / 0.35 | 0.60 (0.70/0.52) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_smallcap-eligible-equal-weight_C.py |
| 2026-09-04 | 39 N n=20 g=1.00 | 8.3% | 0.47 | -36.4% | 0.61 / 0.35 | 0.60 (0.70/0.52) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_smallcap-eligible-equal-weight_C.py |
| 2026-09-04 | 39 N n=40 g=0.75 | 5.2% | 0.42 | -24.1% | 0.44 / 0.40 | 0.60 (0.70/0.52) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_smallcap-eligible-equal-weight_C.py |
| 2026-09-04 | 39 N n=40 g=1.00 | 6.4% | 0.42 | -31.9% | 0.44 / 0.40 | 0.60 (0.70/0.52) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_smallcap-eligible-equal-weight_C.py |
| 2026-09-04 | 39 SPY buy & hold - reference | 14.2% | 0.86 | -33.7% | 0.89 / 0.86 | 0.60 (0.70/0.52) | - | 2026-09-04_smallcap-eligible-equal-weight_C.py |
| 2026-09-04 | 39 RULES v1 on the small panel - reference | 8.1% | 0.60 | -32.8% | 0.70 / 0.52 | 0.60 (0.70/0.52) | - | 2026-09-04_smallcap-eligible-equal-weight_C.py |
| 2026-09-04 | 39 EW all 439 names @75% - CONTROL (no eligibility filter) | 8.1% | 0.64 | -30.7% | 0.82 / 0.61 | 0.60 (0.70/0.52) | - | 2026-09-04_smallcap-eligible-equal-weight_C.py |
| 2026-09-04 | 38 mom12-1 filt=200d n=10 | 16.0% | 0.70 | -35.6% | 0.72 / 0.70 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD) | research/backtests/2026-09-04_small-cap-momentum-clean_cloud.py |
| 2026-09-04 | 38 mom12-1 filt=200d n=20 | 13.4% | 0.69 | -33.0% | 0.75 / 0.68 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD) | research/backtests/2026-09-04_small-cap-momentum-clean_cloud.py |
| 2026-09-04 | 38 mom12-1 filt=200d n=40 | 11.4% | 0.69 | -30.3% | 0.75 / 0.67 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD) | research/backtests/2026-09-04_small-cap-momentum-clean_cloud.py |
| 2026-09-04 | 38 mom12-1 filt=200d n=60 | 7.6% | 0.53 | -30.2% | 0.55 / 0.54 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_small-cap-momentum-clean_cloud.py |
| 2026-09-04 | 38 mom12-1 filt=none n=10 | 14.9% | 0.65 | -38.9% | 0.64 / 0.67 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD) | research/backtests/2026-09-04_small-cap-momentum-clean_cloud.py |
| 2026-09-04 | 38 mom12-1 filt=none n=20 | 13.5% | 0.68 | -34.9% | 0.73 / 0.66 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD) | research/backtests/2026-09-04_small-cap-momentum-clean_cloud.py |
| 2026-09-04 | 38 mom12-1 filt=none n=40 | 14.6% | 0.80 | -33.9% | 0.80 / 0.82 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD) | research/backtests/2026-09-04_small-cap-momentum-clean_cloud.py |
| 2026-09-04 | 38 mom12-1 filt=none n=60 | 10.7% | 0.65 | -36.5% | 0.67 / 0.65 | 0.65 (0.66/0.65) | KILL 4a / KILL 4b (H1,H2,OOS,DD) | research/backtests/2026-09-04_small-cap-momentum-clean_cloud.py |
| 2026-09-04 | 38 CONTROL EW all 439 @75% (no filter, no ranking) | 10.2% | 0.68 | -36.2% | 0.80 / 0.61 | 0.65 (0.66/0.65) | - | research/backtests/2026-09-04_small-cap-momentum-clean_cloud.py |
| 2026-09-04 | 38 RULES v1 on the small panel - reference | 8.1% | 0.60 | -32.8% | 0.70 / 0.52 | 0.65 (0.66/0.65) | - | research/backtests/2026-09-04_small-cap-momentum-clean_cloud.py |
| 2026-09-04 | 38 SPY buy & hold - reference | 14.2% | 0.86 | -33.7% | 0.89 / 0.86 | 0.65 (0.66/0.65) | - | research/backtests/2026-09-04_small-cap-momentum-clean_cloud.py |
| 2026-09-04 | 38 RULES v1 live (universe.json) - baseline | 6.3% | 0.65 | -13.8% | 0.66 / 0.65 | 0.65 (0.66/0.65) | - | research/backtests/2026-09-04_small-cap-momentum-clean_cloud.py |
| 2026-09-04 | 38 walk-forward plain-Sharpe pick none/n=40 - OOS 2017+ | 16.3% | 0.82 | -33.9% | - / - | 0.65 (0.66/0.65) | KILL 4b (OOS Sharpe 0.818 vs SPY 0.884) | research/backtests/2026-09-04_small-cap-momentum-clean_cloud.py |
| 2026-09-04 | 38 walk-forward 4b-aware pick - OOS 2017+ | - | - | - | - / - | 0.65 (0.66/0.65) | picks NOTHING (no IS point met the -11.2% DD cap) | research/backtests/2026-09-04_small-cap-momentum-clean_cloud.py |
| 2026-09-04 | 38 n=40 gate=vol20 only [diag] | 7.4% | 0.52 | -32.8% | - / - | 0.65 (0.66/0.65) | - | research/backtests/2026-09-04_small-cap-momentum-clean_cloud.py |
| 2026-09-04 | 38 n=40 gate=both [diag] | 5.6% | 0.44 | -27.2% | - / - | 0.65 (0.66/0.65) | - | research/backtests/2026-09-04_small-cap-momentum-clean_cloud.py |
| 2026-09-04 | 38 D1 (best 12-1 decile, EW, 0 bps) [diag] | 21.5% | 0.87 | -42.2% | - / - | 0.65 (0.66/0.65) | - | research/backtests/2026-09-04_small-cap-momentum-clean_cloud.py |
| 2026-09-04 | 38 D10 (worst 12-1 decile, EW, 0 bps) [diag] | 29.2% | 0.94 | -60.3% | - / - | 0.65 (0.66/0.65) | - | research/backtests/2026-09-04_small-cap-momentum-clean_cloud.py |
| 2026-09-04 | 55 universe.json K=200d n=5 | 16.5% | 0.95 | -21.6% | 0.90 / 1.00 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,DD) | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe.json K=200d n=10 | 12.9% | 0.93 | -17.5% | 0.92 / 0.95 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1) | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe.json K=200d n=20 | 12.7% | 1.09 | -18.3% | 1.09 / 1.10 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe.json K=200d n=30 | 11.0% | 1.10 | -16.6% | 1.03 / 1.17 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe.json K=100d n=5 | 15.7% | 0.93 | -22.6% | 0.88 / 0.97 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,DD) | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe.json K=100d n=10 | 12.4% | 0.93 | -18.0% | 1.00 / 0.87 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe.json K=100d n=20 | 11.4% | 1.05 | -15.1% | 1.03 / 1.07 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe.json K=100d n=30 | 9.5% | 1.01 | -12.9% | 0.96 / 1.07 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (H1,CAGR) | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe.json K=50d n=5 | 11.0% | 0.73 | -25.5% | 0.76 / 0.71 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,DD) | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe.json K=50d n=10 | 8.2% | 0.69 | -18.9% | 0.76 / 0.63 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,CAGR) | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe.json K=50d n=20 | 8.3% | 0.82 | -16.1% | 0.81 / 0.84 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,CAGR) | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe.json K=50d n=30 | 7.1% | 0.82 | -14.4% | 0.77 / 0.87 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,CAGR) | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe.json K=none n=5 | 17.0% | 0.97 | -21.4% | 0.90 / 1.04 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,DD) | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe.json K=none n=10 | 13.7% | 0.97 | -17.5% | 0.94 / 1.00 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1) | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe.json K=none n=20 | 13.7% | 1.12 | -18.5% | 1.15 / 1.10 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe.json K=none n=30 | 12.5% | 1.10 | -17.1% | 1.07 / 1.13 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe.json EW-all-eligible K=200d [diag] | 10.4% | 1.05 | -15.9% | 1.07 / 1.04 | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe.json EW-all-eligible K=100d [diag] | 9.9% | 1.01 | -20.0% | 1.10 / 0.92 | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe.json EW-all-eligible K=50d [diag] | 7.4% | 0.79 | -22.3% | 0.87 / 0.71 | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe.json EW-all-eligible K=none [diag] | 12.2% | 1.13 | -18.4% | 1.14 / 1.12 | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe_broad.json K=200d n=5 | 16.7% | 0.88 | -23.4% | 1.02 / 0.78 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe_broad.json K=200d n=10 | 14.2% | 0.89 | -21.4% | 1.11 / 0.71 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe_broad.json K=200d n=20 | 13.1% | 0.96 | -20.1% | 1.12 / 0.81 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (H2) | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe_broad.json K=200d n=30 | 12.2% | 0.97 | -20.3% | 1.15 / 0.82 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (H2,DD) | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe_broad.json K=100d n=5 | 17.0% | 0.90 | -23.8% | 1.04 / 0.79 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe_broad.json K=100d n=10 | 14.0% | 0.89 | -19.6% | 1.11 / 0.71 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (H2,OOS) | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe_broad.json K=100d n=20 | 11.9% | 0.90 | -19.9% | 1.02 / 0.79 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (H2,OOS) | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe_broad.json K=100d n=30 | 11.2% | 0.93 | -20.0% | 1.06 / 0.81 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (H2) | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe_broad.json K=50d n=5 | 12.1% | 0.71 | -26.0% | 0.79 / 0.64 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,DD) | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe_broad.json K=50d n=10 | 11.2% | 0.77 | -22.7% | 0.99 / 0.59 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe_broad.json K=50d n=20 | 9.0% | 0.74 | -20.8% | 0.88 / 0.62 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe_broad.json K=50d n=30 | 8.5% | 0.77 | -19.7% | 0.88 / 0.67 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (H1,H2,OOS,CAGR) | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe_broad.json K=none n=5 | 16.9% | 0.89 | -23.8% | 1.03 / 0.78 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe_broad.json K=none n=10 | 14.4% | 0.90 | -21.4% | 1.09 / 0.74 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe_broad.json K=none n=20 | 12.8% | 0.93 | -20.7% | 1.08 / 0.80 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe_broad.json K=none n=30 | 12.1% | 0.94 | -20.8% | 1.08 / 0.81 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (H2,DD) | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe_broad.json EW-all-eligible K=200d [diag] | 10.7% | 1.03 | -17.7% | 1.15 / 0.92 | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe_broad.json EW-all-eligible K=100d [diag] | 10.2% | 0.99 | -18.2% | 1.12 / 0.86 | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe_broad.json EW-all-eligible K=50d [diag] | 8.4% | 0.85 | -22.9% | 0.98 / 0.72 | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe_broad.json EW-all-eligible K=none [diag] | 12.9% | 1.12 | -20.8% | 1.23 / 1.01 | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 SPY buy & hold (universe.json sample) - reference | 15.3% | 0.89 | -33.7% | 0.96 / 0.84 | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 RULES v1 live (universe.json) - baseline | 6.5% | 0.67 | -13.8% | 0.64 / 0.69 | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe.json walk-forward plain-Sharpe: K=none n=20 OOS | 14.9% | 1.16 | -18.5% | - / - | 0.67 (0.64/0.69) | beats SPY OOS | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe.json walk-forward 4b-aware: K=none n=20 OOS | 14.9% | 1.16 | -18.5% | - / - | 0.67 (0.64/0.69) | beats SPY OOS | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe_broad.json walk-forward plain-Sharpe: K=200d n=30 OOS | 11.6% | 0.90 | -20.3% | - / - | 0.67 (0.64/0.69) | beats SPY OOS | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 55 universe_broad.json walk-forward 4b-aware: K=200d n=30 OOS | 11.6% | 0.90 | -20.3% | - / - | 0.67 (0.64/0.69) | beats SPY OOS | research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py |
| 2026-09-04 | 57 universe.json top20 gate=none @10bps | 13.7% | 1.12 | -18.5% | 1.15 / 1.10 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_trend-gate-as-drawdown-insurance_B.py |
| 2026-09-04 | 57 universe.json top20 gate=200d @10bps | 12.7% | 1.09 | -18.3% | 1.09 / 1.10 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_trend-gate-as-drawdown-insurance_B.py |
| 2026-09-04 | 57 universe.json top20 gate=200d-M @10bps | 13.3% | 1.13 | -17.2% | 1.07 / 1.18 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_trend-gate-as-drawdown-insurance_B.py |
| 2026-09-04 | 57 universe.json top20 gate=band3 @10bps | 13.1% | 1.12 | -18.0% | 1.08 / 1.15 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_trend-gate-as-drawdown-insurance_B.py |
| 2026-09-04 | 57 universe.json top20 gate=band5 @10bps | 13.0% | 1.10 | -18.5% | 1.11 / 1.10 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_trend-gate-as-drawdown-insurance_B.py |
| 2026-09-04 | 57 universe.json ew-all gate=none @10bps | 12.2% | 1.13 | -18.4% | 1.14 / 1.12 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_trend-gate-as-drawdown-insurance_B.py |
| 2026-09-04 | 57 universe.json ew-all gate=200d @10bps | 10.4% | 1.05 | -15.9% | 1.07 / 1.04 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (CAGR) | research/backtests/2026-09-04_trend-gate-as-drawdown-insurance_B.py |
| 2026-09-04 | 57 universe.json ew-all gate=200d-M @10bps | 11.4% | 1.11 | -14.7% | 1.10 / 1.12 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_trend-gate-as-drawdown-insurance_B.py |
| 2026-09-04 | 57 universe.json ew-all gate=band3 @10bps | 11.3% | 1.14 | -15.1% | 1.11 / 1.16 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_trend-gate-as-drawdown-insurance_B.py |
| 2026-09-04 | 57 universe.json ew-all gate=band5 @10bps | 11.5% | 1.11 | -15.8% | 1.09 / 1.12 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_trend-gate-as-drawdown-insurance_B.py |
| 2026-09-04 | 57 universe_broad.json top20 gate=none @10bps | 12.8% | 0.93 | -20.7% | 1.08 / 0.80 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_trend-gate-as-drawdown-insurance_B.py |
| 2026-09-04 | 57 universe_broad.json top20 gate=200d @10bps | 13.1% | 0.96 | -20.1% | 1.12 / 0.81 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (H2) | research/backtests/2026-09-04_trend-gate-as-drawdown-insurance_B.py |
| 2026-09-04 | 57 universe_broad.json top20 gate=200d-M @10bps | 12.7% | 0.93 | -20.5% | 1.10 / 0.78 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_trend-gate-as-drawdown-insurance_B.py |
| 2026-09-04 | 57 universe_broad.json top20 gate=band3 @10bps | 13.0% | 0.95 | -20.1% | 1.10 / 0.82 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (H2) | research/backtests/2026-09-04_trend-gate-as-drawdown-insurance_B.py |
| 2026-09-04 | 57 universe_broad.json top20 gate=band5 @10bps | 12.9% | 0.95 | -20.1% | 1.09 / 0.82 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (H2) | research/backtests/2026-09-04_trend-gate-as-drawdown-insurance_B.py |
| 2026-09-04 | 57 universe_broad.json ew-all gate=none @10bps | 12.9% | 1.12 | -20.8% | 1.23 / 1.01 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (DD) | research/backtests/2026-09-04_trend-gate-as-drawdown-insurance_B.py |
| 2026-09-04 | 57 universe_broad.json ew-all gate=200d @10bps | 10.7% | 1.03 | -17.7% | 1.15 / 0.92 | 0.67 (0.64/0.69) | KEEP 4a / KEEP 4b | research/backtests/2026-09-04_trend-gate-as-drawdown-insurance_B.py |
| 2026-09-04 | 57 universe_broad.json ew-all gate=200d-M @10bps | 11.3% | 1.05 | -17.2% | 1.15 / 0.96 | 0.67 (0.64/0.69) | KEEP 4a / KEEP 4b | research/backtests/2026-09-04_trend-gate-as-drawdown-insurance_B.py |
| 2026-09-04 | 57 universe_broad.json ew-all gate=band3 @10bps | 11.1% | 1.06 | -16.8% | 1.16 / 0.97 | 0.67 (0.64/0.69) | KEEP 4a / KEEP 4b | research/backtests/2026-09-04_trend-gate-as-drawdown-insurance_B.py |
| 2026-09-04 | 57 universe_broad.json ew-all gate=band5 @10bps | 11.1% | 1.04 | -17.5% | 1.13 / 0.96 | 0.67 (0.64/0.69) | KEEP 4a / KEEP 4b | research/backtests/2026-09-04_trend-gate-as-drawdown-insurance_B.py |
| 2026-09-04 | 57 SPY buy & hold (universe.json sample) - reference | 15.3% | 0.89 | -33.7% | 0.96 / 0.84 | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_trend-gate-as-drawdown-insurance_B.py |
| 2026-09-04 | 57 RULES v1 live (universe.json) - baseline | 6.5% | 0.67 | -13.8% | 0.64 / 0.69 | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_trend-gate-as-drawdown-insurance_B.py |
| 2026-09-04 | 57 universe.json walk-forward plain-Sharpe: top20 gate=none OOS | 14.9% | 1.16 | -18.5% | - / - | 0.67 (0.64/0.69) | beats SPY OOS | research/backtests/2026-09-04_trend-gate-as-drawdown-insurance_B.py |
| 2026-09-04 | 57 universe.json walk-forward 4b-aware: top20 gate=none OOS | 14.9% | 1.16 | -18.5% | - / - | 0.67 (0.64/0.69) | beats SPY OOS | research/backtests/2026-09-04_trend-gate-as-drawdown-insurance_B.py |
| 2026-09-04 | 57 universe_broad.json walk-forward plain-Sharpe: ew-all gate=none OOS | 12.5% | 1.10 | -20.8% | - / - | 0.67 (0.64/0.69) | beats SPY OOS | research/backtests/2026-09-04_trend-gate-as-drawdown-insurance_B.py |
| 2026-09-04 | 57 universe_broad.json walk-forward 4b-aware: ew-all gate=band3 OOS | 11.2% | 1.07 | -16.8% | - / - | 0.67 (0.64/0.69) | beats SPY OOS | research/backtests/2026-09-04_trend-gate-as-drawdown-insurance_B.py |
| 2026-09-04 | 4 universe.json top20 gate=none | 13.7% | 1.12 | -18.5% | 1.15 / 1.10 | 0.67 (0.64/0.69) | KEEP 4b / KILL 4a | research/backtests/2026-09-04_abs-momentum-filter_C.py |
| 2026-09-04 | 4 universe.json top20 gate=200d (incumbent) | 12.7% | 1.09 | -18.3% | 1.09 / 1.10 | 0.67 (0.64/0.69) | KEEP 4b / KILL 4a | research/backtests/2026-09-04_abs-momentum-filter_C.py |
| 2026-09-04 | 4 universe.json top20 gate=abs12-1 | 12.4% | 1.06 | -18.4% | 1.05 / 1.08 | 0.67 (0.64/0.69) | KEEP 4b / KILL 4a | research/backtests/2026-09-04_abs-momentum-filter_C.py |
| 2026-09-04 | 4 universe.json top20 gate=200d AND abs | 11.3% | 1.03 | -18.6% | 1.01 / 1.05 | 0.67 (0.64/0.69) | KEEP 4b / KILL 4a | research/backtests/2026-09-04_abs-momentum-filter_C.py |
| 2026-09-04 | 4 universe.json top20 gate=band3 (idea 57 ref) | 13.1% | 1.12 | -18.0% | 1.08 / 1.15 | 0.67 (0.64/0.69) | KEEP 4b / KILL 4a | research/backtests/2026-09-04_abs-momentum-filter_C.py |
| 2026-09-04 | 4 universe.json ew-all gate=none | 12.2% | 1.13 | -18.4% | 1.14 / 1.12 | 0.67 (0.64/0.69) | KEEP 4b / KILL 4a | research/backtests/2026-09-04_abs-momentum-filter_C.py |
| 2026-09-04 | 4 universe.json ew-all gate=200d (incumbent) | 10.4% | 1.05 | -15.9% | 1.07 / 1.04 | 0.67 (0.64/0.69) | KILL 4b (CAGR) | research/backtests/2026-09-04_abs-momentum-filter_C.py |
| 2026-09-04 | 4 universe.json ew-all gate=abs12-1 | 11.4% | 1.07 | -17.1% | 1.12 / 1.04 | 0.67 (0.64/0.69) | KEEP 4b / KILL 4a | research/backtests/2026-09-04_abs-momentum-filter_C.py |
| 2026-09-04 | 4 universe.json ew-all gate=200d AND abs | 10.0% | 1.00 | -15.9% | 1.01 / 0.99 | 0.67 (0.64/0.69) | KILL 4b (CAGR) | research/backtests/2026-09-04_abs-momentum-filter_C.py |
| 2026-09-04 | 4 universe.json ew-all gate=band3 (idea 57 ref) | 11.3% | 1.14 | -15.1% | 1.11 / 1.16 | 0.67 (0.64/0.69) | KEEP 4b / KILL 4a | research/backtests/2026-09-04_abs-momentum-filter_C.py |
| 2026-09-04 | 4 universe_broad top20 gate=none | 12.8% | 0.93 | -20.7% | 1.08 / 0.80 | 0.64 (0.76/0.54) | KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_abs-momentum-filter_C.py |
| 2026-09-04 | 4 universe_broad top20 gate=200d (incumbent) | 13.1% | 0.96 | -20.1% | 1.13 / 0.81 | 0.64 (0.76/0.54) | KILL 4b (H2) | research/backtests/2026-09-04_abs-momentum-filter_C.py |
| 2026-09-04 | 4 universe_broad top20 gate=abs12-1 | 12.8% | 0.94 | -20.7% | 1.11 / 0.81 | 0.64 (0.76/0.54) | KILL 4b (H2,DD) | research/backtests/2026-09-04_abs-momentum-filter_C.py |
| 2026-09-04 | 4 universe_broad top20 gate=200d AND abs | 12.9% | 0.96 | -20.1% | 1.12 / 0.84 | 0.64 (0.76/0.54) | KEEP 4b by +0.0002 (tie) | research/backtests/2026-09-04_abs-momentum-filter_C.py |
| 2026-09-04 | 4 universe_broad top20 gate=band3 (idea 57 ref) | 13.0% | 0.95 | -20.1% | 1.10 / 0.82 | 0.64 (0.76/0.54) | KILL 4b (H2) | research/backtests/2026-09-04_abs-momentum-filter_C.py |
| 2026-09-04 | 4 universe_broad ew-all gate=none | 12.9% | 1.12 | -20.8% | 1.23 / 1.02 | 0.64 (0.76/0.54) | KILL 4b (DD) | research/backtests/2026-09-04_abs-momentum-filter_C.py |
| 2026-09-04 | 4 universe_broad ew-all gate=200d (incumbent) | 10.7% | 1.03 | -17.7% | 1.15 / 0.92 | 0.64 (0.76/0.54) | KEEP 4b by +0.05pp CAGR | research/backtests/2026-09-04_abs-momentum-filter_C.py |
| 2026-09-04 | 4 universe_broad ew-all gate=abs12-1 | 11.8% | 1.07 | -20.1% | 1.16 / 0.99 | 0.64 (0.76/0.54) | KEEP 4b by +0.12pp DD | research/backtests/2026-09-04_abs-momentum-filter_C.py |
| 2026-09-04 | 4 universe_broad ew-all gate=200d AND abs | 10.3% | 0.99 | -17.9% | 1.05 / 0.94 | 0.64 (0.76/0.54) | KILL 4b (CAGR) | research/backtests/2026-09-04_abs-momentum-filter_C.py |
| 2026-09-04 | 4 universe_broad ew-all gate=band3 (idea 57 ref) | 11.1% | 1.06 | -16.8% | 1.16 / 0.97 | 0.64 (0.76/0.54) | KEEP 4b | research/backtests/2026-09-04_abs-momentum-filter_C.py |
| 2026-09-04 | 4 universe.json walk-forward plain-Sharpe AND 4b-aware: top20 gate=none OOS | 14.9% | 1.16 | -18.5% | - / - | 0.67 (0.64/0.69) | no idea-4 arm picked | research/backtests/2026-09-04_abs-momentum-filter_C.py |
| 2026-09-04 | 4 universe_broad walk-forward plain-Sharpe: ew-all gate=none OOS | 12.5% | 1.10 | -20.8% | - / - | 0.64 (0.76/0.54) | no idea-4 arm picked; fails OOS DD | research/backtests/2026-09-04_abs-momentum-filter_C.py |
| 2026-09-04 | 4 universe_broad walk-forward 4b-aware: ew-all gate=band3 OOS | 11.2% | 1.07 | -16.8% | - / - | 0.64 (0.76/0.54) | no idea-4 arm picked | research/backtests/2026-09-04_abs-momentum-filter_C.py |
| 2026-09-04 | 4 OOS reference: RULES v1 baseline (universe.json) | 7.8% | 0.75 | -13.8% | - / - | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_abs-momentum-filter_C.py |
| 2026-09-04 | 4 OOS reference: SPY buy & hold | 15.5% | 0.88 | -33.7% | - / - | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_abs-momentum-filter_C.py |
| 2026-09-04 | 3 universe.json v1 freq=D | 3.6% | 0.40 | -15.7% | 0.42 / 0.38 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,CAGR) | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 universe.json v1 freq=W | 6.5% | 0.67 | -13.8% | 0.64 / 0.69 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,CAGR) | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 universe.json v1 freq=M | 10.2% | 0.96 | -15.4% | 1.08 / 0.87 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (CAGR) | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 universe.json v1 freq=Q | 8.1% | 0.68 | -22.8% | 0.73 / 0.64 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 universe.json top20 freq=D | 10.9% | 0.98 | -16.3% | 0.94 / 1.02 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1) | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 universe.json top20 freq=W | 12.7% | 1.09 | -18.3% | 1.09 / 1.10 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 universe.json top20 freq=M | 14.7% | 1.20 | -19.5% | 1.21 / 1.21 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 universe.json top20 freq=Q | 13.5% | 1.02 | -27.1% | 1.10 / 0.98 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (DD) | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 universe.json ew-all freq=D | 9.4% | 0.97 | -16.9% | 0.97 / 0.97 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (CAGR) | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 universe.json ew-all freq=W | 10.4% | 1.05 | -15.9% | 1.07 / 1.04 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (CAGR) | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 universe.json ew-all freq=M | 11.9% | 1.14 | -17.0% | 1.14 / 1.15 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 universe.json ew-all freq=Q | 11.6% | 1.08 | -22.2% | 1.22 / 0.97 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (DD) | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 universe.json ew-band3 freq=D | 10.8% | 1.10 | -14.7% | 1.07 / 1.14 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 universe.json ew-band3 freq=W | 11.3% | 1.14 | -15.1% | 1.11 / 1.16 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 universe.json ew-band3 freq=M | 11.4% | 1.10 | -18.6% | 1.09 / 1.12 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 universe.json ew-band3 freq=Q | 11.2% | 1.06 | -21.8% | 1.15 / 1.00 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (DD) | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 universe_broad.json v1 freq=D | 2.0% | 0.24 | -25.1% | 0.43 / 0.09 | 0.64 (0.76/0.54) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 universe_broad.json v1 freq=W | 6.4% | 0.64 | -21.2% | 0.76 / 0.54 | 0.64 (0.76/0.54) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 universe_broad.json v1 freq=M | 8.5% | 0.78 | -22.1% | 1.12 / 0.50 | 0.64 (0.76/0.54) | KILL 4a / KILL 4b (H2,OOS,DD,CAGR) | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 universe_broad.json v1 freq=Q | 9.7% | 0.80 | -23.7% | 1.16 / 0.52 | 0.64 (0.76/0.54) | KILL 4a / KILL 4b (H2,OOS,DD,CAGR) | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 universe_broad.json top20 freq=D | 9.9% | 0.76 | -19.7% | 0.95 / 0.60 | 0.64 (0.76/0.54) | KEEP 4a / KILL 4b (H1,H2,OOS,CAGR) | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 universe_broad.json top20 freq=W | 13.1% | 0.96 | -20.1% | 1.12 / 0.81 | 0.64 (0.76/0.54) | KEEP 4a / KILL 4b (H2) | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 universe_broad.json top20 freq=M | 16.4% | 1.10 | -26.1% | 1.33 / 0.92 | 0.64 (0.76/0.54) | KILL 4a / KILL 4b (DD) | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 universe_broad.json top20 freq=Q | 13.8% | 0.92 | -27.1% | 1.27 / 0.65 | 0.64 (0.76/0.54) | KILL 4a / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 universe_broad.json ew-all freq=D | 9.8% | 0.96 | -18.9% | 1.05 / 0.88 | 0.64 (0.76/0.54) | KEEP 4a / KILL 4b (CAGR) | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 universe_broad.json ew-all freq=W | 10.7% | 1.03 | -17.7% | 1.15 / 0.92 | 0.64 (0.76/0.54) | KEEP 4a / KEEP 4b | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 universe_broad.json ew-all freq=M | 11.7% | 1.07 | -21.7% | 1.16 / 0.99 | 0.64 (0.76/0.54) | KILL 4a / KILL 4b (DD) | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 universe_broad.json ew-all freq=Q | 11.5% | 1.04 | -24.4% | 1.23 / 0.88 | 0.64 (0.76/0.54) | KILL 4a / KILL 4b (DD) | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 universe_broad.json ew-band3 freq=D | 11.0% | 1.06 | -17.2% | 1.14 / 0.99 | 0.64 (0.76/0.54) | KEEP 4a / KEEP 4b | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 universe_broad.json ew-band3 freq=W | 11.1% | 1.06 | -16.8% | 1.16 / 0.97 | 0.64 (0.76/0.54) | KEEP 4a / KEEP 4b | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 universe_broad.json ew-band3 freq=M | 11.6% | 1.06 | -22.4% | 1.15 / 0.98 | 0.64 (0.76/0.54) | KILL 4a / KILL 4b (DD) | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 universe_broad.json ew-band3 freq=Q | 11.5% | 1.04 | -24.3% | 1.22 / 0.90 | 0.64 (0.76/0.54) | KILL 4a / KILL 4b (DD) | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 universe.json walk-forward (both rules): ew-all freq=Q OOS | 11.7% | 1.04 | -22.2% | - / - | 0.67 (0.64/0.69) | FAILS OOS 4b (DD,CAGR) | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 universe_broad walk-forward (both rules): top20 freq=M OOS | 15.7% | 1.01 | -26.1% | - / - | 0.64 (0.76/0.54) | FAILS OOS 4b (DD) | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 OOS reference: RULES v1 weekly (universe.json) | 7.8% | 0.75 | -13.8% | - / - | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 3 OOS reference: SPY buy & hold | 15.5% | 0.88 | -33.7% | - / - | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_rebalance-freq_cloud.py |
| 2026-09-04 | 63 universe_broad.json v1 + 0% QQQ core | 6.4% | 0.64 | -21.2% | 0.76 / 0.54 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_broad-H2-binding-bar_cloud.py |
| 2026-09-04 | 63 universe_broad.json v1 + 25% QQQ core | 8.8% | 0.86 | -18.3% | 0.99 / 0.75 | 0.64 (0.76/0.54) | KILL 4b (H2,OOS,CAGR) | research/backtests/2026-09-04_broad-H2-binding-bar_cloud.py |
| 2026-09-04 | 63 universe_broad.json v1 + 50% QQQ core | 11.2% | 0.98 | -17.2% | 1.14 / 0.87 | 0.64 (0.76/0.54) | KEEP 4b | research/backtests/2026-09-04_broad-H2-binding-bar_cloud.py |
| 2026-09-04 | 63 universe_broad.json top20 + 0% QQQ core | 13.1% | 0.96 | -20.1% | 1.12 / 0.81 | 0.64 (0.76/0.54) | KILL 4b (H2) | research/backtests/2026-09-04_broad-H2-binding-bar_cloud.py |
| 2026-09-04 | 63 universe_broad.json top20 + 25% QQQ core | 13.8% | 1.02 | -19.9% | 1.18 / 0.88 | 0.64 (0.76/0.54) | KEEP 4b | research/backtests/2026-09-04_broad-H2-binding-bar_cloud.py |
| 2026-09-04 | 63 universe_broad.json top20 + 50% QQQ core | 14.5% | 1.04 | -22.0% | 1.21 / 0.91 | 0.64 (0.76/0.54) | KILL 4b (DD) | research/backtests/2026-09-04_broad-H2-binding-bar_cloud.py |
| 2026-09-04 | 63 universe_broad.json ew-all + 0% QQQ core | 10.7% | 1.03 | -17.7% | 1.15 / 0.92 | 0.64 (0.76/0.54) | KEEP 4b | research/backtests/2026-09-04_broad-H2-binding-bar_cloud.py |
| 2026-09-04 | 63 universe_broad.json ew-all + 25% QQQ core | 12.0% | 1.06 | -18.8% | 1.19 / 0.95 | 0.64 (0.76/0.54) | KEEP 4b | research/backtests/2026-09-04_broad-H2-binding-bar_cloud.py |
| 2026-09-04 | 63 universe_broad.json ew-all + 50% QQQ core | 13.3% | 1.06 | -21.2% | 1.21 / 0.94 | 0.64 (0.76/0.54) | KILL 4b (DD) | research/backtests/2026-09-04_broad-H2-binding-bar_cloud.py |
| 2026-09-04 | 63 universe_broad.json ew-band3 + 0% QQQ core | 11.1% | 1.06 | -16.8% | 1.16 / 0.97 | 0.64 (0.76/0.54) | KEEP 4b | research/backtests/2026-09-04_broad-H2-binding-bar_cloud.py |
| 2026-09-04 | 63 universe_broad.json ew-band3 + 25% QQQ core | 12.3% | 1.09 | -18.5% | 1.20 / 0.99 | 0.64 (0.76/0.54) | KEEP 4b | research/backtests/2026-09-04_broad-H2-binding-bar_cloud.py |
| 2026-09-04 | 63 universe_broad.json ew-band3 + 50% QQQ core | 13.5% | 1.07 | -21.0% | 1.22 / 0.96 | 0.64 (0.76/0.54) | KILL 4b (DD) | research/backtests/2026-09-04_broad-H2-binding-bar_cloud.py |
| 2026-09-04 | 63 universe.json v1 + 0% QQQ core | 6.5% | 0.67 | -13.8% | 0.64 / 0.69 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,CAGR) | research/backtests/2026-09-04_broad-H2-binding-bar_cloud.py |
| 2026-09-04 | 63 universe.json v1 + 25% QQQ core | 8.8% | 0.87 | -15.3% | 0.91 / 0.85 | 0.67 (0.64/0.69) | KILL 4b (H1,CAGR) | research/backtests/2026-09-04_broad-H2-binding-bar_cloud.py |
| 2026-09-04 | 63 universe.json v1 + 50% QQQ core | 11.2% | 0.98 | -17.0% | 1.08 / 0.91 | 0.67 (0.64/0.69) | KEEP 4b | research/backtests/2026-09-04_broad-H2-binding-bar_cloud.py |
| 2026-09-04 | 63 universe.json top20 + 0% QQQ core | 12.7% | 1.09 | -18.3% | 1.09 / 1.10 | 0.67 (0.64/0.69) | KEEP 4b | research/backtests/2026-09-04_broad-H2-binding-bar_cloud.py |
| 2026-09-04 | 63 universe.json top20 + 25% QQQ core | 13.5% | 1.12 | -18.5% | 1.17 / 1.09 | 0.67 (0.64/0.69) | KEEP 4b | research/backtests/2026-09-04_broad-H2-binding-bar_cloud.py |
| 2026-09-04 | 63 universe.json top20 + 50% QQQ core | 14.3% | 1.10 | -18.8% | 1.21 / 1.03 | 0.67 (0.64/0.69) | KEEP 4b | research/backtests/2026-09-04_broad-H2-binding-bar_cloud.py |
| 2026-09-04 | 63 universe.json ew-all + 0% QQQ core | 10.4% | 1.05 | -15.9% | 1.07 / 1.04 | 0.67 (0.64/0.69) | KILL 4b (CAGR) | research/backtests/2026-09-04_broad-H2-binding-bar_cloud.py |
| 2026-09-04 | 63 universe.json ew-all + 25% QQQ core | 11.8% | 1.08 | -17.3% | 1.15 / 1.03 | 0.67 (0.64/0.69) | KEEP 4b | research/backtests/2026-09-04_broad-H2-binding-bar_cloud.py |
| 2026-09-04 | 63 universe.json ew-all + 50% QQQ core | 13.1% | 1.07 | -20.2% | 1.19 / 0.99 | 0.67 (0.64/0.69) | KEEP 4b | research/backtests/2026-09-04_broad-H2-binding-bar_cloud.py |
| 2026-09-04 | 63 universe.json ew-band3 + 0% QQQ core | 11.3% | 1.14 | -15.1% | 1.11 / 1.16 | 0.67 (0.64/0.69) | KEEP 4b | research/backtests/2026-09-04_broad-H2-binding-bar_cloud.py |
| 2026-09-04 | 63 universe.json ew-band3 + 25% QQQ core | 12.4% | 1.14 | -16.2% | 1.18 / 1.11 | 0.67 (0.64/0.69) | KEEP 4b | research/backtests/2026-09-04_broad-H2-binding-bar_cloud.py |
| 2026-09-04 | 63 universe.json ew-band3 + 50% QQQ core | 13.6% | 1.11 | -19.3% | 1.21 / 1.04 | 0.67 (0.64/0.69) | KEEP 4b | research/backtests/2026-09-04_broad-H2-binding-bar_cloud.py |
| 2026-09-04 | 63 CONTROL universe.json ew-band3 + 25% SPY core (no hindsight) | 11.4% | 1.11 | -16.5% | 1.11 / 1.11 | 0.67 (0.64/0.69) | KEEP 4b (also at 25 bps) | research/backtests/2026-09-04_broad-H2-binding-bar_cloud.py |
| 2026-09-04 | 63 CONTROL universe_broad ew-band3 + 25% SPY core (no hindsight) | 11.3% | 1.04 | -17.7% | 1.13 / 0.96 | 0.64 (0.76/0.54) | KEEP 4b (KILL at 25 bps, CAGR) | research/backtests/2026-09-04_broad-H2-binding-bar_cloud.py |
| 2026-09-04 | 63 CONTROL universe_broad top20 + 25% SPY core (no hindsight) | 12.8% | 0.99 | -20.1% | 1.13 / 0.86 | 0.64 (0.76/0.54) | KEEP 4b — H2 bar fixed by plain beta | research/backtests/2026-09-04_broad-H2-binding-bar_cloud.py |
| 2026-09-04 | 63 universe.json walk-forward (both rules): top20 + 50% QQQ OOS | 15.4% | 1.11 | -18.8% | - / - | 0.67 (0.64/0.69) | clears OOS 4b bars | research/backtests/2026-09-04_broad-H2-binding-bar_cloud.py |
| 2026-09-04 | 63 universe_broad walk-forward (both rules): top20 + 50% QQQ OOS | 14.4% | 0.99 | -22.0% | - / - | 0.64 (0.76/0.54) | FAILS OOS 4b (DD) | research/backtests/2026-09-04_broad-H2-binding-bar_cloud.py |
| 2026-09-04 | 63 OOS reference: SPY buy & hold | 15.5% | 0.88 | -33.7% | - / - | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_broad-H2-binding-bar_cloud.py |
| 2026-09-04 | 67 u.json top20 b=0.25 QQQ core (idea 63 candidate) | 13.5% | 1.12 | -18.5% | 1.17 / 1.09 | 0.67 (0.64/0.69) | KEEP 4b but never walk-forward selected | research/backtests/2026-09-04_core-sleeve-walk-forward-repair_B.py |
| 2026-09-04 | 67 broad top20 b=0.25 QQQ core (idea 63 candidate) | 13.8% | 1.02 | -19.9% | 1.18 / 0.88 | 0.64 (0.76/0.54) | KEEP 4b but never walk-forward selected | research/backtests/2026-09-04_core-sleeve-walk-forward-repair_B.py |
| 2026-09-04 | 67 u.json top20 b=0.50 QQQ core (rule-8 pick) | 14.3% | 1.10 | -18.8% | 1.21 / 1.03 | 0.67 (0.64/0.69) | KEEP 4b | research/backtests/2026-09-04_core-sleeve-walk-forward-repair_B.py |
| 2026-09-04 | 67 broad top20 b=0.50 QQQ core (rule-8 pick, 10/12 points) | 14.5% | 1.04 | -22.0% | 1.21 / 0.91 | 0.64 (0.76/0.54) | KILL 4b (DD) — OOS -22.0% vs -20.2% cap | research/backtests/2026-09-04_core-sleeve-walk-forward-repair_B.py |
| 2026-09-04 | 67 u.json ew-band3 b=0.25 QQQ core | 12.4% | 1.14 | -16.2% | 1.18 / 1.11 | 0.67 (0.64/0.69) | KEEP 4b | research/backtests/2026-09-04_core-sleeve-walk-forward-repair_B.py |
| 2026-09-04 | 67 broad ew-band3 b=0.25 QQQ core | 12.3% | 1.09 | -18.5% | 1.20 / 0.99 | 0.64 (0.76/0.54) | KEEP 4b | research/backtests/2026-09-04_core-sleeve-walk-forward-repair_B.py |
| 2026-09-04 | 67 u.json ew-band3 b=0.25 SPY core (surviving arm) | 11.4% | 1.11 | -16.5% | 1.11 / 1.11 | 0.67 (0.64/0.69) | KEEP 4b (4a fails DD) | research/backtests/2026-09-04_core-sleeve-walk-forward-repair_B.py |
| 2026-09-04 | 67 broad ew-band3 b=0.25 SPY core (surviving arm) | 11.3% | 1.04 | -17.7% | 1.13 / 0.96 | 0.64 (0.76/0.54) | KEEP 4b + KEEP 4a | research/backtests/2026-09-04_core-sleeve-walk-forward-repair_B.py |
| 2026-09-04 | 67 broad walk-forward SPY core (10/12 pts): ew-band3 b=0.00 OOS | 11.2% | 1.07 | -16.8% | - / - | 0.64 (0.76/0.54) | clears OOS 4b | research/backtests/2026-09-04_core-sleeve-walk-forward-repair_B.py |
| 2026-09-04 | 67 broad walk-forward QQQ core (10/12 pts): top20 b=0.50 OOS | 14.4% | 0.99 | -22.0% | - / - | 0.64 (0.76/0.54) | FAILS OOS 4b (DD) — 0/24 points pick b=0.25 | research/backtests/2026-09-04_core-sleeve-walk-forward-repair_B.py |
| 2026-09-04 | 67 OOS reference: SPY buy & hold | 15.5% | 0.88 | -33.7% | - / - | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_core-sleeve-walk-forward-repair_B.py |
| 2026-09-04 | 8 universe.json 12-1 n=5 | 19.9% | 1.06 | -24.1% | 1.04 / 1.09 | 0.67 (0.64/0.69) | KILL 4a (DD) / KILL 4b (DD) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe.json 12-1 n=10 | 15.2% | 1.04 | -20.6% | 1.03 / 1.05 | 0.67 (0.64/0.69) | KILL 4a (DD) / KILL 4b (DD) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe.json 12-1 n=20 | 12.1% | 1.05 | -18.8% | 1.15 / 0.97 | 0.67 (0.64/0.69) | KILL 4a (DD) / KEEP 4b | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe.json 12-1 n=30 | 10.9% | 1.10 | -15.8% | 1.10 / 1.09 | 0.67 (0.64/0.69) | KILL 4a (DD) / KEEP 4b | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe.json 6-1 n=5 | 19.9% | 1.08 | -22.8% | 1.21 / 0.97 | 0.67 (0.64/0.69) | KILL 4a (DD) / KILL 4b (DD) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe.json 6-1 n=10 | 13.9% | 0.96 | -20.6% | 1.08 / 0.88 | 0.67 (0.64/0.69) | KILL 4a (DD) / KILL 4b (DD) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe.json 6-1 n=20 | 11.8% | 1.02 | -19.2% | 1.09 / 0.95 | 0.67 (0.64/0.69) | KILL 4a (DD) / KEEP 4b | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe.json 6-1 n=30 | 10.5% | 1.06 | -16.9% | 1.07 / 1.06 | 0.67 (0.64/0.69) | KILL 4a (DD) / KILL 4b (CAGR) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe.json 3-1 n=5 | 14.5% | 0.85 | -21.0% | 0.80 / 0.90 | 0.67 (0.64/0.69) | KILL 4a (DD) / KILL 4b (H1,DD) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe.json 3-1 n=10 | 12.2% | 0.89 | -18.9% | 0.85 / 0.93 | 0.67 (0.64/0.69) | KILL 4a (DD) / KILL 4b (H1) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe.json 3-1 n=20 | 10.4% | 0.93 | -18.3% | 0.91 / 0.96 | 0.67 (0.64/0.69) | KILL 4a (DD) / KILL 4b (H1,CAGR) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe.json 3-1 n=30 | 9.8% | 1.02 | -16.4% | 0.94 / 1.10 | 0.67 (0.64/0.69) | KILL 4a (DD) / KILL 4b (H1,CAGR) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe.json blend-v1 n=5 | 16.5% | 0.95 | -21.6% | 0.90 / 1.00 | 0.67 (0.64/0.69) | KILL 4a (DD) / KILL 4b (H1,DD) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe.json blend-v1 n=10 | 12.9% | 0.93 | -17.5% | 0.92 / 0.95 | 0.67 (0.64/0.69) | KILL 4a (DD) / KILL 4b (H1) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe.json blend-v1 n=20 | 12.7% | 1.09 | -18.3% | 1.09 / 1.10 | 0.67 (0.64/0.69) | KILL 4a (DD) / KEEP 4b | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe.json blend-v1 n=30 | 11.0% | 1.10 | -16.6% | 1.03 / 1.17 | 0.67 (0.64/0.69) | KILL 4a (DD) / KEEP 4b | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe.json blend-skip n=5 | 16.9% | 0.97 | -22.5% | 1.11 / 0.84 | 0.67 (0.64/0.69) | KILL 4a (DD) / KILL 4b (OOS,DD) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe.json blend-skip n=10 | 12.2% | 0.88 | -20.0% | 0.96 / 0.82 | 0.67 (0.64/0.69) | KILL 4a (DD) / KILL 4b (H1,H2,OOS) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe.json blend-skip n=20 | 11.7% | 1.01 | -19.5% | 1.04 / 0.99 | 0.67 (0.64/0.69) | KILL 4a (DD) / KEEP 4b | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe.json blend-skip n=30 | 10.8% | 1.08 | -16.5% | 1.06 / 1.11 | 0.67 (0.64/0.69) | KILL 4a (DD) / KEEP 4b | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe.json CONTROL EW-all-eligible | 10.4% | 1.05 | -15.9% | 1.07 / 1.04 | 0.67 (0.64/0.69) | KILL 4a (DD) / KILL 4b (CAGR) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe.json CONTROL REVERSED blend-v1 bottom-5 | 2.7% | 0.35 | -21.6% | 0.41 / 0.29 | 0.67 (0.64/0.69) | KILL 4a (H1,H2,DD) / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe.json CONTROL REVERSED blend-v1 bottom-20 | 6.5% | 0.81 | -13.7% | 0.94 / 0.68 | 0.67 (0.64/0.69) | KILL 4a (H2) / KILL 4b (H1,H2,OOS,CAGR) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe.json CONTROL REVERSED 12-1 bottom-5 | 7.2% | 0.67 | -20.9% | 0.49 / 0.86 | 0.67 (0.64/0.69) | KILL 4a (H1,DD) / KILL 4b (H1,OOS,DD,CAGR) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe.json CONTROL REVERSED 12-1 bottom-20 | 7.1% | 0.85 | -14.2% | 0.84 / 0.86 | 0.67 (0.64/0.69) | KILL 4a (DD) / KILL 4b (H1,CAGR) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe.json CONTROL 1m-reversal n=5 | 10.0% | 0.72 | -26.7% | 0.81 / 0.64 | 0.67 (0.64/0.69) | KILL 4a (H2,DD) / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe.json CONTROL 1m-reversal n=20 | 8.0% | 0.82 | -17.3% | 0.89 / 0.76 | 0.67 (0.64/0.69) | KILL 4a (DD) / KILL 4b (H1,H2,OOS,CAGR) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe_broad.json 12-1 n=5 | 20.6% | 1.01 | -26.4% | 1.29 / 0.79 | 0.64 (0.76/0.54) | KILL 4a (DD) / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe_broad.json 12-1 n=10 | 18.8% | 1.08 | -21.4% | 1.28 / 0.93 | 0.64 (0.76/0.54) | KILL 4a (DD) / KILL 4b (DD) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe_broad.json 12-1 n=20 | 13.9% | 0.97 | -21.0% | 1.12 / 0.85 | 0.64 (0.76/0.54) | KEEP 4a / KILL 4b (DD) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe_broad.json 12-1 n=30 | 13.0% | 1.00 | -20.2% | 1.16 / 0.87 | 0.64 (0.76/0.54) | KEEP 4a / KEEP 4b | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe_broad.json 6-1 n=5 | 19.9% | 1.01 | -23.8% | 1.24 / 0.80 | 0.64 (0.76/0.54) | KILL 4a (DD) / KILL 4b (H2,DD) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe_broad.json 6-1 n=10 | 16.9% | 1.02 | -20.2% | 1.25 / 0.83 | 0.64 (0.76/0.54) | KEEP 4a / KILL 4b (H2) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe_broad.json 6-1 n=20 | 14.5% | 1.02 | -20.9% | 1.23 / 0.83 | 0.64 (0.76/0.54) | KEEP 4a / KILL 4b (H2,DD) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe_broad.json 6-1 n=30 | 13.4% | 1.03 | -20.6% | 1.24 / 0.85 | 0.64 (0.76/0.54) | KEEP 4a / KILL 4b (DD) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe_broad.json 3-1 n=5 | 15.9% | 0.87 | -22.6% | 0.91 / 0.83 | 0.64 (0.76/0.54) | KILL 4a (DD) / KILL 4b (H1,H2,OOS,DD) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe_broad.json 3-1 n=10 | 12.2% | 0.80 | -20.9% | 1.04 / 0.58 | 0.64 (0.76/0.54) | KEEP 4a / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe_broad.json 3-1 n=20 | 10.9% | 0.83 | -20.1% | 1.03 / 0.64 | 0.64 (0.76/0.54) | KEEP 4a / KILL 4b (H2,OOS) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe_broad.json 3-1 n=30 | 10.4% | 0.86 | -21.1% | 1.10 / 0.63 | 0.64 (0.76/0.54) | KEEP 4a / KILL 4b (H2,OOS,DD,CAGR) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe_broad.json blend-v1 n=5 | 16.7% | 0.88 | -23.4% | 1.02 / 0.78 | 0.64 (0.76/0.54) | KILL 4a (DD) / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe_broad.json blend-v1 n=10 | 14.2% | 0.89 | -21.4% | 1.11 / 0.71 | 0.64 (0.76/0.54) | KILL 4a (DD) / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe_broad.json blend-v1 n=20 | 13.1% | 0.96 | -20.1% | 1.12 / 0.81 | 0.64 (0.76/0.54) | KEEP 4a / KILL 4b (H2) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe_broad.json blend-v1 n=30 | 12.2% | 0.97 | -20.3% | 1.15 / 0.82 | 0.64 (0.76/0.54) | KEEP 4a / KILL 4b (H2,DD) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe_broad.json blend-skip n=5 | 16.0% | 0.85 | -22.4% | 1.09 / 0.65 | 0.64 (0.76/0.54) | KILL 4a (DD) / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe_broad.json blend-skip n=10 | 13.5% | 0.85 | -23.1% | 1.24 / 0.52 | 0.64 (0.76/0.54) | KILL 4a (H2,DD) / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe_broad.json blend-skip n=20 | 13.1% | 0.94 | -22.1% | 1.22 / 0.70 | 0.64 (0.76/0.54) | KILL 4a (DD) / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe_broad.json blend-skip n=30 | 12.2% | 0.96 | -20.3% | 1.16 / 0.77 | 0.64 (0.76/0.54) | KEEP 4a / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe_broad.json CONTROL EW-all-eligible | 10.7% | 1.03 | -17.7% | 1.15 / 0.92 | 0.64 (0.76/0.54) | KEEP 4a / KEEP 4b | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe_broad.json CONTROL REVERSED blend-v1 bottom-5 | 1.6% | 0.20 | -29.9% | 0.31 / 0.09 | 0.64 (0.76/0.54) | KILL 4a (H1,H2,DD) / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe_broad.json CONTROL REVERSED blend-v1 bottom-20 | 5.7% | 0.65 | -19.0% | 0.90 / 0.44 | 0.64 (0.76/0.54) | KILL 4a (H2) / KILL 4b (H1,H2,OOS,CAGR) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe_broad.json CONTROL REVERSED 12-1 bottom-5 | 8.5% | 0.66 | -26.6% | 0.57 / 0.75 | 0.64 (0.76/0.54) | KILL 4a (H1,DD) / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe_broad.json CONTROL REVERSED 12-1 bottom-20 | 8.0% | 0.81 | -17.0% | 0.86 / 0.76 | 0.64 (0.76/0.54) | KEEP 4a / KILL 4b (H1,H2,OOS,CAGR) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe_broad.json CONTROL 1m-reversal n=5 | 10.7% | 0.70 | -28.1% | 0.83 / 0.59 | 0.64 (0.76/0.54) | KILL 4a (DD) / KILL 4b (H1,H2,OOS,DD) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe_broad.json CONTROL 1m-reversal n=20 | 10.2% | 0.84 | -19.6% | 0.98 / 0.72 | 0.64 (0.76/0.54) | KEEP 4a / KILL 4b (H2,OOS,CAGR) | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 SPY buy & hold (universe.json sample) - reference | 15.3% | 0.89 | -33.7% | 0.96 / 0.84 | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 RULES v1 live (universe.json) - baseline | 6.5% | 0.67 | -13.8% | 0.64 / 0.69 | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe.json walk-forward plain-Sharpe: 6-1 n=5 OOS | 18.5% | 0.97 | -22.8% | - / - | 0.67 (0.64/0.69) | beats SPY OOS; misses OOS 4b | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe.json walk-forward 4b-aware: 6-1 n=20 OOS | 12.3% | 1.02 | -19.2% | - / - | 0.67 (0.64/0.69) | beats SPY OOS; clears OOS 4b | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe_broad.json walk-forward plain-Sharpe: 12-1 n=5 OOS | 17.8% | 0.85 | -26.4% | - / - | 0.64 (0.76/0.54) | loses to SPY OOS; misses OOS 4b | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 8 universe_broad.json walk-forward 4b-aware: 6-1 n=30 OOS | 12.3% | 0.93 | -20.6% | - / - | 0.64 (0.76/0.54) | beats SPY OOS; misses OOS 4b | research/backtests/2026-09-04_lookback-blend_C.py |
| 2026-09-04 | 6 universe.json v1 B=plain L=63 | 6.5% | 0.67 | -13.8% | 0.64 / 0.69 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,CAGR) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe.json v1 B=30% L=63 | 6.6% | 0.66 | -15.2% | 0.61 / 0.72 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,CAGR) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe.json v1 B=30% L=126 | 6.5% | 0.65 | -15.2% | 0.59 / 0.70 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,CAGR) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe.json v1 B=40% L=63 | 6.5% | 0.65 | -13.7% | 0.55 / 0.73 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,CAGR) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe.json v1 B=40% L=126 | 6.5% | 0.65 | -13.7% | 0.55 / 0.73 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,CAGR) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe.json v1 B=50% L=63 | 6.6% | 0.65 | -14.1% | 0.53 / 0.76 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,CAGR) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe.json v1 B=50% L=126 | 6.6% | 0.65 | -13.7% | 0.56 / 0.74 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,CAGR) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe.json v1 B=60% L=63 | 6.7% | 0.66 | -15.4% | 0.55 / 0.75 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,CAGR) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe.json v1 B=60% L=126 | 6.8% | 0.66 | -15.4% | 0.59 / 0.73 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,CAGR) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe.json v1 B=always L=63 | 7.9% | 0.72 | -15.9% | 0.61 / 0.82 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,CAGR) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe.json v1 B=always L=126 | 7.8% | 0.71 | -15.9% | 0.61 / 0.79 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,CAGR) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe.json v1 B=40 L=63 sleeve=best3 [ctrl] | 6.5% | 0.65 | -13.7% | 0.55 / 0.73 | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe.json v1 B=40 L=63 sleeve=ew3 [ctrl] | 6.7% | 0.68 | -13.5% | 0.64 / 0.71 | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe.json v1 B=40 L=63 sleeve=shy [ctrl] | 6.4% | 0.66 | -13.8% | 0.63 / 0.69 | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe.json v1 B=40 L=63 cash-cap-25% [ctrl] | 6.4% | 0.64 | -13.7% | 0.55 / 0.72 | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe.json top20 B=plain L=63 | 12.7% | 1.09 | -18.3% | 1.09 / 1.10 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe.json top20 B=30% L=63 | 12.9% | 1.05 | -19.7% | 0.98 / 1.11 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe.json top20 B=30% L=126 | 12.4% | 1.01 | -19.7% | 0.94 / 1.07 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe.json top20 B=40% L=63 | 12.7% | 1.03 | -18.3% | 0.94 / 1.12 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe.json top20 B=40% L=126 | 12.4% | 1.00 | -18.3% | 0.91 / 1.09 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe.json top20 B=50% L=63 | 12.8% | 1.04 | -18.3% | 0.93 / 1.14 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe.json top20 B=50% L=126 | 12.6% | 1.02 | -18.3% | 0.92 / 1.10 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe.json top20 B=60% L=63 | 13.0% | 1.05 | -19.9% | 0.94 / 1.14 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe.json top20 B=60% L=126 | 12.7% | 1.03 | -19.9% | 0.95 / 1.10 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe.json top20 B=always L=63 | 14.3% | 1.10 | -20.4% | 1.00 / 1.19 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (DD) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe.json top20 B=always L=126 | 13.8% | 1.05 | -20.4% | 0.97 / 1.13 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (DD) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe.json top20 B=40 L=63 sleeve=best3 [ctrl] | 12.7% | 1.03 | -18.3% | 0.94 / 1.12 | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe.json top20 B=40 L=63 sleeve=ew3 [ctrl] | 13.0% | 1.09 | -17.4% | 1.09 / 1.10 | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe.json top20 B=40 L=63 sleeve=shy [ctrl] | 12.6% | 1.08 | -18.2% | 1.08 / 1.09 | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe.json top20 B=40 L=63 cash-cap-25% [ctrl] | 12.6% | 1.07 | -16.8% | 1.02 / 1.13 | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe_broad.json v1 B=plain L=63 | 6.4% | 0.64 | -21.2% | 0.76 / 0.54 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe_broad.json v1 B=30% L=63 | 6.7% | 0.65 | -21.3% | 0.73 / 0.58 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe_broad.json v1 B=30% L=126 | 6.4% | 0.62 | -22.8% | 0.70 / 0.56 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe_broad.json v1 B=40% L=63 | 6.5% | 0.63 | -23.1% | 0.71 / 0.56 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe_broad.json v1 B=40% L=126 | 6.5% | 0.63 | -23.7% | 0.72 / 0.55 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe_broad.json v1 B=50% L=63 | 6.3% | 0.61 | -22.6% | 0.66 / 0.56 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe_broad.json v1 B=50% L=126 | 6.3% | 0.61 | -23.2% | 0.68 / 0.55 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe_broad.json v1 B=60% L=63 | 6.5% | 0.63 | -22.1% | 0.71 / 0.56 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe_broad.json v1 B=60% L=126 | 6.5% | 0.62 | -22.9% | 0.73 / 0.53 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe_broad.json v1 B=always L=63 | 7.9% | 0.72 | -21.6% | 0.75 / 0.69 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe_broad.json v1 B=always L=126 | 7.7% | 0.69 | -22.9% | 0.74 / 0.66 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe_broad.json v1 B=40 L=63 sleeve=best3 [ctrl] | 6.5% | 0.63 | -23.1% | 0.71 / 0.56 | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe_broad.json v1 B=40 L=63 sleeve=ew3 [ctrl] | 6.7% | 0.66 | -22.8% | 0.77 / 0.56 | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe_broad.json v1 B=40 L=63 sleeve=shy [ctrl] | 6.4% | 0.64 | -21.5% | 0.76 / 0.53 | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe_broad.json v1 B=40 L=63 cash-cap-25% [ctrl] | 6.4% | 0.62 | -23.1% | 0.71 / 0.55 | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe_broad.json top20 B=plain L=63 | 13.1% | 0.96 | -20.1% | 1.12 / 0.81 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (H2) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe_broad.json top20 B=30% L=63 | 13.3% | 0.95 | -20.4% | 1.07 / 0.85 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (DD) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe_broad.json top20 B=30% L=126 | 12.9% | 0.92 | -20.4% | 1.03 / 0.83 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (H2,DD) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe_broad.json top20 B=40% L=63 | 13.2% | 0.94 | -20.7% | 1.07 / 0.84 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (DD) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe_broad.json top20 B=40% L=126 | 13.0% | 0.93 | -21.4% | 1.04 / 0.83 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H2,DD) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe_broad.json top20 B=50% L=63 | 12.9% | 0.93 | -20.6% | 1.03 / 0.84 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (DD) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe_broad.json top20 B=50% L=126 | 12.8% | 0.92 | -20.6% | 1.01 / 0.84 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (DD) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe_broad.json top20 B=60% L=63 | 13.2% | 0.94 | -20.6% | 1.07 / 0.84 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (DD) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe_broad.json top20 B=60% L=126 | 13.0% | 0.93 | -20.6% | 1.06 / 0.82 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (H2,DD) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe_broad.json top20 B=always L=63 | 14.7% | 1.01 | -21.1% | 1.10 / 0.94 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (DD) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe_broad.json top20 B=always L=126 | 14.3% | 0.98 | -21.1% | 1.07 / 0.91 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (DD) | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe_broad.json top20 B=40 L=63 sleeve=best3 [ctrl] | 13.2% | 0.94 | -20.7% | 1.07 / 0.84 | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe_broad.json top20 B=40 L=63 sleeve=ew3 [ctrl] | 13.5% | 0.98 | -20.3% | 1.14 / 0.84 | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe_broad.json top20 B=40 L=63 sleeve=shy [ctrl] | 13.1% | 0.96 | -20.0% | 1.12 / 0.81 | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe_broad.json top20 B=40 L=63 cash-cap-25% [ctrl] | 13.1% | 0.96 | -20.7% | 1.11 / 0.83 | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 SPY buy & hold (universe.json sample) - reference | 15.3% | 0.89 | -33.7% | 0.96 / 0.84 | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 RULES v1 live (universe.json) - baseline | 6.5% | 0.67 | -13.8% | 0.64 / 0.69 | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe.json v1 walk-forward plain-Sharpe: plain book OOS | 7.8% | 0.75 | -13.8% | - / - | 0.67 (0.64/0.69) | loses to SPY OOS | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe.json v1 walk-forward 4b-aware: picks NOTHING | - | - | - | - / - | 0.67 (0.64/0.69) | no IS point met the 4b bars | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe.json top20 walk-forward plain-Sharpe: plain book OOS | 14.4% | 1.17 | -18.3% | - / - | 0.67 (0.64/0.69) | beats SPY OOS | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe.json top20 walk-forward 4b-aware: plain book OOS | 14.4% | 1.17 | -18.3% | - / - | 0.67 (0.64/0.69) | beats SPY OOS | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe_broad.json v1 walk-forward plain-Sharpe: plain book OOS | 6.0% | 0.58 | -21.2% | - / - | 0.67 (0.64/0.69) | loses to SPY OOS | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe_broad.json v1 walk-forward 4b-aware: picks NOTHING | - | - | - | - / - | 0.67 (0.64/0.69) | no IS point met the 4b bars | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe_broad.json top20 walk-forward plain-Sharpe: plain book OOS | 12.5% | 0.89 | -20.1% | - / - | 0.67 (0.64/0.69) | beats SPY OOS | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 6 universe_broad.json top20 walk-forward 4b-aware: picks NOTHING | - | - | - | - / - | 0.67 (0.64/0.69) | no IS point met the 4b bars | research/backtests/2026-09-04_defensive-sleeve_cloud.py |
| 2026-09-04 | 68 universe.json 12-1 n=30 1d 5bps | 11.2% | 1.13 | -15.8% | 1.14 / 1.13 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json 12-1 n=30 1d 10bps | 10.9% | 1.10 | -15.8% | 1.10 / 1.09 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json 12-1 n=30 1d 15bps | 10.5% | 1.06 | -15.9% | 1.07 / 1.06 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (CAGR) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json 12-1 n=30 1d 25bps | 9.8% | 1.00 | -15.9% | 1.00 / 0.99 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (CAGR) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json 12-1 n=30 1d 50bps | 7.9% | 0.82 | -16.2% | 0.83 / 0.83 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,CAGR) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json 12-1 n=30 1w 5bps | 11.4% | 1.10 | -17.3% | 1.12 / 1.08 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json 12-1 n=30 1w 10bps | 11.1% | 1.06 | -17.3% | 1.08 / 1.05 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json 12-1 n=30 1w 15bps | 10.7% | 1.03 | -17.4% | 1.05 / 1.02 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json 12-1 n=30 1w 25bps | 9.9% | 0.97 | -17.4% | 0.98 / 0.96 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (CAGR) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json 12-1 n=30 1w 50bps | 8.1% | 0.80 | -17.5% | 0.82 / 0.80 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,CAGR) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json 12-1 n=20 1d 5bps | 12.6% | 1.09 | -18.7% | 1.19 / 1.01 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json 12-1 n=20 1d 10bps | 12.1% | 1.05 | -18.8% | 1.15 / 0.97 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json 12-1 n=20 1d 15bps | 11.6% | 1.01 | -18.8% | 1.10 / 0.93 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json 12-1 n=20 1d 25bps | 10.5% | 0.93 | -18.9% | 1.02 / 0.86 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (CAGR) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json 12-1 n=20 1d 50bps | 8.0% | 0.73 | -19.2% | 0.80 / 0.67 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,CAGR) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json 12-1 n=20 1w 5bps | 12.9% | 1.07 | -19.5% | 1.18 / 0.99 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json 12-1 n=20 1w 10bps | 12.4% | 1.03 | -19.6% | 1.14 / 0.96 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json 12-1 n=20 1w 15bps | 11.8% | 1.00 | -19.6% | 1.10 / 0.92 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json 12-1 n=20 1w 25bps | 10.8% | 0.92 | -19.6% | 1.01 / 0.85 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json 12-1 n=20 1w 50bps | 8.3% | 0.72 | -19.7% | 0.80 / 0.67 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,CAGR) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json blend-v1 n=30 1d 5bps | 11.4% | 1.13 | -16.5% | 1.06 / 1.20 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json blend-v1 n=30 1d 10bps | 11.0% | 1.10 | -16.6% | 1.03 / 1.17 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json blend-v1 n=30 1d 15bps | 10.7% | 1.06 | -16.6% | 0.99 / 1.13 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (CAGR) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json blend-v1 n=30 1d 25bps | 9.9% | 0.99 | -16.7% | 0.92 / 1.07 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,CAGR) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json blend-v1 n=30 1d 50bps | 8.0% | 0.82 | -16.9% | 0.74 / 0.90 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,CAGR) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json blend-v1 n=30 1w 5bps | 11.6% | 1.10 | -18.0% | 1.05 / 1.14 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json blend-v1 n=30 1w 10bps | 11.2% | 1.06 | -18.0% | 1.01 / 1.11 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json blend-v1 n=30 1w 15bps | 10.8% | 1.03 | -18.1% | 0.98 / 1.08 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json blend-v1 n=30 1w 25bps | 10.1% | 0.96 | -18.1% | 0.91 / 1.01 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,CAGR) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json blend-v1 n=30 1w 50bps | 8.2% | 0.80 | -18.2% | 0.73 / 0.86 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,CAGR) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json blend-v1 n=20 1d 5bps | 13.2% | 1.13 | -18.3% | 1.13 / 1.14 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json blend-v1 n=20 1d 10bps | 12.7% | 1.09 | -18.3% | 1.09 / 1.10 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json blend-v1 n=20 1d 15bps | 12.1% | 1.05 | -18.4% | 1.04 / 1.06 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json blend-v1 n=20 1d 25bps | 11.1% | 0.97 | -18.4% | 0.95 / 0.99 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json blend-v1 n=20 1d 50bps | 8.4% | 0.76 | -18.7% | 0.73 / 0.79 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,CAGR) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json blend-v1 n=20 1w 5bps | 13.6% | 1.12 | -18.3% | 1.12 / 1.13 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json blend-v1 n=20 1w 10bps | 13.0% | 1.08 | -18.3% | 1.07 / 1.10 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json blend-v1 n=20 1w 15bps | 12.5% | 1.04 | -18.4% | 1.03 / 1.06 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json blend-v1 n=20 1w 25bps | 11.4% | 0.96 | -18.4% | 0.94 / 0.98 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json blend-v1 n=20 1w 50bps | 8.7% | 0.76 | -18.5% | 0.72 / 0.80 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,CAGR) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json 12-1 n=30 1d 5bps | 13.7% | 1.05 | -20.1% | 1.20 / 0.91 | 0.67 (0.64/0.69) | KEEP 4a / KEEP 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json 12-1 n=30 1d 10bps | 13.0% | 1.00 | -20.2% | 1.16 / 0.87 | 0.67 (0.64/0.69) | KEEP 4a / KEEP 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json 12-1 n=30 1d 15bps | 12.4% | 0.96 | -20.2% | 1.11 / 0.84 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (H2) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json 12-1 n=30 1d 25bps | 11.2% | 0.88 | -20.3% | 1.02 / 0.76 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json 12-1 n=30 1d 50bps | 8.2% | 0.67 | -20.5% | 0.79 / 0.57 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json 12-1 n=30 1w 5bps | 13.8% | 1.04 | -22.6% | 1.30 / 0.82 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H2,DD) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json 12-1 n=30 1w 10bps | 13.2% | 0.99 | -22.7% | 1.25 / 0.79 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json 12-1 n=30 1w 15bps | 12.6% | 0.95 | -22.8% | 1.20 / 0.75 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json 12-1 n=30 1w 25bps | 11.3% | 0.87 | -23.0% | 1.11 / 0.67 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json 12-1 n=30 1w 50bps | 8.2% | 0.66 | -23.6% | 0.87 / 0.49 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json 12-1 n=20 1d 5bps | 14.6% | 1.01 | -21.0% | 1.16 / 0.89 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (DD) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json 12-1 n=20 1d 10bps | 13.9% | 0.97 | -21.0% | 1.12 / 0.85 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (DD) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json 12-1 n=20 1d 15bps | 13.2% | 0.93 | -21.1% | 1.07 / 0.81 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (H2,DD) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json 12-1 n=20 1d 25bps | 11.8% | 0.84 | -21.1% | 0.98 / 0.73 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json 12-1 n=20 1d 50bps | 8.4% | 0.63 | -21.3% | 0.75 / 0.53 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json 12-1 n=20 1w 5bps | 14.9% | 1.01 | -23.0% | 1.26 / 0.82 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H2,DD) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json 12-1 n=20 1w 10bps | 14.2% | 0.97 | -23.1% | 1.21 / 0.78 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json 12-1 n=20 1w 15bps | 13.5% | 0.93 | -23.2% | 1.17 / 0.74 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json 12-1 n=20 1w 25bps | 12.1% | 0.84 | -23.4% | 1.07 / 0.67 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json 12-1 n=20 1w 50bps | 8.6% | 0.63 | -24.0% | 0.83 / 0.47 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json blend-v1 n=30 1d 5bps | 12.9% | 1.02 | -20.3% | 1.19 / 0.86 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (DD) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json blend-v1 n=30 1d 10bps | 12.2% | 0.97 | -20.3% | 1.15 / 0.82 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (H2,DD) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json blend-v1 n=30 1d 15bps | 11.6% | 0.93 | -20.3% | 1.10 / 0.77 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json blend-v1 n=30 1d 25bps | 10.3% | 0.83 | -20.4% | 1.00 / 0.68 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (H2,OOS,DD,CAGR) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json blend-v1 n=30 1d 50bps | 7.1% | 0.60 | -21.4% | 0.76 / 0.46 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json blend-v1 n=30 1w 5bps | 13.1% | 1.00 | -21.7% | 1.25 / 0.79 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H2,DD) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json blend-v1 n=30 1w 10bps | 12.4% | 0.96 | -21.8% | 1.20 / 0.75 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json blend-v1 n=30 1w 15bps | 11.7% | 0.91 | -21.9% | 1.15 / 0.71 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json blend-v1 n=30 1w 25bps | 10.4% | 0.82 | -22.1% | 1.06 / 0.62 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H2,OOS,DD,CAGR) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json blend-v1 n=30 1w 50bps | 7.1% | 0.59 | -22.6% | 0.81 / 0.40 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json blend-v1 n=20 1d 5bps | 13.9% | 1.01 | -20.0% | 1.18 / 0.86 | 0.67 (0.64/0.69) | KEEP 4a / KEEP 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json blend-v1 n=20 1d 10bps | 13.1% | 0.96 | -20.1% | 1.12 / 0.81 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (H2) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json blend-v1 n=20 1d 15bps | 12.3% | 0.91 | -20.1% | 1.07 / 0.76 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (H2,OOS) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json blend-v1 n=20 1d 25bps | 10.8% | 0.81 | -20.2% | 0.97 / 0.67 | 0.67 (0.64/0.69) | KEEP 4a / KILL 4b (H2,OOS) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json blend-v1 n=20 1d 50bps | 7.0% | 0.56 | -21.9% | 0.72 / 0.42 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json blend-v1 n=20 1w 5bps | 14.4% | 1.01 | -22.8% | 1.28 / 0.78 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json blend-v1 n=20 1w 10bps | 13.6% | 0.96 | -22.9% | 1.23 / 0.74 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json blend-v1 n=20 1w 15bps | 12.8% | 0.91 | -23.1% | 1.18 / 0.69 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json blend-v1 n=20 1w 25bps | 11.2% | 0.81 | -23.3% | 1.07 / 0.60 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json blend-v1 n=20 1w 50bps | 7.4% | 0.57 | -23.9% | 0.82 / 0.36 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 SPY buy & hold (universe.json sample) - reference | 15.3% | 0.89 | -33.7% | 0.96 / 0.84 | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 RULES v1 live @10bps (universe.json) - baseline | 6.5% | 0.67 | -13.8% | 0.64 / 0.69 | 0.67 (0.64/0.69) | - | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json WF plain-Sharpe 1d 5bps: 12-1 n=20 OOS | 13.3% | 1.08 | -18.7% | - / - | 0.67 (0.64/0.69) | beats SPY OOS; clears OOS 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json WF 4b-aware 1d 5bps: 12-1 n=20 OOS | 13.3% | 1.08 | -18.7% | - / - | 0.67 (0.64/0.69) | beats SPY OOS; clears OOS 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json WF plain-Sharpe 1d 10bps: 12-1 n=20 OOS | 12.8% | 1.04 | -18.8% | - / - | 0.67 (0.64/0.69) | beats SPY OOS; clears OOS 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json WF 4b-aware 1d 10bps: blend-v1 n=20 OOS | 14.4% | 1.17 | -18.3% | - / - | 0.67 (0.64/0.69) | beats SPY OOS; clears OOS 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json WF plain-Sharpe 1d 15bps: 12-1 n=20 OOS | 12.3% | 1.00 | -18.8% | - / - | 0.67 (0.64/0.69) | beats SPY OOS; clears OOS 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json WF 4b-aware 1d 15bps: picks NOTHING | - | - | - | - / - | 0.67 (0.64/0.69) | no IS point met the 4b bars | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json WF plain-Sharpe 1d 25bps: 12-1 n=20 OOS | 11.2% | 0.93 | -18.9% | - / - | 0.67 (0.64/0.69) | beats SPY OOS; clears OOS 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json WF 4b-aware 1d 25bps: picks NOTHING | - | - | - | - / - | 0.67 (0.64/0.69) | no IS point met the 4b bars | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json WF plain-Sharpe 1d 50bps: 12-1 n=20 OOS | 8.7% | 0.74 | -19.2% | - / - | 0.67 (0.64/0.69) | loses to SPY OOS; misses OOS 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json WF 4b-aware 1d 50bps: picks NOTHING | - | - | - | - / - | 0.67 (0.64/0.69) | no IS point met the 4b bars | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json WF plain-Sharpe 1w 5bps: 12-1 n=20 OOS | 13.5% | 1.05 | -19.5% | - / - | 0.67 (0.64/0.69) | beats SPY OOS; clears OOS 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json WF 4b-aware 1w 5bps: blend-v1 n=20 OOS | 15.5% | 1.20 | -18.3% | - / - | 0.67 (0.64/0.69) | beats SPY OOS; clears OOS 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json WF plain-Sharpe 1w 10bps: 12-1 n=20 OOS | 13.0% | 1.02 | -19.6% | - / - | 0.67 (0.64/0.69) | beats SPY OOS; clears OOS 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json WF 4b-aware 1w 10bps: blend-v1 n=20 OOS | 14.9% | 1.17 | -18.3% | - / - | 0.67 (0.64/0.69) | beats SPY OOS; clears OOS 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json WF plain-Sharpe 1w 15bps: 12-1 n=20 OOS | 12.5% | 0.98 | -19.6% | - / - | 0.67 (0.64/0.69) | beats SPY OOS; clears OOS 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json WF 4b-aware 1w 15bps: picks NOTHING | - | - | - | - / - | 0.67 (0.64/0.69) | no IS point met the 4b bars | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json WF plain-Sharpe 1w 25bps: 12-1 n=20 OOS | 11.4% | 0.91 | -19.6% | - / - | 0.67 (0.64/0.69) | beats SPY OOS; clears OOS 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json WF 4b-aware 1w 25bps: picks NOTHING | - | - | - | - / - | 0.67 (0.64/0.69) | no IS point met the 4b bars | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json WF plain-Sharpe 1w 50bps: 12-1 n=20 OOS | 8.9% | 0.73 | -19.7% | - / - | 0.67 (0.64/0.69) | loses to SPY OOS; misses OOS 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe.json WF 4b-aware 1w 50bps: picks NOTHING | - | - | - | - / - | 0.67 (0.64/0.69) | no IS point met the 4b bars | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json WF plain-Sharpe 1d 5bps: blend-v1 n=30 OOS | 12.2% | 0.95 | -20.3% | - / - | 0.67 (0.64/0.69) | beats SPY OOS; misses OOS 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json WF 4b-aware 1d 5bps: blend-v1 n=30 OOS | 12.2% | 0.95 | -20.3% | - / - | 0.67 (0.64/0.69) | beats SPY OOS; misses OOS 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json WF plain-Sharpe 1d 10bps: blend-v1 n=30 OOS | 11.6% | 0.90 | -20.3% | - / - | 0.67 (0.64/0.69) | beats SPY OOS; misses OOS 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json WF 4b-aware 1d 10bps: blend-v1 n=30 OOS | 11.6% | 0.90 | -20.3% | - / - | 0.67 (0.64/0.69) | beats SPY OOS; misses OOS 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json WF plain-Sharpe 1d 15bps: blend-v1 n=30 OOS | 10.9% | 0.86 | -20.3% | - / - | 0.67 (0.64/0.69) | loses to SPY OOS; misses OOS 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json WF 4b-aware 1d 15bps: blend-v1 n=30 OOS | 10.9% | 0.86 | -20.3% | - / - | 0.67 (0.64/0.69) | loses to SPY OOS; misses OOS 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json WF plain-Sharpe 1d 25bps: blend-v1 n=30 OOS | 9.6% | 0.77 | -20.4% | - / - | 0.67 (0.64/0.69) | loses to SPY OOS; misses OOS 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json WF 4b-aware 1d 25bps: picks NOTHING | - | - | - | - / - | 0.67 (0.64/0.69) | no IS point met the 4b bars | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json WF plain-Sharpe 1d 50bps: 12-1 n=30 OOS | 8.5% | 0.66 | -20.5% | - / - | 0.67 (0.64/0.69) | loses to SPY OOS; misses OOS 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json WF 4b-aware 1d 50bps: picks NOTHING | - | - | - | - / - | 0.67 (0.64/0.69) | no IS point met the 4b bars | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json WF plain-Sharpe 1w 5bps: 12-1 n=30 OOS | 12.8% | 0.92 | -22.6% | - / - | 0.67 (0.64/0.69) | beats SPY OOS; misses OOS 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json WF 4b-aware 1w 5bps: blend-v1 n=30 OOS | 12.0% | 0.90 | -21.7% | - / - | 0.67 (0.64/0.69) | beats SPY OOS; misses OOS 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json WF plain-Sharpe 1w 10bps: 12-1 n=30 OOS | 12.2% | 0.88 | -22.7% | - / - | 0.67 (0.64/0.69) | loses to SPY OOS; misses OOS 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json WF 4b-aware 1w 10bps: picks NOTHING | - | - | - | - / - | 0.67 (0.64/0.69) | no IS point met the 4b bars | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json WF plain-Sharpe 1w 15bps: 12-1 n=30 OOS | 11.6% | 0.85 | -22.8% | - / - | 0.67 (0.64/0.69) | loses to SPY OOS; misses OOS 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json WF 4b-aware 1w 15bps: picks NOTHING | - | - | - | - / - | 0.67 (0.64/0.69) | no IS point met the 4b bars | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json WF plain-Sharpe 1w 25bps: 12-1 n=30 OOS | 10.4% | 0.77 | -23.0% | - / - | 0.67 (0.64/0.69) | loses to SPY OOS; misses OOS 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json WF 4b-aware 1w 25bps: picks NOTHING | - | - | - | - / - | 0.67 (0.64/0.69) | no IS point met the 4b bars | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json WF plain-Sharpe 1w 50bps: 12-1 n=30 OOS | 7.5% | 0.58 | -23.6% | - / - | 0.67 (0.64/0.69) | loses to SPY OOS; misses OOS 4b | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 68 universe_broad.json WF 4b-aware 1w 50bps: picks NOTHING | - | - | - | - / - | 0.67 (0.64/0.69) | no IS point met the 4b bars | research/backtests/2026-09-04_lookback-candidate-cost-and-lag_cloud.py |
| 2026-09-04 | 66 universe.json ew-band3 g=0.75 (turn 4.9x, OOS 1.23) | 11.3% | 1.14 | -15.1% | 1.11 / 1.16 | 0.67 (0.64/0.69) | KEEP 4b (idea 57 arm, reproduced) | research/backtests/2026-09-04_gross-exposure-is-the-error_B.py |
| 2026-09-04 | 66 universe.json ew-band3 g=0.85 (turn 5.5x, OOS 1.23) | 12.8% | 1.14 | -17.1% | 1.11 / 1.16 | 0.67 (0.64/0.69) | KEEP 4b | research/backtests/2026-09-04_gross-exposure-is-the-error_B.py |
| 2026-09-04 | 66 universe.json ew-band3 g=0.90 (turn 5.8x, OOS 1.23) | 13.5% | 1.14 | -18.0% | 1.11 / 1.16 | 0.67 (0.64/0.69) | KEEP 4b — PARK (rule 8 does not select it) | research/backtests/2026-09-04_gross-exposure-is-the-error_B.py |
| 2026-09-04 | 66 universe.json ew-band3 g=1.00 (turn 6.4x, OOS 1.23) | 15.1% | 1.14 | -19.9% | 1.11 / 1.16 | 0.67 (0.64/0.69) | KEEP 4b (Sharpe identical to g=0.75) | research/backtests/2026-09-04_gross-exposure-is-the-error_B.py |
| 2026-09-04 | 66 universe.json ew-band3 g=1.00 + 25% SPY core (turn 4.8x, OOS 1.17) | 15.2% | 1.11 | -21.7% | 1.11 / 1.11 | 0.67 (0.64/0.69) | KILL 4b (DD) — core worse at matched investment | research/backtests/2026-09-04_gross-exposure-is-the-error_B.py |
| 2026-09-04 | 66 universe.json top20-200d g=0.75 (turn 9.6x, OOS 1.17) | 12.7% | 1.09 | -18.3% | 1.09 / 1.10 | 0.67 (0.64/0.69) | KEEP 4b (idea 2 arm, reproduced) | research/backtests/2026-09-04_gross-exposure-is-the-error_B.py |
| 2026-09-04 | 66 universe.json top20-200d g=1.00 (turn 12.8x, OOS 1.17) | 16.9% | 1.09 | -24.0% | 1.09 / 1.10 | 0.67 (0.64/0.69) | KILL 4b (DD) | research/backtests/2026-09-04_gross-exposure-is-the-error_B.py |
| 2026-09-04 | 66 universe.json top20-band3 g=0.75 (turn 9.0x, OOS 1.22) | 13.1% | 1.12 | -18.0% | 1.08 / 1.15 | 0.67 (0.64/0.69) | KEEP 4b | research/backtests/2026-09-04_gross-exposure-is-the-error_B.py |
| 2026-09-04 | 66 universe.json top20-band3 g=1.00 (turn 12.0x, OOS 1.22) | 17.4% | 1.12 | -23.6% | 1.08 / 1.15 | 0.67 (0.64/0.69) | KILL 4b (DD) | research/backtests/2026-09-04_gross-exposure-is-the-error_B.py |
| 2026-09-04 | 66 universe_broad.json ew-band3 g=0.75 (turn 5.2x, OOS 1.07) | 11.1% | 1.06 | -16.8% | 1.16 / 0.97 | 0.64 (0.76/0.54) | KEEP 4a + 4b | research/backtests/2026-09-04_gross-exposure-is-the-error_B.py |
| 2026-09-04 | 66 universe_broad.json ew-band3 g=0.90 (turn 6.2x, OOS 1.07) | 13.4% | 1.06 | -20.0% | 1.16 / 0.97 | 0.64 (0.76/0.54) | KEEP 4a + 4b — PARK (rule 8 does not select it) | research/backtests/2026-09-04_gross-exposure-is-the-error_B.py |
| 2026-09-04 | 66 universe_broad.json ew-band3 g=1.00 (turn 6.8x, OOS 1.07) | 14.8% | 1.06 | -22.1% | 1.16 / 0.97 | 0.64 (0.76/0.54) | KILL 4b (DD) | research/backtests/2026-09-04_gross-exposure-is-the-error_B.py |
| 2026-09-04 | 66 universe_broad.json ew-band3 g=1.00 + 25% SPY core (turn 5.2x, OOS 1.05) | 15.0% | 1.04 | -23.3% | 1.13 / 0.96 | 0.64 (0.76/0.54) | KILL 4b (DD) | research/backtests/2026-09-04_gross-exposure-is-the-error_B.py |
| 2026-09-04 | 66 universe_broad.json top20-200d g=0.75 (turn 13.8x, OOS 0.89) | 13.1% | 0.96 | -20.1% | 1.12 / 0.81 | 0.64 (0.76/0.54) | KILL 4b (H2) — H2 flat 0.814->0.815 across g | research/backtests/2026-09-04_gross-exposure-is-the-error_B.py |
| 2026-09-04 | 66 universe_broad.json top20-200d g=1.00 (turn 18.4x, OOS 0.90) | 17.4% | 0.96 | -26.2% | 1.13 / 0.82 | 0.64 (0.76/0.54) | KILL 4b (H2,DD) — gross does not fix H2 | research/backtests/2026-09-04_gross-exposure-is-the-error_B.py |
| 2026-09-04 | 66 universe_broad.json top20-200d g=1.00 + 25% SPY core (turn 13.9x, OOS 0.94) | 17.0% | 0.99 | -26.3% | 1.13 / 0.86 | 0.64 (0.76/0.54) | KILL 4b (DD) — core DOES move H2 (+0.047, t<1) | research/backtests/2026-09-04_gross-exposure-is-the-error_B.py |
| 2026-09-04 | 66 universe_broad.json top20-band3 g=0.75 (turn 13.7x, OOS 0.90) | 13.0% | 0.95 | -20.1% | 1.10 / 0.82 | 0.64 (0.76/0.54) | KILL 4b (H2) | research/backtests/2026-09-04_gross-exposure-is-the-error_B.py |
| 2026-09-04 | 66 universe_broad.json top20-band3 g=1.00 (turn 18.3x, OOS 0.90) | 17.3% | 0.95 | -26.2% | 1.10 / 0.82 | 0.64 (0.76/0.54) | KILL 4b (H2,DD) | research/backtests/2026-09-04_gross-exposure-is-the-error_B.py |
| 2026-09-04 | 66 WF universe.json R1 max-IS-Sharpe -> ew-band3 g=1.00 core=0.25 OOS | 16.7% | 1.17 | -21.7% | - / - | 0.75 OOS | OOS 4b FAIL (MaxDD) | research/backtests/2026-09-04_gross-exposure-is-the-error_B.py |
| 2026-09-04 | 66 WF universe.json R2 4b-aware -> ew-band3 g=0.95 core=0.25 OOS | 15.8% | 1.17 | -20.6% | - / - | 0.75 OOS | OOS 4b FAIL (MaxDD) | research/backtests/2026-09-04_gross-exposure-is-the-error_B.py |
| 2026-09-04 | 66 WF universe_broad.json R1 max-IS-Sharpe -> ew-band3 g=1.00 core=0.00 OOS | 14.9% | 1.07 | -22.1% | - / - | 0.58 OOS | OOS 4b FAIL (MaxDD) | research/backtests/2026-09-04_gross-exposure-is-the-error_B.py |
| 2026-09-04 | 66 WF universe_broad.json R2 4b-aware -> ew-band3 g=0.95 core=0.00 OOS | 14.2% | 1.07 | -21.1% | - / - | 0.58 OOS | OOS 4b FAIL (MaxDD) | research/backtests/2026-09-04_gross-exposure-is-the-error_B.py |
| 2026-09-04 | 10 U56/v1 (names 56, turn 23.6x, OOS 0.75) | 6.5% | 0.67 | -13.8% | 0.64 / 0.69 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,CAGR) | research/backtests/2026-09-04_sector-only-universe_C.py |
| 2026-09-04 | 10 U56/EWall (names 56, turn 8.2x, OOS 1.11) | 10.4% | 1.05 | -15.9% | 1.07 / 1.04 | 0.67 (0.64/0.69) | KILL 4b (CAGR) | research/backtests/2026-09-04_sector-only-universe_C.py |
| 2026-09-04 | 10 U56/CAND-n5 (names 56, turn 17.6x, OOS 1.00) | 16.5% | 0.95 | -21.6% | 0.90 / 1.00 | 0.67 (0.64/0.69) | KILL 4b (H1,DD) | research/backtests/2026-09-04_sector-only-universe_C.py |
| 2026-09-04 | 10 U56/CAND-n10 (names 56, turn 13.9x, OOS 0.98) | 12.9% | 0.93 | -17.5% | 0.92 / 0.95 | 0.67 (0.64/0.69) | KILL 4b (H1) | research/backtests/2026-09-04_sector-only-universe_C.py |
| 2026-09-04 | 10 U56/CAND-n20 (names 56, turn 9.6x, OOS 1.17) | 12.7% | 1.09 | -18.3% | 1.09 / 1.10 | 0.67 (0.64/0.69) | KEEP-cand 4b | research/backtests/2026-09-04_sector-only-universe_C.py |
| 2026-09-04 | 10 ETF36/v1 (names 36, turn 18.0x, OOS 0.44) | 3.8% | 0.46 | -17.9% | 0.62 / 0.34 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,CAGR) | research/backtests/2026-09-04_sector-only-universe_C.py |
| 2026-09-04 | 10 ETF36/EWall (names 36, turn 8.5x, OOS 0.67) | 5.1% | 0.63 | -21.8% | 0.66 / 0.60 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_sector-only-universe_C.py |
| 2026-09-04 | 10 ETF36/CAND-n5 (names 36, turn 15.0x, OOS 0.59) | 6.3% | 0.54 | -23.4% | 0.54 / 0.54 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_sector-only-universe_C.py |
| 2026-09-04 | 10 ETF36/CAND-n10 (names 36, turn 11.6x, OOS 0.77) | 6.9% | 0.69 | -18.5% | 0.67 / 0.70 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,CAGR) | research/backtests/2026-09-04_sector-only-universe_C.py |
| 2026-09-04 | 10 ETF36/CAND-n20 (names 36, turn 6.7x, OOS 0.94) | 6.8% | 0.82 | -15.2% | 0.75 / 0.88 | 0.67 (0.64/0.69) | KILL 4b (H1,CAGR) | research/backtests/2026-09-04_sector-only-universe_C.py |
| 2026-09-04 | 10 ETF24/v1 (names 24, turn 16.3x, OOS 0.55) | 5.5% | 0.52 | -21.6% | 0.57 / 0.49 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_sector-only-universe_C.py |
| 2026-09-04 | 10 ETF24/EWall (names 24, turn 9.6x, OOS 0.73) | 8.2% | 0.71 | -29.4% | 0.77 / 0.65 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_sector-only-universe_C.py |
| 2026-09-04 | 10 ETF24/CAND-n5 (names 24, turn 13.1x, OOS 0.62) | 6.7% | 0.57 | -23.4% | 0.58 / 0.57 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_sector-only-universe_C.py |
| 2026-09-04 | 10 ETF24/CAND-n10 (names 24, turn 9.3x, OOS 0.73) | 7.1% | 0.68 | -21.5% | 0.70 / 0.66 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_sector-only-universe_C.py |
| 2026-09-04 | 10 ETF24/CAND-n20 (names 24, turn 4.0x, OOS 0.89) | 6.7% | 0.78 | -15.2% | 0.78 / 0.78 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,CAGR) | research/backtests/2026-09-04_sector-only-universe_C.py |
| 2026-09-04 | 10 STK20/v1 (names 20, turn 15.2x, OOS 1.14) | 18.1% | 1.13 | -19.3% | 1.16 / 1.12 | 0.67 (0.64/0.69) | KEEP-cand 4b | research/backtests/2026-09-04_sector-only-universe_C.py |
| 2026-09-04 | 10 STK20/EWall (names 20, turn 9.1x, OOS 1.44) | 19.5% | 1.25 | -30.8% | 1.13 / 1.37 | 0.67 (0.64/0.69) | KILL 4b (DD) | research/backtests/2026-09-04_sector-only-universe_C.py |
| 2026-09-04 | 10 STK20/CAND-n5 (names 20, turn 14.2x, OOS 1.09) | 18.6% | 1.06 | -18.4% | 1.00 / 1.11 | 0.67 (0.64/0.69) | KEEP-cand 4b | research/backtests/2026-09-04_sector-only-universe_C.py |
| 2026-09-04 | 10 STK20/CAND-n10 (names 20, turn 8.5x, OOS 1.37) | 19.0% | 1.31 | -17.3% | 1.30 / 1.32 | 0.67 (0.64/0.69) | KEEP-cand 4b | research/backtests/2026-09-04_sector-only-universe_C.py |
| 2026-09-04 | 10 STK20/CAND-n20 (names 20, turn 3.5x, OOS 1.45) | 12.1% | 1.34 | -12.1% | 1.34 / 1.34 | 0.67 (0.64/0.69) | KEEP-cand 4b + 4a | research/backtests/2026-09-04_sector-only-universe_C.py |
| 2026-09-04 | 10 B136/v1 (names 136, turn 29.4x, OOS 0.58) | 6.4% | 0.64 | -21.2% | 0.76 / 0.54 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_sector-only-universe_C.py |
| 2026-09-04 | 10 B136/EWall (names 136, turn 8.3x, OOS 1.02) | 10.7% | 1.03 | -17.7% | 1.15 / 0.92 | 0.67 (0.64/0.69) | KEEP-cand 4b | research/backtests/2026-09-04_sector-only-universe_C.py |
| 2026-09-04 | 10 B136/CAND-n5 (names 136, turn 21.3x, OOS 0.82) | 16.7% | 0.88 | -23.4% | 1.02 / 0.78 | 0.67 (0.64/0.69) | KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_sector-only-universe_C.py |
| 2026-09-04 | 10 B136/CAND-n10 (names 136, turn 17.5x, OOS 0.78) | 14.2% | 0.89 | -21.4% | 1.11 / 0.71 | 0.67 (0.64/0.69) | KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_sector-only-universe_C.py |
| 2026-09-04 | 10 B136/CAND-n20 (names 136, turn 13.8x, OOS 0.89) | 13.1% | 0.96 | -20.1% | 1.12 / 0.81 | 0.67 (0.64/0.69) | KILL 4b (H2) | research/backtests/2026-09-04_sector-only-universe_C.py |
| 2026-09-04 | 10 BSTK100/v1 (names 100, turn 28.2x, OOS 0.51) | 8.2% | 0.67 | -21.1% | 0.90 / 0.47 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_sector-only-universe_C.py |
| 2026-09-04 | 10 BSTK100/EWall (names 100, turn 8.6x, OOS 1.01) | 12.8% | 1.02 | -26.1% | 1.14 / 0.91 | 0.67 (0.64/0.69) | KILL 4b (DD) | research/backtests/2026-09-04_sector-only-universe_C.py |
| 2026-09-04 | 10 BSTK100/CAND-n5 (names 100, turn 20.6x, OOS 0.80) | 16.4% | 0.87 | -22.1% | 1.01 / 0.76 | 0.67 (0.64/0.69) | KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_sector-only-universe_C.py |
| 2026-09-04 | 10 BSTK100/CAND-n10 (names 100, turn 17.0x, OOS 0.77) | 14.4% | 0.91 | -22.4% | 1.14 / 0.71 | 0.67 (0.64/0.69) | KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_sector-only-universe_C.py |
| 2026-09-04 | 10 BSTK100/CAND-n20 (names 100, turn 12.6x, OOS 0.94) | 13.9% | 1.00 | -20.4% | 1.18 / 0.84 | 0.67 (0.64/0.69) | KILL 4b (DD) | research/backtests/2026-09-04_sector-only-universe_C.py |
| 2026-09-04 | 10 WF S1 max-IS-Sharpe -> STK20/CAND-n10 OOS | 21.2% | 1.37 | -17.3% | - / - | 0.75 OOS | OOS 4b PASS (survivorship, see memo) | research/backtests/2026-09-04_sector-only-universe_C.py |
| 2026-09-04 | 10 WF S2 4b-aware -> STK20/CAND-n20 OOS | 14.0% | 1.45 | -12.1% | - / - | 0.75 OOS | OOS 4b PASS (survivorship, see memo) | research/backtests/2026-09-04_sector-only-universe_C.py |
| 2026-09-04 | 9 u.json/v1/none (turn 23.6x, OOS 0.75) | 6.5% | 0.67 | -13.8% | 0.64 / 0.69 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,CAGR) | research/backtests/2026-09-04_trailing-stop_cloud.py |
| 2026-09-04 | 9 u.json/v1/S10/C21 (turn 23.5x, OOS 0.70) | 6.0% | 0.63 | -13.7% | 0.64 / 0.63 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,CAGR) | research/backtests/2026-09-04_trailing-stop_cloud.py |
| 2026-09-04 | 9 u.json/v1/S15/C0 (turn 23.6x, OOS 0.73) | 6.3% | 0.65 | -14.1% | 0.64 / 0.67 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,CAGR) | research/backtests/2026-09-04_trailing-stop_cloud.py |
| 2026-09-04 | 9 u.json/top20/none (turn 9.6x, OOS 1.17) | 12.7% | 1.09 | -18.3% | 1.09 / 1.10 | 0.67 (0.64/0.69) | KEEP 4b | research/backtests/2026-09-04_trailing-stop_cloud.py |
| 2026-09-04 | 9 u.json/top20/S10/C21 (turn 10.3x, OOS 1.05) | 9.5% | 1.00 | -12.2% | 1.00 / 0.99 | 0.67 (0.64/0.69) | 4a-pass, KILL 4b (CAGR) | research/backtests/2026-09-04_trailing-stop_cloud.py |
| 2026-09-04 | 9 u.json/top20/S15/C0 (turn 10.3x, OOS 1.13) | 12.1% | 1.07 | -16.2% | 1.09 / 1.06 | 0.67 (0.64/0.69) | KEEP 4b | research/backtests/2026-09-04_trailing-stop_cloud.py |
| 2026-09-04 | 9 u.json/top20/S20/C0 (turn 9.8x, OOS 1.16) | 12.4% | 1.09 | -17.0% | 1.09 / 1.09 | 0.67 (0.64/0.69) | KEEP 4b | research/backtests/2026-09-04_trailing-stop_cloud.py |
| 2026-09-04 | 9 u.json/ew-band3/none (turn 4.9x, OOS 1.23) | 11.3% | 1.14 | -15.1% | 1.11 / 1.16 | 0.67 (0.64/0.69) | KEEP 4b | research/backtests/2026-09-04_trailing-stop_cloud.py |
| 2026-09-04 | 9 u.json/ew-band3/S10/C21 (turn 5.6x, OOS 1.13) | 8.2% | 1.04 | -11.5% | 1.04 / 1.04 | 0.67 (0.64/0.69) | 4a-pass, KILL 4b (CAGR) | research/backtests/2026-09-04_trailing-stop_cloud.py |
| 2026-09-04 | 9 u.json/ew-band3/S15/C0 (turn 5.5x, OOS 1.20) | 10.7% | 1.12 | -15.3% | 1.12 / 1.11 | 0.67 (0.64/0.69) | KEEP 4b | research/backtests/2026-09-04_trailing-stop_cloud.py |
| 2026-09-04 | 9 u.json/ew-band3/S15/C21 (turn 5.0x, OOS 1.18) | 10.1% | 1.12 | -12.8% | 1.17 / 1.09 | 0.67 (0.64/0.69) | 4a-pass, KILL 4b (CAGR) | research/backtests/2026-09-04_trailing-stop_cloud.py |
| 2026-09-04 | 9 u.json/ew-band3/S20/C0 (turn 5.0x, OOS 1.21) | 11.0% | 1.13 | -14.8% | 1.12 / 1.14 | 0.67 (0.64/0.69) | KEEP 4b | research/backtests/2026-09-04_trailing-stop_cloud.py |
| 2026-09-04 | 9 broad/v1/none (turn 29.4x, OOS 0.58) | 6.4% | 0.64 | -21.2% | 0.76 / 0.54 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_trailing-stop_cloud.py |
| 2026-09-04 | 9 broad/v1/S10/C21 (turn 29.4x, OOS 0.60) | 6.5% | 0.65 | -20.6% | 0.77 / 0.55 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_trailing-stop_cloud.py |
| 2026-09-04 | 9 broad/v1/S15/C0 (turn 29.4x, OOS 0.56) | 6.3% | 0.63 | -21.7% | 0.76 / 0.52 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_trailing-stop_cloud.py |
| 2026-09-04 | 9 broad/top20/none (turn 13.8x, OOS 0.89) | 13.1% | 0.96 | -20.1% | 1.12 / 0.81 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H2) | research/backtests/2026-09-04_trailing-stop_cloud.py |
| 2026-09-04 | 9 broad/top20/S10/C21 (turn 14.2x, OOS 0.78) | 9.1% | 0.82 | -14.7% | 0.94 / 0.71 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H1,H2,OOS,CAGR) | research/backtests/2026-09-04_trailing-stop_cloud.py |
| 2026-09-04 | 9 broad/top20/S15/C0 (turn 14.4x, OOS 0.85) | 12.2% | 0.92 | -20.1% | 1.10 / 0.76 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H2,OOS) | research/backtests/2026-09-04_trailing-stop_cloud.py |
| 2026-09-04 | 9 broad/top20/S20/C0 (turn 13.9x, OOS 0.88) | 12.8% | 0.95 | -19.0% | 1.12 / 0.80 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H2,OOS) | research/backtests/2026-09-04_trailing-stop_cloud.py |
| 2026-09-04 | 9 broad/ew-band3/none (turn 5.2x, OOS 1.07) | 11.1% | 1.06 | -16.8% | 1.16 / 0.97 | 0.64 (0.76/0.54) | 4a-pass, KEEP 4b | research/backtests/2026-09-04_trailing-stop_cloud.py |
| 2026-09-04 | 9 broad/ew-band3/S10/C21 (turn 5.9x, OOS 1.01) | 8.0% | 0.98 | -13.1% | 1.08 / 0.88 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (CAGR) | research/backtests/2026-09-04_trailing-stop_cloud.py |
| 2026-09-04 | 9 broad/ew-band3/S15/C0 (turn 5.8x, OOS 1.04) | 10.5% | 1.04 | -17.0% | 1.15 / 0.93 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (CAGR) | research/backtests/2026-09-04_trailing-stop_cloud.py |
| 2026-09-04 | 9 broad/ew-band3/S15/C21 (turn 5.3x, OOS 1.07) | 10.1% | 1.06 | -15.0% | 1.17 / 0.95 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (CAGR) | research/backtests/2026-09-04_trailing-stop_cloud.py |
| 2026-09-04 | 9 broad/ew-band3/S20/C0 (turn 5.3x, OOS 1.07) | 10.9% | 1.06 | -16.7% | 1.17 / 0.96 | 0.64 (0.76/0.54) | 4a-pass, KEEP 4b | research/backtests/2026-09-04_trailing-stop_cloud.py |
| 2026-09-04 | 73 U56/EWall (sd 0.281, dS_EW +0.000) | 10.0% | 1.02 | -15.9% | 0.92 / 1.11 | 0.65 (0.66/0.65) | KEEP 4b | research/backtests/2026-09-04_asset-class-dispersion_B.py |
| 2026-09-04 | 73 U56/CAND5 (sd 0.281, dS_EW -0.043) | 17.1% | 0.98 | -21.6% | 0.96 / 1.01 | 0.65 (0.66/0.65) | KILL 4b (DD) | research/backtests/2026-09-04_asset-class-dispersion_B.py |
| 2026-09-04 | 73 U56/CAND10 (sd 0.281, dS_EW -0.067) | 13.2% | 0.96 | -17.5% | 0.95 / 0.97 | 0.65 (0.66/0.65) | KEEP 4b | research/backtests/2026-09-04_asset-class-dispersion_B.py |
| 2026-09-04 | 73 U56/CAND20 (sd 0.281, dS_EW +0.070) | 12.5% | 1.09 | -18.3% | 1.05 / 1.14 | 0.65 (0.66/0.65) | KEEP 4b | research/backtests/2026-09-04_asset-class-dispersion_B.py |
| 2026-09-04 | 73 ETF36/EWall (sd 0.145, dS_EW +0.000) | 4.6% | 0.59 | -21.8% | 0.48 / 0.68 | 0.42 (0.46/0.39) | KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_asset-class-dispersion_B.py |
| 2026-09-04 | 73 ETF36/CAND5 (sd 0.145, dS_EW -0.073) | 5.8% | 0.51 | -23.4% | 0.37 / 0.63 | 0.42 (0.46/0.39) | KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_asset-class-dispersion_B.py |
| 2026-09-04 | 73 ETF36/CAND10 (sd 0.145, dS_EW +0.102) | 6.7% | 0.69 | -18.5% | 0.59 / 0.77 | 0.42 (0.46/0.39) | KILL 4b (H1,H2,OOS,CAGR) | research/backtests/2026-09-04_asset-class-dispersion_B.py |
| 2026-09-04 | 73 ETF36/CAND20 (sd 0.145, dS_EW +0.228) | 6.6% | 0.81 | -15.2% | 0.64 / 0.96 | 0.42 (0.46/0.39) | 4a-pass, KILL 4b (H1,CAGR) | research/backtests/2026-09-04_asset-class-dispersion_B.py |
| 2026-09-04 | 73 ETF24/EWall (sd 0.129, dS_EW +0.000) | 7.5% | 0.69 | -29.4% | 0.66 / 0.71 | 0.50 (0.48/0.52) | KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_asset-class-dispersion_B.py |
| 2026-09-04 | 73 ETF24/CAND5 (sd 0.129, dS_EW -0.109) | 6.6% | 0.58 | -23.4% | 0.49 / 0.65 | 0.50 (0.48/0.52) | KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_asset-class-dispersion_B.py |
| 2026-09-04 | 73 ETF24/CAND10 (sd 0.129, dS_EW -0.001) | 6.9% | 0.68 | -21.5% | 0.62 / 0.75 | 0.50 (0.48/0.52) | 4a-pass, KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_asset-class-dispersion_B.py |
| 2026-09-04 | 73 ETF24/CAND20 (sd 0.129, dS_EW +0.073) | 6.3% | 0.76 | -15.2% | 0.65 / 0.86 | 0.50 (0.48/0.52) | 4a-pass, KILL 4b (H1,H2,CAGR) | research/backtests/2026-09-04_asset-class-dispersion_B.py |
| 2026-09-04 | 73 STK20/EWall (sd 0.378, dS_EW +0.000) | 19.6% | 1.34 | -19.5% | 1.24 / 1.43 | 1.15 (1.17/1.14) | KEEP 4b | research/backtests/2026-09-04_asset-class-dispersion_B.py |
| 2026-09-04 | 73 STK20/CAND5 (sd 0.378, dS_EW -0.270) | 18.7% | 1.07 | -18.4% | 1.00 / 1.13 | 1.15 (1.17/1.14) | KEEP 4b | research/backtests/2026-09-04_asset-class-dispersion_B.py |
| 2026-09-04 | 73 STK20/CAND10 (sd 0.378, dS_EW -0.037) | 19.0% | 1.30 | -17.3% | 1.23 / 1.36 | 1.15 (1.17/1.14) | 4a-pass, KEEP 4b | research/backtests/2026-09-04_asset-class-dispersion_B.py |
| 2026-09-04 | 73 STK20/CAND20 (sd 0.378, dS_EW -0.035) | 11.9% | 1.30 | -12.1% | 1.18 / 1.41 | 1.15 (1.17/1.14) | 4a-pass, KEEP 4b | research/backtests/2026-09-04_asset-class-dispersion_B.py |
| 2026-09-04 | 73 B136/EWall (sd 0.257, dS_EW +0.000) | 10.2% | 1.01 | -17.7% | 1.07 / 0.95 | 0.66 (0.85/0.48) | 4a-pass, KEEP 4b | research/backtests/2026-09-04_asset-class-dispersion_B.py |
| 2026-09-04 | 73 B136/CAND5 (sd 0.257, dS_EW -0.164) | 15.7% | 0.84 | -23.4% | 0.87 / 0.83 | 0.66 (0.85/0.48) | KILL 4b (H1,H2,OOS,DD) | research/backtests/2026-09-04_asset-class-dispersion_B.py |
| 2026-09-04 | 73 B136/CAND10 (sd 0.257, dS_EW -0.138) | 13.6% | 0.87 | -21.4% | 1.04 / 0.74 | 0.66 (0.85/0.48) | KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_asset-class-dispersion_B.py |
| 2026-09-04 | 73 B136/CAND20 (sd 0.257, dS_EW -0.071) | 12.6% | 0.94 | -20.1% | 1.06 / 0.84 | 0.66 (0.85/0.48) | 4a-pass, KILL 4b (H2) | research/backtests/2026-09-04_asset-class-dispersion_B.py |
| 2026-09-04 | 73 BSTK100/EWall (sd 0.278, dS_EW +0.000) | 12.1% | 1.03 | -26.1% | 1.18 / 0.92 | 0.68 (0.96/0.45) | KILL 4b (DD) | research/backtests/2026-09-04_asset-class-dispersion_B.py |
| 2026-09-04 | 73 BSTK100/CAND5 (sd 0.278, dS_EW -0.203) | 15.3% | 0.83 | -22.1% | 0.84 / 0.83 | 0.68 (0.96/0.45) | KILL 4b (H1,H2,OOS,DD) | research/backtests/2026-09-04_asset-class-dispersion_B.py |
| 2026-09-04 | 73 BSTK100/CAND10 (sd 0.278, dS_EW -0.157) | 13.7% | 0.88 | -22.4% | 1.08 / 0.72 | 0.68 (0.96/0.45) | KILL 4b (H2,OOS,DD) | research/backtests/2026-09-04_asset-class-dispersion_B.py |
| 2026-09-04 | 73 BSTK100/CAND20 (sd 0.278, dS_EW -0.057) | 13.2% | 0.98 | -20.4% | 1.13 / 0.85 | 0.68 (0.96/0.45) | 4a-pass, KILL 4b (H2,DD) | research/backtests/2026-09-04_asset-class-dispersion_B.py |
| 2026-09-04 | 73 SMALL484/EWall (sd 0.682, dS_EW +0.000) | 4.8% | 0.41 | -34.3% | 0.43 / 0.40 | 0.52 (0.53/0.60) | KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_asset-class-dispersion_B.py |
| 2026-09-04 | 73 SMALL484/CAND5 (sd 0.682, dS_EW -0.084) | 5.2% | 0.33 | -52.8% | 0.68 / 0.02 | 0.52 (0.53/0.60) | KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_asset-class-dispersion_B.py |
| 2026-09-04 | 73 SMALL484/CAND10 (sd 0.682, dS_EW +0.061) | 7.7% | 0.47 | -35.9% | 0.69 / 0.29 | 0.52 (0.53/0.60) | KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_asset-class-dispersion_B.py |
| 2026-09-04 | 73 SMALL484/CAND20 (sd 0.682, dS_EW +0.082) | 7.2% | 0.49 | -26.3% | 0.67 / 0.35 | 0.52 (0.53/0.60) | KILL 4b (H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_asset-class-dispersion_B.py |
| 2026-09-04 | 13 u56/v1 | 6.5% | 0.67 | -13.8% | 0.64 / 0.69 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_52w-high-proximity_C.py |
| 2026-09-04 | 13 u56/EWall | 10.4% | 1.05 | -15.9% | 1.07 / 1.04 | 0.67 (0.64/0.69) | KILL 4b (CAGR) | 2026-09-04_52w-high-proximity_C.py |
| 2026-09-04 | 13 u56/COMP-n5 | 16.5% | 0.95 | -21.6% | 0.90 / 1.00 | 0.67 (0.64/0.69) | KILL 4b (H1,DD) | 2026-09-04_52w-high-proximity_C.py |
| 2026-09-04 | 13 u56/COMP-n10 | 12.9% | 0.93 | -17.5% | 0.92 / 0.95 | 0.67 (0.64/0.69) | KILL 4b (H1) | 2026-09-04_52w-high-proximity_C.py |
| 2026-09-04 | 13 u56/COMP-n20 | 12.7% | 1.09 | -18.3% | 1.09 / 1.10 | 0.67 (0.64/0.69) | KEEP 4b | 2026-09-04_52w-high-proximity_C.py |
| 2026-09-04 | 13 u56/COMP-n30 | 11.0% | 1.10 | -16.6% | 1.03 / 1.17 | 0.67 (0.64/0.69) | KEEP 4b | 2026-09-04_52w-high-proximity_C.py |
| 2026-09-04 | 13 u56/PROX-n5 | 1.5% | 0.21 | -21.0% | 0.13 / 0.28 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_52w-high-proximity_C.py |
| 2026-09-04 | 13 u56/PROX-n10 | 5.6% | 0.67 | -15.4% | 0.66 / 0.68 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_52w-high-proximity_C.py |
| 2026-09-04 | 13 u56/PROX-n20 | 7.9% | 0.94 | -14.6% | 1.00 / 0.88 | 0.67 (0.64/0.69) | KILL 4b (CAGR) | 2026-09-04_52w-high-proximity_C.py |
| 2026-09-04 | 13 u56/PROX-n30 | 8.9% | 1.05 | -14.5% | 1.03 / 1.07 | 0.67 (0.64/0.69) | KILL 4b (CAGR) | 2026-09-04_52w-high-proximity_C.py |
| 2026-09-04 | 13 u56/BLEND-n5 | 7.3% | 0.61 | -24.0% | 0.43 / 0.77 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_52w-high-proximity_C.py |
| 2026-09-04 | 13 u56/BLEND-n10 | 8.1% | 0.76 | -17.1% | 0.73 / 0.79 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_52w-high-proximity_C.py |
| 2026-09-04 | 13 u56/BLEND-n20 | 9.8% | 1.00 | -16.8% | 0.98 / 1.03 | 0.67 (0.64/0.69) | KILL 4b (CAGR) | 2026-09-04_52w-high-proximity_C.py |
| 2026-09-04 | 13 u56/BLEND-n30 | 10.1% | 1.10 | -15.2% | 1.09 / 1.12 | 0.67 (0.64/0.69) | KILL 4b (CAGR) | 2026-09-04_52w-high-proximity_C.py |
| 2026-09-04 | 13 broad/v1 | 6.4% | 0.64 | -21.2% | 0.76 / 0.54 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_52w-high-proximity_C.py |
| 2026-09-04 | 13 broad/EWall | 10.7% | 1.03 | -17.7% | 1.15 / 0.92 | 0.64 (0.76/0.54) | KEEP 4b | 2026-09-04_52w-high-proximity_C.py |
| 2026-09-04 | 13 broad/COMP-n5 | 16.7% | 0.88 | -23.4% | 1.02 / 0.78 | 0.64 (0.76/0.54) | KILL 4b (H2,OOS,DD) | 2026-09-04_52w-high-proximity_C.py |
| 2026-09-04 | 13 broad/COMP-n10 | 14.2% | 0.89 | -21.4% | 1.11 / 0.71 | 0.64 (0.76/0.54) | KILL 4b (H2,OOS,DD) | 2026-09-04_52w-high-proximity_C.py |
| 2026-09-04 | 13 broad/COMP-n20 | 13.1% | 0.96 | -20.1% | 1.12 / 0.81 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H2) | 2026-09-04_52w-high-proximity_C.py |
| 2026-09-04 | 13 broad/COMP-n30 | 12.2% | 0.97 | -20.3% | 1.15 / 0.82 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H2,DD) | 2026-09-04_52w-high-proximity_C.py |
| 2026-09-04 | 13 broad/PROX-n5 | 0.7% | 0.13 | -22.3% | -0.03 / 0.27 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_52w-high-proximity_C.py |
| 2026-09-04 | 13 broad/PROX-n10 | 3.4% | 0.40 | -22.1% | 0.45 / 0.36 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_52w-high-proximity_C.py |
| 2026-09-04 | 13 broad/PROX-n20 | 5.2% | 0.58 | -15.0% | 0.73 / 0.46 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_52w-high-proximity_C.py |
| 2026-09-04 | 13 broad/PROX-n30 | 7.2% | 0.80 | -15.4% | 0.94 / 0.67 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_52w-high-proximity_C.py |
| 2026-09-04 | 13 broad/BLEND-n5 | 7.5% | 0.58 | -27.2% | 0.65 / 0.52 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_52w-high-proximity_C.py |
| 2026-09-04 | 13 broad/BLEND-n10 | 6.9% | 0.60 | -20.1% | 0.66 / 0.56 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_52w-high-proximity_C.py |
| 2026-09-04 | 13 broad/BLEND-n20 | 7.4% | 0.69 | -18.0% | 0.79 / 0.61 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_52w-high-proximity_C.py |
| 2026-09-04 | 13 broad/BLEND-n30 | 8.8% | 0.84 | -18.0% | 0.96 / 0.73 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H2,OOS,CAGR) | 2026-09-04_52w-high-proximity_C.py |
| 2026-09-04 | 11 u56/v1@0bps | 9.0% | 0.90 | -13.6% | 0.88 / 0.92 | 0.67 (0.64/0.69) | KILL 4b (H1,CAGR) | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 u56/v1@5bps | 7.7% | 0.78 | -13.7% | 0.76 / 0.81 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 u56/v1@10bps | 6.5% | 0.67 | -13.8% | 0.64 / 0.69 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 u56/v1@15bps | 5.2% | 0.55 | -14.0% | 0.52 / 0.58 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 u56/v1@25bps | 2.8% | 0.32 | -15.6% | 0.28 / 0.35 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 u56/v1@50bps | -3.1% | -0.26 | -46.8% | -0.30 / -0.22 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 u56/v1@100bps | -13.9% | -1.35 | -93.0% | -1.42 / -1.30 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 u56/CAND20@0bps | 13.8% | 1.18 | -18.2% | 1.18 / 1.18 | 0.67 (0.64/0.69) | KEEP 4b | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 u56/CAND20@5bps | 13.2% | 1.13 | -18.3% | 1.13 / 1.14 | 0.67 (0.64/0.69) | KEEP 4b | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 u56/CAND20@10bps | 12.7% | 1.09 | -18.3% | 1.09 / 1.10 | 0.67 (0.64/0.69) | KEEP 4b | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 u56/CAND20@15bps | 12.1% | 1.05 | -18.4% | 1.04 / 1.06 | 0.67 (0.64/0.69) | KEEP 4b | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 u56/CAND20@25bps | 11.1% | 0.97 | -18.4% | 0.95 / 0.99 | 0.67 (0.64/0.69) | KILL 4b (H1) | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 u56/CAND20@50bps | 8.4% | 0.76 | -18.7% | 0.73 / 0.79 | 0.67 (0.64/0.69) | 4a-pass, KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 u56/CAND20@100bps | 3.3% | 0.34 | -20.3% | 0.28 / 0.39 | 0.67 (0.64/0.69) | 4a-pass, KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 u56/EWall@0bps | 11.3% | 1.13 | -15.8% | 1.15 / 1.12 | 0.67 (0.64/0.69) | KEEP 4b | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 u56/EWall@5bps | 10.9% | 1.09 | -15.8% | 1.11 / 1.08 | 0.67 (0.64/0.69) | KEEP 4b | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 u56/EWall@10bps | 10.4% | 1.05 | -15.9% | 1.07 / 1.04 | 0.67 (0.64/0.69) | KILL 4b (CAGR) | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 u56/EWall@15bps | 10.0% | 1.01 | -15.9% | 1.03 / 0.99 | 0.67 (0.64/0.69) | KILL 4b (CAGR) | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 u56/EWall@25bps | 9.1% | 0.93 | -16.1% | 0.95 / 0.91 | 0.67 (0.64/0.69) | KILL 4b (H1,CAGR) | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 u56/EWall@50bps | 6.8% | 0.72 | -18.5% | 0.74 / 0.70 | 0.67 (0.64/0.69) | 4a-pass, KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 u56/EWall@100bps | 2.5% | 0.30 | -25.0% | 0.33 / 0.27 | 0.67 (0.64/0.69) | 4a-pass, KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 broad/v1@0bps | 9.6% | 0.92 | -18.4% | 1.04 / 0.81 | 0.64 (0.76/0.54) | KILL 4b (H2,OOS,CAGR) | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 broad/v1@5bps | 8.0% | 0.78 | -19.4% | 0.90 / 0.67 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 broad/v1@10bps | 6.4% | 0.64 | -21.2% | 0.76 / 0.54 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 broad/v1@15bps | 4.9% | 0.50 | -23.1% | 0.62 / 0.40 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 broad/v1@25bps | 1.8% | 0.22 | -26.7% | 0.34 / 0.12 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 broad/v1@50bps | -5.4% | -0.46 | -62.9% | -0.35 / -0.55 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 broad/v1@100bps | -18.4% | -1.73 | -97.3% | -1.64 / -1.81 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 broad/CAND20@0bps | 14.7% | 1.06 | -20.0% | 1.23 / 0.91 | 0.64 (0.76/0.54) | KEEP 4b | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 broad/CAND20@5bps | 13.9% | 1.01 | -20.0% | 1.18 / 0.86 | 0.64 (0.76/0.54) | KEEP 4b | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 broad/CAND20@10bps | 13.1% | 0.96 | -20.1% | 1.12 / 0.81 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H2) | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 broad/CAND20@15bps | 12.3% | 0.91 | -20.1% | 1.07 / 0.76 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H2,OOS) | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 broad/CAND20@25bps | 10.8% | 0.81 | -20.2% | 0.97 / 0.67 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H2,OOS) | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 broad/CAND20@50bps | 7.0% | 0.56 | -21.9% | 0.72 / 0.42 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 broad/CAND20@100bps | -0.1% | 0.06 | -40.6% | 0.21 / -0.07 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 broad/EWall@0bps | 11.7% | 1.11 | -17.3% | 1.22 / 1.00 | 0.64 (0.76/0.54) | 4a-pass, KEEP 4b | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 broad/EWall@5bps | 11.2% | 1.07 | -17.5% | 1.18 / 0.96 | 0.64 (0.76/0.54) | 4a-pass, KEEP 4b | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 broad/EWall@10bps | 10.7% | 1.03 | -17.7% | 1.15 / 0.92 | 0.64 (0.76/0.54) | 4a-pass, KEEP 4b | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 broad/EWall@15bps | 10.3% | 0.99 | -17.9% | 1.11 / 0.88 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (CAGR) | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 broad/EWall@25bps | 9.4% | 0.91 | -18.2% | 1.03 / 0.79 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H2,CAGR) | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 broad/EWall@50bps | 7.1% | 0.71 | -20.3% | 0.84 / 0.58 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 11 broad/EWall@100bps | 2.8% | 0.31 | -24.9% | 0.47 / 0.17 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_cost-sensitivity_cloud.py |
| 2026-09-04 | 73 U56/EWall (inv 75.0%, turn 8.2x, prem +0.000, OOS 1.11) | 10.4% | 1.05 | -15.9% | 1.07 / 1.04 | 0.67 (0.64/0.69) | KILL 4a/KILL 4b(CAGR) | research/backtests/2026-09-04_asset-class-dispersion_cloud.py |
| 2026-09-04 | 73 U56/CANDg-n5 (inv 75.0%, turn 18.5x, prem -0.127, OOS 0.96) | 16.2% | 0.92 | -21.5% | 0.89 / 0.96 | 0.67 (0.64/0.69) | KILL 4a/KILL 4b(H1,DD) | research/backtests/2026-09-04_asset-class-dispersion_cloud.py |
| 2026-09-04 | 73 U56/CANDg-n10 (inv 75.0%, turn 14.7x, prem -0.117, OOS 0.99) | 13.1% | 0.93 | -17.5% | 0.90 / 0.96 | 0.67 (0.64/0.69) | KILL 4a/KILL 4b(H1) | research/backtests/2026-09-04_asset-class-dispersion_cloud.py |
| 2026-09-04 | 73 U56/CANDg-n20 (inv 75.0%, turn 11.0x, prem +0.014, OOS 1.13) | 12.8% | 1.06 | -18.3% | 1.07 / 1.07 | 0.67 (0.64/0.69) | KILL 4a/KEEP 4b | research/backtests/2026-09-04_asset-class-dispersion_cloud.py |
| 2026-09-04 | 73 U56/CAND-n20 (inv 71.7%, turn 9.6x, prem +0.043, OOS 1.17) | 12.7% | 1.09 | -18.3% | 1.09 / 1.10 | 0.67 (0.64/0.69) | KILL 4a/KEEP 4b | research/backtests/2026-09-04_asset-class-dispersion_cloud.py |
| 2026-09-04 | 73 ETF36/EWall (inv 75.0%, turn 8.5x, prem +0.000, OOS 0.67) | 5.1% | 0.63 | -21.8% | 0.67 / 0.60 | 0.46 (0.62/0.34) | KILL 4a/KILL 4b(H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_asset-class-dispersion_cloud.py |
| 2026-09-04 | 73 ETF36/CANDg-n5 (inv 75.0%, turn 16.1x, prem -0.100, OOS 0.58) | 6.3% | 0.53 | -23.6% | 0.55 / 0.52 | 0.46 (0.62/0.34) | KILL 4a/KILL 4b(H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_asset-class-dispersion_cloud.py |
| 2026-09-04 | 73 ETF36/CANDg-n10 (inv 75.0%, turn 13.4x, prem -0.018, OOS 0.68) | 6.3% | 0.61 | -22.6% | 0.62 / 0.61 | 0.46 (0.62/0.34) | KILL 4a/KILL 4b(H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_asset-class-dispersion_cloud.py |
| 2026-09-04 | 73 ETF36/CANDg-n20 (inv 75.0%, turn 9.6x, prem +0.042, OOS 0.74) | 6.1% | 0.67 | -22.1% | 0.67 / 0.68 | 0.46 (0.62/0.34) | KILL 4a/KILL 4b(H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_asset-class-dispersion_cloud.py |
| 2026-09-04 | 73 ETF24/EWall (inv 73.6%, turn 9.6x, prem +0.000, OOS 0.73) | 8.2% | 0.71 | -29.4% | 0.77 / 0.65 | 0.52 (0.57/0.49) | KILL 4a/KILL 4b(H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_asset-class-dispersion_cloud.py |
| 2026-09-04 | 73 ETF24/CANDg-n5 (inv 73.6%, turn 15.9x, prem -0.125, OOS 0.61) | 7.4% | 0.58 | -31.4% | 0.61 / 0.56 | 0.52 (0.57/0.49) | KILL 4a/KILL 4b(H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_asset-class-dispersion_cloud.py |
| 2026-09-04 | 73 ETF24/CANDg-n10 (inv 73.6%, turn 13.2x, prem -0.037, OOS 0.66) | 8.1% | 0.67 | -30.4% | 0.75 / 0.60 | 0.52 (0.57/0.49) | KILL 4a/KILL 4b(H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_asset-class-dispersion_cloud.py |
| 2026-09-04 | 73 ETF24/CANDg-n20 (inv 73.6%, turn 9.9x, prem +0.004, OOS 0.73) | 8.3% | 0.71 | -29.4% | 0.79 / 0.65 | 0.52 (0.57/0.49) | KILL 4a/KILL 4b(H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_asset-class-dispersion_cloud.py |
| 2026-09-04 | 73 STK20/EWall (inv 74.7%, turn 9.1x, prem +0.000, OOS 1.44) | 19.5% | 1.25 | -30.8% | 1.13 / 1.37 | 1.08 (1.06/1.10) | KILL 4a/KILL 4b(DD) | research/backtests/2026-09-04_asset-class-dispersion_cloud.py |
| 2026-09-04 | 73 STK20/CANDg-n5 (inv 74.7%, turn 16.3x, prem -0.204, OOS 1.18) | 19.8% | 1.04 | -30.8% | 0.89 / 1.19 | 1.08 (1.06/1.10) | KILL 4a/KILL 4b(H1,DD) | research/backtests/2026-09-04_asset-class-dispersion_cloud.py |
| 2026-09-04 | 73 STK20/CANDg-n10 (inv 74.7%, turn 11.0x, prem -0.004, OOS 1.41) | 21.0% | 1.24 | -30.8% | 1.11 / 1.38 | 1.08 (1.06/1.10) | KILL 4a/KILL 4b(DD) | research/backtests/2026-09-04_asset-class-dispersion_cloud.py |
| 2026-09-04 | 73 STK20/CANDg-n20 (inv 74.7%, turn 9.2x, prem -0.003, OOS 1.44) | 19.5% | 1.25 | -30.8% | 1.12 / 1.37 | 1.08 (1.06/1.10) | KILL 4a/KILL 4b(DD) | research/backtests/2026-09-04_asset-class-dispersion_cloud.py |
| 2026-09-04 | 73 STK20/CAND-n10 (inv 69.1%, turn 8.5x, prem +0.057, OOS 1.37) | 19.0% | 1.30 | -17.3% | 1.29 / 1.32 | 1.08 (1.06/1.10) | KEEP 4a/KEEP 4b | research/backtests/2026-09-04_asset-class-dispersion_cloud.py |
| 2026-09-04 | 73 STK20/CAND-n20 (inv 49.2%, turn 3.5x, prem +0.090, OOS 1.45) | 12.1% | 1.34 | -12.1% | 1.34 / 1.34 | 1.08 (1.06/1.10) | KEEP 4a/KEEP 4b | research/backtests/2026-09-04_asset-class-dispersion_cloud.py |
| 2026-09-04 | 73 B136/EWall (inv 75.0%, turn 8.3x, prem +0.000, OOS 1.02) | 10.8% | 1.03 | -17.7% | 1.15 / 0.92 | 0.64 (0.76/0.54) | KEEP 4a/KEEP 4b | research/backtests/2026-09-04_asset-class-dispersion_cloud.py |
| 2026-09-04 | 73 B136/CANDg-n5 (inv 75.0%, turn 21.9x, prem -0.152, OOS 0.83) | 16.7% | 0.88 | -24.0% | 1.00 / 0.79 | 0.64 (0.76/0.54) | KILL 4a/KILL 4b(H2,OOS,DD) | research/backtests/2026-09-04_asset-class-dispersion_cloud.py |
| 2026-09-04 | 73 B136/CANDg-n10 (inv 75.0%, turn 17.9x, prem -0.134, OOS 0.78) | 14.3% | 0.90 | -21.4% | 1.12 / 0.71 | 0.64 (0.76/0.54) | KILL 4a/KILL 4b(H2,OOS,DD) | research/backtests/2026-09-04_asset-class-dispersion_cloud.py |
| 2026-09-04 | 73 B136/CANDg-n20 (inv 75.0%, turn 14.3x, prem -0.085, OOS 0.89) | 13.0% | 0.94 | -20.1% | 1.10 / 0.81 | 0.64 (0.76/0.54) | KEEP 4a/KILL 4b(H2) | research/backtests/2026-09-04_asset-class-dispersion_cloud.py |
| 2026-09-04 | 73 BSTK100/EWall (inv 74.8%, turn 8.6x, prem +0.000, OOS 1.01) | 12.8% | 1.02 | -26.1% | 1.14 / 0.91 | 0.69 (0.90/0.51) | KILL 4a/KILL 4b(DD) | research/backtests/2026-09-04_asset-class-dispersion_cloud.py |
| 2026-09-04 | 73 BSTK100/CANDg-n5 (inv 74.8%, turn 21.5x, prem -0.174, OOS 0.78) | 16.4% | 0.85 | -28.7% | 0.99 / 0.73 | 0.69 (0.90/0.51) | KILL 4a/KILL 4b(H2,OOS,DD) | research/backtests/2026-09-04_asset-class-dispersion_cloud.py |
| 2026-09-04 | 73 BSTK100/CANDg-n10 (inv 74.8%, turn 17.9x, prem -0.144, OOS 0.75) | 14.5% | 0.88 | -29.1% | 1.10 / 0.68 | 0.69 (0.90/0.51) | KILL 4a/KILL 4b(H2,OOS,DD) | research/backtests/2026-09-04_asset-class-dispersion_cloud.py |
| 2026-09-04 | 73 BSTK100/CANDg-n20 (inv 74.8%, turn 13.5x, prem -0.078, OOS 0.89) | 13.9% | 0.95 | -27.3% | 1.11 / 0.80 | 0.69 (0.90/0.51) | KILL 4a/KILL 4b(H2,DD) | research/backtests/2026-09-04_asset-class-dispersion_cloud.py |
| 2026-09-04 | 73 SMALL439/EWall (inv 75.0%, turn 13.4x, prem +0.000, OOS 0.28) | 3.6% | 0.33 | -40.0% | 0.44 / 0.25 | 0.56 (0.75/0.40) | KILL 4a/KILL 4b(H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_asset-class-dispersion_cloud.py |
| 2026-09-04 | 73 SMALL439/CANDg-n5 (inv 75.0%, turn 30.1x, prem -0.014, OOS 0.42) | 4.9% | 0.32 | -40.2% | 0.44 / 0.21 | 0.56 (0.75/0.40) | KILL 4a/KILL 4b(H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_asset-class-dispersion_cloud.py |
| 2026-09-04 | 73 SMALL439/CANDg-n10 (inv 75.0%, turn 24.3x, prem +0.142, OOS 0.55) | 7.7% | 0.47 | -31.4% | 0.54 / 0.42 | 0.56 (0.75/0.40) | KILL 4a/KILL 4b(H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_asset-class-dispersion_cloud.py |
| 2026-09-04 | 73 SMALL439/CANDg-n20 (inv 75.0%, turn 20.5x, prem +0.115, OOS 0.46) | 6.4% | 0.45 | -33.5% | 0.61 / 0.31 | 0.56 (0.75/0.40) | KILL 4a/KILL 4b(H1,H2,OOS,DD,CAGR) | research/backtests/2026-09-04_asset-class-dispersion_cloud.py |
| 2026-09-04 | 80 u56/v1 | 6.5% | 0.67 | -13.8% | 0.64 / 0.69 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 u56/EWall | 10.4% | 1.05 | -15.9% | 1.07 / 1.04 | 0.67 (0.64/0.69) | KILL 4b (CAGR) | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 u56/COMP-n5 | 16.5% | 0.95 | -21.6% | 0.90 / 1.00 | 0.67 (0.64/0.69) | KILL 4b (H1,DD) | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 u56/COMP-n10 | 12.9% | 0.93 | -17.5% | 0.92 / 0.95 | 0.67 (0.64/0.69) | KILL 4b (H1) | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 u56/COMP-n20 | 12.7% | 1.09 | -18.3% | 1.09 / 1.10 | 0.67 (0.64/0.69) | KEEP 4b | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 u56/COMP-n30 | 11.0% | 1.10 | -16.6% | 1.03 / 1.17 | 0.67 (0.64/0.69) | KEEP 4b | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 u56/IPROX-n5 | 13.9% | 0.83 | -29.7% | 0.72 / 0.92 | 0.67 (0.64/0.69) | KILL 4b (H1,DD) | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 u56/IPROX-n10 | 11.6% | 0.85 | -20.7% | 0.86 / 0.85 | 0.67 (0.64/0.69) | KILL 4b (H1,DD) | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 u56/IPROX-n20 | 10.6% | 0.96 | -18.3% | 0.98 / 0.94 | 0.67 (0.64/0.69) | KILL 4b (CAGR) | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 u56/IPROX-n30 | 9.5% | 0.99 | -15.9% | 0.96 / 1.02 | 0.67 (0.64/0.69) | KILL 4b (CAGR) | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 u56/IPROXn-n5 | 7.1% | 0.60 | -27.7% | 0.62 / 0.58 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 u56/IPROXn-n10 | 9.5% | 0.83 | -18.9% | 0.86 / 0.80 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 u56/IPROXn-n20 | 9.2% | 0.90 | -17.1% | 0.96 / 0.85 | 0.67 (0.64/0.69) | KILL 4b (CAGR) | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 u56/IPROXn-n30 | 8.8% | 0.97 | -15.7% | 1.01 / 0.93 | 0.67 (0.64/0.69) | KILL 4b (CAGR) | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 u56/LOWVOL-n5 | 1.5% | 0.37 | -15.5% | 0.57 / 0.21 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 u56/LOWVOL-n10 | 3.9% | 0.68 | -18.4% | 0.95 / 0.46 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 u56/LOWVOL-n20 | 6.8% | 0.92 | -12.8% | 1.10 / 0.75 | 0.67 (0.64/0.69) | 4a-pass, KILL 4b (H2,OOS,CAGR) | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 u56/LOWVOL-n30 | 7.4% | 0.96 | -13.8% | 0.96 / 0.96 | 0.67 (0.64/0.69) | 4a-pass, KILL 4b (CAGR) | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 broad/v1 | 6.4% | 0.64 | -21.2% | 0.76 / 0.54 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 broad/EWall | 10.7% | 1.03 | -17.7% | 1.15 / 0.92 | 0.64 (0.76/0.54) | 4a-pass, KEEP 4b | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 broad/COMP-n5 | 16.7% | 0.88 | -23.4% | 1.02 / 0.78 | 0.64 (0.76/0.54) | KILL 4b (H2,OOS,DD) | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 broad/COMP-n10 | 14.2% | 0.89 | -21.4% | 1.11 / 0.71 | 0.64 (0.76/0.54) | KILL 4b (H2,OOS,DD) | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 broad/COMP-n20 | 13.1% | 0.96 | -20.1% | 1.12 / 0.81 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H2) | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 broad/COMP-n30 | 12.2% | 0.97 | -20.3% | 1.15 / 0.82 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H2,DD) | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 broad/IPROX-n5 | 16.2% | 0.87 | -28.5% | 0.99 / 0.76 | 0.64 (0.76/0.54) | KILL 4b (H2,OOS,DD) | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 broad/IPROX-n10 | 14.2% | 0.90 | -22.6% | 0.92 / 0.89 | 0.64 (0.76/0.54) | KILL 4b (H1,DD) | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 broad/IPROX-n20 | 13.4% | 0.98 | -19.7% | 1.04 / 0.93 | 0.64 (0.76/0.54) | 4a-pass, KEEP 4b | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 broad/IPROX-n30 | 12.1% | 0.97 | -19.8% | 1.06 / 0.90 | 0.64 (0.76/0.54) | 4a-pass, KEEP 4b | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 broad/IPROXn-n5 | 6.5% | 0.55 | -26.2% | 0.67 / 0.45 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 broad/IPROXn-n10 | 10.8% | 0.89 | -19.5% | 1.03 / 0.77 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H2,OOS) | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 broad/IPROXn-n20 | 10.8% | 0.91 | -19.3% | 1.07 / 0.77 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H2,OOS) | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 broad/IPROXn-n30 | 10.4% | 0.91 | -19.0% | 1.04 / 0.80 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H2,OOS,CAGR) | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 broad/LOWVOL-n5 | 1.6% | 0.40 | -13.9% | 0.60 / 0.24 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 broad/LOWVOL-n10 | 3.3% | 0.60 | -14.4% | 0.82 / 0.42 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 broad/LOWVOL-n20 | 6.0% | 0.85 | -13.8% | 1.12 / 0.64 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H2,OOS,CAGR) | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 80 broad/LOWVOL-n30 | 6.8% | 0.88 | -15.0% | 1.18 / 0.61 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H2,OOS,CAGR) | 2026-09-04_prox-inverted-signal_cloud.py |
| 2026-09-04 | 83 u56/CAND20/budget-pro0.1 | 13.8% | 1.12 | -21.1% | 1.13 / 1.12 | 0.67 (0.64/0.69) | KILL 4b (DD) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 u56/CAND20/budget-pro0.2 | 12.9% | 1.08 | -18.8% | 1.08 / 1.09 | 0.67 (0.64/0.69) | 4b-pass u56 only, KILL cross-universe | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 u56/CAND20/budget-pro0.4 | 12.6% | 1.08 | -18.3% | 1.09 / 1.08 | 0.67 (0.64/0.69) | 4b-pass u56 only, KILL cross-universe | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 u56/CAND20/budget-top0.1 | 15.3% | 1.11 | -22.9% | 1.14 / 1.10 | 0.67 (0.64/0.69) | KILL 4b (DD) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 u56/CAND20/budget-top0.2 | 13.7% | 1.08 | -21.1% | 1.09 / 1.09 | 0.67 (0.64/0.69) | KILL 4b (DD) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 u56/CAND20/budget-top0.4 | 12.6% | 1.08 | -17.5% | 1.08 / 1.08 | 0.67 (0.64/0.69) | 4b-pass u56 only, KILL cross-universe | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 u56/CAND20/control | 12.7% | 1.09 | -18.3% | 1.09 / 1.10 | 0.67 (0.64/0.69) | 4b-pass u56 only, KILL cross-universe | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 u56/CAND20/gross0.35 | 5.9% | 1.09 | -8.8% | 1.09 / 1.10 | 0.67 (0.64/0.69) | 4a-pass, KILL 4b (CAGR) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 u56/CAND20/gross0.45 | 7.6% | 1.09 | -11.2% | 1.09 / 1.10 | 0.67 (0.64/0.69) | 4a-pass, KILL 4b (CAGR) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 u56/CAND20/gross0.55 | 9.3% | 1.09 | -13.6% | 1.09 / 1.10 | 0.67 (0.64/0.69) | 4a-pass, KILL 4b (CAGR) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 u56/CAND20/gross0.65 | 11.0% | 1.09 | -16.0% | 1.09 / 1.10 | 0.67 (0.64/0.69) | 4b-pass u56 only, KILL cross-universe | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 u56/EWall/budget-pro0.1 | 11.2% | 1.08 | -18.7% | 1.11 / 1.06 | 0.67 (0.64/0.69) | 4b-pass u56 only, KILL cross-universe | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 u56/EWall/budget-pro0.2 | 10.8% | 1.06 | -17.8% | 1.06 / 1.06 | 0.67 (0.64/0.69) | 4b-pass u56 only, KILL cross-universe | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 u56/EWall/budget-pro0.4 | 10.5% | 1.05 | -16.7% | 1.04 / 1.05 | 0.67 (0.64/0.69) | KILL 4b (CAGR) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 u56/EWall/budget-top0.1 | 12.0% | 1.08 | -21.2% | 1.21 / 1.00 | 0.67 (0.64/0.69) | KILL 4b (DD) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 u56/EWall/budget-top0.2 | 11.0% | 1.04 | -19.2% | 1.05 / 1.05 | 0.67 (0.64/0.69) | 4b-pass u56 only, KILL cross-universe | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 u56/EWall/budget-top0.4 | 10.6% | 1.03 | -18.9% | 1.05 / 1.01 | 0.67 (0.64/0.69) | KILL 4b (CAGR) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 u56/EWall/control | 10.4% | 1.05 | -15.9% | 1.07 / 1.04 | 0.67 (0.64/0.69) | KILL 4b (CAGR) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 u56/EWall/gross0.35 | 4.9% | 1.05 | -7.6% | 1.07 / 1.04 | 0.67 (0.64/0.69) | 4a-pass, KILL 4b (CAGR) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 u56/EWall/gross0.45 | 6.2% | 1.05 | -9.7% | 1.07 / 1.04 | 0.67 (0.64/0.69) | 4a-pass, KILL 4b (CAGR) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 u56/EWall/gross0.55 | 7.6% | 1.05 | -11.8% | 1.07 / 1.04 | 0.67 (0.64/0.69) | 4a-pass, KILL 4b (CAGR) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 u56/EWall/gross0.65 | 9.0% | 1.05 | -13.8% | 1.07 / 1.04 | 0.67 (0.64/0.69) | KILL 4b (CAGR) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 broad/CAND20/budget-pro0.1 | 15.3% | 1.05 | -24.7% | 1.29 / 0.86 | 0.64 (0.76/0.54) | KILL 4b (DD) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 broad/CAND20/budget-pro0.2 | 13.7% | 0.98 | -22.6% | 1.21 / 0.79 | 0.64 (0.76/0.54) | KILL 4b (H2,OOS,DD) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 broad/CAND20/budget-pro0.4 | 12.9% | 0.94 | -20.2% | 1.14 / 0.77 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H2,OOS) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 broad/CAND20/budget-top0.1 | 19.2% | 1.10 | -31.8% | 1.28 / 0.97 | 0.64 (0.76/0.54) | KILL 4b (DD) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 broad/CAND20/budget-top0.2 | 16.6% | 1.01 | -30.8% | 1.23 / 0.83 | 0.64 (0.76/0.54) | KILL 4b (H2,DD) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 broad/CAND20/budget-top0.4 | 13.2% | 0.95 | -21.3% | 1.15 / 0.78 | 0.64 (0.76/0.54) | KILL 4b (H2,OOS,DD) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 broad/CAND20/control | 13.1% | 0.96 | -20.1% | 1.12 / 0.81 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H2) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 broad/CAND20/gross0.35 | 6.1% | 0.95 | -9.7% | 1.12 / 0.81 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H2,CAGR) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 broad/CAND20/gross0.45 | 7.9% | 0.96 | -12.3% | 1.12 / 0.81 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H2,CAGR) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 broad/CAND20/gross0.55 | 9.6% | 0.96 | -14.9% | 1.12 / 0.81 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H2,CAGR) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 broad/CAND20/gross0.65 | 11.4% | 0.96 | -17.5% | 1.12 / 0.81 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H2) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 broad/EWall/budget-pro0.1 | 11.5% | 1.05 | -22.6% | 1.16 / 0.96 | 0.64 (0.76/0.54) | KILL 4b (DD) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 broad/EWall/budget-pro0.2 | 11.1% | 1.03 | -21.8% | 1.14 / 0.93 | 0.64 (0.76/0.54) | KILL 4b (DD) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 broad/EWall/budget-pro0.4 | 10.8% | 1.02 | -20.6% | 1.14 / 0.91 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (DD) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 broad/EWall/budget-top0.1 | 12.3% | 1.08 | -23.5% | 1.18 / 0.99 | 0.64 (0.76/0.54) | KILL 4b (DD) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 broad/EWall/budget-top0.2 | 11.7% | 1.03 | -24.9% | 1.16 / 0.92 | 0.64 (0.76/0.54) | KILL 4b (DD) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 broad/EWall/budget-top0.4 | 10.8% | 0.98 | -23.3% | 1.13 / 0.87 | 0.64 (0.76/0.54) | KILL 4b (DD) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 broad/EWall/control | 10.7% | 1.03 | -17.7% | 1.15 / 0.92 | 0.64 (0.76/0.54) | 4b-pass broad only, KILL cross-universe | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 broad/EWall/gross0.35 | 5.0% | 1.03 | -8.5% | 1.14 / 0.92 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (CAGR) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 broad/EWall/gross0.45 | 6.4% | 1.03 | -10.9% | 1.14 / 0.92 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (CAGR) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 broad/EWall/gross0.55 | 7.9% | 1.03 | -13.2% | 1.14 / 0.92 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (CAGR) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 83 broad/EWall/gross0.65 | 9.3% | 1.03 | -15.5% | 1.15 / 0.92 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (CAGR) | 2026-09-04_turnover-budget_B.py |
| 2026-09-04 | 15 u56/v1 | 6.5% | 0.67 | -13.8% | 0.64 / 0.69 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/CAND20 | 12.7% | 1.09 | -18.3% | 1.09 / 1.10 | 0.67 (0.64/0.69) | 4b-pass | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/EWall | 10.4% | 1.05 | -15.9% | 1.07 / 1.04 | 0.67 (0.64/0.69) | KILL 4b (CAGR) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/v1/matched/same/c5 | 7.5% | 0.76 | -13.7% | 0.75 / 0.77 | 0.67 (0.64/0.69) | 4a-pass, KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/v1/matched/same/c10 | 8.6% | 0.82 | -15.0% | 0.85 / 0.80 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,CAGR) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/v1/matched/same/c15 | 9.6% | 0.86 | -19.2% | 0.93 / 0.81 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,CAGR) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/v1/matched/trend/c5 | 8.9% | 0.85 | -15.6% | 0.86 / 0.86 | 0.67 (0.64/0.69) | KILL 4b (H1,CAGR) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/v1/matched/trend/c10 | 11.3% | 0.94 | -17.6% | 1.04 / 0.89 | 0.67 (0.64/0.69) | 4b-pass | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/v1/matched/trend/c15 | 13.6% | 0.95 | -22.9% | 1.18 / 0.87 | 0.67 (0.64/0.69) | KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/v1/add/same/c5 | 7.7% | 0.76 | -14.3% | 0.75 / 0.77 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/v1/add/same/c10 | 9.0% | 0.82 | -16.0% | 0.85 / 0.81 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,CAGR) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/v1/add/same/c15 | 10.2% | 0.86 | -19.9% | 0.93 / 0.83 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,CAGR) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/v1/add/trend/c5 | 9.3% | 0.85 | -17.0% | 0.85 / 0.86 | 0.67 (0.64/0.69) | KILL 4b (H1,CAGR) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/v1/add/trend/c10 | 12.1% | 0.93 | -20.4% | 1.03 / 0.91 | 0.67 (0.64/0.69) | KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/v1/add/trend/c15 | 14.8% | 0.96 | -25.2% | 1.17 / 0.91 | 0.67 (0.64/0.69) | KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/CAND20/matched/same/c5 | 13.5% | 1.15 | -18.2% | 1.18 / 1.13 | 0.67 (0.64/0.69) | 4b-pass | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/CAND20/matched/same/c10 | 14.3% | 1.18 | -19.1% | 1.25 / 1.13 | 0.67 (0.64/0.69) | 4b-pass | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/CAND20/matched/same/c15 | 15.1% | 1.18 | -23.3% | 1.31 / 1.09 | 0.67 (0.64/0.69) | KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/CAND20/matched/trend/c5 | 14.8% | 1.21 | -19.7% | 1.27 / 1.19 | 0.67 (0.64/0.69) | 4b-pass | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/CAND20/matched/trend/c10 | 16.9% | 1.23 | -23.6% | 1.41 / 1.14 | 0.67 (0.64/0.69) | KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/CAND20/matched/trend/c15 | 18.8% | 1.19 | -29.6% | 1.51 / 1.06 | 0.67 (0.64/0.69) | KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/CAND20/add/same/c5 | 14.0% | 1.16 | -18.8% | 1.19 / 1.15 | 0.67 (0.64/0.69) | 4b-pass | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/CAND20/add/same/c10 | 15.3% | 1.20 | -20.1% | 1.27 / 1.16 | 0.67 (0.64/0.69) | 4b-pass | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/CAND20/add/same/c15 | 16.6% | 1.21 | -24.7% | 1.33 / 1.15 | 0.67 (0.64/0.69) | KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/CAND20/add/trend/c5 | 15.7% | 1.22 | -21.5% | 1.27 / 1.20 | 0.67 (0.64/0.69) | KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/CAND20/add/trend/c10 | 18.6% | 1.25 | -24.9% | 1.42 / 1.19 | 0.67 (0.64/0.69) | KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/CAND20/add/trend/c15 | 21.5% | 1.23 | -31.1% | 1.52 / 1.14 | 0.67 (0.64/0.69) | KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/EWall/matched/same/c5 | 11.4% | 1.12 | -16.4% | 1.17 / 1.08 | 0.67 (0.64/0.69) | 4b-pass | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/EWall/matched/same/c10 | 12.3% | 1.15 | -18.7% | 1.26 / 1.07 | 0.67 (0.64/0.69) | 4b-pass | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/EWall/matched/same/c15 | 13.2% | 1.15 | -22.6% | 1.32 / 1.03 | 0.67 (0.64/0.69) | KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/EWall/matched/trend/c5 | 12.7% | 1.18 | -18.8% | 1.27 / 1.13 | 0.67 (0.64/0.69) | 4b-pass | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/EWall/matched/trend/c10 | 14.9% | 1.19 | -23.3% | 1.43 / 1.07 | 0.67 (0.64/0.69) | KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/EWall/matched/trend/c15 | 17.0% | 1.15 | -29.1% | 1.53 / 0.99 | 0.67 (0.64/0.69) | KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/EWall/add/same/c5 | 11.7% | 1.13 | -16.6% | 1.18 / 1.10 | 0.67 (0.64/0.69) | 4b-pass | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/EWall/add/same/c10 | 13.0% | 1.17 | -19.6% | 1.27 / 1.10 | 0.67 (0.64/0.69) | 4b-pass | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/EWall/add/same/c15 | 14.3% | 1.18 | -24.2% | 1.34 / 1.08 | 0.67 (0.64/0.69) | KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/EWall/add/trend/c5 | 13.4% | 1.20 | -19.2% | 1.28 / 1.15 | 0.67 (0.64/0.69) | 4b-pass | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/EWall/add/trend/c10 | 16.3% | 1.22 | -24.1% | 1.43 / 1.13 | 0.67 (0.64/0.69) | KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 u56/EWall/add/trend/c15 | 19.1% | 1.19 | -30.6% | 1.54 / 1.08 | 0.67 (0.64/0.69) | KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/v1 | 6.4% | 0.64 | -21.2% | 0.76 / 0.54 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/CAND20 | 13.1% | 0.96 | -20.1% | 1.12 / 0.81 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H2) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/EWall | 10.7% | 1.03 | -17.7% | 1.15 / 0.92 | 0.64 (0.76/0.54) | 4a-pass, 4b-pass | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/v1/matched/same/c5 | 7.6% | 0.74 | -22.9% | 0.87 / 0.63 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/v1/matched/same/c10 | 8.7% | 0.81 | -24.9% | 0.96 / 0.68 | 0.64 (0.76/0.54) | KILL 4b (H2,OOS,DD,CAGR) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/v1/matched/same/c15 | 9.8% | 0.85 | -28.4% | 1.04 / 0.71 | 0.64 (0.76/0.54) | KILL 4b (H2,OOS,DD,CAGR) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/v1/matched/trend/c5 | 9.0% | 0.84 | -22.3% | 0.97 / 0.73 | 0.64 (0.76/0.54) | KILL 4b (H2,OOS,DD,CAGR) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/v1/matched/trend/c10 | 11.4% | 0.93 | -23.8% | 1.15 / 0.80 | 0.64 (0.76/0.54) | KILL 4b (H2,DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/v1/matched/trend/c15 | 13.8% | 0.96 | -30.0% | 1.28 / 0.81 | 0.64 (0.76/0.54) | KILL 4b (H2,DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/v1/add/same/c5 | 7.7% | 0.73 | -23.6% | 0.87 / 0.63 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/v1/add/same/c10 | 9.0% | 0.80 | -26.1% | 0.96 / 0.68 | 0.64 (0.76/0.54) | KILL 4b (H2,OOS,DD,CAGR) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/v1/add/same/c15 | 10.2% | 0.84 | -29.3% | 1.04 / 0.72 | 0.64 (0.76/0.54) | KILL 4b (H2,OOS,DD,CAGR) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/v1/add/trend/c5 | 9.3% | 0.83 | -22.6% | 0.97 / 0.74 | 0.64 (0.76/0.54) | KILL 4b (H2,OOS,DD,CAGR) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/v1/add/trend/c10 | 12.1% | 0.92 | -24.9% | 1.13 / 0.81 | 0.64 (0.76/0.54) | KILL 4b (H2,DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/v1/add/trend/c15 | 14.8% | 0.95 | -30.3% | 1.26 / 0.83 | 0.64 (0.76/0.54) | KILL 4b (H2,DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/CAND20/matched/same/c5 | 14.0% | 1.01 | -19.9% | 1.20 / 0.85 | 0.64 (0.76/0.54) | 4a-pass, 4b-pass | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/CAND20/matched/same/c10 | 14.8% | 1.05 | -24.2% | 1.26 / 0.87 | 0.64 (0.76/0.54) | KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/CAND20/matched/same/c15 | 15.6% | 1.07 | -29.2% | 1.31 / 0.86 | 0.64 (0.76/0.54) | KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/CAND20/matched/trend/c5 | 15.4% | 1.08 | -21.7% | 1.27 / 0.93 | 0.64 (0.76/0.54) | KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/CAND20/matched/trend/c10 | 17.5% | 1.14 | -27.8% | 1.39 / 0.95 | 0.64 (0.76/0.54) | KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/CAND20/matched/trend/c15 | 19.6% | 1.14 | -33.5% | 1.49 / 0.93 | 0.64 (0.76/0.54) | KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/CAND20/add/same/c5 | 14.4% | 1.02 | -20.5% | 1.20 / 0.87 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/CAND20/add/same/c10 | 15.8% | 1.07 | -25.3% | 1.27 / 0.91 | 0.64 (0.76/0.54) | KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/CAND20/add/same/c15 | 17.0% | 1.09 | -30.4% | 1.33 / 0.92 | 0.64 (0.76/0.54) | KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/CAND20/add/trend/c5 | 16.1% | 1.09 | -23.2% | 1.28 / 0.94 | 0.64 (0.76/0.54) | KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/CAND20/add/trend/c10 | 19.1% | 1.14 | -29.0% | 1.40 / 0.99 | 0.64 (0.76/0.54) | KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/CAND20/add/trend/c15 | 21.9% | 1.15 | -35.1% | 1.50 / 0.99 | 0.64 (0.76/0.54) | KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/EWall/matched/same/c5 | 11.7% | 1.10 | -18.2% | 1.24 / 0.97 | 0.64 (0.76/0.54) | 4a-pass, 4b-pass | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/EWall/matched/same/c10 | 12.7% | 1.13 | -20.0% | 1.32 / 0.98 | 0.64 (0.76/0.54) | 4a-pass, 4b-pass | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/EWall/matched/same/c15 | 13.6% | 1.14 | -22.9% | 1.38 / 0.95 | 0.64 (0.76/0.54) | KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/EWall/matched/trend/c5 | 13.1% | 1.16 | -20.1% | 1.33 / 1.03 | 0.64 (0.76/0.54) | 4a-pass, 4b-pass | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/EWall/matched/trend/c10 | 15.3% | 1.19 | -24.7% | 1.47 / 1.01 | 0.64 (0.76/0.54) | KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/EWall/matched/trend/c15 | 17.4% | 1.15 | -29.2% | 1.57 / 0.94 | 0.64 (0.76/0.54) | KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/EWall/add/same/c5 | 12.1% | 1.11 | -18.3% | 1.25 / 0.98 | 0.64 (0.76/0.54) | 4a-pass, 4b-pass | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/EWall/add/same/c10 | 13.3% | 1.15 | -20.3% | 1.33 / 1.01 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/EWall/add/same/c15 | 14.6% | 1.16 | -24.5% | 1.40 / 1.00 | 0.64 (0.76/0.54) | KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/EWall/add/trend/c5 | 13.7% | 1.18 | -21.1% | 1.34 / 1.05 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/EWall/add/trend/c10 | 16.6% | 1.21 | -24.8% | 1.49 / 1.06 | 0.64 (0.76/0.54) | KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 15 broad/EWall/add/trend/c15 | 19.4% | 1.19 | -30.4% | 1.59 / 1.03 | 0.64 (0.76/0.54) | KILL 4b (DD) | 2026-09-04_crypto-sleeve_C.py |
| 2026-09-04 | 14 sleeve-standalone thr=5 (100% sleeve, daily) | -1.6% | -0.06 | -51.0% | 0.04 / -0.15 | 0.67 (0.64/0.69) | KILL 4b (all bars) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 sleeve-standalone thr=10 (100% sleeve, daily) | -4.2% | -0.22 | -68.5% | -0.33 / -0.12 | 0.67 (0.64/0.69) | KILL 4b (all bars) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 sleeve-standalone thr=20 (100% sleeve, daily) | -5.3% | -0.24 | -73.1% | -0.32 / -0.17 | 0.67 (0.64/0.69) | KILL 4b (all bars) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 u56/v1+rsi2 f=0.25 thr=5 | 4.6% | 0.53 | -12.9% | 0.54 / 0.52 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 u56/v1+rsi2 f=0.25 thr=10 | 3.9% | 0.44 | -14.6% | 0.37 / 0.50 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 u56/v1+rsi2 f=0.25 thr=20 | 3.6% | 0.39 | -15.1% | 0.33 / 0.45 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 u56/v1+rsi2 f=0.50 thr=5 | 2.6% | 0.32 | -17.4% | 0.37 / 0.28 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 u56/v1+rsi2 f=0.50 thr=10 | 1.2% | 0.17 | -29.5% | 0.08 / 0.25 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 u56/v1+rsi2 f=0.50 thr=20 | 0.7% | 0.12 | -22.7% | 0.04 / 0.18 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 u56/top20+rsi2 f=0.25 thr=5 | 9.1% | 0.90 | -15.6% | 0.92 / 0.88 | 0.67 (0.64/0.69) | KILL 4b (H1,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 u56/top20+rsi2 f=0.25 thr=10 | 8.4% | 0.79 | -15.9% | 0.74 / 0.84 | 0.67 (0.64/0.69) | KILL 4b (H1,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 u56/top20+rsi2 f=0.25 thr=20 | 8.1% | 0.73 | -17.6% | 0.69 / 0.77 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 u56/top20+rsi2 f=0.50 thr=5 | 5.6% | 0.59 | -18.8% | 0.65 / 0.54 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 u56/top20+rsi2 f=0.50 thr=10 | 4.1% | 0.41 | -24.3% | 0.33 / 0.48 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 u56/top20+rsi2 f=0.50 thr=20 | 3.5% | 0.34 | -21.6% | 0.27 / 0.40 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 u56/ew-all+rsi2 f=0.25 thr=5 | 7.4% | 0.83 | -16.8% | 0.88 / 0.78 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 u56/ew-all+rsi2 f=0.25 thr=10 | 6.7% | 0.71 | -17.4% | 0.69 / 0.74 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 u56/ew-all+rsi2 f=0.25 thr=20 | 6.4% | 0.65 | -19.5% | 0.63 / 0.66 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 u56/ew-all+rsi2 f=0.50 thr=5 | 4.5% | 0.51 | -19.2% | 0.60 / 0.44 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 u56/ew-all+rsi2 f=0.50 thr=10 | 3.0% | 0.33 | -26.8% | 0.27 / 0.39 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 u56/ew-all+rsi2 f=0.50 thr=20 | 2.5% | 0.26 | -23.7% | 0.22 / 0.30 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 broad/v1+rsi2 f=0.25 thr=5 | 4.6% | 0.52 | -22.1% | 0.66 / 0.39 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 broad/v1+rsi2 f=0.25 thr=10 | 3.8% | 0.42 | -19.9% | 0.46 / 0.39 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 broad/v1+rsi2 f=0.25 thr=20 | 3.6% | 0.38 | -24.5% | 0.44 / 0.33 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 broad/v1+rsi2 f=0.50 thr=5 | 2.6% | 0.32 | -23.2% | 0.48 / 0.18 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 broad/v1+rsi2 f=0.50 thr=10 | 1.2% | 0.16 | -29.7% | 0.12 / 0.19 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 broad/v1+rsi2 f=0.50 thr=20 | 0.7% | 0.12 | -30.0% | 0.12 / 0.11 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 broad/top20+rsi2 f=0.25 thr=5 | 9.5% | 0.82 | -19.2% | 1.00 / 0.66 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H2,OOS,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 broad/top20+rsi2 f=0.25 thr=10 | 8.7% | 0.73 | -18.3% | 0.82 / 0.65 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 broad/top20+rsi2 f=0.25 thr=20 | 8.4% | 0.68 | -21.2% | 0.79 / 0.58 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 broad/top20+rsi2 f=0.50 thr=5 | 5.8% | 0.57 | -22.0% | 0.76 / 0.41 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 broad/top20+rsi2 f=0.50 thr=10 | 4.3% | 0.41 | -26.2% | 0.42 / 0.40 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 broad/top20+rsi2 f=0.50 thr=20 | 3.8% | 0.34 | -24.6% | 0.39 / 0.30 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 broad/ew-all+rsi2 f=0.25 thr=5 | 7.7% | 0.82 | -18.2% | 0.97 / 0.68 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H2,OOS,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 broad/ew-all+rsi2 f=0.25 thr=10 | 6.9% | 0.71 | -17.5% | 0.76 / 0.66 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 broad/ew-all+rsi2 f=0.25 thr=20 | 6.7% | 0.65 | -20.3% | 0.72 / 0.58 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 broad/ew-all+rsi2 f=0.50 thr=5 | 4.6% | 0.52 | -20.0% | 0.69 / 0.37 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 broad/ew-all+rsi2 f=0.50 thr=10 | 3.1% | 0.34 | -26.3% | 0.32 / 0.35 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 14 broad/ew-all+rsi2 f=0.50 thr=20 | 2.6% | 0.27 | -24.3% | 0.30 / 0.25 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_rsi2-sleeve_cloud.py |
| 2026-09-04 | 89 u56/v1 LOYO-audit | 6.5% | 0.67 | -13.8% | 0.64 / 0.69 | 0.67 (0.64/0.69) | 4b-fail (audited; 0/18 LOYO passes) | 2026-09-04_one-year-leverage-audit_cloud.py |
| 2026-09-04 | 89 u56/top20 LOYO-audit | 12.7% | 1.09 | -18.3% | 1.09 / 1.10 | 0.67 (0.64/0.69) | 4b-pass, LOYO-ROBUST 18/18 | 2026-09-04_one-year-leverage-audit_cloud.py |
| 2026-09-04 | 89 u56/frac085 LOYO-audit | 11.3% | 1.07 | -16.7% | 1.09 / 1.06 | 0.67 (0.64/0.69) | 4b-pass, LOYO-ROBUST 18/18 | 2026-09-04_one-year-leverage-audit_cloud.py |
| 2026-09-04 | 89 u56/ew-band3 LOYO-audit | 11.3% | 1.14 | -15.1% | 1.11 / 1.16 | 0.67 (0.64/0.69) | 4b-pass, LOYO-FRAGILE 17/18 (drop 2022) | 2026-09-04_one-year-leverage-audit_cloud.py |
| 2026-09-04 | 89 u56/EWall LOYO-audit | 10.4% | 1.05 | -15.9% | 1.07 / 1.04 | 0.67 (0.64/0.69) | 4b-fail (audited; 1/18 LOYO passes) | 2026-09-04_one-year-leverage-audit_cloud.py |
| 2026-09-04 | 89 u56/SPY LOYO-audit | 15.3% | 0.89 | -33.7% | 0.96 / 0.84 | 0.67 (0.64/0.69) | 4b-fail (audited; 0/18 LOYO passes) | 2026-09-04_one-year-leverage-audit_cloud.py |
| 2026-09-04 | 89 u56/EWall+c10 LOYO-audit | 12.3% | 1.15 | -18.7% | 1.26 / 1.07 | 0.67 (0.64/0.69) | 4b-pass, LOYO-FRAGILE 17/18 (drop 2020) | 2026-09-04_one-year-leverage-audit_cloud.py |
| 2026-09-04 | 89 broad/v1 LOYO-audit | 6.4% | 0.64 | -21.2% | 0.76 / 0.54 | 0.64 (0.76/0.54) | 4b-fail (audited; 0/18 LOYO passes) | 2026-09-04_one-year-leverage-audit_cloud.py |
| 2026-09-04 | 89 broad/top20 LOYO-audit | 13.1% | 0.96 | -20.1% | 1.12 / 0.81 | 0.64 (0.76/0.54) | 4b-fail (audited; 4/18 LOYO passes) | 2026-09-04_one-year-leverage-audit_cloud.py |
| 2026-09-04 | 89 broad/frac085 LOYO-audit | 11.2% | 1.02 | -18.6% | 1.13 / 0.93 | 0.64 (0.76/0.54) | 4b-pass, LOYO-FRAGILE 17/18 (drop 2020) | 2026-09-04_one-year-leverage-audit_cloud.py |
| 2026-09-04 | 89 broad/ew-band3 LOYO-audit | 11.1% | 1.06 | -16.8% | 1.16 / 0.97 | 0.64 (0.76/0.54) | 4b-pass, LOYO-FRAGILE 17/18 (drop 2020) | 2026-09-04_one-year-leverage-audit_cloud.py |
| 2026-09-04 | 89 broad/EWall LOYO-audit | 10.7% | 1.03 | -17.7% | 1.15 / 0.92 | 0.64 (0.76/0.54) | 4b-pass, LOYO-FRAGILE 10/18 (drop 2011,2013,2014,2015,2017,2018,2020,2022) | 2026-09-04_one-year-leverage-audit_cloud.py |
| 2026-09-04 | 89 broad/SPY LOYO-audit | 15.3% | 0.89 | -33.7% | 0.96 / 0.84 | 0.64 (0.76/0.54) | 4b-fail (audited; 0/18 LOYO passes) | 2026-09-04_one-year-leverage-audit_cloud.py |
| 2026-09-04 | 88 u56/v1 | 6.5% | 0.67 | -13.8% | 0.64 / 0.69 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 u56/CAND20 | 12.7% | 1.09 | -18.3% | 1.09 / 1.10 | 0.67 (0.64/0.69) | 4b-pass | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 u56/EWall | 10.4% | 1.05 | -15.9% | 1.07 / 1.04 | 0.67 (0.64/0.69) | KILL 4b (CAGR) | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 u56/v1/abs0.45 | 7.4% | 0.75 | -13.7% | 0.72 / 0.78 | 0.67 (0.64/0.69) | 4a-pass, KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 u56/v1/abs0.60 | 7.5% | 0.76 | -13.7% | 0.75 / 0.77 | 0.67 (0.64/0.69) | 4a-pass, KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 u56/v1/abs0.80 | 8.0% | 0.79 | -14.0% | 0.79 / 0.80 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 u56/v1/p50 | 7.3% | 0.73 | -15.7% | 0.72 / 0.74 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 u56/v1/p70 | 7.8% | 0.77 | -15.6% | 0.76 / 0.79 | 0.67 (0.64/0.69) | KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 u56/v1/p90 | 8.5% | 0.82 | -15.6% | 0.79 / 0.86 | 0.67 (0.64/0.69) | KILL 4b (H1,CAGR) | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 u56/v1/none | 8.9% | 0.85 | -15.6% | 0.86 / 0.86 | 0.67 (0.64/0.69) | KILL 4b (H1,CAGR) | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 u56/CAND20/abs0.45 | 13.4% | 1.15 | -18.2% | 1.15 / 1.16 | 0.67 (0.64/0.69) | 4b-pass | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 u56/CAND20/abs0.60 | 13.5% | 1.15 | -18.2% | 1.18 / 1.13 | 0.67 (0.64/0.69) | 4b-pass | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 u56/CAND20/abs0.80 | 13.9% | 1.17 | -18.1% | 1.21 / 1.15 | 0.67 (0.64/0.69) | 4b-pass | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 u56/CAND20/p50 | 13.2% | 1.11 | -20.0% | 1.15 / 1.09 | 0.67 (0.64/0.69) | 4b-pass | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 u56/CAND20/p70 | 13.7% | 1.15 | -19.7% | 1.18 / 1.13 | 0.67 (0.64/0.69) | 4b-pass | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 u56/CAND20/p90 | 14.4% | 1.19 | -19.7% | 1.21 / 1.19 | 0.67 (0.64/0.69) | 4b-pass | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 u56/CAND20/none | 14.8% | 1.21 | -19.7% | 1.27 / 1.19 | 0.67 (0.64/0.69) | 4b-pass | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 u56/EWall/abs0.45 | 11.2% | 1.12 | -15.9% | 1.14 / 1.10 | 0.67 (0.64/0.69) | 4b-pass | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 u56/EWall/abs0.60 | 11.4% | 1.12 | -16.4% | 1.17 / 1.08 | 0.67 (0.64/0.69) | 4b-pass | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 u56/EWall/abs0.80 | 11.8% | 1.14 | -18.6% | 1.21 / 1.08 | 0.67 (0.64/0.69) | 4b-pass | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 u56/EWall/p50 | 11.1% | 1.07 | -18.2% | 1.14 / 1.02 | 0.67 (0.64/0.69) | 4b-pass | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 u56/EWall/p70 | 11.6% | 1.11 | -18.8% | 1.18 / 1.07 | 0.67 (0.64/0.69) | 4b-pass | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 u56/EWall/p90 | 12.3% | 1.16 | -18.8% | 1.20 / 1.13 | 0.67 (0.64/0.69) | 4b-pass | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 u56/EWall/none | 12.7% | 1.18 | -18.8% | 1.27 / 1.13 | 0.67 (0.64/0.69) | 4b-pass | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 broad/v1 | 6.4% | 0.64 | -21.2% | 0.76 / 0.54 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 broad/CAND20 | 13.1% | 0.96 | -20.1% | 1.12 / 0.81 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H2) | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 broad/EWall | 10.7% | 1.03 | -17.7% | 1.15 / 0.92 | 0.64 (0.76/0.54) | 4a-pass, 4b-pass | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 broad/v1/abs0.45 | 7.3% | 0.72 | -20.7% | 0.84 / 0.62 | 0.64 (0.76/0.54) | 4a-pass, KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 broad/v1/abs0.60 | 7.6% | 0.74 | -22.9% | 0.87 / 0.63 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 broad/v1/abs0.80 | 8.0% | 0.77 | -22.7% | 0.91 / 0.66 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 broad/v1/p50 | 7.3% | 0.71 | -22.5% | 0.84 / 0.60 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 broad/v1/p70 | 7.9% | 0.75 | -22.5% | 0.88 / 0.65 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 broad/v1/p90 | 8.5% | 0.80 | -22.3% | 0.91 / 0.72 | 0.64 (0.76/0.54) | KILL 4b (H1,H2,OOS,DD,CAGR) | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 broad/v1/none | 9.0% | 0.84 | -22.3% | 0.97 / 0.73 | 0.64 (0.76/0.54) | KILL 4b (H2,OOS,DD,CAGR) | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 broad/CAND20/abs0.45 | 13.9% | 1.01 | -19.9% | 1.17 / 0.87 | 0.64 (0.76/0.54) | 4a-pass, 4b-pass | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 broad/CAND20/abs0.60 | 14.0% | 1.01 | -19.9% | 1.20 / 0.85 | 0.64 (0.76/0.54) | 4a-pass, 4b-pass | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 broad/CAND20/abs0.80 | 14.4% | 1.04 | -21.5% | 1.23 / 0.88 | 0.64 (0.76/0.54) | KILL 4b (DD) | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 broad/CAND20/p50 | 13.7% | 0.99 | -21.6% | 1.18 / 0.83 | 0.64 (0.76/0.54) | KILL 4b (H2,DD) | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 broad/CAND20/p70 | 14.2% | 1.02 | -21.7% | 1.20 / 0.87 | 0.64 (0.76/0.54) | KILL 4b (DD) | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 broad/CAND20/p90 | 14.9% | 1.06 | -21.7% | 1.22 / 0.92 | 0.64 (0.76/0.54) | KILL 4b (DD) | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 broad/CAND20/none | 15.4% | 1.08 | -21.7% | 1.27 / 0.93 | 0.64 (0.76/0.54) | KILL 4b (DD) | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 broad/EWall/abs0.45 | 11.6% | 1.10 | -17.7% | 1.21 / 0.99 | 0.64 (0.76/0.54) | 4a-pass, 4b-pass | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 broad/EWall/abs0.60 | 11.7% | 1.10 | -18.2% | 1.24 / 0.97 | 0.64 (0.76/0.54) | 4a-pass, 4b-pass | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 broad/EWall/abs0.80 | 12.1% | 1.12 | -19.8% | 1.27 / 0.98 | 0.64 (0.76/0.54) | 4a-pass, 4b-pass | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 broad/EWall/p50 | 11.4% | 1.06 | -19.7% | 1.21 / 0.92 | 0.64 (0.76/0.54) | 4a-pass, 4b-pass | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 broad/EWall/p70 | 12.0% | 1.09 | -20.1% | 1.25 / 0.97 | 0.64 (0.76/0.54) | 4a-pass, 4b-pass | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 broad/EWall/p90 | 12.6% | 1.14 | -20.1% | 1.27 / 1.03 | 0.64 (0.76/0.54) | 4a-pass, 4b-pass | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |
| 2026-09-04 | 88 broad/EWall/none | 13.1% | 1.16 | -20.1% | 1.33 / 1.03 | 0.64 (0.76/0.54) | 4a-pass, 4b-pass | 2026-09-04_vol-cap-as-a-satellite-clause_B.py |

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
| 2026-09-04 | 19 RP L= 20 g=0.60 | 5.5% | 1.00 | -14.2% | 1.11 / 0.91 | 0.67 (0.64/0.69) | 4b-fail(CAGR) | 2026-09-04_spy-tlt-gld-riskparity_C.py |
| 2026-09-04 | 19 RP L= 20 g=0.75 | 6.8% | 1.00 | -17.5% | 1.11 / 0.91 | 0.67 (0.64/0.69) | 4b-fail(CAGR) | 2026-09-04_spy-tlt-gld-riskparity_C.py |
| 2026-09-04 | 19 RP L= 20 g=1.00 | 9.1% | 1.00 | -22.7% | 1.11 / 0.91 | 0.67 (0.64/0.69) | 4b-fail(DD,CAGR) | 2026-09-04_spy-tlt-gld-riskparity_C.py |
| 2026-09-04 | 19 RP L= 60 g=0.60 | 5.5% | 1.01 | -14.0% | 1.10 / 0.93 | 0.67 (0.64/0.69) | 4b-fail(CAGR) | 2026-09-04_spy-tlt-gld-riskparity_C.py |
| 2026-09-04 | 19 RP L= 60 g=0.75 | 6.9% | 1.01 | -17.2% | 1.10 / 0.93 | 0.67 (0.64/0.69) | 4b-fail(CAGR) | 2026-09-04_spy-tlt-gld-riskparity_C.py |
| 2026-09-04 | 19 RP L= 60 g=1.00 | 9.1% | 1.00 | -22.4% | 1.10 / 0.93 | 0.67 (0.64/0.69) | 4b-fail(DD,CAGR) | 2026-09-04_spy-tlt-gld-riskparity_C.py |
| 2026-09-04 | 19 RP L=120 g=0.60 | 5.4% | 0.98 | -14.1% | 1.06 / 0.91 | 0.67 (0.64/0.69) | 4b-fail(CAGR) | 2026-09-04_spy-tlt-gld-riskparity_C.py |
| 2026-09-04 | 19 RP L=120 g=0.75 | 6.7% | 0.98 | -17.3% | 1.06 / 0.91 | 0.67 (0.64/0.69) | 4b-fail(CAGR) | 2026-09-04_spy-tlt-gld-riskparity_C.py |
| 2026-09-04 | 19 RP L=120 g=1.00 | 8.9% | 0.98 | -22.5% | 1.06 / 0.91 | 0.67 (0.64/0.69) | 4b-fail(DD,CAGR) | 2026-09-04_spy-tlt-gld-riskparity_C.py |
| 2026-09-04 | 19 RP L=252 g=0.60 | 5.3% | 0.96 | -14.3% | 1.02 / 0.91 | 0.67 (0.64/0.69) | 4b-fail(CAGR) | 2026-09-04_spy-tlt-gld-riskparity_C.py |
| 2026-09-04 | 19 RP L=252 g=0.75 | 6.6% | 0.95 | -17.7% | 1.02 / 0.91 | 0.67 (0.64/0.69) | 4b-fail(CAGR) | 2026-09-04_spy-tlt-gld-riskparity_C.py |
| 2026-09-04 | 19 RP L=252 g=1.00 | 8.8% | 0.95 | -23.0% | 1.02 / 0.91 | 0.67 (0.64/0.69) | 4b-fail(DD,CAGR) | 2026-09-04_spy-tlt-gld-riskparity_C.py |
| 2026-09-04 | 19 EW thirds (control) | 9.3% | 0.98 | -23.1% | 1.05 / 0.94 | 0.67 (0.64/0.69) | 4b-fail(DD,CAGR) | 2026-09-04_spy-tlt-gld-riskparity_C.py |
| 2026-09-04 | 19 60/40 SPY-TLT (control) | 10.3% | 1.00 | -27.7% | 1.40 / 0.73 | 0.67 (0.64/0.69) | 4b-fail(H2,OOS,DD,CAGR) | 2026-09-04_spy-tlt-gld-riskparity_C.py |
| 2026-09-04 | 16 u56/v1 none f=1.00 | 6.5% | 0.67 | -13.8% | 0.64 / 0.69 | 0.67 (0.64/0.69) | control 4b-fail | 2026-09-04_monthly-seasonality_cloud.py |
| 2026-09-04 | 16 u56/top20 none f=1.00 | 12.7% | 1.09 | -18.3% | 1.09 / 1.10 | 0.67 (0.64/0.69) | control 4b-PASS | 2026-09-04_monthly-seasonality_cloud.py |
| 2026-09-04 | 16 u56/EWall none f=1.00 | 10.4% | 1.05 | -15.9% | 1.07 / 1.04 | 0.67 (0.64/0.69) | control 4b-fail | 2026-09-04_monthly-seasonality_cloud.py |
| 2026-09-04 | 16 broad/v1 none f=1.00 | 6.4% | 0.64 | -21.2% | 0.76 / 0.54 | 0.64 (0.76/0.54) | control 4b-fail | 2026-09-04_monthly-seasonality_cloud.py |
| 2026-09-04 | 16 broad/top20 none f=1.00 | 13.1% | 0.96 | -20.1% | 1.12 / 0.81 | 0.64 (0.76/0.54) | control 4b-fail | 2026-09-04_monthly-seasonality_cloud.py |
| 2026-09-04 | 16 broad/EWall none f=1.00 | 10.7% | 1.03 | -17.7% | 1.15 / 0.92 | 0.64 (0.76/0.54) | control 4b-PASS | 2026-09-04_monthly-seasonality_cloud.py |
| 2026-09-04 | 16 u56/EWall sep f=0.50 | 10.2% | 1.06 | -15.9% | 1.06 / 1.06 | 0.67 (0.64/0.69) | KILL (best dSharpe +0.007) | 2026-09-04_monthly-seasonality_cloud.py |
| 2026-09-04 | 16 u56/EWall worst6 f=0.50 | 7.0% | 0.91 | -15.9% | 1.13 / 0.74 | 0.67 (0.64/0.69) | KILL (rule-8 IS pick; OOS 0.82 vs ctrl) | 2026-09-04_monthly-seasonality_cloud.py |
| 2026-09-04 | 16 u56/top20 sep f=0.75 | 12.5% | 1.10 | -18.3% | 1.09 / 1.11 | 0.67 (0.64/0.69) | KILL (best dSharpe +0.003) | 2026-09-04_monthly-seasonality_cloud.py |
| 2026-09-04 | 16 u56/top20 worst6 f=0.50 | 8.3% | 0.92 | -18.3% | 1.14 / 0.76 | 0.67 (0.64/0.69) | KILL (rule-8 IS pick; OOS 0.84 vs ctrl) | 2026-09-04_monthly-seasonality_cloud.py |
| 2026-09-04 | 16 u56/v1 sep f=0.00 | 6.5% | 0.69 | -13.8% | 0.57 / 0.80 | 0.67 (0.64/0.69) | KILL (best dSharpe +0.027) | 2026-09-04_monthly-seasonality_cloud.py |
| 2026-09-04 | 16 u56/v1 worst6 f=0.00 | 2.9% | 0.43 | -14.8% | 0.85 / 0.12 | 0.67 (0.64/0.69) | KILL (rule-8 IS pick; OOS 0.18 vs ctrl) | 2026-09-04_monthly-seasonality_cloud.py |
| 2026-09-04 | 16 broad/EWall sep f=0.50 | 10.6% | 1.04 | -17.7% | 1.13 / 0.95 | 0.64 (0.76/0.54) | KILL (best dSharpe +0.010) | 2026-09-04_monthly-seasonality_cloud.py |
| 2026-09-04 | 16 broad/EWall worst6 f=0.25 | 6.8% | 0.89 | -17.7% | 1.36 / 0.53 | 0.64 (0.76/0.54) | KILL (rule-8 IS pick; OOS 0.60 vs ctrl) | 2026-09-04_monthly-seasonality_cloud.py |
| 2026-09-04 | 16 broad/top20 sep f=0.75 | 12.9% | 0.96 | -20.1% | 1.11 / 0.83 | 0.64 (0.76/0.54) | KILL (best dSharpe +0.000) | 2026-09-04_monthly-seasonality_cloud.py |
| 2026-09-04 | 16 broad/top20 worst6 f=0.25 | 6.7% | 0.70 | -20.1% | 1.31 / 0.26 | 0.64 (0.76/0.54) | KILL (rule-8 IS pick; OOS 0.37 vs ctrl) | 2026-09-04_monthly-seasonality_cloud.py |
| 2026-09-04 | 16 broad/v1 sep f=0.00 | 6.9% | 0.70 | -17.9% | 0.70 / 0.71 | 0.64 (0.76/0.54) | KILL (best dSharpe +0.063) | 2026-09-04_monthly-seasonality_cloud.py |
| 2026-09-04 | 16 broad/v1 worst6 f=0.00 | 3.7% | 0.51 | -21.8% | 1.17 / -0.01 | 0.64 (0.76/0.54) | KILL (rule-8 IS pick; OOS 0.08 vs ctrl) | 2026-09-04_monthly-seasonality_cloud.py |
| 2026-09-04 | 16 u56/top20 sep f=0.00 | 12.1% | 1.08 | -18.3% | 1.06 / 1.11 | 0.67 (0.64/0.69) | 4b-pass both-univ but dSharpe<0 (hindsight mask) | 2026-09-04_monthly-seasonality_cloud.py |
| 2026-09-04 | 16 u56/top20 sep f=0.25 | 12.3% | 1.09 | -18.3% | 1.07 / 1.11 | 0.67 (0.64/0.69) | 4b-pass both-univ but dSharpe<0 (hindsight mask) | 2026-09-04_monthly-seasonality_cloud.py |
| 2026-09-04 | 16 broad/top20 sep f=0.00 | 12.3% | 0.94 | -20.1% | 1.04 / 0.85 | 0.64 (0.76/0.54) | 4b-pass both-univ but dSharpe<0 (hindsight mask) | 2026-09-04_monthly-seasonality_cloud.py |
| 2026-09-04 | 16 broad/top20 sep f=0.25 | 12.5% | 0.95 | -20.1% | 1.07 / 0.84 | 0.64 (0.76/0.54) | 4b-pass both-univ but dSharpe<0 (hindsight mask) | 2026-09-04_monthly-seasonality_cloud.py |
| 2026-09-04 | 87 u56/GROSS/EWall=0.8 | 11.1% | 1.05 | -16.9% | 1.07 / 1.04 | 0.67 (0.64/0.69) | 4b-pass both-universe | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 u56/BAND/ew-all=0.02 | 11.0% | 1.11 | -15.1% | 1.10 / 1.11 | 0.67 (0.64/0.69) | 4b-pass both-universe | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 u56/BAND/ew-all=0.03 | 11.3% | 1.14 | -15.1% | 1.11 / 1.16 | 0.67 (0.64/0.69) | 4b-pass both-universe | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 u56/BAND/ew-all=0.05 | 11.5% | 1.11 | -15.8% | 1.09 / 1.12 | 0.67 (0.64/0.69) | 4b-pass both-universe | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 u56/BAND/ew-all=0.08 | 11.9% | 1.13 | -17.1% | 1.18 / 1.09 | 0.67 (0.64/0.69) | 4b-pass both-universe | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 u56/CRYPTO/CAND20=0.05 | 13.5% | 1.15 | -18.2% | 1.18 / 1.13 | 0.67 (0.64/0.69) | 4b-pass both-universe | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 u56/CRYPTO/EWall=0.05 | 11.4% | 1.12 | -16.4% | 1.17 / 1.08 | 0.67 (0.64/0.69) | 4b-pass both-universe | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 u56/CRYPTO/EWall=0.1 | 12.3% | 1.15 | -18.7% | 1.26 / 1.07 | 0.67 (0.64/0.69) | 4b-pass both-universe | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 broad/GROSS/EWall=0.8 | 11.4% | 1.03 | -18.8% | 1.15 / 0.92 | 0.64 (0.76/0.54) | 4b-pass both-universe | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 broad/BAND/ew-all=0.02 | 11.1% | 1.06 | -17.1% | 1.17 / 0.96 | 0.64 (0.76/0.54) | 4b-pass both-universe | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 broad/BAND/ew-all=0.03 | 11.1% | 1.06 | -16.8% | 1.16 / 0.97 | 0.64 (0.76/0.54) | 4b-pass both-universe | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 broad/BAND/ew-all=0.05 | 11.1% | 1.04 | -17.5% | 1.13 / 0.96 | 0.64 (0.76/0.54) | 4b-pass both-universe | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 broad/BAND/ew-all=0.08 | 11.7% | 1.08 | -18.8% | 1.20 / 0.97 | 0.64 (0.76/0.54) | 4b-pass both-universe | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 broad/CRYPTO/CAND20=0.05 | 14.0% | 1.01 | -19.9% | 1.20 / 0.85 | 0.64 (0.76/0.54) | 4b-pass both-universe | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 broad/CRYPTO/EWall=0.05 | 11.7% | 1.10 | -18.2% | 1.24 / 0.97 | 0.64 (0.76/0.54) | 4b-pass both-universe | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 broad/CRYPTO/EWall=0.1 | 12.7% | 1.13 | -20.0% | 1.32 / 0.98 | 0.64 (0.76/0.54) | 4b-pass both-universe | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 u56/GROSS/top20=0.8 | 13.5% | 1.09 | -19.5% | 1.09 / 1.10 | 0.67 (0.64/0.69) | rule-8 R0 pick; OOS-4b PASS | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 u56/GROSS/top20=0.8 | 13.5% | 1.09 | -19.5% | 1.09 / 1.10 | 0.67 (0.64/0.69) | rule-8 Rm(m=0pp) pick; OOS-4b PASS | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 u56/GROSS/EWall=1 | 13.9% | 1.05 | -20.9% | 1.07 / 1.04 | 0.67 (0.64/0.69) | rule-8 R0 pick; OOS-4b fail | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 u56/BAND/ew-all=0.08 | 11.9% | 1.13 | -17.1% | 1.18 / 1.09 | 0.67 (0.64/0.69) | rule-8 R0 pick; OOS-4b PASS | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 u56/BAND/ew-all=0.08 | 11.9% | 1.13 | -17.1% | 1.18 / 1.09 | 0.67 (0.64/0.69) | rule-8 Rm(m=0pp) pick; OOS-4b PASS | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 u56/N/ranked=20 | 12.7% | 1.09 | -18.3% | 1.09 / 1.10 | 0.67 (0.64/0.69) | rule-8 R0 pick; OOS-4b PASS | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 u56/N/ranked=20 | 12.7% | 1.09 | -18.3% | 1.09 / 1.10 | 0.67 (0.64/0.69) | rule-8 Rm(m=0pp) pick; OOS-4b PASS | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 u56/CRYPTO/CAND20=0.15 | 15.1% | 1.18 | -23.3% | 1.31 / 1.09 | 0.67 (0.64/0.69) | rule-8 R0 pick; OOS-4b fail | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 u56/CRYPTO/CAND20=0.15 | 15.1% | 1.18 | -23.3% | 1.31 / 1.09 | 0.67 (0.64/0.69) | rule-8 Rm(m=0pp) pick; OOS-4b fail | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 u56/CRYPTO/EWall=0.15 | 13.2% | 1.15 | -22.6% | 1.32 / 1.03 | 0.67 (0.64/0.69) | rule-8 R0 pick; OOS-4b fail | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 u56/CRYPTO/EWall=0.15 | 13.2% | 1.15 | -22.6% | 1.32 / 1.03 | 0.67 (0.64/0.69) | rule-8 Rm(m=0pp) pick; OOS-4b fail | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 broad/GROSS/top20=1 | 17.4% | 0.96 | -26.2% | 1.13 / 0.82 | 0.64 (0.76/0.54) | rule-8 R0 pick; OOS-4b fail | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 broad/GROSS/top20=0.7 | 12.2% | 0.96 | -18.8% | 1.12 / 0.81 | 0.64 (0.76/0.54) | rule-8 Rm(m=0pp) pick; OOS-4b PASS | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 broad/GROSS/EWall=1 | 14.3% | 1.03 | -23.1% | 1.15 / 0.92 | 0.64 (0.76/0.54) | rule-8 R0 pick; OOS-4b fail | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 broad/GROSS/EWall=0.8 | 11.4% | 1.03 | -18.8% | 1.15 / 0.92 | 0.64 (0.76/0.54) | rule-8 Rm(m=0pp) pick; OOS-4b PASS | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 broad/BAND/ew-all=0.08 | 11.7% | 1.08 | -18.8% | 1.20 / 0.97 | 0.64 (0.76/0.54) | rule-8 R0 pick; OOS-4b PASS | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 broad/BAND/ew-all=0.08 | 11.7% | 1.08 | -18.8% | 1.20 / 0.97 | 0.64 (0.76/0.54) | rule-8 Rm(m=0pp) pick; OOS-4b PASS | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 broad/N/ranked=30 | 12.2% | 0.97 | -20.3% | 1.15 / 0.82 | 0.64 (0.76/0.54) | rule-8 R0 pick; OOS-4b fail | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 broad/N/ranked=30 | 12.2% | 0.97 | -20.3% | 1.15 / 0.82 | 0.64 (0.76/0.54) | rule-8 Rm(m=0pp) pick; OOS-4b fail | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 broad/CRYPTO/CAND20=0.15 | 15.6% | 1.07 | -29.2% | 1.31 / 0.86 | 0.64 (0.76/0.54) | rule-8 R0 pick; OOS-4b fail | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 broad/CRYPTO/EWall=0.15 | 13.6% | 1.14 | -22.9% | 1.38 / 0.95 | 0.64 (0.76/0.54) | rule-8 R0 pick; OOS-4b fail | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 87 broad/CRYPTO/EWall=0.15 | 13.6% | 1.14 | -22.9% | 1.38 / 0.95 | 0.64 (0.76/0.54) | rule-8 Rm(m=0pp) pick; OOS-4b fail | 2026-09-04_interior-4b-selection_cloud.py |
| 2026-09-04 | 86 u56 CAND20/hyst2 (idea 79) | 12.7% | 1.15 | -17.2% | 1.17 / 1.13 | 0.67 (0.64/0.69) | rule-8 pick; 4b KEEP-candidate (u56) | 2026-09-04_gross-matched-turnover-constraints_B.py |
| 2026-09-04 | 86 u56 CAND20/hyst2 gross-matched | 12.9% | 1.11 | -17.2% | 1.14 / 1.09 | 0.67 (0.64/0.69) | gm-invariant; 4b PASS | 2026-09-04_gross-matched-turnover-constraints_B.py |
| 2026-09-04 | 86 u56 CAND20/control (idea 2 KEEP) | 12.7% | 1.09 | -18.3% | 1.09 / 1.10 | 0.67 (0.64/0.69) | control; 4b PASS | 2026-09-04_gross-matched-turnover-constraints_B.py |
| 2026-09-04 | 86 u56 CAND20/control gross-matched | 12.8% | 1.06 | -18.3% | 1.07 / 1.07 | 0.67 (0.64/0.69) | idea 81 fix: -0.029 Sharpe; 4b PASS | 2026-09-04_gross-matched-turnover-constraints_B.py |
| 2026-09-04 | 86 u56 CAND20/budget-top0.1 | 15.3% | 1.11 | -22.9% | 1.14 / 1.10 | 0.67 (0.64/0.69) | rule-8 pick; 4b fail | 2026-09-04_gross-matched-turnover-constraints_B.py |
| 2026-09-04 | 86 u56 CAND20/budget-top0.1 gross-matched | 13.9% | 1.03 | -30.4% | 1.22 / 0.80 | 0.67 (0.64/0.69) | KILL: sign flip vs gmOFF | 2026-09-04_gross-matched-turnover-constraints_B.py |
| 2026-09-04 | 86 u56 EWall/budget-top0.2 | 11.0% | 1.04 | -19.2% | 1.05 / 1.05 | 0.67 (0.64/0.69) | 4b PASS (idea 83's positive) | 2026-09-04_gross-matched-turnover-constraints_B.py |
| 2026-09-04 | 86 u56 EWall/budget-top0.2 gross-matched | 0.9% | 0.18 | -27.8% | 0.20 / 0.17 | 0.67 (0.64/0.69) | KILL: 4b PASS -> fail once gross-matched | 2026-09-04_gross-matched-turnover-constraints_B.py |
| 2026-09-04 | 86 u56 CAND20/monthly gross-matched | 15.3% | 1.21 | -19.5% | 1.20 / 1.23 | 0.67 (0.64/0.69) | idea 3 survives; 4b PASS, MaxDD-bought | 2026-09-04_gross-matched-turnover-constraints_B.py |
| 2026-09-04 | 86 broad CAND20/hyst2 (idea 79) | 14.4% | 1.03 | -20.4% | 1.26 / 0.83 | 0.64 (0.76/0.54) | rule-8 pick; 4b fail (H2,DD) | 2026-09-04_gross-matched-turnover-constraints_B.py |
| 2026-09-04 | 86 broad CAND20/hyst2 gross-matched | 14.3% | 1.01 | -20.4% | 1.24 / 0.82 | 0.64 (0.76/0.54) | gm-invariant; 4b fail (H2,DD) | 2026-09-04_gross-matched-turnover-constraints_B.py |
| 2026-09-04 | 86 broad CAND20/budget-top0.1 | 19.2% | 1.10 | -31.8% | 1.28 / 0.97 | 0.64 (0.76/0.54) | rule-8 pick gmOFF; 4b fail | 2026-09-04_gross-matched-turnover-constraints_B.py |
| 2026-09-04 | 86 broad CAND20/budget-top0.1 gross-matched | 11.9% | 0.81 | -18.1% | 0.89 / 0.73 | 0.64 (0.76/0.54) | KILL: gm demotes pick to control | 2026-09-04_gross-matched-turnover-constraints_B.py |
| 2026-09-04 | 86 broad EWall/control gross-matched | 10.7% | 1.03 | -17.7% | 1.15 / 0.92 | 0.64 (0.76/0.54) | gm-invariant; 4b PASS | 2026-09-04_gross-matched-turnover-constraints_B.py |
| 2026-09-04 | 89 u56 N/ranked n=20 (S16 rule-8 pick) | 12.7% | 1.09 | -18.3% | 1.09 / 1.10 | 0.67 (0.64/0.69) | split-dependent pick; 4b PASS | 2026-09-04_is-window-has-no-crash_C.py |
| 2026-09-04 | 89 u56 N/ranked n=40 (S13+S21 rule-8 pick) | 9.7% | 1.13 | -14.0% | 1.07 / 1.17 | 0.67 (0.64/0.69) | 4b fail (CAGR); 2022+ Sh 1.099 vs 1.100 | 2026-09-04_is-window-has-no-crash_C.py |
| 2026-09-04 | 89 u56 BAND/ew-all b=0.08 (S16/S21 pick) | 11.9% | 1.13 | -17.1% | 1.18 / 1.09 | 0.67 (0.64/0.69) | 4b PASS; S13 picks b=0.02 (-0.034 2022+ Sh) | 2026-09-04_is-window-has-no-crash_C.py |
| 2026-09-04 | 89 broad N/ranked n=30 (S16 pick) | 12.2% | 0.97 | -20.3% | 1.15 / 0.82 | 0.64 (0.76/0.54) | 4b fail (H2,DD); S13->20, S21->40 | 2026-09-04_is-window-has-no-crash_C.py |
| 2026-09-04 | 89 rule-8 split test (S13/S16/S21) | n/a | n/a | n/a | n/a | n/a | KILL: 8/12 + 5/12 picks move, <=0.034 Sharpe; DD cap looser with crash IS | 2026-09-04_is-window-has-no-crash_C.py |
| 2026-09-04 | 88 8a selectability pre-test (22 cells, 122 arms) | n/a | n/a | n/a | n/a | n/a | KILL as worded: flags 4/22 cells (all gross), regret -0.001 there vs -0.061 elsewhere | 2026-09-04_selectability-pre-test_cloud.py |
| 2026-09-04 | 88 u56 F/fraction f=0.15 (rule-8 pick, 8a PASS) | 16.8% | 0.98 | -27.8% | 1.05 / 0.93 | 0.67 (0.64/0.69) | worst selection in run (regret -0.232); 4b fail (DD) | 2026-09-04_selectability-pre-test_cloud.py |
| 2026-09-04 | 88 broad F/fraction f=0.15 (rule-8 pick, 8a PASS) | 13.1% | 0.85 | -29.9% | 1.11 / 0.63 | 0.64 (0.76/0.54) | regret -0.310; 4b fail (H2,OOS,DD) | 2026-09-04_selectability-pre-test_cloud.py |
| 2026-09-04 | 88 u56 GROSS/top20 g=0.80 (rule-8 pick, 8a FAIL) | 13.5% | 1.09 | -19.5% | 1.09 / 1.10 | 0.67 (0.64/0.69) | 4b PASS; IS Sharpe spread 0.0002, OOS MaxDD spread 11.6pp | 2026-09-04_selectability-pre-test_cloud.py |
| 2026-09-04 | 88 u56 CADENCE/top20 freq=M (rule-8 pick) | 14.7% | 1.20 | -19.5% | 1.21 / 1.21 | 0.67 (0.64/0.69) | 4b PASS full+OOS; same rule on broad fails 4b (DD -26.1%) | 2026-09-04_selectability-pre-test_cloud.py |
| 2026-09-04 | 88 u56 HYST/top20 k=2.00 (rule-8 pick) | 12.7% | 1.15 | -17.2% | 1.17 / 1.13 | 0.67 (0.64/0.69) | 4b PASS, 3.9x turnover; reproduces idea 86 | 2026-09-04_selectability-pre-test_cloud.py |
| 2026-09-04 | 85 exit-leg attribution (4 books) | n/a | n/a | n/a | n/a | n/a | mechanism HALF REFUTED: gate 25%/11% of exits on ranked, 57% on unranked | 2026-09-04_exit-schedule-vs-entry-schedule_cloud.py |
| 2026-09-04 | 85 u56 EWall entry-budget B=0.10 | 10.0% | 1.10 | -12.9% | 1.07 / 1.13 | 0.67 (0.64/0.69) | PARK: -0.14 pp/pp vs lever -0.68; 4b fail (CAGR) | 2026-09-04_exit-schedule-vs-entry-schedule_cloud.py |
| 2026-09-04 | 85 broad EWall entry-budget B=0.20 | 10.9% | 1.08 | -16.4% | 1.17 / 0.99 | 0.64 (0.76/0.54) | PARK: 4b PASS full+OOS (control fails OOS CAGR) | 2026-09-04_exit-schedule-vs-entry-schedule_cloud.py |
| 2026-09-04 | 85 broad CAND20 entry-budget B=0.10 | 11.2% | 0.94 | -18.2% | 1.18 / 0.73 | 0.64 (0.76/0.54) | KILL on the ranked book: dSharpe -0.016, t -3.15 | 2026-09-04_exit-schedule-vs-entry-schedule_cloud.py |
| 2026-09-04 | 85 u56 CAND20 total-budget B=0.05 (idea 83 control) | 14.3% | 1.13 | -22.8% | 1.18 / 1.10 | 0.67 (0.64/0.69) | reproduces idea 83: MaxDD worse in 19/20 arms | 2026-09-04_exit-schedule-vs-entry-schedule_cloud.py |
| 2026-09-04 | 84 binding-bar census (8 cells, 480 pts) | n/a | n/a | n/a | n/a | n/a | KILL 2-branch rule: CAGR binds 6/8; Sharpe bars g-invariant (spread 0.006) | 2026-09-04_which-4b-bar-binds_B.py |
| 2026-09-04 | 84 u56 C57/ew-band3 g=0.85 (KEEP-cand) | 12.8% | 1.14 | -17.1% | 1.11 / 1.16 | 0.67 (0.64/0.69) | 4b PASS full+OOS at 5/10/25 bps | 2026-09-04_which-4b-bar-binds_B.py |
| 2026-09-04 | 84 broad C57/ew-band3 g=0.85 (KEEP-cand) | 12.6% | 1.06 | -18.9% | 1.16 / 0.97 | 0.64 (0.76/0.54) | 4b PASS full+OOS at 5/10/25 bps; 4a PASS | 2026-09-04_which-4b-bar-binds_B.py |
| 2026-09-04 | 84 u56 C57/ew-band3 g=0.85 @ 25 bps | 11.9% | 1.06 | -17.2% | 1.04 / 1.09 | 0.67 (0.64/0.69) | answers idea 58: g=0.75 dies here on CAGR | 2026-09-04_which-4b-bar-binds_B.py |
| 2026-09-04 | 84 broad C57/ew-band3 g=0.85 @ 25 bps | 11.6% | 0.99 | -19.1% | 1.09 / 0.89 | 0.64 (0.76/0.54) | 4b PASS both universes at 25 bps (6/80 arms) | 2026-09-04_which-4b-bar-binds_B.py |
| 2026-09-04 | 84 u56 C72/EWall g=0.85 | 11.8% | 1.05 | -17.9% | 1.07 / 1.04 | 0.67 (0.64/0.69) | gross fixes idea 72's 0.26pp CAGR miss; dies at 25 bps | 2026-09-04_which-4b-bar-binds_B.py |
| 2026-09-04 | 84 broad C2/CAND20 g=0.75 (control) | 13.1% | 0.96 | -20.1% | 1.13 / 0.81 | 0.64 (0.76/0.54) | H2-bound: 0/20 lever arms convert (best +0.003) | 2026-09-04_which-4b-bar-binds_B.py |
| 2026-09-04 | 84 broad C72/EWall entry-budget B=0.20 | 10.9% | 1.08 | -16.4% | 1.17 / 0.99 | 0.64 (0.76/0.54) | budget is a Sharpe lever (+0.050), CAGR-neutral (+0.02pp) | 2026-09-04_which-4b-bar-binds_B.py |
| 2026-09-04 | 84 walk-forward RBIND vs R0 vs control | n/a | n/a | n/a | n/a | n/a | mean OOS Sharpe 1.098 / 1.097 / 1.083: rule has no net content | 2026-09-04_which-4b-bar-binds_B.py |
| 2026-09-04 | 22 u56 V1 + DD-control 8%/halve/new-high (literal) | 3.7% | 0.49 | -12.1% | 0.41 / 0.55 | 0.67 (0.64/0.69) | KILL: dSharpe -0.182, 52% of days cut | 2026-09-04_drawdown-control_C.py |
| 2026-09-04 | 22 u56 CAND20 + DD-control 8%/halve/new-high | 8.4% | 0.92 | -14.2% | 0.90 / 0.93 | 0.67 (0.64/0.69) | KILL: dSharpe -0.176, breaks idea 2's 4b pass on CAGR | 2026-09-04_drawdown-control_C.py |
| 2026-09-04 | 22 u56 EWall + DD-control 8%/halve/new-high | 6.7% | 0.83 | -12.5% | 0.82 / 0.84 | 0.67 (0.64/0.69) | KILL: dSharpe -0.217, -3.8pp CAGR for +3.4pp DD | 2026-09-04_drawdown-control_C.py |
| 2026-09-04 | 22 broad V1 + DD-control 8%/halve/new-high | 3.2% | 0.44 | -15.3% | 0.58 / 0.30 | 0.64 (0.76/0.54) | KILL: dSharpe -0.200, 65% of days cut | 2026-09-04_drawdown-control_C.py |
| 2026-09-04 | 22 broad CAND20 + DD-control 8%/halve/new-high | 7.5% | 0.75 | -15.3% | 0.90 / 0.61 | 0.64 (0.76/0.54) | KILL: dSharpe -0.209, -5.6pp CAGR | 2026-09-04_drawdown-control_C.py |
| 2026-09-04 | 22 broad EWall + DD-control 8%/halve/new-high | 7.2% | 0.88 | -14.3% | 1.03 / 0.72 | 0.64 (0.76/0.54) | KILL: dSharpe -0.146, kills idea 72's only 4b pass | 2026-09-04_drawdown-control_C.py |
| 2026-09-04 | 22 u56 CAND20 D=4%/k=0.00 (absorbing state) | -0.1% | -0.05 | -5.8% | -0.07 / n/a | 0.67 (0.64/0.69) | KILL: exits 2011 and never returns, 97.3% of days in cash | 2026-09-04_drawdown-control_C.py |
| 2026-09-04 | 22 u56 CAND20 D=12%/k=0.75 (best treated arm) | 12.0% | 1.06 | -18.3% | 1.09 / 1.05 | 0.67 (0.64/0.69) | 4b PASS but strictly worse than its own control (1.093) | 2026-09-04_drawdown-control_C.py |
| 2026-09-04 | 22 exchange rate: DD rule vs static gross (288 arms) | n/a | n/a | n/a | n/a | n/a | KILL: 1.02 vs 0.57 pp CAGR per pp MaxDD; dominated 252/288 | 2026-09-04_drawdown-control_C.py |
| 2026-09-04 | 22 walk-forward S1/S2 vs control (12 cells) | n/a | n/a | n/a | n/a | n/a | S1 picks the do-nothing corner 12/12 (OOS 0.900 vs 0.922); S2 picks nothing 10/12 | 2026-09-04_drawdown-control_C.py |

### Idea 21 — momentum-plus-quality-proxy (cloud, 2026-09-04)

Top-K by 12-1 momentum among RULES v1's eligible set (200d MA + `vol20 < 0.60`), then drop
`D = round(d·K)` names by `vol20`; equal weight, 0.75 gross, weekly, next-day execution.
Two tuned parameters: `K ∈ {10,20,30}`, `d ∈ {0,0.1,0.2,0.3,0.5}`. Three arms — **HI** (drop
highest-vol = the idea), **LO** (drop lowest-vol = sign check), **CTRL** (no screen, rank-cap
at K−D = the matched-size control). Both gross conventions (MATCHED `g/count`, LITERAL `g/K`)
and 10/25 bps. **312 grid points, all reported** in
`2026-09-04_momentum-plus-quality-proxy_cloud.grid.csv`; representative rows below.
**KILL** — HI beats CTRL on Sharpe in 1/24 cells (means −0.127 broad / −0.156 u56), beats the
reversed screen LO in 2/24, is monotone-decreasing in `d` on both universes and both rankers,
and **rule 8 selects `d = 0` (no screen) on BOTH universes**. Confirms ideas 1 and 80/81: the
short-horizon vol premium inside this gate is positive-signed, so a low-vol tilt is backwards.
By-product: the LITERAL `g/K` denominator de-grosses 0.750 → 0.522 at K=10/d=0.3 and inflates
4a passes 18/39 → 30/39 on broad at unchanged Sharpe — idea 73's artefact, reproduced.
See `2026-09-04_momentum-plus-quality-proxy_cloud.result.md`.

| 2026-09-04 | 21 BROAD HI K=10 d=0.0 (anchor, no screen) | 18.7% | 1.08 | -21.4% | 1.28 / 0.92 | 0.64 (0.76/0.54) | KILL 4b (DD) | 2026-09-04_momentum-plus-quality-proxy_cloud.py |
| 2026-09-04 | 21 BROAD HI K=10 d=0.3 (**the queue's literal proposal**) | 14.8% | 0.93 | -19.2% | 1.13 / 0.77 | 0.64 (0.76/0.54) | KEEP 4a / KILL 4b (H2,OOS) | 2026-09-04_momentum-plus-quality-proxy_cloud.py |
| 2026-09-04 | 21 BROAD LO K=10 d=0.3 (sign check — beats the idea) | 21.1% | 1.07 | -25.5% | 1.39 / 0.82 | 0.64 (0.76/0.54) | KILL 4a / KILL 4b (H2,DD) | 2026-09-04_momentum-plus-quality-proxy_cloud.py |
| 2026-09-04 | 21 BROAD CTRL K=10 d=0.3 (matched-size control) | 18.6% | 0.99 | -23.2% | 1.26 / 0.79 | 0.64 (0.76/0.54) | KILL 4a / KILL 4b (H2,OOS,DD) | 2026-09-04_momentum-plus-quality-proxy_cloud.py |
| 2026-09-04 | 21 BROAD HI K=20 d=0.3 | 10.3% | 0.80 | -19.9% | 1.02 / 0.62 | 0.64 (0.76/0.54) | KILL 4a / KILL 4b | 2026-09-04_momentum-plus-quality-proxy_cloud.py |
| 2026-09-04 | 21 BROAD HI K=30 d=0.3 | 9.9% | 0.86 | -19.4% | 1.06 / 0.68 | 0.64 (0.76/0.54) | KILL 4a / KILL 4b | 2026-09-04_momentum-plus-quality-proxy_cloud.py |
| 2026-09-04 | 21 U56 HI K=10 d=0.0 (anchor) | 15.4% | 1.04 | -20.6% | 1.03 / 1.07 | 0.67 (0.64/0.69) | KILL 4b (DD) | 2026-09-04_momentum-plus-quality-proxy_cloud.py |
| 2026-09-04 | 21 U56 HI K=10 d=0.3 (literal proposal) | 11.1% | 0.86 | -20.8% | 0.84 / 0.89 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,DD) | 2026-09-04_momentum-plus-quality-proxy_cloud.py |
| 2026-09-04 | 21 U56 CTRL K=10 d=0.3 (matched-size control) | 17.0% | 1.03 | -21.5% | 0.95 / 1.10 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,DD) | 2026-09-04_momentum-plus-quality-proxy_cloud.py |
| 2026-09-04 | 21 U56 HI K=20 d=0.3 | 8.3% | 0.84 | -17.6% | 0.97 / 0.74 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,H2,OOS,CAGR) | 2026-09-04_momentum-plus-quality-proxy_cloud.py |
| 2026-09-04 | 21 rule-8 OOS pick BROAD (K=10, d=0 — the screen switched OFF) | 18.3% | 1.00 | -21.4% | OOS-only | v1 OOS 0.58, SPY OOS 0.88 | walk-forward selects no screen | 2026-09-04_momentum-plus-quality-proxy_cloud.py |
| 2026-09-04 | 21 rule-8 OOS pick U56 (K=20, d=0 — the screen switched OFF) | 12.9% | 1.02 | -18.8% | OOS-only | v1 OOS 0.75, SPY OOS 0.88 | walk-forward selects no screen | 2026-09-04_momentum-plus-quality-proxy_cloud.py |
| 2026-09-04 | 94 THE MENU: 16 drawdown instruments, 1 harness, 12 cells | n/a | n/a | n/a | n/a | n/a | PARK: tiers stable, per-instrument price is NOT (median Spearman IS/OOS 0.44, S1 rank-1 in 5/12) | 2026-09-04_drawdown-insurance-price-list_B.py |
| 2026-09-04 | 94 price at 10bps: gates 0.18-0.51 < static gross 0.57 < book-DD 0.60-0.69 < stop (unpriceable) | n/a | n/a | n/a | n/a | n/a | FINDING: 48/68 arm-cells BEAT the gross lever; idea 22's domination is DD-control-specific | 2026-09-04_drawdown-insurance-price-list_B.py |
| 2026-09-04 | 94 u56 EWall + vol60-dg (vol20<0.60 to cash, NO trend filter) | 11.6% | 1.13 | -16.9% | 1.16 / 1.11 | 0.66 (0.64/0.69) | 4b KEEP-candidate: OOS 1.186 vs SPY 0.882, 1.39x turnover | 2026-09-04_drawdown-insurance-price-list_B.py |
| 2026-09-04 | 94 broad EWall + vol60-dg | 12.4% | 1.14 | -18.7% | 1.26 / 1.03 | 0.64 (0.76/0.54) | 4b KEEP-candidate: passes at 10 AND 25 bps on BOTH universes, 1.36x turnover | 2026-09-04_drawdown-insurance-price-list_B.py |
| 2026-09-04 | 94 u56 EWall + band3-rw (= idea 57 ew-band3) | 12.2% | 1.16 | -17.7% | 1.21 / 1.13 | 0.66 (0.64/0.69) | 4b PASS: independent replication of idea 57, holds at 25 bps | 2026-09-04_drawdown-insurance-price-list_B.py |
| 2026-09-04 | 94 broad EWall + band3-rw | 11.7% | 1.07 | -18.5% | 1.17 / 0.98 | 0.64 (0.76/0.54) | 4b PASS: cross-universe, 10 and 25 bps | 2026-09-04_drawdown-insurance-price-list_B.py |
| 2026-09-04 | 94 u56 EWall + band3-dg (200d +/-3pct band, to cash) | 8.7% | 1.21 | -12.1% | 1.23 / 1.19 | 0.66 (0.64/0.69) | 4a KEEP-candidate: dominates live v1 on CAGR, Sharpe AND MaxDD; fails 4b CAGR floor | 2026-09-04_drawdown-insurance-price-list_B.py |
| 2026-09-04 | 94 broad EWall + band3-dg | 8.0% | 1.11 | -12.2% | 1.23 / 0.98 | 0.64 (0.76/0.54) | 4a PASS in all 4 cells (with g200-dg, v1gate-dg); the run's only 4a passes | 2026-09-04_drawdown-insurance-price-list_B.py |
| 2026-09-04 | 94 per-name trailing stop 15/25pct on 3 books x 2 universes | n/a | n/a | n/a | n/a | n/a | KILL: buys NEGATIVE MaxDD in 10/12 cells and zero in 2; unpriceable at any rate | 2026-09-04_drawdown-insurance-price-list_B.py |
| 2026-09-04 | 94 entry-only turnover budget B=0.10/0.20 | n/a | n/a | n/a | n/a | n/a | KILL: exactly 0.000 effect on EWall (never binds); on V1u it is de-grossing to 69pct gross | 2026-09-04_drawdown-insurance-price-list_B.py |
| 2026-09-04 | 94 abs momentum (px > px 252d ago) as insurance | n/a | n/a | n/a | n/a | n/a | KILL: dearest real gate (0.61/0.66) and buys the least DD (0.59-1.14pp median) | 2026-09-04_drawdown-insurance-price-list_B.py |
| 2026-09-04 | 94 gate convention -rw (reweight) vs -dg (de-gross), 6 cells | n/a | n/a | n/a | n/a | n/a | FINDING: -rw buys 2.69pp DD vs -dg 3.50pp at ~half the CAGR cost; the gate is SELECTION, not de-grossing | 2026-09-04_drawdown-insurance-price-list_B.py |
| 2026-09-04 | 26 u56 v1top5 + 50pct sleeve (the idea as worded, natural) | 5.8% | 0.79 | -11.9% | 0.73 / 0.85 | 0.66 (0.64/0.69) | 4a PASS / 4b FAIL (H1 0.725 vs SPY 0.957; CAGR 5.8pct vs 10.66pct floor) | 2026-09-04_ensemble-plus-momentum_C.py |
| 2026-09-04 | 26 u56 v1top5 + 50pct sleeve (gross-matched) | 6.3% | 0.80 | -12.0% | 0.76 / 0.85 | 0.66 (0.64/0.69) | 4a PASS / 4b FAIL (same two bars) | 2026-09-04_ensemble-plus-momentum_C.py |
| 2026-09-04 | 26 broad v1top5 + 50pct sleeve (natural) | 5.8% | 0.79 | -12.1% | 0.81 / 0.76 | 0.64 (0.76/0.53) | 4a PASS / 4b FAIL | 2026-09-04_ensemble-plus-momentum_C.py |
| 2026-09-04 | 26 broad v1top5 + 50pct sleeve (gross-matched) | 6.1% | 0.78 | -14.9% | 0.86 / 0.71 | 0.64 (0.76/0.53) | 4a PASS / 4b FAIL | 2026-09-04_ensemble-plus-momentum_C.py |
| 2026-09-04 | 26 u56 top20 + 25pct sleeve (natural) | 10.8% | 1.09 | -16.0% | 1.06 / 1.11 | 0.66 (0.64/0.69) | 4b PASS but rule-8 unselectable (IS Sharpe monotone falling in f) | 2026-09-04_ensemble-plus-momentum_C.py |
| 2026-09-04 | 26 broad top20 + 25pct sleeve (natural) | 11.1% | 0.97 | -17.3% | 1.11 / 0.85 | 0.64 (0.76/0.53) | 4b PASS: repairs idea 2's broad H2 failure (0.811 -> 0.854 vs SPY 0.834); PARK | 2026-09-04_ensemble-plus-momentum_C.py |
| 2026-09-04 | 26 broad top20 + 25pct sleeve (gross-matched) | 11.5% | 0.97 | -17.7% | 1.12 / 0.84 | 0.64 (0.76/0.53) | 4b PASS; only (book,f) passing 4b on BOTH universes and BOTH conventions | 2026-09-04_ensemble-plus-momentum_C.py |
| 2026-09-04 | 26 sleeve standalone f=1.00 (idea 18 variant B, replicated) | 5.0% | 0.87 | -10.1% | 0.76 / 0.98 | 0.66 (0.64/0.69) | control: reproduces idea 18's row; 4b FAIL on CAGR by 5.7pp | 2026-09-04_ensemble-plus-momentum_C.py |
| 2026-09-04 | 26 diversification test: dSharpe vs linear blend, 36 interior cells | n/a | n/a | n/a | n/a | n/a | MECHANISM CONFIRMED: dSharpe > 0 in 36/36, mean +0.052, range +0.008..+0.085 | 2026-09-04_ensemble-plus-momentum_C.py |
| 2026-09-04 | 26 year attribution of the 25pct sleeve on top20 | n/a | n/a | n/a | n/a | n/a | KILLS the by-product as a rule: sleeve effect NEGATIVE in 17/18 years, only 2022 positive (+1.6/+2.2pp) | 2026-09-04_ensemble-plus-momentum_C.py |
| 2026-09-04 | 26 cost ladder 5/10/15/20/25 bps on top20 f=0 vs f=0.25 | n/a | n/a | n/a | n/a | n/a | cross-universe 4b window 5-10 bps (f=0.25) vs 5 bps (f=0); both dead at 15 | 2026-09-04_ensemble-plus-momentum_C.py |
| 2026-09-04 | 26 sleeve-to-book daily return correlation | n/a | n/a | n/a | n/a | n/a | 0.63-0.82 (u56) / 0.63-0.75 (broad): the sleeve is not an uncorrelated asset | 2026-09-04_ensemble-plus-momentum_C.py |
### Idea 92 — sharpe-bound-books-need-a-book-change (cloud, 2026-09-04)

Test cell inherited from ideas 46/84: `C2/CAND20` on `universe_broad.json` — the project's only
**Sharpe-bound** 4b cell (H2 0.814 vs SPY 0.837, fails on H2 alone). Idea 84 showed no exposure
or turnover lever moves it (best +0.0027 over 20 arms). This run tests the four BOOK changes the
queue named. Four families, one dial each: SECTOR cap {1.00,0.40,0.25,0.15} (price-only annual
sector labels from prior-756d correlation to the 11 SPDRs, look-ahead-free, 11% YoY churn);
WCAP per-name cap {0.0375,0.05,0.075,0.10} on the equal-weight book AND on a 1/rank-weighted
book; NORANK {CAND n=20/40/60, EWall, ew-band3}; GATE {both, none, 200d, vol20, band3, abs}.
**96 grid points, all reported** in `2026-09-04_sharpe-bound-book-change_cloud.grid.csv`.
Harness verified: `SECTOR cap=1.00` ≡ `CAND n=20` to 6dp; `WCAP-RANKW @0.75/20` collapses onto
CAND20 weight-for-weight (max|diff| 2.4e-16 off tie days); the u56 test cell reproduces idea 2's
KEEP row exactly. **Answer: only dropping the ranking is a dial** (ΔH2 +0.158, 4/4 arms convert
the cell; +0.225 at 25 bps). NOT dials: per-name weight cap **exactly inert** on an equal-weight
book (ΔH2 +0.000 at every level, bind rate 0) and ceilinged at the equal-weight book on a
concentrated one; sector cap moves H2 **down** (−0.105 at 15%) with the run's worst walk-forward
regret (−0.187); the eligibility gate tops out at +0.042, below idea 84's own 0.05 threshold —
refuting the pre-registered prediction that the gate carries H2. Rule 8 picks `ew-band3`, which
is also its family's best OOS arm (regret 0.000, the only family where those coincide).
See `..._cloud.result.md` and memo `..._cloud.memo.md`.

| 2026-09-04 | 92 BROAD CAND20 (the Sharpe-bound test cell, control) | 13.1% | 0.96 | -20.1% | 1.13 / 0.81 | 0.64 (0.76/0.54) | KEEP 4a / KILL 4b (H2 by 0.023) | 2026-09-04_sharpe-bound-book-change_cloud.py |
| 2026-09-04 | 92 BROAD SECTOR cap=0.40 | 13.0% | 0.97 | -19.2% | 1.11 / 0.84 | 0.64 (0.76/0.54) | KEEP 4a / KEEP 4b (margin +0.002; dies at 25 bps, not the rule-8 pick) | 2026-09-04_sharpe-bound-book-change_cloud.py |
| 2026-09-04 | 92 BROAD SECTOR cap=0.25 | 11.6% | 0.90 | -18.9% | 1.05 / 0.76 | 0.64 (0.76/0.54) | KEEP 4a / KILL 4b (H2,OOS) | 2026-09-04_sharpe-bound-book-change_cloud.py |
| 2026-09-04 | 92 BROAD SECTOR cap=0.15 | 9.9% | 0.88 | -21.4% | 1.08 / 0.71 | 0.64 (0.76/0.54) | KILL 4a / KILL 4b (H2,OOS,DD,CAGR) — rule-8 pick, regret -0.187 | 2026-09-04_sharpe-bound-book-change_cloud.py |
| 2026-09-04 | 92 BROAD WCAP-EW wmax=0.05/0.075/0.10 (all three) | 13.1% | 0.96 | -20.1% | 1.13 / 0.81 | 0.64 (0.76/0.54) | KILL — measured INERT, identical to control to machine precision | 2026-09-04_sharpe-bound-book-change_cloud.py |
| 2026-09-04 | 92 BROAD WCAP-RANKW uncapped (1/rank weights) | 15.5% | 0.89 | -25.3% | 1.01 / 0.78 | 0.64 (0.76/0.54) | KILL 4a / KILL 4b (H2,OOS,DD) | 2026-09-04_sharpe-bound-book-change_cloud.py |
| 2026-09-04 | 92 BROAD NORANK CAND n=40 | 11.9% | 1.00 | -19.1% | 1.13 / 0.89 | 0.64 (0.76/0.54) | KEEP 4a / KEEP 4b | 2026-09-04_sharpe-bound-book-change_cloud.py |
| 2026-09-04 | 92 BROAD NORANK CAND n=60 | 10.9% | 1.01 | -19.0% | 1.11 / 0.93 | 0.64 (0.76/0.54) | KEEP 4a / KEEP 4b | 2026-09-04_sharpe-bound-book-change_cloud.py |
| 2026-09-04 | 92 BROAD NORANK EWall (no ranking) | 10.7% | 1.03 | -17.7% | 1.15 / 0.92 | 0.64 (0.76/0.54) | KEEP 4a / KEEP 4b | 2026-09-04_sharpe-bound-book-change_cloud.py |
| 2026-09-04 | 92 BROAD NORANK ew-band3 (no ranking) — **the dial, rule-8 pick, regret 0.000** | 11.1% | 1.06 | -16.8% | 1.16 / 0.97 | 0.64 (0.76/0.54) | KEEP 4a / KEEP 4b | 2026-09-04_sharpe-bound-book-change_cloud.py |
| 2026-09-04 | 92 BROAD GATE none | 14.7% | 0.98 | -26.0% | 1.14 / 0.86 | 0.64 (0.76/0.54) | KILL 4a / KILL 4b (DD) | 2026-09-04_sharpe-bound-book-change_cloud.py |
| 2026-09-04 | 92 BROAD GATE 200d only | 14.7% | 0.99 | -24.0% | 1.19 / 0.84 | 0.64 (0.76/0.54) | KILL 4a / KILL 4b (DD) | 2026-09-04_sharpe-bound-book-change_cloud.py |
| 2026-09-04 | 92 BROAD GATE vol20 only | 12.8% | 0.93 | -20.7% | 1.08 / 0.80 | 0.64 (0.76/0.54) | KEEP 4a / KILL 4b (H2,OOS,DD) | 2026-09-04_sharpe-bound-book-change_cloud.py |
| 2026-09-04 | 92 BROAD GATE band3 | 13.0% | 0.95 | -20.1% | 1.10 / 0.82 | 0.64 (0.76/0.54) | KEEP 4a / KILL 4b (H2) | 2026-09-04_sharpe-bound-book-change_cloud.py |
| 2026-09-04 | 92 BROAD GATE abs (200d & mom>0) | 12.9% | 0.96 | -20.1% | 1.12 / 0.84 | 0.64 (0.76/0.54) | KEEP 4a / KEEP 4b (H2 margin +0.000; dies at 25 bps) | 2026-09-04_sharpe-bound-book-change_cloud.py |
| 2026-09-04 | 92 U56 CAND20 (control universe — reproduces idea 2's KEEP row) | 12.7% | 1.09 | -18.3% | 1.09 / 1.10 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b | 2026-09-04_sharpe-bound-book-change_cloud.py |
| 2026-09-04 | 92 U56 NORANK ew-band3 | 11.3% | 1.14 | -15.1% | 1.11 / 1.16 | 0.67 (0.64/0.69) | KILL 4a / KEEP 4b — rule-8 pick, OOS 1.234 | 2026-09-04_sharpe-bound-book-change_cloud.py |
| 2026-09-04 | 92 U56 NORANK EWall | 10.4% | 1.05 | -15.9% | 1.07 / 1.04 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (CAGR) | 2026-09-04_sharpe-bound-book-change_cloud.py |
| 2026-09-04 | 92 U56 SECTOR cap=0.15 | 10.3% | 1.01 | -17.4% | 0.91 / 1.11 | 0.67 (0.64/0.69) | KILL 4a / KILL 4b (H1,CAGR) | 2026-09-04_sharpe-bound-book-change_cloud.py |
| 2026-09-04 | 92 U56 WCAP-EW (all levels) | 12.7% | 1.09 | -18.3% | 1.09 / 1.10 | 0.67 (0.64/0.69) | KILL — measured INERT, identical to control | 2026-09-04_sharpe-bound-book-change_cloud.py |

### Idea 23 — earnings-season-avoidance (cloud, 2026-09-04) — KILL

372 points (2 universes x 3 books x 2 exclusion conventions x [1 anchor + 15 season windows +
15 placebo windows]), all reported; 2 tuned params (start, length); anchor reproduces
`rules_v1_weights` exactly. Blacking single stocks out of the eligible set for a fixed
post-quarter-end window loses Sharpe in **179 of 180 season cells** (mean -0.129, dCAGR -2.19%/yr)
and the best window per cell still loses in 11 of 12. The premise fails first: in-season SPY-excess
return is +0.81 bps/day (u56) / +0.05 (broad) with max |t| 2.39 / 1.42, below the placebo's own
3.10 / 2.16. Rule 8 picks a blackout window in 10/12 cells on higher IS Sharpe (+0.100 mean) and
loses -0.106..-0.420 OOS. Priced as drawdown insurance: 2.88 pp CAGR per pp MaxDD, vs idea 94's
dearest priceable instrument at 0.91 and the gross lever at 0.57.

| Date | Idea / variant | CAGR | Sharpe | MaxDD | H1 / H2 | Baseline Sharpe | Verdict | Script |
|---|---|---|---|---|---|---|---|---|
| 2026-09-04 | 23 PREMISE u56: in-season excess return, 15 windows | n/a | n/a | n/a | n/a | n/a | REFUTED: +0.81 bps/day, max abs t 2.39, placebo max abs t 3.10 | 2026-09-04_earnings-season-avoidance_cloud.py |
| 2026-09-04 | 23 PREMISE broad: in-season excess return, 15 windows | n/a | n/a | n/a | n/a | n/a | REFUTED: +0.05 bps/day, max abs t 1.42, placebo max abs t 2.16 | 2026-09-04_earnings-season-avoidance_cloud.py |
| 2026-09-04 | 23 PREMISE u56: in-season vol (start 14-28d) | n/a | n/a | n/a | n/a | n/a | FINDING: 0.36-0.39 in-season vs 0.30 out — more risk, no more return | 2026-09-04_earnings-season-avoidance_cloud.py |
| 2026-09-04 | 23 EFFECT: dSharpe of the blackout, 180 season cells | n/a | n/a | n/a | n/a | n/a | KILL: mean -0.129, positive in 1/180; dCAGR -2.19%/yr; dMaxDD +0.50pp | 2026-09-04_earnings-season-avoidance_cloud.py |
| 2026-09-04 | 23 PLACEBO (+45d, same duty cycle), 180 cells | n/a | n/a | n/a | n/a | n/a | CONTROL: mean -0.061, positive in 34/180 — season costs 2x the placebo | 2026-09-04_earnings-season-avoidance_cloud.py |
| 2026-09-04 | 23 u56 v1 anchor (no blackout, = live RULES v1) | 6.5% | 0.66 | -13.8% | 0.64 / 0.69 | 0.66 (0.64/0.69) | control: exact reproduction of the live book | 2026-09-04_earnings-season-avoidance_cloud.py |
| 2026-09-04 | 23 u56 v1 + season(21,28) replace (worst arm in that cell) | 4.0% | 0.45 | -14.6% | 0.55 / 0.37 | 0.66 (0.64/0.69) | KILL 4a / KILL 4b (all bars) | 2026-09-04_earnings-season-avoidance_cloud.py |
| 2026-09-04 | 23 u56 top20 anchor (idea 2's standing 4b KEEP) | 12.7% | 1.09 | -18.3% | 1.09 / 1.10 | 0.66 (0.64/0.69) | control: 4b PASS, reproduces idea 2's row | 2026-09-04_earnings-season-avoidance_cloud.py |
| 2026-09-04 | 23 u56 top20 + season(35,14) replace (best arm in that cell) | 11.6% | 1.04 | -17.2% | 0.98 / 1.09 | 0.66 (0.64/0.69) | 4b PASS but INHERITED: -0.057 Sharpe vs its own anchor | 2026-09-04_earnings-season-avoidance_cloud.py |
| 2026-09-04 | 23 u56 ewall anchor | 10.4% | 1.05 | -15.9% | 1.07 / 1.04 | 0.66 (0.64/0.69) | control | 2026-09-04_earnings-season-avoidance_cloud.py |
| 2026-09-04 | 23 broad top20 anchor | 13.1% | 0.96 | -20.1% | 1.13 / 0.81 | 0.64 (0.76/0.53) | control: KEEP 4a / KILL 4b (H2) | 2026-09-04_earnings-season-avoidance_cloud.py |
| 2026-09-04 | 23 broad ewall anchor | 10.7% | 1.03 | -17.7% | 1.14 / 0.92 | 0.64 (0.76/0.53) | control: 4b PASS (idea 10's EWall) | 2026-09-04_earnings-season-avoidance_cloud.py |
| 2026-09-04 | 23 best season window per cell vs its own anchor | n/a | n/a | n/a | n/a | n/a | KILL: loses in 11/12 cells (-0.075..-0.009); sole exception +0.004 on the weakest book | 2026-09-04_earnings-season-avoidance_cloud.py |
| 2026-09-04 | 23 rule-8 walk-forward, 12 cells | n/a | n/a | n/a | n/a | n/a | picks a blackout in 10/12 on IS Sharpe +0.100; OOS -0.188 mean, regret <= 0 in 12/12 | 2026-09-04_earnings-season-avoidance_cloud.py |
| 2026-09-04 | 23 4b census: 7 season rows pass, all on u56/top20 | n/a | n/a | n/a | n/a | n/a | INHERITED: every one has lower Sharpe than its own passing anchor; 0 conversions | 2026-09-04_earnings-season-avoidance_cloud.py |

### Idea 100 — sleeve-with-a-real-diversifier (cloud, 2026-09-05) — PARK (strong)

120 points (5 sleeve fractions x 2 sleeves x 3 books x 2 universes x 2 gross conventions), all
reported; 2 tuned params (f, sleeve); the S9 arm reproduces idea 26 exactly. Restricting idea 26's
sleeve to its four NON-EQUITY assets (TLT/GLD/DBC/UUP) cuts sleeve-to-book correlation from
0.626..0.820 to -0.011..+0.212 and multiplies the convexity by 5.1x (dSharpe vs the linear blend
+0.265 vs +0.052, positive in 36/36 for both) at 2.9x the exchange rate (0.090 vs 0.031 Sharpe per
pp of CAGR surrendered). It repairs BOTH defects that made idea 26's by-product unadoptable: rule 8
now picks f=0.50 in 8/8 S4 cells and beats its own anchor OOS in 8/8, and the Sharpe advantage
survives deleting 2022 in 8/8 cells. But its literal 4b footprint is SMALLER (2/36 vs 4/36) because
every failure is the CAGR floor, which the natural blend misses only by de-grossing to 0.65-0.70.

| Date | Idea / variant | CAGR | Sharpe | MaxDD | H1 / H2 | Baseline Sharpe | Verdict | Script |
|---|---|---|---|---|---|---|---|---|
| 2026-09-05 | 100 PREMISE: S4 sleeve-to-book correlation | n/a | n/a | n/a | n/a | n/a | CONFIRMED: -0.011..+0.212 (S9 0.626..0.820); S4-to-SPY -0.141 | 2026-09-05_sleeve-with-a-real-diversifier_cloud.py |
| 2026-09-05 | 100 CONVEXITY: dSharpe vs linear blend, 36 interior cells each | n/a | n/a | n/a | n/a | n/a | S4 +0.265 (36/36) vs S9 +0.052 (36/36); 0.090 vs 0.031 Sharpe per pp CAGR | 2026-09-05_sleeve-with-a-real-diversifier_cloud.py |
| 2026-09-05 | 100 u56 top20 + 25pct S4 (natural) | 10.2% | 1.14 | -14.2% | 1.11 / 1.18 | 0.66 (0.64/0.69) | KILL 4b on the CAGR floor ALONE (10.2% vs 10.66%); OOS 1.231 | 2026-09-05_sleeve-with-a-real-diversifier_cloud.py |
| 2026-09-05 | 100 u56 top20 + 25pct S4 (gross-matched) | 10.8% | 1.14 | -14.6% | 1.13 / 1.16 | 0.66 (0.64/0.69) | 4b PASS; OOS 1.217; 9.2x/yr turnover | 2026-09-05_sleeve-with-a-real-diversifier_cloud.py |
| 2026-09-05 | 100 broad top20 + 25pct S4 (gross-matched) | 11.3% | 1.01 | -16.0% | 1.17 / 0.87 | 0.64 (0.76/0.53) | KEEP 4a / KEEP 4b; repairs idea 2's broad H2 failure (0.811 -> 0.865) | 2026-09-05_sleeve-with-a-real-diversifier_cloud.py |
| 2026-09-05 | 100 u56 top20 + 50pct S4 (natural, the rule-8 pick) | 7.7% | 1.19 | -10.0% | 1.10 / 1.27 | 0.66 (0.64/0.69) | KEEP 4a / KILL 4b (CAGR floor); OOS 1.308 vs anchor 1.168 | 2026-09-05_sleeve-with-a-real-diversifier_cloud.py |
| 2026-09-05 | 100 broad top20 + 50pct S4 (natural, the rule-8 pick) | 8.0% | 1.08 | -10.9% | 1.18 / 1.00 | 0.64 (0.76/0.53) | KEEP 4a / KILL 4b (CAGR floor); OOS 1.053 vs anchor 0.892 | 2026-09-05_sleeve-with-a-real-diversifier_cloud.py |
| 2026-09-05 | 100 u56 top20 + 50pct S4 re-grossed to g=1.00 (DIAGNOSTIC, 3rd dial) | 11.8% | 1.15 | -14.2% | 1.10 / 1.20 | 0.66 (0.64/0.69) | 4b PASS — PARK: gross not pre-registered (idea 101) | 2026-09-05_sleeve-with-a-real-diversifier_cloud.py |
| 2026-09-05 | 100 broad top20 + 50pct S4 re-grossed to g=1.00 (DIAGNOSTIC, 3rd dial) | 12.2% | 1.06 | -15.6% | 1.17 / 0.96 | 0.64 (0.76/0.53) | 4b PASS on BOTH universes; Sharpe flat to 0.001 across g | 2026-09-05_sleeve-with-a-real-diversifier_cloud.py |
| 2026-09-05 | 100 S4 standalone (f=1.00) | 2.6% | 0.62 | -8.7% | 0.34 / 0.93 | 0.66 (0.64/0.69) | control: 4b FAIL on CAGR by 8pp; the sleeve is not a book | 2026-09-05_sleeve-with-a-real-diversifier_cloud.py |
| 2026-09-05 | 100 S9 standalone (f=1.00, idea 18 variant B replicated) | 5.0% | 0.87 | -10.1% | 0.76 / 0.98 | 0.66 (0.64/0.69) | control: reproduces idea 18 / idea 26 rows exactly | 2026-09-05_sleeve-with-a-real-diversifier_cloud.py |
| 2026-09-05 | 100 rule-8 walk-forward, 24 cells | n/a | n/a | n/a | n/a | n/a | S4 SELECTABLE: picks f=0.50 in 8/8, beats anchor OOS 8/8, regret 0.000..-0.104; S9 picks f=0 in 4/4 top20+ewall cells | 2026-09-05_sleeve-with-a-real-diversifier_cloud.py |
| 2026-09-05 | 100 ex-2022 test (idea 98's proposed bar) | n/a | n/a | n/a | n/a | n/a | S4 dSharpe vs anchor stays positive in 8/8 ex-2022 (shrink -0.015); S9 negative in 4/8 | 2026-09-05_sleeve-with-a-real-diversifier_cloud.py |
| 2026-09-05 | 100 year attribution of the 25pct S4 sleeve | n/a | n/a | n/a | n/a | n/a | contribution positive in only 2/18 years (2011, 2022) — same shape as idea 26, but the Sharpe edge does NOT depend on it | 2026-09-05_sleeve-with-a-real-diversifier_cloud.py |
| 2026-09-05 | 100 cost ladder 5/10/15/20/25 bps, natural gross | n/a | n/a | n/a | n/a | n/a | cross-universe 4b window 5 bps only (CAGR floor); Sharpe decay -0.048/-0.055 per 10 bps | 2026-09-05_sleeve-with-a-real-diversifier_cloud.py |
| 2026-09-05 | 100 4b census (interior points only) | n/a | n/a | n/a | n/a | n/a | S4 2/36 vs S9 4/36; only S9/top20/f=0.25 passes all 4 universe x convention combos | 2026-09-05_sleeve-with-a-real-diversifier_cloud.py |

### Idea 100b — sleeve-with-a-real-diversifier (INDEPENDENT SECOND RUN, lane B, 2026-09-05)

Lane B ran the same idea the same day without seeing the cloud run. Same design (120 points,
2 tuned params), same conclusion, and the shared numbers agree to the printed precision:
correlation -0.011..+0.212 vs 0.626..0.820, dSharpe +0.265 vs +0.052 (36/36 both), exchange rate
0.090 vs 0.031, S4 standalone 2.6%/0.616/-8.7%. Rows below are only what lane B measured that the
cloud run did not; everything else is a duplicate and is not re-listed.
`research/backtests/2026-09-05_sleeve-with-a-real-diversifier_B.result.md`

| Date | Idea / variant | CAGR | Sharpe | MaxDD | H1 / H2 | Baseline Sharpe | Verdict | Script |
|---|---|---|---|---|---|---|---|---|
| 2026-09-05 | 100b cost ladder 5/10/15/20/25 bps, GROSS-MATCHED blend | n/a | n/a | n/a | n/a | n/a | cross-universe 4b survives 10 bps and dies at 15, for BOTH sleeves — the matched convention buys +5 bps over natural but does not fix the cost window | 2026-09-05_sleeve-with-a-real-diversifier_B.py |
| 2026-09-05 | 100b cross-universe 4b arms at 10 bps, all 120 points | n/a | n/a | n/a | n/a | n/a | exactly 3: top20/S4/matched/f=0.25, top20/S9/matched/f=0.25, top20/S9/natural/f=0.25 | 2026-09-05_sleeve-with-a-real-diversifier_B.py |
| 2026-09-05 | 100b S4-vs-S9 paired, same universe/book/conv/f | n/a | n/a | n/a | n/a | n/a | S4 convexity higher in 36/36 (mean +0.212); S4 CAGR toll larger in 36/36 (mean -1.04pp); S4 exchange rate higher in 32/36 | 2026-09-05_sleeve-with-a-real-diversifier_B.py |
| 2026-09-05 | 100b census, 120 points | n/a | n/a | n/a | n/a | n/a | 4a 78, 4b 14; interior 72 pts, 4a 61, 4b 6 (S9 4 / S4 2) — matches the cloud run | 2026-09-05_sleeve-with-a-real-diversifier_B.py |
| 2026-09-05 | 102 top20 + 50% S4 (TLT,GLD,DBC,UUP) g=1.00, u56 — CONTROL, reproduces idea 100 | 11.8% | 1.15 | -14.2% | 1.10 / 1.20 | 0.66 (0.64/0.69) | 4b (control) | 2026-09-05_which-asset-carries-S4_C.py |
| 2026-09-05 | 102 top20 + 50% noTLT (GLD,DBC,UUP) g=1.00, u56 | 12.4% | 1.15 | -15.6% | 1.04 / 1.26 | 0.66 (0.64/0.69) | 4b — dropping TLT costs nothing | 2026-09-05_which-asset-carries-S4_C.py |
| 2026-09-05 | 102 top20 + 50% noTLT (GLD,DBC,UUP) g=1.00, broad | 12.8% | 1.07 | -17.1% | 1.10 / 1.03 | 0.64 (0.76/0.53) | 4b + 4a; only variant surviving 20 bps in any cell | 2026-09-05_which-asset-carries-S4_C.py |
| 2026-09-05 | 102 top20 + 50% noDBC (TLT,GLD,UUP) g=1.00, u56 — rule-8 pick in 6/8 cells | 11.5% | 1.17 | -13.3% | 1.17 / 1.17 | 0.66 (0.64/0.69) | KEEP-candidate 4a+4b, PARK (2 un-pre-registered dials) | 2026-09-05_which-asset-carries-S4_C.py |
| 2026-09-05 | 102 top20 + 50% noDBC (TLT,GLD,UUP) g=1.00, broad | 12.0% | 1.07 | -14.6% | 1.25 / 0.92 | 0.64 (0.76/0.53) | KEEP-candidate 4a+4b; cross-universe 4b to 15 bps | 2026-09-05_which-asset-carries-S4_C.py |
| 2026-09-05 | 102 top20 + 50% noGLD (TLT,DBC,UUP) g=1.00, u56 — GLD is the load-bearing asset | 11.0% | 1.09 | -14.7% | 1.06 / 1.11 | 0.66 (0.64/0.69) | 4b but retains only 25-54% of S4's dSharpe; dead by 15 bps | 2026-09-05_which-asset-carries-S4_C.py |
| 2026-09-05 | 102 top20 + 50% TLTonly g=1.00, u56 | 10.6% | 0.90 | -25.5% | 1.16 / 0.72 | 0.66 (0.64/0.69) | KILL — the TLT hypothesis | 2026-09-05_which-asset-carries-S4_C.py |
| 2026-09-05 | 102 TLT-only sleeve standalone (f=1.00), u56 | 0.7% | 0.11 | -30.7% | 0.28 / -0.09 | 0.66 (0.64/0.69) | KILL — rising-rate regime -4.8% CAGR / -0.80 Sharpe | 2026-09-05_which-asset-carries-S4_C.py |
| 2026-09-05 | 102 deletion test, dSharpe vs bare book at f=0.50, 8 cells | n/a | n/a | n/a | n/a | n/a | mean dSharpe: noDBC +0.163, S4 +0.122, noTLT +0.109, noUUP +0.056, noGLD +0.049, TLTonly -0.118; positive in 8/8 for all but TLTonly (0/8) | 2026-09-05_which-asset-carries-S4_C.py |
| 2026-09-05 | 102 rate-regime split (falling 2009-21 / rising 2022-26), mean dSharpe | n/a | n/a | n/a | n/a | n/a | rising: noTLT +0.418, noDBC +0.293, S4 +0.249, TLTonly -0.548 — dropping TLT is worth MORE in the rising-rate regime | 2026-09-05_which-asset-carries-S4_C.py |
| 2026-09-05 | 102 sleeve attribution, u56 eval window | n/a | n/a | n/a | n/a | n/a | GLD +33.2pp of +62.1pp total (53%), UUP +12.9, DBC +10.4, TLT +5.6 (9.1%); 2022 TLT contribution -1.86% (vote flat 187/251 days), the +4.34% year came from UUP +4.81 / DBC +2.28 | 2026-09-05_which-asset-carries-S4_C.py |
| 2026-09-05 | 102 rule 8, (sleeve,f) chosen on 2009-2016, 2017-2026 untouched | n/a | n/a | n/a | n/a | n/a | picks noDBC/f=0.50 in 6/8 cells, TLTonly/f=0.25 in 2/8, S4 in 0/8, f=0 in 0/8; OOS beats SPY 8/8 and RULES v1 8/8, anchor 6/8; the 2 TLT picks are the run's 2 worst regrets (-0.223/-0.262) | 2026-09-05_which-asset-carries-S4_C.py |
| 2026-09-05 | 102 cost ladder 5/10/15/20/25 bps at f=0.50, cross-universe 4b | n/a | n/a | n/a | n/a | n/a | g=1.00: S4 and noTLT and noDBC hold to 15 bps, noGLD dies at 15, noUUP and TLTonly never pass; nothing survives 25 | 2026-09-05_which-asset-carries-S4_C.py |
| 2026-09-05 | 102 census, 240 points (6 sleeves x 5 f x 2 books x 2 universes x 2 conv) | n/a | n/a | n/a | n/a | n/a | 4a 114, 4b 39; interior 144 pts, 4a 102, 4b 27 (noTLT 8, S4/noDBC/noGLD 5 each, noUUP 4, TLTonly 0) | 2026-09-05_which-asset-carries-S4_C.py |

**Idea 101 (+104 folded) — fixed-gross-S4-blend (cloud, 2026-09-05).** g fixed at 1.00 EX ANTE; two pre-registered
arms (S4 = TLT,GLD,DBC,UUP; S3 = TLT,GLD,UUP), 2 tuned params (f, cost), 600 grid points, all reported.
`research/backtests/2026-09-05_fixed-gross-S4-blend_cloud.result.md`

| Date | Idea / variant | CAGR | Sharpe | MaxDD | H1 / H2 | Baseline Sharpe | Verdict | Script |
|---|---|---|---|---|---|---|---|---|
| 2026-09-05 | 101 top20 + 50% S3 (TLT,GLD,UUP) g=1.00 fixed, u56, W, 10bps | 11.5% | 1.17 | -13.3% | 1.17 / 1.17 | 0.66 (0.64/0.69) | **KEEP 4a+4b** (OOS 1.215 @ 12.3%; SPY OOS 0.882) | 2026-09-05_fixed-gross-S4-blend_cloud.py |
| 2026-09-05 | 101 top20 + 50% S3 (TLT,GLD,UUP) g=1.00 fixed, broad, W, 10bps | 12.0% | 1.07 | -14.6% | 1.25 / 0.92 | 0.64 (0.76/0.53) | **KEEP 4a+4b** (OOS 0.985 @ 11.1%) | 2026-09-05_fixed-gross-S4-blend_cloud.py |
| 2026-09-05 | 101 top20 + 50% S4 (TLT,GLD,DBC,UUP) g=1.00 fixed, u56, W, 10bps | 11.8% | 1.15 | -14.2% | 1.10 / 1.20 | 0.66 (0.64/0.69) | 4b only — fails 4a on u56 (MaxDD -14.2% vs v1 -13.8%) | 2026-09-05_fixed-gross-S4-blend_cloud.py |
| 2026-09-05 | 101 top20 + 50% S4 g=1.00 fixed, broad, W, 10bps | 12.2% | 1.06 | -15.6% | 1.17 / 0.96 | 0.64 (0.76/0.53) | 4a+4b | 2026-09-05_fixed-gross-S4-blend_cloud.py |
| 2026-09-05 | 101 f-grid at g=1.00, W, 10bps (f=0/.25/.50/.75/1.00) | n/a | n/a | n/a | n/a | n/a | Sharpe peaks at f=0.50 in 4/4 cells — interior optimum, not a boundary pick (u56 S3: 1.064/1.127/**1.167**/1.056/0.392) | 2026-09-05_fixed-gross-S4-blend_cloud.py |
| 2026-09-05 | 101 cost ladder 5/10/15/20/25 bps, cross-universe 4b at f=0.50 | n/a | n/a | n/a | n/a | n/a | BOTH arms hold to 15 bps, die at 20; binding bar is the CAGR floor (u56 -0.49pp at 20) — DD has 5.5-6.9pp headroom at every rung | 2026-09-05_fixed-gross-S4-blend_cloud.py |
| 2026-09-05 | 101 4a cost ladder, cross-universe | n/a | n/a | n/a | n/a | n/a | S3 passes 4a on BOTH universes at all 5 rungs incl. 25 bps; S4 fails 4a on u56 at all 5 — drop-DBC (idea 104) is strictly the better arm | 2026-09-05_fixed-gross-S4-blend_cloud.py |
| 2026-09-05 | 101 rule 8, f chosen on 2009-2016 IS Sharpe (g NOT selected) | n/a | n/a | n/a | n/a | n/a | picks f=0.50 in 44/60 cells, f=0 in 1, mean regret -0.019; at W/10bps picks f=0.50 in 4/4 at ZERO regret — fixing gross removes idea 100's selector/4b mismatch | 2026-09-05_fixed-gross-S4-blend_cloud.py |
| 2026-09-05 | 101 rule 8 OOS (2017-2026) of the pick, 60 cells | n/a | n/a | n/a | n/a | n/a | beats its f=0 anchor 51/60, SPY 44/60, RULES v1 60/60; OOS CAGR >= 70% of SPY's in 39/60 | 2026-09-05_fixed-gross-S4-blend_cloud.py |
| 2026-09-05 | 101 cadence bar (idea 65), \|dSharpe\| across D/W/M <= 0.05 at f=0.50 | n/a | n/a | n/a | n/a | n/a | **FAILS 0/2** (spread 0.33 u56, 0.44 broad) — but the f=0 anchor fails identically (0.26/0.36); the sleeve's OWN contribution is +0.041..+0.155, positive 12/12, spread 0.068/0.075. The bar measures the equity book, not the overlay | 2026-09-05_fixed-gross-S4-blend_cloud.py |
| 2026-09-05 | 101 4b under each cadence at f=0.50, g=1.00, 10bps | n/a | n/a | n/a | n/a | n/a | D **fails 4/4**, W passes 4/4, M passes 4/4 — cadence must be pre-registered as part of the rule; monthly dominates weekly on every metric | 2026-09-05_fixed-gross-S4-blend_cloud.py |
| 2026-09-05 | 101 census, 600 points (2 arms x 5 f x 3 cadences x 2 conv x 2 universes x 5 costs) | n/a | n/a | n/a | n/a | n/a | see .grid.csv; every point reported, nothing hidden | 2026-09-05_fixed-gross-S4-blend_cloud.py |

**Idea 109 (filed as a second "104") — CAGR-floor-constrained-rule-8-selector (cloud, 2026-09-05).**
4 pre-registered selectors x 6 overlay grids x 2 books x 2 universes x 2 cost rungs; 176 grid points, 44 cells.
`research/backtests/2026-09-05_cagr-floor-constrained-selector_cloud.result.md`

| Date | Idea / variant | CAGR | Sharpe | MaxDD | H1 / H2 | Baseline Sharpe | Verdict | Script |
|---|---|---|---|---|---|---|---|---|
| 2026-09-05 | 109 S_floor (argmax IS Sharpe s.t. IS CAGR >= 70% SPY IS CAGR) vs rule 8 | n/a | n/a | n/a | n/a | n/a | **KILL** — same pick in 36/44 cells; in the 8 it differs it is WORSE on OOS Sharpe 8/8 (mean -0.057) | 2026-09-05_cagr-floor-constrained-selector_cloud.py |
| 2026-09-05 | 109 mean OOS (2017-2026) Sharpe by selector, 44 cells | n/a | n/a | n/a | n/a | n/a | S_sharpe 1.048 > S_floor 1.038 > S_cagr 1.023 > S_null 0.993 — monotone in CAGR weight; the constraint is a partial step toward the worst-but-one rule | 2026-09-05_cagr-floor-constrained-selector_cloud.py |
| 2026-09-05 | 109 mean OOS CAGR / MaxDD by selector | n/a | n/a | n/a | n/a | n/a | S_floor buys +0.95pp OOS CAGR in the differing cells at the price of 2.53pp MORE OOS drawdown — wrong side of 4b, which caps DD as well as flooring CAGR | 2026-09-05_cagr-floor-constrained-selector_cloud.py |
| 2026-09-05 | 109 4b passes by selector | n/a | n/a | n/a | n/a | n/a | full-sample: S_sharpe 20, S_floor 21, S_cagr 15, S_null 19; OOS-only: 22 / 21 / 16 / 19. Net movement across the 8 differing cells: +1 full, -1 OOS = zero | 2026-09-05_cagr-floor-constrained-selector_cloud.py |
| 2026-09-05 | 109 the motivating case (sleeve grid, u56/top20/10bps) | n/a | n/a | n/a | n/a | n/a | the constraint does NOT fire: f=0.50 IS CAGR 10.8% clears the 10.47% floor, S_floor picks f=0.50 exactly as rule 8 does — idea 100's mismatch was floating gross, not the objective | 2026-09-05_cagr-floor-constrained-selector_cloud.py |
| 2026-09-05 | 109 constraint feasibility | n/a | n/a | n/a | n/a | n/a | INFEASIBLE in 12/44 cells (27%) — no grid point clears the floor, so the selector silently degenerates to argmax IS CAGR, the worst rule tested (breadth, stop, crypto, u56 band/top20) | 2026-09-05_cagr-floor-constrained-selector_cloud.py |
| 2026-09-05 | 109 control — does selection itself pay? | n/a | n/a | n/a | n/a | n/a | yes: S_null (no overlay) is last on OOS Sharpe 0.993 and worst on regret -0.070 vs rule 8's -0.015. Rule 8 as written is doing real work | 2026-09-05_cagr-floor-constrained-selector_cloud.py |
| 2026-09-05 | 99 premise check — sleeve monotonicity (idea 26's claim) | n/a | n/a | n/a | n/a | n/a | **FALSIFIED 0/4 books.** IS Sharpe is hump-shaped with an interior max at f=0.50 in 4/4 (u56/top20 1.012 1.060 1.077 0.938 0.271); OOS is not monotone up in 4/4. Rule 8 picks a NON-null sleeve in 8/8 cells | 2026-09-05_defensive-overlays-are-rule-8-invisible_B.py |
| 2026-09-05 | 99 the gap G = d(IS) − d(OOS) across 6 overlay grids | n/a | n/a | n/a | n/a | n/a | G real but not "defensive": mean −0.058, negative in 82% of 164 points; crypto (the OFFENSIVE grid) is the most negative at −0.078, 12/12. Per grid: sleeve −0.169, crypto −0.078, breadth −0.057, band −0.036, stop −0.004, gross 0.000 | 2026-09-05_defensive-overlays-are-rule-8-invisible_B.py |
| 2026-09-05 | 99 T2 crisis-density regression (17 years × 2 universes) | n/a | n/a | n/a | n/a | n/a | per-year mean d vs that year's SPY MaxDD: slope −0.73 r −0.41 (all), −1.03 r −0.44 (defensive). Sign flips on year-badness INSIDE each window: defensive d = +0.135 in IS bad years vs −0.147 in IS good years; +0.047 / −0.056 OOS. IS holds 2/7 bad years incl. 2013 (d −0.36/−0.42), OOS 4/10 | 2026-09-05_defensive-overlays-are-rule-8-invisible_B.py |
| 2026-09-05 | 99 rule-8 walk-forward, sleeve pick u56/top20/10bps | 12.3% | 1.18 | -14.3% | 1.16 / 1.20 | 0.65 (0.67/0.64) | KEEP-4b (already standing, idea 101) — chosen on 2009-2016 alone, OOS 13.6%/1.261/-14.3% vs SPY 15.5%/0.882/-33.7% | 2026-09-05_defensive-overlays-are-rule-8-invisible_B.py |
| 2026-09-05 | 99 cost of the alleged blindness | n/a | n/a | n/a | n/a | n/a | rule 8 mean OOS Sharpe 1.048 / 20 of 44 4b vs no-overlay 0.993 / 19 vs OOS-best ceiling 1.063 / **15**. Rule 8 beats not-selecting in 30/44 cells; the ceiling is +0.015 away and costs 5 4b passes | 2026-09-05_defensive-overlays-are-rule-8-invisible_B.py |
| 2026-09-05 | 99 defensive-overlays-are-rule-8-invisible | n/a | n/a | n/a | n/a | n/a | **KILL** — premise false, gap is window crisis-density shared by the offensive overlay, worth +0.015 OOS Sharpe. No RULES change | 2026-09-05_defensive-overlays-are-rule-8-invisible_B.py |

**Idea 112 — 2013-as-the-IS-window's-single-point-of-failure (lane C, 2026-09-05).**
Idea 99's harness re-run with the IS window itself put through leave-one-year-out: 6 overlay grids x 2 books x 2 universes x 2 cost rungs = 44 cells / 208 grid points / 164 non-null, x 8 dropped IS years + control.
`research/backtests/2026-09-05_2013-as-the-IS-windows-single-point-of-failure_C.result.md`

| Date | Idea / variant | CAGR | Sharpe | MaxDD | H1 / H2 | Baseline Sharpe | Verdict | Script |
|---|---|---|---|---|---|---|---|---|
| 2026-09-05 | 112 S4 premise — is 2013 the worst overlay year? | n/a | n/a | n/a | n/a | n/a | **TRUE** — pooled mean d -0.386 (u56 -0.360, broad -0.417), rank 1 of 17, 2.3x the next-worst (2017 -0.169). IS-window ranking: 2013 -0.386, 2012 -0.146, 2015 -0.096, 2010 -0.003, 2016 +0.034, 2014 +0.051, 2011 +0.215 | 2026-09-05_2013-as-the-IS-windows-single-point-of-failure_C.py |
| 2026-09-05 | 112 S1 does deleting 2013 change rule 8's pick? | n/a | n/a | n/a | n/a | n/a | **NOT SUPPORTED** — 2013 moves 8/44 cells vs a median year of 8.5 and 2011's 16; fails both clauses of the pre-registered bar | 2026-09-05_2013-as-the-IS-windows-single-point-of-failure_C.py |
| 2026-09-05 | 112 generic one-year fragility of rule 8's pick | n/a | n/a | n/a | n/a | n/a | 72 pick changes over 352 cell-year deletions (20.5%); no IS year leaves the pick untouched (min 2012 = 5, max 2011 = 16) | 2026-09-05_2013-as-the-IS-windows-single-point-of-failure_C.py |
| 2026-09-05 | 112 S2 OOS price of every LOYO pick swap | n/a | n/a | n/a | n/a | n/a | ex-year picks are WORSE OOS: mean dSharpe -0.014, worse in 40/72, net 4b -10, net 4b-OOS -9. 2013's own 8 swaps OOS-neutral (+0.003) but -4 full-sample 4b | 2026-09-05_2013-as-the-IS-windows-single-point-of-failure_C.py |
| 2026-09-05 | 112 S3 does idea 99's gap G survive deleting 2013? | n/a | n/a | n/a | n/a | n/a | **NO** — pooled mean G -0.058 -> -0.019 (frac neg 0.823 -> 0.683); 2013 carries 66% of the gap and is the ONLY year of 8 that fails the pre-registered survival bar | 2026-09-05_2013-as-the-IS-windows-single-point-of-failure_C.py |
| 2026-09-05 | 112 where the G collapse lives (per grid) | n/a | n/a | n/a | n/a | n/a | entirely the sleeve: G_sleeve -0.169 -> **+0.035** (sign flip, shift +0.204); band +0.004, crypto +0.010, breadth -0.013, stop/gross 0.000. Idea 99's headline per-grid ordering is a one-year artefact | 2026-09-05_2013-as-the-IS-windows-single-point-of-failure_C.py |
| 2026-09-05 | 112 4b/4a counts across 44 cells, full IS vs ex-2013 | n/a | n/a | n/a | n/a | n/a | full IS: 4a 17 / 4b 20 / 4b-OOS 22, mean OOS Sharpe 1.048. ex-2013: 4a 20 / 4b 16 / 4b-OOS 19, 1.049 — re-cutting the window buys nothing and costs 4 4b passes | 2026-09-05_2013-as-the-IS-windows-single-point-of-failure_C.py |
| 2026-09-05 | 112 rule-8 walk-forward, standing candidate's cell (sleeve u56/top20/10bps) | 12.3% | 1.18 | -14.3% | 1.16 / 1.20 | 0.65 (OOS 0.70) | **KEEP-4b unchanged** — f=0.50 picked under the full IS window AND all 8 LOYO windows (ex-2013 IS Sharpes 0.815/0.884/**0.953**/0.933/0.582); OOS 13.6% / 1.261 / -14.3% vs SPY 15.5% / 0.882 / -33.7% | 2026-09-05_2013-as-the-IS-windows-single-point-of-failure_C.py |
| 2026-09-05 | 112 2013-as-the-IS-window's-single-point-of-failure | n/a | n/a | n/a | n/a | n/a | **KILL as posed** — 2013 does not select rule 8's parameters and deleting it makes the walk-forward worse; it DOES carry 66% of idea 99's G, whose per-grid reading must be withdrawn | 2026-09-05_2013-as-the-IS-windows-single-point-of-failure_C.py |
| 2026-09-05 | 114 M->S: does the IS margin predict LOYO pick stability? | n/a | n/a | n/a | n/a | n/a | **YES** — Spearman(M,S) -0.368 (perm p 0.046) on 22 primary cells, -0.240 at 25bps, -0.317 pooled; normalised M/sd is stronger (-0.548 p 0.005 / -0.652 p 0.001) | 2026-09-05_IS-Sharpe-margin-as-the-reportable-selector-statistic_cloud.py |
| 2026-09-05 | 114 M->R: does the IS margin predict OOS regret? | n/a | n/a | n/a | n/a | n/a | **NO** — rho +0.119 (p 0.705), wrong sign, and +0.143 at 25bps. Mean OOS regret is only 0.015 Sharpe (median 0.005, max 0.072); pick is already OOS-best in 16/44 cells, so there is nothing to predict | 2026-09-05_IS-Sharpe-margin-as-the-reportable-selector-statistic_cloud.py |
| 2026-09-05 | 114 margin distribution across 44 cells | n/a | n/a | n/a | n/a | n/a | mean M 0.019 Sharpe, median 0.006, IQR 0.002-0.028, max 0.120. By grid: band 0.044, crypto 0.036, sleeve 0.034, breadth 0.004, stop 0.004, gross 0.001 — gross/breadth picks are near coin flips (mean S 0.375/0.469) | 2026-09-05_IS-Sharpe-margin-as-the-reportable-selector-statistic_cloud.py |
| 2026-09-05 | 114 use test: cells split at the median margin (0.008) | n/a | n/a | n/a | n/a | n/a | high-margin half mean S 0.125 vs low 0.330 and pick=OOS-best 45% vs 18%; but mean R 0.018 vs 0.014 (no separation on regret) | 2026-09-05_IS-Sharpe-margin-as-the-reportable-selector-statistic_cloud.py |
| 2026-09-05 | 114 rule-8 walk-forward, all 44 cells (picks on IS only) | n/a | n/a | n/a | n/a | n/a | 10bps: 4a 9 / 4b 13 / 4b-OOS 15, mean OOS Sharpe 1.115. 25bps: 4a 8 / 4b 7 / 4b-OOS 7, 0.982. Harness reproduces idea 112's LOYO rate exactly (72/352 = 20.5%) | 2026-09-05_IS-Sharpe-margin-as-the-reportable-selector-statistic_cloud.py |
| 2026-09-05 | 114 rule-8 walk-forward, standing candidate's cell (sleeve u56/top20/10bps) | 12.3% | 1.18 | -14.3% | 1.16 / 1.20 | 0.65 (OOS 0.70) | **KEEP-4b unchanged** — pick f=0.50 with M 0.018 (below the 44-cell mean), S 0.250, R 0.000; OOS 13.6% / 1.261 / -14.3% vs SPY 15.5% / 0.882 / -33.7% | 2026-09-05_IS-Sharpe-margin-as-the-reportable-selector-statistic_cloud.py |
| 2026-09-05 | 114 IS-Sharpe-margin-as-the-reportable-selector-statistic | n/a | n/a | n/a | n/a | n/a | **PARTIAL** — margin is a selector-STABILITY statistic, not an OOS confidence interval. Recommend rule 8 quote M and M/sd with that caveat stated; it does not separate 4b passers (mean M 0.021 pass vs 0.016 fail) | 2026-09-05_IS-Sharpe-margin-as-the-reportable-selector-statistic_cloud.py |
| 2026-09-05 | 98 survival of the single best year, 14 standing 4b passes | n/a | n/a | n/a | n/a | n/a | **10/14 survive** deleting their own best year (10 bps). Fails: u56 ew-band3 (CAGR), broad EWall (CAGR), broad top20+50S4 (OOS), broad top20+50S3 (H2,OOS). Best year is **2022 in 13 of 14** (top20/u56 is 2018), mean excess +11.7pp | 2026-09-05_one-year-dependence-as-a-KEEP-bar_cloud.py |
| 2026-09-05 | 98 survive EVERY year deleted (strict LOYO) | n/a | n/a | n/a | n/a | n/a | 5/14. Weakest = idea 72's EWall at 10/18 on broad (reproduces idea 89's 10/18); top20 and frac085 18/18 on u56; EWall+vol60dg 17-18/18 on both at BOTH cost rungs | 2026-09-05_one-year-dependence-as-a-KEEP-bar_cloud.py |
| 2026-09-05 | 98 who moved: book or bar, on every LOYO verdict flip | n/a | n/a | n/a | n/a | n/a | **14 of 16 flips are the BAR, not the book** (idea 89: 12/14). All 6 MaxDD flips bar-side — deleting 2020 raises SPY's 0.60x DD cap by 5.53pp vs book moves of 0.68-2.85pp. Under relative-only 4b every candidate is 18/18 | 2026-09-05_one-year-dependence-as-a-KEEP-bar_cloud.py |
| 2026-09-05 | 98 rule-8 walk-forward: bars applied on 2009-2016, judged 2017-2026 (u56) | 13.0% | 1.213 | -15.4% | n/a | SPY OOS 0.882 | **status-quo 4b admits 4 books, mean OOS Sharpe 1.213, 4/4 beat SPY. B1/B2/B3 admit ZERO.** The LOYO gate discards 4 true positives to buy 0 true negatives | 2026-09-05_one-year-dependence-as-a-KEEP-bar_cloud.py |
| 2026-09-05 | 98 rule-8 walk-forward, broad | 11.5% | 1.041 | -17.3% | n/a | SPY OOS 0.882 | B0 7 books / 1.041; B1 the SAME 7 (+0.000); B2 0 books; B3 5 books (+0.020) — all below the pre-registered +0.05 bar | 2026-09-05_one-year-dependence-as-a-KEEP-bar_cloud.py |
| 2026-09-05 | 98 EWall+vol60dg (idea 94) at 25 bps, both universes | 11.4% u56 / 12.1% broad | 1.113 / 1.119 | -16.9% / -18.7% | 1.14/1.09 u56; 1.24/1.01 broad | 0.32 (u56 v1) | one of only TWO standing candidates passing 4b on both universes at 25 bps (the other is idea 84's ew-band3-g085), and the most year-robust of all: 17/18 u56, 18/18 broad at BOTH cost rungs. By-product of this audit, flagged for the Sunday review | 2026-09-05_one-year-dependence-as-a-KEEP-bar_cloud.py |
| 2026-09-05 | 98 one-year-dependence-as-a-KEEP-bar | n/a | n/a | n/a | n/a | n/a | **KILL as a gate, KEEP as a reported statistic** — LOYO survival is descriptive; every bar variant is REPORT-ONLY on the pre-registered walk-forward because 4b's one-year dependence lives in its two ABSOLUTE bars, which are statements about SPY | 2026-09-05_one-year-dependence-as-a-KEEP-bar_cloud.py |
| 2026-09-05 | 97 tier statement C1 (per-name gate < static gross lever) | n/a | n/a | n/a | n/a | n/a | **33/54 rows. u56 6/6 full but 0/6 IS; broad 6/6 full; small 2/6. Panel- AND window-conditional — not quotable** | 2026-09-05_price-list-tier-bar_B.py |
| 2026-09-05 | 97 tier statement C2 (gross lever < book-level DD rule) | n/a | n/a | n/a | n/a | n/a | 38/54 rows (full 13/18, OOS 9/18); inverts on the small panel 2/6 — the DD control is the CHEAPEST instrument there (0.16-0.57) | 2026-09-05_price-list-tier-bar_B.py |
| 2026-09-05 | 97 tier statement C3 (book-level DD rule < per-name stop) | n/a | n/a | n/a | n/a | n/a | **50/54 rows; 6/6 on all three panels full-sample. The one panel-invariant clause — PROPOSED to PROTOCOL** | 2026-09-05_price-list-tier-bar_B.py |
| 2026-09-05 | 97 median tier price by panel (full sample, pp CAGR per pp MaxDD) | n/a | n/a | n/a | n/a | n/a | u56 T1 0.468 < T2 0.592 < T3 0.659 < T4 unpriced; broad 0.294<0.519<0.579<unpriced; **small T3 0.219 < T2 0.279 < T1 0.350 < T4 0.746 — ordering REVERSES** | 2026-09-05_price-list-tier-bar_B.py |
| 2026-09-05 | 97 "a stop is not insurance" re-checked on the 439-name small panel | n/a | n/a | n/a | n/a | n/a | **REFUTED**: stop dMaxDD > 0 in 9/12 small cells (median +1.07pp) vs u56 -0.69pp / broad -1.03pp (priced 0/6 each). Dearest tier, not inert | 2026-09-05_price-list-tier-bar_B.py |
| 2026-09-05 | 97 tier vs instrument rank stability (Spearman) | n/a | n/a | n/a | n/a | n/a | IS->OOS median: tier +0.400 vs instrument +0.418 (dead heat; idea 94's 0.442 reproduces at 0.418). **Cross-panel: tier +0.800 vs instrument +0.386** | 2026-09-05_price-list-tier-bar_B.py |
| 2026-09-05 | 97 rule-8 walk-forward: tier selector vs idea 94's instrument selector | n/a | n/a | n/a | n/a | SPY OOS 0.882 | **Stier WORSE**: mean OOS regret +0.489 vs S1 +0.337, rank-1 4/18 vs 8/18, dOOS Sharpe +0.007. Also: no rule tier beats the IS gross lever in 12/18 cells | 2026-09-05_price-list-tier-bar_B.py |
| 2026-09-05 | 97 crisis-depth signature of the gate price (u56) | n/a | n/a | n/a | n/a | n/a | Gate tier prices 4.108 IS (SPY MaxDD -22.1%) vs 0.404 OOS (SPY MaxDD -33.7%); lever 1.002 -> 0.616. A price without its window's depth is uninterpretable | 2026-09-05_price-list-tier-bar_B.py |
| 2026-09-05 | 97 EWall+vol60-dg / EWall+band3-rw reproduced (u56, 10bps) | 11.6% / 12.2% | 1.133 / 1.161 | -16.9% / -17.7% | n/a | idea 94 published 11.6%/1.133/-16.9% and 12.2%/1.161/-17.7% | EXACT reproduction; harness imported from idea 94, engine-equivalence max diff 0.0 | 2026-09-05_price-list-tier-bar_B.py |
| 2026-09-05 | 97 4b footprint across three panels @10bps | n/a | n/a | n/a | n/a | n/a | u56 14 arms, broad 4 (g200-rw, band3-rw, v1gate-rw, vol60-dg on EWall), **small 0** — every small arm fails H1+H2+OOS+DD together | 2026-09-05_price-list-tier-bar_B.py |
| 2026-09-05 | 116 idea-112 reproduction (44 cells x 9 LOYO windows) | n/a | n/a | n/a | n/a | idea 112 picks.csv/deltas.csv/swaps.csv | **EXACT**: 0/396 pick mismatches, G leverage max \|diff\| 0.0000, 2011 swaps -0.0331 | 2026-09-05_2011-the-opposite-outlier_C.py |
| 2026-09-05 | 116 the 16 ex-2011 pick swaps, priced OOS | n/a | +1.6pp OOS CAGR | -3.1pp OOS MaxDD | n/a | SPY OOS 0.882 | mean dOOS Sharpe **-0.033**, worse 11/16, net 4b -2 / 4b-OOS -3 -> 2011 is a **FEATURE** of rule 8, not a defect | 2026-09-05_2011-the-opposite-outlier_C.py |
| 2026-09-05 | 116 matched-length selector test (28 L2O windows x 44 cells) | n/a | n/a | n/a | n/a | per-year null (8 years) | premium(2011) **+0.169** — largest of 8, 3.9x the next, unstructured-null p 0.00018 — but **below the pre-registered 0.20 bar**: NOT SUPPORTED | 2026-09-05_2011-the-opposite-outlier_C.py |
| 2026-09-05 | 116 OOS price of keeping 2011 in the IS window | n/a | n/a | n/a | n/a | mean OOS regret 0.018-0.028 | +0.010 mean OOS Sharpe, -0.010 regret. Strong dependence, negligible and correctly-signed consequence | 2026-09-05_2011-the-opposite-outlier_C.py |
| 2026-09-05 | 116 contiguous re-cuts: 2011 vs window LENGTH | n/a | n/a | n/a | n/a | n/a | agree 0.682 (with 2011) vs 0.568 (without) is **length**: 4y 0.577 -> 8y 1.000, and 2011-spans average 5.6y vs 4.3y | 2026-09-05_2011-the-opposite-outlier_C.py |
| 2026-09-05 | 116 rule-8 walk-forward, 44 cells x 46 IS windows | 13.3% (OOS) | 1.048 (OOS) | -19.7% (OOS) | n/a | SPY OOS 15.5%/0.882/-33.7% | **rule 8's own full window is the best of all 46**: OOS Sharpe 1.048, 4b 20/44, 4b-OOS 22/44; ex2011 1.036/18/19 | 2026-09-05_2011-the-opposite-outlier_C.py |
| 2026-09-05 | 116 standing KEEP-4b candidate under a 46-window IS sweep | 12.3% | 1.180 | -14.3% | 1.16 / 1.20 | SPY 15.2%/0.889/-33.7% | **UNTOUCHED**: f=0.50 is the modal pick (28 of 46 windows); OOS 13.6%/1.261/-14.3% | 2026-09-05_2011-the-opposite-outlier_C.py |
| 2026-09-05 | 116 QUEUE clause "2011 is the ONLY year making G more negative" | n/a | n/a | n/a | n/a | idea 112 deltas.csv | **FALSE** — 4 years do (2011 -0.0437, 2014 -0.0095, 2016 -0.0092, 2010 -0.0054). Ranking survives, the word "only" does not | 2026-09-05_2011-the-opposite-outlier_C.py |
| 2026-09-05 | 115 idea-112 sleeve reproduction (32 points) | n/a | n/a | n/a | n/a | idea 112 deltas.csv | **EXACT**: max \|diff\| 1.1e-16 over d_IS/d_OOS/G_full/8x G_ex-year; G -0.1694 -> ex2013 +0.0350 | 2026-09-05_sleeve-G-is-2013_cloud.py |
| 2026-09-05 | 115 which asset loses 2013 (exact leg attribution) | n/a | n/a | n/a | n/a | n/a | **ALL FOUR lose**; TLT -1.16pp > DBC -0.80 > GLD -0.71 > UUP -0.69. Gold's -28.8% carries the smallest weight (1.92%) of the four | 2026-09-05_sleeve-G-is-2013_cloud.py |
| 2026-09-05 | 115 pooled G by sleeve composition | n/a | n/a | n/a | n/a | S4 G -0.1694 | exTLT -0.285, exGLD -0.074, **exDBC +0.021**, exUUP -0.146, GLDonly -0.310, FLAT4 +0.173 — DBC carries the sign, not GLD | 2026-09-05_sleeve-G-is-2013_cloud.py |
| 2026-09-05 | 115 2013-dependence by composition (move in G) | n/a | n/a | n/a | n/a | n/a | S4 +0.204, exGLD +0.186, GLDonly +0.147 — **deleting gold leaves 2013 intact**; 2011 moves G further (0.225) | 2026-09-05_sleeve-G-is-2013_cloud.py |
| 2026-09-05 | 115 2013 excess-damage attribution | n/a | n/a | n/a | n/a | S4 excess -1.915 (z -3.38) | dilution (zero-return leg) **27.5%**, gold **10.9%**, other three assets ~62%. 2013 is a WINDOW property | 2026-09-05_sleeve-G-is-2013_cloud.py |
| 2026-09-05 | 115 rule-8 WF, incumbent S4/top20/10bps (u56) | 12.4% | 1.180 | -14.3% | 1.16 / 1.20 | SPY 0.889 (0.96/0.83); v1 0.649 | pick f=0.50, OOS 13.6%/1.261/-14.3% — **UNTOUCHED** by this run | 2026-09-05_sleeve-G-is-2013_cloud.py |
| 2026-09-05 | 115 exDBC/top20/10bps (u56) — sleeve without commodities | 12.1% | 1.200 | -13.4% | 1.24 / 1.17 | SPY 0.889 (0.96/0.83); v1 0.649 | **KEEP-candidate, 4a AND 4b, both universes** (broad 11.9%/1.068/-14.6%); OOS 12.9%/1.240; wins 8/8 vs S4 full-sample, -0.015 OOS. Memo written; gated on idea 106 | 2026-09-05_sleeve-G-is-2013_cloud.py |
| 2026-09-05 | 115 GLDonly sleeve (strong form of the queue hypothesis) | n/a | n/a | n/a | n/a | n/a | **0 of 40 points pass 4b**; rule 8 picks f=0 (no sleeve) in 6 of 8 cells | 2026-09-05_sleeve-G-is-2013_cloud.py |
| 2026-09-05 | 113 rule 8 (S_sharpe, B=0) — 44-cell reference | 13.3% m | n/a | -19.7% m | n/a | SPY OOS 0.882; v1 OOS 0.65 | mean OOS Sharpe **1.048**, regret vs OOS oracle **-0.0150** (reproduces idea 99's +0.015), 20/44 4b; CAGR/MaxDD marked `m` are means of the 44 cells' OOS values | 2026-09-05_crisis-beta-as-the-pre-registrable-selector_C.py |
| 2026-09-05 | 113 S_crisis B=0.05 / 0.10 / 0.20 (the proposal) | 11.4/11.2/11.0% m | n/a | -17.9/-17.5/-17.2% m | n/a | rule 8 mean OOS Sharpe 1.048 | **KILL** — mean OOS Sharpe 0.960 at all three budgets, dOOS **-0.088** (5.9x the whole ceiling), 4b 20 -> 15/14/14 | 2026-09-05_crisis-beta-as-the-pre-registrable-selector_C.py |
| 2026-09-05 | 113 S_anti B=-0.10 (falsification control) | 14.1% m | n/a | -21.5% m | n/a | rule 8 mean OOS Sharpe 1.048 | dial turned BACKWARDS beats the proposal: -0.025 vs -0.088. Sign of crisis beta carries no OOS information | 2026-09-05_crisis-beta-as-the-pre-registrable-selector_C.py |
| 2026-09-05 | 113 T1 crisis-beta stability, 164 non-null points | n/a | n/a | n/a | n/a | n/a | beta_IS -> beta_OOS slope **+0.172** (spearman +0.744): mean beta 2.80 -> 0.378, a **6x shrinkage** the selector does not apply | 2026-09-05_crisis-beta-as-the-pre-registrable-selector_C.py |
| 2026-09-05 | 113 T2 does crisis beta predict OOS payoff? | n/a | n/a | n/a | n/a | d_IS -> d_OOS r +0.850 / rho +0.703 | beta_IS -> d_OOS r **-0.604** / rho +0.159 (signs disagree = outlier-driven). Rule 8's own input is the better predictor | 2026-09-05_crisis-beta-as-the-pre-registrable-selector_C.py |
| 2026-09-05 | 113 structural defect: beta scales with overlay dose | n/a | n/a | n/a | n/a | sleeve u56/top20 | beta_IS 0 -> 2.6 -> 7.1 -> 14.3 -> **31.8** across f; **any B>0 saturates at the grid endpoint** (f=1.00, OOS Sharpe 0.728 vs 1.261). Grid damage -0.460 | 2026-09-05_crisis-beta-as-the-pre-registrable-selector_C.py |
| 2026-09-05 | 113 realised drawdown budget B* | n/a | n/a | n/a | n/a | IS mean annual SPY MaxDD -11.1% | OOS -13.8% -> **B* = +0.027**, below the smallest budget tested; shrunk by T1 the right coefficient is ~**0.005**. B=0 is near-optimal | 2026-09-05_crisis-beta-as-the-pre-registrable-selector_C.py |
| 2026-09-05 | 113 robustness arm: beta on 28 IS quarters | 11.4/10.8/10.7% m | n/a | -17.9/-17.3/-17.2% m | n/a | rule 8 mean OOS Sharpe 1.048 | verdict unchanged — dOOS -0.091/-0.108/-0.108, better in 1-4 of 44, worse in 17-23. T1 slope +0.332 (still 3x shrinkage) | 2026-09-05_crisis-beta-as-the-pre-registrable-selector_C.py |
| 2026-09-05 | 119 reproduction of idea 97's `V1u/small` price column | 7.05% (ctl) | 0.537 (ctl) | -34.0% (ctl) | 0.62 / 0.47 | v1 small 0.603 (0.689/0.526) | EXACT (engine-equiv 0.0; targets identical over 11 specs) but the QUEUE's count is **FALSE**: 6/10 arms priceable, **5** negative (-1.414..-0.399), `band3-dg` prices **+0.604** | 2026-09-05_v1u-small-negative-price_B.py |
| 2026-09-05 | 119 cost axis 0/5/10/25/50 bps, 10 arms | 10.68% -> -6.33% (ctl) | 0.764 -> -0.366 | -28.0% -> -75.2% | n/a | v1 small 0.603 (0.689/0.526) | **dCAGR stays negative at 0 bps** (median -0.112 pp, 6/10 at every cost) but **dMaxDD FLIPS SIGN**: g200-rw +1.19 pp @10bps -> **-1.27 pp @0bps**. The denominator is a cost artefact | 2026-09-05_v1u-small-negative-price_B.py |
| 2026-09-05 | 119 concentration x scaler, n in {5,10,20,40} x /sqrt(vol20) {on,off} | 7.05% -> 18.72% | 0.537 -> 0.690 | -34.0% -> -39.8% | n/a | v1 small 0.603 (0.689/0.526) | negative rates need BOTH: scaler-on 3/3, 3/3, 2/3, 0/3 by n; **scaler-off 0 of 6 priceable cells**. Deleting the scaler at n=5 is worth **+11.7 pp CAGR** at lower turnover (33.3x -> 21.5x) | 2026-09-05_v1u-small-negative-price_B.py |
| 2026-09-05 | 119 name-sampling: 80 seeded sub-panels of 220/439 names, g200-rw | 4.72% (median ctl) | n/a | -40.3% (median ctl) | n/a | v1 small 0.603 (0.689/0.526) | dCAGR<0 **61/80**, dMaxDD>0 **49/80**, joint free-lunch condition **40/80 = 50.0%**; dMaxDD range [-8.75,+7.79] pp against a full-panel +1.19. **The ratio is not a measurable quantity** | 2026-09-05_v1u-small-negative-price_B.py |
| 2026-09-05 | 119 mechanism: how often the gate binds on V1u/small | n/a | n/a | n/a | n/a | 817 rebalance dates | g200 changes the book on **66/817 dates (8.1%)**, ~77 of 4,074 held name-dates (**1.9%**); gated-out names' median vol20 **0.095** vs 0.173 kept; scaler picks vol20 0.173 vs panel 0.399 | 2026-09-05_v1u-small-negative-price_B.py |
| 2026-09-05 | 119 capacity of the V1u/small book | n/a | n/a | n/a | n/a | 4,074 held name-dates | held-name 20d median $ volume p25 **$0.87M** / p50 **$4.33M**; at $10M capital a 15% position is **34.6% of median ADV** (346% at $100M) at 0.64 of NAV traded per week. **Uninvestable above ~$1M** | 2026-09-05_v1u-small-negative-price_B.py |
| 2026-09-05 | 119 portability of the negative price to u56 / broad | 6.6% / 6.5% (g200-rw) | 0.680 / 0.643 | -13.8% / -21.2% | n/a | v1 small 0.603 (0.689/0.526) | **NOT small-panel specific**: g200-rw -1.414 (small) / -0.184 (u56) / -0.118 (broad); v1gate-rw -0.927/-0.084/-0.076. Magnitude is ~8x, sign is not. Widens idea 97's C1 caveat | 2026-09-05_v1u-small-negative-price_B.py |
| 2026-09-05 | 119 rule-8 walk-forward, S1 and S2 both pick `g200-rw` | 8.86% (OOS) | 0.631 (OOS) | -32.8% (OOS) | 0.69 / 0.59 | SPY OOS 15.45%/0.882/-33.7%; v1 OOS 7.92%/0.581 | beats the live book (+0.94 pp CAGR, +0.050 Sharpe, same DD), loses to SPY by -6.6 pp / -0.251. **IS->OOS price sign agreement 2/4** (g200-dg +0.041 IS -> -0.612 OOS) | 2026-09-05_v1u-small-negative-price_B.py |
| 2026-09-05 | 119 PROTOCOL rule 4, both paths, all V1u/small arms | 8.73% (best arm) | 0.634 (best arm) | -32.8% | 0.69 / 0.59 | v1 small 0.603 (0.689/0.526) | **4b 0/43 arm-points, 4a 0/11** — every arm fails H1, H2, OOS, DD and CAGR simultaneously. The negative price compares two books that are both far worse than SPY | 2026-09-05_v1u-small-negative-price_B.py |
| 2026-09-05 | 119 idea-97 small/V1u pricelist reproduction (32 rows) | n/a | n/a | n/a | n/a | idea 97 pricelist.csv | **EXACT**, max \|diff\| 1.8e-15 (dCAGR/dMaxDD/rate/dSharpe) | 2026-09-05_V1u-small-negative-price_cloud.py |
| 2026-09-05 | 119 premise check of the queue's wording | n/a | n/a | n/a | n/a | n/a | **NOT LITERAL**: 11 negative of 13 priceable of 20 gate rows; band3-dg prices POSITIVE at both rungs; both vol60 arms buy exactly 0 drawdown | 2026-09-05_V1u-small-negative-price_cloud.py |
| 2026-09-05 | 119 noise-band test (material = dMaxDD >= 10% of control MaxDD) | n/a | n/a | n/a | n/a | control MaxDD -34.0% | **0 of 11 negative rows are material** (0.05-3.28 pp bought, 0.15-9.7% of the book's own drawdown); a 3 pp floor leaves 1 gate row | 2026-09-05_V1u-small-negative-price_cloud.py |
| 2026-09-05 | 119 name-subsample bootstrap (200 draws) | n/a | n/a | n/a | n/a | n/a | **ARTEFACT in 7 of 12 audits**; all 3 surviving arms are `-rw` (a SELECTION change, not insurance); every `-dg` arm fails (sign held 52-82%) | 2026-09-05_V1u-small-negative-price_cloud.py |
| 2026-09-05 | 119 time-localisation and costs | n/a | n/a | n/a | n/a | n/a | NOT one year (0 sign flips in 96 arm-years; 2020 largest) and NOT costs (gain present at 0 bps; turnover 32.8-33.5x vs control 33.3x) | 2026-09-05_V1u-small-negative-price_cloud.py |
| 2026-09-05 | 119 concentration sweep n in {5,10,20,40} | n/a | n/a | n/a | n/a | n/a | negative-priced arms 5/6 -> 4/8 -> 4/9 -> 2/9; dg arms' CAGR sign flips to normal by n=20; dMaxDD 0.57 -> 7.69 pp | 2026-09-05_V1u-small-negative-price_cloud.py |
| 2026-09-05 | 119 rule-8 WF pick `g200-rw` (small panel, 10 bps) | 8.7% | 0.634 | -32.8% | 0.69 / 0.59 | SPY 0.862; v1-small 0.581 | OOS 8.9%/0.631/-32.8% vs SPY OOS 15.5%/0.882; regret 0.000 on an uninterpretable ratio | 2026-09-05_V1u-small-negative-price_cloud.py |
| 2026-09-05 | 119 KEEP footprint of every audited small/V1u book | n/a | n/a | n/a | n/a | SPY 14.1%/0.862/-33.7% | **0 of 14 pass 4a; 0 of 14 pass 4b** at either cost rung — nothing here is capital-worthy however the price is read | 2026-09-05_V1u-small-negative-price_cloud.py |
| 2026-09-05 | 118 reproduction of idea 97's 36 ddctl price rows (imported simulator) | n/a | n/a | n/a | n/a | n/a | EXACT: max\|d rate\| 1.1e-16, max\|d dCAGR\| 8.9e-16, max\|d dMaxDD\| 1.8e-15 | 2026-09-05_why-ddctl-is-cheap-on-small_cloud.py |
| 2026-09-05 | 118 H0 units: DD-control price vs the panel's own de-gross lever (108 arms) | n/a | n/a | n/a | n/a | lever = control Calmar in 18/18 cells | Spearman(rate, lever) **0.831**; panel rate 0.824/0.547/0.324 (u56/broad/small) vs rate/lever 1.718/1.360/1.153; spread 2.54x -> 1.49x | 2026-09-05_why-ddctl-is-cheap-on-small_cloud.py |
| 2026-09-05 | 118 H1 depth: re-priced at MATCHED control MaxDD (-15/-20/-25/-30%) | n/a | n/a | n/a | n/a | n/a | **ordering INVERTS**: small 0.324 -> 0.608 (dearest); cheapest panel becomes broad 0.431; spread 2.54x -> 1.55x | 2026-09-05_why-ddctl-is-cheap-on-small_cloud.py |
| 2026-09-05 | 118 H2 name vol: small panel split at median vol20 (0.379 vs 0.618) | n/a | n/a | n/a | n/a | n/a | REFUTED as posed (low-vol 0.228 vs high-vol 0.290 raw); sign flips only after lever-normalisation (1.752 vs 0.966) — not an independent channel | 2026-09-05_why-ddctl-is-cheap-on-small_cloud.py |
| 2026-09-05 | 118 H3 absorbing state (idea 93) on the small panel | n/a | n/a | n/a | n/a | n/a | armed **74.2%** of days (u56 50.6%, broad 54.6%), mean episode 465d, max 2003d, **ends armed 24/36 arms**: the control degenerates into de-grossing | 2026-09-05_why-ddctl-is-cheap-on-small_cloud.py |
| 2026-09-05 | 118 decisive control: static-gross ladder vs DD arm at MATCHED drawdown | n/a | n/a | n/a | n/a | n/a | **ladder wins 107/108 arms (small 36/36)** — idea 22's headline is NOT reversed on small caps; idea 97's slope-based `dominated` flag is the wrong test | 2026-09-05_why-ddctl-is-cheap-on-small_cloud.py |
| 2026-09-05 | 118 rule-8 WF pick, small panel EWall 10 bps (D=0.05, k=0.25) | 4.6% (OOS) | 0.644 (OOS) | -15.3% (OOS) | n/a | SPY OOS 15.5%/0.882/-33.7%; ctl OOS 0.637 | 4a True / 4b False; picks below SPY OOS Sharpe in 14/18 cells and below the no-instrument control in 14/18 | 2026-09-05_why-ddctl-is-cheap-on-small_cloud.py |
| 2026-09-05 | 118 KEEP footprint, all 126 arm-points (3 panels x 3 books x 2 costs x 7 arms) | n/a | n/a | n/a | n/a | SPY 14.1%/0.862/-33.7% | 4a 40/126, 4b **3/126 and 0 on the small panel** (u56/TOP20/10bp x2, broad/EWall/10bp) | 2026-09-05_why-ddctl-is-cheap-on-small_cloud.py |
| 2026-09-05 | 120 idea 119 scaler premium vs a point-in-time ADV floor (median dCAGR over 20 (n,g) cells) | n/a | n/a | n/a | n/a | n/a | **+5.35 pp (no floor, 20/20 cells) -> +0.43 ($1M) -> -2.22 ($5M, 1/20) -> -1.31 ($20M)**: the premium is a sub-$1M-ADV effect | 2026-09-05_delete-the-scaler-on-small_cloud.py |
| 2026-09-05 | 120 unscaled ungated book, $5M ADV floor, n=5 g=0.75 (matched gross) | -4.5% | -0.003 | -82.6% | 0.07 / -0.05 | SPY 0.862 (0.89/0.86); v1-small 0.603 | KILL — all 20 headline cells have NEGATIVE CAGR (-0.10% to -13.95%) | 2026-09-05_delete-the-scaler-on-small_cloud.py |
| 2026-09-05 | 120 full grid 5n x 4g x 4 floors x 2 scaler x 2 gate x 2 gross conventions | n/a | n/a | n/a | n/a | SPY 14.1%/0.862/-33.7% | **4a 20/640, 4b 0/640**; every 4a pass is at the no-floor end | 2026-09-05_delete-the-scaler-on-small_cloud.py |
| 2026-09-05 | 120 rule-8 WF pick S1 (argmax IS Sharpe, $5M floor): n=20 g=1.00 | -4.7% | -0.038 | -83.4% | 0.34 / -0.31 | SPY OOS 15.5%/0.882/-33.7%; v1 OOS 7.9%/0.581 | **OOS -9.17%/-0.171/-83.4%**; DD-capped selector S2 (n=20 g=0.25) OOS -1.56%/-0.174/-33.5% | 2026-09-05_delete-the-scaler-on-small_cloud.py |
| 2026-09-05 | 120 no-ranking control: equal-weight every name passing the floor (g=0.75) | 10.2% -> 1.6% | 0.678 -> 0.181 | -36.2% -> -47.5% | 0.80/0.61 -> 0.32/0.08 | SPY 0.862 | **monotone decay in the ADV floor with no ranking at all** (none/1M/5M/20M: 0.678/0.413/0.181/-0.163); the ranking then subtracts a further -6.15 pp CAGR at $5M | 2026-09-05_delete-the-scaler-on-small_cloud.py |
| 2026-09-05 | 120 capacity of the screened book (held-name dollar ADV, % traded per rebalance) | n/a | n/a | n/a | n/a | n/a | $5M floor n=5: median held ADV $14.5M, 5.6% of ADV at $10M (56% at $100M); unscreened $3.7M and 22.5% — the screen buys real capacity by deleting the names that paid | 2026-09-05_delete-the-scaler-on-small_cloud.py |
| 2026-09-05 | 117 harness verification (idea 94 + idea 97 reproduced) | n/a | n/a | n/a | n/a | n/a | engine diff 0.0e+00; `EWall+vol60-dg` 11.6%/1.133/-16.9%; idea 97 u56 tier 4.108 IS / 0.404 OOS vs levers 1.002/0.616 — all EXACT | 2026-09-05_crisis-depth-as-the-price-denominator_B.py |
| 2026-09-05 | 117 P1 whole-window price vs window crisis depth | n/a | n/a | n/a | n/a | n/a | log-log slope u56 **-4.04** (t -5.78, R2 0.68), broad -3.05 (t -3.35), **small +0.13 (t 0.12, REFUTED)**; median IS/OOS ratio 2.18x over 18 cells (idea 97's pair 10.2x is an outlier). Only 2 distinct depths per panel — an IS/OOS contrast, not an elasticity | 2026-09-05_crisis-depth-as-the-price-denominator_B.py |
| 2026-09-05 | 117 P2 portability of the depth-matched episode price | n/a | n/a | n/a | n/a | n/a | median \|log10(IS/OOS)\| **0.455 -> 0.184** (bar 0.227, CONFIRMED); paired better in **92/109** arms (z +7.18); u56 gate tier's 10.2x becomes **0.93x DEEP / 1.34x SHALLOW** | 2026-09-05_crisis-depth-as-the-price-denominator_B.py |
| 2026-09-05 | 117 P3 protection scales with crisis depth (n=2400 arm-episodes) | n/a | n/a | n/a | n/a | n/a | ALL **+0.161 pp/pp t +15.07**; ddctl +0.320 (t 11.6), gate +0.179 (t 12.4), ebud +0.062, **stop +0.012 t +1.46 — the stop does not respond to depth at all**. Dearest episode E5 2018-02 (-10.1%/9d) prices 9.15; cheapest E7 2020 0.37 | 2026-09-05_crisis-depth-as-the-price-denominator_B.py |
| 2026-09-05 | 117 rule-8 WF `Sdepth` (episode price as selector) vs idea 94's `S1` | 7.4% OOS | 0.713 OOS | -19.5% OOS | n/a | S1 8.2%/0.729/-21.3%; v1 4.9%/0.451; SPY 15.5%/0.882/-33.7% | mean OOS regret **+0.425 vs +0.337**, rank-1 4/18 vs 8/18, dOOS Sharpe -0.016, same pick 8/18 — **better description, worse selector; do not adopt** | 2026-09-05_crisis-depth-as-the-price-denominator_B.py |
| 2026-09-05 | 117 KEEP footprint, 306 arm-points, 3 panels x 3 books x 2 rungs | n/a | n/a | n/a | n/a | SPY 15.2%/0.889/-33.7% | 4b @10bps: u56 10, broad 4 (`band3-rw,g200-rw,v1gate-rw,vol60-dg`), **small 0; none on all three panels**. 4a 3/11/12 incl. the small-panel control (known pathology). **No new candidate** | 2026-09-05_crisis-depth-as-the-price-denominator_B.py |
| 2026-09-05 | 117 crisis-depth-as-the-price-denominator (verdict) | n/a | n/a | n/a | n/a | n/a | **PREMISE CONFIRMED on large caps / REFUTED on small; episode-level replacement PASSES its pre-registered bar and is proposed to PROTOCOL rule 4 as a reporting clause, NOT a selector. No RULES change** | 2026-09-05_crisis-depth-as-the-price-denominator_B.py |
| 2026-09-05 | 121 proposed ADV floor (capacity criterion, ADV only) | n/a | n/a | n/a | n/a | n/a | R20 book trades **17.6%** of p25 held-name ADV at $10M with no screen; **$1M floor** is the smallest ladder value under 10% (7.3%). R10 46%->17%, R5 137%->38%. EW books never bind (0.1-1.9%) | 2026-09-05_liquidity-screened-small-panel_cloud.py |
| 2026-09-05 | 121 EWall level decay by floor (g=0.75, the floor's price) | 10.2%/5.9%/1.6%/-4.9% | 0.678/0.413/0.181/-0.163 | -36%/-40%/-48%/-69% | n/a | SPY 14.1%/0.862/-33.7%; v1 8.2%/0.603/-32.8% | none/$1M/$5M/$20M on 348/252/141/44 names; **reproduces idea 120's no-rank control to 3dp**. Panel return is in names it cannot buy; decay is CONFOUNDED with survivorship | 2026-09-05_liquidity-screened-small-panel_cloud.py |
| 2026-09-05 | 121 Claim A re-run: gate cost on small vs the floor (P1 REFUTED) | n/a | n/a | n/a | n/a | n/a | dCAGR(EWgate-EWall) **-6.52/-4.87/-4.03/-3.56 pp** by floor at g=0.75, dSharpe -0.342/-0.268/-0.263/-0.285, **negative in 12/12 cells**; -5.31 -> -3.70 pp at 0 bps. Ideas 49/51/39's inversion is NOT a thin-name artefact | 2026-09-05_liquidity-screened-small-panel_cloud.py |
| 2026-09-05 | 121 Claim B re-run: four-way gate decomposition n=40 (P2 REFUTED) | n/a | n/a | n/a | n/a | n/a | published order holds EXACTLY at the $1M floor (0.358>0.348>0.323>0.312); inversions at $0 (vol60<both) and $5M (200d<vol60). **Spread 0.080 here vs 0.356 published** — the magnitude is a gross-matching convention (idea 81), not liquidity | 2026-09-05_liquidity-screened-small-panel_cloud.py |
| 2026-09-05 | 121 verdict movement, floor $0 -> $1M (the deliverable) | n/a | n/a | n/a | n/a | n/a | **7 of 48 (book,gross) cells move, all 4a True->False**: EWall g0.50, R5u/R10u g0.50, R20u g0.50+0.75, R40u g0.50+0.75. 4a by floor **7/0/0/0**; **4b 0 of 192 at every floor**. Median floor effect dCAGR -3.10 pp, dSharpe -0.222 | 2026-09-05_liquidity-screened-small-panel_cloud.py |
| 2026-09-05 | 121 rule-8 walk-forward at every floor (S1, ranked family) (P4 CONFIRMED) | 3.6%/1.3%/-2.7%/-16.9% OOS | 0.286/0.163/-0.026/-0.608 OOS | -45%/-50%/-53%/-87% OOS | n/a | SPY OOS 15.45%/0.882/-33.7%; v1 OOS 7.92%/0.581/-32.8% | picks R20 g=1.00 at three floors, R5 g=1.00 at $20M; **OOS Sharpe falls monotonically in the floor**; S2 (IS-DD-capped) is EMPTY at every floor >= $1M | 2026-09-05_liquidity-screened-small-panel_cloud.py |
| 2026-09-05 | 121 liquidity-screened-small-panel (verdict) | n/a | n/a | n/a | n/a | n/a | **ANSWERED — $1M ADV floor proposed as PROTOCOL clause 10 (reporting requirement + default, NOT a load_universe change); deletes all 7 of the panel's 4a passes; Claim A and Claim B's ordering both SURVIVE the screen. No RULES change, no new candidate** | 2026-09-05_liquidity-screened-small-panel_cloud.py |
| 2026-09-05 | 96 reproduction of idea 94's stop arms (exact) | n/a | n/a | n/a | n/a | n/a | generalised simulator at (check=daily, lag=t+1) vs idea 94's `run(stop=...)`: **max\|diff\| 0.000e+00**, zero firing-count differences, 24 arms + 12 controls. Published medians re-derive: dMaxDD **-0.69 / -1.32 pp** (pub -0.69/-1.25), dSharpe -0.036/-0.007, turnover 12.5x/11.3x | 2026-09-05_stop-as-negative-insurance_cloud.py |
| 2026-09-05 | 96 the queue's axis: check frequency (daily vs weekly grid) | n/a | n/a | n/a | n/a | n/a | moves median dMaxDD by 0.1-1.3 pp and **never flips a sign**. Idea 94 was ALREADY checking daily (its step 5 is ungated); the weekly grid governs RE-ENTRY, not exit. **The queue's premise about the code is wrong** | 2026-09-05_stop-as-negative-insurance_cloud.py |
| 2026-09-05 | 96 the axis that matters: ONE day of execution lag (P3 REFUTED) | n/a | n/a | n/a | n/a | n/a | median dMaxDD **-0.69 pp** at t+1 (PROTOCOL rule 2) -> **+2.44 pp** at t+2 -> **-0.25 pp** at the next rebalance; non-monotone, sign flips on one bar. dMaxDD<0 in 12/12 vs 4/12 vs 8/12 cells | 2026-09-05_stop-as-negative-insurance_cloud.py |
| 2026-09-05 | 96 mechanism: post-trigger short-term reversal (test H) | n/a | n/a | n/a | n/a | n/a | day after a stop fires the triggering name earns **+0.57% to +2.21%** vs unconditional +0.06%/day, **t +2.70 to +10.37**, excess in 9/12 cells (median +0.615 pp/day), persisting +1.2..+2.6% over 5d. The slower exit harvests a bounce — not insurance | 2026-09-05_stop-as-negative-insurance_cloud.py |
| 2026-09-05 | 96 the 9 apparent 4b passes (all on the NON-conformant t+2 lag) | 12.1-15.1% | 1.057-1.176 | -18.6..-20.1% | 1.12-1.25 / 1.01-1.12 | SPY 15.2%/0.889/-33.7%; all 12 controls fail 4b on the DD cap alone (-22.2%/-22.5% vs -20.2%) | **NOT candidates**: violate rule 2; margins 0.15-1.6 pp on a single-path extremum; rule 8 picks the **no-stop control** in all 4 cells they live in (IS diff <=0.001); **0 of 9 on `broad`** | 2026-09-05_stop-as-negative-insurance_cloud.py |
| 2026-09-05 | 96 rule-8 walk-forward over {12 stop arms + no-stop control}, 12 cells | n/a | n/a | n/a | n/a | v1 OOS 0.714 (u56) / 0.573 (broad); SPY OOS 0.882 | selector takes a stop in **5/12**, mean OOS regret **+0.002**; picks the control in 7/12 including every cell with a 4b pass. Static-gross lever prices drawdown at 0.05-0.74 pp/pp; the conformant stop is off the menu | 2026-09-05_stop-as-negative-insurance_cloud.py |
| 2026-09-05 | 96 stop-as-negative-insurance (verdict) | n/a | n/a | n/a | n/a | n/a | **ANSWERED — idea 94's KILL STANDS and is strengthened. The sign is neither the instrument nor the grid: it is the one-day execution lag, and under PROTOCOL rule 2's own convention the stop still destroys drawdown. Proposed to PROTOCOL: rule 2 extended so every intra-period rule states trigger frequency and execution lag, and no drawdown price is quoted without its lag. No RULES change** | 2026-09-05_stop-as-negative-insurance_cloud.py |
| 2026-09-05 | 122 reproduction of idea 94's pricelist (192 rows, u56 + broad) | n/a | n/a | n/a | n/a | idea 94 pricelist.csv | **EXACT**: max|diff| dCAGR 8.9e-16, dMaxDD 1.8e-15, rate 1.1e-16; NaN-pattern 192/192; cached targets vs idea 94 targets() 0.0e+00 | 2026-09-05_price-denominator-sign-test_C.py |
| 2026-09-05 | 122 denominator sign test on the published rates (q=0.10, tau=0.90) | n/a | n/a | n/a | n/a | idea 119 small panel 49/80 | **90 of 138 admissible (65%)** — D1 cost 133/138, D2 window 98/138, D3 panel 114/138. The premise is NOT literal on the large-cap lists | 2026-09-05_price-denominator-sign-test_C.py |
| 2026-09-05 | 122 where the instability lives (book vs panel) | n/a | n/a | n/a | n/a | n/a | **all 24 D3 and all 5 D1 failures are the 5-name V1u book** (16/41 admissible) vs EWall 47/48, TOP20 27/49 — a book-size effect, not a panel effect | 2026-09-05_price-denominator-sign-test_C.py |
| 2026-09-05 | 122 where the instability lives (window vs cost) | n/a | n/a | n/a | n/a | n/a | **dMaxDD_IS <= 0 in 40 of 138 rows, dMaxDD_OOS <= 0 in 0 of 138**; median dMaxDD IS 0.03/0.17/3.25 vs OOS 3.83/2.27/6.92 pp (TOP20/V1u/EWall) — idea 117's crisis depth, seen in the sign | 2026-09-05_price-denominator-sign-test_C.py |
| 2026-09-05 | 122 all 12 grid points q in {0.05,0.10,0.20} x tau in {0.80,0.90,0.95,1.00} | n/a | n/a | n/a | n/a | n/a | **80-96 of 138 admissible (58-70%)** — the test is insensitive to both of its own tuned parameters | 2026-09-05_price-denominator-sign-test_C.py |
| 2026-09-05 | 122 rule-8 walk-forward, IS-only screen on idea 94's selector | 8.91% (OOS) | 0.801 (OOS) | -19.0% (OOS) | n/a | SPY OOS 15.45%/0.882/-33.7%; v1 OOS 0.470 | **S2 = S1: 0 of 12 picks changed** at the stated setting; control OOS Sharpe 0.852 beats the picks in 7/12 cells, SPY in 6/12 | 2026-09-05_price-denominator-sign-test_C.py |
| 2026-09-05 | 122 rule-8 walk-forward, screen tightened until it binds (q=0.20, tau=1.00) | 8.41% (OOS) | 0.768 (OOS) | -16.7% (OOS) | n/a | SPY OOS 0.882; S1 0.801 | changes 2 of 12 picks and **both are worse OOS** (broad/V1u g200-rw -> ebud-0.10: 0.590->0.367 and 0.169->0.000) — KILL as a selector | 2026-09-05_price-denominator-sign-test_C.py |
| 2026-09-05 | 122 OOS discriminating power of the IS-only screen | n/a | n/a | n/a | n/a | n/a | **none**: OOS denominator positive in 138/138 rows for IS-admissible AND IS-rejected alike at all 12 grid points; the screen keeps the dearer half (median rate 0.494 vs 0.065) | 2026-09-05_price-denominator-sign-test_C.py |
| 2026-09-05 | 122 KEEP footprint of the audited grid, both paths | n/a | n/a | n/a | n/a | SPY 15.2%/0.889/-33.7% | **4a 54/192, 4b 29/192** (inherited from idea 94); of the 90 admissible rows 4a 38, 4b 26. 3 4b passes keep KEEP but lose the right to quote a price | 2026-09-05_price-denominator-sign-test_C.py |

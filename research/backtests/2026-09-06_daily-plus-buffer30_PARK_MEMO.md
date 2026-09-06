# PARK memo — `top20-200d, DAILY cadence, rank buffer m=30` (idea 279 by-product, 2026-09-06, cloud)

1. **What it is.** Idea 66's `top20-200d` book (gross 0.75, t+1) rebalanced DAILY, with idea 273's no-trade band on the composite rank at m=30. Realised turnover 7.05x/yr on broad, 5.85x/yr on u56.
2. **4b, broad136 @10 bps:** CAGR 14.71%, Sharpe 1.0717, MaxDD -18.79%, halves 1.248 / 0.918, OOS 1.0292 vs SPY 0.884. PASS all five bars.
3. **4b, broad136 @25 bps:** 13.51% / 0.9946 / -19.10%, halves 1.170 / 0.842, OOS 0.9534. PASS.
4. **4b, u56 @10 / @25 bps:** 11.73% / 1.1411 / -13.26% (OOS 1.2575) and 10.75% / 1.0546 / -14.43% (OOS 1.1754). PASS both.
5. **Anchor:** daily cadence has no phase, so the anchor band is 0 by construction — the only cell in this run with zero anchor sensitivity.
6. **Why it is PARK, not KEEP.** PROTOCOL rule 8's pre-registered chooser (IS Sharpe on 2009-2016) picks `cad=Q, m=999` on broad and `cad=Q, m=30/50` on u56 — never this cell — and its pick loses to doing nothing OOS. m=30 was found by reading this run's own grid.
7. **Second reason.** At 25 bps on broad it is an ISLAND: m=20 and m=50 both fail 4b on H2; only m=30 survives. On u56 it is not an island (m=15..999 all pass).
8. **4a:** fails everywhere. RULES v2 (live) posts Sharpe 1.107 / MaxDD -12.24% on broad; this arm is higher-return and much higher-drawdown.
9. **SURVIVORSHIP:** broad136 and u56 are current constituents only; absolute CAGR/Sharpe are optimistic. All comparisons here are within-panel on identical days.
10. **Exact RULES wording if it is ever promoted:** *"Each trading day, rank every name whose price is above its 200-day moving average and whose 20-day annualised volatility is below 0.60 by the mean of its percentile ranks on 12-1 month, 6-month and 3-month return. Hold a name once its rank is 20 or better; sell it only when it leaves the eligible set or its rank falls past 50. Hold each position at 3.75% of NAV; the remainder is cash. Orders are placed on the close and filled at the next close."*

Script: `research/backtests/2026-09-06_does-the-buffer-beat-the-cadence-dial-at-matched-realised-turnover_cloud.py`

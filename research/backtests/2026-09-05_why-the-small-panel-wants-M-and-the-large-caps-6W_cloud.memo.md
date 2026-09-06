# Memo — U56 monthly top-20 clears 4b at 0/10/25 bps (by-product of idea 188). NOT PROPOSED.

1. **What passed.** On the fixed U56 panel, `top-20 equal weight on the scan.py composite, no
   vol scaler, gross 0.75, bare 200d gate, vol20 < 0.60, rebalanced MONTHLY, t+1` passes
   PROTOCOL 4b at **0, 10 and 25 bps** — 14.76% CAGR / 1.2081 Sharpe / −19.58% MaxDD at
   10 bps, halves 1.2185 / 1.2064, OOS 1.2866 Sharpe / 16.71% CAGR / −19.58% MaxDD, 4.28×/yr
   turnover. SPY on the same window: 15.23% / 0.8890 / −33.72% (H1 0.9566, H2 0.8340), so the
   4b bars are DD ≤ 20.23% and CAGR ≥ 10.66%. It fails 4a on drawdown, as every growth book does.
2. **Exact RULES wording it would need** (for the record only): *"Eligible = price above its
   200-day moving average and 20-day annualised vol below 0.60. Rank eligible names by the
   equal-weighted average of the percentile ranks of 12−1 momentum, 6-month and 3-month
   return. Hold the top 20 at 3.75% each (75% gross, 25% cash). Re-evaluate on the last
   trading day of each calendar month and execute at the next close."*
3. **Why it is NOT proposed.** It is **single-universe**: the identical construction is 0/7 on
   SMALL439 and 0/7 on ETF36 at every cost rung. Idea 53 already killed a U56-only 4b pass on
   exactly this ground.
4. It is also **not new**: it reproduces the standing candidate the queue carries as idea 182
   (`monthly r6 top-20 on u56 at 10 and 25 bps`), from a different script and a different
   corpus. Treat this as a third independent reproduction, not a discovery.
5. **The nearby Sharpe argmax is worse, not better.** 6W beats M on Sharpe at every rung
   (1.2252 vs 1.2081 at 10 bps) and **fails 4b on drawdown at every rung** (−21.99% vs the
   −20.23% cap). Idea 152's Sharpe-vs-4b sign flip, reproduced on the cadence dial.
6. **SURVIVORSHIP** — U56 is a current-constituent list (idea 54). The level is biased upward
   and this is not a tradable return estimate.
7. Costs are a flat linear bps charge on turnover; no spread/impact model is claimed.
8. Idea 144 applies: a re-cadenced book is the SAME book. This is not a new signal.
9. **Nothing in RULES.md, scan.py, bot.py or baseline.py was touched by idea 188.**
10. **Recommendation: no action.** If Sunday review wants to act on the monthly cadence at
    all, the question to answer first is idea 182's, not this memo's — and the cross-universe
    failure in line 3 has to be closed before either becomes capital-worthy.

# Research Queue (claim an idea by moving it to "In progress" with the date; results go to LEADERBOARD.md)
## Open
1. no-vol-scaling — same composite but without dividing by sqrt(vol20). Does vol scaling help or just favor low-vol ETFs?
2. position-count — top 3 vs 5 vs 8 equal-weight (2 params max: n).
3. rebalance-freq — weekly vs monthly vs quarterly for RULES v1.
4. abs-momentum-filter — replace 200d-MA filter with 12-1 momentum > 0; also try both.
5. dual-momentum-classes — Antonacci-style: SPY/EFA/EEM/TLT/GLD/DBC, hold top 1-2 by 12m return if > T-bill proxy (SHY), else SHY.
6. defensive-sleeve — when breadth (% above 200d) < 40%, move the cash sleeve into TLT/GLD/SHY best-of-3 by 3m momentum.
7. inverse-vol-weights — weight the top 5 by 1/vol20 instead of equal.
8. lookback-blend — 12-1 only vs 6-1 vs 3-1 vs blend; which lookback horizon holds across halves?
9. trailing-stop — add 15% trailing stop overlay to v1.
10. sector-only-universe — run v1 on sectors + broad ETFs only (drop single stocks). Less idiosyncratic risk?
11. cost-sensitivity — v1 at 5/10/25/50 bps; at what cost does the edge die?
12. vol-target — scale v1 gross exposure to target 12% annualized portfolio vol (cap 100%).
13. 52w-high-proximity — rank by closeness to 52w high (George & Hwang) instead of returns.
14. rsi2-sleeve — allocate 25% of book to a RSI2<10-in-uptrend mean-reversion sleeve on sector ETFs.
15. crypto-sleeve — allow BTC-USD/ETH-USD at max 10% each under v1 rules.
16. monthly-seasonality — v1 with exposure reduced in historically weak months (test, expect KILL).
## In progress
## Done (see LEADERBOARD.md)

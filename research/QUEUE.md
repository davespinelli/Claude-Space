# Research Queue (claim an idea by moving it to "In progress" with the date; results go to LEADERBOARD.md)
## Open
1. no-vol-scaling — same composite but without dividing by sqrt(vol20). Does vol scaling help or just favor low-vol ETFs?
2. position-count — top 3 vs 5 vs 8 equal-weight (2 params max: n).
3. rebalance-freq — weekly vs monthly vs quarterly for RULES v1.
4. abs-momentum-filter — replace 200d-MA filter with 12-1 momentum > 0; also try both.
6. defensive-sleeve — when breadth (% above 200d) < 40%, move the cash sleeve into TLT/GLD/SHY best-of-3 by 3m momentum.
8. lookback-blend — 12-1 only vs 6-1 vs 3-1 vs blend; which lookback horizon holds across halves?
9. trailing-stop — add 15% trailing stop overlay to v1.
10. sector-only-universe — run v1 on sectors + broad ETFs only (drop single stocks). Less idiosyncratic risk?
11. cost-sensitivity — v1 at 5/10/25/50 bps; at what cost does the edge die?
13. 52w-high-proximity — rank by closeness to 52w high (George & Hwang) instead of returns.
14. rsi2-sleeve — allocate 25% of book to a RSI2<10-in-uptrend mean-reversion sleeve on sector ETFs.
15. crypto-sleeve — allow BTC-USD/ETH-USD at max 10% each under v1 rules.
16. monthly-seasonality — v1 with exposure reduced in historically weak months (test, expect KILL).
19. spy-tlt-gld-riskparity — inverse-vol risk parity on SPY/TLT/GLD monthly, as a low-turnover benchmark the live book must beat.
21. momentum-plus-quality-proxy — among top-10 momentum in broad universe, drop the 3 highest-vol names (vol as quality proxy). Max 2 params.
22. drawdown-control — v1 with book-level rule: if book drawdown > 8%, halve exposure until new high. (Test, expect mixed)
23. earnings-season-avoidance — v1 excluding single stocks during their earnings weeks (approximate with quarterly calendar). Expect PARK: needs earnings dates.
26. ensemble-plus-momentum — 50% macro-trend-ensemble B + 50% v1 top-5. Diversification of two weak-ish sleeves.
## In progress
24. core-plus-trend-sleeve — 60% SPY/QQQ core (SPY 200d filter to cash) + 40% macro-trend-ensemble variant B. Target: SPY-like CAGR with half the drawdown. (Follows Sep 3 diagnostic) (claimed 2026-09-03, local session)
25. composite-vs-equal-weight — v1 eligibility (above 200d, vol<0.6) but EQUAL weight all eligible names instead of top-5 by score. Does the score add anything? (claimed 2026-09-03, local session)
27. qqq-trend-only — QQQ when above 200d (and 12-1 mom > 0), else SHY. Simplest possible growth+trend benchmark the book must beat. (claimed 2026-09-03, local session)
## Done (see LEADERBOARD.md)
5. dual-momentum-classes — KILL — all 4 variants below baseline Sharpe in H1 (best 0.39 vs 0.64), MaxDD -24% to -36% vs -13.8%; DBC 2022-23 collapse (2026-09-03)
7. inverse-vol-weights — KILL — Sharpe 0.57 vs 0.67 both halves; double vol tilt (score already /sqrt(vol)) concentrates book to 2-3 names (2026-09-03)
12. vol-target — KILL — 10%/14% targets: Sharpe 0.59/0.60 vs 0.67, deeper DD; v1 realizes ~10% vol so cap binds, cuts after spikes (2026-09-03)
17. broad-momentum-top10 — KILL/PARK — at matched 75% exposure Sharpe 0.67 vs 0.66, OOS 0.58 vs 0.74; top20@100% PARK (ties live OOS, 1.7x DD, survivorship-flattered) (2026-09-03)
18. macro-trend-ensemble — KEEP-candidate — variant B (mom-sign votes, inverse-vol, 9 macro ETFs) Sharpe 0.87 (H1 0.75/H2 0.98), MaxDD -10.1%, OOS 1.08 vs 0.74; but CAGR only 5.0%, UUP ~13% weight flatters Sharpe. Sleeve, not replacement (2026-09-03)
20. full-exposure-v1 — KILL — 100% gross = same Sharpe (corr 1.00) at 1.33x vol; SPY-200d filter hurts; per-name filter earns 2pp DD in 2022 only; gap to SPY is selection, not exposure (2026-09-03)

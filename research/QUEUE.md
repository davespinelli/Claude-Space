# Research Queue (claim an idea by moving it to "In progress" with the date; results go to LEADERBOARD.md)
## Open
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
28. eligible-equal-weight-v2 — the v2 candidate: equal-weight ALL names above 200d with vol20<0.60, weekly. Report gross 75/85/100 (all three, no picking), halves, OOS, 2020/2022, turnover. Also with BTC/ETH excluded vs included at 5% cap. (Sep 3 IC finding)
29. momentum-no-vol-scaler — top-5 and top-10 by 12-1 momentum among eligible (no /sqrt(vol) term), 75% and 100% gross; report all; survivorship caveat. (Sep 3 IC finding)
30. qqq-core-plus-sleeve-h1 — why does 60% QQQ + 40% sleeve lose to SPY on Sharpe in 2009-2017? Decompose by year; test 50% QQQ + 10% SPY + 40% sleeve. (Sep 3 PARK)
31. small-cap-pead — post-earnings-announcement drift in small caps: use the 8-K earnings-release date (EDGAR) and the 2-day announcement return as the surprise proxy; long top decile, hold 60 trading days. (Chan-Jegadeesh-Lakonishok 1996; stronger in small caps)
32. insider-cluster-buying — Form 4 open-market purchases by >=2 distinct insiders within 30 days in small caps; hold 6-12 months. (Cohen-Malloy-Pomorski 2012 opportunistic trades)
33. amihud-illiquidity-premium — within the small-cap universe, long the least liquid quintile (Amihud ratio) with a momentum filter; test if the premium survives 10-25 bps costs. (Amihud 2002)
34. volume-shock-continuation — abnormal volume (20d vs 120d) with positive return: continuation vs reversal at 1w/1m/3m horizons in small caps. (Gervais-Kaniel-Mingelgrin 2001 high-volume return premium)
35. options-iv-snapshot-cache — start a DAILY cache of yfinance option chains (IV, skew, put/call OI) for the live universe + candidates; no history exists for free, so build it now for later tests (IV-RV spread, skew as sentiment).
36. spinoff-calendar — Form 10 / 10-12B filings from EDGAR full-text search: build the last 5 years of spin-offs and test the classic 6-24 month post-spin outperformance. (Cusatis-Miles-Woolridge 1993)
37. index-deletion-reversal — Russell reconstitution deletions (June) and S&P 600 removals: post-deletion reversal in small caps.
38. FIX-calendar-day-index — data/prices.csv (and prices_broad.csv) are indexed on calendar days from 2014-09-17 because BTC-USD is in the download; every equity is ffilled across weekends. Distorts all sandbox backtests AND research/scan.py's live 200d/vol20 signals (4.2 of 56 names mis-flagged per day). Fix cache_prices.py + load_universe() + scan.py to a trading-day index. INFRASTRUCTURE — do first, before trusting any further cloud-run result. (2026-09-04, lane A)
39. rerun-sandbox-rows-corrected — after 38, re-run any leaderboard row produced in the sandbox on the corrected index and mark rows that change verdict. (2026-09-04, lane A)
40. vol-scaler-replacement — the scaler is harmful but the no-scaler book breaches 4b's drawdown cap at every n. Test drawdown control ON TOP of the no-scaler book (idea 22's book-level rule, or a 200d-breadth gate) rather than per-name vol scaling. Max 2 params. (2026-09-04, lane A)
## In progress
## Done (see LEADERBOARD.md)
1. no-vol-scaling — KILL as a v1 replacement (all 12 grid points fail 4a on MaxDD and 4b), but the scaler is confirmed harmful: removing it is worth +10.1%/yr (t 3.33) and beats v1 on Sharpe at every (n, gross); nearest miss OFF n=8/75% 13.8%/0.93/-17.9% fails 4b on H1 alone (0.92 vs SPY 0.96). Run also found a repo-wide calendar-day index bug in data/prices.csv (see result memo) (2026-09-04, lane A)
5. dual-momentum-classes — KILL — all 4 variants below baseline Sharpe in H1 (best 0.39 vs 0.64), MaxDD -24% to -36% vs -13.8%; DBC 2022-23 collapse (2026-09-03)
7. inverse-vol-weights — KILL — Sharpe 0.57 vs 0.67 both halves; double vol tilt (score already /sqrt(vol)) concentrates book to 2-3 names (2026-09-03)
12. vol-target — KILL — 10%/14% targets: Sharpe 0.59/0.60 vs 0.67, deeper DD; v1 realizes ~10% vol so cap binds, cuts after spikes (2026-09-03)
17. broad-momentum-top10 — KILL/PARK — at matched 75% exposure Sharpe 0.67 vs 0.66, OOS 0.58 vs 0.74; top20@100% PARK (ties live OOS, 1.7x DD, survivorship-flattered) (2026-09-03)
18. macro-trend-ensemble — KEEP-candidate — variant B (mom-sign votes, inverse-vol, 9 macro ETFs) Sharpe 0.87 (H1 0.75/H2 0.98), MaxDD -10.1%, OOS 1.08 vs 0.74; but CAGR only 5.0%, UUP ~13% weight flatters Sharpe. Sleeve, not replacement (2026-09-03)
20. full-exposure-v1 — KILL — 100% gross = same Sharpe (corr 1.00) at 1.33x vol; SPY-200d filter hurts; per-name filter earns 2pp DD in 2022 only; gap to SPY is selection, not exposure (2026-09-03)
24. core-plus-trend-sleeve — PARK — B (60% QQQ>200d + 40% sleeve) 10.8%/0.95/-18.9%, OOS 14.2%/1.15/-18.9%; fails 4b only on H1 Sharpe 0.84 vs SPY 0.96. Strongest growth candidate (2026-09-03)
25. composite-vs-equal-weight — PARK/ACTIONABLE — traded score IC≈0 (t 0.4); /sqrt(vol20) cancels momentum (pre-scaler IC t 4.2). Equal-weight all eligible @75%: 10.4%/1.05, halves 1.07/1.03 (> SPY both), misses 4b CAGR floor by 0.23pp (2026-09-03)
27. qqq-trend-only — KILL — filter costs 6.4pp CAGR vs QQQ B&H (20.8%/1.01); variants 12-15%/0.83-0.91/-27%; live book beaten 3x by a napkin rule (2026-09-03)

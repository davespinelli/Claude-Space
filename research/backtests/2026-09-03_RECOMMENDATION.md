# Recommendation memo for the Sunday review (written Sep 3 late, local sprint of 9 ideas)

## Finding 1 — the live score is noise (composite-vs-equal-weight)
Rank IC of the traded v1 score vs next 1w/4w returns: +0.004 / +0.001 (t 0.4 / 0.1) over 917 weekly cross-sections, zero in both halves. Bottom-5 by score out-earned top-5. Cause: the composite before `/sqrt(vol20)` has IC t≈4.2; the vol scaler alone has IC t≈-5.7; the division cancels the signal. Adding the score to the eligibility filter costs -3.6%/yr (t -2.1).

## Finding 2 — the eligibility filter is the edge
Equal-weight ALL eligible names (above 200d, vol20<0.60), 75% gross, weekly: CAGR 10.4%, Sharpe 1.05, halves 1.07 / 1.03 (SPY 0.96 / 0.83), lower vol than v1, one third of the turnover. Misses the 4b CAGR floor (70% of SPY = 10.6%) by 0.23pp. Idea 28 in QUEUE tests it properly (gross 75/85/100 reported together, OOS, stress years).

## Finding 3 — growth candidate (core-plus-trend-sleeve B)
60% QQQ (cash when QQQ < 200d) + 40% macro-trend-ensemble sleeve B: CAGR 10.8%, Sharpe 0.95, MaxDD -18.9%; OOS 2017–2026 CAGR 14.2%, Sharpe 1.15, MaxDD -18.9%. Fails 4b only on H1 Sharpe (0.84 vs SPY 0.96). Idea 30 investigates.

## Finding 4 — exposure and universe are not the problem
100% gross v1 has identical Sharpe (corr 1.00). Broad universe adds nothing at matched exposure. QQQ trend filters cost 6pp CAGR vs QQQ buy-and-hold.

## Recommended action for Sunday (if idea 28 verifies under PROTOCOL 4b or clearly under 4a)
RULES v2: drop the score entirely. Hold every instrument that is above its 200d average with vol20 < 0.60, equal weight, gross G (G chosen ONLY from idea 28's three reported values by the pre-stated rule "smallest G whose MaxDD ≤ 60% of SPY's and CAGR ≥ 70% of SPY's"; if none, keep 75%). Weekly rebalance; daily hard exit below 200d stays. Update baseline.py (rules_v2_weights), bot.py, scan.py (score becomes informational), CHANGELOG, RULES.md version.
Do NOT adopt Finding 3 yet; it needs idea 30.

## Caveats to carry into any live decision
Current-constituent survivorship bias in universe.json (favours momentum/growth sleeves). Only 2020 and 2022 are real stress tests. 2009–2026 is a QQQ-favourable regime. Paper + Alpaca live record starts Sep 4; nothing here justifies real capital before ≥8 weeks of live tracking.

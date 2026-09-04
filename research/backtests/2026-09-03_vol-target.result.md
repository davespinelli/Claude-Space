# Idea 12 — vol-target (RULES v1 weights scaled to a constant portfolio vol)

Script: `research/backtests/2026-09-03_vol-target.py` · Costs 10 bps · freq="W" · sample 2009-01-13 → 2026-09-03 (56 tickers, 260-day warm-up skipped)

## LEADERBOARD rows

| Date | Idea | CAGR | Sharpe | MaxDD | Sharpe H1 / H2 | Baseline Sharpe (H1/H2) | Verdict | Script |
|---|---|---|---|---|---|---|---|---|
| 2026-09-03 | vol-target 10% | 5.8% | 0.59 | -14.9% | 0.59 / 0.58 | 0.67 (0.64/0.69) | KILL | research/backtests/2026-09-03_vol-target.py |
| 2026-09-03 | vol-target 14% | 6.9% | 0.60 | -15.3% | 0.60 / 0.61 | 0.67 (0.64/0.69) | KILL | research/backtests/2026-09-03_vol-target.py |

Reference rows printed by `compare()` in the same run: RULES v1 baseline CAGR 6.5%, Sharpe 0.668, MaxDD -13.8%, H1/H2 0.645/0.692; SPY CAGR 15.3%, Sharpe 0.890, MaxDD -33.7%, H1/H2 0.957/0.837.

## Memo

1. Tested: RULES v1 (equal-weight top 5, 75% gross) with the entire weight row multiplied each day by target_vol / trailing-20d annualized vol of the *unscaled v1 strategy's own* daily returns, lagged one day (no look-ahead), capped at 100% gross (no leverage). Two grid points: 10% and 14% target vol.
2. Mechanics caveat stated up front: the scale factor moves daily but the engine only rebalances weekly, so the book adopts whichever scale is in force at each weekly rebalance and then drifts — realistic, and it is what was measured.
3. Sharpe, full sample: 0.586 (10% target) and 0.603 (14% target) vs 0.668 for the RULES v1 baseline and 0.890 for SPY. Both variants lose to the baseline outright.
4. Both halves: 10% target 0.594 / 0.578 vs baseline 0.645 / 0.692; 14% target 0.600 / 0.608 vs the same baseline. The variants lose in H1 **and** H2 — no half is rescued, so this is not a regime-specific failure.
5. MaxDD: -14.9% (10%) and -15.3% (14%) vs -13.8% baseline. Drawdown is *worse* for both, so the risk-control rationale for vol targeting does not show up either. (SPY -33.7%.)
6. Average gross exposure achieved: 80.4% at the 10% target and 93.3% at the 14% target, vs 74.9% for the baseline — i.e. vol targeting is on net a **lever-up**, not a de-risk, for this book. Gross ranged 23.8%–100% (10%) and 33.3%–100% (14%).
7. The cap binds a lot: the 100% gross cap is active on 31.9% of days at the 10% target and 67.3% of days at the 14% target. The baseline's own realized vol is 10.2% full-sample with a median trailing-20d vol of 9.0% (below 10% on 61.7% of days, below 14% on 88.6% of days), so the target is above realized vol most of the time and the rule mostly asks for leverage it is not allowed to take.
8. Verdict per PROTOCOL rule 4: **KILL** for both grid points. KEEP-candidate requires Sharpe above baseline in BOTH halves and MaxDD no worse; neither variant clears either condition (Sharpe lower in both halves, MaxDD deeper).
9. Risks/caveats: the effect is asymmetric and path-dependent — when the cap is not binding the rule cuts exposure precisely after a vol spike, i.e. it sells into the post-drawdown recovery, which is the most plausible source of the worse MaxDD alongside the lower Sharpe. Weekly rebalancing also means the scale actually traded is a stale sample of a daily signal; a daily-rebalance version would trade more and pay more cost, and was not tested.
10. Other caveats: only 2 grid points and one lookback (20d) were tested, so this is not an exhaustive search of the vol-targeting family — but the mechanism failure (target above realized vol → cap binds → mostly just more gross) argues the family is a poor fit for an already low-vol, 75%-max, long-only book rather than that this particular tuning was unlucky. Costs are unchanged at 10 bps; scaling adds turnover at each weekly rebalance, which is included in these numbers. No parameter was re-tuned after seeing results.

# Idea 17 — broad-momentum-top10 (RULES v1 selection on the ~136-name broad universe)

Script: `research/backtests/2026-09-03_broad-momentum-top10.py` · Costs 10 bps · freq="W" · next-day execution · sample 2009-01-13 → 2026-09-02 (broad universe: 136 tickers requested, 135 usable — MMC failed to download and stays all-NaN, so it is never selectable; 260-day warm-up skipped).

Selection logic is unchanged RULES v1: `baseline.score` composite (12-1 momentum + 6m + 3m, cross-sectional percentile ranks, halved when below the 200d MA, divided by sqrt(vol20)), eligibility = price > 200d MA **and** vol20 < 0.60, equal weight on the top N.

## LEADERBOARD rows

| Date | Idea | CAGR | Sharpe | MaxDD | Sharpe H1 / H2 | Baseline Sharpe (H1/H2) | Verdict | Script |
|---|---|---|---|---|---|---|---|---|
| 2026-09-03 | broad-top10 100% gross (N=10,w=10%) | 8.6% | 0.67 | -22.1% | 0.86 / 0.51 | 0.64 (0.78/0.53) | KILL | research/backtests/2026-09-03_broad-momentum-top10.py |
| 2026-09-03 | broad-top20 100% gross (N=20,w=5%) | 11.5% | 0.86 | -22.9% | 1.09 / 0.66 | 0.64 (0.78/0.53) | KILL | research/backtests/2026-09-03_broad-momentum-top10.py |
| 2026-09-03 | broad-top10 75% gross (N=10,w=7.5%) | 6.6% | 0.67 | -16.8% | 0.86 / 0.51 | 0.64 (0.78/0.53) | KILL | research/backtests/2026-09-03_broad-momentum-top10.py |

**Read the baseline column carefully.** `compare()` computes its baseline on whatever `px` it is handed, so the "0.64 (0.78/0.53)" above is **RULES v1 run on the broad universe**, not the live book. The live book was run separately in the same script on the standard universe:

| Date | Idea | CAGR | Sharpe | MaxDD | Sharpe H1 / H2 | Baseline Sharpe (H1/H2) | Verdict | Script |
|---|---|---|---|---|---|---|---|---|
| 2026-09-03 | RULES v1 LIVE (standard universe) — reference, not a new idea | 6.4% | 0.66 | -13.8% | 0.65 / 0.68 | 0.66 (0.65/0.68) | — | research/backtests/2026-09-03_broad-momentum-top10.py |

Other reference rows from the same run: **RULES v1 on the broad universe** CAGR 6.5%, Sharpe 0.644, MaxDD -21.2%, H1/H2 0.779/0.528. **SPY** CAGR 15.2%, Sharpe 0.887, MaxDD -33.7%, H1/H2 0.957/0.831.

Exposure / trading diagnostics (post-warm-up): avg gross 99.6% / 98.9% / 74.7% and annualized turnover 31.6x / 23.8x / 23.7x for top10-100%, top20-100%, top10-75% respectively. Eligible names per day on the broad universe: mean 91.4, min 3, max 128; fewer than 10 eligible on 1.0% of days and fewer than 20 on 2.5% of days (so N=20 is occasionally under-filled in crises, which de-risks by construction).

## Walk-forward (PROTOCOL rule 8) — parameters chosen on 2009-01-13 → 2016-12-30, evaluated 2017-01-03 → 2026-09-02

| Series | IS Sharpe | IS MaxDD | IS CAGR | **OOS Sharpe** | **OOS MaxDD** | OOS CAGR |
|---|---|---|---|---|---|---|
| broad-top10 100% gross (N=10,w=10%) | 0.789 | -12.7% | 9.9% | 0.583 | -22.1% | 7.5% |
| **broad-top20 100% gross (N=20,w=5%)** ← selected | **1.003** | -12.4% | 13.2% | **0.747** | **-22.9%** | 10.2% |
| broad-top10 75% gross (N=10,w=7.5%) | 0.789 | -9.6% | 7.5% | 0.584 | -16.8% | 5.8% |
| RULES v1 on broad universe (baseline A) | 0.720 | -9.7% | 7.0% | 0.587 | -21.2% | 6.1% |
| RULES v1 LIVE, standard universe (baseline B) | 0.558 | -13.1% | 5.0% | 0.743 | -13.8% | 7.7% |
| SPY | 0.899 | -22.1% | 15.0% | 0.879 | -33.7% | 15.4% |

Selection used **IS Sharpe only** and picked N=20, w=5%. OOS it beats baseline A (0.747 vs 0.587) but is a dead heat with the live book B (0.747 vs 0.743) while running 100% gross instead of 75% and taking a 1.7x deeper drawdown (-22.9% vs -13.8%). It loses to SPY on both Sharpe and drawdown-adjusted terms.

## Memo

1. **What was tested:** identical RULES v1 selection maths, only the universe and (N, w) changed — 135 usable broad names instead of 56, equal-weight top N, weekly rebalance, 10 bps, next-day fills. Two tuned parameters (N and w), and w is pinned by the gross-exposure target rather than searched, so effectively one free parameter.
2. **Full-sample result:** top20-100% is the standout (CAGR 11.5%, Sharpe 0.858) and beats v1-on-broad in both halves (1.087/0.660 vs 0.779/0.528), but its MaxDD is -22.9% vs the baseline's -21.2%. Rule 4 requires MaxDD **no worse**, so the mechanical verdict is KILL.
3. **My rule-4 call, stated separately from the mechanical one:** top10-100% = **KILL** (loses H2 to baseline A, 0.512 vs 0.528, and drawdown is worse); top10-75% = **KILL** (also loses H2, 0.513 vs 0.528, by a hair, and loses badly to the live book's 0.682); top20-100% = **PARK**, not KEEP — it wins both halves and OOS against baseline A, but fails the MaxDD condition by 1.7pp and, more importantly, fails the comparison that actually matters (see 4).
4. **The comparison that matters is against the live book, not against v1-on-broad.** At matched 75% gross, going broad is a wash-to-worse: top10-75% Sharpe 0.672 vs the live 0.663 full sample, but 0.584 vs 0.743 out of sample. Nearly all of the top20 headline is exposure (100% vs 75%) plus breadth, not a better signal.
5. **Walk-forward (rule 8):** the choice made blind on 2009–2016 (N=20) did carry OOS in relative terms — 0.747 vs 0.587 for baseline A — so the improvement over v1-run-on-broad is not purely in-sample. But OOS Sharpe against the live book is +0.004, i.e. nothing, and OOS MaxDD is 9.1pp worse. Rule 8's own language: an idea that only wins in-sample is PARK; this one barely wins out-of-sample either, so PARK is the ceiling.
6. **Where the broad-universe edge actually comes from:** breadth in the *baseline itself* is worse (v1-on-broad has a -21.2% MaxDD vs -13.8% for v1-on-standard, and a much worse H2), because the broad list is far more single-stock-heavy and less ETF-cushioned than the standard universe. So the top20 "beat" is partly measured against a weakened yardstick.
7. **Costs and capacity:** 23.8x annual turnover at N=20 and 31.6x at N=10 (100% gross) are high; at 10 bps that is roughly 24–32 bps/yr of modeled cost. Doubling the cost assumption to 20 bps would remove ~0.24–0.32%/yr of CAGR — enough to matter for the exposure-matched variant, not enough to flip top20's ranking against baseline A.
8. **Survivorship bias, stated explicitly per rule 9:** `research/universe_broad.json` is a list of *today's* liquid US large caps and ETFs, so every name in it survived and mostly thrived over 2009–2026 — the direction is unambiguously to overstate returns, plausibly on the order of 1–2%/yr of CAGR for a current-constituent large-cap list over this span, and the overstatement is larger for a concentrated top-10 momentum sleeve (which can only concentrate into known winners) than for the diversified top-20 or for the ETF-heavy standard universe.
9. **What that bias does to the conclusion:** because both the idea and baseline A share the same biased universe, the *relative* broad-vs-broad comparison is roughly bias-neutral, but the cross-universe comparison (broad idea vs the live standard-universe book, which is the decision at hand) is biased *in the idea's favour* — which makes the observed OOS tie with the live book weaker than it looks, and reinforces PARK over KEEP.
10. **Verdict:** **KILL** for (N=10, w=10%) and (N=10, w=7.5%); **PARK** for (N=20, w=5%) — the leaderboard row carries `compare()`'s mechanical KILL because of the MaxDD condition. Nothing here justifies a rules change. What would move it: N=20 at 75% gross (untested here — the grid was specified as three points and was not extended after seeing results), a survivorship-clean or point-in-time universe, and a drawdown-control overlay to fix the one condition it fails. No parameter in this run was re-tuned after seeing results.

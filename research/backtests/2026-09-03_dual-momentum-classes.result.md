# Idea 5 — dual-momentum-classes (Antonacci-style Global Equities / Dual Momentum)

Script: `research/backtests/2026-09-03_dual-momentum-classes.py`
Sample: 2009-01-15 → 2026-09-03 (prices loaded from 2008-01-01, first 260 rows dropped as warm-up)
Universe traded: SPY, EFA, EEM, TLT, GLD, DBC (risky) + SHY (risk-free proxy); zero weight on all other universe tickers.
Costs: 10 bps per unit turnover. Weights decided at close t, applied t+1. Baseline = RULES v1 weekly.

## LEADERBOARD rows (all 4 variants)

| Date | Idea | CAGR | Sharpe | MaxDD | Sharpe H1 / H2 | Baseline Sharpe (H1/H2) | Verdict | Script |
|---|---|---|---|---|---|---|---|---|
| 2026-09-03 | dual-momentum-classes K=1 monthly | 8.7% | 0.54 | -33.8% | 0.36 / 0.69 | 0.67 (0.64/0.69) | KILL | 2026-09-03_dual-momentum-classes.py |
| 2026-09-03 | dual-momentum-classes K=1 weekly | 5.7% | 0.40 | -36.1% | 0.13 / 0.61 | 0.67 (0.64/0.69) | KILL | 2026-09-03_dual-momentum-classes.py |
| 2026-09-03 | dual-momentum-classes K=2 monthly | 7.1% | 0.57 | -24.1% | 0.39 / 0.72 | 0.67 (0.64/0.69) | KILL | 2026-09-03_dual-momentum-classes.py |
| 2026-09-03 | dual-momentum-classes K=2 weekly | 6.9% | 0.56 | -25.7% | 0.29 / 0.80 | 0.67 (0.64/0.69) | KILL | 2026-09-03_dual-momentum-classes.py |

Reference: RULES v1 baseline 6.5% CAGR / 0.67 Sharpe / -13.8% MaxDD (H1 0.64, H2 0.69); SPY 15.3% CAGR / 0.89 Sharpe / -33.7% MaxDD (H1 0.96, H2 0.84).
Avg annual turnover: K=1 M 6.6x, K=1 W 14.3x, K=2 M 5.1x, K=2 W 11.5x.

## Memo

1. Tested: rank SPY/EFA/EEM/TLT/GLD/DBC by 12m total return (px/px.shift(252)-1), hold the top K equal-weight, and park any selected sleeve whose 12m return fails to beat SHY's into SHY instead; K=1 and K=2 x monthly and weekly rebalance, 4 runs, 10 bps.
2. Sharpe vs RULES v1 baseline: every variant loses on the full sample (0.40-0.57 vs 0.67) and, decisively, in the first half (0.13-0.39 vs 0.64); the second half is roughly a coin flip (0.61-0.80 vs 0.69, with K=2 weekly at 0.80 and K=2 monthly at 0.72 nominally ahead).
3. Sharpe vs SPY: all four variants are far behind SPY (0.89) in both halves, and CAGR is 5.7-8.7% against SPY's 15.3% — the defensive overlay cost most of the equity risk premium over this bull-heavy sample.
4. MaxDD: -33.8% / -36.1% (K=1) and -24.1% / -25.7% (K=2) versus the baseline's -13.8%. Every variant is materially worse than the baseline; K=1 is no better than simply owning SPY (-33.7%), which defeats the whole purpose of an absolute-momentum crash filter.
5. The worst drawdown is not 2008-style equity risk: the K=1 monthly peak-to-trough runs 2022-06-09 to 2023-11-10, driven by being locked long DBC on trailing 12m momentum straight through the commodity collapse, then whipsawing across GLD/EFA/SPY in 2023.
6. Turnover impression: monthly is the honest form (5-7x/yr, ~30 position changes over the sample) and weekly roughly doubles it (11-14x/yr) while making results strictly worse — the extra trading buys nothing but cost and whipsaw, confirming the canonical monthly cadence is not an artifact.
7. K=2 dominates K=1 on every risk measure (higher Sharpe, ~10pp shallower MaxDD) at lower turnover; concentration into a single sleeve is the main source of pain, not the dual-momentum logic itself.
8. Verdict per PROTOCOL rule 4: **KILL** for all four variants. KEEP requires Sharpe above baseline in BOTH halves and MaxDD no worse; no variant clears the H1 hurdle (best is 0.39 vs 0.64) and no variant clears the MaxDD hurdle. Not even a PARK: the failure is structural (single-sleeve concentration plus a slow 12m signal), not a tuning gap.
9. Risks/caveats: only ~17.6 years and one regime shape (a long post-GFC equity bull with two commodity round-trips), so the H1/H2 split is more about 2009-2017 vs 2018-2026 macro than about strategy stability; sample starts 2009 so the 2008 crash that makes dual momentum look good in the literature is excluded by the warm-up. ETF inception is not a binding constraint here (DBC 2006, EEM 2003, GLD 2004, EFA 2001, TLT/SHY 2002 all predate the 2008 load date), and the 7 ETFs are survivorship-clean, but the wider universe file is a present-day list.
10. Not tuned further on purpose (PROTOCOL rule 7): only the canonical 12m lookback was used and K was reported at both values rather than searched. Searching lookback or adding a trend filter would likely lift the numbers and would be exactly the overfitting the protocol forbids.

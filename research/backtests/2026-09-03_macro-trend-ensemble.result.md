# Idea 18 — macro-trend-ensemble (time-series momentum, MOP/HOP style, inverse-vol risk parity)

Script: `research/backtests/2026-09-03_macro-trend-ensemble.py` · Costs 10 bps · freq="W" · price panel = `baseline.load_universe()` (56 tickers, 2008-01-02 → 2026-09-02), eval sample 2009-01-13 → 2026-09-02 after the 260-day warm-up `compare()` skips.

Sleeve (9 tickers, everything else weight 0): SPY, QQQ, IWM, EFA, EEM, TLT, GLD, DBC, UUP.
Vote v ∈ {0, 1/3, 2/3, 1}; position = v × inverse-60d-vol weight normalized so a fully-long book is exactly 100% gross; remainder cash. Variant A votes on price > {50, 100, 200}d MA. Variant B votes on sign of {12-1 momentum, 6m return, 3m return}.

## LEADERBOARD rows

| Date | Idea | CAGR | Sharpe | MaxDD | Sharpe H1 / H2 | Baseline Sharpe (H1/H2) | Verdict | Script |
|---|---|---|---|---|---|---|---|---|
| 2026-09-03 | macro-trend-ensemble A (MA votes) | 4.7% | 0.83 | -9.2% | 0.69 / 0.98 | 0.66 (0.65/0.68) | KEEP-candidate | research/backtests/2026-09-03_macro-trend-ensemble.py |
| 2026-09-03 | macro-trend-ensemble B (momentum votes) | 5.0% | 0.87 | -10.1% | 0.75 / 0.98 | 0.66 (0.65/0.68) | KEEP-candidate | research/backtests/2026-09-03_macro-trend-ensemble.py |

Reference rows printed by `compare()` in the same run: RULES v1 baseline CAGR 6.4%, Sharpe 0.663, MaxDD -13.8%, H1/H2 0.646/0.682; SPY CAGR 15.2%, Sharpe 0.887, MaxDD -33.7%, H1/H2 0.957/0.831. (H1/H2 here are `compare()`'s equal-row halves, i.e. the break falls in late 2017 — not the calendar split below.)

## Walk-forward periods (PROTOCOL rule 8) — no parameters tuned, so 2009-2016 is reported straight

| Strategy | Period | CAGR | Vol | Sharpe | MaxDD |
|---|---|---|---|---|---|
| macro-trend-ensemble A (MA votes) | 2009-2016 | 3.2% | 6.1% | 0.553 | -9.2% |
| macro-trend-ensemble A (MA votes) | 2017-2026 | 5.9% | 5.4% | **1.087** | -6.6% |
| macro-trend-ensemble B (momentum votes) | 2009-2016 | 3.6% | 6.0% | 0.614 | -8.6% |
| macro-trend-ensemble B (momentum votes) | 2017-2026 | 6.2% | 5.7% | **1.084** | -10.1% |
| RULES v1 baseline | 2009-2016 | 5.0% | 9.5% | 0.558 | -13.1% |
| RULES v1 baseline | 2017-2026 | 7.7% | 10.7% | 0.743 | -13.8% |
| SPY | 2009-2016 | 15.0% | 17.2% | 0.899 | -22.1% |
| SPY | 2017-2026 | 15.4% | 18.2% | 0.879 | -33.7% |

## Average gross exposure

| Book | Full sample | 2009-2016 | 2017-2026 |
|---|---|---|---|
| macro-trend-ensemble A | 64.2% | 61.2% | 66.8% |
| macro-trend-ensemble B | 65.9% | 62.4% | 68.9% |
| RULES v1 baseline | 74.9% | 75.0% | 74.9% |

A: median gross 65.5%, range 0.0%–100.0%, below 25% on 1.9% of days, above 90% on 5.2%; 6.97 of the 9 assets carry some weight on an average day; annual turnover 6.4x.
B: median gross 67.7%, range 21.9%–100.0%, below 25% on 1.0% of days, above 90% on 3.7%; 7.72 assets on an average day; annual turnover 4.6x.
Average weight per asset (A / B, % of NAV): SPY 8.96/9.29, QQQ 7.17/7.50, IWM 5.61/5.69, EFA 6.86/6.83, EEM 4.87/4.95, TLT 6.16/6.51, GLD 6.58/6.84, DBC 5.01/4.80, UUP 13.02/13.52.

## Memo

1. Tested: a 9-asset macro TSMOM sleeve with a 3-signal trend vote in {0, 1/3, 2/3, 1} scaled by inverse-60d-vol risk-parity weights that sum to 100% when every vote is long; two vote definitions (A = 50/100/200d MAs, B = 12-1/6m/3m momentum signs), weekly rebalance, 10 bps, long-only, no leverage, zero weight on the 47 non-sleeve tickers in the panel.
2. Both variants clear PROTOCOL rule 4 outright: Sharpe 0.827 (A) and 0.865 (B) vs 0.663 for RULES v1, above baseline in **both** `compare()` halves (A 0.688/0.979, B 0.753/0.979 vs 0.646/0.682), MaxDD shallower (-9.2% / -10.1% vs -13.8%), and zero tuned parameters — the 50/100/200, 12-1/6m/3m and 60d-vol lookbacks are the canonical values from Moskowitz-Ooi-Pedersen and Hurst-Ooi-Pedersen, not fitted here. Verdict: **KEEP-candidate for both.**
3. Rule 8 walk-forward: since nothing was fit on 2009-2016, the honest test is the untouched 2017-2026 leg, and both variants win it decisively — Sharpe 1.087 (A) and 1.084 (B) vs baseline 0.743, with MaxDD -6.6% / -10.1% vs -13.8%. This is not an in-sample-only result, so neither drops to PARK on rule 8.
4. One blemish worth naming: on the *calendar* 2009-2016 leg variant A's Sharpe is 0.553 against the baseline's 0.558 — a dead heat that A technically loses. It clears rule 4 only because `compare()`'s equal-row halves break in late 2017, not at year-end 2016. B (0.614 vs 0.558) wins on both definitions, so B is the cleaner of the two.
5. The edge is risk reduction, not return: both variants earn *less* than the baseline (CAGR 4.7% / 5.0% vs 6.4%) and far less than SPY (15.2%), on roughly half the volatility (5.7% / 5.9% vs 10.2% and 17.7%). Anyone judging this on terminal wealth will hate it — $1 grows to $2.23 / $2.37 vs $3.00 baseline and $12.06 for SPY over 17.6 years.
6. Where it pays off is the tails: Sortino 1.05 / 1.08 vs 0.84 baseline, and in 2022 the sleeve lost only 0.4% (A) and 2.5% (B) while SPY lost 18.2%. It also barely participates in melt-ups (2020: +6.2% / +4.8% vs SPY +18.3%). The cost of the smooth ride is a persistent drag in trending-up equity years.
7. Concentration caveat that bothers me most: inverse-vol over an unhedged macro basket hands the largest average weight to UUP (13.0% / 13.5% of NAV), the lowest-vol and most cash-like member of the sleeve. A meaningful slice of the "risk parity" allocation is effectively a dollar-cash position, which mechanically flatters Sharpe and depresses CAGR. The result is partly an artifact of the sizing rule, not purely of the trend signal.
8. Diversification vs the live book is real but incomplete: correlation to RULES v1 is 0.686 (A) and 0.727 (B), to SPY 0.512 / 0.635. A and B correlate 0.901 with each other — they are two views of one idea, not two ideas, so do not count them as independent evidence.
9. Other caveats: only two variants and one sizing rule were run, and the sleeve was chosen a priori (9 liquid macro ETFs) rather than searched, which limits selection bias but also means no sensitivity testing was done — a 20/60/120d MA set or a 20d vol window was never tried, so the reported robustness is "not tuned", not "shown stable". UUP and DBC only start in 2006-2007, so the sleeve cannot be pushed back before 2008; the sample contains one genuine bear regime for macro trend (2022) and one crisis tail (2020), which is thin evidence for a strategy whose whole claim is crisis behavior. Turnover of 6.4x/4.6x a year at 10 bps is already in the numbers; real spreads on DBC and UUP are wider than SPY's and are not modeled per-ticker.
10. Recommendation: promote **B** to KEEP-candidate for a Sunday-review discussion as a low-vol satisfier / possible diversifier to RULES v1, and hold **A** at KEEP-candidate-with-an-asterisk given its 2009-2016 dead heat. Before any rules change, the next test should be (a) an equal-weight version of the sleeve to isolate how much of the Sharpe is the trend vote vs the inverse-vol-into-UUP tilt, and (b) a blended book (RULES v1 + sleeve) to see whether the diversification survives being mixed rather than compared. No leaderboard file was modified in this run (per task instruction); the rows above are ready to append.

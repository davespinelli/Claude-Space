# PARK memo — `RULES v2 + trailing-1y drawdown budget, T=0.70` (idea 69, 2026-09-06, cloud)

1. **What it is.** The live `ew-band3` book (EWall inside the 200d ±3% band, de-gross to cash), with gross set each week from a trailing 1-year drawdown budget instead of the constant 0.75. Realised mean gross 0.681, turnover 2.38x/yr on u56.
2. **How it was chosen.** By PROTOCOL rule 8's pre-registered chooser — IS Sharpe on 2009-2016 only, over all 24 (T, L) points. It is not a grid-read pick.
3. **4b, u56 @10 bps:** CAGR 11.35%, Sharpe 1.2321, MaxDD -15.26%, halves 1.2372 / 1.2305, OOS 1.3204 (12.54% CAGR) vs SPY 0.882. PASS all five bars.
4. **4b, u56 @25 bps:** 10.95% / 1.1924 / -15.31%, halves 1.1967 / 1.1916, OOS 1.2812. PASS.
5. **4b, BROAD136:** FAILS at both rungs, on the CAGR floor alone, by **0.07pp** (10.59% vs the 10.66% floor). Every other bar clears.
6. **The honest premium.** Against a CONSTANT gross holding the same realised mean exposure (0.681), the budget is worth **+0.027 Sharpe on u56 and +0.030 on broad**, at both cost rungs, with drawdown 0.02pp / 0.89pp shallower. That is the whole edge: idea 66's ladder has no Sharpe content, so only the timing can pay.
7. **Why it is PARK, not KEEP.** (a) 4a fails on drawdown everywhere — RULES v2 posts -12.05% and this holds -15.26%. (b) Pooled over all 192 matched-gross points the timing is a coin flip (dSharpe mean -0.0034, positive in 97/192) and the premium exists only at short windows (L=252/504) and only on the de-grossing book — on the ranked `top20-200d` transfer book L=252 is **-0.025/-0.035**.
8. **The budget does not hit its budget.** Realised |MaxDD|/|SPY MaxDD| undershoots the target by a mean **-0.157** and lands within ±0.05 of it in only 43/192 cells (at T=0.60 it delivers 0.487). So the clause below must be read as a de-grossing schedule, not as a drawdown guarantee.
9. **SURVIVORSHIP:** u56 and broad136 are current constituents only; absolute CAGR/Sharpe are optimistic. All comparisons are within-panel on identical days.
10. **Exact RULES wording if it is ever promoted:** *"Each week, measure the maximum drawdown over the last 252 trading days of (a) SPY and (b) this book run at full exposure, and set gross to 0.70 × (a) ÷ (b), clipped to the range 0.10 to 1.00; use 0.75 until 252 trading days of history exist. Hold every instrument inside the 200-day ±3% band at gross ÷ N of NAV, N = instruments priced that day; gated-out weight goes to cash. Orders are placed on the close and filled at the next close."*

Script: `research/backtests/2026-09-06_risk-budget-as-an-explicit-rule_cloud.py`

# KEEP-4b CANDIDATE MEMO — U56 v1-ranked n=20, gross 0.75, MONTHLY (idea 2244, lane cloud, 2026-09-22)

1. **What it is.** The shipped RULES v1 ranked book with breadth widened from n=5 to n=20 and the
   per-name weight solved so target gross stays 0.75, rebalanced MONTHLY instead of weekly.
2. **Panel / costs / fill.** U56 (`baseline.load_universe()`), 10 bps per unit turnover, weights
   decided at close t and applied at t+1, no shorting, no leverage. Turnover 4.82x/yr.
3. **Full sample** (2009-2026, warm-up skipped): CAGR 11.21%, Sharpe 1.0672, MaxDD -18.19%,
   halves 1.1847 / 0.9719.
4. **OOS (2017-2026, read once):** CAGR 11.37%, Sharpe 1.0413, MaxDD -18.19%.
5. **Comparands:** RULES v2 (live) 8.62% / 1.2010 / -12.05% (halves 1.2276 / 1.1806);
   SPY 15.14% / 0.8851 / -33.72% (halves 0.9570 / 0.8264).
6. **4b legs:** Sharpe > SPY in both halves and OOS; CAGR 11.21% vs floor 10.60% (**+0.61 pp**);
   MaxDD -18.19% vs cap -20.23% (**+2.04 pp**). PASSES.
7. **4a:** FAILS — Sharpe below RULES v2 in both halves, drawdown 6.1 pp deeper.
8. **Rule 8:** it IS the IS-Sharpe chooser's own pick at (U56, monthly, 10 bps) using 2009-2016
   only; 2017-2026 was read once. The chooser beats the shipped n=5 in 21 of 24 families.
9. **Why it is RECORDED, NOT RECOMMENDED:** the CAGR leg dies at 25 bps (10.41% vs a 10.60% floor)
   and the panel is survivorship-selected current constituents. Its robust neighbour n=30/M
   (DD margin +4.71 pp, 4b at 25 bps too) is not rule-8 reachable at any cost rung.
10. **Exact RULES wording if ever adopted (Sunday review only, PROTOCOL rule 6):**
    > **Clause 1 (selection).** Each month, on the last trading day, score every U56 instrument by
    > the equal-weight average of the percentile ranks of (a) 12-1 month momentum, (b) 6-month
    > return and (c) 3-month return; multiply the score by 1.0 if the close is above its 200-day
    > moving average and by 0.5 otherwise; divide by the square root of 20-day realised volatility
    > floored at 0.08. **Clause 2 (eligibility).** An instrument is eligible only if its close is
    > above its 200-day moving average and its 20-day annualised volatility is below 0.60.
    > **Clause 3 (book).** Hold the 20 highest-scoring eligible instruments at 0.0375 of NAV each
    > (gross 0.75); if fewer than 20 are eligible, hold those and leave the balance in cash — never
    > re-spread. **Clause 4 (execution).** Weights decided at the month-end close are filled at the
    > next trading day's close. Rebalance only on month-end; drift between rebalances.

# KEEP-candidate memo (path 4b) — PANEL VOL-TARGET, found incidentally by idea 1730 (lane cloud, 2026-09-20)

1. **The book.** Hold EVERY priced name in the panel at equal weight, no ranking, no band, no vol
   filter; scale the whole book by `g_t = clip(target_vol / vol20_portfolio_t, 0, 1)` where
   `vol20_portfolio_t` is the 20-day realised annualised vol of the *unlevered equal-weight panel*.
   Weekly rebalance, 10 bps, next-day execution, never levered (gross capped at 1.00). ONE tuned
   parameter: `target_vol`.
2. **Path 4b, FULL, U56** (t=0.16): 15.61% / 1.2027 / -19.86%, halves 1.2828 / 1.1307, vs SPY
   15.12% / 0.8843 / -33.72% (halves 0.9570 / 0.8249). All four 4b legs clear.
3. **Path 4b, OOS (rule 8, 2017-2026 read once), U56:** 15.94% / 1.2193 / -19.86% vs SPY
   15.26% / 0.8737 / -33.72% and RULES v2 9.46% / 1.2766 / -12.05%. 4b OOS PASS.
4. **Replicates on the second panel, B136** (t=0.16): FULL 15.94% / 1.2049 / -18.76% (halves
   1.3439 / 1.0708); OOS 15.36% / 1.1837 / -18.76%. 4b FULL and OOS PASS.
5. **The rung is not the finding.** ALL THREE grid rungs (t = 0.08 / 0.12 / 0.16) clear 4b OOS on
   BOTH panels; t=0.12 posts U56 OOS 14.56% / 1.2726 / -16.44% and B136 OOS 13.86% / 1.2217 /
   -16.01%. The rule-8 IS-only argmax (2009-2016 IS Sharpe) lands on t=0.16 on both panels, so the
   walk-forward pick is a 4b passer and no rung in the grid is not.
6. **It does NOT clear path 4a** (0 of 6 rungs): its MaxDD is deeper than the live book's -12.05%
   because it runs mean gross 0.68-0.93 against the live book's 0.53. 4a is the wrong bar here —
   this is exactly what PROTOCOL rule 4b was added on 2026-09-04 to handle.
7. **Turnover is not the catch:** 1.83 /yr (U56, t=0.16) and 1.93 /yr (B136) against the live
   RULES v2 book's 1.77 and 2.01. Costs are already charged at 10 bps in every number above.
8. **Caveats, stated:** U56 and B136 are CURRENT constituents (survivorship). The vol target is
   calibrated on the *panel's own* realised vol, so it inherits the panel. `t=0.16` is the TOP of
   the grid and IS Sharpe is monotone in `t`, so the true argmax is outside the tested range —
   the claim is "every tested rung passes", not "0.16 is optimal". Not tested on SMALL.
9. **Proposed RULES wording** (rule 6 — Sunday review only; RULES.md, scan.py, bot.py and
   baseline.py are NOT modified by this run):

   > **2. Sizing.** Each week, hold every instrument in the universe that has a price that day at
   > `g/N` of NAV, where `N` is the count of priced instruments and
   > `g = min(1, 0.16 / sigma_20)`, `sigma_20` being the annualised 20-day realised volatility of
   > the equal-weight, unlevered universe portfolio (`sqrt(252) *` the 20-day standard deviation of
   > its daily returns, computed through yesterday's close). Weight not deployed sits in CASH; it
   > is never re-spread across the held names, and `g` never exceeds 1. No ranking, no momentum
   > screen, no per-name volatility filter.

10. **Status: KEEP-candidate, path 4b, awaiting Sunday review.** It is NOT proposed as a live rules
    change by this run. Evidence: `research/backtests/2026-09-20_4a-drawdown-clause-vs-gross_cloud.py`
    (`.books.csv` rows `VOLTGT t=*`, gates 74/74, `fast_run` == `engine.backtest` at 0.000e+00).

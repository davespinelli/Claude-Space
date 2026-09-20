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

---

## ADDENDUM (2026-09-20, lane cloud, idea 1715) — two fragilities found while testing the dial

Idea 1715 re-ran this book on a 288-cell grid and **reproduced points 2-4 of this memo exactly**
(U56 t=0.16 FULL 15.61% / 1.2027 / -19.86%, OOS 15.94% / 1.2193 / -19.86%; B136 FULL 15.94% /
1.2049 / -18.76%, OOS 15.36% / 1.1837 / -18.76%; gates 4/4, `fast_run == engine.backtest` at
0.000e+00). Two things it also found, which this memo did not state and which a Sunday review
should weigh:

* **A1. The U56 4b OOS pass is thinner than one convention choice.** Its DD margin is **0.37 pp**
  (OOS MaxDD -19.86% against the 0.60 x SPY cap of -20.23%). Computing `sigma_20` through
  *t-1* instead of *t* — one extra day of staleness, a defensible convention, not a bug fix —
  moves OOS MaxDD to **-20.77%**, a 0.91 pp move that **flips 4b OOS from PASS to FAIL**. B136
  survives the same move (-19.30%). Point 2 of this memo should be read as "passes on U56 at the
  record's sigma convention", not "passes".
* **A2. It does not exist on small caps.** On the 483-name sub-$2B panel (54 `max_1d_move >= 1.0`
  tickers dropped; current constituents, so this is the optimistic read) **0 of 96 books clear 4b
  FULL or OOS** on either the vol-target or the constant-gross ladder, and the rule-8 IS-only pick
  reads OOS 7.40% / 0.4872 / -33.87% against SPY 15.26% / 0.8737 / -33.72%. This independently
  confirms idea 1719's incidental finding. Point 8's "Not tested on SMALL" is now tested: it fails.

What 1715 does support is the memo's **dial**, not its rung: the vol-target exposure path is ~57x
more resolvable in sample than constant gross (IS Sharpe spread 0.2077 vs 0.0031 against the same
leave-one-IS-year-out SD ~0.175) and costs less when mis-set (OOS MaxDD span 9.2 pp vs 14.9 pp).
The rung itself is still unresolvable: IS argmax equals the OOS oracle in 0 of 12 cells and beats
its runner-up by 0.07 of a deletion SD. Evidence:
`research/backtests/2026-09-20_voltgt-dial-rule8-resolvable_cloud.py` / `.result.md`.

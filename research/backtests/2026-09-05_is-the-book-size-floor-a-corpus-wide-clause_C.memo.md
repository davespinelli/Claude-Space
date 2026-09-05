# Memo — idea 209 by-product KEEP-candidate (broad `R6@n=25`). NOT proposed for Sunday review.

1. **What it is.** Broad panel (`universe_broad.json`), top 25 names by 6-month total return
   among RULES-v1-eligible names, equal weight, 75% gross, weekly, next-day execution, 10 bps.
2. **How it was chosen.** Not by inspection: it is the rule-8 pick of the pre-registered floor
   `n >= 25` on IS data (≤ 2016-12-31) alone, then read once on 2017-01-01 →.
3. **Full sample:** 14.1% CAGR / **1.061 Sharpe** / −18.9% MaxDD, halves **1.219 / 0.920**,
   turnover 13.1×/yr.
4. **Out of sample (rule 8):** 13.7% / **1.013** / −18.9%, vs SPY 0.882 / 15.45% / −33.72% and
   RULES v1 (broad @ 10 bps) 0.576 / 5.94% / −21.19%.
5. **KEEP path 4b: PASS on all five bars** — H1 +0.262, H2 +0.086, OOS +0.131, MaxDD −18.9% vs
   the 60%-of-SPY cap at −20.2%, CAGR 14.1% vs the 70% floor at 10.7%.
6. **KEEP path 4a: PASS too** (beats RULES v1 in both halves at a shallower drawdown) — the
   only book in the 384-book corpus to clear both paths outside the `R6` broad ladder itself.
7. **Blocker 1 — costs.** It fails 4b at 25 bps. The idea-178 standing candidate has the same
   blocker; nothing here improves on it.
8. **Blocker 2 — one panel, one key, high turnover.** It exists on broad only, H2 = 0.920 is
   thinner than the standing candidate's 0.971, and 13.1×/yr turnover is above its 10.2×.
9. **Blocker 3 — survivorship (idea 54)** and the calendar-day index (idea 38) both apply; no
   level here is a tradable estimate.
10. **Exact RULES wording if it were ever adopted** (it is not being proposed):
    > *Each Friday close, rank every name in `universe_broad.json` that trades above its 200-day
    > moving average and has 20-day annualised volatility below 0.60 by its 6-month total
    > return. Hold the top 25 at equal weight, 3.00% each (75% gross, 25% cash). Rebalance
    > weekly at the next day's close.*

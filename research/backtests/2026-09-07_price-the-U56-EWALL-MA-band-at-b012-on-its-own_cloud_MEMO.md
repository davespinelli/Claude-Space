# KEEP memo — idea 360, U56 wide-band equal-weight (path 4b)

1. **Candidate.** U56 200d MA band at half-width **b = 0.12** with hysteresis, hold every
   in-band name at **0.75 / k_t** (respread over in-band names), weekly, next-day close.
2. **Numbers @10 bps** (2009-01-13 → 2026-09-04): CAGR **14.02%**, Sharpe **1.2264**,
   MaxDD **−19.42%**, halves **1.2611 / 1.2048**, turnover **1.93×/yr**.
3. **vs SPY:** 15.23% / 0.8890 / −33.72%, halves 0.9566 / 0.8340. 4b bars all pass:
   H1 +0.305, H2 +0.371, OOS +0.384, DD slack 0.81 pp, CAGR slack +3.36 pp.
4. **Rule 8 OOS (2017–2026, chosen on ≤2016):** Sharpe **1.2662**, CAGR **15.16%**,
   MaxDD **−19.42%** vs SPY 0.8820 / 15.45% / −33.72%. Regret vs the OOS-best cell 0.0194.
5. **Breakeven c\* = 123.7 bps** — the 4b pass survives 12× PROTOCOL's cost assumption.
6. **Path 4a: FAIL, 0 of 540 U56 cell-rungs.** Live RULES v2 has a −12.05% MaxDD; nothing
   in this family beats it on drawdown. This is a 4b promotion or nothing.
7. **Not an upgrade on every axis:** RULES v2's OOS Sharpe is higher (1.2851). The trade is
   +5.6 pp of OOS CAGR for +7.4 pp of drawdown. Sunday review must price that exchange.
8. **Grid-edge flag CLEARED:** b=0.12 is the argmax and INTERIOR in 15/15 U56 (g × rung)
   cells on a ladder run to b=0.70. Second local peak at b=0.40 sits 0.045 below.
9. **Does not generalise:** fails 4b on B136 (DD) and on 0/120 SMALL439 cells.
   SURVIVORSHIP: current-constituent panels.
10. **Exact RULES wording if promoted** (replaces v2 clauses 2–3 wholesale, does not tweak
    them): *"Eligibility: a name is IN once its close exceeds its 200-day moving average by
    more than 12%, and stays IN until its close falls more than 12% below that average;
    names are OUT before 200 closes exist. Weights: hold every IN name at 75% of NAV
    divided by the number of IN names that day, rebalanced weekly on the last trading day,
    executed at the next close; the balance is cash. No ranking, no vol filter, no
    momentum score."*

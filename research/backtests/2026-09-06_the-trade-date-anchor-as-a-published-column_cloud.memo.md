# KEEP-candidate memo — MEAN-21 anchor-agnostic monthly R6 top-20 (idea 223, 4b, scoped to universe.json)

1. **What it is.** The standing candidate's book, held on all 21 possible month trade-dates at
   once — 1/21 of capital on each anchor — so no trade date is chosen.
2. **Why it exists.** The identical rule spans 8.85pp of full-sample MaxDD across its 21 anchors
   and passes 4b on only 12 of them; the published anchor's pass is a 12-of-21 statement.
   MEAN-21 removes the dial instead of picking a value on it.
3. **Numbers, u56 @10bps:** 12.84% CAGR / 1.1058 Sharpe / −19.61% MaxDD; halves 1.174 / 1.058;
   OOS (2017-01-01..) 13.95% / 1.1280 / −19.61%; turnover 4.85x/yr. **4b PASS.**
4. **@25bps:** 12.03% / 1.0428 / −19.68%; halves 1.105 / 0.999; OOS 1.0682. **4b PASS.**
5. **Against SPY:** 15.23% / 0.8890 / −33.72% (H1 0.9566, H2 0.8340, OOS 0.8820). Against
   RULES v1: 6.45% / 0.6642 / −13.83%. 4a FAILS on drawdown, as every growth book does.
6. **Free parameters: zero.** Nothing is tuned; the 21 anchors are enumerated, not selected.
   Rule 8 is satisfied by construction — an IS chooser is not used at all.
7. **Scope.** Fails 4b on universe_broad.json at both cost rungs (DD −22.51% / −22.63% against a
   20.23% cap). This is a universe.json-scoped candidate, exactly like its parent (idea 182).
8. **Survivorship.** universe.json is a current-constituent list; the level is not an attainable
   return.
9. **Cost of the insurance:** −1.28pp CAGR and −0.050 Sharpe vs the published anchor on u56@10bps.
10. **Exact RULES wording if adopted:**

> **Rebalance.** Monthly. Split the book into 21 equal tranches. Tranche *k* (k = 0..20)
> rebalances on the *k*-th trading bar after the last trading bar of each calendar month, and
> fills at the next close. Each tranche independently holds the top 20 names by
> `R6 / sqrt(max(vol20, 0.08))` among names above their 200-day moving average with
> `vol20 < 0.60`, equal-weighted at 0.75 gross (cash otherwise). No tranche's schedule is chosen;
> all 21 are held.

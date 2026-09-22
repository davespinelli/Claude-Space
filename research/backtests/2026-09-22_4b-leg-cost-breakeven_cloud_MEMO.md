# KEEP-4b CANDIDATE — idea 2270 (2026-09-22, lane cloud). Recorded, NOT recommended. POST-HOC on cadence.

1. **BOOK.** Idea 2264's standing candidate with ONE clause changed: the live RULES v2 band book
   on U56 at `gross = 1.00`, band 3%, t+1, gated-out weight to cash — rebalanced **MONTHLY**
   instead of weekly.
2. **EXACT RULES WORDING if ever promoted.** *"Clause 3 (position size and cadence). Hold every
   name inside the 200-day ±3% band at `G / N` of NAV, N = instruments priced that day,
   gated-out weight to cash, rebalancing on the last trading day of each calendar MONTH. `G` is
   set once a year on the trailing history available at the time as the largest value on the
   ladder {0.25 … 1.50 step 0.125} whose realised maximum drawdown over that history is no worse
   than 0.60 × SPY's over the same history, capped at 1.00 (PROTOCOL rule 2, no leverage). On the
   2009-2016 history that rule returns `G = 1.00`."*
3. **NUMBERS @10 bps, U56.** FULL 11.90% / 1.1735 / −18.81% (halves 1.2145 / 1.1406),
   OOS 12.82% / 1.2252 / −18.81%. Turnover **1.64×/yr** — BELOW live RULES v2's own 1.77×.
4. **COMPARANDS.** Live RULES v2 (weekly, g = 0.75) FULL 8.62% / 1.2010 / −12.05%,
   OOS 9.46% / 1.2767 / −12.05%, 1.77×/yr. SPY FULL 15.14% / 0.8851 / −33.72% (halves 0.9570 /
   0.8264), OOS 15.29% / 0.8751 / −33.72%. 2264's weekly candidate FULL 11.53% / 1.2009 / −15.91%,
   OOS 12.67% / 1.2760 / −15.91%, 2.35×/yr.
5. **THIS IS THE POINT — COST LIFE.** 4b passes FULL *and* OOS at **0 / 5 / 10 / 25 / 50 bps**,
   the only cell in 6,666 that clears all five. Exact breakevens by leg: `L_CAGR` **81.33 bps**
   (the binder), `L_CAGR_OOS` 124.36, `L_H1` 163.55, `L_H2` 201.29, `L_OOS` 224.67, and
   **`L_DD` / `L_DD_OOS` alive beyond 400 bps**. The weekly candidate dies at 45.79 bps.
6. **WHAT IT PAYS.** Drawdown margin +1.42 pp (−18.81% against the −20.23% cap) against the weekly
   cell's +4.32 pp, and −0.0275 of full-sample Sharpe (1.1735 vs 1.2009). It buys 35.5 bps of cost
   life with 2.90 pp of drawdown margin and 0.71×/yr less turnover.
7. **4a: FAIL.** Against the live WEEKLY book it is Sharpe 1.1735 vs 1.2010 and MaxDD −18.81% vs
   −12.05%. In this run's cadence-matched grid the g = 0.75 cell is an identity by construction and 4a is 0 of 36 non-identity unlevered cells (0 of 60 including the levered rungs).
8. **RULE 8.** `G` is chosen on 2009-2016 alone; 2017-2026 was read once. Both choosers — 2264's
   drawdown-budget rule at κ = 0.60 and the habitual IS-Sharpe argmax — pick `G = 1.00` on U56/M
   at every one of the five cost rungs, so the cell is rule-8 reachable by either.
9. **WHY NOT RECOMMENDED — the cadence is POST-HOC.** This run declared GROSS and PANEL as its two
   tuned dials and cadence as REPORTED, NOT TUNED. Picking the monthly cell after seeing its cost
   life is selection on a third axis, and it is disclosed as such rather than laundered into the
   parameter count. It also thins the DD margin that made 2264's cell defensible, and PROTOCOL
   rule 6 gives a cadence change to the Sunday review, not to a run.
10. **CAVEATS.** Survivorship (rule 9): U56 is 2026 constituents held from 2008, so the CAGR level
   is optimistic and both 4b level legs are easier than on a point-in-time panel — **81.33 bps is
   an UPPER bound on the real cost life**. Flat costs, no spread/impact/borrow. One band (3%), one
   delay (t+1), one panel for the candidate. RULES.md / scan.py / bot.py / baseline.py untouched.

# Memo — 4b by-product of idea 352: U56 TOP40 equal-weight, gross 0.75, MONTHLY

1. **Not this idea's question.** Idea 352 asked whether a turnover ceiling pre-screens the queue
   (answer: no). This book is what the 90-point population threw off; it is inside the already
   heavily mined U56 monthly family, so treat it as a **PARK/confirm**, not a fresh discovery.
2. **Numbers, U56, 10 bps, 2009-01-15 → 2026-09-04:** CAGR 12.04%, Sharpe 1.1401, MaxDD −18.00%,
   halves 1.1422 / 1.1425, OOS (2017-) Sharpe 1.2187, OOS CAGR 13.36%, OOS MaxDD −18.00%.
3. **4b bars, all five cleared:** H1 1.1422 > 0.9566, H2 1.1425 > 0.8340, OOS 1.2187 > 0.8820,
   |MaxDD| 18.00% ≤ 20.23%, CAGR 12.04% ≥ 10.66%. It also clears them at **25 bps**.
4. **Cost breakeven c\* = 43.5 bps**, the highest in the 90-book grid; the binding bar at c\* is the
   CAGR floor. Annual turnover **3.67× NAV** — the lowest-turnover 4b pass on the grid.
5. **4a: FAILS.** RULES v2 (live) is Sharpe 1.2056 / MaxDD −12.05% on the same sample. This book
   is higher-return and materially deeper in drawdown. 4b is the only path it takes.
6. **Exact RULES wording if it were ever adopted (it is NOT proposed for Sunday):**
   *"Universe: research/universe.json (U56), BTC/ETH excluded. Eligible on day t: close > its own
   200-day simple moving average AND 20-day realised vol (annualised) < 0.60. Rank the eligible
   names by the scan.py composite (12-1 momentum, 6m and 3m returns, each cross-sectionally
   rank-scaled, averaged, halved when below the 200d MA, divided by sqrt(max(vol20, 0.08))).
   Hold the top 40 by that composite, equally weighted at 0.75/40 = 1.875% of NAV each; if fewer
   than 40 are eligible, hold all of them equally at 0.75/N. Remainder in cash. Rebalance on the
   last trading day of each calendar month, apply at the next close."*
7. **Why 40 and 0.75 are not two fresh tuned parameters here:** both are grid axes reported in
   full (n ∈ {5,10,20,40}, gross ∈ {0.75,1.00}); 40 is the *widest* n tested and the width curve
   is still rising at the edge, which idea 243 already flagged as an unresolved ceiling.
8. **What would falsify it:** a rule-8 read that picks it IS and loses OOS. On U56 the IS-Sharpe
   chooser picked TOP20/g1.00/M instead, whose OOS Sharpe is 1.0778 — **0.14 worse** than this
   book's. So the standing chooser does *not* find it, which is a mark against pre-registering it.
9. **Relation to the 2026-09-04 KEEP (top-20 equal-weight, no vol scaler):** same family, wider
   book, slower cadence. Whether width or cadence carries the +0.14 of OOS Sharpe is untested and
   is the obvious follow-up (queued).
10. **Recommendation: PARK.** Do not take it to Sunday review on this evidence. It is one arm of a
    grid built to answer a different question, its n sits on the grid edge, and no pre-registered
    chooser selects it.

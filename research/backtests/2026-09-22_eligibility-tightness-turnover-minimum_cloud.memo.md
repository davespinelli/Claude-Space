# MEMO — 4b KEEP-CANDIDATE, RECORDED NOT RECOMMENDED (idea 949, lane cloud, 2026-09-22)

1. **Book.** Hold every name whose close is above its own 200-day moving average at a FIXED
   weight of 0.75/Nbar of NAV (Nbar = the panel's time-mean count of names above their MA over the
   sample), the rest in CASH; no vol screen at all (`max_vol` = 1.00, the rung the IS-only chooser
   picks); monthly rebalance, filled at the next close, 10 bps.
2. **Reached how.** m = 1.00 is the rung a legal IS-only chooser (max 2009-2016 Sharpe) selects on
   BOTH large-cap panels, so rule 8 is satisfied without a second look at 2017-2026.
3. **U56 FULL (2009-01-13 -> 2026-09-18):** CAGR 12.57%, Sharpe 1.2168, MaxDD -15.84%, halves
   1.2418 / 1.1982, turnover 2.13x/yr, realised mean gross 0.750.
4. **U56 OOS (2017-2026, read ONCE):** CAGR 13.81%, Sharpe 1.2916, MaxDD -15.84%.
5. **B136 FULL:** 11.82% / 1.1318 / -17.03% (H1 1.2494 / H2 1.0189, turnover 2.26x/yr);
   **B136 OOS:** 11.90% / 1.1475 / -17.03%.  **It replicates across two panels** — rarer in this
   record than a single-panel pass.
6. **vs SPY:** U56 FULL 15.14% / 0.8851 / -33.72%, OOS 15.29% / 0.8751 / -33.72%; B136 FULL
   15.12% / 0.8844 / -33.72%.  All five 4b legs clear on both panels (CAGR floors 10.60% / 10.58%;
   DD caps -20.23%).
7. **vs live RULES v2 (monthly, 10 bps):** U56 8.88% / 1.1720 / -14.38%; B136 8.32% / 1.0833 /
   -15.69%.  Path **4a FAILS on the drawdown leg on both** (-15.84% / -17.03% are deeper than the
   live book's), and 4a is 0 of 408 across this whole run.
8. **Why NOT recommended.** It **fails on SMALL** (Sharpe 0.6171 vs SPY 0.8570, 0 of 136 rungs
   clear 4b there); `Nbar` is a whole-sample constant, i.e. a mild in-sample quantity in the sizing
   rule; and the book is a near-relative of the live RULES v2 band book with the band set to zero,
   so it is a variation on an adopted family rather than an independent finding.
9. **Exact RULES wording IF a Sunday review ever adopts it** (it is NOT proposed here):
   *"Clause 2 (gate). A name is held when its close is above its 200-day moving average and is not
   held otherwise; no volatility screen applies. Each held name carries 0.75/Nbar of NAV, where
   Nbar is the reference count fixed at adoption; the remainder is held in CASH and is never
   re-spread, and total gross is capped at 1.00. Rebalance monthly, on the last trading day of the
   month, filled at the next close."*
10. **RULES.md, scan.py, bot.py and baseline.py were NOT modified.**  Survivorship: U56 and B136 are
    current-constituent panels, so the CAGR and MaxDD levels above are optimistic.

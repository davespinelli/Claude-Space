# Memo — idea 331 KEEP-candidate (PROTOCOL path 4b, U56 only). Recommend PARK, not adoption.

1. **Candidate:** U56, top-20 by the v1 composite with the vol scaler OFF, NORM weights `g/k_t` at
   g = 0.75, **MONTHLY** cadence, **no-trade band m = 20** (enter at rank ≤ 20, sell only past rank 40).
2. **Full sample @10 bps:** 13.30% CAGR / 1.109 Sharpe / −18.73% MaxDD, H1/H2 **1.196 / 1.042**,
   turnover **2.76x/yr**. SPY 15.23% / 0.889 / −33.72%, halves 0.957/0.834. RULES v2 (live) 8.66% / 1.206 / −12.05%.
3. **All five 4b bars clear at 0, 10 AND 25 bps** (@25: 12.83% / 1.074 / −18.83%, H1/H2 1.162/1.006).
   **Breakeven c\* = 95 bps** — the second-highest in the record and demonstrably not a 10-bps artefact.
4. **Rule 8 (the reason this is worth a memo):** it is the IS chooser's OWN pick — (cadence, m) selected
   on 2008–2016 Sharpe alone, 2017+ read once: **OOS 14.15% / 1.124 / −18.73%** vs SPY OOS 0.882 and
   RULES v2 OOS 1.285. It clears all three OOS 4b bars without hindsight.
5. **Why PARK and not KEEP:** the identical book fails 4b on **B136** (MaxDD −26.31% vs the −20.23% cap)
   and on **SMALL439** (every bar) at every rung. **4a is 0/36 across the whole grid** — nothing here beats
   the live book's −12.05% drawdown. And the U56 chooser's regret is **−0.239** (it missed 6W m=0, OOS 1.363),
   so the cell is the best *available* pick, not the best cell.
6. **Sibling, NOT recommended (hindsight):** U56 **6W m=20** reads 14.31% / 1.159 / −19.42%, H1/H2 1.155/1.175,
   OOS 1.250, turnover 2.29x/yr, **c\* = 104 bps — the record's highest**. The IS chooser does not pick it.
7. **Exact RULES wording, if the Sunday review ever adopts it** (single clause, replacing the cadence and
   selection clauses; nothing else in RULES changes):

   > **Cadence.** Rebalance on the last trading day of each **calendar month**; hold weights unchanged in between.
   > **Selection.** Rank the eligible universe (price above its 200-day mean, 20-day annualised vol < 0.60) by the
   > composite of the 12-1 momentum, 6-month and 3-month return percentile ranks, equally weighted, **without any
   > volatility scaling**. Let `k_t` be the number of names ranked 20 or better on that date.
   > **No-trade band.** Hold a name from the date it first ranks 20 or better until the date its rank passes **40**
   > or it leaves the eligible set. Refill free slots, best rank first, from eligible names not already held, until
   > `k_t` names are held.
   > **Sizing.** Equal weight `0.75 / k_t` of NAV per held name; the residual 25% and any unfilled slot weight is CASH.
   > **Universe.** `research/universe.json` (the 56-name ETF/mega-cap panel) only — this clause is **not** validated
   > on the 136-name or sub-$2B panels and must not be applied to them.

8. **Costs and execution:** all numbers are next-day execution at the close, 10 bps per unit turnover unless a rung
   is named. The candidate survives 25 bps and breaks even at 95.
9. **SURVIVORSHIP:** U56 is a current-constituent list, so the 13.30% CAGR level is optimistic. The cadence- and
   band-DIFFERENCES this run measures are far less exposed than the level; the level is what a capital decision uses.
10. **Bottom line:** the first rule-8-clean, 25-bps-surviving 4b pass this lane has produced on a *pre-registered*
    grid — and still a one-panel object. PARK; re-test on a panel the record has not already mined before any capital.

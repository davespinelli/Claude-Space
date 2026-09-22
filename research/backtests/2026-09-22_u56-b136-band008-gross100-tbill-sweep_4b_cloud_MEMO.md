# 4b CANDIDATE — band 0.08 / gross 1.00 / weekly, idle NAV swept to SHY (idea 2213, lane cloud, 2026-09-22)
# RECORDED, NOT RECOMMENDED. It is the same cell 914/2119 killed on weekday fragility; the T-bill sweep
# widens its DD margin from +1.18 to +1.38 pp (U56) but its own 3-offset spread is 1.86 pp, so the
# binding leg is still inside its scheduling noise. It is reachable only by the IS-4b-restricted chooser.
1. Universe: the live panel (U56 = research/universe.json, 56 names). Replicates on B136.
2. Trend band: a name is IN when its close is above its 200-day MA times 1.08, OUT when below 0.92 times
   it, and holds its previous state in between; OUT until 200 closes exist.
3. Sizing: hold every IN name at 1.00 / N of NAV, N = names priced that day. No ranking, no vol filter.
4. Idle NAV: the residual 1 - sum(w) is held in SHY (T-bill proxy), not in 0%-yield cash.
5. Cadence: rebalance on the last trading day of each week; execute at the next close. Costs 10 bps.
6. OOS (2017-2026, read once): U56 12.62% / 1.2158 / -18.85% (H1 1.331 / H2 1.089); B136 11.53% /
   1.1411 / -19.31%; vs SPY OOS 15.29% / 0.8751 / -33.72% and RULES v2 OOS 9.46% / 1.2767 / -12.05%.
7. FULL: U56 11.81% / 1.1862 / -18.85%; 4b PASS in FULL, IS and OOS on both panels, 4/4 cost rungs.
8. 4a: FAIL in every window on both panels (MaxDD far worse than the live book's -12.05%).
9. Blocking objection: DD margin +1.38 pp (U56) / +0.92 pp (B136) vs 3-offset spread 1.86 / 1.13 pp.
10. Also: the habitual argmax-IS-Sharpe chooser does NOT reach this cell under the sweep — it picks
    gross 0.50, which fails 4b on the CAGR leg alone. Do not ship without a 5-offset re-read.

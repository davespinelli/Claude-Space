# Memo — U56 QM+0.00/RESPREAD monthly (nominal 4b pass, recommended **PARK**)

1. **Book.** Universe = research/universe.json less SPY (55 names). Rank every live name by
   `dist = close / 200d-MA − 1`. Hold the top `ceil(x · n_t)` names, `x = 0.7082` (the mean mask
   fraction of `close > 200d-MA` on this panel), equal-weight, gross 0.75, **monthly** rebalance,
   t+1 execution, 10 bps.
2. **Exact RULES wording if ever adopted:** *"On the last trading day of each month, rank every
   instrument with 200 closes by close/200d-MA − 1; hold the top 71% of them at 0.75/k of NAV each,
   k = names held; the remaining 25% of NAV is cash. Execute at the next close."*
3. **Full sample (2009-01-13→2026-09-08):** CAGR 14.35%, Sharpe 1.220, MaxDD −20.15%, halves 1.322/1.136.
4. **SPY:** CAGR 15.19%, Sharpe 0.887, MaxDD −33.72%, halves 0.959/0.829, OOS Sharpe 0.879.
5. **Rule-8 OOS (2017→2026):** CAGR 14.79%, Sharpe 1.221 (+0.34 vs SPY), MaxDD −20.15%.
6. **4b legs:** H1 ✓ H2 ✓ OOS ✓ CAGR ✓ (14.35% vs 10.63% bar) **DD ✓ by 0.08 pp** (−20.15% vs −20.23%).
7. **Why PARK, not KEEP:** the DD leg passes by 0.08 pp. Idea 299 measured 1.13 pp of MaxDD moving
   on the cadence dial alone for one book, so this pass is **cadence-decided, not signal-decided** —
   it would fail at W or Q. It is not a robust 4b passer.
8. **4a:** fails (Sharpe 1.220 vs live RULES v2 1.204 in full but MaxDD −20.15% vs −12.05%).
9. **Turnover** 2.0×/yr; the cost leg is not what binds.
10. **Provenance:** incidental to idea 549 (whose subject was the c_sd census); same family and panel
    as the record's existing 4b footprint (idea 404, 6 of 7 passers on u56). Not a new signal.

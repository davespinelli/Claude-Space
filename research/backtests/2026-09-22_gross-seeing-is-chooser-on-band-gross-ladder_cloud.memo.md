# PARK memo — U56 band 0.02 / gross 1.00 (idea 2121, lane cloud, 2026-09-22)

1. **The book, in exact RULES wording.** *"Hold every name in the U56 universe whose close is
   inside the 200-day moving-average band with hysteresis — IN above MA×1.02, OUT below
   MA×0.98, previous state in between, OUT before 200 closes exist — at 1.00/N of NAV, N =
   instruments priced that day; gated-out weight goes to CASH and is never re-spread.
   Rebalance weekly, weights decided at close t and applied at t+1, 10 bps per unit turnover.
   Long only, no leverage."* It is `baseline.rules_v2_weights(px, band=0.02, gross=1.00)`.
2. **Full sample (10 bps):** CAGR 11.33%, Sharpe 1.1934, MaxDD −15.65%, halves 1.2056 / 1.1856.
3. **OOS 2017–2026 (read once):** CAGR 12.53%, Sharpe 1.2784, MaxDD −15.65%.
4. **Comparands OOS:** RULES v2 9.46% / 1.2767 / −12.05%; SPY 15.29% / 0.8751 / −33.72%.
5. **4b legs, FULL:** H1 1.206 > 0.921 ✓, H2 1.186 > 0.829 ✓, MaxDD −15.65% ≥ −20.23% ✓,
   CAGR 11.33% ≥ 8.03% ✓. **4b legs, OOS:** Sharpe ✓, MaxDD ✓, CAGR 12.53% ≥ 10.70% ✓.
6. **4a: FAIL.** MaxDD −15.65% is worse than RULES v2's −12.05%; 0 of 72 picks in this run
   clear 4a on either panel at any cost rung.
7. **Why this is PARK and not KEEP (i):** it **FAILS 4b inside the IS window itself**
   (`keep4b_is` False), so the rule-8 discipline that would have adopted it never saw a pass.
8. **Why PARK (ii):** only 1 of 7 legal IS-only choosers (IS_CALMAR) reaches it, and that same
   chooser picks `b0.03_g1.00` on B136, which **FAILS 4b OOS**. Choosing IS_CALMAR because it
   won here is a third tuned dial worth ~0.1 of OOS Sharpe (this run's B4 spread).
9. **Why PARK (iii):** the zero-parameter rule MAXGROSS (live band 0.03, top gross rung, no
   in-sample read at all) delivers OOS 12.67% / 1.2760 / −15.91% — statistically the same book.
   The in-sample fitting buys nothing; the exposure buys everything (B7: OOS CAGR is monotone
   up in gross 40/40, OOS Sharpe monotone down 30/40).
10. **Survivorship.** U56 is a current-constituent list; the 11.33%/12.53% CAGR levels are
    optimistic and this memo is a within-tape contrast only. **Do not promote on these numbers.**

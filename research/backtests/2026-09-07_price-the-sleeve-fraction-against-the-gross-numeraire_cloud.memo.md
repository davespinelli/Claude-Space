# PARK memo — ungated QQQ core + macro sleeve at c=0.40 (idea 372, 2026-09-07, cloud)

1. **Status: PARK, not KEEP.** It clears every 4b bar as a pre-registered point at 0/10/25 bps on
   both panels, but PROTOCOL rule 8's IS-Sharpe chooser picks c=1.00 in 6/6 ungated cells (OOS
   Sharpe 0.963, MaxDD −35.1%, a 4b failure). The book is admissible, not selectable.
2. **Numbers (U56 @10 bps, 2009-01-13 → 2026-09-04):** CAGR 11.45%, Sharpe 1.044, MaxDD −17.38%,
   halves 1.144 / 0.975, OOS 1.063, turnover 2.87x/yr. B136 is identical to 4e-4 (degenerate axis).
3. **Bars:** SPY 15.23% / 0.889 / −33.72%, halves 0.957 / 0.834, OOS 0.882 ⇒ 4b needs H1>0.957,
   H2>0.834, OOS>0.882, MaxDD<20.23%, CAGR>10.66%. Slack: DD **2.85pp**, CAGR **0.79pp**.
4. **Survives 25 bps:** 10.97% / 1.005 / −17.45%, halves 1.098 / 0.940, OOS 1.027 (CAGR slack 0.31pp).
5. **4a: FAILS** (0/240). RULES v2 is 8.66% / 1.206 / −12.05% on U56 — lower return, better Sharpe
   and drawdown. This is a 4b (capital-worthy) candidate only.
6. **Why it is not just de-grossing:** against a static-gross ladder point at matched realised mean
   gross (0.795) it buys 1.88 pp of MaxDD per pp of CAGR against the ladder's 1.49, and no ladder
   point clears 4b at any gross (0/120) while this one does.
7. **Window:** c=0.25 fails the CAGR floor, c=0.60 fails the DD cap. The admissible band is
   c ∈ [0.40, 0.50], two of ten grid points. Not a plateau.
8. **The 200d gate must be OFF.** Every gated variant fails 4b (0/60) and the gate turns the sleeve's
   ruler edge negative by 25 bps.
9. **Exact RULES wording if Sunday review ever adopts it** (it should not until the rule-8 gap is
   closed): *"Hold 40% of NAV in QQQ at all times, with no trend filter, and 60% of NAV in the macro
   sleeve: of the nine ETFs SPY, QQQ, IWM, EFA, EEM, TLT, GLD, DBC, UUP, weight each by inverse
   60-day realised volatility, normalised across the nine, times the fraction of its three momentum
   signals (12-1 month, 6 month, 3 month) that are positive. Rebalance weekly at the close, execute
   at the next close."*
10. **Blockers before any KEEP:** (a) rule 8 must be able to select c — the IS chooser is monotone in
    c and picks the worst 4b cell; (b) the book is 40% QQQ over the best large-cap decade in the
    sample; (c) both panels are current-constituent lists; (d) idea 105's open question (is the
    sleeve's value just GLD?) is unresolved and applies here unchanged.

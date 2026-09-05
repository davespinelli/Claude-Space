# Memo — idea 160, the one 4b pass, and why it is NOT proposed

1. **The book.** `u56 @10 bps, FIXQ q = 0.53`: hold the top 53% of the eligible set each
   week by the composite (no `/sqrt(vol20)`), equal-weighted to 75% gross.
   **13.17% / Sharpe 1.0572 / MaxDD −19.36%**, halves **0.9822 / 1.1270**,
   **OOS 15.54% / 1.1813 / −19.36%**, 13.0 turns/yr. It passes 4b full-sample and 4b on the
   OOS window, and its OOS Sharpe is the highest of all 96 books in this run.
2. **Recommendation: DO NOT PROMOTE.** Four reasons, all stated together.
3. Its matched-count control `FIXN n = 19` **also passes 4b** (1.0390, OOS 1.1072), so the
   share-tracking instrument is not what earns the pass — the *level* q ≈ 0.53 is.
4. The same book **fails 4b on broad** (drawdown cap) and **at 25 bps** (H1 and DD), so it
   clears neither a second panel nor idea 82's proposed 25 bps cross-universe bar.
5. Its **H1 margin over SPY is 0.025** (0.9822 vs 0.957) — inside the noise of the panel.
6. It is **one cell of 32** in a family whose mean ΔSharpe vs its own control is **−0.026**,
   and whose rule-8 selector is **last of five, below random** (0.702 vs 0.958).
7. **If the Sunday review nonetheless wanted it, the exact RULES wording would be:**
   > *Each Friday close, rank every eligible name (above its 200-day moving average and
   > `vol20 < 0.60`) by the composite of pct-ranked 12-1, 6-month and 3-month return, with
   > no volatility divisor. Hold the top **53%** of that week's eligible list, equally
   > weighted to **75%** total gross. Execute at the next close. Applies to the 56-name
   > universe.json list only; not established on universe_broad.json or above 10 bps.*
8. The transferable finding is Q5's, not this book's: Sharpe rises near-monotonically in q
   (Spearman +0.86 to +0.98 on both large-cap panels) and the argmax is q → 1.00 in 3 of
   4 primary cells. **The level of selectivity is 5–9× more consequential than whether it is
   pinned**, and the winning level is "hold everything eligible".
9. That is a fourth independent derivation of ideas 72 / 82 / 141's "the ranking subtracts
   value", reached from the selectivity axis rather than the ranking axis.
10. **Nothing in RULES.md, scan.py, bot.py or baseline.py is changed by this run.**

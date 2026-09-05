# Memo — cadence, for idea 107 (evidence, NOT a rules proposal; Sunday review owns RULES)

1. Idea 171's CADENCE positive **partially replicates** on a disjoint corpus (115 books, no B136) and a
   7-point ladder: pooled SEL-SHARPE +0.0388 OOS Sharpe (t +3.26) but **capture falls 67.1% → 23.8%**,
   and it is +0.0006 (t +0.02) on the u56 family, i.e. the dial's *selector* skill is not general.
2. Both of idea 175's questions are answered: **monthly is still the IS pick (91/115, 79.1%)** and
   **monthly is NOT the OOS argmax (12.2%)** — the oracle wants 6W in 60.9% of books (97% on u56/ETF).
3. The decision number is the constant, not the fit. **Cadence = monthly, pre-registered, beats weekly
   by +0.0761 OOS Sharpe pooled (t +6.71) and is positive and significant on all three families**
   (SMALL +0.0978 t+3.91, U56 +0.0469 t+7.24, ETF +0.0730 t+6.82) — about 2× the fitted selector.
4. 6W is larger on large caps (+0.164 / +0.160) but n.s. on the small panel (+0.0163, t +0.81) and Q is
   a cliff (−0.247 / −0.291). **M is the only ladder point positive and significant on all three.**
5. Fitting costs money through its tail: on u56 the selector's 27 M picks earn +0.0531 each and its
   4 Q picks lose −0.3368 each, netting zero. A pre-registered constant cannot land on Q.
6. Exact RULES wording, if and when Sunday review adopts it (one dial, no selector, no new parameter
   to fit): *"Rebalance cadence is **monthly** — target weights are recomputed on the last trading day
   of each calendar month and executed at the next close. Cadence is a pre-registered constant; it is
   never chosen from a backtest window."*
7. This changes cadence only. It does not touch eligibility, ranking, n, or gross.
8. Cost of adopting: turnover falls 5.5× → 2.7×/yr pooled; MaxDD is roughly unchanged (−17.05% → −17.32%
   mean OOS). On the small panel it is the largest single improvement measured here.
9. Caveats: current-constituent survivorship on all three panels (idea 54) — the paired comparison is
   unaffected, the levels are not; idea 38's calendar-day index makes a "bar" a calendar day on
   u56/ETF after 2014-09-17; 6W's win is one grid step from the ladder edge (idea 183).
10. **No new KEEP.** All 59 4b passes are u56-family re-cadencings of idea 2's book (idea 144);
    U56 @ M reproduces idea 171's memo'd by-product to 3 dp. Nothing here is a new book.

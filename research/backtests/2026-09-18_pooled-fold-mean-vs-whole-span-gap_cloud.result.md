# Idea 1278 — is the POOLED-FOLD-MEAN vs WHOLE-SPAN gap a general property? ANSWERED: only of the NON-LINEAR statistics, and MaxDD is the worst by an order of magnitude.

1. **Shape-invariance is exact.** Decomposing GAP = GAP_shape + GAP_trunc over 504 grid points
   (7 statistics x 3 panels x 5 books x 4 fold lengths L = 126/189/252/378), the statistics that
   are linear in the per-day series read max|GAP_shape| = 7.1e-15 (turnover/yr), 6.9e-18 (drag/yr),
   8.3e-17 (meanret/yr) — floating-point zero at every point. Their apparent gap (up to 0.2954
   units/yr of turnover) is ENTIRELY GAP_trunc, the dropped trailing remainder.
2. **Four statistics carry a real, sign-consistent bias.** Share of 72 points with GAP_shape > 0:
   MaxDD 1.000, CAGR 1.000, Sharpe 0.944, vol 0.000 (always negative). Median |GAP_shape| at
   L = 252: MaxDD +0.1665, Sharpe +0.0842, vol -0.0056, CAGR +0.0080.
3. **1276's yardstick reverses on Sharpe when read on books, not chooser differences.** GAP_shape
   at L=252 against the whole 0->50 bps cost ladder's move of the same statistic: MaxDD 9.59x,
   vol 21.32x — but Sharpe only 0.20x (0.0842 vs 0.4205) and CAGR 0.07x (0.0080 vs 0.1077).
4. **MaxDD's gap is structural.** Over L = 126/189/252/378 the median |GAP_shape| roughly halves
   per doubling for CAGR (0.0181 -> 0.0032) and Sharpe (0.1607 -> 0.0640) but barely moves for
   MaxDD (0.1992 -> 0.1400). A drawdown cannot span a fold boundary; no attainable L removes it.
   Worst on SMALL663 (0.2046) vs B136 0.1646 / U56 0.1455.
5. **4b legs.** Fold pass-share lands on the wrong side of 0.5 against the whole-span leg at
   L_H1 0.400/0.400/0.333/0.400 and L_H2 0.400/0.400/0.267/0.133 of cells over the four L's;
   L_CAGR 0.000/0.067/0.000/0.200 and L_DD 0.067/0.067/0.067/0.000. The path legs are fragile.
6. **CAPITAL ARM (rule 8, OOS read once).** U56 chooser on 2009-2016: WHOLE-SPAN Sharpe picks
   MOM20 (+1.1212), FOLD-MEAN picks RULESv2 (+1.0461 vs MOM20 +1.0442, margin 0.0019). OOS
   2017-2026: MOM20 21.42% / 1.1391 / -27.24%; RULESv2 9.47% / 1.2778 / -12.05%; SPY 15.28% /
   0.8745 / -33.72%. B136 and SMALL663 pick identically under both conventions.
7. **VERDICT: KILL (capital), ANSWERED + SCHEMA.** 4b OOS 0 of 6 chooser cells, 4a 0 of 6.
   U56/MOM20 fails L_DD alone (-27.24% vs a -20.23% cap); U56/RULESv2 fails L_CAGR alone (9.47%
   vs a 10.70% floor); B136/MOM10 fails L_H1 and L_DD; SMALL663/RULESv1 fails all four.
8. **PROPOSED SCHEMA LINE (the deliverable 1276 §10 asked for), for the Sunday review, PUBLISHING
   ONLY — it changes no book:** *"A figure published as a mean over folds must name its fold
   length and its fold count, and may be published fold-averaged ONLY if it is linear in the
   per-day return or turnover series (turnover, cost drag, mean return). CAGR, vol, Sharpe and
   MaxDD must be published WHOLE-SPAN; where a fold-averaged value of one of these is quoted it
   must be labelled and its whole-span value given beside it. MaxDD may not be fold-averaged at
   all."* Measured basis: the linear set is exactly zero at 216 of 216 points, so the permission
   costs nothing; MaxDD's bias is 9.59x the record's whole cost ladder and does not shrink with L.
9. **Do NOT read this as licence to drop the cost rung.** On Sharpe and CAGR — the two statistics
   the record's verdicts actually turn on — the 0->50 bps ladder is 5x and 13x the aggregation gap.
   1276's "an order of magnitude larger" holds for its own chooser differences, not for book levels.
10. **SURVIVORSHIP (rule 9).** U56 and B136 are current-constituent lists; SMALL663 is a current
    sub-$2B screen with 52 of 715 names dropped on max_1d_move >= 1.0. Every level is an UPPER
    bound. Points 1-5 are differences of the SAME statistic on the SAME book under two aggregations,
    so a level bias moves both terms together and they are first-order immune; point 6's OOS levels
    are not, and are quoted as upper bounds.

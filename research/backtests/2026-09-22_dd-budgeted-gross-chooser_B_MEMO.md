# KEEP-4b CANDIDATE — idea 2264 (2026-09-22, lane B). Recorded, NOT recommended for promotion.

1. **BOOK.** The live RULES v2 band book, unchanged in every clause except size: `gross = 1.00`
   instead of `0.75`. Panel u56, band 3%, weekly, t+1, gated-out weight to CASH. No leverage.
2. **EXACT RULES WORDING if ever promoted.** *"Clause 3 (position size). Hold every name inside
   the 200-day ±3% band at `G / N` of NAV, N = instruments priced that day, gated-out weight to
   cash. `G` is set once a year on the trailing history available at the time as the largest
   value on the ladder {0.25 … 1.50 step 0.125} whose realised maximum drawdown over that history
   is no worse than 0.60 × SPY's over the same history, and is capped at 1.00 (PROTOCOL rule 2,
   no leverage). On the 2009-2016 history that rule returns `G = 1.00`."*
3. **NUMBERS @10 bps, u56.** FULL 11.53% / 1.2009 / -15.91% (halves 1.2282 / 1.1799),
   OOS 12.67% / 1.2760 / -15.91%, turnover 2.35x/yr.
4. **COMPARANDS.** Live RULES v2 FULL 8.62% / 1.2010 / -12.05%, OOS 9.46% / 1.2767 / -12.05%
   (1.77x/yr). SPY FULL 15.14% / 0.8851 / -33.72%, OOS 15.29% / 0.8751 / -33.72%.
5. **4b, both windows.** PASS at 0 / 5 / 10 / 25 bps in FULL *and* OOS; at 50 bps OOS still
   passes and FULL misses the CAGR floor by 0.11 pp (10.49% vs 10.60%). OOS margins at 10 bps:
   DD **+4.32 pp** (-15.91% vs cap -20.23%), CAGR **+1.97 pp** (12.67% vs floor 10.70%).
6. **4a: FAIL, everywhere — 0 of 110 book cells and 0 of 170 chooser cells.** Gross is
   Sharpe-neutral on this book (1.2010 → 1.2000 over g = 0.25..1.50), so it cannot beat the live
   book's Sharpe in both halves, and it is strictly deeper in drawdown. This is a 4b-only
   candidate on the path PROTOCOL rule 4b says is the one that matters for real capital.
7. **RULE 8 — this is the point.** Idea 2233 PARKed this exact cell as "NOT rule-8 reachable".
   It is reachable: the IS-only rule above picks it on 2009-2016 at every κ ≥ 0.60 on both
   panels and every cost rung, and 2017-2026 was read once. The record's habitual IS-Sharpe
   chooser misses it (picks g = 1.50, 4b OOS 1 of 10) because Sharpe is the one statistic gross
   is invariant to. **κ is not tuned at the pick that matters:** under the no-leverage cap the
   budget is slack for every κ ≥ 0.60, so the rule degenerates to "take the largest legal gross"
   — a zero-parameter rule. κ = 0.60 is itself PROTOCOL 4b's own δ, pre-registered 2026-09-04.
8. **FALSIFICATION (arm R).** Reversed walk-forward (2017-2026 chooses, 2009-2016 read): κ = 0.60
   still clears 4b at 7 of 10 cells, so the forward pass is not an artefact of the IS window being
   the calmer one. κ = 0.40 reads 0 of 10 and κ ≥ 0.70 reads 0 of 10 in both directions.
9. **WHY NOT RECOMMENDED.** It is **panel-dependent**: on b136 the same pick clears 4b FULL at
   0/5/10 bps but misses 4b OOS from 5 bps on, failing the CAGR floor by 0.05-0.21 pp. It buys
   +2.91 pp of CAGR with +3.86 pp of drawdown and no Sharpe at all — a pure sizing decision
   dressed as a rule, and PROTOCOL rule 6 gives that decision to the Sunday review, not to a run.
10. **CAVEATS.** Survivorship (rule 9): u56/b136 are 2026 constituents held from 2008, so every
   CAGR level is optimistic and both 4b level legs are easier than on a point-in-time panel.
   Costs are flat per unit turnover, no spread/impact/borrow. One cadence (W), one delay (t+1),
   one band (3%). Levered rungs g > 1.00 are published but excluded from this candidate.

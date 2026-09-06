# Memo — idea 56 by-product: drop the vol20 clause from idea 2's candidate (PARK, not KEEP)

1. **Candidate.** Idea 2's KEEP-candidate construction with the `vol20 < 0.60` clause deleted:
   MA200 gate only, top-20 equal-weight at 75% gross, weekly, 10 bps, next-day execution, U56.
2. **Numbers (U56, 2009-01-13 → 2026-09-04).** 14.40% CAGR / 1.158 Sharpe / −19.09% MaxDD;
   halves 1.222 / 1.118; OOS (2017–2026) 15.85% / **1.181** / −19.09%; turnover 9.03x/yr.
3. **Versus idea 2's published candidate** (BOTH gate, same everything): +1.66pp CAGR, +0.060 Sharpe,
   +0.125 H1, +0.014 H2, +0.013 OOS Sharpe, −0.94pp MaxDD. Better on 5 of 6 4b metrics.
4. **Versus the bars.** SPY 15.23% / 0.889 / −33.72% (H1 0.957, H2 0.834, OOS 0.882). 4b needs
   MaxDD ≥ −20.23% and CAGR ≥ 10.66%: it clears the DD cap by 1.14pp and the CAGR floor by 3.74pp.
   **4b PASS on U56. 4a FAIL** — live RULES v2 is 1.213 (1.231/1.200), unbeaten by all 48 cells.
5. **Why PARK and not KEEP.** (a) It fails 4b on B136: 14.74% / 0.995 / −24.00%, first-failing bar DD,
   identical in shape to the no-gate book — so the pass is U56-specific, the same cross-universe
   failure idea 53 already recorded for idea 2's candidate. (b) Rule 8's own chooser, run inside the
   cell, picks NONE/n=5 on IS Sharpe and lands at OOS 1.044 — this candidate is the best *ex post*
   cell, not the procedure's pick. Promoting it would be selecting on the full sample.
6. **What is actually established.** vol20 costs 1.94pp of CAGR and 0.065 of Sharpe at n=20 on U56 and
   buys 3.12pp of MaxDD; the trade is real but it is a drawdown purchase, not a return edge, and it is
   negative-Sharpe in 12 of 12 decomposition cells across both universes and both gross conventions.
7. **Exact RULES wording if a future Sunday review ever adopts it** — replacing RULES v1 clause 2's
   eligibility test, quoted here so the proposal is on the record, NOT adopted by this run:
   > *Eligibility: a name is eligible on any rebalance day when its close is above its 200-day simple
   > moving average. (The `20-day annualised volatility < 0.60` condition is removed.) Rank eligible
   > names by the composite of 12-1, 6-month and 3-month return ranks with no volatility scaler; hold
   > the top 20 at 3.75% of NAV each, rebalanced weekly; ineligible weight is held as cash.*
8. **Pre-conditions for that adoption** (none met today): a 4b pass on B136 or a second independent
   large-cap panel; a rule-8 selector that picks it without reading 2017–2026; and a Sunday review, per
   PROTOCOL rule 6 — one rules change per week, and RULES v2 is the live book as of 2026-09-06.
9. **Cheaper interim use.** Report the MA200-only column beside every published RULES v1 gate result.
   It costs one extra backtest and separates "the gate helps" from "the score already did it" — at n=5
   the MA200 gate is bit-identical to no gate at all on both universes.
10. **Survivorship.** U56 and B136 are current constituents of their lists; the levels above are biased
    upward by an unknown amount. The decomposition (differences at fixed panel) is unaffected.

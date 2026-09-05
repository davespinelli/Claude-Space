# Memo to the Sunday review — idea 153, KEEP-candidate (PROTOCOL path 4b), lane C, 2026-09-05

1. **What passed.** Restating the standing 4b KEEP's position count as a **share of the eligible
   list** makes it pass 4b on `universe_broad.json` too, which its name count does not: broad
   n=20 fails 4b on H2 (0.811 vs SPY 0.834); broad n=47/49 — the incumbent's own 0.51-0.53 share
   × broad's eligible count — gives 11.6-11.7%/1.02/-19.0%, halves 1.12/0.93, OOS Sharpe 1.03.
   Nothing is tuned: the share is read off the incumbent.
2. **Where it holds.** 10 bps, both large-cap panels, m ∈ {0.53, 0.75}, no vol scaler.
   4b passes: 10 of 126 books, cross-universe at 4 (m, tilt) points, all no-tilt or POS-tilt.
3. **Where it fails, stated up front.** 25 bps: zero passes (u56 H1, broad H2 + CAGR floor) —
   idea 137's wall. Small panel: zero at every m, all five bars (idea 136, third confirm).
4. **Rule 8.** The share that passes 4b is *not* what an IS-Sharpe chooser picks (it picks
   m = 0.05-0.10). The candidate is defensible only as a **restatement of the incumbent**, not
   as a new sweep. A tilt allowed into the walk-forward *subtracts* 0.028 mean OOS Sharpe.
5. **Proposed RULES wording, exact** (replaces the position-count clause; no other change):
   > *Eligible names are those above their 200-day moving average with vol20 < 0.60. Let Ē be
   > the universe's mean weekly eligible count, fixed in advance from the ten-year sample.
   > Hold the top n = round(0.53 × Ē) eligible names by composite momentum score, equal-weighted
   > at 0.75/n of capital each, with no volatility scaler. Rebalance weekly, execute next day.
   > On research/universe.json (Ē = 37.5) this is n = 20 — the existing book, unchanged. On
   > research/universe_broad.json (Ē = 91.5) it is n = 49.*
6. **Why the wording is a share and not a count.** The count is not portable: overlap between a
   tilted and an untilted book of the same count differs by 0.425 across the three panels, and
   by 0.045 at matched share. A count fitted on a 56-name list is a different experiment on a
   136-name list.
7. **What NOT to write into RULES.** A time-varying n_t = round(0.53 × E_t) is a different rule
   and was **not** tested here. Ē must be a pre-registered constant per universe.
8. **Cost condition to state alongside it.** The pass is a 10 bps result. At 25 bps it is gone on
   both panels; do not size on it without the breakeven curve (idea 108's protocol).
9. **Survivorship.** Both large-cap panels are current constituents (idea 54); the transfer
   claim is about portability across two survivorship-biased lists, not about live-universe
   robustness. Idea 53's random-composition test should be run on n = 49/broad before capital.
10. **Recommendation.** Adopt the wording in (5) as a **scoping clause** for the existing KEEP
    rather than as a new book — it changes no live position on universe.json — and queue the
    time-varying variant, the 25 bps breakeven and the composition test before any size change.

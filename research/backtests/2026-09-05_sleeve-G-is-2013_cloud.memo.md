# Memo — the `exDBC` sleeve as a 4b (and 4a) candidate. Idea 115, 2026-09-05, cloud.

1. **What it is.** The standing KEEP-4b candidate with **DBC removed from the macro sleeve**: the
   leg becomes TLT + GLD + UUP, everything else unchanged (inverse-vol × 3-signal momentum vote,
   `f = 0.50`, top-20 ranked book at 0.75 gross, weekly, next-day execution, 10 bps).
2. **Numbers, u56 / top20 / 10 bps:** full **12.1% CAGR / 1.200 Sharpe / −13.4% MaxDD**, halves
   **1.237 / 1.170**; **OOS 12.9% / 1.240 / −13.4%**. SPY 15.2% / 0.889 / −33.7% (OOS 15.5% / 0.882);
   RULES v1 6.3% / 0.649 / −13.8% (OOS 7.2% / 0.699).
3. **It passes BOTH KEEP paths** — 4a (beats the live book in both halves at a shallower drawdown)
   and 4b — and repeats on `universe_broad.json` in the same cell: 11.9% / 1.068 / −14.6%,
   OOS 11.0% / 0.974, both paths.
4. **It is the walk-forward pick, not a post-hoc point.** Rule 8 with `f` chosen on 2009-2016 alone
   selects `f = 0.50` in that cell, exactly as it does for the incumbent.
5. **It dominates the incumbent full-sample in 8 of 8 cells** (mean ΔSharpe +0.027, mean ΔMaxDD
   +0.021 pp shallower) and is the only sleeve composition whose rule-8 gap `G` is positive (+0.021
   against S4's −0.169) — i.e. removing DBC also removes the sleeve's rule-8 blind spot.
6. **The honest deduction.** It loses to the incumbent marginally *out of sample* (mean ΔOOS Sharpe
   −0.015), and the composition was one of this run's two tuned parameters, so this is a candidate,
   not a selection this run made.
7. **It must not be adopted before queue idea 106 reports.** Idea 102 found DBC's positive
   contribution concentrated in 2021/2022/2026 and its dead years 2009-2013, the severe-contango era;
   if the drag is a sub-period artefact, this candidate is fitted to that sub-period.
8. **Exact RULES wording, if the Sunday review adopts it** (replacing the sleeve clause only):
   *"Macro sleeve: hold 50% of the book in TLT, GLD and UUP, weighted inverse to each asset's
   60-day volatility and scaled by the fraction of its three momentum signals (12−1, 6m, 3m) that
   are positive; the remaining 50% is the ranked equity book. Rebalance weekly with the rest of the
   book, execute at the next close, and re-gross the combined weights to 100%. Commodities (DBC) are
   not held."*
9. **Universe clause it inherits, unchanged:** the ranked equity book carries the large-cap
   universe condition of ideas 39/49 — this has never passed on the sub-$2B panel.
10. **Survivorship:** both lists are current-constituent, so the absolute CAGR is optimistic; the
    ΔSharpe against the incumbent is a same-names, same-days difference and is much less exposed.

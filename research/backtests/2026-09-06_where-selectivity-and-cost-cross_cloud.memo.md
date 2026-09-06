# Memo to Sunday review — idea 155, the q = 0.90 trim (a SCOPING clause, not a new book)

1. **What it is.** Equal-weight the top **90%** of that week's eligible set by the existing
   composite (no vol scaler), 75% gross, weekly, t+1 — i.e. idea 72's `EWall` with its
   worst-ranked decile dropped. Per **idea 144 this is the same book re-dialled, so nothing new
   is proposed**; the clause below scopes an existing book, it does not add one.
2. **Why it is on the table.** Of 12 selectivities × 7 cost rungs × 5 panels it is the only
   q < 1 that beats not ranking at all on both primary panels at 10 bps (+0.0316 U56,
   +0.0072 B136), and it produces more 4b passes across 72 sub-panels than any other q,
   including q = 1.00 (24 vs 19 of 72 at 10 bps).
3. **4b, U56 @10 bps:** 11.30% CAGR / **1.0808** Sharpe / −16.79% MaxDD, halves 1.114 / 1.054,
   **OOS 1.1263**, turnover 9.4×/yr. Passes at 0/5/10/**15** bps.
4. **4b, B136 @10 bps:** 11.14% / 1.0325 / −18.37%, halves 1.148 / 0.925, OOS 1.0267,
   9.3×/yr. Passes at 0/5/10 bps. Cross-universe at PROTOCOL's own cost assumption.
5. **Where it dies:** the 4b **CAGR floor**, at 20 bps (U56) and 15 bps (B136). It therefore
   does **not** clear idea 82's proposed 25 bps cross-universe bar and must not be quoted as if
   it did.
6. **Rule 8, stated against the run's own answer:** the IS window would have picked q = 0.15
   (U56) / 0.10 (B136), not 0.90, and lost 0.216 of OOS Sharpe to doing nothing. **q = 0.90 is a
   full-sample number.** As a pre-registered CONSTANT it beats the no-ranking control OOS at 6 of
   7 rungs and on 56.9% of 72 sub-panels at 10 bps, falling to 43.1% at 25 bps.
7. **Exact RULES wording, if the review wants it (report-only scoping clause, not a book):**
   > *Where a book equal-weights an eligible set, it may drop the lowest-ranked decile of that
   > set (q = 0.90). Any selectivity below q = 0.80 is prohibited without a fresh 4b pass on two
   > panels: at 10 bps every q ≤ 0.80 is worse than not ranking at all on both large-cap panels,
   > and q ≤ 0.20 costs 0.10–0.19 of Sharpe. The decile trim is stated as a constant and is
   > never fitted per book.*
8. **Survivorship (idea 54)** runs against the trim's competitor, not the trim: q = 1.00 holds
   the beaten-down cohort a delisting-aware panel would kill, so the true argmax q is if anything
   lower than 0.90 and this clause is the conservative side of that bias.
9. **The clause is worth about one basis point of Sharpe per rung and decays to nothing.** Its
   value over q = 1.00 falls +0.0161 (0 bps) → +0.0103 (10) → −0.0014 (30) on the primary panels
   and +0.0098 → +0.0008 → −0.0173 over the 72 sub-panels. Reviewers should weigh it as a
   tie-break, not as an edge.
10. **Recommendation: adopt as report-only scoping wording or reject; do NOT promote a book.**
    RULES.md, scan.py, bot.py and baseline.py are untouched by this run.

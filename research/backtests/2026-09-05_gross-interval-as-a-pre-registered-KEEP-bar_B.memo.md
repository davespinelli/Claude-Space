# Memo to the Sunday review — idea 90, amended PROTOCOL proposal (lane B, 2026-09-05)

1. **No RULES change and no new book is proposed.** Idea 90's own proposal — quote the WIDTH of a
   book's 4b-passing gross interval instead of a pass/fail — is KILLED on its own evidence.
2. The object is sound: the 4b-passing set of gross multipliers is a **single contiguous interval
   in 72 of 72 non-empty books** (100%), including the four non-scale-free arms.
3. The width is not: Spearman(IS width, OOS Sharpe) **+0.540** against the binary pass/fail's
   **+0.546** and the incumbent IS-Sharpe's **+0.902**; within passing books the grade falls to
   **+0.055**.
4. As a bar it is actively harmful: at k = 1, raising w\* from 0.05 to 0.30 discards 20 of 31 books
   and **lowers** admitted mean OOS Sharpe 1.022 → 0.989. All 52 grid points are in `...bargrid.csv`.
5. What creates the OOS quality is the **cell count**: no bar 0.827 → non-empty in ≥1 cell 1.022 →
   ≥3 cells 1.039 → **all 4 cells 1.126**. That is a pass/fail count, not a width.
6. **Proposed PROTOCOL wording (rule 4b reporting clause), replacing idea 90's version:**
   *"Every 4b result shall state, for each (universe, cost rung) cell, whether the book's
   static-gross interval is non-empty, and shall report the number of cells in which it is; a
   4b KEEP requires a non-empty interval in all four large-cap cells (universe.json and
   universe_broad.json at 10 and 25 bps). It shall also report the INTERSECTION [m_lo, m_hi] of
   those cells' intervals — the range of gross the book can actually be sized at — in place of a
   single gross number. The width of any one cell's interval shall NOT be quoted as a robustness
   statistic; it has no measured out-of-sample content beyond the pass/fail it refines."*
7. Under that wording exactly **four** (book, arm) pairs qualify today, all on the EWall book:
   `vol60-dg` **m ∈ [0.95, 1.05]**, `vol60-rw` [0.90, 0.95], `band3-rw` [1.00, 1.05],
   `ddctl-8/.5/recover` m = 1.15 (m ≤ 1.30 ceiling; three of the four at m ≤ 1.00).
8. Two of those are the project's standing cross-cell 4b passers (idea 127), recovered here on an
   independent path — so the clause **confirms the incumbent rather than replacing it**, and adds
   a sizing range where RULES currently has a point.
9. **The small panel qualifies nothing**: 0 of 102 books have a non-empty interval at any gross
   level on either cost rung, which is the honest scope limit on any wording adopted.
10. Rule 8 caution against going further: a selector that picks the widest IS interval moves only
    **2 of 7** picks for +0.018 of OOS Sharpe (1.0397 vs 1.0219), one gain and one loss — so the
    interval may be reported, but must **not** be used to choose the arm or the gross.

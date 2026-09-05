# Memo — idea 199, for Sunday review. NOT a rules change; evidence only.

1. **What is KEEP-candidate here is a SELECTION RULE, not a book.** Every book in this run
   belongs to ideas 159/165/168 and is already priced; nothing new is proposed for capital.
2. On idea 178's own 11 cells, a bare pre-registered floor `n >= 25` on the IS-Sharpe argmax
   returns **+0.1297** paired OOS Sharpe (t +12.43, 11W/0L/0T) against the unconstrained
   argmax; the IS-window 4b screen it replaces returns **+0.0287** (t +1.92, 3W/0L/8T).
3. The floor fires in **11 of 11** cells; the screen fires in 4 and is structurally empty at
   25 bps and on the whole small panel. Its picks clear the OOS-window 4b in **6 of 11**
   against the screen's 2, and pass full-sample 4b in **4 of 11** against 2.
4. **Price:** OOS CAGR 13.53% → 10.96%, and cells beating SPY's OOS CAGR go **6 → 0 of 11**.
   The floor trades 4b's CAGR floor for its drawdown cap. Adopt it knowing that.
5. **Mechanism is de-concentration, not selection:** `BIGGEST BOOK` (fit nothing, take the
   largest book) already returns +0.0919; within-cell ρ(n, OOS Sharpe) = +0.489 (t +3.67) on
   the large caps and **reverses to −0.48/−0.28 on the sub-$2B panel**, where the clause does
   not apply.
6. **k = 25 is the queue's grid edge** (idea 183) and t +12.43 is a paired statistic over 11
   cells sharing three panels and one OOS window — the effective sample is well below 11. The
   defensible wording is "k in the twenties", never the point value 25.
7. Best single book the floor selects that clears 4b full-sample **and** the OOS window:
   C159/u56 @10 bps `MOM @ share 0.75, n = 28, g = 0.75` — 11.83% / 1.0676 / −17.08%,
   H1 1.092 / H2 1.052, OOS Sharpe 1.1305. Idea 159's book, not this run's.
8. SURVIVORSHIP (idea 54): current constituents only on all three panels; levels biased up.
9. **Exact RULES wording, if and only if Sunday review adopts it — as a PROTOCOL clause, not
   a change to the live book:**
   > **PROTOCOL 4c (book size).** Any walk-forward that selects a book by an in-sample
   > statistic must publish the selected book's name count `n`, and must report the same
   > selector under a pre-registered floor `n >= k` with k in the twenties. Where the two
   > differ, the floored result is the headline. The floor does not apply to panels on which
   > the within-cell Spearman of `n` against out-of-sample Sharpe is negative (as on the
   > sub-$2B panel). The IS-window 4b screen is redundant to this floor and is dropped.
10. If not adopted, the finding still stands as the reason to stop reporting the IS-window 4b
    screen: it is dominated on every axis by a rule with no parameters to fit.

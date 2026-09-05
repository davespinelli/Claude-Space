# Memo — idea 174, for the Sunday review. No RULES change; one PROTOCOL reporting clause.

1. **Not a KEEP.** Nothing here is a new book; the 151 4b-passing points are idea 171's already
   committed books re-grossed and re-sleeved (idea 144). RULES v1 stands unchanged.
2. **4b is a screen, not a wall.** At the incumbent (phi, delta) = (0.70, 0.60), 173 of 1590
   corpus points clear both coefficients and 151 clear all five bars, across 31 of 53 books.
3. `phi_max(0.60) = 0.9569` — the CAGR floor has **+0.257 of headroom** before the pair empties.
4. **The pair is one number.** A point satisfies the two coefficients iff `k = c/d >= phi/delta`.
   Incumbent requires `k >= 1.1667`; median k is 1.376 and 51 of 53 books clear it. Idea 164's
   `delta/gamma = 0.857` is the same constant inverted — two independent derivations agree.
5. **The CAGR-floor KILL count is about the ladder, not the bar.** `c ~= 0.856 x gross`, so the
   floor needs `g >~ 0.82`, and 8 of the project's 10 gross rungs sit below it: 4b pass rate is
   0.0% at every `g <= 0.60` and 10.7-23.9% at `g >= 0.70`.
6. **Proposed PROTOCOL clause (REPORT-ONLY, no bar changes) — exact wording:**
   > **11. Efficiency ratio.** Any run reporting a rule-4b CAGR-floor or drawdown-cap failure
   > must also report the book's efficiency ratio `k = (CAGR/CAGR_SPY) / (|MaxDD|/|MaxDD_SPY|)`
   > on the same window, and state whether `k >= 0.70/0.60 = 1.167`. A book with `k >= 1.167`
   > that fails either coefficient fails at the gross it was priced at, not at the bar, and the
   > run must say so; a book with `k < 1.167` cannot satisfy both coefficients at any gross and
   > is a genuine 4b failure.
7. This makes the "near-miss on the CAGR floor" family of results (ideas 152/156/161/165/177)
   readable at a glance and stops runs being spent closing gaps that de-grossing cannot close.
8. **The (phi, delta) screen is not a selector.** Rule 8: the IS-chosen pick loses to the
   do-nothing control by 0.075 of OOS Sharpe at the incumbent and in 237 of 240 non-empty cells.
   Do not add it to rule 8. Fifth consecutive instance (ideas 110/132/151/166/171).
9. The region is stable across windows: emptiness agrees in 306 of 320 cells,
   `Spearman(n_IS, n_OOS) = +0.9942`. The bar is not a window artefact either way.
10. **Caveat that must travel with clause 11:** survivorship (idea 54) biases every `k` upward,
    so `k >= 1.167` is a necessary-but-optimistic reading, and the constant 1.167 is 4b's own
    coefficients — it moves if the Sunday review ever moves phi or delta.

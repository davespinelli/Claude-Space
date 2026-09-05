# Memo to the Sunday review — idea 144 (lane C, 2026-09-05)

**Not a KEEP.** No book is proposed and no rule changes. This is a PROTOCOL wording proposal
plus one negative finding, from 7,650 backtests over idea 131's exact 306-book corpus.

1. **The pre-registered hypothesis is dead.** Dropping the ladder from the corpus does NOT make
   any 4b bar redundant: the CAGR floor still uniquely excludes 51 of 306 books (37 at the
   no-leverage ceiling) and the MaxDD cap 18 (22). 4b does not lose a bar.
2. **But it loses a degree of freedom, provably.** Under the convention the cap and the floor can
   only bind at m\* = the largest gross clearing the cap; the m\* rule reproduces the exhaustive
   family verdict in **306 of 306 books, both ceilings**. Two bars, one test.
3. **Proposed PROTOCOL 4b addendum (exact wording):** *"A static rescaling of a book's target
   weights is the SAME book, not a separate candidate, PROVIDED every parameter of its
   instrument is scale-free. The drawdown cap and the CAGR floor are then a single test applied
   at m\*, the largest gross multiplier (m ≤ 1.30 of the 75% target, i.e. no leverage) at which
   the book clears the cap: CAGR(m\*) ≥ φ·CAGR_SPY."*
4. **Proposed PROTOCOL 4 restriction (exact wording):** *"An instrument carrying an absolute-unit
   parameter (a drawdown trigger, a turnover budget) is NOT closed under rescaling and must be
   reported at each gross level separately."* Measured: scale-free arms move Sharpe ≤ 0.013 along
   their family; `ddctl`/`ebud` arms move it up to 0.292 and lose monotonicity in 45 of 72 books.
5. **Price of the convention:** admissions 29 → 58 (→72 with up-grossing), admitted-set OOS
   Sharpe 1.114 → 1.087 (→1.098). The ungated `control` book is admitted in 5 of 18 cells where
   POINT-4b admits it in 0. That concession is the whole cost and should be voted on explicitly.
6. **Rule 8:** the family screen is the first screen this project has that is not inert — it moves
   7 of 18 picks where POINT-4b moves 0 — but it buys no Sharpe (+1.1pp OOS CAGR for −1.7pp of
   drawdown, −0.003 Sharpe). Safe, not valuable: it slides the book along idea 66's line.
7. **Recommend:** adopt (3) and (4) as reporting conventions; do NOT let a screen choose m in
   rule 8 — pin m at the book's published gross, since the walk-forward says the freedom pays
   nothing and costs 1.7pp of out-of-sample drawdown.
8. **Do not adopt** any deletion of the CAGR floor or the DD cap on the strength of this run.
9. **Open:** 14 of idea 129's 27 floor-only victims are admitted once up-grossing to 97.5% is
   allowed; the other 13 still need idea 129's `4b-defensive` class.
10. Caveats that bound all of the above: survivorship (idea 54), the IS window's shallow SPY
    drawdown (idea 128), 7 paired walk-forward cells, and the calendar-day index (idea 38).

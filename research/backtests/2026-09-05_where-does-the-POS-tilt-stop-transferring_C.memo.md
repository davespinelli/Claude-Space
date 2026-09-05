# Memo — idea 162: no RULES change proposed, one PROTOCOL clause offered

1. **Nothing here is proposed for RULES.md.** The run produced 10 formal 4b passes of 132 grid
   points; all 10 are recorded on the LEADERBOARD and every one is declined below.
2. The 8 `mega20` passes (best: 12.05% / 1.337 / −12.1%, halves 1.341/1.341, OOS 1.446 at 10
   AND 25 bps) are declined for three independent reasons, any one sufficient:
   (a) `universe.json['megacap']` is the 20 largest US companies **as of 2026**, so a 2009
   start is near-pure look-ahead selection — RULES v1 itself scores 18.00%/1.121/−19.36%
   there, which is what that bias looks like;
   (b) at n=20 on a 20-name panel the book is scaler-degenerate (INV ≡ NONE ≡ POS, identical
   to the digit) and runs at mean gross **0.492**, so per ideas 144/152 its shallow drawdown
   is bought by de-grossing, not by signal;
   (c) it does not transfer — 0 of 12 arms pass 4b on every equity panel (P6).
3. The 2 `u56` passes (NONE and POS at n=20, 10 bps) are idea 2's and idea 81's known books
   re-measured, not new information, and both fail 4a.
4. **The idea's own instrument is killed by its own walk-forward.** A selector that picks the
   tilt from the panel's IS vol-premium sign returns mean OOS Sharpe 0.5818 against 0.5914 for
   plain IS-Sharpe and 0.5827 for doing nothing (NONE/n=20, and with 2.6pp less drawdown);
   it wins 3 of 22 cells. Acting on the boundary is worth less than nothing out of sample.
5. **Offered for the Sunday review as a PROTOCOL rule-9 reporting clause, verbatim:**
   "Any claim that a cross-sectional tilt's sign depends on universe size must quote the
   Fama-MacBeth t on each panel it names. The vol20 premium is significant only at the ends of
   the size ladder (u56 +0.00455 t +3.81, broad98 +0.00251 t +2.45; the sub-$2B panel's bottom
   ADV deciles only in IC space) and is indistinguishable from zero on every rung between
   `broad78` and `smADV4`. No market-capitalisation series is committed to this repo, so no
   dollar threshold may be quoted as a universe boundary."
6. RULES.md, scan.py, bot.py and baseline.py are unchanged, as required.

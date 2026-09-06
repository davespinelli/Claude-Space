# Memo to the Sunday review — idea 273 (lane C, 2026-09-06). One PROTOCOL clause; NO RULES change.

1. **Not a new book.** `RULES.md`, `scan.py`, `bot.py` and `baseline.py` are untouched. The only
   KEEP-candidate here is idea 223's MEAN-21, already on the record; this run re-derives it and
   narrows it.
2. **The finding.** Sliding the month-end schedule over its full 21-bar wrap kills **24 of the
   26** monthly 4b claims the record's memos have made (16 ANCHOR-ARTEFACT ≤10/21, 8 FRAGILE,
   2 ROBUST). The bar that breaks is the **4b drawdown cap in 24 of 24**; H1/H2/OOS/CAGR never
   break. Bands: 8.02pp (COMP-M), 8.85pp (R6-M), 10.3–10.5pp quarterly, against 4b margins of
   0.6–1.4pp.
3. **CORRECTION to the 2026-09-06 review.** The review disqualified idea 171's by-product on
   "3 of 8 anchors, MaxDD −18.41%..−21.33%". Those digits belong to a book with **SPY left in
   the ranking universe**; idea 171's script says SPY is "benchmark, never tradable". On the
   published book (control [D2]: idea 171's committed `.ladder.csv` row to 2.2e-16) the same
   slide gives **5/8 and −17.74%..−20.74%**. The disqualification's DIRECTION stands (9/21 over
   the full wrap is anchor-dependent); its NUMBER should be corrected in the record.
4. **MEAN-21, re-derived and narrowed.** u56 4b PASS at **0/5/10/25 bps** at t+1 (12.84% /
   1.1058 / −19.61%, halves 1.1737/1.0581, OOS 13.95% / 1.1280, turnover 4.85×/yr) — one rung
   wider than idea 223 published. **New limit: it FAILS 4b on drawdown at t+5 (−20.98%) and t+7
   (−21.79%), and on broad at every rung.** Averaging anchors buys certainty, not margin: the
   margin is 0.62pp and one week of fill delay spends it. Not adoptable on that basis.
5. **Rule 8.** The anchor is not selectable. IS-Sharpe-chosen phase loses **−0.0450** of OOS
   Sharpe against simply keeping the published one (4/32 wins), regret vs the OOS oracle
   −0.0946; the oracle is phase 0 in **0 of 32** cells. Average it away or report the band —
   do not pick it.
6. **Quarterly.** The record contains **zero** quarterly KEEP-candidates. Run as a
   pre-registered extension, the quarterly forms of both books clear 4b at **1 of 21** anchors
   and their band is wider than monthly (9.26pp vs 7.45pp pooled): the slower the cadence, the
   larger the anchor lottery.
7. **Proposed PROTOCOL clause (rule 4 addendum), exact wording:**

   > **Anchor band.** A KEEP-candidate whose rebalance cadence is slower than weekly must
   > report its 4b pass count over the FULL anchor wrap of its own cadence — every trading-bar
   > offset of the schedule, decision and fill slid together with the decision-to-fill gap held
   > at one bar — alongside its published anchor's numbers. A pass rate below 19 of the wrap's
   > anchors is recorded as ANCHOR-DEPENDENT, not as a 4b pass, and the candidate's MaxDD is
   > quoted as the band, not the point.

8. **Scope.** 3 books, 26 claims, u56 and broad, 2009-01-13..2026-09-04. Both panels are
   current-constituent lists (idea 54); levels are survivorship-optimistic, the phase-to-phase
   differences are same-names/same-days and are not.
9. **Reproducibility.** Controls [A]/[A2]/[B] at 1.4e-17; [C] reproduces idea 182B's committed
   `.phase.csv` on 8 phases × 17 columns to 2.2e-16; [D2] reproduces idea 171's committed
   ladder row to 2.2e-16; all three books reproduce their memos' digits (max |d| ≤ 5e-4).
10. **Recommendation.** Adopt clause 7. Correct the review's 3/8 to 5/8 in `CHANGELOG.md` when
    the record is next amended. Do **not** adopt MEAN-21 while its drawdown margin is 0.62pp
    and lag-fragile.

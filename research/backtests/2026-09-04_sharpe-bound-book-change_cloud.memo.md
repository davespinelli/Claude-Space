# Memo — idea 92 for the Sunday review (2026-09-04, cloud)

1. **Finding.** On the project's only Sharpe-bound 4b cell (`CAND20` on `universe_broad.json`,
   H2 0.814 vs SPY 0.837), of the four book changes the queue proposed only **dropping the
   ranking** moves the binding bar: ΔH2 +0.074 (n=40) → +0.114 (n=60) → +0.103 (EWall) →
   **+0.158 (ew-band3)**, all four converting the cell to a 4b pass, and +0.225 at 25 bps.
2. **Not dials** (adds to idea 84's gross and turnover-budget findings): the per-name weight
   cap is **exactly inert** on an equal-weight book (ΔH2 = +0.000 at every level, bind rate 0)
   and on a concentrated book its ceiling *is* the equal-weight book; the sector cap moves H2
   **down** at every usable tightness and posts the run's worst walk-forward regret (−0.187);
   the eligibility gate tops out at +0.042, below idea 84's own 0.05 threshold.
3. **Rule 8.** `ew-band3` is the in-sample pick of its family *and* its best out-of-sample arm
   (regret 0.000 — the only family where those coincide). OOS 11.2% / 1.074 / −16.8% vs RULES
   v1 6.0% / 0.581 and SPY 15.5% / 0.884 / −33.7%.
4. **No new candidate.** The winner is the book idea 84 already put forward at `g = 0.85`.
   This run is an independent pre-registered test that it sits on the right axis, and it
   supplies the mechanism the earlier run lacked: ew-band3 wins because it has no ranking, not
   because of its band width or its gross.
5. **Proposed RULES wording** (only if the Sunday review adopts idea 84's candidate; this memo
   changes no number in it, it supplies the clause that says *why* there is no ranking):

   > **Selection.** Hold **every** eligible name at equal weight. Do **not** rank, score, or
   > sub-select within the eligible set. Eligibility is the whole of the selection rule.

6. **Proposed PROTOCOL note** (rule 4, one line):

   > When a candidate fails 4b on a **Sharpe** bar, no exposure, turnover, weight-cap or
   > sector-cap setting will fix it (ideas 84, 92). Change the selection or abandon the book.

7. **Do not adopt the sector cap.** Its single converting arm (40%) clears H2 by +0.002, dies
   at 25 bps, and is not the arm rule 8 selects.
8. **Do not adopt a per-name weight cap** as a "risk control" on any equal-weight book — it is
   measured inert, not merely weak, and putting it in RULES would imply a control that does
   nothing.
9. **Caveat to carry into the review.** Sector labels here are a price-correlation proxy for
   GICS (11–12.5% annual label churn), so item 7 rejects *correlation-cluster* caps; a true
   GICS sector cap is untested and remains an open question.
10. **Housekeeping.** `rank <= n` selects 21 names on 22/4698 broad days (45/4698 on u56) via
    composite ties, so idea 2's literal `g/n` book runs at 0.7875 gross on those days. Harmless
    but worth a `nlargest`-style tie-break if that construction is ever adopted.

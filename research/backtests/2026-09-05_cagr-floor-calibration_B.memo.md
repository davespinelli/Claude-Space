# Memo to the Sunday review — idea 129: 4b's CAGR floor is a return preference, not a risk bar

1. **Finding.** On a 306-row corpus (3 panels × 3 books × 17 published instruments × 2 cost
   rungs, run on idea 94's imported simulator, 3/3 reproduction checks exact), 4b's CAGR floor
   is the **sole** cause of KILL for **48% of every arm that clears 4b's other four bars** —
   27 of 56 corpus-wide, 11 of 23 on the (Sharpe, MaxDD) Pareto frontier. All 11 pass 4a.
2. **The floor's victims are OOS-better, not OOS-worse.** Screened on the IS window alone and
   read once OOS: floor-only rejects (n=9) score OOS Sharpe **1.160 vs 1.056** admitted
   (+0.104, t +3.22) and OOS MaxDD **−13.4% vs −21.5%** (8.1 pp shallower, t +8.97). They lose
   only on CAGR (9.1% vs 13.4%) — the axis the floor screens on.
3. **Raising the floor buys nothing and costs drawdown.** Over all 21 (φ, δ) grid points, φ
   0 → 0.70 at δ=0.60 removes 27 of 56 admissions and moves mean admitted OOS Sharpe by
   **+0.002** while making mean admitted OOS drawdown **1.9 pp deeper**. The floor and the
   drawdown cap pull against each other.
4. **The floor is inert in selection.** Rule 8, three pre-registered selectors, 18 cells: the
   4b IS screen with the floor, without the floor, and no screen at all pick the **identical
   arm in every cell** (0 of 18 picks changed). It binds only at adoption. This reproduces
   idea 109 on a disjoint arm family.
5. **The floor is not broken and must not be deleted.** On the static-gross ladder — pure
   de-risking — it is the sole KILL in 97 of 342 rows and bites only at gross ≤ 0.80, which is
   exactly its designed job. What it cannot do is distinguish a de-grossed lever from a
   better-shaped defensive book.
6. **Proposed PROTOCOL rule 4b amendment (reporting only — no bar is moved, no rule is tuned):**

   > **4b (capital-worthy).** Sharpe > SPY in BOTH halves AND out-of-sample (rule 8), MaxDD ≤
   > 60% of SPY's, CAGR ≥ 70% of SPY's. An arm that clears the two halves bars, the OOS bar
   > and the drawdown cap and fails **only** the CAGR floor is recorded as **`4b-defensive`**,
   > not KILL: it is capital-worthy at a lower risk budget and its shortfall is a return
   > preference, not a risk failure. Every `4b-defensive` row must state its CAGR shortfall in
   > pp and its mean gross. A `4b-defensive` arm may not be adopted as the live book without a
   > gross decision, and may not be described as killed.

7. **Why a new label rather than a lower floor.** Lowering φ would be tuning a bar until things
   pass (rule 7). The floor's real content is "do not call a 10%-gross book capital-worthy",
   and the ladder control shows it still does that. The defect is only that it reports a
   *different* failure — insufficient exposure — as if it were a *risk* failure.
8. **Rows this reclassifies today.** 27 corpus rows, 11 of them Pareto-best, all EWall books
   with a slow trend gate de-grossed to cash (`band3-dg`, `g200-dg`, `v1gate-dg`, one `ddctl`)
   at ~53% gross. Exemplar u56/EWall/10 bps `band3-dg`: 8.7% / **1.206** / **−12.1%**, halves
   1.226/1.191, OOS 1.285 / −12.1%, short of the floor by 2.0 pp — the best risk-adjusted book
   in its cell. Indicatively, 288 of 1289 published leaderboard rows (22.3%) sit in this class.
9. **No RULES change this week, no candidate change.** The standing 4b candidate
   `EWall + vol60-dg` passes on both large-cap panels under both conventions and is untouched.
   This memo asks only for the PROTOCOL wording in (6).
10. **Caveat the review must weigh.** Group B is 9 correlated arm-rows in 4 cells (same book,
    overlapping series); paired counts are 3/4 on Sharpe and 4/4 on drawdown. Survivorship
    (idea 54) runs against the floor's defence, idea 128's shallow IS window runs toward
    over-admission, and every number is t+1-only (idea 126). The direction is consistent; the
    magnitude is corpus-specific.

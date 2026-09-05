# Memo — PROTOCOL clause 11b: the matched null for an OVERLAY (proposal for Sunday review)

1. Idea 181's clause 11 defines a matched null for a KEYED TILT only. This run defines and validates the
   missing one. **An overlay is a pair (s, A)** — an ON indicator over the book's rebalance dates and an
   action applied while on — and **its matched null is the same action A on a circular rotation of s.**
2. Rotation is the right null: it preserves the on-share and the circular switch count **exactly**
   (0 mismatches in 2160 draws) and destroys only *when* the overlay fires. A permutation would shatter
   episodes; a re-drawn state variable would change the construction rather than the timing.
3. **The clause's stated limit, measured not assumed:** realised turnover matches to 1.25% (DDCTL) and
   0.82% (SLEEVE) but only 25.4% mean / 213.8% max for a rebalance-SKIPPING budget. So idea 186's
   "same on-share *and* turnover" is achievable for overlays that scale or reallocate weights, and **not**
   for one that suppresses a trade. The clause must say so.
4. Proposed wording: *"Clause 11b (overlays). An instrument that acts on a state-dependent schedule must
   report its effect against N ≥ 20 matched nulls formed by circularly rotating its ON indicator over the
   rebalance dates, together with its realised ON-SHARE. An effect is reported as CLEARED only when
   |dSharpe| exceeds every matched draw. Where the action changes the rebalance schedule itself, the
   realised turnover gap between real and null must be published alongside the result."*
5. **Report-only, exactly as idea 181 concluded for tilts.** As a selection gate it is a KILL: rule 8 gives
   S2 − S0 = −0.0361 (t −2.62), winning **0 of 18** cells and abstaining in 11.
6. The fit it would gate is no better: S1 − S0 = −0.0432 (t −2.00), 6/18. Seventh consecutive project
   result (110/132/151/166/171/174/175) that an IS-fitted selector loses to doing nothing.
7. **The column earns its place as a reading, not as a filter.** It clears 17 of 108 (15.7%) and splits the
   three constructions: DDCTL 42%, BUDGET 6%, **SLEEVE 0 of 36**.
8. All 15 clearing DDCTL points have **negative** dSharpe (−0.19 to −0.52): the drawdown control is
   distinguishable from random timing and reliably harmful — independent confirmation of idea 93.
   The conditional sleeve's entire effect (−0.188..+0.032) sits inside a null band averaging 0.176.
   **527 of the LEADERBOARD's 3330 data rows mention a sleeve.**
9. It moves no verdicts: 4b identical in 91.5% of swaps, and null rows clear 4b *more* often than real ones
   (20.7% vs 16.7%). **All 18 real 4b passes here are inside their own null band.**
10. Caveats: current-constituent survivorship on all three panels (idea 54) — real and null inherit it
    identically; only J distinct rotations exist so the nominal 4.8% size is approximate; a rotation cannot
    move the sample's crises, so the clause is weaker for high-on-share overlays (BUDGET fires on 53–93% of
    dates) — which is why on-share must be published with it. **No RULES change, no new book, no KEEP.**

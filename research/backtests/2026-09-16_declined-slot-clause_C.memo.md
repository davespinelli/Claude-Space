# Memo (idea 993, lane C, 2026-09-16) — the DECLINED-SLOT clause. PROPOSED, NOT APPLIED (rule 6).

1. **Defect.** A screen that can decline to pick is scored in this record over its SURVIVING picks
   only, so a refused slot costs nothing and a screen can raise its average by not playing.
2. **Price.** Paying idea 980's refusals moves its headline median OOS Sharpe 1.0590 → 1.0011
   (25.4% of the published gain is the accounting) and its mean 1.0829 → 0.9087 (52.7%).
3. **Sign.** The gain from declining has no fixed sign: mean ΔSharpe on the emptied slots is
   −0.4703 / +0.4066 / +0.0899 for cash / SPY / the live book. It is a fallback fact.
4. **Cost.** On the D/W half the same screen empties all 4 of the control's OOS 4b passes
   (`ctrl_4b_in_emptied` 4 of 4 from floor 0.25 up); on M/Q it empties 0. Refusals are free only
   where the refused slots were worthless, and that is not knowable without scoring them.
5. **PROPOSED PROTOCOL rule 4 clause, exact wording:** *"A rule that can DECLINE to pick reports its
   statistics over ALL slots in its grid, not over the slots it filled. Every declined slot is
   scored with a NAMED FALLBACK — cash, SPY, or the live book — held for the whole evaluation
   window, and the fallback is reported beside the statistic (e.g. 'median OOS Sharpe 1.0011,
   refusals paid at FB_LIVE, 6 of 18 declined'). A screened statistic quoted over surviving picks
   alone is labelled SURVIVING-PICKS-ONLY and carries no comparison with an unscreened control."*
6. **Companion clause:** *"Report the MEAN beside the MEDIAN wherever slots are declined: once every
   fallback lands below every surviving pick the median moves only to a different order statistic
   and understates the refusal cost by a factor of ~2."*
7. **Reading rule for already-committed claims:** read every screened statistic in the record that
   names no fallback as SURVIVING-PICKS-ONLY; its gain over an unscreened control is an upper bound.
8. **Scope.** The clause is a REPORTING requirement. It changes no book, no weight, no threshold,
   and nothing in `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` or `baseline.py`.
9. **Consistency.** Idea 980 is reproduced here to the basis point (G3a/G3b/G3c, 11 of 11 gates);
   the clause re-labels its numbers, it does not contradict any of them.
10. **Not a KEEP for capital.** OOS 4a is 0 at 28 of 28 points and the best screened point loses to
    "refuse everything and hold the live book" (1.0011 / −20.00% vs 1.1061 / −12.24%). 980's PARK
    stands; this KEEP is the reporting clause alone, for the Sunday review to accept or reject.

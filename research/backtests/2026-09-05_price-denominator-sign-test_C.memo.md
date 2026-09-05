# Memo to the Sunday review — idea 122, the denominator sign test

Proposal: **amend PROTOCOL, not RULES.** No trading rule changes; no file was modified by this
run. Evidence: `2026-09-05_price-denominator-sign-test_C.result.md` (192 audited rows,
≈12,400 sub-panel backtests, idea 94's pricelist reproduced to 1.8e-15).

1. **The queue's premise does not hold on the large-cap lists.** Idea 119 found the small-panel
   denominator a coin flip; on universe.json(56) and universe_broad.json **90 of 138 published
   rates (65%) survive** a three-axis sign test. Idea 94's price list is not junk.
2. **The failures have one address: small books and shallow windows.** All 24 panel-axis and
   all 5 cost-axis failures are in the 5-name `V1u` book (admissible 16/41 vs `EWall` 47/48).
   All 40 window-axis failures are the IS half: `dMaxDD_IS ≤ 0` in 40 of 138 rows and
   `dMaxDD_OOS ≤ 0` in **0 of 138**.
3. **Proposed PROTOCOL rule 4 addition, verbatim:**
   > *Denominator sign test.* No ratio may be quoted unless its denominator's sign survives a
   > stated perturbation. For a drawdown price the denominator is
   > `dMaxDD = |MaxDD_control| − |MaxDD_arm|`, and the stated perturbation is: positive at
   > every cost rung in {0, 5, 10, 25} bps; positive in both halves of the sample; and
   > positive in at least 90% of 40 draws that delete 10% of the panel's names at random with
   > the signals recomputed on the sub-panel. A row that fails is reported as the pair
   > `(dCAGR, dMaxDD)` with the axis it failed on, never as a rate.
4. **Scope sentence that ships with it:** a price computed on a book of fewer than ~20 names,
   or in a window whose benchmark MaxDD is shallower than ~25%, has no measurable denominator
   on this data and should not be quoted at all.
5. **It is a reporting bar, not a selector — this is load-bearing.** At its stated setting the
   screen changes **0 of 12** rule-8 walk-forward picks; tightened until it binds it changes 2
   and makes **both worse** (OOS Sharpe 0.590→0.367 and 0.169→0.000).
6. **It has no out-of-sample discriminating power on these panels** (OOS denominator positive
   in 138/138 rows, admissible and rejected alike) and it retains the *dearer* half of the
   menu (median rate 0.494 vs 0.065). Adopt it to stop bad quotes, not to pick instruments.
7. **It is insensitive to its own two parameters:** all 12 (q, τ) grid points give 80–96 of
   138 admissible (58–70%). Nothing here was tuned to a number.
8. **What moves:** idea 22's headline row (`u56/TOP20/ddctl-8/.5/high`, rate 0.994) is
   admissible; idea 74's menu is quotable on `EWall`/`TOP20` but **not on V1u**; three 4b
   passes (`u56/TOP20` band3-rw @10/@25, vol60-rw @10) keep their KEEP status but lose the
   right to quote a price. Idea 117 is supported: the IS/OOS asymmetry is crisis depth.
9. **No KEEP.** 4a 54/192, 4b 29/192 across the audited grid, all inherited from idea 94; the
   walk-forward picks average OOS Sharpe 0.801 against their own control's 0.852 and SPY's
   0.882. Nothing here is capital-worthy.
10. **Caveats shipping with the wording:** both universes are current constituents; the
    calendar-day index bug (idea 38) is unfixed; 40 draws makes τ ≥ 0.95 coarse; and the test
    certifies only that a denominator has a sign, never that a price is useful.

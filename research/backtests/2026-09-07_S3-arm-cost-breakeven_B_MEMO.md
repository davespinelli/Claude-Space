# MEMO — idea 108, for Sunday review. PROPOSAL ONLY; RULES.md unchanged by this run.

1. **No adoption.** `top20 + 50% (TLT,GLD,UUP)` @ g=1.00 is not proposed for the live book: it
   fails 4a against RULES v2 at every cost from 0 to 30 bps on both universes.
2. **Its price is now a number, not a bracket:** cross-universe `c* = 16.0 bps` (u56 16.0,
   broad 16.5), contiguous, on a 0.5 bp grid — 1.60x PROTOCOL's 10 bps assumption.
3. **But the sizing number is 3.5 bps**, the cross-universe breakeven re-measured inside
   2017-2026 (broad, first-half Sharpe bar; at 10 bps that margin is already -0.0760).
4. Proposed PROTOCOL rule 4b addition, REPORT-ONLY: *"A 4b claim must quote `c*` (the highest
   cost on a 0.5 bp grid at which all five bars still pass) AND `c*_OOS` (the same bars
   re-measured inside the rule-8 OOS window). A claim whose `c*_OOS` is below the 10 bps
   costing assumption is not a capital claim."*
5. Proposed PROTOCOL rule 8 note: *"The IS-to-OOS breakeven spread is panel-signed, not
   idea-signed (u56 mean -10.7 bps, broad +4.1 bps here). Never quote a single-universe
   breakeven as an idea's cost budget."*
6. Correction to carry forward: idea 101's "4a on both universes to 25 bps" is a **RULES v1**
   statement (true, and censored — the real value is >=30). Under RULES v2 it is 4a-never.
7. Correction to carry forward: idea 108's own premise, "the CAGR floor binding first", holds
   on u56 only; broad binds on H2, and H1 is the modal binding bar (20 of the 40 passing cells).
8. What survives intact: rule 8 picks f=0.50 in **122/122** rungs of the candidate cell at zero
   regret — idea 101's selector result is robust across the entire cost ladder.
9. Standing blocker unchanged from idea 101: absolute levels rest on current-constituent
   panels (idea 54), so `c*` is biased up and `c*_OOS` is the conservative read.
10. Recommended record change: mark idea 101's S3 arm **4b (cost-qualified, c*=16.0 /
    c*_OOS=3.5)** rather than an unqualified 4b KEEP.

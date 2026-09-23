# Memo — idea 2457, the 4a KEEP-candidate (lane B, run 50, 2026-09-23).  FILED, NOT ADOPTED.

1. **What it is.** Hold every instrument inside the 200d +/-3% hysteretic band at a FIXED 1.25% of
   NAV each (no shared denominator), sweep the residual into SHY, weekly, t+1, 10 bps.
2. **Headline (U56, SHY sweep, 10 bps):** CAGR 8.40%, Sharpe 1.2946, MaxDD -10.43%, halves
   1.3076 / 1.2947, OOS (2017-2026) 9.56% / 1.3808 / -10.43%, turnover 2.52x/yr.
3. **Path 4a, and only 4a.** Sharpe beats live RULES v2 in BOTH halves (1.2262 / 1.1897) and MaxDD
   is shallower than the live book's -12.05%.  It passes 4a at 0 / 10 / 25 bps under both sweep
   conventions — 10 of 192 rows, the first 4a passes since 2326.
4. **It FAILS 4b, on `L_CAGR` alone:** 8.40% against the 0.70 x SPY floor of 10.66%, margin
   -2.26 pp.  `L_H1`, `L_H2`, `L_OOS` and `L_DD` all clear (DD margin +9.80 pp).
5. **Why it is not adopted.** It is the live book DE-GROSSED, not a new edge: CAGR per unit of
   realised risk gross is 17.48% against FLOAT's 17.29% and 17.06-17.14% for every other arm, and
   turnover per unit of risk gross is 5.24 against FLOAT's 5.22.  Nothing improved; less was held.
6. **Rule 8 does not pick it.** Of the 8 U56 IS-only picks (2 sweeps x 4 rungs x 2 choosers),
   0 land on `w* = 0.0125`; 17 of the 32 picks overall take FLOAT, the committed sizing.
7. **It does not replicate on B136.** Joint both-panel 4b is 0 of 16 for this arm, and it carries
   no 4a pass there at all.  A one-panel 4a is a panel fact, not a book.
8. **Survivorship (rule 9):** U56 is CURRENT constituents held from 2008, so `L_CAGR` — the leg
   this candidate fails — is the most contaminated leg, and the true failure margin is wider.
9. **Exact RULES wording, if a Sunday review ever wanted it (4a path, max one change per week):**
   *"Clause 3 (sizing).  Hold each instrument whose band state is IN at 1.25% of NAV, independent
   of the number of names held; hold nothing else; sweep `1 - sum(w)` into SHY.  Scale the whole
   risk book by `min(1, G / sum(w))` so gross never exceeds G = 0.75.  No ranking, no vol filter."*
10. **Recommendation: DO NOT ADOPT.**  A 4a pass bought by holding less is a gross decision, not a
   rule change, and it is strictly dominated by lowering G on the committed rule, which needs no
   new clause at all.  The standing 4b candidate, its `L_DD` leg and its 3.51x turnover blocker
   are unchanged by this run.

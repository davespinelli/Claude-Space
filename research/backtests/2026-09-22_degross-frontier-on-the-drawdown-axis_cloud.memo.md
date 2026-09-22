# MEMO — KEEP-4b candidate, RECORDED AND NOT RECOMMENDED (idea 1545, lane cloud, 2026-09-22)

1. **Book.** U56 panel, top-20 by 126-day momentum among names above their 200d MA with
   vol20 < 0.60, equal weight at gross 0.75, weekly, next-day execution, 10 bps — the frozen
   2026-09-04 anchor — with a constant-volatility-target overlay at **v = 0.20**.
2. **Exact RULES wording if ever adopted:** *"Scale the whole book by
   `min(1, 0.20 / sigma20)`, where `sigma20` is the 20-day realised annualised volatility of
   the book's OWN net return series through close t, applied at t+1; withdrawn weight goes to
   cash and is never re-spread."*
3. **Tuned parameters: two and no more** — (N, H) = (20, 126), frozen at the committed
   anchor and not searched here.  v is the published ladder axis, chosen by rule 8.
4. **Full sample (2009-01-13..2026-09-18):** CAGR 12.25%, Sharpe 1.0741, MaxDD -16.70%,
   halves 1.0937 / 1.0609.  SPY: 15.14%, 0.8851, -33.72%, halves 0.9570 / 0.8264.
5. **Out of sample (v chosen on 2009-2016 only; 2017-2026 read ONCE):** CAGR 13.39%,
   Sharpe 1.1238, MaxDD -16.70%.  SPY OOS: 15.29%, 0.8751, -33.72%.
6. **4b legs, all five cleared:** H1 1.0937 > 0.9570; H2 1.0609 > 0.8264; OOS Sharpe
   1.1238 > 0.8751; MaxDD -16.70% inside the -20.23% cap (+3.53 pp); CAGR 12.25% over the
   10.60% floor (+1.65 pp).  **4a: FAILS** (MaxDD -16.70% against live RULES v2's -12.05%).
7. **Rule-8 reachable:** yes — both published IS-only rulers (IS Sharpe, IS Calmar) pick
   v = 0.20 within the VOLTGT family on all three panels, with 2017-2026 never consulted.
8. **NOT RECOMMENDED, reason 1 — grid edge.**  v = 0.20 is the loosest rung on the ladder;
   the record's standing reading of a chooser that lands on the ladder end is that it is
   declining to act, not selecting.
9. **NOT RECOMMENDED, reason 2 — it barely binds.**  Realised mean gross 0.7174 against the
   un-overlaid book's 0.7196: 0.3% of exposure withdrawn.  Nearly the whole 4b pass is the
   frozen anchor's, which the record already holds; the overlay adds 1.29 pp of OOS MaxDD
   and 0.0105 of OOS Sharpe over it.
10. **What IS new and worth the record's attention:** VOLTGT is the ONLY one of six device
    families that sits strictly OUTSIDE the constant de-gross (CAGR, MaxDD) frontier, at
    10 of 10 U56/B136 cells, in BOTH the full sample and 2017-2026 read alone (15 of 15
    cells agree across windows).  The binding rungs v = 0.08-0.15 cut MaxDD to -10.8% ..
    -15.1% while staying outside the frontier — but **no legal IS-only ruler picks them**,
    so they are PARK, not KEEP, until a chooser that reaches them is found and priced.

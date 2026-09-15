# Memo — offset-blind reporting, and the weekly incumbent (idea 938, lane B, 2026-09-15)

1. **Status: PARK, not KEEP.** Nothing here is promotable today: 4a is 0 of 30 offsets on both
   cadences, and idea 924's answer-key finding still bars capital claims on the U56 panel.
2. **The defect this run found is a REPORTING defect.** Every M-vs-W comparison in the record
   was read at one rebalance phase out of 21, and that phase is the maximum of its own family
   at 16 of 16 grid points (4 panel × claim-set cells × 4 cost rungs).
3. **Exact PROTOCOL wording, if a Sunday review wants it** (rule 6 — this memo does not apply
   it; PROTOCOL.md is untouched by this run):
   > **10. Offset spread (required for any claim that compares rebalance CADENCES):** a book
   > whose cadence is coarser than weekly must be priced at every trading-day phase of its
   > rebalance period (21 for monthly, 5 for weekly) and published as `min / median / max`
   > beside the headline. A cadence claim whose headline phase sits above the 90th percentile
   > of its own phase family is PARK, not KEEP, and the median-phase number is the one quoted.
4. **What that clause would have done to the record:** U56 M/CORE/TOP20's +2.09 pp would have
   been published as **+0.13 / +1.04 / +2.09 pp** and flagged (percentile 1.000).
5. **The part of the 2.09 pp that survives** is the **+0.60 pp of cost drag** (turnover 4.32 vs
   9.48 units/yr at 10 bps) — phase-invariant, mechanical, and the only part worth quoting.
6. **The part that does not** is +1.49 pp of gross return at the canonical phase against
   **+0.45 pp at the median phase and −0.46 pp at the worst**; at 0 bps the gap is negative at
   4 of 25 monthly offsets.
7. **The weekly twin (U56 W/CORE/TOP20, g=0.75, 10 bps) is the offset-robust one:** 4b PASS at
   **5 of 5** weekly phases against the monthly book's 7 of 25, with MaxDD support −18.31% …
   −14.32% against −22.95% … −14.89%. It is the 2026-09-04 KEEP-4b incumbent and this run
   strengthens it rather than replacing anything.
8. **Its exact RULES wording, if a future Sunday review ever promotes it** (not proposed today):
   > Hold the 20 highest-scoring instruments (composite momentum rank, NO vol scaling) that are
   > above their 200-day average with 20-day realised vol < 0.60, equal weight at 0.75/20 of NAV
   > each, rebalanced on the last trading day of each week, applied at the next close; names
   > failing the gate go to cash and the gross is not re-spread.
9. **Blocking conditions on that wording, all live today:** (a) 4a FAIL — Sharpe 1.088 against
   RULES v2's 1.201, MaxDD −18.31% against −12.05%; (b) idea 924 — the U56 panel's only
   4b-bearing sleeve is a 2026 answer key; (c) rule 8 reaches it 0 of 4 IS choosers here.
10. **Do not read this memo as a case for monthly rebalancing anywhere in the record.** The
    honest statement of the cadence result is: offset-blind, the monthly book beats the weekly
    book by **+0.013 of Sharpe**, and 17 of its 25 offsets sit at or below the best weekly phase.

# Memo (idea 981, lane B, 2026-09-15) — PROPOSED, NOT APPLIED (rule 6)

1. **Finding.** 4b's binding leg is a CADENCE object: `L4_DD` fails on 0.633 / 0.647 / 0.832 /
   0.927 of 2,700 matched-gross phase-books at D / W / M / Q, and is the modal failed leg in only
   6 of 12 (panel × cadence) cells — never at daily, never on SMALL.
2. **Reporting clause, proposed for PROTOCOL rule 4 (wording):** *"A claim that a leg of 4b binds,
   or that 4b is a drawdown test, is reported with the CADENCE it was measured at. It generalises
   across cadences only if the same leg is modal at D and W as well as at M and Q."*
3. That clause scopes ideas 968 (89.2%, quarterly) and 976 (36 of 36, M/Q) without contradicting
   either: both are reproduced here exactly (G3 2,520 of 2,520 rows at max|d| 1.776e-15; G4 36 of 36).
4. **Candidate, for completeness, NOT a new rule.** The run's only OOS 4b passers are one object:
   **U56 / BAND03 / gross 1.00** — the LIVE book run at full gross — daily **12.46% / 1.288 /
   −14.77%** and weekly **12.68% / 1.277 / −15.91%**, against SPY OOS 15.27% / 0.874 / −33.72%.
5. The weekly row reproduces idea 973's and idea 982's committed pick to the basis point; this is
   the third independent arrival at it from three different questions.
6. **Exact RULES wording, if a Sunday review ever adopts it:** *"RULES v2 clause 3 — gross G is
   1.00 rather than 0.75; every other clause is unchanged."* Nothing else in RULES.md would move.
7. **Why it is NOT recommended here.** 4a fails on every panel (0 of 36 OOS, 5 of 2,700 full
   sample): at gross 1.00 the drawdown is −15.9% against the live book's −12.1%, so this trades
   one third more drawdown for one third more return.
8. Ideas 973 and 982 both surfaced the same object and both declined to promote it. This run
   agrees and records the third refusal rather than the third sighting.
9. **Survivorship (rule 9):** U56 is a current-constituent list, so the 12.68% and the −15.91%
   are both optimistic; the SPY comparand is not.
10. Applied here: nothing. `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and `baseline.py` are
    untouched. Both clauses are for the Sunday review, max one change per week (rule 6).

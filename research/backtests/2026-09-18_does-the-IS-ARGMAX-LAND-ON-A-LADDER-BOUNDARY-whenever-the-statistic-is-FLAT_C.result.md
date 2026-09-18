# 1195 (lane C, 2026-09-18) — does the IS argmax land on a ladder boundary whenever the statistic is FLAT?

**ANSWERED, AND THE ANSWER REFUTES THE PROPOSED MECHANISM.** 36 cells (3 panels x 4 ladders x 3
statistics), 8 rungs each, anchor N=20/H=126/g=0.75/W, IS = warm-up..2016-12-31, OOS read once.

1. **BOUNDARY LANDING IS REAL AND COMMON: 0.528 of 36 cells against a 0.250 chance line** (U56 0.583,
   B135 0.500, SMALL663 0.500; mean bootstrap P_BOUND 0.486). That part of 1189 stands.
2. **IT IS NOT A FLATNESS FACT.** rho(FLAT_RATIO, BOUNDARY) = **+0.1527** (ALL4) / +0.0689
   (NONGROSS3) — the WRONG SIGN for the proposed mechanism, since low FLAT_RATIO means flat. At all
   six non-degenerate dial points the FLAT group's boundary rate is at or BELOW the non-flat group's
   (diff -0.031, -0.208, -0.548 on ALL4; -0.400, -0.079 on NONGROSS3).
3. **MONOTONICITY IS THE PREDICTOR.** rho(|rank corr of the IS statistic with rung position|,
   BOUNDARY) = **+0.7807** (ALL4) / +0.6668 (NONGROSS3); boundary rate **0.882 at MONO >= 0.90 (17
   cells) vs 0.211 at MONO < 0.90 (19 cells)**. An argmax lands at an end because the statistic is
   ordered in the dial, flat or not.
4. **1189's OWN CELL SHOWS THE CONFOUND.** GROSS is boundary at 9 of 9 cells while its FLAT_RATIO is
   0.64-1.77 on Sharpe and 1.27-3.86 on CAGR/MaxDD: the same ladder is flat on one statistic and the
   steepest of the four on another, and lands on a boundary either way (MONO = 1.000 on all three).
5. **CAPITAL — KILL.** Acting on ANY IS argmax costs **-0.0454 of OOS Sharpe** (positive at 11 of
   36; worst -0.2629, U56/N/CAGR -> N=5) and **-0.0262 of OOS MaxDD (worse at 29 of 36)** against
   simply holding the anchor. **4a 0 of 36 picks and 0 of 87 rung books; 4b 3 of 36 picks, 11 of 87
   books.** IS/OOS Sharpe rank correlation over rungs mean +0.2083 (positive at 24 of 36).
6. **GATES 8 of 9.** G8 (CROSS-RUN 1189) **FAILS AND IS PUBLISHED, NOT REPAIRED**: the IS-Sharpe
   argmax is the TOP gross rung at **3 of 3 panels here, against 1189's committed 2 of 3**. Cause:
   the panels are not the same objects — B135 not B136, and SMALL663 is the pool rebuilt 2026-09-11
   (ideas 1072/1074's label drift). The direction of 1189's reading survives; its count does not.
7. **BYCATCH, PARK NOT KEEP.** U56 N=12/H=126/g=0.75/W (1084's parked book) is **4b PASS** — 17.69%
   CAGR, 1.1687 Sharpe, MaxDD -20.169% (0.061pp inside the -20.2304% cap), OOS Sharpe 1.1751 — and
   on THIS 8-rung N ladder it IS the IS-Sharpe argmax (IS 1.1664), i.e. rule-8 reachable. But 1084's
   9-rung ladder {5..40} sent the same chooser to N=40: **the reach is a rung-set artefact**, and the
   rung set is a choice nobody pre-registered. It stays PARK, and its DD margin is 1259's complaint.
8. **SURVIVORSHIP (rule 9):** U56/B135 are current-constituent lists, SMALL663 a current sub-$2B
   screen; levels are optimistic and every 4b pass is an UPPER bound. The headline is a within-panel
   contrast between cells, which is first-order immune; the 4b legs and the 0.061pp margin are not.
9. **CLAUSE THIS SUPPORTS:** a published argmax should carry its ladder's MONOTONICITY, not its
   flatness. A flatness bar would have cleared 24 of 36 cells at F_BAR=2 while explaining nothing.
10. Script: `2026-09-18_does-the-IS-ARGMAX-LAND-ON-A-LADDER-BOUNDARY-whenever-the-statistic-is-FLAT_C.py`

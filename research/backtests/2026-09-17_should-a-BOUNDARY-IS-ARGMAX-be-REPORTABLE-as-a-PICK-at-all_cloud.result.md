# Idea 1217 (cloud lane, 2026-09-17) — should a BOUNDARY IS-ARGMAX be REPORTABLE as a PICK at all?

**ANSWERED = YES AS A SCHEMA FLAG, NO AS A CHOOSER — AND THE QUESTION IS SECOND-ORDER, BECAUSE
NO IS-ARGMAX PICK PAYS ON THIS GRID AT ALL.**

**ARM 1, THE CENSUS.** 40,988 committed pick rows harvested from **71** committed
`*.walkforward.csv` / `*.picks.csv` artefacts over 82 (file, ladder) reconstructions. Under
**B_STRICT** (the pick is its ladder's min or max rung) the rule would have **SUPPRESSED 19,313
of 40,988 committed pick rows = 47.1%**; C_LADRUNG 46.8%, C_PICK 49.3%. Under **B_WIDE** 83.2%,
but **39.4%** of those sit on ladders shorter than 2k+1 rungs and are boundary *by construction*
— reported in its own column, not folded into the headline. Suppressed picks carry a **higher**
mean committed OOS Sharpe (1.3371 against 1.2559 kept) and a **shallower** mean committed OOS
MaxDD (-13.09% against -13.72%), i.e. in the record as published the boundary picks do not look
like the bad ones — which is exactly why a flag, not a filter, is the right instrument.

**RECOVERY LIMIT, STATED NOT HIDDEN (1152's finding).** The record rarely states a ladder's rung
LIST beside a pick, so each ladder's list is reconstructed from the distinct rung values the file
itself publishes. That under-estimates the true ladder whenever a run published part of its grid,
and an under-estimated list **inflates** the boundary rate. 47.1% is therefore an upper bound on
the true suppression rate.

**ARM 2, THE PRICE.** A decision row is (panel, ladder) — 1205's own construction. Gates G13/G16
reproduce 1205 exactly: U56 GROSS=1.00 MaxDD **-24.9276%** against its committed -24.93%, and the
frozen rung **-19.1276%** against -19.13%.

*Where the boundary habit lives* (primary cadence, B_STRICT): **GROSS 0.9585** of its picks (modal
rung **1.00**, the ladder's top, on a statistic that runs 1.1463 → 1.1485 across the whole ladder,
a spread of **0.0022**), **H 0.6528** (modal rung 252, also the top), **N 0.2383**, **CADENCE
0.0000** (unordered, never flagged). Claim set ALL4 0.4624, NG 0.2971. This is 1189's "flat in
gross" and 1209's monotone-ladder finding arriving as a *selection* fact: GROSS's argmax is the
ladder's end because the ladder ran out, not because the data located a maximum.

*What suppression costs or saves* (ALL4 / NG, against the record's CH_ARGMAX habit, mean over
rule-8 decision rows; paired per-fold SE in brackets):

| bdef | chooser | dSharpe ALL4 | dMaxDD ALL4 | dSharpe NG | dMaxDD NG |
|---|---|---|---|---|---|
| B_STRICT | CH_SUPP_ANCHOR | +0.0084 | +2.36pp | -0.0000 | +0.74pp |
| B_STRICT | CH_SUPP_INTERIOR | -0.0054 | +1.03pp | -0.0115 | -0.04pp |
| B_WIDE | CH_SUPP_ANCHOR | +0.0424 | +2.98pp | +0.0474 | +1.57pp |
| B_WIDE | CH_SUPP_INTERIOR | +0.0479 | +2.82pp | +0.0567 | +1.35pp |

Every paired per-fold t restricted to the folds where the rule actually fired is **|t| <= 0.6**
(357 / 511 fired folds at ALL4, 172 / 323 at NG). **PRE-DECLARED OUTCOME: (B) REPORT AS IS** — the
(A) test was keyed to B_STRICT / CH_SUPP_INTERIOR, which is a wash. POST-HOC AND LABELLED AS SUCH:
the boundary width behaves like a dial on *how much picking the rule does*, not like a diagnostic
that separates good picks from bad — the wider the suppression, the closer the chooser gets to
doing nothing, and the better it does.

**THE DOMINANT FACT.** Doing nothing beats every pick rule on this grid: **CH_ANCHOR OOS Sharpe
0.8845 / MaxDD -25.23% / 4b 4 of 12**, against the record's habit **0.8268 / -28.74% / 4b 0 of
12** and against every suppressed variant. Rule 8 per panel: U56's IS choice is ALL4 / B_NONE /
**CH_ANCHOR** (OOS 17.16% / 1.1759 / -19.13%, 4b 4 of 4) — the walk-forward selected *not
picking*; B136's is NG / B_STRICT / CH_SUPP_INTERIOR (14.23% / 0.9039 / -23.21%, 4b 0 of 3)
against its habit 15.92% / 0.9285 / -24.15% and its anchor 16.29% / 1.0240 / -20.74%; SMALL's is
NG / B_NONE / CH_ARGMAX (7.30% / 0.4681 / -36.86%, 4b 0 of 3) against anchor 7.09% / 0.4534 /
-35.81%. SPY OOS 15.15% / 0.8686 / -33.72% (B136/SMALL span 15.33% / 0.8769); live RULES v2 OOS
9.42% / 1.2717 / -12.05%.

**BOTH KEEP PATHS.** 60 rung books: **4a 0**, 4b full 13, 4b OOS 12, BOTH 12. Boundary rungs
specifically (18 books): 4b full **1**, mean OOS Sharpe 0.8417 and mean OOS MaxDD -26.99%, against
interior rungs (42 books) 0.8735 and -24.79%. 288 stitched curves: **4a 0**, 4b full 44, 4b OOS
44. Rule 8 over 288 distinct OOS rows: **4a 0, 4b 44** — all already-committed books.

**VERDICT: KILL (capital)**, no new book, no memo, no RULES change. The boundary rule is worth
proposing as a **SCHEMA clause** for the Sunday review (rule 6: proposed, not enacted) — flag any
published pick whose rung is at its ladder's boundary, and require the rung list beside it — but
it is **not** a chooser and this run does not offer it as one.

**SURVIVORSHIP (rule 9).** B136 and SMALL are current constituents; SMALL is the sub-$2B screen
with 51 of 715 tickers dropped for max_1d_move >= 1.0 (664 investable), SPY benchmark only. The
bias does not cancel out of the OOS levels or the 4b legs, so any pass there is an upper bound.
The census arm reads committed text and carries no market bias at all.

**GATES 16 of 16.** Runtime 23s, offline, deterministic.

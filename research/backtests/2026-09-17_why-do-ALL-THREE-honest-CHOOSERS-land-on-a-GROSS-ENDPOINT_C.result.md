# Idea 1154 (lane C, 2026-09-17) — why-do-ALL-THREE-honest-CHOOSERS-land-on-a-GROSS-ENDPOINT

**ANSWERED = BECAUSE THE GROSS DIAL IS EXACTLY MONOTONE AND ARGMAX-OF-MONOTONE IS AN
IDENTITY — and the queue's companion claim, that 1150's passing band "is unreachable by
any of them", is REFUTED: a fourth equally honest IS-only chooser reaches it, on both
panels, and its pick is the ONLY gross-dial pick that clears 4b full AND 4b OOS.**
No RULES change, no PROTOCOL edit (rule 6); RULES.md, PROTOCOL.md, scan.py, bot.py,
engine.py and baseline.py untouched. SELECTION: lane C takes the SECOND open idea; 1154 was
second in `## Open` and is not EDGAR / Form 4 / 8-K / options / live-data. Pure price run.

**THE TWO TUNED PARAMETERS AND NO MORE (rule 4, and the two the queue names):**
`CHOOSER` {C_ISSHARPE, C_ISCAGR, C_ISDD, C_ISMAR, C_IS4B} x `DIAL` {D_GROSS 33 rungs, D_N 11,
D_HOLD 9, D_CADENCE 6, D_MAXVOL 7} = **25 cells per panel, 50 in all, every one published**
in `.mono.csv` / `.picks.csv` / `.premium.csv`. The RUNG inside a dial is **not** a third
parameter — it is the object the chooser selects, which is the subject of the run, and all
**132 rungs (66 per panel) are published in `.grid.csv`** whatever any chooser did with them.
PANEL {U56, B136} is not a dial. Every chooser is **IS-only** (2009-01..2016-12-31); none can
see one bar after `IS_END`, so each of the 50 picks *is* a rule-8 decision. Frozen at
1082/1094/1098/1102/1108/1110/1116/1117/1118/1150's construction: CAND20 legs, cap INF,
max_vol 0.60, min hold 126, N=20, gross 0.75, W, **10 bps (rule 2 — a book cannot choose its
cost rate)**, LAG 1, warm-up 260, zero cash, block L=63, 1000 draws, crc32 seeds, q=0.90.

**THE QUESTION WAS SPLIT BEFORE ANY NUMBER WAS READ, BECAUSE HALF OF IT IS AN IDENTITY.**
"Is an endpoint pick a general property of a MONOTONE dial?" is **true by algebra** — the
argmax of a weakly monotone sequence is always attainable at an end. **G9 verifies it on
20,000 synthetic sequences precisely so this run cannot be read as having discovered it.**
The empirical content is the other three questions: how often a dial *is* monotone in the
statistic a chooser reads, whether the **converse** holds, and Q2's premium.

**GATES 10 of 10 PASS, printed before any result number.** G1 fast runner == `engine.backtest`
1.39e-17; G2 committed U56 W/H126/N=20 triple 4.12e-05 (15.5793% / 1.1397 / -19.1276%);
G3 SPY OOS 1.70e-04; G4 1098/1102's committed U56 n=12 triple 4.71e-05; G5 live RULES v2
MaxDD 4.95e-05; G6 determinism 0.00e+00; G7 `cadence_mask` == `engine.rebalance_mask` 0 bars;
**G8 1150's three committed gross-dial picks reproduce at 0 of 6 mismatches** — the object
under test is replayed exactly before anything new is read; G9 the identity; G10 the ladders
nest the record's committed rungs. **PRICE VINTAGE PINNED at 2026-09-15** (idea 1160's
defect, 2026-09-17): the same G2 on the unpinned file reads **1.62e-03, 39.4x the pinned
reading, from ONE extra bar of 4,706** — published, not absorbed.

**THE ANSWER, PART 1 — THE GROSS DIAL IS MONOTONE AT 8 OF 8 LEVEL CELLS, rho = ±1.000.**
IS Sharpe **up** (rho +1.000), IS CAGR **up**, IS MaxDD **down**, IS MAR **up**, on both
panels. So all four of those choosers land on an endpoint *by identity*, and the three
1150 published are not three independent facts but one. **And H_GROSSFLAT — this run's own
pre-registered guess that IS Sharpe would be FLAT-and-noisy rather than monotone — is
REFUTED: it is exactly monotone, with a total spread of 0.0021 (U56) / 0.0057 (B136) of
Sharpe end to end.** Monotone and economically nil at the same time: on U56 that slope is
worth **+0.130 paired bootstrap SD**, i.e. **C_ISSHARPE's gross-1.00 pick is unresolvable**
even though it is mechanically certain, while C_ISCAGR's (+3.15 SD) and C_ISDD's (+3.72 SD)
are real. Same pick, three different strengths of reason.

**THE ANSWER, PART 2 — IT IS A PROPERTY OF THE GROSS DIAL, NOT OF IS-ONLY CHOOSING.**
Across the other four dials monotonicity holds at **0 of 40** cells and the picks go
**interior at 23 of 40**. Endpoint share by dial: D_GROSS 8/10, D_MAXVOL 9/10, D_CADENCE
5/10, D_N 3/10, **D_HOLD 0/10**. Overall **25 of 50 picks are interior.** 1150's
three-for-three is the gross ladder's shape, and generalising it to choosers would have
been wrong.

**THE ANSWER, PART 3 — THE CONVERSE FAILS, SO AN ENDPOINT PICK IS NOT EVIDENCE OF A
MONOTONE DIAL. 17 of the 42 NON-monotone cells (40.5%) still pick an endpoint**, D_MAXVOL
9 of 10 among them (median mono_score 0.500 — a jumble, not a ladder). And those endpoint
preferences are **not resolvable: |need|/SD < 1 at 88.2% of them, median 0.464 SD.**
Reading "it picked the end, so the dial must be monotone" backwards off a published argmax
is unsafe at two cells in five.

**Q2, THE INTERIOR PREMIUM — AND THE CHOOSER THAT REACHES IT.** `need` = best endpoint −
best interior in the chooser's own units, with the paired block-bootstrap SD of that very
difference (same 1,000 draws on both arms, IS window, so the tape cancels). **The one
chooser that is NOT monotone on the gross dial is `C_IS4B` — the min of the three IS-only
4b leg margins — and it lands at gross 0.625 (U56) and 0.575 (B136), deep in the interior,
by need −0.496 = −3.04 SD and −0.606 = −3.43 SD.** The mechanism is visible in one column
of `.grid.csv`: over the whole U56 ladder the IS Sharpe margin `M_S` is flat
(**0.2353 -> 0.2377**), `M_DD` falls monotonically (**+0.7127 -> −0.3903**) and `M_CAGR`
rises monotonically (**−0.6485 -> +0.7738**). **A min of two oppositely-sloped monotone legs
is a TENT, and a tent peaks in the interior.** That is the whole of Q2's answer: to reach
the interior a chooser must read a statistic with at least two monotone components of
opposite sign combined so that neither can run away — a *ratio* is not enough (C_ISMAR is
CAGR/|MaxDD| and is still monotone up, picking 1.00 on both panels), a *min* is.

**RULE 8 AND BOTH KEEP PATHS — 132 cells, 50 IS-only picks, and THE QUEUE'S "UNREACHABLE"
IS REFUTED.** Benchmarks, pinned: **U56 SPY full 15.10% / 0.8829 / −33.72% (halves
0.9588/0.8207), OOS 15.21% / 0.8711 / −33.72%; live RULES v2 8.62% / 1.2008 / −12.05%
(OOS 9.46% / 1.2763). B136 SPY 15.16% / 0.8861 / −33.72% (halves 0.9596/0.8259), OOS 15.33%
/ 0.8767 / −33.72%; live RULES v2 7.98% / 1.0993 / −12.24% (OOS 7.88% / 1.1059).**
Ladder base rates: **4b full 35 of 132, 4b OOS 38, BOTH 34 (25.8%), 4a 0 of 132.**
Chooser picks: **4b full 5, 4b OOS 5, BOTH 5 of 50 (10.0%), 4a 0 of 50** — H_NOPAY holds,
picks clear 4b at **under half** the rate of the rungs they were picked from. But it is no
longer zero: **1150's "0 of 48" was a property of its three choosers, not of honest
choosing.** The five that pass, all rule-8 honest:

| panel | dial | chooser | pick | full CAGR / Sharpe / MaxDD | halves | OOS CAGR / Sharpe / MaxDD |
|---|---|---|---|---|---|---|
| U56 | D_GROSS | C_IS4B | 0.625 | 12.96% / 1.1393 / −16.12% | 1.2034 / 1.0966 | 14.10% / 1.1639 / −16.12% |
| B136 | D_GROSS | C_IS4B | 0.575 | 12.29% / 1.0620 / −16.18% | 1.2884 / 0.8829 | 12.30% / 1.0084 / −16.18% |
| U56 | D_HOLD | C_ISDD | 10 | 13.51% / 1.0936 / −19.33% | 1.1318 / 1.0684 | 15.07% / 1.1485 / −19.33% |
| U56 | D_HOLD | C_IS4B | 10 | 13.51% / 1.0936 / −19.33% | 1.1318 / 1.0684 | 15.07% / 1.1485 / −19.33% |
| U56 | D_MAXVOL | C_ISCAGR | 2.00 | 16.30% / 1.1628 / **−20.16%** | 1.2718 / 1.0936 | 17.79% / 1.1690 / −20.16% |

**4a is 0 of 132 and 0 of 50** — the live book's −12.05% drawdown is not beaten by anything
on any of these ladders, exactly as the record keeps finding.

**WHAT THIS IS NOT, STATED PLAINLY.** It is **not a new edge**. Every passing gross rung is
the standing top-20 / W / H126 family the record already holds and has PARKED, scaled: at
U56 gross 0.575 / 0.625 / 0.750 the full Sharpe reads **1.1391 / 1.1393 / 1.1397** and the
OOS Sharpe **1.1637 / 1.1639 / 1.1644** — the whole 11-rung passing window (0.525..0.775) is
one book at different exposures, which is 1150's identity. What is new is that the exposure
point can be **selected ex ante by an IS-only rule instead of asserted**. And the honest
caveat: **C_IS4B maximises IS versions of the very legs 4b later tests**, so its full-sample
pass is partly tautological; the part that is not is the **OOS** pass, which the chooser
could not see, and the fact that the incumbent 0.75 **fails** 4b on B136 (−20.74% drawdown
against the −20.23% cap) where C_IS4B's 0.575 passes. The U56 D_MAXVOL row passes its
drawdown leg by **0.07 pp** and should be read as a boundary cell, not a candidate.

**SURVIVORSHIP (rule 9).** U56 and B136 are CURRENT-CONSTITUENT panels, so every CAGR and
drawdown LEVEL here is optimistic and both 4b exposure legs are measured against an inflated
book. The bias does not cancel out of the pass/fail table. It very largely does cancel out
of this run's headline, which is about the SHAPE of a statistic across rungs of one dial on
one tape and about paired differences between two rungs of the same book.

**WHAT THE RECORD SHOULD DO WITH IT, STATED NARROWLY (proposed, NOT enacted — rule 6).**
(1) A published argmax on a dial should state whether the statistic is **monotone** over that
dial; if it is, the argmax is an identity and carries no information about the dial. (2) The
converse must not be run backwards: 40.5% of non-monotone cells here still pick an endpoint,
88.2% of them by under one SD. (3) 1150's "the passing band is unreachable by any honest
chooser" should be re-quoted as **"unreachable by a chooser that reads a monotone statistic"**
— a min-of-opposing-legs chooser reaches it on both panels.

Script `research/backtests/2026-09-17_why-do-ALL-THREE-honest-CHOOSERS-land-on-a-GROSS-ENDPOINT_C.py`,
8 CSVs, console log, memo, 4 LEADERBOARD rows. Follow-ups filed 1161, 1162, 1163.

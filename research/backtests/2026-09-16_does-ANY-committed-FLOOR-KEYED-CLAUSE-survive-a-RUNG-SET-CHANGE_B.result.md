# Idea 1131 (lane B, 2026-09-16) — does ANY committed FLOOR-KEYED clause in the record survive a RUNG-SET change?

**ANSWERED = YES, BUT ONLY A MINORITY, AND THE MINORITY IS A NAMED SHORT LIST. 623 of 1,451
committed floor-keyed objects on a ladder whose rung set can move are RUNG-ROBUST; 823 are
RUNG-ESCAPABLE and 0 are RUNG-INDUCED.** At the block level the answer is exact and small:
of the 16 (panel, ladder, statistic) blocks on the two ladders whose rung set actually
changes, **7 survive the CORE -> EXT move and 9 do not**, and only **6** survive *every* one
of the 31 supersets of CORE inside EXT. The survivors are **DD on all four blocks, plus H /
S_FULL on both panels** — nothing else. **KILL of the general reading that a whole-ladder
INF_FLOOR trigger is a tape fact**, a **CORRECTION** to how the record's committed INF_FLOOR
census should be quoted, and a **KILL of the "add rungs" mental model of escape** — the
trigger is not monotone in rungs. No RULES change, no book promoted, no PROTOCOL edit (rule
6); RULES.md, PROTOCOL.md, engine.py, scan.py, bot.py and baseline.py untouched.

**SELECTION:** lane B takes the LAST open idea; 1131 ended '## Open' and names no EDGAR /
Form 4 / 8-K / options / live-data source. It has a PRICE LEG — 74 books over 4 ladders x 2
panels, two rung sets, block-bootstrapped at 3 seed bases — so it carries this run's
mandatory rule-8 walk-forward and both KEEP paths.

## THE TWO DIALS AND NO MORE (PROTOCOL rule 4)
`CLAIM SET` {CS_CELL, CS_PROSE, CS_ALL} x `RUNG SET` {CORE, EXT} = **6 combinations, ALL
published**. PANEL, LADDER and STATISTIC are not dials (all 2 x 4 x 4 rebuilt cells reported
everywhere). **CONFIDENCE q is NOT a dial**: 0.90 is the headline, 0.80 and 0.95 are reported
beside it at every point and nothing is selected on them. **The ALL-vs-ANY reading of a
multi-cell prose claim is NOT a dial either**: ALL is the record's own wording
(1110/1116/1117) and is the headline; ANY is reported beside it. Frozen at
1082/1094/1098/1102/1108/1110/1116/1117/1118/1122's construction: CAND20 legs, cap INF,
max_vol 0.60, gross 0.75, min hold 126, N=20, W, 10 bps, LAG 1, warm-up 260, IS end
2016-12-31, block L=63, 1000 draws, crc32 seeds, 3 seed bases.

## GATES 12 of 12 PASS, printed before any result number
G1 fast runner == `engine.backtest` 1.39e-17; G2 committed U56 W/H126/N=20 triple 3.18e-07
(15.5787% / 1.1397 / -19.1276%); G3 SPY OOS 1.70e-04; G4 / G4b committed U56 n=12 and B136
n=15 triples 4.97e-05 / 2.13e-05; G5 live RULES v2 MaxDD -12.05% at 4.95e-05; G6 determinism
0.00e+00; G7 `cadence_mask` == `engine.rebalance_mask` on D/W/M/Q, 0 differing bars (engine.py
not modified); **G8 reproduces all 54 rows of 1110's committed CORE grid at 0.00e+00**; **G9
reproduces 1117's committed trigger counts on all 32 shared-seed rows at 0.00e+00**; **G10
reproduces all 32 of 1110's committed argmax PEAKS with 0 mismatches** (1 of 32 INF-flag
mismatches, reported and NOT gated — the flag is a redraw quantity, 1108/1116's finding); G11
every ladder x statistic live (min spread 1.79e-03). **HYPOTHESES 4 of 6.**

## THE STRUCTURAL FACT, STATED BEFORE THE CENSUS BECAUSE IT BOUNDS IT
CORE and EXT differ **only** on H (4 -> 9) and CADENCE (4 -> 9). N (9) and GROSS (10) carry
**identical** rung lists at both levels — the same defect 1134 found when it read 4 surviving
GROSS cells as 2 books. **Any committed object keyed only on N or GROSS is rung-inescapable
BY CONSTRUCTION and is excluded from the headline denominator**, which is why this run reports
`mv_*` columns (movers only) beside the raw counts rather than a single pooled share.

## THE HARVEST, AND ITS HONEST LIMIT
Mechanical and published in full. **CSV arm 2,571 committed rows over 18 files** — every row
of a committed `research/backtests/*.csv` carrying a `ladder` column and an INF-flag field
(`inf`, `inf_floor`, `inf_count`, `inf_*`, or a `floor` column literally `inf`), kept whether
the flag fires or not so the denominator is honest. **PROSE arm 9 committed clause / bar /
verdict sentences**: a sentence qualifies only if it carries BOTH a whole-ladder trigger
phrase AND a decision word, with its cells read from its committed LINE. **26,323 CSV rows
are rejected for carrying no INF_FLOOR field at all, 693 for carrying no flag on the row, and
263 prose sentences are rejected — 170 NO_LADDER_NAMED, 71 QUOTES_A_FLOOR_NO_DECISION, 22 on
the SMALL panel this run cannot rebuild. Every reject is published with its reason.** **THE
LIMIT, NAMED: the prose arm is 9 objects.** The record argues its floors in CSVs and in prose
that mostly does not put a ladder name in the same committed line as the trigger, so the prose
verdict rests on a handful of sentences and the weight of this run sits on the CSV arm.

## THE CENSUS (q=0.90, reading ALL, headline base)
| claim set | n | movers | ESCAPABLE | INDUCED | ROBUST | escape share of movers |
|---|---|---|---|---|---|---|
| CS_CELL | 2,571 | 1,445 | 822 | 0 | 623 | **0.5689** |
| CS_PROSE | 9 | 6 | 1 | 0 | 0 | 0.1667 |
| CS_ALL | 2,580 | 1,451 | 823 | 0 | 623 | **0.5672** |

Restricted to objects whose **committed flag actually FIRED as published** — the number the
idea literally asks for — **CS_ALL 639 of 1,226 are ESCAPABLE (0.5212) and 582 are ROBUST**.
**H_DIRECTION SUPPORTED at 823 to 0:** every single move runs one way, exactly as 1118's
mechanism predicts. Over 3 seed bases x 3 q levels x 2 readings the escape share of movers
runs **0.2102 to 0.5691**, so the level is seed- and q-sensitive and the *direction* is not.

## THE BLOCK-LEVEL ANSWER, WHICH IS THE ONE WORTH QUOTING
| | S_FULL | S_OOS | CAGR | DD |
|---|---|---|---|---|
| U56 H | ROBUST | ROBUST | ESCAPABLE | ROBUST |
| U56 CADENCE | ESCAPABLE | ESCAPABLE | ESCAPABLE | ROBUST |
| B136 H | ROBUST | ESCAPABLE | ESCAPABLE | ROBUST |
| B136 CADENCE | ESCAPABLE | ESCAPABLE | ESCAPABLE | ROBUST |

**7 of 16 ROBUST, 9 ESCAPABLE, 0 INDUCED.** **DD is un-resolvable at every rung set on every
block** and is the only statistic that is. A committed floor-keyed claim on **DD**, or on
**H / S_FULL**, is worth quoting; one on **CADENCE at anything but DD**, or on **CAGR
anywhere**, is not.

## THE FATAL DETAIL: THE TRIGGER IS NOT MONOTONE IN RUNGS (H_CHEAP_ESCAPE SUPPORTED)
Exhaustive over all 31 non-empty supersets of CORE inside EXT, per block — no sampling. **Of
the 16 blocks that fire at CORE, 10 can be silenced and 6 cannot be silenced by ANY superset.
Median ESCAPE COST is 1 rung** (max 2). The cheapest escapes are named: U56 H / CAGR by adding
**H=42** alone, U56 CADENCE / S_FULL by adding **2D**, B136 CADENCE / CAGR by adding **2W**.
**And the escape is not "run more rungs": U56 H / S_OOS still fires on the FULL 9-rung EXT
ladder yet falls silent once H=210 alone is added.** Adding rungs is neither necessary nor
sufficient — *which* rungs is what decides — so a clause keyed on a whole-ladder floor cannot
be policed by mandating a rung count either.

## H_COUNT_NOT_ID REFUTED, AND THE REFUTATION IS A CORRECTION TO THE RECORD
At matched k=4, only **1,396 of 2,016 (0.6925)** four-rung subsets of the EXT ladders fire,
against CORE firing in **16 of 16**. Per (panel, ladder), the share of subsets firing at all
four statistics at once is **U56 H 0.5079, U56 CADENCE 0.0952, B136 H 0.7143, B136 CADENCE
0.1825** — product **6.31e-03**. **POST-HOC AND LABELLED AS SUCH:** 1110/1116's rung set is
not a typical 4-rung ladder, it is one that fires where most do not. So the record's committed
INF_FLOOR census is not merely rung-*count* dependent (1118's finding); it rests on a rung
*choice* that fires far more often than a uniformly drawn one of the same size. Quoting
"18 of 32 infinite floors" without naming the rung list overstates how un-resolvable this tape
is.

## H_UNDECLARED REFUTED, AND THE NUMBER IS STILL BAD
**935 of 2,571 committed floor-keyed CSV rows (0.3637) do not state the rung set they were
computed on** — fewer than the majority the hypothesis predicted, so it is recorded as
REFUTED, but for more than a third of the record's floor-keyed rows a reader cannot perform
the check this run performs. 1,151 declare CORE and 485 declare EXT.

## RULE 8 AND BOTH KEEP PATHS — NOTHING PROPOSED
No claim set and no rung set can move a book: the BOOK at every rung is byte-identical across
both dials — only which committed objects get *called* fired changes — so 4a and 4b are
invariant to dial 1 and dial 2 by construction; scored anyway because rule 4 requires it. Rung
chosen on IS 2009-2016 ALONE, per ladder, three choosers, OOS read ONCE: **6 of 48 picks clear
4b full AND OOS; 0 of 48 clear 4a.** Whole grid, 74 rungs: **4b full 17, 4b OOS 18, 4a 0.**
Every passing pick is the standing anchor U56 / W / H=126 / N=20 / gross 0.75 (full 15.58% /
1.1397 / -19.13%, halves 1.2037 / 1.0971, OOS 16.97% / 1.1643 / -19.13%), a cell the record
already holds and has already PARKED, and every one of the six is the ladder's FROZEN DEFAULT
rung re-picked. Benchmarks: U56 SPY full 15.10% / 0.8829 / -33.72% (halves 0.9588 / 0.8207),
OOS 15.21% / 0.8711 / -33.72%; U56 RULES v2 live 8.62% / 1.2007 / -12.05%, OOS 9.45% / 1.2762
/ -12.05%; B136 SPY full 15.16% / 0.8861 / -33.72%, OOS 15.33% / 0.8767 / -33.72%; B136 RULES
v2 7.98% / 1.0993 / -12.24%, OOS 7.88% / 1.1059 / -12.24%. **Nothing new, nothing promoted, no
RULES memo written.**

## WHAT THE RECORD SHOULD DO WITH IT, STATED NARROWLY (proposed, NOT enacted — rule 6)
1122's rule — *a clause is rung-stable iff every quantity in its trigger is a property of the
peak and its own pair, never of the ladder* — is confirmed on a corpus of 2,580 objects rather
than two clauses, and **strengthened**: a whole-ladder trigger is not only rung-*count*
dependent, it is rung-*choice* dependent and non-monotone, so fixing the rung count does not
repair it. **Any committed floor-keyed claim should quote its rung LIST, not its rung count**,
and the 9 ESCAPABLE blocks above should not be cited as tape facts. Filed as ideas 1139-1141 (filed as 1136-1138 and renumbered on push after a lane collision, idea 932's defect again).

## THE DECLARED APPROXIMATION, AND ITS DIRECTION
The corpus is harvested from committed artifacts, so a floor-keyed claim the record made only
in a console log or a script comment is not counted; that omission can only **shrink** the
census, never change a classification. The prose arm's ALL reading takes a multi-cell claim to
fire only when every cell it names fires, which is the record's own wording and is the
**conservative** direction for ESCAPABLE (a claim that fires on fewer cells is harder to
silence); the ANY reading is reported beside it and moves the escape share by at most 0.073.
Blocks on the SMALL panel, and ladders outside {N, H, GROSS, CADENCE}, are **not rebuildable
here** and are published as rejects with that reason rather than scored.

## SURVIVORSHIP (rule 9)
U56 and B136 are CURRENT-CONSTITUENT panels, so every level is optimistic. A rung-to-rung gap
and a rung-to-rung agreement both contrast two books over the same inflated tape and the bias
very largely cancels out of them, out of the floor and out of every quantity classified here;
it does **not** cancel out of the 4b legs, measured against SPY, a real index, so the 17
full-sample 4b passes are an UPPER bound.

Script `research/backtests/2026-09-16_does-ANY-committed-FLOOR-KEYED-CLAUSE-survive-a-RUNG-SET-CHANGE_B.py`,
15 CSVs, console log, 5 LEADERBOARD rows.

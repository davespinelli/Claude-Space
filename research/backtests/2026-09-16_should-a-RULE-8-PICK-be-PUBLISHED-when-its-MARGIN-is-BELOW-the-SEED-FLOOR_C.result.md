# Idea 1100 (lane C, 2026-09-16) — should a RULE-8 PICK be PUBLISHED AT ALL when its MARGIN is BELOW the SEED FLOOR?

**ANSWERED = NO, AND THE QUEUE'S REMEDY IS WORSE THAN THE DISEASE. KILL of "publish it as a
TIE SET instead".** A rule-8 pick is not prose: it names the book that gets the capital, so
substituting its tie set substitutes a *different book*, and at the record's own resolution that
substitution **manufactures 16 4b passes and destroys 20** over the five floor multiples covering
all 14 committed picks. A convention that moves the verdict in both directions is not an honesty
fix. The census half is answered separately and it is the more useful half: **only 30 of 479
committed pick-carrying files (0.063; 12,208 of 79,368 pick rows, 0.154) publish the margin that
decided the pick at all**, and 877's 0.0145 seed floor is the wrong ruler for the ones that do —
the cells' OWN 90% resolution is a **median 12.9x larger**. No RULES change, no PROTOCOL edit
(rule 6): the clause below is STATED for the Sunday review, not enacted. RULES.md, PROTOCOL.md,
engine.py, scan.py, bot.py and baseline.py untouched.

## What was run

Two dials and no more, the queue's own: `CLAIM SET` {CS_CORE, CS_WIDE, CS_ALL} x `FLOOR MULTIPLE`
m {0, 0.5, 1, 2, 3} of 877's 0.0145 = **15 points, all published**. PANEL (U56, B136), LADDER (all
7) and CHOOSER are **not** dials and are reported everywhere; the headline chooser is C_ISSHARPE
because the floor is quoted in Sharpe units, and C_ISDD / C_ISCAGR margins are reported beside it
in their own units and compared to nothing. 10 bps, LAG 1, warm-up 260, IS end 2016-12-31; the
claim sets and ladders are **1096's, verbatim** (L_N, L_H, L_G, L_CAD core; L_NH, L_BOOK, L_MV
wide; 146 cells over two panels). Bootstrap L=63, 1000 crc32-seeded draws, **diagnostic only —
nothing is selected on it**.

**GATES 7 of 7 PASS**, printed before any result number: G1 fast runner == `engine.backtest`
1.39e-17; G2 committed U56 W/H126/N=20 triple 3.18e-07 (15.5787% / 1.1397 / −19.1276%); G3 SPY OOS
1.70e-04; **G4 CROSS-RUN — this run reproduces 1096's committed `margins.csv` at 9.71e-17 on all
14 margins, 14 of 14 the same pick rung**; G5 live RULES v2 MaxDD 4.95e-05; G6 determinism 0.00e+00;
**G7 at m=0 the tie set is the singleton {argmax} and the two books are identical, 0.00e+00**.

## The two books

| | what it is |
|---|---|
| **ARGMAX** | the rung the IS-only chooser names — the record's current publication |
| **TIE** | equal capital to every rung within m x 0.0145 of it, run as \|S\| sleeves, costs inside each sleeve, **no netting between sleeves** (so every TIE-minus-ARGMAX figure is conservative *for* the tie set) |

The headline blend holds the sleeves at equal weight daily — a free cross-sleeve rebalance. The
**no-rebalance DRIFT blend** is computed for every row beside it: signs agree on 31 of 35
multi-rung rows, but its median OOS-Sharpe change is **−0.0011 where the blend's is +0.0026**, so
part of the tie set's apparent gain is the free rebalance and not the tie set.

## The 15 dial points (all published)

| claim set | m | floor | n | below | mean tie | whole-ladder | med dOOS Sharpe | tie wins | 4b full A->T | 4b OOS A->T | **manufactured** |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CS_CORE | 0.0 | 0.0000 | 8 | 0 | 1.00 | 0 | +0.0000 | 0/8 | 3->3 | 3->3 | 0 |
| CS_CORE | 0.5 | 0.0073 | 8 | 2 | 3.25 | 2 | +0.0000 | 0/8 | 3->4 | 3->4 | **2** |
| CS_CORE | 1.0 | 0.0145 | 8 | 6 | 4.00 | 2 | +0.0000 | 3/8 | 3->3 | 3->3 | **4** |
| CS_CORE | 2.0 | 0.0290 | 8 | 7 | 4.12 | 2 | +0.0013 | 4/8 | 3->3 | 3->3 | **4** |
| CS_CORE | 3.0 | 0.0435 | 8 | 7 | 4.62 | 3 | +0.0013 | 4/8 | 3->3 | 3->3 | **4** |
| CS_WIDE | 0.0 | 0.0000 | 6 | 0 | 1.00 | 0 | +0.0000 | 0/6 | 2->2 | 2->2 | 0 |
| CS_WIDE | 0.5 | 0.0073 | 6 | 2 | 1.33 | 0 | +0.0000 | 1/6 | 2->1 | 2->1 | 0 |
| CS_WIDE | 1.0 | 0.0145 | 6 | 2 | 1.67 | 0 | +0.0000 | 1/6 | 2->1 | 2->1 | 0 |
| CS_WIDE | 2.0 | 0.0290 | 6 | 4 | 2.83 | 0 | +0.0000 | 2/6 | 2->1 | 2->1 | 0 |
| CS_WIDE | 3.0 | 0.0435 | 6 | 5 | 3.50 | 0 | +0.0148 | 4/6 | 2->2 | 2->2 | **2** |
| **CS_ALL** | 0.0 | 0.0000 | 14 | 0 | 1.00 | 0 | +0.0000 | 0/14 | 5->5 | 5->5 | 0 |
| **CS_ALL** | 0.5 | 0.0073 | 14 | 4 | 2.43 | 2 | +0.0000 | 1/14 | 5->5 | 5->5 | **2** |
| **CS_ALL** | **1.0** | **0.0145** | **14** | **8** | **3.00** | **2** | **+0.0000** | **4/14** | **5->4** | **5->4** | **4** |
| **CS_ALL** | 2.0 | 0.0290 | 14 | 11 | 3.57 | 2 | +0.0000 | 6/14 | 5->4 | 5->4 | **4** |
| **CS_ALL** | 3.0 | 0.0435 | 14 | 12 | 4.14 | 3 | +0.0062 | 8/14 | 5->5 | 5->5 | **6** |

"manufactured" counts 4b FAIL -> PASS conversions on the full and OOS windows together; the
reverse direction totals **20** over CS_ALL's five multiples against **16** manufactured.

## The picks, their margins and their OWN resolution (C_ISSHARPE, 10 bps)

| panel | ladder | pick vs runner-up | margin | spread | m/spread | own res (90%) | agree | < 0.0145 |
|---|---|---|---|---|---|---|---|---|
| U56 | L_N | 40 vs 12 | 0.0101 | 0.1518 | 0.066 | 0.2172 | 0.513 | **yes** |
| U56 | L_H | 21 vs 63 | 0.0085 | 0.1981 | 0.043 | 0.2045 | 0.509 | **yes** |
| U56 | L_G | 0.75 vs 0.70 | **0.0001** | 0.0014 | 0.078 | 0.0003 | 0.714 | **yes** |
| U56 | L_CAD | W vs M | 0.0078 | 0.0363 | 0.216 | 0.1510 | 0.517 | **yes** |
| U56 | L_NH | 12/21 vs 5/63 | 0.0020 | 0.3770 | 0.005 | 0.3371 | 0.516 | **yes** |
| U56 | L_BOOK | TOP10 vs TOP5 | 0.0242 | 0.1710 | 0.142 | 0.2021 | 0.570 | no |
| U56 | L_MV | 9.99 vs 0.40 | 0.0194 | 0.0911 | 0.213 | 0.1800 | 0.536 | no |
| B136 | L_N | 8 vs 5 | 0.0094 | 0.1870 | 0.050 | 0.1829 | 0.529 | **yes** |
| B136 | L_H | 63 vs 126 | 0.0559 | 0.2877 | 0.194 | 0.2336 | 0.657 | no |
| B136 | L_G | 0.75 vs 0.70 | 0.0003 | 0.0034 | 0.098 | 0.0003 | **0.956** | **yes** |
| B136 | L_CAD | W vs D | 0.0205 | 0.0936 | 0.219 | 0.1915 | 0.554 | no |
| B136 | L_NH | 5/63 vs 8/63 | 0.1238 | 0.5010 | 0.247 | 0.1355 | **0.933** | no |
| B136 | L_BOOK | TOP5 vs TOP10 | **0.0001** | 0.2520 | 0.000 | 0.2071 | 0.500 | **yes** |
| B136 | L_MV | 0.40 vs 0.60 | 0.0405 | 0.1173 | 0.346 | 0.1248 | 0.700 | no |

**8 of 14 below the floor — 1096's D4 count reproduces exactly.** Median margin/spread **0.120**:
the typical published pick beats its runner-up by an eighth of what separates the ladder's ends.
C_ISDD margins run 0.00080–0.03520 (median 0.00757) and C_ISCAGR 0.00044–0.03865 (median 0.01042),
in their own units, compared to nothing.

## Hypotheses: 3 of 6 supported, and the three failures are the finding

- **(a) H_BELOW PASS.** 8 of 14 below 0.0145 at m=1, 1096's D4 to the pick.
- **(b) H_NOINFO FAIL.** The argmax's median OOS-Sharpe advantage over the other members of its
  own tie set is **+0.0018** (8 multi-rung sets), mean OOS rank inside the tie set **0.625**
  against 0.5 for no information. Tiny, but the wrong sign for the queue's premise: the peak of an
  unresolved set is not OOS-worthless, so replacing it with the set is a real trade, not a
  restatement.
- **(c) H_TIE_NOWORSE FAIL.** The tie book's OOS Sharpe beats or matches the argmax's in **4 of
  8** below-floor picks — exactly half, not a majority. Median change over them +0.0038, over all
  14 **+0.0000**. Tie-setting is a coin flip, not a free upgrade.
- **(d) H_NO_MANUFACTURE FAIL — the disqualifying one.** **16 FAIL -> PASS** and **20 PASS -> FAIL**
  over CS_ALL's five multiples. At m=1 alone: U56 L_N's tie {12, 40} converts a 4b FAIL into a
  **PASS on both windows**, B136 L_G's whole-ladder tie does the same, while U56 L_H, L_CAD and
  L_NH each lose a pass they held. A publication convention that can turn a failing book into a
  4b-clearing one **by widening the sentence that describes it** is disqualified whatever else it
  does.
- **(e) H_FLOOR_LAX PASS, and it cuts both ways.** The cells' own 90% resolution exceeds 0.0145 in
  **12 of 14** cells (median 0.1872, **12.9x the seed floor**), and only **2 of 14 picks are
  decided at q=0.90** (B136 L_G 0.956, B136 L_NH 0.933). On the two GROSS ladders the transfer runs
  the *other* way: own resolution 0.0003, i.e. **0.022x** the seed floor, so 877's number calls
  B136 L_G's 0.0003 margin unresolved while the ladder's own bootstrap resolves its sign at 0.956.
  **0.0145 is not this record's resolution in either direction.**
- **(f) H_DECISION applied as declared -> NO** (below 8/14 yes, median dOOS Sharpe +0.0000 yes,
  manufactured 16 — the third leg fails).

## The clause, drafted (STATED for the Sunday review, NOT enacted — PROTOCOL rule 6)

> **PROPOSED PROTOCOL 8b — A RULE-8 PICK CARRIES ITS MARGIN AND ITS LADDER'S RESOLUTION, AND IS
> STILL PUBLISHED AS A RUNG.** A result naming a rung chosen by an IS-only chooser shall quote
> beside it: (i) the **MARGIN** to the runner-up in the chooser's own statistic and units; (ii) the
> **SPREAD** of the ladder in those units; and (iii) the ladder's **OWN measured resolution** at
> the declared confidence — never a floor transferred from another construction. Where the margin
> is below that resolution the pick shall be published **as a rung with its margin marked
> UNRESOLVED**, and shall **not** be replaced by a tie-set book: substituting the set changes the
> book and therefore the 4a/4b verdict, which is a research result requiring its own walk-forward,
> not a change of wording.

## RULE 8 and both KEEP paths — nothing proposed

Rungs chosen on **2009–2016 alone**, OOS 2017–2026 read once. Benchmarks: U56 SPY 15.10% /
0.8829 / −33.72% full (halves 0.9588 / 0.8207), OOS 15.21% / 0.8711 / −33.72%; B136 SPY 15.16% /
0.8861 / −33.72%, OOS 15.33% / 0.8767 / −33.72%; live RULES v2 U56 8.62% / 1.2007 / −12.05%, OOS
9.45% / 1.2762 / −12.05%; B136 7.98% / 1.0993 / −12.24%, OOS 7.88% / 1.1059 / −12.24%.

ARGMAX publications **4b full 25 / 4b OOS 25 / 4a 0** of 70; TIE publications **23 / 23 / 0** of 70;
the whole 146-cell grid **4b full 33, 4b OOS 36, 4a 0**. **4a is empty everywhere**, as it has been
at every rung since 1096.

**14 of 70 tie books clear 4b full AND 4b OOS, and none is proposed.** The best of them, U56 L_N
m=1 tie {12, 40} — full 15.63% / **1.1845** / −20.09% (halves 1.3020 / 1.0968), OOS 16.51% /
1.1807 / −20.09% — is **not** put forward, for reasons fixed before it was read: its DD leg clears
by **0.14 percentage points** (−20.09% against the cap's −20.23%); it is a two-sleeve blend of the
standing top-20 family that gives up OOS CAGR (16.51% vs the incumbent rung's 16.97%) and MaxDD
(−20.09% vs −19.13%) for +0.045 of full-sample Sharpe; and it exists only because of the very
substitution this run's own headline finds moves verdicts 16 one way and 20 the other. Promoting
a book off a convention this run just killed would be exactly the tuning PROTOCOL rule 7 forbids.
The U56 and B136 GROSS whole-ladder ties clear 4b at every m >= 0.5 by **de-grossing** (OOS MaxDD
−13.68% / −14.84%) and are the same trade the record has priced repeatedly; also not proposed.

## Corpus — how much of the record publishes the margin that decided its pick

**479 committed .csv files in `research/backtests` carry a `pick` column (79,368 pick rows). 30 of
them carry a margin beside it (12,208 rows) — 0.063 of files and 0.154 of rows.** This is a schema
scan of the committed record, not a re-derivation of any claim. The consequence is flat: for
roughly six of every seven published pick rows, **no reader can check the pick against any floor,
because the number that decided it was never written down.** That, not the tie set, is the cheap
fix the idea was looking for.

## Survivorship (PROTOCOL rule 9)

U56 and B136 are CURRENT-CONSTITUENT panels, so every level above is optimistic. A margin and a
TIE-minus-ARGMAX difference contrast two books over the same inflated tape and the bias very
largely cancels out of them; it does **not** cancel out of the 4b legs, which are measured against
SPY, a real index — so every 4b pass counted here, argmax or tie, is an upper bound.

## Declared transfers and their direction

(i) 877's 0.0145 is a SEED-noise floor measured on placebo arms; applying it to a deterministic
IS-Sharpe pick margin is a transfer, declared in advance and checked against each cell's own
bootstrap resolution (H_FLOOR_LAX, which finds it wrong by 12.9x in one direction and 45x in the
other). (ii) The TIE book nets no trades between sleeves, so its cost is an upper bound and every
TIE-minus-ARGMAX figure understates the tie set's case — the KILL survives that slack. (iii)
C_ISDD and C_ISCAGR margins are in MaxDD and CAGR units and are compared to no Sharpe floor
anywhere above.

## Files

`.margins.csv` (42 picks x 3 choosers, margins, spreads, own resolution, agreement),
`.ties.csv` (70 tie sets with both books, both blends, all verdicts), `.grid.csv` (the 15 dial
points), `.cells.csv` (all 146 rungs, full/OOS/4a/4b), `.walkforward.csv` (140 publications),
`.corpus.csv` (479 pick-carrying files), `.benchmarks.csv`, `.gates.csv`, `.hypotheses.csv`,
`.console.txt`.

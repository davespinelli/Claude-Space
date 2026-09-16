# Idea 1136 (cloud lane, 2026-09-16) — is 877's SEED FLOOR the RIGHT RULER for a DETERMINISTIC MARGIN at all?

**ANSWERED = NO, AND THE NUMBER IS 116 OF 116. Every committed floor transfer in the record
that asserts a margin is RESOLVED is refused by the destination cell's own measured
resolution — all 116 of them, at q=0.90, in the same direction, with zero exceptions — and
the own ruler resolves 0 of 263 admissible transfers in total.** The declared headline
statistic says something weaker (116 of 263 = 0.4411 flip, so **H_WRONG_RULER is REFUTED as
declared**), and that is reported as declared: the unconditional share is bounded above by
the share of objects that assert RESOLVED at all, so it could never have exceeded 0.4411 on
this corpus. **The declared statistic was the wrong cut, and that is the run's own error,
recorded rather than re-cut into a pass.** KILL of 0.0145 as a ruler for a deterministic
pick margin. No RULES change, no book promoted, no PROTOCOL edit (rule 6); RULES.md,
PROTOCOL.md, engine.py, scan.py, bot.py and baseline.py untouched.

**SELECTION:** this lane takes the FIRST eligible open idea (idea 1 of 2); 1136 headed
'## Open' and names no EDGAR / Form 4 / 8-K / options / spin-off / live-data source. It has
a price leg — 146 books over 7 ladders x 2 panels, 42 rule-8 picks — so it carries this
run's mandatory rule-8 walk-forward and both KEEP paths.

## THE TWO DIALS AND NO MORE (PROTOCOL rule 4)

`CLAIM SET` {CS_CSV, CS_PROSE, CS_ALL} x `CONFIDENCE q` {0.50, 0.68, 0.80, 0.90, 0.95} =
**15 points, ALL published** in `.grid.csv`. PANEL (U56, B136), LADDER (all 7) and CHOOSER
are **not** dials and are reported everywhere; the headline chooser is C_ISSHARPE because
the floor is quoted in Sharpe units. The **OWN-RULER READING is not a dial either**:
HALFWIDTH is the headline (it is a number in 0.0145's own units and can be substituted for
it literally) and AGREEMENT is reported beside it at every one of the 15 points, never
selected on. Block length frozen at L=63, 1000 draws, `zlib.crc32` seeds, base 11361136.
Everything else frozen at 1096/1100's construction: CAND20 legs, cap INF, max_vol 0.60
(except L_MV), gross 0.75 (except L_G), W (except L_CAD), min hold 126 (except L_H), N=20
(L_N free, L_H at 12), 10 bps, LAG 1, warm-up 260, IS end 2016-12-31.

## THE TWO RULERS, DEFINED BEFORE ANY NUMBER

| | what it is |
|---|---|
| **TRANSFER** | the object's own imported floor, m x 0.0145. 877/871 measured it by **redrawing a placebo arm's seed**. It carries **no confidence**, which is the defect under test. |
| **OWN** | the destination cell's measured resolution at q: the half-width of the two-sided q interval of the **paired** block-bootstrap pick-minus-runner-up difference, on the **IS window only** — the window the chooser sees. Beside it, never substituted for it: **AGREEMENT**, the share of draws in which the sign of that difference survives. |

The substitution is not a change of units, it is a change of *object*. A seed floor prices
how far a Sharpe moves when a placebo is redrawn. A rule-8 pick margin is a deterministic
function of one tape, and the only sampling uncertainty in it is the **tape's**. Nothing in
the record had priced that swap as a verdict.

## GATES 10 of 10 PASS, printed before any result number

G1 fast runner == `engine.backtest` 1.39e-17; G2 committed U56 W/H126/N=20 triple 3.18e-07
(15.5787% / 1.1397 / −19.1276%); G3 SPY OOS 1.70e-04; G5 live RULES v2 MaxDD 4.95e-05;
G6 determinism 0.00e+00; **G4 CROSS-RUN — reproduces 1100's committed `margins.csv` on all
14 margins and spreads at 9.71e-17, 14 of 14 the same pick rung**; **G7 reproduces 1096's
committed `above_877_seed_floor` flags on all 14 rows at 0.00e+00**; G8 the own half-width
is monotone non-decreasing in q at every cell (min increment 5.84e-05 — a ruler that ran
backwards in q would not be a ruler); G9 every ladder live (min IS-Sharpe spread 1.39e-03);
**G10 the BOOK grid is 1100's committed 146-rung grid at 1.78e-15**. G10's bar is stated as
**1e-12 = CSV round-trip precision, NOT exact 0**: the comparand is a round-trip of the same
float, so a 0.0 bar is one no correct run can pass, and the measured value is printed either
way. **HYPOTHESES 3 of 5.**

## THE HARVEST, AND ITS HONEST LIMIT

Mechanical, and every reject published. **CSV arm 224 objects over 2 committed files** —
every row of a committed `research/backtests/*.csv` carrying `panel`, `ladder`, a
margin-like column and at least one column that compares that margin to an **imported**
floor (`below_m*`, `above_877_seed_floor`). **PROSE arm 179 objects over 4 committed files**
— a line qualifies only if it carries a floor token AND a decision word AND names a
destination this run can rebuild. **69 prose lines rejected: 48 QUOTES_FLOOR_NO_DECISION,
21 NO_CELL_NAMED**, all published with their reason.

**THREE FILES ARE CONTROLS, NOT TRANSFERS**, and they are the record's own good practice:
`2026-09-11_should-PROTOCOL-quote-the-4a-leg-as-a-COUNT-not-a-SHARE_C.census.csv`
(`below_own_floor`), and 1110's and the 9-rung-argmax run's `.floor.csv` files, which carry
`floor90_pp` / `floor95_pp` measured **in the same file**. They are excluded from the
numerator and named.

**THE LIMIT, NAMED.** 77 of the 179 prose objects come from `QUEUE.md` — a committed
artifact, but idea text, i.e. a proposal rather than a published result. Dropping it
entirely moves the headline by **0.0002** (82 of 186 = 0.4409 against 116 of 263 = 0.4411)
and moves the conditional not at all (1.0000 either way), so nothing below rests on it.
CSV-only reads 41 of 84 = 0.4881 / conditional 1.0000.

## THE 15 DIAL POINTS (all published)

| claim set | q | n obj | admissible | inadm. | flip HW | share | flip AG | share | LAX | STRICT | transfer says RESOLVED | own says RESOLVED |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CS_CSV | 0.50 | 224 | 84 | 140 | 39 | 0.4643 | 37 | 0.4405 | 34 | 5 | 41 | 12 |
| CS_CSV | 0.68 | 224 | 84 | 140 | 39 | 0.4643 | 39 | 0.4643 | 34 | 5 | 41 | 12 |
| CS_CSV | 0.80 | 224 | 84 | 140 | 39 | 0.4643 | 39 | 0.4643 | 34 | 5 | 41 | 12 |
| CS_CSV | **0.90** | 224 | 84 | 140 | 41 | 0.4881 | 39 | 0.4643 | **41** | **0** | 41 | **0** |
| CS_CSV | 0.95 | 224 | 84 | 140 | 41 | 0.4881 | 45 | 0.5357 | 41 | 0 | 41 | 0 |
| CS_PROSE | 0.50 | 179 | 179 | 0 | 76 | 0.4246 | 79 | 0.4413 | 62 | 14 | 75 | 27 |
| CS_PROSE | 0.68 | 179 | 179 | 0 | 76 | 0.4246 | 78 | 0.4358 | 62 | 14 | 75 | 27 |
| CS_PROSE | 0.80 | 179 | 179 | 0 | 76 | 0.4246 | 76 | 0.4246 | 62 | 14 | 75 | 27 |
| CS_PROSE | **0.90** | 179 | 179 | 0 | 75 | 0.4190 | 76 | 0.4246 | **75** | **0** | 75 | **0** |
| CS_PROSE | 0.95 | 179 | 179 | 0 | 75 | 0.4190 | 89 | 0.4972 | 75 | 0 | 75 | 0 |
| **CS_ALL** | 0.50 | 403 | 263 | 140 | 115 | 0.4373 | 116 | 0.4411 | 96 | 19 | 116 | 39 |
| **CS_ALL** | 0.68 | 403 | 263 | 140 | 115 | 0.4373 | 117 | 0.4449 | 96 | 19 | 116 | 39 |
| **CS_ALL** | 0.80 | 403 | 263 | 140 | 115 | 0.4373 | 115 | 0.4373 | 96 | 19 | 116 | 39 |
| **CS_ALL** | **0.90** | **403** | **263** | **140** | **116** | **0.4411** | **115** | **0.4373** | **116** | **0** | **116** | **0** |
| **CS_ALL** | 0.95 | 403 | 263 | 140 | 116 | 0.4411 | 134 | 0.5095 | 116 | 0 | 116 | 0 |

**Every flip at q >= 0.90 is TRANSFER_LAX and none is TRANSFER_STRICT: the imported floor
never calls something unresolved that the tape can resolve. It only ever certifies what the
tape cannot.**

## D1 — THE CONDITIONAL RATE (POST-HOC AND LABELLED AS SUCH)

The declared statistic is unconditional, so it is diluted by the objects the floor *already*
calls unresolved, where the two rulers cannot disagree in the direction that matters. D1 is
a re-cut of two columns already in `.grid.csv`, not a new measurement and not a third dial:

| q | objects asserting RESOLVED | refused by own ruler | conditional flip | own ruler resolves (of 263) |
|---|---|---|---|---|
| 0.50 | 116 | 96 | 0.8276 | 39 |
| 0.68 | 116 | 96 | 0.8276 | 39 |
| 0.80 | 116 | 96 | 0.8276 | 39 |
| **0.90** | **116** | **116** | **1.0000** | **0** |
| 0.95 | 116 | 116 | 1.0000 | 0 |

**At the confidence the record itself quotes, the own ruler refuses every single margin the
imported floor certifies, and certifies nothing at all.**

## THE 14 CELLS — the margin, both rulers, and the ratio

| panel | ladder | pick vs runner-up | margin | spread | own q.50 | own q.90 | own q.95 | agreement | own/0.0145 |
|---|---|---|---|---|---|---|---|---|---|
| U56 | L_N | 40 vs 12 | 0.0101 | 0.1518 | 0.0976 | 0.2306 | 0.2851 | 0.545 | 15.90x |
| U56 | L_H | 21 vs 63 | 0.0085 | 0.1981 | 0.0764 | 0.1875 | 0.2354 | 0.505 | 12.93x |
| U56 | L_G | 0.75 vs 0.70 | 0.0001 | 0.0014 | 0.0001 | 0.0003 | 0.0004 | 0.711 | **0.0221x** |
| U56 | L_CAD | W vs M | 0.0078 | 0.0363 | 0.0620 | 0.1474 | 0.1753 | 0.528 | 10.17x |
| U56 | L_NH | 12/21 vs 5/63 | 0.0020 | 0.3770 | 0.1333 | 0.3241 | 0.3831 | 0.467 | **22.35x** |
| U56 | L_BOOK | TOP10 vs TOP5 | 0.0242 | 0.1710 | 0.0810 | 0.2028 | 0.2458 | 0.586 | 13.98x |
| U56 | L_MV | 9.99 vs 0.40 | 0.0194 | 0.0911 | 0.0751 | 0.1819 | 0.2145 | 0.567 | 12.55x |
| B136 | L_N | 8 vs 5 | 0.0094 | 0.1870 | 0.0745 | 0.1749 | 0.2113 | 0.495 | 12.06x |
| B136 | L_H | 63 vs 126 | 0.0559 | 0.2877 | 0.0900 | 0.2238 | 0.2670 | 0.662 | 15.43x |
| B136 | L_G | 0.75 vs 0.70 | 0.0003 | 0.0034 | 0.0001 | 0.0003 | 0.0004 | **0.953** | **0.0232x** |
| B136 | L_CAD | W vs D | 0.0205 | 0.0936 | 0.0735 | 0.1831 | 0.2161 | 0.581 | 12.63x |
| B136 | L_NH | 5/63 vs 8/63 | 0.1238 | 0.5010 | 0.0531 | 0.1412 | 0.1655 | **0.931** | 9.74x |
| B136 | L_BOOK | TOP5 vs TOP10 | 0.0001 | 0.2520 | 0.0853 | 0.2052 | 0.2559 | 0.530 | 14.15x |
| B136 | L_MV | 0.40 vs 0.60 | 0.0405 | 0.1173 | 0.0488 | 0.1282 | 0.1543 | 0.715 | 8.84x |

Non-GROSS ratio runs **8.84x to 22.35x, median 12.78x** — 1100's committed 12.9x reproduces.
**Median agreement 0.574**: the typical published pick's sign survives a coin flip's worth of
redraws. **Only 2 of 14 cells reach q=0.90 agreement**, both of them cells whose *margins* the
imported floor calls unresolved or barely resolved.

## HYPOTHESES — 3 of 5, and the two failures are both informative

- **(a) H_WRONG_RULER REFUTED as declared.** 116 of 263 = 0.4411 at CS_ALL / q=0.90 /
  HALFWIDTH, below the majority bar I fixed in advance. Reported as a failure, not re-cut.
  The bar was unreachable on this corpus by construction — see D1.
- **(b) H_DIRECTION SUPPORTED at 116 to 0.** Every flip at the headline runs one way.
- **(c) H_GROSS_FLIPS_BACK REFUTED on the headline reading, SUPPORTED on the reading beside
  it, and that split is the finding.** On HALFWIDTH both GROSS cells read UNRESOLVED under
  both rulers — U56's margin 0.0001 against a half-width of 0.0003, B136's 0.0003 against
  0.0003. On AGREEMENT, B136's GROSS margin is resolved at **0.953** while the imported floor
  calls it unresolved: 1100's 0.022x direction is real, but it appears **only in the
  agreement reading**, so the "other way" transfer that 1100 published rests on which of two
  own-ruler readings one takes. Neither reading was selected on; both are published at all 15
  points.
- **(d) H_Q_STABLE SUPPORTED.** Flip share 0.4373 / 0.4373 / 0.4373 / 0.4411 / 0.4411 over
  the five q, **span 0.0038**. The *answer* is not a free parameter even though the *level*
  of the own ruler is.
- **(e) H_UNDECLARED SUPPORTED.** **163 of 263 admissible transfer objects (0.6198) state no
  confidence anywhere beside the floor they apply.** For roughly five of every eight
  committed transfers, a reader cannot even ask the question this run asks.

**THE DECISION RULE, applied as declared -> NOT REFUTED** (it requires (a) AND (b), and (a)
failed). **On the cut that carries the record's actual claims, D1, the answer is
unambiguous.** Both are stated; neither is hidden behind the other.

## THE OWN RULER IS ITSELF A DRAW — reported, not gated

1100 measured these 14 half-widths at seed base 11001100; this run's base is 11361136.
Median |difference| **0.0046**, median ratio **0.9970**, and the RESOLVED/UNRESOLVED verdict
is unchanged on **13 of 14** cells. **The one cell that moves is B136 GROSS** — the cell
1100's "other way" headline rests on, whose margin (0.0003) and half-width (0.0003) are the
same number to four places. So the own ruler's *level* is a draw and its *answer* is not,
except at exactly the place the record has been quoting it hardest.

## UNIT-INADMISSIBLE TRANSFERS — counted apart, never inside a headline

**140 of the 403 harvested objects apply a SHARPE floor to a margin that is not a Sharpe**:
70 in MaxDD units (C_ISDD) and 70 in CAGR units (C_ISCAGR), all carried on `below_m*` columns
of a committed file. 59 of them assert RESOLVED and 57 flip at q=0.90. They are reported here
and excluded from every headline count, because 0.0145 is not a number in those units at all
and calling the comparison "wrong" would flatter it.

## RULE 8 AND BOTH KEEP PATHS — nothing proposed, and the grid is 1100's

Rungs chosen on **2009-2016 alone**, OOS 2017-2026 read once. **42 rule-8 picks: 4b full 10,
4b OOS 10, 4a 0. Whole grid, 146 rungs: 4b full 33, 4b OOS 36, 4a 0.** Benchmarks: U56 SPY
full 15.10% / 0.8829 / −33.72% (halves 0.9588 / 0.8207), OOS 15.21% / 0.8711 / −33.72%; B136
SPY full 15.16% / 0.8861 / −33.72% (halves 0.9596 / 0.8259), OOS 15.33% / 0.8767 / −33.72%;
live RULES v2 U56 8.62% / 1.2007 / −12.05% (OOS 9.45% / 1.2762), B136 7.98% / 1.0993 /
−12.24% (OOS 7.88% / 1.1059). Best pick clearing 4b full AND OOS: U56 L_MV / C_ISCAGR /
max_vol 9.99 — full 16.30% / 1.1627 / −20.16% (halves 1.2718 / 1.0935), OOS 17.79% / 1.1689 /
−20.16%, 2.79x/yr.

**NOTHING PROPOSED, and the reason is structural rather than a judgement call: G10 shows the
book grid here is 1100's committed 146-rung grid to CSV round-trip precision.** This run
re-scores a **ruler**, not a book; no book exists here that 1100 did not already publish and
decline to propose. **4a is empty at every rung**, as it has been since 1096.

## WHAT THE RECORD SHOULD DO WITH IT (proposed, NOT enacted — rule 6)

1100's drafted PROTOCOL 8b already says a pick must quote "the ladder's OWN measured
resolution at the declared confidence — never a floor transferred from another
construction". This run prices that sentence: enacting it **withdraws the RESOLVED
certification from 116 of 116 committed transfers and grants it to none**, so 8b is not a
documentation tidy-up, it is a retraction of every resolution claim the record's pick layer
currently makes. The narrow, cheap half is **H_UNDECLARED**: 0.6198 of transfers state no
confidence, and a confidence is one column.

## SURVIVORSHIP (PROTOCOL rule 9)

U56 and B136 are CURRENT-CONSTITUENT panels, so every LEVEL above is optimistic. A margin,
a bootstrap half-width and a flip count all contrast two rungs over the same inflated tape
and the bias very largely cancels out of them; it does **not** cancel out of the 4b legs,
measured against SPY, a real index, so every 4b pass counted here is an **upper bound**.

## Files

`.margins.csv` (42 cells x 3 choosers, margins, spreads, own half-width at all five q,
agreement), `.objects.csv` (403 harvested transfers), `.scored.csv` (both rulers on every
object at every q), `.grid.csv` (the 15 dial points), `.d1.csv`, `.cells_flip.csv`,
`.redraw.csv`, `.rejects.csv`, `.controls.csv`, `.cells.csv` (all 146 rungs),
`.walkforward.csv` (42 picks), `.gates.csv`, `.hypotheses.csv`, `.console.txt`.
Script `research/backtests/2026-09-16_is-877-s-SEED-FLOOR-the-RIGHT-RULER-for-a-DETERMINISTIC-MARGIN-at-all_cloud.py`.

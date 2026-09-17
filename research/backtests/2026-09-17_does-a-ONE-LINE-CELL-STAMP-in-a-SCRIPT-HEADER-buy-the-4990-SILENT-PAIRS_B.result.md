# QUEUE idea 1167 (lane B, 2026-09-17) — does a ONE-LINE CELL STAMP in a SCRIPT HEADER buy the 4,990 SILENT pairs?

**ANSWERED = NO, AND THE REASON IS WORSE THAN "IT BUYS LITTLE": THE STAMP BUYS FEWER
RE-SCORABLE CLAIMS THAN THE RECORD ALREADY HAS, BECAUSE THE RECORD'S RE-SCORABILITY IS
MANUFACTURED BY DEFAULT FALLBACK.** Of the 4,990 SILENT claim-dimension pairs idea 1149
published, the deepest honest reading of the author's own file converts **975 (0.1954)**; it
declares **572** openly LADDER; and **3,443 (0.6900) have no value in the file at any reading
at all** — for those the axis does not exist in that run and no stamp can write anything but
`NA`. And the re-score goes the *wrong way*: at the head cell (D2_ASSIGN, WIDE) the stamp makes
**440 claims CELL-STATED against 1149's 366** but leaves only **279 RE-SCORABLE against 1149's
committed 291**. Better information about the cell *destroys* re-scorability, because **287 of
1149's 291 (0.9863) reach their cell only by having their unstated dimensions FILLED with the
frozen defaults N=20/H=126/gross=0.75/cadence=W**, and a stamp that states the true value moves
the claim off the 54-book family. **KILL.** A PROTOCOL clause is PROPOSED NOT ENACTED (rule 6);
RULES.md, PROTOCOL.md, engine.py, scan.py, bot.py and baseline.py are untouched, no book is
promoted, no memo is written.

SELECTION: this lane takes the **LAST** open idea; 1167 was last in `## Open` and needs no
EDGAR / Form 4 / 8-K / options / live data. The run carries its own price leg (54 books, 216
book-rung cells, 96 rule-8 picks), so PROTOCOL rule 8 and both KEEP paths are evaluated here.

## THE POPULATION IS A CENSUS, AND IT IS 1149's OWN COMMITTED FILE

All 2,088 rows are read verbatim from `2026-09-17_can-the-RECORD-s-COST-CLAIMS-be-RESOLVED-from-their-SCRIPTS-rather-than-their-PROSE_C.claims.csv`
(59 NARROW / 125 PROX / 2,088 WIDE, 28 CAGR-floor), and its committed `R_PROSE` 82, `R_UNION`
291, `R_LOOSE` 425 are carried along as the things to be reproduced (**G0a, G0b**). Re-harvesting
today's corpus would give a different and larger population and then no number here would be
comparable to the 4,990 the queue asks about.

**Unlike `data/prices.csv`, the SCRIPT corpus did not move.** All **561** scripts 1149 scanned
are on disk **byte-identical** to its scan (**G1**, missing 0, drift 0), so no git recovery is
needed — the script corpus is append-only where the price tape is rewritten nightly (idea 1163).
That is a fact worth recording on its own: a claim about a committed script is reproducible in a
way that a claim about a committed price is not.

## THE TWO DIALS AND NO MORE (PROTOCOL rule 4, and the queue names both)

`STAMP FORM` × `CLAIM SET` {NARROW, PROX, WIDE} = **12 cells, EVERY ONE PUBLISHED** in
`.census.csv`, each with its own 28-claim sub-population. The stamp form is a **reading depth
into the author's own file**, because that is the only thing about a one-line header stamp that
can be measured rather than imagined — nobody can know what a stamp *would* have said, but we
can measure exactly whether the value is **recoverable from the source the author is looking
at**:

| stamp form | extra text region over the previous rung |
|---|---|
| `D0_MODULE` | 1149's reading, **inherited verbatim** — module-level assignments. The NULL. |
| `D1_DEF` | + `def f(..., N=20, ...)` parameter defaults |
| `D2_ASSIGN` | + ANY `NAME = value` anywhere (indented assignments, call-site kwargs) |
| `D3_DOC` | + `NAME=value` / `NAME: value` adjacency in the script's OWN docstring / header block |

Nested by construction, so the ladder is monotone (**G4**, 0 violations) and `D0` reproduces
1149 exactly (**G2** on all 2,805 (script, dim) pairs; **G3** the claim-weighted 4,990 / 1,472;
**G5** `R_STAMP(D0) ≡ R_UNION` on all 2,088 rows). NOT dials, all reported at every value: the
five dimensions; PANEL {U56, B136}; LADDER {N, H, GROSS, CADENCE} at 1082/1086/1094/1097/1110's
rung lists (9+4+10+4 = 27 rungs per panel, **54 books**); the eight 4b legs; the four cost rungs
{0, 10, 25, 50}; the three rule-8 choosers. **The DIMENSION NAME SET is 1149's, inherited
verbatim and deliberately NOT extended** — extending it would confound a DEPTH ladder with an
ALIAS ladder, and `H_NOTAPPLICABLE` is the guard that says whether it is enough.

**ALL SEVEN HYPOTHESES ARE PRE-REGISTERED.** 1149 flagged four of its own as CALIBRATED because
its census had been run in a prototype first; this run's census arm had not been run when the
docstring was written, and `.hypotheses.csv` records each as PRE-REGISTERED. Three of the seven
are REFUTED, including the one this run most expected to confirm.

## (A) WHAT THE STAMP DOES TO THE 4,990 — THE HEADLINE TABLE

CONVERTED = becomes PINNED (the stamp writes a value, the pair is bought). DECLARED-OPEN =
becomes OPEN, so the stamp can only honestly write `LADDER` — honest, and **never re-scorable**.
STILL ABSENT = no value at any reading; the stamp writes `NA`.

| stamp form | CONVERTED | share | DECLARED-OPEN | STILL ABSENT | share |
|---|---|---|---|---|---|
| `D0_MODULE` | 0 | 0.0000 | 0 | 4,990 | 1.0000 |
| `D1_DEF` | 163 | 0.0327 | 30 | 4,797 | 0.9613 |
| **`D2_ASSIGN`** | **909** | **0.1822** | **470** | **3,611** | **0.7236** |
| `D3_DOC` | 975 | 0.1954 | 572 | 3,443 | 0.6900 |

Per dimension at `D3_DOC`: **N** 1,605 → 452 / 337 / 816; **H** 1,989 → 150 / 65 / **1,774**;
**GROSS** 790 → 123 / 78 / 589; **CADENCE** 606 → 250 / 92 / 264. **H is the axis the queue
singled out (1,989 of 2,088 claims silent) and it is the axis the stamp helps least**: 89% of
its silent pairs have no value in the file anywhere. **H_CONVERT is REFUTED** (909 < the
pre-registered 1,000 bar at `D2_ASSIGN`), and **H_ABSENT is CONFIRMED at 0.6900** — the queue's
framing, "a silent constant is one nobody wrote down", is **false for a supermajority of the
4,990**. Most of them are not unwritten constants. They are axes the run does not have.

## (B) THE GUARD ON THIS RUN'S OWN HEADLINE — AND WHY IT ONLY HALF-CLEARS

`H_NOTAPPLICABLE` was pre-registered as the run's own refutation route: if STILL-ABSENT is high
among scripts that **do** run a book, then the binding limit is this run's inherited name set
and not the record, and the headline is void. Measured: STILL-ABSENT at `D3_DOC` is **0.9043 on
CENSUS_ONLY scripts (n = 94 pairs)** against **0.6859 on RUNS_A_BOOK scripts (n = 4,896)**, gap
**+0.2184** — over the pre-registered 0.20 bar, so **CONFIRMED as stated**.

**Stated plainly, because the bar being cleared is not the whole truth:** the CENSUS_ONLY
population is only **94 of 4,990 pairs**, and **0.6859 of the silent pairs on scripts that DO
run a book are still absent at the deepest reading**. So the "the axis does not exist" reading is
*directionally* confirmed and cannot carry the whole 3,443. The residue is split between runs
that name their dials under an alias outside 1149's name set and runs that genuinely construct
no N/H. **This run does not widen the name set to make its own number bigger**, and it does not
claim the 3,443 are all not-applicable. What it does claim, and what its own data support, is
the negative: **no stamp converts them from the source as it stands.**

## (C) THE FINDING THAT MATTERS — RE-SCORABILITY GOES DOWN, AND WHY

| stamp form | set | claims | CELL-STATED | RE-SCORABLE | of which PINNED-REACHED | DEFAULT-REACHED | 28: RESC |
|---|---|---|---|---|---|---|---|
| `D0_MODULE` | WIDE | 2,088 | 366 | **291** | 4 | 287 | 9 |
| `D1_DEF` | WIDE | 2,088 | 380 | 299 | 4 | 295 | 10 |
| **`D2_ASSIGN`** | **WIDE** | **2,088** | **440** | **279** | **1** | **278** | **11** |
| `D3_DOC` | WIDE | 2,088 | 443 | 291 | 1 | 290 | 11 |

(NARROW and PROX are in `.census.csv` and move the same way: PROX 12 → 13 → 15 → 15.)

**`H_RESCORE` is REFUTED**: at the head cell the stamp re-scores **279 against 291**. A deeper,
truer reading of the script makes **more** claims cell-stated (440 vs 366) and **fewer**
re-scorable. That is not a paradox and it is not noise. **`H_DEFAULT` is CONFIRMED at 0.9863:
287 of 1149's committed 291 re-scorable claims reach their cell only because the dimensions
nobody stated were FILLED with the frozen defaults** N=20/H=126/gross=0.75/cadence=W — and those
defaults *are* the incumbent book, so a silent claim lands on the incumbent for free. Give the
stamp a real value for a silent axis and the claim moves off the 54-book one-factor-at-a-time
family and stops resolving.

**So the record's "291 re-scorable" is 98.6% an artefact of default fallback, and the stamp's
real effect is to expose that rather than to extend it.** The one thing the stamp does buy
outright is the queue's headline sub-population: **the 28 CAGR-floor claims go 9 → 11
(`H_28` CONFIRMED)**, and even there **0 of the 11 are PINNED-REACHED** at any stamp form.

## (D) WHAT THE STAMP COSTS A RUN THAT ALREADY HAS THE CONSTANTS

**`H_FREE` is REFUTED at 0.8519.** Of the **486** (script, dim) pairs 1149 classed PINNED at
module level — the runs that by hypothesis already have their constants — the deepest reading
returns the **same single value for 414**, and for the other **72** it returns *more than one*.
For those 72 the module constant is not the only value of that axis in the file, so the author
cannot transcribe: they must **choose**, and that choice is the stamp's real price. All 72 are
published in `.cost.csv`, script and dimension named.

Per script, out of the four construction fields, the stamp is (`VALUE` / `LADDER` / `NA`):
`D0_MODULE` 0.866 / 0.594 / 2.540 → `D3_DOC` 1.257 / 0.988 / 1.756. **Even at the most generous
reading the median script can fill fewer than half its stamp with a value**, and 1.76 of 4 fields
come back `NA`.

## (E) PROTOCOL RULE 8 AND BOTH KEEP PATHS — THE STAMP MOVES NO BOOK

96 rule-8 picks are published (2 panels × 4 ladders × 4 cost rungs × 3 IS-only choosers); every
chooser reads **2009–2016 only** and is evaluated on 2017–2026 untouched. At PROTOCOL's 10 bps:
**4b full+OOS 4 of 24, 4a 0 of 24.** All four 4b passers are `C_ISSHARPE`/`C_ISCAGR` landing on
**GROSS=0.75 and CADENCE=W — the frozen default rung on both ladders**, i.e. pure default
fallback, not a chosen book; flagged, not counted as four independent finds. On the fresh grid
at 10 bps, 15 of 216 book-rung cells clear 4b full+OOS and **0 of 216 clear 4a**.

Benchmarks (10 bps, next-day execution, PROTOCOL rule 2): SPY U56 full **15.06% / 0.8814 /
−33.72%**, halves 0.9598 / 0.8170, OOS 15.15% / 0.8684 / −33.72%; B136 15.16% / 0.8861, OOS
0.8767. Live RULES v2 U56 **8.60% / 1.1980 / −12.05%**, halves 1.2329 / 1.1702, OOS 9.42% /
1.2714.

**The NOMINATED BOOK — the cell most cited by the claims each reading makes re-scorable, the
only channel by which a stamp can move a book — is `U56/N=20` at ALL 12 CELLS.** It is unmoved
at 3 of 3 claim sets and at every stamp form: full **15.55% / 1.1381 / −19.13%**, halves 1.2049 /
1.0932, OOS **16.92% / 1.1615 / −19.13%**; **4b PASS full and OOS, 4a FAIL**. That book is the
standing 2026-09-04 / 2026-09-16 incumbent (and `U56/N=20 ≡ U56/H=126 ≡ U56/GROSS=0.75 ≡
U56/CADENCE=W` — one book reached by four ladders' default rung). **The stamp is CONFIRMATORY,
not generative, so NO MEMO IS WRITTEN** and nothing is proposed for the Sunday review.

## GATES — 15 of 15 PASS

G0a population 2,088 / 125 / 59 pinned. G0b 1149's committed 82 / 291 / 425 / 28 carried.
**G1 all 561 scripts byte-identical to 1149's scan** (0 missing, 0 drift). **G2 `D0_MODULE`
reproduces 1149's committed per-script states on all 2,805 (script, dim) pairs** — the
classifier is reproduced, not re-implemented from memory. **G3 the claim-weighted SILENT/OPEN
4,990 / 1,472 reproduced** from 1149's own claims file. G4 the depth ladder is monotone
(0 violations). **G5 `R_STAMP(D0_MODULE)` reproduces `R_UNION` on all 2,088 rows** (0 rows
differ) — the null rung IS the parent. G6 the `H_FREE` basis is non-empty (486 pairs).
G7 / G8 / G11 determinism (resolver, depth scanner, and the incumbent book rebuilt end-to-end:
0.0 / 0.0 / 0.00e+00). G10a/G10b `r(c) = g − tn·c/1e4 ≡ engine.backtest` at 0 and 10 bps
(1.39e-17). **G9 CROSS-RUN: this run's independent rebuild of 1149's 54 books at 10 bps agrees to
2.22e-16** over CAGR/Sharpe/MaxDD with **G9b 0 verdict flips** — the price leg is a bit-for-bit
replay, and unlike 1149's G3/G5 nothing had to be carried, because the cells this run reads did
not move on the nightly tape.

## HYPOTHESES

| hypothesis | kind | verdict | statistic |
|---|---|---|---|
| `H_ABSENT` | PRE-REGISTERED | **CONFIRMED** | STILL-ABSENT share of the 4,990 at `D3_DOC` = 0.6900 (bar > 0.50) |
| `H_CONVERT` | PRE-REGISTERED | **REFUTED** | CONVERTED at `D2_ASSIGN` = 909 of 4,990 (bar ≥ 1,000) |
| `H_RESCORE` | PRE-REGISTERED | **REFUTED** | `R_STAMP(D2_ASSIGN, WIDE)` re-scores 279 vs `R_UNION`'s 291 (bar: strictly more) |
| `H_28` | PRE-REGISTERED | **CONFIRMED** | the 28 CAGR-floor claims: 11 re-scorable vs `R_UNION`'s 9 |
| `H_DEFAULT` | PRE-REGISTERED | **CONFIRMED** | DEFAULT-REACHED share of the committed 291 = 0.9863 (287 of 291) |
| `H_NOTAPPLICABLE` | PRE-REGISTERED | **CONFIRMED** | CENSUS_ONLY 0.9043 (n=94) vs RUNS_A_BOOK 0.6859 (n=4,896), gap +0.2184 (bar > 0.20) — see (B) |
| `H_FREE` | PRE-REGISTERED | **REFUTED** | module-PINNED pairs whose deepest reading is the same value = 0.8519 (414 of 486) (bar ≥ 0.95) |

## THE PROTOCOL CLAUSE — PROPOSED, NOT ENACTED (rule 6)

Proposed for a future Sunday review, on this run's evidence and not adopted here:

> Every backtest script SHALL carry, as the first line after its docstring, a stamp
> `# CELL: panel=<v> N=<v> H=<v> gross=<v> cadence=<v>`, where each field is a literal value,
> `LADDER` if the run walks that axis, or `NA` if the run has no such axis. **A claim may be
> re-derived onto a cell ONLY from fields the stamp gives as literal values; a dimension the
> stamp marks `LADDER` or `NA`, or omits, is NEVER filled with a default.**

**The second sentence is the whole clause.** The first sentence alone buys 975 of 4,990 pairs and
would *reduce* the record's re-scorable count from 291 to 279. The second sentence is what
retires the 287-of-291 default fallback that is currently doing the work — and it retires it in
the direction of fewer claims honestly scored, not more. On this run's evidence the record's
re-scorability problem is not that authors forgot to write their constants down. **It is that the
resolver supplies constants the authors never had.**

## CAVEATS CARRIED

SURVIVORSHIP: `universe.json` / `universe_broad.json` are current constituents (PROTOCOL rule 9);
inherited from the parent chain, not repaired here. The DIMENSION NAME SET is 1149's and is a
stated limit, quantified in (B), not widened. The 4,990 is a **claim-weighted** population, so a
heavily cited script contributes many pairs; the per-script view is in `.fields.csv` and the
per-pair view in `.pairs.csv`, both published. `R_STAMP` measures what is RECOVERABLE from the
committed source, which is a lower bound on what a live author could have written and an upper
bound on what a reader can verify today — the second is the one PROTOCOL needs.

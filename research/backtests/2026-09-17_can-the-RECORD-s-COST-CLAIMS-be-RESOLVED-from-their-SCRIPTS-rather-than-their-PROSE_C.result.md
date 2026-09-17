# QUEUE idea 1149 (lane C, 2026-09-17) — can the RECORD's COST CLAIMS be RESOLVED from their SCRIPTS rather than their PROSE?

**ANSWERED = NOT FROM THE SCRIPT, BUT YES FROM THE SCRIPT AS A FALLBACK, AND THE QUEUE'S OWN
PREMISE IS THE THING THAT DIES.** The queue asserts that "every claim cites a committed script
whose constants pin panel, N, H, gross and cadence exactly". The first half is true at **0.9933**
(2,074 of 2,088 claims resolve to a committed script that exists on disk). The second half is
**FALSE, and decisively**: the cited script pins the PANEL for only **190 of 2,088** claims, N for
**146**, H for **5**. Read on its own, `R_SCRIPT` re-scores **38 of 2,088 — LESS THAN HALF the 82
the PROSE already reached**. But used as a FALLBACK behind the prose, `R_UNION` re-scores **291 of
2,088 (0.1394) against R_PROSE's 82 (0.0393), a 3.55x gain**, and takes the 28 CAGR-floor claims
from **0 to 9 re-scorable** — the re-score 1098 had to report with a population of ZERO now has a
population, and **5 of the 9 are REFUTED by their own cell's measured killer leg**. No RULES
change, no book promoted, no PROTOCOL edit (rule 6); RULES.md, PROTOCOL.md, engine.py, scan.py,
bot.py and baseline.py untouched. SELECTION: this lane takes the SECOND open idea; 1149 was second
in '## Open' and is not EDGAR / Form 4 / 8-K / options / live-data. Pure price leg of 54 books,
216 book-rung cells and 24 rule-8 picks, so it carries this run's mandatory rule-8 walk-forward
and both KEEP paths.

**THE POPULATION IS A CENSUS AND IT IS 1098's OWN COMMITTED FILE.** All 2,088 rows are read
verbatim out of `2026-09-16_...-or-only-the-CAGR-FLOOR_C.claims.csv` (59 NARROW / 125 PROX / 2,088
WIDE, 28 CAGR-floor), and 1098's own `resolved` (82) and `resolved_loose` (425) columns are
carried along as the thing to be reproduced. **Re-harvesting today's corpus would give a different
and larger population** — `LEADERBOARD.md` has grown 66 lines and `CHANGELOG.md` 249 since, and
there are now 899 `result.md` on disk — **and then no number here would be comparable to the 82
and the 28 the queue asks about.** Idea 1163's vintage finding applied to text instead of prices.
Line numbers index the corpus AS IT WAS, so `LEADERBOARD.md` and `CHANGELOG.md` are recovered from
git at 1098's own commit `3c1e2af6`; G6 fails the run if the on-disk HEAD copies are used instead.

**THE TWO DIALS AND NO MORE (PROTOCOL rule 4, and the queue names both):** `RESOLUTION SOURCE`
{R_PROSE, R_SCRIPT, R_UNION, R_LOOSE} x `CLAIM SET` {NARROW, PROX, WIDE} = **12 cells, EVERY ONE
PUBLISHED** in `.census.csv`, each with its own 28-claim sub-population. The fifth source
`R_UNION_G` is a REPAIR of an inherited guard found by this run (below), reported beside the
headline at all three claim sets and never selected on. NOT dials, all reported at every value:
PANEL {U56, B136}; LADDER {N, H, GROSS, CADENCE} at 1082/1086/1094/1097/1110's rung lists (9 + 4 +
10 + 4 = 27 rungs per panel, **54 books**); the eight 4b legs; the four cost rungs {0, 10, 25, 50};
the three rule-8 choosers. The 1-bp ladder 0..200 is a MEASUREMENT AXIS, not a dial. Frozen at
936/1064/1071/1082/1086/1094/1097/1098's construction.

**CALIBRATED, NOT PREDICTED — SAID UP FRONT.** The census arm was built and run in a wiring
prototype before the script was written, so `H_CITE`, `H_SCRIPTWINS`, `H_GAIN` and `H_28` are
MEASUREMENTS against a stated bar, not forecasts, and they are labelled CALIBRATED in
`.hypotheses.csv` and everywhere they are quoted. `H_LADDERCAUSE`, `H_REFUTE` and `H_DDKILL` were
unmeasured when the file was written. Saying so is cheaper than pretending.

**GATES 19 of 21 PASS, and the two that fail are DECLARED CARRIED, not absorbed.**
G1 **`R_PROSE` reproduces 1098's committed `R_STRICT` on all 2,088 rows at 0.00e+00** — the
resolution rule is reproduced, not re-implemented from memory — and G1b reproduces its
`resolved_loose` at **425 exactly**; G0 pins the population (2088/125/59, 82, 425); G8 recovers the
28 as 1098 defined them; G10 the resolver is reproducible; G9 determinism 0.00e+00; G1a/G1b
`r(c) = g − tn·c/1e4 == engine.backtest` 1.39e-17; G5b 1094's c\* full/OOS **63/64 with killer
`L_H1`** exactly; G7 1097's committed c\*\_full on all 18 shared cells 0.00e+00; **G13 reproduces
1098's committed killer-kind table BIT FOR BIT — 17 books, SHARPE 10 / CAGR 4 / DD 3**; G12 the
guard repair is a strict subset. **G3 (SPY OOS triple, 2.89e-03) and G5 (1094's ladder, 2.22e-03)
FAIL ON THE HEAD TAPE AND ARE PUBLISHED FAILING**, because `data/prices.csv` is rewritten nightly:
**G11 MEASURES the cause rather than asserting it — 31,505 of 258,733 shared cells restated
(0.1218) between 1098's commit and HEAD, reaching back to 2008-01-02, max relative move 8.384e-03,
plus one extra bar** — which replays idea 1163's own census exactly from the other side. Every one
of the three anchors PASSES once re-read on the tape recovered at 1098's commit: **G3b 1.70e-04,
G2b 3.18e-07 (the very value 1098 itself published), G5d 4.96e-05.** Nothing was widened.

## (A) THE QUEUE'S PREMISE, MEASURED AND REFUTED

| | scripts (of 561) PINNED / OPEN / SILENT | claims (of 2,088) PINNED / OPEN / SILENT |
|---|---|---|
| PANEL | 71 / 458 / 32 | **190** / 1,773 / 125 |
| N | 26 / 76 / 459 | **146** / 337 / 1,605 |
| H | 1 / 8 / 552 | **5** / 94 / 1,989 |
| GROSS | 216 / 129 / 216 | 790 / 508 / 790 |
| CADENCE | 243 / 120 / 198 | 949 / 533 / 606 |

PINNED = exactly one literal value at module level; OPEN = two or more, i.e. **the script WALKS A
LADDER over that axis and by construction cannot pin it**; SILENT = no module-level constant of
that name at all. **The record's scripts pin the EXPOSURE dials (gross 790, cadence 949) and not
the SELECTION ones (N 146, H 5).** A cost claim is almost always about a selection cell, so the
script is silent about exactly the axis the claim is about.

**H_LADDERCAUSE was PRE-REGISTERED and is REFUTED: OPEN 1,472 against SILENT 4,990**, claim-weighted
over the four construction dimensions. The failure to pin is **SILENCE, not laddering** — and that
matters, because the two have different repairs. A ladder run can never be pinned from its own
source and no stamp helps; a SILENT dimension is a constant the run simply never named, and a
one-line header stamp would fix 4,990 of the 6,462 unpinned pairs. **H = 1,989 SILENT of 2,088 is
the extreme case: the record's minimum-hold constant is essentially never written down as a
module-level name.**

## (B) THE 12 CELLS — TWO COUNTS THAT NEVER MERGE

`CELL-STATED` = the source pins panel and at least one construction dimension; `RE-SCORABLE` = that
cell is also one of the 54 measured books. A stated cell outside the family is a **PROVENANCE
gain, not a re-derivation**, and the two are printed side by side at every cell.

| source | WIDE cell-stated | WIDE **RE-SCORABLE** | share | of the 28: stated / **re-scorable** |
|---|---|---|---|---|
| R_PROSE (1098's headline) | 124 | **82** | 0.0393 | 0 / **0** |
| R_SCRIPT (the queue, literally) | 59 | **38** | 0.0182 | 4 / **3** |
| **R_UNION (headline)** | 366 | **291** | **0.1394** | 10 / **9** |
| R_LOOSE (1098's rejected first cut) | 473 | **425** | 0.2035 | 11 / **11** |
| R_UNION_G (this run's repair) | 305 | **238** | 0.1140 | 5 / **5** |

**H_SCRIPTWINS REFUTED, 38 against 82.** The script read ALONE is worse than the prose, because a
ladder run states no panel and no N. **H_GAIN SUPPORTED, 291 against 82.** The script is worth a
great deal as a FALLBACK and nothing as a replacement: **209 of the 291 are claims the prose alone
could not reach, and R_UNION loses NONE of R_PROSE's 82** — the union is a strict superset by
construction, which is why it is the honest headline. **75 of the 366 R_UNION cell-stated claims
land OUTSIDE the 54-book family**; they gain provenance and are not re-scored here.

**H_28 is REFUTED against its own bar** — 9 of 28 is not a majority — **but 9 against 1098's 0 is
the substantive answer to the queue's ask**, and it is the difference between a re-score with a
population and one without.

## (C) THE RE-SCORE, POSSIBLE FOR THE FIRST TIME

| source | measured | CONFIRMED | REFUTED | UNDECIDED | TRANSFERRED |
|---|---|---|---|---|---|
| R_PROSE | 0 | 0 | 0 | 0 | 28 |
| R_SCRIPT | 3 | 0 | 0 | 3 | 25 |
| **R_UNION** | **9** | **0** | **5** | **4** | 19 |
| R_LOOSE | 11 | 0 | 9 | 2 | 17 |
| R_UNION_G (repair) | 5 | 0 | 3 | 2 | 23 |

**H_REFUTE SUPPORTED, 5 of 9, and ZERO CONFIRMED at every source.** Every one of the five refuted
claims resolves to `U56/N=20` and is killed on `L_H1` — a SHARPE leg, never the CAGR floor it
assumed. The four UNDECIDED all resolve to `B136/N=20`, which is `DEAD0` (it fails a 4b leg
already at 0 bps, so a rising rung has nothing left to kill). **1094's single-cell correction
therefore survives contact with the record's own claims: of the CAGR-floor claims that can be
re-derived at all, not one is right.** The TRANSFERRED column is never merged into the verdicts:
a transferred rate is an extrapolation, not a re-derivation (1048/1098/1102/1110's convention).

## (D) A DEFECT IN AN INHERITED GUARD, FOUND BY THIS RUN AND PRICED

1098's `OUT_OF_FAMILY` guard reads the CLAIM'S PROSE. That was right when the cell also came from
the prose. **Once the cell comes from the CITED SCRIPT, the guard and the resolution read
different objects** — and two of the nine newly re-scorable CAGR-floor claims turn out to cite
`2026-09-04_ensemble-plus-momentum_C.py` and `2026-09-05_sleeve-with-a-real-diversifier_B.py`,
exactly the families the guard exists to exclude, while their own prose says nothing suspicious.
**`R_UNION_G` applies the same guard to the SCRIPT NAME as well and is published at every cell:
291 -> 238 re-scorable (still 2.90x R_PROSE's 82) and 9 -> 5 of the 28 (still REFUTED 3, CONFIRMED
0).** G12 proves the repair only ever removes rows. **The gain survives its own correction**, and
the corrected numbers are the ones a later run should cite.

## (E) RULE 8 AND BOTH KEEP PATHS — 54 BOOKS, ALL PUBLISHED, AND NOTHING NEW REACHED

Benchmarks: **U56 SPY full 15.06% / 0.8814 / −33.72% (halves 0.9598/0.8170), OOS 15.15% / 0.8684 /
−33.72%; U56 RULES v2 (live) @10 bps 8.60% / 1.1980 / −12.05%, OOS 9.42% / 1.2714; B136 SPY 15.16%
/ 0.8861 / −33.72% (halves 0.9596/0.8259), OOS 15.33% / 0.8767; B136 RULES v2 7.98% / 1.0993 /
−12.24%, OOS 7.88% / 1.1059.** Base rates over the 54 books: **4b full 17 / 16 / 15 / 10 and 4b OOS
19 / 17 / 16 / 14 at 0 / 10 / 25 / 50 bps; 4a 0 of 54 AT EVERY RUNG.**

**Rule 8: 24 IS-only picks on 2009–2016 alone, 4 clear 4b full AND OOS at 10 bps, 0 clear 4a — and
all four picks are the SAME BOOK.** U56 / GROSS / C_ISSHARPE and C_ISCAGR both pick gross 0.750, and
U56 / CADENCE / C_ISSHARPE and C_ISCAGR both pick W: that is **N=20, H=126, gross 0.75, weekly —
the INCUMBENT DEFAULT**, full 15.55% / 1.1381 / −19.13% (halves 1.2049/1.0932), OOS 16.92% / 1.1615
/ −19.13%. It is not a discovery; 1082/1098/1162 committed the same cell at the same numbers.

**NOTHING NEW IS PROPOSED AND NO MEMO IS WRITTEN.** The best non-incumbent book clearing 4b full
and OOS is U56 N=12 (17.65% / 1.1658 / −20.17%, OOS 18.78% / 1.1701) and it is **already committed
by 1098/1102** — 1163 said the same thing four days of research ago — and no chooser here reaches
it (C_ISSHARPE and C_ISDD take N=40, C_ISCAGR takes N=5). **4a is 0 of 54 at every rung and 0 of
24 picks.** A census run is the wrong place to promote a book, and there is no book here to
promote.

**H_DDKILL is REFUTED AND THE BAR WAS THIS RUN'S OWN FAULT, RECORDED AS DECLARED AND NOT RE-CUT.**
It was pre-registered as "the modal killer is the DD cap (1098's answer)", but 1098's "DD cap most
often" is its CLAIM-side census (0.4880 of the 125 claims that name a leg) and its TAPE-side answer
was already SHARPE. The measurement reproduces 1098's table **exactly** (G13): of the 17 books a
rising rung can kill, **SHARPE 10 (0.5882) / CAGR 4 (0.2353) / DD 3 (0.1765)**. So the verdict is a
defect in this run's bar and an independent replication of 1098's finding at the same time.

## SURVIVORSHIP (PROTOCOL rule 9)

U56 and B136 are CURRENT-CONSTITUENT panels, so every CAGR and drawdown LEVEL is optimistic, every
c\* printed here is an UPPER BOUND on the true one, and the bias does NOT cancel out of the 4b
legs, which contrast a book against a real index. **It does not touch this run's headline at all:**
the citation rate, the pin/open/silent tables, the 12 resolution cells and the guard repair are
scans of committed text and committed source code and carry no market bias whatever. The RE-SCORE
arm in (C) inherits the price bias, because it reads a measured killer leg off the tape.

## OUTPUTS

Script `research/backtests/2026-09-17_can-the-RECORD-s-COST-CLAIMS-be-RESOLVED-from-their-SCRIPTS-rather-than-their-PROSE_C.py`,
11 CSVs (`.claims` 2,088 rows, `.census` 15, `.scripts` 561, `.rescore` 140, `.books` 54, `.grid`
216, `.ladder` 54, `.walkforward` 96, `.benchmarks`, `.gates` 21, `.hypotheses` 8), console log,
this note, 5 LEADERBOARD rows. Follow-ups filed 1167 (does a one-line CELL STAMP in a script
header buy the 4,990 SILENT pairs, and what does it cost a run) and 1168 (how many of the record's
OTHER committed censuses inherit a guard that reads a different object than their resolution).

# Idea 1249 (lane C, 2026-09-18) — how many of the 1,074 UNRECOVERABLE RESAMPLE VERDICTS can be RE-DERIVED FROM THEIR SCRIPT?

**VERDICT: KILL (capital), NO NEW BOOK. ANSWERED = 217 of 1,074 (0.2020) — THE SCRIPT LOST IT TOO.
BYCATCH, AND IT IS THE LARGER FINDING: 650 OF THE 728 SILENT UNITS RESOLVE TO A SCRIPT THAT NEVER
DRAWS A BLOCK AT ALL, SO 1243's POPULATION IS 0.61 OUT OF THE CLAUSE'S OWN SCOPE AND 1247's
COMMITTED BILL OF 1,099 RE-RUNS OVERSTATES THE REAL ONE BY 5.3x.** Gates 13 of 13.

Script: `research/backtests/2026-09-18_how-many-of-the-1-074-UNRECOVERABLE-RESAMPLE-VERDICTS-can-be-RE-DERIVED-FROM-THEIR-SCRIPT_C.py`

## The population is 1243's, pinned, and it reproduces EXACTLY

1230 proved the record's censuses have no fixed point, so the corpus is recovered from git at
`e890434^` — the parent of 1243's commit, i.e. the tree 1243's census actually read. On that tree
this run's census reproduces 1243's committed `.scope.csv` **bit for bit: max deviation 0 across
all 3 scopes x 7 columns** (G1), including the 1,074 the queue asks about.

| scope | bound | states_L | ladder | verdict | floor | non_conf | UNRECOVERABLE | 1243's |
|---|---|---|---|---|---|---|---|---|
| SC_BLOCK | 489 | 331 | 39 | 272 | 166 | 450 | **154** | 154 |
| SC_RESAMPLE | 1413 | 332 | 42 | 1196 | 575 | 1371 | **1074** | 1074 |
| SC_ALL | 7989 | 335 | 58 | 4260 | 6353 | 7931 | **7631** | 7631 |

CONTROL, published beside it: today's HEAD corpus has 34,405 units over 1,180 .md files (+310,
+14 since 1243 ran) and its SC_RESAMPLE unrecoverable count is **1,094, not 1,074**. Every number
below is about the pinned tree and says so.

Composition of the 1,074: LEADERBOARD 435, CHANGELOG 97, md paragraphs 542 over 320 files.

## ARM B — attribution reaches 0.8799, and the 0.90 bar is REPORTED FAILED, not moved

| claim set | units | A_STEM | A_COL | A_NAME | A_IDEA | NONE | reach |
|---|---|---|---|---|---|---|---|
| CS_BLOCK | 154 | 69 | 45 | 7 | 0 | 33 | 0.7857 |
| **CS_RESAMPLE** | **1074** | **491** | **428** | **26** | **0** | **129** | **0.8799** |
| CS_ALL | 7631 | 4846 | 2307 | 74 | 0 | 404 | 0.9471 |

`H_REACH` (>= 0.90 resolves to a committed script) **FAILS at 0.8799** on the headline claim set.
Standalone reach, since the paths overlap: A_STEM 491, A_COL 428, A_NAME 473, A_IDEA 36. `H_STEM`
**HELD** — the artefact-stem identity (`X.result.md -> X.py`) reaches more units than PROTOCOL rule
5's own script column, because the column only exists on LEADERBOARD rows. **PUBLISHED, NOT USED:
42 unattributed units carry an `idea NNNN` mention in the body; that names the PARENT idea, not
the emitter, so attributing on it would mis-credit.** A lane wanting the looser rule has the count.

## ARM C — THE ANSWER: 217 of 1,074, and it is monotone DOWN in how wide the clause reaches

All 12 (claim set x resolution rule) cells, every one published:

| claim set | rule | units | NO_SCRIPT | SILENT | PINNED | LADDER | RECOVERABLE | share | modal L | share@63 |
|---|---|---|---|---|---|---|---|---|---|---|
| CS_BLOCK | R_CONST | 154 | 33 | 59 | 62 | 0 | 62 | 0.4026 | 63 | 0.6613 |
| CS_BLOCK | R_LADDER | 154 | 33 | 50 | 34 | 37 | 71 | 0.4610 | 21 | 0.1429 |
| CS_BLOCK | R_ANY | 154 | 33 | 50 | 31 | 40 | 71 | 0.4610 | 21 | 0.1360 |
| CS_BLOCK | R_UNION | 154 | 33 | 47 | 34 | 40 | 74 | 0.4805 | 21 | 0.1311 |
| CS_RESAMPLE | R_CONST | 1074 | 129 | 752 | 193 | 0 | 193 | 0.1797 | 63 | 0.7513 |
| **CS_RESAMPLE** | **R_LADDER** | **1074** | **129** | **728** | **117** | **100** | **217** | **0.2020** | **63** | 0.2171 |
| CS_RESAMPLE | R_ANY | 1074 | 129 | 723 | 110 | 112 | 222 | 0.2067 | 63 | 0.2038 |
| CS_RESAMPLE | R_UNION | 1074 | 129 | 698 | 126 | 121 | 247 | 0.2300 | 63 | 0.1942 |
| CS_ALL | R_CONST | 7631 | 404 | 6559 | 668 | 0 | 668 | 0.0875 | 63 | 0.7615 |
| CS_ALL | R_LADDER | 7631 | 404 | 6460 | 466 | 301 | 767 | 0.1005 | 63 | 0.2910 |
| CS_ALL | R_ANY | 7631 | 404 | 6441 | 442 | 344 | 786 | 0.1030 | 63 | 0.2730 |
| CS_ALL | R_UNION | 7631 | 404 | 6265 | 564 | 398 | 962 | 0.1261 | 63 | 0.2493 |

- **PRE-DECLARED OUTCOME (B) FIRES: THE SCRIPT LOST IT TOO.** 0.2020 < the 0.25 bar for (B) and
  far below (A)'s 0.50. `H_EDIT` **FAILS 217 vs 857**. 1243's "editing cannot bring them into
  conformance" survives for four units in five.
- **OUTCOME (C) DOES NOT FIRE.** Attribution is NOT the binding constraint: 728 SILENT against 129
  NO_SCRIPT. The emitting script is usually found and simply has no L in it.
- **`H_LADDER` FAILS, 100 LADDER vs 117 PINNED.** The record's stated habit is to walk L; among
  the scripts behind these units, more pin one value than walk a set.
- **`H_HEAD63` HELD, and it is the sharpest thing in the table: among scripts that pin a SINGLE L,
  0.7513 of the pinned values are the record's frozen 63.** The dial 1208 called the largest
  unstated one in the record is, where the code states it at all, three-quarters one number.
- The recoverable share falls MONOTONICALLY as the clause reaches wider — 0.46 / 0.20 / 0.10 at
  CS_BLOCK / CS_RESAMPLE / CS_ALL under the headline rule. **A clause is recoverable in proportion
  to how narrowly it is scoped**, which is the next section's point measured a second way.

## ARM C2 — THE BYCATCH, AND IT IS BIGGER THAN THE ANSWER: 0.8929 OF THE SILENT UNITS NEVER DREW A BLOCK

1243's `RESAMPTOK` binds any unit containing "percentile", "draws", "bootstrap" or "its own null".
A unit can therefore be counted non-conforming although the CODE that produced it never ran a block
resample in its life — and then there is no L it lost, and nothing to re-run.

| claim set | SILENT | script DOES draw blocks | script NEVER draws a block | share |
|---|---|---|---|---|
| CS_BLOCK | 50 | 33 | 17 | 0.3400 |
| **CS_RESAMPLE** | **728** | **78** | **650** | **0.8929** |
| CS_ALL | 6460 | 237 | 6223 | 0.9633 |

`H_SCOPE` **HELD at 0.8929.** So the 1,074 decomposes as: **217 repairable by EDIT at zero draws,
650 never in the clause's business at all, 78 genuinely lost an L their own code ran, 129
unattributed.** On CS_BLOCK — the units that actually name a block construction — the same test
reads 0.34, i.e. the over-binding is a property of the WIDE scope, not of the record's prose.

## ARM D — THE BILL, AND 1247's IS 5.3x TOO BIG

Measured on this machine, this tape: **0.2968 ms per draw** at T = 2007 over 9 rungs (400 draws
timed). Each re-run is billed at the emitting script's OWN B where the code names one (mean 1270.8
on the headline cell), else the record's frozen 1000. L = T is free (one legal block start; G7).

| cell | re-runs | edits | form | DRAWS | hours | IN-SCOPE re-runs | IN-SCOPE draws |
|---|---|---|---|---|---|---|---|
| CS_RESAMPLE x R_LADDER | 857 | 217 | CF_POINT | 1,089,078 | 0.09 | **207** | **200,260** |
| CS_RESAMPLE x R_LADDER | 857 | 217 | CF_IDENTITY | 1,089,078 | 0.09 | 207 | 200,260 |
| CS_RESAMPLE x R_LADDER | 857 | 217 | CF_LADDER4 | 4,356,312 | 0.36 | 207 | 801,040 |
| CS_RESAMPLE x R_LADDER | 857 | 217 | CF_LADDER11 | 11,979,858 | 0.99 | 207 | 2,202,860 |

**1247 committed a bill of 1,099 re-runs against this exact population. This run bills 857 — and
of those, only 207 resolve to a script that draws a block at all.** The real cost of bringing
1243's unrecoverable set into conformance is **207 re-runs and 200,260 draws at the point form —
about one minute of compute on this machine** — plus 217 edits at zero draws. The remaining 650
need a SCOPE fix, not a re-run. G7 and G10 both pass (the identity rung is free; the bill is
monotone in rungs).

## ARM E — RULE 8 AND BOTH KEEP PATHS: A RECOVERABILITY RULE IS A DISCLOSURE, NOT A FILTER

(E1) 162 rung books, full sample and 2017-2026. **4a 0 of 162** (the DD leg against live RULES v2,
as at every run since 1096). 4b full 26, 4b OOS 30, BOTH 25 — by panel U56 20/23, B136 6/7, SMALL
0/0. Benchmarks: SPY U56 full 15.13% / 0.8848 / -33.72%, OOS 15.28% / 0.8745 / -33.72%; live RULES
v2 U56 full 8.62% / 1.2017 / -12.05%, OOS 9.47% / **1.2778** / -12.05%, which beats every one of
the 162 books on OOS Sharpe. Best full-Sharpe book U56/A/N=12: 17.69% / 1.1686 / -20.17%, halves
1.2741 / 1.0884, OOS 1.1748 — 4b PASS on the drawdown cap by 0.0006.

(E2/E4) A decision is R-ADMITTED when at least one committed unit citing its panel and its ladder
has a recoverable L; admitted -> act on the IS argmax, otherwise hold the anchor (rule 8, picks on
the IS window only, 2017-2026 read once).

| cell | admitted | mean OOS Sharpe | mean OOS CAGR | mean OOS MaxDD | 4a / 4b / 4b_OOS |
|---|---|---|---|---|---|
| REF_ACT_ON_ALL | 72 | 0.8016 | 0.1102 | -0.2453 | 0 / 6 / 7 |
| REF_DO_NOTHING | 0 | 0.7922 | 0.1099 | -0.2363 | 0 / **24** / 24 |
| REF_POINT_L63 | 18 | 0.8420 | 0.1027 | -0.2051 | 0 / 1 / 1 |
| **all 12 (claim set x rule) cells** | **72** | **0.8016** | **0.1102** | **-0.2453** | **0 / 6 / 7** |
| CONTROL Q_MAJORITY | 0 | 0.7922 | 0.1099 | -0.2363 | 0 / 24 / 24 |
| CONTROL Q_ALL | 0 | 0.7922 | 0.1099 | -0.2363 | 0 / 24 / 24 |

**ALL TWELVE CELLS ARE DECISION-IDENTICAL AND EQUAL TO ACTING ON EVERYTHING: +0.0000.**
`H_CAPITAL` HELD, worst |delta| 0.0094 against either reference. **The degeneracy is published
rather than dressed up** (1223's lesson): the ANY quantifier is saturated, because every (panel,
ladder) cell is cited by 44-176 population units and some one of them always has a recoverable L.
The quantifier CONTROL — reported, never a third dial, and no book is selected on it — shows the
admission rule is a **step function with no middle**: the per-cell recoverable share runs
**0.117-0.265** and never reaches 0.50, so Q_MAJORITY and Q_ALL admit **0 of 72** and collapse
onto doing nothing. There is no setting of this rule that produces an interesting book.

The only thing in the whole arm that beats acting on everything is **doing nothing**, which holds
24 of the 72 4b passes against any acting rule's 6 — the record's standing result, reproduced here
a fourth time.

## Hypotheses, scored

| | statement | result | value |
|---|---|---|---|
| H_REACH | >= 0.90 of the claim set resolves to a committed script | **FAILED** | 0.8799 |
| H_LADDER | among resolved units, LADDER scripts outnumber PINNED | **FAILED** | 100 vs 117 |
| H_STEM | A_STEM alone reaches more units than A_COL alone | HELD | 491 vs 428 |
| H_HEAD63 | the modal PINNED L is the frozen 63 at share >= 0.50 | HELD | 63 at 0.7513 |
| H_EDIT | units repairable by EDIT outnumber units owing a re-run | **FAILED** | 217 vs 857 |
| H_SCOPE | a majority of SILENT units' scripts never draw a block | HELD | 650/728 = 0.8929 |
| H_CAPITAL | no cell moves mean OOS Sharpe by > 0.02 vs both refs | HELD | 0.0094 |

Three of seven failed and all three are reported as failed rather than re-barred. The CENSUS arm
is labelled **CALIBRATED** throughout: it was built in a wiring prototype before the file was
written, so its counts are measurements against 1243's committed file, not forecasts. ARMS B, C,
C2, D and E were unmeasured when the hypotheses were fixed.

## What the record should take from this, in one sentence

**1243's 1,074 is not 1,074 verdicts that lost their block length — it is 217 that can be stamped
from their own code for free, 78 that genuinely lost one, 129 nobody can attribute, and 650 that a
resample-keyed clause should never have bound; the schema debate's cost side is a SCOPE problem,
not a re-run problem, and the honest bill is 207 re-runs and about a minute of compute.**

## Survivorship (rule 9)

U56 and B136 are CURRENT-constituent lists; SMALL is a current sub-$2B screen (664 investable, 51
dropped for max_1d_move >= 1.0). A current-constituent panel flatters momentum drawdowns, so the
4b drawdown leg in ARM E is measured against a flattered comparand. The census, attribution,
recovery and bill arms are price-free and immune; only ARM E's 4a/4b legs carry the bias.

## Not modified

RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py. **No rules change is proposed.** The scope
finding bears on 1247's PROTOCOL 10 proposal and is left for the Sunday review (rule 6) to weigh
as a correction to that proposal's cost estimate, not as a second proposal.

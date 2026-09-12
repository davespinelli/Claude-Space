# Idea 843 (lane C, 2026-09-12) — how many committed "k of n books/arms" counts disagree with their own committed table?

**ANSWERED: THE ANCHOR IS NOT AN ANECDOTE — between 15% and 23% of the record's books/arms counts
cannot be reproduced from the tables the same file committed, and a fifth of them cannot be checked
at all. KILL for capital (a census buys no book); no RULES change, no book promoted, no KEEP
claimed, no memo. RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched (rule 6). One
PROTOCOL line is PROPOSED, NOT APPLIED.**

Corpus: **837 committed documents** (709 `.result.md`, 128 memos) and **4,086 committed CSVs** under
`research/backtests/`; **3,952 "k of n" claims** extracted from **713** of those documents; 3,803
sibling CSVs read, 5 skipped (>20 MB), 2 skipped (>200,000 rows), 0 unreadable. Two tuned
parameters only — **count detector** (D1/D2/D3) and **sample** (S1/S2/S3) — and all 9 grid points
are reported below.

## Gates (printed before any new number)

| gate | result |
|---|---|
| **G1 ANCHOR** | idea 839's `.perbook.csv`, cell `OVERLAP21/H756/OTHER3`, col `delta` → **8 negative / 1 positive / 2 zero of 11 defined** (12 rows of 47) — **PASS**; idea 832's prose "9 of 11" is not in the table |
| **G2 DETERMINISM** | extractor run twice on 120 documents → 449 claims, sha `c14b0b7a23f259c2` both times — **PASS** |
| **G3 DETECTOR UNIT TEST** | planted count recovered **18/18** (D1/D2/D3 × 6 synthetic tables); negative control (unreachable k=5) held — **PASS** |
| **G4 PRICE** | RULES v2 **8.63% / 1.2018 / −12.05%** vs committed 8.66% / 1.2056 / −12.05%; SPY **15.16% / 0.8861 / −33.72%** vs 15.23% / 0.8890 / −33.72% (bars 1.00pp/0.060/2.00pp) — **PASS** |
| **G5 PARTITION** | corpus walk-forward split exhaustive and disjoint: IS 347 files / 1,873 claims + OOS 366 files / 2,079 claims = 3,952 — **PASS** |
| **G6 STANDING CANDIDATE** | reconstructed U56 top-20 book **12.65% / 1.0918 / −18.31%**, halves 1.097/1.094, OOS 1.1669 vs its memo's 12.79% / 1.064 / −18.31%, 1.068/1.066, OOS 1.131 — **PASS** |

## P1 × P2 — the whole 3×3 grid (every point reported)

| sample | detector | claims | re-derivable | not re-derivable | agree | **disagree** | disagree rate | agree rate | chance floor | excess |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 books/arms | D1 | 174 | 89 | 85 | 65 | **24** | 0.2697 | 0.7303 | 0.3037 | +0.4267 |
| **S1 books/arms** | **D2 (headline)** | **174** | **139** | **35** | **107** | **32** | **0.2302** | **0.7698** | **0.5311** | **+0.2387** |
| S1 books/arms | D3 | 174 | 139 | 35 | 118 | **21** | 0.1511 | 0.8489 | 0.6559 | +0.1930 |
| S2 units | D1 | 1,148 | 557 | 591 | 392 | 165 | 0.2962 | 0.7038 | 0.3442 | +0.3596 |
| S2 units | D2 | 1,148 | 942 | 206 | 790 | 152 | 0.1614 | 0.8386 | 0.6126 | +0.2261 |
| S2 units | D3 | 1,148 | 942 | 206 | 849 | 93 | 0.0987 | 0.9013 | 0.7131 | +0.1882 |
| S3 all nouns | D1 | 3,952 | 1,649 | 2,303 | 1,187 | 462 | 0.2802 | 0.7198 | 0.3696 | +0.3502 |
| S3 all nouns | D2 | 3,952 | 3,175 | 777 | 2,680 | 495 | 0.1559 | 0.8441 | 0.5966 | +0.2475 |
| S3 all nouns | D3 | 3,952 | 3,175 | 777 | 2,882 | 293 | 0.0923 | 0.9077 | 0.6997 | +0.2080 |

**Read the DISAGREE column, not the agree column.** The chance floor is the probability that a
uniformly random numerator in [0, n] would also have been called AGREE by the same detector on the
same tables: 0.30–0.70. Agreement clears its floor at every one of the 9 points (+0.19 to +0.43),
so the machinery is measuring something — but at a floor of 0.53 an individual AGREE is weak
evidence. A DISAGREE is the informative side: the detector could produce 10–209 other counts from
that file's own tables and not the one the file published.

**The conservative number is the widest detector's.** D3 adds value-equality and paired-column AND
predicates, so it reproduces the most claims; what it still cannot reproduce is the tightest upper
bound this run can put on genuine mis-statements: **21 of 139 re-derivable books/arms counts
(15.1%), spread over 15 distinct files**. At the headline detector it is 32 of 139 (23.0%) over 22
files.

## What the disagreements look like

Of the 32 at the headline cell: **20 have n > 100** and only **4 have n ≤ 20**; **15 are off by
exactly 1**, 20 by ≤ 2, 26 by ≤ 5, and **6 by more than 5**: `140 of 288 arms` (nearest 96, −44),
`184 of 256 arms` (216, +32), `45 of 72 books` (63, +18), `72 of 306 books` (89, +17),
`82 of 306 books` (89, +7), `41 of 352 books` (47, +6). The shape is off-by-a-few prose
attached to large machine-generated tables, not invention — but the record quotes these counts as
findings, and 6 of them are not near misses.

The full D3 list (the 21 that survive the widest detector) is in `.disagree.csv`; the two that are
small enough for a human to check by eye are:

| file | claim | nearest reachable count |
|---|---|---|
| `2026-09-12_is-the-ONE-RUNG-4b-BAND-a-property-of-every-book-or-of-the-DD-CAP_C` | `11 of 27 books` | 8 |
| `2026-09-12_is-the-NEGATIVE-NEXT-WINDOW-sign-...-CONDITIONING-artefact_cloud` | `9 of 11 books` (quoting idea 832) | 8, via `delta<=0` |

## H_ANCHOR — the machinery rediscovers the queue's own case, blind

In idea 839's file, the three n=11 claims classify as: **`9 of 11 books` → DISAGREE** (nearest 8,
via `delta<=0`), **`8 of 11` → AGREE**, `9 of 11` (second mention) → DISAGREE. The detector was
never told which was right. **H_ANCHOR CONFIRMED.**

## Not re-derivable at all

**35 of 174 books/arms claims (20.1%)** have no committed table of matching size anywhere in the
file that published them — under D1 (whole tables only, no group-by) it is 85 of 174 (48.9%).
Across all 3,952 claims: **777 (19.7%)** under D2/D3, 2,303 (58.3%) under D1.
**H_SOURCE (≥25%) is REFUTED at D2/D3 and CONFIRMED at D1** — i.e. the record's counts are usually
checkable only because its tables are group-able, not because the file points at the right rows.

## Rule 8

**Corpus walk-forward** (cell chosen on files ≤ 2026-09-07, the rest read once): the IS-worst cell
(D1, S1) goes **0.3023 (n=43) → 0.2391 (n=46), drift −0.0632** — inside the pre-registered 0.10
band, so **H_WF CONFIRMED for the rule-8 pick**; at the headline cell (D2, S1) the drift is
**0.2838 → 0.1692 = −0.1146**, just outside it. The level is stable to about ±0.06–0.11, so the
honest statement is "between one in seven and one in four", not a number to 1 pp. All 9 IS/OOS
pairs are in `.wf.csv`.

**PROTOCOL rule-8 price table** (this census proposes no book; reported because the protocol
requires it — U56, weekly, t+1, 10 bps, warm-up 260 days, IS ≤ 2016-12-31, OOS 2017+):

| book | CAGR | Sharpe | MaxDD | H1 / H2 Sharpe | IS Sharpe | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|---|---|
| standing 4b candidate (U56 top-20 composite, g0.75, W) | 12.65% | 1.0918 | −18.31% | 1.0965 / 1.0939 | 0.9935 | 14.33% | 1.1669 | −18.31% |
| RULES v2 baseline (live) | 8.63% | 1.2018 | −12.05% | 1.2349 / 1.1757 | 1.1043 | 9.47% | 1.2782 | −12.05% |
| RULES v1 (previous) | 6.41% | 0.6602 | −13.83% | 0.6510 / 0.6718 | 0.5588 | 7.60% | 0.7361 | −13.83% |
| SPY | 15.16% | 0.8861 | −33.72% | 0.9595 / 0.8259 | 0.8986 | 15.33% | 0.8767 | −33.72% |

**Both KEEP paths, read literally, on the standing candidate: 4a FAIL** (H1 1.0965 vs v2's 1.2349,
H2 1.0939 vs 1.1757, MaxDD −18.31% vs −12.05%); **4b PASS** (H1 1.0965 > SPY 0.9595, H2 1.0939 >
0.8259, OOS 1.1669 > 0.8767, MaxDD −18.31% ≥ cap −20.23%, CAGR 12.65% ≥ floor 10.61%). Nothing in
this run changes that book or claims it: **H_NOBOOK CONFIRMED — a census cannot clear either path,
and this run promotes nothing.**

## Hypotheses, as pre-registered

| hypothesis | result |
|---|---|
| H_RATE ≥10% of re-derivable books/arms counts disagree | **CONFIRMED** — 23.0% (D2), 15.1% (D3) |
| H_ANCHOR 839's "8 of 11" agrees, 832's "9 of 11" does not | **CONFIRMED** exactly |
| H_FLOOR agreement clears its chance floor by ≥0.10 | **CONFIRMED** — +0.2387 at the headline, +0.19…+0.43 everywhere |
| H_SOURCE ≥25% of all claims have no table of matching size | **REFUTED at D2/D3** (19.7%), CONFIRMED at D1 (58.3%) |
| H_WF IS→OOS drift within 0.10 | **CONFIRMED for the rule-8 pick** (−0.063), refused at the headline cell (−0.115) |
| H_NOBOOK the census yields no tradeable book | **CONFIRMED** |

## Verdict and the one line proposed (NOT applied — rule 6)

**CONFIRM of the queue's premise, KILL for capital.** Idea 839's "9 of 11" is one of at least 21
committed counts that their own tables do not support; the record's prose counts carry an error
rate of roughly **1 in 7 to 1 in 4**, concentrated in large-denominator claims, and a fifth of all
counts cannot be checked against the publishing file at all.

Proposed for the Sunday review, not applied here:

> **PROTOCOL 5a.** Every published "k of n" count must name the committed artefact it is read from
> — file, column, and the filter applied (e.g. `…perbook.csv`, `cell==OVERLAP21/H756/OTHER3`,
> `delta<0`). A count that no committed table reproduces is not a finding.

Cheap test of the cost of that line: 20.1% of the record's books/arms counts would fail it today
for lack of a matching table, and a further 15.1% for lack of a matching predicate.

Artefacts: `.py`, `.txt`, `.claims.csv` (3,952 rows, all three detectors), `.grid.csv` (9 cells),
`.disagree.csv` (headline-cell disagreements with nearest reachable count), `.wf.csv` (corpus
walk-forward + price rule-8 table).

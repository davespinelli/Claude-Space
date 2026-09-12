# Idea 574 — re-sweep-the-record-s-TEN-most-cited-UNSWEPT-4b-passes-in-GROSS (cloud, 2026-09-12)

**ANSWERED = 1 of 10 SURVIVES / KILL for capital. Only one of the ten most-cited unswept 4b passes
still passes 4b at its own published gross on today's data at PROTOCOL's 10 bps, and the admissible
gross band has a MEDIAN WIDTH OF ONE RUNG (of 17) among the five books that pass anywhere at all.
The whole 10 × 17 ladder yields 8 passing cells of 170 at 10 bps and 4 of 170 at 25 bps. A
cost/vintage decomposition recovers only 1 of the 9 failures, so this is not a cost or sample-end
story. No KEEP: 4a 0 / 4b 8 / BOTH 0.**

Script: `2026-09-12_re-sweep-the-record-s-TEN-most-cited-UNSWEPT-4b-passes-in-GROSS_cloud.py`
Artefacts: `.census.csv .books.csv .rebuild.csv .decomposition.csv .grid.csv .bands.csv
.walkforward.csv .keeppaths.csv .console.txt`

## The census (unit stated before the number)

LEADERBOARD.md carries **5,409** dated rows; **594** assert a 4b pass under the pre-stated lexicon
(`KEEP-candidate (4b) | 4b PASS | passes 4b | 4b KEEP | KEEP (4b)`), naming **397** distinct
producing scripts (2 rows name none).

A script counts as SWEPT if either of two independent detectors finds ≥2 distinct gross values: an
AST scan of the source, or a `gross`/`g` column with ≥2 distinct values in any committed `.csv` of
its own stem. **G0: the two detectors agree on 283 of 397 scripts**; 8 are swept by the AST scan
only and 106 by the csv scan only, and the union is used — the census is not one regex's opinion.

| unit | swept | unswept | unswept share |
|---|---|---|---|
| scripts | 209 | 188 | **47.4%** |
| 4b-pass leaderboard rows | 320 | 274 | **46.1%** |

**UNIT WARNING.** Idea 311's 98.1% counted committed GRID rows inside `.csv` artefacts. This run
counts PUBLISHED LEADERBOARD rows. These are different denominators and both are published here;
this run does **not** restate one as the other, and 46.1% is not a refutation of 98.1%.

**121 of the 272** unswept 4b-pass rows resolve to a canonical book key under the documented token
lexicon (151 do not and are excluded, with their count published). Those 121 rows collapse to only
**36 distinct book keys** — the most-cited rows are not distinct books, and the ten below are the
top ten by summed citations over keys, not over rows.

## The ten and their ladders

Rungs run g = 0.20 → 1.00, step 0.05. `P` = passes 4b at 10 bps, `.` = fails, `[ ]` marks the
published rung.

```
 #  book key                     cit   20 25 30 35 40 45 50 55 60 65 70 75 80 85 90 95 00
 1  U56/R620/g0.75/M             603    .  .  .  .  .  .  P  P  P  .  . [.] .  .  .  .  .
 2  U56/CAND20/g0.75/M           519    .  .  .  .  .  .  .  .  .  .  . [P] P  .  .  .  .
 3  B136/EWALL/g0.75/W           134    .  .  .  .  .  .  .  .  .  .  . [.] .  .  .  .  .
 4  U56/EWALL/g0.75/W            132    .  .  .  .  .  .  .  .  .  P  . [.] .  .  .  .  .
 5  U56/CAND20/g0.75/W            93    .  .  .  .  .  .  .  .  .  .  . [.] .  P  .  .  .
 6  U56/CAND20/g0.80/W            84    .  .  .  .  .  .  .  .  .  .  .  . [.] P  .  .  .
 7  B136/CAND20/g0.75/W           76    .  .  .  .  .  .  .  .  .  .  . [.] .  .  .  .  .
 8  B136/MA-DG/g0.75/W            68    .  .  .  .  .  .  .  .  .  .  . [.] .  .  .  .  .
 9  BSTK100/CAND20/g0.75/W        68    .  .  .  .  .  .  .  .  .  .  . [.] .  .  .  .  .
10  SMALL/CAND20/g0.75/W          34    .  .  .  .  .  .  .  .  .  .  . [.] .  .  .  .  .
```

| # | published g | rungs passing | band | published passes | on edge | flips |
|---|---|---|---|---|---|---|
| 1 | 0.75 | 3 | 0.50–0.60 | False | – | True |
| 2 | 0.75 | 2 | 0.75–0.80 | **True** | True | True |
| 3 | 0.75 | 0 | – | False | – | False |
| 4 | 0.75 | 1 | 0.65 | False | – | True |
| 5 | 0.75 | 1 | 0.85 | False | – | True |
| 6 | 0.80 | 1 | 0.85 | False | – | True |
| 7–10 | 0.75 | 0 | – | False | – | False |

At 25 bps the pass counts fall to 2 / 1 / 0 / 1 / 0 / 0 / 0 / 0 / 0 / 0 — **4 cells of 170**.

## The six pre-registered hypotheses: 2 of 6

| | claim | reading | verdict |
|---|---|---|---|
| H_KEEP | ≥6 of 10 published points still pass 4b | **1 of 10** (book 2) | **FAIL** |
| H_FLIP | ≥8 of 10 flip somewhere on their ladder | 5 of 10 — the other five **never pass at any gross**, which is worse than flipping | **FAIL** |
| H_NARROW | median band ≤ 6 of 17 rungs | **1.0 rung** over 5 passers | **PASS** |
| H_EDGE | published g within one rung of an endpoint in ≥5 | 1 (only one book passes at its own g at all) | **FAIL** |
| H_MONO | pass set contiguous in g for every passer | 5 of 5 | **PASS** |
| H_WF | IS band contains the OOS band's midpoint in ≥6 of 10 | **2 of 10** | **FAIL** |

H_FLIP and H_EDGE fail for the same reason and it is not a charitable one: they were written
assuming the published points would mostly still pass, so that "where in the band" would be the
interesting question. It is not. Nine of ten do not pass at their own gross, and half do not pass
at any gross on the 17-rung ladder.

## Is it gross, or is it cost and vintage?

Each book re-read at its own published gross under four conventions — this run's (10 bps, sample to
today) and three the rows themselves used (5 bps, and truncation at the row's own publication date):

| # | 10bps/today | 5bps/today | 10bps/as-of | 5bps/as-of |
|---|---|---|---|---|
| 2 U56/CAND20/g0.75/M | **PASS** | PASS | PASS | PASS |
| 6 U56/CAND20/g0.80/W | fail | **PASS** | fail | **PASS** |
| 1, 3, 4, 5, 7, 8, 9, 10 | fail | fail | fail | fail |

**Only 1 of the 9 failures recovers** under a cheaper cost rung or an earlier sample end. Book 6's
pass is bought entirely by the 5 bps convention, which PROTOCOL rule 2 does not permit. The
remaining eight fail under every convention tried, so the failure is a property of the book, not of
the cost rung or the vintage.

## Rebuild fidelity (G3 — measured, not gated)

Eight of the ten leaderboard rows carry **more than one percentage** in their CAGR or MaxDD cell
(multi-panel or multi-arm rows), so their "published triple" is not a single number and they are
excluded from the fidelity statistic. On the two unambiguous rows, median |ΔSharpe| **0.0948**, max
0.0995, median |ΔMaxDD| 2.95%. Books far from their published triple — book 10 at ΔSharpe −0.5392
is the extreme — are canonical rebuilds of the book the row *names*, not byte-reproductions of the
row, and their bands describe that canonical book. **This is the study's main limitation and it is
not hidden: for eight of the ten, the row itself does not publish a single book to reproduce.**
That is itself a finding about the record's row format.

## Rule 8

**WF-A.** The 4b legs recomputed inside the IS window alone and the OOS window alone:

| # | IS band | OOS band | IS mid | OOS mid | IS band contains OOS mid |
|---|---|---|---|---|---|
| 1 | 0.50–0.85 | 0.50–0.60 | 0.68 | 0.55 | True |
| 2 | 0.75–0.85 | 0.75–0.80 | 0.80 | 0.78 | True |
| 3 | 0.55–0.60 | – | 0.57 | – | False |
| 4 | 0.65–0.75 | 0.60–0.65 | 0.70 | 0.62 | False |
| 5, 6 | – | 0.80–0.85 | – | 0.82 | False |
| 7, 8, 10 | – | – | – | – | False |
| 9 | 0.60–0.80 | – | 0.70 | – | False |

**2 of 10.** Six of the ten have an empty band in at least one window, so for those "this book has a
gross band" is not a walk-forwardable statement at all.

**WF-B** (gross chosen per book by IS Sharpe alone, OOS read once, 10 bps): **nine of ten pick
g = 1.00** — the IS Sharpe surface is monotone in gross, which is idea 311/576's zero-cash-leg
artefact showing up again. Comparands OOS: RULES v2 9.47% / 1.278 / −12.05%; SPY 15.33% / 0.877 /
−33.72%.

| # | g\* | IS Sharpe | OOS CAGR | OOS Sharpe | OOS MaxDD | 4a | 4b |
|---|---|---|---|---|---|---|---|
| 1 U56/R620/M | 1.00 | 1.296 | 22.30% | 1.115 | −30.59% | False | fail DD |
| 2 U56/CAND20/M | 1.00 | 1.107 | 15.30% | 1.048 | −23.64% | False | fail DD |
| 3 B136/EWALL/W | 1.00 | 1.148 | 18.39% | 1.091 | −32.72% | False | fail DD |
| 4 U56/EWALL/W | 1.00 | 1.112 | 18.34% | 1.129 | −29.18% | False | fail DD |
| 5, 6 U56/CAND20/W | 1.00 | 0.953 | 14.03% | 1.019 | −22.79% | False | fail DD |
| 7 B136/CAND20/W | 1.00 | 0.985 | 9.96% | 0.734 | −22.88% | False | fail H2,OOS,DD |
| 8 B136/MA-DG/W | 1.00 | 1.057 | 10.40% | 1.114 | −16.63% | False | fail CAGR |
| 9 BSTK100/CAND20/W | 1.00 | 1.158 | 11.34% | 0.745 | −26.59% | False | fail H2,OOS,DD |
| 10 SMALL/CAND20/W | 0.20 | 0.913 | 1.20% | 0.417 | −8.75% | False | fail H2,OOS,CAGR |

**7 of 10 beat SPY on OOS Sharpe, 0 beat the live RULES v2 book, 0 are 4a True, and 0 pass 4b** —
every one of the eight that clear the Sharpe legs is killed by the drawdown cap at g = 1.00. The
IS-Sharpe selector walks each of these books straight past its own admissible band.

## KEEP paths

| cost | cells | 4a | 4b | BOTH |
|---|---|---|---|---|
| 10 bps | 170 | **0** | **8** | **0** |
| 25 bps | 170 | 0 | 4 | 0 |

Fail-4b leg census at 10 bps: CAGR alone 77, DD alone 34, H2+OOS+CAGR 31, H2+OOS+DD+CAGR 12,
pass 8, H2+OOS+DD 8. **No capital candidate.**

## Caveats

* **Survivorship.** U56 / B136 / BSTK100 are current constituents of `universe.json` /
  `universe_broad.json`; the sub-$2B panel is the current constituent list of its screen with the 52
  `max_1d_move ≥ 1.0` tickers dropped per PROTOCOL. Dead names are absent from all four, so every
  CAGR here is biased upward and every 4b CAGR-floor pass is **easier** than on a point-in-time
  panel. The bias therefore works *against* this run's negative finding, not for it.
* Eight of the ten rows do not publish a single reproducible triple (above). Their bands are
  statements about the canonical book their text names.
* The lexicon assumes gross 0.75 and weekly cadence where the row states neither; every such
  assumption is flagged in `.books.csv` (books 7, 8 assume cadence; book 7 assumes gross).
* The selection of "the ten" is vintage-dependent: the record grows, so the citation ranking will
  move. The full 36-key ranking is committed in `.census.csv` / `.books.csv`.

## Consequence for the record

The queue's framing was that these passes need a gross sweep. They need more than that: **at
PROTOCOL's own 10 bps, on today's panels, nine of the ten most-cited unswept 4b passes do not pass
4b at their published gross, and five of them do not pass at any of 17 grosses.** Where a band does
exist it is one to three rungs wide and the published point is outside it in four of five cases. A
4b pass quoted at a single gross should be read as a coordinate on a knife edge until it is swept —
and the sweep, run here, mostly removes it. No RULES, PROTOCOL, scan.py, bot.py or baseline.py edit;
nothing outside this run's own outputs was touched.

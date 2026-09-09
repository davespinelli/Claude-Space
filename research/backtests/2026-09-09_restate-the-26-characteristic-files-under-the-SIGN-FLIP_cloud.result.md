# Idea 295 — restate the 26 characteristic files under the SIGN FLIP (cloud, 2026-09-09)

Run: `research/backtests/2026-09-09_restate-the-26-characteristic-files-under-the-SIGN-FLIP_cloud.py`
(`--reuse` re-runs the analysis off `.arms.csv`; artefacts `.census.csv` 26 rows, `.arms.csv` 504 rows,
`.slopes.csv` 432 rows, `.grid.csv` 64 rows, `.filegrid.csv` 832 rows, `.walkforward.csv`,
`.keeppaths.csv`, `.console.txt`).

**VERDICT: ANSWERED / KILL OF THE QUESTION AS ASKED. "How many published direction claims survive"
has no answer, because the (a)/(b)/(c) classification is not a property of the file — it is a
property of the STRATUM RESOLUTION, an unpublished dial. At 3 strata nothing is zero and nothing
reverses (13 of 26 files SURVIVE); at 21 strata nothing survives (0 of 26). Over the 16 grid points
the surviving count runs 0..13 (median 6.5) on the wide reading and 0..7 (median 1.0) on the tight
one, while the |t| bar moves it barely at all. And the classification does not walk forward: the
in-sample verdict comes back out-of-sample in 37 of 64 cells (57.8%), and for `evol` in 4 of 16
(25%). No KEEP, no memo, no RULES change.**

## What was run

**A. The census (no sampling).** The 26 files are re-derived from idea 276's own committed census
(`2026-09-06_is-breadth-a-small-cap-dummy-everywhere-in-the-record_cloud.census.csv`, `cross & prop &
cmp`). Each file's headline block is extracted mechanically and scanned for the four characteristics
idea 271/284 named. Two readings are carried, both committed, neither a tuned parameter: **WIDE**
(the word anywhere in the 1,500-char headline block) and **TIGHT** (the word inside the bolded
verdict clause, first 300 chars, with a bare `vol20` and a bare `corr` dropped as non-attributions).

**B. The sign flip priced.** Idea 276's MIX rebuilt: k=40 names, a share q from the sub-$2B panel
(44 `max_1d_move ≥ 1.0` names dropped first, 439 usable) and 1−q from the 100-name large-cap **stock**
pool (ETFs excluded), **21 q rungs × 8 draws = 168 panels** on one common window (2010-01-04 ..
2026-09-04). Each panel's four characteristics measured with idea 284's verbatim definitions. Books:
top10, top20, EWall control, RULES v2 as the 4a comparand. 10 bps, weekly, next-day execution,
260-day warm-up skip. Every characteristic × outcome slope estimated twice — **pooled** across the
cap line (the published reading) and **within stratum** (both sides demeaned inside the q bin).

Two tuned parameters, all 16 grid points reported: **t_bar ∈ {1.000, 1.645, 1.960, 2.576}** and
**strata ∈ {3, 5, 7, 21}**.

## 1. The finding — the classification is a resolution statement, not a file property

Modal characteristic verdict, over 9 (arm × outcome) cells each:

| strata | breadth | disp | corr | evol |
|---|---|---|---|---|
| 3 | SURVIVES | SURVIVES | SURVIVES → ZERO | SURVIVES |
| 5 | SURVIVES | ZERO | ZERO | SURVIVES |
| 7 | ZERO | REVERSED | REVERSED → ZERO | SURVIVES → ZERO |
| 21 | ZERO | REVERSED | REVERSED | SURVIVES → ZERO |

(the arrow is the move from t_bar 1.000 to 2.576 — i.e. the |t| bar changes almost nothing; the row
you are on changes everything.)

File counts at the two ends of the strata dial (WIDE reading, t_bar = 1.960):

| class | strata 3 | strata 5 | strata 7 | strata 21 |
|---|---|---|---|---|
| SURVIVES | **12** | 8 | **0** | **0** |
| (a) ZERO once controlled | 1 | 5 | 9 | 7 |
| (b) SIGN-REVERSED once controlled | 0 | 0 | 4 | 6 |
| NOT RESTATABLE (headline names no characteristic) | 10 | 10 | 10 | 10 |
| NOT RESTATABLE (non-price instrument) | 1 | 1 | 1 | 1 |
| LEDGER (no headline claim) | 2 | 2 | 2 | 2 |

At the central point (t_bar 1.960, strata 5): **8 of 26 survive on the wide reading (30.8%), 2 of 26
on the tight one (7.7%)**. Neither number is publishable on its own, because the same run produces
13 and 0 at the same |t| bar by moving a dial no source file ever named.

## 2. Idea 284's sign flip does reproduce — at fine resolution, and not for `evol`

Idea 284's headline was: breadth's within-stratum content is zero, disp/corr/evol reverse sign. On
this ladder **breadth → ZERO and disp → REVERSED and corr → REVERSED all reproduce at strata ≥ 7**,
but **`evol` never reverses modally at any grid point** — it is the one characteristic whose pooled
sign survives the control (SURVIVES at strata 3 and 5, ZERO at 7 and 21, REVERSED at none). Example
slopes (EWall, full window, x standardized): `evol` vs MaxDD pooled −0.058 (t = −13.7), within
−0.036 / −0.033 / −0.031 / −0.023 (t = −8.7 / −8.1 / −7.7 / −6.0) across the four resolutions — same
sign throughout. Against that, `disp` vs Sharpe goes pooled −0.201 (t = −16.4) → within +0.025
(t = +2.9) at 21 strata, a clean flip.

## 3. Idea 276's "26 characteristic files" is an overcount, as idea 276 itself warned

**10 of the 26 name none of the four characteristics anywhere in their headline block (16 of 26 on
the tight reading); 2 are ledgers (LEADERBOARD.md, CHANGELOG.md, which carry no headline claim of
their own); 1 rests on a non-price instrument (Form 4).** So at most 13 files — and on the tight
reading at most 7 — carry a characteristic direction claim that this ladder can restate at all. Idea
276 published 26 as a keyword-level lower bound on the exposed set and said so; read as a count of
direction claims it is roughly 2× too large. No file in the 26 already controls cap mix in its own
headline, so class (c) is empty here.

## 4. Rule 8 (PROTOCOL 8) — the classification fixed on the first half, the second read once

| characteristic | IS verdict comes back OOS | IS modal | OOS modal |
|---|---|---|---|
| breadth | 13/16 (81.2%) | ZERO | SURVIVES |
| corr | 10/16 (62.5%) | ZERO | ZERO |
| disp | 10/16 (62.5%) | ZERO | REVERSED |
| **evol** | **4/16 (25.0%)** | SURVIVES | REVERSED |
| **all** | **37/64 (57.8%)** | | |

A three-way label that reproduces itself out-of-sample 58% of the time cannot retire or confirm a
published claim. This is the decisive leg: even holding the strata dial fixed, the verdict is not
stable across the sample halves.

## 5. The books themselves — both KEEP paths, no selection (all 504 arm-rows)

| arm | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR | OOS Sharpe | OOS MaxDD | 4a | 4b |
|---|---|---|---|---|---|---|---|---|---|
| EWall | 8.8% | 0.726 | −27.9% | 0.914 / 0.599 | 8.4% | 0.692 | −27.8% | 0.0% | 6.5% |
| top10 | 9.1% | 0.712 | −23.9% | 0.808 / 0.590 | 9.1% | 0.681 | −23.7% | 0.0% | 1.8% |
| top20 | 7.7% | 0.777 | −18.4% | 0.880 / 0.674 | 7.7% | 0.744 | −18.3% | 0.0% | 16.1% |
| RULES v2 (live, same panels) | 6.4% | 0.857 | −13.2% | 0.941 / 0.767 | 6.3% | 0.835 | −13.2% | — | — |
| SPY | 14.1% | 0.862 | −33.7% | 0.891 / 0.858 | 15.5% | 0.882 | −33.7% | — | — |

**4a passes 0/504 (0.0%); 4b passes 41/504 (8.1%)**, and every 4b pass sits at q ≤ 0.20 — the
per-rung table in `.console.txt` shows top20 at 1.000 for q ∈ {0, 0.05, 0.20} and 0.000 at all
sixteen rungs from q = 0.25 up. Nothing here is a candidate; this section exists so the classification
above is priced against the live book and SPY rather than floating free.

## Caveats

- The census stage is keyword matching on a headline block. It is mechanical and committed so it can
  be re-read, and both a wide and a tight reading are carried, but it is not a semantic pass; a file
  that attributes a result to a characteristic without naming it is missed by both.
- Class **(c) already within-stratum** is empty: no headline in the 26 uses a stratum / fixed-cap-mix
  / matched-q phrase. That is a finding about the record's vocabulary, not evidence that no file
  controlled for cap mix in its body.
- **SURVIVORSHIP.** The sub-$2B panel and B136 are *current* constituents of their screens, so every
  mixed panel inherits that bias on its small-cap side and the LEVEL of every number here is
  optimistic. The object under test is the WITHIN-vs-POOLED sign contrast, which survivorship moves
  only through the level of the eligible share; no level comparison across q is claimed as tradable.
- Two tuned parameters (t_bar, strata); all 16 grid points, all 432 slope rows and all 832 file×grid
  classifications reported.

RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched. No memo (no KEEP candidate).

**Follow-ups filed:** 532, 533, 534.

# Idea 666 (cloud, 2026-09-10) — is `regret` the only column in the record whose VALUES its source does not contain?

**Verdict: ANSWERED and SPLIT. KILL for capital.** The queue's premise is **two thirds
FALSIFIED and one third CONFIRMED**, and the census turned up a defect the queue did not ask
about and that is worse than the one it did: **the record publishes `regret` in two opposite
sign conventions under one column name**, so every cross-file aggregate over it is undefined.
No RULES change, no book promoted, no KEEP claimed, no PROTOCOL edit; RULES.md, PROTOCOL.md,
scan.py, bot.py and baseline.py untouched.

Script `2026-09-10_is-regret-the-only-column-whose-VALUES-its-source-does-not-contain_cloud.py`
(deterministic, standalone, no network, 57s); console `.console.txt`; CSVs `.reads.csv` (178),
`.censusgrid.csv` (42), `.signs.csv` (178), `.unrep.csv` (62), `.grid.csv` (162),
`.walkforward.csv` (30), `.keeppaths.csv` (6).

---

## GATES (pre-registered, run before any new number was read)

| | |
|---|---|
| G1 | `band_book(0.03, 0.75)` == `baseline.rules_v2_weights` at **0.000e+00**; the vectorised harness == `engine.backtest` at **6.939e-18** |
| G2 | cost-rung identity `r(25) = r(0) − turn·25/1e4` at **0.000e+00** |
| G3 | idea 664's committed `.tail.csv` reproduces its published headline off its OWN artefact: **1,508** tolerance-proof reads (664: 1,508), **1,442 `regret` = 95.6%** (664: 1,442 = 95.6%), **BOOK 1,459 / WINDOW 49** — exact |
| G4 | census partition exact at all 30 grid points, and REPRODUCED non-decreasing in tolerance within every definition |
| G5 | the two sign conventions are exact negatives on the live leg: max\|regret_BP + regret_PB\| = **0.000e+00** |

The run excludes its own output files from the population it audits (a first pass did not, and
the population read 148 files / 180 reads instead of 147 / 178 — the difference is this run's own
`regret_BP`/`regret_PB` columns, and the fix is in the committed script).

---

## THE POPULATION

**147 committed CSVs carry a column whose name contains `regret`: 178 (file, column) reads over
44 distinct spellings, 107,063 published values.** 122 of the reads are the bare spelling
`regret`. Six of the 178 are not regret values at all but flags, counters, p-values and an sd
(`has_regret`, `n_regret_vals`, `p_regret`, `regret_frac`, `regret_nonneg`, `regret_sd`); they
are kept in the pre-registered population (the rule was "the name contains regret") and the
headline is reported both ways.

## (1) RE-DERIVATION — the queue's question, at all 30 grid points

For each read, search the file's OWN other published numeric columns for a formula that
reproduces the column on **every** row. P1 = the definition family, P2 = the tolerance.

| definition | EXACT | 1e-12 | 1e-09 | 1e-06 | 1e-04 | 1e-03 |
|---|---|---|---|---|---|---|
| PAIR   `a − b` | 5 | 108 | 108 | 108 | 110 | 111 |
| PAIRABS `\|a\| − \|b\|` | 5 | 85 | 85 | 85 | 87 | 88 |
| PAIRPP `100·(a − b)` | 1 | 6 | 6 | 6 | 6 | 6 |
| GRPMAX `max(a\|cell) − a` | 1 | 1 | 1 | 1 | 1 | 1 |
| **ALL (union)** | **5** | **113** | 113 | 113 | 115 | **116** |
| NODATA / UNREADABLE | 0 | 0 | 0 | 0 | 0 | 0 |

**116 of 178 reads (65.2%) are re-derivable from their source's own columns; 62 (34.8%) are
not.** Restricted to the 172 that are regret VALUES: **116 reproduced (67.4%), 56 not (32.6%)**.
By published value rather than by column: **92,061 of 107,063 values (86.0%) are re-derivable,
15,002 (14.0%) are not.**

**The single most useful number in the table is the EXACT column: 5.** Only 5 of 178 regret
columns are bitwise reproducible, and 108 more appear the moment the tolerance reaches 1e-12.
That is the mechanism behind idea 664's tail: for the two thirds that ARE derivable, `regret` is
a *floating-point recomputation of a difference of two columns the source does publish* — a
subtraction, not a copy — so a membership test can never find it and a bitwise test can never
pass it, while a 1e-12 test recovers it immediately. **Idea 664's 1,442-read residual is
therefore not one finding but two**, and its BOOK label is right about the third that cannot be
rebuilt and wrong about the two thirds that can.

**All 62 unreproduced reads are PUBLISHED**: 60 sit in a file shipping a committed `.result.md`
or `.memo.md`, 62 are cited by LEADERBOARD.md / CHANGELOG.md / QUEUE.md, over **47 distinct
files**. The residue is not scratch output. The two largest are
`2026-09-08_make-PROTOCOL-quote-REGRET-instead-of-the-selection-MARGIN_cloud.cells.csv`
(`pub_regret`, 6,372 values, closest any definition gets: **4.78**) and
`2026-09-08_the-tenth-selection-loses-instance-as-a-distribution_cloud.cells.csv` (`regret`,
3,604 values, **4.82**) — both are the file that proposed the metric and its immediate
successor, both publish a regret column whose menu of arms they never published, and both are
cited. Every unreproduced read is listed with its column count in `.unrep.csv`.

## (2) THE DEFECT THE QUEUE DID NOT ASK ABOUT — one name, two opposite conventions

Parsing the producing scripts for `regret… = X − Y` and classifying by which side carries
best/oracle/max:

| declared orientation | assignments |
|---|---|
| `PICK_MINUS_BEST` (≤ 0) | **48** |
| `BEST_MINUS_PICK` (≥ 0) | **44** |

over 87 scripts. The committed columns realise the same split: of the 122 bare-`regret` reads,
**66 are non-negative, 40 non-positive, 15 mixed-sign, 1 all-zero**. Pooling the record's own
`regret` values across files gives mean **+0.0676** against a sign-normalised **+0.0786** — the
mixture destroys **14.0%** of the magnitude — and a range of **−0.8124 to +6.6639**.

The consequence is not cosmetic. The record's aggregators reduce a cell with
`("regret", "mean")`, `("regret", "min")` and `("regret", "median")` and then adopt the arm or
family with the **lowest** number. Under BEST_MINUS_PICK the lowest number is the smallest
shortfall — the right choice. Under PICK_MINUS_BEST the lowest number is the largest shortfall —
**the worst choice**. The same eight characters of code mean opposite things in 48 files and 44
files respectively, and nothing in the column name says which.

## (3) LIVE LEG — what the wrong reading costs, rule 8, 10 and 25 bps

Five pre-registered dial families (BAND, GROSS, N, CADENCE, VOLCAP; 27 arms) on U56, B136 and
SMALL439, weights at close *t* applied at *t+1*, weekly, 10 and 25 bps. Rule 8: the arm is
chosen on IS Sharpe over 2009–2016 and 2017-01-01.. is read once. `regret` is then computed both
ways and the family with the lowest number adopted, exactly as the record's aggregators do.

| panel | cost | family under BEST−PICK | under PICK−BEST | OOS Sharpe BP → PB | dSharpe | dCAGR | dMaxDD |
|---|---|---|---|---|---|---|---|
| U56 | 10 | GROSS | N | 1.2781 → 1.0566 | **+0.2215** | −18.27 pp | +20.62 pp |
| U56 | 25 | GROSS | N | 1.2415 → 0.9528 | **+0.2887** | −14.69 pp | +20.59 pp |
| B136 | 10 | GROSS | N | 1.1174 → 0.8442 | **+0.2732** | −10.15 pp | +17.36 pp |
| B136 | 25 | GROSS | N | 1.0732 → 0.7239 | **+0.3493** | −6.80 pp | +18.07 pp |
| SMALL439 | 10 | CADENCE | BAND | 0.6207 → 0.6255 | −0.0048 | −0.29 pp | +0.39 pp |
| SMALL439 | 25 | CADENCE | BAND | 0.5854 → 0.5978 | −0.0124 | −0.33 pp | +0.29 pp |

**The two readings adopt a DIFFERENT family in 6 of 6 (panel, cost) cells.** Mean cost of the
wrong reading **+0.1859 of OOS Sharpe** (range −0.0124 to +0.3493) and **+12.89 pp of OOS
MaxDD**, against **−8.42 pp of OOS CAGR** — the wrong reading systematically adopts the
high-return, high-drawdown top-*n* family. Reported honestly: on SMALL439 the wrong reading is
very slightly BETTER on Sharpe (−0.0048, −0.0124), because that panel's regret spread is an
order of magnitude tighter; the sign of the cost is not universal, its size is.

## KEEP paths — nothing to promote

162 books (3 panels × 27 arms × 2 rungs), both paths on every one.

* **4a: 2 / 162** (both SMALL439 band arms) — **4b: 5 / 162** — **BOTH: 0 / 162.**
* Per panel: U56 4a 0/54, 4b 4/54; B136 4a 0/54, 4b 1/54; SMALL439 4a 2/54, 4b 0/54.
* The five 4b passers are all restatements of books the record already carries: U56 GROSS 1.00
  (i.e. RULES v2 at gross 1, already memoed 2026-09-10), U56 N=40, U56 VOLCAP 0.30 and B136
  GROSS 1.00. Nothing new, no memo.
* Rule-8 picks beating the live book OOS: **9 / 30**. Beating SPY OOS: **17 / 30**.

## WHAT SHOULD CHANGE

1. **A `regret` column must publish its orientation.** The cheapest fix that needs no new
   computation is a naming convention — `regret_shortfall` (≥ 0, best − pick) vs `regret_signed`
   (≤ 0, pick − best) — plus a required sign assert in the producing script. Any aggregate that
   pools `regret` across files is currently unsound and 48 of 92 assignments are on the losing
   side of it.
2. **Idea 664's BOOK label needs splitting.** Two thirds of its 1,442-read `regret` residual is
   a subtraction of two published columns visible at 1e-12, not a different book. Its headline
   should be restated as "1,442 reads are not COPIES", which is true, rather than "not
   reproducible", which is false for 116 of the 178 columns.
3. **Nothing here is capital-relevant.** 0 of 162 books clear both KEEP paths and every 4b
   passer restates a standing candidate. This is a record-hygiene result, and the honest reading
   of the live leg is that the sign convention is worth up to a third of a Sharpe point *to a
   reader of the record*, not a source of edge.

## SURVIVORSHIP AND LIMITATIONS (stated, not hidden)

* SMALL439 is the CURRENT constituents of the sub-$2B screen (data/SMALL_PANEL_README.md); names
  that delisted are absent, so every small-panel return above is biased upward. The 44 tickers
  with `max_1d_move >= 1.0` in data/small_meta.csv were dropped before any book was built.
  B136 is likewise a current-constituent list. Only within-panel contrasts are load-bearing.
* The search covers pairwise and group-max forms. A regret built from three or more columns
  would be missed; `.unrep.csv` lists every unreproduced read with its numeric-column count so
  the residue is auditable rather than asserted.
* A file that computed regret against a menu it never published cannot be reproduced here. That
  is the finding, not a limit of the search — an unpublished input is precisely what "its source
  does not contain" means.

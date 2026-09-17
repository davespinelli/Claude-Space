# Idea 1158 — should a REGIME-to-LENGTH RATIO FIX its FRACTION LADDER or COUNT-MATCH its BETWEEN TERM?

**Lane cloud, 2026-09-17, idea 2 of 2.** Script
`research/backtests/2026-09-17_should-a-REGIME-to-LENGTH-RATIO-FIX-its-FRACTION-LADDER-or-COUNT-MATCH-its-BETWEEN-TERM_cloud.py`,
9 CSVs, console log. No RULES change, no book promoted, no PROTOCOL edit (rule 6); RULES.md,
PROTOCOL.md, engine.py, scan.py, bot.py and baseline.py untouched.

**SELECTION:** this lane takes the LAST eligible open idea. 1158 ended `## Open` and is not
EDGAR / Form 4 / 8-K / options / spin-off / live-data.

---

## ANSWER = NEITHER, AND THE TWO REPAIRS FIX DIFFERENT THINGS

Scored against the four outcomes declared before any number, in the declared order, the answer is
**(D) NEITHER** — and the reason is that the queue's two candidate repairs are not two answers to
one question, they are answers to two different questions:

- **R_FROZEN buys COMPARABILITY and pays for it with the LEVEL and the RESOLUTION.** Comparable
  at **18 of 18** (panel, statistic) cells by construction — but it **misses the resolved value at
  11 of 18 cells** (median relative gap **0.3221**), including **all three** cells of the record's
  headline statistic MAXDD, and its leave-one-ladder-out jackknife SE of log(ratio) is
  **0.6723 against R_COUNT-at-L8's 0.1722 — 3.9x wider.** Freezing a 3-rung ladder throws away
  the resolution the finer ladder bought.
- **R_COUNT is NOT a comparability repair at all.** Comparable at **2 of 18** cells, median
  max/min **2.083x** across the five ladders, worst **17.246x**. Count-matching the between term
  removes the *endpoint* inflation but the medians it averages still move with the ladder.
- **R_ASIS, the record's as-committed between term, is comparable at 0 of 18**, median max/min
  **3.715x**, worst **77.956x**.

**The combination is the clause the headline statistic needs, and only the headline statistic.**
`R_BOTH` (frozen ladder AND count-matched between term) is published because the pre-declared
scoring lands on (D) and a reader will ask. It is **not** a fourth dial value and is never
selected on. It is comparable at 18 of 18 by construction and **lands on the resolved value at
all three MAXDD cells at gaps of 0.0253 / 0.0886 / 0.0151** — an order of magnitude better than
freezing alone. But **it lands at only 4 of 18 cells overall** (median gap **0.3843**, *worse*
than R_FROZEN's 0.3221), because on ratio-valued statistics (SHARPE, CALMAR) the between term is
near zero and both repairs blow up together. **The combination is not reported as a general fix,
and the MAXDD row is not quoted without the 4-of-18.**

---

## THE TWO DIALS AND NO MORE (PROTOCOL rule 4, and the queue names both)

`REPAIR` {R_ASIS, R_FROZEN, R_COUNT} x `FRACTION LADDER` {L2, L3, L4, L6, L8} = **15 cells,
EVERY ONE PUBLISHED** in `.grid.csv`, at every (panel, statistic, construction, partition) —
1,080 rows.

- **R_ASIS** — 1148/1157's between term VERBATIM: `|m[1] - m[fmax]|`, a two-point range over the
  ladder's ENDPOINTS, so extending the ladder moves one of its two points.
- **R_FROZEN** — the clause names the ladder; BOTH terms are computed on L3 = {1,2,3} (1140's
  ladder, where 1148's committed number lives) no matter what ladder the run walked.
- **R_COUNT** — the between term is the EXACT mean |difference| over all C(k,2) pairs of the
  ladder's fraction-medians: the same count-free statistic 1148 used to repair the WITHIN term.

NOT dials, reported at every value: PANEL {U56, B136, SMALL}; the four DIAL LADDERS that are the
ratio's groups (CADENCE {D,W,M,Q}, GROSS 10 rungs, H {21,63,126,252}, N 9 rungs = **27 rung books
per panel, 81 in total, 1148's grid**); STATS {CAGR, VOL, SHARPE, MAXDD, ULCER, CALMAR} with MAXDD
the headline; PARTITIONS {ALIGNED, OFFSET}; CONSTRUCTIONS {C_POOLED (where 1148's committed number
lives), C_BOOK}; WITHIN terms {R_SPREAD, R_SD, R_MATCHED} with R_MATCHED the headline; the
jackknife; the three rule-8 choosers.

**NO BOOTSTRAP, AND THE REASON IS DECLARED UP FRONT.** A regime-to-length ratio compares sub-tapes
at their own POSITIONS on one tape. A moving-block resample destroys exactly that object — it
would leave the within term almost unchanged while making the between term meaningless, i.e. it
would manufacture this run's own answer. The resolution measure used instead is a
**leave-one-ladder-out jackknife over the ratio's own four groups**, which needs no resample at
all, plus the ALIGNED/OFFSET partition as a second axis. **This is a declared departure from
1157, which used a 200-rep block bootstrap for a different quantity.**

---

## GATES — 10 of 10 PASS, and two of them are exact replays of the record's own numbers

- **G1 PASS** fast runner == `engine.backtest` (U56 W/H126/N=20, gross 0.75), dev **1.39e-17**.
- **G2 PASS (4.12e-05)** the committed U56 W/H126/N=20 triple, tape PINNED at 2026-09-15.
- **G3 PASS (1.70e-04)** the committed SPY OOS triple on U56's tape, PINNED.
  **THE VINTAGE, PUBLISHED NOT ABSORBED:** the same two gates on the UNPINNED file read
  **1.62e-03** and **2.89e-03** — idea 1163's nightly-rewrite defect, the exact reason this run
  truncates every tape at the vintage 1148/1157's committed anchors saw.
- **G4 PASS (4.95e-05)** live RULES v2 MaxDD == the committed -12.05%.
- **G5 PASS (7.17e-06)** 1157's committed full-tape MaxDD LEVELS on all three panels.
- **G6 PASS (1.50e-07) — the one the whole run rests on.** 1148/1157's **SMALL / MAXDD /
  R_MATCHED / F_1140 replayed BIT FOR BIT: 0.794259 against the committed 0.794259**, using
  1157's `ratio_from` verbatim, its `matched_sampled` Monte-Carlo statistic, its seed and its
  loop order. All panels: U56 1.1775x, B136 1.3056x, SMALL 0.7943x, POOLED 1.7393x.
- **G7 PASS (1.89e-07)** R_ASIS at L3 with the EXACT all-pairs statistic reproduces that same
  0.794259 — the departure from the Monte-Carlo pair sample removes noise, not signal.
- **G8 PASS (0.00e+00)** R_FROZEN is EXACTLY ladder-invariant by construction. Proved, not
  asserted, because the whole comparability claim for that repair is definitional.
- **G9 PASS — 1157's premise REPRODUCED INDEPENDENTLY.** R_ASIS(L8)/R_ASIS(L3) is
  **U56 0.5615x, B136 0.5148x, SMALL 0.5916x**, against 1157's committed 0.39x-0.59x. The queue's
  starting fact is true on this run's own build.
- **G10 PASS (0.00e+00)** the whole 8,262-row sub-tape table is deterministic.

---

## (A) THE HEADLINE GRID — R_MATCHED ratio at C_POOLED / ALIGNED

Three rows of the 54 published (the headline statistic; the full 1,080-row grid is in
`.grid.csv` and the 54-row comparability table in `.comparability.csv`):

| panel | stat | repair | L2 | L3 | L4 | L6 | L8 | max/min | comparable |
|---|---|---|---|---|---|---|---|---|---|
| U56 | MAXDD | R_ASIS | 1.486 | 1.150 | 0.798 | 0.726 | 0.645 | 2.303 | . |
| U56 | MAXDD | R_FROZEN | 1.150 | 1.150 | 1.150 | 1.150 | 1.150 | 1.000 | Y |
| U56 | MAXDD | R_COUNT | 1.486 | 1.688 | 1.587 | 1.631 | 1.732 | 1.166 | Y |

| repair | comparable cells | median max/min | worst | at MAXDD (U56 / B136 / SMALL) |
|---|---|---|---|---|
| R_ASIS | 0 of 18 | 3.715 | 77.956 | 2.303x / 2.527x / 3.112x |
| R_FROZEN | 18 of 18 | 1.000 | 1.000 | 1.000x / 1.000x / 1.000x |
| R_COUNT | 2 of 18 | 2.083 | 17.246 | 1.166x (Y) / 1.178x (Y) / 1.447x |

**MAXDD is R_COUNT's best statistic and it is the record's headline one** — which is why the
2-of-18 must be quoted beside it and not instead of it.

---

## (B) THE PRICE OF FREEZING — leave-one-ladder-out jackknife

| repair / ladder | median SE(log r) | mean | worst |
|---|---|---|---|
| R_FROZEN @ L3 | 0.6723 | 0.8523 | 2.4419 |
| R_COUNT @ L8 | **0.1722** | 0.2906 | 0.8002 |
| R_ASIS @ L8 | 0.4621 | 0.6040 | 1.8761 |
| R_BOTH @ L3 (published, not a dial) | 0.5085 | 0.5667 | 1.5506 |

**R_COUNT@L8 / R_FROZEN@L3 = 0.2561.** Count-matching at the finest ladder is **3.9x better
resolved** than freezing at the record's ladder. This is the run's most useful number and it is
the one the queue's framing does not anticipate: *the ladder is not only a comparability dial, it
is a resolution dial, and freezing it spends resolution to buy comparability.*

### Does freezing land on the resolved value?

R_FROZEN@L3 vs R_COUNT@L8: **lands within 25% at 7 of 18 cells**, median relative gap **0.3221**.
At the headline statistic it misses at all three panels:

| stat | panel | frozen | resolved | gap | | R_BOTH | gap | |
|---|---|---|---|---|---|---|---|---|
| MAXDD | U56 | 1.1495x | 1.7322x | 0.3364 | MISSES | 1.6883x | 0.0253 | LANDS |
| MAXDD | B136 | 1.3199x | 1.8188x | 0.2743 | MISSES | 1.9799x | 0.0886 | LANDS |
| MAXDD | SMALL | 0.7943x | 1.1737x | 0.3233 | MISSES | 1.1914x | 0.0151 | LANDS |

**R_BOTH lands at 4 of 18 overall (median gap 0.3843), worse than R_FROZEN's 0.3221.** The three
MAXDD rows are its best three, not a representative sample, and are not quoted alone.
**1148's own committed SMALL/MAXDD headline of 0.794x is the frozen reading; the resolved one is
1.174x — the record's number is 32% low against its own finer ladder.**

---

## (C) THE CENSUS — the record's committed sub-tape rows

- **26 committed CSVs** in `research/backtests` carry a sub-tape FRACTION column, **42,170 rows**
  in total.
- **Only 4 of 26 (0.1538) also publish the LADDER they walked.** The rest publish a bare `frac`
  and leave the ladder to be inferred.
- **6 distinct committed ladder labels exist**: `1/1+1/2+1/3`, `1/1+1/2+1/3+1/4+1/6`,
  `1/1+1/2+1/3+1/4+1/5+1/6+1/8`, `F_1140`, `F_FINE`, `F_FINER`. The max fraction actually walked
  runs 0..8 across 21 files, median 1 — **the axis two runs disagree on, undeclared in 22 of 26
  files.**
- **PROSE: 66 committed sentences assert a regime-to-length reading; 0.1061 state a ladder and
  0.2576 quote a number.** Roughly one sentence in four quotes a figure that cannot be checked
  against another run's.

**THE DIRECT ANSWER TO "WHICH MAKES TWO RUNS COMPARABLE", ON THE TWO LADDERS THE RECORD ACTUALLY
WALKED (L3 is 1140/1148's, L8 is 1157's, both committed):**

| repair | median L3-vs-L8 disagreement | worst | within 1.25 |
|---|---|---|---|
| R_ASIS | 1.736x | 7.233x | 3 of 18 |
| R_FROZEN | 1.000x | 1.000x | 18 of 18 |
| R_COUNT | 1.559x | 12.675x | 4 of 18 |

**Only freezing makes two committed runs comparable, and it does so by refusing to read the
finer ladder at all.**

---

## RULE 8 WALK-FORWARD AND BOTH KEEP PATHS — 81 rung books, every one published

Benchmarks (pinned tape): **U56 SPY 15.10% / 0.8829 / -33.72% (halves 0.9588/0.8207), OOS
15.21% / 0.8711 / -33.72%; U56 RULES v2 (live) @10 bps 8.62% / 1.2008 / -12.05%, OOS 9.46% /
1.2763; B136 SPY 15.16% / 0.8861 / -33.72%, OOS 15.33% / 0.8767; B136 LIVE 7.98% / 1.0993 /
-12.24%, OOS 7.88% / 1.1059; SMALL SPY 14.06% / 0.8581 / -33.72%, OOS 15.33% / 0.8767; SMALL
LIVE 4.30% / 0.6637 / -13.89%, OOS 3.75% / 0.5600 / -13.89%.**

Base rates at 10 bps: **4b full 16 of 81 rung books, 4b OOS 17, BOTH 15, 4a 0 of 81** —
U56 10/27, B136 6/27, **SMALL 0 of 27 on every path**. The anchor book is a rung of all four
ladders, so the 81 rung books are **78 distinct books**; every duplicate is published and none is
double-counted.

**NO NEW CANDIDATE, AND THE REASON IS ARITHMETIC.** Eleven of the sixteen 4b passers are the
standing incumbent (U56 N=20/H=126/W) read at a *lower gross rung*, and their Sharpe runs
**1.1389 / 1.1391 / 1.1392 / 1.1394 / 1.1396 / 1.1397 across gross 0.50 -> 0.75** — a spread of
8e-04 over a 1.5x change in gross. **That is idea 1177's degenerate Sharpe-vs-gross ladder
arriving from a third direction, and it is a cross-run confirmation, not a discovery.** The rest
are prior art: U56 N=12, B136 N=15, B136 N=10. The one cell that is not obviously committed is
**U56 CADENCE=Q (15.40% / 1.1389 / -19.94%, OOS 17.28% / 1.1727)** — it is **dominated by the
incumbent on the full sample on every axis** (lower CAGR, lower Sharpe, deeper drawdown) and is
ahead only out of sample. **Preferring it would be selecting on the OOS window, which rule 8
exists to forbid, so it is recorded and not promoted. No memo.**

Choosers (each run under every repair, so a pick that moves is a pick the repair moved):

| panel | repair | chooser | pick | IS S | OOS S | SPY OOS S | >SPY | 4b | 4b OOS | 4a |
|---|---|---|---|---|---|---|---|---|---|---|
| U56 | R_ASIS | CH_ISSHARPE | N=40 | 1.1762 | 1.0985 | 0.8711 | Y | . | . | . |
| U56 | R_ASIS | CH_LOWRATIO | N=10 | 1.1406 | 1.0954 | 0.8711 | Y | . | . | . |
| U56 | R_ASIS | CH_HIGHRATIO | H=21 | 1.1218 | 1.1167 | 0.8711 | Y | . | . | . |
| U56 | R_FROZEN | CH_LOWRATIO | H=252 | 1.1315 | 1.1932 | 0.8711 | Y | . | . | . |
| U56 | R_FROZEN | CH_HIGHRATIO | CADENCE=W | 1.1119 | 1.1644 | 0.8711 | Y | **Y** | **Y** | . |
| U56 | R_COUNT | CH_LOWRATIO | N=10 | 1.1406 | 1.0954 | 0.8711 | Y | . | . | . |
| B136 | R_ASIS | CH_ISSHARPE | N=8 | 1.2951 | 0.7866 | 0.8767 | . | . | . | . |
| B136 | R_ASIS | CH_HIGHRATIO | N=40 | 1.1451 | 1.0535 | 0.8767 | Y | . | . | . |
| B136 | R_FROZEN | CH_HIGHRATIO | H=21 | 1.2112 | 0.9966 | 0.8767 | Y | . | . | . |
| SMALL | R_ASIS | CH_ISSHARPE | H=252 | 0.9833 | 0.6676 | 0.8767 | . | . | . | . |
| SMALL | R_FROZEN | CH_LOWRATIO | CADENCE=D | 0.6294 | 0.3633 | 0.8767 | . | . | . | . |
| SMALL | R_COUNT | CH_LOWRATIO | N=25 | 0.7421 | 0.4164 | 0.8767 | . | . | . | . |

(all 27 picks in `.picks.csv`)

**THE FREE PARAMETER HAS CAPITAL REACH AND NO CAPITAL VALUE.** The repair **moves the pick at 5
of 6 (panel, ratio-chooser) cells** — so a run that acts on a regime-to-length reading is acting
on a number whose undeclared ladder convention changes what it buys. But **0 of 27 picks clear 4a
and exactly 1 of 27 clears 4b**, and that one is
**U56 / R_FROZEN / CH_HIGHRATIO -> CADENCE=W, which is the standing incumbent** — reached by the
*falsification control* under the repair that discards data. **The ratio does not select; it only
disagrees with itself.** CH_LOWRATIO, the reading the record's language implies a run should
prefer, loses to CH_ISSHARPE on OOS Sharpe at B136 and SMALL under every repair.

---

## SURVIVORSHIP (PROTOCOL rule 9)

U56 and B136 are **current-constituent** lists; SMALL is the current output of a sub-$2B screen
less the documented `max_1d_move >= 1.0` exclusion (**52 of 715 tickers dropped; pool served =
663 names + SPY as benchmark**). Every LEVEL is optimistic and every 4a/4b count is an **upper**
bound. A RATIO of two spreads in the statistic's own units is far less exposed — but it is **not
immune**, because a survivorship-flattered panel has a shallower drawdown path and MAXDD is this
family's headline statistic, so the levels are published beside every ratio in `.books.csv`.

---

## VERDICT

**KILL as a capital finding.** Nothing enacted, no memo, no RULES or PROTOCOL edit (rule 6).
A PROTOCOL clause is **PROPOSED NOT ENACTED**:

> *"no sub-tape ratio without its fraction ladder" — any committed sentence quoting a
> regime-to-length, within-to-between or sub-tape spread ratio SHALL name the fraction ladder it
> was computed on and state whether its between term is an endpoint range or a count-matched
> pairwise mean. A ratio quoted without both is not comparable to any other run's."*

The census says why: **22 of 26 committed CSVs and 59 of 66 committed sentences do not name the
ladder, and on the two ladders the record actually walked the as-committed ratio disagrees with
itself by a median 1.736x and up to 7.233x.**

**Follow-ups filed: 1187** (does a sub-tape ratio need a statistic class before a clause can be
written — the combined repair lands at MAXDD and fails on ratio-valued statistics), **1188** (how
many committed sub-tape figures move once the ladder is resolved rather than frozen — 1148's own
headline moves 32%) and **1189** (is the gross-rung degeneracy of Sharpe universal — 11 of this
run's 16 4b passers are one book re-read at a lower gross).

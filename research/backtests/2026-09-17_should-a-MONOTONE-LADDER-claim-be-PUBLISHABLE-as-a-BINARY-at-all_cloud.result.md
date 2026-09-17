# Idea 1173 — should a MONOTONE-LADDER claim be PUBLISHABLE as a BINARY at all?

**Lane cloud, 2026-09-17, idea 1 of 2.** Script
`research/backtests/2026-09-17_should-a-MONOTONE-LADDER-claim-be-PUBLISHABLE-as-a-BINARY-at-all_cloud.py`,
8 CSVs, console log. No RULES change, no book promoted, no PROTOCOL edit (rule 6); RULES.md,
PROTOCOL.md, engine.py, scan.py, bot.py and baseline.py untouched.

**SELECTION:** this lane takes the FIRST eligible open idea. 1173 was first in `## Open` once the
two stale entries above it (1177 and 1172, both already in `## Done`) were skipped, and it is not
EDGAR / Form 4 / 8-K / options / spin-off / live-data.

---

## ANSWER = NO, AND THE NUMBER IS 28.4%

**A published "this ladder is monotone" reproduces on its own tape 28.4% of the time** (mean over
the 6 ladders where the binary fires; min 10.4%, max 60.0%). The binary's *headline* bootstrap
stability of 0.8958 is a 78/84-weighted average of two completely different numbers — 0.9428 for
the 78 ladders where the verdict is NO and **0.2840** for the 6 where it is YES — so a run that
quotes "the binary is stable" is quoting the stability of a verdict that is almost always NO.

Scored against the four outcomes declared before any number was read, the answer is
**(C) BINARY IS CONSERVATIVE ONLY**: 0.9364 of all 102 ladder-level reversals are UNDER-READ.
The binary essentially never claims order that is not there (0 OVER-READ of 84 on G_DOWNSHARE and
G_SPEARMAN, 1 on G_ENDSE), and it misses decisively-ordered ladders 36 to 48 times out of 84.

It is **not** (B): no graded statistic beats the binary by 0.20 on *both* stability and
replication, because the graded statistics buy their replication with lower stability
(G_SPEARMAN 0.6429 replication at 0.6947 stability against the binary's 0.0714 at 0.8958). The
pre-declared bar is scored as declared and is **not** re-cut after the fact.

---

## THE TWO DIALS AND NO MORE (PROTOCOL rule 4, and the queue names both)

`CLAIM SET` {NARROW, PROX, WIDE} x `GRADED STATISTIC` {G_DOWNSHARE, G_DECSTEPS, G_SPEARMAN,
G_ENDSE} = **12 cells, EVERY ONE PUBLISHED** in `.grid.csv`.

NOT dials, reported at every value: PANEL {U56, B136, SMALL}; the n-ladder
{5,8,10,12,15,20,25,30,40} (9 rungs = 1093's 8 adjacent steps); the HOLD ladder
{21,42,52,63,76,90,126} (1093's); the LADDER METRIC {SHARPE, CAGR, MAXDD, ULCER}; the block
bootstrap (63-day blocks x 500 reps) and the permutation null (2,000 draws); the three rule-8
choosers. Frozen at 936/1082/1086/1093's construction: CAND20 legs, cap INF, max_vol 0.60,
gross 0.75, W cadence, 10 bps, LAG 1, WARMUP 260.

**SCOPE, DECLARED NOT GLOSSED.** 1093's own object was the **EDGE** ladder (book CAGR minus a
DD-matched null's median over 40 seeds), which costs roughly 86k rebuilt paths per panel and is
**not** rebuilt here. The 84 ladders measured are METRIC ladders of the same shape, and every
re-score of a committed claim is labelled **TRANSFERRED** throughout. Only 0.0642 of NARROW
claims mention EDGE at all, so the metric family is the record's majority object — but this is
not a re-derivation of 1093's cell and is never described as one.

---

## GATES — 8 of 10 PASS, and the two failures are published failing, not absorbed

- **G1 PASS** fast runner == `engine.backtest` on U56 W/H126/N=20 at gross 0.75, dev **1.39e-17**.
- **G2 FAIL (1.62e-03)** the committed U56 W/H126/N=20 triple *as 936/1082/1093 published it*
  (0.155787 / 1.139701 / -0.191276).
- **G2b PASS (3.82e-07)** the **same cell as 1151/1171/1172 published it today**
  (0.155520 / 1.138079 / -0.191276). This run reads 0.155520 / 1.138079 / -0.191276.
  **THE VINTAGE, PUBLISHED NOT ABSORBED:** `data/prices.csv` is rewritten nightly (idea 1163's
  defect); the two committed vintages of one cell are 1.6e-03 of CAGR apart and this run
  reproduces the current one bit for bit. Nothing in the answer depends on the level.
- **G3 FAIL (2.89e-03)** the committed SPY OOS triple on U56's tape — the same vintage drift,
  the same size as 1149's G3 (2.89e-03) reported it.
- **G4 PASS** `build()` deterministic, 0.00e+00.
- **G5 PASS (1.81e-04)** the permutation machinery is correct: at a **fixed** direction the
  down-share null centres on 0.500.
- **G5b REPORTED NOT GATED — and it is a finding, not a nuisance.** The null every graded
  statistic here actually uses is **self-oriented** (each ladder scored in its own end-to-end
  direction, as the record's claims are), and it centres on **0.5420 +/- 0.0005, not on 0.500**.
  Orienting by the endpoints conditions on them and buys 0.0420 of down-share for free. **A
  record sentence reading "k of 8 steps down, against the 4 of 8 you would get by chance" is
  scored against the wrong null by that margin: at 9 rungs the honest chance level is 4.34
  steps, not 4.**
- **G6 PASS** the permutation null of M_STRICT sits at the exact **2/9! = 5.51e-06**. A strict
  ladder is a 1-in-181,440 ordering, not a 1-in-2 one — which is *why* the binary almost never
  fires and why its stability conditional on firing is the only number worth quoting.
- **G7 PASS** the moving-block bootstrap is unbiased for the mean (0.114 SE of the tape mean).
- **G8 PASS** the three claim sets NEST: NARROW subset of PROX subset of WIDE.

---

## (A) REPLICATION ACROSS HOLDS AND BOOTSTRAP STABILITY — the 84 ladders

Cells read *decisive holds / 7 @ mean bootstrap stability*.

| panel | metric | BINARY | stab | DOWNSHARE | DECSTEPS | SPEARMAN | ENDSE |
|---|---|---|---|---|---|---|---|
| U56 | SHARPE | 0 of 7 | 0.988 | 1/7@0.65 | 0/7@0.82 | 2/7@0.62 | 0/7@0.78 |
| U56 | CAGR | 2 of 7 | 0.739 | 7/7@0.78 | 0/7@0.83 | 7/7@0.85 | 4/7@0.65 |
| U56 | MAXDD | 0 of 7 | 0.955 | 3/7@0.58 | 0/7@0.80 | 3/7@0.58 | 0/7@0.53 |
| U56 | ULCER | 2 of 7 | 0.699 | 5/7@0.64 | 0/7@0.91 | 7/7@0.88 | 5/7@0.58 |
| B136 | SHARPE | 0 of 7 | 0.989 | 3/7@0.61 | 0/7@0.70 | 4/7@0.62 | 0/7@0.85 |
| B136 | CAGR | 1 of 7 | 0.872 | 7/7@0.77 | 0/7@0.83 | 7/7@0.85 | 5/7@0.76 |
| B136 | MAXDD | 0 of 7 | 0.942 | 0/7@0.60 | 2/7@0.71 | 0/7@0.43 | 0/7@0.65 |
| B136 | ULCER | 0 of 7 | 0.834 | 7/7@0.73 | 0/7@0.87 | 7/7@0.83 | 5/7@0.55 |
| SMALL | SHARPE | 0 of 7 | 0.986 | 0/7@0.68 | 0/7@0.74 | 4/7@0.57 | 0/7@0.71 |
| SMALL | CAGR | 0 of 7 | 0.993 | 0/7@0.75 | 0/7@0.78 | 0/7@0.60 | 0/7@0.86 |
| SMALL | MAXDD | 0 of 7 | 0.949 | 4/7@0.60 | 0/7@0.87 | 6/7@0.71 | 2/7@0.49 |
| SMALL | ULCER | 1 of 7 | 0.804 | 5/7@0.61 | 0/7@0.90 | 7/7@0.80 | 1/7@0.54 |

**1093's structural finding replicates on a different family:** the binary fires at **0, 1 or 2
of 7 holds** in every one of the 12 (panel, metric) families, and never at the same hold on two
panels. The graded readings replicate at **7 of 7** in four families (U56/CAGR, U56/ULCER,
B136/CAGR, B136/ULCER on G_SPEARMAN) and at 0 of 7 in others — so "the graded reading always
replicates" is **not** general either, and this run does not repeat that claim.

**A CORRECTION, AND IT IS THIS RUN'S OWN GRADED STATISTIC THAT DIES.** 1093 read "4-7 of 8
decisively-down steps at every hold". On the metric ladders with a 63-day block bootstrap,
**G_DECSTEPS is decisive at 2 of 84 ladders** — the per-step SE on this construction is so wide
that almost no individual step clears 2 SE. The step-decisiveness reading is the one graded
statistic that does *not* transfer off the EDGE family, and it is published failing.

---

## (B) THE CENSUS — 1,417 committed monotonicity sentences across 353 files

| claim set | claims | states a NULL | states a RUNG SET | GRADED phrasing | negated | names PANEL | names METRIC | names HOLD | about EDGE |
|---|---|---|---|---|---|---|---|---|---|
| NARROW | 187 | 0.0909 | 0.3102 | 0.3690 | 0.2406 | 0.2941 | 0.2674 | 0.1551 | 0.0642 |
| PROX | 412 | 0.0534 | 0.2621 | 0.2524 | 0.2354 | 0.1796 | 0.2209 | 0.0704 | 0.0364 |
| WIDE | 1,417 | 0.0381 | 0.1574 | 0.1750 | 0.1983 | 0.1299 | 0.2082 | 0.0268 | 0.0183 |

**The queue's premise about the record holds and is worse than it sounds: only 0.0909 of the
record's most careful monotonicity claims state a null at all, and only 0.3690 use graded
phrasing. Three claims in four are published as a bare binary with nothing to check them
against.** Only 0.1551 of NARROW claims name the hold they were measured at, which is why the
PINNED arm below has a population of 2.

---

## (C) THE 12-CELL GRID — how many committed claims REVERSE

TRANSFERRED = the claim names a panel and a metric, scored against the majority of the 7 holds.
PINNED = the claim also names one of the 7 holds, scored against that hold alone.

| claim set | graded | claims | resolvable | agree | reverse | rev share | under | over | pinned | p_rev | p share |
|---|---|---|---|---|---|---|---|---|---|---|---|
| NARROW | G_DOWNSHARE | 187 | 15 | 3 | 12 | 0.8000 | 2 | 10 | 2 | 2 | 1.0000 |
| NARROW | G_DECSTEPS | 187 | 15 | 3 | 12 | 0.8000 | 0 | 12 | 2 | 2 | 1.0000 |
| NARROW | G_SPEARMAN | 187 | 15 | 6 | 9 | 0.6000 | 2 | 7 | 2 | 2 | 1.0000 |
| NARROW | G_ENDSE | 187 | 15 | 3 | 12 | 0.8000 | 2 | 10 | 2 | 2 | 1.0000 |
| PROX | G_DOWNSHARE | 412 | 21 | 5 | 16 | 0.7619 | 2 | 14 | 2 | 2 | 1.0000 |
| PROX | G_DECSTEPS | 412 | 21 | 4 | 17 | 0.8095 | 0 | 17 | 2 | 2 | 1.0000 |
| PROX | G_SPEARMAN | 412 | 21 | 10 | 11 | 0.5238 | 2 | 9 | 2 | 2 | 1.0000 |
| PROX | G_ENDSE | 412 | 21 | 5 | 16 | 0.7619 | 2 | 14 | 2 | 2 | 1.0000 |
| WIDE | G_DOWNSHARE | 1,417 | 50 | 15 | 35 | 0.7000 | 3 | 32 | 2 | 2 | 1.0000 |
| WIDE | G_DECSTEPS | 1,417 | 50 | 11 | 39 | 0.7800 | 0 | 39 | 2 | 2 | 1.0000 |
| WIDE | G_SPEARMAN | 1,417 | 50 | 23 | 27 | 0.5400 | 3 | 24 | 2 | 2 | 1.0000 |
| WIDE | G_ENDSE | 1,417 | 50 | 15 | 35 | 0.7000 | 3 | 32 | 2 | 2 | 1.0000 |

**How many reverse: 0.5238 to 0.8095 of the transferred claims, at every claim set and every
graded statistic.** The dial that moves the answer is the **graded statistic**, not the claim
set: G_SPEARMAN reverses about half and G_DECSTEPS about four-fifths, at every claim set, while
NARROW -> WIDE moves the share by at most 0.10. **A run that re-scores the record's monotonicity
claims and does not name which graded statistic it used has published a number with a 0.29-wide
free parameter in it.**

**The reversals run the OTHER way from the ladder-level ones and the run says so.** At claim
level the reversals are mostly OVER-READ (the claim asserts order the graded reading does not
find), because 0.8017 of committed claims assert monotonicity while only 6 of 84 measured
ladders are binary-monotone. At ladder level they are 0.9364 UNDER-READ. **Both are true and
they are different objects: the record's claims are selected (a run publishes the ladder it
found ordered), and the 84 measured ladders are a census.** Neither number is quoted as the
other.

**The PINNED arm is 2 claims and reverses 2 of 2. That is a direction, not a measurement, and it
is published as such.**

---

## (D) LADDER-LEVEL REVERSALS — the 84 measured ladders

| graded | agree | UNDER-READ | OVER-READ | under share of reversals |
|---|---|---|---|---|
| G_DOWNSHARE | 48 / 84 | 36 | 0 | 1.0000 |
| G_DECSTEPS | 76 / 84 | 2 | 6 | 0.2500 |
| G_SPEARMAN | 36 / 84 | 48 | 0 | 1.0000 |
| G_ENDSE | 66 / 84 | 17 | 1 | 0.9444 |

**G_DECSTEPS is the exception and it is the informative one: all 6 of the binary-monotone
ladders fail its bar.** Every ladder the record would publish as "monotone" has at least one
step that does not clear 2 SE — i.e. the binary fires on ladders whose individual steps are
individually indistinguishable from zero.

---

## RULE 8 WALK-FORWARD AND BOTH KEEP PATHS — 189 books, every one published

Benchmarks: **U56 SPY 15.06% / 0.8814 / -33.72% (halves 0.9598/0.8170), OOS 15.15% / 0.8684 /
-33.72%; U56 RULES v2 (live) @10 bps 8.60% / 1.1980 / -12.05%, OOS 9.42% / 1.2714 / -12.05%;
B136 SPY 15.16% / 0.8861 / -33.72%, OOS 15.33% / 0.8767; B136 LIVE 7.98% / 1.0993 / -12.24%,
OOS 7.88% / 1.1059; SMALL SPY 14.06% / 0.8581 / -33.72%, OOS 15.33% / 0.8767; SMALL LIVE
4.30% / 0.6637 / -13.89%, OOS 3.75% / 0.5600 / -13.89%.**

Base rates at 10 bps: **4b full 9 of 189, 4b OOS 10, BOTH 9, 4a 0 of 189.** By panel: U56 8/63,
B136 1/63, **SMALL 0 of 63 on every path**.

**AN INDEPENDENT CROSS-RUN REPLICATION, AND IT IS EXACT.** All 9 books clearing 4b full+OOS here
are **the same 9 cells lane C's idea-1093 run published today, agreeing to 6 decimals** (U56
N=10/12/15/30/40 at H=21, N=40 at H=52, N=12 and N=20 at H=126, B136 N=15 at H=126; e.g. U56
N=20/H=126 0.155520 / 1.138079 / -0.191276 in both). **NO NEW CANDIDATE — every passing book is
prior art from the same day, so this arm is CONFIRMATORY, not generative, and no memo is
written.**

Choosers (all choose on 2009-2016 only and read 2017-2026 once; `fb` = fell back because no hold
qualified):

| panel | chooser | N | H | fb | IS S | OOS S | SPY OOS S | >SPY | 4b | 4b OOS | 4a |
|---|---|---|---|---|---|---|---|---|---|---|---|
| U56 | CH_ISSHARPE | 15 | 90 | . | 1.3340 | 1.1033 | 0.8684 | Y | . | . | . |
| U56 | CH_MONO | 15 | 90 | Y | 1.3340 | 1.1033 | 0.8684 | Y | . | . | . |
| U56 | CH_GRADED:G_DOWNSHARE | 15 | 90 | Y | 1.3340 | 1.1033 | 0.8684 | Y | . | . | . |
| U56 | CH_GRADED:G_DECSTEPS | 5 | 63 | . | 1.1967 | 0.8948 | 0.8684 | Y | . | . | . |
| U56 | CH_GRADED:G_SPEARMAN | 15 | 90 | Y | 1.3340 | 1.1033 | 0.8684 | Y | . | . | . |
| U56 | CH_GRADED:G_ENDSE | 15 | 90 | Y | 1.3340 | 1.1033 | 0.8684 | Y | . | . | . |
| B136 | CH_ISSHARPE | 5 | 63 | . | 1.4241 | 0.9156 | 0.8767 | Y | . | . | . |
| B136 | CH_MONO | 5 | 63 | . | 1.4241 | 0.9156 | 0.8767 | Y | . | . | . |
| B136 | CH_GRADED:G_DOWNSHARE | 5 | 63 | . | 1.4241 | 0.9156 | 0.8767 | Y | . | . | . |
| B136 | CH_GRADED:G_DECSTEPS | 30 | 90 | . | 1.2420 | 0.9106 | 0.8767 | Y | . | . | . |
| B136 | CH_GRADED:G_SPEARMAN | 5 | 63 | . | 1.4241 | 0.9156 | 0.8767 | Y | . | . | . |
| B136 | CH_GRADED:G_ENDSE | 5 | 63 | Y | 1.4241 | 0.9156 | 0.8767 | Y | . | . | . |
| SMALL | CH_ISSHARPE | 8 | 42 | . | 0.9880 | 0.5385 | 0.8767 | . | . | . | . |
| SMALL | CH_MONO | 8 | 42 | Y | 0.9880 | 0.5385 | 0.8767 | . | . | . | . |
| SMALL | CH_GRADED:G_DOWNSHARE | 25 | 63 | . | 0.8278 | 0.5043 | 0.8767 | . | . | . | . |
| SMALL | CH_GRADED:G_DECSTEPS | 8 | 42 | Y | 0.9880 | 0.5385 | 0.8767 | . | . | . | . |
| SMALL | CH_GRADED:G_SPEARMAN | 25 | 63 | . | 0.8278 | 0.5043 | 0.8767 | . | . | . | . |
| SMALL | CH_GRADED:G_ENDSE | 15 | 52 | . | 0.7794 | 0.6502 | 0.8767 | . | . | . | . |

**THE SHAPE READING HAS NO CAPITAL CONTENT, AND THE BINARY HAS THE LEAST OF ALL.**
`CH_MONO` **fell back to CH_ISSHARPE at 2 of 3 panels** — on U56 and SMALL no hold's IS n-ladder
is binary monotone, so the binary filter is simply *undefined* as a selection rule — and on B136,
where exactly one hold qualifies (H=63), it picks the identical book CH_ISSHARPE already picked.
**Filtering on a binary changes 0 of 3 picks.** The graded filters do change picks, and every
change is a **loss**: CH_GRADED:G_DECSTEPS costs U56 0.2085 of OOS Sharpe (1.1033 -> 0.8948) and
B136 0.0050, and CH_GRADED:G_DOWNSHARE/G_SPEARMAN cost SMALL 0.0342. **0 of 18 picks clear 4b,
0 of 18 clear 4a, and 0 of 189 books clear 4a at all.**

---

## SURVIVORSHIP (PROTOCOL rule 9)

U56 and B136 are **current-constituent** lists; SMALL is the current output of a sub-$2B screen
less the documented `max_1d_move >= 1.0` exclusion (52 of 715 tickers dropped; pool served =
663 names + SPY as benchmark). Every LEVEL — CAGR, Sharpe, MaxDD — is optimistic and every 4a
and 4b count is an **upper** bound. It very largely cancels out of a SHAPE statistic, which
ranks one construction against itself on one tape, but that cancellation is an argument and not
a measurement, and the levels are published beside every shape in `.ladders.csv` and
`.books.csv` so a reader can check.

---

## VERDICT

**KILL as a capital finding.** Nothing enacted, no memo, no RULES or PROTOCOL edit (rule 6).
The transferable result is procedural and it is worth one line in a future run's header:
**a monotone-ladder claim should not be published as a binary — the binary reproduces 28.4% of
the time when it fires, its own null is a 1-in-181,440 ordering rather than a coin flip, and the
"k of 8 steps" null a reader would assume is 4.34 of 8 and not 4 of 8.**

**Follow-ups filed: 1184, 1185, 1186 (filed as 1181-1183; renumbered on push — lane collision, defect 932 again, the concurrent lane had already taken 1181-1183 from idea 1174).**

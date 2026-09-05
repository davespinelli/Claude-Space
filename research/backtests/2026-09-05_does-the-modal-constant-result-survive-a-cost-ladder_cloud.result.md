# Idea 217 — does-the-modal-constant-result-survive-a-cost-ladder (cloud, 2026-09-05)

**ANSWERED: YES on the result, NO on the queue's reason. The modal constant's win survives
every rung — MODE-LOO beats SEL-SHARPE in 20 of 20 (corpus × live-dial × rung) cells from 5 to
25 bps — but the dial the queue nominated as cost-fragile, CADENCE, has the *most* cost-stable
mode in the set (M at all five rungs, on both corpora). The one mode that MOVES with cost is
N, the book-size dial, and it moves only at the last rung and onto a ladder ENDPOINT on one
corpus. No RULES change, no new book, no KEEP candidate.**

Script `2026-09-05_does-the-modal-constant-result-survive-a-cost-ladder_cloud.py`; artefacts
`.console.txt`, `.ladder.csv` (30 240 rows), `.modes.csv`, `.paired.csv`, `.walkforward.csv`,
`.keep.csv`, `.refs.csv`. 173 s.

## Design and reproduction

Idea 171's script imported verbatim (`Book`, `build_corpus`, `fast_backtest`, `rel_margin`,
`keep_4a`, `keep_4b`, the five dials and their ladders); idea 189's `build_corpus_B` imported
for corpus B. 5 dials × 36 ladder points × 168 books × 5 cost rungs = **30 240 rung-rows**,
t+1, IS ≤ 2016-12-31, OOS ≥ 2017-01-01 read once.

**The cost ladder is derived, not re-simulated.** In `fast_backtest` the cost term is additive
and never feeds back into the holdings, so `net(c) = gross − turnover·c/1e4` **exactly**. Each
ladder point is simulated once at 0 bps and the five rungs are subtractions. Control **[d]**
asserts this against a direct `fast_backtest(cost=c)` re-simulation over 3 books × 5 configs ×
5 rungs: **max |direct − derived| = 0.000e+00**. This makes the rung-to-rung differences
perfectly paired and noise-free — which is the point, and also means a rung comparison is not
an independent replication.

Asserted before any new number: `fast_backtest` == `engine.backtest` at D/W/M/Q (max |dret|
6.2e-17); CAND-20 weights == idea 78's `weights_cand` at 0.000e+00 on three books; the numpy
metric kernels == `engine.metrics` / idea 171's `halves` / `rel_margin` at **0.000e+00**; and
**the derived 10 bps rung matches idea 171's committed `ladder.csv` on all 1908 rows at
3.6e-15 with 0 4a/4b verdict mismatches**, with idea 189's 10-cell mode/share table
reproduced exactly.

## Q3 — the mode at every rung (modal SEL-SHARPE pick / its share)

| corpus | dial | 5 bps | 10 bps | 15 bps | 20 bps | 25 bps | moves? |
|---|---|---|---|---|---|---|---|
| A | GROSS | 1.00 94.3% | 1.00 94.3% | 1.00 94.3% | 1.00 94.3% | 1.00 94.3% | stable |
| A | **N** | 20 20.8% | 20 22.6% | 20 20.8% | 20 22.6% | **50 24.5%** | **MOVES 20 → 50** |
| A | BAND | 0.08 75.5% | 0.08 81.1% | 0.08 84.9% | 0.08 86.8% | 0.08 88.7% | stable |
| A | CADENCE | M 73.6% | M 83.0% | M 86.8% | M 86.8% | M 81.1% | stable |
| A | SLEEVE | 0.30 100% | 0.30 100% | 0.30 100% | 0.30 100% | 0.30 100% | stable |
| B | GROSS | 1.00 84.3% | 1.00 84.3% | 1.00 84.3% | 1.00 84.3% | 1.00 83.5% | stable |
| B | **N** | 15 25.2% | 15 23.5% | 15 24.3% | 15 20.0% | **25 19.1%** | **MOVES 15 → 25** |
| B | BAND | 0.08 67.0% | 0.08 68.7% | 0.08 70.4% | 0.08 71.3% | 0.08 73.0% | stable |
| B | CADENCE | M 88.7% | M 88.7% | M 87.8% | M 86.1% | M 87.0% | stable |
| B | SLEEVE | 0.30 87.8% | 0.30 87.8% | 0.30 89.6% | 0.30 89.6% | 0.30 90.4% | stable |

**The queue's premise is refuted on its own terms.** Both nominated dials really are turnover
dials — over corpus A at 10 bps, CADENCE spans 18.71 → 2.08 turns/yr (D → Q, 9.0×) and N spans
19.68 → 3.75 (n=3 → n=50, 5.2×). But cost does not move the CADENCE mode at all: monthly is
the modal IS pick at every rung on both corpora, and its share *rises* from 73.6% to 86.8%
(A) between 5 and 20 bps. What cost moves is **N**, and only at the last rung, toward a
**larger book** (lower turnover per name) — 20→50 on A, 15→25 on B. On corpus A that
destination is the **ladder endpoint**, i.e. idea 218's truncation artefact reappearing as
soon as the cost rung is raised; on corpus B it is interior.

N's modal share never exceeds 25.2% at any rung on either corpus. It was never a writable
mode at 10 bps (idea 189) and cost does not make it one.

## Q4 — MODE-LOO minus SEL-SHARPE, every rung (positive = the constant beats the fit)

OOS Sharpe, paired over books:

| corpus | dial | 5 bps | 10 bps | 15 bps | 20 bps | 25 bps |
|---|---|---|---|---|---|---|
| A | GROSS | −0.0001 | −0.0001 | −0.0000 | −0.0000 | −0.0000 |
| A | **N** | **+0.0274** (t +1.95) | +0.0215 | +0.0126 | +0.0002 | **+0.0499** (t +3.17) |
| A | BAND | −0.0013 | +0.0005 | +0.0003 | +0.0027 | +0.0022 |
| A | **CADENCE** | **+0.0314** (t +3.30) | +0.0261 | +0.0223 | +0.0234 | **+0.0308** (t +3.23) |
| A | SLEEVE | +0.0000 | +0.0000 | +0.0000 | +0.0000 | +0.0000 |
| B | GROSS | −0.0001 | −0.0000 | −0.0000 | −0.0000 | −0.0000 |
| B | **N** | **+0.0344** (t +3.36) | +0.0256 | +0.0168 | +0.0112 | +0.0123 |
| B | BAND | +0.0050 | +0.0078 | +0.0089 | **+0.0108** (t +2.82) | **+0.0108** (t +2.85) |
| B | **CADENCE** | +0.0209 | +0.0255 | +0.0276 | **+0.0292** (t +3.25) | +0.0279 |
| B | SLEEVE | +0.0030 | +0.0030 | +0.0031 | +0.0028 | +0.0022 |

**The headline: on the two dials where the pick distribution is genuinely spread (N, CADENCE),
MODE-LOO's mean difference is positive in 20 of 20 corpus × dial × rung cells.** Fitting's best
case anywhere in the 5-rung grid is **−0.0001 OOS Sharpe on GROSS** — a dial whose whole OOS
spread is 0.002. The constant's best case is **+0.0499** (N, corpus A, 25 bps).

The full 3 mode-definitions × 2 scores × 5 rungs × 2 corpora × 5 dials = 300-point grid is in
`.paired.csv`; the dials-won summary is flat in the mode definition (MODE-GLOBAL and MODE-LOO
give **identical** numbers at every rung — removing a book's own vote never changes the mode —
and MODE-XCORPUS differs by at most one dial). On the OOS 4b margin the counts are 2–5 of 5
depending on rung and corpus, again with the two live dials carrying it.

**Two cost-dependences that are real, and small.** (i) BAND, one of idea 189's three
"degenerate" dials, becomes a genuine (if tiny) dial at high cost on corpus B: the gap grows
monotonically +0.0050 → +0.0108 with t rising +1.28 → +2.85 as its modal share rises. This is
the one place P4 fails. (ii) The off-mode penalty on CADENCE grows with cost — corpus A
+0.1190 → +0.1633, corpus B +0.1852 → +0.2140 per off-mode book — but the *overall* gap does
not, because agreement rises at the same time (73.6% → 81.1% on A). The mechanism gets more
expensive; the selector makes the mistake less often. Those two cancel.

## Q5 — rule 8 at every rung

Pooled OOS Sharpe (mean over 5 dials × books; all arms chose on ≤ 2016-12-31 only):

| arm | A 5 | A 10 | A 15 | A 20 | A 25 | B 5 | B 10 | B 15 | B 20 | B 25 |
|---|---|---|---|---|---|---|---|---|---|---|
| CONST-INC | 1.0001 | 0.9638 | 0.9275 | 0.8912 | 0.8548 | 0.7117 | 0.6793 | 0.6470 | 0.6146 | 0.5822 |
| RANDOM | 1.0009 | 0.9634 | 0.9259 | 0.8883 | 0.8507 | 0.7180 | 0.6866 | 0.6552 | 0.6237 | 0.5923 |
| SEL-4B | 1.0125 | 0.9806 | 0.9503 | 0.9197 | 0.8892 | 0.7300 | 0.7044 | 0.6791 | 0.6508 | 0.6259 |
| SEL-SHARPE | 1.0386 | 1.0100 | 0.9820 | 0.9533 | 0.9285 | 0.7515 | 0.7251 | 0.6995 | 0.6734 | 0.6484 |
| **MODE-LOO** | **1.0501** | **1.0196** | **0.9891** | **0.9585** | **0.9451** | **0.7642** | **0.7375** | **0.7108** | **0.6842** | **0.6590** |
| ORACLE (n/a) | 1.0752 | 1.0438 | 1.0130 | 0.9825 | 0.9522 | 0.8000 | 0.7716 | 0.7439 | 0.7164 | 0.6892 |

**The ordering CONST < SEL-4B < SEL-SHARPE < MODE-LOO < ORACLE is identical at all five rungs
on both corpora — ten of ten.** MODE-LOO banks **66.6% (A) / 59.4% (B)** of the oracle gap at
5 bps and **92.7% / 71.8%** at 25 bps, against the fit's 51.3% / 45.1% and 75.6% / 61.8% —
i.e. the mode's advantage over the fit is not eroded by cost, it widens slightly. Cost
costs every arm about the same: −0.105 to −0.150 of OOS Sharpe from 5 to 25 bps, with
CONST-INC and RANDOM losing the most (−0.145 / −0.150 on A) and the fitted and modal arms the
least (−0.105) — i.e. the picked points are the cheaper ones, at every rung.

References on the OOS window: **SPY 15.45% / 0.8820 / −33.72%**; RULES v1 on U56 9.08%/0.8627
(5 bps) → 3.78%/0.3992 (25 bps); on B136 7.60%/0.7167 → 1.11%/0.1554; on the small panel
21.05%/0.6437 → 14.24%/0.4872 (corpus A's unfiltered SMALL484) and 9.49%/0.7788 →
3.18%/0.3101 (corpus B's filtered SMALL439).

## Both KEEP paths at every rung

| corpus | bps | rows | 4a | 4b | fixed rows | fixed 4a | fixed 4b |
|---|---|---|---|---|---|---|---|
| A | 5 | 1908 | 1215 | 396 | 180 | 51 | 55 |
| A | 10 | 1908 | 1507 | 250 | 180 | 74 | 36 |
| A | 25 | 1908 | 1745 | 47 | 180 | 101 | 14 |
| B | 5 | 4140 | 953 | 359 | 108 | 22 | 25 |
| B | 10 | 4140 | 1214 | 256 | 108 | 23 | 20 |
| B | 25 | 4140 | 1942 | 98 | 108 | 36 | 13 |

4b falls monotonically with cost (A 396 → 47, B 359 → 98) while 4a *rises* (1215 → 1745),
because 4a's comparator is RULES v1 re-costed at the same rung and RULES v1 is the higher-
turnover book. On the fixed panels, **every surviving 4b pass at 25 bps is U56** (13/36 rows;
B136 0/36, BSTK100 1/36, ETF36 0/36, SMALL484 and SMALL439 0/36 at every rung) — **idea 136's
small-panel null reproduces again — idea 218 counted its fourteenth — now at five cost
rungs**. P7 fails only
because it asserted zero fixed-panel passes at 25 bps; the 27 that survive are all U56 and
BSTK100 re-grossings of a book already in the record (idea 144), so nothing new is proposed.

Among implementable arm-chosen cells **SEL-4B has the most 4b passes at all ten corpus × rung
cells** (A 92/265 → 20/265; B 97/575 → 41/575) while sitting *below* SEL-SHARPE and MODE-LOO
on OOS Sharpe at every one of them — the 4b-margin selector buys 4b passes with OOS Sharpe,
exactly the trade idea 152 measured, and cost does not change the price. The other arms
reorder between rungs and corpora (on A at 5 bps CONST-INC's 70 beats MODE-LOO's 56; on B at
25 bps MODE-LOO's 30 beats CONST-INC's 20), so nothing but the SEL-4B result is stable there.

## Predictions

3 of 7 hit. **P1** (reproduction) and **P2** (additivity) hit exactly. **P5** hit: 20 of 20.
**P3** missed — I predicted the CADENCE mode would slow with cost; it does not move at all.
**P4** missed on BAND alone (max |gap| 0.0108 > 0.01). **P6** missed: the CADENCE gap is
*flat* in cost on corpus A (+0.0314 → +0.0308) and rises only on B. **P7** missed on the
fixed-panel clause (27 U56/BSTK100 passes at 25 bps, all re-grossings).

## What this is worth

The clause idea 189 wanted to write — *read the dial's mode once and write it down; do not fit
it per book* — is **cost-robust over 5 to 25 bps** and does not need a cost qualifier. What it
does need is the qualifier idea 219 is already asking for: the clause is only writable where
the mode is concentrated. This run adds that **concentration itself is cost-stable on CADENCE
(74–89%) and cost-unstable on N (19–25%, and the modal value migrates at 25 bps)**, so the
floor idea 219 seeks should be measured on the mode's *share*, not on cost.

Nothing here is tradable. No RULES change, no new book, no KEEP candidate, and nothing in
RULES.md, scan.py, bot.py or baseline.py touched.

## Caveats (also in the script docstring)

SURVIVORSHIP — B136, U56 and both small panels are current-constituent lists with no
delistings; every arm inherits it equally so the paired comparison is unaffected, but every
LEVEL is biased upward and none is a tradable estimate. Corpus A's SMALL484 is inherited from
idea 171 *without* the `max_1d_move ≥ 1.0` filter (control [c] requires byte-level
reproduction); corpus B's SMALL439 applies it (44 names dropped). The books are not
independent (48/53 and 112/115 are sub-panels of one parent each), so every paired t is over
correlated units and the exact sign test sits beside it. The five rungs share one simulation
per ladder point, so they are perfectly paired and carry no simulation noise — but they are
therefore not five independent replications. Costs are a flat linear bps charge on turnover;
real cost is spread plus impact and scales with name liquidity, so 25 bps on a 439-name
sub-$2B panel is not the same instrument as 25 bps on U56.

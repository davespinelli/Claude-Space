# Idea 880 — how many committed PLACEBO-DIFFERENCED numbers would CHANGE SIGN under the SIGNED estimator?

**Cloud, 2026-09-15. ANSWERED = THE QUESTION HAS A MUCH SMALLER DENOMINATOR THAN IT ASSUMES, AND
THE REPLACEMENT ESTIMATOR IS NOT SIGN-STABLE EITHER. Only **5 of idea 871's 70** committed
placebo-bearing files (**7.1%**) can be re-priced at all, and **8 of those 31 claims are
bit-identical copies of each other** — the record's placebo mass double-counts. On the 23
independent claims: **17.4% change resolvability verdict** between estimators (39.1% over all 151
cuts), but **30.4% have a SIGNED median and a SIGNED mean of opposite sign**, so the signed
estimator cannot be handed the record as a fix without a declared pooling rule.
H_UNADJ and H_WF CONFIRMED; H_ACQ, H_HIDE and H_STABLE REFUTED on their own bars.
KILL for capital — nothing here is a book. No PROTOCOL change is applied (rule 6); one is
PROPOSED. RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched.**

Script: `2026-09-15_how-many-committed-PLACEBO-DIFFERENCED-numbers-would-CHANGE-SIGN-under-the-SIGNED-estimator_cloud.py`
Outputs: `.corpus.csv` `.claims.csv` (151) `.headline.csv` (23) `.walkforward.csv` `.books.csv`
`.console.txt`

## The asymmetry the whole run turns on, stated before any count

**|x| ≥ 0 always. The absolute estimator has no zero of its own.** It can be adjudicated only
against an externally supplied floor — the seed-noise prediction
`median|gap| ≈ 0.6745·1.2533/√NSEED·√(sd_null² + sd_BLOCK²)` — which a run can compute only if it
committed its own per-arm seed dispersion. The signed estimator needs no floor: a sign test
against 50% is calibrated by construction.

So the queue's literal question cannot be asked of an ABS number, which has no sign to change. It
is asked here in the three answerable forms, all pre-registered: **Q1** how many claims *acquire*
a determinate sign; **Q2** whether the signed estimator is itself sign-stable; **Q3** how many
claims change resolvability verdict. Two tuned parameters, as the queue names them: **claim set**
(HEADLINE = one per file × null at 10 bps full sample / ALL = × 3 rungs × 2 windows) and
**estimator** (ABS_MED / ABS_MEAN / SIGNED_MED / SIGNED_MEAN, all four printed at every claim).

## 1. The corpus — discovered by structure, not by a hand-written list

A file is re-priceable iff it committed **per-arm** excess for a null *and* its BLOCK reference on
the same arm keys. Everything else is aggregate-only: the published number survives, the cells
under it do not, and no estimator can be recomputed from it.

| file | rows | seed sd committed? | nulls |
|---|---|---|---|
| 875 `…MIS-DISPERSED…_cloud.excess.csv` | 5,760 | **yes** | BLOCK RAND SM_DOM SM_UNIF SWITCHMATCH |
| CORR-LO `…DE-GROSSING-artefact_cloud.excess.csv` | 17,280 | no | BLOCK BLOCKPOST EPISODEFIX RAND YEARBLOCK |
| 881 `…MAX-RUN-LENGTH…_B.excess.csv` | 11,520 | **yes** | BLOCK BLOCK2 RAND SM_DOM/FILL/LONE/SPLIT2/4/8 SM_UNIF |
| 871 `…RUN-LENGTH-MATCHED-null-by-name_B.nulls.csv` | 13,824 | no | BLOCK RAND RUNPERM SWITCHMATCH |
| 882 `…RESIDUAL-PLUS-0.0012…_cloud.excess.csv` | 13,824 | **yes** | BLOCK BLOCK2 OP_×5 SM_×4 UG_REAL |

**Re-priceable: 5 files. Aggregate-only placebo files found by the same sweep: 9. Against idea
871's own committed census of 70 placebo-bearing files in the record: 5/70 = 7.1%.**
**H_UNADJ CONFIRMED** — and far more strongly than its bar. 92.9% of the record's committed
placebo mass cannot be re-priced under *any* estimator, so the queue's question is answerable for
under a tenth of the numbers it was asked about.

## 2. The claims are not independent — the record double-counts

Pairwise bit-identity of the committed cells (max |difference| over the shared arms = **exactly
0.0**):

| file | file | bit-identical on | for |
|---|---|---|---|
| 875 | CORR-LO | 1,152 arms | BLOCK, RAND |
| 875 | 871 | 1,152 arms | BLOCK, RAND, SWITCHMATCH |
| CORR-LO | 871 | **3,456 arms** | BLOCK, RAND |
| 881 | 882 | 1,152 arms | BLOCK, BLOCK2, SM_DOM, SM_FILL, SM_LONE, SM_SPLIT8 |

**8 of 31 headline claims are duplicates.** The independent headline set is **23**, and every
hypothesis below is read on it. This was not something the run was looking for; it is a
by-product of needing a de-duplicated denominator, and it is the single most re-usable finding
here — the record's placebo claim count overstates its placebo evidence by ~26% at the headline
rung.

## 3. Q1 — ACQUISITION. H_ACQ REFUTED (narrowly)

| claim set | acquire a determinate sign (|z| ≥ 2.0) | direction |
|---|---|---|
| HEADLINE (23, de-duplicated) | **5 (21.7%)** — bar was ≥ 25% | 3 negative / 2 positive |
| ALL (151 cuts) | **61 (40.4%)** | 29 negative / 32 positive |

Reported as it came: at the headline rung the signed estimator gives a determinate sign to about
a fifth of the record's re-priceable placebo claims, not the quarter the bar asked for. Across
all rungs and windows it is two fifths. The five headline acquirers are RAND on two files (an
already-known 13× switch-count artefact, not news), SM_DOM on two files (875/881's own effect),
and SWITCHMATCH on 871.

## 4. H_HIDE REFUTED — ABS was not, in general, calling these "noise"

| file | null | ABS ÷ its own prediction | SIGNED_MED | z |
|---|---|---|---|---|
| 875 | RAND | **16.07** | +0.27201 | −33.94 |
| 875 | SM_DOM | **1.34** | −0.00455 | +3.83 |
| 881 | RAND | **16.07** | +0.27485 | −33.94 |
| 881 | SM_DOM | **0.96** | −0.00348 | +3.83 |

ABS sits at or below its own seed-noise prediction in **1 of 4 = 25%**, against a 66.7% bar.
875's "the estimator is what hides the effect" is true of **SM_DOM on 881's file and nowhere
else** in the re-priceable corpus; the other sign-acquiring claims were already loud under ABS.
The generalisation the queue proposed does not hold. (Only 4 of the 5 acquirers carry a
computable ABS prediction at all — the fifth is on a file that committed no seed dispersion.)

## 5. Q2 — THE REPLACEMENT ESTIMATOR IS NOT SIGN-STABLE. H_STABLE REFUTED

**7 of 23 headline claims (30.4%) — and 26 of 151 cuts (17.2%) — have a SIGNED median and a
SIGNED mean of OPPOSITE sign**, against a < 10% bar.

| file | null | SIGNED_MED | SIGNED_MEAN | z |
|---|---|---|---|---|
| 875 | SWITCHMATCH | −0.00080 | **+0.00099** | +0.71 |
| 881 | BLOCK2 | −0.00015 | **+0.00001** | +0.24 |
| 881 | SM_UNIF | +0.00023 | **−0.00031** | −0.41 |
| 871 | RUNPERM | +0.00013 | **−0.00021** | −0.37 |
| 882 | OP_FILL | +0.00042 | **−0.00005** | −0.94 |
| 882 | OP_SPLIT8 | +0.00044 | **−0.00014** | −0.53 |
| 882 | UG_REAL | −0.00030 | **+0.00033** | +0.18 |

Every one is an unresolvable claim (|z| ≤ 0.94), so no *verdict* turns on the instability — but
every one is a **number the record would quote**, and its sign depends on a pooling choice no
memo declares. This is the decisive practical finding: **swapping ABS for SIGNED does not by
itself make the record's placebo numbers well-defined.** It moves the ambiguity from "no sign at
all" to "sign depends on median vs mean".

## 6. Q3 — how many verdicts actually move

| ABS ↓ / SIGNED → | EXACT ZERO | RESOLVED | not resolvable |
|---|---|---|---|
| RESOLVED | 0 | 3 | **2** |
| UNADJUDICABLE | 0 | 1 | 3 |
| not resolvable | 1 | **1** | 12 |

**HEADLINE: 2 noise → resolved, 2 resolved → noise, of 23 = 17.4%.**
**ALL: 53 noise → resolved, 6 resolved → noise, of 151 = 39.1%** (inflated by the 79
ABS-UNADJUDICABLE cuts, which have no ABS verdict to move *from*).

One claim reads **EXACT ZERO**: idea 882's `OP_REAL`, which is BLOCK by construction. The sign
test is run with ties excluded precisely so that an exact zero is not handed z = −33.9 and
crowned the most resolvable claim in the record — a trap the naive sign test falls into and which
this run had to fix before any count was read.

## 7. Rule 8 (a) — does a re-priced verdict walk forward?

IS = …2016-12-31 fitted, OOS = 2017-01-01… read once, from the committed `excess_IS` /
`excess_OOS` columns. **Of 10 de-duplicated claims resolvable in sample, 7 are resolvable out of
sample with the same sign = 70.0%. H_WF CONFIRMED** (bar 50%). Sign agreement IS vs OOS over all
23 de-duplicated claims: **82.6%**.

Walkers: RAND ×2, SM_DOM ×2, SM_FILL, SM_SPLIT2, SWITCHMATCH (871), OP_DOM. Non-walkers include
SM_SPLIT8 (IS +0.00456 z −4.54 → OOS +0.00158 z −1.12) and RUNPERM (IS −0.00167 z +2.72 → OOS
+0.00090 z −1.84, a **sign flip out of sample on a claim that was resolvable in sample**). The
IS/OOS cuts commit no seed dispersion, so they are ABS-unadjudicable by construction: **out of
sample, the signed reading is the only reading that exists at all.**

## 8. Rule 8 (b) — the books, both KEEP paths (10 bps, next-day, weekly)

Declared IS-only selector: highest 2009–2016 Sharpe over every arm of the panel; OOS read once.

| panel | IS pick | CAGR | Sharpe | MaxDD | H1/H2 | OOS CAGR | OOS Sh | OOS DD | 4a | 4b |
|---|---|---|---|---|---|---|---|---|---|---|
| U56 | CORR-HI q0.07 w1008 d1.00 W g1.00 | 12.73% | 1.034 | −22.93% | 1.160/0.915 | 12.41% | 1.016 | −22.93% | ✗ | ✗ (DD) |
| B136 | CORR-HI q0.12 w252 d1.00 W g1.00 | 13.91% | 1.166 | −16.63% | 1.289/1.037 | 12.97% | 1.154 | −16.63% | ✗ | **✓** |
| SMALL | VOL20-LO q0.17 w252 d1.00 D g1.00 | 5.04% | 0.404 | −48.52% | 0.736/0.201 | 2.00% | 0.203 | −48.52% | ✗ | ✗ |
| — | RULES v2 live (U56) | 8.64% | 1.208 | −11.90% | 1.237/1.186 | 9.49% | 1.286 | −11.90% | — | — |
| — | SPY (U56 window) | 15.13% | 0.885 | −33.72% | 0.959/0.824 | 15.27% | 0.874 | −33.72% | — | — |

Unselected base rates: **4a 0 (0.0%)** on all three panels; 4b U56 61/384 = 15.9%, B136 44/384 =
11.5%, SMALL **0**/384. The B136 pass is the same CORR-family by-product 875 memo'd and declined,
881 declined, and 882 declined — **declined a fourth time, not promoted, no KEEP memo written.**

## PROPOSED PROTOCOL amendment (rule 6: PROPOSED, NOT APPLIED; PROTOCOL.md untouched)

> A run that reports a placebo difference must (a) **commit its per-arm cells including its own
> seed dispersion** — without them the number is unadjudicable forever, which is the state 92.9%
> of the record's placebo mass is already in; (b) **declare its pooling rule (median or mean)
> beside the number**, because 30.4% of the re-priceable headline claims have medians and means
> of opposite sign; and (c) **name the reference null's provenance**, because four committed files
> in this corpus publish bit-identical BLOCK and RAND columns and the record currently counts them
> as separate evidence. Prefer the SIGNED pooled form over |null − BLOCK| — it is the only reading
> that exists out of sample — but do not treat the swap as a fix on its own: it relocates the
> ambiguity rather than removing it.

## Honest limits

1. **The denominator is tiny.** Five files, 23 independent headline claims. Every percentage in
   §3–§6 is a small-sample reading and H_ACQ misses its bar by one claim.
2. This run re-prices only what survived as per-arm data. It says nothing about whether the 65
   unre-priceable files' published numbers were right — only that they cannot be checked.
3. The `dup` detection is bit-identity on shared arm keys. Two runs that shared a seed stream but
   differed in one arm would not be caught; the four collisions found are exact and total.
4. `NSEED = 20` is assumed for the ABS prediction on all three seed-dispersion-bearing files. It
   is correct for 881 and 882 by their own memos and for 875 by its headline; a file that used a
   different budget would have its `obs/pred` mis-scaled, and only 4 claims depend on it.
5. SURVIVORSHIP: the book leg's U56 and B136 are current-constituent lists; SMALL is the sub-$2B
   panel with every `max_1d_move` ≥ 1.0 ticker dropped (716 → 664) and holds current constituents
   only, so its levels are the most optimistic here and its 0-of-384 4b rate is an upper bound
   that still reads zero. The census legs inherit whatever bias their source runs carried.
6. Deterministic; reads committed CSVs read-only.

**Verdict: ANSWERED = 17.4% of the record's 23 independent re-priceable placebo claims change
resolvability verdict (39.1% over all 151 cuts), but only 7.1% of the record's placebo mass can be
re-priced at all, 26% of the headline claims are bit-identical duplicates, and 30.4% of the signed
readings have medians and means of opposite sign / H_UNADJ and H_WF CONFIRMED / H_ACQ, H_HIDE and
H_STABLE REFUTED / KILL for capital.**

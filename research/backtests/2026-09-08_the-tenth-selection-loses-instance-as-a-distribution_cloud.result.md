# Idea 229 — the-tenth-selection-loses-instance-as-a-distribution (cloud, 2026-09-08)

**ANSWERED, and the queue's framing has to change. The record does not hold 10 such instances, it
holds 104 over 69 files; and once they are pooled, the mean loss is not a constant and is not even
reliably a loss — it is −0.0015 of OOS Sharpe with a 95% CI of [−0.0134, +0.0136] under an
instance block. The reason the individual instances look decisive and the pool does not is that
`margin = ROOM − REGRET`: ROOM (how bad the arm you would otherwise have held is) belongs to the
DIAL and its incumbent, and REGRET (the chooser's shortfall against its own pool's OOS best) is
the only term selection controls. On a fresh out-of-corpus 36-cell live corpus, ROOM is +0.110 and
REGRET is +0.0387 [+0.021, +0.058]. So the number PROTOCOL should quote is not the margin at all —
it is the REGRET, ≈ 0.04 of OOS Sharpe per selection, rising ≈ 0.009 per grid step of IS–OOS
argmax distance.** No selector class beats doing nothing on a usable CI; no KEEP (0 of 6 books on
both paths). `RULES.md`, `scan.py`, `bot.py`, `baseline.py` untouched.

Script: `research/backtests/2026-09-08_the-tenth-selection-loses-instance-as-a-distribution_cloud.py`
Artefacts: `.console.txt`, `.census.csv` (every file, admitted or rejected with reason),
`.instances.csv`, `.cells.csv` (24 610 paired cells), `.classes.csv`, `.boot.csv`, `.livegrid.csv`
(234 fresh books), `.walkforward.csv`, `.keeppaths.csv`.

Two tuned parameters: **P1** admission vocabulary ∈ {STRICT, BROAD}; **P2** bootstrap block ∈
{cell, instance, file}. All 2 × 3 points reported. The live corpus's six ladders, their declared
incumbents, the IS/OOS split, costs, cadence, gross and panels are the record's committed
conventions.

## (1) The census — 104 instances, not 10, and every file accounted for

All 305 committed `*.walkforward.csv` scanned. Two admitted shapes, declared before any number was
read: **SHAPE-W** (a per-row `OOS_Sharpe` for a selected arm plus a declared do-nothing control
column, *and* evidence the rows are the outcome of a selection) and **SHAPE-L** (an arm column
whose level set contains both a declared control level and a declared selector level, paired within
the group formed by every non-metric column).

| P1 vocabulary | instances | files (coverage) | paired cells | W / L |
|---|---|---|---|---|
| **STRICT** (do-nothing arm only: control, S0, ctl, ctrl, anchor, none) | **104** | 69 (22.6%) | 5 302 | 66 / 38 |
| BROAD (+ the declared comparand: base, v1, v2, live) | 237 | 119 (39.0%) | 19 308 | 195 / 42 |

Rejections, published rather than hidden: 159 files carry no control column and no control level
(STRICT), 75 carry no `OOS_Sharpe` column at all, 2 carry a control column but no evidence their
rows are IS-selected. **`base_OOS_*` is deliberately excluded from STRICT**: in this record it is
almost always the RULES baseline book — a different strategy, not the unselected arm — and treating
it as "doing nothing" is exactly what flips the sign (see §2).

The coverage number is the honest limit: a run that lost to doing nothing but never wrote a
machine-readable walk-forward file cannot be counted, so **104 is itself a lower bound.**

## (2) Q1 — the mean loss is not a constant, and under STRICT it is not distinguishable from zero

| P1 | cells | instances | cell-weighted mean | instance-weighted mean | cell win rate | instances that win |
|---|---|---|---|---|---|---|
| **STRICT** | 5 302 | 104 | **−0.00202** | **−0.00052** | 34.5% | 47.1% |
| BROAD | 19 308 | 237 | +0.15330 | +0.10217 | 57.0% | 59.9% |

P2, on the mean margin:

| P1 | block | mean | 95% CI | P(mean < 0) |
|---|---|---|---|---|
| STRICT | cell | −0.00205 | [−0.00495, +0.00084] | 91.6% |
| **STRICT** | **instance** | **−0.00147** | **[−0.01342, +0.01361]** | **63.3%** |
| STRICT | file | −0.00161 | [−0.01417, +0.01521] | 63.4% |
| BROAD | cell | +0.15330 | [+0.14891, +0.15793] | 0.0% |
| BROAD | instance | +0.15134 | [+0.06066, +0.25940] | 0.0% |
| BROAD | file | +0.15405 | [+0.08404, +0.26286] | 0.0% |

**The vocabulary decides the sign.** Against the unselected arm the chooser is flat; against the
live baseline book it is +0.15 — but that second number is a statement about the baseline, not
about selection, and it is the confusion the record's prose has been living inside.

**It is not a constant.** Between-instance variance 0.00755 against mean within-instance variance
0.00860 — **46.8%** of the total sits between instances, and the between-instance sd (0.0869) is
**59×** the pooled mean itself (0.0015). The individual published instances range from **−0.4937**
(`does-a-BAND-recover-what-the-raw-200d-gate-burns-in-H1`, 4 cells) through −0.2612 and −0.2518
(`quote-every-n-argmax-with-its-saturation-share`) to −0.0659 over 156 cells
(`price-denominator-sign-test`). Quoting any one of them as "the" number is quoting the tail.

## (3) The decomposition that settles it: margin = ROOM − REGRET

For every cell, identically:

> `margin = (OOS_best − OOS_S0) − (OOS_best − OOS_pick) = ROOM − REGRET`

**ROOM** is how much a perfect chooser could have won over the arm you would otherwise hold — a
property of the dial and its incumbent. **REGRET** is the chooser's own shortfall, ≥ 0 by
construction. Only REGRET is attributable to selection. Fresh live corpus, 36 cells (3 panels × 2
costs × 6 dials), choice on IS ≤ 2016-12-31, 2017–2026 read once:

| dial | incumbent (declared) | beats S0 | ROOM | REGRET | MARGIN | mean \|IS−OOS\| steps |
|---|---|---|---|---|---|---|
| band | 0.03 | 3/6 | +0.03321 | 0.04197 | −0.00877 | 2.33 |
| cadence | W | 2/6 | +0.02190 | 0.01643 | +0.00547 | 0.50 |
| gross | 0.75 | 0/6 | +0.00058 | 0.00135 | −0.00076 | 4.00 |
| **kexp** | **−0.50** | 6/6 | **+0.30848** | 0.06121 | +0.24727 | 2.00 |
| **share** | **0.20** | 4/6 | **+0.26820** | 0.09556 | +0.17263 | 1.17 |
| volcap | 0.60 | 2/6 | +0.02816 | 0.01572 | +0.01244 | 1.50 |
| **ALL** | — | **17/36** | **+0.11009** | **0.03871** | **+0.07138** | 1.92 |

The whole positive margin is two dials. `kexp`'s incumbent is the live k = −0.50 vol scaler that
ideas 168 and 440 have already shown to be on the wrong side of zero, and `share`'s is a mid-ladder
n. Those two supply **+0.28834** of the ROOM; the other four supply **+0.02096**. **On the four
dials with a defensible incumbent the chooser beats do-nothing in 7 of 24 cells, mean margin
+0.00209.** Selecting is a wash whenever the thing you are selecting away from is not already
known-bad.

**REGRET is strictly positive and stable: 0.03871, 95% CI [0.02078, 0.05805].** The record's own
published regret columns agree in order of magnitude: on the 32 STRICT instances that publish one,
cell-weighted **+0.05473**, instance-weighted **+0.02999** (42.9% of cells carry positive regret).
Two independent corpora, the same ≈ 0.03–0.05.

## (4) Q2 — it scales with the IS–OOS argmax distance

| | cells | mean margin | chooser beats S0 |
|---|---|---|---|
| IS and OOS argmax AGREE | 9 / 36 | +0.22587 | 9/9 *(definitional — if the pick IS the OOS argmax it cannot be beaten by any arm, S0 included)* |
| they DISAGREE | 27 / 36 | +0.01989 | **9/27** |

Spearman(\|IS−OOS\| steps, **margin**) = **−0.336**, OLS slope **−0.0395 per grid step**;
normalised by ladder length, Spearman = **−0.501**. Spearman(\|IS−OOS\| steps, **regret**) =
**+0.416**, OLS slope **+0.00929 per grid step** (intercept +0.0209). So the selector's own cost
grows roughly one basis-point-of-Sharpe per hundredth per grid step of disagreement, and the two
argmaxes disagree in **27 of 36** cells (mean distance 1.92 steps).

## (5) Q3 — has any selector class ever won?

Declared name map, per-class bootstrap over instances. A CI built on fewer than 5 instances is
declared unusable up front and is reported as such rather than as a verdict.

| P1 | class | cells | inst | files | cell mean | inst mean | win rate | 95% CI | verdict |
|---|---|---|---|---|---|---|---|---|---|
| STRICT | IS-SHARPE | 4 044 | 76 | 64 | −0.00279 | −0.00461 | 32.3% | [−0.0142, +0.0162] | **not separable** |
| STRICT | GATED | 1 038 | 41 | 22 | +0.00298 | +0.00974 | 44.7% | [−0.0262, +0.0405] | **not separable** |
| STRICT | IS-CAGR | 206 | 3 | 3 | +0.00495 | +0.00307 | 29.1% | [+0.0010, +0.0063] | CI not usable (3 instances) |
| STRICT | RANDOM | 14 | 1 | 1 | −0.25177 | −0.25177 | 14.3% | — | CI not usable (1 instance) |
| BROAD | IS-SHARPE | 14 065 | 194 | 110 | +0.16823 | +0.11045 | 57.9% | [+0.0420, +0.3013] | wins *(against the baseline book, not the unselected arm)* |
| BROAD | GATED | 2 376 | 74 | 31 | +0.16113 | +0.13669 | 63.3% | [+0.0744, +0.2577] | wins *(same caveat)* |
| BROAD | IS-CAGR | 600 | 9 | 4 | +0.09750 | +0.08644 | 48.0% | [−0.0717, +0.3052] | not separable |

**Under STRICT no selector class wins and none loses on a usable CI.** Two classes with enough
instances to judge — plain IS-Sharpe argmax (76 instances, 64 files) and the record's gated /
clause-conditioned selectors (41 instances) — are both flat. The gated family's point estimate is
one notch better than plain IS-argmax (+0.0097 vs −0.0046 instance-weighted) but the intervals
overlap almost entirely; idea 142's K_CAGR result and idea 415's open question are not settled by
this pool, only bounded. ORACLE arms were held out of every class as a non-selector reference.

## (6) Rule 8 on live prices — the pooled books, and both KEEP paths

Equal weight over the 36 cells, 10 bps rung shown for the baselines, weekly, t+1. 4b bars off the
pooled SPY: H1 > 0.965, H2 > 0.834, OOS > 0.882, |MaxDD| ≤ 20.23%, CAGR ≥ 10.05%.

| book | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR | OOS Sharpe | OOS MaxDD | 4a v2 | 4a v1 | 4b | failing |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 IS-Sharpe chooser | 8.05% | 0.911 | −17.12% | 1.035 / 0.811 | 8.13% | 0.879 | −17.12% | False | True | **False** | H2\|OOS\|CAGR |
| S0 do nothing (declared incumbents) | 6.09% | 0.788 | −15.28% | 0.914 / 0.687 | 6.12% | 0.756 | −15.28% | False | False | **False** | H1\|H2\|OOS\|CAGR |
| ORACLE (OOS argmax — not a rule) | 7.41% | 0.898 | −15.72% | 0.976 / 0.837 | 7.84% | 0.904 | −15.72% | False | True | False | CAGR |
| **SPY** | 14.36% | 0.883 | −33.72% | 0.965 / 0.834 | 15.45% | 0.882 | −33.72% | — | — | — | — |
| **RULES v2 (live) @10 bps** | 6.69% | 1.032 | −10.90% | 1.086 / 0.987 | 7.13% | 1.063 | −10.90% | — | — | — | — |
| RULES v1 @10 bps | 6.93% | 0.756 | −18.24% | 0.840 / 0.691 | 7.48% | 0.768 | −18.24% | — | — | — | — |

**0 of 6 on 4a-vs-RULES-v2 and 0 of 6 on 4b.** The pooled chooser book beats the pooled do-nothing
book by +0.1231 OOS Sharpe and +2.01 pp OOS CAGR — but it buys that with +1.83 pp more drawdown,
and *the entire gain is the two known-bad incumbents*: the chooser also beats the ORACLE on CAGR
(8.13% vs 7.84%) purely because the ORACLE is chosen on Sharpe. Neither book is capital-worthy:
both fail SPY's halves and the 4b CAGR floor, and neither beats RULES v2's Sharpe in either half.

Per-panel note: the chooser beats do-nothing in 4/12 cells on u56, 7/12 on broad, 6/12 on SMALL439.
*(SMALL439 = current constituents of the screen with `max_1d_move ≥ 1.0` dropped, 439 names;
**survivorship bias** — a shape check, never a tradable return.)*

## Verdict

**ANSWERED / KILL of the framing.** "Selection loses" is not a fact the record supports as stated,
and neither is its opposite. Pooled against the arm you would otherwise have held, an IS chooser is
flat: −0.0015 of OOS Sharpe, CI [−0.0134, +0.0136], across 104 instances and 5 302 cells. What is
real, positive and stable is **REGRET** — the chooser's shortfall against its own pool's OOS best —
at **≈ 0.04 of OOS Sharpe (live corpus 0.0387 [0.021, 0.058]; record's own published regret columns
0.030–0.055)**, growing **≈ 0.009 per grid step** of IS–OOS argmax disagreement, with the two
argmaxes disagreeing in 27 of 36 fresh cells. Every apparent *gain* from selecting is ROOM, i.e. a
verdict on the incumbent, not on the selector.

## What this run proposes (for the queue, not adopted here)

1. **PROTOCOL should quote REGRET, not margin.** The sentence "an IS chooser loses to doing nothing"
   should become "an IS chooser gives up ≈ 0.04 of OOS Sharpe against the best arm in its own pool,
   and whether that shows up as a loss depends entirely on how bad the arm it replaced was." Any run
   reporting a selection result should publish ROOM and REGRET separately, since their difference is
   the only thing currently reported and it is not attributable to the selector.
2. **A do-nothing control is the unselected arm of the SAME ladder, never the baseline book.** This
   run's P1 shows the two readings differ by 0.155 of Sharpe and by sign. The record has 195 SHAPE-W
   instances whose only control is `base_*`; they are answering a different question from the one
   their prose claims.

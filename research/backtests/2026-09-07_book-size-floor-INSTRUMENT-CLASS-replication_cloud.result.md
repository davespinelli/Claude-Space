# Idea 124 — book-size floor: INDEPENDENT THIRD REPLICATION (cloud, 2026-09-07)

**Script:** `2026-09-07_book-size-floor-INSTRUMENT-CLASS-replication_cloud.py`
**Verdict: CORROBORATES both same-day KILLs, and settles the one thing they disagreed on.
There is NO single number. The floor is a property of the INSTRUMENT CLASS; where a number
does exist it is n ≥ 40, not the queue's "~20".**

## Standing of this run

Two lanes ran idea 124 the same day and both committed a KILL — `..._B.py` (lane B, SPLIT)
and `..._cloud.py` (the other cloud lane). **This is not a fresh claim on the idea.** It
was designed and executed independently of both, without their artefacts, and is committed
under its own slug so nothing of theirs is overwritten. It is kept for three reasons: it
settles a disagreement between them (§[G]), and it reports two things neither does — the
floor decomposed by **instrument class**, and a direct measurement of **why** small books
fail.

## What was asked

Idea 122 found that all 24 panel-axis and all 5 cost-axis sign failures in idea 94's price
list were the 5-name V1u book, while the 56-name EWall book was 47/48. The queue asked to
price the same instruments on top-n books, n ∈ {3, 5, 10, 20, 40, ALL}, and find the n at
which the denominator's sign becomes stable — "a number PROTOCOL can state instead of
'~20 names'".

The denominator is `dDD = |MaxDD(base)| − |MaxDD(armed)|`, the drawdown an instrument
buys. A quoted price `dCAGR / dDD` is meaningless unless dDD > 0 and that sign is stable.

## Design

One tuned dial: **n** ∈ {3, 5, 10, 20, 40, ALL}, with a gross sensitivity at
g ∈ {0.50, 0.75, 1.00} on U56. Base book = equal weight over the top-n names by
`baseline.score`'s composite term alone (no trend multiplier, no vol scaling — those are
the instruments), 75% gross, weekly, next-day execution. 12 instruments, every internal
constant inherited verbatim from idea 94 / RULES v1 (200d, 3% band, vol20 < 0.60, 12-month
absolute momentum, 20% trailing stop, 0.85 lever, 8/4 pp drawdown control) — zero degrees
of freedom. Four sign axes: **cost** {0,10,25}, **window** {full, H1, H2, OOS},
**panel** {U56, B136, SMALL439}, and **block** (6 disjoint sub-windows, MaxDD recomputed
on each block's own equity path). `stop20-*` carried as a pre-registered negative control.

**Gates 4/4:** `fast_backtest` vs `engine.backtest` 0.000e+00 (returns and turnover);
derived 25-bps rung 0.000e+00; `n=ALL` == equal-weight-every-rankable-name 0.000e+00;
`-rw` restores full target gross on every non-empty day 4.441e-16.

## [B] The answer: no single number

Share of instrument cells whose dDD keeps its sign, all three panels, controls excluded:

| n | cost | window | panel | **all 3** | block (all 6) |
|---|---|---|---|---|---|
| 3 | 0.367 | 0.200 | 0.300 | **0.200** | 0.167 |
| 5 | 0.433 | 0.300 | 0.300 | **0.267** | 0.200 |
| 10 | 0.533 | 0.500 | 0.400 | **0.333** | 0.300 |
| 20 | 0.800 | 0.433 | 0.600 | **0.333** | 0.233 |
| 40 | 0.833 | 0.800 | 0.900 | **0.733** | 0.400 |
| ALL | 0.900 | 0.900 | 0.700 | **0.700** | 0.633 |

**Book size is genuinely the dial** — every axis rises monotonically in n — but the
pre-registered 95% bar (idea 122's own published 47/48 = 97.9%) is **never reached at any
n, n=ALL included**. On this three-panel design the queue's requested number does not
exist.

**Restricted to idea 122's own scope (large-cap panels U56 + B136) it does**, and it
reconciles exactly:

| n | 3 | 5 | 10 | 20 | 40 | ALL |
|---|---|---|---|---|---|---|
| all 3 axes | 0.200 | 0.300 | 0.350 | **0.550** | 0.900 | **1.000** |

Idea 122's 5-name V1u book → 0.300 here; its 56-name EWall book → 1.000 here. **The
queue's own "~20 names" is far too low: at n=20 only 55% of denominators are sign-stable.**
The number PROTOCOL can state is **n ≥ 40** (0.900), and n = the full eligible book for
1.000. SMALL439 is what removes the number from the three-panel reading: its own
sign(dDD) rate peaks at 0.900 (n=40) and *falls back to 0.700 at n=ALL*, while U56 and
B136 both reach 1.000.

## [C] The better answer: the floor belongs to the instrument, not the book

Sign survival on all three axes, by instrument (1.00 = held everywhere):

| instrument | 3 | 5 | 10 | 20 | 40 | ALL |
|---|---|---|---|---|---|---|
| **gross85** (static lever) | **1.00** | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| **ddctl8** (book drawdown control) | 0.67 | **1.00** | 1.00 | 0.67 | 1.00 | 1.00 |
| g200-dg | 0.00 | 0.00 | 0.00 | 0.33 | 0.67 | **1.00** |
| band3-dg | 0.00 | 0.00 | 0.67 | 0.33 | **1.00** | 1.00 |
| vol60-dg | 0.33 | 0.67 | 0.67 | **1.00** | 1.00 | 1.00 |
| abs12-dg | 0.00 | 0.00 | 0.00 | 0.00 | 0.67 | **1.00** |
| g200-rw / band3-rw / vol60-rw | 0.00 | 0.00 | 0.00 | 0.00 | 0.67 | **0.00** |

Three classes with three different floors:

1. **EXPOSURE instruments (`gross85`, `ddctl8`): no floor at all.** `gross85` is
   sign-stable at n=3 on every axis and in 6 of 6 blocks. It acts on the whole book by
   construction, so scaling weights by 0.85 scales the drawdown by ≈0.85 identically.
2. **SELECTION + de-gross (`-dg`): floor at n = 40**, full at n = ALL.
3. **SELECTION + respread (`-rw`): no floor exists in the grid.** Three of four `-rw` arms
   are **0.00 at n=ALL** — respreading to full gross gives back exactly the drawdown the
   gate bought, so the denominator never settles. This is the same fact idea 94 measured
   as "-rw buys 2.69 pp against -dg's 3.50 pp", now read as a stability result.

## MECHANISM: below n≈20 the denominator is not noisy, it is ZERO

Median |dDD| at 10 bps, in pp of drawdown:

| class | n=3 | 5 | 10 | 20 | 40 | ALL |
|---|---|---|---|---|---|---|
| EXPOSURE | 7.82 | 6.07 | 4.10 | 3.84 | 5.20 | 5.91 |
| SELECT-dg | **0.000** | **0.000** | 0.95 | 2.68 | 4.91 | 10.51 |
| SELECT-rw | **0.000** | **0.000** | 0.15 | 0.82 | 1.74 | 2.98 |

Share of the book the gate actually removes (median over panels): `g200-dg` and `band3-dg`
strip **0.1% of a 3-name book and 0.3% of a 5-name book**, against 28.8% at n=ALL. A
top-3 momentum book is already above its own 200-day average essentially always, so the
trend gate never fires: the price is **0/0**, and its sign is arbitrary rather than noisy.
This is why the price list has NaN entries at n=3 and n=5 for all eight gate arms — there
is no priceable denominator there at all — and why `gross85`, which cannot be a no-op,
needs no floor.

## Gross sensitivity: the floor is not a function of gross

On U56, the within-panel axes are near-identical across g ∈ {0.50, 0.75, 1.00}:
cost {0.40, 0.50, 0.80, 0.90, 1.00, 1.00} / {0.50, 0.40, 0.80, 0.90, 1.00, 1.00} /
{0.40, 0.40, 0.90, 0.90, 1.00, 1.00}; window likewise. (The `panel` column of the g=0.50
and g=1.00 rows is degenerate — those levels were run on U56 only — and must not be read
as a gross effect.)

## [F] Rule 8

**(a) The floor derived on the in-sample window alone, read once on 2017–2026.** The
*direction* walks forward — sign_ok is monotone in n in both windows — but the *location*
moves one rung: IS says n=ALL (sign 1.000, panel 1.000), OOS says **n=40** (0.967 / 0.900)
with n=ALL falling back to 0.900 / 0.700. A floor quoted as "the full book" is therefore
IS-specific; **n ≥ 40 is the reading that survives both windows.**

**(b) Base-book n chosen on IS Sharpe ≤2016, U56 @10 bps.** The chooser picks **n=3**
(IS 1.3789) and gives up **0.130 of OOS Sharpe** (1.0250 vs the OOS-best n=20's 1.1549)
plus 11 pp of drawdown (−34.50% vs −22.61%). The same narrow books whose price
denominators are unstable are the ones an IS Sharpe chooser prefers — the two failure
modes point the same way.

## [E] KEEP paths, 78 cells × 3 panels × 3 rungs

**4a: 1 of 702 cell-rungs** — U56 / n=ALL / `band3-dg` (10 bps: 8.72% / 1.2088 / −12.05%,
halves 1.2306 / 1.1924, OOS 1.2863, 1.78×/yr). That book **is RULES v2**, differing only
in whether the equal-weight denominator counts *rankable* or *priced* names; it clears the
bars by 0.003 of Sharpe with an identical drawdown. Reported as a reproduction, **not
proposed** — a 0.003 margin against the same rule is a denominator convention, not an edge.

**4b @10 bps: 35 of 234** — U56 29/78, B136 6/78, **SMALL439 0/78 at every rung**. Binding
bar is `DD` almost everywhere (44 of 78 on U56, 64 on B136). Best U56 cells are n=40
`band3-dg` (11.10% / 1.1976 / −15.75%, OOS 1.2612) and n=40 `g200-dg` (10.70% / 1.1771 /
−15.39%, OOS 1.2669) — both reproduce families the record already holds, and both are
dominated on CAGR by idea 360's b=0.12 respread book committed the same day. Nothing new
is proposed.

## Honest limits

1. `stop20-*` is the **stateless** form (20% below the trailing 252-day high), not idea
   94's true per-name trailing stop. It behaved as the pre-registered control at n ≤ 10
   (0.00) but reached 1.00 at n=40/ALL, so it does **not** replicate idea 94's
   "unpriceable in 10 of 12 cells". Treat that row as a different instrument, not a
   contradiction of idea 94.
2. The 95%-bar reading is pre-registered but the bar itself is a choice; the whole curve is
   published so PROTOCOL can set its own.
3. **SURVIVORSHIP:** B136 and SMALL439 are current constituents of their screens and are
   biased upward; U56 carries the same caveat more weakly.

## Proposed PROTOCOL wording

> *A drawdown price (pp of CAGR per pp of MaxDD) may be quoted only when the instrument
> either (a) acts on total exposure rather than on selection, or (b) is applied to a book
> of at least 40 names and sends the removed weight to cash. A price quoted from a
> respread (`-rw`) gate, or from a book of fewer than 40 names, must carry the measured
> dDD beside it; where dDD < 0.5 pp the price is not defined.*

## [G] Reconciliation with the two same-day runs

Both prior runs measure the admissible share over idea 94's **published** price rows, and
both independently flag that idea 94's own 0.10 pp publication floor is a selection filter
whose conditioning set moves with n (lane B: "published rows u56 [18,12,22,22,24,24]"; the
other cloud lane: "a selection filter that favours the narrow books"). Both then report the
ladder as **non-monotone**. This run carries no publication filter at all — all 12
instruments are priced at all 6 rungs on all 3 panels — so it is a direct test of whether
the non-monotonicity is the ladder's or the filter's.

| n | lane C published | lane C all-rows | lane B u56 published | **this run, unfiltered** |
|---|---|---|---|---|
| 3 | 0.649 | 0.375 | 0.556 | 0.200 |
| 5 | 0.846 | 0.344 | 1.000 | 0.267 |
| 10 | 0.650 | 0.406 | 0.864 | 0.333 |
| 20 | 0.551 | 0.453 | 0.727 | 0.333 |
| 40 | 0.885 | 0.719 | 1.000 | 0.733 |
| ALL | 0.979 | 0.734 | 0.958 | 0.700 |
| **down-steps** | **2** (5→10, 10→20) | **1** (3→5) | **3** (5→10, 10→20, 40→ALL) | **1** (40→ALL) |

**It is the filter's.** Remove the publication threshold and the two down-steps at
5→10 and 10→20 vanish on both readings that lack it — lane C's own all-rows column and
this run's unfiltered column. The single remaining down-step here is 40→ALL and is
entirely SMALL439 (U56 and B136 both reach 1.000 at n=ALL).

The three runs **agree** on everything that matters: the verdict (no rung clears the bar,
so no floor is statable), the location of the jump (between n=20 and n=40), and that the
queue's "~20 names" is the wrong number. They disagreed only about a shape the publication
filter was producing. Lane B's independently-derived "n* is 40 on u56" is the same number
this run's walk-forward lands on.

Two findings of the prior runs are **not** tested here and are not contradicted: lane C's
V1u-vs-TOP5 decomposition (the instability is the 1/√vol20 ranking factor, not the name
count) — this run has no vol-scaled book — and lane B's ordering result. They are
complementary to the instrument-class split above, not in competition with it.

## Artefacts

`.grid.csv` (78 cells × 5 panel-gross scopes), `.signtest.csv`, `.floor.csv`,
`.rule8_floor.csv`, `.keeppaths.csv`, `.walkforward.csv`, `.ctx.csv`, `.console.txt`.

# Idea 778 (cloud, 2026-09-11) — is-the-RSS-BAR-the-right-object-when-the-two-parents-OVERLAP

**ANSWERED / KILL for capital. The queue's conclusion is right and its reason is wrong.** Idea 774's
RSS bar *is* over-stated, and correcting it removes about half of its +41 conviction count — but the
whole of that correction comes from RSS being taken over **all three named parents** when the margin
is a single adjacent **two-parent** gap, **not** from the parents' overlap. The cross-parent draw
correlation the queue asked this run to measure is **not measurable at any draw count the record can
afford**: the two pairs that share **zero** names — whose true ρ is exactly 0 by construction — read
|ρ̂| as large as the completely-nested pair at every D. No new KEEP, no memo, no rule change;
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched (rule 6).

SELECTION: taken as the FIRST open idea in QUEUE.md; 778 mentions no EDGAR / Form 4 / 8-K / options /
spin-offs / live data.

Scripts `2026-09-11_is-the-RSS-BAR-the-right-object-when-the-two-parents-OVERLAP_cloud.py` (192s,
2,628-book price grid) and `..._cloud_addendum.py` (the disjoint-pair control, artefacts only).
10 bps · next-day fills · IS ≤ 2016-12-31, OOS ≥ 2017-01-01 read once.

## Gates (pre-registered, printed before any new number was read) — ALL PASS

| gate | object | result | bar |
|---|---|---|---|
| G5 structure | the parent overlap matrix, measured from the committed panels rather than assumed | **U56 55 names, ALL 55 inside B136's 135 — overlap coefficient 1.000, complete nesting. SMALL439 shares 0 names with either.** 1 nested pair, 2 disjoint | exact |
| G1 harvest | idea 567/774's committed `.census.csv` re-harvested from the record's 777 committed markdown files | **607 of 607 rows reproduced exactly** (this run harvests 608; the surplus is a file committed after 774 ran); min-gap pair attached to **607 of 607**, re-harvested parent set agrees with 774's on **607 of 607** | 607 |
| G2 floors | per-parent draw floors rebuilt from prices here vs idea 774's committed `.floors.csv`, all 60 (statistic, D, period) rows | **9.714e-17** — a second independent cross-lane reproduction of idea 567's floors | 1e-12 |
| G3 identity | `fast_backtest` vs `engine.backtest`, one book per parent | **0.000e+00** | 1e-12 |
| G4 headlines | idea 774's nine published movement numbers (POOLED 259 inside of 607; net MIN −8 / MEAN +0 / MAX +8 / **RSS +41**; shares .4942/.4267/.4135/.4399) re-derived from its OWN committed artefacts | max \|d\| **3.394e-05** | 1e-3 |

## Why independent seeds cannot answer this, and what was built instead

With the price history fixed, two draws taken with **independent** seeds have **exactly zero**
covariance no matter what the pools share — drawing S_b never looks at S_a. Pairing idea 774's own
draws by seed index therefore estimates ρ ≈ 0 *by construction*, which is precisely why RSS looked
correct. The correlation the queue means is a property of the **coupling**, not of the pools: the real
U56/B136 pair is two views of one set of names. So this run built that coupling explicitly — a
**common random permutation** of the union pool, each parent taking the first k=36 of its own members.
Measured result: the nested pair's coupled draws share **13.71 of 36 names** on average (min 9, max
19); both disjoint pairs share **0.00 of 36**, every seed. The coupling is real and it works.

## Dials (PROTOCOL rule 4 — exactly two, all 10 points reported)

1. **CORRELATION ESTIMATOR** ∈ {RSS_INDEP (774's bar), PAIR_INDEP (min-gap pair only, ρ=0),
   PAIR_SEED (ρ̂ from independent seed pairs — the null control), PAIR_COUPLED (ρ̂ from the coupled
   ensemble), PAIR_DIRECT (sd of X_i−X_j measured directly — no ρ, no normality)}
2. **BAR** b ∈ {1.0, 2.0} sd

Reported, never selected: statistic family (5), draw count D ∈ {3,6,12,24}, period (FULL/IS/OOS),
gross ∈ {0.50,0.75,1.00}, cadence ∈ {W,M}.

## The answer: the conviction count decomposes, and only one half of it is real

Net claims moved vs idea 567's POOLED bar (FULL, bar 1.0, 607 claims):

| estimator | D=3 | D=6 | D=12 | D=24 | range | verdict |
|---|---|---|---|---|---|---|
| **RSS_INDEP** (idea 774's bar) | +43 | **+41** | +42 | +43 | 2 | STABLE |
| **PAIR_INDEP** (min-gap pair, ρ=0) | +21 | **+18** | +20 | +21 | 3 | STABLE |
| PAIR_SEED | −12 | +25 | +17 | +18 | 37 | unstable |
| PAIR_COUPLED | −26 | +37 | +26 | +16 | **63** | unstable |
| PAIR_DIRECT | −8 | +29 | +33 | +17 | 41 | unstable |

**Of idea 774's +41, +22.2 on average is a specification error that is stable and real** — RSS over
all three named parents applied to what is in fact one adjacent two-parent gap. 262 of the 607 claims
name three panels, and for those 774's bar is √(f_U²+f_B²+f_S²) when the margin lives between exactly
two of them. Restricting the bar to the **min-gap pair** halves the conviction count to **+18…+21**,
and that number is flat in D. **The correlation term the queue asked for adds only −6.8 on average
with a 63-claim swing across draw counts** — noise, not a correction.

Min-gap pair distribution: `B136|U56` **366**, `SMALL|U56` 123, `B136|SMALL` 118. So the nested pair
is the bar-setting pair for **366 of 607** claims — the premise had the right target, wrong mechanism.

## The disjoint-pair control: ρ is unresolved, not zero

Two of the three pairs share zero names, so their true ρ is **exactly 0**. Whatever |ρ̂| they read is
the estimator's own noise, at the same D and the same aggregation:

| D | nested ρ̂ (PREM_SHARPE) | nested max \|ρ̂\| | **DISJOINT max \|ρ̂\| (true = 0)** | Fisher SE | nested z |
|---|---|---|---|---|---|
| 3 | +0.4345 | 0.9407 | **0.9385** | 0.4082 | +1.06 |
| 6 | −0.2985 | 0.3639 | **0.3676** | 0.2357 | −1.27 |
| 12 | −0.4739 | 0.4739 | **0.1842** | 0.1361 | −3.48 |
| 24 | −0.0149 | 0.2848 | **0.2700** | 0.0891 | −0.17 |

The completely-nested pair's |ρ̂| exceeds the structurally-zero pairs' own |ρ̂| in **5 of 20**
(statistic × D) cells — no better than a coin. At D=24, the largest draw count the record can afford,
the nested estimate is **z = −0.17** and even its sign is negative, i.e. the opposite of what complete
nesting predicts. The assumption-free **DIRECT** bar tells the same story: at D=24 the nested pair
reads **0.930× RSS** while the disjoint pairs, where RSS is exactly right, read **1.043× RSS** — the
overlap-adjusted bar is no further from RSS than pairs with no overlap at all.

**So the queue's stated mechanism is unfalsifiable at this resolution.** ρ is not small; it is
unresolved, and idea 777's k-ladder will not fix it — the limit is the 24-draw count, not k.

## Rule 8 walk-forward

**WF-A (the answer OOS)** — floors *and* both ρ estimators rebuilt on IS only and on OOS only, census
re-scored at all 10 points. Share inside (D=6, bar 1.0) FULL / IS / OOS: RSS_INDEP .4942/.5519/.4811,
PAIR_INDEP .4563/.5486/.4399, PAIR_SEED .4679/.4712/.4695, PAIR_COUPLED .4876/.5618/**.4250**,
PAIR_DIRECT .4745/.5338/.4415. Net conviction vs POOLED by period: RSS **+41/+37/+34** (the most
stable object in the run), PAIR_INDEP +18/+35/+9, PAIR_COUPLED +37/+43/**0**. **Direction agrees IS vs
OOS for 3 of 5 estimators** — and the two that disagree are both correlation-corrected ones. Nested-pair
ρ̂ (PREM_SHARPE, D=6) by period: −0.2985 FULL / −0.0996 IS / −0.1260 OOS; the disjoint pair
`B136|SMALL439`, true ρ = 0, reads −0.0175 IS / **+0.3207 OOS**.

**WF-B (the bar priced as a book)** — in each (gross, cadence) cell rank the three parents by IS
MA-gate premium; act on the IS-best parent only if the IS best-minus-worst span clears b × **that
pair's** corrected difference-sd, else stand down to RULES v2 on U56. OOS read once:

| book | acts | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|
| PAIR_COUPLED bar 1.0 (= always-act) | 6 of 6 | 13.00% | 1.1567 | −18.40% |
| RSS / PAIR_INDEP / PAIR_SEED / PAIR_DIRECT bar 1.0; PAIR_COUPLED bar 2.0 | 3 of 6 | 10.94% | 1.1966 | −15.06% |
| all four at bar 2.0 (full stand-down) | 0 of 6 | 9.45% | 1.2747 | −12.05% |
| **RULES v2 U56 (live book)** | — | **9.45%** | **1.2747** | **−12.05%** |
| SPY | — | 15.24% | 0.8721 | −33.72% |

**Decision books beating RULES v2 OOS Sharpe: 0 of 10. Beating SPY: 10 of 10.** Every book that acts
at all buys CAGR with drawdown and loses Sharpe — the same trade idea 774 and idea 567 already killed.

## KEEP paths

Full price grid **2,628 books** (36 REAL, 864 idea-774 independent draws, 1,728 coupled pair draws):
**4a 8/2628, 4b 149/2628, BOTH 0/2628.** By kind: REAL 4a 0/36 4b 3/36, DRAW 4a 2/864 4b 49/864,
CPL 4a 6/1728 4b 97/1728. The three REAL 4b passers are `U56/MA-RS/g0.75/W`, `U56/MA-RS/g0.75/M`,
`B136/MA-RS/g0.75/W` — **a third independent reproduction of idea 567's existing MA-RS gate**, nothing
new. Binding 4b legs: DD 930, CAGR 550. Decision books: **4a 0/10, 4b 1/10, BOTH 0/10**, and the single
4b pass is the always-act control (fails 4a, gives up 0.118 of OOS Sharpe for 6.4 pp more drawdown) —
idea 567's already-killed rule re-wrapped for the third time.

**NO KEEP-CANDIDATE, NO MEMO, NO RULES CHANGE.**

## PROTOCOL proposal (Sunday, not adopted)

Idea 774's proposed line — *"a margin that is a gap BETWEEN named panels must be quoted against the
root-sum-square of those panels' own draw floors"* — should be amended before adoption: quote it
against the RSS of **the two panels bracketing the margin**, not of every panel the claim names. That
is the half of 774's +41 that survives at every draw count. The overlap correction should **not** be
added: it is unresolved at D ≤ 24, and a bar built from an unresolved ρ̂ swings 63 claims.

## Survivorship

`universe_broad.json` and the small panel are **current constituents**, so every stock-side level
carries a survivorship premium and the LEVEL floors (SHARPE, CAGR, MAXDD) are lower bounds on true
dispersion; an arm-minus-arm premium on the same panel largely cancels it. The small panel drops every
ticker with `max_1d_move ≥ 1.0` (439 of 483 kept). The three parents also start on different dates
(U56/B136 2008-01-02, SMALL439 2010-01-04), inherited from idea 567's floor construction — noted
wherever a cross-parent correlation is quoted.

## Follow-ups proposed

779. **does the MIN-GAP-PAIR restatement change any published VERDICT, not just the count** — this run
shows +18…+21 of 607 claims move under the stable half of 774's correction, but a moved count is not a
moved conclusion. Re-read the ~20 claims that move and report how many carry a headline the record
relies on elsewhere. Max 2 params (claim set, bar).

780. **how many DRAWS would resolve a cross-parent ρ to ±0.10** — the disjoint control reads |ρ̂| up to
0.27 at D=24 against a true 0, so the record cannot measure any cross-panel correlation at its current
draw budget. Bootstrap the required D and publish it as the minimum before any future overlap-corrected
bar is quoted. Max 2 params (D ladder, target width).

781. **is the THREE-PARENT RSS error present in the record's other composite bars** — 774's bar summed
over every named parent because the census stores the named set, not the bracketing pair. Census the
record's other multi-object bars for the same "sum over all named, compare to a two-object gap"
specification error. Max 2 params (bar family, sample).

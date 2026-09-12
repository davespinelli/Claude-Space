# Idea 520 — give every reproduction gate a UNIT and a min(native, proposed) BAR

**lane B, 2026-09-12** · script `2026-09-12_give-every-reproduction-gate-a-UNIT-and-a-min-native-proposed-BAR_B.py`
**VERDICT: ANSWERED — premise CONFIRMED, back-fill KILLED, the (unit, bar) stamp is INSUFFICIENT. No book KEEP.**

Two tuned params, both swept, all 60 grid points reported: **UNIT SOURCE** `W ∈ {0,3,6,12,25}` lines of
source context, **BAR MULTIPLIER** `K ∈ {1,3,10,30,100,1000}`. Floor quantile pre-registered at q=0.99
(ladder 0.50/0.90/0.99/1.00 reported as sensitivity). 10 bps, t+1 execution, rule-8 split 2016-12-31.

## Gates (printed before any new number)

| gate | measured | bar | |
|---|---|---|---|
| G1 | numpy runner vs `engine.backtest`: returns 0.00e+00, turnover 0.00e+00 | <1e-12 | **PASS** |
| G2 | `EWALL(0.75) == baseline.rules_v2_weights` on U56: 0.00e+00 | 0.0 | **PASS** |
| G3 | idea 515's census: **520** clauses, **412** unknown units (**79.2%**) | published 520/412/79.2% | **PASS** |
| G4 | idea 515's S48 claim survival: native **0.6585** vs flat-1e-6 **0.5854** | published | **PASS** |
| G5 | `min(native, proposed) ≤ native` on all 472 declared bars | — | **PASS** |

**Incidental finding, worth its own line.** `engine.backtest` emits **2 NaN return days** on every panel
where the numpy runner emits 0. The return series is otherwise bit-identical (max|Δ| = 0.00e+00), but the
two NaN shift the observation count and move Sharpe by **2.52e-04 (U56) / 2.28e-04 (B136) / 1.68e-04
(SMALL)**. This is the entire SELF floor for the `sharpe` unit — every other unit's SELF floor is ~1e-16.
A self-consistency gate written at 1e-12 on Sharpe therefore **fails on which runner you used**, with no
disagreement about any return. A skipna `.max()` hides this, so both series are `fillna(0)`-ed on both
sides before differencing here.

## 1. The premise is CONFIRMED. The back-fill the queue asks for does NOT work.

Reading the clause text alone (W=0) names a unit on **105 of 520 (20.2%)** — statistically the same as
idea 515's hand-assigned 108 (20.8%) — and agrees with the hand reading on **85/94 = 90.4%**. Widening
the window buys coverage and sells precision, **monotonely and without a crossing point**:

| W | unit named | coverage | agreement with the hand anchor |
|---|---|---|---|
| 0 | 105 | 20.2% | **85/94 = 90.4%** |
| 3 | 491 | 94.4% | 48/108 = 44.4% |
| 6 | 516 | 99.2% | 36/108 = 33.3% |
| 12 | 520 | 100.0% | 27/108 = 25.0% |
| 25 | 520 | 100.0% | 18/108 = **16.7%** |

At 100% coverage the stamp is wrong 5 times in 6. **Coverage bought from surrounding source is not
recovery, it is invention.** The 412 unit-less clauses are unit-less in the source, not in the census.

## 2. "Proposed" is TWO numbers, not one — and that kills the (unit, bar) stamp.

The proposed bar is measured from prices: the reproduction noise floor of each unit over **84
perturbation cells** (3 panels × 3 gross × 3 cadences), split into two pre-registered strata that are
never pooled — **SELF** (same panel, same window; column order or implementation differs) and **REPRO**
(2% vintage drop, or a one-day start shift).

| unit | SELF floor (q0.99, 30 cells) | REPRO floor (q0.99, 54 cells) | ratio |
|---|---|---|---|
| cagr | 2.220e-16 | 3.761e-03 | 1.7e+13 |
| sharpe | 2.449e-04 | 2.297e-02 | 9.4e+01 |
| dd | 5.551e-16 | 9.650e-03 | 1.7e+13 |
| turnover | 3.797e-16 | 4.324e-02 | 1.1e+14 |
| weight | 1.110e-16 | 2.789e-03 | 2.5e+13 |
| share | 2.220e-16 | 2.514e-03 | 1.1e+13 |
| return | 1.585e-16 | 5.910e-03 | 3.7e+13 |
| price | 0.000e+00 | 0.000e+00 | — |
| count | 0.000e+00 | 4.880e+04 | ∞ |

**Up to 14 orders of magnitude apart for the SAME unit.** Priced on the 92 W=0 clauses that carry both a
unit and a native bar: against the SELF floor **14 are un-passable (15.2%)** and 21 are vacuous (>1e3×);
against the REPRO floor **92 are un-passable (100.0%)**. Same clause, same unit, opposite verdict. So
`(unit, declared_bar)` is **not** a sufficient stamp — the gate must also declare **which reproduction it
claims**. That is the finding the queue entry did not anticipate.

## 3. Rule 8 — both legs

**Leg 1 (this idea's own decision object): the floor calibrated on 2009–2016 books, read ONCE on
2017–2026.** The REPRO floor transfers with OOS/IS ratio median **1.79** (min 0.502, max 3.98); the SELF
floor transfers at median **1.00** (min 0.862, max 3.46). An IS-calibrated REPRO bar clears 77.2% of OOS
cells at K=1, **88.9% at K≥10, and never more** — the residual is `price`, whose floor is exactly 0 and
which no strict `<` bar can clear. **K=10 is the smallest multiplier that transfers; above it nothing is
bought.**

**Leg 2 (PROTOCOL book leg): 27 books + 6 benchmark rows, 4 IS-only selectors × 3 panels, each pick read
ONCE on 2017-01-01+.** `4a 1/12, 4b 4/12, BOTH 0/12` — the same picks and the same counts as the
2026-09-11 lane-B run on this family. The book leg **reproduces the standing EW-band result and
contributes no new book.** Best 4b cell, U56 EW-band g=1.00/M: full 11.95% / 1.182 / −18.56% (H1 1.228 /
H2 1.145), OOS 12.89% / 1.236 / −18.56%, against RULES v2 8.65% / 1.209 / −11.90% (OOS 1.287) and SPY
15.16% / 0.886 / −33.72% (OOS 0.877). It fails 4a on both halves and on MaxDD. **No KEEP claimed.**

## 4. Proposal (for Sunday review — PROTOCOL only; RULES.md, scan.py, bot.py, baseline.py untouched)

The queue's `(unit, declared_bar)` + `min(native, proposed)` rule is **adopted with one added field and
one correction**, both forced by the numbers above:

> **PROTOCOL 10 (proposed).** Every reproduction gate must declare a triple
> `(unit, kind, declared_bar)` at the site of the assert, where `unit` is one of
> {cagr, sharpe, dd, turnover, weight, price, share, return, count} and `kind` is `SELF` (the same panel
> and window, recomputed) or `REPRO` (a different panel vintage or sample window). The gate passes at
> `min(declared_bar, 10 × floor[unit, kind])`, read as `≤` where the floor is zero. Units must be
> **declared when the gate is written**; back-filling a unit from surrounding source is not permitted —
> measured at 16.7% accuracy at full coverage (§1). A gate that declares no `kind` is read as `REPRO`.

**Why the added field:** without `kind` the same clause is 15.2% or 100.0% un-passable (§2).
**Why K=10:** it is the smallest multiplier whose IS-calibrated bar transfers out-of-sample (§3).
**Why not back-fill:** §1.

## Artefacts

`.console.txt` (full log) · `.census.csv` (520 clauses, unit at every W) · `.floors.csv` (84 perturbation
cells) · `.grid.csv` (60 grid points, both strata) · `.walkforward.csv` (leg 1) · `.bookleg.csv` +
`.bookgrid.csv` (leg 2).

**Survivorship:** B136 and SMALL are current constituents of their screens (PROTOCOL rule 9); the floors
measured on them are therefore floors for a survivorship-clean panel and are, if anything, too tight.

# Idea 123 — relative-priceability-floor (lane C, 2026-09-05)

**Verdict: ANSWERED — the relative floor is worth adopting as a REPORT-ONLY PROTOCOL clause
and is a KILL as a selector (rule 8 costs 0.019 of OOS Sharpe). Two of the queue's own
premises are REFUTED: a negative price is *not* a symptom of a shallow denominator outside
the small panel (only 48 of 76 negatives are removed), and the floor does not rescue idea
97's tier statement — it makes it worse (121/162 clause-rows true → 114/162).**

Script `research/backtests/2026-09-05_relative-priceability-floor_C.py`, console
`…_C.console.txt`, data `…_C.{grid,pricelist,floors,stability,tiers,walkforward,cells}.csv`.
864 price rows (3 panels × 3 books × 2 costs × 16 arms × 3 windows), 306 arm-points,
5 φ grid points, all reported.

## 0. Reproduction — the audit is of the published files, not a re-derivation

Idea 94's module is imported, not re-implemented; idea 97's three panels are rebuilt under
idea 97's own conventions.

- engine-equivalence of the control vs `engine.backtest` @10 bps on u56: **max|diff| 0.0**.
- published `EWall+vol60-dg` u56 @10 bps: 11.6% / 1.133 / −16.9% — exact.
- idea 97's committed `pricelist.csv`: **288 of 288 rows** matched, max|Δ dCAGR| 8.9e-16,
  max|Δ dMaxDD| 3.6e-15, max|Δ rate| 4.4e-16, NaN-pattern 288/288.
- idea 97's committed `grid.csv`: **306 of 306 arm-points bit-identical** on CAGR, Sharpe,
  MaxDD, OOS_CAGR, OOS_Sharpe (max|diff| 0.0) and on both KEEP flags (p4a 306/306,
  p4b 306/306).

## 1. The re-tabulation (every published price, both floors)

`ABS` = idea 94's rule (publish iff dMaxDD > 0.10 pp). `REL(φ)` = publish iff
dMaxDD ≥ φ·|MaxDD_ctl| **in that window**. Headline φ = 0.10 is idea 119's own materiality
bar, adopted unchanged. All five φ reported in `…floors.csv`.

Full-window rows published under ABS = 202 of 288. Removed by REL:

| φ | u56 | broad | small | ALL | % of published |
|---|---|---|---|---|---|
| 0.00 | 0/70 | 0/68 | 0/64 | 0/202 | 0.0% |
| 0.02 | 0/70 | 8/68 | 10/64 | 18/202 | 8.9% |
| 0.05 | 0/70 | 10/68 | 21/64 | 31/202 | 15.3% |
| **0.10** | **6/70** | **16/68** | **31/64** | **53/202** | **26.2%** |
| 0.20 | 36/70 | 30/68 | 36/64 | 102/202 | 50.5% |

The removals have the same address idea 122 found for the sign test — **the book, not the
panel**: V1u 73 of 171 published rows removed (42.7%), TOP20 52/173 (30.1%), EWall 39/214
(18.2%). And a tier: **the stop dies. T4 loses 21 of its 23 published rows (91.3%)**, T1 gate
119/364 (32.7%), T3 ddctl 5/108 (4.6%). Median removed row buys **3.4% of the control's own
drawdown**; median kept row buys 6.6 pp.

## 2. R1 REFUTED — a negative price is not a shallow-denominator artefact off the small panel

76 published prices are negative across the three windows; REL(0.10) removes **48 (63.2%)**,
against a pre-registered 80% bar.

- In **idea 119's own cell** the claim is literally right: `small/V1u` full window has 11
  negatives and REL(0.10) removes **11 of 11**; only 7 of its 23 published prices survive.
- On **u56** it is wrong: 1 of 9 full-window negatives removed, 5 of 16 OOS. The surviving
  negatives sit at **7–29% of the control's |MaxDD|** (`u56/V1u band3-rw` @25 bps OOS: dMaxDD 5.84 pp
  = 29.3% of a −19.9% control, rate −0.163). Those are deep, material, and still negative:
  free insurance on the concentrated large-cap book is a measurement, not a rounding error.
- The intuition "small denominator ⇒ inflated |price|" is panel-specific:
  ρ(|rate|, dMaxDD as % of ctl) = **+0.392 u56, +0.143 broad, −0.412 small**, pooled −0.081.

## 3. R2 CONFIRMED — the removed rows are the coin flips (the one real argument for the floor)

For the 202 full-window published prices, compare the same arm's IS and OOS price:

| group | n | IS→OOS price-sign agreement | median \|rate_OOS − rate_IS\| | IS dMaxDD > 0 |
|---|---|---|---|---|
| kept by REL(0.10) | 149 | **88.4%** | **0.891** | 79.9% |
| removed by REL(0.10) | 53 | **49.1%** | 2.701 | 54.7% |

A removed price is a fair coin on whether it will even have the same sign out of sample; a
kept price replicates its sign 9 times in 10 and moves a third as much. This is the whole
case for the clause, and it is the case idea 94's absolute floor cannot make.

## 4. R3 CONFIRMED but in the wrong direction — the floor does not rescue idea 97's sentence

C1 gate < lever, C2 lever < DD rule, C3 DD rule < stop. Clause-rows true (18 cells × 3
windows = 54 rows per clause):

| window | C1 ABS → REL | C2 ABS → REL | C3 ABS → REL | exact order ABS → REL |
|---|---|---|---|---|
| full | 14/18 → **10/18** | 13/18 → 13/18 | 18/18 → 18/18 | 11/18 → 9/18 |
| IS | 5/18 → 4/18 | 16/18 → 16/18 | 15/18 → **16/16** | 2/18 → 3/18 |
| OOS | 14/18 → **10/18** | 9/18 → 9/18 | 17/18 → 18/18 | 7/18 → 4/18 |
| **all** | **33/54 → 24/54** | 38/54 → 38/54 | 50/54 → 52/52 | 20/54 → 16/54 |

15 clause-truth flips plus one order-only change. Two readings, both against the sentence:

1. **C1 gets worse, and the losses are all V1u.** Every C1 flip is `broad/V1u` (10 and 25 bps,
   full and OOS) or `small/V1u`: the gate tier looked cheaper than simply holding less only
   because of rows whose denominator is under a tenth of the book's own drawdown. Small-panel
   C1 goes 2/6 → **0/6** full and 2/6 → 0/6 OOS: idea 97's panel inversion is *stronger*, not
   weaker, once the shallow rows go. Median small-panel gate tier price 0.350 → **0.551**
   against a 0.279 lever.
2. **C3 becomes true by unmeasurability, not by price.** T4 keeps 2 of 23 rows, and idea 97's
   pre-registered convention ranks an unpriceable tier last, so "the stop is dearest" turns
   into "the stop buys nothing you can measure". Anyone quoting C3 under a relative floor is
   quoting a definition.

## 5. Rule 8 walk-forward — R4 REFUTED, the floor must not choose

Eligibility on 2009/2011–2016 only, 2017–2026 untouched. S1 = idea 94's selector (IS
dMaxDD ≥ 1.0 pp, argmin IS rate); Srel(φ) = the same argmin under the IS relative floor.
Means over the 18 cells:

| selector | picks | changed vs S1 | mean regret | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|
| **S1 (idea 94)** | 18 | — | **0.441** | 8.2% | **0.729** | −21.3% |
| Srel(0.00) | 18 | 7 | 0.742 | 8.9% | 0.731 | −22.7% |
| Srel(0.02) | 18 | **0** | 0.441 | 8.2% | 0.729 | −21.3% |
| Srel(0.05) | 18 | **0** | 0.441 | 8.2% | 0.729 | −21.3% |
| **Srel(0.10)** | 18 | 2 | 0.602 | 7.9% | **0.710** | −20.5% |
| Srel(0.20) | 14 (4 cells empty) | 5 | 0.871 | 6.1% | 0.625 | −19.2% |
| control (no instrument) | 18 | — | — | 10.6% | 0.762 | −27.4% |
| RULES v1 OOS | — | — | — | 7.7 / 5.9 / 7.9% | 0.747 / 0.576 / 0.581 | −13.8 / −21.2 / −32.8% |
| SPY OOS | — | — | — | 15.45% | 0.882 | −33.7% |

The two picks REL(0.10) changes are `broad/EWall@10` (stop25 → vol60-dg, OOS Sharpe
1.095 → 1.122) and `small/V1u@25` (g200-rw → ebud-0.20, **0.304 → −0.076**); net −0.019 of
mean OOS Sharpe and +0.161 of mean regret. At φ = 0.20 four of 18 cells have **no eligible
arm at all**. Same verdict as idea 122's sign test, reached by an independent screen: an
IS-computed admissibility rule on this price axis is at best inert and at worst a
value-destroying chooser. **Report-only.**

Note that no selector beats the no-instrument control (0.762) and none beats SPY (0.882) on
OOS Sharpe — the ranking of drawdown instruments is a measurement exercise, not a book.

## 6. KEEP paths (PROTOCOL rule 4) — R5, nothing new

All 306 arm-points carry 4a/4b flags identical to idea 97's (306/306): **97 pass 4a, 29 pass
4b**, every one of them an arm ideas 94/97 already published (gated `TOP20`/`EWall` books on
u56 and broad, e.g. `u56/TOP20 band3-dg` 14.4% / 1.157 / −19.8%, OOS Sharpe 1.189). This run
produces **no new KEEP candidate on either path** and is not proposing a book: the object on
trial is a publication rule. S1's picks pass 4a in 5 of 18 cells and 4b in 4; Srel(0.10)'s in
6 and 5.

## What PROTOCOL should take

A report-only clause, proposed in `…_C.memo.md`: quote **dMaxDD as a percentage of the
control's own |MaxDD|** next to every price, and mark a price whose denominator is under 10%
of it as **not interpretable** — because those are exactly the prices that fail to keep their
sign out of sample (49% vs 88%). The clause must not be used to select (§5), must not be
back-applied to the tier sentence as a rescue (§4), and does not license calling a deep
negative price an artefact (§2).

**Caveats.** Survivorship: all three panels are current-constituent lists; the small panel's
bias is the worst and falls on beaten-down names, the cohort a gate excludes, so small-panel
gate prices are flattered. The calendar-day index (open idea 38) is unfixed for u56/broad and
affects control and arm equally inside every cell. The full and OOS windows share their
deepest drawdown (2020), so a row's admissibility is often identical in the two — the
independent windows here are IS vs OOS, which is how §3 is measured.

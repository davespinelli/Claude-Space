# Idea 1538 (lane C, 2026-09-19) — is EXPOSURE-STATE DISAGREEMENT the THIRD LADDER AXIS, and is TWO NUMBERS ENOUGH?

**VERDICT: KILL the "two numbers are enough" hypothesis — T1, T4 and T5 all FAIL — while CONFIRMING
that `flat_one` is a real, ladder-independent axis. One incidental KEEP-4b candidate falls out.**

Script `research/backtests/2026-09-19_exposure-state-disagreement-third-ladder-axis_C.py`.
351 cells (3 panels x [36 rungs + 27 adjacent pairs x 3 blend weights]), every one published.
Two tuned parameters only: blend weight lambda {0.25, 0.50, 0.75} and overlap statistic
{OV_HOLD, OV_CAP}. All 14 gates PASS. 38s, offline, deterministic.

---

## 0. THE BUILD GATE — the precondition idea 1538 was filed on

Idea 1530's post-hoc `flat_one` fit was measured on 78 pairs of which only ONE ladder carried any
`flat_one` at all (L_S the trailing stop, mean 0.3190; L_C 0.0015; the other six EXACTLY 0.0000).
This run built the axis into **three independent mechanisms** and measured it (mean `flat_one` at
lambda = 0.50):

| ladder | mechanism | B136 | SMALL | U56 | max |
|---|---|---|---|---|---|
| L_S | own-equity drawdown stop | 0.3306 | 0.3209 | 0.3055 | 0.5546 |
| L_M | SPY price vs its own MA {None,200,150,100} | 0.0916 | 0.0823 | 0.0916 | 0.1740 |
| L_R | cross-sectional breadth {None,0.35,0.50,0.65} | 0.0896 | 0.2370 | 0.0875 | 0.3482 |
| L_X | **MAXVOL {0.60,0.12,0.08,0.06}** | 0.0101 | 0.0017 | 0.0054 | 0.0247 |
| L_G / L_N / L_H / L_B | gross / N / min-hold / band | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| L_C | cadence | 0.0000 | 0.0046 | 0.0000 | 0.0107 |

**G11 PASSES** on L_S, L_M and L_R, so the re-fit is a genuine three-mechanism fit and not 1530's
single-ladder fit again.

**THE THIRD ROUTE IDEA 1538 PROPOSED DOES NOT BUILD, AND IS PUBLISHED AS A NEGATIVE.** 1538 named
"a MAXVOL rung coarse enough to empty the book". It cannot be built off this incumbent: the
min-hold H = 126 **retains a held name regardless of its eligibility**, so tightening the ceiling
SHRINKS the book without EMPTYING it. On U56 the eligible SET is empty on 0.0% of days at m = 0.15,
1.0% at 0.12 and 2.5% at 0.10, while the BOOK is flat on **0.00%** of days at every m down to 0.10
and only 1.39% at m = 0.08 and 0.06. L_X is carried at all four rungs anyway so the record owns the
measurement: max mean `flat_one` **0.0101**, a factor of 30 below L_S. **MAXVOL is an eligibility
dial, not an exposure-state dial.**

---

## 1. THE RE-FIT — flat_one survives as an axis, but two numbers do NOT reach the bar

Pooled OLS over all 81 pairs at lambda = 0.50, y = `D_sharpe`, x1 = 1 - OV, x2 = `flat_one`:

| stat | ONE number R^2 | TWO numbers R^2 | + ladder identity | dR^2 | worst ladder residual |
|---|---|---|---|---|---|
| OV_HOLD | **0.0011** | **0.5460** | 0.5698 | **+0.0238** | L_R t -1.25 |
| OV_CAP  | **0.0891** | **0.5435** | 0.5694 | **+0.0259** | L_R t -1.06 |

*(1530 committed: one number 0.0154 / 0.1117, two numbers 0.6094 / 0.6066, dR^2 +0.0053 / +0.0079.)*

- **T1 R^2 >= 0.80: FAIL on both statistics (0.5460 / 0.5435).** And note the direction: measured on
  three mechanisms instead of one, the two-number fit is **WORSE than 1530's 0.6094**, not better.
  1530's figure was flattered by being fitted on the single ladder it was describing.
- **T2 dR^2 < 0.05: PASS on both (+0.0238 / +0.0259).** This is the run's positive finding and it is
  stronger than 1530's, because there are now nine ladders and three flat mechanisms for identity to
  explain: **whatever the two numbers explain, they explain the same way on every ladder.**
  `flat_one` is not a description of the stop.
- **T3 no ladder |t| > 2: PASS** (worst L_R, t -1.25 / -1.06).
- Fitted coefficient on `flat_one` **+0.3973** (OV_HOLD): a pair that disagrees about being invested
  on 10% of days opens ~0.040 of Sharpe of blend gap, against ~0.0070 for a 10-point drop in overlap.
  **The exposure-state axis is ~5.6x the overlap axis per unit.**

## 2. T4 LEAVE-ONE-LADDER-OUT — the test 1530 could not run, and the one that kills the rule

Fit the two numbers on the OTHER EIGHT ladders, predict the held-out one (R^2 against the held-out
ladder's own mean; it can go negative).

| held out | OV_HOLD, TWO numbers | (ONE number) | mean abs D |
|---|---|---|---|
| **L_S** own-equity DD | **+0.1075** | -0.5161 | 0.1252 |
| **L_M** SPY vs MA | **+0.7652** | -0.3410 | 0.0225 |
| **L_R** breadth | **-32.2242** | -0.9114 | 0.0258 |
| L_X MAXVOL | -0.5746 | -3.0781 | 0.0504 |
| L_G gross | -38595.87 | -307965.57 | 0.0001 |
| L_N / L_H / L_C / L_B | -1.95 / -0.19 / -8.55 / -7.76 | -13.94 / -6.07 / -7.99 / -139.19 | <= 0.016 |

**T4 (>= 0.50 on each flat ladder): FAIL.** OV_CAP is the same story (+0.1358 / +0.7631 / -30.85).
The rule transfers to the SPY macro gate and to nothing else. The breadth ladder is mispriced by a
factor of thirty: two rungs that disagree about being invested on 9% of days for a BREADTH reason do
not open the gap that two rungs disagreeing for a STOP reason open. **"Days flat apart" is not one
number — the REASON the books are apart is load-bearing, and a third regressor is needed.**
The huge negative R^2 values on the non-flat ladders are the honest arithmetic of dividing by a
near-zero variance (mean |D| = 0.0001 on L_G), not a second failure; they say only that those
ladders' gaps are too small to be predicted by anything.

## 3. T5 RULE 8 ON THE RULE ITSELF — the rule generalises across TIME far better than across LADDERS

Coefficients fit on the IS gaps (warm-up..2016-12-31) with IS-window overlaps and IS-window
`flat_one`; the 2017-2026 gaps read ONCE.

| stat | IS R^2 (two) | **OOS R^2 (two)** | IS R^2 (one) | OOS R^2 (one) |
|---|---|---|---|---|
| OV_HOLD | 0.2031 | **+0.7317** | 0.0754 | **-0.0398** |
| OV_CAP | 0.1608 | **+0.7284** | 0.0675 | **+0.1461** |

**T5 (>= 0.80): FAIL, but narrowly and in a way that favours the axis** — the two-number rule fitted
on pre-2017 data alone explains **73%** of the 2017-2026 blend gaps, where the one-number rule
explains **none** (-0.04). The temporal generalisation is real; the cross-ladder generalisation is
not. That asymmetry is the finding.

**TWO NUMBERS ENOUGH: FALSE on both overlap statistics (T1 F, T2 P, T3 P, T4 F, T5 F).**

---

## 4. BOTH KEEP PATHS AT ALL 351 CELLS

- **Path 4a: 0/351 full and 0/351 OOS.** No cell on any of the nine ladders beats the live RULES v2
  book on both halves. Consistent with 1530 (0/336) and 710 (0/495).
- **Path 4b: 71/351 full, 74/351 OOS, 67/351 BOTH.** Concentrated in the two NEW macro gates —
  L_M 19, L_R 15, then L_G 8, L_S 7, L_N 6, L_B 5, L_H 3, L_X 2, L_C 2.
- Per panel (BOTH): U56 53/117, B136 14/117, **SMALL 0/117**. SMALL's binding legs are H1 (13/117
  full) and CAGR (5/117 full, 0/117 OOS), as in every prior run on that panel.

## 5. RULE 8 CAPITAL ARM — the primary chooser LOSES, one restricted chooser reaches a 4b pass

| panel | chooser | cell | OOS CAGR/Sharpe/MaxDD | 4b OOS |
|---|---|---|---|---|
| U56 | ARGMAX-IS (all 117) | L_X blend 0.08\|0.06 @0.75 | 4.11% / 0.6503 / -18.17% | False |
| U56 | ARGMAX-IS (flat ladders) | **L_M blend None\|200 @0.75** | **16.48% / 1.2250 / -18.05%** | **True** |
| U56 | DO NOTHING (incumbent) | — | 17.32% / 1.1857 / -19.13% | True |
| B136 | ARGMAX-IS (all 117) | L_B=0.1 | 20.02% / 1.1502 / -25.29% | False |
| B136 | ARGMAX-IS (flat ladders) | **L_M blend None\|200 @0.50** | 14.29% / 1.0250 / -16.73% | **True** |
| B136 | DO NOTHING | — | 16.19% / 1.0180 / -20.74% | False |
| SMALL | ARGMAX-IS (all 117) | L_X blend 0.08\|0.06 @0.75 | 6.86% / 0.4760 / -42.68% | False |
| SMALL | ARGMAX-IS (flat ladders) | L_R=0.5 | -0.48% / 0.0213 / -32.46% | False |
| SMALL | DO NOTHING | — | 6.70% / 0.4398 / -36.51% | False |

**MEAN OOS SHARPE: chooser 0.7588 vs DO NOTHING 0.8812 — DOING NOTHING WINS.** The unrestricted
argmax-IS chooser is wrecked on two of three panels by L_X's extreme MAXVOL rungs, whose tiny books
post the highest IS Sharpe in the run (U56 1.3176, SMALL 2.0234) and then collapse OOS (0.6503,
0.4760). That is the cost of putting an unbuildable ladder on the grid, and it is reported, not
hidden.

## 6. THE INCIDENTAL KEEP-4b CANDIDATE (memo: `.memo.md`)

**U56, L_M blend None|200 @ lambda = 0.75** — algebraically a TWO-STATE GROSS, because both sleeves
share one selection frame: gross 0.75 when SPY > its 200d MA, **0.5625** when below.

| | CAGR | Sharpe | MaxDD | H1 / H2 |
|---|---|---|---|---|
| candidate FULL | 14.92% | **1.1788** | **-18.05%** | 1.2196 / 1.1532 |
| candidate OOS | 16.48% | **1.2250** | **-18.05%** | — |
| frozen incumbent FULL | 15.80% | 1.1537 | -19.13% | 1.2067 / 1.1203 |
| frozen incumbent OOS | 17.32% | 1.1857 | -19.13% | — |
| SPY OOS | 15.26% | 0.8738 | -33.72% | — |
| RULES v2 OOS | 9.46% | 1.2769 | -12.05% | — |

4b PASS full AND OOS; beats the frozen anchor on BOTH Sharpes with a shallower drawdown; turnover
3.24x/yr, charged. On B136 the same cell at lambda = 0.50 also passes 4b full and OOS where the
**anchor fails both** (1.0822/-17.81% vs 1.0654/-20.74%).

**THE HONEST LIMITS, STATED AS LOUDLY AS THE PASS.** (i) It is **1 of 3 choosers**, and the chooser
that reaches it restricts the pool to the three flat ladders — a pool restriction is itself a
choice, even though it reads no OOS row. (ii) The OOS Sharpe contrast against the anchor is
**+0.0393, t = +1.06** (paired circular-block bootstrap, L = 65, 400 reps) — **not significant**,
exactly the regime idea 1511 measured. (iii) **Path 4a is FALSE**: it does not beat live RULES v2.
(iv) On SMALL it fails 4b on both windows. **NOT proposed for enactment**; PROTOCOL rule 6 gives the
Sunday review that call.

---

## GATES — 14/14 PASS

G0 sample 16.7y min (U56/B136 18.7y, SMALL 16.7y). **G1 cross-script replay of the committed 2026-09-04 U56 anchor: max |dev|
3.72e-05** (15.80%/1.1537/-19.13% full, 1.1857 OOS). G2 anchor bit-identical on all 9 ladders
(max |dret| 0.0). G3 351/351 cells published. G4 exactly two tuned parameters. G5 the chooser reads
no row on or after 2017-01-01. G6 no leverage (max realised weight sum 1.000000). G7 idea 1509's
mechanism replayed (gross blend == single intermediate rung, max |dSharpe| 0.0). G8 netted blend
turnover <= naive + split-restoration at every row, 0 violations of 243 blends. G9 the stop, the SPY
macro gate and the breadth gate are NON-ANTICIPATING (truncated-tape replay bit-identical).
G10 deterministic recompute. **G11 the build gate PASSES.** **G12 the enactable TWO-STATE GROSS
wording of the incidental candidate (gross 0.75 above SPY's 200d MA, lambda*0.75 below) reproduces
the two-sleeve blend to max |dSharpe| 0.0002 over all 3 lambdas x 3 panels** — so the RULES wording
in the memo is the measured book, not a paraphrase of it (U56 lambda = 0.75: two-state 14.91% /
1.1790 / -18.02% full, 16.47% / 1.2252 / -18.02% OOS, against the blend's 14.92% / 1.1788 /
-18.05% and 16.48% / 1.2250 / -18.05%).

**SURVIVORSHIP (rule 9):** U56 and B136 are CURRENT-constituent lists and SMALL a CURRENT sub-$2B
screen carried back to 2008/2010, so every ABSOLUTE level above is an UPPER BOUND. What the fit
reads is a CONTRAST between a blend and its own two rungs over the SAME names on the SAME days,
which the bias cannot manufacture; the capital arm's levels carry the bias in full.

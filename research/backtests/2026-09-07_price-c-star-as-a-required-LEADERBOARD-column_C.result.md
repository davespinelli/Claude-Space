# Idea 356 — price-c*-as-a-required-LEADERBOARD-column (lane C, 2026-09-07)

**SPLIT. The measurement survives; the mandate does not.** c* is *exactly* measurable — the
record's own 5-bps ladder reproduces the bisection value to a maximum of **0.0022 bps** over
42 cells, so every c* the record has published is a real number, not a ladder artefact. But
the queue's proposal — make c* a mandatory column with a floor, "c* < 15 bps is not a capital
claim" — is **KILLED on its own terms**: c* is *not knowable in advance*
(spearman(c\*_IS, c\*_OOS) = **+0.077**), the floor rule scores **below the majority base rate
at every F** (accuracy 0.57–0.62 vs base 0.71–0.79, lift −0.14 to −0.17), the column is
degenerate (0 or "never" on **33 of 42** cells), and applied as a rule-8 screen it changes
**0 of 14** picks at the anchor rung and 1 of 14 overall — for **−0.033** OOS Sharpe.

Script: `research/backtests/2026-09-07_price-c-star-as-a-required-LEADERBOARD-column_C.py`
Console: `…_C.console.txt` · `…_C.cstar.csv` (42) · `…_C.keeppaths.csv` (42) ·
`…_C.walkforward.csv` (140) · `…_C.floors.csv` (6)

## Design (pre-registered before anything was read)

A proposal to change what the record *must* report is only as good as the statistic it
mandates, so three gates were fixed in the docstring first:

- **C1 MEASURABLE** — |c\*(5-bps ladder) − c\*(exact)| ≤ 2.0 bps on ≥ 90% of cells, and the
  4b pass set must be an interval (a book that fails at c and passes again at c+h has no c\*).
- **C2 PREDICTIVE** — c\*_IS (2009–2016 only) must classify c\*_OOS (2017–2026) against the
  floor at accuracy strictly above the majority-class base rate.
- **C3 USEFUL** — a rule-8 chooser screening on c\*_IS ≥ F must not *lower* mean OOS Sharpe
  against the record's plain best-IS-Sharpe chooser at the 10-bps anchor.

**Two tuned parameters, all 30 points reported:** ladder step `h ∈ {5.0, 2.5, 1.0, 0.5, 0.25}`
bps × reporting floor `F ∈ {0, 5, 10, 15, 20, 25}` bps. The menu is idea 352's, verbatim and
fixed — 7 books × 3 cadences {W,M,Q} × 2 panels (U56, B136) = **42 cells**. Cadence is *not*
a tuned parameter here: it is part of the fixed rule-8 menu the choosers pick over.

Three c\* per cell, all from one zero-cost run: `c*_full` (5 bars, whole sample — the record's
published column), `c*_IS` (4 bars on 2009–2016, what a reporter could have known in 2016; no
OOS bar because it did not exist yet), `c*_OOS` (the same 4 bars on 2017–2026).

**Gates passed before any result was read:** cost identity `r_c = r_0 − turnover·c/1e4` vs
`engine.backtest` at 10 bps, **max|diff| = 0.000e+00** on all 42 cells; the numpy metrics used
for the fine ladder vs `engine.metrics`, **0.000e+00** on the same 42 series; and c\*(h=5)
against idea 352's committed `.breakeven.csv`, **max|diff| = 3.553e-15** on 42/42 rows.

## 1. C1 — the ladder step (param 1): PASS, decisively

| estimator | MAE vs exact | max | cells off by > 2 bps |
|---|---|---|---|
| h = 5.0 (the record's own) | 0.0002 bps | **0.0022** | 0/37 |
| h = 2.5 | 0.0000 | 0.0007 | 0/37 |
| h = 1.0 | 0.0000 | 0.0001 | 0/37 |
| h = 0.5 / 0.25 | 0.0000 | 0.0000 | 0/37 |

100% of comparable cells inside the 2-bps gate; **0 of 126 (cell × window) points revive**
above their crossing, so the 4b pass set is an interval and c\* is well defined. The record's
published c\* numbers — the 1.0-to-43.5-bps spread the queue cites — are correct as measured.
**Refining the ladder is wasted work: h = 5 bps is already exact to two thousandths of a bp.**

## 2. C2 — the floor (param 2): FAIL, and it fails backwards

The standing weekly cells, in-sample vs out-of-sample:

| panel/book | T/yr | c\*_full | c\*_IS | c\*_OOS |
|---|---|---|---|---|
| U56/N20 | 9.62 | 24.66 | **0.54** | **42.90** |
| U56/F085 | 9.58 | 16.24 | 6.19 | 24.33 |
| U56/BAND12 | 1.93 | never | never | never |
| U56/BRCASH | 9.72 | 23.32 | **2.26** | **39.64** |
| U56/RULESv2 | 1.77 | 0.00 | 0.00 | 0.00 |
| B136/N20 | 13.75 | 7.68 | 0.00 | 3.00 |
| B136/F085 | 9.51 | 14.82 | 12.98 | 13.59 |
| B136/BAND12 | 2.06 | 0.00 | never | 0.00 |
| B136/BRCASH | 13.41 | 11.50 | 0.00 | 9.21 |
| B136/RULESv2 | 2.01 | 0.00 | 0.00 | 0.00 |

`spearman(c*_IS, c*_OOS) = +0.077` over all 42 cells (+0.152 over the 30 standing ones). The
two books whose cost robustness was *best* out of sample — U56/N20 (42.9 bps) and U56/BRCASH
(39.6 bps) — are precisely the two a 2016 reporter would have struck at F = 15 (c\*_IS 0.54
and 2.26). Confusion of the floor rule, predicting c\*_OOS ≥ F from c\*_IS ≥ F:

| F | TP | FP | FN | TN | acc | base rate | lift | precision |
|---|---|---|---|---|---|---|---|---|
| 5 | 7 | 13 | 5 | 17 | 0.57 | 0.71 | −0.14 | 0.35 |
| 10 | 6 | 13 | 5 | 18 | 0.57 | 0.74 | −0.17 | 0.32 |
| **15** | 5 | 12 | 5 | 20 | **0.60** | **0.76** | **−0.17** | **0.29** |
| 20 | 5 | 12 | 5 | 20 | 0.60 | 0.76 | −0.17 | 0.29 |
| 25 | 5 | 12 | 4 | 21 | 0.62 | 0.79 | −0.17 | 0.29 |

**Beats the base rate at 0 of 6 floors.** Saying "no claim is a capital claim" unconditionally
is more accurate than applying the proposed screen, at every floor tested.

Two supporting facts. **Degeneracy:** c\*_full is exactly 0 on 28/42 cells and "never" on 5,
so it carries a finite non-zero number on **9/42 = 21%** of the menu — most of the record's
rows would get a column that says only "fails at zero cost". **The floor's bite:** at F = 15,
**6 of the 10** standing weekly claims are struck (U56/RULESv2, B136/N20, B136/F085,
B136/BAND12, B136/BRCASH, B136/RULESv2) — i.e. the entire broad panel plus the live book.

## 3. C3 / rule 8 — the screen changes nothing, then changes one thing for the worse

Choosers fitted on ≤ 2016, 2017– read once, both panels × 7 rungs = 14 decisions:

| rule | mean OOS Sharpe | OOS CAGR | OOS MaxDD | > anchor | > RULES v2 | > SPY | regret |
|---|---|---|---|---|---|---|---|
| S1 best IS Sharpe (record default) | 1.1301 | 15.10% | −22.83% | 14/14 | 1/14 | 14/14 | 0.1030 |
| S2 best IS Sharpe among IS-4b clearers | 1.1277 | 15.01% | −22.67% | 14/14 | 1/14 | 14/14 | 0.1053 |
| **S3_15 best IS Sharpe among c\*_IS ≥ 15** | **1.1277** | 15.01% | −22.67% | 14/14 | 1/14 | 14/14 | 0.1053 |
| S4 max c\*_IS | 1.1277 | 15.01% | −22.67% | 14/14 | 1/14 | 14/14 | 0.1053 |
| **S5 best IS Sharpe among T ≤ 6.2×** | **1.1992** | 14.33% | −20.96% | 14/14 | **7/14** | 14/14 | **0.0339** |
| anchor N20/W | 0.9599 | | | | | | |
| RULES v2/W | 1.1805 | | | | | | |
| SPY | 0.8820 | | | | | | |

At the 10-bps anchor every c\*-based chooser picks exactly what S1 picks (BAND12/W on U56,
N20/M on B136 → OOS 1.266 / 1.007, mean 1.1364, CAGR 15.41%, DD −22.76%), so **C3 passes
vacuously**: the floor changes **0 of 14** picks at F = 0 and **1 of 14** at every F ≥ 5, and
that one change costs **−0.0331** OOS Sharpe. A screen that never fires cannot be a mandatory
gate.

## 4. The by-product: the record already has the column it needs

The statistic the record *already publishes* beside every row — annual turnover — is what c\*
was reaching for, and it is stable where c\* is not: **spearman(turnover_IS, turnover_OOS) =
+0.994** against c\*'s +0.077. Used as the rule-8 screen (S5, idea 352's own published
T ≤ 6.2× budget) it lifts mean OOS Sharpe to **1.1992 vs S1's 1.1301**, cuts regret from
0.1030 to **0.0339**, and is the only chooser that beats the live RULES v2 book more than
once (7/14 vs 1/14). It picks U56/BAND12/W on **12 of 14** decisions — idea 352's PARKed
cost-robust cell, reached here by an ex-ante rule rather than by hindsight.

Note also why c\* looks turnover-shaped in the pooled record and is not:
`spearman(turnover, c*_full) = +0.640` over all 42 cells but **−0.733** over the 9 cells with
c\* > 0. The pooled sign is entirely the c\* = 0 mass (slow books that fail 4b on the DD cap
at zero cost). This is the same Simpson structure idea 354 is chartered to test on the
turnover ceiling, on a second grid.

## 5. Coverage — what a mandate would actually cost

Grep-derived at runtime so it cannot go stale: LEADERBOARD.md holds **2983** committed rows,
**1911** of which mention 4b (539 also say KEEP). This run could rebuild **5** books = 30
cells. A *mandatory* column would have to be back-filled on all 1911 rows by re-running each
parent script; nothing in the record automates that. The mandate's cost is ~1900 re-runs for
a statistic that is degenerate on 79% of cells and anti-predictive at every floor.

## Both KEEP paths

**4a: 0/42** at the anchor (nothing beats RULES v2 in both halves — the record's standing
result, reconfirmed on this grid). **4b: 12/42**, of which 10 also clear the queue's c\* ≥ 15
floor. **No new KEEP.** The one cell the ex-ante turnover screen keeps selecting, U56/BAND12/W
(14.02% / 1.226 / −19.42%, H1 1.261 / H2 1.205, OOS 1.266, c\* never inside 50 bps), is
already PARKed by idea 352 and is not re-proposed here.

## Recommendation to PROTOCOL (not applied — rules change only at Sunday review)

Do **not** mandate c\* or its floor. Keep publishing c\* where a parent already computes it,
as a descriptive number (C1 says it is exact), and if the record wants an ex-ante
capital-worthiness screen beside 4b, use **annual turnover against idea 352's T ≤ 6.2× budget**
— it is already in every row, is stable IS→OOS at +0.994, and is the only screen tested here
that improves the rule-8 chooser.

**SURVIVORSHIP:** universe.json (56) and universe_broad.json (136) are current-constituent
lists, so absolute CAGRs are optimistic on both panels. This run holds names, days, filter,
gross and fill fixed and moves only the cost rung, so the c\* comparisons across cells are far
less exposed than the levels are.

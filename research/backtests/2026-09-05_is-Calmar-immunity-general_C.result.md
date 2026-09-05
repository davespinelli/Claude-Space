# idea 141 — is-Calmar-immunity-general (lane C, 2026-09-05)

**VERDICT: KILL of the premise.** Idea 132's "100% / 100% / 57% / 29%" immunity is a property of
**one bar vector**, not of a selector class. Randomise the bar levels and **no selector is immune** —
K_Sharpe falls 1.000 → **0.634–0.789**, K_Calmar 1.000 → **0.641–0.793**. What survives, and is new,
is a **graded** version of the claim with a mechanism: immunity is bought by **rank-alignment with
the statistics the bars are written on**, not by being risk-adjusted. No rules change, no new book.

## Pre-checks (passed before any new number was read)
* Engine-equivalence on all three panels, 3 ungated books: **max|diff| = 0.000e+00**.
* Idea 132's corpus re-derived, not read: **306 of 306 rows**, max|diff| **2.2e-16** across
  CAGR/Sharpe/MaxDD/H1/H2/IS_*/OOS_*/gross, **0** `adm_S1` disagreements.
* Idea 132's four published immunity rates come back **exactly**: K_Sharpe 100%, K_Calmar 100%,
  K_CAGR 57%, K_MaxDD 29% (7 of 18 cells non-empty, median admitted 0 of 17).

## Corpus and grid
3 panels (u56/broad/small) × 3 books (V1u/TOP20/EWall) × 2 cost rungs (10, 25 bps) = 18 cells ×
17 arms = **306 backtests**, weekly, t+1. Two tuned parameters, both swept exhaustively:
**selector** (8 values — 5 risk-adjusted, 3 not) × **screen tightness qmax** (0.25/0.50/0.75/1.00)
= **32 grid points, all printed**, plus a `K_RANDOM` control. Each bar is drawn at a quantile
q ~ U(0, qmax) of that cell's own 17 arm values, so the screen keeps 4b's shape (IS_H1 > b1,
IS_H2 > b2, |IS_MaxDD| < bDD, IS_CAGR > bC) and loses its calibration. 4000 draws per (cell, qmax),
seed 20260905.

## (1) The premise is dead at the published point already
Extending idea 132's own table to eight selectors, at PROTOCOL's own bars:

| selector | class | immunity at published bars |
|---|---|---|
| K_Sharpe | RA | 100% |
| K_Calmar | RA | 100% |
| K_Sortino | RA | 100% |
| K_MinHalf | RA | 86% |
| K_CAGR | **NRA** | **57%** |
| K_H2Sharpe | **RA** | **43%** |
| K_MaxDD | NRA | 29% |
| K_NegVol | NRA | 0% |

An RA selector (K_H2Sharpe, 43%) sits **below** a non-RA one (K_CAGR, 57%). The class boundary
does not partition immunity even at the point idea 132 measured.

## (2) Under randomised bars nobody is immune — P1 FAILED
Pooled over 18 cells × 4000 draws, immunity = P(unscreened argmax admissible | admissible set
non-empty):

| selector | qmax 0.25 | 0.50 | 0.75 | 1.00 |
|---|---|---|---|---|
| K_Calmar | 0.793 | 0.657 | 0.641 | 0.676 |
| K_Sortino | 0.793 | 0.693 | 0.670 | 0.673 |
| K_Sharpe | 0.789 | 0.674 | 0.634 | 0.652 |
| K_MinHalf | 0.763 | 0.600 | 0.585 | 0.622 |
| K_CAGR | 0.723 | 0.555 | 0.530 | 0.512 |
| K_H2Sharpe | 0.650 | 0.480 | 0.507 | 0.549 |
| K_MaxDD | 0.407 | 0.239 | 0.201 | 0.233 |
| K_NegVol | 0.097 | 0.040 | 0.029 | 0.026 |
| *K_RANDOM (control)* | *0.573* | *0.340* | *0.214* | *0.163* |
| *size-matched null* | *0.573* | *0.343* | *0.215* | *0.162* |

The pre-registered bar for the premise was immunity ≥ 0.90 at every qmax; **K_Sharpe's minimum is
0.634 and K_Calmar's is 0.641**. Idea 132's 100% is what a screen looks like when it admits a
large, favourably-placed set — not immunity.

## (3) What survives: a large, graded, real lift — not immunity
Lift over the size-matched null (`K_RANDOM` reproduces the null to **0.0027**, P5 held, so the
null is trustworthy):

| selector | qmax 0.25 | 0.50 | 0.75 | 1.00 |
|---|---|---|---|---|
| K_Calmar | +0.220 | +0.314 | +0.426 | **+0.514** |
| K_Sortino | +0.220 | +0.350 | +0.455 | **+0.511** |
| K_Sharpe | +0.216 | +0.331 | +0.419 | **+0.491** |
| K_CAGR | +0.151 | +0.212 | +0.315 | +0.350 |
| K_MaxDD | −0.165 | −0.104 | −0.014 | +0.071 |
| K_NegVol | −0.475 | −0.303 | −0.186 | −0.135 |

At the tightest screen a risk-adjusted argmax is admissible **4.0–4.2× more often than chance**
(0.65–0.68 vs 0.162). The correct statement is *"IS-Sharpe and IS-Calmar argmaxes are unusually
screen-robust"*, not *"immune"*, and it is a **quantity**, so it can be compared, not asserted.

## (4) The mechanism: alignment, not class — P4 HELD, P2 HELD
Mean rank-correlation of each selector's statistic with the four bar statistics, across 17 arms ×
18 cells; `rho_min` is the weakest of the four:

| selector | ρ(IS_H1) | ρ(IS_H2) | ρ(IS_MaxDD) | ρ(IS_CAGR) | **ρ_min** | immunity @1.00 |
|---|---|---|---|---|---|---|
| K_Calmar | +0.654 | +0.653 | −0.011 | +0.758 | **−0.056** | 0.676 |
| K_Sharpe | +0.794 | +0.657 | −0.119 | +0.788 | **−0.146** | 0.652 |
| K_Sortino | +0.785 | +0.687 | −0.209 | +0.862 | **−0.218** | 0.673 |
| K_H2Sharpe | +0.341 | +1.000 | −0.171 | +0.717 | **−0.214** | 0.549 |
| K_MinHalf | +0.544 | +0.797 | −0.319 | +0.757 | **−0.361** | 0.622 |
| K_CAGR | +0.622 | +0.717 | −0.433 | +1.000 | **−0.433** | 0.512 |
| K_MaxDD | −0.188 | −0.171 | +1.000 | −0.433 | **−0.499** | 0.233 |
| K_NegVol | −0.343 | −0.522 | +0.605 | −0.773 | **−0.785** | 0.026 |

**Spearman(ρ_min, immunity) = +0.881** across the 8 selectors (ρ_mean +0.833) — P4's bar was +0.70.
Alignment orders the selectors *across* the RA/NRA boundary: K_CAGR (ρ_min −0.433) outranks the RA
selector K_H2Sharpe at three of four qmax values, and the boundary is broken at **3 of 4** qmax
(P2 held). Explanation **(D) co-monotonicity** beats **(C) class property**.

**What actually excludes a risk-adjusted argmax is 4b's DRAWDOWN cap.** Exclusion attribution at
qmax=1.00: K_Calmar/K_Sortino/K_Sharpe are cut by the DD bar in 0.39–0.55 of exclusions, while
K_MaxDD and K_NegVol are cut by the CAGR bar in 0.88 and 0.93. Every RA selector's single weakest
alignment is with `IS_MaxDD` — that is the whole of the residual vulnerability.

## (5) P3 FAILED, reported as found
Immunity is **not** monotone in qmax for any selector except K_CAGR, K_NegVol and K_RANDOM: it
falls to qmax=0.75 and rises again at 1.00 (K_Sharpe 0.789 → 0.674 → 0.634 → 0.652). The cause is
the conditioning, not a reversal: at qmax=1.00 only **42.5%** of draws leave a non-empty set
(vs 100% at 0.25), and conditioning on non-emptiness selects the looser draws. The **lift** over
the size-matched null, which is not distorted by that conditioning, *is* monotone for all six
informative selectors. The lift, not the raw rate, is the statistic to quote.

## (6) Rule-8 walk-forward — the selector question is OOS-immaterial
Screens and selectors read 2009–2016 only; OOS 2017–2026 read once; FALLBACK convention (a screen
admitting nothing holds the cell's ungated control). Means over 18 cells × 4000 draws:

| | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|
| best selector at any qmax (K_H2Sharpe, 0.25) | 9.8% | **0.773** | −25.2% |
| K_Sharpe (0.25 / 1.00) | 9.4% / 10.1% | 0.724 / 0.749 | −24.2% / −26.0% |
| K_Calmar (0.25 / 1.00) | 9.9% / 10.2% | 0.745 / 0.750 | −24.9% / −26.0% |
| worst selector (K_NegVol, 0.25) | 7.1% | 0.698 | −19.3% |
| **K_RANDOM control** | 9.3–10.2% | **0.738–0.753** | −24.4% to −26.1% |
| ungated control (no screen) | **10.65%** | **0.762** | −27.4% |
| RULES v1 (live book) | 4.86% | 0.451 | −25.3% |
| **SPY** | **15.45%** | **0.882** | −33.7% |

The whole 8-selector × 4-tightness grid spans **0.698–0.773** OOS Sharpe, and a **random** selector
lands at 0.738–0.753 — inside the pack, above five of eight selectors at qmax=1.00. Under
PROTOCOL's own published bars the eight selectors span **0.743–0.760**, i.e. **0.017**. Every one
loses to SPY (0.882) and none beats the do-nothing ungated control (0.762) by more than 0.011.
Whatever immunity is or is not, choosing among these selectors is worth nothing out of sample.

## KEEP paths
248 distinct arms are picked by some selector at some qmax. Full sample: **82 pass 4a**, **28 pass
4b**; on the OOS window alone **30 pass 4b**. Every one is a pre-existing leaderboard book. **No
KEEP on either path** — this run selects among existing arms and cannot promote a book.

## Predictions, scored
* **P0** reproduction — **HELD** (306/306 to 2.2e-16; four published rates exact).
* **P1** K_Sharpe and K_Calmar keep immunity ≥ 0.90 with lift ≥ 0.10 at every qmax — **FAILED**
  (min immunity 0.634 / 0.641). The premise is killed.
* **P2** the RA/NRA boundary does not partition immunity — **HELD** (broken at 3 of 4 qmax).
* **P3** immunity non-increasing in qmax — **FAILED** (see §5; the lift is monotone, the rate is not).
* **P4** Spearman(ρ_min, immunity) ≥ +0.70 — **HELD** (+0.881).
* **P5** K_RANDOM tracks the analytic null within 0.05 — **HELD** (0.0027).

## What this says about idea 110
Idea 110 asks whether IS-Sharpe is the right rule-8 selector. This run says the question is
mis-framed twice over: the immunity that motivated it is **calibration, not structure** (§2), and
even at its most favourable reading the selector choice moves OOS Sharpe by **0.017** under the
published bars and **0.075** across the entire randomised grid, against a **0.120** gap to SPY (§6).
Idea 110 should be answered on OOS return, not on screen behaviour.

## Caveats
* Survivorship on all three current-constituent panels (idea 54); every CAGR here is optimistic and
  no level in this file is an achievable return.
* Idea 128: the IS window cannot express a deep drawdown, which biases the DD bar toward admitting
  too much — for every selector equally, so it does not explain the ordering in §4, but it does mean
  the DD bar's exclusion share in §4 is a **lower** bound.
* Idea 126: t+1 execution only.
* The randomised bars are drawn from each cell's own cross-arm distribution, which is what makes
  tightness comparable across cells. It also means they are not SPY-relative: this file measures
  the screen's **shape**, not 4b's economic content.

Script: `2026-09-05_is-Calmar-immunity-general_C.py` · console: `.console.txt` ·
data: `.grid.csv`, `.cells.csv`, `.immunity.csv`, `.alignment.csv`, `.walkforward.csv`

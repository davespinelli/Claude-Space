# Idea 319 — is-the-narrow-day-effect-ORDERING-the-same-panel-ordering-as-the-gate-premium
lane B, 2026-09-09 · `2026-09-09_is-the-narrow-day-effect-ORDERING-the-same-panel-ordering-as-the-gate-premium_B.py`

## Verdict: **KILL of the coincidence as evidence — and of the CONC ladder as a measurement**

The queue asked whether one panel characteristic prices BOTH orderings or whether the
agreement is two three-point ladders. **It is two three-point ladders, and one of them is
not even a ladder: the narrow-day concentration effect is statistically indistinguishable
from zero on all three published panels.** Rules unchanged, no book promoted, no memo.

## Gates (run first, all PASS)
| gate | result |
|---|---|
| G1 vectorised runner vs `engine.backtest` on a CONC book | max\|dret\| **2.78e-17**, max\|dturn\| **5.55e-16** (2 ragged-left-edge NaN bars excluded, both inside the discarded 260-bar warm-up) |
| G2 idea 316's CONC anchors at the pinned (q=0.20, c=0.35) point | **2.57e-05** — 6.4870 / −0.1620 / −3.8471 reproduced exactly |
| G3 idea 312's GATE premia at (g=0.75, W) | **2.88e-07** — −0.03309 / −0.06533 / −0.17475 reproduced exactly |

By-product from G2: the queue's headline **+5.17 / −1.46 / −3.06** is the MEAN of idea 316's
16 (q, c) points, not a cell. At the pinned point the same table reads **+6.487 / −0.162 /
−3.847**. The ordering U56 > B136 > SMALL439 is identical at both readings, so the queue's
claim is intact at the exact books this run generalises.

## Design
Three panels cannot answer a "do two ladders agree" question, so the three points were
replaced by a population: **144 sub-panels** (k ∈ {20, 36, 50} × origin ∈ {U56, B136, SMALL,
POOL} × 12 seeds) plus the 3 real anchors, with **BOTH** statistics measured on **every**
one, at the same pinned dials (gross 0.75, weekly, 10 bps, t+1, MA200, vol20 < 0.60, scorer
off, n0 = 20, q = 0.20, c = 0.35), on one common window (2010-01-04 → 2026-09-04, 4,194 bars,
16.6 yr). 588 books. Tuned parameters, exactly two: **k** and the **characteristic x**; all
3 × 6 = 18 cells reported.

## The three anchors, re-measured on the common window
| panel | GATE (Sharpe) | CONC (pp/yr) | CONC t | narrow days |
|---|---|---|---|---|
| U56 | −0.0172 | **+5.899 ± 4.763** | **+1.24** | 807 |
| B136 | −0.0437 | **+0.323 ± 5.248** | **+0.06** | 839 |
| SMALL439 | −0.1747 | **−4.229 ± 7.734** | **−0.55** | 671 |

Both ladders are monotone U56 > B136 > SMALL439 — the queue's premise is true. **And not one
of the three CONC numbers is two standard errors from zero.**

## H_COINC — HOLDS (the two ladders do not move together)
ρ(GATE, CONC) over the 144 draws: **Pearson −0.0162 / Spearman +0.0709** (bar |ρ| < 0.30).
Confound-free within-origin readings: U56 +0.322, B136 −0.044, SMALL −0.131, POOL −0.130 —
no consistent sign. IS +0.037 / OOS −0.002. The instruments are independent.

## THE TRIPLE TEST — what a three-point agreement is worth
20,000 random triples, asking how often the GATE ordering equals the CONC ordering:

| triple shape | same full order | same top-vs-bottom sign |
|---|---|---|
| any 3 draws | 0.1949 | 0.5356 |
| 1 each from U56 / B136 / SMALL (**the published shape**) | **0.2452** | 0.5944 |
| chance floor | 0.1667 | 0.5000 |

**The published coincidence recurs 24.5% of the time on composition luck alone.** It is worth
about 0.6 bits over a coin-shaped null — not evidence of a shared mechanism.

## H_ONECHAR — FAILS
OLS of each statistic on each characteristic over the draw population (all 18 cells in
`.fits.csv`; k = ALL shown):

| x | R² gate | R² conc | t gate | t conc |
|---|---|---|---|---|
| etf_share | 0.1674 | 0.0556 | +5.34 | +2.89 |
| breadth | 0.2345 | 0.0034 | +6.59 | +0.70 |
| cvol | 0.2208 | 0.0037 | −6.34 | −0.72 |
| mean_vol | 0.2249 | 0.0070 | −6.42 | −1.00 |
| rho_bar | 0.1392 | 0.0008 | +4.79 | +0.34 |
| small_share | 0.2777 | 0.0040 | −7.39 | −0.75 |

No characteristic clears the 0.50 bar on both (best: etf_share, min R² **0.0556**). The
asymmetry is the finding: **the GATE ladder has a weak but real characteristic reading
(R² 0.14–0.39, |t| 4.8–7.4, rising with k); the CONC ladder has none at all** — max R²
**0.072** anywhere in the grid, and 5 of 6 characteristics fail to reach |t| = 1.

Cheapness of "reproducing the ordering": fit on draws only, then evaluate at the real panels'
own x, and **three characteristics (etf_share, mean_vol, small_share) reproduce BOTH published
orderings** — while explaining 5.6%, 0.7% and 0.4% of CONC. Max residuals run 0.35–0.73 × the
published gap. Reproducing a 3-point ordering is nearly free; the R² is where the claim dies.

## H_NOISE — both ladders are inside their own composition noise
Within-cell seed sd as a multiple of that ladder's own published U56−SMALL439 gap
(GATE 0.0978, CONC 10.334):

- median **GATE 0.943×**, **CONC 0.529×** (bar 0.50); sd ≥ half the gap in **GATE 10/12**,
  **CONC 6/12** cells.
- Share of same-cell seed **pairs** differing by more than the WHOLE published gap:
  **GATE 42.7%, CONC 25.8%** (idea 312's test, reproduced on both instruments).

A second, independent noise source for CONC: it is a mean over ~600–850 narrow days and
carries its own sampling error at fixed composition. Pooled median |t| **0.81**; **|t| ≥ 2 on
8 of 144 draws (5.6%)** — exactly the false-positive rate of a null. By origin: U56 5.6%,
B136 0.0%, SMALL 11.1%, POOL 5.6%.

## Rule 8 walk-forward
**WF-A (on the answer):** slope sign held IS → OOS in **12/12** (x, stat) fits, but the GATE
fits' R² collapses by 4–9× (etf_share 0.314 → 0.034; small_share 0.391 → 0.089; cvol 0.360 →
0.058) and the CONC fits are noise in both windows (R²_IS ≤ 0.013, R²_OOS ≤ 0.057). The
co-movement statistic is +0.037 IS and −0.002 OOS.

**WF-B (on a book):** (arm, origin, k) chosen by IS Sharpe ≤ 2016-12-31, OOS 2017-01-01→ read
once. Pick **EWall / B136 / k=20**, IS Sharpe 1.0950 → **OOS CAGR 14.51%, Sharpe 1.0923,
MaxDD −25.0%**. Comparands OOS: RULES v2 **9.52% / 1.2834 / −12.1%**; SPY **15.45% / 0.8820 /
−33.7%**. The pick beats SPY's OOS Sharpe and loses its CAGR and its drawdown cap; it loses
outright to the live book on Sharpe. Cell books: **4a 0/12, 4b 0/12, BOTH 0/12**, 11 of 12
failing 4b on the DD leg alone.

## KEEP paths
**4a 0/588 · 4b 80/588 · BOTH 0/588.** Binding 4b legs across all books: H1,H2,OOS,DD,CAGR
229 · DD 122 · H1,H2,OOS,DD 41 · H2,OOS,DD 27.

4b is a KEEP path on its own, so the 80 passers were priced before being declined: **only
26/80 beat their own ungated EWall control** on the same sub-panel (idea 311's reading — a 4b
pass on a fixed-gross selection book is a dial placement, not an edge), and only **3 are
implementable** rather than a random draw:

| book | CAGR | Sharpe | MaxDD | H1/H2 | OOS Sharpe | 4a | beats own control |
|---|---|---|---|---|---|---|---|
| U56 / MA-RS | 11.01% | 1.0553 | −18.6% | 1.004/1.109 | 1.117 | False | False |
| U56 / NF20 | 12.79% | 1.0782 | −18.1% | 1.060/1.103 | 1.140 | False | True |
| B136 / MA-RS | 11.20% | 1.0450 | −20.1% | 1.105/1.004 | 1.066 | False | False |

All three are books the record already carries (MA-RS is idea 51's treatment, NF20 idea 2's
broad leg), all fail 4a against the live RULES v2, and this run measured them only as the
fixed instruments of a ladder question. **DECLINED: no memo, no promotion, no rule change.**

## What this says about the record
1. **The narrow-day concentration effect should not be quoted as a per-panel number.** Its
   own standard error is 4.8–7.7 pp/yr against point estimates of +5.9 / +0.3 / −4.2. Idea
   316's KILL is unaffected (it rested on signs across 48 points, episodes and rule 8, not on
   the magnitude) — but the ladder inside it is not a measurement, and idea 319's premise was
   built on reading it as one.
2. **A three-panel ordering agreement between two statistics is worth ~24% against a 17%
   floor.** It should not be cited as evidence for a shared mechanism anywhere in the record.
   This is the second instrument on which idea 312's noise-floor result reproduces.
3. **The two ladders are not the same fact.** GATE has a weak characteristic reading that
   survives IS → OOS in sign and collapses in R²; CONC has none. Whatever orders the gate
   premium across panels does not order the concentration effect.

## Honesty notes
- SURVIVORSHIP: `universe.json` (56) and `universe_broad.json` (136) are current-constituent
  lists; SMALL439 is the current constituents of a sub-$2B screen with the README's
  `max_1d_move ≥ 1.0` names dropped. Absolute CAGRs are optimistic on every panel and most on
  SMALL; `small_share` is reported as a characteristic precisely because idea 568 showed
  origin survives characteristic matching.
- SPY is a benchmark column only in the population (never drawn, never tradable), a
  deliberate deviation from idea 316's U56/B136 convention so the four origins are built
  identically. G2/G3 use the original convention, including SPY inside idea 316's rank
  denominator on SMALL439 — that detail alone moves the published SMALL439 CONC by 0.38 pp/yr.
- 2022 dominates U56's narrow state (idea 316) and sits inside the OOS window. The population
  result is the evidence; the three-panel anchors are description.
- The 4a comparand is the LIVE RULES v2 on U56 over this window (PROTOCOL 3's literal
  wording), one fixed comparand for all 588 books — the ambiguity queue idea 398 is about.

## Outputs
`.console.txt` `.gates.csv` `.panels.csv` `.books.csv` `.corr.csv` `.triples.csv` `.fits.csv`
`.predict.csv` `.noise.csv` `.straddle.csv` `.walkforward.csv` `.keeppaths.csv`

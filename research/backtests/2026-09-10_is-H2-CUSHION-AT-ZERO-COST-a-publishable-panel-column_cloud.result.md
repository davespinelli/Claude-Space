# Idea 411 — is H2 CUSHION AT ZERO COST a publishable panel column? (cloud, 2026-09-10)

**Verdict: SPLIT. The queue's CLAIM is right and its COLUMN is wrong. The zero-cost cushion does
out-predict turnover (AUC 0.8245 vs 0.7359 at 10 bps; rule-8 OOS AUC 0.9632 vs 0.6616) — but the
reason is stronger than the queue's, and it disqualifies turnover outright: 207 of 207 4b failures
at 10 bps ALREADY FAIL AT 0 BPS, so there is not one arm in 216 whose verdict the cost rung
decides. And H2 is not the leg that binds: the drawdown cap binds 142 of 216 arms and H2 only 35,
all of them on SMALL439. KILL of `H2CUSH0` as the publishable column; the publishable column is
`MINCUSH0` — and its AUC of 1.0000 is an identity, not a result. No RULES change, no book
promoted, no KEEP claimed; RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.
4a 0/648, 4b 24/648 (a known family — see below).**

Script `research/backtests/2026-09-10_is-H2-CUSHION-AT-ZERO-COST-a-publishable-panel-column_cloud.py`.
Artefacts: `.console.txt`, `.arms.csv` (648 arm-rows), `.screens.csv`, `.decomp.csv`, `.wf.csv`.

## Design

**216 arms, every one reported**: 3 panels (u56 / broad136 / small439) × 6 books (TOP5 / TOP10 /
TOP20 / TOP40 / EWALL / RULESv2) × 2 gross (0.75 / 1.00) × 2 cadences (W / M) × 3 lambdas
(1.00 / 0.50 / 0.25, idea 137's partial-rebalance dial), each priced at 0 / 10 / 25 bps = **648
arm-rows**. The two tuned parameters are the ones the question is about: **screen column** and
**threshold**; the arm menu is a reporting axis and nothing was selected on it.

### Gates — ALL PASS

| gate | result |
|---|---|
| G1 `fast_bt` vs `engine.backtest` at W and M, returns **and** turnover, 3 panels | max **6.41e-16 / 8.88e-16** |
| G2 cost-rung identity vs a live 25 bps run | max **6.41e-16** — load-bearing: it is the exact statement that a rung reaches a return series **only** through turnover, which is what makes turnover the incumbent column at all |
| G3 lambda = 1.0 is a strict no-op on the weights | **0.000e+00** on all three panels |
| G4 AUC machinery: outcome as its own predictor / 200 random permutations | **1.0000** / **0.4971** |

## A2 — a measured fact this run did not go looking for

**Idea 137's lambda dial is turnover-NON-monotone in 9 of 72 cells, and every one is a
variable-gross book** (8 RULESv2, 1 EWALL/M). The dial takes an EWMA of the target and then
restores the **raw** book's daily gross onto it; on a book whose gross moves day to day
(RULESv2's band sends names to cash) that re-gross step *manufactures* daily trading instead of
removing it. Measured: u56/RULESv2/g1.0/W runs **2.353 → 2.454 → 2.585 x/yr** as lambda falls
1.00 → 0.50 → 0.25, i.e. the dial **raises** turnover by up to **1.098x**. Ideas 137 and 412
measured the dial on fixed-gross books only. Reported here, not swept under a gate.

## B — the decomposition that decides the question

Every 4b failure splits into **LEVEL** (the arm already fails at 0 bps, so no cost column could
ever have saved it) and **COST** (passes at 0 bps, fails at the rung — the only failures turnover
can own).

| rung | arms failing 4b | LEVEL | COST |
|---|---|---|---|
| **10 bps** | 207 / 216 | **207 (100.0%)** | **0 (0.0%)** |
| 25 bps | 210 / 216 | 207 (98.6%) | 3 (1.4%) |

Per panel at 10 bps: u56 66 fail / 66 LEVEL / 0 COST (6 pass at 0 bps), broad 69 / 69 / 0 (3),
small 72 / 72 / 0 (0). **The 10 bps pass-set and the 0 bps pass-set are the same nine arms.**

This is the finding. Turnover is a perfectly good predictor of *cost*, and cost decides **zero**
of 216 verdicts at the PROTOCOL rung. A screening column built on turnover is answering a question
the data never asks.

## B2 — which 4b leg actually binds (argmin of the five margins, 10 bps)

| binding leg | arms | | by panel | CAGR | DD | H1 | H2 | OOS |
|---|---|---|---|---|---|---|---|---|
| **DD (drawdown cap)** | **142** | | broad | 9 | 63 | 0 | 0 | 0 |
| H2 | 35 | | small | 0 | 17 | 7 | **35** | 13 |
| CAGR | 19 | | u56 | 10 | 62 | 0 | 0 | 0 |
| OOS | 13 | | | | | | | |
| H1 | 7 | | | | | | | |

By book family the split is cleaner still: DD binds 110 of the 144 ranked/EWALL arms, while
**CAGR binds 19 of the 36 RULESv2 arms** — the same "the binding bar on the low-gross family is
the CAGR floor" that idea 442 reached from the cash-credit direction, reproduced here from the
margin side.

**H2 binds on exactly one panel (SMALL439) and nowhere else.** Idea 137's aside generalised a
SMALL-panel fact to a panel column. Median margins at 10 bps: u56 H1 +0.3005 / H2 +0.2558 /
OOS +0.2715 / **DD −0.0582** / CAGR +0.0712; broad +0.2758 / +0.1290 / +0.1568 / **−0.0869** /
+0.0815; small −0.1037 / **−0.2433** / −0.2230 / −0.1896 / +0.0337.

## C — the two columns as predictors (10 bps; TURNOVER sign-flipped so "more is better")

| column | AUC | rho vs 4b margin (pooled) | rho **within panel** | AUC u56 | AUC broad |
|---|---|---|---|---|---|
| **MINCUSH0** | **1.0000** | 0.9942 | 0.9571 | 1.0000 | 1.0000 |
| DDCUSH0 | 0.9206 | 0.7488 | 0.7164 | 0.9091 | 0.9179 |
| OOSCUSH0 | 0.9147 | 0.8564 | 0.4664 | 0.8914 | 0.9614 |
| **H2CUSH0** (the queue's column) | **0.8245** | 0.8077 | **0.3640** | 0.8586 | 0.6184 |
| **TURNOVER** (incumbent) | **0.7359** | 0.4019 | **0.3385** | 0.7121 | 0.6957 |
| H1CUSH0 | 0.5395 | 0.5516 | −0.1294 | 0.2348 | 0.4155 |
| CAGRCUSH0 | 0.1594 | −0.1943 | −0.5855 | 0.0909 | 0.0870 |

**MINCUSH0's 1.0000 is an identity being restated, not a result:** `MINCUSH0 > 0` *is* the 4b
predicate evaluated at 0 bps, and section B shows the 10 bps verdict set is identical to the 0 bps
one. It is printed because that identity is exactly the finding. (SMALL439 has zero passers, so
its AUC is undefined on every column — stated, not hidden.)

**The pooling caveat, applied to this run's own answer (idea 605's lesson).** H2CUSH0's headline
advantage over turnover is 0.8077 vs 0.4019 pooled but **0.3640 vs 0.3385 within panel** — a near
tie. Most of the cushion column's apparent edge is a *between-panel* level difference, which is
the artefact idea 605 was killed for. The 25 bps rung reads the same way (0.8169 / 0.4599 pooled,
0.2999 / 0.4829 within — where turnover actually wins).

## D — the screens (every column × every threshold, base rate 4.2%, no-screen F1 = 0.0800)

| column | best q | threshold | n predicted | precision | recall | **F1** |
|---|---|---|---|---|---|---|
| MINCUSH0 | 95 | −0.0065 | 11 | 0.8182 | 1.0000 | **0.9000** (identity) |
| H2CUSH0 | 90 | +0.3260 | 22 | 0.2273 | 0.5556 | **0.3226** |
| JOINT | 95 | 0.7847 | 11 | 0.2727 | 0.3333 | 0.3000 |
| TURNOVER | 35 | 3.2456 x/yr | 76 | 0.1184 | 1.0000 | **0.2118** |

The full 21-point ladder for every column is in `.screens.csv` and printed in `.console.txt`.
**The joint screen never beats the better single column** — 0.3000 against H2CUSH0's 0.3226 — so
neither column earns a place beside the other (H4: no).

## E — H3's three controls against the tautology charge

**(a) predicting a rung it was not measured at (25 bps):** H2CUSH0 AUC **0.9556**, turnover 0.7635.
**(b) OUT OF PANEL** (threshold chosen on one panel, applied to the other two), F1:

| chosen on | H2CUSH0 | TURNOVER | MINCUSH0 |
|---|---|---|---|
| u56 | **0.0000** | 0.1176 | 0.7500 |
| broad | 0.1579 | 0.1818 | 0.9231 |
| small | 0.1176 | 0.0000 | 0.1176 |

**A cushion THRESHOLD does not transport across panels** — chosen on u56 it catches nothing on the
other two, and turnover beats it in 2 of 3 directions. The *ordering* transports (AUC), the *cut*
does not. Any "publishable panel column" proposal has to survive this and H2CUSH0 does not.

**(c) PROTOCOL rule 8** — threshold chosen on 2009–2016 alone, 2017–2026 read exactly once,
outcome = the arm's OOS Sharpe beating SPY's (base rate 64.8%):

| column | IS F1 | OOS precision | OOS recall | **OOS F1** | **OOS AUC** |
|---|---|---|---|---|---|
| **H2CUSH0** | 0.4134 | 0.9714 | 0.9714 | **0.9714** | **0.9632** |
| MINCUSH0 | 0.9398 | 0.9773 | 0.3071 | 0.4674 | 0.9762 |
| **TURNOVER** | 0.4218 | 0.7593 | 0.5857 | **0.6613** | **0.6616** |

**On the one control that is not a restatement of the outcome, the zero-cost H2 cushion measured
on the first half beats turnover out of sample by a wide margin (AUC 0.9632 vs 0.6616).** That is
the queue's claim, verified — for the softer "beats SPY OOS" outcome, where cost erosion genuinely
could have mattered and still does not.

## F — both KEEP paths, and why no KEEP is claimed

**4a 0 / 648 · 4b 24 / 648 · BOTH 0 / 648** (0 bps 9/216, 10 bps 9/216, 25 bps 6/216).

All nine 4b passers at 10 bps are **RULESv2 at gross 1.00** — six on u56, three on broad, none on
small — i.e. the record's already-published **gross-1.00 family** (ideas 439 / 442), reproduced
here from a different direction. Not a new candidate, and three reasons not to treat it as one:

1. The margins are razor thin: the widest is u56 / RULESv2 / gross 1.00 / monthly at
   **margin_min +0.0130** (CAGR 11.96%, Sharpe 1.1781, MaxDD −18.81%, halves 1.214 / 1.150,
   OOS 1.2336); broad's three sit at **+0.0004 … +0.0006**.
2. **Idea 619, run in this same sprint today, measures the median W-vs-M phase band on these
   panels at 0.0468 of Sharpe — 3.6× the widest margin here.** The cadence half of this book's
   parameterisation is inside its own nuisance band.
3. Under rule 8 only 5 of the 9 also pass 4b in-sample, with IS margins of +0.0023 … +0.0050.

The live configuration (RULESv2, gross 0.75, weekly) misses 4b by **−0.0200** on u56 and −0.0263
on broad, and by −0.3224 on small, with **CAGR the binding leg in every case** — the 70%-of-SPY
floor, exactly as idea 442 found.

## Reading

The queue asked whether H2-cushion-at-0-bps is a publishable panel column, tested against turnover.
Three answers, in order of how much they should change what the record does:

1. **At 10 bps the cost rung decides nothing.** 207 of 207 failures are level failures. Any
   screening column whose content is turnover — the incumbent, and the record's habit — is
   answering the wrong question at the rung PROTOCOL actually binds at.
2. **The cushion that matters is the MINIMUM over the five 4b legs, and on the large-cap panels
   that minimum is the DRAWDOWN CAP** (142 of 216 arms), not H2. H2 binds only on SMALL439.
   Idea 137's aside was a SMALL-panel observation promoted to a panel column.
3. **The cushion's edge over turnover is mostly between-panel** (within-panel rho 0.3640 vs
   0.3385) and its threshold does not transport across panels — but its *ordering* survives the
   rule-8 out-of-sample control decisively (AUC 0.9632 vs 0.6616).

**Proposed for Sunday review, report-only, no RULES change applied:** any file that reports a 4b
verdict at a cost rung should publish the same verdict at **0 bps** beside it. One extra column,
already computed by every script that runs a cost ladder, and it separates a level failure from a
cost failure — a distinction that, on this menu, covers 100% of the outcomes. That is a cheaper
and better-targeted proposal than adding an `H2CUSH0` column, which this run kills.

### Caveats
* **Survivorship** (idea 54): current constituents on all three panels; SMALL439 drops the 44
  `max_1d_move >= 1.0` tickers. No level here is an attainable return; every comparison that
  carries the conclusion is between arms priced on the same panel.
* **The base rate is 4.2%** (9 positives in 216). Every AUC and F1 at that base rate is a small-
  sample statistic; SMALL439 has no positives at all and its column AUCs are undefined. The
  decomposition in section B is a count, not an estimate, and does not depend on the base rate.
* Panels truncated to their common last date 2026-09-04 (idea 328); 10 bps and t+1 execution
  (idea 126); MaxDD is one number off one path (idea 321) and the 4b DD leg turns on exactly it.
* Idea 613: inside one rung a drag re-pricing (turnover × c) is a strictly monotone transform of
  turnover, so DRAG was not run as a separate column — it would be the identical ranking.

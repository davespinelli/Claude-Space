# Idea 484 — does-one-dispersion-number-really-out-predict-136-name-dummies (lane C, 2026-09-09)

**ANSWERED. The queue's hypothesis is CONFIRMED: idea 252's leg-(3) ordering is a SMALL-N
ARTEFACT and does not survive a 2x increase in draws. The name-additive model catches `sd` in
12 of 12 book-Sharpe cells on BOTH panels, at a median D\* of 100 draws per k cell — twice idea
252's own N — and by D=500 it is ahead by a median 0.60 of out-of-fold R². The sentence "a
single dispersion number out-predicts the whole 136-name additive model on this panel" is true
only at N=50 and must be restated with its N. No RULES change, no KEEP-candidate, no memo;
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.**

Script `2026-09-09_does-one-dispersion-number-really-out-predict-136-name-dummies_C.py`;
console `.console.txt`; CSVs `.grid.csv.gz` (3,000 books), `.nested.csv` (252 ladder points),
`.crossover.csv` (72), `.walkforward.csv` (252). Elapsed 848s.

---

## What was asked

Idea 252's leg (3) reported, on B136 with idea 78's 50 draws per k cell:

> the name-level model ALONE predicts out of fold at R² −0.197…+0.424 (median **+0.151**); `sd`
> ALONE at R² +0.026…+0.375 (median **+0.289**) — a single dispersion number out-predicts the
> whole 136-name additive model on this panel.

That is exactly the ordering a small-N comparison produces whether or not it is true of the
population: a 136-parameter ridge fitted on 45 training rows is mostly shrinkage, while a
2-parameter line on the same 45 rows is already near its asymptote. The queue asked whether the
ordering is an artefact of N, and **where the crossover is**.

## Reproduction gates (run before any new number was read)

| gate | result |
|---|---|
| [a] U56/CAND20 from `engine.backtest` | 12.6530% / 1.09172 / −18.3083% (published 12.7% / 1.092–1.093 / −18.3%) |
| [a] U56/RULES v1 | 6.4194% / 0.66110 / −13.8278% (published 6.5% / 0.664–0.666 / −13.8%) |
| [b] FAST BACKTEST — the vectorised backtester that runs 3,000 books vs `engine.backtest` on 6 drawn books | max abs difference **2.776e-17** on the evaluation window |
| [c] GRID — the first 50 draws of each B136 k cell vs idea 78's committed `gridB.csv` | 300 rows × 17 numeric columns, **max abs difference 8.3e-16** |
| [d] IDEA 252's OWN NUMBER, leg (3) recomputed at D=50 on B136 | M alone median **+0.1509** (published +0.151), range −0.1968..+0.4237 (published −0.197..+0.424); sd alone median **+0.2894** (published +0.289), range +0.0262..+0.3750 (published +0.026..+0.375); nested gain positive **72/72** (published 72/72) |

The draw ladder is **nested**: draw *d* is the same name set at every D, and on B136 the first 50
draws of each k cell are idea 78's own, which is what gate [c] proves. So every number below is
read on a superset of idea 252's rows, not on a different sample.

## Two tuned parameters (the queue's own): draws and panel

D ∈ {50, 100, 150, 200, 300, 400, 500} per k cell × panel ∈ {B136 (P=136), SMALL484 (P=483
tradable names — idea 78's label; the panel carries 483 non-SPY columns)}. Everything else is
idea 78/83/252's, imported unchanged: k ∈ {20,40,80}, n ∈ {5,20}, gate, gross 0.75, weekly,
10 bps, next-day execution, the 2009–2016/2017–2026 split, seeds `SEED_B + k`, 10 folds by draw
index. The ridge penalty is **not** a third tuned parameter: the headline curve picks λ by a
nested inner 5-fold CV inside each training fold, and the whole six-point ladder plus the
oracle (best-λ-per-cell, the most generous reading M can be given) is reported beside it.

## (1) THE LEARNING CURVES — `sd` is at its asymptote by N=50; M is nowhere near its own

Median out-of-fold R² over the 12 book-Sharpe cells per panel/D:

| panel | D | `sd` alone | M (CV λ) | M (oracle λ) | M + `sd` | nested gain |
|---|---|---|---|---|---|---|
| B136 | 50 | **+0.2894** | +0.1971 | +0.2778 | +0.5259 | +0.2344 |
| B136 | 100 | +0.2942 | **+0.4989** | +0.5243 | +0.6081 | +0.1227 |
| B136 | 150 | +0.3016 | +0.6847 | +0.7003 | +0.7298 | +0.0624 |
| B136 | 200 | +0.3091 | +0.7916 | +0.7965 | +0.8236 | +0.0238 |
| B136 | 300 | +0.3008 | +0.8500 | +0.8500 | +0.8647 | +0.0131 |
| B136 | 400 | +0.3096 | +0.8697 | +0.8697 | +0.8725 | +0.0064 |
| B136 | 500 | +0.2899 | **+0.8826** | +0.8826 | +0.8845 | +0.0031 |
| SMALL484 | 50 | **−0.0387** | −0.0834 | −0.0151 | −0.0806 | +0.0063 |
| SMALL484 | 100 | −0.0263 | **+0.0301** | +0.0867 | +0.0344 | −0.0101 |
| SMALL484 | 200 | −0.0209 | +0.2317 | +0.2542 | +0.2304 | −0.0015 |
| SMALL484 | 300 | −0.0117 | +0.4278 | +0.4528 | +0.4264 | −0.0014 |
| SMALL484 | 500 | −0.0065 | **+0.5865** | +0.5955 | +0.5872 | −0.0009 |

`sd`'s curve is **flat**: on B136 it moves +0.2894 → +0.2899 across a 10× increase in draws.
M's rises +0.1971 → +0.8826. The two curves are not competing hypotheses about the panel; one
of them is a measurement of N.

## (2) THE CROSSOVER — D\* = 100, i.e. 2x idea 252's own N

Smallest D on the ladder with oofR²(M) ≥ oofR²(`sd`), per cell:

| panel | λ rule | cells where M catches `sd` | median D\* | gap at D=50 | gap at D=500 | slope of gap on log D |
|---|---|---|---|---|---|---|
| B136 | CV | **12 of 12** | **100** | +0.0843 | −0.5959 | −0.2981 (negative 12/12) |
| B136 | oracle | **12 of 12** | 100 | +0.0115 | −0.5959 | −0.2668 (negative 12/12) |
| SMALL484 | CV | **12 of 12** | **100** | +0.0360 | −0.5927 | −0.2779 (negative 12/12) |
| SMALL484 | oracle | **12 of 12** | 50 | −0.0297 | −0.6018 | −0.2562 (negative 12/12) |

48 of 48 (panel × λ rule × cell) gaps close monotonically in log D and every one of them
crosses inside the ladder. Cell-by-cell D\* is in `.crossover.csv`; the largest is 200 (one
SMALL484 premium cell). Nothing here needed extrapolation.

Counted the other way: at D=50, `sd` beats M in 8/12 (B136) and 9/12 (SMALL484) cells — idea
252's finding, reproduced. **At D=500, `sd` beats M in 0/12 on both panels.**

## (3) THE SECOND CASUALTY — idea 252's "72 of 72" nested gain is also an N=50 statement

Idea 252's secondary bar was that adding `sd` to the name-level model must improve out-of-fold
prediction; it reported 72/72 with median gain +0.2391. Reproduced here at D=50 (72/72). But
the gain decays with the same N that produced the ordering: on B136 the median gain falls
+0.2344 → **+0.0031** (still positive in 9/12 cells at D=500, so the *direction* survives on the
large panel, ~75× smaller); on SMALL484 it turns **negative** (median −0.0009, positive in only
3/12). Once the ridge has data, `sd` is very nearly redundant to it.

**What this does NOT touch.** Idea 252's headline — that `sd` survives the out-of-fold
name-level control on the partial-t test at N=50 — is a different leg and is not re-run here.
This run says only that leg (3)'s *ordering* sentence is about N. Whether the partial test
still leaves `sd` alive once the control reaches oofR² 0.88 is a genuinely open question and is
filed to the queue rather than asserted.

## (4) BOTH KEEP PATHS — all 3,000 fresh books

4a: Sharpe > the comparand book in both halves AND MaxDD no worse. 4b: Sharpe > SPY in both
halves AND out of sample, MaxDD ≤ 60% of SPY's, CAGR ≥ 70% of SPY's.

| panel | book | N | 4a vs RULES v1 (superseded) | 4a vs **LIVE RULES v2** | 4b | BOTH |
|---|---|---|---|---|---|---|
| B136 | CAND-5 | 1500 | 285 | **0** | 30 | 0 |
| B136 | CAND-20 | 1500 | 1462 | **12** | 394 | **1** |
| SMALL484 | CAND-5 | 1500 | 27 | **0** | 0 | 0 |
| SMALL484 | CAND-20 | 1500 | 11 | **1** | 0 | 0 |

The v1→v2 collapse (1462 → 12) independently reproduces the 2026-09-09 cloud restatement on a
fresh grid. **One book of 3,000 clears both paths** (B136, k=20, draw 80, CAND-20: 11.68% /
1.260 / −12.04%, OOS Sharpe 1.361). It is not a KEEP candidate and no memo is written: it is
one random 20-name list found by scanning 3,000 sub-panels, its in-sample Sharpe ranks only
145th of 1,500, and 4b alone passes on 394 of 1,500 B136 CAND-20 books — a bar this panel
clears by coin flip. It is a name list, not a rule.

## (5) RULE 8 WALK-FORWARD — selectors fitted on 2009–2016, 2017–2026 read once

Mean OOS over 7 ladder points × 2 book sizes:

| panel | arm | OOS CAGR | OOS Sharpe | OOS MaxDD | beats SPY | beats live v2 |
|---|---|---|---|---|---|---|
| B136 | S0 do-nothing (whole panel) | 14.27% | 0.8529 | −21.71% | — | 0/14 |
| B136 | S1 IS-Sharpe argmax | 11.87% | 1.0725 | −16.26% | 11/14 | 3/14 |
| B136 | S2 max IS `sd` | 12.38% | 1.0535 | −17.83% | 11/14 | 7/14 |
| B136 | S3 `sd`-model OOF pred | 12.77% | 1.0697 | −18.62% | 11/14 | 7/14 |
| B136 | **S4 M-model OOF pred** | 13.93% | **1.0091** | −20.16% | 11/14 | 3/14 |
| B136 | S5 M+`sd` OOF pred | 12.29% | 1.1023 | −16.02% | 14/14 | 3/14 |
| B136 | S6 random draw | 10.16% | 0.8490 | −19.28% | — | 1/14 |
| B136 | SPY / RULES v2 | 15.45% / 7.98% | 0.8820 / **1.1185** | −33.72% / −12.24% | | |
| SMALL484 | S0 do-nothing | 6.89% | 0.4324 | −39.56% | 0/14 | 0/14 |
| SMALL484 | S2 max IS `sd` | 0.01% | 0.0485 | −30.62% | 0/14 | 0/14 |
| SMALL484 | S3 `sd`-model OOF pred | 0.44% | 0.0771 | −30.30% | 0/14 | 0/14 |
| SMALL484 | S4 M-model OOF pred | 2.16% | 0.2157 | −43.61% | 0/14 | 0/14 |
| SMALL484 | S5 M+`sd` OOF pred | 1.78% | 0.1938 | −43.98% | 0/14 | 0/14 |
| SMALL484 | SPY / RULES v2 | 15.45% / 4.55% | 0.8820 / **0.6629** | −33.72% / −12.09% | | |

**No arm on either panel beats the live book on average, and no arm on SMALL484 beats even
SPY.** The prediction-model selectors split by panel and neither wins: the name-additive
selector beats the dispersion selector in 5 of 14 B136 ladder points (mean −0.0605) and 9 of 14
SMALL484 points (mean +0.1387). Better out-of-fold *fit* (M, by a mile at D≥150) does not buy a
better *choice*: the object being predicted, a draw's in-sample Sharpe, is not what pays out of
sample. The one B136 both-paths book above was picked once, by S3 at D=100 — one arm at one
ladder point of 14, whose own mean (1.0697) is below the live book's 1.1185.

## What the record should say now

Idea 252's leg (3) sentence needs its N attached wherever it is quoted: *"at 50 draws per k
cell, one dispersion number out-predicts a 136-name additive ridge; at 100 draws the ridge is
ahead, and at 500 it is ahead by 0.60 of out-of-fold R² on both panels."* The general claim —
that a low-dimensional summary beats name dummies **on this panel** — is refuted.

## Caveats

* **Survivorship (rule 9):** both panels are current constituents. That cuts *against* the
  name-additive model, which is fitted on names already known to have survived — the most
  favourable possible sample for a fixed-effect design. It still loses at N=50, and it wins at
  N≥100 on ground that flatters it either way.
* The comparison is of **out-of-fold predictive R² on the same 10-fold split** idea 252 used;
  folds are by draw index, so training size is 0.9·D throughout and the ladder is a clean
  learning curve, not a change of estimator.
* EWall halves are not in idea 78's grid schema and are not restated (marked −1 above).
* The 3,000 books are fresh runs, not a re-read of committed output; gate [c] is what ties them
  to the published grid.

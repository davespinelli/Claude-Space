# Idea 486 — census-every-published-N-EQUALS-50-model-comparison-in-the-record (lane C, 2026-09-09)

**ANSWERED. The queue's premise is REFUTED as a record-wide worry and CONFIRMED as a
single-file fact. The record contains exactly ONE independent published model-vs-model
comparison decided at N ≤ 100 rows with a >10-parameter gap — idea 252's — and its ordering is
re-read here at D=1000 draws per k cell (20× idea 252's N, 2× idea 484's): `sd` beats the
name-additive ridge in 8/12 book-Sharpe cells at D=50 and 0/12 at D=1000 on B136, 9/12 → 0/12
on SMALL484. Every OTHER model comparison the scan resolves has a parameter gap of ≤ 5, and
the largest gap at any N ≤ 150 outside the wide class is 3. No RULES change, no KEEP-candidate;
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.**

Script `2026-09-09_census-every-published-N-EQUALS-50-model-comparison-in-the-record_C.py`;
console `.console.txt`; CSVs `.census.csv` (72 files), `.pairs.csv` (52 comparisons, ALL
reported), `.censusgrid.csv` (16 grid points), `.reread.csv`, `.nested.csv` (216 ladder
points), `.crossover.csv` (72), `.keeppaths.csv`, `.walkforward.csv` (216), `.grid.csv.gz`
(6,000 books). Elapsed 580 s.

---

## What was asked

Idea 484 found that a 136-parameter ridge and a 2-parameter line compared at N=50 report an
ordering that reverses at N=100 and inverts by 0.60 R² at N=500, with the low-dimensional side
FLAT across the whole ladder. The queue asked how much of the record sits in that regime:
census every model-vs-model comparison decided at N ≤ 100 rows where the two sides differ by
more than ~10 fitted parameters, and re-read each at the largest N its own panel can supply.

**Pre-registered definition (written before any count was read).** A *comparison* is a pair of
model specifications whose fit statistics are published side by side in the same table or
sentence, scored on the SAME target and the SAME rows. `p` = fitted parameters including the
intercept. `N` = rows the comparison was decided on. Every resolved spec set contributes all of
its unordered pairs.

**Two tuned parameters (the queue's own), both census axes, all 16 points reported:** N floor
∈ {50, 75, 100, 150} and parameter gap G ∈ {2, 5, 10, 20}; a pair is in scope iff `N ≤ Nfloor`
AND `gap > G`. Panel and the draw ladder D are reporting axes, not tuned — every point published.

## Reproduction gates (all run before any new number was read)

| gate | result |
|---|---|
| [a] U56/CAND20 from `engine.backtest` (the 2026-09-04 KEEP-4b candidate) | **12.6530% / 1.09172 / −18.3083%**, halves 1.09418/1.09573 (published 12.7% / 1.092–1.093 / −18.3%) |
| [a] U56/RULES v1 | 6.4194% / 0.66110 / −13.8278% (published 6.5% / 0.664–0.666 / −13.8%) |
| [a] panel integrity | B136 carries 136 columns, SMALL484 carries 484 — asserted, not assumed, because `load_universe(broad=True)` reaches `data/prices_broad.csv` only via its exception path |
| [b] FAST BACKTEST vs `engine.backtest` on 6 drawn books | max abs difference **2.776e-17** on the evaluation window |
| [c] GRID — 25 draws of each k cell on each panel re-run fresh vs idea 484's committed `.grid.csv.gz` | 150 rows × 27 numeric columns, max abs difference **7.105e-15** → the D=1000 ladder is a nested extension of idea 484's own draws, not a different sample |
| [d] IDEA 252's OWN NUMBERS at D=50 on B136 | M alone median **+0.1509** (published +0.151), range −0.1968..+0.4237 (published −0.197..+0.424); `sd` alone median **+0.2894** (published +0.289), range +0.0262..+0.3750 (published +0.026..+0.375); nested gain positive **72/72** (published 72/72) |
| [e] MECHANICAL SCAN reproduces idea 483's census | 72 / 66 / 7 / 3 against idea 483's published 70 / 66 / 5 / 3 — the same regexes, over a corpus that has grown by two wide files since |
| [f] free reproduction | the phase-sensitivity per-cadence table rebuilt from that file's own `.books.csv` returns its published R² to three decimals in all 5 cadences (0.087/0.326/0.409 at 10W, etc.) |

## (1) THE CENSUS — the exposed class is ONE independent comparison

10 published spec sets resolve to **52 comparisons**, every one in `.pairs.csv`. Counts of
comparisons in scope:

| Nfloor \ G | 2 | 5 | 10 | 20 |
|---|---|---|---|---|
| 50 | 2 (1 indep.) | 2 (1) | 2 (1) | 2 (1) |
| 75 | 2 (1) | 2 (1) | 2 (1) | 2 (1) |
| **100** | 2 (1) | 2 (1) | **2 (1)** | 2 (1) |
| 150 | 5 (**4**) | 2 (1) | 2 (1) | 2 (1) |

The two comparisons in the queue's own cell are idea 252's (`sd` p=2 vs the 136-name additive
ridge, N=50) and idea 484's re-read of that same comparison. **Excluding the re-read, the class
is one file.** The grid is FLAT from G=20 down to G=5: nothing in the record sits between a
gap of 5 and a gap of 134. It grows only at (Nfloor=150, G=2), where three gap-3 pairs from
`can-a-panel-property-choose-the-cadence` (N=115) enter.

**The largest parameter gap anywhere else in the record is 5** — `does-the-cash-drag-share…`
(c_bar alone p=2 vs 1+c_bar+panel+family+cadence p=7) at N=162, above every N floor tested. The
record's typical fit is 1–4 parameters at N=49–560. Idea 483 already measured the artefact in
that regime: at its NARROW10 rung the in-sample and out-of-fold answers differ by ≤ 0.05.

## (2) THE RE-READ AT MAX N — the wide class, D=1000 per k cell

Median out-of-fold R² over the 12 book-Sharpe cells per panel (CV λ; the oracle-λ reading, the
most generous the ridge can be given, is in the console and agrees):

| panel | λ rule | `sd` D=50 → D=1000 | M D=50 → D=1000 | gap D=50 → D=1000 | `sd` beats M | median D\* |
|---|---|---|---|---|---|---|
| B136 | CV | +0.2894 → **+0.3054** | +0.1971 → **+0.9106** | +0.0843 → −0.6150 | 8/12 → **0/12** | **100** |
| B136 | oracle | +0.2894 → +0.3054 | +0.2778 → +0.9106 | +0.0115 → −0.6150 | 7/12 → **0/12** | 100 |
| SMALL484 | CV | −0.0387 → **−0.0028** | −0.0834 → **+0.7976** | +0.0360 → −0.7981 | 9/12 → **0/12** | 100 |
| SMALL484 | oracle | −0.0387 → −0.0028 | −0.0151 → +0.7976 | −0.0297 → −0.7981 | 2/12 → **0/12** | 50 |

`sd`'s curve moves +0.2894 → +0.3054 across a **20× increase in draws**; M's moves +0.1971 →
+0.9106. M catches `sd` inside the ladder in **12 of 12 cells on both panels at both λ rules**,
median D\* = 100. Doubling idea 484's ladder does not move the crossover and does not rescue the
low-dimensional side: the two curves are not competing hypotheses about the panel, one of them
is a measurement of N. **Idea 252 leg (3)'s ordering sentence is an N=50 statement, and this run
extends the evidence from 10× to 20× its N without changing the verdict.**

## (3) THE RE-READ AT MAX N — everything else in scope

* **`why-does-the-DD-ranking-die-on-U56`** publishes its own two N's. Refitting on its committed
  186 cell slopes: `e only` R² +0.4093 (n=12) → **+0.1088** (n=186); `k only` +0.4672 →
  +0.1055; `e + k` +0.6389 → **+0.1697**, which reproduces that file's own published large-N row
  to the digit. The ORDERING **HOLDS** (`e+k` still leads) but the margin decays +0.2296 →
  +0.0610. Small N inflated the effect fourfold; it did not invent it.
* **`is-phase-sensitivity`**, published per cadence at n=115, re-read on the pool (N=**575**, the
  largest N its panel supplies) with cadence fixed effects added to every spec so pooling itself
  is not the change: R² family 0.5415, properties 0.5536, both 0.5552 → *properties > family*,
  agreeing with 4 of the 5 published cadence strata (2M, the weakest at R² 0.036, is the one
  that disagrees). **The published ordering survives its own largest N.**
* Every remaining comparison is PANEL-CAPPED at its published N: there is no larger N in the
  file's own committed output, and this is stated rather than papered over.

## (4) BOTH KEEP PATHS — all 6,000 books

4a: Sharpe > the comparand in both halves AND MaxDD no worse. 4b: Sharpe > SPY in both halves
AND out of sample, MaxDD ≤ 60% of SPY's, CAGR ≥ 70% of SPY's.

| panel | book | N | 4a vs RULES v1 (superseded) | 4a vs **LIVE RULES v2** | 4b | BOTH |
|---|---|---|---|---|---|---|
| B136 | CAND-5 | 3000 | 531 | **0** | 61 | 0 |
| B136 | CAND-20 | 3000 | 2911 | **21** | 747 | **1** |
| SMALL484 | CAND-5 | 3000 | 48 | **0** | 0 | 0 |
| SMALL484 | CAND-20 | 3000 | 22 | **2** | 0 | 0 |

**One book of 12,000 book-rows clears both paths** — B136, k=20, draw 80, CAND-20, 11.68% /
1.2597 / −12.04%, halves 1.2574/1.2663, OOS Sharpe 1.3608. It is the same draw idea 484 found,
reproduced on a doubled grid, and it is still **not** a KEEP candidate and gets no memo: 4b
alone passes on 747 of 3,000 B136 CAND-20 books, a bar this panel clears roughly by coin flip,
and the book is one random 20-name list found by scanning thousands of sub-panels. It is a name
list, not a rule. The v1→v2 collapse (2911 → 21) again reproduces the 2026-09-09 cloud
restatement, now on 2× the books.

## (5) RULE 8 WALK-FORWARD — selectors fitted on 2009–2016, 2017–2026 read once

Mean OOS over 6 ladder points × 2 book sizes:

| panel | arm | OOS CAGR | OOS Sharpe | OOS MaxDD | beats SPY | beats live v2 |
|---|---|---|---|---|---|---|
| B136 | S0 do-nothing (whole panel) | 14.27% | 0.8529 | −21.71% | — | 0/12 |
| B136 | S1 IS-Sharpe argmax | 12.04% | 1.0911 | −16.35% | — | — |
| B136 | S3 `sd`-model OOF pred | 12.04% | 1.0455 | −18.19% | 8/12 | 6/12 |
| B136 | S4 M-model OOF pred | 14.81% | 1.0304 | −20.43% | 10/12 | 3/12 |
| B136 | S5 M+`sd` OOF pred | 12.37% | **1.1121** | −16.11% | **12/12** | 3/12 |
| B136 | S6 random draw | 11.05% | 0.8616 | −21.54% | — | — |
| B136 | SPY / **RULES v2 (live)** | 15.45% / 7.98% | 0.8820 / **1.1185** | −33.72% / −12.24% | | |
| SMALL484 | S0 do-nothing | 6.89% | 0.4324 | −39.56% | 0/12 | 0/12 |
| SMALL484 | S3 `sd`-model OOF pred | 2.60% | 0.2404 | −27.92% | 0/12 | 0/12 |
| SMALL484 | S4 M-model OOF pred | 4.48% | 0.3324 | −37.32% | 0/12 | 0/12 |
| SMALL484 | S5 M+`sd` OOF pred | 4.83% | 0.3439 | −36.20% | 0/12 | 0/12 |
| SMALL484 | SPY / **RULES v2 (live)** | 15.45% / 4.55% | 0.8820 / **0.6629** | −33.72% / −12.09% | | |

**No arm on either panel beats the live book on average**, and no arm on SMALL484 beats even
SPY. The best B136 arm (S5, 1.1121) still sits below RULES v2 (1.1185). Winning the out-of-fold
FIT by 0.60 R² at D=1000 buys the name-additive selector nothing: it beats the dispersion
selector in 6 of 12 B136 ladder points (mean −0.0151) and 8 of 12 SMALL484 points (mean
+0.0920) — a coin flip on the panel where it dominates the fit. The object being predicted, a
draw's in-sample Sharpe, is not what pays out of sample.

## What the record should say now

Two sentences, both now supported at N=1000:

1. *"At 50 draws per k cell one dispersion number out-predicts a 136-name additive ridge; at 100
   draws the ridge is ahead, and at 1,000 it is ahead by 0.61 (B136) and 0.80 (SMALL484) of
   out-of-fold R², with `sd` flat across the whole 20× range."*
2. *"That regime is one file. The record's other 51 published model comparisons differ by ≤ 5
   fitted parameters — ≤ 3 at any N ≤ 150 — so idea 484's mechanism does not generalise to them,
   and idea 483's NARROW10 measurement (IS-vs-OOF ≤ 0.05) is the right prior for the rest."*

## Caveats

* **Census coverage is a LOWER bound, and says so.** The scan resolves a published comparison
  only where the file wrote a spec/parameter table to a committed CSV (MECHANICAL, 7 of 10 sets)
  or printed one to its console (ADJUDICATED, 3 sets, each carrying its console file and line in
  `.pairs.csv`). A comparison made only in prose, with no fit table anywhere, is invisible to it.
  The mechanical layer is tied to idea 483's published census by gate [e].
* **Survivorship (rule 9):** both panels are current constituents. That cuts *against* the
  name-additive model, which is fitted on names already known to have survived. It still loses
  at N=50 and wins at N ≥ 100 on ground that flatters it either way.
* The comparison is of out-of-fold predictive R² on the same 10-fold split idea 252 used; folds
  are by draw index, so training size is 0.9·D throughout and the ladder is a clean learning
  curve, not a change of estimator.
* Books for draws 0..499 are read from idea 484's committed grid rather than re-run; gate [c]
  re-runs 150 of them fresh and requires an exact match (7.1e-15) before any of them is used.
* EWall halves are not in idea 78's grid schema and are not restated (marked −1 in §4).

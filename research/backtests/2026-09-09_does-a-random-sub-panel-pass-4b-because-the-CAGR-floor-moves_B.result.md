# Idea 253 — does a random sub-panel pass 4b because the CAGR floor moves? (lane B, 2026-09-09)

**VERDICT: ANSWERED / SPLIT. The queue's premise is half right, and the half that is wrong is
the finding. The CAGR floor is the bar a random sub-panel is *centred below* and the raw-unit
argmin in 67.2% of the record's published 4b passes — but measured in each panel's own
random-sub-panel noise the DD cap binds more often (47.6% of rows, 71.5% of file-votes). The
two argmins disagree on 26.1% of rows, so "which bar was closest" is not a fact about the
record, it is a fact about the units. And 46.8% of the 25,028 reproduced published 4b passes
sit inside their own panel's random-sub-panel base rate.** No RULES change, no book promoted,
no memo. Script `2026-09-09_does-a-random-sub-panel-pass-4b-because-the-CAGR-floor-moves_B.py`.
`RULES.md`, `scan.py`, `bot.py`, `baseline.py` untouched.

Tuned parameters (PROTOCOL rule 4, max 2): **k** (sub-panel size) and **book** (EWall | CAND20).
All 18 grid points are printed and written to `.null.csv`. 10 bps, weekly, next-day execution.

## Gates

- `fast_backtest` vs `engine.backtest`: max |dret| **2.08e-17**, max |dturnover| **5.55e-16**.
- Digit-exact anchor: idea 83's published B136 SPY line reproduces —
  **15.23% / 0.889 / −33.72%, halves 0.957/0.834, OOS 0.882** (its `console.txt` line 11).
- The books are idea 83's own `weights_ewall` / `weights_cand` verbatim (gross 0.75, 200d MA +
  vol<60% gate, de-gross to cash), so PART A's base rates are comparable to idea 78/83's ~46%.
- Panel 4b bars: U56 CAGR floor 10.63% / DD cap 20.23%; B136 10.66% / 20.23%; SMALL 9.89% / 20.23%.

## PART A — the null (2,700 draws, 150 per cell, seeded off (panel, k, draw))

| panel | 4b base rate | cell range | random passes |
|---|---|---|---|
| U56 | **28.1%** | 0.0% (k14 CAND20) – 76.0% (k42 CAND20) | 253 / 900 |
| B136 | **23.0%** | 0.0% (k20 CAND20) – 38.7% (k80 EWall) | 207 / 900 |
| SMALL | **0.0%** | 0.0% everywhere | **0 / 900** |

B136 k=80 EWall = **38.7%** against idea 78/83's published **46%** at N=50 (gap 7.3 pp ≈ 0.9
combined binomial sd): idea 78's base rate reproduces. **SMALL clears 4b zero times in 900 draws**
— the sub-$2B panel is not near the bars on any leg, so nothing below speaks to it.

**Which bar the null is short of.** Mean slack ÷ sd across all 900 draws of a panel:

| panel | H1 | H2 | OOS | DD | CAGR |
|---|---|---|---|---|---|
| U56 | +0.31 | +1.34 | +1.60 | +0.71 | **−0.45** |
| B136 | +0.93 | +0.22 | +0.71 | +0.38 | **−0.28** |

**The CAGR floor is the only bar a random sub-panel sits below on average, on both panels.** It
is also the bar with the smallest absolute noise (slack sd 0.007–0.025 of CAGR vs 0.05–0.20 of
Sharpe), which is exactly what makes the raw-unit and noise-unit answers below disagree.

## PART B — the back-fill over the committed record

Corpus, mechanically: **2,074 committed CSVs, 795 carry a 4b column, 248 also carry a panel column
and all of CAGR/Sharpe/MaxDD/H1/H2/OOS_Sharpe** (190,072 rows). Published 4b **PASS** rows:
**26,316**; 1,100 on unmappable panel labels; **25,153 recovered**.

**Reproduction gate:** recomputing all five bars from each row's own metrics against this
repository's panel SPY reference re-derives the parent's published pass on **25,028 of 25,153
(99.5%)**. The 125 that do not are excluded from every number below; my reference says they fail
H1 72 / CAGR 55 / DD 18 / H2 10 / OOS 1. The two worst offenders —
`holding-period-as-the-hidden-variable_cloud.grid.csv` (19) and
`quote-every-n-argmax-with-its-saturation-share_cloud.grid.csv` (7) — are **the same two files
idea 150 rejected on its own independent gate**, which is a clean cross-check of this harvest.

**Which bar was closest to binding, over 25,028 reproduced passes (237 files):**

| units | H1 | H2 | OOS | DD | CAGR |
|---|---|---|---|---|---|
| raw (Sharpe pts / DD frac / CAGR frac) | 283 (1.1%) | 80 (0.3%) | 8 (0.0%) | 7,848 (31.4%) | **16,809 (67.2%)** |
| panel noise units (z = slack / sd_null) | 2,244 (9.0%) | 418 (1.7%) | 20 (0.1%) | **11,902 (47.6%)** | 10,444 (41.7%) |
| file-weighted (one vote per file × panel, N=438) | 1 (0.2%) | 10 (2.3%) | 0 (0.0%) | **313 (71.5%)** | 114 (26.0%) |

The two argmins agree on only **73.9%** of rows. **The three Sharpe legs are essentially never the
binding bar** — 10.8% of rows and 2.5% of file-votes between them. Whatever else 4b is doing on
this record, it is a DD/CAGR bar, and the queue was right that the CAGR floor is where the record
sits closest in raw terms. Per panel (noise units): B136 DD 41% / CAGR 54%; U56 DD 51% / CAGR 36%.
SMALL contributes **0** reproduced published passes.

**Marginality.** min-z = distance to the nearest bar in that panel's random-sub-panel noise:

| panel | q10 | q25 | median | q75 | q90 | < 0.25 sd | < 0.50 sd |
|---|---|---|---|---|---|---|---|
| B136 | +0.033 | +0.109 | +0.265 | +0.414 | +0.568 | 46.6% | 84.4% |
| U56 | +0.069 | +0.137 | +0.287 | +0.370 | +0.525 | 43.4% | 88.7% |

## The headline the queue asked for

A published pass is **inside** its panel's random-sub-panel base rate when its min-z is no better
than the **median min-z of the random draws that cleared 4b on that panel** — a typical coin-flip
pass rather than a distinguished one.

| panel | random base rate | random passes (median / q90 min-z) | published passes | inside median | inside q90 | median published percentile |
|---|---|---|---|---|---|---|
| U56 | 28.1% | 253 (+0.287 / +0.587) | 17,000 | **49.9%** | 92.9% | 50.2% |
| B136 | 23.0% | 207 (+0.203 / +0.508) | 8,028 | **40.3%** | 85.1% | 66.7% |
| **all** | 17.0% (2,700 draws) | 460 | **25,028** | **46.8%** | — | — |

**Just under half of every 4b pass this project has published is, on the bar that actually
binds it, indistinguishable from a random sub-panel of the same panel that happened to clear.**

## RULE 8 — walk-forward (cell chosen on IS 2009–2016 pass rate only, read once on 2017–2026)

| panel | IS-argmax cell | IS rate | **OOS rate** | full | cell median OOS CAGR/Sharpe/MaxDD |
|---|---|---|---|---|---|
| B136 | k=80 EWall | 49.3% | **26.0%** | 38.7% | 10.51% / 0.998 / −18.53% |
| U56 | k=28 EWall | 12.7% | **50.0%** | 27.3% | 11.20% / 1.055 / −16.91% |
| SMALL | k=60 CAND20 | 0.0% | **0.0%** | 0.0% | 2.24% / 0.238 / −29.29% |

**The base rate does not transfer**: it halves on B136 and quadruples on U56 out of sample. The
IS-argmax *draw* read once OOS: B136 12.44% / 1.106 / −19.09% (rank **5/150** in its own cell),
U56 10.73% / 1.011 / −24.68% (**100/150**), SMALL 1.63% / 0.191 / −28.74% (**93/150**) — no
consistent selection skill. OOS comparands: RULES v2 baseline 7.98% / 1.119 / −12.24% (B136),
9.51% / **1.282** / −12.05% (U56), 4.55% / 0.663 / −12.09% (SMALL); SPY 15.45% / 0.882 / −33.72%.

## Both KEEP paths — the three rule-8 picked draws, full sample, 10 bps

| book | CAGR | Sharpe | MaxDD | H1/H2 | 4a | 4b |
|---|---|---|---|---|---|---|
| B136 k=80 EWall #57 | 12.80% | 1.142 | −19.09% | 1.279/1.017 | no | **KEEP** (slacks DD +0.0114, CAGR +0.0214) |
| U56 k=28 EWall #88 | 11.41% | 1.106 | −24.68% | 1.370/0.884 | no | no (DD) |
| SMALL k=60 CAND20 #70 | 4.80% | 0.440 | −28.74% | 0.702/0.213 | no | no (all five) |

**4a 0/3, 4b 1/3 — and the one 4b pass is not promotable.** It is an unselected random draw on a
current-constituent panel whose DD slack is a hair over the cap; it is the exact object this run
measures the base rate of. Nothing here is a rule.

## What this establishes

1. **"Which bar is closest to binding" is unit-dependent, and the record has never said which
   units it means.** Raw units say CAGR (67.2%); the panel's own sampling noise says DD (47.6%
   of rows, 71.5% of files). Any future claim about a binding bar must state its unit.
2. **The CAGR floor is the selective bar** — the only one a random sub-panel is centred below on
   both live panels — but it is selective by a *hair*: its noise unit is 5–20× smaller than the
   Sharpe legs', which is why it dominates the raw argmin and not the z argmin.
3. **46.8% of the record's published 4b passes are inside their own panel's random base rate.**
   4b as written admits coin flips on U56 and B136 at roughly one pass in four; 85–93% of
   published passes sit under the random q90. This bears on every 4b count the project has
   published, including idea 247's live KEEP-candidate.
4. **The base rate does not walk forward** (49.3%→26.0% on B136, 12.7%→50.0% on U56), so an
   in-sample base-rate correction cannot be calibrated once and reused.
5. **SMALL is a different regime entirely**: 0 of 900 random draws clear, and the record has 0
   reproduced published 4b passes on it. Nothing above applies there.

## Caveats

- **Coverage.** Only the 248 files carrying a panel column *and* unsuffixed
  CAGR/Sharpe/MaxDD/H1/H2/OOS_Sharpe are harvested; the multi-cost files that publish
  `_0`/`_10`/`_25` suffixed columns (≈15 files) are **not** in the census. Stated hole.
- **The noise unit** `sd_null(bar | panel)` is pooled over the k grid and both books. A different
  k grid moves it, and the DD-vs-CAGR ordering in z units is the number most sensitive to that
  choice; the raw-unit and file-weighted columns are given so the reader can judge without it.
- **Survivorship** (PROTOCOL rule 9): B136 and the small panel are current constituents; the
  random sub-panel null inherits that bias in full.
- Rows are counted as published, so a few very large grids dominate the row-weighted column; the
  file-weighted row is the un-dominated read.

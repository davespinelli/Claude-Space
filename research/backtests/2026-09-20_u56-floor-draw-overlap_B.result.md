# Idea 775 (lane B, 2026-09-20) — is the U56 FLOOR ADVANTAGE a DRAW-OVERLAP ARTEFACT?

**ANSWERED / SPLIT. KILL the U56 reading of the per-parent floor: U56's advantage over B136 is a
`(k, M)` artefact that REVERSES SIGN when the overlap is matched, and after the finite-population
correction the two parents' implied name-level dispersions sit 4.4% apart. The three-parent 1.98x
spread does NOT vanish — but what is left of it is SMALL665, not U56. KILL for capital: no new
book, and the floor itself is ANTI-informative as a selector.**

Script `2026-09-20_u56-floor-draw-overlap_B.py` (construction imported verbatim from idea 567's
own module). Gates **22 of 24**; the two failures are the finding of section 1 and are published,
not repaired.

## 1. The record's floor bar is not a reproducible object (G2 FAIL, G2b FAIL — both published)

| | U56 | B136 | SMALL |
|---|---|---|---|
| idea 567, committed (PREM_SHARPE, D=6, FULL) | 0.050224 | 0.099511 | 0.094077 (SMALL**439**) |
| rebuilt on 567's OWN tape end dates (G2b) | 0.050227 | 0.099706 | — |
| rebuilt on today's tape (G2) | 0.050485 | 0.100241 | 0.063317 (SMALL**665**) |

The **ratio** reproduces (1.9855 today vs 567's 1.9813), so the construction is verbatim; the
levels do not. Max |dev| **4.770e-04 over 90 rows on 567's own tape** (cache restatement) and
**2.147e-03 over 45 rows on today's** (5–10 extra trading days). The SMALL parent was rebuilt on
2026-09-11 (439 → 665 names) and its floor moved **0.094077 → 0.063317, −32.7%**: every committed
claim scored against SMALL439's bar was scored against a number that no longer exists.

## 2. The answer: matched overlap, and zero overlap (PREM_SHARPE, FULL, D = 24)

| K RULE | level | realised overlap | k: U56 / B136 / SMALL | floors | 3-parent ratio | **U56 / B136** | P(U56 narrower) |
|---|---|---|---|---|---|---|---|
| FIXED_K | 12 | 0.1086 | 12 / 12 / 12 | .1148 / .1174 / .1810 | 1.5768 | **0.9780** | 0.543 |
| FIXED_K | 24 | 0.2153 | 24 / 24 / 24 | .0867 / .0918 / .1311 | 1.5114 | **0.9451** | 0.648 |
| FIXED_K | **36 (567's own rung)** | 0.3249 | 36 / 36 / 36 | .0469 / .0719 / .1018 | 2.1711 | **0.6520** | **0.994** |
| RATIO_K | phi 0.0541 | 0.0511 | 3 / 7 / 36 | .1119 / .1162 / .1018 | 1.1415 | **0.9637** | 0.594 |
| RATIO_K | phi 0.2667 | 0.2697 | 15 / 36 / 177 | .1081 / .0719 / .0550 | 1.9647 | **1.5038** | **0.025** |
| RATIO_K | phi 0.6545 | 0.6532 | 36 / 88 / 435 | .0469 / .0295 / .0303 | 1.5874 | **1.5874** | **0.005** |
| DISJOINT | k 12 | **0.0000** | 12 / 12 / 12 | .1123 / .1116 / .1936 | 1.7337 | **1.0056** | 0.492 |
| DISJOINT | k 24 | **0.0000** | 24 / 24 / 24 | .0710 / .1090 / .0986 | 1.5345 | **0.6517** | 0.944 |

**The pre-registered three-parent test: H_OVERLAP FALSIFIED, H_PANEL HOLDS.** Mean max/min over
the matched- and zero-overlap arms is **1.5924** against 567's 1.9813 (bars: < 1.25 / >= 1.50).

**The noise calibration that the three-parent statistic needs.** A max/min over three sd estimates
exceeds 1 even when the true floors are identical: a chi null at the estimator's own dof (D−1=23)
has **median 1.2680, 95th percentile 1.6601**. Only **4 of 8** cells have a bootstrap interval
(2,000 resamples of the draws, of the partitions on the DISJOINT arm) that excludes even the null's
median. Most of the surviving "spread" is the estimator, not the parents.

**The decisive pairwise read — the queue's actual question.** U56/B136 spans **0.6517 .. 1.5874**
across the eight schemes; its bootstrap interval covers 1.0 in **5 of 8**; U56 is the narrowest-floor
parent in **4 of 8** cells and the **widest in 2**. At 567's own rung U56 is 0.652 of B136 with
P = 0.994; at matched overlap it is 1.50x and 1.59x **wider** with P = 0.025 and 0.005. **The sign
of U56's advantage is set by the matching convention, which is what "artefact" means.**

## 3. Why — the finite-population law (Q4)

`sigma_p = floor / sqrt((M-k)/(k(M-1)))`, i.e. the floor with BOTH width and overlap removed:

* **U56 0.4417, B136 0.4618, SMALL665 0.7046** — U56/B136 = **0.9565** (4.4% apart), both vs
  SMALL665 = 0.63 / 0.66.
* pooled `log(floor) = +0.6545 log(scale) − 1.2825`, **R² = 0.7549** (the iid law predicts slope
  +1; names inside a parent are correlated, so the floor falls with k more slowly).
* parent dummies add **ΔR² = +0.1278**, carried by **SMALL665 +0.3887** against B136 +0.0509.

So the one genuine panel fact is that sub-$2B names are ~57% more dispersed than large caps. The
U56-vs-B136 gap the record has been quoting is arithmetic: U56 eats 65% of its parent at k = 36
where B136 eats 27%.

## 4. Capital arm and rule 8 — KILL, no new book

6,912 books (3 parents x 8 schemes x 24 draws x 3 gross x 2 cadences x 2 arms), 10 bps, t+1:
**4a 11/6912, 4b FULL 340, 4b OOS 362, BOTH 1** (one U56 RATIO_K k=15 draw at gross 0.50 monthly).
SMALL665 passes **0 of 2304** on every path. Binding 4b leg: DD (1,958 rows), then CAGR (983).

Rule 8 (choosers fitted on warm-up..2016-12-31, 2017-2026 read once): **4a OOS 0/15, 4b OOS 4/15.**

| pick | FULL CAGR / Sharpe / MaxDD (H1/H2) | OOS CAGR / Sharpe / MaxDD | 4a | 4b |
|---|---|---|---|---|
| U56 C_FLOORMIN (FIXED_K 36 MA-RS tranche) | 11.86% / 1.1212 / −17.76% (1.207/1.059) | 12.65% / 1.1340 / −17.76% | n | **Y** |
| U56 C_FLOORMAX (RATIO_K 0.0541 MA-RS tranche) | 10.97% / 1.1256 / −17.47% (1.228/1.040) | 11.38% / 1.1314 / −17.47% | n | **Y** |
| U56 C_LIVE (RULES v2, whole parent) | 8.62% / 1.2010 / −12.05% (1.228/1.181) | 9.46% / 1.2766 / −12.05% | n | n |
| U56 SPY | 15.12% / 0.8843 / −33.72% (0.957/0.825) | 15.26% / 0.8737 / −33.72% | — | — |

**The floor is anti-informative as a selector**: C_FLOORMIN mean OOS Sharpe **0.8987** against its
own mirror C_FLOORMAX **0.9624** (d **−0.0637**, narrower floor wins 1 of 3 parents), and both lose
to doing nothing (C_LIVE 0.9747). The two 4b passes are reached by OPPOSITE choosers, so nothing was
chosen; the book underneath them is the record's existing MA-RS gate at gross 0.75 on a tranche whose
draws cover the parent — prior art, already among the committed 4b passers idea 774 declined to
claim. **No candidate, no memo, no rule change** (RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py untouched, rule 6).

## 5. Residue for the record (NOT a rules change; a Sunday-review proposal at most)

1. A per-parent draw floor must be quoted with its **k/M**, or in overlap-free units
   (`floor / sqrt((M-k)/(k(M-1)))`). Bare per-parent floors are not comparable across parents.
2. A max/min over three floors must be quoted against its own chi/bootstrap null (**1.268 median,
   1.660 at the 95th, at D = 24**); 567's 1.98x sits 1.19x above that null's median, and the spread
   at matched overlap does not clear it at all.
3. The 558 committed claims that were scored against U56's narrow bar were scored against a bar
   that is narrow for arithmetic reasons; idea 774's RSS assignment inherits the same defect.

**SURVIVORSHIP (rule 9):** U56 / B136 are current-constituent lists and SMALL665 a current sub-$2B
screen carried back to 2010, so every absolute level is an upper bound. The headline is a dispersion
across draws inside one parent on one tape, first-order immune to the level; the 4b pass counts are
not.

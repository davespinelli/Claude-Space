# Idea 497 — re-run-the-3-wide-and-unfolded-census-files-individually (lane B, 2026-09-10)

**ANSWERED, and the PREMISE IS KILLED. The queue's "3 files whose fit is both wide and
unfolded" are not wide. All three published fits reproduce exactly from their own committed
artefacts, and at runtime their largest design is p=6 on n=162 — p/n = 0.0370, so free R² is
at most 3.7%, not the >10-parameter regime idea 483's static flag implied. Substituting K-fold
predictions at four fold counts and five penalties (650 grid points) moves exactly ONE
published number: F1's best-fitting spec, which flips from the 4-parameter
`h* + episode + family` to `family` alone at 19 of 20 out-of-fold points. That flip
STRENGTHENS F1's own published conclusion rather than overturning it. Six of the seven
headline claims across the three files hold at every out-of-fold point. Rule 8: 78
walk-forward arms, 0 pass 4a, 0 pass 4b. No RULES change, no KEEP-candidate, no memo;
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.**

Script `2026-09-10_re-run-the-3-wide-and-unfolded-census-files-individually_B.py`; console
`.console.txt`; CSVs `.grid.csv` (650 points), `.verdicts.csv` (200 rows), `.walkforward.csv`
(78 arms). Runs standalone in ~40 s; reads only committed artefacts + `research/baseline.py`.

---

## The three files, and the instrument

Idea 483's cloud census scored 70 committed files on two **static** flags,
`has_fold_machinery` and `wide_design_hint`. Exactly 3 are wide-and-unfolded:

| | file | fit site | published block |
|---|---|---|---|
| F1 | `2026-09-06_can-a-panel-property-choose-the-cadence_cloud.py` | :344 `lstsq` | §2 decomp, 6 specs, n=115 books |
| F2 | `2026-09-06_does-the-cash-drag-share-depend-on-the-panel-or-on-the-gate-level_cloud.py` | :169 `pinv` | B3 full + 4 partial R², n=162 |
| F3 | `2026-09-06_is-phase-sensitivity-a-book-property-or-a-panel-one_cloud.py` | :398 `lstsq` | T1(i), 3 specs × 5 cadences, n=115 |

No book is re-run. Each design and target is rebuilt from that file's own committed CSVs
(F1's ladder from idea 175's committed `ladder.csv`, which F1 itself gates against at 1e-10),
so **stage 0 is an exact reproduction gate before anything is substituted**. Then, holding the
design fixed, the in-sample fitted value is replaced by an out-of-fold prediction, with the
published R²'s own denominator (full-sample `ȳ`), deterministic seed-497 folds identical
across specs inside a file, and a standardised ridge whose standardisation is fitted on the
TRAIN fold only. **λ = 0, K = IS is the file exactly as committed.**

**Params (2): fold count K ∈ {2, 5, 10, LOO}, penalty λ ∈ {0, 0.1, 1, 10, 100}.**

## (0) Reproduction gates — ALL PASS

F1 all six specs at max |Δ| 3.05e-16. F2 full R² and all four partial R² at max |Δ| 3.69e-05
(the console publishes 4 decimals; that is the printing, not the fit). F3 all fifteen numbers
at max |Δ| 4.46e-04 (same rounding limit).

## (1) THE PREMISE — none of the three is wide

| | published R² | n | p | p/n = free R² |
|---|---|---|---|---|
| F2 full (widest design here) | 0.6098 | 162 | 6 | **0.0370** |
| F1 `h* + episode + family` | 0.4518 | 115 | 4 | 0.0348 |
| F3 `both`, any cadence | 0.0361–0.4086 | 115 | 4 | 0.0348 |
| F2 partial `family` | 0.3739 | 162 | 1 | 0.0062 |

Max p/n over all 21 published sites is **0.0370**. `wide_design_hint` fires on the *text*
`get_dummies`/per-name in the source; at runtime every dummy block here is 1–2 columns
(3 panels, 2 families, 3 cadences). The queue's ask — "more than ~10 fitted parameters" —
describes none of these files, which agrees with lane C's independent finding that the
record's only over-bar linear-algebra site is idea 252's own.

## (2) WHICH PUBLISHED NUMBERS MOVE — 650 grid points, all in `.grid.csv`

Held-rate = share of the 20 **out-of-fold** (K × λ) points at which the published sentence
still reads the same:

| file | published claim | held IS (5) | held OOF (20) |
|---|---|---|---|
| F1 | properties add little over the family label | 5/5 | **20/20** |
| F1 | the 4-param spec is the best-fitting spec | 5/5 | **1/20** |
| F2 | LEVEL beats PANEL; largest partial R² is family | 5/5 | **20/20** |
| F3 | predictors beat family @2W | 4/5 | 16/20 |
| F3 | predictors beat family @6W / @8W / @10W | 5/5 each | **20/20** each |
| F3 | (control) @2M — F3 itself reports family > predictors | 0/5 | 0/20 |

**F1 — the one number that moves.** Published: `family` alone 0.4453, `h* + episode + family`
0.4518, so the properties add +0.0065 and the 4-parameter spec is the argmax. Out of fold the
increment is **negative at every point** (−0.0103 to −0.0542), and the argmax flips to
`family` alone at 19 of 20 OOF points (the exception is K=2, λ=100). The published +0.0065 is
free R² and nothing else. This does **not** overturn F1: its published sentence is that
neither property absorbs the family, and out of fold that reads *more* strongly, not less.

**F2 — the B3 answer is robust, and gets sharper.** `LEVEL` wins at all 25 points. Out of
fold the two dummy blocks published at +0.0020 (panel) and +0.0018 (cadence) go **negative**
(−0.0061 to −0.0209): they are worth less than nothing once they must predict rows they were
not fitted on, while `c_bar` (0.2708 → 0.2455–0.2844) and `family` (0.3739 → 0.3769–0.3980)
are undamaged. The published margin c_bar-over-panel *widens* out of fold.

**F3 — the large gaps are real, the small ones are penalty-fragile.** At 8W the predictors'
R² is 0.3067 in sample and 0.2676–0.2914 out of fold while family collapses 0.0677 → −0.0310
to +0.0388; at 10W, 0.3264 → 0.2045–0.3075 against family 0.0874 → −0.0822 to +0.0581. The
2W claim (published gap +0.0273) fails at exactly five points — **λ=100 at every K, in sample
included** — so that one is a *penalty* fact, not a folding fact, and 2W is the cadence where
F3's own gap was smallest to begin with.

**The dial that moves these files is the folding, not the penalty.** Across λ ∈ [0, 10] no
published number moves by more than 0.006; λ=100 shrinks everything toward the mean uniformly.
Switching IS → OOF moves F1's 4-param R² by 0.066, F3's 10W family R² by 0.170.

## (3) RULE 8 — F1's fit as a cadence selector, and both KEEP paths

Every input taken from IS ≤ 2016-12-31 only (`IS_Sharpe`, `hstarIS_IR_s21`,
`episode_days_IS`); 2017–2026 read once, to score. 78 arms = 3 fitted specs × 5 K × 5 λ + 3
no-fit references, all in `.walkforward.csv`.

| selector | mean OOS Sharpe | picked M | mean OOS CAGR | mean OOS MaxDD |
|---|---|---|---|---|
| constant 6W (no fit) | **0.7797** | 0/115 | 6.49% | −20.26% |
| constant M (no fit) | 0.7559 | 115/115 | 6.02% | −17.32% |
| IS-Sharpe argmax (incumbent) | 0.7449 | 109/115 | 5.93% | −17.68% |
| **every fitted arm, all 75 (K × λ × spec)** | **0.7559** | 115/115 | 6.02% | −17.32% |

The IS gap `IS_Sharpe(M) − IS_Sharpe(6W)` is positive on **94.8%** of books (mean +0.1355);
the OOS gap is positive on **27.0%** (mean −0.0238), Spearman(IS, OOS) = **−0.1801**. A fitted
predictor of a one-signed target is one-signed, so **every fitted arm at every fold count and
every penalty is the constant-M arm in disguise** — and constant M is the wrong constant. The
fit is not merely useless here; it reproduces the sign that reverses.

**Both KEEP paths: 4a 0/78 arms, 4b 0/78 arms, 0 book-level passes of either.** Protocol
comparands on U56, 10 bps, weekly, warm-up dropped:

| | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|---|
| RULES v2 baseline (live) | 8.63% | 1.202 | −12.05% | 1.231 / 1.180 | 9.48% | 1.279 | −12.05% |
| RULES v1 (previous) | 6.39% | 0.658 | −13.83% | 0.643 / 0.675 | 7.60% | 0.736 | −13.83% |
| SPY | 15.15% | 0.886 | −33.72% | 0.959 / 0.826 | 15.32% | 0.876 | −33.72% |

The best fitted arm's 0.7559 mean OOS Sharpe is below SPY's 0.876 and far below the live
book's 1.279. Nothing here is promotable, so no memo and no RULES wording.

## What this is worth to the record

1. `wide_design_hint` in idea 483's cloud census is a **static text flag with no runtime
   content**; three of its five hits are 1–6 parameter fits. Any future census that quotes it
   should publish p and n beside it.
2. The record now has one concrete case of an in-sample R² gain that is entirely free:
   F1's +0.0065 for two panel properties over a family label, which is −0.010 to −0.054 out
   of fold. It is small, and it points the same way F1 already published.
3. **A one-signed target is a silent selector-killer.** F1's IS gap is 95% one-signed, so no
   fit of it — at any fold count, any penalty, any spec — can produce a selector different
   from a constant. Any future "can property X choose dial Y" study should publish the sign
   balance of its target before fitting anything.

## Limits

The three designs are rebuilt from committed artefacts rather than by re-executing the three
files end to end, so this run gates on the published *fit inputs and outputs*, not on the
books upstream of them; F1's ladder is covered by F1's own 1e-10 gate against idea 175, F2's
and F3's inputs are the files' own written CSVs. The F2 and F3 gates are limited to 5e-5 and
5e-4 by the files' console print precision, not by the arithmetic. Survivorship: F1 and F3 run
on the 115-book corpus and F2 on SMALL439/U56/B136, all current constituents.

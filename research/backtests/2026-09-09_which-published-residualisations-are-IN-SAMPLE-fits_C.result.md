# Idea 483 — which-published-residualisations-are-IN-SAMPLE-fits (lane C, 2026-09-09)

> **This is a SECOND, INDEPENDENT RUN of idea 483.** The cloud lane answered it the same day
> with a *static* census (70 files carry a fit call, 5 wide, 3 wide-and-unfolded) plus a re-run
> on 600 fresh synthetic draw books. This run answers it by *runtime instrumentation of the
> record itself*. It **agrees** with the cloud run's headline (the >10-parameter regime is not
> the record; the typical fit is a 1–2 parameter slope), **corrects** its census (the exposed
> set is 134 sites in 7 scripts, 116 of them a groupby-mean family the static scan did not
> see), and **disagrees** with it on which dial dominates — see §2. Its conclusion about the
> book (fixing the fit changes the inference, not the book) is reproduced independently.

**ANSWERED. The census is mostly NEGATIVE and it re-labels the question. Idea 252's hazard —
`p` parameters fitted on the same `N` rows the fitted value is tested against, ONE-SIDED —
exists at exactly ONE linear-algebra site in the record, and that site is idea 252's own,
which already ran itself out of fold. The record's 134 over-the-bar sites are 116 two-sided
Frisch–Waugh within transforms, where in-sample fitting IS the estimator and "refit it out of
fold" is the wrong remedy. No RULES change, no KEEP-candidate, no memo; RULES.md,
PROTOCOL.md, scan.py, bot.py and baseline.py untouched.**

Script `2026-09-09_which-published-residualisations-are-IN-SAMPLE-fits_C.py` (`--sweep`
regenerates stage 0); console `.console.txt`; CSVs `.runtime.csv.gz` (302 043 instrumented fit
calls), `.sweepstatus.csv`, `.census.csv` (244 sites), `.highdim.csv`, `.artefacts.csv`,
`.freeR2.csv`, `.rerun.csv` (1 008 grid points), `.withindof.csv`, `.walkforward.csv` (258
rows). Sweep 270.6 min; the analysis itself re-runs from the committed log in 23 s.

---

## What was asked, and the instrument

The queue asked to *census the record for every control or residualisation fitted on the same
rows it is tested on, and re-run the ones with more than ~10 fitted parameters out of fold.*

A static scan cannot answer this: `p` and `N` are runtime facts. So every committed backtest
script carrying a linear-fit primitive or a groupby transform was **re-executed under an
instrumented numpy** — `lstsq`, `solve`, `pinv`, `inv`, `polyfit` and `GroupBy.transform` are
wrapped and log `(op, N, p, file, line)` at every call — inside a **write sandbox** that
redirects every write under the repo into a scratch mirror, so the sweep cannot touch a
committed artefact (`git status` after the sweep: clean). `solve`/`inv`/`pinv` see only a
`p × p` gram, so `N` is recovered from the caller's own design; a first pass that read the
gram's row count as `N` produced spurious `p == N` sites and was discarded and re-run.

**Coverage, stated plainly.** 446 committed backtest scripts. 81 contain a fit primitive or a
groupby transform and were swept; **all 81 produced a log** (21 did not exit 0 — 18 hit the
wall-clock cap, 3 raised; the cap was re-applied as SIGINT on a retry pass so the instrument
still dumps what it saw, and their calls up to that point are in the census). A further 177
scripts compute a correlation or covariance beta, which is a two-parameter in-sample fit by
construction (free R² = 2/N) and cannot cross the p>10 bar however it is counted. This run's
own script is excluded from its own census.

## The right statistic is p/N, not p

For an OLS fit whose design knows nothing about the target, the in-sample R² has expectation
**p/N** whatever the data say — that is the share of *any* regressor the control absorbs for
free. Monte Carlo at the record's own (N, p) pairs, 200 draws, for a continuous design and for
balanced group indicators (the `groupby().transform("mean")` form):

| N | p | p/N | mean R², dummy | mean R², gauss |
|---|---|---|---|---|
| 21 | 7 | 0.333 | 0.311 | 0.288 |
| 78 | 15 | 0.192 | 0.183 | 0.186 |
| 400 | 36 | 0.090 | 0.088 | 0.086 |
| 150 | 138 | 0.920 | 0.919 | 0.922 |
| 50 | 136 | ≥1 | 1.000 | 1.000 |

## (1) THE CENSUS

244 distinct `(script, file, line, op, p)` sites, 302 043 calls, 55 scripts. **134 sites are
over the queue's p>10 bar, in 7 scripts.** Site-level p distribution below the bar: p=2 at 64
sites, p=7 at 13, everything else in ones and threes.

**p>10 is necessary but not sufficient.** Idea 252's hazard needs the fitted value used
ONE-SIDED — as a regressor whose coefficient is then tested, or as a residual read as signal —
on its own fitting rows. When the same fit is removed from BOTH sides (`x` and `y` demeaned by
the same cell means), that is the Frisch–Waugh within transform: the in-sample fit *is* the
estimator, it is unbiased, and refitting it out of fold is the wrong question. Splitting the
134 by whether the same script/function/op/p/N carries two or more fits:

| sided | op | sites | scripts | p range | max p/N |
|---|---|---|---|---|---|
| two-sided (within transform) | gb_s_mean | **116** | 2 | 11–5164 | 0.250 |
| ONE-SIDED | gb_s_mean | 13 | 3 | 12–91 | 0.167 |
| ONE-SIDED | gb_s_lambda | 1 | 1 | 24 | 0.059 |
| ONE-SIDED | solve (ridge) | **4** | 1 | 136–138 | **3.044** |

The four `solve` sites are idea 252's membership ridge — **the record's only over-bar
linear-algebra fit, and the only one the queue's hazard actually describes.** It is also the
one run that already read itself out of fold.

**What the record calls a "control" is usually not a fit.** Of 2 148 committed CSVs, **117
carry a control-BOOK column** — a matched comparand *backtest*, which fits no parameters and
cannot absorb a regressor — and 30 carry a residual column, of which 21 come from scripts the
sweep saw fit nothing at all: they are arithmetic decomposition identities (total − timing −
composition), p = 0.

## (2) THE RE-RUN — 1 008 grid points, all reported

Reproduction gate first: this run's ridge/fold machinery reproduces **288 of idea 252's 288
committed `regressions.csv` rows** (its OOF == this run's folds=10) at max abs diff 1.25e-16
(R2_sd) / 1.11e-16 (R2_F) / 8.95e-13 (pR2) / 8.88e-16 (t) / **3.01e-11 (kill_F)**. Idea 83's
membership matrix is re-derived from `SEED_B+k` at 8.327e-17 over 300 rows, and `gridB.csv`
vs `draws.csv` at 0.000e+00 over 20 numeric columns. No book is re-run.

Headline cell (n=20, pooled, CAND Sharpe; N=150, p=138, p/N = 0.92), `kill` = pR²(sd|F)/R²(sd),
idea 252's column, bar `kill < 1/3`:

| λ | IS | OOF2 | OOF5 | OOF10 | OOF25 | OOF50 |
|---|---|---|---|---|---|---|
| 0.0 | 0.012 | 1.008 | 1.019 | 0.984 | 0.853 | 0.830 |
| 0.5 | **0.000** | 0.781 | 0.762 | 0.762 | 0.647 | 0.644 |
| 2.0 | 0.005 | 0.764 | 0.680 | **0.675** | 0.593 | 0.591 |
| 8.0 | 0.044 | 0.758 | 0.622 | 0.599 | 0.555 | 0.551 |
| 32 | 0.139 | 0.856 | 0.650 | 0.614 | 0.573 | 0.566 |
| 128 | 0.348 | 1.036 | 0.853 | 0.805 | 0.741 | 0.728 |
| 512 | 0.799 | 1.016 | 1.047 | 1.094 | 1.041 | 1.040 |

**The fold count is not the dial; the IS/OOF switch is.** Across K = 2…50 the headline `kill`
moves by at most 0.14; switching from the in-sample fit to any out-of-fold fit moves it by
0.76. **This is the opposite ordering to the same-day cloud run of this idea**, which reported
that "the IS-vs-OOF gap at fixed lam never exceeds 0.13" and that "the dominant dial is the
penalty, not the folding". That was measured on 600 fresh synthetic draw books at p/n
0.28–2.20; this is measured on idea 252's own committed rows at p/N 0.92. Both dials move the
answer — along λ at fixed OOF10 `kill` runs 0.98 → 1.09 — but **on the actual site the folding
is the larger of the two**, and a residualisation should be quoted with both. Pooled over all 1 008 points: in sample R²(sd~M) median 0.9125, `kill` median 0.090,
the control "kills" sd on **115 of 168** cells and leaves |t(sd|F)|<2 on 145 of 168. Out of
fold: R²(sd~M) median 0.0717, `kill` median 0.857, kills sd on **61 of 840** points — and per
cell, on **29 of 168 at any fold count and 3 of 168 at every fold count.** The in-sample and
out-of-fold verdicts **disagree on 126 of 168 cells**. Idea 252's K=10 reading is not a
fold-count artefact.

## (3) THE OTHER FAMILY — priced, not refitted

For the 116 two-sided sites the slope is the within estimator and is unbiased; the only cost is
p degrees of freedom, so a t read with dof N−2 instead of N−p−1 is overstated by
√((N−2)/(N−p−1)). Over those sites: **median inflation 1.0511, q90 1.1002, max 1.1530**
(p=56 on N=224). Monte Carlo with x and y INDEPENDENT, 200 draws, share of draws clearing
|t|>2 (a correct procedure sits at 0.05):

| N | p | naive dof | correct dof | leave-one-out |
|---|---|---|---|---|
| 224 | 56 | 0.095 | 0.055 | 0.100 |
| 224 | 56 | 0.090 | 0.050 | 0.110 |
| 548 | 120 | 0.080 | 0.025 | 0.070 |

**The naive-dof within-cell t roughly doubles the false-positive rate at the record's worst
p/N, and leaving one out does NOT fix it** — the remedy for this family is the degrees of
freedom, not a fold split. (The record's largest such site, `within_cell_fit`, already uses
cluster-robust SE, which sidesteps the dof question entirely.)

## (4) RULE 8 — the control as a SELECTOR, and both KEEP paths

Parameters chosen on 2009–2016 only (`Sharpe_IS`, `sd_IS`, membership); 2017–2026 read only to
score the pick, from idea 78's committed columns. 258 rows = 2 fitted selectors × 6 schemes ×
7 penalties × 3 k-cells + 2 no-fit references × 3 k-cells. B136: SPY 15.23%/0.889/−33.72%,
OOS Sharpe 0.882; RULES v2 8.03%/1.106/−12.24%, OOS Sharpe 1.119.

| selector | scheme | mean OOS Sharpe | mean OOS rank /50 | same pick as reference |
|---|---|---|---|---|
| RAW-sd (no control at all) | none | **1.1163** | 8.0 | — |
| IS-Sharpe argmax (incumbent) | none | 1.0657 | 8.0 | — |
| CTRL-fit | **IS** | 1.0590 | 9.3 | **19/21 = the incumbent** |
| CTRL-fit | OOF2/5/10/25/50 | 0.998–1.088 | 11.1–22.0 | 0–4/21 |
| SD-resid | IS | 1.0315 | 14.9 | 0/21 vs raw sd |
| SD-resid | OOF2…50 | 1.028–1.062 | 10.8–15.7 | 0–2/21 vs raw sd |

**An in-sample fitted control is the incumbent selector in disguise: it picks the IS-Sharpe
argmax on 19 of 21 cells, and out of fold on 0–4.** And no fitted-control arm, in sample or
out of fold, beats simply ranking on raw dispersion with no control at all.

**Both KEEP paths: 4a 24/258 against the live RULES v2, 4b 110/258 against SPY, both 0/258.**
Binding 4b bars: CAGR 97, H2 37, DD 26, OOS 11, H1 4. Nothing is promotable, so no KEEP and no
memo. RULES.md untouched.

## Incidental, for the record

Three scripts fail their own reproduction gates when re-executed today —
`2026-09-07_does-a-levered-f-060-book-clear-the-CAGR-floor_C.py` aborts on *"idea 138
reproduction FAILED on the exact subset"*, and two others raise. Not investigated here; the
sweep only observed it. Queued as a follow-up.

## Limits

The 13 one-sided `gb_s_mean` sites (p 12–91, p/N ≤ 0.167) are demeanings of a single column
whose leave-one-out restatement is an exact per-cell rescaling by m/(m−1) — bounded, and
typically 1/(1 − p/N) ≤ 1.20 at the record's worst — but they were **not** restated on their
own data here, because the sweep records p and N and not the cell-size vector. That is the one
piece of the queue's ask this run leaves open, and it is queued.

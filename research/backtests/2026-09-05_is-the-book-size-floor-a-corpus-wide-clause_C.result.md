# Idea 209 — is-the-book-size-floor-a-corpus-wide-clause (lane C, 2026-09-05)

**VERDICT: ANSWERED — NO. The size floor is a UNIVERSE clause, not a PROTOCOL one. The sign
reverses at exactly one boundary — the sub-$2B panel — and it reverses on every axis measured:
in the archive (LARGE ρ = +0.674, 97 of 101 cells positive; SMALL ρ = −0.361, 2 of 34
positive, across 17 independent scripts), in a fresh corpus where `n` is the swept axis rather
than a derived share (u56 +0.866 and broad +0.880, 24 of 24 arm-cells positive; small +0.197,
7 of 12, and NEGATIVE in 4 of 6 ranking keys at 25 bps), and in what the floor actually earns
out of sample (rule 8, `n >= 25`: +0.2252 paired OOS Sharpe on the large panels against
+0.0467 on the small one; the unbounded `BIGGEST BOOK` is +0.2992 large and −0.0060 small).**
Idea 199's clause is confirmed where it was measured and refuted as a corpus-wide statement.
Rules unchanged; no book proposed.

Script: `2026-09-05_is-the-book-size-floor-a-corpus-wide-clause_C.py` (464 s, 384 backtests +
a 497-file archive scan, seed 20260905, no `hash()`-derived seeds). Outputs: `.console.txt`,
`.census.csv`, `.corpus.csv`, `.cellrho.csv`, `.confound.csv`, `.walkforward.csv`,
`.summary.csv`.

---

## 1. PART A — the archive census (the queue's literal ask)

Every committed CSV under `research/backtests/` was re-read. A file is **usable** only if it
publishes a book-size column `n` (≥ 3 distinct book-size-like values) *and* its own
out-of-sample Sharpe. Cells are the file's own context columns (`corpus`, `panel`, `cost`,
`signal`, `g`, `scaler`, …); ρ is Spearman within the cell, over whatever varies inside it
(arms, shares, keys, draws) — idea 199's convention.

| | count |
|---|---|
| CSVs scanned | 497 |
| usable (publish both `n` and an own OOS Sharpe) | **17** |
| cells with a computable ρ | **135** |
| distinct underlying corpora (after collapsing republished cells) | **70** |

| panel class | cells | mean ρ(n, OOS Sharpe) | median | positive | distinct-corpus cells | distinct positive |
|---|---|---|---|---|---|---|
| **LARGE** (u56 / broad) | 101 | **+0.674** | +0.730 | **97 (96.0%)** | 49 | 46 (93.9%) |
| **SMALL** (sub-$2B) | 34 | **−0.361** | −0.458 | **2 (5.9%)** | 21 | 1 (4.8%) |

Descriptive Welch t(LARGE−SMALL) = **+19.78** — reported as a description only: cells share
panels, scripts and one OOS window, so the effective sample is far below 135 and this is not a
p-value. What survives that discount is the count: **not one of the 17 scripts disagrees about
the sign of the panel split.** Idea 199's own −0.482 small-panel figure is reproduced exactly
and appears four times in the archive under four different script names, which is why the
de-duplicated column is given beside the raw one.

**Coverage is the census's real limitation, and it is severe: 480 of 497 CSVs are unusable**,
almost all because `n` is published as a single value or two (the file swept something else and
fixed the book size). A clause about `n` can only be back-checked where `n` was varied, and the
project has varied it in 17 files.

## 2. PART B — a fresh corpus where `n` is exogenous

The archive's `n` is nearly always *derived* (a share `m` of the eligible pool), so its
correlation with anything is confounded with `m`. Here `n` is the swept axis itself: top-`n`
equal weight among RULES-v1-eligible names (above 200d, vol20 < 0.60), g = 0.75, weekly, t+1.
384 books = 3 panels × 2 cost rungs × 6 ranking keys × up to 11 values of `n`. All reported.

ρ(n, ·) within each (panel, cost) cell, arms pooled:

| panel | cost | ρ(n, OOS Sharpe) | ρ(n, −OOS MaxDD) | ρ(n, IS Sharpe) | ρ(n, OOS CAGR) |
|---|---|---|---|---|---|
| u56 | 10 / 25 | **+0.677 / +0.624** | −0.536 / −0.674 | +0.074 / +0.192 | −0.074 / −0.032 |
| broad | 10 / 25 | **+0.515 / +0.422** | −0.434 / −0.547 | +0.161 / +0.160 | −0.006 / +0.029 |
| **small** | 10 / 25 | **+0.296 / +0.085** | −0.730 / −0.682 | +0.327 / +0.369 | −0.130 / −0.030 |

Per ranking key (`ρ(n, OOS Sharpe)`, every key reported):

| panel | cost | COMP | NOVOL | MOM | R6 | INVVOL | RND |
|---|---|---|---|---|---|---|---|
| u56 | 10 / 25 | +0.988 / +1.000 | +0.879 / +0.879 | +0.600 / +0.600 | +0.867 / +0.867 | +0.988 / +0.988 | +0.891 / +0.842 |
| broad | 10 / 25 | +0.873 / +0.973 | +0.945 / +0.945 | +0.655 / +0.600 | +0.882 / +0.873 | +0.909 / +0.945 | +1.000 / +0.964 |
| **small** | 10 / 25 | **+0.355 / −0.555** | +0.664 / +0.718 | +0.745 / +0.745 | **+0.000 / −0.064** | **+0.282 / −0.655** | **+0.327 / −0.200** |

u56 **12 of 12** arm-cells positive (mean +0.866); broad **12 of 12** (+0.880); small **7 of
12** (+0.197), and at 25 bps four of the six keys are negative. Two things follow. (a) The
large-cap effect is not a property of one ranking key — a *random* key gives +1.000 and +0.964,
so this is de-concentration, not selection, exactly as idea 199 concluded. (b) On the small
panel the honest description is **not "the sign reverses" but "the effect is absent and its
sign is set by the ranking key and the cost rung"** — a weaker and less tidy claim than idea
199's −0.48/−0.28, which came from a corpus with derived `n`.

Drawdown is the one thing that behaves the same everywhere: ρ(n, −OOS MaxDD) is −0.43 to −0.73
on all three panels, *strongest on the small one*. Bigger books are shallower everywhere; only
on large caps is that shallowness also worth Sharpe.

## 3. The confound, tested rather than asserted

On u56 the top of the ladder (n = 40) **is** the entire eligible pool (median breadth 40); on
the small panel n = 60 is still a 39% slice. So "bigger is better on large caps" could just be
"the large ladders run out of pool and the small one does not". Two matched windows:

| panel | cost | breadth | max n/pool | ρ all n | ρ on n ∈ [5,40] | ρ on n/pool ∈ [0.05,0.40] |
|---|---|---|---|---|---|---|
| u56 | 10 / 25 | 40 | 1.000 | +0.677 / +0.624 | +0.664 / +0.622 | **+0.291 / +0.236** (n ∈ [2,15]) |
| broad | 10 / 25 | 98 | 0.612 | +0.515 / +0.422 | +0.348 / +0.293 | **+0.299 / +0.250** (n ∈ [5,30]) |
| small | 10 / 25 | 153 | 0.392 | +0.296 / +0.085 | +0.110 / −0.082 | **−0.003 / −0.070** (n ∈ [8,60]) |

**The confound is real and about half the raw large-cap effect is it** — matching on share of
pool cuts u56 from +0.68 to +0.29 — **but it does not explain the panel split**: at matched
share the large panels stay at +0.24…+0.30 and the small panel sits at zero or below. Anyone
quoting idea 199's +0.79 large-cap ρ should quote +0.29 instead.

## 4. Rule 8 — what the floor actually earns, by panel class

Picks chosen on IS (≤ 2016-12-31) only; 2017-01-01 → read once. Six (panel, cost) cells, paired
against `S0` = the unconstrained IS-Sharpe argmax. **The floor k is the run's only tuned
parameter and every value is reported.**

| selector | mean OOS Sharpe | mean OOS CAGR | mean OOS MaxDD | dOOS | t | W/L/T | mean n | **dOOS LARGE** | **dOOS SMALL** | OOS-4b clears | 4a | 4b |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S0 do-nothing (IS-Sharpe argmax) | 0.6823 | 14.05% | −29.09% | — | — | — | 10.8 | — | — | 0/6 | 1 | 0 |
| FLOOR n ≥ 5 | 0.7443 | 13.46% | −24.25% | +0.0620 | +2.16 | 3/0/3 | 12.7 | +0.0930 | +0.0000 | 0/6 | 1 | 0 |
| FLOOR n ≥ 10 | 0.7948 | 12.61% | −22.96% | +0.1124 | +2.93 | 4/0/2 | 16.7 | +0.1686 | +0.0000 | 2/6 | 1 | 2 |
| FLOOR n ≥ 15 | 0.7857 | 10.58% | −21.52% | +0.1033 | +3.03 | 5/0/1 | 25.0 | +0.1317 | +0.0467 | 3/6 | 2 | 3 |
| FLOOR n ≥ 20 | 0.7955 | 10.28% | −21.42% | +0.1132 | +2.89 | 5/0/1 | 26.7 | +0.1464 | +0.0467 | 3/6 | 2 | 2 |
| **FLOOR n ≥ 25** | **0.8480** | 10.44% | −20.89% | **+0.1657** | +3.07 | 5/0/1 | 30.0 | **+0.2252** | **+0.0467** | 3/6 | 2 | 2 |
| FLOOR n ≥ 30 | 0.8328 | 8.45% | −19.31% | +0.1505 | +1.67 | 4/1/1 | 40.0 | +0.2024 | +0.0467 | 1/6 | 3 | 1 |
| BIGGEST BOOK (no fitting at all) | 0.8798 | 8.83% | −18.88% | +0.1975 | +2.37 | 5/1/0 | 53.3 | **+0.2992** | **−0.0060** | 2/6 | 4 | 1 |
| ORACLE-OOS (ceiling, not implementable) | 0.9378 | 10.52% | −20.48% | +0.2554 | +3.93 | 6/0/0 | 40.0 | +0.3105 | +0.1453 | 2/6 | 5 | 1 |

Idea 199's headline is **directionally reproduced on a corpus it never saw** — every rung beats
do-nothing on mean OOS Sharpe and on OOS drawdown, `n ≥ 25` is the best rung, and the CAGR
price is the same one (14.05% → 10.44%, a 3.6pp surrender). What the split column adds is that
**the entire premium is the large panels.** On the small panel the floor never loses, but it
buys +0.0467 of OOS Sharpe once and nothing at all below k = 15, and taking it to the extreme
(`BIGGEST BOOK`) turns *negative*. The ORACLE row says the small panel does contain +0.145 of
findable OOS Sharpe — the floor just is not the instrument that finds it.

The ladder is **not monotone** (k = 15 at +0.1033 sits below k = 10 at +0.1124; k = 30 falls
back to +0.1505 and loses a cell), and k = 25 sits one rung from the grid edge. Idea 199's
"k in the twenties, not 25" survives; "25" does not.

## 5. Both KEEP paths

Full sample, g = 0.75, weekly, t+1. Benchmarks: SPY 15.23% / 0.889 / −33.72%, halves
0.957/0.834 (small panel's own window: 14.13% / 0.862 / −33.72%). RULES v1: u56@10bps 6.45% /
0.664 / −13.83%; broad@10bps 6.39% / 0.635 / −21.19%; small@10bps 13.55% / 0.523 / −44.83%.

* **Pool-wide:** 95 of 384 books pass 4a, **28 pass 4b**, 48 clear the OOS-window 4b.
* **Every 4b pass is a large-cap book at 10 bps** (26 of 28; the other two are u56 at 25 bps).
  **0 of 132 small-panel books pass 4b at any n, any key, either cost rung** — independent
  confirmation of queue idea 136's premise.
* **4a and 4b together:** only on broad@10bps, where the `R6` ladder passes both from n = 8 to
  n = 60.

**By-product KEEP-candidate (memo'd, NOT proposed):** the rule-8 `FLOOR n ≥ 25` pick on
broad@10bps is `R6@n=25` — top 25 by 6-month return among eligible, equal weight, g = 0.75,
weekly — **14.1% / 1.061 / −18.9%, halves 1.219 / 0.920, OOS 13.7% / 1.013 / −18.9%, turnover
13.1×/yr, passing 4a AND 4b on all five bars.** It was selected out of sample by a
pre-registered floor, not chosen by looking at it. It is **not** offered for Sunday review:
it dies at 25 bps (4b fail), it exists only on the broad panel, its H2 (0.920) is thinner than
the standing idea-178 candidate's, and 13.1×/yr turnover is above the standing candidate's
10.2×. It is recorded so the next run does not rediscover it as new.

## 6. Caveats, carried not buried

* **Census coverage is 17 of 497 files.** The conclusion is about the corpora that varied `n`,
  not about the LEADERBOARD as a whole. Files where `n` is fixed cannot speak to this either
  way, and I did not re-run any of them.
* **The 135 cells are not 135 experiments.** 70 survive de-duplication and even those share
  three panels, one OOS window and a handful of book families. Every t here is descriptive.
* **The panel split is one boundary observed once.** "LARGE vs SMALL" is u56/broad against one
  sub-$2B panel; there is no second small-cap universe in the project to replicate on. The
  clause could equally be about breadth, liquidity, or the panel's construction rather than
  market cap. Idea 195's market-cap leg is still uncached, so this cannot be decomposed.
* **SURVIVORSHIP (idea 54):** all three panels are current constituents; the small panel has no
  delistings, which if anything *flatters* it. Every selector reads the same biased panel, so
  the comparison is unaffected, but no level here is a tradable estimate.
* **Idea 38:** u56/broad carry the calendar-day index after 2014-09-17. **Idea 126:** t+1 only.
* Predictions were **not** pre-registered for this run, so none are claimed. What would have
  falsified the conclusion: any large-cap cell with ρ < 0 that was not a 3-point ladder (one
  exists, broad/MOM/10bps at −0.472, out of 101), or a matched-share window that collapsed the
  panel gap (it halved the large-cap effect and left the gap intact).

## 7. Proposed PROTOCOL wording, report-only, for Sunday review (evidence, not a rule change)

> **Idea 199's book-size floor is universe-conditional and must be stated as such.** On the
> large-cap panels (u56, broad) a bigger book is better out of sample — ρ(n, OOS Sharpe) =
> +0.674 across 101 archive cells from 17 independent scripts (96% positive), +0.866 / +0.880
> on a fresh corpus with `n` swept directly (24 of 24 arm-cells positive, a *random* ranking key
> included), and a pre-registered floor `n ≥ k` for k in the twenties returns **+0.2252** paired
> OOS Sharpe against the unconstrained IS-Sharpe argmax. **On the sub-$2B panel the effect is
> absent** (archive ρ = −0.361, 2 of 34 cells positive; fresh corpus +0.197 with four of six
> ranking keys negative at 25 bps), the floor returns **+0.0467**, and removing the ceiling
> entirely turns it negative (−0.0060). About half the large-cap correlation is the ladder
> reaching the whole eligible pool: matched on share of pool it falls from +0.68 to **+0.29**,
> and that is the figure to quote. Any walk-forward that applies a size floor must name the
> panel it applies to; on a small-cap panel the floor is not supported by this evidence.
> Separately, ρ(n, −OOS MaxDD) is −0.43…−0.73 on *all* panels, so a floor may still be
> defended as drawdown control everywhere — but not as a Sharpe instrument outside large caps.

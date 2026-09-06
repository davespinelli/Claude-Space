# Idea 221 — is-phase-sensitivity-a-book-property-or-a-panel-one (cloud, 2026-09-06)

**VERDICT: KILL. It is NEITHER. Phase sensitivity is a panel-DATE effect: within a panel every
book is hit by the same phase on the same dates, so there is almost no book-level residual for a
book property to predict — and the two predictors the idea names are not it.**

Corpus: idea 175's 115 books verbatim (same seeds). 6 cadences × their phases = **3,680 runs**,
10 bps, t+1, IS ≤ 2016-12-31 / OOS 2017-01-01.. Two tuned params: cadence point (6, all reported)
× predictor (2, both reported). All four reproduction controls PASS, including the two decisive
ones: **[c] the phase grid reproduces idea 187's committed .phase.csv on all 2,300 rows at
2.220e-16**, and **[d] the episode machinery reproduces idea 76's committed episodes.csv on all
805 rows at 5.684e-14**. **[T4] Q (k=1 phase freedom) returns spread exactly 0.000e+00 on all 115
books** — the machinery returns zero where zero phase freedom exists.

## The per-book spread is 2.5x the family number idea 187 published — and they are not the same thing

Idea 187 averaged OOS Sharpe over books first and spread the family MEANS. The per-book spread
(mean over books of each book's own max−min) at 6W is **0.3787 ALL / 0.3459 SMALL / 0.3979 U56 /
0.4084 ETF**, against 187's 0.1518 / 0.2618 / 0.3957 / 0.3862. That U56 and ETF barely move
between the two definitions is the first sign of what T5 confirms.

## T1 — book or panel? Neither.

| cad | R² family alone | R² P1+P2 alone | R² both | ΔR² P1 given family | ΔR² P2 given family |
|---|---|---|---|---|---|
| mean over 5 cadences | **0.066** | 0.168 | 0.225 | +0.122 | +0.028 |

Family explains 3.8–11.2% of the variance in log spread. **And a book's phase sensitivity is not
even stable across independent cadences**: median pooled Spearman of per-book spread between
cadence pairs is **+0.086** over 10 pairs (within-family medians SMALL 0.061, U56 0.291, ETF
−0.035). A property that does not reproduce itself at a different block length is not a book
property.

## T2 — prediction: the pre-registered sign is REVERSED within family for P1

Pre-registration: P1 persistence NEGATIVE (long episodes ⇒ phase-insensitive), P2 eligible-name
turnover POSITIVE.

| predictor | pooled ρ (median over cadences) | within-family medians |
|---|---|---|
| P1 mean holding-episode length / block | −0.042 | SMALL **+0.130**, U56 **+0.540**, ETF **+0.177** |
| P2 eligible-name turnover | +0.034 | SMALL +0.148, U56 +0.029, ETF −0.024 |

The idea's mechanism — "a book whose episodes are long relative to the block should be
phase-insensitive" — is **wrong in sign within every family**, most strongly on U56 (ρ +0.540,
t +3.57 at 6W; +0.732, t +5.98 at 8W). Books that hold longer are *more* phase-sensitive, because
a longer episode means fewer, larger, less-diversified alignment bets.

The strongest cross-book correlate is neither predictor but the **control**: n_names, ρ −0.36 to
−0.40 pooled at 6W/8W/10W (daily selected-set churn, ρ −0.38 to −0.41, is its near-duplicate).
Small books have big phase spreads. That is a diversification effect, not a holding-period one.

## T3 — screenability: the only test that could have written a PROTOCOL clause. It fails.

Split at the **IS-only** median (no future information), the "predicted-insensitive" half must
have the lower realised OOS spread. P1 **HOLDS in 1 of 5 cadences, FAILS in 2** (at 6W the
predicted-insensitive half is *worse*: 0.4035 vs 0.3536, t −2.80). P2 holds in 2 of 5, fails in 1.
Median ratio 0.981 (P1) / 0.886 (P2). There is no screen here.

## T5 (POST-HOC, labelled) — the mechanism: phase is a panel-date shock, not a book trait

Added after T1–T3 came back null, to ask the prior question they assume: **is there any
book-level variation to predict?**

| cad | family | k | argmax agree | argmin agree | chance 1/k | common share |
|---|---|---|---|---|---|---|
| 6W | U56 | 6 | **0.97** | **0.97** | 0.17 | **0.906** |
| 6W | ETF | 6 | 0.67 | **1.00** | 0.17 | **0.936** |
| 2M | U56 | 2 | **1.00** | **1.00** | 0.50 | 0.910 |
| 8W | ETF | 8 | 0.73 | 0.94 | 0.12 | 0.842 |
| 6W | SMALL | 6 | 0.53 | 0.47 | 0.17 | 0.470 |

Median over all 15 (cadence, family) cells: **common share 0.675, argmax agreement 0.73 against a
chance rate of 0.17**. On the large-cap panels 62–94% of the phase variance is a single common
profile: **every book rebalances on the same dates and eats the same alignment draw.** There is
essentially no idiosyncratic residual, which is why no book property predicts it — and why 187's
family-mean spread (0.3957 U56) is nearly the whole per-book spread (0.3979). The small panel is
the partial exception (common share 0.279 at 6W, 0.046–0.696 overall), i.e. the one place phase
is partly idiosyncratic — and it is also the place both predictors are weakest.

## PROTOCOL rule 8 walk-forward — the screen destroys the value it was meant to protect

Parameters on IS only, OOS read once. REC = cadence by IS Sharpe at phase 0 (what the record
does). SCREENED = REC's cadence only where IS persistence ≥ the IS median, else fall back to W.

| family | arm | n | OOS CAGR | OOS Sharpe | OOS MaxDD | Δ vs CONST-W0 | t (paired) |
|---|---|---|---|---|---|---|---|
| ALL | CONST-W0 | 115 | 5.26% | 0.6798 | −17.05% | — | — |
| ALL | REC | 115 | 5.75% | 0.7186 | −17.98% | +0.0388 | 3.26 |
| ALL | **SCREENED** | 115 | 5.49% | **0.6949** | −17.36% | **+0.0151** | 1.80 |
| ALL | PHASE-AVG | 115 | 5.79% | **0.7223** | −17.72% | **+0.0425** | 3.53 |
| SMALL | SCREENED | 49 | 1.75% | 0.2077 | −24.03% | +0.0025 | 0.42 |
| U56 | SCREENED | 33 | 11.47% | 1.2074 | −15.13% | −0.0157 | −0.68 |
| ETF | SCREENED | 33 | 5.05% | 0.9058 | −9.70% | +0.0646 | 5.19 |

Benchmarks, same OOS window: **SPY 15.45% / 0.8820 / −33.72%**; RULES v1 **U56 7.73% / 0.7471 /
−13.83%**, **SMALL 6.35% / 0.4923 / −36.12%**. The screen admits 59/115 books and **keeps only 39%
of REC's OOS premium (+0.0151 of +0.0388)** — it is a filter with no information that mostly just
reverts books to weekly. **PHASE-AVG (idea 222's estimator) is the best arm at +0.0425, t 3.53**,
beating the record's own REC, and it needs no book property at all.

## KEEP paths — both evaluated on all 3,680 rows

4a: 404. 4b: 137, **all on U56** (SMALL 0/1568, ETF 0/1056). But **only 3 of 86 (book, cadence)
cells pass 4b at ALL of their own phases** — the other 83 are phase-conditional passes, i.e. a
book that clears 4b only because the sample happened to start where it did. **No candidate.** The
best cell, U56k20d05 @ 10W, passes at 5 of its 10 phases; it is a 20-name random sub-panel of a
current-constituent list and is not proposed for anything.

## Caveats

SURVIVORSHIP: SMALL439/U56/ETF36 and every sub-panel are current-constituent lists (idea 54);
the small panel drops the 44 max_1d_move ≥ 1.0 tickers per the standing rule. No level here is an
attainable return; the cross-book RANK tests that carry the conclusion are not driven by it.
Idea 38: large-cap panels are calendar-day indexed after 2014-09-17, so their phase spreads are a
LOWER bound. A phase is not a tradable choice — nothing here recommends picking one.

## What this says to the Sunday review

Idea 187's proposed PROTOCOL clause 12 ("report the effect against that cadence's own phase
spread") **should not be softened into a per-book screen** — this run tested exactly that and it
does not exist. T5 says why: phase is a property of the SAMPLE START DATE crossed with the panel's
dates, common to every book on that panel. The implementable response is idea 222's estimator, not
a screen: **trade the phase-averaged book** (k sub-books at 1/k each), which here is the best
walk-forward arm at +0.0425 (t 3.53) over the weekly incumbent and removes the alignment draw by
construction rather than warning about it.

RULES.md, scan.py, bot.py, baseline.py untouched.

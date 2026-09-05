# Idea 171 — do-gross-choice-rules-lose-to-constants-in-general (lane C, 2026-09-05)

**Verdict: ANSWERED. The general claim survives, but at 1 of 5 dials, not 5 of 5.**
Fitting a dial in-sample beats leaving it at its inherited constant on **exactly one** of the
project's five fitted dials — **CADENCE** — and on **zero** of five if the out-of-sample score is
the 4b margin rather than raw Sharpe. The one apparent second winner (SLEEVE) is a ladder-geometry
artefact, proven so by two controls.

Script: `2026-09-05_do-gross-choice-rules-lose-to-constants-in-general_C.py` ·
1908 ladder rows · 53 books · 10 bps · t+1 · IS ≤ 2016-12-31, OOS ≥ 2017-01-01 · 142 s.

## Design

Five dials, each swept over a ladder that **contains its own incumbent constant**, with the other
four held at their incumbents, on 53 books (5 fixed panels + 48 idea-78-style sub-panels of B136,
k ∈ {20,40,80} × 16 draws, seed 171500+k). 36 ladder points, all reported book-by-book.

| dial | ladder | incumbent | provenance of the constant |
|---|---|---|---|
| GROSS | 0.20…1.00 (10) | **0.75** | RULES v1's 5 × 15%; idea 78/166's static |
| N | 3…50 (10) | **20** | idea 2's 4b KEEP candidate |
| BAND | 0.00…0.08 (5) | **0.00** | RULES v1 / `scan.py` gate on a bare `px > MA200` |
| CADENCE | D, W, M, Q (4) | **W** | RULES v1 and `baseline.compare()`'s default |
| SLEEVE | 0.00…0.30 (7) | **0.00** | no sleeve in RULES v1 or the 4b candidate |

Two tuned parameters (PROTOCOL rule 4): the **selector** (SEL-SHARPE = IS Sharpe argmax, the
project's incumbent rule-8 selector; SEL-4B = IS 4b relative-min-margin argmax, idea 166's MAXMARG)
× the **ladder point**. Dial and book are corpus axes. Three controls, none tuned: **CONST**
(do nothing), **RANDOM** (a uniformly random ladder point, idea 151's control), **ORACLE** (the OOS
argmax — not implementable, an upper bound).

**Reproduction, asserted before any new number was read.** [a] the vectorised `fast_backtest`
reproduces `products/backtester/engine.backtest` to max |Δreturn| ≤ 6.2e-17 and |Δturnover| ≤
1.2e-15 at all four cadences — PASS. [b] at BAND = 0 the CAND-20 weights equal idea 78's
`weights_cand` **exactly** (max |Δw| = 0.000e+00 on U56, B136, BSTK100) — PASS. The incumbent cell
is idea 78's book, not a look-alike.

## The count

| selector | OOS score | ahead on | ahead **and** sign-test p < 0.05 | dials |
|---|---|---|---|---|
| SEL-SHARPE (incumbent) | OOS Sharpe | 3/5 | **2/5** | CADENCE, SLEEVE |
| SEL-SHARPE (incumbent) | OOS 4b margin | 1/5 | **0/5** | — |
| SEL-4B | OOS Sharpe | 4/5 | **2/5** | CADENCE, SLEEVE |
| SEL-4B | OOS 4b margin | 4/5 | **2/5** | N, SLEEVE |
| RANDOM *(control)* | OOS Sharpe | 2/5 | **1/5** | SLEEVE |

Paired over 53 books, exact two-sided binomial sign test:

| dial | SEL-SHARPE mean Δ OOS Sharpe | t | win/loss | sign p | verdict |
|---|---|---|---|---|---|
| GROSS | **−0.0006** | −4.24 | 14/39 | 0.0008 | **fitting LOSES** |
| N | −0.0215 | −1.47 | 20/21 | 1.00 | behind, n.s. |
| BAND | +0.0085 | +1.08 | 27/23 | 0.67 | ahead, n.s. |
| CADENCE | **+0.0642** | +4.54 | 40/11 | 0.0001 | **fitting WINS** |
| SLEEVE | +0.1801 | +37.73 | 53/0 | 0.0000 | wins — but see below |

## Why SLEEVE is not a win (two controls, both decisive)

1. **The selector is byte-identical to the oracle.** SEL-SHARPE picks f = 0.30 in **53 of 53**
   books; so does ORACLE. Agreement 100.0%. The mean-OOS-Sharpe ladder is monotone in f
   (Spearman ρ = +1.000) and truncated at 0.30, so the "selector" is not choosing — it is running
   to the edge of the grid. Extend the grid and it runs further.
2. **The random control wins too.** RANDOM banks 55.5% of the oracle's gain on SLEEVE
   (+0.1000, t = +11.2, p < 1e-4). A dial where coin-flipping beats the constant is a dial whose
   ladder slopes, not a dial where fitting has skill.

Capture ratio — the share of the oracle's OOS-Sharpe gain each arm actually banks:

| dial | ORACLE gain | SEL-SHARPE | SEL-4B | RANDOM | reading |
|---|---|---|---|---|---|
| GROSS | +0.0014 | −40.2% | −36.8% | +21.2% | loses to the constant |
| N | +0.0900 | −23.9% | +4.7% | −45.8% | loses to the constant |
| BAND | +0.0325 | +26.2% | +18.3% | −15.3% | not significant |
| **CADENCE** | **+0.0956** | **+67.1%** | +48.0% | −33.0% | **selector skill** |
| SLEEVE | +0.1801 | +100.0% | +15.7% | +55.5% | it *is* the ladder's endpoint |

CADENCE is the only dial that clears all four bars at once: beats the constant, significantly,
by more than the random control does, and is **not** merely the endpoint of a monotone ladder
(oracle sits at an interior point in 96.2% of books; SEL-SHARPE agrees with it in 75.5%,
choosing M in 44/53, while ORACLE chooses M in 48/53).

## Why the 4b margin flips the answer to 0 of 5

The dial that wins on Sharpe **loses on the score PROTOCOL actually grades against**. Under
SEL-SHARPE the mean Δ in the OOS 4b relative min-margin is CADENCE −0.0473, SLEEVE −0.0304
(p = 0.0008), and no dial is significantly positive. Mechanism, visible in the ladder means: gross,
sleeve and cadence all buy Sharpe by **surrendering CAGR**, and 4b's floor (CAGR ≥ 70% of SPY's) is
the bar that then binds. Mean OOS CAGR across the 53 books: CONST 9.96% → SEL-SHARPE 8.82% on
SLEEVE, with mean OOS Sharpe 0.964 → 1.144 and mean OOS MaxDD −17.18% → −12.56%. The book gets
safer and lower-returning; 4b counts that as a loss.

## GROSS reproduces idea 166 exactly as predicted (P2 HIT)

Mean OOS Sharpe across the gross ladder is **flat to 0.001** (0.964 at every point from 0.20 to
1.00) — gross is a near-pure scale lever, so the Sharpe ladder is degenerate and any IS Sharpe
argmax is chasing noise. SEL-SHARPE consequently picks g = 1.00 in **50 of 53** books and loses
(p = 0.0008). The 4b-margin ladder is *not* flat and peaks at g = 0.80 (−0.158) with 0.75 at
−0.161 and 0.70 at −0.179 — idea 166's 0.70–0.80 plateau, reproduced on a different corpus.

## PROTOCOL rule 8 walk-forward

The design *is* the walk-forward: every selector reads ≤ 2016-12-31 only; 2017→ is read once.
Mean OOS across the 53 books (benchmarks: SPY OOS CAGR 15.45% / Sharpe 0.882 / MaxDD −33.72%;
RULES v1 OOS Sharpe 0.576 on B136, 0.747 on U56, 0.605 on SMALL):

| dial | arm | OOS CAGR | OOS Sharpe | OOS MaxDD | OOS 4b pass |
|---|---|---|---|---|---|
| — | CONST (all dials) | 9.96% | 0.964 | −17.18% | 11/53 |
| CADENCE | SEL-SHARPE | 11.55% | **1.028** | −20.00% | 6/53 |
| CADENCE | SEL-4B | 11.30% | 1.010 | −20.03% | 10/53 |
| SLEEVE | SEL-SHARPE | 8.82% | **1.144** | −12.56% | 7/53 |
| SLEEVE | SEL-4B | 9.65% | 0.992 | −16.06% | **18/53** |
| GROSS | SEL-SHARPE | 13.00% | 0.963 | −22.25% | 5/53 |
| N | SEL-SHARPE | 10.84% | 0.942 | −18.36% | 8/53 |
| BAND | SEL-SHARPE | 10.29% | 0.972 | −17.72% | 10/53 |

Note the sign disagreement that runs through the whole run: **every arm that raises mean OOS
Sharpe lowers the OOS 4b pass count**, and the single best 4b-pass arm (SLEEVE/SEL-4B, 18/53) is
not the best Sharpe arm. Classic S1 book-pick (best IS Sharpe book, read once OOS): under CADENCE
every arm except CONST beats both SPY and RULES v1 (SEL-SHARPE B136k80d13 @ M: 12.56% / 0.994 /
−21.57%); CONST does not (0.808). That is the same finding at the book level.

## Both KEEP paths (PROTOCOL rule 4), all 1908 rows

- **4a: 1507/1908 pass.** (4a's drawdown test is against RULES v1's −13.8% to −21.2%, which most
  of these books clear.)
- **4b: 250/1908 pass.** Binding bars across all rows: **CAGR 1223**, H2 689, DD 447, OOS 405, H1 312
  — the CAGR floor is the most-violated bar by a wide margin, which is exactly why every
  Sharpe-raising arm above loses on the 4b margin.
- **214 of the 250 are sub-panel books** — a corpus device, not tradable, and not proposable.
- **36 are on the fixed panels** (U56 20, B136 7, BSTK100 9), and every one is a
  re-parameterisation of a book already in the record (idea 144's convention).

**One of them is walk-forward-supported and is written up as a by-product KEEP-candidate:**
`U56 / CADENCE = M` — the standing top-20 EW book rebalanced monthly instead of weekly. Both
selectors pick M on U56 from the IS window alone, and M is also the oracle. Full sample
14.8% / **1.208** / −19.6%, halves 1.219/1.206, OOS Sharpe **1.287**, turnover **4.28×/yr** vs
9.45× — against the incumbent weekly 12.9% / 1.108 / −18.2%, OOS 1.177, and SPY 15.2% / 0.889 /
−33.7%, OOS 0.882. See `.memo.md`. **Two blockers are stated there, not buried: the drawdown
margin is 0.6 pp, and the same move fails 4b on the broad universe by 5.9 pp of drawdown.**

## Predictions scorecard (written before any number was read)

| | prediction | outcome |
|---|---|---|
| P1 | reproduction [a]+[b] hold | **HIT** |
| P2 | GROSS: fitting loses | **HIT** (mean Δ −0.0006, p = 0.0008) |
| P3 | fitting wins on 0 or 1 of 5 | **MISS** — ahead on 3/5, significant on 2/5 (1/5 after controls) |
| P4 | CADENCE is the most likely dial to win | **MISS as scored** (SLEEVE's Δ is larger) — but CADENCE is the only dial that survives the geometry and random controls, so the substance of P4 held and the scoring rule was the wrong one |
| P5 | RANDOM lands between CONST and the selectors | RANDOM +0.0045 vs SEL-SHARPE +0.0461 vs CONST 0 — **HIT in aggregate**, but RANDOM *beats* SEL-SHARPE on GROSS and N |
| P6 | ORACLE beats everything | **HIT** (+0.0799 mean over dials) |
| P7 | no 4b KEEP | **MISS** — 250 rows pass, 36 on tradable panels, 1 walk-forward-supported |

4 of 7 hit. The two most informative misses are P3 (the general claim is weaker than ideas
110/151/132/166 suggested) and P7 (a methodology run turned up a candidate).

## Caveats, carried not buried

- **Survivorship**: B136, U56 and the small panel are current-constituent lists (idea 54). All
  arms and dials inherit it equally so the *paired* comparison is unaffected; the *level* of every
  number is not.
- **Idea 144**: a re-grossed / re-cadenced book is the same book. No verdict flip on a ladder is a
  new signal.
- **SLEEVE's ladder is truncated at 0.30 by choice.** The finding "SEL == ORACLE at the endpoint"
  is *about* that truncation. A wider grid would move the endpoint, not create skill.
- On k = 20 sub-panels the N ladder saturates at n ≥ 20 (every eligible name is held), so those
  points collapse onto ew-all. Reported, not hidden.
- The SLEEVE dial gives a sub-panel access to TLT/GLD/UUP, which its core cannot hold. That is
  ideas 101/134's construction, kept unchanged so that f = 0 is the same book.
- Idea 38 (calendar-day price index) and idea 126 (t+1 execution only) carry over.
- **CADENCE's win is one dial on one corpus.** Idea 107 (open) owns the cadence question and
  should decide it; this run hands it a 53-book paired result, not a rules change.

## What this means for PROTOCOL

The honest generalisation of ideas 110/151/132/166 is narrower than "fitting never pays":

> On dials whose ladder is a **scale lever** (GROSS) or is **flat** (BAND), an IS-fitted argmax is
> chasing noise and loses to the constant. On dials whose ladder is **monotone and truncated**
> (SLEEVE), an argmax is not a choice and the apparent win belongs to the grid, not the selector.
> Fitting pays only on a dial with an **interior optimum driven by a mechanism that transfers**
> — of the five, only cadence (turnover cost) qualifies, and even there it buys Sharpe by
> surrendering the CAGR that 4b grades on.

Three follow-up ideas are queued (173–175).

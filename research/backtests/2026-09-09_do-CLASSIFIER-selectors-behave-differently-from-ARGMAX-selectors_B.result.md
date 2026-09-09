# Idea 278 — do CLASSIFIER selectors behave differently from ARGMAX selectors?

**Lane B, 2026-09-09. Verdict: KILL / ANSWERED — no, not on any published cut, and out of
corpus the sign runs the other way.**

## The question and the declared map

Idea 271's CSEL (pick the narrowest arm whose *fitted reversal probability* clears a
threshold) beat do-nothing OOS while losing on the full sample — the opposite shape to the
argmax choosers in idea 229's pool. The queue asked whether the *mechanism* separates the two.

Fixed before any number was read:

| record class | mechanism | why |
|---|---|---|
| IS-SHARPE, IS-CAGR, SHRUNK-FIT | **ARGMAX** | the pick maximises an IS-estimated performance metric (a shrunk estimate is still argmaxed) |
| GATED, ABSTAIN | **CLASSIFIER** | the pick is set by a threshold on a fitted statistic that is not the objective, and the selector may abstain onto the control |
| RANDOM, OTHER, ORACLE | HELD OUT | a null, an incumbent, and a non-rule |

Idea 229's `census()` is imported and re-run, not re-derived. It now admits **110 instances
over 75 files / 5,479 paired cells** (STRICT) against the parent's published 104/69/5,302 —
the corpus grew from 305 to 369 committed `*.walkforward.csv` files in four days; the parent's
rows are inside these. Coverage is still only 20.3% (STRICT) / 36.3% (BROAD), so every count
here remains a lower bound.

## A — the record: the two mechanisms are not separable at any of the 12 grid points

Tuned parameter 1 = vocabulary (STRICT/BROAD); the activity subset and the bootstrap block are
reported in full, not chosen.

| vocab | subset | ARGMAX cell mean | CLASSIFIER cell mean | DIFF (instance block) | 95% CI | separable |
|---|---|---|---|---|---|---|
| STRICT | ALL | −0.00381 (4,426 cells / 85 inst) | +0.00240 (1,039 / 42) | **−0.00709** | [−0.04676, +0.02944] | no |
| STRICT | ACTIVE | −0.00554 (3,042) | +0.00294 (849) | −0.00974 | [−0.05974, +0.03424] | no |
| BROAD | ALL | +0.14912 (16,724 / 229) | +0.16019 (2,381 / 78) | −0.01796 | [−0.16337, +0.14060] | no |
| BROAD | ACTIVE | +0.16483 | +0.17512 | −0.01771 | [−0.16924, +0.13788] | no |

0 of 12 points separable. The cell block is the only one that comes close (STRICT/ALL
−0.00615, P(<0) 96.0%), and the cell block ignores the clustering the parent already showed
dominates this corpus (46.8% of variance between instances), so it is the wrong block to read.

**The inactivity confound runs the opposite way to the one anticipated.** A classifier can
abstain, so its margins were expected to be shrunk toward zero by inactivity. In fact ARGMAX
carries **31.3%** exactly-zero margins against CLASSIFIER's **18.3%** (STRICT): the argmax
choosers are the ones that most often land back on the control arm. Restricting to active
cells therefore *widens* the gap slightly (−0.00709 → −0.00974) instead of closing it, and it
still does not separate.

## B — out of corpus, live prices, rule 8: the lean reverses

A real fitted-probability classifier in CSEL's shape was built on idea 229's 36-cell live
corpus (3 panels × 2 cost rungs × 6 pre-registered dials). Logistic fit on an **inner split of
the IS window only** — features from 2009-01-01..2012-12-31, labels from
2013-01-01..2016-12-31, `logit(p) = −0.9540 + 3.4582·Δ_fit_Sharpe + 3.9986·(step/ladder_len)`,
in-fit accuracy 0.626 against a 0.530 base rate. Decision features recomputed on the full IS
window; 2017-2026 read once.

Tuned parameter 2 = the threshold p\*, all 7 rungs reported:

| p\* | picks | abstains | LABEL margin | **OOS margin** | beats S0 | vs ARGMAX |
|---|---|---|---|---|---|---|
| 0.50 | 35 | 1 | +0.11890 | +0.04632 | 18/36 | −0.01940 |
| 0.55 | 34 | 2 | +0.11852 | +0.04410 | 17/36 | −0.02163 |
| 0.60 | 34 | 2 | +0.11852 | +0.04410 | 17/36 | −0.02163 |
| **0.65** | 32 | 4 | **+0.13019** | +0.04160 | 15/36 | −0.02412 |
| 0.70 | 20 | 16 | +0.12952 | +0.03938 | 11/36 | −0.02635 |
| 0.80 | 16 | 20 | +0.11800 | +0.04093 | 10/36 | −0.02480 |
| 0.90 | 4 | 32 | +0.05881 | +0.03900 | 4/36 | −0.02672 |

p\* = 0.65 is the pre-registered rung (best LABEL-window margin, chosen inside IS). **Every one
of the seven rungs is below ARGMAX out of sample**, monotone in p\* over 0.65–0.90. Paired over
the 36 cells, CLASSIFIER − ARGMAX = **−0.02412, 95% CI [−0.05286, +0.00268], P(<0) 96.0%** —
the same "leans but does not separate" as Part A, with the sign flipped.

## Rule 8 walk-forward — the pooled books (both KEEP paths)

| book | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR / Sharpe / MaxDD | 4a-v2 | 4b |
|---|---|---|---|---|---|---|---|
| CLASSIFIER p\*=0.65 | 7.99% | 0.888 | −18.46% | 1.004 / 0.796 | 8.20% / 0.867 / −18.46% | False | False |
| ARGMAX (idea 229 S1) | 8.05% | 0.910 | −17.31% | 1.041 / 0.803 | 8.11% / 0.877 / −17.31% | False | False |
| S0 do nothing | 6.17% | 0.796 | −15.32% | 0.927 / 0.691 | 6.18% / 0.762 / −15.32% | False | False |
| ORACLE (not a rule) | 7.35% | 0.893 | −15.56% | 0.977 / 0.827 | 7.77% / 0.899 / −15.56% | False | False |
| SPY | 14.34% | 0.882 | −33.72% | 0.968 / 0.831 | 15.42% / 0.881 / −33.72% | — | False |
| RULES v2 (live) @10bps | 6.69% | 1.031 | −10.90% | 1.089 / 0.983 | 7.12% / 1.061 / −10.90% | — | False |

**4a-v2 0 of 13 books, 4b 0 of 13.** Both selector books fail 4b on H2, OOS and the CAGR floor
and neither beats RULES v2's Sharpe in either half; the classifier buys +1.14 pp of drawdown
over ARGMAX for −0.0100 of pooled OOS Sharpe. No KEEP on either path.

## Verdict

**KILL / ANSWERED.** The mechanism does not separate OOS expectancy: 0 of 12 record grid points
and 0 of 7 live threshold rungs separable. Where the two do lean, they lean in *opposite*
directions — the record's classifiers sit ~+0.006 to +0.011 above its argmaxes, and a real
fitted-probability classifier built to CSEL's recipe sits −0.024 *below* the argmax on fresh
out-of-corpus prices. Idea 271's CSEL result is therefore an instance, not a class property,
and the ARGMAX/CLASSIFIER distinction should not be used to pre-rank selectors.

**Survivorship:** the broad and small panels are current constituents, inherited whole from the
parent corpus. Only within-panel differences between selectors are read here, which is the
comparison the bias leaves usable; the absolute CAGRs above are upper bounds.

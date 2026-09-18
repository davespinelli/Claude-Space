# Idea 1245 (lane C, 2026-09-18) — is N_eff^PR the statistic the record should publish beside every walk?

**ANSWER: NO, NOT THE ONE 1239 MEASURED.** Pre-declared outcome **(B)** fires. Verdict **KILL (capital)** —
no new book, no RULES change, no PROTOCOL edit. 10 of 10 gates, 19s, offline, deterministic.

## The test that settles it
Three K=6 control candidate sets per panel with KNOWN degrees of freedom: **CTRL_CLONE** (6 re-leverings of
the anchor, true dof 1), **CTRL_DISJOINT** (the same rule on 6 disjoint name pools — genuinely different
books that still share the market factor; G8 verifies 0 names shared by any two), **CTRL_IID** (6 independent
gaussian series, true dof 6). Resolution `R = (X(DISJOINT) - X(CLONE)) / (X(IID) - X(CLONE))`.

| estimator | U56 | B136 | SMALL663 | mean | R >= 0.50 |
|---|---|---|---|---|---|
| **E_PR_RAW (1239's)** | 0.164 | 0.148 | 0.286 | **0.199** | **0 of 3** |
| E_PR_XS (cross-demeaned) | 0.969 | 0.985 | 0.997 | 0.983 | 3 of 3 |
| E_PR_RESID (SPY-residual) | 0.772 | 0.675 | 0.669 | 0.705 | 3 of 3 |
| E_ENT_RAW | 0.348 | 0.324 | 0.518 | 0.397 | 1 of 3 |
| E_ENT_XS | 0.984 | 0.992 | 0.999 | 0.992 | 3 of 3 |
| E_SL_BAR (the record's bar reading) | 0.600 | 1.000 | 0.800 | 0.800 | 3 of 3 |

Six books that **cannot hold each other's names** read **1.74 / 1.82 / 2.43** under E_PR_RAW where six
re-leverings of ONE book read 1.000 and six independent series read 5.99. **1239's "~1.1 degrees of freedom"
is very largely a reading of equity beta, not of candidate-set diversity.** The bar-based reading the queue
proposed to replace is the more resolving of the two.

## What the record's own headline number becomes
On the committed 19-book UNION set: E_PR_RAW 1.103 / 1.124 / 1.175, against **E_PR_XS 3.364 / 3.349 / 3.948**,
E_PR_RESID 1.273 / 1.356 / 1.384 and E_SL_BAR 8 / 4 / 7. The GROSS ladder reads 1.000 under every estimator
(1189's identity replays at 5.86e-05, G4), so the degeneracy finding itself survives — only its magnitude on
the NON-GROSS ladders was beta.

## The clause, priced
Clause: print N_eff beside the stated N; re-word when stated N >= 2x N_eff. Census 34,630 committed units;
CS_STRICT 2,105 claims, 402 resolvable to a rebuildable ladder. **The clause re-words 0.9950 of them under
E_PR_RAW, 0.9773 under E_PR_XS, 0.9552 under E_SL_BAR** — under EVERY estimator it re-words essentially every
headline, because the record's stated N counts CELLS (panel x dial x dial, median 50) and its rebuildable
candidate sets hold at most 19 books. So the re-word COUNT is not where the estimators differ; the printed
NUMBER is: across the 15 axis subsets E_PR_RAW spans 1.000-1.209 (sd 0.066) against E_PR_XS 1.240-3.937
(sd 0.709) and E_SL_BAR 1.000-7.000 (sd 1.843). **A statistic with sd 0.066 across every walk the record has
ever done cannot be the one printed beside them.**

## Capital, rule 8, OOS read once
4a **0 of 66** books and **0 of 363** rule-8 rows. 4b full+OOS 15 books / 26 rule-8 rows, collapsing to the U56
anchor (15.78% / 1.1522 / -19.13%, OOS 17.28% / 1.1832), its gross re-leverings, N=15, H=21 and B136 gross
rungs — **prior art, not a candidate**. Chooser arms (IS argmax on warm-up..2016-12-31, 2017-2026 read once,
45 (panel, subset) cells): DO_NOTHING **0.8869**, RAW 0.8526, DEDUP:E_PR_RAW:MIN 0.8207, DEDUP:E_PR_XS:MIN
0.8173, DEDUP:E_PR_RESID:MIN 0.8523, DEDUP:E_SL_BAR:MIN 0.8830. **No arm beats doing nothing.** G10 proves the
structural half: a de-dup that keeps the best-IS member of each cluster **cannot move an IS-argmax chooser**
(0 of 135 picks moved at every estimator) — the whole cost of a de-dup clause is its representative rule, not
its N_eff.

## The one thing worth keeping
N_eff does NOT predict the selection penalty (rank corr with OOS(pick) - OOS(do-nothing): -0.105 E_PR_RAW,
-0.261 E_PR_XS, -0.373 E_ENT_XS — negative, i.e. more measured diversity reads WORSE). It carries weak
information about IS->OOS **decay**: +0.316 (E_PR_XS) / +0.353 (E_ENT_XS) / +0.300 (E_SL_BAR) against the
stated candidate count K's **+0.152**. Roughly twice K's rank information, on 45 non-independent cells — a
lead, not a result.

## Survivorship (rule 9)
U56 and B136 are current-constituent lists; SMALL663 is a current sub-$2B screen less 51 names with
max_1d_move >= 1.0. Every LEVEL is optimistic. The headline is a RATIO of an estimator against its own
controls on the same tape, which a common level bias largely cancels out of; the 4a/4b columns and the
rule-8 levels carry the full bias.

## Reflexivity (1230)
This memo and this run's console become census units for the next run, so the 34,630 denominator is
tree-dated: it is a claim about the tree that existed on 2026-09-18 at this commit.

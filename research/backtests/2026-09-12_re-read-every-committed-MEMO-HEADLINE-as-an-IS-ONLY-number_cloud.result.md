# Idea 836 — re-read every committed MEMO HEADLINE as an IS-ONLY number (cloud lane, 2026-09-12)

**ANSWERED: every lead number in the record changes rank, and the MaxDD headline is not a
prediction at all — it is an identity. KILL for the "published headline = validated number"
reading. No KEEP claimed, no book promoted, no memo written.**

Script: `2026-09-12_re-read-every-committed-MEMO-HEADLINE-as-an-IS-ONLY-number_cloud.py`
(`.txt` console log, `.books.csv`, `.grid.csv`, `.ranks.csv`, `.census.csv`, `.wf.csv`).
Two tuned parameters: **P1 memo set** (MEMO8 / MEMO12 / MEMO14), **P2 split date**
(2013-12-31 … 2018-12-31, six rungs). Cost {0, 10, 25} bps and the lead reading
{CAGR, Sharpe, MaxDD} are **reported at all 324 grid points**, not selected.

## Gates (printed before any new number)

| gate | result |
|---|---|
| G1+G2 books reproduce their own committed triples | **12 of 12 PASS** (K2, V1 publish no triple, marked so); LIVE = 8.63% / 1.2018 / −12.05% vs RULES.md v2's 8.63% / 1.202 / −12.05% |
| G3 vectorised window metrics vs `engine.metrics` | max \|diff\| **2.220e-16** vs bar 1e-10 — PASS |
| G4 IS/POST split exhaustive + disjoint, 14 books × 6 splits | PASS |
| G5 MaxDD-identity count at the 2016 split | **11 of 12**, reproducing idea 833's committed 11 of 12 — PASS |

## The headline cell (MEMO12, split 2016-12-31, 10 bps)

`post_share = 0.5483` — **55% of every published FULL-sample headline is the 2017+ window
itself**, the window the memo then cites as its validation. At the 2013 split it is 0.7184.

| lead reading | ρ(FULL, IS-only) | perm95 null band | books changing rank | max displacement | top-1 FULL → IS-only → POST |
|---|---|---|---|---|---|
| **CAGR** (the lead number in every memo) | **+0.7832** | 0.5804 | **9 of 12** | 5 places (K2) | **R3 → R4 → K8** |
| Sharpe | **+0.5175** — *inside the null band* | 0.5804 | **12 of 12** | 8 places (R4) | **R3 → R4 → K8** |
| MaxDD | **−0.0839** — noise | 0.5804 | 11 of 12 | 9 places (K3, K8, R4) | K7 → K7 → K7 |

The published **Sharpe** ordering of the twelve books is **not distinguishable from a
relabelling** of its own in-sample half's ordering (+0.5175 against a 20,000-permutation
two-sided 95% band of 0.5804 at n=12).

## The MaxDD headline is an identity, not a number about the book

ρ(FULL MaxDD, POST MaxDD) = **+1.0000 exactly, at every one of the six splits**, on MEMO8 and
MEMO12 (+0.9956 on MEMO14). Eleven of twelve books' worst drawdown happens after 2016, so the
memo's third headline number *is* its out-of-sample number, restated. Against the IS-only
window the same correlation is **−0.0839**.

## Contamination: the FULL headline "predicts" the future because it contains it

ρ(FULL, POST) − ρ(IS-only, POST), the lead number, at the six splits:

| split | ρ(FULL,POST) | ρ(IS,POST) | contamination |
|---|---|---|---|
| 2013-12-31 | +0.9930 | +0.6923 | +0.3007 |
| 2014-12-31 | +0.9860 | +0.6503 | +0.3357 |
| 2015-12-31 | +0.9860 | +0.7622 | +0.2238 |
| 2016-12-31 | +0.9161 | +0.5524 | +0.3636 |
| 2017-12-31 | +0.9091 | +0.6993 | +0.2098 |
| 2018-12-31 | +0.8392 | +0.6993 | +0.1399 |

**6 of 6 splits positive**, median +0.2622, and the contamination *shrinks monotonically as the
POST window shrinks* — the signature of in-window arithmetic, not of predictive content. On the
Sharpe reading it is far larger (+0.6923 … +0.8951, ρ(IS,POST) **negative** at four of six
splits, −0.2797 at the 2016 split).

## Rule 8 — chosen on the first half (IS ≤ 2016-12-31), 2017+ read once

| book | IS CAGR / Sharpe / MaxDD | OOS CAGR / Sharpe / MaxDD | 4a | 4b |
|---|---|---|---|---|
| **R4** (IS-only pick, best IS Sharpe 1.2538) | 15.56% / 1.2538 / −10.15% | **14.52% / 1.0400 / −19.43%** | FAIL | PASS |
| **R3** (the *published* headline's pick) | 14.62% / 1.2449 / −10.63% | 16.00% / 1.2154 / −19.98% | FAIL | PASS |
| **K8** (OOS-best) | 11.92% / 1.0248 / −14.79% | **16.04% / 1.3937 / −12.72%** | FAIL | PASS |
| LIVE (RULES v2 baseline) | 7.61% / 1.1043 / −7.89% | 9.47% / 1.2782 / −12.05% | — | — |
| SPY | 14.96% / 0.8986 / −22.06% | 15.33% / 0.8767 / −33.72% | — | — |

**4a: 0 of 12 PASS on the OOS window. 4b: 11 of 12 PASS** (only K7 fails, on the CAGR floor) —
the same count as the fixed window, and every book's OOS CAGR is **below SPY's 15.33% except K8
(16.04%) and R3 (16.00%)**. The IS-only chooser picks **R4, which has the worst OOS Sharpe of
the twelve (1.0400)**; it gives up 0.354 OOS Sharpe against K8 — the record's n-th "selection
loses to doing nothing".

## Pre-registered hypotheses: 6 of 8 PASS

| | verdict | number |
|---|---|---|
| H_RANK | PASS | 3 of 12 move ≥3 places on the lead number (9 move at all, max 5 at K2) |
| H_TOP1 | PASS | top-1 FULL R3 → IS-only R4 (POST top-1 is K8, neither of them) |
| H_RHO | PASS | ρ(FULL CAGR, IS CAGR) = +0.7832 < 0.90 |
| H_CONTAM | PASS | 6 of 6 splits, median +0.2622 |
| H_MAXDD_ID | PASS | 11 of 12 MaxDD identities |
| H_STABLE | PASS | no lead order identical across all splits (min pairwise ρ: CAGR +0.7692, Sharpe +0.8322, MaxDD +0.5664 with 10 of 15 MaxDD pairs identical) |
| **H_WF** | **FAIL** | IS-only pick R4 ≠ OOS-best K8 |
| **H_CENSUS** | **FAIL** | only 26 of 132 memo files state no IS-only reading (0.1970) vs bar 0.50 |

**H_CENSUS's failure is the useful half of the census.** Of 132 committed memo files, 46 quote
a full-sample headline, 106 mention an IS-only or rule-8 reading somewhere, and only **7** quote
a full-sample headline with no IS-only reading anywhere. The record is not silent about rule 8 —
it runs it and writes it down. The defect is narrower and worse: the number the memo *leads*
with is the contaminated one, and the rule-8 number is in section 4 where no leaderboard row,
no queue entry and no cross-idea citation ever reads it.

## What this run does NOT establish

It does not say the books are bad (11 of 12 pass 4b OOS at 10 bps). It says the *ordering
device* the record uses to talk about them — the published headline — carries between +0.14 and
+0.36 of borrowed correlation with its own out-of-sample window on the lead reading, and is
inside the n=12 noise band on the Sharpe reading. n is 8–14 throughout; a ρ of 0.5 is not
separable from noise at this corpus size (idea 837 is the standing follow-up for n ≥ 30).
Survivorship: `universe.json` and `universe_broad.json` are current-constituent lists, so every
LEVEL above is optimistic; the contrast is within-corpus, which survivorship does not hit
uniformly, so the ordering statistics carry it too.

## Recommendation (NOT applied — PROTOCOL.md untouched, Sunday review decides)

Any memo headline that quotes a FULL-sample triple should quote the **IS-only triple beside it**,
and any cross-idea citation of "the published Sharpe/MaxDD" should name which window it is on.
Filed as queue items 840 and 841 rather than edited into PROTOCOL.md by this lane.

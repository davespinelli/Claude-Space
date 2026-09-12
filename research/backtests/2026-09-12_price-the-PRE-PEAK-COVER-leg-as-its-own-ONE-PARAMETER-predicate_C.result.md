# Idea 820 — price the PRE-PEAK COVER leg as its own ONE-PARAMETER predicate (lane C, 2026-09-12)

**ANSWERED = THE PRE-PEAK TERM IS THE STRICTLY WORSE OF THE TWO CANDIDATE MISSING TERMS, AND THE
TWO ARE EXACTLY COMPLEMENTARY — WHICH IS WHY NEITHER IS A MISSING TERM.  KILL for capital.**

## The head-to-head the idea asks for (qualifying corpus: 14 long-decline cells, 897 scored arms, 111 ties, 114 DECLINE-predicate arms)

| term | #pred | necessity P(pred\|tie) | true ties LOST | sufficiency P(tie\|pred) | FP left |
|---|---|---|---|---|---|
| DECLINE (813) | 114 | 1.0000 | 0 | 0.9737 | 3 |
| +PRE m=5 / 10 / 21 / 42 | 114 | 1.0000 | 0 | 0.9737 | 3 |
| +PRE m=63 | 102 | 0.8919 | 12 | 0.9706 | 3 |
| +PRE m=126 | 99 | 0.8649 | 15 | 0.9697 | 3 |
| +PRE m=252 | 84 | 0.7297 | 30 | 0.9643 | 3 |
| **+PRE m=ALL (the queue's literal leg)** | **42** | **0.3784** | **69** | **1.0000** | **0** |
| +POST k=5 (817's headline) | 99 | 0.8919 | 12 | 1.0000 | 0 |
| +POST k=ALL | 60 | 0.5405 | 51 | 1.0000 | 0 |

All 8 m-rungs × 2 family sets printed, on 4 corpora, at all 5 cover bars (`.mladder.csv`,
`.predicates.csv`).  Headline m = ALL is **rule-chosen, not picked**: the smallest rung with
sufficiency 1.0000 and #pred ≥ 30, a rule stated before the grid was read — and it is the *only*
rung that reaches sufficiency 1.0000 at all, so there is no plateau (H_PLATEAU FAIL).

**THE PRICE:** to buy the same sufficiency 817's POST term bought for 12 discarded true ties,
the PRE term must discard **69** — necessity 1.0000 → 0.3784 against POST's 0.8919.
H_CHEAPER FAILS, and it fails by 5.75×.  Every rung that costs nothing (m ≤ 42) buys nothing:
#pred, necessity, sufficiency and FP count are all identical to the bare DECLINE predicate.
The term is a step function with one step, and the step is the whole pre-peak history.

## Why: the two terms are EXACTLY complementary, 3 and 3, and neither is a missing term

Of 813's 15 false positives over all windows, PRE removes 12 and POST removes 12 — but **not the
same 12**.  PRE reaches **3 of the 3** no POST rung can reach (U56 POST20 SPYDD 0.20 ×3 gross:
arm trough 2023-03-10, control trough 2025-04-08, cover_RECOVERY exactly 0, cover_PRE_ALL 0.0292 —
817's named unreachable rows).  POST reaches **3 of the 3** no PRE rung can reach (U56 E2015
CORR 0.40 ×3 gross: cover_PRE_ALL exactly 0.0000, the arm de-grossed *after* the control's peak).
Neither term reaches 0 of them.  H_COMPL PASSES — and that is the finding: each conjunct removes
the false positives that live on its own side of the peak and is blind to the other side, which is
the signature of a filter fitted to counterexamples, not of a term the predicate was missing.

The stacked form is reported as a **diagnostic only** (the queue asks that the two be priced
against each other, not stacked): DECLINE+PRE_ALL+POST_5 reaches sufficiency 1.0000 with 0 FP —
at necessity **0.3243**, and DECLINE+PRE_ALL+POST_ALL collapses to #pred 18, which is *exactly*
the 18 qualifying arms with zero cover over the whole window, i.e. the arms that ARE CONTROL-U.
No stacked row is promoted anywhere.

The other reading of "single-conjunct alternative" — PRE_m **alone**, without DECLINE — is printed
too and is worse still: necessary (1.0000 at m ≤ 42) but sufficiency **0.1382–0.1774** at every
rung, 561 false positives at m=5.  There is no reading of the pre-peak leg that is two-directional.

## Corroboration of 817's correction to 813, from the episode dates this run prints

The 3 PRE-only-removable rows have control peak **2025-02-19** and arm trough **2023-03-10**: the
de-gross sits two years before the episode began, so no post-trough clause can reach it — exactly
817's stated mechanism, now measured from the other side.

## Gates and reproduction — 4 of 4 mechanical, 2 of 2 corpus, 1 of 1 cross-run

G1 0.000e+00, G2 1.388e-17, G3 0.000e+00 (all panels), G4 ≤ 1.778e-04.
G5a the 596/811 sub-corpus: 141 arms / 45 ties / 1.0000 / 1.0000, ties by family
SPYTR 0 / BREADTH 12 / VOL 18 / SPYDD 15 — all PASS.
G5b 813's qualifying corpus: 14 cells / 897 arms / 111 ties / 114 predicate arms / 0.9737 / 3 FP,
and 15 FP over all windows CORR 9 / VOL 3 / SPYDD 3 — all PASS.
G7 (new): **all 1,890 rows** join 817's committed cell file key-for-key and `cover_PRE_ALL` equals
its `cover_PREPEAK` to **1.110e-16**, with `cover_DECLINE`, `tie_U` and all nine `cover_POST_k`
columns reproducing to ≤ 1.110e-16.  This run is 817's corpus, not a new one.

Cover-bar ladder flat: the m ladder's rates are unchanged across eps ∈ {0, 1e-12, 1e-6, 1e-4, 1e-3}.
PRE_m ≡ PRE_m+COST, 0 disagreements at all 8 rungs over 1,404 scored cells.
Necessity is monotone non-increasing in m (H_MONO PASS), so the cover windows are built right.

## Pre-registered hypotheses: 7 of 11 pass

PASS — H_REPRO, H_SUFF1, H_POWER (#pred 42 ≥ 30), H_NONTRIV (42 > 18), H_NOSPYDD (1.0000 with the
confound dropped, #pred 39, necessity 0.4333), H_COMPL, H_MONO.
**FAIL — H_NEC1 (load-bearing): 0.3784, not 1.0000.  H_CHEAPER: 69 ties lost vs POST's 12.
H_PLATEAU: one qualifying rung, a knife edge.  H_ALLFP: 3 of 15 survive the headline rung.**

## PROTOCOL rule 8 (mandatory) and both KEEP paths — KILL for capital

(a) standing 2016/2017 split, FULL window, dial chosen on IS Sharpe alone, OOS read once:
median OOS CAGR/Sharpe/MaxDD **U56 9.08% / 1.271 / −9.98%**, **B136 7.51% / 1.100 / −10.94%**,
**SMALL 3.09% / 0.512 / −12.44%**, against **SPY OOS 15.33% / 0.877 / −33.72%** and RULES v2 OOS
9.47% / 1.278 / −12.05% (U56), 7.88% / 1.106 / −12.24% (B136), 3.75% / 0.560 / −13.89% (SMALL).
6 of 54 FULL picks pass 4b OOS, 2 of 54 pass 4a OOS.
(b) window-local half split on the six short windows, reported beside (a): over all 375 picks,
**20 pass 4b OOS and 11 pass 4a OOS**.

Fixed windows, all 1,404 scored arms: 4a 47, 4b 61; 4b AND 4b-OOS 28; and of those, **0 beat their
own CONTROL-M on any window except one PRE20 row** (B136 DISP 0.15 g=1.00, 10.95%/1.173/−10.46% vs
ctlM 9.56%/1.142/−9.12%) — a window that ends in 2019 and is wholly in-sample, the same single row
817 found.  The binding 4b leg on FULL is CAGR (113 of 246).

**No KEEP claimed on either path, no book proposed or promoted, no memo.**
RULES.md, PROTOCOL.md, research/scan.py, products/bot/bot.py and research/baseline.py untouched.

## Survivorship and scope

All three panels are current-constituent lists, SMALL worst (52 tickers with max_1d_move ≥ 1.0
dropped, 663 left).  Every LEVEL is optimistic; the predicate rates are within-panel agreement
rates, which survivorship moves far less.  Several windows are 3–5 years inside a bull leg, so no
Sharpe or CAGR read off them is a capital claim.

## What this settles for the record

596's decline-cover predicate stays **necessary-only**.  817 showed one candidate conjunct buys
sufficiency by spending necessity; 820 shows the other candidate does the same thing *worse*, and
that the two are complementary rather than nested — so the record should stop treating either as a
missing term.  Idea 822 (does ANY two-directional MaxDD-tie predicate exist on this corpus) is now
the only open form of the question, and this run supplies its two single-leg baselines:
PRE_ALL (42 / 0.3784 / 1.0000) and POST_5 (99 / 0.8919 / 1.0000).

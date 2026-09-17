# Idea 1210 (lane C, 2026-09-17) — how many committed CHOOSER COMPARISONS rest on FEWER THAN TEN PICKS?

**VERDICT: KILL (capital) / ANSWERED — 44 of 165 (0.2667) rest on fewer than ten picks, and at
the tape's own per-pick SD only 80 of 165 (0.4848) clear a 2-SE bar — 29 of 165 (0.1758) if the
picks are single-period reads. The median committed comparison sits EXACTLY on its own
resolution boundary (needs 22 picks, supplies 21); the tail does not (90th percentile needs
3,969 picks and supplies 213).**

Script: `2026-09-17_how-many-committed-CHOOSER-COMPARISONS-rest-on-FEWER-THAN-TEN-PICKS_C.py`
(21 s, offline, deterministic). Gates 7 of 7 PASS.

## The two dials, all 9 cells published

| claim set | bar | n | resolved | share | K<10 | resolved & K<10 | median K | median \|X\| |
|---|---|---|---|---|---|---|---|---|
| C_STRICT | B_1SE | 165 | 106 | 0.6424 | 44 | 17 | 21 | 0.0500 |
| **C_STRICT** | **B_2SE** | **165** | **80** | **0.4848** | **44** | **11** | **21** | **0.0500** |
| C_STRICT | B_NULL90 | 165 | 76 | 0.4606 | 44 | 11 | 21 | 0.0500 |
| C_ADJ | B_1SE | 107 | 72 | 0.6729 | 24 | 10 | 24 | 0.0415 |
| C_ADJ | B_2SE | 107 | 51 | 0.4766 | 24 | 7 | 24 | 0.0415 |
| C_ADJ | B_NULL90 | 107 | 48 | 0.4486 | 24 | 7 | 24 | 0.0415 |
| C_BROAD | B_1SE | 196 | 115 | 0.5867 | 61 | 22 | 18 | 0.0430 |
| C_BROAD | B_2SE | 196 | 86 | 0.4388 | 61 | 13 | 18 | 0.0430 |
| C_BROAD | B_NULL90 | 196 | 82 | 0.4184 | 61 | 13 | 18 | 0.0430 |

Headline cell (`C_STRICT` × `B_2SE`) was declared before any number was read.

## What was measured, and what was only harvested

`sigma_d` is the only thing measured on the tape: the per-pick SD of the OOS-Sharpe difference
between two of the record's three honest choosers, over 1101's rung books.

* `sigma_CELL = 0.1176` over 216 paired picks (3 panels × 2 anchors × 4 ladders × 3 IS windows
  × 3 chooser pairs), each pick read on the FULL OOS window 2017–2026. **Adjudication basis**,
  declared in advance, because it is the unit the record's own "mean OOS Sharpe over K picks"
  claims average over.
* `sigma_FOLD = 0.3707` over 2,160 paired picks read on ONE OOS calendar year each — 1206's
  order of magnitude. Published as the robustness column, never selected on.
* The two choosers pick the SAME rung at 0.3380 of CELL picks, which shrinks the SD and makes
  the census MORE generous, not less.
* Clustered / iid SE ratio, median over pairs: **1.39**. Every "resolved" count here is
  therefore an UPPER BOUND — the record's picks share panels, anchors and one tape.

## The census

The harvest classifies every number sitting inside ±140 characters of an "OOS Sharpe" cue:
**GAP 312 / LEVEL 1,328 / LABEL 110** of 1,750 QUANT hits. Only the GAP class — the numbers the
record writes AS differences — is adjudicated (`H_MARKED`); the naive reading that adjudicates
all three (`H_NAIVE`: 915 C_STRICT claims, 0.5322 resolved at `sigma_CELL`, 0.2918 at
`sigma_FOLD`) is published beside it so the classification's effect is visible.

Hand audit of the GAP class, 20 rows drawn with `random_state=1210` from the C_STRICT frame:
**18 of 20 are genuine OOS-Sharpe difference statements**; the two misses were a `premium`
column and a MaxDD statistic. Read every count below as ~0.90 precise.

K distribution over the 196 adjudicable GAP claims (C_BROAD): K 1–2 **19**, 3–5 **21**, 6–9
**21**, 10–19 **43**, 20–49 **37**, 50–99 **18**, 100+ **37**. 6 committed gaps are written as
EXACTLY 0.000 (no count resolves a zero). 85.4% of C_STRICT QUANT hits carry a recoverable
count on their own line; the rest state none and are never imputed one.

The quadratic is the whole story: `K_req(X) = (2 sigma_d / X)^2`.

| quantile of adjudicated claims | picks NEEDED | picks SUPPLIED |
|---|---|---|
| 50% | 21 | 21 |
| 75% | 235 | 74 |
| 90% | 3,969 | 213 |
| 99% | 5,533,245 | 873 |

## PROTOCOL rule 8 (parameters chosen on 2009–2016 alone, 2017–2026 read once)

| who | n picks | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|
| CH_ISSHARPE | 24 | 11.61% | 0.7963 | −25.59% |
| CH_ISCAGR | 24 | 11.81% | 0.7866 | −26.21% |
| CH_ISDD | 24 | 9.56% | 0.8157 | −21.85% |
| RULES v2 (live) U56 / B136 / SMALL | — | 9.42% / 7.88% / 3.75% | 1.2714 / 1.1059 / 0.5600 | −12.05% / −12.24% / −13.89% |
| SPY | — | 15.15–15.33% | 0.8684–0.8767 | −33.72% |

All three choosers lose to the live book on OOS Sharpe and to SPY on OOS CAGR. The pairwise
comparisons between them — the exact object this census is about, made honestly — are **all
three UNRESOLVED**: +0.0097 (t +0.58, needs 594 picks), −0.0195 (t −0.79, needs 146), −0.0291
(t −0.93, needs 65), against the 24 picks each supplies. Per-cell sign agreement between the
full-window and the per-year reading of the same gap runs **0.5278 / 0.6528 / 0.6944** — near a
coin on the pair the record would call "closest".

## Both KEEP paths (rule 4) on the 144 distinct books this run built

4a **0 of 144**. 4b FULL 20, 4b OOS 24, **4b FULL and OOS 19 of 144** (U56 14/48, B136 5/48,
SMALL 0/48). These are 1101's rung books, not this idea's object — recorded, not promoted, no
memo. Nothing in a text census can pass a KEEP path on its own.

## Limits, stated

1. `sigma_d` is measured between the record's three honest choosers on 1101's four ladders. The
   committed claims compare a far more heterogeneous set of rules; a pair whose picks differ
   more often would carry a larger SD and resolve FEWER claims, not more.
2. The count recovery reads the count cue nearest the gap on the same line. Where a line quotes
   several counts, the nearest one may not be the claim's own — 14.6% of C_STRICT QUANT hits
   state no count at all and are excluded rather than imputed.
3. Independence across picks is assumed by the bar itself; the measured clustered/iid ratio of
   1.39 says the true bars are ~39% higher than the ones used here.
4. Rule 9 survivorship: U56, B136 and SMALL are current-constituent lists; every level is
   optimistic.

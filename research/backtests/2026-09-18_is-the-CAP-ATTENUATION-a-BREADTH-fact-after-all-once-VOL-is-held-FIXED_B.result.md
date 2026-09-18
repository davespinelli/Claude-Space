# Idea 1080 (lane B, 2026-09-18) — is the CAP ATTENUATION a BREADTH fact after all, once VOL is held FIXED?

**ANSWER: NO. KILL (capital) and KILL of the queue's own premise.** Breadth matching does not close
the 0.4063 cap shift; on the vol-matched ladder it *widens* the cap gap; and the premise that
breadth tracks rho across 1073's four cells holds only on the FULL-SAMPLE breadth measure, which no
panel can be built on. Gates **8 of 8 PASS**. Hypotheses 3 of 8.

Script: `research/backtests/2026-09-18_is-the-CAP-ATTENUATION-a-BREADTH-fact-after-all-once-VOL-is-held-FIXED_B.py`
836 panels, 3,344 book rows, 10 bps, weekly, next-day, GROSS 0.75, IS ..2016 / OOS 2017.. .

## The object, reproduced exactly
G5/G6 replay idea 1073's crossing arm on its own pools, seed and k set: rho BSTK-LO **+0.8759**,
BSTK-HI **+0.7649**, SMALL-LO **+0.3586**, SMALL-HI **+0.1769** and the four FULL-SAMPLE breadths
0.7376 / 0.6796 / 0.5943 / 0.4179 — all to **max|d| 0.00e+00**, and the shift
|rho(BSTK-HI) − rho(SMALL-LO)| reproduces at **0.4063**.

## 1. The premise is MEASURE-DEPENDENT, and it fails on the only measure a panel can be built on
A breadth used to *select* names must be IS-only. Per-name IS breadth (gate-pass rate on weekly
rebalance days, 2010..2016) gives cell means **BSTK-LO 0.7931 / BSTK-HI 0.6920 / SMALL-LO 0.6892 /
SMALL-HI 0.4621**. The two cells the 0.4063 shift is taken between are therefore **already matched**:
|d| = **0.0082** on realised panels, against **0.0853** on 1073's full-sample measure. There was
almost nothing at the decisive contrast for a breadth match to remove. (H_ALREADY FAIL.)

## 2. Matching binds, and the shift does not respond (headline block k=20)
| beta | shift | % of this block's UNMATCHED | % of committed 0.4063 | \|d breadth_IS\| | \|d vol\| |
|---|---|---|---|---|---|
| UNMATCHED | 0.1708 | 100.0% | 42.0% | 0.0082 | 0.0314 |
| 0.25 | 0.0928 | 54.3% | 22.8% | 0.0021 | 0.0180 |
| 0.20 | 0.2300 | 134.6% | 56.6% | 0.0024 | 0.0038 |
| 0.15 | 0.1614 | **94.5%** | 39.7% | 0.0106 | 0.0072 |

G7: the dial binds — SD of panel IS breadth falls 0.1287 → 0.0279. The shift bounces on both sides
of its unmatched value (non-monotone, H_MONO FAIL) and **94.5% survives** at the tightest tolerance
(H_SURVIVE FAIL). A dial that moves an object to 54%, then 135%, then 94% of its starting value is
not moving it at all; it is draw noise on 12 heavily-overlapping draws.

**Block honesty:** 1073's committed 0.4063 pools k ∈ {20,30,40}. On the k=20 block alone it is
**0.1708** — 42% of the committed figure. Part of the published 0.4063 is a k-pooling object, and
that is reported here, not netted into the breadth answer.

## 3. On the vol-matched LADDER, breadth matching moves the cap gap the WRONG way
rho(q=0.00) − rho(q=1.00) inside 1073's tau=0.20 vol window, k=20:
**UNMATCHED +0.2852 → beta 0.20 +0.3783 (133%) → beta 0.12 +0.7520 (264%)**. Holding breadth fixed
makes the cap axis *stronger*. (H_LADDER FAIL; the k=30 sub-block, reported not headlined, reads
+0.3964 → +0.3351, with beta 0.12 infeasible.)

## 4. Where breadth DOES bite — and why it still cannot be the cap axis
The mirror arm (cap fixed, breadth moved, each pool cut at its own median IS breadth):

| cell | breadth_IS | panel_vol | rho |
|---|---|---|---|
| BSTK-BLO | 0.6573 | 0.2901 | +0.7284 |
| BSTK-BHI | 0.8277 | 0.2247 | +0.6059 |
| SMALL-BLO | 0.4371 | 0.5124 | +0.0750 |
| SMALL-BHI | 0.7250 | 0.3168 | +0.4879 |

Within SMALL, moving breadth shifts rho **0.4129** — the same size as the 0.4063 cap shift. Within
BSTK it shifts it **0.1225**, and **in the opposite direction**. Breadth is a strong dial inside
small caps and a weak, oppositely-signed one inside large caps, so it is not a common axis that
could stand in for cap. H_BCROSS passes on its literal wording (max = 0.4129 ≥ 0.4063) and the pass
is reported as one-sided: it is carried entirely by the small pool.

## 5. H_SIGN is REFUTED on this block
1073's "strength dial, not sign dial" claim (rho > 0 everywhere) does not hold at k=20: SMALL-HI
UNMATCHED reads **−0.0740** (min over 29 published cells; max +0.8824). Not a large negative, and no
interval is published for it, so the claim made here is only that the SIGN is not shown to be
positive in every cell — not that it is negative.

## Rule 8 (required) and both KEEP paths
n/k chosen on 2009-2016 IS Sharpe only inside each (arm, cell, beta, k, draw) choice set, 2017- read
once. Mean OOS Sharpe / CAGR / MaxDD by selector, CROSS arm: RATIO-MAX **0.5383 / 6.20% / −23.27%**,
IS-SHARPE-MAX 0.4908 / 6.50% / −25.88%, RANDOM 0.4373 / 5.76% / −30.60%, RATIO-MIN 0.2965 / 4.52% /
−41.61%. On the SAME panels **SPY OOS Sharpe 0.8767 / CAGR 15.33% / MaxDD −33.72%** and **RULES v2
OOS Sharpe 0.6169 / CAGR 4.90% / MaxDD −14.27%**. The best selector beats SPY on 29.6% of choice
sets and RULES v2 on 23.7%. By beta on the CROSS arm the chooser's edge over the do-nothing anchor
is +0.0987 (UNMATCHED), +0.1077 (0.25), +0.1126 (0.20), +0.0849 (0.15) — no ordering in the dial.

**KEEP paths, every book row: 4a 0 of 3,344; 4b 153 of 3,344 (4.6%).** By arm: CROSS 86 of 1,488,
CROSSB 38 of 384, MATCH 10 of 1,088, REPRO 19 of 384. These are the record's committed CAND-n books
on random sub-panels of a survivor screen, so a 4b pass is a statement about the draw. **Nothing is
promoted. No memo, no RULES change.**

## Limits, stated before the verdict
1. At the tightest CROSS beta the decisive cells hold 32 names, so 12 k=20 draws overlap heavily;
   every rho is a firmer POINT than an INTERVAL and only ORDERING and SIGN are claimed (idea 1044).
2. Breadth and vol are not orthogonal on this tape (SMALL-LO breadth 0.6892 vs SMALL-HI 0.4621), so
   a breadth window moves the vol mix too — |d vol| is printed beside every shift.
3. The matched window is where the pools OVERLAP; it speaks for neither pool's typical name.
4. IS breadth is measured on 2010-2016, which holds one real drawdown (2011) and no 2020/2022.
5. SURVIVORSHIP (rule 9): a realised gate-pass rate is measured on names that survived to be
   screened today, so a high-breadth window is doubly a survivor window. Every level is an upper
   bound; the quoted results are within-grid differences on identical dates and are first-order
   immune.

## NOT claimed
That breadth is irrelevant (§4 shows it is the dominant dial *inside* the small pool). That 1073's
0.4063 is wrong (it reproduces to 0.00e+00). That any committed verdict flips. That the k=20 shift
of 0.1708 and the pooled 0.4063 are shown to differ — no interval is published for either.

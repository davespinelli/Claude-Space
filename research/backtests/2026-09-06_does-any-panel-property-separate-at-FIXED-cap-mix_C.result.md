# Idea 284 — does-any-panel-property-separate-at-FIXED-cap-mix (lane C, 2026-09-06)

**Verdict: ANSWERED. Split answer, and the pooled record has the SIGN WRONG.**
**`breadth` is KILLED as an independent property (ρ +0.02…+0.07, p 0.57–0.87 inside the stratum,
against +0.61…+0.74 pooled). `corr` and `disp` SURVIVE at fixed capitalisation — and their
within-stratum signs are the OPPOSITE of their pooled signs.** No KEEP: 4a **0/525**, 4b **23/525**
and not one of them is a pre-registered selector's pick. `corr` is a **PARK** with a memo.

Script: `research/backtests/2026-09-06_does-any-panel-property-separate-at-FIXED-cap-mix_C.py`
Console: `…_C.console.txt` · CSVs: `.panels` (105 panels) `.cells` (525 grid points) `.walkforward`

## Construction

k = 40 names per panel throughout, so panel WIDTH is never confounded with composition.
q = share drawn from SMALL439, the rest from BSTK100 (stock vs stock — idea 276's axis, unchanged).

| stratum | draws | purpose |
|---|---|---|
| **q = 0.500** (20 small + 20 large) | **60 seeded** | the verdict is read here; q is constant by construction |
| q = 0.000 / q = 1.000 | 20 each | anchors, for the pooled-vs-within contrast only |
| NAMED U56 B136 BSTK100 ETF36 SMALL439 | 5 | reproduction rows |

105 panels × 5 arms (EWall, CAND10, CAND20, RULES v1, RULES v2) = **525 cells, all reported**.
Tuned parameters: **q (3) and n (2)**. Seeds are replication, never selection. Common calendar
2010-01-04 → 2026-09-04 (4,194 days). SPY on it: 14.13% / 0.8616 / −33.72%, halves 0.891/0.858,
OOS 0.8820. 10 bps, weekly, next-day, gate = above-200d AND vol20 < 0.60, 75% gross.

**Reproduction gate.** U56/CAND20 12.7% published → **13.04% / 1.0821 / −18.30%, OOS 1.1458**
(idea 276 published 12.7% / 1.098 / −18.1%, OOS 1.168 — the known last-digit calendar gap).
Named-panel characteristics reproduce idea 271's ordering exactly: SMALL439 breadth 0.3048 vs
0.6442–0.6665 for every large-cap panel, dispersion 0.1507 vs 0.057–0.096, corr 0.1710 vs 0.31–0.38.

## Q1 — the answer. Spearman(IS characteristic, OOS Sharpe), 20,000-permutation p

| book | char | **ρ WITHIN q=0.5** (n=60) | p | ρ POOLED (n=100) | p | sign |
|---|---|---|---|---|---|---|
| CAND10 | **breadth** | **+0.0222** | 0.872 | +0.6090 | 0.0000 | — |
| | disp | +0.3932 | 0.0016 | −0.4559 | 0.0000 | **FLIP** |
| | corr | −0.3648 | 0.0046 | +0.4974 | 0.0000 | **FLIP** |
| | evol | +0.2310 | 0.077 | −0.5122 | 0.0000 | **FLIP** |
| CAND20 | **breadth** | **+0.0281** | 0.829 | +0.7148 | 0.0000 | — |
| | **disp** | **+0.5313** | 0.0000 | −0.5512 | 0.0000 | **FLIP** |
| | **corr** | **−0.4815** | 0.0003 | +0.5864 | 0.0000 | **FLIP** |
| | evol | +0.4241 | 0.0008 | −0.5895 | 0.0000 | **FLIP** |
| EWall | **breadth** | **+0.0742** | 0.574 | +0.7360 | 0.0000 | — |
| | disp | +0.4704 | 0.0002 | −0.5779 | 0.0000 | **FLIP** |
| | corr | −0.4708 | 0.0005 | +0.6062 | 0.0000 | **FLIP** |
| | evol | +0.3228 | 0.0120 | −0.6266 | 0.0000 | **FLIP** |

Two separate findings, and the second is the one the record does not currently know:

1. **breadth is exactly a capitalisation dummy.** Pooled it is the single strongest predictor in
   the table (+0.74 on EWall); hold q fixed and it is indistinguishable from noise in all three
   books. This is idea 276's collinearity finding upgraded from "noisier proxy" to **"zero
   independent content"**, measured on returns rather than on the statistic.
2. **Every other characteristic reverses sign under the control.** Small-cap panels have high
   dispersion, high eligible-set vol, low correlation AND bad OOS Sharpe, so pooling across strata
   makes dispersion and vol look bad and correlation look good. At fixed cap mix the ordering is
   the other way round: **more dispersion is better, less correlation is better**. This is a
   textbook Simpson reversal, and it means the record's cross-panel characteristic sentences are
   not merely confounded — where they state a direction, that direction is backwards.

**What survives a control for the other three** (rank-partial ρ, within-stratum):

| | breadth | disp | corr | evol |
|---|---|---|---|---|
| CAND10 | +0.103 | +0.264 | **−0.212** | −0.126 |
| CAND20 | +0.146 | +0.247 | **−0.298** | +0.031 |
| EWall | +0.196 | +0.261 | **−0.323** | −0.073 |

`evol` collapses to ≈0 — it is mediated by the other two. `corr` and `disp` both survive.

**Split-half replication (seeds 0–29 vs 30–59, nothing tuned):** corr **−0.55 / −0.22**,
**−0.58 / −0.42**, **−0.50 / −0.42** — negative in both halves in all three books. disp +0.51/+0.28,
+0.68/+0.38, +0.60/+0.37 — positive in both halves. **breadth flips sign between halves**
(−0.088/+0.150, −0.129/+0.196, −0.006/+0.212), which is what a zero looks like.

**Joint fit inside the stratum** (OOS Sharpe ~ 1 + four z-scored IS characteristics):
R² 0.188 / 0.308 / 0.308 (CAND10 / CAND20 / EWall). `corr` is the only individually significant
coefficient in all three (t −2.11 / −2.39 / −2.60); breadth t +0.67 / +0.85 / +1.37.

**Controls on the same 60 points.** Idea 271's winning predictor `EWall_IS_Sharpe` — the un-ranked
book's own in-sample Sharpe, which beat every characteristic *between* panels — is **not
significant within the stratum**: ρ +0.1490 (p 0.260) and +0.1803 (p 0.173). Nor is the book's own
IS Sharpe (+0.231 / +0.161) or `n_elig` (+0.034 / +0.028). Inside a fixed cap mix the ordering
information is in the characteristics, not in the level. Idea 271's headline is itself a
between-stratum statement.

**Monotone tercile ordering of `corr`** (mean OOS Sharpe, 20 panels per tercile):

| IS-corr tercile | CAND10 | CAND20 | EWall |
|---|---|---|---|
| low (0.207–0.263) | **0.7634** | **0.8057** | **0.8003** |
| mid | 0.7124 | 0.7268 | 0.7136 |
| high (0.286–0.339) | 0.6216 | 0.6440 | 0.6525 |

## Q2 — Rule 8 walk-forward inside q=0.5 (selectors and directions fixed before any OOS read)

IS 2009-01-01→2016-12-31 chooses one panel; OOS 2017-01-01→2026-09-04 read once.
Anchor = drawing a panel at random = mean OOS Sharpe over all 60 (CAND10 **0.6991**, seed sd 0.1709,
best 1.1859; CAND20 **0.7255**, sd 0.1451, best 1.0499). SPY OOS 0.8820, RULES v2 OOS 0.8654,
RULES v1 OOS 0.6303.

| rule | pre-registered as | pick | OOS Sh (n=10) | vs anchor | OOS Sh (n=20) | vs anchor |
|---|---|---|---|---|---|---|
| **S_CORR** | **LOWEST IS mean pairwise corr** | q0.5~s34 | **1.0704** | **+0.3713** | **1.0130** | **+0.2875** |
| S_BREADTH | highest IS breadth | q0.5~s26 | 0.7798 | +0.0806 | 0.8497 | +0.1242 |
| S_ISS | highest IS Sharpe of the book | s06 / s48 | 0.7672 | +0.0681 | 0.6023 | −0.1232 |
| S_DISP | highest IS dispersion | q0.5~s53 | 0.5435 | −0.1556 | 0.6849 | −0.0406 |
| S_EVOL | LOWEST IS eligible-set vol | q0.5~s47 | 0.5352 | −0.1639 | 0.6760 | −0.0496 |
| S_EWALL | highest IS EWall Sharpe | q0.5~s38 | 0.4873 | −0.2118 | 0.6124 | −0.1131 |
| ANCHOR | do nothing | — | 0.6991 | 0.000 | 0.7255 | 0.000 |

**S_CORR is the only selector that beats the anchor, SPY and RULES v2 out of sample in both books**
(vs SPY +0.1884 / +0.1310; vs v2 +0.2050 / +0.1476), with regret **0.1155 / 0.0369** against the
stratum's best panel — at n=20 it lands within 0.04 Sharpe of the single best of 60 draws, the
**96.7th percentile** at both n. Its sign check is ordinally right at both extremes: the reverse
extreme (highest IS corr, s47) lands at 0.5352 / 0.6760, *below* the anchor. Every other selector's
sign check is ambiguous or inverted.

S_DISP and S_EVOL both LOSE to the anchor even though `disp` orders the stratum strongly
(ρ +0.53) — the argmax of dispersion picks a tail panel whose dispersion came from bad names.
An ordering that is real in the middle of the distribution does not have to survive an argmax
selector, and this run is a clean instance of that gap.

## KEEP paths — every one of the 525 cells

| stratum | arm | n cells | 4a | 4b | mean full Sharpe | mean OOS Sharpe | mean MaxDD |
|---|---|---|---|---|---|---|---|
| q=0.0 | CAND20 / EWall | 20 / 20 | 0 / 0 | 6 / 7 | 0.9945 / 1.0217 | 0.9829 / 1.0102 | −24.8% / −24.4% |
| **q=0.5** | CAND10 / CAND20 / EWall | 60 each | 0 | **1 / 2 / 2** | 0.706 / 0.751 / 0.748 | 0.699 / 0.726 / 0.722 | −28.2% / −27.0% / −26.8% |
| q=1.0 | all | 100 | 0 | **0** | 0.248 / 0.245 / 0.248 | 0.219 / 0.221 / 0.227 | −43.9% / −43.2% / −43.1% |
| NAMED | — | 25 | 0 | 2 (U56/CAND20, B136/EWall) | | | |

**4a 0/525** — RULES v2 is beaten nowhere, consistent with the whole record.
**4b 23/525**, 20 of them at q ≤ 0.5 and **none at q = 1.0**, reproducing idea 276's admissibility
shape. Only **5 of 300** stratum cells pass, and the passers have lower IS corr than the
non-passers (0.244 / 0.250 vs 0.275 / 0.275) — the same direction as Q1, on the KEEP path itself.

**S_CORR's pick is NOT a KEEP.** q0.5~s34 at n=10 is 15.36% / 1.0166 / −24.18%, halves 0.959/1.072,
OOS 1.0704: it beats SPY in **both halves and out of sample** and clears the CAGR floor, and fails
4b on the **drawdown cap alone** (−24.2% against the −20.2% bar = 60% of SPY's −33.7%). Same story
at n=20 (12.85% / 0.9892 / −24.06%, halves 0.962/1.020, OOS 1.0130, fails DD only). A half-small-cap
panel carries small-cap drawdowns; the selector cannot fix that.

## Honest limits

- **60 draws are not 60 independent panels.** Every panel is a 20+20 subset of the same 100 large
  and 439 small names, so panels share constituents and the permutation p-values, which are valid
  under label exchangeability, still overstate the effective sample. The split-half replication
  (which shares the same overlap structure) is the more informative robustness number, and it is
  weaker than the full-sample ρ: −0.55 / −0.22 at n=10.
- **One stratum, one k.** q = 0.5 and k = 40 were fixed by the queue. Whether the corr ordering
  holds at q = 0.25 or 0.75, or at k = 20 or 80, is untested here.
- **Six selectors were pre-registered and one won.** S_CORR's margin is supported by the n=60
  ordering (p 0.0003–0.0046), the monotone tercile table and the correct sign check, not by the
  single pick alone — but the pick itself sits at the 96.7th percentile, and an argmax landing in
  the top tail is partly luck. The tercile gradient (low-corr mean 0.806 vs SPY 0.882 at n=20) is
  the honest effect size, and **it still loses to SPY**: only 9 of 60 stratum panels beat SPY OOS.
- **What `corr` might be proxying for is not established.** At fixed q it is not capitalisation,
  but it could be sector concentration or factor overlap among the 20 large names. Nothing here
  rules that out; the queue entries below are the follow-ups.
- **SURVIVORSHIP.** SMALL439 and BSTK100 are current constituents. The bias is common to all 60
  panels and inflates the between-panel spread in level, which is the raw material a characteristic
  would have to order — so it runs *toward* finding structure. The breadth KILL is conservative;
  the corr/disp survival is an upper bound.

## What this means for the record

Idea 276 counted **26 files (upper bound) and 14 (tight lower bound)** whose headline attributes a
result to a panel property across the capitalisation line. This run says those files split two ways,
and neither way leaves the claim as written:

- files leaning on **breadth** state a relation that is **zero** once cap mix is held fixed;
- files leaning on **dispersion, correlation or eligible-set vol** state a relation whose
  **sign reverses** once cap mix is held fixed.

**RULES wording recommended: none.** No 4a pass, no 4b pass from any selector, and the one selector
that transfers picks a panel that fails the drawdown cap. Recommended to PROTOCOL as a reporting
habit, not a rules change: **when a claim orders panels on a characteristic, report the panels'
capitalisation mix beside it, and state whether the comparison is within or across that mix** —
because on this data the two give opposite answers for three of the four characteristics in use.

Ideas 293–295 queued.

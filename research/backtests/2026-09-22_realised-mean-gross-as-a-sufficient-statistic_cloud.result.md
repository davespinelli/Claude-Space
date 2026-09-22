# Idea 1494 — is REALISED MEAN GROSS a SUFFICIENT STATISTIC for every DEVICE-vs-DEGROSS loss?

**Lane cloud, 2026-09-22. Script `2026-09-22_realised-mean-gross-as-a-sufficient-statistic_cloud.py`.
VERDICT: ANSWERED = NO at the metric level — KILL of the sufficiency premise — but YES at the
DECISION level. NO NEW CAPITAL BOOK (4a 0 of 228 cells; the only 4b passers are the plain
gross ladder, i.e. the standing 2026-09-04 candidate's own family, with no device at all).**

90 device books (3 panels x 6 families x 5 rungs), each against its OWN exactly-gross-matched
de-gross twin, plus a 48-rung pure gross ladder (3 panels x 16 scale factors). Exactly two
tuned parameters, (N, H) = (20, 126), **frozen** at the committed anchor and not searched.

## Gates

| gate | value |
|---|---|
| G0 | SMALL house filter: **54 tickers dropped** (max_1d_move >= 1.0), 665 names kept, SPY benchmark only and never a constituent |
| G1 | twin gross match: max abs difference **1.92e-07** over 90 books, median 1.92e-08 — the twin sits at the device's own realised mean gross |
| G2 | circular block bootstrap LB = 65d, B = 400, seed 20260922, the SAME blocks for all 90 books in a replicate |
| internal | `MADIST k=0.00` and `MAXVOL m=0.60` reproduce BASE bit-for-bit (residual +0.0000 on every metric), so the device machinery is a no-op at its own base rungs |

## A. The residual is NOT zero — the premise fails

Device minus its own gross-matched twin, mean over each family's 5 rungs, SE from the block
bootstrap:

| panel | family | R_CAGR | t | R_MaxDD | t | R_Sharpe | t |
|---|---|---|---|---|---|---|---|
| U56 | BAND | **+0.0044** | +1.94 | -0.0032 | -0.39 | +0.0115 | +0.65 |
| U56 | MADIST | +0.0000 | +0.00 | -0.0042 | -0.31 | **-0.1055** | **-2.11** |
| U56 | MAXVOL | **-0.0116** | **-2.50** | +0.0208 | +1.82 | -0.0340 | -0.85 |
| U56 | SPYFILT | -0.0016 | -0.22 | -0.0085 | -0.33 | -0.0681 | -1.01 |
| U56 | STOP | -0.0115 | -1.83 | -0.0230 | -1.09 | **-0.1947** | **-3.28** |
| U56 | VOLTGT | -0.0060 | -1.48 | +0.0269 | +1.74 | -0.0194 | -0.49 |
| B136 | BAND | -0.0017 | -0.88 | -0.0030 | -0.52 | -0.0131 | -1.18 |
| B136 | MADIST | **-0.0100** | **-2.21** | -0.0068 | -0.42 | **-0.0785** | **-2.46** |
| B136 | MAXVOL | **-0.0204** | **-3.73** | +0.0113 | +0.79 | -0.0733 | -1.95 |
| B136 | SPYFILT | -0.0099 | -1.03 | -0.0050 | -0.16 | -0.1190 | -1.64 |
| B136 | STOP | **-0.0150** | **-2.18** | -0.0220 | -1.06 | **-0.1755** | **-3.45** |
| B136 | VOLTGT | -0.0079 | -1.51 | +0.0345 | +1.53 | -0.0208 | -0.43 |
| SMALL | BAND | -0.0036 | -1.73 | -0.0091 | -0.70 | -0.0220 | -1.76 |
| SMALL | MADIST | +0.0005 | +0.18 | -0.0007 | -0.06 | +0.0038 | +0.22 |
| SMALL | MAXVOL | -0.0064 | -0.51 | -0.0485 | -1.07 | -0.0292 | -0.34 |
| SMALL | SPYFILT | +0.0113 | +0.91 | -0.0084 | -0.13 | +0.0602 | +0.65 |
| SMALL | STOP | **-0.0299** | **-2.31** | **-0.1912** | **-2.52** | **-0.3645** | **-2.76** |
| SMALL | VOLTGT | -0.0053 | -0.84 | -0.0100 | -0.33 | -0.0334 | -0.64 |

**POOLED over all 90 books: R_CAGR = -0.0069 (SE 0.0030, t -2.29), R_Sharpe = -0.0709
(SE 0.0281, t -2.53), R_MaxDD = -0.0139 (SE 0.0116, t -1.20).**

Two things follow, and the second is the one the record has not said:

1. The pooled residual is **resolvably negative on CAGR and Sharpe**. At its own realised mean
   gross a device is not merely "no better" than a plain de-gross — it is **0.69 pp/yr of CAGR
   and 0.071 of Sharpe worse**, at 2.3 and 2.5 SE.
2. **It buys nothing on the leg it was built for.** R_MaxDD pools to **-0.0139** — the wrong
   sign for a drawdown-buying device — and is not resolvable (t -1.20). Only VOLTGT and MAXVOL
   show a positive drawdown residual anywhere and neither clears 2 SE (best: U56 MAXVOL +1.82,
   B136 VOLTGT +1.53).

**The residual is also not ONE number.** It ranges from **+0.0115** (U56 BAND Sharpe) to
**-0.3645** (SMALL STOP Sharpe), a spread of 0.376 of Sharpe, and its sign flips by family and
by panel (SMALL SPYFILT +0.0602, U56 SPYFILT -0.0681). The eight 2026-09-19 runs were therefore
**not** re-discovering one scalar; they were measuring six different exchange rates, and three
of them (STOP everywhere, MADIST on the large panels, MAXVOL on B136) are resolvably bad.

## B. Gross is a good sufficient statistic for CAGR and a bad one for MaxDD

OLS of the metric on realised mean gross ALONE, pooled within panel over all 30 device books:

| panel | R2 CAGR | slope | residual sd | R2 MaxDD | slope | residual sd |
|---|---|---|---|---|---|---|
| U56 | **0.7885** | +0.1992 | 0.0099 | **0.2837** | -0.1450 | 0.0220 |
| B136 | **0.6624** | +0.2421 | 0.0132 | **0.3328** | -0.2096 | 0.0226 |
| SMALL | **0.5655** | +0.1152 | 0.0159 | **0.0017** | -0.0122 | 0.0463 |

Within a single family the CAGR fit is often near-perfect (U56 MADIST 0.9957, STOP 0.9901,
SPYFILT 0.9790, MAXVOL 0.9741, VOLTGT 0.9665; B136 VOLTGT 0.9747, STOP 0.9612) — but the MaxDD
fit is not: **0.0017 on SMALL pooled**, 0.0601 (B136 MAXVOL), 0.0903 (SMALL MAXVOL), 0.1270
(B136 SPYFILT), 0.1566 (SMALL STOP), 0.1788 (U56 STOP). VOLTGT is the one family whose drawdown
is a pure gross function (R2 0.9825 / 0.9878 / 0.9356) — which is exactly what it is built to
be. **So "a device is just a de-gross" is close to true for the return leg and false for the
drawdown leg**, and the drawdown leg is the one 4a is decided on.

## C. Both KEEP paths at all 228 published cells

| population | 4a | 4b |
|---|---|---|
| 90 devices | **0 of 90** | 29 of 90 |
| 90 gross-matched twins | **0 of 90** | **49 of 90** |
| 48 ladder rungs | **0 of 48** | 6 of 48 |

Per panel: U56 devices 0/30 4a, 16/30 4b (twins 21/30); B136 13/30 4b (twins 28/30); **SMALL 0
of 30 on both paths, and its twins 0 of 30 too.** The twins pass 4b **more often than the
devices they are matched to** (49 vs 29) — the sharpest form of the record's standing result.

The six ladder 4b passes are the **BASE book with no device at all**, at f = 0.80-1.10:
U56 f=1.00 (realised gross 0.720) **12.24% / 1.0644 / -17.99%**, OOS Sharpe 1.1133, against SPY
15.14% / 0.8851 / -33.72%; B136 f=1.00 (gross 0.742) 14.55% / 1.0473 / -19.39%, OOS Sharpe
0.9498. That is the **standing 2026-09-04 candidate's own family** (top-N equal weight, no vol
scaler), reproduced here as a by-product — **not a new book**.

## D. Rule 8 — the DECISION is gross-decidable even though the metric is not

Dials chosen on the IS window (panel start .. 2016-12-31) only; 2017-2026 read exactly once.
DEVICE chooser = argmax IS Sharpe over that panel's 30 device books; GROSS-ONLY chooser =
argmax IS Sharpe over its 16 ladder rungs.

| panel | chooser | pick | IS Sharpe | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|
| U56 | DEVICE | MAXVOL m=0.80 | 1.0838 | 14.05% | 1.1113 | -18.50% |
| U56 | GROSS-ONLY | f=0.80 | 1.0014 | 10.72% | **1.1131** | **-14.54%** |
| U56 | BASE / RULES v2 / SPY | — | 1.0014 / 1.1043 / 0.8986 | 13.43% / 9.46% / 15.29% | 1.1133 / **1.2767** / 0.8751 | -17.99% / **-12.05%** / -33.72% |
| B136 | DEVICE | MAXVOL m=0.80 | 1.2453 | 15.07% | **1.0124** | -19.37% |
| B136 | GROSS-ONLY | f=1.60 | 1.1773 | 21.22% | 0.9522 | -30.00% |
| B136 | BASE / RULES v2 / SPY | — | 1.1759 / 1.0922 / 0.8987 | 13.41% / 7.85% / 15.26% | 0.9498 / **1.1017** / 0.8737 | -19.39% / **-12.24%** / -33.72% |
| SMALL | DEVICE | MAXVOL m=0.25 | 0.9560 | **-1.02%** | **-0.0391** | -33.98% |
| SMALL | GROSS-ONLY | f=1.60 | 0.2734 | 9.67% | **0.4685** | -42.51% |
| SMALL | BASE / RULES v2 / SPY | — | 0.2705 / 0.8632 / 0.8316 | 6.90% / 4.41% / 15.29% | 0.4669 / **0.6472** / 0.8751 | -28.55% / **-12.48%** / -33.72% |

**SUFFICIENCY OOS GAP (device chooser minus gross-only chooser), Sharpe: U56 -0.0018,
B136 +0.0601, SMALL -0.5076.** Searching thirty devices instead of sixteen gross rungs buys
**nothing** on U56 (a dead heat to the third decimal), +0.06 on B136, and **costs -0.51 on
SMALL**, where the IS argmax device (MAXVOL m=0.25) returns **-1.02% CAGR at Sharpe -0.0391**
out of sample. So the record's eight device runs were, at the level of the DECISION they
support, one gross ladder — even though the metric residual that justified them is resolvably
non-zero. And on the axis that matters, the live RULES v2 book beats both choosers on OOS
Sharpe and drawdown on all three panels.

## Caveats

One cadence (W), one cost rung (10 bps), one gross anchor (0.75), one phase (Friday), t+1,
(N, H) frozen at (20, 126). The devices are the six families the 2026-09-19 runs used; a
seventh family could sit anywhere in the observed +0.01 to -0.36 Sharpe range. Residual SEs are
block-bootstrap (LB 65d, B 400) on a paired contrast; no multiplicity correction is applied
across the 18 family cells, so the two or three marginal |t| ~ 2 readings should be treated as
suggestive and the pooled figures as the headline. **Rule 9 SURVIVORSHIP:** B136 and SMALL are
CURRENT constituents of their screens (SMALL additionally drops 54 tickers with max_1d_move >=
1.0), so every absolute CAGR and every 4a/4b pass count on those panels is upward-biased; the
residual is a within-panel, within-book, same-days contrast and is first-order immune to it.

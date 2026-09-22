# Idea 1465 — does the beta band's CAGR premium ON SMALL survive a turnover-matched and a permutation control?

**Lane cloud, run 22, 2026-09-22.  Script:** `research/backtests/2026-09-22_small-band-cagr-premium-controls_cloud.py`
**VERDICT: ANSWERED — the premium is REAL and it is a BETA-ORDERING premium, not a rebalancing-frequency
artefact.  It is NOT a book: 0 of 30 SMALL cells clear 4b (the DD leg fails 30 of 30).  MECHANISM finding +
KILL of the rebalancing-artefact reading + KILL of SMALL as a 4b panel at this N/gross.  No RULES change.**

**SURVIVORSHIP (PROTOCOL rule 9).**  The SMALL panel is the CURRENT constituents of a sub-$2B screen
(`data/SMALL_PANEL_README.md`), so every *level* on it is biased UP; 54 tickers with `max_1d_move >= 1.0`
were dropped before anything was computed, leaving 665 investable names, 2010-01-04..2026-09-18 (15.6y).
Every comparison below is WITHIN that panel — cell vs its own same-H anchor vs its own two controls, all
holding the IDENTICAL names on the IDENTICAL rows — which is exactly why the PREMIUM, not the level, is the
object of the run.  The 4b bars are still read against SPY and so remain survivorship-contaminated; that is
one more reason the capital answer here is NO.

## The premise replicates exactly (cross-script, vs idea 1444)
Cell CAGR minus its own same-H `c = 0` anchor, over the 24 biting cells (c > 0):

| panel | positive | median | min | max |
|---|---|---|---|---|
| SMALL | **24 of 24** | +1.198 pp | +0.336 | +3.182 |
| U56 | **0 of 24** | -2.178 pp | -4.109 | -0.748 |

The U56 `(c=0, H=126)` anchor reproduces the committed incumbent to the published digits
(15.80% / 1.1537 / -19.13% full; 17.32% / 1.1857 / -19.13% OOS).

## Control 1 — RANK-PERMUTATION twin (K = 8 seeds): the ordering carries ALL of it
Same weight multiset, same names, same name count, same effective N, same gross — only the assignment of
weight to name is randomised.

| panel | cell beats PERM | median d | resolved \|t\|>2 | PERM premium over anchor |
|---|---|---|---|---|
| SMALL | **24 of 24** | **+2.920 pp** | **24 of 24** | POSITIVE at **0 of 24** (median **-1.541 pp**) |
| U56 | 0 of 24 | -0.264 pp | 0 of 24 | positive at 0 of 24 (median -1.770 pp) |

The permutation twin does not merely fail to reproduce the premium on SMALL — it goes the *other way*
(-1.54 pp).  The whole +1.20 pp median is bought by WHICH name gets the cap, i.e. by the trailing-beta
ordering.  Realised book beta falls monotonically with c (1.05 -> 0.77 at H = 126), so the channel is a
genuine low-beta tilt.

## Control 2 — TURNOVER-MATCHED REBALANCE CONTROL (zero cross-sectional information)
The same-H equal-weight anchor reset to its target every `k` trading days inside each min-hold segment,
`k` SOLVED over a fixed ladder to match the cell's realised turnover (median match error 4.6%, max 10.1%).

| panel | cell beats TMRC | median d | resolved \|t\|>2 | TMRC premium over anchor |
|---|---|---|---|---|
| SMALL | **24 of 24** | +1.086 pp | 8 of 24 | median **+0.018 pp** |
| U56 | 0 of 24 | -2.174 pp | 24 of 24 | median +0.022 pp |

Forced extra rebalancing at matched turnover is worth **~2 bp/yr on both panels** — statistically nothing.
The "rebalancing-frequency artefact" reading of idea 1444's asymmetry is **KILLED on its own currency**.

## The capital answer: NO BOOK
The idea's own clause required the DD leg to move.  It does move — every c lowers MaxDD (SMALL: shallower
than its anchor at 22 of 24, than PERM at 23 of 24, than TMRC at 23 of 24) — but nowhere near enough.

| SMALL | CAGR | Sharpe | MaxDD | H1 / H2 |
|---|---|---|---|---|
| best-Sharpe cell (H = 252, c = 1.00) | 14.00% | 0.9049 | -31.49% | 1.2110 / 0.6549 |
| its own anchor (H = 252, c = 0) | 12.28% | 0.7483 | -35.37% | 0.9694 / 0.5587 |
| frozen anchor (H = 126, c = 0) | 7.81% | 0.5092 | -36.51% | 0.6791 / 0.3826 |
| RULES v2 (live) | 8.14% | 1.1638 | -12.05% | 1.0664 / 1.2538 |
| SPY | 14.03% | 0.8571 | -33.72% | 0.9028 / 0.8409 |

4b on SMALL: **0 of 30 FULL, 0 of 30 OOS**; leg failures H1 16/30, **H2 30/30**, **DD 30/30**, CAGR 5/30.
The 4b DD cap is 0.60 x SPY's -33.72% = **-20.23%**; SMALL's shallowest cell is **-31.01%**, i.e. still
**10.8 pp outside**.  4a: 0 of 30 (the live book draws -12.05%).  U56 for contrast: 16 of 30 FULL and
16 of 30 OOS clear 4b, all of them at LOWER c — the band costs U56 CAGR and never buys a pass.

## Rule 8 walk-forward — (c, H) chosen on warm-up..2016-12-31, 2017-2026 read ONCE
| panel | chooser | pick | OOS CAGR | OOS Sharpe | OOS MaxDD | 4b OOS |
|---|---|---|---|---|---|---|
| SMALL | C_ISSHARPE | H=252, c=1.00 | 11.05% | 0.7204 | -31.49% | no |
| SMALL | C_ISPREM | H=21, c=1.00 | 10.73% | 0.6649 | -37.97% | no |
| SMALL | C_ANCHOR (zero-parameter) | H=126, c=0 | 6.70% | 0.4398 | -36.51% | no |
| SMALL | SPY | — | 15.29% | 0.8753 | -33.72% | — |
| SMALL | RULES v2 | — | 9.46% | 1.2770 | -12.05% | — |
| U56 | C_ISSHARPE | H=378, c=0.50 | 14.00% | 1.0455 | -20.30% | no |
| U56 | C_ISPREM | H=21, c=0.00 | 15.17% | 1.1088 | -20.19% | **yes** |
| U56 | C_ANCHOR (zero-parameter) | H=126, c=0 | **17.32%** | **1.1857** | **-19.13%** | **yes** |

Both legal SMALL choosers beat the zero-parameter anchor OOS by a wide margin (+0.281 / +0.225 of Sharpe)
— the dial is *learnable* — and both still lose to SPY's OOS Sharpe (0.8753) and miss 4b on the DD leg.
On U56 the ZERO-PARAMETER anchor beats every fitted pick OOS again, the record's standing pattern.

## What this changes
1. Idea 1444's SMALL asymmetry is now **explained and controlled**, not merely observed: it is the beta
   ordering (PERM reverses it at 24 of 24), and it is NOT churn (TMRC is worth 2 bp/yr).
2. The **turnover-matched rebalance control (TMRC)** is a cheap, zero-information control that any future
   run pricing a device that raises turnover should carry; here it retired the competing explanation in one
   pass on both panels.
3. **SMALL stays closed for 4b at N = 20 / gross 0.75**: the DD leg fails 30 of 30 and the best cell is
   10.8 pp outside the cap.  A low-beta tilt that buys 4-5 pp of drawdown cannot close a 17 pp gap.

**34 gates recorded, 0 FAIL** (G0 sample; G1 c=0 == anchor bit-identical at 6 H; G2 c=0 PERM == c=0 cell;
G3 identical name frame per H; G4 all 30 cells published per panel; G5 exactly 2 tuned parameters; G6
choosers read no OOS row; G7 exposure channel shut to 0.00e+00; G8 every non-empty rebalance sums to 0.75;
G9 band width strictly increasing in c; G12 headline recompute bit-identical; G13 H dial bites; G14 the
drop rule removed 54 names).  RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py NOT modified.

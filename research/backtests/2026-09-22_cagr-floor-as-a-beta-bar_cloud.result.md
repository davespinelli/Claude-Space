# Idea 955 — is the 4b CAGR FLOOR a BETA BAR in disguise? (lane cloud, 2026-09-22)

**ANSWERED = YES on the DIAGNOSIS, KILL of the REMEDY.** The floor *is* a beta bar — beta
explains **96.3%** of the CAGR spread across the gross ladder and the floor binds as a
gross-1.00 bar. But a beta-matched comparand is not a re-calibration of that bar, it is a
**deletion**: its 4b pass set is **identical to having no CAGR floor at all at 288 of 288
unlevered cells**, on the full-sample and the OOS leg alike. PROTOCOL rule 4b's floor stands.

Script: `2026-09-22_cagr-floor-as-a-beta-bar_cloud.py`. **432 cells published** (3 panels x 3 books
{RULESV2 band .03, BAND06, V1N20} x 6 gross rungs x 2 cadences x 4 cost rungs), of which **288 are
unlevered** and carry every KEEP count; gross 1.25/1.50 are priced and published as an unfinanced,
NOT-ADOPTABLE arm per PROTOCOL rule 2 and are excluded from all counts. Two tuned dials and no
more: **GROSS LADDER** and **FLOOR DEFINITION**.

Floor definitions (the dial under test): `F_SPY70` CAGR >= 0.70*CAGR(SPY) (the incumbent);
`F_BETA` >= 0.70*beta*CAGR(SPY); `F_GROSS` >= 0.70*mean realised gross*CAGR(SPY); `F_NONE`
no floor (zero-information control). Under rule 8 the beta and gross used in the floor are
estimated on **2009-2016 only**; 2017-2026 is read once.

## Gates (12 of 12 exact)
| gate | max abs diff |
|---|---|
| G1 numpy engine == `engine.backtest`, 3 panels x {W,M} | **0.000000** (6 of 6) |
| G2 `bk_rulesv2(0.75)` == `baseline.rules_v2_weights` | **0.000000** (3 of 3) |
| G3 beta(SPY, SPY) == 1 | **0.000000** (3 of 3) |

## 1. The diagnosis holds: the CAGR leg is 96% a beta reading
Over the 24 (panel, cadence, cost) families, spearman(beta, CAGR) has median **+0.9580** and the
OLS R^2 of CAGR on beta has median **0.9626**; median residual sd is **0.0060** against a CAGR sd
of **0.0328**, i.e. **beta explains 96.3% of the CAGR spread**. At the live 0-10 bps rungs R^2 runs
0.945-0.999 on all three panels. It decays only at 50 bps (U56/W 0.534, SMALL/W 0.123), where
turnover cost — not exposure — starts to move CAGR.

**And the incumbent floor binds exactly where beta is highest.** At 10 bps, unlevered, the number
of cells clearing `F_SPY70` by gross rung: U56 **0/0/1/6** and B136 **0/0/1/6** at gross
0.25/0.50/0.75/1.00, SMALL **0/0/0/0** at every rung. The floor is, on these books, a
**gross-1.00 bar** — which is a beta bar, since beta is proportional to gross by construction.

## 2. The remedy fails: a beta-matched floor is not a bar at all
| floor | 4b full | 4b OOS | 4b full+OOS | CAGR leg rejects (full / OOS) | rule-8 abstentions |
|---|---|---|---|---|---|
| `F_SPY70` (incumbent) | 19 | 18 | 16 | 244 / 249 of 288 | **39 of 72** |
| `F_BETA` | **137** | **140** | **137** | 16 / 49 | 2 |
| `F_GROSS` | **137** | **140** | **137** | 52 / 116 | 8 |
| `F_NONE` (control) | **137** | **140** | **137** | 0 / 0 | 0 |

`F_BETA`'s and `F_GROSS`'s 4b pass sets are **element-for-element identical to `F_NONE`'s**, full
and OOS, at all 288 cells. The 16 cells `F_BETA` does reject are cells that already fail another
leg, so the floor never decides a verdict it did not also decide by being absent.

**Mechanism, exactly.** Along the gross ladder the book's own CAGR-per-unit-beta is
dCAGR/dbeta = **0.2362** (U56), **0.2139** (B136), **0.1507** (SMALL) with a positive intercept,
while a beta-matched floor has slope 0.70*CAGR(SPY) = **0.1060 / 0.1059 / 0.0982**. The book's line
lies above the floor's line at every beta on the ladder, so the bar is **non-binding by
construction**. A beta-matched floor only starts to bind at a multiplier
**k > 1.560 (U56), 1.415 (B136), 1.074 (SMALL)** in `CAGR >= k*beta*CAGR(SPY)` — i.e. one would
have to demand 156% of the beta-matched comparand on U56 before the leg said anything at all.
The incumbent's 0.70 is therefore not a mis-calibrated beta bar; **0.70 of SPY is the only
setting of this family that is a bar.**

## 3. Which committed CAGR-leg failures survive?
Of 288 unlevered cells, **244 fail the incumbent floor**; **228 of those clear `F_BETA`** and
**118 of those clear every other 4b leg** (Sharpe in both halves, DD cap) on the full sample and
on OOS alike. But per section 2 all 118 survive **because the bar was removed, not re-calibrated**,
and their economics say the same thing: the rescued cells are de-grossed near-cash books —
U56 RULESV2 at gross 0.25 reads **CAGR 2.85%** (Sharpe 1.2010, MaxDD -4.10%) against SPY's
15.14%. A 4b "pass" for a 2.85% CAGR book is precisely what the floor exists to prevent.

## 4. KEEP paths
* **4a: 30 of 288** (vs live RULES v2 on the same panel and cost rung).
* **BOTH 4a and 4b under the incumbent floor: 0 of 288.**
* **BOTH 4a and 4b under the beta floor: 5** — all five at the **50 bps** rung on B136 at gross
  0.25-0.50, CAGR **2.47%-5.13%**, i.e. near-cash books that clear 4a only because 50 bps crushes
  the baseline harder than it crushes them. **Recorded, not candidates.** No new KEEP.

## 5. Rule 8 (gross chosen on 2009-2016 among the rungs each floor admits IN SAMPLE; OOS read once)
The floor definition moves the **label**, not the **book**: the four arms pick the **same gross at
57 of 72 families**, and median OOS Sharpe is **0.9876 for all four arms**, identical to four
decimal places. What does change is abstention: the incumbent floor admits **no** gross rung in
sample at **39 of 72** families against `F_BETA`'s 2 and `F_NONE`'s 0. Scored on the **incumbent**
floor out of sample, all four arms read **16-17 of 72** — the beta floor's extra passes (25 of 72
on its own floor) exist only in its own units.

## Honest caveats
* SURVIVORSHIP: all three panels are CURRENT constituents; SMALL is the sub-$2B screen with the
  54 names whose `max_1d_move >= 1.0` dropped (665 remain). Every SMALL number is
  survivorship-inflated and reported, never adopted alone.
* Beta is an in-sample OLS statistic of the book against SPY; the rule-8 arm uses the 2009-2016
  estimate only, but the full-sample arm in section 1 is a **measurement**, not a rule-8 result.
* The R^2 = 0.96 is measured **along the gross ladder**, where exposure is the dominant moving
  part by construction. It says the floor cannot distinguish de-grossing from skill; it does not
  say CAGR carries no skill information on other axes.

## Verdict
**ANSWERED = YES (the 4b CAGR floor is 96% a beta reading and binds as a gross-1.00 bar) +
KILL of the beta-matched and exposure-matched comparands as replacements (pass set identical to
NO FLOOR at 288 of 288 cells; non-binding by construction below k = 1.56/1.42/1.07) +
KILL of the 5 BOTH-path cells as candidates (2.5%-5.1% CAGR near-cash books at 50 bps).
NO NEW KEEP. PROTOCOL rule 4b's 0.70-of-SPY floor stands unchanged.**

# Idea 483 — which published residualisations are IN-SAMPLE fits? (cloud, 2026-09-09)

**Verdict: ANSWERED; idea 252's generalisation REFUTED on a fresh grid. The exposed class is
3 files, not the record; the mechanism reproduces and scales with p/n, but idea 252's headline
flip (survive 0.000 in sample -> 0.675 out of fold) reproduces at 0 of 144 grid points, and the
RIDGE PENALTY, not the folding, is the dominant dial. No KEEP, no memo, no RULES change.
RULES.md, scan.py, bot.py, baseline.py and PROTOCOL.md untouched.**

Script `2026-09-09_which-published-residualisations-are-IN-SAMPLE-fits_cloud.py`; outputs
`.census.csv` (70 rows), `.grid.csv` (144 rows, ALL reported), `.walkforward.csv` (288 rows),
`.keeppaths.csv` (600 rows), `.console.txt`. Two tuned parameters only: fold count K in
{2,3,5,10} and ridge penalty lam in {1e-3,1e-2,0.1,1,10,100}. 10 bps, weekly, next-day
execution. Runtime 1284 s.

## A. Census (static scan of every committed .py under research/, heuristic)

| files with a fit call (`lstsq`/`polyfit`/`solve`/`pinv`/`Ridge`/`OLS`/`curve_fit`) | 70 |
|---|---|
| ... with NO fold/holdout machinery anywhere in the file | **66 (94.3%)** |
| ... with a wide (per-name / dummy / design-matrix) hint | 5 |
| ... **wide AND unfolded — the >10-parameter in-sample class idea 483 asks about** | **3** |

So the unfolded-fit habit is near-universal (94.3%) but almost entirely LOW-DIMENSIONAL:
the record's typical fit is a 1-2 parameter slope or a `polyfit`, where the artefact is small
(measured below). Only **3 files** sit in the regime idea 252 exposed. The scan is file-level
regex: "has fold machinery" is an UPPER bound on discipline (a file can fold one fit and not
another) and the wide hint is a LOWER bound. Census is in `.census.csv`, one row per file.

## B. Re-run out of fold — 200 draw books per panel, k=20 names, EW, weekly, 10 bps

`survive = pR2(sd | control) / R2(sd raw)`, the record's own convention (idea 252 quotes 0.000
in sample and 0.675 out of fold). Raw signal: U56 t +2.49 (R2 0.0304), B136 t +4.30 (0.0856),
SMALL439 t +1.02 (0.0052 — below |t|>=2, so its survive ratios are suppressed as
uninterpretable rather than reported as noise divided by noise).

**The mechanism reproduces, decisively, and is monotone in p/n** (median over the grid):

| panel | width | p | p/n | control reproduces `sd` IS | ... OUT OF FOLD | fit of y IS | ... OOF |
|---|---|---|---|---|---|---|---|
| U56 | WIDE | 55 | 0.28 | 0.9766 | 0.9387 | 0.9877 | 0.9662 |
| B136 | WIDE | 135 | 0.68 | 0.9866 | 0.6676 | 0.9946 | 0.7636 |
| SMALL439 | WIDE | 439 | 2.20 | **0.9984** | **0.3151** | 0.9972 | **0.0251** |
| B136 | NARROW10 | 10 | 0.05 | 0.1356 | 0.0224 | 0.1515 | 0.0166 |
| SMALL439 | NARROW10 | 10 | 0.05 | 0.0482 | -0.1154 | 0.0193 | -0.1058 |
| U56 | NARROW10 | 10 | 0.05 | 0.6779 | 0.6263 | 0.1876 | 0.0926 |

The in-sample wide control reproduces the very summary it is meant to control for at R2
0.977-0.998 on every panel — idea 252's 0.998-0.9996 is not special to B136. Out of fold that
collapses to 0.315 at p/n 2.20. **The ~10-parameter line in the idea text is real**: at
NARROW10 the IS and OOF answers differ by <= 0.05 of survive on B136 (0.5002 vs 0.5050), so
folding a small fit changes nothing.

**But idea 252's reported flip does not generalise.** Grid points reproducing its signature
(survive_IS < 0.05 AND survive_OOF > 0.30): **0 of 144** (WIDE 0/72, NARROW 0/72). The
direction alone (sd survives more out of fold) holds in only **22 of 72** WIDE points and 19 of
72 NARROW. On B136 WIDE at lam=0.001 the pair is 0.0199 (t +0.58) vs 0.0682 (t +0.94): right
sign, an order of magnitude short of 0.000 -> 0.675.

**The penalty dominates the folding.** On B136 WIDE, `survive` runs 0.020 -> 0.959 as lam goes
1e-3 -> 100 (t_IS +0.58 -> +4.21), while the IS-vs-OOF gap at any fixed lam is <= 0.13. Same on
U56 (0.249 -> 1.269). A residualisation result quoted without its penalty is therefore
uninterpretable, whether or not it was folded — that is the transferable finding here, and it
is NOT in PROTOCOL.

## Rule 8 walk-forward (choose on the first half, evaluate on the untouched second)

| panel | S_RAW_IS_SHARPE | S_RESID_INSAMPLE | S_RESID_OOF | S_SD_ONLY | mean draw | RULES v2 | SPY |
|---|---|---|---|---|---|---|---|
| U56 OOS Sharpe | 1.1669 | 1.1069 | 1.1457 | 0.8737 | 1.0346 | **1.1828** | 0.8287 |
| B136 OOS Sharpe | 1.0540 | **1.0795** | 1.0328 | 1.0201 | 0.9847 | 0.9844 | 0.8340 |
| SMALL439 OOS Sharpe | 0.4192 | **0.5823** | 0.4192 | 0.3251 | 0.5597 | 0.5770 | 0.8577 |

The IS-fitted and OOF-fitted selectors pick a DIFFERENT draw in 3/24 (U56), 16/24 (B136) and
16/24 (SMALL439) cells, so the choice of control is not cosmetic — but **the honest control
does not pay**: median OOS Sharpe d(OOF - IS-fitted) is +0.0387 / -0.0467 / -0.1631. Fixing the
fit changes the INFERENCE, not the book. Every selector loses to SPY on OOS CAGR on all three
panels, and to the mean draw on SMALL439 — another idea-229 selection-loses instance.

## KEEP paths

**4a 0/600, 4b 0/600** across all 600 draw books (200 per panel, full sample + both halves).
Comparands: RULES v2 (live) U56 8.6%/1.204/-12.1%, B136 8.0%/1.106/-12.2%, SMALL439
3.8%/0.572/-14.7%; RULES v1 6.4%/0.661, 6.4%/0.635, 7.4%/0.565; SPY 15.2%/0.887/-33.7%
(15.2%/0.889, 14.1%/0.862 on the small panel's window). Random 20-name equal-weight books are
not capital-worthy on any panel, which is the expected result and is why they make a clean
substrate for the control question.

## Caveats

SURVIVORSHIP: B136 and SMALL439 are current constituents only (SMALL439 = the 483-name sub-$2B
panel with the 44 tickers whose `max_1d_move >= 1.0` dropped first, per `data/small_meta.csv`).
The census is a static regex scan, not an execution of the 70 files; it bounds the exposed class
rather than proving each file's fit is or is not folded. `sd` here is the cross-sectional sd of
member annualised returns over the evaluation window, idea 83's key; a different summary could
behave differently.

## Proposed follow-ups

1. Publish `lam` (and the fitted R2 of control-on-key) beside every residualisation result —
   the penalty moves `survive` by 50x, the folding by <= 0.13.
2. Re-read the 3 wide-and-unfolded census files individually at their own penalties.
3. Test whether the p/n = 1 crossover is where OOF reproduction of the key falls below 0.5.

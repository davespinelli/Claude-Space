# Idea 2270 — what COST RUNG does the STANDING CANDIDATE's 4b PASS actually LIVE ON?

**(2026-09-22, lane cloud.) ANSWERED, exactly: the standing candidate's 4b pass lives on
`0 <= c <= 45.79 bps`, and the leg that kills it is the CAGR FLOOR, not the drawdown cap.
The queue line's premise is HALF right and the half that is wrong is optimistic by ~15 bps.**

Script: `2026-09-22_4b-leg-cost-breakeven_cloud.py` · artefacts: `.grid.csv.gz` (6,666 dense
cells), `.breakeven.csv` (660 leg-breakevens), `.walkforward.csv`, `.gates.csv`, `.stdout.txt`.

## What was run
BOOK `baseline.rules_v2_weights(px, band=0.03, gross=g)` — the live book, unchanged in every
clause except size. Gross ladder g ∈ {0.25 … 1.50 step 0.125} (2264's own, rungs > 1.00 published
but flagged LEVERED and excluded from any candidate per PROTOCOL rule 2). Panels U56 / B136 /
SMALL; cadences W and M; a dense **0–100 bps cost ladder in 1 bps steps**, every rung published.
**Two tuned dials and no more: GROSS g and PANEL.** The cost ladder is the axis under test;
cadence and band are reported, not tuned.

Every 4b leg is carried as a **margin** (>= 0 passes) and its breakeven is found two ways: by
**bisection on the true metric to 0.01 bps**, and by the **analytic first-order** shorthand the
queue line proposes, `dCAGR/dc = −(annual turnover)/1e4`, `dSharpe/dc = −(annual turnover)/1e4/vol`.

## Gates — 15 of 15
| gate | result |
|---|---|
| G1 positions are cost-invariant: `r(c) = r0 − turnover·c/1e4` | **0.000000** on 6 of 6 checked cells |
| G2 reproduce 2264's twelve published headline numbers | all 12 exact — max err **1.9e-3** (turnover 2.3519 vs 2.35), **<= 4.9e-5** on every CAGR/Sharpe/MaxDD |
| G3 reproduce the 50 bps FULL CAGR miss | **−0.109 pp** (2264 published 0.11 pp: 10.49% vs floor 10.60%) |
| G4 every 4b leg margin monotone non-increasing in cost | **0 of 462** (book, leg) paths non-monotone |

## 1. The premise, tested
The queue line says the margin is "exactly linear in bps at fixed turnover because the engine
never feeds cost back into positions". **The first clause is exactly true** (G1: the
reconstruction is bit-exact), and so is the consequence that matters — SPY is a cost-free
buy-and-hold comparand, so every 4b BAR is cost-invariant and every 4b margin is monotone
decreasing in cost (G4, 0 of 462 violations). **The linearity clause is false**, because CAGR and
MaxDD are non-linear functionals of the return path. The analytic breakeven is systematically
**TOO GENEROUS on the binding leg**: median **+15.2 bps** on `L_CAGR` (n = 20, range +0.15 to
+38.1) and **+14.0 bps** on `L_CAGR_OOS` (n = 21, up to +46.5). On the Sharpe legs it is
−5.9 bps (`L_H1`, n = 55) to +6.7 (`L_H2`, n = 44) and near-exact on `L_OOS` (+0.7, n = 44).
**A breakeven quoted from the shorthand should be read as an upper bound, not a number.**

## 2. The answer — the standing candidate (U56 / W / g = 1.00), breakeven bps by leg
| leg | margin @10 bps | **exact breakeven** | analytic | analytic error |
|---|---|---|---|---|
| `L_CAGR` (CAGR >= 0.70 × SPY) | +0.009 | **45.79** | 49.75 | +3.95 |
| `L_CAGR_OOS` | +0.020 | 84.38 | 93.07 | +8.68 |
| `L_H1` (Sharpe > SPY, 1st half) | +0.271 | 117.76 | 112.77 | −4.99 |
| `L_H2` | +0.353 | 151.94 | 160.08 | +8.14 |
| `L_OOS` | +0.401 | 173.48 | 174.43 | +0.95 |
| `L_DD` (MaxDD >= 0.60 × SPY) | +0.043 | **330.91** | — | — |
| `L_DD_OOS` | +0.043 | 341.97 | — | — |
| `L4a_H2`, `L4a_DD` | −0.001, −0.039 | dead at 0 bps | — | — |

**The drawdown cap carries 7.2× the cost headroom of the CAGR floor.** The record's anxiety about
this candidate's DD leg is misplaced: at 10 bps the DD margin is +4.32 pp and survives to 331 bps,
while the CAGR margin is +0.90 pp and is gone at 45.79. The pass is a CAGR-floor object.

## 3. The panel axis, quantified
The same cell on **B136 / W dies at 11.40 bps** — 1.40 bps of headroom over PROTOCOL's own binding
10 bps rung — and its **4b-OOS reading dies at 3.29 bps** (`L_CAGR_OOS` is already −0.002 at
10 bps). That is 2264's "panel-dependent, misses the OOS CAGR floor by 0.05–0.21 pp from 5 bps on",
now stated as a number. On U56 / M the same cell lives to **81.33 bps**.

## 4. The structural finding — 4b on this book is a CAGR-floor bar, not a cost bar
`L_CAGR` is **dead at zero cost on 38 of 42 unlevered cells**: the CAGR floor kills 90% of the
gross ladder before a single basis point is charged. Only **3 of 42 unlevered cells are alive at
0 bps on all five 4b legs** — U56/W g=1.00, U56/M g=1.00, B136/W g=1.00 — and **all three bind on
`L_CAGR`**. Cost never decides WHICH leg binds on a live cell; it only decides how far the top
rung of the ladder goes. (Levered, published and not adoptable: U56/W g=1.125 dies at 91.06 bps,
g=1.25 at 117.94; B136/W g=1.125 at 51.27, g=1.25 at 56.70.)

**4a**: the 4a comparand here is cadence-matched (RULES v2 run at the book's own cadence), so the
g = 0.75 cell is an IDENTITY by construction and is the only 4a "pass" in the grid. The honest
count is **4a 0 of 36 non-identity unlevered cells** (0 of 60 including the levered rungs).

## 5. Rule 8 (g chosen on 2009-2016 ONLY; 2017-2026 read ONCE)
2264's IS-only drawdown-budget chooser (κ = 0.60, capped at 1.00) and the habitual IS-Sharpe
chooser pick **g = 1.00 at 22 of 24** (panel × cadence × cost) cells; they disagree only on
SMALL/W at 25 and 50 bps, where the budget chooser steps down to 0.875. **The chosen cell's
breakeven is a property of the book, not of the rung it was evaluated at** — U56/W reads 45.79 bps
at every one of the five sampled costs, B136/W 11.40 at every one. 4b FULL+OOS is reached at
U56/W 0–25 bps, **U56/M 0–50 bps**, B136/W FULL 0–10 and OOS 0 only, SMALL 0 of 10.

## 6. A second KEEP-4b candidate, recorded NOT recommended — and DISCLOSED POST-HOC
The same standing candidate run **MONTHLY** nearly doubles its cost life: **81.33 bps against the
weekly cell's 45.79**, on 1.64×/yr turnover against 2.35×, with `L_DD` alive beyond 400 bps. It is
the only cell in the grid that clears 4b FULL *and* OOS at **all five** sampled rungs including
50 bps. It pays 2.90 pp of drawdown margin for that. Cadence was declared REPORTED, NOT TUNED in
this run's construction, so selecting this cell is **post-hoc on the cadence axis and is disclosed
as such**. Memo: `2026-09-22_4b-leg-cost-breakeven_cloud_MEMO.md`.

## Caveats
Survivorship (PROTOCOL rule 9): U56 / B136 are 2026 constituents held from 2008 and SMALL is the
current-constituent sub-$2B screen with `max_1d_move >= 1.0` tickers dropped. Every CAGR level is
optimistic and both 4b level legs are easier than on a point-in-time panel, so **every breakeven
bps here is an UPPER bound on the real one**. Costs are flat per unit turnover — no spread, impact
or borrow, and a real 46 bps book would not trade at 46 bps flat. One band (3%), one delay (t+1).

RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py untouched.

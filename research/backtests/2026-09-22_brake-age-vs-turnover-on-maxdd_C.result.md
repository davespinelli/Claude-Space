# Idea 1505 (lane C, 2026-09-22) — does SLOWING ANY ROTATION COST DRAWDOWN, or is that specific to the CAP?

**ANSWERED = SPLIT. YES on the title question (it is NOT specific to the cap, at 100 of 120 braked rungs
and on 3 of 4 families) — and a KILL of the idea's own MECHANISM: HOLDING AGE is not the axis. TURNOVER
carries the whole correlation and AGE adds exactly 0.0000 of R-squared over it. One KEEP-4b candidate
recorded NOT recommended.**

Script `research/backtests/2026-09-22_brake-age-vs-turnover-on-maxdd_C.py`.
660 published grid rows (132 books x 5 cost rungs), 10 of 10 gates PASS.

## The books
One frozen base book — the 2026-09-04 incumbent (top N = 20 by the live 3-leg composite, MAXVOL 0.60,
equal weight, gross 0.75, weekly, t+1) — under four brake families, on three panels:

| family | dial | rungs |
|---|---|---|
| F1 MINHOLD | min-hold H | 1, 21, 42, 63, 95, 126, 189, 252, 378, 504, 756 |
| F2 CAP | per-rebalance turnover cap x mechanism | {0.05, 0.075, 0.10, 0.15, 0.20, 0.25, inf} x {CONVICTION, PRORATA} |
| F3 MINHOLD x CADENCE | H x cadence | {1, 63, 126, 252} x {W, M, Q} |
| F4 HYSTERESIS | rank exit buffer K_out (K_in = 20) | 20, 25, 30, 40, 50, 60, 80 |

All four families share ONE unbraked book (H = 1 == cap = inf == K_out = 20 == W/H = 1), bit-identical
at 0.000e+00 (gate G2).

## 1. The title question: YES, and not specific to the cap
At 10 bps, **100 of 120 braked rungs are DEEPER than their own unbraked book**; the most-braked end is
deeper at **10 of 12 (family x panel) ladders**, mean deepening **-4.30 pp**, worst **-11.16 pp** (SMALL,
H = 756). The mechanism 1484 found in the cap is present in the min-hold, in the cadence grid and in the
cap alike. **The one exception is the RANK-HYSTERESIS family**: 4 of 18 rungs deeper, and on U56 and SMALL
its most-braked rung is SHALLOWER (+2.91 pp / +0.82 pp).

## 2. The mechanism question: AGE IS NOT THE AXIS (the KILL)
MaxDD (pp) on z-scored AGE and TURNOVER, panel fixed effects, 10 bps, n = 132:

| regressor | univariate beta | OLS t | R2 | joint beta | OLS t | bootstrap t |
|---|---|---|---|---|---|---|
| AGE (days) | -0.5363 | -1.82 | 0.0249 | **+0.0135** | +0.05 | +1.30 |
| TURNOVER (x/yr) | +1.6990 | +6.58 | 0.2500 | **+1.7033** | +6.22 | +1.50 |

R2 joint = 0.2500 = R2 turnover alone. **Age contributes nothing once turnover is in, and its joint
coefficient flips sign.** The two are separable (corr -0.3228, VIF 1.12; family age-per-turnover ratios
11.9 / 42.3 / 76.6 / 85.1), so this is not a collinearity artefact — gate G8 was read before any
coefficient. Not a cost artefact either: the sign holds at every rung (b_turn_joint +1.89 / +1.79 / +1.70
/ +1.40 / +0.47 at 0 / 5 / 10 / 25 / 50 bps) and a brake LOWERS cost drag, which would push the other way.

## 3. But the surviving regressor does not resolve under the honest ruler
Paired circular-block bootstrap (L = 63, 200 reps, one start matrix per panel shared by every book,
regressors fixed, each book's MaxDD recomputed on the resampled path): pooled b_turn_joint **+1.25,
t +1.50, 95% CI [-0.32, +2.76]**, negative in 8.5% of reps. Every panel is the same story (t 0.68-1.26).
**No coefficient in this run resolves at |t| > 2.** The delete-one-calendar-year jackknife is kinder to
the sign than to the size: b_turn_joint is positive at **19 of 19** deleted years (+1.63 to +2.26) and
b_age_joint straddles zero at 15 of 19 (-0.05 to +0.79, the +0.79 being 2020 alone).

## 4. The incumbent does NOT buy its DD leg — it pays for it
H4 FALSIFIED on all three panels. MaxDD, unbraked H = 1 vs the incumbent H = 126, 10 bps:
**U56 -18.18% -> -19.13% (-0.95 pp), B136 -20.06% -> -20.75% (-0.69 pp), SMALL -32.83% -> -36.53%
(-3.70 pp).** The queue's premise ("H = 126 is buying its DD leg IN SPITE OF its age effect") is refuted:
it is not buying the DD leg at all. What H = 126 buys is CAGR (+2.84 pp on U56) and Sharpe (+0.076).

## 5. What the hysteresis exception says the axis really is
F4 is the only family whose brake can STILL SELL A FALLING NAME — it drops a name the moment its rank
passes K_out, however long it has been held. It raises U56 position age 66.3 -> 147.1 days (2.2x) and cuts
turnover 10.80 -> 4.78x/yr, and its MaxDD gets 2.91 pp SHALLOWER. That single family falsifies AGE and
TURNOVER alike as laws. The reduced-form reading the record can defend is narrower than either: a brake
deepens the drawdown when it forces the book to HOLD A NAME THE SCREEN HAS ALREADY DROPPED (F1, F2, F3
all do); a brake that only delays the DECISION, while keeping the right to sell on a rank breach, does not.

## 6. Rule 8 (2017-2026 read ONCE) and the KEEP paths
- **4a: 0 of 660** published grid points. The base book is strictly deeper than the live band book.
- **4b: 100 of 660 FULL, 107 of 660 OOS, 95 of 660 both.** 85 of the 95 are U56, 10 B136, **0 SMALL**.
- Walk-forward: 48 chooser picks (3 panels x 4 families x 4 choosers), **12 clear 4b OOS**, all U56.
  Mean OOS Sharpe C_SHARPE 0.9019 > C_LIVE 0.8627 > C_AGE 0.8561 > C_TURN 0.8461 — i.e. **DIAL 2 loses to
  both the record's habitual chooser and to doing nothing.** Choosing the brake rung by either regression
  is worth less than not choosing at all.
- **One KEEP-4b candidate, rule-8 REACHABLE, recorded NOT RECOMMENDED**: U56, K_out = 50, @10 bps FULL
  11.69% / 1.0778 / -15.27% (halves 1.1489 / 1.0240), OOS 12.94% / 1.1303 / -15.27%, turnover 4.804x/yr.
  Picked on 2009-2016 alone by C_SHARPE, C_AGE and C_TURN. It is dominated by the incumbent it modifies
  (-4.09 pp CAGR, -0.075 Sharpe) and buys a DD leg that was never binding. See the MEMO.

## 7. A record-hygiene by-product
Idea 1484's in-source anchor constant `C_U56` (CAGR 0.1580 / Sharpe 1.1537 / oSharpe 1.1857) disagrees
with **1484's own committed grid row** (0.157836 / 1.152437 / 1.184488) by 1.3e-3 of Sharpe. This run
replays the GRID ROW to 3.8e-7 on its worst component (the residual is `data/prices.csv` being fully
re-cached on 2026-09-22, commit 85bb8c1, which restates adjusted closes).
A second one: **the min-hold CLOCK and a POSITION's age are different objects.** 1484's frame restarts a
name's H clock whenever the ranking re-takes it after it has aged out, so "H = 126" means "cannot be
dropped within 126 days of the last SELECTION event", not "held 126 days". Every age here is the POSITION
age, measured from the EXECUTED weights (gate G9).

## Caveats
Survivorship (rule 9): U56 / B136 are 2026 constituent lists carried back to 2008 and SMALL a current
sub-$2B screen, so every level is an upper bound; what is read here is a contrast across books built over
the same names on the same days. Flat costs, no spread/impact/borrow. MaxDD is a single-path extremum and
nothing in section 2 resolves at |t| > 2 under section 3's ruler. No leverage, no shorting, t+1, one K_in.

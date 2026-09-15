# Idea 769 — why is the DRIFT FLOOR 8x larger under RESPREAD than DEGROSS?
Lane C, 2026-09-15. Script `2026-09-15_why-is-the-DRIFT-FLOOR-8x-larger-under-RESPREAD-than-DEGROSS_C.py`.

**ANSWERED — THE 8x IS REAL AND THE PUBLISHED REASON IS HALF OF IT. The floor is BILINEAR in the
per-name target AND the book exposure, not a denominator fact; and its LEVEL does not walk
forward. KILL for capital (4a 21/720, 4b 30/720, BOTH 0/720; 0 of 9 rule-8 IS selectors reach a
4b pass on the OOS window). Nothing promoted; RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py untouched.**

## Setup
2 tuned params, the queue's own: **CONSTRUCTION {RESPREAD, DEGROSS} × k/n q {0.10, 0.20, 0.30,
0.50, 0.70, 0.90}**. Reported axes, never selected over: panel {U56 55, B136 135, SMALL 663},
cadence {D, W, M, Q}, arm {MA-DIST, MOM}, handling {DRIFT, RTT}, theta {+0.06, 0.00, −0.12}
(the GATE family, idea 562's own setting), cost rung {0, 10, 25}. Gross pinned at the live 0.75,
10 bps, next-day execution. IS = start..2016-12-31, OOS = 2017-01-01..end, read once.
**720 books priced; 180 arm-pair drift cells.**

The FIXK arm pair selects **exactly** k_t = round(q·n_t) names in both arms, so every shared
name carries an identical target and the depth-match residual idea 562 had to carry is **zero
by construction** — gate G3, max |MRES_pp| = 0.000e+00 (GATE family, for contrast: 0.0033).

Gates: **G0** run() vs engine.backtest 0.000e+00 · **G1** derived cost rungs 0.000e+00 ·
**G2** DRIFT ≡ 0 at cadence D 0.000e+00 · **G3** MRES ≡ 0 in FIXK 0.000e+00. **4 of 4 PASS.**

## 1. The 8x reproduces
| floor = max |DRIFT_pp| over q and {W,M,Q} | RESPREAD | DEGROSS | ratio |
|---|---|---|---|
| U56 | 0.10767 | 0.00888 | 0.0825 |
| B136 | 0.19134 | 0.00779 | 0.0407 |
| SMALL | 0.03874 | 0.01080 | 0.2787 |
| **FIXK pooled** | **0.19134** | **0.01080** | **0.0564** |
| GATE family (562's own setting) | 0.06171 | 0.01631 | 0.2643 |
| idea 562 published | 0.13740 | 0.01640 | 0.1194 |

## 2. The reason is NOT the shared denominator
Two readings were pre-registered before any number was read. Along the q ladder they predict
opposite shapes, because at a single k/n the target size w and the book exposure E move
together and cannot be told apart.

| slope of log|DRIFT| on log q (median over 3 panels × {W,M,Q}) | measured | H_DENOM | H_EXPO | H_BILINEAR |
|---|---|---|---|---|
| RESPREAD | **−0.6609** | −1 | 0 | −1 |
| DEGROSS | **+1.1072** | 0 | +1 | +1 |
| total abs error | — | 1.4463 | 0.7681 | **0.4463** |

**H_DENOM is rejected on its own test.** H_BILINEAR was written down *after* the two
pre-registered readings were scored and is flagged post-hoc throughout, but it is
parameter-free, not fitted: one bar after a rebalance a shared name held at the same target w
by both arms satisfies h_A − h_B = w(1+r_j)(1/tot_A − 1/tot_B) with tot_X = 1 + E_X·rp_X, so
tot_A − tot_B is first order in the exposure E. Hence |DRIFT| ~ w·E, giving slopes −1 / +1 and
a construction gap of **(k/n)²**. It is scored on the same unchanged grid — no new tuning, no
new axis.

**The (k/n) exponent, measured per cell as β = log(raw ratio)/log(k/n):
median 1.9293, IQR [1.8518, 2.0902].** H_DENOM needs β = 1 (miss 0.9293); H_BILINEAR needs
β = 2 (**miss 0.0707**). Normalising by w alone leaves a median residual ratio of 0.4960, so
H_COLLAPSE fails: the floor is not one number in target-weight units either.

Pooled law log|DRIFT_pp| = a + b1·log w + b2·log k: **b1 +1.6731 (se 0.1819), b2 +1.4153
(se 0.1811), R² 0.4473** (per-panel b1 1.89–2.00). Identification caveat printed in full:
inside RESPREAD w ≡ gross/k, so ρ(log w, log k) = −1.0000 there and b1/b2 are separated only
by the DEGROSS cells and the panel spread.

## 3. Rule 8 on the claim — the floor LEVEL does not walk forward
IS fit (2009–2016 only): b1 +1.4382, b2 +1.2776, R² 0.3321. Applied untouched to 2017–2026:
**OOS R² 0.3703, median pred/act 0.6000 — the IS law under-predicts the OOS floor by 40%.**
Floor levels: RESPREAD **0.18079 IS → 0.32775 OOS (1.81×)**, DEGROSS 0.01103 → 0.02253.
The **construction RATIO** is the portable part: 0.0610 IS vs 0.0687 OOS.
So a published floor must name its window; a published construction ratio need not.

## 4. Rule 8 on the books — KILL
Three IS-only selectors, all declared before the OOS window was read (SEL-SHARPE, SEL-CALMAR,
SEL-DDCAP = highest IS Sharpe among cells inside the 4b DD cap measured on IS data alone).

| panel | selector | pick | OOS CAGR / Sharpe / MaxDD | 4a | 4b (full) | 4b (OOS window) |
|---|---|---|---|---|---|---|
| U56 | SEL-SHARPE | RESPREAD q0.10 Q MA-DIST | 22.98% / 1.0142 / −33.02% | FAIL | FAIL (DD) | FAIL (DD) |
| U56 | SEL-CALMAR | RESPREAD q0.10 M MA-DIST | 26.73% / 1.1881 / −28.90% | FAIL | FAIL (DD) | FAIL (DD) |
| U56 | SEL-DDCAP | DEGROSS q0.10 Q MA-DIST | 2.31% / 0.9481 / −3.90% | FAIL | FAIL (CAGR) | FAIL (CAGR) |
| B136 | SEL-SHARPE | DEGROSS q0.10 Q MA-DIST | 1.81% / 0.9339 / −2.89% | FAIL | FAIL (CAGR) | FAIL (CAGR) |
| B136 | SEL-CALMAR | RESPREAD q0.10 W MA-DIST | 17.09% / 0.9696 / −21.68% | FAIL | FAIL (DD) | FAIL (DD) |
| B136 | SEL-DDCAP | DEGROSS q0.10 Q MA-DIST | 1.81% / 0.9339 / −2.89% | FAIL | FAIL (CAGR) | FAIL (CAGR) |
| SMALL | SEL-SHARPE | RESPREAD q0.70 M MOM | 8.07% / 0.5603 / −35.25% | FAIL | FAIL (H2,OOS,DD,CAGR) | FAIL (OOS,DD,CAGR) |
| SMALL | SEL-CALMAR | RESPREAD q0.50 M MA-DIST | 8.66% / 0.6087 / −36.72% | FAIL | FAIL (H1,H2,OOS,DD,CAGR) | FAIL (OOS,DD,CAGR) |
| SMALL | SEL-DDCAP | DEGROSS q0.50 M MOM | 4.41% / 0.5737 / −18.61% | FAIL | FAIL (H2,OOS,CAGR) | FAIL (OOS,CAGR) |

Comparands OOS — SPY 15.27–15.33% / 0.874–0.877 / −33.72%; RULES v2 9.49% / 1.286 / −11.90%
(U56), 7.88% / 1.108 / −12.18% (B136), 3.75% / 0.559 / −13.89% (SMALL).

**0 of 9 (panel × selector) cells reach 4b on the OOS window**, and the reason is the same on
every one: the DD cap and the CAGR floor bind on opposite sides of the q axis. Of the 576 FIXK
books, **200 fail on DD alone and 156 on CAGR alone** — every selector that clears the CAGR
floor blows the DD cap, and every selector that clears the DD cap (all three SEL-DDCAP picks go
to DEGROSS q≤0.50) starves the CAGR floor.

Full-sample counts across all 720 books: **4a 21, 4b 30, BOTH 0**. The 30 full-sample 4b passes
are **26 U56** (20 FIXK — RESPREAD q∈{0.50,0.70} and DEGROSS q=0.90 — plus 6 GATE) and
**4 B136 GATE**; none is reachable by any IS-only selector. Cost rungs, FIXK: 4a **62 / 17 / 1**
and 4b **23 / 20 / 18** at 0 / 10 / 25 bps.

**Drift is worth nothing as capital**, confirming 562 on the book side: DRIFT − RTT median
Sharpe **+0.0000** over 288 matched cells, DRIFT > RTT in 33.0% of them.

## What this changes in the record
Idea 562's `RESPREAD 0.1374 / DEGROSS 0.0164` should not be quoted as two constants with a
denominator story. The floor is a **surface**, |DRIFT| ≈ C · w · E, whose construction gap is
(k/n)² and whose level moves 1.81× between the two windows. Any committed pp-leg compared
against "the drift floor" needs the floor re-read at that leg's own (w, E, window), not at
562's headline pair.

## Caveats
SURVIVORSHIP: B136 and SMALL are current constituents only; dead names are absent and CAGR
levels are inflated. DRIFT_pp is an arm-minus-arm quantity inside one panel at identical depth,
where the bias very largely cancels; the 4a/4b columns and the rule-8 levels are **not**
protected. H_BILINEAR is post-hoc (section 2); its β = 2 prediction is parameter-free and was
tested on the unchanged pre-registered grid, but it was not the hypothesis this run set out to
test. The law's R² is 0.4473 pooled — the (w, k) surface explains under half the log variance,
and the residual is cadence- and panel-specific.

# Idea 117 — crisis-depth-as-the-price-denominator (lane B, 2026-09-05)

**Verdict: PREMISE CONFIRMED on the large-cap panels, REFUTED on the small panel; the
episode-level replacement PASSES its pre-registered portability bar and is proposed to
PROTOCOL as a reporting clause. No new book KEEP (4a or 4b) — this is a measurement run.**

Script `2026-09-05_crisis-depth-as-the-price-denominator_B.py`, console
`.console.txt`, data `.grid.csv` (306 arm-points), `.pricelist.csv` (288),
`.episodes.csv` (29 panel-theta episodes), `.epprice.csv` (7,776 arm-episode prices),
`.stability.csv`, `.regime.csv`, `.walkforward.csv`.

## Harness verification (run before anything was read)

Idea 94's module is imported, not re-implemented. `engine.backtest` equivalence of the
control is `max|diff| = 0.000e+00` (EXACT). Idea 94's published `EWall+vol60-dg` u56 @10 bps
row reproduces to the decimal (11.6% / 1.133 / -16.9%). **Idea 97's published headline
reproduces exactly**: u56 median T1_gate tier price **4.108 IS / 0.404 OOS** against levers
**1.002 / 0.616**. Every number below is therefore on the same simulator as the citation it
audits.

## Episodes (idea 62's classification, built here — idea 62 is still Open)

SPY drawdown episodes on the u56/broad slice at theta = 10% (9 of them; the small panel starts
2011 and has 7):

| eid | peak | trough | recovery | depth pp | peak→trough d | speed | bin | window |
|---|---|---|---|---|---|---|---|---|
| E1 | 2009-01-28 | 2009-03-09 | 2009-04-17 | 22.06 | 27 | FAST | DEEP | IS |
| E2 | 2010-04-23 | 2010-07-02 | 2010-11-04 | 15.70 | 49 | FAST | SHALLOW | IS |
| E3 | 2011-04-29 | 2011-10-03 | 2012-02-03 | 18.61 | 108 | SLOW | SHALLOW | IS |
| E4 | 2015-07-20 | 2016-02-11 | 2016-04-18 | 13.02 | 143 | SLOW | SHALLOW | IS |
| E5 | 2018-01-26 | 2018-02-08 | 2018-08-06 | 10.10 | 9 | FAST | SHALLOW | OOS |
| E6 | 2018-09-20 | 2018-12-24 | 2019-04-12 | 19.35 | 65 | SLOW | SHALLOW | OOS |
| E7 | 2020-02-19 | 2020-03-23 | 2020-08-10 | 33.72 | 23 | FAST | DEEP | OOS |
| E8 | 2022-01-03 | 2022-10-12 | 2023-12-13 | 24.50 | 195 | SLOW | DEEP | OOS |
| E9 | 2025-02-19 | 2025-04-08 | 2025-06-26 | 18.76 | 34 | FAST | SHALLOW | OOS |

The IS window's -22.06% "worst crisis" is **E1, a 27-day fragment of the GFC that the
evaluation slice (from 2009-01-13) merely clips**; the OOS window holds two genuine >20%
crises. The IS/OOS asymmetry rule 8 imposes is therefore not 1 crisis vs 1 crisis, it is
**1 clipped crash + 3 shallow episodes vs 2 deep + 3 shallow** (idea 111's year-composition
finding, restated on the episode axis).

theta sensitivity (tuned parameter 1, all points reported): 8% → 13 episodes, 10% → 9,
15% → 7; median arm-episode protection +0.065 / +0.250 / +0.413 pp; median episode price
1.205 / 0.825 / 0.730. No conclusion below changes sign across the three.

## P1 — the whole-window price IS a regime reading (CONFIRMED on large caps, not on small)

Regressing log(median whole-window price of a cell) on log(that window's SPY MaxDD), pooled
over 3 panels x 3 books x 2 costs x 3 windows = 54 points:

| scope | slope | t | R² |
|---|---|---|---|
| ALL | **-1.577** | -2.58 | 0.114 |
| u56 | **-4.035** | -5.78 | 0.676 |
| broad | **-3.052** | -3.35 | 0.412 |
| small | +0.127 | +0.12 | 0.001 |

Median IS/OOS price ratio across the 18 cells is **2.18x** (min 0.03x, max 13.05x); idea 97's
published pair is 10.2x, i.e. the citation is near the top of the distribution, not typical.

**Honest limit on P1:** each panel supplies only TWO distinct depths (its IS depth and its OOS
depth — `full` shares the OOS depth), so these slopes are a re-expression of the IS-vs-OOS
contrast, not an elasticity estimated over 54 independent depths. The t-statistics are
inflated by that. P3 below is the version of the same claim with real variation in x.
**And the small panel refutes P1 outright**: there the whole-window price is just as unstable
(P2) but the instability does not track depth at all.

## P2 — the depth-matched episode price is 2.5x more portable across windows (CONFIRMED)

Median |log10(IS price / OOS price)| per arm (0.30 = a 2x swing, 1.00 = 10x):

| scope | whole-window | episode (all) | episode (depth-matched) |
|---|---|---|---|
| ALL | 0.455 | 0.209 | **0.184** |
| u56 | 0.752 | 0.348 | 0.334 |
| broad | 0.337 | 0.170 | 0.137 |
| small | 0.422 | 0.170 | 0.123 |

Pre-registered bar (ep_match ≤ whole/2 on ALL): **0.184 vs 0.227 — CONFIRMED**. Paired on the
109 arms where both are defined, the depth-matched price is more portable in **92/109**
(sign-test z = +7.18); by panel 36/42 u56, 30/33 broad, 26/34 small. Paired medians 0.455 →
0.175.

**The decisive number.** The exact object idea 97 published — the u56 gate tier — priced at
4.108 IS / 0.404 OOS, a **10.2x** swing. Priced per crisis at matched depth it is:

| u56 T1_gate | IS | OOS | IS/OOS |
|---|---|---|---|
| DEEP episodes | 0.240 | 0.257 | **0.93x** |
| SHALLOW episodes | 1.085 | 0.808 | **1.34x** |

Pooled over all panels/books/costs: DEEP 0.298 IS / 0.476 OOS, SHALLOW 1.288 IS / 1.116 OOS.
**The entire 10x IS/OOS gap in the published price is a depth-mix effect.** Within a depth
bin the price barely moves between windows.

## P3 — the mechanism: protection scales with crisis depth (CONFIRMED)

Pooled OLS of protect(e) (pp of drawdown the arm saved inside episode e) on the episode's SPY
depth, 2,400 arm-episodes at theta 10%:

| tier | slope (pp per pp) | t | R² | n |
|---|---|---|---|---|
| ALL | **+0.1608** | +15.07 | 0.087 | 2400 |
| T1_gate | +0.1785 | +12.43 | 0.093 | 1500 |
| T3_ddctl | **+0.3199** | +11.60 | 0.311 | 300 |
| T4_stop | +0.0116 | **+1.46** | 0.007 | 300 |
| X_ebud | +0.0624 | +2.61 | 0.022 | 300 |

So a whole-window MaxDD denominator is, to first order, **a depth in disguise multiplied by a
tier-specific coefficient** — which is exactly why dividing by it makes every instrument look
dear in a shallow window. Two by-products worth their own line:

* **The per-name trailing stop does not scale with depth at all** (t +1.46). It delivers the
  same negligible protection in a -33.7% crash as in a -10% wobble. This is a stronger and
  more mechanical version of idea 94/97's "the stop is the dearest tier": it is not merely
  expensive, it is **non-responsive to the thing it is supposed to insure**.
* **The book-level DD control has the steepest depth response (+0.32, R² 0.31)**, i.e. it is
  the instrument whose apparent price moves most with the window's regime — the direct
  mechanism behind idea 118's open question about why it looks cheap where drawdowns are deep.

Cheapest-looking crises are the deep fast ones (E7 2020: median price 0.368-0.406 across
panels); the dearest is **E5 (2018-02, -10.1% in 9 trading days), which prices at 9.150 on u56
and 7.604 on broad**. A price quoted without its episode's depth is uninterpretable by a
factor of ~25.

## Rule 8 walk-forward — P4: the episode price is a better DESCRIPTION, not a better SELECTOR

Parameters chosen on IS only (u56/broad 2009-2016, small 2010-2016), evaluated untouched on
2017-2026. `S1` = idea 94's argmin IS whole-window rate; `Sdepth` = argmin IS depth-matched
episode price (median over IS SHALLOW episodes), both gated at ≥1.0 pp of IS protection.

| | mean OOS regret | median | rank-1 | OOS CAGR | OOS Sharpe | OOS MaxDD | 4a | 4b |
|---|---|---|---|---|---|---|---|---|
| S1 | **+0.337** | +0.116 | 8/18 | 8.22% | 0.729 | -21.25% | 5/18 | 4/18 |
| Sdepth | +0.425 | +0.415 | 4/18 | 7.38% | 0.713 | **-19.52%** | **10/18** | 3/18 |
| control | — | — | — | 10.65% | 0.762 | -27.39% | — | — |
| RULES v1 | — | — | — | 4.86% | 0.451 | — | — | — |
| SPY | — | — | — | 15.45% | 0.882 | -33.72% | — | — |

The two selectors agree in 8/18 cells. **Sdepth does NOT beat S1** (regret +0.088 worse, mean
dOOS Sharpe -0.016) — P4 confirmed. The one signed difference is that Sdepth systematically
buys more drawdown for less return (OOS MaxDD -19.5% vs -21.3%, CAGR 7.4% vs 8.2%, 4a passes
10/18 vs 5/18), which is what a criterion built on protection-per-crisis should do, and is a
worse trade under 4b's CAGR floor. **Do not adopt the episode price as a selector.**

Both selectors land far below SPY OOS (0.729 / 0.713 vs 0.882) and above live RULES v1
(0.451). Best single OOS cell is `u56/EWall/band3-rw` at 0.134 CAGR / 1.203 Sharpe / -17.7%
(S1) and `band3-dg` at 0.095 / 1.285 / -12.1% (Sdepth).

## KEEP paths (PROTOCOL rule 4) — P5 confirmed, no new candidate

Every arm evaluated on both paths at both cost rungs, all reported in `.grid.csv`.

* **4b @10 bps:** u56 10 arms (`abs12-rw, band3-dg, band3-rw, ddctl-8/.5/recover, g200-dg,
  g200-rw, v1gate-dg, v1gate-rw, vol60-dg, vol60-rw`), broad 4 (`band3-rw, g200-rw, v1gate-rw,
  vol60-dg`), **small 0**. @25 bps: u56 6, broad 2, small 0.
* **Arms passing 4b on all three panels: none.** P5 confirmed. Idea 94's published
  cross-universe pair (`band3-rw`, `vol60-dg`) is reproduced and is still the only pair that
  survives both large panels at both rungs.
* **4a @10 bps:** u56 3, broad 11, small 12 — including the small-panel *control*, the known
  4a pathology (ideas 22/40/94/97): live RULES v1 is so weak on small caps (OOS Sharpe 0.581)
  that beating it is not evidence of anything.
* Binding 4b constraint @10 bps across the 306 rows: the drawdown cap alone in 27 cases, the
  CAGR floor alone in 14, everything at once in 42.

## Recommendation to the Sunday review (no file modified)

Amend PROTOCOL rule 4 with one sentence, in addition to idea 97's pending amendment:

> Any drawdown price (pp of CAGR per pp of MaxDD) must be quoted **per crisis episode at a
> stated depth** — the episodes of the window, classified by SPY peak-to-trough depth with a
> 20 pp SHALLOW/DEEP boundary — with the premium measured on calm days only. A price whose
> denominator is a whole-window MaxDD may not be compared across windows or panels, because
> the denominator is the window's worst crash, not a property of the instrument.

And add one falsifiable clause to the price list itself, which this run establishes with
real variation in the regressor: **the per-name trailing stop's protection does not scale
with crisis depth (slope +0.012, t +1.46) while every other tier's does** (gate +0.179,
DD control +0.320).

Do **not** adopt the episode price as a walk-forward selector (P4).

## Caveats

* Survivorship on all three current-constituent panels (idea 54), worst on small, in the
  direction that flatters gates. Every number here is a within-cell same-days delta, but no
  absolute CAGR should be quoted.
* P1's slopes rest on two distinct depths per panel; P3 is the version with real x-variation.
* The small panel refutes P1 and yet shows the largest P2 improvement — the whole-window
  price is unstable there for reasons other than depth mix, which is unexplained and belongs
  with open idea 118.
* Calm-day annualisation compounds a non-contiguous day subset at 252 d/yr; it is a premium
  proxy, not a tradeable return.
* 29 panel-theta episodes and 9 at the point value is a small sample; only P3 (n=2,400
  arm-episodes) and P2's sign test (92/109) have real margin.
* Calendar-day index (open idea 38) unfixed for u56/broad; the small panel is trading-day
  indexed, so its episode list is shorter and starts in 2011.

# Idea 312 — is-the-panel-ordering-an-ETF-SHARE-effect (lane B, 2026-09-09)

**ANSWERED / KILL of the ETF-share reading — and the panel ordering itself does not survive
the noise floor this test exposes.** ETF share does not carry idea 51's `U56 > B136 >
SMALL439` gate premium; inside B136 the premium's slope in ETF share runs the **wrong way**
(−0.0641 per unit s, so an all-ETF panel gates *worse*), the slope's sign **flips** between IS
and OOS, and **39.4% of same-ETF-share 36-name draws differ from each other by more than the
whole published three-panel gap**. No RULES change, no book promoted, no KEEP claimed;
RULES.md, PROTOCOL.md, products/scan.py, products/bot/bot.py and research/baseline.py
untouched.

Script: `2026-09-09_is-the-panel-ordering-an-ETF-SHARE-effect_B.py` · 10 bps, t+1 fills, no
leverage, no shorting · 840 books · runtime 62 s · outputs `.console.txt` `.grid.csv`
`.ladder.csv` `.noisefloor.csv` `.predict.csv` `.chars.csv` `.walkforward.csv` `.keeppaths.csv`

## Design

Treatment is idea 51's premium verbatim: `Sharpe(MA-RS) − Sharpe(EWall)` at matched
(gross, cadence), both arms equal-weight, RESPREAD so gross is pinned and the premium is pure
selection. Panels are **k-matched draws of 36 names from B136** (panel width never varies),
`n_etf = round(s·36)`, six seeds per rung, drawn with idea 291's committed crc32 scheme so the
ALL36 panels are the same objects as that run's. Tuned parameters (rule 4, exactly two):
**ETF share s** and **cadence {W, M}**; gross {0.50, 0.75, 1.00} is a reported axis (max
premium range across the three gross rungs: **0.0046**), seed is replication, ETF pool
flavour is a reported contrast. All 840 grid points are in `.grid.csv`.

## Gates, both PASS

| gate | result |
|---|---|
| **G1 reproduction** — idea 51's committed `.grid.csv`, 36 rows × 13 columns | **B136 8.88e-16, SMALL439 1.28e-15**; U56 1.22e-05 |
| **G2 identity** — vectorised runner vs `engine.backtest` | **1.388e-17** |
| published premium re-read | U56 **−0.0045**, B136 **−0.0465**, SMALL439 **−0.1023**; gap **+0.0978** (pre-registered 0.0978) |

U56's 1.2e-05 is a **data revision, not a code difference**: `data/prices.csv` was rewritten
between the two runs — against commit `e02949d`'s copy every shared bar moved by ≤ **5.09e-05
relative** (AVGO 5.1e-5, NVDA 4.1e-5, AAPL 3.5e-5 — an adjusted-close back-revision) and one
bar was appended (2026-09-08). `prices_broad.csv` and `prices_small.csv.gz` are unchanged,
which is why the other two panels gate at 1e-15. All panels are truncated to idea 51's last
bar (2026-09-04) so the comparison is on idea 51's own sample.

## The ladder — premium by ETF share, all 6 (gross, cadence) points averaged

| s (ETF share) | ALL36 | EQ24 | NONEQ12 |
|---|---|---|---|
| 0.000 | **−0.0820** | (shared) | (shared) |
| 0.125 | — | −0.1309 | −0.0991 |
| 0.250 | −0.0754 | −0.0811 | −0.0663 |
| 0.333 | — | — | −0.0658 |
| 0.500 | −0.1126 | −0.1721 | — |
| 0.667 | — | −0.0759 | — |
| 0.750 | −0.0701 | — | — |
| 1.000 | **−0.1648** | — | — |

**H_ETF FALSE.** The ALL36 ladder is neither monotone nor positively sloped: spread
**−0.0828 = −0.85 × GAP**, i.e. it moves by nearly the size of the published panel gap and in
the *opposite direction*. Fit: `premium = −0.0689 − 0.0641·s`, R² 0.416.
**H_FLAT FALSE too** — this is not "ETF share does nothing", it is "ETF share runs backwards".

**H_PRED FALSE.** Evaluating the ALL36 fit at the real panels' own shares:

| panel | ETF share | predicted | actual | residual |
|---|---|---|---|---|
| U56 | 0.643 | −0.1102 | **−0.0045** | +0.1057 |
| B136 | 0.265 | −0.0859 | −0.0465 | +0.0394 |
| SMALL439 | 0.000 | −0.0689 | **−0.1023** | −0.0333 |

The ladder predicts the ordering **reversed** and explains **−42.2%** of the published gap.

**H_CLASS FALSE.** Within the ETF family the slope is not an equity-wrapper fact: EQ24 is
essentially flat (−0.0206, R² 0.018) and **NONEQ12 (bonds/FX/commodities) is the only pool
with a positive slope** (+0.0717, R² 0.439) — the opposite sign to pooled ALL36, whose
negative slope leans on the single s = 1.000 panel (ETF36, no seed variation there).

## The noise floor (POST-HOC — forced by the seed sd, not pre-registered)

Premium per (rung, seed), averaged over the 6 (gross, cadence) points:

| flavour | s | range across 6 seeds | seed sd | same-s pairs differing by ≥ GAP |
|---|---|---|---|---|
| ALL36 | 0.000 | 0.2781 | 0.1024 | 8 / 15 |
| ALL36 | 0.250 | 0.1465 | 0.0622 | 5 / 15 |
| ALL36 | 0.500 | 0.2164 | 0.0753 | 6 / 15 |
| ALL36 | 0.750 | 0.1320 | 0.0431 | 1 / 15 |
| EQ24 | 0.500 | 0.3231 | 0.1095 | 8 / 15 |
| NONEQ12 | 0.333 | 0.1562 | 0.0676 | 7 / 15 |

**65 of 165 same-ETF-share seed pairs (39.4%) differ by more than the entire published
three-panel GAP of 0.0978.** Mean within-rung seed sd is **0.0745 = 0.76 × GAP**; the standard
error of a 6-seed rung mean is 0.0304. A single 36-name draw's composition luck reproduces
the published ordering four times in ten. Idea 51's three panels are three draws.

## Rule 8 walk-forward (IS ≤ 2016-12-31, OOS ≥ 2017-01-01, read once)

**WF-A — the answer itself.** Refit the premium~s slope inside each window:

| window | s=0.00 | 0.25 | 0.50 | 0.75 | 1.00 | slope | R² |
|---|---|---|---|---|---|---|---|
| FULL | −0.0820 | −0.0754 | −0.1126 | −0.0701 | −0.1648 | −0.0641 | 0.416 |
| IS | −0.1508 | −0.1142 | −0.1472 | −0.0703 | −0.1263 | **+0.0372** | 0.205 |
| OOS | −0.0251 | −0.0474 | −0.0879 | −0.0690 | −0.1968 | **−0.1461** | 0.750 |

The slope's **sign flips** IS → OOS and its magnitude changes 3.9×. Even the backwards
relationship is not a stable fact — ETF share is not an instrument for this premium in either
direction.

**WF-B — a book.** (s, cadence) chosen by IS Sharpe of the seed-pooled MA-RS book at g = 0.75
(picks s = 0.250, M), read OOS once:

| book | CAGR | Sharpe | MaxDD | H1/H2 | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|---|
| WF-B pick, MA-RS s=0.25/M | 13.15% | 1.125 | −21.27% | 1.223/1.047 | 13.78% | **1.135** | −21.27% |
| same pick, EWall control | 14.87% | 1.149 | −25.48% | 1.249/1.059 | 14.84% | **1.142** | −25.48% |
| RULES v2 (live, B136) | 8.03% | 1.106 | −12.24% | 1.229/0.984 | 7.98% | 1.119 | −12.24% |
| RULES v1 (B136) | 6.39% | 0.635 | −21.19% | 0.756/0.532 | 5.94% | 0.576 | −21.19% |
| SPY | 15.23% | 0.889 | −33.72% | 0.957/0.834 | 15.45% | 0.882 | −33.72% |

The IS-chosen gated book beats SPY and RULES v2 OOS — and still **loses to its own ungated
control** (1.135 vs 1.142) on Sharpe, CAGR and every half. The gate is a cost, OOS included.

## Both KEEP paths — all 840 books

**4a: 0 / 840. 4b: 56 / 840** (MIX 24 EWall + 29 MA-RS; REAL 3, all U56/B136 MA-RS rows
already in the record). 4b binding legs: DD 508, CAGR 331, H1 181, H2 117, OOS 93. **None is
a capital candidate**: a MIX panel is a seeded random 36-name draw of current B136
constituents, not a rule anyone can trade, and 24 of the 53 MIX passers are the *ungated*
control. No memo is filed.

## What does move with composition (reported covariates, not instruments)

| | cvol | rho | breadth | beta |
|---|---|---|---|---|
| ALL36 s=0.00 → s=1.00 | 0.307 → 0.210 | 0.359 → 0.344 | 0.692 → 0.674 | 1.028 → 0.710 |
| U56 (real) | 0.265 | 0.333 | 0.686 | 0.856 |
| B136 (real) | 0.282 | 0.339 | 0.686 | 0.927 |
| SMALL439 (real) | **0.562** | **0.176** | **0.475** | 1.068 |

Univariate fits over the 12 rungs are all weak (best R² 0.130, rho). The point the table makes
is about **support**: every B136 sub-panel lives at cvol 0.21–0.31 and breadth 0.67–0.71, while
SMALL439 sits at 0.562 and 0.475 — far outside anything a re-composition of B136 can reach.
The panel that anchors the published ordering's low end cannot be reproduced by ETF share, by
this design or any other drawn from B136.

## Survivorship, stated

`universe_broad.json` is CURRENT constituents, so the stock end of every ladder carries a
survivorship premium the ETF end structurally cannot. That bias inflates the stock end's
CAGR *level*; the premium is an arm-minus-arm difference on the same panel, so it very largely
cancels there. It does not touch the noise-floor result, which is a within-rung dispersion.

## For the queue

Two things follow. (1) The record should stop reading the three-panel premium ordering as a
*property* of anything — cap, asset class or otherwise — until a design with more than three
draws per level is run: at 0.0745 seed sd against a 0.0978 gap, three panels cannot separate a
panel property from composition luck, and this run's own ladder shows same-s draws crossing
that gap 39.4% of the time. (2) Every published claim of the form "characteristic X orders the
panels" that rests on the same three panels inherits the same defect and is worth a census.

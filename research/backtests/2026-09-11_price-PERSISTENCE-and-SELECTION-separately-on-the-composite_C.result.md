# Idea 679 — price PERSISTENCE and SELECTION separately on the composite (lane C, 2026-09-11)

**VERDICT: ANSWERED — PERSISTENCE carries it, and the answer puts a BASE-RATE CLAUSE on the
standing 2026-09-04 KEEP-4b candidate. KILL for capital: 4a 0/21, 4b 3/21, BOTH 0/21, no new
book, no RULES change.**

Script `research/backtests/2026-09-11_price-PERSISTENCE-and-SELECTION-separately-on-the-composite_C.py`
· 3 panels × 7 holding periods × {RANKED, RMATCH(60 draws), RFREE(60 draws)} = 21 cells, 2,541
books, all reported · 10 bps binding, 0/25 bps a labelled appendix · PROTOCOL rules 2, 4, 5, 8, 9.

## The decomposition

Every book holds `min(20, n_elig)` names at a fixed 0.75/20 of NAV through the incumbent's own
gate (200d MA, vol20 < 0.60, composite, no vol scaler, weekly cadence). Held-name COUNT is
matched day by day, so daily GROSS is identical across books by construction (G4, 2.220e-16).

| book | which names | how long held |
|---|---|---|
| `RANKED(h)` | top-20 by composite | re-formed every h weeks; **h=1 IS the standing incumbent** |
| `RMATCH(h)` | random | replaces **exactly as many names as RANKED(h) did, on the same dates** |
| `RFREE(h)` | random | whole list re-drawn at every re-formation |

`SELECTION = RANKED − RMATCH` (which names, at matched turnover) ·
`PERSISTENCE = RMATCH − RFREE` (how long held, with no selection skill) ·
their sum is the composite's total edge over an equal-gross coin flip.

## GATES (6, pre-registered, printed before any new number was read) — ALL PASS

`G1` Panel.run == engine.backtest @10 bps **6.939e-18** · `G1b` the O(T·20) sparse engine every
book below uses == Panel.run **7.199e-16** · `G2` band_book(0.03,0.75) == rules_v2_weights
**0.000e+00** · `G3` RANKED(h=1) re-derives the 2026-09-04 KEEP-4b incumbent at **12.63% /
1.0903 / −18.31%** (published 2026-09-04 vintage 12.66% / 1.0921 / −18.31%, max|d| **1.777e-03**;
identical to idea 672's re-derivation on today's cache) · `G4` coin-flip daily gross == RANKED's
at every h **2.220e-16** · `G5` RMATCH churn shortfall (re-adds forced by an exhausted eligible
pool) **0.4303%** of target replacements · `G6` SMALL439 drops all 44 `max_1d_move >= 1.0`
tickers.

**Provenance:** RANKED(h=1) trades **9.6376×/yr** — idea 502's 9.64× to four figures. RFREE(h=1)
trades **37.19×/yr**, reproducing 502's over-traded RANDROT null (36.48×/yr) and its **0/60**
4b pass share. RMATCH(h=1) trades **9.679×/yr**: the turnover-matched null the record lacked.

## THE ANSWER — persistence, by a factor of four

Mean over the 21 cells at 10 bps:

| leg | dSharpe (mean) | median | >0 in | dCAGR | dOOS Sharpe |
|---|---|---|---|---|---|
| SELECTION (which names) | **+0.0211** | +0.0112 | 13/21 | +2.46% | +0.0222 |
| PERSISTENCE (how long) | **+0.0886** | +0.0237 | 16/21 | +1.16% | +0.0825 |
| TOTAL vs a free coin flip | +0.1097 | — | — | +3.62% | +0.1047 |

**PERSISTENCE carries 80.8% of the composite's Sharpe edge over an equal-gross coin flip and
78.8% of its OOS Sharpe edge.** SELECTION carries ~19%, and its sign flips by panel (U56
+0.0314, B136 **−0.0027**, SMALL439 +0.0345 mean dSharpe) while PERSISTENCE is positive on all
three (+0.0622 / +0.1069 / +0.0966). Selection is where the CAGR is (+2.46% vs +1.16%) — idea
504/672's "earns CAGR, no Sharpe" replicates a third time, now against a turnover-matched
control.

**The mechanism is cost, not return.** Coin-flip 4b pass shares, mean over all 21 cells:

| rung | RMATCH (slow churn) | RFREE (fast churn) |
|---|---|---|
| 0 bps | 0.232 | **0.249** |
| 10 bps | 0.132 | 0.044 |
| 25 bps | 0.035 | 0.001 |

At zero cost slow churn is worth nothing — the free coin flip is marginally *better*. The whole
persistence leg is saved transaction costs, exactly the reading idea 502 proposed.

## THE BASE-RATE CLAUSE — the standing KEEP-4b candidate sits inside its own matched null

The only 4b passes in the run are `U56 RANKED h=1, 2, 4` (the incumbent and its two neighbours).
At those same three cells the **turnover-matched coin flip clears 4b in 30%, 32% and 47% of 60
draws**, and the incumbent sits at its **80.0th / 76.7th / 81.7th Sharpe percentile**. On B136 the
shares are 32% / 47% / 52%. Idea 502's reassuring **0/1000 at 10 bps was a turnover artefact** of
a null that churned 3.9× too fast; matched to the candidate's own churn, roughly a third of
random 20-name books clear the bar. **The 2026-09-04 KEEP-4b candidate needs the base-rate clause
502 concluded it did not need.** (SMALL439 is the one clean panel: 0/21 RANKED and 0/840 coin-flip
4b passes.)

## PROTOCOL rule 8 — h chosen on 2009–2016 only, 2017–2026 read once

| panel | pick | OOS CAGR / Sharpe / MaxDD | SPY OOS | live v2 OOS | vs matched coin flip |
|---|---|---|---|---|---|
| U56 | h=4 | 15.14% / **1.168** / −20.14% | 15.24% / 0.872 / −33.72% | 9.45% / 1.275 | **+0.1396** |
| B136 | h=8 | 13.75% / **0.858** / −26.15% | 15.45% / 0.882 / −33.72% | 7.98% / 1.119 | **−0.0811** |
| SMALL439 | h=8 | 5.87% / **0.401** / −40.86% | 15.45% / 0.882 / −33.72% | 3.85% / 0.568 | **−0.0095** |

Selection beats its turnover-matched coin flip out of sample on **1 of 3 panels**; on B136 and
SMALL439 the coin flip wins. The chooser beats SPY's OOS Sharpe on U56 only, and beats the live
book on no panel. The blind-commit h=1 book scores 1.165 / 0.892 / 0.487 — the chooser buys
+0.003 on U56 and loses 0.034 and 0.086 on the other two.

## What this does NOT license

No book is promoted; RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are untouched.
Rule 6 keeps any wording change to the Sunday review. **PROPOSED for that review** (not applied):
PROTOCOL rule 4b gains *"a 4b pass must also be reported against a TURNOVER-MATCHED random-list
base rate on the same panel; a book inside the 90th percentile of that null is PARK, not KEEP"* —
which, on today's numbers, moves the 2026-09-04 candidate from KEEP to PARK.

## Survivorship (PROTOCOL 9)

B136 is today's constituents and SMALL439 the current sub-$2B screen only; every LEVEL on those
panels is biased upward and none is tradeable. U56 carries a milder form. Both legs reported here
are within-panel differences over the same names and days, so the bias largely differences out;
the 4b pass COUNTS, measured against SPY, do not enjoy that protection.

Artefacts: `.console.txt`, `.grid.csv` (189 rows), `.legs.csv` (21), `.walkforward.csv` (9),
`.draws.csv` (2,520 per-draw rows at 10 bps).

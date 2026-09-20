# Idea 906 (slug `does-the-k-over-n-OVERLAP-survive-a-POINT-IN-TIME-shaped-ADMISSION-HAIRCUT`) — lane B, 2026-09-20

**ANSWERED / SPLIT. The U56 k/n overlap SURVIVES the survivorship stress; the B136 arm is KILLED;
and the channel the record should have been worried about is BREADTH, not winners.**
Script `2026-09-20_kn-overlap-vs-admission-haircut_B.py`; 182 panel-cells x 8 books = **1,456 book-cells**
and 910 chooser-cells, all published in `.grid.csv` / `.walkforward.csv` / `.passrates.csv`.

## The construction
Admission is masked at the WEIGHTS level, never in the price history: a name not admitted on day t
cannot be held on day t, but its trailing windows (200d MA, vol20, the 3/6/12m composite) are
computed on its full series exactly as the live book does. That is point-in-time index membership,
and it leaves the admitted name set as the only moving part.

* **Tuned params (2):** `d` (annual drop rate) in {0.00, 0.05, 0.10, 0.20}; `kind` in
  {RANDOM, WINNERCUT, LOSERCUT}. WINNERCUT drops the highest full-sample total returns (the
  survivorship windfall — a deliberate look-ahead STRESS, not a rule), LOSERCUT the lowest,
  RANDOM is the neutral null. SPY is the benchmark and is never dropped.
* **Control axis (both arms always reported):** `SHRINK` — dropped names are gone, so breadth falls
  with d; `ROTATE` — a dropped name serves a ONE-YEAR exile and returns, so exactly one cohort is
  out at a time and breadth is flat in calendar time. RANDOM at the same d is then an exactly
  breadth-matched null for WINNERCUT.
* **Books:** MEMO_887's ratio-width ladder, r in {0.20,0.35,0.50,0.75} x gross in {0.75,1.00},
  monthly, 10 bps, t+1, cash never respread. Baseline: live RULES v2 on the SAME admitted panel,
  weekly. SPY buy-and-hold. 5 seeds per cell.

**GATES (all PASS).** (1) local `bt()` replays `engine.backtest`, max|d| **0.000e+00** at W and M.
(2) `v2_weights(adm=None)` is `baseline.rules_v2_weights` bit-for-bit, max|d| **0.000e+00**.
(3) MEMO_887 reproduces on today's tape: published 0.157 / 1.152 / -16.9% -> **0.1560 / 1.1483 /
-16.87%** (g=1.00) and 0.117 / 1.150 / -12.9% -> **0.1165 / 1.1468 / -12.92%** (g=0.75);
max |published - reproduced| **0.0037**, i.e. tape drift since 2026-09-14, construction verbatim.

## (A) THE ANSWER ON U56 — THE OVERLAP IS NOT AN EX-POST-WINNER FACT
At **matched breadth** the standing candidate (r = 0.35, g = 0.75) is flat in every cut kind through
d = 0.10, 5 of 5 seeds clearing 4b FULL **and** OOS in each:

| U56 ROTATE | CAGR | Sharpe | MaxDD | OOS Sharpe | 4b FULL+OOS |
|---|---|---|---|---|---|
| d = 0 (no haircut) | 11.65% | 1.1468 | -12.92% | 1.1291 | 1 / 1 |
| RANDOM d = 0.05 / 0.10 / 0.20 | 11.68 / 11.70 / 11.53% | 1.1404 / 1.1364 / 1.1108 | -12.97 / -13.02 / -14.71% | 1.1264 / 1.1708 / 1.0941 | 5/5, 5/5, 4/5 |
| **WINNERCUT** d = 0.05 / 0.10 / 0.20 | 10.88 / 10.73 / **9.73%** | 1.0923 / 1.0873 / 1.0176 | -12.82 / -12.78 / -14.78% | 1.0946 / 1.0856 / 1.0109 | 5/5, 5/5, **0/5** |
| LOSERCUT d = 0.05 / 0.10 / 0.20 | 11.64 / 12.24 / 12.78% | 1.1486 / 1.1464 / 1.0907 | -12.92 / -14.57 / -17.53% | 1.1388 / 1.1716 / 1.1160 | 5/5, 5/5, 5/5 |

(SPY full 15.12% / 0.8843 / -33.72%, bars DD -20.23% and CAGR 10.59%; SPY OOS 15.26% / 0.8737 /
-33.72%. Live RULES v2 on the uncut panel 8.62% / 1.2010 / -12.05%; seed sd in the table above is
<= 0.0046 of CAGR and <= 0.046 of Sharpe.)

Exiling the ex-post best names at 5% and 10% a year costs **0.06 of Sharpe and 0.9 pp of CAGR** and
changes no verdict. Only at a **20%/yr** winner exile does the g = 0.75 rung fall through the 4b
**CAGR floor** (9.73% against 10.59%) — and the g = 1.00 rung at the same cell still passes (12.99%).

## (B) IT IS NOT DIRECTIONAL — SO IT IS NOT SURVIVORSHIP, IT IS NAME-SET PERSISTENCE
Ladder-wide 4b FULL+OOS pass rate on U56 ROTATE at d = 0.20: RANDOM **0.625**, WINNERCUT **0.375**,
LOSERCUT **0.375**. Removing the best names and removing the worst names cost exactly the same.
What degrades the book at a high exile rate is that the SAME subset is persistently absent, not that
the absent subset won.

## (C) THE REAL FRAGILITY IS BREADTH, AND THE RECORD HAS NEVER PRICED IT
Rule-8 OOS 4b pass rate on U56, by chooser, pooled over all cut kinds and rates:

| chooser | d = 0 | ROTATE (breadth flat) | SHRINK (breadth falls) |
|---|---|---|---|
| C_SHARPE | 1.000 | 0.689 | 0.067 |
| C_CALMAR | 1.000 | 0.711 | 0.111 |
| C_4bIS | 1.000 | 0.844 | 0.178 |
| C_FROZEN (r=0.35, g=0.75) | 1.000 | **0.867** | 0.333 |
| C_LIVE (RULES v2, do nothing) | 0.000 | 0.111 | 0.289 |

SHRINK takes the admitted count 55 -> 39.9 -> 27.1 -> 15.3 and the ladder's 4b rate 0.750 -> 0.700 ->
0.475 -> 0.100 (RANDOM). The binding leg is the **DD cap** (pass share 0.875 -> 0.750 -> 0.575 ->
0.200) — the book's drawdown is bought with breadth, which is exactly the dial no committed 4b claim
in this record quotes.

## (D) B136 — KILL. THAT ARM OF THE OVERLAP IS WINNER-CARRIED
B136 clears 4b FULL+OOS at 0.125 of the ladder uncut. Breadth-matched, **WINNERCUT kills all of it:
0 of 120 book-cells at d = 0.05 / 0.10 / 0.20**, against RANDOM's 0.100 / 0.175 / 0.175 and LOSERCUT's
0.025 / 0.025 / 0.000 at identical admitted counts. No chooser reaches 4b OOS on more than 0.111 of
B136's ROTATE cells. Idea 887's cross-panel reading of the k/n overlap does not survive; the U56
reading does.

## (E) 4a — 2 of 1,456
Both are the same U56 SHRINK/RANDOM/d=0.05/seed 3 panel (r = 0.35 and 0.50 at g = 0.75), i.e. a
haircut that happened to hurt the baseline more than the book. Path 4a remains closed on this axis.

## WHAT THIS TEST CANNOT DO (stated up front)
A haircut can only REMOVE names the cached panel contains. It cannot ADD the constituents a true
point-in-time index held and later deleted, because those series are not in `data/`. So this bounds
the overlap's dependence on the ex-post WINNERS (tight: it survives 10%/yr winner exile) and says
nothing about the absence of the FAILED names — that direction still needs a point-in-time
constituent file, which is LOCAL/Actions work, not cloud. `universe.json` / `universe_broad.json`
remain CURRENT constituents, so every absolute level here is still optimistic.

## VERDICT
**ANSWERED. KEEP-candidate (path 4b) REAFFIRMED for MEMO_887's U56 cell under a survivorship stress
it had never faced, with one new fragility on the record; KILL for the B136 arm; and a new
BREADTH finding that belongs beside every 4b drawdown claim. Not a rules change (rule 6).**

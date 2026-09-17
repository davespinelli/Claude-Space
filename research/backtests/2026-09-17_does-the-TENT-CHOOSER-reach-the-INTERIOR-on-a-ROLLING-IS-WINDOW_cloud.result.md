# Idea 1161 (cloud lane, 2026-09-17) — does the TENT CHOOSER reach the INTERIOR on a ROLLING IS WINDOW?

**ANSWERED = YES, AND EMPHATICALLY: the interior pick is a property of the CHOOSER, not of
1154's one window. 361 of 368 rolling choices (98.1%) land in the interior.** The pick is
also deeply unstable (median move rate 0.833) and moving it is nearly free (median 1.18
bps/yr of drag), and — the one hypothesis this run got wrong — **the 4b OOS pass SURVIVES
re-choosing at 19 of 24 cells against the ladder's own base rate of 22 of 66.**

## Construction

Two tuned parameters and no more (PROTOCOL rule 4, the two the queue names):
`WINDOW {W504, W756, W1260, WEXP}` x `CADENCE {R6M, R1Y, R2Y}` = 12 cells per panel,
**24 in all, every one published** in `.cells.csv`. The gross RUNG is not a third
parameter — it is the object the chooser selects (1154's framing); all 33 rungs of both
panels are in `.grid.csv`. PANEL {U56, B136} is not a dial.

**COMMON SPAN, declared before any number.** A rolling chooser cannot choose until warm-up
plus one window exists, so all four windows would otherwise be scored on four different
tapes. Every cell, control and benchmark here is scored from bar `WARMUP + max(window) =
1520` (**2014-01-21 -> 2026-09-15, 3,186 bars**), and WEXP is given the same first choice
date, so the windows differ in LOOKBACK only and never in scored tape. **These figures are
therefore NOT comparable to 1154's full-tape ones** (which start at bar 260); 1154's own
numbers are replayed on 1154's own span in gate G8 and quoted from its file, never
re-derived.

Price vintage pinned at **2026-09-15** (idea 1160's defect, 1163 open on it); G2 published
both ways. Frozen at 1082/1094/1098/1102/1108/1110/1116/1117/1118/1150/1154's construction:
CAND20 legs, cap INF, max_vol 0.60, min hold 126, N=20, cadence W, 10 bps (rule 2), LAG 1,
warm-up 260, zero cash.

## Gates — 10 of 10 PASS, printed before any result number

| gate | what | value |
|---|---|---|
| G1 | fast runner == `engine.backtest` | 1.39e-17 |
| G2 | committed U56 W/H126/N=20 full-tape triple, PINNED (15.5793% / 1.1397 / -19.1276%) | 4.12e-05 |
| G2u | *the vintage, published not absorbed:* same gate UNPINNED | **1.62e-03, 39.4x, from ONE extra bar of 4,706** |
| G3 | SPY OOS triple, PINNED | 1.70e-04 |
| G4 | CROSS-RUN 1098/1102's committed U56 n=12 triple | 4.71e-05 |
| G5 | live RULES v2 full-tape MaxDD == committed -12.05% | 4.95e-05 |
| G6 | determinism (same cell twice) | 0.00e+00 |
| G7 | `cadence_mask` == `engine.rebalance_mask` (D/W/M/Q) | 0 bars |
| **G8** | **CROSS-RUN 1154's one-shot C_IS4B picks — 0.625 (U56) / 0.575 (B136)** | **0 of 2 mismatches** |
| G9 | time-varying-gross build with a CONSTANT vector == the scalar path | 0.00e+00 |
| G10 | the gross ladder nests the record's committed rungs | 0 missing |

G8 is the one that licenses the run: the object under test is replayed exactly, on 1154's
own IS window and span, before anything new is read.

## Hypotheses — 4 of 5 SUPPORTED, and the refutation is the finding

| hypothesis | bar | value | verdict |
|---|---|---|---|
| H_INTERIOR | interior share of all choices >= 0.75 | **0.9810** | SUPPORTED |
| H_STABLE | median move rate >= 0.50 (the pick is UNSTABLE) | **0.8333** | SUPPORTED |
| H_CHEAP | median added turnover < 0.50x NAV/yr | **0.1177** | SUPPORTED |
| H_OOSPASS | fewer than 12 of 24 cells clear 4b OOS | **19** | **REFUTED** |
| H_NOGAIN | median (rolling - K_FROZEN) Sharpe <= 0 | **-0.0245** | SUPPORTED |

## (Q1) The interior — the tent is the chooser's, not the window's

**361 of 368 choices (0.9810) are interior rungs.** All **7** endpoint picks are gross 1.000,
all on **B136**, all on the two shortest windows (W504/W756), and all clustered in
**2021-07 .. 2023-07** — a 2-3 year lookback ending in that stretch contains no drawdown
deep enough to make `M_DD` bind, so the tent degenerates into a monotone ramp. U56 picks the
interior at **184 of 184**. The tent shape 1154 found on one window is a structural property
of `min(M_S, M_DD, M_CAGR)` and survives every window and cadence tested.

Pick levels: median **0.5625 (U56)** and **0.5125 (B136)**, range 0.300 .. 1.000 — the
rolling chooser systematically **de-grosses** relative to the incumbent 0.750, and sits
somewhat below 1154's one-shot 0.625 / 0.575.

## (Q2) How often it moves, and what moving costs

**Move rate median 0.833, range 0.360 (WEXP/R6M) .. 1.000** — at the 2-year cadence every
single re-choice moves the pick on both panels. Mean absolute step **0.0685** of gross,
about 2.7 rungs. The peak of a tent sits where two noisy legs cross, which is the least
resolvable point on a ladder whose whole-span Sharpe spread is **0.0041 (U56: 1.1303..1.1344)
and 0.0082 (B136)**; the argmax wanders accordingly.

**It is nearly free.** Against the same cell with its gross frozen at its own median pick,
the moving adds a median of **0.118x NAV/yr of turnover = 1.18 bps/yr of drag** (range
-0.12 .. +6.04 bps/yr; the -0.12 cells trade *less* than the frozen comparand). Switching
gross trades only the cash leg, so instability is cheap here in a way it would not be on a
selection dial.

## (Q3) Does the 4b OOS pass survive re-choosing — and the honest reading

**Yes, and at better than the ladder's base rate: 19 of 24 rolling cells clear 4b OOS
against 22 of 66 ladder rungs (0.79 vs 0.33).** 4b full: 10 of 24 cells vs 13 of 66 rungs.
**4a is 0 of 24 and 0 of 66.**

By panel: U56 **10 of 12** cells clear 4b full and 4b OOS; B136 **0 of 12** full, **9 of 12**
OOS. But the mechanism is exposure, not skill, and this run states it plainly:

| U56, common span | CAGR | Sharpe | MaxDD | halves | OOS |
|---|---|---|---|---|---|
| K_FROZEN gross 0.750 | 15.80% | 1.1334 | -19.13% | 0.9215/1.3332 | 16.97% / 1.1644 |
| K_ONESHOT gross 0.625 (1154's pick) | 13.14% | 1.1328 | -16.12% | 0.9209/1.3324 | 14.10% / 1.1639 |
| K_ORACLE gross 1.000 | 21.13% | 1.1344 | -24.93% | 0.9224/1.3346 | 22.72% / 1.1652 |
| rolling W1260/R2Y | 11.89% | 1.1312 | -13.28%* | 0.9507/1.2932 | 12.55% / 1.1801 |
| SPY | 13.74% | 0.8368 | -33.72% | 0.6054/1.0746 | 15.21% / 0.8711 |
| RULES v2 (live) | 8.46% | 1.1960 | -12.05% | 0.8727/1.4954 | 9.46% / 1.2763 |

\* MaxDD on the common span is -13.28% for that cell on the rule-8 second half and -13.28%
full; the cells table carries every cell's own figure.

**Sharpe across the whole 33-rung U56 ladder spans 0.0041 while CAGR spans 16.97 pp
(4.16% -> 21.13%)**, exactly 1150's identity: the gross dial is one book at different
exposures. So a 4b verdict on it is decided by the **drawdown cap and CAGR floor**, never by
Sharpe. The rolling rule passes more often because it de-grosses into the cap, and it pays
for that in CAGR.

## Rule 8 walk-forward — the (window, cadence) PAIR chosen on the first half, scored on the second

Three independent honest choosers read only the first half of the common span
(2014-01 .. 2020-05) and the pick is scored on the untouched second half (2020-05 .. 2026-09).

| panel | chooser | picks | 2nd half CAGR / Sharpe / MaxDD | SPY 2nd half | 4b OOS |
|---|---|---|---|---|---|
| U56 | C_H1SHARPE | (W1260, R2Y) | 14.73% / **1.2932** / **-13.28%** | 18.22% / 1.0746 / -24.50% | **PASS** |
| U56 | C_H1CAGR | (WEXP, R2Y) | 15.79% / **1.3169** / **-13.28%** | 18.22% / 1.0746 / -24.50% | **PASS** |
| U56 | C_H1TENT | (W1260, R2Y) | 14.73% / **1.2932** / **-13.28%** | 18.22% / 1.0746 / -24.50% | **PASS** |
| U56 | K_FROZEN 0.750 | — | 19.65% / 1.3332 / -15.77% | same | **fail** |
| B136 | all three | (WEXP, R2Y) | 13.09% / 1.0329 / -14.24% | 18.03% / 1.0637 / -24.50% | fail |
| B136 | K_FROZEN 0.750 | — | 16.78% / 1.0385 / -17.55% | same | fail |

**3 of 3 U56 choosers clear 4b OOS where the frozen incumbent fails** — and the honest
reading of that row is uncomfortable: **K_FROZEN's second-half Sharpe is HIGHER (1.3332 vs
1.2932) and its CAGR much higher (19.65% vs 14.73%); it fails only on drawdown, -15.77%
against the -14.70% cap.** The rolling rule wins the 4b verdict by being smaller, not by
being better. On B136 every chooser fails, on the Sharpe leg, incumbent included.

## Verdict

**4b KEEP-CANDIDATE on U56 (memo written, recommends PARK). 4a KILL — 0 of 24 and 0 of 66.**
It is a rule-8-clean pass on the panel where it passes, and a KILL on B136. See
`.memo.md` for the exact RULES wording and the four reasons not to enact it.

## Survivorship (rule 9)

U56 and B136 are CURRENT-CONSTITUENT panels, so every CAGR and drawdown LEVEL is optimistic
and both the 4b drawdown cap and the CAGR floor are measured against an inflated book; the
bias does **not** cancel out of the 4b legs. It very largely **does** cancel out of this
run's headline claims — interior share, move rate and switch cost all contrast the same book
against itself across windows on the same tape.

Script `2026-09-17_does-the-TENT-CHOOSER-reach-the-INTERIOR-on-a-ROLLING-IS-WINDOW_cloud.py`,
6 CSVs, console log. RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.

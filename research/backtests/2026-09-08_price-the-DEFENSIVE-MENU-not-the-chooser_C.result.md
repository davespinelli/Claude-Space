# idea 418 — price-the-DEFENSIVE-MENU-not-the-chooser (lane C, 2026-09-08)

**VERDICT: ANSWERED / SPLIT. The MENU is confirmed a de-risking instrument in its purest form —
the uniform blend buys OOS drawdown in 72 of 72 cells, the only default in the record that never
misses — but the queue's antecedent is FALSE: the blend does NOT dominate the choosers. It loses
to K_CAGR on OOS Sharpe and OOS CAGR, is not separable from K_Random on Sharpe, and no genuine
multi-arm blend clears both KEEP paths at PROTOCOL's own 10-bps rung. KILL for "the honest rule-8
default is the blend, not a pick"; PARK for the blend as a named drawdown instrument.**

Corpus: idea 151's, re-derived — 3 panels x 9 (small: 6) books at matched gross 0.75 x 3 cost
rungs (0/10/25 bps) x idea 94's 17 arms = **72 cells, 1,224 arm-rows**, plus 288 blend rows
(2 constructions x 2 pools x 72 cells). Two tuned parameters, both reported at every value:
DEFAULT (6) x POOL (2). Weekly cadence, t+1 execution, IS <= 2016-12-31, OOS 2017-01-01..2026.

## Gates
* **(a)** `run_held` (idea 94's `H.run` plus the per-bar held matrix and traded delta the blend
  needs) reproduces `H.run`'s returns, turnover and gross on **all 1,224 arm-rows**, and
  `MENU_SEP` equals the mean of its sleeves' net returns: **max|diff| 4.163e-17**.
* **(b)** Idea 151's committed grid reproduces **1,224 of 1,224 rows EXACT (< 1e-12) on all three
  panels**, and the IS-4b admissibility flag agrees on **1,224 of 1,224**. Idea 401's restatement
  defect does not bite here because both runs read the same caches.

## Q1 — what the menu costs and what it buys (vs the do-nothing control, paired, 72 cells)

| default (P_ALL) | d OOS MaxDD (pp shallower) | d OOS CAGR (pp) | d OOS Sharpe | mean price (pp CAGR / pp DD) |
|---|---|---|---|---|
| **MENU_SEP** | **+3.76, 72/72, t +16.52** | **-1.97, 0/72, t -12.55** | -0.0149, 13/59, t -3.94 | **0.52** |
| MENU_NET | +3.80, 72/72, t +16.42 | -1.92, 0/72, t -12.40 | -0.0111, 16/56, t -3.05 | 0.50 |
| K_Sharpe | +2.19, 42/48, t +5.00 | -1.15, 7/55, t -5.42 | -0.0241, 18/37, t -3.34 | 0.53 |
| K_Random | +2.11, 40/55, t +4.12 | -1.27, 10/64, t -5.44 | -0.0196, 20/44, t -2.60 | 0.60 |
| K_CAGR | +0.58, 35/40, t +5.66 | **+0.21, 25/46, t +2.60** | **+0.0100, 33/46, t +3.17** | n/a (both signs positive) |

The blend is **the only default in the census that is never wrong on drawdown**: 72/72 at every
rung separately (0 bps +3.77, 10 bps +3.75, 25 bps +3.76, all t >= +8.9). It is also the only
default that is **never right on CAGR**: 0/72, mean -1.97 pp. Idea 151's "the menu de-risks
whoever picks" is confirmed and sharpened — the menu's expected member is holdable, and holding
it is the strongest form of the effect.

**Marginal exchange rate** (OLS of d CAGR on d MaxDD, both pp, moved cells): choosers pooled
-0.315 +/- 0.029 (n 221), blends pooled -0.518 +/- 0.027 (n 208), difference -0.203, **t -5.11**.
The *mean* price is common across defaults (0.52 / 0.53 / 0.60) but the *marginal* price is not:
the blend buys its extra drawdown dearer. Caveat carried: the two clouds do not span the same
range of d(MaxDD) — the blend's is far wider — so the slope gap is partly a statement about where
each default sits on the dial rather than about the dial's shape.

## Q2 — the netting credit, measured for the first time in this record

MENU_NET minus MENU_SEP, same cell and pool, P_ALL: **exactly 0.0000 at 0 bps** (max|d| 0.00e+00,
as construction requires), **+0.0311 pp of OOS CAGR at 10 bps** (+0.0033 Sharpe) and **+0.0626 pp
at 25 bps** (+0.0083 Sharpe); mean annual turnover falls 0.41x. Running the menu in one account
rather than seventeen sleeves is worth about **3 bps of CAGR at PROTOCOL's rung** — real, and two
orders of magnitude smaller than the 1.97 pp the menu costs. It never changes a verdict here.

## Q3 — dominance (MENU_SEP minus each default, same cell + pool, 144 rows)

| vs | OOS Sharpe | OOS CAGR | OOS MaxDD |
|---|---|---|---|
| D_NONE | **-0.0070, t -3.20** | -1.12 pp, t -10.04 | **+2.36 pp, 103W/1L, t +12.45** |
| K_Sharpe | +0.0073, t +1.61, sign p 0.76 | -0.42 pp, t -3.37 | +0.87 pp, t +3.70 |
| K_Random | +0.0058, t +1.40, 49W/49L | -0.31 pp, t -2.50 | +0.82 pp, t +3.28 |
| **K_CAGR** | **-0.0140, t -5.27, 23W/75L** | **-1.24 pp, t -11.94, 1W/97L** | +1.74 pp, t +9.05 |

The blend dominates **only on drawdown**. Against the incumbent K_Sharpe it is a coin flip on
Sharpe (47W/51L, sign p 0.76) — it does not beat the chooser it was proposed to replace — and it
is comprehensively beaten by K_CAGR, idea 416's pre-registered rule-8 default, on both return
metrics. **The queue's "if the blend dominates every chooser" antecedent is false, so the
consequent does not follow.**

## KEEP paths (72 rows per default x pool; 4a vs cost-matched RULES v2, 4b full and OOS-window)

| default (P_ALL) | 4a v2 | 4b full | 4b OOS | BOTH | beat SPY (OOS Sharpe) |
|---|---|---|---|---|---|
| **MENU_SEP** | **4** | **18** | 16 | 2 | 42 |
| MENU_NET | 4 | 18 | 17 | 2 | 42 |
| K_CAGR | 4 | 13 | 14 | 4 | 44 |
| K_Sharpe | 1 | 12 | 13 | 0 | 41 |
| K_Random | 1 | 12 | 15 | 1 | 40 |
| D_NONE | 0 | 9 | 9 | 0 | 44 |

The blend is the **best 4b-producing default in the census** (18 of 72 vs the control's 9), and at
PROTOCOL's own 10-bps rung it produces 6 of 24 against the control's 2 and K_Sharpe's 4. It is not
the best BOTH-paths default: K_CAGR is (4 vs 2). P5 confirmed — the blend passes 4b in 18 cells
against the 34 cells where *some* single arm passes; averaging seventeen books dilutes the CAGR
the 4b floor is measured against (P_ALL blend mean CAGR margin +2.39 pp at 0 bps, +0.90 at 10,
**-1.25 at 25**, and `CAGR` is a named failing bar in 29 of the 54 P_ALL misses).

### The one both-paths row at 10 bps is not a blend
`MENU_SEP/P_S1, u56, S3-50, 10 bps` clears 4a-vs-v2, 4b(full) and 4b(OOS): CAGR 11.27%, Sharpe
1.262, MaxDD -11.63%, halves 1.279/1.249, OOS Sharpe 1.289 / CAGR 11.73% / MaxDD -11.63%, against
SPY's 15.23% / 0.889 / -33.72% (halves 0.957/0.834, OOS 0.882) and RULES v2 @10bps' 8.66% / 1.206
/ -12.05%. **Its pool contains ONE arm (`band3-rw`) — it is a pick wearing a blend's name.** The
genuine 17-arm blend on that same cell fails 4b on the CAGR floor at every rung (margin -0.011 at
10 bps). This is idea 163's fallback confound reproduced independently on a new instrument: the
IS-4b screen leaves **46 of 72 P_S1 pools with one member or none** (empty in 40; median pool size
1), and **18 of the 20 P_S1 blend 4b passes come from the 26 non-degenerate pools**. Every P_S1
column in this file must be read as a screen-admission statistic, not a blend statistic.

The three genuine multi-arm both-paths blends (broad/S3-50 P_ALL n=17, u56/S3-50 P_S1 n=8,
u56/S4-50 P_ALL n=17) are all at the **0-bps rung**, which is a reported axis and not tradeable.
**No genuine blend clears both paths at 10 bps.**

## Pre-registered predictions
P1 CONFIRMED (72/72, +3.76 pp) · P2 CONFIRMED (-1.97 pp) · P3 CONFIRMED (0.0000 / +0.0311 /
+0.0626 pp by rung) · P4 CONFIRMED (blend -0.0149 > K_Sharpe -0.0241) · P5 CONFIRMED (18 vs 34) ·
P6 CONFIRMED (44/72 above the pool's median arm).

## Caveats
Survivorship (idea 54) — current constituents on all three panels, every CAGR flattered, so the
4b counts are optimistic; it cannot flip a paired sign. MENU_NET nets the **cost** only, each
sleeve's state machine still reads its own equity (conservative for the blend). Idea 128 — the IS
window cannot express a deep drawdown, so P_S1 admits too much. Idea 414 — the 4a comparand
convention is unsettled; 4a here is cost-matched RULES v2, with v1 reported alongside in the
CSVs. Idea 126 — t+1 execution only. 72 cells are not 72 independent observations, and the 17
sleeves inside one blend overlap almost completely; per-panel and per-rung breakdowns are in the
console file so the clustering is visible.

Files: `.console.txt` `.grid.csv` `.blend.csv` `.picks.csv` `.walkforward.csv` `.paired.csv`
`.keeppaths.csv`.

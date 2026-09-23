# idea 2535 (lane cloud, run 70, 2026-09-23) — DOES THE CANDIDATE'S DRAWDOWN EDGE SURVIVE A REALISED-VOL-MATCHED COMPARAND?

**ANSWERED = NO. KILL of the reading that the standing candidate's MaxDD edge is a TIMING statement.
Once the comparand is matched on the candidate's own TRAILING REALISED VOL instead of its GROSS, the
candidate's drawdown advantage falls from 64 of 64 book-rows to 34 of 64 (L=21: 53.1%), its Sharpe
advantage REVERSES (OOS ahead-share 60.9% -> 14.1%), and 4b-STRICT goes 0 of 64 at the tightest
matching window. The edge is a RISK-BUDGET statement, not a gate.**

Script: `research/backtests/2026-09-23_vol-matched-comparand_cloud.py` (17 of 17 gates pass, 107 s,
offline on the committed caches). Rows `.rows.csv` (512 scorings), books `.books.csv`, walk-forward
`.walkforward.csv`, gates `.gates.csv`, console `.log.txt`.

## What was asked, and the one thing that is new
Every comparand the record has scored the candidate against is matched on GROSS (idea 2532's
`BLEND_G`) or not matched at all (SPY, EWBH). **Gross is not risk.** The 200d band gate de-grosses
exactly when the panel is choppy, so a gross-matched blend is de-risked at the same TIMES the
candidate is — the matching was doing the work the run wanted to credit to the gate. The sharper
comparand matches on risk itself:

    VOLM_t = k_t x EWBH(panel) + (1 - k_t) x SHY,
    k_t    = clip( sigma_L(candidate returns, trailing L days, known at t)
                   / sigma_L(EWBH returns, trailing L days, known at t), 0, 1 )

Same names, same tape, same days, same cadence, same rung, no leverage. **G5: the ex-ante match is
exact** — `max |k_t x sigma_L(EWBH) - sigma_L(cand)| = 3.5e-18` over all 64 (cell, L) pairs; the
no-leverage clip binds on **0.53% of scored days on average (max 4.27%)**. Realised full-sample vol
of VOLM vs the candidate: **1.0643 / 1.0578 / 1.0526 / 1.0425** (U56, L = 21/63/126/252) and
**1.0377 / 1.0279 / 1.0235 / 1.0120** (B136) — matched to within 1-6%, against gross-matching's
5.7 pp of vol gap and EWBH's 9.4 pp.

DIAL 1 `L` in {21, 63, 126, 252}; DIAL 2 gross in {0.75, 1.00}. **Two tuned parameters, no more.**
Published axes, never selected on: panels {U56, B136}, cadence {W, M}, per-name cap {0.020 = CAP2,
INF = CAND}, rungs {0, 10, 25, 50} bps, band 0.03, MA 200d, SHY sweep phi = 1.00. 64 book-rows x 8
comparands = **512 published scorings**.

## The headline cell (U56, CAP2, g 0.75, W, 10 bps — the committed candidate, G3 reproduced)

| book | CAGR | Sharpe | MaxDD | Vol | H1 / H2 | OOS CAGR | OOS Sharpe | mean gross |
|---|---|---|---|---|---|---|---|---|
| **CANDIDATE** | 11.62% | 1.2687 | -14.81% | 8.99% | 1.303 / 1.246 | 12.77% | 1.3318 | 0.6718 |
| SPY | 15.23% | 0.8897 | -33.72% | 17.70% | 0.957 / 0.835 | 15.45% | 0.8831 | 1.00 |
| EWBH(U56) | 25.24% | 1.0941 | -44.19% | 23.00% | 1.252 / 1.054 | 30.35% | 1.1217 | 1.00 |
| BLEND_G (2532, gross-matched) | 16.55% | 1.1137 | -30.11% | 14.73% | 1.342 / 1.051 | 20.11% | 1.1348 | 0.6718 |
| **VOLM_L63 (vol-matched)** | **11.75%** | **1.2166** | **-17.89%** | **9.51%** | 1.271 / 1.182 | **13.19%** | **1.2815** | 0.4580 |
| VOLM_L21 | 12.00% | 1.2328 | -16.54% | 9.56% | 1.272 / 1.211 | 13.53% | 1.3050 | 0.4627 |
| VOLM_L252 | 10.77% | 1.1394 | -21.57% | 9.37% | 1.221 / 1.092 | 12.32% | 1.1945 | 0.4340 |

The candidate's famous 30-pp drawdown gap over EWBH and 15-pp gap over the gross-matched blend
collapses to **3.08 pp over VOLM_L63 and 1.73 pp over VOLM_L21**, and it pays for that with
-0.13 pp of CAGR. B136 is worse: VOLM_L63 beats the candidate on every leg
(13.20% / 1.2046 / -18.20% vs 11.82% / 1.1180 / -17.10%).

## Which legs move (the idea's own question), share of 64 book-rows the candidate leads

| comparand | Sharpe H1 | Sharpe H2 | Sharpe OOS | MaxDD no worse | CAGR no lower |
|---|---|---|---|---|---|
| SPY | 100.0% | 93.8% | 100.0% | 100.0% | 21.9% |
| EWBH | 25.0% | 51.6% | 60.9% | **100.0%** | 0.0% |
| BLEND_G (gross-matched) | 15.6% | 56.2% | 60.9% | **100.0%** | 0.0% |
| **VOLM_L21** | 29.7% | 18.8% | **18.8%** | **53.1%** | 10.9% |
| **VOLM_L63** | 20.3% | 15.6% | **14.1%** | **64.1%** | 9.4% |
| VOLM_L126 | 29.7% | 17.2% | 15.6% | 71.9% | 9.4% |
| VOLM_L252 | 35.9% | 37.5% | 29.7% | 73.4% | 34.4% |

**VOLM_L63 minus BLEND_G, in pp of rows ahead: Sharpe OOS -46.9, Sharpe H2 -40.6, MaxDD -35.9,
CAGR +9.4, Sharpe H1 +4.7.** Median gap (candidate minus comparand) over all rows: dMaxDD falls
**+17.77 pp (EWBH) -> +10.38 pp (gross-matched) -> +0.44 pp (vol-matched, L63)** and dSharpe turns
**+0.0201 -> -0.0752**. Both of the candidate's two published virtues are exposure.

**The answer is monotone in the matching window, which is the tell.** 4b-STRICT passes run
**0 / 2 / 5 / 14 of 64** at L = 21 / 63 / 126 / 252. A longer window is a LOOSER risk match — it
de-risks too slowly to follow the candidate into a crisis — so the passes appear exactly as the
matching degrades and vanish where it is tightest. Nothing here is selected on L; all four are
reported.

**4b-PROTO is 0 of 64 under EVERY VOLM, and that is an artefact of the protocol's own constant,
stated rather than hidden.** The `MaxDD >= 0.60 x comparand's` leg was calibrated against SPY's
-33.72%; against a comparand whose own MaxDD is -17.89% it demands the candidate lose no more than
-10.73%, which no book in this family does. `L_DD` therefore fails 64 of 64 under every VOLM. The
honest bar against a low-drawdown comparand is **4b-STRICT** (beats it outright, no SPY-calibrated
constant), which is why both were pre-stated and both are reported.

**Path 4a: 0 of 64.** The candidate does not beat the live RULES v2 book on both halves with no
worse MaxDD at any grid point.

## Rule 8 walk-forward (dials fitted on warm-up..2016-12-31, 2017-2026 read ONCE)
The vol window `L` is a COMPARAND dial and is **never chosen** — choosing it would be selecting a
benchmark; all four are reported on the same pick. Book dials (cap, gross) fitted by IS Sharpe and
IS Calmar at every (panel, cadence, rung): 32 picks, `0.020/0.75` in 28 of 32.

| OOS 2017-2026, pooled over 32 picks | CAGR | Sharpe | MaxDD |
|---|---|---|---|
| **the pick** | **12.04%** | **1.1392** | **-18.49%** |
| live RULES v2 baseline | 8.68% | 1.1928 | -12.15% |
| SPY | 15.36% | 0.8784 | -33.72% |

Beat the live book's OOS Sharpe **6 of 32**; SPY's **32 of 32**; EWBH's 21; the gross-matched
blend's 19; **VOLM_L63's 3 of 32** (4 / 5 / 11 at L = 21 / 126 / 252). OOS MaxDD no worse than
VOLM_L63's in **22 of 32**. Full-sample 4b-PROTO on the pick: SPY 20 of 32, EWBH 0, **every VOLM 0**;
4b-STRICT 0 / 1 / 4 / 10 at L = 21 / 63 / 126 / 252.

## Verdict
**KILL** — of the drawdown-edge reading, not of the book's arithmetic. The candidate's MaxDD
advantage is what you get for holding 0.46 of NAV in the panel and the rest in SHY; a passive sleeve
of the same names run at the same realised volatility gets the same drawdown and more Sharpe. This
closes the exposure axis that 2532 opened: after 2516 (survivorship) and 2532 (gross), **vol** was
the last matching the family had not faced, and it is the one that takes the drawdown leg too.
No RULES change, no new candidate.

## Caveats
Survivorship (rule 9): U56 / B136 are CURRENT constituents of their screens held back to 2008. EWBH,
BLEND_G and VOLM carry the **identical** contamination on the identical tape and days, so the
candidate-vs-VOLM contrast is differenced clean; the SPY columns are not and are kept for protocol
continuity only. VOLM is a *comparand*, not a proposal — it is a look-back vol-targeted sleeve and
would need its own 4b run before anyone traded it. The no-leverage clip at k = 1 binds on 0.53% of
scored days on average (max 4.27% in one cell) and **never once in any gross-0.75 cell** — it is
reached only where the book runs at gross 1.00, and then mostly in calm tape (pooled over all cells
the binding days are 2009: 435, 2013: 369, 2017: 198, 2014: 174, 2021: 136, 2011: 83, all other
years 125 combined), i.e. where the candidate is nearly fully invested and the panel is quiet.
Without the clip VOLM would be levered, which this record does not score.

# Idea 504 — price the EW-ALL control for the top-20 book on the 1,000-draw grid

**Run:** started 2026-09-10, finished 2026-09-11 UTC, cloud. **Script:** `2026-09-10_price-the-EW-ALL-control-for-the-top-20-book-on-the-1000-draw-grid_cloud.py`
**Verdict: ANSWERED — KILL for the ranking clause as a SELECTION claim.** At a matched gross the top-20
momentum-ranked book does **not** beat holding every eligible name: median dSharpe **−0.0007 (U56, t −1.24,
win 0.490), −0.0319 (B136, t −29.17, win 0.192), −0.0050 (SMALL439, t −8.60, win 0.395)** at 10 bps over
1,000 draws per panel. The entire apparent edge over EW-all is **exposure**. 4a 1/12,000 book-cells,
4b passes are a CAGR-floor artefact, nothing promoted, no RULES change.

## Gates (pre-registered, printed before any new number was read)

| Gate | Result |
|---|---|
| G1 `fast_backtest` == `engine.backtest` @10 bps | **6.939e-18** PASS |
| G2 `band_book(0.03,0.75)` == `baseline.rules_v2_weights` | **0.000e+00** PASS |
| G3 the standing **2026-09-04 KEEP-4b incumbent** re-derived on full U56 | got **12.63% / 1.0903 / −18.31%** vs published **12.66% / 1.0921 / −18.31%**, max\|d\| **1.777e-03** PASS |
| G4 EWall holds exactly gross 0.75 whenever any name is eligible | **8.882e-16** PASS |
| G4b EWmg's realised daily gross == CAND20's, every day | **9.992e-16** PASS |
| G5 draws nested across k ∈ {20,40,60} (20 seeds) | PASS |
| G6 SMALL439 drops all 44 tickers with `max_1d_move >= 1.0` | PASS (483 → 439 tradable) |

**G3 also settles the incumbent's construction**, which the record states in prose but not in code. Four
readings were tried; only one reproduces the published row: **rank over ALL columns (SPY included, as
`baseline` does), a FIXED 0.75/20 per selected name (de-grossing to cash when fewer than 20 are eligible,
not renormalising), vol scaler OFF, vol20 cap 0.60 ON.** `gross/k` renormalisation gives 13.02% / 1.0806
and excluding SPY from the rank gives 12.83% / 1.1059 — both miss. The 1.8e-03 residual is the price-cache
vintage channel. This convention is what the whole run is built on and is now pinned in code.

## Stated limitation — provenance

The queue cites idea 486's committed 6,000-book / 1,000-draw grid. That artefact could not be located in
`research/backtests` by filename, by a per-row CAND20+EWall header, by a `keep4a == -1` sentinel, or by the
strings "nested draw" / "747". The nearest committed relative
(`2026-09-09_what-n-would-make-the-partial-estimable_C.panels.csv`, 960 rows, k=40) is a **different** draw
construction. This run therefore **re-derives** the draw family deterministically (seed 504, stated in code)
and says so: these are fresh draws, not a restatement of 486's, and no claim here is conditioned on 486's
rows. Reported, not hidden.

## Design

1,000 nested draws per panel; each draw's sub-panel is the first **k=40** names of a seeded permutation.
Four books on each sub-panel, all through the **same** eligibility gate (above the 200d MA, vol20 < 0.60):

| Book | Definition |
|---|---|
| CAND20 | top 20 by composite score, **fixed 0.75/20** per name — the KEEP-4b family |
| CAND5 | top 5, fixed 0.75/5 |
| EWall | **every** eligible name, sharing a full gross of 0.75 |
| EWmg | every eligible name, equal weight, **at CAND20's own gross that day** |

CAND-n de-grosses to cash when fewer than n names are eligible, so **EWall is not gross-matched to it and
EWmg is** — exactly, day by day (G4b). Both are reported throughout, because idea 311/460's standing
complaint is that a "control" differing in exposure prices exposure and calls it signal. **Tuned: 2 (cost
rung, panel).** Everything else is structural. **SURVIVORSHIP (PROTOCOL 9): B136 and SMALL439 are today's
constituents only — levels biased up. The headline is a within-draw difference on the same 40 names over
the same days, which differences most of that out; the levels are not tradeable estimates.**

## (1) THE ANSWER — the edge is exposure, not selection

Median over 1,000 draws, **10 bps**:

| panel | CAND20 − EWall | = SELECTION (CAND20 − EWmg) | + EXPOSURE (EWmg − EWall) |
|---|---|---|---|
| U56 | **+0.0587** | **−0.0007** | **+0.0594** |
| B136 | **+0.0104** | **−0.0319** | **+0.0423** |
| SMALL439 | **−0.0124** | **−0.0050** | **−0.0073** |

Against the gross-matched control the ranking clause is **zero on U56 and negative on the other two**, at
every cost rung, and it **loses more draws than it wins on all three panels**: win rate 0.490 / 0.192 /
0.395 at 10 bps (0.432 / 0.148 / 0.415 at 25 bps). The un-matched EW-all comparison — the one the record
has been publishing — reads +0.0587 on U56 with t +58.4 and a 0.972 win rate, and **99% of that is the
exposure difference between a book that de-grosses to cash and one that does not.**

**What ranking does buy is CAGR, not Sharpe.** CAND20 − EWmg median dCAGR is **+1.46 pp/yr (U56), +0.58 pp
(B136), −0.04 pp (SMALL439)** — the concentration raises return, and raises volatility by at least as much,
while **deepening drawdown by 1.69 pp (U56) / 0.94 pp (B136)**. OOS it is mixed: dOOS Sharpe median +0.0275
(U56, win 0.833), −0.0154 (B136, win 0.384), −0.0055 (SMALL439, win 0.418).

**CAND5 is worse still** against the same EW-all control: dSharpe −0.1296 (U56, win 0.015), −0.1478 (B136,
win 0.076), +0.0119 (SMALL439, win 0.540) at 10 bps, with dOOS −0.1364 / −0.2060 / +0.0676. Narrowing the
book past 20 destroys risk-adjusted return everywhere except the small panel.

**The advantage rises with the cost rung on every panel** (U56 +0.0478 → +0.0587 → +0.0742 at 0/10/25 bps;
SMALL439 flips sign, −0.0376 → −0.0124 → +0.0230). A fixed-weight 20-name book re-trades only on membership
changes; EW-all re-weights to the whole eligible set every week. So part of what the record has been reading
as selection is a **turnover** difference, and it is the part that grows as costs rise.

## (2) BOTH KEEP PATHS, ALL FOUR BOOKS — EWall's halves restated (the queue's actual ask)

12,000 book-cells (4 books × 3 costs × 1,000 draws × … ) per panel-group, no −1 sentinels anywhere.

**4a: 1 pass in the entire grid** (SMALL439, CAND20/EWmg, one draw). **BOTH: 0.**

4b pass rate at **10 bps**:

| panel | CAND20 | EWall | EWmg | CAND5 |
|---|---|---|---|---|
| U56 | **0.723** | 0.348 | **0.178** | 0.118 |
| B136 | **0.444** | 0.308 | **0.251** | 0.010 |
| SMALL439 | 0.000 | 0.000 | 0.000 | 0.000 |

At 25 bps: U56 0.209 / 0.024 / 0.002 / 0.001; B136 0.115 / 0.045 / 0.042 / 0.000. **SMALL439 passes 4b
zero times out of 12,000 cells at every rung.**

Read with (1), this table is the clearest statement of idea 311/530/657's problem the record has produced:
CAND20 beats its **gross-matched** control on the 4b pass rate by +0.545 (U56) while **losing to it on
Sharpe**. 4b's Sharpe legs are measured against SPY — a bar both books clear — so the pass rate is decided
by the **CAGR floor**, which sees exactly the extra return that concentration buys and none of the extra
volatility and drawdown it costs. The 4b pass rate is not measuring what the ranking clause claims.

## (3) RULE 8 — the in-sample chooser destroys value

Pick among the four books on 2009–2016 IS Sharpe per draw, score 2017–2026 untouched. Mean OOS Sharpe:

| panel | cost | chosen | always EWmg | always CAND20 | always EWall | oracle | regret | SPY | live v2 |
|---|---|---|---|---|---|---|---|---|---|
| U56 | 10 | **1.1370** | 1.1741 | **1.2012** | 1.0792 | 1.2043 | 0.0673 | 0.8721 | **1.2747** |
| U56 | 25 | 1.0534 | 1.0690 | 1.0967 | 0.9544 | 1.1001 | 0.0466 | 0.8721 | 1.2378 |
| B136 | 10 | 0.9779 | **1.0345** | 1.0199 | 0.9758 | 1.0503 | 0.0724 | 0.8820 | **1.1185** |
| B136 | 25 | 0.8882 | 0.9296 | 0.9134 | 0.8546 | 0.9444 | 0.0562 | 0.8820 | 1.0740 |
| SMALL439 | 10 | 0.2259 | 0.1984 | 0.1924 | 0.2395 | 0.3539 | 0.1280 | 0.8820 | 0.5680 |

**The chooser loses to committing blindly to one book on every panel and every rung** — to always-CAND20 on
U56, to always-EWmg on B136, to always-EWall on SMALL439 — at a regret of 0.047–0.128 OOS Sharpe. It picks
EWmg most of the time (0.636 on U56, 0.502 on B136 at 10 bps, rising to 0.832/0.662 at 25 bps) and still
ends behind. **Nothing in the grid beats the live RULES v2 book** (1.2747 U56, 1.1185 B136), and SMALL439's
whole book family is far below SPY out of sample (0.23 vs 0.88).

## (4) WHAT THIS MEANS FOR THE STANDING KEEP-4b CANDIDATE

It does **not** by itself demote the 2026-09-04 candidate: 4b is a test against SPY, and the book still
passes it. What it kills is the **reason**. The candidate is "top-20 equal weight, no vol scaler", and the
implicit claim in choosing 20 names out of the eligible set is that ranking earns something. At a matched
gross, on 1,000 draws, on three panels, at three cost rungs, **it does not earn Sharpe** — it earns CAGR and
pays for it in volatility and 1.7 pp of drawdown. A gated equal-weight book at the same exposure is at least
as good risk-adjusted and simpler, with one fewer moving part to overfit.

Whether to restate the live rules accordingly is a **Sunday-review** matter (PROTOCOL 6), not this run's
call, and this run proposes no RULES/PROTOCOL edit. Filed as idea 672 so the review has it on the queue.

## Follow-ups filed

672 (restate the KEEP-4b candidate against a gross-matched gated equal-weight book and decide which is the
live rule), 673 (how much of the record's published CAND-vs-EWall premia are exposure — re-price every
committed one at a matched gross), 674 (is the 4b CAGR floor the only bar that separates a concentrated book
from its matched control).

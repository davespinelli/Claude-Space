# Idea 335 — does the c* EQUALITY at 20 bps generalise?

**Lane C, 2026-09-07. Verdict: KILL of the proposition. `c*(book + de-grossing overlay) <= c*(book at matched mean gross)` is NOT an identity, and the anchor it was generalised from does not survive an independent rebuild. Rules unchanged; no new KEEP (4a 0/90 at every rung; 4b 16/90 @10 bps, 0/90 @25, and 12 of the 16 are overlays on the NF20 twin of the record's already-standing 2026-09-04 4b row, none of them with a higher c* than that parent).**

Script: `research/backtests/2026-09-07_does-the-c-star-EQUALITY-at-20-bps-generalise_C.py`
Data: `.grid.csv` (90), `.parents.csv` (6), `.walkforward.csv` (60), `.anchor.csv` (7), `.console.txt`.

## Design

Parent (idea 40/41's book, never tuned): eligible = above the 200d MA and vol20 < 0.60; rank by the v1 composite **without** the /sqrt(vol20) term; hold the top `k = min(20, E_t)` equal-weight at `g0/k`; weekly, next-day execution, U56 and B136.

Two tuned parameters only (PROTOCOL rule 4): (1) the parent's gross rung `g0 ∈ {0.50, 0.75, 1.00}`, (2) the overlay's dial. Panel, overlay family and cost rung are census axes — every level is reported, nothing is selected on outcome. 5 families × 3 dial values × 3 rungs × 2 panels = **90 cells, all in `.grid.csv`**.

Overlay families, each de-grossing, each paired with its **matched-gross control** — the same parent scaled by the closed-form constant `a = mean gross(overlay) / mean gross(parent)`, i.e. the plain gross dial held at the overlay's own realised mean exposure (match error 0.000e+00 on all 90 cells):

| family | kind | dial |
|---|---|---|
| BREADTH | book-level, idea 41's convention | depth ∈ {0.75, 0.50, 0.25} at B = 0.40 |
| DDCTL | book-level | T ∈ {0.05, 0.10, 0.20}, cut to 0.50 |
| VOLCAP | book-level | target vol ∈ {0.10, 0.15, 0.25} |
| MABAND | per-name, daily liquidation to cash | b ∈ {0.00, 0.06, 0.12} |
| STOP | per-name, daily liquidation to cash | s ∈ {0.10, 0.20, 0.30} off a 60d high |

`c*` = first cost in [0, 50] bps at which any bar of a KEEP path turns non-positive (0.25-bps bracket then 60 bisections); computed for 4b (vs SPY) and 4a (vs RULES v2 at the same rung) on full / IS 2008-2016 / OOS 2017-2026.

## Gates (all printed in [0]; every one exact)

* **G1** `fast_bt` == `engine.backtest` on returns **and** turnover at 0 and 25 bps: `0.000e+00`.
* **G2** per-name overlay at OFF (mask all-True) == parent: `0.000e+00`.
* **G3** book-level overlay at OFF (m ≡ 1) == parent: `0.000e+00`.
* **G4** matched control at a = 1 == parent: `0.000e+00`.
* **G5** Sharpe invariance of the gross dial, a ∈ {0.25..1.00} × c ∈ {0,10,25}: max |dSharpe| `2.220e-16`.
* **G6** c* bisection reproduces on a re-run: `0.000e+00`. Matched-gross solve error over 90 cells: `0.000e+00`.
* **G7** the record's standing 2026-09-04 KEEP-4b row (`46 N n=20`, published 12.7% / 1.09 / -18.3%, halves 1.09/1.10) rebuilt at fixed n=20: **12.66% / 1.092 / -18.31% (1.09/1.10) — EXACT**. This run's parent is its NF20 twin (12.83% / 1.070 / -18.31%).

## (1) The inequality fails, and it fails where it matters

A cell is **informative** only if at least one side has a non-zero c*; when both already fail 4b at zero cost the inequality reads 0 ≤ 0 and carries nothing.

| path / window | holds (all 90) | holds (informative) | violations | max widening |
|---|---|---|---|---|
| 4b / full | 80/90 | **29 / 39** | 10 | **+17.67 bps** |
| 4b / IS | 87/90 | 10 / 13 | 3 | +14.60 bps |
| 4b / OOS | 73/90 | **22 / 39** | 17 | **+26.30 bps** |
| 4a / any | 90/90 | **0 informative** | 0 | — |

The 4a column is silent by construction: no arm in the grid beats RULES v2 at zero cost on either panel (v2 Sharpe 1.206 U56 / 1.106 B136), so every 4a c* is 0 and 90/90 is 0 ≤ 0 ninety times. It is reported, not counted as support.

Two violations are consequential rather than marginal — the overlay clears 4b at 10 bps where its matched-gross control fails at **zero** cost:

| cell | c* overlay | c* control | gap | 4b @10 bps |
|---|---|---|---|---|
| U56 g0=1.00 VOLCAP target=0.15 | **17.67** | 0.00 | +17.67 | PASS |
| U56 g0=1.00 DDCTL T=0.10 | **11.67** | 0.00 | +11.67 | PASS |
| B136 g0=0.75 VOLCAP target=0.25 | 11.25 | 6.85 | +4.40 | PASS |

## (2) The mechanism is Sharpe re-timing, and it is why idea 42 saw an equality

G5 makes the control's Sharpe **exactly** the parent's at every cost rung, so the control's c* can only move through CAGR and MaxDD. A de-grossing overlay also moves Sharpe. Spearman(dSharpe@10bps, gap) over the 39 informative cells is **+0.336**, and the violation count orders by family exactly as that predicts:

| family | informative | holds | violations | mean dSharpe@10 | max dSharpe@10 |
|---|---|---|---|---|---|
| **BREADTH** | 6 | **6** | **0** | +0.0015 | +0.0265 |
| MABAND | 6 | 5 | 1 | -0.0153 | +0.0163 |
| DDCTL | 8 | 6 | 2 | -0.0643 | 0.0000 |
| STOP | 8 | 6 | 2 | -0.0670 | -0.0041 |
| **VOLCAP** | 11 | **6** | **5** | -0.0057 | **+0.0354** |

BREADTH — idea 42's own family — is the one family that never widens c*. Its gate fires on a slow panel-level state variable and buys no Sharpe (mean +0.0015), so it behaves exactly as an exposure dial. The families that violate are the ones timed on the book's **own realised risk** (VOLCAP, DDCTL): they cut before drawdowns rather than after, which moves the Sharpe path the control cannot move. Generalising from BREADTH was generalising from the one family where the proposition is true.

## (3) The anchor does not reproduce

Idea 42's arm rebuilt on its own width (U56, n=3, g=1.00, B=0.40, depth 0.50) and its comparand (plain gross dial g=0.85):

| arm | c*_4b | CAGR@10 | Sharpe@10 | MaxDD@10 | fails 4b at 0 bps on |
|---|---|---|---|---|---|
| n=3 ungated parent g=1.00 | 0.00 | 29.0% | 1.039 | -33.11% | DD |
| n=3 overlay B=0.40 depth=0.50 | 0.00 | 26.6% | 1.009 | -27.04% | DD |
| n=3 plain gross dial g=0.85 | 0.00 | 24.8% | 1.039 | -28.91% | DD |
| n=3 matched-gross control | 0.00 | 27.4% | 1.039 | -31.50% | DD |

Both arms are 0.00 — a **degenerate** tie, not a 20-bps one. At g=1.00 the n=3 book draws down -33.1% ungated and -27.0% gated against a 4b DD cap of 20.23% (60% of SPY's), so neither arm has a 4b cost budget at all. This is a re-measurement, not idea 42's file — the eligibility, breadth series, panel and c* estimator are this run's, and idea 42's 20 bps may have been read off a different bar set. Nothing here says idea 42 erred. What it does establish is that the 20-bps equality is not a property that survives an independent rebuild of the described arm, so it cannot carry a general law.

## (4) KEEP paths and rule 8

Census over all 90 cells: **4a 0/90 at 0, 10 and 25 bps. 4b 34/90 @0, 16/90 @10, 0/90 @25.** Failing-bar distribution @10 bps: CAGR 16, none 16, `H2,CAGR,OOS` 12, DD 11, `H2,DD,OOS` 10, then a tail.

All 16 cells clearing 4b @10 bps sit on the U56 parent, 12 of them at g0=0.75 — the NF20 twin of the record's standing 2026-09-04 KEEP-4b row, whose own c* is **22.60 bps**. No overlay on that parent has a **higher** c* (range 12.15 – 22.60; the best two only tie it) and none has a higher CAGR. On the one book in this corpus that already clears 4b, every de-grossing overlay spends cost budget rather than buying it. **No new KEEP.**

Rule 8 (dial chosen on 2008-2016 only, two choosers — IS c*_4b and IS Sharpe@10 — 2017-2026 read once, 60 IS-chosen arms):

* **13/60** IS-chosen arms clear the full 4b bar set @10 bps; **0/60** clear 4a.
* **40/60** beat SPY's OOS Sharpe (0.882); **0/60** beat both SPY and RULES v2 (OOS 1.285 U56 / 1.119 B136).
* The identity holds on the OOS window for the IS-chosen dial in **51/60** arms; over the whole grid it fails in **17/39** informative OOS cells, its worst case wider (+26.30 bps) than the full sample's.
* Highest-OOS-Sharpe IS-chosen arm that also clears 4b @10 bps: U56 g0=0.75 MABAND b=0.00, OOS 14.5% / 1.181 / -15.8% @10 bps against the parent's 14.5% / 1.137 / -18.3%, SPY's 15.5% / 0.882 / -33.7% and RULES v2's 1.285. It beats SPY on Sharpe and drawdown, loses to it on CAGR, and loses to the live book on Sharpe — i.e. it is inside the standing 4b family, not an improvement on it.

## What the record should carry

The queue's proposition is false as stated, so **c* cannot be read off a book's mean exposure** and an overlay's c* must be measured, not inferred. The correct restatement, which this run does support: *a de-grossing overlay widens c* only when it moves the Sharpe path, and only risk-timed overlays (vol caps, drawdown control) do that; breadth-style state gates behave as pure exposure dials and never widen it.* Any future "the overlay paid for itself" claim should be reported beside its matched-gross control's c*, because for BREADTH-class gates that control is the whole story.

## Caveats

1. `universe.json` (56) and `universe_broad.json` (136) are **current-constituent** lists — survivorship; absolute CAGRs are optimistic on both, and B136 **contains** U56, so two panels is not two independent samples.
2. Gross is capped at 1.00 (PROTOCOL rule 2, no leverage); a c* that only leverage would move is reported as unmoved.
3. c* is a breakeven, not a return: a high-c* book with a bad level is still a bad book, which is why section [5] reports the levels beside it.
4. Book-level and per-name overlays use two different (both stated) turnover conventions — idea 41's published multiplier convention and direct simulation respectively. The two are never mixed inside a single overlay-vs-control comparison, but a cross-family comparison of c* levels inherits both.
5. The 4a path is silent on this corpus (0 informative cells); nothing here should be read as evidence about 4a either way.

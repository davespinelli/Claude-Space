# idea 258 — price-the-ranking-on-the-exchange-rate-menu (cloud, 2026-09-06)

**Verdict: ANSWERED / KILL of "drop the ranking" as a drawdown instrument — on REACH, not on price.**

Script: `research/backtests/2026-09-06_price-the-ranking-on-the-exchange-rate-menu_cloud.py`
Artefacts: `.console.txt`, `.grid.csv` (468 rows), `.menu.csv`, `.walkforward.csv`, `.sell.csv`

## What was run

Idea 74's menu with a seventh family. `DERANK` = start from the ranked book (CAND-20) and
widen it, n in {30, 40, 60, 80, 120, ALL-rankable}, constant gross 0.75 (idea 81's NORM
convention, so the de-grossing channel cannot manufacture the price). Control = CAND-20 on the
same convention. All 7 families x 6 levels x 2 books x 3 panels (u56, B136, SMALL480) x 2 cost
rungs = 468 arms, every grid point printed. Two tuned dimensions only: family and level.

Gates: idea 245's [A] (run == engine.backtest, 0.0), [B] (dg lever convention), [C] (stop ==
idea 94's, 0.0); [D] every published rate recomputed from the committed grid (0.0);
[E] NORM vs idea 74's literal `GROSS/20` control (u56 mean gross 0.7503 vs 0.7468, MaxDD
−22.63% vs −21.92%); [F] the ladder's top rung is EWall on the *rankable* set — the coverage
gap against `w_ewall0` is 0.35 names/day on u56, 0.70 on B136, and is the same at every rung;
[G] idea 74's committed CAND20 dg rates re-read (0.775 … 0.740).

## The answer

**DERANK is not on the menu because it cannot reach the budgets, not because it is dear.**

| | u56 @10bps | B136 @10bps | SMALL @10bps |
|---|---|---|---|
| DERANK max MaxDD it can buy | **1.59 pp** | **2.30 pp** | **0.52 pp** |
| de-gross reach (same control) | 13.13 pp | 14.86 pp | 17.49 pp |
| next-widest family's reach | ddctl 8.37 pp | ddctl 9.42 pp | ddctl 11.02 pp |

It reaches a pre-registered budget in **2 of 30** (panel, cost, budget) cells — B136 at T=2pp
only — and **never at T ≥ 4 pp on any panel at any cost rung**. On the small panel at 25 bps its
reach is **negative** (−1.63 pp): dropping the ranking makes the drawdown *worse*.

Where it does reach, it is **cheaper** than de-gross, so the queue's conditional
("if it is dearer than de-gross, the correct book is EWall de-grossed") **is not triggered**:

* B136 @10bps, T=2: derank 0.607 vs dg 0.617 → rank **4 of 5** reachable families
  (abs 0.330 < 200d < ddctl < **derank 0.607** < dg 0.617)
* B136 @25bps, T=2: derank **−0.030** (free insurance) vs dg 0.508 → rank **1 of 5**

That is a two-cell result and it is not stable. Along its own ladder the rate is
**non-monotone and unbounded**: u56 @10bps 0.796 (n=30) → 1.371 (n=40) → **13.98** (n≥60, where
the ladder saturates at 56 names); B136 @25bps 0.924 (n=40) → 0.119 → **−0.030 → −0.662 → −2.60**.
Widening from 20 to 30–40 names buys ~1.6 pp of drawdown; widening the rest of the way gives it
back. The ranking is a one-shot, sign-unstable dial, not a ladder.

**Rule 8 (family AND level chosen on 2009–2016, 2017–2026 read once):** the IS-cheapest family
is DERANK in **0 of 21** cells — every pick is de-gross. IS-cheapest stays OOS-cheapest in 9/21;
mean OOS rate regret **+0.181** (median +0.122), reproducing idea 74's own instability. DERANK
is the OOS-cheapest arm exactly once (B136 @25bps T=2, rate −0.101) and that is hindsight.

**KEEP paths:** DERANK passes 4a in **2 of 36** arms and 4b in **0 of 36**. Every large-cap
derank arm fails 4b on **DD**. By family across all 468 arms: 4a 111, 4b 48 —
band 19/72, ddctl 10/72, 200d 8/72, abs 6/72, dg 3/72, stop 2/72, **derank 0/36**.
The 4b passes reproduce idea 74's published band-family arms; nothing new is claimed from them.

## The sell side (the same pair read the other way, EWall control)

| panel @10bps | n=20 vs EWall-rankable | pp CAGR gained | pp MaxDD sold | rate |
|---|---|---|---|---|
| u56 | 15.60% vs 13.23% | +2.37 | +0.17 | **13.98** |
| B136 | 14.83% vs 14.14% | +0.69 | +0.39 | **1.76** |
| SMALL | 14.65% vs 10.20% | +4.44 | **−6.42** | free (shallower AND richer) |

Idea 82's published 0.86 pp/pp **does not reproduce on this construction** — u56 prices at
13.98, B136 at 1.76. That is not a refutation of idea 82: its books use its own gross
convention and its own EWall (all priced names, not the rankable set), and the denominator is a
difference of two single realised extrema. It is a warning that the 0.86 the queue quotes is
construction-specific and should not be carried as a constant.

## Predictions, scored

* P1 derank rate ≈ 0.86 ± 0.25 — **FALSE** (0.80–13.98 on u56, sign-unstable on B136)
* P2 derank dearer than dg at every reachable large-cap budget — **FALSE** (0 of 2 cells)
* P3 derank reach < 4 pp — **TRUE** (1.59 / 2.30 / 0.52 pp)
* P4 derank ranks 4th–7th — **PARTLY** (rank 4 at 10 bps, rank 1 at 25 bps; mean 2.50 of 5)
* P5 rule 8 never picks derank — **TRUE** (0 of 21)
* P6 the two sides do not contradict — **TRUE** (buy side is a reach failure; sell side is cheap)

## What it means for the book

The drawdown dial on a ranked book is **gross**, and it is gross by default rather than by
price: de-gross is the only family that reaches every budget on every panel, and it is the
rule-8 pick in 21 of 21 cells. Dropping the ranking is a ~1.6–2.3 pp move with an unstable sign
and no ladder behind it, so it cannot be written into RULES as a drawdown instrument at any
budget. The correct book remains **CAND-n de-grossed**, not EWall — but the reason is reach,
and idea 82's separate Sharpe/CAGR case for EWall is untouched by this run.

## Caveats

SURVIVORSHIP: all three panels are current constituents with no delistings, so every rate here
is priced in a world with less drawdown to buy; it runs specifically against the wide arm,
which holds the names a delisting-aware panel would kill. The small panel is secondary
throughout (ideas 39/49/136: the trend gate is inverted there). u56's derank ladder saturates
at n ≥ 56 — four of its six rungs are the same book, and that is printed, not hidden. A rate's
denominator is a difference of two single realised extrema and is the noisiest object in the
project (idea 117). Costs are flat linear bps on turnover (idea 126). No level here is a
tradable estimate.

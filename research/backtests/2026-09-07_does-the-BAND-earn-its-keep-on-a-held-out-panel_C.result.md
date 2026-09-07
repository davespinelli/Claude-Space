# Idea 347 — does the no-trade BAND earn its keep at MATCHED CADENCE on a panel the record has not mined?

**Verdict: KILL the band as a distinct instrument.** The queue's own hypothesis is FALSIFIED, and
the instrument dies anyway — for a different and stronger reason than the one that was pre-registered.

Script: `2026-09-07_does-the-BAND-earn-its-keep-on-a-held-out-panel_C.py` (23 s, deterministic).
Book fixed at idea 331's convention: top-20 eligible by the v1 composite with the vol scaler OFF,
NORM weights `g/k_t` at g = 0.75, next-day execution, 10 bps unless a rung is named.
Two tuned parameters: **cadence** ∈ {D, W, 2W, M, 6W, Q} × **m** ∈ {0, 10, 20, 40}. Panel and cost
rung {0, 10, 25} are reported axes. All 24 cells × 3 panels × 3 rungs are in `.grid.csv`.

## 0. Reproduction gates — all pass to the published digit

| gate | this run | idea 331 published |
|---|---|---|
| fast_backtest vs engine.backtest | max\|dr\| **0.000e+00**, max\|dturn\| **0.000e+00** | — |
| derived rung r(25) vs `backtest(cost_bps=25)` | max\|d\| **0.000e+00** | — |
| `sel_band(m=0)` nests `sel_hard(n=20)` | **0** disagreements on all 6 cadences | — |
| U56 M m=20 (331's PARK candidate) | 13.30% / 1.109 / −18.73%, 1.196/1.042, 2.76x, OOS 1.124, c\* 95 | identical |
| U56 6W m=20 (331's sibling) | 14.31% / 1.159 / −19.42%, 1.155/1.175, 2.29x, OOS 1.250, c\* 104 | identical |
| B136 W m=20 / M m=20 (inherited 329 gates) | 14.27% / 1.009 / −20.43%, H2 0.817 · 16.77% / 1.108 / −26.31%, H2 1.006, OOS 1.092 | identical |
| 331's matched-turnover split at m=20 | **U56 2/6, B136 4/6** | 2/6, 4/6 |

## 1. The queue's hypothesis is falsified

The queue predicted the matched-turnover win rate would fall to ~9/18 off U56. It does the opposite.

| panel | wins @10 bps | sign-test p | median dSharpe | @0 bps | @25 bps |
|---|---|---|---|---|---|
| **B80held (HELD OUT)** | **12/18** | 0.238 | **+0.0406** | 12/18 | 12/18 |
| U56 (331's parent) | 8/18 | 0.815 | −0.0110 | 9/18 | 9/18 |
| B136 | 10/18 | 0.815 | +0.0368 | 10/18 | 11/18 |

Reading idea 331's own `matched.csv` first shows why the premise was wrong: its per-panel splits were
U56 **2/6**, B136 4/6, SMALL439 4/6. U56 is where the band did *worst*, so "10/18 is a U56 artefact"
was never consistent with the parent's own file. Nothing is significant on any panel (p ≥ 0.24, and
the sign test is optimistic here — the 18 cells share twins).

## 2. Why the band dies anyway: the "matched" comparison is matched at the grid edge

The m=0 twin pool has a **turnover floor** — its slowest cell, Q m=0. Every slow banded cell falls
below that floor and is matched to the edge, i.e. credited for turnover the cadence dial *cannot
reach at all*. That is exactly where the wins live:

| panel | m=0 floor | banded cells below it | band wins there | cells pinned to the Q m=0 twin | band wins there |
|---|---|---|---|---|---|
| B80held | 3.28x | 6/18 | **6/6** | 10/18 | **10/10** |
| U56 | 2.71x | 6/18 | 4/6 | 9/18 | 7/9 |
| B136 | 3.63x | 6/18 | 5/6 | 9/18 | 7/9 |

Restrict to comparisons that are actually turnover-matched and the effect inverts:

| relative gap \|turn gap\|/twin turn | B80held | U56 | B136 | **pooled** |
|---|---|---|---|---|
| ≤ 5% | 2/4 | 3/5 | 2/3 | 7/12 |
| ≤ 10% | 4/8 | 3/9 | 3/7 | **10/24, median dSharpe −0.0233** |
| ≤ 20% | 7/13 | 5/13 | 7/15 | 19/41 |
| all cells | 12/18 | 8/18 | 10/18 | 30/54, median +0.0135 |

**On the cells where the match holds, the band loses more often than it wins, on all three panels.**
The same picture by cadence — the band's wins are a slow-cadence phenomenon, i.e. exactly where the
twin is pinned to the Q grid edge (idea 240/256's grid-edge flag applies):

| panel | D | W | 2W | M | 6W | Q | fast vs slow |
|---|---|---|---|---|---|---|---|
| B80held | 2/3 | 0/3 | 1/3 | 3/3 | 3/3 | 3/3 | **3/9 vs 9/9** |
| U56 | 0/3 | 1/3 | 0/3 | 3/3 | 3/3 | 1/3 | 1/9 vs 7/9 |
| B136 | 3/3 | 0/3 | 0/3 | 2/3 | 3/3 | 2/3 | 3/9 vs 7/9 |

Pooled: **23/27 slow, 7/27 fast.** The band beats the calendar only where the calendar has run out.

## 3. Both KEEP paths — the band admits nothing off U56

| rung | 4b | of which m=0 | of which m>0 | 4a |
|---|---|---|---|---|
| 0 bps | 17/72 | 4/18 | 13/54 | **0/72** |
| 10 bps | 14/72 | 2/18 | 12/54 | **0/72** |
| 25 bps | 10/72 | 1/18 | 9/54 | **0/72** |

**All 14 of the 10-bps 4b passes are U56.** B80held 0/24 and B136 0/24 at every rung; every one of
those 48 cells fails 4b at **zero** cost, so `c* = --` throughout. Binding bars over all 72 cells:
DD 55, H2 34, OOS 23, CAGR 10, H1 9. On B80held the **DD cap binds on all 24 cells** (realised
−24.2% … −29.8% against a −20.23% cap), so no setting of (cadence, m) at n=20/g=0.75 can clear 4b
on that panel — a panel fact, not a band fact (this reproduces idea 333's B136 finding on the
held-out slice). **4a is 0/72: nothing here beats the live book in both halves without a worse
drawdown.** No panel shows a banded 4b pass where the cadence dial alone has none.

## 4. Rule 8 walk-forward — (cadence, m) chosen on ≤2016 Sharpe @10 bps, 2017+ read once

| panel | arm | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|
| **B80held** | IS-chosen **2W m=10** | 9.65% | **0.729** | −28.09% |
| | IS-chosen, band-free pool (2W m=0) | 8.68% | 0.681 | −27.34% |
| | anchor W m=0 | 8.32% | 0.661 | −29.21% |
| | OOS-best M m=10 (hindsight) | 14.45% | 1.014 | −26.13% |
| | RULES v2 (live baseline) | 6.89% | 0.944 | −12.49% |
| | SPY | 15.45% | 0.882 | −33.72% |
| **U56** | IS-chosen **Q m=40** | 14.03% | 1.065 | −19.06% |
| | IS-chosen, band-free pool (M m=0) | 17.57% | **1.307** | −19.51% |
| | anchor W m=0 | 14.45% | 1.131 | −18.31% |
| | RULES v2 / SPY | 9.53% / 15.45% | 1.285 / 0.882 | −12.05% / −33.72% |
| **B136** | IS-chosen **M m=0** (band not picked) | 16.41% | 1.041 | −26.10% |
| | anchor W m=0 | 12.45% | 0.884 | −20.05% |
| | RULES v2 / SPY | 7.98% / 15.45% | 1.119 / 0.882 | −12.24% / −33.72% |

Regret (IS-chosen − OOS-best): B80held −0.284, U56 −0.299, B136 −0.051. The cost of removing the
band from the chooser's menu is **+0.048 on B80held, −0.242 on U56, 0.000 on B136** — i.e. the band
helps the chooser on the held-out panel by less than a quarter of what it costs on the parent, and
the chooser beats SPY OOS on **0/3** panels once it picks a banded cell (B80held 0.729 < 0.882;
U56's 1.065 clears SPY but is 0.242 *below* what the band-free chooser would have taken). The
chooser beats the live book OOS on **0/3**.

## 5. What actually generalises

The **cadence** dial moves Sharpe by +0.13 to +0.17 (W→M/6W, m=0) on every panel; the band moves it
by −0.10 to +0.25 with no stable sign except at D, where it is uniformly positive (+0.08 … +0.25) —
i.e. the band's one robust use is as a brake on a daily book, and a daily book with a brake is
strictly worse than simply rebalancing weekly. Turnover remains the ordering key: spearman(turn/yr,
Sharpe) = −0.603 / −0.330 / −0.350 across all 24 cells (−0.657 / −0.371 / −0.486 on m=0 alone).

## 6. Caveats

1. **SURVIVORSHIP** — all three panels are current-constituent lists; every CAGR level is optimistic.
   This run compares cells *on the same panel*, which is far less exposed than the levels.
2. **B80held is held out from idea 331's menu but is not independent of B136** (it is 80 of its 136
   columns), so B80held/B136 agreement is weaker evidence than B80held/U56 agreement. The decisive
   §2 result holds on U56 too, which is the independent leg.
3. 2W and 6W decimate the weekly mask and are phase-anchored to the panel's first complete week; a
   different phase is a different, untested choice.
4. The sign test treats 18 sharing comparisons as independent — its p is a lower bound.
5. §2's relative-gap thresholds are diagnostics on the *matching*, not on the book; three of them are
   reported, none is chosen.

## 7. Bottom line

The band is not U56-specific — it wins slightly more often on a panel the record had never mined.
It is, however, **an artefact of the turnover-matching itself**: on the 24 pooled comparisons where
the twin is genuinely turnover-matched the band wins 10 and loses 14, and every clean win sits where
the banded cell has dropped below the cadence dial's floor. Off U56 it clears neither KEEP path at
any of the three cost rungs, on 48 of 48 cells, at zero cost. **KILL.** Idea 331's `[B2]` reading
should be restated in the record: a nearest-turnover twin drawn from a pool with a floor is not a
matched comparison, and the record's other matched-turnover claims should be re-read for the same
grid-edge pin.

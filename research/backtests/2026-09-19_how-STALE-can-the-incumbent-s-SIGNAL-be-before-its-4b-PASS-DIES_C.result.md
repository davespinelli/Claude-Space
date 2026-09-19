# Idea 1298 (lane C, 2026-09-19) — how STALE can the incumbent's SIGNAL be before its 4b PASS DIES?

**ANSWER: three days under the construction this idea describes — and the pass dies on the
DRAWDOWN leg, not on return. The Sharpe decay itself is NOT resolvable on this tape at any rung
out to a full month, under either construction. As a DIAL the lag is a KILL: choosing it in sample
costs -0.0192 OOS Sharpe on average (worst -0.0618) and the IS pick is the ex-post best OOS lag on
0 of 6 arms, so PROTOCOL rule 2's frozen d = 1 stands.**

## 1. The finding that matters for capital

U56, the frozen 2026-09-04 book (N=20, H=126, gross 0.75, weekly, 10 bps), trading **d rows late**:

| d | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR | OOS Sharpe | 4b DD room (pp) | 4b |
|---|---|---|---|---|---|---|---|---|
| 1 (rule 2) | 15.82% | 1.1543 | -19.13% | 1.2072 / 1.1209 | 17.34% | 1.1862 | **+1.101** | PASS |
| 2 | 15.92% | 1.1567 | -20.07% | 1.2251 / 1.1115 | 17.36% | 1.1813 | +0.156 | PASS |
| 3 | 15.80% | 1.1497 | -20.07% | 1.2142 / 1.1075 | 17.29% | 1.1784 | +0.160 | PASS |
| 5 | 15.50% | 1.1263 | -20.60% | 1.1865 / 1.0882 | 17.09% | 1.1598 | **-0.365** | FAIL (DD) |
| 10 | 15.62% | 1.1295 | -21.07% | 1.1869 / 1.0949 | 17.24% | 1.1609 | -0.839 | FAIL (DD) |
| 21 | 15.64% | 1.1234 | -21.10% | 1.2437 / 1.0417 | 16.84% | 1.1244 | -0.870 | FAIL (DD) |

SPY 15.12% / 0.8843 / -33.72% (OOS 15.26% / 0.8737); live RULES v2 8.62% / 1.2010 / -12.05%
(OOS 9.46% / 1.2766). 4a fails at all 36 cells of the run, as it does everywhere in this family.

**The whole 4b pass rests on 1.10 pp of drawdown room, and one week of trading late costs 1.47 pp
of drawdown.** The CAGR leg never binds (+4.9 to +5.3 pp of room at every rung) and the Sharpe legs
never bind on U56. Staleness does not stop the book earning; it makes the book take a deeper
drawdown, and the 4b cap is where that shows up.

## 2. The decay is not resolvable, so the pass/fail flips are not findings

Paired circular-block bootstrap (400 reps, 63-row blocks, seed 20260919; both books resampled on
identical blocks): **0 of 36 cells have |t| >= 2 on the Sharpe difference from d = 1.** Worst on
U56/LATE is t = -1.25 at d = 5; worst anywhere is +1.92 (B136/SNAP, d = 2). The U56/LATE ladder is
ordered (rho = -0.886, OLS -0.00156 Sharpe per day of staleness) but its whole spread, 0.0333, is
1.49x the median rung SE. Outcome **(C) UNRESOLVED** under the rule fixed before the run.

So the honest reading is not "the book survives 3 days": it is that the tape cannot resolve the
Sharpe cost of staleness, while the drawdown cost is monotone (-0.95, -0.94, -1.47, -1.94, -1.97 pp
at d = 2, 3, 5, 10, 21) and is enough to break 4b by d = 5.

## 3. The record contains TWO incompatible definitions of "execution lag", and they disagree by
more than the effect

* **LATE** (this idea's wording, "trades late"): decide on the weekly close, trade d rows later.
* **SNAP** (idea 1287's construction): trade on the fixed row after the weekly close with a
  d-row-old snapshot.

Identical at d = 1; at d >= 2 they are different books. |SNAP - LATE| in Sharpe reaches **0.1051
(B136, d = 21)** and **0.1000 (B136, d = 2)** against a median rung SE of 0.0498 — the naming
ambiguity is **2.1x the measurement noise** and larger than either ladder's own spread. The U56 4b
verdicts disagree rung for rung: LATE passes at d = 1, 2, 3; SNAP passes at d = 1 and 5 only.

This also settles the replay: SNAP reproduces 1287's committed rows to **3.4e-2** (most cells
~1e-3) while LATE misses them by **1.0e-1**, a factor 3.0 — so 1287's non-monotone U56 ladder is
its construction plus unresolved noise, not a tape-vintage artefact. **A committed lag result that
does not name its construction is uninterpretable.**

## 4. Rule 8 — the lag is not a dial worth choosing

Lag chosen on warm-up..2016-12-31 by IS Sharpe (ties to the lower lag), 2017-2026 read once,
against PROTOCOL's frozen d = 1:

| conv | panel | IS pick | IS margin | OOS Sharpe pick | OOS Sharpe d=1 | chooser gain | ex-post best d |
|---|---|---|---|---|---|---|---|
| LATE | U56 | 21 | +0.0159 | 1.1244 | 1.1862 | **-0.0618** | 1 |
| LATE | B136 | 2 | +0.0066 | 0.9992 | 1.0184 | -0.0192 | 1 |
| LATE | SMALL | 10 | +0.0972 | 0.4642 | 0.4407 | +0.0235 | 21 |
| SNAP | U56 | 10 | +0.0342 | 1.1353 | 1.1862 | -0.0509 | 21 |
| SNAP | B136 | 3 | +0.1164 | 1.0570 | 1.0184 | +0.0386 | 21 |
| SNAP | SMALL | 10 | +0.0769 | 0.4423 | 0.4407 | +0.0016 | 2 |

Mean **-0.0114** OOS Sharpe across the six arms (LATE -0.0192, worst -0.0618); positive on 3 of 6,
and the IS pick is the ex-post best OOS lag on **0 of 6**. There is no staleness worth selecting.

## 5. Gates, and what is NOT claimed

* **Anchor.** (U56, d=1) reads 15.82% / 1.1543 / -19.13%, OOS 17.34% / 1.1862 against the committed
  15.79% / 1.1529 / -19.13%, OOS 17.30% / 1.1837 — worst |diff| **2.5e-3**, which misses a 5e-4
  exact replay but sits inside the tape-vintage floor (idea 1335 measured ~7e-3 of half-sample
  movement from one daily rewrite of `data/prices*.csv`; commit 4e19a80 rewrote it on 2026-09-18).
  Every cell here is built on ONE tape, so the within-run comparisons are unaffected; only the
  cross-run comparisons in sections 3 and 5 carry that floor, and they are labelled.
* **Not claimed:** that d = 1 is safe. It is the only rung with drawdown room, and 1.10 pp is
  inside what a single tape rewrite has been shown to move. Nothing here estimates live expectancy.
* **Survivorship (rule 9).** U56/B136 are current-constituent hand-kept lists; SMALL is a current
  constituent sub-$2B screen (54 tickers with max_1d_move >= 1.0 dropped). All three flatter a
  momentum book, so the drawdown levels above are optimistic and the DD leg's 1.10 pp of room is
  an upper bound.
* 36 cells, all published in `.grid.csv`; decay/SE in `.decay.csv`; rule 8 in `.walkforward.csv`;
  full console in `.log.txt`. Deterministic, offline, 11s.

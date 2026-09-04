# Idea 87 — `interior-4b-passes-are-unselectable`: **KILL the rule-8 amendment** (cloud lane, 2026-09-04)

Script `research/backtests/2026-09-04_interior-4b-selection_cloud.py` · console `…console.txt` ·
grid `…grid.csv` (66 points) · selections `…selections.csv` (48).
10 bps, weekly, weights at close *t* applied *t+1*. Two tuned parameters: the grid parameter
and the selection margin `m`. Harness reproduces idea 2's KEEP row (**12.7 % / 1.093 / −18.3 %,
halves 1.088 / 1.103**), idea 72's `B136/EWall` (**10.7 % / 1.027 / −17.7 %**) and idea 57's
`ew-band3` on broad (**11.1 % / 1.064 / −16.8 %**, the CHANGELOG's published figures) to the
decimal before any new number is read.

**Question.** Ideas 66 and 15 each produced a cross-universe 4b pass at an *interior* parameter
value that rule 8 overshot. Does `Rm(m)` = "argmax IS Sharpe **s.t.** |IS MaxDD| ≤ 0.60·|SPY IS
MaxDD| − *m* pp and IS CAGR ≥ 0.70·SPY IS CAGR", *m* ∈ {0,1,2} pp, recover it out of sample?

**Answer: no — and the reason is that two of the six grids cannot be selected on by anything.**

---

## 1. Rm does not beat rule 8 on anything that matters

| rule | selections | infeasible | OOS Sharpe vs default arm | vs grid OOS-best | picks pass OOS-4b | picks an INTERIOR full-4b arm |
|---|---|---|---|---|---|---|
| R0 (incumbent) | 12 | 0 | **+0.031** (9/12 wins) | −0.028 (hits 2/12) | 4/12 | 3/12 |
| Rm(m=0pp) | 10 | 2 | +0.027 (7/10) | −0.034 (**0/10**) | 6/10 | 4/10 |
| Rm(m=1pp) | 9 | 3 | +0.029 (5/9) | −0.029 (**0/9**) | 5/9 | 3/9 |
| Rm(m=2pp) | 4 | **8** | +0.033 (3/4) | −0.030 (**0/4**) | 2/4 | 2/4 |

The one incremental recovery worth naming is `GROSS/EWall` on broad, where Rm(0pp) picks
g = 0.80 instead of R0's g = 1.00 — an OOS Sharpe difference of **+0.0009**. That is 4b
*compliance*, not performance. And **13 of 48 selections are infeasible** (8 of 12 at m = 2pp):
the amended rule is not even well-defined without a fallback the QUEUE never specified.

## 2. The premise is half right, and the half that is wrong is fatal

The QUEUE assumed "IS Sharpe is monotone in the risk parameter while the 4b drawdown cap is not".
Measured spreads *within* each grid:

| grid | IS Sharpe spread | IS MaxDD spread | OOS Sharpe spread |
|---|---|---|---|
| GROSS/top20 (u56 / broad) | **0.0002 / 0.0046** | 7.6 / 8.8 pp | 0.0008 / 0.0038 |
| GROSS/EWall (u56 / broad) | **0.0007 / 0.0025** | 7.3 / 7.4 pp | 0.0001 / 0.0021 |
| CRYPTO/CAND20 (u56 / broad) | 0.156 / 0.131 | **0.0000 / 0.0000** | 0.067 / 0.099 |
| CRYPTO/EWall (u56 / broad) | 0.174 / 0.159 | **0.0000 / 0.0000** | 0.078 / 0.100 |
| BAND/ew-all (u56 / broad) | 0.124 / 0.084 | 1.2 / 1.0 pp | 0.120 / 0.053 |
| N/ranked (u56 / broad) | 0.123 / 0.080 | 7.7 / 9.3 pp | 0.293 / 0.197 |

* **Gross is not selectable.** A 2× change in gross moves IS Sharpe by 0.0002-0.0046 and OOS
  Sharpe by 0.0001-0.0038, while moving IS MaxDD by 7-9 pp. R0's pick on this grid is decided
  by the fourth decimal of a noise statistic (it lands on g = 1.00 in 3 of 4 cells); Rm's pick is
  decided entirely by the constraint. Neither is selection — this replicates ideas 66/73/83's
  finding that gross is an exact lever with zero Sharpe content, and shows it *forecloses* the
  amendment rather than motivating it.
* **The crypto constraint is degenerate.** IS MaxDD is spread **exactly 0.0000** across the cap
  grid on both universes: the in-sample max-drawdown episode predates the crypto sleeve's
  tradeable window, so the constraint carries **zero** information about the parameter it is
  meant to constrain. Consequently Rm picks cap = 0.15 whenever feasible — identical to R0, and
  failing 4b on DD both full-sample and OOS on both lists. **Rm recovers idea 15's c = 0.05 in
  0 of 8 (rule, universe) cells.** The interior crypto pass is not recoverable by *any* rule of
  this shape.
* Where selection genuinely has content (BAND, N: IS Sharpe spread 0.08-0.12), the margin
  changes nothing except by making the problem infeasible (`N/ranked` broad at m ≥ 1pp).

## 3. The margin is unstable in *m* and disagrees across universes

`GROSS/top20` broad picks 1.00 → 0.70 → 0.60 → 0.60 as the rule goes R0 → m=0 → 1 → 2;
`BAND/ew-all` broad picks 0.08 → 0.08 → 0.08 → 0.02. Four of six grids give a **different pick
per universe** under at least one rule. A selection rule whose answer moves with an arbitrary
1 pp margin, and differs by list, is not a rule — it is a second tuned parameter wearing a
safety label.

## 4. What the run *does* confirm (no amendment needed)

* **8 arms pass full-sample 4b on BOTH universes**: `BAND/ew-all` at 0.02, 0.03, 0.05, 0.08;
  `CRYPTO/CAND20` 0.05; `CRYPTO/EWall` 0.05 and 0.10; `GROSS/EWall` 0.80.
* Idea 57's band book is the run's most robust object: **every** feasible rule picks band = 0.08,
  and *all four* non-zero bands pass cross-universe 4b. R0 was never the obstacle there.
* Idea 2's n = 20 is picked by every rule on u56 (4b PASS) but every rule picks n = 30 on broad
  (4b fails on DD) — the universe-specificity ideas 44/53 flagged, reproduced independently.

## Verdict — **KILL** for the amendment; the ideas were parked correctly

The QUEUE's hypothesis, "rule 8's selection rule — not the ideas — is what has been failing", is
**false**. Rule 8 did not fail on ideas 66 and 15; those grids have no selectable content, and no
constrained-argmax variant can manufacture some. Rules unchanged. PROTOCOL rule 8 unchanged.

## Proposed PROTOCOL clause (for the Sunday review — a *pre-test*, not a new selection rule)

> **8a. Selectability pre-test.** Before walk-forward-selecting a parameter, report the grid's
> in-sample spread in the selection objective and in each binding 4b bar. If the IS Sharpe spread
> across the whole grid is under 0.02 (gross-type levers), or the spread in a binding constraint
> is 0.00 (a constraint blind to the parameter), the parameter is a **policy dial, not an
> estimate**: rule 8 does not apply to it and it must be set by a stated risk budget (idea 69),
> reported as a structural variant. Only parameters that pass the pre-test are walk-forward
> selected.

**Caveats.** Both lists are current constituents (SURVIVORSHIP — absolute CAGRs optimistic; this
run compares *selection rules on a common grid*, so the bias falls on every arm alike). BTC/ETH
are the two crypto survivors and their weekend moves land in the Monday bar, so every crypto arm
here is an upper bound (idea 15's caveats carry over unchanged). The IS window contains no
COVID-scale crash (IS SPY MaxDD −22.1 % vs OOS −33.7 %), which is *why* the IS drawdown cap is
the weak constraint — a point that argues against the amendment, not for it.

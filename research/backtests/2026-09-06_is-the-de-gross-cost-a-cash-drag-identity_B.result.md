# Idea 290 — is-the-de-gross-cost-a-cash-drag-identity (lane B, 2026-09-06)

**Verdict: the strict identity is a KILL; the 91% version is the result.**
De-grossing is *algebraically* a leverage transform of the respread book (exact to 2.08e-17),
and per cell **91.4% of its CAGR cost is pure cash drag** — but the remaining **9%** is not
noise: it is **negative in 35 of 36 cells** (mean −0.40 pp/yr, worst −1.24 pp), it **grows with
band width** (−0.32 → −0.57 pp from b=0.00 to b=0.12) and with **slower cadence** (Q −0.75 pp
vs W −0.27 pp). And the regression the QUEUE proposed — gap on mean gross — is **misspecified**:
R² 0.573 at 10 bps, resid sd 0.70 pp.

Script `research/backtests/2026-09-06_is-the-de-gross-cost-a-cash-drag-identity_B.py`;
outputs `.console.txt`, `.grid.csv`, `.identity.csv`, `.walkforward.csv`, `.summary.csv`.

## Reproduction gates (binding before any new number was read)

| gate | this run | published |
|---|---|---|
| No-filter EWall control, weekly, 10 bps | **10.2% / 0.679 / −36.2%** | idea 49/52: 10.2% / 0.677–0.679 / −36.2% |
| DEGROSS gate-cost range across all 12 (gate×cadence) arms, 0 bps | **4.78 – 8.33 pp** | idea 52: 4.78 – 8.33 pp |
| Band dial removes this share of RESPREAD/MA/W cost | **75.4%** | idea 52: ~76% |

## P1 — the construction (HOLDS, 2.08e-17)

Both books share one gate mask `g` and differ only in the denominator: RESPREAD `w = g/k_t·G`
(k = names gated IN), DEGROSS `w = g/n_t·G` (n = names LIVE). So `w_dg = (k_t/n_t)·w_rs` at
every rebalance, and the engine's between-rebalance drift *preserves* proportionality (both
renormalise the same growth vector against their own total). Therefore `r_dg,t = c_t·r_rs,t`
**exactly**, with `c_t` = realised-gross ratio = share of live names gated in.
Measured worst `max_t |r_dg,t − c_t·r_rs,t|` over the 36 cells: **2.082e-17**.

**The de-gross book is the respread book at time-varying leverage c_t ∈ [0.42, 0.52]. There is
no separate "de-gross strategy" on this panel.**

## P2 — the QUEUE's regression (FAILS its bar, and the bar was the wrong test)

| y | slope (pp per unit gross) | intercept | R² | resid sd | max\|resid\| |
|---|---|---|---|---|---|
| gap @10 bps | −25.45 | +5.01 | **0.573** | 0.698 pp | 1.704 pp |
| gap @0 bps | −22.42 | +3.56 | **0.621** | 0.557 pp | 1.278 pp |

Bar was R² ≥ 0.95 and resid sd ≤ 0.25 pp → **FAILS**. The reason is specification, not physics:
cash drag is a **product**, (1−c̄)·μ, and across these 36 cells mean gross barely moves
(0.314 → 0.394) while the respread book's own CAGR moves 5.0% → 10.7%. Consequently:

| regressor(s) | R² |
|---|---|
| mean gross alone (the QUEUE's form) | 0.621 |
| respread CAGR alone | **0.880** |
| both | 0.916 (resid sd 0.267 pp) |
| **constant-leverage replay, zero fitted parameters** | 0.664 |

## P3 — the structural decomposition (FAILS its bar, narrowly, and systematically)

Replay `r_A,t = c̄·r_rs,t` (one number per cell, its own mean leverage) and read the CAGR:

* mean \|gap₀\| **4.346 pp**, mean \|residual\| **0.4005 pp** = **9.22%** of the gap
* **exposure share: mean 0.914, min 0.798, max 1.000**
* bars were mean\|resid\| ≤ 0.25 pp **and** ≤ 10%×4.346 = 0.435 pp → **FAILS the first, passes the second**
* **residual sign: 35 negative / 1 positive** — not noise
* by cadence W −0.273 / M −0.184 / Q −0.745 pp; by gate MA −0.519 / MAVOL −0.282 pp;
  by band 0.00 −0.322 → 0.12 −0.574 pp

The sign is the finding: de-grossing does not merely hold less; it holds less **at the wrong
times**, and the penalty widens exactly as the band widens — the same dial idea 52 showed
removes 75% of the *respread* cost.

## Rule 8 walk-forward — (band, cadence) on 2010–2016, 2017–2026 read once

| arm | pick | OOS CAGR | OOS Sharpe | OOS MaxDD | regret | vs ctrl | vs SPY | vs LIVE |
|---|---|---|---|---|---|---|---|---|
| RESPREAD MA | b=0.12, M | 10.73% | 0.7163 | −37.6% | −0.0723 | +0.079 | −0.166 | −0.569 |
| RESPREAD MAVOL | b=0.12, M | 6.54% | 0.5084 | −38.4% | 0.000 | −0.129 | −0.374 | −0.777 |
| DEGROSS MA | b=0.05, M | 4.69% | 0.6543 | −16.7% | 0.000 | +0.017 | −0.228 | −0.631 |
| DEGROSS MAVOL | b=0.05, M | 2.05% | 0.4104 | −14.7% | −0.0527 | −0.227 | −0.472 | −0.875 |

OOS comparands: no-filter control 10.10%/0.6372/−36.2% · **SPY 15.45%/0.8820/−33.7%** ·
**LIVE RULES v2 9.53%/1.2851/−12.1%**. Picks beating SPY 0/4, the control 2/4, the live book 0/4.

## KEEP paths (all 72 cells)

**4a 0/72. 4b 0/72.** Binding 4b bars: H1 72, H2 72, OOS 72, CAGR 67, DD 46 — nothing on this
panel clears SPY in any half, gated or not, under either construction. No memo, no candidate.

## What the record should do with this

1. A de-gross-vs-respread contrast is **~91% a re-pricing of exposure**. Quoting one as
   evidence about a *gate* without the constant-leverage replay beside it overstates the gate
   by roughly 10× on this panel.
2. Do **not** estimate that share by regressing the gap on mean gross (R² 0.57–0.62). The
   correct per-cell estimator is the zero-parameter constant-leverage replay.
3. The 9% residual is a real, signed, dial-dependent cost of de-grossing's exposure **timing**
   and deserves its own column, not to be absorbed into "the gate".

**SURVIVORSHIP:** `data/prices_small.csv.gz` is a screen of *current* sub-$2B constituents, no
delistings. The headline is an arm-minus-arm contrast on identical names and days (the two
constructions share one gate mask), so the bias very largely cancels out of P1/P2/P3; it does
not cancel out of the 4a/4b level columns, which are reported only to record that both are 0.

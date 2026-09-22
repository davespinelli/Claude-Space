# Idea 2241 (lane B, 2026-09-22) — does an ASYMMETRIC 200d BAND (b_in, b_out) clear 4b where the SYMMETRIC one cannot?

**ANSWERED = NO. KILL on BOTH KEEP paths, 0 of 420 published grid points.** The band's two
edges do buy real exposure and real return, but the whole reachable range of the dial tops out
**below** 4b's CAGR floor — even at ZERO cost with perfect hindsight on both parameters.

Script: `research/backtests/2026-09-22_asymmetric-band-entry-exit_B.py`
Artefacts: `.grid.csv` (420 rows, every point), `.comparands.csv`, `.walkforward.csv`,
`.gates.csv`, `.log.txt`.

## What was priced

RULES v2 clause 2's single band constant split into two edges — IN above `ma*(1+b_in)`
(entry lag), OUT below `ma*(1-b_out)` (exit patience), previous state in between, OUT before
200 closes. Sizing, cadence and gross are the live ones and are **not** tuned
(`gross = 0.75 / N`, weekly, de-gross to cash).

* **Tuned, exactly two:** `b_in` in {0.00, 0.01, 0.02, 0.03, 0.05, 0.08}, `b_out` in
  {0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12} — 42 cells.
* **Reported, never selected:** cost rung {0, 5, 10, 25, 50} bps, panel {U56, B136}, cadence W.
* 42 x 5 x 2 = **420 rows, all published in `.grid.csv`**.

**GATES: 12 of 12 PASS.** G1 `b_in = b_out = 0.03` reproduces `baseline.rules_v2_weights`
exactly (max |dw| = 0.0); G2 the state matrix equals `baseline.band_state` exactly; G3 the
10 bps return line is identical to the live baseline's to 0.0; G4 the loose corner carries more
exposure than the tight one (0.649 vs 0.380 U56); G5 the grid's own 0.03/0.03 cell reproduces
the comparand baseline Sharpe to 0.0; G6 the grid is complete on both panels.

## Numbers at the PROTOCOL rung (10 bps, FULL sample 2009-01-13 -> 2026-09-18)

| | CAGR | Sharpe | MaxDD | H1 / H2 Sharpe | mean exposure | turnover |
|---|---|---|---|---|---|---|
| U56 live (0.03/0.03) | 8.62% | 1.2010 | -12.05% | 1.2276 / 1.1806 | 0.533 | 1.77/yr |
| U56 max-CAGR (0.01/0.12) | 10.02% | 1.1595 | -15.83% | — | 0.645 | 1.16/yr |
| B136 live (0.03/0.03) | 7.96% | 1.0972 | -12.24% | 1.2296 / 0.9669 | 0.532 | 2.01/yr |
| B136 max-CAGR (0.00/0.12) | 10.17% | 1.1309 | -16.79% | — | 0.644 | 1.28/yr |
| B136 max-Sharpe (0.03/0.08) | 9.29% | 1.1429 | -14.90% | — | 0.591 | 1.42/yr |
| SPY buy-and-hold | 15.14% | 0.8851 | -33.72% | 0.9570 / 0.8264 | — | — |

4b bars on this sample: **CAGR floor 10.60% (U56) / 10.59% (B136)**, DD cap -20.23%.

## The mechanism, and why it cannot reach

1. **The dial works.** `dCAGR/d(mean exposure)` = **+0.1133 (U56) / +0.1648 (B136), R2 0.94**
   across the 42 cells. Loosening both edges is worth **+1.40 pp (U56) / +2.21 pp (B136)** of
   CAGR against the live cell, and it does so at *lower* turnover (1.77 -> 1.16/yr), because a
   wider hysteresis band trades less.
2. **It costs drawdown, and the budget is there to pay.** The same move costs **-3.78 pp /
   -4.55 pp** of MaxDD, landing at -15.83% / -16.79% against the 4b cap of -20.23%. The DD cap
   binds in **0 of 84** 4b-fail rows at 10 bps; both SPY Sharpe legs and the OOS Sharpe leg pass
   in **100%** of them.
3. **The ceiling is structural.** The loosest legal corner (0.00 / 0.12) reaches mean exposure
   **0.645**, i.e. 86% of the 0.75 gross cap. At **zero cost** and with both parameters chosen
   by hindsight the best FULL CAGR the whole ladder reaches is **10.15% (U56) / 10.31% (B136)** —
   **0.45 pp / 0.28 pp short of the floor**. So the CAGR floor binds in **100%** of fails and
   there is no cell, cost rung or panel where it does not. Widening the band cannot fix a book
   whose gross is 0.75: the missing return is a SIZE shortfall dressed as a timing question.
4. **4a dies on a different leg on each panel.** U56: **0 of 42** cells beat the live book's
   Sharpe in *both* halves — the live 0.03/0.03 cell IS the Sharpe argmax, so symmetry is
   locally optimal there. B136: 9 of 42 cells beat both halves and 11 of 42 hold the DD leg, but
   the two sets are **disjoint** — the best-Sharpe cell (0.03/0.08, 1.1429 vs live 1.0972,
   +1.33 pp CAGR) fails 4a only because its MaxDD is 2.66 pp worse than the live book's. That is
   exactly the asymmetry PROTOCOL rule 4b was added to correct, and 4b then fails it on return.

## Rule 8 walk-forward (parameters from 2009-2016 ONLY; 2017-2026 read once)

Chooser = argmax IS Sharpe over the 42 cells, per (panel, cost). Picks: **U56 0.02/0.08**
(0.03/0.12 at 50 bps), **B136 0.01/0.12** — the loose corner, at every rung.

| 10 bps, OOS 2017-2026 | CAGR | Sharpe | MaxDD |
|---|---|---|---|
| U56 rule-8 pick (0.02/0.08) | 9.77% | 1.1848 | -14.61% |
| U56 live baseline | 9.46% | 1.2767 | -12.05% |
| B136 rule-8 pick (0.01/0.12) | 9.50% | 1.0734 | -16.54% |
| B136 live baseline | 7.85% | 1.1017 | -12.24% |
| SPY | 15.29% | 0.8751 | -33.72% |

OOS 4b floor = 10.70% (U56) / 10.68% (B136): both picks **fail by 0.9 / 1.2 pp**, with the DD
cap unbinding by 5.6 / 3.7 pp. **4a is 0 of 10 (panel x cost) walk-forward cells.**

**A finding worth carrying:** the IS-Sharpe chooser beats the live book in-sample by +0.082
(U56) / +0.118 (B136) Sharpe and then **loses to it out-of-sample on 9 of 10 cells** (the single
exception is B136 at 50 bps, where the live book's turnover is punished harder). On this ladder
IS Sharpe is an **anti-predictor of OOS Sharpe** — the in-sample gain of a looser band does not
survive, while its extra drawdown does.

## Verdict

**KILL on 4a and KILL on 4b**, at every cost rung, on both panels, in FULL, IS and OOS. No
memo, no RULES wording, no rules change. `RULES.md`, `scan.py`, `bot.py`, `baseline.py`,
`PROTOCOL.md` untouched.

## Honest limits

One gross (0.75), one cadence (W), one weekday offset, one MA length (200d) — the result is a
statement about the band's two edges at the live sizing, not about bands in general. Both panels
are current constituents (PROTOCOL rule 9: survivorship-optimistic). Costs are a flat per-unit-
turnover model with no spread, impact or borrow. The exposure ceiling of 0.645 is a property of
this band family and this universe, not a theorem.

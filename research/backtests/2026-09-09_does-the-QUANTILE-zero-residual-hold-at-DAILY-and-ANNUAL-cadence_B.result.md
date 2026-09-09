# Idea 307 — does-the-QUANTILE-zero-residual-hold-at-DAILY-and-ANNUAL-cadence (lane B, 2026-09-09)

**ANSWERED. The zero HOLDS at DAILY — tighter than anything idea 300 published — and BREAKS at
ANNUAL. QUANTILE-M is a control on D/W/M/Q and is NOT one at A. KILL of the unqualified
"pure-exposure control" claim; the control survives with an explicit cadence bound.**

Script: `2026-09-09_does-the-QUANTILE-zero-residual-hold-at-DAILY-and-ANNUAL-cadence_B.py`
Outputs: `.grid.csv` `.decomp.csv` `.cadence.csv` `.walkforward.csv` `.leaderboard.txt` `.console.txt`

Panel SMALL439 (439 sub-$2B names, the 44 with `max_1d_move >= 1.0` dropped), 2011-01-13..2026-09-04
(15.61 yrs), gross 0.75, 10 bps, next-day execution. Two tuned dials, all 45 points reported:
theta (9, idea 300's grid verbatim) x cadence (5: D, W, M, Q, A). x is a deterministic function of
theta (the matching), not a third dial. 180 books.

## Gates, read before the headline

| gate | result | bar |
|---|---|---|
| G0.1 local cadence-extended runner vs `engine.backtest` at D/W/M/Q | **0.000e+00** on returns, 0 mask-disagreement bars | < 1e-15 |
| G0.2 idea 300's committed `.decomp.csv` resid0 at W/M/Q, 162/162 cells | **4.441e-14** pp/yr (c_bar 3.3e-16) | < 1e-6 |
| G0.3 idea 290's identity `r_dg,t == c_t * r_rs,t` at 0 bps, every cadence | worst **6.731e-16** (D) | < 1e-12 |
| G0.4 matching quality, \|d mask fraction (Q − MA)\| at all 9 thetas | worst **0.00166** | < 0.01 |

`engine.rebalance_mask` has no "A", and PROTOCOL forbids editing the engine, so the annual arm runs
through a local copy of engine's own loop with one extra period key; G0.1 is what makes the A column
a different *cadence* rather than a different *backtester*. Rebalances in the window:
D=3934, W=817, M=189, Q=63, **A=16** — the dial spans 246x.

## The headline: QUANTILE-M resid0 (pp/yr), 9 thetas per cell

| cadence | mean FULL | sd | max abs | mean OOS | mean c_sd | verdict vs the 0.05 band |
|---|---|---|---|---|---|---|
| **D** | **−0.0006** | 0.0027 | **0.0034** | **−0.0007** | 0.0009 | **PASS — 16x tighter than W, the tightest published point** |
| W | −0.0094 | 0.0075 | 0.0189 | −0.0053 | 0.0025 | (idea 300, reproduced) |
| M | −0.0390 | 0.0197 | 0.0636 | −0.0268 | 0.0058 | (idea 300, reproduced) |
| Q | +0.0114 | 0.0043 | 0.0170 | +0.0316 | 0.0097 | (idea 300, reproduced) |
| **A** | **−0.1239** | 0.0476 | **0.1789** | **−0.1700** | 0.0158 | **FAIL — 2.5x the mean bar, 1.8x the max bar, 3.4x OOS** |

Pre-registered clauses (H_ZERO_IS_A_CONTROL needs all eight):

- D: (1) PASS |−0.0006| ≤ 0.05 · (2) PASS 0.0034 ≤ 0.10 · (3) PASS |−0.0007| ≤ 0.05 · (4) PASS inside the W/M/Q envelope [−0.0890, +0.0614]
- A: (1) **FAIL** |−0.1239| · (2) **FAIL** 0.1789 · (3) **FAIL** |−0.1700| · (4) **FAIL** outside the envelope

**H_ZERO_IS_A_CONTROL FAILS. H_ZERO_IS_INTERIOR HOLDS** — but "interior" is the wrong word for the
shape that came out: the zero is *monotonically better* as cadence shortens, and it is the long end
alone that breaks it.

At A the residual is also **one-signed**: negative at all 9 thetas (min −0.0347, max −0.1789), so it
is a systematic drag, not scatter.

## Why: the "constant exposure by construction" claim decays with holding period

`c_t == x` is true only on rebalance days. Between them the book drifts, and the longer the block the
further c_t wanders from x. The realised dispersion is monotone in cadence —
mean c_sd **0.0009 (D) → 0.0025 (W) → 0.0058 (M) → 0.0097 (Q) → 0.0158 (A)**, an 18x span — and the
mean exposure itself drifts up with it (c_bar 0.5101 → 0.5164). At A each level is held across a full
calendar year, so `pred0`'s arithmetic c_bar is standing in for a step function with a year of
compounding inside each step, and the Jensen gap that `resid0` collects is no longer negligible.
|mean resid0| tracks c_sd at D < W < M < A; **Q is the exception** (c_sd 0.0097 but resid0 only
+0.0114, and positive at 9/9 thetas), so the mapping is a tendency, not a law.

## The consequence that matters: at A the control stops discriminating

`resid0`'s job is to separate a pure cash dial from a gate that times. The gap between the two
families, in units of the QUANTILE cell's own sd:

| cadence | resid0 Q | resid0 MA | gap (pp/yr) | gap in Q sd |
|---|---|---|---|---|
| D | −0.0006 | −0.0904 | −0.0897 | −32.9 |
| W | −0.0094 | −0.2164 | −0.2070 | −27.5 |
| M | −0.0390 | −0.2416 | −0.2025 | −10.3 |
| Q | +0.0114 | −0.6871 | −0.6985 | −164.1 |
| **A** | **−0.1239** | **−0.1078** | **+0.0162** | **+0.34** |

At annual cadence the two gates' residuals are indistinguishable — and the sign of the gap flips, so
the "pure" gate carries the *larger* drag. A control that cannot be told apart from the thing it is
controlling for is not a control at that point on the dial.

## Second finding (not asked for, worth the record): the MA lump is cadence-bound too

Idea 298 published the MA gate's residual as "a level-independent lump of roughly −0.3..−0.6 pp/yr",
and idea 300 carried that as a pre-registered band of [−0.70, −0.20]. Extended to the ends, the MA
residual is **−0.0904 (D)** and **−0.1078 (A)** — both outside that band, against −0.2164 / −0.2416 /
−0.6871 at W/M/Q. The MA gate's residual is not level-independent in cadence; it is largest at Q and
collapses toward zero at both extremes, for different reasons (D: exposure re-set every bar, no block
to compound the mistiming; A: only 16 decisions in 15.6 years). **The band is a W/M/Q fact.**

## Rule 8 walk-forward (IS 2010..2016-12-31 chooses, OOS 2017-01-01..2026 read once)

**WF-A** — (theta, cadence) picked on IS Sharpe inside each family x construction arm:

| arm | IS pick | OOS Sharpe | OOS CAGR | OOS MaxDD | vs SPY | vs RULES v2 | vs EWall control | regret |
|---|---|---|---|---|---|---|---|---|
| MA-THRESH/RESPREAD | θ=+0.30, M | 1.1042 | 24.02% | −30.8% | +0.2221 | −0.1809 | +0.4807 | 0.0000 |
| MA-THRESH/DEGROSS | θ=−0.40, Q | 0.5874 | 7.98% | −32.5% | −0.2946 | −0.6977 | −0.0593 | 0.2474 |
| QUANTILE-M/RESPREAD | θ=−0.12, Q | 0.6307 | 9.35% | −34.8% | −0.2513 | −0.6544 | −0.0161 | 0.1561 |
| QUANTILE-M/DEGROSS | θ=−0.12, Q | 0.6365 | 7.03% | −25.4% | −0.2456 | −0.6486 | −0.0103 | 0.1451 |

SPY OOS Sharpe 0.8820 / CAGR 15.45% / MaxDD −33.7%; RULES v2 OOS 1.2851 / 9.53% / −12.1%. Three of
four IS picks land below SPY, all four below RULES v2, and three of four below their own no-gate
control — the gate adds nothing OOS on this panel, consistent with idea 300.

**WF-B** — the cadence dial itself is not learnable: IS-best cadence matches OOS-best in **1/4** arms.
IS points at Q in three arms; OOS pays at M in three. Always-M beats the IS pick in every arm but one.
Nobody should select cadence on IS Sharpe here.

**WF-C** — is a hard ZERO still the best available predictor of the OOS residual? On QUANTILE-M,
**yes at D/W/M/Q, no at A**: MAE(zero) 0.0020 / 0.0063 / 0.0268 / 0.0316 beats every fitted
alternative, but at A MAE(zero) = 0.1700 loses to the IS per-cell estimate's 0.1192 and the IS
constant's 0.1194. That is the operational statement of the break — at A the residual is large enough
and stable enough that *knowing it* beats *assuming it away*. Zero wins 8/10 family x cadence cells
overall (4/5 on QUANTILE-M, 4/5 on MA-THRESH).

## Both KEEP paths, all 180 books

**4a 0/180 · 4b 0/180 · BOTH 0/180**, and 0/36 at every single cadence. 4b failing clauses over the
180: H1 179, OOS 177, H2 174, CAGR 166, DD 130. Best book per cadence by full-sample Sharpe:

| cad | best book | CAGR | Sharpe | MaxDD | halves | OOS | turn/yr | 4b fails |
|---|---|---|---|---|---|---|---|---|
| D | QUANTILE-M/DEGROSS θ=−0.40 | 8.28% | 0.6025 | −35.8% | 0.67/0.57 | 0.5806 | 4.43 | H1,H2,OOS,DD,CAGR |
| W | MA-THRESH/RESPREAD θ=+0.30 | 14.93% | 0.7714 | −43.4% | 0.48/1.02 | 1.0431 | 19.47 | H1,DD |
| M | MA-THRESH/RESPREAD θ=+0.30 | 20.86% | 1.0264 | −30.8% | 0.94/1.11 | 1.1042 | 8.19 | DD |
| Q | MA-THRESH/RESPREAD θ=+0.30 | 15.75% | 0.7708 | −35.9% | 0.60/0.92 | 0.9013 | 4.31 | H1,DD |
| A | MA-THRESH/RESPREAD θ=+0.30 | 13.08% | 0.6802 | −35.9% | 0.73/0.66 | 0.6736 | 1.32 | H1,H2,OOS,DD |

The one near-miss (M/RESPREAD, DD only) is a full-gross unhedged small-cap book carrying the panel's
whole −30.8% drawdown against SPY's 60% bar of −20.2%; it is not a defence and it is not a candidate.

**SURVIVORSHIP:** `data/prices_small.csv.gz` is current constituents of the screen — no delistings —
so every CAGR *level* above is inflated and the 4a/4b columns inherit that bias whole. The headline
`resid0` is an arm-minus-arm contrast on the same names, the same ranking and the same days, so the
bias very largely cancels out of it. No memo, no RULES change.

## What the record should do with this

QUANTILE-M stays the record's pure-exposure control, **with a stated bound: cadence D through Q**.
Published numbers that used it at W/M/Q are unaffected (reproduced to 4.4e-14). Any future use at
annual or longer holding periods must carry the residual explicitly — it is −0.12 pp/yr full-sample,
−0.17 pp/yr OOS, one-signed, and the same size as the MA gate it is supposed to price against.

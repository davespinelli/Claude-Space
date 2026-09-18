# Idea 1313 — do SELECTION and EXPOSURE STACK at SMALL's DD CAP?
*(2026-09-18, lane cloud, idea 1 of 2. Script: `2026-09-18_do-SELECTION-and-EXPOSURE-STACK-at-SMALL-s-DD-CAP_cloud.py`, offline, deterministic, 22.4s.)*

**VERDICT: KILL on the queue's own question (SMALL's -20.23% cap stays shut) — and a
KEEP-4b PASS on U56 / B136 that the stack, not either instrument alone, is responsible for.**

## What was run
Two dials only (PROTOCOL rule 4): **N {15, 20, 30, 40}** x **TARGET {6, 8, 10, 12}%**.
Frozen at values prior runs already certified and not touched here: H=63 (1301's shallowest
cell), WINDOW=21d (1297's only OOS winner), CAP=0.60 (the incumbent's gross — no leverage,
rule 2), cadence W, 10 bps, warm-up 260, decide-at-t / apply-at-t+1.
Scaler: `k_t = min(0.60, TARGET / v_t)`, `v_t` = annualised sd of the SELECTION book's own
flat-gross returns over the 21 rows **ending at t-1** (1297's B_CONST basis; a recursive
B_SELF arm is published as robustness). 16 stacked cells + 4 selection-only + 4
exposure-only + the frozen anchor, **every cell published**, on U56 / B136 / SMALL663
(41 books x 3 panels; +48 B_SELF). Replay gates G0-G5 all PASS, including 1301's
selection claim (+4.66 pp MaxDD, +0.70 pp CAGR) and 1297's exposure claim (-22.70% at 6%/21d).

## 1. SMALL: the stack does NOT close the gap — it moves the binder, it does not clear it
| leg | anchor (N=15/H=126 flat) | best STACK cell (N=30/6%) | 4b requirement |
|---|---|---|---|
| MaxDD | -33.35% | **-18.69%** | >= -20.23% |
| CAGR | 7.06% | **5.47%** | >= 9.84% |

3 of 16 stacked cells clear the **drawdown** cap — something neither instrument alone ever
did (1297's deepest reached -22.43%, 1301's -28.69%). **0 of 16 clear the cap AND the CAGR
floor.** The cap is bought, and the CAGR floor is what it is bought with: every cell that
clears -20.23% lands at 5.32-5.47% CAGR against a 9.84% floor, a 4.4 pp miss where the
anchor missed by 2.8 pp. **4b is 0/16 full-sample and 0/16 OOS on SMALL; 4a is 0/48 on all
panels.** The queue's hypothesis is answered NO on the panel it was asked about.

## 2. The instruments ADD where the cap is already clear and SUBSTITUTE where it binds
`resid = dMaxDD(stack) - [dMaxDD(selection) + dMaxDD(exposure)]`, all vs the same anchor:

| panel | resid mean | range | additive (|r|<=1pp) | substituting (r<-1pp) |
|---|---|---|---|---|
| U56 | **+3.19 pp** | -0.76 .. +6.13 | 4/16 | 0/16 |
| B136 | **+6.57 pp** | +5.66 .. +8.09 | 0/16 | 0/16 |
| SMALL663 | **-1.07 pp** | -3.45 .. +1.53 | 4/16 | **8/16** |

The sign of the interaction is a PANEL fact, not a property of the two instruments: on the
large-cap panels the stack is **super-additive** (it buys more drawdown than the two dials
bought separately, and CAGR resid is positive too, +0.49/+0.57 pp), while on SMALL — the only
panel where the 4b DD leg actually binds — it is **sub-additive in 8 of 16 cells**. Any future
claim that "selection and exposure compose" must name its panel.

## 3. U56 / B136: a real 4b pass, and the stack is what buys it
Best U56 cell **N=15 / TARGET=6%**: full sample **11.81% / 1.2290 / -10.66%** (H1 1.294,
H2 1.172; turnover 3.79x/yr) vs the frozen anchor 13.66% / 1.1706 / -16.38% and SPY 15.13% /
0.8849 / -33.72% (cap -20.23%, floor 10.59%). It is the **super-additive cell** (resid
+6.13 pp): selection alone at N=15/H=63 makes drawdown *worse* (-21.22%, 4b FAIL) and
exposure alone reaches only -11.95%. 4b passes **11/16 (U56)** and **14/16 full, 12/16 OOS
(B136)**; **4a 0/48** — the live book's drawdown is unbeatable by construction, as the record
has found every time.

## 4. Rule 8 (params chosen on warm-up..2016-12-31, 2017-2026 read ONCE)
argmax IS Sharpe picks **U56 N=15/6%**, B136 N=15/10%, SMALL N=40/8%.

| panel | OOS stack | OOS anchor | OOS SPY | OOS RULES v2 | 4b OOS |
|---|---|---|---|---|---|
| U56 | **12.31% / 1.2444 / -10.66%** | 15.12% / 1.1947 / -16.38% | 15.28% / 0.8747 / -33.72% | 9.47% / 1.2781 / -12.05% | **PASS** |
| B136 | 13.06% / 1.0374 / -15.54% | 14.11% / 1.0454 / -15.97% | 15.33% / 0.8769 / -33.72% | 7.88% / 1.1061 / -12.24% | **PASS** |
| SMALL663 | 4.39% / 0.4283 / -22.26% | 6.40% / 0.4653 / -33.35% | 15.33% / 0.8769 / -33.72% | 4.47% / 0.6518 / -12.18% | FAIL |

U56's pick is the only one that improves on its own anchor out of sample: **+0.0497 of OOS
Sharpe and +5.72 pp of OOS MaxDD for -2.81 pp of OOS CAGR** — a larger Sharpe gain than
1297's exposure-only OOS winner bought (+0.0166 for -1.54 pp), at a larger CAGR price. B136's
pick is OOS-flat against its anchor (-0.0081 Sharpe); SMALL's is negative on every leg. The
B_SELF arm agrees on direction (U56 pick identical, +3.37 pp OOS MaxDD, -0.0076 Sharpe).

## What this is NOT
Not a RULES change (rule 6; that is a Sunday decision). Not a SMALL solution. Not a free
lunch: **every** U56/B136 4b pass here is bought with CAGR, so the stack is a
drawdown-for-return trade an operator must want, not a dominance.

**SURVIVORSHIP (rule 9).** U56 / B136 / SMALL663 are current-constituent lists; SMALL663 is a
sub-$2B screen carried back to 2010, so every absolute SMALL number is biased **up** — which
makes the SMALL KILL stronger, not weaker.

# Idea 291 — does-the-banded-slow-filter-survive-on-the-large-cap-panels

**Run:** cloud, 2026-09-06. Script `2026-09-06_does-the-banded-slow-filter-survive-on-the-large-cap-panels_cloud.py`.
**Verdict: ANSWERED, SPLIT. "Slowing" is TWO dials and they go opposite ways on large caps.
KILL of idea 52's actual form (band ≥0.05 AND quarterly) — it does not replicate. PARK of the
BAND half, which is real, monotone and ~70% timing, but whose argmax sits on the grid EDGE in
4 of 4 arms. No RULES change, no KEEP; `RULES.md`, `scan.py`, `bot.py`, `baseline.py` untouched.**

## What was run

Idea 52's exact 18-point grid — band b ∈ {0.00, 0.02, 0.03, 0.05, 0.08, 0.12} × cadence ∈ {W, M, Q}
(2 tuned parameters) — at **RESPREAD** (75% gross always deployed across the gated-IN names, so
the filter is pure selection/timing), on **U56** and **B136**. Reported never-selected axes: gate
(MA = 200d band only; MAVOL = the band AND `vol20<0.60`) × construction (RESPREAD, DEGROSS control).
**144 cells, all printed**, each also at 0 bps. Control = EWall, every live name at 75% gross, no
filter, at the same cadence. 10 bps, t+1 execution.

## 1. The mechanism: the band slows the gate without changing how much it holds

| U56 / MA | b=0.00 | 0.02 | 0.03 | 0.05 | 0.08 | 0.12 |
|---|---|---|---|---|---|---|
| flips/name/yr (daily) | 7.865 | 2.488 | 1.842 | 1.278 | 0.843 | **0.540** |
| mean share IN | 70.8% | 70.8% | 70.8% | 68.4% | 67.6% | **67.7%** |

Flips fall **14.6×** while the held share barely moves. The band is a churn dial, not an exposure
dial — so anything it earns is a genuine re-selection effect, not the filter quietly switching off.
B136 is the same shape (8.023 → 0.615 flips, 70.9% → 71.0% IN).

## 2. The BAND half helps, and it is mostly TIMING not cost

dSharpe vs no-filter control at the same cadence, RESPREAD, weekly:

| | b=0.00 | 0.02 | 0.03 | 0.05 | 0.08 | 0.12 |
|---|---|---|---|---|---|---|
| U56 / MA | −0.033 | +0.014 | +0.039 | +0.032 | +0.055 | **+0.103** |
| B136 / MA | −0.064 | −0.046 | −0.052 | −0.050 | −0.013 | **+0.056** |

Widening the band is worth **+0.136 (U56) / +0.120 (B136)** of Sharpe over the hard gate at weekly.
**At ZERO cost the gain persists: CAGR 12.47% → 14.31% on U56/MA/W (+1.85 pp), 12.54% → 13.90% on
B136/MA/W (+1.36 pp).** Turnover falls 7.60 → 1.93 /yr, worth only **0.57 pp** at 10 bps — so
roughly **70% of the band's value is timing and 30% is the cost saving**. On large caps whipsaw is
real, which is the opposite of idea 60's finding on the sub-$2B panel (the 3% band recovered only
7.0% of the gate's damage there).

## 3. The CADENCE half does NOT help — and idea 52's actual form fails to replicate

Sharpe at cadence c minus weekly, RESPREAD, at the live band b=0.03: U56/MA **M −0.008, Q −0.057**;
U56/MAVOL **M −0.031, Q −0.072**; B136/MA M +0.018, Q +0.042; B136/MAVOL M −0.006, Q −0.019.
Slowing hurts on U56, is a wash on B136. The band's own gain also *shrinks* as cadence slows
(+0.136 at W → +0.055 at M → +0.083 at Q on U56/MA): the two dials are substitutes, not complements.

**Idea 52's small-cap winner re-priced here — gate MA, b ≥ 0.05, cadence Q, RESPREAD (it beat the
control by +0.053 Sharpe on SMALL439): 2 of 6 cells beat the control, mean dSharpe −0.0109**, and
0 of 6 clears 4b (all fail the drawdown cap). U56 b=0.05/Q −0.026, b=0.08/Q −0.035, b=0.12/Q +0.045;
B136 b=0.05/Q −0.038, b=0.08/Q −0.024, b=0.12/Q +0.013. The two positives are b=0.12, i.e. the band,
not the cadence.

## 4. Rule 8 walk-forward (8 arms; (b, cadence) on ≤2016 by IS Sharpe, 2017–2026 read once)

Chooser beats the no-filter control OOS in **5 of 8** arms and SPY in 8 of 8, but **loses to the
pre-registered anchor (b=0.03, W) in 6 of 8**: mean OOS Sharpe **1.1293 vs 1.1733 (−0.0440)**, mean
regret 0.0875. Picked cadences {M 3, W 3, Q 2}, picked bands {0.12 ×4, 0.02 ×2, 0.00, 0.08} — no
cadence preference at all, and the band picks cluster at the edge. SPY OOS 0.882; RULES v2 OOS
1.294 (U56) / 1.121 (B136).

## 5. KEEP paths, and why the best cell is PARKed

**4a: 0 / 144.** **4b: 29 / 144 — all RESPREAD (0 / 72 DEGROSS).** First failing bar: CAGR 58,
DD 47, H2 10. U56 RESPREAD 19/36, B136 RESPREAD 10/36.

Best cell — **U56 / RESPREAD / MA / b=0.12 / W: CAGR 14.09%, Sharpe 1.233, MaxDD −19.36%,
H1/H2 1.268/1.211, OOS 15.22%/1.272/−19.36%, turnover 1.93/yr, +0.103 vs the control.** 4b PASS,
and it is the only 4b passer that also beats the do-nothing control by more than 0.06.

**PARK, not KEEP, for three stated reasons:**
1. **Grid edge.** b=0.12 is the argmax in **4 of 4** RESPREAD arms — the band dial is unbounded at
   the top of the grid, so its optimum has not been located. Any number quoted here is a lower bound.
2. **Not cross-universe.** The same cell on B136 is 13.66%/1.179/−21.72% and **fails 4b on the
   drawdown cap** (−21.72% vs the −20.23% bar); its H2 is 1.078 against U56's 1.211.
3. **Not chooser-reachable.** Rule 8 inside U56/RESPREAD/MA picks (b=0.02, Q) → OOS 1.084, **0.188
   of Sharpe short** of this cell. A hindsight-only optimum is not a candidate.

The next test this earns is a widened band ladder (b to 0.20–0.30) with the cadence held at weekly,
which would either locate the optimum or show the curve is still climbing when the gate stops
gating.

## Caveats

B136 is current-constituent (survivorship, PROTOCOL rule 9); U56 excludes BTC/ETH. All at 10 bps
per unit turnover with t+1 execution; costs were not swept. The control's own turnover is 0.84/yr
(U56) so the comparison is not cost-flattered in the filter's favour.

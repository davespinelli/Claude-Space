# Idea 556 — why does the MA slice flip from better to worse at the panel boundary?

**Lane C, 2026-09-09.** Script: `2026-09-09_why-does-the-MA-SLICE-flip-from-better-to-worse-at-the-panel-boundary_C.py`
**Verdict: ANSWERED / KILL of the "panel boundary" reading. No KEEP candidate (4a 0/162, 4b 10/162, BOTH 0/162).**

## The question

Idea 305's exact attribution splits the MA gate's zero-cost CAGR advantage over a depth-matched
quantile gate as `dCAGR0_dg = SELECTION + LEVEL + TIMING`, and reports SELECTION as
**+1.2436 pp/yr (SMALL439)** against **−0.5779 (U56)** and **−0.4058 (B136)** — the same gate on the
same ranking, so the MA slice reads as a *better* slice on small caps and a *worse* one on large
caps. The queue asked: split SELECTION into the names the MA slice **adds** and the names it
**drops** at matched depth, and say which side carries the sign.

## The decomposition (exact, no modelling)

With `W^MA`, `W^Q` the two RESPREAD arms' held weights straight out of the engine and `r` the name
returns, the zero-cost book return is exactly `Σ_i W_i r_i`, so

```
gap_t = Σ_ADD  W^MA r      names only the MA slice holds
      − Σ_DROP W^Q  r      names only the depth-matched quantile slice holds
      + Σ_BOTH (W^MA−W^Q) r   shared names, at a DAILY depth mismatch
```

Gates: three-leg identity max |residual| **1.2e-16** (bar 1e-12); zero-cost identity **9.7e-17**;
reproduction of idea 305's 108 cadence-W `pairs.csv` rows across 4 columns worst |d| **3.6e-15**,
and its SELECTION leg itself to **6.7e-14** (bar 1e-9). Every one of the 27 (panel × theta) cells is
reported; 162 books, all reported.

## Answer: the DROP side carries the sign, on every panel

| panel | ADD | DROP | BOTH | SELECTION | ADD dominates | SEL>0 |
|---|---|---|---|---|---|---|
| U56 | +0.5183 | **−3.8515** | +2.8461 | −0.8863 | 0/9 | 1/9 |
| B136 | +0.6288 | **−3.4964** | +2.4218 | −0.6438 | 0/9 | 2/9 |
| SMALL439 | +0.9637 | **−1.9950** | +1.7153 | +0.7450 | 0/9 | 4/9 |

pp/yr, mean over the 9 thetas, cadence W, QUANTILE-M, zero cost.

**DROP is the larger leg in 27 of 27 cells on all three panels** (and 27/27 again on the fractional
gate QUANTILE-F, so it is not the `ceil()` rounding). The MA threshold's slice is decided by what it
**declines to hold**, not by what it buys: the ADD leg never exceeds +1.62 pp/yr anywhere, while DROP
runs to −12.78. Per name, the added names return 9.8–14.7 %/yr exposure-weighted while the dropped
names return 33–58 %/yr — dropping them always costs; the only question is how much.

**H_ADD FAILS** (0/4 positive-SELECTION SMALL439 thetas are ADD-carried).
**H_PANEL FAILS** — the dominant side is not a panel property at all; it is DROP everywhere.

## And the panel spread is a DROP-leg fact too

SMALL439 − U56, per leg: ADD **+0.4454**, DROP **+1.8566**, BOTH **−1.1307**, Jensen +0.4600, total
SELECTION **+1.6312**. The DROP leg alone is **113.8 %** of the spread. SMALL439 does not win because
its MA slice picks better names; it "wins" because the names its MA slice declines to hold ran at
11.9–15.2 %/yr in the shallow rungs instead of the 20–40 %/yr the same names ran at on U56/B136.

## The framing is depth, not panel

The theta→x map is panel-specific: theta +0.30 is x = 0.0426 (U56), 0.0401 (B136), **0.1011**
(SMALL439). Holding matched depth: nearest-x cross-panel pairs (|dx| ≤ 0.05, 25 pairs) agree on
SELECTION's sign **21/25** and on the dominant side **25/25**. Pooled `sel ~ 1+x+x²` gives R² 0.0994;
adding panel dummies gives R² 0.2081, incremental **F = 1.510 on (2,22), p > 0.05**. **H_DEPTH HOLDS**
on its pre-registered bar — but read honestly: the depth model explains only 9.9 % of cell-level
variation, so the finding is *the panel label adds nothing once depth is held*, not *depth explains
SELECTION*. The leg that does track depth is the carrying one: `DROP ~ 1+x+x²` has R² **0.5881**
(0.6713 with panel dummies), fit `DROP = −8.0984 + 17.1027x − 10.7557x²`.

## A methodological finding the record should carry

The matching pins the **mean** mask fraction, not the daily one, so the two arms hold most of the
same names at *different* weights. That shared-names leg (BOTH) is **31.5 % of the decomposed
magnitude** (U56 32.9 %, B136 29.4 %, SMALL439 32.3 %) and **|BOTH| exceeds |SELECTION| itself in 17
of 27 cells** — on U56 BOTH is +2.85 pp/yr against a SELECTION of −0.89. **"SELECTION" as published is
not a clean names statistic**; roughly a third of its magnitude is a daily depth mismatch between the
arms. Any future use of the SELECTION/LEVEL/TIMING split should publish BOTH beside it.

## Rule 8 walk-forward (IS ≤ 2016-12-31 chosen, OOS 2017+ read once)

- **WF-A (the claim):** the dominant side chosen IS holds OOS in **9/9** cells on U56 and B136 and
  **7/9** on SMALL439, per quantile family — **50/54** overall. The SELECTION *sign* holds only
  43/54. The side is the durable statement; the sign is not.
- **WF-B (book pick, IS Sharpe → OOS read once):** no arm beats RULES v2 OOS on any panel
  (best OOS Sharpe 1.1521 vs v2 1.2817). 12 of 18 beat SPY OOS (0.8786), all of them on U56/B136;
  every SMALL439 pick loses to SPY (OOS Sharpe 0.54–0.59).
- **WF-C (depth vs panel model):** OOS MAE — DEPTH 1.6917, PANEL 1.6967, zero 1.7482, pooled IS mean
  1.6729. Sign agreement 18/27 both. **Neither model beats the pooled mean out of sample**: the
  cell-level SELECTION number is not predictable from either x or the panel label.

## Both KEEP paths (10 bps, full sample, all 162 books)

**4a 0/162. 4b 10/162. BOTH 0/162.** 4b failing legs: DD 103, CAGR 82, OOS 61, H2 60, H1 60 — the
drawdown cap is still the binding leg (ideas 500/527/530). All 10 4b passers are deep rungs
(x ≥ 0.708) on U56 (8) and B136 (2); every one fails 4a. **No KEEP candidate, no memo, no RULES
change.**

## Caveats

- **SURVIVORSHIP:** B136 and SMALL439 are current constituents only (44 tickers with
  `max_1d_move ≥ 1.0` dropped from the small panel first). CAGR levels are inflated and the 4a/4b
  columns are not immune. The ADD/DROP legs are same-panel arm-minus-arm differences so the bias
  largely cancels — but the ADD side is exactly the side survivorship flatters most, and the headline
  is that ADD is *not* what carries the sign, which survivorship would bias toward the opposite
  conclusion. The finding is therefore conservative in the direction that matters.
- Cadence is fixed at W. Idea 305's published panel means pool 3 cadences and 2 quantile families, so
  the SEL column here is a subset of that pool, not a restatement of it.
- Two tuned parameters only: panel × theta. `x` is a deterministic function of theta.

## Follow-ups proposed

- 558: publish BOTH (the shared-names depth-mismatch leg) beside every SELECTION/LEVEL/TIMING split
  in the record, and re-read how many published SELECTION numbers are majority-BOTH.
- 559: re-run the matching at DAILY matched depth (`k_q ≡ k_ma` every day) and report what SELECTION
  becomes once BOTH is zero by construction.
- 560: price the DROP leg on its own as a screening statistic — the dropped-name return rate
  `rbar_drop` is a per-cell number available before any book is built.

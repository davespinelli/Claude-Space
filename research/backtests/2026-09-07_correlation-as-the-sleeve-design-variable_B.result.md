# Idea 103 — correlation-as-the-sleeve-design-variable (lane B, 2026-09-07) — **SPLIT: the curve is REAL and survives the return control; correlation is KILLED as a sleeve design variable**

**Script:** `research/backtests/2026-09-07_correlation-as-the-sleeve-design-variable_B.py`
**Artefacts:** `.console.txt`, `.grid.csv` (1,920 points), `.correlation.csv`, `.sleeves.csv`,
`.curve.csv` (1,152 interior cells), `.slopes.csv`, `.walkforward.csv`, `.preregistered.csv`

## What was run

Idea 100 has **two** sleeves. Two points define a slope by construction; they cannot say whether
the slope is monotone, where it flattens, or whether it is correlation at all rather than the
sleeve's own return. This run builds the curve.

**32 sleeves**, not 6: the queue says "adding equity ETFs back one at a time", but one order is
one path and a path is not a curve, so this runs **all 2⁵ = 32 subsets** of EQ5
(SPY QQQ IWM EFA EEM) on top of MACRO4 (TLT GLD DBC UUP), in idea 18 variant B's construction
verbatim (3-signal vote × inverse-60d-vol risk parity). Subset ∅ is idea 100's S4, the full
subset is its S9. The literal one-at-a-time ladder is labelled inside the 32 and reported
separately. Realised correlation spans **−0.011 … +0.820**, the range the queue asked for.

**Tuned parameters: exactly 2** — the sleeve (32) and f ∈ {0, 0.25, 0.50, 0.75, 1.00}. Books
(v1 / top20 / ewall), panels (u56 / B136), and blend convention (natural / gross-matched) are
reported controls, never selected on. Grid = 32 × 5 × 3 × 2 × 2 = **1,920 points, all reported**.
10 bps, weekly, t+1, gross 0.75.

**Control asserted before any number was read:** `fast_backtest` vs
`products/backtester/engine.backtest` on RULES v1 / u56 → max |diff| **0.000e+00**.
**Idea 100's endpoints reproduce exactly:** S4 to the 3 books **−0.011 … +0.212**, S9
**+0.626 … +0.820**; median conv_per_pp **0.090** (S4) and **0.031** (S9) — idea 100's published
0.090 / 0.031 to 3 decimals.

## (1) Is the relationship monotone? — **No, and the non-monotonicity is the interesting part**

Within every one of the 36 (panel × book × convention × f) cells the relationship is close to
deterministic: slope(dSharpe on corr) is **negative in 36/36** cells, slope(conv_per_pp on corr)
in **33/36**, median within-cell R² **0.92 / 0.92**, median within-cell Spearman **−0.910**.
Pooled: dSharpe = 0.254 − **0.278**·corr (t **−25.4**, R² 0.359); conv_per_pp = 0.088 − **0.081**·corr
(t **−13.0**, R² 0.129); Spearman −0.380 / −0.476.

But across the pooled **correlation deciles it is not monotone** — dSharpe falls 0.208 → 0.060
through the 6th bin, then rises to 0.078 and ends at 0.067 in the top decile. The pooled
non-monotonicity is cross-cell level heterogeneity, not noise inside a cell.

**The decay is strongly convex, which the linear slope hides.** Mean dSharpe by number of equity
ETFs added: **0.265 → 0.144 → 0.090 → 0.068 → 0.058 → 0.052**. **57.1% of the entire S4→S9 loss of
convexity is spent on the FIRST equity ETF, 82.1% by the second**; adds 3–5 are a plateau at
+0.05–0.06. The one-at-a-time ladder shows the same shape (corr 0.099 → 0.467 → 0.658 → 0.718 →
0.743 → 0.744; conv_per_pp 0.090 → 0.040 → 0.019 → 0.019 → 0.023 → 0.031).

## (2) Is it correlation, or the sleeve's own return? — **60% of it is correlation**

Adding equity ETFs raises the sleeve's standalone CAGR 2.6% → 5.0% as well as its correlation.
Controlling for the sleeve's own CAGR **and** Sharpe: the corr coefficient on dSharpe falls
−0.278 → **−0.167** (t **−9.19**), i.e. **40% of the raw slope was the sleeve's return, 60%
survives**; on conv_per_pp it barely moves, −0.081 → **−0.075** (t −7.16), a 7% attenuation.
Correlation is a genuine explanator of convexity, not a proxy for return.

## (3) Where does it stop paying? — **it never turns negative; it flattens, and 4b runs the other way**

*Convexity reading.* dSharpe stays **positive in 1,119 of 1,152** interior cells. The 33 negatives
are scattered at corr +0.418…+0.722 and do **not** form a threshold — S9 itself, at corr 0.744–0.820,
is positive again. Above corr ≈ 0.6 the curve is a plateau, not a cliff: corr > 0.50 (906 cells)
mean dSharpe **+0.0725**, median conv_per_pp **0.0316**; corr < 0.20 (30 cells) **+0.2853** / **0.0902**.

*KEEP reading — this is what kills the design variable.* Over the 1,152 interior points: 4a **2**,
4b **99**. All 99 4b passes are f = 0.25 on the top20 book, and they span corr **+0.035 … +0.820** —
**every correlation bucket passes, S9 included**. Pass rate by number of equity ETFs is flat-to-
**rising**: 5.6% / 7.2% / 8.1% / 9.2% / 10.0% / **11.1%**. The KEEP path is ordered in the *opposite*
direction to the convexity metric, because 4b's binding bar here is the CAGR floor and equity ETFs
bring CAGR. **A design variable that orders the diagnostic and anti-orders the bar is not a design
variable.**

## (4) PROTOCOL rule 8 — walk-forward (REQUIRED, run)

(sleeve, f) chosen **jointly** on 2009–2016 by IS Sharpe over 160 arms per cell, 2017–2026 untouched.

- Picks f = 0 (no sleeve) in **0/12** cells; beats its own no-sleeve anchor OOS in **12/12** and
  SPY OOS in **12/12**; beats the live RULES v2 OOS in only **4/12**; mean regret **−0.118**;
  **4b at the pick: 0/12**.
- Best pick — u56 / top20 / natural / **S4 at f = 0.50**: OOS **CAGR 8.9%, Sharpe 1.308, MaxDD −10.0%**
  vs anchor 1.168, RULES v2 OOS **1.285** (9.5%, −12.1%) and SPY OOS **0.882** (15.5%, −33.7%).
  Full sample: 7.7% / **1.192** / −10.0%, halves 1.104 / 1.274 — **fails 4a** (Sharpe below RULES v2's
  1.226 in H1) and **fails 4b** (CAGR 7.7% against the 10.66% floor).
- The IS chooser lands on a low-correlation sleeve (S4 or S4+QQ) in 8/12 cells — but
  **pre-registering the lowest-correlation sleeve** (S4 fixed, zero fitting on the sleeve axis)
  **beats the free sleeve choice OOS in only 1/12 cells, mean −0.0915**. So even the one actionable
  use of the curve loses money out of sample.

## Verdict — **SPLIT. Curve CONFIRMED; correlation KILLED as a sleeve design variable. No KEEP, no PARK.**

The queue's regression exists, is highly significant, holds inside every cell, and survives the
sleeve-return control. It is also useless for building a book: the convexity it orders does not
transfer to either KEEP path (4b 0/12 at the rule-8 pick, 4a 2/1920 over the whole grid), the 4b
pass rate runs the other way, and pre-registering on it loses 0.09 of OOS Sharpe in 11 of 12 cells.
The actionable content is negative and cheap: **57% of the diversification is gone after one equity
ETF**, so a sleeve is either non-equity or it is not a sleeve — there is no useful interior.

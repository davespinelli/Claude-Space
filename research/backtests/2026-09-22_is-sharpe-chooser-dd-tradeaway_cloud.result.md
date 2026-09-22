# Idea 960 — does the IS-Sharpe chooser's `L4_DD` OOS failure generalise?

**2026-09-22, lane cloud, run 12.** Script `2026-09-22_is-sharpe-chooser-dd-tradeaway_cloud.py`.
720 book cells (3 panels x 6 gross rungs x 5 widths x 2 cadences x 4 cost rungs) and 576 chooser
cells published. 5 of 5 gates exact; G3 reproduces idea 951's two committed headline cells to
**3.3e-03** (u56 g=0.75 M 10 bps: TOP20 OOS 16.68% / 1.2837 / −19.51%, TOP10 OOS 17.30% / 1.1003 /
−23.22% against 951's 16.67% / 1.283 / −19.51% and 17.20% / 1.097 / −23.20%).

## ANSWERED = PARTIAL. The DIRECTION generalises; the TRADE does not.

**951's trade is a POINT, not a law.** Its cell read *+3.69 pp of drawdown bought with +0.53 pp of
OOS CAGR*. Pooled over C_SHARPE's 144 chooser cells, its pick is deeper out of sample than the
no-information control (fixed width 20) at **55.6%** — a coin flip — and the median move is
**−1.34 pp of MaxDD for −0.49 pp of OOS CAGR**. At the median the habitual chooser does not *buy*
return with drawdown; it gives up **both**. **KILL of the trade as a general fact.**

**What does generalise is the weaker and more useful claim: the habitual chooser is worth less
than its own default.** Over the same 144 cells:

| chooser | L4_DD OOS pass | 4b FULL pass | 4b OOS pass | 4a pass | abstentions |
|---|---|---|---|---|---|
| C_SHARPE (habitual) | **31.9%** | **2.8%** | 3.5% | 0.0% | 0 |
| C_CALMAR | 34.7% | 3.5% | 4.9% | 0.0% | 0 |
| **C_DDB060** (idea 2264's device) | **83.9%** | **16.1%** | 16.1% | 0.0% | **82 of 144** |
| C_LIVE (no information, width 20) | 36.8% | 6.2% | 8.3% | 1.4% | 0 |

The habitual IS-Sharpe chooser **halves** the no-information control's 4b pass rate (2.8% vs 6.2%)
and loses the DD leg 4.9 pp more often. This is idea 953's "a free parameter is worth less than
its default" reproduced on the WIDTH dial, and it is the third dial on which it now holds.

## The mechanism, and where the effect actually lives

Width is a strong drawdown dial and a weak Sharpe dial, so an IS-Sharpe argmax over it is mostly
selecting noise onto an axis that matters out of sample:

| width | median OOS MaxDD | median OOS CAGR | median OOS Sharpe | median IS Sharpe | L4_DD OOS rate |
|---|---|---|---|---|---|
| 5 | −35.13% | 11.51% | 0.7162 | 0.8572 | 22.9% |
| 10 | −28.40% | 12.00% | 0.7925 | 0.8747 | 31.9% |
| 20 | −26.23% | 10.37% | 0.8635 | 0.9199 | 36.8% |
| 40 | **−23.71%** | 8.17% | 0.9916 | 0.9201 | **43.1%** |
| ALL | −26.61% | 7.57% | 0.9549 | 0.9248 | 35.4% |

Pooled median IS Sharpe moves **0.068** across the whole width axis while median OOS MaxDD moves
**11.4 pp**; within a single (panel, gross, cadence) cell the IS-Sharpe spread across widths is
0.212 at the median against a 9.17 pp OOS MaxDD spread. Same shape as idea 2264's gross result —
a dial the chooser's statistic barely sees, and the drawdown cap pays for it.

**It is panel-driven, and the run says so rather than pooling it away.** C_SHARPE's pick is deeper
than the incumbent at **100% / 87.5% of small-panel cells** (median −2.17 to −4.95 pp), **50% on
u56** (median −1.58 to −5.83 pp) and at **25% / 12.5% on b136 with a median of exactly 0.00 pp** —
because on b136 at monthly cadence the chooser picks width 20, i.e. it IS the incumbent. The
chooser is also not a systematic ladder-end taker: it picks the NARROWEST rung (5) on u56-monthly
and the WIDEST (ALL) on small, at every gross rung.

**Gross does not move it.** The trade-away share is flat in gross on every panel (b136 0.250 at
g ≤ 1.00 and 0.125 at 1.25/1.50; small 1.000 then 0.875; u56 0.500 throughout), so the queue's
0.25–1.50 ladder is not where this effect lives.

## No new KEEP

- Book-level base rates over all 720 cells: **4a 5, 4b 34, 4b OOS 46, BOTH 0.**
- Four of the five 4a passes are at the **0 bps** rung; the only one surviving 10 bps is
  b136 / g=0.25 / width 40 / M (4.60% / 1.0960 / −8.39%), which fails 4b on the CAGR floor.
- **Every one of the 240 small-panel cells fails 4b**, on the most survivorship-flattered panel of
  the three.
- Binding legs over the 686 4b FAIL cells: **L4_DD 475**, L2_H2 382, L3_OOS 376, L5_CAGR 367,
  L1_H1 326 — on this shelf the DD cap is the largest binder, unlike the record's record-wide
  count where the CAGR floor dominates.

## Caveats

- **Survivorship (PROTOCOL rule 9 / idea 54):** u56 and b136 are 2026 constituents held from 2008;
  the small panel is the CURRENT sub-$2B screen (665 names after dropping the 54 tickers with
  `max_1d_move >= 1.0` per `data/small_meta.csv`), so its CAGR levels are the most optimistic of
  the three and its 4b level legs the easiest — and it still passes 4b nowhere.
- Gross rungs above 1.00 are levered with **no financing charge modelled**; every headline is also
  reported on the unlevered sub-ladder g ≤ 1.00, where C_SHARPE's trade-away share is 58.3% and
  its median move −1.34 pp of MaxDD for −0.44 pp of CAGR — the same reading.
- Costs are flat per unit turnover (no spread, impact, borrow) and enter by the exact affine
  identity `r(c) = r(0) − turnover·c/1e4`, gated at 0.000e+00. Execution t+1 throughout.
- C_DDB060's 83.9% is bought with a **57% abstention rate** (82 of 144 cells, by panel 21/48 u56,
  25/48 b136, 36/48 small): it is a conservative device, not a better argmax.
- This run proposes no rules change; PROTOCOL rule 6 gives that to the Sunday review.

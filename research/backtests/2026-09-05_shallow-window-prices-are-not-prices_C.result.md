# idea 128 — shallow-window-prices-are-not-prices (lane C, 2026-09-05)

**ANSWERED. Double KILL: the queue's premise is a tautology of the priceability filter, and the
depth threshold it asked me to locate does not exist anywhere in the observable range.**

Script: `2026-09-05_shallow-window-prices-are-not-prices_C.py` · console:
`…_C.console.txt` · data: `.windows.csv` (1,640 rolling windows), `.grid.csv` (45 points),
`.deciles.csv`, `.perbook.csv`, `.lengthmatched.csv`, `.rule8windows.csv`, `.troughs.csv`,
`.pricelist.csv`, `.reproduction.csv`, `.walkforward.csv`.

## 0. Reproduction (exact)

Idea 94's harness imported unchanged; `H.run` with every instrument off equals
`engine.backtest` to **max|diff| 0.000e+00** on both panels. Idea 122's published counts
reproduce to the row: **192 arm-rows, 138 priceable, dMaxDD_IS ≤ 0 in 40, dMaxDD_OOS ≤ 0 in 0,
4a 54/192, 4b 29/192.** So this run audits the same file, not a re-derivation.

## 1. The premise is a tautology (KILL 1)

The queue reads `40 IS vs 0 OOS` as evidence that a shallow window cannot measure a drawdown
instrument. It is not. `published` conditions on **dMaxDD_full > 0.10 pp**, and the full-sample
MaxDD of these books is attained inside the OOS window:

| | arms whose full-sample trough is in 2017-2026 |
|---|---|
| universe.json(56) | 51 of 52 (V1u 16/17, TOP20 17/17, EWall 17/17, SPY 1/1) |
| universe_broad.json | 52 of 52 |

Consequently **dMaxDD_full == dMaxDD_OOS exactly in 132 of the 138 published rows**
(corr 0.998; corr with dMaxDD_IS 0.755). Filtering on `dMaxDD_full > 0.10` *is* filtering on
`dMaxDD_OOS > 0`, so the 0-of-138 is arithmetic, not measurement. Unconditionally, at 10 bps
over all 96 arm-rows: **dMaxDD_IS > 0 in 58, dMaxDD_OOS > 0 in 71, dMaxDD_full > 0 in 71** —
the same 71. The real IS/OOS gap is 60% vs 74%, not 71% vs 100%.

## 2. The 90% crossing does not exist (KILL 2)

1,640 rolling windows (L ∈ {2,3,4,5,6}y, monthly starts, both panels), each scored by its own
SPY MaxDD (`depth`) and by the share of the 51 arms per panel with dMaxDD > 0 (`frac`).

* **frac rises with depth** — pooled L=4 deciles: 0.63 / 0.60 / 0.54 / 0.51 / 0.63 / 0.67 /
  0.57 / 0.70 / 0.68 / 0.69 across depth 9.7 → 33.7 pp. Slope +0.0051/pp, t **+7.07**, R² 0.13.
* **but the significance is an overlap illusion.** On the disjoint subset (step = L) the same
  slope carries t **+0.04** (pooled L=4); across the 15 (L, scope) fits t_disj > 2 in exactly
  one (u56, L=5, n=3). P1 is **not** supported under honest inference.
* **and it never reaches 0.90.** Empirical crossing is undefined at **45 of 45** grid points.
  Max `frac` over all 1,640 windows is **0.833**; 0 of 328 L=4 windows reach 0.90, 1.5% reach
  0.80. The fitted extrapolation puts the L=4 / p*=0.90 crossing at **77.5 pp** of SPY drawdown
  pooled (u56 57.2, broad 144.8) — deeper than 2008's −55% and than anything in the sample.
  At the looser p*=0.80 the fitted crossing is still 44.9–65.3 pp across L.
* **length does not substitute for depth.** Holding depth in a 28–35 pp band, `frac` moves
  0.661 → 0.708 as L goes 2 → 6 y. Rule 8's own 9.7-year OOS half (depth 33.7 pp) scores
  0.750 / 0.729; its 8-year IS half (22.1 pp) scores 0.583 / 0.625.
* **P3 confirmed in level, not in slope.** At L=4 the fitted frac at 22.1 pp depth is V1u
  0.451 / EWall 0.682 / TOP20 0.720; V1u's fitted 90% crossing is 82.98 pp vs EWall's 64.33.
  The 5-name book is unpriceable at every depth, which is idea 122's own address for the
  cost- and panel-axis failures.

## 3. Rule 8 (walk-forward, selection on 2009–2016 only)

S0 = hold the control; S1 = idea 94's selector (lowest IS rate among arms buying ≥ 1.0 pp) on
the full IS half; S2 = the same selector on the **deepest L-year sub-window inside IS**.

| L | S0 OOS Sharpe / CAGR / MaxDD | S1 | S2 |
|---|---|---|---|
| 2 | 0.937 / 12.04% / −22.5% | 0.885 / 9.92% / −19.0% | 0.839 / 9.24% / −19.3% |
| 3 | " | " | 0.885 / 9.16% / −18.3% |
| **4** | **0.937 / 12.04% / −22.5%** | **0.885 / 9.92% / −19.0%** | **0.885 / 9.16% / −18.3%** |
| 5 | " | " | 0.872 / 9.81% / −19.3% |
| 6 | " | " | 0.838 / 9.35% / −18.2% |

Benchmarks OOS 2017–2026: RULES v1 **7.73% / 0.747 / −13.8%**, SPY **15.45% / 0.882 / −33.7%**.
S1 and S2 pick different arms in **13 of 30** cells and S2 is never better in the mean — the
depth clause changes picks without buying anything. **No selector beats doing nothing (S0).**
The mechanism is visible: the deepest IS sub-window has depth **22.062 pp for every L from 2 to
6**, identical to the whole IS half, because SPY's 2009–2016 maximum is the post-warm-up tail of
the GFC. Inside rule 8's IS window a deeper ruler cannot be bought at any length.

## 4. KEEP paths

Both evaluated on all 192 arm-points: **4a 54, 4b 29** — idea 122's numbers unchanged
(u56: EWall 7/8, TOP20 1/15, V1u 0/0; broad: EWall 26/6, TOP20 20/0, V1u 0/0). Every passer is
an already-published gated `TOP20`/`EWall` arm. **No new KEEP candidate**; this run tests a
publication rule, not a book. Live RULES untouched.

## 5. Caveats

Survivorship: both panels are current-constituent lists, so absolute levels are optimistic; the
reported quantity is the stability of a sign, which is far less exposed, and a survivorship-free
panel would deepen every drawdown — moving the crossing, not the direction. With BTC/ETH excluded
(`baseline.EXCLUDE`) both panels load on a **trading-day** index (3,679 one-day / 846 three-day
gaps), so idea 38's calendar-day defect does not bite this run. Overlapping windows are reported
alongside the disjoint subset precisely because the overlapping t-stats are not inference.

# Idea 360 — price the U56 EWALL MA band at b=0.12 on its own (cloud, 2026-09-07)

**Script:** `2026-09-07_price-the-U56-EWALL-MA-band-at-b012-on-its-own_cloud.py`
**Verdict: KEEP-candidate (path 4b, U56, RESPREAD b=0.12 g=0.75) — grid-edge flag CLEARED;
4a KILL 0/540; and a KILL of the obvious follow-on (widening the LIVE band is harmful).**

## What was asked

Idea 359's by-product (hold every U56 name inside the 200d ±12% band at g/N, g=0.75,
weekly) was measured *inside a census*, not priced. The queue asked for a b × gross
sweep, a breakeven c*, and — before anything else — clearance of idea 240/256's
grid-edge flag, because the census's band ladder was monotone in b out to its widest
point (0.12).

## Design

Two tuned parameters only: **b** ∈ {0.00, 0.03, 0.05, 0.08, 0.12, 0.16, 0.20, 0.25, 0.30,
0.40, 0.50, 0.70} and **gross g** ∈ {0.50, 0.60, 0.75, 0.85, 1.00}. Reported (untuned)
axes: weighting convention, panel, cost rung.

The **convention** axis is the addition that made the run decisive:

| | weight on a kept name | realised gross |
|---|---|---|
| `RESPREAD` | g / k_t (k_t = names in band) | ≈ g always |
| `DEGROSS` | g / N_t (N_t = names priced) — gated weight → cash | ≈ 0.51–0.53 at g=0.75 |

`DEGROSS` **is** `baseline.rules_v2_weights` (gated equal at 0.000e+00), so RULES v2 sits
*inside this grid* at (DEGROSS, b=0.03, g=0.75) and the b ladder answers "should the live
band be wider?" directly.

**Gates 4/4:** `fast_backtest` vs `engine.backtest` 0.000e+00 (returns and turnover);
derived 25-bps rung vs a direct `cost_bps=25` run 0.000e+00; DEGROSS arm ==
`rules_v2_weights` 0.000e+00 on 3 (b,g) cells; and all 5 committed U56 MAB-EWALL rows of
idea 359 reproduced on 8 columns at **7.105e-15**.

## [B] The grid-edge flag is CLEARED

Pushing b from the census's 0.12 to 0.70 turns the curve over immediately: on
**U56/RESPREAD the argmax is b = 0.12 in 15 of 15 (g × rung) cells and INTERIOR in all
15** — Sharpe@10 runs 1.0909 → 1.1609 → 1.1548 → 1.1780 → **1.2264** → 1.1619 → 1.1367 →
1.1102 → 1.1233 → 1.1811 → 1.1165 → 1.0504 across the b ladder. 85 of 90
(panel × conv × g × rung) argmaxes are interior; the 5 that are not are B136/DEGROSS at
0 bps on the b=0 low edge, not this idea's arm.

Two honest caveats on the shape: the U56 curve is **bimodal**, with a second local peak at
b=0.40 (1.1811) only 0.045 below the b=0.12 peak and a trough of 1.1102 between them; and
**U56/DEGROSS peaks at b=0.03 in 15/15 cells** — the live rules' band width is already the
optimum *under the live convention*.

## [F] The headline, priced (U56)

| cell | CAGR | Sharpe | MaxDD | H1 / H2 | OOS Sharpe | turnover | c*_4b | 4a | 4b |
|---|---|---|---|---|---|---|---|---|---|
| **RESPREAD b=0.12 g=0.75** @10bps | **14.02%** | **1.2264** | −19.42% | 1.2611 / 1.2048 | **1.2662** | 1.93×/yr | **123.7 bps** | no | **PASS** |
| same @0 bps | 14.24% | 1.2440 | −19.35% | 1.2775 / 1.2233 | 1.2845 | 1.93×/yr | 123.7 | no | PASS |
| same @25 bps | 13.69% | 1.2000 | −19.53% | 1.2363 / 1.1769 | 1.2389 | 1.93×/yr | 123.7 | no | PASS |
| parent RESPREAD b=0 g=0.75 @10 | 11.55% | 1.0909 | −18.65% | 1.1669 / 1.0366 | 1.1118 | 7.62×/yr | 20.5 | no | PASS |
| RULES v2 = DEGROSS b=0.03 g=0.75 @10 | 8.66% | 1.2056 | −12.05% | 1.2259 / 1.1908 | 1.2851 | 1.78×/yr | **0.0** | — | fail CAGR |
| DEGROSS b=0.12 g=0.75 @10 | 8.72% | 1.1515 | −12.15% | 1.2326 / 1.0783 | 1.1765 | 0.92×/yr | 0.0 | no | fail CAGR |
| SPY | 15.23% | 0.8890 | −33.72% | 0.9566 / 0.8340 | 0.8820 | — | — | — | — |

The queue's number survives pricing exactly, and the band buys **+0.135 of Sharpe, 3.9×
less turnover and 6× the cost cushion** over its own b=0 parent. `c*_4b = 123.7 bps` is
the largest breakeven of any U56 cell with Sharpe > 1.15: the KEEP survives 12× PROTOCOL's
cost assumption.

## The KILL inside the same grid: do NOT widen the live band

Moving the live rules' band 0.03 → 0.12 **under the live de-gross convention** costs
**−0.054 of Sharpe** (1.2056 → 1.1515), −0.109 of OOS Sharpe (1.2851 → 1.1765) and buys
+0.06 pp of CAGR. The headline's advantage is **not the band width — it is the
convention**: RESPREAD deploys 0.750 of NAV against DEGROSS's 0.509, and that is where the
+5.3 pp of CAGR comes from. The convention delta is itself a function of b and **flips
sign at b ≈ 0.05** on all three panels (U56 dSharpe +0.045 at b=0.03, −0.075 at b=0.12):
at a narrow band the gate fires often and de-grossing to cash is real timing; at a wide
band it fires rarely and de-grossing just idles capital.

## [D] KEEP paths, all 360 cells × 3 rungs

**4a: 0 of 180 on U56 at every rung** (0 of 540 cell-rungs) — nothing here beats the live
book, exactly as the queue expected. (B136/DEGROSS passes 4a in 10–12 of 60 and
SMALL439/DEGROSS in 11–18 of 60, but those compare a panel's book to *that panel's* RULES
v2, not to the live U56 book.)

**4b @10 bps: 33 of 360** — U56 12/60 RESPREAD + 7/60 DEGROSS, B136 9/60 + 5/60,
**SMALL439 0/120 at every rung**. Binding bars on U56 are `DD` 36 and `CAGR` 12 under
RESPREAD, and `CAGR` 53 of 60 under DEGROSS: the de-gross convention fails 4b almost
everywhere by not deploying enough capital, and the respread convention fails it by
drawing down too far. The best DEGROSS passer (b=0.03, g=1.00: 11.59%, 1.2054, −15.91%,
OOS 1.2844, c* 45.5) has a smaller drawdown and a higher OOS Sharpe than the headline but
2.4 pp less CAGR and a third of the cost cushion.

## [E] Rule 8 walk-forward — (b, g) chosen on ≤2016, read once on 2017–2026

U56 @10 bps:

| arm | conv | b | g | IS Sharpe | OOS Sharpe | OOS CAGR | OOS MaxDD |
|---|---|---|---|---|---|---|---|
| plain IS-Sharpe pick | DEGROSS | 0.40 | 0.50 | 1.2650 | 1.1930 | 4.01% | −4.88% |
| **4b-aware IS pick** | RESPREAD | 0.12 | 0.85 | 1.1766 | **1.2661** | 17.23% | −21.80% |
| headline | RESPREAD | 0.12 | 0.75 | 1.1762 | **1.2662** | 15.16% | −19.42% |
| OOS-best (regret 0) | DEGROSS | 0.03 | 0.50 | 1.1037 | 1.2856 | 6.32% | −8.12% |
| b=0 parent | RESPREAD | 0.00 | 0.75 | 1.0669 | 1.1118 | 12.43% | −18.65% |
| RULES v2 (live) | — | — | — | 1.1043 | 1.2851 | 9.53% | −12.05% |
| SPY | — | — | — | 0.8986 | 0.8820 | 15.45% | −33.72% |

The b dial **walks forward on U56**: b=0.12 is the IS pick under the 4b-aware screen at
every rung and its OOS regret is 0.0194, against 0.1739 for the do-nothing parent.

The plain IS-Sharpe chooser is **actively harmed by the convention axis**: it buys the
low-gross defensive corner (DEGROSS b=0.40 g=0.50, IS 1.2650) and gives up 0.093 of OOS
Sharpe and 11 pp of OOS CAGR for it. This is the record's cleanest instance yet of the
4b-aware screen earning its keep (ideas 152/163). Caveat: the IS 4b screen is not a
full-sample guarantee — at 10 bps it admits g=0.85, whose *full-sample* MaxDD (−21.80%)
breaches the 4b DD cap it passed in-sample.

## Honest limits

1. The headline does **not** dominate the live book: OOS Sharpe 1.2662 < RULES v2's
   1.2851. It wins on CAGR (15.2% vs 9.5%) and loses on drawdown (−19.4% vs −12.1%). It
   is a growth substitute, not an upgrade on every axis.
2. It is **not unique**: 12 of 60 U56 RESPREAD cells clear 4b at 10 bps, the b=0 parent
   among them. Its distinction is the argmax position plus the cost cushion.
3. It does **not generalise**: at b=0.12/g=0.75 it fails 4b on B136 (DD −21.74% vs the
   −20.23% cap) and 0 of 120 SMALL439 cells pass at any rung.
4. **SURVIVORSHIP:** B136 and SMALL439 are *current* constituents of their screens and are
   biased upward; U56 carries the same caveat more weakly. No number here is a live
   expectation.
5. Sharpe is invariant in g to ~4 decimals — g is a pure risk scalar, so this is
   effectively a one-dial book plus a leverage choice, and the 4b DD cap is what picks g.

## Artefacts

`.grid.csv` (360 cells × 3 rungs, every point), `.edge.csv` (90 argmax rows), `.ctx.csv`,
`.keeppaths.csv`, `.walkforward.csv`, `.console.txt`, and `_MEMO.md` (the KEEP wording).

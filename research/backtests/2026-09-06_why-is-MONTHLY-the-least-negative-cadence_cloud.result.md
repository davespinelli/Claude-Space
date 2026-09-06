# Idea 302 — why-is-MONTHLY-the-least-negative-cadence-for-the-de-gross-timing-residual (cloud, 2026-09-06)

**Verdict: ANSWERED / KILL of the cadence reading. Monthly is the least negative rung because
month-end is a lucky PHASE, not because a monthly dial times exposure better. Once the phase is
integrated out the M-vs-Q gap is gone (7% / −13% / −37% of its published size) and the residual
has no consistent cadence ordering at all. Rules unchanged; no KEEP (4a 1/360, 4b 40/360, and
the rule-8 pick is not one of the 40).**

Script `2026-09-06_why-is-MONTHLY-the-least-negative-cadence_cloud.py`, 1440 backtests
(3 panels × 2 gates × 6 bands × 2 constructions × 20 phase-runs) scored at 0 and 10 bps, plus 15
no-filter controls, the live book and SPY. 146s, deterministic.

## Controls, asserted before any new number was read
| | bar | result |
|---|---|---|
| [a] vectorised backtester vs `engine.backtest`, 12 books | < 1e-12 | returns **5.9e-17**, held gross **1.6e-15** — HOLDS |
| [b] `cad_mask(W/CAL-M/CAL-Q, phase 0)` == `engine.rebalance_mask` | exact | HOLDS on all 3 panels |
| [c] B0: reproduce idea 297's committed `.decomp.csv` | < 1e-6 | **432 of 432 rows**, worst \|diff\| **8.9e-14** — HOLDS |
| [d] identity `r_dg,t ≡ c_t·r_rs,t` at 0 bps, 720 pairs | < 1e-12 | **5.6e-17** — HOLDS |
| [e] k=1 negative control (W, CAL-M, CAL-Q): MEANPH == PH0 | 0.0 | **0.0e+00** — HOLDS |

So this run measures idea 297's quantity, at idea 297's points, plus the block twins 4W (4
phases) and 13W (13 phases) that idea 297 never ran.

## The five pre-registered readings
| | bar | SMALL439 | U56 | B136 | reading |
|---|---|---|---|---|---|
| **A1** phase range ≥ published M−Q gap (13W) | ≥2/3 panels | 0.846 vs 0.562 | 1.073 vs 0.445 | 1.063 vs 0.365 | **3/3 — phase spread is 1.5–2.9× the effect** |
| **A2** phase-averaged 4W−13W gap ≥ 0.5×gap | 3/3 panels | +0.041 (**7%**) | −0.057 (**−13%**) | −0.134 (**−37%**) | **0/3 — the gap does not survive, and reverses sign on two panels** |
| **A3** CAL-M in the top half of its 4W phases, CAL-Q in the bottom half of its 13W | ≥2/3 each | M rank **1**/4, Q **9**/13 | M **2**/4, Q **12**/13 | M **2**/4, Q **13**/13 | **3/3 and 3/3 — calendar luck** |
| **A4** 4W cells non-negative at EVERY one of their 4 phases | 0 ⇒ phase draw | — | — | — | **0 of 36 — the sign anomaly is a draw** |
| **A5** MEANPH(IS) beats PH0(IS) on OOS MAE | ≥2/3 panels | 0.616 vs 0.605 | **0.251 vs 0.267** | **0.504 vs 0.587** | **2/3 — averaging is the better estimator** |

## What the numbers say
1. **The published ordering is an alignment draw.** Idea 297's M (−0.184 / −0.072 / −0.302 pp/yr)
   and Q (−0.745 / −0.517 / −0.666) are single phases of a 4-week and a 13-week block. Sweeping
   every phase, the panel-mean residual runs −0.84…−0.33 (4W) and −1.00…+0.36 (13W) on
   SMALL439/U56/B136 — a range of 0.51–0.60 and 0.85–1.07 pp/yr against a published M−Q gap of
   only 0.56 / 0.44 / 0.36. The dial is being read inside its own noise.
2. **Month-end is a good phase and quarter-end a bad one, on all three panels.** CAL-M ranks 1st
   or 2nd of its 4 phases everywhere; CAL-Q ranks 9th, 12th and 13th of 13. That is one fact —
   calendar alignment — masquerading as a cadence-length effect.
3. **Phase-averaged, the cadence effect is gone and its sign is not stable.** MEANPH residuals
   (FULL): SMALL439 W −0.273 / 4W −0.600 / 13W −0.641; U56 W −0.310 / 4W −0.225 / **13W −0.168**;
   B136 W −0.489 / 4W −0.417 / **13W −0.282**. Weekly is the least negative rung on the small
   panel and the MOST negative on both large panels. There is no cadence ordering to publish.
   OOS (2017–) says the same: 13W is the least negative rung on U56 (−0.131) and B136 (−0.466).
4. **The 6 non-negative cells were phase luck.** All 6 are CAL-M. At 4W, 12 of 36 cells are
   non-negative at phase 0 and 13 at some phase, but **0 of 36 at every phase**; the three that
   survive MEANPH (U56/MAVOL, b = 0.00/0.02/0.03) have a phase range of 0.54–0.72 pp/yr around a
   mean of +0.28…+0.39, i.e. they are means of a spread that straddles zero.
5. **What DOES survive is idea 297's headline, unchanged:** the residual is negative nearly
   everywhere and phase-averaging makes it MORE negative on the block points (SMALL439 4W
   −0.78 → −0.60 is the one direction it moves the other way; U56 4W +0.07 → −0.23, B136
   −0.13 → −0.42). De-grossing still times its own exposure badly; it just does not do so as a
   function of cadence length.
6. **Estimator upgrade, rule 8.** Predicting a cell's OOS phase-averaged residual from its IS
   value, phase averaging beats the single-phase reading on 2 of 3 panels (U56 0.251 vs 0.267,
   B136 0.504 vs 0.587) and both beat the naive zero on 2 of 3. Every future cadence claim about
   the residual should be read at MEANPH, not phase 0.

## KEEP paths (10 bps, MEANPH collapse, 360 cells)
**4a 1/360, 4b 40/360.** All 40 4b passers are RESPREAD (no de-grossing) on U56 and B136 — the
already-published equal-weight-above-the-band family (idea 298/299's parked candidate), not a new
construction; best is U56/MA/W/b=0.12 at 14.09%/**1.2330**/−19.36% (OOS 1.2723). No DEGROSS cell
passes 4b anywhere.

**Walk-forward (rule 8, (band, cadence) chosen on IS Sharpe inside each of 12 panel × gate ×
construction arms, 2017– read once):** OOS beats SPY in 16/24 arms, the live RULES v2 book in
**0/24**, the matched no-filter control in 14/24. Critically the IS-chosen U56/MA/RESPREAD arm is
CAL-Q b=0.02 → OOS 12.87%/1.0843/−21.78%, which **fails 4b on the drawdown cap** (−21.8% vs the
−20.2% bar); the 40 passers above are hindsight cells, not choosable ones. The two collapses pick
the same cadence point in only 7/12 arms, and MEANPH's picks are worth +0.0080 of mean OOS Sharpe.

## Caveats
Costs 10 bps, next-day execution, 75% gross, no shorting or leverage. SURVIVORSHIP: all three
panels are current constituents (prices_small.csv is today's sub-$2B screen with the 44
`max_1d_move >= 1.0` names dropped; universe(_broad).json are today's large caps/ETFs); the
residual is an arm-minus-arm contrast on identical names and days so the bias very largely
cancels there, but it does NOT cancel from the 4a/4b level columns. Phase is integrated out, not
chosen: no result here is a tradable claim about picking a rebalance date.

# Idea 1660 (lane C, 2026-09-19) — does the BAND's GATE-OUT RATE predict a panel's REALISED GROSS well enough to RETIRE the BISECTED TWIN?

**VERDICT: KEEP (method) with a STATED BOUNDARY.** The closed form replaces the 44-step bisection
for a SAME-SLICE matched-exposure contrast — 0 of 540 KEEP-verdict flips, max |dSharpe| 0.000496,
max |dMaxDD| 0.56 pp, both an order of magnitude inside the pre-registered bars. It does NOT
replace it where an IS-FIT k is read OOS onto a 4b drawdown verdict already inside its own noise:
**2 of 27 chooser rows flip, on a DD margin of 0.11 pp against idea 1511's own 2.93 pp SE.**

Script: `2026-09-19_band-gate-out-rate-predicts-realised-gross_C.py` — 695s, offline, deterministic,
**12/12 gates PASS**. Dials: band c {0.00, 0.01, 0.03, 0.05, 0.10} x gross G {0.25, 0.50, 0.75, 1.00}
= 20 cells (rule 4: two tuned parameters). Published, not dials: PANEL {U56, B136, SMALL} x CADENCE
{W, M, Q} x SLICE {FULL, IS, OOS} x COST {0, 10, 25, 50} bps = **8640 published rows**.

## Q0 — THE FORM. 1649's 0.75x proportionality is REAL but it is a WEEKLY fact, not a law.

Ratio `R / (G * mean s)` over 540 (panel, cadence, cell, slice) points:

| panel | mean | min | max |
|---|---|---|---|
| U56 | 0.998846 | 0.975495 | 1.015020 |
| B136 | 0.997280 | 0.978386 | 1.011462 |
| SMALL | 1.005391 | 0.989744 | 1.030015 |

So 1649 was not reading a coincidence: realised gross **is** target gross times the in-band share,
to within 3% at the worst point in the record and to within 0.12% on the live weekly cadence.
But the residual is **monotone in the rebalance interval**, and steeply:

| cadence | FORM A mean abs residual | max abs residual |
|---|---|---|
| W | **0.0253 pp** | 0.1253 pp |
| M | 0.1504 pp | 0.8869 pp |
| Q | 0.4137 pp | **1.7249 pp** |

FORM A (`R_hat = G * mean s`, zero runs): mean −0.0258 pp, mean abs 0.1964 pp, max abs 1.7249 pp
(U56/Q, c=0.03, G=1.00, IS). FORM B (`R_hat = mean of the HELD target path`, also zero runs) trades
bias for tail: mean **+0.1638 pp** (it is biased, not centred) but max abs only 0.6437 pp. The gap
between them is exactly the stale-weight effect, and it is the whole cadence term.

## Q1 — THE TWIN, PRICED. The substitution is invisible at every cost rung.

Pre-registered bars, fixed before the run: |dSharpe| < **0.0089** (idea 1617's smallest committed
device margin) and |dMaxDD| < **2.93 pp** (idea 1511's measured paired circular-block SE).

| twin | slice | max abs dSharpe | max abs dMaxDD | max abs dCAGR | cells |
|---|---|---|---|---|---|
| TWIN_R (`k = R_cell`) | FULL | 0.000096 | 0.2108 pp | 0.1241 pp | 180 |
| TWIN_R | OOS | 0.000169 | 0.2295 pp | 0.1392 pp | 180 |
| TWIN_A (`k = G * mean s`) | FULL | 0.000233 | 0.5539 pp | 0.3345 pp | 180 |
| TWIN_A | OOS | **0.000496** | **0.5632 pp** | 0.3329 pp | 180 |

Stable across 0 / 10 / 25 / 50 bps (max abs dSharpe 0.000504 / 0.000496 / 0.000484 / 0.000463).
Target-gross error itself: mean |k_A − k_bisect| 0.0028, max 0.0217; |k_R − k_bisect| mean 0.0021,
max 0.0074. **VERDICT FLIPS, same slice: 0 of 540 on 4a and 0 of 540 on 4b, for BOTH substitutions.**

## THE BOUNDARY — where the formula is NOT safe, stated in full.

Rule 8 solves the twin on IS rows and reads it OOS. There the 1.5 pp of gross the formula adds is
enough to tip a knife-edge verdict: **U56 quarterly, band 0.00, G 1.00**, picked by BOTH C_SHARPE
and C_MEMO.

| book | k fit on IS | OOS CAGR | OOS Sharpe | OOS MaxDD | 4b |
|---|---|---|---|---|---|
| TWIN_BISECT | 0.689525 | 12.98% | 1.1708 | **−20.118%** | **PASS** |
| TWIN_R | 0.693907 | 13.07% | 1.1707 | −20.240% | FAIL |
| TWIN_A | 0.704109 | 13.26% | 1.1705 | −20.523% | FAIL |

The 4b DD cap is −20.230%. The bisected twin passes by **0.11 pp**, which is **1/27th of the
2.93 pp SE the record itself measured for a MaxDD contrast**. This is not a formula failure — it is
a verdict that was never adjudicable. Published as the boundary condition, not buried.

## Q2/Q3 — CAPITAL ARM (real books, both KEEP paths, rule 8)

4b pass counts at 10 bps, out of 180 cells: CELL 13 FULL / 11 OOS; every twin family 2 FULL / 3 OOS.
**11 of 180 CELL books clear 4b on FULL *and* OOS — and ALL 11 sit at G = 1.00, the top gross rung.**
The band rung ranges over 0.00–0.10 among them; the gross rung does not vary at all. On this grid
the 4b pass is a **gross** claim, exactly as the 2026-09-19 record has said all day.

Rule-8 legitimate pick, U56 weekly (C_SHARPE and C_MEMO agree, IS rows only, 2017–2026 read once):
**band 0.10, G 1.00.**

| | CAGR | Sharpe | MaxDD | H1 / H2 | turnover |
|---|---|---|---|---|---|
| CELL FULL | 11.72% | 1.1726 | −16.30% | 1.247 / 1.107 | 1.32x |
| CELL OOS | 12.14% | **1.1940** | −16.30% | 1.343 / 1.032 | 1.38x |
| its matched twin FULL | 12.12% | 1.1189 | −20.85% | 1.192 / 1.061 | 0.77x |
| its matched twin OOS | 12.32% | 1.1269 | −20.48% | 1.283 / 0.963 | 0.78x |
| SPY FULL | 15.12% | 0.8844 | −33.72% | — | — |
| SPY OOS | 15.26% | 0.8738 | −33.72% | — | — |
| LIVE RULES v2 FULL | 8.62% | 1.2011 | −12.05% | — | — |

Clears 4b FULL **and** OOS at 0 / 10 / 25 / 50 bps. **4a: FAIL** (live RULES v2 draws −12.05%; path
4a cannot adjudicate a growth book — the record's standing finding, reproduced).

**AND THE HONEST HALF.** Pooled over all 180 cells at 10 bps, the band CELL **loses** to its own
realised-gross-matched twin: Sharpe higher in only 76 of 180 FULL (mean dSharpe **−0.0407**) and
64 of 180 OOS (mean **−0.0469**), while being shallower in 104 of 180 (mean +0.62 pp). The de-gross
result survives a fourth family. The headline cell is one of the 76, not the rule.

## GATES 12/12 and survivorship

G0 18.68y / 18.68y / 16.68y; G1 fast_run vs `engine.backtest` returns **2.776e-17** and turnover
1.943e-16; G2 derived 25 bps rung vs a fresh engine run **1.735e-17**; G3 the (U56, W, c=0.03,
G=0.75) cell replays `baseline.rules_v2_weights` to **1.735e-17**; G4 bisection quality **2.900e-14**
over every twin; G5 two dials; **G6 no chooser reads a 2017+ row, tested on a HARD-TRUNCATED tape
(0.000e+00, argmax identical)**; G7 8640 of 8640 published; G8 max realised gross 0.982143, no
shorting, no leverage, **0 twins infeasible**; G9/G10 turnover, realised gross and in-band share
published per cell and per twin.

**SURVIVORSHIP (rule 9).** U56 and B136 are current-constituent lists and SMALL a current sub-$2B
screen carried back to 2010, so every ABSOLUTE level above — including the 4b pass — is an **UPPER
BOUND**. The headline is a twin-minus-twin contrast inside one frame over the same names on the same
days at the same realised exposure and is first-order immune; the 4b pass counts are **NOT**.

*(all 8640 grid rows are published at `2026-09-19_band-gate-out-rate-predicts-realised-gross_C.grid.csv.gz`; the 540 form-residual rows at `.form.csv`, the 108 walk-forward rows at `.walkforward.csv`, the gates at `.gates.csv`, the full console at `.log.txt`.)*

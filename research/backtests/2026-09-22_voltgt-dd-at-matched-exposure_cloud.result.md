# Idea 1537 — is VOL-TARGETING the ONE device that BUYS DRAWDOWN at MATCHED EXPOSURE?

**(2026-09-22, lane cloud.) ANSWERED = PARTIAL. The SIGN survives a finer ladder on two panels
of three; the CLAIM does not survive its own error bar; and the capital question the queue line
actually asks answers NO at 0 of 156 cells.**

Script: `2026-09-22_voltgt-dd-at-matched-exposure_cloud.py` ·
artefacts: `.grid.csv` (168 cells), `.bootstrap.csv` (42 rungs), `.walkforward.csv`, `.gates.csv`,
`.stdout.txt`.

## What was run
BASE frozen at the record's 2026-09-04 anchor shape (top-20 by 126d momentum among names above
their 200d MA with vol20 < 0.60, equal weight at gross 0.75, weekly, t+1).
DEVICE `VOLTGT(v)` = base weights × min(1, v / rv_t), rv_t = 20d realised vol of the BASE book's
own returns, annualised — causal, decided at close t, applied at t+1.
ANCHOR = the same base book scaled by a CONSTANT chosen so its **realised** mean gross equals the
device's (gate G1, max mismatch 1.7e-10).
Ladder v ∈ 0.06 … 0.30 step 0.02 (13 rungs) + 1534's own five; panels U56 / B136 / SMALL;
costs 0 / 10 / 25 / 50 bps reconstructed exactly. **Two tuned dials and no more: VOL TARGET v and
PANEL.** Every grid point published.

## Gates (4 families, all exact)
| gate | result |
|---|---|
| G1 device/anchor realised gross match | max 1.7e-10 over 42 rungs (tol 5e-4) |
| G2 cost reconstruction `r(c) = r0 − turnover·c/1e4` | **0.000e+00** on 3 of 3 panels |
| G4 an unbinding target (v = 9.99) reproduces the base book | **0.000e+00** on 3 of 3 panels |
| G3 1534's pooled VOLTGT dMaxDD on its own five rungs @10 bps | **+1.72 pp** vs published **+0.97 pp** |

**G3 is a PARTIAL reproduction and is reported as one.** The SIGN and the ordering replicate; the
LEVEL does not, and the most likely cause is the SMALL panel — this run drops the 54 tickers with
`max_1d_move >= 1.0` from `data/small_meta.csv` before pricing, which 1534 did not. The +0.97 pp
should not be quoted as reproduced.

## The findings
**1. The sign is real but PANEL-SPLIT, so it is not a device fact.** dMaxDD (device − matched
anchor) @10 bps on the fine ladder: **B136 +2.63 pp, U56 +1.69 pp, SMALL −0.79 pp.** At 50 bps it
is negative on two of three (U56 −0.22, SMALL −2.87, B136 +0.41): the shallower drawdown is bought
with turnover, and the cost ladder takes it back.

**2. It does not survive its own error bar where the device BINDS.** Paired circular-block
bootstrap (LB = 65, B = 500, the same blocks drawn for every book and panel in a replicate).
At the binding rungs v = 0.06–0.12 the t on dMaxDD is 1.18–1.57 on U56/B136 and −0.01 to −0.32 on
SMALL, with a 95% CI straddling zero at **every panel**. The only |t| > 2 cells sit at
v ≥ 0.18–0.24, where the scalar is nearly always 1 and the "device" is within a rounding error of
the base book (U56 v = 0.24 reads dMaxDD −0.0001 with se 0.0003). **Every cell that clears 2σ is a
cell where vol targeting does almost nothing.**

**3. It is not free.** dSharpe is negative at every binding rung on all three panels (pooled
−0.011 @10 bps, −0.043 @50 bps) and dCAGR −0.34 pp @10 bps. That is 1534's own −0.56 pp/yr
direction, re-confirmed on 13 rungs.

**4. THE QUEUE'S QUESTION — NO, at 0 of 156.** Rungs clearing **4b OUT OF SAMPLE while their own
matched-exposure anchor does not: 0 of 156.** The reverse (anchor clears, device does not): **4**.
Vol targeting never buys a 4b pass a zero-parameter constant de-gross does not already have, and
it sometimes loses one.

**5. 4a is 0 of 156** on every panel and every cost rung — the v1-shape ranked book never beats
live RULES v2 in both halves with no worse drawdown, device or anchor.

**6. Rule 8 (v chosen on … 2016 only; 2017–2026 read ONCE).** The IS-Sharpe chooser picks the
LOOSEST rung it is offered on all three panels at the binding cost — v = 0.20 (U56), 0.24 (B136),
0.26 (SMALL) — i.e. it chooses to turn the device OFF. 4b OOS is reached at 2 of 12
(panel × cost) cells, and at both of them the anchor reaches it too.

## One KEEP-4b candidate, RECORDED AND NOT RECOMMENDED
The rule-8 pick on U56 at 10 bps clears 4b FULL and OOS, so it is recorded; it is not recommended
and the memo says why. See `2026-09-22_voltgt-dd-at-matched-exposure_cloud_MEMO.md`.

## Caveats
Survivorship (PROTOCOL rule 9): U56 / B136 are 2026 constituents held from 2008; SMALL is the
current-constituent sub-$2B screen (`data/SMALL_PANEL_README.md`) with `max_1d_move >= 1.0`
tickers dropped. Every CAGR level is optimistic and both 4b level legs are easier than on a
point-in-time panel. Costs are flat per unit turnover — no spread, impact or borrow. One cadence
(W), one delay (t+1), one base shape (N = 20, H = 126).

RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py untouched.

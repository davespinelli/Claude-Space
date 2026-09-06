# Idea 263 — persistence-vs-cost-as-a-required-column (cloud, 2026-09-06)

**Verdict: KEEP AMENDED (pre-registered branch (b)) — a REPORTING clause only. No book, no
RULES change, no PROTOCOL edit by this script (rule 6).**

The queue proposed: *any comparison between two arms whose turnovers differ by more than 2x
must publish both turnovers and the difference at 0 bps beside the quoted rung.* This run
scored that clause as a trigger on 138 within-family pairs of the record's own **real
(non-null) dials** — cadence, n, gross, the vol scaler, the eligibility gate, the hysteresis
band, ranked-vs-EWall — over U56 / B136 / SMALL439, 24 books per panel simulated once at
0 bps with every rung derived exactly.

## What the clause is protecting against is real

* **34 of 138 pairs (25%) have a breakeven inside 0–25 bps** — U56 14/46, SMALL439 13/46,
  B136 7/46. **23 of 138 change sign between 0 and PROTOCOL's own 10 bps.** A quarter of the
  record's within-family comparisons are statements about the rung, not about the arms.
* Rule 8 makes it concrete: **the rung the chooser reads changes the pick on 2 of 3 panels,
  and the OOS gap is large.** U56 — chooser at 0/10 bps picks `FWD20gate-none` (OOS Sharpe
  **1.162**, CAGR 16.4%, MaxDD −21.6%), chooser at 25 bps picks `FWD10@Q` (OOS **0.867**).
  SMALL439 — 0/10 bps picks `FWD20vs` (OOS **0.319**), 25 bps picks `FWD10@M` (OOS **0.481**).
  B136 picks `FWD10@Q` at all three rungs (OOS 0.795).

## But the 2x turnover ratio is the wrong trigger

Scored against measured truth (breakeven in (0, 25] bps), on all 138 pairs:

| trigger | fires | TP | FP | FN | TN | precision | recall |
|---|---|---|---|---|---|---|---|
| `ratio > 2.0x` (the queue's) | 71 | 28 | 43 | 6 | 61 | **0.394** | 0.824 |
| `ratio > 1.4x` (idea 267's band) | 105 | 29 | 76 | 5 | 28 | 0.276 | 0.853 |
| `ratio > 3.0x` | 34 | 17 | 17 | 17 | 87 | 0.500 | 0.500 |
| `abs_gap > 5.0` (|T/vol| gap) | 110 | 33 | 77 | 1 | 27 | 0.300 | 0.971 |
| **`c*` from the four published numbers, in 0–25** | **34** | **34** | **0** | **0** | **104** | **1.000** | **1.000** |

The **GROSS family is the clean counter-example**: scaling gross scales turnover *and* vol
together, so `T/vol` — the denominator of idea 262's law — barely moves however big the
turnover ratio gets. Its 18 pairs run to a **3.99x turnover ratio** at a median |gap| of
**0.548**, and **only 1 of 18 flips inside 0–25 bps**. Six of the ratio's 43 false flags are
gross pairs. In the other direction the ratio **misses 6 real flippers**, including
`U56 FWD40 vs FWD60` (ratio 1.69, c\* = 10.5 bps — it straddles PROTOCOL's own rung) and
`SMALL439 FWD20 vs FWD20vs` (ratio 1.21, c\* = 11.6 bps).

## The four numbers are sufficient

Idea 262's law `c* = dSharpe(0)·1e4/(T_x/vol_x − T_y/vol_y)`, re-scored here on **non-null**
arms for the first time (58 flipping pairs): **R² 0.9996, median |error| 0.015 bps, 90th pct
0.439 bps**. So the clause's *content* is right and its *threshold* is wrong: publishing both
turnovers, both vols and dSharpe(0) lets any reader recover the breakeven with a calculator
and no re-run, which is a perfect screen; keying the requirement on a 2x ratio flags 43 pairs
that cannot flip and misses 6 that do.

## By-products (honest, not a claim)

* **4a passes 116/504, 4b passes 85/504.** At 10 bps the 4b passes are `U56 FWD20 / FWD20@M /
  FWD40@M / FWD20gate-ma / FWD20b10 / FWD20b20` and `B136 FWD40 / FWD60 / EWALL`. Binding 4b
  clause across the 10-bps grid: DD 43, H2 41, CAGR 37, OOS 34, H1 32.
* The only book passing **both** paths at 10 bps is `U56 FWD40@M` — CAGR 10.9%, Sharpe 1.194,
  MaxDD −13.8%, halves 1.183/1.206, OOS Sharpe 1.300 / CAGR 12.1% / MaxDD −13.8%, turnover
  2.36x/yr, vs RULES v1 OOS 0.747 and SPY OOS 0.882 (CAGR 15.5%, MaxDD −33.7%). **This is a
  point of the already-published n × cadence grid** (the record's monthly-dominates-weekly
  result), not a new rule, and it is not proposed as one here.

## Caveats

SMALL439 is the sub-$2B panel with the 44 `max_1d_move >= 1.0` tickers dropped — **current
constituents of the screen only, no delistings (survivorship)**; it is never pooled with the
large-cap panels. B136 and U56 are current-constituent lists too (PROTOCOL rule 9).

# Idea 329 — does the no-trade BAND rescue the B136 H2 bar?  **KILL (premise falsified)**

Lane C, 2026-09-07. Script `2026-09-07_does-the-BAND-rescue-the-B136-H2-bar_C.py`,
console `…_C.console.txt`, grid `…_C.grid.csv`, walk-forward `…_C.walkforward.csv`.

## Pre-registration (fixed before the run)

| | |
|---|---|
| panel | **B136** (`research/universe_broad.json`, 135 names + SPY) |
| n | **20**, not swept |
| m | **20**, not swept for the verdict (swept 0/5/10/20/40 as a reported context axis only) |
| weights | NORM `w_i = 0.75 / k_t`, RULES v1 eligibility (200d MA, vol20 < 0.60), v1 composite, vol scaler OFF |
| tuned dial | **cadence ∈ {W, M, Q}** — one parameter |
| reported axes | cost ∈ {0, 10, 25} bps; m; U56 and SMALL439 as context |
| decision rule | the cell clears **all five** 4b bars at 10 bps at some cadence → idea 325's PARK is cross-universe and goes to Sunday review; otherwise the candidate is a **U56 object** |

## Correction to the queue entry

Idea 329 says the cell "fails 4b on B136 on ONE bar". Re-reading idea 325's committed grid
(section `[0]`): at 10 bps it fails on **TWO** — H2 (margin −0.0170) **and** the drawdown cap
(margin −0.0020, MaxDD −20.43% against the −20.23% cap). The queue text is corrected, not
carried forward, and this matters: a cadence that buys H2 by widening drawdown cannot pass.

## Answer: **NO cadence clears the cell.** 0 of 3 at 10 bps (and 0 of 3 at 0 and at 25 bps).

Pre-registered cell, B136 n=20 m=20, 10 bps. SPY bars on this sample: H1 > 0.957, H2 > 0.834,
OOS > 0.882, MaxDD ≥ −20.23%, CAGR ≥ 10.66%.

| cadence | turn/yr | CAGR | Sharpe | MaxDD | H1 / H2 | OOS | H1 marg | **H2 marg** | OOS marg | **DD marg** | CAGR marg | 4b |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **W** | 6.20 | 14.27% | 1.009 | −20.43% | 1.235 / 0.817 | 0.926 | +0.2784 | **−0.0170** | +0.0436 | **−0.0020** | +0.0361 | **fail H2, DD** |
| **M** | 4.16 | 16.77% | 1.108 | −26.31% | 1.241 / 1.006 | 1.092 | +0.2841 | **+0.1722** | +0.2102 | **−0.0608** | +0.0611 | **fail DD** |
| **Q** | 2.62 | 15.41% | 1.002 | −27.38% | 1.248 / 0.819 | 0.921 | +0.2915 | **−0.0154** | +0.0394 | **−0.0716** | +0.0475 | **fail H2, DD** |

The H2 bar **is** rescuable — monthly buys **+0.189** of H2 margin over weekly (0.817 → 1.006,
clearing SPY's 0.834 by 0.17) and lifts OOS from 0.926 to 1.092. It is bought with drawdown:
MaxDD goes −20.43% → −26.31%, i.e. the DD margin pays **−0.059** for the H2 gain of **+0.189**.
4b is a conjunction, so the trade is not admissible. Quarterly buys neither bar. **The cadence
dial does not have a setting where B136 top-20 clears 4b.**

Whole grid (3 panels × 3 cadences × 5 m = 45 cells, every point in `…grid.csv`):

| rung | 4b passes | 4a passes | where |
|---|---|---|---|
| 0 bps | 13/45 | **0/45** | 11 U56, **2 B136** (W m=0, W m=5), 0 SMALL439 |
| 10 bps | 11/45 | **0/45** | **11 U56, 0 B136, 0 SMALL439** |
| 25 bps | 10/45 | **0/45** | **10 U56, 0 B136, 0 SMALL439** |

B136's only two 4b passes have breakevens of **6.9 and 7.5 bps** — below PROTOCOL's own 10 bps,
so they are 0-bps artefacts in exactly the sense lane C's 2026-09-07 run established. **On this
family, B136 has no book that survives its own cost assumption.** SMALL439 is not close on any
cell (best H2 margin −0.427). 4a is 0/45 at every rung: RULES v2's −12% drawdown is untouchable
for a 75%-gross equity book, which is the standing reason 4a is not the operative path.

## Rule 8 walk-forward — (cadence, m) chosen on 2008–2016 IS Sharpe @10 bps, 2017–2026 read once

| panel | IS pick | IS Sharpe | OOS Sharpe | OOS CAGR | OOS MaxDD | pre-reg (W,m=20) OOS | anchor (W,m=0) OOS | OOS-best | regret | SPY OOS | RULES v2 OOS |
|---|---|---|---|---|---|---|---|---|---|---|---|
| U56 | Q, m=40 | 1.213 | 1.065 | 14.03% | −19.06% | 1.187 | 1.131 | M m=5 → 1.314 | **+0.249** | 0.882 | 1.285 |
| **B136** | M, m=0 | 1.212 | **1.041** | 16.41% | −26.10% | **0.926** | 0.884 | M m=20 → 1.092 | +0.051 | 0.882 | 1.119 |
| SMALL439 | M, m=40 | 0.677 | 0.300 | 3.85% | −35.11% | 0.461 | 0.466 | W m=40 → 0.531 | **+0.231** | 0.882 | 0.568 |

The chooser misses the OOS-best cell on all three panels (11th such instance in the record) and
loses to the LIVE book out of sample on all three (−0.220 / −0.078 / −0.268). On B136 the
chooser's monthly pick does beat SPY OOS by +0.159 — but at −26.1% drawdown, so it fails 4b
out of sample for the same reason it fails in sample.

## Verdict

**KILL of the rescue premise. Idea 325's PARK candidate is a U56 OBJECT and is labelled one.**
It clears 4b at 10 bps on U56 at every m (breakevens 21–48 bps) and on B136 at no m, no
cadence, no rung ≥ 10 bps. The cross-universe promotion the queue entry contemplated does not
happen.

## By-product, PARKed not KEPT

`U56, top-20, NORM g/k at 0.75, **monthly**, m=0` clears all five 4b bars at **0, 10 and 25 bps**:
15.30% / 1.213 / −19.51%, H1/H2 1.200/1.232, OOS **1.307**, turnover 4.8×/yr, **breakeven 68.6
bps**. That is the highest-breakeven 4b pass lane C has produced and it is not a 10-bps artefact.
It is **not** written up as a KEEP because (a) it was found on the context axis, not the
pre-registered cell, (b) the identical book on B136 fails 4b on drawdown at every rung
(−26.10%), and (c) it still fails 4a on drawdown (−19.51% against the live book's −12.05%),
even though its OOS Sharpe 1.307 edges RULES v2's 1.285 on the same panel. Cadence, not the
band, is the dial that moved it — queued as idea 331.

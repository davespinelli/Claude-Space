# Idea 838 — how-many-INDEPENDENT-BOOK-FORMS-does-the-record-actually-contain (cloud, 2026-09-12)

**ANSWERED = 2 (U56), 3 (B136), 6 (SMALL664) — not 14. KILL as a capital idea; no KEEP claimed, no
memo, no book promoted, no RULES/PROTOCOL edit applied (rule 6). RULES.md, PROTOCOL.md, scan.py,
bot.py and baseline.py untouched.**

Script `2026-09-12_how-many-INDEPENDENT-BOOK-FORMS-does-the-record-actually-contain_cloud.py`;
outputs `.arms.csv` (60 rows), `.clusters.csv` (126), `.walkforward.csv` (42), `.console.txt`.
10 bps, t+1, weekly, gross 0.75 (two gross-dial arms excepted), 20 arms x 3 panels.
Tuned parameters: FORM SET (WIDE 20 arms / CORE 11) and CORRELATION WINDOW (FULL / IS / ROLL252) —
18 cells, all reported. The tau ladder (7 rungs) and the panel are REPORTED, NEVER SELECTED.
SURVIVORSHIP: B136 and SMALL664 are current constituents only; SMALL664 = the small panel after
dropping all 52 tickers with `max_1d_move >= 1.0` in `data/small_meta.csv` (the panel file now
carries 716 columns, not the 485 the README quotes — 664 survive the filter, SPY benchmark-only).

## GATES (all printed before any new number)
G1 engine vs vectorised runner max|dret| **1.041e-17** (bar 1e-12) PASS · G2 max daily gross
**1.000000** (bar <= 1.0) PASS · G3 determinism PASS (note: the engine's own `shift(1)` leaves the
first 4 days NaN in BOTH runners; they are dropped by the 260-day warm-up) · G4 dial anchor
corr(EW_G100, EW_G0375) = 0.9999 / 0.9998 / 0.9996 (bar 0.99) PASS.

## THE ANSWER
The count depends entirely on where the threshold sits, so the threshold is fixed by the arms whose
answer is known: the six PURE DIAL pairs (gross 1.00/0.75/0.375, n 20/10/5, weekly/monthly). A
threshold that splits a dial pair is measuring a scalar, not a form.

| panel | weakest dial-pair rho | tau_dial (FULL) | **independent forms at tau_dial** | forms at tau=0.95 | n_eff (participation ratio) |
|---|---|---|---|---|---|
| U56 | 0.8125 (LOWVOL20/LOWVOL10) | 0.80 | **2 of 20 arms** | 10 | 1.48 |
| B136 | 0.8312 (LOWVOL20/LOWVOL10) | 0.80 | **3 of 20 arms** | 11 | 1.64 |
| SMALL664 | 0.7969 (TOP20_MOM/TOP5_MOM) | 0.80 | **6 of 20 arms** | 13 | 2.08 |

On the IS window and on ROLL252 the small panel has **no rung at all** that merges every dial pair —
TOP20/TOP5 correlate at 0.7969, below the whole ladder. **The ceiling on every future cross-book n
is 2 / 3 / 6, and the participation ratio, which needs no threshold, is lower still: 1.48 / 1.64 /
2.08.** Idea 837's 14 families is an upper bound off by 4-7x on the large-cap panels.

## PRE-REGISTERED HYPOTHESES — 2 of 5 PASS, and the three failures carry the result
- **H_CEIL PASSES.** At tau=0.95/FULL/WIDE the count is 10 / 11 / 13, all below 14 — but this rung
  is exactly the one the dials show is too high.
- **H_DIAL FAILS, 7 of 18 dial pairs split at tau=0.95** (TOP20/TOP5 on all three panels,
  LOWVOL20/LOWVOL10 on all three, TOP20/TOP10 on SMALL664). A CONCENTRATION dial makes a new
  return series in a way a GROSS dial (rho 0.9999) and a CADENCE dial (0.9629-0.9886) do not. Any
  census that counts arms at a 0.95-style threshold is counting n as a form.
- **H_WINDOW FAILS, max spread 4 forms** across {FULL, IS, ROLL252} at fixed (panel, form set, tau)
  — the count is not window-free, and ROLL252 is systematically the lowest (rolling medians are
  higher: mean rho +0.8374 vs +0.8003 on U56).
- **H_STABLE FAILS (rule 8), min pair agreement 0.6727** over 42 cells (U56/CORE/tau 0.90: 4 IS
  forms become 3 OOS forms). Agreement is >= 0.90 in 33 of 42 cells but the partition is not a
  window-stable object at the rungs where the count is small.
- **H_ENS PASSES.** The IS-fitted, one-arm-per-cluster ensemble (representative = first in
  catalogue order, NEVER the best performer) clears 4b in **11 of 42** cells — all on U56/B136,
  **0 of 14 on SMALL664**.

## RULE 8 WALK-FORWARD, OOS 2017-01-01 … 2026-09-11 (nothing fitted on it)
Best ensemble cell, U56/WIDE/tau 0.95 (9 IS forms): OOS **CAGR +13.62%, Sharpe 1.194, MaxDD
−19.78%** vs **RULES v2** (+9.47%, 1.278, −12.2%) and **SPY** (+15.33%, 0.877, −33.72%).
B136/WIDE/tau 0.95: +11.81% / 1.134 / −19.49%. SMALL664 never passes (best 0.995 Sharpe at
−29.10% MaxDD, CAGR floor and DD cap both bind).
**This is not a KEEP.** On U56 alone five single arms already clear 4b on their own (MA_RS,
BAND_RS, VOLCAP_DG, MOM_MA_DG, CORRLO20; CORRLO20 full Sharpe 1.263, OOS 1.220), and 0 of 60 arms
clear 4a on any panel — consistent with the record's finding that 4b is cheap on U56 and 4a is
unreachable without de-grossing. The ensemble's advantage over its own members is inside that
spread, and its partition fails its own OOS stability test.

## WHAT THIS BUYS THE RECORD
Every cross-book statistic on this corpus should quote n <= 2 (U56), 3 (B136), 6 (SMALL664) — or
the participation ratio 1.48 / 1.64 / 2.08 — not the arm count. A 20-arm sweep on U56 is two
independent things measured ten times.

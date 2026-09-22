# Idea 2290 — is the CARRY SLEEVE's gain a 2022-2026 RATE-REGIME DRAW?

**Lane cloud, 2026-09-22. Script `2026-09-22_carry-sleeve-rate-regime-draw_cloud.py`.
VERDICT: ANSWERED — NO, for the instrument the clause actually ships (SHY). KILL of the
regime-draw premise; the 4a KEEP-candidate from idea 2294 SURVIVES all six windows.
SEPARATE CONFIRMED DEFECT: the instrument dial is NOT rule-8 learnable, and every 4b pass
in the grid is an artefact of deleting the 2022 bond bear market.**

Two dials and no more: instrument {NONE, SHY, IEF, TLT} (phi FROZEN at 1.00, clause 7's
shipped value) x window {FULL, EX22, EX21, EX20, ZIRPFLAT, ZIRPSWAP}. Panel {U56, B136}
and cost rung {0, 10, 25, 50} bps are reported at every cell, never selected: **288
published sleeve cells** (charged and MMF-rebated variants), plus 96 phi=0 controls.

## Gates

| gate | value |
|---|---|
| G1 U56 | idea 2294's own construction reproduced EXACTLY: SHY phi=1 @10bps = **9.1201% / 1.2675 / -11.4824%** (2294's memo: 9.1201% / 1.2675 / -11.4824%) |
| G1 B136 | **8.4751% / 1.1669 / -11.6473%** (2294's memo: 8.4751% / 1.1669 / -11.6473%) |
| G2 | `bt_percol` vs `engine.backtest`: max abs difference **4.3e-19 (U56) / 1.7e-18 (B136)** — the cost-rung decomposition is exact |

This run's primary construction differs from 2294's in one deliberate way: the sleeve is a
SYNTHETIC `CARRY` column invisible to `rules_v2_weights`, so a counterfactual sleeve tape
cannot move a single equity decision. G1 shows the two constructions agree to the printed
digit at the shipped cell.

## A. The premise is FALSE for SHY and TRUE for the instruments the clause forbids

Mean annual sleeve gain (book minus its own phi=0 control), U56 @ 10 bps charged:

| instrument | 2009-2021 | 2022-2026 | instrument's own mean annual return, 2009-2021 / 2022-2026 |
|---|---|---|---|
| **SHY** | **+0.4501%** | **+0.7060%** | +1.0692% / +1.9157% |
| IEF | +1.7226% | **-0.9697%** | +3.5463% / -1.4316% |
| TLT | +2.6313% | **-4.2998%** | +5.8387% / -7.2377% |

B136 reads the same to within 0.2 pp on every row. The idea's premise — "the entire T-bill
carry on this tape is earned after 2021, SHY's own 2009-2021 CAGR is near zero" — is **not
what the tape says**: SHY returned ~1.07%/yr on average through the ZIRP years and the
sleeve collected **64% as much gain then as it does now**. The higher post-2021 yield is
paid for by the 2022 capital loss (SHY -3.88%, sleeve -2.64 pp on the book).

## B. Two explicit ZIRP counterfactuals retain the whole gain

`ZIRPFLAT` regrows the sleeve instrument from 2022-01-01 at its own 2009-2021 mean daily log
return with zero vol; `ZIRPSWAP` replays its 2009-2021 daily returns in order. Both keep the
equity tape untouched. SHY, phi=1.00, 10 bps:

| panel | variant | FULL gain | ZIRPFLAT | ZIRPSWAP | EX22 (sample ends 2021) |
|---|---|---|---|---|---|
| U56 | charged | +0.500%/yr | +0.505% (**100.9%**) | +0.711% (**142.1%**) | +0.457% (**91.3%**) |
| U56 | mmf | +0.612%/yr | +0.617% (100.7%) | +0.823% (134.4%) | +0.565% (92.3%) |
| B136 | charged | +0.516%/yr | +0.497% (96.4%) | +0.682% (132.3%) | +0.441% (85.4%) |
| B136 | mmf | +0.627%/yr | +0.608% (97.0%) | +0.794% (126.6%) | +0.550% (87.8%) |

**4a is True at the shipped cell in all six windows on both panels.** Across the whole grid
SHY clears 4a in **13-14 of 16 cells in every window, FULL included**; IEF clears 4a in 16 of
16 in every window **except FULL, where it clears 0 of 16**; TLT clears 4a **0 of 96**. The
regime dependence the idea suspected is real and it lands entirely on the instruments
clause 7 already excludes.

## C. Rule 8 — the instrument dial is NOT identifiable in sample

Dials chosen on 2009-2016 only (a window that is entirely ZIRP); 2017-2026 read once.

| panel | IS Sharpe NONE / SHY / IEF / TLT | IS spread best-worst | block-bootstrap SE | t |
|---|---|---|---|---|
| U56 charged | 1.1043 / 1.1532 / 1.2973 / 0.9867 | +0.3106 | 0.1967 | **+1.58** |
| U56 mmf | 1.1043 / 1.1688 / 1.3125 / 0.9978 | +0.3147 | 0.1873 | **+1.68** |
| B136 charged | 1.0922 / 1.1383 / 1.2953 / 1.0142 | +0.2811 | 0.1955 | **+1.44** |
| B136 mmf | 1.0922 / 1.1527 / 1.3096 / 1.0250 | +0.2846 | 0.1946 | **+1.46** |

Not one panel resolves the dial at |t| > 2 (LB = 65d, B = 400, seed 20260922). `C_ISSHARPE`
nevertheless picks **IEF on 4 of 4 cells** — the longest duration that looked best in the
ZIRP era — and loses out of sample on every one:

| panel | chooser | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|
| U56 | C_ISSHARPE = IEF | 9.85% | 1.1997 | **-18.06%** |
| U56 | zero-parameter SHY | **10.14%** | **1.3558** | **-11.48%** |
| U56 | control NONE (the ship) | 9.46% | 1.2767 | -12.05% |
| U56 | SPY | 15.29% | 0.8751 | -33.72% |
| B136 | C_ISSHARPE = IEF | 8.25% | 1.0455 | **-19.69%** |
| B136 | zero-parameter SHY | **8.57%** | **1.1908** | **-11.65%** |
| B136 | control NONE (the ship) | 7.85% | 1.1017 | -12.24% |
| B136 | SPY | 15.26% | 0.8737 | -33.72% |

The record's chooser law again, and with the sharpest possible edge: the fitted dial costs
**6.6 pp of drawdown** against the no-fit default on both panels. The clause must therefore
name the instrument's PROPERTY (zero duration), never let a backtest pick it.

## D. Path 4b: 52 of 288 pass, and every single pass deletes the 2022 bond crash

| instrument | EX20 | EX21 | EX22 | **FULL** | ZIRPFLAT | ZIRPSWAP |
|---|---|---|---|---|---|---|
| SHY | 0/16 | 0/16 | 0/16 | **0/16** | 0/16 | 0/16 |
| IEF | 0/16 | 0/16 | 0/16 | **0/16** | 3/16 | 8/16 |
| TLT | 0/16 | 10/16 | 7/16 | **0/16** | 10/16 | 14/16 |

**0 of 48 cells pass 4b on the FULL tape.** Every pass is a long-duration position scored on
a window that either stops before 2022 (EX21/EX22) or replaces 2022-2026 with a fabricated
ZIRP tape. The CAGR floor is the binding leg in **197 of 288** cells and binds ALONE in most
of them; the DD cap binds alone in 2. Idea 2294's 4b KILL is confirmed and strengthened: the
only route to a 4b pass through this clause is a bond bet plus a deleted bear market.

## Caveats

One cadence (W), one band (0.03), one gross (0.75), one phase (Friday), phi frozen at 1.00,
t+1 execution, two panels, 10 bps as the live rung. **Rule 9 SURVIVORSHIP:** U56 and B136
are current-constituent lists held from 2008, so every absolute CAGR is upward-biased and
the 4a/4b pass counts inherit that bias; the sleeve contrast is same-tape, same-names,
same-days and first-order immune. The true instrument (an MMF or BIL, zero duration) is
**not in the cached panels** — SHY is the shortest available, so it is a conservative proxy
for the 2022 loss and an optimistic one for duration risk. `ZIRPSWAP` and `ZIRPFLAT` are
counterfactual tapes, not history; they are reported as sensitivity, and no verdict here
rests on a 4b pass they produce.

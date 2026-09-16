# Idea 1097 (lane C, 2026-09-16) — is the BREAKEVEN RUNG c* PREDICTABLE from BINDING-LEG MARGIN over TURNOVER ALONE?

**ANSWERED = NO AS THE QUEUE WROTE IT, YES ONCE THE UNITS ARE CONVERTED — AND THE CONVERSION
NEEDS NO FITTED PARAMETER.** The literal `margin / turnover` form is wrong by two to three
orders of magnitude on every Sharpe leg. A parameter-free unit conversion closes 6 of the 8
legs to ~1 bp. The DRAWDOWN leg — which is in the binding set at **47 of 54 cells** — does not
close under any of the four forms. No RULES change, no book promoted, no PROTOCOL edit (rule 6);
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.

## THE TWO DIALS AND NO MORE (PROTOCOL rule 4)
`LEG` {L_H1, L_H2, L_OOS, L_DD, L_CAGR, O_S, O_DD, O_CAGR} x `FORM` {F_RAW, F_UNIT, F_K1,
F_KLEG} — **all 32 points published** (`.scores.csv`), plus the derived conjunction reading at
every form (`.conjunction.csv`). Frozen and NOT dials: 1082/1086/1094's N {5,8,10,12,15,20,25,
30,40} x H {21,63,126} = 27 cells per panel, **all 54 reported** (`.cells.csv`, `.ladder.csv`);
cap INF; CAND20 legs; max_vol 0.60; gross 0.75; weekly; LAG 1; warm-up 260; IS end 2016-12-31;
4b constants 0.60/0.70. **Cost is not a dial** — it is the axis whose breakeven is predicted.
Every fitted constant is fitted on **U56 alone**; B136 is a pure hold-out.

## THE FOUR FORMS AND WHAT THEY COST
| form | free params | what it is |
|---|---|---|
| `F_RAW` | 0 | `1e4 * m_L(0) / tn_L` — the queue's literal proposal |
| `F_UNIT` | 0 | Sharpe legs `1e4*m*sigma_L/tn_L`; DD legs `1e4*m/(tn_L*dt_L)`; CAGR legs = RAW |
| `F_K1` | 1 | `k * F_RAW`, one global k = 0.1626 |
| `F_KLEG` | 1 per leg | `k_L * F_RAW`, the queue's "per leg" fit |

## THE ANSWER, LEG BY LEG (median |err| in bps against the true 1-bp ladder)
| leg | n | F_RAW | F_UNIT | F_K1 | F_KLEG | verdict flips @10 bps (best form) |
|---|---|---|---|---|---|---|
| L_H1 | 53 | **746.80** | **1.16** | 24.16 | 9.92 | 0 of 54 |
| L_H2 | 47 | **371.22** | **0.83** | 4.72 | 5.54 | 0 of 54 |
| L_OOS = O_S | 51 | **365.84** | **0.80** | 5.90 | 5.88 | 0 of 54 |
| L_CAGR | 48 | 15.01 | 15.01 | 88.95 | **0.64** | 0 of 54 |
| O_CAGR | 48 | 15.80 | 15.80 | 92.42 | **0.45** | 0 of 54 |
| L_DD | 10 | 65.54 | 35.71 | 71.90 | **18.15** | 0 of 54 |
| O_DD | 10 | 65.75 | 34.71 | 71.93 | **19.32** | 0 of 54 |

- **H_RAW REFUTED, exactly as pre-registered.** `margin/turnover` alone lands within PROTOCOL's
  own 10 bps rung at **8.5% of the 318 scorable (cell, leg) points**. It is not a near miss: on
  L_H1 it over-states the breakeven by a median **746.80 bps**, because a Sharpe margin is not
  in units of annual return.
- **F_UNIT closes the four Sharpe legs with NO fitted constant**: median |err| 0.80–1.16 bps,
  **100% within 10 bps, and ZERO verdict flips at 10, 25 and 50 bps, on both panels.**
- **The CAGR legs need one constant, and that constant is not free either.** F_KLEG's fitted
  `k[L_CAGR] = 0.8756` against `1/(1 + median book CAGR) = 0.8568` (ratio 1.022): the gap
  between `m/tn` and the truth is **compounding**, so `c* = 1e4*m/(tn*(1+CAGR))` is a closed
  form with no free parameter. With it: median |err| **0.64 bps**, 100% within 5 bps, 0 flips.
- **The DRAWDOWN leg does not close under any form.** Best is F_KLEG at median 18.15 bps, p90
  78.78, only 30% within 10 bps, and `k[L_DD]=8.39` against the episode-length identity's 10.96
  (ratio 0.766). The reason is `H_LINEAR REFUTED`: the DD leg's 0–10 bps slope is **0.175** of
  its 0–200 bps slope (every other leg 0.99–1.04), because cost does not merely deepen the
  existing drawdown, it moves which episode is the maximum. Worst slope-implied error 219.85 bps.

## DOES ONE CLOSED FORM REPLACE THE LADDER? `H_ONEFORM` **REFUTED** — BUT IT REPLACES IT AT PROTOCOL'S OWN RUNG
At the conjunction (1094's object), F_KLEG reads median |err| **1.34 bps** (full) / 2.01 (OOS),
F_UNIT 1.61 / 6.36 — but **max |err| 44.0–46.9 bps** at the one DD-bound cell each, so neither
meets the 5 bps per-leg bar on DD, and hold-out verdict flips are 16 (F_KLEG) not 0. What both
forms do get right is the decision: **0 of 54 conjunction verdict flips at PROTOCOL's 10 bps**,
2 at 25 bps, 1 at 50 bps, and F_KLEG names the **true binding leg at 100% of live cells**
(`H_BINDING SUPPORTED`; F_UNIT 89% / 70%). So the ladder can be replaced by arithmetic for a
pass/fail at 10 bps, and cannot be replaced for a *quoted* c* value.

## TWO CORRECTIONS TO THE RECORD
1. **"solved c* exactly ... for 54 cells" is wrong.** Only **9 of 54** cells have a finite
   full-sample c* (10 of 54 OOS); the other 45 **fail 4b at 0 bps and have no breakeven at all**
   (U56 8/27, B136 1/27). 1094's `rho(c*, turnover) = -0.65` reproduces to the digit — and is a
   statement about **n = 9**: 2,000-rep bootstrap 90% interval **[-0.932, -0.071]**, width 0.860.
   The OOS reading is **-0.4863, interval [-0.852, +0.148]**, straddling zero. `H_RHO SUPPORTED`:
   it reproduces and it is unresolved.
2. **1094's "8–42x" is a ratio of SLICE MEANS, and it is span-dependent.** G6 reproduces all six
   committed slice values at 8.88e-16. Read **per cell** on the same 0→50 bps span the ratio runs
   median **14.49x, range 3.10–96.81x** over the 54 cells — the published envelope understates
   the spread at both ends by ~3x. Read over 0→200 bps the same ratio reads median 3.41x (U56) /
   2.42x (B136), because the DD leg is the non-linear one.

## GATES 15 of 15 PASS, printed before any result number
G1/G1b/G1c `r(c) = g - tn*c/1e4` == `engine.backtest` at 0/10/25 bps (1.39e-17); G2 936/1071/
1082/1094's committed U56 W/H126 N=20 triple (3.18e-07); G3 SPY OOS triple (1.70e-04); G4 live
RULES v2 MaxDD -12.05% (4.95e-05); **G5a/G5b/G5c reproduce 1094's 54 committed turnover values
(1.78e-15) and BOTH committed c* columns EXACTLY (0 mismatches, 9 and 10 finite)**; **G6
reproduces 1094's six committed D1 slice means (8.88e-16)**; G7 conjunction c* == min over
per-leg c* at all 54 cells (`H_MIN SUPPORTED`); G8 every per-leg pass set is an interval from
0 bps; G9 the c* axis is live (spread 200 bps).

## RULE 8 AND BOTH KEEP PATHS — NOTHING PROPOSED
Cell chosen on **IS 2009–2016 only**, OOS 2017–2026 read once, three declared choosers.
**A look-ahead was caught in this run's own first pass and is recorded rather than removed:**
`C_CSTARPRED` initially scored cells with FULL-SAMPLE margins and picked cells that clear 4b on
both panels. That is not an IS-only chooser. Rebuilt on IS-window margins, IS turnover, IS vol
and the IS drawdown episode — and on `F_UNIT`, the parameter-free form, so no fitted constant
enters either — it picks differently and **fails**:

| panel | chooser | pick | OOS CAGR / Sharpe / MaxDD @10 bps | 4b OOS | 4b full | 4a | regret |
|---|---|---|---|---|---|---|---|
| U56 | C_ISSHARPE | N=12 H=21 | 17.57% / 1.1426 / -19.48% | **PASS** | **PASS** | FAIL | +0.0632 |
| U56 | C_CSTARTRUE | N=40 H=126 | 14.00% / 1.0983 / -22.98% | FAIL (O_DD) | FAIL | FAIL | +0.1075 |
| U56 | C_CSTARPRED | N=30 H=63 | 14.72% / 1.1180 / -21.78% | FAIL (O_DD) | FAIL | FAIL | +0.0878 |
| B136 | C_ISSHARPE | N=5 H=63 | 20.46% / 0.9156 / -28.62% | FAIL (O_DD) | FAIL | FAIL | +0.1539 |
| B136 | C_CSTARTRUE | N=40 H=63 | 13.89% / 0.9641 / -28.28% | FAIL (O_DD) | FAIL | FAIL | +0.1054 |
| B136 | C_CSTARPRED | N=40 H=63 | 13.89% / 0.9641 / -28.28% | FAIL (O_DD) | FAIL | FAIL | +0.1054 |

Bars: SPY OOS 15.21% / 0.8711 / -33.72% (U56), 15.33% / 0.8767 / -33.72% (B136); RULES v2 @10 bps
OOS 9.45% / 1.2762 / -12.05% and 7.88% / 1.1059 / -12.24%. Over all 54 cells at 10 bps:
**4b full 8, 4b OOS 9, 4a 0**. **Selecting on cost headroom is WORSE than selecting on IS Sharpe
on both panels** — the only chooser that reaches a 4b pass here is the incumbent IS-Sharpe one.
Independent of the choosers, the IS-only parameter-free form matches the IS-only truth at median
|err| **3.75 bps**, max 10.74, 94% of the 17 cells with a finite IS c* — the form validates on a
window it was never scored on, which is the part of this run that survives.

**SURVIVORSHIP (PROTOCOL rule 9).** U56 and B136 are current-constituent lists. Every level is
optimistic and every breakeven rung — true or predicted — is an UPPER bound on the cost a real
book of this kind could have paid.

# Idea 628 — does the SCALE channel need its own pre-rule-8 gate? (lane C, 2026-09-10)

**ANSWERED: yes, it needs its own gate. KILL of the queue's second horn — idea 185's leak law does
not price the same thing more cheaply.** No RULES change, no book promoted, no KEEP claimed.

## Gates (five, all pass)
| gate | value | tol |
|---|---|---|
| G1 `fast_backtest` == `engine.backtest` | 1.388e-17 ret / 3.331e-16 turn | 1e-12 |
| G2 cost-rung identity @25bps | 1.388e-17 | 1e-12 |
| G3 idea 623's committed `.arms.csv`, 363 shared rows | 4.441e-16 | 5e-3 |
| G4 causal scale-free control clears T1 and T2 | 0.000e+00 | 0 |
| G5 idea 623's FLAGS under a **new RNG seed**, 20 shared keys | 0 T1 / 0 T2 disagreements | 0 |

## The instrument (T2-cleared set: 14 of 26 keys, 6 scale-leaking)
| screen | TP | FP | FN | TN | AUC (T2-cleared) | AUC (all 26) | implementable at the rule-8 decision point? |
|---|---|---|---|---|---|---|---|
| T1 (structural, idea 433) | 6 | 0 | 0 | 8 | 1.0000 | 1.0000 | yes — reads no returns at all |
| LEAKH (185's law, 252d fwd, IS-only inputs) | see ladder | — | — | — | 1.0000 | 0.6438 | yes |
| LEAKT (185's published oracle form) | see ladder | — | — | — | 0.9792 | 0.6875 | **no** |

**0 of the 38 published ladder points reproduce T1's reading.** τ=0.05 catches all 6 leaks and kills
VOL20; τ=0.10 catches 3 of 6 and kills none.

## The band (post-hoc, ORACLE-PLACED — labelled as such everywhere)
LEAKH's separating band is **(0.0733, 0.0753], width 0.0020 = 0.040 of one ladder step**. On the
early half of its own IS date set it is (0.0417, 0.0447]; on the late half it **does not exist**
(width −0.0215). The full-window τ\*=0.0743 misclassifies in both halves. LEAKT is not separable on
the full set at all (band −0.1518). T1's counterpart gap is **166 rank steps**, with no threshold to
place.

## Consequence: the gate where it is proposed to sit (82 gates × 5 families × 3 rungs = 1,200 cells)
| gate @10bps | admits | rule-8 pick | OOS CAGR / Sharpe / MaxDD | vs SPY | vs RULES v2 |
|---|---|---|---|---|---|
| NONE | 26 | FWDRET/POS/m=1.00 | 39.03% / 2.198 / −26.70% | +1.316 | +1.640 |
| T1 alone | 16 | FWDRET/POS/m=1.00 | 39.03% / 2.198 / −26.70% | +1.316 | +1.640 |
| T2 alone | 14 | PXRANGE/NEG/m=1.00 | 16.04% / 1.037 / −26.53% | **+0.155** | +0.479 |
| **T1&T2** | 8 | VOL20/NEG/m=0.50 | 5.79% / **0.467** / −26.88% | **−0.415** | −0.091 |
| T2&LEAKH>τ\* (oracle-placed) | 8 | VOL20/NEG/m=0.50 | 5.79% / 0.467 / −26.88% | −0.415 | −0.091 |

SPY OOS 15.45% / 0.882 / −33.72%; RULES v2 3.77% / 0.558 / −14.58%; RULES v1 6.66% / 0.499; control
6.23% / 0.434. **T1 given T2 changes the pick at 3/3 rungs**; 19 of 82 gates are honest at all three
rungs and every one is T1&T2, an oracle LEAKT gate, or τ\*. At τ\* the leak-law gate admits **exactly
the T1&T2 set** — it matches the certificate only when placed by someone who already knows the answer.

PROTOCOL 4 over all 471 arms: **4a 0/471, 4b 0/471** (MaxDD binds 468). Predictions P1/P2/P3/P6 HIT;
P4 and P5 MISS, and both misses are the finding.

Survivorship (PROTOCOL 9): SMALL430 is a survivor of a survivor, filtered by `data/small_meta.csv`'s
own full-sample `max_1d_move` — a terminal-dated filter T2 itself flags. No number here is a capital
claim.

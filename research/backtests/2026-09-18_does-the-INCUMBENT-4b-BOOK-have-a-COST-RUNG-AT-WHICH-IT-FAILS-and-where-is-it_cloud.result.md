# Idea 1277 (lane cloud, idea 2 of 2, 2026-09-18) — does the INCUMBENT 4b BOOK have a COST RUNG AT WHICH IT FAILS, and WHERE IS IT?

**ANSWERED: YES, AT 118 bps UNDER THE RECORD'S FLAT MODEL AND 84 NOMINAL bps UNDER A VOL-SCALED ONE — AND THOSE ARE THE SAME NUMBER. The 34-bp gap is entirely a LEVEL fact (the book trades names 1.4176x the panel median vol, so PROTOCOL's 10 bps is 14.18 bps actually paid), not a shape fact: restated in EFFECTIVE bps the two models agree to +0.9% on four of five legs. KILL (capital) — no new book, no RULES/PROTOCOL change.** 15 of 15 gates, 14s, offline, deterministic.

## The construction
Dial 1 = COST RUNG {0, 10, 25, 50, 75, 100, 150, 200} bps (the queue's own extension), plus a FINE 0..400 bps curve at 1-bp resolution so every failing rung is SOLVED. Dial 2 = COST MODEL {M_PROP — the record's flat charge on traded notional; M_VOLSPREAD — the same rung redistributed as `c * clip(vol20_i / median_j vol20_j, 0.25, 4.0)` bps of each name's OWN traded notional, a half-spread proxy that is wider on volatile names and widens for the whole book when volatility rises}. **208 published books, 26 (book, model) fine-ladder solutions.** Headline object: the standing 2026-09-04 book (U56 / N=20 / H=126 / gross 0.75 / weekly). Reported at every rung and model, not as dials: U56 anchor A's full 9-rung H ladder, U56 anchor B (N=12 / gross 0.55 / monthly) at H=63 and H=252, the same construction on B135 and SMALL663, SPY (costless at every rung) and live RULES v2 re-run at the matched rung.

## The incumbent, rung by rung (M_PROP | M_VOLSPREAD)
| nominal | eff. bps (VS) | CAGR | Sharpe | MaxDD | H1/H2 | OOS CAGR / Sharpe / MaxDD | drag pp/yr | 4b |
|---|---|---|---|---|---|---|---|---|
| 0 | 0.0 | 15.95% | 1.1639 | -19.08% | 1.228/1.122 | 17.39% / 1.1898 / -19.08% | 0.000 | PASS |
| 10 | 10.0 \| 14.2 | 15.62% \| 15.48% | 1.1424 \| 1.1335 | -19.13% \| -19.14% | 1.205/1.101 \| 1.196/1.092 | 17.04% / 1.1690 \| 16.89% / 1.1598 | 0.290 \| 0.411 | PASS \| PASS |
| 25 | 25.0 \| 35.4 | 15.12% \| 14.77% | 1.1101 \| 1.0878 | -19.20% \| -19.29% | 1.171/1.070 \| 1.148/1.048 | 16.52% / 1.1377 \| 16.13% / 1.1145 | 0.724 \| 1.026 | PASS \| PASS |
| 50 | 50.0 \| 70.9 | 14.29% \| 13.60% | 1.0562 \| 1.0114 | -19.35% \| -19.54% | 1.114/1.018 \| 1.068/0.974 | 15.66% / 1.0855 \| 14.89% / 1.0390 | 1.448 \| 2.053 | PASS \| PASS |
| 75 | 75.0 \| 106.3 | 13.46% \| 12.44% | 1.0022 \| 0.9349 | -19.51% \| -19.78% | 1.057/0.966 \| 0.988/0.899 | 14.80% / 1.0332 \| 13.66% / 0.9633 | 2.172 \| 3.079 | PASS \| PASS |
| 100 | 100.0 \| 141.8 | 12.64% \| 11.29% | 0.9480 \| 0.8582 | -19.66% \| -20.03% | 1.000/0.914 \| 0.908/0.825 | 13.95% / 0.9808 \| 12.44% / 0.8875 | 2.896 \| 4.106 | PASS \| **FAIL L_H1** |
| 150 | 150.0 \| 212.6 | 11.02% \| 9.02% | 0.8396 \| 0.7046 | -19.97% \| -20.51% | 0.885/0.810 \| 0.747/0.676 | 12.27% / 0.8758 \| 10.03% / 0.7357 | 4.344 \| 6.158 | FAIL L_H1,L_H2 \| FAIL all five |
| 200 | 200.0 \| 283.5 | 9.42% \| 6.80% | 0.7310 \| 0.5513 | -20.27% \| -22.14% | 0.770/0.706 \| 0.586/0.528 | 10.61% / 0.7708 \| 7.68% / 0.5842 | 5.792 \| 8.211 | FAIL all five \| FAIL all five |

Bars, unchanged at every rung (SPY pays no turnover — idea 1063's one-sided handicap, stated not hidden): U56 SPY 15.13% / 0.8849 / -33.72%, halves 0.9600/0.8236, OOS 15.28% / 0.8747; 4b DD cap -20.2304%, CAGR floor 10.5938%. Live RULES v2 at the matched rung: 1.2268/-12.03% (0 bps), 1.2018/-12.05% (10), 1.1015/-12.16% (50), 0.9757/-12.28% (100). **4a fails at 0 of 208 cells** — the live book's -12% drawdown against a growth book, rule 4's own stated reason for path 4b.

## The exact failing rungs, solved on the fine ladder
| leg | M_PROP | M_VOLSPREAD (nominal) | M_VOLSPREAD in EFFECTIVE bps | shape effect |
|---|---|---|---|---|
| whole 4b | **118** | **84** | 119.1 | +1.1 bps (+0.9%) |
| L_H1 | 118 | 84 | 119.1 | +1.1 (+0.9%) |
| L_H2 | 144 | 101 | 143.2 | -0.8 (-0.6%) |
| L_OOS | 151 | 105 | 148.8 | -2.2 (-1.4%) |
| L_DD | 194 | 121 | 171.5 | **-22.5 (-11.6%)** |
| L_CAGR | 164 | 116 | 164.4 | +0.4 (+0.3%) |

**The answer to the queue's question is 118 bps of effective cost, and the first leg to go is the FIRST-HALF Sharpe, not the drawdown cap.** Pre-declared outcome (B) fires on the nominal reading and (A) on the effective one; both are published because the distinction is the finding. The one leg where the model's SHAPE genuinely matters is the path-dependent one: charging the same total cost in the volatile weeks rather than evenly costs the drawdown cap 11.6% of its headroom, because the charge lands inside the drawdown instead of being spread over the recovery.

## The level fact, which is the part that should change how the record quotes costs
The incumbent's traded notional is **1.4176x the panel's median vol20**, so a "10 bps" assumption on this book is **14.18 bps actually paid**, and PROTOCOL rule 2's rung understates this book's cost by 42%. The ratio rises monotonically with the min hold — 1.1983 / 1.2343 / 1.2991 / 1.3219 / 1.3482 / 1.3849 / **1.4176** / 1.4360 / 1.4738 at H = 5 / 10 / 21 / 42 / 63 / 90 / **126** / 189 / 252 — i.e. the longer the hold, the more the remaining trading concentrates in high-volatility names. It is 1.5842 on U56 anchor B H=252, 1.3803 on B135 and 1.3593 on SMALL663.

## Neighbours and other panels (same fine ladder)
U56 anchor A: H=5 fails 4b at 25 bps, H=10 at 35, H=21 at 9 (the DD leg — idea 1275's finding, reproduced), H=42/63/90/189/252 already fail at 0 bps on the DD cap. **The incumbent is the ONLY rung of its own ladder with three-figure headroom.** U56 anchor B: H=63 fails at 39 bps (the CAGR floor), H=252 at 128 bps flat / 81 nominal (128.4 effective). B135 and SMALL663 fail at 0 bps on the DD cap under both models. Grid totals: **4b 40 of 208; by rung under M_PROP 6/5/4/2/2/2/0/0 of 13 and under M_VOLSPREAD 6/5/4/2/2/0/0/0** — the vol-scaled model costs the grid its last two passes at 100 bps.

## Rule 8 (OOS read once)
48 decisions = 2 models x 8 rungs x 3 IS-only choosers over U56 anchor A's nine rungs, H chosen on warm-up..2016-12-31 alone. **Pick-minus-incumbent OOS Sharpe -0.0744 mean, positive at 5 of 48, reach (pick == incumbent) 0 of 48, 4b among the picks 6 of 48.** By model: M_PROP -0.0777 (positive 1 of 24), M_VOLSPREAD -0.0711 (4 of 24); picks are H ∈ {10, 21, 189} under both. **No IS-only chooser reaches the incumbent at any rung under either cost model**, which is the same negative result 1236/1274/1275 report for this ladder and is the reason nothing here is promoted.

## Gates
15 of 15 PASS. G1 fast runner == engine.backtest 1.4e-17. G2 CROSS-RUN committed incumbent triple on a tape truncated to 2026-09-15, maxdiff 1.70e-04 (the daily tape restatement, published not toleranced). **G3 CROSS-RUN agreement with idea 1275's grid committed earlier today across the five shared rungs: 2.22e-16.** G4 the realised effective/nominal ratio published at every headline book. G5 M_VOLSPREAD with the multiplier pinned to 1.0 IS M_PROP bit for bit (0.000e+00). G6 Sharpe and CAGR non-increasing in the rung at every book x model (0 violations). G7 the 0-bps cell IS the gross series under both models. G8 live RULES v2 MaxDD -0.1205. G9 determinism 0.000e+00. G10 the multiplier inside [0.25, 4.0] on all three panels. G11 the re-charged live comparand IS a direct 10-bps engine run (0.000e+00), which is what makes the 401-rung 4a ladder exact rather than approximate.

## What the record should take from this (offered, not adopted; rule 6 reserves that for a Sunday review)
*A committed cost rung is a NOMINAL number. Any book whose traded notional is not median-volatility pays a multiple of it, so a cost claim should state the book's realised effective/nominal ratio beside the rung — on the incumbent that multiple is 1.4176, and PROTOCOL rule 2's 10 bps is 14.18 bps paid.*

## Survivorship (rule 9)
U56 and B135 are CURRENT-constituent lists; SMALL663 is a current sub-$2B screen (`max_1d_move >= 1.0` dropped first). The headroom measured here is an UPPER bound in a second, specific way beyond the usual level bias: the names that would have been delisted are not in the panel to be traded expensively on the way out, and those are exactly the trades a vol-scaled charge would price worst. The headline is a CONTRAST between cost rungs and cost models on one book and one tape, first-order immune to a level bias moving all rungs together; the 4a/4b legs and the failing rungs themselves are not.

# Idea 926 — does the ZERO-COST pass-to-BASE-RATE INVERSION hold on MONTHLY books? (cloud, 2026-09-15)

**ANSWER: YES — and it is 680's headline that is the cadence-specific one. At monthly cadence the
inversion SURVIVES the PROTOCOL rung: ρ(4b pass, null base rate) = +0.4349 at 10 bps against
weekly's −0.0728, and 7 of 30 monthly cells still leave a coin flip clearing 4b more than 5% of
the time (max 40.8%) where weekly leaves 0 of 30. KILL for "rule 2 already does the clause's whole
job" as a cadence-free statement.**

Script `2026-09-15_does-the-ZERO-COST-to-BASE-RATE-INVERSION-hold-on-MONTHLY-books_cloud.py`.
Idea 680's 30 cells (5 book keys × 3 panels × 2 claim sets) re-run at **freq='M'** beside its own
weekly arm, 250 draws per cell (the first 250 seeds of 680's nested 1000), 3 cost rungs, both
windows. Gates **7 of 7**, including **G3 an EXACT cross-run reproduction** of all 90 of 680's
committed 250-draw weekly rows (worst |delta| 2.75e-14 over base rate, book Sharpe/CAGR/MaxDD,
both gross columns, null mean Sharpe and percentile).

*One gate was corrected, not relaxed, before the published run:* G1's first draft compared
`ctx.run` with `engine.backtest` over the whole stream and read NaN at both cadences, because
`engine.backtest` itself emits NaN on row 0 (`w_target` is shifted, so the first rebalance reads a
NaN row). It now compares from row 260 on the RULES v2 band book — idea 680's own G1 construction
and the warm-up cut every published metric in this record uses — and reads **W 8.67e-18 /
M 1.21e-17**. No result number changed between the two runs; the draw seeds and every cell are
identical.

## The answer — ρ at every rung, both cadences

| freq | cost | cells | 4b | ρ(pass, base rate) | base rate \| pass | base rate \| fail | mean | max | >0.05 | >0.50 | outside null |
|---|---|---|---|---|---|---|---|---|---|---|---|
| W | 0 | 30 | 7 | **+0.6569** | 0.5869 | 0.0722 | 0.1923 | 1.000 | 12 | 5 | 1 |
| W | 10 | 30 | 4 | **−0.0728** | 0.0000 | 0.0005 | 0.0004 | 0.012 | **0** | 0 | 4 |
| W | 25 | 30 | 2 | UNDEF (every base rate 0.000) | 0.0000 | 0.0000 | 0.0000 | 0.000 | 0 | 0 | 2 |
| M | 0 | 30 | 3 | **+0.4131** | 0.3600 | 0.0616 | 0.0915 | 0.964 | 8 | 2 | 1 |
| M | 10 | 30 | 3 | **+0.4349** | 0.1640 | 0.0204 | 0.0348 | 0.408 | **7** | 0 | 1 |
| M | 25 | 30 | 3 | **+0.4245** | 0.0160 | 0.0006 | 0.0021 | 0.044 | 0 | 0 | 3 |

680's weekly reading reproduces (+0.6569 at 250 draws against its committed +0.6387 at 1000;
−0.0728 against its −0.1048 — the sign and the collapse both reproduce, the third digit is the
draw budget). The monthly column is the finding: **ρ does not fall between 0 and 25 bps at all**
(+0.4131 → +0.4349 → +0.4245), i.e. under monthly cadence the association between clearing 4b and
having an easy null is essentially cost-invariant, while under weekly cadence it is erased between
0 and 10 bps.

## Why — the premise checks out, and it is the whole mechanism

| | W turnover | M turnover | M/W |
|---|---|---|---|
| TOP5 (U56/B136/SMALL) | 17.7x / 21.3x / 31.3x | 7.7x / 9.5x / 13.2x | 0.436 / 0.444 / 0.421 |
| TOP20 | 9.6x / 13.8x / 21.3x | 4.3x / 6.3x / 10.1x | 0.449 / 0.458 / 0.476 |
| EWELIG | 8.2x / 8.3x / 11.9x | 3.6x / 3.8x / 5.5x | 0.443 / 0.456 / 0.460 |
| BAND03 | 1.8x / 2.0x / 2.6x | 1.2x / 1.4x / 1.6x | 0.696 / 0.692 / 0.622 |

**H_TURN PASSES**: median M/W ratio **0.4483** over the 30 cells. The queue's "a third" is nearer
45%, and the exception is informative — BAND03, the live baseline's own construction, only falls
to ~0.69 because it barely trades to begin with. A 10 bps rung costs a weekly TOP5 book about
2.1 pp of return a year and a monthly one about 0.9 pp; that difference is the entire reason the
null survives the rung on one cadence and not the other.

## Where the surviving base rates sit (10 bps, per cell)

Every monthly cell above the 0.05 bar is on **U56**: TOP20 **0.408**, TOP10 0.188, TOP5 0.100,
EWELIG 0.064 (CORE); TOP10 0.056, TOP20 0.024, BAND03 0.020, TOP5 0.012 (EXT). B136 contributes
TOP20 0.080, TOP10 0.064, TOP5 0.024; **SMALL439 is 0.000 on all 20 cells at both cadences**. So
the effect is a large-cap, mega-cap-concentrated phenomenon, exactly as 680 found at 0 bps — the
cadence change widens it, it does not move it.

**The single most capital-relevant number in this run:** `U56 / CORE / TOP20` — the key of the
record's standing 2026-09-04 KEEP-4b incumbent — clears 4b at monthly cadence AND its own exactly
gross-matched coin-flip null clears the same bar on **40.8% of 250 draws at 10 bps**. At weekly
cadence the same cell's null reads 0.000. The monthly version of the incumbent's book shape is
not distinguishable from a coin flip by 4b.

## Hypotheses (all pre-registered in the script docstring)

| bar | result | reading |
|---|---|---|
| H_TURN | **PASS** | median M/W turnover 0.4483 (bar ≤ 0.50) — the premise is real. |
| H_SURVIVE | **PASS** | ρ(M, 10 bps) **+0.4349** ≥ +0.30, base rate 0.1640 for passers vs 0.0204 for failers. The inversion survives PROTOCOL rule 2's rung. |
| H_ZERO | **PASS** | ρ(M, 0 bps) +0.4131 — the inversion reproduces on monthly books at zero cost. |
| H_LEVEL | **PASS** | 7 of 30 monthly cells above 0.05 at 10 bps (bar ≥ 6), against 0 of 30 weekly. |
| H_COST | **FAIL** | the LEVEL collapse is not cadence-free: mean base rate falls 0.1923 → 0.0004 weekly (−0.192) but only 0.0915 → 0.0348 monthly (−0.057, under the 0.10 bar). Failing this bar is what passing H_SURVIVE is made of. |
| H_WF | **PASS** | 5 of 12 rule-8 picks clear 4b out of sample — see below. |

## Rule 8 (choice on 2009–2016 only, 2017–2026 read once)

| freq | cost | pick | IS Sharpe | OOS CAGR / Sharpe / MaxDD | SPY OOS | v2 OOS | OOS 4a/4b | its null's base rate |
|---|---|---|---|---|---|---|---|---|
| W | 0 | B136 EXT TOP10 | 1.160 | 19.40% / 0.887 / −27.86% | 15.33% / 0.877 / −33.72% | 8.11% / 1.136 / −12.21% | 0/0 | 0.016 |
| W | 0 | U56 EXT BAND03 | 1.131 | 12.95% / 1.301 / −15.88% | 15.27% / 0.874 / −33.72% | 9.66% / 1.302 / −12.03% | 0/**1** | **0.972** |
| W | 10 | U56 EXT BAND03 | 1.105 | 12.68% / 1.277 / −15.91% | same | 9.46% / 1.277 / −12.05% | 0/**1** | 0.000 |
| W | 25 | U56 EXT BAND03 | 1.067 | 12.28% / 1.240 / −15.96% | same | 9.17% / 1.241 / −12.09% | 0/**1** | 0.000 |
| M | 0 | U56 EXT TOP5 | 1.326 | 21.79% / 0.872 / −34.53% | same | 9.70% / 1.240 / −14.36% | 0/0 | 0.032 |
| M | 10 | U56 EXT TOP5 | 1.283 | 20.50% / 0.832 / −34.61% | same | 9.56% / 1.224 / −14.38% | 0/0 | 0.012 |
| M | 25 | U56 EXT TOP5 | 1.218 | 18.59% / 0.773 / −34.72% | same | 9.35% / 1.200 / −14.41% | 0/0 | 0.000 |

**OOS-window 4b 5 of 12 picks, 4a 0 of 12.** Two readings worth keeping. (1) The monthly IS
chooser picks `U56/EXT/TOP5` at every rung and it fails 4b out of sample on the DD cap and the
Sharpe leg together (−34.61% against the −20.23% cap; OOS Sharpe 0.832 against SPY's 0.874) — the
monthly cadence buys turnover savings and pays for them in drawdown. (2) The one weekly pick that
does clear 4b at 0 bps, `U56/EXT/BAND03`, has a null base rate of **0.972** at that rung: at zero
cost a coin flip in its own gross path clears 4b 97% of the time. That is 680's inversion in one
row, and it is the reason the clause was proposed at all.

## Verdict

**KILL** for 680's conclusion *as a cadence-free statement*, and a **PARK** for the base-rate
clause it killed. 680 was right that 10 bps empties the null on WEEKLY books and right that the
clause adds nothing there. It does not follow — and this run shows it does not hold — that rule 2
does the clause's job at the cadence real capital would actually trade: on monthly books the
association is +0.4349 at 10 bps and +0.4245 at 25 bps, and the incumbent's own book shape leaves
a 40.8% coin-flip base rate. The cheap repair is a REPORTING line, not a new bar: any 4b pass on a
book turning over under ~10x a year should be published with its own gross-matched null base rate
beside it. Nothing promoted; no RULES, PROTOCOL, scan.py, bot.py or baseline.py change made.

**SURVIVORSHIP (PROTOCOL 9):** all three panels are current-constituent lists, so a coin flip
drawn here is a better book than one drawn in real time — every base rate above is an UPPER bound
and each book's standing inside its null is a LOWER bound. That direction favours this run's
conclusion, so the conclusion is the conservative one; the 4b levels themselves (SPY-referenced)
are upper bounds and are not protected by the same-tape argument.

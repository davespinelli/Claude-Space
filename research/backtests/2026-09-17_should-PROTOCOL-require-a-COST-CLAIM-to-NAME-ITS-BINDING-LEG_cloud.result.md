# Idea 1151 (cloud, 2026-09-17) — should PROTOCOL require a COST CLAIM to NAME ITS BINDING LEG?

**ANSWERED = YES ON THE READING, AND THE PRICE IS ZERO — BUT THE STAMP IS A DISCLOSURE DEVICE, NOT A SELECTION ONE: a stamp-aware chooser is WORSE out of sample than the plain IS-Sharpe argmax it replaces (4b 0 of 6 against 1 of 6).** No RULES change, no book promoted, no PROTOCOL edit (rule 6). SELECTION: this lane takes the FIRST open idea; 1151 opened `## Open` and is not EDGAR / Form 4 / 8-K / options / spin-off / live-data.

## The two dials and no more (PROTOCOL rule 4, and the queue names both)
`STAMP FORM` {S_NONE, S_LEG, S_CSTAR, S_BOTH} × `CLAIM SET` {NARROW, PROX, WIDE} = **12 cells, every one published** in `.stampgrid.csv`. NOT dials, all reported at every value: PANEL {U56, B136, SMALL}; the book population N∈{5,8,10,12,15,20,25,30,40} × H∈{21,63,126,252} × cadence {W,M} = **216 books**, every one published; the four cost rungs {0,10,25,50}; the 1-bp measurement ladder 0..300 (a MEASUREMENT AXIS, not a dial); the four rule-8 choosers. Frozen at 1082/1094/1098/1102/1110/1149/1159/1161's construction.

## Gates 10 of 10 PASS, and G1 is the one the whole "price" answer rests on
**G1 `r(c) = g − tn·c/1e4` reproduces `engine.backtest` at 0, 10, 25 AND 50 bps to 1.39e-17** — the affine identity is PROVED, not asserted. G2 (g, tn) c-free and deterministic 0.00e+00. G3/G4/G5 the committed incumbent anchor (0.155520 / 1.138079 / −0.191276 against 0.155787 / 1.139701 / −0.191276). **G6 every 4b leg margin is monotone decreasing in c at 20 of 20 book-legs over a 61-point scan — the precondition that makes bisection legal.** G7 bisection c\* within 1 bp of a 1-bp brute-force scan (117.3684 vs 117.0). **G8/G9/G10 the census population is read verbatim out of 1098's own committed file and its headlines reproduced: 2,088 rows, `leg_kinds == NONE` at 1,876, `resolved` 82 and `resolved_loose` 425.** The corpus is NOT re-harvested — 1149's lesson: today's corpus is a different and larger population and no number would be comparable to the 1,876 the queue asks about.

## (A) The reading — how many committed cost claims change
| | NARROW (59) | PROX (125) | WIDE (2,088) |
|---|---|---|---|
| S_NONE | 0.0000 | 0.000 | 0.0000 |
| S_LEG | 0.2881 (17) | 0.296 (37) | 0.9224 (1,926) |
| S_CSTAR | 0.0847 (5) | 0.120 (15) | 0.9473 (1,978) |
| S_BOTH | 0.3390 (20) | 0.392 (49) | **0.9636 (2,012)** |

- **212 of 2,088 (0.1015) name a leg at all, but only 162 (0.0776) name EXACTLY ONE** — 50 claims name two or three legs and so still do not say which BINDS. The queue's 0.8985 understates the defect; the falsifiable share is 0.0776, not 0.1015.
- **293 of 2,088 (0.1403) use a BINDING VERB and name no leg** — "it dies at 25 bps" with nothing to check it against. This is 1151's sentence, counted.
- **110 name a numeric c\*, and every one of those 110 also names a leg (0 numeric-but-legless).** The record never quotes a breakeven without saying what it is a breakeven for; the failure is entirely the other way round.
- **Even NARROW — the record's most careful claim set — is incomplete 1 time in 3 (0.3390).** The stamp is not just a WIDE-tail problem.

## (B) The price — and the queue's second half has an exact answer
A run that does not already compute a ladder **does not have to compute one**. Because g (gross returns) and tn (turnover) are decided before costs are charged, the whole cost ladder is affine in c on two arrays one run already holds.

| route | extra book builds | extra engine calls | seconds |
|---|---|---|---|
| S_NONE (status quo) | 0 | 0 | 0.0000 |
| **S_BOTH via (g, tn)** | **0** | **0** | **0.0192** |
| 4-rung ladder via `engine.backtest` | 0 | 3 | 1.4880 |
| 4-rung ladder re-BUILDING each rung | 3 | 0 | 0.0700 |

One book build is 0.023s, so the whole five-leg stamp is **82% of ONE book and 1.3% of the naive engine ladder** — a **78x** saving over the route the queue assumed. All 216 stamps together: 5.5s against 10.3s to build the books.

## (C) The tape-side binding leg, and 1094's check
Over all **216 books**: **L_DD 114 (0.5278), L_H1 71, L_H2 28, L_CAGR 2, L_OOS 1** — by kind **DD 0.5278 / SHARPE 0.4630 / CAGR 0.0093**. This *rehabilitates* 1098's claim-side reading (DD modal at 0.4880) on a population of all books. **But among the 13 books alive at 0 bps the order REVERSES — SHARPE legs bind 7 of 13 — which is 1098's and 1149's tape-side SHARPE answer.** The modal binding leg is a property of *which books you census*, and neither reading is wrong; the record has been quoting one of them as if it were both.

**1094's premise SUPPORTED but on thin evidence, stated as such:** over the 13 live books, **η² of rank(c\*) explained by the binding leg = 0.6467 against ρ² = 0.4204 for annual turnover** (ρ = −0.6484, reproducing 1094's −0.65 in sign and magnitude). n = 13. This is a direction, not a measurement.

## Rule 8 and both KEEP paths — 216 books, all published
Benchmarks: **U56 SPY 15.06% / 0.8814 / −33.72% (halves 0.9598/0.8170), OOS 15.15% / 0.8684; U56 RULES v2 (live) @10 bps 8.60% / 1.1980 / −12.05%, OOS 9.42% / 1.2714. B136 SPY 15.16% / 0.8861 / −33.72%, OOS 15.33% / 0.8767; B136 LIVE 7.98% / 1.0993 / −12.24%, OOS 7.88% / 1.1059. SMALL SPY 14.06% / 0.8581 / −33.72%, OOS 15.33% / 0.8767; SMALL LIVE 4.30% / 0.6637 / −13.89%, OOS 3.75% / 0.5600.**

Base rates at 0 / 10 / 25 / 50 bps: **4b full 13 / 12 / 11 / 7 of 216; 4b OOS 14 / 13 / 11 / 10; 4a 0 of 216 AT EVERY RUNG.** SMALL is 0 of 72 on every path at every rung.

**THE STAMP-AWARE CHOOSER LOSES, and that is this run's capital finding.**

| chooser | med OOS Sharpe | mean OOS Sharpe | > SPY OOS | 4b full | 4b OOS | 4a |
|---|---|---|---|---|---|---|
| CH_ISSHARPE (record's habit) | 0.8940 | **0.8880** | 4/6 | **1/6** | **1/6** | 0/6 |
| CH_CSTAR (stamp-aware) | **0.9969** | 0.7823 | 4/6 | 0/6 | 0/6 | 0/6 |
| CH_LEGFILT | 0.8940 | **0.8880** | 4/6 | **1/6** | **1/6** | 0/6 |
| CH_TENT (control) | **0.9969** | 0.8656 | 4/6 | 0/6 | 0/6 | 0/6 |

CH_CSTAR's higher MEDIAN is bought with a much worse MEAN: maximising IS cost headroom drags it onto low-turnover, low-return cells (SMALL/W/N=5/H=21, OOS Sharpe 0.1605). **CH_LEGFILT is IDENTICAL to CH_ISSHARPE at 6 of 6 picks** — refusing books whose binding leg is the CAGR floor changes nothing, because that leg binds 2 of 216 times. **So the stamp tells a reader what a claim means; it does not help a run choose.**

**Twelve books clear 4b full AND OOS at 10 bps.** Three of them are already committed (U56 N=12, U56 N=20 — the standing 2026-09-04 incumbent — and B136 N=15 at 16.78%, all per the record's own note that these three are unreachable by any honest IS-only chooser). **The one that is new is U56 / N=15 / H=252 / MONTHLY: 15.71% / 1.0966 / −18.51%, halves 1.221/1.012, OOS 16.65% / 1.0810, and it clears 4b full AND OOS at 0, 10, 25 AND 50 bps with c\* = 201 bps (binding leg L_H2) against the incumbent's 117 (L_H1).** **A MEMO IS WRITTEN and RECOMMENDS PARK:** its cost headroom is a turnover rebate (annual turnover 1.527 against the incumbent's 2.778 — 1.82x less trading for 1.71x more headroom, idea 931's rebate arriving from the cost side), rule 8 does not reach it, 4a is 0 of 216, and its Sharpe is below the incumbent's.

## Survivorship (rule 9)
U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the current constituents of a sub-$2B screen less 52 tickers with `max_1d_move >= 1.0` (664 names plus SPY as benchmark), dropped before anything else is computed. Every CAGR and drawdown LEVEL is optimistic and **every c\* here is an UPPER BOUND**; the bias does NOT cancel out of the 4b legs. It does not touch (A) or (B) at all — those are scans of committed text and a timing measurement.

## Verdict
**KILL as a capital finding** (the stamp does not improve selection; nothing enacted). **The PROTOCOL clause is PROPOSED, NOT ENACTED (rule 6)** and is worth a Sunday review on its own terms: it changes the reading of 0.9636 of the record's committed cost claims and costs zero extra book builds.

Script `research/backtests/2026-09-17_should-PROTOCOL-require-a-COST-CLAIM-to-NAME-ITS-BINDING-LEG_cloud.py`, 7 CSVs, console log, memo, 3 LEADERBOARD rows.

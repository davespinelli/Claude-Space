# Idea 779 (lane C, 2026-09-11) — does-the-MIN-GAP-PAIR-restatement-change-any-published-VERDICT-not-just-the-count

**ANSWERED — YES, IT MOVES PUBLISHED VERDICTS, AND NO, NONE OF THEM CAN BE RETIRED ON IT / KILL for capital.**

## Question

Idea 778 re-scored idea 567/774's 607-claim panel-ordering census against the MIN-GAP PAIR bar
(RSS restricted to the two panels bracketing the margin, rho = 0) and reported the movement as a
count: net vs POOLED **+21 / +18 / +20 / +21** at D = 3/6/12/24. The queue's objection: a moved
count is not a moved conclusion. This run **reads** the moved claims and asks whether any of them
carries a headline the rest of the record leans on.

## Gates — ALL PASS (after one declared failure, below)

| gate | what | result |
|---|---|---|
| G1 harvest | fresh harvest of 781 committed md files reproduces 567/774/778's census | **607 of 607** (this run harvests 610; surplus = files committed after 778 ran) |
| G2 floors | per-parent floors rebuilt from prices vs 774/778's committed `.floors.csv`, 60 rows | max \|d\| **9.714e-17** (bar 1e-12) |
| G3 identity | `fast_backtest` vs `engine.backtest`, one book per parent | **0.000e+00** |
| G4 headline | 778's PAIR_INDEP net-vs-POOLED re-derived **twice** — from its own `.moves.csv` and rebuilt from prices | **+21/+18/+20/+21 = +21/+18/+20/+21 = +21/+18/+20/+21**, exact |
| G5 reliance | self- and same-run citation excluded; every leg must sit strictly inside 2–98% | VENUE 72.0%, CITED 27.3%, ECHO 44.5%, QUEUED 3.6%, ANY 93.6%, STRICT 40.2% |

**G5 failed on the first version of this script and is reported, not hidden.** That version let
`LEADERBOARD.md` and `QUEUE.md` count as *citing* files. PROTOCOL rule 5 makes them name every
committed script by construction, so CITED read **100.0%** and ANY read **100.0%** — a reliance
measure that convicts everything measures nothing. The leg was rebuilt with an INDEX exclusion
(the two index documents are excluded as citers, but remain eligible as venues) before any answer
was read.

## Two dials (PROTOCOL rule 4), all 10 points reported

CLAIM SET in {ALL, 2PANEL, 3PANEL, NESTED_PAIR, NZ} × BAR in {1.0, 2.0}.
Reported, never selected: D in {3,6,12,24}, period (FULL/IS/OOS), reliance leg (6), direction,
statistic family (5).

### Headline grid (D = 6, FULL)

| claim set | bar | n | moved | OUT→IN | IN→OUT | moved share | ANY-relied | STRICT |
|---|---|---|---|---|---|---|---|---|
| ALL | 1.0 | 607 | 18 | 18 | **0** | 2.97% | 15 | **8** |
| ALL | 2.0 | 607 | 48 | 48 | **0** | 7.91% | 46 | 17 |
| 2PANEL | 1.0 | 345 | 11 | 11 | 0 | 3.19% | 8 | 4 |
| 2PANEL | 2.0 | 345 | 28 | 28 | 0 | 8.12% | 27 | 6 |
| 3PANEL | 1.0 | 262 | 7 | 7 | 0 | 2.67% | 7 | 4 |
| 3PANEL | 2.0 | 262 | 20 | 20 | 0 | 7.63% | 19 | 11 |
| NESTED_PAIR | 1.0 | 366 | 13 | 13 | 0 | 3.55% | 10 | 5 |
| NESTED_PAIR | 2.0 | 366 | 21 | 21 | 0 | 5.74% | 21 | 7 |
| NZ | 1.0 | 465 | 18 | 18 | 0 | 3.87% | 15 | 8 |
| NZ | 2.0 | 465 | 48 | 48 | 0 | **10.32%** | 46 | 17 |

**Every move, at every one of the 10 points, is OUT→IN — 0 acquittals in 259 moves.** The min-gap-pair
bar only ever makes a published gap *less* distinguishable, never more; 774's one-directional
asymmetry survives its own restatement.

## The answer to the queue's question

**10 of the 18 moved claims live in a CONTROL document** — LEADERBOARD.md 5, CHANGELOG.md 3,
QUEUE.md 2 — and **8 of 18 are STRICT** (control document **and** cited or echoed by a different
run). Named examples, each of which becomes "not distinguishable from its floor" under the
restatement:

- `CHANGELOG.md` — **"H_DOMINANT FAIL at 43% (bar 75%)"**, the cadence-argmax verdict (margin 0.1370).
- `CHANGELOG.md` — **"the IS window … gives up 0.216 of OOS Sharpe to the no-ranking control"** (0.1160).
- `CHANGELOG.md` — **"THE BY-PRODUCT: the no-trade band, not the name count, is the turnover dial"** (0.1410).
- `LEADERBOARD.md` — the phase-spread row **"6W ALL 0.1518 / SMALL 0.2618 / U56 0.3957 / ETF 0.3862"** (0.1339).
- `LEADERBOARD.md` + `QUEUE.md` — **"THE ORDERING REVERSES … U56 −0.3642 > B136 −1.1499 > SMALL439 −1.2430"** (0.0931).

So the queue's premise is confirmed on its face: the restatement does not only move a count, it
moves headlines the record is still quoting.

## …and the two reasons it retires nothing

**H_LEAN FALSIFIED.** The movers are **not** enriched in relied-on claims. At the headline point
(ALL, bar 1.0, D=6, FULL) the mover ANY-rate is **83.3% against a non-mover base rate of 93.9%,
lift −10.6 pp**; STRICT is 44.4% against 40.1%, **lift +4.4 pp**. Across all 10 points the ANY lift
runs −20.1 pp to +7.0 pp and the STRICT lift −16.1 pp to +12.0 pp, straddling zero. The movers are
a **random draw from the census with respect to reliance** — the restatement hits load-bearing
claims at exactly the rate it hits everything else, so "10 of 18 sit in control documents" is the
base rate (72.0%) talking, not a finding about the restatement.

**H_MOVE FALSIFIED** at the top of the grid: 10.32% of the NZ subset moves at bar 2.0 (bar was 10%).

**WF-A kills the retirement outright.** Rebuilding the floors on IS returns only and on OOS returns
only and recomputing the whole mover set: **FULL 18, IS 35, OOS 11 movers, IS ∩ OOS = 1, Jaccard
0.0222** (34 IS-only, 10 OOS-only). Net vs POOLED by period: FULL +21/+18/+20/+21, IS
+32/+35/+25/+29, **OOS −2/+9/+15/+13 — the sign flips at D=3.** The *count* is stable (778's
finding); the *identity of which claims move* is not the same object out of sample. No individual
verdict can be retired on evidence that reshuffles this completely between halves of the sample.

## Rule 8 WF-B — the restatement priced as a decision rule

Act on the IS-best parent only if the IS span clears bar × the min-gap-pair floor **and** the
backing claim set survives the reliance filter; else stand down to the live book. OOS read once.

| book | acted | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|
| all 5 claim sets, bar 1.0 (NESTED_PAIR excepted) | 3 of 6 | 10.94% | 1.1966 | −15.06% |
| all 5 claim sets, bar 2.0; NESTED_PAIR bar 1.0 | 0 of 6 | 9.45% | 1.2747 | −12.05% |
| ALWAYS-ACT (778's control) | 6 of 6 | 13.00% | 1.1567 | −18.40% |
| **RULES v2 U56 (live book)** | — | **9.45%** | **1.2747** | **−12.05%** |
| **SPY** | — | **15.24%** | **0.8721** | **−33.72%** |

**Beating RULES v2 OOS Sharpe: 0 of 10. Beating SPY OOS Sharpe: 10 of 10.** Every rule that trades
the panel ordering gives up Sharpe and takes more drawdown than doing nothing; the rules that match
the live book are the ones that stand down in 6 of 6 cells, i.e. that never trade the ordering at
all — the third independent reproduction of idea 776's stand-down reading.

## KEEP paths

Full price grid (REAL panels + 774's independent draws, 900 books): **4a 2/900, 4b 52/900, BOTH
0/900**. REAL books: 4a 0/36, 4b 3/36 (`U56/MA-RS/g0.75/W`, `U56/MA-RS/g0.75/M`,
`B136/MA-RS/g0.75/W` — the MA-RS gate the record already holds, re-found for the fourth time).
Decision books: **4a 0/10, 4b 0/10, BOTH 0/10**; the binding leg on every one is CAGR.
**No candidate, no memo, no rule change.**

## PROTOCOL proposal (Sunday, not adopted)

Nothing to add to 778's amendment, and one thing *not* to do: do **not** back out the moved claims.
This run's own WF-A says the moved set has a Jaccard of 0.022 between the two halves of the sample,
so a retirement list built on the full sample would be a list of 18 claims of which ~1 would still
be on it if the record had stopped in 2016. If a future run wants to retire anything on a floor
comparison, the floor's own **period stability** has to be published beside it.

## Survivorship

`universe_broad.json` and the small panel are **current constituents**; every stock-side level
carries a survivorship premium and the LEVEL floors (SHARPE, CAGR, MAXDD) are lower bounds on true
dispersion. An arm-minus-arm premium on the same panel largely cancels it. The three parents start
on different dates (U56/B136 2008, SMALL 2010), inherited from 567's floor construction.

## Artefacts

`.grid.csv` `.floors.csv` `.census.csv` `.reliance.csv` `.movers.csv` `.verdicts.csv` `.g4.csv`
`.walkforward.csv` `.keeppaths.csv` `.console.txt`

Follow-ups: 788–790.

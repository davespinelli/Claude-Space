# Idea 962 (lane C, 2026-09-15) — does an IS-CHOSEN PHASE ever SURVIVE out of sample on ANY book?

**ANSWERED = YES, SIX TIMES IN 180 — WHICH IS LESS THAN HALF WHAT A COIN WOULD HAVE FOUND.
KILL for choosing the rebalance phase in sample.** No RULES change, no KEEP, no memo, no book
promoted; `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched (rule 6).

Script: `2026-09-15_does-an-IS-CHOSEN-PHASE-ever-SURVIVE-OOS-on-ANY-BOOK_C.py`
(`.grid.csv` 12,600 rows · `.walkforward.csv` 2,400 · `.families.csv` 300 · `.hypotheses.csv`
· `.console.txt`), 194.6 s.

## Gates — seven, all PASS, run before any hypothesis number was read
| gate | what | result |
|---|---|---|
| G0 | `offset_mask(·,per,0)` == `engine.rebalance_mask` on W/M/Q | 0 differing rows |
| G1 | `Ctx.run` == `engine.backtest` @10 bps, worse of M and Q | 2.082e-17 |
| G2 | BAND03 @0.75 == `rules_v2_weights` (the LIVE rules) | 0.000e+00 |
| G3 | **942's committed `grid.csv` replayed on 12,600 of 12,600 rows**, 13 columns | max abs 1.776e-15 |
| G4 | determinism (TOP20 / M / phase 3 re-derived twice) | 0.000e+00 |
| G5 | RULES v2 weekly 8.6227%/1.2014/−12.0549% == `engine.backtest(freq='W')` | 2.220e-16 |
| G6 | **every chooser is IS-ONLY**: picks invariant to permuted OOS columns | 0 of 1,800 mismatches |

REPORTED, not a gate: the record's published constants (RULES v2 8.6282%/1.2018/−12.0549%,
SPY 15.16%/0.8861/−33.72%) differ from today's cache by up to 1.494e-03 — a data-cache drift,
not a machinery difference; 942's own committed grid agrees with this run at 1e-15 (G3).

## The design (PROTOCOL rule 4: two tuned parameters)
TUNED 1 **chooser**, 6 levels, all reported, all IS-only by construction: `C_CAGR`, `C_SHARPE`,
`C_CALMAR`, `C_DDMIN`, `C_ISLEGS` (most 4b legs passed in sample), `C_MEDIAN` (the family-median
IS CAGR phase). TUNED 2 **book set**, 5 levels: TOP05 / TOP10 / TOP20 / EWELIG / BAND03 (942's).
Reported axes, nothing fitted: panel U56/B136/SMALL, cadence M (21 phases) / Q (63), gross
CORE 0.75 / EXT 1.00, cost 0/5/10/25/50 bps, and both 4b conventions (REC = the record's,
OOSPURE = every leg inside the OOS window). Controls: CANONICAL (phase 0), FAMILY (all phases),
ORACLE (hindsight-best phase — not a strategy, it only says whether ANY phase could have passed).
Rule 8 throughout: the phase is chosen on **2009–2016 alone** and 2017–2026 is read **once**.

## The answer, at 10 bps / CORE (180 chooser cells = 6 × 5 books × 3 panels × 2 cadences)
| source | OOS 4b PASS (REC) | OOS 4b PASS (OOSPURE) | OOS 4a PASS |
|---|---|---|---|
| CANONICAL (phase 0) | **2 of 30 = 0.067** | 2 of 30 | 0 of 30 |
| all six IS choosers | **6 of 180 = 0.033** | 6 of 180 | **0 of 180** |
| ORACLE (hindsight) | 12 of 30 = 0.400 | 11 of 30 | 0 of 30 |

Per chooser: C_MEDIAN 2, C_CAGR 1, C_SHARPE 1, C_DDMIN 1, C_ISLEGS 1, **C_CALMAR 0** — flat
across choosers, which is what luck looks like. Same ordering at every cost rung (chooser 0.033
vs canonical 0.067 at 0/5/10 bps, 0.033/0.067 at 25 and 50) and at EXT gross (0.017 vs 0.033).
Over all rungs and both gross: chooser **43 of 1,800 (0.024)**, canonical **15 of 300 (0.050)**.

**The blind-random-phase null settles it.** Scoring each family by its own fraction of passing
phases and convolving exactly (Poisson-binomial), a coin picking phases at random on those same
180 cells passes **14.10 times (sd 2.81)**. The six choosers passed **6**: `P(X ≤ 6 | blind) =
0.0017`. Inside the 12 families where some phase does pass, the choosers hit **6 of 72 (0.083)**
against a blind rate of **0.196**. The canonical phase passed 2 against a blind expectation of
**2.35** — indistinguishable from chance. **Choosing in sample is significantly worse than not
choosing; the canonical is exactly as good as a coin.**

Why: the in-sample phase ranking is **anti-predictive**. Median within-family Spearman
ρ(IS CAGR, OOS CAGR) = **−0.153** over 30 families (mean −0.186, positive in only 0.300 of them;
Sharpe −0.164), worst on BAND03/Q (−0.657) and EWELIG/M (−0.391). H_PRED (bar ≥ 0.30) fails in
the wrong direction, not merely at zero.

## What the dial is worth, and what choosing buys
OOS CAGR spread within a family: median **3.09 pp (M)** / **6.53 pp (Q)**, max **15.34 / 25.49 pp**
(IS spreads are similar: 2.73 / 4.72 median). Mean |OOS regret| of a chooser vs the canonical is
**2.175 pp** of CAGR — the dial is large, it is simply not steerable.
Against the canonical the choosers are a coin flip on levels: OOS CAGR higher in **95 of 180
(0.528)**, mean regret **+0.634 pp** (median +0.069, range −9.53 … +13.95), mean extra OOS
drawdown **−0.209 pp**. H_BEAT (bar 0.60) fails. Against the **family mean** — the phase-averaged
honest estimator — the choosers win in only **0.400** of cells, and five of the six lose on
average (C_MEDIAN +0.465 pp is the only positive). So the small positive CAGR regret vs the
canonical is a fact about the canonical sitting low in its own family (942's result), not about
the chooser finding anything.

## 942's `L4_DD` claim does NOT generalise
942 reported that every IS pick fails OOS on **`L4_DD` alone** on its 12-cell slice. Over the 174
failing chooser cells here the failing-leg string is exactly `L4_DD` in **0.379** (66 cells);
29 cells fail **all five legs**, 22 fail `L2_H2,L3_OOS,L4_DD,L5_CAGR`, 12 fail `L5_CAGR` alone.
H_DD (bar 0.90) fails. Under OOSPURE the same picture (47 exactly `L4_DD`, 43 failing all five).
**The `L4_DD`-alone characterisation is a 12-cell artefact; the drawdown leg is the most common
single killer but it is the sole killer in barely a third of failures.**

## Could any phase have passed? (H_ORACLE also fails — in the informative direction)
The hindsight-best phase fails 4b in **0.600** of the 30 verdict-rung families, i.e. **12 of 30
families contain at least one 4b-passing phase** (U56 carries 9 of the 12; B136 3; SMALL none).
So the 4b failure is NOT purely a phase fact — a passing phase usually exists on U56 — but no
IS rule finds it. Meanwhile **4a is dead everywhere**: 22 of 12,600 grid rows and **0 of 210**
picked cells beat the live RULES v2 book out of sample on the 4a path.

## Capital verdict
**KILL.** No configuration here is capital-worthy: 4a 0 of 180, 4b 6 of 180 at less than half
the blind rate, and the two canonical passes (U56/TOP20/M 16.7% / 1.28 / −19.5%; U56/EWELIG/M
13.0% / 1.22 / −17.0%) are the record's already-known U56 monthly cells, not a new book.
The operational consequence is a convention, not a dial: **trade the canonical period-end phase
and publish the family spread beside every phase-sensitive claim** — choosing the phase in sample
is measurably worse than not choosing it, and the phase-averaged estimator beats the chooser in
60% of cells.

SURVIVORSHIP (rule 9): U56 / B136 / SMALL are current-constituent lists; every level above is
optimistic. The chooser-vs-canonical contrast is same-tape, same-universe, same-weights and
differs only in which day the identical book trades, so the pass-rate comparison is unaffected;
the 4b levels are read against SPY, so a survivor panel makes 4b failures RARER — every failure
reported here is, if anything, understated.

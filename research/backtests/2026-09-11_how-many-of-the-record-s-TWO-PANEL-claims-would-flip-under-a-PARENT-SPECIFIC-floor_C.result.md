# Idea 774 (lane C, 2026-09-11) — how-many-of-the-record-s-TWO-PANEL-claims-would-flip-under-a-PARENT-SPECIFIC-floor

**ANSWERED / KILL for capital, and the queue's premise is refuted twice over: a parent-specific
floor moves FEW verdicts (0–41 of 607, dial-dependent), moves them in the OPPOSITE direction to the
one the queue assumed (toward MORE claims inside, not fewer), and moves TWO-panel claims LESS than
three-panel ones.** No RULES change, no book promoted, no NEW KEEP claimed, no memo, no PROTOCOL
edit applied; RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched (rule 6).

SELECTION: taken as the SECOND open idea per this lane's rule; 774 mentions no EDGAR / Form 4 / 8-K
/ options / live data.

Script `2026-09-11_how-many-of-the-record-s-TWO-PANEL-claims-would-flip-under-a-PARENT-SPECIFIC-floor_C.py`
· 900-book price grid · 10 bps · next-day fills · IS ≤ 2016-12-31, OOS ≥ 2017-01-01 read once · 61s.

## Gates (pre-registered, printed before any new census number was read) — ALL PASS

| gate | object | result | bar |
|---|---|---|---|
| G1 harvest | idea 567's committed `.census.csv` re-harvested from the record's 776 committed markdown files | **607 of 607 rows reproduced exactly** (this run harvests 608; the surplus is one file committed after 567 ran); named-parent set recovered for **607 of 607** | 607 |
| G2 floors | the per-parent draw floors rebuilt from prices here vs idea 567's committed `.floors.csv`, all 60 (statistic, D, period) rows | **9.714e-17** — an independent same-day cross-lane reproduction | 1e-12 |
| G3 identity | `fast_backtest` vs `engine.backtest` | **0.000e+00** | 1e-12 |
| G4 headlines | idea 567's five published census numbers re-derived from its OWN committed census | max \|d\| **4.416e-04** (42.67% vs 42.7%, 465 nonzero exact, 25.16% vs 25.2%, 3-panel 52.67%, 2-panel nonzero 16.42%, 3-panel PREM_SHARPE 35/55 exact) | 1e-3 |

## The dial the queue did not specify, and it decides the answer

"Its own named-parent floor" is not one object once a claim names two parents — which **345 of the
607** claims do. A claim "U56 0.31 > B136 0.17" is about a **difference** between two parents' draws,
so the bar is the dispersion of that difference, not of either level. Five assignments priced side
by side (dial 1) × bar ∈ {1.0, 2.0} sd (dial 2) — **all 10 points reported**, at every statistic
family and every draw count D ∈ {3,6,12,24} (reported axes, never selected):

**Share of the 607 inside its own floor (D=6, FULL):**

| assign | mean bar | inside @1.0 sd | inside @2.0 sd | 2-panel nonzero @1.0 | 3-panel nonzero @1.0 |
|---|---|---|---|---|---|
| POOLED (567's incumbent) | 0.0691 | **42.67%** | 50.74% | 16.42% | 37.06% |
| MIN of named parents | 0.0600 | 41.35% | 49.59% | 14.55% | 35.53% |
| MEAN of named parents | 0.0686 | **42.67%** | 50.74% | 16.42% | 37.06% |
| MAX of named parents | 0.0769 | 43.99% | 53.38% | 16.79% | 40.61% |
| **RSS (sd of the difference — the correct bar)** | **0.1083** | **49.42%** | 59.47% | 20.52% | 52.28% |

## How many verdicts move, and in which direction (the queue's actual question)

| assign (D=6, bar 1.0) | OUT→IN | IN→OUT | net | moved | of which 2-panel | of which 3-panel |
|---|---|---|---|---|---|---|
| MEAN | 0 | 0 | **+0** | **0.0%** | 0 of 345 | 0 of 262 |
| MIN | 0 | 8 | −8 | 1.3% | 5 of 345 (1.4%) | 3 of 262 (1.1%) |
| MAX | 8 | 0 | +8 | 1.3% | 1 of 345 (0.3%) | 7 of 262 (2.7%) |
| **RSS** | **41** | **0** | **+41** | **6.8%** | **11 of 345 (3.2%)** | **30 of 262 (11.5%)** |

At bar 2.0: MEAN +0 (1 each way), MIN −7, MAX +16, RSS +53 (8.7% moved). **Not one claim moves
IN→OUT under MAX or RSS at either bar.** By named-parent set (D=6, bar 1.0): `B136+SMALL` (n=47) is
**25.53% inside under all five assignments — literally immovable**, because B136's and SMALL439's
floors are within 6% of each other at D=6; `B136+SMALL+U56` (n=262) moves 52.67% → 64.12%;
`B136+U56` (n=228) 37.28% → 41.23%; `SMALL+U56` (n=70) 34.29% → 37.14%.

**H_DIR FALSIFIED.** The queue reasoned that because 558 of the census's claims name U56 and U56's
floor is the narrowest (0.0502 vs 0.0995/0.0941), a parent-specific bar would exonerate them. It does
the opposite: a claim that *compares* U56 to another parent must clear the dispersion of the gap,
which is **larger than either parent's own floor** (RSS 0.1083 vs the pooled 0.0691). The
parent-specific floor **convicts 41 more claims and acquits none**.

**H_TWO FALSIFIED.** The 2-panel/3-panel asymmetry is not a pooled-bar artefact: the nonzero
inside-share gap **grows** from 20.64 pp (POOLED) to 31.76 pp (RSS), **1.54x**, and two-panel claims
are the ones that move *least* (3.2% vs 11.5%).

**H_SPREAD FALSIFIED, narrowly.** MIN 41.35% vs RSS 49.42% is **8.1 pp**, inside the 10 pp bar
pre-registered as "under-specified" (bar 2.0: 9.9 pp). The assignment dial is real but modest,
because POOLED ≡ MEAN to **0 of 607 verdicts** at bar 1.0 — 43% of the census names all three
parents, and the rest average close to the pool.

## Rule 8 walk-forward

**WF-A (the answer OOS).** Floors rebuilt on IS only and OOS only, census re-scored at all 10 points.
Net movement vs POOLED, D=6 bar 1.0: RSS **+37 IS / +34 OOS**, MAX +13/+22, MIN −4/−26, MEAN +1/−6.
**The direction of movement agrees IS vs OOS for 4 of 5 assignments** (MEAN flips from ≈0, i.e.
noise) — so the conviction is out-of-sample stable. The **levels** are not: pooled inside-share runs
49.09% IS vs 42.50% OOS, so "inside its floor" remains a resolution statement, not a fact.

**WF-B (the re-score priced as a decision rule).** In each (gross, cadence) cell, rank the three
parents by IS MA-gate premium and ACT (trade MA-RS on the IS-best parent) only if the IS span clears
bar × the assignment's floor, else STAND DOWN to the live book; equal-weight the six cells; OOS read
ONCE. The gate does change what you trade — at MAX/RSS bar 2.0 it stands down in **6 of 6** cells —
but it never earns anything:

| rule | acted | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|
| RSS / MAX bar 2.0 (full stand-down) | 0/6 | 9.45% | **1.2747** | −12.05% |
| POOLED / MEAN / MAX / RSS bar 1.0, MIN bar 2.0 | 3/6 | 10.94% | 1.1966 | −15.06% |
| MIN bar 1.0 ( = ALWAYS-ACT, idea 567's rule) | 6/6 | 13.00% | 1.1567 | −18.40% |
| **RULES v2 U56 (live book)** | — | 9.45% | **1.2747** | −12.05% |
| SPY | — | 15.24% | 0.8721 | −33.72% |

**Decision books beating RULES v2 OOS Sharpe: 0/10. Beating SPY: 10/10.** Every gated rule that acts
at all loses OOS Sharpe to the live book for more drawdown; the only ones that match it are the two
that stand down completely, i.e. that trade nothing.

## KEEP paths

**Full 900-book grid: 4a 2/900, 4b 52/900, BOTH 0/900** — an exact third reproduction of idea 567's
counts, with the same three REAL 4b passers (U56 MA-RS g0.75 W and M, B136 MA-RS g0.75 W), i.e. the
record's existing MA-RS gate re-found. 4b by parent U56 39 / B136 13 / SMALL439 0; binding failure
legs DD 313, CAGR 191.

**Decision books: 4a 0/10, 4b 1/10, BOTH 0/10.** The single 4b pass (MIN bar 1.0: 12.09% / 1.1332 /
−18.40% full-sample) **is idea 567's ALWAYS-ACT rule under a different wrapper** — the rule 567
already priced and killed for losing to the live book — and it is an equal-weight blend of MA-RS
books the record already holds. **It is NOT claimed as a new KEEP and gets no memo:** it fails 4a,
its OOS Sharpe (1.1567) loses to RULES v2 (1.2747) by 0.118 for 6.4 pp more drawdown, and its panel
choice is fixed on in-sample data forever.

## Reading

The queue asked which two-panel claims a parent-specific floor would rescue. The answer is **none**:
under every assignment that is defensible for a between-parent gap, a parent-specific floor is
**wider** than the pooled one, so it can only convict. The record's habit of scoring a cross-panel
margin against a within-panel floor has been **flattering** its claims, not penalising them — idea
567's 42.7% is a floor on the problem, and the honest number is **49.4%**.

SURVIVORSHIP: `universe_broad.json` and the small panel are current constituents; the LEVEL floors
(SHARPE, CAGR, MAXDD) are lower bounds on true dispersion, the arm-minus-arm premium largely cancels it.

PROTOCOL proposal (Sunday, **not** adopted): when a margin is a gap BETWEEN named panels, quote it
against the root-sum-square of those panels' own draw floors, not against a pooled within-panel sd.

Artefacts: `.grid.csv` (900) `.floors.csv` (60) `.census.csv` (607 + parent set) `.rescore.csv` (120)
`.moves.csv` (360) `.walkforward.csv` `.keeppaths.csv` (900) `.console.txt`.

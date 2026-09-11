# Idea 788 (cloud lane, 2026-09-11) — publish-a-PERIOD-STABILITY-column-beside-every-FLOOR-COMPARISON-verdict-in-the-record

**ANSWERED — THE COLUMN IS WARRANTED AND IT FAILS ITS OWN BAR: 11.7% of the record's 607
committed floor-comparison verdicts flip when the floor is re-estimated on half the sample.
The instability is almost entirely the SHARPE family, and it is almost entirely
one-directional. / KILL for capital (no book, no rule change).**

## Question

Idea 779 closed with a proposal it did not execute: *"If a future run wants to retire
anything on a floor comparison, the floor's own period stability has to be published beside
it."* Its evidence was one number — the mover set's Jaccard of 0.0222 between IS-only and
OOS-only floors — measured on one bar form at one dial. This run builds the column: every
committed `inside/outside its floor` verdict is re-scored on FULL, IS-only and OOS-only
floors, and the per-claim agreement is published as a required field.

The object is **different from 779's**. 779 measured the stability of a *restatement* (which
claims move when the bar *form* changes). This run measures the stability of the *verdict*
(does a claim read INSIDE or OUTSIDE when the floor is estimated on a different *period*) —
which is the thing every published floor comparison actually quotes.

## Gates — ALL PASS

| gate | what | result |
|---|---|---|
| G1 harvest | fresh harvest of 783 committed md files reproduces 778's census | **607 of 607** (this run harvests 614; surplus = files committed after 778 ran) |
| G2 floors | per-parent floors rebuilt from prices vs 774/778's committed `.floors.csv`, 60 rows × 6 cols | max \|d\| **9.714e-17** (bar 1e-12) |
| G3 identity | `fast_backtest` vs `engine.backtest`, one book per parent | **0.000e+00** |
| G4 779 repro | 779's WF-A mover counts rebuilt **from prices** | FULL **18**, IS **35**, OOS **11**, IS∩OOS **1**, Jaccard **0.0222** — exact |
| G5 degeneracy | INSIDE share must sit strictly inside 2–98% in every period | FULL 45.6%, IS 54.9%, OOS 44.0% |

## Two dials (PROTOCOL rule 4), all 20 points reported

VERDICT SET in {ALL, 2PANEL, 3PANEL, NESTED_PAIR, NZ} × SPLIT in {FULL_vs_IS, FULL_vs_OOS,
IS_vs_OOS, ALL3}. Reported, never selected: bar form (POOLED / RSS_INDEP / PAIR_INDEP),
D ∈ {3,6,12,24}, bar multiple ∈ {1.0, 2.0}, statistic family (5), period (3), venue.
Headline point declared before the run: **PAIR_INDEP, D=6, bar=1.0** (778's restatement, the
record's current bar).

### Agreement rate — the 20 tuned points

| verdict set | n | FULL_vs_IS | FULL_vs_OOS | IS_vs_OOS | **ALL3** |
|---|---|---|---|---|---|
| ALL | 607 | 0.9077 | 0.9671 | 0.8913 | **0.8830** |
| 2PANEL | 345 | 0.9507 | 0.9652 | 0.9275 | **0.9217** |
| 3PANEL | 262 | 0.8511 | 0.9695 | 0.8435 | **0.8321** |
| NESTED_PAIR | 366 | 0.9126 | 0.9590 | 0.8716 | **0.8716** |
| NZ | 465 | 0.8796 | 0.9570 | 0.8581 | **0.8473** |

**B1 FAILS.** ALL3 agreement over ALL claims is **88.30%** against a pre-registered bar of
90%: **71 of 607 committed verdicts (11.7%) are period-dependent.** Over the full reported
grid (20 tuned points × 24 dial settings) agreement runs **0.7786 to 1.0000**; on ALL claims
alone it runs **0.8468 (PAIR_INDEP, D=3, bar 1.0) to 0.9572 (PAIR_INDEP, D=24, bar 2.0)**.

## Where the instability lives

**It is one family.** At the headline point:

| family | n | stable | rate |
|---|---|---|---|
| MAXDD | 118 | 117 | 0.9915 |
| CAGR | 86 | 85 | 0.9884 |
| PREM_CAGR | 42 | 41 | 0.9762 |
| PREM_SHARPE | 101 | 92 | 0.9109 |
| **SHARPE** | **260** | **201** | **0.7731** |

SHARPE carries **59 of the 71 unstable claims**. The level families the record leans on for
drawdown and return arithmetic are stable to better than 1%; the Sharpe comparisons are not.

**It is one-directional.** Of the 56 claims whose verdict changes between the FULL floor and
the IS floor, **56 of 56 go OUTSIDE→INSIDE** — zero acquittals, the same asymmetry 774/779
found under a different restatement. The mechanism is mechanical and worth stating plainly:
the IS window is shorter, so the across-draw s.d. is larger, so the IS floor is larger and
convicts more (INSIDE share IS 54.9% vs FULL 45.6% vs OOS 44.0%). FULL→OOS is much milder
(20 flips, 15 of them the other way).

**More correction has bought less stability.** Averaged over both bar multiples and all four
D, ALL3 agreement on ALL claims reads **POOLED 0.9331, RSS_INDEP 0.9343, PAIR_INDEP 0.9104**
— 778's restatement, the newest and most defensible bar form, is the **least** period-stable
of the three. At D=3, bar 1.0 the spread is 0.9259 (POOLED) vs 0.8468 (PAIR_INDEP). Narrower
bars sit closer to the margins, so more claims are within a period's worth of noise of their
own verdict. Raising D helps monotonically on every form (PAIR_INDEP 0.8468 → 0.9292 from
D=3 to D=24).

## …and the same negative result 779 got about *which* claims move

The unstable claims are **not** enriched in the record's control documents:
**66.2% of the 71 sit in a control document against a base rate of 70.7% — lift −4.5 pp.**
By venue: LEADERBOARD.md 28, CHANGELOG.md 16, QUEUE.md 3, individual result files 24. So the
column convicts headline claims at exactly the rate it convicts everything else. Named
examples, each of which reads differently on an IS-only floor:

- `CHANGELOG.md` — **"H_DOMINANT FAIL at 43% (bar 75%)"** (margin 0.1370): FULL INSIDE / IS INSIDE / **OOS OUTSIDE**.
- `CHANGELOG.md` — **"RULES v2 OOS Sharpe … U56 1.2788, B136 1.1185, SMALL439 0.5680"** (0.1603): FULL OUTSIDE / **IS INSIDE** / OOS OUTSIDE.
- `CHANGELOG.md` — **"Every unit's pick loses to the live RULES v2 book out of sample on all three panels"** (0.1568): FULL OUTSIDE / **IS INSIDE** / OOS OUTSIDE.
- `CHANGELOG.md` — **"COST IS NOT THE MECHANISM … 6-8% of the effect it would have to explain"** (0.2213): FULL OUTSIDE / **IS INSIDE** / OOS OUTSIDE.

## Rule 8

**WF-A is the column itself** — every verdict computed on IS-only and on OOS-only floors and
compared claim by claim (the table above). **WF-B prices the floor comparison as a decision
rule**, parameters from the first half only, OOS read once: for each (statistic, D) cell rank
the three parents by their **IS** value on the REAL MA-RS g=0.75 W book, and ACT (hold the
IS-best parent's book through 2017+) iff the IS min-gap ≥ bar × IS floor; else stand down to
the live book.

| book | acted | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|
| every IS-floor decision book, 24 cells × 2 bars | **0 of 48** | 9.45% | 1.2747 | −12.05% |
| same rule on FULL floors (look-ahead oracle) | 0 of 24 | 9.45% | 1.2747 | −12.05% |
| ALWAYS-ACT, SHARPE / PREM_SHARPE (picks U56) | 3/3 | 12.37% | 1.1078 | −18.62% |
| ALWAYS-ACT, CAGR (picks B136) | 1/1 | 11.97% | 1.0660 | −20.12% |
| **RULES v2 U56 (live book)** | — | **9.45%** | **1.2747** | **−12.05%** |
| **SPY** | — | **15.24%** | **0.8721** | **−33.72%** |

**Beating RULES v2 OOS Sharpe: 0 of 48. Beating SPY OOS Sharpe: 48 of 48.** The IS min-gaps
(SHARPE 0.0240, CAGR 0.0072, PREM_SHARPE 0.0578) are an order of magnitude below their own
floors (0.29–0.35, 0.045–0.053, 0.20–0.24), so **the rule never acts at any of the 48 cells**
— the fourth independent reproduction of idea 776's stand-down reading. **B3: the period
instability of the floor costs nothing in capital, because the floor never clears in the
first place — IS-floor and FULL-floor decisions agree 24 of 24.** The only books that act
are the ALWAYS-ACT controls that skip the floor test entirely, and they give up 0.17–0.21 of
OOS Sharpe and take 6–8 pp more drawdown to buy 2.5–2.9 pp of OOS CAGR.

## KEEP paths

Full price grid (3 REAL panels + 774's 24 independent draws each, 900 books):
**4a 2/900, 4b 52/900, BOTH 0/900**; REAL books 4a 0/36, 4b 3/36
(`U56/MA-RS/g0.75/W`, `U56/MA-RS/g0.75/M`, `B136/MA-RS/g0.75/W`) — an exact independent
reproduction of 779's committed counts. Decision books: **4a 0/52, 4b 3/52**, and all three
4b passes are the **ALWAYS-ACT controls** (the MA-RS gate the record already holds), not the
floor rule — the floor rule contributes **0 of 48**. Binding 4b failure legs across the grid:
DD 637, CAGR 425, H1 322, H2 315, OOS 306. **No candidate, no memo, no rule change.**

## PROTOCOL proposal (Sunday, not adopted — this run changed nothing)

Add to rule 4 or to the floor-comparison convention: *any published `inside/outside its
floor` verdict must carry the floor's period-stability flag (verdict recomputed on IS-only
and OOS-only floors, all three agreeing) beside it, and a verdict that is not ALL3-stable may
not be used to retire, promote or order anything.* On the current record that would flag
**71 of 607 claims (11.7%)**, of which **59 are Sharpe comparisons**. The cheap partial fix
is orthogonal and should be stated with it: **raise D**. At D=24 the headline form reads
92.9% (bar 1.0) and 95.7% (bar 2.0) against 84.7% / 87.8% at D=3, for nothing but compute.

## Survivorship

`universe_broad.json` and the small panel are **current constituents only**; every stock-side
level carries a survivorship premium and the LEVEL floors (SHARPE, CAGR, MAXDD) are lower
bounds on true dispersion, so the true agreement rate is an upper bound on what a
delisting-complete panel would give. Names with `max_1d_move >= 1.0` are dropped from the
small panel per PROTOCOL. The three parents start on different dates (U56/B136 2008, SMALL
2010), inherited from 567's floor construction.

## Artefacts

`.stability.csv` (the column: 14,568 rows = 607 claims × 3 bar forms × 4 D × 2 bar, each with
`verdict_FULL / verdict_IS / verdict_OOS / STABLE`) `.agreement.csv` `.floors.csv` `.grid.csv`
`.g4.csv` `.walkforward.csv` `.keeppaths.csv` `.console.txt`

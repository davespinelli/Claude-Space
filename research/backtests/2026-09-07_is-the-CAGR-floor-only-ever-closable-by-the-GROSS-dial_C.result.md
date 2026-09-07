# Idea 334 — is the CAGR floor only ever closable by the GROSS dial?

**Lane C, cloud, 2026-09-07.** Script `2026-09-07_is-the-CAGR-floor-only-ever-closable-by-the-GROSS-dial_C.py`.
Artefacts: `.console.txt`, `.census.csv`, `.siblings.csv`, `.margins.csv`, `.grid.csv`,
`.headline.csv`, `.walkforward.csv`.

## Verdict

**KILL of the premise as written, KEEP of its consequence.** The 4b CAGR floor is *not*
closable by the gross dial alone — **concentration closes it more often than gross does**
(5 of 8 CAGR-only parents vs 2 of 8 @10 bps). But both closers are **exposure dials**, and
every one of the record's six *construction* instruments closes it in **0 of 68 points at
0, 10 and 25 bps**. The queue's conclusion therefore survives in a stronger form: the CAGR
floor is a statement about **risk appetite (gross OR concentration)**, not about book
construction — and it is not specifically about leverage.

**No KEEP proposed. 4a 0/297 at 10 and 25 bps.** The 13 4b passes @10 bps are
re-measurements of the filed CAND-20 / U56-monthly family (best cell U56 MARS20 g=0.75
freq=M: 14.68% / 1.176 / −19.51% / H1 1.143 H2 1.211 / OOS 1.288, cf. idea 189's
14.8% / 1.2081 / −19.6% / OOS 1.2866). Nothing new.

## Method

Ideas 387/391 showed the record's **prose** mis-attributes ~7% of what it attributes, so
the census runs on **committed numbers**: 219 machine-written failing-bar columns
(`fail4b`, `first_fail4b`, `fail4b_10`, …) in 182 CSVs, 172,144 rows. A row is a CAGR-only
near-miss iff that column reads exactly `CAGR`.

Four legs: **L1** archive census · **L2/L2b** archive one-dial sibling test with value-gated
attribution · **L3** fresh causal measurement on a controlled corpus · **L4** rule-8
walk-forward. Tuned parameters (2): the instrument's dial value and the parent's gross
rung. Panel, book-form and instrument identity are census axes — every level reported.

Gates, all 0.000e+00 / exact: G1/G2 `fast_backtest` == `engine.backtest` on returns and
turnover at 0 and 25 bps; G3 `band_state(b=0)` == `px>ma200` (0 / 242,015); G4
`sel_band(m=0)` == `sel_hard(n)` on every rebalance day (0 disagreements); G5 breadth
overlay at depth=0 == parent (|dw| 0.000e+00); G6 the archive scan is byte-identical on a
re-read.

## L1 — the near-miss class is 1 row in 6

**26,951 of 172,144 rows (15.66%) are CAGR-only near-misses**, in 158 sources across 148
files — against 21,205 outright 4b passes (12.32%). The class the queue asked about is
larger than the class of passes.

## L2 — the archive, once attribution is gated on VALUES not names

A sibling is a row sharing **every** identity column (metrics and verdicts excluded) except
one; `bps` is a grouping key, never a dial. Genuine one-dial closures of a CAGR-only parent:

| family | files | closures | par_closed / par_with_sib | median dCAGR of the closure |
|---|---|---|---|---|
| CONC | 22 | 192 | 163/321 | +1.32 pp |
| MABAND | 10 | 23 | 25/40 | +1.40 pp |
| NTBAND | 13 | 4 | 4/4 | +2.16 pp |
| CADENCE | 11 | 2 | 2/4 | +1.61 pp |
| GROSS | 16 | 2 | 2/5 | +4.34 pp |
| VOLSCALE | 4 | 4 | 2/2 | +2.92 pp |
| BREADTH | 16 | 0 | 0/0 (never swept beside one) | — |

**A lexical-overload finding falls out of this leg.** Without a value gate the archive says
CADENCE closes the floor **540 times at a median +4.26 pp**. 535 of those closures come
from a column named **`f`** in 6 files whose values are `{0.5, 0.2, 0.1}` — a *fraction*,
not a rebalance frequency. Gating attribution on the value set (cadence must be a cadence
token; gross in [0.05,3]; n a positive integer; b in [0,0.5]) reclassifies them
`REJECTED:CADENCE` and leaves 2 genuine cadence closures. Same defect, same shape as ideas
359 (`band` lexicon) and 384 (`m` overloaded in 53 of 68 files) — now in a third column
name. `depth` (12 files, 88 closures) and `n` (7 files) are likewise rejected for
non-uniform value types. **Any census of this record that attributes dials by column name
alone is wrong by an order of magnitude on at least one family.**

## L3 — the causal test (the headline)

18 parents = 3 panels (U56, B136, SMALL439) × 2 book-forms (MARS20 = composite top-20
inside the 200d collar; EWALL = the RULES v2 all-names form) × gross {0.35, 0.50, 0.75}.
**8 are CAGR-only near-misses** (parent fail-bar distribution: CAGR 8, `H1,H2,OOS,CAGR` 4,
`H2,CAGR` 2, `H1,H2,OOS,DD,CAGR` 2, pass 1, `H2` 1). Gaps to the floor: **1.94 to 7.18
pp/yr, median 5.02**. Then one dial at a time, everything else frozen — 122 instrument
points per cost rung.

**Parents closed / parents converted to a full 4b pass (of 8):**

| family | @0 bps | @10 bps | @25 bps |
|---|---|---|---|
| CONC | 5 closed / **5 converted** | **5 closed** / 1 converted | 2 / 0 |
| GROSS | 5 closed / 3 converted | 2 closed / **0** converted | 2 / 0 |
| CADENCE | 0 / 0 | 0 / 0 | 0 / 0 |
| MABAND | 0 / 0 | 0 / 0 | 0 / 0 |
| NTBAND | 0 / 0 | 0 / 0 | 0 / 0 |
| VOLCAP | 0 / 0 | 0 / 0 | 0 / 0 |
| BREADTH | 0 / 0 | 0 / 0 | 0 / 0 |
| VOLSCALE | 0 / 0 | 0 / 0 | 0 / 0 |

**CAGR AUTHORITY** — the largest CAGR move each instrument can produce off these parents,
against a population whose *smallest* gap is 1.94 pp:

| @10 bps | GROSS | CONC | CADENCE | MABAND | VOLCAP | VOLSCALE | BREADTH | NTBAND |
|---|---|---|---|---|---|---|---|---|
| max dCAGR (pp/yr) | **+11.39** | **+9.47** | +0.99 | +0.73 | +0.66 | 0.00 | −0.03 | −0.39 |

The two exposure dials have **10–14x** the CAGR authority of every construction instrument,
and every construction instrument's *ceiling* (≤ +0.99 pp) sits **below the smallest gap in
the population** (1.94 pp). That is why they close 0 of 68 — not narrowly, but by an order
of magnitude. Idea 42's breadth-overlay result (0 of 486) reproduces exactly here: BREADTH
is the only family whose best point is *negative* at every cost rung.

**Three qualifications the queue's framing does not contain.**
1. **Gross capped at 1.00 (no leverage, PROTOCOL rule 2) closes only 2 of 8** @10 bps. Even
   the dial the queue credits fails on 6 of 8 near-misses without leverage.
2. **Closing the bar is not passing 4b.** @10 bps the 9 CONC closures and 4 GROSS closures
   yield **one** full pass between them; the rest break DD (GROSS: `fail4b` moves `CAGR` →
   `DD`) or H1/H2/OOS (CONC: median dSharpe −0.162). The floor and the DD cap are jointly
   binding, and both closers move both.
3. **Costs decide it.** Converts collapse 5+3 → 1+0 → 0+0 across 0 / 10 / 25 bps: CONC's
   authority falls +11.8 → +9.5 → +6.1 pp as its turnover is charged.

## L4 — rule 8 (dial chosen on ≤2016, 2017-2026 read once)

135 parent × family cells per chooser. IS-Sharpe chooser: beats own parent anchor 54/135,
SPY 81/135, RULES v2 3/135, mean regret +0.0216. IS-CAGR chooser: 60/135, 81/135, 3/135,
mean regret +0.0157.

Restricted to the 8 CAGR-only parents — **does the chosen dial close the floor OOS?**

| chooser | GROSS | CONC | CADENCE | others |
|---|---|---|---|---|
| IS Sharpe | 5/8 | 3/8 | 1/8 | 0/8 each |
| IS CAGR | 5/8 | 5/8 | 1/8 | 0/8 each |

The ordering survives out of sample. CADENCE's single OOS closure (U56 MARS20 g=0.50,
W→M, OOS CAGR 11.35% vs an OOS floor of 10.82%) clears by **0.53 pp** — consistent with its
≈1 pp authority, not a counterexample to it. Note the closers do *not* dominate: the arms
with the best OOS *Sharpe* are CADENCE (median 1.068) and VOLCAP (1.010), while CONC — the
best closer — has the worst median OOS Sharpe (0.80–0.84) and by far the largest regret
(+0.041 to +0.050).

## Proposal (for Sunday review, not a rules change)

The queue's `closable-by` column is supportable, with the value set **{GROSS, CONC, none}**
rather than {GROSS, none}. Suggested PROTOCOL note under rule 4b, as a reading aid only:

> A 4b failure whose sole failing bar is CAGR is a statement about the book's **exposure**,
> not its construction. In this record only two dials move CAGR by more than ~1 pp/yr —
> gross and name count — and both move MaxDD with it; six construction instruments
> (cadence, MA band, no-trade band, vol cap, vol scaler, breadth gate) closed such a miss
> in 0 of 68 measured points at 0, 10 and 25 bps.

**A second, cheaper amendment** falls out of L2: every census of this record that maps a
dial column to an instrument by NAME must gate on the column's VALUE SET. `f`, `depth`,
`m`, `n` and the `band` lexicon are all overloaded across files, and here that overload
inflated one family's closure count from 2 to 540.

## Caveats

Every panel is a current-constituent list (**survivorship**); SMALL439's CAGR is biased up,
i.e. its floor is tested in the book's favour. U56 ⊂ B136 and U56 is 36/56 ETFs, so three
panels are not three independent samples. The GROSS arms are absolute (g ∈ {0.85, 1.00}),
so they are the same two books for every parent — 16 GROSS points are 2 books × 8 parents.
L2 can only speak about dials the record actually swept beside a CAGR-only parent; L3
exists to close exactly that gap, and its own corpus is 18 parents, not the record.

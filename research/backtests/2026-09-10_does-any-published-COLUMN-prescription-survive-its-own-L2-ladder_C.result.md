# Idea 617 — does any published COLUMN prescription survive its own L2 ladder?  (lane C, 2026-09-10)

**VERDICT: SPLIT — the PREMISE is confirmed and larger than 613 claimed (93.1% of the record's
rung-carrying files publish a ladder containing 10 and 25 bps), the ASK answers **2 of 6** on the
primary target and **0 of 6** on the second, and 613's own L2 reversal **fails to replicate on a
new dial**, which weakens 613's KILL rather than extending it. No KEEP claimed, no book promoted.
RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py untouched.**

Script `2026-09-10_does-any-published-COLUMN-prescription-survive-its-own-L2-ladder_C.py`;
`.console.txt`, `.rungcensus.csv` (1 045 rung columns in 1 034 files), `.grid.csv` (2 592
arm-rows), `.columns.csv` (648 cell-rung rows), `.survive.csv` (144 grid points), `.width.csv`,
`.widthladder.csv`, `.wf.csv` (192 picks), `.wfpairs.csv` committed beside it.
Runs in 165 s, deterministic.

## Axes, and what is ever selected on (PROTOCOL 4)
The queue names the two tuned parameters and both are swept in full with every point reported:
**P1 column** (239 EWall control / 471 matched-gross twin / 583 gross-on-CAGR / 604 block placebo
/ 607 crossing cost, with **613 DRAG as the already-published control**) and **P2 rung ladder**
(L1 = [10], L2 = [10, 25], L4 = [0, 10, 25, 50], L6 = [0, 5, 10, 15, 25, 50] bps).
The fresh leg's dials are **band** (6 points, 0.00–0.08) and **gross** (3 points, 0.50/0.75/1.00),
fully enumerated and never chosen. Panels, books, forms and rungs are reported axes. The only
selection anywhere is PROTOCOL rule 8.

**Every column is computed IN SAMPLE (2009–2016); every target is OUT OF SAMPLE (2017–2026).**
No column is a function of the window it is scored on.

## Gates — all pass, before any new number was read
* **G1** vectorised runner vs `engine.backtest` on the evaluated slice: max|dr|
  **6.409e-16 / 6.297e-16 / 6.093e-16**, max|dturnover| **2.776e-16 / 3.331e-16 / 2.776e-16**
  (u56 / broad / small).
* **G2** rung identity `r(c) = r(0) − turnover·c/1e4` vs a live `engine.backtest(25)`:
  **6.409e-16 / 6.297e-16 / 6.093e-16**. This licenses reading six rungs off one simulation.
* **G3** the TWIN reproduces the ARM's realised mean gross: max|d| **1.221e-15**.
* **G4a** idea 616's committed `.grid.csv` reproduced on the **small** panel (ARM/CTRL/TWIN) at
  **1.110e-16**. **G4b** the u56/broad gap in G4a is the **universe convention and nothing else**:
  616 keeps SPY investable on u56/broad, this run drops the benchmark from every panel (613's,
  stricter, convention); rebuilding one u56 cell under 616's own convention reproduces 616 at
  **0.000e+00**. The PLACEBO form is excluded from the gate by construction (seed 617 vs 616).

## H0 — THE PREMISE. L2 is not just *a* published ladder, it is *the* published ladder
2 836 committed CSVs scanned; **1 034 carry a cost-rung column** (1 045 columns).

| distinct rungs published | files | share |
|---|---|---|
| 1 | 17 | 1.6 % |
| **2** | **597** | **57.7 %** |
| 3 | 230 | 22.2 % |
| 4–12 | 190 | 18.4 % |

| most-published ladder | files |
|---|---|
| **[10, 25] = L2** | **559** |
| [0, 10, 25] | 209 |
| [0, 5, 10, 15, 20, 25, 30] | 43 |
| [5, 10, 15, 20, 25] | 37 |
| [0, 10] | 31 |
| **[0, 10, 25, 50] = L4** | **16** |
| **[0, 5, 10, 15, 25, 50] = L6** | **14** |
| **[10] = L1** | **13** |

**963 of 1 034 rung-carrying files (93.1 %) publish a ladder containing both 10 and 25 bps.**
L4 and L6 — the ladders on which idea 613's drag column *won* — together account for **30 files,
2.9 %**. 613's framing ("the only rung pair the record routinely publishes") is right, and the
concentration is stronger than it stated.

## H1 — THE ASK. Two of six survive their own L2 ladder
Population, declared (idea 612): **TOP20 ARM rows only**, 324 pooled rows at L6 — 239's EWall
control is degenerate on an EWALL arm, so pooling the EWALL arms in would let one column be
scored on a population the others are not. The EWALL arms are reported separately below.
SURVIVES on ladder L ⇔ |rho(target, prescribed)| > |rho(target, incumbent)| on L's rows.

**Primary target: the arm's realised 2017–2026 Sharpe at the same rung.** POOLED reading:

| prescription | incumbent | L1 [10] | **L2 [10, 25]** | L4 | L6 |
|---|---|---|---|---|---|
| **239** un-ranked EWall control | dS vs CTRL | **+0.4175 S** | **+0.3216 SURVIVES** | +0.3574 S | +0.3650 S |
| **471** matched-gross twin | dS vs CTRL | +0.0000 fails | **−0.0002 FAILS** | −0.0025 | −0.0009 |
| **583** gross on a CAGR claim | dCAGR vs CTRL | −0.0475 fails | **−0.0742 FAILS** | −0.1098 | −0.0987 |
| **604** block placebo | dS vs CTRL | −0.2587 fails | **−0.2678 FAILS** | +0.0184 S | −0.0237 |
| **607** crossing cost | dS vs TWIN | **UNDEFINED** | **−0.2226 FAILS** | −0.2622 | −0.2449 |
| *613 drag (published control)* | turnover | *+0.0000 fails* | ***+0.0842 SURVIVES*** | *+0.2221 S* | *+0.1648 S* |

Survivor count by ladder: **L1 1 / L2 2 / L4 3 / L6 2** (CELL reading: 1 / 2 / 2 / 2).

Three things in that table are load-bearing:

* **613's H2 reproduces exactly.** At L1 the drag re-pricing gains **+0.0000** — a positive affine
  map of turnover at a fixed rung cannot move a rank, and the measurement says so to the digit.
  On the CELL reading (columns averaged over the ladder) the gain is **+0.0000 at every ladder**,
  because averaging is affine too. A prescription of this shape can only pay by *pooling rungs*.
* **607 fails for a reason 613 never had to face: it does not exist at L1.** A crossing cost is a
  slope, so it needs ≥ 2 distinct rungs; the 13 files that publish [10] alone cannot carry the
  column at all (n_undef = 54/54 cells). This is a second, structural way for a prescription to
  fail its own ladder, and the census says it bites 1.6 % of the record's rung-carrying files.
* **239 is the one prescription that is not about cost at all**, and it is the only one that wins
  by a wide margin at every ladder. It is also, per idea 616, the prescription with the *lowest*
  compliance in the record (0.4 % at proposal, 2.7 % now).

**Second target: OOS d-Sharpe against the arm's own full-gross control. 0 of 6 survive, at every
ladder.** At L2: 239 −0.0361, 471 −0.0000, 583 −0.0431, 604 −0.4636, 607 −0.4909, 613 −0.1461.
This is the honest limit on the whole exercise: the incumbent *is* the in-sample version of the
second target, so it wins that scoring by construction, and **which target a column prescription
is scored against moves the verdict at least as much as which ladder it is read on.** A
prescription that "survives" is therefore always a claim about a stated target, never about the
column in the abstract. On the **EWALL arm population** (324 rows; 239 degenerate at exactly
0.0000 gain by construction) only 613 survives L2, at **+0.0601**.

## H3 — 613's L2 REVERSAL DOES NOT REPLICATE ON A DIAL 613 NEVER RAN
613's own test form, re-run with the 200d **band** as the dial whose 4b window is measured
(108 (panel, book, gross, rung) width cells; mean w_pts 0.75, 18 non-empty):

| ladder | \|rho(w, turnover)\| | \|rho(w, drag)\| | better order |
|---|---|---|---|
| L1 [10] | 0.0986 | 0.0986 | **tie** (identical by construction — 613's H2 again) |
| **L2 [10, 25]** | 0.0945 | **0.1085** | **DRAG** |
| L4 | 0.0900 | **0.1673** | DRAG |
| L6 | 0.0930 | **0.1475** | DRAG |

On the **sleeve** dial 613 ran, drag lost at L2 (0.056 vs 0.088) and that loss is what 613
published as the prescription's KILL. On the **band** dial it wins at L2. So the L2 failure is a
property of 613's dial, not a law about ladders — and **617's job was to find that out, so the
result cuts against the run that filed it.** The stable part of 613 is the algebra (L1 tie,
exactly), not the L2 reversal.

## Rule 8 (PROTOCOL 8) — (band, gross) chosen on 2009–2016 alone, 2017–2026 read once at 10 bps
192 picks = 4 ladders x 6 cells (3 panels x 2 books) x 8 column selectors.

| selector | median OOS CAGR | median OOS Sharpe | median OOS MaxDD | > SPY | > RULES v2 | OOS 4b | OOS 4a |
|---|---|---|---|---|---|---|---|
| S_dS_ctrl (incumbent) | 7.84 % | **1.020** | −17.65 % | 4/6 | 2/6 | 0/6 | 0/6 |
| S_EWALL (239) | 8.28 % | 1.023 | −16.51 % | 4/6 | 2/6 | 0/6 | 0/6 |
| S_TWIN (471) | 7.84 % | 1.020 | −17.65 % | 4/6 | 2/6 | 0/6 | 0/6 |
| S_GROSSC (583) | 8.28 % | 1.023 | −11.84 % | 4/6 | 2/6 | 0/6 | 0/6 |
| S_PLAC (604) | 7.84 % | 1.020 | −14.69 % | 4/6 | 2/6 | 0/6 | 0/6 |
| S_CSTAR (607) | 7.82 % | 1.019 | −14.34 % | 4/6 | 1/6 | 0/6 | 0/6 |
| S_TO (613 incumbent) | 7.84 % | 1.020 | −11.84 % | 4/6 | 2/6 | 0/6 | 0/6 |
| S_DRAG (613) | 7.84 % | 1.020 | −11.84 % | 4/6 | 2/6 | 0/6 | 0/6 |

Every row is **identical at L1, L2, L4 and L6** — the picks are ladder-invariant, which is H2 in
decision form. Prescribed minus incumbent OOS Sharpe: 239 **+0.003** (2/6 cells won, picks differ
2/6), 583 +0.003 (3/6), 471 +0.000 (0/6, picks differ 0/6), 604 +0.000 (0/6, picks differ 2/6),
607 **−0.001** (0/6, picks differ 3/6), **613 +0.000 with picks differing 0/6 at every ladder** —
the drag selector and the turnover selector are the same selector.
**OOS 4b 0/192, OOS 4a 0/192.**

Comparands on the same OOS window: SPY **15.32 % / 0.876 / −33.72 %**; RULES v2 @10 bps
u56 **9.48 % / 1.279 / −12.05 %**, broad 7.98 % / 1.119 / −12.24 %, small 3.85 % / 0.568 / −14.68 %.
Headline L2 pick, u56/TOP20 under S_dS_ctrl and S_TWIN (band 0.08, gross 1.00): full sample
**19.65 % / 1.180 / −25.80 %**, halves **1.277 / 1.116**, OOS **1.184 / 21.30 % / −25.80 %** — it
beats SPY's Sharpe on every bar and **fails 4b on the drawdown cap** (25.80 % against the
20.23 % that is 60 % of SPY's), which is the record's usual binding leg on a concentrated book.

## KEEP paths (PROTOCOL 4, evaluated on every one of 648 ARM rows)
**4a** vs the live RULES v2, cost-matched: **6 / 648** — all SMALL/EWALL at 15–50 bps, where
RULES v2 is itself weak (Sharpe 0.572).
**4b** vs SPY on all five bars: **82 / 648** (21/17/16/14/12/2 at 0/5/10/15/25/50 bps).
**BOTH: 0 / 648, at every rung. No KEEP, nothing promoted, no memo filed.**
All 16 of the 10-bps 4b passers are the record's already-published families: u56/TOP20 g=0.75
(6 bands, best band 0.08 at **14.68 % / 1.180 / −19.83 %**, halves 1.276/1.116, OOS 1.183) and
u56 + broad EWALL g=1.00. Binding 4b bar over all 648: **CAGR 262**, DD 134, H2 132, H1 70, OOS 50.

## What the record should do with this
Not "publish column X". The two facts that generalise are:
1. **A column prescription must name its TARGET and its LADDER, or it is not falsifiable.** The
   same six columns give 2/6 survivors on one target and 0/6 on another, and 1/2/3/2 survivors
   across four ladders.
2. **A column that is a fixed monotone transform of the incumbent at a fixed rung (drag of
   turnover, and any per-rung rescaling) can never change a single-rung reading, and 57.7 % of
   the record's rung-carrying files publish two rungs or fewer.** Prescriptions of that shape
   should be published as *pooling* rules, not as column rules.
Neither is proposed as a PROTOCOL edit here; PROTOCOL.md is untouched.

## Predictions, scored
P1 **RIGHT** — the census would confirm L2 dominance (predicted "modal"; measured 54.1 % modal,
93.1 % containing).
P2 **RIGHT** — most prescriptions would fail L2 (predicted ≤ 2 survivors; measured 2).
P3 **WRONG** — I predicted 613's L2 reversal would replicate on a second dial. It does not:
drag WINS at L2 on the band dial.
P4 **RIGHT** — 607 would be undefined at L1 (n_undef 54/54).
P5 **WRONG** — I predicted the surviving columns would show up in the rule-8 decision. They do
not: every selector lands within 0.004 OOS Sharpe and the drag selector is byte-identical to the
turnover selector in 6/6 cells.

## Caveats carried
* **SURVIVORSHIP (idea 54):** all three panels are current constituents; SMALL439 additionally
  drops the 44 `max_1d_move >= 1.0` tickers from `data/small_meta.csv` before anything runs.
* **UNIVERSE CONVENTION:** SPY is dropped from the investable set on every panel here. Idea 616
  kept it investable on u56/broad, which is the whole G4a gap (G4b re-derives it at 0.000e+00).
* The census reads **committed CSVs only**; a rung ladder quoted in prose is invisible to it, and
  a numeric column named like a rung but meaning something else is excluded by a name-and-range
  filter (idea 286/523's over-counting problem).
* **c\*(L) is constant within a cell**, so on the POOLED reading its x-column repeats inside a
  ladder; the CELL reading, reported beside it, does not have that property and agrees.
* The block placebo is **one seed (617)** — a comparand, not a distribution.
* MaxDD is one number off one path (idea 321) and the 4b DD cap turns on exactly that number.
* Idea 126: t+1 execution, no lag band. Idea 38: u56/broad carry the calendar-day index.
* 6 cells is a thin rule-8 population; the ladder-invariance of the picks is a strong result but
  the +0.003 selector differences are inside any reasonable noise band and are not claimed.

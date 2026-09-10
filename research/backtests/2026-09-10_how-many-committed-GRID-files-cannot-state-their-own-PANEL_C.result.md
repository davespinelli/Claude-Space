# Idea 653 — how many committed GRID files cannot state their own PANEL? (lane C, 2026-09-10)

**SPLIT. The queue's premise is REFUTED on recoverability, CONFIRMED on exposure, and the panel
stamp is KILLED as a rule-8 selector input. No RULES change, no book promoted, no KEEP claimed,
no memo; RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.**

Two tuned parameters and no more: **P1 RECOVERY SOURCE** (L0 DECLARED / L1 ALIAS / L2 LABEL /
L3 SIBLING / L4 SCRIPT / L5 TRANSITIVE — all six reported) and **P2 CLAIM READING** (LOOSE /
STRICT — both reported). Panels, books, bands, grosses, rungs and the null's draw count are
reported axes, never chosen.

## Gates (all PASS, run before any new number)

| gate | result |
|---|---|
| G1 `fast_bt` vs `engine.backtest`, 4 panels, returns / turnover | **6.409e-16 / 4.996e-16** |
| G2 cost-rung identity vs a live `cost_bps=25` run | **6.409e-16** |
| G3 idea 480's A3 census reproduced, **VINTAGE-PINNED** to its own 96 files | **96 / 370,102 / 7 / 107,816**, per-file row drift **0/96**, unstated drift **0/96** |
| G4 ladder monotone; no level contradicts an L0 label | **PASS**; **0 of 262,574** L0-labelled rows |
| G5 degenerate (whole-panel) draw has zero null dispersion | **0.000e+00** |

G3 had to be pinned: today's tree carries **1 more** five-margin block (288 rows, panel stated)
added after idea 480 ran. On the shared 96 the reproduction is exact, digit for digit. The
census also excludes this run's own artefacts — a census must not read its own output.

## A — the recovery ladder (P1). The queue's 7 files are 6 recoverable and 1 not.

Pinned population, 96 blocks, 370,102 rows:

| level | files with any unstated row | unstated rows | share |
|---|---|---|---|
| L0 DECLARED (idea 480's 3-key mapper) | 7 | 107,816 | 0.2913 |
| L1 +ALIAS | 5 | 107,177 | 0.2896 |
| L2 +LABEL column | 4 | 105,376 | 0.2847 |
| L3 +SIBLING CSV | 4 | 105,376 | 0.2847 |
| L4 +PARENT SCRIPT | **1** | 105,303 | 0.2845 |
| L5 +TRANSITIVE | **1** | **105,303** | **0.2845** |

* **2 of the 7 were never unstated at all.** `pre-register-K_CAGR…grid.csv` (510 rows) and
  `the-DD-cap-is-what-cuts…grid.csv` (129 rows) print `bstk100` in their own `panel` column —
  idea 542's documented **fourth panel** (the broad panel minus every ETF, SPY held out). Idea
  480's alias map knew three keys; the files stated their panel and the reader could not map it.
  The full panel-column vocabulary the record writes is 14 tokens, all of which map cleanly.
* **4 more are recovered from artefacts the record already commits**: `keep-candidate-universe-
  robustness_cloud.draws.csv` (1,600 rows) carries the panel in its `arm` column
  (`U56-drop` / `B136-size-control`); the two `v1u-small-negative-price_B` files (43 rows) and
  `is-the-DD-cap-unreachable-on-SMALL439…grid.csv` (30 rows) are single-panel runs whose parent
  `.py` names exactly one `load_universe` flavour or whose filename names the panel.
* **1 file is genuinely unrecoverable, and it is 97.7% of the problem.**
  `re-cut-every-published-BINDING-BAR-claim-as-a-STEP-NORMALISED-argmin_cloud.cells.csv` holds
  105,303 of the 107,816 unstated rows. Its residual diagnosis is decisive: **99.7%** of those
  rows point at a **MULTI-panel source file** through a `file` column that carries **no row id**,
  across 75 distinct sources. 0.3% point at a file with no five-margin block. **0** point at a
  single-panel source that merely forgot to say so.

So the defect the queue named — "no mappable panel column" — is the wrong diagnosis for the rows
that actually matter. The missing field is a **ROW ID on a file that re-reads another file's
rows**, not a panel stamp.

## B — do the published claims depend on a panel-relative quantity? (P2)

48 published sentences name one of the six stems across CHANGELOG / LEADERBOARD / QUEUE and each
stem's own `.result.md`. **LOOSE 20/48 = 0.417; STRICT 4/48 = 0.083**, and **4 of 6 files carry
at least one strict panel-relative published claim** (a number quoted in noise units, a per-panel
scale, or a named-panel contrast). Per-file STRICT share runs 0.000 (v1u-small, whose whole run
is one panel) to 0.143. The exposure is real but thin: most of what these files published is a
within-file absolute statement that never needed the stamp.

## C — payoff: recovering the panel moves the binding bar

The panel-noise null is rebuilt fresh for all four panels (120 equal-weight half-panel draws
inside the live 200d band, seed 653). Idea 480's own committed `.scales.csv` recovers a scale for
**B136 and U56 only** — its noise-unit reading never reached SMALL439 at all; that limit is lifted
here and reported.

| level | convertible files | convertible rows | modal bar flips RAW→NOISE | cell-level median flip |
|---|---|---|---|---|
| L0 DECLARED | 92/97 | 262,574 / 370,390 | **33/92 (0.359)** | 0.386 |
| L5 TRANSITIVE | **97/97** | 265,087 / 370,390 | **37/97 (0.381)** | 0.386 |

The modal binding bar of the record's blocks is `CAGR 47 / H2 27 / DD 21 / H1 2` read RAW and
`CAGR 66 / DD 29 / H1 2` read in panel-noise units: **H2 disappears entirely as a modal binding
bar** once the margins are scaled. Recovery is not bookkeeping — it buys a different answer on
38% of blocks.

## D — the live cost: the stamp is KILLED as a rule-8 selector input

Fresh grid: 4 panels × 3 books (EWALL / TOP20 / LOWVOL20) × 3 grosses × 4 bands, 144 simulations
read at 5 rungs = **720 arm-rows**, weekly, t+1.

**KEEP paths (PROTOCOL 4), every arm-row:** 4a **22/720**, 4b **62/720**, **BOTH 0/720**.
At PROTOCOL's own 10 bps rung: 4a 4, 4b 13, BOTH 0.

**GROSS-LADDER CONTROL (idea 311).** Of the 48 (panel, book, band) cells at 10 bps, **13 carry at
least one 4b pass and 0 pass at all three grosses — all 13 pass at exactly one.** Max
|Sharpe(g=1.00) − Sharpe(g=0.50)| over the same cells is **0.0052**: the ladder moves the 4b CAGR
floor and DD cap, not the risk-adjusted number. Every 4b pass in this grid is gross-decided, so
**nothing here is promoted** and no memo is filed.

**RULE 8 (PROTOCOL 8)** — (book, gross, band) chosen on 2009–2016 only, 2017–2026 read once. Four
pre-registered selectors; S1 needs no panel stamp, S2 divides each IS margin by the arm's **own**
panel-noise scale, S3 by **another panel's** (the mis-stamped read).

| selector | OOS CAGR | OOS Sharpe | OOS MaxDD | beats SPY | beats RULES v2 | OOS 4b | OOS 4a |
|---|---|---|---|---|---|---|---|
| S0 IS Sharpe | 14.55% | 0.8895 | −30.29% | 12/20 | 6/20 | 0/20 | 0/20 |
| **S1 RAW bind (no stamp)** | 9.61% | **0.8774** | −20.44% | 15/20 | 4/20 | **10/20** | 0/20 |
| **S2 OWN panel (stamped)** | 9.61% | 0.8735 | −20.41% | 15/20 | 6/20 | 8/20 | 0/20 |
| S3 MIS-stamped | 9.58% | 0.8754 | −20.44% | 15/20 | 4/20 | 7/20 | 0/20 |

Per-panel at 10 bps, OOS: **U56** SPY 15.32% / 0.876 / −33.7%, RULES v2 9.48% / 1.279 / −12.1%,
every selector picks TOP20 g0.75 b0.00 (16.61% / 1.166 / −22.2%). **B136** SPY 15.45% / 0.882 /
−33.7%, v2 7.98% / 1.119 / −12.2%, S1=S2=S3 pick EWALL g1.00 b0.06 (10.84% / 1.101 / −18.0%).
**SMALL439** v2 3.84% / 0.566 / −14.7%; S1/S3 pick LOWVOL20 g0.75 b0.00 (2.18% / 0.263 / −22.5%),
S2 picks g1.00 b0.06 and does **worse** (0.87% / 0.145 / −21.6%). **BSTK100** v2 8.89% / 1.140 /
−12.9%; S1/S2 pick EWALL g1.00 b0.02 (12.10% / 1.164 / −17.2%), S3 g1.00 b0.04 (12.04% / 1.141).

S1 vs S2 agree on **13/20 (65.0%)** picks; S2 vs S3 on **15/20 (75.0%)**. So the stamp changes the
chosen book in 35% of cells — **and the change is negative**: the stamped selector is 0.0039 Sharpe
*behind* the selector that needs no stamp, and clears OOS 4b on 8 cells against S1's 10. Being
**mis**-stamped costs 0.0019 Sharpe against being correctly stamped, an order of magnitude less
than the record's own headline gaps. **0/20 rule-8 picks clear 4a on any selector.**

## Verdict

The queue's "7 files cannot state their own panel" survives only as "1 file cannot, and 2 of the
7 always could". The record's real infrastructure gap is narrower and sharper than the queue
feared: a **row-id column on any artefact that re-reads another artefact's rows**. Reading a
published binding-bar claim in panel-noise units genuinely needs the stamp (38% of blocks change
their modal bar). *Choosing a book* does not: the un-stamped selector is the better one out of
sample, and no arm on the fresh grid clears both KEEP paths at any rung.

## Caveats carried
Committed CSVs only; a prose-only claim is invisible to the block census (LOOSE is the upper
bound). SURVIVORSHIP (PROTOCOL 9, idea 54): u56/broad/bstk100 are today's constituents,
SMALL439 the sub-$2B screen's survivors — every CAGR is inflated and every 4b CAGR floor is
generous; only within-panel contrasts are read as edges. MaxDD is one number off one path
(idea 321) and the 4b DD cap turns on exactly it. t+1 execution, no lag band (idea 126). The
L4/L5 rules assign a panel only on unanimous evidence, so the ladder is a **lower** bound on
recoverability. The fresh grid's three dials exceed PROTOCOL's two-parameter cap and are a
control apparatus for the stamp question, never a proposal — which is the second reason nothing
is promoted.

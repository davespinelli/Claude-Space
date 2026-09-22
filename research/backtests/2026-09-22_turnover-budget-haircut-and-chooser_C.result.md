# Idea 2087 — does the 1795 TURNOVER-BUDGET KEEP-CANDIDATE survive a POINT-IN-TIME-SHAPED ADMISSION HAIRCUT and a SECOND CHOOSER?

**Lane C, 2026-09-22.**  **ANSWERED, AND THE TWO HALVES SPLIT.  The CELL is the most
admission-robust object the record has priced — it clears 4b FULL+OOS on `400 of 400` U56
haircut draws and `120 of 120` B136 draws, at every depth to 30% of names dropped, at every
cost rung 0–50 bps and at t+2.  The CHOOSER is not: the pre-stated pooled bar FAILS at
`0.4671 < 0.50`, and the chooser ranking INVERTS across panels (IS_LEGS, the rule that reached
the candidate, is best on U56 at 0.785 and third-worst-but-two on B136 at 0.300, while
IS_SHARPE runs 0.680 / 0.983 the other way).  By the run's own pre-stated CAPITAL rule
(V1∧V2∧V3∧V4) the candidate is therefore DOWNGRADED to PARK — on the CHOOSER leg alone.**
Script: `2026-09-22_turnover-budget-haircut-and-chooser_C.py`.  Grid `.grid.csv.gz`
(**78,240 rows, all published**), cell survival `.cellsurvival.csv` (652 rows), rule-8 picks
`.choosers.csv` (4,564 rows), gates `.gates.csv`, console `.log.txt`.

## What was priced

Idea 1795's KEEP-4b candidate verbatim: **U56, equal-weight, `g = clip(t/σ20, 0, 1)` capped at
gross 1.00, MONTHLY trade, TURNOVER BUDGET `B` turns/yr** (refresh trigger `R = D`, executed
only while trailing-252-day realised turnover plus the refresh's own cost stays inside `B`);
fills t+1, 10 bps headline.  The published cell is `t = 0.12, B = 5.0`.
622 panels were priced (501 U56 + 151 B136) × 30 cells (`t` × `B`) × 4 cost rungs.

**Two tuned dials, every value reported.**  HAIRCUT DEPTH `d ∈ {0.05, 0.10, 0.20, 0.30}` —
at each depth `round(d × 55)` single names are dropped at random from the panel, 100 seeded
draws on U56 and 30 on B136, with σ20 **re-estimated on the surviving names** as a real
investor on a shorter list would.  CHOOSER SET — seven legal IS-only rules reading 2009–2016
alone: `IS_SHARPE`, `IS_LEGS`, `IS_CALMAR`, `IS_MINMARG`, `IS_CAGRSLACK`, `IS_DD` and
`CELL_ALPHA` (a deliberate **no-information control**: it takes the alphabetically first cell
label).  Reported, not tuned: 1795's own ladders `t ∈ {0.08,0.10,0.12,0.16,0.20}` ×
`B ∈ {0.5,1.0,1.5,2.0,3.0,5.0}`, cost {0,10,25,50} bps, trade cadence M, panel U56 (the
candidate's own) with B136 as a replication arm, σ fixed at the standing memo's (L=20, d=0),
and a SPY-droppable haircut control at d = 0.20.

**Gates 6 of 6 PASS.**  G0 18.7 y.  **G1 the d = 0 cell reproduces the committed 1795
candidate to `1.21e-04`** (FULL 14.07% / 1.2509 / −15.90%, OOS 15.40% / 1.3570 / −15.90%).
G2 the d = 0 draw drops nothing.  G3 gross never exceeds 1.000000 on any draw.  **G4 all 520
haircut draws are distinct name sets** (100/100 at each U56 depth, 30/30 at each B136 depth).
G5 all four cost rungs are scored off ONE gross run.
*G1 earned its keep: the first build dropped SPY from the d = 0 panel and missed the committed
numbers by 5.07e-03.  The bug is fixed; SPY is a held name in every keep-SPY draw.*

## V1 — TRIGGERED, and by a wide margin.  The cell does not care which names it holds

U56, published cell, 10 bps, share of draws clearing **4b FULL+OOS**:

| depth | names held | 4b FULL+OOS | mean CAGR [5–95%] | mean MaxDD [5–95%] | mean OOS Sharpe |
|---|---|---|---|---|---|
| 0.00 (undamaged) | 56 | 1/1 | 14.07% | −15.90% | 1.3570 |
| 0.05 | 53 | **100/100** | 14.02% [13.50, 14.44] | −16.11% [−16.83, −15.54] | 1.3473 |
| 0.10 | 50 | **100/100** | 13.95% [13.14, 14.57] | −16.17% [−17.19, −15.22] | 1.3365 |
| 0.20 | 45 | **100/100** | 13.83% [12.73, 14.61] | −16.31% [−17.85, −14.75] | 1.3245 |
| 0.30 | 40 | **100/100** | 13.80% [12.59, 15.16] | −16.26% [−17.93, −14.44] | 1.3175 |
| 0.20, SPY also droppable | 45 | **100/100** | 13.87% | −16.26% | 1.3281 |

B136 replicates: **30/30 at every depth**, mean OOS Sharpe 1.2815 → 1.2625 over d = 0.05 → 0.30.
The DD margin (the leg that kills most 4b candidates in this record) degrades gracefully:
**+4.33 pp undamaged → +3.97 pp at d = 0.30**, 5th percentile +2.30 pp; the **worst single draw
of 400** reads −18.56% MaxDD, still **+1.67 pp inside the −20.23% cap**, with CAGR 12.80% and
OOS Sharpe 1.2852.  The CAGR margin runs +3.47 → +3.21 pp, 5th percentile +2.00 pp.  The
minimum over all five 4b legs across all 400 draws is **+0.0129 — never negative**.
On the cost ladder the cell holds 100/100 at 0, 10 and 25 bps at every depth, and 95/100 at the
single worst corner (50 bps × d = 0.30).

## V2 — TRIGGERED.  It is not a one-chooser artefact, but only one chooser finds *this* cell

On the undamaged U56 panel, **4 of 7 choosers reach a cell clearing 4b FULL+OOS**:
`IS_SHARPE` → t=0.16|B=5.0 (OOS 16.63% / 1.2728 / −19.77%), `IS_LEGS` → **the published cell**
(15.40% / 1.3570 / −15.90%), `IS_CALMAR` → t=0.10|B=3.0 (14.54% / 1.3289 / −18.12%),
`IS_CAGRSLACK` → t=0.20|B=5.0 (17.44% / 1.2454 / −19.98%).  The three that miss all miss on the
**same leg, L4_DD**: `IS_MINMARG` (−23.84%), `IS_DD` (−24.29%) and `CELL_ALPHA` (−27.77%).
B136: 4 of 7 reach, and `IS_LEGS`/`IS_CALMAR` there produce the run's **only 4a passes**
(t=0.08|B=3.0, OOS 11.88% / 1.3288 / −12.07%).
Only `IS_LEGS` ever lands on the published cell — 55.0% of haircut draws; pooled over all seven
choosers the published-cell rate is 9.5%.

## V3 — NOT TRIGGERED (0.4671).  This is the finding, and it is a chooser finding

Pooled over all 2,800 (draw, chooser) pairs on U56 keep-SPY haircuts at 10 bps, the 4b FULL+OOS
share is **0.4671 (1,308 / 2,800)**, below the pre-stated 0.50 bar.  Per chooser:

| chooser | U56 share (rank) | B136 share (rank) |
|---|---|---|
| `IS_LEGS` | **0.785** (1) | 0.300 (5) |
| `IS_MINMARG` | 0.708 (2) | 0.517 (3) |
| `IS_SHARPE` | 0.680 (3) | **0.983** (1) |
| `IS_CAGRSLACK` | 0.578 (4) | 0.950 (2) |
| `IS_CALMAR` | 0.458 (5) | 0.500 (4) |
| `IS_DD` | 0.058 (6) | 0.033 (6) |
| `CELL_ALPHA` (null) | 0.005 (7) | 0.008 (7) |

**The spread is 157x from best to worst chooser on the same grid, same draws, same book.**  The
chooser is therefore a live, unpriced dial of this family, not a formality — and its ranking is
**not portable**: Spearman ρ(U56 rank, B136 rank) over the seven rules is **+0.5357**, and the
two informative rules at the top swap ends (`IS_LEGS` 0.785 → 0.300, `IS_SHARPE` 0.680 → 0.983).
A lane that had run 1795 on B136 would have picked a different cell by a different rule and
called a different candidate.
Decay in `d` is real but small: 0.499 / 0.496 / 0.446 / 0.429 over d = 0.05 / 0.10 / 0.20 / 0.30.
Per draw, **97.75% of draws have at least one of the seven choosers reaching 4b** and the mean
count is 3.27 of 7 — the family always contains a passing cell; the question is only whether
the rule you committed to in advance finds it.

**Stated plainly and not re-cut to pass:** the 0.50 bar was pre-registered over the FULL seven-rule
set, which deliberately includes a no-information control (`CELL_ALPHA`, 0.005) and a leg-blind
one (`IS_DD`, 0.058).  Dropping those two lifts the share to **0.6415 (U56) and 0.6500 (B136)**.
That number is reported for the reader, **not substituted for the pre-stated verdict.**

## V4 — TRIGGERED.  V5 — TRIGGERED

0.4671 against the record's committed zero-signal RAND 4b base rate of **0.0360** (idea 907
lane B, 10 bps): **13.0x**.  So the family is decisively not noise even at its pooled worst, and
the `CELL_ALPHA` control's 0.005 confirms the informative choosers are doing real work on this
grid rather than inheriting a generous cell population.
V5: the published cell keeps its 4b verdict at t+2 in **1.000** of draws at every depth on both
panels.

## Path 4a — dead, as it was for 1795

0.0000 on U56 at d = 0.05 / 0.10 / 0.20 and 0.0017 at d = 0.30; 0.014–0.033 on B136.  The
whole-grid 4b census runs 0.4413 → 0.4130 over the U56 depths (0.5344 → 0.5156 on B136), and
the failing leg is **L4_DD in ~88% of failures at every depth** (e.g. 1,456 of 1,657 at
d = 0.05), with L5_CAGR a distant second.  This corroborates the record's standing reading that
the DD cap is the leg that binds for this family, while confirming the published cell sits
comfortably inside it.

## Verdict

| rule | | |
|---|---|---|
| V1 cell survives the haircut at every d ≤ 0.20 | **YES** | 400/400 U56, 120/120 B136 |
| V2 more than one chooser reaches 4b on the clean panel | **YES** | 4 of 7 |
| V3 pooled (draw, chooser) 4b share > 0.50 | **NO** | 0.4671 |
| V4 that share beats the zero-signal RAND base rate | **YES** | 13.0x |
| V5 the cell keeps its 4b verdict at t+2 | **YES** | 1.000 |

**CAPITAL — by the pre-stated rule, the 1795 candidate is DOWNGRADED from KEEP-4b candidate to
PARK, on the CHOOSER leg only.**  The admission exposure the idea was filed to test is CLOSED
in the candidate's favour and closed hard: a 30% random deletion of the name list moves its DD
margin by 0.36 pp and its OOS Sharpe by 0.040, and never once breaks a 4b leg in 400 draws.
What is NOT closed is that the cell's reachability is a property of the chooser, that the
chooser is a dial nobody has priced, and that its ranking inverts between the two panels the
record uses interchangeably.  **A candidate reachable only by the rule that happened to be run
is not yet capital.**  The constructive next step is not another haircut: it is to ask whether
any chooser is stable ACROSS panels, and to score `IS_LEGS`-style leg-counting against
`IS_SHARPE` on a panel neither was selected on.

## Survivorship — a limit of this test, not a footnote

U56 and B136 are **CURRENT-constituent** lists.  A random deletion haircut is a **LOWER BOUND**
on point-in-time damage, not an estimate of it: it removes winners and losers in the proportion
the current list already carries, whereas a true point-in-time panel would **ADD** names that
later failed or were acquired.  So V1's 400/400 is a **necessary** condition cleared, not a
sufficient one, and every CAGR and drawdown LEVEL above remains optimistic.  The haircut and
chooser CONTRASTS are same-tape / same-grid and first-order immune; the pass counts are not.

RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py were not modified.

# Idea 536R — is the MA-residual DRIFT a REGIME, not a PANEL? (INDEPENDENT REPLICATION)

**cloud, 2026-09-11 — filed as 536R, an INDEPENDENT REPLICATION of lane B's same-day answer, NOT
a second claim.** Both lanes claimed idea 536 within the same hour and worked it without sight of
each other; lane B pushed first (`..._B.py`). This file is published because the two runs used
DIFFERENT window ladders and different decomposition statistics and **agree on every hard number
that both computed** — and because lane B's run contains one finding that CORRECTS this one (see
*Where lane B is right and this run was not*). Verdict: **SPLIT — the regime reading wins on the
variance, the 2020+2022 mechanism is KILLED, and the two-half cut overstated two of the three
published drifts. No RULES change, no book promoted; RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py untouched.** One rule-8-reachable 4b pass is reported with a memo and is NOT
recommended — see the last section.

## Cross-lane agreement and the one correction
| statistic | this run (cloud) | lane B | agree |
|---|---|---|---|
| KEEP 4a over the 324-book grid | **0** | **0** | ✓ |
| KEEP 4b over the 324-book grid | **16** | **16** | ✓ |
| WF-A picks, 4a / 4b | **0 / 1** of 12 | **0 / 1** of 12 | ✓ |
| picks beating the LIVE RULES v2 on OOS Sharpe | **0** of 12 | **0** of 12 | ✓ |
| reproduction of idea 301's `.decomp.csv` | 486/486, SMALL439+B136 exact, U56 ≤ 6.864e-03 pp | 486/486, 2.220e-16 pp | ✓ (see note) |
| axis of the residual: TIME or PANEL | TIME (48.3% vs 4.2% incremental) | TIME (partial R² window > panel, 8/8 dials) | ✓ |
| 2020+2022 as the mechanism | KILLED | KILLED (2020 alone reverses the sign; 2022 offsets) | ✓ |
| is the time factor SHARED across panels? | *this run said yes (ρ +0.198…+0.542)* | **NO — U56 is nested inside B136** | ✗ — lane B is right |

**Where lane B is right and this run was not.** This run read the positive cross-panel correlation
of the rolling residual (+0.198…+0.542, positive at every one of the 8 points) as evidence of a
*shared* time factor. Lane B shows that reading is wrong for a reason this run never checked:
**U56 is nested inside B136 — 55 of its 56 names, min-share 1.0000** — so the U56–B136 pair is
one universe measured twice (ρ +0.9032 median, 8/8 ≥ +0.50) while the two genuinely DISJOINT pairs
read ρ +0.1372 median, 0 of 16 ≥ +0.50. This run's own paired-gap table is consistent with that
and did not notice it: the U56−B136 gap is the small, near-significant one (+0.1286 pp, mean
t +1.52) precisely because those two panels are the same names. **The correct statement is lane
B's: the axis is TIME, but the time factor is PANEL-SPECIFIC, not common.** Everything below that
quotes a cross-panel correlation should be read under that correction.

**A note on the reproduction tolerance.** Both lanes re-derive idea 301's committed decomposition
on all 486 rows. This run reads SMALL439 and B136 as **exact (0.00000000)** and U56 at
**6.864e-03 pp**; lane B reads the whole thing at 2.220e-16. The two are not in conflict — they
are different comparands, and the U56-only residue here is the `data/prices.csv` vintage channel
ideas 513/515/692 priced (U56 is the only panel whose price file the daily job touches). Idea 301
itself recorded 1.287e-02 pp on the same channel; today it is smaller.

## A correction this run owes its own first draft
The first version of this file judged PROTOCOL 4a against **RULES v2 re-run on each panel's own
names**. That is a matched-universe object, not the live book; PROTOCOL 4a means *beat the book*,
and ideas 298/301 (and lane B) build that comparand as RULES v2 on **U56** reindexed onto each
panel's calendar. Corrected here: 4a is judged against the live U56 book throughout, which moves
this run's 4a count from 9 to **0** and its "beats RULES v2" count from 7 to **0** of 12 — into
exact agreement with lane B. The matched-universe number is retained as the labelled `v2m_*`
diagnostic and is never used for a verdict. *Bears on the record generally: idea 295/533's
168-panel corpus computes its `base_*` per panel, so every `beats_v2` flag on that ladder —
including idea 715's, filed earlier today — is a matched-universe statement, not a live-book one.*

## Answer in one line
**Both, and the record's version is the wrong half.** On rolling windows the MA-THRESH timing
residual's *variation* is overwhelmingly a common TIME factor — **TIME given PANEL 48.3%** of the
variance against **PANEL given TIME 4.2%** (medians over the 8 (W, S) points, an 11.5× ratio) —
and **no paired panel gap reaches |t| ≥ 1.96 on non-overlapping windows**. But the specific
IS→OOS drift idea 301 published is **not** 2020/2022: dropping those windows flips B136
(−0.0276 → **+0.0690**) and U56 (+0.0125 → **+0.0978**) while **SMALL439 is unmoved
(−0.4554 → −0.4528)**.

## Gates
- **G1** — 486 of 486 rows of idea 301's committed `.decomp.csv` re-derive. **SMALL439 and B136
  EXACT at 0.00000000** on all four columns (324 rows); the 162 non-exact rows are **all U56**, max
  |Δresid0| **6.864e-03 pp** — the `data/prices.csv` vintage channel ideas 513/515/692 priced,
  today smaller than idea 301's own 1.287e-02. PASS at idea 301's pre-registered 1e-2 pp bar.
- **G2** — leverage identity |r_dg,t − c_t·r_rs,t| ≤ **5.551e-17** over all 162 cells. PASS at 1e-12.
- **G3** — idea 301's three published drifts re-derive: U56 −0.0222 (pub −0.02), B136 **−0.2423
  (exact)**, SMALL439 −0.5717 (pub −0.57). **And its +0.1355 pp pooled bias re-derives exactly
  (|Δ| 3.2e-05)** — but only when BOTH families are pooled under one IS global mean. On MA-THRESH
  alone the same object is **−0.2787 pp**: pooling the near-zero QUANTILE family halves it and
  flips the sign convention. *The record should quote which pooling a bias number came from.*

## Design (2 tuned parameters, all 16 grid points reported)
Idea 298/301's grid verbatim — 3 panels × 2 gate families × 9 levels × 3 cadences = **162 cells,
324 books**, gross 0.75, 10 bps, next-day execution, 0-bps rung derived exactly — re-cut on
rolling windows of **W ∈ {2, 3, 4, 5} years** stepped **S ∈ {6, 12} months**. Panel, family, level
and cadence are inherited reported axes. QUANTILE is a **reported control family, not evidence**:
c_t ≡ x by construction there, so its residual is ~0 by identity.

## The decomposition
| family | var TIME | var PANEL | TIME given PANEL | PANEL given TIME | cross-panel ρ |
|---|---|---|---|---|---|
| **MA-THRESH** | 42.4–63.9% (med **49.2%**) | 0.4–17.5% (med **5.1%**) | **48.3%** | **4.2%** | +0.198 … +0.542 — *but see the nesting correction above: this is the U56⊂B136 pair* |
| QUANTILE (control) | 7.8–22.9% (med 11.6%) | 14.6–49.2% (med 29.6%) | 10.3% | 27.7% | **−0.205 … +0.006, mostly negative** |

The control inverts on every column. Where the gate has real timing content the residual is
dominated by a time axis; where it has none by construction it is a per-panel measurement floor.
That is the internal validation of the TIME-over-PANEL reading — which survives lane B's
correction, since that correction is about whether the time factor is *shared*, not about which
axis carries the variance.

**Paired panel gaps on non-overlapping windows only** (window-demeaning is *not* used as a test —
it shifts each window by a constant and leaves the spread of the panel means algebraically
unchanged): MA-THRESH SMALL439-vs-U56 **−0.2409 pp, mean t −0.74**; U56-vs-B136 **+0.1286 pp,
mean t +1.52**; the largest single |t| anywhere is **1.96** (W=5, U56 vs B136). **No panel
difference separates from zero.**

## Where the published drift actually comes from (MA-THRESH, pp/yr, mean over the 8 points)
| panel | ALL | drop 2020 | drop 2022 | drop 2020+2022 | two-half (idea 301) |
|---|---|---|---|---|---|
| U56 | +0.0125 | +0.0141 | +0.0874 | **+0.0978** | −0.0222 |
| B136 | −0.0276 | −0.0153 | +0.0468 | **+0.0690** | **−0.2423** |
| SMALL439 | **−0.4554** | −0.4030 | −0.5055 | **−0.4528** | −0.5717 |

Two corrections to the record: the two-half cut **overstates B136's drift by ~8.8×**
(−0.2423 vs a rolling −0.0276) and **reverses U56's sign**; and SMALL439's drift is the one real
effect, is **not** a 2020/2022 artefact, and is the only thing the "panel" reading was ever about.

## Rule 8 walk-forward
**WF-B — the deliverable.** Four IS-only predictors of a cell's OOS residual, scored once
(MA-THRESH, 81 cells, OOS MAE): **IS GLOBAL 0.3521 < IS PANEL 0.3904 < TRAIL-2y 0.4576 < ZERO
0.4905 < TRAIL-5y 0.4679 … TRAIL-3y 0.7954**. So **neither reading is actionable**: the panel
constant (idea 301's rival) loses to one global number, and the trailing-regime estimator the
regime reading implies loses to both. The pooling unit is neither the panel nor the recent
window — consistent with idea 301's own "the unit is the GATE FAMILY". On QUANTILE the ordering
inverts (TRAIL-3y best at 0.0161) but that family's residual is ~0 by identity, so it measures
this run's window-length floor, not information.

**WF-A — the book.** (level, cadence) chosen per panel × family × construction on IS Sharpe alone,
OOS read once. Over the 12 picks: **beat the LIVE RULES v2 0** (the matched-universe RULES v2, a
different object, is beaten by 7), **beat SPY 8, beat the no-filter control 5; 4a 0, 4b 1.** Over
all 324 books: **4a 0, 4b 16**; binding 4b bars DD 210, CAGR 172, OOS 127,
H2 122, H1 114. **None of the 16 4b passers passes 4a** (nothing in the grid does), and their MaxDD range
[−0.2022, −0.1655] sits entirely within 3.68 pp of the 4b DD cap (0.2023).

**Cost appendix** — the 12 picks re-priced at 0/10/25/50 bps exactly off the same book: 4b passes
**1 of 12 at every rung**, i.e. the single pass is cost-robust while ten of the twelve fail at
0 bps too.

## The one 4b pass — reported, memo'd, NOT recommended
U56 / QUANTILE / RESPREAD / x = 0.50 / monthly, gross 0.75, 10 bps, 2009-01-13 → 2026-09-10:
**CAGR 15.47% · Sharpe 1.2359 · MaxDD −19.80% · halves 1.3518 / 1.1454 · OOS 15.95% / 1.2164 /
−19.80% · turnover 3.11×/yr**, against **SPY 15.11% / 0.8835 / −33.72%, halves 0.9595 / 0.8211,
OOS 15.24% / 0.8721 / −33.72%**. All five 4b bars pass, at 0, 10, 25 and 50 bps, with the level
chosen on IS Sharpe alone (x = 0.50 is the IS argmax at 1.2665). Memo:
`2026-09-11_4b-candidate-U56-MA-DISTANCE-TOP-HALF-monthly_memo.md`.

**Why it is not recommended, in the same breath:** (1) it **loses to the live book out of sample**
— the live RULES v2 (U56) reads OOS Sharpe **1.2834** against this book's 1.2164, and it fails 4a
outright (as do all 324 books here, and all 16 of the 4b passers); (2) the binding bar is the DD cap and the margin is **0.43 pp** (−0.1980 against
−0.2023), with the neighbouring levels x = 0.20/0.30/0.70/0.80/0.90/0.95 all failing on DD — a
window two rungs wide, the knife-edge shape ideas 670/675/677 have documented; (3) the base rate
argues against reading it as evidence: **16 of 324 books here (4.9%)** clear 4b, and idea 502
measured **78.1% of gross-matched coin flips** clearing 4b on U56 at 0 bps; (4) **survivorship** —
U56 is a current-constituent list, so the level is optimistic.

## Caveats
SURVIVORSHIP (idea 54, `data/SMALL_PANEL_README.md`): `prices_small.csv.gz` (44 names with
`max_1d_move ≥ 1.0` dropped first), `universe.json` and `universe_broad.json` are all **current
constituents** — no delistings — so every CAGR level is inflated and the 4a/4b columns inherit
that whole. The headline object is an arm-minus-arm contrast on the same names and days (DEGROSS
and RESPREAD share one gate mask), so the bias very largely cancels out of gap0/pred0/resid0; it
does **not** cancel out of the KEEP columns. Rolling windows overlap, so every t quoted above is
computed on disjoint windows only (n_indep 3–7) and is correspondingly low-powered — which is
itself part of the finding: at this sample length a panel effect of the published size is not
measurable.

Artefacts: `.grid.csv` (324) `.decomp.csv` (486) `.rolling.csv` `.anova.csv` `.drift.csv`
`.walkforward.csv` `.walkforward_estimators.csv` `.costappendix.csv` `.console.txt`

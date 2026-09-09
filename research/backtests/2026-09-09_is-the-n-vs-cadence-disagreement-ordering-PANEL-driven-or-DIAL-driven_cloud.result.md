# Idea 499 — is the n-vs-cadence disagreement ordering PANEL-driven or DIAL-driven? (cloud, 2026-09-09)

**Verdict: ANSWERED. The ordering is DIAL-driven, and the panel set is nearly irrelevant.
Run both idea-270 dial sets on the SAME twelve panels and the ordering flips completely:
Delta = rate(n) − rate(cadence) is +0.500 under lane B's parameterisation and −0.417 under
the cloud parameterisation, |Delta_B − Delta_C| = 0.917 at permutation p 0.0012. Cutting the
panel set from 12 to the cloud parent's 3 moves Delta by at most 0.167 and never changes its
sign. KILL of "the two runs disagreed because they used different panels". No KEEP-candidate,
no memo, no RULES change; RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.**

Script `2026-09-09_is-the-n-vs-cadence-disagreement-ordering-PANEL-driven-or-DIAL-driven_cloud.py`;
outputs `.arms.csv` (915 rows — ALL grid points), `.cells.csv` (330 selector cells),
`.factorial.csv`, `.walkforward.csv`, `.console.txt`. Runtime 1050 s. 10 bps headline
(25 bps rung on the three cloud panels), weekly base cadence except on the cadence dial,
next-day execution, long only. PROTOCOL rule 8 throughout: both selectors see IS
2009-01-01..2016-12-31 only and OOS 2017-01-01+ is read once.

## Design

Two factors, the queue's own, crossed:

* `dialset` ∈ {B, CLOUD} — each parent's dial families lifted **verbatim** from its own
  script (arm lists, book forms, and for lane B's `n` its EWall arm and `sat_share ≤ 0.25` cap).
* `panelset` ∈ {B12, CLOUD3} — CLOUD3 = {U56, B136, SMALL439} is a strict **subset** of
  B12 (those three + BSTK100 + lane B's 8 pre-registered seeded sub-panels), so the whole
  grid is computed once on the 12 shared panels and the 3-panel reading is the same numbers
  re-read, never a separate run.

Two nuisance conventions the parents also differ on are carried as free reporting axes:
the IS/OOS split (CAL = protocol rule 8 calendar, lane B's; MID = sample midpoint, the
cloud parent's) and the cost rung. A cell (panel, dial) **disagrees** iff argmax IS_Sharpe
and argmax IS_CAGR pick a different arm — both parents' own definition, arm identity, no
tie band. Tuned parameters: **one**, the dial value inside a cell, chosen on IS only.

## Reproduction gates — both PASS exactly, before any new number was read

| gate | reproduced | published |
|---|---|---|
| G1 cloud parent (CLOUD dials, CLOUD3, MID split, 10+25 bps) | **11/36**; cadence 4/6, volcap 3/6, band 2/6, n 2/6, gross 0/6, quantile 0/6 | 11/36; cadence 4/6, volcap 3/6, band 2/6, n 2/6, gross 0/6, quantile 0/6 |
| G2 lane B (B dials, B12, CAL split, 10 bps) | **12/60**; n 7/12, trim 2/12, cadence 1/12, gross 1/12, volgate 1/12 | 12/60; n 7/12, trim 2/12, cadence 1/12, gross 1/12, volgate 1/12 |

Both parents' headline counts are recovered to the cell. The non-replication between them
is therefore real and is not an implementation difference in this run.

## The answer — the 2×2 (Delta = rate(n) − rate(cadence), 10 bps)

| split | panelset | dialset | Delta | n | cadence | ordering |
|---|---|---|---|---|---|---|
| CAL | B12 | B | **+0.500** | 7/12 | 1/12 | B-like |
| CAL | B12 | CLOUD | **−0.417** | 1/12 | 6/12 | cloud-like |
| CAL | CLOUD3 | B | +0.667 | 2/3 | 0/3 | B-like |
| CAL | CLOUD3 | CLOUD | −0.333 | 0/3 | 1/3 | cloud-like |
| MID | B12 | B | +0.583 | 8/12 | 1/12 | B-like |
| MID | B12 | CLOUD | −0.333 | 2/12 | 6/12 | cloud-like |
| MID | CLOUD3 | B | +0.667 | 2/3 | 0/3 | B-like |
| MID | CLOUD3 | CLOUD | −0.333 | 1/3 | 2/3 | cloud-like |

**The dial set decides the sign in all four rows; the panel set never does.**

* Dial-set effect, panels held fixed: Delta swings **+0.500 → −0.417** on B12 and
  **+0.667 → −0.333** on CLOUD3.
* Panel-set effect, dial set held fixed: **+0.500 → +0.667** (B dials) and
  **−0.417 → −0.333** (CLOUD dials) — magnitude moves ≤ 0.167, sign never.
* Split convention, dials and panels held fixed: **+0.500 → +0.583** (B) and
  **−0.417 → −0.333** (CLOUD) — ≤ 0.083, sign never.
* Cost rung (CLOUD3, CAL): B **+0.667 at both rungs**; CLOUD −0.333 → 0.000 at 25 bps,
  a move from 1/3 to 0/3 cells and not a sign change worth the name.

Tests on the 12 shared panels, CAL, 10 bps: McNemar on the `n` dial **B-only 6,
CLOUD-only 0, exact p 0.0312**; on `cadence` **B-only 0, CLOUD-only 5, exact p 0.0625**.
Permutation with the dial-set labels exchangeable within each (panel, dial):
**|Delta_B − Delta_C| = 0.9167, p 0.0012** (20,000 draws, seed 499).

## Why — the mechanism, from two contrasts the grid already isolates

**1. Cadence isolates BOOK FORM with the arm list held exactly fixed.** Both parents sweep
the identical four arms D/W/M/Q. Lane B applies them to an **EWall** base book (1/12
disagreements); the cloud parent applies them to the **RULES-v2 band** book (6/12). All six
cloud disagreements have the same shape — S_SHARPE picks `W`, S_CAGR picks `M` or `Q` — a
systematic "CAGR wants a slower book" that simply does not exist on the EWall base. Nothing
about the panels changes between the two columns.

**2. The `n` dial differs in its MENU ENDPOINTS, not in the panels.** Lane B's ladder
carries an `EWall` arm alongside FWD 5…60 under the saturation cap; 5 of its 7
disagreements are S_SHARPE picking `EWall` or a wide FWD against S_CAGR picking **FWD5**,
the narrowest arm. The cloud ladder has no EWall arm and its two selectors land on the same
endpoint (`N50` five times, `N5` four times), disagreeing once in twelve.

**3. Corroboration on the band family.** Lane B's `trim` and the cloud's `band` are the same
book form with different arm lists (…0.05, 0.08 vs …0.08, 0.12): 2/12 vs 5/12. Arm-list
composition moves disagreement even when the book form is held fixed.

The honest caveat: "dial set" bundles the base book form, the ranking key, the eligibility
legs, the arm list and (for `n`) the saturation cap. Contrast 1 unbundles the book form
cleanly; contrast 3 unbundles the arm list cleanly; the `n` contrast does not, and its
sub-factors are a follow-up.

## Per-dial rates on the 12 shared panels (CAL, 10 bps)

| dialset | dial | rate | | dialset | dial | rate |
|---|---|---|---|---|---|---|
| B | n | 7/12 = 0.583 | | CLOUD | cadence | 6/12 = 0.500 |
| B | trim | 2/12 = 0.167 | | CLOUD | band | 5/12 = 0.417 |
| B | cadence | 1/12 = 0.083 | | CLOUD | volcap | 3/12 = 0.250 |
| B | gross | 1/12 = 0.083 | | CLOUD | quantile | 2/12 = 0.167 |
| B | volgate | 1/12 = 0.083 | | CLOUD | n | 1/12 = 0.083 |
| | | | | CLOUD | gross | 0/12 = 0.000 |

Pooled disagreement: B 12/60 (20.0%), CLOUD 17/72 (23.6%) — the *pooled rate* replicates
across parameterisations to within 4 points; only its **attribution to dials** does not.
`gross` at 0/12 stays mechanical (Sharpe is near-invariant in gross, CAGR monotone).

## Rule 8 walk-forward — neither selector earns its keep (OOS 2017+, read once)

Mean over all 132 ten-bps CAL cells (both dial sets, 12 panels):

| | S_SHARPE | S_CAGR | DONOTHING | RULES v2 (live) | RULES v1 | SPY |
|---|---|---|---|---|---|---|
| OOS Sharpe | 0.8007 | 0.7807 | **0.8074** | **0.9196** | 0.4641 | 0.8817 |
| OOS CAGR | 8.74% | 8.77% | 8.17% | 7.01% | 5.49% | **15.44%** |

S_SHARPE beats the do-nothing control in **56/132** cells, S_CAGR in **52/132**. Both trail
the live RULES v2 book on OOS Sharpe by ~0.12 and SPY on OOS CAGR by ~6.7 pp. Another
idea-229 instance, agreeing with both parents. Per-dial rows are in `.walkforward.csv`.

## Both KEEP paths, all 870 arm rows

* **CAL: 4a 14/870, 4b 48/870.** MID: 4a 18/870, 4b 44/870.
* The 46 CAL 4b passers at 10 bps sit on B136 (14), U56 (15), the four B60 sub-panels (15)
  and BSTK100 (2) — **zero on SMALL439 or any M120 panel** — and are led by `volgate` 12,
  `gross` 10, `n` 10: the open-eligibility, higher-gross equal-weight book again, the same
  shape idea 270R published. None is a new book form.
* The 14 CAL 4a passers are **13 band-book arms and one duplicate pair**: `SMALL439` band
  0.05 at 10 and 25 bps appears **once under each dial set with identical numbers**
  (4.17%/0.6170/−14.6% at 10 bps, 3.81%/0.5673/−15.1% at 25 bps) — a same-book cross-check
  that the two parameterisations price the identical arm identically. That arm is idea
  270R's own flagged case and is **again NOT filed as a KEEP candidate**: its Sharpe curve
  is monotone in the band out to the widest point tested (S7_M120 shows 0.05 → 0.08 → 0.12
  at 0.6658 → 0.7180 → 0.7244), so idea 240/256/328's grid-edge flag applies. The remaining
  4a rows are seeded sub-panels, which ideas 78/83 already priced as passing by construction.

**No KEEP-candidate, no memo.**

## Caveats

SURVIVORSHIP: B136 / BSTK100 are current constituents of `universe_broad.json`; SMALL439 is
the 483-name sub-$2B screen with the 44 tickers whose `max_1d_move ≥ 1.0` dropped first
(`data/small_meta.csv`, `data/SMALL_PANEL_README.md`); the 8 seeded sub-panels inherit that
bias. Twelve panels is a small denominator for a rate difference, which is why the headline
is carried by a paired within-panel test rather than by two independent proportions. The
25 bps rung exists only on the three cloud panels, so the cost row is read on 3 cells per
arm and is reported as indicative. No network was used.

## Proposed follow-ups

1. Unbundle lane B's `n` dial: hold the ranking key and eligibility legs fixed and add /
   remove the `EWall` arm alone, to price how much of the 7/12 is the endpoint's presence.
2. Census the record for published "dial X disagrees most" claims and re-read each with its
   base book form stated beside it — contrast 1 says the book form, not the dial name, is
   the carrier.
3. Require every committed selector grid to publish its base book form and its arm list, so
   two runs of "the same dial" are comparable at all.

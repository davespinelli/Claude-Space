# Idea 567 — how-many-published-PANEL-ORDERING-claims-survive-a-draw-level-noise-floor

Lane B, 2026-09-11. Script: `2026-09-11_how-many-published-PANEL-ORDERING-claims-survive-a-draw-level-noise-floor_B.py`
Artefacts: `.grid.csv` (900) `.floors.csv` (60) `.census.csv` (607) `.verdicts.csv` (40) `.walkforward.csv` `.keeppaths.csv` (900) `.console.txt`

## VERDICT

**ANSWERED / KILL of the three-panel ordering as evidence — and a KILL for capital (BOTH 0/900, no new KEEP, no memo).**
The floor is real and reproduces independently; the alarm is **not** corpus-wide, but it is decisive exactly where
idea 312 raised it, and **out of sample the entire published U56 > B136 > SMALL439 span sits inside the floor**.

## GATES (all pre-registered, all run before any new number was read)

| gate | what | result | bar | |
|---|---|---|---|---|
| G0 | draw scheme rebuilt twice, 72 draws | `0` differ | 0 | PASS |
| G1 | `fast_backtest` vs `engine.backtest`, one book per parent | `0.000e+00` | 1e-12 | PASS |
| G2 | idea 312's committed `.noisefloor.csv` rebuilt from its own `.grid.csv`, all 11 rungs (lo/hi/rng/sd/pairs/pairs_ge_GAP) | `1.110e-16` | 1e-12 | PASS |
| G3 | idea 312's headline `0.0745` mean within-rung sd and `65/165 = 39.4%` pair-crossing share | `3.234e-05` / `6.061e-05` | 1e-4 | PASS |

## PRICE LEG — the floor, rebuilt on the REAL parents

k = 36 names per draw, 24 crc32-seeded draws (`DRAW|{parent}|{seed}`) out of each parent, 3 gross x 2 cadence x 2 arms
= 900 books. Parents: U56 (55 tradable + SPY), B136 (135 + SPY), SMALL439 (439 + SPY). Arms are idea 51's verbatim
`EWall` (control) and `MA-RS` (RESPREAD gate), so a premium is pure selection with gross held fixed.

**Tuned parameters: exactly two — STATISTIC (5) x DRAW COUNT D (4). All 20 grid points reported, at both bars.**

Floor = within-parent sd of the statistic across draws, averaged over the 3 gross x 2 cadence cells, pooled over parents.

| statistic | D=3 | D=6 | D=12 | D=24 | parent max/min (D=6) |
|---|---|---|---|---|---|
| PREM_SHARPE | 0.0907 | **0.0813** | 0.0811 | 0.0809 | 1.98x |
| PREM_CAGR | 0.0134 | 0.0133 | 0.0130 | 0.0128 | 2.74x |
| SHARPE | 0.1020 | 0.1074 | 0.1110 | 0.1062 | 1.11x |
| CAGR | 0.0132 | 0.0188 | 0.0192 | 0.0182 | 1.16x |
| MAXDD | 0.0295 | 0.0308 | 0.0392 | 0.0415 | 2.61x |

- **H_FLOOR HOLDS.** The MA-gate premium floor built on the three REAL parents is **0.0813** against idea 312's
  **0.0745** built inside B136 at fixed ETF share — **1.09x**, an unplanned cross-reproduction from a different
  draw population and a different seeding key. The floor is a property of 36-name composition, not of 312's design.
- **H_PARENT HOLDS (1.98x).** U56 **0.0502**, B136 **0.0995**, SMALL439 **0.0941**. U56 draws 36 of 56 names, so its
  draws overlap by construction and its floor is structurally the smallest. **A single pooled floor is the wrong bar:**
  a claim must be scored against the floor of the parents it actually names, and a U56-anchored claim gets the
  easiest bar in the record.
- **H_D HOLDS (swing 0.5 pp).** The share of claims inside moves 42.3% -> 42.8% from D=3 to D=24, so "inside its
  floor" is **not** itself a resolution statement here (idea 528's worry does not bite at this sample size).

## CENSUS LEG — 607 committed panel-ordering claims from 133 files

Harvested from 775 committed markdown files: sentences quoting a recoverable number against >= 2 of
{U56, B136, SMALL439}, classified to a statistic family by keyword, margin = smallest adjacent gap in the quoted
ordering. 142 of the 607 have margin exactly 0 (a number restated for two panels, or a degenerate parse), so the
nonzero count is reported beside every share.

| cut | n | inside 1.0 sd | share |
|---|---|---|---|
| all claims | 607 | 259 | **42.7%** |
| nonzero margin | 465 | 117 | **25.2%** |
| **3-panel claims** (the form the idea names) | 262 | 138 | **52.7%** |
| 3-panel, nonzero margin | 197 | 73 | **37.1%** |
| 2-panel, nonzero margin | 268 | 44 | 16.4% |
| **3-panel PREM_SHARPE** (312's own family) | 55 | 35 | **63.6%** |
| 3-panel PREM_SHARPE, nonzero | 49 | 29 | **59.2%** |

By family at D=6, bar 1.0 sd: PREM_SHARPE **63/101 (62.4%)**, MAXDD 53/118 (44.9%), SHARPE 103/260 (39.6%),
PREM_CAGR 15/42 (35.7%), CAGR 25/86 (29.1%). At bar 2.0 sd PREM_SHARPE goes to 69.3%.

**H_MOST is FALSIFIED for the corpus and HOLDS for the family it was raised on.** The record does not generally quote
panel orderings inside their noise — 74.8% of nonzero-margin claims clear their own floor. But the MA-gate premium,
the statistic idea 51/312 built the "universe boundary" reading on, is inside its floor in **nearly two of three**
three-panel claims. The alarm is specific, not systemic, and it is specific to the claim the record acted on.
Source makes no difference (RECORD-LEVEL files 42.2%, script result/memo files 43.8%), so this is a habit of the
whole record, not of one lane. 69 of 133 files carry at least one inside-floor claim.

## RULE 8 WALK-FORWARD (IS <= 2016-12-31, OOS >= 2017-01-01, OOS read once)

**WF-A — the answer.** Floors rebuilt on IS only and OOS only. IS floors are much wider (PREM_SHARPE 0.1276,
SHARPE 0.1990) than OOS (0.0863, 0.1033); the inside-count is unchanged in 3 of 5 families and moves by <= 5 claims
in the other two. The verdict is not an artefact of the sample half it is measured on.

**The decisive leg — does the published ordering survive its own floor out of sample?**

| gross | cadence | IS order | OOS order | same | IS span | OOS span |
|---|---|---|---|---|---|---|
| 0.50 | W | U56>B136>SMALL439 | U56>B136>SMALL439 | yes | 0.2904 | 0.0788 |
| 0.50 | M | U56>B136>SMALL439 | U56>SMALL439>B136 | **no** | 0.1202 | 0.0510 |
| 0.75 | W | U56>B136>SMALL439 | U56>B136>SMALL439 | yes | 0.2868 | 0.0777 |
| 0.75 | M | U56>B136>SMALL439 | U56>SMALL439>B136 | **no** | 0.1149 | 0.0516 |
| 1.00 | W | U56>B136>SMALL439 | U56>B136>SMALL439 | yes | 0.2831 | 0.0767 |
| 1.00 | M | U56>B136>SMALL439 | U56>SMALL439>B136 | **no** | 0.1097 | 0.0522 |

IS order is the published one in **6 of 6** cells at a median span of **0.2017 = 1.58x the IS floor (0.1276)** — in
sample the ordering clears its bar. Out of sample the median span collapses to **0.0645 = 0.75x the OOS floor
(0.0863)** and the B136/SMALL439 leg **flips at cadence M in 3 of 6 cells**. **The published three-panel ordering is
an in-sample fact whose out-of-sample span is smaller than one panel's own composition luck.** Only the U56 > rest
leg survives OOS, and U56 is the parent with the *smallest* floor, i.e. the leg the noise bar is least able to reject.

**WF-B — the ordering taken as a trading instruction.** (parent, gross, cadence) chosen by IS Sharpe of the MA-RS
book alone on the REAL parents; OOS read once.

Selected: **U56, gross 1.00, cadence M** (IS Sharpe 1.1204).

| | CAGR | Sharpe | MaxDD |
|---|---|---|---|
| selected book, OOS | **18.26%** | **1.1936** | **-23.73%** |
| RULES v2 (same panel), OOS | 9.45% | 1.2747 | -12.05% |
| SPY, OOS | 15.24% | 0.8721 | -33.72% |

The IS-chosen book **loses to the live baseline on Sharpe (-0.0811) while running 11.7 pp more drawdown** — the extra
CAGR is exposure, not skill — and it **fails 4b on the DD leg**. Across all 18 REAL books: beat RULES v2 OOS
**3/18**, beat SPY OOS **12/18**.

## KEEP PATHS (every one of the 900 books scored, both paths)

**4a 2/900, 4b 52/900, BOTH 0/900.** By parent — 4a: U56 2, B136 0, SMALL439 0; 4b: U56 39, B136 13, SMALL439 0.
By kind — 4b: DRAW 49, REAL 3. Binding 4b failure legs: DD 313, the full stack (H1,H2,OOS,DD,CAGR) 206, CAGR 191,
H1,H2,OOS,DD 88.

- Both **4a** passers are random 36-name **DRAW** subsets of U56 (seeds 7 and 19, gross 0.50, cadence M) and both
  **fail 4b on CAGR**. A seeded random subset is not a rule anyone can trade; these are diagnostics of the floor's
  width, not candidates.
- All three **REAL 4b** passers are the plain MA-RS gate at gross 0.75 — U56/W 11.55% / 1.0914 / -18.62%,
  U56/M 12.60% / 1.1594 / -18.21%, B136/W 11.66% / 1.0585 / -20.12% — i.e. the record's existing gate arm re-found
  at its known setting, not a new book. **No new KEEP-candidate, no memo, no rule change.**

## WHAT THIS CHANGES

1. The queue's alarm is **confirmed for the MA-gate premium and rejected as a general habit**: 59-64% of three-panel
   premium claims are inside their own floor, against 16.4% of two-panel claims of any family.
2. The floor is **parent-specific (1.98x)**, so the record's practice of quoting one number for "the panel ordering"
   has been scoring U56-anchored claims against a bar built partly on SMALL439's much wider dispersion.
3. The ordering's **only out-of-sample content is U56 > rest**, at 0.75x its own floor — not enough to carry the
   "universe boundary" reading that ideas 51 and 312 were arguing about.

PROTOCOL proposal for Sunday (not adopted here, rule 6): any claim that one panel orders above another must quote the
draw-level floor of the parents it names, at the same statistic, and state the margin as a multiple of it.

SURVIVORSHIP: `universe_broad.json` and the small panel are CURRENT constituents. The bias lifts the LEVEL statistics
(SHARPE/CAGR/MAXDD floors are lower bounds on true dispersion) and largely cancels in the arm-minus-arm premium.

`RULES.md`, `scan.py`, `bot.py`, `baseline.py`, `PROTOCOL.md` untouched (rule 6).

Follow-ups proposed: 773, 774, 775 (see QUEUE.md).

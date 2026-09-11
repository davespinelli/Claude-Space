# Idea 536 — is-the-MA-residual-DRIFT-a-regime-not-a-panel (lane B, 2026-09-11)

**VERDICT: SPLIT — idea 301's PANEL reading is REFUTED, the queue's REGIME reading is NOT
CONFIRMED, and the third thing is what the data says.** The MA-THRESH timing residual's variance
is overwhelmingly a **time** axis, not a panel axis (partial R²(window) beats partial R²(panel)
at **8 of 8** dials, by up to 128×) — so "SMALL439's residual is unstable" is the wrong
sentence. But the time factor is **not shared**: the record's three panels are not three
readings of one calendar, because **U56 is entirely nested inside B136** (55 of 56 names,
min-share **1.0000**), and every bit of the apparent commonality lives in that one nested pair.
Across the two genuinely **disjoint** pairs the rolling residual series correlate at a median
**ρ +0.1372** (0 of 16 fits ≥ +0.50) against the nested pair's **+0.9032** (8 of 8). The object
is **panel-specific time**. **4a 0/324, 4b 16/324, WF-A picks 4a 0/12 / 4b 1/12 — no KEEP, no
memo, no rules change.**

Grid imported verbatim from ideas 298/301: 3 panels × 2 gate families × 9 levels × 3 cadences =
162 cells / 324 books, 10 bps, gross 0.75, next-day execution, 0-bps rung derived exactly.
Tuned dials (2, the queue's own): **window length L ∈ {2,3,4,5} yr × step S ∈ {6,12} mo = 8
cells, every statistic reported at all 8.**

## B4 REPRODUCTION GATE — PASS, exactly

486 of 486 committed rows matched. `max |Δresid0_pp|` on SMALL439 + B136 = **2.220e-16 pp**
(bar 1e-2). U56 reads **1.152e-02 pp** — the known `data/prices.csv` vintage drift (ideas
513/515; idea 301 failed the same bar at 1.287e-02 on U56 and restated on the 108
exactly-reproducing cells). Identity `max |r_dg,t − c_t·r_rs,t| = 5.551e-17` over 162 cells.
Idea 301's three headline drifts reproduce: **B136 −0.2423, SMALL439 −0.5717, U56 −0.0222**
(published −0.0216; the 6e-4 is that same U56 vintage).

## B1 COMMON-TIME — **FAIL, 0/8**, and the reason is a panel-nesting artefact

| L, S | ρ B136~SMALL439 | ρ B136~U56 | ρ SMALL439~U56 | median |
|---|---|---|---|---|
| 2y, 6mo | +0.3870 | **+0.8391** | +0.2961 | +0.3870 |
| 3y, 6mo | +0.1829 | **+0.9330** | +0.0961 | +0.1829 |
| 3y, 12mo | −0.0495 | **+0.8901** | −0.0769 | −0.0495 |
| 4y, 12mo | +0.0070 | **+0.9510** | −0.1469 | +0.0070 |
| 5y, 12mo | +0.2273 | **+0.9091** | +0.0636 | +0.2273 |

Name overlap, measured in the run: **U56 ∩ B136 = 55 names, min-share 1.0000, Jaccard 0.4074**;
SMALL439 ∩ U56 = SMALL439 ∩ B136 = **0 names, Jaccard 0.0000**. So of the three pairs, one is
the same panel read twice. **DISJOINT pairs (16 fits): ρ median +0.1372, range −0.1469..+0.3870,
0/16 ≥ +0.50. NESTED pair (8 fits): ρ median +0.9032, range +0.7275..+0.9510, 8/8 ≥ +0.50.**
The common-time signal is *entirely* the nesting. STEP 1b is a restatement in the manner of idea
301's own B3b; the bar was not moved.

## B2 VARIANCE — **PASS 8/8 on partial R², but the dof-fair statistic splits at L ≥ 4**

MA-THRESH, two-way fit `resid0_pp ~ 1 + panel + window`:

| L, S | partial R²(window) | partial R²(panel) | F(window) | F(panel) | sd across windows | sd across panels |
|---|---|---|---|---|---|---|
| 2y, 6mo | **0.2939** | 0.0023 | 34.51 | 2.63 | 0.6785 pp | 0.0613 pp |
| 3y, 6mo | **0.2206** | 0.0159 | 23.52 | 16.81 | 0.4723 | 0.1356 |
| 3y, 12mo | **0.1675** | 0.0258 | 17.40 | 13.77 | 0.3974 | 0.1698 |
| 4y, 12mo | **0.1128** | 0.0467 | 11.07 | 23.49 | 0.2667 | 0.1942 |
| 5y, 12mo | **0.0997** | 0.0823 | 9.73 | 39.38 | 0.2123 | 0.2231 |

Window has many more levels than panel, so partial R² favours it mechanically; on the
dof-adjusted F the ordering **reverses at L ≥ 4** (F_window > F_panel in **4 of 8** cells, all
four at L ∈ {2,3}). Read honestly: **at the queue's own 3-year dial time wins on both
statistics**, and the panel level only shows through once 4–5 year windows have averaged the
time swing away. Either way idea 301's per-panel constant is not the governing unit.

**Placebo holds.** On QUANTILE (`c_t ≡ x` by construction) the ordering is reversed —
partial R²(panel) > partial R²(window) at every L ≥ 3, F_panel **62–234** vs F_window **2–5** —
and the whole time swing is **sd 0.0084..0.0227 pp/yr** against MA-THRESH's **0.2123..0.6785**.
The time movement is MA-gate *content*, not an artefact of the decomposition.

## B3 ATTRIBUTION — **FAIL as pre-registered (1/3), because 2020 and 2022 push opposite ways**

MA-THRESH mean resid0 (pp/yr) under the five pre-declared exclusions:

| exclusion | B136 drift | SMALL439 drift | U56 drift |
|---|---|---|---|
| none | −0.2423 | −0.5717 | −0.0222 |
| **2020 only** | **+0.1245** (sign flip) | **−0.2923** (−48.9%) | **+0.3213** (sign flip) |
| 2022 only | −0.4900 | −0.8668 | −0.3962 |
| 2020 + 2022 | −0.0989 (−59.2%) | −0.5508 (−3.7%) | −0.0190 (−14.5%) |
| placebo 2008–09 (IS side) | +0.0968 | −0.5717 (panel starts 2010) | +0.2209 |

**2020 alone over-explains the whole large-cap drift** — deleting it reverses the sign on both
B136 and U56 — and explains **half** of SMALL439's. **2022 is a large offsetting positive**
(deleting it makes every drift much more negative), so the joint 2020+2022 deletion nets out and
the pre-registered bar fails. The placebo is not clean either: deleting 2008–09 moves the *IS*
mean on B136 (−0.2864 → −0.6256) and U56 (−0.3162 → −0.5592). **Single calendar years move this
statistic by more than the published IS/OOS drift itself**, on both sides of the rule-8 boundary.

## Rule 8 — WF-B (the deliverable) and B5

Every predictor fitted on windows ending ≤ 2016-12-31, scored **once** on windows starting ≥
2017-01-01. MA-THRESH scope, OOS MAE (pp/yr):

| estimator | L=2,S=6 | L=3,S=6 | L=3,S=12 | L=5,S=12 | beats GLOBAL |
|---|---|---|---|---|---|
| ZERO | 1.1810 | 1.0051 | 0.9150 | 0.7045 | 0/8 |
| GLOBAL | 1.0803 | 0.9473 | 0.8598 | 0.6265 | — |
| PANEL | 1.0983 | 0.9770 | 0.8957 | 0.6177 | **2/8** |
| FAMILY | 1.0803 | 0.9473 | 0.8598 | 0.6265 | 0/8 |
| **LAG1-PANEL** | 1.0348 | **0.8753** | 0.8441 | 0.6012 | **7/8** |
| LAG1-POOLED | 1.0905 | 0.9194 | 0.8566 | 0.6172 | 3/8 |
| WINDOW-ORACLE (not usable) | 0.9645 | 0.8631 | 0.8090 | 0.6151 | 8/8 |

**B5 FAIL (3/8).** The *pooled* lag — the predictor a shared regime would justify — does not
beat a global constant. The *panel's own* lag does, **7 of 8**, and beats the contemporaneous
oracle in 3 cells. That is the same answer B1 and B2 give from the other side: the time
variation is real and it is panel-specific. **And it is worth almost nothing**: a perfect
contemporaneous regime reader buys only **1.2%–10.7%** of OOS MAE over one global constant.
Every pooled estimator still carries idea 301's positive bias (+0.11 to +0.33 pp/yr).

## Rule 8 — WF-A (the book), and both KEEP paths

(level, cadence) chosen on IS Sharpe 2010–2016 per panel × family × construction, OOS read once.

| panel | family | con | pick | OOS CAGR | OOS Sharpe | OOS MaxDD | RULES v2 OOS | SPY OOS | 4a | 4b fails |
|---|---|---|---|---|---|---|---|---|---|---|
| U56 | QUANTILE | RESPREAD | x=0.50, M | **15.95%** | **1.2164** | −19.80% | 1.2747 | 0.8721 | no | **— (pass)** |
| U56 | MA-THRESH | RESPREAD | θ=0.20, Q | 21.20% | 0.9326 | −32.51% | 1.2747 | 0.8721 | no | DD |
| B136 | MA-THRESH | RESPREAD | θ=0.20, Q | 21.11% | 1.0665 | −29.53% | 1.2851 | 0.8820 | no | DD |
| B136 | MA-THRESH | DEGROSS | θ=−0.25, Q | 13.58% | 1.1384 | −24.16% | 1.2851 | 0.8820 | no | DD |
| SMALL439 | MA-THRESH | RESPREAD | θ=0.30, M | 24.02% | 1.1042 | −30.78% | 1.2851 | 0.8820 | no | DD |
| SMALL439 | MA-THRESH | DEGROSS | θ=−0.40, Q | 7.98% | 0.5874 | −32.47% | 1.2851 | 0.8820 | no | H1,H2,OOS,DD,CAGR |

**WF-A: 4a 0/12, 4b 1/12. Beat RULES v2 on OOS Sharpe 0/12; beat SPY 8/12.** The single 4b
passer is idea 301's / idea 298's own PARK candidate — U56 QUANTILE x=0.50 monthly RESPREAD —
reached again, and it is still a third un-pre-registered dial with no cross-panel replication
and DD near the bar. **PARK re-affirmed, not promoted.**

Whole grid: **4a 0/324, 4b 16/324, both 0/324.** The 16 are ideas 298/301's 16, same cells
(13 U56, 3 B136, **0 SMALL439**). 4b failure signatures: DD 121, all-five 70, CAGR 52,
H1/H2/OOS/CAGR 33, pass 16, remainder ≤ 8 each.

## What this changes in the record

1. **Idea 301's "SMALL439's residual is unstable" is a panel label on a time object.** The
   governing axis is the window, not the panel, at the 2–3 year resolution the record's own
   claims live at.
2. **Two of the record's three panels are one panel.** `U56 ⊂ B136` at min-share 1.0000. Any
   "holds on 3 panels" / "replicates cross-panel" claim built on {U56, B136, SMALL439} has
   **two independent readings, not three**. This is not specific to idea 536 and is the most
   portable thing this run found.
3. **A single calendar year (2020) can reverse a published IS/OOS drift**, and a second (2022)
   can hide it by offsetting. Reporting an IS/OOS drift without a per-year cut is not safe.
4. **Nothing actionable.** The ceiling on regime-reading this statistic is 1.2%–10.7% of MAE.
   Idea 298's zero-parameter constant survives as the practical prescription, for the reason
   idea 301 gave (FAMILY/GLOBAL, not PANEL), and now also because the alternative is worthless.

**SURVIVORSHIP:** `prices_small.csv.gz`, `universe.json` and `universe_broad.json` are all
current constituents — no delistings — so every CAGR *level* is inflated and the 4a/4b columns
inherit that whole. The headline object is an arm-minus-arm contrast on the same names and days
(DEGROSS and RESPREAD share one gate mask), so the bias very largely cancels out of
gap0/pred0/resid0; it does **not** cancel out of the KEEP columns.

`RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and `baseline.py` untouched.

Outputs: `.grid.csv` `.decomp.csv` `.rolling.csv.gz` `.factor.csv` `.pairs.csv` `.exclusion.csv`
`.exclusion.summary.csv` `.estimator.csv` `.walkforward.csv` `.console.txt`

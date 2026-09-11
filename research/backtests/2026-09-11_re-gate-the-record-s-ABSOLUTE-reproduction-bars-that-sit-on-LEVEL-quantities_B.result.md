# Idea 734 — re-gate the record's ABSOLUTE reproduction bars that sit on LEVEL quantities (lane B, 2026-09-11)

Population: (A) every `assert` clause carrying a numeric bar in the 690 committed backtest
scripts — 758 asserts, 426 with a bar; (B) a corpus of cross-script reproduction gaps built
from the record's own committed `.grid.csv` artefacts — 365 usable artefacts, 547 pairs
sharing >= 2 key columns and >= 20 matched rows, **6,144 pair x metric cells over 1,371,716
matched rows**. 10 bps, next-day execution throughout.
Tuned: QUANTITY CLASS (6) x BAR FORM (ABS / REL / HYBRID) x bar ladder (1e-12 ... 1e-2) —
**every grid point reported** in `.grid.csv`.

## Gates (all PASS)
- **G1** `fast_backtest` vs `engine.backtest` on U56: returns **0.000e+00**, turnover **0.000e+00** (bar 1e-12).
- **G2** `EWALL(0.75)` nests `baseline.rules_v2_weights` **0.000e+00**.
- **G3 THE ANCHOR REPRODUCES EXACTLY** — idea 538's failing gate, re-measured from the two committed grids: 324/324 books matched, **max|d turn_yr| 9.1443e-03** (published 9.144e-03) = **4.5029e-04 relative on a level of 20.3094/yr**. **G3b** the queue's claim "B136/SMALL439 exactly 0" is **TRUE** (both 0.000e+00, n=108 each; the whole gap is U56).
- **G4** `rel == abs / level` identity 0 to 1e-15.

## The finding: the premise is right about that gate and wrong about the record
**G3c, the control the queue entry did not run.** On the SAME 324-row pair, every other
shared quantity: turnover's relative gap **4.50e-04** is the THIRD SMALLEST of 14 columns.
`H2` 1.16e-02, `oCAGR` 1.45e-02, `oSharpe` 1.12e-02 are 25-32x WORSE in relative terms.
The prices.csv vintage drift is not a turnover problem and not a level problem — turnover
merely has the largest *absolute* gap because it has the largest *level*.

**Why it cannot generalise (arithmetic, before any data).** `rel = abs / level`, so a
relative bound is LOOSER than an absolute one at the same number **iff level > 1**.
Median levels in this record: **TURNOVER 9.78** — and **CAGR 0.088, DD 0.206, GROSS 0.735,
VOL 0.130, SHARPE 0.887**. Turnover is the only class above 1. On the other four
"level-valued" classes the proposed re-gating is STRICTER, not looser.

**Priced on the cells where a bar form can bite.** 6,136 of 6,144 cells are near-identity
reproductions; **5,434 of those are bit-identical** and pass every bar under every form.
The live sub-population is the **702 DRIFT cells** (non-zero gap). At the record's own
working bar 1e-6:

| class | level | DRIFT cells | ABS pass | REL pass | recovered | newly caught |
|---|---|---|---|---|---|---|
| TURNOVER | 9.78 | 38 | 28 (73.7%) | 30 (78.9%) | **2** | 0 |
| GROSS | 0.73 | 47 | 47 (100%) | 47 (100%) | 0 | 0 |
| CAGR | 0.088 | 180 | 147 (81.7%) | 139 (77.2%) | 0 | **8** |
| DD | 0.206 | 151 | 139 (92.1%) | 114 (75.5%) | 0 | **25** |
| VOL | 0.130 | 0 | — | — | — | — |
| SHARPE (control) | 0.887 | 286 | 209 (73.1%) | 205 (71.7%) | 0 | 4 |

Across the LEVEL classes the swap **recovers 2 cells and newly fails 33**. The
discrimination leg is **UNDERPOWERED and reported as such**: only 8 DISTINCT (non-
reproduction) cells exist in the whole corpus, so the false-PASS columns carry no verdict.

**Census (Part A).** 426 numeric-bar asserts: **394 ABS, 6 REL, 7 EXACT, 19 SHAPE**. Only
**72 absolute bars (16.9%) sit on level-valued quantities** — TURNOVER 20, GROSS 20, CAGR 16,
DD 16 — against 102 on RETURNS and 13 on SHARPE; **192 (45.1%) could not be classified and
are reported unclassified, not imputed**. Extrapolating the measured DRIFT recovery rate
onto those counts puts **~1.1 clauses** on the other side of their bar. The record contains
**six** relative bars in total.

## Rule 8 (walk-forward), both legs
- **Bar leg** (the idea's own decision object): the bar calibrated on IS-window gaps only
  (`K=10 x` the 99th percentile), then read ONCE on the matching OOS-window gaps.
  **0 of 1,203 OOS decisions (NEAR) and 0 of 129 (DRIFT) differ between ABS and REL.**
  Once the bar is calibrated to the quantity at all, the FORM stops mattering entirely —
  which is the actionable reading of idea 538's failure: the defect was a hard-coded 1e-6,
  not the absence of a denominator.
  **Reported failure mode:** `IS_MaxDD->OOS_MaxDD` calibrates to `bar_abs = bar_rel = 0`
  (its IS gaps are bit-identical) and then fails 231/231 OOS cells under BOTH forms. A
  quantile-calibrated bar collapses to zero on a deterministic quantity.
- **Book leg** (PROTOCOL compliance): 27 books (3 panels x gross {0.50, 0.75, 1.00} x cadence
  {W, M, Q}), 4 IS-only selectors x 3 panels = 12 picks chosen on 2009-2016 and read ONCE on
  2017-01-01+. Picks OOS CAGR **2.95%-12.86%** / OOS Sharpe **0.6178-1.2840** / OOS MaxDD
  **-8.01% to -21.87%**, against RULES v2 OOS Sharpe **1.2834 (U56) / 1.1206 (B136) /
  0.5665 (SMALL439)** and SPY OOS **0.8721 / 0.8820** at OOS CAGR 15.24% / 15.45%.
  **4a 1/12, 4b 4/12. No book KEEP** — the 4b passes are U56/B136 gross-1.00 EWALL books the
  record has already published; nothing new.

## Verdict — KILL of the general proposal, KEEP of the narrow one. NOTHING APPLIED.
Do **not** re-gate the record's absolute bars on relative bounds: on four of the five
level-valued classes the swap is a tightening, and it buys 2 cells while newly failing 33.
The defensible narrow rule, **PROPOSED for a Sunday review, NOT APPLIED** (PROTOCOL.md,
RULES.md, scan.py, bot.py and baseline.py are untouched):

> **PROTOCOL 1 addendum (proposed).** A reproduction gate on a quantity whose typical level
> exceeds 1 — turnover, gross notional, any count or per-year rate — states its bar as a
> RELATIVE bound `max|a-b| / max(|a|,|b|) < tol`, and prints the level beside the gap. Bars
> on quantities of level <= 1 (returns, CAGR, drawdown, gross fraction, Sharpe) stay
> absolute. Either form, when the compared artefacts come from different `data/prices.csv`
> vintages, states the vintage allowance rather than silently taking it.

Under that wording idea 538's G1 turnover leg reads **4.5029e-04 relative on a level of
20.31**, and is a PASS against the 1e-3 relative bar the record's other vintage-drift
allowances already imply — while nothing else in the record moves.

## Caveats
Current-constituent survivorship in all three panels (see `data/SMALL_PANEL_README.md`).
Part B's corpus is the record's own artefacts, so its gap distribution inherits whatever
correlated mistakes the record contains; 45.1% of Part A's clauses are unclassified. The
8-cell DISTINCT control means this run cannot price the false-PASS side of the swap.

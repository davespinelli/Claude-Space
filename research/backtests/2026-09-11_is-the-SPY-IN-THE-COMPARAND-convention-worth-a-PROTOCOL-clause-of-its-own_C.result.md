# Idea 740 — is the SPY-IN-THE-COMPARAND convention worth a PROTOCOL clause of its own?

**Lane C, 2026-09-11.** Script `2026-09-11_is-the-SPY-IN-THE-COMPARAND-convention-worth-a-PROTOCOL-clause-of-its-own_C.py`.
10 bps, next-day execution, weekly cadence, band 0.03 — the live RULES v2 settings throughout.
Tuned parameters: **gross g** and **book form (v2band / v1rules)**. Nothing else is searched.

## Verdict: **ANSWERED — YES. The clause is worth writing, and the reason is not the size of the effect, it is that BOTH readings are in live use in the record's own source tree.** PROPOSED, not applied (rule 6).

## What the convention actually is

`load_universe()` returns SPY inside the frame, so `baseline.compare()`'s comparand holds SPY as an
**investable name**, not merely in the denominator:

| GATE | result |
|---|---|
| G1 `v2_weights(INCL)` == `baseline.rules_v2_weights` | max\|Δr\| **0.000e+00** PASS |
| G2 live RULES v2 U56 @10 bps | 8.61% / **1.1998** / −12.05% vs committed 8.66% / 1.2056 / −12.05% PASS — **vintage gap 0.0058 of Sharpe**, the identification bar for PART B |
| G3 SPY is a POSITION | mean **1.9275%** of the U56 book, held on **81.4%** of days PASS |
| G4 the three treatments are distinct books | max\|r_INCL−r_ZERO\| 1.277e-03, max\|r_ZERO−r_DROP\| 6.542e-04 PASS |

Idea 733's GATE G0a priced only the **denominator** half of this (N incl/excl SPY, 1e-4 of OOS Sharpe).
The whole convention is **~50× larger** than that on U56: **ΔOOS Sharpe +0.0088**.

## Size (PART A, 36 grid points, all reported in `.grid.csv` / `.deltas.csv`)

DROP − INCL on the comparand itself:

| panel | v2band ΔSharpe | v2band Δhalf (max) | v2band ΔMaxDD | v1rules ΔSharpe | v1rules ΔH2 | v1rules ΔMaxDD |
|---|---|---|---|---|---|---|
| U56 | **+0.0071** | +0.0088 | +0.16 pp | −0.0022 | +0.0096 | 0.00 pp |
| B136 | +0.0020 | +0.0022 | +0.06 pp | **−0.0239** | **−0.0544** | −0.34 pp |
| SMALL439 | **−0.0014** | −0.0016 | −0.02 pp | **+0.0381** | **+0.1219** | **+3.29 pp** |

**The sign flips by panel** — dropping SPY helps the U56/B136 v2 comparand and hurts the SMALL439 one.
So this is a convention, not an edge. The v1 comparand (the one ~3/4 of the record's canonical rows
quote) is **5–50× more exposed** than the v2 one.

**Resolvability** (`.resolvability.csv`): the gap exceeds the record's own 2 dp reporting bin (±0.005)
**and** the daily `prices.csv` vintage gap (0.0058) on **5 of 12** (panel × book × gross) cells — all
three v1 cells and all three U56 v2 cells. On the other 7 the convention is below the precision the
record prints.

**One committed-family 4b verdict is decided by it.** B136 v2band g1.00: the 4b CAGR floor is 10.660%;
INCL 10.7246% PASS, ZERO 10.6479% **FAIL by 0.012 pp**, DROP 10.7302% PASS. 1 of 12 cells flips 4b
between INCL and ZERO; **0 of 12 between INCL and DROP**.

## Which reading does the record run on? (PART B / B2)

**Not answerable from the LEADERBOARD, answerable from the source.**

- 1,334 of 5,292 leaderboard lines (25.2%) carry a canonically-formatted baseline triple. Identification
  at published 2 dp returns none 966 / ZERO 350 / INCL 8 / DROP 2 / ambiguous 8 — but **every one of
  those "unique" labels is a half-cent rounding artefact** (the 8 "INCL" rows sit on B136 v1's exact
  0.635 boundary), and the convention gap (0.0071) is only **1.2×** the vintage gap (0.0058). The
  record's printed precision cannot identify its own comparand. Idea 737's 1,079-row flip count is a
  count of *rounding-bin straddles*, not of identified rows.
- **The source census settles it.** 694 committed backtest scripts: 674 (97.1%) import `baseline`;
  **29 (4.2%) call `compare()` → INCL by construction**; **329 (47.4%) build a SPY-free frame → DROP**;
  7 do both in one file. Both readings are in active use, roughly half the corpus each way.

**Exposure of the published 4a column** (`.flips.csv`, every canonical row re-adjudicated against one
panel's comparand under INCL vs DROP — a sensitivity census; a row's own panel is not recoverable from
the table):

| comparand | U56 | B136 | SMALL439 |
|---|---|---|---|
| v2band g0.75 (live) | 0 flips | 2 | 6 |
| v1rules (pre-2026-09-06) | **22** | **43** | **74** |

i.e. **0–0.45% of the post-v2 record and 1.6–5.5% of the v1-era record**.

## Rule 8 walk-forward (PART C — g fixed on IS ≤ 2016 only, 2017–2026 read once)

| panel | treat | pick g | OOS CAGR | OOS Sharpe | OOS MaxDD | 4b OOS |
|---|---|---|---|---|---|---|
| U56 | INCL | 1.00 | 12.66% | 1.2740 | −15.91% | **PASS** |
| U56 | ZERO | 1.00 | 12.47% | 1.2828 | −15.43% | **PASS** |
| U56 | DROP | 1.00 | 12.70% | 1.2827 | −15.70% | **PASS** |
| B136 | INCL/ZERO/DROP | 1.00 | 10.58–10.66% | 1.1174–1.1195 | −15.96 to −16.16% | FAIL (CAGR floor) |
| SMALL439 | INCL/ZERO/DROP | 1.00 | 5.01–5.04% | 0.5657–0.5672 | −19.2% | FAIL (both halves) |

vs **RULES v2 OOS** 9.45% / 1.2747 / −12.05% (U56) and **SPY OOS** 15.24% / 0.8721 / −33.72%.
The pick is g = 1.00 under all three treatments on all three panels (IS Sharpe spread across the gross
ladder is 0.0011–0.0025, i.e. the selector is near-indifferent), |ΔOOS Sharpe| ≤ 0.0088, and **the OOS
4b verdict is identical under all three treatments everywhere**. The record's standing 4b candidate
(U56 band book at g = 1.00) is therefore **SPY-convention-invariant** — a robustness win it did not have
before.

## KEEP paths

- **4b:** 5 of 36 grid points pass (U56 g1.00 ×3 treatments, B136 g1.00 INCL and DROP). **No new
  candidate** — these are the standing 2026-09-04/09-11 family, reproduced, not discovered.
- **4a:** 8 of 36 pass, and **every one is an artefact of this convention**: U56 and B136 v2band at
  g ∈ {0.50, 0.75} under ZERO and DROP clear 4a against the INCL live comparand while being *the same
  book minus a 1.9% SPY sleeve*. Margins are +0.007 of Sharpe and +0.16 pp of MaxDD — **1.2× the
  data-vintage noise on the same statistic** — and the sign flips on SMALL439. **NOT PROMOTED, NO MEMO.**
  This is the sharpest argument for the clause: without a stated SPY convention, PROTOCOL 4a can be
  passed by re-framing the comparand instead of by building a book.

## PROPOSED PROTOCOL wording (rule 6: proposed, NOT applied)

> **Rule 3, added sentence:** *The comparand runs on the idea's own investable frame with SPY excluded
> from it; SPY appears only as the rule-4b benchmark. Any result quoting a comparand that holds SPY as
> a constituent must say so. Because `load_universe()` returns SPY in-frame, `baseline.compare()`
> currently implements the other reading — a 4a verdict whose margin is under 0.01 of Sharpe is not
> reportable until the two agree.*

## Caveats

SMALL439 is survivorship-biased (current constituents of the screen; 483 names minus the 44 with
`max_1d_move ≥ 1.0`) — reported, never promoted. `data/prices.csv` is re-downloaded daily, so the
absolute constants here sit 0.0058 of Sharpe below the committed ones; every Δ in this file is measured
within a single vintage and is exact within it.

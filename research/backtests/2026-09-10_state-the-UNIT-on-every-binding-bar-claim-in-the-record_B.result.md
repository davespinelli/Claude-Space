# Idea 480 — state the UNIT on every binding-bar claim in the record (lane B, 2026-09-10)

**VERDICT: ANSWERED / KILL of the queue's premise as posed. "Panel-noise units" is not one
unit — it is a null-construction choice, and changing only the null moves the binding bar on
34.1% of the record's own census rows, MORE than the 26.0% RAW-vs-NOISE disagreement the queue
was worried about. The queue's headline ("DD in panel-noise units, 47.6%") is a property of
idea 253's particular null AND of U56 alone. No KEEP, no memo, no RULES change.**
RULES.md, scan.py, bot.py, baseline.py and PROTOCOL.md untouched.

Script: `research/backtests/2026-09-10_state-the-UNIT-on-every-binding-bar-claim-in-the-record_B.py`
Artefacts: `.prose.csv .blocks.csv .rescored.csv .scales.csv .null.csv .grid.csv .truth.csv
.accuracy.csv .walkforward.csv .keeppaths.csv .console.txt`
Two tuned parameters and no more: **UNIT** ∈ {RAW, NOISE, IQR, RANK} and **PANEL** ∈ {U56,
B136, SMALL439}. Every grid point and every (UNIT × PANEL) cell is printed. Determinism was
checked by running the script twice in separate processes: byte-identical apart from the
runtime line.

---

## GATES (all passed before any new number was read)

| gate | result |
|---|---|
| G1 `fast_backtest` vs `engine.backtest`, U56 gross 0.75 | **1.041e-17** on the evaluation window and on all finite rows. `engine.backtest` returns NaN on 2 rows (its row-0 turnover is NaN because `w_target.shift(1)` is NaN there); both are 2008 warm-up and are dropped by every arm here |
| G2 live RULES v2, U56 @10 bps | CAGR 8.63% / Sharpe 1.2021 / MaxDD −12.05% |
| G3 idea 253's committed census re-read (25,153 rows, 238 files) | RAW modal **CAGR 0.670** (queue 0.672), NOISE modal **DD 0.474** (queue 0.476), disagreement **0.2604** (queue 0.261) — **the premise reproduces** |
| G4 the census's `z` is `m` ÷ a per-panel constant | max relative sd **2.756e-14**, so idea 253's scales are exactly recoverable from its own committed columns |

---

## PART A — the audit the queue asked for

644 committed `result.md`/`memo.md` files plus `CHANGELOG.md` yield **99 sentences naming
exactly one binding bar** (67 in result/memo over 53 files — idea 632, using the identical regex, reported 58 over 47 when
the corpus was **617** files rather than today's **644**, so the 9 extra claims are result files
committed since it ran — plus 32 in CHANGELOG.md, which idea 632 did not scan). Named bar: CAGR 41, DD 26, H2 12, H1 10, OOS 10.

Only **13 of 99** link to idea 253's census by run stem. Of those 13, **10 FLIP** between the
two units — nine of them RAW `CAGR` → NOISE `DD`. The prose agrees with its own run's RAW modal
bar **7/13** and with its NOISE modal bar **6/13**: *before any re-cut, the record's prose is
already only half-consistent with either column.* All 13 are listed per claim in `.console.txt`.

**The panel split is the first half of the kill.** On the census's own rows:

| panel | N | RAW modal | NOISE modal | disagree |
|---|---|---|---|---|
| U56 | 17,092 | CAGR 0.641 | **DD 0.505** | 0.2872 |
| B136 | 8,059 | CAGR 0.730 | **CAGR 0.538** | 0.2035 |
| SMALL | 2 | DD | DD | 0.0000 |

The queue's "DD in panel-noise units (47.6%)" is a **U56 statement**. U56 is 68% of the census;
on B136 the modal bar is CAGR under *both* units, and SMALL has two rows and no recoverable
scale at all. Panel — the queue's own second parameter — already breaks the headline.

## PART A2 — the unit itself is a construction choice, and that is the whole story

`binding = argmin_b m_b/sd_b`, and DD-vs-CAGR is the contest, so the entire result turns on one
number: `sd_null(DD)/sd_null(CAGR)`. Idea 253's null draws random **sub-panels at the panel's
own k**; this run's draws equal-weight **random half-panels inside the live 200d band**. Both
are defensible readings of "panel noise":

| panel | idea 253's null | this run's null | × |
|---|---|---|---|
| B136 | 2.107 | 1.226 | **1.72** |
| U56 | 2.244 | 1.026 | **2.19** |

Re-scoring **the record's own 25,153 rows** under this run's null instead:

| unit | modal shares |
|---|---|
| RAW (published `m`) | CAGR 0.670, DD 0.313, H1 0.014, H2 0.004 |
| NOISE, idea 253's null (the committed `z`) | **DD 0.474**, CAGR 0.417, H1 0.091, H2 0.017 |
| NOISE, this run's null | **CAGR 0.450**, H1 0.293, DD 0.171, H2 0.084 |

**34.11% of rows (8,579/25,153) change their binding bar when only the null changes** — larger
than the 26.04% RAW-vs-NOISE disagreement the queue raised as the problem. Per panel the
null-change flip is 0.3730 on U56 and 0.2735 on B136, and U56's noise-modal bar goes
**DD → H1**. There is no "the panel-noise reading" to compare RAW against.

## PART A3 — 96 committed five-margin blocks, and idea 150 by name

Idea 253's census reaches 238 files but only 13 prose claims. Reading the margins **directly**
reaches further: **96 committed CSVs carry a complete five-margin block with ≥8 rows —
370,102 rows.** Of these, **7 files (107,816 rows) cannot be converted to panel-noise units at
all**, because the panel is unstated or unmappable in the file. That is itself the answer to
"state the unit": the conversion needs a panel the file never printed.

Of the 91 convertible files, by modal binding bar: RAW **CAGR 45 / H2 25 / DD 20 / H1 1**;
NOISE-253 **CAGR 53 / DD 38**; NOISE-this-run **CAGR 67 / DD 23 / H1 1**. **37/91 (40.7%) flip
RAW → NOISE-253**, and **19/91 (20.9%) move again when only the null changes** (cell-level
median 0.186). Prose claims auditable this way rise from 13 to **19**, matching RAW 10/19,
NOISE-253 8/16, NOISE-this-run 10/16.

**Idea 150 — the claim the queue names first — fails its own title under every unit.** Its two
committed blocks (`.grid.csv` 67,108 rows and `.churn.csv` 29,198 rows, all three panels) are
modal **CAGR under RAW, under NOISE-253, and under NOISE-this-run** — never DD. This is not a
new contradiction so much as a confirmation of idea 150's *own body*, which already reports
"the DD cap is *not* the dominant cutter — the CAGR floor cuts more" (DD cap alone 32.5% vs
CAGR floor alone 39.2% of Sharpe-clearing exclusions). **The DD claim lives only in idea 150's
title, and the record's prose census reads titles.** Part of the record's DD-claim population
is a headline artefact, not a units artefact.

## PART B — deciding the unit by counterfactual, and why it cannot decide

A binding-bar claim is falsifiable: move the dial and watch which bar actually breaks first
(passers) or clears last (failures). 126 fresh grid points (3 panels × 3 dials: band, gross, n),
11 of them 4b passes, all in `.grid.csv`. 74 rows are scorable; 52 TIE and are excluded.

| subset | RAW | NOISE | IQR | RANK | N |
|---|---|---|---|---|---|
| all scorable | 0.892 | 0.919 | **0.932** | 0.054 | 74 |
| PASS regime (the census's regime) | **0.727** | 0.545 | 0.636 | 0.000 | 11 |
| FAIL regime | 0.921 | **0.984** | **0.984** | 0.063 | 63 |
| RAW and NOISE name different bars | 0.286 | 0.571 | **0.714** | 0.000 | **7** |

**This test is honestly underpowered, and the reason is structural.** The TRUE bar is `CAGR` in
**74 of 74** scorable rows, so a constant predictor that always says CAGR scores **1.000** —
above every unit. And 57 of the 74 rows have exactly one negative bar, where every positive
rescaling shares the argmin by construction. **Only 7 rows discriminate RAW from NOISE** (2 vs 4
correct). `RANK` is the one unambiguous result here: 0.054, *below* the 0.200 chance rate, and it
should not be used. Between RAW, NOISE and IQR this experiment ranks but cannot decide.

## PART C — RULE 8 (chosen on 2009–2016, 2017–2026 read once)

`sd_null` and the ground truth were recomputed on IS alone. IS accuracy: RAW 0.865, **NOISE
0.892**, IQR 0.892, RANK 0.054 → **the IS-chosen unit is NOISE**. Out of sample: RAW 0.851,
NOISE 0.878, **IQR 0.892**, RANK 0.041 — the IS choice is *not* the OOS best, which is the
expected price of choosing a unit on data.

Acting on the claim (defend the named bar: move the dial to the IS value buying it the most
slack, among IS 4b passers where any exist), then reading 2017–2026 once, mean over 9
panel × dial cells:

| unit | OOS Sharpe | Δ SPY | Δ RULES v2 | OOS CAGR | OOS MaxDD |
|---|---|---|---|---|---|
| RAW | **0.9107** | +0.0307 | −0.0778 | 8.83% | −18.79% |
| NOISE | 0.8836 | +0.0037 | −0.1048 | 8.63% | −18.57% |
| IQR | 0.8836 | +0.0037 | −0.1048 | 8.63% | −18.57% |
| RANK | 0.8818 | +0.0019 | −0.1066 | 8.39% | −18.21% |
| CONTROL (stay at c0) | 0.8688 | −0.0111 | −0.1196 | 7.10% | −16.19% |

Full sample and halves (PROTOCOL 4), mean over panels × dials; baselines are the mean over the
three panels:

| row | CAGR | Sharpe | MaxDD | H1 | H2 |
|---|---|---|---|---|---|
| RAW pick | 8.85% | 0.9198 | −18.79% | 1.017 | 0.833 |
| NOISE pick | 8.82% | 0.9086 | −18.57% | 1.019 | 0.810 |
| IQR pick | 8.82% | 0.9086 | −18.57% | 1.019 | 0.810 |
| RANK pick | 8.54% | 0.9024 | −18.21% | 1.007 | 0.809 |
| CONTROL pick | 6.85% | 0.8496 | −16.19% | 0.906 | 0.799 |
| **RULES v2 baseline (live)** | 6.83% | **0.9601** | **−12.99%** | 1.010 | **0.914** |
| RULES v1 (previous) | 6.73% | 0.6193 | −23.71% | 0.714 | 0.537 |
| SPY | **14.84%** | 0.8787 | −33.72% | 0.935 | 0.839 |

Per panel, OOS 2017–2026 (mean over dials × units): U56 pick 1.1413 vs RULES v2 1.2788 vs SPY
0.8758 (CAGR 10.78% / 9.48% / 15.32%; MaxDD −14.33% / −12.05% / −33.72%); B136 0.9845 / 1.1185 /
0.8820 (9.27% / 7.98% / 15.45%; −16.96% / −12.24% / −33.72%); SMALL439 0.5314 / 0.5680 / 0.8820
(4.90% / 3.85% / 15.45%; −22.91% / −14.68% / −33.72%).

**Every unit's pick loses to the live RULES v2 book out of sample on all three panels**, and the
best-to-worst spread across units is +0.029 OOS Sharpe against a −0.08 to −0.11 gap to the live
book that all of them concede. All four beat the CONTROL, so *acting on a binding-bar claim at
all* is worth more (+0.013 to +0.042 OOS Sharpe, +1.3 to +1.7 pp OOS CAGR) than *which unit you
read it in* — bought with 2.0–2.6 pp of extra drawdown.

## KEEP paths — both, on every grid point

126 grid points: **4b 11** (B136 5/42, U56 6/42, SMALL439 0/42), **4a 23** (B136 10, U56 11,
SMALL439 2), **BOTH 0**. Every 4b passer is a point on an already-committed gross/band/n ladder
on the record's own panels. **No KEEP is claimed and no memo is written.**

## What this changes

Nothing in RULES, and nothing written into PROTOCOL by this run. Three things the record should
carry, offered for the Sunday review rather than adopted here:

1. `m_bind` published without its **null** is not reproducible. Idea 632 asked for the
   normaliser to be named; this run shows that is not enough — two defensible nulls move 34.1%
   of the record's own rows. A file publishing a noise-unit binding bar must publish the null.
2. A file publishing a five-margin block must publish its **panel**. 7 of 96 blocks (107,816
   rows) cannot be converted at all for want of it.
3. The record's `DD binds` prose population is partly a **title** artefact. Idea 150's title
   says DD; its body and all three units say CAGR.

**Survivorship caveat (PROTOCOL 9):** U56, B136 and SMALL439 are current-constituent lists, and
SMALL439 additionally drops `data/small_meta.csv max_1d_move >= 1.0` (idea 118, a terminal-dated
screen per idea 627). Absolute CAGR/Sharpe/MaxDD levels above are biased upward and none is a
tradable estimate. The findings meant to survive that bias are the within-panel contrasts —
which bar is the argmin, and RAW vs NOISE vs null — because both readings are taken off the
*identical* books, so the bias is common to them. Idea 38 (u56/broad calendar-day index) and
idea 126 (t+1 only, no lag band) also apply.

Follow-ups queued: 652, 653, 654.

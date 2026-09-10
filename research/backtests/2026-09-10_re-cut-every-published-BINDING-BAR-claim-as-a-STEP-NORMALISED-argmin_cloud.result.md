# Idea 632 — re-cut every published BINDING-BAR claim as a step-normalised argmin

**Run:** 2026-09-10, cloud. **Verdict: ANSWERED / KILL for the raw `m_bind` column as a
publishable claim. No KEEP, no RULES change.** RULES.md, scan.py, bot.py, baseline.py and
PROTOCOL.md untouched.

Script: `research/backtests/2026-09-10_re-cut-every-published-BINDING-BAR-claim-as-a-STEP-NORMALISED-argmin_cloud.py`
Artefacts: `.files.csv .g0.csv .census.csv .cells.csv .summary.csv .prose.csv .prose_linked.csv
.grid.csv .density.csv .densitysummary.csv .walkforward.csv .keeppaths.csv .console.txt`

Two tuned parameters and no more: **NORM** ∈ {RAW, SD, IQR, RANK, SENS} and **CLAIMSET** ∈
{ALL, PASS4b, FAIL4b}. Every grid point is written out.

---

## Answer

**44% of the record's binding-bar claims do not survive a unit-free re-read, and the record's
entire `H2 binds` family (28 of 81 claims) is an artefact of taking a minimum across three
different units.**

PART A. 83 committed `research/backtests/*.csv` file×family blocks carry the complete five-margin
set (`m_H1, m_H2, m_OOS` in **Sharpe** units; `m_DD` in **MaxDD fraction**; `m_CAGR` in **CAGR
fraction**); 81 of them have ≥8 rows and so state a claim — **105,504 cells**. G0: where a file
publishes a bind-shaped column of its own, 12 of 14 columns reproduce the raw argmin *exactly*,
so "the published claim is the raw argmin" is established, not assumed.

PART B, cell level and claim level (a claim survives if the file's **modal** binding bar is
unchanged):

| CLAIMSET | claims | cells | SD cell / claim | IQR cell / claim | RANK cell / claim |
|---|---|---|---|---|---|
| ALL | 81 | 105,504 | 0.722 / **0.568** | 0.695 / 0.556 | 0.546 / 0.259 |
| PASS4b | 72 | 36,199 | 0.773 / **0.833** | 0.759 / 0.556 | 0.472 / 0.417 |
| FAIL4b | 80 | 69,295 | 0.704 / 0.537 | 0.669 / 0.512 | 0.562 / 0.350 |

The published modal bar, and what it becomes:

| modal bar | RAW (published) | SD | IQR | RANK |
|---|---|---|---|---|
| CAGR | 32 | 36 | 36 | 14 |
| **H2** | **28** | **0** | **1** | **0** |
| DD | 17 | 41 | 42 | 65 |
| H1 | 4 | 4 | 2 | 2 |

`H2` is the reading that dies: 28 → 0. It is the smallest-dispersion Sharpe bar, so it wins a
raw min it would never win in noise units. The bar the record *should* be naming is `DD`
(17 → 41). The 4b-passing subset is the sturdiest claim set (0.833 survival) — the claims that
matter for capital move least — and `FAIL4b` is the weakest (0.537), which is the wrong way
round for a record that uses `m_bind` mostly to explain failures.

PART C. 617 committed result/memo files yield **58 sentences naming exactly one binding bar**
across 47 files (CAGR 24, DD 21, H1 6, H2 4, OOS 3). Only 12 of those files also commit a
five-margin block in the same run; on those 16 linked (prose, file) pairs the prose bar matches
its own file's modal bar **7/16 under RAW** — i.e. the prose is already only half-consistent with
the column it is describing, before any re-cut — and 7/16 under SD/IQR, 4/16 under RANK.

**The record contains its own precedent.** `2026-09-09_does-a-random-sub-panel-pass-4b-because-
the-CAGR-floor-moves_B.census.csv` publishes both `binding` (z-normalised) and `binding_raw`
(25,153 rows). They disagree on **26.0%** of rows and flip the headline: raw modal `CAGR`
(16,845/25,153) vs z-normalised modal `DD` (11,920/25,153).

---

## A correction to idea 408R's framing

Idea 408R found `steps` is not density-free (median x4/x1 ratio 2.089, `inf` on 22% of cells)
and recommended `margin/|dm/dc|`. **That defect does not reach the binding-bar claim.** Dividing
all five bars by the same one-step motion `h` is a common positive factor, and a common positive
factor cannot move an argmin (gate G3: 500/500 random rows). So `margin/step` and
`margin/|dm/dc|` name the **same** bar at a given density; they differ only in the number
printed beside it. Idea 408's 41.3% disagreement is a **unit** effect, not a density effect.

PART D confirms this on a fresh grid whose spacing this file controls (3 panels × 3 dials ×
2 densities = 351 points, all in `.grid.csv`). Density-invariance of the argmin, on the 120 dial
values published at both x1 and x2 spacing:

| NORM | density-invariant | agreement with RAW argmin |
|---|---|---|
| RAW | 1.0000 (by construction) | — |
| IQR | 1.0000 | 0.650 |
| SD | 0.9500 | 0.655 |
| RANK | 0.9500 | 0.265 |
| SENS `m/|dm/dc|` | 0.8500 (finite-difference error only) | 0.641 |

The density channel is worth ≤15% of points; the **unit** channel is worth 35%. `SD` and `IQR`
carry a second, smaller defect nobody has priced: they depend on **which points the publisher
chose to print** (5% of points move when the same dial value is published on a finer grid).
`IQR` is the only normaliser that is both unit-free and exactly density-invariant here.

---

## PART E — rule 8 (choose on 2008–2016, evaluate 2017–2026 untouched), both KEEP paths

The normaliser changes the rule-8 pick in **18 of 18** (panel × dial × density) cells — every
one. It barely changes the answer. Mean over 90 picks:

| NORM | OOS Sharpe | Δ vs RULES v2 | Δ vs SPY | OOS CAGR | OOS MaxDD | 4b | 4a |
|---|---|---|---|---|---|---|---|
| RAW | 0.8661 | −0.1254 | −0.0138 | 0.1062 | −0.2669 | 0.222 | 0.000 |
| SD | 0.8707 | −0.1208 | −0.0092 | 0.1046 | −0.2515 | 0.222 | 0.000 |
| IQR | 0.8730 | −0.1186 | −0.0070 | 0.1076 | −0.2835 | 0.222 | 0.000 |
| RANK | 0.8739 | −0.1177 | −0.0061 | 0.0984 | −0.2706 | 0.000 | 0.000 |
| SENS | **0.8854** | −0.1061 | **+0.0055** | 0.0917 | −0.1762 | 0.222 | 0.056 |

Best-to-worst spread is **+0.019 OOS Sharpe** (SENS over RAW) — real in sign, and the only
normaliser whose picks beat SPY out of sample on average, but a fifth of the −0.11 to −0.13 gap
to the live RULES v2 book that all five picks concede. Per panel, OOS 2017–2026, mean over
dials × densities × normalisers:

| panel | pick Sharpe | RULES v2 | SPY | pick CAGR | v2 CAGR | SPY CAGR | pick MaxDD | v2 MaxDD | SPY MaxDD |
|---|---|---|---|---|---|---|---|---|---|
| U56 | 1.1290 | 1.2876 | 0.8758 | 14.17% | 9.51% | 15.32% | −19.62% | −11.90% | −33.72% |
| B136 | 0.9719 | 1.1206 | 0.8820 | 12.00% | 7.98% | 15.45% | −23.77% | −12.18% | −33.72% |
| SMALL439 | 0.5206 | 0.5665 | 0.8820 | 4.34% | 3.84% | 15.45% | −31.52% | −14.70% | −33.72% |

Both KEEP paths over all 351 fresh grid points: **32 pass 4b** (all on the `gross` dial — U56 18,
B136 14; the ladder idea 585 already owns), **5 pass 4a** (SMALL439 `band`). Of the 90 rule-8
picks, 16 pass 4b and **1** passes 4a. **No KEEP is claimed**: every 4b passer here is an
already-committed gross-ladder point, and every rule-8 pick loses to the live RULES v2 book out
of sample on all three panels.

---

## What this changes

Nothing in RULES. One reporting habit, proposed and **not** written into PROTOCOL by this run:
a file that publishes `m_bind` should publish the **normaliser** beside it, and `IQR` is the one
that is both unit-free and density-invariant on this evidence. The 28 committed `H2 binds`
claims should be read as "no bar binds in noise units" rather than as an H2 result.

**Survivorship caveat (PROTOCOL 9):** B136 and SMALL439 are *current* constituent lists —
delisted, acquired and screened-out names are absent, so their absolute CAGR/Sharpe levels are
biased upward and none of the level numbers above is a tradable estimate. SMALL439 additionally
drops the 44 names with `data/small_meta.csv max_1d_move >= 1.0`. Only the within-panel
contrasts (which bar is the argmin, and the RAW-vs-normalised comparison) are meant to survive
that bias, since both readings are taken on the identical books.

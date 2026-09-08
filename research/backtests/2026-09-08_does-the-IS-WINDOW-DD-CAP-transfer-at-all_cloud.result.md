# Idea 420 — does the IS-window DD cap transfer at all?  (cloud, 2026-09-08)

**ANSWERED, and the queue's premise is FALSIFIED. The IS drawdown slope is NOT ~0: it is
+0.918 (t +8.19), statistically indistinguishable in size from the CAGR slope (+0.902) and
nearly twice the Sharpe slope (+0.508). The IS-window DD cap should NOT be dropped from IS
screens. What IS broken is its LEVEL, not its ranking: 96.2% of arms draw down deeper out of
sample, by a mean 7.64 pp and a ratio of 1.49x — idea 128's window bias made concrete, and
it is a calibration fault with a stated fix. Rules unchanged; one KEEP-candidate by-product
memo written (not adopted). RULES.md, scan.py, bot.py, baseline.py untouched.**

Census: every `research/backtests/*.csv` carrying, per arm, a matched (IS_M, OOS_M) pair.
**1,539 files scanned → 67 ADMITTED** (1,118 no arm column, 270 no matched pair, 84 no usable
cell); **29,365 arm-rows over 3,158 cells and 67 files**, 8 panel labels, 13 cost rungs.
Cells discovered mechanically (a column is a cell label only if it is not a metric/mask
column, has 2–40 values and is *not* functionally determined by the arm); ledger committed.
Two tuned parameters — metric M ∈ {MaxDD, CAGR, Sharpe} × transform ∈ {demeaned level,
within-cell rank, top-quartile hit} — **all 9 grid points reported**, SEs clustered by
parent file.

## 1. The transfer, within cell (the queue's own test)

| M | n | cells | slope | R² | t (file-clustered) | mean within-cell rho | P(OOS top-Q \| IS top-Q) |
|---|---|---|---|---|---|---|---|
| **MaxDD** | 19,401 | 2,241 | **+0.918** | 0.412 | +8.19 | +0.429 (83.7% of cells > 0) | **0.580** (base 0.25, z +40.5) |
| CAGR | 20,697 | 2,330 | +0.902 | 0.707 | +31.73 | +0.668 | 0.588 |
| Sharpe | 28,316 | 3,036 | +0.508 | 0.365 | +8.52 | +0.396 | **0.334** |

**The DD bar transfers as well as the CAGR bar and better than Sharpe on the quartile test
(0.580 vs 0.334).** The record's incumbent rule-8 selector is IS-Sharpe — the *least*
transferable of the three by this measurement.

## 2. The real fault is LEVEL, not order

| M | mean OOS − IS | share of arms worse OOS | mean \|OOS\| / mean \|IS\| |
|---|---|---|---|
| **MaxDD** | **−7.64 pp** | **96.2%** | **1.49x** |
| CAGR | +1.06 pp | 35.6% | 1.09x |
| Sharpe | +0.015 | 46.4% | 1.01x |

An IS drawdown cap set at the level you want out of sample is therefore wrong by about half
again, in one direction, on 96% of arms; the same window is unbiased in CAGR and Sharpe.
The fresh grid reproduces it independently: shift −5.85 pp, **100.0%** of arms worse,
ratio **1.63x**, slope **+1.49**.

## 3. Where it fails, it fails by panel — not by cost rung

Per panel, MaxDD slope: broad **+1.085** (t +7.23), B136 +0.399 (t +1.68), SMALL439 +0.354
(t +1.07, ns), **U56 +0.051 (t +0.45, ns; quartile hit 0.316)**. Per rung it is stable
(+1.064 @10 bps, +1.004 @25, +1.228 @0). **On U56 the IS drawdown ranking carries no
information; on broad it carries slope ~1.** Every split is in `.transfer.csv`.

## 4. RULE 8 — the slopes are pre-registrable

Fit on the record's first half by parent-file date (33 files / 12,295 arm-rows, < 2026-09-06),
read the second half untouched (34 files / 17,070 rows):

| M | IS slope (R²) | OOS slope (R²) | IS rho → OOS rho |
|---|---|---|---|
| MaxDD | +0.900 (0.377) | **+0.925 (0.426)** | +0.393 → +0.469 |
| CAGR | +0.864 (0.612) | +0.914 (0.739) | +0.603 → +0.736 |
| Sharpe | +0.484 (0.326) | +0.517 (0.382) | +0.368 → +0.419 |

Every slope is **higher** out of sample. Nothing here is an in-sample artefact.

## 5. The decision, priced on real prices (fresh 31-arm menu, 6 cells, 186 arm-rows)

u56 / broad136 / SMALL439 × 10 and 25 bps; IS through 2016-12-31, OOS 2017-01-01.. read once.
Screen = idea 163's S1 shape on the IS window (IS H1 and H2 Sharpe > SPY's IS halves, IS
CAGR ≥ 70% of SPY's), **WITH** its DD leg (IS MaxDD ≥ 60% of SPY's IS MaxDD) vs **NO-DD**.

The DD leg changes the pick in **2 of 6 cells** and empties the pool in **2 of 6** (both
SMALL439). Where it changes the pick (broad136 @10 and @25) it buys **+16.6 pp of OOS
drawdown** for **−7.5 pp of OOS CAGR** and +0.05 / +0.03 OOS Sharpe; pooled over all six
cells, **+5.54 pp OOS MaxDD, −2.52 pp OOS CAGR, +0.0135 OOS Sharpe**. It is a real
instrument with a real price, not an inert clause.

Levels (freshly computed, OOS 2017-01-01..2026-09-04): SPY **15.45% / 0.8820 / −33.72%**
(4b OOS bars 10.82% and −20.23%); RULES v2 @10 bps u56 **9.53% / 1.2851 / −12.05%**,
broad136 7.98% / 1.1185 / −12.24%, SMALL439 3.85% / 0.5680 / −14.68%.
KEEP paths over the fresh grid: @10 bps 4a(v2) 8/93, 4b 13/93, 4b(OOS) 11/93, **BOTH 0/93**;
@25 bps 3 / 9 / 9 / **0**. SMALL439 admits **0 of 62** on 4b at every rung.
SURVIVORSHIP: the small panel and `universe_broad.json` are current constituents only
(data/SMALL_PANEL_README.md) — read the contrasts, not the levels.

**By-product (KEEP-candidate, path 4b, NOT adopted):** the screened pick on u56 is
`EW all names above the 200d MA, full gross, monthly` — full sample **11.96% / 1.2126 /
−15.49%** (H1 1.249 / H2 1.179), OOS **12.72% / 1.2750 / −15.49%** at 10 bps and
12.37% / 1.2434 / −15.54% at 25 bps; it clears 4b on the full sample and on the OOS window
at both rungs and fails 4a against RULES v2. It is a **plateau, not a point**: all 8
gross-1.00 arms on u56@10 clear 4b across bands 0–6% and both cadences. Memo with exact
RULES wording: `2026-09-08_u56-ewall-magate-fullgross_KEEP_MEMO.md`. Sunday review decides.

## What this changes

PROTOCOL's IS-window DD cap is **enforceable and should stay** — the queue's proposed
deletion is refused by its own test. The correction the record needs instead is a
**calibration constant**: an IS drawdown bar is optimistic by ~1.5x, so either state IS DD
caps as within-cell ranks, or scale an absolute IS cap by ~1.5 before reading it as an OOS
promise. Idea 163's "screened arms draw down 3.30 pp deeper" is consistent with this and is
not evidence of non-transfer: the *ranking* transfers, the *level* does not — and 163 itself
attributed 95.3% of that number to empty-pool fallback.

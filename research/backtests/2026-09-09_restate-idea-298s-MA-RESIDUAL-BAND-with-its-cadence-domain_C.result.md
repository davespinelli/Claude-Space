# Idea 551 — restate idea 298's MA-RESIDUAL BAND with its cadence domain (lane C, 2026-09-09)

**ANSWERED / KILL of the queue's premise, and the audit comes back clean.**
The band `[-0.70, -0.20]` pp/yr is **not** a W/M/Q fact that collapses at both ends. That is a
**SMALL439** fact at the daily end. On the two large panels the DAILY mean is comfortably
**inside** the band (U56 **-0.2636**, B136 **-0.3776**). What is panel-general is the **ANNUAL**
break, on all three. The correct stamp is **"not annual"**, not "W/M/Q". And no committed result
changes verdict: 5 uses of the band, 4 of them inside the domain on every panel, 1 flip which is
idea 307 itself — the file that published the restriction. **0 uncorrected verdict changes.**

Script: `research/backtests/2026-09-09_restate-idea-298s-MA-RESIDUAL-BAND-with-its-cadence-domain_C.py`
540 books = 3 panels × 9 thetas × 5 cadences × 2 families × 2 constructions, 135 decomposition
cells. Gross 0.75, 10 bps, next-day execution, no shorting, no leverage; the 0-bps rung every
residual uses is derived exactly (`r0 = r10 + turnover*bps/1e4`), not re-run. Ten of the fifteen
(panel × cadence) cells this question needs had never been run: idea 307 measured the cadence
profile on SMALL439 only, while idea 298 fitted the band on three panels.

---

## Gates first (asserted and printed before any headline number)

| gate | bar | result |
|---|---|---|
| G0.1 local cadence-extended runner == `engine.backtest` at D/W/M/Q, every panel | < 1e-15 | **PASS, 0.000e+00** over 12 probes, 0 mask-disagreement bars |
| G0.2 idea 298's `.decomp.csv` MA resid0, 3 panels × W/M/Q | < 1e-6 pp/yr | **FAIL at the bar, 5.523e-03** — see below |
| G0.3 idea 307's `.decomp.csv` MA resid0, SMALL439 × 5 cadences | < 1e-6 pp/yr | **PASS, 8.327e-17** (45/45 cells) |
| G0.4 identity `r_dg,t == c_t * r_rs,t` at 0 bps, every cadence, every panel | < 1e-12 | **PASS, 6.731e-16** |
| G0.5 \|d mask fraction (QUANTILE-M − MA)\| at all 9 thetas × 3 panels | < 0.01 | **FAIL at the bar, 0.01396** — see below |
| G0.6 LIVE RULES v2 U56 weekly 10 bps | 8.66% / 1.2056 / -12.05% at 5e-4 | **FAIL at the bar**: 8.64% / **1.2037** / -12.05% |

Both G0.2 and G0.6 fail for the **same reason, and it is not this script**: `data/prices.csv`
is refreshed daily and now ends **2026-09-08**, while `data/prices_broad.csv` and
`data/prices_small.csv.gz` are cached Fridays and end **2026-09-04** (idea 514's vintage split).
The evidence is exact: idea 298's 81 MA cells reproduce to **2.220e-14 on B136 and 2.220e-14 on
SMALL439** — machine precision — and the entire 5.5e-03 discrepancy is **U56-only** (mean
8.0e-04, worst U56/θ=+0.30/M), the one panel whose cache moved. `c_bar` matches to 2.5e-05
everywhere. The drift is 0.6% of the band's half-width and cannot touch any verdict here; the
1e-6 bar is a restatement bar being asked to absorb three extra trading days.

G0.5's failures are **U56-only and mechanical**: 3 of 9 thetas, worst 0.01396, and every one is
below **1/n = 0.0182** — the `ceil(x·n_t)` granularity floor on a 55-name panel. B136 (max
0.0044, 1/n 0.0074) and SMALL439 (max 0.0017), where idea 307 asserted this gate, pass
comfortably. It bounds the **QUANTILE-M control column on U56 only**; the MA-THRESH headline
does not use the matching at all.

---

## (1) THE HEADLINE — the band is a NOT-ANNUAL fact, not a W/M/Q fact

MA-THRESH mean resid0 (pp/yr, FULL sample, 9 thetas per cell). `in band` is against the
published `[-0.70, -0.20]`.

| panel | D | W | M | Q | A |
|---|---|---|---|---|---|
| **U56** | **-0.2636 ✓** | -0.4439 ✓ | -0.2957 ✓ | -0.2728 ✓ | **+0.0727 ✗** |
| **B136** | **-0.3776 ✓** | -0.4688 ✓ | -0.3723 ✓ | -0.4284 ✓ | **-0.0843 ✗** |
| **SMALL439** | **-0.0904 ✗** | -0.2164 ✓ | -0.2416 ✓ | -0.6871 ✓ | **-0.1078 ✗** |

**H_DOMAIN** (pre-registered: inside in all 9 interior cells AND outside in all 6 extreme cells)
— clause (1) **PASS 9/9**, clause (2) **FAIL 4/6**. **H_DOMAIN FAILS.**
**H_ONE_PANEL** (pre-registered rival: at least one large panel has its D or A mean inside)
— **HOLDS, 2/4.** The daily collapse is SMALL439's alone.

The "largest in the middle of the dial" shape is also SMALL439's alone. On SMALL439 the profile
peaks at Q (**-0.6871**, 2.5× its own W). On U56 it peaks at **W** (-0.4439) and Q is the
*shallowest* interior cell (-0.2728); on B136 it peaks at W too (-0.4688). Three panels, three
different interior shapes, one shared fact: **A is outside the band everywhere.**

**The mechanism, and why A is the real boundary.** The matched QUANTILE-M control (constant
depth, same ranking, same mean exposure) says the cadence effect is the MA gate's, not the
decomposition's — its own residual is ≈0 at D on all three panels (-0.0030 / -0.0003 / -0.0006)
and grows only to -0.04 by Q. The separation MA − QUANTILE:

| panel | D | W | M | Q | A |
|---|---|---|---|---|---|
| U56 | -0.2606 | -0.4325 | -0.2562 | -0.2306 | **+0.0539** |
| B136 | -0.3773 | -0.4573 | -0.3317 | -0.3842 | **-0.0456** |
| SMALL439 | -0.0897 | -0.2070 | -0.2025 | -0.6985 | **+0.0162** |

At ANNUAL the MA gate's residual is **indistinguishable from a pure-exposure gate's** on every
panel — the sign even flips on two. That is the finding that generalises, and it is the same
place idea 307 found the QUANTILE control stops discriminating.

## (2) THE BAR DIAL — the published band is a band on the MEAN, not a coverage interval

In-band share of the 9 individual thetas, by cadence, at half-width multiples m around the
published centre -0.45 (m = 1.0 **is** `[-0.70, -0.20]`), pooled over the three panels:

| m | band | D | W | M | Q | A |
|---|---|---|---|---|---|---|
| 0.50 | [-0.575, -0.325] | 0.333 | 0.259 | 0.370 | 0.333 | 0.000 |
| 0.75 | [-0.637, -0.262] | 0.444 | 0.296 | 0.481 | 0.481 | 0.000 |
| **1.00** | **[-0.700, -0.200]** | **0.481** | **0.481** | **0.556** | **0.519** | **0.074** |
| 1.50 | [-0.825, -0.075] | 0.778 | 0.815 | 0.778 | 0.630 | 0.630 |
| 2.00 | [-0.950, +0.050] | 0.926 | 0.926 | 1.000 | 0.889 | 0.852 |

At the published width barely half the cells sit inside at *any* cadence, and 7% at A; you need
**m = 2.0** for 85-100%. Anyone quoting `[-0.70, -0.20]` as a cell-level expectation is quoting
a 50% interval. It is a bar on a 9-theta mean and should only ever be read as one.

## (3) THE AUDIT — 5 uses, 1 flip, 0 uncorrected

Census rule, pre-registered: BAR = the literal `-0.70`/`-0.20` pair inside a `.py`;
PRIOR = the prescription in prose ("0.3–0.6 pp/yr", "level-independent lump", "lump of -0.38").
Ledgers (QUEUE / LEADERBOARD / CHANGELOG) excluded — they restate, they do not use. Each use's
cadence domain read from its own `CADENCES = [...]`. **Measured domain of the band (inside on
all three panels): W, M, Q.**

| use | role | cadences | pooled resid0 | pooled reading | per-cadence reading | flips |
|---|---|---|---|---|---|---|
| 300 `does-a-pure-exposure-gate-exist-on-the-small-panel_C` | **BAR** (`BAR_MA_RESID`) | W,M,Q | -0.3808 | PASS | PASS | no |
| 298 `does-the-cash-drag-share-depend-on-the-panel-or-on-the-gate-level_cloud` | PRIOR | W,M,Q | -0.3808 | PASS | PASS | no |
| 302 `is-the-negative-exposure-timing-residual-a-general-property-of-gates_B` | PRIOR | W,M,Q | -0.3808 | PASS | PASS | no |
| 307 `does-the-QUANTILE-zero-residual-hold-at-DAILY-and-ANNUAL-cadence_B` | PRIOR | D,W,M,Q,A | -0.2852 | PASS | **FAIL** | **yes** |
| `is-the-gate-timing-residual-a-constant-in-pp-per-year_B` | PRIOR | W,M,Q | -0.3808 | PASS | PASS | no |

**1 flip of 5**, and it is idea 307 — the file that *found* the break and already states the
restriction in its own committed result. **Uncorrected flips: 0.** H_AUDIT as literally
pre-registered (flip count == 0) **FAILS**; the substantive answer the queue asked for is
**no committed result changes verdict.** The band was used, four times out of five, exactly
inside the domain it turns out to have.

The 307 row also demonstrates the hazard in one number: pooling resid0 across D..A gives
**-0.2852, which PASSES the band**, while the per-cadence reading fails at D (SMALL439) and at A
(everywhere). A pooled-across-cadence mean can clear a bar that none of its own extreme cells
clears.

## (4) RULE 8 — the cadence stamp is bookkeeping, not a better predictor

**WF-A** (θ, cadence chosen on IS Sharpe 2009/11–2016, OOS 2017–2026 read once, 12 arms):
beats SPY **8/12**, beats LIVE RULES v2 **0/12**, beats its own cadence-matched no-gate control
**2/12**. Best OOS Sharpe 1.1384 (B136 MA/DEGROSS θ=-0.25 Q) against RULES v2 OOS **1.2817** and
SPY OOS 0.879/0.882.

**WF-B** — fit the band on IS only, unqualified (one band for the dial) vs qualified (one per
cadence), score OOS untouched:

| cad | qualified IS band | cov unqual | cov qual | cov published | MAE unqual | MAE qual | MAE zero |
|---|---|---|---|---|---|---|---|
| D | [-1.049, +0.506] | 1.000 | 1.000 | 0.407 | 0.2160 | 0.2224 | 0.2485 |
| W | [-1.116, +0.553] | 0.926 | 0.963 | 0.630 | 0.2602 | 0.2449 | 0.4351 |
| M | [-0.713, +0.530] | 0.963 | 0.741 | 0.407 | 0.3049 | 0.3728 | 0.4489 |
| Q | [-0.787, +0.287] | 0.704 | 0.630 | 0.333 | 0.4616 | 0.4564 | 0.5868 |
| A | [-1.046, +0.497] | 0.889 | 0.889 | 0.111 | 0.3451 | 0.3804 | **0.2302** |

The cadence-qualified band beats the unqualified one on OOS MAE in only **2/5** cadences, and a
hard **ZERO** beats it at A. The published band's own OOS coverage is 33-63% at W/M/Q and
**11% at A**. So: stamp the domain because the A cells are wrong without it, but do not expect
the stamp to buy accuracy.

**WF-C** — H_DOMAIN re-read one window at a time: IS **6/9 interior inside, 3/6 extremes
outside**; OOS **8/9 and 5/6**. The domain claim holds in **neither** window on its own. It is a
full-sample pooled statement about a 9-theta mean, and it should be quoted that way.

## (5) Both KEEP paths, all 540 books

**4a 1/540, 4b 19/540, BOTH 0/540.** By panel: U56 1 / 17, B136 0 / 2, SMALL439 0 / 0.
By cadence (4b): D 3, W 8, M 7, Q 0, A 1. 4b failing legs: DD 370, CAGR 282, OOS 218, H2 215,
H1 210. The single 4a passer is **QUANTILE-M / DEGROSS, U56, θ=+0.06, M** (7.02% / 1.2364 /
-9.20%, halves 1.3010 / 1.1905, OOS 1.2603) — the constant-depth twin, the same cell idea 306
found, **not** the MA form the band describes. No KEEP candidate, no memo, no RULES change.

**SURVIVORSHIP:** SMALL439 and B136 are current constituents of their screens — no delistings —
so every CAGR level and the whole 4a/4b column are inflated. The headline is arm-minus-arm on
the same names, ranking and days, so the bias very largely cancels out of resid0.

---

## What the record should carry forward

1. Quote the band as **`[-0.70, -0.20]` pp/yr, MA-THRESH gate, D through Q on U56/B136, W
   through Q on SMALL439, and NOT at annual cadence** — a mean over 9 thetas, not a cell-level
   expectation (only ~50% of cells sit inside at the published width).
2. The one panel-general cadence fact is that **the MA gate stops being distinguishable from a
   pure-exposure gate at annual cadence** (separation -0.046 / +0.016 / +0.054 pp/yr, sign
   flipped on two panels).
3. **No published verdict is retracted.** Idea 300's `BAR_MA_RESID` gate and the three prose
   priors all ran at W/M/Q and all still pass, per cadence as well as pooled.
4. Never pool a residual across the cadence dial before applying a bar to it: -0.2852 pooled
   D..A clears a band that its own D and A cells do not.

Outputs: `.grid.csv` (540 books) `.decomp.csv` (405 window-cells) `.band.csv` `.census.csv`
`.walkforward.csv` `.console.txt`.

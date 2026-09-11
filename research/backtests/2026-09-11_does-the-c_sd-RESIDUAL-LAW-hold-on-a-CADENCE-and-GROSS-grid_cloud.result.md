# Idea 539 — does the c_sd RESIDUAL LAW hold on a CADENCE and GROSS grid?

**Lane:** cloud · **Date:** 2026-09-11 · **Script:** `2026-09-11_does-the-c_sd-RESIDUAL-LAW-hold-on-a-CADENCE-and-GROSS-grid_cloud.py`

> **FILED AS AN INDEPENDENT REPLICATION (320R / 536R precedent), NOT A SECOND CLAIM.**
> Lane B worked idea 539 the same day without sight of this run and pushed first
> (`2026-09-11_does-the-c_sd-RESIDUAL-LAW-hold-on-a-CADENCE-and-GROSS-grid_B.py`). **Its
> verdict stands.** The two runs agree on every hard number both computed — beta
> −1.0264 / −1.5722 / −2.1435, t −6.32 / −6.32 / −6.31, R² 0.1999 / 0.1996 / 0.1991,
> beta/gross −2.0529 / −2.0963 / −2.1435, reproduction 486/486 at 6.864e-03 pp with B136
> and SMALL439 exactly 0, retirement bar 6 of 9 with every D-only point failing by 23–27%,
> 4a 0/1296, 4b 46/1296, WF-A picks beating RULES v2 OOS 0.
>
> **This run defers to lane B on two readings.** (1) **Cadence:** it pooled cadences into
> *sets* (W/M/Q, D-only, all) and read a 1.60× IS / 4.4× OOS gap. Lane B's **per-cadence**
> cut is finer and shows the pooled W/M/Q −2.0963 averages a **15× spread** — W −3.4627,
> D −3.3596, Q −2.4952, **M −0.2354 (t −0.42, R² 0.0034): monthly carries no c_sd slope at
> all**. So "the law holds on W/M/Q" is itself a pooling artefact, and lane B's statement is
> the correct one; everything below about cadence should be read through it. (2)
> **Mechanism:** gate G4 below reads max \|Δc_sd\| 9.861e-03 *pooled* and calls c_t not
> gross-invariant. Lane B shows the deviation is **QUANTILE-only** — MA-THRESH, which carries
> the entire residual, is gross-invariant to 1.1e-02 exactly as `c_t = k_t/n_t` predicts.
> That is the correct statement; §G4 below is the pooled version of it and the caveat it
> draws (a low-exposure-variance family's c_sd is substantially a gross artefact) survives.
>
> **What this run adds:** an independently written numpy backtester gated at 8.882e-16
> against `engine.backtest`; the 0.979× / 1.000× / 1.023× check of the measured slopes
> against the *pre-registered* −1.5722·g/0.75 scaling, which makes "the level is
> 0.75-specific, the law is beta/gross" a prediction met rather than a fit; and a 6-pick
> WF-A at panel × family granularity.

**Verdict (this lane, independently reached): SPLIT — the gross half SURVIVES (restated), the
cadence half is KILLED. No KEEP.**

Idea 535 published `resid0_pp = -0.0209 + (-1.5722) * c_sd(IS)` (t −0.87 | −6.32, IS R² 0.1996,
162 cells) and retired idea 301's GATE FAMILY constant on the strength of it. Every one of those
cells sat at gross 0.75 and at cadences W/M/Q. This run re-cut the whole decomposition at
gross ∈ {0.50, 0.75, 1.00} × cadence ∈ {D, W, M, Q} — 1,296 books, 648 decomposition cells,
each on FULL/IS/OOS.

## Gates (asserted before any new number was read)

| gate | what | result |
|---|---|---|
| G1 | `fast_backtest` == `engine.backtest` (numpy clone, 4 probe books) | **PASS** max dev **8.882e-16** |
| G2 | reproduce idea 535's committed `.decomp.csv` at g=0.75, W/M/Q | **PASS** 486/486 rows; max \|d resid0_pp\| **6.864e-03** pp (bar 1e-2), max \|d c_sd\| **8.510e-05** (bar 1e-4) — **exactly 0.00000000 on B136 and SMALL439**, the whole deviation is U56 (the known daily drift of `data/prices.csv`, ideas 513/515) |
| G3 | reproduce the published fit | **PASS** const −0.0209 (t −0.87), **c_sd(IS) −1.5722 (t −6.32)**, IS R² 0.1996, n 162 — \|d slope\| 0.00004, \|d t\| 0.0032 |
| G4 | is `c_t` invariant in gross, as the construction implies? | **FAIL** — see below |

## G4 failed: `c_sd` is NOT a gross-free axis

`c_t = gross(DEGROSS_t) / gross(RESPREAD_t)` is a ratio of two books carrying the same gross, so
it *looks* gross-free. It is not, because the engine's inter-rebalance drift renormalises by a
total that includes the **cash leg**, and the cash leg is gross-dependent.

    max |c_bar(g=0.50) - c_bar(g=1.00)| = 4.042e-03
    max |c_sd (g=0.50) - c_sd (g=1.00)| = 9.861e-03

That is small against MA-THRESH's own c_sd (≈ 0.2–0.3) but **~4x QUANTILE's** (≈ 0.0024), so on
the QUANTILE half of the grid a material part of the measured c_sd is a gross artefact of the
drift convention, not gate content. Any future c_sd claim on a low-exposure-variance family
needs to say which gross it was measured at.

## Headline 1 — GROSS: the −1.5722 is a 0.75-specific LEVEL; the law is slope/g

| cadence set | window | g=0.50 | g=0.75 | g=1.00 | spread of slope/g | hi/lo |
|---|---|---|---|---|---|---|
| W/M/Q (idea 535) | IS | **−1.0264** | **−1.5722** | **−2.1435** | — | — |
| W/M/Q, **slope / g** | IS | −2.0529 | −2.0963 | −2.1435 | **+0.0907** (4.2% of level) | 0.958 |
| W/M/Q, **slope / g** | OOS | −4.9880 | −5.0038 | −5.0266 | +0.0386 | 0.992 |
| D/W/M/Q, **slope / g** | IS | −2.3657 | −2.4052 | −2.4479 | +0.0822 | 0.966 |

The raw slope moves **2.09x over a 2x gross move**, so quoting −1.5722 without its gross is
wrong. Against the pre-registered mechanical prediction (`−1.5722 * g / 0.75`) the measured
slopes land at **0.979x / 1.000x / 1.023x** — the law survives, restated as
**≈ −2.1 pp/yr per unit c_sd per unit gross** on idea 535's own cadence set.

## Headline 2 — CADENCE: the law does NOT survive daily, and the retirement flips

| cadence set | IS slope/g | OOS slope/g | vs W/M/Q IS |
|---|---|---|---|
| W/M/Q (idea 535) | −2.0963 | −5.0038 | 1.00x |
| **D only** | **−3.3596** | **−1.1454** | **1.60x** |
| D/W/M/Q (all) | −2.4052 | −4.0711 | 1.15x |

Daily cells carry a **60% steeper** IS slope and a **4.4x flatter** OOS slope — the sign is
stable but nothing else is. And idea 535's retirement bar **flips**:

**B1a (CSD.is OOS MAE ≤ 0.95 × FAMILY OOS MAE), λ=1, all 9 (gross × cadence-set) points:**

| cadence set | g=0.50 | g=0.75 | g=1.00 |
|---|---|---|---|
| W/M/Q (idea 535) | 0.9219 ✅ | 0.9153 ✅ | 0.9074 ✅ |
| **D only** | **1.2297 ❌** | **1.2492 ❌** | **1.2710 ❌** |
| D/W/M/Q (all) | 0.9409 ✅ | 0.9335 ✅ | 0.9260 ✅ |

**6 of 9 points hold.** On daily cells CSD.is is worse than the FAMILY constant at every gross,
and worse than **predicting zero** (D-only g=0.75: ZERO 0.1260, FAMILY 0.1129, CSD.is 0.1411).
Idea 535's retirement of the family label is a W/M/Q result. It must be quoted with its cadence.

## Rule 8 walk-forward and both KEEP paths (PROTOCOL rules 4 and 8)

WF-B is the ladder above: every form fitted on IS cells only, scored once on OOS cells.

WF-A — inside each panel × family arm, (level, cadence, gross, construction) chosen on **IS
Sharpe alone** over 216 candidates; each pick read **once** on OOS (> 2016-12-31):

| panel | family | pick | OOS CAGR | OOS Sharpe | OOS MaxDD | vs RULES v2 (S) | vs SPY (S) | 4a | 4b | 4b fail |
|---|---|---|---|---|---|---|---|---|---|---|
| B136 | MA-THRESH | θ0.20 Q g1.00 RESPREAD | 0.2799 | 1.0693 | −0.3776 | 1.2851 ✗ | 0.8820 ✓ | ✗ | ✗ | DD |
| B136 | QUANTILE | x0.90 M g1.00 RESPREAD | 0.1818 | 1.1051 | −0.3146 | 1.2851 ✗ | 0.8820 ✓ | ✗ | ✗ | DD |
| SMALL439 | MA-THRESH | θ0.30 M g1.00 RESPREAD | 0.3190 | 1.1019 | −0.4044 | 1.2851 ✗ | 0.8820 ✓ | ✗ | ✗ | DD |
| SMALL439 | QUANTILE | x0.80 Q g0.50 DEGROSS | 0.0524 | 0.6279 | −0.1884 | 1.2851 ✗ | 0.8820 ✗ | ✗ | ✗ | H1,H2,OOS,CAGR |
| U56 | MA-THRESH | θ0.20 Q g1.00 RESPREAD | 0.2780 | 0.9421 | −0.4065 | 1.2747 ✗ | 0.8721 ✓ | ✗ | ✗ | DD |
| U56 | QUANTILE | x0.50 M g1.00 RESPREAD | 0.2144 | 1.2180 | −0.2569 | 1.2747 ✗ | 0.8721 ✓ | ✗ | ✗ | DD |

**6 picks: 0 beat RULES v2 OOS Sharpe, 5 beat SPY OOS Sharpe, 4a 0/6, 4b 0/6.** Five of six fail
4b on the **DD leg alone** — the IS-Sharpe selector walks straight into gross 1.00 and the DD cap
takes it.

Whole corpus, 1,296 books: **4a 0, 4b 46 (3.5%)**. All 46 sit on U56 (36) and B136 (10); **SMALL439
passes 4b 0 times at any gross or cadence**. By cadence: M 20, W 14, D 8, Q 4 — and every one of
the 8 daily passes is on U56, B136 clearing 4b 0 times at daily cadence. By gross: U56 0.50 → 8,
0.75 → 18, 1.00 → 10; B136 0.50 → 4, 0.75 → 3, 1.00 → 3. The two binding legs across the corpus
are DD (347 sole failures) and CAGR (344).

**No KEEP, no memo.** Nothing here is a capital candidate.

## Caveats

SURVIVORSHIP (idea 54, `data/SMALL_PANEL_README.md`): `prices_small.csv.gz`, `universe.json` and
`universe_broad.json` are all **current constituents with no delistings**, so every CAGR *level*
above is inflated and the 4a/4b columns inherit that whole. The headline object is an arm-minus-arm
contrast on the same names and days (DEGROSS and RESPREAD share one gate mask), so the bias very
largely cancels out of gap0/pred0/resid0; it does **not** cancel out of the KEEP columns. SMALL439
drops all 44 tickers with `max_1d_move >= 1.0` before use (439 names remain).

Costs 10 bps per unit turnover; the 0-bps rung is derived exactly (`r0 = r10 + turnover*bps/1e4`),
never re-run. Weights decided at close t, applied at t+1. No shorting; gross 1.00 is fully
invested, never above.

## Follow-ups filed

Lane B's **724–726** stand (the monthly-zero slope, whether the daily inversion generalises, and
re-stating the record's pp/yr slopes in beta/gross units). This run files only one that lane B's
finer mechanism cut does not already cover:

- **730** — does the drift-convention gross leak in `c_t` (§G4, 9.861e-03, concentrated in
  QUANTILE per lane B) change any *published* QUANTILE-family residual verdict, whose own c_sd is
  only ~0.0024?

# Idea 552 — is-the-ANNUAL-collapse-a-JENSEN-artefact-of-the-c_bar-PREDICTOR (cloud, 2026-09-09)

**Verdict: ANSWERED / H_JENSEN — the annual collapse does not survive, and neither does the
interior signal.** Idea 551's "at annual the MA gate is indistinguishable from a pure-exposure
gate" is a statement about the **arithmetic mean of the exposure path**, not about the gate.
Swapping in the compounding-consistent geometric predictor the queue asked for moves the
separation by **+0.22 to +0.59 pp/yr on the MA arm and by 0.000–0.010 pp/yr on the control**,
which turns the annual cell from ≈0 into the **largest** cell on every panel and the interior
cells into ≈0. All six (control × panel) collapse ratios go from 0.13–0.23 (collapsed) to
6.3–24.4 (not collapsed). Five defensible zero-parameter estimators of the same path give five
different qualitative stories, so the **sign of the separation is not identified until the
constant is named**.

Script: `2026-09-09_is-the-ANNUAL-collapse-a-JENSEN-artefact-of-the-c_bar-PREDICTOR_cloud.py`
Artefacts: `.grid.csv` (all 810 books) `.decomp.csv` (1,215 cells × 5 forms × 3 windows)
`.sep.csv` `.ratios.csv` `.jensen.csv` `.walkforward.csv` `.keeppaths.csv` `.console.txt`

## Gates, read before the headline — all six PASS

| gate | bar | result |
|---|---|---|
| G0 cadence-extended runner vs `engine.backtest` at D/W/M/Q, all 3 panels | < 1e-12 | **PASS**, 8.882e-16 |
| G1 identity `r_dg,t = c_t · r_rs,t` at 0 bps | < 1e-12 | **PASS**, 5.274e-16 |
| G2 AM ≥ GEO ≥ HARM cellwise | all cells | **PASS**, 1215/1215 both |
| G3 the PATH predictor drives resid0 to 0 | < 1e-12 | **PASS**, 8.882e-14 pp/yr |
| R1a idea 551's MA resid0, 15 cells | < 0.01 pp/yr | **PASS**, max \|Δ\| **0.00005** |
| R1b idea 551's MA−QUANTILE-M separation, 15 cells | < 0.01 pp/yr | **PASS**, max \|Δ\| **0.00004** |

**G3 is the point of the whole run.** Because `r_dg,t = c_t · r_rs,t` exactly, the residual is

`resid0 = CAGR(c_t · r_rs) − CAGR(c · r_rs)`

for whatever scalar `c` the predictor uses. resid0 is **entirely** a path-versus-constant
statistic, so *which constant* is not a detail of the estimator — it is half the definition. The
record has only ever used one. (Exposure-path zero share: max 0.372, mean 0.0056; GEO and HARM
are computed on the positive support and re-weighted by 1 − zero share, which is what keeps
AM ≥ GEO ≥ HARM exact.)

## The headline — separation MA − control (pp/yr), control = QUANTILE-M

| panel | form | D | W | M | Q | **A** |
|---|---|---|---|---|---|---|
| U56 | ARITH *(the record's)* | −0.2606 | −0.4325 | −0.2562 | −0.2306 | **+0.0539** |
| | **GEO** | +0.1098 | −0.0290 | +0.1611 | +0.2278 | **+0.6261** |
| | HARM | +0.5760 | +0.4748 | +0.6916 | +0.8644 | +1.3793 |
| | MEDIAN | −0.4196 | −0.5831 | −0.3923 | −0.3944 | −0.2205 |
| | JADJ | +0.0985 | −0.0405 | +0.1489 | +0.1990 | +0.5326 |
| B136 | ARITH | −0.3773 | −0.4573 | −0.3317 | −0.3842 | **−0.0456** |
| | **GEO** | −0.0231 | −0.0729 | +0.0797 | +0.0983 | **+0.5357** |
| SMALL439 | ARITH | −0.0897 | −0.2070 | −0.2025 | −0.6985 | **+0.0162** |
| | **GEO** | +0.1265 | +0.0423 | +0.0518 | −0.4014 | **+0.2668** |

Collapse ratio `R = |sep_A| / min over D,W,M,Q of |sep_c|`; the pre-registered reading is
"collapse present" when `R < 0.5`:

| control | panel | ARITH | GEO | HARM | MEDIAN | JADJ |
|---|---|---|---|---|---|---|
| QUANTILE-M | U56 | **0.234** | 21.62 | 2.91 | 0.562 | 13.14 |
| | B136 | **0.137** | 23.20 | 2.78 | 0.641 | 71.42 |
| | SMALL439 | **0.180** | 6.30 | 7.90 | 2.157 | 5.42 |
| QUANTILE-F | U56 | **0.212** | 20.45 | 2.90 | 0.580 | 12.56 |
| | B136 | **0.130** | 24.44 | 2.78 | 0.634 | 61.97 |
| | SMALL439 | **0.175** | 6.45 | 7.99 | 2.164 | 5.52 |

Collapse present on **6/6** under ARITH and **0/6** under every other form, on both controls.
**⇒ H_JENSEN**, on idea 551's own arm and on the matched restatement alike.

**The honest caveat on the ratio.** `R` rises partly because its *denominator* collapses: under
GEO the interior cells are near zero, not because the annual cell grew into something meaningful.
The defensible statement is not "the annual break is fake and the interior is real" — it is that
**the level, the sign and the cadence-ordering of this statistic are all predictor artefacts**.
ARITH says negative everywhere with annual nearest zero; HARM says positive everywhere
(+0.32 … +1.40); MEDIAN says negative everywhere *including* annual; GEO and JADJ say ≈0 in the
interior and largest at annual. Same books, same days, same ranking, five location estimators of
the same exposure path.

## The mechanism — the Jensen term lands almost entirely on the MA arm

`pred0(ARITH) − pred0(GEO)`, mean over 9 θ (pp/yr):

| panel | family | D | W | M | Q | A |
|---|---|---|---|---|---|---|
| U56 | MA-THRESH | 0.3710 | 0.4042 | 0.4185 | 0.4609 | **0.5824** |
| | QUANTILE-M | 0.0006 | 0.0007 | 0.0012 | 0.0025 | 0.0102 |
| B136 | MA-THRESH | 0.3544 | 0.3847 | 0.4120 | 0.4839 | **0.5867** |
| | QUANTILE-M | 0.0002 | 0.0003 | 0.0006 | 0.0014 | 0.0053 |
| SMALL439 | MA-THRESH | 0.2162 | 0.2494 | 0.2548 | 0.2985 | 0.2541 |
| | QUANTILE-M | 0.0000 | 0.0001 | 0.0005 | 0.0014 | 0.0034 |

Because the exposure-path SD is **0.111–0.137** for the MA gate and **0.0006–0.0158** for the
constant-depth control, the arithmetic predictor's Jensen error is ~60–1000× larger on the arm
under test than on its own control. The separation the record reads as "what the MA gate's depth
movement buys" is, in the arithmetic parameterisation, **mostly that error** — 0.22–0.59 pp/yr
against a separation of 0.05–0.70 pp/yr. It grows monotonically with cadence on 5 of 6
(panel, family) MA rows, which is exactly why the annual cell was the one that looked different.

## Rule 8 walk-forward

**WF-A (the statistic).** Collapse ratio on IS alone, then read once on the untouched OOS window:
IS/OOS agreement on "collapse present" is **26 of 30** (0.8667) cells. The four disagreements are
all MEDIAN. More telling: **under ARITH the collapse is present in both halves on B136 only** —
on U56 (IS 0.579 / OOS 1.443) and SMALL439 (12.55 / 2.12) it is absent in *both* halves, i.e.
even the record's own reading is a full-sample artefact on 2 of 3 panels. Annual cadence gives
only ~9 rebalances per half, so the half-sample ratios are noisy and are reported as evidence
about stability, not as a replacement headline.

**WF-B (the book).** (θ, cadence) chosen on IS Sharpe in each panel × family × construction arm,
OOS read once: beats the no-gate EWall control **2/18**, beats SPY 11/18, beats RULES v2 (live)
**0/18**.

## KEEP paths (both, all 810 books)

`4a: 1 / 810` · `4b: 27 / 810` · `BOTH: 0`. Failing bars: DD 558, CAGR 418, OOS 312, H2 309,
H1 300. The single 4a passer — U56, θ +0.06, monthly, QUANTILE-M/DEGROSS: CAGR 7.02 %,
Sharpe 1.2364, MaxDD −9.20 %, halves 1.301 / 1.191, OOS Sharpe 1.2603 — is the **same cell idea
305 already published**, fails 4b on CAGR, and its OOS Sharpe sits *below* the live book's. It is
recorded as a reproduction, **not** a new KEEP-candidate. Comparands on U56 over
2009-01-13…2026-09-08: RULES v2 (live) CAGR 8.64 %, Sharpe 1.2037, MaxDD −12.05 %, halves
1.2309 / 1.1828, OOS 1.2817; SPY CAGR 15.19 %, Sharpe 0.8871, MaxDD −33.72 %, halves
0.9587 / 0.8287, OOS 0.8786. **No book promoted, no memo, no RULES change.**

## What the record has to change

Every published `resid0`, `pred0` and MA-minus-QUANTILE separation must carry the **predictor
form** alongside the panel, cadence and window. "The MA gate's timing residual is −0.35 pp/yr" is
shorthand for "…under an arithmetic-mean exposure predictor", and the same books under a
compounding-consistent one give ≈0 or the opposite sign. The specific claim under audit — idea
551's "at annual the MA gate is indistinguishable from a pure-exposure gate" — is **withdrawn as
stated**: it is true of ARITH and false of GEO, HARM, MEDIAN and JADJ.

**SURVIVORSHIP:** B136 and SMALL439 are current constituents only — CAGR levels and both KEEP
columns are inflated. resid0, the Jensen term and the separation are arm-minus-arm contrasts on
the same names, days and ranking, so they are very largely immune. SMALL439 drops the 44 tickers
with `max_1d_move ≥ 1.0` in `data/small_meta.csv`.

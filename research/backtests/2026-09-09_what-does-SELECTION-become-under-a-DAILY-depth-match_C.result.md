# Idea 559 — what-does-SELECTION-become-under-a-DAILY-depth-match (lane C, 2026-09-09)

**Verdict: ANSWERED / KILL of idea 305's SELECTION leg as a "which names" statistic, and KILL
of its panel ordering.** Under the queue's daily depth match, SELECTION does not shrink — it is
**identically zero**, because the MA gate and idea 305's quantile control rank on the *same*
variable. Idea 305's published SELECTION (+1.2436 SMALL439 / −0.4058 B136 / −0.5779 U56 pp/yr)
and idea 556's ADD/DROP/BOTH split of it are **100% depth-timing**, 0% name choice.

Script: `2026-09-09_what-does-SELECTION-become-under-a-DAILY-depth-match_C.py`
Outputs: `.legs.csv .pairs.csv .grid.csv .match.csv .walkforward.csv .keeppaths.csv .console.txt`

## Design

10 bps, next-day execution (engine), gross 0.75, no shorting, no leverage. Tuned dials: **2** —
panel {U56, B136, SMALL439} × theta (9 rungs). Reported contrasts (not selected over): family
× construction × cadence. 351 books, every grid point reported.

| family | gate | depth match |
|---|---|---|
| `MA-THRESH` | `px > MA200*(1+theta)`, i.e. `dist > theta` with `dist = px/MA200 − 1` | — |
| `QUANTILE-M` | top-k by **dist** | idea 305's: `k_t = ceil(x·n_t)`, `x` = the MA gate's MEAN mask fraction |
| `QUANTILE-D` | top-k by **dist** | the queue's: `k_t = k_ma(t)`, pinned every day |
| `MOM-M` | top-k by **12-1 momentum** (`px.shift(21)/px.shift(252) − 1`) | MEAN-matched |
| `MOM-D` | top-k by **12-1 momentum** | DAILY-matched |

Cadence W (live) with both constructions = 270 books; cadence D RESPREAD for three families
= 81 books.

## Gates — all PASS

| gate | value | bar |
|---|---|---|
| G1 zero-cost identity `Σ W_i r_i == ret + turnover·bps/1e4` (351 books) | 1.110e-16 | 1e-12 |
| G2 three-leg identity `ADD+DROP+BOTH == gap` (486 cells) | 1.318e-16 | 1e-12 |
| R1 reproduces idea 556's `legs.csv` (81 rows × ADD/DROP/BOTH/SELECTION) | 1.776e-15 | 1e-9 |
| R2 reproduces idea 305's `pairs.csv` cadence-W rows (54 × 4 columns) | 3.553e-15 | 1e-9 |

## H_IDENT — **HOLDS**. The daily-matched control *is* the gate.

`MA-THRESH` admits exactly `{dist > theta}`. Taking the top `k_ma(t)` names by `dist` returns
that same set. Measured, not asserted:

- **0** disagreeing (name, day) cells over all 27 (panel, theta) cells × every bar.
- max |SELECTION| over the 162 `QUANTILE-D` leg rows (W and D) = **0.000e+00 pp/yr**.
- max |ADD|, |DROP|, |BOTH| over the same rows = **0.000e+00 pp/yr**.
- corroboration: every `QUANTILE-D` book equals its `MA-THRESH` twin to 1e-12 on CAGR, Sharpe,
  MaxDD and OOS Sharpe — including all 6 of its 4b passers, which duplicate the gate's.

**So closing the mismatch channel annihilates the contrast rather than narrowing it.** Whatever
idea 305's SELECTION leg measures, it is not which names the MA slice holds — at equal daily
depth the two gates hold the *same* names. The 27-cell mean depth error of the MEAN match is
**15.5 names/day** (U56 4.3, B136 10.4, SMALL439 31.7); that mismatch is the entire leg.

## The real question: SELECTION on a ranker that is actually different

`MOM-D` (12-1 momentum, daily-matched) is the non-degenerate comparand. Panel means of the
SELECTION leg, 9 thetas, FULL sample, RESPREAD, pp/yr:

| cadence | control | U56 | B136 | SMALL439 | ordering |
|---|---|---|---|---|---|
| W | `QUANTILE-D` | 0.0000 | 0.0000 | 0.0000 | (degenerate) |
| W | `QUANTILE-M` (idea 305's) | −0.8863 | −0.6438 | **+0.7450** | SMALL439 > B136 > U56 |
| W | `MOM-M` | −1.3542 | −1.5190 | −0.4217 | SMALL439 > U56 > B136 |
| W | `MOM-D` | **−0.3642** | −1.1499 | **−1.2430** | **U56 > B136 > SMALL439** |
| D | `MOM-D` | −2.2040 | −3.2526 | −2.9826 | U56 > SMALL439 > B136 |

idea 305 (pooled over 3 cadences × 2 qfams): U56 −0.5779, B136 −0.4058, SMALL439 +1.2436 →
**SMALL439 > B136 > U56**.

### H_ORDER — **FAILS**, and it fails by reversing

On the pre-registered cell (cadence W, `MOM-D`) the ordering is **exactly reversed**:
U56 −0.3642 > B136 −1.1499 > SMALL439 −1.2430. Three matches give three different orderings,
and SMALL439 is *last* under the only match that closes the depth channel. SELECTION is also
negative in **22 of 27** (panel, theta) cells — at matched daily depth the MA slice **loses** to a
momentum-picked slice of the same size. The 5 positive cells sit at the two ends of the theta
ladder: theta +0.30 on all three panels (where the gate holds 1–3 names) and theta −0.40 on U56
and B136 (where it holds nearly everything).

"The MA threshold's slice is a better slice on small caps" does not survive the depth match:
it was a statement about depth, published as a statement about names and about panels.

## H_DRIFT — **FAILS as a composite**, both sub-claims confirmed

The queue's premise is that BOTH is zero by construction under a daily match. Precisely:

| cadence | control | mean \|BOTH\| | max \|BOTH\| | BOTH share of \|ADD\|+\|DROP\|+\|BOTH\| | cells \|BOTH\|>\|SEL\| |
|---|---|---|---|---|---|
| W | `QUANTILE-M` | 2.3277 | 9.1395 | **31.5%** | 17/27 |
| W | `MOM-M` | 1.8796 | 6.0264 | 17.8% | 13/27 |
| W | `MOM-D` | 0.0106 | 0.0766 | **0.4%** | 0/27 |
| D | `MOM-D` | 0.0012 | 0.0133 | 0.3% | 0/27 |
| W/D | `QUANTILE-D` | 0.0000 | 0.0000 | 0.0% | 0/27 |

(The 31.5% row reproduces idea 556's headline exactly.) The composite fails only on its literal
"exactly 0 at cadence D" clause. The reason is isolated: at cadence D, `BOTH_pp` is **exactly
0.000** in the 18 cells where the daily match is exact, and non-zero **only** in the 9 cells where
the 12-1 ranker has fewer rankable names than `k_ma` (dk 0.006–0.190 names/day; corr(dk, |BOTH|)
= 0.58). Both substantive sub-claims hold:

1. a daily match collapses BOTH from **31.5% → 0.4%** of the decomposed magnitude, and it never
   exceeds |SELECTION| again (17/27 → 0/27);
2. what remains at weekly cadence is **drift**, not name choice — the engine re-normalises drifted
   weights daily, so two arms holding a shared name at the same *target* hold it at different
   weights between rebalances (max 0.0766 pp/yr).

**Consequence for the record:** "BOTH = 0 by construction" is true only where the match is exact
*and* there is no drift. Any published decomposition at weekly-or-slower cadence carries a drift
leg that a daily match does not remove.

## Rule 8 walk-forward (IS = start..2016-12-31, OOS = 2017-01-01..end, read once)

- **WF-A** (SELECTION sign / dominant side picked IS, checked OOS, 18 cells × 9 thetas):
  sign holds **133/162**, dominant side **147/162** — but 54 of those are the degenerate
  `QUANTILE-D` cells that hold 9/9 trivially. On the 9 non-degenerate `MOM-D`/`MOM-M` cells only,
  sign holds **59/81** (dominant side 68/81) and the panel means flip sign IS→OOS in 3 of 9
  (U56 `MOM-D` +1.21 → −1.66; U56 `MOM-M` +0.10 → −2.54; SMALL439 `MOM-M` −2.89 → +1.19).
- **WF-B** (theta picked on IS Sharpe per panel × cadence × family × construction, OOS read once,
  39 cells): **beats RULES v2 OOS 0/39**, beats SPY OOS 25/39. Best OOS Sharpe 1.1626
  (U56 `MOM-D`/DEGROSS theta −0.25, OOS CAGR 13.17%, OOS MaxDD −20.74%) against RULES v2 OOS
  **1.2817** and SPY OOS 0.8786.
- **WF-C** (`MOM-D`, cadence W): the DEPTH model `sel ~ 1+x+x²` fitted IS beats the PANEL-mean
  model out of sample — OOS MAE **1.5847** vs **2.4368**, and beats zero (2.2524) and the pooled
  IS mean (1.8963); OOS sign agreement 24/27 vs 17/27. Even for a genuinely different ranker,
  **the panel label is the worse predictor of SELECTION than the matched depth is** — consistent
  with idea 556's H_DEPTH, now on a contrast where SELECTION is not identically zero.

## Both KEEP paths — 351 books

**4a 0/351, 4b 20/351, BOTH 0/351.** 4b failing bars: DD 245, CAGR 170, H2 159, OOS 157, H1 155.
All 20 4b passers are U56 (15) or B136 (5); 7 are `MA-THRESH` and the *same* 7 are its identical
`QUANTILE-D` twin (2 `QUANTILE-M`, 2 `MOM-M`, 2 `MOM-D`), so the distinct-book count is 13. Best
4b passer by Sharpe: U56 `QUANTILE-M`
/DEGROSS theta −0.12 — CAGR 12.43%, Sharpe 1.1560, MaxDD −20.01%, halves 1.2554/1.0713, OOS
Sharpe 1.1416. Comparands (U56): SPY CAGR 15.19% / Sharpe 0.8871 / MaxDD −33.72% / halves
0.9587/0.8287 / OOS 0.8786; RULES v2 8.64% / 1.2037 / −12.05% / 1.2309/1.1828 / OOS 1.2817.
**No book promoted, no memo, RULES.md / scan.py / bot.py / baseline.py untouched.**

## Survivorship and other honest limits

- B136 and SMALL439 are **current constituents only**; CAGR levels are inflated and the 4a/4b
  columns are not immune. The ADD/DROP/SELECTION legs are same-panel arm-minus-arm differences,
  so the bias very largely cancels there.
- H_IDENT is a property of *this* pairing: the MA gate and a quantile gate on the MA gate's own
  ranking variable. It says nothing about a quantile control built on a different signal — which
  is exactly why `MOM-D` was added rather than reported as an afterthought.
- The `MOM-D` ordering is a 9-theta panel mean with wide within-panel spread (U56 ranges −2.26 to
  +5.30); the claim made is the reversal of the *ordering*, not a stable per-theta level.
- `MOM-M` and `QUANTILE-M` share the identical mean-match depth error by construction, so their
  BOTH legs are not independent evidence of each other.

## Follow-ups filed: 561, 562, 563

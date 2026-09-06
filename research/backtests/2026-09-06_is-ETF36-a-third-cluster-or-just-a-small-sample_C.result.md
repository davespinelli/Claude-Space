# Idea 277 — is-ETF36-a-third-cluster-or-just-a-small-sample (lane C, 2026-09-06)

**Verdict: ANSWERED / KILL of the third-cluster hypothesis.** On the reversal statistic an
ETF panel is **not a distinct regime** — it is a **SMALL SAMPLE**. ETF36's published 2/7
sits inside the seed range of k-matched *stock* panels, the ETF share explains **less of the
reversal share than the random seed does** (between/within sd ratio **0.54x**, permutation
p **0.41**), and the curve is non-monotone, so the queue's "where does it turn over" has no
answer to give. What ETF share *does* move, monotonically and hard, is the **level**: OOS
Sharpe falls **1.0597 → 0.6656** and OOS CAGR **12.60% → 5.58%** across the sweep, **8 of 8
steps in the right direction**. No KEEP-candidate, no memo, no RULES change; `RULES.md`,
`scan.py`, `bot.py` and `baseline.py` untouched.

Script: `2026-09-06_is-ETF36-a-third-cluster-or-just-a-small-sample_C.py`

## Design

Idea 271's characteristic model predicted **zero** reversals on ETF36 at every leave-one-
source-out fit and landed exactly on that source's base rate (lift **0.0000**) — the one
source where the model was neither right nor wrong. ETF36 is also the odd panel physically
(k=36 against 100–439; corr 0.34, disp 0.062). Those two facts are perfectly confounded, so
this run **mixes the panels and holds width fixed**: k = **36** everywhere, with
n_etf = round(s·36) ETFs drawn from the 36-name ETF set and 36 − n_etf stocks from BSTK100,
for

    s in {0.000, 0.125, 0.250, 0.375, 0.500, 0.625, 0.750, 0.875, 1.000}
      -> n_etf 0, 5, 9, 14, 18, 23, 27, 32, 36     x seed in {0..5}

At s = 1.000 every seed is the same panel and it **is ETF36 exactly** (asserted at run time,
not assumed), so the sweep terminates on the parent's own panel. Pool = **5 NAMED + 48 MIX
= 53 panels × 7 pre-registered ratios = 371 reversal cells, 1060 backtests, 530 grid points
per cost rung, all reported.** Weekly, t+1, 10 bps, gross 0.75, gate above-200d AND
vol20 < 0.60, ranking key = the composite without the vol scaler; 0 bps is a diagnostic
column only. Reversal is idea 259/269's epsilon rule unchanged.

Tuned parameters: **ETF share s (9)** and **target ratio r\* (7)**. The characteristics are
measured, not tuned; the cost rung is fixed at PROTOCOL's 10 bps.

**Seed history, stated because it is a design change.** The first pass ran seeds {0,1,2} and
died in a print-formatting call **after** Q1/Q2 had printed. The seed count was raised 3 → 6
for power before any verdict was formed. Seeds are keyed by string, so seeds 0–2 are the
**identical** panels: the 3-seed subset is printed beside the 6-seed pool and reproduces the
first pass exactly (s=0 rung 0.6190 / s=0.125 0.3333 / s=0.25 0.7143 / … / ETF36 0.2857).
Both are reported everywhere the verdict rests on them; neither changes the sign.

## Reproduction gate (5/5 exact, before any new number was read)

| cell | this run | published |
|---|---|---|
| B136/EWall | 10.7% / 1.026 / −17.7%, OOS 1.019 | 10.7% / 1.026 / −17.7%, OOS 1.019 |
| U56/EWall | 10.4% / 1.049 / −15.9% | 10.4% / 1.049 / −15.9% |
| per-panel counts | **6 / 6 / 4 / 2 / 0 of 7** | 6 / 6 / 4 / 2 / 0 of 7 |
| share by ratio | 0.60 / 0.60 / 0.80 / 0.80 / 0.40 / 0.40 / 0.00 | identical |

## (1) The sweep — the reversal share does not move with the ETF share

| s | panels | share | sd | min | max | breadth | disp | corr | evol |
|---|---|---|---|---|---|---|---|---|---|
| 0.000 | 6 | 0.5238 | 0.3216 | 0.1429 | 0.8571 | 0.6821 | 0.0964 | 0.3626 | 0.2414 |
| 0.125 | 6 | 0.3333 | 0.3216 | 0.0000 | 0.7143 | 0.6788 | 0.0929 | 0.3530 | 0.2296 |
| 0.250 | 6 | 0.6667 | 0.2502 | 0.2857 | 1.0000 | 0.6747 | 0.0932 | 0.3404 | 0.2201 |
| 0.375 | 6 | 0.5476 | 0.2289 | 0.2857 | 0.8571 | 0.6714 | 0.0884 | 0.3522 | 0.2124 |
| 0.500 | 6 | 0.6905 | 0.2289 | 0.4286 | 1.0000 | 0.6743 | 0.0844 | 0.3539 | 0.2015 |
| 0.625 | 6 | 0.5952 | 0.3053 | 0.1429 | 0.8571 | 0.6677 | 0.0823 | 0.3464 | 0.1932 |
| 0.750 | 6 | 0.4524 | 0.2461 | 0.1429 | 0.7143 | 0.6782 | 0.0752 | 0.3551 | 0.1792 |
| 0.875 | 6 | 0.4048 | 0.2103 | 0.1429 | 0.7143 | 0.6727 | 0.0693 | 0.3465 | 0.1713 |
| **1.000 (= ETF36)** | 1 | **0.2857** | — | 0.2857 | 0.2857 | 0.6750 | 0.0620 | 0.3436 | 0.1579 |

- **Spearman(s, share) = −0.0886, t −0.61**, permutation p **0.5470** (2000 shuffles of the
  rung label). The 3-seed subset gives −0.1845, t −0.90 — same sign, same nothing.
- The curve **reverses direction twice** over its 8 steps. It crosses its own midpoint at
  s = 0.078, 0.152 and 0.875, and the 0.50 level at s = 0.016, 0.188 and 0.708. **The queue's
  "where does the reversal share turn over" has no single answer because the curve is not
  monotone** — that is the finding, not a missing number.
- **Between-rung sd 0.1419 vs within-rung (seed) sd 0.2641 → ratio 0.54x**, permutation
  p **0.4105**. Which ETFs and which stocks you happened to draw matters roughly **twice as
  much** as how many of them were ETFs.

## (2) Step or continuum? Neither — there is no shape to fit

| model | R² | adjR² | key t |
|---|---|---|---|
| linear in s | 0.0041 | −0.0171 | s −0.44 |
| step at s = 1 only | 0.0159 | −0.0050 | −0.87 |
| step at s ≥ 0.875 | 0.0411 | +0.0207 | −1.42 |
| linear in s + step at s = 1 | 0.0169 | −0.0259 | −0.21 / −0.77 |

The best of the four explains **4.1%** of 49 panels at t −1.42. A cluster is a claim about a
discontinuity; there is no discontinuity here, and there is no slope either.

## (3) The small-sample band — ETF36 is an ordinary draw

k-matched **stock** panels at s = 0.000 (same k = 36, same grid) score
**0.1429, 0.2857, 0.2857, 0.7143, 0.8571, 0.8571** — mean 0.5238, sd 0.3216, range
[0.1429, 0.8571]. ETF36's **0.2857 is INSIDE** that range, at **z = −0.74**; **35.4%** of the
48 s<1 panels score at or below it. The mechanical floor from 7 cells at p = 0.5 is
sqrt(.25/7) = **0.1890**, and the observed within-rung sd is 0.2641 — i.e. **most of the
spread the record has been reading off 7-cell panel shares is sampling noise.** Idea 269C's
five-panel ordering (B136 6/7 … ETF36 2/7 … SMALL439 0/7) is a **ranking of six-to-seven-cell
binomials**, and only its SMALL439 end survives that (idea 271 already showed breadth is
perfectly bimodal there, with no overlap).

## (4) Mediation — ETF-ness is not even a characteristic story

Idea 271's four characteristics fitted on the **48 s<1 MIX panels** (R² 0.1838; breadth
t +2.27, disp t +2.26, corr t −0.08, evol t −1.79) predict ETF36 at **0.3541** against an
actual **0.2857** — residual **−0.0684 = −0.26 residual sd**, comfortably inside the 95%
prediction band [−0.152, 0.861]. **The parent's lift-0.0000 on ETF36 was not the model being
blind to a third regime; there was no third regime to see.**

One genuine nuance, reported because it is the only place s is significant: **marginally** s
is worth nothing (R² 0.0041, t −0.44), but **conditional on the four characteristics** it
carries t **+3.47** with a **positive** sign (+0.4551) and lifts R² 0.1956 → 0.3717 — while
evol's coefficient flips −0.2058 → +0.3222. That is **suppression**, not a hidden effect:
raising the ETF share mechanically lowers dispersion (0.0964 → 0.0620) and eligible-set vol
(0.2414 → 0.1579), and the two channels cancel. The record only ever observes the marginal
effect, and the marginal effect is zero.

## Rule 8 (PROTOCOL) — walk-forward, IS ≤ 2016 chooses, 2017–2026 read once

**(i) The relationship.** All 4 rules × 19–20 thresholds are in `.threshold_grid.csv`.
OOS majority base rate over the 343 sweep cells **0.5219** (OOS reversal rate 0.4781):

| classifier | IS acc | OOS acc |
|---|---|---|
| CONST (IS majority = False) | 0.5977 | 0.5219 |
| R_THRESH (r < 0.10) — idea 269C | 0.6093 | 0.5219 |
| **S_ONLY (ETF share alone)** | 0.6006 | **0.5131** |
| CHAR (idea 271's four) | 0.6706 | 0.5714 |
| CHAR+s | 0.6997 | **0.6356** |

**The ETF share alone is the only rule in the table that loses to the constant out of
sample** (0.5131 vs 0.5219). On the honest test — **train s ≤ 0.500, predict s > 0.500**, the
ETF end held out entirely, base rate 0.6316 on 133 cells — CHAR+s scores **0.6541** (+0.0225,
i.e. **3 cells**), CHAR **0.6241** (below the base rate) and S_ONLY predicts *nothing*
(pred_rate 0.0000, lands exactly on 0.6316). Nothing here is worth a column.

**(ii) The book** — pooled equal-weight over the 5 NAMED panels, 10 bps, OOS read once:

| book | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|---|
| EWALL (do nothing) | 8.81% | 0.8807 | −20.6% | 0.99 / 0.78 | 8.61% | 0.8574 | −20.6% |
| FWD20 (incumbent) | 10.84% | 0.9028 | −21.4% | 1.00 / 0.82 | 11.12% | 0.9031 | −21.4% |
| S_SHARPE | 12.77% | 0.9372 | −21.6% | 1.07 / 0.82 | 12.43% | 0.8887 | −21.6% |
| S_CAGR | 14.36% | 0.8462 | −23.0% | 0.93 / 0.77 | 13.99% | 0.7973 | −23.0% |
| **ESEL (CHAR+s selector)** | 10.05% | 0.8658 | −21.9% | 0.97 / 0.78 | 9.97% | **0.8426** | −21.9% |
| RSEL (width rule) | 11.19% | 0.8135 | −21.3% | 0.88 / 0.76 | 11.80% | 0.8247 | −21.3% |
| RULES v1 | 6.74% | 0.7399 | −17.3% | 0.89 / 0.61 | 6.43% | 0.6908 | −17.3% |
| **RULES v2 (live baseline)** | 7.07% | **1.0464** | **−11.2%** | 1.11 / 0.98 | 7.16% | **1.0776** | −11.2% |
| **SPY** | 15.23% | 0.8890 | −33.7% | 0.96 / 0.83 | 15.45% | 0.8820 | −33.7% |

ESEL **buys nothing**: it loses to do-nothing EWALL on OOS Sharpe by −0.0148 while adding
turnover, loses to the incumbent FWD20 by −0.0605, and sits **0.235 of Sharpe and 10.7pp of
drawdown behind the live book**. This is the record's *n*-th instance of an IS chooser
losing to a constant.

**(iii) The by-product that is real — ETF share is a dilution dial, seed-averaged:**

| s | CAGR | Sharpe | OOS CAGR | OOS Sharpe |
|---|---|---|---|---|
| 0.000 | 13.13% | 1.0745 | 12.60% | 1.0597 |
| 0.125 | 11.75% | 1.0435 | 11.85% | 1.0576 |
| 0.250 | 11.22% | 1.0466 | 11.25% | 1.0434 |
| 0.375 | 10.16% | 0.9864 | 10.21% | 0.9809 |
| 0.500 | 9.18% | 0.9366 | 9.51% | 0.9626 |
| 0.625 | 8.28% | 0.8813 | 8.56% | 0.8953 |
| 0.750 | 7.63% | 0.8571 | 7.61% | 0.8529 |
| 0.875 | 6.34% | 0.7368 | 6.74% | 0.7682 |
| 1.000 | 5.11% | 0.6287 | 5.58% | 0.6656 |

(EWall, 10 bps; SPY over the same window 15.23%/0.8890/−33.7%, OOS 15.45%/0.8820/−33.7%.)
**OOS Sharpe and OOS CAGR are monotone in s in 8 of 8 steps**; full-sample Sharpe in 7 of 8.
Adding ETFs to a stock panel is a **pure dilution** — averaged over the 8 steps it costs
**0.0493 of OOS Sharpe and 0.88 pp/yr of OOS CAGR per 0.125 of ETF share** — and it never
once buys drawdown (EWall OOS MaxDD wanders −16.4% to −22.0% with no order in s, the deepest
rung being s = 0.000). **ETF36 is the low-return endpoint
of a smooth continuum, not a regime.** The IS-Sharpe pick is monotone in only 6 of 8 steps
and beats EWall OOS at s ≤ 0.125 only, losing at every rung from 0.250 up.

## Both KEEP paths, all 530 grid points per rung

| rung | 4a (vs live RULES v2) | 4a (vs RULES v1) | 4b (vs SPY + rule 8) |
|---|---|---|---|
| 10 bps | **0 / 530** | 107 / 530 | **31 / 530** |
| 0 bps | **0 / 530** | 68 / 530 | 71 / 530 |

**4a 0/530 against the live book at both rungs** — the 4a pathology again (idea 136), against
107/530 versus the superseded v1. Binding bar over the @10 bps failures: **H2 355, CAGR 331,
DD 324, OOS 321, H1 301.** The 4b pass rate by rung is 0.017 / 0.167 / 0.050 / 0.000 / 0.083 /
0.067 / 0.000 / 0.000 / **0.000** — **every rung at s ≥ 0.750 passes zero of 60**, consistent
with (iii). All 8 NAMED-panel passes (U56 FWD-31/20/14, B136 FWD-99/74/50/35 and B136 EWall)
are idea 269C's already-published set; the other 23 are MIX sub-panels. **No KEEP-candidate.**

## Survivorship

`universe_broad.json` is current constituents and every MIX panel is a subset of it, so the
bias is inherited whole. The un-ranked book holds everything and takes the full survivorship
premium while a ranked book can only redistribute it, so the bias runs **toward** reversals —
toward finding *more* cluster structure than a live universe would have shown. The
"no distinct regime" verdict is therefore conservative; the dilution slope in (iii), which
runs against the stock-heavy end, is if anything **understated**.

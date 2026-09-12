# Idea 589 — is the RETURN TAX of widening a RANK DECAY curve? (lane B, 2026-09-12)

**ANSWERED: YES — the tax IS the rank-decay curve, in its PARTIAL-MEAN form, to R² 0.995 with a
constant 0.77 attenuation; it is NOT the panel's name count; and the curve does not FORECAST, so
it is a decomposition, not a screening rule. KILL for capital (4a 0/60, 4b 1/60, and the
pre-registered rule-8 pick fails 4b out of sample on all three panels). One candidate PARKED.**
No RULES change proposed. RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.

## What was run

Books: `baseline.rules_v1_weights(px, n, w=g/n)` — rank eligible names (above 200d MA, vol20 <
0.60, priced) by the v1 composite score, hold the top *n* at *g*/N each, rest cash, weekly, next-day
execution. Two tuned parameters, as PROTOCOL 4 allows: width *n* ∈ {1,2,3,5,8,10,15,20,30,40} and
gross *g* ∈ {0.75, 1.00}. Three panels (U56, B136, SMALL716) × 10 widths × 2 gross = **60 books, all
reported**, at cost rungs 0 / 10 / 25 bps (10 bps headline). SPY is excluded from the tradeable set
on every panel (it is the benchmark; `rules_v2_weights`, the 4a comparand, is called unmodified and
therefore does hold it on U56/B136 — a level effect on the comparand, not on any slope here).

The decay curve: μ(k) = mean forward return of the *k*-th ranked eligible name, close t+1 → close
t′+1 (the engine's own timing), measured separately on FULL / IS (→2016) / OOS (2017→).

Gates, all three panels: cost identity `r(c) = r(0) − turnover·c/1e4` max|Δ| **0.000e+00**; book ==
`rules_v1_weights` max|Δ| **0.000e+00**; rank-tie disagreements between the average-rank and
first-rank objects 27 / 6 / 1 name-days out of ~4,400 × N (ties only, no effect on any book).

## H_DECAY — the arithmetic prediction

d(AnnRet)/dn from *n*→*n′* should equal g·52·(M(n′) − M(n))/(n′ − n), M = partial mean of μ(k).

| test | n | result |
|---|---|---|
| adjacent width steps, 0 bps | 162 | Pearson **+0.998**, OLS real = **0.772**·pred, R² 0.996, median \|err\| 0.14%/yr |
| adjacent width steps, 10 bps | 162 | Pearson **+0.998**, OLS real = **0.776**·pred, R² 0.995, median \|err\| 0.15%/yr |
| headline 5→20 contrast, FULL | 6 cells | Pearson **+0.999**, Spearman **+1.000** |

The curve predicts the tax almost exactly, but with a **constant 23% attenuation**: a traded book
keeps only ~0.77 of the decay curve's arithmetic step, because it drifts between rebalances,
de-grosses to cash when fewer than *n* names are eligible, and compounds. The attenuation is stable
across panels, eras and both gross levels — it is a property of the execution convention, not of a
panel.

Cell-level (5→20, FULL, 10 bps): U56 **+0.23 / +0.30** %/yr per name (g 0.75 / 1.00), B136 **+0.15 /
+0.20**, SMALL716 **−0.98 / −1.26**. On the two large-cap panels widening is a *subsidy*, not a tax —
the decay curve there is flat to slightly rising (OLS +13 and +34 bp/yr per rank, R² 0.03 and 0.15),
so the top-ranked names do not out-earn rank 20–40 at all. The tax is real and large only on
SMALL716, whose curve genuinely decays (−72 bp/yr per rank, R² 0.27).

## H_N — the rival

Across the 6 (panel × gross) cells, Spearman(width slope, **N**) = **−0.956** and Spearman(width
slope, median eligible count) = −0.956, against Spearman(width slope, **decay OLS slope**) = +0.478
— on that crude reading the name count wins. Two things settle it honestly:

1. Six points is not evidence, and N is perfectly confounded with panel identity (56 / 135 / 715).
2. **Within a panel N is constant**, so it explains none of the 162-point step test that the decay
   curve explains at R² 0.995. The decay curve's *partial-mean* form also gives Spearman **+1.000**
   against the realized cell slopes — the summary statistic that loses to N is the OLS-slope
   compression of the curve, not the curve. **The right statistic is M(n′) − M(n), not a fitted
   slope; the record should stop quoting a rank-decay "slope" at all.**

## Rule 8 — walk-forward, both on the book and on the relationship

Books: *n* and *g* chosen on 2009–2016 IS Sharpe alone, per panel; 2017–2026 read once.

| panel | IS pick | OOS CAGR / Sharpe / MaxDD | RULES v2 (same window) | SPY | OOS 4a | OOS 4b |
|---|---|---|---|---|---|---|
| U56 | n=20 g=1.00 | 14.39% / 1.04 / −22.5% | 9.47% / 1.28 / −12.1% | 15.33% / 0.88 / −33.7% | no | **no** (DD) |
| B136 | n=30 g=1.00 | 10.67% / 0.78 / −24.3% | 7.88% / 1.11 / −12.2% | 15.33% / 0.88 / −33.7% | no | **no** (H1+H2+DD+CAGR) |
| SMALL716 | n=10 g=0.75 | 19.36% / 0.73 / −27.9% | 4.47% / 0.65 / −12.2% | 15.33% / 0.88 / −33.7% | no | **no** (H1+H2+DD) |

IS→OOS Sharpe ordering over each 20-point grid is stable (Spearman +0.830 / +0.817 / +0.931) — the
width dial is not noise. It simply does not clear the 4b bars: every pick dies on the drawdown cap.

The relationship walked forward too: fit H_DECAY on IS (real = 0.702·pred, R² 0.959, n=54), then use
the **IS** curve to predict **OOS** steps — Pearson +0.910 but Spearman **+0.266**, median |err|
0.37%/yr, 2.5× the in-window error. The OOS curve on OOS books is back to +0.998. **The decay curve
must be measured in the window it is asked to explain; it decomposes, it does not forecast.** Any
future use of it as a screening rule is therefore refuted in advance by this run.

## Idea 320's premise, re-measured

On this grid (FULL, 10 bps, 6 cells): vol-benefit spread 2.329%, return-cost spread 1.564%, ratio
**0.67×** — idea 320's "return cost 1.5× more dispersed" is **NOT reproduced in direction** as
stated. But both spreads are dominated by SMALL716; on the two large-cap panels alone the ratio is
**24×**, i.e. 320's direction holds where its cells lived and reverses only once a 40%-vol panel
enters. Either way the comparison is a raw SCALE comparison in 320's form and in this one, and
should be normalised before it is quoted again.

## KEEP census (10 bps, full sample, 60 books)

**4a 0 / 60. 4b 1 / 60. BOTH 0.** Binding 4b bar: H1+H2+DD+CAGR 16, H1+H2+DD 14, H1+H2+CAGR 10,
H2+CAGR 6, H2+DD 5, CAGR 3, H2+DD+CAGR 2, DD 2, H2 1, none 1. Cost ladder: 4b count 6 → 1 → 1 at
0 / 10 / 25 bps — **five of the six zero-cost passers are paid for by 10 bps of turnover.** OOS
(2017–2026) over the same 60 books: 4a 0 / 60, 4b 4 / 60; passing 4b on BOTH full sample and OOS:
**1 / 60**.

## PARK (not KEEP): U56 top-40, gross 1.00, weekly

Full sample CAGR 12.54%, Sharpe 1.13, MaxDD −17.9%, halves 1.10 / 1.15, turnover 6.4×/yr; 4b passes
at 0, 10 **and** 25 bps. OOS CAGR 14.47%, Sharpe 1.26, MaxDD −17.9% — it passes 4b out of sample as
well. It is **PARK, not KEEP**, for two reasons stated plainly:

1. It was **not the rule-8 IS pick** (that was n=20). It is the best of 60 books read off the whole
   grid, i.e. a third selection — exactly the failure mode idea 590 flagged this week.
2. *n* = 40 is the **endpoint of the width grid** (and with only two gross levels, every book is a
   gross endpoint by construction, so the meaningful endpoint claim is the width one). Its Sharpe is
   still rising in *n* at the edge, so the grid never contained its argmax.

The honest next step is a pre-registered re-run of this one book with the width fixed in advance and
the grid extended past 40, on a cost ladder — filed as a new queue idea, not promoted here.

## Caveats

Current-constituent survivorship on all three panels (favours the wide books most, since widening
adds the lower-ranked survivors). SMALL716's n=1 and n=2 books read −88.8% MaxDD and 95–125%
annualised vol; those cells are reported but are thin-name price artefacts as much as strategy
results, and nothing in the answer rests on them. Only 2020 and 2022 are real stress tests. 2009–2026
is a QQQ-favourable regime.

# Idea 496 — publish the PENALTY beside every residualisation (lane B, 2026-09-10)

**VERDICT: KILL of the record-wide premise; CONFIRMED as a narrow, width-conditional
hazard. No RULES change, no book promoted, no KEEP. RULES.md, PROTOCOL.md, scan.py,
bot.py and baseline.py untouched.**

The queue's premise was: "`survive` moves 0.020 -> 0.959 across lam 1e-3..100 on
broad136 ... so the record's residualisation results are dominated by an unpublished
dial." Both halves of that sentence are tested here. The movement is real. The
*domination of the record* is not — because at the width the record actually fits at,
the dial does not move anything.

## Corpus, costs, execution
500 equal-weight 20-name draw books (250 per panel, U56 and B136, seeds 4960+i),
10 bps, weekly, weights decided at close t applied at t+1 (engine). No network; panels
read the committed caches. **672 grid points, all reported in `.grid.csv`.**
Tuned parameters, exactly two as the queue allows: **penalty (lam) and panel**.
Reported-but-not-tuned axes: design width p (7 values), sample size n (3 nested
prefixes), target key (2), verdict type (3).
**SURVIVORSHIP:** B136 and U56 are current constituents only (idea 54).

## A. Does the dial exist in the record, and is it published?

**A1 — the dial barely exists.** Of **109** committed `.py` under `research/` carrying a
fit call, **6 (5.5%)** penalise at all (ridge / `lam*np.eye` / `Ridge(`); **103 (94.5%)**
are unpenalised OLS, where lam is identically 0 and there is no dial to publish. All 6
penalised files are dated 2026-09-09 or later — i.e. the entire penalised lineage is
idea 252/483 and its own descendants. Every one of the 6 already sweeps lam in-file.

**A2 — the literal ask.** Of **74** committed CSVs whose columns carry a residualisation
statistic (`survive` / `kill` / `pR2` / `partial` / `*_resid` / `t_partial` ...), **7
(9.5%)** also carry a penalty column. **2,154 rows publish a penalty; 195,140 do not.**
That 90.5% figure is the headline the idea asked for — but A1 explains it: the missing
column is missing because the fit is OLS, not because a ridge penalty was hidden.

## B. Re-read at the three pre-registered penalties (lam 0.01 / 1.0 / 100.0)

72 cells (panel x key x n x p) re-read at all three. **24 cells have |t_raw| < 2, so the
kill fraction is uninterpretable; they are suppressed from the KILL/ALL tallies, not
imputed** (idea 483's own convention). Readable cells: 48.

| verdict | stable at all three penalties |
|---|---|
| KILL (survive < 1/3 AND \|t\| < 2) | 34/48 (70.8%) |
| SIGN of the residualised slope | 59/72 (81.9%) |
| SIG (\|t\| >= 2) | 58/72 (80.6%) |
| ALL THREE | **30/48 (62.5%)** |

**The result that matters is that stability is monotone in p/n, and the record lives at
the stable end.** Readable cells, by design width:

| p/n | cells | ALL-stable | median `survive` range across the three penalties |
|---|---|---|---|
| < 0.05 | 18 | **88.9%** | 0.050 |
| 0.05–0.2 | 16 | 68.8% | 0.334 |
| 0.2–0.5 | 6 | 50.0% | 0.639 |
| 0.5–1 | 5 | **0.0%** | 0.851 |
| > 1 | 3 | 0.0% | 0.525 |

**At or below the record's own widest committed residualisation** — idea 658 measured it
at p=6 on n=162, p/n **0.0370** — 10 readable cells, **ALL-stable 100%**, median
`survive` range across the three penalties **0.0304**. At p/n > 0.5, idea 483's WIDE
regime: 8 cells, **ALL-stable 0%**, median range **0.758**. Idea 483's 0.020 -> 0.959 is
reproduced (full sweep spans 0.0000 -> 2.081 across lam), and it is a property of a
regime the record does not occupy.

**B4 — the wide control is not merely penalty-sensitive, it is wrong.** A positive
control was run at every grid point: `y = 3*key + noise`, raw t +105 (U56) / +102 (B136),
so a correct residualisation must never kill the key. **112 of 672 grid points kill it
anyway** — 0 at p/n < 0.05, then 9 / 30 / 48 / 25 as p/n rises. **B5** gives the
mechanism, unchanged from idea 483: median R² with which the name-control reproduces the
key it is meant to control for runs 0.017 -> 0.996 (U56) and 0.033 -> 0.998 (B136) across
the same buckets.

So the reporting habit idea 483 proposed should be narrowed: a residualisation needs its
penalty published **only where p/n is large enough for the penalty to bind**, and above
p/n ≈ 0.5 the right response is not to publish the penalty but to not run the fit.

## C. Rule 8 walk-forward (parameters chosen on 2009–2016, evaluated on 2017–2026)

Pre-registered arm: lam = 1.0, the middle of the three penalties, fixed before any OOS
number was read; the book is the IS argmax of the residualised Sharpe.

| | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|
| U56 pick (lam 1.0) | 15.98% | 1.137 | −22.66% |
| B136 pick (lam 1.0) | 18.62% | 1.078 | −34.14% |
| RULES v2 (live) OOS | 9.48% / 7.98% | 1.279 / 1.119 | −12.05% / −12.24% |
| SPY OOS | 15.32% / 15.45% | 0.876 / 0.882 | −33.72% |

**The penalty changes the inference, not the book** — the same conclusion idea 483 drew
about folding. Across 8 lam values the residual selector picks only **2 distinct draws**
per panel (U56 switches at lam 100, B136 at lam 10); OOS Sharpe of the pick spans
1.137–1.226 (U56) and 1.066–1.078 (B136). **8/8 lam values beat SPY on OOS Sharpe; 0/8
beat the live RULES v2 book on OOS Sharpe, on either panel.**

## KEEP paths — **4a 0/500, 4b 0/500**

Priced for every draw book on both panels, full sample + halves + OOS. Neither path
passes, and the leg breakdown says why, identically on both panels:

| leg | U56 | B136 |
|---|---|---|
| 4b H1 Sharpe > SPY | 223/250 | 244/250 |
| 4b H2 Sharpe > SPY | 248/250 | 240/250 |
| 4b OOS Sharpe > SPY | 249/250 | 244/250 |
| 4b CAGR ≥ 70% SPY | **250/250** | **250/250** |
| 4b MaxDD ≤ 60% SPY | **0/250** | **0/250** |
| 4a H1 / H2 / MaxDD vs RULES v2 | 87 / 16 / **0** | 91 / 117 / **0** |

A random 20-name equal-weight book clears every Sharpe leg and the CAGR floor and dies
**solely** on the drawdown cap (−20.2% required, best draw −27.6%). This is an exposure
fact about ungated 100%-gross equity books, not a result about penalties, and it is
consistent with the record's standing finding that the 4b MaxDD leg is what growth books
fail on.

## Limits
- The census is a column-name and source-regex instrument, so A1/A2 are **lower bounds**
  on residualisations and upper bounds on nothing; a fit hidden behind a helper this
  regex misses is uncounted. This run's own artefacts are excluded from its own census.
- 24 of 72 stability cells are unreadable (|t_raw| < 2, U56 `sd` at n=50/100 and B136
  `mean_vol` at n=50/100) — reported, not imputed.
- Two panels, not three; SMALL439 was not run, so the p/n ladder is measured on large
  caps only.
- p/n above 0.5 is reached by shrinking n (nested draw prefixes), not by adding real
  regressors, so the wide cells are also the small-sample cells.

## Artefacts
`.py`, `.console.txt`, `.grid.csv` (672 points), `.stability.csv` (72 cells),
`.walkforward.csv`, `.keeppaths.csv` (500 books), `.census_py.csv` (109 files),
`.census_csv.csv` (74 files).

# Idea 270R — is S_CAGR vs S_SHARPE a general selector pair? (cloud, 2026-09-09)

**INDEPENDENT REPLICATION.** Lane B answered idea 270 in the same session (`..._B.py`, 5 dials x
12 panels, 348 arms). This run was claimed and executed independently on a different design (6
dials x 3 panels x 2 cost rungs, 174 arms) and is filed as a replication, not a new answer. It
**agrees on the verdict and contradicts two of lane B's structural readings** — which is itself
the finding.

**Verdict: the queue's premise REFUTED, second time independently. The disagreement is real but
a minority event; the +CAGR/-Sharpe EXCHANGE is not a constant, not general, and on this grid not
even reliably signed. Neither selector beats doing nothing. No KEEP claimed, no memo, no RULES
change; RULES.md, scan.py, bot.py, baseline.py and PROTOCOL.md untouched.**

Script `2026-09-09_is-S_CAGR-vs-S_SHARPE-a-general-selector-pair_cloud.py`; outputs `.arms.csv`
(174 rows, ALL grid points), `.cells.csv` (36 rows), `.console.txt`. Rule 8 throughout: both
selectors see the FIRST half only, every number below is the untouched SECOND half. 10 bps
headline with a 25 bps rung beside it, weekly (except on the cadence dial), next-day execution.
Runtime 461 s.

## Design

Dials (one tuned parameter each, plus the one companion constant the book form needs, held at the
live value): `n` in {5,10,20,30,50} (composite-ranked, above MA200, EW, gross 0.75); `band` in
{0.00,0.01,0.03,0.05,0.08,0.12} (RULES v2); `gross` in {0.25,0.50,0.75,1.00}; `volcap` in
{0.30,0.45,0.60,0.90,inf}; `quantile` in {0.10,0.25,0.50,0.75,1.00}; `cadence` in {D,W,M,Q}.
Panels U56 / broad136 / SMALL439. Comparands on the same OOS window: RULES v2 (live), RULES v1,
SPY, and EWALL (every priced name equal-weighted at the dial's gross — the do-nothing control).

## Result

**Disagreement is a minority event: 11 of 36 cells (30.6%)** — 7/18 at 10 bps, 4/18 at 25 bps.
Lane B got 12/60 (20%). Both refute "the selectors are interchangeable".

**Which dial disagrees does NOT replicate.** Here: cadence 4/6, volcap 3/6, band 2/6, n 2/6,
gross 0/6, quantile 0/6. Lane B: n 7/12 (58.3%) against 1/12 for cadence. Two independent designs
put the disagreement on different dials, so "it is an n-dial phenomenon" does not survive a
change of panel set and cost rung. `gross` and `quantile` disagreeing zero times is mechanical:
Sharpe and CAGR are monotone in the same direction along both.

**The exchange rate is not a constant, and here not even reliably signed.** Per-cell pp of OOS
CAGR per point of OOS Sharpe over the 11 disagreeing cells: **-48.0, -9.4, -4.2, +1.0, +12.9,
+16.3, +16.9, +19.8, +22.8, +45.0, +73.7** — three cells carry the opposite sign. The shape idea
259 named (+CAGR, -Sharpe) holds in only **3 of 11** cells; **6 are free lunches** (both metrics
better) and 2 are both-worse.

**Lane B's invariant denominator does not reproduce.** Lane B reports dOOS Sharpe homogeneous at
~-0.014 (permutation p 0.31). Here dOOS Sharpe on disagreeing cells is **median +0.0073, mean
+0.0769 (t +1.65), positive in 6 of 11**; excluding the one SMALL439/volcap outlier it is median
+0.0029, mean +0.0388, positive in 5 of 10. dOOS CAGR is **median +0.54 pp, mean +1.49 pp
(t +2.14), positive in 9 of 11** — the CAGR leg is the one that replicates in sign, matching lane
B's census direction (+0.63 pp) and idea 259's +2.53 pp. Choosing on CAGR buys CAGR; that it
costs Sharpe is not established on this grid.

## Neither selector earns its keep (OOS, mean over 36 cells)

| | S_SHARPE | S_CAGR | EWALL (do nothing) | RULES v2 (live) | SPY |
|---|---|---|---|---|---|
| OOS Sharpe | 0.7814 | 0.8049 | **0.8956** | 0.8911 | 0.8401 |
| OOS CAGR | 7.47% | 7.92% | **12.23%** | 6.54% | 15.26% |

S_SHARPE beats the EWALL control in **7 of 36** cells, S_CAGR in **7 of 36** (mean deficits
-0.1142 and -0.0907 of Sharpe). Both beat the mean arm (24/36 and 25/36) — selection beats a
random arm and loses to not selecting at all. Another idea-229 instance, agreeing with lane B.

## KEEP paths (all 174 arms, protocol judgement, both cost rungs)

**4b 14/174**, every one an already-known shape: U56 `n` 20/30/50, `gross` 1.00, `volcap` 0.90/inf,
`quantile` 0.75/1.00 at 10 bps (plus U56 `gross` 1.00 surviving 25 bps), and broad136 `gross` 1.00,
`volcap` 0.60/0.90/inf, `quantile` 1.00 at 10 bps. All are the open-eligibility, full-gross
equal-weight book — the 4b path selecting exposure, not a rule. **Only 1 of the 14 survives 25 bps.**
Selected arms: S_SHARPE 4b 8/36, S_CAGR 4b 8/36.

**4a 2/174** — SMALL439 `band` 0.05 at 10 bps (4.18%/0.6183/-14.6%, halves 0.6385/0.6031 against
RULES v2's 3.81%/0.5725/-14.7%, halves 0.5699/0.5770) and at 25 bps. **NOT filed as a KEEP
candidate and no memo written**: the Sharpe curve is monotone in `band` out to the widest point
tested (0.08 -> 0.6286, 0.12 -> 0.6520, both above the 0.05 arm in both halves), so idea
240/256/328's grid-edge flag applies, and 0.05 "passes" only because 0.08 and 0.12 breach the
MaxDD leg by 0.2-1.3 pp. It is one panel, the panel the live book does not trade, and the margin
over v2 is +0.046 of Sharpe. Reported for the record, not proposed for adoption.

## Caveats

SURVIVORSHIP: broad136 and SMALL439 are current constituents only (SMALL439 = the 483-name
sub-$2B panel with the 44 tickers whose `max_1d_move >= 1.0` dropped first, per
`data/small_meta.csv`). The IS/OOS split is the sample midpoint, not lane B's 2009-2016 /
2017-2026 calendar split; on the small panel the windows therefore differ from theirs. 36 cells
is a small denominator for a heterogeneity claim — the contradiction with lane B is reported as a
non-replication, not as a refutation of their permutation test.

## Proposed follow-ups

1. Run both designs' dial sets on ONE panel set to isolate whether the n-vs-cadence ordering is
   panel-driven or dial-parameterisation-driven.
2. Price the 6 free-lunch cells against their own EWALL control before anyone calls them free.
3. Re-read the SMALL439 band ladder with the DD cap removed, to check how many published 4a
   passes are grid-edge points held in place by the MaxDD leg alone.

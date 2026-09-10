# Idea 498 — is p/n = 1 the crossover for key reproduction? (cloud, 2026-09-10)

**KILL — REFUTED as pre-registered, and refuted in both directions: p/n = 1 is not the crossing,
and p/n is not the axis.** Nothing promoted, no RULES change; RULES.md, PROTOCOL.md, scan.py,
bot.py, baseline.py untouched.

Corpus: 900 equal-weight 20-name draw books per panel (2,700 books), 10 bps, weekly, t+1, idea
483's seeds. Object: `REPRO_OOF` = the out-of-fold R² of a ridge on the membership matrix M
predicting the control's **own key**. Tuned exactly two as the queue allows — DRAWS n (12 rungs
30…900, nested prefixes of one pool) × p (column subsets 10…full panel) — **all reported**. lam
(6), K (4), target, panel, cost rung and sample half are reported axes, never tuned; the headline
cell was pre-registered as **lam = 1.0, K = 10, p = full panel, target = sd** before any number
was read.

**GATES.** G1 sub-panel backtest == whole-panel backtest, 8 books × 3 rungs, **6.94e-17**;
G1b the derived cost ladder `r(c) = r0 − turnover·c/1e4` == a live costed backtest, **0.00e+00**;
G4 `mn` is exactly linear in M, **0.00e+00**; G5 fast metrics vs `engine.metrics`, **2.22e-16**;
G3 reproduces the queue's quoted triple exactly.

**G2 is reported SPLIT, per idea 591's precedent, because one panel's price file is live and two
are frozen.** G2a PROVENANCE on B136 + SMALL439 (96 committed rows): **5.51e-12**, bar 1e-9 —
the machinery is idea 483's exactly, to machine precision. G2b VINTAGE on U56 (48 rows):
**5.27e-02** — not a machinery difference. U56 is served by `data/prices.csv`, which the daily
job appends to (it now runs to 2026-09-09 against B136/SMALL439's 2026-09-04), so U56's `ann` and
every U56 book Sharpe shift slightly. It moves no published number at its published precision:
G3 reproduces U56's headline median to 4dp **on this vintage**, and no verdict below rests on a
U56 quantity read to better than 1e-3.

**Two provenance corrections for the record.** (i) The queue's triple 0.939 / 0.668 / 0.315 is
idea 483's **median over its own 6 lam × 4 K grid** at WIDE and n = 200, not a single cell — its
per-panel **max** is 0.9545 / 0.8772 / 0.4546 and its **min** is 0.2681 / −0.5237 / 0.0166. A
statistic whose grid spans −0.52 to +0.88 was published as one number. (ii) Idea 483's NARROW10
subset is the 10 most-drawn names **in its own 200-draw M**; that is a different set of names from
the 10 most-drawn in a 900-draw pool, so its rows only join when the subset is rebuilt at n = 200.

## Q1 — the queue's test: REFUTED

At the pre-registered headline, the crossing where honest reproduction of `sd` falls below 0.50:

| panel | p | crossing n* | **p/n\*** | REPRO_OOF at n=900 | at n=30 |
|---|---|---|---|---|---|
| U56 | 55 | 43.7 | **1.257** | +0.9694 | +0.1047 |
| B136 | 135 | 73.3 | **1.843** | +0.9645 | −0.2799 |
| SMALL439 | 439 | 218.8 | **2.006** | +0.9483 | +0.1319 |

Two of three sit outside the CONFIRMED band [0.75, 1.333] and SMALL439 sits outside the PARTIAL
band [0.50, 2.00] as well. Over the full reported lam × K grid, 66 of 72 cells cross at all and
**p/n\* spans 0.122 to 2.031** (median 1.267; per panel 0.955 / 1.234 / 1.880). There is no single
crossing constant to publish.

## Q1b — an independent lane ran the same idea the same day, and its fix works on this grid

Lane B (`..._B.py`) executed idea 498 concurrently and reached the same verdict from a different
grid (16,128 points to this run's 9,216): p/n = 1 is not the crossover and p/n is not sufficient.
It went one step further and named the denominator — **n_train, not n** — which explains a
pattern this run's lam × K table shows but did not account for: my crossings read ~0.74 at K = 2
and ~1.28 at K = 10, and a K-fold ridge fits on n(K−1)/K rows, not n.

Rescaling this run's own 66 crossing cells by K/(K−1) reproduces lane B's result independently:

| statistic | median by K (2 / 5 / 10 / 25) | max/min across K |
|---|---|---|
| p/n\* (as published above) | 0.740 / 1.327 / 1.284 / 1.437 | **1.943x** |
| p/n_train\* | 1.480 / 1.659 / 1.426 / 1.497 | **1.163x** |

Lane B measured 1.792x → 1.195x on its grid; this run gets 1.943x → 1.163x on a different one.
The pooled median moves 1.267 → **1.491**, and the share of cells within ±20% of a constant is
0.106 for 1.0 against **0.424** for 1.7 — so the better denominator does not rescue p/n = 1, it
refutes it further while making lane B's ~1.7 the defensible constant. At the pre-registered
headline the three panels read p/n_train\* 1.397 / 2.047 / 2.229.

This is corroboration, not confirmation of a shared assumption: the two runs share idea 483's
seeds and book construction but differ in draw pool (900 vs its own), p ladder, n ladder, key set
and crossing estimator, and neither lane saw the other's numbers before committing.

## Q2 — p/n is not the axis, and this is the load-bearing result

At **identical p/n = 0.8889**, REPRO_OOF runs from **−0.7533** (B136, p=40, n=45) to **+0.7133**
(SMALL439, p=320, n=360) — a spread of 1.47 at the same p/n, and monotone in p, which is the
opposite of what a p/n law permits. The worst within-band spread over the grid is **1.9641**
against a whole-grid range of −1.3015 to +0.9694: the band tells you almost nothing.

Low p/n is **not sufficient** either. At n = 900 the narrow designs never become honest:

| panel | p | p/n at n=900 | REPRO_OOF |
|---|---|---|---|
| B136 | 10 | **0.011** | −0.0002 |
| B136 | 20 | 0.022 | +0.0058 |
| SMALL439 | 80 | **0.089** | −0.0692 |
| SMALL439 | 160 | 0.178 | +0.1901 |

A control 90× narrower than its row count still cannot reproduce its own key. Seven of the
sub-full-panel (panel, p) curves are `never_above` — they do not cross at **any** n on the
ladder. **A narrow control is never a control, at any p/n.**

## Q3 — and the failure is not the nonlinearity

`mn` (the mean of member annualised returns) is **exactly** linear in M, verified at 0.00e+00.
If `sd`'s failure were its nonlinearity, `mn` would be reproduced where `sd` is not. It is not:
the two curves track each other cell for cell (U56 n=45: sd +0.5298 vs mn +0.5374; n=60: +0.8281
vs +0.7847) and the crossings sit on top of each other — **sd 1.257 / 1.843 / 2.006 against mn
1.287 / 1.764 / 1.605**. The exactly-linear control fails in the same places and by the same
amounts. So the honest statement is about rows and design coverage, not about what shape the key
is.

## Q4 — rule 8

Key rebuilt on the first half of each panel's sample alone, crossing located there, second half
read once. A crossing exists in **both halves on 3 of 3 panels**, but its *value* does not
travel: H1 → H2 is 1.524 → 1.320, 3.234 → 1.974, 1.184 → 2.087 (ratios 0.866 / 0.610 / **1.763**,
|H2 − H1| up to 1.260 in p/n units). Existence walks forward; the constant does not. The
book-level selector chooser beats RULES v2 OOS on 5 of 12 panel × selector cells and SPY on 5 of
12, with the in-sample-residual and out-of-fold-residual selectors picking the identical book in
all three panels.

## Q5 — PROTOCOL, both KEEP paths

All 2,700 books at 0 / 10 / 25 bps: **4a 0 / 0 / 0 and 4b 0 / 0 / 0, BOTH 0.** Unfiltered random
20-name books carry no gate and no sleeve, so this is the expected floor and is reported as such,
not as a finding; the binding leg is DD on 1,639 of the 2,700 cells at 10 bps. Reference at 10
bps — RULES v2 (live) U56 8.63% / 1.2021 / −12.05%, B136 8.03% / 1.1058 / −12.24%, SMALL439 3.81%
/ 0.5725 / −14.68%; SPY 15.15% / 0.8855 / −33.72%; mean draw book 17.86% / 1.1297 / −29.14%,
18.88% / 1.1216 / −32.68%, 13.13% / 0.6773 / −46.33%.

## What should be published instead (a proposal for Sunday review, not adopted here)

The record should stop quoting a control's honesty as a p/n number. Two statements survive this
run and both are cheap to compute:

1. **At the full panel** the crossing is roughly a constant multiple of p, but the constant is
   **≈ 1.7, not 1**, and it should be read against **training rows**: `p/n_train* ~ 1.7`, which
   both lanes reach independently (Q1b). A wide control needs roughly `n_train ≳ 1.7p`.
2. **Below the full panel the p/n framing collapses**: coverage governs, and a control that spans
   a small share of the panel never reproduces its key however many rows it is given. Any
   published residualisation should carry `p`, `n` **and** `p/P`, plus its own out-of-fold
   `REPRO_OOF` — which is the one number that answers the question directly and costs one
   K-fold fit.

**SURVIVORSHIP.** All three panels are current-constituent screens, so every CAGR and drawdown
level above is optimistic; SMALL439 is 439 sub-$2B names that exist today (44 dropped for
max_1d_move ≥ 1.0 per `data/small_meta.csv`), starting 2010-01-04. The object of this run is a
within-panel reproduction R² between a design and its own key, which a common level shift does
not move; the cross-panel readings inherit whatever differential the three screens carry, and
Q1's within-panel n sweep at fixed p is the control offered against that.

Script `research/backtests/2026-09-10_is-p-over-n-1-the-crossover-for-key-reproduction_cloud.py`;
outputs `.grid.csv.gz` (9,216 points), `.crossings.csv`, `.lamK.csv`, `.walkforward.csv`,
`.selectors.csv`, `.keeppaths.csv.gz`, `.refs.csv`, `.console.txt`.

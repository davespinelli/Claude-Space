# idea 213 — publish-the-cash-carve-out-beside-every-sleeve-MaxDD (lane C, 2026-09-06)

**VERDICT: KILL of the drawdown half of the sleeve claim, across the whole recoverable record.
Of 615 published sleeve arms that improve their own book's MaxDD, 72 (11.7%) beat a matched-f
cash carve-out at all, 1 (0.16%) keeps more than a quarter of the gain from it, and 0 keep half.
The best surviving claim in the record still hands 82.4% of its drawdown gain to cash.**

Script: `research/backtests/2026-09-06_publish-the-cash-carve-out-beside-every-sleeve-MaxDD_C.py`
(console, `.backfill.csv` 744 arms, `.census.csv` 563 rows, `.survival.csv`, `.keep.csv`,
`.walkforward.csv` alongside).  1224 backtests, deterministic, no network.

## The control

For every published sleeve arm `(1-f) x EQUITY + f x SLEEVE` whose own `f=0` control is
published beside it, idea 190's control is re-derived:

    CASH-f  =  (1-f) x (that arm's own f=0 weights), not rescaled.

Same book, same cadence, same cost, same trade dates — the sleeve leg replaced by cash.
`dD = |MaxDD_base| - |MaxDD_arm|`, `retention = dD_cash / dD_sleeve`.  A claim **survives at
bar b** iff `dD_sleeve > 0 and retention < b`.  A second control, **CASH-GM**, scales the base
to the sleeve arm's own realised mean gross (idea 135's matched-mean-gross control), so the
two together separate "the sleeve is an exposure cut" from "an exposure cut you could have
taken for free does as well".

Tuned parameters: exactly two — the control convention {CASH-f, CASH-GM} and the bar
b in {1.00, 0.75, 0.50}.  Both swept, all six grid points reported, neither selected on.
Panels, books, sleeve sets, f and cost rungs are inherited from the parents.

## Reproduction, before any control was read

| check | result |
|---|---|
| [a] vectorised simulator vs `engine.backtest` (u56/R20 @10bps) | max\|dret\| **1.388e-17** PASS |
| [b] A/idea190, 72 arms x CAGR/Sharpe/MaxDD vs its `.grid.csv` | **2.220e-16** PASS |
| [b] B/idea134, 48 arms | **4.718e-16** PASS |
| [b] C/idea105, 192 arms | **1.055e-15** PASS |
| [b] D1/idea103c and D2/idea103b, 96 arms each | **1.055e-15** PASS |
| [b] E/idea018, 48 arms | **6.661e-16** PASS |
| [b] F/idea106, 192 arms | **1.110e-15** PASS |
| [b] G/idea015 (crypto), 72 arms | dMaxDD 4.8e-06 but dSharpe **4.2e-03** — FAIL |
| [b] H/idea014 (rsi2), 36 arms | dMaxDD 1.9e-03, dSharpe **4.3e-03** — FAIL |
| [d] truncation probe over ALL rows of G and H (the simulator is causal, so a parent that ran on a shorter panel is a strict prefix) | best 3.798e-03 (G) / 2.099e-03 (H) — **does NOT collapse, so it is not sample extension; both parents DROPPED** |
| [c] CASH-f as defined here vs idea 190's own 36 committed cash rows | **2.220e-16** PASS |

The control itself therefore reproduces its parent exactly; nothing below rests on a
re-implementation of it.

## Coverage — what could and could not be back-filled

563 LEADERBOARD rows mention a sleeve.  366 (65.0%) come from a script that committed a grid
CSV; adapters were written for 332 (59.0%); after reproduction the admitted corpus is **98
LEADERBOARD rows = 744 published sleeve arms from 7 parents** (a leaderboard row summarises a
whole grid, so the arm count is the honest denominator).  Left unbacked:

* **234 rows** — `crypto-sleeve_C` (156) and `rsi2-sleeve_cloud` (78).  Both ran 2026-09-04 and
  neither re-derives on today's `data/prices.csv`; truncation does not explain the gap, so the
  panel they ran on is gone.  For crypto, MaxDD alone reproduces to 4.8e-06, so its retention
  is printed as a **labelled appendix and excluded from every headline count** (3 claims,
  median retention 2.491).
* **197 rows** — scripts that committed no grid CSV at all (`defensive-sleeve_cloud` 140,
  `core-sleeve-walk-forward-repair_B` 22, `core-plus-trend-sleeve` 8, and a long tail).
  These cannot be back-filled without re-running the parent.

That 65%/35% split is itself a finding: a third of the record's sleeve claims are not
auditable from what is committed.

## The result

**615 of 744 arms (82.7%) make a drawdown claim.**  Against the matched-f cash carve-out:

| control | bar 1.00 | bar 0.75 | bar 0.50 |
|---|---|---|---|
| **CASH-f** | 72 / 615 (**11.7%**) | 1 / 615 (**0.16%**) | 0 / 615 (**0.00%**) |
| CASH-GM | 613 / 615 (99.7%) | 610 (99.2%) | 600 (97.6%) |

* median CASH-f retention **1.347**, mean 2.361; cash is **strictly better than the sleeve in
  88.3%** of claims.  Counting the duplicated D1/D2 corpus once: 523 claims, median 1.294,
  86.2%.
* the two controls disagree completely, and that is the mechanism: **CASH-GM retention is
  -0.000 (median) under a gross-matched blend and +0.256 under a natural one**.  Holding the
  book's gross fixed and swapping the mix buys nothing; taking the same fraction OUT of the
  book buys almost all of it.  The claim that survives is never "these assets diversify" — it
  is "hold less equity", and the record priced that as an asset choice.
* by parent (median retention): A/idea190 **0.984**, B/idea134 **1.003**, F/idea106 1.346,
  C/idea105 1.574, D1=D2/idea103 1.900, E/idea018 2.187.  **Idea 190's own 98.4% was the most
  favourable corpus in the record**; on 7x the arms the effect is stronger, not weaker.
* by f: 0.954 / 0.977 / 0.962 at f = 0.10 / 0.15 / 0.20, then 1.244 / 1.229 / 1.477 / 2.279 at
  f = 0.25 / 0.50 / 0.75 / 1.00.  Not monotone at the low end (P3 MISS): the only zone where a
  sleeve beats cash on drawdown at all is **f <= 0.20 on a gross-matched blend**, and even
  there it beats it by 2-5% of the gain.
* Sharpe is a different story and is reported beside it: mean dSharpe vs base **+0.0064 for the
  sleeve vs -0.0013 for cash**, sleeve better in 71.2% of claims; mean dCAGR **-3.61% vs
  -6.11%**.  The sleeve is not worthless — its DRAWDOWN evidence is.

### What this does to 4b

538 of 744 sleeve arms pass 4b's drawdown cap.  **536 of those 538 (99.6%) have their own
matched-f cash control passing the same cap**, and **339 (63.0%) have their f=0 base already
passing it**.  Full 4b: sleeve 116, CASH-f 54; 4a: sleeve 435, CASH-f 420.  Crossing the two,
**20 arms both pass 4b and beat their cash control — every one of them at retention 0.82-0.997**.
The single best is `u56 / R40 + S3 / f=0.10 / 10 bps`: 12.89% / 1.1885 / -19.13% against a cash
control at -19.56%, i.e. **the strongest sleeve drawdown claim the record can support is worth
0.43pp of MaxDD**.  No KEEP-candidate is proposed on that.

### Rule 8 (PROTOCOL 8) — 68 cells, f* and sleeve* chosen on 2009-2016 IS Sharpe only

| arm (mean over 68 cells) | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|
| SLEEVE (IS pick) | 8.76% | **1.0820** | -12.31% |
| CASH-f at the same f | 6.27% | 0.9660 | **-10.33%** |
| CASH-GM | 12.21% | 0.9573 | -19.97% |
| BASE (do nothing) | 12.23% | 0.9573 | -20.06% |
| RULES v1 | 6.03% | 0.5910 | -18.05% |
| SPY | 15.45% | 0.8820 | -33.72% |

Paired **SLEEVE - CASH-f: dSharpe +0.1204 (t +10.78, 63/68 wins) but dMaxDD +1.98pp DEEPER
(t +6.01; the sleeve is shallower in only 7 of 68 cells)**.  Paired SLEEVE - BASE: dSharpe
+0.1247 (t +11.08), dMaxDD -7.75pp (t -18.39).  68 of 68 cells show the sleeve improving OOS
drawdown over its own base; **of those the sleeve still beats the cash control in 10.3%**, and
\|dOOS MaxDD\| is under 2pp in 69.1% of cells.  Out of sample the sleeve's whole drawdown
advantage is the exposure cut, and what it does add — Sharpe — is exactly the thing the
record attributes to it least often.  Note the level: the IS-picked sleeve beats SPY's OOS
Sharpe on average but runs at 57% of SPY's CAGR, below 4b's 70% floor.

## Predictions (pre-registered in the script header, scored)

| | prediction | outcome |
|---|---|---|
| P1 | median CASH-f retention >= 0.75 | **HIT** — 1.347 |
| P2 | retention >= 1 commoner under the natural convention | **HIT** — 98.1% vs 83.1% |
| P3 | retention rises with f | **MISS** — flat-to-falling below f=0.20, rising above |
| P4 | >= 50% of DD-cap passers have CASH-f passing too | **HIT** — 99.6% |
| P5 | \|dOOS MaxDD\| < 2pp in a majority of cells | **HIT** — 69.1% |

P3's miss is the informative one: it locates the only region (f <= 0.20, gross-matched) where a
sleeve's drawdown claim is not simply an exposure claim, and shows the margin there is a few
percent of the gain rather than a difference in kind.

## Proposed to the Sunday review (report-only; no RULES change)

> **PROTOCOL clause 11f.**  Any published claim that an overlay, sleeve or blend improves a
> book's drawdown must be quoted beside a matched-f cash carve-out — `(1-f)` times that book's
> own un-overlaid weights, same cadence, same cost, same trade dates — and must state the
> retention `dMaxDD_cash / dMaxDD_overlay`.  Where the blend is gross-matched, the
> matched-mean-gross control must be quoted too, since the two disagree by construction.  A
> drawdown claim with retention >= 1.00 is an exposure claim and must be worded as one.

Nothing in `RULES.md`, `scan.py`, `bot.py` or `baseline.py` was touched.

## Caveats carried

* Survivorship: u56/broad are current-constituent lists (idea 54); the equity leg is inflated
  more than the ETF sleeve, which biases retention **downward** — a high retention here is the
  conservative reading.
* Idea 128: the IS window cannot express a deep drawdown, so any IS drawdown screen is loose.
* Ideas 223/182B: MaxDD is sensitive to the trade-date anchor.  Every arm here is quoted at its
  parent's own anchor and the cash control shares it, so the RATIO is far less anchor-exposed
  than either level, but the levels are single draws.
* Idea 126: t+1 execution throughout.
* D1/D2 are the same corpus in two lanes; the de-duplicated figures are printed beside the
  pooled ones and move nothing (median 1.294 vs 1.347).

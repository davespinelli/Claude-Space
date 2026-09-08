# Idea 137 — is broad@25bps a TURNOVER wall or an H2-REGIME wall? (cloud, 2026-09-07)

Script: `2026-09-07_broad-25bps-is-the-wall_cloud.py`
Outputs: `.console.txt`, `.grid.csv` (1,680 arm-rows), `.decomp.csv`, `.matched.csv`, `.walkforward.csv`, `.keeppaths.csv`
Run launched 2026-09-07 UTC; finished just after the 09-08 UTC rollover.

## Verdict — SPLIT. The wall is **REGIME**, not turnover — and the wall is **not a wall**, it is idea 134's arm set.

Two answers, and the second one is the more useful:

**(1) The queue's question, answered: REGIME.** Holding turnover fixed across panels does **not**
save broad. 82–84% of the u56-minus-broad gap at 25 bps is already present at **zero cost**.

**(2) The premise is scoped, not general.** Idea 134's "0 of 442 arm-rows at broad@25bps" is
reproduced *for its own corpus* (ranked/R20 base, weekly cadence: 0/221 @25 bps in its committed
grid). Opened onto the cadence and partial-rebalancing dials, **broad@25bps clears 4b in 46 of 112
rows** here (u56 43/112, small 0/56). The wall is a property of the *ranked base book at weekly
cadence*, not of the panel-at-25-bps.

## The wall, reproduced (weekly, λ=1, the book idea 134 priced), 25 bps

| panel | book | turnover | CAGR | Sharpe | MaxDD | H1 | H2 | OOS Sharpe | worst-of-5 margin | binding | 4b |
|---|---|---|---|---|---|---|---|---|---|---|---|
| u56 | TOP20+S3 f=0.25 | 8.89x/yr | 11.41% | **1.0951** | −17.21% | 1.189 | **1.029** | **1.086** | **+0.0075** | CAGR | **PASS** |
| broad | TOP20+S3 f=0.25 | 12.13x/yr | 10.43% | 0.8858 | −19.07% | 1.049 | **0.760** | **0.833** | −0.0741 | **H2** | FAIL |
| SPY (both) | — | — | 15.23% | 0.8890 | −33.72% | 0.957 | 0.834 | 0.882 | — | — | — |

The turnover figures match the queue's (12.2x broad vs 8.8x u56) and the binding bar is H2, as
idea 134 said. Idea 134's named "best member H2 0.791 / OOS 0.861" sits close to this row's
0.760 / 0.833 (a different arm from its menu).

## D1 — exact cost decomposition (gate: derived r(25 bps) vs simulated, **max|d| 0.000e+00**)

With no state machine active, holdings and turnover are cost-independent, so every rung reads off
one simulation and `gap(25) = gap(0) + cost-response` is an identity, not a fit.

| metric | gap(0 bps) | gap(25 bps) | cost term | REGIME share |
|---|---|---|---|---|
| Sharpe | +0.0637 | +0.0765 | +0.0128 | median **0.852** |
| H1 | −0.0283 | −0.0172 | +0.0111 | median 0.961 |
| **H2** | **+0.1431** | **+0.1572** | +0.0142 | median **0.972** |
| OOS Sharpe | +0.1254 | +0.1400 | +0.0147 | median **0.964** |

(means over all 112 (book, f, λ, cadence) cells). On idea 134's own reference book
(TOP20, f=0.25, weekly, λ=1): Sharpe gap 0.1709 → 0.2093, H2 gap **0.2271 → 0.2694**, OOS gap
0.2100 → 0.2531 — i.e. **82% / 84% / 83% of the gap is regime, 18% / 16% / 17% is cost.**

## D2 — matched turnover (the queue's own instruction). T* = u56's own weekly/λ=1 turnover.

Broad is dialled onto u56's turnover along (cadence, λ) and read at 25 bps:

| book | panel | native turnover | native Sharpe / H2 / OOS | matched at | matched turnover | Sharpe / H2 / OOS | worst-of-5 | 4b |
|---|---|---|---|---|---|---|---|---|
| TOP20 f=0.25 | u56 | 8.89 | 1.0951 / 1.029 / 1.086 | W, λ=1 | 8.89 | 1.0951 / 1.029 / 1.086 | +0.0075 | PASS |
| TOP20 f=0.25 | broad | 12.13 | 0.8858 / 0.760 / 0.833 | W, λ=0.35 | 9.28 | **0.9704 / 0.821 / 0.898** | **−0.0127 (H2)** | **FAIL** |
| TOP20 f=0.00 | broad | 13.18 | 0.8460 / 0.732 / 0.807 | D, λ=0.10 | 9.06 | 0.9646 / 0.796 / 0.876 | −0.0583 (DD) | FAIL |
| TOP20 f=0.00 | small | 16.26 | 0.6491 / 0.613 / 0.696 | W, λ=0.15 | 9.68 | 0.6513 / 0.544 / 0.642 | −0.3139 (H2) | FAIL |

Across the four broad cells: 4b passes **1/4 matched vs 1/4 natively** (the one pass is idea 139's
EWall+S3 f=0.25 book, which already passes). Matching turnover buys broad **+0.053 Sharpe,
+0.037 H2, +0.039 OOS** and moves its worst-of-five margin from **−0.055 to −0.028** — a real
recovery of roughly 40% of the Sharpe gap, and **it does not cross zero.**

## D3 — matched cost drag (changes nothing about the book, only its price)

Giving broad the rung that equates turnover × bps (c* = 25 × to_u56 / to_broad):

| book | panel | turnover | c* | Sharpe @25 → @c* | H2 | OOS | worst-of-5 |
|---|---|---|---|---|---|---|---|
| TOP20 f=0.25 | broad | 12.13 | 18.3 bps | 0.8858 → **0.9536** | 0.8220 | 0.8963 | **−0.0171** |
| TOP20 f=0.00 | broad | 13.18 | 17.2 bps | 0.8460 → 0.9140 | 0.7958 | 0.8712 | −0.0675 |
| TOP20 f=0.00 | small | 16.26 | 13.9 bps | 0.6491 → 0.7367 | 0.6934 | 0.7798 | −0.1643 |
| TOP20 f=0.25 | u56 | 8.89 | 25.0 bps | 1.0951 (unchanged) | 1.0294 | 1.0862 | **+0.0075** |

Two independent equalisations, same answer: **broad still fails, and it fails on H2.**

## D4 — the H2 regime, read at zero cost

SPY bars are identical on u56 and broad (same benchmark, same window): H1 0.9566 / H2 0.8340 /
OOS 0.8820. At **0 bps**, weekly, λ=1, the H2 margin over SPY is:

| book | u56 | broad | small |
|---|---|---|---|
| EWall f=0.00 | +0.2450 | +0.1972 | −0.2335 |
| EWall f=0.25 | +0.3481 | +0.3057 | n/a |
| TOP20 f=0.00 | +0.3355 | **+0.1012** | −0.0640 |
| TOP20 f=0.25 | +0.3848 | **+0.1577** | n/a |

Broad's ranked book enters the cost question with roughly **a third of u56's H2 cushion**, before a
single basis point is charged. That is the wall.

**The one honest tension, stated rather than buried:** at the *bar* level the arithmetic points the
other way. Of the 4b bars that fail on broad at 25 bps (weekly, λ=1), only **2 of 7 (28.6%)** already
fail at 0 bps — cost flips the other five. On u56 it is 2 of 2 (100%), on small 6 of 8 (75%). Both
readings are true and they are not in conflict: broad sits far below u56 for regime reasons at every
cost, and the last 16–18% of cost drag is what pushes specific bars from just-above to just-below.
This is precisely the thin-margin phenomenon idea 401 measures on the same day — **a large regime gap
plus a small cost increment, with the published verdict decided by the increment.**

## Rule 8 (PROTOCOL 8) — (cadence, λ) chosen on IS 2009-2016 by IS Sharpe @25 bps, OOS read once

| | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|
| IS-chosen (cadence, λ) | — | **1.0457** | — |
| control (weekly, λ=1) | — | 0.9680 | — |
| RULES v2 (live) @25 bps, u56 / broad / small | 9.24% / 7.64% / 3.39% | 1.2483 / 1.0740 / 0.5056 | −12.24% / −12.28% / −15.27% |
| SPY | 15.45% | 0.8820 | −33.72% |

Premium over the do-nothing control **+0.0778, positive in 8 of 10 cells**, regret 0.0205. The chooser
picks a cadence slower than weekly in 8 of 10 cells (M in 6, Q in 2; W once, D once) and λ<1 in 6 of
10 — consistent with turnover mattering *at the margin* while not deciding the panel gap. Full 4b (which includes the OOS bar) holds for the IS-chosen
setting in **4 of 10** cells: u56 2/4, broad 2/4, small 0/2. Both broad passes are f=0.25 books.

## KEEP paths

1,680 arm-rows. **4b: 562** (broad 46/112 and u56 43/112 at 25 bps; small **0/336** at every rung).
**4a against the LIVE RULES v2 book, cost-matched: 0** — every book here runs −18% to −35% MaxDD
against v2's −12%, so 4a's no-regression-on-drawdown clause is unreachable. **BOTH: 0.** (4a against
v1 for continuity: 675.) **No new book, no new KEEP, no RULES change.**

By-product, weakness first: broad/EWall + 25% S3 sleeve at **λ=0.35 weekly, 25 bps** gives OOS Sharpe
**1.1804** against the unsmoothed 1.1616 — but λ smoothing is a third instrument on a book that is
already idea 139's standing candidate (blocked on ideas 105/106/395), the gain is +0.019 of Sharpe,
and it is an IS-chosen setting. Not promoted, recorded only.

## Reproduction gates (run before any new number)

- `H.run` vs `engine.backtest`, EWall weekly, u56: **0.000e+00**.
- Derived `r(25 bps) = r_gross − turnover×25/1e4` vs a simulated 25 bps run: **0.000e+00** — the D1
  identity is exact, not approximate.
- Idea 138's committed grid, 16 shared rows: broad **2.220e-16**, u56 **8.909e-06**; `pass4b`
  agreement **16/16**. The u56 drift is `data/prices.csv` having been rewritten by the
  `Daily close 2026-09-07 [actions]` commit (vendor restatement of adjusted closes) while
  `data/prices_broad.csv` was not touched — see idea 401's result for the same finding.

## Caveats

- **SURVIVORSHIP (idea 54):** three current-constituent panels; the small panel is a sub-$2B screen
  run today and back-filled to 2010 (`max_1d_move >= 1.0` tickers dropped, idea 118). It flatters
  low-turnover, buy-and-hold settings — **exactly the end of the dial D2 moves toward** — so a
  negative matched-turnover result is understated, not overstated.
- **λ smoothing is an instrument as well as a turnover dial**: it changes the book's path, not only
  its trading. D3 exists precisely because it changes nothing about the book at all, and the two
  equalisations are read together; they agree.
- Idea 38 (u56/broad calendar-day index) and idea 126 (t+1 only, no lag band) carry forward.

## Follow-ups proposed

410. `re-scope-idea-134-s-wall-in-the-record` — "broad@25bps admits 0 of 442" is true of a ranked-base
     weekly corpus and false of the panel (46/112 here). Census every published "the panel/rung admits
     nothing" claim for the same over-generalisation.
411. `is-H2-cushion-a-publishable-panel-column` — broad's ranked book enters at a third of u56's
     zero-cost H2 margin, which predicts its 4b failure better than its turnover does. Test H2-cushion-
     at-0-bps as a screening column across panels, against turnover as the incumbent predictor.
412. `does-partial-rebalancing-beat-cadence-as-the-turnover-dial` — the IS chooser picks slower cadence
     in 7 of 10 cells but λ<1 in 5; price the two dials against each other at matched realised turnover,
     since only one of them changes the book's path.

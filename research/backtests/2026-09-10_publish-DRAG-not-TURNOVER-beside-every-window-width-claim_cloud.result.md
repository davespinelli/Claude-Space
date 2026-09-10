# Idea 613 — publish DRAG, not TURNOVER, beside every window-width claim  (cloud, 2026-09-10)

**VERDICT: SPLIT — the census PREMISE is CONFIRMED and larger than the queue supposed, 403's
SLOPE and LEVEL both REPLICATE on a third panel and a second sleeve, and the queue's own
PRESCRIPTION is KILLED at the record's published rung pair.  No KEEP, no book promoted, no memo,
no RULES change.  RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py untouched.**

Script `2026-09-10_publish-DRAG-not-TURNOVER-beside-every-window-width-claim_cloud.py`; console,
`.census.csv` (164 width-claim files), `.sites.csv`, `.grid.csv` (5 280 arm-rows), `.windows.csv`
(480 window measurements), `.walkforward.csv` committed beside it.  Runs in 154 s, deterministic.

## Axes, and what is ever selected on (PROTOCOL 4)
The queue names the two tuned parameters and both are swept in full with every point reported:
**P1 claim set** (TIER-A strict / TIER-B loose) and **P2 rung ladder**
(L1 = [10], L2 = [10, 25], L4 = [0, 10, 25, 50], L6 = [0, 5, 10, 15, 25, 50] bps).
The fresh leg's `f` is the **dial whose window is measured** (uniform 0.00–0.50, step 0.05,
fully enumerated, no point ever chosen) and `lambda` is the **turnover instrument** (idea 137's
partial rebalance, verbatim ladder, fully enumerated, never chosen).  Panels, books, sleeves and
cost rungs are reported axes.  The only selection anywhere is PROTOCOL rule 8.

## Gates — all pass, before any new number was read
* **G1** the vectorised segment runner vs `engine.backtest` on the evaluated slice:
  max|dr| **6.4e-16 / 6.3e-16 / 6.1e-16** and max|dturnover| **3.3e-16 / 3.3e-16 / 2.8e-16**
  on u56 / broad / small.
* **G2** the rung identity `r(c) = r(0) − turnover·c/1e4` vs a live `engine.backtest(25)`:
  **6.4e-16 / 6.3e-16 / 6.1e-16**.  This licenses reading six rungs off one simulation and is
  also why the question is well posed: with no equity-reading instrument, turnover reaches a
  return series **only** through cost.
* **G3** idea 403's committed `.windows.csv` (384 rows): base turnover strictly monotone in
  lambda in **48/48** cells, and its within-cell rho(w_contig, drag) reproduces at
  **−0.960 … −0.877** over 8 cells against the **−0.854 … −0.960** the queue quotes.

## H1 — CENSUS.  The premise is confirmed, and it is worse than "how many change rank"
2 768 committed CSVs scanned (this run's own artefacts excluded).  A column only counts as a
turnover or a rung if its **name** is not a statistic about one (`spearman_turn_pass` is not a
turnover) and its **values** sit in the right physical range — a keyword census over-counts by
3.5x here, which is idea 286/523's finding on a new statistic.

| tier | files with a width/window column | + turnover | + rung | **re-priceable as published** |
|---|---|---|---|---|
| **TIER-A** (strict: an interval width on a dial) | **44** | 2 (4.5 %) | 14 (31.8 %) | **1 (2.3 %)** |
| **TIER-B** (loose: every keyword hit) | **164** | 15 (9.1 %) | 53 (32.3 %) | **7 (4.3 %)** |

**The single strict-tier file that can be re-priced on drag is idea 403's own `.windows.csv` —
the file that made the prescription.**  Every other committed width claim in the record, 43 of
44 strictly and 157 of 164 loosely, cannot be re-priced at all without re-running it: the drag
column the queue asks for is not merely wrong, it is **absent**.

## H2 — ALGEBRA.  The re-pricing is a strict NO-OP inside one rung
`drag = base_to · c/1e4` is a **positive affine map** of `base_to` at fixed `c`, so the ranking is
identical by construction.  A drag re-pricing can move a ranking **only** where the claim pools
cells at different rungs.  Measured, not asserted: on the fresh grid the L1 ladder gives
**0 of 80 cells moved, Kendall tau exactly 1.000, 0 discordant pairs, argmax unchanged.**
This is the load-bearing fact and it makes the rung ladder the whole tuned parameter.

## H3 — SLOPE.  403 replicates on a THIRD panel and a SECOND sleeve
The CASH sleeve (plain de-grossing to `(1−f)`) is new — 403 ran only the TLT/GLD/UUP ETF sleeve,
which does not exist on a pure small-cap panel.

| panel | book | sleeve | rho(w, drag) | rho(w, base_to) | rho @0 bps | rho @25 bps | mean w_pts |
|---|---|---|---|---|---|---|---|
| u56 | TOP20 | ETF3 | **−0.923** | −0.038 | +0.577 | −0.779 | 6.90 |
| u56 | TOP20 | CASH | **−0.847** | −0.051 | +0.577 | −0.674 | 4.35 |
| u56 | EWALL | ETF3 | **−0.932** | 0.000 | n/a | n/a | 4.63 |
| u56 | EWALL | CASH | **−0.755** | −0.051 | n/a | n/a | 1.27 |
| broad | TOP20 | ETF3 | **−0.931** | −0.124 | +0.756 | −0.873 | 4.21 |
| broad | TOP20 | CASH | **−0.928** | −0.238 | −0.282 | −0.577 | 1.25 |
| broad | EWALL | ETF3 | **−0.930** | 0.000 | n/a | n/a | 3.67 |
| broad | EWALL | CASH | **−0.374** | +0.282 | +0.845 | n/a | 0.06 |
| small | TOP20 | CASH | INERT | — | — | — | 0.00 |
| small | EWALL | CASH | INERT | — | — | — | 0.00 |

Median rho(width, drag) **−0.925** over the 8 non-inert cells; 6 of 8 sit inside 403's quoted
[−0.854, −0.960].  The two that do not (**−0.755**, **−0.374**) are the two thinnest cells, with
mean widths 1.27 and 0.06 grid points — a width that is almost always 0 cannot correlate with
anything.  **The cost signature is exact:** median rho(width, base_to) is **+0.577 at 0 bps** and
**−0.726 at 25 bps**.  A dial that does nothing at zero cost and everything at high cost is a
cost dial, which is 403's own test and it passes again.

**SMALL439 is INERT, and for a reason the record already published.**  Both small-panel cells have
width 0 at every one of 48 (lambda, rung) points, and the binding margin is flat in `f` at
−0.136 (TOP20) / −0.245 (EWALL) — i.e. the bar that fails is a **Sharpe** leg, which no amount of
de-grossing can move.  This re-derives idea 575's KILL ("can SMALL439 clear a 4b Sharpe leg under
ANY unlevered book form" — no) as a *width* statement, independently.

## H4 — LEVEL.  403's reversed intercept replicates, 4 of 4 non-degenerate cells
Under a pure drag law the higher-turnover book must carry the **narrower** window at any positive
rung.  It does not.  On every (panel, sleeve) cell with any width content, TOP20 has **6.9–11.0x**
EWALL's base turnover **and the wider window**:

| panel / sleeve | TO ratio | mean w_pts TOP20 | mean w_pts EWALL | verdict |
|---|---|---|---|---|
| u56 / ETF3 | 8.0x | **6.90** | 4.63 | 403 sign — turnover ranks width backwards |
| u56 / CASH | 8.0x | **4.35** | 1.27 | 403 sign |
| broad / ETF3 | 11.0x | **4.21** | 3.67 | 403 sign |
| broad / CASH | 11.0x | **1.25** | 0.06 | 403 sign |
| small / CASH | 6.9x | 0.00 | 0.00 | degenerate (both empty) |

Pooled over all 480 window measurements, rho(width, base_to) = **−0.073** (403 reported −0.127 —
both are nothing).  So `width ≈ intercept(panel, book, sleeve) − slope · drag` with the two terms
carrying opposite signs in turnover is **confirmed on a second, independent grid**.

## H5 — THE ASK.  How many change rank, and does it help?
| ladder | rungs | cells | moved | frac | Kendall tau | discordant pairs | argmax changed |
|---|---|---|---|---|---|---|---|
| L1 | [10] | 80 | **0** | **0.000** | **1.000** | 0 | no |
| L2 | [10, 25] | 160 | 160 | 1.000 | 0.764 | 1 474 | yes |
| L4 | [0, 10, 25, 50] | 320 | 318 | 0.994 | 0.414 | 13 739 | yes |
| L6 | [0, 5, 10, 15, 25, 50] | 480 | 478 | 0.996 | 0.445 | 30 372 | yes |

And on the record's own two re-priceable published sites (`.sites.csv`): **456 of 456 cells move
rank (100 %)**, and rho flips sign on one of them (idea 403's file: rho(width, base_to) **+0.222**
→ rho(width, drag) **−0.259**).

**But "changes rank" is not "is better", and this is where the queue's prescription fails.**
Asking which of the two orders actually PREDICTS width:

| ladder | \|rho(w, turnover)\| | \|rho(w, drag)\| | better order |
|---|---|---|---|
| L1 [10] | 0.078 | 0.078 | tie (identical by construction) |
| **L2 [10, 25]** | **0.088** | **0.056** | **TURNOVER** |
| L4 [0, 10, 25, 50] | 0.133 | **0.311** | DRAG |
| L6 [0, 5, 10, 15, 25, 50] | 0.073 | **0.200** | DRAG |

**L2 is the record's own published rung pair** — 10 bps is PROTOCOL's rung and 25 bps is the
second rung nearly every committed file reports.  On exactly that ladder the drag column the
queue wants published is **worse than the turnover column it replaces**, and it only starts to
pay once the ladder reaches 0 and 50 bps, rungs the record almost never publishes.  The
prescription as worded — "publish drag beside every window-width claim" — is therefore **KILLED
at the rung pair it would actually be applied on**, and survives only as the narrower claim below.

## What the record should do with this instead
Not "publish drag", but: **a width-width comparison across cells is only meaningful at a fixed
rung, and at a fixed rung drag and turnover are the same column.**  The re-pricing 613 proposes
is a no-op where it is safe and is an improvement only across a rung range wider than the record
publishes.  The honest one-line amendment to 403's closing sentence is that base turnover
predicts **how fast a window closes as the rung rises**, and neither turnover nor drag predicts
**how wide it is** — the intercept does, and the intercept is a panel/book/sleeve fact.

## KEEP paths (PROTOCOL 4, both evaluated on every arm-row)
**4a** vs the live RULES v2 book, cost-matched: **55 / 5 280**, and **0 at 25 and 50 bps**.
**4b** vs SPY on all five bars: **1 264 / 5 280** (300/266/241/219/156/82 at 0/5/10/15/25/50 bps).
**BOTH: 12 / 5 280, all twelve at 0 and 5 bps — below PROTOCOL's own 10 bps rung.  At 10 bps and
above, BOTH = 0.**  Nothing is promoted and no memo is filed.  Per-cell at 10 bps: u56/TOP20/ETF3
4b 63/88 (4a 6), u56/EWALL/ETF3 4b 40/88 (4a 8), u56/TOP20/CASH 4b 39/88, broad/TOP20/ETF3 4b
46/88, broad/EWALL/ETF3 4b 32/88, broad/TOP20/CASH 4b 13/88, u56/EWALL/CASH 4b 8/88,
broad/EWALL/CASH and both small cells **0/88**.

## Rule 8 (PROTOCOL 8) — (f, lambda) chosen on 2009–2016 alone, 2017–2026 read exactly once
60 picks per selector (3 panels x book x sleeve x 6 rungs).

| selector | median f | median lambda | OOS Sharpe | OOS CAGR | OOS MaxDD | beats SPY | beats RULES v2 | clears OOS 4b | clears OOS 4a |
|---|---|---|---|---|---|---|---|---|---|
| S0 IS-Sharpe | 0.00 | 0.06 | **1.046** | 12.25 % | −21.67 % | 46/60 | 26/60 | 6/60 | **0/60** |
| S1 IS-4b screened | 0.15 | 0.06 | 1.036 | 12.45 % | −22.02 % | 46/60 | 21/60 | **13/60** | **0/60** |
| S2 min-turnover | 0.50 | 0.06 | 0.999 | 10.23 % | −18.41 % | 46/60 | 16/60 | 0/60 | **0/60** |
| S3 min-drag | 0.28 | 0.06 | 1.002 | 11.01 % | −19.66 % | 47/60 | 16/60 | 0/60 | **0/60** |

At 10 bps, by panel (SPY OOS and RULES v2 OOS are the comparands):

| panel | SPY OOS CAGR / Sharpe / MaxDD | RULES v2 OOS | S0 | S1 |
|---|---|---|---|---|
| u56 | 15.32 % / 0.876 / −33.7 % | 9.48 % / 1.279 / −12.1 % | 12.53 % / **1.216** / −17.3 % | 13.23 % / 1.196 / −18.4 % |
| broad | 15.45 % / 0.882 / −33.7 % | 7.98 % / 1.119 / −12.2 % | 12.40 % / **1.115** / −19.5 % | 12.14 % / 1.104 / −19.1 % |
| small | 15.45 % / 0.882 / −33.7 % | 3.85 % / 0.568 / −14.7 % | 12.22 % / 0.673 / −34.8 % | 12.22 % / 0.673 / −34.8 % |

Every selector beats SPY's OOS Sharpe on 46–47 of 60 picks and **none of the 240 picks clears 4a
out of sample**.  The chooser buys the turnover instrument as 403 found: **lambda = 0.06 is the
median pick for all four selectors**, on EWALL cells that trade 0.83x/yr as well as on TOP20's
6.6–11.9x — idea 615's open question, seen again.
**S2 and S3 are identical in 50 of 60 cells and the 10 exceptions are exactly the 10 zero-rung
cells, where drag is identically 0 and the order is UNDEFINED rather than different — 0
disagreements at any rung above 0.**  That is H2 again, as a selector.

## Predictions, scored
P1 **RIGHT** (the census would find the drag column mostly absent) — but I predicted ~10 %
strict-tier coverage and it is **2.3 %, one file, 403's own**.
P2 **RIGHT** (single-rung re-pricing is a no-op; 0/80, tau exactly 1.000).
P3 **RIGHT** (403's slope replicates; median −0.925 against its −0.854…−0.960).
P4 **RIGHT** (403's reversed intercept replicates, 4/4 non-degenerate cells).
P5 **WRONG** (I predicted drag would be the better predictor at every ladder; at the record's own
L2 = [10, 25] it is **worse**, 0.056 vs 0.088).

## Caveats carried
* **SURVIVORSHIP (idea 54):** all three panels are current constituents; SMALL439 additionally
  drops the 44 `max_1d_move >= 1.0` tickers from `data/small_meta.csv` before anything runs
  (439 investable names, 2010→2026).  The equity leg is flattered relative to the ETF sleeve, so
  every width here is biased narrow and toward low f.
* The census reads **committed CSVs only**; a width claim made in prose and never written to a
  CSV is invisible to it, which is why TIER-B is reported as the loose bound beside TIER-A.
* lambda can only **lower** turnover, so the falsification is one-sided; and it changes the book's
  **path** as well as its trading, which is why the cost route is the arbiter (403's own caveat).
* MaxDD is one number off one path and the 4b DD cap turns on exactly that number (idea 321).
* Idea 126: t+1 execution, no lag band.  Idea 38: u56/broad carry the calendar-day index.
* Width is a within-cell statistic on a fixed uniform grid and is never pooled by value across
  panels without the grid being identical, which it is here by construction.

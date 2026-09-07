# Idea 378 — back-fill the mean-name-count column over every quoted price

**2026-09-07, lane B.  Verdict: ANSWERED + INFRASTRUCTURE DEFECT.  The column is
delivered for 1546 of 2122 priced rows (72.9%); the queue's own method reaches 9.8%.
No rules change, no new KEEP.**

Script `2026-09-07_back-fill-the-mean-name-count-column-over-every-quoted-price_B.py`;
artefacts `.census.csv`, `.widthmap.csv`, `.backfill.csv`, `.answer.csv`, `.grid.csv`,
`.walkforward.csv`, `.ordering.csv`, `.console.txt`.

## Gates (asserted before any new number)

| gate | what | result |
|---|---|---|
| G1 | the TOP20 / V1u / EWall rungs of this ladder **are** idea 94's `targets()`, on all 3 panels × 11 (gate × conv) | `max|dw| = 0.000e+00` **EXACT** |
| G2 | `H.run` with every instrument off == `engine.backtest` @10 bps, all books, all panels | `max|diff| = 0.000e+00` **EXACT** |
| G3 | the price grid reproduces idea 124's committed `_B2.grid.csv` on every shared (uni, book, cost, arm) key | **448 rows, `max|err| = 1.776e-15`** |

G3 is the load-bearing one: the books re-measured in [B] are idea 124's books, not
look-alikes, so the widths below attach to the record's own prices.

## [A] The queue's literal method fails on 90.2% of the record

2122 PRICED rows (a number in CAGR / Sharpe / MaxDD) and 565 RATE rows ("k of N") were
classified; 125 table lines were header or malformed and are excluded by name.

| tier | what is recoverable | PRICED | RATE |
|---|---|---|---|
| **R1 MEASURED** | a sibling CSV carries a holdings column (`names`, `n_names`, `mean_names`, `names_held`, `breadth`) | **208 (9.8%)** | 96 (17.0%) |
| R2 NOMINAL-COL | only the dial `n` / `nkeep` / `topn` / `rung` | 288 (13.6%) | 182 (32.2%) |
| R3 ROW-TEXT | the row names a size (`TOP20`, `n=20`, `5-name`) or a panel | 1050 (49.5%) | 10 (1.8%) |
| R0 UNDEFINED | nothing — 576 priced rows sit on a script with **no committed CSV at all** | 576 (27.1%) | 277 (49.0%) |

The queue asked for recovery "from its parent's grid CSVs".  Done literally that reaches
**208 of 2122 (9.8%)**.  This generalises idea 359's 5.3%-on-206-band-rows to the whole
record and puts the same amendment on firmer ground: **a `names` column on every grid CSV**
is the only route to a record that can check its own two width clauses.

## [B] Width map — nominal is not width, and the error is one-sided

Mean holdings := mean over weekly rebalance days of `#{|w| > 1e-9}` in the target book.

| control book | nominal | U56 | B136 | SMALL484 |
|---|---|---|---|---|
| TOP3 / TOP5 / TOP10 / TOP20 / TOP40 | 3/5/10/20/40 | 3.0 / 4.9 / 9.9 / 19.9 / 39.9 | 3.0 / 5.0 / 10.0 / 19.9 / 39.9 | 3.0 / 5.0 / 10.0 / 20.0 / 40.0 |
| TOPALL (scored limit) | panel | **53.8** | **130.7** | **367.8** |
| EWall (priced limit) | panel | 54.1 | 131.4 | 382.0 |
| **RULES v2 (LIVE)** | panel | **38.4** | 93.2 | 185.7 |
| RULES v1 / V1u | 5 | 5.0 | 5.0 | 5.0 |

Median measured/nominal ratio by nominal level: 0.986 / 0.991 / 0.992 / 0.984 / 0.971 at
n = 3/5/10/20/40, then **0.686 / 0.685 / 0.386** at nominal 56 / 136 / 483.  Hard top-n
rungs are honest to ~2%; every whole-panel label overstates, by a third on B136 and by
**61%** on SMALL484.  Over the 264 (panel × book × gate × conv) cells the nominal proxy
puts the cell on the wrong side of the threshold in **30 (11.4%) at 20 names** and
**49 (18.6%) at 40**.

**The live book is inside idea 124's ordering clause.**  RULES v2 on U56 holds **38.4**
names against a `56` the record would have written — below the 40-name bar at which
idea 124 found the menu's ordering reproducible.

## [C] The answer

| threshold | rows below (corrected) | rows below (raw nominal) | share of the 1546 recovered | share of all 2122 priced |
|---|---|---|---|---|
| 5 | 110 | 47 | 7.1% | 5.2% |
| 10 | 223 | 142 | 14.4% | 10.5% |
| **20 — idea 124's SIGN clause** | **759** | 371 | **49.1%** | **35.8%** |
| **40 — idea 124's ORDERING clause** | **1332** | 951 | **86.2%** | **62.8%** |
| 56 | 1401 | 1041 | 90.6% | 66.0% |

576 rows (27.1%) stay UNDEFINED and are never imputed.  Reading the raw nominal instead
of the corrected width would have undercounted the sign clause by 388 rows and the
ordering clause by 381.

## [D] KEEP paths, 1224 grid points (3 panels × 8 books × 17 arms × 3 cost rungs)

`4a 0/408 @0 bps, 1/408 @10, 1/408 @25` — and the single passer is **not a new book**:
U56 TOPALL + `band3-dg` correlates **0.9998** with live RULES v2 at `max|dw| = 0.0147`
and holds 38.38 names against the live book's 38.44.  It is RULES v2 under the SCORED
rather than the PRICED denominator — exactly idea 380's convention gap, re-derived here
by accident.  `4b 60/44/22 of 408 @0/10/25 bps`, every passer on U56 or B136, every one
a re-measurement of a family the record already holds; nothing proposed.  First-failing
4b bar @10: H1 171, DD 99, H2 62, CAGR 28, OOS 4.

## [E1] Rule 8 — the rung is not choosable in-sample

Rung chosen on IS (≤2016) Sharpe @10 bps, 2017–2026 read once, per (panel × arm), 51 cells.
The IS chooser beats its own TOP20 anchor OOS in **7/51**, SPY in 17/51, live RULES v2 in
13/51; **mean regret −0.1545**.  IS picks TOP3 15×, TOP20 13×, TOP10 12×; the OOS argmax is
TOPALL 23× and TOP20 18× — the chooser reaches for concentration in-sample and pays for it.
This is idea 124's kill of the floor-as-a-dial reproduced on a third construction.

## [E2] The ordering clause survives — but only once the column is MEASURED

spearman(IS rate list, OOS rate list) over the 16 arms, per (panel × rung), 24 cells:

| width class | by **measured** holdings | by **nominal** n |
|---|---|---|
| < 20 | +0.0448 (n=14) | +0.1772 (n=12) |
| 20–40 | +0.4726 (n=4) | **−0.3214** (n=3) |
| ≥ 40 | **+0.6948** (n=6) | +0.6137 (n=9) |

On the measured column the clause is **monotone** and reproduces idea 124's finding on a
fresh corpus.  On the nominal dial it is **not monotone** — the middle class inverts.  Five
of 24 rungs change class when nominal is replaced by measured.  The column is not
bookkeeping: it is what makes the record's own reproducibility clause legible.

## Proposal (for Sunday review — an amendment, not a rules change)

1. Every grid CSV writes a `names` column: mean holdings per rebalance day of the target
   book.  (Idea 359 proposed this on band rows; it is now measured on the whole record.)
2. LEADERBOARD gains a `names` column; a row that cannot state one is quoted as `n/a`,
   not as its panel size.
3. PROTOCOL rule 4 gains a caveat sentence: *"A price measured on a book holding under 40
   names has an ordering that does not reproduce out-of-sample (idea 124/378); under 20
   names its sign does not either. State the book's mean holdings, never its nominal n."*

## Caveats

Survivorship (all three panels are current constituents) flatters every level; rung
differences much less so.  SMALL484 is the cached 484-column sub-$2B panel with SPY
excluded from every book, not the record's SMALL439, and starts 2010-01-04.  [A] and [C]
are text/artefact classifications of a hand-written file — reproducible, not
authoritative, and every classified row is committed.  Mean holdings is measured on
TARGET weights; a per-name trailing stop can hold fewer names intraperiod than its
target says.

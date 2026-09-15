# Idea 937 — re-score the record's committed `freq='M'` 4b PASS rows against their own MONTHLY nulls

**2026-09-15, lane B.** Script `2026-09-15_re-score-committed-freq-M-4b-PASS-rows-against-their-own-MONTHLY-nulls_B.py`.
`RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched. **Nothing promoted. Rule 6 untouched.**

## ANSWERED = YES, AT PROTOCOL'S OWN RUNG AND ONLY THERE — KILL for the record's committed MONTHLY 4b PASS rows at 5–10 bps as evidence about a rule

**58.8% of the re-priceable committed monthly 4b passes (40 of 68 STRICT; 641 of 1,507 = 42.5% WIDE) sit on a
cell whose own gross-matched monthly coin flip clears 4b at more than 5%** at PROTOCOL rule 2's 10 bps. On the
identical cells run WEEKLY, the number is **0 of 68 and 0 of 1,507**. One quarter of the STRICT block (17 of 68)
sits on a cell whose coin flip passes more than **one time in four**.

## WHAT WAS ASKED

Idea 926 measured a 4-of-30 vs 0-of-30 gap in cells whose coin flip clears 4b at 10 bps between the monthly and
weekly grids, with a 40.5% maximum. Idea 680 could not census this because its nulls were weekly-only. The queue
asked for the census: harvest the record's committed `freq='M'` 4b PASS rows and re-price each against a monthly
gross-matched null.

## WHY IT MATTERS FOR CAPITAL

4b is the only path in this project allowed to move real money, and a 4b row is read as "this rule beat SPY on
four legs". Idea 680 showed that reading is roughly safe on WEEKLY books at 10 bps — a coin flip drawn from the
same admission pool almost never clears the bar. Idea 926 then showed the protection is bought by weekly
TURNOVER, not by the bar. The record contains a large block of monthly 4b passes certified before anyone had a
monthly null to compare them with. This run prices that block.

## WHAT WAS MEASURED

A **CENSUS** of 4,592 committed `.csv` artifacts (211 eligible, 122,006,137 bytes, 412,396 rows, sha `7ff2dbe`)
plus a **REBUILD** of **3 panels × 5 book templates × 4 gross rungs × 2 cadences × 5 cost rungs = 600 book rows,
120 null families × 400 draws = 48,000 null books and 1,800 null cells, all published**. The null is idea
680/926/931's construction unmodified: on each DECISION row it holds the book's own k(t) names at the book's own
per-name weight g/k(t), drawn uniformly from the book's own candidate pool, so gross, count and cash are
identical row by row (G5) and only WHICH names differs; it is re-drawn on its own cadence so it carries the same
turnover effect the book does. Two tuned dials, all 6 points reported: CLAIM SET {STRICT, WIDE} × DRAWS
{100, 200, 400} (nested prefixes of one stream per family, G8). The WEEKLY arm is a fixed CONTROL, not a third
axis — it is 680/926's published grid and the reproduction target of G3b.

## THE CENSUS, AND THE 2,413 ROWS THAT ARE NOT CLAIMS

142,848 committed cadence-`M` rows carry a 4b flag; **8,337 of them are PASSES. 2,413 of those 8,337 (28.9%) are
NULL-DRAW rows** — per-draw artifacts from `.draws.csv` files, i.e. the record's own coin flips, whose pass flags
would have inflated this census with the very object it measures. They are excluded from both claim sets and
counted. That leaves **5,924 committed CLAIM rows**, of which **STRICT re-prices 323 (5.5%, 25 cells, 7 files)**
and **WIDE 1,810 (30.6%, 48 cells, 38 files)**. The 5,601 STRICT misses are named: 3,336 carry a panel label
this tree cannot rebuild, 2,201 a book label, 61 no cost, 3 no gross. **The unmapped mass is the honest limit of
this run** and is why the headline is quoted as a share of what is re-priceable, never of the record.

## THE RE-SCORE, BY COST RUNG — the exposure is a 5–10 bps phenomenon and nothing else

| rung | claims (STRICT) | mean M base | mean W base | M/W | share M > 5% | share W > 5% |
|---|---|---|---|---|---|---|
| 0 bps | 66 | 29.80% | 42.41% | 0.70 | 78.8% | 78.8% |
| 5 bps | 64 | 23.45% | 2.09% | **11.2×** | 78.1% | 3.1% |
| **10 bps** | **68** | **13.80%** | **0.27%** | **50.7×** | **58.8%** | **0.0%** |
| 25 bps | 67 | 1.13% | 0.00% | — | 0.0% | 0.0% |
| 50 bps | 58 | 0.06% | 0.00% | — | 0.0% | 0.0% |

WIDE reads 31.42 / 24.78 / **13.31** / 1.05 / 0.05% against 41.79 / 1.85 / **0.05** / 0.00 / 0.00%, i.e. the same
shape on 5.6× the claims. At the family level, **8 of 60 monthly families clear 5% at 10 bps against 0 of 60
weekly ones** (max 44.25% monthly, 1.00% weekly) — 926's "4 of 30, maximum 40.5%" reproduced on a wider grid at
a different seed.

**The structure is the finding.** At ZERO cost the weekly null is the EASIER one (42.41% vs 29.80%): a fast coin
flip that pays nothing to trade beats SPY's Sharpe more often than a slow one. The moment PROTOCOL's cost rung
bites, the weekly null dies (2.09% → 0.27% → 0.00%) while the monthly one survives (23.45% → 13.80%), because
weekly books pay 13.3× of annual turnover and monthly ones 6.0×. By 25 bps both are gone. **The window in which a
monthly 4b pass is uninformative is 5–10 bps — which is exactly and only where PROTOCOL rule 2 reads it.**

## THE PRE-REGISTERED HYPOTHESES, AS THEY CAME OUT

- **H_BASE FAILS at 44.0%** pooled over all five rungs (bar > 50%). It fails *because of the pooling*: at
  PROTOCOL's own binding rung the share is **58.8%**, and at 5 bps 78.1%, but 25 and 50 bps contribute 125 claims
  at 0.0%. Stated as it was pre-registered; the rung-level table above is the number that bears on capital.
- **H_CAD FAILS at 1.52×** (bar 2.0×), for the same reason and in the same direction: the 0 bps rung, where the
  weekly mean (42.41%) *exceeds* the monthly (29.80%), drags the pooled ratio down. Per rung the ratio is
  **11.2× at 5 bps and 50.7× at 10 bps**. A single pooled cadence ratio is not a well-posed quantity — the same
  conclusion idea 943 reached for cadence gains and idea 933 for a Shapley share: **a base-rate claim quoted
  without its rung is not a claim.**
- **H_CLAIM PASSES at |Δ| 0.023** (44.0% STRICT vs 41.7% WIDE). The headline is not a claim-set artefact, and the
  WIDE re-interpretations (CAND20 → TOP20 and the rest) do not move it.

## WHAT IT COSTS THE STANDING CANDIDATE

`U56 / TOP20 / g0.75 / MONTHLY / 10 bps` — the 2026-09-04 candidate on the 2026-09-15 monthly convention, and the
single most-claimed cell in the census (17 committed monthly 4b passes) — reads **14.69% / 1.2025 / −19.51% with
a monthly null base rate of 44.25% against a weekly base rate of 0.00%**. Its own coin flip clears 4b nearly one
time in two. At 0 bps the same cell's null is at 94.25%, at 5 bps 77.00%. This is a fourth independent strike on
that book this week, after idea 933's answer-key mega-cap sleeve, idea 938's rebalance-offset artefact and idea
931's cadence-gain percentile of 1.2.

Of the **7 monthly full-sample 4b passes** on the 60-cell grid at 10 bps, **3 are inside their own null**
(TOP20/0.75 44.2%, EWELIG/0.75 5.5%, BAND03/1.00 5.5%) and 4 are outside it. Of the 5 weekly ones, all 5 are
outside. **4a is 0 of 60 on both cadences** — no cell on this grid beats the live RULES v2 book in both halves
without a worse drawdown.

## RULE 8 (PROTOCOL rule 8) — parameters chosen on 2009–2016 ALONE, 2017–2026 read ONCE, BOTH KEEP paths

Three IS-only choosers (best IS Sharpe; best IS Sharpe among books clearing the IS 4b level legs; best IS Sharpe
among books whose IS null base rate ≤ 0.05) × 3 panels × 5 rungs × {monthly-only, cadence-also-chosen} =
**90 picks, 84 live (6 IS sets EMPTY). OOS 4b 0 of 84. OOS 4a 0 of 84.**

| | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|
| U56 best pick (CH_SHARPE @10 bps, M/TOP5/g1.00) | 20.50% | 0.832 | −34.61% |
| B136 best pick (CH_SHARPE @10 bps, M/TOP20/g1.00) | 20.81% | 1.005 | −33.68% |
| SMALL663 best pick (CH_SHARPE @10 bps, M/BAND03/g1.00) | 5.43% | 0.595 | −21.94% |
| **SPY** (U56 tape / B136 tape) | **15.27% / 15.33%** | **0.874 / 0.877** | **−33.72%** |
| **RULES v2 live baseline** (U56 M / B136 M @10 bps) | **9.56% / 8.25%** | **1.224 / 1.085** | **−15.69%** |

The B136 pick beats SPY's OOS Sharpe (1.005 vs 0.877) and its CAGR by 5.5 pp, and **still fails 4b on `L4_DD`
alone**: −33.68% against a bar of 0.60 × −33.72% = −20.23%. The U56 pick fails on Sharpe and drawdown together.
4a fails everywhere — v2's OOS Sharpe of 1.224 is not beaten by any IS-chosen book. **The base-rate clause is
free but not sufficient**: CH_BASE lands on the same pick as CH_SHARPE on 20 of 20 U56/B136 cells and cuts the
mean null OOS 4b rate from 4.1% (CH_4bIS) to 0.9%, at no cost in OOS Sharpe (0.783 both) — it screens out the
easy cells without finding a good rule.

## GATES — 10 of 10, and G3a is a CORRECTION TO THE RECORD

- **G1** `ctx.run` ≡ `engine.backtest` @10 bps on both cadences: 1.21e-17 / 8.67e-18.
- **G2** `band_book(0.03, 0.75)` ≡ `baseline.rules_v2_weights`: 0.000e+00.
- **G3a** REPRODUCTION of `U56/TOP20/0.75/M/10 bps`: got **14.69% / 1.2025 / −19.51%** against idea 926's
  COMMITTED 14.69% / 1.203 / −19.51%, max|d| **5.23e-04**. **Idea 931's G3 reported this same cell at 15.28% /
  1.2120 and attributed the +0.59 pp gap to a VINTAGE DRIFT on this tree. At sha `2a340b2` this file's code path
  reproduces 926's committed number exactly and misses 931's re-read by 0.0095, so the drift is not a property of
  the TREE — it belongs to 931's own construction.** Reported, not gated; filed as follow-up 967.
- **G3b** CROSS-RUN null leg at a different seed base (937 vs 926): the same cell's monthly null base rate reads
  **44.25% against 926/931's published 38.4%**, |d| 0.058 inside the 0.10 bar. The exposure is not a one-seed
  artefact.
- **G5** gross match ≤ 0.0000 worst over all 120 families. **G6** determinism 0.000e+00. **G7** SMALL663: 52
  tickers with `max_1d_move ≥ 1.0` dropped (663 names + SPY). **G8** draw nesting exact. **G9** every census
  denominator carries (sha, files, bytes, rows) — idea 894's proposed clause, applied voluntarily. **G10** the
  null is INVESTED on every family (min mean gross 0.2736, min median vol 0.0471) — the gate exists because idea
  931's first cut wrote the draw on the APPLICATION rows and held pure cash on every non-daily cadence.

## THE GUARD THIS PROPOSES — for Sunday review, NOT written into PROTOCOL.md here (rule 6)

> *"PROTOCOL 11 — any published 4b PASS must quote, beside its verdict, (a) the cost rung it is read at and
> (b) the 4b pass rate of its own gross-matched null on its own rebalance cadence at that rung. A 4b pass whose
> null base rate exceeds 5% is a statement about the admission family, not about the rule, and may not be cited
> as a capital claim."*

Cost of adoption as measured here: **40 of the 68 re-priceable committed monthly passes at 10 bps would lose
their citation, and 3 of the 7 monthly full-sample 4b passes on this grid, including the standing candidate's own
cell.** Weekly passes are untouched (0 of 68).

## SURVIVORSHIP (PROTOCOL 9)

`universe.json` / `universe_broad.json` / the SMALL screen are CURRENT-CONSTITUENT lists, so every CAGR and
drawdown LEVEL here is optimistic. The direction is specific and is stated rather than hidden: a coin flip drawn
from a survivor panel is a BETTER book than one drawn in real time, so **every null base rate above is an UPPER
bound**. That makes a HIGH base rate a soft indictment (the real-time rate would be lower) and a LOW base rate a
hard exoneration. Every headline in this run is of the first kind, so it is an upper bound and nothing is
promoted on it. The 4b bar is SPY, which is not survivorship-inflated.

## VERDICT

**KILL** for the record's committed monthly 4b PASS rows at 5–10 bps as evidence about a rule, on the 30.6% of
them this tree can re-price. Not a KEEP candidate on either path: 4a 0 of 120 full-sample cells, rule-8 OOS 4b
0 of 84 and OOS 4a 0 of 84. No memo, nothing promoted, rule 6 untouched.

Artifacts: `.census.csv` (11,848), `.books.csv` (600), `.nulls.csv` (1,800), `.draws.csv` (48,000),
`.rescore.csv` (6,399), `.cells.csv` (25), `.headline.csv` (6), `.rungs.csv` (10), `.walkforward.csv` (90),
`.hypotheses.csv`, `.gates.csv`, `.console.txt`.

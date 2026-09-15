# Idea 964 (cloud lane, 2026-09-15) — should the PHASE-AVERAGED MEAN replace the CANONICAL?

**ANSWERED = NO. KILL for the queue's proposal as a RE-PUBLICATION rule; PARK for one tranched
book it turns up. Nothing promoted, no rule change, rule 6 untouched.** `RULES.md`,
`PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched.
SELECTION: the FIRST Open idea in QUEUE.md, per the lane rule; it carries a price leg and names
no EDGAR / Form 4 / 8-K / options / spin-off / live-data object.

Script `2026-09-15_should-the-PHASE-AVERAGED-MEAN-replace-the-CANONICAL_cloud.py`.
Artifacts: `.grid.csv` (12,600), `.fport.csv` (300), `.families.csv` (300), `.census.csv`
(26,100), `.censussummary.csv`, `.corpus.csv`, `.walkforward.csv` (270), `.hypotheses.csv`,
`.console.txt`.

## What was asked
Idea 962 found the canonical rebalance phase scoring exactly at the blind-random rate (2 4b
passes against a Poisson-binomial 2.35) while the FAMILY MEAN beat every in-sample chooser in
0.600 of cells. The queue asked for the census: re-publish the record's committed monthly and
quarterly CAGR claims as CANONICAL, FAMILY MEAN and FAMILY SPREAD, and report how many change
SIGN or VERDICT.

## The distinction the queue's wording hides, and which this run prices separately
- **CANON** — phase 0, the period-end rebalance. The only object the live rules trade.
- **FMEAN** — the mean of the METRIC across the family's phases. An estimator. **No allocation
  of capital produces a mean-of-Sharpes**, so FMEAN can never be a KEEP and is never read as one
  below.
- **FPORT** — the TRANCHED book: 1/P of NAV in each of the P phase-books, re-levelled daily.
  This one *is* tradable, and it is what "trade the phase average" would mean at a desk.

## What was measured
12,600 grid rows (5 books × 3 panels × 2 gross × (21 M + 63 Q) phases × 5 cost rungs) plus the
300 tranched books built from the same phase returns, 270 rule-8 picks, and a census of 4,746
committed csv artifacts of which 43 (31 MB, 89,696 M/Q claim rows) carry a committed M/Q CAGR
claim with a nameable family key; 3 otherwise-eligible files were excluded as the record's own
null/coin-flip generators and are named in `.corpus.csv`.
TUNED 2: CLAIM SET (STRICT / WIDE / GRID) and CADENCE (M / Q / pooled) — every level printed,
none chosen. Panel, book, gross, cost rung, estimator and both 4b conventions are reported
constants. **GATES 7 of 7**, including **G3: idea 962's committed 12,600-row `grid.csv`
reproduced on 12,600 of 12,600 rows over 13 columns, max|d| 1.776e-15** — this run nests the
record's own grid.

## The answer — the swap changes almost nothing on the record
| claim set | rows | cells | sign flips (FMEAN) | verdict flips (FPORT) | cell-weighted |
|---|---|---|---|---|---|
| STRICT | 600 | 300 | **0.053** | **0.030** | 0.053 / 0.030 |
| WIDE | 25,200 | 300 | 0.053 | 0.028 | 0.053 / 0.030 |
| GRID | 300 | 300 | 0.053 | 0.030 | 0.053 / 0.030 |

`H_SIGN` **FAIL** (0.053 against a 0.10 bar) and `H_VERDICT` **FAIL** (0.030 against 0.10).
Re-publishing every committed monthly/quarterly CAGR claim as the family mean would move the
sign of (claim CAGR − SPY CAGR) on about 1 claim in 19 and the 4b verdict on about 1 in 33.
Row, cell and file weighting agree here to within 0.002 — this census does **not** reproduce
idea 970's row-vs-cell gap, because no single cell dominates the mapped rows.
64,496 harvested rows do **not** map onto this grid (29,332 at a gross that is not 0.75/1.00,
24,210 on a panel this grid does not carry, 10,794 on a book it does not carry, 160 off the cost
ladder). They are DROPPED and never counted as agreeing.

## The real finding — the canonical's bias is a CADENCE object, and 962's reading holds on only one of them
`H_BIAS` **PASSES pooled and FAILS on both of its own cadences taken separately**, which is the
part worth carrying forward:

| cadence | median (CANON − FMEAN) CAGR | canonical's percentile inside its own family | family CAGR spread (median / max) |
|---|---|---|---|
| **M** (21 phases) | **+0.600 pp** | **0.929** | 3.05 pp / 12.24 pp |
| **Q** (63 phases) | **−1.112 pp** | **0.063** | 4.37 pp / 23.77 pp |
| pooled | −0.213 pp (bar ±0.25) | 0.444 (bar [0.40, 0.60]) | — |

The pooled PASS is an averaging artefact of two large, opposite biases. **Month-end rebalancing
sits at the 93rd percentile of its own phase family and quarter-end at the 6th.** Idea 962's
"the canonical sits low in its own family" is a QUARTERLY fact and is the reverse of the truth
monthly — every committed monthly claim in the record is roughly +0.6 pp of CAGR optimistic
against a phase-blind reading, and every quarterly one roughly −1.1 pp pessimistic.

## The tranche is a quarterly object, and it is not free
| cadence | FPORT Sharpe > CANON | median Sharpe gain | FPORT turn/yr ≤ CANON |
|---|---|---|---|
| M | 0.300 of 30 | −0.0288 | 0.700 |
| Q | **1.000 of 30** | **+0.1022** | 0.433 |
| pooled | 0.650 (bar 0.75) → `H_TRADE` **FAIL** | | 0.567 (bar 0.90) → `H_CHEAP` **FAIL** |

Tranching wins in **every** quarterly family and loses in 70% of monthly ones, and it does not
pay for itself in turnover (the 63 tranches each trade 1/63 of NAV, but they trade 63 times more
often, so realised turnover is roughly unchanged — median 3.45/yr against the canonical's 3.41).
And it buys **no extra passability**: at 10 bps the grid carries **3 of 60 4b passes under CANON
and 3 of 60 under FPORT** — the tranche moves which cells pass, not how many.

## Rule 8 — one pass in 54, and it is a knife edge
Book × gross chosen on **2009–2016 alone** by 3 IS-only choosers × 3 panels × 2 cadences × 3
estimators, 2017–2026 read **once** (G6: picks invariant to permuted OOS columns).
**OOS 4b: CANON 0 of 18, FMEAN 0 of 18, FPORT 1 of 18. OOS 4a: 0 of 54.**

The single pass is `U56 / Q / FPORT / C_ISLEGS → EWELIG @ gross 0.75`:
full 11.60% / **1.107** / −20.14%, halves 1.203 / 1.035, **OOS 12.31% / 1.121 / −20.14%**
against **SPY OOS 15.27% / 0.874 / −33.72%** and **RULES v2 OOS 9.46% / 1.277 / −12.05%**.
Its canonical twin — the same book, same gross, quarter-end — reads OOS 11.53% / 1.034 / −22.21%
and **fails on `L4_DD` alone**. So the tranche does create a 4b pass the canonical does not have.

**It is PARK, not KEEP, for two reasons stated before the verdict was read.** (i) The DD leg
clears by **0.09 pp**: 20.14% against a cap of 0.60 × 33.72% = 20.23%. (ii) **26 of that
family's 63 phases pass 4b on their own** (within-family pass share 0.413), so a quarterly phase
drawn at random out of this family clears 4b more than two times in five and the tranche's pass
carries almost no information about the rule. It also fails 4a on drawdown against the live
book, as every growth candidate in this record does.

If Sunday wants it anyway, the exact RULES wording, **proposed and NOT applied** (rule 6):
> *Each quarter-end and on each of the 62 trading days before it, rebalance 1/63 of NAV: inside
> that tranche, hold every instrument priced that day that is above its own 200-day moving
> average with 20-day realised vol < 0.60, equal-weighted, at 75% gross, the gated-out weight in
> cash; decided at the close, executed at the next close.*

## Capital
**No.** One OOS 4b pass in 54 rule-8 picks, on a drawdown leg that clears by 0.09 pp, inside a
family where 41% of the phases pass unaided, and 0 of 54 on 4a. Nothing here justifies moving
real capital. The queue's proposal — replace the canonical with the family mean in every
committed claim — is a **KILL**: it changes 5.3% of committed claims' sign and 3.0% of their
verdicts, and the mean it would substitute is not a portfolio.

## What this proposes instead (a LABELLING clause, for Sunday review, NOT written into PROTOCOL.md)
> *"Every committed claim on a MONTHLY or QUARTERLY book is published with its family's CAGR
> spread and with the canonical phase's percentile inside that family. The canonical is not
> replaced — it is what the live rules trade — but a monthly claim is read as roughly +0.6 pp of
> CAGR optimistic and a quarterly one as roughly −1.1 pp pessimistic against a phase-blind
> reading, and a 4b pass is reported as NON-CERTIFYING wherever its own family's within-phase
> pass share exceeds 0.25."*
Cost of adoption as measured here: 0 committed claims are withdrawn, 3.0% of committed M/Q 4b
verdicts are re-labelled, and the one rule-8 pass this run found is labelled non-certifying by
its own 0.413 family share.

## Survivorship (rule 9)
U56, B136 and SMALL are CURRENT-CONSTITUENT lists; SMALL additionally drops the 52 tickers with
`max_1d_move` ≥ 1.0 per `data/small_meta.csv`. Every CAGR and drawdown LEVEL above is optimistic.
The CANON-vs-FMEAN-vs-FPORT contrast is the same names on the same tape under different
rebalance DAYS and is very nearly immune to it; the 4b levels are read against SPY, which is not
survivorship-inflated, so the single 4b PASS reported here is an UPPER bound and every FAIL is
understated.

Follow-ups filed: 974 (is the month-end/quarter-end bias reversal a flow fact or a calendar-count
artefact), 975 (price the quarterly tranche against a gross-matched rotating null), 976 (does the
0.413 within-family pass share generalise into a non-certifying rule for every 4b claim).

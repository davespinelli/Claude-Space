# Idea 352 — is-the-0-bps-to-10-bps-cliff-the-real-killer-of-the-idea-40-family (cloud, 2026-09-07)

**VERDICT: SPLIT. The cliff is real and turnover orders it (spearman -0.826). But a turnover
ceiling is NOT the cheapest pre-screen for the queue — it has lift 3.64 inside a construction
family and lift < 1 pooled over the committed record, and it changes 0 of 3 rule-8 picks.
KILL as a queue-wide pre-screen; the within-family ordering is the keepable part.**

Script: `2026-09-07_is-the-0-bps-to-10-bps-cliff-the-real-killer_cloud.py` ·
console `.console.txt` · 90-point live grid `.grid.csv` · 24 breakevens `.cstar.csv` ·
screen curves `.screen.csv` · record census `.census.csv` / `.census_ceiling.csv` ·
rule 8 `.walkforward.csv` + `.menu_*.csv`.

Tuned parameters: **2** (turnover ceiling T\*, cost rung c). Panels / families / n / cadence /
gross are the *population being screened*, and all 90 points are reported.

## Reproduction gate
`max |backtest(cost_bps=10) − (r0 − turnover·10/1e4)|` = **0.000e+00** on all three panels, so
every rung below is exact, not re-simulated.

## The cliff (live grid, 90 books = 3 panels × 5 families × 2 gross × 3 cadences)

| rung | 4b passes | 4a passes |
|---|---|---|
| 0 bps | **24 / 90** (U56 19, B136 5, SMALL439 0) | — |
| 5 bps | 15 / 90 | — |
| 10 bps | **9 / 90** (U56 7, B136 2) | **0 / 90** |
| 25 bps | 4 / 90 | — |

**63% of the 0-bps passes are dead by the PROTOCOL rung.** Idea 41's family is not unusual;
it is the general shape.

## Is turnover what sets the breakeven? YES, within the family

For all 24 zero-bps passes the exact breakeven `c*` (largest 0.5-bp rung still clearing 4b):

* **c\* vs annual turnover: spearman −0.826, pearson −0.515 (n=24).**
* Pass count for 4b@10 by turnover quartile: **7 / 1 / 1 / 0** (medians 8.2 / 14.6 / 25.9 / 52.5 ×/yr).
* Which bar kills the pass as cost rises: **CAGR 17, H1 3, H2 2, DD 2** of 24 — the CAGR floor
  binds first two-thirds of the time, which is the assumption a turnover ceiling encodes.
* But the closed form a ceiling implies, `c*_pred = CAGR-margin / (T/1e4)`, **over-predicts in
  24 of 24** by mean **+4.61 bps** (MAE 4.61). Costs raise vol as well as cutting return, and
  in 7 of 24 a Sharpe or DD bar binds before CAGR does. A pure turnover ceiling is
  systematically optimistic about how much cost a book survives.

## Is a turnover ceiling the cheapest pre-screen? NO — it inverts on the record

Target = "clears 4b at 10 bps", base rate 0.100 over the 90 live points:

| screen | threshold | admitted | precision | recall | **lift** |
|---|---|---|---|---|---|
| turnover ceiling | ≤ 5 ×/yr | 6 | 0.333 | 0.222 | 3.33 |
| turnover ceiling | **≤ 8 ×/yr** | 11 | **0.364** | 0.444 | **3.64** |
| turnover ceiling | ≤ 15 ×/yr | 34 | 0.235 | 0.889 | 2.35 |
| 0-bps Sharpe bar | ≥ 1.0 | 46 | 0.196 | 1.000 | 1.96 |
| 0-bps Sharpe bar | ≥ 1.1 | 24 | 0.250 | 0.667 | 2.50 |
| 0-bps Sharpe bar | ≥ 1.2 | 0 | — | 0.000 | — |

On this grid the ceiling beats the Sharpe bar on precision and lift at every matched admit
share, and it is the cheaper statistic (turnover is a property of `n` × cadence × panel, so it
is knowable before any return is scored).

**Then the record contradicts it.** 117 of the 1,108 committed CSVs carry both a turnover
column and a full-sample 4b flag — **61,200 pooled rows**:

| slice | n | 4b rate | median turnover, passes | median turnover, fails |
|---|---|---|---|---|
| all rungs | 61,200 | 0.148 | 9.03 | 7.78 |
| rows stating 0 bps | 3,725 | 0.296 | 9.33 | 9.30 |
| rows stating 10 bps | 25,851 | 0.157 | **9.11** | **4.95** |
| rows stating 25 bps | 18,823 | 0.085 | 7.91 | 9.83 |

Pooled over the record a 4b pass has *higher* turnover than a failure at the PROTOCOL rung, and
the ceiling's lift is **below 1.0 at every ceiling up to 8 ×/yr** (0.07–0.74 on the 10-bps
slice), only reaching 1.24 at a ceiling of 12 ×/yr that already admits 73% of the rows. The
record's low-turnover population is dominated by de-grossed, gated and cash-heavy books that
fail on the CAGR floor for reasons cost never touches, so the within-family ordering reverses
across families. **This is the answer to the queue's question, and it is no.**

## Rule 8 walk-forward (ceiling chosen on 2008-2016 only, 2017- read once)

T\* = the tightest ceiling admitting ≥ ⅓ of each panel's IS menu; the screened menu's max-IS-Sharpe
book is then read once OOS.

| panel | T\* ×/yr | admitted | screened pick | OOS CAGR / Sharpe / MaxDD | unscreened pick | OOS CAGR / Sharpe / MaxDD | RULES v2 OOS | SPY OOS |
|---|---|---|---|---|---|---|---|---|
| U56 | 9.95 | 10/30 | TOP20/g1.00/M | 16.38% / **1.0778** / −23.64% | *same* | 16.38% / 1.0778 / −23.64% | 1.2851 (9.53%, −12.05%) | 0.8820 (15.45%, −33.72%) |
| B136 | 12.33 | 10/30 | TOP40/g1.00/M | 14.97% / **0.9714** / −29.50% | *same* | 14.97% / 0.9714 / −29.50% | 1.1185 (7.98%, −12.24%) | 0.8820 |
| SMALL439 | 16.43 | 10/30 | TOP10/g0.75/M | 5.73% / **0.4638** / −32.62% | TOP10/g1.00/M | 7.28% / 0.4647 / −42.09% | 0.5680 (3.85%, −14.68%) | 0.8820 |

* **Screened − unscreened OOS Sharpe: 0.000 / 0.000 / −0.001, mean −0.0003, wins 0/3.** The
  ceiling changes what the chooser picks in 1 of 3 panels and buys nothing when it does
  (it does cut that pick's OOS drawdown 42.1% → 32.6%).
* **Admitted-set − whole-menu mean OOS Sharpe: +0.157 / +0.211 / +0.033, mean +0.134, wins 3/3.**
  The ceiling genuinely raises the *average* quality of the menu — it is just redundant with an
  IS-Sharpe chooser, which already avoids the high-turnover tail.

So the ceiling is a real fact about the menu and a useless addition to the pipeline: the
statistic it improves is one nobody trades.

## KEEP paths

**4a: 0 / 90 at 10 bps.** Nothing on this grid beats RULES v2 in both halves with no worse
drawdown; RULES v2's OOS Sharpe (1.285 U56) is above every screened and unscreened pick.

**4b: 9 / 90 at 10 bps, 4 / 90 at 25.** The widest-margin point is a by-product, not this
idea's question — see `.memo.md`. U56 TOP40 equal-weight, gross 0.75, monthly: 12.04% CAGR,
Sharpe 1.1401, MaxDD −18.00%, halves 1.1422/1.1425, OOS Sharpe 1.2187, **c\* = 43.5 bps**,
turnover 3.67 ×/yr. It clears all five 4b bars at 10 *and* 25 bps.

## Caveats

* SMALL439 is current constituents of a sub-$2B screen (survivorship); 44 of 483 tickers with
  `max_1d_move ≥ 1.0` dropped first. It contributed **0 of 24** zero-bps 4b passes, so it
  constrains nothing here except by its absence.
* The census normalises turnover to ×/yr by treating any value > 25 as a percentage; the record
  is not unit-consistent and that rule is a judgement, stated so it can be re-read.
* The census pools rows from different books, panels and vintages without weighting; it measures
  what the *record as written* would tell a screener, which is exactly the queue's question.

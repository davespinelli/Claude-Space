# Idea 604 — does every published MATCHED-GROSS TWIN claim need a PLACEBO column?

**Run:** cloud, 2026-09-10 · `2026-09-10_does-every-published-MATCHED-GROSS-TWIN-claim-need-a-PLACEBO-column_cloud.py`
**Verdict: YES — CONFIRMED, and the correction is larger than idea 602's one family suggested.
One NEW 4b KEEP-CANDIDATE falls out (memo below). No RULES/PROTOCOL/baseline edit.**

## Reproduction gates
| gate | result |
|---|---|
| G1 derived cost rung `r(c) = r(0) − turnover·c/1e4` | max\|diff\| **0.000e+00** PASS |
| G2 idea 84 EWALL U56 g=0.85 @10bps | 11.8% / 1.05 / −17.9% / H 1.07/1.03 (committed 11.8/1.05/−17.9/1.07/1.04) |
| G3 idea 602's committed `.placebo.csv.gz` | recomputed **BLOCK 0.259 / RAND 0.010** — its published headline, exactly |
| G4 twin interpolation on the 0.01-gross cache, 6 off-grid g | max\|dSharpe\| **3.6e-08** |
| G5 placebo matching identity (BLOCK/RAND share the real arm's twin) | max\|on-share diff\| **0.000e+00**, max\|mean-multiplier diff\| **0.000e+00** |

## [1] The census — how exposed is the record?
Walking every committed `.py`/`.md`/`.txt` in `research/backtests` plus LEADERBOARD/CHANGELOG/
QUEUE/RULES/PROTOCOL for matched-gross / matched-exposure / de-grossed-control / twin language:

| reading (tuned param 1) | files | sites | file carries ANY placebo/null word | placebo word **near** the site |
|---|---|---|---|---|
| WIDE (any matching site) | **410** | **2 067** | 57 (13.9%) | 22 (5.4%) |
| HEADLINE (site in the file's headline block) | 262 | 1 352 | 35 (13.4%) | 18 (6.9%) |
| ARM (file emits a per-arm twin column in a committed CSV) | 257 | 1 107 | 28 (10.9%) | 10 (3.9%) |

Those placebo counts are an **upper bound** — the regex catches any use of "null", "bootstrap",
"shuffle", "permutation" anywhere in the file, most of which are not a twin-leg placebo.
Instrument families named in a twin claim's context: TREND 105 files, COUNT 95, VOL 58,
SLEEVE 51, BREADTH 35, DD 31, STOP 25, CORR 18, MOM 14, DISP 4.

## [2] The re-pricing — nine clause families, three panels, every grid point
9 families (ABS / QEXP / QROLL breadth, RVOL, DISP, CORR, DDGATE, MAGATE, MOMGATE) × 3 levels ×
3 depths × 2 cadences × 2 gross × 3 rungs × 3 panels = **2 916 arms and 58 320 placebo rows**.
Coverage of the census: **265 of 436 family-mentions (60.8%)**; STOP goes to idea 396's own run
the same day, SLEEVE to idea 395, COUNT (the n dial) is not a de-grossing clause.

### The headline (pooled, all families, all panels)
| rung | REAL twin win rate | BLOCK placebo | RAND placebo | **readable excess** |
|---|---|---|---|---|
| 0 bps | 0.502 | 0.311 | 0.326 | **+0.191** |
| **10 bps** | **0.439** | **0.248** | 0.009 | **+0.191** |
| 25 bps | 0.342 | 0.177 | 0.003 | +0.165 |

**56.5% of the published win rate at the protocol rung is placebo.** On the dSharpe scale the
placebo is *negative* in all nine families (median −0.0006 to −0.0534) while the real margin is
positive in only four, so the correction runs both ways: per arm, the raw margin is positive in
**42.8%** and the placebo-differenced excess in **65.9%** — and **738 of 2 916 arms (25.3%)
change the SIGN of their twin verdict** when the column is added.

### Per family × panel (BLOCK, 10 bps; bar: diff ≥ 0.10 AND z ≥ 2.0)
Survives **16 of 27** cells; **REVERSED (the placebo beats the real gate) in 9**.

| family | U56 REAL/BLOCK | B136 REAL/BLOCK | SMALL REAL/BLOCK |
|---|---|---|---|
| QROLL | 1.000 / 0.250 | 1.000 / 0.244 | 0.944 / 0.347 |
| MAGATE | 0.722 / 0.194 | 0.722 / 0.219 | 0.667 / 0.306 |
| CORR | 0.722 / 0.217 | 0.667 / 0.200 | **0.000 / 0.317** |
| QEXP | 0.667 / 0.267 | 0.556 / 0.178 | 0.500 / 0.289 |
| ABS | 0.889 / 0.211 | 0.389 / 0.206 | **0.222 / 0.311** |
| DISP | 0.389 / 0.206 | 0.417 / 0.167 | **0.000 / 0.333** |
| RVOL | 0.389 / 0.111 | 0.333 / 0.139 | **0.111 / 0.328** |
| MOMGATE | **0.222 / 0.300** | 0.278 / 0.256 | **0.056 / 0.347** |
| **DDGATE** | **0.000 / 0.186** | **0.000 / 0.217** | **0.000 / 0.356** |

Two results worth naming. **DDGATE never beats its twin anywhere (0 of 324) while its own
no-information placebo does 19–36% of the time** — de-grossing on the book's own drawdown is
*strictly worse* than holding the same cash on shuffled days. And **7 of 9 families reverse on
SMALL**, so the small panel's published twin claims are the most exposed in the record.
Across the finer cut (family × panel × cadence × gross × rung) **110 of 324 cells (34.0%) are
reversed**.

## [3] KEEP paths and rule 8
**4a: 0 of 2 916 at every rung** — no de-grossing clause in this run beats cost-matched
RULES v2 in both halves with no worse drawdown. 4b: 347 / **166** / 35 at 0 / 10 / 25 bps.
At 10 bps **16 of the 166 are inherited** (the ungated EWALL base itself passes 4b only at
B136 / g=0.75 / 10 bps); **150 are earned**, 114 of which also beat their own twin.

**The claim's own rule 8 is weak and is reported as such:** the sign of the placebo-differenced
excess holds IS→OOS in only **14 of 27** panel × family cells, Spearman(excess_IS, excess_OOS)
= **0.154**. In-sample the excess is negative in 13 of 27 cells and out-of-sample positive in
19 of 27. So *that the column is needed* is settled; *how big it is for a given family* is not
stable across the 2016/2017 boundary. QROLL is the exception — it is positive in both windows
on all three panels (U56 +0.550 → +0.731; B136 +0.194 → +0.744; SMALL +0.281 → +0.603).

Book-level rule 8 (choose family/level/depth/cadence/gross on IS Sharpe, read 2017+ once):
| panel | IS pick | OOS pick | OOS RULES v2 | OOS SPY |
|---|---|---|---|---|
| U56 | QROLL q=0.17 d=1.00 W g=1.00 | **16.01% / 1.391 / −12.77%** | 9.48% / 1.279 / −12.05% | 15.32% / 0.876 / −33.72% |
| B136 | CORR 0.20 d=0.50 W g=1.00 | 12.50% / 1.037 / −17.37% | 7.98% / 1.119 / −12.24% | 15.45% / 0.882 / −33.72% |
| SMALL | ABS 0.40 d=1.00 W g=1.00 | 1.16% / 0.154 / −30.47% | 3.85% / 0.568 / −14.68% | 15.45% / 0.882 / −33.72% |

Picks beat RULES v2 OOS 1 of 3, SPY OOS 2 of 3.

---

# MEMO — new 4b KEEP-CANDIDATE (for Sunday review; NOT adopted here)

1. **Book.** U56 (`research/universe.json`), eligible names equal-weighted at **gross 1.00**,
   weekly rebalance, 10 bps — the run's `EWALL` base — with one de-grossing clause.
2. **Clause.** Panel breadth = share of priced names above their own 200-day MA. When breadth
   sits **below its trailing 1008-day 0.17 quantile**, hold **zero** (depth 1.00); otherwise
   hold the full book. State read at close *t*, applied at *t+1*. Fires 12.2% of days.
3. **Full sample @10 bps:** CAGR **14.13%**, Sharpe **1.2204**, MaxDD **−14.79%**,
   halves **1.1361 / 1.3038**, OOS 2017+ **16.01% / 1.3910 / −12.77%**.
4. **4b passes at 0, 10 AND 25 bps** (1.2993 / 1.2204 / 1.1015 full-sample Sharpe), with every
   leg clear — SPY 15.15% / 0.886 / −33.72%, halves 0.959/0.826, OOS 0.876.
5. **It is an EARNED pass:** the ungated g=1.00 base fails 4b on the DD cap at every rung
   (−20.75% vs the −20.23% cap); the clause cures the drawdown without losing the CAGR floor.
6. **It beats its own matched-gross twin** (a static EWALL at g_eff = 0.8777) by
   **+0.170 / +0.174 / +0.180** Sharpe at 0 / 10 / 25 bps — the margin *widens* with cost.
7. **It survives this run's placebo column:** QROLL/U56 REAL 1.000 vs BLOCK 0.250 (z 6.53), and
   its placebo-differenced excess is positive both in and out of sample.
8. **It transports to B136** (4b at all three rungs: 13.12% / 1.0844 / −16.18%, OOS 1.1796,
   twin margin +0.058) and **fails on SMALL** (0.4187 Sharpe, all five 4b legs fail).
9. **It was the rule-8 IS pick on U56**, not a post-hoc selection: chosen on 2009–2016 Sharpe
   alone and read once on 2017+.
10. **It FAILS 4a** (p4a False at every rung — it does not beat cost-matched RULES v2 in both
    halves), so under PROTOCOL 4 it is a 4b-only candidate; two tuned parameters (q, depth) and
    the same family idea 399/601 already studied at g=0.75, where it does **not** pass.

**Proposed RULES wording, if Sunday adopts it:**
> Hold every eligible name at 1/N of NAV (N = names priced and eligible that day), rebalanced
> weekly. Compute panel breadth b_t = share of priced names above their 200-day moving average.
> If b_t is below the 0.17 quantile of b over the trailing 1008 trading days, hold 100% cash
> until the next weekly rebalance at which b_t is at or above it. Decide at the close, trade at
> the next close.

**Caveats for the reviewer.** Survivorship: U56 and B136 are current-constituent lists, so CAGR
and drawdown levels are optimistic; the twin contrast is the durable part. The 1008-day window
is inherited from ideas 399/601, not fitted here. 4a fails. The clause is a full-exit rule and
its 12.2% firing rate means its record rests on a small number of episodes.

# Idea 332 — price the H2-for-DD exchange rate as a record-wide constant (cloud, 2026-09-07)

**KILL of the constant. The premise fails one level deeper than "the number varies": across the
cadence dial the move is not reliably a TRADE-OFF at all, so there is nothing for an exchange
rate to be the rate of. No RULES change, no book promoted, no KEEP claimed; RULES.md, scan.py,
bot.py and baseline.py untouched.**

Script: `2026-09-07_price-the-H2-for-DD-exchange-rate-as-a-record-wide-constant_cloud.py`
(console `.console.txt`; 108-row `.grid.csv`; 108-row `.pairs.csv`; 5,447-row `.census.csv`;
`.usability.csv`; `.walkforward.csv`).

## Definitions (fixed before any number was read)

`H2 margin = Sharpe(H2) − Sharpe(SPY,H2)`; `DD margin = 0.60·|MaxDD(SPY)| − |MaxDD(book)|`;
both are 4b bars, both must be > 0. `R = Δ(H2 margin) / Δ(DD margin)` over a cadence pair with
everything else held fixed. SPY is constant inside a panel, so `R = ΔH2 / −Δ|MaxDD|`, which is
why the census can pool files that never shared a benchmark alignment. `R < 0` is idea 329's
direction: slowing down buys H2 and pays drawdown.

## Reproduction gates (all PASS, before any new number was read)

| Gate | Result |
|---|---|
| `fast_backtest` vs `engine.backtest`, returns / turnover | **0.000e+00 / 0.000e+00** |
| derived rung `r(c) = r(0) − turnover·c/1e4` vs `engine.backtest(cost_bps=10)` | **0.000e+00** |
| idea 329's committed B136 n=20 m=20 W→M, re-derived from the definitions | ΔH2 **+0.1892** (pub +0.189), ΔDDm **−0.0588** (pub −0.059), **R = −3.217** (pub −3.2) |
| idea 329's B136 top-20 m=0 WEEKLY, rebuilt from this script's own book | 12.99% / 0.943 / −20.05%, H2 0.803 — **4/4 exact** |
| idea 329's B136 top-20 m=0 MONTHLY, rebuilt | 16.61% / 1.109 / −26.10%, H2 0.958 — **4/4 exact** |

## [A] The fresh corpus (108 books; all printed, all in `.grid.csv`)

Book: top-n eligible by the RULES v1 composite with the vol scaler OFF, v1 eligibility (above
the 200d MA, vol20 < 0.60), NORM weights `g/k_t`, next-day execution, 10 bps.
Tuned: **n ∈ {10,20,40} × cadence ∈ {W,2W,M,Q}** (2 parameters). Reported axes: gross ∈
{0.50,0.75,1.00}, panel ∈ {U56, B136, SMALL484}.

**KEEP paths over all 108 points: 4a 0/108, 4b 8/108** (all U56 and B136, all at gross ≤ 0.75;
RULES v2's −12.05% MaxDD dominates every cell on 4a). The eight: U56 n=20 W and M at g=0.75,
U56 n=40 W and M at g=0.75, U56 n=10 M at g=0.50, B136 n=10 and n=20 M at g=0.50, B136 n=40 W
at g=0.75 — i.e. the record's already-known U56 top-20/top-40 objects, not a new one.

## [A2] The exchange rate is not a constant — and mostly not an exchange rate

**Sign census (the scale-free reading; a ratio of two differences explodes when its denominator
is near zero, so the quadrant is prior to the number):**

| Quadrant | Fresh (108) | Archive (5,447) |
|---|---|---|
| STRICTLY WORSE — slowing loses H2 **and** DD margin | **49.1%** | **49.5%** |
| TRADE-OFF — buys H2, pays DD (idea 329's quadrant) | 39.8% | 33.4% |
| FREE LUNCH — buys both | 11.1% | 14.8% |
| REVERSE — loses H2, buys DD | 0.0% | 2.2% |

**R itself:** fresh corpus median **+0.766**, IQR [−2.384, +4.140], range **−48.7 … +72.8**;
with a denominator guard (|ΔDDm| ≥ 0.01, 91/108 kept) still **−20.2 … +22.1**. Archive: median
+1.265, 10–90 pct [−5.36, +6.56], range **−55.4 … +63.1**; only **5.3%** of 5,447 archival pairs
land within ±20% of idea 329's −3.217, and only **35.7%** even share its sign. Spread by axis
(fresh): panel 21.1–121.5 wide, n 41.1–121.5, gross 64.5–121.5. The gross-normalised candidate
`R × gross` does **not** rescue it (spread 84.3; medians +0.47/+0.48/+0.54 by gross) — Sharpe is
gross-invariant and MaxDD is not, so `R ∝ 1/g` is the *only* part of the variation gross
explains, and it is a small part.

**What does survive is a PAIR-TYPE statement, not a dial statement.** Idea 329 measured W→M, and
W→M is the one pair type where the trade-off is the norm: **22/27 fresh pairs in the trade-off
quadrant**, median R **−3.054**, range [−16.8, +2.5] — its −3.217 sits essentially at that
median. At the other end, **M→Q is 27/27 STRICTLY WORSE** on every panel, n and gross: past
monthly, slowing down loses H2 *and* drawdown, so the "slow down to buy H2" instrument is
bounded above by monthly and is not a dial that can be pushed. W→2W splits 12/12/3.

## [B] Archival census

**22 committed grid CSVs** carry a cadence dial with H2 and MaxDD; **5,447 pairs** priced.
A first pass returned 0 pairs on idea 329's own file: it stores `gross` as a *realised* mean
(45 distinct values on 45 rows), so grouping on it fragments every group. The census now drops
key columns that cannot group (nunique > rows/3) and **skips** any group where a cadence repeats
(the signature of over-merging), which is strictly conservative. Idea 329's file then yields 43
pairs, R ∈ [−13.8, +40.5], containing its own −3.217.

## [C] Is the constant usable? No — it does no work

The queue's deliverable: from ONE weekly cell, cadence closes the H2 bar without breaking the DD
cap iff `DDmargin_W − |H2deficit_W / R| > 0`. Scored against the observed monthly cell, 27 cells:

| Rule | Accuracy |
|---|---|
| leave-one-panel-out R | 88.9% (24/27) |
| **CONTROL: R = ∞ (no exchange rate at all — predict on `DDmargin_W > 0`)** | **88.9% (24/27)** |
| CONTROL: R = −3.217 held fixed | 92.6% (25/27) |
| majority class | 70.4% |

No variant separates from the R-free control by more than one cell of 27. The +18.5% edge over
the majority class is carried entirely by "does the weekly cell already have DD margin"; the
exchange rate is decoration. Confusion (LOO): TP 7, FP 2, FN 1, TN 17.

## [D] Rule 8 walk-forward (n × cadence chosen on ≤2016 by IS Sharpe @10 bps, gross pinned 0.75)

| Panel | Pick | OOS CAGR | OOS Sharpe | OOS MaxDD | W n=20 anchor OOS | RULES v2 OOS | SPY OOS | Regret | Full-sample 4b |
|---|---|---|---|---|---|---|---|---|---|
| U56 | n=10, M | 18.09% | **1.131** | −23.22% | 1.131 | 1.285 | 0.882 | +0.177 | FAIL (DD) |
| B136 | n=10, Q | 14.42% | **0.804** | −28.61% | 0.884 | 1.119 | 0.882 | +0.340 | FAIL (H2, OOS, DD) |
| SMALL484 | n=10, M | 8.31% | **0.484** | −34.17% | 0.466 | 0.568 | 0.882 | +0.123 | FAIL (H1,H2,OOS,DD,CAGR) |

SPY OOS: 15.45% / 0.882 / −33.72%. The honest chooser beats SPY OOS on U56 only (+0.249), ties
the weekly anchor there, and **loses to SPY on B136 (−0.078) and SMALL484 (−0.398)**; it clears
no KEEP path on any panel and is beaten by the live book on all three. Consistent with idea 333:
the IS window prefers narrow (n=10) everywhere and that preference does not pay OOS.

## Verdict

**KILL** of "the H2-for-DD exchange rate is a record-wide constant of the cadence dial", on three
independent grounds: the sign is not fixed (49% of moves lose both margins), the magnitude spans
two orders of magnitude on every axis the queue asked about, and the constant adds nothing to a
rule that ignores it. **Two by-products worth carrying forward:** (1) the trade-off reading is
specific to **W→M**, where it holds 22/27 with median R −3.05 — quote it as a pair-type statement
or not at all; (2) **M→Q is 27/27 strictly worse**, so cadence as an H2 instrument is bounded
above by monthly — a free pre-screen that kills quarterly arms without running them.

## Caveats

(1) All three panels are current-constituent lists — **SURVIVORSHIP** — which flatters every
momentum book; a ratio of two differences inherits the bias of both. The small panel is the worst
offender (sub-$2B names surviving to 2026-09); the 44 tickers with `max_1d_move ≥ 1.0` in
`data/small_meta.csv` are dropped first, leaving 439 names. (2) SMALL484 starts 2010-01-04, so
its halves and IS window are not the same calendar as U56/B136. (3) 2W decimates the weekly mask
(every 2nd week-end), phase-anchored to the panel's first complete week; another phase is an
unreported choice. (4) The archive census pools files with different books, costs and
conventions — it prices the SPREAD of R, which is the question, not a pooled estimate of R. It
also re-reads this run's own `.grid.csv` (158 of 5,447 pairs, 2.9%), listed in the per-file table
in the console. Excluding it (5,289 pairs) leaves every quoted figure intact: median +1.261,
10–90 pct [−5.44, +6.55], same range, negative 35.7%, within ±20% of −3.217 5.2%, and quadrants
49.2 / 33.4 / 15.0 / 2.3%.

# Idea 65 — cadence-sensitivity-as-a-KEEP-test (lane B, 2026-09-06)

**Verdict: KILL of cadence-insensitivity as a pre-registered KEEP bar — on both readings.**
As a *verdict* bar it is degenerate (it rejects 15 of 15 arms that pass 4b weekly, keeping
**0 of 48**). As a *chooser* it is a re-labelling of turnover (rank-corr with log turnover
**+0.92 to +0.99** inside every cell) and is worth **+0.000 OOS Sharpe in 3 of 4 cells and
-0.106 in the fourth**. No KEEP-candidate, no RULES change. **4a 0 of 192, 4b 35 of 192.**

Script: `research/backtests/2026-09-06_cadence-sensitivity-as-a-KEEP-test_B.py`
Console: `2026-09-06_cadence-sensitivity-as-a-KEEP-test_B.console.txt`
Grid CSV: `2026-09-06_cadence-sensitivity-as-a-KEEP-test_B.grid.csv` (all 192 points)

## Design

192 points = 2 universes (`universe.json` 56 names, `universe_broad.json` 136) x 12
pre-existing published books x 4 cadences {D,W,M,Q} x 2 cost rungs {10, 25 bps}. Every
point printed. Books are taken as given from the record (v1, v2-live, top12/20/30, ew-all,
ew-band3, ew-band5, frac55/70/85, ew-nogate) so the cadence axis is the only thing that
moves; nothing is tuned here. Two tuned numbers total: the bar's tolerance TAU (pre-registered
0.05, with the whole span distribution printed so any TAU can be read off) and the cadence
set itself. Rule 8: the span used for prediction is computed on **2009-2016 only**; 2017-2026
is read afterwards, untouched.

**Reproduction gates 3/3 EXACT.** On the record's own sample end (`2026-09-03`; the cache has
since gained one trading day) the harness returns idea 2's `top20` at **12.7%/1.093/-18.3%**,
idea 57's `ew-band3` at **11.3%/1.136/-15.1%** and idea 3's `ew-all` control at
**10.4%/1.050/-15.9%** — the published rows to the decimal. Analytic-cost identity vs a real
`cost_bps=10` engine run: max|diff| **0.000e+00**.

## Result 1 — the bar as proposed rejects everything (Q1)

15 of the 48 (universe, cost, book) arms pass 4b at the incumbent weekly cadence. Requiring
the 4b verdict to survive all of D/W/M/Q keeps **0 of them**. Across all 48 arms: **0
pass-all, 26 fail-all, 22 FLIP.** The bar has a 100% rejection rate and therefore carries no
information — it cannot separate candidates because there are no survivors to separate.

The mechanism is not robustness of the edge, it is the **MaxDD cap**: the quarterly arm
drifts furthest between rebalances and blows through it. Of the 15 arms that pass 4b weekly,
the quarterly version fails in **15 of 15, and on `DD` in 15 of 15**; across the whole grid
`Q` fails 4b on `DD` in **46 of 48** arms. The bar is a single-cadence veto wearing four
cadences. Idea 3's own cadence set was D/W/M; on that narrower bar 2 arms survive
(`ew-band3` and `ew-band5`, u56 @10bps only).

**The three standing candidates, as asked (all 4 universe x cost cells each):**

| candidate | u56 @10 | u56 @25 | broad @10 | broad @25 |
|---|---|---|---|---|
| idea 2 `top20` | span 0.228, 2/4 | 0.481, 1/4 | 0.339, 0/4 | 0.630, 0/4 |
| idea 46 `frac85` | 0.228, 2/4 | 0.513, 1/4 | 0.129, 1/4 | 0.383, 0/4 |
| idea 57 `ew-band3` | **0.071**, 3/4 | 0.062, 1/4 | **0.020**, 2/4 | 0.058, 0/4 |

`span` = max-min full-sample Sharpe over D/W/M/Q; the second number is how many of the 4
cadences pass 4b. **All three FAIL the DWMQ bar in all 4 cells.** Idea 3's observation that
`ew-band3` is the cadence-insensitive one is confirmed on the *magnitude* — its span is 3x
to 17x smaller than `top20`'s and it is the only standing candidate to survive idea 3's DWM
bar — but the survival is confined to u56 @10bps and does not reach the 25 bps rung on either
panel. Across all 48 arms the worst cadence is `D` in **37 of 48** and the best is `M` in
**35 of 48**.

## Result 2 — the continuous version predicts OOS, and the predictor is turnover (Q2/Q2c)

Ranking arms by the **in-sample (2009-2016) cadence span** is strongly and sign-consistently
related to out-of-sample outcome:

- Spearman(IS span, OOS weekly Sharpe) = **-0.780 pooled**, and **-0.811 / -0.958 / -0.965 /
  -1.000** in the four (universe, cost) cells — negative 4/4.
- Median split on IS span: LOW half mean OOS Sharpe **1.115** (+0.233 vs SPY), HIGH half
  **0.846** (-0.036 vs SPY); difference **+0.270, t +5.40**.

This looked like a real ex-ante robustness signal. It is not a *new* one. Inside each
(universe, cost) cell, where the 12 books have 12 distinct turnovers at one cost rung:

| cell | Sp(span, OOS) | Sp(log turnover, OOS) | Sp(span, log turnover) | **partial Sp(span, OOS \| log turnover)** |
|---|---|---|---|---|
| u56 @10 | -0.811 | -0.839 | **+0.923** | -0.175 |
| u56 @25 | -0.958 | -0.930 | **+0.979** | -0.634 |
| broad @10 | -0.965 | -0.972 | **+0.965** | -0.438 |
| broad @25 | -1.000 | -0.986 | **+0.986** | -1.000 |

The cadence span is a **monotone transform of turnover** (+0.92 to +0.99 in every cell), and
turnover predicts OOS at least as well as the span does in 3 of 4 cells. Pooled, partialling
log turnover out cuts the association from -0.780 to **-0.297**; the per-cell partials are
unstable (-0.175 to -1.000) because span and turnover are near-collinear at n=12, which is
itself the finding. The record already knows turnover is the binding term (ideas 273/279:
corr(turnover, Sharpe) -0.946/-0.986), so the span adds a second name for a term already in
the book.

## Result 3 — as a chooser it is worth nothing (Q2b, rule 8)

Selection on 2009-2016 weekly Sharpe only, OOS read afterwards:

| cell | unbarred pick | OOS | barred pick (span<=median) | OOS | bar worth |
|---|---|---|---|---|---|
| u56 @10 | v2-live | 1.285 | v2-live | 1.285 | **+0.000** |
| u56 @25 | v2-live | 1.248 | v2-live | 1.248 | **+0.000** |
| broad @10 | ew-nogate | 1.101 | ew-nogate | 1.101 | **+0.000** |
| broad @25 | ew-nogate | 1.073 | ew-nogate | 1.073 | **+0.000** |

At the pre-registered TAU=0.05 the bar admits **no book at all** in 3 of the 4 cells and in
the fourth admits exactly one — the book the unbarred chooser already picked. Choosing by
minimum span *instead of* IS Sharpe is worse on average: u56@10 picks `ew-nogate` (OOS 1.179)
over `v2-live` (OOS 1.285), **-0.106**; the other three cells tie or gain +0.001. And the
min-span pick equals the **min-turnover** pick in 3 of 4 cells — the two rules are the same
instrument.

## What this means for the protocol

Do **not** add cadence-insensitivity to PROTOCOL rule 4. It rejects every candidate the
record has, it does not survive the addition of a fourth cadence, its apparent predictive
content is turnover, and it changes no selection. If a turnover-flavoured robustness bar is
wanted, rank on realised turnover directly — it is cheaper (no extra backtests), it is
already measured on every arm, and it predicts OOS at least as well in 3 of 4 cells.

Two by-products worth keeping in the record: (1) **4a is 0 of 192** — RULES v2 is beaten
nowhere in this book family at either cost rung, consistent with the standing finding that
4a's drawdown clause kills every growth book; (2) the **quarterly cadence fails 4b on the
MaxDD cap almost universally**, which is a cleaner statement of idea 3's "monthly buys return
with drawdown" than idea 3 could make with three cadences.

**Survivorship:** both lists are current constituents, so absolute CAGR/Sharpe are optimistic.
The cadence-vs-cadence comparisons are far less exposed — every arm holds the same names on
the same days and differs only in when it trades.

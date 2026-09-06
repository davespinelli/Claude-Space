# Idea 182 — monthly-r6-top20-as-a-single-hypothesis (cloud, 2026-09-06)

**VERDICT: KEEP-candidate via PROTOCOL path 4b, SCOPED TO universe.json (u56).** The
pre-registered book clears 4b in **9 of 9 u56 cells** — every cost rung (5/10/25 bps) crossed
with every execution lag (t+1, t+5, t+7) — full-sample **and** on the OOS window alone, and it
survives **400/400 composition draws at 10 bps**. It still **fails the universe change**: 0 of 9
cells on broad and 0 of 9 on small, on the drawdown cap both times.

## The book, fixed before any number was read — nothing tuned

`R6 = px/px.shift(126) − 1`, divided by `vol20.clip(0.08)**0.5`; gate `px > 200d MA AND
vol20 < 0.60`; top 20 by that signal, equal weight, gross 0.75 (cash for empty slots); **monthly**.
Panel, cost rung, execution lag and composition draw are audit axes, not parameters.

**Note for the record:** idea 173's ANCHOR carries `p = 0.5`, so the published R6 book **does**
carry RULES v1's vol scaler. The QUEUE line does not say so; control [c] proves it — this exact
config reproduces the committed 13.61% / 1.1557 / −18.81%.

All four controls PASS: **[b]** the lag-1 simulator equals `engine.backtest` at 1.735e-17 and
cost linearity at 1.735e-17; **[e]** the composition-draw shortcut equals the published
`weights()` on the subset panel at **exactly 0.000e+00**; **[c] the decisive one — the (u56, R6,
M, t+1) rows at 10 and 25 bps reproduce idea 173's committed grid.csv on all 11 columns at
4.441e-16.**

## u56 — 9 of 9 cells clear 4b, full-sample and OOS-window

| lag | bps | CAGR | Sharpe | MaxDD | H1 | H2 | OOS CAGR | OOS Sharpe | turn/yr | 4b | 4b margin |
|---|---|---|---|---|---|---|---|---|---|---|---|
| t+1 | 5 | 13.88% | 1.1763 | −18.78% | 1.250 | 1.121 | 14.83% | 1.1892 | 4.82 | **PASS** | +0.072/DD |
| t+1 | 10 | 13.61% | 1.1557 | −18.81% | 1.228 | 1.102 | 14.56% | 1.1695 | 4.82 | **PASS** | +0.070/DD |
| t+1 | 25 | 12.79% | 1.0937 | −18.90% | 1.161 | 1.044 | 13.72% | 1.1102 | 4.82 | **PASS** | +0.066/DD |
| t+5 | 10 | 12.92% | 1.0822 | −17.61% | 1.145 | 1.038 | 13.95% | 1.0997 | 4.80 | **PASS** | +0.129/DD |
| t+7 | 10 | 12.86% | 1.0670 | −20.01% | 1.102 | 1.046 | 14.22% | 1.1075 | 4.82 | **PASS** | **+0.011/DD** |
| t+7 | 25 | 12.05% | 1.0068 | −20.10% | 1.037 | 0.989 | 13.40% | 1.0504 | 4.82 | **PASS** | **+0.006/DD** |

SPY on u56: 15.23% / 0.8890 / −33.72%, halves 0.957/0.834, OOS 15.45% / 0.8820 / −33.72%.
RULES v1 @10 bps: 6.45% / 0.6642 / −13.83%, OOS 7.73% / 0.7471 / −13.83%.

**The binding bar is the drawdown cap in all 27 cells.** At t+1 the margin is 1.4pp of MaxDD
(−18.81% against the −20.23% cap); at t+7 it is **0.2pp** (−20.01%). A one-calendar-week fill
nearly exhausts the cap. **4a fails everywhere at 5 and 10 bps** on the same drawdown comparison
against the live book's −13.83% — which is exactly the case rule 4b was added for.

## Idea 53 composition draws — the fitted-list objection does not survive

Drop 5 and 10 names at random, 200 draws each, seed 182, t+1:

| panel | drop | bps | 4b pass rate | 4b-OOS rate | Sharpe mean | Sharpe p05 | mean 4b margin |
|---|---|---|---|---|---|---|---|
| u56 | 5 | 10 | **100.0%** | 100.0% | 1.1393 | 1.0873 | +0.099 |
| u56 | 10 | 10 | **100.0%** | 100.0% | 1.1372 | 1.0591 | +0.129 |
| u56 | 5 | 25 | **100.0%** | 100.0% | 1.0802 | 1.0276 | +0.088 |
| u56 | 10 | 25 | **96.5%** | 99.5% | 1.0809 | 1.0007 | +0.098 |
| broad | 5/10 | 10/25 | **0.0%** | 0.0% | 1.129 / 1.052 | 1.095 | −0.207 |
| small | 5/10 | 10/25 | **0.0%** | 0.0% | 0.488 / 0.396 | 0.449 | −0.898 |

The 5th-percentile Sharpe over 400 u56 draws is **1.0591** — above SPY's 0.8890 in every draw.
The single failing configuration is drop-10 at 25 bps (7 of 200 draws), where the **CAGR floor**
takes over from the DD cap as the binding bar in 49% of draws. **This is not a claim about 55
particular tickers.**

## PROTOCOL rule 8 — the walk-forward picks M by itself on u56

The published M was 1 of 90 grid selections chosen with the whole sample visible, so the
walk-forward asks what an IS-only chooser would have done. On the R6 cadence ladder D/W/M/Q,
parameters on ≤ 2016-12-31 only, OOS read once:

| panel | bps | CONST-W | IS-PICK | FIXED-M | ORACLE |
|---|---|---|---|---|---|
| u56 | 5 | 1.1265 | **M 1.1892** | M 1.1892 | M 1.1892 |
| u56 | 10 | 1.0809 | **M 1.1695** | M 1.1695 | M 1.1695 |
| u56 | 25 | 0.9438 | **M 1.1102** | M 1.1102 | M 1.1102 |

On u56 **IS-PICK = FIXED-M = ORACLE at all three cost rungs**: the in-sample-only chooser lands
on monthly by itself, and monthly is also the out-of-sample argmax. The cadence is not a
hindsight pick here. Across all 9 (panel, cost) cells the IS chooser lands on M in 6/9; the
exceptions are broad @25 bps and small @25 bps, where it picks Q and loses (small: −0.1911 vs
CONST-W).

## Where it fails, stated plainly

**broad**: 0/9 cells, DD margin −0.211, MaxDD −24.5% against the −20.23% cap, in every one of
400 draws. **small**: 0/9, margin −0.890, failing H1, H2, OOS, DD *and* CAGR. The book is a
u56 result. Ideas 44/53 flagged exactly this for idea 2's candidate; the same limitation applies
here, and the composition draws separate the two objections cleanly — **composition is fine, a
different universe is not.**

## One thing this book has that the record's other cadence claims do not

Ideas 187/221 established that a multi-unit-block cadence point is an alignment draw: at 6W the
per-book phase spread is 0.379 and the argmax phase agrees across books 73% of the time.
**MONTHLY is a k=1 calendar block — it has exactly one phase**, so this point carries no
block-phase alignment draw at all. That is a property of the cadence, not evidence for the book,
but it means the usual "which weeks did it trade" objection does not apply.

## Caveats

SURVIVORSHIP: universe.json, universe_broad.json and the small panel are current-constituent
lists (idea 54); the small panel drops the 44 max_1d_move ≥ 1.0 tickers. **The composition draws
resample within a survivor list — they bound sensitivity to composition, not survivorship, and
no level here is an attainable return.** Idea 38: the large-cap panels are calendar-day indexed
after 2014-09-17, which is why both a 5-bar and a 7-bar lag are reported rather than one
"1-week" number. 4b's own bars are relative to SPY over this sample and inherit its regime.

RULES.md, scan.py, bot.py, baseline.py untouched. Memo with exact RULES wording:
`2026-09-06_monthly-r6-top20-as-a-single-hypothesis_cloud.memo.md`.

# Idea 350 — is the BINDING drawdown episode a HIGH-BREADTH event across the record?

**ANSWERED (2026-09-07, lane C). The queue's premise is FALSIFIED as worded, its
conclusion survives in a weaker form, and the mechanism idea 41 saw is something else:
a RUNNER-UP FLOOR. No RULES change; one 4b KEEP-candidate filed as a by-product.
RULES.md, scan.py, bot.py and baseline.py untouched.**

## Reproduction gates (all PASS, before any new number was read)
* derived rung identity `r(c) = r(0) - turnover*c/1e4` vs `engine.backtest(cost_bps=25)`: **0.000e+00**
* idea 40/41 U56 controls: NONE n=3 **21.9% / 1.04 / -25.8%** (H1 1.01 / H2 1.06), n=5 **16.5% / 0.95 / -21.6%**
* LIVE RULES v2 U56: **8.66% / 1.2056 / -12.05%** (halves 1.2259 / 1.1908)
* idea 41's own committed breadth-gate cells (U56 n=3, B=0.30, 10 bps): MaxDD **-0.205534**
  at multiplier 0.50 AND 0.00, matching its grid to 6 decimals. CAGR differs in the 4th
  decimal only (0.2097 vs 0.2095) because this file excludes SPY from breadth and idea 41
  included it.

## What was censused
6 canonical book forms (EWALL, TOP3, TOP10, TOP20, MAEW, RULES v2) x 3 panels (U56, B136,
SMALL439) x 3 rungs (0/10/25 bps) = **54 stamped books**; each one's maximum-drawdown window
date-stamped and decomposed against panel breadth. Overlay grid = 54 books x B in
{0.30, 0.40, 0.50} x depth in {0.25, 0.50, 1.00} = **486 points, all reported**. Two tuned
parameters (B, depth); book form, panel and rung are reported axes, not tuned.

## [1] The premise, as worded, is FALSE
The binding drawdown window's mean breadth is **below its panel's unconditional mean in 54
of 54 books** — median percentile **0.169** among all same-length windows on the same panel
(max 0.236). The binding episode is a distinctly LOW-breadth window, not a high-breadth one.

## [2] The premise's CONCLUSION survives, as a LAG statement
Breadth falls during the episode, so the loss front-runs the signal. Share of the window's
down-day loss taken while a gate armed below B would still be OFF: median **0.793** at
B=0.30, 0.705 at 0.40, 0.533 at 0.50 (signed loss shares 0.692 / 0.787 / 0.737). So roughly
four fifths of the binding loss is already booked before a 30% gate arms — the gate is
**late, not misaimed**. It is not universal: on U56 TOP3 — idea 41's own book — the share is
**0.017**, i.e. the gate is armed through essentially the whole episode.

## [3] The real mechanism behind idea 41's saturation: a RUNNER-UP FLOOR
Where the overlay is deep enough to displace the binding episode (**230 of 486 points**), the
RESIDUAL binding window is one whose down-day loss is **98.3% (median) taken above the gate's
own threshold** — ≥ 0.99 in 87 of those 230. On U56 TOP3 the gate cuts the Jun-Sep 2022
episode and the drawdown moves to **2021-11-05 → 2022-01-24**, which the gate cannot reach at
any depth; hence MaxDD is **identical (-0.205534) at every depth**, exactly as idea 41
reported. MaxDD is a min-statistic: overlay improvement saturates at the second-worst
episode, whatever the first one's breadth was.

## [4] The family is NOT retirable — but it does not earn its keep
486 points: median dDD **+1.154 pp** (positive in 393/486), median dCAGR **-0.762 pp**, median
dSharpe **-0.0196** (positive in only 125/486), beats idea 351's free-exposure numeraire in
**204/486**. KEEP paths: **4a 24/486** (all at 0 bps), **4b 52/486** (36 / 13 / 3 at 0 / 10 /
25 bps; U56 42, B136 10, **SMALL439 0**). Rank correlation between a book's "loss taken above
B" share and the gate's dDD is **-0.53 / -0.55 / -0.40** at B = 0.30 / 0.40 / 0.50 — the
census statistic PREDICTS which books a breadth gate can help, which is the usable finding.

## [5] Rule 8 (menu = gate-OFF + 9 cells, chosen on IS ≤ 2016 Sharpe, 10 bps)
The chooser takes the gate in 11 of 18 books. OOS Sharpe beats its own ungated control in
**5 of 18** (median dOOS **+0.0000**), OOS MaxDD in 10 of 18 (median +0.516 pp), median
regret 0.0376. OOS Sharpe > SPY (0.882) in 10 of 18; > RULES v2 OOS (1.285 U56 / 1.119 B136 /
0.566 SMALL439) in **2 of 18**. On SMALL439 the chooser picks a full cut in 5 of 6 books and
gives back 0.16-0.20 of OOS Sharpe.

## Verdict
**ANSWERED / no rule change.** The "wrong window" argument for retiring breadth-gated
overlays is not supported: the window is reachable in principle, the gate is simply late, and
what caps it is the runner-up episode. The family should be retired on the numbers that
actually matter — a negative median dSharpe and a 5-in-18 out-of-sample record against
do-nothing — not on the premise the queue proposed. One 4b KEEP-candidate falls out (U56
equal-weight + breadth gate at B=0.40, depth 0.50 — see the memo), rule-8 selectable, but
single-panel.

## Caveats
All three panels are current-constituent lists (SURVIVORSHIP), so drawdown LEVELS are
optimistic and the 4b DD cap is a level test; the loss-share decomposition is within-window
and is not affected. SMALL439 drops 44 tickers with max_1d_move ≥ 1.0 and starts 2010-01-04,
so its halves are not the same calendar halves. The sample starts 2009-01-13 (260-day
warm-up), so the GFC is only partly inside it and the binding episode for most books is 2020
or 2022. Breadth on a 200d MA is lagging by construction — that is the hypothesis under test,
not a measurement defect.

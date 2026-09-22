# Idea 2223 — does a NO-TRADE BAND on the CORE band book buy back what the SLEEVE costs?
lane cloud, 2026-09-22, run 11. Script: `2026-09-22_core-no-trade-band_cloud.py`

## Question
Idea 2213 priced the idle-NAV sleeve's turnover lift (1.92x -> 3.03x/yr) but left the CORE
weights rebalanced every week. This run puts a drift tolerance on the core leg and asks two
things: (i) can it return ~1.11x/yr of turnover to the budget, and (ii) does the book that
results clear either KEEP path.

## Construction
Live RULES v2 book (hold every name inside the 200d +/- c band at gross 0.75 / N, weekly,
next-day execution). At each weekly rebalance the L1 distance between the rule's target and
the DRIFTED holdings is compared with `tol`; inside the tolerance the book does not trade at
all. Exactly two tuned parameters: `tol` and `c`. Two arms on the same two parameters —
**LAZY-ALL** (the tolerance blocks every trade, exits included) and **LAZY-KEEPEXIT** (names
that have gated OUT are always sold; the tolerance governs the rest).

Grid: tol in {0, .02, .04, .06, .08, .10, .15, .20, .30, .40} x c in {.02, .03, .05, .08},
2 arms x 2 panels (U56, B136) x 3 cost rungs (10/25/50 bps) = **480 cells, all reported** in
`.grid.csv`; the 10 bps grid is printed in full in `.log.txt`.

## Gates (pre-registered, printed before any hypothesis was read) — 16 of 16 PASS
G1/G2 the lazy runner reproduces `engine.backtest` on `rules_v2_weights` at tol=0 to
**0.000e+00** on both returns and turnover, on both panels — the tolerance axis starts at the
live book itself. G3 at tol=99 the book trades once and never again (post-inception turnover
0.000e+00). G4 the 25 bps rung equals the 10 bps returns minus 15 bps x turnover to 3.5e-18:
the cost axis is an identity, not an interpolation. G5 max target gross 0.7366 (U56) /
0.7137 (B136) — never levered, never short. G6 the two arms are genuinely different books.
G7 17.65 years per panel. G8 56 / 136 names.

## Result — 4b KILL everywhere, on the CAGR floor, with the DD cap slack
**0 of 480 cells clear 4b.** The binding leg is the CAGR floor at every single cell. Best
CAGR reached anywhere on the grid is **0.613 x SPY** (U56, c=.05 tol=.40) and **0.595 x SPY**
(B136, c=.03 tol=.30) against the 0.70 floor, while the drawdown cap is not close to binding
(0.445 / 0.461 of SPY's -33.72% against the 0.60 allowance). This reproduces the record's
standing finding from a new direction: the band book is short of RETURN, and a turnover
rebate is not where return comes from.

## Result — 4a: one cell in 80 at 10 bps, and no chooser can reach it
At the headline 10 bps rung exactly **one** of 80 cells clears 4a: LAZY-KEEPEXIT, U56,
c=0.02, tol=0.08 — CAGR 8.43% / Sharpe 1.2114 / MaxDD -11.97% against the live book's
8.62% / 1.2010 / -12.05%, i.e. +0.0104 of Sharpe held by H1 +0.0132 and H2 +0.0082 and a DD
6 bp shallower. It is at a band c the live book does not use, it is one cell out of eighty,
and **the rule-8 chooser never picks it**. The 4a count rises at 25 bps (7 cells) and 50 bps
(16 cells) — the pattern the record has already named a duration/cost artefact: a turnover
rebate is worth more the more each unit of turnover costs.

## Rule 8 walk-forward (choose on IS = to 2017-11-10, read OOS untouched) — fails 12 of 12
The IS-Sharpe chooser lands on the **loosest rung of the grid (tol 0.30 or 0.40) in all 12
(panel, arm, cost) cells** — a grid edge, not an interior argmax. Out of sample the picked
book **loses to the live baseline in 12 of 12**: U56 10 bps LAZY-ALL OOS 9.08% / 1.0947 /
-12.59% and LAZY-KEEPEXIT 7.53% / 1.0950 / -11.20% against live RULES v2 OOS 8.93% / 1.1806 /
-12.05%; B136 10 bps 6.52% / 0.8130 / -13.37% and 5.91% / 0.8351 / -14.01% against live
7.01% / 0.9669 / -12.24%. SPY OOS 14.82% / 0.8264 / -33.72%. The tolerance beats SPY's OOS
Sharpe in 4 of the 6 U56/B136 10-25 bps picks, but that leg was never the binding one.

## The idea's own question, answered in turnover units
On U56 at the live band c=0.03, annual turnover runs 1.774x (tol=0, the live book) ->
1.223x (tol=.10) -> 0.892x (tol=.20) -> 0.718x (tol=.30) -> 0.505x (tol=.40). So **yes, the
core leg can return the sleeve's whole +1.11x/yr lift** — a tolerance of about 0.31 does it.
It is not free: that cell costs **-0.103 of full Sharpe (1.0984 vs 1.2010), -0.122 of OOS
Sharpe, and 3.3 pp of MaxDD (-15.36% vs -12.05%)**. The core band therefore funds the sleeve
in QUANTITY but not in QUALITY, and since the sleeve itself was killed on 4b (idea 2227) and
is 4a-adoptable only through its own no-trade band (idea 2231), there is nothing left to fund.

## Verdict
**KILL (4b)** — 0 of 480 cells, CAGR floor binding in 100% of fails, DD cap binding in 0%.
**KILL (4a in the rule-8 sense)** — the single 10 bps 4a cell is unreachable by any IS-only
chooser, and the chooser's own picks lose to the live book OOS in 12 of 12.

## Honest limits
Survivorship (PROTOCOL rule 9): U56 and B136 are current-constituent panels. One gross
(0.75), one cadence (W), one weekday offset, one split point. The tolerance is on the total
L1 distance to the drifted book; a per-name tolerance is a different (untested) device. The
4a margin on the one passing cell (+0.0104 of Sharpe) sits inside the record's own measured
paired-bootstrap SE for a Sharpe contrast, which is a further reason not to read it as a find.

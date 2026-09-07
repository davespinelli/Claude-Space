# Idea 136 — the-small-panel-has-no-defensive-class (cloud, 2026-09-07)

**SPLIT: the QUESTION is answered — it is THE PANEL, not the bars — and the queue's stated
DIAGNOSTIC is FALSIFIED. Rules unchanged; no new KEEP (4a 1/540 across all three panels, 4b
0/180 on the small panel at every cost rung including 0 bps).**

The small panel has no defensive books because it has no good books: its arms fail the three
Sharpe bars **180 of 180**, and the drawdown cap fails on **155 of 180** as well — so the
failure signature is not "H1/H2/OOS but not the DD cap", it is "everything".

## What was run

540 rows = 3 panels x 5 books x 4 overlays x 3 gross rungs x 3 cost rungs, each scored against
TWO references (SPY and IWM) on TWO windows (each panel's own, and the common one). Exactly
two tuned parameters: book width n and gross g. Panel, overlay, cost, reference and window are
census axes.

- **panels** SMALL439 = the 483-name sub-$2B panel minus the 44 tickers with
  `max_1d_move >= 1.0` in `data/small_meta.csv` (gate G3, 439 traded names); U56 (55 traded);
  B136 (135 traded).
- **books** TOP5 / TOP10 / TOP20 / TOP40 (v1 composite without the /sqrt(vol20) term, eligible
  = above the 200d MA and vol20 < 0.60, equal weight at g/k, k = min(n, E_t)) and EWALL (equal
  weight over every eligible name) — the construction that supplied idea 129's Pareto-best
  defensive members.
- **overlays** CTRL, G200 (cash while lagged panel breadth < 0.50), VT10 (vol target 0.10),
  DD10 (half gross while the book's lagged drawdown is worse than -10%); book-level, idea 41's
  convention verbatim.
- **gross** 0.53 (idea 129's published defensive mean gross), 0.75 (the live rung), 1.00.
- **costs** 10 and 25 bps, plus a **0-bps diagnostic rung** — never a KEEP rung, present only
  to separate "the panel has no defensive books" from "costs ate them".

Two controls the queue does not ask for and the comparison cannot survive without:

1. **Window control.** The small panel opens 2010-01-04, so its evaluation window starts
   2011-01-13, while idea 133 read u56/broad from 2009. Every panel is therefore re-read on
   the COMMON window as the primary table. It does not rescue the small panel: U56's defensive
   count is 38/180 common vs its own-window number, B136's 24/180, SMALL439's **0/180 on both**.
2. **Bars control.** "SPY's reference numbers being wrong for a small-cap panel" is directly
   testable — re-score all five bars against **IWM**, which is investable, in
   `data/prices.csv`, and not survivorship-screened. IWM's own numbers on the common window:
   CAGR 10.21%, Sharpe 0.552 (H1 0.620 / H2 0.511 / OOS 0.520), MaxDD -41.13% — a much lower
   bar than SPY's 14.13% / 0.862 (0.891 / 0.858 / 0.882) / -33.72%.

Gates, all 0.000e+00: `fast_bt` == `engine.backtest` on returns AND turnover at 0 and 25 bps;
overlay at OFF (m == 1) == parent on r / turnover / gross; the 44 dropped tickers absent from
the traded panel and exactly 439 names traded; zero weight on benchmark columns (SPY and IWM
on the small panel, IWM everywhere); bar arithmetic == `engine.metrics` on RULES v2.

## The decomposition (common window, SPY reference)

| panel | n | fail H1 | fail H2 | fail OOS | fail DD | fail CAGR | pass 4b | defensive | pass 4a |
|---|---|---|---|---|---|---|---|---|---|
| SMALL439 | 180 | **180** | **180** | **180** | **155** | 177 | 0 | **0** | 0 |
| U56 | 180 | 68 | 27 | 32 | 37 | 86 | 50 | 38 | 0 |
| B136 | 180 | 57 | 108 | 98 | 61 | 89 | 27 | 24 | 1 |

Only two failing-bar signatures exist on the small panel: **H1,H2,OOS,DD (155 arms)** and
H1,H2,OOS (25 arms). Arms with zero non-floor failures — the defensive candidate set —
SMALL439 **0/180**, U56 88/180, B136 51/180.

How far each bar misses on SMALL439 (failing arms only): H1 median **-0.515** Sharpe (worst
-1.023, closest -0.165); H2 median -0.705; OOS median -0.603; DD median -13.4pp of drawdown
(worst -53.2pp, closest -0.6pp). These are not near misses. The median small-panel arm at
10 bps runs CAGR 2.8% / Sharpe 0.305 / MaxDD -30.6%, against U56's 10.4% / 1.012 / -15.5% and
B136's 10.1% / 0.906 / -16.9% on the identical window.

## Panel, or bars?

Re-scored against IWM instead of SPY, on the common window:

| panel | fail H1 | fail H2 | fail OOS | fail DD | pass 4b | defensive |
|---|---|---|---|---|---|---|
| SMALL439 | **171** | **168** | 147 | 123 | 1 | **0** |
| U56 | 1 | 0 | 0 | 8 | 144 | 27 |
| B136 | 6 | 12 | 10 | 29 | 123 | 17 |

Against a benchmark whose full-sample Sharpe is 0.552, the small-panel arms still fail H1 on
171 of 180 and H2 on 168 of 180, and produce **zero** defensive members. The bars are not
mis-calibrated: the books lose to a small-cap index, not just to SPY.

**And it is not costs either.** At the 0-bps diagnostic rung the best small-panel arm anywhere
in the grid is TOP10 at gross 1.00 with no overlay: CAGR 13.2%, **Sharpe 0.602**, MaxDD
-39.9% — still short of SPY's 0.862 on every half, and short of the -20.23% drawdown cap by
19.7pp. Small-panel turnover runs 13.7/yr (EWALL) to 24.6/yr (TOP5), so 10 bps costs about
1.4–2.5pp of CAGR a year; removing all of it does not make a single arm defensive.

## Rule 8 walk-forward ((n, g) chosen on 2011–2016, 2017–2026 read once)

Cells are panel x overlay x cost at the PROTOCOL rungs; four selectors fixed in advance (S0 no
screen; S1 all five IS bars; S2 floor deleted; S3 IS-window defensive).

**On SMALL439, S1, S2 and S3 are empty in 8 of 8 cells each — 24 of 24.** Idea 133's "6 of 18
empty cells" is not a sampling accident: on the small panel the screened candidate set is
empty everywhere, at every gross level and both cost rungs. S0 (no screen) is the only
selector that can pick at all there, and its pick delivers OOS **0.7% CAGR / 0.070 Sharpe /
-39.2% MaxDD** against SPY's OOS 15.45% / 0.882 / -33.72%.

For contrast, on U56 the class-aimed selector S3 delivers OOS 10.5% / **1.125** / -13.2%, and
on B136 8.1% / 0.719 / -14.2%. Across all 42 non-empty picks: 17/42 beat SPY's OOS Sharpe,
1/42 clears 4b, 0/42 clears 4a, 1/42 is defensive.

## Verdict

The queue offered two hypotheses and the answer is the first — **the panel** — but the
diagnostic it proposed for reaching that answer does not work. "If it is always H1/H2/OOS
rather than the DD cap" is false: the DD cap fails on 86% of small-panel arms too. The correct
statement is stronger and simpler: the small panel produces no book that clears ANY of the
four non-floor bars against SPY, and none that clears the halves bars even against IWM, at any
gross level, under any of the four defensive overlays, and with costs set to zero. There is
nothing there for a defensive class to contain.

PROTOCOL needs no recalibration for small caps on this evidence. What it should carry instead
is the caveat that the small panel is not a source of 4b candidates at all.

## Caveats

**SURVIVORSHIP, and it runs the conservative way here.** All three panels are
current-constituent lists; the small panel screens on names that are sub-$2B *today* and have
priced continuously since 2010, so every sub-$2B name that delisted, was taken under or went
to zero is absent. That inflates the small panel's CAGR and flatters its drawdowns and halves
Sharpes — so a "no defensive books" finding measured on it is conservative, while a "the bars
are mis-calibrated" finding would not have been. The small panel's window (2011–2026) contains
no 2008–09 bear market, so its drawdown cap is measured on a window that cannot express a deep
one (idea 128). MaxDD is one number off one path. IWM is a diagnostic reference only; SPY
remains the PROTOCOL bar.

Files: `.grid.csv` (1080 rows = 540 arms x 2 windows), `.refs.csv` (12), `.walkforward.csv`
(96), `.console.txt`.

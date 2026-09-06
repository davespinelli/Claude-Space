# idea 276 — is-the-gate-a-drawdown-instrument-on-every-panel (cloud, 2026-09-06)

**Verdict: ANSWERED — the band is NOT the project's cheapest drawdown instrument. It is the
cheapest one on U56 only (6 of 8 cells), it is never cheapest on B136 (0/8) or SMALL439 (0/8),
and it cannot even be priced at the top gross rung. The vol gate is the only instrument that
prices in all 24 cells and it wins the mean rank.**

Script: `2026-09-06_is-the-gate-a-drawdown-instrument-on-every-panel_cloud.py`
Artefacts: `.grid.csv` (168 full + 168 IS arm-cells), `.oos.csv`, `.keep.csv`, `.walkforward.csv`,
`.console.txt`.

## What was run

EWall (equal-weight every priced name) on U56 / B136 / SMALL439, weekly, t+1, at 10 and 25 bps.
Six de-grossing instruments plus the static gross lever as the control. Every arm's base
multiplier `m` is **solved** so its realised mean gross equals a target G ∈ {0.40, 0.50, 0.60,
0.75} on the window being scored, which removes the "safer because it holds less" channel that
idea 94's fixed-base-gross price list left open. Price = pp of CAGR forgone per pp of MaxDD
bought against the control at the *same realised gross*; yield is its reciprocal (the QUEUE's
"drawdown per pp of forgone CAGR"). Two tuned parameters: instrument family and G.
`gross50` is not a competitor here — at matched gross it *is* the control, the G=0.50 rung.

Harness check: with every instrument off, the simulator reproduces `engine.backtest` to
0.0e+00 on the evaluated slice. The U56 control reproduces the published live-book numbers
exactly (v2 8.66% / 1.2056 / −12.05%, IS 1.1043, OOS 1.2851).

## The price list (full sample, 10 bps, lower = cheaper)

| panel | G | band3 | g200 | abs12 | vol60 | v1gate | ddctl8 | cheapest |
|---|---|---|---|---|---|---|---|---|
| U56 | 0.40 | **0.164** | 0.261 | 0.467 | 0.216 | 0.344 | 0.324 | band3 |
| U56 | 0.50 | **0.168** | 0.268 | 0.484 | 0.223 | 0.354 | 0.928 | band3 |
| U56 | 0.60 | **0.172** | 0.276 | 0.501 | 0.229 | 0.364 | 1.583 | band3 |
| U56 | 0.75 | *unmatched* | *unm.* | *unm.* | **0.240** | *unm.* | 0.481 | vol60 |
| B136 | 0.40 | 0.300 | 0.365 | 0.621 | **0.199** | 0.412 | 0.227 | vol60 |
| B136 | 0.50 | 0.310 | 0.377 | 0.645 | **0.206** | 0.426 | 0.496 | vol60 |
| B136 | 0.60 | 0.320 | 0.389 | 0.669 | **0.213** | 0.440 | 0.842 | vol60 |
| B136 | 0.75 | *unm.* | *unm.* | *unm.* | **0.223** | *unm.* | 0.333 | vol60 |
| SMALL439 | 0.40 | 0.328 | 0.348 | 0.285 | 0.486 | 0.645 | **0.192** | ddctl8 |
| SMALL439 | 0.50 | 0.333 | 0.354 | 0.290 | 0.504 | 0.505 | **0.061** | ddctl8 |
| SMALL439 | 0.60 | 0.314 | 0.329 | 0.291 | 0.523 | 0.436 | **0.018** | ddctl8 |
| SMALL439 | 0.75 | *unm.* | *unm.* | *unm.* | 0.554 | *unm.* | 0.208 | vol60/ddctl8 |

25 bps reproduces the same ordering everywhere except SMALL439 G=0.40, where abs12 edges ddctl8.

**Mean rank over all 24 panel × cost × G cells** (NaN where the arm cannot be priced):
vol60 **1.92 (n=24)**, band3 1.94 (n=16), ddctl8 2.94 (n=18), g200 3.38 (n=16), abs12 4.56 (n=16),
v1gate 4.57 (n=14). band3's rank is computed on two thirds of the board because of the next point.

## The reachability finding (idea 154's ceiling, re-met here)

At G=0.75 **no per-name gate can reach the target gross at m=1.0**: band3 tops out at realised
0.7102 on U56, 0.7085 on B136, g200 at 0.7096, v1gate at 0.6920. 40 of 168 full-sample cells are
UNMATCHED and are reported but never priced or picked. This is a substantive result, not
bookkeeping: **a gate is not a free exposure dial** — above a panel-specific ceiling it cannot
express a book at all, whereas the vol gate and the book-level DD control reach every rung.

## Rule 8 (m and arm both chosen on 2009–2016, evaluated untouched on 2017–2026)

- band3 is the IS pick in **2 of 24 cells** and the OOS-cheapest in 6; vol60 is the IS pick in 14.
- IS pick == OOS cheapest in **8 of 24** cells. Mean Spearman(IS price, OOS price) **+0.267**,
  positive in 10 of 13 cells where it is defined — the ordering is weakly, not reliably, stable.
- On SMALL439 the correlation is *negative* in 3 of 6 defined cells (−1.00, −0.90, −0.50): the
  price list does not transport to the small-cap panel at all.
- 8 of 24 cells have no eligible IS arm (nothing bought ≥ 1.0 pp of IS drawdown at that gross),
  and every U56 cell at 25 bps is one of them.

## KEEP paths

- **4a:** 8 of 168 full-sample cells, 7 of them also passing the OOS 4a bars — all on B136 at
  G=0.40/0.50 (band3, vol60, ddctl8). None on the live panel: nothing here beats RULES v2 on
  its own board.
- **4b:** 14 full-sample passes, **13 also passing the OOS 4b bars**, and every single one sits
  at the **top rung G=0.75** — the CAGR floor (70% of SPY's 15.23%) kills all four instruments at
  every lower gross (128 of 144 treated cells fail the CAGR bar). Cross-panel and cross-cost:
  `vol60` and `ddctl8` pass on **U56 and B136 at both 10 and 25 bps**; band3 passes on U56 only.
  `vol60` @0.75 on U56: 12.08% / 1.1333 / −17.56%, halves 1.156/1.113, OOS 12.59% / 1.1858 /
  −17.44%, turnover 1.44×/yr, vs SPY 15.23% / 0.8890 / −33.72% (OOS 15.45% / 0.8820 / −33.72%).
  This re-confirms idea 94's memo candidate on a third harness — see the memo beside this file.

## Predictions, scored

- **P1 holds** — every gate arm's price is positive and finite wherever it is defined; no
  instrument buys drawdown for free at matched gross.
- **P2 holds** — band3 is not uniquely cheapest; the answer to the QUEUE question is
  "merely one of several", and *which* one is a property of the panel.
- **P3 half-wrong** — ddctl8 is indeed cheapest on the panel where the trend family inverts
  (SMALL439, all rungs), but on U56 it is the *dearest* arm at G=0.50–0.60 (0.93–1.58), not close
  to band3. Its price is also the least stable across G of any arm.
- **P4 wrong** — no cell has negative dd_bought. The undefined cells came from the reachability
  ceiling instead, which the prediction did not anticipate.
- **P5 holds** — no arm passes 4b on all three panels; SMALL439 contributes zero 4b passes.

## Caveats

SURVIVORSHIP: all three panels are current-constituent lists; SMALL439 has no delistings, so its
levels are optimistic by an unknown one-directional margin falling hardest on beaten-down names —
exactly the cohort a trend gate exits. Comparisons here share a panel, days, cost and realised
gross, so the deltas are far less exposed than the levels, but no SMALL439 level should be quoted
as an expected return. The G ladder has four rungs; every 4b pass sits on the top one, so those
passes are a statement about gross as much as about the instrument (idea 274's knife-edge result).

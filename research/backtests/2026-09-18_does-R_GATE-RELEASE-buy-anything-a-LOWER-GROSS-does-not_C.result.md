# Idea 1067 (lane C, 2026-09-18) — does R_GATE RELEASE buy anything a LOWER GROSS does not?

**ANSWER: NO. KILL (capital). No new book, no RULES change proposed.**

Two dials, all 20 points reported for both kinds: GROSS {0.75, 0.65, 0.55, 0.45, 0.35} x MIN HOLD
{5, 21, 63, 126}, over 2 panels x 3 mechanisms x 4 rebalance grids = **1,080 book arms** plus a
400-arm gross-matched null. 10 bps, next-day execution, N=20, gross-to-cash (no leverage).
**Gates 8 of 8 PASS**; this script's `minhold_book` is **bit-identical** to 1065's own (max|dW| 0.0
over 8 books), so the release tested here IS 1065's R_GATE release.

## 1. The head to head, at matched drawdown (96 cells, gross solved exactly by bisection)

| H | n | g* median | d_CAGR | SOFT wins | d_Sharpe | d_OOS_Sharpe | d_turnover |
|---|---|---|---|---|---|---|---|
| 5 | 24 | 0.750 | -0.0043 | 0.583 | -0.0096 | -0.0076 | +0.403 |
| 21 | 24 | 0.654 | +0.0074 | 0.792 | -0.0158 | +0.0092 | +2.082 |
| 63 | 24 | 0.596 | +0.0087 | 0.667 | -0.0251 | -0.0114 | +2.660 |
| 126 | 24 | 0.689 | -0.0043 | 0.333 | -0.0276 | -0.0387 | +2.440 |

**POOLED: d_CAGR +0.0019 (median +0.0000, SOFT wins 0.594), d_Sharpe -0.0195 (wins 0.427),
d_OOS_Sharpe -0.0121 (wins 0.490), d_turnover +1.896/yr — SOFT trades MORE at 0.990 of cells.**
Per panel: U56 d_CAGR +0.0038 / d_OOS -0.0006; B136 d_CAGR -0.0001 / d_OOS -0.0236. The rung-wise
match (lowest declared rung clearing SOFT's |MaxDD|) reads the same way: d_Sharpe -0.0096 /
-0.0156 / -0.0248 / -0.0272 at H = 5 / 21 / 63 / 126.

**The turnover rebate 1065 credited the release with does not survive the right comparand.** 1065
scored SOFT against HARD *at the same gross* and found it keeps 69-77% of the rebate. Against HARD
*de-grossed to the same drawdown* — which keeps 100% of its own rebate and gives the drawdown back
for free — SOFT trades **+1.90 turns/yr more** at 95 of 96 cells. The mechanism's one priced
benefit is an artefact of the comparand.

## 2. Why de-grossing is the fair comparand: Sharpe is gross-invariant (H_GROSSINV PASS)

Over 0.75 -> 0.35, **max|Sharpe(g) - Sharpe(0.75)| = 0.0087** across all 216 cells, while CAGR moves
up to 0.0909 and |MaxDD| up to 0.1490 (monotone at 216 of 216 cells, G4). De-grossing is a pure
drawdown-for-CAGR trade at a known price, and **4b's drawdown leg is therefore purchasable by
anyone**: it fails at 0.676 of arms at g=0.75 and 0.000 at g=0.35. What stops the purchase is the
CAGR floor — **4b passes 64 / 74 / 62 / 0 / 0 arms at g = 0.75 / 0.65 / 0.55 / 0.45 / 0.35**, and
L_CAGR is the most-failed leg overall (567 of 1,080, against L_DD 295, L_H2 250, L_OOS 91, L_H1 10).

## 3. Both KEEP paths, the null, and rule 8

**4a: 0 of 1,080.** **4b: 200 of 1,080** — BOOK_H0 20, BOOK_HARD 92, BOOK_SOFT 88; **BOTH: 0.**
SOFT does not out-pass HARD. The **gross-matched null passes 4b at 0.072 overall but at 0.250 at
g=0.65** — the rung where books pass most (0.343) is the rung where a random-key book passes most
too, so a 4b PASS quoted at g=0.65 is worth about a quarter of a coin flip less than it looks.

Rule 8 (arm chosen on IS Sharpe alone per panel x mechanism, OOS read ONCE): **6 of 6 picks beat
SPY on OOS Sharpe, 0 of 6 beat live RULES v2**, and SOFT is picked at only 1 of 6. Head to head
under rule 8 — best SOFT arm against the best HARD arm whose IS |MaxDD| is no worse — **SOFT wins
at 3 of 6, mean d_OOS_Sharpe +0.0101.** A coin flip.

## 4. The do-nothing control, and the sharpest single number in the run

Against the H=0 book (no min hold at all) de-grossed to the same IS drawdown, the best SOFT arm
wins OOS Sharpe at **13 of 22** cells (mean +0.0354, -4.57 turns/yr) — again a coin flip. In the
cell rule 8 actually picked, doing nothing is strictly better:

| U56 / CAND20 / M / g=0.75 | full | halves | OOS | turn |
|---|---|---|---|---|
| BOOK_SOFT H=126 (the pick) | 14.30% / 1.1733 / -18.91% | 1.2565 / 1.1107 | 15.53% / 1.2025 / -18.91% | 3.34 |
| BOOK_HARD H=126 | 14.71% / 1.0830 / -23.08% | 1.2253 / 0.9919 | 15.98% / 1.0793 / -23.08% | 2.14 |
| **BOOK_H0 (no min hold)** | **15.26% / 1.2123 / -19.51%** | 1.2039 / 1.2267 | **17.50% / 1.3059 / -19.51%** | 4.77 |

Benchmarks: SPY U56 full 15.13% / 0.8848 / -33.72%, OOS 15.28% / 0.8745; RULES v2 (live) full
8.62% / 1.2017 / -12.05%, OOS 9.47% / 1.2778.

## 5. Published, not repaired

- **The queue's premise levels are a mis-transcription (G7).** "15.58% -> 14.16%, MaxDD -21.68% at
  H=63" matches **no** committed gross-0.75 arm; 15.58% is U56/CAND20/W HARD at **H=126**, and
  14.16% / -21.68% appear nowhere. The real premise is 1065's (B) table — medians over 24 cells,
  dCAGR **-0.0197** at H=63 — which **G6 reproduces to 4.62e-04** on all four holds.
- **One committed row of 1065 does not reproduce from 1065's own code (G2b).** 8 of 9 committed
  U56/CAND20/W arms replay to <5e-5 on 1065's own tape end; `BOOK_SOFT / H=63` deviates 2.39e-03
  in Sharpe and 1.29e-02/yr in turnover while |MaxDD| agrees to 3.2e-07. Since G2 proves the
  builder is bit-identical, that row is a defect in the committed artefact, not here. It moves no
  verdict in this run — every number above is re-derived from this run's own books.
- **`engine.backtest` returns 2 non-finite days** on U56 (index 0 and 3, inside the 260-day
  warm-up). `nrun` returns none and agrees with the engine to 2.8e-17 on the other 4,705 days (G1).

## 6. Survivorship (rule 9)

U56 and B136 are current-constituent panels; **every LEVEL above is optimistic**. The headline is a
within-cell, matched-drawdown, same-dates contrast of one book against another, which a level bias
common to the cell largely cancels out of. The 4a/4b PASS COUNTS and the rule-8 OOS levels are
levels and carry the full bias.

## 7. What the record should take, in one sentence

**R_GATE release is a more expensive way to buy a drawdown reduction that 15 percentage points of
gross gives away for free — it costs Sharpe (-0.0195), costs OOS Sharpe (-0.0121), trades 1.9 turns
a year more, and its CAGR edge at matched drawdown has a median of exactly zero — so the min-hold
tax should be priced against a de-grossed book, never against the same book at the same gross.**

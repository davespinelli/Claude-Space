# Idea 1270 (lane cloud, 2026-09-18) — is the DD LEG a CONCENTRATION fact once N and GROSS are moved TOGETHER at MATCHED EXPOSURE?

**ANSWERED: NO. AT LEVEL EXPOSURE BREADTH MAKES THE DRAWDOWN *WORSE* ON BOTH LARGE-CAP PANELS
AND COSTS CAGR MONOTONICALLY ON ALL THREE. MaxDD IS AN EXPOSURE OBJECT BY 2.0x-3.5x. CAPITAL
VERDICT: KILL — no new book, nothing enacted (rule 6).**

## What was run
Dial 1 = N in {10,20,30,40,50}. Dial 2 = a target **realised mean exposure** in
{0.55,0.65,0.75,0.85,1.00}, with the gross that attains it **solved per cell** by bisection and
both the solved gross and the realised exposure published — the queue's "proof the line is
level". 150 cells (x 3 panels x 2 slot conventions) plus 30 unmatched flat-0.75 controls.
Frozen: the standing 2026-09-04 book (RAW 3-leg composite, above-200d AND vol20<0.60, H=126,
weekly, 10 bps, t+1, warm-up 260). Gross capped at 1.00 — no leverage (rule 2); the 10
unreachable FIXN cells are published at the cap, not levered into.

## The structural finding that has to come first (pre-declared outcome (A))
**Under the incumbent's own sizing (w = 1/len(held)) the realised exposure does not depend on N
at all.** The solved gross is invariant in N to 1.6e-04 at every exposure rung (G5a), because
the book is always fully at its gross whenever it holds any name. So **the iso-exposure line IS
the plain N ladder at gross 0.75**, and 1081's reading already covered it. The idea's premise —
that N buys diversification "with cash" — is true only under **fixed 1/N slots** (FIXN), where a
thinning screen de-grosses the book. Both conventions are therefore reported at every cell.
How much the matching is worth under FIXN, against the same N at flat 0.75:
U56 -0.05 / -0.19 / -0.38 / -0.79 / **-2.03**pp of MaxDD and +0.04 / +0.17 / +0.28 / +0.51 /
**+1.24**pp of CAGR at N = 10/20/30/40/50; B135 at most -0.23pp / +0.16pp; SMALL663 **nothing at
all**, because n_sel there is either N or 0 at every rebalance (partial-thin share 0.0000 at
every N, against 0.0154..0.6592 on U56), so FIXN and LEN are literally the same book.

## The iso-exposure line at the committed 0.75
| panel / slot | N=10 | N=20 | N=30 | N=40 | N=50 | rank corr(N, MaxDD) | rank corr(N, CAGR) |
|---|---|---|---|---|---|---|---|
| U56 / LEN MaxDD | -20.76% | **-19.12%** | -22.07% | -22.45% | -21.73% | **-0.60** | **-1.00** |
| U56 / LEN CAGR | 17.05% | 15.77% | 14.59% | 13.44% | 12.82% | | |
| B135 / LEN MaxDD | **-20.19%** | -20.73% | -24.34% | -25.37% | -26.46% | **-1.00** | **-1.00** |
| B135 / LEN CAGR | 18.52% | 16.18% | 15.98% | 15.31% | 14.92% | | |
| SMALL663 MaxDD | -43.44% | -35.81% | -36.31% | -36.11% | **-34.90%** | +0.70 | -0.90 |
| SMALL663 CAGR | 8.74% | 7.87% | 7.80% | 7.29% | 7.59% | | |

The committed N=20 is the **drawdown argmax of the whole U56 line**: every broader book at
exactly level exposure is worse on drawdown *and* on return. On B135 the line is monotone
worsening, -6.26pp of MaxDD from N=10 to N=50 for -3.60pp of CAGR. Pre-declared outcome **(C)**
fires on both large-cap panels. Outcome **(B)** fires only on SMALL663 (+8.54pp of MaxDD from
N=10 to N=50, rank corr +0.70) — a panel that fails all five 4b legs at all 50 cells, so its
breadth effect is not a book. Overall the honest reading is **(D)**: panel-specific, and the
panels that could carry capital are (C).

## The surface — exposure vs breadth
Mean MaxDD spread **across N at fixed exposure** vs **across exposure at fixed N**:
U56 3.34 vs 11.65pp (**3.49x**) and 3.82 vs 10.99pp (2.87x); B135 6.28 vs 12.71pp (2.02x) and
5.63 vs 11.82pp (2.10x); SMALL663 8.45 vs 18.64pp (2.20x). **Drawdown on this book is two to
three and a half times more a function of how much is held than of how many names hold it.**

## Capital and rule 8 (the verdict)
- **4a: 0 of 150.** 4b: 35 of 150 (U56 9 LEN + 8 FIXN, B135 8 + 10, SMALL663 0 + 0). The binding
  leg is the DD cap at 14 / 15 / 17 / 15 of the large-cap fails and all five legs on SMALL663 —
  the sixth run in a row to land there.
- **Rule 8**: (N, EXPO) chosen on warm-up..2016-12-31 by IS Sharpe alone, 2017-2026 read once,
  against do-nothing = (N=20, EXPO=0.75) = the committed book. The IS-argmax picks
  **EXPO = 1.00 at 6 of 6 (panel, slot) cells** — full exposure maximises in-sample Sharpe — and
  then **fails 4b's DD cap at 6 of 6**. Deltas: U56 **-0.0688** / -0.0006, B135 **-0.0966** /
  -0.0918, SMALL663 +0.0207 / +0.0207; **mean -0.0361**, beating do-nothing at 2 of 6 and only on
  the panel that fails 4b everywhere. IS/OOS rank corr over the 25 cells -0.55 / +0.08 / -0.25 /
  -0.06 / -0.03 / -0.03. **0 of 6 rule-8 picks clear either KEEP path.** U56/LEN pick (N=50,
  EXPO=1.00): OOS 1.1144 / 17.56% / -28.20% against do-nothing 1.1832 / 17.28% / -19.12%; SPY OOS
  0.8747 / 15.28% / -33.72%; live RULES v2 OOS Sharpe 1.2781.
- The 8 4b conversions on B135/LEN are all at EXPO 0.55-0.75 with N=10-50 — **bought by
  de-grossing, not by breadth** — and B135/FIXN's do-nothing cell already passes 4b, so the
  conversions are a convention artefact, not a mechanism.

## Gates: 27 of 28, and the one failure is the finding
**G2 the line is level**: realised mean exposure equals its target to 9.0e-13 / 4.7e-13 / 1.1e-12
at every reachable cell — the reading rests entirely on this. **G5b FAILS on SMALL663** (the
solved gross does not move with N under FIXN) and **G5c explains it and passes**: FIXN can only
de-gross where 0 < n_sel < N, and that share is 0.0000 at every N on a 663-name pool. The failure
is a property of the panel, not the code, and it is published rather than re-specified away.
**G3** no leverage: solved gross inside (0, 1.00]; the 10 unreachable FIXN cells sit at the cap
with realised exposure 0.904..0.999. **G6** holdings support bit-identical at gross 0.40 vs 0.80
— the exposure dial moves exposure and nothing else. **G7** fast runner == `engine.backtest`
1.74e-17. **G4** determinism 0.000e+00 on the re-solved U56 LEN grid. **G8** SPY held on 0 days of
all three panels. **G1** the anchor replays 15.7814% / 1.1522 / -19.1276% against the committed
15.7147% / 1.1480 / -19.1276%, err 4.16e-03 — published, not toleranced: `data/prices.csv` is
refreshed daily and its adjusted closes are restated retroactively (idea 1203, the same day,
measured that one-day restatement at 2.9e-04 of IS Sharpe and 7.5e-03 of OOS Sharpe).

## Survivorship (rule 9)
U56 and B135 are current-constituent lists; SMALL663 is a current sub-$2B screen (52 of 715
dropped for max_1d_move >= 1.0). Every level is optimistic and every 4b pass is an upper bound.
The headline is a **shape in N at level exposure inside one panel over one tape**, so it is
first-order immune to a level bias that moves all cells together. One direction is not neutral
and is stated: a current-constituent panel has no delistings, so the screen never thins for the
reason it would thin in life, and the wide-N cells (N=40, 50 on a 55-name panel) are flattered
relative to a live panel where the tail names would be gone rather than merely out of favour.
That biases the test **toward** outcome (B), which makes the (C) finding the stronger conclusion.

## What the record should carry forward
The search for the binding 4b drawdown leg inside the book's **breadth** is over: at level
exposure, breadth costs CAGR monotonically on all three panels and buys no drawdown on either
panel that could carry capital. Combined with 1262/1263/1264/1266/1267/1271, every dial that
moves *how much* or *how many* is now priced and every one is reproduced or beaten by a flat
gross cut. What has never been moved is *when* a name stops being eligible — which is exactly
idea 1269, left Open for the next lane.

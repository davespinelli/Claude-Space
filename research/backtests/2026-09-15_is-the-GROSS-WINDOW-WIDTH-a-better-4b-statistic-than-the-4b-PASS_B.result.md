# Idea 677 (lane B, 2026-09-15) — is the GROSS WINDOW WIDTH a better 4b statistic than the 4b PASS?

**VERDICT: KILL for capital. The width is a BETTER RANKER and a WORSE CLASSIFIER, and it is
dominated by both of its own legs.** Nothing promoted; `RULES.md`, `PROTOCOL.md`, `scan.py`,
`bot.py` and `baseline.py` untouched.

Script `2026-09-15_is-the-GROSS-WINDOW-WIDTH-a-better-4b-statistic-than-the-4b-PASS_B.py`;
every point in `.books.csv` (192), `.ladder.csv` (5,760), `.predict.csv` (30),
`.walkforward.csv` (48), `.decompose.csv`, `.grid.csv`, `.null.csv`, `.console.txt`.

## The construction

PROTOCOL 4b's two level legs are two one-sided constraints on a book's GROSS:
`MaxDD(g) ≥ 0.60·MaxDD(SPY)` binds from above (→ `g_max`), `CAGR(g) ≥ 0.70·CAGR(SPY)` binds from
below (→ `g_min`). Width `W = g_max − g_min`. 192 books (3 panels × 4 gate families × 3 modes ×
5 breadth triggers = 180, plus 3 ZEROSIG and 9 RANDGATE controls) were run at a 30-rung gross
ladder 0.05→1.50, **5,760 runs in 22s**, W solved by interpolated crossing on the IS window alone.
Tuned: rung resolution STEP ∈ {0.25, 0.10, 0.05} and chooser size k ∈ {1, 3, 5, 10} — two dials,
all 12 combinations reported for all four choosers.

## Gates (printed before any result number)

| Gate | Result |
|---|---|
| G1 TREND/ROW @0.75 **is** `rules_v2_weights` | max\|dW\| **0.000e+00**, max\|dreturn\| **1.041e-17** PASS |
| G2 the O(T) gross-scaling runner == `engine.backtest` | max\|dreturn\| **6.939e-18**, max\|dturnover\| **1.561e-16** PASS |
| G3 committed triples | SPY U56 **15.1302% / 0.8845 / −33.7173%**; RULES v2 U56 **8.6227% / 1.2013 / −12.0549%** PASS |
| G4 ZEROSIG cash blend | MaxDD(g)/MaxDD(SPY) = 0.278 / 0.536 / 0.777 / 1.000 at g = 0.25/0.50/0.75/1.00 PASS |
| G5 ladder monotonicity | MaxDD(g) non-increasing **192/192**; CAGR(g) non-decreasing **190/192** |
| G6 determinism | **0.000e+00** |

## What the width is

Gate books (n=180): median **W = −0.0523**, `W ≥ 0` for **76/180**, and **21/180** cannot reach the
CAGR floor anywhere on a ladder that runs to 1.50. **Tuned dial 1 is inert**: moving the rung
resolution from 0.25 to 0.05 moves the median width by **0.0002** and the `W ≥ 0` count by **zero**
(76/180 at all three). Controls behave: ZEROSIG (`g × SPY`) has **W < 0 on every panel at every
resolution** (U56/B136 **−0.1196**, SMALL663 **−0.1055**) — H4 PASS, though the level is **half the
−0.25 the queue quotes from idea 670**, so 670's figure is resolution- or panel-specific and should
not be cited as a constant. RANDGATE (coin-flip gate) median **−0.2723**, `W ≥ 0` in **0/9**.

## The deciding test — W vs the binary PASS against the untouched 2017–2026 window

Identical at all three rung resolutions (STEP 0.05 shown; gate books, n=180):

| target | **W** | **PASS_IS_4b** | W better? |
|---|---|---|---|
| OOS Sharpe (Spearman) | **+0.7515** | +0.5196 | YES — **H1 PASS** |
| OOS MaxDD (Spearman) | **+0.2981** | −0.0438 | YES — **H2 PASS** |
| OOS CAGR (Spearman) | +0.5826 | +0.5759 | marginal (+0.0067) |
| AUC → OOS 4b verdict | 0.8212 | **0.8840** | **no — H3 FAIL** |

The Sharpe result is not noise: a 20-draw relabelling null (seed 677) spans **−0.1502 … +0.0961**
and the real +0.7515 is the **100th percentile**.

**But the decomposition kills the statistic.** W's two legs, and the raw quantity it is built out
of, each predict the out-of-sample book *better than their difference does*:

| predictor | OOS Sharpe | OOS MaxDD | OOS CAGR |
|---|---|---|---|
| **W = g_max − g_min** | +0.7515 | +0.2981 | +0.5826 |
| g_max (DD-cap leg) alone | +0.3181 | **+0.8103** | −0.1511 |
| g_min (CAGR-floor leg) alone | −0.1749 | +0.5805 | −0.5057 |
| plain IS MaxDD | +0.1160 | **+0.7942** | −0.3321 |
| plain IS Sharpe | **+0.7126** | +0.0350 | +0.7361 |

The width's drawdown power (**+0.2981**) is a *quarter* of its own `g_max` leg's (**+0.8103**) and
below the plain in-sample MaxDD it is computed from (**+0.7942**); its Sharpe power (+0.7515) is
barely above just ranking on in-sample Sharpe (+0.7126). The subtraction destroys information.

## The capital leg — PROTOCOL 8, chosen on 2009–2016, 2017–2026 read once

Four choosers × 12 (STEP, k) points = 48 blends, every one in `.walkforward.csv`.
`WIDTH` trades each pick at its own window midpoint (which clips to gross **1.00**);
`WIDTH@75` is the **same picks at the live 0.75**, isolating selection from sizing.

| chooser | OOS 4b | OOS 4a | median OOS CAGR / Sharpe / MaxDD | 4b failing leg |
|---|---|---|---|---|
| WIDTH (midpoint gross 1.00) | **3/12** | 0/12 | 10.59% / 1.140 / −14.61% | **CAGR floor ×9** |
| WIDTH@75 (gross-matched) | **0/12** | 0/12 | 7.93% / 1.141 / −11.06% | **CAGR floor ×12** |
| PASS (incumbent) | **12/12** | 0/12 | 11.93% / 1.100 / −19.14% | — |
| ISSHARPE (reference) | **12/12** | 0/12 | 11.78% / 1.115 / −18.57% | — |

SPY OOS **15.33% / 0.877 / −33.72%**; RULES v2 OOS **1.106**. The width chooser beats the pass
chooser on OOS Sharpe **12/12** and OOS MaxDD **12/12** — gross-matched too — and loses OOS CAGR
**12/12** gross-matched (3/12 unmatched). That is the whole story: **the width selects books that
are safer and lower-returning, and 4b's CAGR floor is exactly the leg it then fails.** Its only
three 4b passes are the k=1 cells, i.e. the single highest-width book of 180
(`B136|TREND|AGG|0.60`, OOS **12.39% / 1.163 / −17.37%**), and the pass chooser's own k=1 book gets
4b as well. Cost-invariant: at 0/10/25 bps the STEP 0.05, k=5 cells move ≤0.08 of Sharpe.

**4a is 0/48 here and 0/180 at the book level**, consistent with the record.

## Answer to the queue

**NO.** The gross window width is *not* a better 4b statistic than the 4b pass. It ranks OOS
Sharpe and OOS MaxDD better (H1, H2 PASS, versus a null it clears at the 100th percentile), but it
**classifies the out-of-sample 4b verdict worse** (AUC 0.821 vs 0.884, H3 FAIL) and, used as a
chooser, it fails 4b **12/12 gross-matched** on the CAGR floor where the incumbent passes 12/12.
H5's 12/12 "win" is a Sharpe-and-drawdown win bought with return, not a 4b win.

The reportable residue is the *leg*, not the width: **`g_max` alone carries OOS drawdown at
Spearman +0.8103** where the binary pass carries −0.0438. Under rule 6 (proposed, NOT applied): a
4b claim could publish `g_max` — the largest gross at which the book still clears the DD cap —
beside its binary pass, since that is the one number here with out-of-sample content the pass does
not have. Nothing in this run justifies replacing the pass, and no RULES change is proposed.

**Caveats.** All three panels are current-constituent lists (PROTOCOL 9); levels are optimistic.
SMALL663's IS window starts 2011-01 (warm-up), so blends containing a small-cap book are scored on
the intersection of trading days, reported per row in `.walkforward.csv`. Only 2020 and 2022 are
real stress tests in the OOS window.

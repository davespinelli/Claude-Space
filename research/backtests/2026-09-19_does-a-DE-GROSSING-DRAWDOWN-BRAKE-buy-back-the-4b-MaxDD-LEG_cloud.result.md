# Idea 1296 (lane cloud, 2026-09-19) — does a DE-GROSSING DRAWDOWN BRAKE buy back the 4b MaxDD LEG?

**VERDICT: KILL (capital), NO NEW BOOK — and the idea's own PREMISE does not hold at the
incumbent cell.**

## 1. The premise fails before the dials do

Idea 1215's "the DD cap is the modal binder" was measured over a population of *failing* cells.
At the frozen 2026-09-04 incumbent the DD leg is not the binder and there is nothing to buy back:

| panel | anchor MaxDD | 4b DD cap (0.60 x SPY) | DD margin | CAGR margin | DD leg |
|---|---|---|---|---|---|
| U56   | -16.38% | -20.23% | **+3.85 pp** | +3.08 pp | PASS |
| B136  | -15.97% | -20.23% | **+4.26 pp** | +2.85 pp | PASS |
| SMALL | -32.63% | -20.23% | -12.40 pp | -2.27 pp | FAIL |

Across all 45 cells the binding legs rank **CAGR 22 fails > H2 21 > H1 16 > DD 14**. On the two
panels this family has ever cleared 4b on, the brake can only be asked *not to break* a leg that
already passes. On SMALL, the one panel where the DD leg does fail, exactly **one** of the ten
braked cells recovers it (OWN200 d0.00) and it does so by holding cash forever: CAGR margin
-9.81 pp, 4b still FAIL.

## 2. What the brake does buy (full sample, 10 bps, t+1)

SPY200 is monotone and well-behaved on both large-cap panels: shallower drawdown at every depth,
paid for in CAGR, with a shallow Sharpe optimum around d0.50-0.75.

| panel | cell | CAGR | Sharpe | MaxDD | H1/H2 | OOS Sharpe | turn |
|---|---|---|---|---|---|---|---|
| U56 | NONE (anchor) | 13.67% | 1.1717 | -16.38% | 1.253/1.122 | 1.1965 | 2.46 |
| U56 | SPY200 d0.50 | 12.03% | **1.1869** | -14.54% | 1.242/1.151 | **1.2393** | 3.02 |
| U56 | SPY200 d0.75 | 12.86% | **1.1902** | -15.44% | 1.258/1.147 | 1.2286 | 2.71 |
| B136 | NONE (anchor) | 13.43% | 1.0630 | -15.97% | 1.232/0.941 | 1.0387 | 2.65 |
| B136 | SPY200 d0.75 | 12.73% | **1.0796** | -14.97% | 1.275/0.938 | 1.0449 | 2.90 |

Four cells beat their panel's anchor on full-sample Sharpe *and* clear 4b full + OOS. All four
are SPY200 at d0.50/0.75; none is on SMALL; **4a is 0 of 45** (the live RULES v2 book's -12.05%
MaxDD is unreachable for any 0.60-gross equity book).

## 3. Rule 8 kills it: the gain is not choosable

(BASIS, DEPTH) chosen on warm-up..2016-12-31 by argmax IS Sharpe, 2017-2026 read ONCE.

| panel | IS pick | IS Sharpe (anchor) | OOS Sharpe pick / anchor | d OOS Sharpe | ex-post best OOS |
|---|---|---|---|---|---|
| U56   | **NONE** d0.00 | 1.1482 (1.1482) | 1.1965 / 1.1965 | +0.0000 | SPY200 d0.50 (1.2393) |
| B136  | SPY200 d0.50 | 1.1570 (1.1072) | 1.0327 / 1.0387 | **-0.0060** | SPY200 d0.75 (1.0449) |
| SMALL | SPY200 d0.00 | 0.8218 (0.7118) | 0.3460 / 0.4728 | **-0.1267** | NONE (0.4728) |

Mean d OOS Sharpe **-0.0442**; the chooser beats doing nothing **0 of 3**; the ex-post best cell
differs from the IS pick **3 of 3**. On U56 — the only panel with a live 4b pass — the in-sample
chooser *declines the brake outright* (NONE is the IS argmax at 1.1482 against SPY200 d0.75's
1.1457), and the +0.0428 of OOS Sharpe sitting in SPY200 d0.50 is visible only with hindsight.
PROTOCOL rule 8 says an in-sample-only winner is PARK; this is weaker than that — it does not win
in sample at all.

## 4. A mechanical defect worth recording

The self-referential basis has an **absorbing state**: at OWN200 d0.00 the book goes fully to
cash, its equity is then flat, a flat curve is never *above* its own 200d mean, so the brake never
releases — 100.0% engaged on all three panels, zero return, Sharpe undefined. Any future
book-equity brake must define its release condition on something other than the braked curve.
Relatedly, the engaged share is a constant across depth for the exogenous basis (SPY200: 17.4% /
17.4% / 15.5%) and path-dependent for the self-referential one (OWN200 U56: 100.0 / 39.4 / 20.9 /
13.8 / 11.2% at d0.00..1.00).

## 5. Gates and provenance

10/10 asserted gates pass, plus 9 published stamps. G0 sample >= 10y on all three panels. G2
BASIS=NONE is one book at all five depths (max deviation 0.0). G3 DEPTH=1.00 reproduces the
unbraked book under every basis (0.0). G4 DEPTH=0.00 moves the book on all three panels.
**The U56 (N=15, W) anchor replays idea 1335's committed `.grid.csv` row to float64 noise:
CAGR dev +5.6e-17, Sharpe +2.2e-16, MaxDD -2.8e-17, H1/H2 exactly 0, turnover -4.4e-16** — same
machinery, same tape.

SURVIVORSHIP (rule 9): U56 / B136 / SMALL are current-constituent lists; SMALL is a sub-$2B screen
carried back to 2010 (`data/small_meta.csv` drops the `max_1d_move >= 1.0` names), so its LEVELS
are an upper bound and only its CONTRASTS across basis and depth are read here.

Deterministic, offline, 16s.

# Idea 2246 — does the both-paths cell's 8.18x/yr turnover decompose into an equity leg and a sleeve leg?

**2026-09-22, lane cloud, run 11.  Script:** `2026-09-22_both-paths-turnover-leg-decomposition_cloud.py`
**Verdict: ANSWERED — YES, and the split is lopsided.  No new KEEP candidate; the incumbent's own
4a+4b pass at <= 10 bps is reproduced and unchanged.**

## What was measured
The record's only 4a+4b book (`u56 / S3-50 + band3-rw`, weekly, t+1, gross 0.75) was re-run with the
drifted portfolio carried **per leg**, so every traded unit is attributable.  Nothing is tuned
(tuned-parameter count = 0); cost rung and panel are reported axes.  Gates: G1 the leg construction
reproduces `i133.book_weights` to 1.1e-16; G2 the per-leg simulator reproduces `engine.backtest`
returns and turnover to 7e-18 / 6e-16; G3 the (u56, 10 bps) cell reproduces the Sunday review's
idea-142 re-run to < 4e-4 on every statistic; G4 the attribution is additive to 1.8e-15; G5 all
32 cells published.

## The answer
| panel | total | equity leg | sleeve leg | share eq | share sl | rescale re-coupling | live v2 book |
|---|---|---|---|---|---|---|---|
| u56   | 8.18x/yr | **6.36x** | 1.82x | **77.8%** | 22.2% | +1.27x (**15.6%**) | 1.77x/yr (4.61x) |
| broad | 10.88x/yr | **9.08x** | 1.79x | **83.5%** | 16.5% | +1.90x (**17.4%**) | 2.01x/yr (5.41x) |

Standalone at full gross 0.75 the equity leg runs 9.45x (u56) / 13.43x (broad) and the sleeve 4.44x
on both; the blend's netting between the two on the columns they share (TLT/GLD/UUP are selectable
by the ranker on both panels) saves only **0.11x / 0.04x per year**, i.e. the legs are almost
perfectly non-overlapping traders.

## Why this closes the device search on the sleeve
The sleeve leg's contribution is **1.82x / 1.79x per year — essentially identical on both panels and
essentially the size of the whole live book**.  Even a **free** sleeve (zero turnover, same returns)
leaves 6.36x on u56 and 9.08x on broad, still **3.6x and 4.5x the live book**.  Conversely a free
ranking leaves 1.82x, i.e. at the live book's own level.  The 8.18x is the **top-20 composite rank
churn**, not the weekly risk-parity re-solve, and not the blend.  This is the mechanism behind the
floors that KILLED 2254 (hysteresis, floor 4.67x) and 2250 (slow refresh, floor ~5x): both devices
were aimed at the right leg and still could not clear it, because the leg they must shrink carries
78–84% of the trading and is the same leg that carries the return.

The rescale re-coupling is real but second-order (+15.6% / +17.4%) and **is not free to remove**: the
DECOUPLED twin (each leg pinned at its own fixed gross 0.375) trades 6.90x / 8.98x instead of
8.18x / 10.88x and **loses both KEEP paths at every cost rung** (u56 @10 bps 8.74% / 1.1278 / -12.72%
against the incumbent's 11.27% / 1.2634 / -11.63%).  Turnover bought with 2.5 pp of CAGR is not a
saving.

## KEEP paths and rule 8 (2017-2026 read once)
4 of 32 cells clear **both** paths, all four the INCUMBENT at 5 and 10 bps:
u56 @10 bps **11.27% / 1.2634 / -11.63%**, halves 1.2822/1.2476, OOS **1.2885** (live v2 OOS 1.2767,
SPY OOS 0.8751); broad @10 bps 11.47% / 1.1333 / -11.82%, halves 1.3115/0.9746, OOS 1.0413 (live v2
OOS 1.1017).  The IS-only chooser (argmax IS Sharpe on 2009-2016 over the four comparands) picks
INCUMBENT at **8 of 8** panel x cost cells; its OOS clears both paths at 5 and 10 bps and **0 of 4**
at 25 and 50 bps.  EQONLY, SLONLY and DECOUPLED clear neither path at any rung on any panel.

## Caveats
Survivorship (PROTOCOL rule 9 / idea 54): u56 and broad are current constituents, so every CAGR level
is optimistic and both 4b bars are easier than on a point-in-time panel.  The turnover **shares** are
same-tape / same-names contrasts and are first-order immune; the pass counts are not.  Flat costs, no
spread/impact/borrow.  One cadence (W), one delay (t+1), one blend (0.50), one band (3%), one gross
(0.75).  This is an accounting of the incumbent's own trading — it lowers no turnover by itself and
proposes no rules change.

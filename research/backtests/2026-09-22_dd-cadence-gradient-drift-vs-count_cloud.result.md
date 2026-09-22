# Idea 983 — is the 4b DD leg's CADENCE GRADIENT a DRIFT fact or a REBALANCE-COUNT fact?

**Lane cloud, run 22, 2026-09-22.  Script:** `research/backtests/2026-09-22_dd-cadence-gradient-drift-vs-count_cloud.py`
**VERDICT: ANSWERED = REBALANCE COUNT.  Removing exposure drift ENTIRELY leaves 102.5% of the
gradient standing — the gradient is very slightly WIDER without drift.  KILL of the drift
reading, and with it of any device that hopes to buy 4b DD margin at a slow cadence by
controlling gross.  No KEEP candidate, no RULES change.  15 gates, 0 FAIL.**

## The premise, reproduced on this run's own tape
Idea 981's `L4_DD` fail rate over 2,700 matched-gross phase-books (3 panels x 5 books x 2 gross x
D/W/M/Q with 1/5/21/63 phases), 10 bps: **D 0.6333 / W 0.6467 / M 0.8317 / Q 0.9270**, range 0.2937.
This run's DRIFT arm: **0.6333 / 0.6467 / 0.8365 / 0.9280**, range 0.2947.  D and W reproduce to
**0.0e+00**; M and Q move by 0.0048 because the committed caches have grown five trading days
since 2026-09-15 (981 read U56 to 2026-09-14 and SMALL to 2026-09-11 with 664 names; this run
reads all three panels to 2026-09-18 with 665 SMALL names), which flips 3 of 630 books at M and
2 of 1,890 at Q.  **Every control below is differenced against THIS run's own DRIFT arm**, so the
tape growth cancels exactly.

## The controls (DIAL 1), and that they bite
| control | what it removes | max \|realised gross − target\| | turnover vs DRIFT (W/M/Q) |
|---|---|---|---|
| DRIFT (inert; the live engine's convention) | nothing | **0.1345** | — |
| NODRIFT_G (the idea's literal control: reset to target GROSS daily) | exposure drift | **4.4e-16** | higher at 82 of 90, median 1.023x |
| NODRIFT_W (strict: reset to the full target WEIGHT VECTOR daily) | exposure **and** concentration drift | **0.0e+00** | higher at **90 of 90** |

At cadence D all three are **bit-identical** (a daily book has no drift to remove) — gate G9b,
max turnover difference 0.0e+00.  That is the construction working exactly as intended.

## THE ANSWER — `L4_DD` fail rate by cadence, every control, every rung
| rung | control | D | W | M | Q | **range Q−D** | share of DRIFT's range surviving |
|---|---|---|---|---|---|---|---|
| **0 bps** (the mechanism rung: 981's premise lives here) | DRIFT | 0.5667 | 0.6467 | 0.8302 | 0.9270 | **+0.3603** | — |
| | NODRIFT_G | 0.5667 | 0.6467 | 0.8429 | 0.9360 | **+0.3693** | **102.5%** |
| | NODRIFT_W | 0.5667 | 0.6400 | 0.8429 | 0.9360 | **+0.3693** | **102.5%** |
| **10 bps** (the capital rung) | DRIFT | 0.6333 | 0.6467 | 0.8365 | 0.9280 | +0.2947 | — |
| | NODRIFT_G | 0.6333 | 0.6467 | 0.8444 | 0.9376 | +0.3042 | 103.2% |
| | NODRIFT_W | 0.6333 | 0.6467 | 0.8460 | 0.9376 | +0.3042 | 103.2% |
| 25 bps | DRIFT / NODRIFT_G / NODRIFT_W | | | | | +0.2291 / +0.2392 / +0.2397 | 104.4% / 104.6% |
| 50 bps | DRIFT / NODRIFT_G / NODRIFT_W | | | | | +0.1307 / +0.1423 / +0.1466 | 108.9% / 112.1% |

Pre-registered bars: H_DRIFT (< 50% survives) **FALSE**; H_COUNT (>= 80% survives) **TRUE**, at
every one of the four rungs and under both controls.  The answer is not marginal — killing drift
makes the gradient **slightly wider**, never narrower.

## Why, measured directly: there was never enough drift to explain it
Median \|realised gross − target gross\| under DRIFT: **D 0.00000, W 0.00138, M 0.00370, Q 0.00693**.
A quarterly book's exposure wanders by seven tenths of one percent of NAV.  Median realised gross
runs 0.7486 / 0.7488 / 0.7500 / 0.7521 across D/W/M/Q.  A 0.36 swing in the DD fail rate cannot be
bought with 0.7 pp of exposure; the staleness of the HOLDINGS is what it is made of.

## Unanimous across panels (headline rung), and across DIAL 2
| panel | DRIFT D→Q range | NODRIFT_G | NODRIFT_W |
|---|---|---|---|
| U56 | +0.5587 | +0.5841 | +0.5825 |
| B136 | +0.3571 | +0.3571 | +0.3556 |
| SMALL | +0.1651 | +0.1667 | +0.1698 |

DIAL 2 (cadence ladder): CORE4 span +0.3603 → +0.3693 / +0.3693; COARSE3 +0.2803 → +0.2893 /
+0.2960; FINE2 +0.0800 → +0.0800 / +0.0733.  3 of 3 panels and 2 of 3 ladders leave the gradient
intact or wider; only FINE2 (D vs W, where the control is inert at D by construction and the whole
span is 0.08) moves the other way, by 0.007.

## Both KEEP paths at the capital rung (10 bps) — the controls are DIAGNOSTICS, not proposals
| control | 4b pass | 4a pass | median turnover | median CAGR |
|---|---|---|---|---|
| DRIFT | 141 of 2,700 (0.0522) | 5 of 2,700 | 4.23 /yr | 12.65% |
| NODRIFT_G | 128 of 2,700 (0.0474) | **0 of 2,700** | 4.50 /yr | 12.66% |
| NODRIFT_W | 130 of 2,700 (0.0481) | **0 of 2,700** | 6.65 /yr | 12.75% |

A daily reset costs more than it buys at every real cost rung: both controls LOWER the 4b pass
rate and take 4a to zero.  **No 4b pass under either control is a capital candidate** and none is
recorded as one — which is exactly what was pre-registered.

## Rule 8 — (CONTROL, LADDER) chosen on warm-up..2016-12-31 ONLY, 2017-2026 read ONCE
| panel | chooser | pick | OOS median CAGR | OOS median Sharpe | OOS median MaxDD |
|---|---|---|---|---|---|
| U56 | C_ISDD / C_ISSHARPE | (DRIFT, COARSE3) | 16.80% | 1.0759 | -24.99% |
| U56 | **C_LIVE (zero-parameter)** | (DRIFT, CORE4) | 16.76% | 1.0755 | -24.89% |
| U56 | SPY / RULES v2 | — | 15.29% / 9.46% | 0.8753 / 1.2770 | -33.72% / -12.05% |
| B136 | C_ISDD | (NODRIFT_G, COARSE3) | 16.08% | 0.9310 | -28.10% |
| B136 | C_ISSHARPE | (NODRIFT_W, COARSE3) | 16.09% | 0.9288 | -28.03% |
| B136 | **C_LIVE (zero-parameter)** | (DRIFT, CORE4) | 15.81% | **0.9346** | -27.90% |
| B136 | SPY / RULES v2 | — | 15.26% / 7.85% | 0.8739 / 1.1019 | -33.72% / -12.24% |
| SMALL | C_ISDD | (NODRIFT_W, COARSE3) | 5.92% | 0.4576 | -43.05% |
| SMALL | C_ISSHARPE | (NODRIFT_G, COARSE3) | 5.91% | 0.4500 | -42.75% |
| SMALL | **C_LIVE (zero-parameter)** | (DRIFT, CORE4) | 5.81% | 0.4554 | -42.54% |
| SMALL | SPY / RULES v2 | — | 15.29% / 3.64% | 0.8753 / 0.5459 | -33.72% / -14.16% |

No legal IS-only chooser on this dial pair is worth anything out of sample: the fitted picks beat
the ZERO-PARAMETER shipped convention by at most **+0.0004 of OOS Sharpe** (U56), and on B136 the
zero-parameter rung is outright **best**.  The record's standing pattern holds again.

## What this changes
1. **The DD cap's cadence gradient is intrinsic to trading slowly.**  It is made of stale
   HOLDINGS, not of wandering exposure, so no gross-control, vol-target, de-gross or band device
   can reach it at a slow cadence.  The 2026-09-22 CHANGELOG's run of de-grossing and exposure
   devices that "fail the CAGR floor while the DD leg never binds" now has a reason: at M/Q the
   DD leg is already lost to re-selection frequency before any exposure dial is turned.
2. **The only lever that moves it is rebalance count** — i.e. cadence itself, or a selection rule
   that refreshes holdings without paying full turnover (min-hold, hysteresis, tranching).  That
   is where the record's drawdown research should go.
3. **A reporting clause worth adopting:** any committed DD or cadence claim should carry its
   realised \|gross − target\| path, because this run shows the record has been implicitly
   attributing to drift a quantity that never exceeds 0.7 pp of NAV at its slowest.

**SURVIVORSHIP (rule 9):** B136 and SMALL are CURRENT constituents, so their levels are biased up;
the 54 SMALL tickers with `max_1d_move >= 1.0` were dropped before anything was computed (665
names remain).  Every statement here is a WITHIN-cell contrast across controls on the identical
name set and the identical target weight matrix (gate G5, max spread 0.0e+00), which is what makes
the answer robust to that bias.

**GATES: 15 recorded, 0 FAIL** — G0 offset_mask(.,0) == engine.rebalance_mask; G1 the DRIFT runner
== `engine.backtest` to 6.9e-18; G2 BAND03@0.75 == `baseline.rules_v2_weights` to 0.0e+00; G3
cross-run vs 981 with the tape-growth cause named and quantified; G4 sample; G5 matched gross
across the ladder AND the controls (0.0e+00); G6 the control bites; G7 choosers read no OOS row;
G8 neither control creates gross the target lacks (4.3e-15); G9/G9b/G9c the controls differ where
they should and are identical where they must be; G10 determinism; G11 all 32,400 cells published;
G12 exactly two tuned parameters.  RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py NOT
modified.

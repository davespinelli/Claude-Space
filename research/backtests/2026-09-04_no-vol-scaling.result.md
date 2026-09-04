# Idea 1 — no-vol-scaling — result (2026-09-04, lane A)

**Verdict: KILL as a replacement for RULES v1 (fails 4a and 4b at every one of the 12 grid
points) — but the treatment itself is decisively confirmed: the `/sqrt(vol20)` term costs the
live book ~10pp/yr. Nearest miss: OFF n=8, 75% gross (PARK).**

A second, larger finding came out of the run: `data/prices.csv` is on a CALENDAR-day index,
which distorts every backtest run in the no-internet sandbox AND the live daily scanner.
See "Data bug" below and CHANGELOG. All numbers in this file are on a corrected trading-day
index; the raw-cache numbers are in the console log for contrast.

## Setup
Grid: vol_scale ON (=v1) / OFF, crossed with n ∈ {3,5,8} and gross ∈ {75%,100%} — the two
tuned parameters PROTOCOL rule 4 allows. All 12 points reported. Weekly, 10 bps, next-day
execution. Eligibility (200d MA, vol20<0.60), lookbacks and rebalance are v1's own, untouched.
Sanity: ON n=5 / 75% reproduces the live baseline to 0.00e+00 daily error (Sharpe 0.6665).

## Full grid (trading-day index; sample 2009-01-13 → 2026-09-03)
| variant | CAGR | Vol | Sharpe | MaxDD | H1 / H2 | IS Sharpe | OOS CAGR | OOS Sharpe | OOS MaxDD | vol20 held | turnover | 4a | 4b |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ON  n=3 75% | 6.4% | 10.6% | 0.63 | -13.6% | 0.66 / 0.61 | 0.60 | 7.0% | 0.66 | -13.2% | 13.0% | 27.9x | no | no |
| ON  n=3 100% | 8.3% | 14.2% | 0.63 | -17.9% | 0.66 / 0.61 | 0.60 | 9.1% | 0.66 | -17.5% | 13.0% | 37.2x | no | no |
| ON  n=5 75% (=v1) | 6.5% | 10.2% | 0.67 | -13.8% | 0.64 / 0.69 | 0.55 | 7.8% | 0.75 | -13.8% | 14.1% | 23.6x | no | no |
| ON  n=5 100% | 8.5% | 13.6% | 0.67 | -18.2% | 0.64 / 0.69 | 0.55 | 10.2% | 0.75 | -18.2% | 14.1% | 31.5x | no | no |
| ON  n=8 75% | 8.0% | 10.1% | 0.82 | -16.4% | 0.87 / 0.77 | 0.81 | 8.4% | 0.82 | -16.4% | 15.5% | 18.7x | no | no |
| ON  n=8 100% | 10.6% | 13.5% | 0.81 | -21.5% | 0.88 / 0.76 | 0.81 | 11.1% | 0.82 | -21.5% | 15.5% | 24.9x | no | no |
| OFF n=3 75% | 21.9% | 21.3% | 1.04 | -25.8% | 1.01 / 1.06 | 1.02 | 23.9% | 1.06 | -25.8% | 31.8% | 20.8x | no | no |
| OFF n=3 100% | 29.0% | 28.4% | 1.04 | -33.1% | 1.02 / 1.07 | 1.02 | 31.7% | 1.06 | -33.1% | 31.8% | 27.6x | no | no |
| OFF n=5 75% | 16.5% | 17.8% | 0.95 | -21.6% | 0.90 / 1.00 | 0.90 | 18.5% | 1.00 | -21.6% | 29.4% | 17.6x | no | no |
| OFF n=5 100% | 21.9% | 23.7% | 0.95 | -28.0% | 0.90 / 1.01 | 0.90 | 24.5% | 1.00 | -28.0% | 29.4% | 23.5x | no | no |
| **OFF n=8 75%** | **13.8%** | 15.1% | **0.93** | **-17.9%** | **0.92 / 0.95** | 0.87 | **15.4%** | **0.98** | -16.6% | 27.0% | 15.0x | no | **no (H1 only)** |
| OFF n=8 100% | 18.3% | 20.2% | 0.93 | -23.4% | 0.92 / 0.95 | 0.88 | 20.5% | 0.98 | -21.7% | 27.0% | 19.9x | no | no |
| RULES v1 baseline | 6.5% | 10.2% | 0.67 | -13.8% | 0.64 / 0.69 | 0.55 | 7.8% | 0.75 | -13.8% | — | — | — | — |
| SPY | 15.3% | 17.7% | 0.89 | -33.7% | 0.96 / 0.84 | 0.90 | 15.5% | 0.88 | -33.7% | — | — | — | — |

## The treatment effect is large and significant
At v1's own configuration (n=5, 75%): OFF − ON = **+10.09%/yr, t = 3.33**, corr(ON,OFF) 0.711.
OFF beats ON on Sharpe at every single (n, gross) pair. Mechanism, exactly as idea 25
predicted: the scaler drops the average vol20 of held names from 29.4% to 14.1% and leaves
only 31% name overlap between the two books — it is not a risk adjustment on a momentum book,
it is a different (low-vol) book.

## Walk-forward (PROTOCOL rule 8) — chosen on 2009-2016, evaluated on 2017-2026
Pre-stated rule (fixed before any OOS number was looked at): highest in-sample Sharpe within
each arm, ties to smaller n then smaller gross.
- ON arm picks n=8 / 100% → OOS CAGR 11.1%, Sharpe 0.82, MaxDD -21.5%
- OFF arm picks n=3 / 100% → OOS CAGR 31.7%, Sharpe 1.06, MaxDD -33.1%
- RULES v1 OOS 7.8% / 0.75 / -13.8% · SPY OOS 15.5% / 0.88 / -33.7%

The OFF pick beats baseline and SPY on OOS Sharpe and CAGR, and **still fails both KEEP paths**:
- 4a: H1 1.02 > 0.64 pass, H2 1.07 > 0.69 pass, MaxDD -33.1% vs -13.8% **FAIL**
- 4b: H1 1.02 > SPY 0.96 pass, H2 1.07 > 0.84 pass, OOS 1.06 > 0.88 pass, CAGR 29.0% > 10.7%
  pass, MaxDD -33.1% vs the -20.2% cap **FAIL**

A second, drawdown-aware selection rule (highest IS Sharpe subject to IS MaxDD ≤ 60% of SPY's
IS MaxDD — added *after* seeing the grid, so reported as secondary, not as the result) selects
nothing at all in the OFF arm: every no-scaler point breaches the in-sample cap (best is
n=8/75% at -17.9% vs the -13.2% cap). So no ex-ante rule reaches a 4b-passing configuration.

## Nearest miss (PARK): OFF n=8, 75% gross
13.8% CAGR / 0.93 Sharpe / **-17.9% MaxDD** (vs SPY -33.7%), halves 0.92 / 0.95, OOS 15.4% /
0.98 / -16.6%, turnover 15.0x/yr. It clears three of 4b's four tests — MaxDD -17.9% ≤ -20.2%
cap, CAGR 13.8% ≥ 10.7% floor, OOS Sharpe 0.98 > 0.88 — and **fails only on H1 Sharpe, 0.918 vs
SPY's 0.957**, a gap of 0.04. It is not selectable by the pre-stated rule (it has the *lowest*
IS Sharpe in the OFF arm), so it is a PARK, not a KEEP. Doubling n from 3 to 8 costs 8.1pp of
CAGR and buys 7.9pp of drawdown — the honest trade the OFF arm offers.

## Cost sensitivity (turnover is 15-28x/yr, so this is not optional)
- OFF n=3 100%: 5bps 1.09/23.2% · 10bps 1.04/21.9% · 25bps 0.89/18.1% · 50bps 0.65/12.2%
- OFF n=8 75%: 5bps 0.98/14.7% · 10bps 0.93/13.8% · 25bps 0.78/11.3% · 50bps 0.54/7.2%

The edge survives 25 bps but not 50. At 25 bps OFF n=8 still beats v1's 10 bps Sharpe.

## Data bug found during this run (the more important finding)
`data/prices.csv` is indexed on **calendar days** from 2014-09-17 — the day BTC-USD's history
starts. yfinance returns a 7-day index when crypto is in the ticker list, and `cache_prices.py`
`.ffill()`s every equity across weekends. `load_universe()` drops the crypto *columns* but keeps
those *rows*, so from Sep-2014 on ~30% of daily returns in the cache are exactly zero and each
year has 365 rows instead of 252. Consequences:

1. **Metrics.** `engine.metrics()` annualizes with `len(r)/252` and `sqrt(252)`. On raw cache
   v1 reads 4.65% / 0.555 / halves 0.659–0.452; on a trading-day index it reads 6.48% / 0.666 /
   0.641–0.692 — which reproduces the Sep-3 leaderboard row exactly, confirming the Sep-3 rows
   were run locally on live yfinance data and are sound. Only sandbox/Actions runs are affected.
   The distortion is concentrated in the second half of the sample, so it corrupts the H1/H2
   robustness test PROTOCOL rule 4 depends on.
2. **It flips verdicts.** SPY reads 11.5% CAGR / 0.78 Sharpe on the raw cache vs 15.3% / 0.89
   corrected, so KEEP path 4b's "Sharpe > SPY" and "CAGR ≥ 70% of SPY" are materially easier.
   Concretely: on the raw cache OFF n=8/75% **passes 4b**; on corrected data it fails. A cloud
   lane taking the cache at face value would have promoted a false KEEP today.
3. **Live signals, not just research.** `research/scan.py` downloads the universe *including*
   BTC-USD/ETH-USD and ffills, so the daily scan runs on the same 7-day index: its
   `rolling(200)` mean spans ~143 trading days, not 200, and `rolling(20)` vol spans ~14.
   Measured 2015+: the 200d-MA flag differs from the true one on **7.6% of ticker-days**, at
   least one name is flipped on **95.8% of days** (mean 4.2 of 56 names), full eligibility
   differs on 8.1% of ticker-days, and vol20 reads a median **0.84x** of its true value — so
   the vol<0.60 gate is loose and the `1/sqrt(vol20)` scaler is mis-scaled. The paper book
   started trading today on these signals.

Fix (for the Sunday review; PROTOCOL forbids this script from touching baseline.py / scan.py):
drop crypto from the download or reindex to NYSE trading days in `cache_prices.py` and
`load_universe()`, and re-derive `scan.py`'s index the same way. Everything in this file after
the "raw cache" section already uses the corrected index.

## Caveats
`universe.json` is current constituents — survivorship bias flatters every momentum arm here,
and the OFF arm (which holds 27-32% vol names) more than the ON arm. 2020 and 2022 are the only
real stress tests. Turnover of 15-28x/yr is high enough that fill quality, not the 10 bps
assumption, would decide the live outcome.

# Idea 31 — PEAD with the announcement-day return as the surprise proxy — result (2026-09-04)

**Verdict: KILL (all 4 grid points, both KEEP paths). The strategy makes 17–19%/yr, but the
PEAD sort contributes none of it — a control that goes long the *worst*-reacting announcers
earns MORE (20.7% CAGR / 1.16 Sharpe) than the top tercile. What is being measured is an
equal-weight, survivorship-biased large-cap book, not drift.**

Script: `research/backtests/2026-09-04_small-cap-pead.py` ·
console: `research/backtests/2026-09-04_small-cap-pead.console.txt` ·
event cache: `data/earnings_dates.csv` (built by `research/fetch_earnings_dates.py`)

## Naming correction, stated up front
The brief calls this **small-cap** PEAD. `research/universe_broad.json` is 136 **large-cap**
US names plus ~30 ETFs — there is no small-cap single-name data in this repo. CJL (1996) find
the drift is concentrated in small, illiquid, thinly-covered names, which is exactly the
segment this universe excludes. So this is a test of large-cap PEAD; a null here does **not**
refute the small-cap result, it is consistent with it.

## Data
- **Events:** EDGAR `submissions` JSON (incl. the older `filings.files` shards), 8-K filings
  whose `items` field contains **2.02** (Results of Operations), filed ≥ 2012-01-01.
  **6,019 raw filings across 99 tickers.** 37 universe members yield nothing: 30 are ETFs
  (no 8-Ks), MMC failed to download from yfinance and was dropped from the panel.
  `company_tickers.json` maps XOM and BLK to re-registered CIKs whose history starts after
  the reorg; predecessor CIKs (34088, 1364742) are added by hand in the fetcher.
- After collapsing multiple 2.02 filings for the same quarter (a second 8-K within 20 trading
  days of a kept one is dropped) and requiring t-1/t/t+1 prices: **5,647 usable announcements,
  99 tickers, 2012-01-05 → 2026-09-02** (~385/yr, ≈ 4.0 per name per year — the right order).
- **Prices:** `baseline.load_universe(broad=True)`, live yfinance, 4,698 trading-day rows
  2008-01-02 → 2026-09-03, 135 usable columns.

## Signal — and the filing-time ambiguity
EDGAR records a filing **date**, not a **time**, so we cannot know whether the market reacted
on day `t` or day `t+1`. As specified in the brief, the surprise is **the larger-in-absolute-
value of the two candidate 1-day abnormal returns**:

    W_t  = r(close[t-1]→close[t])   − SPY, same window     (filed pre-close)
    W_t1 = r(close[t]→close[t+1])   − SPY, same window     (filed post-close)
    surprise = W_t if |W_t| ≥ |W_t1| else W_t1

Their union is the close[t-1]→close[t+1] 2-day abnormal return, reported below as a
sensitivity row ("SENS tercile 2day-CAR"). **This max-abs rule is a real approximation and it
biases the sort towards larger-|CAR| events**; it cannot be resolved without EDGAR's
`acceptanceDateTime`, which the submissions JSON exposes only for recent filings. Both
quantities are fully known at close[t+1], the cohort is formed at the weekly rebalance on/after
t+1, and the engine applies weights the *next* day — so there is no look-ahead under either
reading. Mean |CAR| 3.96%, sd 5.36%.

## Portfolio
Each weekly rebalance date, rank every announcement whose reaction window completed in the last
5 trading days; go long the top tercile (or top quintile) equal-weight; hold 40 or 60 trading
days. Overlapping cohorts, equal weight across all open slots, gross 100%, 10 bps, next-day
execution (`engine.backtest`, `freq="W"`). Two tuned parameters (cut, hold) = the 4-point grid.

## Full sample (2012-01-20 → 2026-09-03)
| variant | CAGR | Vol | Sharpe | MaxDD | H1 / H2 | avg names | turnover |
|---|---|---|---|---|---|---|---|
| tercile h=40 | 16.8% | 17.8% | 0.96 | -34.7% | 1.11 / 0.87 | 22 | 23.7x |
| tercile h=60 | 18.9% | 17.6% | 1.07 | -33.5% | 1.29 / 0.93 | 32 | 8.5x |
| quintile h=40 | 16.8% | 18.8% | 0.92 | -36.0% | 1.13 / 0.78 | 15 | 23.4x |
| quintile h=60 | 19.4% | 18.6% | 1.05 | -35.0% | 1.35 / 0.84 | 21 | 9.0x |
| **CONTROL all-announcers h=60** (no sort) | **19.6%** | 16.8% | **1.15** | -33.8% | 1.37 / 1.03 | 87 | 5.6x |
| **CONTROL bottom-tercile h=60** (sort reversed) | **20.7%** | 17.5% | **1.16** | **-32.1%** | 1.30 / 1.09 | 32 | 8.5x |
| CONTROL mid-tercile h=60 | 18.1% | 16.4% | 1.10 | -35.7% | 1.37 / 0.95 | 30 | 8.3x |
| SENS tercile 2day-CAR h=60 | 19.3% | 17.5% | 1.10 | -33.5% | 1.36 / 0.92 | 32 | 8.5x |
| RULES v1 baseline (broad universe) | 6.9% | 10.8% | 0.67 | -21.2% | 0.86 / 0.50 | — | — |
| SPY | 14.9% | 16.6% | 0.92 | -33.7% | 1.06 / 0.86 | — | — |

**The controls are the result.** Long the *worst*-reacting third of announcers beats long the
best third on CAGR (+1.8pp), Sharpe (1.16 vs 1.07) and drawdown (-32.1% vs -33.5%). Holding
*every* announcer with no sort at all also beats the top tercile. The four headline rows are
long-only equal-weight exposure to 99 currently-listed large caps, cycled every 60 days — the
surprise ranking is decoration. The 2-day-CAR sensitivity (1.10) changes nothing, so the
filing-time approximation is not what kills it.

## Walk-forward (PROTOCOL rule 8), IS 2012-01-20–2018-12-31 / OOS 2019-01-01–2026-09-03
Sample starts 2012, so the rule-8 windows are shortened as the brief directs. Selection rule
pre-stated before any OOS number was read: highest IS Sharpe on the 4-point grid; ties → wider
cut, then shorter hold.

| variant | IS CAGR | IS Sharpe | IS MaxDD | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|
| tercile h=40 | 15.6% | 1.04 | -18.9% | 18.0% | 0.93 | -34.7% |
| tercile h=60 | 17.9% | 1.18 | -19.8% | 19.8% | 1.01 | -33.5% |
| quintile h=40 | 17.2% | 1.07 | -17.8% | 16.4% | 0.83 | -36.0% |
| **quintile h=60 (IS pick)** | **20.3%** | **1.25** | -18.8% | 18.6% | **0.92** | -35.0% |
| RULES v1 baseline (broad) | 8.4% | 0.83 | -9.7% | 5.5% | 0.54 | -21.2% |
| SPY | 12.0% | 0.94 | -19.3% | 17.6% | 0.94 | -33.7% |

The in-sample pick (quintile h=60) delivers **OOS Sharpe 0.92 — below SPY's 0.94** and with
nearly twice SPY's drawdown-adjusted risk. The point that *does* beat SPY out of sample
(tercile h=60, 1.01) is not the one the pre-stated rule selects. Classic in-sample-only win.

## KEEP tests (PROTOCOL rule 4)
| variant | 4a H1>base | 4a H2>base | 4a MaxDD | **4a** | 4b H1>SPY | 4b H2>SPY | 4b OOS>SPY | 4b DD ≤60% SPY | 4b CAGR ≥70% SPY | **4b** |
|---|---|---|---|---|---|---|---|---|---|---|
| tercile h=40 | pass | pass | FAIL | **FAIL** | pass | pass | FAIL | FAIL | pass | **FAIL** |
| tercile h=60 | pass | pass | FAIL | **FAIL** | pass | pass | pass | FAIL | pass | **FAIL** |
| quintile h=40 | pass | pass | FAIL | **FAIL** | pass | FAIL | FAIL | FAIL | pass | **FAIL** |
| quintile h=60 | pass | pass | FAIL | **FAIL** | pass | FAIL | FAIL | FAIL | pass | **FAIL** |

4a fails on drawdown everywhere (-33% to -36% vs the live book's -21.2%). 4b fails on the
MaxDD cap everywhere (the cap is -20.2%, i.e. 60% of SPY's -33.7%) and on OOS Sharpe at three
of four points. Nothing is close.

## Event study — where the drift actually is
Mean forward abnormal return (vs SPY) from close[t+1], by surprise tercile:

| horizon | low | mid | high | high − low | t |
|---|---|---|---|---|---|
| 20d | +0.17% | +0.21% | +0.64% | **+0.47%** | +1.98 |
| 40d | +0.79% | +0.29% | +0.82% | +0.03% | +0.09 |
| 60d | +1.60% | +0.34% | +1.13% | **−0.47%** | −1.07 |

(Overlapping windows → these t-stats are an optimistic upper bound.)

There is a small, marginally-significant drift at **20 days** (+0.47%, t≈2.0, which is roughly
2× the 10 bps round-trip cost and would not survive realistic slippage), and it is **gone by
40 days and reverses by 60**. The 40/60-day holds mandated by the brief sit exactly in the dead
zone. That is why the top tercile cannot beat the bottom tercile: the sort has no information
left at the horizon being traded. Note this diagnostic is nested — it is the same overlapping
event sample as the backtest, so it is corroboration, not an independent test.

## Memo (10 lines)
1. **Verdict: KILL** at all four grid points — fails 4a (drawdown vs the live book) and fails
   4b (MaxDD cap, and OOS Sharpe below SPY at the pre-stated pick).
2. The 17–19%/yr headline is not alpha: an unsorted control (19.6%/1.15) and a **reversed**
   control long the worst announcers (20.7%/1.16) both beat every sorted variant.
3. Event study explains it: drift is ~+0.47% at 20d (t≈2.0, overlapping) and zero-to-negative
   at the 40–60d horizons the brief specifies.
4. Nothing here justifies a rules change; do not carry any variant to Sunday review.
5. **Caveat — survivorship.** 99 currently-listed large caps over 2012–2026, a period with no
   permanent losers. This alone plausibly accounts for the whole 4–5pp/yr over SPY, and it
   inflates the controls as much as the signal (which is why the *relative* result stands).
6. **Caveat — wrong segment.** This is large-cap PEAD; CJL's effect lives in small caps. The
   null is evidence about this universe, not about the anomaly.
7. **Caveat — filing-time ambiguity.** EDGAR gives dates, not times; the max-abs rule is a
   guess about which day the market reacted, and it biases the sort toward large-|CAR| events.
   The 2-day-CAR sensitivity (Sharpe 1.10 vs 1.07) says this choice does not drive the verdict.
8. **Caveat — small sample.** 14.6 years, ~385 events/yr, one real bear market (2022) and one
   crash (2020); H1/H2 Sharpe spreads of 0.4–0.5 across variants show how unstable this is.
9. **Caveat — event hygiene.** Some 8-K/2.02 filings are not quarterly earnings (guidance
   updates, monthly sales); the 20-day dedup collapses duplicates but does not classify them.
10. **Worth one follow-up, not more:** a 20-day-hold version with a liquidity/size tilt is the
    only place the data points to — but at 20d the gross edge is ~0.5% against a 10 bps
    round trip plus real slippage, so the prior should be that it is uninvestable too.

## LEADERBOARD rows
| Date | Idea | CAGR | Sharpe | MaxDD | Sharpe H1 / H2 | Baseline Sharpe (H1/H2) | Verdict | Script |
|---|---|---|---|---|---|---|---|---|
| 2026-09-04 | pead-tercile-h40 | 16.8% | 0.96 | -34.7% | 1.11 / 0.87 | 0.67 (0.86/0.50) | KILL | research/backtests/2026-09-04_small-cap-pead.py |
| 2026-09-04 | pead-tercile-h60 | 18.9% | 1.07 | -33.5% | 1.29 / 0.93 | 0.67 (0.86/0.50) | KILL | research/backtests/2026-09-04_small-cap-pead.py |
| 2026-09-04 | pead-quintile-h40 | 16.8% | 0.92 | -36.0% | 1.13 / 0.78 | 0.67 (0.86/0.50) | KILL | research/backtests/2026-09-04_small-cap-pead.py |
| 2026-09-04 | pead-quintile-h60 | 19.4% | 1.05 | -35.0% | 1.35 / 0.84 | 0.67 (0.86/0.50) | KILL | research/backtests/2026-09-04_small-cap-pead.py |
| 2026-09-04 | pead-CONTROL-bottom-tercile-h60 (diagnostic) | 20.7% | 1.16 | -32.1% | 1.30 / 1.09 | 0.67 (0.86/0.50) | — | research/backtests/2026-09-04_small-cap-pead.py |
| 2026-09-04 | pead-CONTROL-all-announcers-h60 (diagnostic) | 19.6% | 1.15 | -33.8% | 1.37 / 1.03 | 0.67 (0.86/0.50) | — | research/backtests/2026-09-04_small-cap-pead.py |

_Baseline column is RULES v1 run on the broad universe over the same 2012-2026 sample.
Research, not investment advice._

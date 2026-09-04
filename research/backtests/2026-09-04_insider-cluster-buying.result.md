# Idea 32 — insider cluster buying (Cohen, Malloy & Pomorski 2012) — 2026-09-04

Script: `research/backtests/2026-09-04_insider-cluster-buying.py` ·
console: `2026-09-04_insider-cluster-buying.console.txt` ·
insider cache: `data/form4_purchases.csv` (2,600 qualifying purchases, 96 tickers,
2012-01-04 → 2026-08-26).
Prices: `baseline.load_universe(broad=True)` → 136 names, `MMC` dropped (no price history —
Marsh & McLennan's ticker is now MRSH and yfinance returns an empty column, in the committed
cache too), so 135 names are tradable. Trading-day index verified in-script (250–253 rows/yr).
Sample **2012-01-01 → 2026-09-04**, weekly rebalance, 10 bps per unit turnover, next-day
execution. `load_universe` re-downloads from yfinance on each run, so figures move in the third
decimal between runs; the console file is the run these tables come from.

## Verdict

**hold=12m → PARK. hold=6m → KILL.** Neither reaches a KEEP path, and the binding constraint is
**drawdown, not signal**.

- **4a (beat the book): FAIL, both.** MaxDD −39.7% / −39.8% against RULES v1's −21.2%.
- **4b (capital-worthy): FAIL, both — for different reasons.**
  `hold=12m` clears every Sharpe test with room (H1 1.308 vs SPY 1.127, H2 1.284 vs 0.847, OOS
  1.359 vs 0.936) and its CAGR of 26.6% is 175% of SPY's, but 4b caps MaxDD at 60% of SPY's
  (−20.2%) and the book draws down **−39.7%** — one test of five, missed by 2×.
  `hold=6m` fails on Sharpe as well: H1 0.958 < SPY's 1.127.
- **PARK** rather than KILL for `hold=12m` because the edge is present, survives the rule-8
  walk-forward and survives dropping its largest contributor. What fails is position sizing,
  which this script deliberately does not tune.

## LEADERBOARD rows

| Date | Idea | CAGR | Sharpe | MaxDD | Sharpe H1 / H2 | Baseline Sharpe (H1/H2) | Verdict | Script |
|---|---|---|---|---|---|---|---|---|
| 2026-09-04 | insider-cluster-buying hold=6m (broad universe, 2012+) | 21.2% | 0.97 | -39.8% | 0.96 / 1.01 | 0.66 (0.86/0.49) | KILL | research/backtests/2026-09-04_insider-cluster-buying.py |
| 2026-09-04 | insider-cluster-buying hold=12m (broad universe, 2012+) | 26.6% | 1.27 | -39.7% | 1.31 / 1.28 | 0.66 (0.86/0.49) | PARK (4b: Sharpe yes, MaxDD no) | research/backtests/2026-09-04_insider-cluster-buying.py |
| 2026-09-04 | RULES v1 baseline, 2012+ broad-universe sample — reference | 6.8% | 0.66 | -21.2% | 0.86 / 0.49 | 0.66 (0.86/0.49) | — | research/backtests/2026-09-04_insider-cluster-buying.py |
| 2026-09-04 | SPY buy & hold, 2012+ sample — reference | 15.2% | 0.94 | -33.7% | 1.13 / 0.85 | 0.66 (0.86/0.49) | — | research/backtests/2026-09-04_insider-cluster-buying.py |

Supporting risk figures, same sample:

| | Vol | Sortino | Calmar |
|---|---|---|---|
| hold=6m | 22.3% | 1.33 | 0.53 |
| hold=12m | 20.2% | 1.68 | 0.67 |
| RULES v1 | 10.8% | 0.85 | 0.32 |
| SPY | 16.5% | 1.16 | 0.45 |

## Walk-forward (PROTOCOL rule 8)

Parameters chosen on **2012–2018** only, evaluated untouched on **2019–2026**. The split is
shifted from the protocol's 2009–2016 / 2017–2026 because Form 4 XML coverage only becomes
complete in 2012 — stated here rather than silently absorbed. Selection rule, fixed before
looking at the OOS column: highest in-sample Sharpe, ties to the shorter hold.

| | IS Sharpe | IS CAGR | OOS Sharpe | OOS CAGR | OOS MaxDD |
|---|---|---|---|---|---|
| hold=6m | 0.852 | 14.9% | 1.073 | 27.1% | −39.8% |
| **hold=12m** (IS pick) | **1.185** | **19.8%** | **1.359** | **33.2%** | **−39.7%** |
| RULES v1 | 0.813 | 8.2% | 0.533 | 5.5% | −21.2% |
| SPY | 0.990 | 12.6% | 0.936 | 17.6% | −33.7% |

The in-sample pick is also the better arm out of sample, and its OOS Sharpe (1.359) beats both
benchmarks. The signal is not an in-sample artefact. The drawdown is identical in and out of
sample (−39.7%), which is the point: it is structural, not a one-off.

## Clusters per year

Cluster = ≥2 distinct reporting owners with qualifying open-market purchases (Form 4,
non-derivative table, code P, acquired, shares × price ≥ $10,000) whose **transaction** dates
fall inside a 30-calendar-day window. Signal date = the later of the two **filing** dates, so
nothing is used before it is public (median filing lag 2 days, p90 4 days).

| Year | Cluster signal-days | Distinct tickers | Qualifying purchases |
|---|---|---|---|
| 2012 | 20 | 8 | 155 |
| 2013 | 4 | 2 | 94 |
| 2014 | 12 | 5 | 452 |
| 2015 | 14 | 10 | 162 |
| 2016 | 19 | 13 | 414 |
| 2017 | 14 | 4 | 176 |
| 2018 | 19 | 11 | 233 |
| 2019 | 28 | 14 | 124 |
| 2020 | 26 | 17 | 209 |
| 2021 | 5 | 4 | 74 |
| 2022 | 12 | 7 | 223 |
| 2023 | 13 | 4 | 79 |
| 2024 | 6 | 6 | 25 |
| 2025 | 10 | 7 | 112 |
| 2026 (to Aug 26) | 13 | 7 | 68 |
| **Total** | **215** | **57 distinct** | **2,600** |

Cluster size: 128 two-insider, 42 three, 14 four, 31 five-or-more (max 13). Most-clustered
names: GE 27 signal-days, T 14, NEE 12, KO / SCHW / ABBV 9 each, BAC 8. 551 distinct reporting
owners; median purchase $406k.

**Clusters are rare and counter-cyclical**: they spike after drawdowns (2012 post-GFC
financials, 2016, 2018–19, 2020) and dry up in melt-ups (5 in 2021, 6 in 2024). Only 57 of the
108 non-ETF names ever produce one.

## Why it draws down 40% — the concentration problem

This governs the verdict, and it follows directly from the strategy as specified (equal weight,
gross 100%, cash only when nothing qualifies):

| | avg gross | avg names | median names | days with ≤2 names | days in cash | turnover/yr |
|---|---|---|---|---|---|---|
| hold=6m | 99.1% | 4.4 | 4 | **28.5%** | 0.9% | 6.9× |
| hold=12m | 99.4% | 7.9 | 7 | 2.4% | 0.6% | 4.2× |

`hold=6m` is a **1–4 stock portfolio at full exposure for more than a quarter of the sample**.
That is why its vol is 22.3% and its H1 Sharpe sits below SPY's despite a 21.2% CAGR — not
enough breadth for the Sharpe to survive. `hold=12m` roughly doubles effective breadth purely
by holding longer, and that alone lifts Sharpe 0.97 → 1.27 and cuts vol 22.3% → 20.2%. **The
6m-vs-12m gap is mostly a breadth effect, not a horizon effect** — a caution against reading
"insider signals decay slowly" out of this table.

It is **not** one lucky ticker. Dropping the single largest gross contributor:

- hold=6m ex-`C`: 20.8% / Sharpe 0.96 / −39.8%, halves 0.93 / 1.00 (from 21.2% / 0.97)
- hold=12m ex-`AVGO`: 25.7% / Sharpe 1.23 / −39.7%, halves 1.31 / 1.22 (from 26.6% / 1.27)

The top-5 contributors are spread across sectors and eras (hold=12m: AVGO +0.24, SCHW +0.21,
BSX +0.21, TSLA +0.20, BAC +0.20, out of +3.82 total gross).

**Vol-matched diagnostic** — each book scaled by ONE full-sample constant to SPY's 16.5% vol.
Uses full-sample information, so it is a diagnostic and not a tradable rule:

| | scalar | CAGR | Sharpe | MaxDD |
|---|---|---|---|---|
| hold=6m | ×0.74 | 15.9% | 0.97 | −30.9% |
| hold=12m | ×0.82 | 21.7% | 1.27 | −33.5% |
| RULES v1 | ×1.54 | 10.0% | 0.66 | −31.2% |
| SPY | ×1.00 | 15.2% | 0.94 | −33.7% |

At matched risk `hold=12m` earns **+6.5pp/yr over SPY** with a drawdown just inside SPY's — so
the excess return is not merely leverage. But note the scalar that gets there (×0.82) still
leaves MaxDD at −33.5%, far outside 4b's −20.2% cap. A real fix has to change **breadth or
timing**, not just size.

## Calendar-year returns

| Year | hold=6m | hold=12m | RULES v1 | SPY |
|---|---|---|---|---|
| 2012 | +26.5% | +22.5% | +15.7% | +16.0% |
| 2013 | +27.8% | +58.9% | +19.4% | +32.3% |
| 2014 | +13.0% | +9.3% | −0.7% | +13.5% |
| 2015 | +27.5% | +22.4% | +6.8% | +1.2% |
| 2016 | +29.5% | +33.2% | +0.4% | +12.0% |
| 2017 | −6.3% | +17.5% | +14.7% | +21.7% |
| 2018 | −6.5% | −13.3% | +2.7% | −4.6% |
| 2019 | +53.1% | +47.8% | +7.3% | +31.2% |
| 2020 | +55.1% | +34.6% | +4.1% | +18.3% |
| 2021 | +8.9% | +26.2% | +16.3% | +28.7% |
| 2022 | +1.5% | +19.5% | −4.1% | −18.2% |
| 2023 | +14.8% | +29.5% | −7.8% | +26.2% |
| 2024 | +34.8% | +52.0% | +21.1% | +24.9% |
| 2025 | +68.8% | +34.4% | +6.6% | +17.7% |
| 2026 (to Sep 4) | −8.3% | +13.0% | +1.5% | +13.8% |

2022 (`hold=12m` +19.5% against SPY's −18.2%) is the most interesting year and the most fragile:
it comes from a handful of clusters bought into the 2022 selloff. One good year in a 15-year
sample is an anecdote, not a demonstrated defensive property.

## Data provenance and what was skipped

The brief's prescribed download method turned out not to be feasible as specified. The
substitution is the largest single caveat on these numbers, so it is reported in full.

- The 108 non-ETF names filed **128,930 Form 4s** between 2012-01-01 and today. The prescribed
  pre-filter (keep only ticker-months with ≥2 filings) removes almost nothing — **126,987
  remain** — because large caps file Form 4s continuously for grants, vesting and 10b5-1 sales.
  At ≤8 req/s that crawl is ~4.4 hours, and the 6,000-download cap would have sampled 4.7% of
  filings. At a 4.7% sample the probability of catching **both** legs of a genuine two-insider
  cluster is ~0.2%: the signal would have been empty and the backtest meaningless. The stated
  fallback (60 largest names) does not fix this either — still ~70k filings.
- **2012-01-01 → 2026-03-31 therefore comes from the SEC's own structured Form 345 data sets**
  (`https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/<YYYY>q<N>_form345.zip`)
  — 57 quarterly files, 57 requests, ~12 minutes. These are the SEC's parse of exactly the same
  Form 4 XML (`TRANS_CODE`, `TRANS_SHARES`, `TRANS_PRICEPERSHARE` per non-derivative
  transaction, `RPTOWNERCIK` per filing). **2,552 of the 2,600 rows.**
- **2026-04-01 → today is not published as a data set yet**, so that window *is* crawled per
  filing exactly as briefed: `https://data.sec.gov/submissions/CIK##########.json` plus the
  older `filings.files` shards, XML parsed with
  `research/deepvalue/fetch_filings.parse_form4`. 3,016 Form 4s found, 2,911 after the
  ≥2-per-ticker-month pre-filter, **all 2,911 downloaded** (cap 6,000; nothing capped out),
  ~55 minutes. **48 of the 2,600 rows.**
- **SKIPPED / not downloaded:** the ~126,000 individual Form 4 XML documents dated before
  2026-04-01. They are covered by the data sets instead. Nothing was dropped for the download
  cap; the only pre-filter applied is the briefed ≥2-filings-per-ticker-month rule on the
  2026Q2+ crawl (105 filings excluded by it).
- **Cross-check (`--parse-check`, offline):** the two sources do not overlap in time, and
  re-crawling a sample of the pre-2026Q2 filings hit SEC rate limiting (HTTP 503) after a build
  this size. Instead the check runs `parse_form4` over the 1,092 Form 4 XML documents already
  cached by the deep-value pipeline (`research/deepvalue/filings/*/raw/`) and compares them to
  the same accessions in the cached quarterly data sets: **525 accessions present in both, 525
  agree on total code-P purchase value to within 1%, 0 disagree** (16 of the 525 contain a
  code-P purchase, so the check also confirms 509 true negatives — no spurious purchases from
  either source). Different issuers, same document format and same quarters.
- 28 universe tickers are ETFs with no insiders and no CIK in the SEC ticker map (SPY, QQQ, the
  XL\* sector funds, TLT, GLD, …). MMC is absent from the current ticker map because the ticker
  is now MRSH; its historical Form 4s are still matched by symbol, but with no usable price
  column its single cluster is dropped. XOM's current ticker-map CIK is a 2025 holdco with no
  pre-2025 filings — symbol matching (primary) rather than CIK matching (fallback) handles it.

## Memo

1. **Verdict: `hold=12m` PARK, `hold=6m` KILL.** Neither reaches KEEP; the 12m arm fails 4b on
   one test of five and passes the other four.
2. **The edge is real and out of sample.** IS Sharpe 1.185 → OOS 1.359, against SPY's 0.990 →
   0.936 and RULES v1's 0.813 → 0.533. It survives the rule-8 walk-forward and survives dropping
   its largest contributor.
3. **The book is not investable as specified.** Equal weight at 100% gross over a signal this
   sparse means 4.4 names (6m) or 7.9 names (12m); MaxDD −39.7% is roughly double 4b's −20.2%
   cap, and identical in both halves.
4. **6m vs 12m is a breadth effect, not a horizon effect.** The longer hold wins mainly because
   it doubles the number of simultaneous positions — do not read it as slow signal decay.
5. **Survivorship bias is first-order here, not boilerplate.** `universe_broad.json` is today's
   constituent list and this is a 4–8 name concentrated book. Insider clusters concentrate in
   *distressed* names (2012 financials, 2018–19 GE and T, 2020) — precisely the population where
   the losers get delisted out of the universe. C and BAC contributing +0.31 and +0.24 is a
   post-GFC survivor story. **The true CAGR is materially below 26.6%; the drawdown is not.**
6. **The universe is also wrong for the idea.** CMP's effect lives in small and mid caps with
   real information asymmetry. 108 mega caps yield only 215 cluster-days in 15 years and only 57
   names ever qualify — a thin, lumpy signal on the least inefficient part of the market.
7. **The signal is regime-timed.** Clusters spike after selloffs (2012, 2016, 2018–19, 2020,
   2022) and vanish in melt-ups (5 in 2021, 6 in 2024). Much of the CAGR may be mechanical
   buy-the-dip beta rather than insider information; this backtest cannot separate the two.
8. **CMP's actual contribution is untested here.** Their result is that only *opportunistic*
   insiders predict returns and routine (same-month-every-year) traders do not. This script uses
   every code-P buyer. The routine/opportunistic split is the obvious next test and the one most
   likely to raise Sharpe without touching sizing.
9. **What would have to change for a KEEP:** breadth or timing, not a scalar — a constant
   vol-match to SPY still leaves MaxDD at −33.5%. Candidates, deliberately **not** run here so
   this stays one idea with one honest verdict: a minimum-names floor with the balance in cash,
   a cluster sleeve capped at 20–30% of a diversified book, or the opportunistic filter above.
10. **Data caveat, plainly:** 98% of the insider rows come from the SEC's own Form 345 data sets
    rather than a per-filing XML crawl, because the briefed crawl is a 4.4-hour job whose
    6,000-filing cap would have given a ~0.2% cluster detection rate. The parser and the data
    sets were cross-checked on 525 shared filings with zero disagreements.

_Research, not investment advice. Past performance is not indicative of future results._

# Idea 36 — spin-off calendar (2026-09-04)

Scripts: `research/spinoffs.py` (data build) · `2026-09-04_spinoff-calendar.py` (event study)
Console: `2026-09-04_spinoff-calendar.console.txt` · Events: `2026-09-04_spinoff-calendar.events.csv`
Data: `data/spinoffs.csv` (278 registrants, EDGAR full-text search, 2015-01-01 → 2026-09-04),
prices from yfinance. Sample 2015-03-20 → 2026-09-03, 10 bps on entry and on exit.

## Verdict

**PARK.** The direction of the Cusatis-Miles-Woolridge result reproduces — an investable
spin-off book returns 32.1%/yr at Sharpe 1.11 against IWM's 9.2%/0.51 — but three things stop
this being a KEEP under either PROTOCOL path, and none of them is fixable by more tuning:

1. **It is five names.** Dropping the top 5 winners by return takes CAGR 32.1% → 20.7% and
   Sharpe 1.11 → 0.82; dropping the top 3 gives 23.8%/0.90. Dropping the worst 3 *improves*
   it to 34.8%/1.20. A 105-event sample whose result moves that far on five observations is
   not an estimate of an effect, it is an estimate of five stocks.
2. **The per-event evidence is weak.** 59 of 105 events beat IWM over their 12 months — a
   one-sided sign test p of 0.12. Median excess +9.4%, but the 10%-trimmed mean is +10.9%
   against an untrimmed mean of +30.4%, i.e. the mean is a tail artefact.
3. **Survivorship is not a caveat here, it is the sample.** Of 278 10-12B registrants, only
   171 resolve to a ticker and 129 to usable prices. The 107 with no ticker are a mix of
   shells that never listed *and* spin-offs that died and were scrubbed from EDGAR's current
   ticker map. There is no way to tell which from this data, and the bias runs one way.

MaxDD -45.3% also fails 4b outright (cap is 60% of IWM's -41.1% = -24.7%), and this is not a
book that can be run at PROTOCOL's no-leverage 100%: mean 8.6 positions at 28.7% vol.

The idea is worth keeping alive because the *data asset* is now built and improves with time.
What it needs before a re-test is a point-in-time ticker map (so dead spin-offs stay in the
sample) — see "What would change the verdict".

## What the data build produced

`research/spinoffs.py` enumerates every Form 10-12B / 10-12B/A via EDGAR full-text search
(`https://efts.sec.gov/LATEST/search-index?q=&forms=10-12B&startdt=..&enddt=..&from=..`),
quarter by quarter, 2015 → today. **An empty `q` with a `forms` filter is the exhaustive
form-type listing**: for 2024Q1 it returns exactly the 11 filings in the quarterly full index
(`.../full-index/2024/QTR1/form.idx`), one hit per *filing*. A non-empty `q` such as
`"Form 10"` is strictly narrower (it only matches documents containing the phrase) and returns
one hit per *document* — 29 hits for the same 11 filings. Use the empty query.

914 filings → 278 registrants (13 seen only via an amendment whose original predates 2015).

| year | registrants | w/ ticker | w/ dist. date |
|---|---|---|---|
| 2015 | 55 | 28 | 51 |
| 2016 | 33 | 16 | 25 |
| 2017 | 10 | 4 | 9 |
| 2018 | 27 | 17 | 26 |
| 2019 | 36 | 12 | 15 |
| 2020 | 16 | 10 | 13 |
| 2021 | 20 | 17 | 20 |
| 2022 | 20 | 19 | 19 |
| 2023 | 19 | 13 | 14 |
| 2024 | 17 | 15 | 16 |
| 2025 | 8 | 8 | 7 |
| 2026 (to 09-04) | 17 | 12 | 11 |
| **total** | **278** | **171** | **226** |

The 2015-16 bulge is real but is not spin-off activity: those years carry a wave of
shell/blank-check 10-12B registrations (many from the same filing agents), which is why their
ticker-resolution rate is ~50% against 2022-25's ~95%. **Form 10-12B is not a synonym for
"spin-off"** and the study has to screen, which it does — see the arms below.

Distribution date: Form 10 registration is automatically effective 60 days after filing, which
is a poor proxy for the actual distribution. The script instead takes, in order of preference,
the **CERT** (the exchange's certification approving the listing — 149 cases), **8-A12B** (5),
or the first **8-K** filed after registration (72); 52 have none. **25-NSE is recorded but is a
delisting notice**, so it marks the end of a listing and is carried for completeness only.
CERT still leads the first trade by ~2-4 weeks (GE Vernova: CERT 2024-03-07, first trade
2024-04-02), so the event study does **not** use it — it uses the security's first traded day
from prices, which is the only unambiguous date available.

Spot-check that the calendar is right: GEV, SOLV, GEHC, VLTO, KNF, FTRE, PHIN, NATL, VSTS, WS,
KLG, CURB, ECG, SNDK, AMTM, RHLD, AMRZ, RAL, SOLS, RXO, MBC, CR, MSGE, ESAB, GXO, OGN, EMBC
are all present with correct dates.

## Event-study design (fixed before any result was read)

- **Event date** = the security's first traded day from prices, not from filings.
- **Entry** = close of first trade + 30 trading days. **Hold** = 252 trading days.
- **Portfolio** = calendar-time, equal weight over whatever is live (the standard construction
  for staggered overlapping events). Reported both daily-rebalanced (Fama convention) and
  drift-weighted (equal dollars injected at each event's own entry, weights drift after).
- **Benchmark** = IWM as the brief specifies; SPY reported alongside.
- **Ticker-recycling guard**: a ticker is accepted only if its price history *begins* within
  [-60d, +730d] of the 10-12B filing. Without this, a 2019 registrant inherits a decade of an
  unrelated issuer's prices. 26 events are dropped by it.
- **Two arms, both fully reported.** `ALL` = every registrant with prices. `INVESTABLE` = also
  NYSE/Nasdaq listed, entry close ≥ $5, 20d median dollar volume at entry ≥ $1m — measured at
  the entry bar, no look-ahead. 105 of 129 events qualify. This is the only screen, and it is
  an investability screen rather than a tuned parameter.

## Results

Portfolio, 2015-03-20 → 2026-09-03 (2,882 days, invested 100% of days; mean 8.6 positions in
the investable arm, max 15):

| book | CAGR | Sharpe | MaxDD | vol |
|---|---|---|---|---|
| INVESTABLE, daily-EW | 32.1% | 1.11 | -45.3% | 28.7% |
| INVESTABLE, drift | 33.7% | 1.08 | -49.1% | 31.3% |
| ALL, daily-EW | 24.6% | 0.74 | -46.3% | 38.8% |
| ALL, drift | 47.4% | 1.05 | -46.3% | 46.4% |
| IWM | 9.2% | 0.51 | -41.1% | 22.4% |
| SPY | 14.0% | 0.83 | -33.7% | 17.6% |

The `ALL` arm's 47.4% drift CAGR is a single OTC shell (LDSN, +5,850% over its 12 months) and
should be read as a warning about the raw 10-12B list, not as a result.

Halves, INVESTABLE drift: H1 (2015-03 → 2020-12) **16.6% / 0.70 / -49.1%** against SPY's
12.7%/0.74; H2 (2020-12 → 2026-09) **53.5% / 1.41 / -34.0%** against SPY's 15.4%/0.94. The
edge is overwhelmingly H2, and H1 does not beat SPY on Sharpe — **4b fails in H1 on Sharpe and
in both halves on drawdown.**

Per-event, 12-month holds:

| arm | n | hit vs IWM | mean excess | median excess | t | mean log ret (t) |
|---|---|---|---|---|---|---|
| INVESTABLE | 105 | 56.2% | +30.4% | +9.4% | +2.37 | +0.147 (+2.67) |
| ALL | 129 | 53.5% | +66.6% | +5.9% | +1.45 | -0.011 (-0.12) |

Note the ALL arm's mean log return is *negative* while its mean simple return is +77.6%: the
raw 10-12B population loses money in the median and typical case and is rescued entirely by one
tail. The investable screen is what makes the number mean anything.

By first-trade year (INVESTABLE, median excess vs IWM): 2015 +9.4%, 2016 +25.9%, 2017 -4.8%,
2018 -4.1%, 2019 -10.5%, 2020 +9.2%, 2021 -6.6%, 2022 +21.6%, 2023 +5.9%, 2024 +16.8%,
2025 +20.9%, 2026 -2.1%. Four of twelve cohorts are negative and no cohort has n > 13.

Robustness (INVESTABLE, daily-EW):

| book | CAGR | Sharpe | MaxDD |
|---|---|---|---|
| all 105 | 32.1% | 1.11 | -45.3% |
| ex top-1 (SNDK) | 28.8% | 1.04 | -45.3% |
| ex top-3 (SNDK, RHLD, CRNC) | 23.8% | 0.90 | -48.8% |
| ex top-5 (+ ASIX, PNTG) | 20.7% | 0.82 | -49.4% |
| ex worst-1 (FEAM) | 33.6% | 1.16 | -45.3% |
| ex worst-3 (+ KLXE, CYCN) | 34.8% | 1.20 | -43.2% |

Sign test on excess vs IWM: 59/105 positive, one-sided p ≈ 0.12. Trimmed mean excess +10.9%.

## Caveats (all of them bind)

1. **Survivorship, twice.** (a) The ticker map comes from *today's* EDGAR submissions feed and
   `company_tickers.json`; a spin-off that was acquired or delisted long ago may have no
   current ticker and silently leave the sample. 107 of 278 registrants have no ticker.
   (b) 10 of 129 events are truncated because prices stop mid-hold. For an acquisition that is
   roughly correct (you cash out near the deal price); for a delisting-to-zero it biases the
   result **up**, because the final collapse is simply missing.
2. **The recycling guard has a bias of its own.** It drops 26 events, including real spin-offs
   whose ticker Yahoo backfills with the predecessor's history (AA, JBTM, HTZ). Those are
   systematically the *large-parent* spin-offs — the ones the literature is actually about.
3. **n = 105 over 11 years**, ~9 events a year, four negative cohorts. Nothing here survives an
   honest multiple-comparisons haircut.
4. **This book cannot be run under PROTOCOL rule 2.** 28.7% vol, -45.3% MaxDD, mean 8.6 names,
   and positions that only exist when a spin-off happens to have occurred 30 days ago.
5. **No walk-forward (rule 8) was run** and none should be: with one tuned decision (the
   30-day entry lag, taken from the brief, not fitted) and a 105-event sample, an OOS split
   would leave ~50 events per side and be uninterpretable. Rule 8 is a KEEP-candidate
   requirement; this is a PARK.
6. Prices are yfinance adjusted closes. Spin-off adjustment for the *parent* is a known weak
   point in that data, but this study never holds a parent.

## What would change the verdict

- A **point-in-time ticker map** built from each CIK's own 8-A12B/CERT filings and historical
  `company_tickers.json` snapshots, so dead spin-offs stay in the sample. This is the single
  highest-value fix and it is tractable — the submissions JSON is already cached.
- A hand-classified `is_true_spinoff` flag (parent CIK + distribution ratio from the Form 10
  information statement) to replace the liquidity proxy. ~278 rows is a feasible manual pass.
- Re-run at 6- and 24-month horizons, which is what Cusatis-Miles-Woolridge actually tested;
  the 12-month window here was chosen by the brief.
- Re-check in 2-3 years, when the calendar has ~30 more events and `data/spinoffs.csv` can be
  refreshed by re-running `research/spinoffs.py`.

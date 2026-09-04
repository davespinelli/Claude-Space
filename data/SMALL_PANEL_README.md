# Small-cap price panel — survivorship warning

Built 2026-09-04 by `research/cache_small.py`.

Files: `prices_small.csv` (adjusted closes, 4dp), `volume_small.csv` (share volume),
`small_meta.csv` (ticker, first_date, last_date, n_rows, max_1d_move, n_steps).

Panel: 483 tickers x 4194 trading days,
2010-01-04 to 2026-09-04.
Source universe: `research/deepvalue/universe_under2b.csv` (485 tickers);
2 dropped for <250 rows of history, 0 returned no data.

## SURVIVORSHIP BIAS — read before using any backtest on this panel

The universe is the **current** constituent list of the sub-$2B value screen, so
the panel contains only companies that are still listed, still public and still
under $2B **today**. It does not contain the small caps of 2010-2025 that were
acquired, taken private, bankrupted, delisted, or that grew past $2B. Every name
in the panel survived the whole sample by construction.

Consequences for any test run on this panel:

- Returns are biased **upward** (dead names are missing; the acquired ones are
  missing their takeover premium, which cuts the other way but is far smaller).
- Cross-sectional strategies look better than they were, especially deep-value
  and low-price sorts, where the missing names are exactly the ones that failed.
- The bias grows with lookback: 2010-2015 results are the least trustworthy.

Treat results here as **relative** comparisons between strategies on the same
panel, never as achievable absolute returns. Any leaderboard row from this panel
must carry the survivorship caveat.

Prices are forward-filled across missing days; volume is left as NaN where the
vendor had no bar. Panel index is the equity trading-day calendar (no crypto in
this universe, so no calendar-day contamination — cf. QUEUE idea 38).

## Data quality — repaired

`cache_small.clean()` masks two classes of bad cell to NaN before the panel is saved:

- **3299 non-positive closes across 2 tickers.** yfinance's back
  adjustment drives heavy distributors negative (VATE is negative for its whole
  pre-2020 history) and emits runs of literal zeros before a listing begins (DEC,
  732 zero bars in 2021-23). A price <= 0 is not a price.
- **32 isolated one-day bad prints across 14 tickers** — a bar more
  than 60% from BOTH neighbours in the same direction (PROP 41 -> 2 -> 59 on
  2020-02-27; SPCB 144 -> 8 -> 144 on 2012-09-25).

## Data quality — FLAGGED, NOT repaired (you must decide)

42 tickers contain a one-day move above +100% that **does not reverse** — a
persistent level step. These are missing split adjustments, post-bankruptcy
re-listings where the pre-event equity was cancelled, or genuine events. They are
left in the panel because some are real, but an unfiltered momentum or reversal
test **will be dominated by them**: AMPY jumps +16,083% on 2016-10-24 and stays
there.

`small_meta.csv` carries `max_1d_move` and `n_steps` per ticker. To exclude the
worst, filter on it:

```python
meta = pd.read_csv("data/small_meta.csv", index_col=0)
px = px[[c for c in px.columns if meta.max_1d_move.get(c, 0) < 1.0]]
```

Worst offenders (ticker: max 1-day move):

- `AMPY` +16,079%
- `HCWC` +3,400%
- `DEC` +1,907%
- `ORGO` +513%
- `BYRN` +380%
- `MVST` +339%
- `KODK` +318%
- `PROP` +300%
- `PBYI` +295%
- `GEVO` +262%
- `RXT` +227%
- `BATL` +212%
- `DCTH` +205%
- `PAYS` +200%
- `AEYE` +200%

#!/usr/bin/env python3
# survivorship: current constituents of the sub-$2B screen only
"""Cache daily adjusted closes AND share volumes since 2010 for the 485-name
sub-$2B universe (research/deepvalue/universe_under2b.csv) so backtests can run
offline.  Writes:

    data/prices_small.csv   adjusted closes, 4dp   (index Date, cols tickers)
    data/volume_small.csv   share volume, integer  (same index/cols)
    data/small_meta.csv     ticker, first_date, last_date, n_rows

SURVIVORSHIP BIAS: the universe file is the *current* output of the sub-$2B
value screen.  Names that were small caps in 2010 and have since been acquired,
delisted or grown past $2B are absent, and every surviving name is present for
its whole history.  Any backtest on this panel is biased upward.  See
data/SMALL_PANEL_README.md.

Run: .venv/bin/python research/cache_small.py
"""
from __future__ import annotations
import datetime as dt
from pathlib import Path
import numpy as np, pandas as pd, yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
UNIVERSE_CSV = ROOT / "research" / "deepvalue" / "universe_under2b.csv"
DATA = ROOT / "data"
START = "2010-01-01"
BATCH = 60
MIN_ROWS = 250          # ~1 trading year; below that the name is useless for 12-1 signals
MAX_MB = 1              # always gzip: keeps the weekly refresh diff small in git


def load_tickers(path: Path = UNIVERSE_CSV) -> list[str]:
    """Tickers from the screen, normalised for yfinance (class shares use '-', e.g. BRK-B)."""
    s = pd.read_csv(path, usecols=["ticker"])["ticker"].astype(str).str.strip().str.upper()
    s = s.str.replace(".", "-", regex=False).str.replace("/", "-", regex=False)
    return sorted({t for t in s if t and t != "NAN"})


def _download(tickers, start=START):
    """download_aligned-style handling, minus the crypto branch (no crypto in this universe).

    Returns (closes, volumes) on the equity trading-day index.  Missing tickers
    are simply absent from the returned columns.
    """
    raw = yf.download(list(tickers), start=start, auto_adjust=True,
                      progress=False, threads=True, group_by="column")
    if raw is None or len(raw) == 0:
        return pd.DataFrame(), pd.DataFrame()
    out = []
    for field in ("Close", "Volume"):
        df = raw[field]
        if isinstance(df, pd.Series):
            df = df.to_frame(list(tickers)[0])
        out.append(df.dropna(how="all"))
    close, vol = out
    close = close.dropna(axis=1, how="all")
    vol = vol.reindex(index=close.index, columns=close.columns)
    return close, vol



def clean(px: pd.DataFrame):
    """Mechanical data-quality pass on raw (un-ffilled) closes.

    Two repairs, both unambiguous, applied by masking the offending cells to NaN:
      1. non-positive closes - yfinance back-adjustment can drive a heavily
         distributing name negative (VATE) or emit a run of literal zeros before
         a listing really begins (DEC).  A price <= 0 is not a price.
      2. isolated one-day bad prints - a bar more than 60% away from BOTH
         neighbours in the SAME direction (PROP 41 -> 2 -> 59, SPCB 144 -> 8 -> 144).

    NOT repaired, only flagged: persistent level steps (a >100% one-day move that
    does not come back).  Those are missing split adjustments, post-bankruptcy
    re-listings of a cancelled equity (AMPY +16083% in 2016) or genuine events,
    and the caller must decide.  Their tickers are listed in small_meta.csv
    (max_1d_move, n_steps) and in data/SMALL_PANEL_README.md.
    """
    n_nonpos = int((px <= 0).sum().sum())
    n_nonpos_t = int(((px <= 0).sum() > 0).sum())
    p = px.mask(px <= 0)
    prev, nxt = p.shift(1), p.shift(-1)
    dev_p, dev_n = p / prev - 1, p / nxt - 1
    spike = (dev_p.abs() > 0.60) & (dev_n.abs() > 0.60) & (np.sign(dev_p) == np.sign(dev_n))
    p = p.mask(spike)
    r = p.ffill().pct_change()
    step = r.abs() > 1.0
    rep = dict(n_nonpos=n_nonpos, n_nonpos_t=n_nonpos_t,
               n_spike=int(spike.values.sum()), n_spike_t=int((spike.sum() > 0).sum()),
               step_counts=step.sum()[step.sum() > 0].sort_values(ascending=False),
               max_move=r.max())
    return p, rep


def build(start=START, batch=BATCH, verbose=True):
    tickers = load_tickers()
    if verbose:
        print(f"universe: {len(tickers)} tickers from {UNIVERSE_CSV.name}")
    closes, vols, missing = [], [], []
    batches = [tickers[i:i + batch] for i in range(0, len(tickers), batch)]
    for i, chunk in enumerate(batches, 1):
        try:
            c, v = _download(chunk, start)
        except Exception as e:
            if verbose:
                print(f"  batch {i}/{len(batches)}: FAILED ({type(e).__name__}: {e})")
            missing += chunk
            continue
        got = set(c.columns)
        missing += [t for t in chunk if t not in got]
        closes.append(c); vols.append(v)
        if verbose:
            print(f"  batch {i}/{len(batches)}: {len(got)}/{len(chunk)} tickers, {len(c)} rows")

    if missing:                                   # retry the failures once, one batch
        if verbose:
            print(f"retrying {len(missing)} failed tickers once: {', '.join(sorted(missing)[:12])}"
                  + (" ..." if len(missing) > 12 else ""))
        retry, still = sorted(set(missing)), []
        for chunk in [retry[i:i + batch] for i in range(0, len(retry), batch)]:
            try:
                c, v = _download(chunk, start)
                still += [t for t in chunk if t not in set(c.columns)]
                if len(c.columns):
                    closes.append(c); vols.append(v)
            except Exception as e:
                if verbose:
                    print(f"  retry batch FAILED ({type(e).__name__})")
                still += chunk
        missing = sorted(set(still))

    px = pd.concat(closes, axis=1).sort_index()
    vx = pd.concat(vols, axis=1).sort_index()
    px = px.loc[:, ~px.columns.duplicated()]
    vx = vx.loc[:, ~vx.columns.duplicated()]
    vx = vx.reindex(index=px.index, columns=px.columns)

    px, rep = clean(px)
    if verbose:
        print(f"clean: masked {rep['n_nonpos']} non-positive closes ({rep['n_nonpos_t']} tickers), "
              f"{rep['n_spike']} one-day bad prints ({rep['n_spike_t']} tickers); "
              f"flagged {len(rep['step_counts'])} tickers with unreversed >100% steps")

    # count rows before the thin-drop, so we can report why names went
    n_rows = px.notna().sum()
    thin = sorted(n_rows[n_rows < MIN_ROWS].index)
    px = px.drop(columns=thin)
    vx = vx.drop(columns=thin)
    px = px.dropna(how="all")
    vx = vx.reindex(index=px.index)
    px = px.ffill()                               # ffill closes only; volume gaps stay NaN

    steps = rep["step_counts"].reindex(px.columns).fillna(0).astype(int)
    meta = pd.DataFrame({
        "ticker": px.columns,
        "first_date": [px[c].first_valid_index() for c in px.columns],
        "last_date": [px[c].last_valid_index() for c in px.columns],
        "n_rows": [int(px[c].notna().sum()) for c in px.columns],
        "max_1d_move": rep["max_move"].reindex(px.columns).round(3).values,
        "n_steps": steps.values,
    }).set_index("ticker").sort_index()

    DATA.mkdir(exist_ok=True)
    p_px = _save(px.round(4), DATA / "prices_small.csv")
    p_vx = _save(vx, DATA / "volume_small.csv", float_format="%.0f")
    meta.to_csv(DATA / "small_meta.csv")
    _write_readme(px, len(tickers), thin, missing, meta, rep)

    if verbose:
        print(f"\nprices : {p_px.name}  {px.shape[0]} rows x {px.shape[1]} tickers  "
              f"{p_px.stat().st_size/1e6:.1f} MB")
        print(f"volume : {p_vx.name}  {vx.shape}  {p_vx.stat().st_size/1e6:.1f} MB")
        print(f"range  : {px.index[0].date()} .. {px.index[-1].date()}")
        print(f"dropped: {len(thin)} thin (<{MIN_ROWS} rows): {', '.join(thin) if thin else '-'}")
        print(f"missing: {len(missing)} no data after retry: {', '.join(missing) if missing else '-'}")
        full = int((meta.n_rows >= 0.98 * len(px)).sum())
        print(f"coverage: {full}/{len(meta)} tickers have >=98% of the {len(px)} rows; "
              f"median history {int(meta.n_rows.median())} rows "
              f"({meta.n_rows.median()/252:.1f}y); "
              f"{int((meta.first_date <= px.index[5]).sum())} present at 2010 start")
    return px, vx, meta


def _save(df: pd.DataFrame, path: Path, **kw) -> Path:
    """Write CSV; if it exceeds MAX_MB, write .csv.gz instead and drop the plain file."""
    df.to_csv(path, **kw)
    if path.stat().st_size > MAX_MB * 1e6:
        gz = path.with_suffix(".csv.gz")
        df.to_csv(gz, compression="gzip", **kw)
        path.unlink()
        return gz
    path.with_suffix(".csv.gz").unlink(missing_ok=True)   # stale gz from a previous build
    return path


def _write_readme(px, n_universe, thin, missing, meta, rep):
    worst = rep["max_move"].reindex(meta.index).sort_values(ascending=False)
    worst = worst[worst > 1.0]
    step_table = "\n".join(f"- `{t}` +{v:,.0%}" for t, v in worst.head(15).items()) or "- none"
    n_nonpos, n_nonpos_t = rep["n_nonpos"], rep["n_nonpos_t"]
    n_spike, n_spike_t = rep["n_spike"], rep["n_spike_t"]
    n_step_t = len(worst)
    (DATA / "SMALL_PANEL_README.md").write_text(f"""# Small-cap price panel — survivorship warning

Built {dt.date.today()} by `research/cache_small.py`.

Files: `prices_small.csv` (adjusted closes, 4dp), `volume_small.csv` (share volume),
`small_meta.csv` (ticker, first_date, last_date, n_rows, max_1d_move, n_steps).

Panel: {px.shape[1]} tickers x {px.shape[0]} trading days,
{px.index[0].date()} to {px.index[-1].date()}.
Source universe: `research/deepvalue/universe_under2b.csv` ({n_universe} tickers);
{len(thin)} dropped for <250 rows of history, {len(missing)} returned no data.

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

- **{n_nonpos} non-positive closes across {n_nonpos_t} tickers.** yfinance's back
  adjustment drives heavy distributors negative (VATE is negative for its whole
  pre-2020 history) and emits runs of literal zeros before a listing begins (DEC,
  732 zero bars in 2021-23). A price <= 0 is not a price.
- **{n_spike} isolated one-day bad prints across {n_spike_t} tickers** — a bar more
  than 60% from BOTH neighbours in the same direction (PROP 41 -> 2 -> 59 on
  2020-02-27; SPCB 144 -> 8 -> 144 on 2012-09-25).

## Data quality — FLAGGED, NOT repaired (you must decide)

{n_step_t} tickers contain a one-day move above +100% that **does not reverse** — a
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

{step_table}
""")


if __name__ == "__main__":
    build()

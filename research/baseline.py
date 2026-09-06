#!/usr/bin/env python3
"""RULES v1 as a vectorized weights function, plus a compare() helper used by every backtest.
Usage in a backtest script:
    import sys; sys.path.insert(0, "research")
    from baseline import load_universe, rules_v1_weights, compare
    px = load_universe()
    compare("my-idea", my_weights_fn, px)
"""
import json, sys
from pathlib import Path
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import load_prices, backtest, metrics, report  # noqa

EXCLUDE = {"BTC-USD", "ETH-USD"}

def _small_path(stem):
    """data/<stem>.csv, or the .csv.gz variant if the panel was large enough to be gzipped."""
    for p in (ROOT / "data" / f"{stem}.csv", ROOT / "data" / f"{stem}.csv.gz"):
        if p.exists(): return p
    raise FileNotFoundError(f"data/{stem}.csv[.gz] not found — run research/cache_small.py")

def _read_small(stem):
    return pd.read_csv(_small_path(stem), index_col=0, parse_dates=True).sort_index()

def load_volume(start="2010-01-01", small=False):
    """Daily share volume. small=True -> data/volume_small.csv (the sub-$2B panel)."""
    if not small: raise ValueError("load_volume currently only serves the small panel (small=True)")
    return _read_small("volume_small").loc[start:]

def load_universe(start="2008-01-01", exclude=EXCLUDE, broad=False, small=False, with_spy=True):
    """Daily adjusted closes.

    small=True returns the 485-name sub-$2B panel from data/prices_small.csv (offline,
    no network).  SURVIVORSHIP: current constituents of the screen only — see
    data/SMALL_PANEL_README.md.  with_spy joins a single benchmark column "SPY"
    from data/prices.csv (reindexed onto the small panel's trading days) because
    compare() needs it; the panel is otherwise pure small caps.
    """
    if small:
        px = _read_small("prices_small")
        if start: px = px.loc[start:]
        px = px.dropna(how="all").ffill()
        if with_spy:
            spy = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)["SPY"]
            spy = spy.reindex(px.index, method="ffill").rename("SPY")   # benchmark, NOT a constituent
            px = pd.concat([px.drop(columns=["SPY"], errors="ignore"), spy], axis=1)
        return px
    if broad:
        T = json.loads((ROOT / "research" / "universe_broad.json").read_text())
        cache = ROOT / "data" / "prices_broad.csv"
        try:
            px = load_prices(T, start=start)
        except Exception:
            px = pd.read_csv(cache, index_col=0, parse_dates=True)
        return px.dropna(how="all").ffill()
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    T = sorted({t for g in U.values() for t in g} - set(exclude))
    return load_prices(T, start=start)

def score(px, vol_scale=True):
    """Same composite as research/scan.py, computed for every day."""
    mom = px.shift(21) / px.shift(252) - 1; r6 = px / px.shift(126) - 1; r3 = px / px.shift(63) - 1
    comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    s = comp * (0.5 + 0.5 * above.astype(float))
    if vol_scale: s = s / vol20.clip(lower=0.08) ** 0.5
    return s, above, vol20

def rules_v1_weights(px, n=5, w=0.15, max_vol=0.60, vol_scale=True):
    s, above, vol20 = score(px, vol_scale)
    elig = s.where(above & (vol20 < max_vol))
    rank = elig.rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * w

def band_state(px, band=0.03):
    """RULES v2 clause 2: 200d MA band with hysteresis. IN above ma*(1+band), OUT below
    ma*(1-band), previous state in between, OUT before 200 closes exist."""
    ma = px.rolling(200).mean()
    raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
    raw = raw.mask(px > ma * (1 + band), 1.0).mask(px < ma * (1 - band), 0.0)
    return raw.ffill().fillna(0.0) > 0.5

def rules_v2_weights(px, band=0.03, gross=0.75):
    """RULES v2 (live since 2026-09-06): hold every name inside the 200d +/-3% band at
    gross/N of NAV, N = instruments priced that day; gated-out weight goes to CASH (de-gross,
    never re-spread). No ranking, no vol filter. Weekly cadence (freq='W')."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, band), 0.0)

def _row(name, r):
    m = metrics(r); h = len(r) // 2; m1, m2 = metrics(r.iloc[:h]), metrics(r.iloc[h:])
    return dict(name=name, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"], H2=m2["Sharpe"])

def compare(name, weights_fn, px, freq="W", cost_bps=10, baseline_freq="W", write_report=False):
    """Run idea vs the LIVE baseline (RULES v2 since 2026-09-06) vs RULES v1 vs SPY over the
    common sample; print table; return dict for the leaderboard. The 4a verdict is judged
    against RULES v2; the v1 row is kept for continuity with the pre-2026-09-06 record."""
    res = backtest(px, weights_fn(px), cost_bps=cost_bps, freq=freq)
    base = backtest(px, rules_v2_weights(px), cost_bps=cost_bps, freq=baseline_freq)
    old = backtest(px, rules_v1_weights(px), cost_bps=cost_bps, freq=baseline_freq)
    start = px.index[260]                                    # skip warm-up
    r, b, spy = res["returns"].loc[start:], base["returns"].loc[start:], px["SPY"].pct_change().fillna(0).loc[start:]
    rows = [_row(name, r), _row("RULES v2 baseline (live)", b), _row("RULES v1 (previous)", old["returns"].loc[start:]), _row("SPY", spy)]
    df = pd.DataFrame(rows).set_index("name")
    print(df.to_string(float_format=lambda x: f"{x:.3f}"))
    keep = rows[0]["H1"] > rows[1]["H1"] and rows[0]["H2"] > rows[1]["H2"] and rows[0]["MaxDD"] >= rows[1]["MaxDD"]
    verdict = "KEEP-candidate" if keep else "KILL"
    print("Verdict:", verdict)
    if write_report: report(name, {"returns": r, "equity": (1 + r).cumprod(), "turnover": res["turnover"].loc[start:]}, spy, ROOT / "research" / "backtests" / "reports")
    d = rows[0]; b0 = rows[1]
    line = f"| {pd.Timestamp.today().date()} | {name} | {d['CAGR']:.1%} | {d['Sharpe']:.2f} | {d['MaxDD']:.1%} | {d['H1']:.2f} / {d['H2']:.2f} | {b0['Sharpe']:.2f} ({b0['H1']:.2f}/{b0['H2']:.2f}) | {verdict} | {name} |"
    print("LEADERBOARD row:\n" + line)
    return dict(row=line, verdict=verdict, table=df)

if __name__ == "__main__":
    px = load_universe()
    compare("RULES v2 (self-check)", rules_v2_weights, px)

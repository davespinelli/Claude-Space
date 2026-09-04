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
def load_universe(start="2008-01-01", exclude=EXCLUDE):
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

def _row(name, r):
    m = metrics(r); h = len(r) // 2; m1, m2 = metrics(r.iloc[:h]), metrics(r.iloc[h:])
    return dict(name=name, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"], H2=m2["Sharpe"])

def compare(name, weights_fn, px, freq="W", cost_bps=10, baseline_freq="W", write_report=False):
    """Run idea vs RULES v1 baseline vs SPY over the common sample; print table; return dict for the leaderboard."""
    res = backtest(px, weights_fn(px), cost_bps=cost_bps, freq=freq)
    base = backtest(px, rules_v1_weights(px), cost_bps=cost_bps, freq=baseline_freq)
    start = px.index[260]                                    # skip warm-up
    r, b, spy = res["returns"].loc[start:], base["returns"].loc[start:], px["SPY"].pct_change().fillna(0).loc[start:]
    rows = [_row(name, r), _row("RULES v1 baseline", b), _row("SPY", spy)]
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
    compare("RULES v1 (self-check)", rules_v1_weights, px)

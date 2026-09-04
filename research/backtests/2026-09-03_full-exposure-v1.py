#!/usr/bin/env python3
"""Idea 20 — "full-exposure-v1": does the 75% gross cap explain RULES v1's CAGR gap to SPY?

RULES v1 holds the top 5 eligible names at 15% each = 75% gross, >=25% permanent cash.
Its CAGR is far below SPY's. This script decomposes that gap into three components:

  * exposure      — 75% -> 100% gross (5 names @ 20%)
  * market filter — an index-level 200d SPY trend gate on top of full exposure
  * per-name gate — the 200d MA eligibility filter that v1 applies to each candidate

Variants (all weekly rebalance, 10 bps, px = baseline.load_universe()):

  A  v1 selection, 5 names @ 20% each (100% gross). Only change vs baseline: position size.
  B  A + market filter: SPY below its 200d MA -> every weight halved (50% gross).
  C  A + market filter: SPY below its 200d MA -> fully to cash (0% gross).
  D  5 names @ 20% but WITHOUT the per-name 200d filter — pure momentum. The 200d MA is
     removed everywhere it appears in v1: both the eligibility gate (`above_200 == True`)
     and the score's 0.5+0.5*above tilt. The vol20 < 0.60 eligibility gate is kept, so the
     ONLY difference vs A is the 200d MA.
  D2 (diagnostic, not one of the four) — gate removed but the score tilt kept, to show how
     much of D's behaviour comes from the gate vs from the tilt.

No parameter is tuned inside any variant: n=5 and w=20% are fixed by the brief, the 200d
lookback is v1's own, and the halving factor in B is 1/2 by construction. The only free
choice is *which variant*, so the walk-forward (PROTOCOL rule 8) picks the variant with the
best 2009-2016 Sharpe and reports its untouched 2017-2026 out-of-sample result. OOS numbers
for all variants are printed too, for transparency.

Deterministic, standalone.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, score, rules_v1_weights, compare
from engine import backtest, metrics

COST_BPS = 10
FREQ = "W"
N = 5
W_FULL = 0.20          # 5 x 20% = 100% gross
MAX_VOL = 0.60         # v1 eligibility, unchanged
MA = 200               # v1's own trend lookback, unchanged
IS_END = "2016-12-31"  # walk-forward: parameters/variant chosen on 2009-2016 only
OOS_START = "2017-01-01"
SCRIPT = Path(__file__).name


# ---------------------------------------------------------------- weight functions
def spy_above_200(px):
    """SPY vs its own 200d MA, using the close at t only (engine applies weights at t+1)."""
    spy = px["SPY"]
    return spy > spy.rolling(MA).mean()


def variant_A(px):
    """v1 selection, 100% gross."""
    return rules_v1_weights(px, n=N, w=W_FULL, max_vol=MAX_VOL)


def _market_scaled(px, off_scale):
    w = variant_A(px)
    scale = spy_above_200(px).map({True: 1.0, False: off_scale}).astype(float)
    return w.mul(scale, axis=0)


def variant_B(px):
    """A + SPY below 200d MA -> half weights (50% gross)."""
    return _market_scaled(px, 0.5)


def variant_C(px):
    """A + SPY below 200d MA -> fully to cash."""
    return _market_scaled(px, 0.0)


def variant_D(px):
    """A but with the 200d MA removed entirely: pure (vol-scaled) momentum, vol20 gate kept."""
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    s = comp / vol20.clip(lower=0.08) ** 0.5          # baseline.score minus the (0.5+0.5*above) tilt
    elig = s.where(vol20 < MAX_VOL)
    rank = elig.rank(axis=1, ascending=False)
    return (rank <= N).astype(float) * W_FULL


def variant_D2(px):
    """Diagnostic: eligibility gate dropped but the score's above-200d tilt kept."""
    s, above, vol20 = score(px)
    elig = s.where(vol20 < MAX_VOL)
    rank = elig.rank(axis=1, ascending=False)
    return (rank <= N).astype(float) * W_FULL


VARIANTS = [
    ("A full-exposure 100% gross", variant_A),
    ("B full-exposure + SPY-200d half", variant_B),
    ("C full-exposure + SPY-200d cash", variant_C),
    ("D full-exposure no per-name 200d", variant_D),
    ("D2 no 200d gate, tilt kept (diagnostic)", variant_D2),
]
HEADLINE = [v[0] for v in VARIANTS[:4]]   # the four variants the walk-forward chooses among


# ---------------------------------------------------------------- helpers
def period(r, lo=None, hi=None):
    return r.loc[lo:hi]


def m_row(name, r):
    m = metrics(r)
    return dict(name=name, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], Years=m["Years"])


def fmt_pct(x):
    return f"{x:.1%}"


def main():
    px = load_universe()
    start = px.index[260]                     # same warm-up skip compare() uses
    print(f"Universe: {px.shape[1]} tickers, {px.index[0].date()} -> {px.index[-1].date()}")
    print(f"Eval sample starts {start.date()}  |  IS <= {IS_END}, OOS >= {OOS_START}")
    sa = spy_above_200(px).loc[start:]
    print(f"SPY below its 200d MA on {(~sa).mean():.1%} of days in the eval sample\n")

    # ---- full-sample leaderboard rows via the standard compare()
    rets = {}
    rows = []
    for name, fn in VARIANTS:
        print("=" * 86)
        print(f"### {name}")
        out = compare(name, fn, px, freq=FREQ, cost_bps=COST_BPS)
        # compare() puts the idea name in the last column; PROTOCOL wants the script filename
        rows.append(out["row"].rsplit("|", 2)[0] + f"| {SCRIPT} |")
        res = backtest(px, fn(px), cost_bps=COST_BPS, freq=FREQ)
        rets[name] = res["returns"].loc[start:]
        w = fn(px).loc[start:]
        print(f"Avg gross exposure: {w.sum(axis=1).mean():.1%}  "
              f"(turnover {res['turnover'].loc[start:].sum()/metrics(rets[name])['Years']:.1f}x/yr)")
        print()

    base = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    rets["RULES v1 baseline"] = base
    rets["SPY"] = spy
    bw = rules_v1_weights(px).loc[start:]
    print(f"Baseline avg gross exposure: {bw.sum(axis=1).mean():.1%}\n")

    print("=" * 86)
    print("LEADERBOARD rows (full sample)")
    for r in rows:
        print(r)
    print()

    # ---- walk-forward (PROTOCOL rule 8)
    order = HEADLINE + ["D2 no 200d gate, tilt kept (diagnostic)", "RULES v1 baseline", "SPY"]
    tbl = []
    for name in order:
        r = rets[name]
        ins, oos = period(r, None, IS_END), period(r, OOS_START, None)
        mi, mo = metrics(ins), metrics(oos)
        tbl.append(dict(name=name,
                        IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"]))
    wf = pd.DataFrame(tbl).set_index("name")
    print("Walk-forward: IS 2009-2016 (selection) | OOS 2017-2026 (untouched)")
    print(wf.to_string(float_format=lambda x: f"{x:.3f}"))

    pick = max(HEADLINE, key=lambda n: metrics(period(rets[n], None, IS_END))["Sharpe"])
    print(f"\nVariant chosen on IS Sharpe alone: {pick}")
    for n in (pick, "RULES v1 baseline", "SPY"):
        mo = metrics(period(rets[n], OOS_START, None))
        print(f"  OOS {n:42s} CAGR {mo['CAGR']:7.1%}  Sharpe {mo['Sharpe']:5.2f}  MaxDD {mo['MaxDD']:7.1%}")

    # ---- decomposition of the CAGR gap to SPY (full sample)
    print("\nCAGR decomposition (full eval sample):")
    for n in ["RULES v1 baseline"] + HEADLINE + ["SPY"]:
        m = metrics(rets[n])
        print(f"  {n:42s} CAGR {m['CAGR']:7.1%}  Sharpe {m['Sharpe']:5.2f}  MaxDD {m['MaxDD']:7.1%}")
    gap = metrics(spy)["CAGR"] - metrics(base)["CAGR"]
    closed = metrics(rets[HEADLINE[0]])["CAGR"] - metrics(base)["CAGR"]
    print(f"  Baseline->SPY CAGR gap: {gap:.1%}; sizing 15%->20% closes {closed:.1%} "
          f"({closed/gap:.0%} of the gap)")


if __name__ == "__main__":
    main()

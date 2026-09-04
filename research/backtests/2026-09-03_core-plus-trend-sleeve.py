#!/usr/bin/env python3
"""Idea 24 — "core-plus-trend-sleeve": a passive equity core (trend-gated) blended with the
macro-trend-ensemble variant-B defensive sleeve, aiming for SPY-like CAGR at roughly half the
drawdown.

Motivation
----------
Idea 18 (research/backtests/2026-09-03_macro-trend-ensemble.py) produced a KEEP-candidate
defensive sleeve — variant B, 9 macro ETFs, 3 momentum-sign votes, inverse-60d-vol risk parity —
with Sharpe 0.87 and MaxDD -10.1%, but a CAGR of only 5.0% vs SPY's 15.2%. Its own memo (line 10)
asked for exactly this follow-up: "a blended book ... to see whether the diversification survives
being mixed rather than compared." This script does that with a beta core rather than RULES v1.

Sleeve weights are the *faithful* variant-B function copied from that script (same MACRO list,
MOM_LAGS, VOL_WINDOW), scaled by the sleeve fraction.

Variants (all weekly, 10 bps, long-only, no leverage, px = baseline.load_universe())
-----------------------------------------------------------------------------------
  A  60% SPY when SPY > its own 200d MA else cash, + 0.40 x sleeve-B
  B  60% QQQ when QQQ > its own 200d MA else cash, + 0.40 x sleeve-B
  C  50% SPY when SPY > its own 200d MA else cash, + 0.50 x sleeve-B
  D  60% SPY always (NO 200d filter),              + 0.40 x sleeve-B

D exists only to isolate what the 200d filter contributes; A vs D is the clean read.
In B the filter is on the core asset itself (QQQ > QQQ's 200d MA), which is the literal
"same construction with QQQ as the core". SPY appears in both the core and the sleeve, so the
two books are ADDED, never overwritten (max combined SPY weight in A = 60% + 0.4x its sleeve
weight, still well under 100% gross).

Tuned-parameter count (PROTOCOL rule 4): core fraction (60/40, one number) and the 200d MA
window. The sleeve's own lookbacks (12-1/6m/3m, 60d vol) are canonical TSMOM values carried over
unchanged from idea 18, and 200d is the same window RULES v1 already uses. So: 2 parameters.

No look-ahead: every input at date t uses data through t only; engine.backtest applies the row
decided at t to the t+1 close. Deterministic, standalone.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, rules_v1_weights, compare
from engine import backtest, metrics

COST_BPS = 10
FREQ = "W"
SPLIT = "2017-01-01"
IS_END = "2016-12-31"

# ---------------------------------------------------------------- sleeve (idea 18, variant B)
MACRO = ["SPY", "QQQ", "IWM", "EFA", "EEM", "TLT", "GLD", "DBC", "UUP"]
MOM_LAGS = (252, 126, 63)      # 12-1 (with 21d skip), 6m, 3m
VOL_WINDOW = 60
MA_WINDOW = 200                # core trend filter


def _risk_parity(sub: pd.DataFrame) -> pd.DataFrame:
    """Inverse trailing-60d-vol weights over the 9 macro assets, rows normalized to 1.0."""
    vol = sub.pct_change().rolling(VOL_WINDOW).std()
    inv = 1.0 / vol.replace(0.0, np.nan)
    return inv.div(inv.sum(axis=1), axis=0)


def _vote_mom(sub: pd.DataFrame) -> pd.DataFrame:
    """Variant B vote: fraction of {12-1 mom, 6m ret, 3m ret} that are positive."""
    signals = [sub.shift(21) / sub.shift(MOM_LAGS[0]) - 1,   # 12-1 momentum
               sub / sub.shift(MOM_LAGS[1]) - 1,             # 6m
               sub / sub.shift(MOM_LAGS[2]) - 1]             # 3m
    votes = [(s > 0).astype(float).where(s.notna()) for s in signals]
    return sum(votes) / len(votes)


def sleeve_b_weights(px: pd.DataFrame) -> pd.DataFrame:
    """macro-trend-ensemble variant B, full size (gross <= 100%), zero outside the 9 macro ETFs."""
    sub = px[MACRO]
    w = (_vote_mom(sub) * _risk_parity(sub)).fillna(0.0)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[MACRO] = w
    return out


# ---------------------------------------------------------------- core + blend
def core_weights(px: pd.DataFrame, ticker: str, frac: float, use_filter: bool) -> pd.DataFrame:
    """`frac` in `ticker` when it is above its own 200d MA (or always, if use_filter=False)."""
    p = px[ticker]
    if use_filter:
        ma = p.rolling(MA_WINDOW).mean()
        on = (p > ma).astype(float).where(ma.notna(), 0.0)
    else:
        on = pd.Series(1.0, index=px.index)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[ticker] = frac * on
    return out


def blend(ticker: str, core_frac: float, use_filter: bool):
    sleeve_frac = 1.0 - core_frac

    def _fn(px: pd.DataFrame) -> pd.DataFrame:
        return core_weights(px, ticker, core_frac, use_filter) + sleeve_frac * sleeve_b_weights(px)

    return _fn


VARIANTS = {
    "core-plus-sleeve A (60% SPY>200d + 40% sleeve)":  blend("SPY", 0.60, True),
    "core-plus-sleeve B (60% QQQ>200d + 40% sleeve)":  blend("QQQ", 0.60, True),
    "core-plus-sleeve C (50% SPY>200d + 50% sleeve)":  blend("SPY", 0.50, True),
    "core-plus-sleeve D (60% SPY no filter + 40% sleeve)": blend("SPY", 0.60, False),
}


# ---------------------------------------------------------------- reporting helpers
def period_row(label, r):
    m = metrics(r)
    return dict(period=label, start=str(r.index[0].date()), end=str(r.index[-1].date()),
                CAGR=m["CAGR"], Vol=m["Vol"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"])


def half_rows(name, r):
    m = metrics(r)
    h = len(r) // 2
    m1, m2 = metrics(r.iloc[:h]), metrics(r.iloc[h:])
    return dict(strategy=name, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1_Sharpe=m1["Sharpe"], H2_Sharpe=m2["Sharpe"],
                H1_MaxDD=m1["MaxDD"], H2_MaxDD=m2["MaxDD"])


def main():
    px = load_universe()
    missing = [t for t in MACRO if t not in px.columns]
    if missing:
        raise SystemExit(f"missing tickers in universe panel: {missing}")
    start = px.index[260]
    print(f"Price panel: {px.shape[1]} tickers, {px.index[0].date()} -> {px.index[-1].date()}")
    print(f"Sleeve (idea 18 variant B): {MACRO}")
    print(f"Eval sample starts {start.date()} (260-day warm-up skipped by compare())\n")

    series, weights, turnovers = {}, {}, {}
    for name, wfn in VARIANTS.items():
        print("=" * 100)
        print(f"### {name}")
        compare(name, wfn, px, freq=FREQ, cost_bps=COST_BPS)
        w = wfn(px)
        res = backtest(px, w, cost_bps=COST_BPS, freq=FREQ)
        series[name] = res["returns"].loc[start:]
        weights[name] = w.loc[start:]
        turnovers[name] = res["turnover"].loc[start:]
        g = weights[name].sum(axis=1)
        print(f"Avg gross exposure: {g.mean():.1%}  (min {g.min():.1%}, median {g.median():.1%}, "
              f"max {g.max():.1%})")
        print(f"Annual turnover: {turnovers[name].sum() / (len(series[name]) / 252):.1f}x\n")

    base = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
    series["RULES v1 baseline"] = base
    series["SPY"] = px["SPY"].pct_change().fillna(0).loc[start:]
    # reference: the standalone sleeve at full size, for context
    series["sleeve B standalone (100%)"] = backtest(
        px, sleeve_b_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]

    print("=" * 100)
    print("### Full sample + compare()-style halves (PROTOCOL rule 4)\n")
    print(pd.DataFrame([half_rows(n, r) for n, r in series.items()]).set_index("strategy")
          .to_string(float_format=lambda x: f"{x:.3f}"))

    print("\n" + "=" * 100)
    print("### Walk-forward (PROTOCOL rule 8): in-sample 2009-2016 / OOS 2017-2026\n")
    rows = []
    for name, r in series.items():
        for label, seg in (("2009-2016", r.loc[:IS_END]), ("2017-2026", r.loc[SPLIT:])):
            rows.append(dict(strategy=name, **period_row(label, seg)))
    wf = pd.DataFrame(rows).set_index(["strategy", "period"])
    print(wf.to_string(float_format=lambda x: f"{x:.3f}"))

    is_sharpe = {n: metrics(series[n].loc[:IS_END])["Sharpe"] for n in VARIANTS}
    pick = max(is_sharpe, key=is_sharpe.get)
    print("\nIn-sample (2009-2016) Sharpe by variant: "
          + ", ".join(f"{n.split()[1]}={v:.3f}" for n, v in is_sharpe.items()))
    print(f"Rule-8 selection (highest 2009-2016 Sharpe): {pick}")
    oos = metrics(series[pick].loc[SPLIT:])
    bo = metrics(series["RULES v1 baseline"].loc[SPLIT:])
    so = metrics(series["SPY"].loc[SPLIT:])
    print(f"  OOS 2017-2026 {pick}: CAGR {oos['CAGR']:.2%}, Sharpe {oos['Sharpe']:.3f}, "
          f"MaxDD {oos['MaxDD']:.2%}")
    print(f"  OOS 2017-2026 baseline:  CAGR {bo['CAGR']:.2%}, Sharpe {bo['Sharpe']:.3f}, "
          f"MaxDD {bo['MaxDD']:.2%}")
    print(f"  OOS 2017-2026 SPY:       CAGR {so['CAGR']:.2%}, Sharpe {so['Sharpe']:.3f}, "
          f"MaxDD {so['MaxDD']:.2%}")

    print("\n" + "=" * 100)
    print("### Calendar-year returns (all years; 2020 and 2022 are the stress tests)\n")
    yr = pd.DataFrame({n: r.groupby(r.index.year).apply(lambda x: (1 + x).prod() - 1)
                       for n, r in series.items()})
    print(yr.to_string(float_format=lambda x: f"{x:+.2%}"))
    print("\nStress years only:")
    print(yr.loc[[2020, 2022]].T.to_string(float_format=lambda x: f"{x:+.2%}"))

    print("\n" + "=" * 100)
    print("### Average gross exposure\n")
    grows = []
    for name in VARIANTS:
        g = weights[name].sum(axis=1)
        c = weights[name][["SPY", "QQQ"]].sum(axis=1)
        grows.append(dict(strategy=name, full=g.mean(), IS_2009_2016=g.loc[:IS_END].mean(),
                          OOS_2017_2026=g.loc[SPLIT:].mean(), min=g.min(), max=g.max(),
                          SPY_plus_QQQ=c.mean()))
    gb = rules_v1_weights(px).loc[start:].sum(axis=1)
    grows.append(dict(strategy="RULES v1 baseline", full=gb.mean(),
                      IS_2009_2016=gb.loc[:IS_END].mean(), OOS_2017_2026=gb.loc[SPLIT:].mean(),
                      min=gb.min(), max=gb.max(), SPY_plus_QQQ=np.nan))
    gs = sleeve_b_weights(px).loc[start:].sum(axis=1)
    grows.append(dict(strategy="sleeve B standalone (100%)", full=gs.mean(),
                      IS_2009_2016=gs.loc[:IS_END].mean(), OOS_2017_2026=gs.loc[SPLIT:].mean(),
                      min=gs.min(), max=gs.max(), SPY_plus_QQQ=np.nan))
    print(pd.DataFrame(grows).set_index("strategy").to_string(float_format=lambda x: f"{x:.1%}"))

    print("\nCorrelation of daily returns:")
    print(pd.DataFrame(series).corr().to_string(float_format=lambda x: f"{x:.3f}"))

    print("\nDays the core filter was OFF (cash core), % of eval sample:")
    for name, wfn in VARIANTS.items():
        tick = "QQQ" if "QQQ" in name else "SPY"
        frac = 0.50 if " C " in f" {name} " or "50%" in name else 0.60
        core_only = core_weights(px, tick, frac, "no filter" not in name).loc[start:][tick]
        print(f"  {name}: {(core_only == 0).mean():.1%}")

    print("\nGrowth of $1 over the eval sample:")
    for n, r in series.items():
        print(f"  {n}: ${(1 + r).prod():.2f}")


if __name__ == "__main__":
    main()

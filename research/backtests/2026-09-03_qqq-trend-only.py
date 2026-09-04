#!/usr/bin/env python3
"""Idea 27 — "qqq-trend-only": the simplest growth-plus-trend benchmark the book must beat.

The point of this script is NOT to find an edge. It is to erect a floor. If a one-line rule
("hold QQQ while it is above its 200-day moving average, otherwise hold T-bills") beats the
live RULES v1 book, then every more complicated idea in research/backtests has to clear that
floor before it deserves attention.

Variants (all long-only, no leverage, 10 bps per unit turnover, price panel = baseline.load_universe())
  A  100% QQQ when QQQ > 200d MA, else 100% SHY.                         Checked weekly (freq="W").
  B  As A, but risk-on also requires QQQ 12-1 momentum > 0
     (px.shift(21)/px.shift(252) - 1 > 0). Both conditions must hold.     Checked weekly (freq="W").
  C  As A, but the risk-on leg is a 50/50 QQQ/SPY core instead of 100% QQQ. Checked weekly (freq="W").
  D  As A, checked MONTHLY (freq="M") instead of weekly — the whipsaw-cost measurement.

Tuned-parameter count (PROTOCOL rule 4 allows <= 2):
  A: 1 (the 200-day MA window).   B: 2 (200d MA + the 12-1 momentum lookback).
  C: 2 (200d MA + the 50/50 split). D: 1 (200d MA; the monthly check frequency is the thing
  being measured, not fitted).
All of these are the textbook values (Faber 2007 / Jegadeesh-Titman 12-1), not values searched
on this data.

No look-ahead: the signal at date t uses closes through t only, and engine.backtest shifts the
weight row by one day before applying it, so the trade happens at the t+1 close.

Rule 8 walk-forward: the variant with the best 2009-2016 Sharpe is SELECTED on that window only,
and its 2017-2026 out-of-sample leg is then reported untouched, alongside the OOS leg of all four
variants, the RULES v1 baseline, SPY and QQQ buy-and-hold.

Honesty control demanded by the task: QQQ's 2009-2026 run is historically exceptional. QQQ
buy-and-hold is therefore reported everywhere the variants are, so the memo can separate
"QQQ beat SPY" from "the trend filter helped".

Deterministic, standalone.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, rules_v1_weights, compare
from engine import backtest, metrics, rebalance_mask

COST_BPS = 10
MA_WINDOW = 200
MOM_LONG = 252          # 12-1 momentum: 12 months back ...
MOM_SKIP = 21           # ... skipping the most recent month
SPLIT = "2017-01-01"
IS_END = "2016-12-31"
CAL_YEARS = [2018, 2020, 2022]


# ----------------------------------------------------------------------------- signals
def _above_ma(px):
    ma = px["QQQ"].rolling(MA_WINDOW).mean()
    return (px["QQQ"] > ma) & ma.notna()


def _mom_positive(px):
    mom = px["QQQ"].shift(MOM_SKIP) / px["QQQ"].shift(MOM_LONG) - 1
    return (mom > 0) & mom.notna()


def _signal(px, variant):
    if variant == "B":
        return _above_ma(px) & _mom_positive(px)
    return _above_ma(px)


def _weights(px, variant):
    """Target weights: risk-on leg when the signal is True, 100% SHY otherwise."""
    on = _signal(px, variant)
    w = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    if variant == "C":
        w["QQQ"] = np.where(on, 0.5, 0.0)
        w["SPY"] = np.where(on, 0.5, 0.0)
    else:
        w["QQQ"] = np.where(on, 1.0, 0.0)
    w["SHY"] = np.where(on, 0.0, 1.0)
    return w


VARIANTS = {
    "qqq-trend-only A (QQQ/SHY, 200d, weekly)":        dict(variant="A", freq="W"),
    "qqq-trend-only B (A + 12-1 mom>0, weekly)":       dict(variant="B", freq="W"),
    "qqq-trend-only C (50/50 QQQ+SPY core, weekly)":   dict(variant="C", freq="W"),
    "qqq-trend-only D (QQQ/SHY, 200d, monthly)":       dict(variant="D", freq="M"),
}


def weights_fn(variant):
    return lambda px: _weights(px, variant)


# ----------------------------------------------------------------------------- reporting helpers
def period_row(label, r):
    m = metrics(r)
    return dict(period=label, start=str(r.index[0].date()), end=str(r.index[-1].date()),
                CAGR=m["CAGR"], Vol=m["Vol"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"])


def half_rows(name, r):
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    return dict(name=name, CAGR=m["CAGR"], Vol=m["Vol"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=m1["Sharpe"], H2=m2["Sharpe"], H1DD=m1["MaxDD"], H2DD=m2["MaxDD"])


def round_trips(px, variant, freq, start):
    """A round trip = one exit from the risk-on leg plus the following re-entry.

    Counted on the state actually traded: the signal sampled on the engine's rebalance dates
    (shifted one day, matching how backtest() applies weights). Two state flips = one round trip.
    """
    on = _signal(px, variant)
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False)
    state = on.where(mask).ffill().loc[start:].dropna().astype(bool)
    flips = state.ne(state.shift()).fillna(False)
    flips.iloc[0] = False
    per_year = flips.groupby(flips.index.year).sum()
    return flips, per_year


def cal_years(series_map):
    out = {}
    for name, r in series_map.items():
        out[name] = r.groupby(r.index.year).apply(lambda x: (1 + x).prod() - 1)
    return pd.DataFrame(out)


# ----------------------------------------------------------------------------- main
def main():
    px = load_universe()
    for t in ("QQQ", "SPY", "SHY"):
        if t not in px.columns:
            raise SystemExit(f"missing ticker in universe panel: {t}")
    start = px.index[260]
    print(f"Price panel: {px.shape[1]} tickers, {px.index[0].date()} -> {px.index[-1].date()}")
    print(f"Eval sample starts {start.date()} (260-day warm-up skipped by compare())")
    print(f"Legs used: QQQ, SPY, SHY. Everything else in the panel gets weight 0.\n")

    series, leaderboard, exposure = {}, [], {}
    for name, cfg in VARIANTS.items():
        print("=" * 100)
        print(f"### {name}")
        wfn = weights_fn(cfg["variant"])
        out = compare(name, wfn, px, freq=cfg["freq"], cost_bps=COST_BPS)
        # compare() puts the idea name in the last column; PROTOCOL wants the script filename.
        parts = out["row"].rstrip().rstrip("|").split("|")
        parts[-1] = f" research/backtests/{Path(__file__).name} "
        leaderboard.append("|".join(parts) + "|")
        res = backtest(px, wfn(px), cost_bps=COST_BPS, freq=cfg["freq"])
        r = res["returns"].loc[start:]
        series[name] = r
        on = _signal(px, cfg["variant"]).loc[start:]
        flips, per_year = round_trips(px, cfg["variant"], cfg["freq"], start)
        yrs = len(r) / 252
        exposure[name] = dict(pct_risk_on=on.mean(), flips=int(flips.sum()),
                              round_trips_per_year=flips.sum() / 2 / yrs,
                              turnover=res["turnover"].loc[start:].sum() / yrs,
                              per_year=per_year)
        print(f"Time in the risk-on leg: {on.mean():.1%} of days")
        print(f"State flips: {int(flips.sum())} over {yrs:.1f}y  =>  "
              f"{flips.sum() / 2 / yrs:.2f} round-trips/yr")
        print(f"Annual turnover: {res['turnover'].loc[start:].sum() / yrs:.2f}x\n")

    base = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS, freq="W")["returns"].loc[start:]
    series["RULES v1 baseline (live)"] = base
    series["SPY buy-and-hold"] = px["SPY"].pct_change().fillna(0).loc[start:]
    series["QQQ buy-and-hold"] = px["QQQ"].pct_change().fillna(0).loc[start:]

    # ---- full sample + halves
    print("=" * 100)
    print("### Full sample + compare()-style halves (equal row counts)\n")
    tbl = pd.DataFrame([half_rows(n, r) for n, r in series.items()]).set_index("name")
    print(tbl.to_string(float_format=lambda x: f"{x:.3f}"))

    # ---- calendar splits
    print("\n" + "=" * 100)
    print("### Calendar halves: 2009-2016 (in-sample window for rule 8) vs 2017-2026 (OOS)\n")
    rows = []
    for name, r in series.items():
        for label, seg in (("2009-2016", r.loc[:IS_END]), ("2017-2026", r.loc[SPLIT:])):
            rows.append(dict(strategy=name, **period_row(label, seg)))
    per = pd.DataFrame(rows).set_index(["strategy", "period"])
    print(per.to_string(float_format=lambda x: f"{x:.3f}"))

    # ---- calendar years
    print("\n" + "=" * 100)
    print("### Calendar-year returns (2018 / 2020 / 2022 highlighted; all years shown)\n")
    cy = cal_years(series)
    print(cy.to_string(float_format=lambda x: f"{x:+.1%}"))
    print("\nRequested years only:")
    print(cy.loc[[y for y in CAL_YEARS if y in cy.index]].to_string(float_format=lambda x: f"{x:+.1%}"))

    # ---- round trips per year
    print("\n" + "=" * 100)
    print("### Round-trips per year (state flips / 2; a flip = risk-on <-> risk-off at a rebalance)\n")
    rt = pd.DataFrame({n: e["per_year"] / 2 for n, e in exposure.items()}).fillna(0.0)
    print(rt.to_string(float_format=lambda x: f"{x:.1f}"))
    print("\nSummary:")
    for n, e in exposure.items():
        print(f"  {n}: {e['round_trips_per_year']:.2f} round-trips/yr, "
              f"{e['pct_risk_on']:.1%} of days risk-on, turnover {e['turnover']:.2f}x/yr")

    # ---- rule 8 walk-forward
    print("\n" + "=" * 100)
    print("### PROTOCOL rule 8 walk-forward: select on 2009-2016 Sharpe, evaluate 2017-2026\n")
    is_sharpe = {n: metrics(series[n].loc[:IS_END])["Sharpe"] for n in VARIANTS}
    for n, s in sorted(is_sharpe.items(), key=lambda kv: -kv[1]):
        print(f"  IS 2009-2016 Sharpe  {s:6.3f}  {n}")
    picked = max(is_sharpe, key=is_sharpe.get)
    print(f"\nSELECTED on 2009-2016 Sharpe: {picked}")

    oos_rows = []
    for name, r in series.items():
        seg = r.loc[SPLIT:]
        m = metrics(seg)
        oos_rows.append(dict(strategy=name, selected=(name == picked),
                             CAGR=m["CAGR"], Vol=m["Vol"], Sharpe=m["Sharpe"],
                             MaxDD=m["MaxDD"], Sortino=m["Sortino"], Total=m["Total"]))
    oos = pd.DataFrame(oos_rows).set_index("strategy")
    print("\nOut-of-sample 2017-2026:")
    print(oos.to_string(float_format=lambda x: f"{x:.3f}"))

    b_oos = metrics(base.loc[SPLIT:])
    p_oos = metrics(series[picked].loc[SPLIT:])
    print(f"\nSelected variant OOS Sharpe {p_oos['Sharpe']:.3f} vs baseline OOS {b_oos['Sharpe']:.3f}; "
          f"MaxDD {p_oos['MaxDD']:.1%} vs {b_oos['MaxDD']:.1%}")

    # ---- QQQ-vs-SPY attribution
    print("\n" + "=" * 100)
    print("### Attribution: how much is 'QQQ beat SPY' vs 'the trend filter helped'?\n")
    qqq, spy = series["QQQ buy-and-hold"], series["SPY buy-and-hold"]
    a = series["qqq-trend-only A (QQQ/SHY, 200d, weekly)"]
    mq, ms, ma_ = metrics(qqq), metrics(spy), metrics(a)
    print(f"  SPY buy-and-hold : CAGR {ms['CAGR']:.2%}  Sharpe {ms['Sharpe']:.3f}  MaxDD {ms['MaxDD']:.1%}")
    print(f"  QQQ buy-and-hold : CAGR {mq['CAGR']:.2%}  Sharpe {mq['Sharpe']:.3f}  MaxDD {mq['MaxDD']:.1%}")
    print(f"  A (QQQ + trend)  : CAGR {ma_['CAGR']:.2%}  Sharpe {ma_['Sharpe']:.3f}  MaxDD {ma_['MaxDD']:.1%}")
    print(f"  step 1, asset choice (QQQ - SPY)  : CAGR {mq['CAGR'] - ms['CAGR']:+.2%}  "
          f"Sharpe {mq['Sharpe'] - ms['Sharpe']:+.3f}  MaxDD {mq['MaxDD'] - ms['MaxDD']:+.1%}")
    print(f"  step 2, trend filter (A - QQQ)    : CAGR {ma_['CAGR'] - mq['CAGR']:+.2%}  "
          f"Sharpe {ma_['Sharpe'] - mq['Sharpe']:+.3f}  MaxDD {ma_['MaxDD'] - mq['MaxDD']:+.1%}")
    print("\n  Same decomposition on the OOS leg 2017-2026:")
    mq2, ms2, ma2 = metrics(qqq.loc[SPLIT:]), metrics(spy.loc[SPLIT:]), metrics(a.loc[SPLIT:])
    print(f"  step 1, asset choice (QQQ - SPY)  : CAGR {mq2['CAGR'] - ms2['CAGR']:+.2%}  "
          f"Sharpe {mq2['Sharpe'] - ms2['Sharpe']:+.3f}")
    print(f"  step 2, trend filter (A - QQQ)    : CAGR {ma2['CAGR'] - mq2['CAGR']:+.2%}  "
          f"Sharpe {ma2['Sharpe'] - mq2['Sharpe']:+.3f}")

    print("\n  Correlation of daily returns:")
    corr = pd.DataFrame(series).corr()
    print(corr.to_string(float_format=lambda x: f"{x:.3f}"))

    print("\n" + "=" * 100)
    print("### LEADERBOARD rows\n")
    for line in leaderboard:
        print(line)


if __name__ == "__main__":
    main()

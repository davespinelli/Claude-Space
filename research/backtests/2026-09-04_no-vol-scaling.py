#!/usr/bin/env python3
"""Idea 1 - "no-vol-scaling": does dividing the RULES v1 composite by sqrt(vol20) help,
or does it just tilt the book toward low-vol ETFs and cancel the momentum signal?

RULES v1 ranks eligible names (above 200d MA, vol20 < 0.60) by

    score = mean(pct-rank 12-1, pct-rank 6m, pct-rank 3m) * (0.5 + 0.5*above200d) / sqrt(vol20)

and buys the top 5 at 15% each.  Idea 25 (2026-09-03) showed the traded score has rank IC
t = 0.4 while the SAME composite BEFORE the division has t = 4.2, and the scaler alone has
t = -5.7 - i.e. the division cancels the signal.  That was a diagnostic on one configuration
(n=5, 75% gross).  This script tests the trading consequence properly, over a grid, with a
walk-forward, and against both PROTOCOL KEEP paths.

Design
------
One binary treatment - the idea itself:
    ON   score / sqrt(vol20)   (RULES v1 as live)
    OFF  score, no division    (the idea)
crossed with at most TWO tuned parameters (PROTOCOL rule 4):
    n     positions held      in {3, 5, 8}
    gross book exposure       in {75%, 100%}   (per-name weight = gross / n)
=> 12 grid points.  ALL of them are reported, full sample, both halves, and OOS.  Nothing
else is tuned: the 200d gate, vol20 < 0.60, the 21/63/126/252-day lookbacks and the weekly
rebalance are RULES v1's own.  ON at n=5, gross 75% IS the live baseline and must reproduce
its numbers exactly.

Walk-forward (PROTOCOL rule 8)
------------------------------
Parameters are chosen on 2009-2016 ONLY and the choice is then evaluated untouched on
2017-2026.  Pre-stated selection rule, fixed before looking at any OOS number: within each
arm (ON / OFF) pick the (n, gross) with the highest in-sample Sharpe; ties break to smaller n
then smaller gross.  The OOS column of every one of the 12 points is printed too, so the
selection rule can be audited rather than trusted.

Verdicts
--------
4a (beat the book): Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than RULES v1.
4b (capital-worthy): Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
    CAGR >= 70% of SPY's.
Both are evaluated for every grid point and for the walk-forward selection.

DATA BUG FOUND WHILE RUNNING THIS (read before trusting any cloud-run backtest)
-------------------------------------------------------------------------------
`data/prices.csv` is indexed on CALENDAR days from 2014-09-17 onward - the day BTC-USD's
history starts.  yfinance returned a 7-day index because the crypto tickers trade on
weekends; every equity was forward-filled across Saturday and Sunday.  `load_universe()`
drops the crypto COLUMNS but keeps those ROWS, so from Sep-2014 on ~30% of daily "returns"
in the cache are exactly zero and each year has 365 rows instead of ~252.

`engine.metrics()` annualizes with `len(r)/252` years and `std * sqrt(252)`.  On a 365-row
year that understates CAGR and Sharpe, and it does so ONLY in the second half of the sample,
so it also corrupts the H1/H2 robustness test that PROTOCOL rule 4 depends on.  Measured on
RULES v1 over the same sample:

    raw cache index  : v1 CAGR 4.65%, Sharpe 0.555, H1 0.659 / H2 0.452 | SPY CAGR 11.48%, Sharpe 0.779
    trading-day index: v1 CAGR 6.48%, Sharpe 0.666, H1 0.641 / H2 0.692 | SPY CAGR 15.26%, Sharpe 0.890

The trading-day figures reproduce the Sep-3 leaderboard's baseline row (6.4% / 0.66 / -13.8%,
halves 0.65/0.68) exactly, which confirms the Sep-3 rows were run locally against live
yfinance (a trading-day index) and are sound.  Any backtest run in the no-internet sandbox
straight off the cache is not.  Note SPY's CAGR is deflated by 3.8pp and its Sharpe by 0.11,
so KEEP path 4b's "70% of SPY CAGR" and "Sharpe > SPY" tests are materially easier on the raw
cache - a candidate can pass 4b for no reason but the index.

This script therefore runs the whole grid TWICE: on the raw cache (comparable to nothing, kept
only to document the distortion) and on a trading-day index (the numbers that count, and the
ones reported to the leaderboard).  The proper fix is a `.dropna()`/business-day filter inside
`baseline.load_universe()`, but PROTOCOL forbids this script from touching baseline.py - raised
for the Sunday review.

Deterministic, standalone.  10 bps costs, next-day execution (engine default).
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
MAX_VOL = 0.60            # v1 eligibility, unchanged
NS = [3, 5, 8]            # tuned parameter 1
GROSSES = [0.75, 1.00]    # tuned parameter 2
IS_END = "2016-12-31"     # walk-forward: parameters chosen on 2009-2016 only
OOS_START = "2017-01-01"
SCRIPT = Path(__file__).name


# ---------------------------------------------------------------- weights
def trading_days(px):
    """Restore a trading-day index: drop weekends, then drop any remaining row on which no
    ticker moved at all (the forward-filled-holiday signature).  Yields ~252 rows/year."""
    r = px.pct_change().fillna(0.0)
    weekday = px.index.dayofweek < 5
    moved = (r != 0).sum(axis=1) > 0
    keep = weekday & (moved | (np.arange(len(px)) == 0))
    return px[keep]


def eligible_mask(px):
    """RULES v1's own eligibility filter: above the 200d MA and vol20 < 0.60."""
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def vol20_of(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def make_weights(vol_scale, n, gross):
    """Top-n by the composite (with or without the /sqrt(vol20) term), equal weight."""
    def fn(px):
        s = score(px, vol_scale=vol_scale)[0]
        elig = s.where(eligible_mask(px))
        rank = elig.rank(axis=1, ascending=False)
        return (rank <= n).astype(float) * (gross / n)
    return fn


GRID = [(vs, n, g) for vs in (True, False) for n in NS for g in GROSSES]


def label(vs, n, g):
    return f"{'ON ' if vs else 'OFF'} n={n} gross={g:.0%}"


# ---------------------------------------------------------------- helpers
def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def verdict_4a(r, base):
    """Sharpe > baseline in both halves and MaxDD no worse (less negative or equal)."""
    h1, h2 = half_sharpes(r)
    b1, b2 = half_sharpes(base)
    return h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"]


def verdict_4b(r, spy, r_oos, spy_oos):
    """Sharpe > SPY in both halves AND OOS; MaxDD <= 60% of SPY's; CAGR >= 70% of SPY's."""
    h1, h2 = half_sharpes(r)
    s1, s2 = half_sharpes(spy)
    m, ms = metrics(r), metrics(spy)
    return (h1 > s1 and h2 > s2
            and metrics(r_oos)["Sharpe"] > metrics(spy_oos)["Sharpe"]
            and abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"])
            and m["CAGR"] >= 0.70 * ms["CAGR"])


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.3f}")


# ---------------------------------------------------------------- main
def run(px, tag, emit_leaderboard=True):
    print("#" * 118)
    print(f"### {tag}")
    print("#" * 118)
    start = px.index[260]                    # same warm-up skip compare() uses
    print(f"Universe: {px.shape[1]} tickers, {px.index[0].date()} -> {px.index[-1].date()}")
    print(f"Eval sample starts {start.date()}  |  IS <= {IS_END}, OOS >= {OOS_START}")
    print(f"Grid: vol_scale ON/OFF x n in {NS} x gross in {[f'{g:.0%}' for g in GROSSES]} "
          f"= {len(GRID)} points, all reported\n")

    base = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    base_is, base_oos = base.loc[:IS_END], base.loc[OOS_START:]
    spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]

    rets, wts, tos = {}, {}, {}
    for vs, n, g in GRID:
        fn = make_weights(vs, n, g)
        w = fn(px)
        res = backtest(px, w, cost_bps=COST_BPS, freq=FREQ)
        k = label(vs, n, g)
        rets[k] = res["returns"].loc[start:]
        wts[k] = w.loc[start:]
        tos[k] = res["turnover"].loc[start:]

    # ---- sanity: ON n=5 gross 75% must reproduce the live baseline
    live = rets[label(True, 5, 0.75)]
    print(f"Sanity check (ON n=5 gross 75% vs live baseline): max abs daily diff "
          f"{(live - base).abs().max():.2e}, Sharpe {metrics(live)['Sharpe']:.4f} vs "
          f"{metrics(base)['Sharpe']:.4f}\n")

    # ---- full sample + halves + OOS for every grid point
    rows = []
    for vs, n, g in GRID:
        k = label(vs, n, g)
        r = rets[k]
        m = metrics(r)
        h1, h2 = half_sharpes(r)
        ris, roos = r.loc[:IS_END], r.loc[OOS_START:]
        mis, moos = metrics(ris), metrics(roos)
        held = (wts[k] > 0).sum(axis=1)
        v20 = vol20_of(px).loc[start:]
        hv = (v20 * (wts[k] > 0)).sum(axis=1) / held.replace(0, np.nan)
        rows.append(dict(variant=k, CAGR=m["CAGR"], Vol=m["Vol"], Sharpe=m["Sharpe"],
                         MaxDD=m["MaxDD"], H1=h1, H2=h2,
                         IS_Sharpe=mis["Sharpe"], OOS_CAGR=moos["CAGR"],
                         OOS_Sharpe=moos["Sharpe"], OOS_MaxDD=moos["MaxDD"],
                         held=held.mean(), vol_held=hv.mean(),
                         turn=tos[k].sum() / m["Years"],
                         p4a=verdict_4a(r, base),
                         p4b=verdict_4b(r, spy, roos, spy_oos)))
    grid = pd.DataFrame(rows).set_index("variant")

    for name, r in (("RULES v1 baseline", base), ("SPY", spy)):
        m = metrics(r)
        h1, h2 = half_sharpes(r)
        moos = metrics(r.loc[OOS_START:])
        grid.loc[name] = dict(CAGR=m["CAGR"], Vol=m["Vol"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                              H1=h1, H2=h2, IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                              OOS_CAGR=moos["CAGR"], OOS_Sharpe=moos["Sharpe"],
                              OOS_MaxDD=moos["MaxDD"], held=np.nan, vol_held=np.nan,
                              turn=np.nan, p4a=False, p4b=False)

    print("=" * 118)
    print("FULL GRID (all 12 points reported; H1/H2 = Sharpe by sample half; IS = 2009-2016, OOS = 2017-2026)")
    print(fmt(grid))
    print()

    # ---- mechanism: what does the scaler actually buy?
    print("=" * 118)
    print("Mechanism - average vol20 of held names and average number held, at n=5 / 75%:")
    for vs in (True, False):
        k = label(vs, 5, 0.75)
        print(f"  vol_scale {'ON ' if vs else 'OFF'}: avg vol20 of held {grid.loc[k, 'vol_held']:.1%}, "
              f"turnover {grid.loc[k, 'turn']:.1f}x/yr, CAGR {grid.loc[k, 'CAGR']:.2%}, "
              f"Sharpe {grid.loc[k, 'Sharpe']:.3f}, MaxDD {grid.loc[k, 'MaxDD']:.1%}")
    on, off = rets[label(True, 5, 0.75)], rets[label(False, 5, 0.75)]
    sp = off - on
    print(f"  OFF - ON spread (n=5, 75%): mean {sp.mean()*252:+.2%}/yr, "
          f"t = {sp.mean()/(sp.std()/np.sqrt(len(sp))):.2f}, corr(ON,OFF) = {on.corr(off):.3f}")
    print()

    # ---- overlap of the two books
    w_on, w_off = wts[label(True, 5, 0.75)] > 0, wts[label(False, 5, 0.75)] > 0
    ov = (w_on & w_off).sum(axis=1) / w_on.sum(axis=1).replace(0, np.nan)
    print(f"Name overlap ON vs OFF (n=5, 75%): mean {ov.mean():.1%} of the ON book "
          f"is also in the OFF book\n")

    # ---- walk-forward (PROTOCOL rule 8): pick on IS only, evaluate OOS untouched
    print("=" * 118)
    print("WALK-FORWARD - parameters chosen on 2009-2016 by highest IS Sharpe, evaluated on 2017-2026")
    wf_rows = []
    picks = {}
    for vs in (True, False):
        cand = [(label(vs, n, g), n, g) for n in NS for g in GROSSES]
        best = max(cand, key=lambda c: (grid.loc[c[0], "IS_Sharpe"], -c[1], -c[2]))
        picks[vs] = best[0]
        print(f"  arm vol_scale {'ON ' if vs else 'OFF'}: picked {best[0]} "
              f"(IS Sharpe {grid.loc[best[0], 'IS_Sharpe']:.3f})")
    for name, r in [(picks[True], rets[picks[True]]), (picks[False], rets[picks[False]]),
                    ("RULES v1 baseline", base), ("SPY", spy)]:
        roos = r.loc[OOS_START:]
        m = metrics(roos)
        wf_rows.append(dict(variant=name, OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"],
                            OOS_MaxDD=m["MaxDD"], OOS_Vol=m["Vol"]))
    wf = pd.DataFrame(wf_rows).set_index("variant")
    print()
    print(fmt(wf))
    print()

    # ---- second, constraint-aware selection rule.  HONESTY NOTE: this rule was added AFTER
    # seeing the grid above, so it is reported as a secondary, not as the pre-stated result.
    # Its motivation is that a pure IS-Sharpe rule ignores the drawdown constraint that KEEP
    # path 4b itself imposes, so it structurally favours the most concentrated (n=3) book.
    # Rule: highest IS Sharpe among points whose IN-SAMPLE MaxDD <= 60% of SPY's in-sample
    # MaxDD (4b's own drawdown test, applied to 2009-2016 only).
    dd_cap = 0.60 * abs(metrics(spy_is)["MaxDD"])
    print(f"Secondary rule (post-hoc, see script comment): IS MaxDD cap = {dd_cap:.1%} "
          f"(60% of SPY IS MaxDD {metrics(spy_is)['MaxDD']:.1%})")
    picks2 = {}
    for vs in (True, False):
        cand = [(label(vs, n, g), n, g) for n in NS for g in GROSSES]
        ok = [c for c in cand if abs(metrics(rets[c[0]].loc[:IS_END])["MaxDD"]) <= dd_cap]
        if not ok:
            print(f"  arm vol_scale {'ON ' if vs else 'OFF'}: no point satisfies the IS DD cap")
            continue
        best = max(ok, key=lambda c: (metrics(rets[c[0]].loc[:IS_END])["Sharpe"], -c[1], -c[2]))
        picks2[vs] = best[0]
        print(f"  arm vol_scale {'ON ' if vs else 'OFF'}: picked {best[0]} "
              f"(IS Sharpe {metrics(rets[best[0]].loc[:IS_END])['Sharpe']:.3f}, "
              f"IS MaxDD {metrics(rets[best[0]].loc[:IS_END])['MaxDD']:.1%}) -> "
              f"OOS CAGR {metrics(rets[best[0]].loc[OOS_START:])['CAGR']:.2%}, "
              f"Sharpe {metrics(rets[best[0]].loc[OOS_START:])['Sharpe']:.3f}, "
              f"MaxDD {metrics(rets[best[0]].loc[OOS_START:])['MaxDD']:.1%}")
    print()

    # ---- in-sample drawdown of every OFF point, so the "no point qualifies" claim is auditable
    print("In-sample (2009-2016) MaxDD of every grid point vs the 4b-consistent cap:")
    for vs, n, g in GRID:
        k = label(vs, n, g)
        isdd = metrics(rets[k].loc[:IS_END])["MaxDD"]
        print(f"  {k}: IS MaxDD {isdd:6.1%}  [{'under' if abs(isdd) <= dd_cap else 'OVER '} cap] "
              f"| full-sample MaxDD {grid.loc[k, 'MaxDD']:6.1%}")
    print()

    # ---- cost sensitivity (turnover is 12-24x/yr, so this matters).  Covers the pre-stated
    # walk-forward pick and the single grid point that passes 4b on the full sample.
    print("Cost sensitivity (Sharpe / CAGR, full sample):")
    for k, (vs, n, g) in [(picks[False], (False, 3, 0.75)),
                          (label(False, 8, 0.75), (False, 8, 0.75))]:
        line = []
        for c in (5, 10, 25, 50):
            rr = backtest(px, make_weights(vs, n, g)(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
            mm = metrics(rr)
            line.append(f"{c}bps {mm['Sharpe']:.2f}/{mm['CAGR']:.1%}")
        print(f"  {k}: " + "  |  ".join(line))
    print()

    winner = picks[False]
    r_w = rets[winner]
    roos_w = r_w.loc[OOS_START:]
    m, ms = metrics(r_w), metrics(spy)
    h1, h2 = half_sharpes(r_w)
    s1, s2 = half_sharpes(spy)
    b1, b2 = half_sharpes(base)
    print(f"Walk-forward selection for the IDEA arm (vol_scale OFF): {winner}")
    print(f"  4a: H1 {h1:.2f} vs base {b1:.2f} [{'pass' if h1 > b1 else 'FAIL'}] | "
          f"H2 {h2:.2f} vs {b2:.2f} [{'pass' if h2 > b2 else 'FAIL'}] | "
          f"MaxDD {m['MaxDD']:.1%} vs {metrics(base)['MaxDD']:.1%} "
          f"[{'pass' if m['MaxDD'] >= metrics(base)['MaxDD'] else 'FAIL'}] -> "
          f"{'KEEP' if verdict_4a(r_w, base) else 'fails 4a'}")
    print(f"  4b: H1 {h1:.2f} vs SPY {s1:.2f} [{'pass' if h1 > s1 else 'FAIL'}] | "
          f"H2 {h2:.2f} vs {s2:.2f} [{'pass' if h2 > s2 else 'FAIL'}] | "
          f"OOS {metrics(roos_w)['Sharpe']:.2f} vs {metrics(spy_oos)['Sharpe']:.2f} "
          f"[{'pass' if metrics(roos_w)['Sharpe'] > metrics(spy_oos)['Sharpe'] else 'FAIL'}] | "
          f"MaxDD {m['MaxDD']:.1%} vs 60% of SPY {0.60*ms['MaxDD']:.1%} "
          f"[{'pass' if abs(m['MaxDD']) <= 0.60*abs(ms['MaxDD']) else 'FAIL'}] | "
          f"CAGR {m['CAGR']:.1%} vs 70% of SPY {0.70*ms['CAGR']:.1%} "
          f"[{'pass' if m['CAGR'] >= 0.70*ms['CAGR'] else 'FAIL'}] -> "
          f"{'KEEP' if verdict_4b(r_w, spy, roos_w, spy_oos) else 'fails 4b'}")
    print()

    # ---- calendar years for the two n=5/75% books and the benchmarks
    print("=" * 118)
    print("Calendar-year returns (n=5, 75% gross)")
    yr = pd.DataFrame({"ON (=v1)": on, "OFF (idea)": off, "SPY": spy})
    print((yr.groupby(yr.index.year).apply(lambda x: (1 + x).prod() - 1)
           ).to_string(float_format=lambda x: f"{x:+.1%}"))
    print()

    # ---- leaderboard rows for ALL 12 grid points (PROTOCOL: report every grid point)
    if not emit_leaderboard:
        return
    print("=" * 118)
    print("LEADERBOARD rows (all 12 grid points; verdict column = 4a / 4b outcome)")
    for vs, n, g in GRID:
        k = label(vs, n, g)
        r = rets[k]
        m = metrics(r)
        h1, h2 = half_sharpes(r)
        bm = metrics(base)
        b1, b2 = half_sharpes(base)
        v = ("KEEP 4b" if grid.loc[k, "p4b"] else
             "KEEP 4a" if grid.loc[k, "p4a"] else "KILL")
        print(f"| 2026-09-04 | no-vol-scaling {k} | {m['CAGR']:.1%} | {m['Sharpe']:.2f} | "
              f"{m['MaxDD']:.1%} | {h1:.2f} / {h2:.2f} | {bm['Sharpe']:.2f} ({b1:.2f}/{b2:.2f}) | "
              f"{v} | {SCRIPT} |")



def signal_damage(px_raw, px_td):
    """How much does the calendar-day index change the SIGNALS themselves (not just the
    metrics)?  A 200-row rolling mean over a calendar-day index spans ~143 trading days, and
    a 20-row vol spans ~14.  research/scan.py downloads the universe WITH BTC-USD/ETH-USD, so
    the live daily scan is on the same 7-day index and inherits this."""
    _, ab_cal, v_cal = score(px_raw)
    _, ab_td, v_td = score(px_td)
    idx = px_td.index[px_td.index >= "2015-01-01"]          # after the index turns calendar-daily
    a, b = ab_cal.reindex(idx), ab_td.reindex(idx)
    dis = a != b
    e_cal = (ab_cal & (v_cal < MAX_VOL)).reindex(idx)
    e_td = (ab_td & (v_td < MAX_VOL)).reindex(idx)
    d2 = e_cal != e_td
    print("SIGNAL DAMAGE (2015+, after the cache index turns calendar-daily):")
    print(f"  200d-MA flag differs on {dis.values.mean():.2%} of ticker-days; "
          f"{(dis.sum(axis=1) > 0).mean():.1%} of days have at least one name flipped; "
          f"mean {dis.sum(axis=1).mean():.2f} of {a.shape[1]} names/day")
    print(f"  full eligibility (200d AND vol20<{MAX_VOL}) differs on {d2.values.mean():.2%} of "
          f"ticker-days, mean {d2.sum(axis=1).mean():.2f} names/day")
    print(f"  vol20 on the calendar index is a median {(v_cal.reindex(idx)/v_td.reindex(idx)).stack().median():.3f}x "
          f"of the true value (weekend zeros damp it), so the vol gate is loose and the "
          f"1/sqrt(vol20) scaler is mis-scaled")
    print()


def main():
    px_raw = load_universe()
    px_td = trading_days(px_raw)
    print("=" * 118)
    print("DATA CHECK - see the module docstring. Rows per year, raw cache vs trading-day index:")
    for tag, p_ in (("raw cache", px_raw), ("trading-day", px_td)):
        n = pd.Series(1, index=p_.index).groupby(p_.index.year).sum()
        print(f"  {tag:12s}: {len(p_)} rows total; per year "
              f"min {n.iloc[:-1].min()}, median {int(n.iloc[:-1].median())}, max {n.iloc[:-1].max()}")
    print()
    signal_damage(px_raw, px_td)
    run(px_raw, "RAW CACHE (calendar-day index - DISTORTED, documentation only)", emit_leaderboard=False)
    print()
    print("#" * 118)
    print()
    run(px_td, "TRADING-DAY INDEX (the numbers that count)", emit_leaderboard=True)


if __name__ == "__main__":
    main()

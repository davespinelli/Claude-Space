#!/usr/bin/env python3
"""Idea 40 - "vol-scaler-replacement": can a BOOK-LEVEL risk control replace RULES v1's
per-name `/sqrt(vol20)` scaler?

Context (lane A, 2026-09-04, idea 1 "no-vol-scaling")
-----------------------------------------------------
Dropping the `/sqrt(vol20)` term from the v1 composite is worth +10.1%/yr (t 3.33) and beats
v1 on Sharpe at every (n, gross).  But the resulting book breaches PROTOCOL 4b's drawdown cap
(MaxDD <= 60% of SPY's) at every n: -25.8% at n=3, -21.6% at n=5, -17.9% at n=8 (75% gross),
against a cap of ~-20%.  The nearest miss, OFF n=8 / 75%, clears the cap and fails 4b on H1
Sharpe alone (0.918 vs SPY 0.957).

So the scaler is a bad risk control (it is a low-vol *selection* tilt that cancels the
momentum signal), but the un-scaled book does need SOME risk control.  This script tests
whether a control applied to the BOOK - after selection, so it cannot corrupt the signal -
does the job the scaler was supposed to do.

Design
------
Base book (fixed, not tuned): the lane-A "OFF" book.  Eligible = above 200d MA and
vol20 < 0.60 (RULES v1's own filter); rank eligible names by the v1 composite WITHOUT the
`/sqrt(vol20)` term; hold the top n equal-weight at 75% gross (v1's live gross); weekly
rebalance; 10 bps costs; next-day execution.

Treatment - the idea under test, three arms:
    NONE      no overlay (= lane A's OFF book; the control)
    DD        book-level drawdown control (QUEUE idea 22): when the book's own drawdown from
              its running equity peak exceeds D, halve exposure; restore to full only when
              the book makes a new equity high.
    BREADTH   200d-breadth gate: when the fraction of universe names trading above their own
              200d MA falls below B, halve exposure; restore when it recovers above B.

Tuned parameters (PROTOCOL rule 4: at most two):
    1. n          positions held        in {3, 5, 8}
    2. threshold  D in {6%, 8%, 12%}  (DD arm) / B in {30%, 40%, 50%}  (BREADTH arm)
Nothing else is tuned.  Gross is fixed at 75%, the halving factor is fixed at 0.5, and the
200d / vol20 / 21-63-126-252-day lookbacks and the weekly schedule are RULES v1's own.
Grid = 3 (NONE) + 9 (DD) + 9 (BREADTH) = 21 points, ALL reported.

No look-ahead: both overlay signals are computed from data through day t and the exposure
change is executed at day t+1's close, matching the engine's convention.  The exposure switch
is charged 10 bps on the traded notional (|dmult| * gross) on the day it takes effect.

Walk-forward (PROTOCOL rule 8) - two selection rules, both fixed before any OOS number is read
-----------------------------------------------------------------------------------------
Parameters are chosen on 2009-2016 ONLY and evaluated untouched on 2017-2026.
    Rule S1 (Sharpe):  within each arm, the (n, threshold) with the highest in-sample Sharpe;
                       ties break to smaller n, then smaller threshold.
    Rule S2 (4b-aware): the same, but restricted to in-sample points whose in-sample MaxDD is
                       within 60% of SPY's in-sample MaxDD - i.e. selecting for the thing this
                       idea exists to fix.  If no point qualifies, S2 is reported as "none".
Both rules are reported for all three arms, and the OOS column of all 21 points is printed, so
the selection can be audited rather than trusted.

Verdicts
--------
4a (beat the book): Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than RULES v1.
4b (capital-worthy): Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
    CAGR >= 70% of SPY's.
Evaluated for every grid point and for the walk-forward selections.

Data: data/prices.csv, now on a corrected trading-day index (commit c006b43, lane A idea 38);
verified in-script.  Survivorship caveat: research/universe.json is a current-constituent list,
which flatters any momentum book.

Deterministic, standalone.  Reads baseline.py; modifies nothing.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, score, rules_v1_weights
from engine import backtest, metrics

COST_BPS = 10
FREQ = "W"
MAX_VOL = 0.60                  # v1 eligibility, unchanged
GROSS = 0.75                    # v1's live gross, FIXED (not a tuned parameter)
HALVE = 0.5                     # overlay cuts exposure to this multiple, FIXED
NS = [3, 5, 8]                  # tuned parameter 1
DD_THRESH = [0.06, 0.08, 0.12]  # tuned parameter 2, DD arm
BR_THRESH = [0.30, 0.40, 0.50]  # tuned parameter 2, BREADTH arm
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SCRIPT = Path(__file__).name

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 40)


# ---------------------------------------------------------------- book construction
def eligible_mask(px):
    """RULES v1's own eligibility filter: above the 200d MA and vol20 < 0.60."""
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def base_weights(px, n):
    """Top-n eligible names by the v1 composite WITHOUT /sqrt(vol20), equal weight at GROSS."""
    s = score(px, vol_scale=False)[0]
    rank = s.where(eligible_mask(px)).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (GROSS / n)


def breadth(px):
    """Fraction of the universe trading above its own 200d MA, computed at each day t."""
    above = px > px.rolling(200).mean()
    return above.sum(axis=1) / above.notna().sum(axis=1).replace(0, np.nan)


# ---------------------------------------------------------------- overlays
def overlay_none(r, _):
    return r, pd.Series(1.0, index=r.index)


def overlay_dd(r, thresh):
    """Book-level drawdown control.  State machine on the OVERLAID book's own equity, so the
    peak is the peak of what is actually traded.  Decision uses data through t, exposure
    changes at t+1, and the switch pays COST_BPS on |dmult| * GROSS."""
    vals = r.values
    out = np.empty(len(vals))
    mults = np.empty(len(vals))
    mult, pending, eq, peak = 1.0, 1.0, 1.0, 1.0
    for i, ri in enumerate(vals):
        cost = abs(pending - mult) * GROSS * COST_BPS / 1e4   # switch executes today
        mult = pending
        ret = ri * mult - cost
        out[i] = ret
        mults[i] = mult
        eq *= 1 + ret
        peak = max(peak, eq)
        dd = eq / peak - 1
        if mult == 1.0 and dd < -thresh:
            pending = HALVE                                   # cut, effective tomorrow
        elif mult < 1.0 and eq >= peak:
            pending = 1.0                                     # new high -> restore tomorrow
    return pd.Series(out, index=r.index), pd.Series(mults, index=r.index)


def overlay_signal(r, sig):
    """Generic 'halve while sig is True' overlay.  `sig` must already be shifted by one day
    (decided at t, executed at t+1)."""
    mult = np.where(sig.reindex(r.index).fillna(False).values, HALVE, 1.0)
    dmult = np.abs(np.diff(np.concatenate([[1.0], mult])))
    out = r.values * mult - dmult * GROSS * COST_BPS / 1e4
    return pd.Series(out, index=r.index), pd.Series(mult, index=r.index)


# ---------------------------------------------------------------- metric helpers
def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def verdict_4a(r, base):
    h1, h2 = half_sharpes(r)
    b1, b2 = half_sharpes(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def verdict_4b(r, spy, r_oos, spy_oos):
    h1, h2 = half_sharpes(r)
    s1, s2 = half_sharpes(spy)
    m, ms = metrics(r), metrics(spy)
    return bool(h1 > s1 and h2 > s2
                and metrics(r_oos)["Sharpe"] > metrics(spy_oos)["Sharpe"]
                and abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"])
                and m["CAGR"] >= 0.70 * ms["CAGR"])


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.3f}")


def label(arm, n, th):
    if arm == "NONE":
        return f"NONE    n={n}"
    unit = "D" if arm == "DD" else "B"
    return f"{arm:<7} n={n} {unit}={th:.0%}"


# ---------------------------------------------------------------- main
def main():
    px = load_universe()
    yrs = px.index.to_series().groupby(px.index.year).count()
    print("=" * 120)
    print(f"Idea 40 vol-scaler-replacement (lane B) | {SCRIPT}")
    print("=" * 120)
    print(f"Universe: {px.shape[1]} tickers, {px.index[0].date()} -> {px.index[-1].date()}")
    print(f"Index sanity (must be ~252 rows/yr; the calendar-day bug gave 365): "
          f"2013 {yrs.get(2013)}, 2018 {yrs.get(2018)}, 2024 {yrs.get(2024)}")
    if yrs.loc[2015:2024].max() > 300:
        print("!! CALENDAR-DAY INDEX DETECTED - results below are not comparable. Aborting.")
        sys.exit(1)

    start = px.index[260]                      # same warm-up skip baseline.compare() uses
    print(f"Eval sample: {start.date()} -> {px.index[-1].date()} | IS <= {IS_END}, OOS >= {OOS_START}")
    print(f"Base book: top-n by composite WITHOUT /sqrt(vol20), eligible only, {GROSS:.0%} gross, "
          f"weekly, {COST_BPS} bps")
    print(f"Grid: NONE x {len(NS)} + DD x {len(NS)*len(DD_THRESH)} + BREADTH x "
          f"{len(NS)*len(BR_THRESH)} = {len(NS)*(1+len(DD_THRESH)+len(BR_THRESH))} points, all reported\n")

    base_v1 = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]

    br = breadth(px)
    br_lag = br.shift(1)                       # decided at t, executed at t+1

    # ---- raw (un-overlaid) book per n
    raw, raw_to = {}, {}
    for n in NS:
        res = backtest(px, base_weights(px, n), cost_bps=COST_BPS, freq=FREQ)
        raw[n] = res["returns"].loc[start:]
        raw_to[n] = res["turnover"].loc[start:]

    # ---- build the full grid
    variants = {}
    for n in NS:
        variants[("NONE", n, None)] = overlay_none(raw[n], None)
        for d in DD_THRESH:
            variants[("DD", n, d)] = overlay_dd(raw[n], d)
        for b in BR_THRESH:
            variants[("BREADTH", n, b)] = overlay_signal(raw[n], br_lag < b)

    rows = []
    for (arm, n, th), (r, mult) in variants.items():
        m = metrics(r)
        h1, h2 = half_sharpes(r)
        r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
        m_is, m_oos = metrics(r_is), metrics(r_oos)
        rows.append(dict(variant=label(arm, n, th), arm=arm, n=n, th=th,
                         CAGR=m["CAGR"], Vol=m["Vol"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                         H1=h1, H2=h2,
                         IS_Sharpe=m_is["Sharpe"], IS_MaxDD=m_is["MaxDD"],
                         OOS_CAGR=m_oos["CAGR"], OOS_Sharpe=m_oos["Sharpe"], OOS_MaxDD=m_oos["MaxDD"],
                         cut=(mult < 1).mean(), turn=raw_to[n].sum() / m["Years"],
                         p4a=verdict_4a(r, base_v1), p4b=verdict_4b(r, spy, r_oos, spy_oos)))
    grid = pd.DataFrame(rows).set_index("variant")
    grid_only = grid.copy()

    for nm, r in (("RULES v1 baseline", base_v1), ("SPY", spy)):
        m = metrics(r)
        h1, h2 = half_sharpes(r)
        m_oos = metrics(r.loc[OOS_START:])
        grid.loc[nm] = dict(arm="-", n=np.nan, th=np.nan, CAGR=m["CAGR"], Vol=m["Vol"],
                            Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                            IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                            IS_MaxDD=metrics(r.loc[:IS_END])["MaxDD"],
                            OOS_CAGR=m_oos["CAGR"], OOS_Sharpe=m_oos["Sharpe"],
                            OOS_MaxDD=m_oos["MaxDD"], cut=np.nan, turn=np.nan,
                            p4a=False, p4b=False)

    show = ["CAGR", "Vol", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe", "IS_MaxDD",
            "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "cut", "turn", "p4a", "p4b"]
    print("=" * 120)
    print("FULL GRID - all 21 points. H1/H2 = Sharpe by sample half. cut = fraction of days at "
          "half exposure. turn = base-book turnover x/yr.")
    print(fmt(grid[show]))
    print()

    m_spy = metrics(spy)
    dd_cap, cagr_floor = 0.60 * abs(m_spy["MaxDD"]), 0.70 * m_spy["CAGR"]
    print(f"4b thresholds on this sample: MaxDD cap {-dd_cap:.1%}, CAGR floor {cagr_floor:.1%}, "
          f"SPY halves {m_spy and half_sharpes(spy)[0]:.3f} / {half_sharpes(spy)[1]:.3f}, "
          f"SPY OOS Sharpe {metrics(spy_oos)['Sharpe']:.3f}")
    print()

    # ---- does the overlay do its job? mechanism, at the control's own drawdown
    print("=" * 120)
    print("MECHANISM - what each overlay does to the raw book's drawdown (per n, best threshold "
          "by MaxDD improvement):")
    for n in NS:
        m0 = metrics(raw[n])
        print(f"  n={n}: raw {m0['CAGR']:.2%} / {m0['Sharpe']:.3f} / {m0['MaxDD']:.1%}")
        for arm, ths in (("DD", DD_THRESH), ("BREADTH", BR_THRESH)):
            for th in ths:
                r, mult = variants[(arm, n, th)]
                m = metrics(r)
                print(f"      {arm:<7} th={th:.0%}: {m['CAGR']:.2%} / {m['Sharpe']:.3f} / "
                      f"{m['MaxDD']:.1%}  (DD kept {m['MaxDD']/m0['MaxDD']:.0%} of raw, "
                      f"CAGR kept {m['CAGR']/m0['CAGR']:.0%}, {((mult<1).mean()):.0%} of days at half)")
    print()

    # ---- stress years
    print("=" * 120)
    print("STRESS YEARS (calendar-year total return):")
    keys = [("NONE", 8, None), ("DD", 8, 0.08), ("BREADTH", 8, 0.40),
            ("NONE", 5, None), ("DD", 5, 0.08), ("BREADTH", 5, 0.40)]
    yr = pd.DataFrame({label(*k): (1 + variants[k][0]).groupby(variants[k][0].index.year).prod() - 1
                       for k in keys})
    yr["RULES v1"] = (1 + base_v1).groupby(base_v1.index.year).prod() - 1
    yr["SPY"] = (1 + spy).groupby(spy.index.year).prod() - 1
    print(yr.loc[[y for y in (2011, 2015, 2018, 2020, 2022, 2025) if y in yr.index]]
          .to_string(float_format=lambda x: f"{x:+.1%}"))
    print()

    # ---- walk-forward, PROTOCOL rule 8
    print("=" * 120)
    print("WALK-FORWARD (rule 8): parameters chosen on 2009-2016 only, evaluated on 2017-2026.")
    is_dd_cap = 0.60 * abs(metrics(spy_is)["MaxDD"])
    print(f"  In-sample SPY MaxDD {metrics(spy_is)['MaxDD']:.1%} -> S2 in-sample DD cap {-is_dd_cap:.1%}")
    picks = {}
    for arm in ("NONE", "DD", "BREADTH"):
        sub = grid_only[grid_only.arm == arm].copy()
        sub["th_r"] = sub["th"].fillna(0.0)
        s1 = sub.sort_values(["IS_Sharpe", "n", "th_r"], ascending=[False, True, True]).index[0]
        ok = sub[sub.IS_MaxDD >= -is_dd_cap]
        s2 = (ok.sort_values(["IS_Sharpe", "n", "th_r"], ascending=[False, True, True]).index[0]
              if len(ok) else None)
        picks[(arm, "S1")] = s1
        picks[(arm, "S2")] = s2
    wf = pd.DataFrame([dict(rule=f"{arm} / {rule}", pick=(p if p else "none (no IS point met the DD cap)"),
                            **({} if p is None else grid_only.loc[p, ["IS_Sharpe", "IS_MaxDD", "OOS_CAGR",
                                                                     "OOS_Sharpe", "OOS_MaxDD", "p4a", "p4b"]].to_dict()))
                       for (arm, rule), p in picks.items()]).set_index("rule")
    for nm, r in (("RULES v1 baseline", base_v1), ("SPY", spy)):
        m_oos = metrics(r.loc[OOS_START:])
        wf.loc[nm] = dict(pick="-", IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                          IS_MaxDD=metrics(r.loc[:IS_END])["MaxDD"], OOS_CAGR=m_oos["CAGR"],
                          OOS_Sharpe=m_oos["Sharpe"], OOS_MaxDD=m_oos["MaxDD"], p4a=False, p4b=False)
    print(fmt(wf))
    print()

    # ---- verdict summary
    print("=" * 120)
    print("KEEP PATHS - points passing either path (full-sample tests + OOS Sharpe for 4b):")
    p4a = grid_only[grid_only.p4a]
    p4b = grid_only[grid_only.p4b]
    print(f"  4a passes: {list(p4a.index) if len(p4a) else 'none'}")
    print(f"  4b passes: {list(p4b.index) if len(p4b) else 'none'}")
    if len(p4b):
        print(fmt(p4b[show]))
    else:
        near = grid_only.copy()
        near["fail"] = [
            ", ".join(f for f, bad in (
                ("H1<=SPY", row.H1 <= half_sharpes(spy)[0]),
                ("H2<=SPY", row.H2 <= half_sharpes(spy)[1]),
                ("OOS<=SPY", row.OOS_Sharpe <= metrics(spy_oos)["Sharpe"]),
                ("MaxDD", abs(row.MaxDD) > dd_cap),
                ("CAGR", row.CAGR < cagr_floor)) if bad)
            for row in grid_only.itertuples()]
        print("\n  Nearest misses (which 4b tests each point fails):")
        print(near[["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "fail"]]
              .sort_values("Sharpe", ascending=False).to_string(float_format=lambda x: f"{x:.3f}"))
    print()

    # ---- leaderboard rows
    print("=" * 120)
    print("LEADERBOARD rows:")
    b0 = metrics(base_v1)
    bh1, bh2 = half_sharpes(base_v1)
    today = pd.Timestamp("2026-09-04").date()
    for v in grid_only.index:
        row = grid_only.loc[v]
        vd = "KEEP 4a" if row.p4a else ("KEEP 4b" if row.p4b else "KILL")
        print(f"| {today} | 40 {v} | {row.CAGR:.1%} | {row.Sharpe:.2f} | {row.MaxDD:.1%} | "
              f"{row.H1:.2f} / {row.H2:.2f} | {b0['Sharpe']:.2f} ({bh1:.2f}/{bh2:.2f}) | {vd} | {SCRIPT} |")


if __name__ == "__main__":
    main()

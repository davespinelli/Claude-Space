#!/usr/bin/env python3
"""QUEUE idea 23 — earnings-season-avoidance (cloud, 2026-09-04).

Question (as worded in QUEUE.md)
--------------------------------
"v1 excluding single stocks during their earnings weeks (approximate with quarterly
calendar).  Expect PARK: needs earnings dates."

We have no earnings dates in the sandbox (no network, no EDGAR).  What we CAN test
honestly is the calendar approximation the queue itself proposes: US large caps are
overwhelmingly December-fiscal-year filers reporting 2-6 weeks after each calendar
quarter end, so a fixed post-quarter-end window covers most of the reporting mass of
most names in both panels.  If the effect the idea is after is large, a window that is
right on average should show it; if a fixed season window does nothing, per-name dates
would have to carry the entire effect for the idea to be alive.

Two things are therefore measured, and they are separable:
  (A) PREMISE — do single stocks earn MORE (or just be more volatile) inside the
      approximate season than outside it?  Direct panel measurement of per-name daily
      excess return / vol / kurtosis in-season vs out, plus a placebo season.  The
      literature prior is Frazzini-Lamont (2007) "earnings announcement premium":
      returns are HIGHER in announcement months, i.e. avoidance should COST return.
  (B) THE RULE — the book with single stocks forced out of the eligible set during the
      window, at every grid point, both universes, both gross conventions.

Design (PROTOCOL rules 1-9)
---------------------------
Panels    : `baseline.load_universe()` (56 names: 36 ETFs + 20 mega-cap stocks) and
            `load_universe(broad=True)` (136 names: 36 ETFs + 100 large caps).
            SURVIVORSHIP: both are CURRENT constituents; every level below is biased up.
            ETFs are never blacked out (a fund has no earnings date), which is also why
            the u56 panel is the weaker test — only 20 of 56 names can ever be excluded.
Blackout  : calendar days d with  start <= (d - most recent quarter end) < start+length,
            applied to SINGLE STOCKS only (universe.json's ETF groups are exempt).
Tuned     : exactly 2 — `start` in {7,14,21,28,35} days after quarter end and `length`
            in {14,21,28} days.  15 windows, ALL reported.  Everything else is held at
            the incumbent books' own settings: gate (200d, vol20<0.60), gross 75%,
            weekly cadence, 10 bps, next-day execution.
Controls  : `start=None` (no blackout) is the anchor in every cell, and a PLACEBO season
            shifted +45 days (mid-quarter, outside any plausible reporting window) is run
            at the same lengths — an "avoidance" effect that shows up equally in the
            placebo is a calendar/turnover artefact, not earnings.
Books     : v1 (live rules, top-5 risk-adjusted), top20 (idea 2's standing 4b KEEP,
            no vol scaler), ewall (idea 10's equal-weight-all-eligible).  The book is NOT
            a tuned parameter here: all three are reported and nothing is selected on it.
Conventions: `replace` (rank/weight over the eligible set with the blacked-out names
            removed — the book still holds n names at constant gross) and `cash` (rank
            over the full eligible set, then sit the blacked-out holdings out in cash —
            gross falls).  Both are reported: ideas 66/73/84 established gross is an
            exact lever with ~zero Sharpe content, so the `cash` form confounds the rule
            with a de-grossing on 4b's CAGR/drawdown bars and cannot be read alone.
Rule 8    : (start,length) chosen on 2009-2016 by IS Sharpe, evaluated on 2017-2026
            untouched, per (universe, book, convention); OOS reported vs RULES v1 and SPY.

KNOWN DATA CAVEAT (queue idea 38): data/prices*.csv are indexed on CALENDAR days after
2014-09-17 because BTC-USD is in the download, so post-2014 weekends are zero-return
rows.  That affects every arm here identically (including baseline and SPY), so the
cross-arm comparisons are apples-to-apples; absolute Sharpe levels are not trustworthy
until idea 38 lands.  It also means the blackout window is applied on calendar days,
which is exactly what a quarterly-calendar approximation wants.

Deterministic, standalone:
    python research/backtests/2026-09-04_earnings-season-avoidance_cloud.py
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd

from baseline import load_universe, rules_v1_weights, score
from engine import backtest, metrics

COST_BPS = 10
FREQ = "W"
GROSS = 0.75
SPLIT = "2017-01-01"
IS_END = "2016-12-31"
STARTS = [7, 14, 21, 28, 35]
LENGTHS = [14, 21, 28]
PLACEBO_SHIFT = 45
OUT = Path(__file__).with_suffix("")

_U = json.loads((REPO / "research" / "universe.json").read_text())
ETFS = set(_U["broad"]) | set(_U["sectors"]) | set(_U["bonds_fx_commod"])


# ---------------------------------------------------------------- blackout calendar
def days_since_quarter_end(idx):
    """Calendar days since the most recent 3/31, 6/30, 9/30 or 12/31."""
    qe = pd.Series(idx, index=idx).apply(lambda d: (d - pd.offsets.QuarterEnd(1)).normalize())
    return (pd.Series(idx, index=idx) - qe).dt.days


def blackout_mask(px, start, length, shift=0):
    """DataFrame[date x ticker], True where the name is inside its approximate season.

    ETFs are never True.  start=None -> all False (the no-blackout anchor).
    """
    M = pd.DataFrame(False, index=px.index, columns=px.columns)
    if start is None:
        return M
    d = days_since_quarter_end(px.index)
    s = start + shift
    inwin = (d >= s) & (d < s + length)
    stocks = [c for c in px.columns if c not in ETFS]
    M.loc[:, stocks] = np.repeat(inwin.values[:, None], len(stocks), axis=1)
    return M


# ---------------------------------------------------------------- books
def _elig(px):
    s, above, vol20 = score(px, vol_scale=False)
    return s, (above & (vol20 < 0.60) & s.notna())


def _ranked(s, ok, black, n, w_each, replace):
    """Top-n by composite `s` among `ok`.

    replace=True  : rank on the eligible set with blacked-out names REMOVED, so the
                    next-best names are promoted and the book still holds n names at
                    constant gross.  This is "avoid the name, keep the exposure".
    replace=False : rank on the FULL eligible set, then zero the blacked-out holdings
                    and leave the weight in CASH.  This is "avoid the name, sit out".
    Both are reported; ideas 66/73/84 established gross is an exact lever, so the two
    have to be separated or the rule is confounded with a de-grossing.
    """
    if replace:
        rank = s.where(ok & ~black).rank(axis=1, ascending=False)
        return (rank <= n).astype(float) * w_each
    rank = s.where(ok).rank(axis=1, ascending=False)
    return ((rank <= n) & ~black).astype(float) * w_each


def book_v1(px, black, replace):
    """RULES v1: top-5 by the risk-adjusted composite, 15% each (75% gross)."""
    s, above, vol20 = score(px, vol_scale=True)
    return _ranked(s, above & (vol20 < 0.60), black, 5, 0.15, replace)


def book_top20(px, black, replace, n=20):
    """Idea 2's 4b KEEP-candidate: top-n composite, no vol scaler, GROSS/n each."""
    s, base_ok = _elig(px)
    return _ranked(s, base_ok, black, n, GROSS / n, replace)


def book_ewall(px, black, replace):
    """Idea 10's EWall: equal-weight every eligible name, GROSS in total.

    replace=True -> re-equal-weight over the survivors (gross held at GROSS);
    replace=False -> keep 1/k weights from the FULL eligible count, survivors only
    (gross falls by the blacked-out share).
    """
    s, base_ok = _elig(px)
    k_all = base_ok.sum(axis=1)
    keep = (base_ok & ~black).astype(float)
    k = keep.sum(axis=1) if replace else k_all
    return keep.div(k.where(k > 0), axis=0).fillna(0.0) * GROSS


BOOKS = {"v1": book_v1, "top20": book_top20, "ewall": book_ewall}


# ---------------------------------------------------------------- metrics helpers
def stats(r):
    m = metrics(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"])


def full_row(r):
    h = len(r) // 2
    a, b, c = stats(r), stats(r.iloc[:h]), stats(r.iloc[h:])
    o, i = stats(r.loc[SPLIT:]), stats(r.loc[:IS_END])
    return dict(CAGR=a["CAGR"], Sharpe=a["Sharpe"], MaxDD=a["MaxDD"], H1=b["Sharpe"], H2=c["Sharpe"],
                IS_Sharpe=i["Sharpe"], OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"])


def keep_4a(row, base):
    return bool(row["H1"] > base["H1"] and row["H2"] > base["H2"] and row["MaxDD"] >= base["MaxDD"])


def keep_4b(row, spy):
    return bool(row["H1"] > spy["H1"] and row["H2"] > spy["H2"] and row["OOS_Sharpe"] > spy["OOS_Sharpe"]
                and row["MaxDD"] >= 0.60 * spy["MaxDD"] and row["CAGR"] >= 0.70 * spy["CAGR"])


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.3f}")


# ---------------------------------------------------------------- (A) premise test
def premise(tag, px):
    """Do single stocks behave differently inside the approximate season?"""
    print("=" * 110)
    print(f"### (A) PREMISE, universe {tag}: per-name daily stats in-season vs out "
          f"(single stocks only, SPY-excess)")
    stocks = [c for c in px.columns if c not in ETFS]
    rets = px[stocks].pct_change()
    spy = px["SPY"].pct_change()
    ex = rets.sub(spy, axis=0)
    d = days_since_quarter_end(px.index)
    rows = []
    for label, shift in (("season", 0), (f"placebo(+{PLACEBO_SHIFT}d)", PLACEBO_SHIFT)):
        for start in STARTS:
            for length in LENGTHS:
                s = start + shift
                m = ((d >= s) & (d < s + length)).values
                a, b = ex[m], ex[~m]
                av, bv = a.stack().dropna(), b.stack().dropna()
                # Welch t on the difference of daily mean excess return
                t = (av.mean() - bv.mean()) / np.sqrt(av.var() / len(av) + bv.var() / len(bv))
                rows.append(dict(window=label, start=start, length=length,
                                 days_in=int(m.sum()), share=m.mean(),
                                 ex_in_bps=1e4 * av.mean(), ex_out_bps=1e4 * bv.mean(),
                                 diff_bps=1e4 * (av.mean() - bv.mean()), t=t,
                                 vol_in=av.std() * np.sqrt(252), vol_out=bv.std() * np.sqrt(252)))
    P = pd.DataFrame(rows)
    print(fmt(P.set_index(["window", "start", "length"])))
    sea = P[P["window"] == "season"]
    pla = P[P["window"] != "season"]
    print(f"\nseason  : mean diff {sea['diff_bps'].mean():+.2f} bps/day, positive in "
          f"{int((sea['diff_bps'] > 0).sum())}/{len(sea)} windows, max |t| {sea['t'].abs().max():.2f}")
    print(f"placebo : mean diff {pla['diff_bps'].mean():+.2f} bps/day, positive in "
          f"{int((pla['diff_bps'] > 0).sum())}/{len(pla)} windows, max |t| {pla['t'].abs().max():.2f}")
    P["universe"] = tag
    return P


# ---------------------------------------------------------------- (B) the rule
def run_universe(tag, px, records):
    start_eval = px.index[260]
    print("=" * 110)
    print(f"### (B) UNIVERSE {tag}: {px.shape[1]} tickers "
          f"({len([c for c in px.columns if c not in ETFS])} single stocks, "
          f"{len([c for c in px.columns if c in ETFS])} ETFs), "
          f"{px.index[0].date()} -> {px.index[-1].date()} | eval from {start_eval.date()}")

    base_r = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start_eval:]
    spy_r = px["SPY"].pct_change().fillna(0).loc[start_eval:]
    base, spy = full_row(base_r), full_row(spy_r)
    print("\nReference rows (same days, same costs):")
    print(fmt(pd.DataFrame({"RULES v1 baseline": base, "SPY": spy}).T))
    print(f"\n4b bars: Sharpe > SPY H1 {spy['H1']:.3f} / H2 {spy['H2']:.3f} / OOS {spy['OOS_Sharpe']:.3f}"
          f" · MaxDD >= {0.60 * spy['MaxDD']:.1%} · CAGR >= {0.70 * spy['CAGR']:.2%}")

    grid = [("none", None, 0, 0)]
    grid += [("season", s, L, 0) for s in STARTS for L in LENGTHS]
    grid += [("placebo", s, L, PLACEBO_SHIFT) for s in STARTS for L in LENGTHS]

    for bname, bfn in BOOKS.items():
        for replace in (True, False):
            conv = "replace" if replace else "cash"
            rows = []
            for kind, s, L, shift in grid:
                M = blackout_mask(px, s, L, shift)
                w = bfn(px, M, replace)
                res = backtest(px, w, cost_bps=COST_BPS, freq=FREQ)
                r = res["returns"].loc[start_eval:]
                row = full_row(r)
                yrs = len(r) / 252
                row["Turn/yr"] = res["turnover"].loc[start_eval:].sum() / yrs
                row["Gross"] = w.loc[start_eval:].sum(axis=1).mean()
                row["4a"] = keep_4a(row, base)
                row["4b"] = keep_4b(row, spy)
                rows.append(dict(universe=tag, book=bname, conv=conv, kind=kind,
                                 start=(-1 if s is None else s), length=L, **row))
                records.append(rows[-1])
            df = pd.DataFrame(rows).set_index(["kind", "start", "length"])[
                ["Gross", "Turn/yr", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                 "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "4a", "4b"]]
            anchor = rows[0]
            print(f"\n--- {tag} | book={bname} | conv={conv}  "
                  f"(anchor kind=none: CAGR {anchor['CAGR']:.1%}, Sharpe {anchor['Sharpe']:.3f}, "
                  f"MaxDD {anchor['MaxDD']:.1%})")
            print(fmt(df))
    return base, spy


def main():
    universes = {"u56": load_universe(), "broad": load_universe(broad=True)}

    prem = [premise(tag, px) for tag, px in universes.items()]
    pd.concat(prem).to_csv(OUT.with_suffix(".premise.csv"), index=False)

    records, refs = [], {}
    for tag, px in universes.items():
        refs[tag] = run_universe(tag, px, records)

    G = pd.DataFrame(records)
    G.to_csv(OUT.with_suffix(".grid.csv"), index=False)

    # ------------------------------------------------------- effect size vs the anchor
    print("\n" + "=" * 110)
    print("### Effect of the blackout against the SAME book with no blackout (dSharpe, dCAGR, dMaxDD)")
    print("A real avoidance edge is dSharpe > 0 in the season rows and ~0 in the placebo rows.\n")
    eff = []
    for (tag, bname, conv), sub in G.groupby(["universe", "book", "conv"], sort=False):
        a = sub[sub["kind"] == "none"].iloc[0]
        for _, r in sub[sub["kind"] != "none"].iterrows():
            eff.append(dict(universe=tag, book=bname, conv=conv, kind=r["kind"],
                            start=r["start"], length=r["length"],
                            dSharpe=r["Sharpe"] - a["Sharpe"], dCAGR=r["CAGR"] - a["CAGR"],
                            dMaxDD=r["MaxDD"] - a["MaxDD"], dTurn=r["Turn/yr"] - a["Turn/yr"]))
    E = pd.DataFrame(eff)
    E.to_csv(OUT.with_suffix(".effect.csv"), index=False)
    summ = E.groupby(["kind", "universe", "book", "conv"]).agg(
        n=("dSharpe", "size"), dSharpe_mean=("dSharpe", "mean"), dSharpe_min=("dSharpe", "min"),
        dSharpe_max=("dSharpe", "max"), pos=("dSharpe", lambda x: int((x > 0).sum())),
        dCAGR_mean=("dCAGR", "mean"), dMaxDD_mean=("dMaxDD", "mean"))
    print(fmt(summ))
    for kind in ("season", "placebo"):
        sub = E[E["kind"] == kind]
        print(f"\n{kind:8s}: dSharpe mean {sub['dSharpe'].mean():+.4f}, positive in "
              f"{int((sub['dSharpe'] > 0).sum())}/{len(sub)} cells; "
              f"dCAGR mean {sub['dCAGR'].mean():+.2%}; dMaxDD mean {sub['dMaxDD'].mean():+.2%}")

    # ------------------------------------------------------- rule 8 walk-forward
    print("\n" + "=" * 110)
    print("### PROTOCOL rule 8 — (start,length) chosen on 2009-2016 by IS Sharpe, 2017-2026 untouched")
    print("Selection pool = the anchor plus the 15 SEASON windows (the placebo is a control, never picked).\n")
    wf = []
    for (tag, bname, conv), sub in G.groupby(["universe", "book", "conv"], sort=False):
        pool = sub[sub["kind"].isin(["none", "season"])]
        pick = pool.loc[pool["IS_Sharpe"].idxmax()]
        anchor = sub[sub["kind"] == "none"].iloc[0]
        base, spy = refs[tag]
        wf.append(dict(universe=tag, book=bname, conv=conv,
                       pick=f"{pick['kind']}({int(pick['start'])},{int(pick['length'])})",
                       IS_Sharpe=pick["IS_Sharpe"], IS_anchor=anchor["IS_Sharpe"],
                       OOS_CAGR=pick["OOS_CAGR"], OOS_Sharpe=pick["OOS_Sharpe"], OOS_MaxDD=pick["OOS_MaxDD"],
                       anchor_OOS_Sharpe=anchor["OOS_Sharpe"], dOOS_vs_anchor=pick["OOS_Sharpe"] - anchor["OOS_Sharpe"],
                       best_OOS_in_pool=pool["OOS_Sharpe"].max(),
                       regret=pick["OOS_Sharpe"] - pool["OOS_Sharpe"].max(),
                       base_OOS_Sharpe=base["OOS_Sharpe"], spy_OOS_Sharpe=spy["OOS_Sharpe"],
                       beats_base=bool(pick["OOS_Sharpe"] > base["OOS_Sharpe"]),
                       beats_spy=bool(pick["OOS_Sharpe"] > spy["OOS_Sharpe"]),
                       full_4a=bool(pick["4a"]), full_4b=bool(pick["4b"])))
    W = pd.DataFrame(wf)
    print(fmt(W.set_index(["universe", "book", "conv"])))
    W.to_csv(OUT.with_suffix(".walkforward.csv"), index=False)

    # ------------------------------------------------------- census
    print("\n" + "=" * 110)
    print(f"### CENSUS over all {len(G)} grid points (incl. anchors and placebos): "
          f"4a {int(G['4a'].sum())}, 4b {int(G['4b'].sum())}")
    season = G[G["kind"] == "season"]
    anchors = G[G["kind"] == "none"]
    print(f"Season rows only ({len(season)}): 4a {int(season['4a'].sum())}, 4b {int(season['4b'].sum())}")
    print(f"Anchors ({len(anchors)}): 4a {int(anchors['4a'].sum())}, 4b {int(anchors['4b'].sum())}")
    keeps = season[season["4b"]]
    if len(keeps):
        print("\nSeason rows passing 4b:")
        print(fmt(keeps.set_index(["universe", "book", "conv", "start", "length"])[
            ["Gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "4a", "4b"]]))
        # do they pass BECAUSE of the blackout, or despite it?
        print("\n(their anchors, same book/conv, for comparison)")
        print(fmt(anchors.set_index(["universe", "book", "conv"])[
            ["Gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "4a", "4b"]]))
    print(f"\nWritten: {OUT.name}.premise.csv / .grid.csv / .effect.csv / .walkforward.csv")


if __name__ == "__main__":
    main()

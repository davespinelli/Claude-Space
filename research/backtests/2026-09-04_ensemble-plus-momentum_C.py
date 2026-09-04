#!/usr/bin/env python3
"""QUEUE idea 26 — ensemble-plus-momentum (lane C, 2026-09-04).

Question (as worded in QUEUE.md)
--------------------------------
"50% macro-trend-ensemble B + 50% v1 top-5.  Diversification of two weak-ish sleeves."

Idea 18's variant B (TSMOM votes on 9 macro ETFs, inverse-vol risk parity) is a
low-return / high-Sharpe defensive sleeve (5.0% CAGR, 0.87 Sharpe, -10.1% MaxDD).
RULES v1's top-5 book is a low-return / low-Sharpe momentum book (6.4% / 0.66 / -13.8%).
Idea 24 already married the sleeve to a PASSIVE core (SPY/QQQ + 200d gate).  Idea 26 is
the untested marriage: sleeve + the project's own ACTIVE cross-sectional book.  If the
two sleeves are genuinely uncorrelated, the blend's Sharpe should sit above the weighted
average of the parts, and the 4b bars (which the parts fail from opposite directions —
the sleeve on CAGR, v1 on Sharpe) might be cleared jointly.

Design (PROTOCOL rules 1-9)
---------------------------
Panels    : `baseline.load_universe()` (56 names) and `load_universe(broad=True)`
            (136 names).  All 9 macro ETFs are present in both.  SURVIVORSHIP: both
            lists are CURRENT constituents, so every result here is biased upward.
Sleeve S  : idea 18 variant B copied verbatim from
            research/backtests/2026-09-03_macro-trend-ensemble.py — vote in {0,1/3,2/3,1}
            on the signs of {12-1 momentum, 6m, 3m} times inverse-60d-vol risk parity
            over SPY QQQ IWM EFA EEM TLT GLD DBC UUP, normalised to 1.0.  Gross <= 100%.
Books E   : (a) `v1`     — RULES v1 live weights (top-5 risk-adjusted, 15% each = 75%).
                          This is the book the idea names.
            (b) `top20`  — idea 2's standing 4b KEEP-candidate: top 20 by the v1
                          composite WITHOUT /sqrt(vol20), 0.75/20 each.
            (c) `ewall`  — idea 10's `EWall`: equal-weight every eligible name, 75% gross.
            (b) and (c) are carried because the project's best books are no longer v1;
            a diversification claim that only works against the weakest sleeve is not a
            claim about diversification.
Blend     : natural   w = f*S + (1-f)*E   (gross drifts with f: f*g_S + (1-f)*g_E)
            matched   w = (f*S + (1-f)*E) rescaled per row to E's OWN gross that day.
            Both conventions are REPORTED, not chosen: the project has established
            (ideas 66, 84) that gross is an exact lever with ~zero Sharpe content, so the
            natural blend confounds the mix with a gross change on the 4b CAGR/DD bars.
Tuned     : exactly 2 — f in {0.00, 0.25, 0.50, 0.75, 1.00} and the book in {v1,top20,ewall}.
            The sleeve's lookbacks (252/126/63, 60d vol) are canonical TSMOM constants
            carried over unchanged; the gate (200d, vol20<0.60), gross (75%), cadence
            (weekly) and costs (10 bps) are all held at the values the incumbent books
            already use.  Grid = 5 f x 3 books x 2 universes x 2 conventions = 60 points,
            ALL reported (f=0.00 and f=1.00 are the two controls: pure book, pure sleeve).
Execution : weekly rebalance, weights decided at close t applied at t+1 (engine), 10 bps
            per unit turnover.  Long only, no leverage.
Rule 8    : f chosen on 2009-2016 by in-sample Sharpe, evaluated on 2017-2026 untouched,
            per (universe, book, convention); OOS reported against the RULES v1 baseline
            and SPY on the same days.

KNOWN DATA CAVEAT (queue idea 38): data/prices*.csv are indexed on CALENDAR days after
2014-09-17 because BTC-USD is in the download, so post-2014 weekends appear as zero-return
rows.  That inflates row counts and deflates daily vol identically for every arm here,
including the baseline and SPY, so the CROSS-ARM comparisons below are apples-to-apples;
the absolute Sharpe levels are not trustworthy until idea 38 lands.

Deterministic, standalone:  python research/backtests/2026-09-04_ensemble-plus-momentum_C.py
"""
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
MACRO = ["SPY", "QQQ", "IWM", "EFA", "EEM", "TLT", "GLD", "DBC", "UUP"]
MOM_LAGS = (252, 126, 63)
VOL_WINDOW = 60
FGRID = [0.00, 0.25, 0.50, 0.75, 1.00]
SPLIT = "2017-01-01"
IS_END = "2016-12-31"
OUT = Path(__file__).with_suffix("")


# ---------------------------------------------------------------- sleeve (idea 18 B)
def _risk_parity(sub):
    vol = sub.pct_change().rolling(VOL_WINDOW).std()
    inv = 1.0 / vol.replace(0.0, np.nan)
    return inv.div(inv.sum(axis=1), axis=0)


def _vote_mom(sub):
    sig = [sub.shift(21) / sub.shift(MOM_LAGS[0]) - 1,
           sub / sub.shift(MOM_LAGS[1]) - 1,
           sub / sub.shift(MOM_LAGS[2]) - 1]
    return sum((s > 0).astype(float).where(s.notna()) for s in sig) / len(sig)


def sleeve_weights(px):
    """macro-trend-ensemble variant B at full size; zero outside the 9 macro ETFs."""
    sub = px[MACRO]
    w = (_vote_mom(sub) * _risk_parity(sub)).fillna(0.0)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[MACRO] = w
    return out


# ---------------------------------------------------------------- equity books
def book_v1(px):
    return rules_v1_weights(px)                       # top-5, 15% each, /sqrt(vol20)


def book_top20(px, n=20):
    """Idea 2's 4b KEEP-candidate: top-n composite WITHOUT the vol scaler, GROSS/n each."""
    s, above, vol20 = score(px, vol_scale=False)
    elig = s.where(above & (vol20 < 0.60))
    rank = elig.rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (GROSS / n)


def book_ewall(px):
    """Idea 10's EWall: equal-weight every eligible name, GROSS in total."""
    s, above, vol20 = score(px, vol_scale=False)
    elig = (above & (vol20 < 0.60) & s.notna()).astype(float)
    k = elig.sum(axis=1)
    return elig.div(k.where(k > 0), axis=0).fillna(0.0) * GROSS


BOOKS = {"v1": book_v1, "top20": book_top20, "ewall": book_ewall}


def blend(E, S, f, matched):
    """Natural blend, or the same blend rescaled per row to E's own gross."""
    w = (1 - f) * E + f * S
    if not matched:
        return w
    gE, gW = E.sum(axis=1), w.sum(axis=1)
    scale = (gE / gW.where(gW > 1e-12)).fillna(0.0)
    return w.mul(scale, axis=0)


# ---------------------------------------------------------------- metrics helpers
def stats(r):
    m = metrics(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"])


def full_row(r):
    h = len(r) // 2
    a, b = stats(r), stats(r.iloc[:h])
    c = stats(r.iloc[h:])
    o = stats(r.loc[SPLIT:])
    i = stats(r.loc[:IS_END])
    return dict(CAGR=a["CAGR"], Sharpe=a["Sharpe"], MaxDD=a["MaxDD"],
                H1=b["Sharpe"], H2=c["Sharpe"],
                IS_Sharpe=i["Sharpe"], OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"],
                OOS_MaxDD=o["MaxDD"])


def keep_4a(row, base):
    return bool(row["H1"] > base["H1"] and row["H2"] > base["H2"] and row["MaxDD"] >= base["MaxDD"])


def keep_4b(row, spy):
    return bool(row["H1"] > spy["H1"] and row["H2"] > spy["H2"] and row["OOS_Sharpe"] > spy["OOS_Sharpe"]
                and row["MaxDD"] >= 0.60 * spy["MaxDD"]        # both negative
                and row["CAGR"] >= 0.70 * spy["CAGR"])


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.3f}")


# ---------------------------------------------------------------- main
def run_universe(tag, px, records):
    start = px.index[260]
    print("=" * 100)
    print(f"### UNIVERSE {tag}: {px.shape[1]} tickers, {px.index[0].date()} -> {px.index[-1].date()}"
          f"  | eval from {start.date()}")
    missing = [t for t in MACRO if t not in px.columns]
    if missing:
        raise SystemExit(f"missing macro tickers in {tag}: {missing}")

    S = sleeve_weights(px)
    base_r = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
    spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
    base, spy = full_row(base_r), full_row(spy_r)
    ref = pd.DataFrame({"RULES v1 baseline": base, "SPY": spy}).T
    print("\nReference rows (same days, same costs):")
    print(fmt(ref))
    print(f"\n4b bars on this window: Sharpe > SPY H1 {spy['H1']:.3f} / H2 {spy['H2']:.3f} / "
          f"OOS {spy['OOS_Sharpe']:.3f} · MaxDD >= {0.60*spy['MaxDD']:.1%} · CAGR >= {0.70*spy['CAGR']:.2%}")

    for bname, bfn in BOOKS.items():
        E = bfn(px)
        for matched in (False, True):
            conv = "matched" if matched else "natural"
            rows = []
            for f in FGRID:
                w = blend(E, S, f, matched)
                res = backtest(px, w, cost_bps=COST_BPS, freq=FREQ)
                r = res["returns"].loc[start:]
                row = full_row(r)
                yrs = len(r) / 252
                row["Turn/yr"] = res["turnover"].loc[start:].sum() / yrs
                row["Gross"] = w.loc[start:].sum(axis=1).mean()
                row["4a"] = keep_4a(row, base)
                row["4b"] = keep_4b(row, spy)
                rows.append(dict(universe=tag, book=bname, conv=conv, f=f, **row))
                records.append(rows[-1])
            df = pd.DataFrame(rows).set_index("f")[
                ["Gross", "Turn/yr", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                 "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "4a", "4b"]]
            print(f"\n--- {tag} | book={bname} | blend={conv} | f = sleeve fraction "
                  f"(f=0 pure book, f=1 pure sleeve)")
            print(fmt(df))
    return base, spy, base_r, spy_r


def main():
    records = []
    refs = {}
    for tag, px in (("u56", load_universe()), ("broad", load_universe(broad=True))):
        base, spy, base_r, spy_r = run_universe(tag, px, records)
        refs[tag] = (base, spy, base_r, spy_r)

    G = pd.DataFrame(records)
    OUT.with_suffix(".grid.csv").write_text(G.to_csv(index=False))

    # ---------------------------------------------------------- rule 8 walk-forward
    print("\n" + "=" * 100)
    print("### PROTOCOL rule 8 — f chosen on 2009-2016 by IS Sharpe, 2017-2026 evaluated untouched\n")
    wf = []
    for (tag, bname, conv), sub in G.groupby(["universe", "book", "conv"], sort=False):
        pick = sub.loc[sub["IS_Sharpe"].idxmax()]
        base, spy, base_r, spy_r = refs[tag]
        wf.append(dict(universe=tag, book=bname, conv=conv, f_star=pick["f"],
                       IS_Sharpe=pick["IS_Sharpe"],
                       OOS_CAGR=pick["OOS_CAGR"], OOS_Sharpe=pick["OOS_Sharpe"],
                       OOS_MaxDD=pick["OOS_MaxDD"],
                       base_OOS_Sharpe=base["OOS_Sharpe"], base_OOS_CAGR=base["OOS_CAGR"],
                       base_OOS_MaxDD=base["OOS_MaxDD"],
                       spy_OOS_Sharpe=spy["OOS_Sharpe"], spy_OOS_CAGR=spy["OOS_CAGR"],
                       spy_OOS_MaxDD=spy["OOS_MaxDD"],
                       beats_base=bool(pick["OOS_Sharpe"] > base["OOS_Sharpe"]),
                       beats_spy=bool(pick["OOS_Sharpe"] > spy["OOS_Sharpe"]),
                       full_4a=bool(pick["4a"]), full_4b=bool(pick["4b"])))
    W = pd.DataFrame(wf)
    print(fmt(W.set_index(["universe", "book", "conv"])))
    OUT.with_suffix(".walkforward.csv").write_text(W.to_csv(index=False))

    # ---------------------------------------------------------- diversification test
    print("\n" + "=" * 100)
    print("### Is the blend more than the weighted average of its parts?")
    print("dSharpe(f) = Sharpe(blend f) - [(1-f)*Sharpe(f=0) + f*Sharpe(f=1)] ; >0 = real diversification\n")
    dv = []
    for (tag, bname, conv), sub in G.groupby(["universe", "book", "conv"], sort=False):
        s = sub.set_index("f")["Sharpe"]
        for f in FGRID[1:-1]:
            dv.append(dict(universe=tag, book=bname, conv=conv, f=f,
                           Sharpe=s[f], lin=(1 - f) * s[0.0] + f * s[1.0],
                           dSharpe=s[f] - ((1 - f) * s[0.0] + f * s[1.0])))
    D = pd.DataFrame(dv)
    print(fmt(D.set_index(["universe", "book", "conv", "f"])))
    print(f"\ndSharpe: mean {D['dSharpe'].mean():+.3f} · median {D['dSharpe'].median():+.3f} · "
          f"positive in {int((D['dSharpe'] > 0).sum())}/{len(D)} cells · "
          f"range [{D['dSharpe'].min():+.3f}, {D['dSharpe'].max():+.3f}]")
    OUT.with_suffix(".diversification.csv").write_text(D.to_csv(index=False))

    # ---------------------------------------------------------- correlation of the sleeves
    print("\n" + "=" * 100)
    print("### Correlation of daily returns between the sleeve and each book (eval window)\n")
    for tag, px in (("u56", load_universe()), ("broad", load_universe(broad=True))):
        start = px.index[260]
        S = sleeve_weights(px)
        sr = backtest(px, S, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        cols = {"sleeve": sr, "SPY": px["SPY"].pct_change().fillna(0).loc[start:]}
        for bname, bfn in BOOKS.items():
            cols[bname] = backtest(px, bfn(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        C = pd.DataFrame(cols).corr()
        print(f"--- {tag}")
        print(fmt(C))

    # ---------------------------------------------------------- year attribution
    print("\n" + "=" * 100)
    print("### Calendar-year returns: where does the sleeve pay and where does it cost?")
    print("(top20 = idea 2's standing 4b KEEP; +25% = the same book with f=0.25 natural blend)\n")
    for tag, px in (("u56", load_universe()), ("broad", load_universe(broad=True))):
        start = px.index[260]
        S, E = sleeve_weights(px), book_top20(px)
        cols = {
            "top20 (f=0)": backtest(px, E, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:],
            "top20 +25% sleeve": backtest(px, blend(E, S, 0.25, False), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:],
            "sleeve (f=1)": backtest(px, S, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:],
            "RULES v1": backtest(px, rules_v1_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:],
            "SPY": px["SPY"].pct_change().fillna(0).loc[start:],
        }
        Y = pd.DataFrame(cols).groupby(lambda d: d.year).apply(lambda x: (1 + x).prod() - 1)
        Y["sleeve effect"] = Y["top20 +25% sleeve"] - Y["top20 (f=0)"]
        print(f"--- {tag}")
        print(Y.to_string(float_format=lambda x: f"{x:+.1%}"))
        print()

    # ---------------------------------------------------------- cost ladder (control)
    print("=" * 100)
    print("### Cost sensitivity of the surviving arm (control, not a tuned parameter)")
    print("PROTOCOL fixes costs at 10 bps; idea 82 found the incumbent's cross-universe 4b margin")
    print("dies by 7.5 bps, so any successor has to be re-priced.\n")
    ladder = []
    for tag, px in (("u56", load_universe()), ("broad", load_universe(broad=True))):
        start = px.index[260]
        S, E = sleeve_weights(px), book_top20(px)
        spy = full_row(px["SPY"].pct_change().fillna(0).loc[start:])
        for c in (5, 10, 15, 20, 25):
            for f in (0.00, 0.25):
                r = backtest(px, blend(E, S, f, False), cost_bps=c, freq=FREQ)["returns"].loc[start:]
                row = full_row(r)
                ladder.append(dict(universe=tag, cost_bps=c, f=f, CAGR=row["CAGR"], Sharpe=row["Sharpe"],
                                   MaxDD=row["MaxDD"], H1=row["H1"], H2=row["H2"],
                                   OOS_Sharpe=row["OOS_Sharpe"], **{"4b": keep_4b(row, spy)}))
    L = pd.DataFrame(ladder)
    print(fmt(L.set_index(["universe", "cost_bps", "f"])))
    OUT.with_suffix(".costladder.csv").write_text(L.to_csv(index=False))

    # ---------------------------------------------------------- verdict census
    print("\n" + "=" * 100)
    n4a, n4b = int(G["4a"].sum()), int(G["4b"].sum())
    print(f"### CENSUS over all {len(G)} grid points: 4a passes {n4a}, 4b passes {n4b}")
    if n4a or n4b:
        print(fmt(G[G["4a"] | G["4b"]].set_index(["universe", "book", "conv", "f"])[
            ["Gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "4a", "4b"]]))
    # blend-only census (f strictly interior): does the IDEA, not its controls, ever pass?
    inner = G[(G["f"] > 0) & (G["f"] < 1)]
    print(f"\nInterior points only (the idea itself, f in {FGRID[1:-1]}): "
          f"{len(inner)} points, 4a {int(inner['4a'].sum())}, 4b {int(inner['4b'].sum())}")
    print(f"\nGrid written to {OUT.name}.grid.csv / .walkforward.csv / .diversification.csv")


if __name__ == "__main__":
    main()

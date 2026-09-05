#!/usr/bin/env python3
"""QUEUE idea 100 — sleeve-with-a-real-diversifier (cloud, 2026-09-04).

Question (as worded in QUEUE.md)
--------------------------------
"Idea 26's sleeve is 0.63-0.82 correlated with the equity books because 5 of its 9 assets
are equity ETFs.  Re-run the f-grid with the sleeve restricted to TLT/GLD/DBC/UUP (the
non-equity four) at the same inverse-vol risk parity: does a genuinely lower correlation
buy the same Sharpe convexity at less CAGR?"

Idea 26's finding was a confirmed mechanism with an insufficient size: dSharpe against the
linear blend of the parts was positive in 36/36 interior cells (mean +0.052), but CAGR fell
almost exactly linearly toward the sleeve's own 5.0%, so 4b's CAGR floor bound by f=0.50.
Its diagnosis was that the sleeve is a lower-return version of the same long-equity trend
exposure.  If that diagnosis is right, cutting the 5 equity ETFs out should raise the
convexity per unit of CAGR given up.  If the convexity instead *falls*, the diversification
in idea 26 was equity beta timing, not diversification, and the whole sleeve family is done.

Design (PROTOCOL rules 1-9)
---------------------------
Panels    : `baseline.load_universe()` (56) and `load_universe(broad=True)` (136).  All 9
            macro ETFs are in both.  SURVIVORSHIP: current constituents; levels biased up.
Sleeves   : S9 — idea 18 variant B / idea 26's sleeve, verbatim: vote in {0,1/3,2/3,1} on
                 the signs of {12-1, 6m, 3m} times inverse-60d-vol risk parity over
                 SPY QQQ IWM EFA EEM TLT GLD DBC UUP, row-normalised to 1.0.  CONTROL —
                 this run must reproduce idea 26's numbers before its own are readable.
            S4 — the same construction restricted to TLT GLD DBC UUP (the non-equity four).
Books E   : v1 (live RULES v1 top-5), top20 (idea 2's standing 4b KEEP), ewall (idea 10's
            EWall).  Reported, never selected on — the book is not a tuned parameter here.
Blend     : natural  w = (1-f)*E + f*S   ;  matched  = the same rescaled per row to E's own
            gross.  Both reported (ideas 66/84: gross is an exact lever with ~0 Sharpe
            content, so the natural blend confounds the mix with an exposure change).
Tuned     : exactly 2 — f in {0.00,0.25,0.50,0.75,1.00} and the sleeve in {S9,S4}.
            Lookbacks (252/126/63, 60d vol), gate, gross (75%), cadence (weekly) and costs
            (10 bps) are all held at the incumbent books' values.
            Grid = 5 f x 2 sleeves x 3 books x 2 universes x 2 conventions = 120 points,
            ALL reported (f=0 and f=1 are the controls: pure book, pure sleeve).
Rule 8    : f chosen on 2009-2016 by IS Sharpe, 2017-2026 evaluated untouched, per
            (universe, book, convention, sleeve); OOS reported vs RULES v1 and SPY.
Extra bars (idea 26's three objections, applied to this run's own survivors):
            - correlation of the sleeve to each book (the idea's own premise);
            - dSharpe against the linear blend, and CAGR given up per unit of it;
            - calendar-year attribution + leave-one-year-out (idea 98's proposed bar);
            - 5/10/15/20/25 bps cost ladder (idea 82: the incumbent's window is 5-7.5 bps).

KNOWN DATA CAVEAT (queue idea 38): data/prices*.csv are indexed on CALENDAR days after
2014-09-17 because BTC-USD is in the download, so post-2014 weekends are zero-return rows.
It hits every arm, the baseline and SPY identically — cross-arm comparisons are
apples-to-apples; absolute Sharpe levels wait on idea 38.

Deterministic, standalone:
    python research/backtests/2026-09-04_sleeve-with-a-real-diversifier_cloud.py
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
MACRO9 = ["SPY", "QQQ", "IWM", "EFA", "EEM", "TLT", "GLD", "DBC", "UUP"]
MACRO4 = ["TLT", "GLD", "DBC", "UUP"]
SLEEVES = {"S9": MACRO9, "S4": MACRO4}
MOM_LAGS = (252, 126, 63)
VOL_WINDOW = 60
FGRID = [0.00, 0.25, 0.50, 0.75, 1.00]
SPLIT = "2017-01-01"
IS_END = "2016-12-31"
OUT = Path(__file__).with_suffix("")


# ---------------------------------------------------------------- sleeves
def _risk_parity(sub):
    vol = sub.pct_change().rolling(VOL_WINDOW).std()
    inv = 1.0 / vol.replace(0.0, np.nan)
    return inv.div(inv.sum(axis=1), axis=0)


def _vote_mom(sub):
    sig = [sub.shift(21) / sub.shift(MOM_LAGS[0]) - 1,
           sub / sub.shift(MOM_LAGS[1]) - 1,
           sub / sub.shift(MOM_LAGS[2]) - 1]
    return sum((s > 0).astype(float).where(s.notna()) for s in sig) / len(sig)


def sleeve_weights(px, assets):
    """idea 18 variant B, restricted to `assets`; zero everywhere else."""
    sub = px[assets]
    w = (_vote_mom(sub) * _risk_parity(sub)).fillna(0.0)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[assets] = w
    return out


# ---------------------------------------------------------------- equity books
def book_v1(px):
    return rules_v1_weights(px)


def book_top20(px, n=20):
    s, above, vol20 = score(px, vol_scale=False)
    rank = s.where(above & (vol20 < 0.60)).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (GROSS / n)


def book_ewall(px):
    s, above, vol20 = score(px, vol_scale=False)
    elig = (above & (vol20 < 0.60) & s.notna()).astype(float)
    k = elig.sum(axis=1)
    return elig.div(k.where(k > 0), axis=0).fillna(0.0) * GROSS


BOOKS = {"v1": book_v1, "top20": book_top20, "ewall": book_ewall}


def blend(E, S, f, matched):
    w = (1 - f) * E + f * S
    if not matched:
        return w
    gE, gW = E.sum(axis=1), w.sum(axis=1)
    return w.mul((gE / gW.where(gW > 1e-12)).fillna(0.0), axis=0)


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


# ---------------------------------------------------------------- main grid
def run_universe(tag, px, records):
    start = px.index[260]
    print("=" * 115)
    print(f"### UNIVERSE {tag}: {px.shape[1]} tickers, {px.index[0].date()} -> {px.index[-1].date()}"
          f" | eval from {start.date()}")
    for name, assets in SLEEVES.items():
        missing = [t for t in assets if t not in px.columns]
        if missing:
            raise SystemExit(f"missing sleeve tickers in {tag}: {missing}")

    base_r = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
    spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
    base, spy = full_row(base_r), full_row(spy_r)
    print("\nReference rows (same days, same costs):")
    print(fmt(pd.DataFrame({"RULES v1 baseline": base, "SPY": spy}).T))
    print(f"\n4b bars: Sharpe > SPY H1 {spy['H1']:.3f} / H2 {spy['H2']:.3f} / OOS {spy['OOS_Sharpe']:.3f}"
          f" · MaxDD >= {0.60 * spy['MaxDD']:.1%} · CAGR >= {0.70 * spy['CAGR']:.2%}")

    for sname, assets in SLEEVES.items():
        S = sleeve_weights(px, assets)
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
                    row["Turn/yr"] = res["turnover"].loc[start:].sum() / (len(r) / 252)
                    row["Gross"] = w.loc[start:].sum(axis=1).mean()
                    row["4a"] = keep_4a(row, base)
                    row["4b"] = keep_4b(row, spy)
                    rows.append(dict(universe=tag, sleeve=sname, book=bname, conv=conv, f=f, **row))
                    records.append(rows[-1])
                df = pd.DataFrame(rows).set_index("f")[
                    ["Gross", "Turn/yr", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                     "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "4a", "4b"]]
                print(f"\n--- {tag} | sleeve={sname} | book={bname} | blend={conv} "
                      f"(f=0 pure book, f=1 pure sleeve)")
                print(fmt(df))
    return base, spy


def main():
    universes = {"u56": load_universe(), "broad": load_universe(broad=True)}
    records, refs = [], {}
    for tag, px in universes.items():
        refs[tag] = run_universe(tag, px, records)
    G = pd.DataFrame(records)
    G.to_csv(OUT.with_suffix(".grid.csv"), index=False)

    # ---------------------------------------------------------- (1) the premise: correlation
    print("\n" + "=" * 115)
    print("### (1) PREMISE — daily-return correlation of each sleeve to each book (eval window)")
    print("The idea claims S4 is a genuine diversifier where S9 (0.63-0.82 in idea 26) is not.\n")
    corr_rows = []
    for tag, px in universes.items():
        start = px.index[260]
        cols = {"SPY": px["SPY"].pct_change().fillna(0).loc[start:]}
        for sname, assets in SLEEVES.items():
            cols[sname] = backtest(px, sleeve_weights(px, assets), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        for bname, bfn in BOOKS.items():
            cols[bname] = backtest(px, bfn(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        C = pd.DataFrame(cols).corr()
        print(f"--- {tag}")
        print(fmt(C))
        for sname in SLEEVES:
            for bname in list(BOOKS) + ["SPY"]:
                corr_rows.append(dict(universe=tag, sleeve=sname, book=bname, corr=C.loc[sname, bname]))
        print()
    R = pd.DataFrame(corr_rows)
    R.to_csv(OUT.with_suffix(".correlation.csv"), index=False)
    piv = R.pivot_table(index=["universe", "book"], columns="sleeve", values="corr")
    piv["S4 - S9"] = piv["S4"] - piv["S9"]
    print(fmt(piv))
    print(f"\nS9 to the 3 books: {R[(R.sleeve=='S9') & (R.book!='SPY')]['corr'].min():.3f}"
          f"..{R[(R.sleeve=='S9') & (R.book!='SPY')]['corr'].max():.3f}   "
          f"S4 to the 3 books: {R[(R.sleeve=='S4') & (R.book!='SPY')]['corr'].min():.3f}"
          f"..{R[(R.sleeve=='S4') & (R.book!='SPY')]['corr'].max():.3f}")

    # ---------------------------------------------------------- (2) convexity per unit of CAGR
    print("\n" + "=" * 115)
    print("### (2) CONVEXITY — dSharpe vs the linear blend of the parts, and what it costs")
    print("dSharpe(f) = Sharpe(f) - [(1-f)Sharpe(0) + f Sharpe(1)] ; dCAGR(f) = CAGR(f) - CAGR(0)")
    print("The idea's question is whether S4 buys the same dSharpe at less dCAGR.\n")
    dv = []
    for (tag, sname, bname, conv), sub in G.groupby(["universe", "sleeve", "book", "conv"], sort=False):
        s = sub.set_index("f")["Sharpe"]
        c = sub.set_index("f")["CAGR"]
        for f in FGRID[1:-1]:
            lin = (1 - f) * s[0.0] + f * s[1.0]
            dv.append(dict(universe=tag, sleeve=sname, book=bname, conv=conv, f=f,
                           Sharpe=s[f], dSharpe=s[f] - lin, dCAGR=c[f] - c[0.0],
                           # dSharpe bought per PERCENTAGE POINT of CAGR surrendered vs f=0
                           conv_per_pp=(s[f] - lin) / max(100 * (c[0.0] - c[f]), 1e-9)))
    D = pd.DataFrame(dv)
    D.to_csv(OUT.with_suffix(".convexity.csv"), index=False)
    print(fmt(D.groupby(["sleeve", "f"]).agg(
        n=("dSharpe", "size"), dSharpe_mean=("dSharpe", "mean"), dSharpe_min=("dSharpe", "min"),
        dSharpe_max=("dSharpe", "max"), pos=("dSharpe", lambda x: int((x > 0).sum())),
        dCAGR_mean=("dCAGR", "mean"), dSharpe_per_pp_CAGR=("conv_per_pp", "median"))))
    for sname in SLEEVES:
        sub = D[D.sleeve == sname]
        print(f"\n{sname}: dSharpe mean {sub.dSharpe.mean():+.3f}, positive in "
              f"{int((sub.dSharpe > 0).sum())}/{len(sub)}, range [{sub.dSharpe.min():+.3f}, "
              f"{sub.dSharpe.max():+.3f}]; dCAGR mean {sub.dCAGR.mean():+.2%}; "
              f"median dSharpe per pp of CAGR surrendered {sub.conv_per_pp.median():.4f}")

    # ---------------------------------------------------------- (3) rule 8
    print("\n" + "=" * 115)
    print("### (3) PROTOCOL rule 8 — f chosen on 2009-2016 by IS Sharpe, 2017-2026 untouched\n")
    wf = []
    for (tag, sname, bname, conv), sub in G.groupby(["universe", "sleeve", "book", "conv"], sort=False):
        pick = sub.loc[sub["IS_Sharpe"].idxmax()]
        anchor = sub[sub.f == 0.0].iloc[0]
        base, spy = refs[tag]
        wf.append(dict(universe=tag, sleeve=sname, book=bname, conv=conv, f_star=pick["f"],
                       IS_Sharpe=pick["IS_Sharpe"],
                       IS_monotone_down=bool(sub.sort_values("f")["IS_Sharpe"].diff().dropna().le(0).all()),
                       OOS_Sharpe_at_fstar=pick["OOS_Sharpe"], OOS_Sharpe_anchor=anchor["OOS_Sharpe"],
                       best_OOS_in_grid=sub["OOS_Sharpe"].max(),
                       f_best_OOS=sub.loc[sub["OOS_Sharpe"].idxmax(), "f"],
                       regret=pick["OOS_Sharpe"] - sub["OOS_Sharpe"].max(),
                       spy_OOS=spy["OOS_Sharpe"], base_OOS=base["OOS_Sharpe"],
                       full_4b=bool(pick["4b"])))
    W = pd.DataFrame(wf)
    print(fmt(W.set_index(["universe", "sleeve", "book", "conv"])))
    W.to_csv(OUT.with_suffix(".walkforward.csv"), index=False)
    print(f"\nrule 8 picks f=0 (no sleeve) in {int((W.f_star == 0).sum())}/{len(W)} cells; "
          f"IS Sharpe monotone decreasing in f in {int(W.IS_monotone_down.sum())}/{len(W)}; "
          f"mean regret {W.regret.mean():+.3f}")

    # ---------------------------------------------------------- (4) census + survivors
    print("\n" + "=" * 115)
    inner = G[(G.f > 0) & (G.f < 1)]
    print(f"### (4) CENSUS over all {len(G)} points: 4a {int(G['4a'].sum())}, 4b {int(G['4b'].sum())}")
    print(f"Interior points only (the idea itself): {len(inner)}, 4a {int(inner['4a'].sum())}, "
          f"4b {int(inner['4b'].sum())}")
    for sname in SLEEVES:
        sub = inner[inner.sleeve == sname]
        print(f"  {sname}: 4a {int(sub['4a'].sum())}/{len(sub)}, 4b {int(sub['4b'].sum())}/{len(sub)}")
    if int(inner["4b"].sum()):
        print("\nInterior points passing 4b:")
        print(fmt(inner[inner["4b"]].set_index(["universe", "sleeve", "book", "conv", "f"])[
            ["Gross", "Turn/yr", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "4a"]]))
        # cross-universe / cross-convention survivors: the bar idea 26's by-product had to clear
        k = inner[inner["4b"]].groupby(["sleeve", "book", "f"]).size()
        print("\n(sleeve, book, f) cells passing 4b in all 4 (universe x convention) combinations:")
        print(k[k == 4] if (k == 4).any() else "  none")

    # ---------------------------------------------------------- (5) year attribution + LOYO
    print("\n" + "=" * 115)
    print("### (5) YEAR ATTRIBUTION and LEAVE-ONE-YEAR-OUT (idea 98's proposed bar)")
    print("Idea 26's by-product died here: its sleeve contribution was negative in 17/18 years.\n")
    loyo = []
    for tag, px in universes.items():
        start = px.index[260]
        E = book_top20(px)
        cols = {"top20 (f=0)": backtest(px, E, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]}
        for sname, assets in SLEEVES.items():
            S = sleeve_weights(px, assets)
            cols[f"top20 +25% {sname}"] = backtest(px, blend(E, S, 0.25, False), cost_bps=COST_BPS,
                                                   freq=FREQ)["returns"].loc[start:]
            cols[f"{sname} alone"] = backtest(px, S, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        cols["SPY"] = px["SPY"].pct_change().fillna(0).loc[start:]
        Y = pd.DataFrame(cols).groupby(lambda d: d.year).apply(lambda x: (1 + x).prod() - 1)
        for sname in SLEEVES:
            Y[f"{sname} effect"] = Y[f"top20 +25% {sname}"] - Y["top20 (f=0)"]
        print(f"--- {tag}")
        print(Y.to_string(float_format=lambda x: f"{x:+.1%}"))
        for sname in SLEEVES:
            e = Y[f"{sname} effect"]
            print(f"    {sname}: contribution positive in {int((e > 0).sum())}/{len(e)} years, "
                  f"best year {e.idxmax()} {e.max():+.1%}, worst {e.idxmin()} {e.min():+.1%}")
        # leave-one-year-out on Sharpe, for the f=0.25 arms and the anchor
        for label in ["top20 (f=0)"] + [f"top20 +25% {s}" for s in SLEEVES]:
            r = cols[label]
            full = metrics(r)["Sharpe"]
            drops = {y: metrics(r[r.index.year != y])["Sharpe"] for y in sorted(set(r.index.year))}
            worst_y = min(drops, key=drops.get)
            loyo.append(dict(universe=tag, arm=label, Sharpe=full, worst_drop_year=worst_y,
                             Sharpe_ex_worst=drops[worst_y], delta=drops[worst_y] - full))
        print()
    LY = pd.DataFrame(loyo)
    print(fmt(LY.set_index(["universe", "arm"])))
    LY.to_csv(OUT.with_suffix(".loyo.csv"), index=False)

    # ---------------------------------------------------------- (5b) delete the sleeve's OWN best year
    print("\n" + "=" * 115)
    print("### (5b) Does the sleeve still earn its place with 2022 deleted?")
    print("2022 is the only year either sleeve contributes materially. The bar: dSharpe(blend - anchor)")
    print("must stay positive on the sample with 2022 removed, or the overlay is a one-year artefact.\n")
    ex = []
    for tag, px in universes.items():
        start = px.index[260]
        E = book_top20(px)
        anchor = backtest(px, E, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        for sname, assets in SLEEVES.items():
            S = sleeve_weights(px, assets)
            for f in (0.25, 0.50):
                for matched in (False, True):
                    r = backtest(px, blend(E, S, f, matched), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
                    m_all = metrics(r)["Sharpe"] - metrics(anchor)["Sharpe"]
                    k = r.index.year != 2022
                    m_ex = metrics(r[k])["Sharpe"] - metrics(anchor[k])["Sharpe"]
                    ex.append(dict(universe=tag, sleeve=sname, f=f,
                                   conv="matched" if matched else "natural",
                                   dSharpe_full=m_all, dSharpe_ex2022=m_ex, shrink=m_ex - m_all))
    X = pd.DataFrame(ex)
    print(fmt(X.set_index(["universe", "sleeve", "f", "conv"])))
    X.to_csv(OUT.with_suffix(".ex2022.csv"), index=False)
    for sname in SLEEVES:
        s = X[X.sleeve == sname]
        print(f"{sname}: dSharpe vs anchor stays positive ex-2022 in "
              f"{int((s.dSharpe_ex2022 > 0).sum())}/{len(s)} cells "
              f"(full-sample positive in {int((s.dSharpe_full > 0).sum())}/{len(s)}); "
              f"mean shrink {s.shrink.mean():+.3f}")

    # ---------------------------------------------------------- (5c) gross diagnostic
    print("\n" + "=" * 115)
    print("### (5c) DIAGNOSTIC (not a tuned parameter, not a KEEP claim): the binding 4b bar")
    print("for every S4 arm is the CAGR floor. Ideas 66/84 established gross is an exact lever with")
    print("~zero Sharpe content, so this ladder reports what re-grossing the rule-8 pick would cost")
    print("in drawdown. Any candidate built this way needs its own pre-registered run.")
    print("g=1.25 is LEVERAGE, which PROTOCOL rule 2 forbids unless the idea says so; it is shown")
    print("only to locate where the CAGR floor is cleared, never as an admissible book.\n")
    gl = []
    for tag, px in universes.items():
        start = px.index[260]
        spy = full_row(px["SPY"].pct_change().fillna(0).loc[start:])
        E = book_top20(px)
        for sname, assets in SLEEVES.items():
            S = sleeve_weights(px, assets)
            w0 = blend(E, S, 0.50, False)
            g0 = w0.sum(axis=1)
            for g in (0.75, 0.85, 1.00, 1.25):
                w = w0.mul((g / g0.where(g0 > 1e-12)).fillna(0.0), axis=0)
                r = backtest(px, w, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
                row = full_row(r)
                gl.append(dict(universe=tag, sleeve=sname, target_gross=g, CAGR=row["CAGR"],
                               Sharpe=row["Sharpe"], MaxDD=row["MaxDD"], H1=row["H1"], H2=row["H2"],
                               OOS_Sharpe=row["OOS_Sharpe"],
                               CAGR_floor=0.70 * spy["CAGR"], DD_cap=0.60 * spy["MaxDD"],
                               **{"4b": keep_4b(row, spy)}))
    GL = pd.DataFrame(gl)
    print(fmt(GL.set_index(["universe", "sleeve", "target_gross"])))
    GL.to_csv(OUT.with_suffix(".grossladder.csv"), index=False)

    # ---------------------------------------------------------- (6) cost ladder
    print("\n" + "=" * 115)
    print("### (6) COST LADDER (control, not a tuned parameter) — idea 82: the incumbent's")
    print("cross-universe 4b window is 5-7.5 bps, so any successor has to be re-priced.\n")
    ladder = []
    for tag, px in universes.items():
        start = px.index[260]
        spy = full_row(px["SPY"].pct_change().fillna(0).loc[start:])
        E = book_top20(px)
        for sname, assets in SLEEVES.items():
            S = sleeve_weights(px, assets)
            for c in (5, 10, 15, 20, 25):
                for f in (0.00, 0.25, 0.50):
                    r = backtest(px, blend(E, S, f, False), cost_bps=c, freq=FREQ)["returns"].loc[start:]
                    row = full_row(r)
                    ladder.append(dict(universe=tag, sleeve=sname, cost_bps=c, f=f, CAGR=row["CAGR"],
                                       Sharpe=row["Sharpe"], MaxDD=row["MaxDD"], H1=row["H1"], H2=row["H2"],
                                       OOS_Sharpe=row["OOS_Sharpe"], **{"4b": keep_4b(row, spy)}))
    L = pd.DataFrame(ladder)
    print(fmt(L.set_index(["universe", "sleeve", "cost_bps", "f"])))
    L.to_csv(OUT.with_suffix(".costladder.csv"), index=False)
    print(f"\nWritten: {OUT.name}.grid.csv / .correlation.csv / .convexity.csv / "
          f".walkforward.csv / .loyo.csv / .ex2022.csv / .grossladder.csv / .costladder.csv")


if __name__ == "__main__":
    main()

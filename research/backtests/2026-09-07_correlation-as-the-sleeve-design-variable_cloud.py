#!/usr/bin/env python3
"""Idea 103 (cloud, 2026-09-07): correlation-as-the-sleeve-design-variable.

QUEUE TEXT: "idea 100 found convexity per pp of CAGR (0.090 vs 0.031) tracks sleeve-to-book
correlation (-0.011..0.212 vs 0.626..0.820) across exactly two sleeves.  Build the curve
rather than the pair: sweep sleeves spanning correlation ~-0.2 to +0.8 by adding equity ETFs
back one at a time, and regress convexity-per-pp on realised correlation.  Is the
relationship monotone, and where does it stop paying?"

CONSTRUCTION (idea 100's, verbatim -- this run must reproduce its S4 and S9 rows first)
--------------------------------------------------------------------------------------
Sleeve  = vote in {0,1/3,2/3,1} on the signs of {12-1, 6m, 3m} times inverse-60d-vol risk
          parity over the sleeve's assets, row-normalised.
Books   = v1 (live RULES v1 top-5), top20, ewall -- reported, never selected on.
Blend   = natural w = (1-f)E + fS ; matched = the same rescaled per row to E's own gross.
Convexity  dSharpe(f) = Sharpe(f) - [(1-f)Sharpe(0) + f Sharpe(1)]
Cost of it dCAGR(f)   = CAGR(0) - CAGR(f)  (pp given up vs the pure book)
The statistic         conv_per_pp = dSharpe(f) / (100 * dCAGR(f))

THE LADDER (the curve the queue asked for).  Start from S4 = TLT GLD DBC UUP and add the
five equity ETFs back ONE AT A TIME, in the record's own list order, to S9:
    S4 -> +SPY -> +QQQ -> +IWM -> +EFA -> +EEM = S9
and, as a REPORTED ROBUSTNESS PATH (not a third tuned parameter), the reverse add order
    S4 -> +EEM -> +EFA -> +IWM -> +QQQ -> +SPY = S9
which shares both endpoints.  If the curve is a function of CORRELATION it must not care
which path reached a given correlation; if the two paths disagree at matched correlation,
the queue's variable is the wrong one.

THE NULL.  SCASH -- a sleeve of nothing at all, i.e. f held in cash.  Its correlation to
every book is exactly 0 by construction, so it is the zero-correlation point the curve must
beat to mean anything, and it is the same instrument as the gross dial (ideas 351/367's
NUMERAIRE clause).  Under the MATCHED convention SCASH is algebraically the book itself,
which is used below as a reproduction gate (dSharpe must be 0.000e+00).

TUNED PARAMETERS: exactly 2 -- f in {0,0.25,0.50,0.75,1.00} and the sleeve (11 of them).
Everything else (lookbacks 252/126/63, 60d vol, gross 0.75, weekly cadence, 10 bps) is held
at the incumbent books' values.  Grid = 11 sleeves x 3 books x 2 universes x 2 conventions
x 5 f = 660 points, ALL reported.

RULE 8: (sleeve, f) chosen on 2009-2016 by IS Sharpe, 2017-2026 read ONCE, per (universe,
book, convention).  OOS CAGR/Sharpe/MaxDD reported against RULES v2 (live baseline), RULES
v1 (idea 100's comparand) and SPY.  Both KEEP paths reported for every point.

SURVIVORSHIP: both panels are current constituents (levels biased up); the sleeve ETFs are
survivors by construction.  No small-cap panel here -- the sleeve assets are not in it.

Deterministic, standalone, offline:
    python3 research/backtests/2026-09-07_correlation-as-the-sleeve-design-variable_cloud.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
sys.path.insert(0, str(REPO / "products" / "backtester"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa
from engine import backtest, metrics  # noqa

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 800)

COST_BPS, FREQ, GROSS = 10, "W", 0.75
MOM_LAGS, VOL_WINDOW = (252, 126, 63), 60
FGRID = [0.00, 0.25, 0.50, 0.75, 1.00]
SPLIT, IS_END = "2017-01-01", "2016-12-31"
CORE4 = ["TLT", "GLD", "DBC", "UUP"]
FWD = ["SPY", "QQQ", "IWM", "EFA", "EEM"]          # the record's own list order
REV = ["EEM", "EFA", "IWM", "QQQ", "SPY"]
OUT = Path(__file__).with_suffix("")


def build_ladder():
    """11 sleeves: the cash null, the 4-asset core, both add paths, the shared S9 endpoint."""
    L = {"SCASH": [], "S4": list(CORE4)}
    for i, t in enumerate(FWD[:-1], start=1):                 # S5f..S8f
        L[f"S{4+i}f"] = CORE4 + FWD[:i]
    for i, t in enumerate(REV[:-1], start=1):                 # S5r..S8r
        L[f"S{4+i}r"] = CORE4 + REV[:i]
    L["S9"] = CORE4 + FWD                                     # shared endpoint of both paths
    return L


SLEEVES = build_ladder()


# ---------------------------------------------------------------- sleeves / books
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
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    if not assets:                                            # SCASH: hold nothing
        return out
    sub = px[assets]
    out[assets] = (_vote_mom(sub) * _risk_parity(sub)).fillna(0.0)
    return out


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


# ---------------------------------------------------------------- metrics
def stats(r):
    m = metrics(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"])


def full_row(r):
    h = len(r) // 2
    a, b, c = stats(r), stats(r.iloc[:h]), stats(r.iloc[h:])
    o, i = stats(r.loc[SPLIT:]), stats(r.loc[:IS_END])
    return dict(CAGR=a["CAGR"], Sharpe=a["Sharpe"], MaxDD=a["MaxDD"], H1=b["Sharpe"], H2=c["Sharpe"],
                IS_Sharpe=i["Sharpe"], IS_CAGR=i["CAGR"],
                OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"])


def keep_4a(row, base):
    return bool(row["H1"] > base["H1"] and row["H2"] > base["H2"] and row["MaxDD"] >= base["MaxDD"])


def keep_4b(row, spy):
    return bool(row["H1"] > spy["H1"] and row["H2"] > spy["H2"] and row["OOS_Sharpe"] > spy["OOS_Sharpe"]
                and row["MaxDD"] >= 0.60 * spy["MaxDD"] and row["CAGR"] >= 0.70 * spy["CAGR"])


def spearman(a, b):
    a, b = pd.Series(np.asarray(a, float)), pd.Series(np.asarray(b, float))
    ok = a.notna() & b.notna()
    if ok.sum() < 3:
        return np.nan
    return float(np.corrcoef(a[ok].rank(), b[ok].rank())[0, 1])


def ols(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    if len(x) < 3:
        return np.nan, np.nan, np.nan, 0
    b = np.polyfit(x, y, 1)
    yh = np.polyval(b, x)
    ss = ((y - y.mean()) ** 2).sum()
    r2 = 1 - ((y - yh) ** 2).sum() / ss if ss > 0 else np.nan
    return float(b[0]), float(b[1]), float(r2), int(len(x))


# ---------------------------------------------------------------- main
def main():
    print("SLEEVE LADDER (all 11, both add paths, shared endpoints S4 and S9):")
    for k, v in SLEEVES.items():
        print(f"  {k:6s} n={len(v)}  {v if v else '(cash)'}")

    universes = {"u56": load_universe(), "broad": load_universe(broad=True)}
    records, corr_rows, refs = [], [], {}

    for tag, px in universes.items():
        start = px.index[260]
        for name, assets in SLEEVES.items():
            miss = [t for t in assets if t not in px.columns]
            if miss:
                raise SystemExit(f"missing sleeve tickers in {tag}: {miss}")

        base_r = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        v2_r = backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
        base, v2, spy = full_row(base_r), full_row(v2_r), full_row(spy_r)
        refs[tag] = (base, v2, spy)
        print("\n" + "=" * 118)
        print(f"### {tag}: {px.shape[1]} tickers, {px.index[0].date()} -> {px.index[-1].date()}, eval from {start.date()}")
        print(pd.DataFrame({"RULES v1": base, "RULES v2 (live)": v2, "SPY": spy}).T.to_string(
            float_format=lambda x: f"{x:.4f}"))
        print(f"4b bars: H1>{spy['H1']:.4f} H2>{spy['H2']:.4f} OOS>{spy['OOS_Sharpe']:.4f} "
              f"|MaxDD|<={abs(0.60*spy['MaxDD']):.2%} CAGR>={0.70*spy['CAGR']:.2%}")

        # sleeve return series + correlations to each book
        S_w = {s: sleeve_weights(px, a) for s, a in SLEEVES.items()}
        S_r = {s: backtest(px, w, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:] for s, w in S_w.items()}
        B_w = {b: fn(px) for b, fn in BOOKS.items()}
        B_r = {b: backtest(px, w, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:] for b, w in B_w.items()}
        for s in SLEEVES:
            for b in list(BOOKS) + ["SPY"]:
                other = B_r[b] if b in B_r else spy_r
                c = 0.0 if s == "SCASH" else float(pd.concat([S_r[s], other], axis=1).corr().iloc[0, 1])
                corr_rows.append(dict(universe=tag, sleeve=s, book=b, n_assets=len(SLEEVES[s]), corr=c))

        for sname in SLEEVES:
            for bname in BOOKS:
                for matched in (False, True):
                    conv = "matched" if matched else "natural"
                    for f in FGRID:
                        w = blend(B_w[bname], S_w[sname], f, matched)
                        res = backtest(px, w, cost_bps=COST_BPS, freq=FREQ)
                        r = res["returns"].loc[start:]
                        row = full_row(r)
                        row["Turn_yr"] = res["turnover"].loc[start:].sum() / (len(r) / 252)
                        row["Gross"] = float(w.loc[start:].sum(axis=1).mean())
                        row["p4a"] = keep_4a(row, v2)
                        row["p4a_v1"] = keep_4a(row, base)
                        row["p4b"] = keep_4b(row, spy)
                        records.append(dict(universe=tag, sleeve=sname, book=bname, conv=conv,
                                            n_assets=len(SLEEVES[sname]), f=f, **row))
        print(f"  {len(SLEEVES)} sleeves x {len(BOOKS)} books x 2 conventions x {len(FGRID)} f = "
              f"{len(SLEEVES)*len(BOOKS)*2*len(FGRID)} points done")

    G = pd.DataFrame(records)
    R = pd.DataFrame(corr_rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    R.to_csv(f"{OUT}.correlation.csv", index=False)

    # ------------------------------------------------------------ gates
    print("\n" + "=" * 118)
    print("### REPRODUCTION GATES")
    g1 = G[(G.sleeve == "SCASH") & (G.conv == "matched")]
    piv = g1.pivot_table(index=["universe", "book"], columns="f", values="Sharpe")
    err = float((piv.max(axis=1) - piv.min(axis=1)).abs().max())
    print(f"  (a) MATCHED cash sleeve is algebraically the book: max Sharpe spread across f = "
          f"{err:.3e}  {'PASS' if err < 1e-9 else 'FAIL'}")
    print("  (b) idea 100's published S4 / S9 rows (u56 top20, 10 bps, weekly):")
    for sn, fv, conv, want in [("S4", 0.25, "natural", "10.2% / 1.14 / -14.2% / 1.11 / 1.18"),
                               ("S4", 0.25, "matched", "10.8% / 1.14 / -14.6% / 1.13 / 1.16"),
                               ("S4", 0.50, "natural", " 7.7% / 1.19 / -10.0% / 1.10 / 1.27")]:
        q = G[(G.universe == "u56") & (G.book == "top20") & (G.sleeve == sn) & (G.f == fv) & (G.conv == conv)]
        if len(q):
            q = q.iloc[0]
            print(f"      {sn} f={fv} {conv:8s} -> {q.CAGR:.1%} / {q.Sharpe:.2f} / {q.MaxDD:.1%} / "
                  f"{q.H1:.2f} / {q.H2:.2f}   (published {want})")
    print("  (c) S9 standalone (f=1.00, u56, natural) reproduces idea 26 / idea 100's control:")
    q = G[(G.universe == "u56") & (G.book == "top20") & (G.sleeve == "S9") & (G.f == 1.0) & (G.conv == "natural")]
    if len(q):
        q = q.iloc[0]
        print(f"      {q.CAGR:.1%} / {q.Sharpe:.2f} / {q.MaxDD:.1%} / {q.H1:.2f} / {q.H2:.2f}   "
              f"(published 5.0% / 0.87 / -10.1% / 0.76 / 0.98)")

    # ------------------------------------------------------------ (1) the correlation ladder
    print("\n" + "=" * 118)
    print("### (1) THE CORRELATION LADDER — realised daily-return corr(sleeve, book), eval window")
    P = R[R.book != "SPY"].pivot_table(index=["sleeve", "n_assets"], columns=["universe", "book"], values="corr")
    P["MEAN"] = P.mean(axis=1)
    print(P.sort_values("MEAN").to_string(float_format=lambda x: f"{x:.3f}"))
    print(f"\n  Span achieved: {P['MEAN'].min():+.3f} .. {P['MEAN'].max():+.3f} "
          f"(queue asked for ~-0.2 .. +0.8)")

    # ------------------------------------------------------------ (2) convexity per pp
    print("\n" + "=" * 118)
    print("### (2) CONVEXITY per pp of CAGR, by sleeve (idea 100's statistic, unchanged)")
    dv = []
    cmap = {(r.universe, r.sleeve, r.book): r.corr for r in R.itertuples()}
    for (tag, sname, bname, conv), sub in G.groupby(["universe", "sleeve", "book", "conv"], sort=False):
        s, c = sub.set_index("f")["Sharpe"], sub.set_index("f")["CAGR"]
        for f in FGRID[1:-1]:
            lin = (1 - f) * s[0.0] + f * s[1.0]
            giveup = 100 * (c[0.0] - c[f])
            dv.append(dict(universe=tag, sleeve=sname, book=bname, conv=conv, f=f,
                           n_assets=len(SLEEVES[sname]),
                           corr=cmap[(tag, sname, bname)],
                           Sharpe=s[f], dSharpe=s[f] - lin, dCAGR_pp=-giveup,
                           conv_per_pp=(s[f] - lin) / max(giveup, 1e-9),
                           # RAW statistic: Sharpe gained per pp of CAGR surrendered vs the
                           # pure book.  Unlike conv_per_pp it needs no f=1 endpoint, so it is
                           # DEFINED for the cash null (whose f=1 Sharpe is NaN: zero vol).
                           raw_per_pp=((s[f] - s[0.0]) / giveup) if giveup > 1e-6 else np.nan,
                           dSharpe_raw=s[f] - s[0.0]))
    D = pd.DataFrame(dv)
    D.to_csv(f"{OUT}.convexity.csv", index=False)
    agg = D.groupby(["sleeve", "n_assets"]).agg(
        n=("dSharpe", "size"), corr_mean=("corr", "mean"),
        dSharpe_mean=("dSharpe", "mean"), dSharpe_pos=("dSharpe", lambda x: int((x > 0).sum())),
        dCAGR_pp_mean=("dCAGR_pp", "mean"),
        conv_per_pp_median=("conv_per_pp", "median"),
        conv_per_pp_mean=("conv_per_pp", "mean")).sort_values("corr_mean")
    print(agg.to_string(float_format=lambda x: f"{x:.4f}"))
    agg.to_csv(f"{OUT}.ladder.csv")

    # ------------------------------------------------------------ (3) the regression
    print("\n" + "=" * 118)
    print("### (3) REGRESSION of convexity-per-pp on realised correlation")
    for label, sub in [("ALL 360 interior points", D),
                       ("natural only", D[D.conv == "natural"]),
                       ("matched only", D[D.conv == "matched"]),
                       ("f=0.25", D[D.f == 0.25]), ("f=0.50", D[D.f == 0.50]), ("f=0.75", D[D.f == 0.75]),
                       ("excluding the SCASH null", D[D.sleeve != "SCASH"])]:
        sl, ic, r2, n = ols(sub["corr"], sub["conv_per_pp"])
        rho = spearman(sub["corr"], sub["conv_per_pp"])
        print(f"  {label:26s} n={n:4d}  slope {sl:+.4f}  intercept {ic:+.4f}  R2 {r2:.4f}  spearman {rho:+.4f}")

    print("\n  MONOTONICITY: within each (universe, book, conv, f) cell, order the 11 sleeves by")
    print("  realised correlation and count adjacent inversions of conv_per_pp.")
    mono = []
    for key, sub in D.groupby(["universe", "book", "conv", "f"], sort=False):
        ss = sub.sort_values("corr")
        v = ss.conv_per_pp.values
        inv = int((np.diff(v) > 0).sum())          # a rise as correlation rises = an inversion
        mono.append(dict(universe=key[0], book=key[1], conv=key[2], f=key[3],
                         inversions=inv, pairs=len(v) - 1, strictly_monotone=(inv == 0),
                         rho=spearman(ss["corr"], ss.conv_per_pp)))
    M = pd.DataFrame(mono)
    M.to_csv(f"{OUT}.monotonicity.csv", index=False)
    print(f"  strictly monotone-decreasing cells: {int(M.strictly_monotone.sum())}/{len(M)}; "
          f"mean inversions {M.inversions.mean():.2f} of {M.pairs.iloc[0]} pairs; "
          f"mean within-cell spearman {M.rho.mean():+.4f} (negative = the queue's direction)")
    print(M.groupby(["conv", "f"]).agg(cells=("inversions", "size"), mono=("strictly_monotone", "sum"),
                                       mean_inv=("inversions", "mean"), mean_rho=("rho", "mean")).to_string(
        float_format=lambda x: f"{x:.3f}"))

    # ------------------------------------------------------------ (4) path dependence
    print("\n" + "=" * 118)
    print("### (4) IS IT CORRELATION, OR WHICH ETF WAS ADDED?  Forward vs reverse path at matched size")
    pd_rows = []
    for k in range(5, 9):
        a, b = f"S{k}f", f"S{k}r"
        for (tag, bname, conv, f), sub in D.groupby(["universe", "book", "conv", "f"], sort=False):
            ra = sub[sub.sleeve == a]
            rb = sub[sub.sleeve == b]
            if len(ra) and len(rb):
                ra, rb = ra.iloc[0], rb.iloc[0]
                pd_rows.append(dict(pair=f"{a} vs {b}", universe=tag, book=bname, conv=conv, f=f,
                                    corr_f=ra["corr"], corr_r=rb["corr"], d_corr=ra["corr"] - rb["corr"],
                                    conv_f=ra.conv_per_pp, conv_r=rb.conv_per_pp,
                                    d_conv=ra.conv_per_pp - rb.conv_per_pp))
    PDF = pd.DataFrame(pd_rows)
    PDF.to_csv(f"{OUT}.pathdep.csv", index=False)
    print(PDF.groupby("pair").agg(n=("d_conv", "size"), mean_corr_f=("corr_f", "mean"),
                                  mean_corr_r=("corr_r", "mean"), mean_d_corr=("d_corr", "mean"),
                                  mean_d_conv=("d_conv", "mean"),
                                  same_sign_as_corr=("d_conv", lambda x: np.nan)).to_string(
        float_format=lambda x: f"{x:.4f}"))
    agree = int(((PDF.d_corr < 0) == (PDF.d_conv > 0)).sum())
    print(f"  Sign agreement with the correlation story (lower corr -> higher convexity): "
          f"{agree}/{len(PDF)} = {agree/len(PDF):.3f}")
    sl, ic, r2, n = ols(PDF.d_corr, PDF.d_conv)
    print(f"  Paired regression d_conv on d_corr: slope {sl:+.4f}, R2 {r2:.4f}, n={n}")

    # ------------------------------------------------------------ (5) where does it stop paying
    print("\n" + "=" * 118)
    print("### (5) WHERE DOES IT STOP PAYING?  Against the SCASH null (corr = 0, the gross dial).")
    print("  NOTE, stated because it is a limit of the statistic and not a result: conv_per_pp is")
    print("  UNDEFINED for the cash null -- its f=1 endpoint is all cash, zero vol, Sharpe NaN, so")
    print("  the linear blend it is measured against does not exist.  The null is therefore read on")
    print("  raw_per_pp = (Sharpe(f) - Sharpe(0)) / pp of CAGR surrendered, which needs no endpoint")
    print("  and is computed identically for every sleeve.  Under the MATCHED convention the cash")
    print("  null IS the book (gate (a): 4e-16), so it surrenders no CAGR and the null exists only")
    print("  on the NATURAL side; ideas 351/367 say a pure exposure cut has ~zero Sharpe content, so")
    print("  the bar a sleeve must clear is raw_per_pp above the null's, not above zero.\n")
    nat = D[D.conv == "natural"]
    null = nat[nat.sleeve == "SCASH"].set_index(["universe", "book", "f"])["raw_per_pp"]
    D2 = nat[nat.sleeve != "SCASH"].copy()
    D2["null_raw"] = [null.get((r.universe, r.book, r.f), np.nan) for r in D2.itertuples()]
    D2["beats_null"] = D2.raw_per_pp > D2.null_raw
    print(f"  the null itself (SCASH, natural): raw_per_pp mean {null.mean():+.4f}, "
          f"range [{null.min():+.4f}, {null.max():+.4f}], n={len(null)}")
    B = D2.groupby(["sleeve", "n_assets"]).agg(
        n=("beats_null", "size"), corr_mean=("corr", "mean"),
        beats_null=("beats_null", "sum"),
        raw_mean=("raw_per_pp", "mean"), null_mean=("null_raw", "mean"),
        conv_mean=("conv_per_pp", "mean")).sort_values("corr_mean")
    B["beat_rate"] = B.beats_null / B.n
    print(B.to_string(float_format=lambda x: f"{x:.4f}"))
    B.to_csv(f"{OUT}.vs_null.csv")
    bins = pd.cut(D2["corr"], [-1, 0.1, 0.25, 0.40, 0.55, 0.70, 1.0])
    print("\n  by realised-correlation bin (natural convention only, the side the null exists on):")
    print(D2.groupby(bins, observed=True).agg(
        n=("beats_null", "size"), conv_per_pp=("conv_per_pp", "mean"),
        raw_per_pp=("raw_per_pp", "mean"), null=("null_raw", "mean"),
        beat_rate=("beats_null", "mean"), dSharpe=("dSharpe", "mean")).to_string(
        float_format=lambda x: f"{x:.4f}"))
    sl, ic, r2, n = ols(D2["corr"], D2["raw_per_pp"])
    print(f"\n  regression of the DEFINED statistic: raw_per_pp on corr -> slope {sl:+.4f}, "
          f"intercept {ic:+.4f}, R2 {r2:.4f}, spearman {spearman(D2['corr'], D2['raw_per_pp']):+.4f}, n={n}")

    # ------------------------------------------------------------ (6) the mechanism
    print("\n" + "=" * 118)
    print("### (6) MECHANISM — is the correlation ordering a fact about DELIVERED Sharpe, or about")
    print("###     the benchmark idea 100's statistic subtracts?")
    print("  conv_per_pp subtracts the LINEAR BLEND (1-f)*Sharpe(0) + f*Sharpe(1).  Sharpe(1) is the")
    print("  sleeve's own standalone Sharpe, and adding equity ETFs raises it.  So a sleeve can look")
    print("  less 'convex' purely because the yardstick it is measured against got longer, with no")
    print("  change in the Sharpe the blend actually delivers.  raw_per_pp has no such term.\n")
    s1 = G[G.f == 1.0].set_index(["universe", "sleeve", "book", "conv"])["Sharpe"]
    D["sleeve_Sharpe"] = [s1.get((r.universe, r.sleeve, r.book, r.conv), np.nan) for r in D.itertuples()]
    ok = D[D.sleeve != "SCASH"]                       # SCASH's f=1 Sharpe is NaN by construction
    print(f"  corr(realised sleeve-book correlation, sleeve standalone Sharpe) = "
          f"{np.corrcoef(ok['corr'], ok.sleeve_Sharpe)[0,1]:+.4f}   "
          f"(sleeve Sharpe {ok.sleeve_Sharpe.min():.3f}..{ok.sleeve_Sharpe.max():.3f})")
    for label, yv in [("conv_per_pp (idea 100's statistic)", "conv_per_pp"),
                      ("raw_per_pp   (no linear-blend term)", "raw_per_pp")]:
        sl, ic, r2, n = ols(ok["corr"], ok[yv])
        rho = spearman(ok["corr"], ok[yv])
        # residualise the statistic on the sleeve's own standalone Sharpe, then re-regress
        b = np.polyfit(ok.sleeve_Sharpe, ok[yv].fillna(ok[yv].mean()), 1)
        resid = ok[yv] - np.polyval(b, ok.sleeve_Sharpe)
        sl2, _, r22, n2 = ols(ok["corr"], resid)
        rho2 = spearman(ok["corr"], resid)
        print(f"  {label:38s} raw: slope {sl:+.4f} R2 {r2:.4f} spearman {rho:+.4f} | "
              f"after removing the sleeve's own standalone Sharpe: slope {sl2:+.4f} R2 {r22:.4f} "
              f"spearman {rho2:+.4f}")
    D.to_csv(f"{OUT}.convexity.csv", index=False)

    # ------------------------------------------------------------ KEEP paths
    print("\n" + "=" * 118)
    print(f"### KEEP PATHS over all {len(G)} points (both reported, none selected on)")
    kp = G.groupby(["universe", "conv"]).agg(n=("p4b", "size"), p4b=("p4b", "sum"),
                                             p4a_v2=("p4a", "sum"), p4a_v1=("p4a_v1", "sum"))
    print(kp.to_string())
    print(f"  TOTAL: 4b {G.p4b.sum()}/{len(G)}; 4a vs RULES v2 {G.p4a.sum()}/{len(G)}; "
          f"4a vs RULES v1 {G.p4a_v1.sum()}/{len(G)}")
    # f=0 is the SAME pure book under all 11 sleeves, so the raw count over-states.  Count
    # DISTINCT books: collapse f=0 (and, under `matched`, the algebraically-identical SCASH).
    Gd = G.copy()
    Gd["sleeve_eff"] = np.where(Gd.f == 0.0, "-", Gd.sleeve)
    Gd["conv_eff"] = np.where((Gd.f == 0.0) | (Gd.sleeve == "SCASH"), "-", Gd.conv)
    Dq = Gd.drop_duplicates(subset=["universe", "book", "sleeve_eff", "conv_eff", "f"])
    print(f"  DISTINCT books (f=0 collapsed across sleeves; matched-vs-natural collapsed for the "
          f"cash null): {len(Dq)} of {len(G)} rows; 4b {int(Dq.p4b.sum())}/{len(Dq)}, "
          f"4a vs v2 {int(Dq.p4a.sum())}/{len(Dq)}")
    if G.p4b.sum():
        cols = ["universe", "sleeve", "book", "conv", "f", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "Turn_yr", "Gross", "p4a"]
        print("\n  4b passes (DISTINCT books only):")
        print(Dq[Dq.p4b][cols].sort_values("Sharpe", ascending=False).to_string(
            index=False, float_format=lambda x: f"{x:.4f}"))
    G[G.p4b].to_csv(f"{OUT}.keeppaths.csv", index=False)

    # ------------------------------------------------------------ RULE 8
    print("\n" + "=" * 118)
    print("### RULE 8 WALK-FORWARD — (sleeve, f) chosen on 2009-2016 IS Sharpe, 2017- read ONCE")
    wf = []
    for (tag, bname, conv), sub in G.groupby(["universe", "book", "conv"], sort=False):
        base, v2, spy = refs[tag]
        pick = sub.loc[sub.IS_Sharpe.idxmax()]
        ctrl = sub[(sub.f == 0.0)].iloc[0]                        # the no-sleeve control
        cashp = sub[sub.sleeve == "SCASH"]
        cashp = cashp.loc[cashp.IS_Sharpe.idxmax()]               # best CASH arm, the null
        wf.append(dict(universe=tag, book=bname, conv=conv,
                       pick=f"{pick.sleeve}@f={pick.f:.2f}", pick_corr=cmap[(tag, pick.sleeve, bname)],
                       pick_OOS_CAGR=pick.OOS_CAGR, pick_OOS_Sharpe=pick.OOS_Sharpe,
                       pick_OOS_MaxDD=pick.OOS_MaxDD,
                       ctrl_OOS_Sharpe=ctrl.OOS_Sharpe, ctrl_OOS_CAGR=ctrl.OOS_CAGR,
                       ctrl_OOS_MaxDD=ctrl.OOS_MaxDD,
                       null_pick=f"SCASH@f={cashp.f:.2f}", null_OOS_Sharpe=cashp.OOS_Sharpe,
                       v2_OOS_Sharpe=v2["OOS_Sharpe"], v2_OOS_CAGR=v2["OOS_CAGR"],
                       v1_OOS_Sharpe=base["OOS_Sharpe"],
                       spy_OOS_Sharpe=spy["OOS_Sharpe"], spy_OOS_CAGR=spy["OOS_CAGR"],
                       spy_OOS_MaxDD=spy["OOS_MaxDD"]))
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    print(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    d = W.pick_OOS_Sharpe - W.ctrl_OOS_Sharpe
    d2 = W.pick_OOS_Sharpe - W.null_OOS_Sharpe
    print(f"\n  IS pick minus no-sleeve control, OOS Sharpe: mean {d.mean():+.4f}, wins {int((d>0).sum())}/{len(d)}")
    print(f"  IS pick minus best CASH (null) arm, OOS Sharpe: mean {d2.mean():+.4f}, wins {int((d2>0).sum())}/{len(d2)}")
    print(f"  IS chooser picked a sleeve with correlation: "
          f"{W.pick_corr.min():.3f}..{W.pick_corr.max():.3f} (mean {W.pick_corr.mean():.3f})")
    print(f"  vs RULES v2 OOS Sharpe: pick wins {int((W.pick_OOS_Sharpe > W.v2_OOS_Sharpe).sum())}/{len(W)}; "
          f"vs SPY OOS: {int((W.pick_OOS_Sharpe > W.spy_OOS_Sharpe).sum())}/{len(W)}")

    print("\nWritten:", ", ".join(sorted(p.name for p in OUT.parent.glob(OUT.name + ".*"))))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Idea 357 (cloud, 2026-09-07): is-the-SLEEVE-S-OWN-SHARPE-the-real-design-variable.

QUEUE TEXT: "idea 103 falsified correlation as the sleeve design variable by showing it is
91% a proxy for the sleeve's own standalone Sharpe (corr +0.746; residualising kills
spearman -0.624 -> -0.056).  Re-run the ladder ranking sleeves by their OWN Sharpe instead,
holding realised correlation as the control, and ask which of the two survives the other.
Max 2 params (sleeve, f)."

WHY THE PARENT CANNOT ANSWER ITS OWN QUESTION
---------------------------------------------
Idea 103's ladder is ONE-DIMENSIONAL by construction: it is built by adding equity ETFs to
S4 one at a time, which raises the sleeve's correlation to the book AND its own standalone
Sharpe together (+0.746).  On such a ladder "corr survives own-Sharpe" and "own-Sharpe
survives corr" are the same regression run twice; whichever is residualised second wins.
Idea 103 residualised on own-Sharpe and killed corr, but the symmetric test would have
killed own-Sharpe just as easily.  The honest answer needs sleeves that DECOUPLE the two.

THIS RUN THEREFORE WIDENS THE SLEEVE POPULATION, NOT THE PARAMETER COUNT.  `sleeve` is
still one tuned parameter; it simply ranges over a population that spans the (corr,
own-Sharpe) PLANE instead of a line:

  * idea 103's 11 rungs, verbatim (SCASH, S4, S5f..S8f, S5r..S8r, S9) -- the reproduction
    gate: this run must recover its +0.746 and its -0.624 -> -0.056 collapse exactly.
  * 10 single-asset sleeves chosen a priori to break the collinearity, NOT chosen on any
    result: GDX / USO / SLV / UNG (low correlation, poor own Sharpe), TLT / GLD / SHY / DBC
    (low correlation, varied own Sharpe), HYG (mid correlation, good own Sharpe), QQQ (high
    correlation, high own Sharpe).  Every one is priced in BOTH panels since 2008.

  = 21 sleeves.  Everything else is idea 103's, unchanged: the same vote-momentum x
  inverse-60d-vol risk-parity sleeve construction, the same three books (v1 / top20 /
  ewall), both universes, both blend conventions, f in {0, .25, .50, .75, 1.00}, 10 bps,
  weekly, gross 0.75.  Grid = 21 x 3 x 2 x 2 x 5 = 1260 points, ALL reported.

THE DECISIVE TESTS
------------------
(A) BIVARIATE.  Regress each statistic on (corr, own_Sharpe) jointly, and report both
    partial spearmans, on the parent's 11-rung ladder AND on the 21-sleeve plane.  A
    variable "survives the other" only if its partial keeps its sign and size.
(B) MATCHED STRATA.  Inside correlation bins, does own-Sharpe still order the statistic?
    Inside own-Sharpe bins, does correlation?  This needs no linear form at all.
(C) RULE 8 (the one that decides).  Three PRE-REGISTERED choosers on 2009-2016, each read
    ONCE on 2017-2026: S_OWN picks the sleeve with the highest IS standalone Sharpe;
    S_CORR picks the lowest IS correlation to that book; FREE is idea 103's joint IS-Sharpe
    argmax.  f is always the IS-Sharpe argmax given the chosen sleeve.  A design variable
    that cannot beat the no-sleeve control, the cash null and the other variable out of
    sample is not a design variable, whatever its in-sample regression says.

STATISTICS.  conv_per_pp = dSharpe(f)/(100*dCAGR(f)) with dSharpe against the LINEAR BLEND
(idea 100's, confounded by its own f=1 endpoint), and raw_per_pp = (Sharpe(f)-Sharpe(0))/pp
surrendered (benchmark-free, defined for the cash null).  Both reported everywhere -- idea
359 is open on exactly this ambiguity, so neither is privileged here.

SURVIVORSHIP: both panels are current constituents (levels biased up); the sleeve ETFs are
survivors by construction.  No small-cap panel: the sleeve assets are not in it.

Deterministic, standalone, offline:
    python3 research/backtests/2026-09-07_is-the-SLEEVE-S-OWN-SHARPE-the-real-design-variable_cloud.py
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
pd.set_option("display.max_rows", 900)

COST_BPS, FREQ, GROSS = 10, "W", 0.75
MOM_LAGS, VOL_WINDOW = (252, 126, 63), 60
FGRID = [0.00, 0.25, 0.50, 0.75, 1.00]
SPLIT, IS_END = "2017-01-01", "2016-12-31"
CORE4 = ["TLT", "GLD", "DBC", "UUP"]
FWD = ["SPY", "QQQ", "IWM", "EFA", "EEM"]          # the record's own list order
REV = ["EEM", "EFA", "IWM", "QQQ", "SPY"]
# a-priori decoupling set: picked for WHERE THEY SIT in the (corr, own-Sharpe) plane, not
# for any backtest result.  Fixed before the grid was run; none is dropped afterwards.
SINGLES = ["GDX", "USO", "SLV", "UNG", "TLT", "GLD", "SHY", "DBC", "HYG", "QQQ"]
OUT = Path(__file__).with_suffix("")


def build_ladder():
    """idea 103's 11 rungs verbatim, then the 10 single-asset decoupling sleeves."""
    L = {"SCASH": [], "S4": list(CORE4)}
    for i in range(1, len(FWD)):
        L[f"S{4+i}f"] = CORE4 + FWD[:i]
    for i in range(1, len(REV)):
        L[f"S{4+i}r"] = CORE4 + REV[:i]
    L["S9"] = CORE4 + FWD
    for t in SINGLES:
        L[f"X_{t}"] = [t]
    return L


SLEEVES = build_ladder()
LADDER11 = ["SCASH", "S4", "S5f", "S6f", "S7f", "S8f", "S5r", "S6r", "S7r", "S8r", "S9"]


# ---------------------------------------------------------------- sleeves / books (idea 103's)
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
    if not assets:
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
    a, b, c = stats(r), stats(r.iloc[:len(r) // 2]), stats(r.iloc[len(r) // 2:])
    o, i = stats(r.loc[SPLIT:]), stats(r.loc[:IS_END])
    return dict(CAGR=a["CAGR"], Sharpe=a["Sharpe"], MaxDD=a["MaxDD"], H1=b["Sharpe"], H2=c["Sharpe"],
                IS_Sharpe=i["Sharpe"], IS_CAGR=i["CAGR"], IS_MaxDD=i["MaxDD"],
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
    ss = ((y - y.mean()) ** 2).sum()
    r2 = 1 - ((y - np.polyval(b, x)) ** 2).sum() / ss if ss > 0 else np.nan
    return float(b[0]), float(b[1]), float(r2), int(len(x))


def ols2(X, y):
    """Bivariate OLS with intercept -> (b1, b2, R2, n, t1, t2)."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    ok = np.isfinite(y) & np.isfinite(X).all(axis=1)
    X, y = X[ok], y[ok]
    if len(y) < 5:
        return (np.nan,) * 4 + (0, np.nan, np.nan)
    A = np.column_stack([np.ones(len(y)), X])
    beta, *_ = np.linalg.lstsq(A, y, rcond=None)
    res = y - A @ beta
    ss = ((y - y.mean()) ** 2).sum()
    r2 = 1 - (res ** 2).sum() / ss if ss > 0 else np.nan
    dof = max(len(y) - A.shape[1], 1)
    s2 = (res ** 2).sum() / dof
    try:
        cov = s2 * np.linalg.inv(A.T @ A)
        se = np.sqrt(np.diag(cov))
        t = beta / se
    except np.linalg.LinAlgError:
        t = np.full(3, np.nan)
    return float(beta[1]), float(beta[2]), float(r2), int(len(y)), float(t[1]), float(t[2])


def partial_spearman(y, x, z):
    """spearman(y, x) after linearly removing z from BOTH, on ranks."""
    df = pd.DataFrame({"y": np.asarray(y, float), "x": np.asarray(x, float), "z": np.asarray(z, float)}).dropna()
    if len(df) < 5:
        return np.nan
    ry, rx, rz = df.y.rank(), df.x.rank(), df.z.rank()
    ey = ry - np.polyval(np.polyfit(rz, ry, 1), rz)
    ex = rx - np.polyval(np.polyfit(rz, rx, 1), rz)
    if ey.std() == 0 or ex.std() == 0:
        return np.nan
    return float(np.corrcoef(ey, ex)[0, 1])


# ---------------------------------------------------------------- main
def main():
    print("SLEEVE POPULATION (21): idea 103's 11 rungs + 10 a-priori decoupling singletons")
    for k, v in SLEEVES.items():
        print(f"  {k:8s} n={len(v)}  {v if v else '(cash)'}")

    universes = {"u56": load_universe(), "broad": load_universe(broad=True)}
    records, corr_rows, refs, own_rows = [], [], {}, []

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
        print("\n" + "=" * 120)
        print(f"### {tag}: {px.shape[1]} tickers, {px.index[0].date()} -> {px.index[-1].date()}, eval from {start.date()}")
        print(pd.DataFrame({"RULES v1": base, "RULES v2 (live)": v2, "SPY": spy}).T.to_string(
            float_format=lambda x: f"{x:.4f}"))
        print(f"4b bars: H1>{spy['H1']:.4f} H2>{spy['H2']:.4f} OOS>{spy['OOS_Sharpe']:.4f} "
              f"|MaxDD|<={abs(0.60*spy['MaxDD']):.2%} CAGR>={0.70*spy['CAGR']:.2%}")

        S_w = {s: sleeve_weights(px, a) for s, a in SLEEVES.items()}
        S_res = {s: backtest(px, w, cost_bps=COST_BPS, freq=FREQ) for s, w in S_w.items()}
        S_r = {s: v["returns"].loc[start:] for s, v in S_res.items()}
        B_w = {b: fn(px) for b, fn in BOOKS.items()}
        B_r = {b: backtest(px, w, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:] for b, w in B_w.items()}

        # the sleeve's OWN standalone record (the candidate design variable), full / IS / OOS
        for s in SLEEVES:
            rr = S_r[s]
            m, mi, mo = stats(rr), stats(rr.loc[:IS_END]), stats(rr.loc[SPLIT:])
            own_rows.append(dict(universe=tag, sleeve=s, n_assets=len(SLEEVES[s]),
                                 own_Sharpe=m["Sharpe"], own_CAGR=m["CAGR"], own_MaxDD=m["MaxDD"],
                                 own_IS_Sharpe=mi["Sharpe"], own_OOS_Sharpe=mo["Sharpe"],
                                 own_gross=float(S_w[s].loc[start:].sum(axis=1).mean())))
        # realised correlations, full window and IS-only (IS version is what rule 8 may use)
        for s in SLEEVES:
            for b in list(BOOKS) + ["SPY"]:
                other = B_r[b] if b in B_r else spy_r
                if s == "SCASH":
                    c = c_is = 0.0
                else:
                    c = float(pd.concat([S_r[s], other], axis=1).corr().iloc[0, 1])
                    ii = pd.concat([S_r[s].loc[:IS_END], other.loc[:IS_END]], axis=1)
                    c_is = float(ii.corr().iloc[0, 1])
                corr_rows.append(dict(universe=tag, sleeve=s, book=b, n_assets=len(SLEEVES[s]),
                                      corr=c, corr_IS=c_is))

        # ---- the grid.  f=0 is the SAME pure book for every sleeve and convention: computed
        # once and reused (identical by construction, not an approximation).
        cache = {}
        for bname in BOOKS:
            r0 = backtest(px, B_w[bname], cost_bps=COST_BPS, freq=FREQ)
            cache[(bname, "PURE")] = r0
        for sname in SLEEVES:
            for bname in BOOKS:
                for matched in (False, True):
                    conv = "matched" if matched else "natural"
                    for f in FGRID:
                        if f == 0.0:
                            res, w = cache[(bname, "PURE")], B_w[bname]
                        else:
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
            print(f"  ... {sname} done ({len(records)} rows)")

    G = pd.DataFrame(records)
    R = pd.DataFrame(corr_rows)
    O = pd.DataFrame(own_rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    R.to_csv(f"{OUT}.correlation.csv", index=False)
    O.to_csv(f"{OUT}.sleeves.csv", index=False)

    cmap = {(r.universe, r.sleeve, r.book): r.corr for r in R.itertuples()}
    cmap_is = {(r.universe, r.sleeve, r.book): r.corr_IS for r in R.itertuples()}
    omap = {(r.universe, r.sleeve): r.own_Sharpe for r in O.itertuples()}
    omap_is = {(r.universe, r.sleeve): r.own_IS_Sharpe for r in O.itertuples()}

    # ------------------------------------------------------------ gates
    print("\n" + "=" * 120)
    print("### REPRODUCTION GATES")
    g1 = G[(G.sleeve == "SCASH") & (G.conv == "matched")]
    piv = g1.pivot_table(index=["universe", "book"], columns="f", values="Sharpe")
    err = float((piv.max(axis=1) - piv.min(axis=1)).abs().max())
    print(f"  (a) MATCHED cash sleeve is algebraically the book: max Sharpe spread across f = "
          f"{err:.3e}  {'PASS' if err < 1e-9 else 'FAIL'}")
    print("  (b) idea 100 / idea 103's published S4 rows (u56 top20, 10 bps, weekly):")
    for sn, fv, conv, want in [("S4", 0.25, "natural", "10.2% / 1.14 / -14.2% / 1.11 / 1.18"),
                               ("S4", 0.25, "matched", "10.8% / 1.14 / -14.6% / 1.13 / 1.16"),
                               ("S4", 0.50, "natural", " 7.7% / 1.19 / -10.0% / 1.10 / 1.27"),
                               ("S9", 1.00, "natural", " 5.0% / 0.87 / -10.1% / 0.76 / 0.98")]:
        q = G[(G.universe == "u56") & (G.book == "top20") & (G.sleeve == sn) & (G.f == fv) & (G.conv == conv)]
        q = q.iloc[0]
        print(f"      {sn} f={fv} {conv:8s} -> {q.CAGR:.1%} / {q.Sharpe:.2f} / {q.MaxDD:.1%} / "
              f"{q.H1:.2f} / {q.H2:.2f}   (published {want})")

    # ------------------------------------------------------------ the two axes
    print("\n" + "=" * 120)
    print("### (0) THE TWO CANDIDATE DESIGN VARIABLES, sleeve by sleeve")
    axes = O.pivot_table(index=["sleeve", "n_assets"], columns="universe", values="own_Sharpe")
    axes.columns = [f"ownSharpe_{c}" for c in axes.columns]
    cm = R[R.book != "SPY"].pivot_table(index=["sleeve", "n_assets"], columns="universe", values="corr")
    cm.columns = [f"corr_{c}" for c in cm.columns]
    AX = axes.join(cm)
    AX["corr_MEAN"] = AX[[c for c in AX if c.startswith("corr_")]].mean(axis=1)
    AX["own_MEAN"] = AX[[c for c in AX if c.startswith("ownSharpe_")]].mean(axis=1)
    print(AX.sort_values("corr_MEAN").to_string(float_format=lambda x: f"{x:.3f}"))
    AX.to_csv(f"{OUT}.axes.csv")

    lad = AX.loc[[s for s in AX.index if s[0] in LADDER11]]
    lad = lad[lad.own_MEAN.notna()]
    allx = AX[AX.own_MEAN.notna()]
    print(f"\n  COLLINEARITY of the two axes (the whole point of this run), sleeve-level:")
    print(f"    idea 103's 11-rung ladder : pearson {np.corrcoef(lad.corr_MEAN, lad.own_MEAN)[0,1]:+.4f}  "
          f"spearman {spearman(lad.corr_MEAN, lad.own_MEAN):+.4f}  n={len(lad)}")
    print(f"    this run's 21-sleeve plane: pearson {np.corrcoef(allx.corr_MEAN, allx.own_MEAN)[0,1]:+.4f}  "
          f"spearman {spearman(allx.corr_MEAN, allx.own_MEAN):+.4f}  n={len(allx)}")

    # ------------------------------------------------------------ statistics
    print("\n" + "=" * 120)
    print("### (1) THE STATISTICS (idea 100's conv_per_pp and the benchmark-free raw_per_pp)")
    dv = []
    for (tag, sname, bname, conv), sub in G.groupby(["universe", "sleeve", "book", "conv"], sort=False):
        s, c = sub.set_index("f")["Sharpe"], sub.set_index("f")["CAGR"]
        for f in FGRID[1:-1]:
            lin = (1 - f) * s[0.0] + f * s[1.0]
            giveup = 100 * (c[0.0] - c[f])
            dv.append(dict(universe=tag, sleeve=sname, book=bname, conv=conv, f=f,
                           n_assets=len(SLEEVES[sname]),
                           corr=cmap[(tag, sname, bname)], own_Sharpe=omap[(tag, sname)],
                           sleeve_blend_Sharpe=s[1.0],
                           Sharpe=s[f], dSharpe=s[f] - lin, dCAGR_pp=-giveup,
                           conv_per_pp=(s[f] - lin) / max(giveup, 1e-9),
                           raw_per_pp=((s[f] - s[0.0]) / giveup) if giveup > 1e-6 else np.nan,
                           dSharpe_raw=s[f] - s[0.0]))
    D = pd.DataFrame(dv)
    # conv_per_pp's denominator is the CAGR the blend surrenders.  idea 103 already found it
    # UNDEFINED for the cash null; on this wider population it also EXPLODES for any sleeve
    # whose CAGR matches the book's (the denominator passes through zero).  Flag those points
    # rather than delete them, and report every regression twice: raw, and on defined points.
    D["denom_pp"] = -D.dCAGR_pp
    D["conv_defined"] = D.denom_pp.abs() >= 0.05          # >= 0.05 pp of CAGR surrendered
    n_bad = int((~D.conv_defined).sum())
    print(f"  conv_per_pp denominator guard: {n_bad}/{len(D)} interior points surrender < 0.05 pp "
          f"of CAGR, where the statistic is numerically undefined (worst |conv_per_pp| "
          f"{D.loc[~D.conv_defined, 'conv_per_pp'].abs().max():.3e}).")
    print("  Sleeves contributing them: " +
          ", ".join(f"{k}({v})" for k, v in D[~D.conv_defined].sleeve.value_counts().items()))
    D.to_csv(f"{OUT}.convexity.csv", index=False)
    print(D.groupby(["sleeve", "n_assets"]).agg(
        n=("dSharpe", "size"), corr=("corr", "mean"), own_Sharpe=("own_Sharpe", "mean"),
        dSharpe=("dSharpe", "mean"), dSharpe_raw=("dSharpe_raw", "mean"),
        conv_per_pp=("conv_per_pp", "median"), raw_per_pp=("raw_per_pp", "median")
    ).sort_values("corr").to_string(float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------ (A) bivariate
    print("\n" + "=" * 120)
    print("### (A) WHICH VARIABLE SURVIVES THE OTHER — bivariate OLS and partial spearmans")
    print("###     (SCASH excluded throughout: its own standalone Sharpe is NaN by construction)")
    # --- first, reproduce idea 103's OWN chain exactly, by its own method.  It residualised
    # the statistic (only) on the sleeve's standalone Sharpe with a LINEAR fit and then took
    # spearman against corr -- a semi-partial, not a partial.  Both are reported here because
    # they do not agree, and the record quotes the semi-partial.
    lad0 = D[D.sleeve.isin(LADDER11) & (D.sleeve != "SCASH")]
    print("  idea 103 REPRODUCTION (its 11-rung ladder, its own method):")
    print(f"    pooled corr(realised corr, sleeve standalone Sharpe) = "
          f"{np.corrcoef(lad0['corr'], lad0.sleeve_blend_Sharpe)[0,1]:+.4f}   (published +0.746)")
    for yv in ("conv_per_pp", "raw_per_pp"):
        b = np.polyfit(lad0.sleeve_blend_Sharpe, lad0[yv].fillna(lad0[yv].mean()), 1)
        semi = spearman(lad0["corr"], lad0[yv] - np.polyval(b, lad0.sleeve_blend_Sharpe))
        print(f"    {yv:12s} spearman vs corr {spearman(lad0['corr'], lad0[yv]):+.4f} -> "
              f"semi-partial (idea 103's method) {semi:+.4f} | proper partial spearman "
              f"{partial_spearman(lad0[yv], lad0['corr'], lad0.sleeve_blend_Sharpe):+.4f}")
    print("    (published for conv_per_pp: -0.624 -> -0.056)\n")

    rows = []
    for pop, sel in [("idea 103 ladder (11)", D[D.sleeve.isin(LADDER11)]),
                     ("this run's plane (21)", D),
                     ("plane, conv defined", D[D.conv_defined])]:
        sub0 = sel[sel.sleeve != "SCASH"]
        for yv in ("conv_per_pp", "raw_per_pp", "dSharpe", "dSharpe_raw"):
            s_c, _, r2c, nc = ols(sub0["corr"], sub0[yv])
            s_o, _, r2o, no = ols(sub0["own_Sharpe"], sub0[yv])
            b1, b2, r2, n, t1, t2 = ols2(sub0[["corr", "own_Sharpe"]].values, sub0[yv].values)
            rows.append(dict(pop=pop, y=yv, n=n,
                             uni_corr_slope=s_c, uni_corr_R2=r2c,
                             uni_own_slope=s_o, uni_own_R2=r2o,
                             joint_corr_b=b1, joint_corr_t=t1,
                             joint_own_b=b2, joint_own_t=t2, joint_R2=r2,
                             rho_corr=spearman(sub0["corr"], sub0[yv]),
                             rho_own=spearman(sub0["own_Sharpe"], sub0[yv]),
                             pr_corr_given_own=partial_spearman(sub0[yv], sub0["corr"], sub0["own_Sharpe"]),
                             pr_own_given_corr=partial_spearman(sub0[yv], sub0["own_Sharpe"], sub0["corr"])))
    BV = pd.DataFrame(rows)
    BV.to_csv(f"{OUT}.bivariate.csv", index=False)
    print(BV.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\n  READ: pr_corr_given_own is idea 103's -0.056 collapse; pr_own_given_corr is the")
    print("  symmetric test it never ran.  On the 11-rung ladder BOTH must collapse (collinear);")
    print("  only the 21-sleeve plane can separate them.")

    # within-cell version (the record's own convention: no pooling across books/panels)
    print("\n  WITHIN-CELL (universe x book x conv x f), SCASH dropped:")
    wc = []
    for key, sub in D[D.sleeve != "SCASH"].groupby(["universe", "book", "conv", "f"], sort=False):
        pops = [("ladder11", sub[sub.sleeve.isin(LADDER11)]), ("plane21", sub),
                ("plane21_convdef", sub[sub.conv_defined])]
        for pn, ss in pops:
            if len(ss) < 6:
                continue
            for yv in ("conv_per_pp", "raw_per_pp"):
                wc.append(dict(pop=pn, universe=key[0], book=key[1], conv=key[2], f=key[3], y=yv,
                               rho_corr=spearman(ss["corr"], ss[yv]),
                               rho_own=spearman(ss["own_Sharpe"], ss[yv]),
                               pr_corr=partial_spearman(ss[yv], ss["corr"], ss["own_Sharpe"]),
                               pr_own=partial_spearman(ss[yv], ss["own_Sharpe"], ss["corr"])))
    WC = pd.DataFrame(wc)
    WC.to_csv(f"{OUT}.withincell.csv", index=False)
    print(WC.groupby(["pop", "y"]).agg(
        cells=("rho_corr", "size"), rho_corr=("rho_corr", "mean"), rho_own=("rho_own", "mean"),
        pr_corr=("pr_corr", "mean"), pr_own=("pr_own", "mean"),
        corr_neg=("rho_corr", lambda x: int((x < 0).sum())),
        own_pos=("rho_own", lambda x: int((x > 0).sum())),
        pr_corr_neg=("pr_corr", lambda x: int((x < 0).sum())),
        pr_own_pos=("pr_own", lambda x: int((x > 0).sum()))
    ).to_string(float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------ (B) matched strata
    print("\n" + "=" * 120)
    print("### (B) MATCHED STRATA — no functional form.  Does each variable order the statistic")
    print("###     INSIDE bins of the other?  21-sleeve plane, SCASH dropped, and the ordering")
    print("###     is measured WITHIN each (universe, book, conv, f) cell before averaging --")
    print("###     pooling across f would confound both axes with the blend fraction itself.")
    P = D[D.sleeve != "SCASH"].copy()
    P["corr_bin"] = pd.qcut(P["corr"], 4, duplicates="drop")
    P["own_bin"] = pd.qcut(P["own_Sharpe"], 4, duplicates="drop")
    strat = []
    for yv in ("conv_per_pp", "raw_per_pp"):
        for holder, mover in (("corr_bin", "own_Sharpe"), ("own_bin", "corr")):
            for key, g in P.groupby(["universe", "book", "conv", "f", holder], observed=True):
                b = key[-1]
                g2 = g if yv != "conv_per_pp" else g[g.conv_defined]
                if len(g2) < 3:
                    continue
                strat.append(dict(y=yv, held=holder, moved=mover, bin=str(b), n=len(g2),
                                  span=float(g2[mover].max() - g2[mover].min()),
                                  rho=spearman(g2[mover], g2[yv])))
    ST = pd.DataFrame(strat)
    ST.to_csv(f"{OUT}.strata.csv", index=False)
    for yv in ("conv_per_pp", "raw_per_pp"):
        for holder, mover, want in (("corr_bin", "own_Sharpe", "+"), ("own_bin", "corr", "-")):
            s = ST[(ST.y == yv) & (ST.held == holder)]
            print(f"\n  --- {yv}: does {mover} order it INSIDE {holder} quartiles? "
                  f"(the hypothesis predicts {want})")
            print(s.groupby("bin").agg(cells=("rho", "size"), mean_span=("span", "mean"),
                                       mean_rho=("rho", "mean"),
                                       pos=("rho", lambda x: int((x > 0).sum())),
                                       neg=("rho", lambda x: int((x < 0).sum()))
                                       ).to_string(float_format=lambda x: f"{x:.4f}"))
            print(f"      pooled over bins: mean rho {s.rho.mean():+.4f}, "
                  f"{int((s.rho>0).sum())}/{len(s)} positive")

    # ------------------------------------------------------------ KEEP paths
    print("\n" + "=" * 120)
    print(f"### KEEP PATHS over all {len(G)} points (both reported, none selected on)")
    print(G.groupby(["universe", "conv"]).agg(n=("p4b", "size"), p4b=("p4b", "sum"),
                                              p4a_v2=("p4a", "sum"), p4a_v1=("p4a_v1", "sum")).to_string())
    print(f"  TOTAL: 4b {G.p4b.sum()}/{len(G)}; 4a vs RULES v2 {G.p4a.sum()}/{len(G)}; "
          f"4a vs RULES v1 {G.p4a_v1.sum()}/{len(G)}")
    Gd = G.copy()
    Gd["sleeve_eff"] = np.where(Gd.f == 0.0, "-", Gd.sleeve)
    Gd["conv_eff"] = np.where((Gd.f == 0.0) | (Gd.sleeve == "SCASH"), "-", Gd.conv)
    Dq = Gd.drop_duplicates(subset=["universe", "book", "sleeve_eff", "conv_eff", "f"])
    print(f"  DISTINCT books (f=0 collapsed across sleeves; matched==natural for the cash null): "
          f"{len(Dq)} of {len(G)} rows; 4b {int(Dq.p4b.sum())}/{len(Dq)}, 4a vs v2 {int(Dq.p4a.sum())}/{len(Dq)}")
    cols = ["universe", "sleeve", "book", "conv", "f", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
            "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "Turn_yr", "Gross", "p4a"]
    if Dq.p4b.sum():
        print("\n  4b passes (DISTINCT books only), best 25 by Sharpe:")
        print(Dq[Dq.p4b][cols].sort_values("Sharpe", ascending=False).head(25).to_string(
            index=False, float_format=lambda x: f"{x:.4f}"))
    Dq[Dq.p4b].to_csv(f"{OUT}.keeppaths.csv", index=False)

    # ------------------------------------------------------------ (C) RULE 8
    print("\n" + "=" * 120)
    print("### (C) RULE 8 WALK-FORWARD — three PRE-REGISTERED sleeve choosers, IS 2009-2016,")
    print("###     OOS 2017-2026 read ONCE.  f = IS-Sharpe argmax given the chosen sleeve.")
    wf = []
    for (tag, bname, conv), sub in G.groupby(["universe", "book", "conv"], sort=False):
        b1, v2, spy = refs[tag]
        pool = sub[(sub.f > 0) & (sub.sleeve != "SCASH")]

        def best_f(sname):
            q = pool[pool.sleeve == sname]
            return q.loc[q.IS_Sharpe.idxmax()]

        cand = sorted({s for s in pool.sleeve})
        s_own = max(cand, key=lambda s: omap_is[(tag, s)])            # highest IS own Sharpe
        s_cor = min(cand, key=lambda s: cmap_is[(tag, s, bname)])     # lowest IS correlation
        picks = {"S_OWN": best_f(s_own), "S_CORR": best_f(s_cor),
                 "FREE": pool.loc[pool.IS_Sharpe.idxmax()]}
        ctrl = sub[sub.f == 0.0].iloc[0]
        cashp = sub[sub.sleeve == "SCASH"]
        cashp = cashp.loc[cashp.IS_Sharpe.idxmax()]
        for pname, p in picks.items():
            wf.append(dict(universe=tag, book=bname, conv=conv, chooser=pname,
                           pick=f"{p.sleeve}@f={p.f:.2f}",
                           pick_corr_IS=cmap_is[(tag, p.sleeve, bname)],
                           pick_own_IS=omap_is[(tag, p.sleeve)],
                           OOS_CAGR=p.OOS_CAGR, OOS_Sharpe=p.OOS_Sharpe, OOS_MaxDD=p.OOS_MaxDD,
                           p4b=bool(p.p4b), p4a=bool(p.p4a),
                           ctrl_OOS_Sharpe=ctrl.OOS_Sharpe, ctrl_OOS_CAGR=ctrl.OOS_CAGR,
                           ctrl_OOS_MaxDD=ctrl.OOS_MaxDD,
                           null_OOS_Sharpe=cashp.OOS_Sharpe,
                           v2_OOS_Sharpe=v2["OOS_Sharpe"], v1_OOS_Sharpe=b1["OOS_Sharpe"],
                           spy_OOS_Sharpe=spy["OOS_Sharpe"], spy_OOS_CAGR=spy["OOS_CAGR"],
                           spy_OOS_MaxDD=spy["OOS_MaxDD"]))
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    print(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\n  SUMMARY per chooser (12 cells each): mean OOS Sharpe and win counts")
    summ = W.groupby("chooser").apply(lambda g: pd.Series(dict(
        n=len(g), OOS_Sharpe=g.OOS_Sharpe.mean(), OOS_CAGR=g.OOS_CAGR.mean(), OOS_MaxDD=g.OOS_MaxDD.mean(),
        beats_ctrl=int((g.OOS_Sharpe > g.ctrl_OOS_Sharpe).sum()),
        d_ctrl=(g.OOS_Sharpe - g.ctrl_OOS_Sharpe).mean(),
        beats_null=int((g.OOS_Sharpe > g.null_OOS_Sharpe).sum()),
        beats_v2=int((g.OOS_Sharpe > g.v2_OOS_Sharpe).sum()),
        beats_SPY=int((g.OOS_Sharpe > g.spy_OOS_Sharpe).sum()),
        p4b=int(g.p4b.sum()))), include_groups=False)
    print(summ.to_string(float_format=lambda x: f"{x:.4f}"))
    piv = W.pivot_table(index=["universe", "book", "conv"], columns="chooser", values="OOS_Sharpe")
    print("\n  HEAD TO HEAD, cell by cell (OOS Sharpe):")
    print(piv.to_string(float_format=lambda x: f"{x:.4f}"))
    print(f"\n  S_OWN beats S_CORR out of sample in {int((piv['S_OWN'] > piv['S_CORR']).sum())}/{len(piv)} cells, "
          f"mean gap {(piv['S_OWN'] - piv['S_CORR']).mean():+.4f}")
    print(f"  FREE  beats S_OWN  in {int((piv['FREE'] > piv['S_OWN']).sum())}/{len(piv)}; "
          f"FREE beats S_CORR in {int((piv['FREE'] > piv['S_CORR']).sum())}/{len(piv)}")

    print("\nWritten:", ", ".join(sorted(p.name for p in OUT.parent.glob(OUT.name + ".*"))))


if __name__ == "__main__":
    main()

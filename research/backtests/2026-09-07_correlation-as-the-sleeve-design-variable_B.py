#!/usr/bin/env python3
"""QUEUE idea 103 — correlation-as-the-sleeve-design-variable (lane B, 2026-09-07).

Question (as worded in QUEUE.md)
--------------------------------
"Idea 100 found convexity per pp of CAGR (0.090 vs 0.031) tracks sleeve-to-book correlation
(-0.011..0.212 vs 0.626..0.820) across exactly two sleeves.  Build the curve rather than the
pair: sweep sleeves spanning correlation ~-0.2 to +0.8 by adding equity ETFs back one at a
time, and regress convexity-per-pp on realised correlation.  Is the relationship monotone,
and where does it stop paying?"

Idea 100 has TWO points.  Two points define a slope by construction; they cannot say whether
the slope is a slope, whether it is monotone, or where it flattens.  They also cannot separate
correlation from everything else that moves when the 5 equity ETFs go back in — above all the
sleeve's own standalone return, which rose 2.6% -> 5.0% between S4 and S9.  This run builds
the curve and controls for that.

Design (PROTOCOL rules 1-9)
---------------------------
Panels    : `baseline.load_universe()` (u56, 56) and `load_universe(broad=True)` (B136).  All 9
            macro ETFs are in both.  SURVIVORSHIP: current constituents; levels biased up.
            Cross-panel agreement is a reported control, never a selection.
Sleeves   : idea 18 variant B / idea 26 / idea 100 construction, VERBATIM (vote in {0,1/3,2/3,1}
            on the signs of {12-1, 6m, 3m} x inverse-60d-vol risk parity, row-normalised to 1.0).
            Base = MACRO4 (TLT GLD DBC UUP) = idea 100's S4.  Add-ons = EQ5 (SPY QQQ IWM EFA EEM).
            The queue says "adding equity ETFs back one at a time"; ONE order is one path and a
            path is not a curve, so this runs ALL 2^5 = 32 subsets of EQ5 on top of MACRO4.
            Subset {} is idea 100's S4, subset {all} is idea 100's S9 — both are CONTROLS that
            must reproduce, and the literal one-at-a-time ladder is labelled inside the 32.
Books E   : v1 (live RULES v1 top-5), top20 (idea 2's 4b KEEP), ewall (idea 10's EWall).
            Reported controls, never selected on.
Blend     : natural w = (1-f)E + fS ; matched = the same rescaled per row to E's own gross.
Tuned     : exactly 2 — the SLEEVE (32 compositions) and f in {0,0.25,0.50,0.75,1.00}.
            Lookbacks (252/126/63, 60d vol), gate, gross (75%), cadence (weekly) and costs
            (10 bps) held at the incumbent books' values.
            Grid = 32 sleeves x 5 f x 3 books x 2 panels x 2 conventions = 1920 points,
            ALL reported to `.grid.csv` (f=0 pure book and f=1 pure sleeve are the controls).
Curve     : the idea's own object.  For every interior point (f in {0.25,0.50,0.75}),
              dSharpe(f)   = Sharpe(f) - [(1-f)Sharpe(0) + f Sharpe(1)]      (convexity)
              conv_per_pp  = dSharpe(f) / max(100*(CAGR(0)-CAGR(f)), eps)    (idea 100's units)
            regressed on the sleeve's REALISED daily-return correlation to that same book.
            Reported: OLS slope/R2, Spearman rho, decile bin means (is it monotone?), and the
            correlation at which the curve stops paying (dSharpe <= 0).
Confound  : correlation is not the only thing that moves.  A second regression adds the
            sleeve's OWN standalone CAGR and Sharpe as controls, because adding equity ETFs
            raises both.  If correlation's coefficient dies under that control, the "design
            variable" is return, not correlation.
Rule 8    : REQUIRED and run.  (sleeve, f) chosen jointly on 2009-2016 by IS Sharpe,
            2017-2026 evaluated untouched, per (panel, book, convention).  OOS CAGR/Sharpe/MaxDD
            reported against the LIVE baseline (RULES v2), RULES v1 and SPY, with the
            do-nothing (f=0) anchor and the grid's best OOS arm (regret).
KEEP      : both PROTOCOL paths evaluated on every one of the 1920 points — 4a vs RULES v2
            (live), 4b vs SPY (H1, H2, OOS Sharpe, DD <= 60% of SPY's, CAGR >= 70% of SPY's).
Control   : `fast_backtest` is asserted equal to `products/backtester/engine.backtest` before
            any number below is read.

KNOWN DATA CAVEAT (queue idea 38): data/prices*.csv are indexed on CALENDAR days after
2014-09-17 because BTC-USD is in the download, so post-2014 weekends are zero-return rows.
It hits every arm, the baselines and SPY identically.

Deterministic, standalone:
    python research/backtests/2026-09-07_correlation-as-the-sleeve-design-variable_B.py
"""
import itertools
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd

from baseline import load_universe, rules_v1_weights, rules_v2_weights, score
from engine import backtest, metrics, rebalance_mask

COST_BPS = 10
FREQ = "W"
GROSS = 0.75
MACRO4 = ["TLT", "GLD", "DBC", "UUP"]
EQ5 = ["SPY", "QQQ", "IWM", "EFA", "EEM"]
MOM_LAGS = (252, 126, 63)
VOL_WINDOW = 60
FGRID = [0.00, 0.25, 0.50, 0.75, 1.00]
INTERIOR = [0.25, 0.50, 0.75]
OOS_START = "2017-01-01"
IS_END = "2016-12-31"
OUT = Path(__file__).with_suffix("")
pd.set_option("display.width", 200)


# ---------------------------------------------------------------- engine (verified clone)
def fast_backtest(px, w, cost_bps=COST_BPS, freq=FREQ):
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).fillna(0.0).shift(1).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    nT, nC = rets.shape
    held = np.empty((nT, nC)); turn = np.zeros(nT); cur = np.zeros(nC)
    for i in range(nT):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        g = cur * (1 + rets[i])
        tot = g.sum() + (1 - cur.sum())
        if tot > 0:
            cur = g / tot
    port = np.nansum(held * rets, axis=1) - turn * cost_bps / 1e4
    return pd.Series(port, index=px.index), pd.Series(turn, index=px.index)


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
    sub = px[list(assets)]
    w = (_vote_mom(sub) * _risk_parity(sub)).fillna(0.0)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[list(assets)] = w
    return out


def sleeve_family():
    """All 32 subsets of EQ5 added to MACRO4, ordered by |subset|. Labels are stable."""
    fam = []
    for k in range(len(EQ5) + 1):
        for combo in itertools.combinations(EQ5, k):
            name = "S4" if k == 0 else ("S9" if k == 5 else "S4+" + "".join(t[0] + t[-1] for t in combo))
            fam.append((name, MACRO4 + list(combo), k, "+".join(combo)))
    return fam


# the queue's literal reading: one order, add one at a time. Labelled inside the 32.
ONE_AT_A_TIME = [tuple(EQ5[:k]) for k in range(6)]


# ---------------------------------------------------------------- books
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


# ---------------------------------------------------------------- rows / bars
def full_row(r):
    h = len(r) // 2
    a, b, c = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    o = metrics(r.loc[OOS_START:]); i = metrics(r.loc[:IS_END])
    return dict(CAGR=a["CAGR"], Sharpe=a["Sharpe"], MaxDD=a["MaxDD"], H1=b["Sharpe"], H2=c["Sharpe"],
                IS_Sharpe=i["Sharpe"], OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"])


def keep_4a(row, base):
    return bool(row["H1"] > base["H1"] and row["H2"] > base["H2"] and row["MaxDD"] >= base["MaxDD"])


def keep_4b(row, spy):
    return bool(row["H1"] > spy["H1"] and row["H2"] > spy["H2"] and row["OOS_Sharpe"] > spy["OOS_Sharpe"]
                and row["MaxDD"] >= 0.60 * spy["MaxDD"] and row["CAGR"] >= 0.70 * spy["CAGR"])


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.3f}")


def ols(y, X, names):
    """Plain OLS with an intercept; returns coefficients, t-stats, R2."""
    X = np.column_stack([np.ones(len(y))] + [np.asarray(c, float) for c in X])
    y = np.asarray(y, float)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    n, k = X.shape
    s2 = resid @ resid / max(n - k, 1)
    try:
        se = np.sqrt(np.diag(s2 * np.linalg.pinv(X.T @ X)))
    except np.linalg.LinAlgError:
        se = np.full(k, np.nan)
    ss_tot = ((y - y.mean()) ** 2).sum()
    r2 = 1 - (resid @ resid) / ss_tot if ss_tot > 0 else np.nan
    return pd.DataFrame({"coef": beta, "se": se, "t": beta / se},
                        index=["const"] + list(names)), r2, n


def spearman(a, b):
    a = pd.Series(a).rank(); b = pd.Series(b).rank()
    return float(a.corr(b))


# ---------------------------------------------------------------- main
def main():
    fam = sleeve_family()
    print(f"### idea 103 — correlation-as-the-sleeve-design-variable (lane B, 2026-09-07)")
    print(f"Sleeve family: {len(fam)} compositions = MACRO4 {MACRO4} + every subset of EQ5 {EQ5}")
    print(f"Grid: {len(fam)} sleeves x {len(FGRID)} f x {len(BOOKS)} books x 2 panels x 2 conventions "
          f"= {len(fam)*len(FGRID)*len(BOOKS)*4} points, all written to .grid.csv")
    print(f"Costs {COST_BPS} bps, cadence {FREQ}, t+1 execution, gross {GROSS}.\n")

    panels = {"u56": load_universe(), "B136": load_universe(broad=True)}

    # ---- control: fast_backtest == engine.backtest, asserted before any number is read
    px0 = panels["u56"]
    a = backtest(px0, rules_v1_weights(px0), cost_bps=COST_BPS, freq=FREQ)["returns"]
    b = fast_backtest(px0, rules_v1_weights(px0))[0]
    d = float((a - b).abs().max())
    print(f"CONTROL fast_backtest vs engine.backtest on RULES v1 / u56: max |diff| = {d:.3e}")
    assert d < 1e-12, d

    records, refs, corr_rows, sleeve_rows = [], {}, [], []

    for tag, px in panels.items():
        start = px.index[260]
        print("\n" + "=" * 118)
        print(f"### PANEL {tag}: {px.shape[1]} tickers {px.index[0].date()} -> {px.index[-1].date()} "
              f"| eval from {start.date()}")
        spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
        v2_r = fast_backtest(px, rules_v2_weights(px))[0].loc[start:]
        v1_r = fast_backtest(px, rules_v1_weights(px))[0].loc[start:]
        spy, v2, v1 = full_row(spy_r), full_row(v2_r), full_row(v1_r)
        refs[tag] = (v2, v1, spy)
        print("\nReference rows (same days, same costs):")
        print(fmt(pd.DataFrame({"RULES v2 (live baseline)": v2, "RULES v1 (previous)": v1, "SPY": spy}).T))
        print(f"\n4b bars on {tag}: Sharpe > SPY H1 {spy['H1']:.3f} / H2 {spy['H2']:.3f} / "
              f"OOS {spy['OOS_Sharpe']:.3f} · MaxDD >= {0.60*spy['MaxDD']:.2%} · "
              f"CAGR >= {0.70*spy['CAGR']:.2%}")

        # book returns (for the correlation axis)
        book_w = {bn: bf(px) for bn, bf in BOOKS.items()}
        book_r = {bn: fast_backtest(px, w)[0].loc[start:] for bn, w in book_w.items()}

        for sname, assets, k, combo in fam:
            S = sleeve_weights(px, assets)
            s_r = fast_backtest(px, S)[0].loc[start:]
            srow = full_row(s_r)
            sleeve_rows.append(dict(panel=tag, sleeve=sname, n_eq=k, added=combo,
                                    sleeve_CAGR=srow["CAGR"], sleeve_Sharpe=srow["Sharpe"],
                                    sleeve_MaxDD=srow["MaxDD"],
                                    corr_SPY=float(s_r.corr(spy_r))))
            for bn in BOOKS:
                corr_rows.append(dict(panel=tag, sleeve=sname, n_eq=k, added=combo, book=bn,
                                      corr=float(s_r.corr(book_r[bn]))))
            for bn, E in book_w.items():
                for matched in (False, True):
                    conv = "matched" if matched else "natural"
                    for f in FGRID:
                        w = blend(E, S, f, matched)
                        r, turn = fast_backtest(px, w)
                        r = r.loc[start:]
                        row = full_row(r)
                        row["Turn/yr"] = turn.loc[start:].sum() / (len(r) / 252)
                        row["Gross"] = float(w.loc[start:].sum(axis=1).mean())
                        row["4a"] = keep_4a(row, v2)
                        row["4b"] = keep_4b(row, spy)
                        records.append(dict(panel=tag, sleeve=sname, n_eq=k, added=combo,
                                            book=bn, conv=conv, f=f, **row))

    G = pd.DataFrame(records)
    C = pd.DataFrame(corr_rows)
    SL = pd.DataFrame(sleeve_rows)
    G.to_csv(OUT.with_suffix(".grid.csv"), index=False)
    C.to_csv(OUT.with_suffix(".correlation.csv"), index=False)
    SL.to_csv(OUT.with_suffix(".sleeves.csv"), index=False)
    print(f"\nGrid complete: {len(G)} points written.")

    # ------------------------------------------------------- (0) controls reproduce idea 100
    print("\n" + "=" * 118)
    print("### (0) CONTROL — the two endpoints must reproduce idea 100's published pair")
    print("idea 100 (.correlation.csv): S9 to the 3 books 0.626..0.820, S4 -0.011..0.212;")
    print("median conv_per_pp 0.031 (S9) vs 0.090 (S4). Panel tags there were u56/broad.\n")
    ends = C[C.sleeve.isin(["S4", "S9"])].pivot_table(index=["panel", "book"], columns="sleeve", values="corr")
    print(fmt(ends))
    for s in ("S4", "S9"):
        v = C[C.sleeve == s]["corr"]
        print(f"  {s} to the 3 books, both panels: {v.min():+.3f} .. {v.max():+.3f}")

    # ------------------------------------------------------- (1) the curve
    print("\n" + "=" * 118)
    print("### (1) THE CURVE — convexity and convexity-per-pp against realised correlation")
    print("dSharpe(f) = Sharpe(f) - [(1-f)Sharpe(0) + f Sharpe(1)]; "
          "conv_per_pp = dSharpe / pp of CAGR given up vs f=0\n")
    cmap = {(r.panel, r.sleeve, r.book): r.corr for r in C.itertuples()}
    smap = {(r.panel, r.sleeve): (r.sleeve_CAGR, r.sleeve_Sharpe) for r in SL.itertuples()}
    dv = []
    for (tag, sname, bn, conv), sub in G.groupby(["panel", "sleeve", "book", "conv"], sort=False):
        s = sub.set_index("f")["Sharpe"]; c = sub.set_index("f")["CAGR"]
        sc, ss = smap[(tag, sname)]
        for f in INTERIOR:
            lin = (1 - f) * s[0.0] + f * s[1.0]
            give = 100 * (c[0.0] - c[f])
            dv.append(dict(panel=tag, sleeve=sname, n_eq=int(sub.n_eq.iloc[0]), book=bn, conv=conv, f=f,
                           corr=cmap[(tag, sname, bn)], sleeve_CAGR=sc, sleeve_Sharpe=ss,
                           Sharpe=s[f], dSharpe=s[f] - lin, dCAGR=c[f] - c[0.0], pp_given=give,
                           conv_per_pp=(s[f] - lin) / max(give, 1e-9)))
    D = pd.DataFrame(dv)
    D.to_csv(OUT.with_suffix(".curve.csv"), index=False)
    print(f"{len(D)} interior cells (32 sleeves x 3 f x 3 books x 2 panels x 2 conventions).")

    print("\n-- by number of equity ETFs added (the queue's axis), pooled over books/panels/conv/f:")
    by_k = D.groupby("n_eq").agg(cells=("dSharpe", "size"), corr_mean=("corr", "mean"),
                                 dSharpe_mean=("dSharpe", "mean"), dSharpe_pos=("dSharpe", lambda x: int((x > 0).sum())),
                                 dCAGR_mean=("dCAGR", "mean"),
                                 conv_per_pp_med=("conv_per_pp", "median"),
                                 sleeve_CAGR=("sleeve_CAGR", "mean"))
    print(fmt(by_k))

    print("\n-- the queue's literal one-at-a-time ladder (S4, +SPY, +QQQ, +IWM, +EFA, +EEM):")
    lad_names = []
    for combo in ONE_AT_A_TIME:
        hit = [n for n, a, k, cb in fam if tuple(sorted(cb.split("+") if cb else [])) == tuple(sorted(combo))]
        lad_names.append(hit[0])
    lad = D[D.sleeve.isin(lad_names)].copy()
    lad["order"] = lad.sleeve.map({n: i for i, n in enumerate(lad_names)})
    print(fmt(lad.groupby(["order", "sleeve"]).agg(
        corr=("corr", "mean"), dSharpe=("dSharpe", "mean"),
        conv_per_pp=("conv_per_pp", "median"), sleeve_CAGR=("sleeve_CAGR", "mean"))))

    print("\n-- correlation deciles (is the relationship MONOTONE?):")
    D["cbin"] = pd.qcut(D["corr"], 10, duplicates="drop")
    bins = D.groupby("cbin", observed=True).agg(
        cells=("dSharpe", "size"), corr_mid=("corr", "mean"),
        dSharpe=("dSharpe", "mean"), dSharpe_pos=("dSharpe", lambda x: int((x > 0).sum())),
        conv_per_pp=("conv_per_pp", "median"), pp_given=("pp_given", "mean"))
    print(fmt(bins))
    mono_d = bool(bins["dSharpe"].diff().dropna().le(0).all() or bins["dSharpe"].diff().dropna().ge(0).all())
    mono_c = bool(bins["conv_per_pp"].diff().dropna().le(0).all() or bins["conv_per_pp"].diff().dropna().ge(0).all())
    print(f"\nMonotone across the 10 correlation bins?  dSharpe {mono_d}   conv_per_pp {mono_c}")
    print(f"Spearman(corr, dSharpe)     = {spearman(D['corr'], D['dSharpe']):+.4f}")
    print(f"Spearman(corr, conv_per_pp) = {spearman(D['corr'], D['conv_per_pp']):+.4f}")
    print(f"Spearman(corr, pp_given)    = {spearman(D['corr'], D['pp_given']):+.4f}   "
          f"(what the correlation axis costs in CAGR)")

    # ------------------------------------------------------- (2) the regression
    print("\n" + "=" * 118)
    print("### (2) THE REGRESSION the queue asked for, and the confound it does not control")
    for yname in ("dSharpe", "conv_per_pp"):
        print(f"\n-- {yname} ~ corr   (pooled, n={len(D)})")
        t1, r2a, n1 = ols(D[yname], [D["corr"]], ["corr"])
        print(fmt(t1) + f"    R2 {r2a:.4f}")
        print(f"-- {yname} ~ corr + sleeve_CAGR + sleeve_Sharpe   (the confound: adding equity ETFs")
        print(f"   raises the sleeve's own return as well as its correlation)")
        t2, r2b, _ = ols(D[yname], [D["corr"], D["sleeve_CAGR"], D["sleeve_Sharpe"]],
                         ["corr", "sleeve_CAGR", "sleeve_Sharpe"])
        print(fmt(t2) + f"    R2 {r2b:.4f}")

    print("\n-- the same slope inside every (panel, book, conv, f) cell, so it is not a pooling artefact:")
    slopes = []
    for (tag, bn, conv, f), sub in D.groupby(["panel", "book", "conv", "f"]):
        tb, r2c, nn = ols(sub["conv_per_pp"], [sub["corr"]], ["corr"])
        td, r2d, _ = ols(sub["dSharpe"], [sub["corr"]], ["corr"])
        slopes.append(dict(panel=tag, book=bn, conv=conv, f=f, n=nn,
                           slope_conv_per_pp=tb.loc["corr", "coef"], t_conv=tb.loc["corr", "t"], R2_conv=r2c,
                           slope_dSharpe=td.loc["corr", "coef"], t_dS=td.loc["corr", "t"], R2_dS=r2d,
                           rho_conv=spearman(sub["corr"], sub["conv_per_pp"])))
    SLP = pd.DataFrame(slopes)
    SLP.to_csv(OUT.with_suffix(".slopes.csv"), index=False)
    print(fmt(SLP.set_index(["panel", "book", "conv", "f"])))
    print(f"\nslope(conv_per_pp on corr) negative in {int((SLP.slope_conv_per_pp < 0).sum())}/{len(SLP)} cells; "
          f"slope(dSharpe on corr) negative in {int((SLP.slope_dSharpe < 0).sum())}/{len(SLP)}; "
          f"median R2 {SLP.R2_conv.median():.3f} / {SLP.R2_dS.median():.3f}")

    # ------------------------------------------------------- (3) where does it stop paying
    print("\n" + "=" * 118)
    print("### (3) WHERE DOES IT STOP PAYING — the queue's second question")
    print("Two readings. (a) convexity: the correlation at which dSharpe crosses 0.")
    print("(b) 4b: the correlation above which no arm in the family clears the capital bar.\n")
    for tag, sub in D.groupby("panel"):
        neg = sub[sub.dSharpe <= 0]
        print(f"{tag}: dSharpe <= 0 in {len(neg)}/{len(sub)} interior cells"
              + (f"; those sit at corr {neg['corr'].min():+.3f}..{neg['corr'].max():+.3f}" if len(neg) else ""))
    hi = D[D["corr"] > 0.5]; lo = D[D["corr"] < 0.2]
    print(f"\ncorr > 0.50 ({len(hi)} cells): dSharpe mean {hi.dSharpe.mean():+.4f}, "
          f"conv_per_pp median {hi.conv_per_pp.median():.4f}, CAGR given up {hi.pp_given.mean():.2f} pp")
    print(f"corr < 0.20 ({len(lo)} cells): dSharpe mean {lo.dSharpe.mean():+.4f}, "
          f"conv_per_pp median {lo.conv_per_pp.median():.4f}, CAGR given up {lo.pp_given.mean():.2f} pp")

    inner = G[(G.f > 0) & (G.f < 1)]
    print(f"\n-- KEEP census over all {len(G)} points: 4a {int(G['4a'].sum())}, 4b {int(G['4b'].sum())}")
    print(f"   interior only ({len(inner)}): 4a {int(inner['4a'].sum())}, 4b {int(inner['4b'].sum())}")
    ib = inner.merge(C, on=["panel", "sleeve", "book"], how="left")
    print("\n-- 4a / 4b pass rate by number of equity ETFs in the sleeve:")
    print(fmt(ib.groupby("n_eq_x").agg(cells=("4b", "size"), corr_mean=("corr", "mean"),
                                       pass_4a=("4a", "sum"), pass_4b=("4b", "sum"))))
    if int(ib["4b"].sum()):
        p4 = ib[ib["4b"]]
        print(f"\n-- the {len(p4)} interior 4b passes, by correlation:")
        print(fmt(p4.sort_values("corr")[["panel", "sleeve", "book", "conv", "f", "corr",
                                          "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe",
                                          "Turn/yr"]].set_index(["panel", "sleeve", "book", "conv", "f"])))
        print(f"\n4b passes span corr {p4['corr'].min():+.3f} .. {p4['corr'].max():+.3f}; "
              f"highest-correlation pass at {p4['corr'].max():+.3f}")
        best = p4.sort_values("OOS_Sharpe", ascending=False).head(5)
        print("\n-- best 5 interior 4b passes by OOS Sharpe:")
        print(fmt(best[["panel", "sleeve", "book", "conv", "f", "corr", "CAGR", "Sharpe", "MaxDD",
                        "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "Turn/yr"]]
                  .set_index(["panel", "sleeve", "book", "conv", "f"])))

    # ------------------------------------------------------- (4) rule 8
    print("\n" + "=" * 118)
    print("### (4) PROTOCOL rule 8 — (sleeve, f) chosen JOINTLY on 2009-2016 by IS Sharpe,")
    print("2017-2026 evaluated untouched. 160 arms per cell (32 sleeves x 5 f).\n")
    wf = []
    for (tag, bn, conv), sub in G.groupby(["panel", "book", "conv"]):
        v2, v1, spy = refs[tag]
        pick = sub.loc[sub["IS_Sharpe"].idxmax()]
        anchor = sub[sub.f == 0.0].iloc[0]
        wf.append(dict(panel=tag, book=bn, conv=conv, sleeve_star=pick["sleeve"], f_star=pick["f"],
                       n_eq_star=int(pick["n_eq"]), corr_star=cmap[(tag, pick["sleeve"], bn)],
                       IS_Sharpe=pick["IS_Sharpe"],
                       OOS_CAGR=pick["OOS_CAGR"], OOS_Sharpe=pick["OOS_Sharpe"], OOS_MaxDD=pick["OOS_MaxDD"],
                       anchor_OOS_Sharpe=anchor["OOS_Sharpe"], anchor_OOS_CAGR=anchor["OOS_CAGR"],
                       best_OOS_in_grid=sub["OOS_Sharpe"].max(),
                       regret=pick["OOS_Sharpe"] - sub["OOS_Sharpe"].max(),
                       v2_OOS_Sharpe=v2["OOS_Sharpe"], v1_OOS_Sharpe=v1["OOS_Sharpe"],
                       spy_OOS_Sharpe=spy["OOS_Sharpe"], spy_OOS_CAGR=spy["OOS_CAGR"],
                       spy_OOS_MaxDD=spy["OOS_MaxDD"],
                       beats_anchor=bool(pick["OOS_Sharpe"] > anchor["OOS_Sharpe"]),
                       beats_SPY=bool(pick["OOS_Sharpe"] > spy["OOS_Sharpe"]),
                       beats_v2=bool(pick["OOS_Sharpe"] > v2["OOS_Sharpe"]),
                       full_4b=bool(pick["4b"]), full_4a=bool(pick["4a"])))
    W = pd.DataFrame(wf)
    W.to_csv(OUT.with_suffix(".walkforward.csv"), index=False)
    print(fmt(W.set_index(["panel", "book", "conv"])[
        ["sleeve_star", "f_star", "n_eq_star", "corr_star", "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe",
         "OOS_MaxDD", "anchor_OOS_Sharpe", "regret", "spy_OOS_Sharpe", "v2_OOS_Sharpe",
         "beats_anchor", "beats_SPY", "beats_v2", "full_4b"]]))
    print(f"\nrule 8 picks f=0 (no sleeve) in {int((W.f_star == 0).sum())}/{len(W)} cells; "
          f"beats its own no-sleeve anchor OOS in {int(W.beats_anchor.sum())}/{len(W)}; "
          f"beats SPY OOS in {int(W.beats_SPY.sum())}/{len(W)}; "
          f"beats RULES v2 OOS in {int(W.beats_v2.sum())}/{len(W)}; "
          f"mean regret {W.regret.mean():+.4f}")
    print(f"IS-chosen sleeve correlation: {W.corr_star.min():+.3f}..{W.corr_star.max():+.3f}; "
          f"n_eq chosen {sorted(W.n_eq_star.unique())}; 4b at the pick {int(W.full_4b.sum())}/{len(W)}")

    print("\n-- rule 8 restricted to the CORRELATION question: within each cell, does the IS chooser")
    print("   pick a LOW-correlation sleeve, and would a pre-registered 'lowest-correlation sleeve'")
    print("   rule (zero fitting on the sleeve axis, f still chosen IS) have done better OOS?")
    pre = []
    for (tag, bn, conv), sub in G.groupby(["panel", "book", "conv"]):
        v2, v1, spy = refs[tag]
        s4 = sub[sub.sleeve == "S4"]
        pk = s4.loc[s4["IS_Sharpe"].idxmax()]
        full = sub.loc[sub["IS_Sharpe"].idxmax()]
        pre.append(dict(panel=tag, book=bn, conv=conv,
                        S4_f_star=pk["f"], S4_OOS_Sharpe=pk["OOS_Sharpe"], S4_OOS_CAGR=pk["OOS_CAGR"],
                        S4_OOS_MaxDD=pk["OOS_MaxDD"], S4_4b=bool(pk["4b"]),
                        free_sleeve=full["sleeve"], free_OOS_Sharpe=full["OOS_Sharpe"],
                        delta=pk["OOS_Sharpe"] - full["OOS_Sharpe"],
                        spy_OOS=spy["OOS_Sharpe"]))
    P = pd.DataFrame(pre)
    P.to_csv(OUT.with_suffix(".preregistered.csv"), index=False)
    print(fmt(P.set_index(["panel", "book", "conv"])))
    print(f"\npre-registering the lowest-correlation sleeve (S4) beats the free sleeve choice OOS in "
          f"{int((P.delta > 0).sum())}/{len(P)} cells, mean delta {P.delta.mean():+.4f}")

    print(f"\nWritten: {OUT.name}.grid.csv / .correlation.csv / .sleeves.csv / .curve.csv / "
          f".slopes.csv / .walkforward.csv / .preregistered.csv")


if __name__ == "__main__":
    main()

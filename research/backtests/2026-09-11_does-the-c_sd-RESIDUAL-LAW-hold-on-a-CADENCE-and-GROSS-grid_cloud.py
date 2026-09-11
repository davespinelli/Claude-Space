#!/usr/bin/env python3
"""Idea 539 - "does-the-c_sd-RESIDUAL-LAW-hold-on-a-CADENCE-and-GROSS-grid"
(cloud lane, 2026-09-11).

The question
------------
Idea 535 replaced idea 301's GATE FAMILY constant for the de-grossing timing residual with a
continuous predictor and published the fit

    resid0_pp  =  -0.0209  +  (-1.5722) * c_sd(IS)        t = -0.87 | -6.32,  IS R2 0.1996,
                                                          162 cells, OOS MAE 0.1771 vs 0.1936

Every one of those 162 cells was run at a FIXED gross of 0.75 and at three cadences (W, M, Q).
The queue's objection: c_sd is the SD of the book's exposure path and gross is the one input
that scales exposure directly, so a slope quoted in pp per unit c_sd may be a 0.75-specific
number rather than a law.  This run re-cuts the whole decomposition at gross in
{0.50, 0.75, 1.00} and adds DAILY cadence, and reports whether the slope is invariant.

What the construction predicts before any number is read (pre-registered)
------------------------------------------------------------------------
    c_t = gross(DEGROSS_t) / gross(RESPREAD_t) is a RATIO of two books that carry the same
    gross, so c_t - and therefore c_bar and c_sd - are INVARIANT in gross by construction.
    resid0_pp is a CAGR gap in pp/yr between two books whose returns both scale roughly with
    gross, so the residual should scale roughly LINEARLY in gross.
    => the slope in pp per unit c_sd should scale ~ g / 0.75, i.e. the LEVEL -1.5722 is a
       0.75 number, while slope / g should be the invariant.  Both are reported.
    This is a prediction, not a result; the run measures how close to it the grid lands, and
    the c_sd-invariance leg is checked to machine tolerance rather than assumed.

Tuned parameters (PROTOCOL rule 4: at most two) - ALL grid points reported
    1. gross    in {0.50, 0.75, 1.00}
    2. cadence  in {D, W, M, Q}      (D is the queue's addition; W/M/Q are idea 535's)
    Panels (3), gate families (2) and strictness levels (9) are INHERITED from ideas 298/301/535
    verbatim and are reported axes, never tuned.  Predictor forms are restricted to the three
    the queue's claim is about (ZERO / GLOBAL / FAMILY incumbent, and CSD.is), fitted exactly as
    idea 535 fits them; the shrinkage ladder is inherited at its published values.

Grid: 3 panels x 2 families x 9 levels x 4 cadences x 3 gross x 2 constructions = 1,296 books,
      648 decomposition cells, each decomposed on FULL / IS / OOS windows.

How the answer is decided (pre-registered, before any number below was read)
    INVARIANT      the gross-normalised slope (slope / g) is within its own cross-gross spread,
                   AND the retirement bar (CSD.is OOS MAE <= 0.95 * FAMILY OOS MAE) holds at
                   EVERY gross and at every cadence set.
    0.75-SPECIFIC  either the normalised slope moves monotonically with gross beyond that
                   spread, or the retirement bar flips sign at some gross.
    Reported either way; a KILL of the law is the useful result.

Rule 8 walk-forward (PROTOCOL rule 8, required)
    WF-A  THE BOOK.  Inside each panel x family arm, (level, cadence, gross, construction) is
          chosen on IS (<= 2016-12-31) by IS Sharpe ALONE and the pick is read ONCE on the
          untouched OOS window, reported as OOS CAGR / Sharpe / MaxDD against RULES v2 (the
          live book, PROTOCOL rule 3) and SPY.  Both KEEP paths are evaluated on every one of
          the 1,296 books and on every pick.
    WF-B  THE DELIVERABLE.  The estimator itself is a walk-forward: CSD.is is fitted on the IS
          cells only and scored ONCE on the OOS cells, separately at each gross.

Gates, asserted before any new number is read
    G1  fast_backtest == engine.backtest to 1e-12 on a sample of books (the grid is 1,296
        books; the engine's per-row pandas loop is replaced by an exact numpy clone).
    G2  at gross 0.75 and cadences W/M/Q the recomputed decomposition reproduces idea 535's
        committed .decomp.csv: max |d resid0_pp| < 1e-2 pp, max |d c_sd| < 1e-4 (idea 535's
        own allowance for the daily drift of data/prices.csv, ideas 513/515).
    G3  the published fit is reproduced: CSD.is slope -1.5722, t -6.32 on those 162 cells.
    G4  c_t is invariant in gross to 1e-12 (the construction claim above, checked not assumed).

Costs 10 bps per unit turnover; the 0-bps rung is DERIVED exactly (r0 = r10 + turnover*bps/1e4),
never re-run, so it is the same book.  Weights decided at close t, applied at t+1.  No shorting,
no leverage: gross 1.00 is fully invested, never above.

SURVIVORSHIP (idea 54, data/SMALL_PANEL_README.md): prices_small.csv.gz, universe.json and
universe_broad.json are CURRENT constituents, no delistings, so every CAGR LEVEL here is
inflated and the 4a / 4b columns inherit that whole.  The headline object is an arm-minus-arm
contrast on the SAME names and days (DEGROSS and RESPREAD share one gate mask), so the bias
very largely cancels out of gap0 / pred0 / resid0; it does NOT cancel out of the KEEP columns.
SMALL439 drops every ticker with max_1d_move >= 1.0 in data/small_meta.csv before use.

Outputs: .grid.csv .decomp.csv .slopes.csv .estimator.csv .walkforward.csv .console.txt .result.md
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
sys.path.insert(0, str(REPO / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask  # noqa: E402

COST_BPS = 10
GROSSES = [0.50, 0.75, 1.00]                 # tuned param 1
CADENCES = ["D", "W", "M", "Q"]              # tuned param 2
CAD535 = ["W", "M", "Q"]
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]
QUANT_X = [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95]
MA_THETA = [0.30, 0.20, 0.12, 0.06, 0.00, -0.06, -0.12, -0.25, -0.40]
FAMILIES = ["QUANTILE", "MA-THRESH"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
LAMBDAS = [0.00, 0.25, 0.50, 0.75, 1.00]
FORMS = ["ZERO", "GLOBAL", "FAMILY", "CSD.is"]
B1A_RATIO = 0.95
B3_TOL_PP, B3_TOL_CSD = 1e-2, 1e-4
REF535 = REPO / "research" / "backtests" / (
    "2026-09-09_is-the-FAMILY-constant-really-a-c_sd-constant_cloud.decomp.csv")
PUB_SLOPE, PUB_T = -1.5722, -6.32

OUT = Path(__file__).with_suffix("")
LOG = []
pd.set_option("display.width", 240)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 900)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


def ols(X, y):
    X, y = np.asarray(X, float), np.asarray(y, float)
    n, p = X.shape
    XtXi = np.linalg.pinv(X.T @ X)
    b = XtXi @ (X.T @ y)
    e = y - X @ b
    ssr = float(e @ e)
    sst = float(((y - y.mean()) ** 2).sum())
    dof = max(1, n - p)
    se = np.sqrt(np.maximum(np.diag(XtXi * (ssr / dof)), 0))
    t = np.where(se > 0, b / np.where(se > 0, se, 1.0), np.nan)
    return dict(b=b, t=t, R2=(1 - ssr / sst if sst > 0 else np.nan), n=n)


# ---------------------------------------------------------------- exact numpy clone of engine
def fast_backtest(prices, weights, cost_bps, freq, _ret_cache={}):
    """Bit-for-bit clone of engine.backtest with the per-row pandas indexing removed.
    Gated against the engine in G1; used only because the grid is 1,296 books."""
    idx = prices.index
    ck = (id(prices), prices.shape)
    if ck not in _ret_cache:
        _ret_cache[ck] = prices.pct_change().fillna(0.0).values
    rets = _ret_cache[ck]
    W = weights.reindex(idx).fillna(0.0).shift(1).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values
    n = len(idx)
    held = np.empty_like(rets)
    turn = np.zeros(n)
    cur = np.zeros(rets.shape[1])
    for i in range(n):
        if mask[i] or i == 0:
            new = W[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return {"returns": pd.Series(port, index=idx), "turnover": pd.Series(turn, index=idx),
            "gross": pd.Series(held.sum(axis=1), index=idx)}


# ---------------------------------------------------------------- idea 298/301/535 constructions
def panels():
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv = [c for c in pxs.columns if c != "SPY" and c not in bad]
    px56 = load_universe()
    px136 = load_universe(broad=True)
    out = {"SMALL439": (pxs[inv], pxs["SPY"]),
           "U56": (px56[[c for c in px56.columns if c != "SPY"]], px56["SPY"]),
           "B136": (px136[[c for c in px136.columns if c != "SPY"]], px136["SPY"])}
    P(f"panels: SMALL439 {out['SMALL439'][0].shape[1]} names ({len(bad)} dropped for "
      f"max_1d_move >= 1.0; SURVIVORSHIP: current constituents only), "
      f"U56 {out['U56'][0].shape[1]}, B136 {out['B136'][0].shape[1]}")
    return out


def live_mask(px):
    return px.notna() & px.shift(1).notna()


def gate_mask(px, family, level):
    live = live_mask(px)
    ma = px.rolling(200).mean()
    if family == "MA-THRESH":
        return (px > ma * (1 + level)) & live
    dist = (px / ma - 1).where(live)
    n = live.sum(axis=1)
    kt = np.ceil(level * n).astype(int).clip(lower=1)
    rank = dist.rank(axis=1, ascending=False, method="first")
    return rank.le(kt, axis=0).fillna(False) & live


def book(px, family, level, construction, gross, _mc={}):
    k = (id(px), family, level)
    if k not in _mc:
        _mc[k] = gate_mask(px, family, level)
    g = _mc[k]
    if construction == "RESPREAD":
        return g.astype(float).div(g.sum(axis=1).clip(lower=1), axis=0) * gross
    return g.astype(float).div(live_mask(px).sum(axis=1).clip(lower=1), axis=0) * gross


def stat(r):
    h = len(r) // 2
    m, mi, mo = metrics(r), metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                isCAGR=mi["CAGR"], isSharpe=mi["Sharpe"], isMaxDD=mi["MaxDD"],
                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"])


def verdict_4a(s, b):
    return bool(s["H1"] > b["H1"] and s["H2"] > b["H2"] and s["MaxDD"] >= b["MaxDD"])


def fail_4b(s, spy):
    t = {"H1": s["H1"] > spy["H1"], "H2": s["H2"] > spy["H2"],
         "OOS": s["oSharpe"] > spy["oSharpe"],
         "DD": abs(s["MaxDD"]) <= 0.60 * abs(spy["MaxDD"]),
         "CAGR": s["CAGR"] >= 0.70 * spy["CAGR"]}
    f = [k for k, v in t.items() if not v]
    return ",".join(f) if f else "-"


def cagr(r):
    return metrics(r)["CAGR"]


def design(form, df):
    one = np.ones(len(df))
    if form == "CSD.is":
        return np.column_stack([one, df.c_sd_is.values]), ["const", "c_sd(IS)"]
    raise KeyError(form)


def predict(form, lam, IS, OOS, fits=None, tag=""):
    gmean = float(IS.resid0_pp.mean())
    if form == "ZERO":
        return pd.Series(0.0, index=OOS.index)
    if form == "GLOBAL":
        local = pd.Series(gmean, index=OOS.index)
    elif form == "FAMILY":
        mp = IS.groupby("family").resid0_pp.mean()
        local = pd.Series(mp.reindex(pd.Index(OOS.family)).values, index=OOS.index).fillna(gmean)
    else:
        Xi, nm = design(form, IS)
        f = ols(Xi, IS.resid0_pp.values)
        if fits is not None:
            fits.append(dict(tag=tag, form=form, terms="|".join(nm),
                             coef="|".join(f"{b:.4f}" for b in f["b"]),
                             tstat="|".join(f"{t:.2f}" for t in f["t"]),
                             slope=f["b"][-1], slope_t=f["t"][-1], IS_R2=f["R2"], n=f["n"]))
        Xo, _ = design(form, OOS)
        local = pd.Series(Xo @ f["b"], index=OOS.index)
    return lam * local + (1 - lam) * gmean


def mae(pred, truth):
    return float(np.abs(np.asarray(pred, float) - np.asarray(truth, float)).mean())


# ---------------------------------------------------------------- main
def main():
    P("=" * 160)
    P("Idea 539 does-the-c_sd-RESIDUAL-LAW-hold-on-a-CADENCE-and-GROSS-grid (cloud) | "
      + Path(__file__).name)
    P("=" * 160)
    P(f"costs {COST_BPS} bps (0-bps rung DERIVED r0 = r10 + turnover*bps/1e4), next-day "
      f"execution, no shorting/leverage.  IS <= {IS_END}, OOS >= {OOS_START} (PROTOCOL rule 8).")
    P(f"tuned dials: GROSS {GROSSES} x CADENCE {CADENCES}.  ALL grid points reported.")
    P(f"published object under test: CSD.is slope {PUB_SLOPE} (t {PUB_T}) on idea 535's 162 cells.")
    PN = panels()

    # ---------------- G1: the numpy clone
    P("\n" + "=" * 160)
    P("G1 fast_backtest == engine.backtest")
    P("=" * 160)
    g1 = 0.0
    px_probe = PN["U56"][0]
    for fam, lvl, con, g, cad in [("MA-THRESH", 0.06, "DEGROSS", 0.75, "W"),
                                  ("QUANTILE", 0.40, "RESPREAD", 0.50, "M"),
                                  ("MA-THRESH", -0.25, "RESPREAD", 1.00, "D"),
                                  ("QUANTILE", 0.95, "DEGROSS", 1.00, "Q")]:
        w = book(px_probe, fam, lvl, con, g)
        a = backtest(px_probe, w, cost_bps=COST_BPS, freq=cad)
        b = fast_backtest(px_probe, w, COST_BPS, cad)
        d = float((a["returns"] - b["returns"]).abs().iloc[1:].max())
        dt = float((a["turnover"] - b["turnover"]).abs().iloc[1:].max())
        dg = float((a["weights"].sum(axis=1) - b["gross"]).abs().iloc[1:].max())
        g1 = max(g1, d, dt, dg)
        P(f"  {fam:10s} lvl {lvl:+.2f} {con:8s} g {g:.2f} {cad}: max |d returns| {d:.3e} "
          f"turnover {dt:.3e} gross {dg:.3e}")
    P(f"  G1 max deviation {g1:.3e}  ->  {'PASS' if g1 < 1e-12 else 'FAIL'}")
    if g1 >= 1e-12:
        P("  G1 FAILED - stopping")
        flush_log()
        return

    # ---------------- the grid
    P("\n" + "=" * 160)
    P("GRID: 3 panels x 2 families x 9 levels x 4 cadences x 3 gross x 2 constructions")
    P("=" * 160)
    rows, decomp, ctxt = [], [], {}
    for pname, (px, spy_px) in PN.items():
        start = px.index[260]
        years = len(px.loc[start:]) / 252
        spy_s = stat(spy_px.pct_change().fillna(0.0).loc[start:])
        px_u = load_universe()
        live_full = backtest(px_u, rules_v2_weights(px_u), cost_bps=COST_BPS,
                             freq="W")["returns"]
        live_s = stat(live_full.reindex(px.index).fillna(0.0).loc[start:])
        P(f"\nPANEL {pname}  eval from {start.date()} ({years:.2f} yrs)")
        P(f"  SPY      CAGR {spy_s['CAGR']:.4f} Sharpe {spy_s['Sharpe']:.4f} "
          f"MaxDD {spy_s['MaxDD']:.4f} H1/H2 {spy_s['H1']:.3f}/{spy_s['H2']:.3f} "
          f"OOS S {spy_s['oSharpe']:.4f} OOS CAGR {spy_s['oCAGR']:.4f} "
          f"OOS DD {spy_s['oMaxDD']:.4f}")
        P(f"  RULES v2 CAGR {live_s['CAGR']:.4f} Sharpe {live_s['Sharpe']:.4f} "
          f"MaxDD {live_s['MaxDD']:.4f} H1/H2 {live_s['H1']:.3f}/{live_s['H2']:.3f} "
          f"OOS S {live_s['oSharpe']:.4f} OOS CAGR {live_s['oCAGR']:.4f} "
          f"OOS DD {live_s['oMaxDD']:.4f}")
        ctxt[pname] = (spy_s, live_s)
        for family in FAMILIES:
            levels = QUANT_X if family == "QUANTILE" else MA_THETA
            for level in levels:
                for cad in CADENCES:
                    for gross in GROSSES:
                        got = {}
                        for con in CONSTRUCTIONS:
                            res = fast_backtest(px, book(px, family, level, con, gross),
                                                COST_BPS, cad)
                            r10 = res["returns"].loc[start:]
                            turn = res["turnover"].loc[start:]
                            r0 = r10 + turn * COST_BPS / 1e4
                            s = stat(r10)
                            got[con] = dict(r0=r0, gross=res["gross"].loc[start:], s=s)
                            rows.append(dict(panel=pname, family=family, level=level, cad=cad,
                                             gross=gross, con=con, **s, CAGR0=cagr(r0),
                                             turn_yr=turn.sum() / years,
                                             p4a=verdict_4a(s, live_s), f4b=fail_4b(s, spy_s)))
                        dg, rs = got["DEGROSS"], got["RESPREAD"]
                        c_t = (dg["gross"] / rs["gross"].replace(0, np.nan)).fillna(0.0)
                        ident = float((dg["r0"] - c_t * rs["r0"]).abs().max())
                        for tag, lo, hi in (("FULL", None, None), ("IS", None, IS_END),
                                            ("OOS", OOS_START, None)):
                            sl = slice(lo, hi)
                            rr, rd = rs["r0"].loc[sl], dg["r0"].loc[sl]
                            cb = float(c_t.loc[sl].mean())
                            g0 = 100 * (cagr(rd) - cagr(rr))
                            p0 = 100 * (cagr(cb * rr) - cagr(rr))
                            decomp.append(dict(panel=pname, family=family, level=level, cad=cad,
                                               gross=gross, ident_max_err=ident, window=tag,
                                               c_bar=cb, c_sd=float(c_t.loc[sl].std()),
                                               gap0_pp=g0, pred0_pp=p0, resid0_pp=g0 - p0,
                                               CAGR_rs0=cagr(rr), CAGR_dg0=cagr(rd)))
            P(f"  ... {pname} / {family} done "
              f"({len(levels) * len(CADENCES) * len(GROSSES) * 2} books)")
            flush_log()

    G = pd.DataFrame(rows)
    D = pd.DataFrame(decomp)
    G["p4b"] = G.f4b == "-"
    G.to_csv(f"{OUT}.grid.csv", index=False)
    D.to_csv(f"{OUT}.decomp.csv", index=False)
    P(f"\nbooks {len(G)}  decomposition cells {len(D) // 3}  identity max |r_dg - c_t*r_rs| "
      f"{D.ident_max_err.max():.3e}")

    # ---------------- G4 c_t invariance in gross
    P("\n" + "=" * 160)
    P("G4 is c_t (hence c_bar and c_sd) INVARIANT in gross, as the construction implies?")
    P("=" * 160)
    key4 = ["panel", "family", "level", "cad", "window"]
    w = D.pivot_table(index=key4, columns="gross", values=["c_bar", "c_sd"])
    dcb = float((w["c_bar"][0.50] - w["c_bar"][1.00]).abs().max())
    dcs = float((w["c_sd"][0.50] - w["c_sd"][1.00]).abs().max())
    P(f"  max |c_bar(g=0.50) - c_bar(g=1.00)| = {dcb:.3e}")
    P(f"  max |c_sd (g=0.50) - c_sd (g=1.00)| = {dcs:.3e}")
    g4 = max(dcb, dcs) < 1e-12
    P(f"  G4 {'PASS - c_sd is a gross-free axis' if g4 else 'FAIL - c_sd moves with gross'}")

    # ---------------- G2 reproduction vs idea 535
    P("\n" + "=" * 160)
    P("G2 REPRODUCTION vs idea 535's committed .decomp.csv (gross 0.75, cadences W/M/Q)")
    P("=" * 160)
    key = ["panel", "family", "level", "cad", "window"]
    ref = pd.read_csv(REF535)
    mine = D[(D.gross == 0.75) & (D.cad.isin(CAD535))]
    m = mine.merge(ref[key + ["resid0_pp", "gap0_pp", "pred0_pp", "c_bar", "c_sd"]], on=key,
                   suffixes=("", "_ref"))
    P(f"  matched rows: {len(m)} of {len(mine)} recomputed and {len(ref)} committed")
    for c in ["resid0_pp", "gap0_pp", "pred0_pp", "c_bar", "c_sd"]:
        m[f"d_{c}"] = (m[c] - m[f"{c}_ref"]).abs()
    P(fmt(m.groupby("panel")[["d_resid0_pp", "d_gap0_pp", "d_pred0_pp", "d_c_bar",
                              "d_c_sd"]].max(), 8))
    b3r, b3c = float(m.d_resid0_pp.max()), float(m.d_c_sd.max())
    g2 = (b3r < B3_TOL_PP) and (b3c < B3_TOL_CSD)
    P(f"  max |d resid0_pp| {b3r:.3e} pp (bar {B3_TOL_PP}), max |d c_sd| {b3c:.3e} "
      f"(bar {B3_TOL_CSD})  ->  G2 {'PASS' if g2 else 'FAIL'}")

    # ---------------- cells
    def cells_for(gross, cads):
        s = D[(D.gross == gross) & (D.cad.isin(cads))]
        IS = s[s.window == "IS"].sort_values(key[:4]).reset_index(drop=True)
        OO = s[s.window == "OOS"].sort_values(key[:4]).reset_index(drop=True)
        assert (IS[key[:4]].values == OO[key[:4]].values).all()
        C = IS[key[:4]].copy()
        C["c_sd_is"], C["c_bar_is"] = IS.c_sd.values, IS.c_bar.values
        C["resid_is"], C["resid_oos"] = IS.resid0_pp.values, OO.resid0_pp.values
        return C

    # ---------------- G3 the published fit
    P("\n" + "=" * 160)
    P("G3 reproduce idea 535's published CSD.is fit on its own 162 cells")
    P("=" * 160)
    C535 = cells_for(0.75, CAD535)
    f535 = ols(np.column_stack([np.ones(len(C535)), C535.c_sd_is.values]), C535.resid_is.values)
    P(f"  n {f535['n']}  const {f535['b'][0]:+.4f} (t {f535['t'][0]:.2f})  "
      f"c_sd(IS) {f535['b'][1]:+.4f} (t {f535['t'][1]:.2f})  IS R2 {f535['R2']:.4f}")
    P(f"  published: {PUB_SLOPE:+.4f} (t {PUB_T:.2f}), IS R2 0.1996")
    g3 = abs(f535["b"][1] - PUB_SLOPE) < 5e-3 and abs(f535["t"][1] - PUB_T) < 0.10
    P(f"  G3 {'PASS' if g3 else 'FAIL'}  |d slope| {abs(f535['b'][1]-PUB_SLOPE):.5f}  "
      f"|d t| {abs(f535['t'][1]-PUB_T):.4f}")
    for k, v in (("G1", True), ("G2", g2), ("G3", g3), ("G4", g4)):
        P(f"  GATE {k}: {'PASS' if v else 'FAIL'}")
    flush_log()

    # ---------------- THE HEADLINE: the slope across the gross x cadence grid
    P("\n" + "=" * 160)
    P("HEADLINE: the CSD.is slope at every (gross x cadence-set) grid point, ALL reported")
    P("=" * 160)
    slopes = []
    cadsets = {"W/M/Q (idea 535)": CAD535, "D only": ["D"], "D/W/M/Q (all)": CADENCES}
    for gross in GROSSES:
        for cname, cads in cadsets.items():
            C = cells_for(gross, cads)
            for wtag, col in (("IS", "resid_is"), ("OOS", "resid_oos")):
                f = ols(np.column_stack([np.ones(len(C)), C.c_sd_is.values]), C[col].values)
                slopes.append(dict(gross=gross, cadset=cname, window=wtag, n=f["n"],
                                   const=f["b"][0], const_t=f["t"][0], slope=f["b"][1],
                                   slope_t=f["t"][1], R2=f["R2"],
                                   slope_per_gross=f["b"][1] / gross,
                                   pred_if_linear=PUB_SLOPE * gross / 0.75))
    S = pd.DataFrame(slopes)
    S.to_csv(f"{OUT}.slopes.csv", index=False)
    P(fmt(S.set_index(["cadset", "window", "gross"]).sort_index()))

    P("\n  gross-normalised slope (slope / g) - the invariance test:")
    for cname in cadsets:
        for wtag in ("IS", "OOS"):
            s = S[(S.cadset == cname) & (S.window == wtag)].sort_values("gross")
            v = s.slope_per_gross.values
            P(f"    {cname:18s} {wtag:3s}  " + "  ".join(
                f"g={g:.2f}: {x:+.4f}" for g, x in zip(s.gross, v))
              + f"   spread {v.max()-v.min():+.4f}  ratio hi/lo {v.max()/v.min():.3f}")
    P("\n  RAW slope vs the 'scales with g' prediction (-1.5722 * g / 0.75):")
    for cname in cadsets:
        s = S[(S.cadset == cname) & (S.window == "IS")].sort_values("gross")
        P(f"    {cname:18s}  " + "  ".join(
            f"g={g:.2f}: {a:+.4f} vs {b:+.4f} ({a/b:.3f}x)"
            for g, a, b in zip(s.gross, s.slope, s.pred_if_linear)))

    # ---------------- WF-B the estimator ladder at every gross
    P("\n" + "=" * 160)
    P("WF-B THE ESTIMATOR LADDER: every form fitted on IS cells, scored ONCE on OOS cells")
    P("=" * 160)
    est, fits = [], []
    for gross in GROSSES:
        for cname, cads in cadsets.items():
            C = cells_for(gross, cads)
            IS = C.rename(columns={"resid_is": "resid0_pp"})
            OO = C.rename(columns={"resid_oos": "resid0_pp"})
            for form in FORMS:
                for lam in LAMBDAS:
                    p = predict(form, lam, IS, OO, fits if lam == 1.0 else None,
                                tag=f"g{gross:.2f}|{cname}")
                    est.append(dict(gross=gross, cadset=cname, form=form, lam=lam, n=len(C),
                                    OOS_MAE=mae(p, OO.resid0_pp.values)))
    E = pd.DataFrame(est)
    E.to_csv(f"{OUT}.estimator.csv", index=False)
    P(fmt(pd.DataFrame(fits).set_index(["tag", "form"])[["coef", "tstat", "IS_R2", "n"]]
          if fits else pd.DataFrame()))
    for cname in cadsets:
        P(f"\n  OOS MAE (pp/yr), cadence set = {cname}:")
        P(fmt(E[E.cadset == cname].pivot_table(index=["gross", "form"], columns="lam",
                                               values="OOS_MAE")))
    P("\n  RETIREMENT BAR B1a (CSD.is lam=1 OOS MAE <= 0.95 x FAMILY lam=1 OOS MAE):")
    bar = []
    for gross in GROSSES:
        for cname in cadsets:
            s = E[(E.gross == gross) & (E.cadset == cname) & (E.lam == 1.0)].set_index("form")
            fa, cs = float(s.loc["FAMILY", "OOS_MAE"]), float(s.loc["CSD.is", "OOS_MAE"])
            bar.append(dict(gross=gross, cadset=cname, FAMILY=fa, CSD_is=cs, ratio=cs / fa,
                            B1a=cs <= B1A_RATIO * fa))
    B = pd.DataFrame(bar)
    P(fmt(B.set_index(["cadset", "gross"])))
    P(f"  B1a holds at {int(B.B1a.sum())} of {len(B)} (gross x cadence-set) points")

    # ---------------- WF-A the book
    P("\n" + "=" * 160)
    P("WF-A THE BOOK: (level, cadence, gross, construction) chosen on IS Sharpe alone inside")
    P("each panel x family arm; the pick is read ONCE on OOS.  Both KEEP paths on all books.")
    P("=" * 160)
    P(f"  corpus: {len(G)} books.  4a passes {int(G.p4a.sum())}  4b passes {int(G.p4b.sum())}")
    P(fmt(G.groupby(["panel", "cad"])[["p4a", "p4b"]].sum(), 0))
    P(fmt(G.groupby(["panel", "gross"])[["p4a", "p4b"]].sum(), 0))
    picks = []
    for (pname, family), sub in G.groupby(["panel", "family"]):
        spy_s, live_s = ctxt[pname]
        r = sub.loc[sub.isSharpe.idxmax()]
        picks.append(dict(panel=pname, family=family, n_cand=len(sub), level=r.level, cad=r.cad,
                          gross=r.gross, con=r.con, IS_Sharpe=r.isSharpe,
                          OOS_CAGR=r.oCAGR, OOS_Sharpe=r.oSharpe, OOS_MaxDD=r.oMaxDD,
                          v2_OOS_CAGR=live_s["oCAGR"], v2_OOS_Sharpe=live_s["oSharpe"],
                          v2_OOS_MaxDD=live_s["oMaxDD"], spy_OOS_CAGR=spy_s["oCAGR"],
                          spy_OOS_Sharpe=spy_s["oSharpe"], spy_OOS_MaxDD=spy_s["oMaxDD"],
                          beats_v2=r.oSharpe > live_s["oSharpe"],
                          beats_spy=r.oSharpe > spy_s["oSharpe"], p4a=r.p4a, p4b=r.p4b,
                          f4b=r.f4b))
    W = pd.DataFrame(picks)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(fmt(W))
    P(f"\n  picks {len(W)}: beat RULES v2 OOS Sharpe {int(W.beats_v2.sum())}, "
      f"beat SPY OOS Sharpe {int(W.beats_spy.sum())}, 4a {int(W.p4a.sum())}, "
      f"4b {int(W.p4b.sum())}")
    P("  4b failure legs over the whole corpus:")
    P(G.f4b.value_counts().head(12).to_string())
    flush_log()
    P(f"\nwrote {OUT.name}.*")


if __name__ == "__main__":
    main()

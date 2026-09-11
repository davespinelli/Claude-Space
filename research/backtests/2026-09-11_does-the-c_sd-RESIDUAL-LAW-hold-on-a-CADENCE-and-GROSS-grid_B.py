#!/usr/bin/env python3
"""Idea 539 - "does-the-c_sd-RESIDUAL-LAW-hold-on-a-CADENCE-and-GROSS-grid" (lane B, 2026-09-11).

The question
------------
Idea 535 fitted the de-grossing TIMING RESIDUAL on a continuous predictor

    resid0_pp  ~  1 + c_sd(IS)        ->  const -0.0209 (t -0.87), slope -1.5722 (t -6.32),
                                          IS R2 0.1996, n = 162 IS cells

where, for a (panel, family, strictness, cadence) cell,

    gap0  = 100 * (CAGR(DEGROSS, 0 bps) - CAGR(RESPREAD, 0 bps))     pp/yr
    pred0 = 100 * (CAGR(c_bar * RESPREAD) - CAGR(RESPREAD))          constant-leverage cash drag
    resid0 = gap0 - pred0                                            the TIMING of c_t
    c_t   = (held gross of DEGROSS) / (held gross of RESPREAD),  c_bar/c_sd its mean/sd

Every one of those 162 cells was run at a FIXED gross of 0.75 and at cadences {W, M, Q}.
The queue asks whether -1.5722 is a LAW or a 0.75-specific number, and whether daily
rebalancing changes it.  This run re-cuts the whole decomposition at gross {0.50, 0.75, 1.00}
x cadence {W, M, Q, D}: 3 panels x 2 families x 9 levels x 4 cadences x 3 grosses = 648
cells, 1296 books, every one reported.

The queue's own premise is itself testable (and is pre-registered as G2)
-----------------------------------------------------------------------
The queue says "c_sd is the one input that gross scales directly".  That is not what the
construction does.  At every rebalance DEGROSS holds k_t/n_t of the RESPREAD book's weight
(both are `gross * mask / denominator`, with denominators n_t and k_t), so

    c_t(rebalance) = k_t / n_t     -- the GROSS dial cancels EXACTLY.

It does not cancel between rebalances: the engine renormalises held weights against NAV
including a zero-yielding cash sleeve (`cur = growth / (growth.sum() + 1 - cur.sum())`),
which is not homogeneous of degree 1 in the held gross, so a 0.75 book and a 1.00 book drift
differently.  Whether the leftover gross-dependence of c_sd is material is an empirical
question, pre-registered below, and either answer is a correction to the queue's sentence.

Tuned parameters (PROTOCOL rule 4: at most two).  Reported at EVERY grid point, selected at
none except inside the rule-8 walk-forward.
    1. GROSS, 3 values {0.50, 0.75, 1.00}          (0.75 is idea 535's fixed value)
    2. CADENCE, 4 values {W, M, Q, D}              (D is the queue's addition)
   12 (gross, cadence) grid points.  Everything else -- panels, families, the 9 strictness
   levels, the windows, the cost -- is IMPORTED VERBATIM from ideas 298/301/535 and is the
   population the law is fitted on, not a dial.

Pre-registered bars, written before any number from the new grosses was read
---------------------------------------------------------------------------
G1  REPRODUCTION GATE, asserted first.  The (gross=0.75, cad in {W,M,Q}) subgrid of this run
    IS idea 535's 162 cells.  max |d resid0_pp| < 1e-2 pp and max |d c_sd| < 1e-4 against
    idea 301's committed .decomp.csv, AND the CSD.is fit on that subgrid must reproduce
    slope -1.5722 / const -0.0209 / t -6.32 to < 5e-4 in native units.  (Idea 301 recorded a
    1.287e-02 pp U56 failure of its own gate against idea 298, attributed to the daily drift
    of data/prices.csv; the same allowance is made here and stated.)
G2  THE QUEUE'S PREMISE.  Per cell, r_g = c_sd(gross=g) / c_sd(gross=0.75) for g in
    {0.50, 1.00}.
      G2-SCALES   the queue's reading: median r_g within 0.10 of g/0.75 (0.667 / 1.333).
      G2-INVARIANT the construction's reading: max |r_g - 1| < 0.05 at both off-grosses.
    Exactly one can pass.  Reported either way.
B1  SLOPE INVARIANCE IN GROSS (the headline).  Fit resid0_pp ~ 1 + c_sd on the IS cells of
    each gross, pooling cadences {W,M,Q} so the comparand is idea 535's exact population.
    BAR: beta(0.50) and beta(1.00) both inside beta(0.75) +/- 1.96*se(0.75).  PASS ->
    the law is INVARIANT; FAIL -> -1.5722 is a 0.75-specific number.
B2  IS THE FAILURE PURE SCALE?  Only read if B1 fails.  BAR: |beta(g)/beta(0.75) - g/0.75|
    <= 0.10 at BOTH off-grosses -> the slope is a SCALE fact and beta/gross is the invariant
    the record should publish.  beta/gross is reported at all three grosses regardless.
B3  CADENCE.  Fit the same form within EACH cadence at EACH gross (12 slopes, all reported).
    BAR: the daily slope is inside the same gross's pooled-{W,M,Q} 95% CI.  PASS -> daily
    is on the same law; FAIL -> the published law is a {W,M,Q} law.
B4  DOES THE RETIREMENT SURVIVE?  Idea 535's B1a/B1b re-applied at every (gross, cadence-set):
    OOS MAE of CSD.is (fitted IS-only) vs the FAMILY constant, on ALL cells and on the
    MA-THRESH cells alone.  B1a: MAE_ALL <= 0.95 * MAE(FAMILY).  B1b: MAE_MA <= MAE(FAMILY_MA).

Rule 8 walk-forward (required, PROTOCOL rule 8).  IS <= 2016-12-31, OOS >= 2017-01-01.
  WF-A  THE BOOK.  Inside each (panel, family, construction) arm, (level, cadence, gross) --
        this run's own dials -- is chosen on 2010..2016 IS Sharpe alone; 2017..end read ONCE.
        OOS CAGR / Sharpe / MaxDD against RULES v2 (live), SPY, and the cadence-matched
        no-filter EWall control at the same gross.  12 arms.
  WF-B  THE DELIVERABLE.  Every estimator in B4 is fitted on IS cells only and scored once
        on the OOS cells; every slope in B1/B3 is an IS fit.
  WF-C  IS THE LAW ACTIONABLE?  Use the IS-fitted CSD.is prediction of the gap (pred0 at the
        cell's IS c_bar plus the predicted residual) to CHOOSE the construction per cell --
        DEGROSS if the predicted gap is positive, else RESPREAD -- and read OOS Sharpe ONCE
        against always-RESPREAD, always-DEGROSS and the OOS oracle, at every gross.  A law
        that changes no decision is a reporting rule, not a book, and this says which.

Verdicts (both KEEP paths, on every one of the 1296 books)
    4a  Sharpe > RULES v2 (live) in BOTH halves AND MaxDD no worse than RULES v2.
    4b  Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

SURVIVORSHIP: prices_small.csv.gz, universe.json and universe_broad.json are all CURRENT
constituents -- no delistings -- so every CAGR LEVEL here is inflated and the 4a/4b columns
inherit that whole.  The headline object is an arm-minus-arm contrast on the SAME names and
days at the SAME gross (DEGROSS and RESPREAD share one gate mask), so the bias very largely
cancels out of gap0 / pred0 / resid0; it does NOT cancel out of the KEEP columns.  SMALL439
additionally drops every ticker with max_1d_move >= 1.0 in data/small_meta.csv before use.

Costs 10 bps, next-day execution, no shorting, no leverage (gross <= 1.00).  The 0-bps rung
is DERIVED exactly (r0 = r10 + turnover*bps/1e4), never re-run, so it is the same book.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing outside its outputs.
Outputs: .grid.csv .decomp.csv .slope.csv .estimator.csv .walkforward.csv .console.txt .result.md
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, rules_v2_weights
from engine import backtest, metrics

COST_BPS = 10
GROSSES = [0.50, 0.75, 1.00]
REF_GROSS = 0.75
CADENCES = ["W", "M", "Q", "D"]
REF_CADS = ["W", "M", "Q"]
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]
QUANT_X = [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95]
MA_THETA = [0.30, 0.20, 0.12, 0.06, 0.00, -0.06, -0.12, -0.25, -0.40]
FAMILIES = ["QUANTILE", "MA-THRESH"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

# idea 535's committed CSD.is fit on the 162 IS cells at gross 0.75
REF_SLOPE, REF_CONST, REF_T = -1.5722, -0.0209, -6.32
G1_TOL_PP, G1_TOL_CSD, G1_TOL_FIT = 1e-2, 1e-4, 5e-4
G2_SCALE_TOL, G2_INV_TOL = 0.10, 0.05
B2_TOL = 0.10
B1A_RATIO = 0.95
REF301 = REPO / "research" / "backtests" / (
    "2026-09-09_is-the-gate-timing-residual-a-constant-in-pp-per-year_B.decomp.csv")

OUT = Path(__file__).with_suffix("")
LOG = []
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
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
    return dict(b=b, se=se, t=t, R2=(1 - ssr / sst if sst > 0 else np.nan), n=n)


# ---------------------------------------------------------------- idea 298/301 constructions
def panels():
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv = [c for c in pxs.columns if c != "SPY" and c not in bad]
    px56 = load_universe()
    px136 = load_universe(broad=True)
    out = {
        "SMALL439": (pxs[inv], pxs["SPY"]),
        "U56": (px56[[c for c in px56.columns if c != "SPY"]], px56["SPY"]),
        "B136": (px136[[c for c in px136.columns if c != "SPY"]], px136["SPY"]),
    }
    P(f"panels: SMALL439 {out['SMALL439'][0].shape[1]} names ({len(bad)} dropped for "
      f"max_1d_move >= 1.0), U56 {out['U56'][0].shape[1]}, B136 {out['B136'][0].shape[1]}")
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


def unit_book(px, g, construction):
    """idea 301's book() at gross = 1; the GROSS dial multiplies this."""
    if construction == "RESPREAD":
        k = g.sum(axis=1).clip(lower=1)
        return g.astype(float).div(k, axis=0)
    n = live_mask(px).sum(axis=1).clip(lower=1)
    return g.astype(float).div(n, axis=0)


def control_unit(px):
    live = live_mask(px)
    return live.astype(float).div(live.sum(axis=1).clip(lower=1), axis=0)


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


# ---------------------------------------------------------------- estimator ladder (B4)
def fit_csd(df):
    X = np.column_stack([np.ones(len(df)), df.c_sd_is.values])
    return ols(X, df.resid_is.values)


def est_scores(C):
    """Fit ZERO / GLOBAL / FAMILY / CSD.is on the IS cells of C, score once on the OOS cells."""
    g = float(C.resid_is.mean())
    f = fit_csd(C)
    fam = C.groupby("family").resid_is.mean()
    preds = {
        "ZERO": pd.Series(0.0, index=C.index),
        "GLOBAL": pd.Series(g, index=C.index),
        "FAMILY": pd.Series(fam.reindex(pd.Index(C.family)).values, index=C.index),
        "CSD.is": pd.Series(f["b"][0] + f["b"][1] * C.c_sd_is.values, index=C.index),
    }
    rows = []
    for name, p in preds.items():
        for sub in ("ALL", "MA-THRESH", "QUANTILE"):
            m = slice(None) if sub == "ALL" else (C.family == sub).values
            e = np.abs(p.values[m] - C.resid_oos.values[m])
            rows.append(dict(form=name, subset=sub, n=int(e.size), MAE=float(e.mean()),
                             RMSE=float(np.sqrt((e ** 2).mean()))))
    return pd.DataFrame(rows), f, preds


# ---------------------------------------------------------------- main
def main():
    PN = panels()
    P("=" * 185)
    P("Idea 539 does-the-c_sd-RESIDUAL-LAW-hold-on-a-CADENCE-and-GROSS-grid (lane B) | "
      + Path(__file__).name)
    P("=" * 185)
    P(f"costs {COST_BPS} bps (0-bps rung DERIVED as r0 = r10 + turnover*bps/1e4), next-day "
      f"execution, IS <= {IS_END}, OOS >= {OOS_START} (PROTOCOL rule 8).")
    P(f"tuned dials: GROSS {GROSSES} x CADENCE {CADENCES} = {len(GROSSES)*len(CADENCES)} grid "
      f"points, ALL reported.  3 panels x 2 families x 9 levels x 12 = 648 cells, 1296 books.")
    P("pre-registered bars:")
    P(f"  G1 REPRODUCTION  the (gross={REF_GROSS}, cad in {REF_CADS}) subgrid vs idea 301's "
      f"committed .decomp.csv: max|d resid0_pp| < {G1_TOL_PP} pp, max|d c_sd| < {G1_TOL_CSD}; "
      f"and the CSD.is fit == ({REF_CONST}, {REF_SLOPE}, t {REF_T}) to < {G1_TOL_FIT}")
    P(f"  G2 QUEUE PREMISE  r_g = c_sd(g)/c_sd({REF_GROSS}).  SCALES: |median r_g - g/{REF_GROSS}| "
      f"<= {G2_SCALE_TOL}.  INVARIANT: max|r_g - 1| < {G2_INV_TOL}.  Exactly one can pass.")
    P(f"  B1 SLOPE INVARIANCE  beta(0.50), beta(1.00) inside beta({REF_GROSS}) +/- 1.96*se, "
      f"cadences {REF_CADS} pooled (idea 535's exact population)")
    P(f"  B2 PURE SCALE (only if B1 fails)  |beta(g)/beta({REF_GROSS}) - g/{REF_GROSS}| <= {B2_TOL} at both")
    P(f"  B3 CADENCE  the daily slope inside the same gross's pooled-{REF_CADS} 95% CI")
    P(f"  B4 RETIREMENT  CSD.is OOS MAE <= {B1A_RATIO} * FAMILY on ALL cells and <= FAMILY on "
      f"the MA-THRESH cells, at every (gross, cadence-set)")
    flush_log()

    px_u = load_universe()
    live_full = backtest(px_u, rules_v2_weights(px_u), cost_bps=COST_BPS, freq="W")["returns"]

    rows, decomp, panel_spy, panel_live = [], [], {}, {}
    for pname, (px, spy_px) in PN.items():
        start = px.index[260]
        years = len(px.loc[start:]) / 252
        spy_r = spy_px.pct_change().fillna(0.0).loc[start:]
        spy_s = stat(spy_r)
        live_s = stat(live_full.reindex(px.index).fillna(0.0).loc[start:])
        panel_spy[pname], panel_live[pname] = spy_s, live_s
        cu = control_unit(px)
        ctrl = {}
        for cad in CADENCES:
            for gr in GROSSES:
                rc = backtest(px, cu * gr, cost_bps=COST_BPS, freq=cad)
                ctrl[(cad, gr)] = stat(rc["returns"].loc[start:])
        P("\n" + "-" * 185)
        P(f"PANEL {pname}: evaluation from {start.date()} ({years:.2f} yrs)")
        P(f"  SPY CAGR {spy_s['CAGR']:.4f} Sharpe {spy_s['Sharpe']:.4f} MaxDD {spy_s['MaxDD']:.4f} "
          f"halves {spy_s['H1']:.4f}/{spy_s['H2']:.4f} OOS Sharpe {spy_s['oSharpe']:.4f} "
          f"OOS CAGR {spy_s['oCAGR']:.4f} OOS MaxDD {spy_s['oMaxDD']:.4f}")
        P(f"  RULES v2 (live, 4a comparand): CAGR {live_s['CAGR']:.4f} Sharpe {live_s['Sharpe']:.4f} "
          f"MaxDD {live_s['MaxDD']:.4f} halves {live_s['H1']:.4f}/{live_s['H2']:.4f} "
          f"OOS Sharpe {live_s['oSharpe']:.4f} OOS CAGR {live_s['oCAGR']:.4f}")
        P(f"  4b bars from SPY: H1>{spy_s['H1']:.3f} H2>{spy_s['H2']:.3f} "
          f"OOS>{spy_s['oSharpe']:.3f} MaxDD>=-{0.60*abs(spy_s['MaxDD']):.1%} "
          f"CAGR>={0.70*spy_s['CAGR']:.2%}")
        P("  EWall control (no gate), OOS Sharpe by (cadence, gross): "
          + " ".join(f"{c}/{g:.2f}={ctrl[(c,g)]['oSharpe']:.3f}" for c in CADENCES for g in GROSSES))
        flush_log()

        for family in FAMILIES:
            levels = QUANT_X if family == "QUANTILE" else MA_THETA
            for level in levels:
                gm = gate_mask(px, family, level)
                ub = {con: unit_book(px, gm, con) for con in CONSTRUCTIONS}
                for cad in CADENCES:
                    for gr in GROSSES:
                        got = {}
                        for con in CONSTRUCTIONS:
                            res = backtest(px, ub[con] * gr, cost_bps=COST_BPS, freq=cad)
                            r10 = res["returns"].loc[start:]
                            turn = res["turnover"].loc[start:]
                            r0 = r10 + turn * COST_BPS / 1e4
                            grs = res["weights"].loc[start:].sum(axis=1)
                            s = stat(r10)
                            got[con] = dict(r0=r0, gross=grs, s=s)
                            rows.append(dict(panel=pname, family=family, level=level, cad=cad,
                                             gross=gr, con=con, **s, CAGR0=cagr(r0),
                                             gross_mean=grs.mean(), turn_yr=turn.sum() / years,
                                             dSharpe_ctrl=s["Sharpe"] - ctrl[(cad, gr)]["Sharpe"],
                                             ctrl_oSharpe=ctrl[(cad, gr)]["oSharpe"],
                                             p4a=verdict_4a(s, live_s), f4b=fail_4b(s, spy_s),
                                             spy_Sharpe=spy_s["Sharpe"],
                                             spy_oSharpe=spy_s["oSharpe"]))
                        dg, rs = got["DEGROSS"], got["RESPREAD"]
                        c_t = (dg["gross"] / rs["gross"].replace(0, np.nan)).fillna(0.0)

                        def dec_window(lo, hi, tag):
                            sl = slice(lo, hi)
                            rr, rd = rs["r0"].loc[sl], dg["r0"].loc[sl]
                            cb = float(c_t.loc[sl].mean())
                            g0 = 100 * (cagr(rd) - cagr(rr))
                            p0 = 100 * (cagr(cb * rr) - cagr(rr))
                            return dict(window=tag, c_bar=cb, c_sd=float(c_t.loc[sl].std()),
                                        gap0_pp=g0, pred0_pp=p0, resid0_pp=g0 - p0,
                                        share=(p0 / g0 if abs(g0) > 1e-9 else np.nan),
                                        CAGR_rs0=cagr(rr), CAGR_dg0=cagr(rd),
                                        oSharpe_rs=rs["s"]["oSharpe"], oSharpe_dg=dg["s"]["oSharpe"],
                                        isSharpe_rs=rs["s"]["isSharpe"],
                                        isSharpe_dg=dg["s"]["isSharpe"])
                        base = dict(panel=pname, family=family, level=level, cad=cad, gross=gr)
                        for tag, lo, hi in (("FULL", None, None), ("IS", None, IS_END),
                                            ("OOS", OOS_START, None)):
                            decomp.append({**base, **dec_window(lo, hi, tag)})
            P(f"  ... {pname} / {family} done ({len(levels)*len(CADENCES)*len(GROSSES)*2} books)")
            flush_log()

    G = pd.DataFrame(rows)
    D = pd.DataFrame(decomp)
    G["p4b"] = G.f4b == "-"
    G.to_csv(f"{OUT}.grid.csv", index=False)
    D.to_csv(f"{OUT}.decomp.csv", index=False)

    # ---------------- cell table
    key = ["panel", "family", "level", "cad", "gross"]
    W = {t: D[D.window == t].sort_values(key).reset_index(drop=True) for t in ("IS", "OOS")}
    IS, OOS = W["IS"], W["OOS"]
    assert (IS[key].values == OOS[key].values).all(), "IS/OOS cell alignment"
    C = IS[key].copy()
    C["c_sd_is"], C["c_bar_is"] = IS.c_sd.values, IS.c_bar.values
    C["c_sd_oos"] = OOS.c_sd.values
    C["resid_is"], C["resid_oos"] = IS.resid0_pp.values, OOS.resid0_pp.values
    C["gap_is"], C["gap_oos"] = IS.gap0_pp.values, OOS.gap0_pp.values
    C["pred_is"] = IS.pred0_pp.values
    C["oSharpe_rs"], C["oSharpe_dg"] = OOS.oSharpe_rs.values, OOS.oSharpe_dg.values

    # ---------------- G1 reproduction gate, first
    P("\n" + "=" * 185)
    P("G1 REPRODUCTION GATE vs idea 301's committed .decomp.csv (asserted before any new number)")
    P("=" * 185)
    rk = ["panel", "family", "level", "cad", "window"]
    ref = pd.read_csv(REF301)
    sub = D[(D.gross == REF_GROSS) & (D.cad.isin(REF_CADS))]
    m = sub.merge(ref[rk + ["resid0_pp", "gap0_pp", "pred0_pp", "c_bar", "c_sd"]], on=rk,
                  suffixes=("", "_ref"))
    P(f"  matched rows: {len(m)} of {len(sub)} recomputed (gross {REF_GROSS}, cad {REF_CADS}) "
      f"and {len(ref)} committed")
    for c in ["resid0_pp", "gap0_pp", "pred0_pp", "c_bar", "c_sd"]:
        m[f"d_{c}"] = (m[c] - m[f"{c}_ref"]).abs()
    dcols = ["d_resid0_pp", "d_gap0_pp", "d_pred0_pp", "d_c_bar", "d_c_sd"]
    P(fmt(m.groupby("panel")[dcols].max(), 8))
    g1r, g1c = float(m.d_resid0_pp.max()), float(m.d_c_sd.max())
    g1a = (g1r < G1_TOL_PP) and (g1c < G1_TOL_CSD)
    P(f"  max |d resid0_pp| = {g1r:.3e} pp (bar {G1_TOL_PP}), max |d c_sd| = {g1c:.3e} "
      f"(bar {G1_TOL_CSD})  ->  G1-decomp {'PASS' if g1a else 'FAIL'}")
    ref_cells = C[(C.gross == REF_GROSS) & (C.cad.isin(REF_CADS))]
    f75 = fit_csd(ref_cells)
    P(f"  CSD.is refit on those {f75['n']} IS cells: const {f75['b'][0]:.4f} (t {f75['t'][0]:.2f}), "
      f"slope {f75['b'][1]:.4f} (t {f75['t'][1]:.2f}), se {f75['se'][1]:.4f}, R2 {f75['R2']:.4f}")
    dfit = max(abs(f75["b"][1] - REF_SLOPE), abs(f75["b"][0] - REF_CONST))
    dt_ = abs(f75["t"][1] - REF_T)
    g1b = (dfit < G1_TOL_FIT) and (dt_ < 0.01) and (f75["n"] == 162)
    P(f"  vs idea 535 committed (const {REF_CONST}, slope {REF_SLOPE}, t {REF_T}): "
      f"max |d coef| {dfit:.3e} (bar {G1_TOL_FIT}), |d t| {dt_:.3e}, n {f75['n']}  ->  "
      f"G1-fit {'PASS' if g1b else 'FAIL'}")
    P(f"  G1 OVERALL: {'PASS' if (g1a and g1b) else 'FAIL'}")
    if not (g1a and g1b):
        P("  G1 FAILED -- everything below is reported but must not be read as a restatement "
          "of idea 535 on the rows that differ.")
    flush_log()

    # ---------------- G2 the queue's premise
    P("\n" + "=" * 185)
    P("G2 THE QUEUE'S PREMISE: 'c_sd is the one input that gross scales directly'")
    P("=" * 185)
    base = C[C.gross == REF_GROSS].set_index(["panel", "family", "level", "cad"])
    g2rows, g2pass = [], {}
    for gr in GROSSES:
        cur = C[C.gross == gr].set_index(["panel", "family", "level", "cad"])
        r_is = (cur.c_sd_is / base.c_sd_is).dropna()
        r_oos = (cur.c_sd_oos / base.c_sd_oos).dropna()
        g2rows.append(dict(gross=gr, expected_if_SCALES=gr / REF_GROSS, n=len(r_is),
                           med_ratio_IS=float(r_is.median()), min_IS=float(r_is.min()),
                           max_IS=float(r_is.max()), med_ratio_OOS=float(r_oos.median()),
                           max_abs_dev_from_1=float((r_is - 1).abs().max())))
        g2pass[gr] = (float(r_is.median()), float((r_is - 1).abs().max()))
    G2 = pd.DataFrame(g2rows).set_index("gross")
    P(fmt(G2, 6))
    sc = all(abs(g2pass[g][0] - g / REF_GROSS) <= G2_SCALE_TOL for g in GROSSES if g != REF_GROSS)
    iv = all(g2pass[g][1] < G2_INV_TOL for g in GROSSES if g != REF_GROSS)
    P(f"  G2-SCALES (queue's reading)      : {'PASS' if sc else 'FAIL'}")
    P(f"  G2-INVARIANT (construction's)    : {'PASS' if iv else 'FAIL'}")
    G2.to_csv(f"{OUT}.premise.csv")
    flush_log()

    # ---------------- B1 / B2 / B3 slopes
    P("\n" + "=" * 185)
    P("B1/B2/B3 THE c_sd SLOPE: resid0_pp ~ 1 + c_sd(IS), fitted on IS cells only")
    P("=" * 185)
    srows = []
    for gr in GROSSES:
        for cadset, tag in [(REF_CADS, "WMQ(535 population)"), (CADENCES, "WMQD(all)")] + \
                           [([c], c) for c in CADENCES]:
            d = C[(C.gross == gr) & (C.cad.isin(cadset))]
            f = fit_csd(d)
            srows.append(dict(gross=gr, cadset=tag, n=f["n"], const=f["b"][0],
                              slope=f["b"][1], se=f["se"][1], t=f["t"][1], R2=f["R2"],
                              slope_over_gross=f["b"][1] / gr,
                              lo95=f["b"][1] - 1.96 * f["se"][1],
                              hi95=f["b"][1] + 1.96 * f["se"][1]))
    S = pd.DataFrame(srows)
    S.to_csv(f"{OUT}.slope.csv", index=False)
    P(fmt(S.set_index(["gross", "cadset"]), 4))

    ref_row = S[(S.gross == REF_GROSS) & (S.cadset == "WMQ(535 population)")].iloc[0]
    lo, hi = ref_row.lo95, ref_row.hi95
    P(f"\n  beta({REF_GROSS}) = {ref_row.slope:.4f}, se {ref_row.se:.4f}, 95% CI [{lo:.4f}, {hi:.4f}]")
    b1 = {}
    for gr in GROSSES:
        if gr == REF_GROSS:
            continue
        b = float(S[(S.gross == gr) & (S.cadset == "WMQ(535 population)")].slope.iloc[0])
        inside = bool(lo <= b <= hi)
        b1[gr] = (b, inside)
        P(f"    beta({gr:.2f}) = {b:.4f}  -> {'INSIDE' if inside else 'OUTSIDE'} the CI")
    B1 = all(v[1] for v in b1.values())
    P(f"  B1 SLOPE INVARIANCE IN GROSS: {'PASS -- the law is invariant' if B1 else 'FAIL -- -1.5722 is gross-specific'}")

    P("\n  B2 IS THE FAILURE PURE SCALE?  beta(g)/beta(0.75) vs g/0.75")
    b2ok = []
    for gr in GROSSES:
        if gr == REF_GROSS:
            continue
        ratio = b1[gr][0] / ref_row.slope
        exp = gr / REF_GROSS
        ok = abs(ratio - exp) <= B2_TOL
        b2ok.append(ok)
        P(f"    gross {gr:.2f}: ratio {ratio:.4f} vs expected {exp:.4f}  d {ratio-exp:+.4f}  "
          f"{'within' if ok else 'OUTSIDE'} {B2_TOL}")
    B2 = all(b2ok)
    P(f"  B2 PURE SCALE: {'PASS -- beta/gross is the invariant' if B2 else 'FAIL'}")
    P("  gross-normalised slope beta/gross (WMQ population): "
      + " ".join(f"{g:.2f}->{float(S[(S.gross==g)&(S.cadset=='WMQ(535 population)')].slope_over_gross.iloc[0]):.4f}"
                 for g in GROSSES))

    P("\n  B3 CADENCE: the daily slope against the same gross's pooled-WMQ 95% CI")
    b3ok = []
    for gr in GROSSES:
        rr = S[(S.gross == gr) & (S.cadset == "WMQ(535 population)")].iloc[0]
        dd = S[(S.gross == gr) & (S.cadset == "D")].iloc[0]
        ok = bool(rr.lo95 <= dd.slope <= rr.hi95)
        b3ok.append(ok)
        P(f"    gross {gr:.2f}: beta(D) {dd.slope:.4f} vs WMQ CI [{rr.lo95:.4f}, {rr.hi95:.4f}] "
          f"-> {'INSIDE' if ok else 'OUTSIDE'}")
    B3 = all(b3ok)
    P(f"  B3 CADENCE: {'PASS -- daily is on the same law' if B3 else 'FAIL -- the published law is a WMQ law'}")
    flush_log()

    # ---------------- B4 the retirement bar, re-applied
    P("\n" + "=" * 185)
    P("B4 DOES IDEA 535's RETIREMENT SURVIVE?  estimators fitted on IS cells, scored ONCE on "
      "OOS cells, at every (gross, cadence-set).  MAE in pp/yr")
    P("=" * 185)
    erows = []
    for gr in GROSSES:
        for cadset, tag in [(REF_CADS, "WMQ"), (CADENCES, "WMQD"), (["D"], "D")]:
            d = C[(C.gross == gr) & (C.cad.isin(cadset))].reset_index(drop=True)
            E, f, _ = est_scores(d)
            E["gross"], E["cadset"] = gr, tag
            erows.append(E)
    E = pd.concat(erows, ignore_index=True)
    E.to_csv(f"{OUT}.estimator.csv", index=False)
    piv = E.pivot_table(index=["gross", "cadset"], columns=["subset", "form"], values="MAE")
    P(fmt(piv, 4))
    b4rows = []
    for (gr, tag), d in E.groupby(["gross", "cadset"]):
        def mae(f, s):
            return float(d[(d.form == f) & (d.subset == s)].MAE.iloc[0])
        a = mae("CSD.is", "ALL") <= B1A_RATIO * mae("FAMILY", "ALL")
        b = mae("CSD.is", "MA-THRESH") <= mae("FAMILY", "MA-THRESH")
        b4rows.append(dict(gross=gr, cadset=tag, MAE_CSD_ALL=mae("CSD.is", "ALL"),
                           MAE_FAM_ALL=mae("FAMILY", "ALL"),
                           ratio=mae("CSD.is", "ALL") / mae("FAMILY", "ALL"),
                           MAE_CSD_MA=mae("CSD.is", "MA-THRESH"),
                           MAE_FAM_MA=mae("FAMILY", "MA-THRESH"), B1a=a, B1b=b,
                           RETIRES=bool(a and b)))
    B4T = pd.DataFrame(b4rows).set_index(["gross", "cadset"])
    P("\n  " + "-" * 100)
    P(fmt(B4T, 4))
    B4 = bool(B4T.RETIRES.all())
    P(f"  B4 RETIREMENT holds at {int(B4T.RETIRES.sum())} of {len(B4T)} (gross, cadence-set) "
      f"points -> {'PASS' if B4 else 'FAIL'}")
    flush_log()

    # ---------------- WF-A the book (rule 8)
    P("\n" + "=" * 185)
    P("WF-A RULE 8: (level, cadence, gross) chosen on IS Sharpe alone inside each "
      "(panel, family, construction) arm; OOS read ONCE")
    P("=" * 185)
    wf = []
    for (pn, fam, con), d in G.groupby(["panel", "family", "con"]):
        pick = d.loc[d.isSharpe.idxmax()]
        spy_s, live_s = panel_spy[pn], panel_live[pn]
        wf.append(dict(panel=pn, family=fam, con=con, pick_level=pick.level,
                       pick_cad=pick.cad, pick_gross=pick.gross, is_Sharpe=pick.isSharpe,
                       oCAGR=pick.oCAGR, oSharpe=pick.oSharpe, oMaxDD=pick.oMaxDD,
                       spy_oCAGR=spy_s["oCAGR"], spy_oSharpe=spy_s["oSharpe"],
                       spy_oMaxDD=spy_s["oMaxDD"], live_oSharpe=live_s["oSharpe"],
                       live_oCAGR=live_s["oCAGR"],
                       beats_SPY_oos=bool(pick.oSharpe > spy_s["oSharpe"]),
                       beats_LIVE_oos=bool(pick.oSharpe > live_s["oSharpe"]),
                       p4a=bool(pick.p4a), p4b=bool(pick.p4b), f4b=pick.f4b))
    WF = pd.DataFrame(wf).set_index(["panel", "family", "con"]).sort_index()
    WF.to_csv(f"{OUT}.walkforward.csv")
    P(fmt(WF, 4))
    P(f"\n  WF-A picks: beat SPY OOS {int(WF.beats_SPY_oos.sum())}/{len(WF)}, beat RULES v2 OOS "
      f"{int(WF.beats_LIVE_oos.sum())}/{len(WF)}, 4a {int(WF.p4a.sum())}/{len(WF)}, "
      f"4b {int(WF.p4b.sum())}/{len(WF)}")
    P(f"  ALL {len(G)} books: 4a {int(G.p4a.sum())}/{len(G)}, 4b {int(G.p4b.sum())}/{len(G)}")
    P("  4b first-fail tally over all books: "
      + str(G.f4b.value_counts().head(10).to_dict()))
    P("  4a / 4b by gross:")
    P(fmt(G.groupby("gross")[["p4a", "p4b"]].sum().join(G.groupby("gross").size().rename("n")), 0))
    P("  4a / 4b by cadence:")
    P(fmt(G.groupby("cad")[["p4a", "p4b"]].sum().join(G.groupby("cad").size().rename("n")), 0))
    flush_log()

    # ---------------- WF-C is the law actionable
    P("\n" + "=" * 185)
    P("WF-C IS THE LAW ACTIONABLE?  IS-fitted CSD.is predicts the gap; the sign picks the "
      "construction; OOS Sharpe read ONCE")
    P("=" * 185)
    arows = []
    for gr in GROSSES:
        for cadset, tag in [(REF_CADS, "WMQ"), (CADENCES, "WMQD")]:
            d = C[(C.gross == gr) & (C.cad.isin(cadset))].reset_index(drop=True)
            f = fit_csd(d)
            pred_resid = f["b"][0] + f["b"][1] * d.c_sd_is.values
            pred_gap = d.pred_is.values + pred_resid
            choose_dg = pred_gap > 0
            picked = np.where(choose_dg, d.oSharpe_dg.values, d.oSharpe_rs.values)
            oracle = np.maximum(d.oSharpe_dg.values, d.oSharpe_rs.values)
            true_dg = d.gap_oos.values > 0
            arows.append(dict(gross=gr, cadset=tag, n=len(d),
                              share_DEGROSS=float(choose_dg.mean()),
                              hit_rate=float((choose_dg == true_dg).mean()),
                              PICK=float(picked.mean()),
                              ALWAYS_RS=float(d.oSharpe_rs.mean()),
                              ALWAYS_DG=float(d.oSharpe_dg.mean()),
                              ORACLE=float(oracle.mean()),
                              PICK_minus_best_fixed=float(
                                  picked.mean() - max(d.oSharpe_rs.mean(), d.oSharpe_dg.mean())),
                              share_of_oracle_gap=float(
                                  (picked.mean() - max(d.oSharpe_rs.mean(), d.oSharpe_dg.mean()))
                                  / (oracle.mean() - max(d.oSharpe_rs.mean(), d.oSharpe_dg.mean()))
                                  if oracle.mean() > max(d.oSharpe_rs.mean(), d.oSharpe_dg.mean())
                                  else np.nan)))
    A = pd.DataFrame(arows).set_index(["gross", "cadset"])
    A.to_csv(f"{OUT}.actionable.csv")
    P(fmt(A, 4))
    flush_log()

    # ---------------- verdict
    P("\n" + "=" * 185)
    P("VERDICT")
    P("=" * 185)
    P(f"  G1 reproduction      {'PASS' if (g1a and g1b) else 'FAIL'}")
    P(f"  G2-SCALES (queue)    {'PASS' if sc else 'FAIL'}   G2-INVARIANT {'PASS' if iv else 'FAIL'}")
    P(f"  B1 slope invariance  {'PASS' if B1 else 'FAIL'}")
    P(f"  B2 pure scale        {'PASS' if B2 else 'FAIL'}")
    P(f"  B3 cadence (daily)   {'PASS' if B3 else 'FAIL'}")
    P(f"  B4 retirement holds  {'PASS' if B4 else 'FAIL'}")
    keep = int(G.p4a.sum()) > 0 or int(G.p4b.sum()) > 0
    P(f"  KEEP paths over {len(G)} books: 4a {int(G.p4a.sum())}, 4b {int(G.p4b.sum())}")
    P(f"  WF-A picks: 4a {int(WF.p4a.sum())}/{len(WF)}, 4b {int(WF.p4b.sum())}/{len(WF)}, "
      f"beat RULES v2 OOS {int(WF.beats_LIVE_oos.sum())}/{len(WF)}, "
      f"beat SPY OOS {int(WF.beats_SPY_oos.sum())}/{len(WF)}")
    P("  This is a DIAGNOSTIC idea: its deliverable is the law's domain, not a book.  "
      "No KEEP is claimed from the 4a/4b columns unless a WF-A pick carries one.")
    flush_log()

    res = dict(g1=(g1a and g1b), g2_scales=sc, g2_inv=iv, B1=B1, B2=B2, B3=B3, B4=B4,
               S=S, G2=G2, B4T=B4T, WF=WF, A=A, G=G, f75=f75, b1=b1, ref_row=ref_row)
    write_result(res)
    flush_log()
    return res


def write_result(r):
    S, WF, G = r["S"], r["WF"], r["G"]
    ref = r["ref_row"]
    wmq = S[S.cadset == "WMQ(535 population)"].set_index("gross")
    lines = [
        "# Idea 539 — does-the-c_sd-RESIDUAL-LAW-hold-on-a-CADENCE-and-GROSS-grid (lane B, 2026-09-11)",
        "",
        f"**G1 reproduction {'PASS' if r['g1'] else 'FAIL'}** — the (gross 0.75, cad W/M/Q) subgrid "
        f"reproduces idea 301's committed decomposition and idea 535's CSD.is fit "
        f"(const {r['f75']['b'][0]:.4f}, slope {r['f75']['b'][1]:.4f}, t {r['f75']['t'][1]:.2f}, "
        f"n {r['f75']['n']}).",
        "",
        "## The headline: the slope at every gross (cadences W/M/Q, idea 535's exact population)",
        "",
        "```",
        fmt(wmq[["n", "const", "slope", "se", "t", "R2", "slope_over_gross", "lo95", "hi95"]], 4),
        "```",
        "",
        f"- **B1 SLOPE INVARIANCE IN GROSS: {'PASS' if r['B1'] else 'FAIL'}** — "
        f"beta(0.75) = {ref.slope:.4f} [{ref.lo95:.4f}, {ref.hi95:.4f}]; "
        + "; ".join(f"beta({g:.2f}) = {v[0]:.4f} {'INSIDE' if v[1] else 'OUTSIDE'}"
                    for g, v in r["b1"].items()) + ".",
        f"- **B2 PURE SCALE: {'PASS' if r['B2'] else 'FAIL'}** — "
        + "; ".join(f"beta({g:.2f})/beta(0.75) = {v[0]/ref.slope:.4f} vs g/0.75 = {g/REF_GROSS:.4f}"
                    for g, v in r["b1"].items()) + ".",
        f"- **B3 CADENCE (daily): {'PASS' if r['B3'] else 'FAIL'}**.",
        f"- **B4 idea 535's RETIREMENT: {'PASS' if r['B4'] else 'FAIL'}** at "
        f"{int(r['B4T'].RETIRES.sum())} of {len(r['B4T'])} (gross, cadence-set) points.",
        "",
        "## G2 — the queue's premise ('c_sd is the one input that gross scales directly')",
        "",
        "```", fmt(r["G2"], 6), "```",
        "",
        f"G2-SCALES {'PASS' if r['g2_scales'] else 'FAIL'} / "
        f"G2-INVARIANT {'PASS' if r['g2_inv'] else 'FAIL'}.",
        "",
        "## All 12 (gross, cadence) slopes",
        "", "```", fmt(S.set_index(["gross", "cadset"]), 4), "```",
        "",
        "## B4 — estimator ladder (fitted IS, scored once OOS)",
        "", "```", fmt(r["B4T"], 4), "```",
        "",
        "## WF-A (rule 8): (level, cadence, gross) chosen on IS Sharpe, OOS read once",
        "", "```", fmt(WF, 4), "```",
        "",
        f"WF-A picks beat SPY OOS {int(WF.beats_SPY_oos.sum())}/{len(WF)}, RULES v2 "
        f"{int(WF.beats_LIVE_oos.sum())}/{len(WF)}.  4a {int(G.p4a.sum())}/{len(G)} books, "
        f"4b {int(G.p4b.sum())}/{len(G)} books.",
        "",
        "## WF-C — is the law actionable?",
        "", "```", fmt(r["A"], 4), "```",
        "",
        "SURVIVORSHIP: SMALL439/U56/B136 are current constituents only (no delistings); CAGR "
        "levels and the 4a/4b columns are inflated.  The residual is an arm-minus-arm contrast "
        "on the same names, days and gross, so the bias very largely cancels out of it.",
    ]
    Path(f"{OUT}.result.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()

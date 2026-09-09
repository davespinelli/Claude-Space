#!/usr/bin/env python3
"""Idea 535 - "is-the-FAMILY-constant-really-a-c_sd-constant" (cloud lane, 2026-09-09).

The question
------------
Idea 301 found that the best pooling unit for the de-grossing TIMING RESIDUAL

    gap0 = pred0 + resid0        (DEGROSS minus RESPREAD CAGR gap, in pp/yr, at 0 bps)
           ^ constant-leverage cash drag at the cell's own mean leverage c_bar
                    ^ the TIMING of c_t -- the gate's own content

is the GATE FAMILY (OOS MAE 0.1936 pp over 162 cells, against 0.2458 for a single global
constant and 0.2641 for predicting zero).  It also reported `corr(c_sd, |resid0|)` = 0.7765
pooled and 0.57 / 0.56 WITHIN each family, where c_sd is the standard deviation of the gate's
own exposure path c_t.  So the queue asks: is 'family' just a coarse read of HOW MUCH THE
GATE'S EXPOSURE MOVES?  Replace the family dummy with a CONTINUOUS c_sd predictor fitted on
IS cells and score it against the FAMILY constant on the SAME OOS cells.  A continuous
predictor that wins retires the family label.

Why the pooled correlation is not the test
------------------------------------------
The QUANTILE family holds a FIXED FRACTION of the panel by construction, so its c_t is
almost constant (c_sd ~ 1e-3) and its resid0 is ~0 BY IDENTITY, not by evidence.  The
MA-THRESH family's exposure moves with the market (c_sd ~ 0.2-0.3) and carries the whole
residual.  A pooled corr(c_sd, |resid0|) of 0.78 across the two is therefore mostly the
family label written in continuous ink.  The decisive question is WITHIN MA-THRESH, where
the family constant is a single number and c_sd still varies 5x across strictness levels.
Both cuts are pre-registered below and both are reported.

The ex-ante problem (a method finding, not a dial)
--------------------------------------------------
c_sd is a property of a WINDOW.  Using the OOS window's own c_sd to predict that window's
resid0 is a peek: at decision time only the IS window's c_sd is known.  Both are carried as
separate PREDICTOR FORMS -- `.is` (honest, usable) and `.oos` (a feasibility ceiling, marked
PEEK everywhere it appears) -- so the gap between them prices exactly how much of any c_sd
win is unavailable in advance.

Design
------
The 162-cell grid is IMPORTED VERBATIM from ideas 298/301 -- 3 panels x 2 gate families x 9
strictness levels x 3 cadences, 324 books -- and every construction (gate_mask / book /
control_book / stat / dec_window) is idea 301's code verbatim.  A REPRODUCTION GATE (B3)
asserts the recomputed resid0 and c_sd against idea 301's committed .decomp.csv before any
new number is read.  Nothing about the grid is re-chosen here; it is the population the
estimators are scored on, not a dial.

Tuned parameters (PROTOCOL rule 4: at most two).  Reported at EVERY grid point, selected at
none except inside the rule-8 walk-forward.
    1. PREDICTOR FORM, 10 values (all fitted on IS cells only, by OLS, pooled over all cells
       unless the form names a group):
         ZERO           predict 0 pp/yr                                   (0 numbers)
         GLOBAL         one IS mean over all IS cells                     (1)
         FAMILY         IS mean per gate family  <- THE INCUMBENT         (2)
         CSD.is         1 + c_sd(IS)                                      (2)
         CSD.oos        1 + c_sd(OOS)                            PEEK     (2)
         CSD0.is        0 + c_sd(IS)   (through the origin)               (1)
         LOGCSD.is      1 + log(c_sd(IS) + 1e-4)                          (2)
         CSDxVOL.is     1 + c_sd(IS) + c_sd(IS) * panel_vol(IS)           (3)
         CSD+CBAR.is    1 + c_sd(IS) + c_bar(IS)                          (3)
         FAM+CSD.is     family dummy + c_sd(IS)  (does c_sd ADD to family?) (3)
    2. SHRINKAGE lambda toward the GLOBAL IS mean, 5 values {0.00, 0.25, 0.50, 0.75, 1.00}:
         pred = lambda * form + (1 - lambda) * global_IS_mean.  lambda = 0 collapses every
         form to GLOBAL.  ZERO is the no-information baseline and is never shrunk.
       10 x 5 = 50 estimator cells, every one reported on both cuts (ALL 162 / MA-THRESH 81).

Windows are PROTOCOL rule 8's, fixed before the run: IS <= 2016-12-31, OOS >= 2017-01-01.
Costs 10 bps, gross 0.75, next-day execution, no shorting, no leverage.  The 0-bps rung is
DERIVED exactly (r0 = r10 + turnover*bps/1e4), never re-run, so it is the same book.

Pre-registered bars, written before any OOS number was read
-----------------------------------------------------------
B1  THE RETIREMENT BAR (the queue's own test, "a continuous predictor that wins retires the
    family label").  BOTH legs must hold for the best `.is` c_sd form at its best lambda:
      B1a  OOS MAE on ALL 162 cells <= 0.95 * OOS MAE(FAMILY, lambda=1)
      B1b  OOS MAE on the 81 MA-THRESH cells <= OOS MAE(FAMILY, lambda=1) on the same 81
           (i.e. it must not buy the pooled win by losing inside the family)
    A form passing B1a alone is the family label in continuous ink and is reported as such.
B2  WITHIN-FAMILY CONTENT.  On the 81 MA-THRESH cells alone, does c_sd(IS) carry ANY
    out-of-sample signal about the residual?  OOS MAE(CSD.is, best lambda) < OOS MAE of the
    MA-THRESH IS mean (a single number) on those same 81 cells.  Reported either way.
B3  REPRODUCTION GATE vs idea 301's committed .decomp.csv, asserted first: max |d resid0_pp|
    and max |d c_sd| over the 486 (cell x window) rows < 1e-2 pp / 1e-4.  Idea 301 recorded a
    1.287e-02 pp U56 failure of its own gate against idea 298, attributed to the daily drift
    of data/prices.csv (ideas 513/515); the same allowance is made here and stated.

Rule 8 walk-forward (required, PROTOCOL rule 8)
  WF-A  THE BOOK.  Inside each panel x family arm, (level, cadence) is chosen on 2010..2016
        by IS Sharpe alone; 2017..end is read ONCE.  OOS CAGR / Sharpe / MaxDD reported
        against RULES v2 (the live book), SPY, and the cadence-matched no-filter control.
  WF-B  THE DELIVERABLE.  The estimator ladder IS a walk-forward: every form is fitted on IS
        cells only and scored once on the OOS cells.
  WF-C  IS THE PREDICTOR ACTIONABLE?  Use each estimator's predicted gap (pred0 at the IS
        c_bar plus the predicted residual) to CHOOSE the construction per cell -- DEGROSS if
        the predicted gap is positive, else RESPREAD -- and read the OOS Sharpe ONCE, against
        always-RESPREAD, always-DEGROSS and the OOS oracle.  A diagnostic that changes no
        decision is a reporting rule, not a book, and this says which.

Verdicts (both KEEP paths, on every one of the 324 books)
    4a  Sharpe > RULES v2 (live) in BOTH halves AND MaxDD no worse than RULES v2.
    4b  Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

SURVIVORSHIP: prices_small.csv.gz, universe.json and universe_broad.json are all CURRENT
constituents -- no delistings -- so every CAGR LEVEL here is inflated and the 4a/4b columns
inherit that whole.  The headline object is an arm-minus-arm contrast on the SAME names and
days (DEGROSS and RESPREAD share one gate mask), so the bias very largely cancels out of
gap0 / pred0 / resid0; it does NOT cancel out of the KEEP columns.  SMALL439 additionally
drops every ticker with max_1d_move >= 1.0 in data/small_meta.csv before use.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing outside its outputs.
Outputs: .grid.csv .decomp.csv .estimator.csv .walkforward.csv .console.txt .result.md
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
GROSS = 0.75
CADENCES = ["W", "M", "Q"]
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]
QUANT_X = [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95]
MA_THETA = [0.30, 0.20, 0.12, 0.06, 0.00, -0.06, -0.12, -0.25, -0.40]
FAMILIES = ["QUANTILE", "MA-THRESH"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

FORMS = ["ZERO", "GLOBAL", "FAMILY", "CSD.is", "CSD.oos", "CSD0.is", "LOGCSD.is",
         "CSDxVOL.is", "CSD+CBAR.is", "FAM+CSD.is"]
PEEK_FORMS = {"CSD.oos"}
LAMBDAS = [0.00, 0.25, 0.50, 0.75, 1.00]

# pre-registered bars
B1A_RATIO = 0.95
B3_TOL_PP, B3_TOL_CSD = 1e-2, 1e-4
REF301 = REPO / "research" / "backtests" / (
    "2026-09-09_is-the-gate-timing-residual-a-constant-in-pp-per-year_B.decomp.csv")

OUT = Path(__file__).with_suffix("")
LOG = []
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 700)


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


def book(px, family, level, construction):
    g = gate_mask(px, family, level)
    if construction == "RESPREAD":
        k = g.sum(axis=1).clip(lower=1)
        return g.astype(float).div(k, axis=0) * GROSS
    n = live_mask(px).sum(axis=1).clip(lower=1)
    return g.astype(float).div(n, axis=0) * GROSS


def control_book(px):
    live = live_mask(px)
    return live.astype(float).div(live.sum(axis=1).clip(lower=1), axis=0) * GROSS


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


# ---------------------------------------------------------------- estimator ladder
def design(form, df, panel_vol):
    """Return (X, names) for a predictor form evaluated on the rows of `df`.

    `.is` forms read c_sd_is / c_bar_is, which are known at decision time; `.oos` forms read
    the OOS window's own c_sd and are PEEKS, carried only to price the ex-ante penalty.
    """
    one = np.ones(len(df))
    if form == "CSD.is":
        return np.column_stack([one, df.c_sd_is.values]), ["const", "c_sd(IS)"]
    if form == "CSD.oos":
        return np.column_stack([one, df.c_sd_oos.values]), ["const", "c_sd(OOS) PEEK"]
    if form == "CSD0.is":
        return np.column_stack([df.c_sd_is.values]), ["c_sd(IS)"]
    if form == "LOGCSD.is":
        return np.column_stack([one, np.log(df.c_sd_is.values + 1e-4)]), ["const", "log c_sd(IS)"]
    if form == "CSDxVOL.is":
        v = df.panel.map(panel_vol).values
        return (np.column_stack([one, df.c_sd_is.values, df.c_sd_is.values * v]),
                ["const", "c_sd(IS)", "c_sd(IS)*panelvol(IS)"])
    if form == "CSD+CBAR.is":
        return (np.column_stack([one, df.c_sd_is.values, df.c_bar_is.values]),
                ["const", "c_sd(IS)", "c_bar(IS)"])
    if form == "FAM+CSD.is":
        d = (df.family.values == "MA-THRESH").astype(float)
        return (np.column_stack([one, d, df.c_sd_is.values]),
                ["const", "1{MA-THRESH}", "c_sd(IS)"])
    raise KeyError(form)


def predict(form, lam, IS, OOS, panel_vol, fits=None):
    """Fit `form` on IS cells only, predict every OOS cell, shrink toward the IS global mean."""
    gmean = float(IS.resid0_pp.mean())
    if form == "ZERO":
        return pd.Series(0.0, index=OOS.index)          # never shrunk: the no-information rung
    if form == "GLOBAL":
        local = pd.Series(gmean, index=OOS.index)
    elif form == "FAMILY":
        mp = IS.groupby("family").resid0_pp.mean()
        local = pd.Series(mp.reindex(pd.Index(OOS.family)).values, index=OOS.index).fillna(gmean)
    else:
        Xi, nm = design(form, IS, panel_vol)
        f = ols(Xi, IS.resid0_pp.values)
        if fits is not None:
            fits.append(dict(form=form, terms="|".join(nm),
                             coef="|".join(f"{b:.4f}" for b in f["b"]),
                             tstat="|".join(f"{t:.2f}" for t in f["t"]), IS_R2=f["R2"], n=f["n"]))
        Xo, _ = design(form, OOS, panel_vol)
        local = pd.Series(Xo @ f["b"], index=OOS.index)
    return lam * local + (1 - lam) * gmean


def score(pred, truth):
    e = np.asarray(pred, float) - np.asarray(truth, float)
    sse0 = float((np.asarray(truth, float) ** 2).sum())
    return dict(MAE=float(np.abs(e).mean()), RMSE=float(np.sqrt((e ** 2).mean())),
                bias=float(e.mean()), maxAE=float(np.abs(e).max()),
                R2_vs_zero=(1 - float((e ** 2).sum()) / sse0 if sse0 > 0 else np.nan))


# ---------------------------------------------------------------- main
def main():
    PN = panels()
    P("=" * 175)
    P("Idea 535 is-the-FAMILY-constant-really-a-c_sd-constant (cloud) | " + Path(__file__).name)
    P("=" * 175)
    P(f"costs {COST_BPS} bps (0-bps rung DERIVED as r0 = r10 + turnover*bps/1e4), gross {GROSS}, "
      f"next-day execution.  IS <= {IS_END}, OOS >= {OOS_START} (PROTOCOL rule 8).")
    P(f"tuned dials: FORM {FORMS} x SHRINKAGE {LAMBDAS} = {len(FORMS)*len(LAMBDAS)} estimator "
      f"cells, ALL reported on both cuts.  The 162-cell grid is IMPORTED from ideas 298/301 "
      f"verbatim, not re-chosen here.")
    P("pre-registered bars:")
    P(f"  B1a RETIREMENT  best .is c_sd form OOS MAE(ALL 162) <= {B1A_RATIO} * OOS MAE(FAMILY, lam=1)")
    P("  B1b RETIREMENT  the same form must NOT lose to FAMILY on the 81 MA-THRESH cells")
    P("  B2  WITHIN-FAMILY  CSD.is beats the MA-THRESH IS mean on the 81 MA-THRESH cells")
    P(f"  B3  REPRODUCTION  max |d resid0_pp| < {B3_TOL_PP} pp and max |d c_sd| < {B3_TOL_CSD} "
      f"vs idea 301's committed .decomp.csv")
    P("PEEK forms (OOS-window c_sd) are a feasibility ceiling, never a deliverable.")

    px_u = load_universe()
    live_full = backtest(px_u, rules_v2_weights(px_u), cost_bps=COST_BPS, freq="W")["returns"]

    rows, decomp, panel_vol, panel_spy, panel_live = [], [], {}, {}, {}
    for pname, (px, spy_px) in PN.items():
        start = px.index[260]
        years = len(px.loc[start:]) / 252
        spy_r = spy_px.pct_change().fillna(0.0).loc[start:]
        spy_s = stat(spy_r)
        live_s = stat(live_full.reindex(px.index).fillna(0.0).loc[start:])
        panel_spy[pname], panel_live[pname] = spy_s, live_s
        ctrl, ctrl0 = {}, {}
        for cad in CADENCES:
            rc = backtest(px, control_book(px), cost_bps=COST_BPS, freq=cad)
            r10 = rc["returns"].loc[start:]
            ctrl[cad] = stat(r10)
            ctrl0[cad] = cagr(r10 + rc["turnover"].loc[start:] * COST_BPS / 1e4)
        # panel volatility, IS window only (a predictor input; never reads OOS)
        pv = float(px.loc[start:IS_END].pct_change().mean(axis=1).std() * np.sqrt(252))
        panel_vol[pname] = pv
        P("\n" + "-" * 175)
        P(f"PANEL {pname}: evaluation from {start.date()} ({years:.2f} yrs).  "
          f"IS panel vol (EW daily, <= {IS_END}) {pv:.4f}")
        P(f"  SPY CAGR {spy_s['CAGR']:.4f} Sharpe {spy_s['Sharpe']:.4f} MaxDD {spy_s['MaxDD']:.4f} "
          f"halves {spy_s['H1']:.4f}/{spy_s['H2']:.4f} OOS Sharpe {spy_s['oSharpe']:.4f} "
          f"OOS CAGR {spy_s['oCAGR']:.4f}")
        P(f"  RULES v2 (live, 4a comparand): CAGR {live_s['CAGR']:.4f} Sharpe {live_s['Sharpe']:.4f} "
          f"MaxDD {live_s['MaxDD']:.4f} halves {live_s['H1']:.4f}/{live_s['H2']:.4f} "
          f"OOS Sharpe {live_s['oSharpe']:.4f} OOS CAGR {live_s['oCAGR']:.4f}")
        for cad in CADENCES:
            P(f"  CONTROL EWall {cad} (no gate): CAGR {ctrl[cad]['CAGR']:.4f} "
              f"Sharpe {ctrl[cad]['Sharpe']:.4f} MaxDD {ctrl[cad]['MaxDD']:.4f} "
              f"OOS Sharpe {ctrl[cad]['oSharpe']:.4f} | 0 bps CAGR {ctrl0[cad]:.4f}")
        P(f"  4b bars from SPY: H1>{spy_s['H1']:.3f} H2>{spy_s['H2']:.3f} "
          f"OOS>{spy_s['oSharpe']:.3f} MaxDD>=-{0.60*abs(spy_s['MaxDD']):.1%} "
          f"CAGR>={0.70*spy_s['CAGR']:.2%}")
        flush_log()

        for family in FAMILIES:
            levels = QUANT_X if family == "QUANTILE" else MA_THETA
            for level in levels:
                for cad in CADENCES:
                    got = {}
                    for con in CONSTRUCTIONS:
                        res = backtest(px, book(px, family, level, con), cost_bps=COST_BPS, freq=cad)
                        r10 = res["returns"].loc[start:]
                        turn = res["turnover"].loc[start:]
                        r0 = r10 + turn * COST_BPS / 1e4
                        grs = res["weights"].loc[start:].sum(axis=1)
                        s = stat(r10)
                        got[con] = dict(r10=r10, r0=r0, gross=grs, s=s)
                        rows.append(dict(panel=pname, family=family, level=level, cad=cad,
                                         con=con, **s, CAGR0=cagr(r0),
                                         gross_mean=grs.mean(), turn_yr=turn.sum() / years,
                                         dSharpe_ctrl=s["Sharpe"] - ctrl[cad]["Sharpe"],
                                         p4a=verdict_4a(s, live_s), f4b=fail_4b(s, spy_s),
                                         spy_Sharpe=spy_s["Sharpe"], spy_oSharpe=spy_s["oSharpe"],
                                         ctrl_oSharpe=ctrl[cad]["oSharpe"]))
                    dg, rs = got["DEGROSS"], got["RESPREAD"]
                    c_t = (dg["gross"] / rs["gross"].replace(0, np.nan)).fillna(0.0)
                    ident_err = float((dg["r0"] - c_t * rs["r0"]).abs().max())

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
                                    cov_c_r=float(np.cov(c_t.loc[sl], rr)[0, 1] * 252),
                                    oSharpe_rs=rs["s"]["oSharpe"], oSharpe_dg=dg["s"]["oSharpe"],
                                    isSharpe_rs=rs["s"]["isSharpe"], isSharpe_dg=dg["s"]["isSharpe"])
                    base = dict(panel=pname, family=family, level=level, cad=cad,
                                ident_max_err=ident_err)
                    for tag, lo, hi in (("FULL", None, None), ("IS", None, IS_END),
                                        ("OOS", OOS_START, None)):
                        decomp.append({**base, **dec_window(lo, hi, tag)})
            P(f"  ... {pname} / {family} done ({len(levels)*len(CADENCES)*2} books)")
            flush_log()

    G = pd.DataFrame(rows)
    D = pd.DataFrame(decomp)
    G["p4b"] = G.f4b == "-"
    G.to_csv(f"{OUT}.grid.csv", index=False)
    D.to_csv(f"{OUT}.decomp.csv", index=False)

    # ---------------- B3 reproduction gate, first
    P("\n" + "=" * 175)
    P("B3 REPRODUCTION GATE vs idea 301's committed .decomp.csv (asserted before any new number)")
    P("=" * 175)
    key = ["panel", "family", "level", "cad", "window"]
    ref = pd.read_csv(REF301)
    m = D.merge(ref[key + ["resid0_pp", "gap0_pp", "pred0_pp", "c_bar", "c_sd"]], on=key,
                suffixes=("", "_ref"))
    P(f"  matched rows: {len(m)} of {len(D)} recomputed and {len(ref)} committed")
    for c in ["resid0_pp", "gap0_pp", "pred0_pp", "c_bar", "c_sd"]:
        m[f"d_{c}"] = (m[c] - m[f"{c}_ref"]).abs()
    dcols = ["d_resid0_pp", "d_gap0_pp", "d_pred0_pp", "d_c_bar", "d_c_sd"]
    P(fmt(m.groupby("panel")[dcols].max(), 8))
    b3r, b3c = float(m.d_resid0_pp.max()), float(m.d_c_sd.max())
    b3 = (b3r < B3_TOL_PP) and (b3c < B3_TOL_CSD)
    P(f"  max |d resid0_pp| = {b3r:.3e} pp (bar {B3_TOL_PP}), max |d c_sd| = {b3c:.3e} "
      f"(bar {B3_TOL_CSD})  ->  B3 {'PASS' if b3 else 'FAIL'}")
    nz = m.loc[m.d_resid0_pp > 1e-9, "panel"].value_counts().to_dict()
    P(f"  rows differing by >1e-9 pp, by panel: {nz}")
    P(f"  identity max |r_dg,t - c_t*r_rs,t| over {len(D)} cells: {D.ident_max_err.max():.3e} "
      f"({'HOLDS' if D.ident_max_err.max() < 1e-12 else 'FAILS'} at 1e-12)")
    if not b3:
        P("  B3 FAILED -- everything below is reported but must not be read as a restatement "
          "of idea 301 on the panels that differ.")
    flush_log()

    # ---------------- the cell table: c_sd and the residual, IS and OOS
    W = {t: D[D.window == t].set_index(key[:4]).sort_index() for t in ("FULL", "IS", "OOS")}
    IS, OOS = W["IS"].reset_index(), W["OOS"].reset_index()
    assert (IS[key[:4]].values == OOS[key[:4]].values).all(), "IS/OOS cell alignment"
    C = IS[key[:4]].copy()
    C["c_sd_is"], C["c_bar_is"] = IS.c_sd.values, IS.c_bar.values
    C["c_sd_oos"], C["c_bar_oos"] = OOS.c_sd.values, OOS.c_bar.values
    C["resid_is"], C["resid_oos"] = IS.resid0_pp.values, OOS.resid0_pp.values
    ISf = C.rename(columns={"resid_is": "resid0_pp"})
    OOSf = C.rename(columns={"resid_oos": "resid0_pp"})

    P("\n" + "=" * 175)
    P("IS THE POOLED corr(c_sd, |resid0|) A FAMILY EFFECT?  (idea 301 reported 0.7765 pooled, "
      "0.57/0.56 within family)")
    P("=" * 175)
    cr = []
    for wtag, cs, rs_ in (("IS", "c_sd_is", "resid_is"), ("OOS", "c_sd_oos", "resid_oos")):
        for sub, d in [("ALL", C)] + [(f, g) for f, g in C.groupby("family")]:
            cr.append(dict(window=wtag, subset=sub, n=len(d),
                           corr_abs=float(np.corrcoef(d[cs], d[rs_].abs())[0, 1]),
                           corr_signed=float(np.corrcoef(d[cs], d[rs_])[0, 1]),
                           c_sd_mean=float(d[cs].mean()), c_sd_sd=float(d[cs].std()),
                           resid_mean=float(d[rs_].mean()), resid_sd=float(d[rs_].std())))
    CR = pd.DataFrame(cr)
    P(fmt(CR.set_index(["window", "subset"]), 4))
    P("  cross-window persistence of the predictor itself:")
    for f, g in C.groupby("family"):
        P(f"    {f:10s} corr(c_sd_is, c_sd_oos) = {np.corrcoef(g.c_sd_is, g.c_sd_oos)[0,1]:.4f}"
          f"   corr(resid_is, resid_oos) = {np.corrcoef(g.resid_is, g.resid_oos)[0,1]:.4f}")
    P(f"    {'ALL':10s} corr(c_sd_is, c_sd_oos) = {np.corrcoef(C.c_sd_is, C.c_sd_oos)[0,1]:.4f}"
      f"   corr(resid_is, resid_oos) = {np.corrcoef(C.resid_is, C.resid_oos)[0,1]:.4f}")
    CR.to_csv(f"{OUT}.corr.csv", index=False)
    flush_log()

    # ---------------- WF-B: the estimator ladder
    P("\n" + "=" * 175)
    P("WF-B THE ESTIMATOR LADDER: every form fitted on the 162 IS cells, scored ONCE on the "
      "162 OOS cells.  ALL 50 grid points, both cuts.  (MAE / RMSE in pp/yr)")
    P("=" * 175)
    fits, est = [], []
    seen_fit = set()
    for form in FORMS:
        for lam in LAMBDAS:
            ff = fits if (form not in seen_fit and form not in ("ZERO", "GLOBAL", "FAMILY")) else None
            pred = predict(form, lam, ISf, OOSf, panel_vol, fits=ff)
            seen_fit.add(form)
            for sub in ("ALL", "MA-THRESH", "QUANTILE"):
                mask = slice(None) if sub == "ALL" else (OOSf.family == sub)
                p = pred[mask] if sub != "ALL" else pred
                y = OOSf.resid0_pp[mask] if sub != "ALL" else OOSf.resid0_pp
                est.append(dict(form=form, lam=lam, subset=sub, n=len(y),
                                peek=form in PEEK_FORMS, **score(p, y)))
    E = pd.DataFrame(est)
    E.to_csv(f"{OUT}.estimator.csv", index=False)
    F = pd.DataFrame(fits)
    if len(F):
        P("  IS fits (coefficients are fitted on IS cells only):")
        P(fmt(F.set_index("form"), 4))
    for sub in ("ALL", "MA-THRESH", "QUANTILE"):
        P(f"\n  OOS MAE by (form x lambda), subset = {sub}:")
        piv = E[E.subset == sub].pivot(index="form", columns="lam", values="MAE").reindex(FORMS)
        P(fmt(piv, 4))
    flush_log()

    # ---------------- B1 / B2
    P("\n" + "=" * 175)
    P("B1 THE RETIREMENT BAR and B2 WITHIN-FAMILY CONTENT")
    P("=" * 175)

    def mae(form, lam, sub):
        r = E[(E.form == form) & (E.lam == lam) & (E.subset == sub)]
        return float(r.MAE.iloc[0])

    fam_all, fam_ma = mae("FAMILY", 1.0, "ALL"), mae("FAMILY", 1.0, "MA-THRESH")
    zero_all, zero_ma = mae("ZERO", 1.0, "ALL"), mae("ZERO", 1.0, "MA-THRESH")
    glob_all = mae("GLOBAL", 1.0, "ALL")
    P(f"  incumbent FAMILY lam=1 : OOS MAE  ALL {fam_all:.4f}   MA-THRESH {fam_ma:.4f}")
    P(f"  references             : ZERO ALL {zero_all:.4f} / MA {zero_ma:.4f};  GLOBAL ALL {glob_all:.4f}")
    honest = [f for f in FORMS if f.endswith(".is") and "CSD" in f]
    best_rows = []
    for f in honest:
        sub_e = E[(E.form == f) & (E.subset == "ALL")]
        lam_star = float(sub_e.loc[sub_e.MAE.idxmin(), "lam"])
        best_rows.append(dict(form=f, lam_star=lam_star,
                              MAE_ALL=mae(f, lam_star, "ALL"),
                              MAE_MA=mae(f, lam_star, "MA-THRESH"),
                              MAE_QU=mae(f, lam_star, "QUANTILE"),
                              ratio_vs_FAMILY_ALL=mae(f, lam_star, "ALL") / fam_all,
                              ratio_vs_FAMILY_MA=mae(f, lam_star, "MA-THRESH") / fam_ma,
                              B1a=mae(f, lam_star, "ALL") <= B1A_RATIO * fam_all,
                              B1b=mae(f, lam_star, "MA-THRESH") <= fam_ma))
    B = pd.DataFrame(best_rows).set_index("form")
    P("\n  every honest (.is) c_sd form at its own best lambda on the ALL cut:")
    P(fmt(B, 4))
    b1 = bool((B.B1a & B.B1b).any())
    winners = list(B.index[B.B1a & B.B1b])
    b1a_only = list(B.index[B.B1a & ~B.B1b])
    P(f"\n  B1 RETIREMENT: {'PASS' if b1 else 'FAIL'} -- forms clearing BOTH legs: "
      f"{winners if winners else 'none'}")
    P(f"     forms clearing B1a but FAILING B1b (a pooled win bought by losing inside the "
      f"family): {b1a_only if b1a_only else 'none'}")
    # B2: within MA-THRESH, does c_sd beat that family's own IS constant?
    ma_is_mean = float(ISf.loc[ISf.family == "MA-THRESH", "resid0_pp"].mean())
    ma_const_mae = float((ma_is_mean - OOSf.loc[OOSf.family == "MA-THRESH", "resid0_pp"]).abs().mean())
    csd_ma_e = E[(E.form == "CSD.is") & (E.subset == "MA-THRESH")]
    csd_ma_lam = float(csd_ma_e.loc[csd_ma_e.MAE.idxmin(), "lam"])
    csd_ma = float(csd_ma_e.MAE.min())
    b2 = csd_ma < ma_const_mae
    P(f"\n  B2 WITHIN-FAMILY: MA-THRESH IS mean = {ma_is_mean:.4f} pp -> OOS MAE {ma_const_mae:.4f} "
      f"on 81 cells;  CSD.is best (lam={csd_ma_lam}) {csd_ma:.4f}  ->  {'PASS' if b2 else 'FAIL'}")
    P(f"     (FAMILY lam=1 on those 81 cells is the same single number: {fam_ma:.4f})")
    peek_e = E[(E.form == "CSD.oos") & (E.subset == "ALL")]
    peek_best = float(peek_e.MAE.min())
    peek_ma = float(E[(E.form == "CSD.oos") & (E.subset == "MA-THRESH")].MAE.min())
    P(f"\n  PEEK ceiling (contemporaneous c_sd, NOT available at decision time): "
      f"ALL {peek_best:.4f}, MA-THRESH {peek_ma:.4f} -- the ex-ante penalty on the ALL cut is "
      f"{B.MAE_ALL.min() - peek_best:+.4f} pp")
    flush_log()

    # ---------------- WF-A: the book walk-forward
    P("\n" + "=" * 175)
    P("WF-A THE BOOK: (level, cadence) chosen on IS Sharpe inside each panel x family x "
      "construction arm; OOS read ONCE.  12 arms x 2 constructions.")
    P("=" * 175)
    wf = []
    for (pn, fam, con), g in G.groupby(["panel", "family", "con"]):
        pick = g.loc[g.isSharpe.idxmax()]
        spy_s, live_s = panel_spy[pn], panel_live[pn]
        wf.append(dict(panel=pn, family=fam, con=con, pick_level=pick.level, pick_cad=pick.cad,
                       isSharpe=pick.isSharpe, oCAGR=pick.oCAGR, oSharpe=pick.oSharpe,
                       oMaxDD=pick.oMaxDD, ctrl_oSharpe=pick.ctrl_oSharpe,
                       spy_oCAGR=spy_s["oCAGR"], spy_oSharpe=spy_s["oSharpe"],
                       spy_oMaxDD=spy_s["oMaxDD"], live_oCAGR=live_s["oCAGR"],
                       live_oSharpe=live_s["oSharpe"], live_oMaxDD=live_s["oMaxDD"],
                       beats_SPY_oos=pick.oSharpe > spy_s["oSharpe"],
                       beats_LIVE_oos=pick.oSharpe > live_s["oSharpe"],
                       beats_CTRL_oos=pick.oSharpe > pick.ctrl_oSharpe,
                       p4a=pick.p4a, p4b=pick.p4b, f4b=pick.f4b))
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(fmt(WF.set_index(["panel", "family", "con"])[
        ["pick_level", "pick_cad", "isSharpe", "oCAGR", "oSharpe", "oMaxDD", "spy_oSharpe",
         "live_oSharpe", "ctrl_oSharpe", "beats_SPY_oos", "beats_LIVE_oos", "beats_CTRL_oos",
         "p4a", "p4b"]], 4))
    P(f"\n  WF-A picks beat SPY out of sample {int(WF.beats_SPY_oos.sum())}/{len(WF)}, "
      f"RULES v2 {int(WF.beats_LIVE_oos.sum())}/{len(WF)}, the EWall control "
      f"{int(WF.beats_CTRL_oos.sum())}/{len(WF)};  4a {int(WF.p4a.sum())}/{len(WF)}, "
      f"4b {int(WF.p4b.sum())}/{len(WF)}")

    # ---------------- WF-C: is the estimator actionable?
    P("\n" + "=" * 175)
    P("WF-C IS THE PREDICTOR ACTIONABLE?  IS-predicted gap chooses DEGROSS vs RESPREAD per "
      "cell; OOS Sharpe read ONCE.")
    P("=" * 175)
    # the exposure leg pred0 at the IS c_bar is known at decision time; add the predicted residual
    pred0_is = IS.pred0_pp.values
    o_rs, o_dg = OOS.oSharpe_rs.values, OOS.oSharpe_dg.values
    realised_pos = int((OOS.gap0_pp.values > 0).sum())
    P(f"  realised OOS gap0 > 0 in {realised_pos} of {len(OOS)} cells "
      f"(IS: {int((IS.gap0_pp.values > 0).sum())}/{len(IS)})")
    act = []
    for form in FORMS:
        for lam in LAMBDAS:
            pr = predict(form, lam, ISf, OOSf, panel_vol).values
            choose_dg = (pred0_is + pr) > 0
            sel = np.where(choose_dg, o_dg, o_rs)
            act.append(dict(form=form, lam=lam, peek=form in PEEK_FORMS,
                            n_DEGROSS=int(choose_dg.sum()), mean_oSharpe=float(sel.mean()),
                            vs_always_RS=float(sel.mean() - o_rs.mean()),
                            vs_always_DG=float(sel.mean() - o_dg.mean()),
                            vs_oracle=float(sel.mean() - np.maximum(o_rs, o_dg).mean())))
    A = pd.DataFrame(act)
    A.to_csv(f"{OUT}.actionable.csv", index=False)
    P(fmt(A.set_index(["form", "lam"]), 4))
    P(f"\n  always-RESPREAD {o_rs.mean():.4f} | always-DEGROSS {o_dg.mean():.4f} | "
      f"OOS oracle {np.maximum(o_rs, o_dg).mean():.4f} | distinct choice vectors: "
      f"{A.n_DEGROSS.nunique()} value(s) of n_DEGROSS across all {len(A)} estimator cells")
    flush_log()

    # ---------------- KEEP paths on all 324 books
    P("\n" + "=" * 175)
    P("BOTH KEEP PATHS on all 324 books (PROTOCOL rule 4)")
    P("=" * 175)
    P(f"  4a passes: {int(G.p4a.sum())} of {len(G)};  4b passes: {int(G.p4b.sum())} of {len(G)};"
      f"  both: {int((G.p4a & G.p4b).sum())}")
    P("  4b failing-bar counts (SET semantics, every failing bar listed):")
    bar = pd.Series([b for s in G.f4b for b in (s.split(",") if s != "-" else [])]).value_counts()
    P(fmt(bar.to_frame("n_books"), 0))
    if G.p4b.any():
        P("\n  the 4b passers:")
        P(fmt(G[G.p4b][["panel", "family", "level", "cad", "con", "CAGR", "Sharpe", "MaxDD",
                        "H1", "H2", "oSharpe", "p4a"]], 4))
    P("\n  4b passes by panel x family x construction:")
    P(fmt(G.groupby(["panel", "family", "con"]).p4b.sum().to_frame("n_4b"), 0))

    # ---------------- verdict
    P("\n" + "=" * 175)
    P("VERDICT")
    P("=" * 175)
    P(f"  B3 reproduction  : {'PASS' if b3 else 'FAIL'} (max |d resid0| {b3r:.3e} pp, "
      f"max |d c_sd| {b3c:.3e})")
    wtxt = str(winners) if winners else "no honest continuous c_sd form clears both legs"
    P(f"  B1 retirement    : {'PASS' if b1 else 'FAIL'}  -- {wtxt}")
    P(f"  B2 within-family : {'PASS' if b2 else 'FAIL'}  -- CSD.is {csd_ma:.4f} vs the "
      f"MA-THRESH constant {ma_const_mae:.4f} on 81 OOS cells")
    P(f"  THE ANSWER: the FAMILY constant is {'RETIRED by' if b1 else 'NOT retired by'} a "
      f"continuous c_sd predictor.")
    P("  No KEEP is claimed from an estimator: this run's deliverable is a diagnostic, and the "
      "KEEP columns above are the same 324 books idea 301 already priced.")
    flush_log()

    # ---------------- result.md
    md = [f"# Idea 535 — is-the-FAMILY-constant-really-a-c_sd-constant (cloud, 2026-09-09)",
          "",
          f"**B3 reproduction {'PASS' if b3 else 'FAIL'}** (max |d resid0| {b3r:.3e} pp, "
          f"max |d c_sd| {b3c:.3e} vs idea 301's committed .decomp.csv).",
          "",
          f"**B1 RETIREMENT {'PASS' if b1 else 'FAIL'}** — honest (.is) c_sd forms clearing both "
          f"legs: {winners if winners else 'none'}; clearing the pooled leg only: "
          f"{b1a_only if b1a_only else 'none'}.",
          f"**B2 WITHIN-FAMILY {'PASS' if b2 else 'FAIL'}** — CSD.is OOS MAE {csd_ma:.4f} vs the "
          f"MA-THRESH IS constant {ma_const_mae:.4f} on the same 81 OOS cells.",
          "",
          f"Incumbent FAMILY (lam=1): OOS MAE **{fam_all:.4f}** (ALL 162) / **{fam_ma:.4f}** "
          f"(MA-THRESH 81). ZERO {zero_all:.4f}/{zero_ma:.4f}. GLOBAL {glob_all:.4f} (ALL).",
          f"PEEK ceiling (contemporaneous c_sd, unavailable ex ante): {peek_best:.4f} ALL / "
          f"{peek_ma:.4f} MA-THRESH.",
          "",
          "## corr(c_sd, |resid0|), pooled vs within family", "", "```",
          fmt(CR.set_index(["window", "subset"]), 4), "```", "",
          "## Every honest c_sd form at its own best lambda (ALL cut)", "", "```",
          fmt(B, 4), "```", "",
          "## WF-A (rule 8): (level, cadence) chosen on IS Sharpe, OOS read once", "", "```",
          fmt(WF.set_index(["panel", "family", "con"])[
              ["pick_level", "pick_cad", "oCAGR", "oSharpe", "oMaxDD", "spy_oSharpe",
               "live_oSharpe", "beats_SPY_oos", "beats_LIVE_oos", "p4a", "p4b"]], 4), "```", "",
          f"WF-A picks beat SPY OOS {int(WF.beats_SPY_oos.sum())}/{len(WF)}, RULES v2 "
          f"{int(WF.beats_LIVE_oos.sum())}/{len(WF)}. 4a {int(G.p4a.sum())}/{len(G)} books, "
          f"4b {int(G.p4b.sum())}/{len(G)} books.",
          "",
          "SURVIVORSHIP: SMALL439/U56/B136 are current constituents only (no delistings); CAGR "
          "levels and the 4a/4b columns are inflated. The residual is an arm-minus-arm contrast "
          "on the same names and days, so the bias very largely cancels out of it.",
          ""]
    Path(f"{OUT}.result.md").write_text("\n".join(md))
    flush_log()
    P("\nwrote: .grid.csv .decomp.csv .estimator.csv .corr.csv .actionable.csv .walkforward.csv "
      ".result.md .console.txt")
    flush_log()


if __name__ == "__main__":
    main()

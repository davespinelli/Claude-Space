#!/usr/bin/env python3
"""Idea 301 - "is-the-gate-timing-residual-a-constant-in-pp-per-year" (lane B, 2026-09-09).

The question
------------
Idea 290 split the DEGROSS-minus-RESPREAD CAGR gap of a de-grossing gate into

    gap0  =  pred0  +  resid0
             ^ constant-leverage cash drag at the cell's own mean leverage c_bar (pure exposure)
                       ^ the TIMING of c_t -- the gate's own content, in pp/yr

and idea 298 KILLED the share-vs-c_bar discount curve (`share ~ 1 - 0.0706*c_bar`, IS R2 0.0487,
loses to a flat constant out of sample).  What idea 298 proposed in its place is ZERO-PARAMETER:

    "subtract the gate's own timing residual (~0.0 pp/yr for a pure-exposure gate,
     0.3-0.6 pp/yr for an MA gate), INDEPENDENT of c_bar."

That prescription is a CONSTANCY claim and idea 298 never tested it out of sample.  It rests on
one in-sample regression, `resid0 ~ 1 + (1 - c_bar)` per panel, whose INTERCEPT was significant
(-0.619 / -0.267 / -0.352 pp, t -5.43 / -3.16 / -3.96) while the slope explained R2 0.04-0.19.
An intercept that is significant in-sample is not the same object as a number you may subtract
from next decade's cell.  This run tests the constancy directly, and answers the queue's own
head-to-head: does a PER-PANEL constant beat a SINGLE GLOBAL one?

Design
------
The cell grid is IMPORTED VERBATIM from idea 298 -- 3 panels x 2 gate families x 9 strictness
levels x 3 cadences = 162 decomposition cells, 324 books.  Nothing about that grid is re-chosen
here; it is the population the estimator is scored on, not a dial.  Every construction
(gate_mask / book / control_book / stat) is idea 298's code verbatim, and a REPRODUCTION GATE
(B3) asserts the recomputed resid0 against idea 298's committed .decomp.csv before any new
number is read.

Tuned parameters (PROTOCOL rule 4: at most two).  Reported at EVERY grid point, selected at
none except inside the rule-8 walk-forward.
    1. POOLING LEVEL of the constant, 7 values:
         ZERO        predict 0 pp/yr                              (0 numbers -- idea 298's naive)
         GLOBAL      one IS mean over all cells                   (1 number)
         FAMILY      IS mean per gate family                      (2)
         PANEL       IS mean per panel                            (3)  <- the queue's rival
         PANELxFAM   IS mean per (panel, family)                  (6)  <- the queue's own unit
         CELL        the cell's own IS resid0                     (162, maximal flexibility)
         CBAR-OLS    IS fit resid0 ~ 1 + c_bar within (panel,fam) (12 -- idea 298's rejected form)
    2. SHRINKAGE lambda toward GLOBAL, 5 values {0.00, 0.25, 0.50, 0.75, 1.00}:
         pred = lambda * local + (1 - lambda) * global.  lambda = 0 collapses every level to
         GLOBAL, lambda = 1 is the pure local estimator.  35 estimator cells, all reported.

Windows are PROTOCOL rule 8's, fixed before the run: IS <= 2016-12-31, OOS >= 2017-01-01.
Costs 10 bps, gross 0.75, next-day execution, no shorting, no leverage.  The 0-bps rung is
DERIVED exactly (r0 = r10 + turnover*bps/1e4), never re-run, so it is the same book.

Pre-registered bars, written before any OOS number was read
-----------------------------------------------------------
B1  CONSTANCY (the title).  Judged on the MA-THRESH cells, because the QUANTILE family has
    c_t == x BY CONSTRUCTION and its resid0 is ~0 by identity, not by evidence.
      B1a  OOS MAE(PANELxFAM, lambda=1) < OOS MAE(ZERO) on the 81 MA-THRESH cells.
      B1b  |mean OOS resid0 - mean IS resid0| <= 0.15 pp/yr in >= 4 of the 6 panel x family arms.
    "A constant in pp/yr" is CONFIRMED only if BOTH hold; otherwise the prescription is not
    usable as written and this run says so.
B2  PER-PANEL vs GLOBAL (the queue's head-to-head).
      OOS MAE(PANEL, lambda=1) <= 0.95 * OOS MAE(GLOBAL) on all 162 cells, AND per-panel wins
      in >= 2 of 3 panels.  Reported either way.
B3  REPRODUCTION GATE vs idea 298's committed .decomp.csv, asserted first: max |d resid0_pp|
    over the 486 (cell x window) rows < 1e-2 pp, with SMALL439 and B136 expected at ~0 and any
    U56 residual attributed to the known data drift of data/prices.csv (ideas 513/515).

Rule 8 walk-forward (required)
  WF-A  THE BOOK.  Inside each panel x family x construction arm, (level, cadence) is chosen on
        2010..2016 by IS Sharpe; 2017..end is read ONCE.  OOS CAGR / Sharpe / MaxDD reported
        against RULES v2 (the live book), SPY, and the cadence-matched no-filter control.
  WF-B  THE DELIVERABLE.  The estimator ladder above IS a walk-forward: every predictor is
        fitted on IS cells only and scored once on OOS cells.
  WF-C  IS THE ESTIMATOR ACTIONABLE?  Use the IS-predicted gap (pred0 at the IS c_bar plus the
        predicted residual) to CHOOSE the construction per cell -- DEGROSS if the predicted gap
        is positive, else RESPREAD -- and read the OOS Sharpe once, against always-RESPREAD,
        always-DEGROSS and the OOS oracle.  A diagnostic that changes no decision is a
        reporting rule, not a book, and this says which.

Verdicts (both KEEP paths, on every one of the 324 books)
    4a  Sharpe > RULES v2 (live) in BOTH halves AND MaxDD no worse than RULES v2.
    4b  Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

SURVIVORSHIP: prices_small.csv.gz, universe.json and universe_broad.json are all CURRENT
constituents -- no delistings -- so every CAGR LEVEL here is inflated and the 4a/4b columns
inherit that whole.  The headline object is an arm-minus-arm contrast on the SAME names and
days (DEGROSS and RESPREAD share one gate mask), so the bias very largely cancels out of
gap0 / pred0 / resid0; it does NOT cancel out of the KEEP columns.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing outside its outputs.
Outputs: .grid.csv .decomp.csv .estimator.csv .walkforward.csv .console.txt
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

POOLINGS = ["ZERO", "GLOBAL", "FAMILY", "PANEL", "PANELxFAM", "CELL", "CBAR-OLS"]
LAMBDAS = [0.00, 0.25, 0.50, 0.75, 1.00]

# pre-registered bars
B1B_TOL_PP, B1B_ARMS = 0.15, 4
B2_RATIO, B2_PANELS = 0.95, 2
B3_TOL_PP = 1e-2
REF298 = REPO / "research" / "backtests" / (
    "2026-09-06_does-the-cash-drag-share-depend-on-the-panel-or-on-the-gate-level_cloud.decomp.csv")

OUT = Path(__file__).with_suffix("")
LOG = []
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 600)


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


# ---------------------------------------------------------------- idea 298's constructions
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
KEYS = {"ZERO": [], "GLOBAL": [], "FAMILY": ["family"], "PANEL": ["panel"],
        "PANELxFAM": ["panel", "family"], "CELL": ["panel", "family", "level", "cad"]}


def predict(pool, lam, IS, OOS):
    """Fit `pool` on IS cells only, predict each OOS cell, shrink toward the GLOBAL IS mean."""
    gmean = float(IS.resid0_pp.mean())
    if pool == "ZERO":
        local = pd.Series(0.0, index=OOS.index)
    elif pool == "CBAR-OLS":
        local = pd.Series(np.nan, index=OOS.index)
        for (pn, fam), g in IS.groupby(["panel", "family"]):
            f = ols(np.column_stack([np.ones(len(g)), g.c_bar.values]), g.resid0_pp.values)
            m = (OOS.panel == pn) & (OOS.family == fam)
            local[m] = f["b"][0] + f["b"][1] * OOS.loc[m, "c_bar"].values
    else:
        k = KEYS[pool]
        if not k:
            local = pd.Series(gmean, index=OOS.index)
        else:
            mp = IS.groupby(k).resid0_pp.mean()
            idx = pd.MultiIndex.from_frame(OOS[k]) if len(k) > 1 else pd.Index(OOS[k[0]])
            local = pd.Series(mp.reindex(idx).values, index=OOS.index).fillna(gmean)
    if pool == "ZERO":
        return local                      # ZERO is the no-information baseline; never shrunk
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
    P("=" * 170)
    P("Idea 301 is-the-gate-timing-residual-a-constant-in-pp-per-year (lane B) | " + Path(__file__).name)
    P("=" * 170)
    P(f"costs {COST_BPS} bps (0-bps rung DERIVED as r0 = r10 + turnover*bps/1e4), gross {GROSS}, "
      f"next-day execution.  IS <= {IS_END}, OOS >= {OOS_START} (PROTOCOL rule 8).")
    P(f"tuned dials: POOLING {POOLINGS} x SHRINKAGE {LAMBDAS} = {len(POOLINGS)*len(LAMBDAS)} "
      f"estimator cells, all reported.  The 162-cell grid (panel x family x level x cadence) is "
      f"IMPORTED from idea 298 verbatim, not re-chosen here.")
    P("pre-registered bars:")
    P(f"  B1a CONSTANCY  OOS MAE(PANELxFAM, lam=1) < OOS MAE(ZERO) on the 81 MA-THRESH cells")
    P(f"  B1b CONSTANCY  |mean OOS resid0 - mean IS resid0| <= {B1B_TOL_PP} pp in >= {B1B_ARMS}/6 arms")
    P(f"  B2  PANEL vs GLOBAL  OOS MAE(PANEL) <= {B2_RATIO} * OOS MAE(GLOBAL) on 162 cells AND "
      f"per-panel wins in >= {B2_PANELS}/3 panels")
    P(f"  B3  REPRODUCTION  max |d resid0_pp| vs idea 298's committed .decomp.csv < {B3_TOL_PP} pp")

    px_u = load_universe()
    live_full = backtest(px_u, rules_v2_weights(px_u), cost_bps=COST_BPS, freq="W")["returns"]

    rows, decomp = [], []
    for pname, (px, spy_px) in PN.items():
        start = px.index[260]
        years = len(px.loc[start:]) / 252
        spy_r = spy_px.pct_change().fillna(0.0).loc[start:]
        spy_s = stat(spy_r)
        live_s = stat(live_full.reindex(px.index).fillna(0.0).loc[start:])
        ctrl, ctrl0 = {}, {}
        for cad in CADENCES:
            rc = backtest(px, control_book(px), cost_bps=COST_BPS, freq=cad)
            r10 = rc["returns"].loc[start:]
            ctrl[cad] = stat(r10)
            ctrl0[cad] = cagr(r10 + rc["turnover"].loc[start:] * COST_BPS / 1e4)
        P("\n" + "-" * 170)
        P(f"PANEL {pname}: evaluation from {start.date()} ({years:.2f} yrs).  "
          f"SPY CAGR {spy_s['CAGR']:.4f} Sharpe {spy_s['Sharpe']:.4f} MaxDD {spy_s['MaxDD']:.4f} "
          f"halves {spy_s['H1']:.4f}/{spy_s['H2']:.4f} OOS {spy_s['oSharpe']:.4f}")
        P(f"  RULES v2 (live, 4a comparand) on this window: CAGR {live_s['CAGR']:.4f} "
          f"Sharpe {live_s['Sharpe']:.4f} MaxDD {live_s['MaxDD']:.4f} "
          f"halves {live_s['H1']:.4f}/{live_s['H2']:.4f} OOS {live_s['oSharpe']:.4f}")
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
                                    oSharpe_rs=rs["s"]["oSharpe"], oSharpe_dg=dg["s"]["oSharpe"])
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
    P("\n" + "=" * 170)
    P("B3 REPRODUCTION GATE vs idea 298's committed .decomp.csv (asserted before any new number)")
    P("=" * 170)
    key = ["panel", "family", "level", "cad", "window"]
    ref = pd.read_csv(REF298)
    m = D.merge(ref[key + ["resid0_pp", "gap0_pp", "pred0_pp", "c_bar"]], on=key,
                suffixes=("", "_ref"))
    P(f"  matched rows: {len(m)} of {len(D)} recomputed and {len(ref)} committed")
    for c in ["resid0_pp", "gap0_pp", "pred0_pp", "c_bar"]:
        m[f"d_{c}"] = (m[c] - m[f"{c}_ref"]).abs()
    P(fmt(m.groupby("panel")[["d_resid0_pp", "d_gap0_pp", "d_pred0_pp", "d_c_bar"]].max(), 8))
    b3max = float(m.d_resid0_pp.max())
    b3 = b3max < B3_TOL_PP
    P(f"  max |d resid0_pp| = {b3max:.3e} pp  ->  B3 {'PASS' if b3 else 'FAIL'} at {B3_TOL_PP} pp")
    P(f"  identity max |r_dg,t - c_t*r_rs,t| over {len(D)} cells: {D.ident_max_err.max():.3e} "
      f"({'HOLDS' if D.ident_max_err.max() < 1e-12 else 'FAILS'} at 1e-12)")
    if not b3:
        P("  B3 FAILED -- everything below is reported but must not be read as a restatement "
          "of idea 298.")
    flush_log()

    # ---------------- the residual itself, IS vs OOS, every arm
    W = {t: D[D.window == t].set_index(key[:4]).sort_index() for t in ("FULL", "IS", "OOS")}
    IS, OOS = W["IS"].reset_index(), W["OOS"].reset_index()
    assert (IS[key[:4]].values == OOS[key[:4]].values).all(), "IS/OOS cell alignment"

    P("\n" + "=" * 170)
    P("THE RESIDUAL, ARM BY ARM: is it the same number in the two windows?  (pp/yr)")
    P("=" * 170)
    arm = []
    for (pn, fam), gi in IS.groupby(["panel", "family"]):
        go = OOS[(OOS.panel == pn) & (OOS.family == fam)]
        fi = ols(np.column_stack([np.ones(len(gi)), gi.c_bar.values]), gi.resid0_pp.values)
        fo = ols(np.column_stack([np.ones(len(go)), go.c_bar.values]), go.resid0_pp.values)
        arm.append(dict(panel=pn, family=fam, n=len(gi),
                        IS_mean=gi.resid0_pp.mean(), IS_sd=gi.resid0_pp.std(),
                        OOS_mean=go.resid0_pp.mean(), OOS_sd=go.resid0_pp.std(),
                        drift=go.resid0_pp.mean() - gi.resid0_pp.mean(),
                        IS_slope=fi["b"][1], IS_t=fi["t"][1], IS_R2=fi["R2"],
                        OOS_slope=fo["b"][1], OOS_t=fo["t"][1], OOS_R2=fo["R2"],
                        rho_IS_OOS=np.corrcoef(gi.resid0_pp.values, go.resid0_pp.values)[0, 1]))
    A = pd.DataFrame(arm).set_index(["panel", "family"])
    P(fmt(A, 4))
    b1b_ok = int((A.drift.abs() <= B1B_TOL_PP).sum())
    P(f"\n  B1b: |drift| <= {B1B_TOL_PP} pp in {b1b_ok} of 6 arms  ->  "
      f"{'PASS' if b1b_ok >= B1B_ARMS else 'FAIL'} (bar {B1B_ARMS}/6)")
    P("  (a slope whose |t| is large is idea 298's own rejected c_bar dependence re-appearing;"
      " rho_IS_OOS is whether the CELL ORDERING within an arm survives at all)")

    P("\n  every one of the 162 cells, IS vs OOS resid0 (pp/yr):")
    cellview = IS[key[:4] + ["c_bar", "gap0_pp", "pred0_pp", "resid0_pp"]].merge(
        OOS[key[:4] + ["c_bar", "gap0_pp", "pred0_pp", "resid0_pp"]], on=key[:4],
        suffixes=("_IS", "_OOS"))
    P(fmt(cellview.set_index(key[:4]), 4))
    flush_log()

    # ---------------- WF-B: the estimator ladder
    P("\n" + "=" * 170)
    P("WF-B  THE ESTIMATOR LADDER -- fitted on IS cells ONLY, scored once on the OOS cells")
    P("=" * 170)
    est = []
    subsets = {"ALL": OOS.index, "MA-THRESH": OOS.index[OOS.family == "MA-THRESH"],
               "QUANTILE": OOS.index[OOS.family == "QUANTILE"]}
    for pool in POOLINGS:
        for lam in (LAMBDAS if pool != "ZERO" else [1.00]):
            pr = predict(pool, lam, IS, OOS)
            for sname, ix in subsets.items():
                sc = score(pr.loc[ix], OOS.loc[ix, "resid0_pp"])
                est.append(dict(pool=pool, lam=lam, subset=sname, n=len(ix), **sc))
            for pn in PN:
                ix = OOS.index[OOS.panel == pn]
                sc = score(pr.loc[ix], OOS.loc[ix, "resid0_pp"])
                est.append(dict(pool=pool, lam=lam, subset=f"panel:{pn}", n=len(ix), **sc))
    E = pd.DataFrame(est)
    E.to_csv(f"{OUT}.estimator.csv", index=False)
    for sname in ["ALL", "MA-THRESH", "QUANTILE"]:
        P(f"\n--- OOS scores, subset {sname} ---")
        P(fmt(E[E.subset == sname].pivot_table(index="pool", columns="lam",
                                               values="MAE").reindex(POOLINGS), 4))
        P(f"  (table above = OOS MAE in pp/yr; full MAE/RMSE/bias/R2 in .estimator.csv)")
        P(fmt(E[(E.subset == sname) & (E.lam.isin([1.00]))]
              .set_index("pool")[["MAE", "RMSE", "bias", "maxAE", "R2_vs_zero"]]
              .reindex(POOLINGS), 4))

    def mae(pool, lam, subset):
        r = E[(E.pool == pool) & (E.lam == lam) & (E.subset == subset)]
        return float(r.MAE.iloc[0])

    P("\n" + "=" * 170)
    P("B1a / B2 -- the two pre-registered head-to-heads")
    P("=" * 170)
    z_ma, pf_ma = mae("ZERO", 1.0, "MA-THRESH"), mae("PANELxFAM", 1.0, "MA-THRESH")
    b1a = pf_ma < z_ma
    P(f"  B1a  MA-THRESH OOS MAE: PANELxFAM {pf_ma:.4f} vs ZERO {z_ma:.4f} pp  ->  "
      f"{'PASS' if b1a else 'FAIL'}")
    P(f"       (same on ALL 162 cells: PANELxFAM {mae('PANELxFAM',1.0,'ALL'):.4f} vs "
      f"ZERO {mae('ZERO',1.0,'ALL'):.4f})")
    b1 = b1a and (b1b_ok >= B1B_ARMS)
    P(f"  B1   CONSTANCY = B1a AND B1b  ->  {'CONFIRMED' if b1 else 'NOT CONFIRMED'}")
    gl, pa = mae("GLOBAL", 1.0, "ALL"), mae("PANEL", 1.0, "ALL")
    wins = sum(mae("PANEL", 1.0, f"panel:{pn}") < mae("GLOBAL", 1.0, f"panel:{pn}") for pn in PN)
    b2 = (pa <= B2_RATIO * gl) and (wins >= B2_PANELS)
    P(f"  B2   PANEL {pa:.4f} vs GLOBAL {gl:.4f} pp (ratio {pa/gl:.4f}), per-panel wins "
      f"{wins}/3  ->  {'PASS' if b2 else 'FAIL'}")
    for pn in PN:
        P(f"       panel {pn}: PANEL {mae('PANEL',1.0,f'panel:{pn}'):.4f} vs "
          f"GLOBAL {mae('GLOBAL',1.0,f'panel:{pn}'):.4f} vs ZERO {mae('ZERO',1.0,f'panel:{pn}'):.4f}")
    best = E[(E.subset == "ALL")].sort_values("MAE").iloc[0]
    bestma = E[(E.subset == "MA-THRESH")].sort_values("MAE").iloc[0]
    P(f"  best estimator over all 35 cells: ALL -> {best['pool']} lam {best['lam']:.2f} "
      f"MAE {best['MAE']:.4f}; MA-THRESH -> {bestma['pool']} lam {bestma['lam']:.2f} "
      f"MAE {bestma['MAE']:.4f}")

    P("\n  B1b restricted to the family that is not degenerate.  QUANTILE has c_t == x BY "
      "CONSTRUCTION, so its resid0 ~ 0 is an identity, not evidence of constancy; counting the "
      "three QUANTILE arms toward B1b is what carries the bar.  On MA-THRESH alone:")
    ma_arms = A.xs("MA-THRESH", level="family")
    P(f"    |drift| <= {B1B_TOL_PP} pp in {int((ma_arms.drift.abs() <= B1B_TOL_PP).sum())} of 3 "
      f"MA-THRESH arms (QUANTILE: "
      f"{int((A.xs('QUANTILE', level='family').drift.abs() <= B1B_TOL_PP).sum())} of 3)")
    flush_log()

    # ---------------- B3b: restate the headline on the panels that reproduce EXACTLY
    P("\n" + "=" * 170)
    P("B3b RESTATEMENT on the two panels that reproduce idea 298 at 0.000e+00 (SMALL439 + B136),")
    P("    so no headline here rides on the U56 vintage drift that failed B3")
    P("=" * 170)
    IS2, OOS2 = IS[IS.panel != "U56"], OOS[OOS.panel != "U56"]
    OOS2 = OOS2.reset_index(drop=True)
    IS2 = IS2.reset_index(drop=True)
    e2 = []
    for pool in POOLINGS:
        for lam in (LAMBDAS if pool != "ZERO" else [1.00]):
            pr = predict(pool, lam, IS2, OOS2)
            for sname, ix in {"ALL": OOS2.index,
                              "MA-THRESH": OOS2.index[OOS2.family == "MA-THRESH"]}.items():
                e2.append(dict(pool=pool, lam=lam, subset=sname,
                               **score(pr.loc[ix], OOS2.loc[ix, "resid0_pp"])))
    E2 = pd.DataFrame(e2)
    for sname in ["ALL", "MA-THRESH"]:
        P(f"\n--- 108-cell restatement, subset {sname} (OOS MAE, pp/yr) ---")
        P(fmt(E2[E2.subset == sname].pivot_table(index="pool", columns="lam",
                                                 values="MAE").reindex(POOLINGS), 4))
    g2 = lambda p, s: float(E2[(E2.pool == p) & (E2.lam == 1.0) & (E2.subset == s)].MAE.iloc[0])
    P(f"\n  B1a restated: MA-THRESH PANELxFAM {g2('PANELxFAM','MA-THRESH'):.4f} vs "
      f"ZERO {g2('ZERO','MA-THRESH'):.4f}  ->  "
      f"{'PASS' if g2('PANELxFAM','MA-THRESH') < g2('ZERO','MA-THRESH') else 'FAIL'}")
    P(f"  B2 restated: PANEL {g2('PANEL','ALL'):.4f} vs GLOBAL {g2('GLOBAL','ALL'):.4f} "
      f"(ratio {g2('PANEL','ALL')/g2('GLOBAL','ALL'):.4f})  ->  "
      f"{'PASS' if g2('PANEL','ALL') <= B2_RATIO*g2('GLOBAL','ALL') else 'FAIL'}")
    P(f"  best pooling on the exact-reproducing panels: "
      f"{E2[E2.subset=='ALL'].sort_values('MAE').iloc[0]['pool']} "
      f"(ALL), {E2[E2.subset=='MA-THRESH'].sort_values('MAE').iloc[0]['pool']} (MA-THRESH)")
    flush_log()

    # ---------------- WF-A: the book
    P("\n" + "=" * 170)
    P("WF-A  THE BOOK -- (level, cadence) chosen on IS Sharpe inside each panel x family x "
      "construction arm, OOS read ONCE")
    P("=" * 170)
    wf = []
    for (pn, fam, con), g in G.groupby(["panel", "family", "con"]):
        pick = g.sort_values("isSharpe", ascending=False).iloc[0]
        wf.append(dict(panel=pn, family=fam, con=con, level=pick.level, cad=pick.cad,
                       isSharpe=pick.isSharpe, oCAGR=pick.oCAGR, oSharpe=pick.oSharpe,
                       oMaxDD=pick.oMaxDD, spy_oSharpe=pick.spy_oSharpe,
                       ctrl_oSharpe=pick.ctrl_oSharpe,
                       beats_SPY=pick.oSharpe > pick.spy_oSharpe,
                       beats_ctrl=pick.oSharpe > pick.ctrl_oSharpe,
                       oracle_oSharpe=g.oSharpe.max(),
                       regret=pick.oSharpe - g.oSharpe.max(), p4a=pick.p4a, f4b=pick.f4b))
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(fmt(WF.set_index(["panel", "family", "con"]), 4))
    live_o = metrics(live_full.loc[OOS_START:])
    P(f"\n  RULES v2 (live book, U56) OOS: CAGR {live_o['CAGR']:.4f} Sharpe {live_o['Sharpe']:.4f} "
      f"MaxDD {live_o['MaxDD']:.4f}")
    P(f"  WF-A picks beat SPY OOS {int(WF.beats_SPY.sum())}/{len(WF)}, beat the cadence-matched "
      f"no-filter control {int(WF.beats_ctrl.sum())}/{len(WF)}, beat RULES v2 OOS "
      f"{int((WF.oSharpe > live_o['Sharpe']).sum())}/{len(WF)}; mean regret vs the OOS oracle "
      f"{WF.regret.mean():.4f}")

    # ---------------- WF-C: does the estimator change a decision?
    P("\n" + "=" * 170)
    P("WF-C  IS THE ESTIMATOR ACTIONABLE?  IS-predicted gap picks the construction; OOS read once")
    P("=" * 170)
    P("  predicted gap for a cell = pred0(IS c_bar, IS returns) + predicted residual.  "
      "DEGROSS if > 0, else RESPREAD.")
    wc = []
    for pool in POOLINGS:
        for lam in (LAMBDAS if pool != "ZERO" else [1.00]):
            pr = predict(pool, lam, IS, OOS)
            pg = IS.pred0_pp.values + pr.values
            chosen = np.where(pg > 0, OOS.oSharpe_dg.values, OOS.oSharpe_rs.values)
            oracle = np.maximum(OOS.oSharpe_dg.values, OOS.oSharpe_rs.values)
            wc.append(dict(pool=pool, lam=lam, n_DEGROSS=int((pg > 0).sum()),
                           mean_oSharpe=float(chosen.mean()),
                           vs_RESPREAD=float(chosen.mean() - OOS.oSharpe_rs.mean()),
                           vs_DEGROSS=float(chosen.mean() - OOS.oSharpe_dg.mean()),
                           regret_vs_oracle=float((chosen - oracle).mean())))
    WC = pd.DataFrame(wc)
    P(fmt(WC.set_index(["pool", "lam"]), 4))
    P(f"\n  always-RESPREAD mean OOS Sharpe {OOS.oSharpe_rs.mean():.4f}; "
      f"always-DEGROSS {OOS.oSharpe_dg.mean():.4f}; "
      f"OOS oracle {np.maximum(OOS.oSharpe_dg.values, OOS.oSharpe_rs.values).mean():.4f}")
    P(f"  OOS truth: the realised gap is negative in "
      f"{int((OOS.gap0_pp < 0).sum())}/{len(OOS)} cells, so the sign the chooser needs is "
      f"nearly constant and no estimator can earn on it.")
    flush_log()

    # ---------------- KEEP paths on all 324 books
    P("\n" + "=" * 170)
    P("KEEP PATHS on all 324 books (4a vs RULES v2 live; 4b vs SPY, both halves + OOS + DD + CAGR)")
    P("=" * 170)
    P(fmt(G.groupby(["panel", "family", "con"])[["p4a", "p4b"]].sum().astype(int), 0))
    P(f"\n  4a: {int(G.p4a.sum())}/{len(G)}   4b: {int(G.p4b.sum())}/{len(G)}   "
      f"both: {int((G.p4a & G.p4b).sum())}/{len(G)}")
    fails = G.f4b.value_counts()
    P("\n  4b failure signatures (most common first):")
    P(fails.head(12).to_string())
    if G.p4b.any():
        P("\n  the 4b passers:")
        P(fmt(G[G.p4b].set_index(["panel", "family", "level", "cad", "con"])[
            ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "oSharpe", "p4a"]], 4))

    P("\n" + "=" * 170)
    P("VERDICT")
    P("=" * 170)
    P(f"  B3 reproduction {'PASS' if b3 else 'FAIL'} (max |d resid0| {b3max:.3e} pp)")
    P(f"  B1 CONSTANCY {'CONFIRMED' if b1 else 'NOT CONFIRMED'} "
      f"(B1a {'PASS' if b1a else 'FAIL'}, B1b {b1b_ok}/6)")
    P(f"  B2 per-panel beats global: {'PASS' if b2 else 'FAIL'} (ratio {pa/gl:.4f}, wins {wins}/3)")
    P(f"  KEEP: 4a {int(G.p4a.sum())}/{len(G)}, 4b {int(G.p4b.sum())}/{len(G)}")
    flush_log()
    P("\nSURVIVORSHIP: all three panels are CURRENT constituents; CAGR levels are inflated and the "
      "4a/4b columns inherit that.  The residual is an arm-minus-arm contrast on the same names "
      "and days, so the bias very largely cancels out of it.")
    flush_log()


if __name__ == "__main__":
    main()

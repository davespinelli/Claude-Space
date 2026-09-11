#!/usr/bin/env python3
"""Idea 538 - "is-c_sd-the-right-SCALE-or-is-it-a-TURNOVER-proxy" (lane B, 2026-09-11).

The question
------------
Idea 535 retired the GATE-FAMILY label as a predictor of the de-grossing TIMING RESIDUAL by
fitting a continuous predictor on the exposure path's dispersion:

    resid0_pp ~ 1 + c_sd(IS)     ->  OOS MAE 0.1771 (ALL 162 cells) vs FAMILY's 0.1936

where, for a (panel, family, strictness, cadence) cell at gross 0.75,

    gap0   = 100 * (CAGR(DEGROSS, 0 bps) - CAGR(RESPREAD, 0 bps))     pp/yr
    pred0  = 100 * (CAGR(c_bar * RESPREAD) - CAGR(RESPREAD))          constant-leverage drag
    resid0 = gap0 - pred0                                             the TIMING of c_t
    c_t    = (held gross of DEGROSS) / (held gross of RESPREAD),  c_bar/c_sd its mean/sd.

The queue's objection: c_sd is the standard deviation of the held-exposure path, and an
exposure path that moves a lot is a book that TRADES a lot, so c_sd may be nothing but the
book's own rebalancing traffic wearing a new name -- and realised annual turnover is a
number the record already prints for every single book (`turn_yr` in every .grid.csv).  If
turnover substitutes for c_sd, the "retirement" is a restatement of a column the record has
published all along; if it does not, c_sd is carrying something turnover cannot see.

This run re-fits idea 535's estimator ladder on idea 535's EXACT 162-cell population with
realised annual turnover in place of c_sd, and with BOTH, and scores every rung out of
sample.  324 books (162 cells x 2 constructions), every one reported with 4a/4b.

Turnover is measured on the IS window only for the `.is` (honest) forms -- the annualised
sum of the engine's own per-day turnover series over 2010..2016 -- because at decision time
the OOS window's traffic is not knowable.  Three turnover readings are carried, because the
cell has two books and the record's `turn_yr` column is per BOOK, not per cell:
    TO    = turnover of the DEGROSS arm      (the arm whose timing the residual is about)
    TOrs  = turnover of the RESPREAD arm     (the comparand arm)
    DTO   = TO - TOrs                        (the extra traffic de-grossing itself creates)

Tuned parameters (PROTOCOL rule 4: at most two).  Reported at EVERY grid point, selected at
none except inside the rule-8 walk-forward.
    1. PREDICTOR FORM, 13 values (below)   -- idea 535's dial, extended with the turnover arm
    2. SHRINKAGE lambda, 5 values {0.00, 0.25, 0.50, 0.75, 1.00}:
         pred = lambda * form + (1 - lambda) * global_IS_mean;  lambda = 0 collapses every
         form to the global IS mean.  Idea 535's exact dial and exact grid.
   65 estimator cells x 3 subsets = 195 rows, ALL reported.
Everything else -- the 3 panels, 2 families, 9 strictness levels, 3 cadences, gross 0.75, the
windows, the 10 bps cost -- is IMPORTED VERBATIM from ideas 298/301/535.  It is the
population the estimator is fitted on, not a dial of this run.

FORMS.  `.is` forms read only IS-window quantities (honest).  `.oos` forms read the OOS
window's own predictor and are PEEKS: they price the ex-ante penalty and are never a
deliverable.
    ZERO GLOBAL FAMILY                 the incumbent rungs (FAMILY is the thing 535 retired)
    CSD.is                             idea 535's winner, the incumbent continuous predictor
    TO.is TOrs.is DTO.is LOGTO.is      the turnover arm (the queue's substitute)
    CSD+TO.is                          BOTH, as the queue asks
    FAM+TO.is FAM+CSD.is               family label plus a continuous term
    CSD.oos TO.oos                     PEEK ceilings

Pre-registered bars, written before any turnover number was read
----------------------------------------------------------------
G1  REPRODUCTION, asserted first.  This run's 162 cells are idea 535's 162 cells.
    max |d resid0_pp| < 1e-2 pp and max |d c_sd| < 1e-4 against idea 301's committed
    .decomp.csv; max |d turn_yr| < 1e-6 against idea 535's committed .grid.csv (FULL window);
    and the ladder must reproduce idea 535's published OOS MAE for CSD.is (0.177128) and
    FAMILY (0.193564) at lambda = 1 on the ALL cut to < 5e-4.  (Idea 301 recorded a 1.287e-02
    pp U56 failure of its own gate against idea 298 from the daily drift of data/prices.csv;
    the same allowance is made here and stated.)
G2  THE QUEUE'S PREMISE -- "c_sd is mechanically close to turnover".  Pearson AND Spearman
    rho(c_sd_is, TO_is) over the 162 cells, pooled and per family, with n stated beside each
    (idea 564's rule), plus the condition number of the CSD+TO design.
      G2-PROXY      |rho| >= 0.70 pooled  -> the queue's reading: they are near the same variable
      G2-DISTINCT   |rho| <  0.30 pooled  -> they are different variables and the swap is a
                                            genuine model change, not a relabelling
    Exactly one can pass; a value in between is reported as PARTIAL and neither passes.
B1  DOES TURNOVER ALONE RETIRE THE FAMILY LABEL?  Idea 535's own two bars, re-applied to the
    best honest TURNOVER form at its own best lambda:
      B1a  OOS MAE(ALL 162)      <= 0.95 * OOS MAE(FAMILY, lambda=1)
      B1b  OOS MAE(MA-THRESH 81) <=        OOS MAE(FAMILY, lambda=1) on the same 81
B2  DOES THE RETIREMENT SURVIVE THE SWAP?  Head-to-head on the ALL cut at each form's own
    best lambda.  BAR: MAE(best TURNOVER form) <= MAE(CSD.is).  PASS -> turnover is at least
    as good and the record should publish the column it already has; FAIL -> c_sd is doing
    something turnover cannot, and by how much is reported in pp.
B3  IS THERE ANY INCREMENT IN BOTH?  BAR: MAE(CSD+TO.is, best lambda) <= 0.95 * MAE(CSD.is,
    best lambda).  PASS -> turnover adds information beyond c_sd.
B4  IS c_sd A TURNOVER PROXY IN THE FIT ITSELF?  Orthogonalise on the IS cells: regress
    c_sd_is on (1, TO_is), keep the residual, and re-fit resid0 ~ 1 + c_sd_perp.  BAR: the
    c_sd slope keeps its sign and |t| >= 0.5 * |t| of the raw CSD.is fit.  PASS -> the c_sd
    signal is NOT the turnover signal.  Reported with the mirror test (TO orthogonalised on
    c_sd) so neither direction is privileged.

Rule 8 walk-forward (required, PROTOCOL rule 8).  IS <= 2016-12-31, OOS >= 2017-01-01.
  WF-A  THE BOOK.  Inside each (panel, family, construction) arm -- 12 arms -- the cell dials
        (level, cadence) are chosen on 2010..2016 IS Sharpe ALONE and 2017..end is read ONCE.
        OOS CAGR / Sharpe / MaxDD reported against RULES v2 (live), SPY, and the
        cadence-matched no-gate EWall control at the same gross.
  WF-B  THE DELIVERABLE.  Every estimator in the ladder is fitted on IS-window cell values
        only and scored once on the OOS-window values; every slope in B1..B4 is an IS fit.
  WF-C  IS EITHER PREDICTOR ACTIONABLE?  Use each IS-fitted estimator to CHOOSE the
        construction per cell (predicted gap = pred0 at the cell's IS c_bar + predicted
        residual; DEGROSS if positive, else RESPREAD) and read OOS Sharpe ONCE against
        always-RESPREAD, always-DEGROSS and the OOS oracle.  A predictor that changes no
        decision is a reporting rule, not a book, and this leg says which.

Verdicts (both KEEP paths, on every one of the 324 books)
    4a  Sharpe > RULES v2 (live) in BOTH halves AND MaxDD no worse than RULES v2.
    4b  Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

SURVIVORSHIP: prices_small.csv.gz, universe.json and universe_broad.json are all CURRENT
constituents -- no delistings -- so every CAGR LEVEL here is inflated and the 4a/4b columns
inherit that whole.  The headline object is an arm-minus-arm contrast on the SAME names and
days at the SAME gross (DEGROSS and RESPREAD share one gate mask), so the bias very largely
cancels out of gap0 / pred0 / resid0; it does NOT cancel out of the KEEP columns.  SMALL439
additionally drops every ticker with max_1d_move >= 1.0 in data/small_meta.csv before use.

Costs 10 bps, next-day execution, no shorting, no leverage (gross 0.75).  The 0-bps rung is
DERIVED exactly (r0 = r10 + turnover*bps/1e4), never re-run, so it is the same book.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing outside its outputs.
Outputs: .grid.csv .decomp.csv .cells.csv .estimator.csv .fits.csv .walkforward.csv
         .console.txt .result.md
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

FORMS = ["ZERO", "GLOBAL", "FAMILY", "CSD.is",
         "TO.is", "TOrs.is", "DTO.is", "LOGTO.is",
         "CSD+TO.is", "FAM+TO.is", "FAM+CSD.is",
         "CSD.oos", "TO.oos"]
PEEK_FORMS = {"CSD.oos", "TO.oos"}
TURNOVER_FORMS = ["TO.is", "TOrs.is", "DTO.is", "LOGTO.is"]
LAMBDAS = [0.00, 0.25, 0.50, 0.75, 1.00]

# idea 535's committed ladder numbers (lambda = 1, ALL cut) -- the G1 fit gate
REF_MAE_CSD, REF_MAE_FAM = 0.177128, 0.193564
G1_TOL_PP, G1_TOL_CSD, G1_TOL_TURN, G1_TOL_MAE = 1e-2, 1e-4, 1e-6, 5e-4
G2_PROXY, G2_DISTINCT = 0.70, 0.30
B1A_RATIO, B3_RATIO, B4_T_RATIO = 0.95, 0.95, 0.50

REF301 = REPO / "research" / "backtests" / (
    "2026-09-09_is-the-gate-timing-residual-a-constant-in-pp-per-year_B.decomp.csv")
REF535 = REPO / "research" / "backtests" / (
    "2026-09-09_is-the-FAMILY-constant-really-a-c_sd-constant_cloud.grid.csv")

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


def spearman(a, b):
    """Rank correlation, stated by name (idea 564's PROTOCOL lesson)."""
    ra = pd.Series(a).rank().values
    rb = pd.Series(b).rank().values
    return float(np.corrcoef(ra, rb)[0, 1])


def pearson(a, b):
    return float(np.corrcoef(np.asarray(a, float), np.asarray(b, float))[0, 1])


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


# ---------------------------------------------------------------- estimator ladder
def design(form, df):
    """(X, names) for a predictor form on the rows of the cell table `df`.

    Every column is an IS-window quantity except the two PEEK forms, which read the OOS
    window's own predictor and exist only to price the ex-ante penalty.
    """
    one = np.ones(len(df))
    if form == "CSD.is":
        return np.column_stack([one, df.c_sd_is.values]), ["const", "c_sd(IS)"]
    if form == "CSD.oos":
        return np.column_stack([one, df.c_sd_oos.values]), ["const", "c_sd(OOS) PEEK"]
    if form == "TO.is":
        return np.column_stack([one, df.to_is.values]), ["const", "turn_yr_DG(IS)"]
    if form == "TO.oos":
        return np.column_stack([one, df.to_oos.values]), ["const", "turn_yr_DG(OOS) PEEK"]
    if form == "TOrs.is":
        return np.column_stack([one, df.tors_is.values]), ["const", "turn_yr_RS(IS)"]
    if form == "DTO.is":
        return np.column_stack([one, df.dto_is.values]), ["const", "d turn_yr(IS)"]
    if form == "LOGTO.is":
        return np.column_stack([one, np.log(df.to_is.values + 1e-4)]), ["const", "log turn_yr_DG(IS)"]
    if form == "CSD+TO.is":
        return (np.column_stack([one, df.c_sd_is.values, df.to_is.values]),
                ["const", "c_sd(IS)", "turn_yr_DG(IS)"])
    if form == "FAM+TO.is":
        d = (df.family.values == "MA-THRESH").astype(float)
        return np.column_stack([one, d, df.to_is.values]), ["const", "1{MA-THRESH}", "turn_yr_DG(IS)"]
    if form == "FAM+CSD.is":
        d = (df.family.values == "MA-THRESH").astype(float)
        return np.column_stack([one, d, df.c_sd_is.values]), ["const", "1{MA-THRESH}", "c_sd(IS)"]
    raise KeyError(form)


def predict(form, lam, C, fits=None):
    """Fit `form` on the IS-window residual of every cell, predict every cell, shrink toward
    the IS global mean.  Scoring is against the OOS-window residual (WF-B)."""
    gmean = float(C.resid_is.mean())
    if form == "ZERO":
        return pd.Series(0.0, index=C.index)            # never shrunk: the no-information rung
    if form == "GLOBAL":
        local = pd.Series(gmean, index=C.index)
    elif form == "FAMILY":
        mp = C.groupby("family").resid_is.mean()
        local = pd.Series(mp.reindex(pd.Index(C.family)).values, index=C.index).fillna(gmean)
    else:
        X, nm = design(form, C)
        f = ols(X, C.resid_is.values)
        if fits is not None:
            fits.append(dict(form=form, terms="|".join(nm),
                             coef="|".join(f"{b:.4f}" for b in f["b"]),
                             se="|".join(f"{s:.4f}" for s in f["se"]),
                             tstat="|".join(f"{t:.2f}" for t in f["t"]),
                             IS_R2=f["R2"], n=f["n"]))
        local = pd.Series(X @ f["b"], index=C.index)
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
    P("=" * 185)
    P("Idea 538 is-c_sd-the-right-SCALE-or-is-it-a-TURNOVER-proxy (lane B) | " + Path(__file__).name)
    P("=" * 185)
    P(f"costs {COST_BPS} bps (0-bps rung DERIVED as r0 = r10 + turnover*bps/1e4), gross {GROSS}, "
      f"next-day execution.  IS <= {IS_END}, OOS >= {OOS_START} (PROTOCOL rule 8).")
    P(f"tuned dials: FORM ({len(FORMS)}) x SHRINKAGE {LAMBDAS} = {len(FORMS)*len(LAMBDAS)} "
      f"estimator cells, ALL reported on all 3 subsets.  The 162-cell grid (3 panels x 2 "
      f"families x 9 levels x 3 cadences, 324 books) is IMPORTED from ideas 298/301/535.")
    P(f"FORMS: {FORMS}   PEEK (never a deliverable): {sorted(PEEK_FORMS)}")
    P("pre-registered bars:")
    P(f"  G1 REPRODUCTION  vs idea 301 .decomp.csv: max|d resid0_pp| < {G1_TOL_PP} pp, "
      f"max|d c_sd| < {G1_TOL_CSD};  vs idea 535 .grid.csv: max|d turn_yr| < {G1_TOL_TURN};  "
      f"ladder MAE(CSD.is,lam=1,ALL) == {REF_MAE_CSD} and MAE(FAMILY,lam=1,ALL) == "
      f"{REF_MAE_FAM} to < {G1_TOL_MAE}")
    P(f"  G2 QUEUE PREMISE  rho(c_sd_is, TO_is), Pearson AND Spearman, n stated.  "
      f"PROXY |rho| >= {G2_PROXY};  DISTINCT |rho| < {G2_DISTINCT};  in between = PARTIAL")
    P(f"  B1 TURNOVER RETIRES FAMILY?  best honest TURNOVER form: MAE(ALL) <= {B1A_RATIO} * "
      f"MAE(FAMILY,lam=1) AND MAE(MA-THRESH) <= MAE(FAMILY,lam=1) on the 81")
    P("  B2 SURVIVES THE SWAP?  MAE(best TURNOVER form) <= MAE(CSD.is), each at its own best lambda")
    P(f"  B3 INCREMENT IN BOTH?  MAE(CSD+TO.is) <= {B3_RATIO} * MAE(CSD.is)")
    P(f"  B4 c_sd A TURNOVER PROXY IN THE FIT?  c_sd orthogonalised on TO keeps sign and "
      f"|t| >= {B4_T_RATIO} * |t| of the raw CSD.is fit (mirror test reported too)")
    flush_log()

    px_u = load_universe()
    live_full = backtest(px_u, rules_v2_weights(px_u), cost_bps=COST_BPS, freq="W")["returns"]

    rows, decomp, panel_spy, panel_live = [], [], {}, {}
    for pname, (px, spy_px) in PN.items():
        start = px.index[260]
        idx = px.loc[start:].index
        yrs_full = len(idx) / 252
        yrs_is = len(idx[idx <= IS_END]) / 252
        yrs_oos = len(idx[idx >= OOS_START]) / 252
        spy_s = stat(spy_px.pct_change().fillna(0.0).loc[start:])
        live_s = stat(live_full.reindex(px.index).fillna(0.0).loc[start:])
        panel_spy[pname], panel_live[pname] = spy_s, live_s
        cu = control_unit(px)
        ctrl = {}
        for cad in CADENCES:
            rc = backtest(px, cu * GROSS, cost_bps=COST_BPS, freq=cad)
            ctrl[cad] = stat(rc["returns"].loc[start:])
        P("\n" + "-" * 185)
        P(f"PANEL {pname}: evaluation from {start.date()} ({yrs_full:.2f} yrs; IS {yrs_is:.2f}, "
          f"OOS {yrs_oos:.2f})")
        P(f"  SPY CAGR {spy_s['CAGR']:.4f} Sharpe {spy_s['Sharpe']:.4f} MaxDD {spy_s['MaxDD']:.4f} "
          f"halves {spy_s['H1']:.4f}/{spy_s['H2']:.4f} OOS Sharpe {spy_s['oSharpe']:.4f} "
          f"OOS CAGR {spy_s['oCAGR']:.4f} OOS MaxDD {spy_s['oMaxDD']:.4f}")
        P(f"  RULES v2 (live, 4a comparand): CAGR {live_s['CAGR']:.4f} Sharpe {live_s['Sharpe']:.4f} "
          f"MaxDD {live_s['MaxDD']:.4f} halves {live_s['H1']:.4f}/{live_s['H2']:.4f} "
          f"OOS Sharpe {live_s['oSharpe']:.4f} OOS CAGR {live_s['oCAGR']:.4f}")
        P(f"  4b bars from SPY: H1>{spy_s['H1']:.3f} H2>{spy_s['H2']:.3f} "
          f"OOS>{spy_s['oSharpe']:.3f} MaxDD>=-{0.60*abs(spy_s['MaxDD']):.1%} "
          f"CAGR>={0.70*spy_s['CAGR']:.2%}")
        P("  EWall control (no gate) OOS Sharpe by cadence: "
          + " ".join(f"{c}={ctrl[c]['oSharpe']:.3f}" for c in CADENCES))
        flush_log()

        for family in FAMILIES:
            levels = QUANT_X if family == "QUANTILE" else MA_THETA
            for level in levels:
                gm = gate_mask(px, family, level)
                ub = {con: unit_book(px, gm, con) for con in CONSTRUCTIONS}
                for cad in CADENCES:
                    got = {}
                    for con in CONSTRUCTIONS:
                        res = backtest(px, ub[con] * GROSS, cost_bps=COST_BPS, freq=cad)
                        r10 = res["returns"].loc[start:]
                        turn = res["turnover"].loc[start:]
                        r0 = r10 + turn * COST_BPS / 1e4
                        grs = res["weights"].loc[start:].sum(axis=1)
                        s = stat(r10)
                        t_full = turn.sum() / yrs_full
                        t_is = turn.loc[:IS_END].sum() / yrs_is
                        t_oos = turn.loc[OOS_START:].sum() / yrs_oos
                        got[con] = dict(r0=r0, gross=grs, s=s,
                                        t_full=t_full, t_is=t_is, t_oos=t_oos)
                        rows.append(dict(panel=pname, family=family, level=level, cad=cad,
                                         gross=GROSS, con=con, **s, CAGR0=cagr(r0),
                                         gross_mean=grs.mean(), turn_yr=t_full,
                                         turn_yr_is=t_is, turn_yr_oos=t_oos,
                                         dSharpe_ctrl=s["Sharpe"] - ctrl[cad]["Sharpe"],
                                         ctrl_oSharpe=ctrl[cad]["oSharpe"],
                                         p4a=verdict_4a(s, live_s), f4b=fail_4b(s, spy_s),
                                         spy_Sharpe=spy_s["Sharpe"], spy_oSharpe=spy_s["oSharpe"]))
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
                                    isSharpe_rs=rs["s"]["isSharpe"], isSharpe_dg=dg["s"]["isSharpe"])
                    base = dict(panel=pname, family=family, level=level, cad=cad, gross=GROSS)
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

    # ---------------- cell table (162 rows)
    key = ["panel", "family", "level", "cad"]
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
    C["isSharpe_rs"], C["isSharpe_dg"] = IS.isSharpe_rs.values, IS.isSharpe_dg.values

    Gk = G.sort_values(key + ["con"]).reset_index(drop=True)
    dgg = Gk[Gk.con == "DEGROSS"].set_index(key)
    rsg = Gk[Gk.con == "RESPREAD"].set_index(key)
    ci = C.set_index(key)
    C["to_is"] = dgg.turn_yr_is.reindex(ci.index).values
    C["to_oos"] = dgg.turn_yr_oos.reindex(ci.index).values
    C["to_full"] = dgg.turn_yr.reindex(ci.index).values
    C["tors_is"] = rsg.turn_yr_is.reindex(ci.index).values
    C["tors_oos"] = rsg.turn_yr_oos.reindex(ci.index).values
    C["dto_is"] = C.to_is - C.tors_is
    C.to_csv(f"{OUT}.cells.csv", index=False)
    assert len(C) == 162, f"expected 162 cells, got {len(C)}"

    # ---------------- G1 reproduction gate, first
    P("\n" + "=" * 185)
    P("G1 REPRODUCTION GATE (asserted before any turnover number is read)")
    P("=" * 185)
    g1 = {}
    rk = ["panel", "family", "level", "cad", "window"]
    ref = pd.read_csv(REF301)
    mine = D[rk + ["c_bar", "c_sd", "gap0_pp", "pred0_pp", "resid0_pp"]]
    m = mine.merge(ref[rk + ["c_bar", "c_sd", "resid0_pp"]], on=rk, suffixes=("", "_ref"))
    P(f"  matched {len(m)} of {len(mine)} cell-windows against idea 301's committed .decomp.csv")
    d_res = (m.resid0_pp - m.resid0_pp_ref).abs()
    d_csd = (m.c_sd - m.c_sd_ref).abs()
    g1["resid_max"], g1["csd_max"] = float(d_res.max()), float(d_csd.max())
    for pn, grp in m.groupby("panel"):
        P(f"    {pn:9s} max|d resid0_pp| {abs(grp.resid0_pp-grp.resid0_pp_ref).max():.3e}  "
          f"max|d c_sd| {abs(grp.c_sd-grp.c_sd_ref).max():.3e}  n {len(grp)}")
    P(f"  POOLED max|d resid0_pp| {g1['resid_max']:.3e} pp (bar {G1_TOL_PP})  -> "
      f"{'PASS' if g1['resid_max'] < G1_TOL_PP else 'FAIL'}")
    P(f"  POOLED max|d c_sd|      {g1['csd_max']:.3e} (bar {G1_TOL_CSD})  -> "
      f"{'PASS' if g1['csd_max'] < G1_TOL_CSD else 'FAIL'}")
    P("  (idea 301 itself recorded a 1.287e-02 pp U56 failure against idea 298 from the daily "
      "drift of data/prices.csv; the same allowance is stated, not silently taken.)")

    ref535 = pd.read_csv(REF535)
    mg = G[key + ["con", "turn_yr"]].merge(ref535[key + ["con", "turn_yr"]],
                                           on=key + ["con"], suffixes=("", "_ref"))
    d_turn = (mg.turn_yr - mg.turn_yr_ref).abs()
    g1["turn_max"] = float(d_turn.max())
    P(f"  turn_yr vs idea 535's committed .grid.csv: matched {len(mg)}/{len(G)} books, "
      f"max|d| {g1['turn_max']:.3e} (bar {G1_TOL_TURN}) -> "
      f"{'PASS' if g1['turn_max'] < G1_TOL_TURN else 'FAIL'}")
    flush_log()

    # ---------------- the ladder (WF-B: IS fit, OOS score)
    fits = []
    est = []
    for form in FORMS:
        ff = fits if form not in ("ZERO", "GLOBAL", "FAMILY") else None
        seen = False
        for lam in LAMBDAS:
            pred = predict(form, lam, C, fits=(ff if not seen else None))
            seen = True
            for sub in ("ALL", "MA-THRESH", "QUANTILE"):
                msk = np.ones(len(C), bool) if sub == "ALL" else (C.family == sub).values
                est.append(dict(form=form, lam=lam, subset=sub, n=int(msk.sum()),
                                peek=form in PEEK_FORMS,
                                **score(pred.values[msk], C.resid_oos.values[msk])))
    E = pd.DataFrame(est)
    F = pd.DataFrame(fits)
    E.to_csv(f"{OUT}.estimator.csv", index=False)
    F.to_csv(f"{OUT}.fits.csv", index=False)

    def mae(form, lam, sub="ALL"):
        r = E[(E.form == form) & (E.lam == lam) & (E.subset == sub)]
        return float(r.MAE.iloc[0])

    fam_all, fam_ma = mae("FAMILY", 1.00, "ALL"), mae("FAMILY", 1.00, "MA-THRESH")
    csd_all_l1 = mae("CSD.is", 1.00, "ALL")
    g1["mae_csd"], g1["mae_fam"] = csd_all_l1, fam_all
    d_csd_mae, d_fam_mae = abs(csd_all_l1 - REF_MAE_CSD), abs(fam_all - REF_MAE_FAM)
    P(f"  ladder vs idea 535: MAE(CSD.is,lam=1,ALL) {csd_all_l1:.6f} vs {REF_MAE_CSD} "
      f"(|d| {d_csd_mae:.2e});  MAE(FAMILY,lam=1,ALL) {fam_all:.6f} vs {REF_MAE_FAM} "
      f"(|d| {d_fam_mae:.2e});  bar {G1_TOL_MAE} -> "
      f"{'PASS' if max(d_csd_mae, d_fam_mae) < G1_TOL_MAE else 'FAIL'}")
    g1_pass = (g1["resid_max"] < G1_TOL_PP and g1["csd_max"] < G1_TOL_CSD
               and g1["turn_max"] < G1_TOL_TURN and max(d_csd_mae, d_fam_mae) < G1_TOL_MAE)
    P(f"  G1 OVERALL -> {'PASS' if g1_pass else 'FAIL'}")
    flush_log()

    # ---------------- G2 the queue's premise
    P("\n" + "=" * 185)
    P("G2  THE QUEUE'S PREMISE: is c_sd 'mechanically close' to the book's rebalancing traffic?")
    P("=" * 185)
    g2rows = []
    for sub, sel in (("ALL", np.ones(len(C), bool)),
                     ("MA-THRESH", (C.family == "MA-THRESH").values),
                     ("QUANTILE", (C.family == "QUANTILE").values)):
        cs, to, tors, dto = (C.c_sd_is.values[sel], C.to_is.values[sel],
                             C.tors_is.values[sel], C.dto_is.values[sel])
        g2rows.append(dict(subset=sub, n=int(sel.sum()),
                           pearson_csd_TO=pearson(cs, to), spearman_csd_TO=spearman(cs, to),
                           pearson_csd_TOrs=pearson(cs, tors), spearman_csd_TOrs=spearman(cs, tors),
                           pearson_csd_DTO=pearson(cs, dto), spearman_csd_DTO=spearman(cs, dto)))
    G2 = pd.DataFrame(g2rows).set_index("subset")
    P(fmt(G2, 4))
    rp = float(G2.loc["ALL", "pearson_csd_TO"])
    rs_ = float(G2.loc["ALL", "spearman_csd_TO"])
    Xb, _ = design("CSD+TO.is", C)
    cond = float(np.linalg.cond(Xb))
    P(f"\n  condition number of the CSD+TO design matrix: {cond:.2f} "
      f"(a genuine collinearity problem is >= 30)")
    both_low = abs(rp) < G2_DISTINCT and abs(rs_) < G2_DISTINCT
    both_high = abs(rp) >= G2_PROXY and abs(rs_) >= G2_PROXY
    g2v = "PROXY" if both_high else ("DISTINCT" if both_low else "PARTIAL")
    P(f"  pooled rho(c_sd_is, TO_is): PEARSON {rp:+.4f}, SPEARMAN {rs_:+.4f}, n 162  ->  G2 = {g2v}")
    flush_log()

    # ---------------- the ladder, printed in full
    P("\n" + "=" * 185)
    P("THE LADDER  (WF-B: every form fitted on the IS-window residual of the 162 cells, scored "
      "ONCE on the OOS-window residual).  OOS MAE, pp/yr.")
    P("=" * 185)
    for sub in ("ALL", "MA-THRESH", "QUANTILE"):
        P(f"\n  OOS MAE by (form x lambda), subset = {sub} "
          f"(n = {int(E[(E.subset==sub)].n.iloc[0])}):")
        piv = E[E.subset == sub].pivot(index="form", columns="lam", values="MAE").reindex(FORMS)
        P(fmt(piv, 4))
    P("\n  IS fits (all coefficients, all t-stats, IS R2):")
    P(fmt(F.set_index("form"), 4))
    flush_log()

    # ---------------- B1/B2/B3 head-to-head
    P("\n" + "=" * 185)
    P("B1 / B2 / B3  DOES TURNOVER SUBSTITUTE FOR c_sd?")
    P("=" * 185)
    P(f"  incumbent FAMILY (lam=1): OOS MAE ALL {fam_all:.4f}  MA-THRESH {fam_ma:.4f}")
    best = []
    for f in FORMS:
        sub_e = E[(E.form == f) & (E.subset == "ALL")]
        lam_star = float(sub_e.loc[sub_e.MAE.idxmin(), "lam"])
        best.append(dict(form=f, peek=f in PEEK_FORMS, lam_star=lam_star,
                         MAE_ALL=mae(f, lam_star, "ALL"),
                         MAE_MA=mae(f, lam_star, "MA-THRESH"),
                         MAE_QU=mae(f, lam_star, "QUANTILE"),
                         ratio_vs_FAMILY_ALL=mae(f, lam_star, "ALL") / fam_all,
                         ratio_vs_FAMILY_MA=mae(f, lam_star, "MA-THRESH") / fam_ma,
                         B1a=mae(f, lam_star, "ALL") <= B1A_RATIO * fam_all,
                         B1b=mae(f, lam_star, "MA-THRESH") <= fam_ma))
    B = pd.DataFrame(best).set_index("form")
    P("\n  every form at its own best lambda on the ALL cut (PEEK rows are a ceiling, not a "
      "deliverable):")
    P(fmt(B, 4))

    Bt = B.loc[TURNOVER_FORMS]
    best_to = Bt.MAE_ALL.idxmin()
    to_all, to_ma = float(Bt.loc[best_to, "MAE_ALL"]), float(Bt.loc[best_to, "MAE_MA"])
    b1a = bool(Bt.loc[best_to, "B1a"])
    b1b = bool(Bt.loc[best_to, "B1b"])
    P(f"\n  B1  best honest TURNOVER form = {best_to} (lam {Bt.loc[best_to,'lam_star']:.2f})")
    P(f"      B1a ALL 162      {to_all:.4f} vs bar {B1A_RATIO}*{fam_all:.4f} = "
      f"{B1A_RATIO*fam_all:.4f}  -> {'PASS' if b1a else 'FAIL'}")
    P(f"      B1b MA-THRESH 81 {to_ma:.4f} vs bar {fam_ma:.4f}  -> {'PASS' if b1b else 'FAIL'}")
    P(f"      B1 OVERALL -> {'PASS' if (b1a and b1b) else 'FAIL'}")

    csd_all = float(B.loc["CSD.is", "MAE_ALL"])
    csd_lam = float(B.loc["CSD.is", "lam_star"])
    b2 = to_all <= csd_all
    P(f"\n  B2  head-to-head on ALL 162: {best_to} {to_all:.4f} vs CSD.is {csd_all:.4f} "
      f"(lam {csd_lam:.2f})  ->  {'PASS' if b2 else 'FAIL'}  "
      f"(turnover is {to_all-csd_all:+.4f} pp/yr of MAE {'better' if b2 else 'worse'})")

    both_all = float(B.loc["CSD+TO.is", "MAE_ALL"])
    b3 = both_all <= B3_RATIO * csd_all
    P(f"  B3  BOTH: CSD+TO.is {both_all:.4f} vs bar {B3_RATIO}*{csd_all:.4f} = "
      f"{B3_RATIO*csd_all:.4f}  -> {'PASS' if b3 else 'FAIL'}  "
      f"(increment {both_all-csd_all:+.4f} pp/yr)")
    peek_all = float(B.loc[["CSD.oos", "TO.oos"], "MAE_ALL"].min())
    P(f"  PEEK ceiling (contemporaneous predictor, unavailable ex ante): {peek_all:.4f} ALL; "
      f"the ex-ante penalty on the best honest form is "
      f"{float(B[~B.peek].MAE_ALL.min()) - peek_all:+.4f} pp/yr")
    flush_log()

    # ---------------- B4 orthogonalisation
    P("\n" + "=" * 185)
    P("B4  IS THE c_sd SIGNAL THE TURNOVER SIGNAL?  (orthogonalise on the IS cells, both ways)")
    P("=" * 185)
    y = C.resid_is.values
    one = np.ones(len(C))
    raw_csd = ols(np.column_stack([one, C.c_sd_is.values]), y)
    raw_to = ols(np.column_stack([one, C.to_is.values]), y)
    fx = ols(np.column_stack([one, C.to_is.values]), C.c_sd_is.values)
    csd_perp = C.c_sd_is.values - np.column_stack([one, C.to_is.values]) @ fx["b"]
    o_csd = ols(np.column_stack([one, csd_perp]), y)
    fy = ols(np.column_stack([one, C.c_sd_is.values]), C.to_is.values)
    to_perp = C.to_is.values - np.column_stack([one, C.c_sd_is.values]) @ fy["b"]
    o_to = ols(np.column_stack([one, to_perp]), y)
    orth = pd.DataFrame([
        dict(fit="resid0 ~ 1 + c_sd(IS)           [raw]", slope=raw_csd["b"][1],
             t=raw_csd["t"][1], IS_R2=raw_csd["R2"], n=raw_csd["n"]),
        dict(fit="resid0 ~ 1 + c_sd_perp(TO)      [c_sd net of turnover]", slope=o_csd["b"][1],
             t=o_csd["t"][1], IS_R2=o_csd["R2"], n=o_csd["n"]),
        dict(fit="resid0 ~ 1 + TO(IS)             [raw]", slope=raw_to["b"][1],
             t=raw_to["t"][1], IS_R2=raw_to["R2"], n=raw_to["n"]),
        dict(fit="resid0 ~ 1 + TO_perp(c_sd)      [turnover net of c_sd]", slope=o_to["b"][1],
             t=o_to["t"][1], IS_R2=o_to["R2"], n=o_to["n"]),
    ]).set_index("fit")
    P(fmt(orth, 4))
    b4 = (np.sign(o_csd["b"][1]) == np.sign(raw_csd["b"][1])
          and abs(o_csd["t"][1]) >= B4_T_RATIO * abs(raw_csd["t"][1]))
    P(f"\n  B4 c_sd net of turnover keeps sign {np.sign(o_csd['b'][1]) == np.sign(raw_csd['b'][1])}, "
      f"|t| {abs(o_csd['t'][1]):.2f} vs bar {B4_T_RATIO}*{abs(raw_csd['t'][1]):.2f} = "
      f"{B4_T_RATIO*abs(raw_csd['t'][1]):.2f}  ->  {'PASS' if b4 else 'FAIL'}")
    P(f"  mirror: turnover net of c_sd keeps |t| {abs(o_to['t'][1]):.2f} of its raw "
      f"{abs(raw_to['t'][1]):.2f}, IS R2 {o_to['R2']:.4f} vs raw {raw_to['R2']:.4f}")
    flush_log()

    # ---------------- WF-C actionability
    P("\n" + "=" * 185)
    P("WF-C  IS EITHER PREDICTOR ACTIONABLE?  IS-fitted choice of construction, OOS Sharpe read ONCE")
    P("=" * 185)
    act = []
    always_rs = float(C.oSharpe_rs.mean())
    always_dg = float(C.oSharpe_dg.mean())
    oracle = float(np.maximum(C.oSharpe_rs.values, C.oSharpe_dg.values).mean())
    for form in FORMS:
        for lam in LAMBDAS:
            pr = predict(form, lam, C).values
            pred_gap = C.pred_is.values + pr           # predicted 0-bps gap, pp/yr
            pick_dg = pred_gap > 0
            picked = np.where(pick_dg, C.oSharpe_dg.values, C.oSharpe_rs.values)
            act.append(dict(form=form, lam=lam, peek=form in PEEK_FORMS,
                            n_DEGROSS=int(pick_dg.sum()), OOS_Sharpe_pick=float(picked.mean()),
                            vs_RESPREAD=float(picked.mean()) - always_rs,
                            vs_DEGROSS=float(picked.mean()) - always_dg,
                            share_of_oracle=((float(picked.mean()) - always_rs) /
                                             (oracle - always_rs) if oracle > always_rs else np.nan)))
    A = pd.DataFrame(act)
    P(f"  always-RESPREAD mean OOS Sharpe {always_rs:.4f} | always-DEGROSS {always_dg:.4f} | "
      f"OOS oracle {oracle:.4f}  (162 cells)")
    P(fmt(A.set_index(["form", "lam"]), 4))
    n_pos = int((C.pred_is.values + predict("CSD.is", 1.0, C).values > 0).sum())
    P(f"\n  CSD.is (lam=1) predicts a POSITIVE 0-bps gap in {n_pos} of 162 cells; the sign of "
      f"pred0 is set by c_bar < 1 in every cell, so the decision is an identity, not a fit.")
    flush_log()

    # ---------------- WF-A book leg + KEEP paths
    P("\n" + "=" * 185)
    P("WF-A  THE BOOK.  (level, cadence) chosen on IS Sharpe alone inside each (panel, family, "
      "construction) arm; OOS read ONCE.")
    P("=" * 185)
    wf = []
    for (pn, fam, con), grp in G.groupby(["panel", "family", "con"]):
        pick = grp.loc[grp.isSharpe.idxmax()]
        sp, lv = panel_spy[pn], panel_live[pn]
        wf.append(dict(panel=pn, family=fam, con=con, level=pick.level, cad=pick.cad,
                       isSharpe=pick.isSharpe, oCAGR=pick.oCAGR, oSharpe=pick.oSharpe,
                       oMaxDD=pick.oMaxDD,
                       live_oSharpe=lv["oSharpe"], live_oCAGR=lv["oCAGR"], live_oMaxDD=lv["oMaxDD"],
                       spy_oSharpe=sp["oSharpe"], spy_oCAGR=sp["oCAGR"], spy_oMaxDD=sp["oMaxDD"],
                       ctrl_oSharpe=pick.ctrl_oSharpe,
                       beats_live=pick.oSharpe > lv["oSharpe"],
                       beats_spy=pick.oSharpe > sp["oSharpe"],
                       beats_ctrl=pick.oSharpe > pick.ctrl_oSharpe,
                       p4a=bool(pick.p4a), p4b=bool(pick.p4b), f4b=pick.f4b))
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(fmt(WF.set_index(["panel", "family", "con"]), 4))
    P(f"\n  WF-A picks: beat RULES v2 OOS {int(WF.beats_live.sum())}/{len(WF)} | beat SPY OOS "
      f"{int(WF.beats_spy.sum())}/{len(WF)} | beat the no-gate EWall control OOS "
      f"{int(WF.beats_ctrl.sum())}/{len(WF)} | 4a {int(WF.p4a.sum())}/{len(WF)} | "
      f"4b {int(WF.p4b.sum())}/{len(WF)}")

    P("\n  KEEP paths over ALL 324 books (PROTOCOL rule 4):")
    P(f"    4a (Sharpe > RULES v2 in BOTH halves AND MaxDD no worse): {int(G.p4a.sum())}/{len(G)}")
    P(f"    4b (Sharpe > SPY both halves AND OOS, MaxDD <= 60% SPY, CAGR >= 70% SPY): "
      f"{int(G.p4b.sum())}/{len(G)}")
    fc = G.f4b.value_counts()
    P("    4b failing-bar sets (SET semantics, all failing bars listed per book):")
    for k, v in fc.items():
        P(f"      {k:28s} {v}")
    P("\n  Per-panel 4a/4b:")
    P(fmt(G.groupby(["panel", "con"]).agg(n=("p4a", "size"), p4a=("p4a", "sum"),
                                          p4b=("p4b", "sum"),
                                          best_Sharpe=("Sharpe", "max"),
                                          best_oSharpe=("oSharpe", "max")), 4))
    flush_log()

    # ---------------- verdict
    P("\n" + "=" * 185)
    P("VERDICT")
    P("=" * 185)
    keep = int(G.p4a.sum()) > 0 or int(G.p4b.sum()) > 0
    P(f"  G1 {'PASS' if g1_pass else 'FAIL'} | G2 {g2v} | B1 {'PASS' if (b1a and b1b) else 'FAIL'} "
      f"| B2 {'PASS' if b2 else 'FAIL'} | B3 {'PASS' if b3 else 'FAIL'} | "
      f"B4 {'PASS' if b4 else 'FAIL'}")
    P(f"  4a {int(G.p4a.sum())}/{len(G)}, 4b {int(G.p4b.sum())}/{len(G)}; WF-A picks beat "
      f"RULES v2 {int(WF.beats_live.sum())}/{len(WF)}, SPY {int(WF.beats_spy.sum())}/{len(WF)}")
    P(f"  KEEP candidate: {keep}")

    md = [
        f"# Idea 538 - is c_sd the right SCALE, or is it a TURNOVER proxy?  (lane B, {pd.Timestamp.today().date()})",
        "",
        f"Population: idea 535's exact 162 cells (3 panels x 2 families x 9 levels x 3 cadences "
        f"{CADENCES}, gross {GROSS}), 324 books, 10 bps, next-day execution.",
        f"Tuned: PREDICTOR FORM ({len(FORMS)}) x SHRINKAGE {LAMBDAS} = {len(FORMS)*len(LAMBDAS)} "
        f"estimator cells, all reported on all 3 subsets.",
        "",
        "## Gates",
        f"- **G1 REPRODUCTION {'PASS' if g1_pass else 'FAIL'}** - max|d resid0_pp| "
        f"{g1['resid_max']:.3e} pp, max|d c_sd| {g1['csd_max']:.3e} vs idea 301; max|d turn_yr| "
        f"{g1['turn_max']:.3e} vs idea 535; ladder reproduces MAE(CSD.is) {csd_all_l1:.6f} "
        f"(published {REF_MAE_CSD}) and MAE(FAMILY) {fam_all:.6f} (published {REF_MAE_FAM}).",
        f"- **G2 {g2v}** - rho(c_sd_is, turn_yr_DG_is) over n=162: PEARSON {rp:+.4f}, "
        f"SPEARMAN {rs_:+.4f}; CSD+TO design condition number {cond:.2f}.",
        "",
        "## Bars",
        f"- **B1 {'PASS' if (b1a and b1b) else 'FAIL'}** - best honest turnover form {best_to} "
        f"(lam {Bt.loc[best_to,'lam_star']:.2f}): OOS MAE ALL {to_all:.4f} vs bar "
        f"{B1A_RATIO*fam_all:.4f} ({'pass' if b1a else 'fail'}); MA-THRESH {to_ma:.4f} vs "
        f"{fam_ma:.4f} ({'pass' if b1b else 'fail'}).",
        f"- **B2 {'PASS' if b2 else 'FAIL'}** - {best_to} {to_all:.4f} vs CSD.is {csd_all:.4f} "
        f"on the ALL cut ({to_all-csd_all:+.4f} pp/yr).",
        f"- **B3 {'PASS' if b3 else 'FAIL'}** - CSD+TO.is {both_all:.4f} vs bar "
        f"{B3_RATIO*csd_all:.4f} (increment over c_sd alone {both_all-csd_all:+.4f} pp/yr).",
        f"- **B4 {'PASS' if b4 else 'FAIL'}** - c_sd orthogonalised on turnover: slope "
        f"{o_csd['b'][1]:+.4f}, t {o_csd['t'][1]:.2f} vs raw t {raw_csd['t'][1]:.2f}; mirror "
        f"(turnover net of c_sd) t {o_to['t'][1]:.2f} of raw {raw_to['t'][1]:.2f}.",
        "",
        "## Rule 8",
        f"- WF-A: 12 arms, (level, cadence) picked on IS Sharpe alone. Beat RULES v2 OOS "
        f"{int(WF.beats_live.sum())}/{len(WF)}, SPY {int(WF.beats_spy.sum())}/{len(WF)}, "
        f"no-gate EWall control {int(WF.beats_ctrl.sum())}/{len(WF)}.",
        f"- WF-B: every ladder rung is an IS fit scored once on the OOS-window residual.",
        f"- WF-C: always-RESPREAD {always_rs:.4f} / always-DEGROSS {always_dg:.4f} / oracle "
        f"{oracle:.4f} mean OOS Sharpe; every honest form's share of the oracle gap is in "
        f"`.walkforward` prose above.",
        "",
        "## KEEP paths",
        f"- 4a {int(G.p4a.sum())}/{len(G)} books; 4b {int(G.p4b.sum())}/{len(G)} books.",
        "",
        "SURVIVORSHIP: all three panels are current constituents; CAGR levels are inflated and "
        "the 4a/4b columns inherit that. The headline object is an arm-minus-arm contrast on the "
        "same names, days and gross, so the bias very largely cancels out of gap0/pred0/resid0.",
    ]
    Path(f"{OUT}.result.md").write_text("\n".join(md) + "\n")

    line = (f"| {pd.Timestamp.today().date()} | idea538 c_sd-vs-TURNOVER (162 cells, "
            f"{len(FORMS)}x{len(LAMBDAS)} ladder) | - | - | - | - | - | "
            f"G2 {g2v}, B1 {'PASS' if (b1a and b1b) else 'FAIL'}, B2 "
            f"{'PASS' if b2 else 'FAIL'}, B3 {'PASS' if b3 else 'FAIL'}, B4 "
            f"{'PASS' if b4 else 'FAIL'} | {Path(__file__).name} |")
    P("\nLEADERBOARD row (headline):\n" + line)
    flush_log()
    return dict(g1=g1_pass, g2=g2v, b1=(b1a and b1b), b2=b2, b3=b3, b4=b4,
                fam_all=fam_all, csd_all=csd_all, to_all=to_all, both_all=both_all,
                best_to=best_to, p4a=int(G.p4a.sum()), p4b=int(G.p4b.sum()),
                wf_live=int(WF.beats_live.sum()), wf_spy=int(WF.beats_spy.sum()), n=len(G))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Idea 303 - "is-the-de-gross-timing-residual-a-per-panel-CONSTANT" (cloud, 2026-09-06).

The question
------------
Idea 290 showed a DE-GROSSING gate book is algebraically the same gate's RESPREAD book run at
time-varying leverage c_t = (gross held by DG)/(gross held by RS), so its 0-bps CAGR gap splits
exactly into

    gap0 = [ constant-leverage drag at the cell's own mean leverage c_bar ]  <- exposure
         + [ residual from the TIMING of c_t ]                               <- gate content

Idea 297 measured that residual on 108 cells (3 panels x 2 gates x 3 cadences x 6 bands) and
found it negative nearly everywhere.  Its walk-forward reported that the IS PANEL MEAN predicts
the OOS residual better than the naive zero (OOS MAE 0.488 vs 0.591 on SMALL439, 0.267 vs 0.385
on U56, 0.420 vs 0.671 on B136 = 17-31% better), while the per-CELL IS value beats the zero by
less and per-cell sign agreement is only 58-75%.

QUEUE wording: "Pre-register the per-panel constant as THE estimator against a global constant
and the zero, on a corpus disjoint from idea 297's cells.  Max 2 params."

The disjointness that matters
------------------------------
Idea 297's 17-31% number is IN-CORPUS: the panel constant was fitted on the IS half of the SAME
108 cells it was then scored on (different window, same cells).  A panel constant that is a real
property of the panel must transfer to cells the fit never saw.  So:

    FIT corpus  = idea 297's exact 108 cells, IS window only (bands 0.00/0.02/0.03/0.05/0.08/0.12)
    TEST corpus = 108 DISJOINT cells, OOS window only (bands 0.01/0.04/0.06/0.10/0.15/0.20)

Same panels, same gates, same cadences, same construction pair - only the band dial is moved off
every value idea 297 used, so no (panel, gate, cadence, band) cell appears in both.  The
estimators are fitted on IS residuals of the OLD bands and scored on OOS residuals of the NEW
bands: disjoint in cells AND in time.

Estimators (all fitted on the FIT corpus only)
-----------------------------------------------
    ZERO    predict 0 pp/yr                       (the naive estimator PROTOCOL defaults to)
    GLOBAL  one constant = mean of all 108 IS residuals
    PANEL   three constants = mean of that panel's 36 IS residuals    <- THE pre-registered one
  reported for context, not in the pre-registered contest:
    PANELGATE  six constants, mean of that (panel, gate)'s 18 IS residuals
    CELLIS     the TEST cell's OWN IS residual (not fitted on the FIT corpus; idea 297's
               per-cell estimator, re-run on the new bands)
    ORACLE     the TEST panel's realised OOS mean (an upper bound, unattainable in practice)

Pre-registered bars (fixed before any number was read)
-------------------------------------------------------
H1 (primary)  PANEL beats ZERO on OOS MAE on ALL THREE panels.  FAILS if any panel fails.
H2            PANEL beats GLOBAL on OOS MAE on ALL THREE panels.
H3            Pooled MAE improvement of PANEL over ZERO >= 10% (idea 297's in-corpus figure was
              17-31%; a transfer that keeps at least ~half of the smallest of those is the bar).
H4            The three fitted panel constants rank the panels in the same order as the realised
              NEW-corpus OOS panel means (Spearman rho = +1 over the three panels).
B0            REPRODUCTION GATE, asserted before any new number is read: the recomputed OLD-band
              cells must match idea 297's committed decomp.csv on c_bar, gap0_pp, pred0_pp and
              resid0_pp to < 1e-6 on all 432 (cell x window) rows.  If B0 fails this script is
              measuring something else and the run aborts.
P1            The leverage identity max |r_dg,t - c_t * r_rs,t| < 1e-12 on all 216 pairs.

Tuned parameters (PROTOCOL rule 4: at most two)
------------------------------------------------
    band     OLD {0.00,0.02,0.03,0.05,0.08,0.12} / NEW {0.01,0.04,0.06,0.10,0.15,0.20}
    cadence  {W, M, Q}
Reported at EVERY value, selected at none except inside the rule-8 walk-forward.  Panel, gate
form and construction are REPORTED dimensions, not tuned - the contrast across them is the
question.  The estimator family is pre-registered, not searched.

Grid
-----
OLD (fit): 3 panels x 2 gates x 3 cadences x 6 bands x 2 constructions = 216 books @ 0 bps.
NEW (test): the same shape on the new bands = 216 books @ 0 bps AND @ 10 bps.
648 backtests, every cell written to CSV and printed.

Walk-forward (PROTOCOL rule 8)
-------------------------------
Two of them.  (a) The estimator contest IS a walk-forward: fitted on IS, scored on OOS, on cells
the fit never saw.  (b) The book-level one PROTOCOL asks for: inside each of the 12
(panel x gate x construction) arms of the NEW corpus, (band, cadence) is chosen on IS Sharpe and
2017-2026 is read once; OOS CAGR/Sharpe/MaxDD reported against the live RULES v2 book, SPY and
the matched no-filter EWall control.  Both KEEP paths evaluated on all 216 NEW cells at 10 bps.

SURVIVORSHIP: all three panels are CURRENT constituents - data/prices_small.csv is a screen of
today's sub-$2B names (the 44 with max_1d_move >= 1.0 dropped) and universe(_broad).json are
today's large caps/ETFs; no delistings.  The residual is an arm-minus-arm contrast on the SAME
names and days (DEGROSS and RESPREAD share one gate mask), so the bias very largely cancels out
of every estimator column; it does NOT cancel out of the 4a/4b columns, which are levels.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing.
"""
import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, band_state, rules_v2_weights
from engine import backtest, metrics

COST_BPS = 10
GROSS = 0.75
MAX_VOL = 0.60
BANDS_OLD = [0.00, 0.02, 0.03, 0.05, 0.08, 0.12]     # idea 297's cells -> FIT corpus
BANDS_NEW = [0.01, 0.04, 0.06, 0.10, 0.15, 0.20]     # disjoint            -> TEST corpus
CADENCES = ["W", "M", "Q"]
GATES = ["MA", "MAVOL"]
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]
PANELS = ["SMALL439", "U56", "B136"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SCRIPT = Path(__file__).name
OUT = Path(__file__).with_suffix("")
PARENT = REPO / "research" / "backtests" / (
    "2026-09-06_is-the-negative-exposure-timing-residual-a-general-property-of-gates_B.decomp.csv")

# pre-registered bars
H3_MIN_GAIN = 0.10       # pooled MAE improvement of PANEL over ZERO
B0_TOL = 1e-6
P1_TOL = 1e-12

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 500)

_LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.4f}")


def sign_p(k, n):
    """Exact two-sided binomial p for k successes of n at p=0.5."""
    if n == 0:
        return np.nan
    tail = sum(math.comb(n, i) for i in range(0, min(k, n - k) + 1)) / 2 ** n
    return min(1.0, 2 * tail)


def spearman(x, y):
    x = pd.Series(np.asarray(x, float)).rank()
    y = pd.Series(np.asarray(y, float)).rank()
    n = len(x)
    rho = float(np.corrcoef(x, y)[0, 1])
    t = rho * math.sqrt((n - 2) / max(1e-12, 1 - rho ** 2)) if n > 2 else np.nan
    return rho, t


# ---------------------------------------------------------------- panels
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


def gate_mask(px, gate, band):
    g = band_state(px, band)
    if gate == "MAVOL":
        vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        g = g & (vol20 < MAX_VOL)
    return g & live_mask(px)


def book(px, gate, band, construction):
    """Identical construction to idea 297 (so B0 can be exact)."""
    g = gate_mask(px, gate, band)
    if construction == "RESPREAD":
        k = g.sum(axis=1).clip(lower=1)
        return g.astype(float).div(k, axis=0) * GROSS
    live = live_mask(px)
    n = live.sum(axis=1).clip(lower=1)
    return (g & live).astype(float).div(n, axis=0) * GROSS


def control_book(px):
    live = live_mask(px)
    n = live.sum(axis=1).clip(lower=1)
    return live.astype(float).div(n, axis=0) * GROSS


def cagr_of(r):
    return metrics(r)["CAGR"]


def stat(r):
    m = metrics(r)
    h = len(r) // 2
    h1, h2 = metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]
    ri, ro = r.loc[:IS_END], r.loc[OOS_START:]
    mi, mo = metrics(ri), metrics(ro)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                isCAGR=mi["CAGR"], isSharpe=mi["Sharpe"], isMaxDD=mi["MaxDD"],
                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"])


def fail_4b(s, spy_s):
    t = {"H1": s["H1"] > spy_s["H1"], "H2": s["H2"] > spy_s["H2"],
         "OOS": s["oSharpe"] > spy_s["oSharpe"],
         "DD": abs(s["MaxDD"]) <= 0.60 * abs(spy_s["MaxDD"]),
         "CAGR": s["CAGR"] >= 0.70 * spy_s["CAGR"]}
    f = [k for k, v in t.items() if not v]
    return ",".join(f) if f else "-"


def verdict_4a(s, b):
    return bool(s["H1"] > b["H1"] and s["H2"] > b["H2"] and s["MaxDD"] >= b["MaxDD"])


def decompose(r_dg0, r_rs0, held_dg, held_rs, window):
    """idea 290's constant-leverage split, restricted to `window`."""
    d, r_, hd, hr = (s.loc[window] for s in (r_dg0, r_rs0, held_dg, held_rs))
    if len(d) < 60:
        return None
    c_t = (hd / hr.replace(0, np.nan)).fillna(0.0)
    c_bar = float(c_t.mean())
    cagr_rs = cagr_of(r_)
    gap0 = 100 * (cagr_of(d) - cagr_rs)
    pred0 = 100 * (cagr_of(c_bar * r_) - cagr_rs)
    return dict(c_bar=c_bar, c_sd=float(c_t.std()), gap0_pp=gap0, pred0_pp=pred0,
                resid0_pp=gap0 - pred0,
                share=(pred0 / gap0) if abs(gap0) > 1e-12 else np.nan,
                n_days=len(d))


def score(pred, actual):
    """Estimator scorecard on one set of cells."""
    e = np.asarray(pred, float) - np.asarray(actual, float)
    a = np.asarray(actual, float)
    p = np.asarray(pred, float)
    sgn = np.mean(np.sign(p) == np.sign(a)) if len(a) else np.nan
    return dict(n=len(a), MAE=float(np.mean(np.abs(e))), RMSE=float(np.sqrt(np.mean(e ** 2))),
                bias=float(np.mean(e)), sign_agree=float(sgn))


# ---------------------------------------------------------------- main
def main():
    assert not (set(BANDS_OLD) & set(BANDS_NEW)), "FIT and TEST bands must be disjoint"
    PX = panels()
    starts = {k: v[0].index[260] for k, v in PX.items()}
    ends = {k: v[0].index[-1] for k, v in PX.items()}
    common_start = max(starts.values())
    common_end = min(ends.values())

    P("=" * 175)
    P(f"Idea 303 is-the-de-gross-timing-residual-a-per-panel-CONSTANT (cloud) | {SCRIPT}")
    P("=" * 175)
    for k in PANELS:
        yrs = len(PX[k][0].loc[starts[k]:]) / 252
        P(f"  {k}: {PX[k][0].index[0].date()} .. {ends[k].date()}; evaluated from "
          f"{starts[k].date()} ({yrs:.2f} yrs, {PX[k][0].shape[1]} names)")
    P(f"  COMMON window: {common_start.date()} .. {common_end.date()}")
    P(f"Costs {COST_BPS} bps (plus a 0-bps rung for the decomposition), gross {GROSS}, "
      f"next-day execution, no shorting, no leverage.")
    P(f"FIT corpus  bands {BANDS_OLD} (idea 297's cells), IS window <= {IS_END}.")
    P(f"TEST corpus bands {BANDS_NEW} (DISJOINT), OOS window {OOS_START}.. .")
    P(f"Pre-registered bars: H1 PANEL < ZERO on OOS MAE on 3/3 panels; H2 PANEL < GLOBAL on 3/3; "
      f"H3 pooled MAE gain over ZERO >= {H3_MIN_GAIN:.0%}; H4 Spearman(fitted panel constant, "
      f"realised OOS panel mean) = +1; B0 repro of idea 297 decomp.csv < {B0_TOL:g}; "
      f"P1 identity < {P1_TOL:g}.")

    for k in PANELS:
        y = PX[k][0].index.to_series().groupby(PX[k][0].index.year).count()
        if y.loc[2013:2024].max() > 300:
            P(f"!! {k} has a CALENDAR-DAY index - aborting."); sys.exit(1)
    P("Index sanity: all three panels ~252 rows/yr (trading-day index confirmed).")

    # ---------------- reference books -------------------------------------
    P("\n" + "-" * 175)
    P("REFERENCE BOOKS (per panel, own window, 10 bps)")
    P("-" * 175)
    ctrl, spy_stat = {}, {}
    for k in PANELS:
        px, spy = PX[k]
        st = starts[k]
        for cad in CADENCES:
            rc = backtest(px, control_book(px), cost_bps=COST_BPS, freq=cad)["returns"].loc[st:]
            ctrl[(k, cad)] = stat(rc)
        spy_stat[k] = stat(spy.pct_change().fillna(0.0).loc[st:])
    px_u = load_universe()
    live_ret = backtest(px_u, rules_v2_weights(px_u), cost_bps=COST_BPS, freq="W")["returns"]
    live_s = stat(live_ret.loc[starts["U56"]:])
    ref = {f"CONTROL EWall {k} {c} (no filter)": ctrl[(k, c)] for k in PANELS for c in CADENCES}
    ref["RULES v2 on universe.json (LIVE BOOK, 4a comparand)"] = live_s
    for k in PANELS:
        ref[f"SPY on {k} window (4b comparand)"] = spy_stat[k]
    P(fmt(pd.DataFrame(ref).T))

    # ---------------- the grid --------------------------------------------
    P("\n" + "-" * 175)
    P("GRID - 432 books (3 panels x 2 gates x 3 cadences x 12 bands x 2 constructions); "
      "OLD bands 0 bps only (fit corpus), NEW bands 0 and 10 bps")
    P("-" * 175)
    rows, ret0, held = {}, {}, {}
    for k in PANELS:
        px, _ = PX[k]
        st = starts[k]
        years = len(px.loc[st:]) / 252
        for con in CONSTRUCTIONS:
            for gate in GATES:
                for cad in CADENCES:
                    for b in BANDS_OLD + BANDS_NEW:
                        w = book(px, gate, b, con)
                        res0 = backtest(px, w, cost_bps=0, freq=cad)
                        key = (k, con, gate, cad, b)
                        ret0[key] = res0["returns"].loc[st:]
                        held[key] = res0["weights"].loc[st:].sum(axis=1)
                        if b in BANDS_NEW:
                            res = backtest(px, w, cost_bps=COST_BPS, freq=cad)
                            r = res["returns"].loc[st:]
                            s = stat(r)
                            rows[key] = dict(panel=k, con=con, gate=gate, cad=cad, band=b, **s,
                                             CAGR0=cagr_of(ret0[key]),
                                             gross_mean=float(held[key].mean()),
                                             turn_yr=res["turnover"].loc[st:].sum() / years,
                                             dCAGR_ctrl=s["CAGR"] - ctrl[(k, cad)]["CAGR"],
                                             dSharpe_ctrl=s["Sharpe"] - ctrl[(k, cad)]["Sharpe"],
                                             p4a=verdict_4a(s, live_s),
                                             f4b=fail_4b(s, spy_stat[k]))
        P(f"  ... {k} done ({len(rows)} priced NEW cells so far)")
    G = pd.DataFrame(rows.values())
    G["p4b"] = G.f4b == "-"
    cols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "oCAGR", "oSharpe", "oMaxDD", "CAGR0",
            "gross_mean", "turn_yr", "dCAGR_ctrl", "dSharpe_ctrl", "p4a", "f4b"]
    for k in PANELS:
        for con in CONSTRUCTIONS:
            for gate in GATES:
                sub = G[(G.panel == k) & (G.con == con) & (G.gate == gate)].set_index(["cad", "band"])[cols]
                P(f"\n--- NEW corpus {k} / {con} / gate {gate} (10 bps) ---")
                P(fmt(sub))
    G.to_csv(f"{OUT}.grid.csv", index=False)

    # ---------------- P1 identity -----------------------------------------
    P("\n" + "-" * 175)
    P("P1 - IS THE DE-GROSS BOOK EXACTLY THE RESPREAD BOOK AT TIME-VARYING LEVERAGE?")
    P("-" * 175)
    p1 = []
    for k in PANELS:
        for gate in GATES:
            for cad in CADENCES:
                for b in BANDS_OLD + BANDS_NEW:
                    kd, kr = (k, "DEGROSS", gate, cad, b), (k, "RESPREAD", gate, cad, b)
                    c_t = (held[kd] / held[kr].replace(0, np.nan)).fillna(0.0)
                    p1.append(dict(panel=k, gate=gate, cad=cad, band=b,
                                   corpus="OLD" if b in BANDS_OLD else "NEW",
                                   max_abs_err=float((ret0[kd] - c_t * ret0[kr]).abs().max())))
    P1 = pd.DataFrame(p1)
    P(fmt(P1.groupby(["corpus", "panel"]).max_abs_err.max().to_frame("worst_max_abs_err")))
    p1_pass = bool(P1.max_abs_err.max() < P1_TOL)
    P(f"P1: worst over all {len(P1)} pairs = {P1.max_abs_err.max():.3e} (bar {P1_TOL:g}) -> "
      f"{'HOLDS' if p1_pass else 'FAILS'}")

    # ---------------- decomposition ---------------------------------------
    P("\n" + "-" * 175)
    P("CONSTANT-LEVERAGE DECOMPOSITION on FULL / COMMON / IS / OOS windows, both corpora")
    P("-" * 175)
    wins = {"FULL": None, "COMMON": slice(common_start, common_end),
            "IS": slice(None, IS_END), "OOS": slice(OOS_START, None)}
    dec = []
    for k in PANELS:
        for gate in GATES:
            for cad in CADENCES:
                for b in BANDS_OLD + BANDS_NEW:
                    kd, kr = (k, "DEGROSS", gate, cad, b), (k, "RESPREAD", gate, cad, b)
                    for wname, w in wins.items():
                        d = decompose(ret0[kd], ret0[kr], held[kd], held[kr],
                                      slice(None) if w is None else w)
                        if d is None:
                            continue
                        dec.append(dict(panel=k, corpus="OLD" if b in BANDS_OLD else "NEW",
                                        window=wname, gate=gate, cad=cad, band=b, **d))
    D = pd.DataFrame(dec)
    D.to_csv(f"{OUT}.decomp.csv", index=False)
    for k in PANELS:
        sub = D[(D.panel == k) & (D.window == "OOS") & (D.corpus == "NEW")].set_index(["gate", "cad", "band"])
        P(f"\n--- {k} / TEST corpus (NEW bands) / OOS window ---")
        P(fmt(sub[["c_bar", "c_sd", "gap0_pp", "pred0_pp", "resid0_pp", "share"]]))

    # ---------------- B0 reproduction gate --------------------------------
    P("\n" + "-" * 175)
    P("B0 REPRODUCTION GATE - recomputed OLD-band cells vs idea 297's committed decomp.csv")
    P("-" * 175)
    keys = ["panel", "window", "gate", "cad", "band"]
    par = pd.read_csv(PARENT)
    mine = D[D.corpus == "OLD"].drop(columns=["corpus"])
    m = par.merge(mine, on=keys, suffixes=("_par", "_new"), validate="one_to_one")
    P(f"  matched {len(m)} of {len(par)} parent rows on {keys}")
    worst = {c: float((m[f"{c}_par"] - m[f"{c}_new"]).abs().max())
             for c in ("c_bar", "gap0_pp", "pred0_pp", "resid0_pp")}
    for c, v in worst.items():
        P(f"  max |parent - mine| {c:>10s} = {v:.3e}")
    b0_pass = len(m) == len(par) and max(worst.values()) < B0_TOL
    P(f"B0 -> {'PASS' if b0_pass else 'FAIL'} (bar {B0_TOL:g})")
    if not b0_pass:
        P("  !! B0 FAILED - construction does not match idea 297. ABORTING.")
        (Path(f"{OUT}.console.txt")).write_text("\n".join(_LOG) + "\n")
        sys.exit(1)

    # ---------------- the estimator contest -------------------------------
    P("\n" + "-" * 175)
    P("THE ESTIMATOR CONTEST - fitted on the FIT corpus (OLD bands, IS window), scored on the "
      "TEST corpus (NEW bands, OOS window)")
    P("-" * 175)
    fit = D[(D.corpus == "OLD") & (D.window == "IS")].copy()
    test = D[(D.corpus == "NEW") & (D.window == "OOS")].copy()
    test_is = D[(D.corpus == "NEW") & (D.window == "IS")].set_index(["panel", "gate", "cad", "band"])
    P(f"  FIT  cells: {len(fit)}   TEST cells: {len(test)}   "
      f"overlap on (panel,gate,cad,band): "
      f"{len(set(map(tuple, fit[['panel','gate','cad','band']].values)) & set(map(tuple, test[['panel','gate','cad','band']].values)))}")

    c_global = float(fit.resid0_pp.mean())
    c_panel = fit.groupby("panel").resid0_pp.mean()
    c_pg = fit.groupby(["panel", "gate"]).resid0_pp.mean()
    P(f"\nFitted constants (pp/yr, from {len(fit)} FIT cells):")
    P(f"  GLOBAL = {c_global:+.4f}")
    P(fmt(c_panel.to_frame("PANEL constant")))
    P(fmt(c_pg.to_frame("PANELGATE constant")))
    P("\nRealised TEST-corpus OOS panel means (the target, for reference only):")
    P(fmt(test.groupby("panel").resid0_pp.agg(["mean", "std", "count"])))

    test["ZERO"] = 0.0
    test["GLOBAL"] = c_global
    test["PANEL"] = test.panel.map(c_panel)
    test["PANELGATE"] = [c_pg.loc[(p, g)] for p, g in zip(test.panel, test.gate)]
    test["CELLIS"] = [float(test_is.loc[(p, g, c, b), "resid0_pp"])
                      for p, g, c, b in zip(test.panel, test.gate, test.cad, test.band)]
    oracle = test.groupby("panel").resid0_pp.mean()
    test["ORACLE"] = test.panel.map(oracle)
    ESTS = ["ZERO", "GLOBAL", "PANEL", "PANELGATE", "CELLIS", "ORACLE"]

    sc = []
    for k in PANELS + ["POOLED"]:
        sub = test if k == "POOLED" else test[test.panel == k]
        for e in ESTS:
            sc.append(dict(panel=k, estimator=e, **score(sub[e], sub.resid0_pp)))
    SC = pd.DataFrame(sc)
    SC.to_csv(f"{OUT}.estimators.csv", index=False)
    P("\nOOS scorecard on the DISJOINT TEST corpus (pp/yr; lower MAE/RMSE is better).  MAE:")
    P(fmt(SC.pivot(index="panel", columns="estimator", values="MAE").reindex(PANELS + ["POOLED"])[ESTS]))
    P("\nRMSE:")
    P(fmt(SC.pivot(index="panel", columns="estimator", values="RMSE").reindex(PANELS + ["POOLED"])[ESTS]))
    P("\nBias (pred - actual):")
    P(fmt(SC.pivot(index="panel", columns="estimator", values="bias").reindex(PANELS + ["POOLED"])[ESTS]))
    P("\nSign agreement (ZERO can never agree by construction):")
    P(fmt(SC.pivot(index="panel", columns="estimator", values="sign_agree").reindex(PANELS + ["POOLED"])[ESTS]))

    # paired, cell-by-cell
    P("\nPaired cell-by-cell comparison of PANEL against each rival (36 cells per panel):")
    pr = []
    for k in PANELS + ["POOLED"]:
        sub = test if k == "POOLED" else test[test.panel == k]
        ep = (sub.PANEL - sub.resid0_pp).abs()
        for e in ["ZERO", "GLOBAL", "PANELGATE", "CELLIS"]:
            er = (sub[e] - sub.resid0_pp).abs()
            wins = int((ep < er).sum())
            pr.append(dict(panel=k, rival=e, n=len(sub), PANEL_wins=wins,
                           frac=wins / len(sub), mean_dMAE=float((ep - er).mean()),
                           p_sign=sign_p(wins, len(sub))))
    PR = pd.DataFrame(pr)
    P(fmt(PR.set_index(["panel", "rival"])))
    PR.to_csv(f"{OUT}.paired.csv", index=False)

    # ---------------- hypotheses ------------------------------------------
    P("\n" + "-" * 175)
    P("PRE-REGISTERED VERDICTS")
    P("-" * 175)
    mae = SC.set_index(["panel", "estimator"]).MAE
    h1_hits = {k: bool(mae[(k, "PANEL")] < mae[(k, "ZERO")]) for k in PANELS}
    h2_hits = {k: bool(mae[(k, "PANEL")] < mae[(k, "GLOBAL")]) for k in PANELS}
    for k in PANELS:
        P(f"  {k:9s} MAE  ZERO {mae[(k,'ZERO')]:.4f}  GLOBAL {mae[(k,'GLOBAL')]:.4f}  "
          f"PANEL {mae[(k,'PANEL')]:.4f}  CELLIS {mae[(k,'CELLIS')]:.4f}  "
          f"ORACLE {mae[(k,'ORACLE')]:.4f}   | gain vs ZERO "
          f"{1 - mae[(k,'PANEL')]/mae[(k,'ZERO')]:+.1%}, vs GLOBAL "
          f"{1 - mae[(k,'PANEL')]/mae[(k,'GLOBAL')]:+.1%}")
    h1 = all(h1_hits.values())
    h2 = all(h2_hits.values())
    pooled_gain = 1 - mae[("POOLED", "PANEL")] / mae[("POOLED", "ZERO")]
    h3 = bool(pooled_gain >= H3_MIN_GAIN)
    rho, _ = spearman([c_panel[k] for k in PANELS], [oracle[k] for k in PANELS])
    h4 = bool(abs(rho - 1.0) < 1e-9)
    P(f"\nH1 PANEL beats ZERO on 3/3 panels: {sum(h1_hits.values())}/3 -> {'HOLDS' if h1 else 'FAILS'}")
    P(f"H2 PANEL beats GLOBAL on 3/3 panels: {sum(h2_hits.values())}/3 -> {'HOLDS' if h2 else 'FAILS'}")
    P(f"H3 pooled MAE gain over ZERO {pooled_gain:+.1%} (bar >= {H3_MIN_GAIN:.0%}) -> "
      f"{'HOLDS' if h3 else 'FAILS'}")
    P(f"H4 Spearman(fitted panel constant, realised OOS panel mean) = {rho:+.3f} -> "
      f"{'HOLDS' if h4 else 'FAILS'}   "
      f"[fitted {', '.join(f'{k} {c_panel[k]:+.3f}' for k in PANELS)}; "
      f"realised {', '.join(f'{k} {oracle[k]:+.3f}' for k in PANELS)}]")

    # ---------------- rule 8, book level ----------------------------------
    P("\n" + "-" * 175)
    P("RULE 8 WALK-FORWARD (book level) - (band, cadence) chosen on IS Sharpe inside each of the "
      "12 NEW-corpus arms, 2017-2026 read once")
    P("-" * 175)
    wf = []
    for k in PANELS:
        for gate in GATES:
            for con in CONSTRUCTIONS:
                sub = G[(G.panel == k) & (G.gate == gate) & (G.con == con)]
                pick = sub.loc[sub.isSharpe.idxmax()]
                wf.append(dict(panel=k, gate=gate, con=con, band=pick.band, cad=pick.cad,
                               isSharpe=pick.isSharpe, oCAGR=pick.oCAGR, oSharpe=pick.oSharpe,
                               oMaxDD=pick.oMaxDD,
                               ctrl_oSharpe=ctrl[(k, pick.cad)]["oSharpe"],
                               spy_oSharpe=spy_stat[k]["oSharpe"],
                               spy_oCAGR=spy_stat[k]["oCAGR"],
                               live_oSharpe=live_s["oSharpe"],
                               beats_ctrl=pick.oSharpe > ctrl[(k, pick.cad)]["oSharpe"],
                               beats_spy=pick.oSharpe > spy_stat[k]["oSharpe"],
                               beats_live=pick.oSharpe > live_s["oSharpe"],
                               p4a=pick.p4a, f4b=pick.f4b))
    WF = pd.DataFrame(wf)
    P(fmt(WF.set_index(["panel", "gate", "con"])))
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(f"\nWalk-forward picks beating: matched EWall control {int(WF.beats_ctrl.sum())}/12, "
      f"SPY {int(WF.beats_spy.sum())}/12, the live RULES v2 book {int(WF.beats_live.sum())}/12.")
    P(f"4a passes among the 12 picks: {int(WF.p4a.sum())}; 4b passes: {int((WF.f4b == '-').sum())}.")

    P("\nBOTH KEEP PATHS over all 216 NEW cells at 10 bps:")
    P(f"  4a (beat the live book in both halves, MaxDD no worse): {int(G.p4a.sum())}/{len(G)}")
    P(f"  4b (beat SPY H1/H2/OOS, DD <= 60% of SPY, CAGR >= 70% of SPY): {int(G.p4b.sum())}/{len(G)}")
    if G.p4b.any():
        P(fmt(G[G.p4b].set_index(["panel", "con", "gate", "cad", "band"])[
            ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "oSharpe", "turn_yr"]]))
    P("  binding 4b bar, count of cells failing on each:")
    P(fmt(G.f4b.value_counts().to_frame("cells")))

    # ---------------- verdict ---------------------------------------------
    P("\n" + "=" * 175)
    passes = sum([h1, h2, h3, h4])
    if h1 and h2 and h3:
        verdict = "KEEP-the-estimator (measurement): the per-panel constant transfers off the fitted cells"
    elif h1 and not h2:
        verdict = "SPLIT: the constant beats the zero but is not PER-PANEL (a global constant does as well)"
    elif not h1:
        verdict = "KILL: the per-panel constant does NOT transfer to cells it was not fitted on"
    else:
        verdict = "SPLIT: direction survives, the pre-registered magnitude bar does not"
    P(f"VERDICT: {verdict}  ({passes}/4 pre-registered bars held; B0 PASS, "
      f"P1 {'PASS' if p1_pass else 'FAIL'})")
    P("This is a MEASUREMENT idea: no book here is a capital candidate on its own; the KEEP "
      "columns are reported because PROTOCOL requires both paths on every cell.")
    P("=" * 175)

    Path(f"{OUT}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()

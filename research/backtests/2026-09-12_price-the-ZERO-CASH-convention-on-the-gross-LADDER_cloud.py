#!/usr/bin/env python3
"""Idea 576 (cloud, 2026-09-12) - price-the-ZERO-CASH-convention-on-the-gross-LADDER.

QUESTION
--------
Idea 311 swept the gross scalar g over 6 unlevered book-forms x 3 panels x 2 cadences x 17 grosses
(612 books) and found Sharpe very nearly invariant in g - but not exactly: it drifts **+0.0065 per
unit of g**, small, systematic and POSITIVE across all 36 cells.  That is precisely the signature of
the engine's convention that the un-invested fraction (1 - g) earns **zero**: a book at g = 0.20
parks 80% of NAV in a 0% asset, so its excess return per unit of risk is dragged down, and the drag
shrinks as g rises.

Idea 406 asked the matching question from the other side (what is the de-grossed cash leg worth?)
and was PARKed on the instrument.  This run prices the CONVENTION itself.  It re-runs idea 311's
exact 612-book ladder with the idle fraction credited at 0 (idea 311's convention, the anchor),
150 bps and 300 bps per annum, and reports:

    1. whether the +0.0065/unit-g Sharpe slope FLATTENS as the cash is paid for;
    2. whether any admissible 4b gross BAND widens once cash earns;
    3. whether the PANEL ORDERING of band widths (U56 vs B136 vs the small panel) survives.

MECHANICS - how the cash is credited
    The idle fraction is made an EXPLICIT held column: weights are augmented with
    w_cash = 1 - sum(w_risky), priced off a synthetic index compounding at the flat annual rate
    over trading days, and the whole book is then run through the SAME drift / renormalisation /
    turnover machinery.  Turnover (and therefore cost) is charged on the RISKY legs only, exactly as
    idea 311 charged it, so the only thing that changes between rungs is what the idle money earns.
    At rate 0 this is algebraically idea 311's runner, and G2 asserts that to 1e-12.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two - the queue's own: cash rate, gross)
    1. CASH  in {0, 150, 300} bps/yr   (0 = idea 311's convention, the anchor; 150/300 = the queue's)
    2. g     in {0.20, 0.25, ..., 1.00} - idea 311's 17-point ladder, unlevered, NOT re-tuned
All 3 x 17 = 51 tuned points are reported, at every (panel, form, cadence).  REPORTED-NEVER-SELECTED
axes: panel (U56, B136, small), book-form (EWall control + 5 treatments), cadence (W, M), window
(FULL, IS, OOS).  Nothing is picked on any of them.

PRE-REGISTERED HYPOTHESES (written before any credited number was read)
    H_REPRO : at CASH=0 this run reproduces idea 311's committed `.grid.csv` rows on U56 and B136
              inside idea 630's STANDING reproduction tolerance (tol_X(k) = a*k^b on elapsed days
              k; here k = 3 days between idea 311's run and this one).  Both runs pin the sample
              end at 2026-09-04, so any residual drift is a PRICE RESTATEMENT (re-fetched adjusted
              closes), not a moving window - which is why a 1e-9 bar is the wrong instrument and
              idea 630's is the right one.  The small panel has grown from 439 to 663 tradable
              names since idea 311 ran, so its rows CANNOT reproduce and are reported as a
              different panel, not a failed reproduction.
    H_FLAT  : the drag reading.  The median Sharpe slope in g falls MONOTONICALLY as the cash rate
              rises, and at 300 bps its magnitude is smaller than at 0 bps (i.e. paying for the idle
              money removes the drift the record attributed to it).
    H_KILL  : the strong form - at some rate at or below 300 bps the median slope reaches zero or
              changes sign, i.e. the whole +0.0065 is the zero-cash convention and nothing else.
    H_WIDEN : crediting cash WIDENS admissible 4b bands (it lifts CAGR most at low g, where the CAGR
              floor is what binds), so the count of (panel, form, cadence) cells whose band widens
              exceeds the count that narrows, at both 150 and 300 bps.
    H_ORDER : the PANEL ORDERING of mean band width is invariant to the cash rate - whatever the
              ordering of U56 / B136 / small is at 0 bps, it is the same at 150 and at 300.
    H_NOFREE: the honest control - crediting cash does NOT create a KEEP.  The count of books
              passing PROTOCOL 4b at 150/300 bps against a SPY comparand that is FULLY INVESTED
              (and therefore earns no such credit) is reported beside the 4a count against a
              RULES v2 comparand credited at the SAME rate.  A 4b pass bought only by the credit is
              an artefact of an asymmetric comparand and is named as one.

GATES (run and printed BEFORE any new number is read)
    G1 identity : fast_backtest (cash=0) vs engine.backtest on one real book per panel.   bar 1e-12
    G2 cash-0   : the cash-crediting runner at rate 0 vs the plain runner, every panel.    bar 1e-12
    G3 credit   : the credited runner checked against an INDEPENDENT day-by-day reimplementation
                  (engine.backtest's own loop with the idle fraction earning the rate), at every
                  rate, on a real book.                                                   bar 1e-12
    G4 repro    : idea 311's committed grid rows at CASH=0 (see H_REPRO).

RULE 8 WALK-FORWARD (required)
    IS = start..2016-12-31, OOS = 2017-01-01..end, OOS read ONCE.
    WF-A: the 4b band is solved on the IS window alone at every cash rate, g* = the IS band midpoint,
          and the OOS band is read once - reporting whether g* is inside it, at every rate.  This is
          idea 311's own walk-forward, re-run on each rung, so "does the credit make the band
          transportable" is answered and not assumed.
    WF-B: a BOOK.  Form picked by IS Sharpe, g picked as the IS band midpoint, on B136/W as idea 311
          did, at each cash rate; OOS CAGR / Sharpe / MaxDD read ONCE against RULES v2 (credited at
          the same rate) and against SPY (buy-and-hold, uncredited - it holds no cash).

KEEP PATHS 4a and 4b are evaluated for EVERY book at EVERY rate and the counts reported.

THE CAVEAT, STATED BEFORE THE RESULT: a FLAT 150 / 300 bps over 2009-2026 is not the cash rate that
    existed.  T-bills paid roughly 10 bps to 2015 and roughly 500 bps after 2022, so a flat credit
    back-loads too little onto the IS window and too much onto nothing - it is a SENSITIVITY
    instrument for the convention, not a return forecast, and idea 642 has the real-instrument
    version (SHY) open.  Any band widening it buys is concentrated in the LOW-g books that hold the
    most idle cash, which are exactly the books the record least wants to certify.

SURVIVORSHIP: B136 and the small panel are CURRENT constituents (universe_broad.json is today's
    list; the small panel is today's sub-$2B screen with every max_1d_move >= 1.0 ticker dropped
    first, per PROTOCOL).  Dead names are absent, so every panel return here is biased UPWARD.

PROTOCOL: 10 bps per unit turnover on the risky legs, weights at close t applied t+1 (engine
convention), no shorting, no leverage (g <= 1.00).  Deterministic, standalone, no network.
Reads research/baseline.py and idea 311's committed grid; modifies nothing but its own outputs:
    .grid.csv .bands.csv .slopes.csv .order.csv .walkforward.csv .keeppaths.csv .console.txt
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score  # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STAMP = Path(__file__).name[:-3]
OUT = Path(__file__).resolve().parent

COST = 10.0
MA_WIN = 200
IS_END, OOS_START = "2016-12-31", "2017-01-01"
CADENCE = ["W", "M"]
GGRID = [round(0.20 + 0.05 * i, 2) for i in range(17)]      # idea 311's ladder, unlevered
CASH_BPS = [0.0, 150.0, 300.0]                              # TUNED 1 (0 = idea 311's convention)
CASH_ANCHOR = 0.0
FORMS = ["EWall", "MA-RS", "MA-DG", "TOP20", "TOP10", "MA20"]
CONTROL = "EWall"
LEGS = ("H1", "H2", "OOS", "DD", "CAGR")
SHARPE_LEGS = ("H1", "H2", "OOS")
PARENT311 = OUT / "2026-09-09_does-4b-discriminate-ANYTHING-on-gross-scalar-books_cloud.grid.csv"
PARENT_END = "2026-09-04"
SLOPE311 = 0.0065           # idea 311's committed Sharpe slope in g at the zero-cash convention
TOL = 1e-12
ELAPSED_K = 3               # days between idea 311's run (2026-09-09) and this one (2026-09-12)
# idea 630's standing reproduction tolerance, tol_X(k) = a * k ** b
TOL630 = {"Sharpe": (8.94e-03, 0.50), "H1": (9.14e-03, 0.57), "H2": (1.81e-02, 0.55),
          "OOS_Sharpe": (2.35e-02, 0.47), "IS_Sharpe": (8.94e-03, 0.50),
          "CAGR": (1.70e-03, 0.45), "IS_CAGR": (1.70e-03, 0.45), "OOS_CAGR": (1.70e-03, 0.45),
          "MaxDD": (1.70e-03, 0.45), "OOS_MaxDD": (1.70e-03, 0.45)}


def tol630(col, k=ELAPSED_K):
    a, b = TOL630[col]
    return a * k ** b

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


# ------------------------------------------------------------------ runners
def fast_backtest(prices, weights, cost_bps=COST, freq="W"):
    """Idea 311/312/568's vectorised runner, verbatim.  The idle fraction earns ZERO."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mask)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return {"returns": pd.Series(port, index=idx), "turnover": pd.Series(turn, index=idx)}


def cash_backtest(prices, weights, cash_bps=0.0, cost_bps=COST, freq="W"):
    """The same runner with the idle fraction held as an EXPLICIT asset earning `cash_bps`/yr.

    The cash column joins the drift and renormalisation exactly like any other holding; turnover
    (and therefore cost) is charged on the RISKY legs only, as idea 311 charges it.  At cash_bps = 0
    this is algebraically identical to fast_backtest - asserted in G2."""
    idx = prices.index
    rets_r = prices.pct_change().fillna(0.0).values
    wt_r = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    cash_daily = (1.0 + cash_bps / 1e4) ** (1.0 / 252.0) - 1.0
    T, N = rets_r.shape
    rets = np.hstack([rets_r, np.full((T, 1), cash_daily)])
    wt = np.hstack([wt_r, np.clip(1.0 - wt_r.sum(axis=1, keepdims=True), 0.0, None)])
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N + 1)), C[:-1]])
    reb = np.flatnonzero(mask)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1)
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1)
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb, :N] - heldp[reb, :N]).sum(axis=1)
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return {"returns": pd.Series(port, index=idx), "turnover": pd.Series(turn, index=idx),
            "cash_weight": pd.Series(held[:, N], index=idx)}


# ------------------------------------------------------------------------- helpers
def slow_cash_backtest(prices, weights, cash_bps=0.0, cost_bps=COST, freq="W"):
    """engine.backtest's own day-by-day loop, with the idle fraction earning `cash_bps`/yr.
    Written independently of cash_backtest and used only as gate G3."""
    rets = prices.pct_change().fillna(0.0)
    w_target = weights.reindex(prices.index).fillna(0.0).shift(1)
    mask = rebalance_mask(prices.index, freq).shift(1, fill_value=False)
    cd = (1.0 + cash_bps / 1e4) ** (1.0 / 252.0) - 1.0
    held = np.zeros((len(prices.index), prices.shape[1]))
    cash_w = np.zeros(len(prices.index))
    cur = np.zeros(prices.shape[1])
    cur_c = 1.0
    turnover = np.zeros(len(prices.index))
    for i in range(len(prices.index)):
        if mask.iloc[i] or i == 0:
            new = np.nan_to_num(w_target.iloc[i].values)
            turnover[i] = np.abs(new - cur).sum()
            cur = new
            cur_c = max(1.0 - cur.sum(), 0.0)
        held[i] = cur
        cash_w[i] = cur_c
        growth = cur * (1 + rets.iloc[i].values)
        growth_c = cur_c * (1 + cd)
        tot = growth.sum() + growth_c
        if tot > 0:
            cur = growth / tot
            cur_c = growth_c / tot
    port = (held * rets.values).sum(axis=1) + cash_w * cd - turnover * cost_bps / 1e4
    return {"returns": pd.Series(port, index=prices.index),
            "turnover": pd.Series(turnover, index=prices.index)}


def _priced(px, tradable):
    e = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    cols = [c for c in px.columns if c in tradable]
    e[cols] = px[cols].notna().astype(float)
    return e


def _ew(mask, g):
    n = mask.sum(axis=1).replace(0, np.nan)
    return g * mask.div(n, axis=0).fillna(0.0)


def above_ma(px, win=MA_WIN):
    return px > px.rolling(win).mean()


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def rowify(r, tn=None):
    m = metrics(r)
    h1, h2 = halves(r)
    mi, mo = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    d = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
             IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
             OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])
    if tn is not None:
        d["turnover"] = float(tn.sum() / m["Years"])
    return d


def keep_4a(r, b):
    a1, a2 = halves(r)
    b1, b2 = halves(b)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(b)["MaxDD"])


def legs_4b(r, spy, sub=False):
    """Idea 311's five 4b legs, verbatim."""
    a1, a2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    sh_r = m["Sharpe"] if sub else metrics(r.loc[OOS_START:])["Sharpe"]
    sh_s = ms["Sharpe"] if sub else metrics(spy.loc[OOS_START:])["Sharpe"]
    return dict(H1=bool(a1 > s1), H2=bool(a2 > s2), OOS=bool(sh_r > sh_s),
                DD=bool(m["MaxDD"] >= 0.60 * ms["MaxDD"]),
                CAGR=bool(m["CAGR"] >= 0.70 * ms["CAGR"]))


def fail_str(lg):
    f = [k for k, v in lg.items() if not v]
    return ",".join(f) if f else "-"


def ols(x, y):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    A = np.vstack([np.ones_like(x), x]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    resid = y - A @ coef
    ss = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - float((resid ** 2).sum()) / ss if ss > 0 else np.nan
    return float(coef[0]), float(coef[1]), r2


def real_panels():
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    return {
        "U56": (px56.dropna(how="all").ffill().loc[:PARENT_END], set(px56.columns)),
        "B136": (px136.dropna(how="all").ffill().loc[:PARENT_END], set(px136.columns)),
        f"SMALL{len(s_stk)}": (pxs[s_stk + ["SPY"]].dropna(how="all").ffill().loc[:PARENT_END],
                               set(s_stk)),
    }, len(bad)


def form_weights(name, px, tradable, g, sc=None):
    """Idea 311's pre-registered menu of unlevered book-forms, verbatim."""
    e = _priced(px, tradable) > 0
    if name == "EWall":
        return _ew(e, g)
    ma = above_ma(px) & e
    if name == "MA-RS":
        return _ew(ma, g)
    if name == "MA-DG":
        n = e.sum(axis=1).replace(0, np.nan)
        return g * ma.astype(float).div(n, axis=0).fillna(0.0)
    s = sc.where(e)
    if name in ("TOP20", "TOP10"):
        k = 20 if name == "TOP20" else 10
        return _ew(s.rank(axis=1, ascending=False) <= k, g)
    if name == "MA20":
        return _ew(s.where(ma).rank(axis=1, ascending=False) <= 20, g)
    raise ValueError(name)


def band_from(sub, legcols=("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")):
    """Idea 311's band solver, verbatim: the set of g where every named leg passes."""
    ok = sub[list(legcols)].all(axis=1).values
    gs = sub["gross"].values
    if not ok.any():
        always_fail = [c for c in legcols if not sub[c].any()]
        sharpe_names = {f"{p_}{k}" for k in SHARPE_LEGS for p_ in ("L_", "ISL_", "OOSL_")}
        reason = "SHARPE" if set(always_fail) & sharpe_names else "SCALE"
        return (np.nan, np.nan, 0.0, 0, True, reason)
    idx = np.flatnonzero(ok)
    lo, hi = float(gs[idx[0]]), float(gs[idx[-1]])
    return (lo, hi, hi - lo, int(ok.sum()), bool(idx[-1] - idx[0] + 1 == len(idx)), "-")


# ==================================================================================== run
def main():
    t0 = time.time()
    P("=" * 120)
    P(f"# {STAMP}")
    P("# IDEA 576 - idea 311's +0.0065/unit-g Sharpe drift is the signature of idle cash earning")
    P("#            ZERO.  Re-run its 612-book gross ladder with cash credited at 0 / 150 / 300 bps")
    P("#            and report whether the slope flattens, whether any 4b band widens, and whether")
    P("#            the panel ordering of band widths survives.")
    P("=" * 120)
    P(f"# PROTOCOL: cost {COST:.0f} bps on the RISKY legs, next-day fills, no leverage, "
      f"IS <= {IS_END}, OOS >= {OOS_START}, sample truncated at {PARENT_END}")
    P(f"# TUNED (2): CASH in {{{', '.join(f'{c:.0f}' for c in CASH_BPS)}}} bps x g in "
      f"{GGRID[0]:.2f}..{GGRID[-1]:.2f} step 0.05 ({len(GGRID)} points).  REPORTED-NOT-SELECTED:")
    P("#            panel, book-form, cadence, window.  Every grid point is written to .grid.csv.")
    P("")
    P("PRE-REGISTERED: H_REPRO (CASH=0 reproduces idea 311's committed rows on U56/B136),")
    P(f"  H_FLAT (median Sharpe slope in g falls monotonically in the cash rate and is smaller in")
    P(f"  magnitude at 300 bps than at 0, where idea 311 read {SLOPE311:+.4f}), H_KILL (it reaches")
    P("  zero or flips sign by 300 bps), H_WIDEN (more bands widen than narrow at 150 and at 300),")
    P("  H_ORDER (the panel ordering of mean band width is rate-invariant), H_NOFREE (any 4b pass")
    P("  bought by the credit is an asymmetric-comparand artefact - SPY holds no cash - and is")
    P("  named as one).")
    P("")
    P("CAVEAT (before the result): a FLAT 150/300 bps over 2009-2026 is not the cash rate that")
    P("  existed (~10 bps to 2015, ~500 after 2022).  This is a SENSITIVITY instrument for the")
    P("  convention, not a return forecast; idea 642 holds the real-instrument (SHY) version.")
    P("SURVIVORSHIP: B136 and the small panel are CURRENT constituents; dead names are absent, so")
    P("  every panel return here is biased UPWARD.")
    P("")

    panels, n_bad = real_panels()
    SMALLK = [k for k in panels if k.startswith("SMALL")][0]
    ref, SC = {}, {}
    for nm, (px, tr) in panels.items():
        st = px.index[260]
        ref[nm] = dict(start=st, spy=px["SPY"].pct_change().fillna(0.0).loc[st:])
        s, _, _ = score(px, vol_scale=False)
        SC[nm] = s
        P(f"  {nm:9s} {px.shape[1]:4d} cols, {len(tr):4d} tradable, sample from {st.date()}")
    P(f"  small panel: {n_bad} tickers with max_1d_move >= 1.0 dropped per PROTOCOL")
    P("")

    # ---------------------------------------------------------------- gates G1/G2/G3
    P("=" * 120)
    P("GATES (printed before any new number is read)")
    P("=" * 120)
    g1 = g2 = 0.0
    for nm, (px, tr) in panels.items():
        w = form_weights("MA-RS", px, tr, 0.75, SC[nm])
        a = fast_backtest(px, w, COST, "W")["returns"]
        b = backtest(px, w, cost_bps=COST, freq="W")["returns"]
        c = cash_backtest(px, w, 0.0, COST, "W")["returns"]
        g1 = max(g1, float((a - b).abs().max()))
        g2 = max(g2, float((a - c).abs().max()))
    P(f"G1 identity : fast_backtest vs engine.backtest,  max |dret| = {g1:.3e} (bar {TOL:.0e}) -> "
      f"{'PASS' if g1 <= TOL else 'FAIL'}")
    P(f"G2 cash-0   : cash_backtest(0) vs fast_backtest, max |dret| = {g2:.3e} (bar {TOL:.0e}) -> "
      f"{'PASS' if g2 <= TOL else 'FAIL'}")
    # G3: the credited runner vs an independent day-by-day reimplementation of the same accounting
    pxU, trU = panels["U56"]
    wg3 = form_weights("MA-RS", pxU, trU, 0.60, SC["U56"])
    g3 = 0.0
    for cb in CASH_BPS:
        a = cash_backtest(pxU, wg3, cb, COST, "W")["returns"]
        b = slow_cash_backtest(pxU, wg3, cb, COST, "W")["returns"]
        d = float((a - b).abs().max())
        g3 = max(g3, d)
        P(f"   cash {cb:5.0f} bps: max |dret| vs the day-by-day loop = {d:.3e}")
    P(f"G3 credit   : vectorised vs independent loop, max |dret| = {g3:.3e} (bar {TOL:.0e}) -> "
      f"{'PASS' if g3 <= TOL else 'FAIL'}")
    P("")

    # ---------------------------------------------------------------- the ladder
    P("=" * 120)
    P("THE LADDER - 6 forms x 3 panels x 2 cadences x 17 grosses x 3 cash rates")
    P("=" * 120)
    grid = []
    V2 = {}
    for nm, (px, tr) in panels.items():
        st = ref[nm]["start"]
        spy = ref[nm]["spy"]
        for cb in CASH_BPS:
            V2[(nm, cb)] = cash_backtest(px, rules_v2_weights(px), cb, COST,
                                         "W")["returns"].loc[st:]
        for form in FORMS:
            for g in GGRID:
                w = form_weights(form, px, tr, g, SC[nm])
                for freq in CADENCE:
                    for cb in CASH_BPS:
                        res = cash_backtest(px, w, cb, COST, freq)
                        r = res["returns"].loc[st:]
                        row = dict(panel=nm, form=form, cadence=freq, gross=g, cash_bps=cb)
                        row.update(rowify(r, res["turnover"].loc[st:]))
                        row["mean_cash_w"] = float(res["cash_weight"].loc[st:].mean())
                        lg = legs_4b(r, spy)
                        row.update({f"L_{k}": v for k, v in lg.items()})
                        row["fail4b"] = fail_str(lg)
                        row["keep4b"] = all(lg.values())
                        row["keep4a"] = keep_4a(r, V2[(nm, cb)])
                        lgi = legs_4b(r.loc[:IS_END], spy.loc[:IS_END], sub=True)
                        row.update({f"ISL_{k}": v for k, v in lgi.items()})
                        row["IS_keep4b"] = all(lgi.values())
                        lgo = legs_4b(r.loc[OOS_START:], spy.loc[OOS_START:], sub=True)
                        row.update({f"OOSL_{k}": v for k, v in lgo.items()})
                        row["OOS_keep4b"] = all(lgo.values())
                        grid.append(row)
        P(f"  {nm:9s} done ({time.time()-t0:.0f}s)")
    G = pd.DataFrame(grid)
    P(f"  {len(G)} books on the ladder ({time.time()-t0:.0f}s)")
    P("")

    # ---------------------------------------------------------------- G4 reproduction
    P("=" * 120)
    P("G4 - reproduction of idea 311's committed grid at CASH=0 (no credited number read yet)")
    P("=" * 120)
    par = pd.read_csv(PARENT311)
    mine0 = G[G.cash_bps == CASH_ANCHOR]
    cols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe", "IS_CAGR", "OOS_CAGR",
            "OOS_Sharpe", "OOS_MaxDD"]
    P(f"  bar = idea 630's standing tolerance tol_X(k) = a*k^b at k = {ELAPSED_K} elapsed days "
      f"(both runs pin the sample end at {PARENT_END}, so the residual is a price RESTATEMENT):")
    P("    " + "  ".join(f"{c} {tol630(c):.2e}" for c in ("Sharpe", "H1", "H2", "OOS_Sharpe",
                                                         "CAGR")))
    H_REPRO = True
    for pnl in par.panel.unique():
        here = pnl if pnl in set(G.panel.unique()) else SMALLK
        a = par[par.panel == pnl].set_index(["form", "cadence", "gross"])[cols].sort_index()
        b = mine0[mine0.panel == here].set_index(["form", "cadence", "gross"])[cols].sort_index()
        j = a.join(b, how="inner", lsuffix="_c", rsuffix="_r")
        ds = {c: float((j[c + "_c"] - j[c + "_r"]).abs().max()) for c in cols}
        worst = max(ds, key=lambda c: ds[c] / tol630(c))
        ok = all(ds[c] <= tol630(c) for c in cols)
        tag = ("PASS" if ok else "FAIL") if pnl == here else "DIFFERENT PANEL (not a reproduction)"
        P(f"  {pnl:9s} vs {here:9s}: {len(j)} rows x {len(cols)} cols, max |d| "
          f"{max(ds.values()):.3e}; worst vs its own bar {worst} {ds[worst]:.3e} / "
          f"{tol630(worst):.3e} = {ds[worst]/tol630(worst):.3f}x  -> {tag}")
        if pnl == here and pnl in ("U56", "B136"):
            H_REPRO &= ok
    P(f"  H_REPRO (U56 and B136 at CASH=0, inside idea 630's tolerance) -> "
      f"{'PASS' if H_REPRO else 'FAIL'}")
    P(f"  the small panel carries {len(panels[SMALLK][1])} tradable names today against idea 311's "
      f"439: its rows are a different panel, not a failed reproduction.")
    P("")

    # ---------------------------------------------------------------- H_FLAT / H_KILL
    P("=" * 120)
    P("H_FLAT / H_KILL - does the Sharpe slope in g flatten once the idle cash is paid for?")
    P("=" * 120)
    lin = []
    for (pnl, form, cad, cb), d in G.groupby(["panel", "form", "cadence", "cash_bps"]):
        d = d.sort_values("gross")
        _, bs, r2s = ols(d.gross, d.Sharpe)
        _, bc, r2c = ols(d.gross, d.CAGR)
        _, bd, r2d = ols(d.gross, d.MaxDD)
        lin.append(dict(panel=pnl, form=form, cadence=cad, cash_bps=cb, slope_Sharpe=bs,
                        r2_Sharpe=r2s, slope_CAGR=bc, r2_CAGR=r2c, slope_MaxDD=bd, r2_MaxDD=r2d,
                        Sharpe_span=float(d.Sharpe.max() - d.Sharpe.min()),
                        CAGR_span=float(d.CAGR.max() - d.CAGR.min()),
                        DD_span=float(d.MaxDD.max() - d.MaxDD.min()),
                        mean_cash_w=float(d.mean_cash_w.mean())))
    LIN = pd.DataFrame(lin)
    P(f"  {'cash':>5s} {'cells':>6s} {'median slope_Sharpe':>20s} {'mean':>9s} {'min':>9s} "
      f"{'max':>9s} {'>0':>7s} {'median |slope|':>15s} {'median Sharpe span':>19s}")
    for cb in CASH_BPS:
        d = LIN[LIN.cash_bps == cb]
        P(f"  {cb:5.0f} {len(d):6d} {d.slope_Sharpe.median():20.5f} {d.slope_Sharpe.mean():9.5f} "
          f"{d.slope_Sharpe.min():9.5f} {d.slope_Sharpe.max():9.5f} "
          f"{int((d.slope_Sharpe > 0).sum()):4d}/{len(d):<2d} "
          f"{d.slope_Sharpe.abs().median():15.5f} {d.Sharpe_span.median():19.5f}")
    med = {cb: float(LIN[LIN.cash_bps == cb].slope_Sharpe.median()) for cb in CASH_BPS}
    H_FLAT = bool(all(med[CASH_BPS[i]] >= med[CASH_BPS[i + 1]] for i in range(len(CASH_BPS) - 1))
                  and abs(med[CASH_BPS[-1]]) < abs(med[CASH_ANCHOR]))
    H_KILL = bool(med[CASH_BPS[-1]] <= 0.0)
    P(f"  idea 311's committed slope at the zero-cash convention: {SLOPE311:+.4f}/unit g;  "
      f"this run at 0 bps: {med[CASH_ANCHOR]:+.5f}")
    P(f"  H_FLAT (median slope monotone down in the rate AND |slope| smaller at 300 than at 0) -> "
      f"{'PASS' if H_FLAT else 'FAIL'}")
    P(f"  H_KILL (median slope <= 0 by 300 bps) -> {'PASS' if H_KILL else 'FAIL'}")
    # c* - the flat cash rate at which the median slope crosses zero: the PRICE of the convention
    cstar = np.nan
    for i in range(len(CASH_BPS) - 1):
        a_, b_ = CASH_BPS[i], CASH_BPS[i + 1]
        ya, yb = med[a_], med[b_]
        if (ya > 0) != (yb > 0) and ya != yb:
            cstar = a_ + (b_ - a_) * ya / (ya - yb)
            break
    P(f"  c* (flat cash rate at which the median slope in g crosses ZERO, linear between the")
    P(f"     bracketing rungs) = {cstar:.1f} bps/yr" if np.isfinite(cstar) else
      "  c* : the median slope does not cross zero on this rung set")
    P("     -> that is the price of the zero-cash convention in cash-rate units: a book ladder")
    P("        quoted at 0% idle cash is quoted at a cash rate c* below the one that would make")
    P("        its Sharpe genuinely g-invariant.")
    P("")
    P("  per-panel medians (reported, never selected):")
    for pnl in G.panel.unique():
        P(f"    {pnl:9s} " + "  ".join(
            f"{cb:.0f}bps {float(LIN[(LIN.panel==pnl)&(LIN.cash_bps==cb)].slope_Sharpe.median()):+.5f}"
            for cb in CASH_BPS))
    P("  per-form medians (reported, never selected):")
    for form in FORMS:
        P(f"    {form:7s} " + "  ".join(
            f"{cb:.0f}bps {float(LIN[(LIN.form==form)&(LIN.cash_bps==cb)].slope_Sharpe.median()):+.5f}"
            for cb in CASH_BPS)
          + f"   mean idle weight {float(LIN[LIN.form==form].mean_cash_w.mean()):.3f}")
    P("")

    # ---------------------------------------------------------------- the bands
    P("=" * 120)
    P("THE ADMISSIBLE 4b g-BAND AT EVERY CASH RATE")
    P("=" * 120)
    bands = []
    for (pnl, form, cad, cb), d in G.groupby(["panel", "form", "cadence", "cash_bps"]):
        d = d.sort_values("gross")
        lo, hi, w, npt, iv, why = band_from(d)
        lo2, hi2, w2, npt2, _, _ = band_from(d, legcols=("L_DD", "L_CAGR"))
        _, _, _, npt3, _, _ = band_from(d, legcols=("L_H1", "L_H2", "L_OOS"))
        bands.append(dict(panel=pnl, form=form, cadence=cad, cash_bps=cb, lo=lo, hi=hi, width=w,
                          n_pts=npt, interval=iv, empty_reason=why, scale_width=w2,
                          scale_lo=lo2, scale_hi=hi2, scale_pts=npt2, sharpe_pts=npt3))
    B = pd.DataFrame(bands)
    P(f"  {'panel':9s} {'form':7s} {'cad':3s}" + "".join(
        f" | {int(cb):3d}bps band     w" for cb in CASH_BPS))
    for (pnl, form, cad), d in B.groupby(["panel", "form", "cadence"]):
        d = d.set_index("cash_bps")
        line = f"  {pnl:9s} {form:7s} {cad:3s}"
        for cb in CASH_BPS:
            r = d.loc[cb]
            bs = f"[{r['lo']:.2f},{r['hi']:.2f}]" if r["n_pts"] else "EMPTY"
            line += f" | {bs:>12s} {r['width']:5.2f}"
        P(line)
    P("")
    piv = B.pivot_table(index=["panel", "form", "cadence"], columns="cash_bps",
                        values=["width", "n_pts"])
    wid = piv["width"]
    wider = {cb: int((wid[cb] > wid[CASH_ANCHOR] + 1e-12).sum()) for cb in CASH_BPS[1:]}
    narrower = {cb: int((wid[cb] < wid[CASH_ANCHOR] - 1e-12).sum()) for cb in CASH_BPS[1:]}
    same = {cb: int((wid[cb] - wid[CASH_ANCHOR]).abs().le(1e-12).sum()) for cb in CASH_BPS[1:]}
    newly = {cb: int(((piv['n_pts'][cb] > 0) & (piv['n_pts'][CASH_ANCHOR] == 0)).sum())
             for cb in CASH_BPS[1:]}
    lost = {cb: int(((piv['n_pts'][cb] == 0) & (piv['n_pts'][CASH_ANCHOR] > 0)).sum())
            for cb in CASH_BPS[1:]}
    for cb in CASH_BPS[1:]:
        P(f"  vs the 0-bps convention at {cb:.0f} bps: WIDER {wider[cb]}, NARROWER {narrower[cb]}, "
          f"unchanged {same[cb]} of {len(wid)} cells;  bands that become non-empty {newly[cb]}, "
          f"that vanish {lost[cb]};  mean width {float(wid[cb].mean()):.3f} vs "
          f"{float(wid[CASH_ANCHOR].mean()):.3f}")
    H_WIDEN = bool(all(wider[cb] > narrower[cb] for cb in CASH_BPS[1:]))
    P(f"  H_WIDEN -> {'PASS' if H_WIDEN else 'FAIL'}")
    P("")

    # ---------------------------------------------------------------- panel ordering
    P("=" * 120)
    P("H_ORDER - does the PANEL ORDERING of mean band width survive the cash rate?")
    P("=" * 120)
    ordrows, orders = [], {}
    for cb in CASH_BPS:
        d = B[B.cash_bps == cb].groupby("panel").agg(
            mean_width=("width", "mean"), nonempty=("n_pts", lambda s: int((s > 0).sum())),
            cells=("n_pts", "size"), mean_pts=("n_pts", "mean"))
        d = d.sort_values("mean_width", ascending=False)
        orders[cb] = tuple(d.index)
        for pnl, r in d.iterrows():
            ordrows.append(dict(cash_bps=cb, panel=pnl, mean_width=float(r.mean_width),
                                nonempty=int(r.nonempty), cells=int(r.cells),
                                mean_pts=float(r.mean_pts)))
        P(f"  {cb:5.0f} bps: " + "  >  ".join(
            f"{p} ({float(d.loc[p,'mean_width']):.3f}, {int(d.loc[p,'nonempty'])}/"
            f"{int(d.loc[p,'cells'])} non-empty)" for p in d.index))
    ORD = pd.DataFrame(ordrows)
    H_ORDER = bool(len(set(orders.values())) == 1)
    P(f"  H_ORDER (same ordering at every rate) -> {'PASS' if H_ORDER else 'FAIL'}  "
      f"[{' | '.join(str(orders[cb]) for cb in CASH_BPS)}]")
    P("")

    # ---------------------------------------------------------------- WF-A
    P("=" * 120)
    P(f"RULE 8 WF-A - band solved on IS <= {IS_END}, g* = IS midpoint, OOS >= {OOS_START} read ONCE")
    P("=" * 120)
    wf = []
    for (pnl, form, cad, cb), d in G.groupby(["panel", "form", "cadence", "cash_bps"]):
        d = d.sort_values("gross")
        lo_i, hi_i, w_i, n_i, _, _ = band_from(d, legcols=tuple(f"ISL_{k}" for k in LEGS))
        lo_o, hi_o, w_o, n_o, _, _ = band_from(d, legcols=tuple(f"OOSL_{k}" for k in LEGS))
        gstar = np.nan if n_i == 0 else round(((lo_i + hi_i) / 2) / 0.05) * 0.05
        inside = bool(n_o > 0 and not np.isnan(gstar) and lo_o - 1e-9 <= gstar <= hi_o + 1e-9)
        wf.append(dict(leg="WF-A", panel=pnl, form=form, cadence=cad, cash_bps=cb, IS_lo=lo_i,
                       IS_hi=hi_i, IS_width=w_i, IS_pts=n_i, gstar=gstar, OOS_lo=lo_o,
                       OOS_hi=hi_o, OOS_width=w_o, OOS_pts=n_o, gstar_in_OOS=inside))
    WFA = pd.DataFrame(wf)
    P(f"  {'cash':>5s} {'IS non-empty':>13s} {'OOS non-empty':>14s} {'g* inside OOS band':>19s} "
      f"{'mean IS width':>14s} {'mean OOS width':>15s}")
    for cb in CASH_BPS:
        d = WFA[WFA.cash_bps == cb]
        ne = d[d.IS_pts > 0]
        P(f"  {cb:5.0f} {int((d.IS_pts>0).sum()):6d}/{len(d):<6d} "
          f"{int((d.OOS_pts>0).sum()):7d}/{len(d):<6d} "
          f"{int(ne.gstar_in_OOS.sum()):10d}/{len(ne):<8d} {float(d.IS_width.mean()):14.3f} "
          f"{float(d.OOS_width.mean()):15.3f}")
    P("  (idea 311 read 9 of 20 at the zero-cash convention: the IS band does not transport.)")
    P("")

    # ---------------------------------------------------------------- WF-B
    P("=" * 120)
    P("RULE 8 WF-B - a BOOK: form by IS Sharpe, g = IS band midpoint, B136/W, OOS read ONCE")
    P("=" * 120)
    wfb = []
    pxB, trB = panels["B136"]
    stB = ref["B136"]["start"]
    spyB = ref["B136"]["spy"]
    msp = metrics(spyB.loc[OOS_START:])
    for cb in CASH_BPS:
        selb = G[(G.panel == "B136") & (G.cadence == "W") & (G.cash_bps == cb)]
        ist = selb.groupby("form").IS_Sharpe.mean().sort_values(ascending=False)
        pick_form = str(ist.index[0])
        prow = WFA[(WFA.panel == "B136") & (WFA.form == pick_form) & (WFA.cadence == "W")
                   & (WFA.cash_bps == cb)].iloc[0]
        pick_g = float(prow.gstar) if prow.IS_pts > 0 else 0.75
        w = form_weights(pick_form, pxB, trB, pick_g, SC["B136"])
        rp = cash_backtest(pxB, w, cb, COST, "W")["returns"].loc[stB:]
        v2 = V2[("B136", cb)]
        d = rowify(rp)
        mv2 = metrics(v2.loc[OOS_START:])
        wfb.append(dict(leg="WF-B", cash_bps=cb, panel="B136", cadence="W", form=pick_form,
                        gstar=pick_g, IS_band_empty=bool(prow.IS_pts == 0), **d,
                        keep4a_vs_v2=keep_4a(rp, v2), fail4b_full=fail_str(legs_4b(rp, spyB)),
                        fail4b_oos=fail_str(legs_4b(rp.loc[OOS_START:], spyB.loc[OOS_START:],
                                                    sub=True)),
                        v2_OOS_CAGR=mv2["CAGR"], v2_OOS_Sharpe=mv2["Sharpe"],
                        v2_OOS_MaxDD=mv2["MaxDD"], spy_OOS_CAGR=msp["CAGR"],
                        spy_OOS_Sharpe=msp["Sharpe"], spy_OOS_MaxDD=msp["MaxDD"]))
        P(f"  {cb:5.0f} bps: pick {pick_form} g={pick_g:.2f}"
          f"{' (IS band EMPTY, g defaults 0.75)' if prow.IS_pts == 0 else ''}")
        P(f"            FULL {d['CAGR']:7.2%} / {d['Sharpe']:.4f} / {d['MaxDD']:7.2%} "
          f"(H1 {d['H1']:.4f}, H2 {d['H2']:.4f});  OOS {d['OOS_CAGR']:7.2%} / "
          f"{d['OOS_Sharpe']:.4f} / {d['OOS_MaxDD']:7.2%}")
        P(f"            RULES v2 (B136, cash {cb:.0f} bps) OOS {mv2['CAGR']:7.2%} / "
          f"{mv2['Sharpe']:.4f} / {mv2['MaxDD']:7.2%};  SPY OOS {msp['CAGR']:7.2%} / "
          f"{msp['Sharpe']:.4f} / {msp['MaxDD']:7.2%}")
        P(f"            4a vs RULES v2 {wfb[-1]['keep4a_vs_v2']};  4b fail legs (full) "
          f"{wfb[-1]['fail4b_full']};  in the OOS window alone {wfb[-1]['fail4b_oos']}")
    WFB = pd.DataFrame(wfb)
    P("")

    # ---------------------------------------------------------------- KEEP paths
    P("=" * 120)
    P("KEEP PATHS 4a / 4b - every book, every cash rate")
    P("=" * 120)
    P("  4a's comparand (RULES v2) is credited at the SAME rate as the book; 4b's comparand (SPY,")
    P("  buy-and-hold) holds no cash and is therefore UNCHANGED by the rate - stated, not hidden.")
    P(f"  {'cash':>5s} {'books':>6s} {'4a':>6s} {'4b':>6s} {'BOTH':>6s}  binding 4b legs")
    for cb in CASH_BPS:
        d = G[G.cash_bps == cb]
        legs = pd.Series([x for s in d.loc[~d.keep4b, "fail4b"] for x in s.split(",")]
                         ).value_counts()
        P(f"  {cb:5.0f} {len(d):6d} {int(d.keep4a.sum()):6d} {int(d.keep4b.sum()):6d} "
          f"{int((d.keep4a & d.keep4b).sum()):6d}  "
          + "  ".join(f"{k} {v}" for k, v in legs.items()))
    for cb in CASH_BPS:
        d = G[(G.cash_bps == cb) & G.keep4b]
        if len(d):
            P(f"  {cb:5.0f} bps 4b passers by panel: "
              + "  ".join(f"{k} {v}" for k, v in d.panel.value_counts().items())
              + "   by form: " + "  ".join(f"{k} {v}" for k, v in d.form.value_counts().items()))
    base4b = set(map(tuple, G[(G.cash_bps == CASH_ANCHOR) & G.keep4b][
        ["panel", "form", "cadence", "gross"]].values))
    for cb in CASH_BPS[1:]:
        now = set(map(tuple, G[(G.cash_bps == cb) & G.keep4b][
            ["panel", "form", "cadence", "gross"]].values))
        P(f"  {cb:5.0f} bps: 4b passes BOUGHT by the credit {len(now - base4b)}, "
          f"LOST {len(base4b - now)}")
    P("  Every pass bought by the credit is a pass against a comparand that does not receive it;")
    P("  none is a capital candidate and none is claimed as one.")
    P("")

    # ---------------------------------------------------------------- verdict
    P("=" * 120)
    P("VERDICT")
    P("=" * 120)
    for a, b in dict(H_REPRO=H_REPRO, H_FLAT=H_FLAT, H_KILL=H_KILL, H_WIDEN=H_WIDEN,
                     H_ORDER=H_ORDER).items():
        P(f"  {a:8s} {'PASS' if b else 'FAIL'}")
    P(f"  median Sharpe slope in g: " + "  ".join(f"{cb:.0f}bps {med[cb]:+.5f}" for cb in CASH_BPS))
    P(f"  mean 4b band width:       " + "  ".join(
        f"{cb:.0f}bps {float(B[B.cash_bps==cb].width.mean()):.3f}" for cb in CASH_BPS))
    P("")

    G.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    B.to_csv(OUT / f"{STAMP}.bands.csv", index=False)
    LIN.to_csv(OUT / f"{STAMP}.slopes.csv", index=False)
    ORD.to_csv(OUT / f"{STAMP}.order.csv", index=False)
    pd.concat([WFA, WFB], ignore_index=True, sort=False).to_csv(
        OUT / f"{STAMP}.walkforward.csv", index=False)
    G[["panel", "form", "cadence", "gross", "cash_bps", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
       "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "mean_cash_w", "keep4a", "fail4b",
       "keep4b"]].to_csv(OUT / f"{STAMP}.keeppaths.csv", index=False)
    P(f"  wrote grid {len(G)}, bands {len(B)}, slopes {len(LIN)}, order {len(ORD)}, "
      f"wf {len(WFA)+len(WFB)} rows ({time.time()-t0:.0f}s)")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()

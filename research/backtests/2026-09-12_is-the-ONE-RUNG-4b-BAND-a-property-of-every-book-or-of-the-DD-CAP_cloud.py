#!/usr/bin/env python3
"""Idea 804 (cloud, 2026-09-12) - is-the-ONE-RUNG-4b-BAND-a-property-of-every-book-or-of-the-DD-CAP.

QUESTION
--------
Idea 574 swept the ten most-cited unswept 4b passes over 17 gross rungs and found (a) the admissible
band has a MEDIAN WIDTH OF ONE RUNG among the five books that pass anywhere, (b) the pass set is
contiguous in every case, (c) at the IS-Sharpe-optimal g=1.00 every Sharpe-clearing book dies on the
4b drawdown cap alone.  That was read off five books.  This run asks whether "the one-rung band" is a
property of BOOKS or a property of the BARS: decompose each band's two edges leg by leg over a much
wider book set, and report whether the band is really the DD cap's upper edge meeting the CAGR
floor's lower edge with nothing else in play.

WHAT COUNTS AS WHAT (every rule stated before any number)
---------------------------------------------------------
* A **book** is (panel, form, n, cadence).  Gross is NOT part of the book here - it is the dial.
* PROTOCOL 4b has FIVE legs: H1 Sharpe > SPY, H2 Sharpe > SPY, OOS Sharpe > SPY, MaxDD <= 60% of
  SPY's, CAGR >= 70% of SPY's.  A cell PASSES 4b when all five hold; otherwise the failing legs are
  named.  Legs are computed exactly as idea 574's `fail_4b`, same code path, same window.
* A book's **band** is the set of gross rungs at which it passes 4b.  It is CONTIGUOUS when that set
  is an interval of the grid; band width is only a meaningful summary if it is, so contiguity is
  measured per book and published, never assumed.
* The band's **lower-edge binding legs** are the legs that fail at the rung immediately BELOW the
  band (or `GRID-LO` when the band starts at the grid's first rung, i.e. the edge is the grid's, not
  a bar's).  **Upper-edge binding legs** likewise at the rung immediately ABOVE (or `GRID-HI`).
* A book is **SHARPE-CLEARING** when its three Sharpe legs (H1, H2, OOS) hold at SOME rung.  This
  matters because the Sharpe legs are near-invariant in gross by construction (a book at gross g is
  the same holdings mixed with cash, so mean and vol both scale and only the cost drag differs) -
  measured per book at G4, not asserted.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two - the queue's own: book set, gross)
    1. BOOK SET  5 panels x 5 forms x 2 cadences = 50 books.  ALL 50 reported.
                 panels  U56, ETF36, B136, BSTK100, SMALL
                 forms   EWALL, MA-DG, MA-RS, CAND20, R620   (n fixed at 20 where a form takes one)
                 cadence W (weekly), M (monthly)
    2. GROSS     17 rungs, g = 0.20, 0.25, ... , 1.00.  ALL 17 reported for ALL 50 books.
REPORTED-NEVER-SELECTED: cost rung (10 bps per PROTOCOL, 25 bps beside it), window (FULL / IS / OOS),
the 4a path, and the per-leg edge attribution itself.

GATES (printed before any band number is read)
    G1 engine     : fast_backtest vs engine.backtest on one book.                      bar 1e-9
    G2 comparands : live RULES v2 on U56 and SPY over this run's window, printed so every later bar
                    can be checked by hand.                                            no bar
    G3 linearity  : weights(g) == g * weights(1.00) for every form, so the 50 x 17 grid is built
                    once per book and scaled.                                          bar 1e-12
    G4 invariance : per book, the spread of each Sharpe leg across the 17 rungs.  MEASURED and
                    published, no bar - it is the mechanism the answer turns on.

PRE-REGISTERED HYPOTHESES (written before any grid point was read)
    H_DD    : the upper edge binds on DD ALONE in >= 2/3 of the bands that have a bar-set upper edge.
    H_CAGR  : the lower edge binds on CAGR ALONE in >= 2/3 of the bands that have a bar-set lower edge.
    H_ONLY  : in >= 2/3 of bands, the two edges together involve ONLY {DD, CAGR} - no Sharpe leg
              appears at either edge.  (This is the queue's "nothing else in play".)
    H_NARROW: median band width <= 2 of 17 rungs over the wider set (574 measured 1 on five books).
    H_MONO  : the 4b pass set is contiguous for every book that passes anywhere.
    H_RATE  : >= 50% of the 50 books pass 4b somewhere (574's 5-of-10 rate generalises).
    H_WF    : rule 8 - the IS-fitted band contains the OOS-admissible band's midpoint for >= half of
              the books admissible in both windows.

RULE 8 WALK-FORWARD (required)
    IS = ..2016-12-31, OOS = 2017-01-01.. , OOS read ONCE.
    WF-A on the ANSWER: bands and their edge attribution are recomputed inside the IS window alone
       and inside the OOS window alone; IS/OOS band overlap, midpoint agreement and - the point of
       this idea - whether the SAME legs bind the SAME edges out of sample.
    WF-B on a BOOK: (book, gross) chosen by IS Sharpe ALONE over the whole 50 x 17 IS grid, then OOS
       CAGR / Sharpe / MaxDD read ONCE against live RULES v2 (U56, weekly, 10 bps) and against SPY.
       The IS-best-gross-per-book OOS table is published for all 50.

KEEP PATHS: 4a and 4b are evaluated at every one of the 50 x 17 x 2 costs = 1,700 cells and counted.

SURVIVORSHIP: U56 / ETF36 / B136 / BSTK100 are current constituents of universe.json /
    universe_broad.json; the sub-$2B panel is the current constituent list of its screen with every
    ticker whose max_1d_move >= 1.0 in data/small_meta.csv dropped first, per PROTOCOL.  Names that
    died are absent from all of them, so every CAGR here is biased upward and every 4b CAGR-floor
    pass is easier than it would be on a point-in-time panel.  Stated again beside the result.

PROTOCOL: 10 bps per unit turnover, next-day fills (engine), no shorting, no leverage.
Deterministic, standalone, no network.  Reads research/baseline.py; modifies nothing but its own
outputs: .grid.csv .bands.csv .edges.csv .invariance.csv .walkforward.csv .keeppaths.csv .console.txt
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score, metrics, backtest  # noqa: E402
from engine import rebalance_mask  # noqa: E402

STAMP = "2026-09-12_is-the-ONE-RUNG-4b-BAND-a-property-of-every-book-or-of-the-DD-CAP_cloud"
OUT = ROOT / "research" / "backtests"

COST_MAIN, COST_ALT = 10.0, 25.0
GGRID = [round(0.20 + 0.05 * i, 2) for i in range(17)]        # TUNED 2
PANELS = ["U56", "ETF36", "B136", "BSTK100", "SMALL"]         # TUNED 1 (a)
FORMS = ["EWALL", "MA-DG", "MA-RS", "CAND20", "R620"]         # TUNED 1 (b)
CADENCES = ["W", "M"]                                         # TUNED 1 (c)
NDEF = 20
IS_END, OOS_START = "2016-12-31", "2017-01-01"
MAX_VOL, MA_WIN, TOL = 0.60, 200, 1e-9
LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


# ------------------------------------------------------------------ vectorised runner (idea 574)
def fast_backtest(prices, weights, cost_bps, freq):
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
    return pd.Series(port, index=idx)


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def keep_4a(r, b):
    a1, a2 = halves(r)
    b1, b2 = halves(b)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(b)["MaxDD"])


def legs_4b(r, spy, lo=None, hi=None, oos=True):
    """PROTOCOL 4b's five legs, each returned as pass/fail, inside the window [lo, hi].
    oos=False drops the OOS leg (it is undefined inside a single window) and says so by name."""
    rr, ss = r.loc[lo:hi], spy.loc[lo:hi]
    a1, a2 = halves(rr)
    s1, s2 = halves(ss)
    m, ms = metrics(rr), metrics(ss)
    d = {"H1": bool(a1 > s1), "H2": bool(a2 > s2),
         "DD": bool(m["MaxDD"] >= 0.60 * ms["MaxDD"]),
         "CAGR": bool(m["CAGR"] >= 0.70 * ms["CAGR"])}
    if oos:
        d["OOS"] = bool(metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"])
    return d


def failstr(d):
    f = [k for k in LEGS if k in d and not d[k]]
    return ",".join(f) if f else "-"


# ------------------------------------------------------------------ panels and books
def panels():
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    etf36 = U["broad"] + U["sectors"] + U["bonds_fx_commod"]
    b_stk = [t for t in px136.columns if t not in set(etf36) and t != "SPY"]
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]

    def sub(px, cols, tradable=None):
        cols = [c for c in cols if c in px.columns]
        keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px.columns else [])))
        return px[keep].dropna(how="all").ffill(), set(tradable if tradable is not None else cols)

    return {"U56": sub(px56, list(px56.columns)),
            "ETF36": sub(px56, [t for t in etf36 if t in px56.columns]),
            "B136": sub(px136, list(px136.columns)),
            "BSTK100": sub(px136, b_stk, tradable=b_stk),
            "SMALL": sub(pxs, s_stk, tradable=s_stk)}, len(bad), len(s_stk)


def build_weights(px, tradable, form, n, g):
    """Target weights at gross g.  Every form is linear in g (checked at G3)."""
    cols = [c for c in px.columns if c in tradable]
    priced = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    priced[cols] = px[cols].notna().astype(float)
    pm = priced > 0
    if form == "EWALL":
        cnt = pm.sum(axis=1).replace(0, np.nan)
        return g * pm.div(cnt, axis=0).fillna(0.0)
    ma = (px > px.rolling(MA_WIN).mean()) & pm
    if form == "MA-DG":
        cnt = pm.sum(axis=1).replace(0, np.nan)
        return (g * pm.div(cnt, axis=0).fillna(0.0)).where(ma, 0.0)
    if form == "MA-RS":
        cnt = ma.sum(axis=1).replace(0, np.nan)
        return g * ma.div(cnt, axis=0).fillna(0.0)
    if form == "CAND20":
        s, above, vol20 = score(px)
        s = s.where(pm)
        elig = s.where(above & (vol20 < MAX_VOL))
        rk = elig.rank(axis=1, ascending=False)
        return (rk <= n).astype(float) * (g / n)
    if form == "R620":
        r6 = (px / px.shift(126) - 1.0).where(pm)
        rk = r6.rank(axis=1, ascending=False)
        return (rk <= n).astype(float) * (g / n)
    raise ValueError(form)


# ------------------------------------------------------------------ band helpers
def band_of(passes):
    """passes: list of bool over GGRID.  Returns (lo_idx, hi_idx, width, contiguous)."""
    idx = [i for i, p in enumerate(passes) if p]
    if not idx:
        return None, None, 0, True
    lo, hi = min(idx), max(idx)
    return lo, hi, len(idx), len(idx) == hi - lo + 1


def edges(passes, fails):
    """Which legs bind each edge of the pass band.  fails: list of dicts (leg -> bool pass)."""
    lo, hi, w, contig = band_of(passes)
    if lo is None:
        return None
    lower = "GRID-LO" if lo == 0 else failstr(fails[lo - 1])
    upper = "GRID-HI" if hi == len(passes) - 1 else failstr(fails[hi + 1])
    return dict(lo=GGRID[lo], hi=GGRID[hi], width=w, contiguous=contig, lower=lower, upper=upper)


def main():
    t0 = time.time()
    P(f"# Idea 804 - {STAMP}")
    P(f"# run {pd.Timestamp.utcnow():%Y-%m-%d %H:%M} UTC | PROTOCOL 10 bps, next-day fills, no leverage")

    PX, n_bad, n_small = panels()
    P(f"\nPanels: " + ", ".join(f"{k}={len(v[1])} tradable ({len(v[0])} rows "
                                f"{v[0].index[0]:%Y-%m-%d}..{v[0].index[-1]:%Y-%m-%d})"
                                for k, v in PX.items()))
    P(f"SMALL panel: dropped {n_bad} tickers with max_1d_move >= 1.0 per PROTOCOL -> {n_small} tradable.")

    # ---------------- G1 engine agreement
    px, trad = PX["U56"]
    w = build_weights(px, trad, "EWALL", NDEF, 0.75)
    a = fast_backtest(px, w, COST_MAIN, "W")
    b = backtest(px, w, cost_bps=COST_MAIN, freq="W")["returns"]
    d = float(np.abs(a.reindex(b.index).fillna(0) - b).max())
    P(f"\nG1 engine agreement  max|fast - engine| = {d:.3e}  bar 1e-9  -> {'PASS' if d < TOL else 'FAIL'}")
    assert d < TOL, "G1 failed"

    # ---------------- G3 linearity of every form in g
    P("\nG3 linearity  max|w(g) - g*w(1.00)| per form (bar 1e-12):")
    ok = True
    for form in FORMS:
        w1 = build_weights(px, trad, form, NDEF, 1.00)
        w5 = build_weights(px, trad, form, NDEF, 0.55)
        e = float(np.abs(w5.values - 0.55 * w1.values).max())
        ok &= e < 1e-12
        P(f"    {form:8s} {e:.3e}")
    P(f"    -> {'PASS' if ok else 'FAIL'}  (grid built once per book, scaled by g)")
    assert ok, "G3 failed"

    # ---------------- G2 comparands
    START = {k: v[0].index[260] for k, v in PX.items()}
    base = fast_backtest(px, rules_v2_weights(px), COST_MAIN, "W").loc[START["U56"]:]
    P("\nG2 comparands (this run's windows):")
    P(f"    RULES v2 live (U56, W, 10 bps)  CAGR {metrics(base)['CAGR']:.2%} Sharpe {metrics(base)['Sharpe']:.2f} "
      f"MaxDD {metrics(base)['MaxDD']:.1%}  halves {halves(base)[0]:.2f}/{halves(base)[1]:.2f}")
    SPY = {}
    for k, (p, _) in PX.items():
        s = p["SPY"].pct_change().fillna(0.0).loc[START[k]:]
        SPY[k] = s
        m = metrics(s)
        P(f"    SPY on {k:8s} CAGR {m['CAGR']:.2%} Sharpe {m['Sharpe']:.2f} MaxDD {m['MaxDD']:.1%} "
          f"halves {halves(s)[0]:.2f}/{halves(s)[1]:.2f} | 4b bars: CAGR floor {0.70*m['CAGR']:.2%}, "
          f"DD cap {0.60*m['MaxDD']:.1%}")

    # ---------------- the grid
    P(f"\nGrid: {len(PANELS)} panels x {len(FORMS)} forms x {len(CADENCES)} cadences = "
      f"{len(PANELS)*len(FORMS)*len(CADENCES)} books x {len(GGRID)} rungs x 2 costs = "
      f"{len(PANELS)*len(FORMS)*len(CADENCES)*len(GGRID)*2} cells.  ALL reported.")
    grid, bands, inv, wf = [], [], [], []
    for panel in PANELS:
        pxp, tradp = PX[panel]
        spy = SPY[panel]
        st = START[panel]
        base_p = fast_backtest(pxp, rules_v2_weights(pxp), COST_MAIN, "W").loc[st:]
        for form in FORMS:
            w1 = build_weights(pxp, tradp, form, NDEF, 1.00)
            for cad in CADENCES:
                key = f"{panel}/{form}/{cad}"
                passes = {COST_MAIN: [], COST_ALT: []}
                fails = {COST_MAIN: [], COST_ALT: []}
                isp, oosp, isf, oosf, is_sharpe = [], [], [], [], []
                for g in GGRID:
                    for cost in (COST_MAIN, COST_ALT):
                        r = fast_backtest(pxp, w1 * g, cost, cad).loc[st:]
                        d5 = legs_4b(r, spy)
                        m = metrics(r)
                        passes[cost].append(all(d5.values()))
                        fails[cost].append(d5)
                        if cost == COST_MAIN:
                            mi, mo = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
                            dis = legs_4b(r, spy, hi=IS_END, oos=False)
                            dos = legs_4b(r, spy, lo=OOS_START, oos=False)
                            isp.append(all(dis.values())); oosp.append(all(dos.values()))
                            isf.append(dis); oosf.append(dos)
                            is_sharpe.append(mi["Sharpe"])
                            grid.append(dict(book=key, panel=panel, form=form, cadence=cad, gross=g,
                                             cost_bps=cost, CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                                             MaxDD=m["MaxDD"], H1=halves(r)[0], H2=halves(r)[1],
                                             IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                                             OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                             pass4b=all(d5.values()), fail4b=failstr(d5),
                                             pass4a=keep_4a(r, base_p),
                                             IS_pass4b=all(dis.values()), IS_fail4b=failstr(dis),
                                             OOS_pass4b=all(dos.values()), OOS_fail4b=failstr(dos)))
                        else:
                            grid.append(dict(book=key, panel=panel, form=form, cadence=cad, gross=g,
                                             cost_bps=cost, CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                                             MaxDD=m["MaxDD"], H1=halves(r)[0], H2=halves(r)[1],
                                             IS_CAGR=np.nan, IS_Sharpe=np.nan, IS_MaxDD=np.nan,
                                             OOS_CAGR=np.nan, OOS_Sharpe=np.nan, OOS_MaxDD=np.nan,
                                             pass4b=all(d5.values()), fail4b=failstr(d5),
                                             pass4a=keep_4a(r, base_p), IS_pass4b=None, IS_fail4b="",
                                             OOS_pass4b=None, OOS_fail4b=""))
                # G4 invariance: spread of each Sharpe leg over the 17 rungs (10 bps)
                sub = [c for c in grid if c["book"] == key and c["cost_bps"] == COST_MAIN]
                inv.append(dict(book=key,
                                H1_spread=max(c["H1"] for c in sub) - min(c["H1"] for c in sub),
                                H2_spread=max(c["H2"] for c in sub) - min(c["H2"] for c in sub),
                                OOS_spread=max(c["OOS_Sharpe"] for c in sub) - min(c["OOS_Sharpe"] for c in sub),
                                CAGR_spread=max(c["CAGR"] for c in sub) - min(c["CAGR"] for c in sub),
                                DD_spread=max(c["MaxDD"] for c in sub) - min(c["MaxDD"] for c in sub),
                                sharpe_clearing=any(c["fail4b"] in ("-", "DD", "CAGR", "DD,CAGR",
                                                                    "CAGR,DD") for c in sub)))
                e10 = edges(passes[COST_MAIN], fails[COST_MAIN])
                e25 = edges(passes[COST_ALT], fails[COST_ALT])
                bands.append(dict(book=key, panel=panel, form=form, cadence=cad,
                                  n_pass=sum(passes[COST_MAIN]),
                                  lo=e10["lo"] if e10 else np.nan, hi=e10["hi"] if e10 else np.nan,
                                  width=e10["width"] if e10 else 0,
                                  contiguous=e10["contiguous"] if e10 else True,
                                  lower_edge=e10["lower"] if e10 else "",
                                  upper_edge=e10["upper"] if e10 else "",
                                  n_pass_25=sum(passes[COST_ALT]),
                                  lo25=e25["lo"] if e25 else np.nan, hi25=e25["hi"] if e25 else np.nan,
                                  ladder="".join("P" if p else "." for p in passes[COST_MAIN])))
                eis = edges(isp, isf)
                eos = edges(oosp, oosf)
                kbest = int(np.argmax(is_sharpe))
                r_best = fast_backtest(pxp, w1 * GGRID[kbest], COST_MAIN, cad).loc[st:]
                mo, ms = metrics(r_best.loc[OOS_START:]), metrics(spy.loc[OOS_START:])
                mb = metrics(base_p.loc[OOS_START:])
                wf.append(dict(book=key, IS_lo=eis["lo"] if eis else np.nan,
                               IS_hi=eis["hi"] if eis else np.nan,
                               IS_width=eis["width"] if eis else 0,
                               IS_lower=eis["lower"] if eis else "", IS_upper=eis["upper"] if eis else "",
                               OOS_lo=eos["lo"] if eos else np.nan, OOS_hi=eos["hi"] if eos else np.nan,
                               OOS_width=eos["width"] if eos else 0,
                               OOS_lower=eos["lower"] if eos else "", OOS_upper=eos["upper"] if eos else "",
                               g_isbest=GGRID[kbest], IS_Sharpe=is_sharpe[kbest],
                               OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                               OOS_CAGR_spy=ms["CAGR"], OOS_Sharpe_spy=ms["Sharpe"], OOS_MaxDD_spy=ms["MaxDD"],
                               OOS_CAGR_base=mb["CAGR"], OOS_Sharpe_base=mb["Sharpe"], OOS_MaxDD_base=mb["MaxDD"]))
        P(f"    {panel:8s} done  ({time.time()-t0:.0f}s)")

    G = pd.DataFrame(grid)
    B = pd.DataFrame(bands)
    I = pd.DataFrame(inv)
    W = pd.DataFrame(wf)
    G.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    B.to_csv(OUT / f"{STAMP}.bands.csv", index=False)
    I.to_csv(OUT / f"{STAMP}.invariance.csv", index=False)
    W.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)

    # ---------------- G4 report
    P("\nG4 invariance - spread of each metric across the 17 gross rungs (10 bps), median over 50 books:")
    P(f"    H1 Sharpe {I.H1_spread.median():.3f}  H2 Sharpe {I.H2_spread.median():.3f}  "
      f"OOS Sharpe {I.OOS_spread.median():.3f}  |  CAGR {I.CAGR_spread.median():.2%}  "
      f"MaxDD {I.DD_spread.median():.1%}")
    P(f"    max over books: H1 {I.H1_spread.max():.3f} H2 {I.H2_spread.max():.3f} "
      f"OOS {I.OOS_spread.max():.3f} | CAGR {I.CAGR_spread.max():.2%} MaxDD {I.DD_spread.max():.1%}")

    # ---------------- ladders
    P("\n## The 50 ladders (g = 0.20 -> 1.00, step 0.05; P = passes 4b at 10 bps)")
    P(f"    {'book':24s} {' '.join(f'{int(g*100):02d}' for g in GGRID)}   band      lower-edge / upper-edge")
    for _, r in B.iterrows():
        bd = "-" if r.n_pass == 0 else f"{r.lo:.2f}-{r.hi:.2f}"
        P(f"    {r.book:24s} {'  '.join(r.ladder)}   {bd:9s} {r.lower_edge or '-'} / {r.upper_edge or '-'}")

    # ---------------- hypotheses
    P("\n## Pre-registered hypotheses")
    bb = B[B.n_pass > 0]
    n_pass_books = len(bb)
    P(f"    books passing 4b somewhere: {n_pass_books} of {len(B)} "
      f"({n_pass_books/len(B):.0%}); passing cells {int(G[(G.cost_bps==COST_MAIN)].pass4b.sum())} "
      f"of {int((G.cost_bps==COST_MAIN).sum())} at 10 bps, "
      f"{int(G[(G.cost_bps==COST_ALT)].pass4b.sum())} of {int((G.cost_bps==COST_ALT).sum())} at 25 bps")
    res = {}
    res["H_RATE"] = (n_pass_books >= 0.5 * len(B), f"{n_pass_books}/{len(B)} books pass somewhere (bar >= 25)")
    if n_pass_books:
        res["H_NARROW"] = (bb.width.median() <= 2, f"median band width {bb.width.median():.1f} rungs of 17 (bar <= 2)")
        res["H_MONO"] = (bool(bb.contiguous.all()), f"{int(bb.contiguous.sum())}/{n_pass_books} bands contiguous")
        up = bb[~bb.upper_edge.isin(["GRID-HI"])]
        lo = bb[~bb.lower_edge.isin(["GRID-LO"])]
        dd_only = (up.upper_edge == "DD").sum()
        cagr_only = (lo.lower_edge == "CAGR").sum()
        res["H_DD"] = (len(up) > 0 and dd_only >= 2/3 * len(up),
                       f"upper edge = DD alone in {dd_only}/{len(up)} bar-set upper edges")
        res["H_CAGR"] = (len(lo) > 0 and cagr_only >= 2/3 * len(lo),
                         f"lower edge = CAGR alone in {cagr_only}/{len(lo)} bar-set lower edges")
        def only_bars(r):
            toks = set()
            for e in (r.lower_edge, r.upper_edge):
                if e and not e.startswith("GRID"):
                    toks |= set(e.split(","))
            return toks <= {"DD", "CAGR"}
        n_only = int(bb.apply(only_bars, axis=1).sum())
        res["H_ONLY"] = (n_only >= 2/3 * n_pass_books,
                         f"{n_only}/{n_pass_books} bands have only DD/CAGR at both edges")
        both = W[(W.IS_width > 0) & (W.OOS_width > 0)]
        if len(both):
            inside = int(((both.IS_lo <= (both.OOS_lo + both.OOS_hi) / 2) &
                          ((both.OOS_lo + both.OOS_hi) / 2 <= both.IS_hi)).sum())
            res["H_WF"] = (inside >= 0.5 * len(both),
                           f"IS band contains OOS midpoint in {inside}/{len(both)} books admissible in both")
        else:
            res["H_WF"] = (False, "no book is admissible in BOTH the IS and the OOS window")
    for k in ["H_DD", "H_CAGR", "H_ONLY", "H_NARROW", "H_MONO", "H_RATE", "H_WF"]:
        if k in res:
            v, txt = res[k]
            P(f"    {k:9s} {'PASS' if v else 'FAIL'}  - {txt}")

    # ---------------- edge census
    P("\n## Edge census (which legs bind, over all bands, 10 bps)")
    if n_pass_books:
        P("    lower edges: " + ", ".join(f"{k} x{v}" for k, v in bb.lower_edge.value_counts().items()))
        P("    upper edges: " + ", ".join(f"{k} x{v}" for k, v in bb.upper_edge.value_counts().items()))
    P("\n    fail-reason census over ALL 850 cells at 10 bps (first token counts once per cell):")
    fc = G[G.cost_bps == COST_MAIN].fail4b.value_counts().head(12)
    for k, v in fc.items():
        P(f"      {k:20s} {v}")
    P("\n    per-leg failure rate over the 850 cells at 10 bps:")
    for leg in LEGS:
        n = int(G[G.cost_bps == COST_MAIN].fail4b.str.split(",").apply(lambda t: leg in t).sum())
        P(f"      {leg:5s} fails in {n:4d} / 850 cells ({n/850:.0%})")

    # ---------------- rule 8
    P("\n## RULE 8 WALK-FORWARD")
    P("    WF-A  IS-fitted band vs OOS-admissible band, and whether the same legs bind the same edges")
    P(f"    {'book':24s} {'IS band':12s} {'IS edges':22s} {'OOS band':12s} {'OOS edges':22s} same-edges")
    same = 0
    nboth = 0
    for _, r in W.iterrows():
        if r.IS_width == 0 and r.OOS_width == 0:
            continue
        isb = "-" if r.IS_width == 0 else f"{r.IS_lo:.2f}-{r.IS_hi:.2f}"
        osb = "-" if r.OOS_width == 0 else f"{r.OOS_lo:.2f}-{r.OOS_hi:.2f}"
        s = (r.IS_lower == r.OOS_lower and r.IS_upper == r.OOS_upper) if (r.IS_width and r.OOS_width) else None
        if r.IS_width and r.OOS_width:
            nboth += 1
            same += bool(s)
        P(f"    {r.book:24s} {isb:12s} {(r.IS_lower+' / '+r.IS_upper)[:22]:22s} {osb:12s} "
          f"{(r.OOS_lower+' / '+r.OOS_upper)[:22]:22s} {'' if s is None else s}")
    P(f"    same legs bind the same edges in {same}/{nboth} books admissible in both windows")

    P("\n    WF-B  gross chosen by IS Sharpe alone per book, OOS read ONCE (10 bps):")
    P(f"    {'book':24s} {'g*':5s} {'IS Sh':6s} {'OOS CAGR':9s} {'OOS Sh':7s} {'OOS DD':8s} | "
      f"{'SPY CAGR':9s} {'SPY Sh':7s} {'SPY DD':8s} | {'v2 CAGR':8s} {'v2 Sh':6s}")
    for _, r in W.iterrows():
        P(f"    {r.book:24s} {r.g_isbest:<5.2f} {r.IS_Sharpe:<6.2f} {r.OOS_CAGR:<9.2%} {r.OOS_Sharpe:<7.2f} "
          f"{r.OOS_MaxDD:<8.1%} | {r.OOS_CAGR_spy:<9.2%} {r.OOS_Sharpe_spy:<7.2f} {r.OOS_MaxDD_spy:<8.1%} | "
          f"{r.OOS_CAGR_base:<8.2%} {r.OOS_Sharpe_base:<6.2f}")
    kbest = W.IS_Sharpe.idxmax()
    r = W.loc[kbest]
    P(f"\n    single best IS-Sharpe (book, gross) over the whole grid: {r.book} @ g={r.g_isbest:.2f} "
      f"(IS Sharpe {r.IS_Sharpe:.2f})")
    P(f"      OOS read ONCE: CAGR {r.OOS_CAGR:.2%} Sharpe {r.OOS_Sharpe:.2f} MaxDD {r.OOS_MaxDD:.1%}  "
      f"vs SPY {r.OOS_CAGR_spy:.2%} / {r.OOS_Sharpe_spy:.2f} / {r.OOS_MaxDD_spy:.1%}  "
      f"vs RULES v2 {r.OOS_CAGR_base:.2%} / {r.OOS_Sharpe_base:.2f} / {r.OOS_MaxDD_base:.1%}")

    g10 = G[G.cost_bps == COST_MAIN]

    # ---------------- WF-C (POST-HOC, declared as such)
    P("\n    WF-C  POST-HOC ARM - ADDED AFTER WF-A AND WF-B WERE READ, and reported as post-hoc, not")
    P("          as a pre-registered result.  WF-B picks gross by IS Sharpe alone, and because the")
    P("          Sharpe legs are near-invariant in gross (G4) that rule is close to arbitrary and lands")
    P("          at the grid top for almost every book.  WF-C states the alternative IS rule the band")
    P("          itself suggests - 'gross = the MIDPOINT of the IS-admissible 4b band' - and reads the")
    P("          OOS window ONCE at that gross.  It is a different selection rule, not a re-read.")
    P(f"    {'book':24s} {'g_mid':6s} {'OOS CAGR':9s} {'OOS Sh':7s} {'OOS DD':8s} {'OOS 4b legs failing':22s}")
    nmid = nmid_pass = 0
    for _, r in W.iterrows():
        if not r.IS_width:
            continue
        gmid = GGRID[int(round((GGRID.index(round(r.IS_lo, 2)) + GGRID.index(round(r.IS_hi, 2))) / 2))]
        c = g10[(g10.book == r.book) & (np.isclose(g10.gross, gmid))].iloc[0]
        nmid += 1
        nmid_pass += bool(c.OOS_pass4b)
        P(f"    {r.book:24s} {gmid:<6.2f} {c.OOS_CAGR:<9.2%} {c.OOS_Sharpe:<7.2f} {c.OOS_MaxDD:<8.1%} "
          f"{(c.OOS_fail4b if not c.OOS_pass4b else 'PASSES 4b in OOS'):22s}")
    P(f"    IS-band-midpoint gross passes the four in-window 4b legs OOS in {nmid_pass}/{nmid} books "
      f"(the OOS leg itself is undefined inside the OOS window and is stated, not dropped).")

    # ---------------- keep paths
    n4a, n4b = int(g10.pass4a.sum()), int(g10.pass4b.sum())
    nboth_c = int((g10.pass4a & g10.pass4b).sum())
    P(f"\n## KEEP PATHS over the {len(g10)} cells at 10 bps: 4a {n4a} | 4b {n4b} | BOTH {nboth_c}")
    kp = g10[["book", "gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe",
              "pass4a", "pass4b", "fail4b"]]
    kp.to_csv(OUT / f"{STAMP}.keeppaths.csv", index=False)
    if n4b:
        P("    4b-passing cells:")
        for _, c in g10[g10.pass4b].iterrows():
            P(f"      {c.book:24s} g={c.gross:.2f} CAGR {c.CAGR:.2%} Sharpe {c.Sharpe:.2f} "
              f"MaxDD {c.MaxDD:.1%} halves {c.H1:.2f}/{c.H2:.2f} OOS Sh {c.OOS_Sharpe:.2f} 4a={c.pass4a}")
    P(f"\nSURVIVORSHIP: all five panels are CURRENT constituents; every CAGR above is biased upward "
      f"and every CAGR-floor pass is easier than on a point-in-time panel.")
    P(f"\ndone in {time.time()-t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()

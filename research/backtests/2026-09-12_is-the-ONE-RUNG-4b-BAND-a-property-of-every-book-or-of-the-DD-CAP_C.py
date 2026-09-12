#!/usr/bin/env python3
"""Idea 804 (lane C, 2026-09-12) - is-the-ONE-RUNG-4b-BAND-a-property-of-every-book-or-of-the-DD-CAP.

QUESTION
--------
Idea 574 swept the ten most-cited unswept 4b passes over 17 gross rungs and found (a) only five of
the ten pass 4b at ANY gross, (b) among those five the admissible band has a MEDIAN WIDTH OF ONE
RUNG, (c) the pass set is contiguous in g in every case, and (d) at the IS-Sharpe-optimal g = 1.00
every Sharpe-clearing book dies on the drawdown cap alone.

That is a suggestive shape but it was never decomposed.  PROTOCOL 4b is a conjunction of FIVE
legs - Sharpe > SPY in H1, in H2, and out-of-sample, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's -
and "the band" is the intersection of five per-leg admissible g-sets.  The queue's reading is that
the band is really just TWO of those five legs meeting: the DD cap cutting the band from above (more
gross -> deeper drawdown) and the CAGR floor cutting it from below (less gross -> less return), with
the three Sharpe legs never binding at either edge.  If that is right, the "one rung" is not a
property of any book: it is an arithmetic property of the 4b bar itself, and every book on the
record inherits it.

This run tests that directly, on a WIDER and PRE-DECLARED book set rather than on ten books the
record happened to cite.

WHAT COUNTS AS WHAT (every rule stated before any number)
---------------------------------------------------------
* A **book** is (panel, form, n, cadence).  Gross is NOT part of the book here - it is the dial.
* A **leg** is one of the five PROTOCOL-4b conditions, computed verbatim as in idea 574's
  `fail_4b`: H1, H2, OOS (Sharpe > SPY's, on that window), DD (MaxDD >= 0.60 * SPY's MaxDD, both
  negative), CAGR (CAGR >= 0.70 * SPY's CAGR).
* A leg's **admissible set** is the set of gross rungs at which THAT LEG ALONE passes.  The 4b
  **band** is the intersection of all five.  Both are read off the same 60 x 17 grid.
* A leg's **shape** over the ladder is classified as LOWER (a prefix {g <= x}), UPPER (a suffix
  {g >= x}), ALL, NONE, or NONMONO (anything else).  The classification is mechanical, not eyeballed.
* A leg is **SLACK** for a book when dropping it leaves the band unchanged; it is **BINDING AT THE
  LOWER EDGE** when it fails at the rung immediately below the band, and **BINDING AT THE UPPER
  EDGE** when it fails at the rung immediately above.  An edge that is the end of the ladder is
  reported as CENSORED, never counted as bound by anything.
* **DD-CAGR SUFFICIENCY**: the band equals (DD set) intersect (CAGR set).  This is the queue's
  "nothing else in play", made into a testable equality on the actual rung sets.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two - the queue's own: book set, gross)
    1. BOOK SET  5 panels (U56, ETF36, B136, BSTK100, SMALL) x 6 forms (EWALL, MA-DG, MA-RS,
                 BAND3, CAND20, R620) x 2 cadences (W, M) = 60 books, declared in full before any
                 result is read.  ALL 60 reported, pass or fail, no post-hoc filtering.
    2. GROSS     17 rungs, g = 0.20, 0.25, ..., 1.00 - idea 574's ladder, unchanged.
REPORTED-NEVER-SELECTED: cost rung (10 bps per PROTOCOL, 25 bps beside it), panel, form, cadence,
window (FULL / IS / OOS), and the 4a path.

GATES (printed before any band or leg number is read)
    G1 engine    : fast_backtest vs engine.backtest on one book.                     bar 1e-9
    G2 linearity : build_weights(g) == g * build_weights(1.0) for every form.  The whole grid is
                   computed by scaling a unit-gross weight matrix, so this must hold exactly or the
                   grid is wrong.                                                   bar 1e-12
    G3 comparands: RULES v2 (U56, live) and SPY over this run's window, with the four 4b bars
                   printed as numbers so every later verdict can be checked by hand.   no bar
    G4 continuity: idea 574's five band-carrying books re-read here, band width beside the width
                   574 published.  MEASURED, NOT GATED - 574 pinned books out of leaderboard prose
                   and this run declares them, so an exact match is not expected; a gross
                   disagreement would invalidate the comparison and is reported either way.

PRE-REGISTERED HYPOTHESES (written before any grid point was read)
    H_SUFF  : the queue's reading - for >= 70% of books with a NON-EMPTY band, the band equals
              (DD set) intersect (CAGR set) exactly, i.e. the three Sharpe legs are slack.
    H_UPPER : every non-empty band's upper edge, when not censored, is bound by DD.
    H_LOWER : every non-empty band's lower edge, when not censored, is bound by CAGR.
    H_SHAPE : DD's admissible set is LOWER-shaped and CAGR's is UPPER-shaped for >= 90% of books -
              the monotonicity the queue's reading silently assumes.
    H_NARROW: idea 574's "one rung" replicates on the wider set - median band width <= 2 of 17
              rungs among books that pass anywhere.
    H_WF    : rule 8 - the BINDING-LEG IDENTITY walks forward: the (lower, upper) binding-leg pair
              read on IS alone matches the pair read on OOS alone for >= 60% of books with a
              non-empty band in both windows.
    H_ARITH : the strong form - if only DD and CAGR are in play and both are proportional to
              gross, the band is computable in CLOSED FORM from the g = 1.00 cell alone,
              g_lo* = 0.70 * CAGR_SPY / CAGR(1.00) and g_hi* = 0.60 * MaxDD_SPY / MaxDD(1.00).
              Bar: the predicted band matches the measured band EXACTLY for >= 70% of 60 books.
              This consumes 1 of the 17 rungs and predicts the other 16.

RULE 8 WALK-FORWARD (required, and run whatever the verdict)
    IS = ..2016-12-31, OOS = 2017-01-01.., OOS read ONCE.
    WF-A on the ANSWER: the five legs, per-leg sets, band and binding legs are recomputed inside IS
       alone and inside OOS alone.  (Inside a window the OOS leg collapses into that window's own
       second half; that is stated, not hidden.)  Agreement of the binding-leg pair is the
       walk-forward of "the band is the DD cap meeting the CAGR floor".
    WF-B on a BOOK: two selectors, both fitted on IS ONLY, then read ONCE on OOS -
       (i) IS-BAND-MIDPOINT: the book+gross at the midpoint of the widest IS-admissible band;
       (ii) IS-SHARPE: the book+gross with the best IS Sharpe (574's selector, which walked every
            book past its own band to g = 1.00).
       OOS CAGR / Sharpe / MaxDD reported against RULES v2 (live) and SPY, both OOS.

KEEP PATHS: 4a and 4b evaluated at every one of the 60 x 17 x 2 = 2,040 cells and counted.

SURVIVORSHIP: U56 / ETF36 / B136 / BSTK100 are current constituents of universe.json /
    universe_broad.json; SMALL is the current constituent list of its screen with every ticker whose
    max_1d_move >= 1.0 in data/small_meta.csv dropped first, per PROTOCOL.  Dead names are absent
    from all of them, so every CAGR here is biased upward and every 4b CAGR-floor pass is EASIER
    than on a point-in-time panel - which makes the CAGR leg look LESS binding than it truly is.

PROTOCOL: 10 bps per unit turnover, next-day fills (engine), no shorting, no leverage.
Deterministic, standalone, no network.  Modifies nothing but its own outputs:
    .grid.csv .legs.csv .bands.csv .walkforward.csv .keeppaths.csv .console.txt
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

STAMP = "2026-09-12_is-the-ONE-RUNG-4b-BAND-a-property-of-every-book-or-of-the-DD-CAP_C"
OUT = ROOT / "research" / "backtests"

COST_MAIN, COST_ALT = 10.0, 25.0
GGRID = [round(0.20 + 0.05 * i, 2) for i in range(17)]      # TUNED 2 - 17 rungs
IS_END, OOS_START = "2016-12-31", "2017-01-01"
MAX_VOL, MA_WIN, TOL = 0.60, 200, 1e-9
LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]

# TUNED 1 - the book set, declared in full before any result is read
PANEL_KEYS = ["U56", "ETF36", "B136", "BSTK100", "SMALL"]
FORMS = [("EWALL", 0), ("MA-DG", 0), ("MA-RS", 0), ("BAND", 3), ("CAND", 20), ("R6", 20)]
FREQS = ["W", "M"]

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


# ------------------------------------------------------------------ vectorised runner (574's)
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


def rowify(r):
    m = metrics(r)
    h1, h2 = halves(r)
    mi, mo = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])


def keep_4a(r, b):
    a1, a2 = halves(r)
    b1, b2 = halves(b)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(b)["MaxDD"])


def legs_4b(r, spy):
    """PROTOCOL 4b as FIVE separate booleans (True = that leg passes).  Identical arithmetic to
    idea 574's fail_4b, only decomposed."""
    a1, a2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    return {"H1": bool(a1 > s1), "H2": bool(a2 > s2),
            "OOS": bool(metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"]),
            "DD": bool(m["MaxDD"] >= 0.60 * ms["MaxDD"]),
            "CAGR": bool(m["CAGR"] >= 0.70 * ms["CAGR"])}


def legs_4b_window(r, spy, lo=None, hi=None):
    """The same five legs INSIDE one window.  The OOS leg collapses into that window's own second
    half (it is the same object as H2 there); reported under its own name and stated as such."""
    rr, ss = r.loc[lo:hi], spy.loc[lo:hi]
    a1, a2 = halves(rr)
    s1, s2 = halves(ss)
    m, ms = metrics(rr), metrics(ss)
    return {"H1": bool(a1 > s1), "H2": bool(a2 > s2), "OOS": bool(a2 > s2),
            "DD": bool(m["MaxDD"] >= 0.60 * ms["MaxDD"]),
            "CAGR": bool(m["CAGR"] >= 0.70 * ms["CAGR"])}


# ------------------------------------------------------------------ set algebra on the ladder
def shape_of(idxs, n):
    """Classify a set of rung indices as LOWER (prefix), UPPER (suffix), ALL, NONE, NONMONO."""
    s = sorted(idxs)
    if not s:
        return "NONE"
    if len(s) == n:
        return "ALL"
    if s == list(range(len(s))):
        return "LOWER"
    if s == list(range(n - len(s), n)):
        return "UPPER"
    return "NONMONO"


def band_of(legsets, n, use=LEGS):
    """Intersection of the named leg sets, as a sorted rung-index list."""
    out = set(range(n))
    for L in use:
        out &= legsets[L]
    return sorted(out)


def edges(band, legsets, n):
    """Which legs fail at the rung just below / just above the band.  '' = censored (ladder end)."""
    if not band:
        return "", "", True
    lo, hi = band[0], band[-1]
    below = "" if lo == 0 else "+".join(L for L in LEGS if (lo - 1) not in legsets[L])
    above = "" if hi == n - 1 else "+".join(L for L in LEGS if (hi + 1) not in legsets[L])
    contig = (band == list(range(lo, hi + 1)))
    return below, above, contig


# ------------------------------------------------------------------ panels and books (574's)
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
    if form == "BAND":
        w = rules_v2_weights(px[cols + (["SPY"] if "SPY" in px.columns and "SPY" not in cols
                                        else [])], band=n / 100.0, gross=g)
        return w.reindex(columns=px.columns).fillna(0.0).where(pm, 0.0)
    if form == "CAND":
        s, above, vol20 = score(px)
        s = s.where(pm)
        elig = s.where(above & (vol20 < MAX_VOL))
        rk = elig.rank(axis=1, ascending=False)
        return (rk <= n).astype(float) * (g / n)
    if form == "R6":
        r6 = (px / px.shift(126) - 1.0).where(pm)
        rk = r6.rank(axis=1, ascending=False)
        return (rk <= n).astype(float) * (g / n)
    raise ValueError(form)


def fmt_ladder(setidx, n):
    return "".join("P" if i in setidx else "." for i in range(n))


def main():
    t0 = time.time()
    P("=" * 118)
    P(f"# {STAMP}")
    P("# IDEA 804 - decompose the 4b gross band leg by leg over a WIDER, PRE-DECLARED book set:")
    P("#            which of the five 4b legs binds at each end of each band, and is 'the band'")
    P("#            really the DD cap's upper edge meeting the CAGR floor's lower edge?")
    P("=" * 118)
    P(f"# PROTOCOL: {COST_MAIN:.0f} bps per unit turnover ({COST_ALT:.0f} bps reported beside it),")
    P(f"#           next-day fills, no shorting, no leverage.  IS <= {IS_END}, OOS >= {OOS_START}.")
    P(f"# TUNED (2, the queue's own): BOOK SET ({len(PANEL_KEYS)} panels x {len(FORMS)} forms x "
      f"{len(FREQS)} cadences = {len(PANEL_KEYS) * len(FORMS) * len(FREQS)} books) x GROSS "
      f"({len(GGRID)} rungs {GGRID[0]:.2f}..{GGRID[-1]:.2f}).")
    P("# REPORTED-NOT-SELECTED: cost rung, panel, form, cadence, window, the 4a path.")
    P("")
    P("PRE-REGISTERED: H_SUFF (band == DD n CAGR for >=70% of banded books), H_UPPER (upper edge")
    P("  always DD-bound where not censored), H_LOWER (lower edge always CAGR-bound where not")
    P("  censored), H_SHAPE (DD LOWER-shaped and CAGR UPPER-shaped in >=90% of books), H_NARROW")
    P("  (median band <= 2 of 17 rungs), H_WF (binding-leg pair agrees IS vs OOS in >=60%).")
    P("")

    # ------------------------------------------------------------------ panels, comparands, gates
    PAN, n_bad, n_small = panels()
    P("=" * 118)
    P("PANELS, COMPARANDS, GATES")
    P("=" * 118)
    P("  " + "; ".join(f"{k} {len(v[1])} tradable / {v[0].shape[1]} cols" for k, v in PAN.items()))
    P(f"  small panel: {n_bad} tickers with max_1d_move >= 1.0 dropped per PROTOCOL, "
      f"{n_small} tradable")
    P("  SURVIVORSHIP: all five panels are CURRENT constituents; dead names are absent, so every")
    P("  CAGR below is biased upward and the CAGR leg is therefore EASIER here than on a")
    P("  point-in-time panel - the bias works AGAINST this run's CAGR-floor finding, not for it.")
    px56 = PAN["U56"][0]
    base_full = fast_backtest(px56, rules_v2_weights(px56), COST_MAIN, "W")
    START = px56.index[260]
    b_ret = base_full.loc[START:]
    spy_ret = px56["SPY"].pct_change().fillna(0.0).loc[START:]
    bm, sm = rowify(b_ret), rowify(spy_ret)

    w_test = build_weights(px56, PAN["U56"][1], "CAND", 20, 0.75)
    r1 = fast_backtest(px56, w_test, COST_MAIN, "W")
    r2 = backtest(px56, w_test, cost_bps=COST_MAIN, freq="W")["returns"]
    d1 = float(np.abs(r1 - r2).max())
    P("")
    P(f"  G1 engine    : max |fast_backtest - engine.backtest| on U56/CAND20/g0.75  {d1:.3e}"
      f"   bar 1e-9 -> {'PASS' if d1 < TOL else 'FAIL'}")
    dlin = 0.0
    for form, nn in FORMS:
        w1 = build_weights(px56, PAN["U56"][1], form, nn, 1.0)
        for g in (0.20, 0.55, 0.90):
            dlin = max(dlin, float(np.abs(build_weights(px56, PAN["U56"][1], form, nn, g)
                                          - g * w1).max().max()))
    P(f"  G2 linearity : max |w(g) - g*w(1)| over all {len(FORMS)} forms x 3 grosses  {dlin:.3e}"
      f"   bar 1e-12 -> {'PASS' if dlin < 1e-12 else 'FAIL'}")
    if dlin >= 1e-12:
        P("     G2 FAILED - the unit-gross scaling shortcut is invalid; aborting rather than")
        P("     publishing a grid built on a false assumption.")
        (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")
        return
    P(f"  G3 comparands over {START.date()}..{px56.index[-1].date()} ({len(b_ret)} bars):")
    P(f"     RULES v2 (U56, live)  CAGR {bm['CAGR']:.2%}  Sharpe {bm['Sharpe']:.4f}  "
      f"MaxDD {bm['MaxDD']:.2%}  halves {bm['H1']:.4f}/{bm['H2']:.4f}  | OOS "
      f"{bm['OOS_CAGR']:.2%}/{bm['OOS_Sharpe']:.4f}/{bm['OOS_MaxDD']:.2%}")
    P(f"     SPY                   CAGR {sm['CAGR']:.2%}  Sharpe {sm['Sharpe']:.4f}  "
      f"MaxDD {sm['MaxDD']:.2%}  halves {sm['H1']:.4f}/{sm['H2']:.4f}  | OOS "
      f"{sm['OOS_CAGR']:.2%}/{sm['OOS_Sharpe']:.4f}/{sm['OOS_MaxDD']:.2%}")
    P(f"     the five 4b bars: H1 Sharpe > {sm['H1']:.4f}, H2 Sharpe > {sm['H2']:.4f}, "
      f"OOS Sharpe > {sm['OOS_Sharpe']:.4f},")
    P(f"                       MaxDD >= {0.60 * sm['MaxDD']:.2%}, CAGR >= {0.70 * sm['CAGR']:.2%}"
      "   (bars are panel-specific: each book is judged against SPY on ITS OWN window)")
    P("")

    # ------------------------------------------------------------------ the grid
    nb = len(PANEL_KEYS) * len(FORMS) * len(FREQS)
    P("=" * 118)
    P(f"THE GRID - {nb} books x {len(GGRID)} gross rungs x 2 cost rungs = "
      f"{nb * len(GGRID) * 2} cells, all reported in .grid.csv")
    P("=" * 118)
    grid = []
    bid = 0
    for pk in PANEL_KEYS:
        px, tr = PAN[pk]
        st = px.index[260]
        spy_b = px["SPY"].pct_change().fillna(0.0).loc[st:]
        base_b = base_full.reindex(px.index).fillna(0.0).loc[st:]
        for form, nn in FORMS:
            w1 = build_weights(px, tr, form, nn, 1.0)          # G2 licenses the scaling below
            for freq in FREQS:
                bid += 1
                key = f"{pk}/{form}{nn or ''}/{freq}"
                for cost in (COST_MAIN, COST_ALT):
                    for gi, g in enumerate(GGRID):
                        r = fast_backtest(px, g * w1, cost, freq).loc[st:]
                        L = legs_4b(r, spy_b)
                        LI = legs_4b_window(r, spy_b, None, IS_END)
                        LO = legs_4b_window(r, spy_b, OOS_START, None)
                        grid.append(dict(book=bid, key=key, panel=pk, form=form, n=nn, freq=freq,
                                         cost=cost, gi=gi, g=g,
                                         keep4b=all(L.values()), keep4a=keep_4a(r, base_b),
                                         **{f"leg_{k}": v for k, v in L.items()},
                                         **{f"IS_leg_{k}": v for k, v in LI.items()},
                                         **{f"OOS_leg_{k}": v for k, v in LO.items()},
                                         **rowify(r)))
        P(f"  panel {pk:8s} done  t={time.time() - t0:6.1f}s  cells so far {len(grid)}")
    GR = pd.DataFrame(grid)
    GR.to_csv(f"{OUT}/{STAMP}.grid.csv", index=False)
    P(f"  grid complete: {len(GR)} cells in {time.time() - t0:.1f}s")
    P("")

    # ------------------------------------------------------------------ leg decomposition
    P("=" * 118)
    P("LEG DECOMPOSITION - each leg's own admissible gross set, and the band as their intersection")
    P("=" * 118)
    P(f"  ladder columns are g = {GGRID[0]:.2f} .. {GGRID[-1]:.2f} step 0.05 (17 rungs); "
      "'P' = that leg passes at that rung.")
    P("")
    n = len(GGRID)
    legrows, bandrows = [], []
    for (bid_, key), sub in GR[GR.cost == COST_MAIN].groupby(["book", "key"], sort=True):
        sub = sub.sort_values("gi")
        sets = {L: set(sub.loc[sub[f"leg_{L}"], "gi"].astype(int)) for L in LEGS}
        band = band_of(sets, n)
        below, above, contig = edges(band, sets, n)
        ddc = sorted(sets["DD"] & sets["CAGR"])
        for L in LEGS:
            legrows.append(dict(book=bid_, key=key, leg=L, shape=shape_of(sets[L], n),
                                n_pass=len(sets[L]), ladder=fmt_ladder(sets[L], n),
                                slack=bool(band_of(sets, n, [x for x in LEGS if x != L]) == band)))
        row = sub.iloc[0]
        bandrows.append(dict(
            book=bid_, key=key, panel=row.panel, form=row.form, freq=row.freq,
            band_w=len(band), band_lo=GGRID[band[0]] if band else np.nan,
            band_hi=GGRID[band[-1]] if band else np.nan, contiguous=contig,
            ladder=fmt_ladder(band, n), dd_cagr_w=len(ddc),
            dd_cagr_ladder=fmt_ladder(ddc, n), suff=bool(ddc == band),
            bind_lo=below or ("CENSORED" if band else ""),
            bind_hi=above or ("CENSORED" if band else ""),
            slack_legs="+".join(L for L in LEGS
                                if band_of(sets, n, [x for x in LEGS if x != L]) == band),
            n4a=int(sub.keep4a.sum())))
    LGS, BD = pd.DataFrame(legrows), pd.DataFrame(bandrows)
    LGS.to_csv(f"{OUT}/{STAMP}.legs.csv", index=False)
    BD.to_csv(f"{OUT}/{STAMP}.bands.csv", index=False)

    P("  LEG SHAPES over all 60 books (a leg's admissible set as a function of gross):")
    sh = LGS.pivot_table(index="leg", columns="shape", values="book", aggfunc="count").fillna(0)
    sh = sh.reindex(LEGS)
    P("    " + sh.astype(int).to_string().replace("\n", "\n    "))
    ddl = LGS[(LGS.leg == "DD")]
    cal = LGS[(LGS.leg == "CAGR")]
    dd_ok = int(ddl["shape"].isin(["LOWER", "ALL", "NONE"]).sum())
    ca_ok = int(cal["shape"].isin(["UPPER", "ALL", "NONE"]).sum())
    P(f"    DD   set is LOWER/ALL/NONE-shaped (falls as gross rises) in {dd_ok} of {len(ddl)} books")
    P(f"    CAGR set is UPPER/ALL/NONE-shaped (rises with gross)      in {ca_ok} of {len(cal)} books")
    P(f"    H_SHAPE (both >= 90%): {'PASS' if dd_ok >= 0.9 * len(ddl) and ca_ok >= 0.9 * len(cal) else 'FAIL'}")
    P("")
    P("  PER-BOOK BANDS (4b at 10 bps).  'band' = all five legs; 'DDnCAGR' = only those two.")
    P(f"  {'#':>2s} {'book':24s} {'band ladder (17 rungs)':22s} {'w':>2s} "
      f"{'DDnCAGR ladder':22s} {'=':>1s} {'binds lo':>12s} {'binds hi':>12s} {'slack':>14s}")
    for _, r in BD.iterrows():
        P(f"  {r.book:2d} {r.key:24s} {r.ladder:22s} {r.band_w:2d} {r.dd_cagr_ladder:22s} "
          f"{'Y' if r.suff else 'n':>1s} {r.bind_lo or '-':>12s} {r.bind_hi or '-':>12s} "
          f"{r.slack_legs or '-':>14s}")
    P("")

    nz = BD[BD.band_w > 0]
    P("=" * 118)
    P("THE ANSWER")
    P("=" * 118)
    P(f"  books with a NON-EMPTY 4b band : {len(nz)} of {len(BD)}")
    if len(nz):
        P(f"  band width (rungs of 17)       : median {nz.band_w.median():.1f}  "
          f"mean {nz.band_w.mean():.2f}  min {nz.band_w.min()}  max {nz.band_w.max()}")
        P(f"  contiguous in g                : {int(nz.contiguous.sum())} of {len(nz)}")
        nsuff = int(nz.suff.sum())
        P(f"  H_SUFF  band == DD n CAGR      : {nsuff} of {len(nz)} "
          f"({nsuff / len(nz):.0%})  -> {'PASS' if nsuff >= 0.70 * len(nz) else 'FAIL'} (bar 70%)")
        lo_c = nz.bind_lo.value_counts()
        hi_c = nz.bind_hi.value_counts()
        P(f"  lower-edge binding leg census  : {dict(lo_c)}")
        P(f"  upper-edge binding leg census  : {dict(hi_c)}")
        lo_u = nz[nz.bind_lo != "CENSORED"]
        hi_u = nz[nz.bind_hi != "CENSORED"]
        lo_cagr = int((lo_u.bind_lo == "CAGR").sum())
        hi_dd = int((hi_u.bind_hi == "DD").sum())
        P(f"  H_LOWER uncensored lower edges bound by CAGR ALONE: {lo_cagr} of {len(lo_u)} -> "
          f"{'PASS' if len(lo_u) and lo_cagr == len(lo_u) else 'FAIL'}")
        P(f"  H_UPPER uncensored upper edges bound by DD ALONE  : {hi_dd} of {len(hi_u)} -> "
          f"{'PASS' if len(hi_u) and hi_dd == len(hi_u) else 'FAIL'}")
        P(f"  H_NARROW median band <= 2 rungs: median {nz.band_w.median():.1f} -> "
          f"{'PASS' if nz.band_w.median() <= 2 else 'FAIL'}")
        sl = LGS[LGS.book.isin(nz.book)].groupby("leg").slack.mean().reindex(LEGS)
        P("  per-leg SLACK rate among banded books (1.00 = that leg never changes the band):")
        P("    " + "  ".join(f"{L} {sl[L]:.2f}" for L in LEGS))
    else:
        P("  no book has a non-empty 4b band at 10 bps; H_SUFF / H_UPPER / H_LOWER / H_NARROW are")
        P("  VACUOUS and are reported as such, not as passes.")
    P("")
    # ---------------------------------------------------- the band as a closed form (H_ARITH)
    P("=" * 118)
    P("H_ARITH - if the band is only DD meeting CAGR, ONE backtest should predict it")
    P("=" * 118)
    P("  Pre-registered before reading: if the three Sharpe legs are gross-invariant and the two")
    P("  LEVEL legs are proportional to gross, then from the g=1.00 cell ALONE plus SPY,")
    P("      g_lo* = 0.70 * CAGR_SPY / CAGR(1.00)      g_hi* = 0.60 * MaxDD_SPY / MaxDD(1.00)")
    P("  and the band is the rungs in [g_lo*, g_hi*] whenever no Sharpe leg is dead.  This uses")
    P("  1 of the 17 rungs, so it is a PREDICTION of the other 16, not a restatement.")
    P("  H_ARITH: the predicted band equals the measured band exactly for >= 70% of 60 books.")
    ar = []
    for pk in PANEL_KEYS:
        px_, _ = PAN[pk]
        st_ = px_.index[260]
        sp_ = rowify(px_["SPY"].pct_change().fillna(0.0).loc[st_:])
        for (bid_, key), sub in GR[(GR.cost == COST_MAIN) & (GR.panel == pk)].groupby(
                ["book", "key"], sort=True):
            sub = sub.sort_values("gi")
            top = sub.iloc[-1]
            sets = {L: set(sub.loc[sub[f"leg_{L}"], "gi"].astype(int)) for L in LEGS}
            meas = band_of(sets, n)
            dead = any(len(sets[L]) == 0 for L in ("H1", "H2", "OOS"))
            glo = 0.70 * sp_["CAGR"] / top.CAGR if top.CAGR > 0 else np.inf
            ghi = 0.60 * sp_["MaxDD"] / top.MaxDD if top.MaxDD < 0 else np.inf
            pred = [] if dead else [i for i, g in enumerate(GGRID) if glo - 1e-12 <= g <= ghi + 1e-12]
            ar.append(dict(book=bid_, key=key, g_lo_star=glo, g_hi_star=ghi,
                           sharpe_leg_dead=dead, pred=fmt_ladder(pred, n),
                           meas=fmt_ladder(meas, n), exact=bool(pred == meas),
                           d_lo=(pred[0] - meas[0]) if (pred and meas) else np.nan,
                           d_hi=(pred[-1] - meas[-1]) if (pred and meas) else np.nan))
    AR = pd.DataFrame(ar)
    AR.to_csv(f"{OUT}/{STAMP}.arith.csv", index=False)
    ex = int(AR.exact.sum())
    P(f"  exact band match from one cell: {ex} of {len(AR)} ({ex / len(AR):.0%}) -> "
      f"{'PASS' if ex >= 0.70 * len(AR) else 'FAIL'} (bar 70%)")
    both_ = AR.dropna(subset=["d_lo"])
    if len(both_):
        P(f"  edge error in RUNGS over the {len(both_)} books non-empty in both: lower median "
          f"{both_.d_lo.median():.1f} (|err|<=1 in {int((both_.d_lo.abs() <= 1).sum())}), upper "
          f"median {both_.d_hi.median():.1f} (|err|<=1 in {int((both_.d_hi.abs() <= 1).sum())})")
    P("  the 8 largest misses (predicted vs measured):")
    for _, r in AR[~AR.exact].head(8).iterrows():
        P(f"    {r.key:24s} pred {r.pred}  meas {r.meas}  g*=[{r.g_lo_star:.2f},{r.g_hi_star:.2f}]")
    P("")
    P("  G4 CONTINUITY (measured, not gated) - idea 574's banded books as declared here:")
    for k in ["U56/CAND20/M", "U56/EWALL/W", "U56/CAND20/W", "B136/EWALL/W", "B136/MA-DG/W"]:
        m = BD[BD.key == k]
        if len(m):
            r = m.iloc[0]
            P(f"    {k:18s} band {r.ladder}  w={r.band_w}  "
              f"({r.band_lo if r.band_w else '-'}..{r.band_hi if r.band_w else '-'})")
    P("    574 published widths 2 / 1 / 1 / 0 / 0 for these five at their own pinned definitions;")
    P("    this run DECLARES the books rather than pinning them from prose, so exact agreement is")
    P("    not expected and is not claimed.")
    P("")

    # ------------------------------------------------------------------ rule 8
    P("=" * 118)
    P("RULE 8 WALK-FORWARD")
    P("=" * 118)
    P(f"  IS <= {IS_END}; OOS >= {OOS_START}, read ONCE.  Inside a window the OOS leg IS that")
    P("  window's own H2 (stated, not hidden), so a window band is the intersection of four")
    P("  distinct legs, not five.")
    P("")
    wf = []
    for (bid_, key), sub in GR[GR.cost == COST_MAIN].groupby(["book", "key"], sort=True):
        sub = sub.sort_values("gi")
        d = {}
        for tag, pre in (("IS", "IS_leg_"), ("OOS", "OOS_leg_")):
            sets = {L: set(sub.loc[sub[f"{pre}{L}"], "gi"].astype(int)) for L in LEGS}
            b = band_of(sets, n)
            lo, hi, ct = edges(b, sets, n)
            d[tag] = dict(band=b, lo=lo or ("CENSORED" if b else ""),
                          hi=hi or ("CENSORED" if b else ""), ladder=fmt_ladder(b, n),
                          suff=bool(sorted(sets["DD"] & sets["CAGR"]) == b), contig=ct)
        both = bool(d["IS"]["band"] and d["OOS"]["band"])
        wf.append(dict(book=bid_, key=key, IS_ladder=d["IS"]["ladder"], IS_w=len(d["IS"]["band"]),
                       IS_lo=d["IS"]["lo"], IS_hi=d["IS"]["hi"], IS_suff=d["IS"]["suff"],
                       OOS_ladder=d["OOS"]["ladder"], OOS_w=len(d["OOS"]["band"]),
                       OOS_lo=d["OOS"]["lo"], OOS_hi=d["OOS"]["hi"], OOS_suff=d["OOS"]["suff"],
                       both=both,
                       pair_agree=bool(both and d["IS"]["lo"] == d["OOS"]["lo"]
                                       and d["IS"]["hi"] == d["OOS"]["hi"]),
                       overlap=len(set(d["IS"]["band"]) & set(d["OOS"]["band"])),
                       IS_mid=GGRID[d["IS"]["band"][len(d["IS"]["band"]) // 2]] if d["IS"]["band"] else np.nan))
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}/{STAMP}.walkforward.csv", index=False)
    P("  WF-A - the ANSWER walked forward (binding-leg identity), books with a band in BOTH windows:")
    P(f"  {'#':>2s} {'book':24s} {'IS band':20s} {'IS lo/hi':>18s} {'OOS band':20s} "
      f"{'OOS lo/hi':>18s} {'pair':>5s}")
    wb = WF[WF.both]
    for _, r in wb.iterrows():
        P(f"  {r.book:2d} {r.key:24s} {r.IS_ladder:20s} "
          f"{(r.IS_lo or '-') + '/' + (r.IS_hi or '-'):>18s} {r.OOS_ladder:20s} "
          f"{(r.OOS_lo or '-') + '/' + (r.OOS_hi or '-'):>18s} {'Y' if r.pair_agree else 'n':>5s}")
    if len(wb):
        ag = int(wb.pair_agree.sum())
        P(f"  H_WF binding-leg pair agrees IS vs OOS: {ag} of {len(wb)} ({ag / len(wb):.0%}) -> "
          f"{'PASS' if ag >= 0.60 * len(wb) else 'FAIL'} (bar 60%)")
        P(f"  IS-window DD n CAGR sufficiency: {int(WF.IS_suff.sum())} of {len(WF)}; "
          f"OOS-window: {int(WF.OOS_suff.sum())} of {len(WF)}")
    else:
        P("  no book carries a band in BOTH windows; H_WF is VACUOUS and reported as such.")
    P(f"  books with an IS band: {int((WF.IS_w > 0).sum())} of {len(WF)}; "
      f"with an OOS band: {int((WF.OOS_w > 0).sum())} of {len(WF)}")
    P("")

    P("  WF-B - a BOOK chosen on IS ALONE by two selectors, OOS read ONCE (10 bps):")
    ISCELL = GR[GR.cost == COST_MAIN].copy()
    sel = {}
    cand = WF[WF.IS_w > 0]
    if len(cand):
        c = cand.sort_values(["IS_w", "book"], ascending=[False, True]).iloc[0]
        sel["IS-BAND-MIDPOINT"] = (int(c.book), float(c.IS_mid))
    s2 = ISCELL.sort_values("IS_Sharpe", ascending=False).iloc[0]
    sel["IS-SHARPE"] = (int(s2.book), float(s2.g))
    P(f"  comparands OOS: RULES v2 {bm['OOS_CAGR']:.2%} / {bm['OOS_Sharpe']:.4f} / "
      f"{bm['OOS_MaxDD']:.2%}   SPY {sm['OOS_CAGR']:.2%} / {sm['OOS_Sharpe']:.4f} / "
      f"{sm['OOS_MaxDD']:.2%}")
    P(f"  {'selector':18s} {'book':24s} {'g':>5s} {'OOS CAGR':>9s} {'OOS Sharpe':>11s} "
      f"{'OOS MaxDD':>10s} {'4a':>4s} {'4b legs failing OOS':>22s}")
    wfb = []
    for nm, (bk, gg) in sel.items():
        row = ISCELL[(ISCELL.book == bk) & (np.abs(ISCELL.g - gg) < 1e-9)].iloc[0]
        fo = "+".join(L for L in LEGS if not row[f"OOS_leg_{L}"]) or "-"
        P(f"  {nm:18s} {row.key:24s} {gg:5.2f} {row.OOS_CAGR:8.2%} {row.OOS_Sharpe:11.4f} "
          f"{row.OOS_MaxDD:9.2%} {str(bool(row.keep4a)):>4s} {fo:>22s}")
        wfb.append(dict(selector=nm, key=row.key, g=gg, OOS_CAGR=row.OOS_CAGR,
                        OOS_Sharpe=row.OOS_Sharpe, OOS_MaxDD=row.OOS_MaxDD,
                        keep4a=bool(row.keep4a), OOS_fail=fo,
                        base_OOS_Sharpe=bm["OOS_Sharpe"], spy_OOS_Sharpe=sm["OOS_Sharpe"],
                        base_OOS_CAGR=bm["OOS_CAGR"], spy_OOS_CAGR=sm["OOS_CAGR"],
                        base_OOS_MaxDD=bm["OOS_MaxDD"], spy_OOS_MaxDD=sm["OOS_MaxDD"]))
    pd.DataFrame(wfb).to_csv(f"{OUT}/{STAMP}.wfb.csv", index=False)
    P("")

    # ------------------------------------------------------------------ KEEP paths
    P("=" * 118)
    P("KEEP PATHS - both evaluated at every cell (PROTOCOL rule 4)")
    P("=" * 118)
    kp = []
    for cost, sub in GR.groupby("cost"):
        a, b = int(sub.keep4a.sum()), int(sub.keep4b.sum())
        both = int((sub.keep4a & sub.keep4b).sum())
        kp.append(dict(cost=cost, cells=len(sub), keep4a=a, keep4b=b, both=both))
        P(f"  {cost:.0f} bps: {len(sub)} cells | 4a {a} | 4b {b} | BOTH {both}")
    pd.DataFrame(kp).to_csv(f"{OUT}/{STAMP}.keeppaths.csv", index=False)
    m10 = GR[GR.cost == COST_MAIN]
    fc = m10.apply(lambda r: "+".join(L for L in LEGS if not r[f"leg_{L}"]) or "PASS", axis=1)
    P("  fail-4b leg census at 10 bps (which legs fail, over all 1020 cells):")
    for k, v in fc.value_counts().head(12).items():
        P(f"    {k:28s} {v}")
    P(f"  KEEP verdict: {'4b KEEP-candidate cells exist' if int(m10.keep4b.sum()) else 'no cell passes 4b'}"
      f"; BOTH-path cells at 10 bps: {int((m10.keep4a & m10.keep4b).sum())}")
    P("")
    P(f"# done in {time.time() - t0:.1f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()

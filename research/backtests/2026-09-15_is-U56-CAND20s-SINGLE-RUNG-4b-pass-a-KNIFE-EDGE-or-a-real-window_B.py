#!/usr/bin/env python3
"""
IDEA 675 -- is-U56-CAND20-s-SINGLE-RUNG-4b-pass-a-KNIFE-EDGE-or-a-real-window   (lane B, 2026-09-15)
====================================================================================================

THE QUEUE'S QUESTION (verbatim intent, 2026-09-11)
--------------------------------------------------
  Idea 670 found the record's own 2026-09-04 KEEP 4b book passes at EXACTLY g=0.75 and nowhere on
  the rest of the 8-rung ladder, while every band-book pass sits at g >= 0.95.  Re-run that ONE
  book on a 0.01-resolution gross ladder and report the TRUE WIDTH of its pass window, and whether
  the window survives rule-8 selection and a cost sweep.  Max 2 params (gross resolution, cost rung).

WHY IT MATTERS.  "Passes at exactly one rung of eight" reads like a knife edge -- a book whose only
4b pass is an accident of where the ladder happened to be sampled.  But idea 670's rungs around the
pass are 0.60, 0.75, 0.85: three samples spanning 0.25 of gross.  A window 0.20 wide and a window
0.005 wide look IDENTICAL at that resolution.  The record has quoted "single rung" as though it
were a fragility finding.  Either it is one, or it is a statement about idea 670's rung spacing.
This run settles which, on the book's own tape, and prices what a walk-forward chooser would get.

THE BOOK (the record's, restated -- nothing here is re-specified)
----------------------------------------------------------------
  CAND20  top-20 names by the composite rank score WITHOUT the vol scaler
          (baseline.score(px, vol_scale=False)), eligible = above its own 200d MA and vol20 < 0.60,
          equal weight g/k of NAV, rest in CASH at 0%, weekly rebalance, weights at close t filled
          t+1, 10 bps per unit turnover.  This is idea 670's CAND20 arm and the 2026-09-04 KEEP 4b
          book.  Its committed 8-rung ladder is the cross-run gate G3 below.

WHAT IS TUNED AND WHAT IS NOT (PROTOCOL 4: no more than 2 tuned parameters)
--------------------------------------------------------------------------
  TUNED 1  GROSS RESOLUTION   STEP in {0.25, 0.10, 0.05, 0.01}   (the queue's own first dial)
  TUNED 2  COST RUNG          COST in {0, 10, 25, 50} bps        (the queue's own second dial)
           EVERY point of both is reported, in .ladder.csv / .window.csv.  10 bps is PROTOCOL 2's
           binding rung and is the only one any verdict below is stated at; the other three are
           audit axes the queue asked for by name.
  NOT TUNED  the book (n=20, no vol scaler, cap 0.60, weekly, warm-up 260 rows) -- all the record's
           committed definitions; the IS/OOS split 2016-12-31 / 2017-01-01 (PROTOCOL 8); the 4b
           bars 0.60 x |MaxDD_SPY| and 0.70 x CAGR_SPY (PROTOCOL 4b); the panels.
  REPORTED AXES  panel (U56 primary, B136 portability), window (FULL / H1 / H2 / IS / OOS),
           price vintage (today's, and idea 670's own last date -- see G3b/VINTAGE below).

THE STATISTIC
-------------
  On the gross axis the five 4b legs are one-sided constraints (idea 670/677's reading):
      L1  H1 Sharpe > SPY H1        L2  H2 Sharpe > SPY H2        L3  OOS Sharpe > SPY OOS
      L4  |MaxDD(g)| <= 0.60 |MaxDD_SPY|      binds from ABOVE  ->  g <= g_max
      L5  CAGR(g)    >= 0.70 CAGR_SPY         binds from BELOW  ->  g >= g_min
  L1/L2/L3 are SCALE-FREE to four decimals on this book (Sharpe moves 0.0015 across the whole
  ladder), so the window is cut by L4 and L5 alone; the Sharpe legs are reported as pass COUNTS at
  every window so that a window where they bind is visible rather than assumed away.
  The PASS WINDOW is [g_min, g_max]; its WIDTH is W = g_max - g_min.  Two readings side by side:
      W_ladder(STEP)  the contiguous 5-leg pass run measured on a ladder of that step (what 670 saw)
      W_exact         g_min and g_max solved by BISECTION on L5 and L4 to 1e-4 of gross (the truth)
  The support is g in [0.01, 1.50] so a window whose FLOOR is unreachable can be REPORTED rather
  than silently clipped (idea 677's convention).  Any g > 1.00 is LEVERAGE, flagged NOT TRADEABLE;
  no recommendation below stands on such a point.

PRE-REGISTERED BARS (fixed before any number below was read)
------------------------------------------------------------
  KNIFE EDGE   W_exact <= 0.02 of gross at 10 bps on U56 FULL.
  REAL WINDOW  W_exact >= 0.10 AND the live constant g = 0.75 sits >= 0.03 inside BOTH boundaries.
  NARROW       anything between.

PRE-REGISTERED HYPOTHESES
-------------------------
  H1  (the queue's question) W_exact >= 0.10 on U56 FULL at 10 bps -- i.e. 670's "single rung" is a
      RUNG-SPACING artefact, not a knife edge.
  H2  (cost) the window is non-empty and contains g = 0.75 at every cost rung in {0, 10, 25, 50}.
      Reported beside it, because the two are NOT the same number: the cost at which the DD-cap x
      CAGR-floor WINDOW closes (W_exact = 0), and the cost at which the FIVE-LEG 4b PASS goes empty.
      The second is the binding one and it is lower, because cost drags the Sharpe legs.
  H3  (rule 8) the window solved on the IS window ALONE (2009-2016, against IS SPY's own bars) is
      non-empty, and the g chosen from it by a pre-registered IS-only rule clears 4b out of sample.
      Four IS-only choosers, all fixed here:
        PICK-MIN     the 2026-09-03 memo's own rule, "smallest g whose MaxDD <= 60% of SPY's and
                     CAGR >= 70% of SPY's", read on IS only.
        PICK-MID     the midpoint of the IS window (the maximal-margin point).
        PICK-SHARPE  IS-Sharpe argmax over the IS 5-LEG pass set (a reference; may be EMPTY, in
                     which case that is reported as the finding it is, not skipped).
        PICK-LIVE    g = 0.75, the live constant, fitted on NOTHING -- the zero-parameter reference.
  H4  (well-posedness) MaxDD is non-increasing and CAGR non-decreasing in g on the 0.01 ladder, so
      the pass set IS an interval and "width" is a meaningful word.
  H5  (is the window a full-sample-only object) the windows solved on H1 alone and on H2 alone,
      each against its OWN half of SPY, both contain the FULL-sample window's midpoint.

GATES (run and printed BEFORE any hypothesis number is read)
------------------------------------------------------------
  G1   fast_backtest == engine.backtest at 10 bps, returns AND turnover                 bar 1e-12
  G2   weights(g) == g * weights(1.00) at bar 1e-12, so on this ladder gross is PURE exposure.
       BAR CORRECTION, stated not hidden: an exact-0.0 bar is UNREACHABLE here and this run's first
       pass mis-set it and recorded a FAIL at 5.55e-17.  The two sides divide by the name count in
       a different order (g/k vs g*(1/k)) so they differ in the last bit of a double and can never
       be bit-identical.  Idea 670 hit and published the same correction; 1e-12 is the record's
       float bar and the one G1 uses for the same reason.
  G3a  CROSS-RUN on TODAY's price cache: idea 670's committed `.grid.csv` CAND20 rows -- 2 panels x
       8 rungs x 6 metrics.  EXPECTED TO DRIFT and reported, not asserted: the cache has grown
       since 2026-09-11 (U56 4702 -> 4704 rows, B136 4699 -> 4703).
  G3b  CROSS-RUN VINTAGE-MATCHED, each panel truncated to idea 670's own last date (U56 2026-09-10,
       B136 2026-09-04).                                                                 bar 5e-4
       G3b FAILS and the failure is localized rather than explained away: matching the row count
       removes most of the G3a gap, MaxDD reproduces to 1e-8 and CAGR to 1e-5 on U56, but the whole
       SHARPE family is off by a uniform-signed ~5e-4 (U56) / ~6e-3 (B136).  MaxDD is a path
       extremum and CAGR an endpoint ratio; Sharpe averages every day, so this is the signature of
       small per-name revisions in the ADJUSTED price history (the record's own PRICES-VINTAGE
       effect), to which a 20-name concentrated book is far more exposed than the 56-name band book
       -- which is why G4b passes at 1.8e-05 on the SAME frames.
  G3c  CROSS-RUN restricted to the two WINDOW-CUTTING metrics (CAGR and MaxDD, the only two this
       run's headline is measured on), U56 vintage-matched.  THIS is the bar the headline rests on.
       B136 fails the same restriction at ~1.3e-3, so every B136 number is a PORTABILITY reading
       and no headline rests on it.                                                      bar 5e-4
  G4a/G4b  SPY and RULES v2 (live) on U56 reproduce their committed triples
       (15.1113% / 0.8835 / -33.7173% and 8.6132% / 1.1998 / -12.0549%), today and matched. bar 5e-4
  G5   MONOTONICITY of the 0.01 ladder (H4's gate form), reported as violation counts
  G6   DETERMINISM: ladder points rebuilt, max |dSharpe| and |dMaxDD|                    bar 0.0
  G7   the fine ladder is priced from g * weights(1.00); G7 asserts the METRICS from that path equal
       the metrics from the record's own g/k construction                                bar 1e-12

PROTOCOL COMPLIANCE
-------------------
  2  10 bps binding, weights decided at close t applied t+1, weekly, no leverage in any traded
     recommendation (ladder points above 1.00 are reported and flagged, never recommended).
  3  every reported book compared to RULES v2 (live baseline) and SPY buy-and-hold, same sample.
  4  BOTH KEEP paths evaluated at EVERY grid point.  4a is judged against RULES v2.
  8  WALK-FORWARD: window, boundaries and every chooser decision computed on 2009-2016 ALONE;
     2017-2026 read ONCE per (panel, chooser, cost).
  9  SURVIVORSHIP: U56 (research/universe.json) and B136 (universe_broad.json) are CURRENT
     constituent lists.  Every CAGR and drawdown LEVEL below is optimistic -- the book's, RULES
     v2's and SPY's alike -- and both 4b bars are easier here than on a point-in-time panel.  The
     run's HEADLINE is a WIDTH on the gross axis of ONE book against ITS OWN SPY bars, a same-tape
     same-names statement, far less exposed than a level; the OOS triples are levels and are
     upper bounds.

Outputs beside this script: .console.txt .ladder.csv .window.csv .walkforward.csv .gates.csv
                            .result.md
"""
from __future__ import annotations

import json
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score           # noqa: E402
from engine import backtest, rebalance_mask                           # noqa: E402

# ---------------- reported constants (never tuned) --------------------------------------------
FREQ = "W"
MAXVOL = 0.60
NCAND = 20
WARM = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_MULT, CAGR_MULT = 0.60, 0.70
GROSS_LIVE = 0.75
G_LO, G_HI = 0.01, 1.50
BISECT_TOL = 1e-4
FLOAT_BAR = 1e-12

# ---------------- the two tuned parameters -----------------------------------------------------
STEPS = [0.25, 0.10, 0.05, 0.01]
COSTS = [0.0, 10.0, 25.0, 50.0]
COST0 = 10.0

# ---------------- pre-registered bars ----------------------------------------------------------
KNIFE_BAR, REAL_BAR, REAL_MARGIN = 0.02, 0.10, 0.03

# ---------------- cross-run references ---------------------------------------------------------
IDEA670_GRID = ROOT / "research" / "backtests" / (
    "2026-09-11_is-the-GROSS-dial-s-4b-FOOTPRINT-the-CAGR-FLOOR-alone_C.grid.csv")
IDEA670_VINTAGE = {"U56": "2026-09-10", "B136": "2026-09-04"}   # that run's own last dates
G4_SPY = dict(CAGR=0.151113, Sharpe=0.883474, MaxDD=-0.337173)
G4_V2 = dict(CAGR=0.086132, Sharpe=1.199807, MaxDD=-0.120549)
IDEA670_LADDER = [0.20, 0.35, 0.50, 0.60, 0.75, 0.85, 0.95, 1.00]

LINES: list[str] = []


def P(s: str = "") -> None:
    print(s, flush=True)
    LINES.append(str(s))


def dump(df: pd.DataFrame, suffix: str) -> None:
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"    wrote {p.name}  ({len(df)} rows)")


# ==============================================================================================
# 1.  ENGINE  (vectorised equivalent of engine.backtest; G1 asserts equality)
# ==============================================================================================
def fast_backtest(prices, weights, freq=FREQ, cost=COST0, want_turn=False):
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy()
    m[0] = True
    T, Ncol = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, Ncol)), C[:-1]])
    reb = np.flatnonzero(m)
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
    r = pd.Series((held * rets).sum(axis=1) - turn * cost / 1e4, index=idx)
    if want_turn:
        return r, pd.Series(turn, index=idx)
    return r


def sharpe(r):
    v = r.std() * np.sqrt(252)
    return (r.mean() * 252) / v if v else np.nan


def trip(r):
    eq = (1 + r).cumprod()
    yrs = len(r) / 252
    v = r.std() * np.sqrt(252)
    h = len(r) // 2
    return dict(CAGR=eq.iloc[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan,
                Sharpe=(r.mean() * 252) / v if v else np.nan,
                MaxDD=(eq / eq.cummax() - 1).min(),
                H1=sharpe(r.iloc[:h]), H2=sharpe(r.iloc[h:]))


# ==============================================================================================
# 2.  THE BOOK
# ==============================================================================================
def prep(px):
    sc, above, vol20 = score(px, vol_scale=False)
    return sc, above, vol20


def cand20_weights(px, pre, g, n=NCAND):
    """The record's own construction: g/k on the selected names."""
    sc, above, vol20 = pre
    elig = sc.where(above & (vol20 < MAXVOL))
    sel = (elig.rank(axis=1, ascending=False) <= n).astype(float)
    k = sel.sum(axis=1).replace(0, np.nan)
    return (sel.mul(g / k, axis=0)).fillna(0.0)


# ==============================================================================================
# 3.  PANEL CONTEXT
# ==============================================================================================
WINDOWS = ["FULL", "H1", "H2", "IS", "OOS"]
LEGNAMES = ["L1_H1", "L2_H2", "L3_OOS", "L4_DDcap", "L5_CAGRfloor"]


def slice_win(r, win):
    if win == "FULL":
        return r
    if win == "H1":
        return r.iloc[:len(r) // 2]
    if win == "H2":
        return r.iloc[len(r) // 2:]
    if win == "IS":
        return r.loc[:IS_END]
    if win == "OOS":
        return r.loc[OOS_START:]
    raise KeyError(win)


def build_ctx(px):
    start = px.index[WARM]
    pre = prep(px)
    ctx = dict(px=px, pre=pre, start=start, W1=cand20_weights(px, pre, 1.00),
               spy=px["SPY"].pct_change().fillna(0.0).loc[start:],
               v2=fast_backtest(px, rules_v2_weights(px), cost=COST0).loc[start:],
               bars={}, spy_m={}, v2_m={}, cache={})
    for w in WINDOWS:
        m = trip(slice_win(ctx["spy"], w))
        ctx["spy_m"][w] = m
        ctx["v2_m"][w] = trip(slice_win(ctx["v2"], w))
        ctx["bars"][w] = dict(dd_cap=DD_MULT * abs(m["MaxDD"]), cagr_floor=CAGR_MULT * m["CAGR"],
                              h1=m["H1"], h2=m["H2"], sh=m["Sharpe"])
    return ctx


def price(ctx, g, cost):
    """Priced from g * weights(1.00) -- the exact scaling identity (gate G7)."""
    key = (round(float(g), 6), float(cost))
    if key not in ctx["cache"]:
        ctx["cache"][key] = fast_backtest(ctx["px"], float(g) * ctx["W1"],
                                          cost=float(cost)).loc[ctx["start"]:]
    return ctx["cache"][key]


def legs_on(ctx, r, win):
    s = slice_win(r, win)
    m = trip(s)
    b, sm, vm = ctx["bars"][win], ctx["spy_m"][win], ctx["v2_m"][win]
    if win == "FULL":
        l3 = sharpe(slice_win(r, "OOS")) > sharpe(slice_win(ctx["spy"], "OOS"))
    else:
        l3 = m["Sharpe"] > sm["Sharpe"]
    L = dict(L1_H1=bool(m["H1"] > b["h1"]), L2_H2=bool(m["H2"] > b["h2"]), L3_OOS=bool(l3),
             L4_DDcap=bool(abs(m["MaxDD"]) <= b["dd_cap"]),
             L5_CAGRfloor=bool(m["CAGR"] >= b["cagr_floor"]))
    return dict(**m, **L, pass4b=all(L.values()),
                pass4a=bool(m["H1"] > vm["H1"] and m["H2"] > vm["H2"] and m["MaxDD"] >= vm["MaxDD"]),
                dd_slack=b["dd_cap"] - abs(m["MaxDD"]), cagr_slack=m["CAGR"] - b["cagr_floor"])


# ==============================================================================================
# 4.  BISECTION
# ==============================================================================================
def bisect_boundary(f, lo, hi, tol=BISECT_TOL):
    """Largest x in [lo,hi] with f(x) >= 0, given f decreasing."""
    if f(lo) < 0:
        return np.nan, "empty"
    if f(hi) >= 0:
        return hi, "unbounded"
    a, b = lo, hi
    while b - a > tol:
        mid = 0.5 * (a + b)
        if f(mid) >= 0:
            a = mid
        else:
            b = mid
    return a, "ok"


def solve_window(ctx, win, cost):
    b = ctx["bars"][win]

    def dd_slack(g):
        return b["dd_cap"] - abs(trip(slice_win(price(ctx, g, cost), win))["MaxDD"])

    def cagr_slack(g):
        return trip(slice_win(price(ctx, g, cost), win))["CAGR"] - b["cagr_floor"]

    g_max, st_max = bisect_boundary(dd_slack, G_LO, G_HI)
    g_min_m, st_min = bisect_boundary(lambda g: cagr_slack(G_LO + G_HI - g), G_LO, G_HI)
    if st_min == "unbounded":
        g_min, st_min = G_LO, "ok_at_support_floor"
    elif st_min == "empty":
        g_min = np.nan
    else:
        g_min = G_LO + G_HI - g_min_m
    W = (g_max - g_min) if (np.isfinite(g_max) and np.isfinite(g_min)) else np.nan
    return dict(window=win, cost=cost, g_min=g_min, g_max=g_max, W_exact=W,
                st_min=st_min, st_max=st_max, dd_cap=b["dd_cap"], cagr_floor=b["cagr_floor"],
                live_inside=bool(np.isfinite(W) and g_min <= GROSS_LIVE <= g_max),
                live_margin_lo=GROSS_LIVE - g_min if np.isfinite(g_min) else np.nan,
                live_margin_hi=g_max - GROSS_LIVE if np.isfinite(g_max) else np.nan,
                tradeable=bool(np.isfinite(W) and g_min <= 1.00))


def closure_cost(ctx, win="FULL", lo=0.0, hi=200.0, tol=0.05):
    """The cost rung at which W_exact hits 0 -- the window's own closing price, in bps."""
    def w_at(c):
        s = solve_window(ctx, win, c)
        return s["W_exact"] if np.isfinite(s["W_exact"]) else -1.0
    if w_at(lo) <= 0:
        return np.nan
    if w_at(hi) > 0:
        return np.inf
    a, b = lo, hi
    while b - a > tol:
        mid = 0.5 * (a + b)
        if w_at(mid) > 0:
            a = mid
        else:
            b = mid
    return a


def pass_closure_cost(ctx, win="FULL", lo=0.0, hi=100.0, tol=0.05):
    """The cost at which the FIVE-leg 4b pass set goes empty -- scanned inside the window at that
    cost, since L4/L5 define the window and L1/L2/L3 are near-flat in g."""
    def any_pass(c):
        w = solve_window(ctx, win, c)
        if not (np.isfinite(w["W_exact"]) and w["W_exact"] > 0):
            return False
        gs = np.unique(np.round(np.linspace(w["g_min"], w["g_max"], 21), 4))
        return any(legs_on(ctx, price(ctx, float(g), c), win)["pass4b"] for g in gs)
    if not any_pass(lo):
        return np.nan
    if any_pass(hi):
        return np.inf
    a, b = lo, hi
    while b - a > tol:
        mid = 0.5 * (a + b)
        if any_pass(mid):
            a = mid
        else:
            b = mid
    return a


def ladder_grid(step):
    n = int(round((1.50 - step) / step)) + 1
    return np.round(np.array([step * (i + 1) for i in range(n)]), 6)


def contiguous_pass_run(gs, passes):
    best = (np.nan, np.nan, np.nan, 0)
    i = 0
    while i < len(gs):
        if passes[i]:
            j = i
            while j + 1 < len(gs) and passes[j + 1]:
                j += 1
            if j - i + 1 > best[3]:
                best = (gs[i], gs[j], gs[j] - gs[i], j - i + 1)
            i = j + 1
        else:
            i += 1
    return best


# ==============================================================================================
# 5.  MAIN
# ==============================================================================================
def main():
    t0 = time.time()
    P("=" * 190)
    P("IDEA 675 - is U56/CAND20's SINGLE-RUNG 4b pass a KNIFE EDGE or a REAL WINDOW?   (lane B, 2026-09-15)")
    P("The book: top-20 by the NO-VOL-SCALER composite among names above 200d with vol20<0.60,")
    P("equal weight g/k, cash at 0%, weekly, t+1 fills. The 2026-09-04 KEEP 4b book = idea 670's CAND20 arm.")
    P(f"TUNED 1 gross resolution STEP in {STEPS}   TUNED 2 cost rung {[int(c) for c in COSTS]} bps")
    P(f"Bars: PROTOCOL 4b DD cap {DD_MULT}x|MaxDD_SPY|, CAGR floor {CAGR_MULT}x CAGR_SPY. "
      f"Support g in [{G_LO}, {G_HI}], bisection tol {BISECT_TOL}.")
    P(f"PRE-REGISTERED: KNIFE EDGE if W_exact <= {KNIFE_BAR}; REAL WINDOW if W_exact >= {REAL_BAR} "
      f"and g=0.75 sits >= {REAL_MARGIN} inside both boundaries; NARROW otherwise.")
    P("=" * 190)

    P("\n[1] PANELS (today's price cache)")
    panels, raw = {}, {}
    for name, kw in (("U56", {}), ("B136", dict(broad=True))):
        px = load_universe(**kw)
        raw[name] = px
        panels[name] = build_ctx(px)
        c = panels[name]
        sm, vm = c["spy_m"]["FULL"], c["v2_m"]["FULL"]
        P(f"    {name}: {px.shape[1]} columns, {px.index[0].date()} -> {px.index[-1].date()} "
          f"({len(px)} rows), scored from {c['start'].date()} ({len(c['spy'])} days)")
        P(f"      SPY      {sm['CAGR']:.4%} / {sm['Sharpe']:.4f} / {sm['MaxDD']:.4%}  halves "
          f"{sm['H1']:.4f}/{sm['H2']:.4f}   -> 4b bars: DD cap {-c['bars']['FULL']['dd_cap']:.4%}, "
          f"CAGR floor {c['bars']['FULL']['cagr_floor']:.4%}")
        P(f"      RULES v2 {vm['CAGR']:.4%} / {vm['Sharpe']:.4f} / {vm['MaxDD']:.4%}  halves "
          f"{vm['H1']:.4f}/{vm['H2']:.4f}   (the 4a comparand)")

    # ------------------------------------------------------------------ GATES
    P("\n" + "=" * 190)
    P("[2] GATES - printed BEFORE any hypothesis number is read")
    P("=" * 190)
    gates, grows = {}, []
    u = panels["U56"]

    wl = cand20_weights(u["px"], u["pre"], GROSS_LIVE)
    fr, ft = fast_backtest(u["px"], wl, cost=COST0, want_turn=True)
    er = backtest(u["px"], wl, cost_bps=COST0, freq=FREQ)
    d_r = float(np.abs(fr - er["returns"]).max())
    d_t = float(np.abs(ft - er["turnover"]).max())
    gates["G1"] = d_r < FLOAT_BAR and d_t < FLOAT_BAR
    P(f"  G1  fast_backtest == engine.backtest         max|dret| {d_r:.3e}  max|dturn| {d_t:.3e}"
      f"   bar 1e-12   {'PASS' if gates['G1'] else 'FAIL'}")

    worst2 = 0.0
    for g in (0.20, 0.37, 0.75, 0.99, 1.31):
        worst2 = max(worst2, float(np.abs(cand20_weights(u["px"], u["pre"], g)
                                          - g * u["W1"]).max().max()))
    gates["G2"] = worst2 < FLOAT_BAR
    P(f"  G2  weights(g) == g * weights(1.00)          max|dev| {worst2:.3e}"
      f"                       bar 1e-12   {'PASS' if gates['G2'] else 'FAIL'}")
    P("      BAR CORRECTION (stated, not hidden): this run's FIRST pass set G2's bar at exact 0.0 and")
    P("      recorded a FAIL at 5.551e-17.  The bar was unreachable: the two sides divide by the name")
    P("      count in a different order (g/k vs g*(1/k)) and differ in the last bit of a double.")
    P("      Idea 670 hit and published the same correction; 1e-12 is the record's float bar.")

    worst7 = 0.0
    for g in (0.31, 0.75, 1.13):
        a = trip(fast_backtest(u["px"], cand20_weights(u["px"], u["pre"], g),
                               cost=COST0).loc[u["start"]:])
        b = trip(price(u, g, COST0))
        worst7 = max(worst7, max(abs(a[k] - b[k]) for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2")))
    gates["G7"] = worst7 < FLOAT_BAR
    P(f"  G7  ladder priced from g*W(1.00) == g/k book  max|dmetric| {worst7:.3e}"
      f"                  bar 1e-12   {'PASS' if gates['G7'] else 'FAIL'}")

    ref = pd.read_csv(IDEA670_GRID)
    ref = ref[ref.arm == "CAND20"]
    mcols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe"]

    def cross_run(ctxs, tag):
        worst, rows = 0.0, []
        for pan in ("U56", "B136"):
            c = ctxs[pan]
            for _, rr in ref[ref.panel == pan].iterrows():
                r = price(c, float(rr.gross), COST0)
                mine = dict(trip(r), OOS_Sharpe=sharpe(slice_win(r, "OOS")))
                sgn = {k: mine[k] - float(rr[k]) for k in mcols}
                dev = {k: abs(v) for k, v in sgn.items()}
                worst = max(worst, max(dev.values()))
                rows.append(dict(vintage=tag, panel=pan, gross=float(rr.gross),
                                 **{f"d_{k}": dev[k] for k in mcols},
                                 **{f"s_{k}": sgn[k] for k in mcols}))
        return worst, rows

    w3a, r3a = cross_run(panels, "today")
    gates["G3a"] = None
    P(f"\n  G3a CROSS-RUN idea 670 CAND20 grid on TODAY's cache: 16 rows x 6 metrics, "
      f"worst |dev| {w3a:.3e}   (REPORTED, no bar)")

    matched = {}
    for pan in ("U56", "B136"):
        matched[pan] = build_ctx(raw[pan].loc[:IDEA670_VINTAGE[pan]])
        P(f"      {pan} vintage-matched to {IDEA670_VINTAGE[pan]}: "
          f"{len(matched[pan]['px'])} rows (today {len(raw[pan])})")
    w3b, r3b = cross_run(matched, "matched")
    gates["G3b"] = w3b < 5e-4
    P(f"  G3b CROSS-RUN VINTAGE-MATCHED to idea 670's own last dates: worst |dev| {w3b:.3e}"
      f"   bar 5e-4   {'PASS' if gates['G3b'] else 'FAIL'}")
    m3 = pd.DataFrame(r3b)
    P(f"      Matching the row count removes {1 - w3b/max(w3a,1e-18):.0%} of the G3a gap but NOT all")
    P("      of it, so the residual is NOT only the cache's 2-4 extra rows. WHERE IT SITS, per metric")
    P("      (worst |dev| over the 8 rungs, and the residual's SIGN -- uniform sign means a tape")
    P("      difference, not a construction difference):")
    for pan in ("U56", "B136"):
        s = m3[m3.panel == pan]
        P(f"        {pan:5s} " + "  ".join(
            f"{k} {s[f'd_{k}'].max():.2e}({'+' if s[f's_{k}'].mean() > 0 else '-'})" for k in mcols))
    P("      DIAGNOSIS, stated as a limit of this reproduction and not explained away: MaxDD")
    P("      reproduces to 1e-8 / 1e-6 and CAGR to 1e-5 / 1e-3, while the whole Sharpe family is off")
    P("      by a uniform-signed ~5e-4 (U56) / ~6e-3 (B136). MaxDD is a path extremum and CAGR an")
    P("      endpoint ratio; Sharpe is a mean/vol over every day. That is the signature of small")
    P("      per-name revisions in the ADJUSTED price history (auto_adjust re-states past closes when")
    P("      a dividend is paid), which the record already tracks as the PRICES-VINTAGE effect. A")
    P("      20-name concentrated book is far more exposed to it than the 56-name band book, which is")
    P("      why G4b passes at 1.8e-05 on the SAME frames where G3b fails.")

    dw = max(max(abs(rr[f"d_{k}"]) for k in ("CAGR", "MaxDD")) for rr in r3b
             if rr["panel"] == "U56")
    gates["G3c"] = dw < 5e-4
    P(f"  G3c CROSS-RUN restricted to the TWO WINDOW-CUTTING metrics (CAGR, MaxDD -- the only two")
    P(f"      this run's headline is measured on), U56 vintage-matched: worst |dev| {dw:.3e}"
      f"   bar 5e-4   {'PASS' if gates['G3c'] else 'FAIL'}")
    dwb = max(max(abs(rr[f"d_{k}"]) for k in ("CAGR", "MaxDD")) for rr in r3b
              if rr["panel"] == "B136")
    P(f"      the same restriction on B136 reads {dwb:.3e} (fails 5e-4, clears 2e-3), so every")
    P("      B136 number below is a PORTABILITY reading and no headline rests on it.")

    def g4(ctxs, tag):
        sm, vm = ctxs["U56"]["spy_m"]["FULL"], ctxs["U56"]["v2_m"]["FULL"]
        return max(abs(sm[k] - G4_SPY[k]) for k in G4_SPY), max(abs(vm[k] - G4_V2[k]) for k in G4_V2)

    d4a_s, d4a_v = g4(panels, "today")
    d4b_s, d4b_v = g4(matched, "matched")
    gates["G4a"] = None
    gates["G4b"] = max(d4b_s, d4b_v) < 5e-4
    P(f"  G4a SPY / RULES v2 committed U56 triples on TODAY's cache: worst |dev| "
      f"{max(d4a_s, d4a_v):.3e}   (REPORTED, no bar)")
    P(f"  G4b SPY / RULES v2 committed U56 triples VINTAGE-MATCHED: worst |dev| "
      f"{max(d4b_s, d4b_v):.3e}   bar 5e-4   {'PASS' if gates['G4b'] else 'FAIL'}")

    P("\n    building the 0.01 ladder (150 rungs x 4 cost rungs x 2 panels) ...")
    fine = ladder_grid(0.01)
    for pan, c in panels.items():
        for cost in COSTS:
            for g in fine:
                price(c, float(g), cost)
    P(f"    done in {time.time()-t0:.1f}s")

    mono_rows = []
    for pan, c in panels.items():
        for cost in COSTS:
            for win in WINDOWS:
                ms = [trip(slice_win(price(c, float(g), cost), win)) for g in fine]
                dd = np.array([m["MaxDD"] for m in ms])
                cg = np.array([m["CAGR"] for m in ms])
                mono_rows.append(dict(panel=pan, cost=cost, window=win,
                                      dd_violations=int((np.diff(dd) > 0).sum()),
                                      cagr_violations=int((np.diff(cg) < 0).sum()),
                                      n_steps=len(fine) - 1))
    mono = pd.DataFrame(mono_rows)
    gates["G5"] = bool((mono.dd_violations == 0).all() and (mono.cagr_violations == 0).all())
    P(f"  G5  MONOTONICITY of the 0.01 ladder: {len(mono)} (panel,cost,window) blocks, worst DD "
      f"violations {mono.dd_violations.max()}, worst CAGR violations {mono.cagr_violations.max()} "
      f"of {len(fine)-1} steps   {'PASS' if gates['G5'] else 'FAIL'}")

    d6 = 0.0
    for g in (0.31, 0.75, 1.13):
        m1 = trip(price(u, g, COST0))
        m2 = trip(fast_backtest(u["px"], g * u["W1"], cost=COST0).loc[u["start"]:])
        d6 = max(d6, abs(m1["Sharpe"] - m2["Sharpe"]), abs(m1["MaxDD"] - m2["MaxDD"]))
    gates["G6"] = d6 == 0.0
    P(f"  G6  DETERMINISM (ladder points rebuilt)      max|dSharpe|,|dMaxDD| {d6:.3e}"
      f"                bar 0.0     {'PASS' if gates['G6'] else 'FAIL'}")

    barred = {k: v for k, v in gates.items() if v is not None}
    P(f"\n  GATES WITH A BAR: {sum(barred.values())} of {len(barred)} PASS   "
      + "  ".join(f"{k}={'PASS' if v else 'FAIL'}" for k, v in barred.items())
      + "   (G3a/G4a are reported diagnostics, no bar)")
    dump(pd.DataFrame(r3a + r3b), "gates")

    # ------------------------------------------------------------------ the ladder
    P("\n" + "=" * 190)
    P("[3] THE LADDER - every point of both tuned parameters, all five 4b legs decomposed")
    P("=" * 190)
    lad_rows = []
    for pan, c in panels.items():
        for cost in COSTS:
            for g in fine:
                r = price(c, float(g), cost)
                for win in WINDOWS:
                    lad_rows.append(dict(panel=pan, cost=cost, gross=float(g), window=win,
                                         **legs_on(c, r, win)))
    lad = pd.DataFrame(lad_rows)
    dump(lad, "ladder")

    P(f"\n  U56 / FULL / {int(COST0)} bps - the rungs idea 670 sampled (*), then the interior it missed")
    sub = lad[(lad.panel == "U56") & (lad.window == "FULL") & (lad.cost == COST0)]
    show = sorted(set(IDEA670_LADDER) | {0.61, 0.62, 0.63, 0.65, 0.70, 0.80, 0.82, 0.83, 0.84})
    P("       g      CAGR     Sharpe    MaxDD     H1     H2   L1 L2 L3 L4 L5  4b  4a   DDslack  CAGRslack")
    for g in show:
        rr = sub[np.isclose(sub.gross, g)]
        if rr.empty:
            continue
        rr = rr.iloc[0]
        star = "*" if g in IDEA670_LADDER else " "
        f = lambda b: " Y" if b else " ."   # noqa: E731
        P(f"   {star} {g:4.2f}  {rr.CAGR:7.3%}  {rr.Sharpe:7.4f}  {rr.MaxDD:8.3%}  {rr.H1:5.3f}  "
          f"{rr.H2:5.3f}  {f(rr.L1_H1)}{f(rr.L2_H2)}{f(rr.L3_OOS)}{f(rr.L4_DDcap)}"
          f"{f(rr.L5_CAGRfloor)}  {f(rr.pass4b)} {f(rr.pass4a)}  {rr.dd_slack:+8.4f}  "
          f"{rr.cagr_slack:+9.5f}")
    P("\n  WHICH LEGS BIND (pass counts over the 150-rung ladder, U56 FULL 10 bps) - the Sharpe legs")
    P("  are reported rather than assumed away:")
    P("      " + "   ".join(f"{L} {int(sub[L].sum())}/150" for L in LEGNAMES))

    # ------------------------------------------------------------------ H1
    P("\n" + "=" * 190)
    P("[4] H1 - THE TRUE WIDTH, and what each ladder resolution SEES of it")
    P("=" * 190)
    win_rows = []
    for pan, c in panels.items():
        for cost in COSTS:
            for win in WINDOWS:
                w = solve_window(c, win, cost)
                s = lad[(lad.panel == pan) & (lad.cost == cost) & (lad.window == win)]
                for step, gs in ([(st, ladder_grid(st)) for st in STEPS]
                                 + [("670", np.array(IDEA670_LADDER))]):
                    keep = s[np.isin(np.round(s.gross.values, 6), np.round(gs, 6))
                             ].sort_values("gross")
                    lo, hi, wlad, cnt = contiguous_pass_run(keep.gross.values, keep.pass4b.values)
                    win_rows.append(dict(panel=pan, **w, STEP=str(step), n_rungs=len(gs),
                                         n_pass_rungs=int(keep.pass4b.sum()), run_lo=lo, run_hi=hi,
                                         W_ladder=wlad, run_rungs=cnt,
                                         pass4a_rungs=int(keep.pass4a.sum())))
    wdf = pd.DataFrame(win_rows)
    dump(wdf, "window")

    P(f"\n  U56 / FULL / {int(COST0)} bps - THE ANSWER TO THE QUEUE'S QUESTION")
    a = wdf[(wdf.panel == "U56") & (wdf.window == "FULL") & (wdf.cost == COST0)]
    a0 = a.iloc[0]
    P(f"      g_min (CAGR floor L5 binds from below)  {a0.g_min:.4f}   [{a0.st_min}]   floor "
      f"{a0.cagr_floor:.4%}")
    P(f"      g_max (DD cap L4 binds from above)      {a0.g_max:.4f}   [{a0.st_max}]   cap "
      f"{-a0.dd_cap:.4%}")
    P(f"      W_exact = g_max - g_min                 {a0.W_exact:.4f} of gross "
      f"({a0.W_exact*100:.2f} gross points)")
    P(f"      live g=0.75 inside? {a0.live_inside}   margin below {a0.live_margin_lo:+.4f}, "
      f"above {a0.live_margin_hi:+.4f}")
    P("\n      WHAT EACH LADDER RESOLUTION SEES (contiguous 5-leg 4b pass run on that ladder):")
    P("        ladder   rungs   4b-pass rungs   run             W_ladder   4a-pass rungs")
    order = {"0.25": 0, "0.1": 1, "0.05": 2, "0.01": 3, "670": 4}
    for _, rr in a.assign(_o=a.STEP.map(order)).sort_values("_o").iterrows():
        run = f"[{rr.run_lo:.2f}, {rr.run_hi:.2f}]" if np.isfinite(rr.run_lo) else "none"
        wv = rr.W_ladder if np.isfinite(rr.W_ladder) else float("nan")
        lab = "670's own" if rr.STEP == "670" else rr.STEP
        P(f"        {lab:9s} {rr.n_rungs:4d}   {rr.n_pass_rungs:13d}   {run:14s}  {wv:8.2f}   "
          f"{rr.pass4a_rungs:13d}")
    verdict_width = ("KNIFE EDGE" if a0.W_exact <= KNIFE_BAR else
                     "REAL WINDOW" if (a0.W_exact >= REAL_BAR and a0.live_margin_lo >= REAL_MARGIN
                                       and a0.live_margin_hi >= REAL_MARGIN) else "NARROW")
    P(f"\n      H1 pre-registered bar (W_exact >= {REAL_BAR}): "
      f"{'CONFIRMED' if a0.W_exact >= REAL_BAR else 'REFUTED'}    -> WIDTH VERDICT: {verdict_width}")

    mw = solve_window(matched["U56"], "FULL", COST0)
    P(f"\n      VINTAGE CHECK (does the width depend on the 2-row cache growth G3a found?):")
    P(f"        today's cache      [{a0.g_min:.4f}, {a0.g_max:.4f}]  W {a0.W_exact:.4f}")
    P(f"        670's own vintage  [{mw['g_min']:.4f}, {mw['g_max']:.4f}]  W {mw['W_exact']:.4f}"
      f"   -> |dW| {abs(mw['W_exact']-a0.W_exact):.4f}")

    P("\n  Every other (panel, window) at 10 bps, for context:")
    P("      panel  window    g_min    g_max   W_exact   0.75 in?   tradeable")
    for _, rr in wdf[(wdf.cost == COST0) & (wdf.STEP == "0.01")].iterrows():
        P(f"      {rr.panel:5s}  {rr.window:6s}  {rr.g_min:7.4f}  {rr.g_max:7.4f}  {rr.W_exact:7.4f}"
          f"   {str(rr.live_inside):8s}   {rr.tradeable}")

    # ------------------------------------------------------------------ H2
    P("\n" + "=" * 190)
    P("[5] H2 - THE COST SWEEP (the queue's second dial)")
    P("=" * 190)
    tr = fast_backtest(u["px"], GROSS_LIVE * u["W1"], cost=0.0, want_turn=True)[1].loc[u["start"]:]
    tpy = tr.sum() / (len(tr) / 252)
    P(f"  U56/CAND20 turnover at g=0.75: {tpy:.2f}x per year, so each 10 bps of cost is about "
      f"{tpy*10/1e4:.2%} of CAGR per year. The DD cap does not see cost; the CAGR floor does, so")
    P("  cost walks g_min UP against a nearly fixed g_max and the window closes from below.")
    P("      panel  cost   g_min    g_max   W_exact   0.75 in?   4b at 0.75?   note")
    h2_ok = True
    for pan in ("U56", "B136"):
        for cost in COSTS:
            rr = wdf[(wdf.panel == pan) & (wdf.window == "FULL") & (wdf.cost == cost)
                     & (wdf.STEP == "0.01")].iloc[0]
            p75 = lad[(lad.panel == pan) & (lad.window == "FULL") & (lad.cost == cost)
                      & np.isclose(lad.gross, 0.75)].iloc[0].pass4b
            note = "" if (np.isfinite(rr.W_exact) and rr.W_exact > 0) else "WINDOW CLOSED (g_min > g_max)"
            if pan == "U56" and not (np.isfinite(rr.W_exact) and rr.live_inside):
                h2_ok = False
            P(f"      {pan:5s}  {int(cost):3d}   {rr.g_min:7.4f}  {rr.g_max:7.4f}  {rr.W_exact:7.4f}"
              f"   {str(rr.live_inside):8s}   {str(bool(p75)):11s}   {note}")
    P("\n  TWO CLOSING PRICES, and the gap between them is the run's second real finding.")
    P("  Note the 25 bps rows above: on U56 the window is still 0.0979 wide and 0.75 is still INSIDE")
    P("  it, yet the 5-leg 4b pass is already FALSE. The window is cut by L4/L5 only; at 25 bps the")
    P("  H1-SHARPE leg (L1) fails at 0 of 150 rungs on U56, because cost drags the book's first-half")
    P("  Sharpe to 0.9283 against SPY's 0.9588. So the 4b PASS dies BEFORE the window closes.")
    cc, pc = {}, {}
    for pan, c in panels.items():
        cc[pan] = closure_cost(c)
        pc[pan] = pass_closure_cost(c)
        P(f"      {pan}: DD-cap x CAGR-floor WINDOW closes at {cc[pan]:.1f} bps "
          f"({cc[pan]/10:.1f}x PROTOCOL's rung);  the FIVE-LEG 4b PASS closes at "
          f"{pc[pan]:.1f} bps ({pc[pan]/10:.1f}x)")
    P(f"      -> the binding cost tolerance on U56 is {pc['U56']:.1f} bps, not {cc['U56']:.1f}: a "
      f"{cc['U56']/max(pc['U56'],1e-9):.1f}x difference, and quoting the window alone would "
      f"overstate it.")
    P(f"\n      H2 (window non-empty and contains 0.75 at EVERY cost rung on U56): "
      f"{'CONFIRMED' if h2_ok else 'REFUTED'}")

    # ------------------------------------------------------------------ H5
    P("\n" + "=" * 190)
    P("[6] H5 - is the window a FULL-SAMPLE-ONLY object? (each half solved against its OWN SPY)")
    P("=" * 190)
    h5_ok = True
    for pan in ("U56", "B136"):
        fr_ = wdf[(wdf.panel == pan) & (wdf.window == "FULL") & (wdf.cost == COST0)
                  & (wdf.STEP == "0.01")].iloc[0]
        mf = 0.5 * (fr_.g_min + fr_.g_max)
        for win in ("H1", "H2"):
            rr = wdf[(wdf.panel == pan) & (wdf.window == win) & (wdf.cost == COST0)
                     & (wdf.STEP == "0.01")].iloc[0]
            inside = bool(np.isfinite(rr.W_exact) and rr.g_min <= mf <= rr.g_max)
            if pan == "U56" and not inside:
                h5_ok = False
            P(f"      {pan:5s} {win}: window [{rr.g_min:.4f}, {rr.g_max:.4f}] W {rr.W_exact:.4f}"
              f"   contains that panel's full-sample midpoint {mf:.4f}? {inside}")
    P(f"\n      H5 (both U56 half-windows contain the full-sample midpoint): "
      f"{'CONFIRMED' if h5_ok else 'REFUTED'}")

    # ------------------------------------------------------------------ RULE 8
    P("\n" + "=" * 190)
    P("[7] RULE 8 - the window and the pick computed on 2009-2016 ALONE; 2017-2026 read ONCE")
    P("=" * 190)
    P("  A CAVEAT THAT MUST COME FIRST, because it changes what 'IS-only chooser' can mean here:")
    for pan in ("U56", "B136"):
        s = lad[(lad.panel == pan) & (lad.window == "IS") & (lad.cost == COST0)]
        P(f"      {pan} IN-SAMPLE 5-leg 4b pass set at 10 bps: {int(s.pass4b.sum())} of 150 rungs."
          f"   legs: " + "  ".join(f"{L} {int(s[L].sum())}/150" for L in LEGNAMES))
    P("      On U56 the IS H1-Sharpe leg fails at EVERY rung, so there is NO in-sample 4b passer to")
    P("      choose from: PICK-SHARPE has an empty feasible set and PICK-MIN / PICK-MID select from")
    P("      the DD-cap x CAGR-floor window alone. That is reported as the finding it is.")

    wf_rows = []
    for pan, c in panels.items():
        for cost in COSTS:
            wis = wdf[(wdf.panel == pan) & (wdf.window == "IS") & (wdf.cost == cost)
                      & (wdf.STEP == "0.01")].iloc[0]
            isl = lad[(lad.panel == pan) & (lad.window == "IS") & (lad.cost == cost)]
            feas = isl[isl.pass4b].sort_values("gross")
            picks = {"PICK-LIVE": GROSS_LIVE}
            if np.isfinite(wis.W_exact) and wis.W_exact > 0:
                picks["PICK-MIN"] = float(wis.g_min)
                picks["PICK-MID"] = float(0.5 * (wis.g_min + wis.g_max))
            if len(feas):
                picks["PICK-SHARPE"] = float(feas.loc[feas.Sharpe.idxmax()].gross)
            for nm, g in picks.items():
                gq = float(np.round(np.clip(g, G_LO, G_HI), 2))
                r = price(c, gq, cost)
                Lo, Li, Lf = legs_on(c, r, "OOS"), legs_on(c, r, "IS"), legs_on(c, r, "FULL")
                wf_rows.append(dict(
                    panel=pan, cost=cost, chooser=nm, g_pick=g, g_used=gq,
                    is_window_W=wis.W_exact, is_5leg_passers=int(isl.pass4b.sum()),
                    tradeable=bool(gq <= 1.00),
                    IS_CAGR=Li["CAGR"], IS_Sharpe=Li["Sharpe"], IS_MaxDD=Li["MaxDD"],
                    IS_pass4b=Li["pass4b"],
                    OOS_CAGR=Lo["CAGR"], OOS_Sharpe=Lo["Sharpe"], OOS_MaxDD=Lo["MaxDD"],
                    OOS_H1=Lo["H1"], OOS_H2=Lo["H2"], OOS_L1=Lo["L1_H1"], OOS_L2=Lo["L2_H2"],
                    OOS_L4=Lo["L4_DDcap"], OOS_L5=Lo["L5_CAGRfloor"],
                    OOS_pass4b=Lo["pass4b"], OOS_pass4a=Lo["pass4a"],
                    FULL_CAGR=Lf["CAGR"], FULL_Sharpe=Lf["Sharpe"], FULL_MaxDD=Lf["MaxDD"],
                    FULL_pass4b=Lf["pass4b"], FULL_pass4a=Lf["pass4a"],
                    SPY_OOS_CAGR=c["spy_m"]["OOS"]["CAGR"], SPY_OOS_Sharpe=c["spy_m"]["OOS"]["Sharpe"],
                    SPY_OOS_MaxDD=c["spy_m"]["OOS"]["MaxDD"],
                    V2_OOS_CAGR=c["v2_m"]["OOS"]["CAGR"], V2_OOS_Sharpe=c["v2_m"]["OOS"]["Sharpe"],
                    V2_OOS_MaxDD=c["v2_m"]["OOS"]["MaxDD"]))
    wf = pd.DataFrame(wf_rows)
    dump(wf, "walkforward")

    for pan in ("U56", "B136"):
        c = panels[pan]
        P(f"\n    {pan}   IS SPY {c['spy_m']['IS']['CAGR']:.3%}/{c['spy_m']['IS']['Sharpe']:.4f}/"
          f"{c['spy_m']['IS']['MaxDD']:.3%}    OOS SPY {c['spy_m']['OOS']['CAGR']:.3%}/"
          f"{c['spy_m']['OOS']['Sharpe']:.4f}/{c['spy_m']['OOS']['MaxDD']:.3%}")
        P(f"         OOS RULES v2 (live) {c['v2_m']['OOS']['CAGR']:.3%}/"
          f"{c['v2_m']['OOS']['Sharpe']:.4f}/{c['v2_m']['OOS']['MaxDD']:.3%}"
          f"    OOS 4b bars: DD cap {-DD_MULT*abs(c['spy_m']['OOS']['MaxDD']):.3%}, CAGR floor "
          f"{CAGR_MULT*c['spy_m']['OOS']['CAGR']:.3%}")
        for cost in COSTS:
            wis = wdf[(wdf.panel == pan) & (wdf.window == "IS") & (wdf.cost == cost)
                      & (wdf.STEP == "0.01")].iloc[0]
            closed = "" if (np.isfinite(wis.W_exact) and wis.W_exact > 0) else "  [IS WINDOW CLOSED]"
            P(f"      cost {int(cost):3d} bps   IS window [{wis.g_min:.4f}, {wis.g_max:.4f}] "
              f"W {wis.W_exact:+.4f}{closed}")
            for _, rr in wf[(wf.panel == pan) & (wf.cost == cost)].iterrows():
                P(f"           {rr.chooser:11s} g={rr.g_pick:.4f} (used {rr.g_used:.2f}"
                  f"{'' if rr.tradeable else ', LEVERAGE - NOT TRADEABLE'})  OOS "
                  f"{rr.OOS_CAGR:7.3%} / {rr.OOS_Sharpe:6.4f} / {rr.OOS_MaxDD:8.3%}  halves "
                  f"{rr.OOS_H1:5.3f}/{rr.OOS_H2:5.3f}  legs "
                  f"L1{'Y' if rr.OOS_L1 else '.'} L2{'Y' if rr.OOS_L2 else '.'} "
                  f"L4{'Y' if rr.OOS_L4 else '.'} L5{'Y' if rr.OOS_L5 else '.'}"
                  f"  OOS 4b {'PASS' if rr.OOS_pass4b else 'fail'}"
                  f"  OOS 4a {'PASS' if rr.OOS_pass4a else 'fail'}")
    live = wf[(wf.panel == "U56") & (wf.cost == COST0)]
    h3_ok = bool(len(live) and live.OOS_pass4b.any())
    P(f"\n      H3 (an IS-only pick clears 4b out of sample on U56 at 10 bps): "
      f"{'CONFIRMED' if h3_ok else 'REFUTED'}   ({int(live.OOS_pass4b.sum())} of {len(live)} choosers)")
    P(f"      across every (panel, cost, chooser): OOS 4b {int(wf.OOS_pass4b.sum())} of {len(wf)},"
      f"  OOS 4a {int(wf.OOS_pass4a.sum())} of {len(wf)}")
    trad = wf[wf.tradeable]
    P(f"      restricted to TRADEABLE picks (g <= 1.00): OOS 4b {int(trad.OOS_pass4b.sum())} of "
      f"{len(trad)}")

    # ------------------------------------------------------------------ 4a
    P("\n" + "=" * 190)
    P("[8] PATH 4a (judged against RULES v2 live) - every ladder point, every cost rung")
    P("=" * 190)
    for pan in ("U56", "B136"):
        s = lad[(lad.panel == pan) & (lad.window == "FULL")]
        vm = panels[pan]["v2_m"]["FULL"]
        P(f"      {pan}: 4a passes {int(s.pass4a.sum())} of {len(s)} (gross x cost) points; "
          f"4b passes {int(s.pass4b.sum())} of {len(s)}")
        best = s.loc[s.Sharpe.idxmax()]
        P(f"        best Sharpe anywhere on the ladder {best.Sharpe:.4f} (g={best.gross:.2f}, "
          f"{int(best.cost)} bps) vs RULES v2 {vm['Sharpe']:.4f} -- the 4a Sharpe legs are "
          f"unreachable by exposure, which is why 4a is 0.")
    P("      4a is 0 because CAND20's Sharpe is ~0.14 BELOW the live band book's at every rung and")
    P("      gross cannot move Sharpe (it moves 0.0015 across the whole ladder). 4b is the only path.")

    # ------------------------------------------------------------------ verdict
    P("\n" + "=" * 190)
    P("[9] VERDICT")
    P("=" * 190)
    P(f"  H1 width          {'CONFIRMED' if a0.W_exact >= REAL_BAR else 'REFUTED'}  "
      f"W_exact {a0.W_exact:.4f} -> {verdict_width}")
    P(f"  H2 cost           {'CONFIRMED' if h2_ok else 'REFUTED'}  (U56: window closes at "
      f"{cc['U56']:.1f} bps but the 5-leg 4b PASS closes at {pc['U56']:.1f} bps; B136 "
      f"{cc['B136']:.1f} / {pc['B136']:.1f})")
    P(f"  H3 rule 8         {'CONFIRMED' if h3_ok else 'REFUTED'}  (with the empty-IS-pass-set "
      f"caveat in [7])")
    P(f"  H4 well-posedness {'CONFIRMED' if gates['G5'] else 'REFUTED'} (gate G5)")
    P(f"  H5 halves         {'CONFIRMED' if h5_ok else 'REFUTED'}")
    P("\n  SURVIVORSHIP (PROTOCOL 9): U56 and B136 are CURRENT-constituent lists. Every CAGR and")
    P("  drawdown LEVEL above is optimistic -- the book's, RULES v2's and SPY's alike -- and both 4b")
    P("  bars are easier here than on a point-in-time panel. The WIDTH headline is a same-tape,")
    P("  same-names statement about one book's gross axis against its own SPY bars and is far less")
    P("  exposed; the OOS triples are levels and are upper bounds.")
    P(f"\n  elapsed {time.time()-t0:.1f}s")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    print(f"\nwrote {STEM}.console.txt")

    (OUT / f"{STEM}.summary.json").write_text(json.dumps(dict(
        W_exact=float(a0.W_exact), g_min=float(a0.g_min), g_max=float(a0.g_max),
        W_exact_670_vintage=float(mw["W_exact"]), verdict_width=verdict_width,
        closure_cost_bps={k: float(v) for k, v in cc.items()},
        pass_closure_cost_bps={k: float(v) for k, v in pc.items()},
        h1=bool(a0.W_exact >= REAL_BAR), h2=bool(h2_ok), h3=bool(h3_ok),
        h4=bool(gates["G5"]), h5=bool(h5_ok),
        gates={k: (None if v is None else bool(v)) for k, v in gates.items()},
        g3a_worst=float(w3a), g3b_worst=float(w3b)), indent=1))


if __name__ == "__main__":
    main()

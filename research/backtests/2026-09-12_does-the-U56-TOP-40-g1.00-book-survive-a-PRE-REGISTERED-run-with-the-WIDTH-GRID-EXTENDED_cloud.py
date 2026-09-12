#!/usr/bin/env python3
"""Idea 806 - does the U56 TOP-40 g1.00 book survive a PRE-REGISTERED run with the WIDTH
GRID EXTENDED to the panel's eligible ceiling?   (cloud lane, 2026-09-12)

WHY THIS RUN EXISTS
-------------------
Idea 589 swept 60 books (3 panels x 10 widths x 2 gross) and found exactly ONE that clears
PROTOCOL 4b on the full sample AND out of sample: U56, v1 eligibility, top 40 names by the
v1 composite, gross 1.00 spread g/n each with the rest in CASH, weekly rebalance
(12.54% / 1.13 / -17.9%; OOS 14.47% / 1.26 / -17.9%; 4b at 0, 10 and 25 bps).  It was
PARKED, not KEPT, on two grounds that this run tests directly:

  (1) it was the best of 60 cells read off a fully-swept grid, and it was NOT the rule-8
      in-sample pick (n = 20 was).  Choosing it after reading the grid is a third selection.
  (2) n = 40 was the width grid's ENDPOINT with Sharpe still rising in n, so the grid never
      contained the dial's argmax.  An endpoint argmax is not a measurement of a maximum.

This run fixes the book in advance, extends the width grid past 40 to the panel's eligible
ceiling so the argmax can be interior, and reads the cost ladder and a delayed-fill arm.

THE BOOK, FIXED BEFORE ANY RESULT IS READ
-----------------------------------------
panel      U56 = research/universe.json, 55 tradeable names.  SPY is the BENCHMARK and is
           excluded from the tradeable set (idea 589's convention; holding the benchmark
           inside a ranked book contaminates a width measurement).
eligible   v1 eligibility, unchanged: priced, close > its own 200d mean, vol20 < 0.60.
score      the v1 composite exactly as research/scan.py / baseline.score computes it
           (mom/r6/r3 percentile ranks, x (0.5 + 0.5 * above200d), / sqrt(vol20)).
weights    w_i = g / n for the top-n eligible names by that score, 0 otherwise.  Fewer than
           n eligible names => the book runs BELOW g and the remainder sits in CASH
           (de-gross, never re-spread) - the record's standing convention.
gross      g = 1.00, FIXED.  Not a dial in this run.
cadence    weekly (freq 'W'), PROTOCOL rule 2 next-day fill (lag 1).

TUNED PARAMETERS: TWO, exactly as the queue allows and PROTOCOL rule 4 permits -
  (1) WIDTH n, on the extended grid below;
  (2) COST rung.
Everything else is a REPORTED-NEVER-SELECTED axis: execution lag (1, 2, 3 trading days) and
the IS/OOS split.  Gross, panel, eligibility, score and cadence are pinned by the queue.

THE EXTENDED WIDTH GRID, AND WHY IT REACHES THE CEILING
-------------------------------------------------------
U56 carries 55 tradeable names; the v1-eligible count has median 40 and maximum 54 over the
scored sample.  So n = 40 - idea 589's endpoint - sits exactly AT the median eligible count,
which is the first thing this grid can distinguish: above it the book de-grosses more than
half the time by construction.  The grid runs

    n in {5, 10, 15, 20, 25, 30, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 55}

i.e. 17 rungs, dense around 40, terminating at n = 55 = EVERY tradeable name, the panel's
hard ceiling (at n = 55 the book can never reach gross 1.00, since at least one name is
always ineligible).  Any interior argmax is therefore a real interior argmax, and an argmax
that still sits at the ceiling would mean "hold the whole panel", not "hold 40 names".

COSTS: 0 / 5 / 10 / 25 / 50 bps.  10 bps is the PROTOCOL headline.  The ladder comes off one
run per (width, lag) because cost is a same-day subtraction from the return path, not a
change to the holdings: r(c) = r_gross - turnover * c / 1e4.  Gate G3 proves that identity
against engine.backtest(cost_bps=...) to 0.

PRE-REGISTERED HYPOTHESES (declared here, before the grid is read; every one is reported
whichever way it falls)
-----------------------------------------------------------------------------------------
  H_REPRO   : the n = 40 cell reproduces idea 589's committed headline
              12.54% / 1.13 / -17.9% (full) and 14.47% / 1.26 / -17.9% (OOS), |dSharpe| <= 0.02.
  H_40      : n = 40 passes 4b on the full sample at 10 bps (589's claim, re-read alone).
  H_INTERIOR: with the grid at the ceiling, the full-sample Sharpe argmax is INTERIOR -
              neither n = 5 nor n = 55.  If the argmax is still the top rung, the dial has
              no maximum on this panel and 589's n = 40 was an artefact of where it stopped.
  H_PICK    : the rule-8 pick - n chosen on the IS window (..2016-12-31) by IS Sharpe ALONE,
              ties to the SMALLER n, OOS (2017-01-01..) read exactly once - passes 4b OOS.
              THIS IS THE RUN'S REAL TEST.  589's 4b passer was not this pick.
  H_PICK40  : the rule-8 IS pick IS n = 40, i.e. a pre-registered selector would have chosen
              the book the record parked.
  H_COST    : the rule-8 pick passes 4b at every cost rung through 25 bps.
  H_DELAY   : the rule-8 pick passes 4b at lag 2 (one extra trading day of fill delay),
              10 bps.  Reported at lag 3 beside it.
  H_NEIGH   : the rule-8 pick's 4b pass is not a knife edge - both adjacent width rungs also
              pass 4b on the same window.

GATES (run first, printed, and all four must pass before any verdict is read)
  G1 the book function reproduces baseline.rules_v1_weights(px[trade], n, w=g/n) exactly.
  G2 the vectorised runner reproduces products/backtester/engine.backtest on the headline
     cell (returns and turnover paths) to <= 1e-9.
  G3 the derived cost ladder equals engine.backtest(cost_bps=c) for c = 25 to <= 1e-9.
  G4 the eligible-count ceiling is what this file claims (max eligible < 55).

SURVIVORSHIP CAVEAT, stated up front: research/universe.json is a CURRENT-constituent list,
so every LEVEL here is optimistic, and widening flatters most - adding low-ranked names adds
survivors that were never at risk of delisting.  That bias works in the same direction as the
finding this run is testing, which is the honest reason to distrust a wide-book 4b pass.

OUTPUTS (all committed under research/backtests/)
  .console.txt     full log
  .grid.csv        17 widths x 5 costs x 3 lags = 255 cells, ALL reported
  .walkforward.csv rule-8 IS grid, the IS pick, the OOS read, vs RULES v2 and SPY
  .keeppaths.csv   4a / 4b verdicts and binding legs on every cell
  .result.md       the answer
RULES.md, PROTOCOL.md, research/scan.py, products/bot/bot.py and research/baseline.py are
NOT modified by this script.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa: E402
from engine import backtest, metrics, rebalance_mask                           # noqa: E402

DATE = "2026-09-12"
SLUG = "does-the-U56-TOP-40-g1.00-book-survive-a-PRE-REGISTERED-run-with-the-WIDTH-GRID-EXTENDED"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

# ---------------- pre-registered constants ------------------------------------------------
WIDTHS = [5, 10, 15, 20, 25, 30, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 55]
GROSS = 1.00                      # FIXED by the queue
COSTS = [0, 5, 10, 25, 50]        # tuned dial 2
COST_MAIN = 10
LAGS = [1, 2, 3]                  # reported, never selected (1 = PROTOCOL next-day fill)
LAG_MAIN = 1
FREQ = "W"
MAXVOL = 0.60
IS_END, OOS_START = "2016-12-31", "2017-01-01"
N_PARKED = 40                     # idea 589's parked width
WARMUP = 260                      # baseline.compare's convention

# idea 589's committed headline for the n=40 / g=1.00 / 10 bps cell (CHANGELOG 2026-09-12)
PUB = dict(CAGR=0.1254, Sharpe=1.13, MaxDD=-0.179, OOS_CAGR=0.1447, OOS_Sharpe=1.26, OOS_MaxDD=-0.179)
PUB_TOL_SHARPE = 0.02
PUB_TOL_CAGR = 0.005
PUB_TOL_DD = 0.01

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ---------------- book --------------------------------------------------------------------
def elig_rank(px: pd.DataFrame, trade: list[str]):
    q = px[trade]
    s, above, vol20 = score(q)
    elig = s.where(above & (vol20 < MAXVOL))
    return elig, elig.rank(axis=1, ascending=False)


def book(px: pd.DataFrame, rk: pd.DataFrame, n: int, g: float = GROSS) -> pd.DataFrame:
    w = (rk <= n).astype(float) * (g / n)
    return w.reindex(columns=px.columns).fillna(0.0)


# ---------------- vectorised runner (idea 804/805's, re-gated here) -----------------------
def fast_run(prices: pd.DataFrame, weights: pd.DataFrame, mask: pd.Series, lag: int):
    """(gross return path before costs, turnover path, realised gross path).  Costs are
    applied afterwards: r(c) = r_gross - turn * c / 1e4, exact because the engine subtracts
    cost from the same day's return rather than changing the holdings (gate G3)."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(lag).fillna(0.0).values
    mk = mask.shift(lag, fill_value=False).values.copy()
    mk[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mk)
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
    return (pd.Series((held * rets).sum(axis=1), index=idx),
            pd.Series(turn, index=idx),
            pd.Series(held.sum(axis=1), index=idx))


# ---------------- PROTOCOL rule 4 ---------------------------------------------------------
def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]


def legs_4b(r, spy):
    """PROTOCOL 4b as five booleans over the FULL sample (ideas 574 / 804 / 805 arithmetic)."""
    a1, a2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    return {"H1": bool(a1 > s1), "H2": bool(a2 > s2),
            "OOS": bool(metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"]),
            "DD": bool(m["MaxDD"] >= 0.60 * ms["MaxDD"]),
            "CAGR": bool(m["CAGR"] >= 0.70 * ms["CAGR"])}


def legs_4b_window(r, spy, lo=None, hi=None):
    """The same five legs measured INSIDE one window.  The OOS leg collapses into that
    window's own second half (the same object as H2) - named and reported, not hidden."""
    rr, ss = r.loc[lo:hi], spy.loc[lo:hi]
    a1, a2 = halves(rr)
    s1, s2 = halves(ss)
    m, ms = metrics(rr), metrics(ss)
    return {"H1": bool(a1 > s1), "H2": bool(a2 > s2), "OOS": bool(a2 > s2),
            "DD": bool(m["MaxDD"] >= 0.60 * ms["MaxDD"]),
            "CAGR": bool(m["CAGR"] >= 0.70 * ms["CAGR"])}


def keep_4a(r, b):
    a1, a2 = halves(r)
    b1, b2 = halves(b)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(b)["MaxDD"])


def keep_4a_window(r, b, lo=None, hi=None):
    rr, bb = r.loc[lo:hi], b.loc[lo:hi]
    a1, a2 = halves(rr)
    b1, b2 = halves(bb)
    return bool(a1 > b1 and a2 > b2 and metrics(rr)["MaxDD"] >= metrics(bb)["MaxDD"])


def triple(r, lo=None, hi=None):
    m = metrics(r.loc[lo:hi])
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def spearman(x, y):
    """Spearman rho without scipy (the sandbox has pandas/numpy only).  Named, per idea 564."""
    a, b = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3:
        return float("nan")
    ra = pd.Series(a[ok]).rank().values
    rb = pd.Series(b[ok]).rank().values
    return float(np.corrcoef(ra, rb)[0, 1])


def main():
    t0 = time.time()
    P(f"# Idea 806 - {SLUG}")
    P(f"# cloud lane, {DATE}.  Book FIXED in advance: U56 / v1 eligibility / top-n by the v1")
    P(f"# composite / w = {GROSS:.2f}/n each / rest CASH / weekly / next-day fill.")
    P(f"# TUNED: width n ({len(WIDTHS)} rungs) and cost ({len(COSTS)} rungs).  REPORTED-NEVER-SELECTED:")
    P(f"# execution lag {LAGS}, and the IS/OOS split.  IS ..{IS_END}  OOS {OOS_START}..")
    P("# SURVIVORSHIP: universe.json is a CURRENT-constituent list - every level is optimistic,")
    P("# and widening flatters most, because the names a wide book adds are survivors.")

    px = load_universe().dropna(how="all").ffill()
    trade = [c for c in px.columns if c != "SPY"]
    elig, rk = elig_rank(px, trade)
    mask0 = rebalance_mask(px.index, FREQ)
    start = px.index[WARMUP]
    spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
    base_res = backtest(px, rules_v2_weights(px), cost_bps=0, freq=FREQ)
    base = (base_res["returns"] - base_res["turnover"] * COST_MAIN / 1e4).loc[start:]

    ec = elig.loc[start:].notna().sum(axis=1)
    P(f"\npanel U56: {len(trade)} tradeable names (SPY excluded from the book), "
      f"{len(px.loc[start:])} scored days {start.date()}..{px.index[-1].date()}")
    P(f"v1-eligible count: min {ec.min()}  p05 {ec.quantile(.05):.0f}  median {ec.median():.0f}  "
      f"p95 {ec.quantile(.95):.0f}  MAX {ec.max()}   (n={N_PARKED} sits at the "
      f"{(ec <= N_PARKED).mean():.1%} quantile of the eligible count)")

    # ================================ GATES =============================================
    P("\n" + "=" * 100)
    P("GATES (all four must pass before any verdict is read)")
    P("=" * 100)
    w40 = book(px, rk, N_PARKED)
    w_ref = rules_v1_weights(px[trade], n=N_PARKED, w=GROSS / N_PARKED).reindex(columns=px.columns).fillna(0.0)
    g1 = float(np.abs(w40.values - w_ref.values).max())
    eng0 = backtest(px, w40, cost_bps=0, freq=FREQ)
    fr, ft, fg = fast_run(px, w40, mask0, LAG_MAIN)
    # engine.backtest emits NaN on row 0 (it reads shift(1) weights before any rebalance has
    # happened), so G2/G3 are measured over the SCORED sample start.. - exactly the window
    # every metric in this file uses.  fast_run itself is NaN-free.
    g2 = max(float(np.abs(eng0["returns"].loc[start:].values - fr.loc[start:].values).max()),
             float(np.abs(eng0["turnover"].loc[start:].values - ft.loc[start:].values).max()))
    eng25 = backtest(px, w40, cost_bps=25, freq=FREQ)
    g3 = float(np.abs((fr - ft * 25 / 1e4).loc[start:].values - eng25["returns"].loc[start:].values).max())
    g4 = int(ec.max()) < len(trade)
    for nm, v, ok in [("G1 book == baseline.rules_v1_weights(n,w=g/n)", f"max|dw| {g1:.3e}", g1 < 1e-12),
                      ("G2 fast_run == engine.backtest (returns, turnover)", f"max|d| {g2:.3e}", g2 < 1e-9),
                      ("G3 derived cost rung == engine.backtest(cost_bps=25)", f"max|d| {g3:.3e}", g3 < 1e-9),
                      ("G4 max eligible < tradeable count (ceiling is real)", f"{ec.max()} < {len(trade)}", g4)]:
        P(f"   {nm:<52} {v:<22} {'PASS' if ok else 'FAIL'}")
    assert g1 < 1e-12 and g2 < 1e-9 and g3 < 1e-9 and g4, "a gate failed - no verdict is read"

    # ================================ MAIN GRID =========================================
    P("\n" + "=" * 100)
    P(f"MAIN GRID - {len(WIDTHS)} widths x {len(COSTS)} costs x {len(LAGS)} lags = "
      f"{len(WIDTHS)*len(COSTS)*len(LAGS)} cells, ALL REPORTED")
    P("=" * 100)
    W = {n: book(px, rk, n) for n in WIDTHS}
    paths: dict[tuple, pd.Series] = {}
    rows, keeprows = [], []
    for lag in LAGS:
        for n in WIDTHS:
            rg, tn, gr = fast_run(px, W[n], mask0, lag)
            rg, tn, gr = rg.loc[start:], tn.loc[start:], gr.loc[start:]
            yrs = len(rg) / 252
            for cb in COSTS:
                r = rg - tn * cb / 1e4
                paths[(lag, n, cb)] = r
                m, mi, mo = metrics(r), metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
                L = legs_4b(r, spy)
                LO = legs_4b_window(r, spy, OOS_START, None)
                rows.append(dict(lag=lag, n=n, gross=GROSS, cost_bps=cb,
                                 CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], Vol=m["Vol"],
                                 H1=halves(r)[0], H2=halves(r)[1],
                                 IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                                 OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                 turn_per_yr=float(tn.sum() / yrs), mean_gross=float(gr.mean()),
                                 pass_4a=keep_4a(r, base), pass_4b=all(L.values()),
                                 fail_4b="+".join(k for k in LEGS if not L[k]) or "-none-",
                                 pass_4a_OOS=keep_4a_window(r, base, OOS_START, None),
                                 pass_4b_OOS=all(LO.values()),
                                 fail_4b_OOS="+".join(k for k in LEGS if not LO[k]) or "-none-"))
                keeprows.append(dict(lag=lag, n=n, cost_bps=cb, window="full",
                                     **{f"leg_{k}": L[k] for k in LEGS},
                                     pass_4b=all(L.values()), pass_4a=keep_4a(r, base)))
                keeprows.append(dict(lag=lag, n=n, cost_bps=cb, window="OOS",
                                     **{f"leg_{k}": LO[k] for k in LEGS},
                                     pass_4b=all(LO.values()),
                                     pass_4a=keep_4a_window(r, base, OOS_START, None)))
    grid = pd.DataFrame(rows)
    grid.to_csv(f"{OUT}.grid.csv", index=False)
    pd.DataFrame(keeprows).to_csv(f"{OUT}.keeppaths.csv", index=False)

    mS, mB = metrics(spy), metrics(base)
    oS, oB = metrics(spy.loc[OOS_START:]), metrics(base.loc[OOS_START:])
    iS, iB = metrics(spy.loc[:IS_END]), metrics(base.loc[:IS_END])
    s1, s2 = halves(spy)
    P(f"\ncomparands on the scored sample ({start.date()}..):")
    P(f"   SPY        full {mS['CAGR']:>7.2%} / {mS['Sharpe']:.3f} / {mS['MaxDD']:>7.2%}   "
      f"halves {s1:.3f} / {s2:.3f}   IS {iS['CAGR']:.2%}/{iS['Sharpe']:.3f}/{iS['MaxDD']:.2%}   "
      f"OOS {oS['CAGR']:.2%}/{oS['Sharpe']:.3f}/{oS['MaxDD']:.2%}")
    P(f"   RULES v2   full {mB['CAGR']:>7.2%} / {mB['Sharpe']:.3f} / {mB['MaxDD']:>7.2%}   "
      f"halves {halves(base)[0]:.3f} / {halves(base)[1]:.3f}   "
      f"IS {iB['CAGR']:.2%}/{iB['Sharpe']:.3f}/{iB['MaxDD']:.2%}   "
      f"OOS {oB['CAGR']:.2%}/{oB['Sharpe']:.3f}/{oB['MaxDD']:.2%}")
    P(f"   4b bars: Sharpe > SPY in BOTH halves and OOS; MaxDD >= {0.60*mS['MaxDD']:.2%}; "
      f"CAGR >= {0.70*mS['CAGR']:.2%}   (OOS-window bars: DD >= {0.60*oS['MaxDD']:.2%}, "
      f"CAGR >= {0.70*oS['CAGR']:.2%})")

    # ---- H_REPRO
    P("\n" + "-" * 100)
    P(f"G5 / H_REPRO - idea 589's n={N_PARKED} cell, re-read alone at {COST_MAIN} bps, lag {LAG_MAIN}")
    P("-" * 100)
    r40 = paths[(LAG_MAIN, N_PARKED, COST_MAIN)]
    c, s, dd = triple(r40)
    oc, os_, odd = triple(r40, OOS_START, None)
    P(f"   committed  full {PUB['CAGR']:.2%} / {PUB['Sharpe']:.2f} / {PUB['MaxDD']:.1%}    "
      f"OOS {PUB['OOS_CAGR']:.2%} / {PUB['OOS_Sharpe']:.2f} / {PUB['OOS_MaxDD']:.1%}")
    P(f"   this run   full {c:.2%} / {s:.2f} / {dd:.1%}    OOS {oc:.2%} / {os_:.2f} / {odd:.1%}")
    H_REPRO = (abs(s - PUB["Sharpe"]) <= PUB_TOL_SHARPE and abs(os_ - PUB["OOS_Sharpe"]) <= PUB_TOL_SHARPE
               and abs(c - PUB["CAGR"]) <= PUB_TOL_CAGR and abs(oc - PUB["OOS_CAGR"]) <= PUB_TOL_CAGR
               and abs(dd - PUB["MaxDD"]) <= PUB_TOL_DD and abs(odd - PUB["OOS_MaxDD"]) <= PUB_TOL_DD)
    P(f"   deltas Sharpe {s-PUB['Sharpe']:+.4f} / OOS {os_-PUB['OOS_Sharpe']:+.4f}, "
      f"CAGR {c-PUB['CAGR']:+.4f} / OOS {oc-PUB['OOS_CAGR']:+.4f}, "
      f"MaxDD {dd-PUB['MaxDD']:+.4f} / OOS {odd-PUB['OOS_MaxDD']:+.4f}")
    P(f"   H_REPRO (tol Sharpe {PUB_TOL_SHARPE}, CAGR {PUB_TOL_CAGR}, DD {PUB_TOL_DD}): "
      f"{'PASS' if H_REPRO else 'FAIL'}")
    P("   NOTE data/prices.csv is re-downloaded daily, so U56 rows reproduce to ~3e-3, not")
    P("   bit-exact (idea 406); the tolerances above are set for that, not for noise hiding.")

    # ---- A. the width ladder
    P("\n" + "=" * 100)
    P(f"A. WIDTH LADDER at the PROTOCOL cost ({COST_MAIN} bps), lag {LAG_MAIN}, g = {GROSS:.2f}")
    P("   EVERY rung reported.  The grid reaches n = 55 = the whole tradeable panel.")
    P("=" * 100)
    ml = grid[(grid.lag == LAG_MAIN) & (grid.cost_bps == COST_MAIN)].set_index("n")
    P(f"{'n':>4} {'mgross':>7} {'CAGR':>8} {'Sharpe':>7} {'MaxDD':>8} {'H1':>6} {'H2':>6} "
      f"{'ISSh':>6} {'OOSCAGR':>8} {'OOSSh':>6} {'OOSDD':>8} {'turn':>6}  {'fail4b':<16} "
      f"{'4b':>4} {'4a':>4} {'4bOOS':>6}")
    for n in WIDTHS:
        r = ml.loc[n]
        P(f"{n:>4} {r.mean_gross:>7.3f} {r.CAGR:>8.2%} {r.Sharpe:>7.3f} {r.MaxDD:>8.2%} "
          f"{r.H1:>6.3f} {r.H2:>6.3f} {r.IS_Sharpe:>6.3f} {r.OOS_CAGR:>8.2%} {r.OOS_Sharpe:>6.3f} "
          f"{r.OOS_MaxDD:>8.2%} {r.turn_per_yr:>6.2f}  {r.fail_4b:<16} "
          f"{'PASS' if r.pass_4b else 'fail':>4} {'PASS' if r.pass_4a else 'fail':>4} "
          f"{'PASS' if r.pass_4b_OOS else 'fail':>6}")
    n_argmax = int(ml["Sharpe"].idxmax())
    n_argmax_oos = int(ml["OOS_Sharpe"].idxmax())
    H_INTERIOR = n_argmax not in (WIDTHS[0], WIDTHS[-1])
    H_40 = bool(ml.loc[N_PARKED, "pass_4b"])
    band = [n for n in WIDTHS if ml.loc[n, "pass_4b"]]
    band_oos = [n for n in WIDTHS if ml.loc[n, "pass_4b_OOS"]]
    P(f"\n   full-sample Sharpe argmax n = {n_argmax} (Sharpe {ml['Sharpe'].max():.3f}); "
      f"OOS Sharpe argmax n = {n_argmax_oos}")
    P(f"   H_INTERIOR (argmax not at a grid endpoint {WIDTHS[0]} or {WIDTHS[-1]}): "
      f"{'PASS' if H_INTERIOR else 'FAIL'}")
    P(f"   H_40 (n={N_PARKED} passes 4b on the full sample at {COST_MAIN} bps): "
      f"{'PASS' if H_40 else 'FAIL'}")
    P(f"   4b-pass width band, full sample: {band if band else 'EMPTY'}  "
      f"({len(band)} of {len(WIDTHS)} rungs)")
    P(f"   4b-pass width band, OOS window : {band_oos if band_oos else 'EMPTY'}  "
      f"({len(band_oos)} of {len(WIDTHS)} rungs)")
    P(f"   Sharpe spread over the ladder {ml['Sharpe'].max()-ml['Sharpe'].min():.4f}; "
      f"OOS Sharpe spread {ml['OOS_Sharpe'].max()-ml['OOS_Sharpe'].min():.4f}; "
      f"MaxDD spread {ml['MaxDD'].max()-ml['MaxDD'].min():.2%}")

    # ---- B. rule 8 walk-forward
    P("\n" + "=" * 100)
    P(f"B. RULE 8 WALK-FORWARD - n chosen on IS ({start.date()}..{IS_END}) by IS SHARPE ALONE,")
    P(f"   ties to the SMALLER n; OOS ({OOS_START}..) read exactly ONCE.  {COST_MAIN} bps, lag {LAG_MAIN}.")
    P("=" * 100)
    isl = ml["IS_Sharpe"]
    n_pick = int(min(isl[isl == isl.max()].index))
    H_PICK40 = n_pick == N_PARKED
    P(f"   IS Sharpe by width: " + "  ".join(f"{n}:{isl.loc[n]:.3f}" for n in WIDTHS))
    P(f"   IS pick n* = {n_pick} (IS Sharpe {isl.max():.4f}); full-sample argmax was {n_argmax}; "
      f"|n* - argmax| = {abs(n_pick-n_argmax)}")
    P(f"   H_PICK40 (the pre-registered selector picks idea 589's n={N_PARKED}): "
      f"{'PASS' if H_PICK40 else 'FAIL'}")
    rho = spearman(ml["IS_Sharpe"].values, ml["OOS_Sharpe"].values)
    rho_tail = spearman(ml["IS_Sharpe"].loc[10:].values, ml["OOS_Sharpe"].loc[10:].values)
    P(f"   Spearman(IS Sharpe, OOS Sharpe) over the {len(WIDTHS)} rungs: {rho:+.3f}; "
      f"excluding n=5 (the one degenerate rung): {rho_tail:+.3f}")
    P(f"   IS Sharpe spread over the 16 non-degenerate rungs "
      f"{ml['IS_Sharpe'].loc[10:].max()-ml['IS_Sharpe'].loc[10:].min():.4f} vs OOS spread "
      f"{ml['OOS_Sharpe'].loc[10:].max()-ml['OOS_Sharpe'].loc[10:].min():.4f} "
      f"- the IS objective the selector maximises is ~{(ml['OOS_Sharpe'].loc[10:].max()-ml['OOS_Sharpe'].loc[10:].min())/(ml['IS_Sharpe'].loc[10:].max()-ml['IS_Sharpe'].loc[10:].min()):.1f}x FLATTER than what it is choosing over.")

    wf = []
    for nm, nsel in [("IS-SHARPE (pre-declared)", n_pick),
                     ("589's PARKED n=40", N_PARKED),
                     ("full-sample argmax (ORACLE, not a selector)", n_argmax)]:
        r = paths[(LAG_MAIN, nsel, COST_MAIN)]
        LO = legs_4b_window(r, spy, OOS_START, None)
        oc, os_, odd = triple(r, OOS_START, None)
        wf.append(dict(selector=nm, n=nsel, OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=odd,
                       OOS_4b=all(LO.values()),
                       OOS_fail="+".join(k for k in LEGS if not LO[k]) or "-none-",
                       OOS_4a=keep_4a_window(r, base, OOS_START, None),
                       SPY_OOS_CAGR=oS["CAGR"], SPY_OOS_Sharpe=oS["Sharpe"], SPY_OOS_MaxDD=oS["MaxDD"],
                       V2_OOS_CAGR=oB["CAGR"], V2_OOS_Sharpe=oB["Sharpe"], V2_OOS_MaxDD=oB["MaxDD"]))
    P(f"\n   {'selector':<44} {'n':>4} {'OOSCAGR':>9} {'OOSSh':>7} {'OOSDD':>8}  "
      f"{'fail4b(OOS)':<14} {'4bOOS':>6} {'4aOOS':>6}")
    for w in wf:
        P(f"   {w['selector']:<44} {w['n']:>4} {w['OOS_CAGR']:>9.2%} {w['OOS_Sharpe']:>7.3f} "
          f"{w['OOS_MaxDD']:>8.2%}  {w['OOS_fail']:<14} "
          f"{'PASS' if w['OOS_4b'] else 'fail':>6} {'PASS' if w['OOS_4a'] else 'fail':>6}")
    P(f"   {'SPY (OOS comparand)':<44} {'-':>4} {oS['CAGR']:>9.2%} {oS['Sharpe']:>7.3f} {oS['MaxDD']:>8.2%}")
    P(f"   {'RULES v2 (OOS comparand)':<44} {'-':>4} {oB['CAGR']:>9.2%} {oB['Sharpe']:>7.3f} {oB['MaxDD']:>8.2%}")
    H_PICK = bool(wf[0]["OOS_4b"])
    P(f"\n   H_PICK (the rule-8 IS pick passes 4b OUT OF SAMPLE): {'PASS' if H_PICK else 'FAIL'}")

    # neighbours of the pick
    i = WIDTHS.index(n_pick)
    nb = [WIDTHS[j] for j in (i - 1, i + 1) if 0 <= j < len(WIDTHS)]
    nb_ok = []
    for n in nb:
        LO = legs_4b_window(paths[(LAG_MAIN, n, COST_MAIN)], spy, OOS_START, None)
        nb_ok.append(all(LO.values()))
        P(f"   neighbour n={n}: OOS 4b {'PASS' if all(LO.values()) else 'fail'} "
          f"({'+'.join(k for k in LEGS if not LO[k]) or '-none-'})")
    H_NEIGH = bool(nb_ok) and all(nb_ok)
    P(f"   H_NEIGH (both adjacent rungs also pass 4b OOS): {'PASS' if H_NEIGH else 'FAIL'}")

    # ---- B2. POST-HOC selectors: could ANY IS-only rule have reached the band?
    P("\n" + "-" * 100)
    P("B2. POST-HOC SELECTORS - declared AFTER the IS-SHARPE result above was read, and")
    P("    labelled post-hoc for that reason.  They are NOT part of this run's verdict; they")
    P("    exist to tell the next run whether any IS-ONLY rule could have reached the 4b band,")
    P("    or whether the band is only visible once the full sample has been read.")
    P("    Each one uses IS data ONLY, and the OOS window is read once per selector.")
    P("-" * 100)
    is_paths = {n: paths[(LAG_MAIN, n, COST_MAIN)].loc[:IS_END] for n in WIDTHS}
    spy_is = spy.loc[:IS_END]
    is_m = {n: metrics(is_paths[n]) for n in WIDTHS}
    is_legs = {n: legs_4b_window(paths[(LAG_MAIN, n, COST_MAIN)], spy, None, IS_END) for n in WIDTHS}
    is_band = [n for n in WIDTHS if all(is_legs[n].values())]
    cal = pd.Series({n: is_m[n]["Calmar"] for n in WIDTHS})
    n_cal = int(min(cal[cal == cal.max()].index))
    dd_bar = 0.60 * metrics(spy_is)["MaxDD"]
    feas = [n for n in WIDTHS if is_m[n]["MaxDD"] >= dd_bar]
    n_feas = int(min(feas)) if feas else None
    n_mid = int(is_band[len(is_band) // 2]) if is_band else None
    P(f"    IS-window 4b band (IS data only): {is_band if is_band else 'EMPTY'}")
    P(f"    IS DD cap (0.60 x SPY IS MaxDD) = {dd_bar:.2%}; widths clearing it in-sample: "
      f"{feas if feas else 'NONE'}")
    P(f"    IS Calmar by width: " + "  ".join(f"{n}:{cal.loc[n]:.2f}" for n in WIDTHS))
    posthoc = []
    for nm, nsel in [("IS-CALMAR (post-hoc)", n_cal),
                     ("IS-DD-FEASIBLE smallest n (post-hoc)", n_feas),
                     ("IS-4b-BAND-MIDPOINT (post-hoc)", n_mid)]:
        if nsel is None:
            P(f"    {nm:<40} EMPTY - the selector has nothing to pick")
            continue
        r = paths[(LAG_MAIN, nsel, COST_MAIN)]
        LO = legs_4b_window(r, spy, OOS_START, None)
        oc2, os2, odd2 = triple(r, OOS_START, None)
        posthoc.append(dict(selector=nm, n=nsel, OOS_CAGR=oc2, OOS_Sharpe=os2, OOS_MaxDD=odd2,
                            OOS_4b=all(LO.values()),
                            OOS_fail="+".join(k for k in LEGS if not LO[k]) or "-none-",
                            OOS_4a=keep_4a_window(r, base, OOS_START, None),
                            SPY_OOS_CAGR=oS["CAGR"], SPY_OOS_Sharpe=oS["Sharpe"],
                            SPY_OOS_MaxDD=oS["MaxDD"], V2_OOS_CAGR=oB["CAGR"],
                            V2_OOS_Sharpe=oB["Sharpe"], V2_OOS_MaxDD=oB["MaxDD"], posthoc=True))
        P(f"    {nm:<40} n={nsel:<4} OOS {oc2:>7.2%} / {os2:.3f} / {odd2:>7.2%}  "
          f"fail4b {posthoc[-1]['OOS_fail']:<10} "
          f"{'PASS' if all(LO.values()) else 'fail'}")
    n_posthoc_pass = sum(1 for p in posthoc if p["OOS_4b"])
    P(f"    {n_posthoc_pass} of {len(posthoc)} post-hoc IS-only selectors reach a 4b pass OOS.")
    pd.DataFrame([dict(w, posthoc=False) for w in wf] + posthoc).to_csv(
        f"{OUT}.walkforward.csv", index=False)

    # ---- C. cost ladder at the pick and at 40
    P("\n" + "=" * 100)
    P(f"C. COST LADDER, lag {LAG_MAIN} - at the rule-8 pick n={n_pick} and at 589's n={N_PARKED}")
    P("=" * 100)
    H_COST = True
    for nsel in sorted({n_pick, N_PARKED}):
        P(f"\n   n = {nsel}")
        P(f"   {'bps':>4} {'CAGR':>8} {'Sharpe':>7} {'MaxDD':>8} {'OOSCAGR':>8} {'OOSSh':>6} "
          f"{'OOSDD':>8}  {'fail4b':<16} {'4b':>4} {'4bOOS':>6}")
        cl = grid[(grid.lag == LAG_MAIN) & (grid.n == nsel)].set_index("cost_bps")
        for cb in COSTS:
            r = cl.loc[cb]
            P(f"   {cb:>4} {r.CAGR:>8.2%} {r.Sharpe:>7.3f} {r.MaxDD:>8.2%} {r.OOS_CAGR:>8.2%} "
              f"{r.OOS_Sharpe:>6.3f} {r.OOS_MaxDD:>8.2%}  {r.fail_4b:<16} "
              f"{'PASS' if r.pass_4b else 'fail':>4} {'PASS' if r.pass_4b_OOS else 'fail':>6}")
        if nsel == n_pick:
            H_COST = all(bool(cl.loc[cb, "pass_4b_OOS"]) for cb in COSTS if cb <= 25)

    P(f"\n   H_COST (the rule-8 pick passes 4b OOS at every rung through 25 bps): "
      f"{'PASS' if H_COST else 'FAIL'}")
    # cost breakeven on the OOS 4b verdict at the pick
    cl = grid[(grid.lag == LAG_MAIN) & (grid.n == n_pick)].set_index("cost_bps")
    passing = [cb for cb in COSTS if bool(cl.loc[cb, "pass_4b_OOS"])]
    P(f"   cost rungs where n={n_pick} passes 4b OOS: {passing if passing else 'NONE'}")

    # ---- D. delayed fill
    P("\n" + "=" * 100)
    P(f"D. EXECUTION-DELAY LADDER at {COST_MAIN} bps (lag 1 = PROTOCOL next-day fill)")
    P("=" * 100)
    H_DELAY = True
    for nsel in sorted({n_pick, N_PARKED}):
        P(f"\n   n = {nsel}")
        P(f"   {'lag':>4} {'CAGR':>8} {'Sharpe':>7} {'MaxDD':>8} {'H1':>6} {'H2':>6} {'OOSCAGR':>8} "
          f"{'OOSSh':>6}  {'fail4b':<16} {'4b':>4} {'4bOOS':>6}")
        dl = grid[(grid.n == nsel) & (grid.cost_bps == COST_MAIN)].set_index("lag")
        for lag in LAGS:
            r = dl.loc[lag]
            P(f"   {lag:>4} {r.CAGR:>8.2%} {r.Sharpe:>7.3f} {r.MaxDD:>8.2%} {r.H1:>6.3f} "
              f"{r.H2:>6.3f} {r.OOS_CAGR:>8.2%} {r.OOS_Sharpe:>6.3f}  {r.fail_4b:<16} "
              f"{'PASS' if r.pass_4b else 'fail':>4} {'PASS' if r.pass_4b_OOS else 'fail':>6}")
        if nsel == n_pick:
            H_DELAY = bool(dl.loc[2, "pass_4b_OOS"])
    P(f"\n   H_DELAY (the rule-8 pick passes 4b OOS with a +1-day fill, lag 2): "
      f"{'PASS' if H_DELAY else 'FAIL'}")

    # ---- E. full census over all 255 cells
    P("\n" + "=" * 100)
    P("E. CENSUS over all 255 cells")
    P("=" * 100)
    P(f"   4b passes, full sample: {int(grid.pass_4b.sum())} of {len(grid)}; "
      f"4b passes, OOS window: {int(grid.pass_4b_OOS.sum())}; "
      f"4a passes, full sample: {int(grid.pass_4a.sum())}; 4a OOS: {int(grid.pass_4a_OOS.sum())}")
    P("   binding 4b legs (full sample), most common first:")
    for k, v in grid.fail_4b.value_counts().items():
        P(f"      {k:<22} {v:>4}")
    P("   4b pass count by cost rung (full / OOS):")
    for cb in COSTS:
        sub = grid[grid.cost_bps == cb]
        P(f"      {cb:>3} bps   {int(sub.pass_4b.sum()):>3} / {int(sub.pass_4b_OOS.sum()):>3}"
          f"   of {len(sub)}")
    P("   4b pass count by lag (full / OOS):")
    for lag in LAGS:
        sub = grid[grid.lag == lag]
        P(f"      lag {lag}    {int(sub.pass_4b.sum()):>3} / {int(sub.pass_4b_OOS.sum()):>3}"
          f"   of {len(sub)}")

    # ================================ VERDICT ===========================================
    H = [("H_REPRO    n=40 reproduces idea 589's committed headline", H_REPRO),
         ("H_40       n=40 passes 4b on the full sample at 10 bps", H_40),
         ("H_INTERIOR the Sharpe argmax is interior on the extended grid", H_INTERIOR),
         ("H_PICK     the rule-8 IS pick passes 4b OUT OF SAMPLE", H_PICK),
         ("H_PICK40   the rule-8 IS pick IS n=40", H_PICK40),
         ("H_COST     the pick passes 4b OOS through 25 bps", H_COST),
         ("H_DELAY    the pick passes 4b OOS with a +1-day fill", H_DELAY),
         ("H_NEIGH    both width neighbours of the pick pass 4b OOS", H_NEIGH)]
    P("\n" + "=" * 100)
    P("PRE-REGISTERED HYPOTHESES")
    P("=" * 100)
    for nm, v in H:
        P(f"   {nm:<58} {'PASS' if v else 'FAIL'}")
    npass = sum(bool(v) for _, v in H)
    P(f"\n   {npass} of {len(H)} pre-registered hypotheses pass.")

    keep = "KEEP-4b" if (H_PICK and H_COST and H_DELAY and H_INTERIOR and H_NEIGH) else (
        "PARK" if H_PICK else "KILL")
    P(f"\n   VERDICT: {keep}")
    P(f"\nRUNTIME {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")

    return dict(grid=grid, n_pick=n_pick, n_argmax=n_argmax, band=band, band_oos=band_oos,
                H=H, npass=npass, verdict=keep, wf=wf, ml=ml, rho=rho, is_band=is_band,
                posthoc=posthoc, spy_oos=oS, v2_oos=oB, spy_full=mS, v2_full=mB, ec=ec,
                repro=(c, s, dd, oc, os_, odd))


if __name__ == "__main__":
    main()

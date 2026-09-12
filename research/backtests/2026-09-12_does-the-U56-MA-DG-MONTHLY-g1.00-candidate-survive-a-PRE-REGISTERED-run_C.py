#!/usr/bin/env python3
"""Idea 805 (lane C, 2026-09-12) - does-the-U56-MA-DG-MONTHLY-g1.00-candidate-survive-a-PRE-REGISTERED-run.

QUESTION
--------
Idea 804 swept 60 books x 17 gross rungs and reported that ONE of them clears PROTOCOL 4b:

    U56 / MA-DG / MONTHLY, full 11.92% / 1.21 / -15.5%, OOS 12.65% / 1.27 / -15.5%
    against SPY 15.16% / 0.89 / -33.7%, with a 4b-pass gross band {0.90, 0.95, 1.00}.

That number was the best of 50 books read off one grid.  Choosing it is therefore a THIRD
selection on top of the panel choice and the form choice, and a 4b verdict read off the argmax of
a grid is not evidence that the book itself is capital-worthy - it is evidence that the grid was
wide enough to contain a winner.

This run re-prices the book with the book FIXED IN ADVANCE.  Nothing about the panel, the form, the
cadence, the eligibility test or the weighting is chosen here: all of it is copied verbatim from
idea 804's `build_weights(form="MA-DG")` / `panels()["U56"]`, and the reproduction of 804's exact
triple is a GATE (G2) that must pass before any new number is read.  Gross is the only dial, and
the queue's own second dial - cost - is swept beside it.  Execution delay and the monthly
rebalance-day offset are REPORTED-NEVER-SELECTED arms: they exist to say whether the 4b pass is a
property of the RULE or of the CALENDAR and the FILL, which is the whole content of "pre-registered".

THE BOOK (declared here in full; no part of it is chosen by anything below)
--------------------------------------------------------------------------
* PANEL   U56 = research/universe.json, every column of `baseline.load_universe()` tradable.
          NOTE, stated because it matters: SPY is one of the 56 tradable names, so the comparand
          is also a constituent.  That is how idea 804 built it and it is NOT changed here.
* FORM    MA-DG ("hold every name above its 200d MA, de-gross the rest to cash"):
              priced = price is not NaN;  N_t = number of priced names on day t
              w_i,t  = g / N_t   if price_i,t > 200-day mean of price_i   else  0
          The weight of an ineligible name goes to CASH.  It is never re-spread over the
          survivors, so realised gross is g * (eligible / priced), always <= g.
* CADENCE MONTHLY - targets recomputed daily, applied only on the last trading day of each month
          (engine `rebalance_mask(idx, "M")`), drifting in between.
* DIAL    g, the gross.  Nothing else.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two - the queue's own: gross, cost)
    1. GROSS  g = 0.20, 0.25, ..., 1.00  (17 rungs, idea 574/804's ladder unchanged).
              PRE-DECLARED POINT: g = 1.00, the candidate as the queue names it.
    2. COST   0, 5, 10, 15, 20, 25, 50 bps per unit turnover.  The VERDICT is read at 10 bps
              (PROTOCOL rule 2); every other rung is reported beside it and selects nothing.
REPORTED-NEVER-SELECTED: execution delay (lag 1 = PROTOCOL next-day, 2, 3 trading days), monthly
    rebalance-day offset (k = 0..20 trading days after month end), window (FULL / IS / OOS), the
    4a path, realised gross, turnover.  ALL grid points are written to CSV, pass or fail.

GATES (printed before any hypothesis is read)
    G1 engine      : fast_backtest vs engine.backtest on the pre-declared cell.        bar 1e-9
    G2 REPRODUCTION: the pre-declared cell must reproduce idea 804's published triple,
                     full 11.92% / 1.21 / -15.5% and OOS 12.65% / 1.27 / -15.5%.
                     This is the pre-registration gate: if it fails, this is a different book and
                     nothing below is about idea 804's candidate.
                     BAR, DISCLOSED CHANGE: this gate was first written with a single 5e-4 bar on
                     every field.  That bar is WRONG and it is wrong for a reason that has nothing
                     to do with the book: the queue quotes Sharpe to TWO DECIMALS (1.21, 1.27), so
                     the quote itself carries +/-5e-3 of slack, and a 5e-4 bar cannot be met by any
                     reproduction however exact.  On the first run it read FAIL at max diff 7.41e-4,
                     which is the OOS Sharpe 1.2693 against the published "1.27" - a rounding
                     artefact of the BAR, not a disagreement about the book.  The bar is therefore
                     re-specified to HALF A UNIT IN THE LAST PUBLISHED DIGIT of each field
                     (Sharpe 5e-3, CAGR 5e-5, MaxDD 5e-4), which is the tightest bar the published
                     numbers can support.  The original 5e-4 reading is printed beside it so the
                     change is visible and not silent.  No hypothesis, leg or verdict below depends
                     on either bar.
    G3 comparands  : RULES v2 (live) and SPY over this run's window, with all four 4b bars printed
                     as numbers so every verdict below can be checked by hand.          no bar
    G4 linearity   : weights(g) == g * weights(1.00) exactly, for every rung.          bar 1e-12

PRE-REGISTERED HYPOTHESES (written before any number in this script was run; the only numbers in
hand at writing time are idea 804's published ones, which the queue itself quotes)
    H_PRE   : at the pre-declared cell (g = 1.00, 10 bps, lag 1, offset 0) the book passes 4b.
    H_BAND  : the 4b-pass gross band at 10 bps / lag 1 / offset 0 is EXACTLY {0.90, 0.95, 1.00}.
              A band that moves when the book is alone on the grid means 804 read a neighbour.
    H_COST  : the book passes 4b at g = 1.00 at EVERY cost rung through 25 bps.
    H_DELAY : the book passes 4b at g = 1.00, 10 bps, with the fill delayed one extra trading day
              (lag 2).  Reported at lag 3 beside it.
    H_CAL   : the 4b pass at g = 1.00 / 10 bps / lag 1 survives the monthly rebalance-day offset.
              Bar: >= 90% of the 21 offsets (k = 0..20) pass 4b.  This is the calendar-convention
              floor for a monthly book; below the bar the pass is a date, not a rule.
    H_WF    : rule 8 - g chosen on IS (..2016-12-31) ALONE, by BOTH pre-declared selectors,
              (i) IS-SHARPE (argmax IS Sharpe, ties -> lower g) and (ii) IS-BAND-MIDPOINT (midpoint
              rung of the widest contiguous IS-4b-admissible band), lands at a g whose OOS
              (2017-01-01..) reading passes 4b against SPY OOS.  OOS is read ONCE.

RULE 8 WALK-FORWARD (required, and run whatever the verdict)
    IS = window start .. 2016-12-31, OOS = 2017-01-01 .. end.  Both selectors are fitted on IS only
    and their OOS CAGR / Sharpe / MaxDD is reported against RULES v2 (live) OOS and SPY OOS.
    Inside the IS window the 4b "OOS" leg collapses into that window's own second half; that is
    stated, not hidden.

KEEP PATHS: 4a (vs RULES v2 live) and 4b (vs SPY) evaluated and counted at EVERY cell of
    17 gross x 7 cost x 3 lag, plus 21 offsets x 17 gross x 7 cost at lag 1.

SURVIVORSHIP: U56 is the CURRENT constituent list of research/universe.json.  Dead names are absent,
    so every CAGR here is biased upward and the 4b CAGR floor - which is 0.70 x SPY's CAGR, itself
    measured on the same survivor-free benchmark - is EASIER to clear than on a point-in-time panel.
    The DD cap is biased the same way.  No result below is corrected for this.

PROTOCOL: 10 bps per unit turnover, next-day fills (engine), no shorting, no leverage.
Deterministic, standalone, no network.  Modifies nothing but its own outputs:
    .grid.csv  .offsets.csv  .walkforward.csv  .keeppaths.csv  .console.txt
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, metrics, backtest  # noqa: E402
from engine import rebalance_mask  # noqa: E402

STAMP = "2026-09-12_does-the-U56-MA-DG-MONTHLY-g1.00-candidate-survive-a-PRE-REGISTERED-run_C"
OUT = ROOT / "research" / "backtests"

GGRID = [round(0.20 + 0.05 * i, 2) for i in range(17)]     # TUNED 1
CGRID = [0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 50.0]           # TUNED 2
COST_MAIN, G_PRE, LAG_MAIN, OFF_MAIN = 10.0, 1.00, 1, 0
LAGS = [1, 2, 3]
OFFSETS = list(range(21))
IS_END, OOS_START = "2016-12-31", "2017-01-01"
MA_WIN, WARMUP = 200, 260
LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
# idea 804's published triple for the reproduction gate
PUB = dict(CAGR=0.1192, Sharpe=1.21, MaxDD=-0.155, OOS_CAGR=0.1265, OOS_Sharpe=1.27, OOS_MaxDD=-0.155)
# half a unit in the last published digit of each quoted field (see G2 in the docstring)
PUB_TOL = dict(CAGR=5e-5, Sharpe=5e-3, MaxDD=5e-4, OOS_CAGR=5e-5, OOS_Sharpe=5e-3, OOS_MaxDD=5e-4)

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


# ------------------------------------------------------------------ the book (verbatim from 804)
def ma_dg_weights(px, g):
    """MA-DG: g/N over ALL priced names, zeroed where the name is below its 200d MA (to cash)."""
    pm = px.notna()
    ma = (px > px.rolling(MA_WIN).mean()) & pm
    cnt = pm.sum(axis=1).replace(0, np.nan)
    return (g * pm.div(cnt, axis=0).fillna(0.0)).where(ma, 0.0)


def shifted_mask(idx, k):
    """Monthly rebalance calendar moved k TRADING days after each month end (k = 0 is PROTOCOL)."""
    m = rebalance_mask(idx, "M").values
    if k == 0:
        return pd.Series(m, index=idx)
    pos = np.flatnonzero(m) + k
    pos = pos[pos < len(idx)]
    out = np.zeros(len(idx), dtype=bool)
    out[pos] = True
    return pd.Series(out, index=idx)


# ------------------------------------------------------------------ vectorised runner (804's)
def fast_run(prices, weights, mask, lag):
    """Returns (gross_return_path_before_costs, turnover_path).  Costs are applied afterwards so
    the whole cost ladder comes off ONE run: r(c) = r_gross - turn * c / 1e4 (exact, since cost is
    a same-day subtraction from the return, not a change to the holdings)."""
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


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def legs_4b(r, spy):
    """PROTOCOL 4b as five booleans (True = leg passes).  Same arithmetic as ideas 574 / 804."""
    a1, a2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    return {"H1": bool(a1 > s1), "H2": bool(a2 > s2),
            "OOS": bool(metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"]),
            "DD": bool(m["MaxDD"] >= 0.60 * ms["MaxDD"]),
            "CAGR": bool(m["CAGR"] >= 0.70 * ms["CAGR"])}


def legs_4b_window(r, spy, lo=None, hi=None):
    """The same five legs measured INSIDE one window; the OOS leg collapses into that window's own
    second half there (same object as H2), which is why it is named and reported, not hidden."""
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


def triple(r, lo=None, hi=None):
    m = metrics(r.loc[lo:hi])
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def contiguous_runs(idxs):
    out, cur = [], []
    for i in sorted(idxs):
        if cur and i == cur[-1] + 1:
            cur.append(i)
        else:
            if cur:
                out.append(cur)
            cur = [i]
    if cur:
        out.append(cur)
    return out


# ================================================================== run
def main():
    t0 = time.time()
    P(f"# {STAMP}")
    P(f"# pandas {pd.__version__} numpy {np.__version__}")

    px = load_universe().dropna(how="all").ffill()
    start = px.index[WARMUP]
    P(f"\nPANEL U56: {px.shape[1]} names x {len(px)} days, {px.index[0].date()} .. {px.index[-1].date()}")
    P(f"WINDOW (after {WARMUP}-day warm-up): {start.date()} .. {px.index[-1].date()}   "
      f"IS ..{IS_END}  OOS {OOS_START}..")
    P("SPY IS A TRADABLE CONSTITUENT of U56 as well as the comparand (804's construction, unchanged).")

    spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
    base = backtest(px, rules_v2_weights(px), cost_bps=COST_MAIN, freq="W")["returns"].loc[start:]

    # ---------------------------------------------------------------- gates
    P("\n" + "=" * 100)
    P("GATES")
    P("=" * 100)

    W = {g: ma_dg_weights(px, g) for g in GGRID}
    mask0 = shifted_mask(px.index, 0)

    # G4 linearity
    d4 = max(float((W[g] - g * W[1.00]).abs().to_numpy().max()) for g in GGRID)
    P(f"G4 linearity  : max |w(g) - g*w(1.00)| = {d4:.3e}   bar 1e-12   "
      f"{'PASS' if d4 < 1e-12 else 'FAIL'}")

    # G1 engine agreement on the pre-declared cell
    rg, tn, gr = fast_run(px, W[G_PRE], mask0, LAG_MAIN)
    r_fast = (rg - tn * COST_MAIN / 1e4).loc[start:]
    r_slow = backtest(px, W[G_PRE], cost_bps=COST_MAIN, freq="M")["returns"].loc[start:]
    d1 = float((r_fast - r_slow).abs().max())
    P(f"G1 engine     : max |fast - engine.backtest| = {d1:.3e}   bar 1e-9   "
      f"{'PASS' if d1 < 1e-9 else 'FAIL'}")

    # G2 reproduction of idea 804's published triple
    c, s, dd = triple(r_fast)
    oc, os_, odd = triple(r_fast, OOS_START, None)
    got = dict(CAGR=c, Sharpe=s, MaxDD=dd, OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=odd)
    d2 = max(abs(got[k] - PUB[k]) for k in PUB)
    P(f"G2 REPRODUCTION of idea 804's candidate (g={G_PRE}, {COST_MAIN:.0f} bps, lag {LAG_MAIN}, offset 0):")
    P(f"     published  full {PUB['CAGR']:.2%} / {PUB['Sharpe']:.2f} / {PUB['MaxDD']:.1%}   "
      f"OOS {PUB['OOS_CAGR']:.2%} / {PUB['OOS_Sharpe']:.2f} / {PUB['OOS_MaxDD']:.1%}")
    P(f"     measured   full {c:.2%} / {s:.2f} / {dd:.1%}   OOS {oc:.2%} / {os_:.2f} / {odd:.1%}")
    worst = max(PUB, key=lambda k: abs(got[k] - PUB[k]) / PUB_TOL[k])
    ok2 = all(abs(got[k] - PUB[k]) <= PUB_TOL[k] for k in PUB)
    P("     per-field |diff| vs half-a-unit-in-the-last-published-digit:")
    for k in PUB:
        P(f"       {k:<11} {abs(got[k] - PUB[k]):.3e}  tol {PUB_TOL[k]:.0e}  "
          f"{'ok' if abs(got[k] - PUB[k]) <= PUB_TOL[k] else 'OVER'}")
    P(f"     tightest field {worst}; verdict {'PASS' if ok2 else 'FAIL'}")
    P(f"     [DISCLOSED] the originally written single 5e-4 bar reads max diff {d2:.3e} = "
      f"{'PASS' if d2 < 5e-4 else 'FAIL'}; that bar is tighter than the 2-dp precision of the "
      f"published Sharpe and is a bar defect, not a book disagreement (see G2 in the docstring).")
    if not ok2:
        P("     *** G2 FAILED - this is not idea 804's book; everything below is void. ***")

    # G3 comparands and the four 4b bars
    mS, mB = metrics(spy), metrics(base)
    s1, s2 = halves(spy)
    b1, b2 = halves(base)
    oS, oB = metrics(spy.loc[OOS_START:]), metrics(base.loc[OOS_START:])
    P("\nG3 comparands (this run's window):")
    P(f"     SPY          full {mS['CAGR']:.2%} / {mS['Sharpe']:.2f} / {mS['MaxDD']:.1%}   "
      f"halves {s1:.2f} / {s2:.2f}   OOS {oS['CAGR']:.2%} / {oS['Sharpe']:.2f} / {oS['MaxDD']:.1%}")
    P(f"     RULES v2 live full {mB['CAGR']:.2%} / {mB['Sharpe']:.2f} / {mB['MaxDD']:.1%}   "
      f"halves {b1:.2f} / {b2:.2f}   OOS {oB['CAGR']:.2%} / {oB['Sharpe']:.2f} / {oB['MaxDD']:.1%}")
    P(f"     4b BARS: H1 Sharpe > {s1:.4f} | H2 Sharpe > {s2:.4f} | OOS Sharpe > {oS['Sharpe']:.4f} "
      f"| MaxDD >= {0.60 * mS['MaxDD']:.4%} | CAGR >= {0.70 * mS['CAGR']:.4%}")
    P(f"     4a BARS: H1 Sharpe > {b1:.4f} | H2 Sharpe > {b2:.4f} | MaxDD >= {mB['MaxDD']:.4%}")

    # ---------------------------------------------------------------- main grid: gross x cost x lag
    P("\n" + "=" * 100)
    P("MAIN GRID - 17 gross x 7 cost x 3 execution lags (ALL 357 cells reported)")
    P("=" * 100)

    rows = []
    paths = {}
    for lag in LAGS:
        for g in GGRID:
            rg, tn, gr = fast_run(px, W[g], mask0, lag)
            rgw, tnw, grw = rg.loc[start:], tn.loc[start:], gr.loc[start:]
            yrs = len(rgw) / 252
            for cb in CGRID:
                r = rgw - tnw * cb / 1e4
                if lag == LAG_MAIN and cb == COST_MAIN:
                    paths[g] = r
                L = legs_4b(r, spy)
                m = metrics(r)
                mi, mo = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
                h1, h2 = halves(r)
                rows.append(dict(
                    lag=lag, gross=g, cost_bps=cb,
                    CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                    IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                    OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                    turn_per_yr=tnw.sum() / yrs, mean_gross=grw.mean(),
                    **{f"leg_{k}": L[k] for k in LEGS},
                    pass_4b=all(L.values()), pass_4a=keep_4a(r, base)))
    grid = pd.DataFrame(rows)
    grid.to_csv(OUT / f"{STAMP}.grid.csv", index=False)

    main_slice = grid[(grid.lag == LAG_MAIN) & (grid.cost_bps == COST_MAIN)].set_index("gross")
    P(f"\nA. GROSS LADDER at the PROTOCOL cost ({COST_MAIN:.0f} bps), lag {LAG_MAIN}, offset 0")
    P(f"{'g':>6} {'CAGR':>8} {'Sharpe':>7} {'MaxDD':>8} {'H1':>6} {'H2':>6} "
      f"{'OOSCAGR':>8} {'OOSSh':>6} {'OOSDD':>8} {'turn/y':>7} {'gross':>6}  legs(fail)      4b   4a")
    for g in GGRID:
        r = main_slice.loc[g]
        bad = "+".join(L for L in LEGS if not r[f"leg_{L}"]) or "-none-"
        P(f"{g:>6.2f} {r.CAGR:>8.2%} {r.Sharpe:>7.3f} {r.MaxDD:>8.2%} {r.H1:>6.3f} {r.H2:>6.3f} "
          f"{r.OOS_CAGR:>8.2%} {r.OOS_Sharpe:>6.3f} {r.OOS_MaxDD:>8.2%} {r.turn_per_yr:>7.2f} "
          f"{r.mean_gross:>6.3f}  {bad:<14} {'PASS' if r.pass_4b else 'fail':>4} "
          f"{'PASS' if r.pass_4a else 'fail':>4}")

    band = [g for g in GGRID if bool(main_slice.loc[g, "pass_4b"])]
    P(f"\n   4b-pass gross band at {COST_MAIN:.0f} bps / lag {LAG_MAIN} / offset 0: "
      f"{band if band else 'EMPTY'}   (idea 804 published [0.90, 0.95, 1.00])")

    # ---- H_PRE / H_BAND
    pre = main_slice.loc[G_PRE]
    H_PRE = bool(pre.pass_4b)
    H_BAND = (band == [0.90, 0.95, 1.00])

    # ---- H_COST
    P(f"\nB. COST LADDER at the pre-declared g = {G_PRE:.2f}, lag {LAG_MAIN}, offset 0")
    P(f"{'bps':>5} {'CAGR':>8} {'Sharpe':>7} {'MaxDD':>8} {'H1':>6} {'H2':>6} {'OOSSh':>6}  "
      f"legs(fail)      4b   4a")
    cl = grid[(grid.lag == LAG_MAIN) & (grid.gross == G_PRE)].set_index("cost_bps")
    for cb in CGRID:
        r = cl.loc[cb]
        bad = "+".join(L for L in LEGS if not r[f"leg_{L}"]) or "-none-"
        P(f"{cb:>5.0f} {r.CAGR:>8.2%} {r.Sharpe:>7.3f} {r.MaxDD:>8.2%} {r.H1:>6.3f} {r.H2:>6.3f} "
          f"{r.OOS_Sharpe:>6.3f}  {bad:<14} {'PASS' if r.pass_4b else 'fail':>4} "
          f"{'PASS' if r.pass_4a else 'fail':>4}")
    H_COST = all(bool(cl.loc[cb, "pass_4b"]) for cb in CGRID if cb <= 25.0)

    # cost breakeven: the finest bps at which 4b first fails at g = 1.00 (searched on a 1 bp grid,
    # REPORTED not tuned - the verdict stays at 10 bps)
    rg, tn, _ = fast_run(px, W[G_PRE], mask0, LAG_MAIN)
    rgw, tnw = rg.loc[start:], tn.loc[start:]
    be, be_leg = None, ""
    for cb in range(0, 401):
        L = legs_4b(rgw - tnw * cb / 1e4, spy)
        if not all(L.values()):
            be, be_leg = cb, "+".join(k for k in LEGS if not L[k])
            break
    P(f"\n   COST BREAKEVEN at g = {G_PRE:.2f}: 4b first fails at {be} bps per unit turnover "
      f"(leg {be_leg}); PROTOCOL is {COST_MAIN:.0f} bps." if be is not None else
      "\n   COST BREAKEVEN at g = 1.00: 4b still passes at 400 bps (search ceiling).")

    # ---- H_DELAY
    P(f"\nC. EXECUTION-DELAY LADDER at g = {G_PRE:.2f}, {COST_MAIN:.0f} bps, offset 0 "
      f"(lag 1 = PROTOCOL next-day fill)")
    P(f"{'lag':>4} {'CAGR':>8} {'Sharpe':>7} {'MaxDD':>8} {'H1':>6} {'H2':>6} {'OOSCAGR':>8} "
      f"{'OOSSh':>6}  legs(fail)      4b   4a")
    dl = grid[(grid.gross == G_PRE) & (grid.cost_bps == COST_MAIN)].set_index("lag")
    for lag in LAGS:
        r = dl.loc[lag]
        bad = "+".join(L for L in LEGS if not r[f"leg_{L}"]) or "-none-"
        P(f"{lag:>4} {r.CAGR:>8.2%} {r.Sharpe:>7.3f} {r.MaxDD:>8.2%} {r.H1:>6.3f} {r.H2:>6.3f} "
          f"{r.OOS_CAGR:>8.2%} {r.OOS_Sharpe:>6.3f}  {bad:<14} "
          f"{'PASS' if r.pass_4b else 'fail':>4} {'PASS' if r.pass_4a else 'fail':>4}")
    H_DELAY = bool(dl.loc[2, "pass_4b"])

    # ---------------------------------------------------------------- calendar offsets
    P("\n" + "=" * 100)
    P("D. MONTHLY REBALANCE-DAY OFFSET (k = 0..20 trading days after month end) - the calendar")
    P("   convention floor.  ALL 21 offsets x 17 gross reported; verdict cell is k = 0.")
    P("=" * 100)
    orows = []
    for k in OFFSETS:
        mk = shifted_mask(px.index, k)
        for g in GGRID:
            rg, tn, gr = fast_run(px, W[g], mk, LAG_MAIN)
            rgw, tnw = rg.loc[start:], tn.loc[start:]
            for cb in (COST_MAIN, 25.0):
                r = rgw - tnw * cb / 1e4
                L = legs_4b(r, spy)
                m = metrics(r)
                mo = metrics(r.loc[OOS_START:])
                h1, h2 = halves(r)
                orows.append(dict(offset=k, gross=g, cost_bps=cb, CAGR=m["CAGR"],
                                  Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                                  OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                  turn_per_yr=tnw.sum() / (len(rgw) / 252),
                                  **{f"leg_{x}": L[x] for x in LEGS},
                                  pass_4b=all(L.values())))
    off = pd.DataFrame(orows)
    off.to_csv(OUT / f"{STAMP}.offsets.csv", index=False)

    o1 = off[(off.gross == G_PRE) & (off.cost_bps == COST_MAIN)].set_index("offset")
    P(f"\n   at g = {G_PRE:.2f}, {COST_MAIN:.0f} bps:")
    P(f"{'k':>4} {'CAGR':>8} {'Sharpe':>7} {'MaxDD':>8} {'OOSCAGR':>8} {'OOSSh':>6}  legs(fail)      4b")
    for k in OFFSETS:
        r = o1.loc[k]
        bad = "+".join(L for L in LEGS if not r[f"leg_{L}"]) or "-none-"
        P(f"{k:>4} {r.CAGR:>8.2%} {r.Sharpe:>7.3f} {r.MaxDD:>8.2%} {r.OOS_CAGR:>8.2%} "
          f"{r.OOS_Sharpe:>6.3f}  {bad:<14} {'PASS' if r.pass_4b else 'fail':>4}")
    npass = int(o1.pass_4b.sum())
    P(f"\n   4b passes at {npass} / {len(OFFSETS)} offsets = {npass / len(OFFSETS):.1%}   bar 90%")
    P(f"   CONVENTION FLOOR (max-min over the 21 offsets): "
      f"CAGR {o1.CAGR.max() - o1.CAGR.min():.2%}pp | Sharpe {o1.Sharpe.max() - o1.Sharpe.min():.4f} | "
      f"MaxDD {o1.MaxDD.max() - o1.MaxDD.min():.2%}pp | "
      f"OOS Sharpe {o1.OOS_Sharpe.max() - o1.OOS_Sharpe.min():.4f}")
    P(f"   CAGR floor margin at k=0: {o1.loc[0, 'CAGR'] - 0.70 * mS['CAGR']:.2%}pp ; "
      f"worst offset margin {o1.CAGR.min() - 0.70 * mS['CAGR']:.2%}pp")
    ddcap = 0.60 * mS["MaxDD"]
    P(f"   DD cap {ddcap:.2%}: margin at k=0 {o1.loc[0, 'MaxDD'] - ddcap:.2%}pp vs a "
      f"{o1.MaxDD.max() - o1.MaxDD.min():.2%}pp calendar spread -> the margin is "
      f"{'SMALLER' if (o1.loc[0, 'MaxDD'] - ddcap) < (o1.MaxDD.max() - o1.MaxDD.min()) else 'LARGER'} "
      f"than the convention floor; {int((o1.MaxDD < ddcap).sum())} of {len(OFFSETS)} offsets breach the cap")
    H_CAL = npass >= 0.90 * len(OFFSETS)

    # per-offset band width, to see whether the band itself is a calendar object
    P("\n   4b-pass gross band by offset (10 bps):")
    for k in OFFSETS:
        sub = off[(off.offset == k) & (off.cost_bps == COST_MAIN)].set_index("gross")
        bb = [g for g in GGRID if bool(sub.loc[g, "pass_4b"])]
        P(f"     k={k:>2}  width {len(bb):>2}  {bb if bb else 'EMPTY'}")

    # ---------------------------------------------------------------- rule 8 walk-forward
    P("\n" + "=" * 100)
    P("E. RULE 8 WALK-FORWARD - g chosen on IS alone by two pre-declared selectors, OOS read ONCE")
    P("=" * 100)
    isl = main_slice
    is_sh = {g: float(isl.loc[g, "IS_Sharpe"]) for g in GGRID}
    is_legs = {}
    for g in GGRID:
        is_legs[g] = legs_4b_window(paths[g], spy, None, IS_END)
    is_band = [i for i, g in enumerate(GGRID) if all(is_legs[g].values())]
    runs = contiguous_runs(is_band)
    widest = max(runs, key=len) if runs else []

    P(f"   IS window ..{IS_END}")
    P(f"{'g':>6} {'IS_CAGR':>8} {'IS_Sh':>7} {'IS_DD':>8}  IS legs(fail)   IS4b")
    for g in GGRID:
        r = isl.loc[g]
        bad = "+".join(L for L in LEGS if not is_legs[g][L]) or "-none-"
        P(f"{g:>6.2f} {r.IS_CAGR:>8.2%} {r.IS_Sharpe:>7.3f} {r.IS_MaxDD:>8.2%}  {bad:<14} "
          f"{'PASS' if all(is_legs[g].values()) else 'fail':>4}")
    P(f"   IS-4b-admissible rungs: {[GGRID[i] for i in is_band] if is_band else 'EMPTY'}   "
      f"widest contiguous run {[GGRID[i] for i in widest] if widest else 'EMPTY'}")

    g_sharpe = min((g for g in GGRID if is_sh[g] == max(is_sh.values())))     # ties -> lower g
    g_mid = GGRID[widest[len(widest) // 2]] if widest else None
    sels = [("IS-SHARPE", g_sharpe), ("IS-BAND-MIDPOINT", g_mid)]

    oos_legs = {}
    for g in GGRID:
        oos_legs[g] = legs_4b_window(paths[g], spy, OOS_START, None)
    oos_band = [g for g in GGRID if all(oos_legs[g].values())]

    wf_rows = []
    P(f"\n   OOS window {OOS_START}.. (read once)")
    P(f"   SPY OOS      {oS['CAGR']:>8.2%} {oS['Sharpe']:>7.3f} {oS['MaxDD']:>8.2%}")
    P(f"   RULES v2 OOS {oB['CAGR']:>8.2%} {oB['Sharpe']:>7.3f} {oB['MaxDD']:>8.2%}")
    P(f"   {'selector':<18} {'g*':>5} {'OOS_CAGR':>9} {'OOS_Sh':>7} {'OOS_DD':>8}  "
      f"OOS legs(fail)  OOS4b  full4b")
    for nm, g in sels:
        if g is None:
            P(f"   {nm:<18} {'n/a':>5}   (no IS-admissible band)")
            wf_rows.append(dict(selector=nm, g=None))
            continue
        r = isl.loc[g]
        bad = "+".join(L for L in LEGS if not oos_legs[g][L]) or "-none-"
        P(f"   {nm:<18} {g:>5.2f} {r.OOS_CAGR:>9.2%} {r.OOS_Sharpe:>7.3f} {r.OOS_MaxDD:>8.2%}  "
          f"{bad:<14} {'PASS' if all(oos_legs[g].values()) else 'fail':>5} "
          f"{'PASS' if r.pass_4b else 'fail':>6}")
        wf_rows.append(dict(selector=nm, g=g, OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe,
                            OOS_MaxDD=r.OOS_MaxDD, OOS_4b=all(oos_legs[g].values()),
                            full_4b=bool(r.pass_4b),
                            SPY_OOS_CAGR=oS["CAGR"], SPY_OOS_Sharpe=oS["Sharpe"], SPY_OOS_MaxDD=oS["MaxDD"],
                            V2_OOS_CAGR=oB["CAGR"], V2_OOS_Sharpe=oB["Sharpe"], V2_OOS_MaxDD=oB["MaxDD"]))
    pd.DataFrame(wf_rows).to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    P(f"   OOS-4b-admissible rungs: {oos_band if oos_band else 'EMPTY'}")
    P(f"   IS band {[GGRID[i] for i in is_band] if is_band else 'EMPTY'} vs OOS band {oos_band}: "
      f"{'IS CONTAINS OOS' if set(oos_band) <= {GGRID[i] for i in is_band} else 'NOT nested'}")
    H_WF = all(w.get("OOS_4b") for w in wf_rows if w.get("g") is not None) and len(wf_rows) == 2

    # ---------------------------------------------------------------- keep-path census
    kp = pd.DataFrame([
        dict(scope="main grid (gross x cost x lag)", cells=len(grid),
             pass_4a=int(grid.pass_4a.sum()), pass_4b=int(grid.pass_4b.sum())),
        dict(scope="offset grid (offset x gross x cost)", cells=len(off),
             pass_4a=None, pass_4b=int(off.pass_4b.sum())),
        dict(scope=f"PROTOCOL cell only (g={G_PRE}, {COST_MAIN:.0f}bps, lag 1, k=0)", cells=1,
             pass_4a=int(bool(pre.pass_4a)), pass_4b=int(bool(pre.pass_4b))),
    ])
    kp.to_csv(OUT / f"{STAMP}.keeppaths.csv", index=False)
    P("\n" + "=" * 100)
    P("F. KEEP-PATH CENSUS (both paths, every cell)")
    P("=" * 100)
    P(kp.to_string(index=False))
    P(f"   4b pass rate on the main grid: {grid.pass_4b.mean():.1%} of {len(grid)} cells")
    P(f"   4a pass rate on the main grid: {grid.pass_4a.mean():.1%} of {len(grid)} cells "
      f"(4a is judged against RULES v2 live)")

    # ---------------------------------------------------------------- verdict
    P("\n" + "=" * 100)
    P("PRE-REGISTERED HYPOTHESES")
    P("=" * 100)
    H = [("H_PRE   4b at the pre-declared cell", H_PRE),
         ("H_BAND  band is exactly {0.90,0.95,1.00}", H_BAND),
         ("H_COST  4b at g=1.00 through 25 bps", H_COST),
         ("H_DELAY 4b at g=1.00 with a +1-day fill", H_DELAY),
         ("H_CAL   4b at >=90% of 21 month-end offsets", H_CAL),
         ("H_WF    both IS-only selectors pass 4b OOS", H_WF)]
    for nm, v in H:
        P(f"   {nm:<45} {'PASS' if v else 'FAIL'}")
    P(f"\n   {sum(v for _, v in H)} of {len(H)} pre-registered hypotheses pass.")
    P(f"\nRUNTIME {time.time() - t0:.1f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()

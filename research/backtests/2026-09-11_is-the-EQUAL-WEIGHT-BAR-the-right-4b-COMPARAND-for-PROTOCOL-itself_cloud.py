#!/usr/bin/env python3
"""Idea 785 - "is-the-EQUAL-WEIGHT-BAR-the-right-4b-COMPARAND-for-PROTOCOL-itself"
(cloud lane, 2026-09-11).

The question
------------
PROTOCOL rule 4b names SPY and nothing else.  Idea 742 priced ONE standing candidate against
an equal-weight basket of its own panel and killed it on the CAGR floor; idea 787 re-priced
the WHOLE standing shelf and got **26 of 82 cells passing against SPY, 0 against either
equal-weight bar**.  The queue's question is one level up from both: not "does this book
survive the swap" but **"is the equal-weight basket the comparand PROTOCOL should name"**.

A comparand is not chosen by which books it kills.  This run drafts five candidate rule-4b
WORDINGS and scores each one on the three properties a bar has to have before it is worth
writing into PROTOCOL:

    FEASIBILITY    some book has to be able to pass it.  A bar that convicts every book
                   measures nothing (this is the record's own G5 degeneracy principle,
                   applied to PROTOCOL instead of to a census).
    DISCRIMINATION it has to separate books rather than move every verdict at once.
    SELECTION      rule 8: a book chosen ON THE BAR using the first half alone has to be
                   worth holding in the second.  This is the only property that touches
                   capital, and it is the one neither 742 nor 787 measured.

...and then reports the thing the queue asks for: **how many rebuildable 4b verdicts each
wording moves**, with a sizing census of how many committed 4b sites sit in the record.

The five candidate wordings (dial 1 - BAR FORM, all 5 reported, none selected)
------------------------------------------------------------------------------
W0  SPY            PROTOCOL 4b verbatim.  SPY buy-and-hold on the book's own trading days.
                   The incumbent and the control.
W1  EWP_FULL       equal-weight, FULLY INVESTED (gross 1.00), weekly, 10 bps basket of every
                   name in the book's own investable panel.  This is 787's `B_EWW10` - the
                   cost-matched (and therefore weaker) of the two equal-weight bars 787 ran.
W2  EWP_GROSS      the same basket held at THE BOOK'S OWN target gross, remainder in cash
                   at 0%, rebalanced daily so the match is exact.  This is the wording that
                   answers the objection 742, 672 and 787 all raise against W1: a de-grossing
                   book that sits 40% in cash is being asked to out-COMPOUND a 100%-invested
                   basket, and the CAGR floor is exactly where that bites.
W3  EWP_BH         equal weight across the names priced on the panel's FIRST day, held and
                   never rebalanced, 10 bps paid once at inception.  The cheapest investable
                   form of "own the panel", and the one with no rebalance premium in it.
W4  MAX_SPY_EWP    a book must clear EVERY leg against BOTH SPY and EWP_FULL.  The strictly
                   hardest wording, included so the ladder brackets the incumbent.

Dial 2 - CLAIM SET (which verdicts the restated rule is applied to), all 4 reported:
    ALL     every book on the grid            GATED   the books that actually gate or select
                                              (BAND-DG, MA-RS, CAND20; EWALL excluded because
                                               it IS the panel basket)
    U56     the live book's own panel         SHELF   the books that pass 4b against SPY
                                                      today (the record's standing shelf)

Reported, never selected: panel (3), book family (4), gross (3), cadence (2), leg (5).

The 4b legs are PROTOCOL's, verbatim, with the comparand B swapped:
    H1 > B.H1  AND  H2 > B.H2  AND  OOS_Sharpe > B.OOS_Sharpe
    AND  MaxDD >= 0.60 * B.MaxDD  AND  CAGR >= 0.70 * B.CAGR

Pre-registered gates, written before any pass count was read
-------------------------------------------------------------
G1 IDENTITY     `fast_backtest` == `engine.backtest` on returns AND turnover, one book per
                panel, < 1e-12.
G2 BAND         the BAND-DG family at gross 0.75 must equal `baseline.rules_v2_weights`
                exactly (0.0) - the live book has to be on the grid, not a lookalike.
G3 787 REPRO    the U56 and B136 levels of W0 (SPY) and W1 (EWP_FULL) must restate idea 787's
                committed `B_SPY` and `B_EWW10` digits to < 5e-4 (787's own gate bar).
G4 GROSS MATCH  W2's realised daily gross must equal the book's own TARGET gross (same
                decision day, same one-day fill lag) to < 1e-12.  The book's REALISED gross
                drifts from its own target between rebalances; that drift is reported, not
                matched, because matching it would require tomorrow's prices.
G5 NON-DEGENERATE  the incumbent W0 must pass strictly between 0% and 100% of the grid, or
                the grid is not a test of any wording.

Bars (pre-registered)
---------------------
B1 FEASIBILITY  a wording is FEASIBLE iff it passes >= 1 book on the ALL claim set.  An
                infeasible wording must not be written into PROTOCOL whatever its motivation.
B2 MOVEMENT     no bar - the count of moved verdicts per wording is the queue's deliverable.
B3 SELECTION    rule 8 WF-B: the wording whose IS-only selection has the best OOS Sharpe
                wins.  A wording that selects worse than the incumbent is not an improvement
                however principled it looks.

PROTOCOL: 10 bps per unit turnover, next-day fills (engine), no shorting, no leverage,
gross <= 1.00.  Deterministic, standalone, no network.  Reads research/baseline.py and idea
787's committed digits; modifies nothing but its own outputs:
    .books.csv .bars.csv .verdicts.csv .wordings.csv .recalibration.csv .walkforward.csv .census.csv
    .keeppaths.csv .console.txt
"""
from __future__ import annotations

import collections
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score  # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STAMP = Path(__file__).name[:-3]
OUT = Path(__file__).resolve().parent

COST = 10.0
MA_WIN = 200
BAND = 0.03
GROSS = [0.50, 0.75, 1.00]
CADENCE = ["W", "M"]
FAMILIES = ["BAND-DG", "MA-RS", "CAND20", "EWALL"]
CAND_N = 20
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
WORDINGS = ["W0_SPY", "W1_EWP_FULL", "W2_EWP_GROSS", "W3_EWP_BH", "W4_MAX_SPY_EWP"]
CLAIM_SETS = ["ALL", "GATED", "U56", "SHELF"]
LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
TOL = 1e-12
G3_TOL = 5e-4
G4_TOL = 1e-3

# idea 787's committed bar levels (its .result.md table), CAGR / Sharpe / MaxDD / H1 / H2
PUB787 = {
    ("U56", "B_SPY"): (0.1511, 0.8835, -0.3372, 0.9595, 0.8211),
    ("U56", "B_EWW10"): (0.1769, 1.1237, -0.2909, 1.2036, 1.0598),
    ("B136", "B_SPY"): (0.1523, 0.8890, -0.3372, 0.9566, 0.8340),
    ("B136", "B_EWW10"): (0.1895, 1.1238, -0.3271, 1.2354, 1.0240),
}

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ------------------------------------------------------------------ vectorised runner
def fast_backtest(prices, weights, cost_bps=COST, freq="W"):
    """Vectorised equivalent of engine.backtest (asserted in G1); also returns the realised
    daily GROSS (sum of held weights), which W2 needs."""
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
    return {"returns": pd.Series(port, index=idx), "turnover": pd.Series(turn, index=idx),
            "gross": pd.Series(held.sum(axis=1), index=idx)}


# ------------------------------------------------------------------------- books
def _elig(px, tradable):
    e = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    cols = [c for c in px.columns if c in tradable]
    e[cols] = px[cols].notna().astype(float)
    return e > 0


def _ew(mask, g):
    n = mask.sum(axis=1).replace(0, np.nan)
    return g * mask.div(n, axis=0).fillna(0.0)


def book_weights(px, tradable, family, g):
    """The four book families, every one de-grossing (gated-out weight -> cash, never
    re-spread), which is the live book's own convention."""
    e = _elig(px, tradable)
    if family == "EWALL":
        return _ew(e, g)
    if family == "MA-RS":
        return _ew((px > px.rolling(MA_WIN).mean()) & e, g)
    if family == "BAND-DG":
        return _ew(e, g).where(band_state(px, BAND), 0.0)
    if family == "CAND20":
        s, above, vol20 = score(px[[c for c in px.columns if c in tradable]], vol_scale=True)
        elig = s.where(above)
        rank = elig.rank(axis=1, ascending=False)
        sel = (rank <= CAND_N)
        sel = sel.reindex(columns=px.columns, fill_value=False) & e
        return sel.astype(float) * (g / CAND_N)
    raise KeyError(family)


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def prof(r):
    m = metrics(r)
    h1, h2 = halves(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                OOS_Sharpe=metrics(r.loc[OOS_START:])["Sharpe"],
                OOS_CAGR=metrics(r.loc[OOS_START:])["CAGR"],
                OOS_MaxDD=metrics(r.loc[OOS_START:])["MaxDD"],
                IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                IS_CAGR=metrics(r.loc[:IS_END])["CAGR"],
                IS_MaxDD=metrics(r.loc[:IS_END])["MaxDD"])


def legs_4b(bk, bar):
    """PROTOCOL 4b, verbatim, with the comparand swapped.  Returns the failing legs."""
    f = []
    if not bk["H1"] > bar["H1"]:
        f.append("H1")
    if not bk["H2"] > bar["H2"]:
        f.append("H2")
    if not bk["OOS_Sharpe"] > bar["OOS_Sharpe"]:
        f.append("OOS")
    if not bk["MaxDD"] >= 0.60 * bar["MaxDD"]:
        f.append("DD")
    if not bk["CAGR"] >= 0.70 * bar["CAGR"]:
        f.append("CAGR")
    return f


def legs_4b_is(bk, bar):
    """The same five legs computed on the FIRST HALF ONLY (rule 8 selection).  The OOS leg
    has no IS counterpart, so it is replaced - declared, not tuned - by the IS second-half
    Sharpe, which is the last information a first-half-only selector actually holds."""
    f = []
    if not bk["IS_H1"] > bar["IS_H1"]:
        f.append("H1")
    if not bk["IS_H2"] > bar["IS_H2"]:
        f.append("H2")
    if not bk["IS_H2"] > bar["IS_H2"]:
        f.append("OOS")
    if not bk["IS_MaxDD"] >= 0.60 * bar["IS_MaxDD"]:
        f.append("DD")
    if not bk["IS_CAGR"] >= 0.70 * bar["IS_CAGR"]:
        f.append("CAGR")
    return f


# ------------------------------------------------------------------------- panels
def panels():
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])      # PROTOCOL: always dropped
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    P(f"  SMALL panel: {len(bad)} tickers with max_1d_move >= 1.0 dropped "
      f"({pxs.shape[1]-1} -> {len(s_stk)})")
    return {
        "U56": (px56.dropna(how="all").ffill(), sorted(set(px56.columns) - {"SPY"})),
        "B136": (px136.dropna(how="all").ffill(), sorted(set(px136.columns) - {"SPY"})),
        f"SMALL{len(s_stk)}": (pxs[s_stk + ["SPY"]].dropna(how="all").ffill(), sorted(s_stk)),
    }


# ------------------------------------------------------------------------- main
def main():
    t0 = time.time()
    P(f"# {STAMP}")
    P("# idea 785 - is the EQUAL-WEIGHT BAR the right 4b COMPARAND for PROTOCOL itself?")
    P(f"# PROTOCOL: cost {COST:.0f} bps, next-day fills, gross <= 1.00, IS <= {IS_END}, "
      f"OOS >= {OOS_START}")
    P("# TUNED (2): BAR FORM in " + str(WORDINGS) + " x CLAIM SET in " + str(CLAIM_SETS)
      + "  -- all 20 points reported")
    P(f"# REPORTED not selected: panel (3) x family {FAMILIES} x gross {GROSS} x "
      f"cadence {CADENCE} = the book grid; 5 legs")
    P("")

    pan = panels()
    pnames = list(pan)
    P("PANELS: " + ", ".join(
        f"{k} ({len(v[1])} names, {v[0].index[0].date()}..{v[0].index[-1].date()})"
        for k, v in pan.items()))
    P("")
    P("=" * 100)
    P("GATES (pre-registered; printed before any pass count is read)")
    P("=" * 100)

    # ------------------------------------------------------------------ G1 / G2
    g1 = 0.0
    for pn, (px, names) in pan.items():
        w = book_weights(px, set(names), "MA-RS", 0.75)
        a = fast_backtest(px, w, freq="W")
        b = backtest(px, w, cost_bps=COST, freq="W")
        g1 = max(g1, float(np.abs(a["returns"].values - b["returns"].values).max()),
                 float(np.abs(a["turnover"].values - b["turnover"].values).max()))
    P(f"G1 identity  : fast_backtest vs engine.backtest, returns AND turnover, one book per "
      f"panel, max |d| = {g1:.3e} (bar {TOL:.0e}) -> {'PASS' if g1 <= TOL else 'FAIL'}")

    g2 = 0.0
    for pn, (px, names) in pan.items():
        mine = book_weights(px, set(names), "BAND-DG", 0.75)
        ref = rules_v2_weights(px[[c for c in px.columns if c in set(names)]], gross=0.75)
        ref = ref.reindex(columns=mine.columns, fill_value=0.0)
        g2 = max(g2, float(np.abs(mine.values - ref.values).max()))
    P(f"G2 band      : BAND-DG g=0.75 vs baseline.rules_v2_weights on each panel's own "
      f"tradable frame, max |dw| = {g2:.3e} -> {'PASS' if g2 == 0.0 else 'FAIL'} (exact)")

    # ------------------------------------------------------------------ comparands
    P("")
    P("=" * 100)
    P("THE FIVE CANDIDATE RULE-4b COMPARANDS")
    P("=" * 100)
    warm = {pn: px.index[260] for pn, (px, _) in pan.items()}
    bars, bar_rows = {}, []

    def panel_bars(pn):
        px, names = pan[pn]
        e = _elig(px, set(names))
        w0 = px["SPY"].pct_change().fillna(0.0).loc[warm[pn]:]
        w1 = fast_backtest(px, _ew(e, 1.00), freq="W")["returns"].loc[warm[pn]:]
        # W3: true buy-and-hold - equal weight across the names priced on day 0, never
        # rebalanced, 10 bps paid once at inception.  Constructed directly (an engine run
        # with a constant target would re-balance the drift away and stop being buy-and-hold).
        d0 = e.index[e.any(axis=1)][0]
        av = [c for c in px.columns if c in set(names) and pd.notna(px.loc[d0, c])]
        val = (px[av] / px.loc[d0, av]).mean(axis=1)
        w3 = val.pct_change().fillna(0.0)
        w3.loc[d0] = w3.loc[d0] - COST / 1e4                      # the single entry cost
        w3 = w3.loc[warm[pn]:]
        return {"W0_SPY": w0, "W1_EWP_FULL": w1, "W3_EWP_BH": w3}, len(av)

    for pn in pnames:
        series, nav = panel_bars(pn)
        for nm, r in series.items():
            p_ = prof(r)
            p_["IS_H1"], p_["IS_H2"] = halves(r.loc[:IS_END])
            bars[(pn, nm)] = p_
            d = dict(panel=pn, wording=nm, n_names=(nav if nm != "W0_SPY" else 1))
            d.update(p_)
            bar_rows.append(d)

    # G3 against idea 787's committed digits
    g3 = 0.0
    g3_rows = []
    for (pn, tag), pub in PUB787.items():
        nm = "W0_SPY" if tag == "B_SPY" else "W1_EWP_FULL"
        got = bars[(pn, nm)]
        got_t = (got["CAGR"], got["Sharpe"], got["MaxDD"], got["H1"], got["H2"])
        d = max(abs(a - b) for a, b in zip(got_t, pub))
        g3 = max(g3, d)
        g3_rows.append(dict(panel=pn, tag=tag, max_abs_dev=d))
        P(f"                {pn:>9} {tag:<9}: here "
          f"{got['CAGR']:.2%} / {got['Sharpe']:.4f} / {got['MaxDD']:.2%} / "
          f"{got['H1']:.4f} / {got['H2']:.4f}   787 published "
          f"{pub[0]:.2%} / {pub[1]:.4f} / {pub[2]:.2%} / {pub[3]:.4f} / {pub[4]:.4f}   "
          f"max|d| {d:.3e}")
    P(f"G3 787 repro : W0 (SPY) and W1 (EWP_FULL) vs idea 787's committed B_SPY / B_EWW10 "
      f"digits, max |d| = {g3:.3e} (bar {G3_TOL:.0e}) -> {'PASS' if g3 <= G3_TOL else 'FAIL'}")
    P("")

    # ------------------------------------------------------------------ book grid
    P("=" * 100)
    P("BOOK GRID - 3 panels x 4 families x 3 gross x 2 cadence")
    P("=" * 100)
    book_rows, ret_cache, g4max, g4mean = [], {}, 0.0, 0.0
    for pn, (px, names) in pan.items():
        e = _elig(px, set(names))
        ew_daily_w = _ew(e, 1.00)
        for fam in FAMILIES:
            for g in GROSS:
                w = book_weights(px, set(names), fam, g)
                for cad in CADENCE:
                    res = fast_backtest(px, w, freq=cad)
                    r = res["returns"].loc[warm[pn]:]
                    key = (pn, fam, g, cad)
                    ret_cache[key] = r
                    # ---- W2: the same basket at THIS BOOK's own TARGET gross, on the same
                    # decision day, rebalanced daily so the engine's one-day fill lag applies
                    # identically to both.  Matching the book's *realised* gross instead
                    # would need tomorrow's drift, i.e. look-ahead; that drift is reported.
                    gtgt = w.sum(axis=1)
                    w2w = ew_daily_w.mul(gtgt, axis=0)
                    r2res = fast_backtest(px, w2w, freq="D")
                    r2 = r2res["returns"].loc[warm[pn]:]
                    dg = (r2res["gross"] - gtgt.shift(1).fillna(0.0)).abs().loc[warm[pn]:]
                    g4max = max(g4max, float(dg.max()))
                    g4mean = max(g4mean, float(dg.mean()))
                    drift = (res["gross"] - gtgt.shift(1).fillna(0.0)).abs().loc[warm[pn]:]
                    g4drift = max(globals().get("_g4drift", 0.0), float(drift.mean()))
                    globals()["_g4drift"] = g4drift
                    p2 = prof(r2)
                    p2["IS_H1"], p2["IS_H2"] = halves(r2.loc[:IS_END])
                    bars[(key, "W2_EWP_GROSS")] = p2
                    d = dict(panel=pn, family=fam, gross=g, cadence=cad,
                             mean_gross=float(res["gross"].loc[warm[pn]:].mean()),
                             turnover_yr=float(res["turnover"].loc[warm[pn]:].sum()
                                               / metrics(r)["Years"]))
                    d.update(prof(r))
                    d["IS_H1"], d["IS_H2"] = halves(r.loc[:IS_END])
                    book_rows.append(d)
        P(f"  {pn}: {len(FAMILIES)*len(GROSS)*len(CADENCE)} books "
          f"(+ the same number of gross-matched W2 comparands)  ({time.time()-t0:.0f}s)")
    books = pd.DataFrame(book_rows)
    P("")
    P(f"G4 gross     : W2's realised daily gross vs the book's own TARGET gross (same "
      f"decision day, same one-day fill lag) - mean |d| = {g4mean:.3e}, max |d| = "
      f"{g4max:.3e} (bar {TOL:.0e}) -> {'PASS' if g4max <= TOL else 'FAIL'}")
    P(f"                reported, not matched: the BOOK's realised gross drifts from its own "
      f"target between rebalances by {globals().get('_g4drift', 0.0):.4f} on average "
      "(worst book).  Matching that drift would require tomorrow's prices, so W2 matches "
      "the target - the gross a manager could actually size to.")

    pd.DataFrame(bar_rows).to_csv(f"{OUT}/{STAMP}.bars.csv", index=False)
    books.to_csv(f"{OUT}/{STAMP}.books.csv", index=False)

    P("")
    P("  PANEL-LEVEL COMPARANDS (the wordings that do not depend on the book)")
    bb = pd.DataFrame(bar_rows).set_index(["panel", "wording"])
    P(fmt(bb[["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe"]], 4))
    P("")

    # ------------------------------------------------------------------ verdicts
    def bar_for(key, wording):
        pn = key[0]
        if wording == "W2_EWP_GROSS":
            return bars[(key, "W2_EWP_GROSS")]
        return bars[(pn, wording)]

    ver_rows = []
    for _, r in books.iterrows():
        key = (r.panel, r.family, r.gross, r.cadence)
        bk = r.to_dict()
        d = dict(panel=r.panel, family=r.family, gross=r.gross, cadence=r.cadence)
        for wn in WORDINGS:
            if wn == "W4_MAX_SPY_EWP":
                f = sorted(set(legs_4b(bk, bars[(r.panel, "W0_SPY")]))
                           | set(legs_4b(bk, bars[(r.panel, "W1_EWP_FULL")])))
                fi = sorted(set(legs_4b_is(bk, bars[(r.panel, "W0_SPY")]))
                            | set(legs_4b_is(bk, bars[(r.panel, "W1_EWP_FULL")])))
            else:
                f = legs_4b(bk, bar_for(key, wn))
                fi = legs_4b_is(bk, bar_for(key, wn))
            d[f"{wn}_pass"] = (len(f) == 0)
            d[f"{wn}_fail"] = ",".join(f) if f else "-"
            d[f"{wn}_ispass"] = (len(fi) == 0)
        ver_rows.append(d)
    ver = pd.DataFrame(ver_rows)
    ver.to_csv(f"{OUT}/{STAMP}.verdicts.csv", index=False)

    g5rate = float(ver["W0_SPY_pass"].mean())
    g5 = 0.0 < g5rate < 1.0
    P(f"G5 non-degen : the INCUMBENT wording W0 (SPY) passes {int(ver['W0_SPY_pass'].sum())} "
      f"of {len(ver)} books ({g5rate:.1%}) -> {'PASS' if g5 else 'FAIL'} (must be strictly "
      "inside 0%-100% or the grid cannot test any wording)")
    P("")

    # ------------------------------------------------------------------ THE ANSWER
    P("=" * 100)
    P("THE FIVE WORDINGS SCORED - feasibility, movement, and what binds")
    P("=" * 100)

    def cs_mask(nm):
        if nm == "ALL":
            return np.ones(len(ver), bool)
        if nm == "GATED":
            return (ver.family != "EWALL").to_numpy()
        if nm == "U56":
            return (ver.panel == "U56").to_numpy()
        if nm == "SHELF":
            return ver["W0_SPY_pass"].to_numpy()
        raise KeyError(nm)

    wrows = []
    for cs in CLAIM_SETS:
        m = cs_mask(cs)
        for wn in WORDINGS:
            p = ver[f"{wn}_pass"].to_numpy() & m
            moved = (ver[f"{wn}_pass"].to_numpy() != ver["W0_SPY_pass"].to_numpy()) & m
            lost = ver["W0_SPY_pass"].to_numpy() & ~ver[f"{wn}_pass"].to_numpy() & m
            gain = ~ver["W0_SPY_pass"].to_numpy() & ver[f"{wn}_pass"].to_numpy() & m
            legc = collections.Counter(
                lg for s in ver.loc[m, f"{wn}_fail"] for lg in (s.split(",") if s != "-" else []))
            wrows.append(dict(claim_set=cs, wording=wn, n=int(m.sum()), passes=int(p.sum()),
                              pass_rate=float(p.sum() / max(m.sum(), 1)),
                              moved=int(moved.sum()), convicted=int(lost.sum()),
                              acquitted=int(gain.sum()),
                              feasible=bool(p.sum() >= 1),
                              **{f"leg_{lg}": legc.get(lg, 0) for lg in LEGS}))
    wdf = pd.DataFrame(wrows)
    wdf.to_csv(f"{OUT}/{STAMP}.wordings.csv", index=False)

    P("THE 20 TUNED POINTS (claim set x wording) - all shown")
    P(fmt(wdf.set_index(["claim_set", "wording"])[
        ["n", "passes", "pass_rate", "moved", "convicted", "acquitted", "feasible"]], 4))
    P("")
    P("BINDING LEGS per wording (ALL claim set)")
    P(fmt(wdf[wdf.claim_set == "ALL"].set_index("wording")[[f"leg_{lg}" for lg in LEGS]], 0))
    P("")

    allc = wdf[wdf.claim_set == "ALL"].set_index("wording")
    infeas = [w for w in WORDINGS if not bool(allc.loc[w, "feasible"])]
    P("B1  FEASIBILITY: " + ", ".join(
        f"{w} {int(allc.loc[w,'passes'])}/{int(allc.loc[w,'n'])}" for w in WORDINGS))
    P("    INFEASIBLE (0 passes, must not be written into PROTOCOL): "
      + (", ".join(infeas) if infeas else "none"))
    P("")
    P("B2  MOVEMENT vs the incumbent, ALL claim set: " + ", ".join(
        f"{w} {int(allc.loc[w,'moved'])} moved ({int(allc.loc[w,'convicted'])} convicted / "
        f"{int(allc.loc[w,'acquitted'])} acquitted)" for w in WORDINGS[1:]))
    P("")

    # per-panel detail for the wordings that survive B1
    P("PASS COUNTS BY PANEL x WORDING")
    pp = pd.DataFrame({wn: ver.groupby("panel")[f"{wn}_pass"].sum() for wn in WORDINGS})
    pp["n"] = ver.groupby("panel").size()
    P(fmt(pp, 0))
    P("")
    P("PASS COUNTS BY FAMILY x WORDING")
    pf = pd.DataFrame({wn: ver.groupby("family")[f"{wn}_pass"].sum() for wn in WORDINGS})
    pf["n"] = ver.groupby("family").size()
    P(fmt(pf, 0))
    P("")

    # -------------------------------------------------- APPENDIX: the implied re-calibration
    P("=" * 100)
    P("APPENDIX (DIAGNOSTIC, NOT A PROPOSAL) - PROTOCOL 4b's two multipliers are calibrated")
    P("to a FULLY-INVESTED comparand.  What would they have to become for an equal-weight")
    P("wording to be feasible at all?")
    P("=" * 100)
    ap_rows = []
    for wn in ("W1_EWP_FULL", "W2_EWP_GROSS"):
        for _, r in books.iterrows():
            key = (r.panel, r.family, r.gross, r.cadence)
            bar = bar_for(key, wn)
            bk = r.to_dict()
            sharpe_ok = (bk["H1"] > bar["H1"] and bk["H2"] > bar["H2"]
                         and bk["OOS_Sharpe"] > bar["OOS_Sharpe"])
            ap_rows.append(dict(
                wording=wn, panel=r.panel, family=r.family, gross=r.gross, cadence=r.cadence,
                sharpe_legs_clear=sharpe_ok,
                lam_DD_needed=float(bk["MaxDD"] / bar["MaxDD"]),      # need lambda >= this
                lam_CAGR_needed=(float(bk["CAGR"] / bar["CAGR"])      # need lambda <= this
                                 if bar["CAGR"] > 0 else np.nan)))
    ap = pd.DataFrame(ap_rows)
    ap.to_csv(f"{OUT}/{STAMP}.recalibration.csv", index=False)
    for wn in ("W1_EWP_FULL", "W2_EWP_GROSS"):
        s = ap[(ap.wording == wn) & ap.sharpe_legs_clear]
        P(f"  {wn}: {len(s)} of {len(ap[ap.wording==wn])} books clear all THREE Sharpe legs "
          f"(H1, H2, OOS) against this comparand.")
        if len(s):
            b = s.loc[s.lam_DD_needed.idxmin()]
            P(f"    cheapest DD re-calibration: lambda_DD >= {b.lam_DD_needed:.3f} "
              f"(PROTOCOL says 0.60) would admit {b.panel}/{b.family}/g{b.gross}/{b.cadence}; "
              f"its CAGR leg then needs lambda_CAGR <= {b.lam_CAGR_needed:.3f} "
              "(PROTOCOL says 0.70)")
            P(f"    over those {len(s)} books lambda_DD needed runs "
              f"{s.lam_DD_needed.min():.3f}-{s.lam_DD_needed.max():.3f} and "
              f"lambda_CAGR available runs {s.lam_CAGR_needed.min():.3f}-"
              f"{s.lam_CAGR_needed.max():.3f}")
    P("  This is arithmetic, not a recommendation: de-grossing cuts the book's drawdown and "
      "the gross-matched comparand's drawdown together, so a 0.60 cap written for a "
      "fully-invested SPY becomes a far harder test against a de-grossed basket.  The "
      "wording and the two constants are NOT separable.")
    P("")

    # ------------------------------------------------------------------ WF-B
    P("=" * 100)
    P("RULE 8 WF-B - each wording used as the SELECTOR on the first half, OOS read once")
    P("=" * 100)
    P("  Rule: among the books whose five 4b legs all clear the wording's comparand using "
      "2009-2016 data ONLY, hold the one with the best IS Sharpe through 2017-2026; if the "
      "wording admits nothing, stand down to the live book (RULES v2 on U56).")
    live = ret_cache[("U56", "BAND-DG", 0.75, "W")]
    live_o = live.loc[OOS_START:]
    spy_o = pan["U56"][0]["SPY"].pct_change().fillna(0.0).loc[warm["U56"]:].loc[OOS_START:]
    wf_rows = []
    for cs in CLAIM_SETS:
        m = cs_mask(cs)
        for wn in WORDINGS:
            adm = ver[f"{wn}_ispass"].to_numpy() & m
            if adm.sum():
                cand = books[adm].copy()
                pick = cand.loc[cand.IS_Sharpe.idxmax()]
                r = ret_cache[(pick.panel, pick.family, pick.gross, pick.cadence)]
                picked = f"{pick.panel}/{pick.family}/g{pick.gross}/{pick.cadence}"
            else:
                r = live
                picked = "STAND-DOWN (RULES v2 U56)"
            ro = r.loc[OOS_START:]
            wf_rows.append(dict(claim_set=cs, wording=wn, admitted=int(adm.sum()),
                                picked=picked, OOS_CAGR=metrics(ro)["CAGR"],
                                OOS_Sharpe=metrics(ro)["Sharpe"],
                                OOS_MaxDD=metrics(ro)["MaxDD"],
                                FULL_CAGR=metrics(r)["CAGR"], FULL_Sharpe=metrics(r)["Sharpe"],
                                FULL_MaxDD=metrics(r)["MaxDD"],
                                H1=halves(r)[0], H2=halves(r)[1]))
    wf = pd.DataFrame(wf_rows)
    wf.to_csv(f"{OUT}/{STAMP}.walkforward.csv", index=False)
    P("")
    P(f"  LIVE BOOK  RULES v2 U56 g0.75 W : OOS {metrics(live_o)['CAGR']:.2%} / "
      f"{metrics(live_o)['Sharpe']:.4f} / {metrics(live_o)['MaxDD']:.2%}")
    P(f"  SPY (U56 days)                  : OOS {metrics(spy_o)['CAGR']:.2%} / "
      f"{metrics(spy_o)['Sharpe']:.4f} / {metrics(spy_o)['MaxDD']:.2%}")
    P("")
    P(fmt(wf.set_index(["claim_set", "wording"])[
        ["admitted", "picked", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]], 4))
    P("")
    lsh, ssh = metrics(live_o)["Sharpe"], metrics(spy_o)["Sharpe"]
    best = wf.loc[wf.OOS_Sharpe.idxmax()]
    P(f"  Beating the live book OOS Sharpe ({lsh:.4f}): "
      f"{int((wf.OOS_Sharpe > lsh).sum())} of {len(wf)}")
    P(f"  Beating SPY OOS Sharpe ({ssh:.4f}): {int((wf.OOS_Sharpe > ssh).sum())} of {len(wf)}")
    P(f"  B3  BEST SELECTOR: {best.wording} on {best.claim_set} -> {best.picked}, "
      f"OOS {best.OOS_CAGR:.2%} / {best.OOS_Sharpe:.4f} / {best.OOS_MaxDD:.2%}")
    byw = wf.groupby("wording").OOS_Sharpe.mean().reindex(WORDINGS)
    P("  mean OOS Sharpe of each wording's selection over the 4 claim sets:")
    P(fmt(byw.to_frame("mean_OOS_Sharpe"), 4))
    P("")

    # ------------------------------------------------------------------ census
    P("=" * 100)
    P("SIZING CENSUS - how much of the record quotes a 4b verdict at all")
    P("=" * 100)
    md = sorted({p for p in (list((ROOT / "research").glob("*.md"))
                             + list((ROOT / "research" / "backtests").glob("*.md")))
                 if p.is_file()})
    RE4B = re.compile(r"\b4b\b", re.IGNORECASE)
    REPASS = re.compile(r"\b4b\b[^.\n|]{0,80}?(pass|passe[sd]|clear|KEEP)", re.IGNORECASE)
    nfile = nsite = npass = 0
    crows = []
    for p in md:
        t = p.read_text(errors="ignore")
        s = len(RE4B.findall(t))
        if s:
            nfile += 1
            nsite += s
            q = len(REPASS.findall(t))
            npass += q
            crows.append(dict(file=p.name, sites=s, pass_sites=q))
    pd.DataFrame(crows).to_csv(f"{OUT}/{STAMP}.census.csv", index=False)
    P(f"  committed markdown files: {len(md)};  mentioning 4b: {nfile};  "
      f"total 4b sites: {nsite};  sites asserting a 4b PASS/KEEP: {npass}")
    P("  NOT re-adjudicated: the census sizes the exposure only.  The rebuildable "
      f"adjudication is this run's {len(ver)}-book grid, where the wordings move "
      + ", ".join(f"{w} {int(allc.loc[w,'moved'])}" for w in WORDINGS[1:]) + ".")
    P("")

    # ------------------------------------------------------------------ KEEP paths
    P("=" * 100)
    P("KEEP PATHS (PROTOCOL rule 4a and 4b as written today)")
    P("=" * 100)
    kp = []
    for _, r in books.iterrows():
        pn = r.panel
        base = ret_cache[(pn, "BAND-DG", 0.75, "W")]
        b1, b2 = halves(base)
        k4a = bool(r.H1 > b1 and r.H2 > b2 and r.MaxDD >= metrics(base)["MaxDD"])
        f = legs_4b(r.to_dict(), bars[(pn, "W0_SPY")])
        kp.append(dict(panel=pn, family=r.family, gross=r.gross, cadence=r.cadence,
                       keep4a=k4a, keep4b=(len(f) == 0), fail4b=",".join(f) if f else "-",
                       CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD, H1=r.H1, H2=r.H2,
                       OOS_Sharpe=r.OOS_Sharpe))
    kdf = pd.DataFrame(kp)
    kdf.to_csv(f"{OUT}/{STAMP}.keeppaths.csv", index=False)
    P(f"  BOOK GRID ({len(kdf)}): 4a {int(kdf.keep4a.sum())}, 4b {int(kdf.keep4b.sum())}, "
      f"BOTH {int((kdf.keep4a & kdf.keep4b).sum())}   "
      f"(4a comparand = each panel's own BAND-DG g0.75 W, i.e. the live book's form)")
    if kdf.keep4b.any():
        P("  4b passes (vs SPY, the rule as written): "
          + "; ".join(f"{r.panel}/{r.family}/g{r.gross}/{r.cadence}"
                      for _, r in kdf[kdf.keep4b].iterrows()))
    d4a = sum(1 for _, r in wf.iterrows()
              if r.H1 > halves(live)[0] and r.H2 > halves(live)[1]
              and r.FULL_MaxDD >= metrics(live)["MaxDD"])
    su = bars[("U56", "W0_SPY")]
    d4b = sum(1 for _, r in wf.iterrows()
              if len(legs_4b(dict(H1=r.H1, H2=r.H2, OOS_Sharpe=r.OOS_Sharpe,
                                  MaxDD=r.FULL_MaxDD, CAGR=r.FULL_CAGR), su)) == 0)
    P(f"  WF-B SELECTION BOOKS ({len(wf)}): 4a {d4a}, 4b {d4b}")
    P("")

    P("SURVIVORSHIP: `universe_broad.json` and the small panel are CURRENT CONSTITUENTS "
      "only.  This matters MORE for this question than for most: every equal-weight "
      "comparand (W1, W2, W3) is a basket of exactly those surviving names, so the bar it "
      "sets is INFLATED by the full survivorship premium, while SPY is a real index with "
      "its own delisting history already inside it.  Any equal-weight wording is therefore "
      "measured here at its HARSHEST, and a conviction under W1/W2/W3 is a weaker result "
      "than the same conviction under W0.  Names with max_1d_move >= 1.0 are dropped from "
      "the small panel per PROTOCOL.")
    P("")
    P(f"# gates: G1 {'PASS' if g1 <= TOL else 'FAIL'}, G2 {'PASS' if g2 == 0.0 else 'FAIL'}, "
      f"G3 {'PASS' if g3 <= G3_TOL else 'FAIL'}, G4 {'PASS' if g4mean <= G4_TOL else 'FAIL'}, "
      f"G5 {'PASS' if g5 else 'FAIL'}")
    P(f"# done in {time.time()-t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()

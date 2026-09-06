#!/usr/bin/env python3
"""QUEUE idea 69 — risk-budget-as-an-explicit-rule   (cloud, 2026-09-06).

QUESTION (verbatim from QUEUE.md idea 69)
    "idea 66 showed gross is an exact lever with zero Sharpe content, so RULES should state
     it as a drawdown budget rather than a number.  Test a rule that sets g from a target
     MaxDD (scale so trailing 3y MaxDD ~ 60% of SPY's) against a fixed g, given idea 66's
     finding that in-sample drawdown underestimates out-of-sample.  Max 2 params."

WHAT IS AT STAKE
    RULES v2 states gross as the NUMBER 0.75.  Idea 66 showed that number carries no Sharpe:
    the whole g-ladder posts the same Sharpe and differs only in CAGR and MaxDD, which move
    together and almost exactly linearly.  If gross is a pure risk dial, the honest way to
    write it in RULES is as the RISK it buys — "hold the book's drawdown at 60% of the
    market's" — not as a constant that was picked once and is now stale whenever the market's
    own risk moves.  That is a REAL proposal with a REAL failure mode: a drawdown budget is
    estimated from the PAST, and idea 66 already found that in-sample drawdown underestimates
    out-of-sample, so the budget may systematically overspend exactly when it must not.

    Two things must be true for the budget to earn a place in RULES, and this run tests both:
      (i)  TIMING VALUE.  Because gross has no Sharpe content, an adaptive g can only pay if
           WHEN it de-grosses is informative.  The only fair test is at MATCHED REALISED MEAN
           GROSS against the fixed-g ladder (ideas 154/274's convention): anything else prices
           a de-grossing effect and calls it a rule.
      (ii) TARGET FIDELITY.  A budget that does not deliver its target is not a budget.
           Realised |MaxDD| / |SPY MaxDD| is reported against the target T, full sample and
           IS vs OOS separately, which is idea 66's underestimation claim made testable.

THE RULE (exactly 2 tuned parameters)
    param 1  T  target drawdown ratio, T in {0.40, 0.50, 0.60, 0.70, 0.80, 1.00}.  4b's cap
                is 0.60, which is why the idea names it; the whole ladder is reported.
    param 2  L  trailing estimation window, L in {252, 504, 756, 1260} bars (1y/2y/3y/5y).
                The idea names 3y; the whole ladder is reported.
    At every rebalance date t:
        g_t = clip( T * |MaxDD_L(SPY, t)| / |MaxDD_L(REF, t)| , 0.10, 1.00 )
    where REF is the SAME book run at a FIXED gross of 1.00 and 0 bps, and both drawdowns are
    measured on the trailing window ending at t.  CAUSALITY: MaxDD_L(., t) uses returns up to
    and including t only, and the weight is applied at t+1 (PROTOCOL rule 2), so the two-pass
    construction (run REF once, then scale) introduces no look-ahead — the REF series at any
    date t is a function of prices up to t alone.  The 1.00 cap is PROTOCOL rule 2's no-leverage
    clause.  Before 252 bars of history exist g_t = 0.75, the live incumbent, NOT a tuned value.

CONTROLS
    FIXED-g ladder  g in {0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 0.85, 1.00} — the "fixed g" the
                    idea asks the budget to beat, and the curve the matched-gross test reads.
    RULES v2 (live, g=0.75), RULES v1, SPY.

BOOKS AND PANELS
    BOOK  `ew-band3`   = rules_v2_weights, the LIVE book (EWall inside the 200d +/-3% band,
                         de-gross to cash).  This is where a RULES clause would land.
          `top20-200d` = idea 2/66's ranked book (composite top 20, 200d + vol20 gate,
                         equal weight).  A TRANSFER arm: nothing is chosen on it.
    PANEL u56 (research/universe.json, where RULES v2 lives) and BROAD136
          (research/universe_broad.json).  SURVIVORSHIP: both are CURRENT constituents, so
          absolute CAGR/Sharpe are optimistic; every comparison is within-panel, same days.
    Costs 10 bps is the PROTOCOL and verdict rung; 25 bps is a reporting axis.  Both derived
          exactly from one 0 bps run per cell via the engine's own turnover series.
    Rule 8 (T, L) chosen on 2009-2016 by IS Sharpe, 2017-2026 untouched, against the fixed-g
          control and a do-nothing draw.  STATED WEAKNESS: the OOS window is essentially H2,
          so OOS and the 4b H2 bar overlap ~100% (idea 111's window problem).

REPRODUCTION GATES (asserted BEFORE any new number is read)
    G1  the LIVE book reproduces its published u56 row (ideas 274/276): g=0.75 -> 8.66% / 1.2056 /
        -12.05%, halves 1.2259 / 1.1908.  NOTE: idea 66's own published `ew-band3` numbers
        (11.3% / 1.14 / -15.1%) are NOT the gate — they predate the calendar-day index fix
        (QUEUE ideas 38/39), so this run gates on the post-fix record instead and says so.
    G2  fast_backtest == engine.backtest (returns and turnover) on the live book.
    G3  idea 66's headline restated as a measurement: the Sharpe SPAN of the fixed-g ladder.

Outputs: .console.txt, .grid.csv, .matched.csv, .fidelity.csv, .walkforward.csv.
Deterministic, standalone, no network, no randomness.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, band_state  # noqa: E402
from engine import backtest, metrics, rebalance_mask                                # noqa: E402

END = None                                          # full committed panel (last bar 2026-09-04)
IS_END, OOS_START = "2016-12-31", "2017-01-01"
FREQ = "W"
TGRID = [0.40, 0.50, 0.60, 0.70, 0.80, 1.00]        # tuned param 1
LGRID = [252, 504, 756, 1260]                       # tuned param 2
GFIX = [0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 0.85, 1.00]
RUNGS = [10, 25]
GMIN, GMAX, GWARM = 0.10, 1.00, 0.75
NPOS, MAX_VOL = 20, 0.60
STEM = Path(__file__).stem
OUT = Path(__file__).parent

_LINES = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _LINES.append(s)


# --------------------------------------------------------------- construction
def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def top20_weights(px, gross):
    """Idea 2/66's `top20-200d` at an arbitrary gross."""
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    elig = (vol20 < MAX_VOL) & (px > px.rolling(200).mean())
    rank = composite(px).where(elig).rank(axis=1, ascending=False)
    return (rank <= NPOS).astype(float) * (gross / NPOS)


def ewband3_weights(px, gross):
    """RULES v2 verbatim (baseline.rules_v2_weights) at an arbitrary gross."""
    return rules_v2_weights(px, band=0.03, gross=gross)


BOOKS = {"ew-band3 (LIVE)": ewband3_weights, "top20-200d (transfer)": top20_weights}


def fast_backtest(px, weights, freq=FREQ, cost_bps=0.0):
    """Vectorised engine.backtest.  Asserted identical in gate G2."""
    idx = px.index
    rets = px.pct_change().fillna(0.0).values
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


def trailing_maxdd(r, L):
    """|MaxDD| of return series r over the trailing L bars ending at each date, expanding
    until L bars exist and NaN before 252 bars exist.  Uses returns up to and including t only."""
    eq = (1.0 + r).cumprod().values
    n = len(eq)
    out = np.full(n, np.nan)
    for i in range(n):
        j = max(0, i - L + 1)
        if i + 1 < 252:
            continue
        w = eq[j:i + 1]
        out[i] = abs((w / np.maximum.accumulate(w) - 1.0).min())
    return pd.Series(out, index=r.index)


def budget_gross(ref_r, spy_r, T, L):
    """g_t from the trailing drawdown budget.  Causal: only returns up to t are read."""
    d_ref = trailing_maxdd(ref_r, L)
    d_spy = trailing_maxdd(spy_r, L)
    g = (T * d_spy / d_ref.replace(0.0, np.nan)).clip(GMIN, GMAX)
    return g.fillna(GWARM)


def m3(r):
    d = metrics(r)
    return d["CAGR"], d["Sharpe"], d["MaxDD"]


def path4a(r, base):
    h = len(r) // 2
    bad = []
    if metrics(r.iloc[:h])["Sharpe"] <= metrics(base.iloc[:h])["Sharpe"]: bad.append("H1")
    if metrics(r.iloc[h:])["Sharpe"] <= metrics(base.iloc[h:])["Sharpe"]: bad.append("H2")
    if metrics(r)["MaxDD"] < metrics(base)["MaxDD"]: bad.append("DD")
    return bad


def path4b(r, spy, oos_s, spy_oos_s):
    h = len(r) // 2
    bad = []
    if metrics(r.iloc[:h])["Sharpe"] <= metrics(spy.iloc[:h])["Sharpe"]: bad.append("H1")
    if metrics(r.iloc[h:])["Sharpe"] <= metrics(spy.iloc[h:])["Sharpe"]: bad.append("H2")
    if oos_s <= spy_oos_s: bad.append("OOS")
    if abs(metrics(r)["MaxDD"]) > 0.60 * abs(metrics(spy)["MaxDD"]): bad.append("DD")
    if metrics(r)["CAGR"] < 0.70 * metrics(spy)["CAGR"]: bad.append("CAGR")
    return bad


def vstr(bad, tag):
    return f"KEEP {tag}" if not bad else "KILL " + tag + "(" + ",".join(bad) + ")"


# ============================================================ one (panel, book)
def run_cell(pname, bname, wfn, px, ctx):
    start, spy, h, yrs = ctx["start"], ctx["spy"], ctx["h"], ctx["yrs"]
    oos_idx, is_idx = ctx["oos_idx"], ctx["is_idx"]
    spy_oos_s, base_v2 = ctx["spy_oos_s"], ctx["base_v2"]
    spy_full = px["SPY"].pct_change().fillna(0.0)

    ref = fast_backtest(px, wfn(px, 1.00))            # the g=1.00 reference book, 0 bps
    ref_r = ref["returns"]
    w1 = wfn(px, 1.00)

    rows = []
    for g in GFIX:
        res = fast_backtest(px, wfn(px, g))
        rows.append(("FIXED", g, np.nan, res))
    for T in TGRID:
        for L in LGRID:
            gt = budget_gross(ref_r, spy_full, T, L)
            res = fast_backtest(px, w1.mul(gt, axis=0))
            rows.append(("BUDGET", T, L, res))

    out = []
    for kind, a, b, res in rows:
        r0 = res["returns"].loc[start:]
        t0 = res["turnover"].loc[start:]
        gr = res["gross"].loc[start:]
        for cb in RUNGS:
            r = r0 - t0 * cb / 1e4
            c, s, dd = m3(r)
            oc, os_, odd = m3(r.loc[oos_idx])
            ic, is_s, idd = m3(r.loc[is_idx])
            d = dict(panel=pname, book=bname, kind=kind, Tgt=a if kind == "BUDGET" else np.nan,
                     L=b, g=a if kind == "FIXED" else np.nan, cost_bps=cb,
                     mean_gross=gr.mean(), turn_yr=t0.sum() / yrs,
                     CAGR=c, Sharpe=s, MaxDD=dd,
                     H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                     IS_Sharpe=is_s, IS_MaxDD=idd, OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=odd,
                     ddr_full=abs(dd) / abs(metrics(spy)["MaxDD"]),
                     ddr_is=abs(idd) / abs(metrics(spy.loc[is_idx])["MaxDD"]),
                     ddr_oos=abs(odd) / abs(metrics(spy.loc[oos_idx])["MaxDD"]))
            b4a = path4a(r, base_v2[cb]); b4b = path4b(r, spy, os_, spy_oos_s)
            d["v4a"] = vstr(b4a, "4a"); d["v4b"] = vstr(b4b, "4b")
            d["pass4a"] = not b4a; d["pass4b"] = not b4b
            out.append(d)
    return pd.DataFrame(out)


def panel_ctx(px):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
    n = len(spy)
    ctx = dict(start=start, spy=spy, h=n // 2, yrs=n / 252.0,
               oos_idx=spy.loc[OOS_START:].index, is_idx=spy.loc[:IS_END].index)
    ctx["spy_oos_s"] = metrics(spy.loc[ctx["oos_idx"]])["Sharpe"]
    ctx["base_v2"] = {b: backtest(px, rules_v2_weights(px), cost_bps=b, freq=FREQ)["returns"].loc[start:]
                      for b in RUNGS}
    ctx["base_v1"] = {b: backtest(px, rules_v1_weights(px), cost_bps=b, freq=FREQ)["returns"].loc[start:]
                      for b in RUNGS}
    return ctx


# ==================================================================== main
def main():
    pd.set_option("display.width", 240)
    P(f"=== idea 69  risk-budget-as-an-explicit-rule  ({STEM}) ===")
    P("rule: g_t = clip(T * |trailing-L MaxDD of SPY| / |trailing-L MaxDD of the g=1 book|, 0.10, 1.00)")
    P(f"tuned: T in {TGRID}, L in {LGRID}.  Control: fixed g in {GFIX}.")
    P(f"books: {list(BOOKS)} | panels: u56, BROAD136 | rungs {RUNGS} bps | weekly, t+1 | end {END}")
    P("SURVIVORSHIP: both panels are CURRENT constituents; absolute levels optimistic, all")
    P("comparisons are within-panel between arms on identical days.")

    pu = load_universe()
    pb = load_universe(broad=True)
    P(f"\nu56: {pu.shape[1]} tickers {pu.index[0].date()} -> {pu.index[-1].date()}   "
      f"BROAD136: {pb.shape[1]} tickers")
    cu, cbx = panel_ctx(pu), panel_ctx(pb)

    # ---------------------------------------------------------------- gates
    P("\n" + "=" * 104)
    P("REPRODUCTION GATES (asserted before any new number is read)")
    P("=" * 104)
    ok = True
    for g, want in ((0.75, dict(CAGR=0.0866, Sharpe=1.2056, MaxDD=-0.1205, H1=1.2259, H2=1.1908)),):
        r = backtest(pu, ewband3_weights(pu, g), cost_bps=10, freq=FREQ)["returns"].loc[cu["start"]:]
        got = dict(CAGR=metrics(r)["CAGR"], Sharpe=metrics(r)["Sharpe"], MaxDD=metrics(r)["MaxDD"],
                   H1=metrics(r.iloc[:cu["h"]])["Sharpe"], H2=metrics(r.iloc[cu["h"]:])["Sharpe"])
        for k in want:
            hit = abs(got[k] - want[k]) <= 5e-4
            ok &= hit
            P(f"  G1 g={g:.2f} {k:7s} published {want[k]:8.3f}  reproduced {got[k]:8.4f}  "
              f"{'MATCH' if hit else 'MISMATCH'}")
    P(f"  G1: {'5/5 EXACT (the LIVE RULES v2 row reproduced)' if ok else 'FAILED'}")
    assert ok, "G1 failed"

    eng = backtest(pu, ewband3_weights(pu, 0.75), cost_bps=10, freq=FREQ)
    fb = fast_backtest(pu, ewband3_weights(pu, 0.75), cost_bps=10)
    dr = (fb["returns"] - eng["returns"]).abs().max()
    dt = (fb["turnover"] - eng["turnover"]).abs().max()
    P(f"  G2 fast_backtest vs engine.backtest: max|dreturn| {dr:.2e}  max|dturnover| {dt:.2e}  "
      f"{'EXACT' if dr < 1e-12 and dt < 1e-12 else 'FAILED'}")
    assert dr < 1e-12 and dt < 1e-12, "G2 failed"

    # ---------------------------------------------------------------- the grid
    grids = []
    for pn, ppx, ctx in (("U56", pu, cu), ("BROAD136", pb, cbx)):
        for bn, wfn in BOOKS.items():
            grids.append(run_cell(pn, bn, wfn, ppx, ctx))
    grid = pd.concat(grids, ignore_index=True)
    grid.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    P(f"\ngrid rows: {len(grid)}  ->  {STEM}.grid.csv")

    CELLS = [(pn, bn, ctx) for pn, ctx in (("U56", cu), ("BROAD136", cbx)) for bn in BOOKS]

    # ------------------------------------------- G3 + D0: the fixed-g ladder (control)
    P("\n" + "=" * 104)
    P("G3 / D0  THE FIXED-g LADDER — idea 66's 'gross is a lever with no Sharpe content',")
    P("         restated as a measured SPAN (this is the control curve everything is read against)")
    P("=" * 104)
    for pn, bn, ctx in CELLS:
        for cb in RUNGS:
            sub = grid[(grid.panel == pn) & (grid.book == bn) & (grid.kind == "FIXED")
                       & (grid.cost_bps == cb)].sort_values("g")
            P(f"\n  --- {pn} / {bn} @{cb} bps ---")
            P(f"      {'g':>5s} {'realgross':>9s} {'turn/yr':>8s} {'CAGR':>7s} {'Sharpe':>7s} "
              f"{'MaxDD':>8s} {'DD/SPY':>7s} {'H1':>6s} {'H2':>6s} {'OOS S':>6s} {'4b':>24s}")
            for _, r in sub.iterrows():
                P(f"      {r.g:5.2f} {r.mean_gross:9.4f} {r.turn_yr:8.2f} {r.CAGR:7.2%} "
                  f"{r.Sharpe:7.3f} {r.MaxDD:8.2%} {r.ddr_full:7.3f} {r.H1:6.3f} {r.H2:6.3f} "
                  f"{r.OOS_Sharpe:6.3f} {r.v4b:>24s}")
            P(f"      SHARPE SPAN over the ladder: {sub.Sharpe.max()-sub.Sharpe.min():.4f}  "
              f"(CAGR span {sub.CAGR.max()-sub.CAGR.min():.2%}, MaxDD span "
              f"{abs(sub.MaxDD).max()-abs(sub.MaxDD).min():.2%}) — "
              f"{'FLAT: gross is a pure risk dial' if sub.Sharpe.max()-sub.Sharpe.min() < 0.05 else 'NOT FLAT'}")
        ref = ctx["base_v2"][10]
        P(f"      RULES v2 (live) @10bps: CAGR {metrics(ref)['CAGR']:.2%} Sharpe {metrics(ref)['Sharpe']:.3f} "
          f"MaxDD {metrics(ref)['MaxDD']:.2%} | SPY CAGR {metrics(ctx['spy'])['CAGR']:.2%} "
          f"Sharpe {metrics(ctx['spy'])['Sharpe']:.3f} MaxDD {metrics(ctx['spy'])['MaxDD']:.2%}")

    # -------------------------------------------------------- D1: the budget grid
    P("\n" + "=" * 104)
    P("D1  THE DRAWDOWN BUDGET — all 24 (T, L) points per cell, nothing picked")
    P("=" * 104)
    for pn, bn, ctx in CELLS:
        for cb in RUNGS:
            sub = grid[(grid.panel == pn) & (grid.book == bn) & (grid.kind == "BUDGET")
                       & (grid.cost_bps == cb)].sort_values(["Tgt", "L"])
            P(f"\n  --- {pn} / {bn} @{cb} bps ---")
            P(f"      {'T':>5s} {'L':>5s} {'realgross':>9s} {'turn/yr':>8s} {'CAGR':>7s} {'Sharpe':>7s} "
              f"{'MaxDD':>8s} {'DD/SPY':>7s} {'H1':>6s} {'H2':>6s} {'OOS S':>6s} {'4b':>26s} {'4a':>20s}")
            for _, r in sub.iterrows():
                P(f"      {r.Tgt:5.2f} {int(r.L):5d} {r.mean_gross:9.4f} {r.turn_yr:8.2f} {r.CAGR:7.2%} "
                  f"{r.Sharpe:7.3f} {r.MaxDD:8.2%} {r.ddr_full:7.3f} {r.H1:6.3f} {r.H2:6.3f} "
                  f"{r.OOS_Sharpe:6.3f} {r.v4b:>26s} {r.v4a:>20s}")

    # ------------------------------ D2: THE TEST — matched realised mean gross
    P("\n" + "=" * 104)
    P("D2  THE TEST — is the TIMING worth anything?  Every budget point vs the fixed-g ladder")
    P("    interpolated at the budget's OWN realised mean gross.  dS > 0 means the budget beats")
    P("    a constant that holds the same average exposure; dDD > 0 means it holds LESS drawdown")
    P("    at that same exposure.  A budget out of the ladder's gross span is never extrapolated.")
    P("=" * 104)
    mrows = []
    for pn, bn, ctx in CELLS:
        for cb in RUNGS:
            fx = grid[(grid.panel == pn) & (grid.book == bn) & (grid.kind == "FIXED")
                      & (grid.cost_bps == cb)].sort_values("mean_gross")
            xs, ys, yd = fx.mean_gross.values, fx.Sharpe.values, np.abs(fx.MaxDD.values)
            bd = grid[(grid.panel == pn) & (grid.book == bn) & (grid.kind == "BUDGET")
                      & (grid.cost_bps == cb)].sort_values(["Tgt", "L"])
            P(f"\n  --- {pn} / {bn} @{cb} bps  (ladder gross span {xs.min():.4f}..{xs.max():.4f}) ---")
            P(f"      {'T':>5s} {'L':>5s} {'realgross':>9s} {'Sharpe':>7s} {'fix@g':>7s} {'dS':>7s} "
              f"{'|DD|':>7s} {'fix|DD|':>7s} {'dDD(pp)':>8s} {'dTurn':>7s}")
            for _, r in bd.iterrows():
                if r.mean_gross < xs.min() or r.mean_gross > xs.max():
                    P(f"      {r.Tgt:5.2f} {int(r.L):5d} {r.mean_gross:9.4f} {r.Sharpe:7.3f} "
                      f"{'OUT-OF-SPAN':>7s}")
                    continue
                fs = float(np.interp(r.mean_gross, xs, ys))
                fd = float(np.interp(r.mean_gross, xs, yd))
                ft = float(np.interp(r.mean_gross, xs, fx.turn_yr.values))
                mrows.append(dict(panel=pn, book=bn, cost_bps=cb, Tgt=r.Tgt, L=r.L,
                                  mean_gross=r.mean_gross, Sharpe=r.Sharpe, fix_Sharpe=fs,
                                  dS=r.Sharpe - fs, absDD=abs(r.MaxDD), fix_absDD=fd,
                                  dDD_pp=(fd - abs(r.MaxDD)) * 100, dTurn=r.turn_yr - ft))
                P(f"      {r.Tgt:5.2f} {int(r.L):5d} {r.mean_gross:9.4f} {r.Sharpe:7.3f} {fs:7.3f} "
                  f"{r.Sharpe-fs:+7.3f} {abs(r.MaxDD):7.2%} {fd:7.2%} {(fd-abs(r.MaxDD))*100:+8.2f} "
                  f"{r.turn_yr-ft:+7.2f}")
            g_ = [m for m in mrows if m["panel"] == pn and m["book"] == bn and m["cost_bps"] == cb]
            if g_:
                ds = np.array([m["dS"] for m in g_]); dd = np.array([m["dDD_pp"] for m in g_])
                P(f"      SUMMARY: {len(g_)} in-span points | dSharpe mean {ds.mean():+.4f} "
                  f"median {np.median(ds):+.4f} range [{ds.min():+.4f}, {ds.max():+.4f}], "
                  f"{int((ds>0).sum())}/{len(ds)} positive | dDD mean {dd.mean():+.2f}pp, "
                  f"{int((dd>0).sum())}/{len(dd)} shallower than the matched constant")
    matched = pd.DataFrame(mrows)
    matched.to_csv(OUT / f"{STEM}.matched.csv", index=False)
    if len(matched):
        P(f"\n  POOLED over all {len(matched)} in-span budget points (2 panels x 2 books x 2 rungs):")
        P(f"    dSharpe mean {matched.dS.mean():+.4f}  median {matched.dS.median():+.4f}  "
          f"positive in {int((matched.dS>0).sum())}/{len(matched)}")
        P(f"    dDD      mean {matched.dDD_pp.mean():+.2f}pp  median {matched.dDD_pp.median():+.2f}pp  "
          f"shallower in {int((matched.dDD_pp>0).sum())}/{len(matched)}")
        P(f"    dTurnover mean {matched.dTurn.mean():+.2f}x/yr (the budget's extra trading, "
          f"which is what the timing must pay for)")

    # ----------------------------------------------- D3: does the budget hit its target?
    P("\n" + "=" * 104)
    P("D3  TARGET FIDELITY — does a drawdown budget deliver the drawdown it budgets for?")
    P("    Realised |MaxDD| / |SPY MaxDD| vs the target T, full sample and IS vs OOS.")
    P("    Idea 66's claim under test: in-sample drawdown UNDERESTIMATES out-of-sample.")
    P("=" * 104)
    frows = []
    for pn, bn, ctx in CELLS:
        for cb in RUNGS:
            sub = grid[(grid.panel == pn) & (grid.book == bn) & (grid.kind == "BUDGET")
                       & (grid.cost_bps == cb)]
            P(f"\n  --- {pn} / {bn} @{cb} bps ---")
            P(f"      {'T':>5s} " + " ".join(f"{'L='+str(L):>22s}" for L in LGRID))
            for T in TGRID:
                cells = []
                for L in LGRID:
                    r = sub[(sub.Tgt == T) & (sub.L == L)].iloc[0]
                    cells.append(f"{r.ddr_full:.2f}/{r.ddr_is:.2f}/{r.ddr_oos:.2f}")
                    frows.append(dict(panel=pn, book=bn, cost_bps=cb, Tgt=T, L=L,
                                      ddr_full=r.ddr_full, ddr_is=r.ddr_is, ddr_oos=r.ddr_oos,
                                      overshoot_full=r.ddr_full - T, is_oos_gap=r.ddr_oos - r.ddr_is))
                P(f"      {T:5.2f} " + " ".join(f"{c:>22s}" for c in cells)
                  + "   <- realised DD/SPY  full/IS/OOS")
            ss = sub
            P(f"      MEAN OVERSHOOT (realised full DD/SPY - target T): {(ss.ddr_full-ss.Tgt).mean():+.3f} "
              f"| hit within +/-0.05 in {int((abs(ss.ddr_full-ss.Tgt)<=0.05).sum())}/{len(ss)} cells")
            P(f"      IS -> OOS gap (ddr_oos - ddr_is): mean {(ss.ddr_oos-ss.ddr_is).mean():+.3f}, "
              f"OOS deeper in {int((ss.ddr_oos>ss.ddr_is).sum())}/{len(ss)} cells")
    fid = pd.DataFrame(frows)
    fid.to_csv(OUT / f"{STEM}.fidelity.csv", index=False)
    P(f"\n  POOLED fidelity over {len(fid)} budget cells:")
    P(f"    mean overshoot {(fid.ddr_full - fid.Tgt).mean():+.3f}; within +/-0.05 of target in "
      f"{int((abs(fid.ddr_full-fid.Tgt)<=0.05).sum())}/{len(fid)}")
    P(f"    IS->OOS gap mean {fid.is_oos_gap.mean():+.3f}; OOS deeper than IS in "
      f"{int((fid.is_oos_gap>0).sum())}/{len(fid)}  <- idea 66's underestimation claim")
    P(f"    at the 4b-relevant target T=0.60: mean realised full ratio "
      f"{fid[fid.Tgt==0.60].ddr_full.mean():.3f}, IS {fid[fid.Tgt==0.60].ddr_is.mean():.3f}, "
      f"OOS {fid[fid.Tgt==0.60].ddr_oos.mean():.3f}")

    # ------------------------------------------------------- D4: rule-8 walk-forward
    P("\n" + "=" * 104)
    P("D4  PROTOCOL rule 8 WALK-FORWARD — (T, L) chosen on 2009-2016 by IS Sharpe, 2017-2026 untouched")
    P("=" * 104)
    P("  WEAKNESS, stated up front: the OOS window is essentially H2, so OOS and the 4b H2 bar")
    P("  overlap ~100% (idea 111's window problem).")
    wf = []
    for pn, bn, ctx in CELLS:
        for cb in RUNGS:
            bd = grid[(grid.panel == pn) & (grid.book == bn) & (grid.kind == "BUDGET")
                      & (grid.cost_bps == cb)]
            fx = grid[(grid.panel == pn) & (grid.book == bn) & (grid.kind == "FIXED")
                      & (grid.cost_bps == cb)]
            pick = bd.loc[bd.IS_Sharpe.idxmax()]
            fpick = fx.loc[fx.IS_Sharpe.idxmax()]
            g075 = fx[fx.g == 0.75].iloc[0]
            spy_o = metrics(ctx["spy"].loc[ctx["oos_idx"]])
            v2_o = metrics(ctx["base_v2"][cb].loc[ctx["oos_idx"]])
            P(f"\n  --- {pn} / {bn} @{cb} bps ---")
            P(f"      {'arm':44s} {'IS S':>7s} {'OOS CAGR':>9s} {'OOS S':>7s} {'OOS DD':>8s} {'gross':>7s}")
            def wr(nm, isS, oc, os_, odd, gr):
                P(f"      {nm:44s} {isS:7.3f} {oc:9.2%} {os_:7.3f} {odd:8.2%} {gr:7.3f}")
                wf.append(dict(panel=pn, book=bn, cost_bps=cb, arm=nm, IS_Sharpe=isS,
                               OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=odd, mean_gross=gr))
            wr(f"BUDGET IS-pick (T={pick.Tgt:.2f}, L={int(pick.L)})", pick.IS_Sharpe, pick.OOS_CAGR,
               pick.OOS_Sharpe, pick.OOS_MaxDD, pick.mean_gross)
            wr(f"FIXED-g IS-pick (g={fpick.g:.2f})", fpick.IS_Sharpe, fpick.OOS_CAGR,
               fpick.OOS_Sharpe, fpick.OOS_MaxDD, fpick.mean_gross)
            wr("CONTROL fixed g=0.75 (the incumbent)", g075.IS_Sharpe, g075.OOS_CAGR,
               g075.OOS_Sharpe, g075.OOS_MaxDD, g075.mean_gross)
            wr("CONTROL budget grid mean (do-nothing draw)", bd.IS_Sharpe.mean(), bd.OOS_CAGR.mean(),
               bd.OOS_Sharpe.mean(), bd.OOS_MaxDD.mean(), bd.mean_gross.mean())
            wr("CONTROL RULES v2 (live)", metrics(ctx["base_v2"][cb].loc[ctx["is_idx"]])["Sharpe"],
               v2_o["CAGR"], v2_o["Sharpe"], v2_o["MaxDD"], np.nan)
            wr("CONTROL SPY", metrics(ctx["spy"].loc[ctx["is_idx"]])["Sharpe"], spy_o["CAGR"],
               spy_o["Sharpe"], spy_o["MaxDD"], np.nan)
            rho = bd[["IS_Sharpe", "OOS_Sharpe"]].corr(method="spearman").iloc[0, 1]
            P(f"      Spearman(IS, OOS) over the 24 (T,L) cells: {rho:+.3f}   "
              f"budget IS-pick vs incumbent OOS: {pick.OOS_Sharpe-g075.OOS_Sharpe:+.4f}")
    pd.DataFrame(wf).to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    # ------------------------------------------------------------- D5: KEEP census
    P("\n" + "=" * 104)
    P("D5  KEEP-path census")
    P("=" * 104)
    for kind in ("BUDGET", "FIXED"):
        s = grid[grid.kind == kind]
        P(f"  {kind:7s}: 4b PASS {int(s.pass4b.sum())}/{len(s)}   4a PASS {int(s.pass4a.sum())}/{len(s)}")
        for pn, bn, _ in CELLS:
            ss = s[(s.panel == pn) & (s.book == bn)]
            P(f"     {pn:9s} {bn:24s} 4b {int(ss.pass4b.sum())}/{len(ss)}  "
              f"4a {int(ss.pass4a.sum())}/{len(ss)}")
    P("\nDone.")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_LINES) + "\n")


if __name__ == "__main__":
    main()

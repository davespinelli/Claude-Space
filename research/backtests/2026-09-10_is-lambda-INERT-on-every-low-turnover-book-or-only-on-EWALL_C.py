#!/usr/bin/env python3
"""Idea 620 — is lambda INERT on every LOW-TURNOVER book, or only on EWALL?   (lane C, 2026-09-10)

QUEUE 620: "idea 412 found the whole lambda ladder moves EWALL turnover by under 0.001 x/yr on
all three panels, which makes idea 137's dial unavailable on half the record's books and quietly
turns 6 of its 10 'lambda<1' picks into no-ops.  Sweep book concentration (n = 5..all) and ask
where lambda's turnover REACH crosses a usable threshold.  Max 2 params (n, lambda)."

WHAT IS ACTUALLY BEING TESTED
  H620 (the queue's own question)  Where on the concentration ladder n = 5 .. ALL does lambda's
     turnover reach cross a usable threshold?  Answered with a PRE-REGISTERED threshold ladder
     (absolute x/yr, relative to base turnover, and economic bps/yr at PROTOCOL's 10 bps rung),
     every rung reported, with the crossing n named per panel per cadence.
  HDRIVER (the queue's implied MECHANISM, and the thing that decides the title)  The queue's own
     title offers two rival explanations for the EWALL inertness: "low turnover" and "EWALL".
     They are DIFFERENT variables and idea 412 could not separate them, because it ran exactly
     two books, and the un-ranked one was also the low-turnover one.  This run separates them:
       - the n-ladder moves BOTH base turnover and raw-target churn together (confounded), but
       - two UN-RANKED CONTROLS (BAND, MA) sit at n = ALL — maximum diversification, zero
         ranking — while their MEMBERSHIP churns.  If lambda's reach is large there, then
         "concentration"/"low turnover" is refuted and the driver is the RAW TARGET's own churn,
         i.e. the quantity the EWMA actually operates on.
     Reported as: reach vs base turnover, reach vs RAWCHG, both correlations, both partials.
  HPATH  Does the dial move the BOOK (Sharpe span, tracking error) wherever it moves turnover?
     A dial with turnover reach and no path reach is still a no-op for every purpose but cost.
  RULE 8  Which chooser — JOINT (n, lambda), NONLY (n, lambda=1), LAMONLY (n=20, lambda) or the
     NO-DIAL control (n=20, lambda=1) — is the better instrument out of sample?  Parameters are
     chosen on 2009-2016 ALONE and 2017-2026 is read exactly once.  The NO-DIAL column is carried
     because idea 621 asks the record for it and it costs nothing to publish here.

AXES (PROTOCOL 4: no more than 2 tuned parameters — the queue names them)
  P1 n (book concentration): top-n of the composite among SCORED names, equal-weighted at
     GROSS/n, plus the endpoint ALL (= every scored name, equal weight) which is the un-ranked
     book.  The ladder is clipped per panel so every finite n is strictly less than that panel's
     MINIMUM daily scored count — n_sel is then exactly n on every day and the dial is clean.
  P2 lambda: idea 137's partial-rebalance dial, ladder lifted VERBATIM from idea 412.
  Panels (u56 / broad136 / small439), the two un-ranked CONTROL books (BAND, MA), cadence (D, W)
  and the cost rungs are REPORTED axes, never selected on.  Every grid point is reported.
  The only selection anywhere in this file is PROTOCOL rule 8.

GATES (before any new number is read)
  G1 the vectorised segment runner vs `engine.backtest` on returns AND turnover at D and W, on
     all three panels.
  G2 the rung identity r(c) = r(0) - turnover*c/1e4 vs a live `engine.backtest(cost_bps=25)`.
  G3 the n-ladder's ALL endpoint vs idea 412's OWN EWALL book (equal weight over PRICED names,
     not scored names): reported as a measured difference in turnover and returns, not asserted
     to be zero — the two definitions differ on names that are priced but not yet scorable.
  G4 REPRODUCTION: idea 412's committed `.grid.csv` EWALL and TOP20 turnovers at k=5/phase=0
     re-derived here from its own book definitions, all three panels, all eight lambdas.
  G5 monotonicity: turnover non-increasing in lambda, and in n, in every cell — exceptions
     counted and printed with their size rather than hidden.

CAVEATS CARRIED
  * SURVIVORSHIP (idea 54): current constituents on all three panels; SMALL439 drops the tickers
    with max_1d_move >= 1.0 from data/small_meta.csv before anything runs.
  * Idea 126: t+1 execution, no lag band.  Idea 38: u56/broad carry the calendar-day index.
  * MaxDD is one number off one path (idea 321); the 4b DD cap turns on exactly that number.
  * Idea 412: a cadence has a PHASE.  Cadence is CLOSED here at the record's own conventions
    (calendar D and W) precisely so that no phase nuisance enters a run about a different dial.
  * These are ungated, un-sleeved books; idea 412 already reported 0/4,608 on both KEEP paths for
    the same book family.  Both paths are priced anyway on every row, as PROTOCOL requires.

Deterministic, standalone.  Modifies nothing outside its own output files.
Writes .console.txt, .grid.csv, .reach.csv, .thresholds.csv, .driver.csv, .walkforward.csv.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-10_is-lambda-INERT-on-every-low-turnover-book-or-only-on-EWALL_C"
OUT = ROOT / "research" / "backtests"
I412 = OUT / "2026-09-10_does-PARTIAL-REBALANCING-beat-CADENCE-as-the-turnover-dial_cloud.grid.csv"

GROSS = 0.75                     # the record's book gross (idea 94 / 412)
NTOP = 20                        # the record's default concentration, used as the LAMONLY anchor
IS_END, OOS_START = "2016-12-31", "2017-01-01"
PHI, DELTA = 0.70, 0.60          # 4b CAGR floor and MaxDD cap, as fractions of SPY's
LAMBDAS = [1.00, 0.70, 0.50, 0.35, 0.25, 0.15, 0.10, 0.06]     # idea 137, verbatim via idea 412
NLADDER = [5, 10, 15, 20, 30, 40, 60, 90, 140, 220]            # finite rungs; ALL is the endpoint
ALL = 10 ** 9                    # sentinel for the un-ranked endpoint
# The SAME dial in its second natural unit (idea 590): coverage c = n / n_scored(t), which unlike
# absolute n reaches the un-ranked endpoint CONTINUOUSLY and can therefore locate the cliff.
CLADDER = [0.02, 0.05, 0.10, 0.20, 0.35, 0.50, 0.65, 0.80, 0.90, 0.95, 0.98, 0.99, 1.00]
# Un-ranked (n = ALL) CONTROL books.  BAND/MA churn in MEMBERSHIP and in GROSS (de-grossed, cash
# sleeve); MARS churns in MEMBERSHIP ONLY (re-spread to constant gross).  MARS is the cell that
# separates "the dial needs churn" from "the dial needs a swinging gross".
CONTROLS = ["BAND", "MA", "MARS"]
CADENCES = ["D", "W"]
RUNGS = [0.0, 5.0, 10.0, 25.0, 50.0]
PCOST = 10.0                     # PROTOCOL's own rung, used for the headline reach numbers
BAND = 0.03                      # RULES v2 clause 2 band
BARS5 = ["H1", "H2", "OOS", "DD", "CAGR"]

# PRE-REGISTERED "usable threshold" ladders (all reported; none selected on)
THR_ABS = [0.01, 0.05, 0.10, 0.25, 0.50, 1.00, 2.00]      # x/yr of turnover the dial can remove
THR_REL = [0.01, 0.05, 0.10, 0.25, 0.50]                  # as a fraction of base turnover
THR_BPS = [1.0, 5.0, 10.0, 25.0]                          # bps/yr of drag saved at 10 bps

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 4000)
LOG: list[str] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# =====================================================================================
# runner (idea 613's segment form; gated against engine.backtest below)
# =====================================================================================
def _mask(idx, freq):
    return rebalance_mask(idx, freq).shift(1, fill_value=False).values


def fast_bt(rets, w_t, mask):
    """engine.backtest's drift algebra, one pass per rebalance SEGMENT."""
    n = len(rets)
    reb = np.unique(np.concatenate(([0], np.flatnonzero(mask))))
    port = np.zeros(n)
    turn = np.zeros(n)
    cur = np.zeros(rets.shape[1])
    for si, i0 in enumerate(reb):
        i1 = reb[si + 1] if si + 1 < len(reb) else n
        if i1 <= i0:
            continue
        new = w_t[i0]
        turn[i0] = np.abs(new - cur).sum()
        A = new[None, :] * np.cumprod(1.0 + rets[i0:i1], axis=0)
        S = A.sum(axis=1) + (1.0 - new.sum())
        port[i0:i1] = S / np.concatenate(([1.0], S[:-1])) - 1.0
        cur = A[-1] / S[-1]
    return port, turn


def masks_of(px, freq):
    return _mask(px.index, freq)


def run(px, W, freq):
    rets = px.pct_change().fillna(0.0).values
    w_t = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    p, t = fast_bt(rets, w_t, _mask(px.index, freq))
    return pd.Series(p, index=px.index), pd.Series(t, index=px.index)


def smooth(W, lam):
    """Idea 137's partial-rebalance dial, verbatim: an EWMA of the raw target with gross restored
    daily, so the dial changes TRADING, not exposure."""
    if lam >= 1.0:
        return W
    S = W.ewm(alpha=lam, adjust=False).mean()
    g = S.sum(axis=1).replace(0, np.nan)
    return S.mul((W.sum(axis=1) / g).fillna(0.0), axis=0).fillna(0.0)


# =====================================================================================
# books
# =====================================================================================
def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def rank_book(comp, n):
    """Top-n of the composite among SCORED names, equal weight at GROSS/n.  n = ALL -> every
    scored name at GROSS/n_scored (the un-ranked endpoint of the same ladder)."""
    if n >= ALL:
        e = comp.notna().astype(float)
        return GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    r = comp.rank(axis=1, ascending=False)
    return (r <= n).astype(float) * (GROSS / n)


def ewall_412(sub):
    """Idea 412's OWN EWALL: equal weight over PRICED names (not scored ones).  G3/G4 only."""
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    return GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def top20_412(sub, comp):
    return (comp.rank(axis=1, ascending=False) <= NTOP).astype(float) * (GROSS / NTOP)


def cover_book(comp, c):
    """The SAME concentration dial in COVERAGE units: hold the top c-fraction of that day's
    scored names, equal weight at GROSS/n_t.  c = 1.00 is exactly the un-ranked book, reached
    CONTINUOUSLY — which absolute n cannot do without exceeding the panel."""
    scored = comp.notna()
    ns = scored.sum(axis=1)
    if c >= 1.0:
        e = scored.astype(float)
        return GROSS * e.div(ns.replace(0, np.nan), axis=0).fillna(0.0)
    k = np.maximum(1, np.rint(c * ns.values)).astype(float)
    sel = comp.rank(axis=1, ascending=False).le(pd.Series(k, index=comp.index), axis=0)
    e = sel.astype(float)
    return GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def control_book(sub, comp, kind):
    """UN-RANKED (n = ALL) books whose MEMBERSHIP churns.  BAND / MA are de-grossed, never
    re-spread — the gated-out weight goes to cash, exactly as RULES v2 does, so BOTH membership
    and GROSS churn.  MARS is the same MA membership RE-SPREAD to a constant GROSS, so ONLY
    membership churns; it is the cell that separates the two mechanisms.  sub and comp share
    columns."""
    ma = sub.rolling(200).mean()
    if kind == "BAND":
        raw = pd.DataFrame(np.nan, index=sub.index, columns=sub.columns)
        raw = raw.mask(sub > ma * (1 + BAND), 1.0).mask(sub < ma * (1 - BAND), 0.0)
        inn = raw.ffill().fillna(0.0) > 0.5
    else:
        inn = sub > ma
    scored = comp.notna()
    if kind == "MARS":
        e = (inn & scored).astype(float)
        return GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    e = scored.astype(float)
    ew = GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(inn & scored, 0.0)


# =====================================================================================
# metrics helpers
# =====================================================================================
def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_of(spy, which="full"):
    s = spy if which == "full" else spy.loc[:IS_END]
    h = len(s) // 2
    m = metrics(s)
    return dict(s1=metrics(s.iloc[:h])["Sharpe"], s2=metrics(s.iloc[h:])["Sharpe"],
                sdd=m["MaxDD"], scagr=m["CAGR"],
                soos=metrics(spy.loc[OOS_START:])["Sharpe"] if which == "full" else np.nan)


def margins(r, b, which="full"):
    s = r if which == "full" else r.loc[:IS_END]
    h = len(s) // 2
    m = metrics(s)
    d = dict(H1=metrics(s.iloc[:h])["Sharpe"] - b["s1"],
             H2=metrics(s.iloc[h:])["Sharpe"] - b["s2"],
             DD=DELTA * abs(b["sdd"]) - abs(m["MaxDD"]),
             CAGR=m["CAGR"] - PHI * b["scagr"])
    if which == "full":
        d["OOS"] = metrics(r.loc[OOS_START:])["Sharpe"] - b["soos"]
    return d


def pass4a(r, base):
    h1, h2 = halves(r)
    b1, b2 = halves(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad & set(px.columns))


def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 3:
        return np.nan
    return float(np.corrcoef(pd.Series(x[ok]).rank(), pd.Series(y[ok]).rank())[0, 1])


def partial_spearman(y, x, z):
    """Spearman partial correlation of y with x controlling for z (rank-then-residualise)."""
    y, x, z = (pd.Series(v, dtype=float) for v in (y, x, z))
    ok = y.notna() & x.notna() & z.notna()
    if ok.sum() < 4:
        return np.nan
    ry, rx, rz = (v[ok].rank().values for v in (y, x, z))
    Z = np.column_stack([np.ones_like(rz), rz])
    ey = ry - Z @ np.linalg.lstsq(Z, ry, rcond=None)[0]
    ex = rx - Z @ np.linalg.lstsq(Z, rx, rcond=None)[0]
    if ey.std() == 0 or ex.std() == 0:
        return np.nan
    return float(np.corrcoef(ey, ex)[0, 1])


# =====================================================================================
# gates
# =====================================================================================
def gates(panels):
    say("=" * 104)
    say("GATES (run before any new number is read)")
    say("=" * 104)
    ok = True
    for pk, (px, sub, comp, _) in panels.items():
        W = rank_book(comp, NTOP).reindex(columns=px.columns).fillna(0.0)
        start = px.index[260]
        g1 = []
        for f in CADENCES:
            rf, tf = run(px, W, f)
            e0 = backtest(px, W, cost_bps=0.0, freq=f)
            g1.append((f, float((rf.loc[start:] - e0["returns"].loc[start:]).abs().max()),
                       float((tf.loc[start:] - e0["turnover"].loc[start:]).abs().max())))
        say(f"  G1 {pk:>5}: segment runner vs engine.backtest  " +
            "  ".join(f"{f}: dr {a:.3e} dto {b:.3e}" for f, a, b in g1))
        ok &= all(a < 1e-12 and b < 1e-12 for _, a, b in g1)

        rf, tf = run(px, W, "W")
        e25 = backtest(px, W, cost_bps=25.0, freq="W")
        d2 = float(((rf - tf * 25.0 / 1e4).loc[start:] - e25["returns"].loc[start:]).abs().max())
        say(f"  G2 {pk:>5}: rung identity vs live engine.backtest(25)   max|dr| {d2:.3e}")
        ok &= d2 < 1e-12

        Wall = rank_book(comp, ALL).reindex(columns=px.columns).fillna(0.0)
        W412 = ewall_412(sub).reindex(columns=px.columns).fillna(0.0)
        ra, ta = run(px, Wall, "W")
        rb, tb = run(px, W412, "W")
        yrs = len(ta.loc[start:]) / 252
        say(f"  G3 {pk:>5}: n=ALL (scored) vs idea 412 EWALL (priced)  "
            f"turnover {ta.loc[start:].sum()/yrs:.4f} vs {tb.loc[start:].sum()/yrs:.4f} x/yr, "
            f"max|dr| {float((ra.loc[start:]-rb.loc[start:]).abs().max()):.3e}  (REPORTED, not asserted)")
    return ok


def gate4(panels):
    """G4 — reproduce idea 412's committed EWALL / TOP20 turnovers at k=5, phase=0, from its own
    book definitions.  Its k=5 cadence is a 5-trading-day grid, not the calendar week; the
    calendar 'W' column is printed beside it so the bridge is visible rather than assumed."""
    if not I412.exists():
        say("  G4: idea 412 grid.csv absent — reproduction gate SKIPPED (reported, not silent)")
        return True
    g = pd.read_csv(I412)
    g = g[(g.k == 5) & (g.phase == 0) & (g.cost == 0.0)]
    say("  G4 REPRODUCTION vs idea 412's committed grid (its books, its k=5 phase=0 grid):")
    worst = 0.0
    for pk, (px, sub, comp, _) in panels.items():
        start = px.index[260]
        idx = px.index
        m5 = np.zeros(len(idx), dtype=bool)
        m5[0::5] = True
        m5 = pd.Series(m5, index=idx).shift(1, fill_value=False).values
        rets = px.pct_change().fillna(0.0).values
        for bk, raw in (("EWALL", ewall_412(sub)), ("TOP20", top20_412(sub, comp))):
            raw = raw.reindex(columns=px.columns).fillna(0.0)
            for lam in LAMBDAS:
                W = smooth(raw, lam)
                w_t = W.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
                _, t = fast_bt(rets, w_t, m5)
                t = pd.Series(t, index=idx).loc[start:]
                mine = t.sum() / (len(t) / 252)
                ref = g[(g.panel == pk) & (g.book == bk) & (np.isclose(g.lam, lam))]["turnover"]
                if len(ref):
                    d = abs(mine - float(ref.iloc[0]))
                    worst = max(worst, d)
    say(f"       worst |d turnover| over 48 committed cells: {worst:.3e} x/yr  "
        f"{'PASS' if worst < 1e-9 else 'FAIL'}")
    return worst < 1e-9


# =====================================================================================
# grid
# =====================================================================================
def ladder_for(comp, start):
    nmin = int(comp.notna().loc[start:].sum(axis=1).min())
    return [n for n in NLADDER if n < nmin] + [ALL], nmin


def run_panel(pk, px, sub, comp, ndrop):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    bfull, bis = bars_of(spy, "full"), bars_of(spy, "IS")
    rets = px.pct_change().fillna(0.0).values
    masks = {f: _mask(px.index, f) for f in CADENCES}
    r2, t2 = run(px, rules_v2_weights(px), "W")         # the LIVE book, at its own weekly cadence
    v2 = {f: {c: (r2 - t2 * c / 1e4).loc[start:] for c in RUNGS} for f in CADENCES}
    lad, nmin = ladder_for(comp, start)
    say(f"\n  panel {pk}: {px.shape[1]} cols ({sub.shape[1]} investable"
        + (f", {ndrop} dropped for max_1d_move>=1.0" if ndrop else "")
        + f"), {start.date()} -> {px.index[-1].date()}; min daily scored {nmin}; "
        f"n-ladder {[('ALL' if n>=ALL else n) for n in lad]} + controls {CONTROLS}")
    say(f"    SPY bars: H1 {bfull['s1']:.3f}  H2 {bfull['s2']:.3f}  OOS {bfull['soos']:.3f}  "
        f"MaxDD {bfull['sdd']:.1%}  CAGR {bfull['scagr']:.2%}")

    # (family, label, builder).  RANKN and COVER are the SAME dial in two units; the CONTROLS are
    # un-ranked books carried as a reported axis.
    books = ([("RANKN", ("ALL" if n >= ALL else str(n)), (lambda n=n: rank_book(comp, n)))
              for n in lad]
             + [("COVER", f"c{c:.2f}", (lambda c=c: cover_book(comp, c))) for c in CLADDER]
             + [(k, "ALL", (lambda k=k: control_book(sub, comp, k))) for k in CONTROLS])
    rows, ser = [], {}
    for fam, lab, build in books:
        raw = build().reindex(columns=px.columns).fillna(0.0)
        # RAWCHG: the annualised L1 churn of the RAW TARGET — the quantity the EWMA acts on.
        rawchg = float(raw.diff().abs().sum(axis=1).loc[start:].mean() * 252)
        gmean = float(raw.sum(axis=1).loc[start:].mean())
        for lam in LAMBDAS:
            W = smooth(raw, lam)
            w_t = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
            for f in CADENCES:
                p, t = fast_bt(rets, w_t, masks[f])
                r0 = pd.Series(p, index=px.index).loc[start:]
                t0 = pd.Series(t, index=px.index).loc[start:]
                ser[(fam, lab, lam, f)] = (r0, t0)
                to = float(t0.sum() / (len(t0) / 252))
                for c in RUNGS:
                    r = r0 - t0 * c / 1e4
                    m = metrics(r)
                    mg, mgi = margins(r, bfull, "full"), margins(r, bis, "IS")
                    h1, h2 = halves(r)
                    rows.append(dict(
                        panel=pk, fam=fam, n=lab, lam=lam, cad=f, cost=c,
                        turnover=to, rawchg=rawchg, gross=gmean,
                        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                        OOSs=metrics(r.loc[OOS_START:])["Sharpe"],
                        OOScagr=metrics(r.loc[OOS_START:])["CAGR"],
                        OOSdd=metrics(r.loc[OOS_START:])["MaxDD"],
                        IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                        **{f"m_{x}": mg[x] for x in BARS5},
                        m_min=min(mg[x] for x in BARS5),
                        pass4b=all(mg[x] > 0 for x in BARS5),
                        pass4a=pass4a(r, v2[f][c]),
                        IS_pass4b=all(mgi[x] > 0 for x in ("H1", "H2", "DD", "CAGR"))))
    return pd.DataFrame(rows), ser, v2, bfull


# =====================================================================================
def reach_table(G, ser):
    """One row per (panel, book, cadence): the dial's REACH in turnover, drag, TE and Sharpe."""
    out = []
    for (pk, fam, n, f), g in G[G.cost == PCOST].groupby(["panel", "fam", "n", "cad"], sort=False):
        g = g.set_index("lam").sort_index(ascending=False)
        base_to = float(g.loc[1.00, "turnover"])
        mn, mx = float(g["turnover"].min()), float(g["turnover"].max())
        reach = base_to - mn
        r1 = ser[(fam, n, 1.00, f)][0]
        te = max(float(((ser[(fam, n, l, f)][0] - r1).std() * np.sqrt(252)))
                 for l in LAMBDAS if l < 1.0)
        out.append(dict(panel=pk, fam=fam, n=n, cad=f, base_to=base_to,
                        to_min=mn, to_max=mx, reach_abs=reach, reach_up=mx - base_to,
                        reach_rel=reach / base_to if base_to else np.nan,
                        drag10=reach * PCOST,           # bps/yr of cost saved at the 10 bps rung
                        TEreach=te,
                        Sreach=float(g["Sharpe"].max() - g["Sharpe"].min()),
                        CAGRreach=float(g["CAGR"].max() - g["CAGR"].min()),
                        rawchg=float(g["rawchg"].iloc[0]), gross=float(g["gross"].iloc[0])))
    return pd.DataFrame(out)


NORDER = {**{str(n): i for i, n in enumerate(NLADDER)}, "ALL": len(NLADDER)}
CORDER = {f"c{c:.2f}": i for i, c in enumerate(CLADDER)}


def crossings(R, fam, order):
    """The queue's own question, answered on a PRE-REGISTERED threshold ladder.  Reach FALLS as
    the book widens, so the crossing is the WIDEST rung that still meets the bar (or 'none')."""
    rows = []
    for (pk, f), g in R[R.fam == fam].groupby(["panel", "cad"], sort=False):
        g = g.assign(o=g["n"].map(order)).sort_values("o")
        for kind, thrs, col in (("abs x/yr", THR_ABS, "reach_abs"),
                                ("rel frac", THR_REL, "reach_rel"),
                                ("bps/yr@10", THR_BPS, "drag10")):
            for th in thrs:
                ok = g[g[col] >= th]
                rows.append(dict(panel=pk, cad=f, unit=fam, kind=kind, thr=th,
                                 widest=(str(ok["n"].iloc[-1]) if len(ok) else "none"),
                                 n_pass=int(len(ok)), n_rungs=int(len(g))))
    return pd.DataFrame(rows)


def walkforward(G, panels):
    """PROTOCOL rule 8: (n, lambda) chosen on 2009-2016 by IS Sharpe; 2017-2026 read ONCE.
    Four menus, including the NO-DIAL control idea 621 asks the record to publish."""
    rows = []
    for (fam, pk, f, c), g in G[G.fam.isin(["RANKN", "COVER"])].groupby(
            ["fam", "panel", "cad", "cost"], sort=False):
        px, sub, comp, _ = panels[pk]
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        so = metrics(spy.loc[OOS_START:])
        r2, t2 = run(px, rules_v2_weights(px), "W")
        b = (r2 - t2 * c / 1e4).loc[start:]
        bo = metrics(b.loc[OOS_START:])
        anchor = str(NTOP) if fam == "RANKN" else "c0.20"    # the record's default concentration
        menus = {
            "JOINT": g,
            "NONLY": g[g.lam == 1.00],
            "LAMONLY": g[g.n == anchor],
            "NODIAL": g[(g.lam == 1.00) & (g.n == anchor)],
        }
        for name, sel in menus.items():
            if not len(sel):
                continue
            pick = sel.loc[sel["IS_Sharpe"].idxmax()]
            rows.append(dict(unit=fam, panel=pk, cad=f, cost=c, menu=name,
                             n=pick["n"], lam=pick["lam"],
                             IS_Sharpe=pick["IS_Sharpe"], OOS_Sharpe=pick["OOSs"],
                             OOS_CAGR=pick["OOScagr"], OOS_MaxDD=pick["OOSdd"],
                             v2_OOS_Sharpe=bo["Sharpe"], v2_OOS_CAGR=bo["CAGR"],
                             v2_OOS_MaxDD=bo["MaxDD"],
                             spy_OOS_Sharpe=so["Sharpe"], spy_OOS_CAGR=so["CAGR"],
                             spy_OOS_MaxDD=so["MaxDD"],
                             beats_v2=bool(pick["OOSs"] > bo["Sharpe"]),
                             beats_spy=bool(pick["OOSs"] > so["Sharpe"])))
    return pd.DataFrame(rows)


# =====================================================================================
def main():
    T0 = time.time()
    say("=" * 104)
    say("IDEA 620 — is lambda INERT on every LOW-TURNOVER book, or only on EWALL?   (lane C)")
    say("=" * 104)
    say(f"tuned parameter 1 (n)      : {NLADDER} + ALL, clipped per panel to n < min daily scored")
    say(f"tuned parameter 2 (lambda) : {LAMBDAS}   (idea 137's ladder, verbatim)")
    say(f"reported axes: panels u56/broad/small, un-ranked CONTROL books {CONTROLS}, "
        f"cadence {CADENCES}, rungs {RUNGS} bps")
    say(f"t+1 execution, gross {GROSS}; IS <= {IS_END}, OOS >= {OOS_START}; "
        f"headline reach read at the {PCOST:.0f} bps rung")
    say("pre-registered usable thresholds: "
        f"abs {THR_ABS} x/yr | rel {THR_REL} | economic {THR_BPS} bps/yr")

    # Panel tuple = (full px incl. the SPY benchmark column, INVESTABLE sub-panel, its composite,
    # n dropped).  u56/broad carry SPY as a constituent by the record's convention (idea 412);
    # on SMALL439 SPY is a benchmark only and is excluded from the investable set.
    P = {}
    u = load_universe()
    P["u56"] = (u, u, composite(u), 0)
    b = load_universe(broad=True)
    P["broad"] = (b, b, composite(b), 0)
    s, nd = small_panel()
    ssub = s[[c for c in s.columns if c != "SPY"]]
    P["small"] = (s, ssub, composite(ssub), nd)

    if not gates(P):
        say("\n*** G1/G2 FAILED — no new number is read. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
        return 1
    if not gate4(P):
        say("\n*** G4 REPRODUCTION FAILED — no new number is read. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
        return 1
    say(f"  gates done in {time.time()-T0:.0f}s")

    say("\n" + "=" * 104)
    say("GRID — every point reported")
    say("=" * 104)
    Gs, SER, V2, BARS = [], {}, {}, {}
    for pk, (px, sub, comp, nd) in P.items():
        g, ser, v2, bfull = run_panel(pk, px, sub, comp, nd)
        Gs.append(g)
        SER[pk] = ser
        V2[pk], BARS[pk] = v2, bfull
        say(f"    {pk} done, {len(g)} rows, {time.time()-T0:.0f}s elapsed")
    G = pd.concat(Gs, ignore_index=True)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    say(f"\n  grid: {len(G)} rows written to {STEM}.grid.csv")

    # ---- G5 monotonicity -------------------------------------------------------------
    bad_l, worst_l, exc = 0, 0.0, []
    for (pk, fam, n, f), g in G[G.cost == 0.0].groupby(["panel", "fam", "n", "cad"], sort=False):
        t = g.sort_values("lam", ascending=False)["turnover"].values
        d = np.diff(t)
        if (d > 1e-12).any():
            bad_l += 1
            worst_l = max(worst_l, float(d.max()))
            exc.append((pk, fam, n, f, float(d.max()), float(t.max() - t[0])))
    ntot = 0
    bad_n, worst_n = 0, 0.0
    for fam, order in (("RANKN", NORDER), ("COVER", CORDER)):
        for (pk, f, lam), g in G[(G.cost == 0.0) & (G.fam == fam)].groupby(
                ["panel", "cad", "lam"], sort=False):
            ntot += 1
            t = g.assign(o=g["n"].map(order)).sort_values("o")["turnover"].values
            d = np.diff(t)
            if (d > 1e-12).any():
                bad_n += 1
                worst_n = max(worst_n, float(d.max()))
    say(f"  G5 monotone DOWN in lambda: {bad_l} exception cells (worst wrong-way step "
        f"{worst_l:.3e} x/yr); monotone DOWN in width: {bad_n}/{ntot} exception cells "
        f"(worst {worst_n:.3e})")
    if exc:
        say("     lambda exceptions, every one listed (panel, family, n, cadence, worst step, "
            "total rise above base):")
        for e in exc:
            say(f"       {e[0]:>5} {e[1]:>5} n={e[2]:>5} {e[3]}  step {e[4]:+.4f}  rise {e[5]:+.4f} x/yr")

    # ---- REACH -----------------------------------------------------------------------
    R = pd.concat([reach_table(G[G.panel == pk], SER[pk]) for pk in P], ignore_index=True)
    R.to_csv(OUT / f"{STEM}.reach.csv", index=False)
    say("\n" + "=" * 104)
    say("FINDING 1 — lambda's REACH along the concentration ladder (10 bps rung, all points)")
    say("=" * 104)
    for f in CADENCES:
        say(f"\n  cadence {f}:")
        sh = R[R.cad == f].pivot_table(index=["panel", "fam", "n"],
                                       values=["base_to", "rawchg", "reach_abs", "reach_rel",
                                               "drag10", "TEreach", "Sreach"], sort=False)
        say(sh.to_string(float_format=lambda x: f"{x:.4f}"))

    # ---- THRESHOLD CROSSINGS ---------------------------------------------------------
    X = pd.concat([crossings(R, "RANKN", NORDER), crossings(R, "COVER", CORDER)],
                  ignore_index=True)
    X.to_csv(OUT / f"{STEM}.thresholds.csv", index=False)
    say("\n" + "=" * 104)
    say("FINDING 2 — the queue's question: WHERE does the reach cross a usable threshold?")
    say("  (reach falls as the book widens, so the entry is the WIDEST rung still meeting the bar)")
    say("=" * 104)
    for unit in ("RANKN", "COVER"):
        say(f"\n  ---- dial unit: {unit} "
            + ("(absolute n; the ladder stops short of the panel by construction)"
               if unit == "RANKN" else "(coverage c = n/n_scored; reaches c = 1.00 CONTINUOUSLY)"))
        for kind in X["kind"].unique():
            say(f"  threshold kind: {kind}")
            say(X[(X.kind == kind) & (X.unit == unit)].pivot_table(
                index="thr", columns=["cad", "panel"], values="widest",
                aggfunc="first", sort=False).to_string())

    # ---- DRIVER: concentration/low-turnover vs raw-target churn ----------------------
    say("\n" + "=" * 104)
    say("FINDING 3 — WHICH variable drives the inertness: base TURNOVER, or the RAW TARGET's churn?")
    say("=" * 104)
    drows = []
    for f in CADENCES:
        s = R[R.cad == f]
        for pop, sel in (("RANKN ladder", s[s.fam == "RANKN"]),
                         ("COVER ladder", s[s.fam == "COVER"]),
                         ("both ladders", s[s.fam.isin(["RANKN", "COVER"])]),
                         ("ladders + CONTROLS", s)):
            drows.append(dict(cad=f, pop=pop, k=len(sel),
                              rho_reach_baseto=spearman(sel.reach_abs, sel.base_to),
                              rho_reach_rawchg=spearman(sel.reach_abs, sel.rawchg),
                              part_baseto=partial_spearman(sel.reach_abs, sel.base_to, sel.rawchg),
                              part_rawchg=partial_spearman(sel.reach_abs, sel.rawchg, sel.base_to)))
    D = pd.DataFrame(drows)
    D.to_csv(OUT / f"{STEM}.driver.csv", index=False)
    say(D.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    say("\n  THE DECISIVE CELLS — un-ranked books (every one is n = ALL, i.e. zero concentration),")
    say("  ordered by raw-target churn.  eff = reach_abs / rawchg is what one unit of target churn")
    say("  buys the dial; a book with churn but no reach would refute the churn explanation.")
    key = R[R.n == "ALL"].sort_values(["cad", "panel", "rawchg"]).copy()
    key["eff"] = key.reach_abs / key.rawchg.replace(0, np.nan)
    say(key[["panel", "cad", "fam", "gross", "base_to", "rawchg", "reach_abs", "reach_up",
             "reach_rel", "eff", "drag10", "TEreach", "Sreach"]].to_string(
        index=False, float_format=lambda x: f"{x:.4f}"))
    say("\n  the same efficiency along the COVER ladder (reach per unit of raw-target churn):")
    cv = R[R.fam == "COVER"].copy()
    cv["eff"] = cv.reach_abs / cv.rawchg.replace(0, np.nan)
    say(cv.pivot_table(index="n", columns=["cad", "panel"], values="eff", sort=False).to_string(
        float_format=lambda x: f"{x:.4f}"))

    # ---- KEEP PATHS ------------------------------------------------------------------
    say("\n" + "=" * 104)
    say("KEEP PATHS — both, priced on every grid row")
    say("=" * 104)
    say(f"  4a (beat the LIVE RULES v2 book, cost-matched): {int(G.pass4a.sum())} / {len(G)}")
    say(f"  4b (capital-worthy vs SPY, all five bars):      {int(G.pass4b.sum())} / {len(G)}")
    say(f"  BOTH: {int((G.pass4a & G.pass4b).sum())} / {len(G)}")
    say("  by rung: " + "  ".join(
        f"{c:.0f}bps 4a {int(G[G.cost==c].pass4a.sum())}/4b {int(G[G.cost==c].pass4b.sum())}"
        for c in RUNGS))
    if G.pass4b.any():
        say("\n  4b passers:")
        say(G[G.pass4b][["panel", "fam", "n", "lam", "cad", "cost", "CAGR", "Sharpe", "MaxDD",
                         "H1", "H2", "OOSs", "m_min"]].to_string(
            index=False, float_format=lambda x: f"{x:.4f}"))
    say("\n  binding 4b bar (the least-slack margin), count by bar over all rows: " +
        "  ".join(f"{x} {int((G[[f'm_{y}' for y in BARS5]].idxmin(axis=1) == f'm_{x}').sum())}"
                 for x in BARS5))

    # ---- RULE 8 ----------------------------------------------------------------------
    WF = walkforward(G, P)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say("\n" + "=" * 104)
    say("PROTOCOL RULE 8 — (n, lambda) chosen on 2009-2016 ALONE; 2017-2026 read exactly once")
    say("=" * 104)
    say(WF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\n  menu summary by DIAL UNIT (median over the 30 panel x cadence x rung cells each):")
    S = WF.groupby(["unit", "menu"]).agg(OOS_Sharpe=("OOS_Sharpe", "median"),
                                         OOS_CAGR=("OOS_CAGR", "median"),
                                         OOS_MaxDD=("OOS_MaxDD", "median"),
                                         beats_v2=("beats_v2", "sum"),
                                         beats_spy=("beats_spy", "sum"),
                                         cells=("menu", "size"))
    say(S.to_string(float_format=lambda x: f"{x:.4f}"))
    say("\n  menu summary POOLED over both units (60 cells each):")
    S = WF.groupby("menu").agg(OOS_Sharpe=("OOS_Sharpe", "median"),
                               OOS_CAGR=("OOS_CAGR", "median"),
                               OOS_MaxDD=("OOS_MaxDD", "median"),
                               beats_v2=("beats_v2", "sum"),
                               beats_spy=("beats_spy", "sum"),
                               cells=("menu", "size"))
    say(S.to_string(float_format=lambda x: f"{x:.4f}"))
    say(f"  SPY OOS Sharpe {WF.spy_OOS_Sharpe.min():.4f}-{WF.spy_OOS_Sharpe.max():.4f}, "
        f"CAGR {WF.spy_OOS_CAGR.min():.2%}-{WF.spy_OOS_CAGR.max():.2%}, "
        f"MaxDD {WF.spy_OOS_MaxDD.min():.2%}")
    say(f"  RULES v2 OOS Sharpe {WF.v2_OOS_Sharpe.min():.4f}-{WF.v2_OOS_Sharpe.max():.4f}, "
        f"CAGR {WF.v2_OOS_CAGR.min():.2%}-{WF.v2_OOS_CAGR.max():.2%}")
    K = ["unit", "panel", "cad", "cost"]
    for m in ("JOINT", "NONLY", "LAMONLY"):
        a = WF[WF.menu == m].set_index(K)["OOS_Sharpe"]
        z = WF[WF.menu == "NODIAL"].set_index(K)["OOS_Sharpe"]
        d = (a - z).dropna()
        say(f"  {m:>7} vs the NO-DIAL control (idea 621's column): beats it in "
            f"{int((d>0).sum())}/{len(d)} cells, median dSharpe {d.median():+.4f}")
    a = WF[WF.menu == "JOINT"].set_index(K)["OOS_Sharpe"]
    for m in ("NONLY", "LAMONLY"):
        z = WF[WF.menu == m].set_index(K)["OOS_Sharpe"]
        d = (a - z).dropna()
        say(f"    JOINT vs the better-known single dial {m:>7}: JOINT wins "
            f"{int((d>0).sum())}/{len(d)}, median dSharpe {d.median():+.4f}")
    for u in ("RANKN", "COVER"):
        lp = WF[(WF.menu == "JOINT") & (WF.unit == u)]["lam"]
        say(f"  JOINT chooser ({u} unit) picks lambda<1 in {int((lp<1).sum())}/{len(lp)} cells "
            f"(idea 137 reported 6/10)")
    say("  UNIT AGREEMENT (idea 590's question): do the two units of the SAME dial pick the same "
        "lambda?")
    piv = WF[WF.menu == "JOINT"].pivot_table(index=["panel", "cad", "cost"], columns="unit",
                                             values="lam", aggfunc="first")
    if {"RANKN", "COVER"} <= set(piv.columns):
        agree = int((piv["RANKN"] == piv["COVER"]).sum())
        say(f"    same lambda in {agree}/{len(piv)} cells; "
            f"median |d lambda| {float((piv['RANKN']-piv['COVER']).abs().median()):.3f}")

    # ---- APPENDIX: idea 311's gross sweep on every 4b passer's book form ---------------
    # Idea 311 found 98.1% of the record's committed 4b passes were never run at a second gross
    # inside their own file, and 97.6% of the ones that WERE swept flip verdict on their own
    # ladder.  Gross is a REPORTED axis here, never tuned: the whole ladder is printed and the
    # admissible band is stated, so this run's own 4b passers cannot join that 98.1%.
    if G.pass4b.any():
        say("\n" + "=" * 104)
        say("APPENDIX (idea 311) — the 4b passers' book form re-run on a GROSS ladder, all points")
        say("=" * 104)
        glad = [round(x, 2) for x in np.arange(0.50, 1.301, 0.05)]
        arows = []
        for pk in sorted(G[G.pass4b].panel.unique()):
            px, sub, comp, _ = P[pk]
            start = px.index[260]
            spy = px["SPY"].pct_change().fillna(0).loc[start:]
            bf = bars_of(spy, "full")
            rets = px.pct_change().fillna(0.0).values
            base = control_book(sub, comp, "MARS").reindex(columns=px.columns).fillna(0.0)
            for g_ in glad:
                W = base * (g_ / GROSS)
                w_t = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
                for f in CADENCES:
                    p_, t_ = fast_bt(rets, w_t, masks_of(px, f))
                    r0 = pd.Series(p_, index=px.index).loc[start:]
                    t0 = pd.Series(t_, index=px.index).loc[start:]
                    for c in RUNGS:
                        r = r0 - t0 * c / 1e4
                        m = metrics(r)
                        mg = margins(r, bf, "full")
                        arows.append(dict(panel=pk, book="MARS", gross=g_, cad=f, cost=c,
                                          CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                          **{f"m_{x}": mg[x] for x in BARS5},
                                          m_min=min(mg[x] for x in BARS5),
                                          pass4b=all(mg[x] > 0 for x in BARS5)))
        A = pd.DataFrame(arows)
        A.to_csv(OUT / f"{STEM}.gross.csv", index=False)
        say(f"  {len(A)} rows over gross {glad[0]}-{glad[-1]}")
        say(A[A.cost == PCOST].pivot_table(index="gross", columns=["panel", "cad"],
                                           values="m_min", sort=False).to_string(
            float_format=lambda x: f"{x:+.4f}"))
        say(f"\n  4b passes on the gross ladder at {PCOST:.0f} bps: "
            f"{int(A[A.cost==PCOST].pass4b.sum())} / {len(A[A.cost==PCOST])}")
        for (pk, f), gg in A[A.cost == PCOST].groupby(["panel", "cad"], sort=False):
            ok = gg[gg.pass4b]["gross"]
            say(f"    {pk:>5} {f}: admissible gross band "
                + (f"[{ok.min():.2f}, {ok.max():.2f}] of {len(glad)} rungs ({len(ok)} pass)"
                   if len(ok) else "EMPTY — no gross on the ladder passes"))
        say("  (idea 311's bar: a 4b pass that holds on ONE gross only is a g-band artefact.)")

    say(f"\n  total runtime {time.time()-T0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

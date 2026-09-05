#!/usr/bin/env python3
"""QUEUE idea 128 — shallow-window-prices-are-not-prices (lane C, 2026-09-05).

Question (pre-registered, verbatim from QUEUE)
----------------------------------------------
"idea 122 found dMaxDD <= 0 in 40 of 138 IS-window rows and 0 of 138 OOS rows, i.e. the
2009-2016 window (SPY MaxDD -22.1%) cannot measure a drawdown instrument at all while
2017-2026 (-33.7%) can.  Test the boundary on rolling 4-year windows: regress the fraction
of arms with a positive denominator on the window's own SPY MaxDD and report the depth at
which the fraction crosses 90%.  Bears on rule 8's IS window and on ideas 111/117."

What is being measured.  Every drawdown "price" this project publishes is

    rate = (CAGR_ctl - CAGR_arm) / (|MaxDD_ctl| - |MaxDD_arm|)      pp CAGR per pp MaxDD

and the denominator dMaxDD is a difference of two single-day extrema.  An evaluation window
that never contains a real drawdown gives BOTH legs a shallow, essentially arbitrary MaxDD,
so dMaxDD is noise around zero and the ratio is meaningless.  Idea 122 showed this happens
in idea 94's IS half and never in its OOS half.  This run asks WHERE the boundary is, as a
number in units of the window's own SPY MaxDD, so PROTOCOL can state a MEASURABILITY DEPTH
instead of naming particular calendar windows.

DESIGN (fixed before any number below was read)
    Corpus: idea 94's arms, imported unchanged and asserted to reproduce its published
    denominators.  3 books (V1u, TOP20, EWall) x 17 treated arms x 2 universes
    (universe.json 56, universe_broad.json 136), at the PROTOCOL cost point 10 bps.
    -> 102 arm-series + 6 controls.  Each arm's denominator is recomputed inside every
    rolling window; the arm itself is never re-fitted (the book is the same book, only the
    measuring window moves), so the ONLY thing varying is the depth of the ruler.

    Rolling windows: length L years, start dates stepping monthly across the evaluated
    sample.  For each window w:
        depth(w)  = |MaxDD of SPY| inside w              (the window's own depth)
        frac(w)   = share of the 102 arms with dMaxDD(w) > 0
    Regress frac on depth (OLS).  Report the crossing depth where the fit reaches p*, and
    the EMPIRICAL crossing (the shallowest depth above which every depth-decile bin holds
    frac >= p*).  Overlapping windows are not independent, so the headline t-stat is
    computed on the DISJOINT subset (step = L) as well as on all windows.

Tuned parameters (PROTOCOL rule 4).  TWO, both of the MEASUREMENT and neither of any
trading rule:
    L   window length in years, {2, 3, 4, 5, 6}
    p*  crossing fraction, {0.80, 0.90, 0.95}
All 15 grid points reported.  L = 4, p* = 0.90 is the queue's pre-registered headline.

Walk-forward (PROTOCOL rule 8), fixed before any OOS number was read.  Selection on
2009-2016 only; 2017-2026 untouched.  In each (universe, book) cell:
    S0  no instrument — hold the control book (the do-nothing benchmark).
    S1  idea 94's selector, unchanged: among arms buying >= 1.0 pp of IS MaxDD, take the
        LOWEST IS rate, measured on the FULL 2009-2016 window.
    S2  the same selector, but every price measured on the DEEPEST L-year sub-window inside
        2009-2016 instead of the whole IS half.  This is the depth clause turned into a
        selector; it consults no OOS data.
    Reported for all three: OOS CAGR / Sharpe / MaxDD vs the cell control, vs live RULES v1
    and vs SPY.  Both KEEP paths (4a vs live v1, 4b vs SPY) evaluated on every arm-point.

Pre-registered predictions (written before any number was read)
    P1  frac(w) rises with depth(w) with a positive slope, t > 2 on the disjoint windows.
    P2  the 90% crossing sits DEEPER than 22.1% (rule 8's IS half), i.e. the IS window is
        formally unable to price these instruments, and shallower than 33.7% (the OOS half).
    P3  the relation is book-dependent: the 5-name V1u book needs a deeper ruler than EWall
        (idea 122 found every panel/cost sign failure in V1u).
    P4  this is a measurement run: S2 does not manufacture a KEEP and its OOS Sharpe is
        within noise of S1's.

Execution realism (PROTOCOL rule 2): inherited from idea 94 — weekly decision at close t
applied at t+1, long-only, no leverage, 10 bps per unit turnover charged inside the loop.

SURVIVORSHIP: universe.json / universe_broad.json are current-constituent lists, so every
absolute level is optimistic.  This run reports the STABILITY OF A SIGN as a function of
window depth; a survivorship-free panel would deepen every drawdown and could only move the
crossing, not the direction of the relation.
INDEX: with BTC/ETH excluded (baseline.EXCLUDE) both panels load on a trading-day index
(3679/846 one/three-day gaps), so idea 38's calendar-day defect does not bite this run.

Deterministic, standalone.  Imports research/baseline.py and idea 94's script; modifies
nothing.
"""
import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))

from baseline import rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

BT = ROOT / "research" / "backtests"
_s94 = importlib.util.spec_from_file_location(
    "i94", BT / "2026-09-04_drawdown-insurance-price-list_B.py")
H = importlib.util.module_from_spec(_s94)
_s94.loader.exec_module(H)

STEM = Path(__file__).stem
OUT = BT / STEM
PCOST = 10.0
PUB_COSTS = [10.0, 25.0]                      # the rungs idea 94 published (reproduction only)
IS_END, OOS_START = H.IS_END, H.OOS_START
BOOKS = list(H.BOOKS)
ARMS = [(n, k, kw, sp) for (n, k, kw, sp) in H.arm_specs() if n != "control"]
UNIS = [("universe.json(56)", dict()), ("universe_broad.json", dict(broad=True))]
LS = (2, 3, 4, 5, 6)                          # tuned parameter 1: window length (years)
PSTARS = (0.80, 0.90, 0.95)                   # tuned parameter 2: crossing fraction
L_STAR, P_STAR = 4, 0.90                      # the queue's pre-registered headline point
STEP_MONTHS = 1
FLOOR = 0.10                                  # idea 94's absolute floor, kept for continuity
MIN_BUY = 1.0                                 # idea 94's selector: >= 1.0 pp of IS MaxDD

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 4000)


def fmt(df):
    return df.to_string(index=False, float_format=lambda x: f"{x:.4f}")


def signals(px):
    return dict(comp=H.composite(px), v20=H.vol20(px), ma=px.rolling(200).mean())


def dpair(rc, ra):
    """(dCAGR, dMaxDD) in pp and idea 94's floored rate."""
    mc, ma = metrics(rc), metrics(ra)
    dc = (mc["CAGR"] - ma["CAGR"]) * 100.0
    dd = (abs(mc["MaxDD"]) - abs(ma["MaxDD"])) * 100.0
    return dc, dd, (dc / dd if dd > FLOOR else np.nan)


def maxdd(r):
    eq = (1 + r).cumprod()
    return float((eq / eq.cummax() - 1).min())


def ols(x, y):
    """slope, intercept, t(slope), R^2 — plain OLS, no correction."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    n = len(x)
    if n < 3 or x.std() == 0:
        return dict(n=n, slope=np.nan, icept=np.nan, t=np.nan, r2=np.nan)
    b, a = np.polyfit(x, y, 1)
    yhat = a + b * x
    ss = float(((y - yhat) ** 2).sum())
    se = np.sqrt(ss / (n - 2) / float(((x - x.mean()) ** 2).sum()))
    return dict(n=n, slope=float(b), icept=float(a), t=float(b / se) if se else np.nan,
                r2=float(1 - ss / ((y - y.mean()) ** 2).sum()))


# ---------------------------------------------------------------- returns corpus
def build_returns(uname, kw):
    px = H.load_universe(**kw)
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    S = signals(px)

    # engine-equivalence guard: H.run with every instrument off must equal engine.backtest
    worst = 0.0
    for b in BOOKS:
        W = H.targets(px, b)
        a = H.run(px, W, bps=PCOST)["r"].loc[start:]
        e = backtest(px, W, cost_bps=PCOST, freq=H.FREQ)["returns"].loc[start:]
        worst = max(worst, float((a - e).abs().max()))
    print(f"[check] {uname}: H.run vs engine.backtest max|diff| = {worst:.3e} "
          f"({'EXACT' if worst < 1e-12 else 'NOT EXACT — unsafe'})")

    rets = {}
    for b in BOOKS:
        for name, kind, kwargs, (g, conv) in H.arm_specs():
            W = H.targets(px, b, g, conv)
            for c in PUB_COSTS:
                rets[(b, name, c)] = H.run(px, W, bps=c, **kwargs)["r"].loc[start:]
    v1_net = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=H.FREQ)["returns"].loc[start:]
              for c in PUB_COSTS}
    return px, start, spy, rets, v1_net


def published_rows(uname, spy, rets, v1_net):
    """Idea 94/122's published table: the reproduction guard and the 4a/4b tabulation."""
    bars = H.bars_of(spy)
    rows = []
    for b in BOOKS:
        for c in PUB_COSTS:
            rc = rets[(b, "control", c)]
            for name, kind, _, _ in ARMS:
                ra = rets[(b, name, c)]
                dc, dd, rate = dpair(rc, ra)
                dc_i, dd_i, rt_i = dpair(rc.loc[:IS_END], ra.loc[:IS_END])
                dc_o, dd_o, rt_o = dpair(rc.loc[OOS_START:], ra.loc[OOS_START:])
                m, mg = metrics(ra), H.margins(ra, bars)
                rows.append(dict(uni=uname, book=b, cost=c, arm=name, kind=kind,
                                 dCAGR=dc, dMaxDD=dd, rate=rate,
                                 published=bool(np.isfinite(rate)),
                                 dMaxDD_IS=dd_i, dMaxDD_OOS=dd_o,
                                 rate_IS=rt_i, rate_OOS=rt_o,
                                 CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                 p4a=H.pass4a(ra, v1_net[c]),
                                 p4b=all(v > 0 for v in mg.values()),
                                 f4b=",".join([k for k, v in mg.items() if not v > 0]) or "-"))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- rolling windows
def window_starts(index, L, step_months=STEP_MONTHS):
    t0, tN = index[0], index[-1]
    out, s = [], pd.Timestamp(t0)
    while True:
        e = s + pd.DateOffset(years=L) - pd.Timedelta(days=1)
        if e > tN:
            break
        out.append((s, e))
        s = s + pd.DateOffset(months=step_months)
    return out


def rolling_table(uname, spy, rets, L):
    """One row per rolling window: its own SPY depth and the share of arms with dMaxDD > 0."""
    wins = window_starts(spy.index, L)
    ctl = {b: rets[(b, "control", PCOST)] for b in BOOKS}
    rows = []
    for (s, e) in wins:
        sw = spy.loc[s:e]
        if len(sw) < 200:
            continue
        depth = abs(maxdd(sw)) * 100.0
        pos, tot, per_book = 0, 0, {}
        for b in BOOKS:
            cw = ctl[b].loc[s:e]
            ddc = abs(maxdd(cw)) * 100.0
            bp, bt = 0, 0
            for name, _, _, _ in ARMS:
                aw = rets[(b, name, PCOST)].loc[s:e]
                dd = ddc - abs(maxdd(aw)) * 100.0
                bp += int(dd > 0)
                bt += 1
            per_book[b] = bp / bt
            pos += bp
            tot += bt
        rows.append(dict(uni=uname, L=L, start=s.date(), end=e.date(), depth=depth,
                         ctl_dd_V1u=abs(maxdd(ctl["V1u"].loc[s:e])) * 100.0,
                         frac=pos / tot, n_arms=tot,
                         **{f"frac_{b}": per_book[b] for b in BOOKS}))
    return pd.DataFrame(rows)


def crossings(R, pstar, col="frac"):
    """Fitted and empirical depth at which `col` crosses pstar."""
    f = ols(R.depth, R[col])
    fit = (pstar - f["icept"]) / f["slope"] if np.isfinite(f["slope"]) and f["slope"] != 0 else np.nan
    # empirical: shallowest depth d such that EVERY window with depth >= d has col >= pstar
    d = R.sort_values("depth", ascending=False)
    emp, run = np.nan, True
    for _, row in d.iterrows():
        if row[col] >= pstar and run:
            emp = row["depth"]
        else:
            run = False
    # decile version: shallowest depth decile from which all deeper deciles have mean >= pstar
    q = pd.qcut(R.depth, min(10, max(2, R.depth.nunique() // 3)), duplicates="drop")
    g = R.groupby(q, observed=True).agg(depth_lo=("depth", "min"), m=(col, "mean")).sort_index()
    dec, run = np.nan, True
    for lo, m in zip(g.depth_lo.values[::-1], g.m.values[::-1]):
        if m >= pstar and run:
            dec = lo
        else:
            run = False
    return dict(slope=f["slope"], icept=f["icept"], t=f["t"], r2=f["r2"], n=f["n"],
                cross_fit=fit, cross_strict=emp, cross_decile=dec,
                frac_at_221=f["icept"] + f["slope"] * 22.1 if np.isfinite(f["slope"]) else np.nan,
                frac_at_337=f["icept"] + f["slope"] * 33.7 if np.isfinite(f["slope"]) else np.nan)


# ---------------------------------------------------------------- walk-forward
def deepest_subwindow(spy, L, lo, hi):
    """The L-year window inside [lo, hi] with the largest |SPY MaxDD|.  IS data only."""
    best, bd = None, -1.0
    s = pd.Timestamp(lo)
    while True:
        e = s + pd.DateOffset(years=L) - pd.Timedelta(days=1)
        if e > pd.Timestamp(hi):
            break
        sw = spy.loc[s:e]
        if len(sw) >= 200:
            d = abs(maxdd(sw))
            if d > bd:
                best, bd = (s, e), d
        s = s + pd.DateOffset(months=STEP_MONTHS)
    return best, bd * 100.0


def select(cell_rets, ctl, lo, hi):
    """Idea 94's selector on the window [lo, hi]: among arms buying >= MIN_BUY pp of MaxDD,
    the lowest rate.  Returns (arm, rate, dMaxDD) or (None, ...) if nothing is eligible."""
    cw = ctl.loc[lo:hi]
    best, brate = None, np.inf
    for name, r in cell_rets.items():
        dc, dd, rate = dpair(cw, r.loc[lo:hi])
        if dd >= MIN_BUY and np.isfinite(rate) and rate < brate:
            best, brate = name, rate
    return best, (brate if best else np.nan)


def walk_forward(uname, spy, rets, v1_net, L):
    spy_o = spy.loc[OOS_START:]
    mo_spy = metrics(spy_o)
    (dlo, dhi), ddepth = deepest_subwindow(spy, L, spy.index[0], IS_END)
    rows = []
    for b in BOOKS:
        ctl = rets[(b, "control", PCOST)]
        cell = {n: rets[(b, n, PCOST)] for n, _, _, _ in ARMS}
        picks = dict(
            S0=("control", np.nan),
            S1=select(cell, ctl, spy.index[0], IS_END),
            S2=select(cell, ctl, dlo, dhi))
        for sel, (arm, rate) in picks.items():
            r_o = (ctl if arm in (None, "control") else rets[(b, arm, PCOST)]).loc[OOS_START:]
            m = metrics(r_o)
            mc = metrics(ctl.loc[OOS_START:])
            rows.append(dict(uni=uname, L=L, book=b, selector=sel,
                             pick=(arm or "NONE(->control)"), IS_rate=rate,
                             IS_window=(f"{spy.index[0].date()}..{IS_END}" if sel != "S2"
                                        else f"{dlo.date()}..{dhi.date()}"),
                             IS_depth=(abs(maxdd(spy.loc[:IS_END])) * 100.0 if sel != "S2"
                                       else ddepth),
                             OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"],
                             ctl_OOS_Sharpe=mc["Sharpe"], ctl_OOS_CAGR=mc["CAGR"],
                             ctl_OOS_MaxDD=mc["MaxDD"],
                             v1_OOS_Sharpe=metrics(v1_net[PCOST].loc[OOS_START:])["Sharpe"],
                             v1_OOS_CAGR=metrics(v1_net[PCOST].loc[OOS_START:])["CAGR"],
                             v1_OOS_MaxDD=metrics(v1_net[PCOST].loc[OOS_START:])["MaxDD"],
                             spy_OOS_Sharpe=mo_spy["Sharpe"], spy_OOS_CAGR=mo_spy["CAGR"],
                             spy_OOS_MaxDD=mo_spy["MaxDD"]))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    print(__doc__)
    ALLP, ALLR, ALLW = [], [], []
    store = {}
    for uname, kw in UNIS:
        print(f"\n================ {uname} ================", flush=True)
        px, start, spy, rets, v1_net = build_returns(uname, kw)
        store[uname] = (spy, rets, v1_net)
        P = published_rows(uname, spy, rets, v1_net)
        ALLP.append(P)
        print(f"[{uname}] {px.shape[1]} names, evaluated {start.date()}..{px.index[-1].date()}, "
              f"SPY MaxDD full {abs(maxdd(spy))*100:.1f}pp  IS {abs(maxdd(spy.loc[:IS_END]))*100:.1f}pp  "
              f"OOS {abs(maxdd(spy.loc[OOS_START:]))*100:.1f}pp   ({time.time()-t0:.0f}s)")
        for L in LS:
            R = rolling_table(uname, spy, rets, L)
            ALLR.append(R)
            print(f"    L={L}y: {len(R)} windows, depth {R.depth.min():.1f}..{R.depth.max():.1f}pp"
                  f"  ({time.time()-t0:.0f}s)", flush=True)
            ALLW.append(walk_forward(uname, spy, rets, v1_net, L))

    P = pd.concat(ALLP, ignore_index=True)
    R = pd.concat(ALLR, ignore_index=True)
    WF = pd.concat(ALLW, ignore_index=True)

    # ---------------- 0. reproduction guard against idea 122's published counts
    print("\n=== 0. REPRODUCTION (idea 122's D2 counts on idea 94's published rows) ===")
    pub = P[P.published]
    rep = pd.DataFrame([dict(rows_total=len(P), rows_published=len(pub),
                             IS_dMaxDD_le0=int((pub.dMaxDD_IS <= 0).sum()),
                             OOS_dMaxDD_le0=int((pub.dMaxDD_OOS <= 0).sum()),
                             full_dMaxDD_le0=int((pub.dMaxDD <= 0).sum()),
                             p4a=int(P.p4a.sum()), p4b=int(P.p4b.sum()))])
    print(fmt(rep))
    print("idea 122 published: 138 priceable rows, IS dMaxDD<=0 in 40, OOS in 0, 4a 54/192, 4b 29/192")
    rep.to_csv(f"{OUT}.reproduction.csv", index=False)

    # ---------------- 0b. is 0/138 a fact about the OOS window, or about the filter?
    # The queue's premise reads the 40-vs-0 contrast as "the shallow window cannot measure".
    # But `published` conditions on dMaxDD_FULL > 0.10, and if the full-sample MaxDD of both
    # legs is ATTAINED INSIDE THE OOS WINDOW then dMaxDD_full == dMaxDD_OOS identically and
    # the 0 is a tautology.  Test it directly.
    print("\n=== 0b. WHERE IS THE FULL-SAMPLE MaxDD ATTAINED? (is 0/138 a tautology?) ===")
    loc = []
    for uname, _ in UNIS:
        spy, rets, _ = store[uname]
        for b in BOOKS:
            for name, _, _, _ in ARMS + [("control", "", {}, ())]:
                r = rets[(b, name, PCOST)]
                eq = (1 + r).cumprod()
                trough = (eq / eq.cummax() - 1).idxmin()
                loc.append(dict(uni=uname, book=b, arm=name, trough=trough,
                                in_OOS=bool(trough >= pd.Timestamp(OOS_START))))
        loc.append(dict(uni=uname, book="SPY", arm="SPY",
                        trough=((1 + spy).cumprod() / (1 + spy).cumprod().cummax() - 1).idxmin(),
                        in_OOS=True))
    LOC = pd.DataFrame(loc)
    LOC["in_OOS"] = [t >= pd.Timestamp(OOS_START) for t in LOC.trough]
    print(fmt(LOC.groupby(["uni", "book"]).agg(n=("arm", "size"),
                                               trough_in_OOS=("in_OOS", "sum")).reset_index()))
    LOC.to_csv(f"{OUT}.troughs.csv", index=False)
    idn = pub.assign(same=lambda d: (d.dMaxDD - d.dMaxDD_OOS).abs() < 1e-9)
    print(f"published rows where dMaxDD_full == dMaxDD_OOS exactly: {int(idn.same.sum())} of {len(idn)}"
          f"   corr(dMaxDD_full, dMaxDD_OOS) = {pub.dMaxDD.corr(pub.dMaxDD_OOS):.3f}"
          f"   corr(dMaxDD_full, dMaxDD_IS) = {pub.dMaxDD.corr(pub.dMaxDD_IS):.3f}")
    unc = P[P.cost == PCOST]
    print(f"UNCONDITIONAL (no priceability filter, 10 bps, {len(unc)} arm-rows): "
          f"dMaxDD_IS > 0 in {int((unc.dMaxDD_IS > 0).sum())}, "
          f"dMaxDD_OOS > 0 in {int((unc.dMaxDD_OOS > 0).sum())}, "
          f"dMaxDD_full > 0 in {int((unc.dMaxDD > 0).sum())}")

    print("\n--- 4a/4b by book (all arm-points, both cost rungs) ---")
    print(fmt(P.groupby(["uni", "book"]).agg(n=("arm", "size"), p4a=("p4a", "sum"),
                                             p4b=("p4b", "sum")).reset_index()))

    # ---------------- 1. the rolling-window curve
    R.to_csv(f"{OUT}.windows.csv", index=False)
    print("\n=== 1. ROLLING WINDOWS: frac(dMaxDD>0) vs the window's own SPY MaxDD ===")
    print("(depth deciles, headline L=4y, both universes pooled)")
    H4 = R[R.L == L_STAR]
    q = pd.qcut(H4.depth, 10, duplicates="drop")
    dec = H4.groupby(q, observed=True).agg(n=("frac", "size"), depth_lo=("depth", "min"),
                                           depth_hi=("depth", "max"), frac=("frac", "mean"),
                                           **{f"f_{b}": (f"frac_{b}", "mean") for b in BOOKS}
                                           ).reset_index(drop=True)
    print(fmt(dec))
    dec.to_csv(f"{OUT}.deciles.csv", index=False)

    # ---------------- 2. THE GRID: all 15 (L, p*) points, per universe and pooled
    print("\n=== 2. GRID (all 15 points reported; L=4, p*=0.90 pre-registered) ===")
    grid = []
    for L in LS:
        for scope in ["POOLED"] + [u for u, _ in UNIS]:
            sub = R[(R.L == L)] if scope == "POOLED" else R[(R.L == L) & (R.uni == scope)]
            if sub.empty:
                continue
            # disjoint subset: step by the window length so no two windows overlap
            dis = sub.sort_values("start").iloc[::max(1, L * 12 // STEP_MONTHS)]
            fd = ols(dis.depth, dis.frac)
            for p in PSTARS:
                c = crossings(sub, p)
                grid.append(dict(L=L, pstar=p, scope=scope, n_win=len(sub),
                                 slope=c["slope"], t_all=c["t"], r2=c["r2"],
                                 n_disj=fd["n"], t_disj=fd["t"],
                                 cross_fit=c["cross_fit"], cross_strict=c["cross_strict"],
                                 cross_decile=c["cross_decile"],
                                 fit_at_IS22=c["frac_at_221"], fit_at_OOS34=c["frac_at_337"]))
    G = pd.DataFrame(grid)
    print(fmt(G))
    G.to_csv(f"{OUT}.grid.csv", index=False)

    # ---------------- 3. per-book crossings at the headline point
    print(f"\n=== 3. PER-BOOK at L={L_STAR}y, p*={P_STAR} (prediction P3: V1u needs a deeper ruler) ===")
    pb = []
    for scope in ["POOLED"] + [u for u, _ in UNIS]:
        sub = R[(R.L == L_STAR)] if scope == "POOLED" else R[(R.L == L_STAR) & (R.uni == scope)]
        for b in BOOKS:
            c = crossings(sub, P_STAR, col=f"frac_{b}")
            pb.append(dict(scope=scope, book=b, slope=c["slope"], t=c["t"], r2=c["r2"],
                           cross_fit=c["cross_fit"], cross_strict=c["cross_strict"],
                           cross_decile=c["cross_decile"],
                           fit_at_IS=c["frac_at_221"], fit_at_OOS=c["frac_at_337"]))
    PB = pd.DataFrame(pb)
    print(fmt(PB))
    PB.to_csv(f"{OUT}.perbook.csv", index=False)

    # ---------------- 4. the two rule-8 windows themselves
    print("\n=== 4. RULE 8's OWN WINDOWS (not 4y — the actual IS/OOS halves) ===")
    r8 = []
    for uname, _ in UNIS:
        spy, rets, _ = store[uname]
        for wname, lo, hi in [("IS 2009-2016", spy.index[0], IS_END),
                              ("OOS 2017-2026", pd.Timestamp(OOS_START), spy.index[-1])]:
            depth = abs(maxdd(spy.loc[lo:hi])) * 100.0
            pos, tot = 0, 0
            per = {}
            for b in BOOKS:
                cw = rets[(b, "control", PCOST)].loc[lo:hi]
                ddc = abs(maxdd(cw)) * 100.0
                bp = sum(int(ddc - abs(maxdd(rets[(b, n, PCOST)].loc[lo:hi])) * 100.0 > 0)
                         for n, _, _, _ in ARMS)
                per[f"frac_{b}"] = bp / len(ARMS)
                pos += bp
                tot += len(ARMS)
            r8.append(dict(uni=uname, window=wname, years=round((pd.Timestamp(hi) - pd.Timestamp(lo)).days / 365.25, 1),
                           depth=depth, frac=pos / tot, **per))
    R8 = pd.DataFrame(r8)
    print(fmt(R8))
    R8.to_csv(f"{OUT}.rule8windows.csv", index=False)

    # ---------------- 4b. depth held fixed, LENGTH varied (the confound)
    print("\n=== 4b. MATCHED DEPTH, VARYING LENGTH — does a LONGER ruler do what a DEEPER "
          "one does not? (bands of the window's own SPY MaxDD) ===")
    bands = [(9, 15), (15, 21), (21, 28), (28, 35)]
    ml = []
    for lo, hi in bands:
        for L in LS:
            sub = R[(R.L == L) & (R.depth >= lo) & (R.depth < hi)]
            if len(sub) < 5:
                continue
            ml.append(dict(band=f"{lo}-{hi}pp", L=L, n=len(sub), frac=sub.frac.mean(),
                           **{f"f_{b}": sub[f"frac_{b}"].mean() for b in BOOKS}))
    ML = pd.DataFrame(ml)
    print(fmt(ML))
    ML.to_csv(f"{OUT}.lengthmatched.csv", index=False)

    # ---------------- 5. walk-forward
    print("\n=== 5. WALK-FORWARD (rule 8): S0 control / S1 idea 94 selector on the full IS "
          "half / S2 the same selector on the DEEPEST IS sub-window ===")
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    print(fmt(WF[WF.L == L_STAR][["uni", "book", "selector", "pick", "IS_window", "IS_depth",
                                  "IS_rate", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]]))
    print("\n--- mean OOS by selector, across L (S2's window depends on L; S0/S1 do not) ---")
    print(fmt(WF.groupby(["L", "selector"]).agg(
        OOS_Sharpe=("OOS_Sharpe", "mean"), OOS_CAGR=("OOS_CAGR", "mean"),
        OOS_MaxDD=("OOS_MaxDD", "mean"),
        n_changed=("pick", "size")).reset_index()))
    b = WF.iloc[0]
    print(f"\nbenchmarks (OOS 2017-2026): RULES v1 {b.v1_OOS_CAGR:.2%}/{b.v1_OOS_Sharpe:.3f}/"
          f"{b.v1_OOS_MaxDD:.1%}   SPY {b.spy_OOS_CAGR:.2%}/{b.spy_OOS_Sharpe:.3f}/{b.spy_OOS_MaxDD:.1%}")
    chg = (WF[WF.selector == "S1"].set_index(["uni", "L", "book"]).pick !=
           WF[WF.selector == "S2"].set_index(["uni", "L", "book"]).pick)
    print(f"S1 vs S2 picks differ in {int(chg.sum())} of {len(chg)} (universe, L, book) cells")

    P.to_csv(f"{OUT}.pricelist.csv", index=False)
    print(f"\n[done {time.time()-t0:.0f}s]")


if __name__ == "__main__":
    main()

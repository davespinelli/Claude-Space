#!/usr/bin/env python3
"""Idea 576 (lane B, 2026-09-12) - price-the-ZERO-CASH-convention-on-the-gross-LADDER.

QUESTION
--------
Idea 311 swept the gross scalar g over 6 unlevered book-forms x 3 panels x 2 cadences x 17
grosses = 612 books and found Sharpe is NOT invariant in g: it drifts +0.0065/unit g, small
but systematic and positive across all 36 cells.  Idea 576 reads that as the signature of the
engine's convention that de-grossed NAV (the 1 - g a book does not invest) earns ZERO: a book
at g = 0.20 parks 80% of NAV in a 0% asset, a book at g = 1.00 parks none.  Re-run the same
ladder crediting cash at 150 and 300 bps and report whether the slope flattens, whether any
admissible 4b band widens, and whether the U56/B136 ordering of band widths survives.

The algebra says the credit cannot simply "flatten" anything:

    r_p = g * R + (1-g) * c   =>   Sharpe = mu/sigma + ((1-g)/g) * c/sigma

At c = 0 that second term vanishes and Sharpe is flat in g - so the convention predicts a
ZERO slope, not a +0.0065 one.  At c > 0 the term is positive and falling in g, so a credit
pushes the slope DOWN, hard.  Either way the idea's premise ("the +0.0065 IS the zero-cash
convention") is testable, and this run tests it three ways: the slope at each rate, the
implied break-even rate that would zero it, and the same slope re-read under the coherent
convention where Sharpe's own risk-free rate equals the credited cash rate.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two): the CASH RATE c and the GROSS g.  Panel,
form and cadence are reported axes; all 1,836 grid points are written to .grid.csv and none
is dropped from any headline.

CASH CONVENTION (stated, not tuned): c is a FLAT annual simple rate credited daily at
c/1e4/252 on the un-invested NAV fraction, compounding between rebalances exactly as the
risky legs do.  A flat rate is wrong in level over 2009-2026 - that is idea 642's open
question and this run does NOT answer it; 0/150/300 bps brackets the realised average.  The
BASELINE is reported twice at each c: RULES v2 at the committed 0% convention and RULES v2
credited at the same c (it de-grosses to cash at gross 0.75, so the credit touches it too).
SPY is fully invested and is unaffected by c.

PRE-REGISTERED HYPOTHESES (written before any cash-credited book was run)
------------------------------------------------------------------------
H_FLAT    : the median Sharpe-vs-g slope over the 36 cells shrinks in MAGNITUDE monotonically
            in c: |med slope(300)| < |med slope(150)| < |med slope(0)|.  This is idea 576's
            own claim - that the +0.0065 is the zero-cash convention.
H_SIGN    : the slope is NEGATIVE in a majority of cells at c = 300 bps (the ((1-g)/g)*c/sigma
            term dominating), i.e. the credit OVERSHOOTS flat rather than flattening.
H_WIDEN   : the admissible 4b g-band is weakly wider at 300 bps than at 0 in a majority of the
            36 cells (the credit lifts CAGR most at low g, where the CAGR floor binds, so the
            band should extend DOWN).
H_ORDER   : the U56-vs-B136 ordering of MEDIAN band width is the same at all three rates.
H_KEEP    : no book passes BOTH keep paths at any c (idea 311 found 0/612).

H_EXCESS is a CONVENTION DIAGNOSTIC added after a one-cell smoke test (U56/MA-RS/W) returned a
credited slope of -0.437, i.e. two orders of magnitude past "flat".  It is reported for all 36
cells and it is not a re-tuning of the five hypotheses above:
H_EXCESS  : under the coherent reading - Sharpe's own risk-free rate set to the SAME c for the
            book and for SPY - the slope in g is INVARIANT in c: |slope_x(c) - slope_x(0)| <=
            0.0100 (idea 51's invariance bar) in a majority of cells.  If this passes, every
            move H_FLAT/H_SIGN see is an artefact of scoring a cash-credited book against a
            zero risk-free rate, and the native +0.0065 is not a cash phenomenon at all.

Rule 8 (walk-forward, REQUIRED): at each c the band is solved on 2009-2016 ONLY, the form is
picked by IS Sharpe and g as the IS band midpoint, and 2017-2026 is read ONCE - reporting OOS
CAGR/Sharpe/MaxDD against RULES v2 (both conventions) and SPY, and whether the IS-chosen g is
still inside that c's OOS band.  WF-A is the per-cell IS-band-vs-OOS-band leg.

Costs 10 bps per unit turnover, weights decided at close t applied t+1 (engine convention),
no shorting, no leverage (g <= 1.00 everywhere).

SURVIVORSHIP: B136 and the small panel are CURRENT constituents (universe_broad.json is
today's list; the small panel is today's sub-$2B screen).  Small-panel names with
max_1d_move >= 1.0 in data/small_meta.csv are dropped FIRST, per PROTOCOL.  Panels are cut at
2026-09-04, idea 311's cut.

DATA DRIFT (measured, not assumed): idea 311's committed .grid.csv was produced on caches that
the repository no longer holds - today's small panel screens 663 tradable names, not the 439
idea 311 ran, so its SMALL439 rows have no counterpart here at all.  G1 therefore gates on
EXACT agreement with idea 311's own committed script re-run on today's panels, and the
distance from its committed numbers is REPORTED as a drift measurement rather than asserted.

GATES
-----
G1  this run's runner == idea 311's committed runner, bit-for-bit, on today's panels; plus a
    reported drift table against its committed .grid.csv.
G2  fast_backtest(cash=0) == engine.backtest on a real book (both the cached and uncached path).
G3  a ZERO-WEIGHT book at c bps earns exactly the credit, every day, at every c.
G4  a book with NO cash leg (EWall at g = 1.00, always fully invested) is INVARIANT in c.
"""
import sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask  # noqa

STAMP = Path(__file__).name[:-3]
OUT = Path(__file__).resolve().parent
COST = 10.0
MA_WIN = 200
IS_END, OOS_START = "2016-12-31", "2017-01-01"
PANEL_END = "2026-09-04"                                   # idea 311's cut
CADENCE = ["W", "M"]
GGRID = [round(0.20 + 0.05 * i, 2) for i in range(17)]     # 0.20 .. 1.00, unlevered
CASHGRID = [0.0, 150.0, 300.0]                             # bps/yr, flat
DAYS = 252.0
PARENT_PY = "2026-09-09_does-4b-discriminate-ANYTHING-on-gross-scalar-books_cloud.py"
PARENT = "2026-09-09_does-4b-discriminate-ANYTHING-on-gross-scalar-books_cloud.grid.csv"
G1_TOL, G2_TOL, G3_TOL, G4_TOL = 0.0, 1e-12, 1e-14, 1e-14
INVAR_BAR = 0.0100
FORMS = ["EWall", "MA-RS", "MA-DG", "TOP20", "TOP10", "MA20"]
CONTROL = "EWall"
LEGS = ("H1", "H2", "OOS", "DD", "CAGR")
SHARPE_LEGS = ("H1", "H2", "OOS")

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


# ------------------------------------------------------------------ vectorised runner
def precompute(prices, freqs=CADENCE):
    """Everything in fast_backtest that depends only on (prices, freq), hoisted out so the
    same panel can be run at 17 grosses x 3 cash rates without recomputing it."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, C.shape[1])), C[:-1]])
    pre = {"idx": idx, "rets": rets, "T": len(idx)}
    for f in freqs:
        mask = rebalance_mask(idx, f).shift(1, fill_value=False).values.copy()
        mask[0] = True
        reb = np.flatnonzero(mask)
        seg = np.searchsorted(reb, np.arange(len(idx)), side="right") - 1
        s0 = reb[seg]
        s0p = reb[np.maximum(seg - 1, 0)]
        pre[f] = {"reb": reb, "s0": s0, "s0p": s0p,
                  "D": Cp / Cp[s0], "Dp": Cp / Cp[s0p], "Cp": Cp}
    return pre


def fast_backtest(prices, weights, cost_bps=COST, freq="W", cash_bps=0.0, pre=None):
    """Idea 312/568's vectorised equivalent of engine.backtest, generalised so the un-invested
    NAV fraction earns `cash_bps` a year (flat, cash_bps/1e4/252 a day) and compounds between
    rebalances exactly as the risky legs do.  cash_bps = 0 reproduces engine.backtest
    bit-for-bit (G2)."""
    if pre is None:
        pre = precompute(prices, [freq])
    idx, rets = pre["idx"], pre["rets"]
    p = pre[freq]
    reb, s0, s0p, D, Dp = p["reb"], p["s0"], p["s0p"], p["D"], p["Dp"]
    T = pre["T"]
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    rc = cash_bps / 1e4 / DAYS
    Kc = np.cumprod(np.full(T, 1.0 + rc))
    Kcp = np.concatenate([[1.0], Kc[:-1]])
    W0 = wt[s0]
    h = W0 * D
    hc = (1.0 - W0.sum(axis=1)) * (Kcp / Kcp[s0])          # the drifting cash leg
    V = h.sum(axis=1) + hc
    held = h / V[:, None]
    heldc = hc / V
    W0p = wt[s0p]
    hp = W0p * Dp
    hcp = (1.0 - W0p.sum(axis=1)) * (Kcp / Kcp[s0p])
    Vp = hp.sum(axis=1) + hcp
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    port = (held * rets).sum(axis=1) + heldc * rc - turn * cost_bps / 1e4
    return {"returns": pd.Series(port, index=idx), "turnover": pd.Series(turn, index=idx)}


# ------------------------------------------------------------------------- helpers
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


def sharpe(r, rf=0.0):
    return metrics(r, rf=rf)["Sharpe"]


def halves(r, rf=0.0):
    h = len(r) // 2
    return sharpe(r.iloc[:h], rf), sharpe(r.iloc[h:], rf)


def rowify(r, tn=None, rf=0.0):
    """Idea 311's row, plus the same four Sharpes re-read at risk-free rate rf (the coherent
    reading of a cash-credited book).  rf is an ANNUAL absolute rate (0.015 = 150 bps)."""
    m = metrics(r)
    h1, h2 = halves(r)
    mi, mo = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    d = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
             IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
             OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])
    if rf:
        h1x, h2x = halves(r, rf)
        d.update(Sharpe_x=sharpe(r, rf), H1_x=h1x, H2_x=h2x,
                 IS_Sharpe_x=sharpe(r.loc[:IS_END], rf), OOS_Sharpe_x=sharpe(r.loc[OOS_START:], rf))
    else:
        d.update(Sharpe_x=d["Sharpe"], H1_x=h1, H2_x=h2,
                 IS_Sharpe_x=d["IS_Sharpe"], OOS_Sharpe_x=d["OOS_Sharpe"])
    if tn is not None:
        d["turnover"] = float(tn.sum() / m["Years"])
    return d


def keep_4a(r, b):
    a1, a2 = halves(r)
    b1, b2 = halves(b)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(b)["MaxDD"])


def legs_4b(r, spy, sub=False, rf=0.0):
    """PROTOCOL 4b's five legs as booleans (idea 311's reading).  rf > 0 reads the three
    Sharpe legs at a common risk-free rate for BOTH the book and SPY; the DD and CAGR legs are
    untouched by rf."""
    a1, a2 = halves(r, rf)
    s1, s2 = halves(spy, rf)
    m, ms = metrics(r), metrics(spy)
    sh_r = sharpe(r, rf) if sub else sharpe(r.loc[OOS_START:], rf)
    sh_s = sharpe(spy, rf) if sub else sharpe(spy.loc[OOS_START:], rf)
    return dict(H1=bool(a1 > s1), H2=bool(a2 > s2), OOS=bool(sh_r > sh_s),
                DD=bool(m["MaxDD"] >= 0.60 * ms["MaxDD"]),
                CAGR=bool(m["CAGR"] >= 0.70 * ms["CAGR"]))


def fail_str(lg):
    f = [k for k, v in lg.items() if not v]
    return ",".join(f) if f else "-"


def ols(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    A = np.vstack([np.ones_like(x), x]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    resid = y - A @ coef
    ss = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - float((resid ** 2).sum()) / ss if ss > 0 else np.nan
    return float(coef[0]), float(coef[1]), r2


def band_from(sub, legcols=("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")):
    """Admissible g-band = the set of g where every named leg passes."""
    ok = sub[list(legcols)].all(axis=1).values
    gs = sub["gross"].values
    if not ok.any():
        always_fail = [c for c in legcols if not sub[c].any()]
        sharpe_names = {f"{p_}{k}" for k in SHARPE_LEGS
                        for p_ in ("L_", "ISL_", "OOSL_", "X_", "ISX_", "OOSX_")}
        reason = "SHARPE" if set(always_fail) & sharpe_names else "SCALE"
        return (np.nan, np.nan, 0.0, 0, True, reason)
    idx = np.flatnonzero(ok)
    lo, hi = float(gs[idx[0]]), float(gs[idx[-1]])
    interval = bool(idx[-1] - idx[0] + 1 == len(idx))
    return (lo, hi, hi - lo, int(ok.sum()), interval, "-")


# ------------------------------------------------------------------------- panels
def small_tradables(pxs):
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    return [c for c in pxs.columns if c != "SPY" and c not in bad]


def real_panels():
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    s_stk = small_tradables(pxs)
    return {
        "U56": (px56.dropna(how="all").ffill().loc[:PANEL_END], set(px56.columns)),
        "B136": (px136.dropna(how="all").ffill().loc[:PANEL_END], set(px136.columns)),
        f"SMALL{len(s_stk)}": (pxs[s_stk + ["SPY"]].dropna(how="all").ffill().loc[:PANEL_END],
                               set(s_stk)),
    }


# ------------------------------------------------------------- the book-form menu
_SCORE: dict = {}


def form_weights(name, px, tradable, g, key=None):
    """Idea 311's pre-registered menu of unlevered forms whose only free dial is g."""
    e = _priced(px, tradable) > 0
    if name == "EWall":
        return _ew(e, g)
    ma = above_ma(px) & e
    if name == "MA-RS":
        return _ew(ma, g)
    if name == "MA-DG":
        n = e.sum(axis=1).replace(0, np.nan)
        return g * ma.astype(float).div(n, axis=0).fillna(0.0)
    if key is not None and key in _SCORE:
        s = _SCORE[key]
    else:
        s, _, _ = score(px, vol_scale=False)
        s = s.where(e)
        if key is not None:
            _SCORE[key] = s
    if name in ("TOP20", "TOP10"):
        k = 20 if name == "TOP20" else 10
        rk = s.rank(axis=1, ascending=False)
        return _ew(rk <= k, g)
    if name == "MA20":
        rk = s.where(ma).rank(axis=1, ascending=False)
        return _ew(rk <= 20, g)
    raise ValueError(name)


# ==================================================================================== run
def main():
    t0 = time.time()
    P("=" * 118)
    P("IDEA 576  price-the-ZERO-CASH-convention-on-the-gross-LADDER   (lane B, 2026-09-12)")
    P("=" * 118)
    P("Re-run idea 311's 612-book gross ladder crediting the un-invested NAV at 0 / 150 / 300 bps.")
    P(f"g grid {GGRID[0]}..{GGRID[-1]} step 0.05 ({len(GGRID)} pts) x cash {[int(c) for c in CASHGRID]} bps "
      f"x {len(FORMS)} forms x 3 panels x {len(CADENCE)} cadences = "
      f"{len(GGRID)*len(CASHGRID)*len(FORMS)*3*len(CADENCE)} books.")
    P("10 bps costs, t+1 fills, no leverage.  Cash is FLAT (c/1e4/252 a day) and compounds between")
    P("rebalances; a flat rate is wrong in level over 2009-2026 (idea 642's question, NOT answered")
    P("here) - 0/150/300 brackets the realised average.")
    P("SURVIVORSHIP: B136 and the small panel are CURRENT constituents; small-panel names with")
    P("max_1d_move >= 1.0 dropped first.  Panels cut at " + PANEL_END + " (idea 311's cut).")
    P("")

    # ---------------------------------------------------------------- panels + refs
    panels = real_panels()
    SMALLK = [k for k in panels if k.startswith("SMALL")][0]
    ref, PRE = {}, {}
    for nm, (px, tr) in panels.items():
        PRE[nm] = precompute(px)
        st = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        v2w = rules_v2_weights(px)
        ref[nm] = dict(start=st, spy=spy,
                       v2={c: fast_backtest(px, v2w, COST, "W", c, PRE[nm])["returns"].loc[st:]
                           for c in CASHGRID})
        P(f"  {nm:9s} {px.shape[1]:4d} cols, {len(tr):4d} tradable, sample from {st.date()} "
          f"to {px.index[-1].date()}  ({time.time()-t0:.0f}s)")

    # ---------------------------------------------------------------- G1 reproduction
    P("")
    P("=" * 118)
    P("G1  REPRODUCTION GATE - this runner vs idea 311's COMMITTED SCRIPT on today's panels")
    P("=" * 118)
    import importlib.util
    spec = importlib.util.spec_from_file_location("idea311", OUT / PARENT_PY)
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    worst1 = 0.0
    for nm, (px, tr) in panels.items():
        for form in FORMS:
            for freq in CADENCE:
                for g in (0.20, 0.60, 1.00):
                    wo = old.form_weights(form, px, tr, g)
                    wn = form_weights(form, px, tr, g, key=nm)
                    dw = float((wo - wn).abs().max().max())
                    dr = float((old.fast_backtest(px, wo, COST, freq)["returns"]
                                - fast_backtest(px, wn, COST, freq, 0.0, PRE[nm])["returns"]
                                ).abs().max())
                    worst1 = max(worst1, dw, dr)
        P(f"  {nm:9s} 36 book-points checked, worst |dweight| / |dreturn| so far {worst1:.3e}  "
          f"({time.time()-t0:.0f}s)")
    assert worst1 <= G1_TOL, f"G1 FAILED at {worst1:.3e}"
    P(f"  G1 PASS - identical to idea 311's committed runner at {worst1:.1e} over 108 book-points")
    P("  (both the cached-precompute path and idea 311's original are exercised here.)")

    # -------------------------------------------------------- G1b drift vs the committed CSV
    P("")
    P("  DRIFT (reported, NOT asserted) - distance from idea 311's committed .grid.csv, which")
    P("  was produced on caches the repository no longer holds:")
    par = pd.read_csv(OUT / PARENT)
    cmpcols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe", "IS_CAGR", "IS_MaxDD",
               "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "turnover"]
    drows = []
    for nm, (px, tr) in panels.items():
        st = ref[nm]["start"]
        for form in FORMS:
            for freq in CADENCE:
                for g in GGRID:
                    res = fast_backtest(px, form_weights(form, px, tr, g, key=nm), COST, freq,
                                        0.0, PRE[nm])
                    r = res["returns"].loc[st:]
                    row = dict(panel=nm, form=form, cadence=freq, gross=g)
                    row.update(rowify(r, res["turnover"].loc[st:]))
                    drows.append(row)
    G0 = pd.DataFrame(drows)
    mm = G0.merge(par, on=["panel", "form", "cadence", "gross"], suffixes=("", "_p"))
    P(f"  committed panels {sorted(par.panel.unique())};  today's panels {sorted(panels)};  "
      f"rows matched {len(mm)}/612")
    if len(mm):
        dd = pd.DataFrame({c: (mm[c] - mm[c + "_p"]).abs() for c in cmpcols})
        for pnl in sorted(mm.panel.unique()):
            s = dd[mm.panel.values == pnl]
            P(f"    {pnl:9s} max |d| {float(s.max().max()):.3e} on `{s.max().idxmax()}`;  "
              f"Sharpe {float(s.Sharpe.max()):.2e}  OOS_Sharpe {float(s.OOS_Sharpe.max()):.2e}  "
              f"turnover {float(s.turnover.max()):.2e}")
    P(f"    {SMALLK:9s} NOT COMPARABLE - idea 311 ran SMALL439; today's screen carries "
      f"{len(panels[SMALLK][1])} tradable names, so no row matches.")

    # ---------------------------------------------------------------- G2 identity
    P("")
    P("=" * 118)
    P("G2  IDENTITY GATE - fast_backtest(cash=0) vs engine.backtest")
    P("=" * 118)
    worst = 0.0
    for nm, (px, tr) in panels.items():
        w = form_weights("MA-RS", px, tr, 0.75, key=nm)
        eng = backtest(px, w, cost_bps=COST, freq="W")["returns"]
        d1 = float((fast_backtest(px, w, COST, "W", 0.0, PRE[nm])["returns"] - eng).abs().max())
        d2 = float((fast_backtest(px, w, COST, "W", 0.0, None)["returns"] - eng).abs().max())
        worst = max(worst, d1, d2)
        P(f"  {nm:9s} max |dreturn|  cached {d1:.3e}   uncached {d2:.3e}")
    assert worst < G2_TOL, f"G2 FAILED at {worst:.3e}"
    P(f"  G2 PASS ({worst:.3e} < {G2_TOL:.0e})")

    # ---------------------------------------------------------------- G3 cash-only book
    P("")
    P("=" * 118)
    P("G3  CREDIT GATE - a ZERO-WEIGHT book earns exactly the credit, every day, at every c")
    P("=" * 118)
    pxB, trB = panels["B136"]
    zero = pd.DataFrame(0.0, index=pxB.index, columns=pxB.columns)
    worst3 = 0.0
    for c in CASHGRID:
        rr = fast_backtest(pxB, zero, COST, "W", c, PRE["B136"])["returns"]
        d = float((rr - c / 1e4 / DAYS).abs().max())
        worst3 = max(worst3, d)
        P(f"  c={c:5.0f} bps   max |r_t - c/1e4/252| {d:.3e}   realised CAGR "
          f"{metrics(rr)['CAGR']:.4%}  (compounded target {(1+c/1e4/DAYS)**DAYS-1:.4%})")
    assert worst3 < G3_TOL, f"G3 FAILED at {worst3:.3e}"
    P(f"  G3 PASS ({worst3:.3e} < {G3_TOL:.0e})")

    # ---------------------------------------------------------------- G4 no-cash-leg
    P("")
    P("=" * 118)
    P("G4  NO-CASH-LEG GATE - EWall at g = 1.00 is fully invested after warm-up, so it must be")
    P("    INVARIANT in c over the scored sample (any difference is a leak in the accounting)")
    P("=" * 118)
    worst4 = 0.0
    for nm, (px, tr) in panels.items():
        st = ref[nm]["start"]
        w = form_weights("EWall", px, tr, 1.00, key=nm)
        base = fast_backtest(px, w, COST, "W", 0.0, PRE[nm])["returns"].loc[st:]
        for c in CASHGRID[1:]:
            d = float((fast_backtest(px, w, COST, "W", c, PRE[nm])["returns"].loc[st:]
                       - base).abs().max())
            worst4 = max(worst4, d)
            P(f"  {nm:9s} c={c:5.0f} bps   max |dreturn vs c=0| {d:.3e}")
    assert worst4 < G4_TOL, f"G4 FAILED at {worst4:.3e}"
    P(f"  G4 PASS ({worst4:.3e} < {G4_TOL:.0e})")

    # ================================================================= PART A - the ladder
    P("")
    P("=" * 118)
    P("PART A  THE CASH-CREDITED g-LADDER")
    P("=" * 118)
    grid = []
    for nm, (px, tr) in panels.items():
        st, spy = ref[nm]["start"], ref[nm]["spy"]
        for form in FORMS:
            for freq in CADENCE:
                for g in GGRID:
                    w = form_weights(form, px, tr, g, key=nm)
                    for c in CASHGRID:
                        rf = c / 1e4
                        res = fast_backtest(px, w, COST, freq, c, PRE[nm])
                        r = res["returns"].loc[st:]
                        row = dict(panel=nm, form=form, cadence=freq, gross=g, cash_bps=c)
                        row.update(rowify(r, res["turnover"].loc[st:], rf=rf))
                        lg = legs_4b(r, spy)
                        row.update({f"L_{k}": v for k, v in lg.items()})
                        row["fail4b"] = fail_str(lg)
                        row["keep4b"] = row["fail4b"] == "-"
                        lx = legs_4b(r, spy, rf=rf)
                        row.update({f"X_{k}": v for k, v in lx.items()})
                        row["fail4b_x"] = fail_str(lx)
                        row["keep4b_x"] = row["fail4b_x"] == "-"
                        row["keep4a_c0"] = keep_4a(r, ref[nm]["v2"][0.0])
                        row["keep4a_cmatched"] = keep_4a(r, ref[nm]["v2"][c])
                        lgi = legs_4b(r.loc[:IS_END], spy.loc[:IS_END], sub=True)
                        row.update({f"ISL_{k}": v for k, v in lgi.items()})
                        row["IS_keep4b"] = all(lgi.values())
                        lgo = legs_4b(r.loc[OOS_START:], spy.loc[OOS_START:], sub=True)
                        row.update({f"OOSL_{k}": v for k, v in lgo.items()})
                        row["OOS_keep4b"] = all(lgo.values())
                        grid.append(row)
        P(f"  {nm:9s} done  ({time.time()-t0:.0f}s)")
    G = pd.DataFrame(grid)
    P(f"  {len(G)} books on the ladder ({len(G)//len(CASHGRID)} per cash rate)")

    # ------------------------------------------------------------------- H_FLAT / H_SIGN
    P("")
    P("=" * 118)
    P("H_FLAT / H_SIGN  - Sharpe's OLS slope in g at each cash rate (ALL 36 cells x 3 rates)")
    P("=" * 118)
    lin = []
    for (pnl, form, cad, c), d in G.groupby(["panel", "form", "cadence", "cash_bps"]):
        d = d.sort_values("gross")
        _, bs, r2s = ols(d.gross, d.Sharpe)
        _, bx, r2x = ols(d.gross, d.Sharpe_x)
        _, bc, r2c = ols(d.gross, d.CAGR)
        _, bd, r2d = ols(d.gross, d.MaxDD)
        lin.append(dict(panel=pnl, form=form, cadence=cad, cash_bps=c,
                        slope_Sharpe=bs, r2_Sharpe=r2s, slope_Sharpe_x=bx, r2_Sharpe_x=r2x,
                        slope_CAGR=bc, r2_CAGR=r2c, slope_MaxDD=bd, r2_MaxDD=r2d,
                        Sharpe_span=float(d.Sharpe.max() - d.Sharpe.min()),
                        Sharpe_x_span=float(d.Sharpe_x.max() - d.Sharpe_x.min())))
    LIN = pd.DataFrame(lin)
    piv = LIN.pivot_table(index=["panel", "form", "cadence"], columns="cash_bps", values="slope_Sharpe")
    pivx = LIN.pivot_table(index=["panel", "form", "cadence"], columns="cash_bps", values="slope_Sharpe_x")
    spn = LIN.pivot_table(index=["panel", "form", "cadence"], columns="cash_bps", values="Sharpe_span")
    P("  " + f"{'panel':10s} {'form':7s} {'cad':4s}" +
      "".join(f"{'slope@' + str(int(c)):>11s}" for c in CASHGRID) +
      f"{'c* bps':>9s}" + "".join(f"{'xslope@' + str(int(c)):>12s}" for c in CASHGRID))
    cstars = []
    for k in piv.index:
        row, rowx = piv.loc[k], pivx.loc[k]
        s0, s3 = float(row[CASHGRID[0]]), float(row[CASHGRID[-1]])
        cstar = np.nan if s0 == s3 else CASHGRID[0] + (0.0 - s0) * (CASHGRID[-1] - CASHGRID[0]) / (s3 - s0)
        cstars.append(dict(panel=k[0], form=k[1], cadence=k[2], cstar=cstar,
                           slope0=s0, slope300=s3,
                           xslope0=float(rowx[CASHGRID[0]]), xslope300=float(rowx[CASHGRID[-1]]),
                           span0=float(spn.loc[k, CASHGRID[0]]), span300=float(spn.loc[k, CASHGRID[-1]])))
        P("  " + f"{k[0]:10s} {k[1]:7s} {k[2]:4s}" +
          "".join(f"{float(row[c]):+11.5f}" for c in CASHGRID) + f"{cstar:9.1f}" +
          "".join(f"{float(rowx[c]):+12.5f}" for c in CASHGRID))
    CST = pd.DataFrame(cstars)
    med = {c: float(LIN[LIN.cash_bps == c].slope_Sharpe.median()) for c in CASHGRID}
    amed = {c: float(LIN[LIN.cash_bps == c].slope_Sharpe.abs().median()) for c in CASHGRID}
    ncell = int((LIN.cash_bps == 0).sum())
    P("")
    P("  median slope   " + "   ".join(f"c={int(c)}: {med[c]:+.5f}" for c in CASHGRID))
    P("  median |slope| " + "   ".join(f"c={int(c)}: {amed[c]:.5f}" for c in CASHGRID))
    h_flat = bool(amed[CASHGRID[2]] < amed[CASHGRID[1]] < amed[CASHGRID[0]])
    neg3 = int((LIN[LIN.cash_bps == CASHGRID[-1]].slope_Sharpe < 0).sum())
    pos0 = int((LIN[LIN.cash_bps == CASHGRID[0]].slope_Sharpe > 0).sum())
    h_sign = bool(neg3 > ncell / 2)
    P(f"  slope POSITIVE at c=0 in {pos0}/{ncell} cells;  NEGATIVE at c=300 in {neg3}/{ncell}")
    P(f"  Sharpe span across the 17 grosses: median {float(LIN[LIN.cash_bps==0].Sharpe_span.median()):.5f} "
      f"at c=0 vs {float(LIN[LIN.cash_bps==CASHGRID[-1]].Sharpe_span.median()):.5f} at c=300 "
      f"(idea 51's invariance bar was {INVAR_BAR})")
    ins = int(CST.cstar.between(0, 300).sum())
    P(f"  implied break-even rate c* (slope = 0, linear in c): median {CST.cstar.median():.1f} bps, "
      f"IQR [{CST.cstar.quantile(.25):.1f}, {CST.cstar.quantile(.75):.1f}], {ins}/{len(CST)} inside [0, 300]")
    P(f"  H_FLAT {'PASS' if h_flat else 'FAIL'}   (median |slope| strictly shrinking in c)")
    P(f"  H_SIGN {'PASS' if h_sign else 'FAIL'}   (slope negative in a majority of cells at 300 bps)")

    # ------------------------------------------------------------------- H_EXCESS
    P("")
    P("=" * 118)
    P("H_EXCESS  - the same slope with Sharpe's own risk-free rate set to c (book AND SPY)")
    P("=" * 118)
    dx = {c: (pivx[c] - pivx[CASHGRID[0]]).abs() for c in CASHGRID[1:]}
    inv_all = 0
    for c in CASHGRID[1:]:
        n_in = int((dx[c] <= INVAR_BAR).sum())
        inv_all += n_in
        P(f"  c={int(c):3d} bps: |xslope(c) - xslope(0)| median {float(dx[c].median()):.5f}, "
          f"max {float(dx[c].max()):.5f};  within idea 51's {INVAR_BAR} bar in {n_in}/{len(dx[c])} cells")
    h_excess = bool(inv_all > len(CASHGRID[1:]) * ncell / 2)
    xmed = {c: float(LIN[LIN.cash_bps == c].slope_Sharpe_x.median()) for c in CASHGRID}
    P(f"  median EXCESS slope  " + "   ".join(f"c={int(c)}: {xmed[c]:+.5f}" for c in CASHGRID))
    P(f"  H_EXCESS {'PASS' if h_excess else 'FAIL'}   (excess-Sharpe slope invariant in c in a majority)")

    # ------------------------------------------------------------------- the bands
    P("")
    P("=" * 118)
    P("PART B  THE ADMISSIBLE 4b g-BAND AT EACH CASH RATE  (native legs; excess legs in .bands.csv)")
    P("=" * 118)
    bands = []
    for (pnl, form, cad, c), d in G.groupby(["panel", "form", "cadence", "cash_bps"]):
        d = d.sort_values("gross")
        lo, hi, w, npt, iv, why = band_from(d)
        lo2, hi2, w2, npt2, _, _ = band_from(d, legcols=("L_DD", "L_CAGR"))
        _, _, _, npt3, _, _ = band_from(d, legcols=("L_H1", "L_H2", "L_OOS"))
        lox, hix, wx, nptx, ivx, whyx = band_from(d, legcols=tuple(f"X_{k}" for k in LEGS))
        bands.append(dict(panel=pnl, form=form, cadence=cad, cash_bps=c, lo=lo, hi=hi, width=w,
                          n_pts=npt, interval=iv, empty_reason=why, scale_lo=lo2, scale_hi=hi2,
                          scale_width=w2, scale_pts=npt2, sharpe_pts=npt3,
                          x_lo=lox, x_hi=hix, x_width=wx, x_pts=nptx, x_interval=ivx,
                          x_empty_reason=whyx))
    B = pd.DataFrame(bands)
    bw = B.pivot_table(index=["panel", "form", "cadence"], columns="cash_bps", values="width")
    bp = B.pivot_table(index=["panel", "form", "cadence"], columns="cash_bps", values="n_pts")
    blo = B.pivot_table(index=["panel", "form", "cadence"], columns="cash_bps", values="lo")
    bhi = B.pivot_table(index=["panel", "form", "cadence"], columns="cash_bps", values="hi")
    xw = B.pivot_table(index=["panel", "form", "cadence"], columns="cash_bps", values="x_width")
    P("  " + f"{'panel':10s} {'form':7s} {'cad':4s}" +
      "".join(f"{'band@' + str(int(c)):>16s}" for c in CASHGRID) +
      f"{'dwidth':>8s}{'x-dwidth':>10s}")
    for k in bw.index:
        cells = [f"[{blo.loc[k, c]:.2f},{bhi.loc[k, c]:.2f}]" if bp.loc[k, c] else "EMPTY"
                 for c in CASHGRID]
        P("  " + f"{k[0]:10s} {k[1]:7s} {k[2]:4s}" + "".join(f"{x:>16s}" for x in cells) +
          f"{float(bw.loc[k, CASHGRID[-1]] - bw.loc[k, CASHGRID[0]]):+8.2f}"
          f"{float(xw.loc[k, CASHGRID[-1]] - xw.loc[k, CASHGRID[0]]):+10.2f}")
    wider = int((bw[CASHGRID[-1]] > bw[CASHGRID[0]] + 1e-12).sum())
    same = int((np.abs(bw[CASHGRID[-1]] - bw[CASHGRID[0]]) <= 1e-12).sum())
    narrow = int((bw[CASHGRID[-1]] < bw[CASHGRID[0]] - 1e-12).sum())
    h_widen = bool(wider + same > len(bw) / 2 and wider >= narrow)
    P("")
    P(f"  band width 0 -> 300 bps:  WIDER {wider}   SAME {same}   NARROWER {narrow}  of {len(bw)} cells")
    xwider = int((xw[CASHGRID[-1]] > xw[CASHGRID[0]] + 1e-12).sum())
    xsame = int((np.abs(xw[CASHGRID[-1]] - xw[CASHGRID[0]]) <= 1e-12).sum())
    P(f"  same, EXCESS legs:        WIDER {xwider}   SAME {xsame}   "
      f"NARROWER {len(xw)-xwider-xsame}")
    for c in CASHGRID:
        sub = B[B.cash_bps == c]
        ne = sub[sub.n_pts > 0]
        P(f"  c={int(c):3d} bps: non-empty {len(ne)}/{len(sub)}  contiguous {int(ne.interval.sum())}/{max(len(ne),1)}"
          f"  median width {(ne.width.median() if len(ne) else float('nan')):.2f}"
          f"  EMPTY by SHARPE {int((sub.empty_reason=='SHARPE').sum())} / by SCALE "
          f"{int((sub.empty_reason=='SCALE').sum())}   (excess-leg non-empty {int((sub.x_pts>0).sum())})")
    P(f"  H_WIDEN {'PASS' if h_widen else 'FAIL'}   (weakly wider in a majority, and more widen than narrow)")

    # ------------------------------------------------------------------- H_ORDER
    P("")
    P("=" * 118)
    P("H_ORDER  - does the U56 / B136 ordering of median band width survive the credit?")
    P("=" * 118)
    orders = []
    P("  " + f"{'c (bps)':>8s}" + "".join(f"{p:>12s}" for p in ("U56", "B136", SMALLK)) +
      f"{'U56 vs B136':>14s}{'U56 vs B136 (excess)':>23s}")
    for c in CASHGRID:
        sub = B[B.cash_bps == c]
        meds = {p: float(sub[sub.panel == p].width.median()) for p in ("U56", "B136", SMALLK)}
        xmeds = {p: float(sub[sub.panel == p].x_width.median()) for p in ("U56", "B136", SMALLK)}
        rel = ">" if meds["U56"] > meds["B136"] else ("<" if meds["U56"] < meds["B136"] else "=")
        xrel = ">" if xmeds["U56"] > xmeds["B136"] else ("<" if xmeds["U56"] < xmeds["B136"] else "=")
        orders.append(dict(cash_bps=c, **{f"med_{k}": v for k, v in meds.items()},
                           **{f"xmed_{k}": v for k, v in xmeds.items()},
                           U56_vs_B136=rel, U56_vs_B136_excess=xrel))
        P("  " + f"{int(c):8d}" + "".join(f"{meds[p]:12.3f}" for p in ("U56", "B136", SMALLK)) +
          f"{rel:>14s}{xrel:>23s}")
    ORD = pd.DataFrame(orders)
    h_order = bool(ORD.U56_vs_B136.nunique() == 1)
    P(f"  H_ORDER {'PASS' if h_order else 'FAIL'}   (same U56-vs-B136 sign at all three rates)")

    # ------------------------------------------------------------------- discrimination
    disc = []
    for (pnl, cad, c), d in B.groupby(["panel", "cadence", "cash_bps"]):
        d = d.set_index("form")
        ctl, tre = d.loc[CONTROL], d.drop(index=CONTROL)
        disc.append(dict(panel=pnl, cadence=cad, cash_bps=c, ctl_width=float(ctl.width),
                         ctl_pts=int(ctl.n_pts), med_treat_width=float(tre.width.median()),
                         best_treat_width=float(tre.width.max()),
                         n_treat_nonempty=int((tre.n_pts > 0).sum()),
                         ctl_ge_median=bool(ctl.n_pts > 0 and ctl.width >= tre.width.median())))
    D = pd.DataFrame(disc)
    P("")
    P("  idea 311's H_NODISC re-read at each c - ungated control band >= median treatment in " +
      ", ".join(f"c={int(c)}: {int(D[D.cash_bps==c].ctl_ge_median.sum())}/{len(D[D.cash_bps==c])}"
                for c in CASHGRID))

    # ------------------------------------------------------------------- KEEP paths
    P("")
    P("=" * 118)
    P("PART C  BOTH KEEP PATHS over all %d books" % len(G))
    P("=" * 118)
    P("  " + f"{'c (bps)':>8s}{'4a (v2 @0%)':>13s}{'4a (v2 @c)':>12s}{'4b':>8s}{'4b excess':>11s}"
      f"{'BOTH':>7s}{'n':>7s}")
    kp = []
    for c in CASHGRID:
        s = G[G.cash_bps == c]
        both = int((s.keep4a_cmatched & s.keep4b).sum())
        kp.append(dict(cash_bps=c, keep4a_c0=int(s.keep4a_c0.sum()),
                       keep4a_cmatched=int(s.keep4a_cmatched.sum()), keep4b=int(s.keep4b.sum()),
                       keep4b_x=int(s.keep4b_x.sum()), both=both, n=len(s)))
        P("  " + f"{int(c):8d}{int(s.keep4a_c0.sum()):13d}{int(s.keep4a_cmatched.sum()):12d}"
          f"{int(s.keep4b.sum()):8d}{int(s.keep4b_x.sum()):11d}{both:7d}{len(s):7d}")
    KP = pd.DataFrame(kp)
    h_keep = bool(KP.both.sum() == 0)
    P(f"  H_KEEP {'PASS' if h_keep else 'FAIL'}   (no book passes BOTH paths at any c)")
    P("  most common 4b fail sets: " +
      ", ".join(f"{k}:{v}" for k, v in G.fail4b.value_counts().head(6).items()))

    # ------------------------------------------------------------------- RULE 8
    P("")
    P("=" * 118)
    P("RULE 8 WALK-FORWARD   band solved on IS <= %s, OOS >= %s read ONCE, at each cash rate"
      % (IS_END, OOS_START))
    P("=" * 118)
    wf = []
    P("  WF-A  IS band vs OOS band per (panel, form, cadence, c)")
    P("  " + f"{'panel':10s} {'form':7s} {'cad':4s} {'c':>5s} {'IS band':>15s} {'g*':>6s} "
        f"{'OOS band':>15s} {'g* in OOS':>10s}")
    for (pnl, form, cad, c), d in G.groupby(["panel", "form", "cadence", "cash_bps"]):
        d = d.sort_values("gross")
        lo_i, hi_i, _, n_i, _, _ = band_from(d, legcols=tuple(f"ISL_{k}" for k in LEGS))
        lo_o, hi_o, _, n_o, _, _ = band_from(d, legcols=tuple(f"OOSL_{k}" for k in LEGS))
        gstar = np.nan if n_i == 0 else round(((lo_i + hi_i) / 2) / 0.05) * 0.05
        inside = bool(n_o > 0 and not np.isnan(gstar) and lo_o - 1e-9 <= gstar <= hi_o + 1e-9)
        wf.append(dict(leg="WF-A", panel=pnl, form=form, cadence=cad, cash_bps=c, IS_lo=lo_i,
                       IS_hi=hi_i, IS_pts=n_i, gstar=gstar, OOS_lo=lo_o, OOS_hi=hi_o,
                       OOS_pts=n_o, gstar_in_OOS=inside))
        bs = f"[{lo_i:.2f}, {hi_i:.2f}]" if n_i else "EMPTY"
        os_ = f"[{lo_o:.2f}, {hi_o:.2f}]" if n_o else "EMPTY"
        P("  " + f"{pnl:10s} {form:7s} {cad:4s} {int(c):5d} {bs:>15s} "
            f"{('%.2f' % gstar) if n_i else '   -':>6s} {os_:>15s} {str(inside):>10s}")
    WFA = pd.DataFrame(wf)
    for c in CASHGRID:
        s = WFA[(WFA.cash_bps == c) & (WFA.IS_pts > 0)]
        P(f"  c={int(c):3d} bps: non-empty IS band in {len(s)}/{len(WFA[WFA.cash_bps==c])} cells; "
          f"IS midpoint g* inside the OOS band in {int(s.gstar_in_OOS.sum())}/{max(len(s),1)}")

    P("")
    P("  WF-B  a BOOK per cash rate: form by IS Sharpe, g = IS band midpoint, B136 / weekly,")
    P("        OOS read once.  Baseline shown at the committed 0% convention AND credited at c.")
    wfb = []
    stB = ref["B136"]["start"]
    spyb = ref["B136"]["spy"]
    for c in CASHGRID:
        selb = G[(G.panel == "B136") & (G.cadence == "W") & (G.cash_bps == c)]
        ist = selb.groupby("form").IS_Sharpe.mean().sort_values(ascending=False)
        pick_form = str(ist.index[0])
        prow = WFA[(WFA.panel == "B136") & (WFA.form == pick_form) & (WFA.cadence == "W")
                   & (WFA.cash_bps == c)].iloc[0]
        pick_g = float(prow.gstar) if prow.IS_pts > 0 else 0.75
        note = "" if prow.IS_pts > 0 else "  (EMPTY IS band -> g defaults to 0.75)"
        P("")
        P(f"  c={int(c)} bps   IS-Sharpe ranking: " + "  ".join(f"{k} {v:+.3f}" for k, v in ist.items()))
        P(f"  PICK (IS only): form {pick_form}, g {pick_g:.2f}{note}")
        rp = fast_backtest(pxB, form_weights(pick_form, pxB, trB, pick_g, key="B136"),
                           COST, "W", c, PRE["B136"])["returns"].loc[stB:]
        books = [(f"WF-B {pick_form} g={pick_g:.2f} c={int(c)}", rp),
                 ("RULES v2 (cash 0%)", ref["B136"]["v2"][0.0]),
                 (f"RULES v2 (cash {int(c)}bps)", ref["B136"]["v2"][c]),
                 ("SPY", spyb)]
        P("  " + f"{'book':30s} {'CAGR':>8s} {'Sharpe':>8s} {'MaxDD':>8s} {'H1':>7s} {'H2':>7s} "
            f"{'OOS_CAGR':>9s} {'OOS_Sh':>8s} {'OOS_DD':>8s}")
        for nm2, r in books:
            d = rowify(r, rf=c / 1e4)
            wfb.append(dict(leg="WF-B", cash_bps=c, book=nm2, pick_form=pick_form,
                            pick_gross=pick_g, **d))
            P("  " + f"{nm2:30s} {d['CAGR']:8.2%} {d['Sharpe']:8.3f} {d['MaxDD']:8.2%} "
                f"{d['H1']:7.3f} {d['H2']:7.3f} {d['OOS_CAGR']:9.2%} {d['OOS_Sharpe']:8.3f} "
                f"{d['OOS_MaxDD']:8.2%}")
        lgf = legs_4b(rp, spyb)
        lgo = legs_4b(rp.loc[OOS_START:], spyb.loc[OOS_START:], sub=True)
        lgx = legs_4b(rp, spyb, rf=c / 1e4)
        P(f"  4a vs RULES v2 @0%: {keep_4a(rp, ref['B136']['v2'][0.0])}   "
          f"4a vs RULES v2 @{int(c)}bps: {keep_4a(rp, ref['B136']['v2'][c])}   "
          f"4b fail (full): {fail_str(lgf)}   4b fail (OOS window): {fail_str(lgo)}   "
          f"4b fail (excess): {fail_str(lgx)}")
    WFB = pd.DataFrame(wfb)

    # ------------------------------------------------------------------- verdict
    P("")
    P("=" * 118)
    P("VERDICT")
    P("=" * 118)
    P(f"  H_FLAT {'PASS' if h_flat else 'FAIL'}   H_SIGN {'PASS' if h_sign else 'FAIL'}   "
      f"H_WIDEN {'PASS' if h_widen else 'FAIL'}   H_ORDER {'PASS' if h_order else 'FAIL'}   "
      f"H_KEEP {'PASS' if h_keep else 'FAIL'}   H_EXCESS {'PASS' if h_excess else 'FAIL'}")
    P("  KEEP path 4a: %d / %d books;  4b: %d / %d;  BOTH: %d.  No book promoted; RULES.md, "
      "PROTOCOL.md, scan.py, bot.py and baseline.py untouched."
      % (int(KP.keep4a_cmatched.sum()), len(G), int(KP.keep4b.sum()), len(G), int(KP.both.sum())))

    for nm2, df in (("grid", G), ("slopes", LIN), ("bands", B), ("order", ORD),
                    ("discrimination", D), ("keeppaths", KP), ("cstar", CST),
                    ("walkforward", pd.concat([WFA, WFB], ignore_index=True))):
        df.to_csv(OUT / f"{STAMP}.{nm2}.csv", index=False)
    P(f"  wrote {STAMP}.{{grid,slopes,bands,order,discrimination,keeppaths,cstar,walkforward}}.csv "
      f"({time.time()-t0:.0f}s)")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()

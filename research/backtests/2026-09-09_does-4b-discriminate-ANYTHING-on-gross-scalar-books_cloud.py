#!/usr/bin/env python3
"""Idea 311 (cloud, 2026-09-09) - does-4b-discriminate-ANYTHING-on-gross-scalar-books.

QUESTION
--------
Idea 51 solved the admissible 4b GROSS band for 30 unlevered book-forms and found it non-empty
in 20 and passing in 20/20 - the no-filter EWall control included - because Sharpe is
essentially invariant in the gross scalar g (span <= 0.0050) while CAGR and MaxDD scale
~linearly in g.  If that is right, then on any book whose only free dial is g:

    * PROTOCOL 4b's three SHARPE legs (H1 > SPY, H2 > SPY, OOS > SPY) are g-INVARIANT.  They
      are the EDGE test and they do not move when the dial moves.
    * PROTOCOL 4b's DD cap (MaxDD >= 0.60 * SPY's) and CAGR floor (CAGR >= 0.70 * SPY's) are
      the only legs g touches, and they move in OPPOSITE directions in g.  They therefore
      define an interval [g_lo, g_hi] - an admissible BAND, not a point.

So a 4b verdict quoted at one ladder point of g is a DIAL PLACEMENT, not a finding, whenever
the Sharpe legs already pass.  This run asks two things:

  A  THE BAND.  Sweep g finely on a pre-registered menu of unlevered book-forms x 3 panels x
     2 cadences.  Measure (i) the Sharpe span in g, (ii) how linear CAGR and MaxDD are in g,
     (iii) the admissible 4b g-band, and (iv) whether the band DISCRIMINATES - is the ungated
     EWall control's band any narrower than the gated/ranked treatments' bands on the same
     panel?  If it is not, 4b on a gross-scalar book separates nothing.

  B  THE CENSUS.  Mechanically re-read every committed research/backtests CSV that carries
     BOTH a gross column and a 4b verdict column, and classify each committed 4b PASS as
        DIAL   the same book-form at the same (panel, cadence, ...) FAILS 4b at some other
               gross the SAME file already ran - the verdict is a placement on its own ladder;
        ROBUST it passes at EVERY gross that file ran for it (>= 2 grosses);
        UNSWEPT the file ran exactly one gross for it, so the question is unanswerable there.
     This is a census of what the record has actually published, not a new backtest.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two): the book-FORM and the gross g.  Panel and
cadence are reported axes; every grid point is written to .grid.csv.

PRE-REGISTERED HYPOTHESES (written before any band was solved)
--------------------------------------------------------------
H_INVAR   : max Sharpe span across the g grid, over all (panel, form, cadence) cells, is
            <= 0.0100 (idea 51 reported <= 0.0050 on a coarser grid).  If this fails, g is
            not a pure scalar dial and the rest of the question dissolves.
H_LINEAR  : CAGR and MaxDD are ~linear in g - R^2 of an OLS in g >= 0.98 in >= 90% of cells.
H_BAND    : the admissible 4b g-band is an INTERVAL (no holes) in >= 95% of non-empty cells.
H_NODISC  : 4b does NOT discriminate on gross-scalar books - in a majority of (panel, cadence)
            cells the ungated EWall control's admissible band is non-empty AND at least as
            wide as the median treatment band.  PASS here answers the title NO.
H_SHARPE  : the three Sharpe legs, not the two scaling legs, are what actually decides 4b on
            these books: the share of cells whose band is EMPTY because a Sharpe leg fails at
            every g exceeds the share empty because DD and CAGR cannot be satisfied together.
H_CENSUS  : in the committed record, DIAL 4b passes outnumber ROBUST ones among swept rows.

Rule 8 (walk-forward, required): the band is solved on 2010-2016 ONLY, g is picked as that
band's midpoint (the natural selector for a dial), the form is picked by IS Sharpe, and the
2017-2026 window is read ONCE - reporting OOS CAGR/Sharpe/MaxDD against RULES v2 and SPY, and
whether the IS-chosen g is still inside the OOS band.

Costs 10 bps per unit turnover, weights at close t applied t+1 (engine convention), no
shorting, no leverage (g <= 1.00 everywhere).

SURVIVORSHIP: B136 and the small panel are CURRENT constituents (universe_broad.json is
today's list; the small panel is today's sub-$2B screen).  Small-panel tickers with
max_1d_move >= 1.0 in data/small_meta.csv are dropped FIRST, per PROTOCOL.

GATES
-----
G1  idea 312's committed grid.csv REAL rows reproduce (36 rows x 13 columns).
G2  fast_backtest == engine.backtest on a real book.
G3  the g-invariance claim is checked against the engine directly, not only the fast runner.
"""
import sys, time, csv, glob
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
CADENCE = ["W", "M"]
GGRID = [round(0.20 + 0.05 * i, 2) for i in range(17)]      # 0.20 .. 1.00, unlevered
PARENT = "2026-09-09_is-the-panel-ordering-an-ETF-SHARE-effect_B.grid.csv"
PARENT_END = "2026-09-04"
G1_TOL, G1_TOL_U56, G2_TOL = 1e-9, 1e-4, 1e-12
INVAR_BAR = 0.0100          # H_INVAR
LIN_BAR, LIN_SHARE = 0.98, 0.90
BAND_SHARE = 0.95

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


# ------------------------------------------------------------------ vectorised runner
def fast_backtest(prices, weights, cost_bps=COST, freq="W"):
    """Vectorised equivalent of engine.backtest (asserted in G2).  Idea 312/568's runner."""
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


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def rowify(r, tn=None):
    m = metrics(r)
    h1, h2 = halves(r)
    mi, mo = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    d = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
             IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
             OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])
    if tn is not None:
        d["turnover"] = float(tn.sum() / m["Years"])
    return d


def keep_4a(r, b):
    a1, a2 = halves(r)
    b1, b2 = halves(b)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(b)["MaxDD"])


def legs_4b(r, spy, sub=False):
    """The five 4b legs as booleans.

    sub=False: r and spy are the FULL sample; H1/H2 are its halves and the OOS leg is the
               post-2017 Sharpe, exactly as PROTOCOL 4b reads.
    sub=True:  r and spy are already ONE window; H1/H2 are that window's halves and the
               third Sharpe leg becomes that window's own Sharpe vs SPY's - the in-window
               restatement of 4b used to solve an IS-only and an OOS-only band.
    """
    a1, a2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    sh_r = m["Sharpe"] if sub else metrics(r.loc[OOS_START:])["Sharpe"]
    sh_s = ms["Sharpe"] if sub else metrics(spy.loc[OOS_START:])["Sharpe"]
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
        "U56": (px56.dropna(how="all").ffill().loc[:PARENT_END], set(px56.columns)),
        "B136": (px136.dropna(how="all").ffill().loc[:PARENT_END], set(px136.columns)),
        f"SMALL{len(s_stk)}": (pxs[s_stk + ["SPY"]].dropna(how="all").ffill().loc[:PARENT_END],
                               set(s_stk)),
    }


# ------------------------------------------------------------- the book-form menu
def form_weights(name, px, tradable, g):
    """PRE-REGISTERED menu of unlevered book-forms whose ONLY free dial is the gross scalar g.

    EWall   every priced tradable name, equal weight, gross g            (NO-EDGE CONTROL)
    MA-RS   200d gate, re-spread over survivors at gross g               (gate, gross held)
    MA-DG   200d gate, de-grossed: gated-out weight goes to CASH         (gate, gross floats)
    TOP20   top 20 by RULES' composite score, equal weight, gross g      (ranked)
    TOP10   top 10 by the same score                                     (ranked, concentrated)
    MA20    200d gate INTERSECT top 20 by score, re-spread at gross g    (gate + ranked)
    """
    e = _priced(px, tradable) > 0
    if name == "EWall":
        return _ew(e, g)
    ma = above_ma(px) & e
    if name == "MA-RS":
        return _ew(ma, g)
    if name == "MA-DG":
        n = e.sum(axis=1).replace(0, np.nan)
        return g * ma.astype(float).div(n, axis=0).fillna(0.0)
    s, _, _ = score(px, vol_scale=False)
    s = s.where(e)
    if name in ("TOP20", "TOP10"):
        k = 20 if name == "TOP20" else 10
        rk = s.rank(axis=1, ascending=False)
        return _ew(rk <= k, g)
    if name == "MA20":
        rk = s.where(ma).rank(axis=1, ascending=False)
        return _ew(rk <= 20, g)
    raise ValueError(name)


FORMS = ["EWall", "MA-RS", "MA-DG", "TOP20", "TOP10", "MA20"]
CONTROL = "EWall"


LEGS = ("H1", "H2", "OOS", "DD", "CAGR")
SHARPE_LEGS = ("H1", "H2", "OOS")


def band_from(sub, legcols=("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")):
    """Admissible g-band = the set of g where every named leg passes.  Returns
    (lo, hi, width, n_points, is_interval, empty_reason)."""
    ok = sub[list(legcols)].all(axis=1).values
    gs = sub["gross"].values
    if not ok.any():
        # why empty?  a leg that fails at EVERY g is a Sharpe-leg kill; otherwise the two
        # scaling legs (DD, CAGR) simply cannot be satisfied at the same g.
        always_fail = [c for c in legcols if not sub[c].any()]
        sharpe_names = {f"{p_}{k}" for k in SHARPE_LEGS for p_ in ("L_", "ISL_", "OOSL_")}
        reason = "SHARPE" if set(always_fail) & sharpe_names else (
            "SCALE" if always_fail else "SCALE")
        return (np.nan, np.nan, 0.0, 0, True, reason)
    idx = np.flatnonzero(ok)
    lo, hi = float(gs[idx[0]]), float(gs[idx[-1]])
    interval = bool(idx[-1] - idx[0] + 1 == len(idx))
    return (lo, hi, hi - lo, int(ok.sum()), interval, "-")


# ==================================================================================== run
def main():
    t0 = time.time()
    P("=" * 118)
    P("IDEA 311  does-4b-discriminate-ANYTHING-on-gross-scalar-books  (cloud, 2026-09-09)")
    P("=" * 118)
    P("A  sweep the gross scalar g finely on 6 unlevered book-forms x 3 panels x 2 cadences and")
    P("   solve PROTOCOL 4b's admissible g-BAND;  B  census the committed record's 4b passes for")
    P("   whether each one is a placement on its own file's gross ladder.")
    P(f"g grid: {GGRID[0]} .. {GGRID[-1]} step 0.05 ({len(GGRID)} points).  10 bps, t+1 fills, no leverage.")
    P("SURVIVORSHIP: B136 and the small panel are CURRENT constituents; small-panel names with")
    P("max_1d_move >= 1.0 dropped first.  Every number inherits that bias.")
    P("")

    # ---------------------------------------------------------------- G1 reproduction
    P("=" * 118)
    P("G1  REPRODUCTION GATE - idea 312's committed grid.csv REAL rows (36 rows x 13 columns)")
    P("=" * 118)
    panels = real_panels()
    SMALLK = [k for k in panels if k.startswith("SMALL")][0]
    ref, real_rows = {}, []
    for nm, (px, tr) in panels.items():
        st = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        v2 = backtest(px, rules_v2_weights(px), cost_bps=COST, freq="W")["returns"].loc[st:]
        ref[nm] = dict(start=st, spy=spy, v2=v2)
        for g in (0.50, 0.75, 1.00):
            for freq in CADENCE:
                res = {k: fast_backtest(px, form_weights(k, px, tr, g), COST, freq)
                       for k in ("EWall", "MA-RS")}
                rets = {k: v["returns"].loc[st:] for k, v in res.items()}
                mc = metrics(rets["EWall"])
                for k in ("EWall", "MA-RS"):
                    r = rets[k]
                    row = dict(panel=nm, kind="REAL", arm=k, gross=g, cadence=freq)
                    row.update(rowify(r, res[k]["turnover"].loc[st:]))
                    row["dCAGR_vs_EWall"] = row["CAGR"] - mc["CAGR"]
                    row["dSharpe_vs_EWall"] = row["Sharpe"] - mc["Sharpe"]
                    real_rows.append(row)
        P(f"  {nm:9s} {px.shape[1]:4d} cols, {len(tr):4d} tradable, sample from {st.date()}  ({time.time()-t0:.0f}s)")
    REAL = pd.DataFrame(real_rows)
    par = pd.read_csv(OUT / PARENT)
    par = par[(par.kind == "REAL") & par.arm.isin(["EWall", "MA-RS"])].copy()
    cmpcols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe", "IS_CAGR", "OOS_CAGR",
               "OOS_Sharpe", "OOS_MaxDD", "turnover", "dCAGR_vs_EWall", "dSharpe_vs_EWall"]
    m = REAL.merge(par, on=["panel", "arm", "gross", "cadence"], suffixes=("", "_p"))
    assert len(m) == 36, len(m)
    perp = m.assign(d=np.abs(m[cmpcols].values - m[[c + '_p' for c in cmpcols]].values).max(1)) \
            .groupby("panel").d.max()
    P(f"  rows matched: {len(m)}/36   per panel: " + "  ".join(f"{k} {v:.2e}" for k, v in perp.items()))
    for pnl, tol in ((SMALLK, G1_TOL), ("B136", G1_TOL), ("U56", G1_TOL_U56)):
        assert float(perp[pnl]) < tol, f"G1 FAILED on {pnl} at {perp[pnl]:.3e} (bar {tol:.0e})"
    P("  G1 PASS.  (U56 carries idea 312's documented prices.csv revision, <= 5.1e-5 relative.)")

    # ---------------------------------------------------------------- G2 identity
    P("")
    P("=" * 118)
    P("G2  IDENTITY GATE - fast_backtest vs engine.backtest")
    P("=" * 118)
    worst = 0.0
    for nm, (px, tr) in panels.items():
        w = form_weights("MA-RS", px, tr, 0.75)
        d = float((fast_backtest(px, w, COST, "W")["returns"]
                   - backtest(px, w, cost_bps=COST, freq="W")["returns"]).abs().max())
        worst = max(worst, d)
        P(f"  {nm:9s} max |dreturn| {d:.3e}")
    assert worst < G2_TOL, f"G2 FAILED at {worst:.3e}"
    P(f"  G2 PASS ({worst:.3e} < {G2_TOL:.0e})")

    # ================================================================= PART A - the band
    P("")
    P("=" * 118)
    P("PART A  THE g-LADDER   6 forms x 3 panels x 2 cadences x %d grosses = %d books"
      % (len(GGRID), len(FORMS) * 3 * len(CADENCE) * len(GGRID)))
    P("=" * 118)
    grid = []
    for nm, (px, tr) in panels.items():
        st, spy, v2 = ref[nm]["start"], ref[nm]["spy"], ref[nm]["v2"]
        for form in FORMS:
            for freq in CADENCE:
                for g in GGRID:
                    res = fast_backtest(px, form_weights(form, px, tr, g), COST, freq)
                    r = res["returns"].loc[st:]
                    row = dict(panel=nm, form=form, cadence=freq, gross=g)
                    row.update(rowify(r, res["turnover"].loc[st:]))
                    lg = legs_4b(r, spy)
                    row.update({f"L_{k}": v for k, v in lg.items()})
                    row["fail4b"] = fail_str(lg)
                    row["keep4b"] = row["fail4b"] == "-"
                    row["keep4a"] = keep_4a(r, v2)
                    # IS-only legs, for rule 8
                    lgi = legs_4b(r.loc[:IS_END], spy.loc[:IS_END], sub=True)
                    row.update({f"ISL_{k}": v for k, v in lgi.items()})
                    row["IS_keep4b"] = all(lgi.values())
                    lgo = legs_4b(r.loc[OOS_START:], spy.loc[OOS_START:], sub=True)
                    row.update({f"OOSL_{k}": v for k, v in lgo.items()})
                    row["OOS_keep4b"] = all(lgo.values())
                    grid.append(row)
        P(f"  {nm:9s} done  ({time.time()-t0:.0f}s)")
    G = pd.DataFrame(grid)
    P(f"  {len(G)} books on the ladder")

    # ------------------------------------------------------------------- H_INVAR
    P("")
    P("=" * 118)
    P("H_INVAR  - is Sharpe invariant in the gross scalar?")
    P("=" * 118)
    inv = G.groupby(["panel", "form", "cadence"]).agg(
        Sharpe_min=("Sharpe", "min"), Sharpe_max=("Sharpe", "max"),
        OOSs_min=("OOS_Sharpe", "min"), OOSs_max=("OOS_Sharpe", "max"),
        CAGR_min=("CAGR", "min"), CAGR_max=("CAGR", "max"),
        DD_min=("MaxDD", "min"), DD_max=("MaxDD", "max")).reset_index()
    inv["Sharpe_span"] = inv.Sharpe_max - inv.Sharpe_min
    inv["OOSSharpe_span"] = inv.OOSs_max - inv.OOSs_min
    inv["CAGR_span"] = inv.CAGR_max - inv.CAGR_min
    inv["DD_span"] = inv.DD_max - inv.DD_min
    P("  " + f"{'panel':10s} {'form':7s} {'cad':4s} {'Sharpe span':>12s} {'OOS Sh span':>12s} "
        f"{'CAGR span':>10s} {'MaxDD span':>11s}")
    for _, r in inv.iterrows():
        P("  " + f"{r['panel']:10s} {r['form']:7s} {r['cadence']:4s} {r['Sharpe_span']:12.5f} "
            f"{r['OOSSharpe_span']:12.5f} {r['CAGR_span']:10.2%} {r['DD_span']:11.2%}")
    max_span = float(inv.Sharpe_span.max())
    h_invar = bool(max_span <= INVAR_BAR)
    P("")
    P(f"  max Sharpe span over {len(inv)} cells and {len(GGRID)} grosses: {max_span:.5f}  "
      f"(bar {INVAR_BAR:.4f})   H_INVAR {'PASS' if h_invar else 'FAIL'}")
    P(f"  by comparison the same cells' CAGR span is up to {inv.CAGR_span.max():.2%} and "
      f"MaxDD span up to {inv.DD_span.max():.2%}")

    # ------------------------------------------------------------------- G3
    P("")
    P("=" * 118)
    P("G3  the invariance claim re-checked against engine.backtest directly (not the fast runner)")
    P("=" * 118)
    pxB, trB = panels["B136"]
    stB = ref["B136"]["start"]
    eng = []
    for g in (0.20, 0.60, 1.00):
        rr = backtest(pxB, form_weights("MA-RS", pxB, trB, g), cost_bps=COST, freq="W")["returns"].loc[stB:]
        eng.append((g, metrics(rr)["Sharpe"], metrics(rr)["CAGR"], metrics(rr)["MaxDD"]))
        P(f"    g={g:.2f}  engine Sharpe {eng[-1][1]:.5f}  CAGR {eng[-1][2]:7.2%}  MaxDD {eng[-1][3]:7.2%}")
    g3span = max(e[1] for e in eng) - min(e[1] for e in eng)
    assert g3span <= INVAR_BAR, f"G3 FAILED: engine Sharpe span {g3span:.5f}"
    P(f"  engine Sharpe span across g in (0.20, 0.60, 1.00): {g3span:.5f}  <= {INVAR_BAR:.4f}   G3 PASS")

    # ------------------------------------------------------------------- H_LINEAR
    P("")
    P("=" * 118)
    P("H_LINEAR  - do CAGR and MaxDD scale linearly in g?")
    P("=" * 118)
    lin = []
    for (pnl, form, cad), d in G.groupby(["panel", "form", "cadence"]):
        d = d.sort_values("gross")
        _, bc, r2c = ols(d.gross, d.CAGR)
        _, bd, r2d = ols(d.gross, d.MaxDD)
        _, bs, r2s = ols(d.gross, d.Sharpe)
        lin.append(dict(panel=pnl, form=form, cadence=cad, slope_CAGR=bc, r2_CAGR=r2c,
                        slope_MaxDD=bd, r2_MaxDD=r2d, slope_Sharpe=bs, r2_Sharpe=r2s))
    LIN = pd.DataFrame(lin)
    share_c = float((LIN.r2_CAGR >= LIN_BAR).mean())
    share_d = float((LIN.r2_MaxDD >= LIN_BAR).mean())
    h_linear = bool(share_c >= LIN_SHARE and share_d >= LIN_SHARE)
    P(f"  R2 of CAGR  in g >= {LIN_BAR}: {share_c:.1%} of {len(LIN)} cells "
      f"(median R2 {LIN.r2_CAGR.median():.4f}, median slope {LIN.slope_CAGR.median():+.4f}/unit g)")
    P(f"  R2 of MaxDD in g >= {LIN_BAR}: {share_d:.1%} of {len(LIN)} cells "
      f"(median R2 {LIN.r2_MaxDD.median():.4f}, median slope {LIN.slope_MaxDD.median():+.4f}/unit g)")
    P(f"  R2 of Sharpe in g (for contrast): median {LIN.r2_Sharpe.median():.4f}, "
      f"median |slope| {LIN.slope_Sharpe.abs().median():.5f}/unit g")
    P(f"  H_LINEAR {'PASS' if h_linear else 'FAIL'}  (bar: >= {LIN_SHARE:.0%} of cells on BOTH)")

    # ------------------------------------------------------------------- the bands
    P("")
    P("=" * 118)
    P("THE ADMISSIBLE 4b g-BAND  (every leg passing simultaneously)")
    P("=" * 118)
    bands = []
    for (pnl, form, cad), d in G.groupby(["panel", "form", "cadence"]):
        d = d.sort_values("gross")
        lo, hi, w, npt, iv, why = band_from(d)
        # what would the band be if ONLY the two scaling legs had to pass?
        lo2, hi2, w2, npt2, iv2, _ = band_from(d, legcols=("L_DD", "L_CAGR"))
        # and if ONLY the three Sharpe legs had to pass (g-invariant -> all or nothing)?
        _, _, _, npt3, _, _ = band_from(d, legcols=("L_H1", "L_H2", "L_OOS"))
        bands.append(dict(panel=pnl, form=form, cadence=cad, lo=lo, hi=hi, width=w,
                          n_pts=npt, interval=iv, empty_reason=why,
                          scale_lo=lo2, scale_hi=hi2, scale_width=w2, scale_pts=npt2,
                          sharpe_pts=npt3))
    B = pd.DataFrame(bands)
    P("  " + f"{'panel':10s} {'form':7s} {'cad':4s} {'4b band':>16s} {'width':>7s} {'pts':>4s} "
        f"{'DD+CAGR only':>16s} {'w':>6s} {'Sharpe legs pts':>16s} {'why empty':>10s}")
    for _, r in B.iterrows():
        bs = f"[{r['lo']:.2f}, {r['hi']:.2f}]" if r["n_pts"] else "EMPTY"
        ss = f"[{r['scale_lo']:.2f}, {r['scale_hi']:.2f}]" if r["scale_pts"] else "EMPTY"
        P("  " + f"{r['panel']:10s} {r['form']:7s} {r['cadence']:4s} {bs:>16s} {r['width']:7.2f} "
            f"{r['n_pts']:4.0f} {ss:>16s} {r['scale_width']:6.2f} {r['sharpe_pts']:16.0f} "
            f"{r['empty_reason']:>10s}")

    nonempty = B[B.n_pts > 0]
    h_band = bool(len(nonempty) == 0 or float(nonempty.interval.mean()) >= BAND_SHARE)
    P("")
    P(f"  non-empty bands: {len(nonempty)}/{len(B)}   contiguous: "
      f"{int(nonempty.interval.sum())}/{len(nonempty)}   H_BAND {'PASS' if h_band else 'FAIL'}")

    # ------------------------------------------------------------------- H_SHARPE
    empt = B[B.n_pts == 0]
    n_sh = int((empt.empty_reason == "SHARPE").sum())
    n_sc = int((empt.empty_reason == "SCALE").sum())
    h_sharpe = bool(n_sh > n_sc)
    P(f"  EMPTY bands by cause: SHARPE-leg kill {n_sh}   DD/CAGR cannot coexist {n_sc}   "
      f"H_SHARPE {'PASS' if h_sharpe else 'FAIL'}")
    P(f"  cells where all three Sharpe legs pass at every g: "
      f"{int((B.sharpe_pts == len(GGRID)).sum())}/{len(B)};  at no g: {int((B.sharpe_pts == 0).sum())}/{len(B)}"
      f"   (they are g-invariant, so it is all-or-nothing)")

    # ------------------------------------------------------------------- H_NODISC
    P("")
    P("=" * 118)
    P("H_NODISC  - does the band DISCRIMINATE the ungated control from the treatments?")
    P("=" * 118)
    disc = []
    for (pnl, cad), d in B.groupby(["panel", "cadence"]):
        d = d.set_index("form")
        ctl = d.loc[CONTROL]
        tre = d.drop(index=CONTROL)
        med = float(tre.width.median())
        best = float(tre.width.max())
        disc.append(dict(panel=pnl, cadence=cad, ctl_width=float(ctl.width),
                         ctl_pts=int(ctl.n_pts), med_treat_width=med,
                         best_treat_width=best, n_treat_nonempty=int((tre.n_pts > 0).sum()),
                         ctl_ge_median=bool(ctl.n_pts > 0 and ctl.width >= med)))
    D = pd.DataFrame(disc)
    P("  " + f"{'panel':10s} {'cad':4s} {'EWall band w':>13s} {'pts':>5s} {'median treat w':>15s} "
        f"{'best treat w':>13s} {'treat non-empty':>16s} {'control >= median':>18s}")
    for _, r in D.iterrows():
        P("  " + f"{r['panel']:10s} {r['cadence']:4s} {r['ctl_width']:13.2f} {r['ctl_pts']:5.0f} "
            f"{r['med_treat_width']:15.2f} {r['best_treat_width']:13.2f} "
            f"{r['n_treat_nonempty']:16.0f} {str(r['ctl_ge_median']):>18s}")
    h_nodisc = bool(D.ctl_ge_median.mean() > 0.5)
    P(f"  control band non-empty AND >= median treatment band in "
      f"{int(D.ctl_ge_median.sum())}/{len(D)} (panel, cadence) cells   "
      f"H_NODISC {'PASS - 4b separates nothing on gross-scalar books' if h_nodisc else 'FAIL'}")

    # ================================================================= PART B - the census
    P("")
    P("=" * 118)
    P("PART B  THE CENSUS - every committed CSV carrying BOTH a gross column and a 4b verdict")
    P("=" * 118)
    GCOLS = ["gross", "gross_scalar"]          # 'g' is excluded: too ambiguous across the record
    VCOLS = ["keep4b", "pass4b", "is4b", "p4b"]
    FCOLS = ["fail4b", "f4b", "fail_4b"]
    VERDICT = {"keep4b", "pass4b", "is4b", "p4b", "fail4b", "f4b", "fail_4b",
               "keep4a", "pass4a", "p4a", "fail4a", "verdict", "pass", "fail"}
    # A column is a METRIC (an OUTCOME, never part of a book's identity) if its name is one of
    # these or carries one of these prefixes.  Anything else - including float DIALS such as
    # level, band, lam, q - is treated as IDENTITY, which SPLITS groups and therefore biases
    # the census AGAINST the DIAL hypothesis.  The conservative direction is deliberate.
    METRIC = {"cagr", "sharpe", "maxdd", "dd", "h1", "h2", "vol", "turnover", "years",
              "sortino", "calmar", "ret", "return", "returns", "equity", "premium", "sd",
              "std", "t", "tstat", "r2", "pval", "p", "slope", "intercept", "span", "effect",
              "achieved", "mean", "median", "min", "max", "n", "count", "beta_", "alpha",
              "hitrate", "breakeven", "margin", "resid", "pred", "actual", "gap", "ratio"}
    MPREFIX = ("is_", "oos_", "oosw_", "dcagr", "dsharpe", "dmaxdd", "dis_", "doos_",
               "d_", "wf_", "prem_", "spy_", "base_", "bench_")

    def is_metric(c):
        lc = str(c).strip().lower()
        return lc in METRIC or lc.startswith(MPREFIX)

    def truthy(v):
        return str(v).strip().lower() in ("true", "1", "yes", "t")

    cen, skipped, gfiles = [], [], 0
    files = sorted(glob.glob(str(OUT / "*.csv")))
    for f in files:
        fn = Path(f).name
        if fn.startswith(STAMP):
            continue
        try:
            with open(f, newline="") as fh:
                head = next(csv.reader(fh))
        except Exception:
            continue
        hs = set(head)
        gcol = next((c for c in GCOLS if c in hs), None)
        vcol = next((c for c in VCOLS if c in hs), None)
        fcol = next((c for c in FCOLS if c in hs), None)
        if gcol is None or (vcol is None and fcol is None):
            continue
        gfiles += 1
        try:
            df = pd.read_csv(f, low_memory=False)
        except Exception as e:
            skipped.append((fn, str(e)[:60]))
            continue
        if vcol is not None:
            passed = df[vcol].map(truthy)
        else:
            passed = df[fcol].astype(str).str.strip().isin(["-", "", "nan", "none", "None"])
        idc = [c for c in df.columns
               if c != gcol and str(c).strip().lower() not in VERDICT and not is_metric(c)]
        if not idc:
            skipped.append((fn, "no identity column"))
            continue
        w = df[idc + [gcol]].copy()
        for c in idc:
            w[c] = w[c].astype(str)
        w["_pass"] = passed.values
        try:
            grp = w.groupby(idc, dropna=False, sort=False)
        except Exception as e:
            skipped.append((fn, str(e)[:60]))
            continue
        for _, d in grp:
            ng = int(d[gcol].nunique())
            npass = int(d["_pass"].sum())
            if npass == 0:
                continue
            cls = "UNSWEPT" if ng < 2 else ("ROBUST" if npass == len(d) else "DIAL")
            cen.append(dict(file=fn, n_id_cols=len(idc), n_rows=len(d), n_gross=ng,
                            n_pass=npass, cls=cls,
                            gmin=float(pd.to_numeric(d[gcol], errors="coerce").min()),
                            gmax=float(pd.to_numeric(d[gcol], errors="coerce").max())))
    CEN = pd.DataFrame(cen)
    P(f"  files scanned {len(files)};  carrying a `gross` column AND a 4b verdict {gfiles};")
    P(f"  files contributing at least one committed 4b PASS "
      f"{CEN.file.nunique() if len(CEN) else 0};  unreadable/no-identity {len(skipped)}")
    P("  identity = every column that is not `gross`, not a 4b/4a verdict and not a known")
    P("  OUTCOME name; float DIALS (level, band, lam, q, ...) count as identity, which SPLITS")
    P("  groups and biases this census AGAINST the DIAL classification on purpose.")
    if len(CEN):
        by = CEN.groupby("cls").agg(book_groups=("cls", "size"), passes=("n_pass", "sum"))
        for c in ("DIAL", "ROBUST", "UNSWEPT"):
            if c in by.index:
                P(f"    {c:8s} book-groups {int(by.loc[c,'book_groups']):6d}   "
                  f"committed 4b passes {int(by.loc[c,'passes']):7d}")
        swept = CEN[CEN.cls != "UNSWEPT"]
        if len(swept):
            nd = int((swept.cls == "DIAL").sum()); nr = int((swept.cls == "ROBUST").sum())
            pdl = int(swept[swept.cls == "DIAL"].n_pass.sum())
            prb = int(swept[swept.cls == "ROBUST"].n_pass.sum())
            h_census = bool(nd > nr)
            P(f"  among SWEPT book-groups (>= 2 grosses): DIAL {nd} ({nd/(nd+nr):.1%})  "
              f"ROBUST {nr} ({nr/(nd+nr):.1%})")
            P(f"  among SWEPT committed 4b passes: DIAL {pdl} ({pdl/max(pdl+prb,1):.1%})  "
              f"ROBUST {prb} ({prb/max(pdl+prb,1):.1%})")
            P(f"  UNSWEPT (one gross only, unanswerable in-file): "
              f"{int((CEN.cls=='UNSWEPT').sum())} groups / "
              f"{int(CEN[CEN.cls=='UNSWEPT'].n_pass.sum())} passes")
            P(f"  H_CENSUS {'PASS' if h_census else 'FAIL'}  (DIAL book-groups outnumber ROBUST)")
        else:
            h_census = None
            P("  no swept book-groups found.")
        top = CEN[CEN.cls == "DIAL"].groupby("file").n_pass.sum().sort_values(ascending=False).head(8)
        if len(top):
            P("  files contributing the most DIAL passes:")
            for k, v in top.items():
                P(f"    {k[:92]:92s} {int(v):6d}")
    else:
        h_census = None
        P("  NO committed file carries both a gross column and a 4b verdict.")

    # ------------------------------------------------------------------- RULE 8
    P("")
    P("=" * 118)
    P("RULE 8 WALK-FORWARD   band solved on IS <= %s, OOS >= %s read ONCE" % (IS_END, OOS_START))
    P("=" * 118)
    wf = []
    P("  WF-A  IS band vs OOS band, per (panel, form, cadence)")
    P("  " + f"{'panel':10s} {'form':7s} {'cad':4s} {'IS band':>15s} {'g* (mid)':>9s} "
        f"{'OOS band':>15s} {'g* in OOS band':>15s}")
    for (pnl, form, cad), d in G.groupby(["panel", "form", "cadence"]):
        d = d.sort_values("gross")
        lo_i, hi_i, w_i, n_i, _, _ = band_from(d, legcols=tuple(f"ISL_{k}" for k in LEGS))
        lo_o, hi_o, w_o, n_o, _, _ = band_from(d, legcols=tuple(f"OOSL_{k}" for k in LEGS))
        gstar = np.nan if n_i == 0 else round(((lo_i + hi_i) / 2) / 0.05) * 0.05
        inside = bool(n_o > 0 and not np.isnan(gstar) and lo_o - 1e-9 <= gstar <= hi_o + 1e-9)
        wf.append(dict(leg="WF-A", panel=pnl, form=form, cadence=cad, IS_lo=lo_i, IS_hi=hi_i,
                       IS_pts=n_i, gstar=gstar, OOS_lo=lo_o, OOS_hi=hi_o, OOS_pts=n_o,
                       gstar_in_OOS=inside))
        bs = f"[{lo_i:.2f}, {hi_i:.2f}]" if n_i else "EMPTY"
        os_ = f"[{lo_o:.2f}, {hi_o:.2f}]" if n_o else "EMPTY"
        P("  " + f"{pnl:10s} {form:7s} {cad:4s} {bs:>15s} "
            f"{('%.2f' % gstar) if n_i else '   -':>9s} {os_:>15s} {str(inside):>15s}")
    WFA = pd.DataFrame(wf)
    both = WFA[(WFA.IS_pts > 0)]
    P(f"  cells with a non-empty IS band: {len(both)}/{len(WFA)};  of those, the IS midpoint g* "
      f"is inside the OOS band in {int(both.gstar_in_OOS.sum())}/{len(both)}")

    P("")
    P("  WF-B  a BOOK: form picked by IS Sharpe (g-invariant), g picked as the IS band midpoint,")
    P("        panel B136, cadence W;  OOS read once.")
    selb = G[(G.panel == "B136") & (G.cadence == "W")]
    ist = selb.groupby("form").IS_Sharpe.mean().sort_values(ascending=False)
    for k, v in ist.items():
        oo = selb[selb.form == k].OOS_Sharpe.mean()
        P(f"    {k:7s} IS Sharpe {v:+.4f}   (OOS {oo:+.4f})")
    pick_form = str(ist.index[0])
    prow = WFA[(WFA.panel == "B136") & (WFA.form == pick_form) & (WFA.cadence == "W")].iloc[0]
    pick_g = float(prow.gstar) if prow.IS_pts > 0 else 0.75
    if prow.IS_pts == 0:
        P(f"    NOTE: {pick_form} has an EMPTY IS 4b band, so no midpoint exists; g defaults to 0.75.")
    P(f"    PICK (IS only): form {pick_form}, g {pick_g:.2f}")

    pxB, trB = panels["B136"]
    stB = ref["B136"]["start"]
    rp = fast_backtest(pxB, form_weights(pick_form, pxB, trB, pick_g), COST, "W")["returns"].loc[stB:]
    v2b = ref["B136"]["v2"]
    spyb = ref["B136"]["spy"]
    P("")
    P("  " + f"{'book':28s} {'CAGR':>8s} {'Sharpe':>8s} {'MaxDD':>8s} {'H1':>7s} {'H2':>7s} "
        f"{'OOS_CAGR':>9s} {'OOS_Sh':>8s} {'OOS_DD':>8s}")
    wfb = []
    for nm2, r in ((f"WF-B {pick_form} g={pick_g:.2f}", rp), ("RULES v2 (B136)", v2b), ("SPY", spyb)):
        d = rowify(r)
        wfb.append(dict(leg="WF-B", book=nm2, **d))
        P("  " + f"{nm2:28s} {d['CAGR']:8.2%} {d['Sharpe']:8.3f} {d['MaxDD']:8.2%} {d['H1']:7.3f} "
            f"{d['H2']:7.3f} {d['OOS_CAGR']:9.2%} {d['OOS_Sharpe']:8.3f} {d['OOS_MaxDD']:8.2%}")
    lgf = legs_4b(rp, spyb)
    P(f"  WF-B 4a vs RULES v2 (B136): {keep_4a(rp, v2b)}    4b fail legs vs SPY (full): {fail_str(lgf)}")
    lgo = legs_4b(rp.loc[OOS_START:], spyb.loc[OOS_START:], sub=True)
    P(f"  WF-B 4b fail legs in the OOS window alone: {fail_str(lgo)}")

    # ------------------------------------------------------------------- KEEP paths
    P("")
    P("=" * 118)
    P("KEEP PATHS over every book on the ladder (4a vs RULES v2 on the SAME panel, 4b vs SPY)")
    P("=" * 118)
    P(f"  books: {len(G)}")
    P(f"  4a passes {int(G.keep4a.sum())}/{len(G)}   4b passes {int(G.keep4b.sum())}/{len(G)}   "
      f"BOTH {int((G.keep4a & G.keep4b).sum())}/{len(G)}")
    legs = pd.Series([x for s in G.loc[~G.keep4b, "fail4b"] for x in s.split(",")]).value_counts()
    P("  binding 4b legs: " + "  ".join(f"{k} {v}" for k, v in legs.items()))
    if int(G.keep4b.sum()):
        P("  4b passers by form:  " + "  ".join(f"{k} {v}" for k, v in G[G.keep4b].form.value_counts().items()))
        P("  4b passers by panel: " + "  ".join(f"{k} {v}" for k, v in G[G.keep4b].panel.value_counts().items()))
        bb = G[G.keep4b].sort_values("Sharpe", ascending=False).head(5)
        for _, r in bb.iterrows():
            P(f"    {r['panel']:10s} {r['form']:7s} {r['cadence']} g={r['gross']:.2f}  "
              f"CAGR {r['CAGR']:6.2%}  Sh {r['Sharpe']:.3f}  DD {r['MaxDD']:7.2%}  "
              f"H1/H2 {r['H1']:.2f}/{r['H2']:.2f}  OOS {r['OOS_Sharpe']:.3f}  4a {r['keep4a']}")
    if int((G.keep4a & G.keep4b).sum()):
        P("  BOTH-path books:")
        for _, r in G[G.keep4a & G.keep4b].iterrows():
            P(f"    {r['panel']:10s} {r['form']:7s} {r['cadence']} g={r['gross']:.2f}  "
              f"CAGR {r['CAGR']:6.2%}  Sh {r['Sharpe']:.3f}  DD {r['MaxDD']:7.2%}  OOS {r['OOS_Sharpe']:.3f}")

    # ------------------------------------------------------------------- verdict
    P("")
    P("=" * 118)
    P("VERDICT")
    P("=" * 118)
    P(f"  H_INVAR  {'PASS' if h_invar else 'FAIL'}   H_LINEAR {'PASS' if h_linear else 'FAIL'}   "
      f"H_BAND {'PASS' if h_band else 'FAIL'}   H_SHARPE {'PASS' if h_sharpe else 'FAIL'}   "
      f"H_NODISC {'PASS' if h_nodisc else 'FAIL'}   "
      f"H_CENSUS {'PASS' if h_census else ('FAIL' if h_census is False else 'N/A')}")

    # ------------------------------------------------------------------- outputs
    G.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    B.merge(LIN, on=["panel", "form", "cadence"]).merge(inv, on=["panel", "form", "cadence"]) \
        .to_csv(OUT / f"{STAMP}.bands.csv", index=False)
    D.to_csv(OUT / f"{STAMP}.discrimination.csv", index=False)
    (CEN if len(CEN) else pd.DataFrame(columns=["file"])).to_csv(OUT / f"{STAMP}.census.csv", index=False)
    pd.concat([WFA, pd.DataFrame(wfb)], ignore_index=True, sort=False).to_csv(
        OUT / f"{STAMP}.walkforward.csv", index=False)
    G[["panel", "form", "cadence", "gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
       "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "keep4a", "fail4b", "keep4b"]].to_csv(
        OUT / f"{STAMP}.keeppaths.csv", index=False)
    P("")
    P(f"  wrote {STAMP}.{{grid,bands,discrimination,census,walkforward,keeppaths}}.csv   ({time.time()-t0:.0f}s)")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()

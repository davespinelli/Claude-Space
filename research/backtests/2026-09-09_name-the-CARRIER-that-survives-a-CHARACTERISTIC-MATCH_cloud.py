#!/usr/bin/env python3
"""Idea 569 (cloud, 2026-09-09) - name-the-CARRIER-that-survives-a-CHARACTERISTIC-MATCH.

QUESTION
--------
Idea 51's MA-gate SELECTION premium `Sharpe(MA-RS) - Sharpe(EWall)` at matched (gross,
cadence) is monotone across three panels

    U56 -0.0045  >  B136 -0.0465  >  SMALL439 -0.1023          (published GAP = +0.0978)

Idea 312 killed the ETF-share read.  Idea 568 killed the cvol/breadth read: on kernel-matched
k=36 draws from the pooled B136+SMALL439 name pool the panel of ORIGIN still moved the premium
by **+0.1961 mean = 2.00x the whole published gap** (t +5.5..+8.0, 0/3 rungs inside the seed
sd).  So neither of the first two characteristics is the carrier.

This run adds the NEXT candidates named in the queue, one at a time, on the SAME machinery:

    mrho    marginal pairwise rho  - mean correlation of the name's daily returns with every
                                     other pooled name (idea 546: the marginal is the one
                                     characteristic statistic that is sign-stable across
                                     disjoint seed blocks; the partial is not)
    beta    beta of the name's daily returns to SPY over the pooled window
    tpers   trend persistence of the 200d signal - 1 minus the daily flip rate of the
            above-200d-MA state, i.e. the mean persistence of the gate's OWN variable
    plevel  log10 median close - the raw price level (a per-share scale, included because the
            queue names it and because it is the closest thing here to a placebo)

    cvol    REFERENCE, re-run so idea 568's answer is re-measured on THIS run's draws and the
            four new candidates are compared against a like-for-like anchor.

If a characteristic is the CARRIER, then holding it fixed must make the panel of origin stop
mattering: at a matched level, a draw built only from B136 names and a draw built only from
SMALL439 names should have the SAME premium.  That is the whole test.

DESIGN (idea 568's, verbatim where it can be)
---------------------------------------------
Pool  = 135 B136 tradables + SMALL tradables on the COMMON trading index (the small cache's
        span).  SMALL names with max_1d_move >= 1.0 in data/small_meta.csv are dropped FIRST.
        SPY joined as benchmark only, never a constituent.
        SURVIVORSHIP: both panels are CURRENT constituents (universe_broad.json is today's
        list; the small panel is today's sub-$2B screen, see data/SMALL_PANEL_README.md).
        Every level of this run inherits that bias; it is a statement about composition of
        surviving names, not about a tradable 2010 universe.
Draw  = k = 36 names, sampled WITHOUT replacement with probability proportional to a Gaussian
        kernel on the name's own characteristic,  w_i = exp(-0.5*((x_i-L)/h)^2), bandwidth
        h = 0.5 * sd(x) over the pooled names (idea 568's BW_MULT, NOT re-tuned).
        Seeded crc32("CHAR|{char}|{L:.6f}|{flavour}|{seed}"), 6 seeds per rung.
        k is 36 at every rung, so panel WIDTH is never confounded with composition.
Levels= PRE-REGISTERED as the pooled distribution's 10/30/50/70/90th percentiles of that
        characteristic (5 rungs each).  No level is hand-picked from a premium.
Arms (idea 51 verbatim, idea 312/568's code):
        EWall  gross g spread equally over every priced tradable name          (CONTROL)
        MA-RS  gross g spread equally over names with px > 200d MA (RESPREAD)  (TREATMENT)
        premium = Sharpe(MA-RS) - Sharpe(EWall) at the SAME (panel, g, cadence).
        RESPREAD holds gross fixed, so the premium is pure selection, no exposure dial.
ORIGIN CONTRAST: each rung is drawn three ways - POOL (all names), BONLY (B136 only), SONLY
        (SMALL only).  At a matched level these differ ONLY in panel of origin.  A rung runs
        only where the flavour can reach the level (feasible band = mean of its 36 lowest /
        36 highest names); infeasible rungs are reported, never silently dropped.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two): the characteristic and the target level.
Gross g in {0.50, 0.75, 1.00} and cadence {W, M} are REPORTED axes averaged over for the
headline premium (idea 51's convention); seed is replication; flavour is a reported contrast.
EVERY grid point is written to .grid.csv.

PRE-REGISTERED HYPOTHESES (written before any premium on a new characteristic was read)
---------------------------------------------------------------------------------------
GAP    = 0.0978  published U56 - SMALL439 premium gap (idea 51).
FLOOR  = 0.0745  idea 312's mean within-rung seed sd of the same premium at k=36.
ORIGIN568 = 0.1961  idea 568's mean matched-level B-S gap on cvol/breadth.

H_CARRIER(char) : at every overlapping matched rung of `char`, |premium(BONLY) -
                  premium(SONLY)| lies INSIDE the within-rung seed sd, AND the mean matched
                  B-S gap is below 0.5 * ORIGIN568.  A characteristic that does this has
                  ABSORBED the origin effect and IS the carrier.  This is the title question.
H_CHAR(char)    : the POOL premium is monotone in `char` in the direction that would
                  reproduce the published panel ordering (the required sign is fixed by the
                  three real panels' OWN values of `char`, computed before any premium), AND
                  |slope * span| >= 0.5 * GAP.
H_NOISE(char)   : that same |slope * span| exceeds the within-rung seed sd measured here.
H_PRED(char)    : the POOL fit predicts U56 > B136 > SMALL in premium AND max|resid| <= 0.03.
H_ANY           : at least one of the four NEW candidates passes H_CARRIER.  If H_ANY fails,
                  the answer to the title is NO CANDIDATE and the panel-of-origin effect is
                  still unnamed after six characteristics.

Rule 8 (walk-forward, required): WF-A refits every slope inside 2010-2016 and again in
2017-2026, read once, and reports whether the sign holds.  WF-B picks (char, level) by IS
Sharpe ALONE at g=0.75/W on the POOL flavour, then reads the OOS window once, against
RULES v2 on B136 and against SPY.  Both KEEP paths (4a vs RULES v2 on the same panel, 4b vs
SPY) are evaluated on EVERY book and counted.

Costs 10 bps per unit turnover, weights at close t applied t+1 (engine convention), no
shorting, no leverage.

GATES
-----
G1  idea 312's committed grid.csv REAL rows reproduce (36 rows x 13 columns).
G2  fast_backtest == engine.backtest on a real book.
G3  idea 568's committed cvol origin gaps reproduce on the rungs this run shares with it.
"""
import sys, time, zlib
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask  # noqa

STAMP = Path(__file__).name[:-3]
OUT = Path(__file__).resolve().parent
COST = 10.0
GROSS = [0.50, 0.75, 1.00]
CADENCE = ["W", "M"]
MA_WIN = 200
IS_END, OOS_START = "2016-12-31", "2017-01-01"
K = 36
SEEDS = [0, 1, 2, 3, 4, 5]
FLAVOURS = ["POOL", "BONLY", "SONLY"]
CHARS = ["cvol", "mrho", "beta", "tpers", "plevel"]     # cvol = idea 568 REFERENCE
NEW_CHARS = ["mrho", "beta", "tpers", "plevel"]
LEVEL_Q = [0.10, 0.30, 0.50, 0.70, 0.90]                # pre-registered rung placement
BW_MULT = 0.5                      # idea 568's bandwidth multiplier, NOT re-tuned
GAP = 0.0978                       # idea 51's published U56 - SMALL439 premium gap
FLOOR = 0.0745                     # idea 312's mean within-rung seed sd at k = 36
ORIGIN568 = 0.1961                 # idea 568's mean matched-level B-S gap
PARENT = "2026-09-09_is-the-panel-ordering-an-ETF-SHARE-effect_B.grid.csv"
PARENT568 = "2026-09-09_can-any-B136-recomposition-reach-SMALL439-s-CHARACTERISTIC-SUPPORT_C.origin.csv"
PARENT_END = "2026-09-04"          # idea 312's / idea 51's / idea 568's last bar
G1_TOL, G1_TOL_U56, G2_TOL, PRED_TOL = 1e-9, 1e-4, 1e-12, 0.03

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


# ------------------------------------------------------------------------- books
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


def make_books(px, tradable, g):
    e = _priced(px, tradable) > 0
    ma = above_ma(px) & e
    return {"EWall": _ew(e, g), "MA-RS": _ew(ma, g)}


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def rowify(r, tn=None):
    m = metrics(r)
    h1, h2 = halves(r)
    mi, mo = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    d = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
             IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"],
             OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])
    if tn is not None:
        d["turnover"] = float(tn.sum() / m["Years"])
    return d


def keep_4a(r, b):
    a1, a2 = halves(r)
    b1, b2 = halves(b)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(b)["MaxDD"])


def fail_4b(r, spy):
    a1, a2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not a1 > s1: f.append("H1")
    if not a2 > s2: f.append("H2")
    if not metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"]: f.append("OOS")
    if not m["MaxDD"] >= 0.60 * ms["MaxDD"]: f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
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
    """PROTOCOL: drop the small-panel tickers with a >= 100% one-day move BEFORE anything."""
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


# ------------------------------------------------ per-NAME characteristics (the new ones)
def name_chars(pool, spy_px):
    """Per-NAME characteristic on the pooled common window.

    cvol   annualised sd of daily returns                              (idea 568 REFERENCE)
    mrho   MARGINAL pairwise rho: mean pairwise correlation of the name with every other
           pooled name (pairwise-complete; idea 546's sign-stable statistic)
    beta   cov(r_i, r_spy) / var(r_spy) on the days both are priced
    tpers  1 - daily flip rate of the name's own above-200d-MA state, over days where a
           200d mean exists.  The persistence of the GATE'S OWN variable.
    plevel log10(median close) - the raw per-share price level
    """
    r = pool.pct_change()
    vol = (r.std() * np.sqrt(252)).astype(float)

    C = r.corr()                                   # pairwise-complete by construction
    n = C.shape[0]
    mrho = ((C.sum(axis=0) - 1.0) / (n - 1)).astype(float)

    sr = spy_px.pct_change().reindex(r.index)
    var_s = float(sr.var())
    beta = r.apply(lambda c: float(c.cov(sr)) / var_s if var_s > 0 else np.nan).astype(float)

    ma = pool.rolling(MA_WIN).mean()
    valid = pool.notna() & ma.notna()
    state = (pool > ma).where(valid)
    flips = state.astype(float).diff().abs()
    flips = flips.where(valid & valid.shift(1))
    denom = (valid & valid.shift(1)).sum().replace(0, np.nan)
    tpers = (1.0 - flips.sum() / denom).astype(float)

    plevel = np.log10(pool.median().astype(float).clip(lower=1e-6))

    return pd.DataFrame(dict(cvol=vol, mrho=mrho, beta=beta, tpers=tpers, plevel=plevel)).dropna()


def panel_chars(px, tradable, spy_r):
    """Panel-level values of the SAME five characteristics (equal-weight over constituents)."""
    cols = [c for c in px.columns if c in tradable]
    sub = px[cols]
    r = sub.pct_change()
    vol = float((r.std() * np.sqrt(252)).mean())
    C = r.corr().to_numpy()
    n = C.shape[0]
    rho = float((np.nansum(C) - n) / (n * (n - 1))) if n > 1 else np.nan
    on = above_ma(sub) & sub.notna()
    breadth = float(on.sum(axis=1).div(sub.notna().sum(axis=1).replace(0, np.nan)).mean())
    ew = r.mean(axis=1).fillna(0.0)
    sp = spy_r.reindex(ew.index).fillna(0.0)
    beta = float(np.cov(ew.values, sp.values)[0, 1] / np.var(sp.values)) if np.var(sp.values) > 0 else np.nan
    ma = sub.rolling(MA_WIN).mean()
    valid = sub.notna() & ma.notna()
    state = (sub > ma).where(valid)
    fl = state.astype(float).diff().abs().where(valid & valid.shift(1))
    den = (valid & valid.shift(1)).sum().replace(0, np.nan)
    tpers = float((1.0 - fl.sum() / den).mean())
    plevel = float(np.log10(sub.median().astype(float).clip(lower=1e-6)).mean())
    return dict(cvol=vol, mrho=rho, beta=beta, tpers=tpers, plevel=plevel, breadth=breadth)


def feasible_band(x):
    """Mean of the 36 lowest / 36 highest values: the reach of a k=36 draw from this pool."""
    v = np.sort(np.asarray(x, float))
    return float(v[:K].mean()), float(v[-K:].mean())


def draw_panels(nc, bnames, snames, levels):
    """Kernel-weighted k=36 draws at each (characteristic, level, flavour, seed)."""
    pools = {"POOL": list(nc.index),
             "BONLY": [c for c in nc.index if c in bnames],
             "SONLY": [c for c in nc.index if c in snames]}
    out, feas = {}, []
    for char, lv in levels.items():
        h = BW_MULT * float(nc[char].std())
        for fl in FLAVOURS:
            names = np.array(pools[fl])
            x = nc.loc[names, char].to_numpy()
            lo, hi = feasible_band(x)
            for L in lv:
                ok = lo <= L <= hi
                feas.append(dict(char=char, flavour=fl, level=L, reach_lo=lo, reach_hi=hi,
                                 feasible=ok, bandwidth=h, n_pool=len(names)))
                if not ok:
                    continue
                for sd in SEEDS:
                    seed = zlib.crc32(f"CHAR|{char}|{L:.6f}|{fl}|{sd}".encode()) % (2 ** 32)
                    rng = np.random.default_rng(seed)
                    w = np.exp(-0.5 * ((x - L) / h) ** 2)
                    w = w / w.sum()
                    pick = sorted(rng.choice(names, size=K, replace=False, p=w).tolist())
                    out[f"{char}~{fl}~L{L:.6f}~{sd}"] = dict(
                        names=pick, char=char, flavour=fl, level=L, seed=sd)
    return out, pd.DataFrame(feas)


# ==================================================================================== run
def main():
    t0 = time.time()
    P("=" * 118)
    P("IDEA 569  name-the-CARRIER-that-survives-a-CHARACTERISTIC-MATCH  (cloud, 2026-09-09)")
    P("=" * 118)
    P("Treatment = idea 51's MA-gate SELECTION premium, Sharpe(MA-RS) - Sharpe(EWall) at matched")
    P("(gross, cadence).  Kernel draws on the CHARACTERISTIC from the pooled B136 + SMALL pool,")
    P("k pinned at 36.  10 bps, t+1 fills, no leverage/shorting.")
    P(f"Candidates: {NEW_CHARS} (new) + cvol (idea 568 reference).")
    P(f"Pre-registered: GAP {GAP:.4f}  FLOOR {FLOOR:.4f}  ORIGIN568 {ORIGIN568:.4f}.")
    P("SURVIVORSHIP: B136 and the small panel are CURRENT constituents; every number below")
    P("inherits that bias and is a statement about surviving names, not a tradable 2010 list.")
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
        for g in GROSS:
            books = make_books(px, tr, g)
            for freq in CADENCE:
                res = {k: fast_backtest(px, w, COST, freq) for k, w in books.items()}
                rets = {k: v["returns"].loc[st:] for k, v in res.items()}
                mc = metrics(rets["EWall"])
                for k in books:
                    r = rets[k]
                    row = dict(panel=nm, kind="REAL", arm=k, gross=g, cadence=freq)
                    row.update(rowify(r, res[k]["turnover"].loc[st:]))
                    row["dCAGR_vs_EWall"] = row["CAGR"] - mc["CAGR"]
                    row["dSharpe_vs_EWall"] = row["Sharpe"] - mc["Sharpe"]
                    row["keep4a"] = keep_4a(r, v2)
                    row["fail4b"] = fail_4b(r, spy)
                    row["keep4b"] = row["fail4b"] == "-"
                    real_rows.append(row)
        P(f"  {nm:9s} {px.shape[1]:4d} cols, {len(tr):4d} tradable, sample from {st.date()}  ({time.time()-t0:.0f}s)")
    REAL = pd.DataFrame(real_rows)

    par = pd.read_csv(OUT / PARENT)
    par = par[(par.kind == "REAL") & par.arm.isin(["EWall", "MA-RS"])].copy()
    cmpcols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe", "IS_CAGR", "OOS_CAGR",
               "OOS_Sharpe", "OOS_MaxDD", "turnover", "dCAGR_vs_EWall", "dSharpe_vs_EWall"]
    keys = ["panel", "arm", "gross", "cadence"]
    m = REAL.merge(par, on=keys, suffixes=("", "_p"))
    assert len(m) == 36, len(m)
    perp = m.assign(d=np.abs(m[cmpcols].values - m[[c + '_p' for c in cmpcols]].values).max(1)) \
            .groupby("panel").d.max()
    P(f"  rows matched: {len(m)}/36   per panel: " + "  ".join(f"{k} {v:.2e}" for k, v in perp.items()))
    for pnl, tol in ((SMALLK, G1_TOL), ("B136", G1_TOL), ("U56", G1_TOL_U56)):
        assert float(perp[pnl]) < tol, f"G1 FAILED on {pnl} at {perp[pnl]:.3e} (bar {tol:.0e})"
    P("  U56 carries idea 312's documented data/prices.csv adjusted-close revision (<= 5.1e-5 relative).")
    P("  G1 PASS.  4a/4b flags reproduce: "
      f"4a {int((m.keep4a == m.keep4a_p).sum())}/36, 4b {int((m.keep4b == m.keep4b_p).sum())}/36")
    pub = REAL[REAL.arm == "MA-RS"].groupby("panel").dSharpe_vs_EWall.mean()
    P("  published premium re-read:  " + "  ".join(f"{k} {v:+.4f}" for k, v in pub.items()))
    gap_reread = float(pub["U56"] - pub[SMALLK])
    P(f"  U56 - {SMALLK} gap re-read: {gap_reread:+.4f}  (pre-registered GAP {GAP:.4f})")

    # ---------------------------------------------------------------- G2 identity
    P("")
    P("=" * 118)
    P("G2  IDENTITY GATE - fast_backtest vs engine.backtest")
    P("=" * 118)
    worst = 0.0
    for nm, (px, tr) in panels.items():
        w = make_books(px, tr, 0.75)["MA-RS"]
        a = fast_backtest(px, w, COST, "W")["returns"]
        b = backtest(px, w, cost_bps=COST, freq="W")["returns"]
        d = float((a - b).abs().max())
        worst = max(worst, d)
        P(f"  {nm:9s} max |dreturn| {d:.3e}")
    assert worst < G2_TOL, f"G2 FAILED at {worst:.3e}"
    P(f"  G2 PASS ({worst:.3e} < {G2_TOL:.0e})")

    # ---------------------------------------------------------------- pooled frame
    P("")
    P("=" * 118)
    P("THE POOL - B136 + SMALL on the common index, five per-name characteristics")
    P("=" * 118)
    pxB, trB = panels["B136"]
    pxS, trS = panels[SMALLK]
    ix = pxB.index.intersection(pxS.index)
    bn = sorted([c for c in pxB.columns if c in trB and c != "SPY"])
    sn = sorted([c for c in pxS.columns if c in trS])
    pool = pd.concat([pxB.loc[ix, bn], pxS.loc[ix, sn]], axis=1).ffill()
    spy_pool = pxB.loc[ix, "SPY"]
    nc = name_chars(pool, spy_pool)
    bnames, snames = set(bn) & set(nc.index), set(sn) & set(nc.index)
    P(f"  pooled index {ix.min().date()} .. {ix.max().date()}  ({len(ix)} bars)")
    P(f"  names: B {len(bnames)}  SMALL {len(snames)}  total {len(nc)}")
    P("")
    P("  per-name characteristic distributions and k=36 REACH")
    P("  " + f"{'char':8s} {'B mean':>8s} {'S mean':>8s} {'sd':>8s} {'bw':>8s} "
        f"{'BONLY reach':>20s} {'SONLY reach':>20s} {'POOL reach':>20s}")
    LEVELS = {}
    for ch_ in CHARS:
        b_lo, b_hi = feasible_band(nc.loc[sorted(bnames), ch_])
        s_lo, s_hi = feasible_band(nc.loc[sorted(snames), ch_])
        p_lo, p_hi = feasible_band(nc[ch_])
        LEVELS[ch_] = [round(float(nc[ch_].quantile(q)), 6) for q in LEVEL_Q]
        P("  " + f"{ch_:8s} {nc.loc[sorted(bnames), ch_].mean():8.4f} {nc.loc[sorted(snames), ch_].mean():8.4f} "
            f"{nc[ch_].std():8.4f} {BW_MULT*float(nc[ch_].std()):8.4f} "
            f"[{b_lo:8.4f},{b_hi:8.4f}] [{s_lo:8.4f},{s_hi:8.4f}] [{p_lo:8.4f},{p_hi:8.4f}]")
    P("")
    P("  PRE-REGISTERED rung levels (pooled 10/30/50/70/90th percentiles):")
    for ch_ in CHARS:
        P(f"    {ch_:8s} " + "  ".join(f"{v:.4f}" for v in LEVELS[ch_]))

    # real panels' own characteristics on the SAME common window (like-for-like)
    P("")
    P("  REAL panels restated on the pooled window (premium re-measured there too):")
    real_common = {}
    for nm, (px, tr) in panels.items():
        pxc = px.reindex(ix).ffill()
        st = pxc.index[260]
        spy = pxc["SPY"].pct_change().fillna(0.0).loc[st:]
        ch = panel_chars(pxc, tr, spy)
        prem = []
        for g in GROSS:
            books = make_books(pxc, tr, g)
            for freq in CADENCE:
                rr = {k: fast_backtest(pxc, w, COST, freq)["returns"].loc[st:] for k, w in books.items()}
                prem.append(metrics(rr["MA-RS"])["Sharpe"] - metrics(rr["EWall"])["Sharpe"])
        real_common[nm] = dict(prem_common=float(np.mean(prem)), prem_full=float(pub[nm]), **ch)
        P(f"    {nm:9s} cvol {ch['cvol']:.4f}  mrho {ch['mrho']:.4f}  beta {ch['beta']:.3f}  "
          f"tpers {ch['tpers']:.4f}  plevel {ch['plevel']:.3f}  premium(full) {pub[nm]:+.4f}  "
          f"premium(common) {np.mean(prem):+.4f}")
    gap_common = real_common["U56"]["prem_common"] - real_common[SMALLK]["prem_common"]
    P(f"    U56 - {SMALLK} gap on the common window: {gap_common:+.4f}  (full sample {gap_reread:+.4f})")

    # required slope sign, fixed by the panels' OWN characteristic values (no premium read)
    P("")
    P("  REQUIRED SLOPE SIGN per characteristic (fixed by the three panels' own values, so that")
    P("  a monotone fit would reproduce the published U56 > B136 > SMALL premium ordering):")
    req_sign, panel_mono = {}, {}
    for ch_ in CHARS:
        u, b_, s_ = (real_common["U56"][ch_], real_common["B136"][ch_], real_common[SMALLK][ch_])
        mono = (u > b_ > s_) or (u < b_ < s_)
        req_sign[ch_] = float(np.sign(u - s_)) if u != s_ else 0.0
        panel_mono[ch_] = bool(mono)
        P(f"    {ch_:8s} U56 {u:+8.4f}  B136 {b_:+8.4f}  {SMALLK} {s_:+8.4f}   "
          f"panel-monotone {str(mono):5s}   required slope sign {req_sign[ch_]:+.0f}")

    # ---------------------------------------------------------------- draws
    P("")
    P("=" * 118)
    P("DRAWS - kernel-matched k=36 sub-panels")
    P("=" * 118)
    dr, FEAS = draw_panels(nc, bnames, snames, LEVELS)
    P(f"  rungs planned {len(FEAS)}, feasible {int(FEAS.feasible.sum())}, draws {len(dr)}")
    infeas = FEAS[~FEAS.feasible]
    if len(infeas):
        P("  INFEASIBLE rungs (flavour cannot reach the level with k=36):")
        for _, r in infeas.iterrows():
            P(f"    {r['char']:8s} {r['flavour']:6s} L={r['level']:9.4f}  reach [{r['reach_lo']:.4f}, {r['reach_hi']:.4f}]")

    # ---------------------------------------------------------------- the ladder
    P("")
    P("=" * 118)
    P("THE LADDER - premium on kernel-matched k=36 draws")
    P("=" * 118)
    grid, chars = [], []
    for key, d in dr.items():
        pxd = pd.concat([pool[d["names"]], spy_pool.rename("SPY")], axis=1).dropna(how="all").ffill()
        tr = set(d["names"])
        st = pxd.index[260]
        spy = pxd["SPY"].pct_change().fillna(0.0).loc[st:]
        v2 = fast_backtest(pxd, rules_v2_weights(pxd), COST, "W")["returns"].loc[st:]
        ch = panel_chars(pxd, tr, spy)
        nb = sum(1 for c in d["names"] if c in bnames)
        chars.append(dict(panel=key, **{k: d[k] for k in ("char", "flavour", "level", "seed")},
                          n_from_B=nb, n_from_S=K - nb, **ch))
        for g in GROSS:
            books = make_books(pxd, tr, g)
            for freq in CADENCE:
                res = {k: fast_backtest(pxd, w, COST, freq) for k, w in books.items()}
                rets = {k: v["returns"].loc[st:] for k, v in res.items()}
                mc = metrics(rets["EWall"])
                mci = metrics(rets["EWall"].loc[:IS_END])["Sharpe"]
                mco = metrics(rets["EWall"].loc[OOS_START:])["Sharpe"]
                for k in books:
                    r = rets[k]
                    row = dict(panel=key, kind="DRAW", arm=k, gross=g, cadence=freq,
                               char=d["char"], flavour=d["flavour"], level=d["level"], seed=d["seed"],
                               achieved=ch[d["char"]], n_from_B=nb,
                               **{f"ach_{c}": ch[c] for c in CHARS})
                    row.update(rowify(r, res[k]["turnover"].loc[st:]))
                    row["dCAGR_vs_EWall"] = row["CAGR"] - mc["CAGR"]
                    row["dSharpe_vs_EWall"] = row["Sharpe"] - mc["Sharpe"]
                    row["dIS_Sharpe_vs_EWall"] = row["IS_Sharpe"] - mci
                    row["dOOS_Sharpe_vs_EWall"] = row["OOS_Sharpe"] - mco
                    row["keep4a"] = keep_4a(r, v2)
                    row["fail4b"] = fail_4b(r, spy)
                    row["keep4b"] = row["fail4b"] == "-"
                    grid.append(row)
    G = pd.DataFrame(grid)
    CH = pd.DataFrame(chars)
    P(f"  {len(dr)} draws x 2 arms x {len(GROSS)} gross x {len(CADENCE)} cadence = {len(G)} books  ({time.time()-t0:.0f}s)")

    T = G[G.arm == "MA-RS"]
    draw_prem = T.groupby(["panel", "char", "flavour", "level", "seed"]).agg(
        premium=("dSharpe_vs_EWall", "mean"),
        prem_IS=("dIS_Sharpe_vs_EWall", "mean"),
        prem_OOS=("dOOS_Sharpe_vs_EWall", "mean"),
        achieved=("achieved", "first"), n_from_B=("n_from_B", "first")).reset_index()
    rung = draw_prem.groupby(["char", "flavour", "level"]).agg(
        n=("premium", "size"), achieved=("achieved", "mean"), n_from_B=("n_from_B", "mean"),
        premium=("premium", "mean"), sd=("premium", "std"),
        prem_IS=("prem_IS", "mean"), prem_OOS=("prem_OOS", "mean")).reset_index()
    P("")
    P("  RUNGS (premium = mean over 6 seeds x 3 gross x 2 cadence; sd = across seeds)")
    P("  " + f"{'char':8s} {'flavour':7s} {'L':>9s} {'achieved':>9s} {'nB/36':>6s} "
        f"{'premium':>9s} {'sd':>7s} {'IS':>8s} {'OOS':>8s}")
    for _, r in rung.iterrows():
        P("  " + f"{r['char']:8s} {r['flavour']:7s} {r['level']:9.4f} {r['achieved']:9.4f} "
            f"{r['n_from_B']:6.1f} {r['premium']:+9.4f} {r['sd']:7.4f} {r['prem_IS']:+8.4f} "
            f"{r['prem_OOS']:+8.4f}")

    floor_here = float(rung.sd.mean())
    P("")
    P(f"  NOISE FLOOR recomputed here: mean within-rung seed sd = {floor_here:.4f} "
      f"({floor_here/GAP:.2f}x the published GAP; idea 312 got {FLOOR:.4f})")

    # ---------------------------------------------------------------- H_CHAR / H_NOISE
    P("")
    P("=" * 118)
    P("H_CHAR / H_NOISE  - is the premium a function of the characteristic?")
    P("=" * 118)
    slopes = []
    for ch_ in CHARS:
        for fl in FLAVOURS:
            d = draw_prem[(draw_prem.char == ch_) & (draw_prem.flavour == fl)]
            if d.level.nunique() < 3:
                continue
            a, b, r2 = ols(d.achieved, d.premium)
            span = float(d.achieved.max() - d.achieved.min())
            rr = rung[(rung.char == ch_) & (rung.flavour == fl)].sort_values("achieved")
            mono_dn = bool((rr.premium.diff().dropna() <= 0).all())
            mono_up = bool((rr.premium.diff().dropna() >= 0).all())
            eff = b * span
            slopes.append(dict(char=ch_, flavour=fl, n=len(d), intercept=a, slope=b, r2=r2,
                               span=span, effect=eff, sd_within=float(rr.sd.mean()),
                               ratio_to_GAP=abs(eff) / GAP, mono_down=mono_dn, mono_up=mono_up,
                               req_sign=req_sign[ch_],
                               sign_ok=bool(np.sign(b) == req_sign[ch_] and req_sign[ch_] != 0)))
    SL = pd.DataFrame(slopes)
    P("  " + f"{'char':8s} {'flavour':7s} {'n':>4s} {'slope':>10s} {'R2':>7s} {'span':>8s} "
        f"{'slope*span':>11s} {'|eff|/GAP':>10s} {'sd_within':>10s} {'signOK':>7s} {'mono':>6s}")
    for _, r in SL.iterrows():
        mono = "down" if r["mono_down"] else ("up" if r["mono_up"] else "-")
        P("  " + f"{r['char']:8s} {r['flavour']:7s} {r['n']:4.0f} {r['slope']:+10.4f} {r['r2']:7.4f} "
            f"{r['span']:8.4f} {r['effect']:+11.4f} {r['ratio_to_GAP']:10.2f} {r['sd_within']:10.4f} "
            f"{str(r['sign_ok']):>7s} {mono:>6s}")

    H_CHAR, H_NOISE = {}, {}
    for ch_ in CHARS:
        row = SL[(SL.char == ch_) & (SL.flavour == "POOL")]
        if not len(row):
            H_CHAR[ch_] = H_NOISE[ch_] = None
            continue
        row = row.iloc[0]
        H_CHAR[ch_] = bool(row["sign_ok"] and abs(row["effect"]) >= 0.5 * GAP)
        H_NOISE[ch_] = bool(abs(row["effect"]) > row["sd_within"])
    P("")
    for ch_ in CHARS:
        P(f"  {ch_:8s} H_CHAR {str(H_CHAR[ch_]):5s}   H_NOISE {str(H_NOISE[ch_]):5s}"
          f"   (bar: correct sign AND |slope*span| >= {0.5*GAP:.4f}; effect above own seed sd)")

    # ---------------------------------------------------------------- H_CARRIER
    P("")
    P("=" * 118)
    P("H_CARRIER  - at a MATCHED level, does the panel of ORIGIN stop mattering?")
    P("=" * 118)
    P("  A characteristic is the CARRIER iff holding it fixed collapses the B-sourced minus")
    P("  S-sourced premium into the seed noise floor.  Idea 568 measured +0.1961 on cvol/breadth.")
    P("")
    orig = []
    for ch_ in CHARS:
        for L in LEVELS[ch_]:
            d = rung[(rung.char == ch_) & (np.abs(rung.level - L) < 1e-9)].set_index("flavour")
            if not {"BONLY", "SONLY"} <= set(d.index):
                continue
            db, ds = d.loc["BONLY"], d.loc["SONLY"]
            sd_pair = float(np.sqrt((db["sd"] ** 2 + ds["sd"] ** 2) / 2))
            gap_bs = float(db["premium"] - ds["premium"])
            orig.append(dict(char=ch_, level=L, achieved_B=db["achieved"], achieved_S=ds["achieved"],
                             match_resid=float(db["achieved"] - ds["achieved"]),
                             prem_B=db["premium"], prem_S=ds["premium"], gap=gap_bs,
                             sd_pair=sd_pair,
                             t=gap_bs / (sd_pair / np.sqrt(len(SEEDS))) if sd_pair > 0 else np.nan,
                             within_floor=abs(gap_bs) <= sd_pair,
                             ratio_to_GAP=gap_bs / GAP, ratio_to_568=gap_bs / ORIGIN568))
    OR = pd.DataFrame(orig)
    H_CARRIER = {}
    if len(OR):
        P("  " + f"{'char':8s} {'L':>9s} {'achB':>8s} {'achS':>8s} {'resid':>8s} {'premB':>8s} "
            f"{'premS':>8s} {'B-S':>8s} {'sd':>7s} {'t':>7s} {'/GAP':>7s} {'/568':>7s}")
        for _, r in OR.iterrows():
            P("  " + f"{r['char']:8s} {r['level']:9.4f} {r['achieved_B']:8.4f} {r['achieved_S']:8.4f} "
                f"{r['match_resid']:+8.4f} {r['prem_B']:+8.4f} {r['prem_S']:+8.4f} {r['gap']:+8.4f} "
                f"{r['sd_pair']:7.4f} {r['t']:+7.2f} {r['ratio_to_GAP']:+7.2f} {r['ratio_to_568']:+7.2f}")
        P("")
        for ch_ in CHARS:
            d = OR[OR.char == ch_]
            if not len(d):
                H_CARRIER[ch_] = None
                P(f"  {ch_:8s} NO OVERLAPPING RUNG - BONLY and SONLY reach disjoint level sets at k=36.")
                continue
            mg = float(d.gap.mean())
            H_CARRIER[ch_] = bool(d.within_floor.all() and abs(mg) < 0.5 * ORIGIN568)
            P(f"  {ch_:8s} H_CARRIER {str(H_CARRIER[ch_]):5s}   {int(d.within_floor.sum())}/{len(d)} "
              f"rungs inside the seed sd   mean B-S {mg:+.4f} = {mg/GAP:+.2f}x GAP = "
              f"{mg/ORIGIN568:+.2f}x idea 568")
    else:
        for ch_ in CHARS:
            H_CARRIER[ch_] = None
        P("  NO OVERLAPPING RUNG on any characteristic.")
    H_ANY = any(H_CARRIER.get(c) is True for c in NEW_CHARS)
    P("")
    P(f"  H_ANY (at least one NEW candidate is the carrier): {'PASS' if H_ANY else 'FAIL'}")

    # ---------------------------------------------------------------- G3 vs idea 568
    P("")
    P("=" * 118)
    P("G3  idea 568's committed cvol/breadth origin gaps, beside this run's cvol rungs")
    P("=" * 118)
    p568 = OUT / PARENT568
    if p568.exists():
        o5 = pd.read_csv(p568)
        P("  idea 568 committed:")
        for _, r in o5.iterrows():
            P(f"    {r['char']:8s} L={r['level']:.3f}  B-S {r['gap']:+.4f}  t {r['t']:+.2f}  "
              f"inside sd {r['within_floor']}")
        P(f"  idea 568 mean matched B-S gap: {o5.gap.mean():+.4f}  (pre-registered {ORIGIN568:.4f})")
        assert abs(float(o5.gap.mean()) - ORIGIN568) < 5e-4, "G3: idea 568's committed mean moved"
        P("  G3 PASS (committed artefact reproduces the pre-registered anchor).")
    else:
        P("  G3 SKIPPED - idea 568's origin.csv not present.")

    # ---------------------------------------------------------------- H_PRED
    P("")
    P("=" * 118)
    P("H_PRED  - does each POOL fit predict the three real panels' published premia?")
    P("=" * 118)
    pred = []
    for ch_ in CHARS:
        row = SL[(SL.char == ch_) & (SL.flavour == "POOL")]
        if not len(row):
            continue
        row = row.iloc[0]
        for nm, rc in real_common.items():
            yhat = row["intercept"] + row["slope"] * rc[ch_]
            for tgt, lbl in ((rc["prem_common"], "common"), (rc["prem_full"], "full")):
                pred.append(dict(char=ch_, panel=nm, x=rc[ch_], pred=yhat, actual=tgt,
                                 window=lbl, resid=tgt - yhat))
    PR = pd.DataFrame(pred)
    H_PRED = {}
    for ch_ in CHARS:
        d = PR[(PR.char == ch_) & (PR.window == "common")]
        if not len(d):
            H_PRED[ch_] = None
            continue
        d = d.set_index("panel")
        order_ok = bool(d.loc["U56", "pred"] > d.loc["B136", "pred"] > d.loc[SMALLK, "pred"])
        mr = float(d.resid.abs().max())
        H_PRED[ch_] = bool(order_ok and mr <= PRED_TOL)
        P(f"  {ch_:8s} predicted  " + "  ".join(f"{k} {v:+.4f}" for k, v in d["pred"].items()) +
          f"   ordering {order_ok}   max|resid| {mr:.4f}   H_PRED {H_PRED[ch_]}")
    P(f"  actual(common)  " + "  ".join(
        f"{k} {v['prem_common']:+.4f}" for k, v in real_common.items()))

    # ---------------------------------------------------------------- RULE 8
    P("")
    P("=" * 118)
    P("RULE 8 WALK-FORWARD   IS <= %s, OOS >= %s (read once)" % (IS_END, OOS_START))
    P("=" * 118)
    wf = []
    P("  WF-A  every slope refit inside each window")
    P("  " + f"{'char':8s} {'flavour':7s} {'slope_IS':>10s} {'R2_IS':>7s} {'slope_OOS':>10s} "
        f"{'R2_OOS':>7s} {'slope_full':>11s} {'sign holds':>11s}")
    for ch_ in CHARS:
        for fl in FLAVOURS:
            d = draw_prem[(draw_prem.char == ch_) & (draw_prem.flavour == fl)]
            if d.level.nunique() < 3:
                continue
            _, b_is, r2_is = ols(d.achieved, d.prem_IS)
            _, b_oos, r2_oos = ols(d.achieved, d.prem_OOS)
            _, b_full, r2_full = ols(d.achieved, d.premium)
            hold = bool(np.sign(b_is) == np.sign(b_oos))
            wf.append(dict(leg="WF-A", char=ch_, flavour=fl, slope_IS=b_is, r2_IS=r2_is,
                           slope_OOS=b_oos, r2_OOS=r2_oos, slope_full=b_full, sign_hold=hold))
            P("  " + f"{ch_:8s} {fl:7s} {b_is:+10.4f} {r2_is:7.3f} {b_oos:+10.4f} {r2_oos:7.3f} "
                f"{b_full:+11.4f} {str(hold):>11s}")
    WFA = pd.DataFrame([w for w in wf if w["leg"] == "WF-A"])
    P(f"  sign holds IS -> OOS in {int(WFA.sign_hold.sum())}/{len(WFA)} (char, flavour) cells")

    P("")
    P("  WF-B  a BOOK: pick (char, level) by IS Sharpe of the seed-pooled MA-RS book at g=0.75/W, POOL")
    sel = G[(G.arm == "MA-RS") & (G.gross == 0.75) & (G.cadence == "W") & (G.flavour == "POOL")]
    pick_tbl = sel.groupby(["char", "level"]).agg(IS_Sharpe=("IS_Sharpe", "mean"),
                                                  OOS_Sharpe=("OOS_Sharpe", "mean")).reset_index()
    for _, r in pick_tbl.sort_values("IS_Sharpe", ascending=False).iterrows():
        P(f"    {r['char']:8s} L={r['level']:9.4f}  IS {r['IS_Sharpe']:+.4f}   (OOS {r['OOS_Sharpe']:+.4f})")
    best = pick_tbl.sort_values("IS_Sharpe", ascending=False).iloc[0]
    P(f"    PICK (IS only): {best['char']} L={best['level']:.4f}")

    keys_pick = [k for k, d in dr.items()
                 if d["char"] == best["char"] and abs(d["level"] - best["level"]) < 1e-9
                 and d["flavour"] == "POOL"]
    rets_pick = []
    for key in keys_pick:
        d = dr[key]
        pxd = pd.concat([pool[d["names"]], spy_pool.rename("SPY")], axis=1).dropna(how="all").ffill()
        st = pxd.index[260]
        w = make_books(pxd, set(d["names"]), 0.75)["MA-RS"]
        rets_pick.append(fast_backtest(pxd, w, COST, "W")["returns"].loc[st:])
    RP = pd.concat(rets_pick, axis=1).fillna(0.0).mean(axis=1)     # equal-weight over the 6 draws
    st_b = pxB.index[260]
    b136_v2 = backtest(pxB, rules_v2_weights(pxB), cost_bps=COST, freq="W")["returns"].loc[st_b:] \
        .reindex(RP.index).fillna(0.0)
    spy_r = spy_pool.pct_change().fillna(0.0).reindex(RP.index).fillna(0.0)
    P("")
    P("  " + f"{'book':28s} {'CAGR':>8s} {'Sharpe':>8s} {'MaxDD':>8s} {'H1':>7s} {'H2':>7s} "
        f"{'OOS_CAGR':>9s} {'OOS_Sh':>8s} {'OOS_DD':>8s}")
    wfb = []
    for nm, r in (("WF-B pick (seed-pooled)", RP), ("RULES v2 (B136)", b136_v2), ("SPY", spy_r)):
        d = rowify(r)
        wfb.append(dict(leg="WF-B", book=nm, **d))
        P("  " + f"{nm:28s} {d['CAGR']:8.2%} {d['Sharpe']:8.3f} {d['MaxDD']:8.2%} {d['H1']:7.3f} "
            f"{d['H2']:7.3f} {d['OOS_CAGR']:9.2%} {d['OOS_Sharpe']:8.3f} {d['OOS_MaxDD']:8.2%}")
    P(f"  WF-B 4a vs RULES v2 (B136): {keep_4a(RP, b136_v2)}    4b fail legs vs SPY: {fail_4b(RP, spy_r)}")

    # ---------------------------------------------------------------- KEEP paths
    P("")
    P("=" * 118)
    P("KEEP PATHS over every book (4a vs RULES v2 on the SAME panel, 4b vs SPY)")
    P("=" * 118)
    ALL = pd.concat([REAL.assign(char="-", flavour="REAL", level=np.nan, seed=-1), G],
                    ignore_index=True, sort=False)
    P(f"  books: {len(ALL)} ({len(REAL)} REAL + {len(G)} DRAW)")
    P(f"  4a passes {int(ALL.keep4a.sum())}/{len(ALL)}   4b passes {int(ALL.keep4b.sum())}/{len(ALL)}   "
      f"BOTH {int((ALL.keep4a & ALL.keep4b).sum())}/{len(ALL)}")
    legs = pd.Series([x for s in ALL.loc[~ALL.keep4b, "fail4b"] for x in s.split(",")]).value_counts()
    P("  binding 4b legs: " + "  ".join(f"{k} {v}" for k, v in legs.items()))
    if int(ALL.keep4b.sum()):
        by_arm = ALL[ALL.keep4b].arm.value_counts()
        P("  4b passers by arm: " + "  ".join(f"{k} {v}" for k, v in by_arm.items()))
        bb = ALL[ALL.keep4b].sort_values("Sharpe", ascending=False).head(5)
        P("  top 4b passers (DIAGNOSTIC ONLY - a kernel draw is not a tradable rule):")
        for _, r in bb.iterrows():
            P(f"    {str(r['panel'])[:36]:36s} {r['arm']:6s} g={r['gross']:.2f} {r['cadence']}  "
              f"CAGR {r['CAGR']:6.2%}  Sh {r['Sharpe']:.3f}  DD {r['MaxDD']:7.2%}  "
              f"H1/H2 {r['H1']:.2f}/{r['H2']:.2f}  OOS {r['OOS_Sharpe']:.3f}")
    KP = ALL[["panel", "kind", "arm", "gross", "cadence", "char", "flavour", "level", "seed",
              "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
              "keep4a", "fail4b", "keep4b"]]

    # ---------------------------------------------------------------- verdict
    P("")
    P("=" * 118)
    P("VERDICT")
    P("=" * 118)
    P("  " + f"{'char':8s} {'H_CARRIER':>10s} {'H_CHAR':>7s} {'H_NOISE':>8s} {'H_PRED':>7s}  mean B-S at matched level")
    for ch_ in CHARS:
        d = OR[OR.char == ch_] if len(OR) else OR
        mg = f"{d.gap.mean():+.4f} ({d.gap.mean()/ORIGIN568:+.2f}x 568)" if len(d) else "no overlapping rung"
        P("  " + f"{ch_:8s} {str(H_CARRIER.get(ch_)):>10s} {str(H_CHAR.get(ch_)):>7s} "
            f"{str(H_NOISE.get(ch_)):>8s} {str(H_PRED.get(ch_)):>7s}  {mg}")
    P("")
    P(f"  H_ANY: {'PASS - a carrier is named' if H_ANY else 'FAIL - NO CANDIDATE closes the matched-level B-S gap'}")

    # ---------------------------------------------------------------- outputs
    G.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    rung.merge(SL, on=["char", "flavour"], how="left", suffixes=("", "_fit")).to_csv(
        OUT / f"{STAMP}.rungs.csv", index=False)
    (OR if len(OR) else pd.DataFrame(columns=["char"])).to_csv(OUT / f"{STAMP}.origin.csv", index=False)
    PR.to_csv(OUT / f"{STAMP}.predict.csv", index=False)
    pd.concat([pd.DataFrame(wf), pd.DataFrame(wfb)], ignore_index=True, sort=False).to_csv(
        OUT / f"{STAMP}.walkforward.csv", index=False)
    KP.to_csv(OUT / f"{STAMP}.keeppaths.csv", index=False)
    CH.merge(FEAS, on=["char", "flavour", "level"], how="left").to_csv(OUT / f"{STAMP}.chars.csv", index=False)
    nc.to_csv(OUT / f"{STAMP}.namechars.csv")
    P("")
    P(f"  wrote {STAMP}.{{grid,rungs,origin,predict,walkforward,keeppaths,chars,namechars}}.csv   ({time.time()-t0:.0f}s)")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()

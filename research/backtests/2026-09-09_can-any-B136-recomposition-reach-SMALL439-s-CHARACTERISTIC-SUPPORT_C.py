#!/usr/bin/env python3
"""Idea 568 (lane C, 2026-09-09) - can-any-B136-recomposition-reach-SMALL439-s-CHARACTERISTIC-SUPPORT.

QUESTION
--------
Idea 51's MA-gate SELECTION premium `Sharpe(MA-RS) - Sharpe(EWall)` at matched (gross,
cadence) is monotone across three panels

    U56 -0.0045  >  B136 -0.0465  >  SMALL439 -0.1023          (published GAP = +0.0978)

and the record reads that as a cap / universe-boundary fact.  Idea 312 (lane B) killed the
ETF-share read: the premium's slope in ETF share runs BACKWARDS (-0.85x the gap) and the
within-rung seed sd is 0.0745 = 0.76x the whole published gap.  Its by-product is this
idea's premise: every k=36 ETF-share-matched sub-panel of B136 lives at cvol 0.21-0.31 and
breadth 0.67-0.71, while SMALL439 sits at cvol 0.562 and breadth 0.475 - the ladder never
reaches the anchor, so the published ordering was never actually bracketed.

This run matches on the CHARACTERISTIC instead of on ETF share.  Draws are kernel-weighted
samples from the POOLED B136 + SMALL439 name pool at a grid of target cvol / breadth levels,
so support can cover both ends by construction.  Then: is the premium a function of the
characteristic once support overlaps, or does the panel of ORIGIN still carry it?

DESIGN
------
Pool  = 135 B136 tradables + 439 SMALL tradables = 574 names on the COMMON trading index
        (2010-01-04 .. 2026-09-04, the small cache's span).  SPY joined as benchmark only.
Draw  = k = 36 names, sampled WITHOUT replacement with probability proportional to a
        Gaussian kernel on the name's own characteristic,  w_i = exp(-0.5*((x_i-L)/h)^2),
        bandwidth h = 0.5 * sd(x) over the pooled names (PRE-REGISTERED, not tuned).
        Seeded crc32("CHAR|{char}|{L:.3f}|{flavour}|{seed}"), 6 seeds per rung.
        k is 36 at every rung, so panel WIDTH is never confounded with composition.
Arms (idea 51 verbatim, idea 312's code):
        EWall  gross g spread equally over every priced tradable name          (CONTROL)
        MA-RS  gross g spread equally over names with px > 200d MA (RESPREAD)  (TREATMENT)
        premium = Sharpe(MA-RS) - Sharpe(EWall) at the SAME (panel, g, cadence).
        RESPREAD holds gross fixed, so the premium is pure selection, no exposure dial.
ORIGIN CONTRAST (reported, not tuned): each rung is drawn three ways -
        POOL  (all 574 names), BONLY (B136 names only), SONLY (SMALL439 names only).
        At a MATCHED characteristic level these differ only in panel of origin, which is
        exactly the confound the published ordering cannot separate.  A rung is run only
        where the flavour can reach the level (feasible band = mean of its 36 lowest /
        36 highest names); infeasible rungs are reported, not silently dropped.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two): the characteristic {cvol, breadth} and the
target level L.  Gross g in {0.50, 0.75, 1.00} and cadence {W, M} are REPORTED axes averaged
over for the headline premium (idea 51's own convention); seed is replication; flavour is a
reported contrast.  Every grid point is written to .grid.csv.

PRE-REGISTERED HYPOTHESES (written before any premium on a pooled draw was read)
-------------------------------------------------------------------------------
GAP   = 0.0978 (published U56 - SMALL439 premium gap, idea 51).
FLOOR = 0.0745 (idea 312's mean within-rung seed sd of the same premium at k=36).
H_SUPPORT : pooled draws reach cvol <= 0.32 AND >= 0.55, and breadth >= 0.68 AND <= 0.48,
            i.e. the draw-level support covers B136's random-draw region AND SMALL439's
            anchor.  This is the idea's premise; FAIL here answers the title NO.
H_CHAR    : premium is monotone non-increasing in cvol (and non-decreasing in breadth) over
            the POOL rungs, AND |slope * span| >= 0.5 * GAP with the published sign.
H_NOISE   : that same |slope * span| exceeds the within-rung seed sd recomputed here.  A
            span inside its own noise floor is not a characteristic effect.
H_ORIGIN  : at matched level, |premium(BONLY) - premium(SONLY)| <= the within-rung sd on
            every overlapping rung.  If origin still separates the arms at matched cvol,
            the characteristic is NOT the carrier and the cap read is not rescued either.
H_PRED    : OLS premium ~ a + b*x on the POOL rungs, evaluated at the three real panels'
            own characteristic, reproduces their published ordering with |resid| <= 0.03
            (idea 312's tolerance, verbatim).

GATES (run before any new number is read)
    G1 reproduction: idea 312's committed `.grid.csv` REAL rows (3 panels x 2 arms x 3 gross
       x 2 cadence = 36 rows) rebuilt from source to 1e-9 (B136 / SMALL439) and 1e-4 (U56,
       which carries the documented data/prices.csv adjusted-close revision).
    G2 identity: the vectorised runner vs engine.backtest on one book per real panel.

RULE 8 WALK-FORWARD (required)
    IS = start..2016-12-31, OOS = 2017-01-01..end, read once.
    WF-A on the ANSWER: refit premium ~ characteristic on IS-only and OOS-only returns;
       report sign hold and magnitude.
    WF-B on a BOOK: choose (characteristic, level) by IS Sharpe of the seed-pooled MA-RS
       book at g=0.75/W, read OOS CAGR/Sharpe/MaxDD ONCE against RULES v2 and SPY.

KEEP PATHS: 4a (vs RULES v2 on the SAME panel) and 4b (vs SPY: Sharpe in both halves and
    OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's) evaluated for EVERY book.  Stated up
    front: a kernel-weighted draw is a diagnostic panel, NOT a rule anyone can trade, so a
    4b pass here is a diagnostic, never a capital candidate.

SURVIVORSHIP: universe_broad.json and the small panel are both CURRENT constituents, so
    every draw carries a survivorship premium; the small end carries more of it.  The
    premium is an arm-minus-arm difference on the SAME panel, so the level bias largely
    cancels, but it is restated beside the headline.

SAMPLE: the pooled index starts 2010-01-04 (the small cache's first bar), so pooled draws
    are read on 2011-01 .. 2026-09 after the 260-bar warm-up - 15.7 years, PROTOCOL rule 1
    satisfied.  The three real panels are restated on that SAME window beside their
    published (full-sample) numbers so the comparison is like-for-like.

PROTOCOL: 10 bps per unit turnover, next-day fills (engine), no shorting, no leverage.
Deterministic, standalone, no network.  Reads research/baseline.py; modifies nothing but its
own outputs: .grid.csv .rungs.csv .origin.csv .predict.csv .walkforward.csv .keeppaths.csv
.console.txt
"""
from __future__ import annotations
import sys, time, zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights  # noqa
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
LEVELS = {"cvol":    [0.25, 0.32, 0.39, 0.46, 0.53, 0.60],
          "breadth": [0.46, 0.52, 0.58, 0.64, 0.70]}
BW_MULT = 0.5                      # bandwidth = BW_MULT * sd(x) over pooled names
GAP = 0.0978                       # idea 51's published U56 - SMALL439 premium gap
FLOOR = 0.0745                     # idea 312's mean within-rung seed sd at k = 36
PARENT = "2026-09-09_is-the-panel-ordering-an-ETF-SHARE-effect_B.grid.csv"
PARENT_END = "2026-09-04"          # idea 312's / idea 51's last bar
G1_TOL, G1_TOL_U56, G2_TOL, PRED_TOL = 1e-9, 1e-4, 1e-12, 0.03

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


# ------------------------------------------------------------------ vectorised runner
def fast_backtest(prices, weights, cost_bps=COST, freq="W"):
    """Vectorised equivalent of engine.backtest (asserted in G2).  Idea 312's runner."""
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


def name_chars(pool):
    """Per-NAME characteristic on the pooled common window: annualised vol and MA breadth."""
    r = pool.pct_change()
    vol = (r.std() * np.sqrt(252)).astype(float)
    on = above_ma(pool) & pool.notna()
    br = (on.sum() / pool.notna().sum().replace(0, np.nan)).astype(float)
    return pd.DataFrame(dict(cvol=vol, breadth=br)).dropna()


def panel_chars(px, tradable, spy_r):
    """idea 312's panel_chars verbatim: constituent vol, pairwise corr, MA breadth, beta."""
    cols = [c for c in px.columns if c in tradable]
    r = px[cols].pct_change()
    vol = float((r.std() * np.sqrt(252)).mean())
    C = r.corr().to_numpy()
    n = C.shape[0]
    rho = float((np.nansum(C) - n) / (n * (n - 1))) if n > 1 else np.nan
    on = above_ma(px[cols]) & px[cols].notna()
    breadth = float(on.sum(axis=1).div(px[cols].notna().sum(axis=1).replace(0, np.nan)).mean())
    ew = r.mean(axis=1).fillna(0.0)
    sp = spy_r.reindex(ew.index).fillna(0.0)
    beta = float(np.cov(ew.values, sp.values)[0, 1] / np.var(sp.values)) if np.var(sp.values) > 0 else np.nan
    return dict(cvol=vol, rho=rho, breadth=breadth, beta=beta)


def feasible_band(x):
    """Mean of the 36 lowest / 36 highest values: the reach of a k=36 draw from this pool."""
    v = np.sort(np.asarray(x, float))
    return float(v[:K].mean()), float(v[-K:].mean())


def draw_panels(nc, bnames, snames):
    """Kernel-weighted k=36 draws at each (characteristic, level, flavour, seed)."""
    pools = {"POOL": list(nc.index),
             "BONLY": [c for c in nc.index if c in bnames],
             "SONLY": [c for c in nc.index if c in snames]}
    out, feas = {}, []
    for char, levels in LEVELS.items():
        h = BW_MULT * float(nc[char].std())
        for fl in FLAVOURS:
            names = np.array(pools[fl])
            x = nc.loc[names, char].to_numpy()
            lo, hi = feasible_band(x)
            for L in levels:
                ok = lo <= L <= hi
                feas.append(dict(char=char, flavour=fl, level=L, reach_lo=lo, reach_hi=hi,
                                 feasible=ok, bandwidth=h, n_pool=len(names)))
                if not ok:
                    continue
                for sd in SEEDS:
                    seed = zlib.crc32(f"CHAR|{char}|{L:.3f}|{fl}|{sd}".encode()) % (2 ** 32)
                    rng = np.random.default_rng(seed)
                    w = np.exp(-0.5 * ((x - L) / h) ** 2)
                    w = w / w.sum()
                    pick = sorted(rng.choice(names, size=K, replace=False, p=w).tolist())
                    out[f"{char}~{fl}~L{L:.3f}~{sd}"] = dict(
                        names=pick, char=char, flavour=fl, level=L, seed=sd)
    return out, pd.DataFrame(feas)


# ==================================================================================== run
def main():
    t0 = time.time()
    P("=" * 112)
    P("IDEA 568  can-any-B136-recomposition-reach-SMALL439-s-CHARACTERISTIC-SUPPORT  (lane C, 2026-09-09)")
    P("=" * 112)
    P("Treatment = idea 51's MA-gate SELECTION premium, Sharpe(MA-RS) - Sharpe(EWall) at matched")
    P("(gross, cadence).  Draws are kernel-weighted on the CHARACTERISTIC from the pooled")
    P("B136 + SMALL439 name pool; k is pinned at 36.  10 bps, t+1 fills, no leverage/shorting.")
    P(f"Pre-registered: GAP {GAP:.4f} (published), FLOOR {FLOOR:.4f} (idea 312 within-rung sd).")
    P("")

    # ---------------------------------------------------------------- G1 reproduction
    P("=" * 112)
    P("G1  REPRODUCTION GATE - idea 312's committed grid.csv REAL rows (36 rows x 13 columns)")
    P("=" * 112)
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
    diffs = {c: float(np.abs(m[c] - m[c + "_p"]).max()) for c in cmpcols}
    perp = m.assign(d=np.abs(m[cmpcols].values - m[[c + '_p' for c in cmpcols]].values).max(1)) \
            .groupby("panel").d.max()
    P(f"  rows matched: {len(m)}/36   max abs diff over {len(cmpcols)} columns: {max(diffs.values()):.3e}")
    P("  per panel: " + "  ".join(f"{k} {v:.2e}" for k, v in perp.items()))
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
    P("=" * 112)
    P("G2  IDENTITY GATE - fast_backtest vs engine.backtest")
    P("=" * 112)
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
    P("=" * 112)
    P("THE POOL - B136 + SMALL439 on the common index")
    P("=" * 112)
    pxB, (_, trB) = panels["B136"][0], panels["B136"]
    pxS = panels[SMALLK][0]
    trS = panels[SMALLK][1]
    ix = pxB.index.intersection(pxS.index)
    bn = sorted([c for c in pxB.columns if c in trB and c != "SPY"])
    sn = sorted([c for c in pxS.columns if c in trS])
    pool = pd.concat([pxB.loc[ix, bn], pxS.loc[ix, sn]], axis=1).ffill()
    spy_pool = pxB.loc[ix, "SPY"]
    nc = name_chars(pool)
    bnames, snames = set(bn) & set(nc.index), set(sn) & set(nc.index)
    P(f"  pooled index {ix.min().date()} .. {ix.max().date()}  ({len(ix)} bars)")
    P(f"  names: B {len(bnames)}  SMALL {len(snames)}  total {len(nc)}")
    for ch in LEVELS:
        b_lo, b_hi = feasible_band(nc.loc[sorted(bnames), ch]); s_lo, s_hi = feasible_band(nc.loc[sorted(snames), ch])
        p_lo, p_hi = feasible_band(nc[ch])
        P(f"  {ch:8s} k=36 REACH   BONLY [{b_lo:.3f}, {b_hi:.3f}]   SONLY [{s_lo:.3f}, {s_hi:.3f}]"
          f"   POOL [{p_lo:.3f}, {p_hi:.3f}]   bandwidth {BW_MULT*float(nc[ch].std()):.4f}")

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
        P(f"    {nm:9s} cvol {ch['cvol']:.4f}  breadth {ch['breadth']:.4f}  rho {ch['rho']:.4f}  "
          f"beta {ch['beta']:.3f}  premium(full) {pub[nm]:+.4f}  premium(common) {np.mean(prem):+.4f}")
    gap_common = real_common["U56"]["prem_common"] - real_common[SMALLK]["prem_common"]
    P(f"    U56 - {SMALLK} gap on the common window: {gap_common:+.4f}  (full sample {gap_reread:+.4f})")

    # ---------------------------------------------------------------- H_SUPPORT
    P("")
    P("=" * 112)
    P("H_SUPPORT  - can a k=36 recomposition reach the anchor?")
    P("=" * 112)
    dr, FEAS = draw_panels(nc, bnames, snames)
    P(f"  rungs planned {len(FEAS)}, feasible {int(FEAS.feasible.sum())}, draws {len(dr)}")
    infeas = FEAS[~FEAS.feasible]
    if len(infeas):
        P("  INFEASIBLE rungs (flavour cannot reach the level with k=36):")
        for _, r in infeas.iterrows():
            P(f"    {r['char']:8s} {r['flavour']:6s} L={r['level']:.3f}  reach [{r['reach_lo']:.3f}, {r['reach_hi']:.3f}]")

    # ---------------------------------------------------------------- the ladder
    P("")
    P("=" * 112)
    P("THE LADDER - premium on kernel-matched k=36 draws")
    P("=" * 112)
    grid, chars = [], []
    for key, d in dr.items():
        cols = list(dict.fromkeys(d["names"] + ["SPY"]))
        pxd = pd.concat([pool[d["names"]], spy_pool.rename("SPY")], axis=1)[cols].dropna(how="all").ffill()
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
                               achieved=ch[d["char"]], cvol=ch["cvol"], breadth=ch["breadth"],
                               rho=ch["rho"], beta=ch["beta"], n_from_B=nb)
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
        achieved=("achieved", "first"), cvol=("cvol", "first"), breadth=("breadth", "first"),
        n_from_B=("n_from_B", "first")).reset_index()
    rung = draw_prem.groupby(["char", "flavour", "level"]).agg(
        n=("premium", "size"), achieved=("achieved", "mean"),
        cvol=("cvol", "mean"), breadth=("breadth", "mean"), n_from_B=("n_from_B", "mean"),
        premium=("premium", "mean"), sd=("premium", "std"),
        prem_IS=("prem_IS", "mean"), prem_OOS=("prem_OOS", "mean")).reset_index()
    P("")
    P("  RUNGS (premium = mean over 6 seeds x 3 gross x 2 cadence; sd = across seeds)")
    P("  " + f"{'char':8s} {'flavour':7s} {'L':>6s} {'achieved':>9s} {'cvol':>7s} {'breadth':>8s} "
        f"{'nB/36':>6s} {'premium':>9s} {'sd':>7s} {'IS':>8s} {'OOS':>8s}")
    for _, r in rung.iterrows():
        P("  " + f"{r['char']:8s} {r['flavour']:7s} {r['level']:6.3f} {r['achieved']:9.4f} "
            f"{r['cvol']:7.4f} {r['breadth']:8.4f} {r['n_from_B']:6.1f} {r['premium']:+9.4f} "
            f"{r['sd']:7.4f} {r['prem_IS']:+8.4f} {r['prem_OOS']:+8.4f}")

    floor_here = float(rung.sd.mean())
    P("")
    P(f"  NOISE FLOOR recomputed here: mean within-rung seed sd = {floor_here:.4f} "
      f"({floor_here/GAP:.2f}x the published GAP; idea 312 got {FLOOR:.4f})")

    # H_SUPPORT verdict from ACHIEVED draw-level characteristics
    ach = draw_prem.groupby("char").achieved
    sup = {}
    for ch_ in LEVELS:
        a = draw_prem[(draw_prem.char == ch_) & (draw_prem.flavour == "POOL")].achieved
        sup[ch_] = (float(a.min()), float(a.max()))
    h_support = (sup["cvol"][0] <= 0.32 and sup["cvol"][1] >= 0.55 and
                 sup["breadth"][1] >= 0.68 and sup["breadth"][0] <= 0.48)
    P(f"  POOL draw-level support: cvol [{sup['cvol'][0]:.4f}, {sup['cvol'][1]:.4f}]  "
      f"breadth [{sup['breadth'][0]:.4f}, {sup['breadth'][1]:.4f}]")
    P(f"  anchors: SMALL cvol {real_common[SMALLK]['cvol']:.4f} breadth {real_common[SMALLK]['breadth']:.4f} | "
      f"B136 cvol {real_common['B136']['cvol']:.4f} breadth {real_common['B136']['breadth']:.4f} | "
      f"idea 312 ETF ladder cvol 0.21-0.31 breadth 0.67-0.71")
    P(f"  H_SUPPORT: {'PASS' if h_support else 'FAIL'}  (bar: cvol <=0.32 and >=0.55, breadth >=0.68 and <=0.48)")

    # ---------------------------------------------------------------- H_CHAR / H_NOISE
    P("")
    P("=" * 112)
    P("H_CHAR / H_NOISE  - is the premium a function of the characteristic?")
    P("=" * 112)
    slopes = []
    for ch_ in LEVELS:
        for fl in FLAVOURS:
            d = draw_prem[(draw_prem.char == ch_) & (draw_prem.flavour == fl)]
            if d.level.nunique() < 3:
                continue
            a, b, r2 = ols(d.achieved, d.premium)
            span = float(d.achieved.max() - d.achieved.min())
            rr = rung[(rung.char == ch_) & (rung.flavour == fl)].sort_values("achieved")
            mono_dn = bool((rr.premium.diff().dropna() <= 0).all())
            mono_up = bool((rr.premium.diff().dropna() >= 0).all())
            slopes.append(dict(char=ch_, flavour=fl, n=len(d), intercept=a, slope=b, r2=r2,
                               span=span, effect=b * span, sd_within=float(rr.sd.mean()),
                               ratio_to_GAP=abs(b * span) / GAP, mono_down=mono_dn, mono_up=mono_up))
    SL = pd.DataFrame(slopes)
    P("  " + f"{'char':8s} {'flavour':7s} {'n':>4s} {'slope':>9s} {'R2':>7s} {'span':>7s} "
        f"{'slope*span':>11s} {'|eff|/GAP':>10s} {'sd_within':>10s} {'mono':>8s}")
    for _, r in SL.iterrows():
        mono = "down" if r["mono_down"] else ("up" if r["mono_up"] else "-")
        P("  " + f"{r['char']:8s} {r['flavour']:7s} {r['n']:4.0f} {r['slope']:+9.4f} {r['r2']:7.4f} "
            f"{r['span']:7.4f} {r['effect']:+11.4f} {r['ratio_to_GAP']:10.2f} {r['sd_within']:10.4f} {mono:>8s}")

    pool_cv = SL[(SL.char == "cvol") & (SL.flavour == "POOL")].iloc[0]
    pool_br = SL[(SL.char == "breadth") & (SL.flavour == "POOL")].iloc[0]
    h_char = bool(pool_cv["mono_down"] and pool_br["mono_up"] and
                  pool_cv["effect"] <= -0.5 * GAP and pool_br["effect"] >= 0.5 * GAP)
    h_noise = bool(abs(pool_cv["effect"]) > pool_cv["sd_within"] and
                   abs(pool_br["effect"]) > pool_br["sd_within"])
    P(f"  H_CHAR : {'PASS' if h_char else 'FAIL'}  (monotone in the published direction AND |slope*span| >= 0.5*GAP = {0.5*GAP:.4f})")
    P(f"  H_NOISE: {'PASS' if h_noise else 'FAIL'}  (POOL effects cvol {pool_cv['effect']:+.4f} vs sd {pool_cv['sd_within']:.4f}; "
      f"breadth {pool_br['effect']:+.4f} vs sd {pool_br['sd_within']:.4f})")

    # ---------------------------------------------------------------- H_ORIGIN
    P("")
    P("=" * 112)
    P("H_ORIGIN  - at MATCHED characteristic level, does the panel of origin still separate?")
    P("=" * 112)
    orig = []
    for ch_ in LEVELS:
        for L in LEVELS[ch_]:
            d = rung[(rung.char == ch_) & (rung.level == L)].set_index("flavour")
            if not {"BONLY", "SONLY"} <= set(d.index):
                continue
            db, ds = d.loc["BONLY"], d.loc["SONLY"]
            sd_pair = float(np.sqrt((db["sd"] ** 2 + ds["sd"] ** 2) / 2))
            gap_bs = float(db["premium"] - ds["premium"])
            orig.append(dict(char=ch_, level=L, achieved_B=db["achieved"], achieved_S=ds["achieved"],
                             prem_B=db["premium"], prem_S=ds["premium"], gap=gap_bs,
                             sd_pair=sd_pair, t=gap_bs / (sd_pair / np.sqrt(len(SEEDS))) if sd_pair > 0 else np.nan,
                             within_floor=abs(gap_bs) <= sd_pair, ratio_to_GAP=gap_bs / GAP))
    OR = pd.DataFrame(orig)
    if len(OR):
        P("  " + f"{'char':8s} {'L':>6s} {'achB':>7s} {'achS':>7s} {'premB':>8s} {'premS':>8s} "
            f"{'B-S':>8s} {'sd':>7s} {'t':>7s} {'(B-S)/GAP':>10s}")
        for _, r in OR.iterrows():
            P("  " + f"{r['char']:8s} {r['level']:6.3f} {r['achieved_B']:7.4f} {r['achieved_S']:7.4f} "
                f"{r['prem_B']:+8.4f} {r['prem_S']:+8.4f} {r['gap']:+8.4f} {r['sd_pair']:7.4f} "
                f"{r['t']:+7.2f} {r['ratio_to_GAP']:+10.2f}")
        h_origin = bool(OR.within_floor.all())
        P(f"  H_ORIGIN: {'PASS' if h_origin else 'FAIL'}  "
          f"({int(OR.within_floor.sum())}/{len(OR)} matched rungs have |B-S| inside the seed sd; "
          f"mean B-S {OR.gap.mean():+.4f} = {OR.gap.mean()/GAP:+.2f}x GAP)")
    else:
        h_origin = None
        P("  H_ORIGIN: NO OVERLAPPING RUNG - BONLY and SONLY reach disjoint level sets at k=36.")

    # ---------------------------------------------------------------- H_PRED
    P("")
    P("=" * 112)
    P("H_PRED  - does the POOL fit predict the three real panels' published premia?")
    P("=" * 112)
    pred = []
    for ch_ in LEVELS:
        row = SL[(SL.char == ch_) & (SL.flavour == "POOL")].iloc[0]
        for nm, rc in real_common.items():
            yhat = row["intercept"] + row["slope"] * rc[ch_]
            for tgt, lbl in ((rc["prem_common"], "common"), (rc["prem_full"], "full")):
                pred.append(dict(char=ch_, panel=nm, x=rc[ch_], pred=yhat, actual=tgt,
                                 window=lbl, resid=tgt - yhat))
    PR = pd.DataFrame(pred)
    for ch_ in LEVELS:
        d = PR[(PR.char == ch_) & (PR.window == "common")].set_index("panel")
        order_ok = bool(d.loc["U56", "pred"] > d.loc["B136", "pred"] > d.loc[SMALLK, "pred"])
        P(f"  {ch_}: predicted  " + "  ".join(f"{k} {v:+.4f}" for k, v in d["pred"].items()) +
          f"   ordering U56>B136>{SMALLK}: {order_ok}")
        P(f"         actual(common) " + "  ".join(f"{k} {v:+.4f}" for k, v in d["actual"].items()) +
          f"   max|resid| {d.resid.abs().max():.4f}")
    h_pred = bool(all(
        (PR[(PR.char == c) & (PR.window == "common")].set_index("panel").pred.loc["U56"] >
         PR[(PR.char == c) & (PR.window == "common")].set_index("panel").pred.loc["B136"] >
         PR[(PR.char == c) & (PR.window == "common")].set_index("panel").pred.loc[SMALLK]) and
        PR[(PR.char == c) & (PR.window == "common")].resid.abs().max() <= PRED_TOL
        for c in LEVELS))
    P(f"  H_PRED: {'PASS' if h_pred else 'FAIL'}  (ordering reproduced AND max|resid| <= {PRED_TOL})")

    # ---------------------------------------------------------------- RULE 8
    P("")
    P("=" * 112)
    P("RULE 8 WALK-FORWARD   IS <= %s, OOS >= %s (read once)" % (IS_END, OOS_START))
    P("=" * 112)
    wf = []
    P("  WF-A  the ANSWER's slope refit inside each window")
    for ch_ in LEVELS:
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
            P(f"    {ch_:8s} {fl:6s}  IS {b_is:+8.4f} (R2 {r2_is:.3f})   OOS {b_oos:+8.4f} "
              f"(R2 {r2_oos:.3f})   full {b_full:+8.4f}   sign holds: {hold}")

    P("")
    P("  WF-B  a BOOK: pick (char, level) by IS Sharpe of the seed-pooled MA-RS book at g=0.75/W")
    sel = G[(G.arm == "MA-RS") & (G.gross == 0.75) & (G.cadence == "W") & (G.flavour == "POOL")]
    pick_tbl = sel.groupby(["char", "level"]).agg(IS_Sharpe=("IS_Sharpe", "mean"),
                                                  OOS_Sharpe=("OOS_Sharpe", "mean")).reset_index()
    for _, r in pick_tbl.sort_values("IS_Sharpe", ascending=False).iterrows():
        P(f"    {r['char']:8s} L={r['level']:.3f}  IS {r['IS_Sharpe']:+.4f}   (OOS {r['OOS_Sharpe']:+.4f})")
    best = pick_tbl.sort_values("IS_Sharpe", ascending=False).iloc[0]
    P(f"    PICK (IS only): {best['char']} L={best['level']:.3f}")

    keys_pick = [k for k, d in dr.items()
                 if d["char"] == best["char"] and abs(d["level"] - best["level"]) < 1e-9 and d["flavour"] == "POOL"]
    rets_pick = []
    for key in keys_pick:
        d = dr[key]
        pxd = pd.concat([pool[d["names"]], spy_pool.rename("SPY")], axis=1).dropna(how="all").ffill()
        st = pxd.index[260]
        w = make_books(pxd, set(d["names"]), 0.75)["MA-RS"]
        rets_pick.append(fast_backtest(pxd, w, COST, "W")["returns"].loc[st:])
    RP = pd.concat(rets_pick, axis=1).fillna(0.0).mean(axis=1)     # equal-weight over the 6 draws
    st_b = pxB.index[260]
    b136_v2 = backtest(pxB, rules_v2_weights(pxB), cost_bps=COST, freq="W")["returns"].loc[st_b:].reindex(RP.index).fillna(0.0)
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
    P("=" * 112)
    P("KEEP PATHS over every book (4a vs RULES v2 on the SAME panel, 4b vs SPY)")
    P("=" * 112)
    ALL = pd.concat([REAL.assign(char="-", flavour="REAL", level=np.nan, seed=-1), G],
                    ignore_index=True, sort=False)
    P(f"  books: {len(ALL)} ({len(REAL)} REAL + {len(G)} DRAW)")
    P(f"  4a passes {int(ALL.keep4a.sum())}/{len(ALL)}   4b passes {int(ALL.keep4b.sum())}/{len(ALL)}   "
      f"BOTH {int((ALL.keep4a & ALL.keep4b).sum())}/{len(ALL)}")
    legs = pd.Series([x for s in ALL.loc[~ALL.keep4b, "fail4b"] for x in s.split(",")]).value_counts()
    P("  binding 4b legs: " + "  ".join(f"{k} {v}" for k, v in legs.items()))
    if int(ALL.keep4b.sum()):
        bb = ALL[ALL.keep4b].sort_values("Sharpe", ascending=False).head(5)
        P("  top 4b passers (DIAGNOSTIC ONLY - a kernel draw is not a tradable rule):")
        for _, r in bb.iterrows():
            P(f"    {str(r['panel'])[:34]:34s} {r['arm']:6s} g={r['gross']:.2f} {r['cadence']}  "
              f"CAGR {r['CAGR']:6.2%}  Sh {r['Sharpe']:.3f}  DD {r['MaxDD']:7.2%}  "
              f"H1/H2 {r['H1']:.2f}/{r['H2']:.2f}  OOS {r['OOS_Sharpe']:.3f}")
    KP = ALL[["panel", "kind", "arm", "gross", "cadence", "char", "flavour", "level", "seed",
              "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
              "keep4a", "fail4b", "keep4b"]]

    # ---------------------------------------------------------------- verdict
    P("")
    P("=" * 112)
    P("VERDICT")
    P("=" * 112)
    P(f"  H_SUPPORT {'PASS' if h_support else 'FAIL'}   H_CHAR {'PASS' if h_char else 'FAIL'}   "
      f"H_NOISE {'PASS' if h_noise else 'FAIL'}   "
      f"H_ORIGIN {'PASS' if h_origin else ('FAIL' if h_origin is False else 'N/A')}   "
      f"H_PRED {'PASS' if h_pred else 'FAIL'}")

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
    P("")
    P(f"  wrote {STAMP}.{{grid,rungs,origin,predict,walkforward,keeppaths,chars}}.csv   ({time.time()-t0:.0f}s)")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()

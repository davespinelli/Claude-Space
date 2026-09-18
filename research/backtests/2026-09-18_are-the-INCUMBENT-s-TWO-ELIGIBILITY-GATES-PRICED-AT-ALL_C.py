#!/usr/bin/env python3
"""
Idea 1339 (lane C, 2026-09-18) — are the INCUMBENT's TWO ELIGIBILITY GATES PRICED AT ALL?

THE PREMISE, READ FROM THE RECORD.  Every 4b pass in this family is built on a selection
frame inherited wholesale from RULES v1's scorer (research/baseline.py: `score` /
`rules_v1_weights`): a name is eligible on day t only if

    (i)  price > its own 200-day moving average           ("MA GATE"), and
    (ii) 20-day annualised vol < 0.60                     ("MAXVOL").

Neither number was ever chosen by a backtest in this record.  0.60 and the MA gate were
written into v1's scorer and have been carried, untouched, into every N / H / GROSS /
CADENCE / phase / lag / cost ladder since.  They are TWO FREE PARAMETERS the record has been
spending without counting.  Idea 1305 has just shown the same thing is true of the CADENCE
coordinate (its W->M step costs U56 -0.1053 of Sharpe, not the free rebate the record
assumed), so the prior that an "inherited default" is harmless is already falsified once.

WHAT IS BEING MEASURED, STATED BEFORE ANY NUMBER IS READ.  The frozen incumbent book
(N=15, H=126, GROSS=0.60, CADENCE=W, 10 bps, decide-at-t / apply-at-t+1) is rebuilt at every
point of

    MAXVOL  in {0.30, 0.45, 0.60, 0.80, NONE}      DIAL 1  (NONE = no vol gate at all)
    MAGATE  in {ON, OFF}                           DIAL 2

10 cells per panel, 3 panels, 30 real books, EVERY ONE published in `.grid.csv`.  Exactly two
tuned parameters (PROTOCOL rule 4); nothing else moves.

WHAT IS *NOT* BEING WALKED, AND WHY.  `above` enters the record's mechanism TWICE: once as the
eligibility filter (i), and once as a multiplicative tilt inside the composite score itself
(`s = comp * (0.5 + 0.5*above)`).  This run walks the ELIGIBILITY GATE ONLY and leaves the
scorer's tilt frozen at every cell, because the tilt is part of the composite being ranked,
not a gate.  MAGATE=OFF therefore means "an under-200d name may be BOUGHT", not "the score
stops caring about the 200d line".  Stated here so the MAGATE=OFF column is not misread as a
bigger change than it is.

PRE-DECLARED OUTCOMES, fixed before the grid was run:
  (A) COORDINATE — the incumbent cell (0.60, ON) passes 4b on U56 and one notch on either
      dial breaks it.  Then the committed pass is a property of two numbers nobody chose.
  (B) PLATEAU — the 4b verdict is unchanged across a contiguous majority of the 10 cells.
      Then the gates are inert dials and the pass is not about them.
  (C) DOMINATED — some non-incumbent cell passes 4b where the incumbent fails, on the same
      panel.  Then the inherited defaults are actively costing the book.
  (D) DEAD EVERYWHERE — no cell passes 4b on any panel.
All four are reported; none is selected on.  A KEEP is taken only if rule 8 licenses it.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9 survivorship); the 4a and
4b legs; the IS and OOS windows; mean eligible-name count and annualised turnover per cell
(so a verdict change can be attributed to the gate's mechanical effect, not guessed at).

PROTOCOL: rule 2 execution (t+1) and 10 bps; rule 3 compare against live RULES v2 AND SPY;
rule 4 both KEEP paths at every cell, max 2 params; rule 8 walk-forward — the (MAXVOL, MAGATE)
cell is chosen on warm-up..2016-12-31 ONLY by IS Sharpe and 2017-2026 is read ONCE, against
the PROTOCOL-default cell (0.60, ON) which nobody had to choose; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

Runs standalone and offline (committed price caches only; no network):
  python research/backtests/2026-09-18_are-the-INCUMBENT-s-TWO-ELIGIBILITY-GATES-PRICED-AT-ALL_C.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-18"
SLUG = "are-the-INCUMBENT-s-TWO-ELIGIBILITY-GATES-PRICED-AT-ALL"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP = 260
REF_COST = 10.0
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G, I_C = 15, 126, 0.60, "W"          # the frozen incumbent
MAXVOLS = [0.30, 0.45, 0.60, 0.80, None]          # DIAL 1
MAGATES = [True, False]                           # DIAL 2
DEFAULT_CELL = (0.60, True)                       # what PROTOCOL/RULES v1 hands you, unchosen
LIVE_MAXDD_COMMITTED = -0.1205

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=value, target=target, pass_=bool(ok)))
    return bool(ok)


def vlab(v):
    return "NONE" if v is None else f"{v:.2f}"


def clab(mv, mg):
    return f"MAXVOL={vlab(mv)}/MA={'ON' if mg else 'OFF'}"


# ==================================================================== mechanism (the record's)
def mech(q):
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = (q > q.rolling(200).mean()).values
    vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
    sc = (comp * (0.5 + 0.5 * above.astype(float))).values      # TILT FROZEN at every cell
    return sc, above, np.nan_to_num(vol20, nan=1e9)


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        m = rebalance_mask(px.index, I_C).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        self.idx = px.index
        self.i0 = WARMUP
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.above, self.vol20 = above, vol20
        self.spy = px["SPY"].pct_change().fillna(0.0).values

    def elig(self, maxvol, magate):
        e = np.ones_like(self.above) if maxvol is None else (self.vol20 < maxvol)
        return (e & self.above) if magate else e


def build1(pan, elig, N, H):
    """The record's min-hold selection frame at GROSS = 1.0, decide at t-1 / apply at t
    (rule 2).  Row t is the APPLICATION-time weight."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    reb = pan.reb
    for i, t in enumerate(reb):
        ts = max(t - 1, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = pan.rank_key[ts].copy()
            k[~(elig[ts] & pr[ts])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def nrun(pan, Wt):
    """Gross daily returns and one-way turnover; costs applied afterwards (gate G2)."""
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    reb = pan.reb
    ends = np.append(reb[1:], T)
    for i0, i1 in zip(reb, ends):
        w0 = Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return (held * rets).sum(axis=1), turn


def at_cost(gr, tu, c=REF_COST):
    return gr - tu * c / 1e4


# ==================================================================== metrics
def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mdd(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min()) if len(e) else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    e = np.cumprod(1 + r)
    return float(e[-1] ** (252 / len(r)) - 1)


def triple(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def bmpack(r):
    h1, h2 = halves(r)
    m = triple(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


def keep_paths(r, bm, live):
    """4a vs the live RULES v2 book; 4b vs SPY (both legs of each, PROTOCOL rule 4)."""
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    k4b = bool(h1 > bm["H1"] and h2 > bm["H2"]
               and m["MaxDD"] >= DD_CAP * bm["MaxDD"]
               and m["CAGR"] >= CAGR_FLOOR * bm["CAGR"])
    return k4a, k4b, m, h1, h2


def annturn(tu, lo, hi):
    n = hi - lo
    return float(np.sum(tu[lo:hi]) * 252.0 / n) if n > 0 else np.nan


# ==================================================================== world
def make_panels():
    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and mv[c] < 1.0]
    return [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
            Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
            Panel("SMALL", pxS, inv)], (pxU, pxB, pxS)


def main():
    t0 = time.time()
    say("=" * 108)
    say(f"IDEA 1339 (lane C, {DATE}) — are the INCUMBENT's TWO ELIGIBILITY GATES PRICED AT ALL?")
    say(f"  FROZEN INCUMBENT: N={I_N} H={I_H} GROSS={I_G:.2f} CADENCE={I_C} cost={REF_COST:.0f}bps")
    say(f"  DIAL 1 MAXVOL {[vlab(v) for v in MAXVOLS]}   DIAL 2 MAGATE ['ON', 'OFF']")
    say(f"  PROTOCOL-default (unchosen) cell: {clab(*DEFAULT_CELL)}")
    say("=" * 108)

    panels, (pxU, pxB, pxS) = make_panels()
    for p in panels:
        say(f"  PANEL {p.name:6s} {len(p.invest):4d} investables, "
            f"{p.idx[0].date()} -> {p.idx[-1].date()}, {len(p.idx)} rows, "
            f"{len(p.reb)} weekly rebalances")
    yrs = (panels[0].idx[-1] - panels[0].idx[0]).days / 365.25
    gate("G0 sample >= 10 years", round(yrs, 2), 10.0, yrs >= 10.0)

    # ---------------------------------------------------------------- build every cell
    say("-" * 108)
    say("BUILDING 30 BOOKS (3 panels x 5 MAXVOL x 2 MAGATE) ...")
    books, bench = {}, {}
    for pan in panels:
        b = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=REF_COST, freq="W")
        bench[pan.name] = dict(spy=pan.spy, live=b["returns"].values)
        for mv in MAXVOLS:
            for mg in MAGATES:
                el = pan.elig(mv, mg)
                W = I_G * build1(pan, el, I_N, I_H)
                gr, tu = nrun(pan, W)
                nelig = float(np.mean((el & pan.priced[:, pan.iinv])[WARMUP:].sum(axis=1)))
                books[(pan.name, mv, mg)] = dict(gr=gr, tu=tu, nelig=nelig, W=W)
        say(f"    {pan.name:6s} 10 cells built   ({time.time()-t0:.0f}s)")

    # ---------------------------------------------------------------- machinery gates
    pan = panels[0]
    kd = ("U56",) + DEFAULT_CELL
    Wd = books[kd]["W"]
    Wdf = pd.DataFrame(Wd, index=pan.idx, columns=pan.px.columns)
    eng = backtest(pan.px, Wdf.shift(-1).fillna(0.0), cost_bps=REF_COST, freq="W")["returns"].values
    g2 = float(np.nanmax(np.abs(eng[WARMUP:] - at_cost(books[kd]["gr"], books[kd]["tu"])[WARMUP:])))
    gate("G2 r(c) = gross - turn*c/1e4 == engine.backtest at the reference rung", g2, 1e-10,
         g2 < 1e-10)
    lmv = mdd(bench["U56"]["live"][WARMUP:])
    gate("G3 live RULES v2 U56 MaxDD == the record's committed -12.05%", round(lmv, 6),
         LIVE_MAXDD_COMMITTED, abs(lmv - LIVE_MAXDD_COMMITTED) < 5e-4)
    # G1: the default cell IS the record's inherited frame (vol20 < 0.60 AND above-200d)
    el_rec = (pan.vol20 < 0.60) & pan.above
    g1 = int(np.sum(el_rec != pan.elig(*DEFAULT_CELL)))
    gate("G1 default cell's eligibility == RULES v1's (above & vol20<0.60), cell-for-cell",
         g1, 0, g1 == 0)
    say(f"    G1 {g1} differing cells   G2 {g2:.3e}   G3 live U56 MaxDD {lmv:.4%}")

    # ---------------------------------------------------------------- the 30-cell grid
    say("-" * 108)
    say("THE GRID — all 30 cells, full sample (warm-up..end), 10 bps, both KEEP paths")
    rows = []
    for pan in panels:
        lo, hi = pan.i0, len(pan.rets)
        bm = bmpack(pan.spy[lo:hi])
        lv = bmpack(bench[pan.name]["live"][lo:hi])
        say(f"\n  PANEL {pan.name}   SPY {bm['CAGR']:7.2%} / {bm['Sharpe']:.4f} / "
            f"{bm['MaxDD']:7.2%} (H1 {bm['H1']:.4f} H2 {bm['H2']:.4f})   "
            f"LIVE v2 {lv['CAGR']:7.2%} / {lv['Sharpe']:.4f} / {lv['MaxDD']:7.2%}")
        say(f"    {'CELL':28s} {'CAGR':>8s} {'Sharpe':>8s} {'MaxDD':>8s} {'H1':>8s} {'H2':>8s} "
            f"{'nElig':>7s} {'turn/y':>7s}  4a  4b")
        for mv in MAXVOLS:
            for mg in MAGATES:
                bk = books[(pan.name, mv, mg)]
                r = at_cost(bk["gr"], bk["tu"])[lo:hi]
                k4a, k4b, m, h1, h2 = keep_paths(r, bm, lv)
                tn = annturn(bk["tu"], lo, hi)
                rows.append(dict(panel=pan.name, maxvol=vlab(mv), magate="ON" if mg else "OFF",
                                 is_default=(mv, mg) == DEFAULT_CELL,
                                 CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                 H1=h1, H2=h2, n_elig=bk["nelig"], turnover_yr=tn,
                                 spy_CAGR=bm["CAGR"], spy_Sharpe=bm["Sharpe"], spy_MaxDD=bm["MaxDD"],
                                 live_Sharpe=lv["Sharpe"], live_MaxDD=lv["MaxDD"],
                                 keep_4a=k4a, keep_4b=k4b,
                                 leg_H1=h1 > bm["H1"], leg_H2=h2 > bm["H2"],
                                 leg_DD=m["MaxDD"] >= DD_CAP * bm["MaxDD"],
                                 leg_CAGR=m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
                mark = " <- PROTOCOL DEFAULT" if (mv, mg) == DEFAULT_CELL else ""
                say(f"    {clab(mv, mg):28s} {m['CAGR']:8.2%} {m['Sharpe']:8.4f} {m['MaxDD']:8.2%} "
                    f"{h1:8.4f} {h2:8.4f} {bk['nelig']:7.1f} {tn:7.2f}  "
                    f"{'Y' if k4a else '.'}   {'Y' if k4b else '.'}{mark}")
    grid = pd.DataFrame(rows)
    grid.to_csv(f"{OUT}.grid.csv", index=False)
    gate("G5 every grid cell published", len(grid), 30, len(grid) == 30)

    # ---------------------------------------------------------------- rule 8 walk-forward
    say("-" * 108)
    say("RULE 8 WALK-FORWARD — cell chosen on warm-up..2016-12-31 by IS Sharpe; 2017-2026 read ONCE")
    wf = []
    for pan in panels:
        i1 = int(pan.idx.searchsorted(pd.Timestamp(OOS_START)))
        lo, hi = pan.i0, len(pan.rets)
        bm_o, lv_o = bmpack(pan.spy[i1:hi]), bmpack(bench[pan.name]["live"][i1:hi])
        bm_f, lv_f = bmpack(pan.spy[lo:hi]), bmpack(bench[pan.name]["live"][lo:hi])
        iss = {}
        for mv in MAXVOLS:
            for mg in MAGATES:
                bk = books[(pan.name, mv, mg)]
                iss[(mv, mg)] = sharpe(at_cost(bk["gr"], bk["tu"])[lo:i1])
        pick = max(iss, key=lambda k: (iss[k] if np.isfinite(iss[k]) else -np.inf))
        say(f"\n  PANEL {pan.name}  IS window {pan.idx[lo].date()} -> {pan.idx[i1-1].date()} "
            f"({i1-lo} rows)   OOS {pan.idx[i1].date()} -> {pan.idx[-1].date()} ({hi-i1} rows)")
        say("    IS Sharpe by cell: " + "  ".join(
            f"{clab(*k)}={v:.4f}" for k, v in sorted(iss.items(), key=lambda x: -x[1])))
        say(f"    IS ARGMAX = {clab(*pick)}   |   PROTOCOL DEFAULT = {clab(*DEFAULT_CELL)}")
        say(f"    OOS SPY {bm_o['CAGR']:7.2%} / {bm_o['Sharpe']:.4f} / {bm_o['MaxDD']:7.2%}   "
            f"OOS LIVE v2 {lv_o['CAGR']:7.2%} / {lv_o['Sharpe']:.4f} / {lv_o['MaxDD']:7.2%}")
        for arm, cell in (("IS_ARGMAX", pick), ("PROTOCOL_DEFAULT", DEFAULT_CELL)):
            bk = books[(pan.name,) + tuple(cell)]
            oos = at_cost(bk["gr"], bk["tu"])[i1:hi]
            full = at_cost(bk["gr"], bk["tu"])[lo:hi]
            k4a, k4b, m, h1, h2 = keep_paths(oos, bm_o, lv_o)
            k4aF, k4bF, mF, h1F, h2F = keep_paths(full, bm_f, lv_f)
            wf.append(dict(panel=pan.name, arm=arm, maxvol=vlab(cell[0]),
                           magate="ON" if cell[1] else "OFF", IS_Sharpe=iss[tuple(cell)],
                           OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"],
                           OOS_H1=h1, OOS_H2=h2, OOS_keep_4a=k4a, OOS_keep_4b=k4b,
                           FULL_CAGR=mF["CAGR"], FULL_Sharpe=mF["Sharpe"], FULL_MaxDD=mF["MaxDD"],
                           FULL_keep_4a=k4aF, FULL_keep_4b=k4bF,
                           oos_spy_CAGR=bm_o["CAGR"], oos_spy_Sharpe=bm_o["Sharpe"],
                           oos_spy_MaxDD=bm_o["MaxDD"], oos_live_Sharpe=lv_o["Sharpe"],
                           oos_live_MaxDD=lv_o["MaxDD"],
                           oos_leg_H1=h1 > bm_o["H1"], oos_leg_H2=h2 > bm_o["H2"],
                           oos_leg_DD=m["MaxDD"] >= DD_CAP * bm_o["MaxDD"],
                           oos_leg_CAGR=m["CAGR"] >= CAGR_FLOOR * bm_o["CAGR"]))
            say(f"    {arm:17s} {clab(*cell):28s} OOS {m['CAGR']:7.2%} / {m['Sharpe']:.4f} / "
                f"{m['MaxDD']:7.2%}   4a {'Y' if k4a else '.'}  4b {'Y' if k4b else '.'}"
                f"  (legs H1 {'Y' if h1>bm_o['H1'] else '.'} H2 {'Y' if h2>bm_o['H2'] else '.'} "
                f"DD {'Y' if m['MaxDD']>=DD_CAP*bm_o['MaxDD'] else '.'} "
                f"CAGR {'Y' if m['CAGR']>=CAGR_FLOOR*bm_o['CAGR'] else '.'})")
        d = [w for w in wf if w["panel"] == pan.name]
        say(f"    CHOOSING COSTS: OOS Sharpe {d[0]['OOS_Sharpe']:.4f} (argmax) - "
            f"{d[1]['OOS_Sharpe']:.4f} (default) = {d[0]['OOS_Sharpe']-d[1]['OOS_Sharpe']:+.4f}")
    wfd = pd.DataFrame(wf)
    wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    gate("G4 the chooser reads no row at or after 2017-01-01 (IS slice ends at i1-1)",
         "by construction", "by construction", True)
    gate("G6 exactly two tuned parameters (MAXVOL, MAGATE)", 2, 2, True)

    # ---------------------------------------------------------------- verdict
    say("=" * 108)
    say("VERDICT")
    n4a, n4b = int(grid.keep_4a.sum()), int(grid.keep_4b.sum())
    say(f"  FULL-SAMPLE: 4a {n4a} of 30 cells; 4b {n4b} of 30 cells.")
    for pn in ["U56", "B136", "SMALL"]:
        g = grid[grid.panel == pn]
        d = g[g.is_default].iloc[0]
        say(f"    {pn:6s} 4b {int(g.keep_4b.sum())} of 10   |  default cell 4b "
            f"{'PASS' if d.keep_4b else 'FAIL'} "
            f"(legs H1 {'Y' if d.leg_H1 else '.'} H2 {'Y' if d.leg_H2 else '.'} "
            f"DD {'Y' if d.leg_DD else '.'} CAGR {'Y' if d.leg_CAGR else '.'})"
            f"  |  best cell by Sharpe: {g.loc[g.Sharpe.idxmax()].maxvol}/"
            f"{g.loc[g.Sharpe.idxmax()].magate} ({g.Sharpe.max():.4f} vs default "
            f"{d.Sharpe:.4f})")
    say(f"  OOS (read once): 4b {int(wfd.OOS_keep_4b.sum())} of {len(wfd)} arms; "
        f"4a {int(wfd.OOS_keep_4a.sum())} of {len(wfd)}.")
    dlt = [w["OOS_Sharpe"] for w in wf if w["arm"] == "IS_ARGMAX"]
    dfl = [w["OOS_Sharpe"] for w in wf if w["arm"] == "PROTOCOL_DEFAULT"]
    say(f"  RULE 8: mean OOS Sharpe IS_ARGMAX {np.mean(dlt):.4f} vs PROTOCOL_DEFAULT "
        f"{np.mean(dfl):.4f}  (choosing the gates in sample is worth "
        f"{np.mean(dlt)-np.mean(dfl):+.4f})")
    # outcome classification, pre-declared
    u = grid[grid.panel == "U56"]
    ud = u[u.is_default].iloc[0]
    others_pass = int(u[~u.is_default].keep_4b.sum())
    if not bool(ud.keep_4b) and others_pass > 0:
        oc = "(C) DOMINATED — a non-default gate cell passes 4b where the default fails"
    elif bool(ud.keep_4b) and others_pass == 0:
        oc = "(A) COORDINATE — only the inherited cell passes; one notch either way breaks it"
    elif int(grid.keep_4b.sum()) == 0:
        oc = "(D) DEAD EVERYWHERE — no cell passes 4b on any panel"
    else:
        oc = "(B) PLATEAU — the 4b verdict survives across several cells; the gates are not the pass"
    say(f"  PRE-DECLARED OUTCOME: {oc}")
    say("  SURVIVORSHIP (rule 9): U56 / B136 / SMALL are CURRENT-CONSTITUENT lists, so every "
        "absolute level here is an upper bound. The gate COMPARISONS are within-panel, "
        "same-names/same-days differences and are first-order immune; the 4b pass COUNTS are not.")

    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say("-" * 108)
    for g in GATES:
        say(f"  {'PASS' if g['pass_'] else 'FAIL'}  {g['gate']}  -> {g['value']} (target {g['target']})")
    say(f"  elapsed {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

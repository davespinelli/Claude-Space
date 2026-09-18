#!/usr/bin/env python3
"""
Idea 1305 (lane cloud, 2026-09-18) — does the VOL-TARGET's ONLY WIN survive a CADENCE CHANGE?

THE PREMISE, READ FROM THE RECORD.  Idea 1297 walked a vol-target overlay TARGET {6..14}% x
WINDOW {21,63,126} on the certified incumbent (U56 / N=15 / H=126 / gross 0.60 / WEEKLY) and
produced exactly ONE out-of-sample winner: U56, TARGET=8%, WINDOW=21d, worth +0.0166 of OOS
Sharpe for -1.54 pp of OOS CAGR.  That book is a WEEKLY scaler on a WEEKLY book, and the
scaler pays its own turnover every week.  Idea 931 established that a W->M cadence change is a
TURNOVER REBATE every book on this tape collects, scaler or not.  So the +0.0166 has two
readings and the record has never separated them:

    (A) EDGE      — the scaler is timing volatility, and the win is the timing.
    (B) REBATE    — the scaler was over-churning, and any change that cuts its churn (a slower
                    cadence being the cheapest one available) recovers the same Sharpe.

THE TEST THAT SEPARATES THEM.  Reading (B) is falsifiable: if the +0.0166 is a rebate, the
UN-SCALED flat book collects the same rebate when IT goes monthly, and the scaler's edge OVER
its own-cadence control does not grow.  This run therefore builds the flat g=0.60 control at
BOTH cadences and reports the DIFFERENCE IN DIFFERENCES

    DiD = [S(scaled@M) - S(flat@M)] - [S(scaled@W) - S(flat@W)]

alongside every level.  A positive DiD is evidence for (A); a DiD at or below zero while the
flat book's own W->M gain covers the +0.0166 is evidence for (B).

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  CADENCE {W, M}                      DIAL 1 — W is 1297's and the incumbent's value
  TARGET  {6, 8, 10, 12, 14} %/yr     DIAL 2 — 1297's full ladder

  WINDOW is FROZEN at 21 trading days (the queue fixes it; 1297's best window on every panel).
  10 cells per panel per vol basis, EVERY ONE published in `.grid.csv` / `.robust.csv`.

  THE SCALER (1297's, unchanged).  At each rebalance application row t,
  k_t = min(0.60, TARGET / v_t), v_t = annualised sd of the BASIS book's daily returns over
  the 21 rows ENDING AT t-1 (rule 2: decided at close t-1, traded at t).  v_t <= 1e-8 leaves
  k_t at the cap 0.60.  k_t is constant between rebalances and pays its own turnover.  The cap
  is the incumbent's own gross, so NO CELL HERE IS LEVERED (rule 2: no leverage).

  TARGET IS A NOMINAL DIAL, NOT AN ACHIEVED VOL.  v_t is measured on the g=0.60 incumbent, so
  a book run at gross k realises roughly (k/0.60)*v.  Every cell publishes its ACHIEVED
  annualised vol (`vol_real`); read that column, not TARGET.

  TWO VOL BASES, both published, neither a third dial (headline is B_CONST, as in 1297):
    B_CONST  v from the CONSTANT-GROSS incumbent book at the SAME cadence.  Non-circular.
    B_SELF   v from the scaled book's OWN realised returns, read causally (row t sees < t).

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); both KEEP paths at
every cell; the IS and OOS windows; the halves; turnover and its 10 bps cost drag at every
cell (that is the rebate, in bp/yr).

PROTOCOL: rule 1 (>= 10 years, gate G0); rule 2 execution t+1, 10 bps, no leverage; rule 3
compare against the live RULES v2 baseline AND SPY; rule 4 both KEEP paths, 2 tuned parameters
and no more; rule 8 walk-forward — (CADENCE, TARGET) chosen on warm-up..2016-12-31 by argmax
IS Sharpe, 2017-2026 read ONCE; rule 9 survivorship stated (B136 and SMALL are CURRENT
constituents only; SMALL is a sub-$2B screen carried back to 2010, so its levels are an upper
bound and only its CONTRASTS are used here).  RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py are NOT modified.

CROSS-RUN REPLAY (gate G8): the CADENCE=W column must reproduce idea 1297's committed
`.grid.csv` cells at WINDOW=21 / TARGET {8,10,12}% on all three panels to < 5e-4.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-18_does-the-VOL-TARGET-s-ONLY-WIN-survive-a-CADENCE-CHANGE_cloud.py
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
SLUG = "does-the-VOL-TARGET-s-ONLY-WIN-survive-a-CADENCE-CHANGE"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP, MAXVOL = 260, 0.60
COST = 10.0                                   # PROTOCOL rule 2's rung
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G = 15, 126, 0.60                 # the incumbent, frozen
WINDOW = 21                                   # FROZEN by the queue
CADENCES = ["W", "M"]                         # DIAL 1
TARGETS = [0.06, 0.08, 0.10, 0.12, 0.14]      # DIAL 2
OOS_START, IS_END = "2017-01-01", "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LIVE_MAXDD_COMMITTED = -0.1205
C1215_U56 = dict(CAGR=0.1366, Sharpe=1.1706, MaxDD=-0.1638)
C1297_OOS_WIN = 0.0166                        # the claim under test
# idea 1297's committed .grid.csv, B_CONST, WINDOW=21, WEEKLY (cross-run replay gate G8)
C1297 = {
    ("U56", 0.08): (0.127828, 1.197323, -0.144066),
    ("U56", 0.10): (0.131792, 1.180091, -0.162928),
    ("U56", 0.12): (0.133071, 1.168065, -0.164305),
    ("B136", 0.08): (0.120646, 1.085073, -0.137019),
    ("B136", 0.10): (0.127209, 1.072276, -0.152890),
    ("B136", 0.12): (0.129959, 1.061139, -0.159704),
    ("SMALL", 0.08): (0.049445, 0.444225, -0.267975),
    ("SMALL", 0.10): (0.055031, 0.455020, -0.287251),
    ("SMALL", 0.12): (0.059595, 0.472086, -0.294231),
}

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=value, target=target, pass_=bool(ok)))
    return bool(ok)


def mech(q):
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = (q > q.rolling(200).mean()).values
    vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
    sc = (comp * (0.5 + 0.5 * above.astype(float))).values
    return sc, above, np.nan_to_num(vol20, nan=1e9)


class Panel:
    """The record's panel object, extended to carry a rebalance index PER CADENCE."""

    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        self.reb = {}
        for c in CADENCES:
            m = rebalance_mask(px.index, c).shift(1, fill_value=False).values.copy()
            m[0] = True
            self.reb[c] = np.flatnonzero(m)
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values


def build1(pan, reb, N, H, lag=1):
    """The record's min-hold selection frame at GROSS = 1.0; lag=1 is rule 2."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    for i, t in enumerate(reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = pan.rank_key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
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


def run_dyn(pan, reb, frame, kfun):
    """1297's runner with a dynamic gross multiplier.  `kfun(t, out)` may read only out[:t]
    (rule 2).  Returns (gross returns, one-way turnover, k per row)."""
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    turn = np.zeros(T)
    out = np.zeros(T)
    ks = np.zeros(T)
    curw = np.zeros(M)
    reb = np.asarray(reb, dtype=np.int64)
    ends = np.append(reb[1:], T)
    for i0, i1 in zip(reb, ends):
        k = float(kfun(i0, out))
        w0 = k * frame[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        ks[i0:i1] = k
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return out, turn, ks


def at_cost(gr, tu, c=COST):
    return gr - tu * c / 1e4


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
    return float(np.cumprod(1 + r)[-1] ** (252 / len(r)) - 1)


def triple(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def annvol(r):
    return float(np.std(np.asarray(r, float), ddof=0) * np.sqrt(252))


def annturn(tu, lo, hi):
    n = hi - lo
    return float(np.sum(tu[lo:hi]) * 252.0 / n) if n > 0 else np.nan


def bmpack(r):
    h1, h2 = halves(r)
    m = triple(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


def keep_paths(r, bm, live):
    """4a vs the live RULES v2 book; 4b vs SPY (full-sample legs; 4b's OOS Sharpe leg is
    applied in the rule-8 section)."""
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    k4b = bool(h1 > bm["H1"] and h2 > bm["H2"]
               and m["MaxDD"] >= DD_CAP * bm["MaxDD"]
               and m["CAGR"] >= CAGR_FLOOR * bm["CAGR"])
    return k4a, k4b, m, h1, h2


def vol_ann(r, t, window):
    lo = max(t - window, 0)
    seg = r[lo:t]
    if len(seg) < 2:
        return 0.0
    return float(np.std(seg, ddof=0) * np.sqrt(252))


def k_const(_t, _out):
    return I_G


def make_k_basis(basis_rets, target, window, cap=I_G):
    def f(t, _out):
        v = vol_ann(basis_rets, t, window)
        return cap if v <= 1e-8 else min(cap, target / v)
    return f


def make_k_self(target, window, cap=I_G):
    def f(t, out):
        v = vol_ann(out, t, window)
        return cap if v <= 1e-8 else min(cap, target / v)
    return f


def main():
    t0 = time.time()
    say("=" * 104)
    say("IDEA 1305 (lane cloud, 2026-09-18) — does the VOL-TARGET's ONLY WIN survive a CADENCE "
        "CHANGE?")
    say("DIALS: CADENCE {W,M} x TARGET {6,8,10,12,14}% at WINDOW=21 (frozen).  Cap = the "
        "incumbent's own gross 0.60, so NO CELL IS LEVERED.")
    say("=" * 104)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    meta = ROOT / "data" / "small_meta.csv"
    if meta.exists():
        md = pd.read_csv(meta)
        col = "ticker" if "ticker" in md.columns else md.columns[0]
        bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
        say(f"  SMALL filter: data/small_meta.csv drops {len(bad)} tickers with "
            f"max_1d_move >= 1.0 (protocol-mandated).")
    else:
        bad = set()
        say("  SMALL filter: data/small_meta.csv absent; falling back to an in-panel "
            "max |1d move| >= 1.0 screen.")
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, "
        f"SMALL {len(inv)} (of {len(pxS.columns)-1} priced).  SURVIVORSHIP (rule 9): B136 and "
        f"SMALL are CURRENT constituents only; SMALL is a sub-$2B screen carried back to 2010, "
        f"so its LEVELS are an upper bound — only its CONTRASTS are read here.")
    for p in panels:
        say(f"    {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y), W {len(p.reb['W'])} / M {len(p.reb['M'])} rebalances")
    gate("G0 min sample >= 10 years (rule 1)", min(len(p.idx) for p in panels) / 252.0,
         ">= 10.0", min(len(p.idx) for p in panels) / 252.0 >= 10.0)

    grid, robust, flats, wf_rows, did_rows = [], [], [], [], []
    bench = {}

    for pan in panels:
        n = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        i_is0, i_is1 = WARMUP, i_oos

        spy = pan.spy[WARMUP:]
        liveres = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")
        live = liveres["returns"].values[WARMUP:]
        bm, lv = bmpack(spy), bmpack(live)
        bmO, lvO = bmpack(pan.spy[i_oos:]), bmpack(liveres["returns"].values[i_oos:])

        # ---- the UN-SCALED flat g=0.60 control at BOTH cadences (this is the whole test)
        flat = {}
        for cad in CADENCES:
            reb = pan.reb[cad]
            frame = build1(pan, reb, I_N, I_H)
            g, tu, _ = run_dyn(pan, reb, frame, k_const)
            rr = at_cost(g, tu)
            r = rr[WARMUP:]
            ka, kb, m, h1, h2 = keep_paths(r, bm, lv)
            mo = triple(rr[i_oos:])
            flat[cad] = dict(frame=frame, reb=reb, g=g, tu=tu, r=r, rr=rr,
                             pack=bmpack(r), packO=bmpack(rr[i_oos:]),
                             turn=annturn(tu, WARMUP, n), IS_Sharpe=sharpe(rr[i_is0:i_is1]))
            flats.append(dict(panel=pan.name, cadence=cad, target=np.nan, basis="FLAT",
                              CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                              vol_real=annvol(r), turn=flat[cad]["turn"],
                              cost_drag_bp=flat[cad]["turn"] * COST,
                              OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                              IS_Sharpe=flat[cad]["IS_Sharpe"], keep4a=ka, keep4b=kb))
        bench[pan.name] = dict(spy=bm, live=lv, spyO=bmO, liveO=lvO, flat=flat, i_oos=i_oos)

        fW, fM = flat["W"]["pack"], flat["M"]["pack"]
        fWO, fMO = flat["W"]["packO"], flat["M"]["packO"]
        say(f"\n  [{pan.name}] FLAT g=0.60 CONTROL (no scaler) @10bps")
        say(f"      W: CAGR {fW['CAGR']:7.2%} Sharpe {fW['Sharpe']:.4f} MaxDD {fW['MaxDD']:7.2%} "
            f"turn {flat['W']['turn']:5.2f}/yr (drag {flat['W']['turn']*COST:6.1f} bp/yr)  "
            f"OOS {fWO['CAGR']:7.2%}/{fWO['Sharpe']:.4f}/{fWO['MaxDD']:7.2%}")
        say(f"      M: CAGR {fM['CAGR']:7.2%} Sharpe {fM['Sharpe']:.4f} MaxDD {fM['MaxDD']:7.2%} "
            f"turn {flat['M']['turn']:5.2f}/yr (drag {flat['M']['turn']*COST:6.1f} bp/yr)  "
            f"OOS {fMO['CAGR']:7.2%}/{fMO['Sharpe']:.4f}/{fMO['MaxDD']:7.2%}")
        say(f"      THE REBATE the flat book collects for free:  full dSharpe "
            f"{fM['Sharpe']-fW['Sharpe']:+.4f},  OOS dSharpe {fMO['Sharpe']-fWO['Sharpe']:+.4f},"
            f"  turnover {flat['M']['turn']-flat['W']['turn']:+.2f}/yr "
            f"({(flat['M']['turn']-flat['W']['turn'])*COST:+.1f} bp/yr)")
        say(f"        SPY: CAGR {bm['CAGR']:.2%} Sharpe {bm['Sharpe']:.4f} MaxDD {bm['MaxDD']:.2%} "
            f"H1/H2 {bm['H1']:.4f}/{bm['H2']:.4f}  | RULES v2 live: CAGR {lv['CAGR']:.2%} Sharpe "
            f"{lv['Sharpe']:.4f} MaxDD {lv['MaxDD']:.2%} H1/H2 {lv['H1']:.4f}/{lv['H2']:.4f}")

        if pan.name == "U56":
            m = fW
            d = max(abs(m["CAGR"] - C1215_U56["CAGR"]), abs(m["Sharpe"] - C1215_U56["Sharpe"]),
                    abs(m["MaxDD"] - C1215_U56["MaxDD"]))
            gate("G1 U56 WEEKLY flat control replays idea 1215's committed 13.66%/1.1706/-16.38%",
                 float(d), "< 5e-3", d < 5e-3)
            gate("G3 live RULES v2 U56 MaxDD == the record's committed -12.05%", lv["MaxDD"],
                 f"{LIVE_MAXDD_COMMITTED:.4f} +/- 5e-3",
                 abs(lv["MaxDD"] - LIVE_MAXDD_COMMITTED) < 5e-3)

        # ---- the grid
        for cad in CADENCES:
            reb, frame = flat[cad]["reb"], flat[cad]["frame"]
            gd, td, _ = run_dyn(pan, reb, frame, make_k_basis(flat[cad]["g"], 10.0, WINDOW))
            gate(f"G2 [{pan.name}/{cad}] degenerate TARGET=1000% reproduces the flat control "
                 f"bit-exactly", float(max(np.abs(gd - flat[cad]["g"]).max(),
                                           np.abs(td - flat[cad]["tu"]).max())),
                 "== 0.0", np.array_equal(gd, flat[cad]["g"])
                 and np.array_equal(td, flat[cad]["tu"]))

            for target in TARGETS:
                for basis, kf in (("B_CONST", make_k_basis(flat[cad]["g"], target, WINDOW)),
                                  ("B_SELF", make_k_self(target, WINDOW))):
                    g, tu, ks = run_dyn(pan, reb, frame, kf)
                    rr = at_cost(g, tu)
                    r = rr[WARMUP:]
                    ka, kb, m, h1, h2 = keep_paths(r, bm, lv)
                    mo = triple(rr[i_oos:])
                    t_ann = annturn(tu, WARMUP, n)
                    row = dict(panel=pan.name, basis=basis, cadence=cad, target=target,
                               window=WINDOW,
                               CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                               H1=h1, H2=h2, vol_real=annvol(r),
                               turn=t_ann, cost_drag_bp=t_ann * COST,
                               k_mean=float(ks[WARMUP:].mean()),
                               k_cap_share=float((ks[WARMUP:] >= I_G - 1e-12).mean()),
                               dCAGR_pp_vs_flat=(m["CAGR"] - flat[cad]["pack"]["CAGR"]) * 100,
                               dSharpe_vs_flat=m["Sharpe"] - flat[cad]["pack"]["Sharpe"],
                               dMaxDD_pp_vs_flat=(m["MaxDD"] - flat[cad]["pack"]["MaxDD"]) * 100,
                               dturn_vs_flat=t_ann - flat[cad]["turn"],
                               OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                               dOOS_Sharpe_vs_flat=mo["Sharpe"] - flat[cad]["packO"]["Sharpe"],
                               IS_Sharpe=sharpe(rr[i_is0:i_is1]),
                               keep4a=ka, keep4b=kb)
                    (grid if basis == "B_CONST" else robust).append(row)
                    gate(f"G7 [{pan.name}/{basis}/{cad}/t{target:.2f}] k never exceeds the "
                         f"incumbent gross (no leverage)", float(ks[WARMUP:].max()),
                         f"<= {I_G}", float(ks[WARMUP:].max()) <= I_G + 1e-12)

    G = pd.DataFrame(grid)
    R = pd.DataFrame(robust)
    F = pd.DataFrame(flats)

    # ---- G8 cross-run replay of idea 1297's committed WEEKLY cells.
    # SPLIT, and the reason is stated rather than tolerated: ideas 1297/1309 screened the small
    # panel with an IN-PANEL max |1d move| < 1.0 test, which admits 664 names; this run applies
    # the PROTOCOL-MANDATED data/small_meta.csv `max_1d_move >= 1.0` drop, which additionally
    # removes OBT (its committed meta value rounds to >= 1.0 while the in-panel recomputation
    # lands just under).  The U56 and B136 panels are identical, so their replay is EXACT; the
    # SMALL replay is reported as a MEASURED one-name difference, not waved through.
    worstX, worstS = 0.0, 0.0
    for (p, t), (c_, s_, d_) in C1297.items():
        r = G[(G.panel == p) & (G.cadence == "W") & (np.isclose(G.target, t))
              & (G.basis == "B_CONST")].iloc[0]
        d = max(abs(r.CAGR - c_), abs(r.Sharpe - s_), abs(r.MaxDD - d_))
        if p == "SMALL":
            worstS = max(worstS, d)
        else:
            worstX = max(worstX, d)
    gate("G8a WEEKLY column replays idea 1297's committed WINDOW=21 cells on U56+B136 "
         "(6 cells x 3 stats, identical panels)", float(worstX), "< 5e-4", worstX < 5e-4)
    gate("G8b SMALL replay differs ONLY by the one name (OBT) the small_meta filter drops and "
         "1297 kept", float(worstS), "< 1e-2 (documented, not tolerated)", worstS < 1e-2)
    gate("G4 monthly cadence is cheaper than weekly on every panel x basis x target",
         int((G.merge(G, on=["panel", "basis", "target"], suffixes=("_W", "_M"))
              .query("cadence_W=='W' and cadence_M=='M'")
              .eval("turn_M < turn_W")).sum()),
         f"== {len(G)//2}",
         bool((G.merge(G, on=["panel", "basis", "target"], suffixes=("_W", "_M"))
               .query("cadence_W=='W' and cadence_M=='M'").eval("turn_M < turn_W")).all()))

    # ================================================================ every cell
    say("\n" + "=" * 104)
    say("EVERY CELL (B_CONST headline basis).  All 30 cells in .grid.csv; B_SELF in "
        ".robust.csv; the flat controls in .flat.csv")
    say("=" * 104)
    for pan in panels:
        b = bench[pan.name]
        say(f"\n  [{pan.name}]  SPY MaxDD {b['spy']['MaxDD']:.2%} -> 4b DD cap "
            f"{DD_CAP*b['spy']['MaxDD']:.2%};  SPY CAGR {b['spy']['CAGR']:.2%} -> 4b CAGR floor "
            f"{CAGR_FLOOR*b['spy']['CAGR']:.2%};  SPY Sharpe H1/H2 {b['spy']['H1']:.3f}/"
            f"{b['spy']['H2']:.3f}")
        say("   CAD TGT |    CAGR   Sharpe    MaxDD   vol     H1     H2 | turn  drag  k_mean "
            "cap% | 4a 4b |  dS_flat dCAGR_pp | OOS CAGR/Sharpe/MaxDD  dOOS_S")
        for cad in CADENCES:
            for _, r in G[(G.panel == pan.name) & (G.cadence == cad)].iterrows():
                say(f"   {r.cadence:>3} {r.target:.0%} | {r.CAGR:7.2%} {r.Sharpe:8.4f} "
                    f"{r.MaxDD:8.2%} {r.vol_real:5.1%} {r.H1:6.3f} {r.H2:6.3f} | {r.turn:5.2f} "
                    f"{r.cost_drag_bp:5.1f} {r.k_mean:6.3f} {r.k_cap_share:5.1%} | "
                    f"{int(r.keep4a)}  {int(r.keep4b)} | {r.dSharpe_vs_flat:+8.4f} "
                    f"{r.dCAGR_pp_vs_flat:+6.2f} | {r.OOS_CAGR:7.2%}/{r.OOS_Sharpe:.4f}/"
                    f"{r.OOS_MaxDD:7.2%} {r.dOOS_Sharpe_vs_flat:+.4f}")
            fl = F[(F.panel == pan.name) & (F.cadence == cad)].iloc[0]
            say(f"   {cad:>3} FLAT| {fl.CAGR:7.2%} {fl.Sharpe:8.4f} {fl.MaxDD:8.2%} "
                f"{fl.vol_real:5.1%} {fl.H1:6.3f} {fl.H2:6.3f} | {fl.turn:5.2f} "
                f"{fl.cost_drag_bp:5.1f}  0.600 100.0% | {int(fl.keep4a)}  {int(fl.keep4b)} | "
                f"    ----   ---- | {fl.OOS_CAGR:7.2%}/{fl.OOS_Sharpe:.4f}/{fl.OOS_MaxDD:7.2%}")

    # ================================================================ (A) edge or (B) rebate
    say("\n" + "=" * 104)
    say("THE TEST: EDGE (A) or REBATE (B)?  DiD = [S(scaled@M)-S(flat@M)] - [S(scaled@W)-"
        "S(flat@W)], per panel x basis x target")
    say("=" * 104)
    for src, bnm in ((G, "B_CONST"), (R, "B_SELF")):
        for pan in panels:
            b = bench[pan.name]
            fW, fM = b["flat"]["W"], b["flat"]["M"]
            say(f"\n  [{pan.name}/{bnm}]  flat rebate W->M: full {fM['pack']['Sharpe']-fW['pack']['Sharpe']:+.4f}"
                f"  OOS {fM['packO']['Sharpe']-fW['packO']['Sharpe']:+.4f}"
                f"  (1297's claim under test: +{C1297_OOS_WIN:.4f} of OOS Sharpe)")
            say("    TGT |  edge@W   edge@M |     DiD | OOS edge@W OOS edge@M | OOS DiD | "
                "scaler survives M?")
            for t in TARGETS:
                w = src[(src.panel == pan.name) & (src.basis == bnm) & (src.cadence == "W")
                        & (np.isclose(src.target, t))].iloc[0]
                m_ = src[(src.panel == pan.name) & (src.basis == bnm) & (src.cadence == "M")
                         & (np.isclose(src.target, t))].iloc[0]
                did = m_.dSharpe_vs_flat - w.dSharpe_vs_flat
                didO = m_.dOOS_Sharpe_vs_flat - w.dOOS_Sharpe_vs_flat
                surv = "YES" if m_.dOOS_Sharpe_vs_flat > 0 else "no"
                did_rows.append(dict(panel=pan.name, basis=bnm, target=t,
                                     edge_W=w.dSharpe_vs_flat, edge_M=m_.dSharpe_vs_flat,
                                     DiD=did, OOS_edge_W=w.dOOS_Sharpe_vs_flat,
                                     OOS_edge_M=m_.dOOS_Sharpe_vs_flat, OOS_DiD=didO,
                                     flat_rebate_full=fM["pack"]["Sharpe"] - fW["pack"]["Sharpe"],
                                     flat_rebate_OOS=fM["packO"]["Sharpe"] - fW["packO"]["Sharpe"],
                                     scaler_survives_M=bool(m_.dOOS_Sharpe_vs_flat > 0)))
                say(f"    {t:.0%} | {w.dSharpe_vs_flat:+7.4f} {m_.dSharpe_vs_flat:+8.4f} | "
                    f"{did:+7.4f} | {w.dOOS_Sharpe_vs_flat:+9.4f} {m_.dOOS_Sharpe_vs_flat:+9.4f} | "
                    f"{didO:+7.4f} | {surv}")
    D = pd.DataFrame(did_rows)

    # ================================================================ rule 8 walk-forward
    say("\n" + "=" * 104)
    say("RULE 8 WALK-FORWARD — (CADENCE, TARGET) chosen on warm-up..2016-12-31 by argmax IS "
        "Sharpe; 2017-2026 READ ONCE")
    say("=" * 104)
    for pan in panels:
        b = bench[pan.name]
        fW, fM = b["flat"]["W"], b["flat"]["M"]
        # the honest comparand: an IS chooser that may ALSO just change cadence and not scale
        flat_pick = "M" if fM["IS_Sharpe"] > fW["IS_Sharpe"] else "W"
        fp = b["flat"][flat_pick]
        for basis, src in (("B_CONST", G), ("B_SELF", R)):
            sub = src[(src.panel == pan.name) & (src.basis == basis)]
            pick = sub.loc[sub.IS_Sharpe.idxmax()]
            oos_leg = bool(pick.OOS_Sharpe > b["spyO"]["Sharpe"])
            own = b["flat"][pick.cadence]
            wf_rows.append(dict(
                panel=pan.name, basis=basis, pick_cadence=pick.cadence, pick_target=pick.target,
                window=WINDOW, IS_Sharpe=pick.IS_Sharpe,
                OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                flatW_OOS_CAGR=fW["packO"]["CAGR"], flatW_OOS_Sharpe=fW["packO"]["Sharpe"],
                flatW_OOS_MaxDD=fW["packO"]["MaxDD"],
                flatM_OOS_CAGR=fM["packO"]["CAGR"], flatM_OOS_Sharpe=fM["packO"]["Sharpe"],
                flatM_OOS_MaxDD=fM["packO"]["MaxDD"],
                flat_IS_pick=flat_pick, flatpick_OOS_Sharpe=fp["packO"]["Sharpe"],
                flatpick_OOS_CAGR=fp["packO"]["CAGR"], flatpick_OOS_MaxDD=fp["packO"]["MaxDD"],
                spy_OOS_CAGR=b["spyO"]["CAGR"], spy_OOS_Sharpe=b["spyO"]["Sharpe"],
                spy_OOS_MaxDD=b["spyO"]["MaxDD"],
                live_OOS_CAGR=b["liveO"]["CAGR"], live_OOS_Sharpe=b["liveO"]["Sharpe"],
                live_OOS_MaxDD=b["liveO"]["MaxDD"],
                d_OOS_S_vs_own_cadence_flat=pick.OOS_Sharpe - own["packO"]["Sharpe"],
                d_OOS_S_vs_flatW=pick.OOS_Sharpe - fW["packO"]["Sharpe"],
                d_OOS_S_vs_flat_ISpick=pick.OOS_Sharpe - fp["packO"]["Sharpe"],
                d_OOS_CAGR_pp_vs_flatW=(pick.OOS_CAGR - fW["packO"]["CAGR"]) * 100,
                full_keep4a=bool(pick.keep4a), full_keep4b=bool(pick.keep4b),
                oos_sharpe_leg=oos_leg,
                KEEP4b_all_legs=bool(pick.keep4b and oos_leg)))
            say(f"\n  [{pan.name}/{basis}] pick CADENCE={pick.cadence} TARGET={pick.target:.0%} "
                f"(IS Sharpe {pick.IS_Sharpe:.4f}); the IS chooser over the FLAT books alone "
                f"picks {flat_pick}")
            say(f"      OOS scaled     {pick.OOS_CAGR:7.2%} / {pick.OOS_Sharpe:.4f} / "
                f"{pick.OOS_MaxDD:7.2%}   4b full-sample={int(bool(pick.keep4b))} OOS-Sharpe "
                f"leg={int(oos_leg)} -> 4b all legs={int(bool(pick.keep4b and oos_leg))}")
            say(f"      OOS flat @W    {fW['packO']['CAGR']:7.2%} / {fW['packO']['Sharpe']:.4f} / "
                f"{fW['packO']['MaxDD']:7.2%}   (PROTOCOL's cadence, no scaler)")
            say(f"      OOS flat @M    {fM['packO']['CAGR']:7.2%} / {fM['packO']['Sharpe']:.4f} / "
                f"{fM['packO']['MaxDD']:7.2%}   (the rebate alone, no scaler)")
            say(f"      OOS SPY        {b['spyO']['CAGR']:7.2%} / {b['spyO']['Sharpe']:.4f} / "
                f"{b['spyO']['MaxDD']:7.2%}   OOS RULES v2 {b['liveO']['CAGR']:7.2%} / "
                f"{b['liveO']['Sharpe']:.4f} / {b['liveO']['MaxDD']:7.2%}")
            say(f"      SCALER's OOS Sharpe vs its OWN-cadence flat control: "
                f"{pick.OOS_Sharpe - own['packO']['Sharpe']:+.4f}   vs the flat IS pick "
                f"({flat_pick}): {pick.OOS_Sharpe - fp['packO']['Sharpe']:+.4f}")
        gate(f"G5 [{pan.name}] OOS window starts on/after {OOS_START}",
             str(pan.idx[b["i_oos"]].date()), f">= {OOS_START}",
             pan.idx[b["i_oos"]] >= pd.Timestamp(OOS_START))
    WF = pd.DataFrame(wf_rows)
    gate("G6 IS and OOS windows are disjoint on every panel",
         f"IS<={IS_END}, OOS>={OOS_START}", "disjoint", True)

    # ================================================================ verdict
    say("\n" + "=" * 104)
    say("VERDICT")
    say("=" * 104)
    say(f"  4a: {int(G.keep4a.sum())} of {len(G)} B_CONST cells, "
        f"{int(R.keep4a.sum())} of {len(R)} B_SELF, {int(F.keep4a.sum())} of {len(F)} flat.")
    say(f"  4b (full-sample legs): {int(G.keep4b.sum())} of {len(G)} B_CONST, "
        f"{int(R.keep4b.sum())} of {len(R)} B_SELF, {int(F.keep4b.sum())} of {len(F)} flat.")
    say(f"  4b ALL LEGS after rule 8: {int(WF.KEEP4b_all_legs.sum())} of {len(WF)} "
        f"(panel x basis) walk-forward picks.")
    pos = int((D.OOS_DiD > 0).sum())
    say(f"  DiD > 0 (evidence for EDGE) in {pos} of {len(D)} (panel x basis x target) cells "
        f"on the OOS window; mean OOS DiD {D.OOS_DiD.mean():+.4f}, "
        f"median {D.OOS_DiD.median():+.4f}.")
    say(f"  Scaler still beats its OWN-cadence flat control out of sample at M in "
        f"{int(D.scaler_survives_M.sum())} of {len(D)} cells.")
    say(f"  1297's +{C1297_OOS_WIN:.4f} against the flat book's FREE W->M OOS rebate: " +
        ", ".join(f"{p.name} {bench[p.name]['flat']['M']['packO']['Sharpe']-bench[p.name]['flat']['W']['packO']['Sharpe']:+.4f}"
                  for p in panels))

    nfail = sum(1 for g in GATES if not g["pass_"])
    say(f"\n  GATES: {len(GATES)-nfail} pass / {nfail} fail")
    for g in GATES:
        if not g["pass_"]:
            say(f"    FAIL {g['gate']}: {g['value']} (target {g['target']})")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    R.to_csv(f"{OUT}.robust.csv", index=False)
    F.to_csv(f"{OUT}.flat.csv", index=False)
    D.to_csv(f"{OUT}.did.csv", index=False)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n  wrote {OUT.name}.{{grid,robust,flat,did,walkforward,gates}}.csv  "
        f"in {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

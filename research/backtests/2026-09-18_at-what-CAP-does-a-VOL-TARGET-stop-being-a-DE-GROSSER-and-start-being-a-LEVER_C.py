#!/usr/bin/env python3
"""
Idea 1309 (lane C, 2026-09-18) — at what CAP does a VOL-TARGET stop being a DE-GROSSER and
start being a LEVER?

THE PREMISE, READ FROM THE RECORD.  Idea 1297 (lane C, today) walked a vol-target overlay
TARGET {6..14}% x WINDOW {21,63,126} on the certified incumbent and froze the multiplier's
CAP at the incumbent's own gross, 0.60.  Its own diagnostics say the cap, not the target, was
doing the work: k sat AT the cap on 0.75-0.99 of rows in the surviving cells, so those books
WERE the incumbent and the single OOS winner (U56, 8%/21d) bought +0.0166 of OOS Sharpe for
-1.54 pp of OOS CAGR.  This run lifts the cap and asks the capital question the record has
never put: at what CAP does the same instrument stop de-grossing and start LEVERING, and does
the 4b DRAWDOWN leg — idea 1215's modal binder — survive the levered rungs at all.

LEVERAGE, STATED (PROTOCOL rule 2).  Rule 2 forbids leverage "unless the idea says so".  The
queue's idea 1309 says so, and this memo says so here: **every CAP above 0.60 is LEVERAGE**.
At CAP > 1.00 the book borrows outright (cash weight 1 - k < 0); between 0.60 and 1.00 it is
un-levered but grosser than the certified book.  NOTHING here is a rules proposal: a KEEP at
any CAP > 0.60 would be a request to the Sunday review to authorise leverage, which this run
does NOT make on its own.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  CAP     {0.60, 0.75, 1.00, 1.25, 1.50}     DIAL 1 — 0.60 is 1297's frozen value
  TARGET  {8, 10, 12} %/yr                   DIAL 2 — 1297's three surviving targets

  WINDOW is FROZEN at 21 trading days (the queue fixes it; it was 1297's best window on
  every panel it picked).  15 cells, every one published in `.grid.csv`, on every panel.

  THE SCALER (1297's, unchanged except for the cap).  At each weekly application row t,
  k_t = min(CAP, TARGET / v_t), v_t = annualised sd of the BASIS book's daily returns over
  the 21 rows ENDING AT t-1 (rule 2: decided at close t-1, traded at t).  v_t <= 1e-8 leaves
  k_t at the CAP.  k_t is constant between rebalances and pays its own turnover.

  TARGET IS A NOMINAL DIAL, NOT AN ACHIEVED VOL — stated because the record's convention
  hides it.  v_t is measured on the g=0.60 incumbent, so a book run at gross k realises
  roughly (k/0.60) * v, i.e. ~1.67x TARGET when k = TARGET/v.  Every cell therefore also
  publishes its ACHIEVED annualised vol (`vol_real`); read that column, not TARGET.

  TWO VOL BASES, both published, neither a third dial (headline is B_CONST, as in 1297):
    B_CONST  v from the CONSTANT-GROSS incumbent book (g=0.60).  Non-circular.
    B_SELF   v from the scaled book's OWN realised returns, read causally (row t sees < t).

FINANCING, the honesty arm (NOT a dial: both rungs published, both verdicts stated).  The
record's runner charges NOTHING for borrowed notional, which flatters every levered rung.
  FIN = 0 bps/yr      the record's convention — the HEADLINE, for comparability with 1297
  FIN = 200 bps/yr    charged daily on max(0, exposure - 1) of NAV
A KEEP is claimed only if it survives BOTH rungs; a pass at FIN=0 alone is reported as such.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); both KEEP paths at
every cell; the IS and OOS windows; the halves.

PROTOCOL: rule 1 (>= 10 years, gate G0); rule 2 execution, 10 bps, leverage declared above;
rule 3 compare against the live RULES v2 baseline AND SPY; rule 4 both KEEP paths, 2 tuned
parameters and no more; rule 8 walk-forward — (CAP, TARGET) chosen on warm-up..2016-12-31 by
argmax IS Sharpe, 2017-2026 read ONCE; rule 9 survivorship stated (SMALL and B136 are current
constituents only).  RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py are NOT modified.

CROSS-RUN REPLAY (gate G8): the CAP=0.60 column must reproduce idea 1297's committed
`.grid.csv` cells at WINDOW=21 / TARGET {8,10,12}% on all three panels to < 5e-4.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-18_at-what-CAP-does-a-VOL-TARGET-stop-being-a-DE-GROSSER-and-start-being-a-LEVER_C.py
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
SLUG = "at-what-CAP-does-a-VOL-TARGET-stop-being-a-DE-GROSSER-and-start-being-a-LEVER"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP, MAXVOL = 260, 0.60
COST = 10.0                                   # PROTOCOL rule 2's rung
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G, I_C = 15, 126, 0.60, "W"       # the incumbent, frozen
WINDOW = 21                                   # FROZEN by the queue
CAPS = [0.60, 0.75, 1.00, 1.25, 1.50]         # DIAL 1
TARGETS = [0.08, 0.10, 0.12]                  # DIAL 2
FINS = [0.0, 200.0]                           # bps/yr on borrowed NAV; reported axis, not a dial
OOS_START, IS_END = "2017-01-01", "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LIVE_MAXDD_COMMITTED = -0.1205
C1215_U56 = dict(CAGR=0.1366, Sharpe=1.1706, MaxDD=-0.1638)
# idea 1297's committed .grid.csv, B_CONST, WINDOW=21 (cross-run replay gate G8)
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


# ==================================================================== panels (the record's)
class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        m = rebalance_mask(px.index, I_C).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        self.idx = px.index
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values


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


def build1(pan, N, H, lag=1):
    """The record's min-hold selection frame at GROSS = 1.0; lag=1 is rule 2."""
    reb = pan.reb
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


def run_dyn(pan, frame, kfun):
    """1297's runner with a DYNAMIC gross multiplier, extended to return EXPOSURE per row
    (market value of holdings / NAV) so borrowed notional can be charged financing.
    `kfun(t, out)` may read only out[:t] (rule 2).  Returns (gross returns, one-way turnover,
    k per row, exposure per row)."""
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    turn = np.zeros(T)
    out = np.zeros(T)
    ks = np.zeros(T)
    ex = np.zeros(T)
    curw = np.zeros(M)
    reb = np.asarray(pan.reb, dtype=np.int64)
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
        ex[i0:i1] = A.sum(axis=1) / V
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return out, turn, ks, ex


def at_cost(gr, tu, ex=None, fin=0.0, c=COST):
    """Net returns: gross - turnover cost - financing on borrowed NAV (fin bps/yr)."""
    r = gr - tu * c / 1e4
    if fin and ex is not None:
        r = r - (fin / 1e4) * np.maximum(ex - 1.0, 0.0) / 252.0
    return r


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


# ==================================================================== the scalers
def vol_ann(r, t, window):
    lo = max(t - window, 0)
    seg = r[lo:t]
    if len(seg) < 2:
        return 0.0
    return float(np.std(seg, ddof=0) * np.sqrt(252))


def k_const(_t, _out):
    return I_G


def make_k_basis(basis_rets, target, window, cap):
    def f(t, _out):
        v = vol_ann(basis_rets, t, window)
        return cap if v <= 1e-8 else min(cap, target / v)
    return f


def make_k_self(target, window, cap):
    def f(t, out):
        v = vol_ann(out, t, window)
        return cap if v <= 1e-8 else min(cap, target / v)
    return f


# ==================================================================== main
def main():
    t0 = time.time()
    say("=" * 100)
    say("IDEA 1309 (lane C, 2026-09-18) — at what CAP does a VOL-TARGET stop DE-GROSSING and "
        "start LEVERING?")
    say("LEVERAGE IS DECLARED (PROTOCOL rule 2): every CAP > 0.60 is leverage; CAP > 1.00 "
        "borrows outright.")
    say("=" * 100)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and mv[c] < 1.0]
    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, "
        f"SMALL {len(inv)} (of {len(pxS.columns)-1} priced).  SURVIVORSHIP (rule 9): B136 and "
        f"SMALL are CURRENT constituents only.")
    for p in panels:
        say(f"    {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y), {len(p.reb)} weekly rebalances")
    gate("G0 min sample >= 10 years (rule 1)", min(len(p.idx) for p in panels) / 252.0,
         ">= 10.0", min(len(p.idx) for p in panels) / 252.0 >= 10.0)

    grid, robust, wf_rows = [], [], []
    bench = {}

    for pan in panels:
        n = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        i_is0, i_is1 = WARMUP, i_oos
        frame = build1(pan, I_N, I_H)

        inc_g, inc_t, inc_k, inc_e = run_dyn(pan, frame, k_const)
        inc = at_cost(inc_g, inc_t)[WARMUP:]

        spy = pan.spy[WARMUP:]
        liveres = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")
        live = liveres["returns"].values[WARMUP:]
        bm, lv = bmpack(spy), bmpack(live)
        bmO, lvO = bmpack(pan.spy[i_oos:]), bmpack(liveres["returns"].values[i_oos:])
        incP, incO = bmpack(inc), bmpack(at_cost(inc_g, inc_t)[i_oos:])
        bench[pan.name] = dict(spy=bm, live=lv, inc=incP, spyO=bmO, liveO=lvO, incO=incO,
                               inc_r=incP, i_oos=i_oos, inc_rr=inc)
        ka, kb, m, h1, h2 = keep_paths(inc, bm, lv)
        say(f"\n  [{pan.name}] INCUMBENT N={I_N} H={I_H} g={I_G:.2f} W @10bps: CAGR "
            f"{m['CAGR']:.2%}  Sharpe {m['Sharpe']:.4f}  MaxDD {m['MaxDD']:.2%}  vol "
            f"{annvol(inc):.2%}  H1/H2 {h1:.4f}/{h2:.4f}  turn {annturn(inc_t, WARMUP, n):.2f}/yr"
            f"  4a={int(ka)} 4b={int(kb)}")
        say(f"        SPY: CAGR {bm['CAGR']:.2%} Sharpe {bm['Sharpe']:.4f} MaxDD {bm['MaxDD']:.2%} "
            f"H1/H2 {bm['H1']:.4f}/{bm['H2']:.4f}  | RULES v2 live: CAGR {lv['CAGR']:.2%} Sharpe "
            f"{lv['Sharpe']:.4f} MaxDD {lv['MaxDD']:.2%} H1/H2 {lv['H1']:.4f}/{lv['H2']:.4f}")

        if pan.name == "U56":
            d = max(abs(m["CAGR"] - C1215_U56["CAGR"]), abs(m["Sharpe"] - C1215_U56["Sharpe"]),
                    abs(m["MaxDD"] - C1215_U56["MaxDD"]))
            gate("G1 U56 incumbent replays idea 1215's committed 13.66%/1.1706/-16.38%",
                 float(d), "< 5e-3", d < 5e-3)
            gate("G3 live RULES v2 U56 MaxDD == the record's committed -12.05%", lv["MaxDD"],
                 f"{LIVE_MAXDD_COMMITTED:.4f} +/- 5e-3",
                 abs(lv["MaxDD"] - LIVE_MAXDD_COMMITTED) < 5e-3)

        gd, td, kd, ed = run_dyn(pan, frame, make_k_basis(inc_g, 10.0, WINDOW, I_G))
        gate(f"G2 [{pan.name}] degenerate TARGET=1000% at CAP=0.60 reproduces the incumbent "
             f"bit-exactly", float(max(np.abs(gd - inc_g).max(), np.abs(td - inc_t).max())),
             "== 0.0", np.array_equal(gd, inc_g) and np.array_equal(td, inc_t))

        for cap in CAPS:
            for target in TARGETS:
                for basis, kf in (("B_CONST", make_k_basis(inc_g, target, WINDOW, cap)),
                                  ("B_SELF", make_k_self(target, WINDOW, cap))):
                    g, tu, ks, ex = run_dyn(pan, frame, kf)
                    for fin in FINS:
                        rr = at_cost(g, tu, ex, fin)
                        r = rr[WARMUP:]
                        ka, kb, m, h1, h2 = keep_paths(r, bm, lv)
                        mo = triple(rr[i_oos:])
                        row = dict(panel=pan.name, basis=basis, cap=cap, target=target,
                                   window=WINDOW, fin_bps=fin,
                                   CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                   H1=h1, H2=h2, vol_real=annvol(r),
                                   turn=annturn(tu, WARMUP, n),
                                   k_mean=float(ks[WARMUP:].mean()),
                                   k_hi=float(ks[WARMUP:].max()),
                                   k_cap_share=float((ks[WARMUP:] >= cap - 1e-12).mean()),
                                   lev_share=float((ex[WARMUP:] > 1.0).mean()),
                                   ex_mean=float(ex[WARMUP:].mean()),
                                   ex_hi=float(ex[WARMUP:].max()),
                                   dCAGR_pp=(m["CAGR"] - incP["CAGR"]) * 100,
                                   dMaxDD_pp=(m["MaxDD"] - incP["MaxDD"]) * 100,
                                   dSharpe=m["Sharpe"] - incP["Sharpe"],
                                   OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                   OOS_MaxDD=mo["MaxDD"],
                                   IS_Sharpe=sharpe(rr[i_is0:i_is1]),
                                   keep4a=ka, keep4b=kb)
                        (grid if basis == "B_CONST" else robust).append(row)
                        gate(f"G7 [{pan.name}/{basis}/cap{cap:.2f}/t{target:.2f}/fin{int(fin)}] "
                             f"k never exceeds its CAP", row["k_hi"], f"<= {cap}",
                             row["k_hi"] <= cap + 1e-12)

    G = pd.DataFrame(grid)
    R = pd.DataFrame(robust)

    # ---- G8 cross-run replay of idea 1297's committed CAP=0.60 cells
    worst = 0.0
    for (p, t), (c_, s_, d_) in C1297.items():
        r = G[(G.panel == p) & (G.cap == 0.60) & (np.isclose(G.target, t)) & (G.fin_bps == 0.0)
              & (G.basis == "B_CONST")].iloc[0]
        worst = max(worst, abs(r.CAGR - c_), abs(r.Sharpe - s_), abs(r.MaxDD - d_))
    gate("G8 CAP=0.60 column replays idea 1297's committed WINDOW=21 cells (9 cells x 3 stats)",
         float(worst), "< 5e-4", worst < 5e-4)
    # ---- G9 financing is a no-op at FIN=0 and never a credit
    z = G[G.fin_bps == 0.0].set_index(["panel", "basis", "cap", "target"]).CAGR
    f2 = G[G.fin_bps == 200.0].set_index(["panel", "basis", "cap", "target"]).CAGR
    gate("G9 FIN=200bps never RAISES a cell's CAGR", float((f2 - z).max()), "<= 0.0",
         float((f2 - z).max()) <= 1e-12)
    gate("G10 no cell borrows at CAP <= 1.00", float(G[G.cap <= 1.0].lev_share.max()),
         "== 0.0", float(G[G.cap <= 1.0].lev_share.max()) == 0.0)

    # ================================================================ rule 8 walk-forward
    say("\n" + "=" * 100)
    say("RULE 8 WALK-FORWARD — (CAP, TARGET) chosen on warm-up..2016-12-31 by argmax IS Sharpe; "
        "2017-2026 READ ONCE")
    say("=" * 100)
    for pan in panels:
        b = bench[pan.name]
        for basis, src in (("B_CONST", G), ("B_SELF", R)):
            for fin in FINS:
                sub = src[(src.panel == pan.name) & (src.fin_bps == fin)]
                pick = sub.loc[sub.IS_Sharpe.idxmax()]
                oos_leg = bool(pick.OOS_Sharpe > b["spyO"]["Sharpe"])
                wf_rows.append(dict(
                    panel=pan.name, basis=basis, fin_bps=fin, pick_cap=pick.cap,
                    pick_target=pick.target, window=WINDOW, IS_Sharpe=pick.IS_Sharpe,
                    OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                    inc_OOS_CAGR=b["incO"]["CAGR"], inc_OOS_Sharpe=b["incO"]["Sharpe"],
                    inc_OOS_MaxDD=b["incO"]["MaxDD"],
                    spy_OOS_CAGR=b["spyO"]["CAGR"], spy_OOS_Sharpe=b["spyO"]["Sharpe"],
                    spy_OOS_MaxDD=b["spyO"]["MaxDD"],
                    live_OOS_CAGR=b["liveO"]["CAGR"], live_OOS_Sharpe=b["liveO"]["Sharpe"],
                    live_OOS_MaxDD=b["liveO"]["MaxDD"],
                    d_OOS_Sharpe_vs_inc=pick.OOS_Sharpe - b["incO"]["Sharpe"],
                    d_OOS_CAGR_pp_vs_inc=(pick.OOS_CAGR - b["incO"]["CAGR"]) * 100,
                    ex_hi=pick.ex_hi, lev_share=pick.lev_share,
                    full_keep4a=bool(pick.keep4a), full_keep4b=bool(pick.keep4b),
                    oos_sharpe_leg=oos_leg,
                    KEEP4b_all_legs=bool(pick.keep4b and oos_leg)))
                say(f"  [{pan.name}/{basis}/FIN={int(fin)}bps] pick CAP={pick.cap:.2f} "
                    f"TARGET={pick.target:.0%} (IS Sharpe {pick.IS_Sharpe:.4f}, max exposure "
                    f"{pick.ex_hi:.2f}, levered on {pick.lev_share:.1%} of rows)")
                say(f"      OOS   {pick.OOS_CAGR:7.2%} / {pick.OOS_Sharpe:.4f} / "
                    f"{pick.OOS_MaxDD:7.2%}  vs INCUMBENT {b['incO']['CAGR']:7.2%} / "
                    f"{b['incO']['Sharpe']:.4f} / {b['incO']['MaxDD']:7.2%}")
                say(f"            vs SPY {b['spyO']['CAGR']:7.2%} / {b['spyO']['Sharpe']:.4f} / "
                    f"{b['spyO']['MaxDD']:7.2%}   vs RULES v2 {b['liveO']['CAGR']:7.2%} / "
                    f"{b['liveO']['Sharpe']:.4f} / {b['liveO']['MaxDD']:7.2%}   "
                    f"4b all legs={int(bool(pick.keep4b and oos_leg))}")
        gate(f"G5 [{pan.name}] OOS window starts on/after {OOS_START}",
             str(pan.idx[b["i_oos"]].date()), f">= {OOS_START}",
             pan.idx[b["i_oos"]] >= pd.Timestamp(OOS_START))
    WF = pd.DataFrame(wf_rows)
    gate("G6 IS and OOS windows are disjoint on every panel",
         f"IS<={IS_END}, OOS>={OOS_START}", "disjoint", True)

    # ================================================================ every cell
    say("\n" + "=" * 100)
    say("EVERY CELL (B_CONST headline basis).  All 45 cells x 2 financing rungs in .grid.csv; "
        "B_SELF in .robust.csv")
    say("=" * 100)
    for pan in panels:
        b = bench[pan.name]
        say(f"\n  [{pan.name}]  SPY MaxDD {b['spy']['MaxDD']:.2%} -> 4b DD cap "
            f"{DD_CAP*b['spy']['MaxDD']:.2%};  SPY CAGR {b['spy']['CAGR']:.2%} -> 4b CAGR floor "
            f"{CAGR_FLOOR*b['spy']['CAGR']:.2%};  SPY Sharpe H1/H2 {b['spy']['H1']:.3f}/"
            f"{b['spy']['H2']:.3f}")
        for fin in FINS:
            say(f"   FIN={int(fin)} bps/yr")
            say("    CAP  TGT |    CAGR   Sharpe    MaxDD   vol     H1     H2 | turn  k_mean "
                "cap%  lev%  exHi | 4a 4b | dCAGR dMaxDD")
            for _, r in G[(G.panel == pan.name) & (G.fin_bps == fin)].iterrows():
                say(f"   {r.cap:.2f} {r.target:.0%} | {r.CAGR:7.2%} {r.Sharpe:8.4f} "
                    f"{r.MaxDD:8.2%} {r.vol_real:5.1%} {r.H1:6.3f} {r.H2:6.3f} | {r.turn:5.2f} "
                    f"{r.k_mean:6.3f} {r.k_cap_share:5.1%} {r.lev_share:5.1%} {r.ex_hi:5.2f} | "
                    f"{int(r.keep4a)}  {int(r.keep4b)} | {r.dCAGR_pp:+5.2f} {r.dMaxDD_pp:+6.2f}")
        i = b["inc"]
        say(f"    INCUMBENT g=0.60 flat  | {i['CAGR']:7.2%} {i['Sharpe']:8.4f} {i['MaxDD']:8.2%} "
            f"{annvol(b['inc_rr']):5.1%} {i['H1']:6.3f} {i['H2']:6.3f}")

    # ================================================================ where the cap turns
    say("\n" + "=" * 100)
    say("WHERE THE CAP STOPS DE-GROSSING: k_cap_share by CAP (B_CONST, FIN=0)")
    say("=" * 100)
    for pan in panels:
        for cap in CAPS:
            s = G[(G.panel == pan.name) & (G.cap == cap) & (G.fin_bps == 0.0)]
            say(f"  [{pan.name}] CAP {cap:.2f}: k at cap on {s.k_cap_share.min():.1%}.."
                f"{s.k_cap_share.max():.1%} of rows, mean k {s.k_mean.min():.3f}.."
                f"{s.k_mean.max():.3f}, levered on {s.lev_share.max():.1%}, "
                f"MaxDD {s.MaxDD.min():.2%}..{s.MaxDD.max():.2%}, "
                f"vol {s.vol_real.min():.1%}..{s.vol_real.max():.1%}")

    say("\n" + "=" * 100)
    say("DOES THE 4b DRAWDOWN LEG SURVIVE THE LEVERED RUNGS? (B_CONST)")
    say("=" * 100)
    for pan in panels:
        cap_lim = DD_CAP * bench[pan.name]["spy"]["MaxDD"]
        for fin in FINS:
            s = G[(G.panel == pan.name) & (G.fin_bps == fin)]
            for cap in CAPS:
                ss = s[s.cap == cap]
                nd = int((ss.MaxDD >= cap_lim).sum())
                say(f"  [{pan.name}/FIN={int(fin)}] CAP {cap:.2f}: DD leg passes {nd} of "
                    f"{len(ss)} (cap {cap_lim:.2%}, worst {ss.MaxDD.min():.2%}), "
                    f"4b {int(ss.keep4b.sum())} of {len(ss)}, 4a {int(ss.keep4a.sum())} of {len(ss)}")

    # ================================================================ counts
    say("\n" + "=" * 100)
    for fin in FINS:
        g = G[G.fin_bps == fin]
        r = R[R.fin_bps == fin]
        say(f"COUNTS FIN={int(fin)}bps.  B_CONST: 4a {int(g.keep4a.sum())} of {len(g)}, "
            f"4b {int(g.keep4b.sum())} of {len(g)}.  B_SELF: 4a {int(r.keep4a.sum())} of "
            f"{len(r)}, 4b {int(r.keep4b.sum())} of {len(r)}.")
        say(f"  of which at a LEVERED cap (CAP > 0.60): 4b "
            f"{int(g[g.cap > 0.60].keep4b.sum())} of {len(g[g.cap > 0.60])} (B_CONST)")
    inc4b = {p.name: keep_paths(bench[p.name]["inc_rr"], bench[p.name]["spy"],
                                bench[p.name]["live"])[1] for p in panels}
    say(f"COUNTS.  the flat INCUMBENT itself passes 4b on: "
        f"{[k for k, v in inc4b.items() if v] or 'no panel'}")
    for fin in FINS:
        r8 = WF[(WF.basis == "B_CONST") & (WF.fin_bps == fin)]
        say(f"RULE 8 FIN={int(fin)}bps.  B_CONST picks clear every 4b leg incl. the OOS Sharpe "
            f"leg on {int(r8.KEEP4b_all_legs.sum())} of {len(r8)} panels; mean OOS Sharpe vs the "
            f"incumbent {r8.d_OOS_Sharpe_vs_inc.mean():+.4f}, mean OOS CAGR "
            f"{r8.d_OOS_CAGR_pp_vs_inc.mean():+.2f} pp; picks "
            f"{sorted(set(zip(r8.panel, r8.pick_cap.round(2), r8.pick_target.round(2))))}")

    # ---- G4 causality
    pan = panels[0]
    frame = build1(pan, I_N, I_H)
    inc_g, _, _, _ = run_dyn(pan, frame, k_const)
    kf = make_k_basis(inc_g, 0.10, WINDOW, 1.25)
    tprobe = pan.reb[(pan.reb > WARMUP + 300)][:25]
    pert = inc_g.copy()
    pert[int(tprobe[-1]):] += 0.05
    kf2 = make_k_basis(pert, 0.10, WINDOW, 1.25)
    dmax = max(abs(kf(int(t), None) - kf2(int(t), None)) for t in tprobe)
    gate("G4 causality: k_t is unmoved by perturbing the tape at/after the last probe row",
         float(dmax), "== 0.0", dmax == 0.0)

    GA = pd.DataFrame(GATES)
    say("\nGATES: " + ", ".join(f"{g['gate'].split()[0]}={'OK' if g['pass_'] else 'FAIL'}"
                                for g in GATES[:8])
        + f" ... {int(GA.pass_.sum())} of {len(GA)} pass")
    if not GA.pass_.all():
        say("  FAILING GATES:")
        for _, g in GA[~GA.pass_].iterrows():
            say(f"    {g.gate}: value={g.value} target={g.target}")

    G.to_csv(f"{OUT}.grid.csv", index=False)
    R.to_csv(f"{OUT}.robust.csv", index=False)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    GA.to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\nRUNTIME {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

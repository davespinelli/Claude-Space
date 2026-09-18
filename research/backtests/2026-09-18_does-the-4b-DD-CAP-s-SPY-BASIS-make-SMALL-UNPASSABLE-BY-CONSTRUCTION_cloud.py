#!/usr/bin/env python3
"""
Idea 1321 (lane cloud, 2026-09-18) — does the 4b DD CAP's SPY BASIS make SMALL UNPASSABLE BY
CONSTRUCTION?

THE PREMISE, READ FROM THE RECORD.  Idea 1301 (this run's first idea) walked N {5..40} x
H {21..252} at the incumbent's gross 0.60 and found ALL 24 SMALL cells fail the 4b drawdown
cap (shallowest -28.69% against -20.23%), while U56 clears 4b BOTH on 14 of 24 and B136 on 8.
Idea 1297 found all 15 of its vol-target rungs fail the same cap on SMALL.  But PROTOCOL's cap
is 0.60 x SPY's -33.72% — a LARGE-CAP index drawdown applied to a small-cap book whose own
beta to that index is 0.658 (1301's LEG A).  The question is not whether SMALL fails; it is
whether SMALL fails because of the BOOK or because of the YARDSTICK.

WHAT IS FROZEN AND INHERITED, NOT TUNED HERE.  The 72 (panel, N, H) books are idea 1301's
committed grid, rebuilt bit-for-bit: 3-leg composite (21/252, 0/126, 0/63), above-200d
eligibility, max_vol 0.60, GROSS 0.60, CADENCE W, min-hold H, decide-at-t / apply-at-t+1
(rule 2), warm-up 260 rows.  N {5,10,15,20,30,40} and H {21,63,126,252} are REPORTED AT EVERY
VALUE and are not this run's dials.  Gate G1 replays 1301's / 1215's U56 incumbent triple and
gate G2 replays 1301's SMALL 0-of-24.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  BASIS      {SPY, PANEL_EW}   which benchmark the 4b DD cap and CAGR floor are read against
  COST RUNG  {10, 25} bps      PROTOCOL rule 2's rung, and the record's stress rung

  4 cells per (panel, N, H); every one published in `.grid.csv`.

  THE BASES.  SPY is the record's committed yardstick, a costless buy-and-hold of the index.
  PANEL_EW is the same object built from the panel itself: equal dollars in every name priced
  at the first post-warm-up row, bought and held to the end, costless by the same convention.
  That is the like-for-like comparand — a passive, zero-turnover claim on the same universe
  the book selects from.  A DAILY-REBALANCED equal-weight index (the cross-sectional mean
  return, compounded) is published as a ROBUSTNESS ARM in `.basis.csv`, not as a third dial;
  it earns a rebalancing bonus a real passive holder does not, so it is the harder yardstick
  and is reported rather than headlined.

  WHICH VERDICT IS READ.  The VERDICT is read on the COMMITTED basis (SPY) at the COMMITTED
  rung (10 bps), exactly as PROTOCOL rule 4b stands.  PANEL_EW and 25 bps are DIAGNOSTICS that
  answer the queue's question — how much of the failure is the yardstick — and no PROTOCOL
  edit is proposed here (rule 6: any bar change is a Sunday-review matter).

PROTOCOL: rule 1 (>= 10 years, gate G0); rule 2 execution, verdict at 10 bps; rule 3 compare
against the live RULES v2 baseline AND SPY; rule 4 both KEEP paths, 2 tuned parameters and no
more; rule 8 walk-forward — (N, H) chosen on warm-up..2016-12-31 by argmax IS Sharpe at each
cost rung, 2017-2026 read ONCE, scored under BOTH bases; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

SMALL PANEL: data/small_meta.csv, drop every ticker with max_1d_move >= 1.0 first (663 of
715).  SURVIVORSHIP: current constituents of a sub-$2B screen carried back to 2010, so every
absolute SMALL number is biased UP — and so is PANEL_EW, which is built from the SAME
survivors, so the diagnostic flatters the new yardstick at least as much as the book.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-18_does-the-4b-DD-CAP-s-SPY-BASIS-make-SMALL-UNPASSABLE-BY-CONSTRUCTION_cloud.py
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
SLUG = "does-the-4b-DD-CAP-s-SPY-BASIS-make-SMALL-UNPASSABLE-BY-CONSTRUCTION"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G, I_C = 15, 126, 0.60, "W"          # the inherited incumbent, frozen
NS = [5, 10, 15, 20, 30, 40]                     # inherited from 1301, reported at every value
HS = [21, 63, 126, 252]                          # inherited from 1301, reported at every value
COSTS = [10.0, 25.0]                             # DIAL 2
BASES = ["SPY", "PANEL_EW"]                      # DIAL 1
VERDICT_BASIS, VERDICT_COST = "SPY", 10.0        # the committed reading
OOS_START, IS_END = "2017-01-01", "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70

C_U56 = dict(CAGR=0.1366, Sharpe=1.1706, MaxDD=-0.1638)   # 1215 / 1297 / 1301, at 10 bps
C_1301_SMALL_SHALLOW = -0.2869                            # 1301's shallowest SMALL cell

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=value, target=target, pass_=bool(ok)))
    say(f"    [{'PASS' if ok else 'FAIL'}] {name}: {value} (target {target})")
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
        self.lo = WARMUP
        self.i_oos = int(np.searchsorted(px.index.values, np.datetime64(OOS_START)))
        self.i_ise = int(np.searchsorted(px.index.values, np.datetime64(IS_END), side="right"))
        # ---- the panel-matched yardsticks, both costless by the record's SPY convention
        q = px[invest]
        live0 = q.iloc[self.lo].notna().values             # priced at the first scored row
        held = q.loc[:, live0].ffill()
        norm = held.iloc[self.lo]
        val = (held / norm).mean(axis=1)                   # equal dollars at lo, bought and held
        self.ew_bh = val.pct_change().fillna(0.0).values
        self.ew_drb = q.pct_change().mean(axis=1).fillna(0.0).values   # robustness arm
        self.n_bh = int(live0.sum())


def build1(pan, N, H, lag=1):
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


def run_const(pan, frame, g=I_G):
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    turn = np.zeros(T)
    out = np.zeros(T)
    curw = np.zeros(M)
    reb = np.asarray(pan.reb, dtype=np.int64)
    ends = np.append(reb[1:], T)
    for i0, i1 in zip(reb, ends):
        w0 = g * frame[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return out, turn


def at_cost(gr, tu, c):
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


def annturn(tu):
    return float(np.sum(tu) * 252.0 / len(tu)) if len(tu) else np.nan


def bmpack(r):
    h1, h2 = halves(r)
    m = triple(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


def legs4b(m, h1, h2, bmk):
    return dict(L_H1=bool(h1 > bmk["H1"]), L_H2=bool(h2 > bmk["H2"]),
                L_DD=bool(m["MaxDD"] >= DD_CAP * bmk["MaxDD"]),
                L_CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bmk["CAGR"]))


def main():
    t0 = time.time()
    say("=" * 100)
    say("IDEA 1321 (lane cloud, 2026-09-18) — does the 4b DD CAP's SPY BASIS make SMALL "
        "UNPASSABLE BY CONSTRUCTION?")
    say("=" * 100)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad]
    say(f"  SMALL filter (house rule, data/small_meta.csv): drops {len(bad)}, keeps {len(inv)} "
        f"of {len(pxS.columns)-1} priced")
    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL663", pxS, inv)]
    for p in panels:
        say(f"    {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y), {len(p.invest)} names, {p.n_bh} in the PANEL_EW "
            f"buy-and-hold, OOS from row {p.i_oos}")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)

    # ------------------------------------------------------------------ the two yardsticks
    say("")
    say("-" * 100)
    say("THE YARDSTICKS — both costless, both full-sample post-warm-up (rule 3's convention)")
    say("-" * 100)
    BM, BM_OOS, LIVE, LIVE_OOS, ARM = {}, {}, {}, {}, []
    for p in panels:
        lo, o = p.lo, p.i_oos - p.lo
        streams = dict(SPY=p.spy[lo:], PANEL_EW=p.ew_bh[lo:])
        for b, s in streams.items():
            BM[(p.name, b)] = bmpack(s)
            BM_OOS[(p.name, b)] = bmpack(s[o:])
        drb = p.ew_drb[lo:]
        ARM.append(dict(panel=p.name, arm="PANEL_EW_DAILY_REBAL", **bmpack(drb),
                        OOS_CAGR=cagr(drb[o:]), OOS_Sharpe=sharpe(drb[o:]),
                        OOS_MaxDD=mdd(drb[o:]),
                        dd_cap=DD_CAP * mdd(drb), cagr_floor=CAGR_FLOOR * cagr(drb)))
        lr = backtest(p.px, rules_v2_weights(p.px), cost_bps=VERDICT_COST,
                      freq="W")["returns"].fillna(0.0).values[lo:]
        LIVE[p.name], LIVE_OOS[p.name] = bmpack(lr), bmpack(lr[o:])
        for b in BASES:
            k = BM[(p.name, b)]
            say(f"  {p.name:9s} {b:9s} {k['CAGR']:7.2%} / {k['Sharpe']:.4f} / {k['MaxDD']:7.2%} "
                f"(H1 {k['H1']:.4f} H2 {k['H2']:.4f}) -> 4b cap {DD_CAP*k['MaxDD']:7.2%}, "
                f"floor {CAGR_FLOOR*k['CAGR']:6.2%}")
        a = ARM[-1]
        say(f"  {p.name:9s} [arm]  DAILY-REBAL EW {a['CAGR']:7.2%} / {a['Sharpe']:.4f} / "
            f"{a['MaxDD']:7.2%} -> cap {a['dd_cap']:7.2%}, floor {a['cagr_floor']:6.2%}")
    pd.DataFrame(ARM).to_csv(f"{OUT}.basis.csv", index=False)

    # ------------------------------------------------------------------ the 4-cell dial grid
    say("")
    say("-" * 100)
    say(f"THE DIAL GRID — BASIS {BASES} x COST {COSTS} bps over the 72 inherited books "
        f"(N {NS} x H {HS} x 3 panels), {len(BASES)*len(COSTS)*72} scorings")
    say("-" * 100)
    rows = []
    ser = {}
    for p in panels:
        lo, o = p.lo, p.i_oos - p.lo
        for N in NS:
            for H in HS:
                gr, tu = run_const(p, build1(p, N, H), I_G)
                for c in COSTS:
                    r = at_cost(gr, tu, c)[lo:]
                    ser[(p.name, N, H, c)] = r
                    m, (h1, h2) = triple(r), halves(r)
                    ris, ros = r[: p.i_ise - lo], r[o:]
                    mo, l4 = triple(ros), LIVE[p.name]
                    for b in BASES:
                        bm, bo = BM[(p.name, b)], BM_OOS[(p.name, b)]
                        L = legs4b(m, h1, h2, bm)
                        Lo = dict(L_OOS_S=bool(mo["Sharpe"] > bo["Sharpe"]),
                                  L_OOS_DD=bool(mo["MaxDD"] >= DD_CAP * bo["MaxDD"]),
                                  L_OOS_CAGR=bool(mo["CAGR"] >= CAGR_FLOOR * bo["CAGR"]))
                        k4b = all(L.values())
                        k4bo = all(Lo.values())
                        rows.append(dict(
                            panel=p.name, basis=b, cost=c, N=N, H=H, gross=I_G,
                            CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                            turn=annturn(tu[lo:]),
                            IS_Sharpe=sharpe(ris), OOS_CAGR=mo["CAGR"],
                            OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                            dd_cap=DD_CAP * bm["MaxDD"], cagr_floor=CAGR_FLOOR * bm["CAGR"],
                            oos_dd_cap=DD_CAP * bo["MaxDD"],
                            oos_cagr_floor=CAGR_FLOOR * bo["CAGR"],
                            keep4a=bool(h1 > l4["H1"] and h2 > l4["H2"]
                                        and m["MaxDD"] >= l4["MaxDD"]),
                            keep4b_full=k4b, keep4b_oos=k4bo,
                            keep4b_both=bool(k4b and k4bo), **L, **Lo))
        say(f"  {p.name}: {len(NS)*len(HS)} books x {len(COSTS)} rungs x {len(BASES)} bases")
    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)

    # ------------------------------------------------------------------ replay gates
    say("")
    say("-" * 100)
    say("REPLAY GATES against idea 1301's / 1215's committed numbers (nothing tuned on them)")
    say("-" * 100)
    a = G[(G.panel == "U56") & (G.N == I_N) & (G.H == I_H) & (G.cost == 10.0)
          & (G.basis == "SPY")].iloc[0]
    d = max(abs(a.CAGR - C_U56["CAGR"]), abs(a.Sharpe - C_U56["Sharpe"]),
            abs(a.MaxDD - C_U56["MaxDD"]))
    gate("G1 U56 incumbent at 10 bps replays 13.66% / 1.1706 / -16.38%",
         f"{a.CAGR:.4%} / {a.Sharpe:.4f} / {a.MaxDD:.4%} (max|dev| {d:.2e})",
         "max|dev| <= 5e-3", d <= 5e-3)
    sm = G[(G.panel == "SMALL663") & (G.cost == 10.0) & (G.basis == "SPY")]
    gate("G2 SMALL at 10 bps on the SPY basis replays 1301's 0 of 24 4b-full passes",
         f"{int(sm.keep4b_full.sum())} of {len(sm)}", "== 0 of 24",
         int(sm.keep4b_full.sum()) == 0 and len(sm) == 24)
    gate("G2b SMALL's shallowest cell replays 1301's -28.69%",
         f"{sm.MaxDD.max():.4%}", "|dev| <= 5e-3",
         abs(sm.MaxDD.max() - C_1301_SMALL_SHALLOW) <= 5e-3)
    u = G[(G.panel == "U56") & (G.cost == 10.0) & (G.basis == "SPY")]
    b1 = G[(G.panel == "B136") & (G.cost == 10.0) & (G.basis == "SPY")]
    gate("G3 U56 / B136 replay 1301's 4b BOTH counts of 14 / 8",
         f"{int(u.keep4b_both.sum())} / {int(b1.keep4b_both.sum())}", "== 14 / 8",
         int(u.keep4b_both.sum()) == 14 and int(b1.keep4b_both.sum()) == 8)
    gate("G4 the SPY yardstick is identical on all three panels (one index, one tape)",
         f"MaxDD {sorted({round(BM[(p.name,'SPY')]['MaxDD'],4) for p in panels})}",
         "one value", len({round(BM[(p.name, "SPY")]["MaxDD"], 4) for p in panels}) == 1)

    # ------------------------------------------------------------------ the queue's question
    say("")
    say("-" * 100)
    say("THE QUEUE'S QUESTION — how much of SMALL's 4b failure is the BOOK and how much the "
        "YARDSTICK?")
    say("-" * 100)
    say("      panel   basis      cost |  cap      floor  | 4b-full 4b-OOS 4b-BOTH of 24 | "
        "leg fails: H1  H2  DD CAGR")
    tab = []
    for p in panels:
        for b in BASES:
            for c in COSTS:
                s = G[(G.panel == p.name) & (G.basis == b) & (G.cost == c)]
                f = {L: int((~s[L]).sum()) for L in ("L_H1", "L_H2", "L_DD", "L_CAGR")}
                tab.append(dict(panel=p.name, basis=b, cost=c, cap=s.dd_cap.iloc[0],
                                floor=s.cagr_floor.iloc[0],
                                n4b_full=int(s.keep4b_full.sum()),
                                n4b_oos=int(s.keep4b_oos.sum()),
                                n4b_both=int(s.keep4b_both.sum()),
                                n4a=int(s.keep4a.sum()), **f))
                say(f"    {p.name:9s} {b:9s} {c:4.0f} | {s.dd_cap.iloc[0]:7.2%} "
                    f"{s.cagr_floor.iloc[0]:6.2%} | {int(s.keep4b_full.sum()):7d} "
                    f"{int(s.keep4b_oos.sum()):6d} {int(s.keep4b_both.sum()):7d}      | "
                    f"{f['L_H1']:11d} {f['L_H2']:3d} {f['L_DD']:3d} {f['L_CAGR']:4d}")
    T = pd.DataFrame(tab)
    T.to_csv(f"{OUT}.summary.csv", index=False)

    sS = T[(T.panel == "SMALL663") & (T.cost == 10.0)]
    spy_r = sS[sS.basis == "SPY"].iloc[0]
    ew_r = sS[sS.basis == "PANEL_EW"].iloc[0]
    say("")
    say(f"  SMALL663 at 10 bps: the DD cap moves {spy_r.cap:.2%} (SPY) -> {ew_r.cap:.2%} "
        f"(PANEL_EW), i.e. {100*(ew_r.cap-spy_r.cap):+.2f} pp, and the CAGR floor "
        f"{spy_r.floor:.2%} -> {ew_r.floor:.2%} ({100*(ew_r.floor-spy_r.floor):+.2f} pp)")
    say(f"  4b-full passes go {int(spy_r.n4b_full)} of 24 -> {int(ew_r.n4b_full)} of 24; "
        f"4b BOTH {int(spy_r.n4b_both)} -> {int(ew_r.n4b_both)}; "
        f"DD-leg failures {int(spy_r.L_DD)} of 24 -> {int(ew_r.L_DD)} of 24")
    gate("G5 SMALL 4b-full passes on the PANEL_EW basis at 10 bps",
         f"{int(ew_r.n4b_full)} of 24", "reported either way", True)
    gate("G6 SMALL DD-leg failures on the PANEL_EW basis at 10 bps",
         f"{int(ew_r.L_DD)} of 24", "reported either way", True)
    # decompose: how many of SMALL's 24 SPY-basis failures survive the yardstick change?
    kspy = G[(G.panel == "SMALL663") & (G.basis == "SPY") & (G.cost == 10.0)]
    kew = G[(G.panel == "SMALL663") & (G.basis == "PANEL_EW") & (G.cost == 10.0)]
    m = kspy.merge(kew, on=["N", "H"], suffixes=("_spy", "_ew"))
    flipped = int(((~m.keep4b_full_spy) & (m.keep4b_full_ew)).sum())
    dd_flip = int(((~m.L_DD_spy) & (m.L_DD_ew)).sum())
    say(f"  of SMALL's {int((~m.keep4b_full_spy).sum())} SPY-basis 4b-full failures, "
        f"{flipped} become passes on the panel-matched basis; of its "
        f"{int((~m.L_DD_spy).sum())} DD-leg failures, {dd_flip} clear the panel-matched cap")

    # ------------------------------------------------------------------ rule 8
    say("")
    say("-" * 100)
    say(f"RULE 8 WALK-FORWARD — (N, H) by argmax IS Sharpe on warm-up..{IS_END} at each cost "
        f"rung (basis-invariant by construction); {OOS_START}.. read ONCE, scored under BOTH bases")
    say("-" * 100)
    wf = []
    for p in panels:
        for c in COSTS:
            s = G[(G.panel == p.name) & (G.cost == c) & (G.basis == "SPY")]
            pick = s.loc[s.IS_Sharpe.idxmax()]
            anc = s[(s.N == I_N) & (s.H == I_H)].iloc[0]
            l4 = LIVE_OOS[p.name]
            say(f"  {p.name:9s} {c:4.0f} bps  pick N={int(pick.N):2d} H={int(pick.H):3d} "
                f"(IS Sharpe {pick.IS_Sharpe:.4f})")
            say(f"    OOS pick   {pick.OOS_CAGR:7.2%} / {pick.OOS_Sharpe:.4f} / "
                f"{pick.OOS_MaxDD:7.2%}   | OOS anchor N15/H126 {anc.OOS_CAGR:7.2%} / "
                f"{anc.OOS_Sharpe:.4f} / {anc.OOS_MaxDD:7.2%} "
                f"(pick - anchor {pick.OOS_Sharpe - anc.OOS_Sharpe:+.4f})")
            say(f"    OOS v2     {l4['CAGR']:7.2%} / {l4['Sharpe']:.4f} / {l4['MaxDD']:7.2%}")
            for b in BASES:
                row = G[(G.panel == p.name) & (G.cost == c) & (G.basis == b)
                        & (G.N == pick.N) & (G.H == pick.H)].iloc[0]
                bo = BM_OOS[(p.name, b)]
                say(f"    vs {b:9s} OOS {bo['CAGR']:7.2%} / {bo['Sharpe']:.4f} / "
                    f"{bo['MaxDD']:7.2%} (cap {DD_CAP*bo['MaxDD']:.2%}, "
                    f"floor {CAGR_FLOOR*bo['CAGR']:.2%}) -> 4b full {row.keep4b_full}, "
                    f"4b OOS {row.keep4b_oos}, BOTH {row.keep4b_both}, 4a {row.keep4a}")
                wf.append(dict(panel=p.name, cost=c, basis=b, pick_N=int(pick.N),
                               pick_H=int(pick.H), IS_Sharpe=pick.IS_Sharpe,
                               OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                               OOS_MaxDD=pick.OOS_MaxDD,
                               anc_OOS_CAGR=anc.OOS_CAGR, anc_OOS_Sharpe=anc.OOS_Sharpe,
                               anc_OOS_MaxDD=anc.OOS_MaxDD,
                               d_vs_anchor=pick.OOS_Sharpe - anc.OOS_Sharpe,
                               bm_OOS_CAGR=bo["CAGR"], bm_OOS_Sharpe=bo["Sharpe"],
                               bm_OOS_MaxDD=bo["MaxDD"],
                               v2_OOS_CAGR=l4["CAGR"], v2_OOS_Sharpe=l4["Sharpe"],
                               v2_OOS_MaxDD=l4["MaxDD"],
                               keep4a=bool(row.keep4a), keep4b_full=bool(row.keep4b_full),
                               keep4b_oos=bool(row.keep4b_oos),
                               keep4b_both=bool(row.keep4b_both)))
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    gate("G7 rule 8 run at every (panel, cost, basis)", f"{len(W)}",
         f"== {len(panels)*len(COSTS)*len(BASES)}", len(W) == len(panels) * len(COSTS) * len(BASES))
    vv = W[(W.basis == VERDICT_BASIS) & (W.cost == VERDICT_COST)]
    gate("G8 rule-8 picks clearing 4b BOTH on the COMMITTED basis and rung",
         f"{int(vv.keep4b_both.sum())} of {len(vv)}", "reported either way", True)
    gate("G9 4a passes anywhere in the grid", int(G.keep4a.sum()), "reported either way", True)

    say("")
    say("-" * 100)
    say("THE COMMITTED READING (basis SPY, 10 bps) — the only verdict this run reads")
    say("-" * 100)
    v = T[(T.basis == VERDICT_BASIS) & (T.cost == VERDICT_COST)]
    for _, x in v.iterrows():
        say(f"  {x.panel:9s} 4a {int(x.n4a):2d}  4b full {int(x.n4b_full):2d}  "
            f"4b OOS {int(x.n4b_oos):2d}  4b BOTH {int(x.n4b_both):2d}   of 24")

    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say("")
    say(f"GATES: {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass")
    say(f"elapsed {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

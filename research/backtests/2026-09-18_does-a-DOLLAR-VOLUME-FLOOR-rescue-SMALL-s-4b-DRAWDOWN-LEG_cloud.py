#!/usr/bin/env python3
"""
Idea 1343 (lane cloud, 2026-09-18) — does a DOLLAR-VOLUME FLOOR rescue SMALL's 4b DRAWDOWN LEG?

THE PREMISE, READ FROM THE RECORD.  SMALL is the panel that fails 4b everywhere.  Idea 1305
(this lane, today) measured its flat g=0.60 incumbent at 7.06% / 0.5202 / -33.35% weekly
against a 4b drawdown cap of -20.23%, and idea 1215 found the DD cap is the modal binder of the
whole family.  The record has always read that as a CONCENTRATION or an EXPOSURE fact and has
walked N and gross accordingly.  But the SMALL panel is screened on PRICE ALONE: its median
name trades about $6.4M/day and its 25th percentile about $2.9M/day, so the book is partly
holding names real capital could not size into — and thin names are exactly where gap risk,
and therefore drawdown, lives.  The LIQUIDITY axis has never been walked.  This run walks it.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  DV    {$0, $1M, $3M, $10M, $30M}    DIAL 1 — 63-day MEDIAN dollar volume floor at admission
  N     {10, 15, 20, 30}              DIAL 2 — 15 is the incumbent's value

  20 cells on SMALL, EVERY ONE published in `.grid.csv`.  H = 126, gross = 0.60, WEEKLY,
  10 bps, t+1 — the incumbent's frozen values.  U56 and B136 are run at DV = $0 across the
  same N ladder as UN-SCREENED CONTROLS (`baseline.load_volume` serves the small panel only),
  so the N axis can be read on three panels even though the DV axis exists on one.

  THE SCREEN, STATED.  dv_t = 63-day rolling MEDIAN of (close x share volume), read at the
  SELECTION row t-1 and applied at t (rule 2: nothing at or after the application row is seen).
  A median, not a mean, so one halt or one block print cannot admit a name.  The floor gates
  ADMISSION only; a name already held exits on the record's own min-hold rule (H) or when it
  stops being priced, exactly as every other eligibility gate in this family behaves.  That is
  the record's convention and it is stated here rather than assumed.

  A DV FLOOR IS NOT A FREE LUNCH: it shrinks the pool, so it is also an N-vs-pool experiment.
  Every cell therefore publishes `pool_mean` (names clearing the floor per rebalance row) and
  `fill` (realised holdings / N), and no verdict is read off a cell whose fill is short.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {SMALL, U56, B136} (rule 9); both KEEP paths at every
cell; the IS and OOS windows; the halves; turnover and its 10 bps drag.

PROTOCOL: rule 1 (>= 10 years, gate G0); rule 2 execution t+1, 10 bps, no leverage; rule 3
compare against the live RULES v2 baseline AND SPY; rule 4 both KEEP paths, 2 tuned parameters
and no more; rule 8 walk-forward — (DV, N) chosen on warm-up..2016-12-31 by argmax IS Sharpe,
2017-2026 read ONCE; rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py are NOT modified.

SURVIVORSHIP, AND WHY IT BITES HARDER HERE (rule 9).  SMALL663 is a CURRENT-constituent sub-$2B
screen carried back to 2010: the names that went to zero are not in it, so its levels are an
upper bound.  A DV floor interacts with that bias in a stated direction — it removes the
thinnest survivors, which are disproportionately the names whose *survival* was least likely —
so a DD improvement from the floor is partly a re-selection of the surviving cohort and is
read as an UPPER bound on the real effect, never a lower one.

CROSS-RUN REPLAY (gates G1, G2): the DV=$0 / N=15 cells must reproduce idea 1305's committed
SMALL flat control (7.06% / 0.5202 / -33.35%) and idea 1215's committed U56 incumbent
(13.66% / 1.1706 / -16.38%) to < 5e-3.

Runs standalone and offline (no network; committed price and volume caches only):
  python research/backtests/2026-09-18_does-a-DOLLAR-VOLUME-FLOOR-rescue-SMALL-s-4b-DRAWDOWN-LEG_cloud.py
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
from baseline import load_universe, load_volume, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-18"
SLUG = "does-a-DOLLAR-VOLUME-FLOOR-rescue-SMALL-s-4b-DRAWDOWN-LEG"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP, MAXVOL = 260, 0.60
COST = 10.0
LEGS = [(21, 252), (0, 126), (0, 63)]
I_H, I_G, I_C = 126, 0.60, "W"                 # frozen incumbent values
DVS = [0.0, 1e6, 3e6, 1e7, 3e7]                # DIAL 1
NS = [10, 15, 20, 30]                          # DIAL 2
DV_WIN = 63                                    # the median's window, frozen
OOS_START, IS_END = "2017-01-01", "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
C1305_SMALL = dict(CAGR=0.0706, Sharpe=0.5202, MaxDD=-0.3335)
C1215_U56 = dict(CAGR=0.1366, Sharpe=1.1706, MaxDD=-0.1638)

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
    def __init__(self, name, px, invest, dv=None):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        m = rebalance_mask(px.index, I_C).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)          # (T x K) over the investables
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        # dv: (T x K) 63d median dollar volume over the investables, or None (no volume served)
        self.dv = dv


def build(pan, N, H, dv_floor, lag=1, sub=None):
    """The record's min-hold selection frame at GROSS=1.0, with a DOLLAR-VOLUME floor applied
    at ADMISSION only.  lag=1 is rule 2.  `sub` is an optional fixed boolean sub-pool mask over
    the investables (the POOL-SIZE null control; it is NOT a dial).  Returns the frame, the
    per-rebalance pool size (names clearing every gate at the selection row), the realised
    holding count, and an ADMISSION-AUDIT violation count (names admitted below the floor)."""
    reb = pan.reb
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    pool, fill, viol = [], [], 0
    for i, t in enumerate(reb):
        ts = max(t - lag, 0)
        ok = pan.elig[ts] & pr[ts]
        if dv_floor > 0.0 and pan.dv is not None:
            ok = ok & (pan.dv[ts] >= dv_floor)
        if sub is not None:
            ok = ok & sub
        pool.append(int(ok.sum()))
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = pan.rank_key[ts].copy()
            k[~ok] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
            if dv_floor > 0.0 and pan.dv is not None and not (pan.dv[ts, c] >= dv_floor):
                viol += 1                                  # ADMISSION AUDIT (gate G4)
        cur = new
        sel = np.flatnonzero(cur >= 0)
        fill.append(len(sel))
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W, np.array(pool, float), np.array(fill, float), viol


def run(pan, frame, g=I_G):
    """Constant-gross runner (1297's, with k frozen).  Returns (gross returns, turnover)."""
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
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(L_H1=bool(h1 > bm["H1"]), L_H2=bool(h2 > bm["H2"]),
                L_DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                L_CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return k4a, bool(all(legs.values())), m, h1, h2, legs


def money(x):
    return "$0" if x == 0 else (f"${x/1e6:.0f}M")


def main():
    t0 = time.time()
    say("=" * 112)
    say("IDEA 1343 (lane cloud, 2026-09-18) — does a DOLLAR-VOLUME FLOOR rescue SMALL's 4b "
        "DRAWDOWN LEG?")
    say("DIALS: DV {$0,$1M,$3M,$10M,$30M} x N {10,15,20,30} at the frozen incumbent "
        "(H=126, gross 0.60, weekly, 10 bps, t+1).  NO leverage.")
    say("=" * 112)

    pxS = load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(md.loc[md["max_1d_move"] >= 1.0, "ticker"].astype(str))
    mv = pxS.pct_change().abs().max()
    invS = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    say(f"  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0 -> {len(invS)} investables of {len(pxS.columns)-1} priced.")

    vol = load_volume(small=True).reindex(index=pxS.index, columns=invS)
    dollar = (vol * pxS[invS]).astype(float)
    dvS = dollar.rolling(DV_WIN, min_periods=DV_WIN).median()
    gate("G7 the DV median is CAUSAL — row t uses only rows <= t (rolling, no centring, "
         "no shift(-k))", f"rolling({DV_WIN}).median(), read at t-1, applied at t",
         "causal by construction", True)
    dvS_v = np.nan_to_num(dvS.values, nan=-1.0)          # NaN during warm-up -> admits nothing

    pxU = load_universe()
    pxB = load_universe(broad=True)
    panels = [Panel("SMALL", pxS, invS, dvS_v),
              Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"])]
    say(f"  PANELS: SMALL {len(invS)} names (DV axis lives here), U56 {len(pxU.columns)-1} and "
        f"B136 {len(pxB.columns)-1} as UN-SCREENED controls "
        f"(baseline.load_volume serves the small panel only).")
    for p in panels:
        say(f"    {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y), {len(p.reb)} weekly rebalances")
    gate("G0 min sample >= 10 years (rule 1)", min(len(p.idx) for p in panels) / 252.0,
         ">= 10.0", min(len(p.idx) for p in panels) / 252.0 >= 10.0)

    say(f"\n  SMALL liquidity, {DV_WIN}d median dollar volume on the last row: "
        + ", ".join(f"p{q}={money(np.nanpercentile(dvS.iloc[-1].values, q))}"
                    for q in (10, 25, 50, 75, 90)))

    grid, wf_rows, null_rows = [], [], []
    admit_viol = 0
    bench = {}

    for pan in panels:
        n = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        i_is0, i_is1 = WARMUP, i_oos
        spy = pan.spy[WARMUP:]
        liveres = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")
        live = liveres["returns"].values[WARMUP:]
        bm, lv = bmpack(spy), bmpack(live)
        bench[pan.name] = dict(spy=bm, live=lv, spyO=bmpack(pan.spy[i_oos:]),
                               liveO=bmpack(liveres["returns"].values[i_oos:]), i_oos=i_oos)
        say(f"\n  [{pan.name}] SPY: CAGR {bm['CAGR']:.2%} Sharpe {bm['Sharpe']:.4f} MaxDD "
            f"{bm['MaxDD']:.2%} H1/H2 {bm['H1']:.4f}/{bm['H2']:.4f}  ->  4b DD cap "
            f"{DD_CAP*bm['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*bm['CAGR']:.2%}")
        say(f"        RULES v2 live: CAGR {lv['CAGR']:.2%} Sharpe {lv['Sharpe']:.4f} MaxDD "
            f"{lv['MaxDD']:.2%} H1/H2 {lv['H1']:.4f}/{lv['H2']:.4f}")

        dvs = DVS if pan.name == "SMALL" else [0.0]
        for dv in dvs:
            for N in NS:
                frame, pool, fill, viol = build(pan, N, I_H, dv)
                admit_viol += viol
                g, tu = run(pan, frame)
                rr = at_cost(g, tu)
                r = rr[WARMUP:]
                ka, kb, m, h1, h2, legs = keep_paths(r, bm, lv)
                mo = triple(rr[i_oos:])
                t_ann = annturn(tu, WARMUP, n)
                grid.append(dict(panel=pan.name, dv=dv, N=N, H=I_H, gross=I_G, cadence=I_C,
                                 CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                 H1=h1, H2=h2, vol_real=annvol(r), turn=t_ann,
                                 cost_drag_bp=t_ann * COST,
                                 pool_mean=float(pool.mean()), pool_min=float(pool.min()),
                                 fill_mean=float(fill.mean()), fill_ratio=float(fill.mean() / N),
                                 OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                 OOS_MaxDD=mo["MaxDD"], IS_Sharpe=sharpe(rr[i_is0:i_is1]),
                                 keep4a=ka, keep4b=kb, **legs))

    G = pd.DataFrame(grid)

    r0 = G[(G.panel == "SMALL") & (G.dv == 0.0) & (G.N == 15)].iloc[0]
    d = max(abs(r0.CAGR - C1305_SMALL["CAGR"]), abs(r0.Sharpe - C1305_SMALL["Sharpe"]),
            abs(r0.MaxDD - C1305_SMALL["MaxDD"]))
    gate("G1 SMALL DV=$0 N=15 replays idea 1305's committed flat control "
         "7.06%/0.5202/-33.35%", float(d), "< 5e-3", d < 5e-3)
    r1 = G[(G.panel == "U56") & (G.N == 15)].iloc[0]
    d1 = max(abs(r1.CAGR - C1215_U56["CAGR"]), abs(r1.Sharpe - C1215_U56["Sharpe"]),
             abs(r1.MaxDD - C1215_U56["MaxDD"]))
    gate("G2 U56 N=15 replays idea 1215's committed incumbent 13.66%/1.1706/-16.38%",
         float(d1), "< 5e-3", d1 < 5e-3)
    sm = G[G.panel == "SMALL"]
    mono = all(sm[sm.N == N].sort_values("dv").pool_mean.is_monotonic_decreasing for N in NS)
    gate("G3 the DV floor is MONOTONE — the admitted pool never grows as the floor rises",
         int(mono), "True", mono)
    gate("G4 ADMISSION AUDIT — no name is ever admitted below the floor in force at its "
         "selection row", admit_viol, "== 0", admit_viol == 0)

    # ================================================================ every cell
    say("\n" + "=" * 112)
    say("EVERY CELL.  20 SMALL cells (DV x N) + 8 un-screened control cells, all in .grid.csv")
    say("=" * 112)
    for pan in panels:
        b = bench[pan.name]
        say(f"\n  [{pan.name}]  4b DD cap {DD_CAP*b['spy']['MaxDD']:.2%}, CAGR floor "
            f"{CAGR_FLOOR*b['spy']['CAGR']:.2%}, SPY H1/H2 {b['spy']['H1']:.3f}/"
            f"{b['spy']['H2']:.3f}")
        say("      DV   N |    CAGR   Sharpe    MaxDD   vol     H1     H2 | turn  drag | pool "
            "fill | 4a 4b | legs H1/H2/DD/CAGR | OOS CAGR/Sharpe/MaxDD")
        for _, r in G[G.panel == pan.name].iterrows():
            say(f"   {money(r.dv):>6} {int(r.N):3d} | {r.CAGR:7.2%} {r.Sharpe:8.4f} "
                f"{r.MaxDD:8.2%} {r.vol_real:5.1%} {r.H1:6.3f} {r.H2:6.3f} | {r.turn:5.2f} "
                f"{r.cost_drag_bp:5.1f} | {r.pool_mean:5.0f} {r.fill_ratio:4.0%} | "
                f"{int(r.keep4a)}  {int(r.keep4b)} | {int(r.L_H1)}{int(r.L_H2)}"
                f"{int(r.L_DD)}{int(r.L_CAGR)}     | {r.OOS_CAGR:7.2%}/{r.OOS_Sharpe:.4f}/"
                f"{r.OOS_MaxDD:7.2%}")

    # ================================================================ does the floor move DD?
    say("\n" + "=" * 112)
    say("DOES THE FLOOR MOVE THE DRAWDOWN LEG?  SMALL, MaxDD and its 4b cap by DV at each N")
    say("=" * 112)
    cap = DD_CAP * bench["SMALL"]["spy"]["MaxDD"]
    say(f"  SMALL 4b DD cap = {cap:.2%};  CAGR floor = "
        f"{CAGR_FLOOR*bench['SMALL']['spy']['CAGR']:.2%}")
    say("     N |" + "".join(f"  {money(dv):>7}" for dv in DVS) + "  |  best MaxDD  gap to cap")
    for N in NS:
        row = sm[sm.N == N].set_index("dv")
        vals = [row.loc[dv, "MaxDD"] for dv in DVS]
        best = max(vals)
        say(f"   {N:3d} |" + "".join(f"  {v:7.2%}" for v in vals) +
            f"  |   {best:7.2%}   {(best-cap)*100:+6.2f}pp")
    say("\n  and what the floor costs in CAGR (SMALL):")
    say("     N |" + "".join(f"  {money(dv):>7}" for dv in DVS))
    for N in NS:
        row = sm[sm.N == N].set_index("dv")
        say(f"   {N:3d} |" + "".join(f"  {row.loc[dv,'CAGR']:7.2%}" for dv in DVS))
    say("\n  admitted pool (names clearing every gate per rebalance row):")
    say("     N |" + "".join(f"  {money(dv):>7}" for dv in DVS))
    for N in NS:
        row = sm[sm.N == N].set_index("dv")
        say(f"   {N:3d} |" + "".join(f"  {row.loc[dv,'pool_mean']:7.0f}" for dv in DVS))

    # ============================================ is it LIQUIDITY or just a SMALLER POOL?
    say("\n" + "=" * 112)
    say("THE CONFOUND, PRICED.  A DV floor shrinks the pool, and a smaller pool is a different "
        "book for reasons that have nothing")
    say("to do with liquidity.  NULL CONTROL (not a dial): at each rung's realised pool size, "
        "draw 20 FIXED RANDOM sub-pools of")
    say("that size from the UN-SCREENED investables, run the same N=15 book, and report the "
        "median.  The DV effect is the gap.")
    say("=" * 112)
    panS = panels[0]
    K = len(panS.invest)
    bmS, lvS = bench["SMALL"]["spy"], bench["SMALL"]["live"]
    nS, ioS = len(panS.idx), bench["SMALL"]["i_oos"]
    say("      DV |  pool | DV-screened CAGR/Sharpe/MaxDD | random-pool median CAGR/Sharpe/MaxDD"
        " | DV effect: dCAGR dSharpe dMaxDD")
    for dv in DVS:
        cell = G[(G.panel == "SMALL") & (G.dv == dv) & (G.N == 15)].iloc[0]
        k = int(round(cell.pool_mean / cell.pool_mean * 0.0)) if False else None
        # pool size to match: the SCREENED panel's mean admitted count, as a share of the
        # un-screened mean admitted count, applied to the full investable list
        share = cell.pool_mean / G[(G.panel == "SMALL") & (G.dv == 0.0)
                                   & (G.N == 15)].iloc[0].pool_mean
        k = max(int(round(share * K)), 15)
        cs, ss, ds = [], [], []
        for seed in range(20):
            rng = np.random.default_rng(1000 + seed)
            mask = np.zeros(K, dtype=bool)
            mask[rng.choice(K, size=k, replace=False)] = True
            fr, _, _, _ = build(panS, 15, I_H, 0.0, sub=mask)
            g_, tu_ = run(panS, fr)
            r_ = at_cost(g_, tu_)[WARMUP:]
            m_ = triple(r_)
            cs.append(m_["CAGR"]); ss.append(m_["Sharpe"]); ds.append(m_["MaxDD"])
        mc, ms_, md_ = float(np.median(cs)), float(np.median(ss)), float(np.median(ds))
        null_rows.append(dict(dv=dv, pool_share=share, k_names=k, n_seeds=20,
                              dv_CAGR=cell.CAGR, dv_Sharpe=cell.Sharpe, dv_MaxDD=cell.MaxDD,
                              null_CAGR=mc, null_Sharpe=ms_, null_MaxDD=md_,
                              null_CAGR_lo=float(np.percentile(cs, 5)),
                              null_CAGR_hi=float(np.percentile(cs, 95)),
                              null_MaxDD_lo=float(np.percentile(ds, 5)),
                              null_MaxDD_hi=float(np.percentile(ds, 95)),
                              dv_effect_CAGR_pp=(cell.CAGR - mc) * 100,
                              dv_effect_Sharpe=cell.Sharpe - ms_,
                              dv_effect_MaxDD_pp=(cell.MaxDD - md_) * 100))
        say(f"   {money(dv):>6} | {k:5d} |  {cell.CAGR:7.2%} {cell.Sharpe:8.4f} "
            f"{cell.MaxDD:8.2%}        |  {mc:7.2%} {ms_:8.4f} {md_:8.2%}             "
            f"|  {(cell.CAGR-mc)*100:+6.2f} {cell.Sharpe-ms_:+8.4f} {(cell.MaxDD-md_)*100:+6.2f}")
    NL = pd.DataFrame(null_rows)

    # ================================================================ rule 8
    say("\n" + "=" * 112)
    say("RULE 8 WALK-FORWARD — (DV, N) chosen on warm-up..2016-12-31 by argmax IS Sharpe; "
        "2017-2026 READ ONCE")
    say("=" * 112)
    for pan in panels:
        b = bench[pan.name]
        sub = G[G.panel == pan.name]
        pick = sub.loc[sub.IS_Sharpe.idxmax()]
        anchor = sub[(sub.dv == 0.0) & (sub.N == 15)].iloc[0]
        oos_leg = bool(pick.OOS_Sharpe > b["spyO"]["Sharpe"])
        wf_rows.append(dict(
            panel=pan.name, pick_dv=pick.dv, pick_N=int(pick.N), IS_Sharpe=pick.IS_Sharpe,
            OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
            anchor_OOS_CAGR=anchor.OOS_CAGR, anchor_OOS_Sharpe=anchor.OOS_Sharpe,
            anchor_OOS_MaxDD=anchor.OOS_MaxDD,
            spy_OOS_CAGR=b["spyO"]["CAGR"], spy_OOS_Sharpe=b["spyO"]["Sharpe"],
            spy_OOS_MaxDD=b["spyO"]["MaxDD"],
            live_OOS_CAGR=b["liveO"]["CAGR"], live_OOS_Sharpe=b["liveO"]["Sharpe"],
            live_OOS_MaxDD=b["liveO"]["MaxDD"],
            d_OOS_Sharpe_vs_anchor=pick.OOS_Sharpe - anchor.OOS_Sharpe,
            d_OOS_MaxDD_pp_vs_anchor=(pick.OOS_MaxDD - anchor.OOS_MaxDD) * 100,
            d_OOS_CAGR_pp_vs_anchor=(pick.OOS_CAGR - anchor.OOS_CAGR) * 100,
            full_keep4a=bool(pick.keep4a), full_keep4b=bool(pick.keep4b),
            oos_sharpe_leg=oos_leg, oos_dd_leg=bool(pick.OOS_MaxDD >= DD_CAP*b["spyO"]["MaxDD"]),
            KEEP4b_all_legs=bool(pick.keep4b and oos_leg)))
        say(f"\n  [{pan.name}] pick DV={money(pick.dv)} N={int(pick.N)} "
            f"(IS Sharpe {pick.IS_Sharpe:.4f})")
        say(f"      OOS pick    {pick.OOS_CAGR:7.2%} / {pick.OOS_Sharpe:.4f} / "
            f"{pick.OOS_MaxDD:7.2%}   4b full-sample={int(bool(pick.keep4b))} OOS-Sharpe "
            f"leg={int(oos_leg)} -> 4b all legs={int(bool(pick.keep4b and oos_leg))}")
        say(f"      OOS anchor  {anchor.OOS_CAGR:7.2%} / {anchor.OOS_Sharpe:.4f} / "
            f"{anchor.OOS_MaxDD:7.2%}   (DV=$0, N=15 — the record's own book)")
        say(f"      OOS SPY     {b['spyO']['CAGR']:7.2%} / {b['spyO']['Sharpe']:.4f} / "
            f"{b['spyO']['MaxDD']:7.2%}   OOS RULES v2 {b['liveO']['CAGR']:7.2%} / "
            f"{b['liveO']['Sharpe']:.4f} / {b['liveO']['MaxDD']:7.2%}")
        say(f"      pick - anchor: Sharpe {pick.OOS_Sharpe-anchor.OOS_Sharpe:+.4f}, MaxDD "
            f"{(pick.OOS_MaxDD-anchor.OOS_MaxDD)*100:+.2f} pp, CAGR "
            f"{(pick.OOS_CAGR-anchor.OOS_CAGR)*100:+.2f} pp")
        gate(f"G5 [{pan.name}] OOS window starts on/after {OOS_START}",
             str(pan.idx[b["i_oos"]].date()), f">= {OOS_START}",
             pan.idx[b["i_oos"]] >= pd.Timestamp(OOS_START))
    WF = pd.DataFrame(wf_rows)
    gate("G6 IS and OOS windows are disjoint on every panel",
         f"IS<={IS_END}, OOS>={OOS_START}", "disjoint", True)

    # ================================================================ verdict
    say("\n" + "=" * 112)
    say("VERDICT")
    say("=" * 112)
    say(f"  4a: {int(G.keep4a.sum())} of {len(G)} cells.  "
        f"4b (full-sample legs): {int(G.keep4b.sum())} of {len(G)}  "
        f"(SMALL {int(sm.keep4b.sum())} of {len(sm)}).")
    say(f"  4b ALL LEGS after rule 8: {int(WF.KEEP4b_all_legs.sum())} of {len(WF)} panels.")
    say(f"  SMALL DD leg (L_DD) passes in {int(sm.L_DD.sum())} of {len(sm)} cells; "
        f"best SMALL MaxDD over the whole 20-cell grid {sm.MaxDD.max():.2%} against a "
        f"{cap:.2%} cap (gap {(sm.MaxDD.max()-cap)*100:+.2f} pp).")
    b30 = sm[sm.dv == 3e7]
    b0 = sm[sm.dv == 0.0]
    say(f"  The floor's whole effect, $0 -> $30M, averaged over the N ladder: MaxDD "
        f"{(b30.MaxDD.values - b0.MaxDD.values).mean()*100:+.2f} pp, CAGR "
        f"{(b30.CAGR.values - b0.CAGR.values).mean()*100:+.2f} pp, Sharpe "
        f"{(b30.Sharpe.values - b0.Sharpe.values).mean():+.4f}, pool "
        f"{b0.pool_mean.mean():.0f} -> {b30.pool_mean.mean():.0f} names.")
    say(f"  AGAINST THE POOL-SIZE NULL at the same pool share, the DV screen's OWN effect is "
        f"dCAGR {NL.dv_effect_CAGR_pp.iloc[-1]:+.2f} pp, dSharpe "
        f"{NL.dv_effect_Sharpe.iloc[-1]:+.4f}, dMaxDD {NL.dv_effect_MaxDD_pp.iloc[-1]:+.2f} pp "
        f"at $30M (and {NL.dv_effect_MaxDD_pp.iloc[2]:+.2f} pp at $3M).")

    nfail = sum(1 for g in GATES if not g["pass_"])
    say(f"\n  GATES: {len(GATES)-nfail} pass / {nfail} fail")
    for g in GATES:
        if not g["pass_"]:
            say(f"    FAIL {g['gate']}: {g['value']} (target {g['target']})")

    G.to_csv(f"{OUT}.grid.csv", index=False)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    NL.to_csv(f"{OUT}.poolnull.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    dvS.iloc[-1].rename("dv_63d_median_last_row").to_frame().to_csv(f"{OUT}.liquidity.csv")
    say(f"\n  wrote {OUT.name}.{{grid,walkforward,poolnull,gates,liquidity}}.csv in {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

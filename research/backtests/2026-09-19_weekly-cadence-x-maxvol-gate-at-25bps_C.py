#!/usr/bin/env python3
"""Idea 1586 (lane C, 2026-09-19): are the incumbent's WEEKLY CADENCE and its MAXVOL 0.60 GATE
JOINTLY worth anything -- and does the cadence argmax INVERT between the 10 and 25 bps rungs?

WHY THIS IDEA.  The live book carries two dials nobody ever priced together.  RULES v2 clause 5
fixes the rebalance at "the last trading day of each week only"; RULES v2 clause 2 explicitly
DROPS the volatility filter, while the frozen 2026-09-04 KEEP-4b incumbent (composite momentum,
N = 20, H = 126) still carries `vol20 < 0.60` as an inherited eligibility gate straight out of
RULES v1.  Idea 1305 priced the W -> M step ALONE and found it costs U56 -0.1053 of Sharpe at
10 bps while refunding only 6.0 bp/yr of drag.  Idea 1009 reports the cadence argmax INVERTS
between 0 and 10 bps.  Neither result says what happens when the two dials move TOGETHER, and
neither was read at a cost rung above the protocol's 10.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  CADENCE  {D, W, M, Q}                  DIAL 1 -- engine.rebalance_mask schedule.  W is live.
  MAXVOL   {0.45, 0.60, 0.80, none}      DIAL 2 -- a name is eligible only if vol20 < m.
                                         0.60 is the inherited value; `none` is NO gate at all
                                         and reduces the LIVE frame EXACTLY to the live book.

16 cells per (frame, panel).  NOT DIALS, published at every value: FRAME {LIVE, INC}, PANEL
{U56, B136, SMALL} (rule 9), COST {10, 25} bps.  **192 cells, every one published** in the
.grid.csv, with both KEEP paths, the halves, IS and OOS windows, turnover and realised gross.

  FRAME LIVE = the live RULES v2 shape (`baseline.band_state`, 200d +/-3% hysteresis band, hold
               every IN name at gross/N of NAV with N = names priced that day, gated-out weight
               to CASH and never re-spread), gross 0.75, PLUS the MAXVOL gate under test.  The
               cell (W, none) IS the live book, bit-for-bit.
  FRAME INC  = the frozen 2026-09-04 KEEP-4b incumbent (composite momentum over (21,252)/(0,126)/
               (0,63), N = 20, H = 126-day min hold, 200d MA gate, vol20 < m), gross 0.75.  The
               cell (W, 0.60) IS the committed anchor: 15.80% / 1.1537 / -19.13% full,
               17.32% / 1.1857 OOS.

COST IS NOT A DIAL.  Weights are cost-independent, so one run of a cell yields BOTH rungs
exactly: r(c) = r_gross - turnover * c / 1e4 (engine.backtest subtracts the charge from the daily
return and never feeds it back into position drift).  That linearity is GATED against a fresh
25 bps engine run, not assumed.  Every KEEP verdict in this file is judged at the protocol's
binding 10 bps; the 25 bps rung is reported alongside, as the idea asks.

THE THREE QUESTIONS, STATED BEFORE THE RUN:
  Q1 INVERSION.  For each (panel, frame, MAXVOL) group, does argmax-over-cadence of full Sharpe
     MOVE between 10 and 25 bps?  Published as a count over all 24 groups, plus the direction
     (a higher cost rung should push the argmax SLOWER if the mechanism is drag).
  Q2 JOINT VALUE.  A 2x2 factorial reading, not two one-at-a-time ladders: for each panel/frame
     and each rival cadence c, the INTERACTION
         [S(W, 0.60) - S(W, none)] - [S(c, 0.60) - S(c, none)]
     says whether the gate is worth MORE at weekly cadence than elsewhere.  If it is ~0 the two
     inheritances are separable and "jointly" is the wrong word for them.
  Q3 IS EITHER WORTH ANYTHING AT ALL?  Both KEEP paths at every cell, and rule 8.

CHOOSERS (rule 8), each fit on warm-up..2016-12-31 ONLY, then 2017-2026 read EXACTLY ONCE, and
re-fit separately at each cost rung:
  C_SHARPE  argmax IS Sharpe over all 16 cells                      (the record's usual chooser)
  C_MEMO    among cells with IS MaxDD <= 0.60 x SPY_IS MaxDD AND IS CAGR >= 0.70 x SPY_IS CAGR,
            take the LOWEST-TURNOVER cell (the cheapest admissible book); else keep the anchor
            -- the 2026-09-03 RECOMMENDATION memo's DD-aware admission with its own "smallest"
            tie-break carried onto these two dials
  C_ANCHOR  the standing cell, choosing nothing: (W, none) on LIVE, (W, 0.60) on INC

WHAT WOULD MAKE THIS A FINDING.  If the cadence argmax does NOT move between 10 and 25 bps, idea
1009's 0-vs-10 inversion is a ZERO-COST artefact and the record should stop quoting it as a
cost-rung fact.  If the interaction term is ~0 at every panel, the two inheritances are separable
and each can be priced alone forever after.  If some (cadence, MAXVOL) cell clears 4b full AND
OOS where the anchor does not, the inheritance was costing real capital.  All three outcomes are
reported; nothing is tuned until it works.

GATES.  G0 sample >= 10y (rule 1).  G1 fast_run vs `engine.backtest` (returns AND turnover) at
every cadence on every panel.  G2 the DERIVED 25 bps rung vs a fresh engine run at 25 bps.  G3
LIVE (W, none) replays `baseline.compare`'s RULES v2 baseline row.  G4 INC (W, 0.60) replays the
committed 2026-09-04 anchor.  G5 exactly two tuned parameters (16 cells).  G6 no chooser reads a
row on or after 2017-01-01 (asserted by construction AND tested on truncated IS input).  G7 192
of 192 cells published.  G8 no leverage, no shorting: max realised gross <= 1.0.  G9 PUBLISHED,
not asserted: turnover per cell and the drag it implies at each rung.  G10 PUBLISHED: realised
mean gross and mean names held per cell, so a Sharpe difference can be read against the exposure
it was bought with.

PROTOCOL: rule 1 (>=10y); rule 2 (t+1, 10 bps per unit turnover, no leverage/shorting); rule 3
(live RULES v2 baseline AND SPY); rule 4 (both KEEP paths, 2 dials); rule 8 (walk-forward); rule 9
(survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-19_weekly-cadence-x-maxvol-gate-at-25bps_C.py
"""
from __future__ import annotations

import sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE, SLUG = "2026-09-19", "weekly-cadence-x-maxvol-gate-at-25bps"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP = 260
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, GROSS, BAND = 20, 126, 0.75, 0.03
GRID_CAD = ["D", "W", "M", "Q"]
GRID_MV = [0.45, 0.60, 0.80, np.inf]          # np.inf == "none", i.e. no volatility gate
MV_LAB = {0.45: "0.45", 0.60: "0.60", 0.80: "0.80", np.inf: "none"}
COSTS = [10.0, 25.0]
FRAMES = ["LIVE", "INC"]
NULL = {"LIVE": ("W", np.inf), "INC": ("W", 0.60)}
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
ANCHOR_INC = dict(CAGR=0.1580, Sharpe=1.1537, MaxDD=-0.1913, oCAGR=0.1732, oSharpe=1.1857)

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    say(f"    GATE {'PASS' if ok else 'FAIL'}  {name}: {value} (target {target})")
    return bool(ok)


def publish(name, value):
    GATES.append(dict(gate=name, value=str(value), target="published, not asserted", pass_=True))
    say(f"    PUBLISHED  {name}: {value}")


# ---------------------------------------------------------------- frozen selection mechanics
def mech(q):
    """The frozen incumbent's composite: three momentum legs, cross-sectional pct ranks, halved
    below the 200d MA.  Identical in form to baseline.score without the 1/sqrt(vol) scaler."""
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
    def __init__(self, name, px, invest, live_cols):
        self.name, self.px, self.invest, self.live_cols = name, px, invest, live_cols
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.ilive = np.array([cols.index(c) for c in live_cols])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.above, self.vol20 = above, vol20
        # LIVE frame inputs, on the LIVE column set
        self.band = band_state(px[live_cols], BAND).values
        lv = (px[live_cols].pct_change().rolling(20).std() * np.sqrt(252)).values
        self.lvol = np.nan_to_num(lv, nan=1e9)
        self.lpriced = px[live_cols].notna().values
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])

    def reb_rows(self, cadence):
        m = rebalance_mask(self.idx, cadence).shift(1, fill_value=False).values.copy()
        m[0] = True
        return np.flatnonzero(m)


def frame_live(pan, m):
    """Live RULES v2 band shape at GROSS = 1.0 plus the vol20 < m gate, shifted so row t carries
    the close-(t-1) decision -- exactly engine.backtest's `weights.shift(1)` convention.
    m = inf reproduces `baseline.rules_v2_weights` on the LIVE column set, bit-for-bit."""
    T, M = pan.rets.shape
    e = pan.lpriced.astype(float)
    n = e.sum(axis=1)
    ew = np.divide(e, np.where(n == 0, np.nan, n)[:, None])
    ew = np.nan_to_num(ew, nan=0.0)
    w = np.where(pan.band & (pan.lvol < m), ew, 0.0)
    W = np.zeros((T, M))
    W[:, pan.ilive] = w
    return np.vstack([np.zeros((1, M)), W[:-1]])


def frame_inc(pan, reb, m, N=I_N, H=I_H, lag=1):
    """Frozen min-hold momentum selection at GROSS = 1.0, eligibility `above 200d MA and
    vol20 < m`.  Row t already carries the close-(t-1) decision (ts = t - lag)."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    elig = pan.above & (pan.vol20 < m)
    pr = pan.priced[:, pan.iinv]
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
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


def run_cell(pan, frame, reb, g=GROSS):
    """Hold g * frame on the schedule, drift between rebalances, de-gross to 0%-yielding cash.
    Returns GROSS-OF-COST daily returns, the turnover path, max realised gross and mean gross --
    identical semantics to engine.backtest, gated at G1."""
    rets = pan.rets
    T, M = rets.shape
    turn = np.zeros(T)
    out = np.zeros(T)
    gsum = np.zeros(T)
    curw = np.zeros(M)
    wsum_max = 0.0
    ends = np.append(reb[1:], T)
    C, Cp = pan.C, pan.Cp
    for i0, i1 in zip(reb, ends):
        if i1 <= i0:
            continue
        w0 = g * frame[i0]
        s0 = float(w0.sum())
        wsum_max = max(wsum_max, s0)
        turn[i0] = float(np.abs(w0 - curw).sum())
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])          # risky value at START of each day
        V = A.sum(axis=1) + (1.0 - s0)
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        gsum[i0:i1] = A.sum(axis=1) / V
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + (1.0 - s0))
    return out, turn, wsum_max, gsum


# ---------------------------------------------------------------- metrics
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


def bmpack(r):
    h1, h2 = halves(r)
    m = triple(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


def keep_paths(r, bm, live):
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(H1=bool(h1 > bm["H1"]), H2=bool(h2 > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return k4a, bool(all(legs.values())), m, h1, h2, legs


CELLS = [(c, m) for c in GRID_CAD for m in GRID_MV]


def chooser_sharpe(ispk):
    return max(CELLS, key=lambda c: (ispk[c]["Sharpe"], GRID_CAD.index(c[0]), -GRID_MV.index(c[1])))


def chooser_memo(ispk, dd_bar, cagr_bar, anchor):
    ok = [c for c in CELLS if ispk[c]["MaxDD"] >= dd_bar and ispk[c]["CAGR"] >= cagr_bar]
    if not ok:
        return anchor, True
    return min(ok, key=lambda c: (ispk[c]["turn"], GRID_CAD.index(c[0]), GRID_MV.index(c[1]))), False


def main():
    t0 = time.time()
    say("=" * 118)
    say("IDEA 1586 (lane C, 2026-09-19) — are the incumbent's WEEKLY CADENCE and MAXVOL 0.60 GATE")
    say("JOINTLY worth anything, and does the cadence argmax INVERT between 10 and 25 bps?")
    say(f"DIALS: CADENCE {GRID_CAD}  x  MAXVOL {[MV_LAB[m] for m in GRID_MV]}  (16 cells).")
    say(f"NOT DIALS, all published: FRAME {FRAMES} x PANEL [U56, B136, SMALL] x COST {COSTS} bps.")
    say(f"NULL CELLS: LIVE (W, none) = the live RULES v2 book; INC (W, 0.60) = the frozen "
        f"2026-09-04 anchor.  Gross {GROSS} on both frames, t+1 execution.")
    say("=" * 118)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)

    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    say(f"  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0; {len(inv)} of {len(pxS.columns)-1} priced names survive.")

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"], list(pxU.columns)),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"], list(pxB.columns)),
              Panel("SMALL", pxS, inv, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, SMALL {len(inv)}.")
    say("  COLUMN SETS, stated not glossed: on U56 and B136 the LIVE frame trades the SAME column "
        "set as the committed `baseline.rules_v2_weights` (SPY included, because it is a universe "
        "constituent there and the live book holds it).  On SMALL, SPY is a joined BENCHMARK, not "
        "a constituent, so the LIVE frame there trades the filtered small-cap list only.")
    say("  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010, so every absolute level below is an UPPER BOUND.  "
        "What survives the bias is the CONTRAST between cadences and MAXVOL rungs on the same "
        "names, the same days and the same frame.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y)")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)
    gate("G5 exactly two tuned parameters", f"{len(GRID_CAD)} cadences x {len(GRID_MV)} maxvol "
         f"= {len(CELLS)} cells", "2 dials", len(CELLS) == 16)

    # ------------------------------------------------ G1 / G2: fast_run vs the engine
    say("\n  [G1/G2] fast_run vs engine.backtest (returns AND turnover), every cadence, every panel")
    d1r = d1t = d2 = 0.0
    for pan in panels:
        for cad in GRID_CAD:
            reb = pan.reb_rows(cad)
            fl = frame_live(pan, np.inf)
            rg, tu, _, _ = run_cell(pan, fl, reb)
            eng = backtest(pan.px, rules_v2_weights(pan.px[pan.live_cols], gross=GROSS)
                           .reindex(pan.idx).fillna(0.0).reindex(columns=pan.px.columns).fillna(0.0),
                           cost_bps=10.0, freq=cad)
            d1r = max(d1r, float(np.max(np.abs((rg - tu * 10.0 / 1e4) - eng["returns"].values))))
            d1t = max(d1t, float(np.max(np.abs(tu - eng["turnover"].values))))
            eng25 = backtest(pan.px, rules_v2_weights(pan.px[pan.live_cols], gross=GROSS)
                             .reindex(pan.idx).fillna(0.0).reindex(columns=pan.px.columns).fillna(0.0),
                             cost_bps=25.0, freq=cad)
            d2 = max(d2, float(np.max(np.abs((rg - tu * 25.0 / 1e4) - eng25["returns"].values))))
    gate("G1 fast_run vs engine.backtest, RETURNS (max |dev| over 12 panel x cadence runs)",
         f"{d1r:.3e}", "< 1e-12", d1r < 1e-12)
    gate("G1b fast_run vs engine.backtest, TURNOVER (max |dev|)", f"{d1t:.3e}", "< 1e-12", d1t < 1e-12)
    gate("G2 DERIVED 25 bps rung vs a fresh 25 bps engine run (max |dev|)",
         f"{d2:.3e}", "< 1e-12", d2 < 1e-12)

    grid, wsum_global = [], 0.0
    RET, TURN, ISPK, BARS = {}, {}, {}, {}
    g3 = {}

    for pan in panels:
        T = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        spy = bmpack(pan.spy[WARMUP:]); spyO = bmpack(pan.spy[i_oos:]); spyI = bmpack(pan.spy[WARMUP:i_oos])
        bars = dict(spy=spy, spyO=spyO, spyI=spyI, i_oos=i_oos, live={}, liveO={})
        for c in COSTS:
            lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=c, freq="W")["returns"].values
            bars["live"][c], bars["liveO"][c] = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])
            if c == 10.0:
                g3[pan.name] = bars["live"][c]
        BARS[pan.name] = bars
        say(f"\n  [{pan.name}]  SPY FULL {spy['CAGR']:.2%} / {spy['Sharpe']:.4f} / {spy['MaxDD']:.2%} "
            f"H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f}  |  4b bars: DD cap {DD_CAP*spy['MaxDD']:.2%}, "
            f"CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           SPY OOS  {spyO['CAGR']:.2%} / {spyO['Sharpe']:.4f} / {spyO['MaxDD']:.2%}  |  "
            f"OOS bars: DD cap {DD_CAP*spyO['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spyO['CAGR']:.2%}")
        for c in COSTS:
            L = bars["live"][c]
            say(f"           RULES v2 live @{c:.0f}bps  {L['CAGR']:.2%} / {L['Sharpe']:.4f} / "
                f"{L['MaxDD']:.2%}  H1/H2 {L['H1']:.3f}/{L['H2']:.3f}  (OOS {bars['liveO'][c]['Sharpe']:.4f})")

        for fr in FRAMES:
            for cad in GRID_CAD:
                reb = pan.reb_rows(cad)
                for m in GRID_MV:
                    fm = frame_live(pan, m) if fr == "LIVE" else frame_inc(pan, reb, m)
                    rg, tu, ws, gs = run_cell(pan, fm, reb)
                    wsum_global = max(wsum_global, ws)
                    yrs = (T - WARMUP) / 252.0
                    nheld = float(np.mean((fm[WARMUP:] > 0).sum(axis=1)))
                    for c in COSTS:
                        r = rg - tu * c / 1e4
                        RET[(pan.name, fr, cad, m, c)] = r
                        TURN[(pan.name, fr, cad, m, c)] = float(tu[WARMUP:].sum() / yrs)
                        k4a, k4b, mt, h1, h2, legs = keep_paths(r[WARMUP:], spy, bars["live"][c])
                        k4aO, k4bO, mo, _, _, legsO = keep_paths(r[i_oos:], spyO, bars["liveO"][c])
                        ISPK[(pan.name, fr, c)] = ISPK.get((pan.name, fr, c), {})
                        ISPK[(pan.name, fr, c)][(cad, m)] = dict(
                            Sharpe=sharpe(r[WARMUP:i_oos]), CAGR=cagr(r[WARMUP:i_oos]),
                            MaxDD=mdd(r[WARMUP:i_oos]), turn=float(tu[WARMUP:i_oos].sum()))
                        grid.append(dict(panel=pan.name, frame=fr, cadence=cad, maxvol=MV_LAB[m],
                                         cost_bps=c, CAGR=mt["CAGR"], Sharpe=mt["Sharpe"],
                                         MaxDD=mt["MaxDD"], H1=h1, H2=h2,
                                         oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                                         isSharpe=ISPK[(pan.name, fr, c)][(cad, m)]["Sharpe"],
                                         isCAGR=ISPK[(pan.name, fr, c)][(cad, m)]["CAGR"],
                                         isMaxDD=ISPK[(pan.name, fr, c)][(cad, m)]["MaxDD"],
                                         turnover_yr=float(tu[WARMUP:].sum() / yrs),
                                         drag_bpyr=float(tu[WARMUP:].sum() / yrs) * c,
                                         mean_gross=float(np.mean(gs[WARMUP:])), mean_names=nheld,
                                         keep4a=k4a, keep4b=k4b, keep4a_oos=k4aO, keep4b_oos=k4bO,
                                         leg_H1=legs["H1"], leg_H2=legs["H2"], leg_DD=legs["DD"],
                                         leg_CAGR=legs["CAGR"], oleg_H1=legsO["H1"],
                                         oleg_H2=legsO["H2"], oleg_DD=legsO["DD"],
                                         oleg_CAGR=legsO["CAGR"],
                                         is_null=bool((cad, m) == NULL[fr])))
        say(f"    [{pan.name}] 32 cells x 2 cost rungs done  ({time.time()-t0:.0f}s elapsed)")

    G = pd.DataFrame(grid)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    gate("G7 every cell published", f"{len(G)} rows in {Path(OUT).name}.grid.csv",
         "192 = 3 panels x 2 frames x 4 cadences x 4 maxvol x 2 rungs", len(G) == 192)
    gate("G8 no leverage, no shorting (max realised target gross)", f"{wsum_global:.4f}",
         f"<= {GROSS:.4f}", wsum_global <= GROSS + 1e-12)

    # ------------------------------------------------ G3 / G4 replays
    lv = G[(G.panel == "U56") & (G.frame == "LIVE") & (G.cadence == "W") & (G.maxvol == "none")
           & (G.cost_bps == 10.0)].iloc[0]
    b = g3["U56"]
    d3 = max(abs(lv["CAGR"] - b["CAGR"]), abs(lv["Sharpe"] - b["Sharpe"]),
             abs(lv["MaxDD"] - b["MaxDD"]), abs(lv["H1"] - b["H1"]), abs(lv["H2"] - b["H2"]))
    gate("G3 LIVE (W, none) on U56 replays baseline.compare's RULES v2 row", f"{d3:.3e}",
         "< 1e-12 (it IS the same book)", d3 < 1e-12)
    ic = G[(G.panel == "U56") & (G.frame == "INC") & (G.cadence == "W") & (G.maxvol == "0.60")
           & (G.cost_bps == 10.0)].iloc[0]
    d4 = max(abs(ic["CAGR"] - ANCHOR_INC["CAGR"]), abs(ic["Sharpe"] - ANCHOR_INC["Sharpe"]),
             abs(ic["MaxDD"] - ANCHOR_INC["MaxDD"]), abs(ic["oCAGR"] - ANCHOR_INC["oCAGR"]),
             abs(ic["oSharpe"] - ANCHOR_INC["oSharpe"]))
    gate("G4 INC (W, 0.60) on U56 replays the committed 2026-09-04 anchor", f"{d4:.3e}",
         "< 5e-4 (committed to 4 dp)", d4 < 5e-4)
    say(f"      anchor replay: {ic['CAGR']:.2%} / {ic['Sharpe']:.4f} / {ic['MaxDD']:.2%}  "
        f"OOS {ic['oCAGR']:.2%} / {ic['oSharpe']:.4f}   vs committed 15.80% / 1.1537 / -19.13%, "
        f"OOS 17.32% / 1.1857")

    # ------------------------------------------------ Q1: does the cadence argmax invert?
    say("\n" + "=" * 118)
    say("Q1 — DOES THE CADENCE ARGMAX INVERT BETWEEN 10 AND 25 bps?  (24 groups = 3 panels x 2 "
        "frames x 4 MAXVOL rungs)")
    say("=" * 118)
    rows = []
    n_inv = n_inv_o = 0
    for pan in panels:
        for fr in FRAMES:
            for m in GRID_MV:
                sub = G[(G.panel == pan.name) & (G.frame == fr) & (G.maxvol == MV_LAB[m])]
                a10 = sub[sub.cost_bps == 10.0].sort_values("Sharpe", ascending=False).iloc[0]
                a25 = sub[sub.cost_bps == 25.0].sort_values("Sharpe", ascending=False).iloc[0]
                o10 = sub[sub.cost_bps == 10.0].sort_values("oSharpe", ascending=False).iloc[0]
                o25 = sub[sub.cost_bps == 25.0].sort_values("oSharpe", ascending=False).iloc[0]
                inv = a10.cadence != a25.cadence
                invo = o10.cadence != o25.cadence
                n_inv += int(inv); n_inv_o += int(invo)
                rows.append(dict(panel=pan.name, frame=fr, maxvol=MV_LAB[m],
                                 argmax_full_10=a10.cadence, argmax_full_25=a25.cadence,
                                 inverts_full=bool(inv), argmax_oos_10=o10.cadence,
                                 argmax_oos_25=o25.cadence, inverts_oos=bool(invo),
                                 S10=a10.Sharpe, S25=a25.Sharpe,
                                 gap10=float(a10.Sharpe - sub[(sub.cost_bps == 10.0) &
                                             (sub.cadence == a25.cadence)].iloc[0].Sharpe)))
                say(f"    {pan.name:<6} {fr:<5} MAXVOL {MV_LAB[m]:<5}  argmax FULL  10bps {a10.cadence} "
                    f"({a10.Sharpe:.4f})  25bps {a25.cadence} ({a25.Sharpe:.4f})  "
                    f"{'INVERTS' if inv else 'stable ':<8} | argmax OOS 10bps {o10.cadence} 25bps "
                    f"{o25.cadence} {'INVERTS' if invo else 'stable'}")
    INV = pd.DataFrame(rows)
    INV.to_csv(f"{OUT}.inversion.csv", index=False)
    say(f"\n  ANSWER Q1: the full-sample cadence argmax moves between the 10 and 25 bps rungs in "
        f"{n_inv} of {len(INV)} groups ({n_inv/len(INV):.4f}); on OOS Sharpe, {n_inv_o} of "
        f"{len(INV)} ({n_inv_o/len(INV):.4f}).")
    cnt10 = INV.argmax_full_10.value_counts().to_dict()
    cnt25 = INV.argmax_full_25.value_counts().to_dict()
    say(f"  argmax cadence distribution, FULL:  10 bps {cnt10}   25 bps {cnt25}")
    publish("Q1 argmax distribution", f"10bps {cnt10} / 25bps {cnt25}")

    # ------------------------------------------------ Q2: is the pair JOINT?
    say("\n" + "=" * 118)
    say("Q2 — IS THE (WEEKLY x MAXVOL 0.60) PAIR JOINT?  2x2 interaction on full Sharpe at 10 bps:")
    say("      I(c) = [S(W,0.60) - S(W,none)] - [S(c,0.60) - S(c,none)].  I ~ 0 => SEPARABLE.")
    say("=" * 118)
    jr = []
    for pan in panels:
        for fr in FRAMES:
            for c in COSTS:
                q = lambda cd, mm: float(G[(G.panel == pan.name) & (G.frame == fr) &
                                           (G.cadence == cd) & (G.maxvol == mm) &
                                           (G.cost_bps == c)].iloc[0].Sharpe)
                mainW = q("W", "0.60") - q("W", "none")
                for cd in [x for x in GRID_CAD if x != "W"]:
                    other = q(cd, "0.60") - q(cd, "none")
                    jr.append(dict(panel=pan.name, frame=fr, cost_bps=c, rival=cd,
                                   gate_at_W=mainW, gate_at_rival=other,
                                   interaction=mainW - other))
                if c == 10.0:
                    say(f"    {pan.name:<6} {fr:<5} @10bps  gate worth at W {mainW:+.4f}  |  " +
                        "  ".join(f"at {cd} {q(cd,'0.60')-q(cd,'none'):+.4f} (I {mainW-(q(cd,'0.60')-q(cd,'none')):+.4f})"
                                  for cd in GRID_CAD if cd != "W"))
    J = pd.DataFrame(jr)
    J.to_csv(f"{OUT}.joint.csv", index=False)
    say(f"\n  ANSWER Q2: |interaction| over {len(J)} (panel, frame, rung, rival) readings — "
        f"mean {J.interaction.abs().mean():.4f}, median {J.interaction.abs().median():.4f}, "
        f"max {J.interaction.abs().max():.4f}.")
    say(f"  For scale, the MAIN effect of the gate at weekly cadence has |mean| "
        f"{J.gate_at_W.abs().mean():.4f} and the record's own W->M cadence step (idea 1305) is "
        f"0.1053 of Sharpe.")
    say(f"  Sign agreement: the gate helps at W in {int((J.gate_at_W>0).sum())} of {len(J)} "
        f"readings and at the rival cadence in {int((J.gate_at_rival>0).sum())} of {len(J)}.")

    # ------------------------------------------------ Q3: both KEEP paths
    say("\n" + "=" * 118)
    say("Q3 — BOTH KEEP PATHS AT THE PROTOCOL'S BINDING 10 bps (96 cells; the 25 bps rung is "
        "reported in the grid but never used for a verdict)")
    say("=" * 118)
    G10 = G[G.cost_bps == 10.0]
    say(f"    4a (beat the live book in BOTH halves, MaxDD no worse): "
        f"{int(G10.keep4a.sum())} of {len(G10)} FULL, {int(G10.keep4a_oos.sum())} OOS")
    say(f"    4b (beat SPY in BOTH halves AND OOS, MaxDD <= 60% SPY, CAGR >= 70% SPY): "
        f"{int(G10.keep4b.sum())} of {len(G10)} FULL, {int(G10.keep4b_oos.sum())} OOS, "
        f"{int((G10.keep4b & G10.keep4b_oos).sum())} BOTH")
    both = G10[G10.keep4b & G10.keep4b_oos].sort_values("Sharpe", ascending=False)
    if len(both):
        say("    4b passers (FULL and OOS), best full Sharpe first:")
        for _, r in both.iterrows():
            say(f"      {r.panel:<6} {r.frame:<5} ({r.cadence}, MAXVOL {r.maxvol:<5}) "
                f"{r.CAGR:.2%} / {r.Sharpe:.4f} / {r.MaxDD:.2%}  H1/H2 {r.H1:.3f}/{r.H2:.3f}  "
                f"OOS {r.oCAGR:.2%} / {r.oSharpe:.4f} / {r.oMaxDD:.2%}  turn {r.turnover_yr:.2f}x/yr"
                f"{'   <== THE STANDING NULL' if r.is_null else ''}")
    say(f"    4a and 4b disjoint? overlap = {int((G10.keep4a & G10.keep4b).sum())} cells")
    for fr in FRAMES:
        s = G10[G10.frame == fr]
        say(f"      by frame {fr}: 4a {int(s.keep4a.sum())}/{len(s)}, 4b {int(s.keep4b.sum())}/{len(s)}")

    # ------------------------------------------------ Q1b: the BREAK-EVEN cost rung
    say("\n" + "=" * 118)
    say("Q1b — WHERE EXACTLY DOES THE WEEKLY CADENCE STOP WINNING?  Because r(c) = r_gross - "
        "turnover * c / 1e4 is EXACT (gated at G2),")
    say("      the whole cost axis is readable off the two cached rungs with no extra backtest.  "
        "c* = the cost in bps at which a")
    say("      SLOWER rival overtakes W on full Sharpe.  c* < 10 means the live cadence is "
        "ALREADY behind; c* > 200 means never.")
    say("=" * 118)

    def srp(rg, tu, c):
        return sharpe(rg - tu * c / 1e4)

    def breakeven(rgA, tuA, rgB, tuB, lo=0.0, hi=200.0):
        f = lambda c: srp(rgB, tuB, c) - srp(rgA, tuA, c)
        if f(lo) > 0:
            return lo                      # the rival is already ahead at zero cost
        if f(hi) <= 0:
            return None                    # never, inside a cost range anyone would pay
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if f(mid) > 0:
                hi = mid
            else:
                lo = mid
        return 0.5 * (lo + hi)

    be = []
    for pan in panels:
        i_oos = BARS[pan.name]["i_oos"]
        for fr in FRAMES:
            for m in GRID_MV:
                def series(cd):
                    r10 = RET[(pan.name, fr, cd, m, 10.0)][WARMUP:]
                    r25 = RET[(pan.name, fr, cd, m, 25.0)][WARMUP:]
                    tu = (r10 - r25) / (15.0 / 1e4)
                    return r10 + tu * 10.0 / 1e4, tu
                rgW, tuW = series("W")
                out = []
                for cd in [x for x in GRID_CAD if x != "W"]:
                    rgB, tuB = series(cd)
                    c = breakeven(rgW, tuW, rgB, tuB)
                    be.append(dict(panel=pan.name, frame=fr, maxvol=MV_LAB[m], rival=cd,
                                   cstar_bps=(np.nan if c is None else c),
                                   ahead_at_zero=bool(c == 0.0),
                                   never_within_200=bool(c is None),
                                   dS_at_10=srp(rgB, tuB, 10.0) - srp(rgW, tuW, 10.0),
                                   dS_at_25=srp(rgB, tuB, 25.0) - srp(rgW, tuW, 25.0),
                                   turn_W=float(tuW.sum() / (len(tuW) / 252.0)),
                                   turn_rival=float(tuB.sum() / (len(tuB) / 252.0))))
                    out.append(f"{cd} c*=" + ("never" if c is None else f"{c:.1f}bps"))
                say(f"    {pan.name:<6} {fr:<5} MAXVOL {MV_LAB[m]:<5}  " + "   ".join(out))
    BE = pd.DataFrame(be)
    BE.to_csv(f"{OUT}.breakeven.csv", index=False)
    fin = BE.dropna(subset=["cstar_bps"])
    say(f"\n  ANSWER Q1b: of {len(BE)} (panel, frame, MAXVOL, rival) pairs, {len(fin)} have a "
        f"break-even inside 0-200 bps and {int(BE.never_within_200.sum())} never overtake W.")
    say(f"  Of the {len(fin)} that do: {int((fin.cstar_bps <= 10).sum())} are ALREADY ahead at the "
        f"protocol's 10 bps, {int(((fin.cstar_bps > 10) & (fin.cstar_bps <= 25)).sum())} cross "
        f"between 10 and 25 bps, {int((fin.cstar_bps > 25).sum())} cross above 25.")
    say(f"  Median c* among the finite ones: {fin.cstar_bps.median():.1f} bps "
        f"(IQR {fin.cstar_bps.quantile(.25):.1f}-{fin.cstar_bps.quantile(.75):.1f}).")
    hl = BE[(BE.panel == "U56") & (BE.frame == "INC") & (BE.maxvol == "0.60") & (BE.rival == "Q")]
    if len(hl):
        h = hl.iloc[0]
        say(f"  THE HEADLINE PAIR — the frozen anchor's own cell, U56/INC/MAXVOL 0.60, W vs Q: "
            f"c* = {h.cstar_bps:.1f} bps.  Below it the anchor's weekly cadence wins; above it the "
            f"quarterly twin does, at {h.turn_rival:.2f}x/yr against {h.turn_W:.2f}x/yr of turnover.")

    # ------------------------------------------------ rule 8 walk-forward
    say("\n" + "=" * 118)
    say("RULE 8 WALK-FORWARD — dials chosen on warm-up..2016-12-31 ONLY, 2017-2026 READ ONCE")
    say("=" * 118)
    wf = []
    for pan in panels:
        bars = BARS[pan.name]
        i_oos = bars["i_oos"]
        for fr in FRAMES:
            anchor = NULL[fr]
            for c in COSTS:
                ispk = ISPK[(pan.name, fr, c)]
                dd_bar = DD_CAP * bars["spyI"]["MaxDD"]
                cagr_bar = CAGR_FLOOR * bars["spyI"]["CAGR"]
                picks = {"C_SHARPE": (chooser_sharpe(ispk), False),
                         "C_MEMO": chooser_memo(ispk, dd_bar, cagr_bar, anchor),
                         "C_ANCHOR": (anchor, False)}
                for nm, (pk, fell) in picks.items():
                    r = RET[(pan.name, fr, pk[0], pk[1], c)]
                    k4aO, k4bO, mo, _, _, legsO = keep_paths(r[i_oos:], bars["spyO"], bars["liveO"][c])
                    ra = RET[(pan.name, fr, anchor[0], anchor[1], c)]
                    wf.append(dict(panel=pan.name, frame=fr, cost_bps=c, chooser=nm,
                                   pick_cadence=pk[0], pick_maxvol=MV_LAB[pk[1]], fellback=fell,
                                   oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                                   d_vs_anchor=mo["Sharpe"] - sharpe(ra[i_oos:]),
                                   d_vs_live=mo["Sharpe"] - bars["liveO"][c]["Sharpe"],
                                   d_vs_spy=mo["Sharpe"] - bars["spyO"]["Sharpe"],
                                   keep4a_oos=k4aO, keep4b_oos=k4bO))
                    if c == 10.0:
                        say(f"    {pan.name:<6} {fr:<5} @{c:.0f}bps {nm:<9} picks ({pk[0]}, "
                            f"MAXVOL {MV_LAB[pk[1]]:<5}){' [FELL BACK]' if fell else '':<12} OOS "
                            f"{mo['CAGR']:.2%} / {mo['Sharpe']:.4f} / {mo['MaxDD']:.2%}   "
                            f"dS vs anchor {mo['Sharpe']-sharpe(ra[i_oos:]):+.4f}  vs live "
                            f"{mo['Sharpe']-bars['liveO'][c]['Sharpe']:+.4f}  vs SPY "
                            f"{mo['Sharpe']-bars['spyO']['Sharpe']:+.4f}  4b_oos {k4bO}")
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    for nm in ["C_SHARPE", "C_MEMO", "C_ANCHOR"]:
        s = W[W.chooser == nm]
        say(f"    POOLED {nm:<9}: mean OOS Sharpe {s.oSharpe.mean():.4f}, beats the anchor in "
            f"{int((s.d_vs_anchor>1e-12).sum())} of {len(s)}, beats live RULES v2 in "
            f"{int((s.d_vs_live>0).sum())}, beats SPY in {int((s.d_vs_spy>0).sum())}, "
            f"4b_oos {int(s.keep4b_oos.sum())}")

    # G6: the chooser cannot see OOS rows -- tested, not asserted
    say("\n  [G6] re-fitting every chooser on IS returns TRUNCATED at 2016-12-31 must give the "
        "identical pick (the IS statistics are computed on [WARMUP:i_oos] by construction).")
    same = True
    for pan in panels:
        i_oos = BARS[pan.name]["i_oos"]
        for fr in FRAMES:
            for c in COSTS:
                trunc = {}
                for cell in CELLS:
                    r = RET[(pan.name, fr, cell[0], cell[1], c)][:i_oos]
                    trunc[cell] = dict(Sharpe=sharpe(r[WARMUP:]), CAGR=cagr(r[WARMUP:]),
                                       MaxDD=mdd(r[WARMUP:]),
                                       turn=ISPK[(pan.name, fr, c)][cell]["turn"])
                same &= chooser_sharpe(trunc) == chooser_sharpe(ISPK[(pan.name, fr, c)])
    gate("G6 choosers read no row on or after 2017-01-01 (truncated re-fit gives identical picks)",
         same, "True", same)
    say(f"  OOS start row per panel: " + ", ".join(
        f"{p.name} {p.idx[BARS[p.name]['i_oos']].date()}" for p in panels))

    # G9 / G10 published
    for pan in panels:
        s = G[(G.panel == pan.name) & (G.cost_bps == 10.0) & (G.frame == "INC")]
        publish(f"G9 turnover x/yr by cadence {pan.name} INC",
                ", ".join(f"{cd} {s[s.cadence==cd].turnover_yr.mean():.2f}" for cd in GRID_CAD))
        s2 = G[(G.panel == pan.name) & (G.cost_bps == 10.0) & (G.frame == "LIVE")]
        publish(f"G10 mean realised gross / mean names, LIVE {pan.name} by MAXVOL",
                ", ".join(f"{MV_LAB[m]}: {s2[s2.maxvol==MV_LAB[m]].mean_gross.mean():.4f} / "
                          f"{s2[s2.maxvol==MV_LAB[m]].mean_names.mean():.1f}" for m in GRID_MV))

    GT = pd.DataFrame(GATES)
    GT.to_csv(f"{OUT}.gates.csv", index=False)
    npass = int(GT.pass_.sum()); ntot = len(GT)
    say(f"\n  GATES: {npass} of {ntot} pass/published.")
    say(f"  Wrote {Path(OUT).name}.grid.csv ({len(G)}), .inversion.csv ({len(INV)}), "
        f".joint.csv ({len(J)}), .breakeven.csv ({len(BE)}), .walkforward.csv ({len(W)}), "
        f".gates.csv ({ntot}), .log.txt")
    say(f"  Elapsed {time.time()-t0:.0f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

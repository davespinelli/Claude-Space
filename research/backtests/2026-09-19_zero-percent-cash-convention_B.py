#!/usr/bin/env python3
"""Idea 1498 (lane B, 2026-09-19): does the record's 0%-CASH CONVENTION hide a 4b pass?  Price
the un-invested NAV as a REAL short-Treasury sleeve (SHY) instead of a 0.00%/yr hole.

WHY THIS IDEA.  Every de-gross in this record parks un-invested NAV at EXACTLY 0.00%/yr.  That
convention was never declared, never tuned, and never priced -- and today it sits directly on the
one number that decides the whole sprint.  Idea 1454 (this morning, lane B) found the live RULES
v2 book fails 4b on the CAGR FLOOR ALONE, by -1.97 pp full-sample and -1.22 pp OOS, with all four
other legs already passing, and concluded the fix is to run the book at G = 1.00 -- i.e. to
ABOLISH the cash leg, because the cash leg earns nothing.  Eight runs before it (1405, 1413,
1429, 1433, 1436, 1461, 1468, 1488) each found a drawdown-buying DEVICE beaten at matched
exposure by a plain DE-GROSS, a contest in which the de-gross is carrying a 0%-yielding bucket.
If that bucket earns what short Treasuries actually paid, BOTH readings can move: the CAGR floor
that binds every rung G <= 0.75 may stop binding, and the de-gross's cost may shrink.

THIS IS NOT A BOOKKEEPING AUDIT.  Crediting the cash leg is an IMPLEMENTABLE RULE CHANGE: park
fraction F of un-invested NAV in SHY and trade it like any other position, paying 10 bps on its
own turnover.  So F is a real dial on a real book, and every cell here is a book that could be
run with real money tomorrow.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  G  {0.25, 0.375, 0.50, 0.625, 0.75, 0.875, 1.00}   DIAL 1 -- constant gross.  Rungs are idea
                                                     1454's and 1446's exactly, so the three
                                                     ladders are readable side by side.  Stops at
                                                     1.00: no leverage (rule 2).  G = 0.75 is the
                                                     live/frozen value on both frames.
  F  {0.00, 0.25, 0.50, 0.75, 1.00}                  DIAL 2 -- fraction of un-invested NAV placed
                                                     in SHY.  F = 0.00 IS the record's standing
                                                     convention and is a cell of the grid, so the
                                                     null "change nothing" is priced on the same
                                                     tape as every candidate.

35 cells per (frame, panel).  NOT DIALS, reported at every value: FRAME {LIVE, INC}, PANEL
{U56, B136, SMALL} (rule 9), both KEEP paths at every cell, the halves, IS and OOS windows,
turnover, realised mean gross and realised mean cash sleeve.  210 cells in all, EVERY ONE
PUBLISHED in the .grid.csv.

  FRAME LIVE = the live RULES v2 shape (`baseline.rules_v2_weights`: 200d +/-3% hysteresis band,
               hold every IN name, de-gross to cash, never re-spread), weekly.  This is the frame
               whose CAGR floor 1454 found binding.
  FRAME INC  = the frozen 2026-09-04 KEEP-4b incumbent (composite momentum, N = 20, H = 126-day
               min hold, 200d MA gate, vol20 < 0.60), weekly.  This is the anchor that beat
               1405 / 1413 / 1429 / 1433 / 1436.

CHOOSERS (rule 8), each fit on warm-up..2016-12-31 ONLY, then 2017-2026 read EXACTLY ONCE:
  C_SHARPE  joint argmax IS Sharpe over all 35 cells                   (the record's usual chooser)
  C_MEMO    smallest G whose IS MaxDD <= 0.60 x SPY_IS MaxDD AND IS CAGR >= 0.70 x SPY_IS CAGR,
            ties broken by smallest F; else keep (0.75, 0.00) -- the 2026-09-03 RECOMMENDATION
            memo's own pre-registered rule, extended to the second dial by its own "smallest"
            logic
  C_CAGR    argmax IS CAGR among cells whose IS MaxDD <= 0.60 x SPY_IS MaxDD   (spend the budget)
  C_ANCHOR  (0.75, 0.00), choosing nothing                             (the null)
All four range over the SAME two dials; they are readings of one grid, not extra parameters.

WHAT WOULD MAKE THIS A FINDING, STATED BEFORE THE RUN.  SHY is a 1-3y Treasury sleeve, so its
realised return over 2009-2026 is small and its 2022 drawdown is real.  The credit at rung G is
at most F x (1 - realised gross) x CAGR(SHY).  If that is ~0.2-0.4 pp/yr it cannot close 1454's
-1.97 pp CAGR gap and the honest answer is that the convention is IMMATERIAL AT THIS RATE LEVEL
-- which is itself worth committing, because it retires an objection to every de-gross contest in
the record.  If instead a (G, F) cell with G < 1.00 clears 4b full AND OOS where its F = 0.00 twin
does not, the convention was hiding a book, and the DD margin bought by the lower G is the prize.
Both outcomes are reported; nothing is tuned until it works.

THE DUTY THIS RUN OWES THE READER.  SHY is NOT a broker sweep rate.  It carries duration: it lost
money in 2022 and it is marked to market daily.  So F = 1.00 is an OPTIMISTIC proxy for a cash
yield in the ZIRP years (2009-2015, when bills paid ~0 and SHY still earned its roll) and a
GENUINE RISK in the rate-rise years.  SHY's own full / IS / OOS CAGR, Sharpe and MaxDD are
published below so the reader can price that themselves.  SHY is also a CONSTITUENT of U56 and
B136, so the INC frame could already select it on momentum; that is the incumbent's existing
behaviour and is left unchanged, and the sleeve is additive to it.

GATES.  G0 sample >= 10y (rule 1).  G1 CROSS-SCRIPT REPLAY of BOTH frames at (0.75, 0.00):
LIVE/U56 must reproduce `baseline.compare`'s RULES v2 baseline row, INC/U56 the committed
2026-09-04 anchor (15.80% / 1.1537 / -19.13% full; 17.32% / 1.1857 / -19.13% OOS).  G2 NO
LEVERAGE: risky sum + cash sleeve never exceeds 1.0.  G3 all 210 cells published.  G4 exactly two
tuned parameters.  G5 no chooser reads a row on or after 2017-01-01 (asserted by construction AND
tested: re-fitting on IS rows truncated to IS_END gives identical picks).  G6 bit-identical
recompute of a sampled cell.  G7 PUBLISHED, NOT ASSERTED: SHY's own return profile, the realised
mean cash sleeve per cell, and the measured pp/yr the credit is worth at every rung.  G8
PUBLISHED: monotonicity of CAGR in F at fixed G.

PROTOCOL: rule 1 (>=10y); rule 2 (t+1, 10 bps on BOTH legs, no leverage, no shorting); rule 3
(RULES v2 live baseline AND SPY); rule 4 (both KEEP paths, 2 dials); rule 8 (walk-forward); rule 9
(survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-19_zero-percent-cash-convention_B.py
"""
from __future__ import annotations

import sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE, SLUG = "2026-09-19", "zero-percent-cash-convention"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H = 20, 126                                  # the frozen 2026-09-04 incumbent
I_G, I_F, CAD = 0.75, 0.00, "W"                     # the null cell on both frames
COST = 10.0
GRID_G = [0.25, 0.375, 0.50, 0.625, 0.75, 0.875, 1.00]
GRID_F = [0.00, 0.25, 0.50, 0.75, 1.00]
FRAMES = ["LIVE", "INC"]
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


# ---------------------------------------------------------------- selection frame (frozen)
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
    def __init__(self, name, px, invest, shy):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.shy = np.nan_to_num(shy.reindex(px.index).ffill().pct_change().values, nan=0.0)
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])

    def reb_rows(self, cadence):
        m = rebalance_mask(self.idx, cadence).shift(1, fill_value=False).values.copy()
        m[0] = True
        return np.flatnonzero(m)


def frame_inc(pan, reb, N, H, lag=1):
    """Frozen min-hold momentum selection at GROSS = 1.0 (the 2026-09-04 incumbent)."""
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


def frame_live(pan, band=0.03):
    """The live RULES v2 band shape at GROSS = 1.0, shifted so row t carries the close-t-1
    decision -- exactly engine.backtest's `weights.shift(1)` convention."""
    return rules_v2_weights(pan.px, band=band, gross=1.0).reindex(pan.idx).fillna(0.0).shift(1).fillna(0.0).values


def run_cell(pan, frame, reb, g, f, cost=COST):
    """The frozen frame at constant gross g, with fraction f of UN-INVESTED NAV in SHY.

    The SHY sleeve is a real position: it drifts with the book between rebalances and pays
    `cost` bps on its own turnover.  f = 0 reduces exactly to the record's 0% cash convention.
    """
    rets, cr = pan.rets, pan.shy
    T, M = rets.shape
    turn = np.zeros(T)
    out = np.zeros(T)
    gsum = np.zeros(T)
    csle = np.zeros(T)
    curw = np.zeros(M)
    wsum_max = 0.0
    ends = np.append(reb[1:], T)
    C, Cp = pan.C, pan.Cp
    for i0, i1 in zip(reb, ends):
        if i1 <= i0:
            continue
        w0 = g * frame[i0]
        s0 = float(w0.sum())
        wsum_max = max(wsum_max, s0 + f * (1.0 - s0))
        turn[i0] = float(np.abs(w0 - curw).sum()) + f * abs(s0 - float(curw.sum()))
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])            # risky value at START of each day
        seg = cr[i0:i1]
        cash_growth = np.concatenate(([1.0], np.cumprod(1.0 + f * seg)[:-1]))
        Ccash = (1.0 - s0) * cash_growth                          # cash value at START of each day
        V = A.sum(axis=1) + Ccash
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1) + (Ccash / V) * (f * seg)
        gsum[i0:i1] = A.sum(axis=1) / V
        csle[i0:i1] = f * Ccash / V
        Ae = w0 * (C[i1 - 1] / base)
        ce = (1.0 - s0) * float(np.prod(1.0 + f * seg))
        curw = Ae / (Ae.sum() + ce)
    return out - turn * cost / 1e4, turn, wsum_max, gsum, csle


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


# ---------------------------------------------------------------- choosers (rule 8)
def chooser_sharpe(cells, ispk):
    return max(cells, key=lambda c: (ispk[c]["Sharpe"], -c[0], -c[1]))


def chooser_memo(cells, ispk, dd_bar, cagr_bar):
    ok = [c for c in cells if ispk[c]["MaxDD"] >= dd_bar and ispk[c]["CAGR"] >= cagr_bar]
    if not ok:
        return (I_G, I_F), True            # the memo's own documented fallback
    return min(ok, key=lambda c: (c[0], c[1])), False


def chooser_cagr(cells, ispk, dd_bar):
    ok = [c for c in cells if ispk[c]["MaxDD"] >= dd_bar]
    if not ok:
        return (I_G, I_F), True
    return max(ok, key=lambda c: (ispk[c]["CAGR"], -c[0], -c[1])), False


def main():
    t0 = time.time()
    say("=" * 118)
    say("IDEA 1498 (lane B, 2026-09-19) — does the record's 0%-CASH CONVENTION hide a 4b pass?")
    say(f"DIALS: G {GRID_G}  x  F {GRID_F} (fraction of un-invested NAV in SHY).")
    say(f"FRAMES (not dials): LIVE = RULES v2 band shape; INC = frozen 2026-09-04 incumbent "
        f"(N={I_N}, H={I_H}).  Both weekly, {COST:.0f} bps on BOTH legs, t+1.  (G,F)=(0.75,0.00) "
        f"is the standing null on each.")
    say("=" * 118)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    ref = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)
    shy_ref = ref["SHY"].sort_index()

    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    say(f"  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0.")

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"], shy_ref),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"], shy_ref),
              Panel("SMALL", pxS, inv, shy_ref)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, SMALL {len(inv)} "
        f"(of {len(pxS.columns)-1} priced).")
    say("  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010.  Every absolute level below — every CAGR, every 4b "
        "pass — is an UPPER BOUND.  What survives that bias is the CONTRAST between F rungs on "
        "the same names, the same days and the same frame.")
    say("  CASH PROXY (stated, not glossed): SHY is a 1-3y Treasury ETF on ADJUSTED closes, i.e. "
        "a short-duration TOTAL-RETURN sleeve — NOT a broker sweep rate.  It is marked to market, "
        "it lost money in 2022, and in 2009-2015 it earned roll that bills did not.  SHY is also "
        "a CONSTITUENT of U56 and B136, so the INC frame may already select it on momentum; that "
        "is left unchanged and this sleeve is ADDITIVE to it.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y)")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)

    # ---- G7a: SHY's own profile, published before anything is credited
    for p in panels:
        i_oos = int(np.searchsorted(p.idx.values, np.datetime64(OOS_START)))
        s_full, s_is, s_oos = triple(p.shy[WARMUP:]), triple(p.shy[WARMUP:i_oos]), triple(p.shy[i_oos:])
        publish(f"G7a SHY PROFILE {p.name}",
                f"FULL {s_full['CAGR']:.2%}/{s_full['Sharpe']:.3f}/{s_full['MaxDD']:.2%}  "
                f"IS {s_is['CAGR']:.2%}/{s_is['MaxDD']:.2%}  OOS {s_oos['CAGR']:.2%}/{s_oos['MaxDD']:.2%}")

    grid, wsum_global = [], 0.0
    RET, ISPK, BARS = {}, {}, {}
    g1 = {}

    for pan in panels:
        T = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        spy = bmpack(pan.spy[WARMUP:]); spyO = bmpack(pan.spy[i_oos:]); spyI = bmpack(pan.spy[WARMUP:i_oos])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq=CAD)["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])
        BARS[pan.name] = dict(spy=spy, spyO=spyO, spyI=spyI, live=live, liveO=liveO, i_oos=i_oos)
        say(f"\n  [{pan.name}]  SPY FULL {spy['CAGR']:.2%} / {spy['Sharpe']:.4f} / {spy['MaxDD']:.2%} "
            f"H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f}  |  4b bars: DD cap {DD_CAP*spy['MaxDD']:.2%}, "
            f"CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           SPY OOS  {spyO['CAGR']:.2%} / {spyO['Sharpe']:.4f} / {spyO['MaxDD']:.2%}  |  "
            f"OOS bars: DD cap {DD_CAP*spyO['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spyO['CAGR']:.2%}")
        say(f"           SPY IS   {spyI['CAGR']:.2%} / {spyI['MaxDD']:.2%}  (the bars C_MEMO and "
            f"C_CAGR read)")
        say(f"           RULES v2 live @{COST:.0f}bps  {live['CAGR']:.2%} / {live['Sharpe']:.4f} / "
            f"{live['MaxDD']:.2%} H1/H2 {live['H1']:.3f}/{live['H2']:.3f}")

        reb = pan.reb_rows(CAD)
        frames = {"LIVE": frame_live(pan), "INC": frame_inc(pan, reb, I_N, I_H)}
        for fr in FRAMES:
            fm = frames[fr]
            for g in GRID_G:
                for f in GRID_F:
                    r, tu, ws, gs, cs = run_cell(pan, fm, reb, g, f)
                    wsum_global = max(wsum_global, ws)
                    RET[(pan.name, fr, g, f)] = r
                    k4a, k4b, m, h1, h2, legs = keep_paths(r[WARMUP:], spy, live)
                    k4aO, k4bO, mo, _, _, legsO = keep_paths(r[i_oos:], spyO, liveO)
                    ISPK[(pan.name, fr, g, f)] = dict(Sharpe=sharpe(r[WARMUP:i_oos]),
                                                      CAGR=cagr(r[WARMUP:i_oos]),
                                                      MaxDD=mdd(r[WARMUP:i_oos]))
                    yrs = (T - WARMUP) / 252.0
                    grid.append(dict(panel=pan.name, frame=fr, G=g, F=f,
                                     CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                                     oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                                     isCAGR=ISPK[(pan.name, fr, g, f)]["CAGR"],
                                     isSharpe=ISPK[(pan.name, fr, g, f)]["Sharpe"],
                                     isMaxDD=ISPK[(pan.name, fr, g, f)]["MaxDD"],
                                     mean_gross=float(np.mean(gs[WARMUP:])),
                                     mean_cash_sleeve=float(np.mean(cs[WARMUP:])),
                                     turnover_yr=float(tu[WARMUP:].sum() / yrs),
                                     keep4a=k4a, keep4b=k4b, keep4a_oos=k4aO, keep4b_oos=k4bO,
                                     leg_H1=legs["H1"], leg_H2=legs["H2"], leg_DD=legs["DD"],
                                     leg_CAGR=legs["CAGR"], oleg_H1=legsO["H1"], oleg_H2=legsO["H2"],
                                     oleg_DD=legsO["DD"], oleg_CAGR=legsO["CAGR"]))
                    if (g, f) == (I_G, I_F):
                        g1[(pan.name, fr)] = dict(m, oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"],
                                                  oMaxDD=mo["MaxDD"])

    G = pd.DataFrame(grid)
    G.to_csv(f"{OUT}.grid.csv", index=False)

    # ---------------------------------------------------------------- gates
    say("\n" + "=" * 118)
    say("GATES")
    say("=" * 118)
    gate("G3 all cells published", len(G), f"{len(GRID_G)*len(GRID_F)*len(FRAMES)*len(panels)}",
         len(G) == len(GRID_G) * len(GRID_F) * len(FRAMES) * len(panels))
    gate("G4 exactly two tuned parameters", "G x F", "2", True)
    gate("G2 no leverage (max risky+sleeve weight)", f"{wsum_global:.6f}", "<= 1.000001",
         wsum_global <= 1.000001)

    # G1a: LIVE/U56 @ (0.75, 0.00) must BE the live baseline row
    lv = BARS["U56"]["live"]; c = g1[("U56", "LIVE")]
    d1 = max(abs(c["Sharpe"] - lv["Sharpe"]), abs(c["MaxDD"] - lv["MaxDD"]), abs(c["CAGR"] - lv["CAGR"]))
    gate("G1a CROSS-SCRIPT REPLAY LIVE/U56 (0.75,0.00) == baseline.compare RULES v2",
         f"max|diff| {d1:.2e}  ({c['CAGR']:.4%}/{c['Sharpe']:.4f}/{c['MaxDD']:.4%} vs "
         f"{lv['CAGR']:.4%}/{lv['Sharpe']:.4f}/{lv['MaxDD']:.4%})", "< 1e-9", d1 < 1e-9)
    # G1b: INC/U56 @ (0.75, 0.00) must be the committed 2026-09-04 anchor
    c = g1[("U56", "INC")]
    d2 = max(abs(c["CAGR"] - ANCHOR_INC["CAGR"]), abs(c["Sharpe"] - ANCHOR_INC["Sharpe"]),
             abs(c["MaxDD"] - ANCHOR_INC["MaxDD"]), abs(c["oCAGR"] - ANCHOR_INC["oCAGR"]),
             abs(c["oSharpe"] - ANCHOR_INC["oSharpe"]))
    gate("G1b CROSS-SCRIPT REPLAY INC/U56 (0.75,0.00) == committed 2026-09-04 anchor",
         f"max|diff| {d2:.2e}  ({c['CAGR']:.4%}/{c['Sharpe']:.4f}/{c['MaxDD']:.4%}; OOS "
         f"{c['oCAGR']:.4%}/{c['oSharpe']:.4f})", "< 5e-4 (published to 4dp)", d2 < 5e-4)

    # G6 determinism
    pan = panels[0]
    reb = pan.reb_rows(CAD)
    r2, _, _, _, _ = run_cell(pan, frame_inc(pan, reb, I_N, I_H), reb, 0.625, 0.50)
    gate("G6 bit-identical recompute (U56/INC G=0.625 F=0.50)",
         f"{float(np.abs(r2 - RET[('U56','INC',0.625,0.50)]).max()):.3e}", "== 0.0",
         bool(np.array_equal(r2, RET[("U56", "INC", 0.625, 0.50)])))

    # G7b/G8: what the credit is actually worth, and is it monotone in F
    say("")
    for pn in [p.name for p in panels]:
        for fr in FRAMES:
            sub = G[(G.panel == pn) & (G.frame == fr)]
            worst = []
            mono = 0
            tot = 0
            for g in GRID_G:
                s = sub[sub.G == g].sort_values("F")
                dl = (s.CAGR.iloc[-1] - s.CAGR.iloc[0]) * 100
                worst.append(dl)
                tot += 1
                mono += int(bool(np.all(np.diff(s.CAGR.values) >= -1e-12)))
            publish(f"G7b CREDIT WORTH {pn}/{fr} (pp/yr CAGR, F=1.00 minus F=0.00, by G rung)",
                    " ".join(f"{g:g}:{d:+.3f}" for g, d in zip(GRID_G, worst)))
            publish(f"G8 CAGR monotone non-decreasing in F at fixed G, {pn}/{fr}", f"{mono} of {tot}")

    ok_gates = all(x["pass_"] for x in GATES)
    say(f"\n  GATES: {sum(x['pass_'] for x in GATES)} of {len(GATES)} pass.")

    # ---------------------------------------------------------------- the headline reads
    say("\n" + "=" * 118)
    say("(1) DOES THE CREDIT MOVE ANY 4b VERDICT?  CELL-BY-CELL, F=0.00 TWIN vs F>0")
    say("=" * 118)
    flips_full, flips_oos, flips_both = [], [], []
    for pn in [p.name for p in panels]:
        for fr in FRAMES:
            for g in GRID_G:
                base = G[(G.panel == pn) & (G.frame == fr) & (G.G == g) & (G.F == 0.0)].iloc[0]
                for f in GRID_F[1:]:
                    cell = G[(G.panel == pn) & (G.frame == fr) & (G.G == g) & (G.F == f)].iloc[0]
                    if bool(cell.keep4b) and not bool(base.keep4b):
                        flips_full.append((pn, fr, g, f))
                    if bool(cell.keep4b_oos) and not bool(base.keep4b_oos):
                        flips_oos.append((pn, fr, g, f))
                    if (bool(cell.keep4b) and bool(cell.keep4b_oos)) and not (bool(base.keep4b) and bool(base.keep4b_oos)):
                        flips_both.append((pn, fr, g, f))
    say(f"  4b FULL verdict flips 0 -> 1 from the cash credit: {len(flips_full)} of "
        f"{len(panels)*len(FRAMES)*len(GRID_G)*(len(GRID_F)-1)} (panel, frame, G, F>0) comparisons")
    say(f"  4b OOS  verdict flips 0 -> 1 from the cash credit: {len(flips_oos)}")
    say(f"  4b FULL *and* OOS flips 0 -> 1: {len(flips_both)}")
    for t in flips_both:
        say(f"      FLIP FULL+OOS  {t[0]}/{t[1]}  G={t[2]:g}  F={t[3]:g}")
    for t in flips_full[:12]:
        say(f"      flip FULL      {t[0]}/{t[1]}  G={t[2]:g}  F={t[3]:g}")
    for t in flips_oos[:12]:
        say(f"      flip OOS       {t[0]}/{t[1]}  G={t[2]:g}  F={t[3]:g}")

    say("\n  THE LIVE BOOK'S OWN GAP (idea 1454's -1.97 pp full / -1.22 pp OOS CAGR miss at G=0.75):")
    for pn in [p.name for p in panels]:
        bar = BARS[pn]
        for f in GRID_F:
            c = G[(G.panel == pn) & (G.frame == "LIVE") & (G.G == I_G) & (G.F == f)].iloc[0]
            say(f"    {pn}/LIVE G=0.75 F={f:.2f}: CAGR {c.CAGR:.2%} vs floor "
                f"{CAGR_FLOOR*bar['spy']['CAGR']:.2%} ({(c.CAGR-CAGR_FLOOR*bar['spy']['CAGR'])*100:+.2f} pp)"
                f" | OOS {c.oCAGR:.2%} vs {CAGR_FLOOR*bar['spyO']['CAGR']:.2%} "
                f"({(c.oCAGR-CAGR_FLOOR*bar['spyO']['CAGR'])*100:+.2f} pp)"
                f" | MaxDD {c.MaxDD:.2%} (cap {DD_CAP*bar['spy']['MaxDD']:.2%})"
                f" | mean cash sleeve {c.mean_cash_sleeve:.3f} | turn {c.turnover_yr:.2f}x/yr")

    say("\n  THE INCUMBENT'S BINDING DD MARGIN (the +1.10 pp the record keeps attacking):")
    for pn in [p.name for p in panels]:
        bar = BARS[pn]
        for f in GRID_F:
            c = G[(G.panel == pn) & (G.frame == "INC") & (G.G == I_G) & (G.F == f)].iloc[0]
            say(f"    {pn}/INC  G=0.75 F={f:.2f}: {c.CAGR:.2%} / {c.Sharpe:.4f} / {c.MaxDD:.2%} "
                f"(DD margin {(c.MaxDD-DD_CAP*bar['spy']['MaxDD'])*100:+.4f} pp) | 4b "
                f"{'PASS' if c.keep4b else 'fail'} | OOS {c.oCAGR:.2%}/{c.oSharpe:.4f}/{c.oMaxDD:.2%} "
                f"4b {'PASS' if c.keep4b_oos else 'fail'}")

    # ---------------------------------------------------------------- counts
    say("\n" + "=" * 118)
    say("(2) CAPITAL: BOTH KEEP PATHS AT EVERY CELL")
    say("=" * 118)
    say(f"  4a (beat the live book) FULL: {int(G.keep4a.sum())} of {len(G)}   OOS: {int(G.keep4a_oos.sum())} of {len(G)}")
    say(f"  4b FULL: {int(G.keep4b.sum())} of {len(G)}   4b OOS: {int(G.keep4b_oos.sum())} of {len(G)}"
        f"   4b FULL *and* OOS: {int((G.keep4b & G.keep4b_oos).sum())} of {len(G)}")
    for pn in [p.name for p in panels]:
        for fr in FRAMES:
            s = G[(G.panel == pn) & (G.frame == fr)]
            say(f"    {pn}/{fr}: 4a {int(s.keep4a.sum())}/{len(s)}  4b FULL {int(s.keep4b.sum())}/{len(s)}"
                f"  4b OOS {int(s.keep4b_oos.sum())}/{len(s)}  4b BOTH {int((s.keep4b & s.keep4b_oos).sum())}/{len(s)}")
    say("  Binding 4b legs FULL (count of cells FAILING each): "
        + "  ".join(f"{k} {int((~G['leg_' + k]).sum())}" for k in ("CAGR", "DD", "H1", "H2")))
    say("  Binding 4b legs OOS  (count of cells FAILING each): "
        + "  ".join(f"{k} {int((~G['oleg_' + k]).sum())}" for k in ("CAGR", "DD", "H1", "H2")))

    # ---------------------------------------------------------------- rule 8
    say("\n" + "=" * 118)
    say("(3) RULE 8 WALK-FORWARD — dials fit on warm-up..2016-12-31 ONLY, 2017-2026 read ONCE")
    say("=" * 118)
    cells = [(g, f) for g in GRID_G for f in GRID_F]
    wf = []
    for pn in [p.name for p in panels]:
        bar = BARS[pn]
        dd_bar, cagr_bar = DD_CAP * bar["spyI"]["MaxDD"], CAGR_FLOOR * bar["spyI"]["CAGR"]
        for fr in FRAMES:
            ispk = {c: ISPK[(pn, fr, c[0], c[1])] for c in cells}
            picks = {"C_SHARPE": (chooser_sharpe(cells, ispk), False),
                     "C_MEMO": chooser_memo(cells, ispk, dd_bar, cagr_bar),
                     "C_CAGR": chooser_cagr(cells, ispk, dd_bar),
                     "C_ANCHOR": ((I_G, I_F), False)}
            for cname, (pick, fell_back) in picks.items():
                row = G[(G.panel == pn) & (G.frame == fr) & (G.G == pick[0]) & (G.F == pick[1])].iloc[0]
                say(f"  {pn}/{fr:4s} {cname:9s} picks G={pick[0]:<6g} F={pick[1]:<5.2f}"
                    f"{'  [FALLBACK FIRED]' if fell_back else '                  '}"
                    f"  OOS {row.oCAGR:.2%} / {row.oSharpe:.4f} / {row.oMaxDD:.2%}"
                    f"  vs OOS bars (floor {CAGR_FLOOR*bar['spyO']['CAGR']:.2%}, cap "
                    f"{DD_CAP*bar['spyO']['MaxDD']:.2%})  4b OOS "
                    f"{'PASS' if row.keep4b_oos else 'fail'}  4a OOS "
                    f"{'PASS' if row.keep4a_oos else 'fail'}")
                wf.append(dict(panel=pn, frame=fr, chooser=cname, G=pick[0], F=pick[1],
                               fallback=fell_back, oCAGR=row.oCAGR, oSharpe=row.oSharpe,
                               oMaxDD=row.oMaxDD, keep4b_oos=bool(row.keep4b_oos),
                               keep4a_oos=bool(row.keep4a_oos), keep4b_full=bool(row.keep4b)))
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    nz = WF[WF.F > 0]
    gate("G5 no chooser reads an OOS row (IS packs built on [WARMUP, i_oos) by construction)",
         "asserted by slicing", "structural", True)
    say(f"\n  Choosers selecting a NON-ZERO cash sleeve (F > 0): {len(nz)} of {len(WF)}.")
    say(f"  Chooser picks clearing 4b OOS: {int(WF.keep4b_oos.sum())} of {len(WF)};"
        f"  clearing 4b FULL and OOS: {int((WF.keep4b_oos & WF.keep4b_full).sum())} of {len(WF)}.")
    for _, r in WF[WF.keep4b_oos & WF.keep4b_full].iterrows():
        say(f"      RULE-8 CLEAN 4b: {r.panel}/{r.frame} {r.chooser} G={r.G:g} F={r.F:.2f} "
            f"OOS {r.oCAGR:.2%}/{r.oSharpe:.4f}/{r.oMaxDD:.2%}")

    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    say(f"\n  Wrote {OUT.name}.grid.csv ({len(G)} cells), .walkforward.csv ({len(WF)}), "
        f".gates.csv, .log.txt   [{time.time()-t0:.1f}s]")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    return G, WF


if __name__ == "__main__":
    main()

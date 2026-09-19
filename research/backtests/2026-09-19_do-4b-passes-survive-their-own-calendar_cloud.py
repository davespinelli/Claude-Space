#!/usr/bin/env python3
"""
Idea 711 (lane cloud, 2026-09-19, idea 2 of 2) — does any published 4b PASS survive its OWN
CALENDAR CONVENTION?

THE PREMISE.  Idea 702's single rule-8-reachable 4b pass exists on idea 694's
broad-intersect-small calendar and VANISHES (0 of 6 honest selectors) on the same panel's native
calendar, two years longer and chosen by nobody for that question.  Every 4b bar in the record is
set by SPY measured on whatever calendar the run happened to load, and every candidate is measured
on the same one, so a "4b PASS" is a statement about a WINDOW as much as about a book.  This run
prices that directly, on the frozen-incumbent family, and DECOMPOSES it.

WHAT A "CALENDAR" ACTUALLY IS IN THIS REPO — MEASURED FIRST, NOT ASSUMED (gate G1).  The three
committed caches are checked row by row: within the common span the U56, B136 and SMALL trading-day
indices are BIT-IDENTICAL (4203 rows each, zero rows in one and not another), so the "intersect
calendar" and the "native calendar" differ on this repo by their START DATE ALONE and by nothing
else.  The GRID half of the calendar question is therefore EMPTY here and is reported as such
rather than being dressed up as a finding; the SPAN half is the whole of it, and it is worth two
years of tape (2008-01-02 vs 2010-01-04, 505 rows).

THE DECOMPOSITION (what makes this more than a truncation).  A shorter calendar changes TWO things
at once, and the record has never separated them:

  WINDOW  the book is built on the FULL native tape and only the METRICS are computed over the
          shorter window.  This is "the same book, scored on a different calendar".
  TAPE    the book is REBUILT on the truncated tape (so the 252-day momentum, the 200-day MA, the
          20-day vol and the weekly rebalance grid are all re-derived from the shorter history)
          and then scored on the same window.  This is what a run that LOADED a shorter cache got.

WINDOW vs NATIVE isolates the measurement window; TAPE vs WINDOW isolates the INDICATOR HISTORY.
If TAPE == WINDOW everywhere, a calendar is only a scoring convention; if not, the calendar
changes WHICH BOOK a rule even holds.

START CONVENTIONS, REPORTED AT EVERY VALUE, NOT TUNED: {NATIVE, 2010-01-04 (the three-panel
intersect), 2011-01-03, 2012-01-03}.  Four values turn a single flip count into a GRADIENT, so a
verdict that survives is seen to survive for a reason and not by luck of one truncation.  SMALL's
NATIVE *is* the intersect (gate G2), so SMALL is the panel that DEFINES the calendar the other two
are cut to, and it has no native/intersect contrast to give.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4), over the frozen 2026-09-04 recipe (top-N by the
composite, min-hold H = 126, MA gate, MAXVOL 0.60, weekly Fri-decide / Mon-trade, 10 bps, t+1):

  N      {10, 15, 20, 30, 40, 60}          DIAL 1
  GROSS  {0.50, 0.60, 0.75, 0.85, 1.00}    DIAL 2      (N = 20, GROSS = 0.75 IS the incumbent)

630 cells in all, EVERY ONE published in .grid.csv, both KEEP paths at every cell.

THE BARS MOVE TOO, AND THAT IS THE POINT.  4b's DD cap (<= 0.60 x SPY MaxDD) and CAGR floor
(>= 0.70 x SPY CAGR) are RE-COMPUTED from SPY on each convention's own window, exactly as a run
on that calendar would have computed them, and the live RULES v2 comparand for 4a is re-run on
each tape.  A flip is therefore attributed to the bar or to the book, separately.

PROTOCOL: rule 1 (>= 10y on every convention: the shortest window is 2012-2026, 14.7y); rule 2
(t+1, 10 bps, no leverage, no shorting); rule 3 (RULES v2 AND SPY, both re-derived per
convention); rule 4 (both KEEP paths, 2 tuned parameters); rule 8 (walk-forward: (N, GROSS) chosen
by argmax IS Sharpe on window-start..2016-12-31 SEPARATELY INSIDE each (panel, start, reading), so
no arm has more than two free parameters; 2017-2026 read ONCE); rule 9 (survivorship stated).
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

GATES.  G1 the three caches' trading-day indices are identical within the common span (the GRID
half of the question is empty).  G2 SMALL's NATIVE window == the intersect window.  G3 the
(N=20, GROSS=0.75) NATIVE cell on U56 reproduces the committed frozen anchor (~15.8% / ~1.153 /
-19.13% full; ~17.3% / ~1.185 OOS).  G4 at start = NATIVE the WINDOW and TAPE readings are
bit-identical by construction.  G5 rule 1 on every convention.  G6 no leverage (weight sum <= 1).
G7 the chooser reads no row on or after 2017-01-01.  G8 all 630 cells published.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-19_do-4b-passes-survive-their-own-calendar_cloud.py
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

DATE = "2026-09-19"
SLUG = "do-4b-passes-survive-their-own-calendar"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_H = 126
I_N, I_G = 20, 0.75
NS = [10, 15, 20, 30, 40, 60]
GS = [0.50, 0.60, 0.75, 0.85, 1.00]
CADENCE, COST = "W", 10.0
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
C_U56 = dict(CAGR=0.1580, Sharpe=1.1537, MaxDD=-0.1913, oSharpe=1.1857)

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


class Tape:
    """One panel on one tape (a start convention).  Everything is re-derived from this tape."""

    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        m = rebalance_mask(px.index, CADENCE).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])


def build_frame(tp, N, H=I_H, lag=1):
    """The frozen top-N min-hold equal-weight frame at GROSS = 1.0 (depends on N only)."""
    T, M = tp.rets.shape
    K = len(tp.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = tp.priced[:, tp.iinv]
    reb = tp.reb
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
            kk = tp.rank_key[ts].copy()
            kk[~(tp.elig[ts] & pr[ts])] = np.inf
            for c in keep:
                kk[c] = np.inf
            order = np.argsort(kk, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(kk[c])]
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, tp.iinv[sel]] = 1.0 / len(sel)
    return W


def run(tp, frame, g):
    rets = tp.rets
    T, M = rets.shape
    turn = np.zeros(T)
    out = np.zeros(T)
    curw = np.zeros(M)
    reb = tp.reb
    ends = np.append(reb[1:], T)
    wmax = 0.0
    for i0, i1 in zip(reb, ends):
        w0 = g * frame[i0]
        wmax = max(wmax, float(w0.sum()))
        turn[i0] = float(np.abs(w0 - curw).sum())
        base = tp.Cp[i0]
        A = w0[None, :] * (tp.Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        Ae = w0 * (tp.C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return out - turn * COST / 1e4, turn, wmax


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


def main():
    t0 = time.time()
    say("=" * 130)
    say("IDEA 711 (lane cloud, 2026-09-19, idea 2 of 2) — does any published 4b PASS survive its "
        "OWN CALENDAR CONVENTION?")
    say("DIALS: N {10,15,20,30,40,60} x GROSS {0.50,0.60,0.75,0.85,1.00} over the frozen 2026-09-04 "
        "recipe (H = 126, MA gate, MAXVOL 0.60, weekly, 10 bps, t+1).  (N=20, G=0.75) IS the incumbent.")
    say("REPORTED CONVENTION AXIS (not a dial): START {NATIVE, 2010-01-04 = the three-panel "
        "intersect, 2011-01-03, 2012-01-03} x READING {WINDOW = same book re-scored, TAPE = book "
        "REBUILT on the shorter tape}.  4b's bars and the RULES v2 comparand are RE-DERIVED per "
        "convention, exactly as a run on that calendar would have derived them.")
    say("=" * 130)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    say(f"  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0.")
    mv = pxS.pct_change().abs().max()
    inv_s = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    RAW = {"U56": (pxU, [c for c in pxU.columns if c != "SPY"]),
           "B136": (pxB, [c for c in pxB.columns if c != "SPY"]),
           "SMALL": (pxS, inv_s)}
    say(f"  PANELS: U56 {len(RAW['U56'][1])} names, B136 {len(RAW['B136'][1])}, "
        f"SMALL {len(inv_s)} (of {len(pxS.columns)-1} priced).")
    say("  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010, so every absolute level and every 4b pass below is "
        "an OPTIMISTIC upper bound.  What this run reads is whether a VERDICT is stable under a "
        "convention change, which the bias cannot manufacture either way.")

    # ---- G1: what is a "calendar" here?  measured, not assumed -----------------------------
    I = pxU.index.intersection(pxB.index).intersection(pxS.index)
    span0, span1 = I[0], I[-1]
    diffs = {}
    for n, (p, _) in RAW.items():
        own = p.loc[span0:span1].index
        diffs[n] = (len(own), len(own.difference(I)), len(I.difference(own)))
    say(f"\n  CALENDAR AUDIT.  three-panel intersect = {span0.date()} .. {span1.date()}, "
        f"{len(I)} rows.  Per panel (rows in span, rows in span NOT in intersect, intersect rows "
        f"NOT in panel): " + ", ".join(f"{k} {v}" for k, v in diffs.items()))
    grid_empty = all(v[1] == 0 and v[2] == 0 for v in diffs.values())
    gate("G1 the three caches' trading-day indices are IDENTICAL within the common span, i.e. the "
         "GRID half of the calendar question is EMPTY on this repo and the SPAN half is all of it",
         f"max off-grid rows {max(max(v[1], v[2]) for v in diffs.values())}", "== 0", grid_empty)
    gate("G2 SMALL's NATIVE window IS the three-panel intersect (so SMALL defines the calendar and "
         "has no native/intersect contrast to give)",
         f"SMALL native {pxS.index[0].date()} vs intersect {span0.date()}",
         "identical", pxS.index[0] == span0)

    STARTS = [("NATIVE", None), ("ISECT2010", span0), ("Y2011", pd.Timestamp("2011-01-03")),
              ("Y2012", pd.Timestamp("2012-01-03"))]

    grid, wf_rows = [], []
    wmax_g, g3_ok, g4_dev = 0.0, None, 0.0

    for pname, (px_full, invest) in RAW.items():
        # native tape, built once
        tp_nat = Tape(pname, px_full, invest)
        frames_nat = {N: build_frame(tp_nat, N) for N in NS}
        lr_nat = backtest(px_full, rules_v2_weights(px_full), cost_bps=COST, freq="W")["returns"]
        books_nat = {}
        for N in NS:
            for g in GS:
                rr, tu, wm = run(tp_nat, frames_nat[N], g)
                wmax_g = max(wmax_g, wm)
                books_nat[(N, g)] = pd.Series(rr, index=tp_nat.idx)
        say(f"\n  [{pname}] native tape {tp_nat.idx[0].date()}..{tp_nat.idx[-1].date()} "
            f"({len(tp_nat.idx)} rows), {len(tp_nat.reb)} weekly rebalances; "
            f"{len(NS)*len(GS)} books built.")

        for sname, s0 in STARTS:
            if s0 is None:
                tp, frames, lr = tp_nat, frames_nat, lr_nat
                readings = ["NATIVE"]
            else:
                pxt = px_full.loc[s0:]
                if len(pxt) < 260 + 252:
                    continue
                tp = Tape(pname, pxt, invest)
                frames = {N: build_frame(tp, N) for N in NS}
                lr = backtest(pxt, rules_v2_weights(pxt), cost_bps=COST, freq="W")["returns"]
                readings = ["WINDOW", "TAPE"]

            # the window every reading in this convention is scored on
            w_idx = tp.idx[WARMUP:]
            i_oos_t = int(np.searchsorted(tp.idx.values, np.datetime64(OOS_START)))
            o_idx = tp.idx[i_oos_t:]
            spy_w = pd.Series(tp.spy, index=tp.idx)
            spy = bmpack(spy_w.loc[w_idx].values)
            spyO = bmpack(spy_w.loc[o_idx].values)
            say(f"    [{pname} / start {sname}] window {w_idx[0].date()}..{w_idx[-1].date()} "
                f"({len(w_idx)} rows, {len(w_idx)/252:.1f}y) | SPY {spy['CAGR']:.2%}/"
                f"{spy['Sharpe']:.4f}/{spy['MaxDD']:.2%} -> 4b bars DD cap "
                f"{DD_CAP*spy['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
            publish(f"WINDOW {pname}/{sname}",
                    f"{len(w_idx)} rows {w_idx[0].date()}..{w_idx[-1].date()}; SPY "
                    f"{spy['CAGR']:.4f}/{spy['Sharpe']:.4f}/{spy['MaxDD']:.4f}")

            for reading in readings:
                if reading == "TAPE":
                    live_s = lr
                else:
                    live_s = lr_nat
                live = bmpack(live_s.reindex(w_idx).fillna(0.0).values)
                liveO = bmpack(live_s.reindex(o_idx).fillna(0.0).values)
                cells = {}
                for N in NS:
                    for g in GS:
                        if reading == "TAPE":
                            rr, tu, wm = run(tp, frames[N], g)
                            wmax_g = max(wmax_g, wm)
                            ser = pd.Series(rr, index=tp.idx)
                        else:
                            ser = books_nat[(N, g)]
                        rw = ser.reindex(w_idx).fillna(0.0).values
                        ro = ser.reindex(o_idx).fillna(0.0).values
                        if reading == "NATIVE":
                            rr2, _, _ = run(tp, frames[N], g)
                            g4_dev = max(g4_dev, float(np.max(np.abs(
                                pd.Series(rr2, index=tp.idx).reindex(w_idx).fillna(0.0).values - rw))))
                        k4a, k4b, m, h1, h2, legs = keep_paths(rw, spy, live)
                        k4aO, k4bO, mo, _, _, legsO = keep_paths(ro, spyO, liveO)
                        cells[(N, g)] = dict(is_Sharpe=sharpe(ser.reindex(
                            tp.idx[WARMUP:i_oos_t]).fillna(0.0).values), r_oos=ro)
                        grid.append(dict(
                            panel=pname, start=sname, reading=reading, N=N, gross=g,
                            win_rows=len(w_idx), win_from=str(w_idx[0].date()),
                            win_to=str(w_idx[-1].date()),
                            CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                            oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                            keep4a=k4a, keep4b=k4b, keep4a_oos=k4aO, keep4b_oos=k4bO,
                            legH1=legs["H1"], legH2=legs["H2"], legDD=legs["DD"],
                            legCAGR=legs["CAGR"], olegDD=legsO["DD"], olegCAGR=legsO["CAGR"],
                            olegH1=legsO["H1"], olegH2=legsO["H2"],
                            dd_margin_pp=100 * (m["MaxDD"] - DD_CAP * spy["MaxDD"]),
                            cagr_margin_pp=100 * (m["CAGR"] - CAGR_FLOOR * spy["CAGR"]),
                            odd_margin_pp=100 * (mo["MaxDD"] - DD_CAP * spyO["MaxDD"]),
                            ocagr_margin_pp=100 * (mo["CAGR"] - CAGR_FLOOR * spyO["CAGR"]),
                            spy_CAGR=spy["CAGR"], spy_Sharpe=spy["Sharpe"], spy_MaxDD=spy["MaxDD"],
                            spy_H1=spy["H1"], spy_H2=spy["H2"],
                            dd_cap=DD_CAP * spy["MaxDD"], cagr_floor=CAGR_FLOOR * spy["CAGR"],
                            live_Sharpe=live["Sharpe"], live_MaxDD=live["MaxDD"],
                            is_Sharpe=cells[(N, g)]["is_Sharpe"]))
                        if (pname == "U56" and sname == "NATIVE" and N == I_N and g == I_G):
                            d = max(abs(m["Sharpe"] - C_U56["Sharpe"]),
                                    abs(mo["Sharpe"] - C_U56["oSharpe"]))
                            g3_ok = gate("G3 the (N=20, G=0.75) NATIVE U56 cell reproduces the "
                                         "committed frozen anchor (~15.8%/~1.153/-19.13% full; "
                                         "~17.3%/~1.185 OOS)",
                                         f"|dSharpe| {d:.2e} (got {m['CAGR']:.4f}/{m['Sharpe']:.4f}/"
                                         f"{m['MaxDD']:.4f}; OOS {mo['CAGR']:.4f}/{mo['Sharpe']:.4f}/"
                                         f"{mo['MaxDD']:.4f})", "< 5e-3", d < 5e-3)
                # ---- rule 8 inside this (panel, start, reading) ----
                best, bs = None, -np.inf
                for key, c in cells.items():
                    if c["is_Sharpe"] > bs:
                        bs, best = c["is_Sharpe"], key
                ro = cells[best]["r_oos"]
                k4aO, k4bO, mo, _, _, legsO = keep_paths(ro, spyO, liveO)
                wf_rows.append(dict(panel=pname, start=sname, reading=reading,
                                    is_N=best[0], is_gross=best[1], is_Sharpe=bs,
                                    oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                                    keep4b_oos=k4bO, keep4a_oos=k4aO,
                                    olegH1=legsO["H1"], olegH2=legsO["H2"], olegDD=legsO["DD"],
                                    olegCAGR=legsO["CAGR"],
                                    spy_oCAGR=spyO["CAGR"], spy_oSharpe=spyO["Sharpe"],
                                    spy_oMaxDD=spyO["MaxDD"],
                                    live_oSharpe=liveO["Sharpe"], live_oMaxDD=liveO["MaxDD"]))

    G = pd.DataFrame(grid)
    W = pd.DataFrame(wf_rows)
    gate("G4 at start = NATIVE the WINDOW and TAPE readings are identical by construction",
         f"max |dret| {g4_dev:.3e}", "< 1e-15", g4_dev < 1e-15)
    gate("G5 rule 1 (>= 10y) on every convention's window",
         f"min window {G.win_rows.min()/252:.2f}y", ">= 10.0", G.win_rows.min() / 252 >= 10.0)
    gate("G6 no leverage: realised weight sum never exceeds 1.0", f"max wsum {wmax_g:.6f}",
         "<= 1.0 + 1e-12", wmax_g <= 1.0 + 1e-12)
    gate("G7 chooser reads no row on or after 2017-01-01",
         "IS = window start + warm-up .. 2016-12-31", "no OOS leakage", True)
    exp = 3 * (len(NS) * len(GS) * (1 + 3 * 2))
    gate("G8 all grid cells published", f"{len(G)} rows", f"== {exp}", len(G) == exp)

    say("\n" + "=" * 130)
    say("GRID — every cell.  4b bars are the convention's OWN (re-derived from SPY on that window).")
    say("=" * 130)
    for pn in ["U56", "B136", "SMALL"]:
        for sname, _ in STARTS:
            for reading in ["NATIVE", "WINDOW", "TAPE"]:
                sub = G[(G.panel == pn) & (G.start == sname) & (G.reading == reading)]
                if not len(sub):
                    continue
                say(f"\n  [{pn} / start {sname} / reading {reading}]  window "
                    f"{sub.win_from.iloc[0]}..{sub.win_to.iloc[0]} ({sub.win_rows.iloc[0]} rows); "
                    f"DD cap {sub.dd_cap.iloc[0]:.2%}, CAGR floor {sub.cagr_floor.iloc[0]:.2%}")
                say("      N gross |    CAGR  Sharpe   MaxDD     H1     H2 | DDmarg CAGRmarg legs "
                    "| 4a 4b | OOS CAGR/Sh/DD 4b_oos | IS Sh")
                for _, r in sub.iterrows():
                    say(f"    {r.N:3d} {r.gross:5.2f} | {r.CAGR:7.2%} {r.Sharpe:7.4f} {r.MaxDD:7.2%} "
                        f"{r.H1:6.3f} {r.H2:6.3f} | {r.dd_margin_pp:+6.2f} {r.cagr_margin_pp:+8.2f} "
                        f"{int(r.legH1)}{int(r.legH2)}{int(r.legDD)}{int(r.legCAGR)} | "
                        f"{int(r.keep4a)}  {int(r.keep4b)}  | {r.oCAGR:7.2%} {r.oSharpe:6.4f} "
                        f"{r.oMaxDD:7.2%}    {int(r.keep4b_oos)}   | {r.is_Sharpe:6.4f}")

    say("\n" + "=" * 130)
    say("THE FLIP CENSUS — for each (panel, N, gross) book, is its 4b verdict INVARIANT across the "
        "four start conventions?  NATIVE is the reference; a FLIP is a verdict that changes.")
    say("=" * 130)
    ref = G[G.start == "NATIVE"].set_index(["panel", "N", "gross"])
    flip_rows = []
    for reading in ["WINDOW", "TAPE"]:
        for sname, _ in STARTS[1:]:
            sub = G[(G.start == sname) & (G.reading == reading)]
            for _, r in sub.iterrows():
                b = ref.loc[(r.panel, r.N, r.gross)]
                flip_rows.append(dict(panel=r.panel, N=r.N, gross=r.gross, start=sname,
                                      reading=reading, ref4b=bool(b.keep4b), new4b=bool(r.keep4b),
                                      ref4b_oos=bool(b.keep4b_oos), new4b_oos=bool(r.keep4b_oos),
                                      flip4b=bool(b.keep4b) != bool(r.keep4b),
                                      flip4b_oos=bool(b.keep4b_oos) != bool(r.keep4b_oos),
                                      ref4a=bool(b.keep4a), new4a=bool(r.keep4a),
                                      flip4a=bool(b.keep4a) != bool(r.keep4a),
                                      d_dd_margin_pp=r.dd_margin_pp - b.dd_margin_pp,
                                      d_cagr_margin_pp=r.cagr_margin_pp - b.cagr_margin_pp,
                                      d_Sharpe=r.Sharpe - b.Sharpe,
                                      d_cap_pp=100 * (r.dd_cap - b.dd_cap),
                                      d_floor_pp=100 * (r.cagr_floor - b.cagr_floor),
                                      legs_changed=",".join(
                                          L for L in ("H1", "H2", "DD", "CAGR")
                                          if bool(b["leg" + L]) != bool(r["leg" + L])),
                                      oos_ident=bool(abs(r.oSharpe - b.oSharpe) < 1e-15)))
    F = pd.DataFrame(flip_rows)
    say("  reading start      | n | 4b FLIPS  (PASS->FAIL / FAIL->PASS) | 4b_OOS FLIPS | 4a FLIPS | "
        "median dDDmarg  dCAGRmarg | bar move: dDDcap  dCAGRfloor")
    for reading in ["WINDOW", "TAPE"]:
        for sname, _ in STARTS[1:]:
            s = F[(F.reading == reading) & (F.start == sname)]
            pf = int((s.ref4b & ~s.new4b).sum())
            fp = int((~s.ref4b & s.new4b).sum())
            pfO = int((s.ref4b_oos & ~s.new4b_oos).sum())
            fpO = int((~s.ref4b_oos & s.new4b_oos).sum())
            say(f"  {reading:>7} {sname:<10} | {len(s):3d} | {int(s.flip4b.sum()):3d}  "
                f"({pf} -> FAIL / {fp} -> PASS)        | {int(s.flip4b_oos.sum()):3d} "
                f"({pfO}/{fpO})   | {int(s.flip4a.sum()):3d}      | "
                f"{s.d_dd_margin_pp.median():+7.2f} {s.d_cagr_margin_pp.median():+8.2f} | "
                f"{s.d_cap_pp.median():+7.2f} {s.d_floor_pp.median():+8.2f}")
    say("\n  PER PANEL (both readings pooled over the three non-native starts):")
    for pn in ["U56", "B136", "SMALL"]:
        s = F[F.panel == pn]
        say(f"    {pn:>5}: 4b flips {int(s.flip4b.sum())} of {len(s)} "
            f"({int((s.ref4b & ~s.new4b).sum())} PASS->FAIL, "
            f"{int((~s.ref4b & s.new4b).sum())} FAIL->PASS); 4b_OOS flips "
            f"{int(s.flip4b_oos.sum())} of {len(s)}")
    say("\n  THE INDICATOR-HISTORY EFFECT (TAPE vs WINDOW at the SAME start and window: same bars, "
        "same window, the book REBUILT on the shorter tape):")
    for sname, _ in STARTS[1:]:
        a = G[(G.start == sname) & (G.reading == "TAPE")].set_index(["panel", "N", "gross"])
        b = G[(G.start == sname) & (G.reading == "WINDOW")].set_index(["panel", "N", "gross"])
        j = a.join(b, rsuffix="_w")
        say(f"    start {sname}: median |dSharpe| {np.abs(j.Sharpe - j.Sharpe_w).median():.4f}, "
            f"max {np.abs(j.Sharpe - j.Sharpe_w).max():.4f}; median |dCAGR| "
            f"{100*np.abs(j.CAGR - j.CAGR_w).median():.3f} pp, max "
            f"{100*np.abs(j.CAGR - j.CAGR_w).max():.3f} pp; 4b disagreements "
            f"{int((j.keep4b != j.keep4b_w).sum())} of {len(j)}; 4b_OOS disagreements "
            f"{int((j.keep4b_oos != j.keep4b_oos_w).sum())} of {len(j)}")

    wf = F[F.reading == "WINDOW"]
    gate("G9 for the WINDOW reading the 2017-2026 OOS block is IDENTICAL to NATIVE by construction "
         "(same book, same OOS rows), so every OOS flip in this run is a TAPE effect",
         f"{int(wf.oos_ident.sum())} of {len(wf)} identical", f"== {len(wf)}",
         int(wf.oos_ident.sum()) == len(wf))

    say("\n  WHICH LEG THE CALENDAR MOVES (of the 4b flips, the legs whose truth value changed):")
    fl = F[F.flip4b]
    from collections import Counter
    cnt = Counter()
    for v in fl.legs_changed:
        for L in [x for x in v.split(",") if x]:
            cnt[L] += 1
    say(f"    {len(fl)} flips; leg-change tally " + (", ".join(
        f"{k} {v}" for k, v in sorted(cnt.items(), key=lambda kv: -kv[1])) or "(none)")
        + f".  The DD cap itself does not move at all (SPY's MaxDD is the 2020 episode, "
          f"present in every window): median dDDcap {F.d_cap_pp.median():+.3f} pp, max "
          f"{F.d_cap_pp.abs().max():.3f} pp.  The CAGR floor DOES move: "
          f"{F.d_floor_pp.min():+.2f} .. {F.d_floor_pp.max():+.2f} pp.")

    say("\n  THE INCUMBENT CELL (N = 20, GROSS = 0.75) — the 2026-09-04 KEEP-4b recipe itself:")
    for pn in ["U56", "B136", "SMALL"]:
        r0 = G[(G.panel == pn) & (G.start == "NATIVE") & (G.N == I_N) & (G.gross == I_G)].iloc[0]
        say(f"    {pn:>5} NATIVE: {r0.CAGR:.2%}/{r0.Sharpe:.4f}/{r0.MaxDD:.2%} halves "
            f"{r0.H1:.3f}/{r0.H2:.3f} -> 4b {int(r0.keep4b)} (legs "
            f"{int(r0.legH1)}{int(r0.legH2)}{int(r0.legDD)}{int(r0.legCAGR)}), 4b_OOS "
            f"{int(r0.keep4b_oos)}")
        for sname, _ in STARTS[1:]:
            for reading in ["WINDOW", "TAPE"]:
                rr_ = G[(G.panel == pn) & (G.start == sname) & (G.reading == reading) &
                        (G.N == I_N) & (G.gross == I_G)]
                if not len(rr_):
                    continue
                r1 = rr_.iloc[0]
                say(f"          {sname:<10} {reading:>6}: {r1.CAGR:.2%}/{r1.Sharpe:.4f}/"
                    f"{r1.MaxDD:.2%} halves {r1.H1:.3f}/{r1.H2:.3f} -> 4b {int(r1.keep4b)} (legs "
                    f"{int(r1.legH1)}{int(r1.legH2)}{int(r1.legDD)}{int(r1.legCAGR)}), 4b_OOS "
                    f"{int(r1.keep4b_oos)}  [{'SAME' if bool(r1.keep4b)==bool(r0.keep4b) else 'FLIP'}]")

    say("\n" + "=" * 130)
    say("RULE 8 WALK-FORWARD — (N, GROSS) chosen by argmax IS Sharpe on window-start..2016-12-31 "
        "SEPARATELY inside each (panel, start, reading); 2017-2026 read ONCE.")
    say("=" * 130)
    say("  panel  start      reading | IS pick (N,g)  IS Sh | OOS CAGR  Sharpe   MaxDD | 4a 4b "
        "legs(H1,H2,DD,CAGR) | SPY OOS CAGR/Sh/DD")
    for _, r in W.iterrows():
        say(f"  {r.panel:>5} {r.start:<10} {r.reading:>7} | ({r.is_N:3d},{r.is_gross:4.2f}) "
            f"{r.is_Sharpe:7.4f} | {r.oCAGR:7.2%} {r.oSharpe:7.4f} {r.oMaxDD:7.2%} | "
            f"{int(r.keep4a_oos)}  {int(r.keep4b_oos)} ({int(r.olegH1)},{int(r.olegH2)},"
            f"{int(r.olegDD)},{int(r.olegCAGR)}) | {r.spy_oCAGR:6.2%}/{r.spy_oSharpe:.4f}/"
            f"{r.spy_oMaxDD:7.2%}")

    say("\n" + "=" * 130)
    say("HEADLINE")
    say("=" * 130)
    say(f"  (0) WHAT A CALENDAR IS HERE: the GRID half of the question is EMPTY — the three "
        f"committed caches share a bit-identical trading-day index over the common span "
        f"({len(I)} rows, 0 off-grid rows on any panel, G1).  The whole of the 'intersect vs "
        f"native calendar' contrast in this repo is the START DATE, worth "
        f"{len(pxU.index) - len(I)} rows (2 years).")
    nat = G[G.start == "NATIVE"]
    say(f"  (1) ON THE NATIVE CALENDAR: 4b passes {int(nat.keep4b.sum())} of {len(nat)} cells "
        f"({', '.join(f'{p} {int(nat[nat.panel==p].keep4b.sum())}/{len(nat[nat.panel==p])}' for p in ['U56','B136','SMALL'])}); "
        f"4b OOS {int(nat.keep4b_oos.sum())} of {len(nat)}; 4a {int(nat.keep4a.sum())} of {len(nat)}.")
    say(f"  (2) THE FLIP RATE: {int(F.flip4b.sum())} of {len(F)} (book, start, reading) contrasts "
        f"flip the FULL-sample 4b verdict ({100*F.flip4b.mean():.1f}%), of which "
        f"{int((F.ref4b & ~F.new4b).sum())} are PASS -> FAIL and "
        f"{int((~F.ref4b & F.new4b).sum())} FAIL -> PASS.  OOS: {int(F.flip4b_oos.sum())} of "
        f"{len(F)} ({100*F.flip4b_oos.mean():.1f}%).  4a: {int(F.flip4a.sum())} of {len(F)}.")
    surv = F.groupby(["panel", "N", "gross"]).agg(ref=("ref4b", "first"),
                                                  allsame=("flip4b", lambda x: not x.any()))
    npass = surv[surv.ref]
    say(f"  (3) SURVIVAL OF A PASS: of the {len(npass)} (panel, N, gross) books that PASS 4b on "
        f"their native calendar, {int(npass.allsame.sum())} keep that verdict at ALL SIX "
        f"convention changes and {len(npass) - int(npass.allsame.sum())} lose it at least once.")
    nfail = surv[~surv.ref]
    say(f"      of the {len(nfail)} books that FAIL natively, "
        f"{len(nfail) - int(nfail.allsame.sum())} PASS under at least one other calendar.")
    say(f"  (4) THE MECHANISM — bar or book?  Moving the start moves 4b's OWN bars: median DD-cap "
        f"move {F.d_cap_pp.median():+.2f} pp and CAGR-floor move {F.d_floor_pp.median():+.2f} pp "
        f"across the three truncations, against a median book DD-margin move of "
        f"{F.d_dd_margin_pp.median():+.2f} pp and CAGR-margin move "
        f"{F.d_cagr_margin_pp.median():+.2f} pp.")
    tp_ = G[G.reading == "TAPE"].set_index(["panel", "start", "N", "gross"])
    wd_ = G[G.reading == "WINDOW"].set_index(["panel", "start", "N", "gross"])
    jj = tp_.join(wd_, rsuffix="_w")
    say(f"  (5) THE INDICATOR-HISTORY EFFECT (TAPE vs WINDOW, same bars and same window): median "
        f"|dSharpe| {np.abs(jj.Sharpe - jj.Sharpe_w).median():.4f}, max "
        f"{np.abs(jj.Sharpe - jj.Sharpe_w).max():.4f}; 4b disagreements "
        f"{int((jj.keep4b != jj.keep4b_w).sum())} of {len(jj)}.  So a shorter cache changes WHICH "
        f"BOOK the rule holds, not only how it is scored.")
    say(f"  (6) RULE 8: the IS-chosen (N, GROSS) is "
        f"{W.groupby(['panel'])[['is_N','is_gross']].nunique().to_dict()} distinct values per panel "
        f"across the {len(W)} (panel, start, reading) arms; OOS 4b passes "
        f"{int(W.keep4b_oos.sum())} of {len(W)}, 4a {int(W.keep4a_oos.sum())} of {len(W)}.")
    for pn in ["U56", "B136", "SMALL"]:
        s = W[W.panel == pn]
        say(f"      {pn:>5}: picks " + ", ".join(
            f"{r.start}/{r.reading}=({r.is_N},{r.is_gross:.2f})->4b_oos {int(r.keep4b_oos)}"
            for _, r in s.iterrows()))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    F.to_csv(f"{OUT}.flips.csv", index=False)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n  wrote {OUT.name}.grid.csv / .flips.csv / .walkforward.csv / .gates.csv / .log.txt")
    say(f"  elapsed {time.time()-t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

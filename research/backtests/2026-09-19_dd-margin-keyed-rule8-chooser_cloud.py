#!/usr/bin/env python3
"""
Idea 1440 (lane cloud, 2026-09-19) — does a DD-MARGIN-KEYED RULE-8 CHOOSER pick a DIFFERENT
BOOK than the ARGMAX-IS-SHARPE chooser, and does the disagreement pay OOS?

THE PREMISE (idea 1429, lane C, this morning).  A beta-keyed floor-and-cap band around the
frozen 2026-09-04 incumbent (U56, N=20, H=126, gross 0.75, weekly, 10 bps, t+1) widened that
book's ONLY binding 4b leg — the MaxDD margin — from +1.1028 pp to +1.83..+4.40 pp, with 4b
passing FULL AND OOS at 16 of 16 biting U56 cells.  And rule 8 declined it anyway: the
protocol's chooser is ARGMAX IN-SAMPLE SHARPE, the band trades CAGR for drawdown at roughly
FLAT Sharpe, so the argmax picked c = 0 — the anchor — on U56 and on B136.

So the question this run asks is not about the band.  It is about the CHOOSER.  PROTOCOL rule
8 fixes the WINDOW (parameters chosen on the first half, 2017-2026 read once) but says nothing
about the OBJECTIVE; the record has always used IS Sharpe.  Under rule 4b the thing that
decides capital is not Sharpe at all — it is the pair (MaxDD <= 0.60 x SPY, CAGR >= 0.70 x
SPY).  A chooser that maximises the quantity 4b actually binds on would pick differently.  Is
that a better chooser, or just a different way to lose?

THE TWO CHOOSERS, both reading the IDENTICAL IS window (warm-up .. 2016-12-31) and the
IDENTICAL 60-cell grid, both blind to 2017-2026 until the cell is locked:

  A  SHARPE-ARGMAX (the record's incumbent chooser, rule 8 as practised):
        argmax over cells of IS Sharpe.
  B  DD-MARGIN-KEYED (the queue's proposal):
        argmax over cells of the IS 4b DD MARGIN = MaxDD_IS - 0.60 x SPY MaxDD_IS,
        SUBJECT TO the IS 4b CAGR FLOOR  CAGR_IS >= 0.70 x SPY CAGR_IS.
        DOCUMENTED FALLBACK, pre-stated: if no cell clears the IS floor, keep the anchor c = 0.
  B' UNCONSTRAINED DD-MARGIN (diagnostic, NOT a candidate): B without the CAGR floor.  It is
     reported at every panel only to show whether the floor BINDS on B's pick; if B and B'
     agree, the constraint is decoration.

Tie-break for every chooser, pre-stated: smallest c, then smallest B (i.e. ties resolve
TOWARD the frozen anchor, never away from it).

CHOOSER STABILITY, measured INSIDE THE IS WINDOW ONLY (it reads no OOS row and so costs the
run nothing under rule 8): each chooser is re-run on the two halves of its own IS window
(warm-up..2013-06-30 and 2013-07-01..2016-12-31).  A chooser that picks a different cell in
each IS half is not selecting a book, it is selecting noise, and its OOS number is a draw
whichever way it lands.

THE GRID — idea 1429's OWN 60 cells, rebuilt here from the same mechanics:
    w_i = (G/n) * (1 + c * z_i),  z_i = 1 - 2*(rank_i - 0.5)/n by ASCENDING trailing beta to
    SPY over B days, G = 0.75, over the incumbent's OWN held names.  c = 0 IS the frozen
    incumbent.  Sum w = G exactly at every rebalance and for every (n, c).
  C  {0.00, 0.25, 0.50, 0.75, 1.00}   DIAL 1 — band half-width
  B  {20, 63, 126, 252}               DIAL 2 — trailing beta lookback (trading days)
20 cells per panel, 60 in all, EVERY ONE published in .grid.csv (PROTOCOL rule 4: two tuned
parameters, no more).  The CHOOSER is the object under study, not a third dial: both choosers
read the same 60 cells and neither adds a free parameter to the book.

WHAT IS READ ONCE.  2017-2026 is read after both choosers have locked their cells, and is
reported for BOTH picks, for the frozen anchor, for the live RULES v2 baseline and for SPY.
The disagreement is then priced by a PAIRED circular-block bootstrap (400 reps x 63-row
blocks, identical block starts) on the OOS Sharpe and OOS MaxDD difference B - A.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); both KEEP paths at
every cell, full sample and OOS; the halves; IS and OOS windows; turnover and its 10 bps drag.

COMPARANDS (rule 3): live RULES v2 at 10 bps weekly, SPY buy-and-hold, and the frozen (c = 0)
incumbent.

PROTOCOL: rule 1 (>= 10y); rule 2 (t+1, 10 bps, no leverage, no shorting); rule 3; rule 4
(both KEEP paths, 2 tuned parameters); rule 8 (walk-forward, 2017-2026 read ONCE); rule 9
(survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py NOT modified.

GATES.  G0 sample >= 10y.  G1 cross-script replay of the committed U56 anchor.  G2 the c = 0
cell is bit-identical across all four B.  G4 all 60 cells published.  G5 exactly two tuned
parameters.  G6 NEITHER chooser reads a row on or after 2017-01-01 (asserted numerically: the
IS slice's last timestamp is < 2017-01-01 and the chooser statistics are functions of that
slice alone).  G7 exposure channel shut (mean gross == the anchor's).  G7b every rebalance's
weight sum == G.  G7c no leverage.  G8 one selection frame per panel.  G11 the band is
respected exactly.  G10 bit-identical recompute of the U56 headline cell.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-19_dd-margin-keyed-rule8-chooser_cloud.py
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
SLUG = "dd-margin-keyed-rule8-chooser"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G = 20, 126, 0.75              # the frozen 2026-09-04 incumbent
COST, CADENCE = 10.0, "W"
CS = [0.00, 0.25, 0.50, 0.75, 1.00]        # DIAL 1 — band half-width
BS = [20, 63, 126, 252]                    # DIAL 2 — beta lookback (trading days)
OOS_START = "2017-01-01"
IS_SPLIT = "2013-07-01"          # IS-window midpoint, used ONLY for chooser stability
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BOOT_REPS, BOOT_BLOCK, SEED = 400, 63, 20260919
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
    """The live selection mechanics (the incumbent's 3-leg composite + MA gate + vol gate)."""
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = (q > q.rolling(200).mean()).values
    vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
    sc = (comp * (0.5 + 0.5 * above.astype(float))).values
    return sc, above, np.nan_to_num(vol20, nan=1e9)


def rolling_beta(R, y, B):
    """Trailing beta of every column of R to y over B TRAILING rows (backward-looking only)."""
    ey = y.rolling(B).mean()
    vy = (y * y).rolling(B).mean() - ey * ey
    ex = R.rolling(B).mean()
    exy = R.mul(y, axis=0).rolling(B).mean()
    cov = exy.sub(ex.mul(ey, axis=0))
    return cov.div(vy.replace(0.0, np.nan), axis=0).values


class Panel:
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
        R = px[invest].pct_change()
        y = px["SPY"].pct_change()
        self.beta = {B: rolling_beta(R, y, B) for B in BS}


def segments(pan, N, H, lag=1):
    """The frozen min-hold selection frame.  Depends on NEITHER dial, so it is built ONCE per
    panel and every cell holds the IDENTICAL names on the IDENTICAL rows (gate G8)."""
    T = pan.rets.shape[0]
    K = len(pan.iinv)
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    reb = pan.reb
    segs = []
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
        stop = reb[i + 1] if i + 1 < len(reb) else T
        segs.append((int(t), int(stop), int(ts), sel.copy()))
    return segs


def band_multiset(n, c):
    """Weight multiset for n names at band half-width c, CAP-FIRST.  Sums to G exactly."""
    if n == 0:
        return np.zeros(0)
    ranks = np.arange(1, n + 1, dtype=float)
    z = 1.0 - 2.0 * (ranks - 0.5) / n
    return (I_G / n) * (1.0 + c * z)


def cell_weights(pan, segs, c, B):
    """Per-segment weights over the segment's OWN held names.  LOWEST trailing beta takes the
    CAP side.  c = 0 is inert (equal weight = the frozen incumbent)."""
    BE = pan.beta[B]
    ws = []
    for (t, stop, ts, sel) in segs:
        n = len(sel)
        if n == 0:
            ws.append(np.zeros(0))
            continue
        m = band_multiset(n, c)
        if c == 0.0:
            order = np.arange(n)
        else:
            b = BE[ts, sel].astype(float)
            fin = np.isfinite(b)
            if not fin.all():
                med = np.nanmedian(b[fin]) if fin.any() else 1.0
                b = np.where(fin, b, med)
            order = np.argsort(b, kind="stable")
        w = np.empty(n)
        w[order] = m
        ws.append(w)
    return ws


def run_book(pan, segs, ws, C, Cp):
    """One book: weights applied at the segment's first row, drifting inside the segment."""
    rets = pan.rets
    T, M = rets.shape
    turn = np.zeros(T)
    out = np.zeros(T)
    gross_path = np.zeros(T)
    maxw = np.zeros(len(segs))
    minw = np.zeros(len(segs))
    wsum_dev = 0.0
    curw = np.zeros(M)
    wsum_max = 0.0
    for j, ((i0, i1, ts, sel), wv) in enumerate(zip(segs, ws)):
        w0 = np.zeros(M)
        if len(sel):
            w0[pan.iinv[sel]] = wv
            maxw[j] = float(wv.max())
            minw[j] = float(wv.min())
            wsum_dev = max(wsum_dev, abs(float(wv.sum()) - I_G))
        wsum_max = max(wsum_max, float(w0.sum()))
        turn[i0] = float(np.abs(w0 - curw).sum())
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        gross_path[i0:i1] = w0.sum()
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return out, turn, gross_path, maxw, minw, wsum_max, wsum_dev


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


def paired_block(a, b, stat="sharpe", reps=BOOT_REPS, L=BOOT_BLOCK, seed=SEED):
    """Paired circular-block bootstrap on a paired statistic (identical block starts)."""
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    nb = int(np.ceil(n / L))
    rng = np.random.default_rng(seed)
    starts = rng.integers(0, n, size=(reps, nb))
    idx = (starts[:, :, None] + np.arange(L)[None, None, :]).reshape(reps, nb * L)[:, :n] % n
    A, B_ = a[idx], b[idx]
    if stat == "sharpe":
        def f(X):
            v = X.std(axis=1, ddof=0) * np.sqrt(252)
            return np.where(v > 0, X.mean(axis=1) * 252 / v, np.nan)
        obs = float(sharpe(a) - sharpe(b))
    else:
        def f(X):
            e = np.cumprod(1 + X, axis=1)
            return (e / np.maximum.accumulate(e, axis=1) - 1).min(axis=1)
        obs = float(mdd(a) - mdd(b))
    d = f(A) - f(B_)
    se = float(np.nanstd(d, ddof=1))
    return obs, se, (obs / se if se > 0 else np.nan)


def pick(rows, key, feasible=None, label=""):
    """Chooser: argmax of `key` over `rows` (each a dict), restricted to `feasible` rows if
    given.  Tie-break pre-stated: smallest c, then smallest B (ties resolve TOWARD the
    anchor).  Returns (row, used_fallback)."""
    pool = [r for r in rows if (feasible is None or feasible(r))]
    fb = False
    if not pool:
        pool = [r for r in rows if r["c"] == 0.0]
        fb = True
    best = max(pool, key=lambda r: (round(key(r), 12), -r["c"], -r["B"]))
    return best, fb


def main():
    t0 = time.time()
    say("=" * 132)
    say("IDEA 1440 (lane cloud, 2026-09-19) — does a DD-MARGIN-KEYED RULE-8 CHOOSER pick a "
        "DIFFERENT BOOK than the ARGMAX-IS-SHARPE chooser?")
    say("GRID: idea 1429's OWN 60 cells — beta-keyed floor-and-cap w=(G/n)(1+c*z) on the "
        "frozen incumbent (U56 N=20 H=126 G=0.75 weekly 10bps t+1); c=0 IS the anchor.")
    say("CHOOSER A = argmax IS Sharpe (the record's).  CHOOSER B = argmax IS 4b DD MARGIN s.t. "
        "IS CAGR >= 0.70 x SPY IS CAGR; fallback c=0.  B' = B without the floor (diagnostic).")
    say("Tie-break for every chooser, pre-stated: smallest c, then smallest B (ties resolve "
        "TOWARD the frozen anchor).  IS = warm-up..2016-12-31;  2017-2026 READ ONCE.")
    say("=" * 132)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    say(f"  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0.")

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, "
        f"SMALL {len(inv)} (of {len(pxS.columns)-1} priced).")
    say("  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010, so every absolute level below is an UPPER BOUND "
        "and every 4b pass an optimistic one.  What this run reads is a CONTRAST between two "
        "CHOOSERS over the SAME 60 books on the SAME days, which the bias cannot manufacture — "
        "but the LEVEL at which either chooser's pick clears 4b is biased upward.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y);  {len(p.reb)} weekly rebalances")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)

    grid, ch_rows, dis_rows = [], [], []
    g2_dev = g7_dev = g7b_dev = g11_dev = 0.0
    wsum_global = 0.0
    headline_ret = None
    is_last_ts = []

    for pan in panels:
        T = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        i_is0, i_is1 = WARMUP, i_oos
        is_last_ts.append(pan.idx[i_is1 - 1])
        spy_f, spy_is, spy_o = (bmpack(pan.spy[WARMUP:]), bmpack(pan.spy[i_is0:i_is1]),
                                bmpack(pan.spy[i_oos:]))
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live_f, live_o = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])
        segs = segments(pan, I_N, I_H)
        C = np.cumprod(1.0 + pan.rets, axis=0)
        Cp = np.vstack([np.ones((1, pan.rets.shape[1])), C[:-1]])
        nsel = np.array([len(s[3]) for s in segs], float)

        say(f"\n  [{pan.name}]  SPY FULL CAGR {spy_f['CAGR']:.2%} Sharpe {spy_f['Sharpe']:.4f} "
            f"MaxDD {spy_f['MaxDD']:.2%}  |  4b bars FULL: DD cap {DD_CAP*spy_f['MaxDD']:.2%}, "
            f"CAGR floor {CAGR_FLOOR*spy_f['CAGR']:.2%}")
        say(f"           SPY IS   CAGR {spy_is['CAGR']:.2%} Sharpe {spy_is['Sharpe']:.4f} MaxDD "
            f"{spy_is['MaxDD']:.2%}  |  4b bars IS (what chooser B reads): DD cap "
            f"{DD_CAP*spy_is['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spy_is['CAGR']:.2%}")
        say(f"           SPY OOS  CAGR {spy_o['CAGR']:.2%} Sharpe {spy_o['Sharpe']:.4f} MaxDD "
            f"{spy_o['MaxDD']:.2%}  |  4b bars OOS: DD cap {DD_CAP*spy_o['MaxDD']:.2%}, CAGR "
            f"floor {CAGR_FLOOR*spy_o['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps FULL CAGR {live_f['CAGR']:.2%} Sharpe "
            f"{live_f['Sharpe']:.4f} MaxDD {live_f['MaxDD']:.2%} | OOS {live_o['CAGR']:.2%}/"
            f"{live_o['Sharpe']:.4f}/{live_o['MaxDD']:.2%}")

        # ---- the frozen anchor (c = 0) ---------------------------------------------------
        ws0 = cell_weights(pan, segs, 0.0, BS[0])
        g0, t0_, gp0, mw0, mn0, wsx, wdx = run_book(pan, segs, ws0, C, Cp)
        wsum_global = max(wsum_global, wsx)
        g7b_dev = max(g7b_dev, wdx)
        anchor = g0 - t0_ * COST / 1e4
        a_f, a_is, a_o = triple(anchor[WARMUP:]), triple(anchor[i_is0:i_is1]), triple(anchor[i_oos:])
        anchor_mg = float(np.mean(gp0[WARMUP:]))
        say(f"           FROZEN ANCHOR (c=0) FULL {a_f['CAGR']:.2%}/{a_f['Sharpe']:.4f}/"
            f"{a_f['MaxDD']:.2%} | IS {a_is['CAGR']:.2%}/{a_is['Sharpe']:.4f}/{a_is['MaxDD']:.2%} "
            f"| OOS {a_o['CAGR']:.2%}/{a_o['Sharpe']:.4f}/{a_o['MaxDD']:.2%}")
        if pan.name == "U56":
            d = max(abs(a_f["Sharpe"] - C_U56["Sharpe"]), abs(a_o["Sharpe"] - C_U56["oSharpe"]))
            gate("G1 cross-script replay of the committed 2026-09-04 U56 anchor "
                 "(15.80%/1.1537/-19.13% full; OOS Sharpe 1.1857)",
                 f"|dSharpe| {d:.2e} (got {a_f['CAGR']:.4f}/{a_f['Sharpe']:.4f}/"
                 f"{a_f['MaxDD']:.4f}; OOS {a_o['Sharpe']:.4f})", "< 5e-3", d < 5e-3)

        # ---- the 20-cell grid --------------------------------------------------------------
        cells = []
        for c in CS:
            for B in BS:
                ws = cell_weights(pan, segs, c, B)
                gg, tu, gp, mw, mn, wsx, wdx = run_book(pan, segs, ws, C, Cp)
                wsum_global = max(wsum_global, wsx)
                g7b_dev = max(g7b_dev, wdx)
                rr = gg - tu * COST / 1e4
                if c == 0.0:
                    g2_dev = max(g2_dev, float(np.max(np.abs(rr - anchor))))
                g7_dev = max(g7_dev, abs(float(np.mean(gp[WARMUP:])) - anchor_mg))
                cap_t = np.where(nsel > 0, (I_G / np.maximum(nsel, 1)) * (1 + c * (1 - 1 / np.maximum(nsel, 1))), 0.0)
                flo_t = np.where(nsel > 0, (I_G / np.maximum(nsel, 1)) * (1 - c * (1 - 1 / np.maximum(nsel, 1))), 0.0)
                g11_dev = max(g11_dev, float(np.max(np.abs(mw - cap_t))), float(np.max(np.abs(mn - flo_t))))

                k4a, k4b, m, h1, h2, legs = keep_paths(rr[WARMUP:], spy_f, live_f)
                k4aO, k4bO, mo, oh1, oh2, legsO = keep_paths(rr[i_oos:], spy_o, live_o)
                mi = triple(rr[i_is0:i_is1])
                is_dd_margin = 100 * (mi["MaxDD"] - DD_CAP * spy_is["MaxDD"])
                is_cagr_margin = 100 * (mi["CAGR"] - CAGR_FLOOR * spy_is["CAGR"])
                n = T - WARMUP
                turn_y = float(np.sum(tu[WARMUP:]) * 252.0 / n)
                row = dict(
                    panel=pan.name, c=c, B=B,
                    CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                    isCAGR=mi["CAGR"], isSharpe=mi["Sharpe"], isMaxDD=mi["MaxDD"],
                    is_dd_margin_pp=is_dd_margin, is_cagr_margin_pp=is_cagr_margin,
                    is_cagr_floor_ok=bool(mi["CAGR"] >= CAGR_FLOOR * spy_is["CAGR"]),
                    oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                    oH1=oh1, oH2=oh2,
                    keep4a=k4a, keep4b=k4b, keep4a_oos=k4aO, keep4b_oos=k4bO,
                    legH1=legs["H1"], legH2=legs["H2"], legDD=legs["DD"], legCAGR=legs["CAGR"],
                    oleg_H1=legsO["H1"], oleg_H2=legsO["H2"], oleg_DD=legsO["DD"],
                    oleg_CAGR=legsO["CAGR"],
                    dd_margin_pp=100 * (m["MaxDD"] - DD_CAP * spy_f["MaxDD"]),
                    cagr_margin_pp=100 * (m["CAGR"] - CAGR_FLOOR * spy_f["CAGR"]),
                    oos_dd_margin_pp=100 * (mo["MaxDD"] - DD_CAP * spy_o["MaxDD"]),
                    oos_cagr_margin_pp=100 * (mo["CAGR"] - CAGR_FLOOR * spy_o["CAGR"]),
                    d_sharpe_vs_anchor=m["Sharpe"] - a_f["Sharpe"],
                    d_cagr_pp_vs_anchor=100 * (m["CAGR"] - a_f["CAGR"]),
                    d_maxdd_pp_vs_anchor=100 * (m["MaxDD"] - a_f["MaxDD"]),
                    mean_gross=float(np.mean(gp[WARMUP:])),
                    max_w=float(mw.mean()), min_w=float(mn.mean()),
                    turn_y=turn_y, drag_bpyr=turn_y * COST,
                    spy_CAGR=spy_f["CAGR"], spy_Sharpe=spy_f["Sharpe"], spy_MaxDD=spy_f["MaxDD"],
                    spy_oCAGR=spy_o["CAGR"], spy_oSharpe=spy_o["Sharpe"], spy_oMaxDD=spy_o["MaxDD"],
                    live_Sharpe=live_f["Sharpe"], live_MaxDD=live_f["MaxDD"],
                    live_oSharpe=live_o["Sharpe"], live_oMaxDD=live_o["MaxDD"],
                    anchor_CAGR=a_f["CAGR"], anchor_Sharpe=a_f["Sharpe"], anchor_MaxDD=a_f["MaxDD"],
                    anchor_oCAGR=a_o["CAGR"], anchor_oSharpe=a_o["Sharpe"], anchor_oMaxDD=a_o["MaxDD"],
                    anchor_dd_margin_pp=100 * (a_f["MaxDD"] - DD_CAP * spy_f["MaxDD"]))
                grid.append(row)
                cells.append(dict(row, ret=rr))
                if pan.name == "U56" and c == 0.50 and B == 126:
                    headline_ret = rr.copy()

        # ---- THE TWO CHOOSERS (both read the IS slice only) --------------------------------
        A, fbA = pick(cells, lambda r: r["isSharpe"])
        Bc, fbB = pick(cells, lambda r: r["is_dd_margin_pp"],
                       feasible=lambda r: r["is_cagr_floor_ok"])
        Bp, fbBp = pick(cells, lambda r: r["is_dd_margin_pp"])
        nfeas = sum(1 for r in cells if r["is_cagr_floor_ok"])

        say(f"\n    CHOOSER A (argmax IS Sharpe)                   -> c={A['c']:.2f} B={A['B']:3d}"
            f"  IS Sharpe {A['isSharpe']:.4f}  IS DD margin {A['is_dd_margin_pp']:+.4f} pp")
        say(f"    CHOOSER B (argmax IS DD margin | IS CAGR floor) -> c={Bc['c']:.2f} "
            f"B={Bc['B']:3d}  IS Sharpe {Bc['isSharpe']:.4f}  IS DD margin "
            f"{Bc['is_dd_margin_pp']:+.4f} pp   [feasible cells {nfeas}/20, fallback used: {fbB}]")
        say(f"    CHOOSER B' (unconstrained, diagnostic)          -> c={Bp['c']:.2f} "
            f"B={Bp['B']:3d}  IS DD margin {Bp['is_dd_margin_pp']:+.4f} pp   "
            f"[floor BINDS on B: {Bp['c'] != Bc['c'] or Bp['B'] != Bc['B']}]")

        # ---- CHOOSER STABILITY inside the IS window (reads no OOS row) --------------------
        i_mid = int(np.searchsorted(pan.idx.values, np.datetime64(IS_SPLIT)))
        stab = {}
        for half, (lo, hi) in (("IS1", (i_is0, i_mid)), ("IS2", (i_mid, i_is1))):
            sub = []
            spy_h = bmpack(pan.spy[lo:hi])
            for cc in cells:
                mh = triple(cc["ret"][lo:hi])
                sub.append(dict(c=cc["c"], B=cc["B"],
                                isSharpe=sharpe(cc["ret"][lo:hi]),
                                is_dd_margin_pp=100 * (mh["MaxDD"] - DD_CAP * spy_h["MaxDD"]),
                                is_cagr_floor_ok=bool(mh["CAGR"] >= CAGR_FLOOR * spy_h["CAGR"])))
            a_h, _ = pick(sub, lambda r: r["isSharpe"])
            b_h, fb_h = pick(sub, lambda r: r["is_dd_margin_pp"],
                             feasible=lambda r: r["is_cagr_floor_ok"])
            stab[half] = ((a_h["c"], a_h["B"]), (b_h["c"], b_h["B"]), fb_h)
        say(f"    CHOOSER STABILITY inside IS (no OOS row read): A picks {stab['IS1'][0]} on "
            f"IS-half-1 and {stab['IS2'][0]} on IS-half-2 (stable: "
            f"{stab['IS1'][0] == stab['IS2'][0]});  B picks {stab['IS1'][1]} and "
            f"{stab['IS2'][1]} (stable: {stab['IS1'][1] == stab['IS2'][1]}).")

        rA, rB = A["ret"], Bc["ret"]
        dsh, se_, t_ = paired_block(rB[i_oos:], rA[i_oos:], "sharpe")
        ddd, ddse, ddt = paired_block(rB[i_oos:], rA[i_oos:], "mdd")
        dshA, _, tAa = paired_block(rA[i_oos:], anchor[i_oos:], "sharpe")
        dshB, _, tBa = paired_block(rB[i_oos:], anchor[i_oos:], "sharpe")
        disagree = bool(A["c"] != Bc["c"] or A["B"] != Bc["B"])

        for lab, r, fb in (("A_sharpe_argmax", A, fbA), ("B_dd_margin", Bc, fbB),
                           ("Bprime_dd_margin_nofloor", Bp, fbBp)):
            ch_rows.append(dict(panel=pan.name, chooser=lab, c=r["c"], B=r["B"],
                                fallback_used=fb,
                                isSharpe=r["isSharpe"], isCAGR=r["isCAGR"], isMaxDD=r["isMaxDD"],
                                is_dd_margin_pp=r["is_dd_margin_pp"],
                                is_cagr_margin_pp=r["is_cagr_margin_pp"],
                                oCAGR=r["oCAGR"], oSharpe=r["oSharpe"], oMaxDD=r["oMaxDD"],
                                keep4b_oos=r["keep4b_oos"], keep4a_oos=r["keep4a_oos"],
                                oleg_H1=r["oleg_H1"], oleg_H2=r["oleg_H2"],
                                oleg_DD=r["oleg_DD"], oleg_CAGR=r["oleg_CAGR"],
                                oos_dd_margin_pp=r["oos_dd_margin_pp"],
                                oos_cagr_margin_pp=r["oos_cagr_margin_pp"],
                                full_CAGR=r["CAGR"], full_Sharpe=r["Sharpe"],
                                full_MaxDD=r["MaxDD"], keep4b=r["keep4b"], keep4a=r["keep4a"],
                                anchor_oCAGR=a_o["CAGR"], anchor_oSharpe=a_o["Sharpe"],
                                anchor_oMaxDD=a_o["MaxDD"],
                                spy_oCAGR=spy_o["CAGR"], spy_oSharpe=spy_o["Sharpe"],
                                spy_oMaxDD=spy_o["MaxDD"],
                                live_oSharpe=live_o["Sharpe"], live_oMaxDD=live_o["MaxDD"]))

        dis_rows.append(dict(panel=pan.name, disagree=disagree,
                             A_IS1=str(stab["IS1"][0]), A_IS2=str(stab["IS2"][0]),
                             A_is_stable=bool(stab["IS1"][0] == stab["IS2"][0]),
                             B_IS1=str(stab["IS1"][1]), B_IS2=str(stab["IS2"][1]),
                             B_is_stable=bool(stab["IS1"][1] == stab["IS2"][1]),
                             A_c=A["c"], A_B=A["B"], B_c=Bc["c"], B_B=Bc["B"],
                             n_feasible_IS=nfeas,
                             d_oCAGR_pp=100 * (Bc["oCAGR"] - A["oCAGR"]),
                             d_oSharpe=Bc["oSharpe"] - A["oSharpe"], t_oSharpe=t_,
                             d_oMaxDD_pp=100 * ddd, t_oMaxDD=ddt,
                             d_oos_dd_margin_pp=Bc["oos_dd_margin_pp"] - A["oos_dd_margin_pp"],
                             A_keep4b_oos=A["keep4b_oos"], B_keep4b_oos=Bc["keep4b_oos"],
                             A_d_oSharpe_vs_anchor=dshA, A_t_vs_anchor=tAa,
                             B_d_oSharpe_vs_anchor=dshB, B_t_vs_anchor=tBa))

    G = pd.DataFrame(grid)
    CH = pd.DataFrame(ch_rows)
    D = pd.DataFrame(dis_rows)

    gate("G2 c=0 cell BIT-IDENTICAL across all four B", f"max |dret| {g2_dev:.3e}", "< 1e-15",
         g2_dev < 1e-15)
    gate("G4 all 60 grid cells published", len(G), "== 60", len(G) == 60)
    gate("G5 exactly two tuned parameters (c, B); the chooser is the object under study, not a "
         "third dial", "2", "== 2", True)
    gate("G6 NEITHER chooser reads a row on or after 2017-01-01",
         "IS last rows " + ", ".join(str(x.date()) for x in is_last_ts),
         "all < 2017-01-01", all(x < pd.Timestamp(OOS_START) for x in is_last_ts))
    gate("G7 exposure channel SHUT: every cell's realised mean gross == the anchor's",
         f"max |dmean gross| {g7_dev:.3e}", "< 1e-12", g7_dev < 1e-12)
    gate("G7b sum-zero identity: every rebalance's weight sum == G = 0.75",
         f"max |dsum| {g7b_dev:.3e}", "< 1e-12", g7b_dev < 1e-12)
    gate("G7c no leverage: realised weight sum never exceeds 1.0", f"max wsum {wsum_global:.6f}",
         "<= 1.0 + 1e-12", wsum_global <= 1.0 + 1e-12)
    gate("G8 selection untouched: ONE frame per panel, built before any dial", "by construction",
         "identical name sets", True)
    gate("G11 the band is respected exactly: realised max/min weight == the analytic cap/floor",
         f"max |dev| {g11_dev:.3e}", "< 1e-12", g11_dev < 1e-12)

    say("\n" + "=" * 132)
    say("GRID — EVERY CELL.  IS = warm-up..2016-12-31 (all a chooser may read).  "
        "OOS = 2017-01-01.. (read ONCE, after both choosers locked).")
    say("=" * 132)
    for pn in ["U56", "B136", "SMALL"]:
        sub = G[G.panel == pn]
        say(f"\n  [{pn}]  anchor FULL DD margin {sub.anchor_dd_margin_pp.iloc[0]:+.4f} pp")
        say("      c    B |   IS CAGR  IS Sh   IS DD | IS DDmarg IS CAGRmarg flr | FULL CAGR  "
            "Sharpe   MaxDD     H1     H2 | 4a 4b | OOS CAGR  Sharpe   MaxDD | o4a o4b | "
            "OOS DDmarg CAGRmarg | turn drag")
        for _, r in sub.iterrows():
            say(f"    {r.c:4.2f} {int(r.B):4d} | {r.isCAGR:8.2%} {r.isSharpe:6.4f} "
                f"{r.isMaxDD:7.2%} | {r.is_dd_margin_pp:+9.3f} {r.is_cagr_margin_pp:+10.3f} "
                f"{int(r.is_cagr_floor_ok)} | {r.CAGR:9.2%} {r.Sharpe:7.4f} {r.MaxDD:7.2%} "
                f"{r.H1:6.3f} {r.H2:6.3f} | {int(r.keep4a)}  {int(r.keep4b)} | {r.oCAGR:8.2%} "
                f"{r.oSharpe:7.4f} {r.oMaxDD:7.2%} | {int(r.keep4a_oos)}   {int(r.keep4b_oos)} | "
                f"{r.oos_dd_margin_pp:+9.3f} {r.oos_cagr_margin_pp:+8.3f} | {r.turn_y:4.2f} "
                f"{r.drag_bpyr:5.1f}")

    say("\n" + "=" * 132)
    say("THE TWO CHOOSERS — 2017-2026 READ ONCE, for both picks, the frozen anchor, the live "
        "RULES v2 baseline and SPY.")
    say("=" * 132)
    say("  panel | chooser                  | pick (c,B) fb | IS Sh  IS DDmarg | OOS CAGR  "
        "Sharpe   MaxDD | o4a o4b legs H1/H2/DD/CAGR | OOS DDmarg CAGRmarg | ANCHOR OOS | SPY "
        "OOS | RULESv2 OOS Sh/DD")
    for _, r in CH.iterrows():
        say(f"  {r.panel:>5} | {r.chooser:24} | ({r.c:4.2f},{int(r.B):4d}) {int(r.fallback_used)} "
            f"| {r.isSharpe:6.4f} {r.is_dd_margin_pp:+9.3f} | {r.oCAGR:8.2%} {r.oSharpe:7.4f} "
            f"{r.oMaxDD:7.2%} | {int(r.keep4a_oos)}   {int(r.keep4b_oos)}  "
            f"{int(r.oleg_H1)}/{int(r.oleg_H2)}/{int(r.oleg_DD)}/{int(r.oleg_CAGR)} | "
            f"{r.oos_dd_margin_pp:+9.3f} {r.oos_cagr_margin_pp:+8.3f} | {r.anchor_oCAGR:6.2%}/"
            f"{r.anchor_oSharpe:.4f}/{r.anchor_oMaxDD:7.2%} | {r.spy_oCAGR:6.2%}/"
            f"{r.spy_oSharpe:.4f}/{r.spy_oMaxDD:7.2%} | {r.live_oSharpe:.4f}/{r.live_oMaxDD:7.2%}")

    say("\n" + "=" * 132)
    say("DO THE TWO CHOOSERS DISAGREE, AND BY HOW MUCH OOS?  (B - A, paired 63-day block "
        "bootstrap, 400 reps, identical block starts)")
    say("=" * 132)
    say("  panel | disagree | A (c,B)      B (c,B)  | IS feasible | dOOS CAGR pp | dOOS Sharpe "
        "(t) | dOOS MaxDD pp (t) | dOOS DD margin pp | 4b OOS A -> B")
    for _, r in D.iterrows():
        say(f"  {r.panel:>5} |   {str(bool(r.disagree)):5}  | ({r.A_c:4.2f},{int(r.A_B):4d})  "
            f"({r.B_c:4.2f},{int(r.B_B):4d}) |   {int(r.n_feasible_IS):2d}/20     | "
            f"{r.d_oCAGR_pp:+12.4f} | {r.d_oSharpe:+9.4f} ({r.t_oSharpe:+5.2f}) | "
            f"{r.d_oMaxDD_pp:+10.4f} ({r.t_oMaxDD:+5.2f}) | {r.d_oos_dd_margin_pp:+17.4f} | "
            f"{int(r.A_keep4b_oos)} -> {int(r.B_keep4b_oos)}")

    say("\n  KEEP paths over all 60 cells: 4a FULL " + f"{int(G.keep4a.sum())} of {len(G)}; "
        f"4b FULL {int(G.keep4b.sum())} of {len(G)}; 4a OOS {int(G.keep4a_oos.sum())}; "
        f"4b OOS {int(G.keep4b_oos.sum())}; 4b FULL and OOS "
        f"{int((G.keep4b & G.keep4b_oos).sum())}.")
    say(f"  CHOOSER STABILITY inside the IS window: chooser A picks the SAME cell in both IS "
        f"halves on {int(D.A_is_stable.sum())} of 3 panels, chooser B on "
        f"{int(D.B_is_stable.sum())} of 3.")
    nd = int(D.disagree.sum())
    say(f"  THE ANSWER TO THE QUEUE'S QUESTION: the two choosers disagree on {nd} of 3 panels.")
    if nd:
        sub = D[D.disagree]
        say(f"    where they disagree, chooser B costs {sub.d_oCAGR_pp.min():+.4f} .. "
            f"{sub.d_oCAGR_pp.max():+.4f} pp of OOS CAGR and moves OOS Sharpe "
            f"{sub.d_oSharpe.min():+.4f} .. {sub.d_oSharpe.max():+.4f} "
            f"(|t| max {sub.t_oSharpe.abs().max():.2f}) and OOS MaxDD "
            f"{sub.d_oMaxDD_pp.min():+.4f} .. {sub.d_oMaxDD_pp.max():+.4f} pp "
            f"(|t| max {sub.t_oMaxDD.abs().max():.2f}).")
    say(f"  4b OOS: chooser A passes on "
        f"{int(CH[CH.chooser=='A_sharpe_argmax'].keep4b_oos.sum())} of 3 panels, chooser B on "
        f"{int(CH[CH.chooser=='B_dd_margin'].keep4b_oos.sum())} of 3.")

    # G10 bit-identical recompute of the U56 headline cell
    pan = panels[0]
    segs = segments(pan, I_N, I_H)
    C = np.cumprod(1.0 + pan.rets, axis=0)
    Cp = np.vstack([np.ones((1, pan.rets.shape[1])), C[:-1]])
    gg, tu, _, _, _, _, _ = run_book(pan, segs, cell_weights(pan, segs, 0.50, 126), C, Cp)
    rr = gg - tu * COST / 1e4
    d10 = float(np.max(np.abs(rr - headline_ret)))
    gate("G10 bit-identical recompute (U56, c=0.50, B=126)", f"max |dret| {d10:.3e}", "< 1e-15",
         d10 < 1e-15)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    CH.to_csv(f"{OUT}.choosers.csv", index=False)
    D.to_csv(f"{OUT}.disagreement.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n  wrote {OUT.name}.grid.csv / .choosers.csv / .disagreement.csv / .gates.csv / "
        f".log.txt")
    say(f"  ALL GATES PASS: {all(g['pass_'] for g in GATES)}   ({time.time()-t0:.1f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

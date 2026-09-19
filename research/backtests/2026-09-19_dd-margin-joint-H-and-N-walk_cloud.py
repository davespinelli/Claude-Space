#!/usr/bin/env python3
"""
Idea 1415 (lane cloud, 2026-09-19 run 2, idea 1 of 2) — is the incumbent's 4b DD MARGIN an
H-and-N CONVENTION TOO?

THE PREMISE.  The standing 2026-09-04 KEEP-4b incumbent (U56, N = 20, H = 126, gross 0.75,
weekly Fri-decide / Mon-trade, 10 bps, t+1, composite legs (21,252)+(0,126)+(0,63), MA gate,
vol20 < 0.60) passes 4b on ONE leg's margin: MaxDD -19.13% against a -20.23% cap, i.e. +1.1028 pp.
This morning idea 1409 showed that margin spans 5.3173 pp across the 12-1 leg's (skip, long)
convention — a dial frozen by fiat on 2026-09-04 and never walked.  H = 126 and N = 20 were
frozen by the SAME fiat.  They have never been walked JOINTLY against the DD margin.  If their
joint spread is comparable to 5.3173 pp, the committed pass is a CELL, not a strategy.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  N  {10, 12, 15, 20, 25, 30, 40}     DIAL 1 — book width (how many names are held)
  H  {0, 21, 42, 63, 126, 252}        DIAL 2 — the minimum hold in trading days.  H = 0 is the
                                               convention-free book (re-rank every week, no
                                               stickiness); H = 126 is the frozen incumbent.

42 cells per panel, 126 in all, EVERY ONE published in .grid.csv.  The incumbent (20, 126) is
present in the grid and is the anchor every cell is scored against.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); both KEEP paths at every
cell; the halves; IS and OOS windows; the DD margin in pp; the CAGR margin in pp; turnover and
its 10 bps drag in bp/yr; realised mean gross.  GROSS IS HELD FIXED at the incumbent's 0.75 — it
is not walked here, precisely so that the (H, N) spread this run reads cannot be a gross effect.

WHAT WOULD MAKE THIS A FINDING RATHER THAN A LADDER.  A spread alone is not evidence: any grid
has one.  Two things decide the verdict.  (i) The SIZE of the joint (H, N) DD-margin spread
against 1409's committed (skip, long) spread of 5.3173 pp and against the anchor's own +1.1028 pp
margin — if the margin moves by more than it is, the pass is a cell.  (ii) RESOLUTION: every
cell's Sharpe and MaxDD gap against the frozen anchor is scored by a PAIRED circular-block
bootstrap (400 reps x 63-row blocks, seed 20260919, identical block starts for both books), so a
gap inside its own SE is published as UNRESOLVED, not as a finding.  |t| > 2 is the record's bar.

COMPARANDS (rule 3): the live RULES v2 baseline at 10 bps weekly, SPY buy-and-hold, and the
FROZEN incumbent cell (N = 20, H = 126).

PROTOCOL: rule 1 (>= 10y); rule 2 (t+1, 10 bps, no leverage, no shorting); rule 3 (RULES v2 AND
SPY); rule 4 (both KEEP paths, exactly 2 tuned parameters); rule 8 (walk-forward: (N, H) chosen
on warm-up..2016-12-31 by argmax IS Sharpe, 2017-2026 read ONCE, scored against the frozen
incumbent); rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py
are NOT modified.

GATES.  G1 CROSS-SCRIPT REPLAY: the (N=20, H=126) U56 cell must reproduce the committed anchor
(15.80% / 1.1537 / -19.13% full; 17.32% / 1.1857 / -19.13% OOS) to < 5e-3 of Sharpe.  G2 all 126
cells published.  G3 exactly two tuned parameters.  G4 the rule-8 chooser reads no row on or
after 2017-01-01.  G5 no leverage: realised weight sum never exceeds 1.0.  G6 the H = 0 column
holds exactly N names at every rebalance where N are eligible (the min-hold is inert).  G7
bit-identical recompute of the anchor cell.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-19_dd-margin-joint-H-and-N-walk_cloud.py
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
SLUG = "dd-margin-joint-H-and-N-walk"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G = 20, 126, 0.75             # the frozen 2026-09-04 incumbent
COST, CADENCE = 10.0, "W"
NS = [10, 12, 15, 20, 25, 30, 40]
HS = [0, 21, 42, 63, 126, 252]
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BOOT_REPS, BOOT_BLOCK, BOOT_SEED = 400, 63, 20260919
C_U56 = dict(CAGR=0.1580, Sharpe=1.1537, MaxDD=-0.1913, oSharpe=1.1857, oCAGR=0.1732)
SKIP_LONG_SPREAD_PP = 5.3173             # idea 1409's committed (skip, long) DD-margin spread
ANCHOR_MARGIN_PP = 1.1028                # the committed U56 DD margin

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


def build1(pan, N, H, lag=1):
    """The min-hold selection frame at GROSS = 1.0 (rows sum to 1 when anything is held).
    H = 0 means no stickiness at all: every rebalance re-ranks from scratch."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    reb = pan.reb
    nsel = []
    for i, t in enumerate(reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if (len(held) and H > 0) else held[:0]
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
        nsel.append(len(sel))
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W, np.array(nsel)


def run_book(pan, frame, C, Cp, g):
    """One book at constant gross g.  Returns gross-of-cost daily returns and per-row turnover."""
    rets = pan.rets
    T, M = rets.shape
    turn = np.zeros(T)
    out = np.zeros(T)
    curw = np.zeros(M)
    reb = pan.reb
    ends = np.append(reb[1:], T)
    wsum_max = 0.0
    for i0, i1 in zip(reb, ends):
        w0 = g * frame[i0]
        wsum_max = max(wsum_max, float(w0.sum()))
        turn[i0] = float(np.abs(w0 - curw).sum())
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return out, turn, wsum_max


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


def _boot_idx(n, reps=BOOT_REPS, L=BOOT_BLOCK, seed=BOOT_SEED):
    nb = int(np.ceil(n / L))
    rng = np.random.default_rng(seed)
    starts = rng.integers(0, n, size=(reps, nb))
    return (starts[:, :, None] + np.arange(L)[None, None, :]).reshape(reps, nb * L)[:, :n] % n


def paired_block(a, b, idx):
    """Paired circular-block bootstrap SE for dSharpe and dMaxDD (identical block starts)."""
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    n = min(len(a), len(b))
    a, b, I = a[:n], b[:n], idx[:, :n]
    A, B = a[I], b[I]

    def sh(X):
        v = X.std(axis=1, ddof=0) * np.sqrt(252)
        return np.where(v > 0, X.mean(axis=1) * 252 / v, np.nan)

    def dd(X):
        E = np.cumprod(1 + X, axis=1)
        return (E / np.maximum.accumulate(E, axis=1) - 1).min(axis=1)

    ds = sh(A) - sh(B)
    dm = dd(A) - dd(B)
    o_s = float(sharpe(a) - sharpe(b))
    o_m = float(mdd(a) - mdd(b))
    se_s = float(np.nanstd(ds, ddof=1))
    se_m = float(np.nanstd(dm, ddof=1))
    return (o_s, se_s, o_s / se_s if se_s > 0 else np.nan,
            o_m, se_m, o_m / se_m if se_m > 0 else np.nan)


def main():
    t0 = time.time()
    say("=" * 128)
    say("IDEA 1415 (lane cloud, 2026-09-19 run 2, idea 1 of 2) — is the incumbent's 4b DD MARGIN "
        "an H-and-N CONVENTION TOO?")
    say("DIALS: N {10,12,15,20,25,30,40} x H {0,21,42,63,126,252} at the frozen incumbent's gross "
        "0.75, MAXVOL 0.60, MA gate ON, weekly, 10 bps, t+1, legs (21,252)+(0,126)+(0,63).")
    say("GROSS IS NOT WALKED: held at 0.75 so the (H, N) spread read here cannot be a gross effect.")
    say("BAR: idea 1409's committed (skip, long) DD-margin spread is 5.3173 pp; the anchor's own "
        f"committed margin is +{ANCHOR_MARGIN_PP:.4f} pp.")
    say("=" * 128)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    say(f"  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0.")
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, "
        f"SMALL {len(inv)} (of {len(pxS.columns)-1} priced).")
    say("  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010, so every absolute level below is an UPPER BOUND "
        "and every 4b pass an optimistic one.  What this run reads is a CONTRAST between (H, N) "
        "cells built on the SAME names and the SAME days, which the bias does not manufacture.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y);  {len(p.reb)} weekly rebalances")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)

    grid, wf_rows = [], []
    wsum_global = 0.0
    g6_bad = 0

    for pan in panels:
        T = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        spy, spyO = bmpack(pan.spy[WARMUP:]), bmpack(pan.spy[i_oos:])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])
        C = np.cumprod(1.0 + pan.rets, axis=0)
        Cp = np.vstack([np.ones((1, pan.rets.shape[1])), C[:-1]])
        bidx_full = _boot_idx(T - WARMUP)
        bidx_oos = _boot_idx(T - i_oos)

        say(f"\n  [{pan.name}]  SPY  CAGR {spy['CAGR']:.2%} Sharpe {spy['Sharpe']:.4f} MaxDD "
            f"{spy['MaxDD']:.2%} H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f}  |  4b bars: DD cap "
            f"{DD_CAP*spy['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps  CAGR {live['CAGR']:.2%} Sharpe {live['Sharpe']:.4f} "
            f"MaxDD {live['MaxDD']:.2%} H1/H2 {live['H1']:.3f}/{live['H2']:.3f}")

        # ---- every (N, H) cell -----------------------------------------------------------
        store, meta = {}, {}
        for N in NS:
            for H in HS:
                frame, nsel = build1(pan, N, H)
                gg, tu, ws = run_book(pan, frame, C, Cp, I_G)
                wsum_global = max(wsum_global, ws)
                rr = gg - tu * COST / 1e4
                store[(N, H)] = rr
                meta[(N, H)] = (nsel, tu)
                if H == 0:
                    # min-hold inert: the book must hold min(N, #eligible-and-priced) names
                    cap = np.array([min(N, int((pan.elig[max(t-1, 0)]
                                                 & pan.priced[max(t-1, 0)][pan.iinv]
                                                 & np.isfinite(pan.rank_key[max(t-1, 0)])).sum()))
                                    for t in pan.reb])
                    g6_bad += int(np.sum(nsel != cap))
        anchor = store[(I_N, I_H)]
        am, ao = triple(anchor[WARMUP:]), triple(anchor[i_oos:])
        ah1, ah2 = halves(anchor[WARMUP:])
        say(f"           FROZEN INCUMBENT (N=20,H=126) CAGR {am['CAGR']:.2%} Sharpe "
            f"{am['Sharpe']:.4f} MaxDD {am['MaxDD']:.2%} H1/H2 {ah1:.4f}/{ah2:.4f} | OOS "
            f"{ao['CAGR']:.2%}/{ao['Sharpe']:.4f}/{ao['MaxDD']:.2%}")
        if pan.name == "U56":
            d = max(abs(am["Sharpe"] - C_U56["Sharpe"]), abs(ao["Sharpe"] - C_U56["oSharpe"]))
            gate("G1 cross-script replay of the committed 2026-09-04 U56 anchor "
                 "(15.80%/1.1537/-19.13% full; 17.32%/1.1857/-19.13% OOS)",
                 f"|dSharpe| {d:.2e}  (got {am['CAGR']:.4f}/{am['Sharpe']:.4f}/{am['MaxDD']:.4f}; "
                 f"OOS {ao['CAGR']:.4f}/{ao['Sharpe']:.4f})",
                 "< 5e-3", d < 5e-3)

        for N in NS:
            for H in HS:
                rr = store[(N, H)]
                nsel, tu = meta[(N, H)]
                k4a, k4b, m, h1, h2, legs = keep_paths(rr[WARMUP:], spy, live)
                k4aO, k4bO, mo, oh1, oh2, legsO = keep_paths(rr[i_oos:], spyO, liveO)
                ds, ses, ts, dm_, sem, tm_ = paired_block(rr[WARMUP:], anchor[WARMUP:], bidx_full)
                dsO, sesO, tsO, dmO, semO, tmO = paired_block(rr[i_oos:], anchor[i_oos:], bidx_oos)
                n = T - WARMUP
                turn_y = float(np.sum(tu[WARMUP:]) * 252.0 / n)
                grid.append(dict(
                    panel=pan.name, N=N, H=H, is_anchor=bool(N == I_N and H == I_H),
                    CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                    oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                    keep4a=k4a, keep4b=k4b, keep4b_oos=k4bO, keep4a_oos=k4aO,
                    legH1=legs["H1"], legH2=legs["H2"], legDD=legs["DD"], legCAGR=legs["CAGR"],
                    dd_margin_pp=100 * (m["MaxDD"] - DD_CAP * spy["MaxDD"]),
                    cagr_margin_pp=100 * (m["CAGR"] - CAGR_FLOOR * spy["CAGR"]),
                    odd_margin_pp=100 * (mo["MaxDD"] - DD_CAP * spyO["MaxDD"]),
                    mean_names=float(np.mean(nsel)), turn_y=turn_y, drag_bpyr=turn_y * COST,
                    d_sharpe_vs_anchor=ds, se_sharpe=ses, t_sharpe=ts,
                    d_maxdd_vs_anchor_pp=100 * dm_, se_maxdd_pp=100 * sem, t_maxdd=tm_,
                    od_sharpe_vs_anchor=dsO, ose_sharpe=sesO, ot_sharpe=tsO,
                    od_maxdd_vs_anchor_pp=100 * dmO, ot_maxdd=tmO,
                    spy_CAGR=spy["CAGR"], spy_Sharpe=spy["Sharpe"], spy_MaxDD=spy["MaxDD"],
                    live_Sharpe=live["Sharpe"], live_MaxDD=live["MaxDD"],
                    spy_oCAGR=spyO["CAGR"], spy_oSharpe=spyO["Sharpe"], spy_oMaxDD=spyO["MaxDD"]))

        # ---- rule 8 ----------------------------------------------------------------------
        i_is0, i_is1 = WARMUP, i_oos
        best, bs = None, -np.inf
        for N in NS:
            for H in HS:
                s = sharpe(store[(N, H)][i_is0:i_is1])
                if s > bs:
                    bs, best = s, (N, H)
        rr = store[best]
        k4aO, k4bO, mo, _, _, legsO = keep_paths(rr[i_oos:], spyO, liveO)
        aO = triple(anchor[i_oos:])
        dsO, sesO, tsO, dmO, semO, tmO = paired_block(rr[i_oos:], anchor[i_oos:], bidx_oos)
        wf_rows.append(dict(panel=pan.name, is_N=best[0], is_H=best[1], is_Sharpe=bs,
                            picked_anchor=bool(best == (I_N, I_H)),
                            oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                            keep4b_oos=k4bO, keep4a_oos=k4aO,
                            anchor_oCAGR=aO["CAGR"], anchor_oSharpe=aO["Sharpe"],
                            anchor_oMaxDD=aO["MaxDD"],
                            d_oSharpe_vs_anchor=mo["Sharpe"] - aO["Sharpe"], t_oSharpe=tsO,
                            d_oMaxDD_vs_anchor_pp=100 * dmO, t_oMaxDD=tmO,
                            spy_oCAGR=spyO["CAGR"], spy_oSharpe=spyO["Sharpe"],
                            spy_oMaxDD=spyO["MaxDD"], live_oSharpe=liveO["Sharpe"]))

        # G7 bit-identical recompute of the anchor cell
        fr2, _ = build1(pan, I_N, I_H)
        gg2, tu2, _ = run_book(pan, fr2, C, Cp, I_G)
        publish(f"G7 bit-identical recompute {pan.name}",
                f"max |dret| {float(np.max(np.abs((gg2 - tu2*COST/1e4) - anchor))):.3e}")

    G = pd.DataFrame(grid)
    W = pd.DataFrame(wf_rows)
    gate("G2 all 126 cells published", len(G), "== 126", len(G) == 126)
    gate("G3 exactly two tuned parameters (N, H)", "2", "== 2", True)
    gate("G4 rule-8 chooser reads no row on or after 2017-01-01", "IS = warm-up..2016-12-31",
         "no OOS leakage", True)
    gate("G5 no leverage: realised weight sum never exceeds 1.0",
         f"max wsum {wsum_global:.6f}", "<= 0.75 + 1e-12", wsum_global <= I_G + 1e-12)
    gate("G6 H = 0 column is the stickiness-free book (min-hold inert)", g6_bad, "== 0",
         g6_bad == 0)

    say("\n" + "=" * 128)
    say("GRID — EVERY (N, H) CELL.  DD margin = MaxDD - 0.60 x SPY MaxDD (positive => the 4b DD "
        "leg passes).  t vs anchor from a paired 63-row block bootstrap, 400 reps.")
    say("=" * 128)
    for pn in ["U56", "B136", "SMALL"]:
        sub = G[G.panel == pn]
        say(f"\n  [{pn}]   SPY MaxDD {sub.spy_MaxDD.iloc[0]:.2%} -> DD cap "
            f"{DD_CAP*sub.spy_MaxDD.iloc[0]:.2%};  CAGR floor "
            f"{CAGR_FLOOR*sub.spy_CAGR.iloc[0]:.2%}")
        say("      N    H |    CAGR  Sharpe   MaxDD     H1     H2 | DDmarg CAGRmarg | 4a 4b 4bO | "
            "names turn drag | dSh_vs_anc    t  | dDD_pp    t  | OOS CAGR/Sharpe/MaxDD")
        for _, r in sub.iterrows():
            tag = " *" if r.is_anchor else "  "
            say(f"    {r.N:3d} {r.H:4d}{tag}| {r.CAGR:7.2%} {r.Sharpe:7.4f} {r.MaxDD:7.2%} "
                f"{r.H1:6.3f} {r.H2:6.3f} | {r.dd_margin_pp:+6.2f} {r.cagr_margin_pp:+8.2f} | "
                f"{int(r.keep4a)}  {int(r.keep4b)}   {int(r.keep4b_oos)} | {r.mean_names:5.1f} "
                f"{r.turn_y:4.2f} {r.drag_bpyr:5.1f} | {r.d_sharpe_vs_anchor:+10.4f} "
                f"{r.t_sharpe:+5.2f} | {r.d_maxdd_vs_anchor_pp:+6.2f} {r.t_maxdd:+5.2f} | "
                f"{r.oCAGR:7.2%} {r.oSharpe:7.4f} {r.oMaxDD:7.2%}")

    say("\n" + "=" * 128)
    say("RULE 8 WALK-FORWARD — (N, H) chosen by argmax IS Sharpe on warm-up..2016-12-31; "
        "2017-2026 read ONCE; scored against the FROZEN incumbent (20, 126).")
    say("=" * 128)
    say("  panel | IS pick (N,H)  IS Sh | OOS CAGR  Sharpe   MaxDD 4b 4a | ANCHOR OOS CAGR/Sh/DD "
        "| dSh (t) | dDD pp (t) | SPY OOS CAGR/Sh/DD")
    for _, r in W.iterrows():
        say(f"  {r.panel:>5} | ({r.is_N:3d},{r.is_H:4d}) {r.is_Sharpe:7.4f} | {r.oCAGR:7.2%} "
            f"{r.oSharpe:7.4f} {r.oMaxDD:7.2%}  {int(r.keep4b_oos)}  {int(r.keep4a_oos)} | "
            f"{r.anchor_oCAGR:7.2%}/{r.anchor_oSharpe:.4f}/{r.anchor_oMaxDD:7.2%} | "
            f"{r.d_oSharpe_vs_anchor:+7.4f} ({r.t_oSharpe:+5.2f}) | "
            f"{r.d_oMaxDD_vs_anchor_pp:+6.2f} ({r.t_oMaxDD:+5.2f}) | "
            f"{r.spy_oCAGR:6.2%}/{r.spy_oSharpe:.4f}/{r.spy_oMaxDD:7.2%}")

    say("\n" + "=" * 128)
    say("HEADLINE")
    say("=" * 128)
    for pn in ["U56", "B136", "SMALL"]:
        sub = G[G.panel == pn]
        a = sub[sub.is_anchor].iloc[0]
        spread = float(sub.dd_margin_pp.max() - sub.dd_margin_pp.min())
        sN = float(sub[sub.H == I_H].dd_margin_pp.max() - sub[sub.H == I_H].dd_margin_pp.min())
        sH = float(sub[sub.N == I_N].dd_margin_pp.max() - sub[sub.N == I_N].dd_margin_pp.min())
        say(f"  {pn}: JOINT (H, N) DD-margin spread {spread:.4f} pp over {len(sub)} cells "
            f"[N alone at H=126: {sN:.4f} pp; H alone at N=20: {sH:.4f} pp].  Anchor margin "
            f"{a.dd_margin_pp:+.4f} pp.  4b passes {int(sub.keep4b.sum())}/{len(sub)} full, "
            f"{int(sub.keep4b_oos.sum())}/{len(sub)} OOS, {int((sub.keep4b & sub.keep4b_oos).sum())} both; "
            f"4a {int(sub.keep4a.sum())}/{len(sub)}.")
        say(f"        against idea 1409's committed (skip, long) spread {SKIP_LONG_SPREAD_PP:.4f} pp: "
            f"ratio {spread/SKIP_LONG_SPREAD_PP:.3f}x;  against the anchor's own margin "
            f"{ANCHOR_MARGIN_PP:.4f} pp: {spread/ANCHOR_MARGIN_PP:.2f}x.")
        say(f"        DD-margin argmax cell "
            f"{sub.loc[sub.dd_margin_pp.idxmax(), ['N','H','dd_margin_pp']].to_dict()};  "
            f"argmin {sub.loc[sub.dd_margin_pp.idxmin(), ['N','H','dd_margin_pp']].to_dict()}")
    nb = G[~G.is_anchor]
    say(f"  RESOLUTION vs the frozen anchor: {int((np.abs(nb.t_sharpe) > 2).sum())} of {len(nb)} "
        f"non-anchor cells resolve |t| > 2 on Sharpe (median dSharpe "
        f"{nb.d_sharpe_vs_anchor.median():+.4f}); "
        f"{int((np.abs(nb.t_maxdd) > 2).sum())} of {len(nb)} on MaxDD (median gap "
        f"{nb.d_maxdd_vs_anchor_pp.median():+.2f} pp).")
    say(f"  OOS: {int((np.abs(nb.ot_sharpe) > 2).sum())} of {len(nb)} resolve |t| > 2 on Sharpe.")
    say(f"  RULE 8: chooser picked the anchor in {int(W.picked_anchor.sum())} of {len(W)} panels; "
        f"mean OOS dSharpe vs anchor {W.d_oSharpe_vs_anchor.mean():+.4f}, "
        f"{int((W.d_oSharpe_vs_anchor > 0).sum())} of {len(W)} positive; OOS 4b "
        f"{int(W.keep4b_oos.sum())} of {len(W)}, 4a {int(W.keep4a_oos.sum())} of {len(W)}.")
    both = G[G.keep4b & G.keep4b_oos]
    say(f"  CELLS PASSING 4b FULL *AND* OOS: {len(both)} of {len(G)} "
        f"({sorted(set(zip(both.panel, both.N, both.H)))[:12]}{' ...' if len(both) > 12 else ''})")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n  wrote {OUT.name}.grid.csv / .walkforward.csv / .gates.csv / .log.txt")
    say(f"  elapsed {time.time()-t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

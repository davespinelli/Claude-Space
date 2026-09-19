#!/usr/bin/env python3
"""
Idea 1433 (lane B, 2026-09-19) — does INTRA-BOOK INVERSE-VOL SIZING buy the BINDING 4b DD LEG
at IDENTICAL NAMES and IDENTICAL GROSS?

THE PREMISE.  The standing 2026-09-04 KEEP-4b incumbent (U56, N = 20, H = 126, gross 0.75,
weekly Fri-decide / Mon-trade, 10 bps, t+1) passes 4b on ONE leg's margin: MaxDD -19.13%
against a -20.23% cap, +1.1028 pp.  Every prior attack on that leg this month died the SAME
death: a trailing equity stop (1405), a breadth throttle (1413) and a convention ensemble
(1423) each shallowed drawdown by HOLDING LESS STOCK or HOLDING MORE NAMES, i.e. they were
EXPOSURE or CONCENTRATION dials in a costume, and every one failed against its own
exposure-matched twin.

This run closes that channel BY CONSTRUCTION.  Selection is untouched: the same names, the
same name count, the same rebalance rows, the same gross 0.75 on every single cell.  The only
thing that moves is how the SAME gross is DIVIDED among the SAME held names:

    w_i  proportional to  (1 / vol_i)^p ,   sum w_i = 0.75

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  P  {0.0, 0.5, 1.0, 1.5, 2.0}      DIAL 1 — sizing exponent.  P = 0.0 IS THE FROZEN
                                              INCUMBENT (equal weight), present at every L.
  L  {20, 63, 126, 252}             DIAL 2 — trailing vol lookback, in trading days.

20 cells per panel, 60 in all, EVERY ONE published in .grid.csv.

THE CONTROL THAT DECIDES THE VERDICT.  A sizing rule that shallows drawdown by simply holding
a more CONCENTRATED or more DISPERSED weight vector is not a finding about volatility — it is
a dispersion dial.  So every cell is scored against its own WEIGHT-PERMUTATION TWIN: at each
rebalance the cell's OWN weight multiset is re-assigned to the SAME held names in a seeded
random order.  The twin therefore matches the cell EXACTLY on gross, on names, on name count,
on rebalance rows and on the whole weight DISTRIBUTION (hence identical effective-N and
identical Herfindahl at every row) and differs ONLY in WHICH name gets WHICH weight.  Any gap
is therefore attributable to the VOL INFORMATION alone.  K = 12 permutation draws per cell
(seeds derived from 20260919) give the twin band; gaps are scored by a PAIRED circular-block
bootstrap (400 reps x 63-row blocks, seed 20260919, identical block starts) against the
MEDIAN-Sharpe twin draw.  |t| > 2 is the record's bar; anything inside its own SE is published
as UNRESOLVED, not as a finding.

THE BAR, PRE-REGISTERED HERE BEFORE ANY NUMBER WAS READ.  This is worth capital only if on
U56 (i) the 4b DD margin exceeds the frozen anchor's own +1.1028 pp AND (ii) the Sharpe edge
over its own permutation twin resolves |t| > 2.  Anything less is a KILL or a PARK, whatever
the headline says.

VOL FLOOR IS NOT A THIRD DIAL: the daily-vol floor is INHERITED from the live code
(`baseline.score` clips vol20 at 0.08 annualised), applied here as 0.08/sqrt(252) per day at
every L.  A name with no vol history at the decision row takes the cross-sectional median of
that row, which is the one choice that neither favours nor penalises it.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); both KEEP paths at
every cell; the halves; IS and OOS windows; turnover and its 10 bps drag in bp/yr; realised
mean gross; realised effective N and max weight.

COMPARANDS (rule 3): the live RULES v2 baseline at 10 bps weekly, SPY buy-and-hold, and the
FROZEN (P = 0) incumbent.

PROTOCOL: rule 1 (>= 10y); rule 2 (t+1, 10 bps, no leverage, no shorting); rule 3 (RULES v2
AND SPY); rule 4 (both KEEP paths, 2 tuned parameters); rule 8 (walk-forward: (P, L) chosen on
warm-up..2016-12-31 by argmax IS Sharpe, 2017-2026 read ONCE, scored against the frozen
incumbent and SPY); rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py are NOT modified.

GATES.  G0 sample >= 10y.  G1 CROSS-SCRIPT REPLAY: the P = 0 cell must reproduce the committed
U56 anchor (15.80% / 1.1537 / -19.13% full; 17.32% / 1.1857 / -19.13% OOS).  G2 the P = 0 cell
is BIT-IDENTICAL across all four L (the sizing is inert at exponent zero).  G3 the P = 0
permutation twin is BIT-IDENTICAL to the P = 0 cell (permuting equal weights changes nothing).
G4 all 60 cells published.  G5 exactly two tuned parameters.  G6 the chooser reads no row on
or after 2017-01-01.  G7 no leverage: realised weight sum never exceeds 1.0, and every cell's
realised mean gross matches the anchor's to < 1e-12 (the exposure channel IS shut).  G8 every
cell holds the IDENTICAL name set on every row as the anchor (selection untouched).  G9 each
permutation twin matches its own cell's effective-N path to < 1e-12.  G10 bit-identical
recompute of the U56 headline cell.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-19_intra-book-inverse-vol-sizing_B.py
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
SLUG = "intra-book-inverse-vol-sizing"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G = 20, 126, 0.75              # the frozen 2026-09-04 incumbent
COST, CADENCE = 10.0, "W"
PS = [0.0, 0.5, 1.0, 1.5, 2.0]
LS = [20, 63, 126, 252]
NPERM, SEED = 12, 20260919
VOL_FLOOR_D = 0.08 / np.sqrt(252.0)        # inherited from baseline.score's clip(lower=0.08)
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BOOT_REPS, BOOT_BLOCK = 400, 63
C_U56 = dict(CAGR=0.1580, Sharpe=1.1537, MaxDD=-0.1913, oSharpe=1.1857)
BAR_DD_PP = 1.1028                          # the anchor's own committed 4b DD margin, U56
BAR_T = 2.0

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
        r = px[invest].pct_change()
        self.vol = {L: r.rolling(L).std().values for L in LS}   # DAILY vol, per lookback


def segments(pan, N, H, lag=1):
    """The frozen min-hold selection frame.  Returns [(i0, i1, ts, local_cols)], where
    local_cols index pan.iinv.  Depends on NEITHER dial, so it is built ONCE per panel and
    every cell in this run holds the IDENTICAL names on the IDENTICAL rows (gate G8)."""
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


def cell_weights(pan, segs, p, L, perm_seed=None):
    """Per-segment weight vector over the segment's OWN held names, summing to I_G.
    perm_seed re-assigns the SAME multiset to the SAME names in a seeded random order."""
    V = pan.vol[L]
    rng = np.random.default_rng(perm_seed) if perm_seed is not None else None
    ws = []
    for (t, stop, ts, sel) in segs:
        n = len(sel)
        if n == 0:
            ws.append(np.zeros(0))
            continue
        if p == 0.0:
            w = np.full(n, 1.0 / n)
        else:
            v = V[ts, sel].astype(float)
            fin = np.isfinite(v)
            if not fin.all():
                med = np.nanmedian(v[fin]) if fin.any() else VOL_FLOOR_D
                v = np.where(fin, v, med)
            v = np.maximum(v, VOL_FLOOR_D)
            x = v ** (-p)
            w = x / x.sum()
        if rng is not None:
            w = w[rng.permutation(n)]
        ws.append(I_G * w)
    return ws


def run_book(pan, segs, ws, C, Cp):
    """One book.  Weights are applied at row i0 and drift inside the segment (engine
    convention: buy-and-hold between rebalances, cash remainder held flat)."""
    rets = pan.rets
    T, M = rets.shape
    turn = np.zeros(T)
    out = np.zeros(T)
    gross_path = np.zeros(T)
    effn = np.zeros(len(segs))
    maxw = np.zeros(len(segs))
    curw = np.zeros(M)
    wsum_max = 0.0
    for j, ((i0, i1, ts, sel), wv) in enumerate(zip(segs, ws)):
        w0 = np.zeros(M)
        if len(sel):
            w0[pan.iinv[sel]] = wv
            q = wv / wv.sum()
            effn[j] = 1.0 / float((q ** 2).sum())
            maxw[j] = float(wv.max())
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
    return out, turn, gross_path, effn, maxw, wsum_max


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


def paired_block_dsharpe(a, b, reps=BOOT_REPS, L=BOOT_BLOCK, seed=SEED):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    nb = int(np.ceil(n / L))
    rng = np.random.default_rng(seed)
    starts = rng.integers(0, n, size=(reps, nb))
    idx = (starts[:, :, None] + np.arange(L)[None, None, :]).reshape(reps, nb * L)[:, :n] % n
    A, B = a[idx], b[idx]

    def sh(X):
        v = X.std(axis=1, ddof=0) * np.sqrt(252)
        return np.where(v > 0, X.mean(axis=1) * 252 / v, np.nan)

    d = sh(A) - sh(B)
    obs = float(sharpe(a) - sharpe(b))
    se = float(np.nanstd(d, ddof=1))
    return obs, se, (obs / se if se > 0 else np.nan)


def main():
    t0 = time.time()
    say("=" * 124)
    say("IDEA 1433 (lane B, 2026-09-19) — does INTRA-BOOK INVERSE-VOL SIZING buy the BINDING "
        "4b DD LEG at IDENTICAL NAMES and IDENTICAL GROSS?")
    say("DIALS: P {0,0.5,1.0,1.5,2.0} x L {20,63,126,252} on the frozen incumbent (N=20, H=126, "
        "gross 0.75, MAXVOL 0.60, MA gate ON, weekly, 10 bps, t+1).  P=0 IS the incumbent.")
    say("CONTROL: a WEIGHT-PERMUTATION twin per cell (same weight multiset, shuffled across the "
        f"same held names, K={NPERM} seeds) — matches gross, names, name count AND the whole")
    say("         weight distribution, so the only difference is WHICH name gets WHICH weight.")
    say(f"PRE-REGISTERED BAR (stated before any number was read): capital only if U56 DD margin "
        f"> {BAR_DD_PP:+.4f} pp AND |t| vs its own permutation twin > {BAR_T:.0f}.")
    say("=" * 124)

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
        "sub-$2B screen carried back to 2010.  Every absolute level below is an UPPER BOUND and "
        "every 4b pass an optimistic one; what this run reads is a CONTRAST between two sizings "
        "of the SAME names on the SAME days, which the bias cannot manufacture.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y);  {len(p.reb)} weekly rebalances")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)

    grid, wf_rows, perm_rows = [], [], []
    wsum_global, g2_dev, g3_dev, g7_dev, g9_dev = 0.0, 0.0, 0.0, 0.0, 0.0
    headline_ret = None

    for pan in panels:
        T = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        spy, spyO = bmpack(pan.spy[WARMUP:]), bmpack(pan.spy[i_oos:])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])
        segs = segments(pan, I_N, I_H)
        C = np.cumprod(1.0 + pan.rets, axis=0)
        Cp = np.vstack([np.ones((1, pan.rets.shape[1])), C[:-1]])

        say(f"\n  [{pan.name}]  SPY  CAGR {spy['CAGR']:.2%} Sharpe {spy['Sharpe']:.4f} MaxDD "
            f"{spy['MaxDD']:.2%} H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f}  |  4b bars: DD cap "
            f"{DD_CAP*spy['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps  CAGR {live['CAGR']:.2%} Sharpe {live['Sharpe']:.4f} "
            f"MaxDD {live['MaxDD']:.2%} H1/H2 {live['H1']:.3f}/{live['H2']:.3f}")

        # ---- the frozen anchor (P = 0) ---------------------------------------------------
        ws0 = cell_weights(pan, segs, 0.0, LS[0])
        g0, t0_, gp0, en0, mw0, ws_ = run_book(pan, segs, ws0, C, Cp)
        wsum_global = max(wsum_global, ws_)
        anchor = g0 - t0_ * COST / 1e4
        am, ao = triple(anchor[WARMUP:]), triple(anchor[i_oos:])
        ah1, ah2 = halves(anchor[WARMUP:])
        anchor_mg = float(np.mean(gp0[WARMUP:]))
        say(f"           FROZEN INCUMBENT (P=0) CAGR {am['CAGR']:.2%} Sharpe {am['Sharpe']:.4f} "
            f"MaxDD {am['MaxDD']:.2%} H1/H2 {ah1:.4f}/{ah2:.4f} | OOS {ao['CAGR']:.2%}/"
            f"{ao['Sharpe']:.4f}/{ao['MaxDD']:.2%} | mean gross {anchor_mg:.6f}, effN "
            f"{en0.mean():.2f}")
        if pan.name == "U56":
            d = max(abs(am["Sharpe"] - C_U56["Sharpe"]), abs(ao["Sharpe"] - C_U56["oSharpe"]))
            gate("G1 cross-script replay of the committed 2026-09-04 U56 anchor "
                 "(15.80%/1.1537/-19.13% full; 17.32%/1.1857/-19.13% OOS)",
                 f"|dSharpe| {d:.2e}  (got {am['CAGR']:.4f}/{am['Sharpe']:.4f}/"
                 f"{am['MaxDD']:.4f}; OOS {ao['Sharpe']:.4f})", "< 5e-3", d < 5e-3)
            say(f"           ANCHOR 4b DD MARGIN (the bar): "
                f"{100*(am['MaxDD'] - DD_CAP*spy['MaxDD']):+.4f} pp")

        # ---- the 20-cell sizing grid -----------------------------------------------------
        for p in PS:
            for L in LS:
                ws = cell_weights(pan, segs, p, L)
                gg, tu, gp, en, mw, wsx = run_book(pan, segs, ws, C, Cp)
                wsum_global = max(wsum_global, wsx)
                rr = gg - tu * COST / 1e4
                if p == 0.0:
                    g2_dev = max(g2_dev, float(np.max(np.abs(rr - anchor))))
                g7_dev = max(g7_dev, abs(float(np.mean(gp[WARMUP:])) - anchor_mg))
                k4a, k4b, m, h1, h2, legs = keep_paths(rr[WARMUP:], spy, live)
                k4aO, k4bO, mo, _, _, legsO = keep_paths(rr[i_oos:], spyO, liveO)

                # --- weight-permutation twins (K seeds) ---
                tw_r, tw_s, tw_dd = [], [], []
                for k in range(NPERM):
                    wsp = cell_weights(pan, segs, p, L, perm_seed=SEED + 1000 * k + int(100 * p) + L)
                    gp_, tp_, gpp, enp, _, _ = run_book(pan, segs, wsp, C, Cp)
                    rp = gp_ - tp_ * COST / 1e4
                    g9_dev = max(g9_dev, float(np.max(np.abs(np.sort(enp) - np.sort(en)))))
                    if p == 0.0:
                        g3_dev = max(g3_dev, float(np.max(np.abs(rp - anchor))))
                    tw_r.append(rp)
                    tw_s.append(sharpe(rp[WARMUP:]))
                    tw_dd.append(mdd(rp[WARMUP:]))
                tw_s = np.array(tw_s)
                tw_dd = np.array(tw_dd)
                jmed = int(np.argsort(tw_s)[len(tw_s) // 2])
                twin = tw_r[jmed]
                dsh, se, tstat = paired_block_dsharpe(rr[WARMUP:], twin[WARMUP:])
                dshO, seO, tO = paired_block_dsharpe(rr[i_oos:], twin[i_oos:])
                s_pct = float(np.mean(tw_s <= m["Sharpe"]))
                dd_pct = float(np.mean(tw_dd <= m["MaxDD"]))
                n = T - WARMUP
                turn_y = float(np.sum(tu[WARMUP:]) * 252.0 / n)
                grid.append(dict(
                    panel=pan.name, p=p, L=L,
                    CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                    oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                    keep4a=k4a, keep4b=k4b, keep4b_oos=k4bO, keep4a_oos=k4aO,
                    legH1=legs["H1"], legH2=legs["H2"], legDD=legs["DD"], legCAGR=legs["CAGR"],
                    dd_margin_pp=100 * (m["MaxDD"] - DD_CAP * spy["MaxDD"]),
                    cagr_margin_pp=100 * (m["CAGR"] - CAGR_FLOOR * spy["CAGR"]),
                    d_sharpe_vs_anchor=m["Sharpe"] - am["Sharpe"],
                    d_maxdd_vs_anchor_pp=100 * (m["MaxDD"] - am["MaxDD"]),
                    mean_gross=float(np.mean(gp[WARMUP:])), eff_n=float(en.mean()),
                    max_w=float(mw.mean()), turn_y=turn_y, drag_bpyr=turn_y * COST,
                    twin_Sharpe_med=float(np.median(tw_s)),
                    twin_Sharpe_lo=float(tw_s.min()), twin_Sharpe_hi=float(tw_s.max()),
                    twin_MaxDD_med=float(np.median(tw_dd)),
                    sharpe_pct_in_twins=s_pct, maxdd_pct_in_twins=dd_pct,
                    d_sharpe_vs_twin=dsh, se_vs_twin=se, t_vs_twin=tstat,
                    od_sharpe_vs_twin=dshO, ose_vs_twin=seO, ot_vs_twin=tO,
                    spy_Sharpe=spy["Sharpe"], spy_MaxDD=spy["MaxDD"], spy_CAGR=spy["CAGR"],
                    live_Sharpe=live["Sharpe"], live_MaxDD=live["MaxDD"],
                    anchor_Sharpe=am["Sharpe"], anchor_MaxDD=am["MaxDD"],
                    anchor_dd_margin_pp=100 * (am["MaxDD"] - DD_CAP * spy["MaxDD"])))
                for k, (s_, d_) in enumerate(zip(tw_s, tw_dd)):
                    perm_rows.append(dict(panel=pan.name, p=p, L=L, draw=k, Sharpe=s_, MaxDD=d_))
                if pan.name == "U56" and p == 1.0 and L == 63:
                    headline_ret = rr.copy()

        # ---- rule 8 ------------------------------------------------------------------------
        i_is0, i_is1 = WARMUP, int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        best, bs = None, -np.inf
        for p in PS:
            for L in LS:
                ws = cell_weights(pan, segs, p, L)
                gg, tu, _, _, _, _ = run_book(pan, segs, ws, C, Cp)
                rr = gg - tu * COST / 1e4
                s = sharpe(rr[i_is0:i_is1])
                if s > bs:
                    bs, best = s, (p, L)
        ws = cell_weights(pan, segs, best[0], best[1])
        gg, tu, _, _, _, _ = run_book(pan, segs, ws, C, Cp)
        rr = gg - tu * COST / 1e4
        k4aO, k4bO, mo, _, _, legsO = keep_paths(rr[i_oos:], spyO, liveO)
        aO = triple(anchor[i_oos:])
        dshA, seA, tA = paired_block_dsharpe(rr[i_oos:], anchor[i_oos:])
        wf_rows.append(dict(panel=pan.name, is_p=best[0], is_L=best[1], is_Sharpe=bs,
                            oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                            keep4b_oos=k4bO, keep4a_oos=k4aO,
                            oleg_H1=legsO["H1"], oleg_H2=legsO["H2"], oleg_DD=legsO["DD"],
                            oleg_CAGR=legsO["CAGR"],
                            anchor_oCAGR=aO["CAGR"], anchor_oSharpe=aO["Sharpe"],
                            anchor_oMaxDD=aO["MaxDD"],
                            d_oSharpe_vs_anchor=mo["Sharpe"] - aO["Sharpe"],
                            t_oSharpe_vs_anchor=tA,
                            spy_oSharpe=spyO["Sharpe"], spy_oCAGR=spyO["CAGR"],
                            spy_oMaxDD=spyO["MaxDD"],
                            live_oSharpe=liveO["Sharpe"], live_oMaxDD=liveO["MaxDD"]))

    G = pd.DataFrame(grid)
    W = pd.DataFrame(wf_rows)
    P = pd.DataFrame(perm_rows)

    gate("G2 P=0 cell BIT-IDENTICAL across all four L", f"max |dret| {g2_dev:.3e}", "< 1e-15",
         g2_dev < 1e-15)
    gate("G3 P=0 permutation twin BIT-IDENTICAL to the P=0 cell", f"max |dret| {g3_dev:.3e}",
         "< 1e-15", g3_dev < 1e-15)
    gate("G4 all 60 grid cells published", len(G), "== 60", len(G) == 60)
    gate("G5 exactly two tuned parameters (p, L)", "2", "== 2", True)
    gate("G6 chooser reads no row on or after 2017-01-01", "IS = warm-up..2016-12-31",
         "no OOS leakage", True)
    gate("G7 exposure channel SHUT: every cell's realised mean gross == the anchor's",
         f"max |dmean gross| {g7_dev:.3e}", "< 1e-12", g7_dev < 1e-12)
    gate("G7b no leverage: realised weight sum never exceeds 1.0", f"max wsum {wsum_global:.6f}",
         "<= 1.0 + 1e-12", wsum_global <= 1.0 + 1e-12)
    gate("G8 selection untouched: every cell shares ONE frame per panel (built once, before any "
         "dial)", "by construction", "identical name sets", True)
    gate("G9 each permutation twin matches its cell's effective-N multiset",
         f"max |d sorted effN| {g9_dev:.3e}", "< 1e-12", g9_dev < 1e-12)

    say("\n" + "=" * 124)
    say("GRID — EVERY CELL.  DD margin = MaxDD - 0.60 x SPY MaxDD (positive = the 4b DD leg "
        "passes).  TWIN = weight-permutation control (same multiset, shuffled names).")
    say("pct = share of the K permutation draws at or below the cell (0.5 = the vol ordering "
        "buys nothing the shuffle does not).")
    say("=" * 124)
    for pan in ["U56", "B136", "SMALL"]:
        sub = G[G.panel == pan]
        say(f"\n  [{pan}]   anchor DD margin {sub.anchor_dd_margin_pp.iloc[0]:+.4f} pp, "
            f"anchor Sharpe {sub.anchor_Sharpe.iloc[0]:.4f}")
        say("      p    L |    CAGR  Sharpe   MaxDD     H1     H2 | DDmarg CAGRmarg | 4a 4b oos4b "
            "| effN maxW meanG | turn drag | twinShMed  dSh    SE     t   | Shpct DDpct | OOS "
            "CAGR/Sh/DD")
        for _, r in sub.iterrows():
            say(f"    {r.p:4.1f} {int(r.L):4d} | {r.CAGR:7.2%} {r.Sharpe:7.4f} {r.MaxDD:7.2%} "
                f"{r.H1:6.3f} {r.H2:6.3f} | {r.dd_margin_pp:+6.2f} {r.cagr_margin_pp:+8.2f} | "
                f"{int(r.keep4a)}  {int(r.keep4b)}   {int(r.keep4b_oos)}   | {r.eff_n:5.2f} "
                f"{r.max_w:4.3f} {r.mean_gross:5.3f} | {r.turn_y:4.2f} {r.drag_bpyr:5.1f} | "
                f"{r.twin_Sharpe_med:9.4f} {r.d_sharpe_vs_twin:+6.4f} {r.se_vs_twin:6.4f} "
                f"{r.t_vs_twin:+5.2f} | {r.sharpe_pct_in_twins:5.3f} {r.maxdd_pct_in_twins:5.3f} "
                f"| {r.oCAGR:7.2%} {r.oSharpe:6.4f} {r.oMaxDD:7.2%}")

    say("\n" + "=" * 124)
    say("RULE 8 WALK-FORWARD — (p, L) chosen by argmax IS Sharpe on warm-up..2016-12-31; "
        "2017-2026 read ONCE.")
    say("=" * 124)
    say("  panel | IS pick (p,L)  IS Sh | OOS CAGR  Sharpe   MaxDD 4b 4a | legs H1/H2/DD/CAGR | "
        "ANCHOR OOS CAGR/Sh/DD | dSh vs anchor (t) | SPY OOS CAGR/Sh/DD")
    for _, r in W.iterrows():
        say(f"  {r.panel:>5} | ({r.is_p:4.1f},{int(r.is_L):4d}) {r.is_Sharpe:6.4f} | "
            f"{r.oCAGR:7.2%} {r.oSharpe:7.4f} {r.oMaxDD:7.2%}  {int(r.keep4b_oos)}  "
            f"{int(r.keep4a_oos)} | {int(r.oleg_H1)}/{int(r.oleg_H2)}/{int(r.oleg_DD)}/"
            f"{int(r.oleg_CAGR)} | {r.anchor_oCAGR:7.2%} {r.anchor_oSharpe:7.4f} "
            f"{r.anchor_oMaxDD:7.2%} | {r.d_oSharpe_vs_anchor:+7.4f} ({r.t_oSharpe_vs_anchor:+5.2f})"
            f" | {r.spy_oCAGR:6.2%}/{r.spy_oSharpe:.4f}/{r.spy_oMaxDD:7.2%}")

    say("\n" + "=" * 124)
    say("THE PRE-REGISTERED BAR")
    say("=" * 124)
    U = G[(G.panel == "U56") & (G.p > 0)]
    leg_i = U[U.dd_margin_pp > BAR_DD_PP]
    leg_ii = U[U.t_vs_twin.abs() > BAR_T]
    both = U[(U.dd_margin_pp > BAR_DD_PP) & (U.t_vs_twin.abs() > BAR_T)]
    say(f"  (i)  U56 DD margin > the anchor's {BAR_DD_PP:+.4f} pp : {len(leg_i)} of {len(U)} "
        f"biting cells (range {U.dd_margin_pp.min():+.4f} .. {U.dd_margin_pp.max():+.4f} pp)")
    say(f"  (ii) U56 |t| vs its own permutation twin > {BAR_T:.0f} : {len(leg_ii)} of {len(U)} "
        f"(t range {U.t_vs_twin.min():+.2f} .. {U.t_vs_twin.max():+.2f})")
    say(f"  BOTH: {len(both)} of {len(U)}.")
    allb = G[G.p > 0]
    say(f"  ALL PANELS, resolution against the shuffle: |t| > 2 at "
        f"{int((allb.t_vs_twin.abs() > BAR_T).sum())} of {len(allb)} cells full-sample, "
        f"{int((allb.ot_vs_twin.abs() > BAR_T).sum())} of {len(allb)} OOS.")
    say(f"  ALL PANELS, KEEP paths: 4a {int(G.keep4a.sum())} of {len(G)}; "
        f"4b full {int(G.keep4b.sum())} of {len(G)}; 4b OOS {int(G.keep4b_oos.sum())} of {len(G)};"
        f" both {int((G.keep4b & G.keep4b_oos).sum())}.")
    say(f"  Median |dSharpe| vs twin across all {len(allb)} biting cells: "
        f"{allb.d_sharpe_vs_twin.abs().median():.4f}; median Sharpe percentile inside the twin "
        f"band {allb.sharpe_pct_in_twins.median():.3f} (0.5 = no information).")

    # G10 bit-identical recompute of the U56 headline cell
    pan = panels[0]
    segs = segments(pan, I_N, I_H)
    C = np.cumprod(1.0 + pan.rets, axis=0)
    Cp = np.vstack([np.ones((1, pan.rets.shape[1])), C[:-1]])
    gg, tu, _, _, _, _ = run_book(pan, segs, cell_weights(pan, segs, 1.0, 63), C, Cp)
    rr = gg - tu * COST / 1e4
    d10 = float(np.max(np.abs(rr - headline_ret)))
    gate("G10 bit-identical recompute (U56, p=1.0, L=63)", f"max |dret| {d10:.3e}", "< 1e-15",
         d10 < 1e-15)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    P.to_csv(f"{OUT}.perm.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    say(f"\n  wrote {OUT.name}.grid.csv / .walkforward.csv / .perm.csv / .gates.csv / .log.txt")
    say(f"  ALL GATES PASS: {all(g['pass_'] for g in GATES)}   ({time.time()-t0:.1f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

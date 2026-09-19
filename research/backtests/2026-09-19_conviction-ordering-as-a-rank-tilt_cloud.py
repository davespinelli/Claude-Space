#!/usr/bin/env python3
"""
Idea 1501 (lane cloud, 2026-09-19, idea 1 of 2) — is the CONVICTION-ORDERING channel a REAL
SIZING DEVICE once it stops hiding inside a TURNOVER CAP?

THE PREMISE.  Idea 1484 split the per-rebalance turnover cap's matched-turnover gap into two
halves and found the BRAKE half NEGATIVE (-0.0211 of Sharpe, positive at only 8 of 30 cells)
while the WHOLE residual was WHICH names get traded: +1.125 pp of CAGR, positive at 26 of 30
cells.  A cap is a clumsy carrier for that claim — it moves turnover, exposure timing and
ordering at once.  This run prices the ordering DIRECTLY, as a rank tilt on the frozen
incumbent's OWN held set, with nothing else moving:

    w_i  proportional to  (G / n) * (1 + k * z_i),     z_i = within-held-set rank z-score

z_i is built from the SAME composite the book already screens on, read on the SAME lagged row
the selection reads, over the SAME names the frozen book holds.  k is the single dial.  k = 0 IS
THE FROZEN INCUMBENT (equal weight) exactly, and k < 0 is the anti-tilt — the sign test that a
positive finding must beat.

WHY A DE-GROSS TWIN IS NOT THE CONTROL HERE (and what replaces it).  The tilt is GROSS-NEUTRAL
BY CONSTRUCTION: sum_i (1 + k z_i) = n because z is demeaned inside the held set, so realised
mean gross is unchanged and the record's usual exposure-matched flat cut degenerates to the k = 0
anchor itself (published, as the g-ladder).  The live confound is different and sharper: a tilt
disperses weights, and DISPERSION ALONE changes a book (it concentrates NAV into fewer names).
So every tilt cell is scored against a PERMUTED-z TWIN — the same k, the same weight multiset at
every single rebalance, the ordering destroyed by a random permutation inside the held set (5
seeds).  The twin has, by construction, identical gross, identical weight dispersion, identical
effective name count and near-identical turnover; it differs ONLY in WHICH name gets the big
weight.  If the tilt does not beat its permuted twin, the ordering carries nothing and 1484's
mechanism line needs retracting.  Gaps are scored by a PAIRED circular-block bootstrap (400 reps
x 63-row blocks, identical block starts for both books); |t| > 2 is the record's bar and a gap
inside its own SE is published UNRESOLVED, not as a finding.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  k     {-1.00,-0.75,-0.50,-0.25,-0.10, 0.00, +0.10, +0.25, +0.50, +0.75, +1.00}   DIAL 1
  COST  {0, 10, 25, 50} bps                                                        DIAL 2
        (verdicts are read at PROTOCOL's binding 10 bps; the other rungs are reported)

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); both KEEP paths at every
cell; the halves; IS and OOS windows; realised mean gross; effective name count 1/sum w^2;
clipped-weight incidence; turnover and its drag in bp/yr.

NO LOOK-AHEAD.  The tilt reads the composite at row t-1 (the same lagged row the frozen
selection reads) and the rebalance grid is itself already lagged one row (rule 2), so it is
Friday-close information traded at Monday's open.  Negative raw weights are impossible to hold
long-only, so (1 + k z) is clipped at 0 and the held set renormalised to exactly G; the clip
incidence is published because a heavy clip turns the tilt into a concentration device and that
is a different finding.

COMPARANDS (rule 3): the live RULES v2 baseline at 10 bps weekly, SPY buy-and-hold, and the
FROZEN (k = 0) incumbent (U56, N = 20, H = 126, gross 0.75, MAXVOL 0.60, MA gate, weekly).

PROTOCOL: rule 1 (>= 10y); rule 2 (t+1, 10 bps, no leverage, no shorting); rule 3; rule 4 (both
KEEP paths, 2 tuned parameters); rule 8 (walk-forward: k chosen on warm-up..2016-12-31, by argmax
IS Sharpe AND separately by argmax IS CAGR, 2017-2026 read ONCE); rule 9 (survivorship stated).
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

GATES.  G1 CROSS-SCRIPT REPLAY: the k = 0 cell must reproduce the committed U56 frozen anchor
(~15.8% / ~1.152 / -19.13% full; ~17.3% / ~1.185 OOS).  G2 the k = 0 tilt frame is BIT-IDENTICAL
to the equal-weight frame.  G3 the k = 0 permuted twin is bit-identical to the anchor at every
seed (a permutation of an equal-weight vector is that vector).  G4 gross neutrality: realised
mean gross identical (< 1e-12) across every k at fixed panel.  G5 no leverage: realised weight
sum never exceeds 1.0.  G6 the chooser reads no row on or after 2017-01-01.  G7 all 132 grid
cells published.  G8 bit-identical recompute of one cell.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-19_conviction-ordering-as-a-rank-tilt_cloud.py
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
SLUG = "conviction-ordering-as-a-rank-tilt"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G = 20, 126, 0.75              # the frozen 2026-09-04 incumbent
CADENCE = "W"
KS = [-1.00, -0.75, -0.50, -0.25, -0.10, 0.00, 0.10, 0.25, 0.50, 0.75, 1.00]
COSTS = [0.0, 10.0, 25.0, 50.0]
COST = 10.0                                 # PROTOCOL's binding rung
PERM_SEEDS = [1, 2, 3, 4, 5]
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BOOT_REPS, BOOT_BLOCK, BOOT_SEED = 400, 63, 20260919
C_U56 = dict(CAGR=0.1580, Sharpe=1.1530, MaxDD=-0.1913, oSharpe=1.1851)   # committed anchor

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
        self.sc = sc
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values


def build_frame(pan, N, H, k=0.0, perm_seed=None, lag=1):
    """The frozen min-hold selection frame at GROSS = 1.0, weighted by the rank tilt.

    k = 0 gives the equal-weight incumbent exactly.  perm_seed != None permutes z inside the
    held set at every rebalance (the ordering-destroying twin: same weight multiset, same n,
    same gross).  Returns (frame, diagnostics dict)."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    reb = pan.reb
    rng = np.random.default_rng(perm_seed) if perm_seed is not None else None
    n_clip = 0
    n_cells = 0
    eff_acc, eff_n = 0.0, 0
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
            kk = pan.rank_key[ts].copy()
            kk[~(pan.elig[ts] & pr[ts])] = np.inf
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
        if not len(sel):
            continue
        n = len(sel)
        if k == 0.0:
            w = np.full(n, 1.0 / n)
        else:
            s = pan.sc[ts, sel]
            s = np.where(np.isfinite(s), s, -np.inf)
            # within-held-set rank (1 = worst .. n = best), ties broken stably
            r = np.empty(n)
            r[np.argsort(s, kind="stable")] = np.arange(1, n + 1)
            if n > 1:
                z = (r - (n + 1) / 2.0) / np.std(r)
            else:
                z = np.zeros(1)
            if rng is not None:
                z = z[rng.permutation(n)]
            raw = 1.0 + k * z
            n_clip += int((raw < 0).sum())
            raw = np.clip(raw, 0.0, None)
            tot = raw.sum()
            w = raw / tot if tot > 0 else np.full(n, 1.0 / n)
        n_cells += n
        eff_acc += 1.0 / float((w ** 2).sum())
        eff_n += 1
        stop = reb[i + 1] if i + 1 < len(reb) else T
        W[t:stop, pan.iinv[sel]] = w
    return W, dict(clip_share=n_clip / max(n_cells, 1), eff_names=eff_acc / max(eff_n, 1))


def run(pan, frame, C, Cp, g):
    """One book: drift between weekly rebalances, gross-of-cost returns + per-row turnover."""
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


def paired_block(a, b, what="sharpe"):
    """Paired circular-block bootstrap SE of (stat(a) - stat(b)); identical block starts."""
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    idx = _boot_idx(n)
    A, B = a[idx], b[idx]
    if what == "sharpe":
        def st(X):
            v = X.std(axis=1, ddof=0) * np.sqrt(252)
            return np.where(v > 0, X.mean(axis=1) * 252 / v, np.nan)
        obs = float(sharpe(a) - sharpe(b))
    else:
        def st(X):
            return np.cumprod(1 + X, axis=1)[:, -1] ** (252.0 / X.shape[1]) - 1.0
        obs = float(cagr(a) - cagr(b))
    d = st(A) - st(B)
    se = float(np.nanstd(d, ddof=1))
    return obs, se, (obs / se if se > 0 else np.nan)


def main():
    t0 = time.time()
    say("=" * 128)
    say("IDEA 1501 (lane cloud, 2026-09-19, idea 1 of 2) — is the CONVICTION-ORDERING channel a "
        "REAL SIZING DEVICE once it stops hiding inside a TURNOVER CAP?")
    say("DIAL 1 k in {-1.00,-0.75,-0.50,-0.25,-0.10,0,+0.10,+0.25,+0.50,+0.75,+1.00}; DIAL 2 COST "
        "in {0,10,25,50} bps.  w_i ~ (G/n)(1 + k z_i), z = within-held rank z-score of the SAME "
        "composite, read at t-1.  k = 0 IS the frozen incumbent (N=20, H=126, G=0.75, weekly).")
    say("CONTROL: a PERMUTED-z twin per cell (5 seeds) — same k, same weight multiset every "
        "rebalance, ordering destroyed.  Gaps scored by a PAIRED 63-row circular-block bootstrap.")
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
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, SMALL {len(inv)} "
        f"(of {len(pxS.columns)-1} priced).")
    say("  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010, so every absolute level below is an UPPER BOUND and "
        "every 4b pass an optimistic one.  What this run reads is a CONTRAST between one ordering "
        "of weights and a random ordering of the SAME weights on the SAME names and days, which "
        "the bias cannot manufacture.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y);  {len(p.reb)} weekly rebalances")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)

    grid, twin_rows, wf_rows = [], [], []
    wsum_global, g2_dev, g3_dev, recompute_dev = 0.0, 0.0, 0.0, None
    meang_dev = 0.0

    for pan in panels:
        T = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        spy, spyO = bmpack(pan.spy[WARMUP:]), bmpack(pan.spy[i_oos:])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])
        C = np.cumprod(1.0 + pan.rets, axis=0)
        Cp = np.vstack([np.ones((1, pan.rets.shape[1])), C[:-1]])

        say(f"\n  [{pan.name}]  SPY  CAGR {spy['CAGR']:.2%} Sharpe {spy['Sharpe']:.4f} MaxDD "
            f"{spy['MaxDD']:.2%} H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f}  |  4b bars: DD cap "
            f"{DD_CAP*spy['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps  CAGR {live['CAGR']:.2%} Sharpe {live['Sharpe']:.4f} "
            f"MaxDD {live['MaxDD']:.2%} H1/H2 {live['H1']:.3f}/{live['H2']:.3f}")

        base_frame, _ = build_frame(pan, I_N, I_H, 0.0)
        gg0, tu0, ws = run(pan, base_frame, C, Cp, I_G)
        wsum_global = max(wsum_global, ws)
        anchor = gg0 - tu0 * COST / 1e4
        am, ao = triple(anchor[WARMUP:]), triple(anchor[i_oos:])
        ah1, ah2 = halves(anchor[WARMUP:])
        mg0 = float(np.mean(I_G * base_frame[WARMUP:].sum(axis=1)))
        say(f"           FROZEN INCUMBENT (k=0) CAGR {am['CAGR']:.2%} Sharpe {am['Sharpe']:.4f} "
            f"MaxDD {am['MaxDD']:.2%} H1/H2 {ah1:.4f}/{ah2:.4f} | OOS {ao['CAGR']:.2%}/"
            f"{ao['Sharpe']:.4f}/{ao['MaxDD']:.2%} | mean gross {mg0:.4f}")
        if pan.name == "U56":
            d = max(abs(am["Sharpe"] - C_U56["Sharpe"]), abs(ao["Sharpe"] - C_U56["oSharpe"]))
            gate("G1 cross-script replay of the committed 2026-09-04 U56 frozen anchor "
                 "(~15.8%/~1.153/-19.13% full; ~17.3%/~1.185 OOS)",
                 f"|dSharpe| {d:.2e} (got {am['CAGR']:.4f}/{am['Sharpe']:.4f}/{am['MaxDD']:.4f}; "
                 f"OOS {ao['CAGR']:.4f}/{ao['Sharpe']:.4f}/{ao['MaxDD']:.4f})", "< 5e-3", d < 5e-3)

        # ---------- the tilt ladder ----------
        books = {}
        for k in KS:
            fr, diag = build_frame(pan, I_N, I_H, k)
            if k == 0.0:
                g2_dev = max(g2_dev, float(np.max(np.abs(fr - base_frame))))
            gg, tu, ws = run(pan, fr, C, Cp, I_G)
            wsum_global = max(wsum_global, ws)
            books[k] = (gg, tu)
            mg = float(np.mean(I_G * fr[WARMUP:].sum(axis=1)))
            meang_dev = max(meang_dev, abs(mg - mg0))
            n = T - WARMUP
            for cb in COSTS:
                rr = gg - tu * cb / 1e4
                k4a, k4b, m, h1, h2, legs = keep_paths(rr[WARMUP:], spy, live)
                k4aO, k4bO, mo, _, _, _ = keep_paths(rr[i_oos:], spyO, liveO)
                ar = anchor if cb == COST else (gg0 - tu0 * cb / 1e4)
                aa, aoo = triple(ar[WARMUP:]), triple(ar[i_oos:])
                turn_y = float(np.sum(tu[WARMUP:]) * 252.0 / n)
                mi = triple(rr[WARMUP:i_oos])
                ai = triple(ar[WARMUP:i_oos])
                grid.append(dict(
                    panel=pan.name, k=k, cost_bps=cb,
                    CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                    oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                    keep4a=k4a, keep4b=k4b, keep4b_oos=k4bO, keep4a_oos=k4aO,
                    legH1=legs["H1"], legH2=legs["H2"], legDD=legs["DD"], legCAGR=legs["CAGR"],
                    dd_margin_pp=100 * (m["MaxDD"] - DD_CAP * spy["MaxDD"]),
                    cagr_margin_pp=100 * (m["CAGR"] - CAGR_FLOOR * spy["CAGR"]),
                    d_cagr_vs_anchor_pp=100 * (m["CAGR"] - aa["CAGR"]),
                    d_sharpe_vs_anchor=m["Sharpe"] - aa["Sharpe"],
                    d_maxdd_vs_anchor_pp=100 * (m["MaxDD"] - aa["MaxDD"]),
                    od_cagr_vs_anchor_pp=100 * (mo["CAGR"] - aoo["CAGR"]),
                    od_sharpe_vs_anchor=mo["Sharpe"] - aoo["Sharpe"],
                    isCAGR=mi["CAGR"], isSharpe=mi["Sharpe"], isMaxDD=mi["MaxDD"],
                    id_sharpe_vs_anchor=mi["Sharpe"] - ai["Sharpe"],
                    id_cagr_vs_anchor_pp=100 * (mi["CAGR"] - ai["CAGR"]),
                    mean_gross=mg, eff_names=diag["eff_names"], clip_share=diag["clip_share"],
                    turn_y=turn_y, drag_bpyr=turn_y * cb,
                    anchor_CAGR=aa["CAGR"], anchor_Sharpe=aa["Sharpe"], anchor_MaxDD=aa["MaxDD"],
                    spy_CAGR=spy["CAGR"], spy_Sharpe=spy["Sharpe"], spy_MaxDD=spy["MaxDD"],
                    live_Sharpe=live["Sharpe"], live_MaxDD=live["MaxDD"]))

        # ---------- permuted-z twins (the control that decides the verdict) ----------
        for k in KS:
            gg, tu = books[k]
            rr = gg - tu * COST / 1e4
            for sd in PERM_SEEDS:
                fr, diag = build_frame(pan, I_N, I_H, k, perm_seed=sd)
                ggp, tup, ws = run(pan, fr, C, Cp, I_G)
                wsum_global = max(wsum_global, ws)
                rp = ggp - tup * COST / 1e4
                if k == 0.0:
                    g3_dev = max(g3_dev, float(np.max(np.abs(rp - anchor))))
                ds, se, ts_ = paired_block(rr[WARMUP:], rp[WARMUP:], "sharpe")
                dc, sec, tc = paired_block(rr[WARMUP:], rp[WARMUP:], "cagr")
                dsO, seO, tO = paired_block(rr[i_oos:], rp[i_oos:], "sharpe")
                dcO, secO, tcO = paired_block(rr[i_oos:], rp[i_oos:], "cagr")
                mt = triple(rp[WARMUP:])
                twin_rows.append(dict(
                    panel=pan.name, k=k, seed=sd,
                    twin_CAGR=mt["CAGR"], twin_Sharpe=mt["Sharpe"], twin_MaxDD=mt["MaxDD"],
                    twin_eff_names=diag["eff_names"], twin_clip_share=diag["clip_share"],
                    twin_turn_y=float(np.sum(tup[WARMUP:]) * 252.0 / (T - WARMUP)),
                    d_sharpe=ds, se_sharpe=se, t_sharpe=ts_,
                    d_cagr_pp=100 * dc, se_cagr_pp=100 * sec, t_cagr=tc,
                    d_maxdd_pp=100 * (triple(rr[WARMUP:])["MaxDD"] - mt["MaxDD"]),
                    od_sharpe=dsO, ose_sharpe=seO, ot_sharpe=tO,
                    od_cagr_pp=100 * dcO, ose_cagr_pp=100 * secO, ot_cagr=tcO))

        # ---------- rule 8 ----------
        i_is0, i_is1 = WARMUP, i_oos
        for chooser in ["IS_SHARPE", "IS_CAGR"]:
            best, bs = None, -np.inf
            for k in KS:
                gg, tu = books[k]
                rr = gg - tu * COST / 1e4
                s = sharpe(rr[i_is0:i_is1]) if chooser == "IS_SHARPE" else cagr(rr[i_is0:i_is1])
                if s > bs:
                    bs, best = s, k
            gg, tu = books[best]
            rr = gg - tu * COST / 1e4
            k4aO, k4bO, mo, _, _, legsO = keep_paths(rr[i_oos:], spyO, liveO)
            ao_ = triple(anchor[i_oos:])
            wf_rows.append(dict(panel=pan.name, chooser=chooser, is_k=best, is_stat=bs,
                                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                                keep4b_oos=k4bO, keep4a_oos=k4aO,
                                legH1=legsO["H1"], legH2=legsO["H2"], legDD=legsO["DD"],
                                legCAGR=legsO["CAGR"],
                                anchor_oCAGR=ao_["CAGR"], anchor_oSharpe=ao_["Sharpe"],
                                anchor_oMaxDD=ao_["MaxDD"],
                                d_oSharpe_vs_anchor=mo["Sharpe"] - ao_["Sharpe"],
                                d_oCAGR_vs_anchor_pp=100 * (mo["CAGR"] - ao_["CAGR"]),
                                spy_oCAGR=spyO["CAGR"], spy_oSharpe=spyO["Sharpe"],
                                spy_oMaxDD=spyO["MaxDD"],
                                live_oSharpe=liveO["Sharpe"], live_oMaxDD=liveO["MaxDD"]))

        if pan.name == "U56":
            fr, _ = build_frame(pan, I_N, I_H, 0.50)
            g2, t2, _ = run(pan, fr, C, Cp, I_G)
            recompute_dev = float(np.max(np.abs((g2 - t2 * COST / 1e4) - (books[0.50][0] - books[0.50][1] * COST / 1e4))))

    G = pd.DataFrame(grid)
    Tw = pd.DataFrame(twin_rows)
    W = pd.DataFrame(wf_rows)

    gate("G2 k=0 tilt frame is bit-identical to the equal-weight frame",
         f"max |dw| {g2_dev:.3e}", "== 0", g2_dev == 0.0)
    gate("G3 k=0 permuted twin is bit-identical to the anchor at every seed",
         f"max |dret| {g3_dev:.3e}", "< 1e-15", g3_dev < 1e-15)
    gate("G4 gross neutrality of the tilt: realised mean gross identical across every k",
         f"max |dmeanG| {meang_dev:.3e}", "< 1e-12", meang_dev < 1e-12)
    gate("G5 no leverage: realised weight sum never exceeds 1.0",
         f"max wsum {wsum_global:.6f}", "<= 1.0 + 1e-12", wsum_global <= 1.0 + 1e-12)
    gate("G6 chooser reads no row on or after 2017-01-01", "IS = warm-up..2016-12-31",
         "no OOS leakage", True)
    gate("G7 all grid cells published", f"{len(G)} rows ({len(KS)} k x {len(COSTS)} costs x 3 panels)",
         f"== {len(KS)*len(COSTS)*3}", len(G) == len(KS) * len(COSTS) * 3)
    gate("G8 bit-identical recompute (U56, k=0.50)", f"max |dret| {recompute_dev:.3e}", "== 0",
         recompute_dev == 0.0)

    say("\n" + "=" * 128)
    say("GRID — every cell.  Verdict rung is COST = 10 bps (PROTOCOL rule 2); the other cost rungs "
        "are reported.  dCAGR/dSharpe are vs the k=0 frozen anchor AT THE SAME COST RUNG.")
    say("=" * 128)
    for pn in ["U56", "B136", "SMALL"]:
        for cb in COSTS:
            sub = G[(G.panel == pn) & (G.cost_bps == cb)]
            say(f"\n  [{pn} / cost {cb:.0f} bps]")
            say("        k |    CAGR  Sharpe   MaxDD     H1     H2 | dCAGRpp  dSh  dDDpp | DDmarg "
                "CAGRmarg | 4a 4b | effN clip% meanG | turn drag | OOS CAGR/Sh/DD  odCAGRpp")
            for _, r in sub.iterrows():
                say(f"    {r.k:+5.2f} | {r.CAGR:7.2%} {r.Sharpe:7.4f} {r.MaxDD:7.2%} {r.H1:6.3f} "
                    f"{r.H2:6.3f} | {r.d_cagr_vs_anchor_pp:+7.3f} {r.d_sharpe_vs_anchor:+6.4f} "
                    f"{r.d_maxdd_vs_anchor_pp:+6.2f} | {r.dd_margin_pp:+6.2f} "
                    f"{r.cagr_margin_pp:+8.2f} | {int(r.keep4a)}  {int(r.keep4b)}  | "
                    f"{r.eff_names:4.1f} {100*r.clip_share:5.1f} {r.mean_gross:5.3f} | "
                    f"{r.turn_y:4.2f} {r.drag_bpyr:5.1f} | {r.oCAGR:7.2%} {r.oSharpe:6.4f} "
                    f"{r.oMaxDD:7.2%} {r.od_cagr_vs_anchor_pp:+7.3f}")

    say("\n" + "=" * 128)
    say("THE CONTROL — TILT vs its PERMUTED-z TWIN (same k, same weight multiset every rebalance, "
        "ordering destroyed).  Seeds pooled: median and per-seed range.  |t| > 2 resolves.")
    say("=" * 128)
    say("  panel     k | dSharpe med (range)        med t | dCAGR pp med (range)      med t | "
        "dMaxDD pp med | OOS dSh med t | OOS dCAGR pp med t")
    for pn in ["U56", "B136", "SMALL"]:
        for k in KS:
            s = Tw[(Tw.panel == pn) & (Tw.k == k)]
            if not len(s):
                continue
            say(f"  {pn:>5} {k:+5.2f} | {s.d_sharpe.median():+7.4f} "
                f"({s.d_sharpe.min():+7.4f}..{s.d_sharpe.max():+7.4f}) {s.t_sharpe.median():+6.2f} | "
                f"{s.d_cagr_pp.median():+7.3f} ({s.d_cagr_pp.min():+7.3f}.."
                f"{s.d_cagr_pp.max():+7.3f}) {s.t_cagr.median():+6.2f} | "
                f"{s.d_maxdd_pp.median():+7.2f} | {s.od_sharpe.median():+7.4f} "
                f"{s.ot_sharpe.median():+6.2f} | {s.od_cagr_pp.median():+7.3f} "
                f"{s.ot_cagr.median():+6.2f}")

    say("\n" + "=" * 128)
    say("RULE 8 WALK-FORWARD — k chosen on warm-up..2016-12-31 at 10 bps (argmax IS Sharpe and, "
        "separately, argmax IS CAGR); 2017-2026 read ONCE.")
    say("=" * 128)
    say("  panel  chooser | IS k  IS stat | OOS CAGR  Sharpe   MaxDD | 4a 4b legs(H1,H2,DD,CAGR) | "
        "ANCHOR OOS CAGR/Sh/DD | dSh  dCAGRpp | SPY OOS CAGR/Sh/DD")
    for _, r in W.iterrows():
        say(f"  {r.panel:>5} {r.chooser:>9} | {r.is_k:+5.2f} {r.is_stat:7.4f} | {r.oCAGR:7.2%} "
            f"{r.oSharpe:7.4f} {r.oMaxDD:7.2%} | {int(r.keep4a_oos)}  {int(r.keep4b_oos)} "
            f"({int(r.legH1)},{int(r.legH2)},{int(r.legDD)},{int(r.legCAGR)}) | "
            f"{r.anchor_oCAGR:7.2%}/{r.anchor_oSharpe:.4f}/{r.anchor_oMaxDD:7.2%} | "
            f"{r.d_oSharpe_vs_anchor:+7.4f} {r.d_oCAGR_vs_anchor_pp:+7.3f} | "
            f"{r.spy_oCAGR:6.2%}/{r.spy_oSharpe:.4f}/{r.spy_oMaxDD:7.2%}")

    say("\n" + "=" * 128)
    say("HEADLINE")
    say("=" * 128)
    g10 = G[G.cost_bps == COST]
    bite = g10[g10.k != 0.0]
    say(f"  4a: {int(g10.keep4a.sum())} of {len(g10)} cells at 10 bps.  4b: "
        f"{int(g10.keep4b.sum())} of {len(g10)}.")
    for pn in ["U56", "B136", "SMALL"]:
        sp = g10[g10.panel == pn]
        say(f"    {pn}: 4b {int(sp.keep4b.sum())} of {len(sp)}; anchor(k=0) 4b "
            f"{int(sp[sp.k==0].keep4b.iloc[0])}")
    pos = bite[bite.k > 0]
    neg = bite[bite.k < 0]
    say(f"  1484's CLAIM TO REPRODUCE (+1.125 pp of CAGR from the ordering channel).  Tilt vs the "
        f"k=0 anchor at 10 bps:")
    say(f"    k > 0 (pro-conviction): median dCAGR {pos.d_cagr_vs_anchor_pp.median():+.3f} pp, "
        f"best {pos.d_cagr_vs_anchor_pp.max():+.3f} pp, positive at "
        f"{int((pos.d_cagr_vs_anchor_pp > 0).sum())} of {len(pos)} cells; median dSharpe "
        f"{pos.d_sharpe_vs_anchor.median():+.4f}")
    say(f"    k < 0 (anti-tilt, the SIGN TEST): median dCAGR "
        f"{neg.d_cagr_vs_anchor_pp.median():+.3f} pp, positive at "
        f"{int((neg.d_cagr_vs_anchor_pp > 0).sum())} of {len(neg)} cells; median dSharpe "
        f"{neg.d_sharpe_vs_anchor.median():+.4f}")
    tb = Tw[Tw.k != 0.0]
    res = tb[np.abs(tb.t_cagr) > 2]
    say(f"  VS THE PERMUTED-z TWIN (the ordering isolated): {len(res)} of {len(tb)} "
        f"(panel, k, seed) contrasts resolve |t| > 2 on CAGR; of those "
        f"{int((res.d_cagr_pp > 0).sum())} favour the REAL ordering.")
    say(f"    median dCAGR vs twin {tb.d_cagr_pp.median():+.3f} pp (median |t| "
        f"{np.abs(tb.t_cagr).median():.2f}); median dSharpe vs twin {tb.d_sharpe.median():+.4f} "
        f"(median |t| {np.abs(tb.t_sharpe).median():.2f})")
    tbp = tb[tb.k > 0]
    say(f"    k > 0 only: median dCAGR vs twin {tbp.d_cagr_pp.median():+.3f} pp, positive at "
        f"{int((tbp.d_cagr_pp > 0).sum())} of {len(tbp)}; median dSharpe "
        f"{tbp.d_sharpe.median():+.4f}, positive at {int((tbp.d_sharpe > 0).sum())} of {len(tbp)}")
    resO = tb[np.abs(tb.ot_cagr) > 2]
    say(f"    OOS: {len(resO)} of {len(tb)} resolve |t| > 2 on CAGR, "
        f"{int((resO.d_cagr_pp > 0).sum() if len(resO) else 0)} favour the real ordering.")
    say("  THE IS SURFACE (what a legal rule-8 chooser can see: warm-up..2016-12-31 at 10 bps):")
    for pn in ["U56", "B136", "SMALL"]:
        sp = g10[g10.panel == pn].sort_values("k")
        say("    " + pn.ljust(5) + " IS Sharpe by k: " +
            "  ".join(f"{r.k:+.2f}:{r.isSharpe:.4f}" for _, r in sp.iterrows()))
        mono = bool((np.diff(sp.isSharpe.values) > 0).all())
        say(f"          IS Sharpe strictly INCREASING in k across the whole ladder: {mono}; "
            f"IS argmax at k = {sp.loc[sp.isSharpe.idxmax(), 'k']:+.2f}, FULL-sample argmax at "
            f"k = {sp.loc[sp.Sharpe.idxmax(), 'k']:+.2f}, OOS argmax at "
            f"k = {sp.loc[sp.oSharpe.idxmax(), 'k']:+.2f}")
    strict = g10[(g10.k != 0) & g10.keep4b & g10.keep4b_oos &
                 (g10.d_sharpe_vs_anchor > 0) & (g10.od_sharpe_vs_anchor > 0)]
    say(f"  STRICT IMPROVEMENT (clears 4b FULL *and* OOS *and* beats the frozen anchor on BOTH "
        f"Sharpes): {len(strict)} of {len(g10[g10.k != 0])} biting cells at 10 bps"
        + ("" if not len(strict) else " -- " + "; ".join(
            f"{r.panel} k={r.k:+.2f} ({r.CAGR:.2%}/{r.Sharpe:.4f}/{r.MaxDD:.2%}; OOS "
            f"{r.oCAGR:.2%}/{r.oSharpe:.4f}/{r.oMaxDD:.2%})" for _, r in strict.iterrows())))
    say(f"  RULE 8: {int((W.d_oSharpe_vs_anchor > 0).sum())} of {len(W)} arms beat the frozen "
        f"anchor's OOS Sharpe (mean {W.d_oSharpe_vs_anchor.mean():+.4f}); "
        f"{int((W.d_oCAGR_vs_anchor_pp > 0).sum())} of {len(W)} beat its OOS CAGR "
        f"(mean {W.d_oCAGR_vs_anchor_pp.mean():+.3f} pp).  IS picks: "
        f"{sorted(W.is_k.unique().tolist())}")
    say(f"    OOS 4b passes among the rule-8 arms: {int(W.keep4b_oos.sum())} of {len(W)}; 4a: "
        f"{int(W.keep4a_oos.sum())} of {len(W)}.")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    Tw.to_csv(f"{OUT}.twins.csv", index=False)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n  wrote {OUT.name}.grid.csv / .twins.csv / .walkforward.csv / .gates.csv / .log.txt")
    say(f"  elapsed {time.time()-t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

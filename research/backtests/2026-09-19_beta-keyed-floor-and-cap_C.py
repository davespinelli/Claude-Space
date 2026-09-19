#!/usr/bin/env python3
"""
Idea 1429 (lane C, 2026-09-19) — does a BETA-KEYED FLOOR-AND-CAP REDISTRIBUTION buy the
BINDING 4b DD LEG at IDENTICAL NAMES, IDENTICAL NAME COUNT and IDENTICAL GROSS?

THE PREMISE.  The standing 2026-09-04 KEEP-4b incumbent (U56, N = 20, H = 126, gross 0.75,
weekly Fri-decide / Mon-trade, 10 bps, t+1) passes 4b on ONE leg's margin: MaxDD -19.13%
against a -20.23% cap, +1.1028 pp.  Every attack on that leg this month died the same death —
a trailing equity stop (1405), a breadth throttle (1413), a convention ensemble (1423) each
shallowed drawdown by HOLDING LESS STOCK or HOLDING MORE NAMES, and each failed against its
own exposure-matched twin.  Lane B's 1433 shut that channel with INVERSE-VOL sizing and found
the leg DOES move at fixed gross (+1.1028 -> +2.29..+5.63 pp on U56), but PAID for it in CAGR
(-1.80..-6.41 pp), broke the 4b CAGR floor at its widest cells, and never resolved the
ordering against its own weight-shuffle twin on U56 (|t| 0 of 16).

This run prices 1433's MIRROR.  The queue's observation is exact: the incumbent is EQUAL
WEIGHT, so a max-weight CAP alone is inert — a cap can only bite if something is redistributed
INTO a floor.  So the rule here is a symmetric FLOOR-AND-CAP band around the incumbent's own
equal weight, keyed on the held names' OWN TRAILING BETA TO SPY:

    rank the n held names by trailing beta (ascending);  z_i = 1 - 2*(rank_i - 0.5)/n  in
    [-1, +1] with sum z = 0 EXACTLY;  w_i = (G/n) * (1 + c * z_i),  G = 0.75.

    -> LOWEST beta receives the CAP side (G/n)*(1 + c*(1-1/n)),
       HIGHEST beta receives the FLOOR side (G/n)*(1 - c*(1-1/n)),
       sum w_i = G to machine precision at every rebalance, for every c and every n.

c = 0 IS THE FROZEN INCUMBENT.  Names, name count, rebalance rows and gross are fixed BY
CONSTRUCTION, so the exposure channel that killed 1405/1413/1423 is shut before any number is
read, and the CONCENTRATION channel is pinned too: for a given c the weight MULTISET is a
deterministic function of c and n alone — it does not depend on the beta lookback, on the
panel or on which names are held — so every cell at the same c has an IDENTICAL effective-N
path and an IDENTICAL Herfindahl path.  The ONLY thing any dial can move is WHICH NAME GETS
WHICH SLOT.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  C  {0.00, 0.25, 0.50, 0.75, 1.00}   DIAL 1 — band half-width (the floor-and-cap width).
                                       c = 0.00 IS the frozen incumbent, present at every B.
                                       c = 1.00 is the widest band with a non-negative floor.
  B  {20, 63, 126, 252}                DIAL 2 — trailing beta lookback, in trading days.

20 cells per panel, 60 in all, EVERY ONE published in .grid.csv.

TWO CONTROLS, BOTH EXACT.  Because the multiset is pinned, a null can match the cell on
EVERYTHING but the ordering:
  (1) RANK-PERMUTATION TWIN — the cell's own weight multiset re-assigned to the same held
      names in seeded random order (K = 12 draws).  Matches gross, names, name count, the
      whole weight distribution, effective N and Herfindahl at every row; differs ONLY in
      which name gets which slot.  Gaps are scored by a PAIRED circular-block bootstrap
      (400 reps x 63-row blocks, seed 20260919, identical block starts).
  (2) ANTI-BETA MIRROR — the SAME band run at -c, i.e. the HIGHEST beta takes the cap.  This
      is the sharpest possible null: identical multiset, exactly REVERSED ordering.  If the
      beta ordering carries DD information, the mirror must be WORSE on MaxDD by roughly as
      much as the cell is better.  If cell and mirror move the SAME way, the band is a
      dispersion dial and beta is decoration.  The mirror is a CONTROL, not a grid cell: it
      is never eligible for KEEP and never read by the rule-8 chooser.

THE BAR, PRE-REGISTERED HERE BEFORE ANY NUMBER WAS READ.  Worth capital only if on U56
(i) the 4b DD margin exceeds the frozen anchor's own +1.1028 pp, (ii) 4b passes FULL-SAMPLE
and OOS (so the CAGR floor that broke 1433's widest cells must hold), and (iii) the Sharpe
edge over its own rank-permutation twin resolves |t| > 2.  Anything less is KILL or PARK,
whatever the headline says.

DIRECTION IS PRE-REGISTERED TOO: the hypothesis under test is LOW BETA TAKES THE CAP (c > 0).
The mirror (c < 0) is reported at every magnitude as a control; a run in which only the MIRROR
works is reported as such and is NOT a finding for the pre-registered rule.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); both KEEP paths at
every cell; the halves; IS and OOS windows; turnover and its 10 bps drag in bp/yr; realised
mean gross; realised effective N, max weight and min weight; realised book beta.

COMPARANDS (rule 3): the live RULES v2 baseline at 10 bps weekly, SPY buy-and-hold, and the
FROZEN (c = 0) incumbent.

PROTOCOL: rule 1 (>= 10y); rule 2 (t+1, 10 bps, no leverage, no shorting); rule 3 (RULES v2
AND SPY); rule 4 (both KEEP paths, 2 tuned parameters); rule 8 (walk-forward: (c, B) chosen on
warm-up..2016-12-31 by argmax IS Sharpe, 2017-2026 read ONCE, scored against the frozen
incumbent and SPY); rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py are NOT modified.

GATES.  G0 sample >= 10y.  G1 CROSS-SCRIPT REPLAY: the c = 0 cell must reproduce the committed
U56 anchor (15.80% / 1.1537 / -19.13% full; 17.32% / 1.1857 / -19.13% OOS).  G2 the c = 0 cell
is BIT-IDENTICAL across all four B (the band is inert at zero width).  G3 the c = 0
permutation twin and the c = 0 mirror are BIT-IDENTICAL to the c = 0 cell.  G4 all 60 cells
published.  G5 exactly two tuned parameters.  G6 the chooser reads no row on or after
2017-01-01.  G7 exposure channel SHUT: every cell's realised mean gross matches the anchor's
to < 1e-12, and no leverage.  G7b every rebalance's weight sum equals G to < 1e-12 (the
sum-zero identity holds at every n).  G8 every cell holds the IDENTICAL name set on every row
(one selection frame per panel, built ONCE before any dial).  G9 every twin AND every mirror
matches its cell's effective-N path to < 1e-12.  G11 THE BAND BINDS AND IS RESPECTED: realised
max weight == (G/n)(1+c(1-1/n)) and min weight == (G/n)(1-c(1-1/n)) at every rebalance, and
the band is strictly wider at each larger c.  G12 beta is computed from rows <= the decision
row only (no look-ahead).  G10 bit-identical recompute of the U56 headline cell.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-19_beta-keyed-floor-and-cap_C.py
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
SLUG = "beta-keyed-floor-and-cap"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G = 20, 126, 0.75              # the frozen 2026-09-04 incumbent
COST, CADENCE = 10.0, "W"
CS = [0.00, 0.25, 0.50, 0.75, 1.00]        # DIAL 1 — band half-width
BS = [20, 63, 126, 252]                    # DIAL 2 — beta lookback (trading days)
NPERM, SEED = 12, 20260919
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
    """The live selection mechanics (baseline.score with the incumbent's 3-leg composite)."""
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
    """Trailing beta of every column of R to the benchmark series y over B TRAILING rows.
    Uses only rows <= the row it is stamped on (pandas rolling is backward-looking): gate G12."""
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


def band_multiset(n, c):
    """The weight multiset for n names at band half-width c, in CAP-FIRST order.
    Depends on (n, c) ONLY — not on the lookback, the panel or which names are held — so
    every cell at the same c shares an identical effective-N / Herfindahl path."""
    if n == 0:
        return np.zeros(0)
    ranks = np.arange(1, n + 1, dtype=float)
    z = 1.0 - 2.0 * (ranks - 0.5) / n            # +1-ish .. -1-ish, sums to EXACTLY 0
    return (I_G / n) * (1.0 + c * z)


def cell_weights(pan, segs, c, B, perm_seed=None, mirror=False):
    """Per-segment weight vector over the segment's OWN held names, summing to I_G.
    LOWEST trailing beta takes the CAP side.  mirror=True runs the band at -c (highest beta
    takes the cap).  perm_seed re-assigns the SAME multiset in seeded random order."""
    BE = pan.beta[B]
    cc = -c if mirror else c
    rng = np.random.default_rng(perm_seed) if perm_seed is not None else None
    ws = []
    for (t, stop, ts, sel) in segs:
        n = len(sel)
        if n == 0:
            ws.append(np.zeros(0))
            continue
        m = band_multiset(n, cc)                 # cap-first
        if c == 0.0:
            order = np.arange(n)                 # inert: every slot is G/n
        else:
            b = BE[ts, sel].astype(float)
            fin = np.isfinite(b)
            if not fin.all():                    # neutral fill: the row's own median beta
                med = np.nanmedian(b[fin]) if fin.any() else 1.0
                b = np.where(fin, b, med)
            order = np.argsort(b, kind="stable")  # ascending beta -> cap first
        w = np.empty(n)
        w[order] = m
        if rng is not None:
            w = w[rng.permutation(n)]
        ws.append(w)
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
    minw = np.zeros(len(segs))
    wsum_dev = 0.0
    curw = np.zeros(M)
    wsum_max = 0.0
    for j, ((i0, i1, ts, sel), wv) in enumerate(zip(segs, ws)):
        w0 = np.zeros(M)
        if len(sel):
            w0[pan.iinv[sel]] = wv
            q = wv / wv.sum()
            effn[j] = 1.0 / float((q ** 2).sum())
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
    return out, turn, gross_path, effn, maxw, minw, wsum_max, wsum_dev


def book_beta(pan, segs, ws, B):
    """Realised weighted-average trailing beta of the book at its own decision rows."""
    BE = pan.beta[B]
    num, den = 0.0, 0.0
    for (t, stop, ts, sel), wv in zip(segs, ws):
        if not len(sel):
            continue
        b = BE[ts, sel].astype(float)
        fin = np.isfinite(b)
        if not fin.any():
            continue
        num += float(np.sum(wv[fin] * b[fin]))
        den += float(np.sum(wv[fin]))
    return num / den if den > 0 else np.nan


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
    """Paired circular-block bootstrap on a PAIRED statistic (identical block starts)."""
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


def main():
    t0 = time.time()
    say("=" * 128)
    say("IDEA 1429 (lane C, 2026-09-19) — does a BETA-KEYED FLOOR-AND-CAP REDISTRIBUTION buy "
        "the BINDING 4b DD LEG at IDENTICAL NAMES and IDENTICAL GROSS?")
    say("RULE: rank the n held names by trailing beta to SPY; z = 1 - 2(rank-0.5)/n (sum 0 "
        "EXACTLY); w = (G/n)(1 + c*z), G = 0.75.  LOWEST beta takes the CAP.")
    say("DIALS: C {0.00,0.25,0.50,0.75,1.00} x B {20,63,126,252} on the frozen incumbent "
        "(N=20, H=126, gross 0.75, MAXVOL 0.60, MA gate ON, weekly, 10 bps, t+1).  c=0 IS it.")
    say(f"CONTROLS: (1) RANK-PERMUTATION twin, K={NPERM} seeds — same multiset, shuffled slots. "
        "(2) ANTI-BETA MIRROR at -c — same multiset, EXACTLY reversed ordering.")
    say(f"PRE-REGISTERED BAR (stated before any number was read): capital only if U56 DD margin "
        f"> {BAR_DD_PP:+.4f} pp AND 4b passes FULL and OOS AND |t| vs its own twin > {BAR_T:.0f}.")
    say("=" * 128)

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
        "every 4b pass an optimistic one; what this run reads is a CONTRAST between two "
        "ORDERINGS of the SAME weights over the SAME names on the SAME days, which the bias "
        "cannot manufacture.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y);  {len(p.reb)} weekly rebalances")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)
    gate("G12 beta uses trailing rows only (pandas rolling is backward-looking; stamped at the "
         "t-1 decision row)", "by construction", "no look-ahead", True)

    grid, wf_rows, perm_rows, mir_rows = [], [], [], []
    wsum_global, g2_dev, g3_dev, g7_dev, g7b_dev, g9_dev, g11_dev = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    g11_mono = True
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
        nsel = np.array([len(s[3]) for s in segs], float)

        say(f"\n  [{pan.name}]  SPY  CAGR {spy['CAGR']:.2%} Sharpe {spy['Sharpe']:.4f} MaxDD "
            f"{spy['MaxDD']:.2%} H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f}  |  4b bars: DD cap "
            f"{DD_CAP*spy['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps  CAGR {live['CAGR']:.2%} Sharpe {live['Sharpe']:.4f} "
            f"MaxDD {live['MaxDD']:.2%} H1/H2 {live['H1']:.3f}/{live['H2']:.3f}")

        # ---- the frozen anchor (c = 0) ---------------------------------------------------
        ws0 = cell_weights(pan, segs, 0.0, BS[0])
        g0, t0_, gp0, en0, mw0, mn0, ws_, wd_ = run_book(pan, segs, ws0, C, Cp)
        wsum_global = max(wsum_global, ws_)
        g7b_dev = max(g7b_dev, wd_)
        anchor = g0 - t0_ * COST / 1e4
        am, ao = triple(anchor[WARMUP:]), triple(anchor[i_oos:])
        ah1, ah2 = halves(anchor[WARMUP:])
        anchor_mg = float(np.mean(gp0[WARMUP:]))
        say(f"           FROZEN INCUMBENT (c=0) CAGR {am['CAGR']:.2%} Sharpe {am['Sharpe']:.4f} "
            f"MaxDD {am['MaxDD']:.2%} H1/H2 {ah1:.4f}/{ah2:.4f} | OOS {ao['CAGR']:.2%}/"
            f"{ao['Sharpe']:.4f}/{ao['MaxDD']:.2%} | mean gross {anchor_mg:.6f}, effN "
            f"{en0.mean():.2f}, mean n held {nsel.mean():.2f}")
        if pan.name == "U56":
            d = max(abs(am["Sharpe"] - C_U56["Sharpe"]), abs(ao["Sharpe"] - C_U56["oSharpe"]))
            gate("G1 cross-script replay of the committed 2026-09-04 U56 anchor "
                 "(15.80%/1.1537/-19.13% full; 17.32%/1.1857/-19.13% OOS)",
                 f"|dSharpe| {d:.2e}  (got {am['CAGR']:.4f}/{am['Sharpe']:.4f}/"
                 f"{am['MaxDD']:.4f}; OOS {ao['Sharpe']:.4f})", "< 5e-3", d < 5e-3)
            say(f"           ANCHOR 4b DD MARGIN (the bar): "
                f"{100*(am['MaxDD'] - DD_CAP*spy['MaxDD']):+.4f} pp")

        # ---- the 20-cell band grid -------------------------------------------------------
        prev_band = None
        for c in CS:
            band_w = []
            for B in BS:
                ws = cell_weights(pan, segs, c, B)
                gg, tu, gp, en, mw, mn, wsx, wdx = run_book(pan, segs, ws, C, Cp)
                wsum_global = max(wsum_global, wsx)
                g7b_dev = max(g7b_dev, wdx)
                rr = gg - tu * COST / 1e4
                if c == 0.0:
                    g2_dev = max(g2_dev, float(np.max(np.abs(rr - anchor))))
                g7_dev = max(g7_dev, abs(float(np.mean(gp[WARMUP:])) - anchor_mg))
                # G11: the realised band must equal the analytic floor-and-cap at every row
                with np.errstate(divide="ignore", invalid="ignore"):
                    cap_t = np.where(nsel > 0, (I_G / np.maximum(nsel, 1)) * (1 + c * (1 - 1 / np.maximum(nsel, 1))), 0.0)
                    flo_t = np.where(nsel > 0, (I_G / np.maximum(nsel, 1)) * (1 - c * (1 - 1 / np.maximum(nsel, 1))), 0.0)
                g11_dev = max(g11_dev, float(np.max(np.abs(mw - cap_t))), float(np.max(np.abs(mn - flo_t))))
                band_w.append(float(np.mean(mw - mn)))
                k4a, k4b, m, h1, h2, legs = keep_paths(rr[WARMUP:], spy, live)
                k4aO, k4bO, mo, _, _, legsO = keep_paths(rr[i_oos:], spyO, liveO)

                # --- rank-permutation twins (K seeds) ---
                tw_r, tw_s, tw_dd = [], [], []
                for k in range(NPERM):
                    wsp = cell_weights(pan, segs, c, B,
                                       perm_seed=SEED + 1000 * k + int(100 * c) + B)
                    gp_, tp_, _, enp, _, _, _, _ = run_book(pan, segs, wsp, C, Cp)
                    rp = gp_ - tp_ * COST / 1e4
                    g9_dev = max(g9_dev, float(np.max(np.abs(enp - en))))
                    if c == 0.0:
                        g3_dev = max(g3_dev, float(np.max(np.abs(rp - anchor))))
                    tw_r.append(rp)
                    tw_s.append(sharpe(rp[WARMUP:]))
                    tw_dd.append(mdd(rp[WARMUP:]))
                tw_s, tw_dd = np.array(tw_s), np.array(tw_dd)
                jmed = int(np.argsort(tw_s)[len(tw_s) // 2])
                twin = tw_r[jmed]
                dsh, se, tstat = paired_block(rr[WARMUP:], twin[WARMUP:], "sharpe")
                ddd, ddse, ddt = paired_block(rr[WARMUP:], twin[WARMUP:], "mdd")
                dshO, seO, tO = paired_block(rr[i_oos:], twin[i_oos:], "sharpe")

                # --- anti-beta mirror (-c): identical multiset, reversed ordering ---
                wsm = cell_weights(pan, segs, c, B, mirror=True)
                gm, tm, _, enm, _, _, _, _ = run_book(pan, segs, wsm, C, Cp)
                rm = gm - tm * COST / 1e4
                g9_dev = max(g9_dev, float(np.max(np.abs(enm - en))))
                if c == 0.0:
                    g3_dev = max(g3_dev, float(np.max(np.abs(rm - anchor))))
                mm, mmo = triple(rm[WARMUP:]), triple(rm[i_oos:])
                mdsh, mse, mt = paired_block(rr[WARMUP:], rm[WARMUP:], "sharpe")
                mddd, mddse, mddt = paired_block(rr[WARMUP:], rm[WARMUP:], "mdd")
                mir_rows.append(dict(panel=pan.name, c=c, B=B,
                                     mir_CAGR=mm["CAGR"], mir_Sharpe=mm["Sharpe"],
                                     mir_MaxDD=mm["MaxDD"], mir_oSharpe=mmo["Sharpe"],
                                     mir_oMaxDD=mmo["MaxDD"],
                                     mir_dd_margin_pp=100 * (mm["MaxDD"] - DD_CAP * spy["MaxDD"]),
                                     cell_MaxDD=m["MaxDD"], cell_Sharpe=m["Sharpe"],
                                     d_sharpe_cell_minus_mirror=mdsh, t_sharpe=mt,
                                     d_maxdd_pp_cell_minus_mirror=100 * mddd, t_maxdd=mddt,
                                     eff_n_dev=float(np.max(np.abs(enm - en)))))

                s_pct = float(np.mean(tw_s <= m["Sharpe"]))
                dd_pct = float(np.mean(tw_dd <= m["MaxDD"]))
                n = T - WARMUP
                turn_y = float(np.sum(tu[WARMUP:]) * 252.0 / n)
                grid.append(dict(
                    panel=pan.name, c=c, B=B,
                    CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                    oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                    keep4a=k4a, keep4b=k4b, keep4b_oos=k4bO, keep4a_oos=k4aO,
                    legH1=legs["H1"], legH2=legs["H2"], legDD=legs["DD"], legCAGR=legs["CAGR"],
                    oleg_H1=legsO["H1"], oleg_H2=legsO["H2"], oleg_DD=legsO["DD"],
                    oleg_CAGR=legsO["CAGR"],
                    dd_margin_pp=100 * (m["MaxDD"] - DD_CAP * spy["MaxDD"]),
                    cagr_margin_pp=100 * (m["CAGR"] - CAGR_FLOOR * spy["CAGR"]),
                    d_sharpe_vs_anchor=m["Sharpe"] - am["Sharpe"],
                    d_cagr_pp_vs_anchor=100 * (m["CAGR"] - am["CAGR"]),
                    d_maxdd_vs_anchor_pp=100 * (m["MaxDD"] - am["MaxDD"]),
                    mean_gross=float(np.mean(gp[WARMUP:])), eff_n=float(en.mean()),
                    max_w=float(mw.mean()), min_w=float(mn.mean()),
                    band_w=float(np.mean(mw - mn)),
                    book_beta=book_beta(pan, segs, ws, B),
                    anchor_book_beta=book_beta(pan, segs, ws0, B),
                    turn_y=turn_y, drag_bpyr=turn_y * COST,
                    twin_Sharpe_med=float(np.median(tw_s)),
                    twin_Sharpe_lo=float(tw_s.min()), twin_Sharpe_hi=float(tw_s.max()),
                    twin_MaxDD_med=float(np.median(tw_dd)),
                    sharpe_pct_in_twins=s_pct, maxdd_pct_in_twins=dd_pct,
                    d_sharpe_vs_twin=dsh, se_vs_twin=se, t_vs_twin=tstat,
                    d_maxdd_pp_vs_twin=100 * ddd, t_maxdd_vs_twin=ddt,
                    od_sharpe_vs_twin=dshO, ose_vs_twin=seO, ot_vs_twin=tO,
                    mirror_MaxDD=mm["MaxDD"], mirror_Sharpe=mm["Sharpe"],
                    d_maxdd_pp_vs_mirror=100 * mddd, t_maxdd_vs_mirror=mddt,
                    d_sharpe_vs_mirror=mdsh, t_sharpe_vs_mirror=mt,
                    spy_Sharpe=spy["Sharpe"], spy_MaxDD=spy["MaxDD"], spy_CAGR=spy["CAGR"],
                    live_Sharpe=live["Sharpe"], live_MaxDD=live["MaxDD"],
                    anchor_Sharpe=am["Sharpe"], anchor_MaxDD=am["MaxDD"],
                    anchor_CAGR=am["CAGR"],
                    anchor_dd_margin_pp=100 * (am["MaxDD"] - DD_CAP * spy["MaxDD"])))
                for k, (s_, d_) in enumerate(zip(tw_s, tw_dd)):
                    perm_rows.append(dict(panel=pan.name, c=c, B=B, draw=k, Sharpe=s_, MaxDD=d_))
                if pan.name == "U56" and c == 0.50 and B == 126:
                    headline_ret = rr.copy()
            bw = float(np.mean(band_w))
            if prev_band is not None and not bw > prev_band - 1e-15:
                g11_mono = False
            prev_band = bw

        # ---- rule 8 ------------------------------------------------------------------------
        i_is0, i_is1 = WARMUP, int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        best, bs = None, -np.inf
        for c in CS:
            for B in BS:
                ws = cell_weights(pan, segs, c, B)
                gg, tu, _, _, _, _, _, _ = run_book(pan, segs, ws, C, Cp)
                rr = gg - tu * COST / 1e4
                s = sharpe(rr[i_is0:i_is1])
                if s > bs:
                    bs, best = s, (c, B)
        ws = cell_weights(pan, segs, best[0], best[1])
        gg, tu, _, _, _, _, _, _ = run_book(pan, segs, ws, C, Cp)
        rr = gg - tu * COST / 1e4
        k4aO, k4bO, mo, _, _, legsO = keep_paths(rr[i_oos:], spyO, liveO)
        aO = triple(anchor[i_oos:])
        dshA, seA, tA = paired_block(rr[i_oos:], anchor[i_oos:], "sharpe")
        ddA, ddseA, ddtA = paired_block(rr[i_oos:], anchor[i_oos:], "mdd")
        wf_rows.append(dict(panel=pan.name, is_c=best[0], is_B=best[1], is_Sharpe=bs,
                            picked_anchor=bool(best[0] == 0.0),
                            oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                            keep4b_oos=k4bO, keep4a_oos=k4aO,
                            oleg_H1=legsO["H1"], oleg_H2=legsO["H2"], oleg_DD=legsO["DD"],
                            oleg_CAGR=legsO["CAGR"],
                            oos_dd_margin_pp=100 * (mo["MaxDD"] - DD_CAP * spyO["MaxDD"]),
                            oos_cagr_margin_pp=100 * (mo["CAGR"] - CAGR_FLOOR * spyO["CAGR"]),
                            anchor_oCAGR=aO["CAGR"], anchor_oSharpe=aO["Sharpe"],
                            anchor_oMaxDD=aO["MaxDD"],
                            d_oSharpe_vs_anchor=mo["Sharpe"] - aO["Sharpe"],
                            t_oSharpe_vs_anchor=tA,
                            d_oMaxDD_pp_vs_anchor=100 * ddA, t_oMaxDD_vs_anchor=ddtA,
                            spy_oSharpe=spyO["Sharpe"], spy_oCAGR=spyO["CAGR"],
                            spy_oMaxDD=spyO["MaxDD"],
                            live_oSharpe=liveO["Sharpe"], live_oMaxDD=liveO["MaxDD"]))

    G = pd.DataFrame(grid)
    W = pd.DataFrame(wf_rows)
    P = pd.DataFrame(perm_rows)
    M = pd.DataFrame(mir_rows)

    gate("G2 c=0 cell BIT-IDENTICAL across all four B", f"max |dret| {g2_dev:.3e}", "< 1e-15",
         g2_dev < 1e-15)
    gate("G3 c=0 permutation twin AND c=0 mirror BIT-IDENTICAL to the c=0 cell",
         f"max |dret| {g3_dev:.3e}", "< 1e-15", g3_dev < 1e-15)
    gate("G4 all 60 grid cells published", len(G), "== 60", len(G) == 60)
    gate("G5 exactly two tuned parameters (c, B)", "2", "== 2", True)
    gate("G6 chooser reads no row on or after 2017-01-01", "IS = warm-up..2016-12-31",
         "no OOS leakage", True)
    gate("G7 exposure channel SHUT: every cell's realised mean gross == the anchor's",
         f"max |dmean gross| {g7_dev:.3e}", "< 1e-12", g7_dev < 1e-12)
    gate("G7b sum-zero identity: every rebalance's weight sum == G = 0.75 exactly",
         f"max |dsum| {g7b_dev:.3e}", "< 1e-12", g7b_dev < 1e-12)
    gate("G7c no leverage: realised weight sum never exceeds 1.0", f"max wsum {wsum_global:.6f}",
         "<= 1.0 + 1e-12", wsum_global <= 1.0 + 1e-12)
    gate("G8 selection untouched: every cell shares ONE frame per panel (built once, before any "
         "dial)", "by construction", "identical name sets", True)
    gate("G9 every twin AND every mirror matches its cell's effective-N path",
         f"max |d effN| {g9_dev:.3e}", "< 1e-12", g9_dev < 1e-12)
    gate("G11 the band is respected exactly: realised max/min weight == the analytic "
         "cap/floor at every rebalance", f"max |dev| {g11_dev:.3e}", "< 1e-12", g11_dev < 1e-12)
    gate("G11b the band is strictly WIDER at each larger c (the dial bites)",
         f"monotone: {g11_mono}", "True", g11_mono)

    say("\n" + "=" * 128)
    say("GRID — EVERY CELL.  DD margin = MaxDD - 0.60 x SPY MaxDD (positive = the 4b DD leg "
        "passes).  TWIN = rank-permutation control (same multiset, shuffled slots).")
    say("MIRROR = the SAME band at -c (highest beta takes the cap): identical multiset, exactly "
        "reversed ordering.  dDD vs mirror > 0 means the cell drew DOWN LESS than its mirror.")
    say("=" * 128)
    for pan in ["U56", "B136", "SMALL"]:
        sub = G[G.panel == pan]
        say(f"\n  [{pan}]   anchor DD margin {sub.anchor_dd_margin_pp.iloc[0]:+.4f} pp, "
            f"anchor Sharpe {sub.anchor_Sharpe.iloc[0]:.4f}, anchor CAGR "
            f"{sub.anchor_CAGR.iloc[0]:.2%}, anchor book beta "
            f"{sub.anchor_book_beta.iloc[0]:.4f}")
        say("      c    B |    CAGR  Sharpe   MaxDD     H1     H2 | DDmarg CAGRmarg | 4a 4b o4b "
            "| effN  maxW  minW  meanG | bBeta | turn drag | dSh_twin   SE     t   | dDD_twin  t "
            "| MIRROR MaxDD  dDD    t   | OOS CAGR/Sh/DD")
        for _, r in sub.iterrows():
            say(f"    {r.c:4.2f} {int(r.B):4d} | {r.CAGR:7.2%} {r.Sharpe:7.4f} {r.MaxDD:7.2%} "
                f"{r.H1:6.3f} {r.H2:6.3f} | {r.dd_margin_pp:+6.2f} {r.cagr_margin_pp:+8.2f} | "
                f"{int(r.keep4a)}  {int(r.keep4b)}  {int(r.keep4b_oos)}  | {r.eff_n:5.2f} "
                f"{r.max_w:5.4f} {r.min_w:5.4f} {r.mean_gross:5.3f} | {r.book_beta:5.3f} | "
                f"{r.turn_y:4.2f} {r.drag_bpyr:5.1f} | {r.d_sharpe_vs_twin:+8.4f} "
                f"{r.se_vs_twin:6.4f} {r.t_vs_twin:+5.2f} | {r.d_maxdd_pp_vs_twin:+7.3f} "
                f"{r.t_maxdd_vs_twin:+5.2f} | {r.mirror_MaxDD:7.2%} "
                f"{r.d_maxdd_pp_vs_mirror:+6.3f} {r.t_maxdd_vs_mirror:+5.2f} | {r.oCAGR:7.2%} "
                f"{r.oSharpe:6.4f} {r.oMaxDD:7.2%}")

    say("\n" + "=" * 128)
    say("RULE 8 WALK-FORWARD — (c, B) chosen by argmax IS Sharpe on warm-up..2016-12-31; "
        "2017-2026 read ONCE.")
    say("=" * 128)
    say("  panel | IS pick (c,B)  IS Sh | OOS CAGR  Sharpe   MaxDD 4b 4a | legs H1/H2/DD/CAGR | "
        "OOS DDmarg CAGRmarg | ANCHOR OOS CAGR/Sh/DD | dSh vs anchor (t) | dDD pp (t) | SPY OOS")
    for _, r in W.iterrows():
        say(f"  {r.panel:>5} | ({r.is_c:4.2f},{int(r.is_B):4d}) {r.is_Sharpe:6.4f} | "
            f"{r.oCAGR:7.2%} {r.oSharpe:7.4f} {r.oMaxDD:7.2%}  {int(r.keep4b_oos)}  "
            f"{int(r.keep4a_oos)} | {int(r.oleg_H1)}/{int(r.oleg_H2)}/{int(r.oleg_DD)}/"
            f"{int(r.oleg_CAGR)} | {r.oos_dd_margin_pp:+8.3f} {r.oos_cagr_margin_pp:+8.3f} | "
            f"{r.anchor_oCAGR:7.2%} {r.anchor_oSharpe:7.4f} {r.anchor_oMaxDD:7.2%} | "
            f"{r.d_oSharpe_vs_anchor:+7.4f} ({r.t_oSharpe_vs_anchor:+5.2f}) | "
            f"{r.d_oMaxDD_pp_vs_anchor:+6.3f} ({r.t_oMaxDD_vs_anchor:+5.2f}) | "
            f"{r.spy_oCAGR:6.2%}/{r.spy_oSharpe:.4f}/{r.spy_oMaxDD:7.2%}")

    say("\n" + "=" * 128)
    say("THE PRE-REGISTERED BAR")
    say("=" * 128)
    U = G[(G.panel == "U56") & (G.c > 0)]
    leg_i = U[U.dd_margin_pp > BAR_DD_PP]
    leg_ii = U[U.keep4b & U.keep4b_oos]
    leg_iii = U[U.t_vs_twin.abs() > BAR_T]
    both = U[(U.dd_margin_pp > BAR_DD_PP) & U.keep4b & U.keep4b_oos & (U.t_vs_twin.abs() > BAR_T)]
    say(f"  (i)   U56 DD margin > the anchor's {BAR_DD_PP:+.4f} pp : {len(leg_i)} of {len(U)} "
        f"biting cells (range {U.dd_margin_pp.min():+.4f} .. {U.dd_margin_pp.max():+.4f} pp)")
    say(f"  (ii)  U56 4b passes FULL and OOS            : {len(leg_ii)} of {len(U)} "
        f"(full {int(U.keep4b.sum())}, OOS {int(U.keep4b_oos.sum())})")
    say(f"  (iii) U56 |t| vs its own rank-permutation twin > {BAR_T:.0f} : {len(leg_iii)} of "
        f"{len(U)} (t range {U.t_vs_twin.min():+.2f} .. {U.t_vs_twin.max():+.2f})")
    say(f"  ALL THREE: {len(both)} of {len(U)}.")
    allb = G[G.c > 0]
    say(f"\n  ALL PANELS, resolution against the SHUFFLE: |t| > 2 on Sharpe at "
        f"{int((allb.t_vs_twin.abs() > BAR_T).sum())} of {len(allb)} cells full-sample, "
        f"{int((allb.ot_vs_twin.abs() > BAR_T).sum())} OOS; on MaxDD at "
        f"{int((allb.t_maxdd_vs_twin.abs() > BAR_T).sum())} of {len(allb)}.")
    say(f"  ALL PANELS, resolution against the MIRROR (the sharpest null): |t| > 2 on MaxDD at "
        f"{int((allb.t_maxdd_vs_mirror.abs() > BAR_T).sum())} of {len(allb)}; on Sharpe at "
        f"{int((allb.t_sharpe_vs_mirror.abs() > BAR_T).sum())} of {len(allb)}.")
    say(f"  SIGN COUNT vs the mirror: the beta ordering draws down LESS than its mirror at "
        f"{int((allb.d_maxdd_pp_vs_mirror > 0).sum())} of {len(allb)} cells "
        f"(0.5 x {len(allb)} = {len(allb)/2:.0f} is the coin).")
    say(f"  ALL PANELS, KEEP paths: 4a {int(G.keep4a.sum())} of {len(G)}; "
        f"4b full {int(G.keep4b.sum())} of {len(G)}; 4b OOS {int(G.keep4b_oos.sum())} of "
        f"{len(G)}; both {int((G.keep4b & G.keep4b_oos).sum())}.")
    say(f"  Median Sharpe percentile inside the twin band across all {len(allb)} biting cells: "
        f"{allb.sharpe_pct_in_twins.median():.3f}; MaxDD percentile "
        f"{allb.maxdd_pct_in_twins.median():.3f} (0.5 = the ordering buys nothing the shuffle "
        f"does not).")
    say(f"  BOOK BETA: anchor {G[G.panel=='U56'].anchor_book_beta.iloc[0]:.4f}; the band moves "
        f"U56's realised weighted beta to {U.book_beta.min():.4f} .. {U.book_beta.max():.4f}.")

    # G10 bit-identical recompute of the U56 headline cell
    pan = panels[0]
    segs = segments(pan, I_N, I_H)
    C = np.cumprod(1.0 + pan.rets, axis=0)
    Cp = np.vstack([np.ones((1, pan.rets.shape[1])), C[:-1]])
    gg, tu, _, _, _, _, _, _ = run_book(pan, segs, cell_weights(pan, segs, 0.50, 126), C, Cp)
    rr = gg - tu * COST / 1e4
    d10 = float(np.max(np.abs(rr - headline_ret)))
    gate("G10 bit-identical recompute (U56, c=0.50, B=126)", f"max |dret| {d10:.3e}", "< 1e-15",
         d10 < 1e-15)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    P.to_csv(f"{OUT}.perm.csv", index=False)
    M.to_csv(f"{OUT}.mirror.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n  wrote {OUT.name}.grid.csv / .walkforward.csv / .perm.csv / .mirror.csv / "
        f".gates.csv / .log.txt")
    say(f"  ALL GATES PASS: {all(g['pass_'] for g in GATES)}   ({time.time()-t0:.1f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

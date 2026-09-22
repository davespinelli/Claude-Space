#!/usr/bin/env python3
"""
Idea 1465 (lane cloud, 2026-09-22) — does the BETA BAND's CAGR PREMIUM ON SMALL survive a
TURNOVER-MATCHED control and a RANK-PERMUTATION control?

THE PREMISE.  Idea 1444 swept the beta band (half-width c) against the min-hold (H) on three
panels and found ONE asymmetry it could not explain: on SMALL the band RAISES CAGR above its
own same-H c = 0 anchor at 24 of 24 biting cells -- so no CAGR-matched de-gross twin can even
be built there -- while on U56 it COSTS CAGR at 24 of 24.  Idea 1436 saw the same sign on
SMALL on the raw return leg.  The record has therefore never priced SMALL's premium against
a control; it has only observed it.

TWO CHANNELS CAN PRODUCE IT, AND THEY HAVE OPPOSITE CAPITAL MEANINGS:
  (1) A LOW-BETA PREMIUM.  The band overweights the lowest-trailing-beta names of the held
      set.  On a small-cap panel the low-beta side may simply earn more.  If so the ORDERING
      carries the premium and a random ordering of the same weights must not reproduce it.
  (2) A REBALANCING-FREQUENCY ARTEFACT.  The band re-sorts weights at every rebalance, so it
      churns far more than its anchor (1444: 2.87 -> up to 9.89 /yr).  Forced periodic
      reversion to a fixed weight vector harvests cross-sectional mean reversion, and small
      caps are the panel where that harvest is largest.  If so, a book with ZERO
      cross-sectional information but the SAME realised turnover reproduces it.

THE TWO CONTROLS, BOTH PRE-REGISTERED, BOTH PRICED ON EVERY CELL:

  PERM(K = 8 seeds) -- RANK-PERMUTATION TWIN.  The cell's own weight multiset re-assigned to
      the SAME held names in seeded random order.  Matches gross, names, name count, the whole
      weight distribution, effective N and Herfindahl on every row; differs ONLY in which name
      gets which slot.  Kills channel (1) if it reproduces the premium.  (1444's construction,
      re-used verbatim so the two runs are comparable.)

  TMRC -- TURNOVER-MATCHED REBALANCE CONTROL.  The same-H c = 0 EQUAL-WEIGHT anchor, holding
      the IDENTICAL names on the IDENTICAL rows, but reset to its equal-weight target every k
      trading days INSIDE each min-hold segment instead of only at the segment's start.  k is
      not a dial: it is SOLVED over a fixed ladder {1,2,3,5,7,10,15,21,42,63,126} by taking
      the k whose realised annual turnover is closest to the cell's, and the match error is
      published for every cell.  TMRC carries ZERO cross-sectional information -- it never
      looks at beta, at rank, or at anything but the calendar -- so if it reproduces the
      premium, channel (2) owns it.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
  c {0.00, 0.25, 0.50, 0.75, 1.00}   DIAL 1 -- band half-width.  c = 0.00 de-bands the cell.
  H {21, 63, 126, 189, 252, 378}     DIAL 2 -- min-hold in trading days.  H = 126 is the
                                     frozen 2026-09-04 incumbent's value.
30 cells per panel, EVERY ONE published in .grid.csv.

FROZEN, NEVER VARIED: beta lookback B = 126 rows (1444's frozen value); N = 20; gross = 0.75;
cadence W; cost 10 bps; t+1.  k (TMRC) and the permutation seeds are SOLVED/FIXED, not tuned.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL.  SMALL is the panel the idea names and the one the
verdict is about; U56 is carried as the published SIGN CONTRAST (1444 found the premium's sign
flips there) and is never selected on.  Both KEEP paths at every cell; halves; IS/OOS; realised
turnover in /yr and its 10 bps drag; realised mean gross; effective N; realised book beta.

THE BAR, PRE-REGISTERED HERE BEFORE ANY NUMBER WAS READ.  On SMALL, the premium is a LOW-BETA
PREMIUM (channel 1) only if, over the 24 biting cells:
  (i)   the cell's CAGR premium over its same-H anchor exceeds the PERM mean premium at a
        majority of cells AND at |t| > 2 on a paired circular-block bootstrap at >= 1 cell;
  (ii)  the cell's premium exceeds its TMRC premium at a majority of cells, same resolution;
  (iii) the DD leg also moves -- the idea's own clause: SMALL's anchor misses the 4b DD cap by
        16.28 pp, so nothing here is a BOOK unless some cell clears 4b.
Failing (i) or (ii) is the pre-registered MECHANISM KILL and is reported as a finding.
Clearing (i)+(ii) but not (iii) is a MECHANISM finding with no capital claim.

PROTOCOL: rule 1 (>= 10y); rule 2 (t+1, 10 bps, no leverage, no shorting); rule 3 (live RULES
v2 AND SPY); rule 4 (both KEEP paths, exactly 2 tuned parameters); rule 8 (walk-forward: (c,H)
chosen on warm-up..2016-12-31 ONLY, 2017-2026 read ONCE) under TWO pre-registered choosers plus
the ZERO-PARAMETER anchor as reference; rule 9 (SURVIVORSHIP STATED: the SMALL panel is the
CURRENT constituents of a sub-$2B screen, so its levels are biased UP; every comparison here is
WITHIN that panel -- cell vs its own anchor vs its own controls -- which is why the premium, not
the level, is the object).  Tickers with max_1d_move >= 1.0 in data/small_meta.csv are DROPPED
before anything is computed.  RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py NOT modified.

GATES.  G0 sample >= 10y.  G1 the c = 0 cell at each H is BIT-IDENTICAL to that H's own anchor.
G2 the c = 0 PERM twin is BIT-IDENTICAL to the c = 0 cell (a permutation of an equal multiset).
G3 at a given H every c holds the IDENTICAL name set on every row.  G4 all 30 cells published
per panel.  G5 exactly two tuned parameters.  G6 the rule-8 choosers read no row on or after
2017-01-01.  G7 EXPOSURE CHANNEL SHUT: at every (H, c) realised mean gross matches the anchor's
to < 1e-12.  G8 no leverage: every rebalance's weight sum == 0.75 to < 1e-12.  G9 the band is
respected exactly and its width is strictly increasing in c.  G10 TMRC holds the IDENTICAL
names as its anchor on every row.  G11 beta uses TRAILING rows only.  G12 bit-identical
recompute of the SMALL headline cell.  G13 the H dial BITES (turnover strictly decreasing in H
at c = 0).  G14 the dropped-ticker rule actually bit (>= 1 name removed).

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-22_small-band-cagr-premium-controls_cloud.py
"""
from __future__ import annotations

import sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights          # noqa: E402
from engine import backtest, rebalance_mask                   # noqa: E402

DATE, SLUG = "2026-09-22", "small-band-cagr-premium-controls"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_G, B_FIXED = 20, 0.75, 126
COST, CADENCE = 10.0, "W"
CS = [0.00, 0.25, 0.50, 0.75, 1.00]
HS = [21, 63, 126, 189, 252, 378]
KLADDER = [1, 2, 3, 5, 7, 10, 15, 21, 42, 63, 126]
NPERM, SEED = 8, 20260922
OOS_START = "2017-01-01"
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BOOT_REPS, BOOT_BLOCK = 400, 63
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


# ---------------------------------------------------------------- selection mechanics
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


def rolling_beta(R, y, B):
    ey = y.rolling(B).mean()
    vy = (y * y).rolling(B).mean() - ey * ey
    ex = R.rolling(B).mean()
    exy = R.mul(y, axis=0).rolling(B).mean()
    return exy.sub(ex.mul(ey, axis=0)).div(vy.replace(0.0, np.nan), axis=0).values


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
        self.beta = rolling_beta(px[invest].pct_change(), px["SPY"].pct_change(), B_FIXED)
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])


def segments(pan, N, H, lag=1):
    """Min-hold selection frame.  Depends on H ONLY, so every c at that H holds the IDENTICAL
    names on the IDENTICAL rows (gate G3)."""
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


def band_multiset(n, c, gross=I_G):
    if n == 0:
        return np.zeros(0)
    ranks = np.arange(1, n + 1, dtype=float)
    z = 1.0 - 2.0 * (ranks - 0.5) / n          # sums to EXACTLY 0
    return (gross / n) * (1.0 + c * z)


def cell_weights(pan, segs, c, perm_seed=None, gross=I_G):
    """LOWEST trailing beta takes the CAP side.  perm_seed shuffles the SAME multiset."""
    BE = pan.beta
    rng = np.random.default_rng(perm_seed) if perm_seed is not None else None
    ws = []
    for (t, stop, ts, sel) in segs:
        n = len(sel)
        if n == 0:
            ws.append(np.zeros(0)); continue
        m = band_multiset(n, c, gross)
        if c == 0.0:
            order = np.arange(n)
        else:
            b = BE[ts, sel].astype(float)
            fin = np.isfinite(b)
            if not fin.all():
                med = np.nanmedian(b[fin]) if fin.any() else 1.0
                b = np.where(fin, b, med)
            order = np.argsort(b, kind="stable")
        w = np.empty(n); w[order] = m
        if rng is not None:
            w = w[rng.permutation(n)]
        ws.append(w)
    return ws


def split_segments(segs, ws, k):
    """TMRC: split every min-hold segment into k-day sub-segments carrying the SAME weight
    vector, i.e. reset to the same target every k rows.  Names are untouched (gate G10)."""
    out_s, out_w = [], []
    for (i0, i1, ts, sel), wv in zip(segs, ws):
        a = i0
        while a < i1:
            b = min(a + k, i1)
            out_s.append((a, b, ts, sel)); out_w.append(wv)
            a = b
    return out_s, out_w


def run_book(pan, segs, ws):
    rets, C, Cp = pan.rets, pan.C, pan.Cp
    T, M = rets.shape
    turn = np.zeros(T); out = np.zeros(T)
    effn = np.zeros(len(segs)); wsum_max = 0.0; gsum = 0.0; gn = 0
    curw = np.zeros(M)
    for j, ((i0, i1, ts, sel), wv) in enumerate(zip(segs, ws)):
        w0 = np.zeros(M)
        if len(sel):
            w0[pan.iinv[sel]] = wv
            q = wv / wv.sum()
            effn[j] = 1.0 / float((q ** 2).sum())
        wsum_max = max(wsum_max, float(w0.sum()))
        turn[i0] = float(np.abs(w0 - curw).sum())
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        gsum += float(w0.sum()) * (i1 - i0); gn += (i1 - i0)
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return out, turn, effn, wsum_max, (gsum / gn if gn else np.nan)


def net(pan, segs, ws):
    g, t, en, wsx, mg = run_book(pan, segs, ws)
    return g - t * COST / 1e4, t, en, wsx, mg


def book_beta(pan, segs, ws):
    num = den = 0.0
    for (t, stop, ts, sel), wv in zip(segs, ws):
        if not len(sel):
            continue
        b = pan.beta[ts, sel].astype(float); fin = np.isfinite(b)
        if not fin.any():
            continue
        num += float(np.sum(wv[fin] * b[fin])); den += float(np.sum(wv[fin]))
    return num / den if den > 0 else np.nan


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


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def bmpack(r):
    h1, h2 = halves(r)
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r), H1=h1, H2=h2)


def keep_paths(r, bm, live):
    h1, h2 = halves(r)
    m = dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(H1=bool(h1 > bm["H1"]), H2=bool(h2 > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return k4a, bool(all(legs.values())), m, h1, h2, legs


def _blocks(n, reps=BOOT_REPS, L=BOOT_BLOCK, seed=SEED):
    nb = int(np.ceil(n / L))
    rng = np.random.default_rng(seed)
    starts = rng.integers(0, n, size=(reps, nb))
    return (starts[:, :, None] + np.arange(L)[None, None, :]).reshape(reps, nb * L)[:, :n] % n


def paired_t_cagr(a, b, idxb):
    """t of the paired CAGR difference a - b on identical circular-block resamples."""
    A, B = np.asarray(a, float)[idxb], np.asarray(b, float)[idxb]
    n = A.shape[1]
    ca = np.cumprod(1 + A, axis=1)[:, -1] ** (252 / n) - 1
    cb = np.cumprod(1 + B, axis=1)[:, -1] ** (252 / n) - 1
    d = ca - cb
    s = d.std(ddof=1)
    obs = cagr(a) - cagr(b)
    return float(obs), float(s), (float(obs / s) if s > 0 else np.nan)


# ---------------------------------------------------------------- panels
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"].astype(str))
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    dropped = len(px.columns) - len(keep)
    px = px[keep]
    return px, dropped


def main():
    t0 = time.time()
    say(f"=== idea 1465 — SMALL band CAGR premium vs PERM and TURNOVER-MATCHED controls ===")
    say(f"    {DATE}  lane cloud   cadence {CADENCE}  cost {COST:.0f} bps  N={I_N} gross={I_G} B={B_FIXED}")

    px_s, dropped = small_panel()
    gate("G14 dropped-ticker rule bit", f"{dropped} names dropped (max_1d_move >= 1.0)", ">= 1", dropped >= 1)
    px_u = load_universe()
    say(f"    SMALL {px_s.shape[1]-1} investable names, {px_s.index[0].date()}..{px_s.index[-1].date()}")
    say(f"    U56   {px_u.shape[1]-1} investable names, {px_u.index[0].date()}..{px_u.index[-1].date()}")

    # live comparand: RULES v2 on its own (U56) universe, 10 bps weekly
    live_u = backtest(px_u, rules_v2_weights(px_u), cost_bps=COST, freq=CADENCE)["returns"]

    panels = {}
    for nm, px in (("SMALL", px_s), ("U56", px_u)):
        invest = [c for c in px.columns if c != "SPY"]
        panels[nm] = Panel(nm, px, invest)

    grid_rows, ctrl_rows = [], []
    headline = {}
    for pname, pan in panels.items():
        say(f"\n--- PANEL {pname} ---")
        i0 = WARMUP
        idx = pan.idx
        yrs = (len(idx) - i0) / 252
        gate(f"G0 {pname} sample >= 10y", f"{yrs:.1f}y", ">= 10y", yrs >= 10)
        oos_mask = np.asarray(idx >= OOS_START)[i0:]
        is_mask = np.asarray(idx <= IS_END)[i0:]

        spy = pan.spy[i0:]
        bm = bmpack(spy)
        liv = live_u.reindex(idx).fillna(0.0).values[i0:]
        lv = bmpack(liv)
        say(f"    SPY       full {bm['CAGR']:7.2%} {bm['Sharpe']:7.4f} {bm['MaxDD']:8.2%}  halves {bm['H1']:.4f}/{bm['H2']:.4f}")
        say(f"    RULES v2  full {lv['CAGR']:7.2%} {lv['Sharpe']:7.4f} {lv['MaxDD']:8.2%}  halves {lv['H1']:.4f}/{lv['H2']:.4f}")
        bm_oos = bmpack(spy[oos_mask]); lv_oos = bmpack(liv[oos_mask])

        segcache, wcache, retcache = {}, {}, {}
        anch = {}
        for H in HS:
            segs = segments(pan, I_N, H)
            segcache[H] = segs
            names_sig = [tuple(s[3].tolist()) for s in segs]
            for c in CS:
                ws = cell_weights(pan, segs, c)
                r, turn, effn, wsx, mg = net(pan, segs, ws)
                r = r[i0:]
                wcache[(H, c)] = ws
                retcache[(H, c)] = r
                if c == 0.0:
                    anch[H] = dict(r=r, turn=turn, mg=mg, ws=ws)
                tpy = float(turn[i0:].sum()) / ((len(turn) - i0) / 252)
                k4a, k4b, m, h1, h2, legs = keep_paths(r, bm, lv)
                ro = r[oos_mask]
                k4ao, k4bo, mo, h1o, h2o, lego = keep_paths(ro, bm_oos, lv_oos)
                prem = cagr(r) - cagr(anch[H]["r"])
                grid_rows.append(dict(
                    panel=pname, H=H, c=c, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                    H1=h1, H2=h2, turnover_yr=tpy, drag_bp_yr=tpy * COST,
                    mean_gross=mg, effN=float(np.mean(effn[effn > 0])), book_beta=book_beta(pan, segs, ws),
                    cagr_prem_vs_anchor_pp=prem * 100,
                    keep4a=k4a, keep4b=k4b, leg_H1=legs["H1"], leg_H2=legs["H2"], leg_DD=legs["DD"], leg_CAGR=legs["CAGR"],
                    oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"], oos_keep4b=k4bo,
                    is_CAGR=cagr(r[is_mask]), is_Sharpe=sharpe(r[is_mask]),
                    is_prem_pp=(cagr(r[is_mask]) - cagr(anch[H]["r"][is_mask])) * 100,
                ))
            # G3: identical names at every c for this H (frame built once, shared)
            publish(f"G3 {pname} H={H} name frame shared by all c", f"{len(names_sig)} segments")

        # ---- gates on the grid
        g = pd.DataFrame(grid_rows)
        gp = g[g.panel == pname]
        ok = True
        for H in HS:
            a = retcache[(H, 0.0)]
            ok &= np.array_equal(a, anch[H]["r"])
        gate(f"G1 {pname} c=0 cell == that H's anchor", "bit-identical at 6 H", "identical", bool(ok))
        permc0 = net(pan, segcache[126], cell_weights(pan, segcache[126], 0.0, perm_seed=1))[0][i0:]
        gate(f"G2 {pname} c=0 PERM twin == c=0 cell", f"max|diff| {np.abs(permc0 - retcache[(126,0.0)]).max():.2e}",
             "< 1e-15", float(np.abs(permc0 - retcache[(126, 0.0)]).max()) < 1e-15)
        mg0 = {H: gp[(gp.H == H) & (gp.c == 0.0)].mean_gross.iloc[0] for H in HS}
        dev = max(abs(gp[gp.H == H].mean_gross - mg0[H]).max() for H in HS)
        gate(f"G7 {pname} exposure channel shut", f"max |mean_gross - anchor| {dev:.2e}", "< 1e-12", dev < 1e-12)
        wsx = max(float(np.abs(w.sum() - I_G)) for H in HS for c in CS for w in wcache[(H, c)] if len(w))
        nempty = sum(1 for H in HS for c in CS for w in wcache[(H, c)] if not len(w))
        gate(f"G8 {pname} no leverage (EVERY non-empty rebalance sums to {I_G})",
             f"max dev {wsx:.2e} over all rebalances; {nempty} empty (pre-warm-up) segments hold 0",
             "< 1e-12", wsx < 1e-12)
        widths = [float(band_multiset(20, c).max() - band_multiset(20, c).min()) for c in CS]
        gate(f"G9 {pname} band width strictly increasing in c", f"{[round(w,5) for w in widths]}",
             "strictly increasing", all(widths[i] < widths[i + 1] for i in range(len(widths) - 1)))
        t0c = [float(gp[(gp.H == H) & (gp.c == 0.0)].turnover_yr.iloc[0]) for H in HS]
        gate(f"G13 {pname} H dial bites (turnover falls with H at c=0)", f"{[round(x,3) for x in t0c]}",
             "strictly decreasing", all(t0c[i] > t0c[i + 1] for i in range(len(t0c) - 1)))
        gate(f"G4 {pname} all 30 cells published", f"{len(gp)}", "30", len(gp) == 30)

        # ---- the two controls, on every BITING cell (c > 0)
        say(f"\n    CONTROLS on {pname}: PERM(K={NPERM}) and TMRC (turnover-matched rebalance)")
        idxb = _blocks(len(retcache[(126, 0.0)]))
        for H in HS:
            segs = segcache[H]
            a_r = anch[H]["r"]; a_c = cagr(a_r)
            # TMRC ladder for this H, computed once (does not depend on c)
            tm = {}
            for k in KLADDER:
                s2, w2 = split_segments(segs, wcache[(H, 0.0)], k)
                r2, t2, _, _, _ = net(pan, s2, w2)
                tm[k] = (r2[i0:], float(t2[i0:].sum()) / ((len(t2) - i0) / 252))
            for c in CS:
                if c == 0.0:
                    continue
                r = retcache[(H, c)]
                tpy = float(gp[(gp.H == H) & (gp.c == c)].turnover_yr.iloc[0])
                pr = [net(pan, segs, cell_weights(pan, segs, c, perm_seed=SEED + s))[0][i0:] for s in range(NPERM)]
                perm_c = float(np.mean([cagr(x) for x in pr]))
                perm_sd = float(np.std([cagr(x) for x in pr], ddof=1))
                perm_dd = float(np.mean([mdd(x) for x in pr]))
                kbest = min(KLADDER, key=lambda k: abs(tm[k][1] - tpy))
                tr, ttpy = tm[kbest]
                obs_p, se_p, t_p = paired_t_cagr(r, np.mean(pr, axis=0), idxb)
                obs_t, se_t, t_t = paired_t_cagr(r, tr, idxb)
                ctrl_rows.append(dict(
                    panel=pname, H=H, c=c,
                    cell_CAGR=cagr(r), anchor_CAGR=a_c, cell_prem_pp=(cagr(r) - a_c) * 100,
                    perm_CAGR=perm_c, perm_sd=perm_sd, perm_prem_pp=(perm_c - a_c) * 100,
                    tmrc_k=kbest, tmrc_CAGR=cagr(tr), tmrc_prem_pp=(cagr(tr) - a_c) * 100,
                    cell_turnover_yr=tpy, tmrc_turnover_yr=ttpy, turnover_match_err=abs(ttpy - tpy),
                    turnover_match_rel=abs(ttpy - tpy) / tpy,
                    d_vs_perm_pp=(cagr(r) - perm_c) * 100, t_vs_perm=t_p,
                    d_vs_tmrc_pp=(cagr(r) - cagr(tr)) * 100, t_vs_tmrc=t_t,
                    cell_MaxDD=mdd(r), perm_MaxDD=perm_dd, tmrc_MaxDD=mdd(tr),
                    cell_Sharpe=sharpe(r), tmrc_Sharpe=sharpe(tr),
                ))
        say(f"    ... {pname} controls done  ({time.time()-t0:.0f}s)")

        # ---- rule 8 walk-forward, this panel
        say(f"\n    RULE 8 walk-forward on {pname}: (c,H) chosen on warm-up..{IS_END}, {OOS_START}+ read ONCE")
        gate(f"G6 {pname} choosers read no OOS row", f"IS rows {int(is_mask.sum())}, OOS rows {int(oos_mask.sum())}",
             "disjoint, IS ends 2016-12-31", bool(not (is_mask & oos_mask).any()))
        cand = [(H, c) for H in HS for c in CS]
        is_sh = {hc: sharpe(retcache[hc][is_mask]) for hc in cand}
        is_pr = {hc: cagr(retcache[hc][is_mask]) - cagr(anch[hc[0]]["r"][is_mask]) for hc in cand}
        choosers = {
            "C_ISSHARPE (argmax IS Sharpe)": max(cand, key=lambda hc: is_sh[hc]),
            "C_ISPREM (argmax IS CAGR premium over same-H anchor)": max(cand, key=lambda hc: is_pr[hc]),
            "C_ANCHOR (zero-parameter, c=0 H=126)": (126, 0.0),
        }
        wf = []
        for cn, hc in choosers.items():
            ro = retcache[hc][oos_mask]
            k4ao, k4bo, mo, h1o, h2o, lego = keep_paths(ro, bm_oos, lv_oos)
            wf.append(dict(panel=pname, chooser=cn, pick_H=hc[0], pick_c=hc[1],
                           oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                           oos_keep4a=k4ao, oos_keep4b=k4bo))
            say(f"      {cn:<52s} -> (H={hc[0]}, c={hc[1]:.2f})  OOS {mo['CAGR']:7.2%} {mo['Sharpe']:7.4f} {mo['MaxDD']:8.2%}  4b={k4bo}")
        wf.append(dict(panel=pname, chooser="SPY (OOS)", pick_H=np.nan, pick_c=np.nan,
                       oos_CAGR=bm_oos["CAGR"], oos_Sharpe=bm_oos["Sharpe"], oos_MaxDD=bm_oos["MaxDD"],
                       oos_keep4a=False, oos_keep4b=False))
        wf.append(dict(panel=pname, chooser="RULES v2 (OOS)", pick_H=np.nan, pick_c=np.nan,
                       oos_CAGR=lv_oos["CAGR"], oos_Sharpe=lv_oos["Sharpe"], oos_MaxDD=lv_oos["MaxDD"],
                       oos_keep4a=False, oos_keep4b=False))
        say(f"      {'SPY (OOS)':<52s}    OOS {bm_oos['CAGR']:7.2%} {bm_oos['Sharpe']:7.4f} {bm_oos['MaxDD']:8.2%}")
        say(f"      {'RULES v2 (OOS)':<52s}    OOS {lv_oos['CAGR']:7.2%} {lv_oos['Sharpe']:7.4f} {lv_oos['MaxDD']:8.2%}")
        headline[pname] = dict(bm=bm, lv=lv, bm_oos=bm_oos, lv_oos=lv_oos, wf=wf,
                               anchor=bmpack(anch[126]["r"]))
        # G12 bit-identical recompute of the headline cell
        rr = net(pan, segcache[126], cell_weights(pan, segcache[126], 1.00))[0][i0:]
        gate(f"G12 {pname} headline cell (H=126,c=1.00) recompute", f"max|diff| {np.abs(rr-retcache[(126,1.0)]).max():.2e}",
             "< 1e-15", float(np.abs(rr - retcache[(126, 1.0)]).max()) < 1e-15)

    G = pd.DataFrame(grid_rows); C = pd.DataFrame(ctrl_rows)
    W = pd.DataFrame([w for p in headline.values() for w in p["wf"]])
    G.to_csv(f"{OUT}.grid.csv", index=False)
    C.to_csv(f"{OUT}.controls.csv", index=False)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)

    # ---------------------------------------------------------------- the verdict
    say("\n=== THE PREMISE: does the band raise CAGR on SMALL and cost it on U56? ===")
    for pname in ("SMALL", "U56"):
        cc = C[C.panel == pname]
        say(f"    {pname}: cell premium over same-H anchor POSITIVE at {(cc.cell_prem_pp > 0).sum()} of {len(cc)} biting cells; "
            f"median {cc.cell_prem_pp.median():+.3f} pp, min {cc.cell_prem_pp.min():+.3f}, max {cc.cell_prem_pp.max():+.3f}")

    say("\n=== CONTROL (1) RANK-PERMUTATION: does the BETA ORDERING carry it? ===")
    for pname in ("SMALL", "U56"):
        cc = C[C.panel == pname]
        w = int((cc.d_vs_perm_pp > 0).sum())
        res = int((cc.t_vs_perm.abs() > BAR_T).sum())
        say(f"    {pname}: cell beats its PERM twin at {w} of {len(cc)}; median d {cc.d_vs_perm_pp.median():+.3f} pp; "
            f"|t|>{BAR_T:.0f} at {res} of {len(cc)}; PERM premium over anchor positive at {(cc.perm_prem_pp>0).sum()} of {len(cc)} "
            f"(median {cc.perm_prem_pp.median():+.3f} pp)")

    say("\n=== CONTROL (2) TURNOVER-MATCHED REBALANCE (zero cross-sectional information) ===")
    for pname in ("SMALL", "U56"):
        cc = C[C.panel == pname]
        w = int((cc.d_vs_tmrc_pp > 0).sum())
        res = int((cc.t_vs_tmrc.abs() > BAR_T).sum())
        say(f"    {pname}: cell beats its TMRC at {w} of {len(cc)}; median d {cc.d_vs_tmrc_pp.median():+.3f} pp; "
            f"|t|>{BAR_T:.0f} at {res} of {len(cc)}; TMRC premium over anchor positive at {(cc.tmrc_prem_pp>0).sum()} of {len(cc)} "
            f"(median {cc.tmrc_prem_pp.median():+.3f} pp); median turnover match error "
            f"{cc.turnover_match_rel.median():.1%} (max {cc.turnover_match_rel.max():.1%})")

    say("\n=== THE DRAWDOWN SIDE (the idea's clause: nothing is a BOOK unless the DD leg moves) ===")
    for pname in ("SMALL", "U56"):
        cc = C[C.panel == pname]
        say(f"    {pname}: cell MaxDD shallower than its ANCHOR at "
            f"{int((cc.cell_MaxDD > (cc.cell_MaxDD*0 + [float(G[(G.panel==pname)&(G.H==h)&(G.c==0.0)].MaxDD.iloc[0]) for h in cc.H])).sum())} of {len(cc)}; "
            f"shallower than PERM at {int((cc.cell_MaxDD > cc.perm_MaxDD).sum())} of {len(cc)}; "
            f"shallower than TMRC at {int((cc.cell_MaxDD > cc.tmrc_MaxDD).sum())} of {len(cc)}; "
            f"cell MaxDD median {cc.cell_MaxDD.median():.2%}, best {cc.cell_MaxDD.max():.2%}")

    say("\n=== 4b / 4a across the grid ===")
    for pname in ("SMALL", "U56"):
        gp = G[G.panel == pname]
        say(f"    {pname}: 4b FULL {int(gp.keep4b.sum())} of {len(gp)};  4b OOS {int(gp.oos_keep4b.sum())} of {len(gp)};  "
            f"4a FULL {int(gp.keep4a.sum())} of {len(gp)}")
        fails = {k: int((~gp[f'leg_{k}']).sum()) for k in ("H1", "H2", "DD", "CAGR")}
        say(f"      4b leg failures: {fails}")

    smc = C[C.panel == "SMALL"]
    bar_i = bool((smc.d_vs_perm_pp > 0).sum() > len(smc) / 2 and (smc.t_vs_perm.abs() > BAR_T).any())
    bar_ii = bool((smc.d_vs_tmrc_pp > 0).sum() > len(smc) / 2 and (smc.t_vs_tmrc.abs() > BAR_T).any())
    bar_iii = bool(G[(G.panel == "SMALL")].keep4b.any())
    say("\n=== PRE-REGISTERED BAR (SMALL) ===")
    say(f"    (i)   beats PERM at a majority AND resolved at |t|>2 somewhere : {bar_i}")
    say(f"    (ii)  beats TMRC at a majority AND resolved at |t|>2 somewhere : {bar_ii}")
    say(f"    (iii) some SMALL cell clears 4b FULL (the DD leg moves)        : {bar_iii}")
    if bar_i and bar_ii and bar_iii:
        verdict = "KEEP-candidate (low-beta premium AND a book)"
    elif bar_i and bar_ii:
        verdict = "MECHANISM: LOW-BETA PREMIUM, no book (4b DD leg does not move)"
    else:
        verdict = "KILL of the low-beta reading — the premium is reproduced by a control"
    say(f"    VERDICT: {verdict}")

    gate("G5 exactly two tuned parameters", "c (band half-width), H (min-hold)", "2", True)
    gates = pd.DataFrame(GATES); gates.to_csv(f"{OUT}.gates.csv", index=False)
    nfail = int((~gates.pass_).sum())
    say(f"\n    GATES: {len(gates)} recorded, {nfail} FAIL")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG))
    say(f"    wrote {OUT.name}.{{grid,controls,walkforward,gates}}.csv + console.txt   ({time.time()-t0:.0f}s)")
    return G, C, W, verdict


if __name__ == "__main__":
    main()

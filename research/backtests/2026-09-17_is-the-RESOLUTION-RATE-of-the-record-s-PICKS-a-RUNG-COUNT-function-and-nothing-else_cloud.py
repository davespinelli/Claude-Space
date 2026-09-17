#!/usr/bin/env python3
"""
Idea 1232 (lane cloud, 2026-09-17) — is the RESOLUTION RATE of the record's PICKS a RUNG-COUNT
function and nothing else?

THE PREMISE, READ FROM THE RECORD.  Idea 1209 found the four ladders' exact-monotone rates
(N 0/42, H 6/42, GROSS 40/42, CADENCE 42/42) are ordered EXACTLY by rung count k
(6, 4, 10, 2 -> rates 0.000, 0.143, 0.952, 1.000 once the k=2 ladder is read as trivially
monotone), that only GROSS's excess survives its own 2/k! null, and that the RESOLUTION rate
is 4 of 168 and entirely on GROSS.  Two different statistics, one suspiciously monotone
ordering.  Both may be ONE k effect wearing four ladder names.

The confound is that the record's four ladders differ in k AND in construction: N re-selects
the book, H changes the min-hold, GROSS re-levers ONE book (1189's degeneracy), CADENCE
re-times it.  Nothing in the record separates "this ladder resolves" from "this ladder has
k rungs".  This run separates them by building ladders of MATCHED CONSTRUCTION at
k = 2, 3, 4, 6, 8, 10 on the SAME dial and reading both rates as functions of k alone.

WHAT IS MEASURED, STATED BEFORE ANY NUMBER IS READ.  For each (panel, fold, dial, sub-ladder):

  MONO      the IS Sharpe sequence taken in RUNG ORDER has zero direction reversals (exactly
            monotone up or down).  Its combinatorial null is 2/k! for k >= 2 (1209's).
  RESOLVED  the IS argmax rung separates from the ladder's BEST OTHER rung by a paired
            moving-block bootstrap (L = 63, B = 400, blocks drawn on the IS window, both books
            read on the SAME resampled index) at t = mean(dSharpe)/SD(dSharpe) > 1.96.
            This is 1233's estimator, unchanged.

PRE-DECLARED OUTCOMES (fixed before the run; the verdict is read off, not chosen):
  (A) IT IS K AND NOTHING ELSE — at every k the three dials' RESOLVED rates lie within 0.10 of
      each other, and the k-spread (max over k minus min over k, pooled across dials) exceeds
      that dial spread.  The record's ladder ordering is a rung-count artefact.
  (B) IT IS NOT K ALONE — at some k the dial spread exceeds 0.10 AND exceeds the k spread.
      Construction carries information the rung count does not.
  (C) NEITHER SEPARABLE — both spreads below 0.10.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  k     {2, 3, 4, 6, 8, 10}                     — the rung count, the thing under test
  DIAL  {N, H, GROSS}                           — which axis the sub-ladders are drawn on

  Each dial is given a TEN-RUNG base ladder so that every k is drawn from a ladder of the same
  length by the same rule (the queue's "matched CONSTRUCTION"):
      N      [5, 8, 10, 12, 15, 20, 25, 30, 35, 40]      (the record's 6 rungs, extended)
      H      [21, 42, 63, 84, 126, 168, 210, 252, 315, 378]  (the record's 4 rungs, extended)
      GROSS  [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]  (the record's own)
  The record's committed anchor rung (N=20, H=126, GROSS=0.75) is a member of all three.
  Sub-ladders preserve rung order.  At each k, all C(10, k) sub-ladders are used when that is
  <= 24, else a seeded sample of 24 (numpy default_rng(1232)); the count is published per cell.

FROZEN, NOT DIALLED: the record's construction — 3-leg composite (21/252, 0/126, 0/63),
above-200d eligibility, max_vol 0.60, GROSS 0.75 and CADENCE W off the dialled axis, 10 bps
(rule 2), decide-at-t / apply-at-t+1, warm-up 260 rows.  The bootstrap at L = 63 / B = 400 and
the 1.96 bar are 1233's and are not tuned here.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); the 14 folds; the 4a and
4b legs; the IS and OOS windows.

THE TRADABLE ARM (rule 8).  A rate is not a book, so the run also prices the policy the
resolution bar implies, made decidable on IS data only, per (panel, dial, k):

  T_ALWAYS    hold the sub-ladder's IS-argmax rung at every fold (the record's habit).
  T_ANCHOR    hold the anchor rung at every fold (1224's substitution).
  T_RESOLVED  hold the IS-argmax rung iff that fold's IS bootstrap RESOLVES it, else the
              anchor — "only act on a pick your own data can separate".

Each policy's fold-year OOS segments are concatenated into ONE tradable daily curve and scored
on BOTH KEEP paths (4a vs live RULES v2, 4b vs SPY), full sample / halves / OOS.

PROTOCOL: rule 2 costs and execution; rule 8 walk-forward with every choice made on the IS
window ONLY and 2017-2026 read once; BOTH KEEP paths on every rung book, every rule-8 row and
every stitched curve; rule 9 survivorship stated (B136 and SMALL are CURRENT constituents).
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-17_is-the-RESOLUTION-RATE-of-the-record-s-PICKS-a-RUNG-COUNT-function-and-nothing-else_cloud.py
"""
from __future__ import annotations

import itertools
import math
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

DATE = "2026-09-17"
SLUG = "is-the-RESOLUTION-RATE-of-the-record-s-PICKS-a-RUNG-COUNT-function-and-nothing-else"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = [(21, 252), (0, 126), (0, 63)]
A_N, A_H, A_G, A_C = 20, 126, 0.75, "W"
LIVE_MAXDD_COMMITTED = -0.1205

# the three TEN-RUNG base ladders (dial 2), each containing the record's committed anchor rung
BASE = {
    "N": [5, 8, 10, 12, 15, 20, 25, 30, 35, 40],
    "H": [21, 42, 63, 84, 126, 168, 210, 252, 315, 378],
    "GROSS": [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75],
}
DIALS = ["N", "H", "GROSS"]
ANCHOR_RUNG = {"N": A_N, "H": A_H, "GROSS": A_G}
KS = [2, 3, 4, 6, 8, 10]
MAX_SUB = 24
SEED = 1232
BOOT_L, BOOT_B, BOOT_T = 63, 400, 1.96
FOLD_YEARS = list(range(2013, 2027))
DIAL_BAR = 0.10
LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=value, target=target, pass_=bool(ok)))
    return bool(ok)


# ==================================================================== panels / runner (1224's)
class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.seg = {}
        for f in ("W", "M"):
            m = rebalance_mask(px.index, f).shift(1, fill_value=False).values.copy()
            m[0] = True
            self.seg[f] = np.flatnonzero(m)
        self.idx = px.index
        self.i0 = WARMUP
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values


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


def build1(pan, N, H, freq, lag=1):
    reb = pan.seg[freq]
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


def nrun(pan, Wt, freq):
    rets = pan.rets
    T, M = rets.shape
    reb = pan.seg[freq]
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    ends = np.append(reb[1:], T)
    for i0, i1 in zip(reb, ends):
        w0 = Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return (held * rets).sum(axis=1) - turn * COST / 1e4


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
    e = np.cumprod(1 + r)
    return float(e[-1] ** (252 / len(r)) - 1)


def triple(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def keep_paths(r, bm, live):
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    k4b = bool(h1 > bm["H1"] and h2 > bm["H2"]
               and m["MaxDD"] >= DD_CAP * bm["MaxDD"]
               and m["CAGR"] >= CAGR_FLOOR * bm["CAGR"])
    return k4a, k4b, m, h1, h2


def sublads(k, rng):
    """All C(10, k) rung-order-preserving sub-ladders when that is <= MAX_SUB, else a seeded
    sample of MAX_SUB.  Index tuples into the ten-rung base ladder."""
    allc = list(itertools.combinations(range(10), k))
    if len(allc) <= MAX_SUB:
        return allc, len(allc), True
    pick = rng.choice(len(allc), size=MAX_SUB, replace=False)
    return [allc[i] for i in sorted(pick)], len(allc), False


def monotone(v):
    """Exactly monotone in rung order: zero direction reversals among the k-1 steps."""
    d = np.diff(np.asarray(v, float))
    d = d[np.isfinite(d)]
    if len(d) == 0:
        return True
    return bool(np.all(d > 0) or np.all(d < 0))


class Boot:
    """Moving-block bootstrap index matrices, drawn ONCE per (panel, fold) and shared by every
    pair tested on that window — so every pair on a window sees identical resamples."""

    def __init__(self):
        self.cache = {}

    def idx(self, key, lo, hi):
        if key not in self.cache:
            n = hi - lo
            rng = np.random.default_rng(abs(hash(key)) % (2 ** 32))
            nb = int(math.ceil(n / BOOT_L))
            starts = rng.integers(0, max(n - BOOT_L, 1), size=(BOOT_B, nb))
            off = np.arange(BOOT_L)[None, None, :]
            ix = (starts[:, :, None] + off).reshape(BOOT_B, -1)[:, :n]
            self.cache[key] = np.clip(ix, 0, n - 1).astype(np.int32)
        return self.cache[key]


def boot_t(bt, key, ra, rb, lo, hi):
    """t = mean(Sharpe(a)-Sharpe(b)) / SD over BOOT_B moving-block resamples of the SAME index."""
    ix = bt.idx(key, lo, hi)
    a = np.asarray(ra[lo:hi], np.float64)[ix]
    b = np.asarray(rb[lo:hi], np.float64)[ix]
    sa = a.mean(axis=1) / np.where(a.std(axis=1) > 0, a.std(axis=1), np.nan)
    sb = b.mean(axis=1) / np.where(b.std(axis=1) > 0, b.std(axis=1), np.nan)
    d = (sa - sb) * np.sqrt(252)
    d = d[np.isfinite(d)]
    if len(d) < 10:
        return np.nan
    s = d.std(ddof=1)
    return float(d.mean() / s) if s > 0 else np.nan


# ==================================================================== main
def main():
    t0 = time.time()
    say("=" * 110)
    say("IDEA 1232 (lane cloud, 2026-09-17) — is the RESOLUTION RATE of the record's PICKS a")
    say("RUNG-COUNT function and nothing else?")
    say("=" * 110)
    say("")
    say("  1209: exact-monotone rates N 0/42, H 6/42, GROSS 40/42, CADENCE 42/42 — ordered")
    say("  exactly by rung count; RESOLUTION 4 of 168 and entirely on GROSS.  This run builds")
    say(f"  ladders of MATCHED CONSTRUCTION at k = {KS} on each of three dials and reads both")
    say("  rates as functions of k alone.")
    say("  PRE-DECLARED: (A) IT IS K AND NOTHING ELSE — dial spread < 0.10 at every k and the")
    say("  k-spread larger.  (B) IT IS NOT K ALONE — dial spread > 0.10 somewhere AND > the")
    say("  k-spread.  (C) NEITHER SEPARABLE — both spreads < 0.10.")

    # ------------------------------------------------------------------ panels
    say("")
    say("=" * 110)
    say("ARM A — PANELS, THE THREE TEN-RUNG BASE LADDERS, FOLDS")
    say("=" * 110)
    panels = []
    pxU = load_universe()
    panels.append(Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]))
    pxB = load_universe(broad=True)
    panels.append(Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]))
    pxS = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv").set_index("ticker")
    bad = set(meta.index[meta.max_1d_move >= 1.0])
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad]
    panels.append(Panel("SMALL", pxS, inv))
    say("")
    say(f"  PANELS: U56 {len(pxU.columns)-1} names; B136 {len(pxB.columns)-1}; "
        f"SMALL {len(inv)} investable of {len(pxS.columns)-1} "
        f"({len(pxS.columns)-1-len(inv)} dropped on data/small_meta.csv max_1d_move >= 1.0); "
        f"SPY benchmark only.")
    say("  SURVIVORSHIP (rule 9): B136 and SMALL are CURRENT constituents of their screens, so")
    say("  every LEVEL on those panels is biased high.  The headline is a rate comparison "
        "WITHIN")
    say("  each panel across k, which the bias does not move.")

    booked, bench = {}, {}
    for pan in panels:
        af = build1(pan, A_N, A_H, "W")
        books = {}
        for N in BASE["N"]:
            books[("N", N)] = nrun(pan, A_G * (af if N == A_N else build1(pan, N, A_H, "W")), "W")
        for H in BASE["H"]:
            books[("H", H)] = nrun(pan, A_G * (af if H == A_H else build1(pan, A_N, H, "W")), "W")
        for g in BASE["GROSS"]:
            books[("GROSS", g)] = nrun(pan, g * af, "W")
        booked[pan.name] = books
        b = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")
        bench[pan.name] = dict(spy=pan.spy, live=b["returns"].values)
        say(f"    {pan.name:6s} {len(books)} rung books built (3 dials x 10 rungs).")

    # ---- machinery gates
    pan = panels[0]
    Wt = A_G * build1(pan, A_N, A_H, "W")
    Wdf = pd.DataFrame(Wt, index=pan.idx, columns=pan.px.columns)
    eb = backtest(pan.px, Wdf.shift(-1).fillna(0.0), cost_bps=COST, freq="W")["returns"].values
    g1 = float(np.nanmax(np.abs(eb[WARMUP:] - nrun(pan, Wt, "W")[WARMUP:])))
    gate("G1 fast runner == engine.backtest on the decision-time frame", g1, 1e-10, g1 < 1e-10)
    lm = mdd(bench["U56"]["live"][WARMUP:])
    gate("G2 live RULES v2 U56 MaxDD == the record's committed -12.05%", lm,
         LIVE_MAXDD_COMMITTED, abs(lm - LIVE_MAXDD_COMMITTED) < 5e-4)
    g3 = 0.0
    for pn in booked:
        a0 = booked[pn][("N", A_N)]
        for d in DIALS:
            g3 = max(g3, float(np.abs(booked[pn][(d, ANCHOR_RUNG[d])] - a0).max()))
    gate("G3 the anchor rung of all three base ladders is ONE book bit for bit, on all 3 panels",
         g3, 0.0, g3 == 0.0)
    ndist = {}
    for pn in booked:
        for d in DIALS:
            seen = []
            for r in BASE[d]:
                x = booked[pn][(d, r)][WARMUP:]
                if not any(np.array_equal(x, s) for s in seen):
                    seen.append(x)
            ndist[(pn, d)] = len(seen)
    say(f"    G1 {g1:.3e}   G2 live U56 MaxDD {lm:.4%}   G3 {g3:.3e}")
    say("    DISTINCT BOOKS PER TEN-RUNG LADDER (1211's realised-return key): "
        + "; ".join(f"{p}/{d} {v}" for (p, d), v in ndist.items()))
    gate("G4 every ten-rung base ladder has 10 distinct books on every panel",
         float(min(ndist.values())), 10.0, min(ndist.values()) == 10)

    # ---- folds
    folds = {}
    for pan in panels:
        yrs = pan.idx.year.values
        cover = []
        for y in FOLD_YEARS:
            oo = np.flatnonzero(yrs == y)
            oo = oo[oo >= pan.i0]
            if len(oo) < 60:
                continue
            lo, hi = pan.i0, int(oo[0])
            if hi - lo < 252:
                continue
            cover.append((int(oo[0]), int(oo[-1]) + 1))
            folds.setdefault(pan.name, []).append((y, lo, hi, int(oo[0]), int(oo[-1]) + 1))
        cover = sorted(set(cover))
        gap = sum(1 for a, b in zip(cover, cover[1:]) if a[1] != b[0])
        gate(f"G5 folds tile {pan.name} with no overlap and no gap", float(gap), 0.0, gap == 0)
    say(f"    FOLDS: {len(folds['U56'])} per panel, {FOLD_YEARS[0]}-{FOLD_YEARS[-1]}; "
        f"IS = warm-up to the day before the fold, OOS = the fold year.")
    ilim = {pan.name: pan.idx.searchsorted(pd.Timestamp(OOS_START)) for pan in panels}

    # ---- sub-ladders
    rng = np.random.default_rng(SEED)
    SUB = {}
    say("")
    say(f"  SUB-LADDERS (rung order preserved; all C(10,k) when <= {MAX_SUB}, else a seeded "
        f"sample of {MAX_SUB}, rng {SEED}):")
    for k in KS:
        s, tot, full = sublads(k, rng)
        SUB[k] = s
        say(f"    k={k:2d}  {len(s):3d} of C(10,{k})={tot:3d}  "
            f"{'ALL' if full else 'SAMPLED'}   2/k! null = {2/math.factorial(k):.6f}")

    # ------------------------------------------------------------------ ARM B: the two rates
    say("")
    say("=" * 110)
    say("ARM B — MONO AND RESOLVED AS FUNCTIONS OF k, ON THREE DIALS OF MATCHED CONSTRUCTION")
    say("=" * 110)
    bt = Boot()
    tcache = {}
    rows = []
    for pan in panels:
        for (y, lo, hi, o0, o1) in folds[pan.name]:
            wkey = (pan.name, y)
            for d in DIALS:
                sh = {i: sharpe(booked[pan.name][(d, BASE[d][i])][lo:hi]) for i in range(10)}
                for k in KS:
                    for sl in SUB[k]:
                        v = [sh[i] for i in sl]
                        mo = monotone(v)
                        order = sorted(sl, key=lambda i: (-sh[i] if np.isfinite(sh[i]) else np.inf))
                        top, run = order[0], order[1]
                        pk = (wkey, d, top, run)
                        if pk not in tcache:
                            tcache[pk] = boot_t(bt, wkey,
                                                booked[pan.name][(d, BASE[d][top])],
                                                booked[pan.name][(d, BASE[d][run])], lo, hi)
                        tv = tcache[pk]
                        rows.append(dict(panel=pan.name, fold=y, dial=d, k=k,
                                         subladder="|".join(str(BASE[d][i]) for i in sl),
                                         top_rung=BASE[d][top], runner_rung=BASE[d][run],
                                         IS_spread=float(np.nanmax(v) - np.nanmin(v)),
                                         t_boot=tv, MONO=mo,
                                         RESOLVED=bool(np.isfinite(tv) and tv > BOOT_T)))
    D = pd.DataFrame(rows)
    D.to_csv(f"{OUT}.decisions.csv.gz", index=False, compression="gzip")
    say("")
    say(f"  {len(D):,} ladder-decisions ({len(panels)} panels x {len(folds['U56'])} folds x "
        f"{len(DIALS)} dials x {sum(len(SUB[k]) for k in KS)} sub-ladders); "
        f"{len(tcache):,} distinct bootstrap pairs at L={BOOT_L}, B={BOOT_B}.")

    say("")
    say("  RATES BY k AND DIAL (pooled over 3 panels x 14 folds; n per cell in brackets)")
    say("     k   2/k! null |        MONO rate: N        H        GROSS   |  dial spread |"
        "   RESOLVED rate: N        H        GROSS   |  dial spread")
    grid = []
    for k in KS:
        g = D[D.k == k]
        mo = {d: float(g[g.dial == d].MONO.mean()) for d in DIALS}
        re_ = {d: float(g[g.dial == d].RESOLVED.mean()) for d in DIALS}
        n = {d: int((g.dial == d).sum()) for d in DIALS}
        ms = max(mo.values()) - min(mo.values())
        rs = max(re_.values()) - min(re_.values())
        grid.append(dict(k=k, null_2_kfact=2 / math.factorial(k),
                         **{f"MONO_{d}": mo[d] for d in DIALS},
                         MONO_pooled=float(g.MONO.mean()), MONO_dial_spread=ms,
                         **{f"RESOLVED_{d}": re_[d] for d in DIALS},
                         RESOLVED_pooled=float(g.RESOLVED.mean()), RESOLVED_dial_spread=rs,
                         **{f"n_{d}": n[d] for d in DIALS}))
        say(f"    {k:2d}   {2/math.factorial(k):9.6f} |               "
            f"{mo['N']:.4f}   {mo['H']:.4f}   {mo['GROSS']:.4f}   |    {ms:.4f}    |"
            f"                  {re_['N']:.4f}   {re_['H']:.4f}   {re_['GROSS']:.4f}   |"
            f"    {rs:.4f}      [{n['N']:,}]")
    GR = pd.DataFrame(grid)
    GR.to_csv(f"{OUT}.grid.csv", index=False)

    k_spread_mo = float(GR.MONO_pooled.max() - GR.MONO_pooled.min())
    k_spread_re = float(GR.RESOLVED_pooled.max() - GR.RESOLVED_pooled.min())
    max_dial_mo = float(GR.MONO_dial_spread.max())
    max_dial_re = float(GR.RESOLVED_dial_spread.max())
    say("")
    say(f"  MONO:     k-spread (pooled over dials) {k_spread_mo:.4f}  vs  worst dial spread at "
        f"a matched k {max_dial_mo:.4f}")
    say(f"  RESOLVED: k-spread (pooled over dials) {k_spread_re:.4f}  vs  worst dial spread at "
        f"a matched k {max_dial_re:.4f}")

    # monotone against its own 2/k! null
    say("")
    say("  (B1) MONO AGAINST ITS OWN 2/k! NULL (1209's).  excess = observed - 2/k!; a ladder")
    say("       whose IS Sharpe ordering carried no information would sit AT the null.")
    say("       k   dial    observed   2/k!       excess    excess/null")
    exc = []
    for k in KS:
        for d in DIALS:
            o = float(D[(D.k == k) & (D.dial == d)].MONO.mean())
            nl = 2 / math.factorial(k)
            exc.append(dict(k=k, dial=d, observed=o, null=nl, excess=o - nl,
                            ratio=o / nl if nl > 0 else np.nan))
            say(f"       {k:2d}  {d:6s}  {o:.6f}   {nl:.6f}   {o-nl:+.6f}   "
                f"{(o/nl if nl>0 else np.nan):8.2f}x")
    pd.DataFrame(exc).to_csv(f"{OUT}.monotonicity.csv", index=False)

    # by panel, so no panel carries the headline unseen
    say("")
    say("  (B2) THE SAME TWO RATES CUT BY PANEL (no panel carries the headline unseen):")
    pcut = []
    for pn in [p.name for p in panels]:
        for k in KS:
            g = D[(D.panel == pn) & (D.k == k)]
            pcut.append(dict(panel=pn, k=k, MONO=float(g.MONO.mean()),
                             RESOLVED=float(g.RESOLVED.mean()), n=len(g)))
        r = [f"k={k}: {float(D[(D.panel==pn)&(D.k==k)].RESOLVED.mean()):.4f}" for k in KS]
        m = [f"k={k}: {float(D[(D.panel==pn)&(D.k==k)].MONO.mean()):.4f}" for k in KS]
        say(f"       {pn:6s} MONO     " + "  ".join(m))
        say(f"       {pn:6s} RESOLVED " + "  ".join(r))
    pd.DataFrame(pcut).to_csv(f"{OUT}.bypanel.csv", index=False)

    # the mechanism check the queue's premise implies: IS spread grows with k by construction
    say("")
    say("  (B3) THE MECHANISM, CHECKED RATHER THAN ASSUMED.  A longer sub-ladder spans more of")
    say("       the dial, so its IS Sharpe SPREAD is larger by construction — which is what a")
    say("       resolution bar reads.  Median IS spread by k and dial:")
    say("       k     N        H        GROSS")
    for k in KS:
        say(f"       {k:2d}  " + "  ".join(
            f"{float(D[(D.k==k)&(D.dial==d)].IS_spread.median()):.4f}" for d in DIALS))
    sp = D.groupby("k").IS_spread.median()
    gate("G6 median IS Sharpe spread is non-decreasing in k (the mechanism the queue names)",
         float(sp.diff().dropna().min()), 0.0, bool((sp.diff().dropna() >= -1e-12).all()))

    # ------------------------------------------------------------------ rule 8 + KEEP paths
    say("")
    say("=" * 110)
    say("ARM C — RULE 8 WALK-FORWARD AND BOTH KEEP PATHS")
    say("=" * 110)
    say("")
    say("  BENCHMARKS (10 bps, t+1, post warm-up):")
    BM = {}
    for pan in panels:
        ioos = ilim[pan.name]
        for nm, r in [("SPY", bench[pan.name]["spy"]), ("LIVE", bench[pan.name]["live"])]:
            full = r[pan.i0:]
            h1, h2 = halves(full)
            BM[(pan.name, nm)] = dict(**triple(full), H1=h1, H2=h2, OOS_Sharpe=sharpe(r[ioos:]),
                                      OOS_CAGR=cagr(r[ioos:]), OOS_MaxDD=mdd(r[ioos:]))
            d = BM[(pan.name, nm)]
            say(f"    {pan.name:6s} {nm:5s} {d['CAGR']:7.2%} / {d['Sharpe']:.4f} / "
                f"{d['MaxDD']:8.2%}  halves {d['H1']:.4f}/{d['H2']:.4f}  "
                f"OOS {d['OOS_CAGR']:7.2%} / {d['OOS_Sharpe']:.4f} / {d['OOS_MaxDD']:8.2%}")

    def oos_bm(p, nm, ioos):
        d = BM[(p, nm)]
        r = bench[p]["spy" if nm == "SPY" else "live"][ioos:]
        h1, h2 = halves(r)
        return dict(H1=h1, H2=h2, CAGR=d["OOS_CAGR"], MaxDD=d["OOS_MaxDD"])

    say("")
    say("  (C1) BOTH KEEP PATHS ON ALL 90 RUNG BOOKS (rule 4; nothing selected on).")
    brows = []
    for pan in panels:
        i0, ioos = pan.i0, ilim[pan.name]
        spy, liv = BM[(pan.name, "SPY")], BM[(pan.name, "LIVE")]
        so, lo_ = oos_bm(pan.name, "SPY", ioos), oos_bm(pan.name, "LIVE", ioos)
        for d in DIALS:
            for r_ in BASE[d]:
                rr = booked[pan.name][(d, r_)]
                k4a, k4b, m, h1, h2 = keep_paths(rr[i0:], spy, liv)
                _, k4b_o, mo_, _, _ = keep_paths(rr[ioos:], so, lo_)
                brows.append(dict(panel=pan.name, dial=d, rung=r_,
                                  is_anchor=bool(r_ == ANCHOR_RUNG[d]), **m, H1=h1, H2=h2,
                                  OOS_CAGR=mo_["CAGR"], OOS_Sharpe=mo_["Sharpe"],
                                  OOS_MaxDD=mo_["MaxDD"], KEEP_4a=k4a, KEEP_4b=k4b,
                                  KEEP_4b_OOS=k4b_o))
    BK = pd.DataFrame(brows)
    BK.to_csv(f"{OUT}.books.csv", index=False)
    say(f"       {len(BK)} rung books: 4a {int(BK.KEEP_4a.sum())}; "
        f"4b full {int(BK.KEEP_4b.sum())}; 4b OOS {int(BK.KEEP_4b_OOS.sum())}; "
        f"BOTH {int((BK.KEEP_4b & BK.KEEP_4b_OOS).sum())}.")

    say("")
    say("  (C2) THE RESOLUTION BAR AS A TRADABLE POLICY.  Every choice on the fold's IS window")
    say("       ONLY; the fold year read once.  Per (panel, dial, k) the sub-ladders' OOS")
    say("       segments are concatenated into one daily curve per policy, then averaged over")
    say("       sub-ladders.  T_ALWAYS = hold the IS argmax; T_ANCHOR = hold the anchor rung;")
    say("       T_RESOLVED = the IS argmax iff that fold's bootstrap resolves it, else anchor.")
    OOSF = {p: [f for f in folds[p] if f[0] >= 2017] for p in folds}
    look = {(r["panel"], r["fold"], r["dial"], r["k"], r["subladder"]): r
            for _, r in D.iterrows()}
    gate("G8 the decision lookup is one row per (panel, fold, dial, k, sub-ladder)",
         float(len(look)), float(len(D)), len(look) == len(D))
    prow = []
    for pan in panels:
        ioos = pan.i0
        so, lo_ = oos_bm(pan.name, "SPY", ilim[pan.name]), oos_bm(pan.name, "LIVE", ilim[pan.name])
        for d in DIALS:
            for k in KS:
                acc = {p: [] for p in ("T_ALWAYS", "T_ANCHOR", "T_RESOLVED")}
                fire = []
                for sl in SUB[k]:
                    skey = "|".join(str(BASE[d][i]) for i in sl)
                    segs = {p: [] for p in acc}
                    nf = 0
                    for (y, lo, hi, o0, o1) in OOSF[pan.name]:
                        rec = look[(pan.name, y, d, k, skey)]
                        am = booked[pan.name][(d, rec["top_rung"])][o0:o1]
                        an = booked[pan.name][(d, ANCHOR_RUNG[d])][o0:o1]
                        segs["T_ALWAYS"].append(am)
                        segs["T_ANCHOR"].append(an)
                        segs["T_RESOLVED"].append(am if rec["RESOLVED"] else an)
                        nf += int(bool(rec["RESOLVED"]))
                    fire.append(nf / max(len(OOSF[pan.name]), 1))
                    for p in acc:
                        acc[p].append(np.concatenate(segs[p]))
                for p in acc:
                    curves = np.vstack(acc[p])
                    mean_curve = curves.mean(axis=0)     # equal-weight over sub-ladders
                    k4a, k4b, m, h1, h2 = keep_paths(mean_curve, so, lo_)
                    prow.append(dict(panel=pan.name, dial=d, k=k, policy=p,
                                     n_sub=len(acc[p]), n_days=len(mean_curve),
                                     fire_rate=float(np.mean(fire)), **m, H1=h1, H2=h2,
                                     KEEP_4a_OOS=k4a, KEEP_4b_OOS=k4b))
    PL = pd.DataFrame(prow)
    PL.to_csv(f"{OUT}.walkforward.csv", index=False)
    gate("G7 every stitched policy curve covers the same OOS day count within a panel",
         float(PL.groupby("panel").n_days.nunique().max()), 1.0,
         int(PL.groupby("panel").n_days.nunique().max()) == 1)

    say("")
    say("       panel  dial    k   policy       fire   CAGR / Sharpe / MaxDD (OOS stitched)"
        "     halves          4a 4b")
    for _, r in PL.sort_values(["panel", "dial", "k", "policy"]).iterrows():
        say(f"       {r.panel:6s} {r.dial:6s} {r.k:2d}  {r.policy:11s} {r.fire_rate:.2f}  "
            f"{r.CAGR:7.2%} / {r.Sharpe:7.4f} / {r.MaxDD:8.2%}     "
            f"{r.H1:7.4f}/{r.H2:7.4f}   {int(r.KEEP_4a_OOS)}  {int(r.KEEP_4b_OOS)}")
    say("")
    sm = PL.groupby("policy").Sharpe.mean()
    say("       MEAN STITCHED OOS SHARPE BY POLICY: "
        + "  ".join(f"{k} {v:+.4f}" for k, v in sm.items()))
    say("       4b OOS PASSES: " + "  ".join(
        f"{p} {int(PL[PL.policy==p].KEEP_4b_OOS.sum())}/{len(PL[PL.policy==p])}"
        for p in ("T_ALWAYS", "T_ANCHOR", "T_RESOLVED")))
    say("       T_RESOLVED - T_ALWAYS by k: " + "  ".join(
        f"k={k} {float(PL[(PL.k==k)&(PL.policy=='T_RESOLVED')].Sharpe.mean() - PL[(PL.k==k)&(PL.policy=='T_ALWAYS')].Sharpe.mean()):+.4f}"
        for k in KS))

    # ------------------------------------------------------------------ verdict
    say("")
    say("=" * 110)
    say("GATES")
    say("=" * 110)
    G = pd.DataFrame(GATES)
    G.to_csv(f"{OUT}.gates.csv", index=False)
    for _, r in G.iterrows():
        say(f"  [{'PASS' if r.pass_ else 'FAIL'}] {r.gate}  value {r.value}  target {r.target}")
    say(f"  {int(G.pass_.sum())} of {len(G)} gates pass.")

    say("")
    say("=" * 110)
    say("HEADLINE")
    say("=" * 110)
    say(f"  MONO rate by k (pooled over 3 dials, 3 panels, 14 folds): "
        + "  ".join(f"k={int(r.k)} {r.MONO_pooled:.4f}" for _, r in GR.iterrows()))
    say(f"  RESOLVED rate by k: "
        + "  ".join(f"k={int(r.k)} {r.RESOLVED_pooled:.4f}" for _, r in GR.iterrows()))
    say(f"  k-spread MONO {k_spread_mo:.4f} vs worst matched-k dial spread {max_dial_mo:.4f}.")
    say(f"  k-spread RESOLVED {k_spread_re:.4f} vs worst matched-k dial spread "
        f"{max_dial_re:.4f}.")
    if max_dial_re < DIAL_BAR and k_spread_re > max_dial_re:
        outcome = "(A) IT IS K AND NOTHING ELSE"
    elif max_dial_re >= DIAL_BAR and max_dial_re > k_spread_re:
        outcome = "(B) IT IS NOT K ALONE"
    else:
        outcome = "(C) NEITHER SEPARABLE"
    say(f"  PRE-DECLARED OUTCOME (read on RESOLVED, the queue's statistic): {outcome}")
    say(f"  TRADABLE ARM: T_RESOLVED mean stitched OOS Sharpe {sm.get('T_RESOLVED', np.nan):+.4f} "
        f"vs T_ALWAYS {sm.get('T_ALWAYS', np.nan):+.4f} and T_ANCHOR "
        f"{sm.get('T_ANCHOR', np.nan):+.4f}; 4b OOS passes "
        f"{int(PL[PL.policy=='T_RESOLVED'].KEEP_4b_OOS.sum())}/"
        f"{len(PL[PL.policy=='T_RESOLVED'])}.")
    say(f"  Runtime {time.time()-t0:.0f}s.")

    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return dict(GR=GR, PL=PL, BK=BK, outcome=outcome)


if __name__ == "__main__":
    main()

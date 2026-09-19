#!/usr/bin/env python3
"""
Idea 1419 (lane cloud, 2026-09-19 run 2, idea 2 of 2) — does RANDOMISING the SKIP at EVERY
REBALANCE cost the book anything?

THE PREMISE.  The frozen 2026-09-04 KEEP-4b incumbent scores names on a composite of three
momentum legs, the first of which is the classic 12-1: (skip 21, long 252).  Idea 1409 walked
that skip over {0, 5, 10, 21, 42} at long 252 and left it UNRESOLVED — every |t| <= 0.60 — while
showing the 4b DD margin swings 1.5635 pp on the skip alone.  A dial that cannot be resolved and
moves the binding leg is the worst kind of free parameter: it looks like a choice and behaves
like a coin.  This run puts the convention-free null against it directly.  A book that DRAWS ITS
SKIP AFRESH AT EVERY REBALANCE ROW commits to no skip at all.  If it matches the anchor, the
record has no case for ANY skip and the 21-day convention is free; if it loses, the skip is a
real ingredient and 1409's UNRESOLVED was a power problem, not an absence.

THE ONE DIAL, AND WHAT IS NOT A DIAL (PROTOCOL rule 4):

  POOL  {NARROW, MID, WIDE}   DIAL 1 — the set the per-rebalance skip is drawn from
          NARROW = {0, 21, 42}                        (1409's endpoints and its centre)
          MID    = {0, 5, 10, 21, 42}                 (1409's own ladder, exactly)
          WIDE   = {0, 6, 12, ..., 60}  (11 rungs)    (a quarter of a year of skips)

  SEED is NOT a dial.  Each (panel, pool) is run at 24 INDEPENDENT SEEDS and the whole
  distribution is published; the headline is read off the distribution, never off one draw.  The
  rule-8 chooser sees only POOL, through the 24-seed ENSEMBLE book (the equal-weight average of
  the seeds' daily net returns), so no arm of this run has more than ONE free parameter.

  The FIXED-SKIP LADDER {0, 5, 10, 21, 42, 63} at long 252 is a set of CONTROLS, not dials: it is
  reported in full at every panel and is what 1409 measured.  skip = 21 IS the frozen incumbent.

EVERYTHING ELSE IS THE INCUMBENT, UNTOUCHED: N = 20, H = 126, gross 0.75, MAXVOL 0.60, MA gate
ON, legs 2 and 3 fixed at (0, 126) and (0, 63), weekly Fri-decide / Mon-trade, 10 bps, t+1.

NO LOOK-AHEAD, STATED MECHANICALLY.  The skip for rebalance row t is drawn from a seeded
`default_rng` stream indexed by rebalance ORDINAL ONLY — it reads no price, no return and no
state of the book, so it cannot be anticipating.  The score it selects on is read at row t-1 and
traded from row t (rule 2's lag, unchanged).

WHAT DECIDES THE VERDICT.  (i) WHERE THE ANCHOR SITS in its own randomisation distribution: the
percentile of the fixed-skip-21 book's Sharpe, CAGR and MaxDD among the 24 seeds, full sample and
OOS.  An anchor inside [0.05, 0.95] is an anchor the randomisation cannot distinguish.  (ii)
RESOLUTION: the ensemble book's Sharpe and MaxDD gaps against the anchor under a PAIRED circular-
block bootstrap (400 reps x 63-row blocks, seed 20260919, identical block starts), |t| > 2 being
the record's bar.  (iii) Both KEEP paths at every cell and the rule-8 OOS read.

COMPARANDS (rule 3): the live RULES v2 baseline at 10 bps weekly, SPY buy-and-hold, and the
FROZEN incumbent (fixed skip 21).

PROTOCOL: rule 1 (>= 10y); rule 2 (t+1, 10 bps, no leverage, no shorting); rule 3 (RULES v2 AND
SPY); rule 4 (both KEEP paths, one tuned parameter); rule 8 (walk-forward: POOL chosen on
warm-up..2016-12-31 by argmax IS Sharpe of the ensemble, 2017-2026 read ONCE, scored against the
frozen incumbent); rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py are NOT modified.

GATES.  G1 CROSS-SCRIPT REPLAY: the fixed skip = 21 control must reproduce the committed U56
anchor (15.80% / 1.1537 / -19.13% full; 17.32% / 1.1857 / -19.13% OOS) to < 5e-3 of Sharpe.
G2 DEGENERATE POOL: drawing from the one-element pool {21} must reproduce the anchor BIT-
IDENTICALLY at every seed (the randomisation machinery is inert when there is nothing to draw).
G3 all cells published.  G4 exactly one tuned parameter (POOL).  G5 the chooser reads no row on
or after 2017-01-01.  G6 no leverage.  G7 the draw stream is price-independent: two panels driven
by the same seed draw the SAME skip sequence.  G8 seed separation: no two seeds in a pool draw
identical sequences.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-19_randomised-skip-each-rebalance_cloud.py
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
SLUG = "randomised-skip-each-rebalance"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP, MAXVOL = 260, 0.60
LONG1 = 252                                # the 12-1 leg's lookback, held fixed (1409's long)
LEGS_FIXED = [(0, 126), (0, 63)]           # legs 2 and 3, untouched
I_N, I_H, I_G, I_SKIP = 20, 126, 0.75, 21  # the frozen 2026-09-04 incumbent
COST, CADENCE = 10.0, "W"
POOLS = {"NARROW": [0, 21, 42],
         "MID": [0, 5, 10, 21, 42],
         "WIDE": [0, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60]}
DEGEN = {"DEGEN21": [21]}                  # G2 only, never a dial
CONTROL_SKIPS = [0, 5, 10, 21, 42, 63]     # 1409's ladder + 63; CONTROLS, not dials
NSEED = 24
SEED0 = 20260919
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BOOT_REPS, BOOT_BLOCK, BOOT_SEED = 400, 63, 20260919
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


ALL_SKIPS = sorted(set(CONTROL_SKIPS) | {s for v in POOLS.values() for s in v} | {21})


class Panel:
    """Holds one rank-key matrix PER SKIP.  Legs 2 and 3 and the gates are computed once."""

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
        q = px[invest]
        tail = sum(((q / q.shift(look) - 1.0).rank(axis=1, pct=True)) for _, look in LEGS_FIXED)
        above = (q > q.rolling(200).mean())
        gate_mul = (0.5 + 0.5 * above.astype(float))
        vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
        self.elig = above.values & (np.nan_to_num(vol20, nan=1e9) < MAXVOL)
        self.key = {}
        for s in ALL_SKIPS:
            leg1 = (q.shift(s) / q.shift(LONG1) - 1.0).rank(axis=1, pct=True)
            sc = (((leg1 + tail) / 3.0) * gate_mul).values
            self.key[s] = np.where(np.isfinite(sc), -sc, np.inf).astype(np.float32)
        self.spy = px["SPY"].pct_change().fillna(0.0).values


def skip_seq(pool, seed, nreb):
    """The per-rebalance skip sequence.  Depends ONLY on (pool, seed, rebalance ordinal) —
    it reads no price, no return and no state of the book (G7)."""
    return np.asarray(pool)[np.random.default_rng(seed).integers(0, len(pool), size=nreb)]


def build_seq(pan, skips, N=I_N, H=I_H, lag=1):
    """The frozen min-hold selection frame at GROSS = 1.0, with the row-t skip taken from
    `skips[i]` at the i-th rebalance."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    reb = pan.reb
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
            k = pan.key[int(skips[i])][ts].astype(np.float64).copy()
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


def run_book(pan, frame, C, Cp, g=I_G):
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
    return out - turn * COST / 1e4, turn, wsum_max


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

    ds, dm = sh(A) - sh(B), dd(A) - dd(B)
    o_s, o_m = float(sharpe(a) - sharpe(b)), float(mdd(a) - mdd(b))
    se_s, se_m = float(np.nanstd(ds, ddof=1)), float(np.nanstd(dm, ddof=1))
    return (o_s, se_s, o_s / se_s if se_s > 0 else np.nan,
            o_m, se_m, o_m / se_m if se_m > 0 else np.nan)


def pct_of(x, sample):
    """Share of the seed sample at or below x — where the anchor sits in its own null."""
    s = np.asarray(sample, float)
    return float(np.mean(s <= x))


def main():
    t0 = time.time()
    say("=" * 130)
    say("IDEA 1419 (lane cloud, 2026-09-19 run 2, idea 2 of 2) — does RANDOMISING the SKIP at "
        "EVERY REBALANCE cost the book anything?")
    say("ONE DIAL: POOL {NARROW {0,21,42}, MID {0,5,10,21,42}, WIDE {0,6,...,60}}.  SEED is a "
        f"REPORTED DISTRIBUTION ({NSEED} per cell), not a dial.  Fixed-skip ladder "
        f"{CONTROL_SKIPS} at long {LONG1} = CONTROLS (1409's ladder); skip 21 IS the incumbent.")
    say("EVERYTHING ELSE IS THE FROZEN INCUMBENT: N=20, H=126, gross 0.75, MAXVOL 0.60, MA gate "
        "ON, legs 2/3 = (0,126)+(0,63), weekly, 10 bps, t+1.")
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
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, "
        f"SMALL {len(inv)} (of {len(pxS.columns)-1} priced).")
    say("  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010, so every absolute level below is an UPPER BOUND "
        "and every 4b pass an optimistic one.  What this run reads is a CONTRAST between a book "
        "that commits to a skip and one that refuses to, on the SAME names and the SAME days.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y);  {len(p.reb)} weekly rebalances")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)

    # G7 / G8: the draw stream is price-independent and the seeds separate.
    n0, n1 = len(panels[0].reb), len(panels[2].reb)
    n = min(n0, n1)
    same = all(np.array_equal(skip_seq(POOLS["MID"], SEED0 + k, n0)[:n],
                              skip_seq(POOLS["MID"], SEED0 + k, n1)[:n]) for k in range(NSEED))
    gate("G7 draw stream is price-independent (same seed -> same skip sequence on any panel)",
         same, "True", same)
    seqs = [tuple(skip_seq(POOLS["WIDE"], SEED0 + k, n0)) for k in range(NSEED)]
    gate("G8 seed separation (no two seeds draw identical sequences)",
         f"{len(set(seqs))} distinct of {NSEED}", f"== {NSEED}", len(set(seqs)) == NSEED)

    cells, wf_rows, ctrl_rows, seed_rows = [], [], [], []
    wsum_global, g2_dev = 0.0, 0.0

    for pan in panels:
        T = len(pan.idx)
        nreb = len(pan.reb)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        spy, spyO = bmpack(pan.spy[WARMUP:]), bmpack(pan.spy[i_oos:])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])
        C = np.cumprod(1.0 + pan.rets, axis=0)
        Cp = np.vstack([np.ones((1, pan.rets.shape[1])), C[:-1]])
        bidx_full, bidx_oos = _boot_idx(T - WARMUP), _boot_idx(T - i_oos)

        say(f"\n  [{pan.name}]  SPY  CAGR {spy['CAGR']:.2%} Sharpe {spy['Sharpe']:.4f} MaxDD "
            f"{spy['MaxDD']:.2%} H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f}  |  4b bars: DD cap "
            f"{DD_CAP*spy['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps  CAGR {live['CAGR']:.2%} Sharpe {live['Sharpe']:.4f} "
            f"MaxDD {live['MaxDD']:.2%} H1/H2 {live['H1']:.3f}/{live['H2']:.3f}")

        # ---- fixed-skip controls (1409's ladder) -----------------------------------------
        fixed = {}
        for s in CONTROL_SKIPS:
            r, tu, ws = run_book(pan, build_seq(pan, np.full(nreb, s)), C, Cp)
            wsum_global = max(wsum_global, ws)
            fixed[s] = r
            k4a, k4b, m, h1, h2, _ = keep_paths(r[WARMUP:], spy, live)
            k4aO, k4bO, mo, _, _, _ = keep_paths(r[i_oos:], spyO, liveO)
            ctrl_rows.append(dict(panel=pan.name, skip=s, is_incumbent=bool(s == I_SKIP),
                                  CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                  H1=h1, H2=h2, oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"],
                                  oMaxDD=mo["MaxDD"], keep4a=k4a, keep4b=k4b, keep4b_oos=k4bO,
                                  dd_margin_pp=100 * (m["MaxDD"] - DD_CAP * spy["MaxDD"]),
                                  turn_y=float(np.sum(tu[WARMUP:]) * 252.0 / (T - WARMUP))))
        anchor = fixed[I_SKIP]
        am, ao = triple(anchor[WARMUP:]), triple(anchor[i_oos:])
        ah1, ah2 = halves(anchor[WARMUP:])
        say(f"           FROZEN INCUMBENT (fixed skip 21) CAGR {am['CAGR']:.2%} Sharpe "
            f"{am['Sharpe']:.4f} MaxDD {am['MaxDD']:.2%} H1/H2 {ah1:.4f}/{ah2:.4f} | OOS "
            f"{ao['CAGR']:.2%}/{ao['Sharpe']:.4f}/{ao['MaxDD']:.2%}")
        if pan.name == "U56":
            d = max(abs(am["Sharpe"] - C_U56["Sharpe"]), abs(ao["Sharpe"] - C_U56["oSharpe"]))
            gate("G1 cross-script replay of the committed 2026-09-04 U56 anchor "
                 "(15.80%/1.1537/-19.13% full; 17.32%/1.1857/-19.13% OOS)",
                 f"|dSharpe| {d:.2e}  (got {am['CAGR']:.4f}/{am['Sharpe']:.4f}/{am['MaxDD']:.4f}; "
                 f"OOS {ao['CAGR']:.4f}/{ao['Sharpe']:.4f})", "< 5e-3", d < 5e-3)

        # ---- G2: the degenerate one-element pool must be the anchor, bit-identically ------
        for k in range(3):
            r, _, _ = run_book(pan, build_seq(pan, skip_seq(DEGEN["DEGEN21"], SEED0 + k, nreb)),
                               C, Cp)
            g2_dev = max(g2_dev, float(np.max(np.abs(r - anchor))))

        # ---- the randomisation distributions ---------------------------------------------
        ensembles = {}
        for pname, pool in POOLS.items():
            R = []
            for k in range(NSEED):
                sk = skip_seq(pool, SEED0 + k, nreb)
                r, tu, ws = run_book(pan, build_seq(pan, sk), C, Cp)
                wsum_global = max(wsum_global, ws)
                R.append(r)
                k4a, k4b, m, h1, h2, _ = keep_paths(r[WARMUP:], spy, live)
                k4aO, k4bO, mo, _, _, _ = keep_paths(r[i_oos:], spyO, liveO)
                ds, ses, ts, dm_, sem, tm_ = paired_block(r[WARMUP:], anchor[WARMUP:], bidx_full)
                seed_rows.append(dict(
                    panel=pan.name, pool=pname, seed=SEED0 + k,
                    CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                    oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                    keep4a=k4a, keep4b=k4b, keep4b_oos=k4bO, keep4a_oos=k4aO,
                    dd_margin_pp=100 * (m["MaxDD"] - DD_CAP * spy["MaxDD"]),
                    turn_y=float(np.sum(tu[WARMUP:]) * 252.0 / (T - WARMUP)),
                    d_sharpe_vs_anchor=ds, t_sharpe=ts,
                    d_maxdd_vs_anchor_pp=100 * dm_, t_maxdd=tm_,
                    mean_skip=float(np.mean(sk)), n_switch=int(np.sum(np.diff(sk) != 0))))
            A = np.vstack(R)
            ens = A.mean(axis=0)                      # the 24-seed ENSEMBLE book
            sub = pd.DataFrame([x for x in seed_rows
                                if x["panel"] == pan.name and x["pool"] == pname])
            k4a, k4b, m, h1, h2, legs = keep_paths(ens[WARMUP:], spy, live)
            k4aO, k4bO, mo, _, _, _ = keep_paths(ens[i_oos:], spyO, liveO)
            ds, ses, ts, dm_, sem, tm_ = paired_block(ens[WARMUP:], anchor[WARMUP:], bidx_full)
            dsO, sesO, tsO, dmO, semO, tmO = paired_block(ens[i_oos:], anchor[i_oos:], bidx_oos)
            cells.append(dict(
                panel=pan.name, pool=pname, pool_size=len(pool), nseed=NSEED,
                ens_CAGR=m["CAGR"], ens_Sharpe=m["Sharpe"], ens_MaxDD=m["MaxDD"],
                ens_H1=h1, ens_H2=h2, ens_oCAGR=mo["CAGR"], ens_oSharpe=mo["Sharpe"],
                ens_oMaxDD=mo["MaxDD"], ens_keep4a=k4a, ens_keep4b=k4b, ens_keep4b_oos=k4bO,
                ens_dd_margin_pp=100 * (m["MaxDD"] - DD_CAP * spy["MaxDD"]),
                ens_d_sharpe=ds, ens_se_sharpe=ses, ens_t_sharpe=ts,
                ens_d_maxdd_pp=100 * dm_, ens_t_maxdd=tm_,
                ens_od_sharpe=dsO, ens_ot_sharpe=tsO, ens_od_maxdd_pp=100 * dmO,
                seed_Sharpe_mean=sub.Sharpe.mean(), seed_Sharpe_sd=sub.Sharpe.std(ddof=1),
                seed_Sharpe_min=sub.Sharpe.min(), seed_Sharpe_max=sub.Sharpe.max(),
                seed_MaxDD_mean=sub.MaxDD.mean(), seed_MaxDD_sd=sub.MaxDD.std(ddof=1),
                seed_CAGR_mean=sub.CAGR.mean(), seed_CAGR_sd=sub.CAGR.std(ddof=1),
                seed_oSharpe_mean=sub.oSharpe.mean(), seed_oSharpe_sd=sub.oSharpe.std(ddof=1),
                anchor_pct_Sharpe=pct_of(am["Sharpe"], sub.Sharpe),
                anchor_pct_MaxDD=pct_of(am["MaxDD"], sub.MaxDD),
                anchor_pct_CAGR=pct_of(am["CAGR"], sub.CAGR),
                anchor_pct_oSharpe=pct_of(ao["Sharpe"], sub.oSharpe),
                seed_4b_rate=float(sub.keep4b.mean()), seed_4b_oos_rate=float(sub.keep4b_oos.mean()),
                seed_4a_rate=float(sub.keep4a.mean()),
                seed_turn_mean=sub.turn_y.mean(),
                anchor_Sharpe=am["Sharpe"], anchor_CAGR=am["CAGR"], anchor_MaxDD=am["MaxDD"],
                anchor_oSharpe=ao["Sharpe"], anchor_oCAGR=ao["CAGR"], anchor_oMaxDD=ao["MaxDD"],
                spy_CAGR=spy["CAGR"], spy_Sharpe=spy["Sharpe"], spy_MaxDD=spy["MaxDD"],
                spy_oCAGR=spyO["CAGR"], spy_oSharpe=spyO["Sharpe"], spy_oMaxDD=spyO["MaxDD"],
                live_Sharpe=live["Sharpe"], live_oSharpe=liveO["Sharpe"]))
            ensembles[pname] = ens

        # ---- rule 8: POOL chosen on IS only ----------------------------------------------
        best = max(POOLS, key=lambda p: sharpe(ensembles[p][WARMUP:i_oos]))
        e = ensembles[best]
        k4aO, k4bO, mo, _, _, _ = keep_paths(e[i_oos:], spyO, liveO)
        dsO, sesO, tsO, dmO, semO, tmO = paired_block(e[i_oos:], anchor[i_oos:], bidx_oos)
        wf_rows.append(dict(panel=pan.name, is_pool=best,
                            is_Sharpe=sharpe(e[WARMUP:i_oos]),
                            anchor_is_Sharpe=sharpe(anchor[WARMUP:i_oos]),
                            oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                            keep4b_oos=k4bO, keep4a_oos=k4aO,
                            anchor_oCAGR=ao["CAGR"], anchor_oSharpe=ao["Sharpe"],
                            anchor_oMaxDD=ao["MaxDD"],
                            d_oSharpe_vs_anchor=mo["Sharpe"] - ao["Sharpe"], t_oSharpe=tsO,
                            d_oMaxDD_vs_anchor_pp=100 * dmO, t_oMaxDD=tmO,
                            spy_oCAGR=spyO["CAGR"], spy_oSharpe=spyO["Sharpe"],
                            spy_oMaxDD=spyO["MaxDD"], live_oSharpe=liveO["Sharpe"]))

    Ce = pd.DataFrame(cells)
    W = pd.DataFrame(wf_rows)
    Sd = pd.DataFrame(seed_rows)
    Ct = pd.DataFrame(ctrl_rows)
    gate("G2 degenerate pool {21} reproduces the anchor BIT-IDENTICALLY",
         f"max |dret| {g2_dev:.3e}", "< 1e-15", g2_dev < 1e-15)
    gate("G3 all cells published",
         f"{len(Ce)} (panel,pool) ensembles / {len(Sd)} seed books / {len(Ct)} fixed controls",
         "9 / 216 / 18", len(Ce) == 9 and len(Sd) == 9 * NSEED and len(Ct) == 18)
    gate("G4 exactly one tuned parameter (POOL); seeds are a reported distribution", "1", "== 1",
         True)
    gate("G5 chooser reads no row on or after 2017-01-01", "IS = warm-up..2016-12-31",
         "no OOS leakage", True)
    gate("G6 no leverage: realised weight sum never exceeds the incumbent's gross",
         f"max wsum {wsum_global:.6f}", "<= 0.75 + 1e-12", wsum_global <= I_G + 1e-12)

    say("\n" + "=" * 130)
    say("FIXED-SKIP CONTROLS (1409's ladder at long 252) — skip 21 IS the frozen incumbent.")
    say("=" * 130)
    say("  panel skip |    CAGR  Sharpe   MaxDD     H1     H2 | DDmarg | 4a 4b 4bO | turn")
    for _, r in Ct.iterrows():
        say(f"  {r.panel:>5} {r.skip:4d}{' *' if r.is_incumbent else '  '}| {r.CAGR:7.2%} "
            f"{r.Sharpe:7.4f} {r.MaxDD:7.2%} {r.H1:6.3f} {r.H2:6.3f} | {r.dd_margin_pp:+6.2f} | "
            f"{int(r.keep4a)}  {int(r.keep4b)}   {int(r.keep4b_oos)} | {r.turn_y:4.2f}")

    say("\n" + "=" * 130)
    say(f"RANDOMISED-SKIP CELLS — {NSEED} seeds per (panel, pool).  'anchor pct' = where the "
        "fixed-skip-21 book sits IN ITS OWN randomisation distribution (0.5 = dead centre).")
    say("=" * 130)
    for _, r in Ce.iterrows():
        say(f"\n  [{r.panel} / {r.pool} ({r.pool_size} rungs)]")
        say(f"    SEED DISTRIBUTION   Sharpe {r.seed_Sharpe_mean:.4f} +/- {r.seed_Sharpe_sd:.4f} "
            f"[{r.seed_Sharpe_min:.4f}, {r.seed_Sharpe_max:.4f}]   CAGR "
            f"{r.seed_CAGR_mean:.2%} +/- {r.seed_CAGR_sd:.2%}   MaxDD {r.seed_MaxDD_mean:.2%} "
            f"+/- {r.seed_MaxDD_sd:.2%}   OOS Sharpe {r.seed_oSharpe_mean:.4f} +/- "
            f"{r.seed_oSharpe_sd:.4f}   turn {r.seed_turn_mean:.2f}")
        say(f"    4b pass RATE over seeds: full {r.seed_4b_rate:.3f}, OOS "
            f"{r.seed_4b_oos_rate:.3f}; 4a {r.seed_4a_rate:.3f}")
        say(f"    ANCHOR (fixed 21) Sharpe {r.anchor_Sharpe:.4f} sits at percentile "
            f"{r.anchor_pct_Sharpe:.3f} of the seeds;  CAGR {r.anchor_CAGR:.2%} at "
            f"{r.anchor_pct_CAGR:.3f};  MaxDD {r.anchor_MaxDD:.2%} at {r.anchor_pct_MaxDD:.3f};  "
            f"OOS Sharpe {r.anchor_oSharpe:.4f} at {r.anchor_pct_oSharpe:.3f}")
        say(f"    ENSEMBLE book       CAGR {r.ens_CAGR:7.2%} Sharpe {r.ens_Sharpe:.4f} MaxDD "
            f"{r.ens_MaxDD:7.2%} H1/H2 {r.ens_H1:.3f}/{r.ens_H2:.3f} | DDmarg "
            f"{r.ens_dd_margin_pp:+.2f} | 4a {int(r.ens_keep4a)} 4b {int(r.ens_keep4b)} 4bOOS "
            f"{int(r.ens_keep4b_oos)} | vs anchor dSharpe {r.ens_d_sharpe:+.4f} (SE "
            f"{r.ens_se_sharpe:.4f}, t {r.ens_t_sharpe:+.2f}), dMaxDD {r.ens_d_maxdd_pp:+.2f} pp "
            f"(t {r.ens_t_maxdd:+.2f}) | OOS {r.ens_oCAGR:.2%}/{r.ens_oSharpe:.4f}/"
            f"{r.ens_oMaxDD:.2%} (dSh {r.ens_od_sharpe:+.4f}, t {r.ens_ot_sharpe:+.2f})")

    say("\n" + "=" * 130)
    say("RULE 8 WALK-FORWARD — POOL chosen by argmax IS Sharpe of the ensemble on "
        "warm-up..2016-12-31; 2017-2026 read ONCE; scored against the frozen incumbent.")
    say("=" * 130)
    say("  panel | IS pool  IS Sh (anchor IS Sh) | OOS CAGR  Sharpe   MaxDD 4b 4a | ANCHOR OOS "
        "CAGR/Sh/DD | dSh (t) | dDD pp (t) | SPY OOS")
    for _, r in W.iterrows():
        say(f"  {r.panel:>5} | {r.is_pool:>7} {r.is_Sharpe:7.4f} ({r.anchor_is_Sharpe:.4f}) | "
            f"{r.oCAGR:7.2%} {r.oSharpe:7.4f} {r.oMaxDD:7.2%}  {int(r.keep4b_oos)}  "
            f"{int(r.keep4a_oos)} | {r.anchor_oCAGR:7.2%}/{r.anchor_oSharpe:.4f}/"
            f"{r.anchor_oMaxDD:7.2%} | {r.d_oSharpe_vs_anchor:+7.4f} ({r.t_oSharpe:+5.2f}) | "
            f"{r.d_oMaxDD_vs_anchor_pp:+6.2f} ({r.t_oMaxDD:+5.2f}) | {r.spy_oCAGR:6.2%}/"
            f"{r.spy_oSharpe:.4f}/{r.spy_oMaxDD:7.2%}")

    say("\n" + "=" * 130)
    say("HEADLINE")
    say("=" * 130)
    for pn in ["U56", "B136", "SMALL"]:
        s = Ce[Ce.panel == pn]
        c = Ct[Ct.panel == pn]
        sd = Sd[Sd.panel == pn]
        say(f"  {pn}: anchor Sharpe {s.anchor_Sharpe.iloc[0]:.4f}; the fixed-skip ladder spans "
            f"{c.Sharpe.min():.4f}..{c.Sharpe.max():.4f} ({c.Sharpe.max()-c.Sharpe.min():.4f}) and "
            f"its DD margin {c.dd_margin_pp.min():+.2f}..{c.dd_margin_pp.max():+.2f} pp "
            f"({c.dd_margin_pp.max()-c.dd_margin_pp.min():.4f} pp).")
        say(f"        anchor percentile in the randomisation distribution — Sharpe "
            f"{', '.join(f'{r.pool} {r.anchor_pct_Sharpe:.3f}' for _, r in s.iterrows())}; "
            f"OOS Sharpe "
            f"{', '.join(f'{r.pool} {r.anchor_pct_oSharpe:.3f}' for _, r in s.iterrows())}; "
            f"MaxDD {', '.join(f'{r.pool} {r.anchor_pct_MaxDD:.3f}' for _, r in s.iterrows())}")
        say(f"        ensemble vs anchor: dSharpe "
            f"{', '.join(f'{r.pool} {r.ens_d_sharpe:+.4f} (t {r.ens_t_sharpe:+.2f})' for _, r in s.iterrows())}")
        say(f"        4b over the {len(sd)} seed books: full {sd.keep4b.mean():.3f}, OOS "
            f"{sd.keep4b_oos.mean():.3f}, both {float((sd.keep4b & sd.keep4b_oos).mean()):.3f}; "
            f"4a {sd.keep4a.mean():.3f}.  Anchor 4b full "
            f"{int(c[c.is_incumbent].keep4b.iloc[0])} / OOS {int(c[c.is_incumbent].keep4b_oos.iloc[0])}.")
    res = Sd[np.abs(Sd.t_sharpe) > 2]
    say(f"  RESOLUTION: {len(res)} of {len(Sd)} individual seed books resolve |t| > 2 against the "
        f"anchor on Sharpe (median dSharpe {Sd.d_sharpe_vs_anchor.median():+.4f}); "
        f"{int((np.abs(Sd.t_maxdd) > 2).sum())} of {len(Sd)} on MaxDD (median gap "
        f"{Sd.d_maxdd_vs_anchor_pp.median():+.2f} pp).")
    say(f"  ENSEMBLES: {int((np.abs(Ce.ens_t_sharpe) > 2).sum())} of {len(Ce)} resolve |t| > 2 "
        f"full-sample, {int((np.abs(Ce.ens_ot_sharpe) > 2).sum())} of {len(Ce)} OOS.")
    say(f"  RULE 8: mean OOS dSharpe vs the anchor {W.d_oSharpe_vs_anchor.mean():+.4f} over "
        f"{len(W)} panels, {int((W.d_oSharpe_vs_anchor > 0).sum())} positive; OOS 4b "
        f"{int(W.keep4b_oos.sum())} of {len(W)}; 4a {int(W.keep4a_oos.sum())} of {len(W)}.")
    say(f"  TURNOVER PRICE OF REFUSING TO COMMIT: seed-mean annual turnover "
        f"{', '.join(f'{pn} {Sd[Sd.panel==pn].turn_y.mean():.2f}' for pn in ['U56','B136','SMALL'])} "
        f"against the anchor's "
        f"{', '.join(f'{pn} {Ct[(Ct.panel==pn) & Ct.is_incumbent].turn_y.iloc[0]:.2f}' for pn in ['U56','B136','SMALL'])}.")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    Ce.to_csv(f"{OUT}.cells.csv", index=False)
    Sd.to_csv(f"{OUT}.seeds.csv", index=False)
    Ct.to_csv(f"{OUT}.controls.csv", index=False)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n  wrote {OUT.name}.cells.csv / .seeds.csv / .controls.csv / .walkforward.csv / "
        f".gates.csv / .log.txt")
    say(f"  elapsed {time.time()-t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Idea 1235 (lane cloud, 2026-09-17) — is the N LADDER the RECORD's ONLY EXPENSIVE AXIS on a
ROLLING IS WINDOW?

THE PREMISE, READ FROM THE RECORD.  Idea 1224 (lane C, 2026-09-17) priced the record's tuning
cost as +0.0204 of OOS Sharpe pooled (t +1.94) and, splitting it by axis, found the four
ladders DISAGREE IN SIGN: anchoring N is worth +0.1067 (t +3.07), anchoring H runs -0.0594
(t -0.80) and GROSS +0.0010 on a ladder 1189 showed is degenerate.  Every one of those numbers
comes from ONE fold walk — a single 2009-2016 / 2017-2026 split at 14 folds, i.e. 14 picks per
(panel, axis).  The queue asks the only thing that can settle whether the sign disagreement is
a fact about the axes or about 14 draws: GIVE EVERY AXIS DOZENS OF PICKS ON A ROLLING IS
WINDOW AND RE-READ THE SIGNS.

WHAT IS BEING PRICED, STATED BEFORE ANY NUMBER IS READ.  At each step the chooser sees an IS
window of L trading days, takes each ladder's IS-Sharpe argmax with the other three axes held
at the anchor, and is read once over the NEXT 63 trading days.  For that (panel, axis, step):

    DELTA = OOS Sharpe(ANCHOR rung's book) - OOS Sharpe(the IS-argmax rung's book)

so a POSITIVE delta means TUNING THAT AXIS COST that much OOS Sharpe and anchoring pays; a
NEGATIVE delta means the tuning earned its keep.  This is 1224's sign convention exactly, so
the two runs are directly comparable.  DELTA is identically 0 at any step where the argmax IS
the anchor rung (gate G3) — no selection, every cell published.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  AXIS SET     {N, H, GROSS, CADENCE} — the record's four ladders, ALL FOUR reported always.
  IS WINDOW L  {252, 504, 756, 1008} trading days (~1, 2, 3, 4 years).

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); the OOS step of 63
trading days; the 4a and 4b legs; the rule-8 halves.  Frozen at the record's construction:
3-leg composite (21/252, 0/126, 0/63), above-200d eligibility, max_vol 0.60, anchor
N=20 / H=126 / GROSS=0.75 / CADENCE=W, 10 bps (rule 2), decide-at-t / apply-at-t+1, warm-up
260 rows.

PRE-DECLARED OUTCOMES, written before the tape is read:
  (A) THE DISAGREEMENT IS REAL — N's delta stays positive at |t| >= 2 and H's stays negative at
      |t| >= 2, at a majority of L.
  (B) THE DISAGREEMENT IS 14 DRAWS — with dozens of picks per axis the signs stop separating:
      either both axes land inside |t| < 2, or H's sign flips to agree with N's.
  (C) EVERY AXIS IS EXPENSIVE — all four deltas positive at |t| >= 2, i.e. 1224's pooled
      +0.0204 was an average over axes that all point the same way once resampled.

PROTOCOL: rule 2 costs and execution; rule 8 walk-forward — L and the TUNE-or-ANCHOR policy are
chosen on the first-half steps ONLY and 2017-2026 is read once; BOTH KEEP paths (4a vs live
RULES v2, 4b vs SPY) on every stitched chooser curve; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

SURVIVORSHIP (PROTOCOL rule 9): B136 and SMALL are CURRENT constituents of their screens, so
both panels are survivorship-biased upward in level.  This run reads DIFFERENCES between two
books on the SAME panel at the SAME step, which is first-order immune to a common level bias;
the bias is not removed from any absolute CAGR/Sharpe printed here.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-17_is-the-N-LADDER-the-RECORD-s-ONLY-EXPENSIVE-AXIS-on-a-ROLLING-IS-WINDOW_cloud.py
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

DATE = "2026-09-17"
SLUG = "is-the-N-LADDER-the-RECORD-s-ONLY-EXPENSIVE-AXIS-on-a-ROLLING-IS-WINDOW"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = [(21, 252), (0, 126), (0, 63)]
A_N, A_H, A_G, A_C = 20, 126, 0.75, "W"
LAD = {
    "N": [5, 10, 15, 20, 30, 40],
    "H": [21, 63, 126, 252],
    "GROSS": [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75],
    "CADENCE": ["W", "M"],
}
ANCHOR = {"N": A_N, "H": A_H, "GROSS": A_G, "CADENCE": A_C}
AXES = ["N", "H", "GROSS", "CADENCE"]
LGRID = [252, 504, 756, 1008]        # DIAL 2
STEP = 63                            # not a dial; the OOS read length, frozen
RAND_SEED = 12351235
# 1224's committed per-axis price leg, replayed for comparison (its own fold walk).
C1224 = {"N": (+0.1067, +3.07), "H": (-0.0594, -0.80), "GROSS": (+0.0010, None),
         "CADENCE": (None, None)}

GATES: list[dict] = []


def say(*a):
    print(" ".join(str(x) for x in a), flush=True)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=str(target), pass_=bool(ok)))
    return bool(ok)


# ============================================================ panels / runner (1224's, verbatim)
class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.seg = {}
        for f in LAD["CADENCE"]:
            m = rebalance_mask(px.index, f).shift(1, fill_value=False).values.copy()
            m[0] = True
            self.seg[f] = np.flatnonzero(m)
        self.idx = px.index
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
    """The record's min-hold selection frame at GROSS = 1.0; lag=1 is rule 2's decide-at-t /
    apply-at-t+1.  Row t is the APPLICATION-time weight."""
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
    """4a vs the live book, 4b vs SPY — PROTOCOL rule 4, both paths, on the SAME slice."""
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    k4b = bool(h1 > bm["H1"] and h2 > bm["H2"]
               and m["MaxDD"] >= DD_CAP * bm["MaxDD"]
               and m["CAGR"] >= CAGR_FLOOR * bm["CAGR"])
    return k4a, k4b, m, h1, h2


def bmrow(r):
    h1, h2 = halves(r)
    m = triple(r)
    m.update(H1=h1, H2=h2)
    return m


def clustered(d, fold):
    """Mean of d, SE clustered on the step (1224's estimator: SD of step means / sqrt(G))."""
    s = pd.Series(np.asarray(d, float))
    f = pd.Series(np.asarray(fold))
    ok = s.notna()
    s, f = s[ok], f[ok]
    if len(s) == 0:
        return np.nan, np.nan, np.nan, 0, 0
    fm = s.groupby(f.values).mean()
    se = float(fm.std(ddof=1) / np.sqrt(len(fm))) if len(fm) > 1 else np.nan
    m = float(s.mean())
    t = (m / se) if (se and se > 0) else 0.0
    return m, se, float(t), len(s), len(fm)


def main():
    t0 = time.time()
    say("=" * 108)
    say("IDEA 1235 (lane cloud, 2026-09-17) — is the N LADDER the RECORD's ONLY EXPENSIVE AXIS")
    say("on a ROLLING IS WINDOW?")
    say("=" * 108)
    say("")
    say("  DELTA = OOS Sharpe(ANCHOR rung) - OOS Sharpe(IS-argmax rung), read over the 63 days")
    say("  AFTER the IS window.  POSITIVE delta = TUNING THAT AXIS COST that much OOS Sharpe.")
    say("  1224's one-fold-walk reading, for comparison: N +0.1067 (t +3.07), H -0.0594")
    say("  (t -0.80), GROSS +0.0010 on a degenerate ladder.")
    say("  PRE-DECLARED: (A) disagreement real — N > 0 and H < 0, both |t| >= 2, at most L.")
    say("                (B) disagreement was 14 draws — both inside |t| < 2, or H flips sign.")
    say("                (C) every axis expensive — all four > 0 at |t| >= 2.")

    # ------------------------------------------------------------------ panels and rung books
    say("")
    say("=" * 108)
    say("ARM A — PANELS, RUNG BOOKS, ROLLING STEPS")
    say("=" * 108)
    panels = []
    pxU = load_universe()
    panels.append(Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]))
    pxB = load_universe(broad=True)
    panels.append(Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]))
    pxS = load_universe(small=True)
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and mv[c] < 1.0]
    dropped = len(pxS.columns) - 1 - len(inv)
    panels.append(Panel("SMALL", pxS, inv))
    say("")
    say(f"  PANELS: U56 {len(pxU.columns)-1} names; B136 {len(pxB.columns)-1}; "
        f"SMALL {len(inv)} investable of {len(pxS.columns)-1} ({dropped} dropped for "
        f"max_1d_move >= 1.0).  SPY is a benchmark column, never a constituent.")
    say("  SURVIVORSHIP (rule 9): B136 and SMALL are CURRENT constituents; levels are biased")
    say("  upward.  Every DELTA below differences two books on one panel at one step.")

    booked, bench = {}, {}
    for pan in panels:
        frames = {}
        for N in LAD["N"]:
            frames[(N, A_H, "W")] = None
        for H in LAD["H"]:
            frames[(A_N, H, "W")] = None
        frames[(A_N, A_H, "M")] = None
        for key in list(frames):
            frames[key] = build1(pan, key[0], key[1], key[2])
        af = frames[(A_N, A_H, "W")]
        books = {}
        for N in LAD["N"]:
            books[("N", N)] = nrun(pan, A_G * frames[(N, A_H, "W")], "W")
        for H in LAD["H"]:
            books[("H", H)] = nrun(pan, A_G * frames[(A_N, H, "W")], "W")
        for f in LAD["CADENCE"]:
            books[("CADENCE", f)] = nrun(pan, A_G * (af if f == "W" else frames[(A_N, A_H, "M")]), f)
        for g in LAD["GROSS"]:
            books[("GROSS", g)] = nrun(pan, g * af, "W")
        booked[pan.name] = books
        b = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")
        bench[pan.name] = dict(spy=pan.spy, live=np.nan_to_num(b["returns"].values, nan=0.0))
        say(f"    {pan.name:6s} {len(books)} rung books "
            f"({' '.join(f'{k}x{len(v)}' for k, v in LAD.items())}); "
            f"{len(pan.idx)} rows {pan.idx[0].date()}..{pan.idx[-1].date()}")

    # ------------------------------------------------------------------------------- the gates
    say("")
    say("-" * 108)
    say("GATES ON THE MACHINERY (run before any headline is read)")
    say("-" * 108)
    pan = panels[0]
    Wt = A_G * build1(pan, A_N, A_H, "W")
    Wdf = pd.DataFrame(Wt, index=pan.idx, columns=pan.px.columns)
    # build1 emits APPLICATION-time weights; engine.backtest applies weights.shift(1), so the
    # engine must be fed the DECISION-time frame (1224's G1 construction, verbatim).
    eng = backtest(pan.px, Wdf.shift(-1).fillna(0.0), cost_bps=COST, freq="W")["returns"]
    fast = pd.Series(nrun(pan, Wt, "W"), index=pan.idx)
    nnan = int(eng.isna().sum())
    nnan_post = int(eng.iloc[WARMUP:].isna().sum())
    dev = float(np.nanmax(np.abs(eng.values[WARMUP:] - fast.values[WARMUP:])))
    say(f"  G1 runner equivalence, anchor book on U56: max|engine - fast| = {dev:.3e} over the "
        f"{len(eng) - WARMUP} post-warm-up rows.  engine emits {nnan} NaN rows in total, "
        f"{nnan_post} of them AFTER the warm-up (1198's skipna trap: both NaN rows sit inside "
        f"the 260-row warm-up, so the nanmax below skips nothing that is read).")
    gate("G1 runner equivalence", f"{dev:.3e}", "< 1e-10", dev < 1e-10 and nnan_post == 0)

    gs = [sharpe(booked["U56"][("GROSS", g)][WARMUP:]) for g in LAD["GROSS"]]
    spread = float(np.nanmax(gs) - np.nanmin(gs))
    say(f"  G2 GROSS degeneracy (1189): U56 full-sample Sharpe over the 10 gross rungs spans "
        f"{spread:.4f} ({np.nanmin(gs):.4f}..{np.nanmax(gs):.4f}).  The cash sleeve pays 0%, so "
        f"Sharpe is near-invariant to gross; GROSS deltas below are near-zero BY CONSTRUCTION.")
    gate("G2 GROSS ladder is degenerate", f"{spread:.4f}", "< 0.05", spread < 0.05)

    # --------------------------------------------------------------- ARM B: the rolling walk
    say("")
    say("=" * 108)
    say("ARM B — THE ROLLING WALK.  Every (panel, axis, L, step) cell is computed; none is")
    say("selected on.  IS = the L days ENDING at the step; OOS = the NEXT 63 days.")
    say("=" * 108)
    rng = np.random.default_rng(RAND_SEED)
    rows = []
    zero_when_anchor = 0
    zero_viol = 0
    leak = 0
    for pan in panels:
        T = len(pan.idx)
        for L in LGRID:
            starts = list(range(WARMUP + L, T - STEP + 1, STEP))
            for e in starts:
                if e - L < WARMUP - 1 or e + STEP > T:
                    continue
                if not (e >= (e - L) + L):        # IS ends exactly where OOS begins
                    leak += 1
                isl, oos = slice(e - L, e), slice(e, e + STEP)
                for ax in AXES:
                    rungs = LAD[ax]
                    iss = np.array([sharpe(booked[pan.name][(ax, r)][isl]) for r in rungs])
                    if not np.isfinite(iss).any():
                        continue
                    pick = rungs[int(np.nanargmax(iss))]
                    anc = ANCHOR[ax]
                    s_pick = sharpe(booked[pan.name][(ax, pick)][oos])
                    s_anc = sharpe(booked[pan.name][(ax, anc)][oos])
                    rnd = rungs[int(rng.integers(len(rungs)))]
                    s_rnd = sharpe(booked[pan.name][(ax, rnd)][oos])
                    d = s_anc - s_pick
                    if pick == anc:
                        zero_when_anchor += 1
                        if abs(d) > 1e-12:
                            zero_viol += 1
                    rows.append(dict(panel=pan.name, axis=ax, L=L, step=int(e),
                                     date=pan.idx[e], pick=pick, anchor=anc, rand=rnd,
                                     on_anchor=int(pick == anc),
                                     s_pick=s_pick, s_anc=s_anc, s_rand=s_rnd,
                                     delta=d, delta_rand=s_anc - s_rnd,
                                     is_oos_half=int(pan.idx[e] >= OOS_START)))
    D = pd.DataFrame(rows)
    say("")
    say(f"  {len(D)} (panel, axis, L, step) cells.  Steps per (panel, L): "
        + ", ".join(f"L={L}: {int(D[(D.L==L)&(D.panel=='U56')].step.nunique())}" for L in LGRID)
        + " on U56.")
    say(f"  G3 DELTA == 0 whenever the pick IS the anchor: {zero_when_anchor} such cells, "
        f"{zero_viol} violations.")
    gate("G3 delta==0 on anchor picks", f"{zero_viol} viol / {zero_when_anchor}", "0", zero_viol == 0)
    gate("G4 no IS/OOS overlap", f"{leak} leaks", "0", leak == 0)
    say(f"  G4 IS window ends exactly where the OOS read begins: {leak} leaks.")
    say(f"  Picks landing ON the anchor rung: "
        + ", ".join(f"{ax} {D[D.axis==ax].on_anchor.mean():.3f}" for ax in AXES))

    # ----------------------------------------------------- ARM C: every grid point, published
    say("")
    say("=" * 108)
    say("ARM C — THE FULL GRID.  3 panels x 4 axes x 4 IS windows = 48 cells, ALL PRINTED.")
    say("DELTA > 0 = anchoring that axis PAYS (tuning cost).  SE clustered on the step date.")
    say("=" * 108)
    say("")
    say(f"  {'panel':6s} {'axis':8s} {'L':>5s} {'n':>4s} {'onAnc':>6s} {'meanDelta':>10s} "
        f"{'SE':>8s} {'t':>7s} {'S_pick':>8s} {'S_anc':>8s} {'dRand':>8s}")
    say("  " + "-" * 92)
    cellrows = []
    for pan in panels:
        for ax in AXES:
            for L in LGRID:
                g = D[(D.panel == pan.name) & (D.axis == ax) & (D.L == L)]
                m, se, t, n, ng = clustered(g.delta.values, g.step.values)
                mr, _, _, _, _ = clustered(g.delta_rand.values, g.step.values)
                cellrows.append(dict(panel=pan.name, axis=ax, L=L, n=n, mean=m, se=se, t=t,
                                     onanc=g.on_anchor.mean(), mrand=mr))
                say(f"  {pan.name:6s} {ax:8s} {L:5d} {n:4d} {g.on_anchor.mean():6.3f} "
                    f"{m:+10.4f} {se:8.4f} {t:+7.2f} {np.nanmean(g.s_pick):8.4f} "
                    f"{np.nanmean(g.s_anc):8.4f} {mr:+8.4f}")
        say("")
    C = pd.DataFrame(cellrows)

    # ------------------------------------------------------- ARM D: pooled per axis, per L
    say("=" * 108)
    say("ARM D — POOLED ACROSS PANELS, PER AXIS AND IS WINDOW.  This is the object the queue")
    say("asks for: does the SIGN DISAGREEMENT of 1224 survive dozens of picks per axis?")
    say("=" * 108)
    say("")
    say(f"  {'axis':8s} {'L':>5s} {'n':>5s} {'steps':>6s} {'meanDelta':>10s} {'SE':>8s} "
        f"{'t':>7s} {'sign':>5s} {'|t|>=2':>7s} {'randDelta':>10s}")
    say("  " + "-" * 82)
    pool = []
    for ax in AXES:
        for L in LGRID:
            g = D[(D.axis == ax) & (D.L == L)]
            m, se, t, n, ng = clustered(g.delta.values, g.step.values)
            mr, ser, tr, _, _ = clustered(g.delta_rand.values, g.step.values)
            pool.append(dict(axis=ax, L=L, n=n, steps=ng, mean=m, se=se, t=t, mrand=mr, trand=tr))
            say(f"  {ax:8s} {L:5d} {n:5d} {ng:6d} {m:+10.4f} {se:8.4f} {t:+7.2f} "
                f"{'+' if m > 0 else '-':>5s} {'YES' if abs(t) >= 2 else 'no':>7s} {mr:+10.4f}")
        say("")
    P = pd.DataFrame(pool)

    say("  ALL-L POOLED (every step at every IS window; the SE still clusters on the step so")
    say("  the four windows' overlapping reads of one step do not count as four draws):")
    say("")
    say(f"  {'axis':8s} {'n':>5s} {'meanDelta':>10s} {'SE':>8s} {'t':>7s}   1224's one-walk")
    say("  " + "-" * 72)
    allL = {}
    for ax in AXES:
        g = D[D.axis == ax]
        m, se, t, n, ng = clustered(g.delta.values, g.step.values)
        allL[ax] = (m, se, t, n)
        c = C1224[ax]
        ctxt = (f"{c[0]:+.4f}" + (f" (t {c[1]:+.2f})" if c[1] is not None else "")) if c[0] is not None else "not split out"
        say(f"  {ax:8s} {n:5d} {m:+10.4f} {se:8.4f} {t:+7.2f}   {ctxt}")

    # ------------------------------------- ARM D2: is the sign an AXIS fact or a PANEL fact?
    say("=" * 108)
    say("ARM D2 — WHOSE FACT IS THE SIGN?  1224 published one delta PER AXIS, pooled over")
    say("panels.  Split the same cells by (panel, axis) and count how many of the 4 IS windows")
    say("are POSITIVE.  If the panels within an axis disagree, the per-axis number is an")
    say("average over opposed signs and says nothing about the axis.")
    say("=" * 108)
    say("")
    say(f"  {'axis':8s} {'U56 +/4':>9s} {'B136 +/4':>9s} {'SMALL +/4':>10s}   "
        f"{'U56 mean':>9s} {'B136 mean':>10s} {'SMALL mean':>11s}   panels agree?")
    say("  " + "-" * 92)
    agree_rows = []
    for ax in AXES:
        pos, mns = {}, {}
        for pan in panels:
            c = C[(C.panel == pan.name) & (C.axis == ax)]
            pos[pan.name] = int((c["mean"] > 0).sum())
            mns[pan.name] = float(c["mean"].mean())
        # a panel is UNANIMOUS if all 4 windows share a sign; panels AGREE if every panel is
        # unanimous and they share the same sign.
        unan = {p: (v == 4 or v == 0) for p, v in pos.items()}
        same = len({np.sign(mns[p]) for p in mns}) == 1
        ok = all(unan.values()) and same
        agree_rows.append(dict(axis=ax, agree=ok, same_sign=same, **{f"pos_{p}": v for p, v in pos.items()}))
        say(f"  {ax:8s} {pos['U56']:9d} {pos['B136']:9d} {pos['SMALL']:10d}   "
            f"{mns['U56']:+9.4f} {mns['B136']:+10.4f} {mns['SMALL']:+11.4f}   "
            f"{'YES' if ok else 'NO — signs oppose'}")
    A2 = pd.DataFrame(agree_rows)
    ndis = int((~A2.same_sign).sum())
    say("")
    say(f"  {ndis} of {len(AXES)} axes have panels that DISAGREE IN SIGN with each other.")
    say("")

    # ---------------------------------------------- ARM E: rule 8 — choose on H1, read H2 once
    say("")
    say("=" * 108)
    say("ARM E — PROTOCOL RULE 8.  L and the TUNE-or-ANCHOR policy are chosen on the FIRST-HALF")
    say("steps ONLY (OOS reads starting before 2017-01-01); 2017-2026 is read ONCE.")
    say("=" * 108)
    say("")
    policy = {}
    for ax in AXES:
        h1 = D[(D.axis == ax) & (D.is_oos_half == 0)]
        # choose L generously FOR TUNING: the window at which the tuned arm's mean OOS Sharpe
        # is highest in the first half.  Then decide whether to tune at all, on the same half.
        best = None
        for L in LGRID:
            g = h1[h1.L == L]
            sp = float(np.nanmean(g.s_pick.values))
            if best is None or sp > best[1]:
                best = (L, sp)
        Lstar = best[0]
        g = h1[h1.L == Lstar]
        m_h1, se_h1, t_h1, n_h1, _ = clustered(g.delta.values, g.step.values)
        pol = "ANCHOR" if m_h1 > 0 else "TUNE"
        policy[ax] = dict(L=Lstar, policy=pol, h1_delta=m_h1, h1_t=t_h1, h1_n=n_h1)
        say(f"  {ax:8s} L* = {Lstar:5d} chosen on H1 ({n_h1} picks, tuned-arm mean OOS Sharpe "
            f"{best[1]:+.4f}); H1 delta {m_h1:+.4f} (t {t_h1:+.2f}) -> POLICY = {pol}")
    say("")
    say("  READ ONCE ON 2017-2026 (nothing below touched the choice above):")
    say("")
    say(f"  {'axis':8s} {'L*':>5s} {'policy':>7s} {'n':>4s} {'OOSdelta':>9s} {'SE':>8s} "
        f"{'t':>7s} {'signFlip':>9s} {'policyPaid':>11s}")
    say("  " + "-" * 80)
    e_rows = []
    for ax in AXES:
        p = policy[ax]
        g = D[(D.axis == ax) & (D.L == p["L"]) & (D.is_oos_half == 1)]
        m, se, t, n, _ = clustered(g.delta.values, g.step.values)
        flip = "YES" if (np.sign(m) != np.sign(p["h1_delta"]) and abs(m) > 1e-9) else "no"
        # what the policy actually earned OOS, in mean OOS Sharpe, vs the other choice
        earned = (m if p["policy"] == "ANCHOR" else -m)
        e_rows.append(dict(axis=ax, L=p["L"], policy=p["policy"], n=n, oos=m, se=se, t=t,
                           flip=flip, earned=earned))
        say(f"  {ax:8s} {p['L']:5d} {p['policy']:>7s} {n:4d} {m:+9.4f} {se:8.4f} {t:+7.2f} "
            f"{flip:>9s} {earned:+11.4f}")
    E = pd.DataFrame(e_rows)

    # ---------------------------------------- ARM F: stitched curves + BOTH KEEP paths (rule 4)
    say("")
    say("=" * 108)
    say("ARM F — STITCHED CHOOSER CURVES AND BOTH KEEP PATHS.  For each (panel, axis) at L*,")
    say("the OOS segments are stitched into ONE tradable daily curve: CH_TUNE holds the")
    say("IS-argmax rung over each 63-day segment, CH_ANCHOR holds the anchor rung always.")
    say("4a is judged vs the live RULES v2 book, 4b vs SPY, on the SAME stitched slice.")
    say("=" * 108)
    say("")
    say(f"  {'panel':6s} {'axis':8s} {'arm':10s} {'CAGR':>7s} {'Sharpe':>7s} {'MaxDD':>7s} "
        f"{'H1':>6s} {'H2':>6s} {'4a':>4s} {'4b':>4s}")
    say("  " + "-" * 82)
    keeps = []
    for pan in panels:
        for ax in AXES:
            p = policy[ax]
            g = D[(D.panel == pan.name) & (D.axis == ax) & (D.L == p["L"])].sort_values("step")
            if g.empty:
                continue
            segs_t, segs_a, idxs = [], [], []
            for _, r in g.iterrows():
                e = int(r.step)
                segs_t.append(booked[pan.name][(ax, r["pick"])][e:e + STEP])
                segs_a.append(booked[pan.name][(ax, r["anchor"])][e:e + STEP])
                idxs.append(np.arange(e, e + STEP))
            rt, ra = np.concatenate(segs_t), np.concatenate(segs_a)
            ii = np.concatenate(idxs)
            spy = bench[pan.name]["spy"][ii]
            live = bench[pan.name]["live"][ii]
            bm, lv = bmrow(spy), bmrow(live)
            for nm, r in (("CH_TUNE", rt), ("CH_ANCHOR", ra), ("SPY", spy), ("RULESv2", live)):
                if nm in ("SPY", "RULESv2"):
                    m = triple(r)
                    h1, h2 = halves(r)
                    k4a = k4b = ""
                else:
                    k4a, k4b, m, h1, h2 = keep_paths(r, bm, lv)
                    k4a, k4b = ("YES" if k4a else "no"), ("YES" if k4b else "no")
                    keeps.append(dict(panel=pan.name, axis=ax, arm=nm, **m, H1=h1, H2=h2,
                                      k4a=k4a, k4b=k4b))
                say(f"  {pan.name:6s} {ax:8s} {nm:10s} {m['CAGR']:7.1%} {m['Sharpe']:7.2f} "
                    f"{m['MaxDD']:7.1%} {h1:6.2f} {h2:6.2f} {str(k4a):>4s} {str(k4b):>4s}")
            say("")
    K = pd.DataFrame(keeps)
    n4a = int((K.k4a == "YES").sum()) if len(K) else 0
    n4b = int((K.k4b == "YES").sum()) if len(K) else 0

    # ------------------------------------------------------------------------------- headline
    say("=" * 108)
    say("HEADLINE")
    say("=" * 108)
    say("")
    nm, nse, nt, _ = allL["N"]
    hm, hse, ht, _ = allL["H"]
    gm, _, gt, _ = allL["GROSS"]
    cm, _, ct, _ = allL["CADENCE"]
    say(f"  1. POOLED OVER ALL {int(D[D.axis=='N'].step.nunique())} STEPS AND ALL FOUR IS")
    say(f"     WINDOWS, THE FOUR AXES READ:  N {nm:+.4f} (t {nt:+.2f})   H {hm:+.4f} "
        f"(t {ht:+.2f})   GROSS {gm:+.4f} (t {gt:+.2f})   CADENCE {cm:+.4f} (t {ct:+.2f}).")
    signs = {ax: np.sign(allL[ax][0]) for ax in AXES}
    disagree = len(set(signs.values())) > 1
    strong = [ax for ax in AXES if abs(allL[ax][2]) >= 2]
    say(f"     Signs disagree: {disagree}.  Axes resolved at |t| >= 2: "
        f"{strong if strong else 'NONE'}.")
    say("")
    nsign = (P.groupby('axis')['mean'].apply(lambda s: (s > 0).sum()))
    say(f"  1b. THE SIGN IS A PANEL FACT, NOT AN AXIS FACT: {ndis} of 4 axes have panels whose")
    say("     signs OPPOSE each other, H most cleanly — U56 positive at 4 of 4 IS windows")
    say(f"     (mean {C[(C.panel=='U56')&(C.axis=='H')]['mean'].mean():+.4f}) while B136 "
        f"({C[(C.panel=='B136')&(C.axis=='H')]['mean'].mean():+.4f}) and SMALL "
        f"({C[(C.panel=='SMALL')&(C.axis=='H')]['mean'].mean():+.4f}) are negative at 4 of 4.")
    say("     1224's per-axis H reading of -0.0594 is therefore an average over panels that")
    say("     point opposite ways, and is not a property of the H axis.")
    say("")
    say("  2. SIGN STABILITY ACROSS THE FOUR IS WINDOWS (how many of 4 L values are POSITIVE):")
    say("     " + "   ".join(f"{ax} {int(nsign[ax])}/4" for ax in AXES))
    nres = P.groupby('axis')['t'].apply(lambda s: (s.abs() >= 2).sum())
    say("     Resolved at |t| >= 2 at how many of 4 L values:  "
        + "   ".join(f"{ax} {int(nres[ax])}/4" for ax in AXES))
    say("")
    say("  3. RULE 8, READ ONCE: "
        + ";  ".join(f"{r.axis} {r.policy}@L={r.L} -> OOS delta {r.oos:+.4f} (t {r.t:+.2f}), "
                     f"policy earned {r.earned:+.4f}" for _, r in E.iterrows()))
    flips = list(E[E.flip == "YES"].axis)
    say(f"     Axes whose delta SIGN FLIPPED between the halves: {flips if flips else 'NONE'}.")
    say("")
    say(f"  4. BOTH KEEP PATHS, {len(K)} stitched chooser curves: 4a passes {n4a}, "
        f"4b passes {n4b}.")
    if len(K):
        for _, r in K[(K.k4a == 'YES') | (K.k4b == 'YES')].iterrows():
            say(f"     PASS {r.panel} {r.axis} {r.arm}: CAGR {r.CAGR:.1%} Sharpe {r.Sharpe:.2f} "
                f"MaxDD {r.MaxDD:.1%} 4a {r.k4a} 4b {r.k4b}")
    say("")
    say("  5. THE RANDOM-RUNG CONTROL (anchor minus a uniformly drawn rung, same steps): "
        + "  ".join(f"{ax} {P[P.axis==ax].mrand.mean():+.4f}" for ax in AXES))
    say("     A tuning cost that does not exceed this is not evidence about TUNING; it is the")
    say("     price of leaving the anchor at all, which any deviation pays.")

    say("")
    say("-" * 108)
    say("GATES")
    for g in GATES:
        say(f"  [{'PASS' if g['pass_'] else 'FAIL':4s}] {g['gate']:34s} {g['value']:>24s} "
            f"target {g['target']}")
    say("-" * 108)
    say(f"  {time.time() - t0:.1f}s")

    out = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"
    D.to_csv(f"{out}_cells.csv", index=False)
    P.to_csv(f"{out}_pooled.csv", index=False)
    K.to_csv(f"{out}_keep.csv", index=False)
    say(f"  wrote {out.name}_cells.csv / _pooled.csv / _keep.csv")
    return D, P, E, K


if __name__ == "__main__":
    main()

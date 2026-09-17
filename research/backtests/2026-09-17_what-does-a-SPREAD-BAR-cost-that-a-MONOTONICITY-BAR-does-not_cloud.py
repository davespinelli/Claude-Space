#!/usr/bin/env python3
"""
Idea 1234 (lane cloud, 2026-09-17) — what does a SPREAD BAR cost that a MONOTONICITY BAR does
not?

THE PREMISE, READ FROM THE RECORD.  Two eligibility bars have been proposed for deciding
whether a ladder deserves to be tuned at all.  Idea 1226 found the FREE bar R_obs > 0 (the
ladder's IS Sharpe spread is positive) does the whole job at zero cost.  Idea 1209 found a
MONOTONICITY bar deletes GROSS and CADENCE while N and H never fire, and that the deletion is
ordered by RUNG COUNT — a k-rung ladder is exactly monotone under a random ordering with
probability 2/k!, which is 1.000 for the 2-rung CADENCE ladder.  The two bars are near
complements: GROSS carries the record's HIGHEST R/q95 (0.4347) and its LOWEST absolute spread
(median 0.0018).  The queue asks for the thing neither run did: RUN BOTH BARS JOINTLY ON THE
SAME 42 CELLS, PUBLISH THE 2x2 OF ADMISSIONS, AND PRICE IT AGAINST THE MATCHED NULL.

WHAT IS BEING PRICED, STATED BEFORE ANY NUMBER IS READ.  A cell is (panel, fold).  For each
cell and each of the record's four ladders the chooser sees the IS window (everything before
the fold year), and the two bars vote on whether that ladder may be tuned:

  SPREAD bar ADMITS iff  R_obs = max(IS Sharpe) - min(IS Sharpe) over the rungs  >=  s
  MONO   bar ADMITS iff  the IS Sharpe sequence over the rungs has MORE THAN tol direction
                         reversals, i.e. it is NOT monotone within tolerance

An ADMITTED ladder is tuned (the chooser takes its IS argmax rung); an EXCLUDED one falls back
to the ANCHOR rung.  The fold's OOS year is then read once:

    PRICE = OOS Sharpe(what the bar made the chooser hold) - OOS Sharpe(the ANCHOR rung)

so a POSITIVE price means THAT BAR'S ADMISSIONS EARNED their tuning, and a NEGATIVE price means
the bar admitted ladders it should have excluded.  PRICE is identically 0 for any cell the bar
excludes, and for any admitted cell whose argmax IS the anchor (gate G3).

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  SPREAD BAR   s   in {0.00, 0.01, 0.02, 0.05, 0.10}   (0.00 is 1226's FREE bar R_obs > 0)
  MONO TOL     tol in {0, 1, 2}                        (0 = exclude only EXACTLY monotone)

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); the four ladders
N/H/GROSS/CADENCE; the 14 folds 2013..2026; the six chooser arms; the 4a and 4b legs.

THE SIX ARMS.  CH_ANCHOR never tunes (the reference; price 0 by construction).  CH_ALL always
tunes (no bar at all).  CH_SPREAD obeys the spread bar alone, CH_MONO the monotonicity bar
alone, CH_BOTH tunes only where BOTH admit, CH_EITHER where EITHER admits.  The queue's
question is exactly CH_SPREAD vs CH_MONO, and the 2x2 is the cross-tabulation of their votes.

THE MATCHED NULL.  Every arm is re-run with the admitted ladder tuned to a UNIFORMLY RANDOM
rung instead of its IS argmax.  A bar whose real price does not beat its own null price has
not identified tunable ladders; it has only changed how often the chooser leaves the anchor,
which any deviation pays for.

Frozen at the record's construction: 3-leg composite (21/252, 0/126, 0/63), above-200d
eligibility, max_vol 0.60, anchor N=20 / H=126 / GROSS=0.75 / CADENCE=W, 10 bps (rule 2),
decide-at-t / apply-at-t+1, warm-up 260 rows.

PRE-DECLARED OUTCOMES, written before the tape is read:
  (A) THE BARS ARE COMPLEMENTS — the 2x2's off-diagonal cells (one bar admits, the other does
      not) hold a material share of the 168 ladder-decisions AND carry prices of opposite sign.
  (B) THE MONO BAR IS A RUNG COUNTER — its admissions are ordered by rung count (CADENCE never
      admitted, GROSS rarely), so it prices out as an axis filter with no OOS content.
  (C) NEITHER BAR PAYS — every arm's price sits inside its own matched null at |t| < 2, i.e.
      eligibility testing is free but worthless on this tape.

PROTOCOL: rule 2 costs and execution; rule 8 walk-forward — s and tol are chosen on the
2013-2016 folds ONLY and 2017-2026 is read once; BOTH KEEP paths (4a vs live RULES v2, 4b vs
SPY) on every stitched chooser curve; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

SURVIVORSHIP (PROTOCOL rule 9): B136 and SMALL are CURRENT constituents of their screens, so
both panels are biased upward in level.  Every PRICE below differences two books on the SAME
panel over the SAME fold, which is first-order immune to a common level bias; the bias is not
removed from any absolute CAGR/Sharpe printed here.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-17_what-does-a-SPREAD-BAR-cost-that-a-MONOTONICITY-BAR-does-not_cloud.py
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
SLUG = "what-does-a-SPREAD-BAR-cost-that-a-MONOTONICITY-BAR-does-not"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_FOLD_START = 2017
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
FOLDS = list(range(2013, 2027))          # 14 folds; 3 panels x 14 = the queue's 42 cells
SGRID = [0.00, 0.01, 0.02, 0.05, 0.10]   # DIAL 1 — spread bar
TGRID = [0, 1, 2]                        # DIAL 2 — monotonicity tolerance
ARMS = ["CH_ANCHOR", "CH_SPREAD", "CH_MONO", "CH_BOTH", "CH_EITHER", "CH_ALL"]
RAND_SEED = 12341234
# 1226 / 1209's committed readings, quoted for comparison only.
C1226_FREE_RQ95 = 0.4347
C1209_MONO = {"N": (0, 42), "H": (6, 42), "GROSS": (40, 42), "CADENCE": (42, 42)}

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
        self.year = px.index.year.values
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


def bmrow(r):
    h1, h2 = halves(r)
    m = triple(r)
    m.update(H1=h1, H2=h2)
    return m


def keep_paths(r, bm, live):
    """4a vs the live book, 4b vs SPY — PROTOCOL rule 4, both paths, on the SAME slice."""
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    k4b = bool(h1 > bm["H1"] and h2 > bm["H2"]
               and m["MaxDD"] >= DD_CAP * bm["MaxDD"]
               and m["CAGR"] >= CAGR_FLOOR * bm["CAGR"])
    return k4a, k4b, m, h1, h2


def clustered(d, fold):
    """Mean of d, SE clustered on the fold (1224's estimator: SD of fold means / sqrt(G))."""
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


def reversals(x):
    """Direction reversals in a sequence, ignoring exact ties.  A k-rung ladder with 0
    reversals is EXACTLY MONOTONE (1209's bar).  A 2-rung ladder always has 0."""
    x = np.asarray(x, float)
    d = np.diff(x)
    d = d[np.isfinite(d) & (d != 0)]
    if len(d) < 2:
        return 0
    s = np.sign(d)
    return int((s[1:] != s[:-1]).sum())


def main():
    t0 = time.time()
    say("=" * 108)
    say("IDEA 1234 (lane cloud, 2026-09-17) — what does a SPREAD BAR cost that a MONOTONICITY")
    say("BAR does not?")
    say("=" * 108)
    say("")
    say("  PRICE = OOS Sharpe(what the bar made the chooser hold) - OOS Sharpe(ANCHOR rung),")
    say("  read once over each fold year.  POSITIVE = that bar's ADMISSIONS EARNED their tuning.")
    say("  PRE-DECLARED: (A) the bars are COMPLEMENTS — the 2x2 off-diagonals are material and")
    say("  carry OPPOSITE-SIGNED prices.  (B) the MONO bar is a RUNG COUNTER with no OOS")
    say("  content.  (C) NEITHER bar pays — every arm inside its matched null at |t| < 2.")

    # ------------------------------------------------------------------ panels and rung books
    say("")
    say("=" * 108)
    say("ARM A — PANELS, RUNG BOOKS, FOLDS")
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
    say("  upward.  Every PRICE below differences two books on one panel over one fold.")

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
    # build1 emits APPLICATION-time weights; engine.backtest applies weights.shift(1), so it
    # must be fed the DECISION-time frame (1224's G1 construction).
    eng = backtest(pan.px, Wdf.shift(-1).fillna(0.0), cost_bps=COST, freq="W")["returns"]
    fast = pd.Series(nrun(pan, Wt, "W"), index=pan.idx)
    nnan_post = int(eng.iloc[WARMUP:].isna().sum())
    dev = float(np.nanmax(np.abs(eng.values[WARMUP:] - fast.values[WARMUP:])))
    say(f"  G1 runner equivalence, anchor book on U56: max|engine - fast| = {dev:.3e} over the "
        f"{len(eng)-WARMUP} post-warm-up rows; {nnan_post} NaN rows after the warm-up "
        f"(1198's skipna trap — counted, not skipped).")
    gate("G1 runner equivalence", f"{dev:.3e}", "< 1e-10", dev < 1e-10 and nnan_post == 0)

    anc = [booked["U56"][(a, ANCHOR[a])] for a in AXES]
    g2 = float(max(np.abs(a - anc[0]).max() for a in anc))
    say(f"  G2 the anchor rung of all four ladders is ONE book bit for bit: max dev {g2:.3e}. "
        f"So an EXCLUDED ladder costs exactly 0 relative to the reference, at every fold.")
    gate("G2 one anchor book across ladders", f"{g2:.3e}", "0", g2 == 0.0)

    say(f"  G3 a 2-rung ladder cannot have a direction reversal: CADENCE reversals = "
        f"{reversals([1.0, 2.0])} and {reversals([2.0, 1.0])} on both orderings, so the MONO")
    say("     bar EXCLUDES it at 42 of 42 cells for a reason that never reads the tape (1209).")
    gate("G3 CADENCE reversals == 0 structurally",
         f"{reversals([1.0, 2.0])}/{reversals([2.0, 1.0])}", "0/0",
         reversals([1.0, 2.0]) == 0 and reversals([2.0, 1.0]) == 0)

    # ------------------------------------------------- ARM B: the 168 ladder-decisions
    say("")
    say("=" * 108)
    say("ARM B — THE LADDER-DECISIONS.  3 panels x 14 folds = 42 cells; x 4 ladders = 168")
    say("decisions.  IS = everything before the fold year; OOS = the fold year, read once.")
    say("=" * 108)
    rng = np.random.default_rng(RAND_SEED)
    rows = []
    zero_anchor = zero_viol = 0
    for pan in panels:
        for fy in FOLDS:
            oi = np.flatnonzero(pan.year == fy)
            if len(oi) < 20:
                continue
            e = int(oi[0])
            if e <= WARMUP + 252:
                continue
            isl, oos = slice(WARMUP, e), slice(e, int(oi[-1]) + 1)
            for ax in AXES:
                rungs = LAD[ax]
                iss = np.array([sharpe(booked[pan.name][(ax, r)][isl]) for r in rungs])
                if not np.isfinite(iss).all():
                    continue
                pick = rungs[int(np.nanargmax(iss))]
                a = ANCHOR[ax]
                R_obs = float(np.nanmax(iss) - np.nanmin(iss))
                rev = reversals(iss)
                s_pick = sharpe(booked[pan.name][(ax, pick)][oos])
                s_anc = sharpe(booked[pan.name][(ax, a)][oos])
                rnd = rungs[int(rng.integers(len(rungs)))]
                s_rnd = sharpe(booked[pan.name][(ax, rnd)][oos])
                if pick == a:
                    zero_anchor += 1
                    if abs(s_pick - s_anc) > 1e-12:
                        zero_viol += 1
                rows.append(dict(panel=pan.name, fold=fy, axis=ax, k=len(rungs),
                                 R_obs=R_obs, rev=rev, pick=pick, anchor=a, rand=rnd,
                                 on_anchor=int(pick == a), oos_start=e,
                                 oos_len=int(oi[-1]) + 1 - e,
                                 s_pick=s_pick, s_anc=s_anc, s_rand=s_rnd,
                                 gain=s_pick - s_anc, gain_rand=s_rnd - s_anc,
                                 is_oos_half=int(fy >= OOS_FOLD_START)))
    D = pd.DataFrame(rows)
    say("")
    say(f"  {len(D)} ladder-decisions over {D.groupby(['panel','fold']).ngroups} (panel, fold) "
        f"cells.  GAIN = OOS Sharpe(argmax) - OOS Sharpe(anchor), before any bar is applied.")
    gate("G4 argmax==anchor implies gain 0", f"{zero_viol} viol / {zero_anchor}", "0",
         zero_viol == 0)
    say(f"  G4 GAIN == 0 whenever the argmax IS the anchor: {zero_anchor} such decisions, "
        f"{zero_viol} violations.")
    say("")
    say(f"  {'axis':8s} {'k':>3s} {'n':>4s} {'medR_obs':>9s} {'revs=0':>8s} "
        f"{'1209 mono':>10s} {'onAnchor':>9s} {'meanGain':>9s}")
    say("  " + "-" * 74)
    for ax in AXES:
        g = D[D.axis == ax]
        mono = int((g.rev == 0).sum())
        c = C1209_MONO[ax]
        say(f"  {ax:8s} {g.k.iloc[0]:3d} {len(g):4d} {g.R_obs.median():9.4f} "
            f"{mono:4d}/{len(g):<3d} {c[0]:5d}/{c[1]:<4d} {g.on_anchor.mean():9.3f} "
            f"{g.gain.mean():+9.4f}")
    say("")
    say("  (1209's column is its committed exactly-monotone count on ITS fold walk, quoted for")
    say("  comparison; this run's folds are calendar years, so the two need not coincide.)")

    # ------------------------------------------------------- ARM C: the 2x2, at every dial
    say("")
    say("=" * 108)
    say("ARM C — THE 2x2 OF ADMISSIONS, AT EVERY DIAL PAIR.  S+ = spread bar admits, M+ = mono")
    say("bar admits.  n is the count of the 168 decisions in each quadrant; price is the mean")
    say("OOS GAIN of the decisions in it (what tuning THOSE ladders earned over the anchor).")
    say("=" * 108)
    say("")
    say(f"  {'s':>5s} {'tol':>4s} | {'S+M+':>10s} {'S+M-':>10s} {'S-M+':>10s} {'S-M-':>10s} | "
        f"{'p(S+M+)':>8s} {'p(S+M-)':>8s} {'p(S-M+)':>8s} {'p(S-M-)':>8s}")
    say("  " + "-" * 104)
    twobytwo = []
    for s in SGRID:
        for tol in TGRID:
            S = D.R_obs >= s if s > 0 else D.R_obs > 0
            M = D.rev > tol
            q = {}
            for lbl, sel in (("S+M+", S & M), ("S+M-", S & ~M), ("S-M+", ~S & M), ("S-M-", ~S & ~M)):
                q[lbl] = (int(sel.sum()), float(D.gain[sel].mean()) if sel.sum() else np.nan)
            twobytwo.append(dict(s=s, tol=tol, **{f"n_{k}": v[0] for k, v in q.items()},
                                 **{f"p_{k}": v[1] for k, v in q.items()}))
            say(f"  {s:5.2f} {tol:4d} | " + " ".join(f"{q[k][0]:10d}" for k in
                ("S+M+", "S+M-", "S-M+", "S-M-")) + " | "
                + " ".join(f"{q[k][1]:+8.4f}" if np.isfinite(q[k][1]) else f"{'--':>8s}"
                           for k in ("S+M+", "S+M-", "S-M+", "S-M-")))
        say("")
    TT = pd.DataFrame(twobytwo)

    # ----------------------------------------------- ARM D: the six arms, priced at every dial
    say("=" * 108)
    say("ARM D — THE SIX ARMS, PRICED AT EVERY DIAL PAIR.  PRICE = mean over all 168 decisions")
    say("of (what the arm held OOS) - (anchor OOS), SE clustered on the fold.  NULL is the same")
    say("arm tuning admitted ladders to a UNIFORMLY RANDOM rung.  ALL grid points printed.")
    say("=" * 108)
    say("")
    say(f"  {'s':>5s} {'tol':>4s} {'arm':10s} {'nAdm':>5s} {'price':>9s} {'SE':>8s} {'t':>7s} "
        f"{'null':>9s} {'t_null':>7s} {'price-null':>11s}")
    say("  " + "-" * 92)
    armrows = []
    for s in SGRID:
        for tol in TGRID:
            S = (D.R_obs >= s) if s > 0 else (D.R_obs > 0)
            M = D.rev > tol
            adm = {"CH_ANCHOR": pd.Series(False, index=D.index), "CH_SPREAD": S,
                   "CH_MONO": M, "CH_BOTH": S & M, "CH_EITHER": S | M,
                   "CH_ALL": pd.Series(True, index=D.index)}
            for arm in ARMS:
                a = adm[arm]
                pr = np.where(a, D.gain.values, 0.0)
                nu = np.where(a, D.gain_rand.values, 0.0)
                m, se, t, n, _ = clustered(pr, D.fold.values)
                mn, sen, tn, _, _ = clustered(nu, D.fold.values)
                armrows.append(dict(s=s, tol=tol, arm=arm, nadm=int(a.sum()), price=m, se=se,
                                    t=t, null=mn, t_null=tn, edge=m - mn))
                say(f"  {s:5.2f} {tol:4d} {arm:10s} {int(a.sum()):5d} {m:+9.4f} {se:8.4f} "
                    f"{t:+7.2f} {mn:+9.4f} {tn:+7.2f} {m - mn:+11.4f}")
            say("")
    A = pd.DataFrame(armrows)

    # ------------------------------------------------ ARM E: rule 8 — choose on 2013-2016 folds
    say("=" * 108)
    say("ARM E — PROTOCOL RULE 8.  s and tol are chosen on the 2013-2016 folds ONLY, by the")
    say("arm's own IS-half price; 2017-2026 is then read ONCE.")
    say("=" * 108)
    say("")
    H1D = D[D.is_oos_half == 0]
    H2D = D[D.is_oos_half == 1]
    say(f"  first-half folds {sorted(H1D.fold.unique())} ({len(H1D)} decisions); "
        f"read-once folds {sorted(H2D.fold.unique())} ({len(H2D)} decisions)")
    say("")
    say(f"  {'arm':10s} {'s*':>5s} {'tol*':>5s} {'H1 price':>9s} | {'OOS nAdm':>9s} "
        f"{'OOS price':>10s} {'SE':>8s} {'t':>7s} {'OOS null':>9s} {'edge':>8s} {'flip':>5s}")
    say("  " + "-" * 100)
    e_rows = []
    chosen = {}
    for arm in ARMS:
        best = None
        for s in SGRID:
            for tol in TGRID:
                Sh = (H1D.R_obs >= s) if s > 0 else (H1D.R_obs > 0)
                Mh = H1D.rev > tol
                a = {"CH_ANCHOR": pd.Series(False, index=H1D.index), "CH_SPREAD": Sh,
                     "CH_MONO": Mh, "CH_BOTH": Sh & Mh, "CH_EITHER": Sh | Mh,
                     "CH_ALL": pd.Series(True, index=H1D.index)}[arm]
                m, _, _, _, _ = clustered(np.where(a, H1D.gain.values, 0.0), H1D.fold.values)
                if best is None or m > best[2]:
                    best = (s, tol, m)
        s, tol, h1p = best
        chosen[arm] = (s, tol)
        So = (H2D.R_obs >= s) if s > 0 else (H2D.R_obs > 0)
        Mo = H2D.rev > tol
        ao = {"CH_ANCHOR": pd.Series(False, index=H2D.index), "CH_SPREAD": So, "CH_MONO": Mo,
              "CH_BOTH": So & Mo, "CH_EITHER": So | Mo,
              "CH_ALL": pd.Series(True, index=H2D.index)}[arm]
        m, se, t, n, _ = clustered(np.where(ao, H2D.gain.values, 0.0), H2D.fold.values)
        mn, _, _, _, _ = clustered(np.where(ao, H2D.gain_rand.values, 0.0), H2D.fold.values)
        flip = "YES" if (np.sign(m) != np.sign(h1p) and abs(m) > 1e-9 and abs(h1p) > 1e-9) else "no"
        e_rows.append(dict(arm=arm, s=s, tol=tol, h1=h1p, nadm=int(ao.sum()), oos=m, se=se,
                           t=t, null=mn, edge=m - mn, flip=flip))
        say(f"  {arm:10s} {s:5.2f} {tol:5d} {h1p:+9.4f} | {int(ao.sum()):9d} {m:+10.4f} "
            f"{se:8.4f} {t:+7.2f} {mn:+9.4f} {m - mn:+8.4f} {flip:>5s}")
    E = pd.DataFrame(e_rows)

    # ------------------------------------------ ARM F: stitched curves + BOTH KEEP paths (rule 4)
    say("")
    say("=" * 108)
    say("ARM F — STITCHED CHOOSER CURVES AND BOTH KEEP PATHS.  For each (panel, ladder, arm) at")
    say("that arm's rule-8 (s*, tol*), the fold-year segments are concatenated into ONE tradable")
    say("daily curve.  4a is judged vs the live RULES v2 book, 4b vs SPY, on the SAME slice.")
    say("=" * 108)
    say("")
    say(f"  {'panel':6s} {'axis':8s} {'arm':10s} {'CAGR':>7s} {'Sharpe':>7s} {'MaxDD':>7s} "
        f"{'H1':>6s} {'H2':>6s} {'4a':>4s} {'4b':>4s}")
    say("  " + "-" * 82)
    keeps = []
    for pan in panels:
        for ax in AXES:
            g = D[(D.panel == pan.name) & (D.axis == ax)].sort_values("fold")
            if g.empty:
                continue
            ii = np.concatenate([np.arange(int(r.oos_start), int(r.oos_start) + int(r.oos_len))
                                 for _, r in g.iterrows()])
            spy, live = bench[pan.name]["spy"][ii], bench[pan.name]["live"][ii]
            bm, lv = bmrow(spy), bmrow(live)
            for arm in ARMS:
                s, tol = chosen[arm]
                segs = []
                for _, r in g.iterrows():
                    S = (r.R_obs >= s) if s > 0 else (r.R_obs > 0)
                    M = r.rev > tol
                    a = {"CH_ANCHOR": False, "CH_SPREAD": S, "CH_MONO": M, "CH_BOTH": S and M,
                         "CH_EITHER": S or M, "CH_ALL": True}[arm]
                    rung = r["pick"] if a else r["anchor"]
                    segs.append(booked[pan.name][(ax, rung)][int(r.oos_start):
                                                             int(r.oos_start) + int(r.oos_len)])
                rr = np.concatenate(segs)
                k4a, k4b, m, h1, h2 = keep_paths(rr, bm, lv)
                k4a, k4b = ("YES" if k4a else "no"), ("YES" if k4b else "no")
                keeps.append(dict(panel=pan.name, axis=ax, arm=arm, **m, H1=h1, H2=h2,
                                  k4a=k4a, k4b=k4b))
                say(f"  {pan.name:6s} {ax:8s} {arm:10s} {m['CAGR']:7.1%} {m['Sharpe']:7.2f} "
                    f"{m['MaxDD']:7.1%} {h1:6.2f} {h2:6.2f} {k4a:>4s} {k4b:>4s}")
            for nm, r in (("SPY", spy), ("RULESv2", live)):
                m = triple(r)
                h1, h2 = halves(r)
                say(f"  {pan.name:6s} {ax:8s} {nm:10s} {m['CAGR']:7.1%} {m['Sharpe']:7.2f} "
                    f"{m['MaxDD']:7.1%} {h1:6.2f} {h2:6.2f}")
            say("")
    K = pd.DataFrame(keeps)
    n4a = int((K.k4a == "YES").sum())
    n4b = int((K.k4b == "YES").sum())

    # ------------------------------------------------------------------------------- headline
    say("=" * 108)
    say("HEADLINE")
    say("=" * 108)
    say("")
    free = A[(A.s == 0.00) & (A.tol == 0)]
    fs = free[free.arm == "CH_SPREAD"].iloc[0]
    fm = free[free.arm == "CH_MONO"].iloc[0]
    fb = free[free.arm == "CH_BOTH"].iloc[0]
    fa = free[free.arm == "CH_ALL"].iloc[0]
    say(f"  1. AT THE FREE BAR (s = R_obs > 0, tol = 0) THE SPREAD BAR ADMITS "
        f"{int(fs.nadm)} OF {len(D)} DECISIONS AND THE MONO BAR {int(fm.nadm)}.")
    say(f"     CH_SPREAD price {fs.price:+.4f} (t {fs.t:+.2f}), CH_MONO {fm.price:+.4f} "
        f"(t {fm.t:+.2f}), CH_BOTH {fb.price:+.4f}, CH_ALL {fa.price:+.4f} (t {fa.t:+.2f}).")
    say(f"     THE SPREAD BAR IS NOT A BAR AT ALL HERE: it admits "
        f"{int(fs.nadm)}/{len(D)} = {fs.nadm/len(D):.3f} of decisions, so CH_SPREAD and CH_ALL "
        f"differ by {abs(fs.price - fa.price):.4f} of Sharpe.")
    say("")
    t0r = TT[(TT.s == 0.00) & (TT.tol == 0)].iloc[0]
    say("  2. THE 2x2 AT THE FREE BAR (S+ = spread admits, M+ = mono admits):")
    for lbl in ("S+M+", "S+M-", "S-M+", "S-M-"):
        p = t0r[f"p_{lbl}"]
        say(f"       {lbl}  n = {int(t0r[f'n_{lbl}']):3d}   price "
            + (f"{p:+.4f}" if np.isfinite(p) else "-- (empty)"))
    off = int(t0r["n_S-M+"])
    say(f"     The off-diagonal S-M+ holds {off} decisions.  The mono bar "
        + ("NEVER admits a ladder the spread bar excludes, so the two bars are NESTED "
           "(mono is a strict sub-filter of spread), not complementary."
           if off == 0 else
           "does admit ladders the spread bar excludes, so the bars are genuinely crossed."))
    say("")
    mono_by_axis = D.groupby("axis").apply(lambda g: (g.rev == 0).mean())
    say("  3. THE MONO BAR IS A RUNG COUNTER (pre-declared outcome B).  Share of decisions that")
    say("     are EXACTLY MONOTONE, by ladder, against rung count k:")
    say("     " + "   ".join(f"{ax} (k={LAD[ax].__len__()}) {mono_by_axis[ax]:.3f}" for ax in AXES))
    say("     CADENCE's 1.000 is structural (gate G3): a 2-rung ladder has no reversal to find.")
    say("")
    say("  4. RULE 8, READ ONCE ON THE 2017-2026 FOLDS:")
    for _, r in E.iterrows():
        say(f"     {r.arm:10s} (s*={r.s:.2f}, tol*={r.tol}) H1 {r.h1:+.4f} -> OOS "
            f"{r.oos:+.4f} (t {r.t:+.2f}), null {r.null:+.4f}, edge {r.edge:+.4f}, "
            f"sign flip {r.flip}")
    nres = int((E.t.abs() >= 2).sum())
    say(f"     Arms resolved OOS at |t| >= 2: {nres} of {len(E)}.")
    say(f"     Arms whose price FLIPPED SIGN between the halves: "
        f"{list(E[E.flip=='YES'].arm) or 'NONE'}.")
    say("")
    say(f"  5. BOTH KEEP PATHS, {len(K)} stitched chooser curves: 4a passes {n4a}, "
        f"4b passes {n4b}.")
    for _, r in K[(K.k4a == 'YES') | (K.k4b == 'YES')].iterrows():
        say(f"     PASS {r.panel} {r.axis} {r.arm}: CAGR {r.CAGR:.1%} Sharpe {r.Sharpe:.2f} "
            f"MaxDD {r.MaxDD:.1%} 4a {r.k4a} 4b {r.k4b}")

    say("")
    say("-" * 108)
    say("GATES")
    for g in GATES:
        say(f"  [{'PASS' if g['pass_'] else 'FAIL':4s}] {g['gate']:34s} {g['value']:>24s} "
            f"target {g['target']}")
    say("-" * 108)
    say(f"  {time.time() - t0:.1f}s")

    out = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"
    D.to_csv(f"{out}_decisions.csv", index=False)
    TT.to_csv(f"{out}_2x2.csv", index=False)
    A.to_csv(f"{out}_arms.csv", index=False)
    K.to_csv(f"{out}_keep.csv", index=False)
    say(f"  wrote {out.name}_decisions.csv / _2x2.csv / _arms.csv / _keep.csv")
    return D, TT, A, E, K


if __name__ == "__main__":
    main()

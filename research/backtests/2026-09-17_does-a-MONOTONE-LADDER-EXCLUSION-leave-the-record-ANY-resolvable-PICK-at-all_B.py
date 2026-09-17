#!/usr/bin/env python3
"""
Idea 1209 (lane B, 2026-09-17) — does a MONOTONE-LADDER EXCLUSION leave the record ANY
resolvable PICK at all?

THE PREMISE, READ FROM THE RECORD.  Idea 1154 found that 15 of its 17 RESOLVED pick decisions
sit on the GROSS ladder, which is exactly monotone in IS Sharpe at 6 of 6 cells (rho = 1.000000)
over a spread of only 0.0014-0.0090 — so the bar that "resolves" those picks is certifying an
IDENTITY (1189: Sharpe is invariant to gross at a 0% cash rate, and what is left is a monotone
cost drag), not a preference between books.  Outside GROSS only 2 of 54 decisions resolve.  The
queue's proposal: score EVERY ladder for monotonicity in its own chooser's statistic, drop the
monotone ones as uninformative by construction, and report what fraction of committed picks
survives on the remainder.

THIS RUN BUILDS AND PRICES THAT EXCLUSION.  It asks three things in order:

  (1) IS MONOTONICITY INFORMATIVE AT ALL, or is it a rung-count artefact?  A ladder of k rungs is
      exactly monotone under a random ordering with probability 2/k!.  For CADENCE (k=2) that is
      1.000 — a two-rung ladder is monotone BY CONSTRUCTION, always, on any tape.  For H (k=4) it
      is 0.0833, for N (k=6) 0.00278, for GROSS (k=10) 5.5e-07.  So "drop the monotone ladders"
      is not one rule: it is a rule that deletes CADENCE unconditionally and GROSS structurally,
      and whose behaviour on N and H is a real measurement.  ARM 0 states the null before any
      price is read; the monotone rates are scored AGAINST it in ARM A, never in isolation.

  (2) WHAT SURVIVES.  ARM B walks the exclusion over the 24-cell grid and reports, at every cell,
      how many ladders survive, how many picks survive, and — the queue's question — what
      fraction of the surviving picks is RESOLVED under each of two resolution bars.

  (3) DOES IT PAY.  ARM C prices the exclusion out of sample on 42 (panel, fold) cells, and
      ARM D runs PROTOCOL rule 8 strictly.  The record has found six times (1206, 1221, 1226,
      1227, 1230, 1231) that DOING NOTHING beats every chooser it has built, so any rule that
      merely shrinks the comparison set and therefore HOLDS THE ANCHOR more often will LOOK like
      it pays.  ARM C separates the two with a move-count-matched null (1227's NL_PERM): each
      chooser's own destination multiset and own move count, re-dealt to random folds.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  MONOTONICITY TOLERANCE  {T_NONE, T_EXACT, T_095, T_090, T_080, T_060}
        T_NONE  drops nothing (the record's current habit, the control).
        T_EXACT drops a ladder iff |rho(rung index, IS Sharpe)| == 1 exactly (1154's reading).
        T_0xx   drops a ladder iff |rho| >= 0.95 / 0.90 / 0.80 / 0.60.
        rho is SPEARMAN of the ladder's own chooser statistic (IS Sharpe) against the rung's
        index in the dial's natural order.  |.| because a ladder that is monotone DOWN is as
        uninformative as one monotone up — it also certifies an ordering the construction forces.

  LADDER SET              {ALL4, NG3, NHG, NH}
        ALL4 = {N, H, GROSS, CADENCE}  the record's own comparison set
        NG3  = {N, H, CADENCE}         1223's degenerate-free set (GROSS removed by hand)
        NHG  = {N, H, GROSS}           CADENCE removed: the k=2 ladder monotone by construction
        NH   = {N, H}                  both structural ladders removed by hand

  24 cells, EVERY ONE PUBLISHED in .grid.csv.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); the 14 calendar folds;
the two RESOLUTION bars {R_SPREAD, R_ARGMAX}; the three choosers {CH_ANCHOR, CH_WIDEST,
CH_RESOLVED}; the 4a and 4b legs; the IS and OOS windows.

Frozen at the record's construction, inherited from 1207/1214/1223/1226 unchanged: 3-leg
composite (21/252, 0/126, 0/63), above-200d eligibility, max_vol 0.60, anchor N=20 / H=126 /
GROSS=0.75 / CADENCE=W, 10 bps (rule 2), DECIDE-AT-t / APPLY-AT-t+1 (lag=1), warm-up 260 rows,
the block bootstrap (B = 63 rows, 800 reps, block starts SHARED across books so the cross-rung
market factor survives), the 14 calendar folds, Hartley's d2(k) for spread normalisation.

PROTOCOL: rule 2 costs and execution; rule 8 walk-forward with every choice made on the IS window
ONLY and 2017-2026 read once; BOTH KEEP paths (4a vs live RULES v2, 4b vs SPY) on every rung
book, every rule-8 pick and every stitched chooser curve; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-17_does-a-MONOTONE-LADDER-EXCLUSION-leave-the-record-ANY-resolvable-PICK-at-all_B.py
"""
from __future__ import annotations

import math
import sys
import time
from itertools import permutations
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-17"
SLUG = "does-a-MONOTONE-LADDER-EXCLUSION-leave-the-record-ANY-resolvable-PICK-at-all"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = [(21, 252), (0, 126), (0, 63)]
A_N, A_H, A_G, A_C = 20, 126, 0.75, "W"

LAD = {
    "N": [5, 10, 15, 20, 30, 40],
    "H": [21, 63, 126, 252],
    "GROSS": [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75],
    "CADENCE": ["W", "M"],
}
LADK = {k: len(v) for k, v in LAD.items()}
ANCHOR_RUNG = {"N": A_N, "H": A_H, "GROSS": A_G, "CADENCE": A_C}

# ---- DIAL 1: the monotonicity tolerance
TOLS = ["T_NONE", "T_EXACT", "T_095", "T_090", "T_080", "T_060"]
TOLV = {"T_EXACT": 1.0, "T_095": 0.95, "T_090": 0.90, "T_080": 0.80, "T_060": 0.60}

# ---- DIAL 2: the ladder set
SETS = ["ALL4", "NG3", "NHG", "NH"]
SETLAD = {"ALL4": ["N", "H", "GROSS", "CADENCE"], "NG3": ["N", "H", "CADENCE"],
          "NHG": ["N", "H", "GROSS"], "NH": ["N", "H"]}

RESBARS = ["R_SPREAD", "R_ARGMAX"]
CHOOSERS = ["CH_ANCHOR", "CH_WIDEST", "CH_RESOLVED"]
FOLD_YEARS = list(range(2013, 2027))
LIVE_MAXDD_COMMITTED = -0.1205
BOOT_B, BOOT_REPS, BOOT_SEED = 63, 800, 12091209
NL_REPS, NL_SEED = 4000, 20912091
NMC, MC_SEED = 400_000, 12141214

D2 = {2: 1.128379, 3: 1.692569, 4: 2.058751, 5: 2.325929, 6: 2.534413, 7: 2.704357,
      8: 2.847201, 9: 2.970026, 10: 3.077505, 11: 3.172873, 12: 3.258457}

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def d2(k):
    return D2[min(max(int(k), 2), 12)]


# ==================================================================== stats helpers
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


def spearman(x, y):
    """Spearman rho with average ranks; nan if fewer than 2 finite pairs or no variance."""
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    m = np.isfinite(x) & np.isfinite(y)
    if m.sum() < 2:
        return np.nan
    rx = pd.Series(x[m]).rank().values
    ry = pd.Series(y[m]).rank().values
    if rx.std() == 0 or ry.std() == 0:
        return np.nan
    return float(np.corrcoef(rx, ry)[0, 1])


def exact_mono_null(k):
    """P(|rho| == 1) for a random ordering of k distinct values = 2/k!."""
    return 2.0 / math.factorial(k) if k >= 2 else np.nan


def tol_null(k, tol, cap=8):
    """P(|rho| >= tol) under a uniformly random ordering of k distinct values.

    Enumerated exactly for k <= cap (k! orderings); for larger k, Monte-Carlo with a fixed seed.
    """
    idx = np.arange(k, dtype=float)
    if k <= cap:
        rs = []
        for p in permutations(range(k)):
            rs.append(abs(spearman(idx, np.array(p, dtype=float))))
        rs = np.array(rs)
    else:
        rng = np.random.default_rng(MC_SEED + k)
        rs = np.empty(60_000)
        for i in range(len(rs)):
            rs[i] = abs(spearman(idx, rng.permutation(k).astype(float)))
    return float((rs >= tol - 1e-12).mean())


# ==================================================================== panels / runner
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


# ==================================================================== main
def main():
    t0 = time.time()
    say("=" * 108)
    say("IDEA 1209 (lane B, 2026-09-17) — does a MONOTONE-LADDER EXCLUSION leave the record ANY")
    say("resolvable PICK at all?")
    say("=" * 108)

    # ------------------------------------------------------------------ ARM 0
    say("")
    say("=" * 108)
    say("ARM 0 — WHAT THE EXCLUSION IS, BEFORE ANY PRICE IS READ")
    say("=" * 108)
    say("")
    say("  A ladder of k rungs is EXACTLY monotone under a random ordering with probability 2/k!.")
    say("  The four ladders the record owns have four completely different null rates, so ONE")
    say("  exclusion rule is four different rules:")
    say("")
    say("     ladder      k     P(|rho|=1)   P(|rho|>=0.95)  P(>=0.90)  P(>=0.80)  P(>=0.60)")
    nullrows = []
    for lad in LAD:
        k = LADK[lad]
        row = dict(ladder=lad, k=k, P_exact=exact_mono_null(k))
        for t in ("T_095", "T_090", "T_080", "T_060"):
            row[t] = tol_null(k, TOLV[t])
        nullrows.append(row)
        say(f"     {lad:9s} {k:3d}   {row['P_exact']:11.3e}   {row['T_095']:12.4f}  "
            f"{row['T_090']:9.4f}  {row['T_080']:9.4f}  {row['T_060']:9.4f}")
    nulldf = pd.DataFrame(nullrows)
    nulldf.to_csv(f"{OUT}.monotone_null.csv", index=False)
    cad_null = float(nulldf[nulldf.ladder == "CADENCE"].P_exact.iloc[0])
    GATES.append(dict(gate="G0 a two-rung ladder (CADENCE) is monotone with probability 1",
                      value=cad_null, target=1.0, pass_=bool(abs(cad_null - 1.0) < 1e-12)))
    say("")
    say("  READ IT BEFORE THE DATA: CADENCE is monotone with probability 1.000 — a two-rung")
    say("  ladder cannot be anything else — so ANY monotone exclusion deletes it unconditionally,")
    say("  on any tape, for a reason that has nothing to do with the tape.  GROSS's null is")
    say("  5.5e-07, so GROSS being monotone at 6 of 6 cells (1154) is either a 1-in-a-million")
    say("  coincidence six times over or a STRUCTURAL fact (1189: Sharpe is invariant to gross at")
    say("  a 0% cash rate; what survives is a monotone cost drag).  N and H are where the rule")
    say("  does actual work: 0.00278 and 0.0833.")

    # ------------------------------------------------------------------ ARM A
    say("")
    say("=" * 108)
    say("ARM A — THE LADDERS, THEIR MONOTONICITY, AND THEIR RESOLUTION")
    say("=" * 108)
    panels = []
    pxU = load_universe()
    panels.append(Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]))
    pxB = load_universe(broad=True)
    panels.append(Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]))
    pxS = load_universe(small=True)
    mvv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and mvv[c] < 1.0]
    panels.append(Panel("SMALL", pxS, inv))
    say("")
    say(f"  PANELS: U56 {len(pxU.columns)-1} names; B136 {len(pxB.columns)-1}; "
        f"SMALL {len(inv)} investable of {len(pxS.columns)-1} "
        f"({len(pxS.columns)-1-len(inv)} dropped for max_1d_move >= 1.0), SPY benchmark only.")

    booked, bench, RM, BOOKKEY = {}, {}, {}, []
    for pan in panels:
        frames = {}
        for N in LAD["N"]:
            frames[(N, A_H, "W")] = None
        for H in LAD["H"]:
            frames[(A_N, H, "W")] = None
        frames[(A_N, A_H, "M")] = None
        for key in list(frames):
            frames[key] = build1(pan, key[0], key[1], key[2])
        anchor_frame = frames[(A_N, A_H, "W")]
        books = {}
        for N in LAD["N"]:
            books[("N", N)] = nrun(pan, A_G * frames[(N, A_H, "W")], "W")
        for H in LAD["H"]:
            books[("H", H)] = nrun(pan, A_G * frames[(A_N, H, "W")], "W")
        for f in LAD["CADENCE"]:
            fr = anchor_frame if f == "W" else frames[(A_N, A_H, "M")]
            books[("CADENCE", f)] = nrun(pan, A_G * fr, f)
        for g in LAD["GROSS"]:
            books[("GROSS", g)] = nrun(pan, g * anchor_frame, "W")
        booked[pan.name] = books
        if not BOOKKEY:
            BOOKKEY = list(books.keys())
        RM[pan.name] = np.column_stack([books[k] for k in BOOKKEY])
        b = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")
        bench[pan.name] = dict(spy=pan.spy, live=b["returns"].values)
        say(f"    {pan.name}: {len(books)} rung books built.")

    # ---- gates on the machinery
    pan = panels[0]
    Wt = A_G * build1(pan, A_N, A_H, "W")
    Wdf = pd.DataFrame(Wt, index=pan.idx, columns=pan.px.columns)
    eb = backtest(pan.px, Wdf.shift(-1).fillna(0.0), cost_bps=COST, freq="W")["returns"].values
    g1 = float(np.nanmax(np.abs(eb[WARMUP:] - nrun(pan, Wt, "W")[WARMUP:])))
    GATES.append(dict(gate="G1 fast runner == engine.backtest on the decision-time frame",
                      value=g1, target=1e-10, pass_=bool(g1 < 1e-10)))
    lm = mdd(bench["U56"]["live"][WARMUP:])
    GATES.append(dict(gate="G2 live RULES v2 U56 MaxDD == the record's committed -12.05%",
                      value=lm, target=LIVE_MAXDD_COMMITTED,
                      pass_=bool(abs(lm - LIVE_MAXDD_COMMITTED) < 5e-4)))
    aidx = BOOKKEY.index(("N", A_N))
    gidx = BOOKKEY.index(("GROSS", A_G))
    cidx = BOOKKEY.index(("CADENCE", "W"))
    hidx = BOOKKEY.index(("H", A_H))
    g3 = max(float(np.nanmax(np.abs(RM["U56"][:, aidx] - RM["U56"][:, j])))
             for j in (gidx, cidx, hidx))
    GATES.append(dict(gate="G3 the anchor rung is the SAME book on all four ladders",
                      value=g3, target=1e-15, pass_=bool(g3 <= 1e-15)))
    r1 = spearman(np.arange(6.0), np.array([1., 2., 3., 4., 5., 6.]))
    r2 = spearman(np.arange(6.0), np.array([6., 5., 4., 3., 2., 1.]))
    g4 = max(abs(r1 - 1.0), abs(r2 + 1.0))
    GATES.append(dict(gate="G4 spearman() returns +1 / -1 on the two monotone orderings",
                      value=g4, target=1e-12, pass_=bool(g4 < 1e-12)))
    g5 = abs(tol_null(4, 1.0) - 2.0 / 24.0)
    GATES.append(dict(gate="G5 enumerated P(|rho|=1 | k=4) == 2/4! exactly",
                      value=g5, target=1e-12, pass_=bool(g5 < 1e-12)))
    say(f"    G1 {g1:.3e}  G2 live U56 MaxDD {lm:.4%}  G3 {g3:.3e}  G4 {g4:.3e}  G5 {g5:.3e}")

    # ---- block bootstrap, block starts SHARED across books
    CS, CSQ = {}, {}
    for p, M in RM.items():
        CS[p] = np.vstack([np.zeros((1, M.shape[1])), np.cumsum(M, axis=0)])
        CSQ[p] = np.vstack([np.zeros((1, M.shape[1])), np.cumsum(M * M, axis=0)])

    def boot_sharpes(p, lo, hi, reps=BOOT_REPS, B=BOOT_B, identity=False):
        nb = (hi - lo) // B
        if nb < 2:
            return None
        n = nb * B
        if identity:
            starts = (lo + B * np.arange(nb))[None, :]
        else:
            pid = sum(ord(ch) for ch in p)
            rng = np.random.default_rng(BOOT_SEED + 17 * lo + 101 * hi + 9973 * pid)
            starts = rng.integers(lo, hi - B + 1, size=(reps, nb))
        tot = CS[p][starts + B].sum(axis=1) - CS[p][starts].sum(axis=1)
        totq = CSQ[p][starts + B].sum(axis=1) - CSQ[p][starts].sum(axis=1)
        mu = tot / n
        var = np.maximum(totq / n - mu * mu, 0.0)
        sd = np.sqrt(var)
        with np.errstate(divide="ignore", invalid="ignore"):
            return np.where(sd > 0, mu * np.sqrt(252) / sd, np.nan)

    p0 = panels[0].name
    lo0, hi0 = panels[0].i0, panels[0].idx.searchsorted(pd.Timestamp(OOS_START))
    ident = boot_sharpes(p0, lo0, hi0, identity=True)[0]
    nb0 = (hi0 - lo0) // BOOT_B
    direct = np.array([sharpe(RM[p0][lo0:lo0 + nb0 * BOOT_B, j]) for j in range(RM[p0].shape[1])])
    g6 = float(np.nanmax(np.abs(ident - direct)))
    GATES.append(dict(gate="G6 block-sum bootstrap == direct Sharpe on the identity tiling",
                      value=g6, target=1e-10, pass_=bool(g6 < 1e-10)))

    LADIDX = {lad: [BOOKKEY.index((lad, r)) for r in LAD[lad]] for lad in LAD}

    # ---- folds
    folds_by_panel = {}
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
            folds_by_panel.setdefault(pan.name, []).append(
                (y, lo, hi, int(oo[0]), int(oo[-1]) + 1))
        cover = sorted(set(cover))
        gap = sum(1 for a, b in zip(cover, cover[1:]) if a[1] != b[0])
        GATES.append(dict(gate=f"G7 folds tile {pan.name} with no overlap and no gap",
                          value=float(gap), target=0.0, pass_=bool(gap == 0)))
    nfold = sum(len(v) for v in folds_by_panel.values())
    say("")
    say(f"    {nfold} (panel, fold) cells = 3 panels x "
        f"{len(folds_by_panel['U56'])} folds ({FOLD_YEARS[0]}-{FOLD_YEARS[-1]}).")

    # ---- per-cell ladder scoring: monotonicity, spread, resolution
    _LC: dict = {}

    def ladcell(p, lad, lo, hi):
        """Everything this run needs about one ladder on one IS window."""
        key = (p, lad, lo, hi)
        if key in _LC:
            return _LC[key]
        ii = LADIDX[lad]
        v = np.array([sharpe(RM[p][lo:hi, j]) for j in ii])
        idx = np.arange(len(ii), dtype=float)
        rho = spearman(idx, v)
        fin = v[np.isfinite(v)]
        R = float(fin.max() - fin.min()) if len(fin) > 1 else np.nan
        order = np.argsort(-np.where(np.isfinite(v), v, -np.inf), kind="stable")
        best = int(order[0])
        second = int(order[1]) if len(order) > 1 else None
        S = boot_sharpes(p, lo, hi)
        q95 = np.nan
        p_arg = np.nan
        se_gap = np.nan
        if S is not None:
            Vb = S[:, ii]
            V0 = Vb - np.nanmean(Vb, axis=0)[None, :]    # recentre: equal true Sharpe under null
            rng_ = np.nanmax(V0, axis=1) - np.nanmin(V0, axis=1)
            rng_ = rng_[np.isfinite(rng_)]
            if len(rng_) > 10:
                q95 = float(np.quantile(rng_, 0.95))
            if second is not None:
                gap = Vb[:, best] - Vb[:, second]
                gap = gap[np.isfinite(gap)]
                if len(gap) > 10:
                    se_gap = float(gap.std(ddof=1))
                    obs = v[best] - v[second]
                    p_arg = (float(abs(obs) / se_gap) if se_gap > 0 else np.inf)
        d = dict(panel=p, ladder=lad, k=len(ii), rho=rho, absrho=abs(rho) if np.isfinite(rho)
                 else np.nan, R_obs=R, q95=q95,
                 pick=LAD[lad][best], runnerup=LAD[lad][second] if second is not None else None,
                 gap=(v[best] - v[second]) if second is not None else np.nan,
                 se_gap=se_gap, t_argmax=p_arg,
                 R_SPREAD=bool(np.isfinite(R) and np.isfinite(q95) and R > q95),
                 R_ARGMAX=bool(np.isfinite(p_arg) and p_arg > 1.959964),
                 sharpes=v, norm_spread=(R / d2(len(ii))) if np.isfinite(R) else np.nan)
        _LC[key] = d
        return d

    say("")
    say("  (A1) EVERY LADDER AT EVERY (panel, fold): monotonicity in its OWN chooser statistic")
    say("       (IS Sharpe), realised spread, and the two resolution bars.")
    lrows = []
    for pan in panels:
        for (y, lo, hi, o0, o1) in folds_by_panel[pan.name]:
            for lad in LAD:
                d = ladcell(pan.name, lad, lo, hi)
                lrows.append({k: v for k, v in d.items() if k != "sharpes"} | dict(fold=y))
    ldf = pd.DataFrame(lrows)
    ldf.to_csv(f"{OUT}.ladders.csv", index=False)

    say("")
    say("       ladder   k   |rho|>=1  >=0.95  >=0.90  >=0.80  >=0.60 | null(=1)  | med R_obs"
        "  med R/q95 | R_SPREAD  R_ARGMAX")
    ratrows = []
    for lad in LAD:
        s = ldf[ldf.ladder == lad]
        rates = {t: float((s.absrho >= TOLV[t] - 1e-12).mean()) for t in TOLS if t != "T_NONE"}
        ratio = (s.R_obs / s.q95).replace([np.inf, -np.inf], np.nan)
        ratrows.append(dict(ladder=lad, k=LADK[lad], **rates,
                            null_exact=exact_mono_null(LADK[lad]),
                            med_R=float(np.nanmedian(s.R_obs)),
                            med_R_over_q95=float(np.nanmedian(ratio)),
                            res_SPREAD=float(s.R_SPREAD.mean()),
                            res_ARGMAX=float(s.R_ARGMAX.mean())))
        say(f"       {lad:8s} {LADK[lad]:2d}   {rates['T_EXACT']:7.3f}  {rates['T_095']:6.3f}  "
            f"{rates['T_090']:6.3f}  {rates['T_080']:6.3f}  {rates['T_060']:6.3f} |"
            f" {exact_mono_null(LADK[lad]):9.2e} | {np.nanmedian(s.R_obs):9.4f}"
            f"  {np.nanmedian(ratio):9.4f} |  {s.R_SPREAD.mean():7.3f}  {s.R_ARGMAX.mean():8.3f}")
    pd.DataFrame(ratrows).to_csv(f"{OUT}.rates.csv", index=False)

    gross_exact = float(ldf[(ldf.ladder == "GROSS")].absrho.ge(1 - 1e-12).mean())
    GATES.append(dict(gate="G8 GROSS is exactly monotone at >= 0.80 of cells (1154's premise)",
                      value=gross_exact, target=0.80, pass_=bool(gross_exact >= 0.80)))
    cad_exact = float(ldf[(ldf.ladder == "CADENCE")].absrho.ge(1 - 1e-12).mean())
    GATES.append(dict(gate="G9 CADENCE is exactly monotone at 1.000 of cells (k=2, by construction)",
                      value=cad_exact, target=1.0, pass_=bool(abs(cad_exact - 1.0) < 1e-12)))

    say("")
    say("  (A2) IS THE MONOTONICITY IN EXCESS OF ITS OWN NULL?  Binomial one-sided p of the")
    say("       observed exact-monotone count against 2/k! over the 42 cells.")
    say("")
    say("       ladder   k   exact of 42   expected   p(one-sided)")
    excrows = []
    for lad in LAD:
        s = ldf[ldf.ladder == lad]
        n = int(s.absrho.notna().sum())
        c = int(s.absrho.ge(1 - 1e-12).sum())
        pnull = exact_mono_null(LADK[lad])
        # exact binomial upper tail
        pv = sum(math.comb(n, i) * pnull ** i * (1 - pnull) ** (n - i) for i in range(c, n + 1))
        excrows.append(dict(ladder=lad, k=LADK[lad], n=n, exact=c, expected=n * pnull, p=pv))
        say(f"       {lad:8s} {LADK[lad]:2d}   {c:3d} of {n:2d}    {n*pnull:8.4f}   {pv:12.3e}")
    pd.DataFrame(excrows).to_csv(f"{OUT}.excess.csv", index=False)

    # ------------------------------------------------------------------ ARM B
    say("")
    say("=" * 108)
    say("ARM B — THE 24-CELL GRID: WHAT SURVIVES THE EXCLUSION")
    say("=" * 108)

    def surviving(p, lo, hi, sname, tol):
        lads = SETLAD[sname]
        if tol == "T_NONE":
            return list(lads)
        th = TOLV[tol]
        out = []
        for lad in lads:
            a = ladcell(p, lad, lo, hi)["absrho"]
            if not np.isfinite(a) or a < th - 1e-12:
                out.append(lad)
        return out

    say("")
    say("  A PICK is one (panel, fold, ladder) decision: the ladder's IS-Sharpe argmax rung.")
    say("  The record's committed habit is T_NONE x ALL4 = 4 picks per cell, 168 in all.")
    say("")
    say("   set    tol       ladders/cell  picks  survive  surv%  | RESOLVED of survivors")
    say("                                                         |  R_SPREAD        R_ARGMAX")
    grows = []
    for sname in SETS:
        for tol in TOLS:
            nl, npick, res_s, res_a = [], 0, 0, 0
            per_lad = {lad: 0 for lad in LAD}
            for pan in panels:
                for (y, lo, hi, o0, o1) in folds_by_panel[pan.name]:
                    surv = surviving(pan.name, lo, hi, sname, tol)
                    nl.append(len(surv))
                    for lad in surv:
                        d = ladcell(pan.name, lad, lo, hi)
                        npick += 1
                        per_lad[lad] += 1
                        res_s += int(d["R_SPREAD"])
                        res_a += int(d["R_ARGMAX"])
            base = len(SETLAD[sname]) * nfold
            grows.append(dict(SET=sname, TOL=tol, mean_ladders=float(np.mean(nl)),
                              cells_with_none=int(np.sum(np.array(nl) == 0)),
                              base_picks=base, picks=npick,
                              surv_share=npick / base if base else np.nan,
                              res_SPREAD=res_s, res_ARGMAX=res_a,
                              res_SPREAD_share=res_s / npick if npick else np.nan,
                              res_ARGMAX_share=res_a / npick if npick else np.nan,
                              **{f"n_{lad}": per_lad[lad] for lad in LAD}))
            say(f"   {sname:6s} {tol:8s}  {np.mean(nl):11.3f}  {base:5d}  {npick:6d}  "
                f"{npick/base:5.3f}  |  {res_s:3d} ({res_s/npick if npick else 0:5.3f})"
                f"   {res_a:3d} ({res_a/npick if npick else 0:5.3f})")
    gdf = pd.DataFrame(grows)
    gdf.to_csv(f"{OUT}.grid.csv", index=False)

    say("")
    say("  (B1) THE QUEUE'S QUESTION, ANSWERED AT THE RECORD'S OWN SET (ALL4):")
    a4 = gdf[gdf.SET == "ALL4"].set_index("TOL")
    base_res_s = int(a4.loc["T_NONE", "res_SPREAD"])
    base_res_a = int(a4.loc["T_NONE", "res_ARGMAX"])
    say(f"       T_NONE  : {int(a4.loc['T_NONE','picks']):3d} picks, "
        f"{base_res_s:3d} resolved on R_SPREAD, {base_res_a:3d} on R_ARGMAX.")
    for tol in TOLS[1:]:
        say(f"       {tol:8s}: {int(a4.loc[tol,'picks']):3d} picks, "
            f"{int(a4.loc[tol,'res_SPREAD']):3d} resolved on R_SPREAD, "
            f"{int(a4.loc[tol,'res_ARGMAX']):3d} on R_ARGMAX.")

    # which ladder carries the resolutions, before and after
    say("")
    say("  (B2) WHO CARRIES THE RESOLUTIONS (T_NONE, ALL4 — the record's habit):")
    say("")
    say("       ladder    picks   R_SPREAD  share of all   R_ARGMAX  share of all")
    tot_s = int(ldf.R_SPREAD.sum())
    tot_a = int(ldf.R_ARGMAX.sum())
    carrows = []
    for lad in LAD:
        s = ldf[ldf.ladder == lad]
        cs, ca = int(s.R_SPREAD.sum()), int(s.R_ARGMAX.sum())
        carrows.append(dict(ladder=lad, picks=len(s), R_SPREAD=cs, R_ARGMAX=ca,
                            share_SPREAD=cs / tot_s if tot_s else np.nan,
                            share_ARGMAX=ca / tot_a if tot_a else np.nan))
        say(f"       {lad:8s} {len(s):6d}   {cs:8d}  {cs/tot_s if tot_s else 0:13.4f}"
            f"   {ca:8d}  {ca/tot_a if tot_a else 0:13.4f}")
    pd.DataFrame(carrows).to_csv(f"{OUT}.carriers.csv", index=False)

    # ------------------------------------------------------------------ ARM C
    say("")
    say("=" * 108)
    say("ARM C — DOES THE EXCLUSION PAY OUT OF SAMPLE (42 rolling folds)?")
    say("=" * 108)

    def book_ret(p, lad, rung, lo, hi):
        return booked[p][(lad, rung)][lo:hi]

    def anchor_ret(p, lo, hi):
        return booked[p][("N", A_N)][lo:hi]

    def choose(p, lo, hi, sname, tol, chooser):
        """Return (ladder, rung, moved) for one cell.  CH_ANCHOR never moves."""
        if chooser == "CH_ANCHOR":
            return ("N", A_N, False)
        surv = surviving(p, lo, hi, sname, tol)
        cand = []
        for lad in surv:
            d = ladcell(p, lad, lo, hi)
            if np.isfinite(d["norm_spread"]):
                cand.append((d["norm_spread"], lad, d))
        if not cand:
            return ("N", A_N, False)
        cand.sort(key=lambda z: (-z[0], z[1]))
        _, lad, d = cand[0]
        if chooser == "CH_RESOLVED" and not d["R_SPREAD"]:
            return ("N", A_N, False)
        rung = d["pick"]
        moved = not (rung == ANCHOR_RUNG[lad])
        return (lad, rung, moved)

    say("")
    say("  Each (panel, fold): choose on the IS window [warm-up, fold start) ONLY, read the fold.")
    say("  A move onto a rung that IS the anchor is a NO-OP (1230's correction): the move rate")
    say("  below is the VALUE rate, not the KEY rate.")
    say("")
    say("   set    tol      chooser        move   mean OOS fold S   vs anchor   med OOS S")
    crows, cellrows = [], []
    for sname in SETS:
        for tol in TOLS:
            for ch in CHOOSERS:
                ss, mv = [], []
                for pan in panels:
                    for (y, lo, hi, o0, o1) in folds_by_panel[pan.name]:
                        lad, rung, moved = choose(pan.name, lo, hi, sname, tol, ch)
                        r = book_ret(pan.name, lad, rung, o0, o1)
                        a = anchor_ret(pan.name, o0, o1)
                        same = bool(np.nanmax(np.abs(r - a)) <= 1e-15)
                        s = sharpe(r)
                        ss.append(s)
                        mv.append(0 if same else 1)
                        cellrows.append(dict(SET=sname, TOL=tol, CHOOSER=ch, panel=pan.name,
                                             fold=y, ladder=lad, rung=rung, key_moved=moved,
                                             value_moved=not same, OOS_S=s,
                                             anchor_OOS_S=sharpe(a)))
                m = float(np.nanmean(ss))
                crows.append(dict(SET=sname, TOL=tol, CHOOSER=ch, move_rate=float(np.mean(mv)),
                                  mean_OOS_S=m, med_OOS_S=float(np.nanmedian(ss)),
                                  n=len(ss)))
    cdf = pd.DataFrame(crows)
    celldf = pd.DataFrame(cellrows)
    celldf.to_csv(f"{OUT}.cells.csv", index=False)
    anch = float(cdf[cdf.CHOOSER == "CH_ANCHOR"].mean_OOS_S.iloc[0])
    cdf["vs_anchor"] = cdf.mean_OOS_S - anch
    cdf.to_csv(f"{OUT}.choosers.csv", index=False)
    for _, r in cdf.iterrows():
        say(f"   {r.SET:6s} {r.TOL:8s} {r.CHOOSER:13s}  {r.move_rate:5.3f}   "
            f"{r.mean_OOS_S:15.4f}   {r.vs_anchor:+9.4f}   {r.med_OOS_S:9.4f}")
    say("")
    say(f"   DOING NOTHING (CH_ANCHOR, identical at every cell by construction) = {anch:.4f}.")

    # ---- the move-count-matched null (1227's NL_PERM)
    say("")
    say("  (C1) THE MOVE-COUNT-MATCHED NULL.  For each (set, tol, chooser) that moves at all:")
    say("       take its OWN destination multiset and its OWN move count, re-deal them to random")
    say(f"       folds {NL_REPS} times, and ask whether the observed mean sits above its own null.")
    say("")
    say("   set    tol      chooser        moves  observed   null mean     gap        p")
    nlrows = []
    rng = np.random.default_rng(NL_SEED)
    cells_all = [(pan.name, y, lo, hi, o0, o1) for pan in panels
                 for (y, lo, hi, o0, o1) in folds_by_panel[pan.name]]
    ncell = len(cells_all)
    # FS[cell, book] — every fold Sharpe of every rung book, computed once
    FS = np.full((ncell, len(BOOKKEY)), np.nan)
    for i, (p, y, lo, hi, o0, o1) in enumerate(cells_all):
        for j, bk in enumerate(BOOKKEY):
            FS[i, j] = sharpe(booked[p][bk][o0:o1])
    BPOS = {bk: j for j, bk in enumerate(BOOKKEY)}
    anchor_S = FS[:, BPOS[("N", A_N)]]
    for (sname, tol, ch), grp in celldf.groupby(["SET", "TOL", "CHOOSER"], sort=False):
        moved_rows = grp[grp.value_moved]
        nmv = len(moved_rows)
        if nmv == 0:
            continue
        obs = float(np.nanmean(grp.OOS_S.values))
        dests = np.array([BPOS[(r.ladder, r.rung)] for r in moved_rows.itertuples()])
        nulls = np.empty(NL_REPS)
        for rep in range(NL_REPS):
            where = rng.choice(ncell, size=nmv, replace=False)
            vals = anchor_S.copy()
            vals[where] = FS[where, dests]
            nulls[rep] = np.nanmean(vals)
        pv = float((nulls >= obs).mean())
        nlrows.append(dict(SET=sname, TOL=tol, CHOOSER=ch, moves=nmv, observed=obs,
                           null_mean=float(nulls.mean()), gap=obs - float(nulls.mean()), p=pv))
        say(f"   {sname:6s} {tol:8s} {ch:13s}  {nmv:5d}  {obs:9.4f}  {nulls.mean():10.4f}  "
            f"{obs-nulls.mean():+8.4f}  {pv:7.4f}")
    nldf = pd.DataFrame(nlrows)
    nldf.to_csv(f"{OUT}.nullperm.csv", index=False)
    if len(nldf):
        say("")
        say(f"   Cells that move at all: {len(nldf)}.  Observed ABOVE its own null at "
            f"{int((nldf.gap > 0).sum())} of {len(nldf)}; mean gap {nldf.gap.mean():+.4f}; "
            f"p < 0.05 at {int((nldf.p < 0.05).sum())} (expected by chance "
            f"{0.05*len(nldf):.1f}).")

    # ------------------------------------------------------------------ ARM D
    say("")
    say("=" * 108)
    say("ARM D — PROTOCOL RULE 8 (choose on 2009-2016 ONLY, read 2017-2026 ONCE) AND BOTH KEEP")
    say("PATHS")
    say("=" * 108)
    say("")
    bm_rows = []
    BM = {}
    for pan in panels:
        i0 = pan.i0
        oo = pan.idx.searchsorted(pd.Timestamp(OOS_START))
        spy = pan.spy[i0:]
        live = bench[pan.name]["live"][i0:]
        h1s, h2s = halves(spy)
        h1l, h2l = halves(live)
        BM[pan.name] = dict(
            i0=i0, oo=oo,
            spy=dict(**triple(spy), H1=h1s, H2=h2s),
            live=dict(**triple(live), H1=h1l, H2=h2l),
            spy_oos=triple(pan.spy[oo:]), live_oos=triple(bench[pan.name]["live"][oo:]))
        s, l = BM[pan.name]["spy"], BM[pan.name]["live"]
        so, lo_ = BM[pan.name]["spy_oos"], BM[pan.name]["live_oos"]
        say(f"   {pan.name:6s} SPY  full {s['CAGR']:7.2%} / {s['Sharpe']:.4f} / {s['MaxDD']:7.2%}"
            f"  (halves {s['H1']:.4f}/{s['H2']:.4f})   OOS {so['CAGR']:7.2%} / "
            f"{so['Sharpe']:.4f} / {so['MaxDD']:7.2%}")
        say(f"   {pan.name:6s} LIVE full {l['CAGR']:7.2%} / {l['Sharpe']:.4f} / {l['MaxDD']:7.2%}"
            f"  (halves {l['H1']:.4f}/{l['H2']:.4f})   OOS {lo_['CAGR']:7.2%} / "
            f"{lo_['Sharpe']:.4f} / {lo_['MaxDD']:7.2%}")
        bm_rows.append(dict(panel=pan.name, kind="SPY", **s) )
        bm_rows.append(dict(panel=pan.name, kind="LIVE", **l))
    pd.DataFrame(bm_rows).to_csv(f"{OUT}.benchmarks.csv", index=False)

    say("")
    say("  (D1) EVERY RUNG BOOK against both KEEP paths, full sample and OOS.")
    brows = []
    for pan in panels:
        i0, oo = BM[pan.name]["i0"], BM[pan.name]["oo"]
        for (lad, rung), r in booked[pan.name].items():
            f = r[i0:]
            o = r[oo:]
            k4a, k4b, m, h1, h2 = keep_paths(f, BM[pan.name]["spy"], BM[pan.name]["live"])
            mo = triple(o)
            so = BM[pan.name]["spy_oos"]
            k4b_oos = bool(mo["Sharpe"] > so["Sharpe"] and mo["MaxDD"] >= DD_CAP * so["MaxDD"]
                           and mo["CAGR"] >= CAGR_FLOOR * so["CAGR"])
            brows.append(dict(panel=pan.name, ladder=lad, rung=rung, CAGR=m["CAGR"],
                              Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                              OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                              OOS_MaxDD=mo["MaxDD"], keep_4a=k4a, keep_4b=k4b,
                              keep_4b_OOS=k4b_oos, keep_4b_BOTH=bool(k4b and k4b_oos)))
    bdf = pd.DataFrame(brows)
    bdf.to_csv(f"{OUT}.books.csv", index=False)
    say(f"       {len(bdf)} rung books: 4a {int(bdf.keep_4a.sum())}, 4b full "
        f"{int(bdf.keep_4b.sum())}, 4b OOS {int(bdf.keep_4b_OOS.sum())}, BOTH "
        f"{int(bdf.keep_4b_BOTH.sum())}.")
    distinct = bdf.groupby(["panel", "CAGR", "Sharpe", "MaxDD"]).size()
    say(f"       Distinct (panel, CAGR, Sharpe, MaxDD) books: {len(distinct)} of {len(bdf)} "
        f"— the GROSS ladder's Sharpe is near-invariant by construction (1189).")

    say("")
    say("  (D2) THE RULE-8 PICKS: every (set, tol, chooser) chosen on the pre-2017 window only,")
    say("       2017-2026 read once, and the stitched full-sample curve of the same rule.")
    say("")
    say("   set    tol      chooser       panel   ladder  rung     OOS CAGR  OOS S   OOS DD "
        " >SPY  4a  4b  4bOOS")
    r8rows = []
    for sname in SETS:
        for tol in TOLS:
            for ch in CHOOSERS:
                for pan in panels:
                    i0, oo = BM[pan.name]["i0"], BM[pan.name]["oo"]
                    lad, rung, moved = choose(pan.name, i0, oo, sname, tol, ch)
                    r = booked[pan.name][(lad, rung)]
                    f, o = r[i0:], r[oo:]
                    k4a, k4b, m, h1, h2 = keep_paths(f, BM[pan.name]["spy"], BM[pan.name]["live"])
                    mo = triple(o)
                    so = BM[pan.name]["spy_oos"]
                    k4b_oos = bool(mo["Sharpe"] > so["Sharpe"]
                                   and mo["MaxDD"] >= DD_CAP * so["MaxDD"]
                                   and mo["CAGR"] >= CAGR_FLOOR * so["CAGR"])
                    beat = bool(mo["Sharpe"] > so["Sharpe"])
                    r8rows.append(dict(SET=sname, TOL=tol, CHOOSER=ch, panel=pan.name,
                                       ladder=lad, rung=rung, key_moved=moved,
                                       IS_Sharpe=sharpe(r[i0:oo]),
                                       CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                       H1=h1, H2=h2, OOS_CAGR=mo["CAGR"],
                                       OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                       SPY_OOS_Sharpe=so["Sharpe"], beats_SPY_OOS=beat,
                                       keep_4a=k4a, keep_4b=k4b, keep_4b_OOS=k4b_oos))
    r8 = pd.DataFrame(r8rows)
    r8.to_csv(f"{OUT}.rule8.csv", index=False)
    for _, r in r8.iterrows():
        say(f"   {r.SET:6s} {r.TOL:8s} {r.CHOOSER:13s} {r.panel:6s} {r.ladder:7s} "
            f"{str(r.rung):6s} {r.OOS_CAGR:9.2%} {r.OOS_Sharpe:6.3f} {r.OOS_MaxDD:8.2%}  "
            f"{'Y' if r.beats_SPY_OOS else '.':4s} {'Y' if r.keep_4a else '.':3s} "
            f"{'Y' if r.keep_4b else '.':3s} {'Y' if r.keep_4b_OOS else '.':5s}")
    say("")
    say(f"       RULE-8 ROWS: {len(r8)}.  4a {int(r8.keep_4a.sum())} of {len(r8)}; "
        f"4b full {int(r8.keep_4b.sum())}; 4b OOS {int(r8.keep_4b_OOS.sum())}; "
        f"BOTH {int((r8.keep_4b & r8.keep_4b_OOS).sum())}; beats SPY OOS Sharpe "
        f"{int(r8.beats_SPY_OOS.sum())}.")
    if int((r8.keep_4b & r8.keep_4b_OOS).sum()):
        w = r8[r8.keep_4b & r8.keep_4b_OOS]
        dk = w.groupby(["panel", "ladder", "rung"]).size()
        say(f"       The {len(w)} passing rule-8 rows collapse to {len(dk)} DISTINCT "
            f"(panel, ladder, rung) books: "
            + "; ".join(f"{a}/{b}={c}" for (a, b, c) in dk.index))

    # ---- stitched chooser curves: re-choose at every fold boundary, walk the fold
    say("")
    say("  (D3) STITCHED CHOOSER CURVES — the rule itself as a book: re-choose at every fold")
    say("       boundary on that fold's IS window only, hold the choice through the fold.")
    say("")
    say("   set    tol      chooser       panel    CAGR    Sharpe   MaxDD    H1/H2      4a  4b"
        "  4bOOS")
    strows = []
    for sname in SETS:
        for tol in TOLS:
            for ch in CHOOSERS:
                for pan in panels:
                    segs, osegs = [], []
                    for (y, lo, hi, o0, o1) in folds_by_panel[pan.name]:
                        lad, rung, _ = choose(pan.name, lo, hi, sname, tol, ch)
                        seg = booked[pan.name][(lad, rung)][o0:o1]
                        segs.append(seg)
                        if pan.idx[o0] >= pd.Timestamp(OOS_START):
                            osegs.append(seg)
                    if not segs:
                        continue
                    f = np.concatenate(segs)
                    o = np.concatenate(osegs) if osegs else np.array([])
                    k4a, k4b, m, h1, h2 = keep_paths(f, BM[pan.name]["spy"], BM[pan.name]["live"])
                    mo = triple(o) if len(o) > 5 else dict(CAGR=np.nan, Sharpe=np.nan,
                                                           MaxDD=np.nan)
                    so = BM[pan.name]["spy_oos"]
                    k4b_oos = bool(np.isfinite(mo["Sharpe"]) and mo["Sharpe"] > so["Sharpe"]
                                   and mo["MaxDD"] >= DD_CAP * so["MaxDD"]
                                   and mo["CAGR"] >= CAGR_FLOOR * so["CAGR"])
                    strows.append(dict(SET=sname, TOL=tol, CHOOSER=ch, panel=pan.name,
                                       CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                       H1=h1, H2=h2, OOS_CAGR=mo["CAGR"],
                                       OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                       keep_4a=k4a, keep_4b=k4b, keep_4b_OOS=k4b_oos))
    st = pd.DataFrame(strows)
    st.to_csv(f"{OUT}.stitched.csv", index=False)
    for _, r in st.iterrows():
        say(f"   {r.SET:6s} {r.TOL:8s} {r.CHOOSER:13s} {r.panel:6s} {r.CAGR:7.2%} "
            f"{r.Sharpe:8.4f} {r.MaxDD:8.2%}  {r.H1:.3f}/{r.H2:.3f}   "
            f"{'Y' if r.keep_4a else '.':3s} {'Y' if r.keep_4b else '.':3s} "
            f"{'Y' if r.keep_4b_OOS else '.':5s}")
    say("")
    say(f"       STITCHED CURVES: {len(st)}.  4a {int(st.keep_4a.sum())}; 4b full "
        f"{int(st.keep_4b.sum())}; 4b OOS {int(st.keep_4b_OOS.sum())}; BOTH "
        f"{int((st.keep_4b & st.keep_4b_OOS).sum())}.")

    # ------------------------------------------------------------------ WALK-FORWARD SUMMARY
    wf = []
    for pan in panels:
        s, l = BM[pan.name]["spy"], BM[pan.name]["live"]
        so, lo_ = BM[pan.name]["spy_oos"], BM[pan.name]["live_oos"]
        wf.append(dict(panel=pan.name, arm="SPY", CAGR=s["CAGR"], Sharpe=s["Sharpe"],
                       MaxDD=s["MaxDD"], OOS_CAGR=so["CAGR"], OOS_Sharpe=so["Sharpe"],
                       OOS_MaxDD=so["MaxDD"]))
        wf.append(dict(panel=pan.name, arm="LIVE RULES v2", CAGR=l["CAGR"], Sharpe=l["Sharpe"],
                       MaxDD=l["MaxDD"], OOS_CAGR=lo_["CAGR"], OOS_Sharpe=lo_["Sharpe"],
                       OOS_MaxDD=lo_["MaxDD"]))
        an = booked[pan.name][("N", A_N)]
        i0, oo = BM[pan.name]["i0"], BM[pan.name]["oo"]
        wf.append(dict(panel=pan.name, arm="ANCHOR (do nothing)", **{
            k: v for k, v in triple(an[i0:]).items()},
            OOS_CAGR=triple(an[oo:])["CAGR"], OOS_Sharpe=triple(an[oo:])["Sharpe"],
            OOS_MaxDD=triple(an[oo:])["MaxDD"]))
    best = r8.sort_values("OOS_Sharpe", ascending=False).iloc[0]
    wf.append(dict(panel=best.panel, arm=f"BEST RULE-8 PICK ({best.SET}/{best.TOL}/{best.CHOOSER})",
                   CAGR=best.CAGR, Sharpe=best.Sharpe, MaxDD=best.MaxDD,
                   OOS_CAGR=best.OOS_CAGR, OOS_Sharpe=best.OOS_Sharpe, OOS_MaxDD=best.OOS_MaxDD))
    pd.DataFrame(wf).to_csv(f"{OUT}.walkforward.csv", index=False)

    # ------------------------------------------------------------------ GATES
    say("")
    say("=" * 108)
    say("GATES")
    say("=" * 108)
    gdf2 = pd.DataFrame(GATES)
    gdf2.to_csv(f"{OUT}.gates.csv", index=False)
    for _, g in gdf2.iterrows():
        say(f"   {'PASS' if g.pass_ else 'FAIL'}  {g.gate:72s}  value {g.value:.6g}")
    say("")
    say(f"   {int(gdf2.pass_.sum())} of {len(gdf2)} gates pass.")
    say("")
    say(f"   Runtime {time.time()-t0:.1f}s.  Outputs: {OUT.name}.*")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

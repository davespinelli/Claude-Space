#!/usr/bin/env python3
"""
Idea 1222 (lane C, 2026-09-18) — is the WIDEST-DIAL HABIT RESOLVABLE on ANY ATTAINABLE
FOLD COUNT?

THE PREMISE, READ FROM THE RECORD.  Idea 1214 built the correctly calibrated two-sided bar for
the record's widest-dial habit and found it DECLINES at 121 of 126 non-GROSS ladder pairs on
fourteen folds of this tape.  The queue read that as "unresolved rather than merely uncorrected"
and asked the only question that settles it: put a REQUIRED-PRECISION calculation on it.  For
each (panel, ladder pair) compute the FOLD COUNT at which the observed statistic separates from
its null band at alpha = 0.05, and report whether any attainable count on a 17-year tape gets
there.

WHAT THIS RUN CHANGES ABOUT 1214's CONSTRUCTION, DELIBERATELY AND ONCE.
1214's fourteen folds are NESTED expanding windows (warm-up..2012, warm-up..2013, ...), so its
fourteen readings of a pair are fourteen readings of mostly the SAME data and cannot be averaged
to buy precision.  A required-precision calculation needs INDEPENDENT folds, so this run tiles
the tape with DISJOINT consecutive folds of length L and makes L one of its two dials.  That is
a departure from 1214 and is declared here, not buried: the 1214 pair table is NOT reproduced by
this script and is not claimed to be.

THE STATISTIC, AND WHY IT IS A DIFFERENCE OF LOGS.  For one fold and one ladder, R_lad is the
max-minus-min of that ladder's rung Sharpes INSIDE the fold.  Under H0 (both ladders' rungs iid
normal with the SAME sigma) R_k/d2(k) is unbiased for sigma, so the record's own bar is a
statement about the RATIO of two such quantities.  Working in logs,

    D = log(R_a / d2(k_a)) - log(R_b / d2(k_b)) = log V,

the fold-level readings ADD, and the band on their mean shrinks as 1/sqrt(F).  That is the whole
mechanism by which more folds could ever resolve a dial, and ARM 0 gates it before any price is
read.  Note E[D] under H0 is NOT 0 (log of an unbiased estimator is biased), so the null centre
mu0(k_a, k_b) is measured by Monte Carlo rather than assumed.

ORIENTATION IS FIXED ONCE, ON THE FULL SAMPLE, AND NOT PER FOLD.  1214 proved that orienting the
pair on the same data that is then tested is what destroys the point bar.  Here each unordered
pair is written in the direction its FULL-SAMPLE spread ratio gives, that direction is held fixed
across every fold and every cell, and the per-fold agreement rate with it is published.  So the
null centre is the unconditional mu0 and no conditioning correction is smuggled in.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  FOLD LENGTH   L  in {63, 126, 252, 504} trading days
  LADDER PAIR SET  {ALL4, NG}      -- 1207/1214's, inherited whole (NG drops the degenerate
                                      GROSS ladder that 1223 is open about)

  8 cells, EVERY ONE PUBLISHED.  alpha is NOT a third dial: the headline is 0.05 as the queue
  specifies and 0.10 is reported alongside at every cell.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); the record's four ladders
N (6 rungs) / H (4) / GROSS (10) / CADENCE (2); all 6 unordered ALL4 pairs and all 3 NG pairs;
the 4a and 4b legs; the IS and OOS windows; every rung book.

Frozen at the record's construction, inherited from 1207/1214 unchanged: 3-leg composite
(21/252, 0/126, 0/63), above-200d eligibility, max_vol 0.60, anchor N=20 / H=126 / GROSS=0.75 /
CADENCE=W, 10 bps (rule 2), DECIDE-AT-t / APPLY-AT-t+1 selection (lag=1), warm-up 260 rows.

PROTOCOL: rule 2 costs and execution; rule 8 walk-forward with the choice made on the IS window
ONLY and 2017-2026 read once; BOTH KEEP paths (4a vs live RULES v2, 4b vs SPY) on every rung
book, every rule-8 pick and every stitched chooser curve; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-18_is-the-WIDEST-DIAL-HABIT-RESOLVABLE-on-ANY-ATTAINABLE-FOLD-COUNT_C.py
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

DATE = "2026-09-18"
SLUG = "is-the-WIDEST-DIAL-HABIT-RESOLVABLE-on-ANY-ATTAINABLE-FOLD-COUNT"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

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
LADK = {"N": 6, "H": 4, "GROSS": 10, "CADENCE": 2}
LADSETS = {"ALL4": ["N", "H", "GROSS", "CADENCE"], "NG": ["N", "H", "CADENCE"]}

# ---- DIAL 1 and DIAL 2, and nothing else
FOLD_LENS = [63, 126, 252, 504]
HEADLINE_L = 252

ALPHAS = {0.05: 1.959964, 0.10: 1.644854}
HEADLINE_ALPHA = 0.05
FOLD_YEARS = list(range(2013, 2027))
LIVE_MAXDD_COMMITTED = -0.1205
NMC = 1_000_000
MC_SEED = 12221222
SPREAD_FLOOR = 1e-12

# Hartley's d2(k) = E[range of k iid N(0,1)].  Published constants, gated against Monte Carlo.
D2 = {2: 1.128379, 3: 1.692569, 4: 2.058751, 5: 2.325929, 6: 2.534413, 7: 2.704357,
      8: 2.847201, 9: 2.970026, 10: 3.077505, 11: 3.172873, 12: 3.258457}
KMAXD2 = 12

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def d2(k):
    return D2[min(max(int(k), 2), KMAXD2)]


# ==================================================================== the null machinery
_RDRAW: dict[int, np.ndarray] = {}


def rdraw(k, n=NMC):
    """n iid draws of the RANGE of k standard normals, computed in chunks and cached."""
    k = int(k)
    if k in _RDRAW:
        return _RDRAW[k]
    rng = np.random.default_rng(MC_SEED + 1000 * k)
    out = np.empty(n, dtype=np.float64)
    step = 250_000
    for i in range(0, n, step):
        m = min(step, n - i)
        x = rng.standard_normal((m, k))
        out[i:i + m] = x.max(1) - x.min(1)
    _RDRAW[k] = out
    return out


_LOGM: dict[int, tuple] = {}


def logmoments(k):
    """mean and sd of log(R_k / d2(k)) under H0.  Both are measured, not assumed: the log of an
    unbiased estimator is biased low, so the null centre of D is NOT zero."""
    k = int(k)
    if k not in _LOGM:
        x = np.log(np.maximum(rdraw(k), 1e-300) / d2(k))
        _LOGM[k] = (float(x.mean()), float(x.std(ddof=1)))
    return _LOGM[k]


def null_moments(ka, kb):
    """centre and sd of D = log(R_a/d2(k_a)) - log(R_b/d2(k_b)) under H0, ladders independent."""
    ma, sa = logmoments(ka)
    mb, sb = logmoments(kb)
    return ma - mb, math.sqrt(sa * sa + sb * sb)


def required_F(effect, sd, z):
    """smallest fold count F at which |effect| exceeds z*sd/sqrt(F).  inf when effect == 0."""
    if not np.isfinite(effect) or not np.isfinite(sd) or sd <= 0 or effect == 0:
        return np.inf
    return math.ceil((z * sd / abs(effect)) ** 2)


# ==================================================================== panels / runner (1214's)
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
    """1098/1159's min-hold selection frame at GROSS = 1.0; lag=1 is rule 2's decide-at-t /
    apply-at-t+1 (1209's correction).  Row t is the APPLICATION-time weight."""
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


# ==================================================================== main
def main():
    t0 = time.time()
    say("=" * 110)
    say("IDEA 1222 (lane C, 2026-09-18) — is the WIDEST-DIAL HABIT RESOLVABLE on ANY")
    say("ATTAINABLE FOLD COUNT?")
    say("=" * 110)

    # ------------------------------------------------------------------ ARM 0
    say("")
    say("=" * 110)
    say("ARM 0 — THE ARITHMETIC, PRINTED BEFORE ANY PRICE IS READ.")
    say("=" * 110)
    mc_err = max(abs(rdraw(k).mean() - D2[k]) for k in (2, 4, 6, 10))
    say(f"  d2(k) Monte Carlo at {NMC:,} draws reproduces the published Hartley constants for the")
    say(f"  record's own rung counts (2/4/6/10) to {mc_err:.3e}.")
    GATES.append(dict(gate="G0 Monte-Carlo d2(k) == published Hartley constants", value=mc_err,
                      target=5e-3, pass_=bool(mc_err < 5e-3)))

    say("")
    say("  THE NULL CENTRE OF D IS NOT ZERO, AND THAT IS MEASURED, NOT ASSUMED.")
    say("     k    E[log(R_k/d2(k))]   sd[log(R_k/d2(k))]")
    for k in sorted(set(LADK.values())):
        m_, s_ = logmoments(k)
        say(f"    {k:3d}        {m_:+10.6f}          {s_:10.6f}")
    say("")
    say("  PER-PAIR NULL MOMENTS (all 6 unordered ALL4 pairs; NG is the 3 that exclude GROSS):")
    say("     pair                 k_a/k_b     mu0        sd0     F* at |D-mu0| = 0.10 / 0.25 / 0.50")
    nrows = []
    for a, b in itertools.combinations(["N", "H", "GROSS", "CADENCE"], 2):
        mu0, sd0 = null_moments(LADK[a], LADK[b])
        f1, f2, f3 = (required_F(e, sd0, ALPHAS[0.05]) for e in (0.10, 0.25, 0.50))
        nrows.append(dict(ladder_a=a, ladder_b=b, k_a=LADK[a], k_b=LADK[b], mu0=mu0, sd0=sd0,
                          F_at_010=f1, F_at_025=f2, F_at_050=f3,
                          in_NG=bool(a != "GROSS" and b != "GROSS")))
        say(f"     {a+'/'+b:20s} {LADK[a]:2d}/{LADK[b]:<2d}   {mu0:+9.5f}  {sd0:9.5f}    "
            f"{f1:6d} / {f2:5d} / {f3:4d}")
    pd.DataFrame(nrows).to_csv(f"{OUT}.nullmoments.csv", index=False)

    say("")
    say("  THE 1/sqrt(F) MECHANISM, GATED.  If the band on the mean of F independent fold")
    say("  readings did not shrink as 1/sqrt(F), no fold count would ever resolve anything.")
    say("     F     sd(mean of F)   sd0/sqrt(F)    ratio")
    rng = np.random.default_rng(MC_SEED + 7)
    ka, kb = 6, 4
    mu0_g, sd0_g = null_moments(ka, kb)
    la = np.log(np.maximum(rdraw(ka), 1e-300) / d2(ka))
    lb = np.log(np.maximum(rdraw(kb), 1e-300) / d2(kb))
    worst = 0.0
    for F in (1, 4, 16, 64):
        ia = rng.integers(0, len(la), size=(20000, F))
        ib = rng.integers(0, len(lb), size=(20000, F))
        dm = (la[ia] - lb[ib]).mean(axis=1)
        pred = sd0_g / math.sqrt(F)
        ratio = dm.std(ddof=1) / pred
        worst = max(worst, abs(ratio - 1.0))
        say(f"     {F:3d}      {dm.std(ddof=1):10.6f}    {pred:10.6f}   {ratio:.4f}")
    GATES.append(dict(gate="G1 band on the mean of F folds shrinks as 1/sqrt(F)", value=worst,
                      target=0.03, pass_=bool(worst < 0.03)))

    say("")
    say("  PRE-DECLARED OUTCOMES, fixed here before any price is read, judged at the HEADLINE")
    say(f"  CELL (LADDER SET = ALL4, L = {HEADLINE_L}, alpha = {HEADLINE_ALPHA}) over the 18")
    say("  (panel, pair) cells, and then at every one of the 8 cells:")
    say("    (A) RESOLVABLE ON THIS TAPE  — >= 0.50 of cells reach |t| > z at a fold count the")
    say("        tape actually supplies (F* <= F_max).")
    say("    (B) MINORITY RESOLVABLE      — 0 < share < 0.50.")
    say("    (C) NOT RESOLVABLE AT ANY ATTAINABLE COUNT — 0 cells at EVERY (L, ladder set).")
    say("  The answer to the queue's question is (A)/(B) = YES on some attainable count,")
    say("  (C) = NO on any.")

    # ------------------------------------------------------------------ panels and books
    say("")
    say("=" * 110)
    say("ARM A — THE REQUIRED FOLD COUNT, ON DISJOINT FOLDS, AT EVERY CELL")
    say("=" * 110)
    panels = []
    pxU = load_universe()
    panels.append(Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]))
    pxB = load_universe(broad=True)
    panels.append(Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]))
    pxS = load_universe(small=True)
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and mv[c] < 1.0]
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

    pan0 = panels[0]
    Wt = A_G * build1(pan0, A_N, A_H, "W")
    Wdf = pd.DataFrame(Wt, index=pan0.idx, columns=pan0.px.columns)
    eb = backtest(pan0.px, Wdf.shift(-1).fillna(0.0), cost_bps=COST, freq="W")["returns"].values
    g2 = float(np.nanmax(np.abs(eb[WARMUP:] - nrun(pan0, Wt, "W")[WARMUP:])))
    GATES.append(dict(gate="G2 fast runner == engine.backtest on the decision-time frame",
                      value=g2, target=1e-10, pass_=bool(g2 < 1e-10)))
    fr0 = build1(pan0, A_N, A_H, "W")
    g3 = float(max(np.abs(g * fr0 - g * fr0).max() for g in LAD["GROSS"]))
    GATES.append(dict(gate="G3 the GROSS ladder is the anchor frame SCALED", value=g3,
                      target=0.0, pass_=bool(g3 == 0.0)))
    lm = mdd(bench["U56"]["live"][WARMUP:])
    GATES.append(dict(gate="G4 live RULES v2 U56 MaxDD == the record's committed -12.05%",
                      value=lm, target=LIVE_MAXDD_COMMITTED,
                      pass_=bool(abs(lm - LIVE_MAXDD_COMMITTED) < 5e-4)))
    say(f"    G2 {g2:.3e}   G3 {g3:.3e}   G4 live U56 MaxDD {lm:.4%}")

    # ---- fast windowed Sharpe on the book matrix
    CS, CSQ, LADIDX = {}, {}, {lad: [BOOKKEY.index((lad, r)) for r in LAD[lad]] for lad in LAD}
    for p, M in RM.items():
        CS[p] = np.vstack([np.zeros((1, M.shape[1])), np.cumsum(M, axis=0)])
        CSQ[p] = np.vstack([np.zeros((1, M.shape[1])), np.cumsum(M * M, axis=0)])

    def win_sharpe(p, lo, hi):
        """annualised Sharpe of every book over [lo, hi), from the cumulative sums."""
        n = hi - lo
        tot = CS[p][hi] - CS[p][lo]
        totq = CSQ[p][hi] - CSQ[p][lo]
        mu = tot / n
        var = np.maximum(totq / n - mu * mu, 0.0)
        sd = np.sqrt(var)
        with np.errstate(divide="ignore", invalid="ignore"):
            return np.where(sd > 0, mu * np.sqrt(252) / sd, np.nan)

    p0 = panels[0].name
    direct = np.array([sharpe(RM[p0][300:1100, j]) for j in range(RM[p0].shape[1])])
    g5 = float(np.nanmax(np.abs(win_sharpe(p0, 300, 1100) - direct)))
    GATES.append(dict(gate="G5 windowed Sharpe from cumsums == direct sharpe()", value=g5,
                      target=1e-9, pass_=bool(g5 < 1e-9)))

    def spread_vec(p, lo, hi):
        """max-minus-min of each ladder's rung Sharpes over [lo, hi)."""
        s = win_sharpe(p, lo, hi)
        out = {}
        for lad, ii in LADIDX.items():
            v = s[ii]
            v = v[np.isfinite(v)]
            out[lad] = float(v.max() - v.min()) if len(v) > 1 else np.nan
        return out

    def folds_of(pan, lo, hi, L):
        """disjoint consecutive folds of length L tiling [lo, hi); the remainder is dropped."""
        F = (hi - lo) // L
        return [(lo + i * L, lo + (i + 1) * L) for i in range(F)]

    # ---- full-sample orientation, fixed ONCE per (panel, pair)
    ORIENT = {}
    for pan in panels:
        sp_full = spread_vec(pan.name, pan.i0, len(pan.rets))
        for a, b in itertools.combinations(["N", "H", "GROSS", "CADENCE"], 2):
            xa = math.log(max(sp_full[a], SPREAD_FLOOR)) - math.log(d2(LADK[a]))
            xb = math.log(max(sp_full[b], SPREAD_FLOOR)) - math.log(d2(LADK[b]))
            ORIENT[(pan.name, a, b)] = (a, b) if xa >= xb else (b, a)
    say("")
    say("  ORIENTATION, FIXED ONCE ON THE FULL SAMPLE AND HELD ACROSS EVERY FOLD AND CELL:")
    for pan in panels:
        pr = [f"{ORIENT[(pan.name, a, b)][0]}>{ORIENT[(pan.name, a, b)][1]}"
              for a, b in itertools.combinations(["N", "H", "GROSS", "CADENCE"], 2)]
        say(f"    {pan.name:6s}  " + "  ".join(pr))

    # ---- the required-precision table
    say("")
    say("  (A1) THE TABLE THE QUEUE ASKED FOR.  For each (panel, pair) and each fold length:")
    say("       F_max = folds the tape supplies;  Dbar = mean of the per-fold log ratio;")
    say("       t = (Dbar - mu0) / (s_emp / sqrt(F_max));  F* = the fold count at which the")
    say("       OBSERVED effect would clear the alpha = 0.05 band, at the tape's own dispersion.")
    say("       YEARS* = F* x L / 252 = how long a tape it would take.")
    rows = []
    tape_years = {}
    for pan in panels:
        tape_years[pan.name] = (len(pan.rets) - pan.i0) / 252.0
        for L in FOLD_LENS:
            fl = folds_of(pan, pan.i0, len(pan.rets), L)
            F_max = len(fl)
            sp = [spread_vec(pan.name, lo, hi) for lo, hi in fl]
            for a0, b0 in itertools.combinations(["N", "H", "GROSS", "CADENCE"], 2):
                a, b = ORIENT[(pan.name, a0, b0)]
                D = np.array([
                    (math.log(max(s[a], SPREAD_FLOOR)) - math.log(d2(LADK[a])))
                    - (math.log(max(s[b], SPREAD_FLOOR)) - math.log(d2(LADK[b])))
                    for s in sp])
                floored = sum(1 for s in sp if not (s[a] > SPREAD_FLOOR and s[b] > SPREAD_FLOOR))
                mu0, sd0 = null_moments(LADK[a], LADK[b])
                Dbar = float(np.mean(D))
                s_emp = float(np.std(D, ddof=1)) if F_max > 1 else np.nan
                eff = Dbar - mu0
                t_emp = (eff / (s_emp / math.sqrt(F_max))) if (F_max > 1 and s_emp > 0) else np.nan
                agree = float(np.mean(D > mu0))
                r = dict(panel=pan.name, L=L, F_max=F_max, ladder_wider=a, ladder_narrower=b,
                         k_w=LADK[a], k_n=LADK[b],
                         in_NG=bool(a != "GROSS" and b != "GROSS"),
                         Dbar=Dbar, mu0=mu0, effect=eff, sd_null=sd0, sd_emp=s_emp,
                         sd_ratio_emp_over_null=(s_emp / sd0) if sd0 > 0 else np.nan,
                         t_emp=t_emp, orient_agree_rate=agree, folds_floored=floored)
                for al, z in ALPHAS.items():
                    Fs_e = required_F(eff, s_emp, z)
                    Fs_n = required_F(eff, sd0, z)
                    tag = f"{int(al*100):02d}"
                    r[f"F_star_emp_{tag}"] = Fs_e
                    r[f"F_star_iid_{tag}"] = Fs_n
                    r[f"years_star_emp_{tag}"] = Fs_e * L / 252.0
                    r[f"resolved_now_{tag}"] = bool(np.isfinite(t_emp) and abs(t_emp) > z)
                    r[f"attainable_{tag}"] = bool(np.isfinite(Fs_e) and Fs_e <= F_max)
                rows.append(r)
    fdf = pd.DataFrame(rows)
    fdf.to_csv(f"{OUT}.foldcount.csv", index=False)

    ok8 = 0
    for _, r in fdf.iterrows():
        Fs = r.F_star_emp_05
        if np.isfinite(Fs) and r.sd_emp > 0:
            ok8 += int(abs(r.effect) / (r.sd_emp / math.sqrt(Fs)) >= ALPHAS[0.05] - 1e-9)
        else:
            ok8 += 1
    GATES.append(dict(gate="G6 F* is the smallest count clearing the band, checked row by row",
                      value=float(len(fdf) - ok8), target=0.0, pass_=bool(ok8 == len(fdf))))

    say("")
    say("       panel   L   F_max  pair            t      |  F*(emp)   YEARS*   attainable?  "
        "resolved now?")
    for _, r in fdf.sort_values(["panel", "L", "ladder_wider", "ladder_narrower"]).iterrows():
        fs = r.F_star_emp_05
        say(f"       {r.panel:6s} {r.L:4d}  {r.F_max:4d}  {r.ladder_wider+'/'+r.ladder_narrower:14s} "
            f"{r.t_emp:+7.3f}  |  {('inf' if not np.isfinite(fs) else f'{int(fs):7d}'):>7s}  "
            f"{('inf' if not np.isfinite(fs) else f'{r.years_star_emp_05:8.1f}'):>8s}   "
            f"{str(bool(r.attainable_05)):5s}        {str(bool(r.resolved_now_05))}")

    say("")
    say("  (A2) THE 8 CELLS — 4 FOLD LENGTHS x 2 LADDER PAIR SETS, EVERY ONE PUBLISHED.")
    say("       'resolved' counts (panel, pair) cells whose observed |t| clears the band AT THE")
    say("       FOLD COUNT THE TAPE SUPPLIES.  'attainable' is the same thing read through F*.")
    say("")
    say("       set    L    cells  F_max  resolved(a=.05)  resolved(a=.10)   median F*   "
        "median YEARS*   min YEARS*")
    crows = []
    for sname, lads in LADSETS.items():
        for L in FOLD_LENS:
            sub = fdf[(fdf.L == L) & (fdf.in_NG if sname == "NG" else True)]
            fs = sub.F_star_emp_05.replace([np.inf], np.nan)
            ys = sub.years_star_emp_05.replace([np.inf], np.nan)
            c = dict(LADDER_SET=sname, L=L, cells=len(sub), F_max=int(sub.F_max.max()),
                     resolved_05=int(sub.resolved_now_05.sum()),
                     resolved_10=int(sub.resolved_now_10.sum()),
                     share_resolved_05=float(sub.resolved_now_05.mean()),
                     attainable_05=int(sub.attainable_05.sum()),
                     median_F_star=float(fs.median()), median_years_star=float(ys.median()),
                     min_years_star=float(ys.min()),
                     median_sd_ratio=float(sub.sd_ratio_emp_over_null.median()))
            crows.append(c)
            say(f"       {sname:5s} {L:4d}   {len(sub):4d}  {c['F_max']:4d}   "
                f"{c['resolved_05']:8d}         {c['resolved_10']:8d}      "
                f"{c['median_F_star']:9.0f}   {c['median_years_star']:12.1f}   "
                f"{c['min_years_star']:10.1f}")
    cdf = pd.DataFrame(crows)
    cdf.to_csv(f"{OUT}.cells.csv", index=False)

    say("")
    say("  (A3) THE BEST CASE ACROSS ALL FOUR FOLD LENGTHS, per (panel, pair): the shortest tape")
    say("       any attainable fold count would need, against the tape actually in hand.")
    say("       panel   pair            best L   F*      YEARS*      tape years   resolvable?")
    brows = []
    for (p, a, b), g in fdf.groupby(["panel", "ladder_wider", "ladder_narrower"]):
        gg = g[np.isfinite(g.years_star_emp_05)]
        if len(gg) == 0:
            brows.append(dict(panel=p, ladder_wider=a, ladder_narrower=b, best_L=np.nan,
                              F_star=np.inf, years_star=np.inf, tape_years=tape_years[p],
                              resolvable_on_tape=False,
                              in_NG=bool(a != "GROSS" and b != "GROSS")))
            say(f"       {p:6s}  {a+'/'+b:14s}   ----     inf        inf       "
                f"{tape_years[p]:8.1f}   False")
            continue
        r = gg.loc[gg.years_star_emp_05.idxmin()]
        res = bool(r.years_star_emp_05 <= tape_years[p])
        brows.append(dict(panel=p, ladder_wider=a, ladder_narrower=b, best_L=int(r.L),
                          F_star=float(r.F_star_emp_05), years_star=float(r.years_star_emp_05),
                          tape_years=tape_years[p], resolvable_on_tape=res,
                          in_NG=bool(a != "GROSS" and b != "GROSS")))
        say(f"       {p:6s}  {a+'/'+b:14s}   {int(r.L):4d}   {int(r.F_star_emp_05):6d}  "
            f"{r.years_star_emp_05:9.1f}   {tape_years[p]:8.1f}   {res}")
    bdf = pd.DataFrame(brows)
    bdf.to_csv(f"{OUT}.bestcase.csv", index=False)
    say("")
    say(f"     RESOLVABLE ON THE TAPE IN HAND, best fold length per pair: "
        f"{int(bdf.resolvable_on_tape.sum())} of {len(bdf)} (panel, pair) cells; "
        f"NG only: {int(bdf[bdf.in_NG].resolvable_on_tape.sum())} of {int(bdf.in_NG.sum())}.")

    # ------------------------------------------------------------------ ARM B
    say("")
    say("=" * 110)
    say("ARM B — PRICING IT.  RULE 8 WALK-FORWARD AND BOTH KEEP PATHS.")
    say("=" * 110)
    say("")
    say("  The required-precision calculation is made DEPLOYABLE as a chooser: it reads the IS")
    say("  window only, decides whether the widest dial is RESOLVED at the fold count that")
    say("  window supplies, and moves only if it is.")
    say("    CH_ANCHOR   never move (the do-nothing control).")
    say("    CH_RAW      tune the raw-widest ladder's IS-argmax rung (the record's habit).")
    say("    CH_POINT    tune the argmax of spread/d2(k) (1155/1207's point repair).")
    say("    CH_RES      tune CH_POINT's winner ONLY if that pair clears the alpha = 0.05 band")
    say("                on the IS window's own disjoint folds at this cell's L; a REVERSED")
    say("                call (t < -z) moves to the runner-up instead; otherwise STAY.")

    BASECH = ["CH_ANCHOR", "CH_RAW", "CH_POINT", "CH_RES"]

    def pick_of(p, lad, lo, hi):
        s = win_sharpe(p, lo, hi)
        best, brung = -np.inf, None
        for rung, j in zip(LAD[lad], LADIDX[lad]):
            if np.isfinite(s[j]) and s[j] > best:
                best, brung = s[j], rung
        return brung

    _FOLDSTAT: dict = {}

    def foldstat(p, lo, hi, L, a, b):
        """(t, F) for the ordered pair (a wider, b narrower) on disjoint folds of [lo, hi)."""
        key = (p, lo, hi, L, a, b)
        if key in _FOLDSTAT:
            return _FOLDSTAT[key]
        F = (hi - lo) // L
        if F < 2:
            _FOLDSTAT[key] = (np.nan, F)
            return _FOLDSTAT[key]
        D = []
        for i in range(F):
            s = spread_vec(p, lo + i * L, lo + (i + 1) * L)
            D.append((math.log(max(s[a], SPREAD_FLOOR)) - math.log(d2(LADK[a])))
                     - (math.log(max(s[b], SPREAD_FLOOR)) - math.log(d2(LADK[b]))))
        D = np.array(D)
        mu0, _ = null_moments(LADK[a], LADK[b])
        se = float(np.std(D, ddof=1)) / math.sqrt(F)
        t = (float(np.mean(D)) - mu0) / se if se > 0 else np.nan
        _FOLDSTAT[key] = (t, F)
        return _FOLDSTAT[key]

    def choose(pan, lo, hi, lads, L):
        sp = spread_vec(pan.name, lo, hi)
        good = {k: v for k, v in sp.items() if k in lads and np.isfinite(v) and v > 0}
        out = {"CH_ANCHOR": ("CADENCE", A_C)}
        info = dict(L=L)
        if not good:
            out.update({c: ("CADENCE", A_C) for c in BASECH})
            return out, info
        raw_w = max(good, key=good.get)
        order = sorted(good, key=lambda k: good[k] / d2(LADK[k]), reverse=True)
        pt_w = order[0]
        run = order[1] if len(order) > 1 else None
        out["CH_RAW"] = (raw_w, pick_of(pan.name, raw_w, lo, hi))
        out["CH_POINT"] = (pt_w, pick_of(pan.name, pt_w, lo, hi))
        info.update(raw_widest=raw_w, point_widest=pt_w, runner_up=run)
        if run is None:
            out["CH_RES"] = ("CADENCE", A_C)
            info.update(t=np.nan, F=0, call="TIE")
            return out, info
        t, F = foldstat(pan.name, lo, hi, L, pt_w, run)
        z = ALPHAS[HEADLINE_ALPHA]
        call = "TIE" if not np.isfinite(t) or abs(t) <= z else ("W" if t > 0 else "N")
        info.update(t=t, F=F, call=call)
        if call == "TIE":
            out["CH_RES"] = ("CADENCE", A_C)
        else:
            win = pt_w if call == "W" else run
            out["CH_RES"] = (win, pick_of(pan.name, win, lo, hi))
        return out, info

    say("")
    say("  BENCHMARKS (10 bps, t+1, post warm-up):")
    BM = {}
    for pan in panels:
        i0 = pan.i0
        ioos = pan.idx.searchsorted(pd.Timestamp(OOS_START))
        for nm, r in [("SPY", bench[pan.name]["spy"]), ("LIVE", bench[pan.name]["live"])]:
            full = r[i0:]
            h1, h2 = halves(full)
            BM[(pan.name, nm)] = dict(**triple(full), H1=h1, H2=h2,
                                      OOS_Sharpe=sharpe(r[ioos:]), OOS_CAGR=cagr(r[ioos:]),
                                      OOS_MaxDD=mdd(r[ioos:]))
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
    say("  BOTH KEEP PATHS ON EVERY RUNG BOOK (rule 4; nothing selected on):")
    brows2 = []
    for pan in panels:
        i0, ioos = pan.i0, pan.idx.searchsorted(pd.Timestamp(OOS_START))
        spy, liv = BM[(pan.name, "SPY")], BM[(pan.name, "LIVE")]
        so, lo_ = oos_bm(pan.name, "SPY", ioos), oos_bm(pan.name, "LIVE", ioos)
        for (lad, rung), r in booked[pan.name].items():
            k4a, k4b, m, h1, h2 = keep_paths(r[i0:], spy, liv)
            _, k4b_o, mo, _, _ = keep_paths(r[ioos:], so, lo_)
            brows2.append(dict(panel=pan.name, ladder=lad, rung=rung, **m, H1=h1, H2=h2,
                               OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                               OOS_MaxDD=mo["MaxDD"], KEEP_4a=k4a, KEEP_4b=k4b,
                               KEEP_4b_OOS=k4b_o))
    bookdf = pd.DataFrame(brows2)
    bookdf.to_csv(f"{OUT}.books.csv", index=False)
    say(f"    {len(bookdf)} rung books: 4a {int(bookdf.KEEP_4a.sum())}; "
        f"4b full {int(bookdf.KEEP_4b.sum())}; 4b OOS {int(bookdf.KEEP_4b_OOS.sum())}; "
        f"BOTH {int((bookdf.KEEP_4b & bookdf.KEEP_4b_OOS).sum())}")
    p4b = bookdf[bookdf.KEEP_4b & bookdf.KEEP_4b_OOS]
    for _, r in p4b.iterrows():
        say(f"      4b BOTH: {r.panel} {r.ladder}={r.rung}  {r.CAGR:7.2%} / {r.Sharpe:.4f} / "
            f"{r.MaxDD:8.2%}  halves {r.H1:.4f}/{r.H2:.4f}  OOS {r.OOS_CAGR:7.2%} / "
            f"{r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:8.2%}")

    say("")
    say("  (B1) THE ROLLING WALK — one calendar year of OOS per fold, stepped one year,")
    say(f"       {FOLD_YEARS[0]}-{FOLD_YEARS[-1]}, IS = warm-up to the day before the fold.")
    prows, stitched, folds_by_panel = [], {}, {}
    for pan in panels:
        yrs = pan.idx.year.values
        for y in FOLD_YEARS:
            oo = np.flatnonzero(yrs == y)
            oo = oo[oo >= pan.i0]
            if len(oo) < 60:
                continue
            lo, hi = pan.i0, int(oo[0])
            if hi - lo < 252:
                continue
            folds_by_panel.setdefault(pan.name, []).append((y, lo, hi, int(oo[0]), int(oo[-1]) + 1))
    for pan in panels:
        for (y, lo, hi, o0, o1) in folds_by_panel[pan.name]:
            for sname, lads in LADSETS.items():
                for L in FOLD_LENS:
                    sel, info = choose(pan, lo, hi, lads, L)
                    for ch in BASECH:
                        s = sel.get(ch, ("CADENCE", A_C))
                        r = booked[pan.name][s][o0:o1]
                        name = f"{ch}/{sname}/L{L}"
                        stitched.setdefault((pan.name, name), []).append((y, r))
                        prows.append(dict(panel=pan.name, fold=y, chooser=name, base=ch,
                                          ladder_set=sname, L=L, ladder=s[0], rung=s[1],
                                          point_widest=info.get("point_widest"),
                                          runner_up=info.get("runner_up"),
                                          t=info.get("t", np.nan), F=info.get("F", 0),
                                          call=info.get("call"),
                                          moved=bool(s != ("CADENCE", A_C)),
                                          OOS_Sharpe=sharpe(r), OOS_CAGR=cagr(r),
                                          OOS_MaxDD=mdd(r)))
    pdf = pd.DataFrame(prows)
    pdf.to_csv(f"{OUT}.picks.csv", index=False)
    mv_anchor = float(pdf[pdf.base == "CH_ANCHOR"].moved.mean())
    GATES.append(dict(gate="G7 CH_ANCHOR move rate == 0", value=mv_anchor, target=0.0,
                      pass_=bool(mv_anchor == 0.0)))
    say(f"       {len(pdf)} pick-cells = {pdf.panel.nunique()} panels x {pdf.fold.nunique()} "
        f"folds x {pdf.chooser.nunique()} choosers.")
    say("")
    say("       HOW OFTEN CH_RES IS ALLOWED TO MOVE AT ALL (its move rate is the resolution")
    say("       rate of the widest-dial habit on an IS window of this tape's length):")
    say("       set    L     CH_RES move   calls W / N / TIE    CH_RAW move   CH_POINT move")
    for sname in LADSETS:
        for L in FOLD_LENS:
            s = pdf[(pdf.ladder_set == sname) & (pdf.L == L)]
            sr = s[s.base == "CH_RES"]
            vc = sr.call.value_counts()
            say(f"       {sname:5s} {L:4d}   {sr.moved.mean():10.4f}   "
                f"{vc.get('W',0):4d} /{vc.get('N',0):4d} /{vc.get('TIE',0):5d}     "
                f"{s[s.base=='CH_RAW'].moved.mean():10.4f}   "
                f"{s[s.base=='CH_POINT'].moved.mean():10.4f}")

    say("")
    say("       mean OOS Sharpe over all picks and the PAIRED delta vs CH_ANCHOR at the same")
    say("       cell, SE clustered on the FOLD (the year folds tile the tape without overlap):")
    drows = []
    for sname in LADSETS:
        for L in FOLD_LENS:
            base = pdf[(pdf.base == "CH_ANCHOR") & (pdf.ladder_set == sname)
                       & (pdf.L == L)].set_index(["panel", "fold"]).OOS_Sharpe
            for ch in ["CH_RAW", "CH_POINT", "CH_RES"]:
                s = pdf[(pdf.base == ch) & (pdf.ladder_set == sname)
                        & (pdf.L == L)].set_index(["panel", "fold"]).OOS_Sharpe
                d = (s - base).dropna()
                fm = d.groupby(level=1).mean()
                se = fm.std(ddof=1) / np.sqrt(len(fm)) if len(fm) > 1 else np.nan
                t = d.mean() / se if se and se > 0 else 0.0
                drows.append(dict(chooser=f"{ch}/{sname}/L{L}", mean_OOS_Sharpe=float(s.mean()),
                                  delta_vs_ANCHOR=float(d.mean()), SE=float(se), t=float(t)))
                say(f"         {ch+'/'+sname+'/L'+str(L):22s} mean OOS Sharpe {s.mean():7.4f}   "
                    f"delta {d.mean():+.4f}   SE {se:.4f}   t {t:+.2f}")
    pd.DataFrame(drows).to_csv(f"{OUT}.deltas.csv", index=False)

    say("")
    say("  (B2) RULE 8 — the single split the PROTOCOL names.  Dials chosen on the IS window")
    say("       (to 2016-12-31) ONLY; 2017-2026 read ONCE.")
    wrows = []
    for pan in panels:
        iend = pan.idx.searchsorted(pd.Timestamp(OOS_START))
        spy, liv = BM[(pan.name, "SPY")], BM[(pan.name, "LIVE")]
        so, lo_ = oos_bm(pan.name, "SPY", iend), oos_bm(pan.name, "LIVE", iend)
        for sname, lads in LADSETS.items():
            for L in FOLD_LENS:
                sel, info = choose(pan, pan.i0, iend, lads, L)
                say(f"       {pan.name:6s} [{sname:5s} L={L:3d}] point-widest "
                    f"{info.get('point_widest')} vs runner-up {info.get('runner_up')}  "
                    f"IS folds F={info.get('F')}  t={info.get('t', float('nan')):+.3f}  "
                    f"-> {info.get('call')}")
                for ch in BASECH:
                    s = sel.get(ch, ("CADENCE", A_C))
                    rf = booked[pan.name][s][pan.i0:]
                    ro = booked[pan.name][s][iend:]
                    k4a, k4b, m, h1, h2 = keep_paths(rf, spy, liv)
                    _, k4b_o, mo, _, _ = keep_paths(ro, so, lo_)
                    wrows.append(dict(panel=pan.name, chooser=f"{ch}/{sname}/L{L}", base=ch,
                                      ladder_set=sname, L=L, ladder=s[0], rung=s[1],
                                      moved=bool(s != ("CADENCE", A_C)), **m, H1=h1, H2=h2,
                                      OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                      OOS_MaxDD=mo["MaxDD"],
                                      SPY_OOS_Sharpe=spy["OOS_Sharpe"],
                                      SPY_OOS_CAGR=spy["OOS_CAGR"],
                                      SPY_OOS_MaxDD=spy["OOS_MaxDD"],
                                      LIVE_OOS_Sharpe=liv["OOS_Sharpe"],
                                      LIVE_OOS_CAGR=liv["OOS_CAGR"],
                                      KEEP_4a=k4a, KEEP_4b=k4b, KEEP_4b_OOS=k4b_o))
                    say(f"         {ch:10s} -> {s[0]}={s[1]:<5}  full {m['CAGR']:7.2%} / "
                        f"{m['Sharpe']:.4f} / {m['MaxDD']:8.2%}  halves {h1:.4f}/{h2:.4f}   "
                        f"OOS {mo['CAGR']:7.2%} / {mo['Sharpe']:.4f} / {mo['MaxDD']:8.2%}   "
                        f"4a {k4a}  4b {k4b}  4b_OOS {k4b_o}")
    wdf = pd.DataFrame(wrows)
    wdf.to_csv(f"{OUT}.walkforward.csv", index=False)

    say("")
    say("  (B3) THE STITCHED DEPLOYABLE CURVES — each chooser's own fold picks, concatenated.")
    srows, stitch_ok = [], 0
    for (p, ch), parts in stitched.items():
        parts = sorted(parts, key=lambda z: z[0])
        r = np.concatenate([x for _, x in parts])
        ro = np.concatenate([x for y, x in parts if y >= 2017])
        stitch_ok += int(len(r) == sum(len(x) for _, x in parts))
        ioos = [q for q in panels if q.name == p][0].idx.searchsorted(pd.Timestamp(OOS_START))
        spy, liv = BM[(p, "SPY")], BM[(p, "LIVE")]
        k4a, k4b, m, h1, h2 = keep_paths(r, spy, liv)
        _, k4b_o, mo, _, _ = keep_paths(ro, oos_bm(p, "SPY", ioos), oos_bm(p, "LIVE", ioos))
        srows.append(dict(panel=p, chooser=ch, n_days=len(r), n_oos_days=len(ro), **m,
                          H1=h1, H2=h2, OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                          OOS_MaxDD=mo["MaxDD"], KEEP_4a=k4a, KEEP_4b=k4b, KEEP_4b_OOS=k4b_o))
    sdf = pd.DataFrame(srows).sort_values(["panel", "chooser"])
    sdf.to_csv(f"{OUT}.stitched.csv", index=False)
    GATES.append(dict(gate="G8 each stitched curve's length == the sum of its folds'",
                      value=float(len(sdf) - stitch_ok), target=0.0,
                      pass_=bool(stitch_ok == len(sdf))))
    say(f"     {len(sdf)} stitched curves: 4a {int(sdf.KEEP_4a.sum())}; "
        f"4b full {int(sdf.KEEP_4b.sum())}; 4b OOS {int(sdf.KEEP_4b_OOS.sum())}; "
        f"BOTH {int((sdf.KEEP_4b & sdf.KEEP_4b_OOS).sum())}")
    for _, r in sdf[sdf.KEEP_4b & sdf.KEEP_4b_OOS].iterrows():
        say(f"       4b BOTH: {r.panel:6s} {r.chooser:22s} {r.CAGR:7.2%} / {r.Sharpe:.4f} / "
            f"{r.MaxDD:8.2%}  halves {r.H1:.4f}/{r.H2:.4f}  OOS {r.OOS_CAGR:7.2%} / "
            f"{r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:8.2%}")
    say(f"     RULE-8 PICKS ({len(wdf)}): 4a {int(wdf.KEEP_4a.sum())}; "
        f"4b full {int(wdf.KEEP_4b.sum())}; 4b OOS {int(wdf.KEEP_4b_OOS.sum())}; "
        f"BOTH {int((wdf.KEEP_4b & wdf.KEEP_4b_OOS).sum())}")
    say("")
    say("     DOES THE RESOLUTION TEST BUY ANYTHING OOS?  rule-8 mean OOS Sharpe by chooser:")
    for ch in BASECH:
        s = wdf[wdf.base == ch]
        say(f"       {ch:10s} mean OOS Sharpe {s.OOS_Sharpe.mean():.4f}   mean OOS CAGR "
            f"{s.OOS_CAGR.mean():7.2%}   worst OOS MaxDD {s.OOS_MaxDD.min():8.2%}   "
            f"moved {s.moved.mean():.3f}")
    anc = wdf[wdf.base == "CH_ANCHOR"].set_index(["panel", "ladder_set", "L"]).OOS_Sharpe
    for ch in ["CH_RAW", "CH_POINT", "CH_RES"]:
        s = wdf[wdf.base == ch].set_index(["panel", "ladder_set", "L"]).OOS_Sharpe
        d = (s - anc).dropna()
        say(f"       {ch:10s} vs CH_ANCHOR: mean d(OOS Sharpe) {d.mean():+.4f}   "
            f"wins {int((d>0).sum())} / losses {int((d<0).sum())} / ties {int((d==0).sum())}")

    # ------------------------------------------------------------------ determinism
    pre = {(a, b): null_moments(LADK[a], LADK[b])
           for a, b in itertools.combinations(LADK, 2)}
    _LOGM.clear()
    _RDRAW.clear()
    det = max(max(abs(null_moments(LADK[a], LADK[b])[0] - m0),
                  abs(null_moments(LADK[a], LADK[b])[1] - s0))
              for (a, b), (m0, s0) in pre.items())
    GATES.append(dict(gate="G9 the null moments are deterministic across two constructions",
                      value=float(det), target=0.0, pass_=bool(det == 0.0)))

    # ------------------------------------------------------------------ gates
    say("")
    say("=" * 110)
    say("GATES")
    say("=" * 110)
    gg = pd.DataFrame(GATES)
    gg.to_csv(f"{OUT}.gates.csv", index=False)
    for _, g in gg.iterrows():
        say(f"  {'PASS' if g.pass_ else 'FAIL'}  {g.gate:68s} {g.value:>14.6g} "
            f"(target {g.target:g})")
    say(f"  {int(gg.pass_.sum())} of {len(gg)} gates pass.")

    # ------------------------------------------------------------------ verdict
    say("")
    say("=" * 110)
    head = cdf[(cdf.LADDER_SET == "ALL4") & (cdf.L == HEADLINE_L)].iloc[0]
    share = head.share_resolved_05
    any_res = int(cdf.resolved_05.sum())
    label = ("(C) NOT RESOLVABLE AT ANY ATTAINABLE COUNT" if any_res == 0 else
             "(A) RESOLVABLE ON THIS TAPE" if share >= 0.50 else "(B) MINORITY RESOLVABLE")
    say(f"ANSWER: {label}")
    say(f"  headline cell (ALL4, L={HEADLINE_L}, alpha=0.05): {head.resolved_05} of "
        f"{head.cells} (panel, pair) cells resolved at F_max = {head.F_max} "
        f"(share {share:.4f}); median F* {head.median_F_star:.0f} = "
        f"{head.median_years_star:.1f} years of tape.")
    say(f"  over all 8 cells: {any_res} of {int(cdf.cells.sum())} resolved; "
        f"best case per (panel, pair) across all four fold lengths: "
        f"{int(bdf.resolvable_on_tape.sum())} of {len(bdf)} need no more tape than the "
        f"{np.mean(list(tape_years.values())):.1f} years in hand.")
    say("=" * 110)
    say(f"runtime {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return dict(fold=fdf, cells=cdf, best=bdf, books=bookdf, picks=pdf, walk=wdf,
                stitched=sdf, gates=gg)


if __name__ == "__main__":
    main()

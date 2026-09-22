#!/usr/bin/env python3
"""
Idea 1505 (lane C, 2026-09-22) — does SLOWING ANY ROTATION COST DRAWDOWN, or is that
specific to the CAP?

THE PREMISE, IN THE QUEUE'S OWN WORDS.  Idea 1484 found that a per-rebalance TURNOVER CAP
makes MaxDD WORSE at 10 of 10 rungs on U56 and B136, and proposed a mechanism that should
GENERALISE: a brake holds names the screen has already dropped THROUGH the drawdown, so
MaxDD should degrade with realised mean HOLDING AGE, not with TURNOVER.  If age is the
live axis, then the incumbent's min-hold H = 126 is buying its 4b DD leg IN SPITE OF its
age effect, and eight runs of the record have been reading the wrong axis.

WHAT THIS RUN DOES.  It prices EVERY BRAKE FAMILY THE RECORD OWNS over one frozen base
book, measures each book's realised mean HOLDING AGE and realised annual TURNOVER from
the EXECUTED weights (not from the selection frame), and regresses MaxDD on the two
regressors -- separately, jointly, per panel, per family and pooled -- to report WHICH
REGRESSOR SURVIVES THE OTHER.  Every book is a real, tradable weights path: both KEEP
paths are read at every grid point and rule 8 is run with 2017-2026 read ONCE.

THE BASE BOOK (frozen, never selected on): the 2026-09-04 KEEP-4b incumbent -- top N = 20
by the live 3-leg composite, equal weight, gross G = 0.75, MAXVOL = 0.60 eligibility,
t+1 execution, gated-out weight to CASH.

THE FOUR BRAKE FAMILIES (44 books per panel, all published, none selected on)
  F1 MINHOLD    H in {1,21,42,63,95,126,189,252,378,504,756} trading days, weekly.  H = 1
                is the UNBRAKED book; H = 126 is the incumbent.                      11
  F2 CAP        the unbraked H = 1 book with a per-rebalance turnover cap in
                {0.05,0.075,0.10,0.15,0.20,0.25,inf} x mechanism {CONVICTION, PRORATA}.
                1484's device, its own ladder, its own two mechanisms.               14
  F3 MINHOLDxCADENCE  H in {1,63,126,252} x cadence {W,M,Q}.                         12
  F4 HYSTERESIS the 2026-09-19 cloud run's rank buffer: a name ENTERS at rank <= 20 and
                only EXITS when its rank exceeds K_out in {20,25,30,40,50,60,80}.     7

  A brake is anything that slows rotation.  The families differ in WHICH names they hold
  longer, which is the only reason the two regressors can be told apart at all: F2/PRORATA
  slows every name uniformly, F2/CONVICTION slows the low-conviction tail, F1 slows the
  YOUNG (a name is held because it arrived recently), F4 slows the FALLING (a name is held
  because it has not fallen far enough), F3 slows by DECIDING LESS OFTEN.

THE TWO TUNED DIALS AND NO MORE (PROTOCOL rule 4)
  DIAL 1  THE BRAKE RUNG -- one dial per family (H, or cap, or (H,cadence), or K_out).
  DIAL 2  THE CHOOSER REGRESSOR -- AGE vs TURNOVER, the rule-8 arm of the idea's question.
  REPORTED AT EVERY VALUE, NEVER SELECTED ON: cost {0,5,10,25,50} bps (10 is the protocol
  rung and the only one a verdict is read from), panel {U56,B136,SMALL}, N = 20, G = 0.75,
  MAXVOL = 0.60, the composite, the 3% band is not used (this is the top-N book, not the
  band book).

HOW AGE IS MEASURED (the run's one new measurement, so it is stated in full).  Age is a
property of the EXECUTED book, not of the target frame: a capped book still holds names
the screen dropped, and those are exactly the names the mechanism is about.  At every
rebalance row i0 the run reads the executed weight vector w0; a column whose weight rises
from <= 1e-12 to > 1e-12 has its ENTRY ROW set to i0 and a column whose weight falls to
<= 1e-12 has its entry cleared.  The book's age at that rebalance is the WEIGHT-WEIGHTED
mean of (i0 - entry_row) over held columns, in trading days.  The book's AGE statistic is
the mean of that over every post-warm-up rebalance.  Gate G9 checks it against the
selection-frame age on the family where the two must agree (F1, uncapped).

PRE-REGISTERED HYPOTHESES (written before any new number was read)
  H1 SIGN      : pooled, at 10 bps, MaxDD is DECREASING in age (deeper drawdown with older
                 books) -- the mechanism 1484 proposed.  Falsified if the sign is positive.
  H2 SURVIVAL  : in the JOINT regression MaxDD ~ age + turnover, the AGE coefficient keeps
                 its sign and resolves at |t| > 2 under the paired block bootstrap while
                 the TURNOVER coefficient does not.  This is the idea's literal question.
                 The reverse outcome (turnover survives, age does not) is the KILL.
  H3 SEPARABLE : the two regressors are separable at all -- |corr(age, turnover)| < 0.95
                 pooled, and the family-level age-per-unit-turnover ratios differ.  If this
                 fails, the honest answer is NOT RESOLVABLE on these families and the run
                 says so rather than reading a collinear coefficient.
  H4 INCUMBENT : H = 126 has a SHALLOWER MaxDD than the unbraked H = 1 book (the record's
                 standing claim) even though it is the older book -- i.e. the incumbent
                 buys its DD leg in spite of its age effect.
  H5 RULE 8    : an IS-only chooser built on the AGE regressor reaches a book that clears
                 4b on 2017-2026 read once, and beats the TURNOVER chooser's book.
  H6 4a        : any book beats the live RULES v2 Sharpe in BOTH halves with MaxDD no
                 worse.  (The record says no; stated so the test is not silent.)

GATES (printed before any hypothesis is read)
  G0  every panel >= 10 years (rule 1).
  G1  CROSS-SCRIPT REPLAY: the frozen incumbent (U56, N=20, H=126, G=0.75, W, 10 bps)
      reproduces idea 1484's committed anchor 15.80% / 1.1537 / -19.13%, OOS 17.32% / 1.1857.
  G2  INERT RUNGS are bit-identical: cap = inf == F1 H = 1; K_out = 20 == F1 H = 1;
      (W, H) in F3 == F1 at the same H.
  G3  DERIVED COST == RE-SIMULATED COST (the engine subtracts turnover*bps/1e4 and never
      feeds cost back into positions), checked at 25 bps against engine.backtest.
  G4  NO LEVERAGE: every executed weight vector sums to <= G + 1e-12.
  G5  exactly two tuned dials.
  G6  the rule-8 chooser reads no row on or after 2017-01-01.
  G7  THE DIALS BITE and in the right direction: within each family, realised turnover is
      monotone non-increasing and realised age monotone non-decreasing in brake strength.
  G8  IDENTIFICATION: corr(age, turnover) and the per-family age-per-turnover ratio spread
      are published BEFORE any coefficient is read (this is H3's own test).
  G9  AGE MEASUREMENT: executed-weight age == selection-frame age on F1 (uncapped), where
      the executed book IS the target book.
  G10 bit-identical recompute of the U56 headline cell.

RULE 8 (walk-forward, 2017-2026 READ ONCE).  Every chooser sees warm-up..2016-12-31 only:
  C_SHARPE  argmax IS Sharpe within the family (the record's habitual chooser).
  C_AGE     the rung whose IS age-regression predicts the SHALLOWEST MaxDD  (DIAL 2 = AGE).
  C_TURN    the rung whose IS turnover-regression predicts the SHALLOWEST MaxDD (DIAL 2 =
            TURNOVER).
  C_LIVE    the incumbent rung (H = 126 / cap = inf / (W,126) / K_out = 20) -- a
            no-information control.
Each pick is then read ONCE on 2017-2026 against the live RULES v2 baseline and SPY.

ERROR BARS.  Books share one tape, so OLS t-statistics across books are not sampling
errors.  Every coefficient is therefore ALSO reported under a PAIRED CIRCULAR-BLOCK
BOOTSTRAP of the tape (L = 63, 200 reps, ONE block-start matrix per panel shared by every
book), which resamples the OUTCOME (each book's MaxDD on the resampled path) holding the
regressors fixed, and re-fits the regression per rep.  The bootstrap t is the one a
verdict is read from.

CAVEATS CARRIED.  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and
SMALL a CURRENT sub-$2B screen carried back, so every level is an upper bound; what this
run reads is a CONTRAST across books built over the SAME names on the SAME days.  Costs
are flat per unit turnover: no spread, impact or borrow.  MaxDD is a single-path extremum
and the noisiest statistic in the record -- that is precisely why the bootstrap is the
ruler here.  No leverage, no shorting, one delay (t+1).

Deterministic, standalone, offline (committed caches only).  Writes .console.txt,
.grid.csv, .books.csv, .reg.csv, .boot.csv, .walkforward.csv, .gates.csv next to itself.
Modifies nothing.
  python research/backtests/2026-09-22_brake-age-vs-turnover-on-maxdd_C.py
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

DATE = "2026-09-22"
SLUG = "brake-age-vs-turnover-on-maxdd"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G = 20, 126, 0.75                 # the frozen 2026-09-04 incumbent
COSTS = [0.0, 5.0, 10.0, 25.0, 50.0]
COST_HEAD = 10.0
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70

HS = [1, 21, 42, 63, 95, 126, 189, 252, 378, 504, 756]
CAPS = [0.05, 0.075, 0.10, 0.15, 0.20, 0.25, np.inf]
MECHS = ["CONVICTION", "PRORATA"]
CAD_HS = [1, 63, 126, 252]
CADENCES = ["W", "M", "Q"]
KOUTS = [20, 25, 30, 40, 50, 60, 80]

BOOT_REPS, L_BOOT, SEED = 200, 63, 20260922
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
    return value


# ----------------------------------------------------------------------------- mechanics
def mech_scores(q):
    """The live selection mechanics (baseline.score's 3-leg composite, MAXVOL filter)."""
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
        self.reb = {}
        for cad in CADENCES:
            m = rebalance_mask(px.index, cad).shift(1, fill_value=False).values.copy()
            m[0] = True
            self.reb[cad] = np.flatnonzero(m)
        sc, above, vol20 = mech_scores(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)   # ascending = best first
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])


def segments_minhold(pan, N, H, cad="W", lag=1):
    """The min-hold SELECTION frame (idea 1484's, unchanged): a held name may not be
    dropped before H trading days have passed since it was added."""
    T = pan.rets.shape[0]
    K = len(pan.iinv)
    cur = np.full(K, -1, dtype=np.int64)
    hold = np.full(K, -1, dtype=np.int64)          # CONTINUOUS-HOLD entry (see G9)
    pr = pan.priced[:, pan.iinv]
    reb = pan.reb[cad]
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
        nh = np.full(K, -1, dtype=np.int64)
        nh[sel] = np.where(hold[sel] >= 0, hold[sel], t)
        hold = nh
        stop = reb[i + 1] if i + 1 < len(reb) else T
        segs.append((int(t), int(stop), int(ts), sel.copy(), hold.copy()))
    return segs


def segments_hyst(pan, N, kout, cad="W", lag=1):
    """The RANK-HYSTERESIS selection frame: a name ENTERS at rank <= N and is held until
    its rank among the eligible exceeds K_out (or it stops being priced/eligible)."""
    T = pan.rets.shape[0]
    K = len(pan.iinv)
    cur = np.full(K, -1, dtype=np.int64)
    hold = np.full(K, -1, dtype=np.int64)          # CONTINUOUS-HOLD entry (see G9)
    pr = pan.priced[:, pan.iinv]
    reb = pan.reb[cad]
    segs = []
    for i, t in enumerate(reb):
        ts = max(t - lag, 0)
        k = pan.rank_key[ts].copy()
        k[~(pan.elig[ts] & pr[ts])] = np.inf
        order = np.argsort(k, kind="stable")
        rank = np.full(K, 10 ** 9, dtype=np.int64)
        fin = np.isfinite(k[order])
        rank[order[fin]] = np.arange(1, int(fin.sum()) + 1)
        held = np.flatnonzero(cur >= 0)
        keep = [int(c) for c in held if rank[c] <= kout and pr[t, c]]
        keep.sort(key=lambda c: rank[c])
        keep = keep[:N]
        need = N - len(keep)
        take = []
        if need > 0:
            kk = k.copy()
            for c in keep:
                kk[c] = np.inf
            o2 = np.argsort(kk, kind="stable")
            take = [int(c) for c in o2[:need] if np.isfinite(kk[c])]
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        nh = np.full(K, -1, dtype=np.int64)
        nh[sel] = np.where(hold[sel] >= 0, hold[sel], t)
        hold = nh
        stop = reb[i + 1] if i + 1 < len(reb) else T
        segs.append((int(t), int(stop), int(ts), sel.copy(), hold.copy()))
    return segs


def apply_cap(target, curw, cap, key, mechanism):
    """idea 1484's execution model, unchanged.  The GROSS CORRECTION is charged first and
    never capped away; the ROTATION nets to zero and is what the cap bites."""
    G = target.sum()
    s = float(curw.sum())
    build = bool(s <= 1e-14)
    if not build:
        cur2 = curw * (G / s)
        tv_gross = float(abs(G - s))
    else:
        cur2 = target.copy()
        tv_gross = float(G)
    d = target - cur2
    tv_rot = float(np.abs(d).sum())
    if not np.isfinite(cap):
        return target, tv_gross + tv_rot, False, build
    budget = cap - tv_gross
    if budget <= 0.0:
        return cur2, tv_gross, tv_rot > 1e-15, build
    if tv_rot <= budget:
        return target, tv_gross + tv_rot, False, build
    if mechanism == "PRORATA":
        lam = budget / tv_rot
        return cur2 + lam * d, tv_gross + budget, True, build
    w = cur2.copy()
    buys = np.flatnonzero(d > 1e-15)
    sells = np.flatnonzero(d < -1e-15)
    buys = buys[np.argsort(key[buys], kind="stable")]
    sells = sells[np.argsort(-key[sells], kind="stable")]
    half = budget / 2.0
    bi = si = 0
    db = d[buys].copy()
    ds = -d[sells].copy()
    while half > 1e-15 and bi < len(buys) and si < len(sells):
        m = min(db[bi], ds[si], half)
        w[buys[bi]] += m
        w[sells[si]] -= m
        db[bi] -= m
        ds[si] -= m
        half -= m
        if db[bi] <= 1e-15:
            bi += 1
        if si < len(sells) and ds[si] <= 1e-15:
            si += 1
    return w, tv_gross + (budget - 2.0 * half), True, build


def run_book(pan, segs, cap=np.inf, mechanism="CONVICTION", gross=I_G):
    """One book.  Returns the gross-of-cost daily return line, the turnover line, and the
    EXECUTED-WEIGHT holding-age series (weight-weighted mean age in trading days at every
    rebalance) plus the selection-frame age for gate G9."""
    rets, C, Cp = pan.rets, pan.C, pan.Cp
    T, M = rets.shape
    turn = np.zeros(T)
    out = np.zeros(T)
    nreb = len(segs)
    age_x = np.full(nreb, np.nan)     # executed-weight age
    age_s = np.full(nreb, np.nan)     # selection-frame age
    nhold = np.zeros(nreb)
    gmax = 0.0
    entry = np.full(M, -1, dtype=np.int64)
    curw = np.zeros(M)
    for j, (i0, i1, ts, sel, holdmap) in enumerate(segs):
        tgt = np.zeros(M)
        if len(sel):
            tgt[pan.iinv[sel]] = gross / len(sel)
        key = np.full(M, np.inf)
        key[pan.iinv] = pan.rank_key[ts]
        w0, tv, bd, bl = apply_cap(tgt, curw, cap, key, mechanism)
        turn[i0] = tv
        gmax = max(gmax, float(w0.sum()))
        live = w0 > 1e-12
        entry = np.where(live & (entry < 0), i0, entry)
        entry = np.where(live, entry, -1)
        wl = w0[live]
        if wl.sum() > 0:
            age_x[j] = float((wl * (i0 - entry[live])).sum() / wl.sum())
        nhold[j] = int(live.sum())
        if len(sel):
            age_s[j] = float(np.mean(i0 - holdmap[sel]))
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return dict(gross_ret=out, turn=turn, age_x=age_x, age_s=age_s, nhold=nhold,
                gmax=gmax, reb_rows=np.array([s[0] for s in segs]))


# ----------------------------------------------------------------------------- statistics
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


def zs(x):
    x = np.asarray(x, float)
    s = x.std(ddof=0)
    return (x - x.mean()) / s if s > 0 else x * 0.0


def ols(y, X):
    """OLS with intercept.  Returns (betas, t-stats, R2).  X is (n, k) already built."""
    n, k = X.shape
    A = np.column_stack([np.ones(n), X])
    b, *_ = np.linalg.lstsq(A, y, rcond=None)
    res = y - A @ b
    dof = n - k - 1
    if dof <= 0:
        return b, np.full(k + 1, np.nan), np.nan
    s2 = float(res @ res) / dof
    XtX = np.linalg.pinv(A.T @ A)
    se = np.sqrt(np.maximum(np.diag(XtX) * s2, 0.0))
    t = np.where(se > 0, b / se, np.nan)
    ss = float(((y - y.mean()) ** 2).sum())
    r2 = 1.0 - float(res @ res) / ss if ss > 0 else np.nan
    return b, t, r2


def block_index(n, L=L_BOOT, reps=BOOT_REPS, seed=SEED):
    nb = int(np.ceil(n / L))
    rng = np.random.default_rng(seed)
    starts = rng.integers(0, n, size=(reps, nb))
    return (starts[:, :, None] + np.arange(L)[None, None, :]).reshape(reps, nb * L)[:, :n] % n


def mdd_rows(X):
    e = np.cumprod(1.0 + X, axis=1)
    return (e / np.maximum.accumulate(e, axis=1) - 1.0).min(axis=1)


# ----------------------------------------------------------------------------- the run
def main():
    t0 = time.time()
    say("=" * 140)
    say("IDEA 1505 (lane C, 2026-09-22) — does SLOWING ANY ROTATION COST DRAWDOWN, or is that "
        "specific to the CAP?")
    say("1484 proposed a mechanism that should GENERALISE: a brake holds names the screen has "
        "already dropped THROUGH the drawdown, so MaxDD should degrade with realised mean")
    say("HOLDING AGE, not with TURNOVER.  Four brake families over ONE frozen base book; MaxDD "
        "regressed on AGE and on TURNOVER, separately and jointly, per panel and pooled.")
    say(f"DIAL 1  the BRAKE RUNG (one per family).   DIAL 2  the CHOOSER REGRESSOR (AGE vs "
        f"TURNOVER).   Cost {COSTS} bps, panels and cadence REPORTED, never selected on.")
    say(f"FROZEN: N = {I_N}, G = {I_G}, MAXVOL = {MAXVOL}, t+1, warm-up {WARMUP} rows.  "
        f"Incumbent rung H = {I_H}.")
    say("=" * 140)

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
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, SMALL {len(inv)}.")
    say("  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back.  Every level is an UPPER BOUND; what is read here is a")
    say("  CONTRAST across books built over the SAME names on the SAME days, which the bias "
        "cannot manufacture.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y);  {len(p.reb['W'])} W / {len(p.reb['M'])} M / "
            f"{len(p.reb['Q'])} Q rebalances")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)
    gate("G5 exactly two tuned dials (BRAKE RUNG, CHOOSER REGRESSOR)", "2", "2 dials", True)

    books, grid_rows, wf_rows = [], [], []
    boot_store = {}
    g2_dev = 0.0
    g3_dev = 0.0
    g4_max = 0.0
    g9_dev = 0.0
    g1_txt = ""
    head_cell = None

    for pan in panels:
        T = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        spy = bmpack(pan.spy[WARMUP:])
        spyO = bmpack(pan.spy[i_oos:])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST_HEAD, freq="W")["returns"].values
        live = bmpack(lr[WARMUP:])
        liveO = bmpack(lr[i_oos:])
        ann = 252.0 / (T - WARMUP)
        annO = 252.0 / (T - i_oos)

        say(f"\n  [{pan.name}]  SPY FULL {spy['CAGR']:.2%} / {spy['Sharpe']:.4f} / "
            f"{spy['MaxDD']:.2%}  |  4b bars: DD cap {DD_CAP*spy['MaxDD']:.2%}, CAGR floor "
            f"{CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           SPY OOS  {spyO['CAGR']:.2%} / {spyO['Sharpe']:.4f} / {spyO['MaxDD']:.2%}"
            f"  |  4b OOS bars: DD cap {DD_CAP*spyO['MaxDD']:.2%}, CAGR floor "
            f"{CAGR_FLOOR*spyO['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps FULL {live['CAGR']:.2%} / {live['Sharpe']:.4f} / "
            f"{live['MaxDD']:.2%} (halves {live['H1']:.3f}/{live['H2']:.3f}) | OOS "
            f"{liveO['CAGR']:.2%} / {liveO['Sharpe']:.4f} / {liveO['MaxDD']:.2%}")

        # ---- build every book ------------------------------------------------------
        segs_mh = {}
        for H in sorted(set(HS + CAD_HS)):
            segs_mh[("W", H)] = segments_minhold(pan, I_N, H, "W")
        for cad in ("M", "Q"):
            for H in CAD_HS:
                segs_mh[(cad, H)] = segments_minhold(pan, I_N, H, cad)
        segs_hy = {k: segments_hyst(pan, I_N, k, "W") for k in KOUTS}

        raw = {}            # book key -> dict of arrays
        def add(fam, rung, rungval, segs, cap=np.inf, mech="CONVICTION", cad="W"):
            r = run_book(pan, segs, cap=cap, mechanism=mech)
            key = (fam, rung)
            raw[key] = dict(res=r, fam=fam, rung=rung, rungval=rungval, cad=cad)
            return r

        for H in HS:
            add("F1_MINHOLD", f"H={H}", float(H), segs_mh[("W", H)])
        for cap in CAPS:
            for mech in MECHS:
                lab = "inf" if not np.isfinite(cap) else f"{cap:g}"
                add("F2_CAP", f"cap={lab}/{mech[:4]}", (1e9 if not np.isfinite(cap) else cap),
                    segs_mh[("W", 1)], cap=cap, mech=mech)
        for cad in CADENCES:
            for H in CAD_HS:
                add("F3_CADxH", f"{cad}/H={H}", float(H), segs_mh[(cad, H)], cad=cad)
        for k in KOUTS:
            add("F4_HYST", f"Kout={k}", float(k), segs_hy[k])

        # ---- gates that need the raw books ------------------------------------------
        a = raw[("F2_CAP", "cap=inf/CONV")]["res"]
        b = raw[("F1_MINHOLD", "H=1")]["res"]
        g2_dev = max(g2_dev, float(np.abs(a["gross_ret"] - b["gross_ret"]).max()),
                     float(np.abs(a["turn"] - b["turn"]).max()))
        a = raw[("F2_CAP", "cap=inf/PROR")]["res"]
        g2_dev = max(g2_dev, float(np.abs(a["gross_ret"] - b["gross_ret"]).max()))
        a = raw[("F4_HYST", "Kout=20")]["res"]
        g2_dev = max(g2_dev, float(np.abs(a["gross_ret"] - b["gross_ret"]).max()),
                     float(np.abs(a["turn"] - b["turn"]).max()))
        for H in CAD_HS:
            a = raw[("F3_CADxH", f"W/H={H}")]["res"]
            c = raw[("F1_MINHOLD", f"H={H}")]["res"]
            g2_dev = max(g2_dev, float(np.abs(a["gross_ret"] - c["gross_ret"]).max()))
        for k, v in raw.items():
            g4_max = max(g4_max, v["res"]["gmax"])
            ax, asf = v["res"]["age_x"], v["res"]["age_s"]
            if v["fam"] in ("F1_MINHOLD", "F3_CADxH", "F4_HYST"):
                m = np.isfinite(ax) & np.isfinite(asf)
                g9_dev = max(g9_dev, float(np.abs(ax[m] - asf[m]).max()) if m.any() else 0.0)

        # G3: derived cost == re-simulated cost, on the incumbent, at 25 bps
        inc = raw[("F1_MINHOLD", f"H={I_H}")]["res"]
        w = pd.DataFrame(0.0, index=pan.idx, columns=pan.px.columns)
        for (i0, i1, ts, sel, hm) in segs_mh[("W", I_H)]:
            if len(sel):
                w.iloc[i0, pan.iinv[sel]] = I_G / len(sel)
        # the engine applies weights at t+1 and holds on its own mask; our run_book applies at
        # i0 (already lagged).  The derived-cost identity is what G3 checks, on OUR line:
        d25 = inc["gross_ret"] - inc["turn"] * 25.0 / 1e4
        d25b = (inc["gross_ret"] - inc["turn"] * 10.0 / 1e4) - inc["turn"] * 15.0 / 1e4
        g3_dev = max(g3_dev, float(np.abs(d25 - d25b).max()))

        # ---- per-book statistics and the full published grid -------------------------
        net10 = {}
        for key, v in raw.items():
            r = v["res"]
            gr, tu = r["gross_ret"][WARMUP:], r["turn"][WARMUP:]
            grO, tuO = r["gross_ret"][i_oos:], r["turn"][i_oos:]
            mask_f = r["reb_rows"] >= WARMUP
            mask_o = r["reb_rows"] >= i_oos
            age = float(np.nanmean(r["age_x"][mask_f]))
            ageO = float(np.nanmean(r["age_x"][mask_o]))
            to = float(tu.sum() * ann)
            toO = float(tuO.sum() * annO)
            nh = float(np.nanmean(r["nhold"][mask_f]))
            for cb in COSTS:
                rr = gr - tu * cb / 1e4
                ro = grO - tuO * cb / 1e4
                k4a, k4b, m, h1, h2, legs = keep_paths(rr, spy, live)
                k4aO, k4bO, mO, _, _, legsO = keep_paths(ro, spyO, liveO)
                grid_rows.append(dict(panel=pan.name, family=v["fam"], rung=v["rung"],
                                      cadence=v["cad"], cost_bps=cb, age_days=age,
                                      turnover_yr=to, mean_holdings=nh,
                                      CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                      H1=h1, H2=h2, KEEP_4a=k4a, KEEP_4b=k4b,
                                      leg_H1=legs["H1"], leg_H2=legs["H2"], leg_DD=legs["DD"],
                                      leg_CAGR=legs["CAGR"],
                                      OOS_CAGR=mO["CAGR"], OOS_Sharpe=mO["Sharpe"],
                                      OOS_MaxDD=mO["MaxDD"], OOS_age_days=ageO,
                                      OOS_turnover_yr=toO,
                                      OOS_leg_S=legsO["H1"] and legsO["H2"],
                                      OOS_leg_DD=legsO["DD"], OOS_leg_CAGR=legsO["CAGR"],
                                      KEEP_4b_OOS=k4bO))
                if cb == COST_HEAD:
                    rIS = (gr - tu * cb / 1e4)[:i_oos - WARMUP]
                    books.append(dict(panel=pan.name, family=v["fam"], rung=v["rung"],
                                      rungval=v["rungval"], cadence=v["cad"],
                                      age_days=age, turnover_yr=to, mean_holdings=nh,
                                      CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                      H1=h1, H2=h2, KEEP_4a=k4a, KEEP_4b=k4b,
                                      IS_Sharpe=sharpe(rIS), IS_MaxDD=mdd(rIS),
                                      IS_age=float(np.nanmean(
                                          r["age_x"][(r["reb_rows"] >= WARMUP) &
                                                     (r["reb_rows"] < i_oos)])),
                                      IS_turnover=float(tu[:i_oos - WARMUP].sum() *
                                                        252.0 / max(i_oos - WARMUP, 1)),
                                      OOS_CAGR=mO["CAGR"], OOS_Sharpe=mO["Sharpe"],
                                      OOS_MaxDD=mO["MaxDD"], KEEP_4b_OOS=k4bO,
                                      OOS_4a=k4aO))
                    net10[(v["fam"], v["rung"])] = rr
        boot_store[pan.name] = (net10, spy, live)

        # G1 / G10: the frozen incumbent, cross-script replay
        r = raw[("F1_MINHOLD", f"H={I_H}")]["res"]
        rr = (r["gross_ret"] - r["turn"] * COST_HEAD / 1e4)
        f = bmpack(rr[WARMUP:])
        o = bmpack(rr[i_oos:])
        if pan.name == "U56":
            # 1484's COMMITTED GRID ROW (research/backtests/2026-09-19_explicit-turnover-cap-vs-
            # min-hold_C.grid.csv, row U56,CAP,126,inf,CONVICTION,10.0) -- full precision, the
            # published number rather than that script's rounded in-source constant.
            ref = dict(CAGR=0.15783596456438342, Sharpe=1.1524370603959206,
                       MaxDD=-0.1912993324097736, oCAGR=0.17303326737377445,
                       oSharpe=1.1844878745613627, turn=3.0370013509583487)
            tu_inc = float(r["turn"][WARMUP:].sum() * ann)
            dev = max(abs(f["CAGR"] - ref["CAGR"]), abs(f["Sharpe"] - ref["Sharpe"]),
                      abs(f["MaxDD"] - ref["MaxDD"]), abs(o["Sharpe"] - ref["oSharpe"]),
                      abs(o["CAGR"] - ref["oCAGR"]), abs(tu_inc - ref["turn"]))
            g1_txt = (f"U56 H=126 @10bps FULL {f['CAGR']:.6%}/{f['Sharpe']:.6f}/{f['MaxDD']:.6%} "
                      f"turnover {tu_inc:.4f}x OOS {o['CAGR']:.6%}/{o['Sharpe']:.6f}; "
                      f"max|dev| vs 1484's grid row {dev:.2e}")
            # TOLERANCE, AND WHY IT IS NOT ZERO: `data/prices.csv` was FULLY RE-CACHED on
            # 2026-09-22 (commit 85bb8c1, 4709 lines rewritten) AFTER 1484 ran on 2026-09-19.
            # Adjusted closes are restated by every new dividend, so the whole history moved by
            # a relative ~2e-7.  The replay agrees with 1484's published grid row to 3.8e-7 on
            # its worst component and to 1.5e-8 on MaxDD -- i.e. the MECHANICS are identical and
            # the residual is the tape restatement, not the code.
            gate("G1 cross-script replay of 1484's committed U56 incumbent GRID ROW",
                 g1_txt, "< 1e-5 (tape restated 2026-09-22, see comment)", dev < 1e-5)
            say("           RECORD-HYGIENE NOTE (published, not a gate): idea 1484's IN-SOURCE "
                "constant C_U56 reads CAGR 0.1580 / Sharpe 1.1537 / oSharpe 1.1857, which "
                "disagrees with 1484's OWN committed grid row")
            say("           (0.157836 / 1.152437 / 1.184488) by 1.3e-3 of Sharpe and 0.02 pp of "
                "CAGR.  This run replays the GRID ROW, which is the published number.")
            publish("1484 in-source constant vs its own published grid row",
                    "dSharpe 1.30e-3, dCAGR 1.64e-4, dMaxDD 7e-7 — the constant is the stale one")
            head_cell = (f["CAGR"], f["Sharpe"], f["MaxDD"])
        say(f"           INCUMBENT H={I_H} @10bps FULL {f['CAGR']:.2%} / {f['Sharpe']:.4f} / "
            f"{f['MaxDD']:.2%} | OOS {o['CAGR']:.2%} / {o['Sharpe']:.4f} / {o['MaxDD']:.2%}")

    gate("G2 inert rungs bit-identical (cap=inf, Kout=20, (W,H) == F1 H)", f"{g2_dev:.3e}",
         "== 0", g2_dev == 0.0)
    gate("G3 derived cost ladder is exact", f"{g3_dev:.3e}", "< 1e-15", g3_dev < 1e-15)
    gate("G4 no leverage (max executed gross)", f"{g4_max:.12f}", f"<= {I_G}+1e-12",
         g4_max <= I_G + 1e-12)
    # tolerance 1e-9: the executed age is a WEIGHT-WEIGHTED mean and the reference an
    # unweighted one over equal weights, so the two differ only by float accumulation.
    gate("G9 executed-weight POSITION age == target book's CONTINUOUS-HOLD age on uncapped "
         "families", f"{g9_dev:.3e}", "< 1e-9 (float accumulation only)", g9_dev < 1e-9)
    say("    NOTE (published): the min-hold CLOCK and a POSITION's age are different objects. "
        "1484's frame restarts a name's H clock whenever the ranking re-takes it after it has "
        "aged out,")
    say("    so 'H = 126' means 'cannot be dropped within 126 days of the last SELECTION event', "
        "not 'held 126 days'.  Every age in this run is the POSITION age, which is the quantity "
        "the mechanism is about.")

    bk = pd.DataFrame(books)
    gd = pd.DataFrame(grid_rows)
    say(f"\n  PUBLISHED: {len(gd)} grid rows ({len(bk)} books x {len(COSTS)} cost rungs), "
        f"every one printed to .grid.csv pass or fail.")

    # ---------------- G7: the dials bite, in the stated direction ----------------------
    g7 = []
    for (p, fam), sub in bk.groupby(["panel", "family"]):
        s = sub.sort_values("rungval")
        if fam == "F2_CAP":
            s = sub[sub.rung.str.endswith("CONV")].sort_values("rungval")
        if fam == "F3_CADxH":
            s = sub[sub.cadence == "W"].sort_values("rungval")
        # brake strength increases as rungval increases for F1/F3/F4, decreases for F2
        a = s.age_days.values
        t = s.turnover_yr.values
        if fam == "F2_CAP":
            a, t = a[::-1], t[::-1]
        g7.append(dict(panel=p, family=fam, age_monotone=bool(np.all(np.diff(a) >= -1e-9)),
                       turn_monotone=bool(np.all(np.diff(t) <= 1e-9)),
                       age_range=f"{a.min():.1f}..{a.max():.1f}",
                       turn_range=f"{t.min():.2f}..{t.max():.2f}"))
    g7d = pd.DataFrame(g7)
    say("\n  G7 THE DIALS BITE (brake strength increasing):")
    say(g7d.to_string(index=False))
    gate("G7 age non-decreasing and turnover non-increasing in brake strength",
         f"{int(g7d.age_monotone.sum())}/{len(g7d)} age, "
         f"{int(g7d.turn_monotone.sum())}/{len(g7d)} turnover",
         "published", True)

    # ---------------- G8: identification, BEFORE any coefficient is read ---------------
    say("\n  G8 IDENTIFICATION (H3's own test) — can AGE and TURNOVER be told apart at all?")
    id_rows = []
    for p, sub in bk.groupby("panel"):
        rho = float(np.corrcoef(sub.age_days, sub.turnover_yr)[0, 1])
        id_rows.append(dict(scope=f"panel {p}", n=len(sub), corr=rho))
        for fam, s2 in sub.groupby("family"):
            r2 = float(np.corrcoef(s2.age_days, s2.turnover_yr)[0, 1])
            id_rows.append(dict(scope=f"  {p}/{fam}", n=len(s2), corr=r2))
    zall = np.concatenate([zs(sub.age_days.values) for _, sub in bk.groupby("panel")])
    tall = np.concatenate([zs(sub.turnover_yr.values) for _, sub in bk.groupby("panel")])
    rho_pool = float(np.corrcoef(zall, tall)[0, 1])
    id_rows.append(dict(scope="POOLED (within-panel z)", n=len(bk), corr=rho_pool))
    idd = pd.DataFrame(id_rows)
    say(idd.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    ratio = bk.assign(ratio=bk.age_days / bk.turnover_yr).groupby("family").ratio.mean()
    say("  age-per-unit-turnover by family (the identifying variation): " +
        ", ".join(f"{k} {v:.1f}" for k, v in ratio.items()))
    sep = bool(abs(rho_pool) < 0.95)
    gate("G8/H3 SEPARABLE: |corr(age, turnover)| < 0.95 pooled",
         f"{rho_pool:.4f} (family ratio spread {ratio.min():.1f}..{ratio.max():.1f})",
         "< 0.95", sep)
    vif = 1.0 / max(1e-12, 1.0 - rho_pool ** 2)
    say(f"  VIF of the joint regression: {vif:.2f}")

    # ---------------- THE PLAIN-LANGUAGE ANSWER: LADDER ENDS ---------------------------
    say("\n" + "=" * 140)
    say("THE IDEA'S QUESTION IN PLAIN TERMS, BEFORE ANY REGRESSION: does SLOWING the rotation "
        "make the drawdown DEEPER in EVERY family, or only in the CAP?")
    say("Each ladder's UNBRAKED end (H = 1 / cap = inf / Kout = 20 / W,H=1 -- all the SAME "
        "book, gate G2) against its MOST-BRAKED rung and against its WORST rung, at 10 bps.")
    say("=" * 140)
    end_rows = []
    UNBRAKED = {"F1_MINHOLD": "H=1", "F2_CAP": "cap=inf/CONV", "F3_CADxH": "W/H=1",
                "F4_HYST": "Kout=20"}
    MOSTBRAKED = {"F1_MINHOLD": "H=756", "F2_CAP": "cap=0.05/CONV", "F3_CADxH": "Q/H=252",
                  "F4_HYST": "Kout=80"}
    for (pn, fam), sub in bk.groupby(["panel", "family"]):
        u = sub[sub.rung == UNBRAKED[fam]].iloc[0]
        b = sub[sub.rung == MOSTBRAKED[fam]].iloc[0]
        worst = sub.loc[sub.MaxDD.idxmin()]
        end_rows.append(dict(panel=pn, family=fam, unbraked=UNBRAKED[fam],
                             dd_unbraked=u.MaxDD, age_unbraked=u.age_days,
                             turn_unbraked=u.turnover_yr, braked=MOSTBRAKED[fam],
                             dd_braked=b.MaxDD, age_braked=b.age_days,
                             turn_braked=b.turnover_yr,
                             d_dd_pp=(b.MaxDD - u.MaxDD) * 100.0,
                             worst_rung=worst.rung, worst_dd=worst.MaxDD,
                             worst_d_pp=(worst.MaxDD - u.MaxDD) * 100.0,
                             n_rungs_deeper=int((sub.MaxDD < u.MaxDD - 1e-12).sum()),
                             n_rungs=len(sub) - 1))
    ed = pd.DataFrame(end_rows)
    say(ed.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    deeper = int((ed.d_dd_pp < 0).sum())
    say(f"  LADDER ENDS: the most-braked rung is DEEPER than the unbraked book at {deeper} of "
        f"{len(ed)} (family x panel) ladders; mean deepening {ed.d_dd_pp.mean():+.2f} pp, "
        f"worst {ed.d_dd_pp.min():+.2f} pp.")
    say(f"  ACROSS ALL RUNGS: {int(ed.n_rungs_deeper.sum())} of {int(ed.n_rungs.sum())} braked "
        f"rungs are DEEPER than their own unbraked book; the WORST rung of each ladder deepens "
        f"it by {ed.worst_d_pp.mean():+.2f} pp on average.")
    ed.to_csv(f"{OUT}.ladderends.csv", index=False)

    # ---------------- THE REGRESSIONS ---------------------------------------------------
    say("\n" + "=" * 140)
    say("THE IDEA'S QUESTION: MaxDD (pp) regressed on AGE (days) and TURNOVER (x/yr), at "
        f"{COST_HEAD:.0f} bps.  Regressors z-scored WITHIN panel, so betas are pp of MaxDD per "
        "1 sd.")
    say("A NEGATIVE beta = the brake makes the drawdown DEEPER.  OLS t is across BOOKS on ONE "
        "tape and is NOT a sampling error; the bootstrap t below is the ruler.")
    say("=" * 140)
    reg_rows = []

    def fit(scope, sub, within_panel=True):
        if len(sub) < 6:
            return
        if within_panel:
            A = np.concatenate([zs(s.age_days.values) for _, s in sub.groupby("panel")])
            Tn = np.concatenate([zs(s.turnover_yr.values) for _, s in sub.groupby("panel")])
            y = np.concatenate([(s.MaxDD.values * 100.0) - (s.MaxDD.values * 100.0).mean()
                                for _, s in sub.groupby("panel")])
        else:
            A, Tn = zs(sub.age_days.values), zs(sub.turnover_yr.values)
            y = sub.MaxDD.values * 100.0
        ba, ta, r2a = ols(y, A[:, None])
        bt, tt, r2t = ols(y, Tn[:, None])
        bj, tj, r2j = ols(y, np.column_stack([A, Tn]))
        reg_rows.append(dict(scope=scope, n=len(sub), corr=float(np.corrcoef(A, Tn)[0, 1]),
                             b_age_uni=ba[1], t_age_uni=ta[1], R2_age=r2a,
                             b_turn_uni=bt[1], t_turn_uni=tt[1], R2_turn=r2t,
                             b_age_joint=bj[1], t_age_joint=tj[1],
                             b_turn_joint=bj[2], t_turn_joint=tj[2], R2_joint=r2j))

    for p, sub in bk.groupby("panel"):
        fit(f"panel {p}", sub, within_panel=False)
    for fam, sub in bk.groupby("family"):
        fit(f"family {fam} (3 panels)", sub)
    fit("POOLED (panel fixed effects)", bk)
    rg = pd.DataFrame(reg_rows)
    say(rg.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------- THE SAME REGRESSION AT EVERY COST RUNG ---------------------------
    say("\n  IS THE SIGN A COST ARTEFACT?  The same pooled regression at every cost rung "
        "(a brake lowers turnover, which LOWERS the cost drag, so a cost artefact would push "
        "MaxDD the OTHER way):")
    cost_rows = []
    for cb, sub in gd.groupby("cost_bps"):
        A = np.concatenate([zs(x.age_days.values) for _, x in sub.groupby("panel")])
        Tn = np.concatenate([zs(x.turnover_yr.values) for _, x in sub.groupby("panel")])
        y = np.concatenate([(x.MaxDD.values * 100.0) - (x.MaxDD.values * 100.0).mean()
                            for _, x in sub.groupby("panel")])
        ba, ta, r2a = ols(y, A[:, None])
        bt_, tt_, r2t = ols(y, Tn[:, None])
        bj, tj, r2j = ols(y, np.column_stack([A, Tn]))
        cost_rows.append(dict(cost_bps=cb, n=len(sub), b_age_uni=ba[1], t_age_uni=ta[1],
                              b_turn_uni=bt_[1], t_turn_uni=tt_[1], b_age_joint=bj[1],
                              t_age_joint=tj[1], b_turn_joint=bj[2], t_turn_joint=tj[2],
                              R2_joint=r2j))
    cr = pd.DataFrame(cost_rows)
    say(cr.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    for _, rw in cr.iterrows():
        reg_rows.append(dict(scope=f"POOLED @ {rw.cost_bps:.0f} bps (panel FE)", n=int(rw.n),
                             corr=np.nan, b_age_uni=rw.b_age_uni, t_age_uni=rw.t_age_uni,
                             R2_age=np.nan, b_turn_uni=rw.b_turn_uni, t_turn_uni=rw.t_turn_uni,
                             R2_turn=np.nan, b_age_joint=rw.b_age_joint,
                             t_age_joint=rw.t_age_joint, b_turn_joint=rw.b_turn_joint,
                             t_turn_joint=rw.t_turn_joint, R2_joint=rw.R2_joint))
    rg = pd.DataFrame(reg_rows)

    # ---------------- PAIRED BLOCK BOOTSTRAP -------------------------------------------
    say("\n  PAIRED CIRCULAR-BLOCK BOOTSTRAP of the tape (L = %d, %d reps, one block-start "
        "matrix per panel shared by every book): the REGRESSORS are held fixed and each book's "
        "MaxDD is recomputed on the resampled path." % (L_BOOT, BOOT_REPS))
    keys = {}
    mats = {}
    for pname, (net10, _, _) in boot_store.items():
        kk = sorted(net10.keys())
        keys[pname] = kk
        mats[pname] = np.vstack([net10[k] for k in kk])
    boot_coef = {k: [] for k in ("age_uni", "turn_uni", "age_joint", "turn_joint")}
    per_panel = {p: {k: [] for k in boot_coef} for p in keys}
    bidx = {p: block_index(mats[p].shape[1]) for p in keys}
    Zg = {}
    for p in keys:
        sub = bk[bk.panel == p].set_index(["family", "rung"])
        order = keys[p]
        Zg[p] = (np.array([sub.loc[k, "age_days"] for k in order], float),
                 np.array([sub.loc[k, "turnover_yr"] for k in order], float))
    for rep in range(BOOT_REPS):
        ys, As, Ts = [], [], []
        for p in keys:
            X = mats[p][:, bidx[p][rep]]
            y = mdd_rows(X) * 100.0
            a, t = zs(Zg[p][0]), zs(Zg[p][1])
            b1, _, _ = ols(y, a[:, None])
            b2, _, _ = ols(y, t[:, None])
            bj, _, _ = ols(y, np.column_stack([a, t]))
            per_panel[p]["age_uni"].append(b1[1])
            per_panel[p]["turn_uni"].append(b2[1])
            per_panel[p]["age_joint"].append(bj[1])
            per_panel[p]["turn_joint"].append(bj[2])
            ys.append(y - y.mean())
            As.append(a)
            Ts.append(t)
        y = np.concatenate(ys)
        A = np.concatenate(As)
        Tn = np.concatenate(Ts)
        b1, _, _ = ols(y, A[:, None])
        b2, _, _ = ols(y, Tn[:, None])
        bj, _, _ = ols(y, np.column_stack([A, Tn]))
        boot_coef["age_uni"].append(b1[1])
        boot_coef["turn_uni"].append(b2[1])
        boot_coef["age_joint"].append(bj[1])
        boot_coef["turn_joint"].append(bj[2])

    boot_rows = []
    def bstat(scope, d):
        for k, v in d.items():
            v = np.asarray(v, float)
            boot_rows.append(dict(scope=scope, coef=k, mean=v.mean(), sd=v.std(ddof=1),
                                  t=v.mean() / v.std(ddof=1) if v.std(ddof=1) > 0 else np.nan,
                                  lo95=np.percentile(v, 2.5), hi95=np.percentile(v, 97.5),
                                  share_neg=float((v < 0).mean())))
    for p in keys:
        bstat(f"panel {p}", per_panel[p])
    bstat("POOLED (panel fixed effects)", boot_coef)
    bt_df = pd.DataFrame(boot_rows)
    say(bt_df.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------- DELETE-ONE-CALENDAR-YEAR JACKKNIFE (second ruler) ----------------
    say("\n  DELETE-ONE-CALENDAR-YEAR JACKKNIFE (second ruler, no resampling): each book's "
        "MaxDD recomputed with one calendar year of the tape removed, the pooled regression "
        "re-fit, and the")
    say("  coefficient reported per deleted year.  This says whether a sign is one episode "
        "(2020, 2022) or the whole tape.")
    years = sorted(set(int(y) for y in panels[0].idx.year))
    jk_rows = []
    yr_map = {pan.name: np.array([d.year for d in pan.idx])[WARMUP:] for pan in panels}
    for y in years:
        ys, As, Ts, ok = [], [], [], True
        for p in keys:
            m = yr_map[p] != y
            if m.sum() < 500:
                ok = False
                break
            X = mats[p][:, m]
            yy = mdd_rows(X) * 100.0
            a, t = zs(Zg[p][0]), zs(Zg[p][1])
            ys.append(yy - yy.mean())
            As.append(a)
            Ts.append(t)
        if not ok:
            continue
        yv = np.concatenate(ys)
        A = np.concatenate(As)
        Tn = np.concatenate(Ts)
        b1, _, _ = ols(yv, A[:, None])
        b2, _, _ = ols(yv, Tn[:, None])
        bj, _, _ = ols(yv, np.column_stack([A, Tn]))
        jk_rows.append(dict(deleted_year=y, b_age_uni=b1[1], b_turn_uni=b2[1],
                            b_age_joint=bj[1], b_turn_joint=bj[2]))
    jk = pd.DataFrame(jk_rows)
    say(jk.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("  NOTE (a property of MaxDD, not a bug): deleting a year BEFORE the binding drawdown "
        "episode changes nothing at all, because removing it scales the whole later path by a "
        "constant and")
    say("  dd = e/cummax - 1 is invariant to that.  The identical rows are the years in which "
        "no book's MaxDD is set.")
    say(f"  SIGN STABILITY across the {len(jk)} delete-one-year fits: b_turn_joint positive at "
        f"{int((jk.b_turn_joint > 0).sum())} of {len(jk)}; b_age_joint positive at "
        f"{int((jk.b_age_joint > 0).sum())} of {len(jk)}.")
    jk.to_csv(f"{OUT}.jackknife.csv", index=False)

    # ---------------- RULE 8 WALK-FORWARD ----------------------------------------------
    say("\n" + "=" * 140)
    say("RULE 8 WALK-FORWARD — every chooser sees warm-up..2016-12-31 ONLY; 2017-2026 read ONCE.")
    say("  C_AGE / C_TURN are DIAL 2: the rung whose IS regression on that regressor predicts the "
        "SHALLOWEST MaxDD.  C_SHARPE is the record's habitual chooser, C_LIVE the incumbent.")
    say("=" * 140)
    g6_ok = True
    for pname, (net10, spy_p, live_p) in boot_store.items():
        pan = [p for p in panels if p.name == pname][0]
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        spyO = bmpack(pan.spy[i_oos:])
        lrO = bmpack(backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST_HEAD,
                              freq="W")["returns"].values[i_oos:])
        sub = bk[bk.panel == pname]
        for fam, s in sub.groupby("family"):
            s = s.copy()
            picks = {}
            picks["C_SHARPE"] = s.loc[s.IS_Sharpe.idxmax(), "rung"]
            for lab, xcol in (("C_AGE", "IS_age"), ("C_TURN", "IS_turnover")):
                x = zs(s[xcol].values)
                y = s.IS_MaxDD.values * 100.0
                b, _, _ = ols(y, x[:, None])
                pred = b[0] + b[1] * x
                picks[lab] = s.iloc[int(np.argmax(pred))]["rung"]
            liverung = {"F1_MINHOLD": f"H={I_H}", "F2_CAP": "cap=inf/CONV",
                        "F3_CADxH": f"W/H={I_H}", "F4_HYST": "Kout=20"}[fam]
            picks["C_LIVE"] = liverung
            for lab, rung in picks.items():
                row = s[s.rung == rung].iloc[0]
                wf_rows.append(dict(panel=pname, family=fam, chooser=lab, pick=rung,
                                    IS_Sharpe=row.IS_Sharpe, IS_age=row.IS_age,
                                    IS_turnover=row.IS_turnover, IS_MaxDD=row.IS_MaxDD,
                                    OOS_CAGR=row.OOS_CAGR, OOS_Sharpe=row.OOS_Sharpe,
                                    OOS_MaxDD=row.OOS_MaxDD, OOS_KEEP_4b=row.KEEP_4b_OOS,
                                    OOS_KEEP_4a=row.OOS_4a,
                                    SPY_OOS_CAGR=spyO["CAGR"], SPY_OOS_Sharpe=spyO["Sharpe"],
                                    SPY_OOS_MaxDD=spyO["MaxDD"],
                                    BASE_OOS_CAGR=lrO["CAGR"], BASE_OOS_Sharpe=lrO["Sharpe"],
                                    BASE_OOS_MaxDD=lrO["MaxDD"]))
    wf = pd.DataFrame(wf_rows)
    say(wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    gate("G6 the rule-8 chooser reads no row on or after 2017-01-01",
         "IS statistics sliced [WARMUP:i_oos] by construction", "no OOS leakage", g6_ok)

    # ---------------- HYPOTHESES --------------------------------------------------------
    say("\n" + "=" * 140)
    say("HYPOTHESES (pre-registered above, read here for the first time)")
    say("=" * 140)
    pool = rg[rg.scope == "POOLED (panel fixed effects)"].iloc[0]
    bp = bt_df[bt_df.scope == "POOLED (panel fixed effects)"].set_index("coef")
    h1 = bool(pool.b_age_uni < 0)
    say(f"  H1 SIGN       : pooled univariate b_age = {pool.b_age_uni:+.4f} pp / sd "
        f"(bootstrap t {bp.loc['age_uni','t']:+.2f}, 95% CI "
        f"[{bp.loc['age_uni','lo95']:+.3f}, {bp.loc['age_uni','hi95']:+.3f}]) -> "
        f"{'CONFIRMED' if h1 else 'FALSIFIED'} (older books draw down deeper)"
        if h1 else
        f"  H1 SIGN       : pooled univariate b_age = {pool.b_age_uni:+.4f} pp / sd -> FALSIFIED")
    ta_j, tt_j = bp.loc["age_joint", "t"], bp.loc["turn_joint", "t"]
    age_surv = bool(abs(ta_j) > BAR_T and np.sign(pool.b_age_joint) == np.sign(pool.b_age_uni))
    turn_surv = bool(abs(tt_j) > BAR_T)
    h2 = bool(age_surv and not turn_surv)
    say(f"  H2 SURVIVAL   : joint b_age {pool.b_age_joint:+.4f} (boot t {ta_j:+.2f}), "
        f"b_turn {pool.b_turn_joint:+.4f} (boot t {tt_j:+.2f}) -> AGE "
        f"{'SURVIVES' if age_surv else 'does NOT survive'}, TURNOVER "
        f"{'SURVIVES' if turn_surv else 'does NOT survive'} -> H2 "
        f"{'CONFIRMED' if h2 else 'FALSIFIED'}")
    say(f"  H3 SEPARABLE  : pooled corr(age, turnover) {rho_pool:+.4f}, VIF {vif:.2f} -> "
        f"{'SEPARABLE' if sep else 'NOT RESOLVABLE — the two axes are one axis on these families'}")
    inc_rows = bk[(bk.family == "F1_MINHOLD")]
    h4_tab = []
    for p, s in inc_rows.groupby("panel"):
        d1 = float(s[s.rung == "H=1"].MaxDD.iloc[0])
        d126 = float(s[s.rung == f"H={I_H}"].MaxDD.iloc[0])
        h4_tab.append((p, d1, d126, d126 - d1))
    h4 = all(x[3] > 0 for x in h4_tab)
    say("  H4 INCUMBENT  : MaxDD H=1 vs H=126 (positive delta = incumbent SHALLOWER): " +
        ", ".join(f"{p} {d1:.2%} -> {d126:.2%} ({dd*100:+.2f} pp)" for p, d1, d126, dd in h4_tab) +
        f" -> {'CONFIRMED' if h4 else 'FALSIFIED'}")
    n4b = int(wf.OOS_KEEP_4b.sum())
    age_wins = wf[wf.chooser == "C_AGE"].OOS_Sharpe.values
    turn_wins = wf[wf.chooser == "C_TURN"].OOS_Sharpe.values
    h5 = bool(n4b > 0 and np.mean(age_wins) > np.mean(turn_wins))
    say(f"  H5 RULE 8     : {n4b} of {len(wf)} chooser picks clear 4b OOS; mean OOS Sharpe "
        f"C_AGE {np.mean(age_wins):.4f} vs C_TURN {np.mean(turn_wins):.4f} vs "
        f"C_SHARPE {wf[wf.chooser=='C_SHARPE'].OOS_Sharpe.mean():.4f} vs "
        f"C_LIVE {wf[wf.chooser=='C_LIVE'].OOS_Sharpe.mean():.4f} -> "
        f"{'CONFIRMED' if h5 else 'FALSIFIED'}")
    n4a = int(gd.KEEP_4a.sum())
    say(f"  H6 4a         : {n4a} of {len(gd)} published grid points clear 4a -> "
        f"{'CONFIRMED' if n4a > 0 else 'FALSIFIED'}")
    say(f"  4b (FULL) at every cost rung: {int(gd.KEEP_4b.sum())} of {len(gd)} points; "
        f"at {COST_HEAD:.0f} bps alone: "
        f"{int(gd[gd.cost_bps==COST_HEAD].KEEP_4b.sum())} of "
        f"{len(gd[gd.cost_bps==COST_HEAD])}.  4b OOS: {int(gd.KEEP_4b_OOS.sum())} of {len(gd)}.")
    both = gd[(gd.KEEP_4b) & (gd.KEEP_4b_OOS)]
    say(f"  BOTH FULL AND OOS 4b: {len(both)} of {len(gd)} grid points.")
    if len(both):
        say(both.sort_values("Sharpe", ascending=False)
            .head(12)[["panel", "family", "rung", "cost_bps", "CAGR", "Sharpe", "MaxDD",
                       "age_days", "turnover_yr", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # G10 bit-identical recompute
    pan = panels[0]
    segs = segments_minhold(pan, I_N, I_H, "W")
    r2 = run_book(pan, segs)
    rr2 = (r2["gross_ret"] - r2["turn"] * COST_HEAD / 1e4)[WARMUP:]
    dev10 = max(abs(cagr(rr2) - head_cell[0]), abs(sharpe(rr2) - head_cell[1]),
                abs(mdd(rr2) - head_cell[2]))
    gate("G10 bit-identical recompute of the U56 headline cell", f"{dev10:.3e}", "== 0",
         dev10 == 0.0)

    # ---------------- write everything --------------------------------------------------
    gd.to_csv(f"{OUT}.grid.csv", index=False)
    bk.to_csv(f"{OUT}.books.csv", index=False)
    rg.to_csv(f"{OUT}.reg.csv", index=False)
    bt_df.to_csv(f"{OUT}.boot.csv", index=False)
    wf.to_csv(f"{OUT}.walkforward.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n  wrote {OUT.name}.grid.csv ({len(gd)} rows), .books.csv ({len(bk)}), .reg.csv "
        f"({len(rg)}), .boot.csv ({len(bt_df)}), .walkforward.csv ({len(wf)}), .jackknife.csv ({len(jk)}), .ladderends.csv ({len(ed)}), .gates.csv")
    say(f"  elapsed {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Idea 1538 (lane C, 2026-09-19) — is EXPOSURE-STATE DISAGREEMENT the THIRD LADDER AXIS, and is
TWO NUMBERS ENOUGH?

THE DEFECT THIS RUN REPAIRS.  Idea 1530 refuted the SCALE/COMPOSITION dichotomy (pooled R^2 of the
blend gap on 1 - OV_HOLD = 0.0154) and found, POST-HOC, that adding `flat_one` — the share of days
two adjacent rungs DISAGREE ABOUT BEING INVESTED AT ALL — lifts the fit to R^2 = 0.6094 and
collapses ladder identity's contribution from +0.3104 to +0.0053.  That reading is not a taxonomy:
of 1530's eight ladders, exactly ONE (the trailing equity stop, L_S) carries any flat_one at all
(mean 0.3190, max 0.5546); the next largest is the cadence ladder at mean 0.0015 and the other six
are identically ZERO.  A regressor fitted on one ladder's variation predicts that ladder, not the
axis.  This run BUILDS flat_one into THREE INDEPENDENT MECHANISMS and re-fits.

THE THREE FLAT-BEARING LADDERS (three different reasons a book goes to cash — this is the point:
if one number governs all three, it is an axis; if it governs only the one it was fitted on, it is
a description of the stop):

  L_S  stop depth      {None, 0.25, 0.15, 0.10}   OWN-EQUITY drawdown      (1530's only one)
  L_M  SPY MA macro    {None, 200, 150, 100}      INDEX PRICE vs its MA    (new)
  L_R  breadth gate    {None, 0.35, 0.50, 0.65}   CROSS-SECTIONAL breadth  (new)

THE FOURTH LADDER THE IDEA PROPOSED, PUBLISHED AS A NEGATIVE.  Idea 1538 also named "a MAXVOL rung
coarse enough to empty the book".  It cannot be built off this incumbent and the run says so with
numbers rather than omitting it:

  L_X  MAXVOL extreme  {0.60, 0.12, 0.08, 0.06}   ELIGIBILITY exhaustion

The min-hold H = 126 RETAINS a held name regardless of its eligibility, so emptying the book needs
every held name to age out in a stretch where nothing is eligible.  Pre-run probe on U56: the
eligible SET is empty on 0.0% of days at m = 0.15, 1.0% at 0.12, 2.5% at 0.10 — but the BOOK is
flat on 0.00% of days at every m down to 0.10 and only 1.39% at 0.08 and 0.06.  It is carried
anyway, at all four rungs, so the record owns the measurement.

THE FIVE NON-FLAT CONTROLS (carried over from 1530 unchanged, and needed: without them the
regression has no variation in the OVERLAP regressor at all):

  L_G  gross     {0.25, 0.50, 0.75, 1.00}      L_N  N        {10, 20, 30, 40}
  L_H  min-hold  {21, 63, 126, 252}            L_C  cadence  {W, 2W, M, Q}
  L_B  MA band   {0.00, 0.03, 0.06, 0.10}

9 ladders x 4 rungs = 36 rungs and 27 adjacent pairs per panel, x 3 blend weights = 81 blends;
117 cells per panel, 351 in all, EVERY ONE published in .grid.csv.  Every ladder contains the
frozen incumbent as one of its rungs (gate G2).  The ladder set and its rungs are ENUMERATED
from idea 1538's own text, not tuned.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4) — the same two as 1530, so the two runs are comparable:

  DIAL 1  BLEND WEIGHT lambda   {0.25, 0.50, 0.75}
  DIAL 2  OVERLAP STATISTIC     {OV_HOLD, OV_CAP}

THE GAP THE TWO NUMBERS MUST PREDICT (1530's definition, unchanged):
  D_lambda = Sharpe(blend) - [lambda*Sharpe(A) + (1-lambda)*Sharpe(B)]
with the blend built as REAL CAPITAL: two sleeves in a daily constant-mix split, pre-trade weights
taken at the ONE-DAY DRIFTED capital share so the cost of RESTORING the split is charged, and
blend turnover netted across sleeves.

PRE-REGISTERED BARS — written here BEFORE any number of this run was read, so the idea can fail.
Pooled over all 27 pairs x 3 panels = 81 pairs at lambda = 0.50, with y = D_sharpe and the TWO
regressors x1 = 1 - OV and x2 = flat_one:

  (T1) R^2 >= 0.80                                    [the bar idea 1538 names explicitly]
  (T2) adding LADDER IDENTITY (9 dummies) raises R^2 by < 0.05
  (T3) no ladder's mean residual from the two-number fit reaches |t| > 2
  (T4) LEAVE-ONE-LADDER-OUT: for EACH of the three flat-bearing ladders, fit the two numbers on
       the other eight ladders and predict the held-out one; out-of-ladder R^2 >= 0.50 on each.
       This is the test 1530 could not run and the reason this run exists: a rule fitted without
       ever seeing the stop must still price the stop.
  (T5) RULE 8 ON THE RULE ITSELF: coefficients fit on the IS gaps (warm-up..2016-12-31) ONLY, the
       2017-2026 gaps read ONCE, OOS R^2 >= 0.80.

TWO NUMBERS ARE ENOUGH iff T1 & T2 & T3 & T4 & T5.  Any of them failing is a finding against the
idea's own hypothesis and is recorded as one.  The one-number (overlap-only) fit is reported beside
every two-number fit for continuity with 1530's committed 0.0154 / 0.6094.

THE CAPITAL ARM (what a prediction rule is worth in money).  Every rung and every blend is a real
book.  Both KEEP paths are evaluated at all 351 cells against the live RULES v2 baseline AND SPY,
on the full sample and on the 2017-2026 OOS window, and the rule-8 chooser (argmax IS Sharpe on
warm-up..2016-12-31 only) is scored OOS against the frozen incumbent, RULES v2 and SPY.

PROTOCOL: rule 1 (>= 10y); rule 2 (t+1, 10 bps, no leverage, no shorting — every gate DE-GROSSES
to cash and never levers); rule 3 (RULES v2 AND SPY); rule 4 (both KEEP paths, exactly 2 tuned
parameters); rule 8 (walk-forward, 2017-2026 read ONCE); rule 9 (survivorship stated).
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

GATES.  G0 sample >= 10y.  G1 CROSS-SCRIPT REPLAY of the committed 2026-09-04 U56 anchor
(15.80% / 1.1537 / -19.13% full; 1.1857 OOS).  G2 the anchor rung is BIT-IDENTICAL on all 9
ladders.  G3 all 351 cells published.  G4 exactly two tuned parameters.  G5 the rule-8 chooser
reads no row on or after 2017-01-01.  G6 no leverage.  G7 1509's MECHANISM REPLAYED (the
lambda-blend of gross 0.50 and 1.00 equals the single gross rung at the blended exposure).
G8 netted blend turnover <= naive + split-restoration at every row.  G9 the stop, the SPY macro
gate and the breadth gate are NON-ANTICIPATING (truncated-tape replay is bit-identical).
G10 deterministic recompute of one cell per panel.  G12 the enactable TWO-STATE
GROSS wording of the incidental KEEP-4b candidate reproduces the two-sleeve blend it was found as.
G11 THE BUILD GATE — all THREE intended
flat-bearing ladders carry mean flat_one >= 0.02 on every panel.  Without G11 this run is 1530's
single-ladder fit again and cannot answer the question it was filed for.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-19_exposure-state-disagreement-third-ladder-axis_C.py
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
SLUG = "exposure-state-disagreement-third-ladder-axis"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP = 260
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G, I_V, I_B, I_C = 20, 126, 0.75, 0.60, 0.00, "W"   # the frozen incumbent
COST = 10.0
OOS_START, IS_END = "2017-01-01", "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LAMBDAS = [0.25, 0.50, 0.75]                     # DIAL 1
OVSTATS = ["OV_HOLD", "OV_CAP"]                  # DIAL 2
BOOT_REPS, BOOT_BLOCK, BOOT_SEED = 400, 63, 20260919
C_U56 = dict(CAGR=0.1580, Sharpe=1.1537, MaxDD=-0.1913, oSharpe=1.1857)

R2_BAR, DR2_BAR, T_BAR, LOLO_BAR, OOS_R2_BAR = 0.80, 0.05, 2.0, 0.50, 0.80

LADDERS = {
    # flat-bearing: three independent reasons a book goes to cash
    "L_S": dict(dial="stop",   rungs=[None, 0.25, 0.15, 0.10],   flat="INTENDED own-equity DD"),
    "L_M": dict(dial="macro",  rungs=[None, 200, 150, 100],      flat="INTENDED SPY price vs MA"),
    "L_R": dict(dial="breadth", rungs=[None, 0.35, 0.50, 0.65],  flat="INTENDED cross-sec breadth"),
    # proposed by idea 1538, published as a negative
    "L_X": dict(dial="maxvol", rungs=[0.60, 0.12, 0.08, 0.06],   flat="PROPOSED eligibility"),
    # non-flat controls (1530's, unchanged)
    "L_G": dict(dial="gross",  rungs=[0.25, 0.50, 0.75, 1.00],   flat="none (scale)"),
    "L_N": dict(dial="N",      rungs=[10, 20, 30, 40],           flat="none (composition)"),
    "L_H": dict(dial="H",      rungs=[21, 63, 126, 252],         flat="none (composition)"),
    "L_C": dict(dial="cadence", rungs=["W", "2W", "M", "Q"],     flat="none (composition)"),
    "L_B": dict(dial="band",   rungs=[0.00, 0.03, 0.06, 0.10],   flat="none (composition)"),
}
FLAT_LADDERS = ["L_S", "L_M", "L_R"]

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


# ---------------------------------------------------------------------------------------------
# statistics
# ---------------------------------------------------------------------------------------------
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


def paired_block_dsharpe(a, b, reps=BOOT_REPS, L=BOOT_BLOCK, seed=BOOT_SEED):
    a, b = np.asarray(a, float), np.asarray(b, float)
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    nb = int(np.ceil(n / L))
    rng = np.random.default_rng(seed)
    starts = rng.integers(0, n, size=(reps, nb))
    idx = (starts[:, :, None] + np.arange(L)[None, None, :]).reshape(reps, nb * L)[:, :n] % n
    A, B = a[idx], b[idx]

    def sh(X):
        v = X.std(axis=1, ddof=0) * np.sqrt(252)
        return np.where(v > 0, X.mean(axis=1) * 252 / v, np.nan)

    d = sh(A) - sh(B)
    obs = float(sharpe(a) - sharpe(b))
    se = float(np.nanstd(d, ddof=1))
    return obs, se, (obs / se if se > 0 else np.nan)


def ols(X, y):
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    fit = X @ beta
    resid = y - fit
    ss_t = float(((y - y.mean()) ** 2).sum())
    r2 = 1.0 - float((resid ** 2).sum()) / ss_t if ss_t > 0 else np.nan
    return beta, resid, r2


def r2_against(y, pred):
    """R^2 of an EXTERNAL prediction (not a fit): 1 - SSE/SST about y's own mean.  It can go
    negative, which is the honest reading when a rule fitted elsewhere mis-prices a ladder."""
    y = np.asarray(y, float)
    p = np.asarray(pred, float)
    ss_t = float(((y - y.mean()) ** 2).sum())
    return 1.0 - float(((y - p) ** 2).sum()) / ss_t if ss_t > 0 else np.nan


# ---------------------------------------------------------------------------------------------
# the panel and the selection frame
# ---------------------------------------------------------------------------------------------
def mech_legs(q: pd.DataFrame):
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return (sum(parts) / len(parts)).values


def band_gate(q: pd.DataFrame, band: float):
    ma = q.rolling(200).mean()
    if band <= 0.0:
        return (q > ma).values
    raw = pd.DataFrame(np.nan, index=q.index, columns=q.columns)
    raw = raw.mask(q > ma * (1 + band), 1.0).mask(q < ma * (1 - band), 0.0)
    return (raw.ffill().fillna(0.0) > 0.5).values


def cadence_rows(idx, cad):
    if cad == "2W":
        m = rebalance_mask(idx, "W").values.copy()
        on = np.flatnonzero(m)
        m[:] = False
        m[on[::2]] = True
        m = pd.Series(m, index=idx)
    else:
        m = rebalance_mask(idx, cad)
    v = m.shift(1, fill_value=False).values.copy()
    v[0] = True
    return np.flatnonzero(v)


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        self.spy_px = px["SPY"]
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        q = px[invest]
        self.q = q
        self.comp = mech_legs(q)
        self.vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
        self._gate, self._reb = {}, {}
        # the two NEW exposure-state devices, both read with a one-day lag so the rebalance row t
        # (which already carries the t-1 decision, see cadence_rows) uses data through t-1 only.
        ab = (q > q.rolling(200).mean())
        self.breadth = (ab.sum(axis=1) / q.notna().sum(axis=1).replace(0, np.nan)).shift(1).values

    def gate_of(self, band):
        if band not in self._gate:
            self._gate[band] = band_gate(self.q, band)
        return self._gate[band]

    def reb_of(self, cad):
        if cad not in self._reb:
            self._reb[cad] = cadence_rows(self.idx, cad)
        return self._reb[cad]

    def macro_of(self, spec, nrows=None):
        """The daily INVESTED/FLAT state, True = invested.  None on both dials -> always True."""
        T = len(self.idx) if nrows is None else nrows
        if spec["macro"] is None and spec["breadth"] is None:
            return np.ones(T, bool)
        if spec["macro"] is not None:
            s = self.spy_px.iloc[:T]
            g = (s > s.rolling(int(spec["macro"])).mean()).shift(1).fillna(False).values
            return g.astype(bool)
        b = self.breadth[:T]
        return np.nan_to_num(b, nan=-1.0) > float(spec["breadth"])

    def frame_inputs(self, band, maxvol):
        above = self.gate_of(band)
        elig = above & (np.nan_to_num(self.vol20, nan=1e9) < maxvol)
        sc = self.comp * (0.5 + 0.5 * above.astype(float))
        key = np.where(np.isfinite(sc), -sc, np.inf)
        return elig, key


def build_frame(pan, elig, key, reb, N, H, lag=1, nrows=None):
    T = pan.rets.shape[0] if nrows is None else nrows
    M = pan.rets.shape[1]
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    reb = reb[reb < T]
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
            k = key[ts].copy()
            k[~(elig[ts] & pr[ts])] = np.inf
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


def run_rung(pan, frame, reb, g, stop=None, macro=None, nrows=None):
    """The daily engine (1530's run_rung, with the vol target replaced by the macro/breadth gate:
    both are DE-GROSS-TO-CASH devices and neither ever levers)."""
    T = pan.rets.shape[0] if nrows is None else nrows
    M = pan.rets.shape[1]
    rets = pan.rets
    isreb = np.zeros(T, bool)
    isreb[reb[reb < T]] = True
    Wpre = np.zeros((T, M))
    Wpost = np.zeros((T, M))
    rg = np.zeros(T)
    turn = np.zeros(T)
    rnet = np.zeros(T)
    scale = np.zeros(T)
    cur = np.zeros(M)
    eq, peak = 1.0, 1.0
    wsum_max = 0.0
    for t in range(T):
        Wpre[t] = cur
        if isreb[t]:
            gt = g
            if stop is not None and eq < peak * (1.0 - stop):
                gt = 0.0                                   # reads equity through t-1 only
            if macro is not None and not macro[t]:
                gt = 0.0                                   # reads prices through t-1 only
            post = gt * frame[t]
        else:
            gt = scale[t - 1] if t else 0.0
            post = cur
        scale[t] = gt
        Wpost[t] = post
        turn[t] = float(np.abs(post - cur).sum())
        wsum_max = max(wsum_max, float(post.sum()))
        r = float(post @ rets[t])
        rg[t] = r
        rnet[t] = r - turn[t] * COST / 1e4
        eq *= 1.0 + rnet[t]
        peak = max(peak, eq)
        cur = post * (1.0 + rets[t]) / (1.0 + r)
    return dict(Wpre=Wpre, Wpost=Wpost, rg=rg, turn=turn, rnet=rnet, wsum=wsum_max)


def run_rung_varg(pan, frame, reb, gseq):
    """run_rung with a per-row gross SEQUENCE instead of a scalar.  Used ONLY by gate G12, to check
    that the enactable RULES wording of the incidental KEEP-4b candidate (a TWO-STATE GROSS) really
    reproduces the two-sleeve blend it was found as."""
    T, M = pan.rets.shape
    isreb = np.zeros(T, bool)
    isreb[reb] = True
    cur = np.zeros(M)
    rnet = np.zeros(T)
    turn = np.zeros(T)
    sc = np.zeros(T)
    for t in range(T):
        if isreb[t]:
            gt = float(gseq[t])
            post = gt * frame[t]
        else:
            gt = sc[t - 1] if t else 0.0
            post = cur
        sc[t] = gt
        tr = float(np.abs(post - cur).sum())
        r = float(post @ pan.rets[t])
        rnet[t] = r - tr * COST / 1e4
        turn[t] = tr
        cur = post * (1.0 + pan.rets[t]) / (1.0 + r)
    return dict(rnet=rnet, turn=turn)


def blend(A, B, lam):
    rA, rB = A["rnet"], B["rnet"]
    prevA = np.concatenate([[0.0], rA[:-1]])
    prevB = np.concatenate([[0.0], rB[:-1]])
    num = lam * (1.0 + prevA)
    s = num / (num + (1.0 - lam) * (1.0 + prevB))
    Wpre = s[:, None] * A["Wpre"] + (1.0 - s)[:, None] * B["Wpre"]
    Wpost = lam * A["Wpost"] + (1.0 - lam) * B["Wpost"]
    turn_net = np.abs(Wpost - Wpre).sum(axis=1)
    turn_naive = lam * A["turn"] + (1.0 - lam) * B["turn"]
    Wpre_lam = lam * A["Wpre"] + (1.0 - lam) * B["Wpre"]
    turn_rest = np.abs(Wpre_lam - Wpre).sum(axis=1)
    rgross = lam * A["rg"] + (1.0 - lam) * B["rg"]
    return dict(rnet=rgross - turn_net * COST / 1e4,
                rnet_naive=rgross - turn_naive * COST / 1e4,
                turn=turn_net, turn_naive=turn_naive, turn_rest=turn_rest,
                wsum=float(Wpost.sum(axis=1).max()))


def overlaps(A, B, start):
    a, b = A["Wpost"][start:], B["Wpost"][start:]
    sa, sb = a.sum(axis=1), b.sum(axis=1)
    both = (sa > 1e-12) & (sb > 1e-12)
    na = np.zeros_like(a)
    nb = np.zeros_like(b)
    na[both] = a[both] / sa[both, None]
    nb[both] = b[both] / sb[both, None]
    ov_hold = float(np.minimum(na[both], nb[both]).sum(axis=1).mean()) if both.any() else np.nan
    cap = np.minimum(a, b).sum(axis=1)
    den = np.maximum(sa, sb)
    ov_cap_row = np.where(den > 1e-12, cap / np.maximum(den, 1e-300), 1.0)
    ov_cap = float(ov_cap_row.mean())
    flat_one = float((((sa > 1e-12) ^ (sb > 1e-12))).mean())
    ja = a > 1e-12
    jb = b > 1e-12
    inter = (ja & jb).sum(axis=1)
    union = (ja | jb).sum(axis=1)
    jac = float(np.where(union > 0, inter / np.maximum(union, 1), 1.0).mean())
    return ov_hold, ov_cap, flat_one, jac


def rung_spec(ladder, v):
    """The frozen incumbent with exactly ONE dial moved."""
    s = dict(N=I_N, H=I_H, g=I_G, maxvol=I_V, band=I_B, cad=I_C,
             stop=None, macro=None, breadth=None)
    d = LADDERS[ladder]["dial"]
    s[{"gross": "g", "stop": "stop", "macro": "macro", "breadth": "breadth", "N": "N", "H": "H",
       "cadence": "cad", "maxvol": "maxvol", "band": "band"}[d]] = v
    return s


def is_anchor(s):
    return (s["N"] == I_N and s["H"] == I_H and s["g"] == I_G and s["maxvol"] == I_V
            and s["band"] == I_B and s["cad"] == I_C and s["stop"] is None
            and s["macro"] is None and s["breadth"] is None)


def build_rung(pan, s, nrows=None):
    elig, key = pan.frame_inputs(s["band"], s["maxvol"])
    reb = pan.reb_of(s["cad"])
    frame = build_frame(pan, elig, key, reb, s["N"], s["H"], nrows=nrows)
    macro = None
    if s["macro"] is not None or s["breadth"] is not None:
        macro = pan.macro_of(s, nrows=nrows)
    return run_rung(pan, frame, reb, s["g"], stop=s["stop"], macro=macro, nrows=nrows)


# ---------------------------------------------------------------------------------------------
def main():
    t0 = time.time()
    say("=" * 124)
    say("IDEA 1538 (lane C, 2026-09-19) — is EXPOSURE-STATE DISAGREEMENT the THIRD LADDER AXIS, "
        "and is TWO NUMBERS ENOUGH?")
    say("9 ladders x 4 rungs = 36 rungs and 27 adjacent pairs per panel x 3 blend weights = 81 "
        "blends -> 117 cells per panel, 351 in all, every one published.")
    say("THREE INDEPENDENT flat-bearing mechanisms built (L_S own-equity DD, L_M SPY price vs MA, "
        "L_R cross-sectional breadth); L_X (MAXVOL) published as the negative.")
    say("DIAL 1 blend weight lambda {0.25,0.50,0.75};  DIAL 2 overlap statistic {OV_HOLD, OV_CAP}.")
    say(f"PRE-REGISTERED: T1 R^2>={R2_BAR}; T2 dR^2<{DR2_BAR}; T3 no ladder |t|>{T_BAR}; "
        f"T4 leave-one-ladder-out R^2>={LOLO_BAR} on each of the 3 flat ladders; "
        f"T5 rule-8 OOS R^2>={OOS_R2_BAR}.")
    say("=" * 124)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    say(f"  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0; {len(inv)} investable names survive.")

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, SMALL {len(inv)}.")
    say("  SURVIVORSHIP (rule 9): U56 and B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010, so every ABSOLUTE level below is an UPPER BOUND.  "
        "What this run reads is a CONTRAST between two books over the SAME names on the SAME days "
        "(a blend against its own two rungs), which the bias cannot manufacture.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y)")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)", round(min(len(p.idx) for p in panels) / 252.0, 2),
         ">= 10.0", min(len(p.idx) for p in panels) / 252.0 >= 10.0)
    gate("G4 exactly two tuned parameters (blend weight lambda, overlap statistic)", 2, "== 2",
         True)

    grid, pairs, wf_rows = [], [], []
    wsum_global, g1_ok = 0.0, None
    anchor_dev, g8_viol, g9_dev, g10_dev, g7_dev = 0.0, 0, 0.0, 0.0, 0.0
    g12_dev = 0.0
    anchor_seen = {}
    rest_bp, netnaive_bp, n_blend = [], [], 0

    for pan in panels:
        T = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        i_is = int(np.searchsorted(pan.idx.values, np.datetime64(IS_END)))
        spy, spyO = bmpack(pan.spy[WARMUP:]), bmpack(pan.spy[i_oos:])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])

        say(f"\n  [{pan.name}]  SPY CAGR {spy['CAGR']:.2%} Sharpe {spy['Sharpe']:.4f} MaxDD "
            f"{spy['MaxDD']:.2%} H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f}  |  4b bars: DD cap "
            f"{DD_CAP*spy['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps CAGR {live['CAGR']:.2%} Sharpe {live['Sharpe']:.4f} "
            f"MaxDD {live['MaxDD']:.2%} H1/H2 {live['H1']:.3f}/{live['H2']:.3f}")
        say(f"           OOS SPY {spyO['CAGR']:.2%}/{spyO['Sharpe']:.4f}/{spyO['MaxDD']:.2%}  |  "
            f"OOS RULES v2 {liveO['CAGR']:.2%}/{liveO['Sharpe']:.4f}/{liveO['MaxDD']:.2%}")

        A0 = build_rung(pan, rung_spec("L_G", I_G))
        anch = A0["rnet"]
        am, ao = triple(anch[WARMUP:]), triple(anch[i_oos:])
        ah1, ah2 = halves(anch[WARMUP:])
        say(f"           FROZEN INCUMBENT  CAGR {am['CAGR']:.2%} Sharpe {am['Sharpe']:.4f} MaxDD "
            f"{am['MaxDD']:.2%} H1/H2 {ah1:.4f}/{ah2:.4f} | OOS {ao['CAGR']:.2%}/"
            f"{ao['Sharpe']:.4f}/{ao['MaxDD']:.2%}")
        if pan.name == "U56":
            d = max(abs(am["Sharpe"] - C_U56["Sharpe"]), abs(ao["Sharpe"] - C_U56["oSharpe"]),
                    abs(am["CAGR"] - C_U56["CAGR"]), abs(am["MaxDD"] - C_U56["MaxDD"]))
            g1_ok = gate("G1 cross-script replay of the committed 2026-09-04 U56 anchor "
                         "(15.80%/1.1537/-19.13% full; 1.1857 OOS)",
                         f"max |dev| {d:.2e} (got {am['CAGR']:.4f}/{am['Sharpe']:.4f}/"
                         f"{am['MaxDD']:.4f}; OOS {ao['Sharpe']:.4f})", "< 5e-3", d < 5e-3)
        del A0

        def cell(name, ladder, kind, rung_a, rung_b, lam, r, turn, extra):
            k4a, k4b, m, h1, h2, legs = keep_paths(r[WARMUP:], spy, live)
            k4aO, k4bO, mo, _, _, legsO = keep_paths(r[i_oos:], spyO, liveO)
            dsh, se, tt = paired_block_dsharpe(r[WARMUP:], anch[WARMUP:])
            dshO, seO, tO = paired_block_dsharpe(r[i_oos:], anch[i_oos:])
            ty = float(np.sum(turn[WARMUP:]) * 252.0 / (T - WARMUP))
            row = dict(panel=pan.name, ladder=ladder, flat_class=LADDERS[ladder]["flat"],
                       kind=kind, rung_a=str(rung_a), rung_b=str(rung_b), lam=lam,
                       CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                       turnover_yr=ty, cost_bp_yr=ty * COST,
                       dCAGR_pp=(m["CAGR"] - am["CAGR"]) * 100.0, dSharpe=dsh,
                       dSharpe_se=se, dSharpe_t=tt,
                       dMaxDD_pp=(m["MaxDD"] - am["MaxDD"]) * 100.0,
                       oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                       odSharpe=dshO, odSharpe_t=tO,
                       odCAGR_pp=(mo["CAGR"] - ao["CAGR"]) * 100.0,
                       keep4a=k4a, keep4b=k4b, keep4a_OOS=k4aO, keep4b_OOS=k4bO,
                       leg_H1=legs["H1"], leg_H2=legs["H2"], leg_DD=legs["DD"],
                       leg_CAGR=legs["CAGR"], legO_H1=legsO["H1"], legO_H2=legsO["H2"],
                       legO_DD=legsO["DD"], legO_CAGR=legsO["CAGR"],
                       is_Sharpe=sharpe(r[WARMUP:i_is]), is_CAGR=cagr(r[WARMUP:i_is]),
                       name=name)
            row.update(extra)
            grid.append(row)
            return row

        for lad, spec in LADDERS.items():
            rungs = spec["rungs"]
            prev = None
            for j, v in enumerate(rungs):
                s = rung_spec(lad, v)
                R = build_rung(pan, s)
                wsum_global = max(wsum_global, R["wsum"])
                if is_anchor(s):
                    anchor_dev = max(anchor_dev, float(np.max(np.abs(R["rnet"] - anch))))
                    anchor_seen.setdefault(pan.name, set()).add(lad)
                flat_rung = float((R["Wpost"][WARMUP:].sum(axis=1) <= 1e-12).mean())
                cell(f"{lad}={v}", lad, "RUNG", v, "", np.nan, R["rnet"], R["turn"],
                     dict(ov_hold=np.nan, ov_cap=np.nan, flat_one=np.nan, jaccard=np.nan,
                          D_sharpe=np.nan, D_cagr=np.nan, turn_naive_yr=np.nan,
                          D_sharpe_IS=np.nan, D_sharpe_OOS=np.nan,
                          flat_share=flat_rung, is_anchor=is_anchor(s)))
                if prev is not None:
                    ovh, ovc, flat1, jac = overlaps(prev, R, WARMUP)
                    shA = sharpe(prev["rnet"][WARMUP:])
                    shB = sharpe(R["rnet"][WARMUP:])
                    shA_i, shB_i = sharpe(prev["rnet"][WARMUP:i_is]), sharpe(R["rnet"][WARMUP:i_is])
                    shA_o, shB_o = sharpe(prev["rnet"][i_oos:]), sharpe(R["rnet"][i_oos:])
                    cgA, cgB = cagr(prev["rnet"][WARMUP:]), cagr(R["rnet"][WARMUP:])
                    ovh_i, ovc_i, flat1_i, _ = overlaps(
                        {"Wpost": prev["Wpost"][:i_is]}, {"Wpost": R["Wpost"][:i_is]}, WARMUP)
                    ovh_o, ovc_o, flat1_o, _ = overlaps(
                        {"Wpost": prev["Wpost"][i_oos:]}, {"Wpost": R["Wpost"][i_oos:]}, 0)
                    for lam in LAMBDAS:
                        Bl = blend(prev, R, lam)
                        wsum_global = max(wsum_global, Bl["wsum"])
                        if (Bl["turn"] - Bl["turn_naive"] - Bl["turn_rest"]).max() > 1e-9:
                            g8_viol += 1
                        n_blend += 1
                        rest_bp.append(float(np.sum(Bl["turn_rest"][WARMUP:])
                                             * 252.0 / (T - WARMUP)) * COST)
                        netnaive_bp.append(float(np.sum(Bl["turn"][WARMUP:] -
                                                        Bl["turn_naive"][WARMUP:])
                                                 * 252.0 / (T - WARMUP)) * COST)
                        rb = Bl["rnet"]
                        Dsh = sharpe(rb[WARMUP:]) - (lam * shA + (1 - lam) * shB)
                        Dcg = cagr(rb[WARMUP:]) - (lam * cgA + (1 - lam) * cgB)
                        Dsh_i = sharpe(rb[WARMUP:i_is]) - (lam * shA_i + (1 - lam) * shB_i)
                        Dsh_o = sharpe(rb[i_oos:]) - (lam * shA_o + (1 - lam) * shB_o)
                        tn = float(np.sum(Bl["turn_naive"][WARMUP:]) * 252.0 / (T - WARMUP))
                        cr = cell(f"{lad} blend {rungs[j-1]}|{v} @{lam:.2f}", lad, "BLEND",
                                  rungs[j - 1], v, lam, rb, Bl["turn"],
                                  dict(ov_hold=ovh, ov_cap=ovc, flat_one=flat1, jaccard=jac,
                                       D_sharpe=Dsh, D_cagr=Dcg, turn_naive_yr=tn,
                                       D_sharpe_IS=Dsh_i, D_sharpe_OOS=Dsh_o,
                                       flat_share=np.nan, is_anchor=False))
                        pairs.append(dict(panel=pan.name, ladder=lad, flat_class=spec["flat"],
                                          rung_a=str(rungs[j - 1]), rung_b=str(v), lam=lam,
                                          ov_hold=ovh, ov_cap=ovc, jaccard=jac, flat_one=flat1,
                                          ov_hold_IS=ovh_i, ov_cap_IS=ovc_i, flat_one_IS=flat1_i,
                                          ov_hold_OOS=ovh_o, ov_cap_OOS=ovc_o,
                                          flat_one_OOS=flat1_o,
                                          Sharpe_A=shA, Sharpe_B=shB,
                                          Sharpe_blend=sharpe(rb[WARMUP:]),
                                          D_sharpe=Dsh, D_cagr=Dcg,
                                          D_sharpe_IS=Dsh_i, D_sharpe_OOS=Dsh_o,
                                          turn_net_yr=cr["turnover_yr"], turn_naive_yr=tn))
                        if lad == "L_G" and rungs[j - 1] == 0.50 and v == 1.00:
                            gex = lam * 0.50 + (1 - lam) * 1.00
                            Rx = build_rung(pan, rung_spec("L_G", gex))
                            g7_dev = max(g7_dev,
                                         abs(sharpe(Rx["rnet"][WARMUP:]) - sharpe(rb[WARMUP:])))
                            del Rx
                    del prev
                prev = R
            del prev
            say(f"    [{pan.name}] {lad} done ({len(grid)} cells, {time.time()-t0:.0f}s)")

        # ---- G12 the enactable RULES wording of the L_M blend is a TWO-STATE GROSS ----------
        # Both sleeves of an L_M blend share ONE selection frame, so lam*A + (1-lam)*B holds the
        # same names at a gross of g when SPY is above its MA and lam*g when it is below.  The two
        # are not bit-identical -- the cash sleeve does not drift with the book intraweek -- so the
        # gap is MEASURED and published rather than asserted away.
        s0 = rung_spec("L_M", None)
        e0, k0 = pan.frame_inputs(s0["band"], s0["maxvol"])
        rb0 = pan.reb_of(s0["cad"])
        fr0 = build_frame(pan, e0, k0, rb0, s0["N"], s0["H"])
        mac = pan.macro_of(rung_spec("L_M", 200))
        for lam in LAMBDAS:
            Ax = run_rung(pan, fr0, rb0, I_G)
            Bx = run_rung(pan, fr0, rb0, I_G, macro=mac)
            blx = blend(Ax, Bx, lam)
            vg = run_rung_varg(pan, fr0, rb0, np.where(mac, I_G, lam * I_G))
            d = abs(sharpe(blx["rnet"][WARMUP:]) - sharpe(vg["rnet"][WARMUP:]))
            g12_dev = max(g12_dev, d)
            if abs(lam - 0.75) < 1e-9 and pan.name == "U56":
                say(f"    G12 [{pan.name}] lam 0.75 blend {cagr(blx['rnet'][WARMUP:]):.4%}/"
                    f"{sharpe(blx['rnet'][WARMUP:]):.4f}/{mdd(blx['rnet'][WARMUP:]):.4%} vs "
                    f"two-state gross {I_G:.4f}/{lam*I_G:.4f} "
                    f"{cagr(vg['rnet'][WARMUP:]):.4%}/{sharpe(vg['rnet'][WARMUP:]):.4f}/"
                    f"{mdd(vg['rnet'][WARMUP:]):.4%}  (OOS {cagr(vg['rnet'][i_oos:]):.4%}/"
                    f"{sharpe(vg['rnet'][i_oos:]):.4f}/{mdd(vg['rnet'][i_oos:]):.4%})")
            del Ax, Bx, blx, vg
        del fr0

        # ---- G9 causality of the THREE equity/market-reading devices ------------------------
        for lad, v in (("L_S", 0.15), ("L_M", 150), ("L_R", 0.50)):
            full = build_rung(pan, rung_spec(lad, v))
            trunc = build_rung(pan, rung_spec(lad, v), nrows=i_oos)
            g9_dev = max(g9_dev, float(np.max(np.abs(full["rnet"][:i_oos] - trunc["rnet"]))))
            del full, trunc

        # ---- G10 deterministic recompute ----------------------------------------------------
        R2 = build_rung(pan, rung_spec("L_M", 150))
        ref = [x for x in grid if x["panel"] == pan.name and x["name"] == "L_M=150"][0]
        g10_dev = max(g10_dev, abs(sharpe(R2["rnet"][WARMUP:]) - ref["Sharpe"]))
        del R2

        # ---- rule 8 capital arm --------------------------------------------------------------
        cand = [x for x in grid if x["panel"] == pan.name]
        for tag, pool in (("ARGMAX-IS (all 117 cells)", cand),
                          ("ARGMAX-IS (blends only)", [x for x in cand if x["kind"] == "BLEND"]),
                          ("ARGMAX-IS (flat ladders only)",
                           [x for x in cand if x["ladder"] in FLAT_LADDERS]),
                          ("DO NOTHING (frozen incumbent)",
                           [x for x in cand if x.get("is_anchor")])):
            pick = max(pool, key=lambda x: (-1e9 if not np.isfinite(x["is_Sharpe"])
                                            else x["is_Sharpe"]))
            wf_rows.append(dict(
                panel=pan.name, chooser=tag, cell=pick["name"], ladder=pick["ladder"],
                kind=pick["kind"], lam=pick["lam"], IS_Sharpe=pick["is_Sharpe"],
                OOS_CAGR=pick["oCAGR"], OOS_Sharpe=pick["oSharpe"], OOS_MaxDD=pick["oMaxDD"],
                FULL_CAGR=pick["CAGR"], FULL_Sharpe=pick["Sharpe"], FULL_MaxDD=pick["MaxDD"],
                FULL_H1=pick["H1"], FULL_H2=pick["H2"],
                anchor_OOS_CAGR=ao["CAGR"], anchor_OOS_Sharpe=ao["Sharpe"],
                anchor_OOS_MaxDD=ao["MaxDD"],
                spy_OOS_CAGR=spyO["CAGR"], spy_OOS_Sharpe=spyO["Sharpe"],
                spy_OOS_MaxDD=spyO["MaxDD"], live_OOS_CAGR=liveO["CAGR"],
                live_OOS_Sharpe=liveO["Sharpe"], live_OOS_MaxDD=liveO["MaxDD"],
                odSharpe=pick["odSharpe"], odSharpe_t=pick["odSharpe_t"],
                keep4a=pick["keep4a"], keep4b=pick["keep4b"],
                keep4a_OOS=pick["keep4a_OOS"], keep4b_OOS=pick["keep4b_OOS"],
                ov_hold=pick["ov_hold"], flat_one=pick["flat_one"], D_sharpe=pick["D_sharpe"]))

    G = pd.DataFrame(grid)
    P = pd.DataFrame(pairs)
    W = pd.DataFrame(wf_rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    P.to_csv(f"{OUT}.pairs.csv", index=False)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)

    gate("G3 all 351 cells published (3 panels x [36 rungs + 27 pairs x 3 lambdas])",
         len(G), "== 351", len(G) == 351)
    gate("G2 the anchor rung is bit-identical on every ladder that contains it "
         f"({sorted(anchor_seen.get('U56', set()))})",
         f"max |dret| {anchor_dev:.3e} over {min(len(v) for v in anchor_seen.values())} ladders/panel",
         "< 1e-12 on all 9 ladders",
         anchor_dev < 1e-12 and all(len(v) == 9 for v in anchor_seen.values()))
    gate("G6 no leverage: max realised weight sum over every rung and every blend",
         f"{wsum_global:.6f}", "<= 1.0 + 1e-9", wsum_global <= 1.0 + 1e-9)
    gate("G7 1509's MECHANISM REPLAYED: the lambda-blend of gross 0.50 and 1.00 equals the single "
         "gross rung at the blended exposure", f"max |dSharpe| {g7_dev:.3e}", "< 5e-3",
         g7_dev < 5e-3)
    gate("G8 netted blend turnover <= naive + split-restoration at EVERY ROW of every blend",
         f"{g8_viol} violations of {n_blend} blends", "== 0", g8_viol == 0)
    publish("G8b split-restoration cost omitted by the naive charge (mean bp/yr over all blends)",
            f"{np.mean(rest_bp):.2f} bp/yr (max {np.max(rest_bp):.2f})")
    publish("G8c netted MINUS naive blend cost (mean bp/yr; positive = the naive ruler "
            "UNDER-charges a real blend)", f"{np.mean(netnaive_bp):+.2f} bp/yr "
            f"(min {np.min(netnaive_bp):+.2f}, max {np.max(netnaive_bp):+.2f})")
    gate("G9 the stop, the SPY macro gate and the breadth gate are NON-ANTICIPATING "
         "(truncated-tape replay)", f"max |dret| {g9_dev:.3e}", "< 1e-12", g9_dev < 1e-12)
    gate("G10 deterministic recompute (L_M=150, one per panel)", f"max |dSharpe| {g10_dev:.3e}",
         "< 1e-12", g10_dev < 1e-12)
    gate("G12 the enactable RULES wording of the L_M blend (a TWO-STATE GROSS, g when SPY is "
         "above its 200d MA and lam*g when below) reproduces the two-sleeve blend it was found as, "
         "over all 3 lambdas x 3 panels", f"max |dSharpe| {g12_dev:.4f}", "< 0.01",
         g12_dev < 0.01)
    gate("G5 the rule-8 chooser reads no row on or after 2017-01-01",
         "is_Sharpe computed on rows [WARMUP, searchsorted(2016-12-31)) only", "by construction",
         True)
    return G, P, W, panels, t0


def analyse(G, P, W, panels, t0):
    lad_names = list(LADDERS)
    H = P[np.isclose(P.lam, 0.50)].copy()

    # ---- (0) THE BUILD GATE -----------------------------------------------------------------
    say("\n" + "=" * 124)
    say("(0) DID THE THREE FLAT LADDERS ACTUALLY GET BUILT?  mean flat_one per ladder per panel "
        "at lambda = 0.50.")
    say("    Idea 1530's record for comparison: L_S 0.3190, L_C 0.0015, all six others EXACTLY "
        "0.0000.")
    say("=" * 124)
    bt = H.pivot_table(index="ladder", columns="panel", values="flat_one", aggfunc="mean")
    bt = bt.reindex(lad_names)
    say("    ladder  mechanism                       " + "".join(f"{c:>10}" for c in bt.columns)
        + "      max")
    for L in lad_names:
        row = bt.loc[L]
        say(f"    {L:<7} {LADDERS[L]['flat']:<32}" + "".join(f"{row[c]:10.4f}" for c in bt.columns)
            + f"{float(H[H.ladder == L].flat_one.max()):9.4f}")
    g11_ok = all(float(bt.loc[L].min()) >= 0.02 for L in FLAT_LADDERS)
    gate("G11 THE BUILD GATE: all THREE intended flat-bearing ladders carry mean flat_one >= 0.02 "
         "on EVERY panel (without it this run is 1530's single-ladder fit again)",
         "; ".join(f"{L} min {float(bt.loc[L].min()):.4f}" for L in FLAT_LADDERS),
         ">= 0.02 each", g11_ok)
    xmin, xmax = float(bt.loc["L_X"].min()), float(bt.loc["L_X"].max())
    say(f"    L_X (the MAXVOL route idea 1538 proposed) carries mean flat_one "
        f"{xmin:.4f}..{xmax:.4f} — the min-hold RETAINS held names regardless of eligibility, so "
        f"tightening the ceiling shrinks the book without EMPTYING it.  Published as a NEGATIVE: "
        f"MAXVOL is not a buildable flat_one ladder off this incumbent.")
    publish("L_X MAXVOL flat_one range (the proposed route that does not build)",
            f"{xmin:.4f}..{xmax:.4f}")

    # ---- (1) the two-number fit --------------------------------------------------------------
    say("\n" + "=" * 124)
    say(f"(1) ARE TWO NUMBERS ENOUGH?  Pooled OLS over all {len(H)} pairs at lambda = 0.50.")
    say("    y = D_sharpe;  x1 = 1 - OV;  x2 = flat_one.  One-number fit reported beside it for "
        "continuity with 1530.")
    say("=" * 124)
    fits = []
    for stat in OVSTATS:
        x1 = (1.0 - H[stat.lower()].values).astype(float)
        x2 = H["flat_one"].values.astype(float)
        y = H["D_sharpe"].values.astype(float)
        ok = np.isfinite(x1) & np.isfinite(x2) & np.isfinite(y)
        Hs = H[ok]
        x1, x2, y = x1[ok], x2[ok], y[ok]
        X1 = np.column_stack([np.ones_like(x1), x1])
        _, _, r2_one = ols(X1, y)
        X = np.column_stack([np.ones_like(x1), x1, x2])
        b, res, r2 = ols(X, y)
        Dm = np.column_stack([(Hs.ladder.values == L).astype(float) for L in lad_names[1:]])
        _, _, r2f = ols(np.column_stack([X, Dm]), y)
        sd = float(res.std(ddof=3))
        say(f"\n  [{stat}]  ONE number  (x1 only):  R^2 = {r2_one:.4f}"
            f"   [1530 committed 0.0154 / 0.1117]")
        say(f"            TWO numbers (x1 + flat_one):  D = {b[0]:+.5f} {b[1]:+.5f}*x1 "
            f"{b[2]:+.5f}*flat_one   R^2 = {r2:.4f}   [1530 committed 0.6094 / 0.6066]")
        say(f"            + LADDER IDENTITY (9 dummies): R^2 = {r2f:.4f}   dR^2 = {r2f - r2:+.4f}"
            f"   [1530 committed +0.0053 / +0.0079]")
        say(f"            per-ladder mean residual from the TWO-number fit "
            f"(residual sd {sd:.5f}):")
        worst_t, worst_l = 0.0, ""
        for L in lad_names:
            m = Hs.ladder.values == L
            if not m.any():
                continue
            mr = float(res[m].mean())
            t = mr / (sd / np.sqrt(m.sum())) if sd > 0 else np.nan
            if abs(t) > abs(worst_t):
                worst_t, worst_l = t, L
            say(f"              {L:<5} n={m.sum():<3} mean resid {mr:+.5f}  t {t:+6.2f}"
                f"   ({LADDERS[L]['flat']})")
        t1, t2, t3 = r2 >= R2_BAR, (r2f - r2) < DR2_BAR, abs(worst_t) <= T_BAR
        say(f"            PRE-REGISTERED: T1 R^2>={R2_BAR} {'PASS' if t1 else 'FAIL'} | "
            f"T2 dR^2<{DR2_BAR} {'PASS' if t2 else 'FAIL'} | T3 no ladder |t|>{T_BAR} "
            f"{'PASS' if t3 else 'FAIL'} (worst {worst_l} t {worst_t:+.2f})")
        fits.append(dict(stat=stat, r2_one=r2_one, r2_two=r2, r2_full=r2f, dr2=r2f - r2,
                         b_int=b[0], b_ov=b[1], b_flat=b[2], resid_sd=sd,
                         worst_t=worst_t, worst_ladder=worst_l, T1=t1, T2=t2, T3=t3))
    F = pd.DataFrame(fits)

    # ---- (2) T4 LEAVE-ONE-LADDER-OUT ----------------------------------------------------------
    say("\n" + "=" * 124)
    say("(2) T4 — LEAVE-ONE-LADDER-OUT.  The test 1530 could not run.  Fit the two numbers on the "
        "OTHER EIGHT ladders,")
    say("    then PREDICT the held-out ladder's gaps.  A rule that never saw the stop must still "
        "price the stop.")
    say("    R^2 here is against the held-out ladder's OWN mean and CAN go negative.")
    say("=" * 124)
    lolo = []
    for stat in OVSTATS:
        say(f"\n  [{stat}]")
        for L in lad_names:
            m = (H.ladder.values == L)
            x1 = (1.0 - H[stat.lower()].values).astype(float)
            x2 = H["flat_one"].values.astype(float)
            y = H["D_sharpe"].values.astype(float)
            ok = np.isfinite(x1) & np.isfinite(x2) & np.isfinite(y)
            tr, te = ok & ~m, ok & m
            if te.sum() < 3 or tr.sum() < 5:
                continue
            Xtr = np.column_stack([np.ones(tr.sum()), x1[tr], x2[tr]])
            b, _, _ = ols(Xtr, y[tr])
            Xte = np.column_stack([np.ones(te.sum()), x1[te], x2[te]])
            pred = Xte @ b
            r2o = r2_against(y[te], pred)
            # the one-number rule's out-of-ladder R^2, for the same held-out set
            b1, _, _ = ols(np.column_stack([np.ones(tr.sum()), x1[tr]]), y[tr])
            r2o1 = r2_against(y[te], np.column_stack([np.ones(te.sum()), x1[te]]) @ b1)
            flag = "FLAT-BEARING" if L in FLAT_LADDERS else ""
            say(f"    hold out {L:<5} n={te.sum():<3} out-of-ladder R^2  TWO numbers {r2o:+8.4f}"
                f"   (ONE number {r2o1:+8.4f})   mean|D| {np.abs(y[te]).mean():.4f}  {flag}")
            lolo.append(dict(stat=stat, held_out=L, n=int(te.sum()), r2_two=r2o, r2_one=r2o1,
                             mean_absD=float(np.abs(y[te]).mean()),
                             flat_bearing=L in FLAT_LADDERS))
        sub = [r for r in lolo if r["stat"] == stat and r["held_out"] in FLAT_LADDERS]
        ok4 = all(r["r2_two"] >= LOLO_BAR for r in sub)
        say(f"    T4 (each of {FLAT_LADDERS} out-of-ladder R^2 >= {LOLO_BAR}): "
            f"{'PASS' if ok4 else 'FAIL'}  — "
            + ", ".join(f"{r['held_out']} {r['r2_two']:+.4f}" for r in sub))
        F.loc[F.stat == stat, "T4"] = ok4
    LO = pd.DataFrame(lolo)

    # ---- (3) T5 RULE 8 ON THE RULE ITSELF ------------------------------------------------------
    say("\n" + "=" * 124)
    say("(3) T5 — RULE 8 ON THE PREDICTION RULE.  Coefficients fit on the IS gaps "
        "(warm-up..2016-12-31) ONLY,")
    say("    with IS-window overlaps and IS-window flat_one; the 2017-2026 gaps are read ONCE.")
    say("=" * 124)
    r8 = []
    for stat in OVSTATS:
        x1i = (1.0 - H[f"{stat.lower()}_IS"].values).astype(float)
        x2i = H["flat_one_IS"].values.astype(float)
        yi = H["D_sharpe_IS"].values.astype(float)
        x1o = (1.0 - H[f"{stat.lower()}_OOS"].values).astype(float)
        x2o = H["flat_one_OOS"].values.astype(float)
        yo = H["D_sharpe_OOS"].values.astype(float)
        ok = (np.isfinite(x1i) & np.isfinite(x2i) & np.isfinite(yi)
              & np.isfinite(x1o) & np.isfinite(x2o) & np.isfinite(yo))
        Xi = np.column_stack([np.ones(ok.sum()), x1i[ok], x2i[ok]])
        b, _, r2i = ols(Xi, yi[ok])
        Xo = np.column_stack([np.ones(ok.sum()), x1o[ok], x2o[ok]])
        r2o = r2_against(yo[ok], Xo @ b)
        b1, _, r2i1 = ols(np.column_stack([np.ones(ok.sum()), x1i[ok]]), yi[ok])
        r2o1 = r2_against(yo[ok], np.column_stack([np.ones(ok.sum()), x1o[ok]]) @ b1)
        t5 = r2o >= OOS_R2_BAR
        say(f"    [{stat}] IS fit  D = {b[0]:+.5f} {b[1]:+.5f}*x1 {b[2]:+.5f}*flat_one   "
            f"IS R^2 {r2i:.4f}  ->  OOS R^2 {r2o:+.4f}   "
            f"T5 (>= {OOS_R2_BAR}) {'PASS' if t5 else 'FAIL'}")
        say(f"             one-number comparison: IS R^2 {r2i1:.4f} -> OOS R^2 {r2o1:+.4f}")
        r8.append(dict(stat=stat, n=int(ok.sum()), b_int=b[0], b_ov=b[1], b_flat=b[2],
                       IS_r2_two=r2i, OOS_r2_two=r2o, IS_r2_one=r2i1, OOS_r2_one=r2o1, T5=t5))
        F.loc[F.stat == stat, "T5"] = t5
    R8 = pd.DataFrame(r8)
    F["two_numbers_enough"] = F[["T1", "T2", "T3", "T4", "T5"]].all(axis=1)

    # ---- (4) both KEEP paths ---------------------------------------------------------------
    say("\n" + "=" * 124)
    say(f"(4) BOTH KEEP PATHS AT ALL {len(G)} CELLS (4a vs live RULES v2; 4b vs SPY, DD cap "
        "0.60x, CAGR floor 0.70x).")
    say("=" * 124)
    for p in ["U56", "B136", "SMALL"]:
        s = G[G.panel == p]
        say(f"    [{p}] 4a {int(s.keep4a.sum())}/{len(s)} full, {int(s.keep4a_OOS.sum())}/{len(s)} "
            f"OOS  |  4b {int(s.keep4b.sum())}/{len(s)} full, {int(s.keep4b_OOS.sum())}/{len(s)} "
            f"OOS, {int((s.keep4b & s.keep4b_OOS).sum())}/{len(s)} BOTH")
        for leg in ["H1", "H2", "DD", "CAGR"]:
            say(f"           4b leg {leg:<4} passes {int(s['leg_'+leg].sum()):>3}/{len(s)} full, "
                f"{int(s['legO_'+leg].sum()):>3}/{len(s)} OOS")
    say(f"    TOTAL 4a {int(G.keep4a.sum())}/{len(G)} full, {int(G.keep4a_OOS.sum())}/{len(G)} OOS;"
        f" 4b {int(G.keep4b.sum())}/{len(G)} full, {int(G.keep4b_OOS.sum())}/{len(G)} OOS, "
        f"{int((G.keep4b & G.keep4b_OOS).sum())}/{len(G)} BOTH")
    both = G[G.keep4b & G.keep4b_OOS]
    if len(both):
        say("    4b BOTH cells by ladder: "
            + ", ".join(f"{k} {v}" for k, v in both.ladder.value_counts().items()))

    # ---- (5) the capital arm ---------------------------------------------------------------
    say("\n" + "=" * 124)
    say("(5) RULE 8 CAPITAL ARM.  Cell chosen by argmax IS Sharpe on warm-up..2016-12-31 ONLY; "
        "2017-2026 read once.")
    say("=" * 124)
    for _, r in W.iterrows():
        say(f"    [{r.panel}] {r.chooser:<32} -> {r.cell:<26} IS {r.IS_Sharpe:.4f} | OOS "
            f"{r.OOS_CAGR:7.2%} / {r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:7.2%}  "
            f"(anchor {r.anchor_OOS_CAGR:.2%}/{r.anchor_OOS_Sharpe:.4f}/{r.anchor_OOS_MaxDD:.2%}; "
            f"SPY {r.spy_OOS_CAGR:.2%}/{r.spy_OOS_Sharpe:.4f}/{r.spy_OOS_MaxDD:.2%}; "
            f"v2 {r.live_OOS_CAGR:.2%}/{r.live_OOS_Sharpe:.4f}/{r.live_OOS_MaxDD:.2%})  "
            f"odSharpe {r.odSharpe:+.4f} t {r.odSharpe_t:+.2f}  4a {r.keep4a_OOS} 4b "
            f"{r.keep4b_OOS}")
    mix = W[W.chooser.str.startswith("ARGMAX-IS (all")]
    non = W[W.chooser.str.startswith("DO NOTHING")]
    say(f"\n    MEAN OOS SHARPE: chooser {mix.OOS_Sharpe.mean():.4f}  vs  do-nothing "
        f"{non.OOS_Sharpe.mean():.4f}  ("
        f"{'CHOOSER WINS' if mix.OOS_Sharpe.mean() > non.OOS_Sharpe.mean() else 'DOING NOTHING WINS'})")

    # ---- verdict -----------------------------------------------------------------------------
    say("\n" + "=" * 124)
    say("VERDICT")
    say("=" * 124)
    for _, r in F.iterrows():
        say(f"    [{r.stat}] one number R^2 {r.r2_one:.4f} -> TWO numbers {r.r2_two:.4f} "
            f"(+{r.r2_two - r.r2_one:.4f});  T1 {r.T1} T2 {r.T2} T3 {r.T3} T4 {r.T4} T5 {r.T5}  "
            f"-> TWO NUMBERS ENOUGH: {r.two_numbers_enough}")
    say(f"    BUILD GATE G11 (three independent flat ladders): "
        f"{all(g['pass_'] for g in GATES if g['gate'].startswith('G11'))}")
    say(f"    CAPITAL: 4a {int(G.keep4a.sum())}/{len(G)} full and {int(G.keep4a_OOS.sum())}/{len(G)}"
        f" OOS; 4b BOTH {int((G.keep4b & G.keep4b_OOS).sum())}/{len(G)}; rule-8 chooser mean OOS "
        f"Sharpe {mix.OOS_Sharpe.mean():.4f} vs do-nothing {non.OOS_Sharpe.mean():.4f}.")

    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    F.to_csv(f"{OUT}.fit.csv", index=False)
    LO.to_csv(f"{OUT}.lolo.csv", index=False)
    R8.to_csv(f"{OUT}.rule8_fit.csv", index=False)
    bt.to_csv(f"{OUT}.buildgate.csv")
    allpass = all(g["pass_"] for g in GATES)
    say(f"\n    ALL GATES PASS: {allpass}   ({time.time()-t0:.0f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    G, P, W, panels, t0 = main()
    analyse(G, P, W, panels, t0)

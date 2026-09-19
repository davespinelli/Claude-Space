#!/usr/bin/env python3
"""
Idea 1530 (lane cloud, 2026-09-19) — is SCALE vs COMPOSITION the RIGHT TAXONOMY for every LADDER
the record owns?

THE PREMISE (idea 1509's mechanism, stated as a prediction).  1509 found that a TWO-RUNG CAPITAL
BLEND can only differ from a single rung when the two rungs HOLD DIFFERENT THINGS, and verified it
on exactly TWO ladders: gross (a SCALE ladder — every rung holds the same names at the same
relative weights, so the blend IS the intermediate rung, |dSharpe| 2.8e-05) and min-hold (a
COMPOSITION ladder — rungs hold different names on the same day, so the blend moves things).  Two
ladders is not a taxonomy.  This run classifies EVERY ladder the record owns by MEASURING the
holdings overlap between adjacent rungs, then asks whether that one number PREDICTS the
blend-vs-rung gap on its own.  If it does, no ladder in the record ever needs re-cutting twice:
the overlap tells you in advance whether a blend can move a contrast.

THE EIGHT LADDERS (each a single dial off the frozen 2026-09-04 KEEP-4b incumbent — U56/B136/SMALL,
N = 20, H = 126, gross 0.75, MAXVOL 0.60, 200d MA gate, weekly Fri-decide / Mon-trade, 10 bps,
t+1 — everything else held fixed).  The PRE-REGISTERED class is written here, BEFORE any number
was read, so the taxonomy can be wrong:

  L_G   gross g      {0.25, 0.50, 0.75, 1.00}          predicted SCALE       (pure exposure)
  L_T   vol target   {none, 0.20, 0.15, 0.10}          predicted SCALE       (de-gross only)
  L_S   stop depth   {none, 0.25, 0.15, 0.10}          predicted SCALE       (de-gross to cash)
  L_N   N            {10, 15, 20, 30, 40}              predicted COMPOSITION (nested, so high ov)
  L_H   min-hold H   {21, 63, 126, 252}                predicted COMPOSITION (1509's own case)
  L_C   cadence      {W, 2W, M, Q}                     predicted COMPOSITION (timing)
  L_V   MAXVOL       {0.30, 0.45, 0.60, 0.90, inf}     predicted COMPOSITION (eligibility)
  L_B   MA band      {0.00, 0.03, 0.06, 0.10}          predicted COMPOSITION (gate hysteresis)

34 rungs per panel, 26 adjacent pairs, 3 blend weights -> 112 cells per panel, 336 in all, EVERY
ONE published in .grid.csv.  The ladder set and its rungs are ENUMERATED, not tuned.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  DIAL 1  BLEND WEIGHT lambda  {0.25, 0.50, 0.75}   how the capital is split across the two rungs.
  DIAL 2  OVERLAP STATISTIC    {OV_HOLD, OV_CAP}    which overlap the taxonomy is built on.

          OV_HOLD (composition-only): on days where BOTH books hold at least one name, the L1
                  overlap sum_i min(n_A,i, n_B,i) of the NORMALISED weight vectors (n = w / sum w);
                  days where exactly one book is flat are EXCLUDED and their share published.
                  This statistic is BLIND to exposure: a pure de-gross scores 1.000.
          OV_CAP  (capital-inclusive): sum_i min(w_A,i, w_B,i) / max(sum w_A, sum w_B) on the
                  UNNORMALISED weights over every day; both-flat -> 1, exactly-one-flat -> 0.
                  This statistic SEES exposure: a gross ladder scores below 1.

          The two are not a convenience.  They ARE the taxonomy question: 1509's mechanism says
          only COMPOSITION differences can open a blend gap, so OV_HOLD should predict the gap and
          OV_CAP should not.  Reported at BOTH values for every pair.

THE BLEND, CONSTRUCTED AS REAL CAPITAL (not as an average of two published statistics).  Two
sleeves held in a DAILY CONSTANT-MIX capital split lambda : 1 - lambda.  Post-trade blend weights
are lambda*W_post,A + (1-lambda)*W_post,B.  Pre-trade blend weights use the ONE-DAY DRIFTED capital
share s_t = lambda(1+r_A,t-1) / (lambda(1+r_A,t-1) + (1-lambda)(1+r_B,t-1)), so the cost of
RESTORING the split is charged, not assumed away.  Blend turnover is therefore the NETTED
sum_i |W_post,blend - W_pre,blend| — when both sleeves want the same name the cross-sleeve trades
cancel, which is the whole economic point of a blend.  The NAIVE (un-netted) charge
lambda*turn_A + (1-lambda)*turn_B is published beside it at every cell as the upper bound; by the
triangle inequality netted <= naive always, and the gap between them is published.

THE GAP THE TAXONOMY MUST PREDICT.
  D_lambda = Sharpe(blend) - [lambda*Sharpe(A) + (1-lambda)*Sharpe(B)]
A SCALE pair blends into a book that is the intermediate rung, and Sharpe is scale-invariant, so
D = 0 is the prediction.  A COMPOSITION pair blends two imperfectly correlated books, so the
blend's volatility falls faster than its mean and D > 0.  The CAGR twin dC_lambda is published
beside it at every cell (1509's carve-out: CAGR is NOT scale-invariant, so a scale pair may open a
CAGR gap while opening no Sharpe gap — a prediction this run can also test).

PRE-REGISTERED BARS (written before any number was read).  Overlap is a SUFFICIENT STATISTIC iff,
pooled over all 26 pairs x 3 panels = 78 pairs at lambda = 0.50:
  (S1) an OLS of D on x = 1 - OV_HOLD reaches R^2 >= 0.80;
  (S2) adding LADDER IDENTITY (8 dummies) raises R^2 by < 0.05; and
  (S3) no ladder's mean residual from the overlap-only fit reaches |t| > 2.
The BINARY taxonomy is ADEQUATE iff a single cut OV_HOLD > theta separates |D| < 0.02 from
|D| >= 0.02 on >= 90% of pairs, with theta CHOSEN ON THE FIRST HALF ONLY (rule 8) and the second
half read once.  Any of these failing is a finding against the idea's own hypothesis and is
recorded as one.

THE CAPITAL ARM (what a taxonomy is worth in money).  Every rung and every blend is a real book.
Both KEEP paths are evaluated at all 336 cells against the live RULES v2 baseline and SPY, on the
full sample and on the 2017-2026 OOS window, and the rule-8 chooser (argmax IS Sharpe on
warm-up..2016-12-31 only) is scored OOS against the frozen incumbent, RULES v2 and SPY.

PROTOCOL: rule 1 (>= 10y); rule 2 (t+1, 10 bps, no leverage, no shorting — the vol target NEVER
levers above the rung's gross); rule 3 (RULES v2 AND SPY); rule 4 (both KEEP paths, exactly 2
tuned parameters); rule 8 (walk-forward, 2017-2026 read ONCE); rule 9 (survivorship stated).
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

GATES.  G0 sample >= 10y.  G1 CROSS-SCRIPT REPLAY of the committed 2026-09-04 U56 anchor
(15.80% / 1.1537 / -19.13% full; 17.32% / 1.1857 / -19.13% OOS).  G2 the anchor rung is
BIT-IDENTICAL wherever it appears (it sits on all 8 ladders).  G3 all 336 cells published.
G4 exactly two tuned parameters.  G5 the rule-8 chooser reads no row on or after 2017-01-01.
G6 no leverage: realised weight sum never exceeds 1.0 at any cell.  G7 1509'S MECHANISM REPLAYED:
the lambda-blend of gross rungs 0.50 and 1.00 must equal the single gross rung at the blended
exposure.  G8 netted blend turnover <= naive blend turnover at every cell (triangle inequality).
G9 the stop and the vol target are NON-ANTICIPATING (truncated-tape replay is bit-identical).
G10 deterministic recompute of one cell per panel.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-19_scale-vs-composition-ladder-taxonomy_cloud.py
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
SLUG = "scale-vs-composition-ladder-taxonomy"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP = 260
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G, I_V, I_B, I_C = 20, 126, 0.75, 0.60, 0.00, "W"   # the frozen incumbent
COST = 10.0
OOS_START, IS_END = "2017-01-01", "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LAMBDAS = [0.25, 0.50, 0.75]                     # DIAL 1
OVSTATS = ["OV_HOLD", "OV_CAP"]                  # DIAL 2
MATERIAL = 0.02                                  # |D| bar for the binary taxonomy
BOOT_REPS, BOOT_BLOCK, BOOT_SEED = 400, 63, 20260919
C_U56 = dict(CAGR=0.1580, Sharpe=1.1537, MaxDD=-0.1913, oSharpe=1.1857)

LADDERS = {
    "L_G": dict(dial="gross", rungs=[0.25, 0.50, 0.75, 1.00], pred="SCALE"),
    "L_T": dict(dial="voltgt", rungs=[None, 0.20, 0.15, 0.10], pred="SCALE"),
    "L_S": dict(dial="stop", rungs=[None, 0.25, 0.15, 0.10], pred="SCALE"),
    "L_N": dict(dial="N", rungs=[10, 15, 20, 30, 40], pred="COMPOSITION"),
    "L_H": dict(dial="H", rungs=[21, 63, 126, 252], pred="COMPOSITION"),
    "L_C": dict(dial="cadence", rungs=["W", "2W", "M", "Q"], pred="COMPOSITION"),
    "L_V": dict(dial="maxvol", rungs=[0.30, 0.45, 0.60, 0.90, np.inf], pred="COMPOSITION"),
    "L_B": dict(dial="band", rungs=[0.00, 0.03, 0.06, 0.10], pred="COMPOSITION"),
}

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
    """Least squares with an intercept already in X.  Returns (beta, resid, R2)."""
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    fit = X @ beta
    resid = y - fit
    ss_t = float(((y - y.mean()) ** 2).sum())
    r2 = 1.0 - float((resid ** 2).sum()) / ss_t if ss_t > 0 else np.nan
    return beta, resid, r2


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
    """The 200d MA gate.  band = 0.00 is the incumbent's plain `px > ma`; band > 0 adds RULES v2
    hysteresis (IN above ma*(1+band), OUT below ma*(1-band), previous state in between)."""
    ma = q.rolling(200).mean()
    if band <= 0.0:
        return (q > ma).values
    raw = pd.DataFrame(np.nan, index=q.index, columns=q.columns)
    raw = raw.mask(q > ma * (1 + band), 1.0).mask(q < ma * (1 - band), 0.0)
    return (raw.ffill().fillna(0.0) > 0.5).values


def cadence_rows(idx, cad):
    """Rebalance rows, decided at t and applied at t+1 (rule 2).  '2W' = every other weekly date."""
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
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        q = px[invest]
        self.q = q
        self.comp = mech_legs(q)
        self.vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
        self._gate, self._reb = {}, {}

    def gate_of(self, band):
        if band not in self._gate:
            self._gate[band] = band_gate(self.q, band)
        return self._gate[band]

    def reb_of(self, cad):
        if cad not in self._reb:
            self._reb[cad] = cadence_rows(self.idx, cad)
        return self._reb[cad]

    def frame_inputs(self, band, maxvol):
        above = self.gate_of(band)
        elig = above & (np.nan_to_num(self.vol20, nan=1e9) < maxvol)
        sc = self.comp * (0.5 + 0.5 * above.astype(float))
        key = np.where(np.isfinite(sc), -sc, np.inf)
        return elig, key


def build_frame(pan, elig, key, reb, N, H, lag=1, nrows=None):
    """The frozen min-hold selection frame at GROSS = 1.0, forward-filled to a daily T x M step
    matrix of TARGET weights.  nrows truncates the tape (used by gate G9)."""
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


def run_rung(pan, frame, reb, g, stop=None, voltgt=None, nrows=None):
    """The daily engine.  Numerically identical to the record's run_book (weights drift
    multiplicatively between rebalances, uninvested NAV earns 0.00%/yr, turnover charged on the
    rebalance row), but it also emits the PRE- and POST-trade daily weight matrices the blend
    construction needs, and it can read its OWN equity (the stop and the vol target)."""
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
            if voltgt is not None and t > 21:
                v = float(rnet[t - 20:t].std(ddof=0)) * np.sqrt(252)
                if v > 0:
                    gt = min(gt, gt * voltgt / v)          # de-gross only, never levers
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


def blend(A, B, lam):
    """Two sleeves in a DAILY CONSTANT-MIX capital split lam : 1-lam.  Returns net returns, netted
    turnover and naive turnover."""
    rA, rB = A["rnet"], B["rnet"]
    prevA = np.concatenate([[0.0], rA[:-1]])
    prevB = np.concatenate([[0.0], rB[:-1]])
    num = lam * (1.0 + prevA)
    s = num / (num + (1.0 - lam) * (1.0 + prevB))
    Wpre = s[:, None] * A["Wpre"] + (1.0 - s)[:, None] * B["Wpre"]
    Wpost = lam * A["Wpost"] + (1.0 - lam) * B["Wpost"]
    turn_net = np.abs(Wpost - Wpre).sum(axis=1)
    turn_naive = lam * A["turn"] + (1.0 - lam) * B["turn"]
    # the SPLIT-RESTORATION component: the turnover spent putting the capital split back to
    # lambda after one day of sleeve drift.  The naive charge omits it entirely, which is why
    # netted turnover is NOT bounded by naive turnover -- it is bounded by naive + restoration
    # (triangle inequality on Wpost - Wpre_lambda and Wpre_lambda - Wpre_drifted).  Gate G8.
    Wpre_lam = lam * A["Wpre"] + (1.0 - lam) * B["Wpre"]
    turn_rest = np.abs(Wpre_lam - Wpre).sum(axis=1)
    rgross = lam * A["rg"] + (1.0 - lam) * B["rg"]
    return dict(rnet=rgross - turn_net * COST / 1e4,
                rnet_naive=rgross - turn_naive * COST / 1e4,
                turn=turn_net, turn_naive=turn_naive, turn_rest=turn_rest,
                wsum=float(Wpost.sum(axis=1).max()))


def overlaps(A, B, start):
    """OV_HOLD (composition-only, flat days excluded) and OV_CAP (capital-inclusive, every day)."""
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
    # name-set Jaccard, published alongside as a third reading (not a dial)
    ja = a > 1e-12
    jb = b > 1e-12
    inter = (ja & jb).sum(axis=1)
    union = (ja | jb).sum(axis=1)
    jac = float(np.where(union > 0, inter / np.maximum(union, 1), 1.0).mean())
    return ov_hold, ov_cap, flat_one, jac


def rung_spec(ladder, v):
    """The frozen incumbent with exactly ONE dial moved."""
    s = dict(N=I_N, H=I_H, g=I_G, maxvol=I_V, band=I_B, cad=I_C, stop=None, voltgt=None)
    d = LADDERS[ladder]["dial"]
    s[{"gross": "g", "voltgt": "voltgt", "stop": "stop", "N": "N", "H": "H",
       "cadence": "cad", "maxvol": "maxvol", "band": "band"}[d]] = v
    return s


def is_anchor(s):
    return (s["N"] == I_N and s["H"] == I_H and s["g"] == I_G and s["maxvol"] == I_V
            and s["band"] == I_B and s["cad"] == I_C and s["stop"] is None and s["voltgt"] is None)


def build_rung(pan, s, nrows=None):
    elig, key = pan.frame_inputs(s["band"], s["maxvol"])
    reb = pan.reb_of(s["cad"])
    frame = build_frame(pan, elig, key, reb, s["N"], s["H"], nrows=nrows)
    return run_rung(pan, frame, reb, s["g"], stop=s["stop"], voltgt=s["voltgt"], nrows=nrows)


# ---------------------------------------------------------------------------------------------
def main():
    t0 = time.time()
    say("=" * 124)
    say("IDEA 1530 (lane cloud, 2026-09-19) — is SCALE vs COMPOSITION the RIGHT TAXONOMY for every "
        "LADDER the record owns?")
    say("8 ladders x 34 rungs x 26 adjacent pairs x 3 blend weights = 112 cells per panel, 336 in "
        "all, every one published.")
    say("DIAL 1 blend weight lambda {0.25,0.50,0.75};  DIAL 2 overlap statistic {OV_HOLD, OV_CAP}.")
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
    gate("G4 exactly two tuned parameters (blend weight lambda, overlap statistic)", 2, "== 2", True)

    grid, pairs, wf_rows = [], [], []
    wsum_global, g1_ok = 0.0, None
    anchor_dev, g8_viol, g9_dev, g10_dev, g7_dev = 0.0, 0, 0.0, 0.0, 0.0
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

        # ---- the frozen incumbent, once, as the contrast anchor -----------------------------
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
            row = dict(panel=pan.name, ladder=ladder, pred_class=LADDERS[ladder]["pred"],
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
            prev_row = None
            for j, v in enumerate(rungs):
                s = rung_spec(lad, v)
                R = build_rung(pan, s)
                wsum_global = max(wsum_global, R["wsum"])
                if is_anchor(s):
                    anchor_dev = max(anchor_dev, float(np.max(np.abs(R["rnet"] - anch))))
                rr = cell(f"{lad}={v}", lad, "RUNG", v, "", np.nan, R["rnet"], R["turn"],
                          dict(ov_hold=np.nan, ov_cap=np.nan, flat_one=np.nan, jaccard=np.nan,
                               D_sharpe=np.nan, D_cagr=np.nan, turn_naive_yr=np.nan,
                               D_sharpe_IS=np.nan, D_sharpe_OOS=np.nan,
                               is_anchor=is_anchor(s)))
                if prev is not None:
                    ovh, ovc, flat1, jac = overlaps(prev, R, WARMUP)
                    shA = sharpe(prev["rnet"][WARMUP:])
                    shB = sharpe(R["rnet"][WARMUP:])
                    shA_i, shB_i = sharpe(prev["rnet"][WARMUP:i_is]), sharpe(R["rnet"][WARMUP:i_is])
                    shA_o, shB_o = sharpe(prev["rnet"][i_oos:]), sharpe(R["rnet"][i_oos:])
                    cgA, cgB = cagr(prev["rnet"][WARMUP:]), cagr(R["rnet"][WARMUP:])
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
                                       D_sharpe_IS=Dsh_i, D_sharpe_OOS=Dsh_o, is_anchor=False))
                        pairs.append(dict(panel=pan.name, ladder=lad,
                                          pred_class=spec["pred"],
                                          rung_a=str(rungs[j - 1]), rung_b=str(v), lam=lam,
                                          ov_hold=ovh, ov_cap=ovc, jaccard=jac, flat_one=flat1,
                                          Sharpe_A=shA, Sharpe_B=shB,
                                          Sharpe_blend=sharpe(rb[WARMUP:]),
                                          D_sharpe=Dsh, D_cagr=Dcg,
                                          D_sharpe_IS=Dsh_i, D_sharpe_OOS=Dsh_o,
                                          turn_net_yr=cr["turnover_yr"], turn_naive_yr=tn))
                        # G7: 1509's mechanism on the SCALE ladder it was verified on
                        if lad == "L_G" and rungs[j - 1] == 0.50 and v == 1.00:
                            gex = lam * 0.50 + (1 - lam) * 1.00
                            Rx = build_rung(pan, rung_spec("L_G", gex))
                            g7_dev = max(g7_dev,
                                         abs(sharpe(Rx["rnet"][WARMUP:]) - sharpe(rb[WARMUP:])))
                            del Rx
                    del prev
                prev, prev_row = R, rr
            del prev
            say(f"    [{pan.name}] {lad} done ({len(grid)} cells, {time.time()-t0:.0f}s)")

        # ---- G9 causality of the two equity-reading devices --------------------------------
        for lad, v in (("L_S", 0.15), ("L_T", 0.15)):
            full = build_rung(pan, rung_spec(lad, v))
            trunc = build_rung(pan, rung_spec(lad, v), nrows=i_oos)
            g9_dev = max(g9_dev, float(np.max(np.abs(full["rnet"][:i_oos] - trunc["rnet"]))))
            del full, trunc

        # ---- G10 deterministic recompute ----------------------------------------------------
        R2 = build_rung(pan, rung_spec("L_H", 63))
        ref = [x for x in grid if x["panel"] == pan.name and x["name"] == "L_H=63"][0]
        g10_dev = max(g10_dev, abs(sharpe(R2["rnet"][WARMUP:]) - ref["Sharpe"]))
        del R2

        # ---- rule 8 capital arm: argmax IS Sharpe over every cell on this panel -------------
        cand = [x for x in grid if x["panel"] == pan.name]
        for tag, pool in (("ARGMAX-IS (all 112 cells)", cand),
                          ("ARGMAX-IS (blends only)", [x for x in cand if x["kind"] == "BLEND"]),
                          ("DO NOTHING (frozen incumbent)",
                           [x for x in cand if x.get("is_anchor")])):
            pick = max(pool, key=lambda x: (-1e9 if not np.isfinite(x["is_Sharpe"])
                                            else x["is_Sharpe"]))
            wf_rows.append(dict(
                panel=pan.name, chooser=tag, cell=pick["name"], ladder=pick["ladder"],
                kind=pick["kind"], lam=pick["lam"], IS_Sharpe=pick["is_Sharpe"],
                OOS_CAGR=pick["oCAGR"], OOS_Sharpe=pick["oSharpe"], OOS_MaxDD=pick["oMaxDD"],
                anchor_OOS_CAGR=ao["CAGR"], anchor_OOS_Sharpe=ao["Sharpe"],
                anchor_OOS_MaxDD=ao["MaxDD"],
                spy_OOS_CAGR=spyO["CAGR"], spy_OOS_Sharpe=spyO["Sharpe"],
                spy_OOS_MaxDD=spyO["MaxDD"], live_OOS_CAGR=liveO["CAGR"],
                live_OOS_Sharpe=liveO["Sharpe"], live_OOS_MaxDD=liveO["MaxDD"],
                odSharpe=pick["odSharpe"], odSharpe_t=pick["odSharpe_t"],
                keep4a_OOS=pick["keep4a_OOS"], keep4b_OOS=pick["keep4b_OOS"],
                ov_hold=pick["ov_hold"], D_sharpe=pick["D_sharpe"]))

    G = pd.DataFrame(grid)
    P = pd.DataFrame(pairs)
    W = pd.DataFrame(wf_rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    P.to_csv(f"{OUT}.pairs.csv", index=False)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)

    gate("G3 all 336 cells published (3 panels x [34 rungs + 26 pairs x 3 lambdas])",
         len(G), "== 336", len(G) == 336)
    gate("G2 the anchor rung is bit-identical wherever it appears (it sits on all 8 ladders)",
         f"max |dret| {anchor_dev:.3e}", "< 1e-12", anchor_dev < 1e-12)
    gate("G6 no leverage: max realised weight sum over every rung and every blend",
         f"{wsum_global:.6f}", "<= 1.0 + 1e-9", wsum_global <= 1.0 + 1e-9)
    gate("G7 1509's MECHANISM REPLAYED: the lambda-blend of gross 0.50 and 1.00 equals the single "
         "gross rung at the blended exposure", f"max |dSharpe| {g7_dev:.3e}", "< 5e-3",
         g7_dev < 5e-3)
    gate("G8 netted blend turnover <= naive + split-restoration at EVERY ROW of every blend "
         "(exact triangle inequality; the NAIVE charge alone does NOT bound it, because it omits "
         "the cost of restoring the capital split)", f"{g8_viol} violations of "
         f"{n_blend} blends", "== 0", g8_viol == 0)
    publish("G8b split-restoration cost omitted by the naive charge (mean bp/yr over all blends)",
            f"{np.mean(rest_bp):.2f} bp/yr (max {np.max(rest_bp):.2f})")
    publish("G8c netted MINUS naive blend cost (mean bp/yr; positive = the naive ruler "
            "UNDER-charges a real blend)", f"{np.mean(netnaive_bp):+.2f} bp/yr "
            f"(min {np.min(netnaive_bp):+.2f}, max {np.max(netnaive_bp):+.2f})")
    say(f"    PUBLISHED: a real two-sleeve blend costs on average {np.mean(netnaive_bp):+.2f} bp/yr "
        f"MORE than the record's naive lambda-weighted charge, because the naive charge omits the "
        f"{np.mean(rest_bp):.2f} bp/yr spent restoring the capital split.  Netting saves less than "
        f"restoration costs.")
    gate("G9 the stop and the vol target are NON-ANTICIPATING (truncated-tape replay)",
         f"max |dret| {g9_dev:.3e}", "< 1e-12", g9_dev < 1e-12)
    gate("G10 deterministic recompute (L_H=63, one per panel)", f"max |dSharpe| {g10_dev:.3e}",
         "< 1e-12", g10_dev < 1e-12)
    gate("G5 the rule-8 chooser reads no row on or after 2017-01-01",
         "is_Sharpe computed on rows [WARMUP, searchsorted(2016-12-31)) only", "by construction",
         True)
    return G, P, W, panels, t0


def analyse(G, P, W, panels, t0):
    say("\n" + "=" * 124)
    say("THE 78 ADJACENT PAIRS AT lambda = 0.50 (26 pairs x 3 panels).  OV_HOLD is composition-only;")
    say("OV_CAP sees exposure too.  D = Sharpe(blend) - [lam*Sharpe(A) + (1-lam)*Sharpe(B)].")
    say("=" * 124)
    H = P[np.isclose(P.lam, 0.50)].copy()
    for p in ["U56", "B136", "SMALL"]:
        sub = H[H.panel == p]
        say(f"\n  [{p}] ladder pred          rungs        | OV_HOLD  OV_CAP  Jacc  flat1 |   "
            "Sh(A)   Sh(B)  Sh(bl) |  D_Sharpe   D_CAGR pp | turn net/naive")
        for _, r in sub.iterrows():
            say(f"    {r.ladder:<5} {r.pred_class:<11} {r.rung_a:>6}->{r.rung_b:<6} | "
                f"{r.ov_hold:7.4f} {r.ov_cap:7.4f} {r.jaccard:5.3f} {r.flat_one:5.3f} | "
                f"{r.Sharpe_A:7.4f} {r.Sharpe_B:7.4f} {r.Sharpe_blend:7.4f} | "
                f"{r.D_sharpe:+9.4f} {r.D_cagr*100:+9.3f} | "
                f"{r.turn_net_yr:5.2f}/{r.turn_naive_yr:5.2f}")

    # ---- (1) is OVERLAP a sufficient statistic? ------------------------------------------
    say("\n" + "=" * 124)
    say("(1) IS OVERLAP A SUFFICIENT STATISTIC FOR THE BLEND GAP?  Pooled OLS over all 78 pairs at "
        "lambda = 0.50.")
    say("=" * 124)
    fits = {}
    lad_names = sorted(LADDERS)
    for stat in OVSTATS:
        x = (1.0 - H[stat.lower()].values).astype(float)
        y = H["D_sharpe"].values.astype(float)
        ok = np.isfinite(x) & np.isfinite(y)
        x, y = x[ok], y[ok]
        Hs = H[ok]
        X1 = np.column_stack([np.ones_like(x), x])
        b1, res1, r2_1 = ols(X1, y)
        Dmat = np.column_stack([(Hs.ladder.values == L).astype(float) for L in lad_names[1:]])
        X2 = np.column_stack([X1, Dmat])
        _, res2, r2_2 = ols(X2, y)
        se = float(res1.std(ddof=2)) if len(res1) > 2 else np.nan
        say(f"\n  [{stat}]  D = {b1[0]:+.5f} {b1[1]:+.5f} * (1 - {stat})   "
            f"R^2 = {r2_1:.4f}   residual sd {se:.5f}")
        say(f"           + LADDER IDENTITY (8 dummies): R^2 = {r2_2:.4f}   "
            f"dR^2 = {r2_2 - r2_1:+.4f}")
        worst_t, worst_l = 0.0, ""
        say(f"           per-ladder mean residual from the {stat}-only fit:")
        for L in lad_names:
            m = Hs.ladder.values == L
            if not m.any():
                continue
            mr = float(res1[m].mean())
            t = mr / (se / np.sqrt(m.sum())) if se > 0 else np.nan
            if abs(t) > abs(worst_t):
                worst_t, worst_l = t, L
            say(f"             {L:<5} n={m.sum():<3} mean resid {mr:+.5f}  t {t:+6.2f}"
                f"   (pre-registered class {LADDERS[L]['pred']})")
        fits[stat] = dict(r2=r2_1, r2_full=r2_2, dr2=r2_2 - r2_1, worst_t=worst_t,
                          worst_ladder=worst_l, slope=b1[1], resid_sd=se)
        s1 = r2_1 >= 0.80
        s2 = (r2_2 - r2_1) < 0.05
        s3 = abs(worst_t) <= 2.0
        say(f"           PRE-REGISTERED: S1 R^2>=0.80 {'PASS' if s1 else 'FAIL'} | "
            f"S2 dR^2<0.05 {'PASS' if s2 else 'FAIL'} | S3 no ladder |t|>2 "
            f"{'PASS' if s3 else 'FAIL'} (worst {worst_l} t {worst_t:+.2f})")
        fits[stat].update(S1=s1, S2=s2, S3=s3, sufficient=bool(s1 and s2 and s3))

    # ---- (1b) POST-HOC: the exposure-state disagreement the dichotomy has no room for -----
    say("\n" + "=" * 124)
    say("(1b) POST-HOC (NOT pre-registered, and labelled as such).  OV_HOLD is blind by "
        "construction to")
    say("     days when exactly ONE rung is flat, and L_S is the one ladder whose rungs differ "
        "ONLY in that way.")
    say("     Adding flat_one -- the share of days the two rungs DISAGREE ABOUT BEING INVESTED AT "
        "ALL -- as a")
    say("     second regressor tests whether the taxonomy needs TWO numbers rather than one.")
    say("=" * 124)
    posthoc = {}
    for stat in OVSTATS:
        x1 = (1.0 - H[stat.lower()].values).astype(float)
        x2 = H["flat_one"].values.astype(float)
        y = H["D_sharpe"].values.astype(float)
        ok = np.isfinite(x1) & np.isfinite(x2) & np.isfinite(y)
        Hs = H[ok]
        X = np.column_stack([np.ones(ok.sum()), x1[ok], x2[ok]])
        b, res, r2 = ols(X, y[ok])
        Dm = np.column_stack([(Hs.ladder.values == L).astype(float) for L in lad_names[1:]])
        _, _, r2f = ols(np.column_stack([X, Dm]), y[ok])
        sd = float(res.std(ddof=3))
        wt, wl = 0.0, ""
        for L in lad_names:
            m = Hs.ladder.values == L
            if not m.any():
                continue
            t = float(res[m].mean()) / (sd / np.sqrt(m.sum())) if sd > 0 else np.nan
            if abs(t) > abs(wt):
                wt, wl = t, L
        say(f"    [{stat} + flat_one]  D = {b[0]:+.5f} {b[1]:+.5f}*(1-{stat}) {b[2]:+.5f}*flat_one"
            f"   R^2 = {r2:.4f}  (was {fits[stat]['r2']:.4f})")
        say(f"                        + ladder identity R^2 = {r2f:.4f}  dR^2 = {r2f - r2:+.4f}; "
            f"worst ladder residual {wl} t {wt:+.2f}")
        posthoc[stat] = dict(stat=stat, r2=r2, r2_full=r2f, dr2=r2f - r2, worst_t=wt,
                             worst_ladder=wl, b_ov=b[1], b_flat=b[2])
    pd.DataFrame([posthoc[s_] for s_ in OVSTATS]).to_csv(f"{OUT}.posthoc_fit.csv", index=False)

    # ---- (2) does the PRE-REGISTERED class survive measurement? ---------------------------
    say("\n" + "=" * 124)
    say("(2) DOES THE PRE-REGISTERED SCALE / COMPOSITION LABEL SURVIVE MEASUREMENT?  A pair is")
    say(f"    MEASURED SCALE iff |D_Sharpe| < {MATERIAL} at lambda = 0.50.")
    say("=" * 124)
    H = H.copy()
    H["measured"] = np.where(H.D_sharpe.abs() < MATERIAL, "SCALE", "COMPOSITION")
    tab = []
    for L in lad_names:
        sub = H[H.ladder == L]
        agree = int((sub.measured == sub.pred_class).sum())
        tab.append(dict(ladder=L, pred=LADDERS[L]["pred"], n=len(sub), agree=agree,
                        mean_ov_hold=float(sub.ov_hold.mean()),
                        mean_ov_cap=float(sub.ov_cap.mean()),
                        mean_D=float(sub.D_sharpe.mean()),
                        max_absD=float(sub.D_sharpe.abs().max())))
        say(f"    {L:<5} pred {LADDERS[L]['pred']:<11} n {len(sub):<3} agree {agree}/{len(sub)}  "
            f"mean OV_HOLD {sub.ov_hold.mean():.4f}  mean OV_CAP {sub.ov_cap.mean():.4f}  "
            f"mean D {sub.D_sharpe.mean():+.4f}  max |D| {sub.D_sharpe.abs().max():.4f}")
    Tclass = pd.DataFrame(tab)
    tot_agree = int(Tclass.agree.sum())
    say(f"\n    PRE-REGISTERED LABEL AGREES ON {tot_agree} of {len(H)} pairs "
        f"({tot_agree/len(H):.1%}).")

    # ---- (3) rule 8 on the taxonomy itself -------------------------------------------------
    say("\n" + "=" * 124)
    say("(3) RULE 8 ON THE TAXONOMY.  The cut theta on OV_HOLD is chosen on the FIRST HALF")
    say("    (warm-up..2016-12-31 blend gaps ONLY) and the 2017-2026 gaps are read ONCE.")
    say("=" * 124)
    rows8 = []
    for stat in OVSTATS:
        ov = H[stat.lower()].values.astype(float)
        yi = (H.D_sharpe_IS.abs().values >= MATERIAL)
        yo = (H.D_sharpe_OOS.abs().values >= MATERIAL)
        cands = np.unique(np.round(ov, 6))
        grid_t = np.concatenate([[-0.001], (cands[:-1] + cands[1:]) / 2.0, [1.001]]) \
            if len(cands) > 1 else np.array([0.5])
        accs = [( (ov <= th) == yi ).mean() for th in grid_t]     # low overlap -> material
        k = int(np.argmax(accs))
        th = float(grid_t[k])
        acc_is, acc_oos = float(accs[k]), float(((ov <= th) == yo).mean())
        base_is = max(yi.mean(), 1 - yi.mean())
        base_oos = max(yo.mean(), 1 - yo.mean())
        say(f"    [{stat}] theta chosen IS = {th:.4f}   IS accuracy {acc_is:.1%} "
            f"(majority-class baseline {base_is:.1%})  ->  OOS accuracy {acc_oos:.1%} "
            f"(baseline {base_oos:.1%})   {'ADEQUATE' if acc_oos >= 0.90 else 'NOT ADEQUATE'} "
            f"(bar 90%)")
        rows8.append(dict(stat=stat, theta=th, acc_IS=acc_is, acc_OOS=acc_oos,
                          base_IS=base_is, base_OOS=base_oos,
                          adequate=bool(acc_oos >= 0.90)))
    T8 = pd.DataFrame(rows8)

    # ---- (4) both KEEP paths at every cell -------------------------------------------------
    say("\n" + "=" * 124)
    say("(4) BOTH KEEP PATHS AT ALL 336 CELLS (4a vs live RULES v2; 4b vs SPY, DD cap 0.60x, "
        "CAGR floor 0.70x).")
    say("=" * 124)
    for p in ["U56", "B136", "SMALL"]:
        s = G[G.panel == p]
        say(f"    [{p}] 4a {int(s.keep4a.sum())}/{len(s)} full, {int(s.keep4a_OOS.sum())}/{len(s)} "
            f"OOS  |  4b {int(s.keep4b.sum())}/{len(s)} full, {int(s.keep4b_OOS.sum())}/{len(s)} "
            f"OOS, {int((s.keep4b & s.keep4b_OOS).sum())}/{len(s)} BOTH")
        for leg in ["H1", "H2", "DD", "CAGR"]:
            say(f"           4b leg {leg:<4} passes {int(s['leg_'+leg].sum()):>3}/{len(s)} full, "
                f"{int(s['legO_'+leg].sum()):>3}/{len(s)} OOS")
    say(f"    TOTAL 4a {int(G.keep4a.sum())}/{len(G)} full, {int(G.keep4a_OOS.sum())}/{len(G)} OOS; "
        f"4b {int(G.keep4b.sum())}/{len(G)} full, {int(G.keep4b_OOS.sum())}/{len(G)} OOS, "
        f"{int((G.keep4b & G.keep4b_OOS).sum())}/{len(G)} BOTH")

    # ---- (5) the capital arm ----------------------------------------------------------------
    say("\n" + "=" * 124)
    say("(5) RULE 8 CAPITAL ARM.  Cell chosen by argmax IS Sharpe on warm-up..2016-12-31 ONLY; "
        "2017-2026 read once.")
    say("=" * 124)
    for _, r in W.iterrows():
        say(f"    [{r.panel}] {r.chooser:<32} -> {r.cell:<28} IS {r.IS_Sharpe:.4f} | OOS "
            f"{r.OOS_CAGR:7.2%} / {r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:7.2%}  "
            f"(anchor {r.anchor_OOS_CAGR:.2%}/{r.anchor_OOS_Sharpe:.4f}/{r.anchor_OOS_MaxDD:.2%}; "
            f"SPY {r.spy_OOS_CAGR:.2%}/{r.spy_OOS_Sharpe:.4f}/{r.spy_OOS_MaxDD:.2%}; "
            f"v2 {r.live_OOS_CAGR:.2%}/{r.live_OOS_Sharpe:.4f}/{r.live_OOS_MaxDD:.2%})  "
            f"odSharpe {r.odSharpe:+.4f} t {r.odSharpe_t:+.2f}  4a {r.keep4a_OOS} 4b "
            f"{r.keep4b_OOS}")
    mix = W[W.chooser.str.startswith("ARGMAX-IS (all")]
    non = W[W.chooser.str.startswith("DO NOTHING")]
    say(f"\n    MEAN OOS SHARPE: chooser {mix.OOS_Sharpe.mean():.4f}  vs  do-nothing "
        f"{non.OOS_Sharpe.mean():.4f}  ({'CHOOSER WINS' if mix.OOS_Sharpe.mean() > non.OOS_Sharpe.mean() else 'DOING NOTHING WINS'})")

    # ---- verdict -----------------------------------------------------------------------------
    say("\n" + "=" * 124)
    say("VERDICT")
    say("=" * 124)
    best = max(OVSTATS, key=lambda s: fits[s]["r2"])
    say(f"    Best overlap statistic by pooled R^2: {best} (R^2 {fits[best]['r2']:.4f} vs "
        f"{fits[[s for s in OVSTATS if s != best][0]]['r2']:.4f}).")
    say(f"    SUFFICIENCY (S1 & S2 & S3): OV_HOLD {fits['OV_HOLD']['sufficient']}, "
        f"OV_CAP {fits['OV_CAP']['sufficient']}.")
    say(f"    BINARY TAXONOMY OOS ACCURACY: "
        + ", ".join(f"{r.stat} {r.acc_OOS:.1%}" for _, r in T8.iterrows()))
    say(f"    PRE-REGISTERED LABEL AGREEMENT: {tot_agree}/{len(H)} pairs.")
    say(f"    CAPITAL: 4a {int(G.keep4a.sum())}/{len(G)} full and {int(G.keep4a_OOS.sum())}/{len(G)}"
        f" OOS; 4b BOTH {int((G.keep4b & G.keep4b_OOS).sum())}/{len(G)}; rule-8 chooser mean OOS "
        f"Sharpe {mix.OOS_Sharpe.mean():.4f} vs do-nothing {non.OOS_Sharpe.mean():.4f}.")

    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    Tclass.to_csv(f"{OUT}.class.csv", index=False)
    pd.DataFrame([fits[s] | dict(stat=s) for s in OVSTATS]).to_csv(f"{OUT}.fit.csv", index=False)
    T8.to_csv(f"{OUT}.rule8_taxonomy.csv", index=False)
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    allpass = all(g["pass_"] for g in GATES)
    say(f"\n    ALL GATES PASS: {allpass}   ({time.time()-t0:.0f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    G, P, W, panels, t0 = main()
    analyse(G, P, W, panels, t0)

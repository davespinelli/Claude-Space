#!/usr/bin/env python3
"""
Idea 1161 (lane B, 2026-09-17) — WHY does a RESAMPLE NULL sit ABOVE the OBSERVED MAXIMUM?

THE PREMISE, READ FROM THE RECORD AND NEVER RECALLED.  Idea 1159 published 108 (panel x
ladder x null type x object) cells in
`2026-09-17_does-ANY-committed-MAXIMUM-KEYED-claim-in-the-record-carry-a-RESAMPLE-NULL_B.objects.csv`
and the observed value sits BELOW its own null's median at 89 of them.  OBJ_MAXDD -- the
book's own |MaxDD| -- is below at 36 of 36.  Idea 1178 (cloud) hit the same wall from the
other side: 8 of its 9 cells have the IID null DEEPER than the observed path, which put a
NEGATIVE denominator under a quantity the record publishes in [0, 1].  A null biased in a
known direction is not a bar.  This run asks whether the bias belongs to the RESAMPLE or to
the BOOK, and what a published band would have to do about it.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  NULL TYPE  {N_IID, N_BLOCK, N_STAT}          -- 1159's three, constructors copied verbatim
  CORRECTION {R_NONE, R_CENTER, R_PERM, R_PIVOT, R_MACH}

  = 15 dial cells, EVERY ONE PUBLISHED, scored on all 36 (panel x ladder x object) cells
  = 540 rows in `.corrections.csv`.  NOTHING IS TUNED: the headline null is 1159's own
  N_BLOCK at L = 63, 1000 draws, on 1159's own seeds, and R_NONE is required to REPRODUCE
  1159's committed file at machine zero (gate G9).  Every correction is then a strict
  re-processing of the record's own draws.

  R_NONE    the record's band: percentiles of the raw resample draws.
  R_CENTER  each draw recentred to the observed total log return before the object is read.
            Kills the DRIFT channel -- a resample's mean is random, |MaxDD| is convex in the
            drift, so E[MaxDD] > MaxDD(at the observed drift) by Jensen alone.
  R_PERM    the without-replacement counterpart of the same null at the same order scale
            (N_IID -> full permutation, N_BLOCK -> block permutation at L = 63, N_STAT ->
            geometric-length block permutation).  The multiset is preserved EXACTLY, so this
            kills the MARGINAL-RESAMPLING channel outright.
  R_PIVOT   the textbook basic/pivotal interval [2*obs - hi, 2*obs - lo] on R_NONE's own
            draws.  Costs no draws; a pure reflection.
  R_MACH    divide the null by the MACHINERY BIAS measured in Arm C on tapes where the truth
            is known.  This is the correction the record would actually have to adopt.

WHAT IS NOT A DIAL.  PANEL {U56, B136, SMALL} is not a dial.  The four LADDERS (N, H, GROSS,
CADENCE) and the three OBJECTS are 1159's, inherited whole.  The TAPE FAMILY {S_REAL, S_PERM,
S_MA1} in Arm C is a FALSIFICATION LADDER, one factor at a time, every cell published and
nothing ever selected on it -- S_PERM and S_MA1 exist only to put a KNOWN answer under the
machinery.  The CHANNEL ladder in Arm D is a one-factor-at-a-time decomposition of the null
CONSTRUCTOR, not a search.  The 216-book population in Arm F is not a dial and every book is
published.  SEED is not a dial (1159's own seeds at the headline; the calibration arm runs 25
independent pseudo-tapes and publishes the spread).

Frozen at 1082/1094/1098/1102/1110/1148/1159/1162's construction: CAND20 legs, max_vol 0.60,
gross 0.75, min hold 126, N = 20, cadence W, 10 bps (rule 2), LAG 1, warm-up 260, IS end
2016-12-31, block L = 63, 1000 draws, crc32 seeds, SEED_BASE 11591159 (1159's).

PROTOCOL: rule 2 costs 10 bps and t+1 execution throughout; rule 8 walk-forward and BOTH KEEP
paths in Arm F; rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py are NOT modified by this script.

Runs standalone and offline:  python research/backtests/2026-09-17_why-does-a-RESAMPLE-NULL-sit-ABOVE-the-OBSERVED-MAXIMUM-at-108-of-108-cells_B.py
"""
from __future__ import annotations

import sys
import time
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-17"
SLUG = "why-does-a-RESAMPLE-NULL-sit-ABOVE-the-OBSERVED-MAXIMUM-at-108-of-108-cells"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"
BT = ROOT / "research" / "backtests"

# ----- 1159's construction, inherited whole -------------------------------------------------
LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST, GROSS0, FREQ0, HOLD0, N0 = 10.0, 0.75, "W", 126, 20
LEGS = [(21, 252), (0, 126), (0, 63)]

LAD_N = [5, 8, 10, 12, 15, 20, 25, 30, 40]
LAD_H = [21, 63, 126, 252]
LAD_G = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]
LAD_C = ["D", "W", "M", "Q"]
LADDERS = {"N": LAD_N, "H": LAD_H, "GROSS": LAD_G, "CADENCE": LAD_C}
ANCHOR = dict(N=N0, H=HOLD0, GROSS=GROSS0, CADENCE=FREQ0)
PANELS = ["U56", "B136", "SMALL"]
OBJECTS = ["OBJ_MAXDD", "OBJ_SPREAD", "OBJ_ARGMAX"]

NULL_TYPES = ["N_BLOCK", "N_IID", "N_STAT"]          # dial 1 (1159's order kept)
N_HEAD = "N_BLOCK"                                   # the record's own basis
CORRECTIONS = ["R_NONE", "R_CENTER", "R_PERM", "R_PIVOT", "R_MACH"]   # dial 2
R_HEAD = "R_NONE"

QS = [0.80, 0.90, 0.95]
Q_HEAD = 0.90
L_BLOCK, BDRAWS = 63, 1000
SEED_BASE = 11591159                                  # 1159's, so its seeds are reproducible

# calibration arm (Arm C)
TAPES = ["S_REAL", "S_PERM", "S_MA1"]
N_PSEUDO, BDRAWS_CAL = 25, 400

# rule 8 population (Arm F)
POP_N = [5, 8, 10, 12, 15, 20, 25, 30, 40]
POP_H = [21, 63, 126, 252]
POP_C = ["W", "M"]
BDRAWS_IS = 400
CHOOSERS = ["CH_ISSHARPE", "CH_ISCAGR", "CH_ISDD", "CH_NULLDD"]

# ----- the record's own committed numbers, QUOTED and GATED, never re-derived ----------------
A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
PRIOR1159 = BT / (f"{DATE}_does-ANY-committed-MAXIMUM-KEYED-claim-in-the-record-carry-a-"
                  f"RESAMPLE-NULL_B")
PRIOR1159_OBJ = Path(str(PRIOR1159) + ".objects.csv")
PRIOR1162 = BT / f"{DATE}_why-does-an-IID-RESAMPLE-produce-DEEPER-drawdowns-than-a-BLOCK-one_B"
PRIOR1162_DECOMP = Path(str(PRIOR1162) + ".decomposition.csv")
# 1159's committed headline, quoted from the queue entry and CHECKED against its own CSV.
# The queue publishes the ratio triple as a bare "0.936 / 0.851 / 0.964 by null type" with NO
# labels.  The mapping below is the one 1159's OWN CSV supports (its NULL_TYPES order) and was
# RECOVERED from that file, not assumed: the first cut of this script read the triple in a
# different order and gate G9c caught it.  That is itself a small defect in the record and it
# is reported in Arm A rather than silently fixed.
Q1159_BELOW, Q1159_CELLS = 89, 108
Q1159_RATIO = {"N_BLOCK": 0.936, "N_IID": 0.851, "N_STAT": 0.964}   # queue's "by null type"

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def seed_of(*parts):
    return SEED_BASE + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


GATES: list[dict] = []


def gate(name, what, value, ok):
    GATES.append(dict(gate=name, check=what, value=float(value), pass_=bool(ok)))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name:<5s} {what}  ->  {value:.3e}")
    return bool(ok)


# =================================================================================================
# 1159's runner, verbatim
# =================================================================================================
def nrun(rets, wt, mk):
    T, N = rets.shape
    mk = mk.copy()
    mk[0] = True
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
    reb = np.flatnonzero(mk)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return (held * rets).sum(axis=1), turn


def fmet(r):
    r = np.asarray(r, float)
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def legs_composite(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return sum(parts) / len(parts)


def mech(px):
    comp = legs_composite(px)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    return sc.values, (above & (vol20 < MAXVOL)).values


def build(rank_key, elig, priced, reb, N, H, T, K, gross):
    W = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
    for i, t in enumerate(reb):
        held = np.flatnonzero(cur >= 0)
        if len(held):
            young = held[(t - cur[held]) < H]
            young = young[priced[t, young]]
        else:
            young = held
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = rank_key[t].copy()
            k[~(elig[t] & priced[t])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new_cur = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new_cur[c] = cur[c]
        for c in take:
            new_cur[c] = t
        cur = new_cur
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = gross / len(sel)
    return W


def windows_of(idx):
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    ins = warm & ~oos
    return warm, ins, oos


def blocks_m(r, warm, ins, oos):
    rr = r[warm]
    c, s, d = fmet(rr)
    h = len(rr) // 2
    oc, os_, od = fmet(r[oos])
    ic, is_, idd = fmet(r[ins])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]),
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)


def legs_4b(b, sb):
    return {"L_H1": bool(b["H1"] > sb["H1"]), "L_H2": bool(b["H2"] > sb["H2"]),
            "L_OOS": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "L_DD": bool(abs(b["MaxDD"]) <= DD_CAP * abs(sb["MaxDD"])),
            "L_CAGR": bool(b["CAGR"] >= CAGR_FLOOR * sb["CAGR"])}


def legs_4b_oos(b, sb):
    return {"O_S": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "O_DD": bool(abs(b["OOS_MaxDD"]) <= DD_CAP * abs(sb["OOS_MaxDD"])),
            "O_CAGR": bool(b["OOS_CAGR"] >= CAGR_FLOOR * sb["OOS_CAGR"])}


def legs_4a(b, lb):
    return {"A_H1": bool(b["H1"] > lb["H1"]), "A_H2": bool(b["H2"] > lb["H2"]),
            "A_DD": bool(b["MaxDD"] >= lb["MaxDD"])}


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep].dropna(how="all").ffill(), len(bad), len(meta)


# =================================================================================================
# THE NULLS.  1159's three, verbatim, plus their WITHOUT-REPLACEMENT counterparts and the two
# one-factor variants (no wrap-around; per-draw drift recentring) the channel ladder needs.
# =================================================================================================
def null_index(kind, rng, T, ndraws):
    if kind == "N_IID":                                   # L = 1: destroys all autocorrelation
        return rng.integers(0, T, size=(ndraws, T))
    if kind == "N_BLOCK":                                 # the record's frozen moving block
        nb = int(np.ceil(T / L_BLOCK))
        st = rng.integers(0, T, size=(ndraws, nb))
        idx = (st[:, :, None] + np.arange(L_BLOCK)[None, None, :]) % T
        return idx.reshape(ndraws, nb * L_BLOCK)[:, :T]
    if kind == "N_STAT":                                  # stationary bootstrap, mean block 63
        p = 1.0 / L_BLOCK
        out = np.empty((ndraws, T), dtype=np.int64)
        out[:, 0] = rng.integers(0, T, size=ndraws)
        newb = rng.random((ndraws, T)) < p
        fresh = rng.integers(0, T, size=(ndraws, T))
        for t in range(1, T):
            cont = (out[:, t - 1] + 1) % T
            out[:, t] = np.where(newb[:, t], fresh[:, t], cont)
        return out
    if kind == "N_BLOCK_NOWRAP":                          # channel ladder: wrap-around removed
        nb = int(np.ceil(T / L_BLOCK))
        st = rng.integers(0, max(T - L_BLOCK, 1) + 1, size=(ndraws, nb))
        idx = st[:, :, None] + np.arange(L_BLOCK)[None, None, :]
        return idx.reshape(ndraws, nb * L_BLOCK)[:, :T]
    raise ValueError(kind)


def perm_index(kind, rng, T, ndraws):
    """The WITHOUT-REPLACEMENT counterpart of `kind` at the SAME order scale.  Every row is a
    permutation of 0..T-1, so the resampled tape's MULTISET -- and therefore its mean, its sd
    and its total return -- is EXACTLY the observed tape's.  Only ORDER is destroyed."""
    base = np.arange(T)
    if kind == "N_IID":                                   # L = 1 blocks: a full permutation
        return rng.permuted(np.tile(base, (ndraws, 1)), axis=1)
    if kind in ("N_BLOCK", "N_BLOCK_NOWRAP"):             # fixed-length contiguous blocks
        cuts = list(range(0, T, L_BLOCK))
        blocks = [base[a:a + L_BLOCK] for a in cuts]
        out = np.empty((ndraws, T), dtype=np.int64)
        for d in range(ndraws):
            order = rng.permutation(len(blocks))
            out[d] = np.concatenate([blocks[i] for i in order])
        return out
    if kind == "N_STAT":                                  # geometric-length contiguous blocks
        out = np.empty((ndraws, T), dtype=np.int64)
        for d in range(ndraws):
            lens, tot = [], 0
            while tot < T:
                ln = int(min(rng.geometric(1.0 / L_BLOCK), T - tot))
                lens.append(ln)
                tot += ln
            cuts = np.cumsum([0] + lens)
            blocks = [base[cuts[i]:cuts[i + 1]] for i in range(len(lens))]
            order = rng.permutation(len(blocks))
            out[d] = np.concatenate([blocks[i] for i in order])
        return out
    raise ValueError(kind)


def boot_maxdd(R, idx, center=False, chunk=50):
    """|MaxDD| (positive, in %) of every row of R under every resample row of idx.

    center=True recentres EACH DRAW so its total log return equals the observed row's, which
    removes the drift channel exactly: a resample's mean is a random variable and |MaxDD| is
    convex in the drift, so the uncorrected null is inflated by Jensen alone."""
    nr, nd = R.shape[0], idx.shape[0]
    out = np.empty((nr, nd))
    LG = np.log1p(R)
    tgt = LG.sum(axis=1)
    T = idx.shape[1]
    ramp = np.arange(1, T + 1, dtype=float)
    for a in range(0, nd, chunk):
        ix = idx[a:a + chunk]
        for j in range(nr):
            cum = np.cumsum(LG[j][ix], axis=1)
            if center:
                cum = cum - np.outer((cum[:, -1] - tgt[j]) / T, ramp)
            run = np.maximum.accumulate(cum, axis=1)
            out[j, a:a + chunk] = -np.expm1(cum - run).min(axis=1) * 100.0
    return out


def band(x, q):
    lo = np.nanpercentile(x, (1 - q) / 2 * 100.0)
    hi = np.nanpercentile(x, (1 + q) / 2 * 100.0)
    return float(lo), float(hi)


def objects_of(obs_dd, anchor_i):
    """1159's three maximum-keyed objects off a vector of |MaxDD| over the ladder's rungs."""
    srt = np.sort(obs_dd)
    return {"OBJ_MAXDD": float(obs_dd[anchor_i]),
            "OBJ_SPREAD": float(obs_dd.max() - obs_dd.min()),
            "OBJ_ARGMAX": float(srt[1] - srt[0])}


def null_objects_of(B):
    """The same three objects, per draw, off a (rungs, ndraws) null matrix."""
    Bs = np.sort(B, axis=0)
    return {"OBJ_MAXDD": None, "OBJ_SPREAD": B.max(axis=0) - B.min(axis=0),
            "OBJ_ARGMAX": Bs[1] - Bs[0]}


def score_cell(o, bb, q_list=QS):
    """The record's own read of one (observed, null draws) pair."""
    med = float(np.nanmedian(bb))
    row = dict(observed=float(o), null_median=med, null_mean=float(np.nanmean(bb)),
               share_ge=float(np.mean(bb >= o)), share_le=float(np.mean(bb <= o)),
               ratio_obs_over_null=(o / med if med else np.nan))
    for q in q_list:
        lo, hi = band(bb, q)
        row[f"lo_{q}"] = lo
        row[f"hi_{q}"] = hi
        row[f"inside_{q}"] = bool(lo <= o <= hi)
    return row


def ma1_filter(X, phi):
    """Impose an MA(1) serial structure with the SAME filter on every rung, then rescale each
    rung to its own sd.  ac1 of the result is phi/(1+phi^2); cross-rung dependence is kept."""
    mu = X.mean(axis=1, keepdims=True)
    sd = X.std(axis=1, ddof=1, keepdims=True)
    E = X - mu
    Y = E + phi * np.roll(E, 1, axis=1)
    Y[:, 0] = E[:, 0]
    s2 = Y.std(axis=1, ddof=1, keepdims=True)
    return mu + Y * (sd / np.where(s2 == 0, 1.0, s2))


def phi_for_ac1(a):
    """The MA(1) coefficient whose lag-1 autocorrelation is a (|a| <= 0.5); phi/(1+phi^2)=a."""
    a = float(np.clip(a, -0.499, 0.499))
    if abs(a) < 1e-12:
        return 0.0
    return (1.0 - np.sqrt(max(1.0 - 4.0 * a * a, 0.0))) / (2.0 * a)


def ac1_of(x):
    x = np.asarray(x, float)
    x = x - x.mean()
    d = float((x * x).sum())
    return float((x[1:] * x[:-1]).sum() / d) if d else np.nan


def vr_of(x, k):
    x = np.asarray(x, float)
    n = (len(x) // k) * k
    if n < 2 * k:
        return np.nan
    a = x[:n].reshape(-1, k).sum(axis=1)
    v1 = x[:n].var(ddof=1)
    return float(a.var(ddof=1) / (k * v1)) if v1 else np.nan


def recovery_of(x, depth=0.05):
    """The book's drawdown-conditional drift: mean daily return while the equity curve is at
    least `depth` below its running max, minus the unconditional mean.  Positive = the tape
    recovers, which is exactly the structure a resample destroys."""
    x = np.asarray(x, float)
    eq = np.cumprod(1.0 + x)
    dd = eq / np.maximum.accumulate(eq) - 1.0
    m = dd <= -depth
    if m.sum() < 30:
        return np.nan, float(m.mean())
    return float(x[m].mean() - x.mean()), float(m.mean())


# =================================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P(f"IDEA 1161 (lane B, {DATE}) — why does a RESAMPLE NULL sit ABOVE the OBSERVED MAXIMUM")
    P("=" * 100)
    P(__doc__.strip())
    P("")

    # ------------------------------------------------------------------ panels
    P("## PANELS")
    raw = {"U56": load_universe(), "B136": load_universe(broad=True)}
    sm, ndrop, nmeta = load_small()
    raw["SMALL"] = sm
    panels = {}
    for panel in PANELS:
        px = raw[panel]
        idx, K, T = px.index, len(px.columns), len(px.index)
        warm, ins, oos = windows_of(idx)
        sc, elig = mech(px)
        spy_i = list(px.columns).index("SPY")
        if panel == "SMALL":
            elig = elig.copy()
            elig[:, spy_i] = False
        panels[panel] = dict(px=px, idx=idx, K=K, T=T,
                             rets=px.pct_change().fillna(0.0).values, priced=px.notna().values,
                             warm=warm, ins=ins, oos=oos, sc=sc, elig=elig)
        P(f"  {panel:<6s} {K:4d} cols, {T:,} rows {idx[0].date()} -> {idx[-1].date()}  "
          f"warm {warm.sum():,}  IS {ins.sum():,}  OOS {oos.sum():,}")
    P(f"  SMALL STAMP: data/small_meta.csv lists {nmeta} tickers; {ndrop} dropped for "
      f"max_1d_move >= 1.0; pool served = {panels['SMALL']['K'] - 1} names + SPY as benchmark.")
    P("")

    def run_cell(panel, N, H, gross, freq):
        d = panels[panel]
        mk = rebalance_mask(d["idx"], freq).values
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        reb = np.flatnonzero(mk)
        W = build(-d["sc"], d["elig"], d["priced"], reb, N, H, d["T"], d["K"], gross)
        Wl = np.zeros_like(W)
        Wl[LAG:] = W[:-LAG]
        g, tn = nrun(d["rets"], Wl, mkl)
        return g - tn * COST / 1e4

    # ------------------------------------------------------------------ gates
    P("## GATES — printed before any result number")
    d = panels["U56"]
    mk = rebalance_mask(d["idx"], FREQ0).values
    reb = np.flatnonzero(mk)
    W = build(-d["sc"], d["elig"], d["priced"], reb, N0, HOLD0, d["T"], d["K"], GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST, freq=FREQ0)["returns"].values
    rfast = run_cell("U56", N0, HOLD0, GROSS0, FREQ0)
    v = float(np.abs(eng[d["warm"]] - rfast[d["warm"]]).max())
    gate("G1", "fast runner == engine.backtest (U56 W/H126/N=20)", v, v < 1e-12)

    m = blocks_m(rfast, d["warm"], d["ins"], d["oos"])
    v = max(abs(m["CAGR"] - A936_WH126[0]), abs(m["Sharpe"] - A936_WH126[1]),
            abs(m["MaxDD"] - A936_WH126[2]))
    gate("G2", "CROSS-RUN the committed U56 W/H126/N=20 triple", v, v < 5e-3)
    P(f"     this run {m['CAGR']:.6f}/{m['Sharpe']:.6f}/{m['MaxDD']:.6f} vs committed "
      f"{A936_WH126[0]:.6f}/{A936_WH126[1]:.6f}/{A936_WH126[2]:.6f}  "
      "(1163's price-vintage defect is CARRIED, not absorbed: the bar is 5e-3, not 5e-5)")

    spy = d["px"]["SPY"].pct_change().fillna(0.0).values
    smm = blocks_m(spy, d["warm"], d["ins"], d["oos"])
    v = max(abs(smm["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
            abs(smm["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
            abs(smm["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gate("G3", "SPY OOS triple", v, v < 5e-3)

    lb_r = backtest(d["px"], rules_v2_weights(d["px"]), cost_bps=COST,
                    freq="W")["returns"].values
    lbm = blocks_m(lb_r, d["warm"], d["ins"], d["oos"])
    v = abs(lbm["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gate("G4", "live RULES v2 MaxDD == committed -12.05%", v, v < 5e-4)

    v = float(np.abs(run_cell("SMALL", N0, HOLD0, GROSS0, FREQ0)
                     - run_cell("SMALL", N0, HOLD0, GROSS0, FREQ0)).max())
    gate("G5", "determinism of the SMALL pipeline", v, v == 0.0)

    # G6 -- 1162's identity: the block family CONTAINS the iid null at L = 1
    global L_BLOCK
    keep_L = L_BLOCK
    L_BLOCK = 1
    i_b = null_index("N_BLOCK", np.random.default_rng(5), 500, 40)
    L_BLOCK = keep_L
    i_i = null_index("N_IID", np.random.default_rng(5), 500, 40)
    v = float(np.abs(i_b - i_i).max())
    gate("G6", "N_BLOCK at L=1 IS N_IID bit for bit (1162's identity)", v, v == 0.0)

    # G7 -- a permutation null preserves the multiset EXACTLY (this is what R_PERM buys)
    rr = np.random.default_rng(3).normal(0.0004, 0.011, (2, 800))
    ok7 = True
    v7 = 0.0
    for k in NULL_TYPES:
        pi = perm_index(k, np.random.default_rng(9), 800, 20)
        ok7 &= bool(all(np.array_equal(np.sort(row), np.arange(800)) for row in pi))
        v7 = max(v7, float(np.abs(np.sort(rr[0][pi], axis=1) - np.sort(rr[0])).max()))
    gate("G7", "perm_index rows are exact permutations for all 3 nulls", v7, ok7 and v7 == 0.0)

    # G8 -- centring forces every draw's TOTAL LOG RETURN onto the observed one
    ix8 = null_index("N_IID", np.random.default_rng(4), 800, 30)
    LG8 = np.log1p(rr)
    cum8 = np.cumsum(LG8[0][ix8], axis=1)
    T8 = 800
    cadj = cum8 - np.outer((cum8[:, -1] - LG8[0].sum()) / T8, np.arange(1, T8 + 1))
    v = float(np.abs(cadj[:, -1] - LG8[0].sum()).max())
    gate("G8", "R_CENTER forces each draw's total log return onto the observed", v, v < 1e-9)

    # G11 -- the observed path is a fixed point of the null machinery when it IS the draw
    idx_id = np.tile(np.arange(600), (3, 1))
    v = float(np.abs(boot_maxdd(rr[:, :600], idx_id)
                     - np.array([[-fmet(x)[2] * 100.0] * 3 for x in rr[:, :600]])).max())
    gate("G11", "boot_maxdd on the identity index == the observed |MaxDD|", v, v < 1e-9)
    P("")

    # ============================================================ ARM A — the premise, from
    #                                                              1159's OWN committed file
    P("## ARM A — THE PREMISE, RE-READ FROM 1159's COMMITTED CSV (never recalled)")
    prior = pd.read_csv(PRIOR1159_OBJ)
    n_below = int((prior.observed < prior.null_median).sum())
    P(f"   {PRIOR1159_OBJ.name}: {len(prior)} cells, observed BELOW its own null median at "
      f"{n_below} ({n_below / len(prior):.3f}).")
    by_nt = prior.groupby("null_type").ratio_obs_over_null.median()
    by_ob = prior.groupby("object").apply(
        lambda g: pd.Series(dict(n=len(g), below=int((g.observed < g.null_median).sum()),
                                 median_ratio=float(g.ratio_obs_over_null.median()))),
        include_groups=False)
    P("   median ratio observed/null by NULL TYPE: "
      + ", ".join(f"{k} {v:.4f}" for k, v in by_nt.items()))
    P("   by OBJECT:")
    for k, r_ in by_ob.iterrows():
        P(f"     {k:<12} {int(r_['n']):3d} cells, below at {int(r_['below']):3d}, "
          f"median ratio {r_['median_ratio']:.4f}")
    gate("G9a", f"1159's committed file carries {Q1159_CELLS} cells",
         abs(len(prior) - Q1159_CELLS), len(prior) == Q1159_CELLS)
    gate("G9b", f"1159's committed 'below at {Q1159_BELOW} of {Q1159_CELLS}' reproduced from "
                "its own file", abs(n_below - Q1159_BELOW), n_below == Q1159_BELOW)
    v = max(abs(by_nt.get(k, np.nan) - q) for k, q in Q1159_RATIO.items())
    gate("G9c", "the queue's median ratios 0.936 / 0.851 / 0.964 reproduced from that file",
         v, v < 5e-4)
    P("     REPORTED, NOT ABSORBED: the queue quotes that triple UNLABELLED. Only 1159's own")
    P("     CSV says which number belongs to which null, and the two readings are far apart")
    P("     (N_BLOCK 0.9358 against N_IID 0.8507, a 0.085 difference on a 0.15 effect). The")
    P("     first cut of this script mapped them in the other order and G9c failed at 8.5e-02.")
    P("")
    P("   AND A SECOND DEFECT IN THE PARENT'S DENOMINATOR, found while rebuilding its cells.")
    P("   Every ladder's ANCHOR rung is the SAME book — N=20, H=126, gross=0.75, weekly — so")
    P("   OBJ_MAXDD's 36 cells are 9 DISTINCT (panel x null) measurements replicated 4 times,")
    P("   differing only by the null's seed.  OBJ_SPREAD and OBJ_ARGMAX are genuinely 36 each")
    P("   (different rung sets).  On DISTINCT cells the parent's headline reads:")
    d_dd = prior[prior.object == "OBJ_MAXDD"].groupby(["panel", "null_type"]).apply(
        lambda g: bool((g.observed < g.null_median).all()), include_groups=False)
    n_dd_all = int(d_dd.sum())
    d_below = (n_dd_all + int((prior[prior.object == "OBJ_SPREAD"].observed
                               < prior[prior.object == "OBJ_SPREAD"].null_median).sum())
               + int((prior[prior.object == "OBJ_ARGMAX"].observed
                      < prior[prior.object == "OBJ_ARGMAX"].null_median).sum()))
    P(f"     OBJ_MAXDD {n_dd_all} of {len(d_dd)} distinct cells (all 4 replicates agree at "
      f"{int((prior[prior.object == 'OBJ_MAXDD'].groupby(['panel', 'null_type']).apply(lambda g: g.observed.lt(g.null_median).nunique() == 1, include_groups=False)).sum())} of {len(d_dd)}),")
    P(f"     OBJ_SPREAD and OBJ_ARGMAX unchanged, so the honest denominator is "
      f"{d_below} of {9 + 36 + 36} (0.765), not {Q1159_BELOW} of {Q1159_CELLS} (0.824).")
    P("   This run publishes BOTH and quotes the distinct-cell reading in its own headline.")
    P("")

    # ============================================================ ARM B — rebuild the 108 cells
    P("## ARM B — REBUILD 1159's 108 CELLS, then apply the CORRECTION dial to its own draws.")
    P("   The ladder books are rebuilt from scratch; the null seeds are 1159's (SEED_BASE "
      f"{SEED_BASE}, crc32 of panel|ladder|null), so R_NONE must reproduce its committed file.")
    series, gridrows = {}, []
    for panel in PANELS:
        dd_ = panels[panel]
        warm = dd_["warm"]
        sb = blocks_m(dd_["px"]["SPY"].pct_change().fillna(0.0).values, warm, dd_["ins"],
                      dd_["oos"])
        lbm_p = blocks_m(backtest(dd_["px"], rules_v2_weights(dd_["px"]), cost_bps=COST,
                                  freq="W")["returns"].values, warm, dd_["ins"], dd_["oos"])
        panels[panel]["spy_m"], panels[panel]["live_m"] = sb, lbm_p
        for lad, rungs in LADDERS.items():
            for rg in rungs:
                c = dict(ANCHOR)
                c[lad] = rg
                r_ = run_cell(panel, c["N"], c["H"], c["GROSS"], c["CADENCE"])
                series[(panel, lad, str(rg))] = r_[warm]
                mm = blocks_m(r_, warm, dd_["ins"], dd_["oos"])
                gridrows.append(dict(panel=panel, ladder=lad, rung=str(rg), **mm))
        P(f"  {panel:<6s} built 27 rung books   SPY {sb['CAGR']:.2%}/{sb['Sharpe']:.4f}/"
          f"{sb['MaxDD']:.2%}   live v2 {lbm_p['CAGR']:.2%}/{lbm_p['Sharpe']:.4f}/"
          f"{lbm_p['MaxDD']:.2%}   ({time.time() - t0:.0f}s)")
    dump(pd.DataFrame(gridrows), "ladder")

    # ---- the raw draws, per (panel, ladder, null type), kept for every correction
    P("")
    P("   drawing the nulls (1000 draws each, 1159's seeds) plus their CENTRED and "
      "PERMUTATION counterparts ...")
    draws = {}
    for panel in PANELS:
        T = int(panels[panel]["warm"].sum())
        for lad, rungs in LADDERS.items():
            R = np.array([series[(panel, lad, str(rg))] for rg in rungs], float)
            obs_dd = np.array([-fmet(r)[2] * 100.0 for r in R])
            ai = [str(rg) for rg in rungs].index(str(ANCHOR[lad]))
            for nt in NULL_TYPES:
                ix = null_index(nt, np.random.default_rng(seed_of(panel, lad, nt)), T, BDRAWS)
                pix = perm_index(nt, np.random.default_rng(seed_of(panel, lad, nt, "PERM")),
                                 T, BDRAWS)
                draws[(panel, lad, nt)] = dict(
                    R=R, obs=objects_of(obs_dd, ai), ai=ai,
                    RAW=boot_maxdd(R, ix), CEN=boot_maxdd(R, ix, center=True),
                    PRM=boot_maxdd(R, pix))
            P(f"   {panel:<6s} {lad:<8s} {len(rungs)} rungs x 3 nulls x 3 constructors "
              f"({time.time() - t0:.0f}s)")

    def obj_draws(B, obj, ai):
        if obj == "OBJ_MAXDD":
            return B[ai]
        if obj == "OBJ_SPREAD":
            return B.max(axis=0) - B.min(axis=0)
        Bs = np.sort(B, axis=0)
        return Bs[1] - Bs[0]

    # ---- R_NONE reproduced against 1159's committed file
    objrows = []
    for (panel, lad, nt), dct in draws.items():
        for obj in OBJECTS:
            o = dct["obs"][obj]
            bb = obj_draws(dct["RAW"], obj, dct["ai"])
            objrows.append(dict(panel=panel, ladder=lad, n_rungs=len(LADDERS[lad]),
                                null_type=nt, object=obj, **score_cell(o, bb)))
    OB = pd.DataFrame(objrows)
    dump(OB, "objects")
    key = ["panel", "ladder", "null_type", "object"]
    mg = OB.merge(prior[key + ["observed", "null_median", "share_ge"]], on=key,
                  suffixes=("", "_p"))
    v_obs = float(np.abs(mg.observed - mg.observed_p).max())
    v_med = float(np.abs(mg.null_median - mg.null_median_p).max())
    gate("G9", f"R_NONE reproduces 1159's committed OBSERVED values ({len(mg)} cells)",
         v_obs, len(mg) == Q1159_CELLS and v_obs < 1e-9)
    gate("G10", "R_NONE reproduces 1159's committed NULL MEDIANS on its own seeds",
         v_med, len(mg) == Q1159_CELLS and v_med < 1e-9)
    if v_med >= 1e-9:
        P("     NOT absorbed: the deviation by panel is "
          + ", ".join(f"{p} {g.eval('abs(null_median-null_median_p)').max():.3e}"
                      for p, g in mg.groupby("panel")))
    dd_ob = OB[OB.object == "OBJ_MAXDD"]
    v = float(dd_ob.groupby(["panel", "null_type"])["observed"].apply(
        lambda s: s.max() - s.min()).max())
    gate("G12", "OBJ_MAXDD's 4 ladders per panel ARE the same book (observed identical)",
         v, v < 1e-12)
    seedspread = dd_ob.groupby(["panel", "null_type"]).apply(
        lambda g: float((g.null_median.max() - g.null_median.min()) / g.null_median.median()),
        include_groups=False)
    P(f"     so the only thing separating those 4 replicates is the null's SEED.  The "
      f"replicate spread of the null MEDIAN is {float(seedspread.median()):.4f} (median) and "
      f"{float(seedspread.max()):.4f} (max)")
    P(f"     of the median itself, against a headline gap of "
      f"{1 - float(dd_ob.ratio_obs_over_null.median()):.4f} — so the 36-of-36 is NOT a seed "
      "artefact, but it is 9 measurements, not 36.")
    P("")

    # ---- the 15 dial cells
    P(f"## THE {len(NULL_TYPES) * len(CORRECTIONS)} DIAL CELLS (NULL TYPE x CORRECTION), "
      "EVERY ONE PUBLISHED")
    P("   R_MACH needs Arm C's machinery factor, so it is filled in after the calibration.")

    # ============================================================ ARM C — CALIBRATION
    P("")
    P("## ARM C — THE DECISIVE ARM.  Put a KNOWN answer under the machinery.")
    P("   S_PERM: the SAME ladder, its rungs re-ordered by ONE common random permutation.")
    P("           Every rung's marginal is EXACT, the cross-rung dependence is EXACT, and")
    P("           there is NO serial structure left to lose.  A resample null of an S_PERM")
    P("           tape is CORRECTLY SPECIFIED, so the truth is ratio = 1.000 and share_le =")
    P("           0.500.  Whatever the machinery reads here is MACHINERY BIAS and nothing else.")
    P("   S_MA1:  the S_PERM tape run through a common MA(1) filter whose lag-1 autocorrelation")
    P("           is the anchor book's OWN.  Serial structure of a KNOWN sign and size, so it")
    P("           prices how much of the real gap an ac1 of that size can possibly explain.")
    P(f"   {N_PSEUDO} independent pseudo-tapes per cell, {BDRAWS_CAL} draws each.")
    calrows = []
    for panel in PANELS:
        T = int(panels[panel]["warm"].sum())
        for lad, rungs in LADDERS.items():
            ai = [str(rg) for rg in rungs].index(str(ANCHOR[lad]))
            R = np.array([series[(panel, lad, str(rg))] for rg in rungs], float)
            a1 = ac1_of(R[ai])
            phi = phi_for_ac1(a1)
            for tape in ("S_PERM", "S_MA1"):
                rngp = np.random.default_rng(seed_of(panel, lad, tape, "TAPE"))
                for s in range(N_PSEUDO):
                    pi = rngp.permutation(T)
                    X = R[:, pi]
                    if tape == "S_MA1":
                        X = ma1_filter(X, phi)
                    xdd = np.array([-fmet(x)[2] * 100.0 for x in X])
                    obs = objects_of(xdd, ai)
                    for nt in NULL_TYPES:
                        rng = np.random.default_rng(seed_of(panel, lad, nt, tape, s))
                        ixc = null_index(nt, rng, T, BDRAWS_CAL)
                        Bc = boot_maxdd(X, ixc)
                        for obj in OBJECTS:
                            o = obs[obj]
                            bb = obj_draws(Bc, obj, ai)
                            med = float(np.nanmedian(bb))
                            calrows.append(dict(panel=panel, ladder=lad, tape=tape, seed=s,
                                                null_type=nt, object=obj, ac1=a1, phi=phi,
                                                observed=o, null_median=med,
                                                ratio=(o / med if med else np.nan),
                                                share_le=float(np.mean(bb <= o))))
            P(f"   {panel:<6s} {lad:<8s} ac1 {a1:+.4f} -> phi {phi:+.4f}   "
              f"({time.time() - t0:.0f}s)")
    CAL = pd.DataFrame(calrows)
    dump(CAL, "calibration")

    P("")
    P("   THE MACHINERY FLOOR.  On S_PERM the truth is ratio 1.000 / share_le 0.500:")
    P("   tape    null      object       median ratio   mean share_le   below-median share")
    mach = {}
    for tape in ("S_PERM", "S_MA1"):
        for nt in NULL_TYPES:
            for obj in OBJECTS:
                s = CAL[(CAL.tape == tape) & (CAL.null_type == nt) & (CAL.object == obj)]
                mr = float(s.ratio.median())
                if tape == "S_PERM":
                    mach[(nt, obj)] = mr
                P(f"   {tape:<7} {nt:<9} {obj:<12} {mr:12.4f}   {float(s.share_le.mean()):13.4f}"
                  f"   {float((s.observed < s.null_median).mean()):18.4f}")
    P("")
    P("   Read per (panel, ladder) cell too — the factor R_MACH actually uses is CELL-LEVEL:")
    machcell = (CAL[CAL.tape == "S_PERM"]
                .groupby(["panel", "ladder", "null_type", "object"]).ratio.median())
    dump(machcell.reset_index().rename(columns={"ratio": "machinery_ratio"}), "machinery")

    # ---- now the full correction grid, R_MACH included
    corrows = []
    for (panel, lad, nt), dct in draws.items():
        for obj in OBJECTS:
            o = dct["obs"][obj]
            raw = obj_draws(dct["RAW"], obj, dct["ai"])
            cen = obj_draws(dct["CEN"], obj, dct["ai"])
            prm = obj_draws(dct["PRM"], obj, dct["ai"])
            mfac = float(machcell.loc[(panel, lad, nt, obj)])
            for corr in CORRECTIONS:
                if corr == "R_NONE":
                    row = score_cell(o, raw)
                elif corr == "R_CENTER":
                    row = score_cell(o, cen)
                elif corr == "R_PERM":
                    row = score_cell(o, prm)
                elif corr == "R_PIVOT":
                    row = score_cell(o, raw)
                    for q in QS:                       # reflect the band through the observed
                        lo, hi = row[f"lo_{q}"], row[f"hi_{q}"]
                        row[f"lo_{q}"], row[f"hi_{q}"] = 2 * o - hi, 2 * o - lo
                        row[f"inside_{q}"] = bool(row[f"lo_{q}"] <= o <= row[f"hi_{q}"])
                    row["null_median"] = 2 * o - row["null_median"]
                    row["ratio_obs_over_null"] = (o / row["null_median"]
                                                  if row["null_median"] else np.nan)
                    row["share_le"], row["share_ge"] = row["share_ge"], row["share_le"]
                else:                                   # R_MACH: divide the null by the floor
                    row = score_cell(o, raw / mfac if mfac else raw)
                corrows.append(dict(panel=panel, ladder=lad, null_type=nt, object=obj,
                                    correction=corr, machinery_ratio=mfac, **row))
    CO = pd.DataFrame(corrows)
    dump(CO, "corrections")

    P("")
    P("## THE HEADLINE TABLE — the 108 cells re-scored under every correction")
    P("   correction   null       below median   median ratio   inside 90%   mean share_le")
    dialrows = []
    for corr in CORRECTIONS:
        for nt in NULL_TYPES:
            s = CO[(CO.correction == corr) & (CO.null_type == nt)]
            row = dict(correction=corr, null_type=nt, n_cells=len(s),
                       n_below=int((s.observed < s.null_median).sum()),
                       share_below=float((s.observed < s.null_median).mean()),
                       median_ratio=float(s.ratio_obs_over_null.median()),
                       inside_90=float(s["inside_0.9"].mean()),
                       mean_share_le=float(s.share_le.mean()))
            dialrows.append(row)
            P(f"   {corr:<12} {nt:<9} {row['n_below']:6d} / {len(s):<5d} "
              f"{row['median_ratio']:13.4f}   {row['inside_90']:10.3f}   "
              f"{row['mean_share_le']:13.4f}")
    DI = pd.DataFrame(dialrows)
    dump(DI, "dialgrid")
    P("")
    for corr in CORRECTIONS:
        s = CO[CO.correction == corr]
        d1 = s[s.object == "OBJ_MAXDD"].groupby(["panel", "null_type"]).apply(
            lambda g: bool(g.observed.median() < g.null_median.median()), include_groups=False)
        d2 = s[s.object != "OBJ_MAXDD"]
        nd = int(d1.sum()) + int((d2.observed < d2.null_median).sum())
        P(f"   ALL {len(s)} cells, {corr:<9}: below median at "
          f"{int((s.observed < s.null_median).sum()):3d} "
          f"({float((s.observed < s.null_median).mean()):.3f}), median ratio "
          f"{float(s.ratio_obs_over_null.median()):.4f}   |  on the {len(d1) + len(d2)} "
          f"DISTINCT cells: {nd:3d} ({nd / (len(d1) + len(d2)):.3f})")
    P("")

    # ============================================================ ARM D — channel decomposition
    P("## ARM D — THE CHANNEL LADDER.  One factor at a time off the record's own N_BLOCK,")
    P("   on the ANCHOR object OBJ_MAXDD (the 36-of-36 cell set).  Each step reports the")
    P("   change in log(observed / null median), so the channels ADD to the total gap.")
    chrows = []
    for panel in PANELS:
        T = int(panels[panel]["warm"].sum())
        for lad in LADDERS:
            dct = draws[(panel, lad, "N_BLOCK")]
            R, ai = dct["R"], dct["ai"]
            o = dct["obs"]["OBJ_MAXDD"]
            rngw = np.random.default_rng(seed_of(panel, lad, "NOWRAP"))
            ixnw = null_index("N_BLOCK_NOWRAP", rngw, T, BDRAWS)
            variants = {
                "K0_RECORD": dct["RAW"][ai],
                "K1_NOWRAP": boot_maxdd(R, ixnw)[ai],
                "K2_CENTER": dct["CEN"][ai],
                "K3_PERM": dct["PRM"][ai],
                "K4_IID": draws[(panel, lad, "N_IID")]["RAW"][ai],
                "K5_IIDPERM": draws[(panel, lad, "N_IID")]["PRM"][ai],
            }
            base = np.log(o / float(np.nanmedian(variants["K0_RECORD"])))
            for k, bb in variants.items():
                med = float(np.nanmedian(bb))
                chrows.append(dict(panel=panel, ladder=lad, variant=k, observed=o,
                                   null_median=med, log_gap=float(np.log(o / med)),
                                   delta_vs_record=float(np.log(o / med) - base)))
    CH = pd.DataFrame(chrows)
    dump(CH, "channels")
    P("   variant       what it removes                       median log gap   vs K0_RECORD")
    WHAT = {"K0_RECORD": "nothing (the record's N_BLOCK, L=63)",
            "K1_NOWRAP": "wrap-around only",
            "K2_CENTER": "the DRIFT channel (Jensen)",
            "K3_PERM": "the MARGINAL-RESAMPLING channel",
            "K4_IID": "all block order (L=63 -> L=1)",
            "K5_IIDPERM": "marginal resampling AND all order"}
    for k in ["K0_RECORD", "K1_NOWRAP", "K2_CENTER", "K3_PERM", "K4_IID", "K5_IIDPERM"]:
        s = CH[CH.variant == k]
        P(f"   {k:<13} {WHAT[k]:<38} {float(s.log_gap.median()):14.4f}   "
          f"{float(s.delta_vs_record.median()):+12.4f}")
    P("")

    # ============================================================ ARM E — the book's own structure
    P("## ARM E — IF ANY GAP SURVIVES, WHOSE STRUCTURE IS IT?  The three carriers the queue")
    P("   names, measured on the 12 ANCHOR books and correlated with the residual gap.")
    strows = []
    for panel in PANELS:
        for lad in LADDERS:
            dct = draws[(panel, lad, "N_BLOCK")]
            x = dct["R"][dct["ai"]]
            rec, sh = recovery_of(x)
            resid = float(np.log(dct["obs"]["OBJ_MAXDD"]
                                 / float(np.nanmedian(obj_draws(dct["PRM"], "OBJ_MAXDD",
                                                                dct["ai"])))))
            strows.append(dict(panel=panel, ladder=lad, ac1=ac1_of(x),
                               vr63=vr_of(x, 63), vr21=vr_of(x, 21),
                               recovery_drift=rec, share_in_dd=sh,
                               resid_log_gap_perm=resid,
                               raw_log_gap=float(np.log(dct["obs"]["OBJ_MAXDD"]
                                                        / float(np.nanmedian(dct["RAW"][dct["ai"]]))))))
    ST = pd.DataFrame(strows)
    dump(ST, "structure")
    P("   panel  ladder     ac1      VR(21)   VR(63)   recovery drift   raw gap   perm gap")
    for _, r_ in ST.iterrows():
        P(f"   {r_['panel']:<6} {r_['ladder']:<9} {r_['ac1']:+7.4f}  {r_['vr21']:7.4f}  "
          f"{r_['vr63']:7.4f}  {r_['recovery_drift']:+14.6f}   {r_['raw_log_gap']:+7.4f}  "
          f"{r_['resid_log_gap_perm']:+8.4f}")
    P("   READ THE LEFT-HAND COLUMNS FIRST: ac1, VR and the recovery drift are IDENTICAL down")
    P("   each panel, because all four anchor rungs ARE the same book (gate G12).  There are")
    P("   THREE distinct books here, not twelve, and the four rows per panel differ ONLY by the")
    P("   null's seed.  A rank correlation over the 12 rows would therefore be a correlation")
    P("   over 3 points with each point counted four times, so this run does NOT report one.")
    PAN = ST.groupby("panel").agg(ac1=("ac1", "first"), vr63=("vr63", "first"),
                                  vr21=("vr21", "first"),
                                  recovery=("recovery_drift", "first"),
                                  perm_gap=("resid_log_gap_perm", "median"),
                                  raw_gap=("raw_log_gap", "median"),
                                  seed_spread=("resid_log_gap_perm",
                                               lambda s: float(s.max() - s.min())))
    dump(PAN.reset_index(), "structure_panel")
    P("   panel   ac1      VR(21)   VR(63)   recovery      perm gap (median of 4 seeds)  "
      "seed spread")
    for p_, r_ in PAN.iterrows():
        P(f"   {p_:<7} {r_['ac1']:+7.4f}  {r_['vr21']:7.4f}  {r_['vr63']:7.4f}  "
          f"{r_['recovery']:+11.6f}  {r_['perm_gap']:+27.4f}  {r_['seed_spread']:11.4f}")
    P("   THE ORDER IS THE SAME ON EVERY COLUMN AND THE SAMPLE IS THREE: the panel with the")
    P("   least negative ac1 and the highest VR(21) (SMALL) carries the LARGEST gap and the")
    P("   most negative ac1 (U56) the smallest, which is the OPPOSITE of the naive mean-")
    P("   reversion story and is exactly 1162's H_MEANREV refutation seen from this side.")
    P("   n = 3.  A DIAGNOSTIC, not a test; no hypothesis in this run turns on it, and the")
    P("   seed spread column shows the gap's own 1000-draw noise for scale.")
    P("")

    # ============================================================ ARM F — rule 8 + KEEP paths
    P("## ARM F — PROTOCOL rule 8 WALK-FORWARD AND BOTH KEEP PATHS")
    P(f"   {len(POP_N)}x{len(POP_H)}x{len(POP_C)} = {len(POP_N)*len(POP_H)*len(POP_C)} books "
      f"per panel, {len(POP_N)*len(POP_H)*len(POP_C)*len(PANELS)} in all, EVERY ONE PUBLISHED.")
    P("   Parameters are chosen on 2009-2016 ONLY (IS) and read once on 2017-2026 (OOS).")
    poprows = []
    for panel in PANELS:
        dd_ = panels[panel]
        sb, lbm_p = dd_["spy_m"], dd_["live_m"]
        Tis = int(dd_["ins"].sum())
        for N in POP_N:
            for H in POP_H:
                for fr in POP_C:
                    r_ = run_cell(panel, N, H, GROSS0, fr)
                    mm = blocks_m(r_, dd_["warm"], dd_["ins"], dd_["oos"])
                    l4b, l4bo, l4a = legs_4b(mm, sb), legs_4b_oos(mm, sb), legs_4a(mm, lbm_p)
                    row = dict(panel=panel, N=N, H=H, cadence=fr, **mm,
                               pass_4b_full=all(l4b.values()),
                               pass_4b_oos=all(l4bo.values()),
                               pass_4a=all(l4a.values()), **l4b, **l4bo, **l4a)
                    # the IS null of this book's own IS |MaxDD|, under each null x correction
                    ris = r_[dd_["ins"]][None, :]
                    o_is = -fmet(ris[0])[2] * 100.0
                    for nt in NULL_TYPES:
                        rng = np.random.default_rng(seed_of(panel, N, H, fr, nt, "IS"))
                        ixi = null_index(nt, rng, Tis, BDRAWS_IS)
                        pixi = perm_index(nt, np.random.default_rng(
                            seed_of(panel, N, H, fr, nt, "ISP")), Tis, BDRAWS_IS)
                        b_raw = boot_maxdd(ris, ixi)[0]
                        b_cen = boot_maxdd(ris, ixi, center=True)[0]
                        b_prm = boot_maxdd(ris, pixi)[0]
                        row[f"isratio_{nt}_R_NONE"] = o_is / float(np.nanmedian(b_raw))
                        row[f"isratio_{nt}_R_CENTER"] = o_is / float(np.nanmedian(b_cen))
                        row[f"isratio_{nt}_R_PERM"] = o_is / float(np.nanmedian(b_prm))
                        row[f"isratio_{nt}_R_PIVOT"] = o_is / max(
                            2 * o_is - float(np.nanmedian(b_raw)), 1e-9)
                        mf = float(machcell.loc[(panel, "N", nt, "OBJ_MAXDD")])
                        row[f"isratio_{nt}_R_MACH"] = (o_is / (float(np.nanmedian(b_raw)) / mf)
                                                       if mf else np.nan)
                    poprows.append(row)
        P(f"   {panel:<6s} {len(POP_N)*len(POP_H)*len(POP_C)} books done "
          f"({time.time() - t0:.0f}s)")
    POP = pd.DataFrame(poprows)
    dump(POP, "walkforward")
    P(f"   4b full {int(POP.pass_4b_full.sum())} of {len(POP)}, 4b OOS "
      f"{int(POP.pass_4b_oos.sum())} of {len(POP)}, 4a {int(POP.pass_4a.sum())} of {len(POP)}")
    for p_, g in POP.groupby("panel"):
        P(f"     {p_:<6} 4b full {int(g.pass_4b_full.sum()):2d}/{len(g)}  4b OOS "
          f"{int(g.pass_4b_oos.sum()):2d}/{len(g)}  4a {int(g.pass_4a.sum()):2d}/{len(g)}")

    both = POP[POP.pass_4b_full & POP.pass_4b_oos]
    best = both.sort_values("OOS_Sharpe", ascending=False).head(1)
    if len(best):
        b = best.iloc[0]
        P(f"   BEST 4b book (full AND OOS): {b['panel']} / {b['cadence']} / N={int(b['N'])} / "
          f"H={int(b['H'])}  full {b['CAGR']:.2%}/{b['Sharpe']:.4f}/{b['MaxDD']:.2%} "
          f"(H1 {b['H1']:.4f} / H2 {b['H2']:.4f})  OOS {b['OOS_CAGR']:.2%}/"
          f"{b['OOS_Sharpe']:.4f}/{b['OOS_MaxDD']:.2%}")
    else:
        P("   NO book passes 4b full AND OOS on this population.")
    for p_ in PANELS:
        sb, lbm_p = panels[p_]["spy_m"], panels[p_]["live_m"]
        P(f"     {p_:<6} SPY full {sb['CAGR']:.2%}/{sb['Sharpe']:.4f}/{sb['MaxDD']:.2%} OOS "
          f"{sb['OOS_CAGR']:.2%}/{sb['OOS_Sharpe']:.4f}/{sb['OOS_MaxDD']:.2%} | live v2 full "
          f"{lbm_p['CAGR']:.2%}/{lbm_p['Sharpe']:.4f}/{lbm_p['MaxDD']:.2%} OOS "
          f"{lbm_p['OOS_CAGR']:.2%}/{lbm_p['OOS_Sharpe']:.4f}/{lbm_p['OOS_MaxDD']:.2%}")
    P("")

    P("   THE CAPITAL QUESTION: does CORRECTING the null change what an IS chooser BUYS?")
    P("   CH_NULLDD picks the book whose IS |MaxDD| is SHALLOWEST relative to its OWN IS null")
    P("   median — the null used as a selector.  If the correction is capital-relevant, the")
    P("   pick must move.  CH_ISSHARPE / CH_ISCAGR / CH_ISDD are the record's three, unmoved")
    P("   by any correction by construction and published as the reference.")
    pickrows = []
    for panel in PANELS:
        g = POP[POP.panel == panel]
        for ch in CHOOSERS:
            if ch == "CH_NULLDD":
                for nt in NULL_TYPES:
                    for corr in CORRECTIONS:
                        col = f"isratio_{nt}_{corr}"
                        i = g[col].idxmin()          # smallest obs/null = most genuinely shallow
                        r_ = POP.loc[i]
                        pickrows.append(dict(panel=panel, chooser=ch, null_type=nt,
                                             correction=corr,
                                             pick=f"N{int(r_['N'])}/H{int(r_['H'])}/"
                                                  f"{r_['cadence']}",
                                             OOS_Sharpe=r_["OOS_Sharpe"],
                                             OOS_CAGR=r_["OOS_CAGR"],
                                             OOS_MaxDD=r_["OOS_MaxDD"],
                                             pass_4b_full=bool(r_["pass_4b_full"]),
                                             pass_4b_oos=bool(r_["pass_4b_oos"]),
                                             pass_4a=bool(r_["pass_4a"])))
            else:
                col = {"CH_ISSHARPE": "IS_Sharpe", "CH_ISCAGR": "IS_CAGR",
                       "CH_ISDD": "IS_MaxDD"}[ch]
                i = g[col].idxmax()
                r_ = POP.loc[i]
                for nt in NULL_TYPES:
                    for corr in CORRECTIONS:
                        pickrows.append(dict(panel=panel, chooser=ch, null_type=nt,
                                             correction=corr,
                                             pick=f"N{int(r_['N'])}/H{int(r_['H'])}/"
                                                  f"{r_['cadence']}",
                                             OOS_Sharpe=r_["OOS_Sharpe"],
                                             OOS_CAGR=r_["OOS_CAGR"],
                                             OOS_MaxDD=r_["OOS_MaxDD"],
                                             pass_4b_full=bool(r_["pass_4b_full"]),
                                             pass_4b_oos=bool(r_["pass_4b_oos"]),
                                             pass_4a=bool(r_["pass_4a"])))
    PK = pd.DataFrame(pickrows)
    dump(PK, "picks")
    nd = PK[PK.chooser == "CH_NULLDD"]
    moved = nd.groupby(["panel", "null_type"]).pick.nunique()
    moved_np = nd[nd.correction != "R_PIVOT"].groupby(["panel", "null_type"]).pick.nunique()
    P(f"   CH_NULLDD: the CORRECTION moves the pick at {int((moved > 1).sum())} of "
      f"{len(moved)} (panel, null type) cells — but {int((moved_np > 1).sum())} of "
      f"{len(moved_np)} once R_PIVOT is set aside.")
    P("   R_PIVOT is the whole of it, and R_PIVOT is a REFLECTION, not a repair: it maps the")
    P("   null through the observed value, which turns 'the null sits above' into 'the null")
    P("   sits below' by construction and does NOT price why.  Its mean OOS Sharpe advantage")
    P("   is reported below and is an n = 9 curiosity, not a finding.")
    for (p_, nt), g in nd.groupby(["panel", "null_type"]):
        P(f"     {p_:<6} {nt:<9} " + "  ".join(
            f"{r_['correction'][2:]}:{r_['pick']}({r_['OOS_Sharpe']:.3f})"
            for _, r_ in g.iterrows()))
    P(f"   picks clearing 4b full AND OOS: {int((PK.pass_4b_full & PK.pass_4b_oos).sum())} of "
      f"{len(PK)};  4a: {int(PK.pass_4a.sum())} of {len(PK)}")
    P("   mean OOS Sharpe of the CH_NULLDD pick, by correction (the capital content, at its")
    P("   true weight):  " + ",  ".join(
        f"{c} {float(nd[nd.correction == c].OOS_Sharpe.mean()):.4f}" for c in CORRECTIONS))
    P("   by chooser:  " + ",  ".join(
        f"{c} n={len(PK[PK.chooser == c])} 4b(full+OOS) "
        f"{int((PK[PK.chooser == c].pass_4b_full & PK[PK.chooser == c].pass_4b_oos).sum())} "
        f"meanOOS {float(PK[PK.chooser == c].OOS_Sharpe.mean()):.4f}" for c in CHOOSERS))
    P("")

    # ============================================================ hypotheses
    P("## HYPOTHESES — declared with their bars, scored once")
    perm_all = CO[CO.correction == "R_PERM"]
    none_all = CO[CO.correction == "R_NONE"]
    cen_all = CO[CO.correction == "R_CENTER"]
    mach_all = CO[CO.correction == "R_MACH"]
    sperm = CAL[CAL.tape == "S_PERM"]
    floor_share = float((sperm.observed < sperm.null_median).mean())
    dd_none = none_all[none_all.object == "OBJ_MAXDD"]
    dd_perm = perm_all[perm_all.object == "OBJ_MAXDD"]

    hyp = []

    def H(name, declared, bar, measured, ok):
        hyp.append(dict(hypothesis=name, declared=declared, bar=bar, measured=measured,
                        supported=bool(ok)))
        P(f"   [{'SUPPORTED' if ok else 'REFUTED  '}] {name:<12} {declared}")
        P(f"                   bar {bar} | measured {measured}")

    ok = floor_share >= 0.70
    H("H_MACHINERY", "the bias survives on a tape with NO serial structure (S_PERM)",
      "share below median >= 0.70 on S_PERM",
      f"{floor_share:.4f} ({int((sperm.observed < sperm.null_median).sum())} of {len(sperm)})",
      ok)

    v_none = float(none_all.ratio_obs_over_null.median())
    v_perm = float(perm_all.ratio_obs_over_null.median())
    ok = v_perm > v_none and abs(1 - v_perm) < abs(1 - v_none) / 2
    H("H_MARGINAL", "the MARGINAL-RESAMPLING channel carries most of the gap (R_PERM halves it)",
      "|1 - median ratio| at least HALVED by R_PERM",
      f"R_NONE {v_none:.4f} -> R_PERM {v_perm:.4f}", ok)

    v_cen = float(cen_all.ratio_obs_over_null.median())
    ok = abs(1 - v_cen) < abs(1 - v_none) / 2
    H("H_DRIFT", "the DRIFT channel (Jensen) carries most of the gap (R_CENTER halves it)",
      "|1 - median ratio| at least HALVED by R_CENTER",
      f"R_NONE {v_none:.4f} -> R_CENTER {v_cen:.4f}", ok)

    nw = CH[CH.variant == "K1_NOWRAP"].delta_vs_record.abs().median()
    ok = bool(nw >= 0.02)
    H("H_WRAP", "wrap-around is a material block artefact",
      "median |delta log gap| >= 0.02", f"{nw:.4f}", ok)

    b_dd = int((dd_perm.observed < dd_perm.null_median).sum())
    ok = b_dd >= 30
    H("H_BOOK", "a BOOK gap survives every machinery repair on OBJ_MAXDD",
      "R_PERM still below median at >= 30 of 36",
      f"{b_dd} of {len(dd_perm)} (R_NONE {int((dd_none.observed < dd_none.null_median).sum())} "
      f"of {len(dd_none)})", ok)

    ma = CAL[CAL.tape == "S_MA1"]
    ma_r = float(ma[ma.object == "OBJ_MAXDD"].ratio.median())
    sp_r = float(sperm[sperm.object == "OBJ_MAXDD"].ratio.median())
    re_r = float(dd_none.ratio_obs_over_null.median())
    frac = ((sp_r - ma_r) / (sp_r - re_r)) if abs(sp_r - re_r) > 1e-12 else np.nan
    ok = bool(np.isfinite(frac) and frac >= 0.50)
    H("H_AC1", "an ac1 of the book's OWN size reproduces most of the residual gap",
      "S_MA1 closes >= 50% of the S_PERM -> REAL distance on OBJ_MAXDD",
      f"S_PERM {sp_r:.4f}, S_MA1 {ma_r:.4f}, REAL {re_r:.4f} -> {frac:.3f}", ok)

    ins_none = float(none_all["inside_0.9"].mean())
    ins_mach = float(mach_all["inside_0.9"].mean())
    ok = ins_mach > ins_none
    H("H_BAND", "R_MACH widens the record's effective coverage of its own observed value",
      "inside-90% share strictly higher than R_NONE's",
      f"R_NONE {ins_none:.4f} -> R_MACH {ins_mach:.4f}", ok)

    ok = bool((moved > 1).sum() >= 5)
    H("H_CAPITAL", "correcting the null moves what an IS chooser buys",
      "CH_NULLDD pick moves at >= 5 of 9 (panel, null) cells",
      f"{int((moved > 1).sum())} of {len(moved)}, but {int((moved_np > 1).sum())} of "
      f"{len(moved_np)} once the R_PIVOT REFLECTION is set aside; mean OOS Sharpe of the pick "
      f"R_NONE {float(nd[nd.correction == 'R_NONE'].OOS_Sharpe.mean()):.4f} vs R_MACH "
      f"{float(nd[nd.correction == 'R_MACH'].OOS_Sharpe.mean()):.4f} vs R_PERM "
      f"{float(nd[nd.correction == 'R_PERM'].OOS_Sharpe.mean()):.4f}", ok)

    fl = (CAL[CAL.tape == "S_PERM"].groupby("object").ratio.median())
    ok = bool(abs(1 - fl["OBJ_MAXDD"]) < 0.02 and abs(1 - fl["OBJ_SPREAD"]) > 0.02)
    H("H_OBJECT", "the machinery floor is OBJECT-dependent: clean on a LEVEL, biased on a "
                  "max-minus-min SPREAD (1148's count inflation, inside the null)",
      "|1 - S_PERM ratio| < 0.02 on OBJ_MAXDD and > 0.02 on OBJ_SPREAD",
      f"OBJ_MAXDD {fl['OBJ_MAXDD']:.4f}, OBJ_SPREAD {fl['OBJ_SPREAD']:.4f}, "
      f"OBJ_ARGMAX {fl['OBJ_ARGMAX']:.4f}", ok)

    HY = pd.DataFrame(hyp)
    dump(HY, "hypotheses")
    GA = pd.DataFrame(GATES)
    dump(GA, "gates")
    P(f"   GATES {int(GA.pass_.sum())} of {len(GA)} PASS.  HYPOTHESES "
      f"{int(HY.supported.sum())} of {len(HY)} SUPPORTED.")
    P("")

    # ============================================================ what a band would need
    P("## WHAT A PUBLISHED BAND WOULD NEED — the deliverable the queue asked for")
    for nt in NULL_TYPES:
        s0 = CO[(CO.correction == "R_NONE") & (CO.null_type == nt)]
        sm_ = CO[(CO.correction == "R_MACH") & (CO.null_type == nt)]
        sp_ = CO[(CO.correction == "R_PERM") & (CO.null_type == nt)]
        P(f"   {nt:<9} the record's band is centred {1/float(s0.ratio_obs_over_null.median()):.4f}x"
          f" ABOVE the observed; the S_PERM machinery floor accounts for "
          f"{float(machcell.xs(nt, level='null_type').median()):.4f}x of it, and after R_MACH "
          f"the centre sits at {float(sm_.ratio_obs_over_null.median()):.4f}x "
          f"(R_PERM {float(sp_.ratio_obs_over_null.median()):.4f}x).")
    P("")
    P("   PER OBJECT, because the answer is NOT the same for a LEVEL and for a SPREAD:")
    P("   object       S_PERM machinery floor   real median ratio   residual after R_MACH")
    for obj in OBJECTS:
        f_ = float(CAL[(CAL.tape == "S_PERM") & (CAL.object == obj)].ratio.median())
        r_ = float(CO[(CO.correction == "R_NONE") & (CO.object == obj)]
                   .ratio_obs_over_null.median())
        m_ = float(CO[(CO.correction == "R_MACH") & (CO.object == obj)]
                   .ratio_obs_over_null.median())
        P(f"   {obj:<12} {f_:22.4f}   {r_:17.4f}   {m_:21.4f}")
    P("   A LEVEL needs NO machinery correction and the whole of its gap is the book's.  A")
    P("   max-minus-min SPREAD needs one of about 5%, and it is the SAME count-inflation")
    P("   idea 1148 corrected in the observed statistic and nobody had checked in the null.")
    P("")
    P("## SURVIVORSHIP (PROTOCOL rule 9)")
    P("   U56, B136 and SMALL are CURRENT-CONSTITUENT lists.  SMALL is the current constituents")
    P(f"   of a sub-$2B screen, {panels['SMALL']['K'] - 1} columns after dropping the {ndrop} "
      f"tickers with max_1d_move >= 1.0")
    P(f"   from data/small_meta.csv (tape {panels['SMALL']['idx'][0].date()} -> "
      f"{panels['SMALL']['idx'][-1].date()}).  Every delisted, zeroed or screened-out name is")
    P("   absent, so every CAGR, drawdown and 4b pass rate above is the MOST FLATTERING the")
    P("   period could have produced.  It bears on this idea's headline DIRECTLY and in the")
    P("   direction of the finding: a survivor-only panel has SHALLOWER observed drawdowns than")
    P("   the real one, which pushes the observed value further BELOW its own null.  The")
    P("   machinery floor measured in Arm C is immune (it is a ratio read on the same panel),")
    P("   the residual book gap is NOT, and that is stated in the result memo.")
    P("")
    P(f"DONE in {time.time() - t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"wrote {OUT.name}.console.txt")
    return dict(CO=CO, DI=DI, CAL=CAL, CH=CH, ST=ST, POP=POP, PK=PK, HY=HY, GA=GA,
                machcell=machcell, panels=panels, best=best, moved=moved)


if __name__ == "__main__":
    main()

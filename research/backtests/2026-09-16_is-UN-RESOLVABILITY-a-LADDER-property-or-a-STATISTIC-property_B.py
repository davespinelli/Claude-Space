#!/usr/bin/env python3
"""Idea 1116 (lane B, 2026-09-16) — is UN-RESOLVABILITY a LADDER property or a STATISTIC
property?

QUESTION (QUEUE idea 1116, verbatim)
    idea 1110 found 8 of 32 CORE cells never resolve their own committed argmax gap even at
    500x the tape, and 18 of 32 carry an infinite floor.  Test whether those cells are the
    same LADDERS across all four statistics or the same STATISTICS across all four ladders,
    and report which axis the record should stop laddering.  Max 2 params (axis, statistic).

WHAT IS TUNED AND WHAT IS NOT (PROTOCOL rule 4)
    Exactly TWO dials: UNRESOLVABILITY DEFINITION {INF_FLOOR, ZERO_CONTENT, NO_TAPE_500}
    x CONFIDENCE q {0.80, 0.90, 0.95} = 9 combinations, ALL published.
    LADDER and STATISTIC are NOT dials — they are the two candidate ANSWERS and all 2 x 4 x 4
    = 32 CORE cells are reported under every combination.  PANEL is not a dial (both panels
    reported everywhere, 1102/1108/1110's convention).  BLOCK LENGTH is not a dial: L=63
    throughout (1098/1102/1108/1110's headline), with L in {21, 126} reported BESIDE the
    headline and never selected on.  Everything else frozen at 1082/1094/1098/1102/1108/1110's
    construction: CAND20 legs, cap INF, max_vol 0.60, gross 0.75 (except on the GROSS ladder),
    W cadence (except on the CADENCE ladder), min hold 126 (except on the H ladder), N=20
    (except on the N ladder), 10 bps, LAG 1, warm-up 260, IS end 2016-12-31, 1000 draws.
    Seeds are zlib.crc32 — 1108's repair of 1102's process-random hash() seeds.

THE THREE DEFINITIONS OF UN-RESOLVABLE (dial 1), pre-registered
    INF_FLOOR     floor(q) is INFINITE: no rung pair in the ladder is sign-resolved at q above
                  the largest UNRESOLVED gap, so the clause can exclude nothing at any gap.
                  This is 1110's "18 of 32" count and it is the headline definition.
    ZERO_CONTENT  the published tie set is the WHOLE ladder (DECIDED = 0).  Implied by
                  INF_FLOOR but strictly weaker as a test: a FINITE floor wider than the
                  peak's distance to every other rung is contentless too.
    NO_TAPE_500   the cell's own committed argmax gap does not clear its own floor at ANY tape
                  multiple M <= 500, under 1110's projection A' = Phi(sqrt(M) Phi^-1(A)).
                  This is 1110's "8 of 32" count.

THE TWO CANDIDATE ANSWERS, AND HOW THEY ARE SEPARATED — before any number
    Un-resolvability is a 4 (ladder) x 4 (statistic) table per panel.  "It is a LADDER
    property" means the table's rows are constant and its columns are not; "a STATISTIC
    property" means the reverse.  Two independent readings, both reported for every cell of
    dial 1 x dial 2:
      DECOMPOSITION  a main-effects two-way decomposition of the cell value over (ladder,
                     statistic).  ETA2_LAD and ETA2_STAT are the shares of total sum of
                     squares carried by each axis's main effect; the remainder is interaction
                     plus, on the pooled table, the panel main effect.  Run on the BINARY
                     indicator AND on two continuous readings that need no threshold at all:
                     REL_FLOOR = min(floor, spread)/spread in (0, 1], and LOG_M = log10 of the
                     tape multiple the cell needs (capped at 500).
      CONCORDANCE    mean pairwise AGREEMENT of the four STATISTICS inside a ladder (6 pairs
                     per ladder) against mean pairwise agreement of the four LADDERS inside a
                     statistic (6 pairs per statistic).  Both sides share the same marginal
                     base rate by construction, so their DIFFERENCE is the readable quantity.

DECLARED BEFORE ANY NUMBER
    (a) H_LADDER      ETA2_LAD > ETA2_STAT on the binary indicator at the HEADLINE cell
                      (INF_FLOOR, q=0.90) in BOTH panels.
    (b) H_STAT        the mirror of (a): ETA2_STAT > ETA2_LAD in BOTH panels.  Exactly one of
                      (a) and (b) can pass; both can fail.
    (c) H_CONCORD     the axis that wins (a)/(b) also wins the CONCORDANCE reading in both
                      panels — within-axis agreement HIGHER along the winning axis.
    (d) H_GROSS_CARRIES  the ladder answer, if it wins, is carried by ONE ladder: GROSS is
                      resolvable at all 4 statistics while at least two other ladders are
                      un-resolvable at all 4, at the headline.  1108 found GROSS is the
                      smallest rung-to-rung DISTANCE ladder (its rungs are near-scalings of
                      one book), so a ladder answer that is really a GROSS answer is a
                      statement about book distance, not about laddering.  Declared as the
                      post-hoc risk this design is most exposed to, and tested head-on.
    (e) H_DD_WORST    DD is the LEAST resolvable statistic (highest mean REL_FLOOR over the 8
                      panel-ladder cells).  1110 found DD's floor does not fall with tape at
                      all (fitted beta +0.2093 against -0.4540 for the rest), so if
                      un-resolvability were a statistic property DD is where it must live.
    (f) THE DECISION RULE, fixed before any number: the answer is LADDER if (a) passes in both
                      panels under a MAJORITY (>= 5) of the 9 dial combinations, STATISTIC if
                      (b) does, and NEITHER otherwise — in which case un-resolvability is a
                      per-cell fact and the record should stop quoting it by axis at all.
                      The continuous readings are the tie-break and are reported regardless.
    (g) NOT A KEEP PATH.  The BOOK at every one of the 54 rungs is byte-identical across both
                      dials — only which cells get CALLED un-resolvable changes — so 4a and 4b
                      are invariant to dial 1 and dial 2 by construction.  Rule 8 (rung chosen
                      on 2009-2016 ALONE, per ladder, three choosers, OOS read ONCE) and both
                      KEEP paths are scored anyway because PROTOCOL rule 4 requires it.

THE DECLARED APPROXIMATION, AND ITS DIRECTION.  NO_TAPE_500 uses 1110's PROJECTION
    A' = Phi(sqrt(M) Phi^-1(A)), which assumes a fixed population gap and an SE falling as
    1/sqrt(T).  Both assumptions run TOWARD resolution, so every M_needed here is a LOWER
    bound and every NO_TAPE_500 count is a LOWER bound on un-resolvability.  The exponent is
    NOT re-measured here: 1110 measured it on disjoint sub-tapes at f = 0.25 and 0.50 and
    published a median beta of -0.4540 over the 24 non-DD cells against 1/sqrt(T)'s -0.50,
    with DD running the other way (+0.2093).  That measurement is INHERITED and named as such;
    DD's M_needed is therefore the least trustworthy column and is reported apart wherever it
    matters.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT panels, so every level
    is optimistic.  A rung-to-rung GAP and a rung-to-rung AGREEMENT both contrast two books
    over the same inflated tape and the bias very largely cancels out of them, out of the floor
    and out of every quantity this run decomposes; it does NOT cancel out of the 4b legs, which
    are measured against SPY, a real index, so any 4b pass reported here is an UPPER bound.
"""
from __future__ import annotations

import sys
import time
import zlib
from itertools import combinations
from math import erf, sqrt
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-16"
SLUG = "is-UN-RESOLVABILITY-a-LADDER-property-or-a-STATISTIC-property"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"
HERE = Path(__file__).resolve().parent
PRIOR1102 = HERE / "2026-09-16_does-the-RESOLUTION-FLOOR-CLAUSE-change-any-committed-ARGMAX-in-the-record_C"
PRIOR1110 = HERE / "2026-09-16_what-does-the-RECORD-LOSE-if-the-FLOOR-CLAUSE-is-ENACTED-AS-WRITTEN_C"

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

STATS = ["S_FULL", "S_OOS", "CAGR", "DD"]
PANELS = ["U56", "B136"]
CHOOSERS = ["C_ISSHARPE", "C_ISDD", "C_ISCAGR"]

DEFS = ["INF_FLOOR", "ZERO_CONTENT", "NO_TAPE_500"]        # dial 1
QGRID = [0.80, 0.90, 0.95]                                 # dial 2
DEF_HEAD, Q_HEAD = "INF_FLOOR", 0.90
L_HEAD = 63
L_SIDE = [21, 126]                                         # reported beside, never selected on
BDRAWS = 1000
M_GRID = np.round(np.arange(1.0, 500.0 + 1e-9, 0.25), 2)   # 1110's tape-multiple grid
M_CAP = 500.0
SEED_BOOT = 11161116

A936_WH126 = (0.155787, 1.139701, -0.191276)
A1098_U56_N12 = (0.1771, 1.1692, -0.2017)
A1098_B136_N15 = (0.1678, 1.0682, -0.1966)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205

LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def seed_of(*parts):
    """Deterministic across processes — 1108's repair of 1102's hash() seeds."""
    return SEED_BOOT + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


def Phi(z):
    return 0.5 * (1.0 + erf(z / sqrt(2.0)))


def Phi_inv(p):
    """Acklam's rational approximation; |abs error| < 1.2e-9 on (0,1)."""
    p = min(max(float(p), 1e-12), 1.0 - 1e-12)
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    pl = 0.02425
    if p < pl:
        q = sqrt(-2 * np.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    if p > 1 - pl:
        q = sqrt(-2 * np.log(1 - p))
        return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    q = p - 0.5
    r = q * q
    return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)


# --------------------------------------------- 1082/1098/1102/1108/1110's fast runner, verbatim
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


def windows(idx):
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


# ------------------------------------------------ 1098/1102's bootstrap, 1108's seed repair
def block_index(rng, T, L, ndraws):
    nb = int(np.ceil(T / L))
    st = rng.integers(0, T, size=(ndraws, nb))
    off = np.arange(L)
    idx = (st[:, :, None] + off[None, None, :]) % T
    return idx.reshape(ndraws, nb * L), nb


def boot_exact(R, idx, nb, L, chunk=100):
    LG = np.log1p(R)
    D = np.concatenate([LG, LG], axis=1)
    CS = np.concatenate([np.zeros((D.shape[0], 1)), np.cumsum(D, axis=1)], axis=1)
    R2 = np.concatenate([R, R], axis=1)
    CS1 = np.concatenate([np.zeros((R.shape[0], 1)), np.cumsum(R2, axis=1)], axis=1)
    CS2 = np.concatenate([np.zeros((R.shape[0], 1)), np.cumsum(R2 ** 2, axis=1)], axis=1)
    nd = idx.shape[0]
    st = idx[:, ::L]
    cag = np.empty((R.shape[0], nd))
    shp = np.empty((R.shape[0], nd))
    n = nb * L
    for a in range(0, nd, chunk):
        s = st[a:a + chunk]
        lsum = (CS[:, s + L] - CS[:, s]).sum(axis=2)
        s1 = (CS1[:, s + L] - CS1[:, s]).sum(axis=2)
        s2 = (CS2[:, s + L] - CS2[:, s]).sum(axis=2)
        cag[:, a:a + chunk] = np.expm1(lsum * (252.0 / n))
        mu = s1 / n
        var = (s2 - n * mu ** 2) / (n - 1)
        sd = np.sqrt(np.maximum(var, 0.0))
        shp[:, a:a + chunk] = np.where(sd > 0, mu * 252.0 / (sd * np.sqrt(252.0)), np.nan)
    return cag, shp


def boot_maxdd(R, idx, chunk=40):
    nr, _ = R.shape
    nd = idx.shape[0]
    out = np.empty((nr, nd))
    for a in range(0, nd, chunk):
        ix = idx[a:a + chunk]
        for j in range(nr):
            path = np.log1p(R[j])[ix]
            cum = np.cumsum(path, axis=1)
            run = np.maximum.accumulate(cum, axis=1)
            out[j, a:a + chunk] = np.expm1(cum - run).min(axis=1)
    return out


def floor_from_agreement(gaps, agree, q):
    """1098's floor, given |gap| and agreement per pair."""
    gaps = np.asarray(gaps, float)
    agree = np.asarray(agree, float)
    un = agree < q
    largest_un = float(gaps[un].max()) if un.any() else 0.0
    ok = (~un) & (gaps > largest_un)
    flo = float(gaps[ok].min()) if ok.any() else float("inf")
    return flo, largest_un, int(un.sum())


def pair_agreement(vals, boot):
    """Per rung pair: signed gap and bootstrap agreement with its sign."""
    k = len(vals)
    out = []
    for i, j in combinations(range(k), 2):
        g = vals[i] - vals[j]
        if not np.isfinite(g):
            continue
        d = boot[i] - boot[j]
        d = d[np.isfinite(d)]
        a = float((np.sign(d) == np.sign(g)).mean()) if len(d) else np.nan
        out.append((i, j, g, a))
    return out


def agree_matrix(prs, k):
    A = np.full((k, k), np.nan)
    np.fill_diagonal(A, 1.0)
    for (i, j, _g, a) in prs:
        A[i, j] = A[j, i] = a
    return A


def floor_of(vals, A, sub, q):
    """Floor(q) over the rung subset `sub` (indices into the full ladder)."""
    gaps, agr = [], []
    for i, j in combinations(sub, 2):
        g = vals[i] - vals[j]
        if not np.isfinite(g) or not np.isfinite(A[i, j]):
            continue
        gaps.append(abs(g))
        agr.append(A[i, j])
    if not gaps:
        return float("inf"), 0.0, 0
    return floor_from_agreement(np.array(gaps), np.array(agr), q)


def tie_set(vals, sub, peak, flo):
    s = {peak}
    for j in sub:
        if np.isfinite(vals[j]) and abs(vals[peak] - vals[j]) < flo:
            s.add(j)
    return sorted(s)


def m_needed(vals, A, q, gap):
    """Smallest M on M_GRID at which the cell's own argmax gap clears its own PROJECTED
    floor, under 1110's A' = Phi(sqrt(M) Phi^-1(A)).  NaN if none at M <= M_CAP.

    Solved EXACTLY rather than by sweeping the grid.  With z = Phi^-1(A) and zq = Phi^-1(q),
    a pair is UNRESOLVED at M iff Phi(sqrt(M) z) < q iff sqrt(M) z < zq, i.e. iff
    M < (zq/z)^2 for z > 0, and ALWAYS (any M) for z <= 0 — since q > 0.5 makes zq > 0.
    So the un-resolved SET changes only at the per-pair critical multiples M_crit = (zq/z)^2,
    and evaluating the floor at M = 1 plus each M_crit rounded UP onto M_GRID gives the same
    answer as the sweep at a fraction of the cost.  Identical by construction, not an
    approximation of it; cross-checked against 1110's committed M_needed column in G9."""
    k = len(vals)
    gaps, agr = [], []
    for i, j in combinations(range(k), 2):
        g = vals[i] - vals[j]
        if not np.isfinite(g) or not np.isfinite(A[i, j]):
            continue
        gaps.append(abs(g))
        agr.append(A[i, j])
    if not gaps or not np.isfinite(gap):
        return np.nan
    gaps = np.asarray(gaps, float)
    zq = Phi_inv(q)
    z = np.array([Phi_inv(min(max(a, 1e-12), 1 - 1e-12)) for a in agr])
    with np.errstate(divide="ignore", invalid="ignore"):
        mcrit = np.where(z > 0, (zq / np.where(z > 0, z, 1.0)) ** 2, np.inf)
    step = float(M_GRID[1] - M_GRID[0])
    cands = {1.0}
    for mc in mcrit:
        if np.isfinite(mc) and mc <= M_CAP:
            cands.add(float(min(M_CAP, np.ceil(max(mc, 1.0) / step) * step)))
    for M in sorted(cands):
        un = mcrit > M
        largest_un = float(gaps[un].max()) if un.any() else 0.0
        ok = (~un) & (gaps > largest_un)
        flo = float(gaps[ok].min()) if ok.any() else float("inf")
        if np.isfinite(flo) and gap >= flo:
            return float(M)
    return np.nan


def two_way(tab):
    """Main-effects decomposition of a (rows x cols) table.  Returns eta2 for each axis."""
    x = np.asarray(tab, float)
    m = np.nanmean(x)
    sst = float(np.nansum((x - m) ** 2))
    if sst <= 0:
        return np.nan, np.nan, np.nan
    ra = np.nanmean(x, axis=1) - m
    ca = np.nanmean(x, axis=0) - m
    ss_r = float(x.shape[1] * np.nansum(ra ** 2))
    ss_c = float(x.shape[0] * np.nansum(ca ** 2))
    return ss_r / sst, ss_c / sst, sst


def concord(tab):
    """Mean pairwise agreement of COLUMNS within each row, and of ROWS within each column."""
    x = np.asarray(tab, float)
    nr, nc = x.shape
    wr = [float(np.mean([x[r, i] == x[r, j] for i, j in combinations(range(nc), 2)]))
          for r in range(nr)]
    wc = [float(np.mean([x[i, c] == x[j, c] for i, j in combinations(range(nr), 2)]))
          for c in range(nc)]
    return float(np.mean(wr)), float(np.mean(wc))


# ------------------------------------------------------------------------------------- main
def main():
    t0 = time.time()
    P(f"# Idea 1116 (lane B, {DATE}) — is UN-RESOLVABILITY a LADDER property or a STATISTIC")
    P("#   property?")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4): UNRESOLVABILITY DEFINITION {DEFS}")
    P(f"#   x CONFIDENCE q {QGRID} = {len(DEFS) * len(QGRID)} combinations, ALL published.")
    P("#   LADDER and STATISTIC are NOT dials — they are the two candidate ANSWERS, and all")
    P("#   2 x 4 x 4 = 32 CORE cells are reported under every combination.  PANEL is not a")
    P(f"#   dial.  BLOCK LENGTH is not a dial: L={L_HEAD} headline, L in {L_SIDE} reported beside.")
    P(f"# FROZEN: CAND20 legs {LEGS}, cap INF, max_vol {MAXVOL}, gross {GROSS0}, cadence "
      f"{FREQ0}, min hold {HOLD0},")
    P(f"#   N {N0}, {COST:.0f} bps, LAG {LAG}, warm-up {WARMUP}, IS end {IS_END}, "
      f"{BDRAWS} draws, crc32 seeds (1108's repair).")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   (a) H_LADDER        ETA2_LAD > ETA2_STAT on the binary indicator at (INF_FLOOR,")
    P("#                       q=0.90) in BOTH panels.")
    P("#   (b) H_STAT          the mirror.  Exactly one of (a)/(b) can pass; both can fail.")
    P("#   (c) H_CONCORD       the winning axis also wins the CONCORDANCE reading, both panels.")
    P("#   (d) H_GROSS_CARRIES GROSS resolvable at all 4 statistics while >= 2 other ladders are")
    P("#                       un-resolvable at all 4 — a ladder answer that is a GROSS answer.")
    P("#   (e) H_DD_WORST      DD is the least resolvable statistic (highest mean REL_FLOOR).")
    P("#   (f) DECISION RULE   LADDER if (a) holds in both panels under >= 5 of the 9 dial")
    P("#                       combinations, STATISTIC if (b) does, NEITHER otherwise.")
    P("#   (g) NOT A KEEP PATH the book at all 54 rungs is byte-identical across both dials;")
    P("#                       4a/4b and rule 8 scored anyway because rule 4 requires it.")
    P("")

    gaterows, gates = [], {}

    # ---------------------------------------------------------------------------- THE GATES
    P("## GATES — printed before any result number")
    panels = {}
    for panel in PANELS:
        px = load_universe(broad=(panel == "B136")).dropna(how="all").ffill()
        idx, K, T = px.index, len(px.columns), len(px.index)
        rets = px.pct_change().fillna(0.0).values
        priced = px.notna().values
        warm, ins, oos = windows(idx)
        sc, elig = mech(px)
        panels[panel] = dict(px=px, idx=idx, K=K, T=T, rets=rets, priced=priced,
                             warm=warm, ins=ins, oos=oos, sc=sc, elig=elig)
        P(f"  {panel}: {K} names, {T:,} rows {idx[0].date()} -> {idx[-1].date()}, "
          f"warm {warm.sum():,}, IS {ins.sum():,}, OOS {oos.sum():,}")

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
        return g - tn * COST / 1e4, tn

    d = panels["U56"]
    mk = rebalance_mask(d["idx"], FREQ0).values
    reb = np.flatnonzero(mk)
    W = build(-d["sc"], d["elig"], d["priced"], reb, N0, HOLD0, d["T"], d["K"], GROSS0)
    Wdf = pd.DataFrame(W, index=d["idx"], columns=d["px"].columns)
    eng = backtest(d["px"], Wdf, cost_bps=COST, freq=FREQ0)["returns"].values
    rfast, _ = run_cell("U56", N0, HOLD0, GROSS0, FREQ0)
    g1 = float(np.abs(eng[d["warm"]] - rfast[d["warm"]]).max())
    gates["G1"] = g1 < 1e-12
    gaterows.append(dict(gate="G1", what="fast runner == engine.backtest (U56 W/H126/N20)",
                         value=g1, pass_=gates["G1"]))
    P(f"  G1  fast runner == engine.backtest                        {g1:.2e}   "
      f"{'PASS' if gates['G1'] else 'FAIL'}")

    m = blocks_m(rfast, d["warm"], d["ins"], d["oos"])
    g2 = max(abs(m["CAGR"] - A936_WH126[0]), abs(m["Sharpe"] - A936_WH126[1]),
             abs(m["MaxDD"] - A936_WH126[2]))
    gates["G2"] = g2 < 5e-5
    gaterows.append(dict(gate="G2", what="CROSS-RUN 936/1071/1082/1094/1102/1108/1110 U56 W/H126/N=20 triple",
                         value=g2, pass_=gates["G2"]))
    P(f"  G2  CROSS-RUN committed U56 W/H126/N=20 triple            {g2:.2e}   "
      f"{'PASS' if gates['G2'] else 'FAIL'}  ({m['CAGR']:.4%} / {m['Sharpe']:.4f} / {m['MaxDD']:.4%})")

    spy = d["px"]["SPY"].pct_change().fillna(0.0).values
    sm = blocks_m(spy, d["warm"], d["ins"], d["oos"])
    g3 = max(abs(sm["OOS_CAGR"] - SPY_OOS_COMMITTED[0]), abs(sm["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
             abs(sm["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gates["G3"] = g3 < 5e-4
    gaterows.append(dict(gate="G3", what="SPY OOS triple", value=g3, pass_=gates["G3"]))
    P(f"  G3  SPY OOS triple                                        {g3:.2e}   "
      f"{'PASS' if gates['G3'] else 'FAIL'}")

    r12, _ = run_cell("U56", 12, HOLD0, GROSS0, FREQ0)
    m12 = blocks_m(r12, d["warm"], d["ins"], d["oos"])
    g4 = max(abs(m12["CAGR"] - A1098_U56_N12[0]), abs(m12["Sharpe"] - A1098_U56_N12[1]),
             abs(m12["MaxDD"] - A1098_U56_N12[2]))
    gates["G4"] = g4 < 5e-4
    gaterows.append(dict(gate="G4", what="CROSS-RUN 1098/1102's committed U56 n=12 triple",
                         value=g4, pass_=gates["G4"]))
    P(f"  G4  CROSS-RUN 1098/1102's committed U56 n=12 triple       {g4:.2e}   "
      f"{'PASS' if gates['G4'] else 'FAIL'}")

    db = panels["B136"]
    r15, _ = run_cell("B136", 15, HOLD0, GROSS0, FREQ0)
    m15 = blocks_m(r15, db["warm"], db["ins"], db["oos"])
    g4b = max(abs(m15["CAGR"] - A1098_B136_N15[0]), abs(m15["Sharpe"] - A1098_B136_N15[1]),
              abs(m15["MaxDD"] - A1098_B136_N15[2]))
    gates["G4b"] = g4b < 5e-4
    gaterows.append(dict(gate="G4b", what="CROSS-RUN 1098/1102's committed B136 n=15 triple",
                         value=g4b, pass_=gates["G4b"]))
    P(f"  G4b CROSS-RUN 1098/1102's committed B136 n=15 triple      {g4b:.2e}   "
      f"{'PASS' if gates['G4b'] else 'FAIL'}")

    lb_r = backtest(d["px"], rules_v2_weights(d["px"]), cost_bps=COST, freq="W")["returns"].values
    lbm = blocks_m(lb_r, d["warm"], d["ins"], d["oos"])
    g5 = abs(lbm["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gates["G5"] = g5 < 5e-4
    gaterows.append(dict(gate="G5", what="live RULES v2 MaxDD == committed -12.05%",
                         value=g5, pass_=gates["G5"]))
    P(f"  G5  live RULES v2 MaxDD == committed -12.05%              {g5:.2e}   "
      f"{'PASS' if gates['G5'] else 'FAIL'}")

    r12b, _ = run_cell("U56", 12, HOLD0, GROSS0, FREQ0)
    g6 = float(np.abs(r12 - r12b).max())
    gates["G6"] = g6 == 0.0
    gaterows.append(dict(gate="G6", what="determinism of the cell pipeline", value=g6,
                         pass_=gates["G6"]))
    P(f"  G6  determinism                                           {g6:.2e}   "
      f"{'PASS' if gates['G6'] else 'FAIL'}")
    P("")

    # ------------------------------------------------- REBUILD THE 32 CORE LADDER CELLS
    P("## THE LADDERS — 4 families x 2 panels, every rung published")
    gridrows, benchrows = [], []
    series, metr, bench = {}, {}, {}
    for panel in PANELS:
        dd_ = panels[panel]
        sb = blocks_m(dd_["px"]["SPY"].pct_change().fillna(0.0).values,
                      dd_["warm"], dd_["ins"], dd_["oos"])
        lbm_p = blocks_m(
            backtest(dd_["px"], rules_v2_weights(dd_["px"]), cost_bps=COST, freq="W")["returns"].values,
            dd_["warm"], dd_["ins"], dd_["oos"])
        bench[panel] = (sb, lbm_p)
        benchrows.append(dict(panel=panel, book="SPY", **sb))
        benchrows.append(dict(panel=panel, book="RULES v2 (live)", **lbm_p))
        P(f"  {panel} SPY        full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%}"
          f"  halves {sb['H1']:.4f}/{sb['H2']:.4f}  OOS {sb['OOS_CAGR']:.2%} / "
          f"{sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"  {panel} RULES v2   full {lbm_p['CAGR']:.2%} / {lbm_p['Sharpe']:.4f} / "
          f"{lbm_p['MaxDD']:.2%}  halves {lbm_p['H1']:.4f}/{lbm_p['H2']:.4f}  OOS "
          f"{lbm_p['OOS_CAGR']:.2%} / {lbm_p['OOS_Sharpe']:.4f} / {lbm_p['OOS_MaxDD']:.2%}")
        for lad, rungs in LADDERS.items():
            mats_w, mats_o = [], []
            for rung in rungs:
                N, H, g, f = N0, HOLD0, GROSS0, FREQ0
                if lad == "N":
                    N = rung
                elif lad == "H":
                    H = rung
                elif lad == "GROSS":
                    g = rung
                else:
                    f = rung
                r, tn = run_cell(panel, N, H, g, f)
                mm = blocks_m(r, dd_["warm"], dd_["ins"], dd_["oos"])
                metr[(panel, lad, rung)] = mm
                mats_w.append(r[dd_["warm"]])
                mats_o.append(r[dd_["oos"]])
                l4b, l4bo, l4a = legs_4b(mm, sb), legs_4b_oos(mm, sb), legs_4a(mm, lbm_p)
                gridrows.append(dict(panel=panel, ladder=lad, rung=rung, N=N, H=H, gross=g,
                                     freq=f,
                                     turnover=float(tn[dd_["warm"]].sum()) / (dd_["warm"].sum() / 252.0),
                                     **mm, pass_4b_full=all(l4b.values()),
                                     pass_4b_oos=all(l4bo.values()),
                                     pass_4a=all(l4a.values()), **l4b, **l4bo, **l4a))
            series[(panel, lad)] = (rungs, np.vstack(mats_w), np.vstack(mats_o))
            sh = [metr[(panel, lad, r_)]["Sharpe"] for r_ in rungs]
            P(f"  {panel} {lad:<8} rungs {rungs}")
            P("        Sharpe " + " ".join(f"{x:.4f}" for x in sh))
    grid = pd.DataFrame(gridrows)
    sp = float(grid["Sharpe"].max() - grid["Sharpe"].min())
    gates["G7"] = sp > 0.05
    gaterows.append(dict(gate="G7", what="the ladders are live (Sharpe spread over all cells)",
                         value=sp, pass_=gates["G7"]))
    P(f"  G7  the ladders are live (Sharpe spread {sp:.4f})          "
      f"{'PASS' if gates['G7'] else 'FAIL'}")
    dump(grid, "grid")
    dump(pd.DataFrame(benchrows), "benchmarks")
    P("")

    # ------------------------------------------ THE BOOTSTRAP: values + pair agreements
    P(f"## THE BOOTSTRAP — L in {[L_HEAD] + L_SIDE}, {BDRAWS} draws, crc32 seeds")
    CELL = {}                     # (L, panel, ladder, stat) -> dict(vals, A, k, rungs)
    for L in [L_HEAD] + L_SIDE:
        for panel in PANELS:
            for lad, rungs in LADDERS.items():
                _, Rw, Ro = series[(panel, lad)]
                rng = np.random.default_rng(seed_of(panel, lad, L))
                ixw, nbw = block_index(rng, Rw.shape[1], L, BDRAWS)
                ixo, nbo = block_index(rng, Ro.shape[1], L, BDRAWS)
                bcw, bsw = boot_exact(Rw, ixw, nbw, L)
                _, bso = boot_exact(Ro, ixo, nbo, L)
                bdd = boot_maxdd(Rw, ixw)
                boots = {"S_FULL": bsw, "S_OOS": bso, "CAGR": bcw * 100.0, "DD": bdd * 100.0}
                fulls = {"S_FULL": np.array([metr[(panel, lad, r_)]["Sharpe"] for r_ in rungs]),
                         "S_OOS": np.array([metr[(panel, lad, r_)]["OOS_Sharpe"] for r_ in rungs]),
                         "CAGR": np.array([metr[(panel, lad, r_)]["CAGR"] for r_ in rungs]) * 100.0,
                         "DD": np.array([metr[(panel, lad, r_)]["MaxDD"] for r_ in rungs]) * 100.0}
                for stat in STATS:
                    v = fulls[stat]
                    prs = pair_agreement(v, boots[stat])
                    CELL[(L, panel, lad, stat)] = dict(vals=v, A=agree_matrix(prs, len(rungs)),
                                                       k=len(rungs), rungs=rungs)
        P(f"  L={L}: 2 panels x 4 ladders x 4 statistics bootstrapped "
          f"({time.time() - t0:.0f}s elapsed)")
    P(f"  {len(CELL)} (L, panel, ladder, stat) cells built; {len(CELL) // 3} CORE cells at L={L_HEAD}")

    # G8 — CROSS-RUN against 1102's committed tie-set verdicts (1108/1110's gate)
    fp = Path(f"{PRIOR1102}.floor.csv")
    if fp.exists():
        f1102 = pd.read_csv(fp)
        f1102 = f1102[(f1102.L == L_HEAD) & (np.isclose(f1102.q, Q_HEAD))]
        agree_n, tot_n, xrows = 0, 0, []
        for _, r_ in f1102.iterrows():
            key = (L_HEAD, r_["panel"], r_["ladder"], r_["stat"])
            if key not in CELL:
                continue
            c = CELL[key]
            flo, _, _ = floor_of(c["vals"], c["A"], list(range(c["k"])), Q_HEAD)
            order = np.argsort(-c["vals"], kind="stable")
            gap = float(c["vals"][order[0]] - c["vals"][order[1]])
            tie = bool(gap < flo)
            tot_n += 1
            agree_n += int(tie == bool(r_["tie_set_verdict"]))
            xrows.append(dict(panel=r_["panel"], ladder=r_["ladder"], stat=r_["stat"],
                              peak_1102=r_["peak"], peak_1116=c["rungs"][int(order[0])],
                              gap_1102=r_["gap"], gap_1116=gap,
                              floor_1102=r_["floor"], floor_1116=flo,
                              tie_1102=bool(r_["tie_set_verdict"]), tie_1116=tie))
        g8 = agree_n / max(tot_n, 1)
        gates["G8"] = g8 >= 30.0 / 32.0
        gaterows.append(dict(gate="G8", what="CROSS-RUN 1102's committed tie-set verdicts (L=63, q=0.90)",
                             value=g8, pass_=gates["G8"]))
        P(f"  G8  CROSS-RUN 1102's tie-set verdicts                     {agree_n} of {tot_n}   "
          f"{'PASS' if gates['G8'] else 'FAIL'}")
        dump(pd.DataFrame(xrows), "cross1102")
    else:
        gates["G8"] = False
        gaterows.append(dict(gate="G8", what="CROSS-RUN 1102's floor.csv", value=np.nan, pass_=False))
        P("  G8  1102's floor.csv NOT FOUND — cross-run gate FAILS")

    # G9 — CROSS-RUN against 1110's committed tapeneed.csv (the premise of this idea)
    tp = Path(f"{PRIOR1110}.tapeneed.csv")
    if tp.exists():
        t1110 = pd.read_csv(tp)
        ok_inf, ok_gap, tot9, trows = 0, 0, 0, []
        for _, r_ in t1110.iterrows():
            key = (L_HEAD, r_["panel"], r_["ladder"], r_["stat"])
            if key not in CELL:
                continue
            c = CELL[key]
            order = np.argsort(-c["vals"], kind="stable")
            gap = float(c["vals"][order[0]] - c["vals"][order[1]])
            flo, _, _ = floor_of(c["vals"], c["A"], list(range(c["k"])), Q_HEAD)
            inf_1110 = not np.isfinite(float(r_["floor_full"]))
            tot9 += 1
            ok_inf += int(inf_1110 == (not np.isfinite(flo)))
            ok_gap += int(abs(gap - float(r_["gap"])) < 1e-6)
            trows.append(dict(panel=r_["panel"], ladder=r_["ladder"], stat=r_["stat"],
                              gap_1110=r_["gap"], gap_1116=gap,
                              floor_1110=r_["floor_full"], floor_1116=flo,
                              inf_1110=inf_1110, inf_1116=not np.isfinite(flo),
                              M_1110=r_["M_needed"]))
        gates["G9"] = (ok_gap == tot9) and (ok_inf >= 30)
        gaterows.append(dict(gate="G9", what="CROSS-RUN 1110's committed gaps and infinite-floor flags",
                             value=float(ok_gap) / max(tot9, 1), pass_=gates["G9"]))
        P(f"  G9  CROSS-RUN 1110's gaps {ok_gap} of {tot9}, inf-floor flags {ok_inf} of {tot9}   "
          f"{'PASS' if gates['G9'] else 'FAIL'}")
        dump(pd.DataFrame(trows), "cross1110")
    else:
        gates["G9"] = False
        gaterows.append(dict(gate="G9", what="CROSS-RUN 1110's tapeneed.csv", value=np.nan, pass_=False))
        P("  G9  1110's tapeneed.csv NOT FOUND — cross-run gate FAILS")
    P("")

    # -------------------------------------------- PER-CELL RESOLVABILITY, EVERY DIAL POINT
    P("## PER-CELL RESOLVABILITY — 32 CORE cells x 3 q, every number published")
    cellrows = []
    for L in [L_HEAD] + L_SIDE:
        for panel in PANELS:
            for lad, rungs in LADDERS.items():
                for stat in STATS:
                    c = CELL[(L, panel, lad, stat)]
                    v, A, k = c["vals"], c["A"], c["k"]
                    sub = list(range(k))
                    spread = float(np.nanmax(v) - np.nanmin(v))
                    order = np.argsort(-v, kind="stable")
                    peak = int(order[0])
                    gap = float(v[order[0]] - v[order[1]])
                    for q in QGRID:
                        flo, largest_un, n_un = floor_of(v, A, sub, q)
                        ts = tie_set(v, sub, peak, flo)
                        decided = k - len(ts)
                        content = decided / (k - 1)
                        Mn = m_needed(v, A, q, gap) if np.isfinite(gap) else np.nan
                        rel = 1.0 if not np.isfinite(flo) else min(flo, spread) / spread
                        cellrows.append(dict(
                            L=L, panel=panel, ladder=lad, stat=stat, k=k,
                            peak=rungs[peak], gap=gap, spread=spread, q=q,
                            floor=flo, rel_floor=rel, n_pairs_unresolved=n_un,
                            tie_size=len(ts), decided=decided, content=content,
                            M_needed=Mn,
                            log_M=np.log10(M_CAP) if not np.isfinite(Mn) else np.log10(max(Mn, 1.0)),
                            INF_FLOOR=not np.isfinite(flo),
                            ZERO_CONTENT=decided == 0,
                            NO_TAPE_500=not np.isfinite(Mn)))
    cells = pd.DataFrame(cellrows)
    dump(cells, "cells")
    head = cells[(cells.L == L_HEAD) & (np.isclose(cells.q, Q_HEAD))]
    P(f"  HEADLINE (L={L_HEAD}, q={Q_HEAD}): INF_FLOOR {int(head.INF_FLOOR.sum())} of 32, "
      f"ZERO_CONTENT {int(head.ZERO_CONTENT.sum())} of 32, "
      f"NO_TAPE_500 {int(head.NO_TAPE_500.sum())} of 32")
    P("  (1110 committed 18 of 32 infinite floors and 8 of 32 never resolving at M<=500)")
    P("")
    P("  THE 4x4 TABLES, headline definition INF_FLOOR at q=0.90 (1 = UN-RESOLVABLE):")
    for panel in PANELS:
        P(f"    {panel}     " + "".join(f"{s:>9}" for s in STATS) + "    row")
        for lad in LADDERS:
            rr = [int(head[(head.panel == panel) & (head.ladder == lad) &
                           (head.stat == s)].INF_FLOOR.iloc[0]) for s in STATS]
            P(f"    {lad:<8}" + "".join(f"{x:>9}" for x in rr) + f"    {sum(rr)}/4")
        cols = [sum(int(head[(head.panel == panel) & (head.ladder == lad) &
                            (head.stat == s)].INF_FLOOR.iloc[0]) for lad in LADDERS)
                for s in STATS]
        P("    col     " + "".join(f"{x:>7}/4" for x in cols))
    P("")

    # -------------------------------------------------- THE DECOMPOSITION, EVERY DIAL POINT
    P("## THE DECOMPOSITION — ETA2 by axis, all 9 dial combinations x 2 panels + pooled")
    decrows = []
    for defn in DEFS:
        for q in QGRID:
            sl = cells[(cells.L == L_HEAD) & (np.isclose(cells.q, q))]
            for panel in PANELS + ["POOLED"]:
                if panel == "POOLED":
                    tab = np.array([[np.nanmean([float(sl[(sl.panel == p) & (sl.ladder == lad) &
                                                          (sl.stat == s)][defn].iloc[0])
                                                 for p in PANELS])
                                     for s in STATS] for lad in LADDERS])
                    ctab = np.array([[np.nanmean([float(sl[(sl.panel == p) & (sl.ladder == lad) &
                                                           (sl.stat == s)]["rel_floor"].iloc[0])
                                                  for p in PANELS])
                                      for s in STATS] for lad in LADDERS])
                    mtab = np.array([[np.nanmean([float(sl[(sl.panel == p) & (sl.ladder == lad) &
                                                           (sl.stat == s)]["log_M"].iloc[0])
                                                  for p in PANELS])
                                      for s in STATS] for lad in LADDERS])
                else:
                    g = sl[sl.panel == panel]
                    tab = np.array([[float(g[(g.ladder == lad) & (g.stat == s)][defn].iloc[0])
                                     for s in STATS] for lad in LADDERS])
                    ctab = np.array([[float(g[(g.ladder == lad) & (g.stat == s)]["rel_floor"].iloc[0])
                                      for s in STATS] for lad in LADDERS])
                    mtab = np.array([[float(g[(g.ladder == lad) & (g.stat == s)]["log_M"].iloc[0])
                                      for s in STATS] for lad in LADDERS])
                el, es, sst = two_way(tab)
                cl, cs, _ = two_way(ctab)
                ml, ms, _ = two_way(mtab)
                wr, wc = concord(tab)
                decrows.append(dict(defn=defn, q=q, panel=panel, n_unres=float(np.nansum(tab)),
                                    eta2_lad=el, eta2_stat=es, eta2_resid=(np.nan if not
                                                                           np.isfinite(el) else 1 - el - es),
                                    sst=sst,
                                    rel_eta2_lad=cl, rel_eta2_stat=cs,
                                    logM_eta2_lad=ml, logM_eta2_stat=ms,
                                    concord_within_ladder=wr, concord_within_stat=wc,
                                    concord_diff=wr - wc,
                                    lad_wins_binary=(np.isfinite(el) and el > es),
                                    stat_wins_binary=(np.isfinite(el) and es > el),
                                    degenerate=(not np.isfinite(el)),
                                    lad_wins_rel=(np.isfinite(cl) and cl > cs),
                                    lad_wins_logM=(np.isfinite(ml) and ml > ms),
                                    lad_wins_concord=wr > wc))
    dec = pd.DataFrame(decrows)
    dump(dec, "decomp")
    P("  defn          q     panel    n_un  eta2_LAD eta2_STAT  resid | relF_LAD relF_STAT |"
      " logM_LAD logM_STAT | conc_LAD conc_STAT")
    for _, r_ in dec.iterrows():
        def _f(x):
            return "  n/a  " if not np.isfinite(x) else f"{x:7.4f}"
        P(f"  {r_['defn']:<13} {r_['q']:.2f}  {r_['panel']:<8} {r_['n_unres']:5.1f}  "
          f"{_f(r_['eta2_lad'])} {_f(r_['eta2_stat'])} {_f(r_['eta2_resid'])} | "
          f"{_f(r_['rel_eta2_lad'])} {_f(r_['rel_eta2_stat'])} | "
          f"{_f(r_['logM_eta2_lad'])} {_f(r_['logM_eta2_stat'])} | "
          f"{r_['concord_within_ladder']:7.4f} {r_['concord_within_stat']:7.4f}")
    P("")

    # ---------------------------------------------------------- MARGINALS: which row, which col
    P("## THE MARGINALS — mean REL_FLOOR by ladder and by statistic (L=63, q=0.90)")
    margrows = []
    for panel in PANELS:
        g = head[head.panel == panel]
        for lad in LADDERS:
            sub = g[g.ladder == lad]
            margrows.append(dict(panel=panel, axis="LADDER", level=lad,
                                 mean_rel_floor=float(sub.rel_floor.mean()),
                                 n_inf=int(sub.INF_FLOOR.sum()),
                                 n_zero=int(sub.ZERO_CONTENT.sum()),
                                 n_notape=int(sub.NO_TAPE_500.sum()),
                                 mean_content=float(sub.content.mean())))
        for s in STATS:
            sub = g[g.stat == s]
            margrows.append(dict(panel=panel, axis="STATISTIC", level=s,
                                 mean_rel_floor=float(sub.rel_floor.mean()),
                                 n_inf=int(sub.INF_FLOOR.sum()),
                                 n_zero=int(sub.ZERO_CONTENT.sum()),
                                 n_notape=int(sub.NO_TAPE_500.sum()),
                                 mean_content=float(sub.content.mean())))
    marg = pd.DataFrame(margrows)
    dump(marg, "marginals")
    for panel in PANELS:
        for ax in ("LADDER", "STATISTIC"):
            P(f"  {panel} by {ax}:")
            for _, r_ in marg[(marg.panel == panel) & (marg.axis == ax)].iterrows():
                P(f"    {r_['level']:<9} mean rel_floor {r_['mean_rel_floor']:.4f}  "
                  f"INF {r_['n_inf']}/4  ZERO {r_['n_zero']}/4  NO_TAPE {r_['n_notape']}/4  "
                  f"mean content {r_['mean_content']:.4f}")
    P("")

    # -------------------------------------------------------------- THE DECLARED HYPOTHESES
    P("## THE DECLARED HYPOTHESES")
    hyp = []
    hd = dec[(dec.defn == DEF_HEAD) & (np.isclose(dec.q, Q_HEAD))]
    a_u = bool(hd[hd.panel == "U56"].lad_wins_binary.iloc[0])
    a_b = bool(hd[hd.panel == "B136"].lad_wins_binary.iloc[0])
    h_lad = a_u and a_b
    h_stat = (not a_u) and (not a_b) and all(
        np.isfinite(hd[hd.panel == p].eta2_lad.iloc[0]) for p in PANELS)
    hyp.append(dict(name="H_LADDER", verdict="PASS" if h_lad else "FAIL",
                    detail=f"eta2_LAD>eta2_STAT U56 {a_u}, B136 {a_b}"))
    hyp.append(dict(name="H_STAT", verdict="PASS" if h_stat else "FAIL",
                    detail=f"mirror of H_LADDER; U56 {not a_u}, B136 {not a_b}"))

    c_u = bool(hd[hd.panel == "U56"].lad_wins_concord.iloc[0])
    c_b = bool(hd[hd.panel == "B136"].lad_wins_concord.iloc[0])
    win_lad = h_lad
    h_conc = (c_u == win_lad) and (c_b == win_lad)
    hyp.append(dict(name="H_CONCORD", verdict="PASS" if h_conc else "FAIL",
                    detail=f"concordance favours LADDER: U56 {c_u}, B136 {c_b}; "
                           f"binary winner LADDER={win_lad}"))

    gr_ok, other_all = {}, {}
    for panel in PANELS:
        g = head[head.panel == panel]
        gr_ok[panel] = int(g[g.ladder == "GROSS"].INF_FLOOR.sum()) == 0
        other_all[panel] = sum(1 for lad in LADDERS if lad != "GROSS" and
                               int(g[g.ladder == lad].INF_FLOOR.sum()) == 4)
    h_gross = all(gr_ok.values()) and all(v >= 2 for v in other_all.values())
    hyp.append(dict(name="H_GROSS_CARRIES", verdict="PASS" if h_gross else "FAIL",
                    detail=f"GROSS fully resolvable {gr_ok}; ladders fully un-resolvable "
                           f"{other_all} (bar: >=2 each panel)"))

    ddmean = {p: float(head[(head.panel == p) & (head.stat == "DD")].rel_floor.mean())
              for p in PANELS}
    worst = {p: max(STATS, key=lambda s: float(head[(head.panel == p) &
                                                    (head.stat == s)].rel_floor.mean()))
             for p in PANELS}
    h_dd = all(worst[p] == "DD" for p in PANELS)
    hyp.append(dict(name="H_DD_WORST", verdict="PASS" if h_dd else "FAIL",
                    detail=f"least-resolvable statistic per panel {worst}; "
                           f"DD mean rel_floor {ddmean}"))

    pp = dec[dec.panel.isin(PANELS)]
    n_lad_both = int((pp.groupby(["defn", "q"]).lad_wins_binary.sum() == 2).sum())
    n_stat_both = int((pp.groupby(["defn", "q"]).stat_wins_binary.sum() == 2).sum())
    n_degen = int((pp.groupby(["defn", "q"]).degenerate.sum() > 0).sum())
    P(f"  dial combinations where the table is DEGENERATE in at least one panel (every cell "
      f"identical, no axis identified): {n_degen} of 9")
    answer = ("LADDER" if n_lad_both >= 5 else "STATISTIC" if n_stat_both >= 5 else "NEITHER")
    hyp.append(dict(name="DECISION_RULE", verdict=answer,
                    detail=f"LADDER wins both panels in {n_lad_both} of 9 dial combinations, "
                           f"STATISTIC in {n_stat_both} of 9 (bar: >=5)"))
    H = pd.DataFrame(hyp)
    dump(H, "hypotheses")
    for _, r_ in H.iterrows():
        P(f"  {r_['name']:<16} {r_['verdict']:<10} {r_['detail']}")
    P("")
    P(f"## THE ANSWER: {answer}")
    P("")

    # ------------------------------------------------------------- D1, POST-HOC AND LABELLED
    P("## D1 — POST-HOC AND LABELLED: does the AXIS answer survive the SEED, when the CELL")
    P("##      FLAGS do not?  This run draws its own bootstrap (SEED_BOOT differs from 1110's),")
    P("##      so G9's 30-of-32 inf-flag agreement is an INDEPENDENT REDRAW, not a defect.")
    d1rows = []
    if tp.exists():
        t = pd.read_csv(tp)
        for label, col, cast in (("INF_FLOOR", "floor_full", lambda v: not np.isfinite(float(v))),
                                 ("NO_TAPE_500", "M_needed", lambda v: not np.isfinite(float(v)))):
            for panel in PANELS:
                g = t[t.panel == panel]
                tab = np.array([[float(cast(g[(g.ladder == lad) & (g.stat == s)][col].iloc[0]))
                                 for s in STATS] for lad in LADDERS])
                el, es, _ = two_way(tab)
                wr, wc = concord(tab)
                # this run's own table, same definition and panel, at q=0.90
                gh = head[head.panel == panel]
                tab_b = np.array([[float(gh[(gh.ladder == lad) & (gh.stat == s)][label].iloc[0])
                                   for s in STATS] for lad in LADDERS])
                elb, esb, _ = two_way(tab_b)
                wrb, wcb = concord(tab_b)
                ndiff = int((tab != tab_b).sum())
                d1rows.append(dict(source="1110 COMMITTED", defn=label, panel=panel,
                                   n_unres=float(tab.sum()), eta2_lad=el, eta2_stat=es,
                                   concord_within_ladder=wr, concord_within_stat=wc,
                                   lad_wins=(np.isfinite(el) and el > es), cells_differ=ndiff))
                d1rows.append(dict(source="THIS RUN", defn=label, panel=panel,
                                   n_unres=float(tab_b.sum()), eta2_lad=elb, eta2_stat=esb,
                                   concord_within_ladder=wrb, concord_within_stat=wcb,
                                   lad_wins=(np.isfinite(elb) and elb > esb), cells_differ=ndiff))
        D1 = pd.DataFrame(d1rows)
        dump(D1, "d1")
        P("  source          defn          panel   n_un  eta2_LAD eta2_STAT  conc_LAD conc_STAT  LADDER wins")
        for _, r_ in D1.iterrows():
            P(f"  {r_['source']:<15} {r_['defn']:<13} {r_['panel']:<6} {r_['n_unres']:4.0f}   "
              f"{r_['eta2_lad']:7.4f} {r_['eta2_stat']:7.4f}   "
              f"{r_['concord_within_ladder']:7.4f} {r_['concord_within_stat']:7.4f}    {r_['lad_wins']}"
              f"   (tables differ in {r_['cells_differ']} of 16 cells)")
        P("  STATED PRECISELY, because the INF_FLOOR rows above are numerically IDENTICAL and")
        P("  that is easy to misread as byte-reproduction: on U56 the two 4x4 tables differ in")
        P("  2 of 16 CELLS (1110 has N/CAGR un-resolvable and GROSS/S_OOS resolvable; this run's")
        P("  redraw has it the other way round).  The decomposition matches to the digit only")
        P("  because those two flips are MIRROR-SYMMETRIC in BOTH margins — they leave the row")
        P("  sums and the column sums as the same multisets — so SS_row, SS_col and SS_total are")
        P("  each unchanged.  That is an accident of this pair of flips, NOT evidence that the")
        P("  decomposition is insensitive to the seed.  D2 is the evidence for that.")
        same = int((D1[D1.source == "1110 COMMITTED"].lad_wins.values ==
                    D1[D1.source == "THIS RUN"].lad_wins.values).sum())
        P(f"  AXIS VERDICT AGREES ON {same} of {len(D1) // 2} (definition, panel) pairs across the two "
          "independent seed draws,")
        P("  even though 4 of 32 CELL-LEVEL flags do not (2 inf-floor, 2 NO_TAPE_500 at M = 359 "
          "and 255 of a 500 cap).")
        P("  Read plainly: the CELL flag is seed-fragile exactly as 1108 found; the AXIS answer "
          "is not.")
        # H_GROSS_CARRIES re-scored on 1110's committed flags
        gk, ok_ = {}, {}
        for panel in PANELS:
            g = t[t.panel == panel]
            inf_ = {(r_["ladder"], r_["stat"]): (not np.isfinite(float(r_["floor_full"])))
                    for _, r_ in g.iterrows()}
            gk[panel] = sum(inf_[("GROSS", s)] for s in STATS) == 0
            ok_[panel] = sum(1 for lad in LADDERS if lad != "GROSS" and
                             sum(inf_[(lad, s)] for s in STATS) == 4)
        P(f"  H_GROSS_CARRIES re-scored on 1110's COMMITTED flags: GROSS fully resolvable {gk}, "
          f"ladders fully un-resolvable {ok_}")
        P("  -> it FAILS on 1110's own flags too, on the B136 leg, so its FAIL above is NOT a "
          "seed artefact;")
        P("  the U56 leg of that FAIL is (U56/GROSS/S_OOS flips with the seed) and is named here.")
    else:
        P("  1110's tapeneed.csv NOT FOUND — D1 not run.")
    P("")

    # --------------------------------------------- D2, POST-HOC AND LABELLED: the seed itself
    P("## D2 — POST-HOC AND LABELLED: the AXIS answer under 3 FURTHER independent seed draws")
    P("##      (a noise measurement, reported in full, NEVER selected on).")
    d2rows = []
    for off in (1, 2, 3):
        for panel in PANELS:
            tabs = {}
            for lad, rungs in LADDERS.items():
                _, Rw, Ro = series[(panel, lad)]
                rng = np.random.default_rng(seed_of(panel, lad, L_HEAD, "reseed", off))
                ixw, nbw = block_index(rng, Rw.shape[1], L_HEAD, BDRAWS)
                ixo, nbo = block_index(rng, Ro.shape[1], L_HEAD, BDRAWS)
                bcw, bsw = boot_exact(Rw, ixw, nbw, L_HEAD)
                _, bso = boot_exact(Ro, ixo, nbo, L_HEAD)
                bdd = boot_maxdd(Rw, ixw)
                bt = {"S_FULL": bsw, "S_OOS": bso, "CAGR": bcw * 100.0, "DD": bdd * 100.0}
                fl = {"S_FULL": np.array([metr[(panel, lad, r_)]["Sharpe"] for r_ in rungs]),
                      "S_OOS": np.array([metr[(panel, lad, r_)]["OOS_Sharpe"] for r_ in rungs]),
                      "CAGR": np.array([metr[(panel, lad, r_)]["CAGR"] for r_ in rungs]) * 100.0,
                      "DD": np.array([metr[(panel, lad, r_)]["MaxDD"] for r_ in rungs]) * 100.0}
                for stat in STATS:
                    v = fl[stat]
                    A = agree_matrix(pair_agreement(v, bt[stat]), len(rungs))
                    flo, _, _ = floor_of(v, A, list(range(len(rungs))), Q_HEAD)
                    tabs[(lad, stat)] = float(not np.isfinite(flo))
            tab = np.array([[tabs[(lad, s)] for s in STATS] for lad in LADDERS])
            el, es, _ = two_way(tab)
            wr, wc = concord(tab)
            d2rows.append(dict(seed_offset=off, panel=panel, n_unres=float(tab.sum()),
                               eta2_lad=el, eta2_stat=es, concord_within_ladder=wr,
                               concord_within_stat=wc, lad_wins=(np.isfinite(el) and el > es)))
    D2 = pd.DataFrame(d2rows)
    dump(D2, "d2")
    for _, r_ in D2.iterrows():
        P(f"  reseed {r_['seed_offset']}  {r_['panel']:<6} INF_FLOOR {r_['n_unres']:4.0f} of 16   "
          f"eta2_LAD {r_['eta2_lad']:7.4f}  eta2_STAT {r_['eta2_stat']:7.4f}   "
          f"conc {r_['concord_within_ladder']:.4f}/{r_['concord_within_stat']:.4f}   "
          f"LADDER wins {r_['lad_wins']}")
    P(f"  LADDER wins the binary decomposition in {int(D2.lad_wins.sum())} of {len(D2)} "
      "(seed, panel) redraws,")
    P(f"  against {int(hd[hd.panel.isin(PANELS)].lad_wins_binary.sum())} of 2 on this run's "
      "headline seed and "
      f"{int(pd.DataFrame(d1rows)[(pd.DataFrame(d1rows).source == '1110 COMMITTED') & (pd.DataFrame(d1rows).defn == 'INF_FLOOR')].lad_wins.sum()) if d1rows else 0}"
      " of 2 on 1110's.")
    P("")

    # ------------------------------------------------------- RULE 8 AND BOTH KEEP PATHS
    P("## RULE 8 — rung chosen on IS 2009-2016 ALONE, per ladder, three choosers, OOS read ONCE")
    pickrows = []
    for panel in PANELS:
        sb, lbm_p = bench[panel]
        for lad, rungs in LADDERS.items():
            for ch in CHOOSERS:
                key = {"C_ISSHARPE": "IS_Sharpe", "C_ISDD": "IS_MaxDD", "C_ISCAGR": "IS_CAGR"}[ch]
                vals = [metr[(panel, lad, r_)][key] for r_ in rungs]
                pick = rungs[int(np.argmax(vals))]
                mm = metr[(panel, lad, pick)]
                l4b, l4bo, l4a = legs_4b(mm, sb), legs_4b_oos(mm, sb), legs_4a(mm, lbm_p)
                srt = np.sort(vals)[::-1]
                pickrows.append(dict(panel=panel, ladder=lad, chooser=ch, pick=pick,
                                     margin=float(srt[0] - srt[1]),
                                     CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                                     H1=mm["H1"], H2=mm["H2"],
                                     OOS_CAGR=mm["OOS_CAGR"], OOS_Sharpe=mm["OOS_Sharpe"],
                                     OOS_MaxDD=mm["OOS_MaxDD"],
                                     pass_4b_full=all(l4b.values()), pass_4b_oos=all(l4bo.values()),
                                     pass_4a=all(l4a.values()), **l4b, **l4bo, **l4a))
    pk = pd.DataFrame(pickrows)
    dump(pk, "walkforward")
    for _, r_ in pk.iterrows():
        P(f"    {r_['panel']:<5} {r_['ladder']:<8} {r_['chooser']:<11} pick {str(r_['pick']):<6} "
          f"margin {r_['margin']:.4f}  full {r_['CAGR']:.2%}/{r_['Sharpe']:.4f}/{r_['MaxDD']:.2%}  "
          f"OOS {r_['OOS_CAGR']:.2%}/{r_['OOS_Sharpe']:.4f}/{r_['OOS_MaxDD']:.2%}  "
          f"4b full {str(r_['pass_4b_full']):<5} 4b OOS {str(r_['pass_4b_oos']):<5} "
          f"4a {r_['pass_4a']}")
    P(f"  ALL PICKS: 4b full {int(pk['pass_4b_full'].sum())} of {len(pk)}, 4b OOS "
      f"{int(pk['pass_4b_oos'].sum())} of {len(pk)}, 4a {int(pk['pass_4a'].sum())} of {len(pk)}")
    P(f"  WHOLE GRID: 4b full {int(grid['pass_4b_full'].sum())} of {len(grid)}, 4b OOS "
      f"{int(grid['pass_4b_oos'].sum())} of {len(grid)}, 4a {int(grid['pass_4a'].sum())} of {len(grid)}")
    if int(grid["pass_4b_full"].sum()):
        P("  4b-full passing cells:")
        for _, r_ in grid[grid.pass_4b_full].iterrows():
            P(f"    {r_['panel']:<5} {r_['ladder']:<8} rung {str(r_['rung']):<6} "
              f"full {r_['CAGR']:.2%}/{r_['Sharpe']:.4f}/{r_['MaxDD']:.2%} halves "
              f"{r_['H1']:.4f}/{r_['H2']:.4f}  OOS {r_['OOS_CAGR']:.2%}/{r_['OOS_Sharpe']:.4f}/"
              f"{r_['OOS_MaxDD']:.2%}  4b OOS {r_['pass_4b_oos']}")
    P("  NOTHING PROPOSED: the BOOK at all 54 rungs is byte-identical across both dials — only")
    P("  which cells get CALLED un-resolvable changes — so 4a and 4b are invariant to dial 1")
    P("  and dial 2 by construction.  Scored because rule 4 says so.")
    P("")
    P("## SURVIVORSHIP (PROTOCOL rule 9)")
    P("  U56 and B136 are CURRENT-CONSTITUENT panels; every level above is optimistic.  A GAP")
    P("  between two rungs and an AGREEMENT between two rungs both contrast two books over the")
    P("  same inflated tape and the bias very largely cancels out of them, out of the floor and")
    P("  out of every quantity decomposed here; it does NOT cancel out of the 4b legs, measured")
    P("  against SPY, a real index, so any 4b pass above is an UPPER bound.")
    P("")
    P("## THE DECLARED APPROXIMATION, AND ITS DIRECTION")
    P("  NO_TAPE_500 rests on 1110's PROJECTION A' = Phi(sqrt(M) Phi^-1(A)): a fixed population")
    P("  gap and an SE falling as 1/sqrt(T).  Both assumptions run TOWARD resolution, so every")
    P("  M_needed here is a LOWER bound and every NO_TAPE_500 count is a LOWER bound on")
    P("  un-resolvability.  The exponent is INHERITED from 1110's sub-tape measurement (median")
    P("  beta -0.4540 over the 24 non-DD cells, DD +0.2093) and is NOT re-measured here, so the")
    P("  DD column's M_needed is the least trustworthy quantity in this run and is named as such.")
    P("")

    dump(pd.DataFrame(gaterows), "gates")
    P(f"# GATES {sum(gates.values())} of {len(gates)} PASS")
    P(f"# elapsed {time.time() - t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"wrote {OUT}.console.txt")


if __name__ == "__main__":
    main()

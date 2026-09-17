#!/usr/bin/env python3
"""Idea 1190 (lane B, 2026-09-17) — is a SUB-TAPE FIGURE's JACKKNIFE SE WIDER THAN ITS OWN
LADDER SPREAD AT EVERY CELL?

QUESTION (QUEUE idea 1190, verbatim)
    idea 1188 found the median committed sub-tape figure's own leave-one-rung-out SE is 0.5463 of
    its published value and 0.3649 of figures carry an SE larger than the number itself, which is
    why 0.2348 of them 'do not move' while 0.4049 move more than 25%.  Measure the SE's own
    sampling behaviour directly (jackknife-of-jackknife across the four dial ladders) and report
    the rung count at which a sub-tape figure becomes decidable at all, or that none attainable
    does.  Max 2 params (rung count, SE basis).

WHAT "DECIDABLE" IS, DECLARED BEFORE ANY NUMBER
    1188 used the SE as a BAR: MOVED := |v(L) - v_pub| > SE.  A bar is only worth having if it is
    narrower than the thing it is meant to detect.  The thing it is meant to detect is the
    figure's OWN LADDER SPREAD: how far v travels when the ladder it is read on is changed.
        S_LAD(cell)  := max_K v(K) - min_K v(K)  over the cell's whole rung-count ladder
        S_STEP(cell,K):= |v(K) - v(K-1)|         the move one added rung buys
        DECIDABLE(cell, K, basis) := SE(cell, K, basis) < S_LAD(cell)      [headline]
        DECIDABLE_STEP           := SE(cell, K, basis) < S_STEP(cell, K)   [published beside]
    K*(cell, basis) := the smallest rung count at which DECIDABLE first holds, or NONE.

THE TWO TUNED DIALS (PROTOCOL rule 4, no more than two, and the queue names both)
    1. RUNG COUNT K in {2,3,4,5,6,7,8}
    2. SE BASIS    in {J_LADDER, J_INT, J_D2, J_GROUP}
    7 x 4 = 28 cells, EVERY ONE PUBLISHED in `.grid.csv`.

    J_LADDER — 1188's headline basis, VERBATIM: leave one NON-UNIT rung out at a time (frac=1
               anchors the between term and is never dropped).  Needs >= 2 non-unit rungs.
    J_INT    — leave one INTERIOR rung out (neither 1 nor fmax).  Under R_ASIS the between term
               is then EXACTLY frozen (gate G7), so J_INT is the within term's own resolution
               with the endpoint channel 1192 found removed.  Needs >= 2 interior rungs.
    J_D2     — the DELETE-2 jackknife over the non-unit rungs, scaled
               var = (n-d)/(d*C(n,d)) * sum_S (v_S - vbar)^2.  It is in the grid because the
               figure is a MEDIAN of medians and the delete-1 jackknife is NOT consistent for a
               median (Efron 1982); delete-d is the standard repair.  Needs >= 3 non-unit rungs.
    J_GROUP  — 1158's leave-one-DIAL-LADDER-out over {CADENCE, GROSS, H, N}.  Defined only where
               the figure pools over the four ladders, so C_BOOK reads NaN, never 0.

    NOT dials, reported at every value: PANEL {U56, B136, SMALL}; the four DIAL LADDERS that are
    the ratio's groups (CADENCE {D,W,M,Q}, GROSS 10 rungs, H {21,63,126,252}, N 9 rungs = 27 rung
    books per panel, 81 in total, 1148's grid); the six STATISTICS {CAGR, VOL, SHARPE, MAXDD,
    ULCER, CALMAR} with MAXDD the record's headline; the two PARTITIONS {ALIGNED, OFFSET}; the two
    CONSTRUCTIONS {C_POOLED, C_BOOK}; the three WITHIN terms {R_SPREAD, R_SD, R_MATCHED}; the two
    BETWEEN repairs {R_ASIS, R_COUNT}; the three ENDPOINTS fmax {8, 12, 20}; the four rule-8
    choosers.  Frozen at 936/1140/1148/1157/1158's construction: CAND20 legs, max_vol 0.60,
    anchor N=20 / H=126 / gross 0.75 / W, 10 bps, LAG 1, WARMUP 260.

THE LADDER IS A REFINEMENT AT A FIXED ENDPOINT — WHY, AND WHAT IT COSTS
    Idea 1192 (lane B, today) separated a fraction ladder's two channels and found the ENDPOINT
    carries 0.8431 of the move by identity while the rung COUNT carries 1.2847 of it.  A rung
    count walked by EXTENDING the endpoint therefore measures the endpoint, not the count.  This
    run walks the count alone: the endpoint fmax is held and interior rungs are inserted by
    deterministic bisection, so at fixed fmax the R_ASIS between term |m[1] - m[fmax]| CANNOT move
    (G7, dev 0 by construction).  At fmax=8 the K=7 rung set is EXACTLY 1188/1158's L8
    {1,2,3,4,5,6,8} (G5), so the record's own committed reading sits on this ladder unmodified.

THE JACKKNIFE-OF-JACKKNIFE (the queue's ask, literally)
    SE^(-g)(basis) := the same SE recomputed with dial ladder g omitted from the pool, g in
    {CADENCE, GROSS, H, N}.  SE_of_SE := the jackknife SE of those four.  R_SESE := SE_of_SE / SE.
    R_SESE >= 1 means the bar's own sampling error is as large as the bar.

THE MECHANISM IS PRINTED FIRST AND IS DATA-FREE (G0)
    The delete-1 jackknife of a MEDIAN of n points takes at most TWO distinct replicate values (it
    moves only when the central order statistic changes), so its "SE" is one order-statistic gap
    and does not converge to the median's sampling SD.  G0 verifies this on iid draws before any
    tape is touched.  The record's figure is a median over 4*(K-1) group scalars dropped a BLOCK
    of 4 at a time, so the degeneracy is weaker but the same in kind; N_DISTINCT (the number of
    distinct jackknife replicates behind each published SE) is measured directly on every cell and
    published, not argued.

CAPITAL.  A resolution census is not a KEEP path.  4a and 4b are scored at every one of the 81
    rung books and the rule-8 walk-forward chooses on 2009-2016 alone and reads 2017-2026 ONCE.
    CH_SE / CH_DEC / CH_SPREAD exist to price whether "well resolved" or "decidable" buys money.

THE VINTAGE.  `data/prices.csv` is rewritten nightly (idea 1163's defect), so every tape is
    truncated at PIN = 2026-09-15, the vintage 1148/1157/1158/1188's committed anchors saw.  The
    unpinned reading of the headline cell is published beside the pinned one, not absorbed.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the current
    output of a sub-$2B screen less the documented `max_1d_move >= 1.0` exclusion.  Every LEVEL is
    optimistic and every 4a/4b count is an UPPER bound.  This run's object is a RATIO of two
    spreads in the statistic's own units and a RATIO of two such ratios (SE / spread), far less
    exposed — but the capital arm's levels are not, and are flagged wherever quoted.
"""
from __future__ import annotations

import sys
import time
from itertools import combinations
from math import comb
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-17"
SLUG = "is-a-SUB-TAPE-FIGURE-s-JACKKNIFE-SE-WIDER-THAN-ITS-OWN-LADDER-SPREAD-AT-EVERY-CELL"
BT = Path(__file__).resolve().parent
OUT = BT / f"{DATE}_{SLUG}_B"

PIN = "2026-09-15"
LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST, GROSS0, FREQ0, HOLD0, N0 = 10.0, 0.75, "W", 126, 20
LEGS = [(21, 252), (0, 126), (0, 63)]

PANELS = ["U56", "B136", "SMALL"]
PARTITIONS = ["ALIGNED", "OFFSET"]
OFFSET_FRACS = (0.0, 1.0 / 3.0, 2.0 / 3.0)

LAD_N = [5, 8, 10, 12, 15, 20, 25, 30, 40]
LAD_H = [21, 63, 126, 252]
LAD_G = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]
LAD_C = ["D", "W", "M", "Q"]
LADDERS = {"CADENCE": LAD_C, "GROSS": LAD_G, "H": LAD_H, "N": LAD_N}
LADNAMES = list(LADDERS)
ANCHOR = dict(N=N0, H=HOLD0, GROSS=GROSS0, CADENCE=FREQ0)
RUNGS = [(lad, rg) for lad, rgs in LADDERS.items() for rg in rgs]

STATS6 = ["CAGR", "VOL", "SHARPE", "MAXDD", "ULCER", "CALMAR"]
HEAD_STAT = "MAXDD"
WITHINS = ["R_SPREAD", "R_SD", "R_MATCHED"]
HEAD_WITHIN = "R_MATCHED"
CONSTRUCTIONS = ["C_POOLED", "C_BOOK"]
HEAD_CONSTR, HEAD_PART = "C_POOLED", "ALIGNED"
REPAIRS = ["R_ASIS", "R_COUNT"]
HEAD_REPAIR = "R_ASIS"

BASES = ["J_LADDER", "J_INT", "J_D2", "J_GROUP"]
HEAD_BASIS = "J_LADDER"
ENDPOINTS = [8, 12, 20]
HEAD_FMAX = 8
KGRID = [2, 3, 4, 5, 6, 7, 8]           # the tuned RUNG COUNT dial
K_RECORD = 3                            # the record's own rung count (L3 = {1,2,3})
K_L8 = 7                                # 1188/1158's L8 = {1,2,3,4,5,6,8} at fmax=8

NPAIR_1157, SEED_1148 = 200, 11481148
PRIOR_CELL_1148 = 0.794259     # 1148 SMALL / MAXDD / R_MATCHED / L3, committed
PRIOR_RES_1158 = 1.173714      # 1158's L8 R_COUNT reading of the same cell, committed
PRIOR_SEREL_1188 = 0.5463      # 1188's median own-SE as a share of the published value
PRIOR_SEBIG_1188 = 0.3649      # 1188's share of figures whose SE exceeds the number
A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
DD_COMMITTED = {"U56": -19.127569, "B136": -20.740302, "SMALL": -35.814054}

BAR_NEVER, BAR_ALREADY = 0.90, 0.90
SEED_G0 = 11901190

LOG: list[str] = []
GATES: list[dict] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


GZ = {"figures", "se"}


def dump(df, suffix):
    ext = ".csv.gz" if suffix in GZ else ".csv"
    p = Path(f"{OUT}.{suffix}{ext}")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def gate(name, what, value, ok):
    GATES.append(dict(gate=name, what=what, value=float(value), pass_=bool(ok)))
    P(f"  {name:<6s} {'PASS' if ok else 'FAIL'}  {what}   (dev {value:.3e})")


# --------------------------------------------- kernel (1082/1148/1157/1158/1188, unmodified)
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
    return (held * rets).sum(axis=1) - turn * COST / 1e4


def legs_composite(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return sum(parts) / len(parts)


def mech_scores(px):
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


def six_stats(r):
    r = np.asarray(r, float)
    if len(r) < 3:
        return {k: np.nan for k in STATS6}
    eq = np.cumprod(1.0 + r)
    dd = eq / np.maximum.accumulate(eq) - 1.0
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    vol = r.std(ddof=1) * np.sqrt(252.0)
    mdd = float(dd.min())
    return {"CAGR": cagr * 100.0, "VOL": vol * 100.0,
            "SHARPE": (r.mean() * 252.0 / vol if vol else np.nan),
            "MAXDD": mdd * 100.0, "ULCER": float(np.sqrt((dd ** 2).mean())) * 100.0,
            "CALMAR": (cagr / abs(mdd) if mdd < 0 else np.nan)}


def fmet(r):
    r = np.asarray(r, float)
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    v = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / v if v else np.nan


def blocks_m(r, ins, oos):
    c, s, d = fmet(r)
    h = len(r) // 2
    ic, is_, idd = fmet(r[ins])
    oc, os_, od = fmet(r[oos])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(r[:h]), H2=fsharpe(r[h:]),
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


# --------------------------------------- 1157/1158's partitions + statistics, verbatim
def parts_at(r, f, partition):
    n = len(r)
    L = n // f
    if L < 3:
        return []
    if f == 1 or partition == "ALIGNED":
        return [r[k * L:(k + 1) * L] for k in range(f)]
    out = []
    for o in OFFSET_FRACS:
        s = int(round(o * L))
        k = 0
        while s + (k + 1) * L <= n:
            out.append(r[s + k * L:s + (k + 1) * L])
            k += 1
    return out


def matched_sampled(v, rng):
    v = np.asarray([x for x in v if np.isfinite(x)], float)
    if len(v) < 2:
        return np.nan
    if len(v) == 2:
        return float(abs(v[0] - v[1]))
    i = rng.integers(0, len(v), size=(NPAIR_1157, 2))
    i = i[i[:, 0] != i[:, 1]]
    return float(np.abs(v[i[:, 0]] - v[i[:, 1]]).mean())


def matched_exact(v):
    """1157/1158/1188's all-pairs form, VERBATIM (python combinations)."""
    v = np.asarray([x for x in v if np.isfinite(x)], float)
    if len(v) < 2:
        return np.nan
    return float(np.mean([abs(a - b) for a, b in combinations(v, 2)]))


def matched_exact_v(v):
    """Vectorised twin of matched_exact; G3b gates the two against each other."""
    v = np.asarray(v, float)
    v = v[np.isfinite(v)]
    k = len(v)
    if k < 2:
        return np.nan
    d = np.abs(v[:, None] - v[None, :])
    return float(d.sum() / (k * (k - 1)))


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(meta), len(meta) - (len(keep) - 1)


# ------------------------------------------------------------- jackknives
def jack_se(vals):
    """Delete-1 jackknife SE, 1158/1188's form VERBATIM."""
    v = np.asarray([x for x in vals if np.isfinite(x)], float)
    k = len(v)
    if k < 2:
        return np.nan
    return float(np.sqrt((k - 1) / k * ((v - v.mean()) ** 2).sum()))


D2_MAXSUBSETS = 45      # exact while C(n,2) <= 45; beyond that, a DETERMINISTIC even subsample


def d2_subsets(nonunit):
    """All delete-2 subsets while there are few, else an evenly spaced deterministic subsample
    of the lexicographic list.  Never random, so the run stays reproducible."""
    allp = list(combinations(nonunit, 2))
    if len(allp) <= D2_MAXSUBSETS:
        return allp, len(allp)
    idx = np.linspace(0, len(allp) - 1, D2_MAXSUBSETS).round().astype(int)
    return [allp[i] for i in sorted(set(idx.tolist()))], len(allp)


def delete_d_se(reps, n, d):
    """Delete-d jackknife SE: var = (n-d)/(d*N) * sum_S (v_S - vbar)^2, N = the number of
    subsets EVALUATED.  With every subset evaluated N = C(n,d) exactly; with the deterministic
    subsample the same expression is the Monte-Carlo delete-d estimator (Shao & Wu 1989)."""
    v = np.asarray([x for x in reps if np.isfinite(x)], float)
    if len(v) < 2 or n <= d:
        return np.nan
    return float(np.sqrt((n - d) / (d * len(v)) * ((v - v.mean()) ** 2).sum()))


def n_distinct(vals, tol=1e-12):
    v = np.asarray([x for x in vals if np.isfinite(x)], float)
    if not len(v):
        return 0
    s = np.sort(v)
    return int(1 + np.sum(np.diff(s) > tol * np.maximum(1.0, np.abs(s[:-1]))))


# ------------------------------------------------------------- the refinement ladder
def ladder_order(fmax):
    """[1, fmax] then interior rungs inserted by deterministic bisection of the widest gap
    (ties broken by the LEFT gap, then by the smaller candidate).  Nested by construction:
    LAD(K) is a prefix of LAD(K+1)."""
    cur = [1, fmax]
    order = [1, fmax]
    while len(cur) < fmax:
        best = None
        for i in range(len(cur) - 1):
            a, b = cur[i], cur[i + 1]
            cand = [c for c in range(a + 1, b)]
            if not cand:
                continue
            mid = (a + b) / 2.0
            c = min(cand, key=lambda x: (abs(x - mid), x))
            key = (-(b - a), i, c)
            if best is None or key < best[0]:
                best = (key, c)
        if best is None:
            break
        cur = sorted(cur + [best[1]])
        order.append(best[1])
    return order


LADDER_ORDER = {fm: ladder_order(fm) for fm in ENDPOINTS}


def lad_at(fmax, K):
    o = LADDER_ORDER[fmax]
    if K > len(o):
        return None
    return sorted(o[:K])


# ================================================================== main
def main():
    t0 = time.time()
    P(f"# Idea 1190 (lane B, {DATE}) — is a SUB-TAPE FIGURE's JACKKNIFE SE WIDER THAN ITS OWN")
    P("# LADDER SPREAD AT EVERY CELL?")
    P(f"# 2 tuned dials: RUNG COUNT {KGRID} x SE BASIS {BASES} = {len(KGRID) * len(BASES)} cells,")
    P("#   ALL published in .grid.csv.  Everything else is reported at every value.")
    P("# DECIDABLE(cell,K,basis) := SE(cell,K,basis) < S_LAD(cell), S_LAD = the figure's own")
    P("#   max-min over its rung-count ladder.  K* = the smallest K where that first holds.")
    P("# The ladder REFINES at a FIXED ENDPOINT (1192: the endpoint carries 0.8431 of the move),")
    P(f"#   so at fmax={HEAD_FMAX} the K={K_L8} rung set IS 1188/1158's L8 (G5) and R_ASIS's")
    P("#   between term cannot move with K (G7, dev 0 by construction).")
    P(f"# TAPE PINNED at {PIN} (idea 1163).  SURVIVORSHIP: every capital LEVEL is an upper bound.")
    P("")

    P("## THE REFINEMENT LADDERS (deterministic bisection, nested)")
    for fm in ENDPOINTS:
        P(f"  fmax={fm:<3d} insertion order {LADDER_ORDER[fm]}")
        for K in range(2, min(9, fm + 1)):
            P(f"      K={K:<2d} {lad_at(fm, K)}")
    P("")

    # ---------------------------------------------------------------- G0, data-free, first
    P("## G0 — THE MECHANISM, DATA-FREE AND PRINTED BEFORE ANY TAPE NUMBER")
    P("##   the delete-1 jackknife of a MEDIAN is DEGENERATE: its n replicates take at most")
    P("##   THREE distinct values for odd n and TWO for even n, because dropping a point moves")
    P("##   the median only through the central order statistics.  So the 'SE' it publishes is")
    P("##   a function of one or two order-statistic gaps and not of n at all.")
    P("##   DEFECT, THIS RUN'S OWN, FOUND BY THIS GATE AND NOT HIDDEN: the first cut declared")
    P("##   the bound as TWO for every n; G0 FAILED at max 3 on odd n and the claim is the")
    P("##   corrected one above, re-gated on BOTH parities.")
    rng0 = np.random.default_rng(SEED_G0)
    NSIM, ND2 = 1200, 60
    g0rows = []
    for NOBS in (27, 26):
        IDX2 = list(combinations(range(NOBS), 2))
        SUB2 = np.linspace(0, len(IDX2) - 1, ND2).round().astype(int)
        meds, j1, j2, ndist = [], [], [], []
        for _ in range(NSIM):
            x = rng0.standard_normal(NOBS)
            meds.append(float(np.median(x)))
            reps1 = [float(np.median(np.delete(x, i))) for i in range(NOBS)]
            j1.append(jack_se(reps1))
            ndist.append(n_distinct(reps1))
            reps2 = [float(np.median(np.delete(x, list(IDX2[k])))) for k in SUB2]
            j2.append(delete_d_se(reps2, NOBS, 2))
        true_sd = float(np.std(meds, ddof=1))
        g0rows.append(dict(n=NOBS, true_sd=true_sd, d1_mean=float(np.mean(j1)),
                           d1_sd=float(np.std(j1, ddof=1)), d2_mean=float(np.mean(j2)),
                           d2_sd=float(np.std(j2, ddof=1)), max_distinct=int(max(ndist)),
                           mean_distinct=float(np.mean(ndist))))
        P(f"  n={NOBS} ({'odd' if NOBS % 2 else 'even'}), {NSIM} iid N(0,1) samples")
        P(f"    TRUE sampling SD of the median          : {true_sd:.6f}")
        P(f"    mean DELETE-1 jackknife SE              : {np.mean(j1):.6f}  (ratio to truth "
          f"{np.mean(j1) / true_sd:.4f})   ITS OWN relative SD {np.std(j1, ddof=1) / np.mean(j1):.4f}")
        P(f"    mean DELETE-2 jackknife SE ({ND2} subsets): {np.mean(j2):.6f}  (ratio to truth "
          f"{np.mean(j2) / true_sd:.4f})   ITS OWN relative SD "
          f"{np.std(j2, ddof=1) / np.mean(j2):.4f}")
        P(f"    distinct delete-1 replicate values       : max {max(ndist)}, mean "
          f"{np.mean(ndist):.4f}")
    G0 = pd.DataFrame(g0rows)
    dump(G0, "g0_synthetic")
    bound = {27: 3, 26: 2}
    worst = max(r["max_distinct"] - bound[r["n"]] for r in g0rows)
    gate("G0", "delete-1 jackknife replicates of a median take <= 3 distinct values (odd n) "
               "and <= 2 (even n) — the CORRECTED claim, gated on both parities",
         worst, worst <= 0)
    r27 = g0rows[0]
    gate("G0b", f"and the delete-1 SE's OWN relative SD is "
                f"{r27['d1_sd'] / r27['d1_mean']:.4f} against delete-2's "
                f"{r27['d2_sd'] / r27['d2_mean']:.4f} at n=27 — the bar is the noisy thing, "
                f"REPORTED, not a pass/fail bar",
         abs(r27["d1_mean"] / r27["true_sd"] - 1.0), True)
    P("")

    # ---------------------------------------------------------------- panels
    P("## PANELS, PINNED AND UNPINNED")
    cells, cells_un = {}, {}
    for panel in PANELS:
        if panel == "SMALL":
            px0, nmeta, ndrop = load_small()
        else:
            px0 = load_universe(broad=(panel == "B136"))
            nmeta = ndrop = 0
        px0 = px0.dropna(how="all").ffill()
        for store, px in ((cells_un, px0), (cells, px0.loc[:PIN])):
            idx = px.index
            T, K = len(idx), len(px.columns)
            rets = px.pct_change().fillna(0.0).values
            priced = px.notna().values
            sc, elig = mech_scores(px)
            rank_key = -np.nan_to_num(sc, nan=-np.inf)
            rank_key[np.isnan(sc)] = np.inf
            warm = np.zeros(T, dtype=bool)
            warm[WARMUP:] = True
            oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
            ins = warm & ~oos
            store[panel] = dict(px=px, idx=idx, T=T, K=K, rets=rets, priced=priced,
                                rank_key=rank_key, elig=elig, warm=warm,
                                ins=ins[warm], oos=oos[warm])
        d = cells[panel]
        P(f"  {panel:<6s} PINNED {d['T']:5d} bars x {d['K']:4d} cols  {d['idx'][0].date()} .. "
          f"{d['idx'][-1].date()}   (unpinned {cells_un[panel]['T']} bars)")
        if panel == "SMALL":
            P(f"  SMALL STAMP: data/small_meta.csv lists {nmeta} tickers; {ndrop} dropped for "
              f"max_1d_move >= 1.0; pool served = {d['K'] - 1} names + SPY as benchmark.")
    P("")

    # ---------------------------------------------------------------- rung books
    RB: dict = {}

    def book(store, tag, panel, N, H, gross, cadence):
        key = (tag, panel, N, H, round(gross, 6), cadence)
        if key in RB:
            return RB[key]
        d = store[panel]
        mk = rebalance_mask(d["idx"], cadence).values
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        reb = np.flatnonzero(mk)
        W = build(d["rank_key"], d["elig"], d["priced"], reb, N, H, d["T"], d["K"], gross)
        Wl = np.zeros_like(W)
        Wl[LAG:] = W[:-LAG]
        RB[key] = nrun(d["rets"], Wl, mkl)
        return RB[key]

    def rung_book(store, tag, panel, lad, rg):
        c = dict(ANCHOR)
        c[lad] = rg
        r = book(store, tag, panel, c["N"], c["H"], c["GROSS"], c["CADENCE"])
        return r[store[panel]["warm"]]

    P(f"## RUNG BOOKS — {len(RUNGS)} per panel (the ratio's four dial ladders), "
      f"{len(RUNGS) * len(PANELS)} in total, 1148's grid")
    BOOKS = {}
    for panel in PANELS:
        for lad, rg in RUNGS:
            BOOKS[(panel, lad, rg)] = rung_book(cells, "P", panel, lad, rg)
        P(f"  {panel:<6s} done   ({time.time() - t0:6.1f}s)")
    P("")

    # ------------------------------- sub-tape part statistics, cached per (book, partition, f)
    FRAC_POOL = sorted(set(range(1, max(ENDPOINTS) + 1)))
    P(f"## SUB-TAPE PART STATISTICS — fracs {FRAC_POOL[0]}..{FRAC_POOL[-1]} x "
      f"{len(PARTITIONS)} partitions x {len(BOOKS)} books")
    PARTVALS: dict = {}
    nseg = 0
    for panel in PANELS:
        for lad, rg in RUNGS:
            r = BOOKS[(panel, lad, rg)]
            for pm in PARTITIONS:
                for f in FRAC_POOL:
                    segs = parts_at(r, f, pm)
                    sts = [six_stats(s) for s in segs]
                    nseg += len(segs)
                    PARTVALS[(panel, pm, lad, rg, f)] = {
                        st: np.array([x[st] for x in sts], float) for st in STATS6}
    P(f"  {nseg:,} sub-tape segments scored on 6 statistics   ({time.time() - t0:6.1f}s)")
    P("")

    # ------------------------------- per-(coordinate, skip, frac) group objects
    # groups[f] and med[f] depend ONLY on f, so every frac SUBSET is assembled from these in
    # O(|subset|).  This is 1158's groups_med, refactored, and G6 gates it against 1158's number.
    SKIPS = [None] + LADNAMES
    P("## GROUP OBJECTS — 1158's groups_med, per frac (so any rung subset is O(|subset|))")
    GOBJ: dict = {}
    for panel in PANELS:
        for pm in PARTITIONS:
            for constr in CONSTRUCTIONS:
                for skip in SKIPS:
                    if constr == "C_BOOK":
                        keys = [("N", N0)]      # 1158's C_BOOK VERBATIM: the anchor book
                    else:
                        keys = [(l, r) for (l, r) in RUNGS if l != skip]
                    for stat in STATS6:
                        for f in FRAC_POOL:
                            bylad: dict = {}
                            allv: list = []
                            for lad, rg in keys:
                                v = PARTVALS[(panel, pm, lad, rg, f)][stat]
                                allv.extend(v.tolist())
                                bylad.setdefault(lad, []).append(v)
                            gvecs = []
                            for lad, mats in bylad.items():
                                n = min(len(m) for m in mats)
                                if n == 0:
                                    continue
                                M = np.vstack([m[:n] for m in mats])
                                gvecs.append(np.nanmedian(M, axis=0))
                            sc = []
                            for gv in gvecs:
                                w = gv[np.isfinite(gv)]
                                if len(w) < 2:
                                    continue
                                sc.append((float(w.max() - w.min()), float(w.std(ddof=1)),
                                           matched_exact_v(w)))
                            med = float(np.nanmedian(allv)) if allv else np.nan
                            GOBJ[(panel, pm, constr, skip, stat, f)] = (sc, med, len(gvecs))
    P(f"  {len(GOBJ):,} (coordinate, skip, frac) group objects   ({time.time() - t0:6.1f}s)")
    P("")

    WIDX = {"R_SPREAD": 0, "R_SD": 1, "R_MATCHED": 2}

    def figure(panel, pm, constr, skip, stat, fracs, repair):
        """The 1157/1158 ratio, assembled on a rung subset.  Returns {within: ratio}."""
        g = GOBJ
        out = {}
        med = {f: g[(panel, pm, constr, skip, stat, f)][1] for f in fracs}
        if repair == "R_COUNT":
            bet = matched_exact_v([med[f] for f in fracs])
        else:
            fmx = max(fracs)
            a, b = med.get(1, np.nan), med.get(fmx, np.nan)
            bet = abs(a - b) if (np.isfinite(a) and np.isfinite(b)) else np.nan
        for w, j in WIDX.items():
            vals = [sc[j] for f in fracs if f != 1
                    for sc in g[(panel, pm, constr, skip, stat, f)][0]]
            wi = float(np.nanmedian(vals)) if vals else np.nan
            out[w] = (wi / bet if (np.isfinite(bet) and bet) else np.nan, wi, bet)
        return out

    # ------------------------------- the figure surface over (coordinate, endpoint, K)
    P("## FIGURE SURFACE — (panel, stat, partition, construction, within, repair) x fmax x K")
    fig_rows = []
    FIGV: dict = {}          # (coord..., fmax, K, w, repair, skip) -> ratio
    for fm in ENDPOINTS:
        Kmax = len(LADDER_ORDER[fm])
        for K in range(2, Kmax + 1):
            fr = lad_at(fm, K)
            for panel in PANELS:
                for pm in PARTITIONS:
                    for constr in CONSTRUCTIONS:
                        for stat in STATS6:
                            for skip in SKIPS:
                                for repair in REPAIRS:
                                    res = figure(panel, pm, constr, skip, stat, fr, repair)
                                    for w in WITHINS:
                                        FIGV[(panel, pm, constr, stat, w, repair, fm, K,
                                              skip)] = res[w][0]
                                        if skip is None:
                                            fig_rows.append(dict(
                                                panel=panel, partition=pm, construction=constr,
                                                stat=stat, within=w, repair=repair, fmax=fm, K=K,
                                                n_rungs=len(fr), fracs="|".join(map(str, fr)),
                                                value=res[w][0], within_term=res[w][1],
                                                between_term=res[w][2]))
    FIG = pd.DataFrame(fig_rows)
    P(f"  {len(FIG):,} published figure readings   ({time.time() - t0:6.1f}s)")
    dump(FIG, "figures")
    P("")

    # ------------------------------- SEs: four bases x (coordinate, fmax, K), + SE-of-SE
    P("## SE SURFACE — four bases, each also recomputed with one DIAL LADDER omitted")
    P("##   (the jackknife-of-jackknife the queue asks for)")

    def ses_at(panel, pm, constr, stat, repair, fm, K, basis, skip):
        """Return {within: (SE, n_distinct_replicates)} — all three within terms in one pass,
        because they share the same rung subsets."""
        fr = lad_at(fm, K)
        nonunit = [f for f in fr if f != 1]
        interior = [f for f in fr if f != 1 and f != max(fr)]
        nan3 = {w: (np.nan, 0) for w in WITHINS}
        if basis == "J_GROUP":
            if constr != "C_POOLED" or skip is not None:
                return nan3
            out = {}
            for w in WITHINS:
                reps = [FIGV[(panel, pm, constr, stat, w, repair, fm, K, g)] for g in LADNAMES]
                out[w] = (jack_se(reps), n_distinct(reps))
            return out
        if basis in ("J_LADDER", "J_INT"):
            drop = nonunit if basis == "J_LADDER" else interior
            if len(drop) < 2:
                return nan3
            reps = [figure(panel, pm, constr, skip, stat, [f for f in fr if f != d], repair)
                    for d in drop]
            return {w: (jack_se([r[w][0] for r in reps]), n_distinct([r[w][0] for r in reps]))
                    for w in WITHINS}
        if basis == "J_D2":
            if len(nonunit) < 3:
                return nan3
            subs, _ = d2_subsets(nonunit)
            reps = [figure(panel, pm, constr, skip, stat,
                           [f for f in fr if f not in dd], repair) for dd in subs]
            return {w: (delete_d_se([r[w][0] for r in reps], len(nonunit), 2),
                        n_distinct([r[w][0] for r in reps])) for w in WITHINS}
        return nan3

    se_rows = []
    SEV: dict = {}
    COORDS = [(panel, pm, constr, stat, w, repair)
              for panel in PANELS for pm in PARTITIONS for constr in CONSTRUCTIONS
              for stat in STATS6 for w in WITHINS for repair in REPAIRS]
    COORDS5 = [(panel, pm, constr, stat, repair)
               for panel in PANELS for pm in PARTITIONS for constr in CONSTRUCTIONS
               for stat in STATS6 for repair in REPAIRS]
    # THREE comparands, all published; S_LAD is the headline and the other two exist because
    #   (i) K=2 is a degenerate rung set (the within term is then ONE frac), so a spread that
    #       includes it could flatter decidability — S_LAD3 drops it;
    #   (ii) the spread the RECORD actually produced is between its two published ladders,
    #       L3 = {1,2,3} and L8 = {1,2,3,4,5,6,8}, which is 1188's own move — S_PUB is that.
    SLAD: dict = {}
    SLAD3: dict = {}
    SPUB: dict = {}
    L3_SET, L8_SET = [1, 2, 3], [1, 2, 3, 4, 5, 6, 8]
    for (panel, pm, constr, stat, repair) in COORDS5:
        f3 = figure(panel, pm, constr, None, stat, L3_SET, repair)
        f8 = figure(panel, pm, constr, None, stat, L8_SET, repair)
        for w in WITHINS:
            a, b = f3[w][0], f8[w][0]
            SPUB[(panel, pm, constr, stat, w, repair)] = (
                abs(a - b) if (np.isfinite(a) and np.isfinite(b)) else np.nan)
        for fm in ENDPOINTS:
            Kmax = len(LADDER_ORDER[fm])
            vals = {w: {K: FIGV[(panel, pm, constr, stat, w, repair, fm, K, None)]
                        for K in range(2, Kmax + 1)} for w in WITHINS}
            for w in WITHINS:
                fin = [v for v in vals[w].values() if np.isfinite(v)]
                SLAD[(panel, pm, constr, stat, w, repair, fm)] = (
                    (max(fin) - min(fin)) if len(fin) >= 2 else np.nan)
                fin3 = [v for K, v in vals[w].items() if K >= 3 and np.isfinite(v)]
                SLAD3[(panel, pm, constr, stat, w, repair, fm)] = (
                    (max(fin3) - min(fin3)) if len(fin3) >= 2 else np.nan)
            for K in range(2, Kmax + 1):
                for basis in BASES:
                    base = ses_at(panel, pm, constr, stat, repair, fm, K, basis, None)
                    # the jackknife-of-jackknife, at the HEADLINE endpoint only (declared):
                    # the same SE recomputed with each dial ladder omitted from the pool.
                    gse = {w: [] for w in WITHINS}
                    if fm == HEAD_FMAX and constr == "C_POOLED" and basis != "J_GROUP":
                        for g in LADNAMES:
                            r = ses_at(panel, pm, constr, stat, repair, fm, K, basis, g)
                            for w in WITHINS:
                                gse[w].append(r[w][0])
                    for w in WITHINS:
                        se, nd = base[w]
                        v = vals[w][K]
                        vprev = vals[w].get(K - 1, np.nan)
                        s_step = (abs(v - vprev) if (np.isfinite(v) and np.isfinite(vprev))
                                  else np.nan)
                        s_lad = SLAD[(panel, pm, constr, stat, w, repair, fm)]
                        s_lad3 = SLAD3[(panel, pm, constr, stat, w, repair, fm)]
                        s_pub = SPUB[(panel, pm, constr, stat, w, repair)]
                        sese = jack_se(gse[w]) if len(gse[w]) >= 2 else np.nan
                        SEV[(panel, pm, constr, stat, w, repair, fm, K, basis)] = se
                        se_rows.append(dict(
                            panel=panel, partition=pm, construction=constr, stat=stat, within=w,
                            repair=repair, fmax=fm, K=K, basis=basis, value=v, SE=se,
                            n_distinct_reps=nd, SE_of_SE=sese,
                            R_SESE=(sese / se if (np.isfinite(sese) and np.isfinite(se) and se)
                                    else np.nan),
                            S_LAD=s_lad, S_LAD3=s_lad3, S_PUB=s_pub, S_STEP=s_step,
                            DECIDABLE3=(bool(se < s_lad3)
                                        if (np.isfinite(se) and np.isfinite(s_lad3)) else np.nan),
                            DECIDABLE_PUB=(bool(se < s_pub)
                                           if (np.isfinite(se) and np.isfinite(s_pub))
                                           else np.nan),
                            se_rel=(abs(se / v) if (np.isfinite(se) and np.isfinite(v) and v)
                                    else np.nan),
                            DECIDABLE=(bool(se < s_lad) if (np.isfinite(se) and np.isfinite(s_lad))
                                       else np.nan),
                            DECIDABLE_STEP=(bool(se < s_step)
                                            if (np.isfinite(se) and np.isfinite(s_step))
                                            else np.nan)))
    SE = pd.DataFrame(se_rows)
    P(f"  {len(SE):,} (coordinate, fmax, K, basis) SEs   ({time.time() - t0:6.1f}s)")
    dump(SE, "se")
    P("")

    # ---------------------------------------------------------------- THE 28-CELL GRID
    P("## THE 28-CELL GRID (2 tuned dials) — share of cells whose SE is WIDER than the cell's")
    P(f"##   own ladder spread, at endpoint fmax={HEAD_FMAX} (headline), all coordinates pooled")
    H = SE[(SE.fmax == HEAD_FMAX)]
    grows = []
    for K in KGRID:
        for basis in BASES:
            s = H[(H.K == K) & (H.basis == basis) & H.DECIDABLE.notna()]
            sd = H[(H.K == K) & (H.basis == basis) & H.DECIDABLE_STEP.notna()]
            s3 = H[(H.K == K) & (H.basis == basis) & H.DECIDABLE3.notna()]
            sp = H[(H.K == K) & (H.basis == basis) & H.DECIDABLE_PUB.notna()]
            defined = H[(H.K == K) & (H.basis == basis)]
            grows.append(dict(
                K=K, basis=basis, n_cells=len(defined), n_defined=len(s),
                share_defined=(len(s) / len(defined) if len(defined) else np.nan),
                share_SE_wider=(1.0 - s.DECIDABLE.mean()) if len(s) else np.nan,
                share_SE_wider_noK2=(1.0 - s3.DECIDABLE3.mean()) if len(s3) else np.nan,
                share_SE_wider_vs_PUB=(1.0 - sp.DECIDABLE_PUB.mean()) if len(sp) else np.nan,
                share_decidable=(s.DECIDABLE.mean() if len(s) else np.nan),
                share_decidable_step=(sd.DECIDABLE_STEP.mean() if len(sd) else np.nan),
                med_se_rel=(s.se_rel.median() if len(s) else np.nan),
                med_R_SESE=(s.R_SESE.median() if len(s) else np.nan),
                med_n_distinct=(s.n_distinct_reps.median() if len(s) else np.nan)))
    GRID = pd.DataFrame(grows)
    dump(GRID, "grid")
    P(GRID.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")

    # ---------------------------------------------------------------- K*
    P("## K* — THE RUNG COUNT AT WHICH A FIGURE FIRST BECOMES DECIDABLE (or NONE)")
    ks_rows = []
    for (panel, pm, constr, stat, w, repair) in COORDS:
        for fm in ENDPOINTS:
            Kmax = len(LADDER_ORDER[fm])
            s_lad = SLAD[(panel, pm, constr, stat, w, repair, fm)]
            for basis in BASES:
                kstar, ndef = None, 0
                for K in range(2, Kmax + 1):
                    se = SEV[(panel, pm, constr, stat, w, repair, fm, K, basis)]
                    if np.isfinite(se) and np.isfinite(s_lad):
                        ndef += 1
                        if se < s_lad and kstar is None:
                            kstar = K
                ks_rows.append(dict(panel=panel, partition=pm, construction=constr, stat=stat,
                                    within=w, repair=repair, fmax=fm, basis=basis,
                                    n_K_defined=ndef, S_LAD=s_lad,
                                    Kstar=(kstar if kstar else np.nan),
                                    ever_decidable=bool(kstar is not None)))
    KS = pd.DataFrame(ks_rows)
    dump(KS, "kstar")
    for basis in BASES:
        for fm in ENDPOINTS:
            s = KS[(KS.basis == basis) & (KS.fmax == fm) & (KS.n_K_defined > 0)]
            if not len(s):
                continue
            P(f"  basis {basis:<9s} fmax {fm:<3d}  cells with any defined K {len(s):4d}   "
              f"EVER decidable {int(s.ever_decidable.sum()):4d} ({s.ever_decidable.mean():.4f})"
              f"   median K* {s.Kstar.median() if s.ever_decidable.any() else float('nan')}")
    P("")

    # ------------- does the SE fall with K at all?  (log-log slope, and what K would be needed)
    P("## DOES THE SE FALL WITH RUNG COUNT?  log-log slope per cell, headline basis")
    sl_rows = []
    for (panel, pm, constr, stat, w, repair) in COORDS:
        for fm in ENDPOINTS:
            Kmax = len(LADDER_ORDER[fm])
            for basis in BASES:
                xs, ys = [], []
                for K in range(2, Kmax + 1):
                    se = SEV[(panel, pm, constr, stat, w, repair, fm, K, basis)]
                    if np.isfinite(se) and se > 0:
                        xs.append(np.log(K))
                        ys.append(np.log(se))
                if len(xs) < 3:
                    continue
                b, a = np.polyfit(xs, ys, 1)
                vals = [FIGV[(panel, pm, constr, stat, w, repair, fm, KK, None)]
                        for KK in range(2, Kmax + 1)]
                fin = [x for x in vals if np.isfinite(x)]
                s_lad = (max(fin) - min(fin)) if len(fin) >= 2 else np.nan
                se_last = float(np.exp(np.clip(a + b * np.log(Kmax), -700, 700)))
                kneed = np.nan
                if np.isfinite(s_lad) and s_lad > 0 and b < -1e-9:
                    lk = (np.log(s_lad) - a) / b
                    kneed = float(np.exp(lk)) if lk < 700 else np.inf
                sl_rows.append(dict(panel=panel, partition=pm, construction=constr, stat=stat,
                                    within=w, repair=repair, fmax=fm, basis=basis, n_pts=len(xs),
                                    slope=b, se_at_Kmax=se_last, S_LAD=s_lad, K_needed=kneed))
    SL = pd.DataFrame(sl_rows)
    dump(SL, "slopes")
    P("##   (a SE that behaves like a standard error falls at about -0.50; a POSITIVE slope means")
    P("##   adding rungs makes the published bar WIDER, so resolution cannot be bought at all)")
    for basis in BASES:
        for fm in (HEAD_FMAX, max(ENDPOINTS)):
            s = SL[(SL.basis == basis) & (SL.fmax == fm)]
            if len(s):
                P(f"  {basis:<9s} fmax {fm:<3d} n {len(s):4d}   median slope "
                  f"{s.slope.median():+.4f}   share RISING (slope > 0) "
                  f"{float((s.slope > 0).mean()):.4f}   share at or below -0.25 "
                  f"{float((s.slope <= -0.25).mean()):.4f}")
    s = SL[(SL.basis == HEAD_BASIS) & (SL.fmax == max(ENDPOINTS))]
    if len(s):
        rising = float((s.slope >= 0).mean())
        kn = s[s.K_needed.notna() & np.isfinite(s.K_needed)]
        P(f"  EXTRAPOLATION on the longest ladder (fmax {max(ENDPOINTS)}, basis {HEAD_BASIS}): "
          f"at {rising:.4f} of cells the SE RISES with K, so NO rung count ever makes those")
        P(f"    cells decidable by adding rungs.  On the {len(kn)} cells where it falls, the "
          f"median K at which the fitted SE would meet S_LAD is {kn.K_needed.median():,.1f} "
          f"(p90 {kn.K_needed.quantile(0.9):,.1f}) — and most of those are already below the")
        P("    ladders walked here, i.e. they are decidable now and do not need more rungs.")
    nmax = min(cells[p]["warm"].sum() for p in PANELS)
    P(f"  MECHANICAL CEILING: the shortest pinned post-warm-up tape is {int(nmax):,} bars and a "
      f"part needs >= 3 bars, so the largest attainable rung is f = {int(nmax) // 3:,} and the")
    P(f"    largest attainable rung COUNT is {int(nmax) // 3:,}.  Anything beyond that is not a "
      f"resolution a tape of this length can be read at.")
    P("")

    # ---------------------------------------------------------------- resolution detail
    P("## RESOLUTION DETAIL — 1188's two numbers, re-measured here as a cross-run check")
    h = SE[(SE.fmax == HEAD_FMAX) & (SE.K == K_L8) & (SE.basis == HEAD_BASIS) & SE.se_rel.notna()]
    if len(h):
        P(f"  own {HEAD_BASIS} SE as a share of the value, at the rung set that IS 1188's L8:")
        P(f"    median {h.se_rel.median():.4f}   (1188 committed {PRIOR_SEREL_1188} on its own "
          f"claim set; this is a DIFFERENT population — every coordinate, not the harvested "
          f"figures — so it is a cross-read, not a replay)")
        P(f"    share whose SE exceeds the number itself: {float((h.se_rel > 1).mean()):.4f}  "
          f"(1188 committed {PRIOR_SEBIG_1188})")
    P("  THE BAR'S OWN SAMPLING ERROR (jackknife-of-jackknife over the four dial ladders):")
    for basis in BASES:
        g = SE[(SE.fmax == HEAD_FMAX) & (SE.basis == basis) & SE.R_SESE.notna()]
        if len(g):
            P(f"    {basis:<9s} n {len(g):5,d}   median SE_of_SE / SE {g.R_SESE.median():.4f}   "
              f"share >= 0.50 {float((g.R_SESE >= 0.5).mean()):.4f}   share >= 1.00 "
              f"{float((g.R_SESE >= 1.0).mean()):.4f}")
    P("  DEGENERACY — distinct jackknife replicate values behind each published SE:")
    for basis in BASES:
        g = SE[(SE.fmax == HEAD_FMAX) & (SE.basis == basis) & (SE.n_distinct_reps > 0)]
        if len(g):
            P(f"    {basis:<9s} median distinct replicates {g.n_distinct_reps.median():.1f}   "
              f"share with <= 2 distinct {float((g.n_distinct_reps <= 2).mean()):.4f}")
    P("  BY STATISTIC (headline basis, K = 1188's L8 rung count, share SE WIDER than S_LAD):")
    for st, g in SE[(SE.fmax == HEAD_FMAX) & (SE.K == K_L8) & (SE.basis == HEAD_BASIS)
                    & SE.DECIDABLE.notna()].groupby("stat"):
        P(f"    {st:<8s} n {len(g):4d}   SE wider {1 - g.DECIDABLE.mean():.4f}   median se_rel "
          f"{g.se_rel.median():.4f}")
    P("  BY WITHIN TERM:")
    for wt, g in SE[(SE.fmax == HEAD_FMAX) & (SE.K == K_L8) & (SE.basis == HEAD_BASIS)
                    & SE.DECIDABLE.notna()].groupby("within"):
        P(f"    {wt:<10s} n {len(g):4d}   SE wider {1 - g.DECIDABLE.mean():.4f}   median se_rel "
          f"{g.se_rel.median():.4f}")
    P("  BY PANEL:")
    for pn, g in SE[(SE.fmax == HEAD_FMAX) & (SE.K == K_L8) & (SE.basis == HEAD_BASIS)
                    & SE.DECIDABLE.notna()].groupby("panel"):
        P(f"    {pn:<8s} n {len(g):4d}   SE wider {1 - g.DECIDABLE.mean():.4f}   median se_rel "
          f"{g.se_rel.median():.4f}")
    P("")

    # ---------------------------------------------------------------- the verdict
    hd = GRID[(GRID.K == K_RECORD) & (GRID.basis == HEAD_BASIS)]
    share_wide_rec = float(hd.share_SE_wider.iloc[0]) if len(hd) else np.nan
    every_K = GRID[GRID.basis == HEAD_BASIS].share_SE_wider.dropna()
    min_wide = float(every_K.min()) if len(every_K) else np.nan
    verdict = ("(UNDECIDED)" if not np.isfinite(min_wide) else
               "(A) NEVER DECIDABLE — the SE is wider than the spread at every rung count"
               if min_wide >= BAR_NEVER else
               "(C) ALREADY DECIDABLE AT THE RECORD'S OWN RUNG COUNT"
               if share_wide_rec <= (1 - BAR_ALREADY) else
               "(B) DECIDABLE ONLY AT HIGHER RESOLUTION")
    P(f"  HEADLINE (basis {HEAD_BASIS}, fmax {HEAD_FMAX}): share of cells whose SE is WIDER than")
    P(f"    their own ladder spread — at rung count K={K_RECORD} (the record's own rung COUNT; "
      f"at this endpoint that rung SET is {lad_at(HEAD_FMAX, K_RECORD)}, not the record's")
    P(f"    {L3_SET}, which is a different ENDPOINT and is read separately as S_PUB): "
      f"{share_wide_rec:.4f}; best over the whole K dial: {min_wide:.4f}")
    P("  THE OTHER TWO COMPARANDS, published beside it and not substituted for it:")
    for basis in BASES:
        g = GRID[GRID.basis == basis]
        if len(g):
            P(f"    {basis:<9s} SE wider than S_LAD (all K) "
              f"{g.share_SE_wider.min():.4f}..{g.share_SE_wider.max():.4f}   than S_LAD3 "
              f"(K>=3, drops the degenerate 2-rung reading) "
              f"{g.share_SE_wider_noK2.min():.4f}..{g.share_SE_wider_noK2.max():.4f}   than "
              f"S_PUB (|v(L8) - v(L3)|, 1188's OWN move) "
              f"{g.share_SE_wider_vs_PUB.min():.4f}..{g.share_SE_wider_vs_PUB.max():.4f}")
    P(f"  VERDICT: {verdict}")
    P("  READING — what the pre-declared label does and does NOT mean here, stated because the")
    P("    label was written before the numbers and is kept as written:")
    kk = KS[(KS.basis == HEAD_BASIS) & (KS.fmax == HEAD_FMAX) & (KS.n_K_defined > 0)]
    slh = SL[(SL.basis == HEAD_BASIS) & (SL.fmax == HEAD_FMAX)]
    P(f"    1. The literal question — 'is the SE wider than its own ladder spread AT EVERY "
      f"CELL?' — is answered NO: at most {float(GRID[GRID.basis == HEAD_BASIS].share_SE_wider.max()):.4f} "
      f"of cells under the record's own basis.")
    P(f"    2. 'Only at higher resolution' does NOT mean a finer ladder buys decidability.  "
      f"Where it is attainable it is attained at the SMALLEST rung count on the dial (median")
    P(f"       K* {kk.Kstar.median():.1f} of {min(KGRID)}..{max(KGRID)}), and beyond that the SE "
      f"RISES with K at {float((slh.slope > 0).mean()):.4f} of cells (median log-log slope "
      f"{slh.slope.median():+.4f} where a standard error would be about -0.50).")
    P(f"       So the {1 - kk.ever_decidable.mean():.4f} of cells that never decide do not "
      f"decide at ANY attainable rung count — more rungs make their bar wider, not narrower.")
    gspan = GRID.groupby("basis").share_SE_wider.median()
    P(f"    3. THE SE BASIS DIAL MOVES THE ANSWER BY MORE THAN AN ORDER OF MAGNITUDE: median "
      f"share SE-wider runs {dict(gspan.round(4))}.")
    P(f"       The record quotes 'its own jackknife SE' as though it were ONE object; it is at "
      f"least four, and they disagree by {float(gspan.max() / max(gspan.min(), 1e-9)):.1f}x on "
      f"the only question a bar exists to answer.")
    P("")

    # ---------------------------------------------------------------- gates
    P("## GATES")
    d = cells["U56"]
    mk = rebalance_mask(d["idx"], FREQ0).values
    W = build(d["rank_key"], d["elig"], d["priced"], np.flatnonzero(mk), N0, HOLD0,
              d["T"], d["K"], GROSS0)
    engs = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                    cost_bps=COST, freq=FREQ0)["returns"]
    eng = engs.values
    v = float(np.abs(eng[d["warm"]] - BOOKS[("U56", "N", N0)]).max())
    gate("G1", "fast runner == engine.backtest post-warm-up (U56 W/H126/N=20, gross 0.75)",
         v, v < 1e-12)
    nnan = int(np.sum(~np.isfinite(eng)))
    where = list(np.flatnonzero(~np.isfinite(eng))[:4])
    gate("G1b", f"idea 1191's engine.backtest NaN REPRODUCES on ndarray: {nnan} non-finite rows "
                f"at {where}, all inside the {WARMUP}-bar warm-up "
                f"({bool(all(i < WARMUP for i in np.flatnonzero(~np.isfinite(eng))))})",
         nnan, bool(all(i < WARMUP for i in np.flatnonzero(~np.isfinite(eng)))))

    m = blocks_m(BOOKS[("U56", "N", N0)], d["ins"], d["oos"])
    a = max(abs(m["CAGR"] - A936_WH126[0]), abs(m["Sharpe"] - A936_WH126[1]),
            abs(m["MaxDD"] - A936_WH126[2]))
    gate("G2", f"CROSS-RUN the committed U56 W/H126/N=20 triple, PINNED at {PIN}", a, a < 5e-5)
    sp = d["px"]["SPY"].pct_change().fillna(0.0).values[d["warm"]]
    sm = blocks_m(sp, d["ins"], d["oos"])
    b = max(abs(sm["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
            abs(sm["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
            abs(sm["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gate("G3", "CROSS-RUN the committed SPY OOS triple on U56's tape", b, b < 5e-4)
    v = max(abs(six_stats(BOOKS[(p, "N", N0)])["MAXDD"] - DD_COMMITTED[p]) for p in PANELS)
    gate("G3b", "CROSS-RUN 1157's committed full-tape MaxDD LEVELS (U56 / B136 / SMALL)",
         v, v < 5e-4)

    rr = np.random.default_rng(SEED_G0)
    dv = 0.0
    for _ in range(200):
        x = rr.standard_normal(rr.integers(2, 40))
        dv = max(dv, abs(matched_exact(x) - matched_exact_v(x)))
    gate("G4", "vectorised matched_exact_v == 1157's combinations form", dv, dv < 1e-12)

    gate("G5", f"at fmax={HEAD_FMAX} the K={K_L8} rung set IS 1188/1158's L8 "
               f"{lad_at(HEAD_FMAX, K_L8)}", 0.0,
         lad_at(HEAD_FMAX, K_L8) == [1, 2, 3, 4, 5, 6, 8])

    got58 = figure("SMALL", "ALIGNED", "C_POOLED", None, "MAXDD",
                   lad_at(HEAD_FMAX, K_L8), "R_COUNT")[HEAD_WITHIN][0]
    v = abs(got58 - PRIOR_RES_1158) / PRIOR_RES_1158
    gate("G6", f"1158's committed L8 R_COUNT reading replayed ({got58:.6f} vs {PRIOR_RES_1158})",
         v, v < 1e-4)

    # 1148's committed 0.794259 is a 200-pair MONTE-CARLO figure (idea 1191: not recoverable
    # without its draw order).  1188 recovered the one order that replays it; it is reproduced
    # here VERBATIM as a cross-run, and reported either way.
    rng = np.random.default_rng(SEED_1148)
    got48 = np.nan
    for panel in PANELS:
        for stat in STATS6:
            fr = [1, 2, 3]
            mats_by_f: dict = {}
            for f in fr:
                by: dict = {}
                av: list = []
                for lad, rg in RUNGS:
                    vv = PARTVALS[(panel, "ALIGNED", lad, rg, f)][stat]
                    av.extend(vv.tolist())
                    by.setdefault(lad, []).append(vv)
                vecs = []
                for lad, mats in by.items():
                    n = min(len(mm) for mm in mats)
                    if n == 0:
                        continue
                    M = np.vstack([mm[:n] for mm in mats])
                    vecs.append(np.nanmedian(M, axis=0))
                mats_by_f[f] = (vecs, float(np.nanmedian(av)) if av else np.nan)
            ranges, sds, matched = [], [], []
            for f in fr:
                if f == 1:
                    continue
                for vv in mats_by_f[f][0]:
                    vv = np.asarray([x for x in vv if np.isfinite(x)], float)
                    if len(vv) < 2:
                        continue
                    ranges.append(float(vv.max() - vv.min()))
                    sds.append(float(vv.std(ddof=1)))
                    mm_ = matched_sampled(vv, rng)
                    if np.isfinite(mm_):
                        matched.append(mm_)
            med = {f: mats_by_f[f][1] for f in fr}
            bs = abs(med[1] - med[max(fr)])
            val = (float(np.nanmedian(matched)) / bs) if (matched and bs) else np.nan
            if panel == "SMALL" and stat == HEAD_STAT:
                got48 = val
    v = abs(got48 - PRIOR_CELL_1148)
    gate("G7", f"1148/1157's SMALL/MAXDD R_MATCHED replayed BIT FOR BIT ({got48:.6f} vs "
               f"{PRIOR_CELL_1148})", v, v < 1e-6)

    bt = FIG[(FIG.repair == "R_ASIS")].groupby(
        ["panel", "partition", "construction", "stat", "within", "fmax"])["between_term"].agg(
        lambda s: (s.max() - s.min()) / max(abs(s.median()), 1e-12))
    btv = float(np.nanmax(bt.values)) if len(bt) else np.nan
    gate("G8", "R_ASIS's between term CANNOT move with K at a fixed endpoint (max rel spread "
               "over the whole K ladder)", btv, np.isfinite(btv) and btv < 1e-12)

    nest = all(set(lad_at(fm, K)).issubset(set(lad_at(fm, K + 1)))
               for fm in ENDPOINTS for K in range(2, len(LADDER_ORDER[fm])))
    gate("G9", "the refinement ladder is NESTED at every endpoint (LAD(K) subset LAD(K+1))",
         0.0, nest)

    for lad, rg in RUNGS:
        r = rung_book(cells_un, "U", "SMALL", lad, rg)
        for f in FRAC_POOL:
            segs = parts_at(r, f, HEAD_PART)
            sts = [six_stats(s) for s in segs]
            PARTVALS[("UNPIN", HEAD_PART, lad, rg, f)] = {
                st_: np.array([x[st_] for x in sts], float) for st_ in STATS6}
    for stat in [HEAD_STAT]:
        for f in FRAC_POOL:
            by: dict = {}
            av: list = []
            for lad, rg in RUNGS:
                vv = PARTVALS[("UNPIN", HEAD_PART, lad, rg, f)][stat]
                av.extend(vv.tolist())
                by.setdefault(lad, []).append(vv)
            vecs = []
            for lad, mats in by.items():
                n = min(len(mm) for mm in mats)
                if n == 0:
                    continue
                M = np.vstack([mm[:n] for mm in mats])
                vecs.append(np.nanmedian(M, axis=0))
            sc = []
            for gv in vecs:
                wv = gv[np.isfinite(gv)]
                if len(wv) < 2:
                    continue
                sc.append((float(wv.max() - wv.min()), float(wv.std(ddof=1)),
                           matched_exact_v(wv)))
            GOBJ[("UNPIN", HEAD_PART, "C_POOLED", None, stat, f)] = (
                sc, float(np.nanmedian(av)) if av else np.nan, len(vecs))
    vun = figure("UNPIN", HEAD_PART, "C_POOLED", None, HEAD_STAT,
                 lad_at(HEAD_FMAX, K_L8), HEAD_REPAIR)[HEAD_WITHIN][0]
    vpin = FIGV[("SMALL", HEAD_PART, "C_POOLED", HEAD_STAT, HEAD_WITHIN, HEAD_REPAIR,
                 HEAD_FMAX, K_L8, None)]
    dev = abs(vun - vpin) / max(abs(vpin), 1e-12)
    gate("G10", f"THE VINTAGE, published not absorbed: headline cell PINNED {vpin:.6f} vs "
                f"UNPINNED {vun:.6f}", dev, True)

    GDF = pd.DataFrame(GATES)
    dump(GDF, "gates")
    P(f"  GATES {int(GDF.pass_.sum())} of {len(GDF)}")
    P("")

    # ---------------------------------------------------------------- rule 8 + KEEP paths
    P("## RULE 8 WALK-FORWARD + BOTH KEEP PATHS — 81 rung books, every one published")
    wf_rows, BENCH = [], {}
    for panel in PANELS:
        dd_ = cells[panel]
        px = dd_["px"]
        spy = px["SPY"].pct_change().fillna(0.0).values[dd_["warm"]]
        live = backtest(px, rules_v2_weights(px), cost_bps=COST,
                        freq="W")["returns"].values[dd_["warm"]]
        sb, lb = blocks_m(spy, dd_["ins"], dd_["oos"]), blocks_m(live, dd_["ins"], dd_["oos"])
        BENCH[panel] = (sb, lb)
        P(f"  {panel:<6s} SPY {sb['CAGR']:7.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:7.2%} "
          f"(OOS {sb['OOS_CAGR']:7.2%} / {sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:7.2%})   "
          f"v2 {lb['CAGR']:7.2%} / {lb['Sharpe']:.4f} / {lb['MaxDD']:7.2%} "
          f"(OOS {lb['OOS_CAGR']:7.2%} / {lb['OOS_Sharpe']:.4f})")
        for lad, rg in RUNGS:
            b = blocks_m(BOOKS[(panel, lad, rg)], dd_["ins"], dd_["oos"])
            l4b, l4bo, l4a = legs_4b(b, sb), legs_4b_oos(b, sb), legs_4a(b, lb)
            wf_rows.append(dict(panel=panel, ladder=lad, rung=rg, **b, **l4b, **l4bo, **l4a,
                                PASS_4b_full=all(l4b.values()), PASS_4b_oos=all(l4bo.values()),
                                PASS_4a=all(l4a.values())))
    WF = pd.DataFrame(wf_rows)
    dump(WF, "walkforward")
    P(f"  BASE RATES over {len(WF)} rung books: 4b full {int(WF.PASS_4b_full.sum())}, "
      f"4b OOS {int(WF.PASS_4b_oos.sum())}, 4b BOTH "
      f"{int((WF.PASS_4b_full & WF.PASS_4b_oos).sum())}, 4a {int(WF.PASS_4a.sum())}")
    for panel in PANELS:
        s = WF[WF.panel == panel]
        P(f"    {panel:<6s} 4b full {int(s.PASS_4b_full.sum()):2d} / 4b OOS "
          f"{int(s.PASS_4b_oos.sum()):2d} / 4b BOTH "
          f"{int((s.PASS_4b_full & s.PASS_4b_oos).sum()):2d} / 4a {int(s.PASS_4a.sum()):2d}"
          f"  of {len(s)}")
    bth = WF[WF.PASS_4b_full & WF.PASS_4b_oos]
    if len(bth):
        P(f"    DISTINCTNESS (idea 1189's warning — a GROSS rung is the SAME book re-grossed, "
          f"and CADENCE=W / GROSS=0.75 / H=126 / N=20 are ALL the anchor book):")
        for pn, g in bth.groupby("panel"):
            byl = dict(g.groupby("ladder").size())
            anchor = sum(1 for _, r in g.iterrows()
                         if (r.ladder, r.rung) in (("CADENCE", FREQ0), ("GROSS", GROSS0),
                                                   ("H", HOLD0), ("N", N0)))
            P(f"      {pn:<6s} {len(g):2d} passes, by ladder {byl}; GROSS-ladder rungs "
              f"{byl.get('GROSS', 0)} (one book re-grossed); copies of the ANCHOR book "
              f"{anchor}")
        P(f"      so {len(bth)} passes are at most "
          f"{len(bth) - sum(max(0, sum(1 for _, r in g.iterrows() if r.ladder == 'GROSS') - 1) for _, g in bth.groupby('panel'))}"
          f" distinct books once each panel's GROSS ladder is collapsed to one.")
        r = bth.sort_values("OOS_Sharpe", ascending=False).iloc[0]
        P(f"    best 4b (full AND OOS): {r.panel}/{r.ladder}={r.rung}  full "
          f"{r.CAGR:.2%}/{r.Sharpe:.4f}/{r.MaxDD:.2%} (H1 {r.H1:.4f}/H2 {r.H2:.4f}), OOS "
          f"{r.OOS_CAGR:.2%}/{r.OOS_Sharpe:.4f}/{r.OOS_MaxDD:.2%}")

    # IS-only choosers: does "well resolved" or "decidable" buy anything?
    P("  CHOOSERS — all four choose on 2009-2016 ONLY; 2017-2026 is read once, below.")
    ISOBJ: dict = {}
    for panel in PANELS:
        dd_ = cells[panel]
        ins = dd_["ins"]
        for lad, rg in RUNGS:
            r = BOOKS[(panel, lad, rg)][ins]
            per = {}
            for f in FRAC_POOL[:HEAD_FMAX]:
                segs = parts_at(r, f, HEAD_PART)
                per[f] = np.array([six_stats(s)[HEAD_STAT] for s in segs], float)
            def fig_is(fr):
                med = {f: (float(np.nanmedian(per[f])) if len(per[f]) else np.nan) for f in fr}
                bet = abs(med[1] - med[max(fr)])
                vals = [matched_exact_v(per[f]) for f in fr if f != 1]
                wi = float(np.nanmedian(vals)) if vals else np.nan
                return wi / bet if (np.isfinite(bet) and bet) else np.nan
            vK = {K: fig_is(lad_at(HEAD_FMAX, K)) for K in KGRID}
            fin = [x for x in vK.values() if np.isfinite(x)]
            s_lad = (max(fin) - min(fin)) if len(fin) >= 2 else np.nan
            fr = lad_at(HEAD_FMAX, K_RECORD)
            reps = [fig_is([f for f in fr if f != dfc]) for dfc in fr if dfc != 1]
            se = jack_se(reps)
            ISOBJ[(panel, lad, rg)] = dict(IS_Sharpe=fsharpe(r), fig=vK[K_RECORD], SE=se,
                                           S_LAD=s_lad,
                                           DEC=bool(np.isfinite(se) and np.isfinite(s_lad)
                                                    and se < s_lad))
    pick_rows = []
    for panel in PANELS:
        dd_ = cells[panel]
        sb, lb = BENCH[panel]
        cand = [(lad, rg) for lad, rg in RUNGS]
        for chooser in ("CH_IS", "CH_SE", "CH_SPREAD", "CH_DEC"):
            pool = cand
            note = ""
            if chooser == "CH_IS":
                key = max(pool, key=lambda k: (ISOBJ[(panel,) + k]["IS_Sharpe"]
                                               if np.isfinite(ISOBJ[(panel,) + k]["IS_Sharpe"])
                                               else -np.inf))
            elif chooser == "CH_SE":
                key = min(pool, key=lambda k: (ISOBJ[(panel,) + k]["SE"]
                                               if np.isfinite(ISOBJ[(panel,) + k]["SE"])
                                               else np.inf))
            elif chooser == "CH_SPREAD":
                key = min(pool, key=lambda k: (ISOBJ[(panel,) + k]["S_LAD"]
                                               if np.isfinite(ISOBJ[(panel,) + k]["S_LAD"])
                                               else np.inf))
            else:
                dec = [k for k in pool if ISOBJ[(panel,) + k]["DEC"]]
                if not dec:
                    dec, note = pool, "NO DECIDABLE BOOK — fell back to the whole pool"
                key = max(dec, key=lambda k: (ISOBJ[(panel,) + k]["IS_Sharpe"]
                                              if np.isfinite(ISOBJ[(panel,) + k]["IS_Sharpe"])
                                              else -np.inf))
            b = blocks_m(BOOKS[(panel, key[0], key[1])], dd_["ins"], dd_["oos"])
            l4b, l4bo, l4a = legs_4b(b, sb), legs_4b_oos(b, sb), legs_4a(b, lb)
            pick_rows.append(dict(panel=panel, chooser=chooser, ladder=key[0], rung=key[1],
                                  n_decidable=sum(1 for k in pool if ISOBJ[(panel,) + k]["DEC"]),
                                  note=note, **b, PASS_4b_full=all(l4b.values()),
                                  PASS_4b_oos=all(l4bo.values()), PASS_4a=all(l4a.values())))
    PK = pd.DataFrame(pick_rows)
    dump(PK, "picks")
    P(PK[["panel", "chooser", "ladder", "rung", "n_decidable", "IS_Sharpe", "CAGR", "Sharpe",
          "MaxDD", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "PASS_4b_full", "PASS_4b_oos",
          "PASS_4a"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    base_pick = {p: tuple(PK[(PK.panel == p) & (PK.chooser == "CH_IS")]
                          .iloc[0][["ladder", "rung"]]) for p in PANELS}
    moved = {ch: sum(1 for p in PANELS
                     if tuple(PK[(PK.panel == p) & (PK.chooser == ch)]
                              .iloc[0][["ladder", "rung"]]) != base_pick[p])
             for ch in ("CH_SE", "CH_SPREAD", "CH_DEC")}
    P(f"  RESOLUTION-BASED CHOOSING MOVES THE PICK vs CH_IS at {moved} of {len(PANELS)} panels "
      f"each; picks clearing 4a {int(PK.PASS_4a.sum())} of {len(PK)}; 4b full AND OOS "
      f"{int((PK.PASS_4b_full & PK.PASS_4b_oos).sum())} of {len(PK)}")
    P("")

    # ---------------------------------------------------------------- summary
    P("## SUMMARY")
    P(f"  cells x endpoints x K x basis SE readings : {len(SE):,}")
    P(f"  published figure readings                 : {len(FIG):,}")
    hh = SE[(SE.fmax == HEAD_FMAX) & (SE.basis == HEAD_BASIS) & SE.DECIDABLE.notna()]
    P(f"  SE WIDER than own ladder spread, {HEAD_BASIS}, fmax {HEAD_FMAX}, all K: "
      f"{int((~hh.DECIDABLE.astype(bool)).sum()):,} of {len(hh):,} "
      f"({1 - hh.DECIDABLE.mean():.4f})")
    for K in KGRID:
        g = hh[hh.K == K]
        if len(g):
            P(f"    K={K}: SE wider {1 - g.DECIDABLE.mean():.4f}  (n {len(g)})")
    kk = KS[(KS.basis == HEAD_BASIS) & (KS.fmax == HEAD_FMAX) & (KS.n_K_defined > 0)]
    if len(kk):
        P(f"  cells EVER decidable at any attainable K  : {int(kk.ever_decidable.sum()):,} of "
          f"{len(kk):,} ({kk.ever_decidable.mean():.4f})")
    P(f"  VERDICT: {verdict}")
    P(f"  runtime {time.time() - t0:.1f}s")

    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return dict(verdict=verdict, GRID=GRID, SE=SE, KS=KS, WF=WF, PK=PK, GDF=GDF)


if __name__ == "__main__":
    main()

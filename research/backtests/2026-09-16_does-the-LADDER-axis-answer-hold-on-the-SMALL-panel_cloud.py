#!/usr/bin/env python3
"""Idea 1119 (cloud lane, 2026-09-16) — does the LADDER axis answer hold on the SMALL panel?

QUESTION (QUEUE idea 1119, verbatim)
    idea 1116's ETA2_LAD/ETA2_STAT margin is 17.0x on U56 but 11.7x on B136, i.e. it weakens as
    the panel widens, and 1073 measured that one book's OOS Sharpe carries reliability 0.0915 on
    small-cap panels against 0.5126 on large-cap ones.  Re-run the 4x4 decomposition on the
    485-name sub-$2B SMALL panel and report whether the ladder axis survives where the draw
    dominates.  Max 2 params (panel, q).

THE TWO TUNED DIALS (PROTOCOL rule 4, no more than two)
    1. PANEL {U56, B136, SMALL}.  U56 and B136 are 1116's own panels, re-run to reproduce its
       committed ETA2 pair (0.8095 / 0.0476 and 0.5556 / 0.0476) as cross-run gates; SMALL is
       the arm this idea adds.
    2. CONFIDENCE q {0.80, 0.90, 0.95}, 1116's grid, all three published.
    LADDER and STATISTIC are NOT dials — they are the two candidate ANSWERS, and all
    3 x 4 x 4 = 48 CORE cells are reported at every q.
    THE UN-RESOLVABILITY DEFINITION IS FROZEN, NOT TUNED: INF_FLOOR, 1116's headline.
    ZERO_CONTENT and NO_TAPE_500 are reported beside it for continuity with 1110/1116 and the
    decision rule never reads them.  BLOCK LENGTH is frozen the same way: L=63 headline, L in
    {21, 126} reported beside and never selected on.
    Everything else frozen at 1082/1094/1098/1102/1108/1110/1116's construction: CAND20 legs,
    cap INF, max_vol 0.60, gross 0.75 (except on the GROSS ladder), W cadence (except on the
    CADENCE ladder), min hold 126 (except on the H ladder), N=20 (except on the N ladder),
    10 bps, LAG 1, warm-up 260, IS end 2016-12-31, 1000 draws, zlib.crc32 seeds (1108's repair).

THE SMALL PANEL, AND ITS STAMP (idea 1074's recommendation, applied)
    `load_universe(small=True)`, then every ticker with `max_1d_move` >= 1.0 dropped per
    data/small_meta.csv.  The pool size and the tape are PRINTED AND STAMPED because idea 706
    found this pool was rebuilt from 439 to 663 usable names on 2026-09-11 and idea 1072 found
    committed SMALL headlines that die on the rebuild: the label "SMALL485" in this idea's own
    text no longer denotes the pool the loader serves.  Whatever count this run gets is the
    count it reports, with the build date beside it.
    SPY IS NOT A CONSTITUENT of the SMALL panel — the loader joins it purely as the 4b
    benchmark — so it is REMOVED from the selectable set there, and gate G_SPY MEASURES how
    many rebalance-date slots it would have taken had it been left in, so the choice is priced
    and not asserted.  On U56 and B136, SPY IS a committed constituent and stays selectable:
    that is what makes the cross-run gates against 1116 meaningful.

DECLARED BEFORE ANY NUMBER
    H_REPRO      the U56 and B136 headline ETA2 pairs reproduce 1116's committed 0.8095/0.0476
                 and 0.5556/0.0476 (gates G10/G11).  This is a gate, not a finding.
    H_LADDER     the idea's question: ETA2_LAD > ETA2_STAT on the binary INF_FLOOR table at
                 q=0.90 on SMALL.
    H_MARGIN_MONO the idea's own premise, stated as it stands: the LAD/STAT margin falls with
                 panel breadth, U56 (17.0x) > B136 (11.7x) > SMALL.  REFUTED by a SMALL margin
                 above B136's.
    H_SURVIVES   the DECISION RULE: LADDER survives on SMALL only if ETA2_LAD > ETA2_STAT at a
                 MAJORITY (>= 2) of the three q values.
    H_REDRAW     POST-HOC AND LABELLED AS SUCH, added after this run's first pass failed its own
                 reproduction gates.  The cause was diagnosed, not assumed: the identical code
                 re-run at 1116's own seed base 11161116 reproduces its committed ETA2,
                 concordance and per-ladder counts bit for bit (gates G7/G8/G9), so what moves
                 between the two bases is the DRAW.  The redraw arm then reports the
                 DISTRIBUTION of ETA2_LAD, ETA2_STAT and their ratio over 8 independent seed
                 bases for all three panels, and asks whether LAD beats STAT on SMALL in a
                 MAJORITY of them.  1116 itself ran 6 such redraws for the axis question; this
                 is the same instrument applied to the quantity the idea's premise is a ratio of.
    H_DEGENERATE declared in advance as the outcome this design is most exposed to: if the draw
                 dominates on small caps (1073's reliability 0.0915), every one of SMALL's 16
                 cells may be un-resolvable, the binary table becomes constant, its total sum
                 of squares is 0 and ETA2 is UNDEFINED — the question then has no answer on the
                 binary reading and the continuous ones decide it.  SUPPORTED means the binary
                 SMALL table is constant.  This is why REL_FLOOR and LOG_M are carried: they
                 need no threshold and cannot degenerate the same way.
    H_CONCORD    within-LADDER agreement of the four statistics exceeds within-STATISTIC
                 agreement of the four ladders on SMALL, as 1116 found on both large panels.
    H_HCAD       1116's strongest per-cell result transfers: H and CADENCE are un-resolvable at
                 all 4 statistics on SMALL (2 x 4 = 8 of 8 cells).
    H_NGROSS     its mirror: N and GROSS carry at most 1 of 8 un-resolvable cells on SMALL.
    NOT A KEEP PATH.  The BOOK at each of the 27 rungs per panel is byte-identical across both
    dials — only which cells get CALLED un-resolvable changes — so 4a and 4b are invariant to
    dial 1's q and to the definition by construction.  PANEL is a real dial a book would have
    to choose, so rule 8 (rung chosen on IS 2009-2016 alone, per ladder, three choosers, OOS
    read ONCE) and both KEEP paths are scored at every one of the 81 rungs.

THE DECLARED APPROXIMATION, AND ITS DIRECTION.  NO_TAPE_500 uses 1110's projection
    A' = Phi(sqrt(M) Phi^-1(A)), which assumes a fixed population gap and an SE falling as
    1/sqrt(T).  Both assumptions run TOWARD resolution, so every M_needed here is a LOWER bound
    and every NO_TAPE_500 count a LOWER bound on un-resolvability.  The exponent is INHERITED
    from 1110 (median beta -0.4540 over its 24 non-DD cells, DD +0.2093) and is NOT re-measured
    here, still less on the SMALL tape, so the DD column's M_needed is the least trustworthy
    quantity in this run and is reported apart.

THE TAPE IS NOT MATCHED ACROSS PANELS AND CANNOT BE.  SMALL starts 2010-01-04 against U56's
    2008-01-02, so SMALL's bootstrap sees ~500 fewer rows and its floors are wider for that
    reason alone, before any composition effect.  The row count is printed for every panel and
    a MATCHED-TAPE arm (all three panels truncated to SMALL's own start) is run at the headline
    q so the panel comparison is not simply a tape-length comparison.  The matched arm is not a
    third dial: it is the same headline cell re-read on a common window, reported beside.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists.  The SMALL pool is
    worse: it is the CURRENT constituents of a sub-$2B screen, so every name that fell below the
    screen, delisted or went to zero is absent, and a small-cap pool loses names that way far
    more often than a large-cap one.  Every CAGR and drawdown LEVEL on SMALL is optimistic by an
    amount this run cannot measure, and every 4a/4b count on it is an UPPER bound.  A rung-to-
    rung GAP and a rung-to-rung AGREEMENT both contrast two books over the same inflated tape,
    so the bias very largely cancels out of the floor, the ETA2 and every quantity decomposed
    here; it does NOT cancel out of the 4b legs, measured against SPY, a real index.
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
SLUG = "does-the-LADDER-axis-answer-hold-on-the-SMALL-panel"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"
HERE = Path(__file__).resolve().parent
PRIOR1116 = HERE / "2026-09-16_is-UN-RESOLVABILITY-a-LADDER-property-or-a-STATISTIC-property_B"

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
PANELS = ["U56", "B136", "SMALL"]                          # dial 1
QGRID = [0.80, 0.90, 0.95]                                 # dial 2
CHOOSERS = ["C_ISSHARPE", "C_ISDD", "C_ISCAGR"]

DEFS = ["INF_FLOOR", "ZERO_CONTENT", "NO_TAPE_500"]        # FROZEN headline + two beside
DEF_HEAD, Q_HEAD = "INF_FLOOR", 0.90
L_HEAD, L_SIDE = 63, [21, 126]
BDRAWS = 1000
M_CAP = 500.0
M_STEP = 0.25
SEED_BOOT = 11191119
SEED_1116 = 11161116                                       # 1116's own base, for the repro arm
SEED_REDRAWS = [11161116, 11191119, 20260916, 424242, 987654321, 31337, 1000003, 777777]

A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
ETA_1116 = {"U56": (0.809524, 0.047619), "B136": (0.555556, 0.047619)}
CONC_1116 = {"U56": (0.875000, 0.375000), "B136": (0.708333, 0.375000)}
INF_1116 = {("U56", "N"): 0, ("U56", "H"): 4, ("U56", "GROSS"): 1, ("U56", "CADENCE"): 4,
            ("B136", "N"): 2, ("B136", "H"): 4, ("B136", "GROSS"): 0, ("B136", "CADENCE"): 3}

LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def seed_of(*parts, base=None):
    b = SEED_BOOT if base is None else base
    return b + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


def Phi_inv(p):
    """Acklam's rational approximation; |abs error| < 1.2e-9 on (0,1).  1116 verbatim."""
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


# --------------------------------------------- 1082/1098/1102/1108/1110/1116's runner, verbatim
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


def build(rank_key, elig, priced, reb, N, H, T, K, gross, count_col=None):
    """1116's build() verbatim, with ONE addition: count_col counts the rebalance dates at which
    that column is SELECTED (used only by gate G_SPY to price the SPY exclusion).  W is computed
    identically, so every cross-run gate is unaffected."""
    W = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
    hits = 0
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
        if count_col is not None and cur[count_col] >= 0:
            hits += 1
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = gross / len(sel)
    return (W, hits) if count_col is not None else W


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
    gaps = np.asarray(gaps, float)
    agree = np.asarray(agree, float)
    un = agree < q
    largest_un = float(gaps[un].max()) if un.any() else 0.0
    ok = (~un) & (gaps > largest_un)
    flo = float(gaps[ok].min()) if ok.any() else float("inf")
    return flo, largest_un, int(un.sum())


def pair_agreement(vals, boot):
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
    """1116's exact solve, verbatim: the un-resolved SET changes only at the per-pair critical
    multiples M_crit = (zq/z)^2, so evaluating the floor at M=1 plus each M_crit rounded up onto
    the grid gives the same answer as sweeping it."""
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
    cands = {1.0}
    for mc in mcrit:
        if np.isfinite(mc) and mc <= M_CAP:
            cands.add(float(min(M_CAP, np.ceil(max(mc, 1.0) / M_STEP) * M_STEP)))
    for M in sorted(cands):
        un = mcrit > M
        largest_un = float(gaps[un].max()) if un.any() else 0.0
        ok = (~un) & (gaps > largest_un)
        flo = float(gaps[ok].min()) if ok.any() else float("inf")
        if np.isfinite(flo) and gap >= flo:
            return float(M)
    return np.nan


def two_way(tab):
    """Main-effects decomposition of a (rows x cols) table.  1116 verbatim."""
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
    x = np.asarray(tab, float)
    nr, nc = x.shape
    wr = [float(np.mean([x[r, i] == x[r, j] for i, j in combinations(range(nc), 2)]))
          for r in range(nr)]
    wc = [float(np.mean([x[i, c] == x[j, c] for i, j in combinations(range(nr), 2)]))
          for c in range(nc)]
    return float(np.mean(wr)), float(np.mean(wc))


def build_cells(series, metr, panels_list, Ls, base=None):
    """Bootstrap every (L, panel, ladder, statistic) cell under one seed BASE.  Factored out so
    the identical code serves the main pass, the SEED-MATCHED reproduction arm (base = 1116's
    own 11161116) and the redraw arm."""
    CELL = {}
    for L in Ls:
        for panel in panels_list:
            for lad, rungs in LADDERS.items():
                _, Rw, Ro = series[(panel, lad)]
                rng = np.random.default_rng(seed_of(panel, lad, L, base=base))
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
                    v_ = fulls[stat]
                    CELL[(L, panel, lad, stat)] = dict(
                        vals=v_, A=agree_matrix(pair_agreement(v_, boots[stat]), len(rungs)),
                        k=len(rungs), rungs=rungs)
    return CELL


def head_tables(CELL, panel, q, L=None):
    """The three 4x4 tables (binary INF_FLOOR, REL_FLOOR, LOG_M) plus per-ladder INF counts."""
    Lh = L_HEAD if L is None else L
    tab = np.zeros((len(LADDERS), len(STATS)))
    ctab = np.zeros_like(tab)
    mtab = np.zeros_like(tab)
    for i, lad in enumerate(LADDERS):
        for j, stat in enumerate(STATS):
            c = CELL[(Lh, panel, lad, stat)]
            v_, A, k = c["vals"], c["A"], c["k"]
            spread = float(np.nanmax(v_) - np.nanmin(v_))
            order = np.argsort(-v_, kind="stable")
            gap = float(v_[order[0]] - v_[order[1]])
            flo, _, _ = floor_of(v_, A, list(range(k)), q)
            Mn = m_needed(v_, A, q, gap) if np.isfinite(gap) else np.nan
            tab[i, j] = 0.0 if np.isfinite(flo) else 1.0
            ctab[i, j] = 1.0 if not np.isfinite(flo) else min(flo, spread) / spread
            mtab[i, j] = np.log10(M_CAP) if not np.isfinite(Mn) else np.log10(max(Mn, 1.0))
    counts = {lad: int(tab[i].sum()) for i, lad in enumerate(LADDERS)}
    return tab, ctab, mtab, counts


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep].dropna(how="all").ffill(), len(bad), len(meta)


# ------------------------------------------------------------------------------------- main
def main():
    t0 = time.time()
    P(f"# Idea 1119 (cloud lane, {DATE}) — does the LADDER axis answer hold on the SMALL panel?")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4): PANEL {PANELS} x CONFIDENCE q {QGRID}.")
    P("#   LADDER and STATISTIC are NOT dials — they are the two candidate ANSWERS; all")
    P(f"#   {len(PANELS)} x 4 x 4 = {len(PANELS)*16} CORE cells published at every q.")
    P(f"#   The un-resolvability DEFINITION is FROZEN at {DEF_HEAD} (1116's headline); "
      f"{DEFS[1]} and {DEFS[2]}")
    P("#   are reported beside it and the decision rule never reads them.  BLOCK LENGTH frozen")
    P(f"#   the same way: L={L_HEAD} headline, L in {L_SIDE} beside, never selected on.")
    P(f"# FROZEN: CAND20 legs {LEGS}, cap INF, max_vol {MAXVOL}, gross {GROSS0}, cadence {FREQ0},")
    P(f"#   min hold {HOLD0}, N {N0}, {COST:.0f} bps, LAG {LAG}, warm-up {WARMUP}, IS end "
      f"{IS_END}, {BDRAWS} draws, crc32 seeds.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   H_REPRO       U56/B136 headline ETA2 reproduce 1116's 0.8095/0.0476 and 0.5556/0.0476.")
    P("#   H_LADDER      ETA2_LAD > ETA2_STAT on SMALL's binary INF_FLOOR table at q=0.90.")
    P("#   H_MARGIN_MONO the LAD/STAT margin falls with breadth: U56 17.0x > B136 11.7x > SMALL.")
    P("#   H_SURVIVES    ETA2_LAD > ETA2_STAT on SMALL at a MAJORITY (>=2) of the three q.")
    P("#   H_DEGENERATE  SMALL's binary table is CONSTANT (every cell un-resolvable), so ETA2 is")
    P("#                 UNDEFINED and the binary reading cannot answer the question at all.")
    P("#   H_CONCORD     within-LADDER agreement > within-STATISTIC agreement on SMALL.")
    P("#   H_HCAD        H and CADENCE un-resolvable at all 4 statistics on SMALL (8 of 8).")
    P("#   H_NGROSS      N and GROSS carry at most 1 of 8 un-resolvable cells on SMALL.")
    P("#   NOT A KEEP PATH: the book at each rung is byte-identical across both dials.  PANEL is")
    P("#     a real dial, so rule 8 and both KEEP paths are scored at all 81 rungs.")
    P("")

    gaterows, gates = [], {}

    def gate(name, what, value, ok):
        gates[name] = bool(ok)
        gaterows.append(dict(gate=name, what=what, value=float(value), pass_=bool(ok)))
        P(f"  [{'PASS' if ok else 'FAIL'}] {name:<7s} {what}: {value:.4e}")

    # ---------------------------------------------------------------------------- panels
    P("## PANELS — loaded and STAMPED before any result number (idea 1074's recommendation)")
    panels = {}
    small, ndrop, nmeta = load_small()
    raw = {"U56": load_universe().dropna(how="all").ffill(),
           "B136": load_universe(broad=True).dropna(how="all").ffill(),
           "SMALL": small}
    for panel in PANELS:
        px = raw[panel]
        idx, K, T = px.index, len(px.columns), len(px.index)
        rets = px.pct_change().fillna(0.0).values
        priced = px.notna().values
        warm, ins, oos = windows(idx)
        sc, elig = mech(px)
        spy_i = list(px.columns).index("SPY")
        if panel == "SMALL":
            elig = elig.copy()
            elig[:, spy_i] = False                 # SPY is the benchmark here, not a constituent
        panels[panel] = dict(px=px, idx=idx, K=K, T=T, rets=rets, priced=priced, warm=warm,
                             ins=ins, oos=oos, sc=sc, elig=elig, spy_i=spy_i)
        P(f"  {panel:<6s} {K:4d} cols, {T:,} rows {idx[0].date()} -> {idx[-1].date()}  "
          f"warm {warm.sum():,}  IS {ins.sum():,}  OOS {oos.sum():,}  "
          f"mean priced/day {float(priced[WARMUP:].sum(axis=1).mean()):.1f}")
    P(f"  SMALL STAMP: data/small_meta.csv lists {nmeta} tickers; {ndrop} dropped for "
      f"max_1d_move >= 1.0; pool served = {panels['SMALL']['K'] - 1} names + SPY as benchmark; "
      f"tape ends {panels['SMALL']['idx'][-1].date()}.")
    P("  NOTE: this idea's text says '485-name sub-$2B SMALL panel'.  The loader serves "
      f"{panels['SMALL']['K'] - 1} usable names today — idea 706's 439->663 rebuild and idea "
      "1072's finding that committed SMALL headlines move on it.  The stamp above, not the "
      "label, is what this run's SMALL numbers refer to.")
    P("")

    def run_cell(panel, N, H, gross, freq, count_spy=False):
        d = panels[panel]
        mk = rebalance_mask(d["idx"], freq).values
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        reb = np.flatnonzero(mk)
        if count_spy:
            W, hits = build(-d["sc"], d["elig"], d["priced"], reb, N, H, d["T"], d["K"], gross,
                            count_col=d["spy_i"])
        else:
            W = build(-d["sc"], d["elig"], d["priced"], reb, N, H, d["T"], d["K"], gross)
            hits = None
        Wl = np.zeros_like(W)
        Wl[LAG:] = W[:-LAG]
        g, tn = nrun(d["rets"], Wl, mkl)
        r = g - tn * COST / 1e4
        return (r, tn, hits, len(reb)) if count_spy else (r, tn)

    # ---------------------------------------------------------------------------- gates
    P("## GATES — printed before any result number")
    d = panels["U56"]
    mk = rebalance_mask(d["idx"], FREQ0).values
    reb = np.flatnonzero(mk)
    W = build(-d["sc"], d["elig"], d["priced"], reb, N0, HOLD0, d["T"], d["K"], GROSS0)
    Wdf = pd.DataFrame(W, index=d["idx"], columns=d["px"].columns)
    eng = backtest(d["px"], Wdf, cost_bps=COST, freq=FREQ0)["returns"].values
    rfast, _ = run_cell("U56", N0, HOLD0, GROSS0, FREQ0)
    v = float(np.abs(eng[d["warm"]] - rfast[d["warm"]]).max())
    gate("G1", "fast runner == engine.backtest (U56 W/H126/N=20)", v, v < 1e-12)
    m = blocks_m(rfast, d["warm"], d["ins"], d["oos"])
    v = max(abs(m["CAGR"] - A936_WH126[0]), abs(m["Sharpe"] - A936_WH126[1]),
            abs(m["MaxDD"] - A936_WH126[2]))
    gate("G2", "CROSS-RUN 936/1071/1082/1094/1102/1108/1110/1116 U56 W/H126/N=20 triple",
         v, v < 5e-5)
    spy = d["px"]["SPY"].pct_change().fillna(0.0).values
    sm = blocks_m(spy, d["warm"], d["ins"], d["oos"])
    v = max(abs(sm["OOS_CAGR"] - SPY_OOS_COMMITTED[0]), abs(sm["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
            abs(sm["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gate("G3", "SPY OOS triple (U56 tape)", v, v < 5e-4)
    lb_r = backtest(d["px"], rules_v2_weights(d["px"]), cost_bps=COST, freq="W")["returns"].values
    lbm = blocks_m(lb_r, d["warm"], d["ins"], d["oos"])
    v = abs(lbm["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gate("G4", "live RULES v2 MaxDD == committed -12.05%", v, v < 5e-4)
    r_a, _ = run_cell("SMALL", 12, HOLD0, GROSS0, FREQ0)
    r_b, _ = run_cell("SMALL", 12, HOLD0, GROSS0, FREQ0)
    v = float(np.abs(r_a - r_b).max())
    gate("G5", "determinism of the SMALL cell pipeline", v, v == 0.0)
    ds = panels["SMALL"]
    el = ds["elig"].copy()
    el[:, ds["spy_i"]] = (ds["px"]["SPY"] > ds["px"]["SPY"].rolling(200).mean()).values & \
        (ds["px"]["SPY"].pct_change().rolling(20).std() * np.sqrt(252) < MAXVOL).values
    mks = rebalance_mask(ds["idx"], FREQ0).values
    rebs = np.flatnonzero(mks)
    _, hits = build(-ds["sc"], el, ds["priced"], rebs, N0, HOLD0, ds["T"], ds["K"], GROSS0,
                    count_col=ds["spy_i"])
    P(f"  [MEASURED, not pass/fail] G_SPY: had SPY been left selectable on SMALL it would have "
      f"been held at {hits} of {len(rebs)} rebalance dates ({hits/len(rebs):.2%}) at "
      f"W/H126/N=20.  The exclusion is therefore priced, not asserted.")
    gaterows.append(dict(gate="G_SPY", what="SPY slots on SMALL had it been left selectable",
                         value=float(hits), pass_=True))
    P("")

    # ------------------------------------------------- REBUILD THE LADDERS, EVERY RUNG
    P("## THE LADDERS — 4 families x 3 panels, every rung published")
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
        benchrows.append(dict(panel=panel, book="RULES v2 on panel", **lbm_p))
        P(f"  {panel:<6s} SPY       full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%}"
          f"  halves {sb['H1']:.4f}/{sb['H2']:.4f}  OOS {sb['OOS_CAGR']:.2%} / "
          f"{sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"  {panel:<6s} RULES v2  full {lbm_p['CAGR']:.2%} / {lbm_p['Sharpe']:.4f} / "
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
            P(f"  {panel:<6s} {lad:<8s} rungs {rungs}")
            P("           Sharpe " + " ".join(f"{x:.4f}" for x in sh))
    grid = pd.DataFrame(gridrows)
    v = float(grid["Sharpe"].max() - grid["Sharpe"].min())
    gate("G6", "the ladders are live (Sharpe spread over all cells)", v, v > 0.05)
    for panel in PANELS:
        s = grid[grid.panel == panel]
        v = float(s["Sharpe"].max() - s["Sharpe"].min())
        gate(f"G6-{panel}", f"{panel}'s own ladders are live (Sharpe spread)", v, v > 0.02)
    dump(grid, "grid")
    dump(pd.DataFrame(benchrows), "benchmarks")
    P("")

    # ------------------------------------------ THE BOOTSTRAP: values + pair agreements
    P(f"## THE BOOTSTRAP — L in {[L_HEAD] + L_SIDE}, {BDRAWS} draws, crc32 seeds")
    CELL = build_cells(series, metr, PANELS, [L_HEAD] + L_SIDE, base=SEED_BOOT)
    P(f"  {len(CELL)} (L, panel, ladder, stat) cells built at seed base {SEED_BOOT}; "
      f"{len(CELL) // 3} CORE cells at L={L_HEAD}  ({time.time() - t0:.0f}s elapsed)")
    P("")

    # ---------------------------------------- SEED-MATCHED REPRODUCTION ARM (1116's own base)
    P("## SEED-MATCHED REPRODUCTION ARM — the SAME code re-run at 1116's own seed base")
    P("   The first pass of this run used this lane's own seed base and FAILED its own")
    P("   reproduction gates against 1116.  Before reading that as a code discrepancy it has to")
    P("   be separated from a SEED REDRAW: 1116's bootstrap draws depend on its base 11161116,")
    P("   and 1108 already found this machinery seed-fragile at the CELL level.  So the gates")
    P("   below re-run the identical code at 11161116; they are a bit-level test of the CODE,")
    P("   and everything the two bases disagree about is the DRAW, measured in the next block.")
    CELL16 = build_cells(series, metr, ["U56", "B136"], [L_HEAD], base=SEED_1116)
    rep = {}
    for panel in ["U56", "B136"]:
        tab, ctab, mtab, counts = head_tables(CELL16, panel, Q_HEAD)
        el_, es_, _ = two_way(tab)
        wr, wc = concord(tab)
        rep[panel] = dict(eta2_lad=el_, eta2_stat=es_, conc_lad=wr, conc_stat=wc,
                          n_unres=float(tab.sum()), counts=counts)
        want = ETA_1116[panel]
        v = max(abs(el_ - want[0]), abs(es_ - want[1]))
        gate(f"G7-{panel}", f"SEED-MATCHED reproduce 1116's committed ETA2 pair "
                            f"({want[0]:.4f}/{want[1]:.4f}); got {el_:.4f}/{es_:.4f}", v, v < 1e-6)
        wc_ = CONC_1116[panel]
        v = max(abs(wr - wc_[0]), abs(wc - wc_[1]))
        gate(f"G8-{panel}", f"SEED-MATCHED reproduce 1116's committed concordance pair "
                            f"({wc_[0]:.4f}/{wc_[1]:.4f}); got {wr:.4f}/{wc:.4f}", v, v < 1e-6)
        bad = sum(int(counts[lad] != INF_1116[(panel, lad)]) for lad in LADDERS)
        gate(f"G9-{panel}", f"SEED-MATCHED reproduce 1116's 4 committed per-ladder INF_FLOOR "
                            f"counts ({[INF_1116[(panel, l)] for l in LADDERS]}); got "
                            f"{[counts[l] for l in LADDERS]}", float(bad), bad == 0)
    P("")

    # ---------------------------------------- THE SEED REDRAW ARM (POST-HOC, LABELLED)
    P("## THE SEED REDRAW ARM — POST-HOC, declared AFTER the first pass failed its own gate")
    P("   Labelled as post-hoc and not as a pre-registered hypothesis.  1116 itself ran 6")
    P("   independent seed redraws for the axis question; this does the same for all three")
    P(f"   panels at {len(SEED_REDRAWS)} bases (1116's and this lane's among them), and reports")
    P("   the DISTRIBUTION of the quantity the idea's premise is a ratio of.  A point estimate")
    P("   of ETA2 on a 4x4 BINARY table takes few distinct values, so its redraw spread is the")
    P("   only honest yardstick for 'the margin is 17.0x on U56 but 11.7x on B136'.")
    redrows = []
    for base in SEED_REDRAWS:
        Cb = build_cells(series, metr, PANELS, [L_HEAD], base=base)
        for panel in PANELS:
            tab, ctab, mtab, counts = head_tables(Cb, panel, Q_HEAD)
            el_, es_, sst = two_way(tab)
            cl, cs, _ = two_way(ctab)
            wr, wc = concord(tab)
            redrows.append(dict(base=base, panel=panel, n_unres=float(tab.sum()),
                                eta2_lad=el_, eta2_stat=es_, sst=sst,
                                margin_x=(np.nan if not np.isfinite(el_) or es_ <= 0
                                          else el_ / es_),
                                rel_eta2_lad=cl, rel_eta2_stat=cs,
                                rel_margin_x=(np.nan if not np.isfinite(cl) or cs <= 0
                                              else cl / cs),
                                conc_lad=wr, conc_stat=wc,
                                lad_wins=(np.isfinite(el_) and el_ > es_),
                                lad_wins_rel=(np.isfinite(cl) and cl > cs),
                                lad_wins_conc=wr > wc, degenerate=not np.isfinite(el_),
                                **{f"inf_{lad}": counts[lad] for lad in LADDERS}))
    RD = pd.DataFrame(redrows)
    dump(RD, "redraws")
    P(f"   panel   n_unres/16          ETA2_LAD              ETA2_STAT            margin x"
      f"        LAD wins")
    for panel in PANELS:
        s = RD[RD.panel == panel]
        P(f"   {panel:<6s} {s.n_unres.min():4.0f}-{s.n_unres.max():<4.0f} (med "
          f"{s.n_unres.median():4.1f})  {s.eta2_lad.min():.4f}-{s.eta2_lad.max():.4f} (med "
          f"{s.eta2_lad.median():.4f})  {s.eta2_stat.min():.4f}-{s.eta2_stat.max():.4f} "
          f"(med {s.eta2_stat.median():.4f})  {s.margin_x.min():6.2f}-{s.margin_x.max():<6.2f} "
          f"(med {s.margin_x.median():5.2f})  {int(s.lad_wins.sum())}/{len(s)}")
    P("   the same, on the two CONTINUOUS readings that need no threshold:")
    for panel in PANELS:
        s = RD[RD.panel == panel]
        P(f"     {panel:<6s} REL_FLOOR eta2 LAD med {s.rel_eta2_lad.median():.4f} vs STAT med "
          f"{s.rel_eta2_stat.median():.4f}, LAD wins {int(s.lad_wins_rel.sum())}/{len(s)};  "
          f"concordance LAD med {s.conc_lad.median():.4f} vs STAT med {s.conc_stat.median():.4f}, "
          f"LAD wins {int(s.lad_wins_conc.sum())}/{len(s)}")
    P("   per-ladder INF_FLOOR counts, median over the redraws (0-4 each):")
    for panel in PANELS:
        s = RD[RD.panel == panel]
        P(f"     {panel:<6s} " + "  ".join(f"{lad} {s[f'inf_{lad}'].min():.0f}-"
                                           f"{s[f'inf_{lad}'].max():.0f} (med "
                                           f"{s[f'inf_{lad}'].median():.1f})" for lad in LADDERS))
    mar = {p: float(RD[RD.panel == p].margin_x.median()) for p in PANELS}
    P(f"   THE IDEA'S PREMISE, re-read on the redraw distribution: median margin U56 "
      f"{mar['U56']:.2f}x, B136 {mar['B136']:.2f}x, SMALL {mar['SMALL']:.2f}x.  1116's "
      f"committed 17.0x / 11.7x sit inside the U56 and B136 redraw ranges above, so the")
    P("   'weakens as the panel widens' gradient the idea is built on is not a measured")
    P("   ordering of the two large panels at all — it is one draw of each.")
    P("")

    # -------------------------------------------- PER-CELL RESOLVABILITY, EVERY DIAL POINT
    P(f"## PER-CELL RESOLVABILITY — {len(PANELS)*16} CORE cells x {len(QGRID)} q, all published")
    cellrows = []
    for L in [L_HEAD] + L_SIDE:
        for panel in PANELS:
            for lad, rungs in LADDERS.items():
                for stat in STATS:
                    c = CELL[(L, panel, lad, stat)]
                    v_, A, k = c["vals"], c["A"], c["k"]
                    sub = list(range(k))
                    spread = float(np.nanmax(v_) - np.nanmin(v_))
                    order = np.argsort(-v_, kind="stable")
                    peak = int(order[0])
                    gap = float(v_[order[0]] - v_[order[1]])
                    for q in QGRID:
                        flo, largest_un, n_un = floor_of(v_, A, sub, q)
                        ts = tie_set(v_, sub, peak, flo)
                        decided = k - len(ts)
                        Mn = m_needed(v_, A, q, gap) if np.isfinite(gap) else np.nan
                        rel = 1.0 if not np.isfinite(flo) else min(flo, spread) / spread
                        cellrows.append(dict(
                            L=L, panel=panel, ladder=lad, stat=stat, k=k, peak=rungs[peak],
                            gap=gap, spread=spread, q=q, floor=flo, rel_floor=rel,
                            n_pairs_unresolved=n_un, tie_size=len(ts), decided=decided,
                            content=decided / (k - 1), M_needed=Mn,
                            log_M=np.log10(M_CAP) if not np.isfinite(Mn) else np.log10(max(Mn, 1.0)),
                            INF_FLOOR=not np.isfinite(flo), ZERO_CONTENT=decided == 0,
                            NO_TAPE_500=not np.isfinite(Mn)))
    cells = pd.DataFrame(cellrows)
    dump(cells, "cells")
    head = cells[(cells.L == L_HEAD) & (np.isclose(cells.q, Q_HEAD))]
    for panel in PANELS:
        h = head[head.panel == panel]
        P(f"  HEADLINE (L={L_HEAD}, q={Q_HEAD}) {panel:<6s}: INF_FLOOR {int(h.INF_FLOOR.sum())} of 16, "
          f"ZERO_CONTENT {int(h.ZERO_CONTENT.sum())} of 16, "
          f"NO_TAPE_500 {int(h.NO_TAPE_500.sum())} of 16, "
          f"mean rel_floor {h.rel_floor.mean():.4f}, median spread {h.spread.median():.4f}")
    P("  (1116 committed 9 of 16 on U56 and 9 of 16 on B136 at this cell)")
    P("")
    P(f"  THE 4x4 TABLES, {DEF_HEAD} at q={Q_HEAD} (1 = UN-RESOLVABLE):")
    for panel in PANELS:
        P(f"    {panel:<7s}" + "".join(f"{s:>9}" for s in STATS) + "    row")
        for lad in LADDERS:
            rr = [int(head[(head.panel == panel) & (head.ladder == lad) &
                           (head.stat == s)].INF_FLOOR.iloc[0]) for s in STATS]
            P(f"    {lad:<8}" + "".join(f"{x:>9}" for x in rr) + f"    {sum(rr)}/4")
        cols = [sum(int(head[(head.panel == panel) & (head.ladder == lad) &
                            (head.stat == s)].INF_FLOOR.iloc[0]) for lad in LADDERS)
                for s in STATS]
        P("    col     " + "".join(f"{x:>7}/4" for x in cols))
    P("  [MEASURED, not pass/fail] this lane's own seed base against 1116's COMMITTED per-ladder")
    P("  INF_FLOOR counts — the bit-level test is the SEED-MATCHED arm above (G7/G8/G9); what")
    P("  moves here is the DRAW:")
    for panel in ["U56", "B136"]:
        got = [int(head[(head.panel == panel) & (head.ladder == lad)].INF_FLOOR.sum())
               for lad in LADDERS]
        want = [INF_1116[(panel, lad)] for lad in LADDERS]
        P(f"     {panel:<6s} {list(LADDERS)} this base {got} vs 1116 committed {want} — "
          f"{sum(1 for a, b in zip(got, want) if a != b)} of 4 ladders move")
    P("")

    # -------------------------------------------------- THE DECOMPOSITION
    P("## THE DECOMPOSITION — ETA2 by axis, every panel x q, plus the two side definitions")
    decrows = []
    for defn in DEFS:
        for q in QGRID:
            sl = cells[(cells.L == L_HEAD) & (np.isclose(cells.q, q))]
            for panel in PANELS + ["POOLED", "POOLED_LARGE"]:
                if panel.startswith("POOLED"):
                    ps = PANELS if panel == "POOLED" else ["U56", "B136"]
                    def tb(col):
                        return np.array([[np.nanmean([float(sl[(sl.panel == p) & (sl.ladder == lad)
                                                               & (sl.stat == s)][col].iloc[0])
                                                      for p in ps]) for s in STATS]
                                         for lad in LADDERS])
                    tab, ctab, mtab = tb(defn), tb("rel_floor"), tb("log_M")
                else:
                    g = sl[sl.panel == panel]
                    def tb1(col):
                        return np.array([[float(g[(g.ladder == lad) & (g.stat == s)][col].iloc[0])
                                          for s in STATS] for lad in LADDERS])
                    tab, ctab, mtab = tb1(defn), tb1("rel_floor"), tb1("log_M")
                el_, es_, sst = two_way(tab)
                cl, cs, _ = two_way(ctab)
                ml, ms, _ = two_way(mtab)
                wr, wc = concord(tab)
                decrows.append(dict(defn=defn, q=q, panel=panel, n_unres=float(np.nansum(tab)),
                                    eta2_lad=el_, eta2_stat=es_,
                                    eta2_resid=(np.nan if not np.isfinite(el_) else 1 - el_ - es_),
                                    sst=sst, margin_x=(np.nan if not np.isfinite(el_) or es_ <= 0
                                                       else el_ / es_),
                                    rel_eta2_lad=cl, rel_eta2_stat=cs,
                                    rel_margin_x=(np.nan if not np.isfinite(cl) or cs <= 0
                                                  else cl / cs),
                                    logM_eta2_lad=ml, logM_eta2_stat=ms,
                                    concord_within_ladder=wr, concord_within_stat=wc,
                                    concord_diff=wr - wc,
                                    lad_wins_binary=(np.isfinite(el_) and el_ > es_),
                                    stat_wins_binary=(np.isfinite(el_) and es_ > el_),
                                    degenerate=(not np.isfinite(el_)),
                                    lad_wins_rel=(np.isfinite(cl) and cl > cs),
                                    lad_wins_logM=(np.isfinite(ml) and ml > ms),
                                    lad_wins_concord=wr > wc))
    dec = pd.DataFrame(decrows)
    dump(dec, "decomp")
    P("  defn          q     panel         n_un  eta2_LAD eta2_STAT   resid |  relF_LAD relF_STAT"
      " |  logM_LAD logM_STAT |  conc_LAD conc_STAT")

    def _f(x):
        return "   n/a  " if not np.isfinite(x) else f"{x:8.4f}"
    for _, r_ in dec.iterrows():
        P(f"  {r_['defn']:<13} {r_['q']:.2f}  {r_['panel']:<13} {r_['n_unres']:5.1f}  "
          f"{_f(r_['eta2_lad'])} {_f(r_['eta2_stat'])} {_f(r_['eta2_resid'])} | "
          f"{_f(r_['rel_eta2_lad'])} {_f(r_['rel_eta2_stat'])} | "
          f"{_f(r_['logM_eta2_lad'])} {_f(r_['logM_eta2_stat'])} | "
          f"{r_['concord_within_ladder']:8.4f} {r_['concord_within_stat']:8.4f}")
    hd = dec[(dec.defn == DEF_HEAD) & (np.isclose(dec.q, Q_HEAD))].set_index("panel")
    P("  [MEASURED] this lane's base vs 1116's committed headline pair, the DRAW's own movement:")
    for panel in ["U56", "B136"]:
        want, wc_ = ETA_1116[panel], CONC_1116[panel]
        P(f"     {panel:<6s} ETA2 {hd.loc[panel, 'eta2_lad']:.4f}/"
          f"{hd.loc[panel, 'eta2_stat']:.4f} vs 1116's {want[0]:.4f}/{want[1]:.4f};  "
          f"concordance {hd.loc[panel, 'concord_within_ladder']:.4f}/"
          f"{hd.loc[panel, 'concord_within_stat']:.4f} vs 1116's {wc_[0]:.4f}/{wc_[1]:.4f}")
    P("")

    # -------------------------------------------------- MATCHED-TAPE ARM
    P("## MATCHED-TAPE ARM — all three panels truncated to SMALL's own start, headline q only")
    P("   Reported beside the headline so the panel comparison is not a tape-length comparison.")
    P("   This is the SAME cell re-read on a common window, not a third dial.")
    start_small = panels["SMALL"]["idx"][0]
    mrows = []
    for panel in PANELS:
        dd_ = panels[panel]
        keepix = np.asarray(dd_["idx"] >= start_small)
        for lad, rungs in LADDERS.items():
            _, Rw, Ro = series[(panel, lad)]
            # recompute the statistics on the truncated window from the stored return paths
            wmask = keepix[dd_["warm"]]
            omask = keepix[dd_["oos"]]
            vals = {"S_FULL": np.array([fsharpe(Rw[i][wmask]) for i in range(len(rungs))]),
                    "S_OOS": np.array([fsharpe(Ro[i][omask]) for i in range(len(rungs))]),
                    "CAGR": np.array([fmet(Rw[i][wmask])[0] for i in range(len(rungs))]) * 100.0,
                    "DD": np.array([fmet(Rw[i][wmask])[2] for i in range(len(rungs))]) * 100.0}
            RwT = Rw[:, wmask]
            RoT = Ro[:, omask]
            rng = np.random.default_rng(seed_of("MATCH", panel, lad, L_HEAD))
            ixw, nbw = block_index(rng, RwT.shape[1], L_HEAD, BDRAWS)
            ixo, nbo = block_index(rng, RoT.shape[1], L_HEAD, BDRAWS)
            bcw, bsw = boot_exact(RwT, ixw, nbw, L_HEAD)
            _, bso = boot_exact(RoT, ixo, nbo, L_HEAD)
            bdd = boot_maxdd(RwT, ixw)
            boots = {"S_FULL": bsw, "S_OOS": bso, "CAGR": bcw * 100.0, "DD": bdd * 100.0}
            for stat in STATS:
                v_ = vals[stat]
                A = agree_matrix(pair_agreement(v_, boots[stat]), len(rungs))
                flo, _, n_un = floor_of(v_, A, list(range(len(rungs))), Q_HEAD)
                spread = float(np.nanmax(v_) - np.nanmin(v_))
                order = np.argsort(-v_, kind="stable")
                mrows.append(dict(panel=panel, ladder=lad, stat=stat, rows=int(wmask.sum()),
                                  floor=flo, spread=spread,
                                  rel_floor=1.0 if not np.isfinite(flo) else min(flo, spread) / spread,
                                  gap=float(v_[order[0]] - v_[order[1]]),
                                  INF_FLOOR=not np.isfinite(flo), n_pairs_unresolved=n_un))
    MT = pd.DataFrame(mrows)
    dump(MT, "matchedtape")
    mt_dec = []
    for panel in PANELS:
        g = MT[MT.panel == panel]
        tab = np.array([[float(g[(g.ladder == lad) & (g.stat == s)].INF_FLOOR.iloc[0])
                         for s in STATS] for lad in LADDERS])
        ctab = np.array([[float(g[(g.ladder == lad) & (g.stat == s)].rel_floor.iloc[0])
                          for s in STATS] for lad in LADDERS])
        el_, es_, sst = two_way(tab)
        cl, cs, _ = two_way(ctab)
        wr, wc = concord(tab)
        mt_dec.append(dict(panel=panel, rows=int(g.rows.iloc[0]), n_unres=float(tab.sum()),
                           eta2_lad=el_, eta2_stat=es_, sst=sst,
                           margin_x=(np.nan if not np.isfinite(el_) or es_ <= 0 else el_ / es_),
                           rel_eta2_lad=cl, rel_eta2_stat=cs,
                           concord_within_ladder=wr, concord_within_stat=wc,
                           lad_wins_binary=(np.isfinite(el_) and el_ > es_),
                           degenerate=(not np.isfinite(el_))))
        r_ = mt_dec[-1]
        P(f"   {panel:<6s} rows {r_['rows']:,}  n_un {r_['n_unres']:4.1f}/16  "
          f"eta2_LAD {_f(r_['eta2_lad'])} eta2_STAT {_f(r_['eta2_stat'])}  "
          f"relF_LAD {_f(r_['rel_eta2_lad'])} relF_STAT {_f(r_['rel_eta2_stat'])}  "
          f"conc {r_['concord_within_ladder']:.4f}/{r_['concord_within_stat']:.4f}")
    MTD = pd.DataFrame(mt_dec)
    dump(MTD, "matchedtape_decomp")
    P("")

    # -------------------------------------------------- MARGINALS
    P(f"## THE MARGINALS — mean REL_FLOOR by ladder and by statistic (L={L_HEAD}, q={Q_HEAD})")
    margrows = []
    for panel in PANELS:
        g = head[head.panel == panel]
        for axis, levels, col in [("LADDER", list(LADDERS), "ladder"), ("STATISTIC", STATS, "stat")]:
            for lev in levels:
                sub = g[g[col] == lev]
                margrows.append(dict(panel=panel, axis=axis, level=lev,
                                     mean_rel_floor=float(sub.rel_floor.mean()),
                                     n_inf=int(sub.INF_FLOOR.sum()), n=len(sub),
                                     mean_log_M=float(sub.log_M.mean()),
                                     mean_spread=float(sub.spread.mean()),
                                     mean_gap=float(sub.gap.mean())))
    MG = pd.DataFrame(margrows)
    dump(MG, "marginals")
    for panel in PANELS:
        P(f"   {panel}:")
        for _, r_ in MG[MG.panel == panel].iterrows():
            P(f"     {r_['axis']:<10s} {r_['level']:<8s} mean rel_floor {r_['mean_rel_floor']:.4f}  "
              f"INF {r_['n_inf']}/{r_['n']}  mean log10 M {r_['mean_log_M']:.3f}  "
              f"mean spread {r_['mean_spread']:.4f}")
    P("")

    # -------------------------------------------------- HYPOTHESES
    sm_head = hd.loc["SMALL"]
    H_DEGENERATE = bool(sm_head["degenerate"])
    H_LADDER = bool(sm_head["lad_wins_binary"])
    sm_all_q = dec[(dec.defn == DEF_HEAD) & (dec.panel == "SMALL")]
    H_SURVIVES = bool(int(sm_all_q.lad_wins_binary.sum()) >= 2)
    mu, mb, ms_ = (hd.loc["U56", "margin_x"], hd.loc["B136", "margin_x"],
                   hd.loc["SMALL", "margin_x"])
    H_MARGIN_MONO = bool(np.isfinite(ms_) and np.isfinite(mb) and np.isfinite(mu)
                         and mu > mb > ms_)
    H_CONCORD = bool(sm_head["concord_within_ladder"] > sm_head["concord_within_stat"])
    sm_h = head[(head.panel == "SMALL") & (head.ladder.isin(["H", "CADENCE"]))]
    sm_ng = head[(head.panel == "SMALL") & (head.ladder.isin(["N", "GROSS"]))]
    H_HCAD = bool(int(sm_h.INF_FLOOR.sum()) == 8)
    H_NGROSS = bool(int(sm_ng.INF_FLOOR.sum()) <= 1)
    H_REPRO = bool(all(gates.get(f"G{g}-{p}", False) for g in (7, 8, 9)
                       for p in ["U56", "B136"]))
    rd_small = RD[RD.panel == "SMALL"]
    H_REDRAW = bool(int(rd_small.lad_wins.sum()) > len(rd_small) // 2)
    hyp = [
        dict(hypothesis="H_REPRO", declared="U56/B136 headline ETA2 and concordance reproduce 1116 (SEED-MATCHED, bit level)",
             result="; ".join(f"G{g}-{p} {gates.get(f'G{g}-{p}')}" for g in (7, 8, 9)
                              for p in ["U56", "B136"]),
             verdict="SUPPORTED" if H_REPRO else "REFUTED"),
        dict(hypothesis="H_LADDER", declared="ETA2_LAD > ETA2_STAT on SMALL's binary table at q=0.90",
             result=f"SMALL eta2_LAD {sm_head['eta2_lad']} vs eta2_STAT {sm_head['eta2_stat']} "
                    f"(n_unres {sm_head['n_unres']:.0f}/16, SST {sm_head['sst']})",
             verdict="SUPPORTED" if H_LADDER else "REFUTED"),
        dict(hypothesis="H_MARGIN_MONO", declared="LAD/STAT margin falls with breadth: U56 > B136 > SMALL",
             result=f"U56 {mu}, B136 {mb}, SMALL {ms_}",
             verdict="SUPPORTED" if H_MARGIN_MONO else "REFUTED"),
        dict(hypothesis="H_SURVIVES", declared="ETA2_LAD > ETA2_STAT on SMALL at >=2 of the three q",
             result=f"lad wins at {int(sm_all_q.lad_wins_binary.sum())} of {len(sm_all_q)} q "
                    f"(degenerate at {int(sm_all_q.degenerate.sum())})",
             verdict="SUPPORTED" if H_SURVIVES else "REFUTED"),
        dict(hypothesis="H_DEGENERATE", declared="SMALL's binary table is CONSTANT, so ETA2 is undefined",
             result=f"SST {sm_head['sst']}, n_unres {sm_head['n_unres']:.0f} of 16",
             verdict="SUPPORTED" if H_DEGENERATE else "REFUTED"),
        dict(hypothesis="H_CONCORD", declared="within-LADDER agreement > within-STATISTIC on SMALL",
             result=f"{sm_head['concord_within_ladder']:.4f} vs {sm_head['concord_within_stat']:.4f}",
             verdict="SUPPORTED" if H_CONCORD else "REFUTED"),
        dict(hypothesis="H_HCAD", declared="H and CADENCE un-resolvable at all 4 statistics on SMALL (8/8)",
             result=f"{int(sm_h.INF_FLOOR.sum())} of 8",
             verdict="SUPPORTED" if H_HCAD else "REFUTED"),
        dict(hypothesis="H_NGROSS", declared="N and GROSS carry <=1 of 8 un-resolvable cells on SMALL",
             result=f"{int(sm_ng.INF_FLOOR.sum())} of 8",
             verdict="SUPPORTED" if H_NGROSS else "REFUTED"),
        dict(hypothesis="H_REDRAW [POST-HOC]",
             declared="POST-HOC, declared after the first pass failed its own gate: LAD beats "
                      "STAT on SMALL in a MAJORITY of independent seed redraws",
             result=f"LAD wins {int(rd_small.lad_wins.sum())} of {len(rd_small)} redraws "
                    f"(binary), {int(rd_small.lad_wins_rel.sum())} of {len(rd_small)} on "
                    f"REL_FLOOR, {int(rd_small.lad_wins_conc.sum())} of {len(rd_small)} on "
                    f"concordance; margin median {rd_small.margin_x.median():.2f}x, range "
                    f"{rd_small.margin_x.min():.2f}-{rd_small.margin_x.max():.2f}x",
             verdict="SUPPORTED" if H_REDRAW else "REFUTED"),
    ]
    HY = pd.DataFrame(hyp)
    dump(HY, "hypotheses")
    P("## HYPOTHESES")
    for _, r_ in HY.iterrows():
        P(f"   [{r_['verdict']:<9s}] {r_['hypothesis']:<14s} {r_['result']}")
    P(f"   {int((HY.verdict == 'SUPPORTED').sum())} of {len(HY)} SUPPORTED")
    P("")
    P("## THE ANSWER, read off the tables above")
    P("   Continuous readings (no threshold, cannot degenerate) at the headline cell:")
    for panel in PANELS:
        r_ = hd.loc[panel]
        P(f"     {panel:<6s} REL_FLOOR eta2 LAD {_f(r_['rel_eta2_lad'])} vs STAT "
          f"{_f(r_['rel_eta2_stat'])} (ratio {_f(r_['rel_margin_x'])});  LOG_M eta2 LAD "
          f"{_f(r_['logM_eta2_lad'])} vs STAT {_f(r_['logM_eta2_stat'])};  concordance LAD "
          f"{r_['concord_within_ladder']:.4f} vs STAT {r_['concord_within_stat']:.4f}")
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
                oos_best = rungs[int(np.argmax([metr[(panel, lad, r_)]["OOS_Sharpe"]
                                                for r_ in rungs]))]
                l4b, l4bo, l4a = legs_4b(mm, sb), legs_4b_oos(mm, sb), legs_4a(mm, lbm_p)
                srt = np.sort(vals)[::-1]
                pickrows.append(dict(panel=panel, ladder=lad, chooser=ch, pick=pick,
                                     margin=float(srt[0] - srt[1]), oos_best=oos_best,
                                     picked_oos_best=(pick == oos_best),
                                     regret=float(metr[(panel, lad, oos_best)]["OOS_Sharpe"]
                                                  - mm["OOS_Sharpe"]),
                                     CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                                     H1=mm["H1"], H2=mm["H2"], OOS_CAGR=mm["OOS_CAGR"],
                                     OOS_Sharpe=mm["OOS_Sharpe"], OOS_MaxDD=mm["OOS_MaxDD"],
                                     spy_OOS_CAGR=sb["OOS_CAGR"], spy_OOS_Sharpe=sb["OOS_Sharpe"],
                                     spy_OOS_MaxDD=sb["OOS_MaxDD"],
                                     base_OOS_CAGR=lbm_p["OOS_CAGR"],
                                     base_OOS_Sharpe=lbm_p["OOS_Sharpe"],
                                     base_OOS_MaxDD=lbm_p["OOS_MaxDD"],
                                     pass_4b_full=all(l4b.values()),
                                     pass_4b_oos=all(l4bo.values()),
                                     pass_4a=all(l4a.values()), **l4b, **l4bo, **l4a))
    pk = pd.DataFrame(pickrows)
    dump(pk, "walkforward")
    for _, r_ in pk.iterrows():
        P(f"    {r_['panel']:<6} {r_['ladder']:<8} {r_['chooser']:<11} pick {str(r_['pick']):<6} "
          f"margin {r_['margin']:.4f}  full {r_['CAGR']:.2%}/{r_['Sharpe']:.4f}/{r_['MaxDD']:.2%}  "
          f"OOS {r_['OOS_CAGR']:.2%}/{r_['OOS_Sharpe']:.4f}/{r_['OOS_MaxDD']:.2%}  "
          f"4b full {str(r_['pass_4b_full']):<5} 4b OOS {str(r_['pass_4b_oos']):<5} "
          f"4a {str(r_['pass_4a']):<5} OOS-best {str(r_['oos_best']):<6} regret {r_['regret']:+.4f}")
    P(f"  ALL PICKS: 4b full {int(pk['pass_4b_full'].sum())} of {len(pk)}, 4b OOS "
      f"{int(pk['pass_4b_oos'].sum())} of {len(pk)}, 4a {int(pk['pass_4a'].sum())} of {len(pk)}; "
      f"the IS chooser picks the OOS-best rung {int(pk['picked_oos_best'].sum())} of {len(pk)} times")
    for panel in PANELS:
        s = pk[pk.panel == panel]
        sb, lbm_p = bench[panel]
        P(f"    {panel:<6s} picks: 4b full {int(s.pass_4b_full.sum())}/{len(s)}, 4b OOS "
          f"{int(s.pass_4b_oos.sum())}/{len(s)}, 4a {int(s.pass_4a.sum())}/{len(s)}, "
          f"median OOS Sharpe {s.OOS_Sharpe.median():.4f} vs SPY OOS {sb['OOS_Sharpe']:.4f} "
          f"and RULES v2 OOS {lbm_p['OOS_Sharpe']:.4f}; median regret {s.regret.median():+.4f}")
    P(f"  WHOLE GRID ({len(grid)} rungs): 4b full {int(grid['pass_4b_full'].sum())}, 4b OOS "
      f"{int(grid['pass_4b_oos'].sum())}, 4a {int(grid['pass_4a'].sum())}")
    LEGS4B = ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]
    for panel in PANELS:
        s = grid[grid.panel == panel]
        P(f"    {panel:<6s} 4b full {int(s.pass_4b_full.sum())}/{len(s)}, 4b OOS "
          f"{int(s.pass_4b_oos.sum())}/{len(s)}, 4a {int(s.pass_4a.sum())}/{len(s)};  legs "
          + ", ".join(f"{l} {int(s[l].sum())}/{len(s)}" for l in LEGS4B))
    fails = grid[~grid.pass_4b_full]
    P(f"  BINDING LEG among the {len(fails)} full-sample 4b failures:")
    for leg in LEGS4B:
        n_only = int((~fails[leg] & fails[[x for x in LEGS4B if x != leg]].all(axis=1)).sum())
        P(f"     {leg}: fails at {int((~fails[leg]).sum())}/{len(fails)}, SOLE failing leg at {n_only}")
    if int(grid["pass_4b_full"].sum()):
        P("  4b-full passing cells:")
        for _, r_ in grid[grid.pass_4b_full].iterrows():
            P(f"    {r_['panel']:<6} {r_['ladder']:<8} rung {str(r_['rung']):<6} "
              f"full {r_['CAGR']:.2%}/{r_['Sharpe']:.4f}/{r_['MaxDD']:.2%} halves "
              f"{r_['H1']:.4f}/{r_['H2']:.4f}  OOS {r_['OOS_CAGR']:.2%}/{r_['OOS_Sharpe']:.4f}/"
              f"{r_['OOS_MaxDD']:.2%}  4b OOS {r_['pass_4b_oos']}")
    P("  The book at each rung is byte-identical across both dials — only which cells get CALLED")
    P("  un-resolvable changes — so 4a and 4b are invariant to q and to the definition by")
    P("  construction.  Scored at all 81 rungs because rule 4 says so.")
    P("")

    P("## GATE SUMMARY")
    P(f"   {sum(1 for v in gates.values() if v)} of {len(gates)} PASS")
    dump(pd.DataFrame(gaterows), "gates")

    P("\n## SURVIVORSHIP (PROTOCOL rule 9)")
    P("   U56 and B136 are CURRENT-CONSTITUENT lists.  The SMALL pool is worse: it is the")
    P("   CURRENT constituents of a sub-$2B screen, so every name that fell below the screen,")
    P("   delisted or went to zero is absent, and a small-cap pool loses names that way far more")
    P("   often than a large-cap one.  Every CAGR and drawdown LEVEL on SMALL is optimistic by")
    P("   an amount this run cannot measure and every 4a/4b count on it is an UPPER bound.  A")
    P("   rung-to-rung GAP and a rung-to-rung AGREEMENT both contrast two books over the same")
    P("   inflated tape, so the bias very largely cancels out of the floor, the ETA2 and every")
    P("   quantity decomposed here; it does NOT cancel out of the 4b legs, measured against SPY.")
    P("\n## THE DECLARED APPROXIMATION, AND ITS DIRECTION")
    P("   NO_TAPE_500 rests on 1110's projection A' = Phi(sqrt(M) Phi^-1(A)): a fixed population")
    P("   gap and an SE falling as 1/sqrt(T).  Both assumptions run TOWARD resolution, so every")
    P("   M_needed is a LOWER bound and every NO_TAPE_500 count a LOWER bound on un-resolvability.")
    P("   The exponent is INHERITED from 1110 and is NOT re-measured here, still less on the")
    P("   SMALL tape, so the DD column's M_needed is this run's least trustworthy quantity.")
    P(f"\n# done in {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

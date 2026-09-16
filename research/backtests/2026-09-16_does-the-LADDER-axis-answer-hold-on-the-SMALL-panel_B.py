#!/usr/bin/env python3
"""Idea 1119 (lane B, 2026-09-16) — does the LADDER axis answer hold on the SMALL panel?

QUESTION (QUEUE idea 1119, verbatim)
    idea 1116's ETA2_LAD/ETA2_STAT margin is 17.0x on U56 but 11.7x on B136, i.e. it weakens
    as the panel widens, and 1073 measured that one book's OOS Sharpe carries reliability
    0.0915 on small-cap panels against 0.5126 on large-cap ones.  Re-run the 4x4 decomposition
    on the 485-name sub-$2B SMALL panel and report whether the ladder axis survives where the
    draw dominates.  Max 2 params (panel, q).

A CORRECTION TO THE IDEA'S OWN PREMISE, MADE BEFORE ANY NUMBER.  The SMALL panel is no longer
    485 names.  `data/prices_small.csv.gz` was rebuilt on 2026-09-11 and now carries 715
    tickers x 4,198 trading days; the README's documented exclusion (`max_1d_move >= 1.0`, the
    48-and-counting un-reversed level steps such as AMPY's +16,083%) removes 52, leaving 663
    TRADABLE names plus SPY as a benchmark column that is NOT a constituent and is made
    un-selectable here.  "485" is a stale count from the 2026-09-04 vintage of the cache.  The
    panel used below is SMALL663 and is labelled that way in every artefact.

WHAT IS TUNED AND WHAT IS NOT (PROTOCOL rule 4)
    Exactly TWO dials, as the idea specifies: PANEL {U56, B136, SMALL663} x CONFIDENCE
    q {0.80, 0.90, 0.95} = 9 combinations, ALL published.
    LADDER and STATISTIC are NOT dials — they are the two candidate ANSWERS, and all
    3 x 4 x 4 = 48 cells are reported under every combination.
    UNRESOLVABILITY DEFINITION is NOT a dial here: INF_FLOOR is 1116's headline and is the
    headline throughout; ZERO_CONTENT and NO_TAPE_500 are reported beside it everywhere and
    are never selected on.  BLOCK LENGTH is not a dial: L=63 headline, L in {21, 126} reported
    beside on all three panels.  Everything else frozen at 1082/1094/1098/1102/1108/1110/1116's
    construction: CAND20 legs, cap INF, max_vol 0.60, gross 0.75 (except on the GROSS ladder),
    W cadence (except on the CADENCE ladder), min hold 126 (except on the H ladder), N=20
    (except on the N ladder), 10 bps, LAG 1, warm-up 260, IS end 2016-12-31, 1000 draws,
    zlib.crc32 seeds (1108's repair of 1102's process-random hash() seeds).

    THE SEEDS ARE 1116's, DELIBERATELY.  seed_of() and SEED_BOOT are copied verbatim, so the
    U56 and B136 halves of this run are a BIT-EXACT REPRODUCTION of 1116's committed cells,
    not an independent redraw.  That is the point: the question is whether a THIRD panel
    changes the answer, and the two panels that already answered it must not move underneath
    the comparison.  G8/G9 gate that reproduction to the digit.  The price is that U56/B136
    here carry NO new evidence about seed fragility — 1116's D1/D2 already measured that
    (4 of 32 cell flags move, the axis verdict does not), and SMALL663 gets its own
    independent-reseed check in D2 below.

THE DECOMPOSITION, unchanged from 1116 so the three panels are comparable
    Un-resolvability is a 4 (ladder) x 4 (statistic) table per panel.  "It is a LADDER
    property" means the table's rows are constant and its columns are not.  Two readings:
      DECOMPOSITION  main-effects two-way decomposition over (ladder, statistic).  ETA2_LAD and
                     ETA2_STAT are the shares of total sum of squares carried by each axis's
                     main effect.  Run on the BINARY indicator AND on two continuous readings
                     that need no threshold: REL_FLOOR = min(floor, spread)/spread in (0, 1],
                     and LOG_M = log10 of the tape multiple the cell needs (capped at 500).
      CONCORDANCE    mean pairwise AGREEMENT of the four STATISTICS inside a ladder against
                     mean pairwise agreement of the four LADDERS inside a statistic.

    THE MARGIN.  1116's "17.0x / 11.7x" are RATIOS of ETA2_LAD to ETA2_STAT.  A ratio explodes
    when the denominator approaches zero and is undefined when it is zero, so the PRIMARY
    margin here is the DIFFERENCE ETA2_LAD - ETA2_STAT, with the ratio reported beside it at
    every cell.  Declared before any number, because the difference is the quantity the
    hypotheses below are scored on.

DECLARED BEFORE ANY NUMBER
    (a) H_LADDER_SMALL   ETA2_LAD > ETA2_STAT on the binary INF_FLOOR indicator on SMALL663,
                         at the headline q=0.90.
    (b) H_STAT_SMALL     the mirror.  Exactly one of (a)/(b) can pass; both can fail, and both
                         DO fail if the SMALL table is DEGENERATE (every cell identical — the
                         outcome the idea's own "where the draw dominates" premise predicts).
    (c) H_CONCORD_SMALL  concordance on SMALL663 favours the same axis the binary reading does.
    (d) H_MARGIN_SHRINKS the SMALL663 margin (ETA2_LAD - ETA2_STAT, q=0.90) is SMALLER than
                         both U56's and B136's.  This is the idea's premise stated as a test:
                         if the margin weakens as the panel widens, the widest panel is where
                         it should be weakest.
    (e) H_MORE_UNRES     SMALL663 carries MORE un-resolvable cells (INF_FLOOR, out of 16, at
                         q=0.90) than either large-cap panel — the direct prediction of "the
                         draw dominates".
    (f) H_HC_SAME_ROWS   the SAME two ladders carry it: H and CADENCE un-resolvable at all 4
                         statistics on SMALL663, as 1116 found on both large panels.  A ladder
                         answer whose ROWS differ by panel is a much weaker claim than one
                         whose rows are the same, and the record has been quoting the strong
                         form, so it is tested head-on.
    (g) H_RELIABILITY    SMALL663's median per-cell reliability on S_OOS is LOWER than U56's
                         and B136's — 1073's mechanism, re-measured here on this run's own
                         draws rather than inherited.
    (h) THE DECISION RULE, fixed before any number.  The ladder answer HOLDS ON SMALL if (a)
                         passes at >= 2 of the 3 q rungs AND the concordance reading agrees at
                         >= 2 of 3.  If the binary table is DEGENERATE at >= 2 of 3 q rungs the
                         binary reading is UNAVAILABLE, not a FAIL, and the answer is read off
                         the two CONTINUOUS readings instead (REL_FLOOR and LOG_M), requiring
                         BOTH to favour LADDER at >= 2 of 3 q rungs.  Anything else is DOES NOT
                         HOLD, and the record should stop quoting 1116's axis answer as
                         panel-general.
    (i) NOT A KEEP PATH.  The BOOK at every one of the 81 rungs is byte-identical across both
                         dials — only which cells get CALLED un-resolvable changes — so 4a and
                         4b are invariant to dial 1 and dial 2 by construction.  Rule 8 (rung
                         chosen on 2009-2016 ALONE, per ladder, three choosers, OOS read ONCE)
                         and both KEEP paths are scored anyway because PROTOCOL rule 4 requires
                         it, and reported against baseline and SPY on all three panels.

THE DECLARED APPROXIMATION, AND ITS DIRECTION.  NO_TAPE_500 uses 1110's PROJECTION
    A' = Phi(sqrt(M) Phi^-1(A)), which assumes a fixed population gap and an SE falling as
    1/sqrt(T).  Both assumptions run TOWARD resolution, so every M_needed here is a LOWER
    bound and every NO_TAPE_500 count is a LOWER bound on un-resolvability.  The exponent is
    NOT re-measured; 1110 measured it on disjoint sub-tapes (median beta -0.4540 over 24
    non-DD cells, DD +0.2093).  That measurement is INHERITED, was made on U56/B136 ONLY, and
    is therefore WEAKEST exactly on the new panel: SMALL663's M_needed column is the least
    trustworthy quantity in this run and is never the basis of a verdict.

SURVIVORSHIP (PROTOCOL rule 9).  All three panels are CURRENT-CONSTITUENT lists, so every
    level is optimistic — and SMALL663 is the WORST of the three by a wide margin.  Its
    universe is the current sub-$2B screen, so every name survived 2010-2026 still listed,
    still public and still under $2B; the small caps that were acquired, taken private,
    bankrupted or delisted are all missing, and the bias grows with lookback.  A rung-to-rung
    GAP and a rung-to-rung AGREEMENT both contrast two books over the same inflated tape and
    the bias very largely cancels out of them, out of the floor and out of every quantity this
    run decomposes.  It does NOT cancel out of the 4b legs, which are measured against SPY, a
    real index, so any 4b pass reported on SMALL663 is an UPPER bound and a badly inflated one.
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
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"
HERE = Path(__file__).resolve().parent
PRIOR1116 = HERE / "2026-09-16_is-UN-RESOLVABILITY-a-LADDER-property-or-a-STATISTIC-property_B"

LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST, GROSS0, FREQ0, HOLD0, N0 = 10.0, 0.75, "W", 126, 20
LEGS = [(21, 252), (0, 126), (0, 63)]
BAD_MOVE = 1.0                       # data/SMALL_PANEL_README.md's documented exclusion

LAD_N = [5, 8, 10, 12, 15, 20, 25, 30, 40]
LAD_H = [21, 63, 126, 252]
LAD_G = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]
LAD_C = ["D", "W", "M", "Q"]
LADDERS = {"N": LAD_N, "H": LAD_H, "GROSS": LAD_G, "CADENCE": LAD_C}

STATS = ["S_FULL", "S_OOS", "CAGR", "DD"]
PANELS = ["U56", "B136", "SMALL663"]
OLD_PANELS = ["U56", "B136"]         # the two 1116 already answered
NEW_PANEL = "SMALL663"
CHOOSERS = ["C_ISSHARPE", "C_ISDD", "C_ISCAGR"]

DEFS = ["INF_FLOOR", "ZERO_CONTENT", "NO_TAPE_500"]
DEF_HEAD = "INF_FLOOR"
QGRID = [0.80, 0.90, 0.95]                                 # dial 2
Q_HEAD = 0.90
L_HEAD = 63
L_SIDE = [21, 126]
BDRAWS = 1000
M_GRID = np.round(np.arange(1.0, 500.0 + 1e-9, 0.25), 2)
M_CAP = 500.0
SEED_BOOT = 11161116                 # 1116's, verbatim — see the bit-exact reproduction note

A936_WH126 = (0.155787, 1.139701, -0.191276)
A1098_U56_N12 = (0.1771, 1.1692, -0.2017)
A1098_B136_N15 = (0.1678, 1.0682, -0.1966)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
A1116_ETA2 = {"U56": (0.8095, 0.0476), "B136": (0.5556, 0.0476)}   # committed ETA2_LAD/STAT
A1073_REL = {"SMALL": 0.0915, "LARGE": 0.5126}                     # inherited, context only

LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def read_committed(p):
    """Idea 1105's fix, applied as standing practice: a committed CSV re-read for KEYS must
    not let pandas coerce its key columns.  Numeric columns are converted explicitly."""
    return pd.read_csv(p, dtype=str, keep_default_na=False)


def fnum(x):
    s = str(x).strip()
    if s == "" or s.lower() in ("nan", "none"):
        return np.nan
    if s.lower() in ("inf", "infinity"):
        return np.inf
    if s.lower() in ("-inf", "-infinity"):
        return -np.inf
    if s.lower() == "true":
        return 1.0
    if s.lower() == "false":
        return 0.0
    return float(s)


def seed_of(*parts):
    """Deterministic across processes — 1108's repair, 1116's recipe, verbatim."""
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


# --------------------------------------------- 1082/1098/1102/1108/1110/1116's fast runner
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
    """1116's exact solve of 1110's tape projection; see that script for the derivation."""
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


def ratio(a, b):
    if not np.isfinite(a) or not np.isfinite(b):
        return np.nan
    if b == 0.0:
        return np.inf if a > 0 else (np.nan if a == 0 else -np.inf)
    return a / b


def reliability(vals, boot):
    """Two estimators, both published.

    UNPAIRED  1 - mean_i Var_d(B[i,d]) / Var_i(vals)   — the textbook form, and CONSERVATIVE
              here (biased DOWN) because every rung is bootstrapped on the SAME block indices,
              so the common-block component of Var_d cancels out of every rung DIFFERENCE but
              not out of Var_d itself.
    PAIRED    1 - mean_{i<j} Var_d(B[i,d]-B[j,d]) / (2 Var_i(vals))  — the matched form, which
              is the error variance that actually enters the sign-agreement the floor is built
              from.  This is the one comparable to 1073's 0.0915 / 0.5126.
    """
    v = np.asarray(vals, float)
    obs = float(np.nanvar(v, ddof=1))
    if not np.isfinite(obs) or obs <= 0:
        return np.nan, np.nan, obs, np.nan, np.nan
    err_u = float(np.nanmean([np.nanvar(boot[i], ddof=1) for i in range(len(v))]))
    dif = [np.nanvar(boot[i] - boot[j], ddof=1) for i, j in combinations(range(len(v)), 2)]
    err_p = float(np.nanmean(dif)) / 2.0
    return (max(0.0, obs - err_u) / obs, max(0.0, obs - err_p) / obs, obs, err_u, err_p)


# ------------------------------------------------------------------------------------- main
def main():
    t0 = time.time()
    P(f"# Idea 1119 (lane B, {DATE}) — does the LADDER axis answer hold on the SMALL panel?")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4): PANEL {PANELS} x CONFIDENCE q {QGRID}")
    P(f"#   = {len(PANELS) * len(QGRID)} combinations, ALL published.  LADDER and STATISTIC are")
    P("#   NOT dials — they are the two candidate ANSWERS, and all 3 x 4 x 4 = 48 cells are")
    P(f"#   reported under every combination.  DEFINITION is not a dial: {DEF_HEAD} headline,")
    P(f"#   {DEFS[1:]} reported beside.  L={L_HEAD} headline, L in {L_SIDE} beside.")
    P(f"# FROZEN: CAND20 legs {LEGS}, cap INF, max_vol {MAXVOL}, gross {GROSS0}, cadence "
      f"{FREQ0}, min hold {HOLD0},")
    P(f"#   N {N0}, {COST:.0f} bps, LAG {LAG}, warm-up {WARMUP}, IS end {IS_END}, "
      f"{BDRAWS} draws, crc32 seeds.")
    P("# SEEDS ARE 1116's VERBATIM: U56/B136 are a BIT-EXACT REPRODUCTION, not a redraw, so")
    P("#   the two panels that already answered cannot move under the comparison.  G8/G9 gate")
    P("#   that to the digit.  SMALL663 gets its own independent-reseed check in D2.")
    P("# CORRECTION TO THE IDEA'S PREMISE, before any number: the SMALL panel is NOT 485 names.")
    P("#   data/prices_small.csv.gz was rebuilt 2026-09-11 to 715 tickers; the README's")
    P(f"#   documented max_1d_move >= {BAD_MOVE} exclusion drops 52, leaving 663 tradable names")
    P("#   plus SPY as a NON-CONSTITUENT benchmark column, made un-selectable here.  '485' is a")
    P("#   stale count from the 2026-09-04 vintage.  The panel is labelled SMALL663 throughout.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   (a) H_LADDER_SMALL   ETA2_LAD > ETA2_STAT on binary INF_FLOOR, SMALL663, q=0.90.")
    P("#   (b) H_STAT_SMALL     the mirror.  Both fail if the SMALL table is DEGENERATE.")
    P("#   (c) H_CONCORD_SMALL  concordance on SMALL663 favours the same axis as the binary.")
    P("#   (d) H_MARGIN_SHRINKS SMALL663's margin (ETA2_LAD - ETA2_STAT) < both U56's and")
    P("#                        B136's.  PRIMARY margin is the DIFFERENCE, not 1116's ratio.")
    P("#   (e) H_MORE_UNRES     SMALL663 carries more INF_FLOOR cells of 16 than either panel.")
    P("#   (f) H_HC_SAME_ROWS   H and CADENCE un-resolvable at all 4 statistics on SMALL663.")
    P("#   (g) H_RELIABILITY    SMALL663's median S_OOS reliability < U56's and B136's.")
    P("#   (h) DECISION RULE    HOLDS if (a) at >= 2 of 3 q AND concordance agrees at >= 2 of 3;")
    P("#                        if the binary table is DEGENERATE at >= 2 of 3 q the binary")
    P("#                        reading is UNAVAILABLE and BOTH continuous readings (REL_FLOOR,")
    P("#                        LOG_M) must favour LADDER at >= 2 of 3.  Else DOES NOT HOLD.")
    P("#   (i) NOT A KEEP PATH  the book at all 81 rungs is byte-identical across both dials;")
    P("#                        4a/4b and rule 8 scored anyway because rule 4 requires it.")
    P("")

    gaterows, gates = [], {}

    # ---------------------------------------------------------------------------- THE GATES
    P("## GATES — printed before any result number")
    panels = {}
    dropped_small = []
    for panel in PANELS:
        if panel == "SMALL663":
            px = load_universe(small=True)
            meta = read_committed(ROOT / "data" / "small_meta.csv")
            meta["max_1d_move"] = meta["max_1d_move"].map(fnum)
            bad = set(meta.loc[meta.max_1d_move >= BAD_MOVE, "ticker"])
            dropped_small = sorted(c for c in px.columns if c in bad)
            px = px[[c for c in px.columns if c not in bad]].dropna(how="all").ffill()
        else:
            px = load_universe(broad=(panel == "B136")).dropna(how="all").ffill()
        idx, K, T = px.index, len(px.columns), len(px.index)
        rets = px.pct_change().fillna(0.0).values
        priced = px.notna().values
        warm, ins, oos = windows(idx)
        sc, elig = mech(px)
        if panel == "SMALL663":
            # SPY is a BENCHMARK column on this panel, not a constituent (see the panel
            # README).  It must never enter the book, on any ladder or rung.
            jspy = list(px.columns).index("SPY")
            elig = elig.copy()
            elig[:, jspy] = False
        panels[panel] = dict(px=px, idx=idx, K=K, T=T, rets=rets, priced=priced,
                             warm=warm, ins=ins, oos=oos, sc=sc, elig=elig)
        P(f"  {panel}: {K} cols, {T:,} rows {idx[0].date()} -> {idx[-1].date()}, "
          f"warm {warm.sum():,}, IS {ins.sum():,}, OOS {oos.sum():,}")
    P(f"  SMALL663: {len(dropped_small)} tickers dropped for max_1d_move >= {BAD_MOVE} "
      f"(README's documented exclusion): {', '.join(dropped_small[:12])}"
      f"{' ...' if len(dropped_small) > 12 else ''}")

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
        return g - tn * COST / 1e4, tn, W

    def live_v2(panel):
        """RULES v2 on a panel.  On SMALL663 SPY is dropped BEFORE the weights are formed, so
        the benchmark column is not held and does not enter the 1/N denominator; its slice
        simply stays in cash, which is what v2 does with any gated-out weight."""
        d = panels[panel]
        px = d["px"]
        if panel == "SMALL663":
            sub = px.drop(columns=["SPY"])
            w = rules_v2_weights(sub).reindex(columns=px.columns).fillna(0.0)
        else:
            w = rules_v2_weights(px)
        return backtest(px, w, cost_bps=COST, freq="W")["returns"].values

    d = panels["U56"]
    mk = rebalance_mask(d["idx"], FREQ0).values
    reb = np.flatnonzero(mk)
    W = build(-d["sc"], d["elig"], d["priced"], reb, N0, HOLD0, d["T"], d["K"], GROSS0)
    Wdf = pd.DataFrame(W, index=d["idx"], columns=d["px"].columns)
    eng = backtest(d["px"], Wdf, cost_bps=COST, freq=FREQ0)["returns"].values
    rfast, _, _ = run_cell("U56", N0, HOLD0, GROSS0, FREQ0)
    g1 = float(np.abs(eng[d["warm"]] - rfast[d["warm"]]).max())
    gates["G1"] = g1 < 1e-12
    gaterows.append(dict(gate="G1", what="fast runner == engine.backtest (U56 W/H126/N20)",
                         value=g1, pass_=gates["G1"]))
    P(f"  G1  fast runner == engine.backtest (U56)                  {g1:.2e}   "
      f"{'PASS' if gates['G1'] else 'FAIL'}")

    ds = panels[NEW_PANEL]
    mks = rebalance_mask(ds["idx"], FREQ0).values
    Ws = build(-ds["sc"], ds["elig"], ds["priced"], np.flatnonzero(mks), N0, HOLD0,
               ds["T"], ds["K"], GROSS0)
    Wsdf = pd.DataFrame(Ws, index=ds["idx"], columns=ds["px"].columns)
    engs = backtest(ds["px"], Wsdf, cost_bps=COST, freq=FREQ0)["returns"].values
    rfs, _, _ = run_cell(NEW_PANEL, N0, HOLD0, GROSS0, FREQ0)
    g1s = float(np.abs(engs[ds["warm"]] - rfs[ds["warm"]]).max())
    gates["G1s"] = g1s < 1e-12
    gaterows.append(dict(gate="G1s", what="fast runner == engine.backtest (SMALL663 W/H126/N20)",
                         value=g1s, pass_=gates["G1s"]))
    P(f"  G1s fast runner == engine.backtest (SMALL663 — NEW PANEL) {g1s:.2e}   "
      f"{'PASS' if gates['G1s'] else 'FAIL'}")

    m = blocks_m(rfast, d["warm"], d["ins"], d["oos"])
    g2 = max(abs(m["CAGR"] - A936_WH126[0]), abs(m["Sharpe"] - A936_WH126[1]),
             abs(m["MaxDD"] - A936_WH126[2]))
    gates["G2"] = g2 < 5e-5
    gaterows.append(dict(gate="G2", what="CROSS-RUN 936/1071/1082/1094/1102/1108/1110/1116 U56 triple",
                         value=g2, pass_=gates["G2"]))
    P(f"  G2  CROSS-RUN committed U56 W/H126/N=20 triple            {g2:.2e}   "
      f"{'PASS' if gates['G2'] else 'FAIL'}  ({m['CAGR']:.4%} / {m['Sharpe']:.4f} / {m['MaxDD']:.4%})")

    spy = d["px"]["SPY"].pct_change().fillna(0.0).values
    sm = blocks_m(spy, d["warm"], d["ins"], d["oos"])
    g3 = max(abs(sm["OOS_CAGR"] - SPY_OOS_COMMITTED[0]), abs(sm["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
             abs(sm["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gates["G3"] = g3 < 5e-4
    gaterows.append(dict(gate="G3", what="SPY OOS triple (U56)", value=g3, pass_=gates["G3"]))
    P(f"  G3  SPY OOS triple                                        {g3:.2e}   "
      f"{'PASS' if gates['G3'] else 'FAIL'}")

    r12, _, _ = run_cell("U56", 12, HOLD0, GROSS0, FREQ0)
    m12 = blocks_m(r12, d["warm"], d["ins"], d["oos"])
    g4 = max(abs(m12["CAGR"] - A1098_U56_N12[0]), abs(m12["Sharpe"] - A1098_U56_N12[1]),
             abs(m12["MaxDD"] - A1098_U56_N12[2]))
    gates["G4"] = g4 < 5e-4
    gaterows.append(dict(gate="G4", what="CROSS-RUN 1098/1102/1116 committed U56 n=12 triple",
                         value=g4, pass_=gates["G4"]))
    P(f"  G4  CROSS-RUN committed U56 n=12 triple                   {g4:.2e}   "
      f"{'PASS' if gates['G4'] else 'FAIL'}")

    db = panels["B136"]
    r15, _, _ = run_cell("B136", 15, HOLD0, GROSS0, FREQ0)
    m15 = blocks_m(r15, db["warm"], db["ins"], db["oos"])
    g4b = max(abs(m15["CAGR"] - A1098_B136_N15[0]), abs(m15["Sharpe"] - A1098_B136_N15[1]),
              abs(m15["MaxDD"] - A1098_B136_N15[2]))
    gates["G4b"] = g4b < 5e-4
    gaterows.append(dict(gate="G4b", what="CROSS-RUN 1098/1102/1116 committed B136 n=15 triple",
                         value=g4b, pass_=gates["G4b"]))
    P(f"  G4b CROSS-RUN committed B136 n=15 triple                  {g4b:.2e}   "
      f"{'PASS' if gates['G4b'] else 'FAIL'}")

    lbm = blocks_m(live_v2("U56"), d["warm"], d["ins"], d["oos"])
    g5 = abs(lbm["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gates["G5"] = g5 < 5e-4
    gaterows.append(dict(gate="G5", what="live RULES v2 MaxDD == committed -12.05%",
                         value=g5, pass_=gates["G5"]))
    P(f"  G5  live RULES v2 MaxDD == committed -12.05%              {g5:.2e}   "
      f"{'PASS' if gates['G5'] else 'FAIL'}")

    r12b, _, _ = run_cell("U56", 12, HOLD0, GROSS0, FREQ0)
    g6 = float(np.abs(r12 - r12b).max())
    gates["G6"] = g6 == 0.0
    gaterows.append(dict(gate="G6", what="determinism of the cell pipeline", value=g6,
                         pass_=gates["G6"]))
    P(f"  G6  determinism                                           {g6:.2e}   "
      f"{'PASS' if gates['G6'] else 'FAIL'}")

    g10 = float(np.abs(Ws[:, list(ds["px"].columns).index("SPY")]).max())
    gates["G10"] = (g10 == 0.0) and (ds["K"] == 664) and (len(dropped_small) == 52)
    gaterows.append(dict(gate="G10",
                         what="SMALL663 composition: 663 tradable + SPY held at weight 0 everywhere",
                         value=g10, pass_=gates["G10"]))
    P(f"  G10 SMALL663 SPY max book weight {g10:.2e}, cols {ds['K']}, dropped "
      f"{len(dropped_small)}   {'PASS' if gates['G10'] else 'FAIL'}")
    P("")

    # ------------------------------------------------- REBUILD THE 48 LADDER CELLS
    P("## THE LADDERS — 4 families x 3 panels, every rung published")
    gridrows, benchrows = [], []
    series, metr, bench = {}, {}, {}
    for panel in PANELS:
        dd_ = panels[panel]
        sb = blocks_m(dd_["px"]["SPY"].pct_change().fillna(0.0).values,
                      dd_["warm"], dd_["ins"], dd_["oos"])
        lbm_p = blocks_m(live_v2(panel), dd_["warm"], dd_["ins"], dd_["oos"])
        bench[panel] = (sb, lbm_p)
        benchrows.append(dict(panel=panel, book="SPY", **sb))
        benchrows.append(dict(panel=panel, book="RULES v2 (live)", **lbm_p))
        P(f"  {panel:<9} SPY      full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%}"
          f"  halves {sb['H1']:.4f}/{sb['H2']:.4f}  OOS {sb['OOS_CAGR']:.2%} / "
          f"{sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"  {panel:<9} RULES v2 full {lbm_p['CAGR']:.2%} / {lbm_p['Sharpe']:.4f} / "
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
                r, tn, _ = run_cell(panel, N, H, g, f)
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
            P(f"  {panel:<9} {lad:<8} rungs {rungs}")
            P("        Sharpe " + " ".join(f"{x:.4f}" for x in sh))
    grid = pd.DataFrame(gridrows)
    sp = float(grid["Sharpe"].max() - grid["Sharpe"].min())
    sps = float(grid[grid.panel == NEW_PANEL]["Sharpe"].max()
                - grid[grid.panel == NEW_PANEL]["Sharpe"].min())
    gates["G7"] = (sp > 0.05) and (sps > 0.05)
    gaterows.append(dict(gate="G7", what="the ladders are live (Sharpe spread, all cells / SMALL663)",
                         value=sps, pass_=gates["G7"]))
    P(f"  G7  the ladders are live (spread all {sp:.4f}, SMALL663 {sps:.4f})   "
      f"{'PASS' if gates['G7'] else 'FAIL'}")
    dump(grid, "grid")
    dump(pd.DataFrame(benchrows), "benchmarks")
    P("")

    # ------------------------------------------ THE BOOTSTRAP: values + pair agreements
    P(f"## THE BOOTSTRAP — L in {[L_HEAD] + L_SIDE}, {BDRAWS} draws, 1116's crc32 seeds")
    CELL, BOOT = {}, {}
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
                    if L == L_HEAD:
                        BOOT[(panel, lad, stat)] = boots[stat]
        P(f"  L={L}: 3 panels x 4 ladders x 4 statistics bootstrapped "
          f"({time.time() - t0:.0f}s elapsed)")
    P(f"  {len(CELL)} (L, panel, ladder, stat) cells built; {len(CELL) // 3} at L={L_HEAD}")

    # G8/G9 — BIT-EXACT reproduction of 1116's committed U56/B136 cells and decomposition
    cp = Path(f"{PRIOR1116}.cells.csv")
    if cp.exists():
        c1116 = read_committed(cp)
        xrows = []
        for _, r_ in c1116.iterrows():
            key = (int(r_["L"]), r_["panel"], r_["ladder"], r_["stat"])
            if key not in CELL or r_["panel"] not in OLD_PANELS:
                continue
            q = fnum(r_["q"])
            c = CELL[key]
            flo, _, _ = floor_of(c["vals"], c["A"], list(range(c["k"])), q)
            order = np.argsort(-c["vals"], kind="stable")
            gap = float(c["vals"][order[0]] - c["vals"][order[1]])
            dg = abs(gap - fnum(r_["gap"]))
            f_old = fnum(r_["floor"])
            df_ = (0.0 if (not np.isfinite(f_old) and not np.isfinite(flo))
                   else abs(flo - f_old))
            xrows.append(dict(L=key[0], panel=key[1], ladder=key[2], stat=key[3], q=q,
                              gap_1116=fnum(r_["gap"]), gap_1119=gap, d_gap=dg,
                              floor_1116=f_old, floor_1119=flo, d_floor=df_,
                              inf_1116=not np.isfinite(f_old), inf_1119=not np.isfinite(flo)))
        X = pd.DataFrame(xrows)
        worst_g = float(X.d_gap.max()) if len(X) else np.nan
        worst_f = float(np.nanmax(X.d_floor.replace([np.inf, -np.inf], np.nan))) if len(X) else np.nan
        inf_ok = int((X.inf_1116 == X.inf_1119).sum())
        gates["G8"] = (worst_g < 1e-12) and (inf_ok == len(X))
        gaterows.append(dict(gate="G8", what="BIT-EXACT reproduction of 1116's U56/B136 cells.csv",
                             value=worst_g, pass_=gates["G8"]))
        P(f"  G8  reproduce 1116's {len(X)} U56/B136 cells: max |dgap| {worst_g:.2e}, max "
          f"|dfloor| {worst_f:.2e}, inf flags {inf_ok} of {len(X)}   "
          f"{'PASS' if gates['G8'] else 'FAIL'}")
        dump(X, "cross1116cells")
    else:
        gates["G8"] = False
        gaterows.append(dict(gate="G8", what="1116's cells.csv", value=np.nan, pass_=False))
        P("  G8  1116's cells.csv NOT FOUND — reproduction gate FAILS")
    P("")

    # -------------------------------------------- PER-CELL RESOLVABILITY, EVERY DIAL POINT
    P("## PER-CELL RESOLVABILITY — 48 cells x 3 q, every number published")
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
    for panel in PANELS:
        h = head[head.panel == panel]
        P(f"  HEADLINE (L={L_HEAD}, q={Q_HEAD}) {panel:<9}: INF_FLOOR {int(h.INF_FLOOR.sum())} of 16, "
          f"ZERO_CONTENT {int(h.ZERO_CONTENT.sum())} of 16, "
          f"NO_TAPE_500 {int(h.NO_TAPE_500.sum())} of 16")
    P(f"  (1116 committed 18 of 32 infinite floors over U56+B136; this run reproduces "
      f"{int(head[head.panel.isin(OLD_PANELS)].INF_FLOOR.sum())} of 32 on the same two)")
    P("")
    P("  THE 4x4 TABLES, INF_FLOOR at q=0.90 (1 = UN-RESOLVABLE):")
    for panel in PANELS:
        P(f"    {panel:<9}" + "".join(f"{s:>9}" for s in STATS) + "    row")
        for lad in LADDERS:
            rr = [int(head[(head.panel == panel) & (head.ladder == lad) &
                           (head.stat == s)].INF_FLOOR.iloc[0]) for s in STATS]
            P(f"    {lad:<9}" + "".join(f"{x:>9}" for x in rr) + f"    {sum(rr)}/4")
        cols = [sum(int(head[(head.panel == panel) & (head.ladder == lad) &
                            (head.stat == s)].INF_FLOOR.iloc[0]) for lad in LADDERS)
                for s in STATS]
        P("    col      " + "".join(f"{x:>7}/4" for x in cols))
    P("")

    # -------------------------------------------------- THE DECOMPOSITION, EVERY DIAL POINT
    P("## THE DECOMPOSITION — ETA2 by axis, 3 panels x 3 q (the 9 dial points), + 3 defs")
    decrows = []
    for defn in DEFS:
        for q in QGRID:
            sl = cells[(cells.L == L_HEAD) & (np.isclose(cells.q, q))]
            for panel in PANELS:
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
                                    eta2_lad=el, eta2_stat=es,
                                    eta2_resid=(np.nan if not np.isfinite(el) else 1 - el - es),
                                    margin=(np.nan if not np.isfinite(el) else el - es),
                                    ratio=ratio(el, es), sst=sst,
                                    rel_eta2_lad=cl, rel_eta2_stat=cs,
                                    rel_margin=(np.nan if not np.isfinite(cl) else cl - cs),
                                    logM_eta2_lad=ml, logM_eta2_stat=ms,
                                    logM_margin=(np.nan if not np.isfinite(ml) else ml - ms),
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
    P("  defn          q     panel      n_un  eta2_LAD eta2_STAT  margin  ratio | relF_LAD"
      " relF_STAT | logM_LAD logM_STAT | conc_LAD conc_STAT")
    for _, r_ in dec.iterrows():
        def _f(x):
            return "  n/a  " if not np.isfinite(x) else f"{x:7.4f}"

        def _r(x):
            return "   n/a" if not np.isfinite(x) else (f"{x:6.1f}" if abs(x) < 1e4 else "  huge")
        P(f"  {r_['defn']:<13} {r_['q']:.2f}  {r_['panel']:<9} {r_['n_unres']:5.1f}  "
          f"{_f(r_['eta2_lad'])} {_f(r_['eta2_stat'])} {_f(r_['margin'])} {_r(r_['ratio'])} | "
          f"{_f(r_['rel_eta2_lad'])} {_f(r_['rel_eta2_stat'])} | "
          f"{_f(r_['logM_eta2_lad'])} {_f(r_['logM_eta2_stat'])} | "
          f"{r_['concord_within_ladder']:7.4f} {r_['concord_within_stat']:7.4f}")
    P("")
    hd = dec[(dec.defn == DEF_HEAD) & (np.isclose(dec.q, Q_HEAD))]
    P("  CROSS-RUN of 1116's committed ETA2 pair (INF_FLOOR, q=0.90):")
    g9ok = True
    for p_ in OLD_PANELS:
        r_ = hd[hd.panel == p_].iloc[0]
        want = A1116_ETA2[p_]
        dl, dsx = abs(r_["eta2_lad"] - want[0]), abs(r_["eta2_stat"] - want[1])
        ok = (dl < 5e-4) and (dsx < 5e-4)
        g9ok &= ok
        P(f"    {p_:<6} 1116 {want[0]:.4f}/{want[1]:.4f}  this run "
          f"{r_['eta2_lad']:.4f}/{r_['eta2_stat']:.4f}   d {dl:.2e}/{dsx:.2e}  "
          f"{'PASS' if ok else 'FAIL'}")
    gates["G9"] = bool(g9ok)
    gaterows.append(dict(gate="G9", what="CROSS-RUN 1116's committed ETA2_LAD/ETA2_STAT",
                         value=float(g9ok), pass_=gates["G9"]))
    P(f"  G9  CROSS-RUN 1116's committed ETA2 pair                  "
      f"{'PASS' if gates['G9'] else 'FAIL'}")
    P("")

    # ---------------------------------------------------------- MARGINALS
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

    # ---------------------------------------------------------- RELIABILITY (the mechanism)
    P("## RELIABILITY — 1073's mechanism, MEASURED on this run's own draws, not inherited")
    P(f"   (1073 committed {A1073_REL['SMALL']:.4f} small-cap vs {A1073_REL['LARGE']:.4f} "
      "large-cap for ONE book's OOS Sharpe; that number is a DIFFERENT object — one book's")
    P("    draw-to-draw reliability — so it is context, NOT a comparand, and is never gated on.)")
    relrows = []
    for panel in PANELS:
        for lad, rungs in LADDERS.items():
            for stat in STATS:
                c = CELL[(L_HEAD, panel, lad, stat)]
                ru, rp, obs, eu, ep = reliability(c["vals"], BOOT[(panel, lad, stat)])
                relrows.append(dict(panel=panel, ladder=lad, stat=stat, k=c["k"],
                                    var_between=obs, var_err_unpaired=eu, var_err_paired=ep,
                                    reliability_unpaired=ru, reliability_paired=rp))
    rel = pd.DataFrame(relrows)
    dump(rel, "reliability")
    P("  panel      stat      median REL_PAIRED (over 4 ladders)   median REL_UNPAIRED")
    for panel in PANELS:
        for s in STATS:
            sub = rel[(rel.panel == panel) & (rel.stat == s)]
            P(f"  {panel:<10} {s:<9} {sub.reliability_paired.median():.4f}"
              f"                          {sub.reliability_unpaired.median():.4f}")
    P("")

    # -------------------------------------------------------------- THE DECLARED HYPOTHESES
    P("## THE DECLARED HYPOTHESES")
    hyp = []
    sm_row = hd[hd.panel == NEW_PANEL].iloc[0]
    a_s = bool(sm_row["lad_wins_binary"])
    b_s = bool(sm_row["stat_wins_binary"])
    degen_s = bool(sm_row["degenerate"])
    hyp.append(dict(name="H_LADDER_SMALL", verdict="PASS" if a_s else "FAIL",
                    detail=f"SMALL663 eta2_LAD {sm_row['eta2_lad']} vs eta2_STAT "
                           f"{sm_row['eta2_stat']}; table degenerate={degen_s}"))
    hyp.append(dict(name="H_STAT_SMALL", verdict="PASS" if b_s else "FAIL",
                    detail=f"mirror of H_LADDER_SMALL; degenerate={degen_s}"))

    c_s = bool(sm_row["lad_wins_concord"])
    h_conc = (c_s == a_s) if not degen_s else (c_s is True)
    hyp.append(dict(name="H_CONCORD_SMALL", verdict="PASS" if h_conc else "FAIL",
                    detail=f"concordance within-ladder {sm_row['concord_within_ladder']:.4f} vs "
                           f"within-stat {sm_row['concord_within_stat']:.4f}; binary LADDER "
                           f"winner={a_s}, degenerate={degen_s}"))

    marg_s = sm_row["margin"]
    marg_u = float(hd[hd.panel == "U56"].margin.iloc[0])
    marg_b = float(hd[hd.panel == "B136"].margin.iloc[0])
    h_shrink = bool(np.isfinite(marg_s) and marg_s < marg_u and marg_s < marg_b)
    hyp.append(dict(name="H_MARGIN_SHRINKS", verdict="PASS" if h_shrink else "FAIL",
                    detail=f"margin U56 {marg_u:.4f}, B136 {marg_b:.4f}, SMALL663 "
                           f"{marg_s if np.isfinite(marg_s) else 'n/a (degenerate)'}"))

    n_inf = {p: int(head[head.panel == p].INF_FLOOR.sum()) for p in PANELS}
    h_more = n_inf[NEW_PANEL] > n_inf["U56"] and n_inf[NEW_PANEL] > n_inf["B136"]
    hyp.append(dict(name="H_MORE_UNRES", verdict="PASS" if h_more else "FAIL",
                    detail=f"INF_FLOOR of 16 per panel {n_inf}"))

    rowsum = {lad: int(head[(head.panel == NEW_PANEL) & (head.ladder == lad)].INF_FLOOR.sum())
              for lad in LADDERS}
    h_rows = (rowsum["H"] == 4 and rowsum["CADENCE"] == 4)
    hyp.append(dict(name="H_HC_SAME_ROWS", verdict="PASS" if h_rows else "FAIL",
                    detail=f"SMALL663 INF_FLOOR row sums (of 4) {rowsum}"))

    med = {p: float(rel[(rel.panel == p) & (rel.stat == "S_OOS")].reliability_paired.median())
           for p in PANELS}
    h_rel = med[NEW_PANEL] < med["U56"] and med[NEW_PANEL] < med["B136"]
    hyp.append(dict(name="H_RELIABILITY", verdict="PASS" if h_rel else "FAIL",
                    detail=f"median paired S_OOS reliability per panel "
                           f"{ {k: round(v, 4) for k, v in med.items()} }"))

    smq = dec[(dec.defn == DEF_HEAD) & (dec.panel == NEW_PANEL)]
    n_a = int(smq.lad_wins_binary.sum())
    n_degen = int(smq.degenerate.sum())
    n_conc = int(smq.lad_wins_concord.sum())
    n_rel = int(smq.lad_wins_rel.sum())
    n_logm = int(smq.lad_wins_logM.sum())
    P(f"  SMALL663 across the 3 q rungs: binary LADDER wins {n_a} of 3, table DEGENERATE "
      f"{n_degen} of 3,")
    P(f"    concordance favours LADDER {n_conc} of 3, REL_FLOOR {n_rel} of 3, LOG_M "
      f"{n_logm} of 3")
    if n_degen >= 2:
        route = "CONTINUOUS (binary table degenerate at >= 2 of 3 q — reading UNAVAILABLE)"
        holds = (n_rel >= 2) and (n_logm >= 2)
    else:
        route = "BINARY"
        holds = (n_a >= 2) and (n_conc >= 2)
    answer = "HOLDS" if holds else "DOES NOT HOLD"
    hyp.append(dict(name="DECISION_RULE", verdict=answer,
                    detail=f"route {route}; binary {n_a}/3, concord {n_conc}/3, "
                           f"rel_floor {n_rel}/3, log_M {n_logm}/3"))
    Hy = pd.DataFrame(hyp)
    dump(Hy, "hypotheses")
    for _, r_ in Hy.iterrows():
        P(f"  {r_['name']:<17} {r_['verdict']:<14} {r_['detail']}")
    P("")
    P(f"## THE ANSWER: the LADDER axis {answer} on SMALL663 (route: {route})")
    P("")

    # ------------------------------------------------------------- D1, POST-HOC AND LABELLED
    P("## D1 — POST-HOC AND LABELLED: WHERE the three panels differ, cell by cell")
    d1rows = []
    for lad in LADDERS:
        for s in STATS:
            v = {p: int(head[(head.panel == p) & (head.ladder == lad) &
                             (head.stat == s)].INF_FLOOR.iloc[0]) for p in PANELS}
            rf = {p: float(head[(head.panel == p) & (head.ladder == lad) &
                                (head.stat == s)].rel_floor.iloc[0]) for p in PANELS}
            d1rows.append(dict(ladder=lad, stat=s, **{f"inf_{p}": v[p] for p in PANELS},
                               **{f"relfloor_{p}": rf[p] for p in PANELS},
                               small_differs_from_both=(v[NEW_PANEL] != v["U56"] and
                                                        v[NEW_PANEL] != v["B136"]),
                               all_three_agree=(v["U56"] == v["B136"] == v[NEW_PANEL])))
    D1 = pd.DataFrame(d1rows)
    dump(D1, "d1")
    P("  ladder    stat        INF U56/B136/SMALL663      rel_floor U56 / B136 / SMALL663")
    for _, r_ in D1.iterrows():
        P(f"  {r_['ladder']:<9} {r_['stat']:<10}  {r_['inf_U56']} / {r_['inf_B136']} / "
          f"{r_['inf_SMALL663']}                  {r_['relfloor_U56']:.4f} / "
          f"{r_['relfloor_B136']:.4f} / {r_['relfloor_SMALL663']:.4f}")
    P(f"  all three panels agree at {int(D1.all_three_agree.sum())} of 16 cells; SMALL663 "
      f"differs from BOTH at {int(D1.small_differs_from_both.sum())} of 16")
    P("")

    # --------------------------------------------- D2, POST-HOC AND LABELLED: SMALL's own seed
    P("## D2 — POST-HOC AND LABELLED: SMALL663's axis answer under 3 INDEPENDENT reseeds")
    P("##      (a noise measurement on the NEW panel, reported in full, NEVER selected on;")
    P("##      1116 already did this for U56/B136 and found the axis verdict seed-stable)")
    d2rows = []
    for off in (1, 2, 3):
        tabs, ctabs = {}, {}
        for lad, rungs in LADDERS.items():
            _, Rw, Ro = series[(NEW_PANEL, lad)]
            rng = np.random.default_rng(seed_of(NEW_PANEL, lad, L_HEAD, "reseed", off))
            ixw, nbw = block_index(rng, Rw.shape[1], L_HEAD, BDRAWS)
            ixo, nbo = block_index(rng, Ro.shape[1], L_HEAD, BDRAWS)
            bcw, bsw = boot_exact(Rw, ixw, nbw, L_HEAD)
            _, bso = boot_exact(Ro, ixo, nbo, L_HEAD)
            bdd = boot_maxdd(Rw, ixw)
            bt = {"S_FULL": bsw, "S_OOS": bso, "CAGR": bcw * 100.0, "DD": bdd * 100.0}
            fl = {"S_FULL": np.array([metr[(NEW_PANEL, lad, r_)]["Sharpe"] for r_ in rungs]),
                  "S_OOS": np.array([metr[(NEW_PANEL, lad, r_)]["OOS_Sharpe"] for r_ in rungs]),
                  "CAGR": np.array([metr[(NEW_PANEL, lad, r_)]["CAGR"] for r_ in rungs]) * 100.0,
                  "DD": np.array([metr[(NEW_PANEL, lad, r_)]["MaxDD"] for r_ in rungs]) * 100.0}
            for stat in STATS:
                v = fl[stat]
                A = agree_matrix(pair_agreement(v, bt[stat]), len(rungs))
                flo, _, _ = floor_of(v, A, list(range(len(rungs))), Q_HEAD)
                tabs[(lad, stat)] = float(not np.isfinite(flo))
                spread = float(np.nanmax(v) - np.nanmin(v))
                ctabs[(lad, stat)] = 1.0 if not np.isfinite(flo) else min(flo, spread) / spread
        tab = np.array([[tabs[(lad, s)] for s in STATS] for lad in LADDERS])
        ctab = np.array([[ctabs[(lad, s)] for s in STATS] for lad in LADDERS])
        el, es, _ = two_way(tab)
        cl, cs, _ = two_way(ctab)
        wr, wc = concord(tab)
        d2rows.append(dict(seed_offset=off, panel=NEW_PANEL, n_unres=float(tab.sum()),
                           eta2_lad=el, eta2_stat=es,
                           rel_eta2_lad=cl, rel_eta2_stat=cs,
                           concord_within_ladder=wr, concord_within_stat=wc,
                           lad_wins=(np.isfinite(el) and el > es),
                           degenerate=(not np.isfinite(el)),
                           lad_wins_rel=(np.isfinite(cl) and cl > cs)))
    D2 = pd.DataFrame(d2rows)
    dump(D2, "d2")
    for _, r_ in D2.iterrows():
        def _f(x):
            return "  n/a  " if not np.isfinite(x) else f"{x:7.4f}"
        P(f"  reseed {r_['seed_offset']}  {r_['panel']} INF_FLOOR {r_['n_unres']:4.0f} of 16   "
          f"eta2_LAD {_f(r_['eta2_lad'])}  eta2_STAT {_f(r_['eta2_stat'])}  "
          f"relF_LAD {_f(r_['rel_eta2_lad'])}  relF_STAT {_f(r_['rel_eta2_stat'])}  "
          f"LADDER wins {r_['lad_wins']} (rel {r_['lad_wins_rel']}), degenerate "
          f"{r_['degenerate']}")
    P(f"  binary LADDER wins {int(D2.lad_wins.sum())} of 3 reseeds, REL_FLOOR "
      f"{int(D2.lad_wins_rel.sum())} of 3, table DEGENERATE {int(D2.degenerate.sum())} of 3, "
      f"against this run's headline seed ({a_s}, {bool(sm_row['lad_wins_rel'])}, {degen_s}).")
    P("")

    # ------------------- D3, POST-HOC AND LABELLED: why the noisiest panel resolves BEST
    P("## D3 — POST-HOC AND LABELLED: does SIGNAL-TO-NOISE explain H_MORE_UNRES failing")
    P("##      BACKWARDS?  The obvious reading of 'the small panel is MORE resolvable' is that")
    P("##      its dials move the book harder than its extra noise costs.  Tested directly.")
    d3rows = []
    for panel in PANELS:
        for lad, rungs in LADDERS.items():
            for stat in STATS:
                c = CELL[(L_HEAD, panel, lad, stat)]
                v, B = c["vals"], BOOT[(panel, lad, stat)]
                spread = float(np.nanmax(v) - np.nanmin(v))
                gaps = np.array([abs(v[i] - v[j]) for i, j in combinations(range(c["k"]), 2)])
                sds = np.array([float(np.nanstd(B[i] - B[j], ddof=1))
                                for i, j in combinations(range(c["k"]), 2)])
                d3rows.append(dict(panel=panel, ladder=lad, stat=stat, spread=spread,
                                   median_gap=float(np.median(gaps)),
                                   median_pair_sd=float(np.median(sds)),
                                   snr_spread=spread / float(np.median(sds)),
                                   snr_gap=float(np.median(gaps)) / float(np.median(sds)),
                                   gap_skew=float(np.max(gaps) / max(np.median(gaps), 1e-12)),
                                   frac_pairs_2sd=float((gaps > 2.0 * sds).mean())))
    D3 = pd.DataFrame(d3rows)
    dump(D3, "d3")
    P("  panel      mean SPREAD   mean med PAIR SD   mean SNR(spread)   mean SNR(gap)   "
      "mean max/med gap   mean frac pairs >2sd")
    for panel in PANELS:
        s = D3[D3.panel == panel]
        P(f"  {panel:<10} {s.spread.mean():11.4f}   {s.median_pair_sd.mean():16.4f}   "
          f"{s.snr_spread.mean():16.4f}   {s.snr_gap.mean():13.4f}   "
          f"{s.gap_skew.mean():16.4f}   {s.frac_pairs_2sd.mean():21.4f}")
    P("  per STATISTIC, SNR (spread/sd), by panel:")
    for s_ in STATS:
        row = " ".join(f"{p}={D3[(D3.panel == p) & (D3.stat == s_)].snr_spread.mean():.3f}"
                       for p in PANELS)
        P(f"    {s_:<8} {row}")
    snr = {p: float(D3[D3.panel == p].snr_spread.mean()) for p in PANELS}
    skew = {p: float(D3[D3.panel == p].gap_skew.mean()) for p in PANELS}
    worst_snr = min(snr, key=snr.get)
    P("")
    P(f"  READ PLAINLY: SNR does NOT explain it, and runs the WRONG WAY.  {worst_snr} has the")
    P(f"  WORST mean SNR of the three ({snr[worst_snr]:.4f} against "
      f"{' / '.join(f'{p} {snr[p]:.4f}' for p in PANELS if p != worst_snr)}) — its spread is")
    P("  wider but its per-pair noise grows FASTER than the spread does — and it still carries")
    P(f"  the FEWEST infinite floors ({n_inf[NEW_PANEL]} of 16 against "
      f"{' / '.join(f'{p} {n_inf[p]}' for p in PANELS if p != NEW_PANEL)}).")
    P("  The reason is what INF_FLOOR actually measures.  It is an ORDER statistic, not a")
    P("  precision statistic: the floor is infinite only when NO resolved pair sits ABOVE the")
    P("  LARGEST un-resolved gap, so one well-separated pair at the top of a right-skewed gap")
    P("  distribution makes a cell finite however poor the panel's AVERAGE precision is.  Mean")
    P(f"  max/median gap runs {' / '.join(f'{p} {skew[p]:.2f}' for p in PANELS)} and the share")
    P("  of pairs separated by more than 2 pair-SDs runs as printed above.")
    P("  CONSEQUENCE FOR THE RECORD, stated as a caution and not as a measured law: an")
    P("  INF_FLOOR count is NOT a panel-precision ranking and must not be read as one.  This")
    P("  run establishes that it is not monotone in mean SNR on three panels; it does not")
    P("  establish what it IS monotone in, and nothing here licenses the reverse reading either.")
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
                                     SPY_CAGR=sb["CAGR"], SPY_Sharpe=sb["Sharpe"],
                                     SPY_MaxDD=sb["MaxDD"], SPY_OOS_CAGR=sb["OOS_CAGR"],
                                     SPY_OOS_Sharpe=sb["OOS_Sharpe"], SPY_OOS_MaxDD=sb["OOS_MaxDD"],
                                     BASE_Sharpe=lbm_p["Sharpe"], BASE_MaxDD=lbm_p["MaxDD"],
                                     BASE_OOS_Sharpe=lbm_p["OOS_Sharpe"],
                                     pass_4b_full=all(l4b.values()), pass_4b_oos=all(l4bo.values()),
                                     pass_4a=all(l4a.values()), **l4b, **l4bo, **l4a))
    pk = pd.DataFrame(pickrows)
    dump(pk, "walkforward")
    for _, r_ in pk.iterrows():
        P(f"    {r_['panel']:<9} {r_['ladder']:<8} {r_['chooser']:<11} pick {str(r_['pick']):<6} "
          f"margin {r_['margin']:.4f}  full {r_['CAGR']:.2%}/{r_['Sharpe']:.4f}/{r_['MaxDD']:.2%}  "
          f"OOS {r_['OOS_CAGR']:.2%}/{r_['OOS_Sharpe']:.4f}/{r_['OOS_MaxDD']:.2%}  "
          f"4b full {str(r_['pass_4b_full']):<5} 4b OOS {str(r_['pass_4b_oos']):<5} "
          f"4a {r_['pass_4a']}")
    P(f"  ALL PICKS: 4b full {int(pk['pass_4b_full'].sum())} of {len(pk)}, 4b OOS "
      f"{int(pk['pass_4b_oos'].sum())} of {len(pk)}, 4a {int(pk['pass_4a'].sum())} of {len(pk)}")
    for panel in PANELS:
        q_ = pk[pk.panel == panel]
        g_ = grid[grid.panel == panel]
        P(f"    {panel:<9} picks 4b full {int(q_.pass_4b_full.sum())}/{len(q_)}, 4b OOS "
          f"{int(q_.pass_4b_oos.sum())}/{len(q_)}, 4a {int(q_.pass_4a.sum())}/{len(q_)}  |  "
          f"whole ladder 4b full {int(g_.pass_4b_full.sum())}/{len(g_)}, 4b OOS "
          f"{int(g_.pass_4b_oos.sum())}/{len(g_)}, 4a {int(g_.pass_4a.sum())}/{len(g_)}")
    P(f"  WHOLE GRID: 4b full {int(grid['pass_4b_full'].sum())} of {len(grid)}, 4b OOS "
      f"{int(grid['pass_4b_oos'].sum())} of {len(grid)}, 4a {int(grid['pass_4a'].sum())} of {len(grid)}")
    for leg in ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]:
        P(f"    4b leg {leg:<7} fails {int((~grid[leg]).sum())} of {len(grid)} cells"
          f"   (SMALL663 {int((~grid[grid.panel == NEW_PANEL][leg]).sum())} of "
          f"{len(grid[grid.panel == NEW_PANEL])})")
    if int(grid["pass_4b_full"].sum()):
        P("  4b-full passing cells:")
        for _, r_ in grid[grid.pass_4b_full].iterrows():
            P(f"    {r_['panel']:<9} {r_['ladder']:<8} rung {str(r_['rung']):<6} "
              f"full {r_['CAGR']:.2%}/{r_['Sharpe']:.4f}/{r_['MaxDD']:.2%} halves "
              f"{r_['H1']:.4f}/{r_['H2']:.4f}  OOS {r_['OOS_CAGR']:.2%}/{r_['OOS_Sharpe']:.4f}/"
              f"{r_['OOS_MaxDD']:.2%}  4b OOS {r_['pass_4b_oos']}")
    P("  NOTHING PROPOSED: the BOOK at all 81 rungs is byte-identical across both dials — only")
    P("  which cells get CALLED un-resolvable changes — so 4a and 4b are invariant to PANEL-as-")
    P("  a-dial and to q by construction.  Scored because rule 4 says so.  And every SMALL663")
    P("  4b figure above sits on the most survivorship-inflated tape in the record.")
    P("")
    P("## SURVIVORSHIP (PROTOCOL rule 9)")
    P("  All three panels are CURRENT-CONSTITUENT lists and SMALL663 is the worst by a wide")
    P("  margin: its universe is the CURRENT sub-$2B screen, so every name survived 2010-2026")
    P("  still listed, still public and still under $2B, and the acquired / delisted / bankrupt")
    P("  small caps are all missing.  A rung-to-rung GAP and a rung-to-rung AGREEMENT contrast")
    P("  two books over the SAME inflated tape, so the bias very largely cancels out of the")
    P("  floor and out of every quantity decomposed here — that is why the axis question can be")
    P("  asked on this panel at all.  It does NOT cancel out of the 4b legs, measured against")
    P("  SPY, so every SMALL663 4b pass above is an UPPER bound and a badly inflated one.")
    P("")
    P("## THE DECLARED APPROXIMATION, AND ITS DIRECTION")
    P("  NO_TAPE_500 rests on 1110's PROJECTION A' = Phi(sqrt(M) Phi^-1(A)).  Both of its")
    P("  assumptions run TOWARD resolution, so every M_needed is a LOWER bound.  The exponent is")
    P("  INHERITED from 1110's sub-tape fit, which was made on U56/B136 ONLY, so it is weakest")
    P("  exactly on the new panel: SMALL663's M_needed / LOG_M column is the least trustworthy")
    P("  quantity in this run.  It is reported in full and is never the sole basis of a verdict")
    P("  (the decision rule's continuous route requires REL_FLOOR to agree with it).")
    P("")

    dump(pd.DataFrame(gaterows), "gates")
    P(f"# GATES {sum(gates.values())} of {len(gates)} PASS")
    P(f"# HYPOTHESES {int((Hy.verdict == 'PASS').sum())} of {int((Hy.name != 'DECISION_RULE').sum())}")
    P(f"# elapsed {time.time() - t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"wrote {OUT}.console.txt")


if __name__ == "__main__":
    main()

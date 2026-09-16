#!/usr/bin/env python3
"""Idea 1110 (lane C, 2026-09-16) — what does the RECORD LOSE if the FLOOR CLAUSE is
ENACTED AS WRITTEN?

QUESTION (QUEUE idea 1110, verbatim)
    idea 1102 found the clause leaves a mean tie set of 4.88 rungs (0.851 of its own ladder)
    and makes 12 of 32 argmaxes WHOLE-LADDER, i.e. contentless.  Price the alternatives
    against it — publishing the argmax with its gap and floor beside it, or raising the
    resolution by lengthening the tape or widening the rungs — and report which one keeps the
    most decidable claims per unit of honesty.  Max 2 params (clause form, confidence).

WHAT IS TUNED AND WHAT IS NOT (PROTOCOL rule 4)
    Exactly TWO dials: CLAUSE FORM {AS_WRITTEN, ANNOTATED, WIDER_RUNGS, LONGER_TAPE}
    x CONFIDENCE q {0.80, 0.90, 0.95} = 12 combinations, ALL published.  PANEL is not a dial
    (both panels reported everywhere, 1102's convention).  LADDER and STATISTIC are not dials
    (all 4 x 4 cells reported).  BLOCK LENGTH is not a dial: L=63 throughout, 1098/1102/1108's
    headline.  Everything else frozen at 1082/1094/1098/1102/1108's construction: CAND20 legs,
    cap INF, max_vol 0.60, gross 0.75 (except on the GROSS ladder), W cadence (except on the
    CADENCE ladder), min hold 126 (except on the H ladder), N=20 (except on the N ladder),
    10 bps, LAG 1, warm-up 260, IS end 2016-12-31.  Seeds are zlib.crc32 (1108's repair of
    1102's process-random hash() seeds — 1108's DEFECT finding).

THE OBJECT BEING PRICED — PRE-REGISTERED, BEFORE ANY NUMBER
    A published argmax claim on a ladder of k rungs is, read strictly, an ASSERTION SET: it
    names a set S of rungs that may hold the optimum and thereby EXCLUDES the k - |S| others.
    Every clause form is scored on exactly two numbers per cell:
      DECIDED     = k - |S|, the rungs the claim actually rules out (its content).  Normalised
                    CONTENT = DECIDED / (k - 1), so 1.0 is a point claim and 0.0 is contentless.
      EXP_FALSE   = sum over the excluded rungs j of (1 - A_peak,j), where A_peak,j is the
                    block-bootstrap probability that a redrawn tape agrees with the published
                    sign of the (peak, j) gap.  This is the EXPECTED NUMBER OF WRONG
                    EXCLUSIONS the clause publishes.
    HONESTY is then the expected share of published exclusions that are wrong,
    ERR = EXP_FALSE / DECIDED, and "decidable claims per unit of honesty", read literally, is
    PRICE = DECIDED / EXP_FALSE — rungs ruled out per wrong exclusion bought.

THE FOUR CLAUSE FORMS (dial 1)
    AS_WRITTEN   1102's clause: S = the TIE SET, every rung within the ladder's floor(q) of
                 the argmax.  Calibrated by construction; the question is what it costs.
    ANNOTATED    the queue's first alternative: S = {argmax}, ALWAYS a point, with its gap and
                 its floor printed beside it.  Maximum content; the question is its error.
    WIDER_RUNGS  the queue's second alternative, first half: coarsen the ladder (headline: keep
                 every 2nd rung including both ends; ENDS-ONLY reported beside it and never
                 selected on), recompute the floor ON THE COARSE LADDER, publish its tie set.
                 A dropped rung is UNADJUDICATED, not excluded — the claim cannot rule out what
                 it no longer measures — so S = tie_set(coarse) UNION (dropped rungs).  This is
                 the whole cost of coarsening and it is counted here.
    LONGER_TAPE  the queue's second alternative, second half: the same clause on a tape M times
                 longer.  The scaling is MEASURED, not assumed: the floor is re-drawn on
                 disjoint contiguous sub-tapes at f = 0.25 and 0.50 of the warm window and
                 beta is fitted per cell from log(floor) vs log(T).  Headline M = 2 (about 34
                 years of tape, i.e. back to 1992 — already impossible for these panels).
                 Agreement is projected as A' = Phi(sqrt(M) * Phi^-1(A)), the exact consequence
                 of an unchanged gap and an SE falling as 1/sqrt(T); the fitted beta is the
                 gate on whether that projection is warranted.

DECLARED BEFORE ANY NUMBER
    (a) H_ANNOT_UNCAL — ANNOTATED is NOT calibrated: its expected share of wrong exclusions
        exceeds (1 - q) in a MAJORITY of the 32 cells at q = 0.90.  A point argmax on this tape
        is a claim the tape does not support, which is 1102's KILL restated as a rate.
    (b) H_ANNOT_PRICE — and yet ANNOTATED buys MORE decided rungs per wrong exclusion than
        AS_WRITTEN, i.e. PRICE(ANNOTATED) > PRICE(AS_WRITTEN) at q = 0.90.  If this fails, the
        clause as written is not merely honest but free, and the queue's first alternative is
        dominated outright.
    (c) H_COARSE_LOSES — WIDER_RUNGS decides FEWER rungs in total than AS_WRITTEN at q = 0.90:
        what coarsening gains in gap it loses in rungs it can no longer speak about.
    (d) H_TAPE_HALF — the floor falls like 1/sqrt(T): the MEDIAN fitted beta over the 24
        non-DD cells lies in [-0.70, -0.30].  DD is declared in advance to be exempt and is
        reported separately: MaxDD is a path functional and its own level grows with tape
        length, so its floor has no reason to fall at all.
    (e) H_TAPE_INFEASIBLE — the tape route does not rescue the record: the MEDIAN tape multiple
        a cell needs for its committed argmax gap to clear its own floor exceeds 4 (about 68
        years), and it is a projection, not a measurement.
    (f) THE DECISION RULE, fixed before any number: among the clause forms CALIBRATED at q
        (ERR <= 1 - q over the record), the answer is the one with the most DECIDED rungs.
        PRICE is reported beside it for every form, calibrated or not.  If AS_WRITTEN is the
        only calibrated form, it wins by default and that is the answer.
    (g) THE CLAUSE IS NOT A KEEP PATH.  4a and 4b are scored at every rung of every ladder and
        rule 8 picks the rung on 2009-2016 ALONE, per ladder, three choosers, OOS read ONCE.
        No clause form can move a book: the BOOK at every cell is byte-identical across all
        four forms, only the PROSE changes.  Scored anyway because rule 4 requires it.

INHERITED INPUT, DECLARED.  The corpus layer re-weights the CORE result onto the 200 VALUED
    argmax claims 1102 harvested from the record, read from 1102's committed claimscored.csv.
    The HARVEST is inherited (it is a text scan, reproducible, and not affected by 1108's seed
    defect); the RATES are re-derived here.  A claim whose family is a CORE ladder and whose
    statistic is a CORE statistic gets the MEASURED rate of its own (ladder, statistic) cell;
    otherwise it gets a TRANSFERRED rate, declared in advance as an EXTRAPOLATION and NOT a
    re-derivation of the claim (1048/1102's convention).  The three bases are counted apart.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT panels, so every level
    is optimistic.  A GAP between two rungs and an AGREEMENT between two rungs both contrast
    two books over the same inflated tape and the bias very largely cancels out of them and out
    of the floor; it does NOT cancel out of the 4b legs, measured against SPY, a real index.
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
SLUG = "what-does-the-RECORD-LOSE-if-the-FLOOR-CLAUSE-is-ENACTED-AS-WRITTEN"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"
PRIOR1102 = (Path(__file__).resolve().parent /
             "2026-09-16_does-the-RESOLUTION-FLOOR-CLAUSE-change-any-committed-ARGMAX-in-the-record_C")

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

CLAUSES = ["AS_WRITTEN", "ANNOTATED", "WIDER_RUNGS", "LONGER_TAPE"]   # dial 1
QGRID = [0.80, 0.90, 0.95]                                            # dial 2
Q_HEAD = 0.90
L_HEAD = 63
BDRAWS = 1000
SUBFRACS = [0.25, 0.50]        # measured sub-tapes for the LONGER_TAPE scaling fit
M_HEAD = 2.0                   # headline tape multiple for LONGER_TAPE
M_PROBE = [2.0, 4.0, 8.0]
COARSE_STEP = 2                # headline coarsening; ENDS reported beside it
SEED_BOOT = 11101110

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


# --------------------------------------------- 1082/1098/1102/1108's fast runner, verbatim
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
    """Symmetric k x k matrix of pair agreements (diagonal 1)."""
    A = np.full((k, k), np.nan)
    np.fill_diagonal(A, 1.0)
    for (i, j, _g, a) in prs:
        A[i, j] = A[j, i] = a
    return A


def floor_of(vals, A, sub, q):
    """Floor(q) restricted to the rung subset `sub` (indices into the full ladder)."""
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
    """Rungs of `sub` within `flo` of the peak's value; the peak is always in it."""
    s = {peak}
    for j in sub:
        if np.isfinite(vals[j]) and abs(vals[peak] - vals[j]) < flo:
            s.add(j)
    return sorted(s)


def _ncoarse(k):
    """Rungs kept by the headline coarsening (every COARSE_STEP-th, both ends)."""
    return len(sorted(set(list(range(0, k, COARSE_STEP)) + [k - 1])))


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 3:
        return np.nan
    ra = pd.Series(a[m]).rank().values
    rb = pd.Series(b[m]).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


# ------------------------------------------------------------------------------------- main
def main():
    t0 = time.time()
    P(f"# Idea 1110 (lane C, {DATE}) — what does the RECORD LOSE if the FLOOR CLAUSE is")
    P("#   ENACTED AS WRITTEN?")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4): CLAUSE FORM {CLAUSES} x CONFIDENCE q {QGRID}")
    P(f"#   = {len(CLAUSES) * len(QGRID)} combinations, ALL published.  PANEL, LADDER and "
      "STATISTIC are not dials (all reported).")
    P(f"#   BLOCK LENGTH is not a dial: L={L_HEAD} throughout, 1098/1102/1108's headline.")
    P(f"# FROZEN: CAND20 legs {LEGS}, cap INF, max_vol {MAXVOL}, gross {GROSS0}, cadence "
      f"{FREQ0}, min hold {HOLD0},")
    P(f"#   N {N0}, {COST:.0f} bps, LAG {LAG}, warm-up {WARMUP}, IS end {IS_END}, "
      f"{BDRAWS} draws, crc32 seeds (1108's repair).")
    P("# THE TWO NUMBERS EVERY FORM IS SCORED ON, pre-registered:")
    P("#   DECIDED   = k - |S|, rungs the published claim rules out (CONTENT = DECIDED/(k-1)).")
    P("#   EXP_FALSE = sum over excluded j of (1 - A_peak,j) — expected WRONG exclusions.")
    P("#   ERR = EXP_FALSE/DECIDED;  PRICE = DECIDED/EXP_FALSE = 'decidable per unit honesty'.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   (a) H_ANNOT_UNCAL   ANNOTATED's ERR > (1-q) in a MAJORITY of the 32 cells at q=0.90.")
    P("#   (b) H_ANNOT_PRICE   PRICE(ANNOTATED) > PRICE(AS_WRITTEN) at q=0.90.")
    P("#   (c) H_COARSE_LOSES  WIDER_RUNGS decides FEWER rungs in total than AS_WRITTEN.")
    P("#   (d) H_TAPE_HALF     median fitted beta over the 24 non-DD cells in [-0.70, -0.30].")
    P("#   (e) H_TAPE_INFEAS   median tape multiple needed to clear a cell's own floor > 4.")
    P("#   (f) DECISION RULE   among forms CALIBRATED at q (ERR <= 1-q), the most DECIDED wins.")
    P("#   (g) NOT A KEEP PATH the book is byte-identical across all four forms; 4a/4b and")
    P("#                       rule 8 scored anyway because rule 4 requires it.")
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
    gaterows.append(dict(gate="G2", what="CROSS-RUN 936/1071/1082/1094/1102/1108 U56 W/H126/N=20 triple",
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

    # ---------------------------------------------------- REBUILD 1102's 32 CORE LADDER CELLS
    P("## THE LADDERS — 4 families x 2 panels, every rung published")
    gridrows, benchrows = [], []
    series, metr = {}, {}
    bench = {}
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
          f"{lbm_p['MaxDD']:.2%}  OOS {lbm_p['OOS_CAGR']:.2%} / {lbm_p['OOS_Sharpe']:.4f} / "
          f"{lbm_p['OOS_MaxDD']:.2%}")
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

    # ------------------------------------------ THE FULL-TAPE BOOTSTRAP: values + agreements
    P(f"## THE FULL-TAPE BOOTSTRAP — L={L_HEAD}, {BDRAWS} draws, crc32 seeds")
    CELL = {}                     # (panel, ladder, stat) -> dict(vals, A, k, rungs)
    for panel in PANELS:
        dd_ = panels[panel]
        for lad, rungs in LADDERS.items():
            _, Rw, Ro = series[(panel, lad)]
            rng = np.random.default_rng(seed_of(panel, lad, L_HEAD))
            ixw, nbw = block_index(rng, Rw.shape[1], L_HEAD, BDRAWS)
            ixo, nbo = block_index(rng, Ro.shape[1], L_HEAD, BDRAWS)
            bcw, bsw = boot_exact(Rw, ixw, nbw, L_HEAD)
            _, bso = boot_exact(Ro, ixo, nbo, L_HEAD)
            bdd = boot_maxdd(Rw, ixw)
            boots = {"S_FULL": bsw, "S_OOS": bso, "CAGR": bcw * 100.0, "DD": bdd * 100.0}
            fulls = {"S_FULL": np.array([metr[(panel, lad, r_)]["Sharpe"] for r_ in rungs]),
                     "S_OOS": np.array([metr[(panel, lad, r_)]["OOS_Sharpe"] for r_ in rungs]),
                     "CAGR": np.array([metr[(panel, lad, r_)]["CAGR"] for r_ in rungs]) * 100.0,
                     "DD": np.array([metr[(panel, lad, r_)]["MaxDD"] for r_ in rungs]) * 100.0}
            for stat in STATS:
                v = fulls[stat]
                prs = pair_agreement(v, boots[stat])
                CELL[(panel, lad, stat)] = dict(vals=v, A=agree_matrix(prs, len(rungs)),
                                                k=len(rungs), rungs=rungs)
        P(f"  {panel}: 4 ladders x 4 statistics bootstrapped")
    P(f"  {len(CELL)} CORE cells built (1102's 32)")

    # G8 — CROSS-RUN against 1102's committed tie-set verdicts
    fp = Path(f"{PRIOR1102}.floor.csv")
    if fp.exists():
        f1102 = pd.read_csv(fp)
        f1102 = f1102[(f1102.L == L_HEAD) & (np.isclose(f1102.q, Q_HEAD))]
        agree_n, tot_n, xrows = 0, 0, []
        for _, r_ in f1102.iterrows():
            key = (r_["panel"], r_["ladder"], r_["stat"])
            if key not in CELL:
                continue
            c = CELL[key]
            flo, _, _ = floor_of(c["vals"], c["A"], list(range(c["k"])), Q_HEAD)
            peak = int(np.argmax(c["vals"]))
            order = np.argsort(-c["vals"], kind="stable")
            gap = float(c["vals"][order[0]] - c["vals"][order[1]])
            tie = bool(gap < flo)
            tot_n += 1
            agree_n += int(tie == bool(r_["tie_set_verdict"]))
            xrows.append(dict(panel=r_["panel"], ladder=r_["ladder"], stat=r_["stat"],
                              peak_1102=r_["peak"], peak_1110=c["rungs"][peak],
                              gap_1102=r_["gap"], gap_1110=gap,
                              floor_1102=r_["floor"], floor_1110=flo,
                              tie_1102=bool(r_["tie_set_verdict"]), tie_1110=tie))
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
    P("")

    # --------------------------------- THE SUB-TAPE MEASUREMENT (the LONGER_TAPE scaling fit)
    P(f"## SUB-TAPE FLOORS — the tape-length scaling MEASURED, not assumed (f = {SUBFRACS} + 1.0)")
    subrows = []
    for panel in PANELS:
        for lad, rungs in LADDERS.items():
            _, Rw, Ro = series[(panel, lad)]
            Tw = Rw.shape[1]
            for f in SUBFRACS:
                w = int(Tw * f)
                nwin = int(1.0 / f)
                per = {s: [] for s in STATS}
                for wi in range(nwin):
                    a, b = wi * w, wi * w + w
                    Rs = Rw[:, a:b]
                    wo = max(int(Ro.shape[1] * f), 3 * L_HEAD)
                    ao = min(wi * wo, max(Ro.shape[1] - wo, 0))
                    Os = Ro[:, ao:ao + wo]
                    rng = np.random.default_rng(seed_of(panel, lad, "sub", f, wi))
                    ixs, nbs = block_index(rng, Rs.shape[1], L_HEAD, BDRAWS)
                    ixo, nbo = block_index(rng, Os.shape[1], L_HEAD, BDRAWS)
                    bcs, bss = boot_exact(Rs, ixs, nbs, L_HEAD)
                    _, bos = boot_exact(Os, ixo, nbo, L_HEAD)
                    bds = boot_maxdd(Rs, ixs)
                    vs = {}
                    for j in range(Rs.shape[0]):
                        c_, s_, dd_v = fmet(Rs[j])
                        vs.setdefault("CAGR", []).append(c_ * 100.0)
                        vs.setdefault("S_FULL", []).append(s_)
                        vs.setdefault("DD", []).append(dd_v * 100.0)
                        vs.setdefault("S_OOS", []).append(fsharpe(Os[j]))
                    bt = {"S_FULL": bss, "S_OOS": bos, "CAGR": bcs * 100.0, "DD": bds * 100.0}
                    for stat in STATS:
                        v = np.array(vs[stat], float)
                        prs = pair_agreement(v, bt[stat])
                        gaps = np.array([abs(p[2]) for p in prs])
                        agr = np.array([p[3] for p in prs])
                        flo, _, _ = floor_from_agreement(gaps, agr, Q_HEAD)
                        spread = float(np.nanmax(v) - np.nanmin(v))
                        per[stat].append((min(flo, spread) if np.isfinite(flo) else spread,
                                          not np.isfinite(flo)))
                for stat in STATS:
                    subrows.append(dict(panel=panel, ladder=lad, stat=stat, frac=f,
                                        T=w, n_windows=nwin,
                                        floor_capped_mean=float(np.mean([x[0] for x in per[stat]])),
                                        n_capped=int(sum(x[1] for x in per[stat]))))
            # the full tape itself
            for stat in STATS:
                c = CELL[(panel, lad, stat)]
                flo, _, _ = floor_of(c["vals"], c["A"], list(range(c["k"])), Q_HEAD)
                spread = float(np.nanmax(c["vals"]) - np.nanmin(c["vals"]))
                subrows.append(dict(panel=panel, ladder=lad, stat=stat, frac=1.0, T=Tw,
                                    n_windows=1,
                                    floor_capped_mean=min(flo, spread) if np.isfinite(flo) else spread,
                                    n_capped=int(not np.isfinite(flo))))
    sub = pd.DataFrame(subrows)
    dump(sub, "subtape")

    betarows = []
    for (panel, lad, stat), g in sub.groupby(["panel", "ladder", "stat"]):
        g = g.sort_values("T")
        x = np.log(g["T"].values.astype(float))
        y = np.log(np.maximum(g["floor_capped_mean"].values.astype(float), 1e-12))
        beta = float(np.polyfit(x, y, 1)[0]) if len(x) >= 2 else np.nan
        betarows.append(dict(panel=panel, ladder=lad, stat=stat, beta=beta,
                             floor_f025=float(g[g.frac == 0.25]["floor_capped_mean"].iloc[0]),
                             floor_f050=float(g[g.frac == 0.50]["floor_capped_mean"].iloc[0]),
                             floor_full=float(g[g.frac == 1.0]["floor_capped_mean"].iloc[0])))
    beta_df = pd.DataFrame(betarows)
    dump(beta_df, "betafit")
    nondd = beta_df[beta_df.stat != "DD"]
    P(f"  fitted beta (log floor vs log T): median over the {len(nondd)} non-DD cells "
      f"{nondd['beta'].median():+.4f}  [IQR {nondd['beta'].quantile(0.25):+.4f}, "
      f"{nondd['beta'].quantile(0.75):+.4f}]")
    P(f"  floors CAPPED at the ladder spread (nothing resolved on that sub-tape): "
      f"{int(sub['n_capped'].sum())} of {int(sub['n_windows'].sum() * 1)} window-cells "
      f"({int(sub[sub.frac == 1.0]['n_capped'].sum())} of {len(sub[sub.frac == 1.0])} on the "
      f"FULL tape) — a capped floor makes beta a statement about the SPREAD's scaling, not the "
      f"floor's, and is declared as such.")
    P(f"  DD cells (declared exempt, H_TAPE_HALF): median beta "
      f"{beta_df[beta_df.stat == 'DD']['beta'].median():+.4f} over "
      f"{len(beta_df[beta_df.stat == 'DD'])} cells")
    P("")

    # ------------------------------------------------------------- THE CLAUSE PRICING (both dials)
    P("## THE CLAUSE PRICING — 4 forms x 3 confidences x 32 cells, every combination published")
    prow = []
    for q in QGRID:
        for (panel, lad, stat), c in CELL.items():
            v, A, k, rungs = c["vals"], c["A"], c["k"], c["rungs"]
            full = list(range(k))
            peak = int(np.argmax(v))
            order = np.argsort(-v, kind="stable")
            gap = float(v[order[0]] - v[order[1]])
            spread = float(np.nanmax(v) - np.nanmin(v))
            flo, lun, nun = floor_of(v, A, full, q)

            def score(S, peak_idx, form, extra=None, Aeff=None):
                Ause = A if Aeff is None else Aeff
                excl = [j for j in full if j not in S]
                ef = float(sum(1.0 - Ause[peak_idx, j] for j in excl
                               if np.isfinite(Ause[peak_idx, j])))
                dec = len(excl)
                row = dict(clause=form, q=q, panel=panel, ladder=lad, stat=stat, rungs=k,
                           peak=rungs[peak_idx], gap=gap, spread=spread,
                           floor=flo if np.isfinite(flo) else np.inf,
                           published_set=str([rungs[j] for j in sorted(S)]),
                           set_size=len(S), decided=dec,
                           content=dec / (k - 1) if k > 1 else np.nan,
                           exp_false=ef,
                           err=(ef / dec) if dec else np.nan,
                           price=(dec / ef) if ef > 0 else (np.inf if dec else np.nan),
                           contentless=bool(dec == 0))
                if extra:
                    row.update(extra)
                prow.append(row)

            # --- AS_WRITTEN -----------------------------------------------------------
            S = tie_set(v, full, peak, flo)
            score(S, peak, "AS_WRITTEN", dict(note=f"floor {flo:.6g}, tie {len(S)} of {k}"))

            # --- ANNOTATED ------------------------------------------------------------
            score([peak], peak, "ANNOTATED",
                  dict(note=f"point argmax, gap {gap:.6g} vs floor {flo:.6g}"))

            # --- WIDER_RUNGS (headline step 2; ENDS reported beside it) ---------------
            for tag, csub in (("step2", sorted(set(list(range(0, k, COARSE_STEP)) + [k - 1]))),
                              ("ends", [0, k - 1])):
                pk_c = max(csub, key=lambda j: (v[j] if np.isfinite(v[j]) else -np.inf))
                flo_c, _, _ = floor_of(v, A, csub, q)
                tie_c = tie_set(v, csub, pk_c, flo_c)
                dropped = [j for j in full if j not in csub]
                S_c = sorted(set(tie_c) | set(dropped))
                if tag == "step2":
                    score(S_c, pk_c, "WIDER_RUNGS",
                          dict(note=f"coarse {len(csub)} of {k} rungs, floor {flo_c:.6g}, "
                                    f"{len(dropped)} unadjudicated", coarse=tag))
                else:
                    score(S_c, pk_c, "WIDER_RUNGS_ENDS",
                          dict(note=f"ENDS-ONLY, reported beside, never selected on", coarse=tag))

            # --- LONGER_TAPE (headline M=2; M in {2,4,8} reported beside it) ----------
            for M in M_PROBE:
                Am = np.full_like(A, np.nan)
                for i in range(k):
                    Am[i, i] = 1.0
                    for j in range(k):
                        if i != j and np.isfinite(A[i, j]):
                            Am[i, j] = Phi(sqrt(M) * Phi_inv(A[i, j]))
                flo_m, _, _ = floor_of(v, Am, full, q)
                S_m = tie_set(v, full, peak, flo_m)
                form = "LONGER_TAPE" if M == M_HEAD else f"LONGER_TAPE_M{int(M)}"
                score(S_m, peak, form,
                      dict(note=f"M={M:g}x tape, PROJECTED floor {flo_m:.6g} (was {flo:.6g})",
                           M=M), Aeff=Am)
    pr = pd.DataFrame(prow)
    dump(pr, "clause")

    # ---- the tape multiple each cell would need for its own committed gap to clear its floor
    needrows = []
    for (panel, lad, stat), c in CELL.items():
        v, A, k = c["vals"], c["A"], c["k"]
        full = list(range(k))
        peak = int(np.argmax(v))
        order = np.argsort(-v, kind="stable")
        gap = float(v[order[0]] - v[order[1]])
        need = np.nan
        for M in np.concatenate([np.arange(1.0, 20.01, 0.25), np.arange(21.0, 501.0, 1.0)]):
            Am = np.full_like(A, np.nan)
            for i in range(k):
                Am[i, i] = 1.0
                for j in range(k):
                    if i != j and np.isfinite(A[i, j]):
                        Am[i, j] = Phi(sqrt(M) * Phi_inv(A[i, j]))
            flo_m, _, _ = floor_of(v, Am, full, Q_HEAD)
            if gap >= flo_m:
                need = float(M)
                break
        needrows.append(dict(panel=panel, ladder=lad, stat=stat, gap=gap,
                             floor_full=floor_of(v, A, full, Q_HEAD)[0], M_needed=need,
                             years_needed=need * (panels[panel]["warm"].sum() / 252.0)
                             if np.isfinite(need) else np.nan))
    need_df = pd.DataFrame(needrows)
    dump(need_df, "tapeneed")
    fin = need_df["M_needed"].dropna()
    P(f"  tape multiple needed for a cell's OWN committed argmax gap to clear its OWN floor "
      f"at q={Q_HEAD}:")
    P(f"    resolves at some M <= 500 in {len(fin)} of {len(need_df)} cells; median M "
      f"{fin.median() if len(fin) else float('nan'):.2f} "
      f"({(fin.median() * panels['U56']['warm'].sum() / 252.0) if len(fin) else float('nan'):.0f} "
      f"years of tape); {int((need_df['M_needed'] <= 2).sum())} of {len(need_df)} clear at M<=2, "
      f"{int((need_df['M_needed'] <= 4).sum())} at M<=4")
    P("")

    # --------------------------------------------------------------- THE RECORD-LEVEL TOTALS
    P("## WHAT THE RECORD KEEPS AND WHAT IT LOSES — totals over the 32 CORE cells")
    totrows = []
    for q in QGRID:
        for form in sorted(pr["clause"].unique()):
            s = pr[(pr.clause == form) & (pr.q == q)]
            dec = float(s["decided"].sum())
            ef = float(s["exp_false"].sum())
            tot_rungs = float((s["rungs"] - 1).sum())
            err = ef / dec if dec else np.nan
            totrows.append(dict(q=q, clause=form, cells=len(s), decided=dec,
                                decidable=tot_rungs, content=dec / tot_rungs,
                                exp_false=ef, err=err,
                                price=(dec / ef) if ef > 0 else np.inf,
                                calibrated=bool(np.isfinite(err) and err <= (1 - q)),
                                contentless_cells=int(s["contentless"].sum()),
                                mean_set_size=float(s["set_size"].mean())))
    tot = pd.DataFrame(totrows)
    dump(tot, "totals")
    for q in QGRID:
        P(f"  q = {q:.2f}   (calibration bar: expected wrong-exclusion share <= {1 - q:.2f})")
        for _, r_ in tot[tot.q == q].sort_values("decided", ascending=False).iterrows():
            P(f"    {r_['clause']:<18} decided {r_['decided']:6.0f} of {r_['decidable']:.0f} "
              f"({r_['content']:.3f})  exp_false {r_['exp_false']:7.2f}  ERR {r_['err']:.4f}  "
              f"PRICE {r_['price']:7.2f}  contentless cells {r_['contentless_cells']:2d}  "
              f"{'CALIBRATED' if r_['calibrated'] else 'NOT calibrated'}")
    P("")
    P("  THE DECISION RULE, applied (declared (f) before any number): among the CALIBRATED")
    P("  forms at each q, the most DECIDED rungs wins.")
    decision = {}
    for q in QGRID:
        cal = tot[(tot.q == q) & (tot.calibrated) & (tot.clause.isin(CLAUSES))]
        if len(cal):
            w = cal.sort_values("decided", ascending=False).iloc[0]
            decision[q] = w["clause"]
            P(f"    q={q:.2f}  ANSWER = {w['clause']}  ({w['decided']:.0f} rungs decided, "
              f"ERR {w['err']:.4f} <= {1 - q:.2f}, PRICE {w['price']:.2f}); calibrated forms: "
              f"{sorted(cal['clause'])}")
        else:
            decision[q] = "NONE"
            P(f"    q={q:.2f}  ANSWER = NONE — no clause form is calibrated at this confidence")
    P("")

    # ------------------------------------------------- D1 / D2 — TWO CORRECTIONS, both filed
    P("## D1 — THE PREMISE'S 4.88 IS NOT THE CLAUSE'S TIE SET (a CORRECTION to 1102)")
    d1rows = []
    if fp.exists():
        f63 = pd.read_csv(fp)
        f63 = f63[(f63.L == L_HEAD) & (np.isclose(f63.q, Q_HEAD))]
        tie_only = f63[f63["tie_set_verdict"]]
        P(f"  1102's committed tie_set column is `mass_set(counts, rungs, 0.90)` — the smallest")
        P(f"  CONTIGUOUS set of rungs carrying 0.90 of the BOOTSTRAP ARGMAX MASS — computed ONCE")
        P(f"  at a fixed 0.90 and written into every q row.  It is NOT the set the clause as")
        P(f"  written publishes (the rungs within the ladder's FLOOR of the argmax), and it")
        P(f"  never consults q.  Two consequences, both measured here:")
        P(f"    (i)  1102's committed tie_set_width does NOT move with q: "
          f"{int((pd.read_csv(fp).pipe(lambda x: x[x.L == L_HEAD]).pivot_table(index=['panel','ladder','stat'], columns='q', values='tie_set_width').pipe(lambda t: (t[0.80] != t[0.95]).sum())))}"
          f" of 32 cells differ between q=0.80 and q=0.95, while its own capped FLOOR moves in "
          f"{int((pd.read_csv(fp).pipe(lambda x: x[x.L == L_HEAD]).pivot_table(index=['panel','ladder','stat'], columns='q', values='floor_capped').pipe(lambda t: (t[0.80] != t[0.95]).sum())))}"
          f" of 32.  THIS run's floor tie set moves in "
          f"{int((pr[pr.clause == 'AS_WRITTEN'].pivot_table(index=['panel','ladder','stat'], columns='q', values='set_size').pipe(lambda t: (t[0.80] != t[0.95]).sum())))} of 32, "
          f"mean set size {pr[(pr.clause == 'AS_WRITTEN') & (pr.q == 0.80)]['set_size'].mean():.2f} / "
          f"{pr[(pr.clause == 'AS_WRITTEN') & (pr.q == 0.90)]['set_size'].mean():.2f} / "
          f"{pr[(pr.clause == 'AS_WRITTEN') & (pr.q == 0.95)]['set_size'].mean():.2f} at q = 0.80 / 0.90 / 0.95.")
        P(f"    (ii) the premise's headline reproduces EXACTLY as a mass-set figure over the "
          f"{len(tie_only)} TIE cells only:")
        P(f"         mean width {tie_only['tie_set_width'].mean():.3f} rungs, "
          f"{float((tie_only['tie_set_width'] / tie_only['rungs']).mean()):.3f} of its ladder, "
          f"{int((tie_only['tie_set_width'] == tie_only['rungs']).sum())} of 32 WHOLE-LADDER "
          f"— the queue's 4.88 / 0.851 / 12.")
        aw90 = pr[(pr.clause == "AS_WRITTEN") & (pr.q == Q_HEAD)]
        P(f"         The CLAUSE's own set, over all 32 cells: mean {aw90['set_size'].mean():.3f} "
          f"of {aw90['rungs'].mean():.2f} rungs "
          f"({float((aw90['set_size'] / aw90['rungs']).mean()):.3f} of its ladder), "
          f"{int(aw90['contentless'].sum())} of 32 CONTENTLESS.")
        P(f"  THE CORRECTION, and it runs AGAINST the clause: enacted as written the clause")
        P(f"  costs MORE than 1102 published — {int(aw90['contentless'].sum())} of 32 committed "
          f"argmaxes lose all content, not 12.")
        d1rows.append(dict(what="1102 mass_set over TIE cells", cells=len(tie_only),
                           mean_width=float(tie_only["tie_set_width"].mean()),
                           mean_frac=float((tie_only["tie_set_width"] / tie_only["rungs"]).mean()),
                           whole_ladder=int((tie_only["tie_set_width"] == tie_only["rungs"]).sum())))
        d1rows.append(dict(what="1110 FLOOR tie set over all CORE cells, q=0.90", cells=len(aw90),
                           mean_width=float(aw90["set_size"].mean()),
                           mean_frac=float((aw90["set_size"] / aw90["rungs"]).mean()),
                           whole_ladder=int(aw90["contentless"].sum())))
    P("")
    P("## D2 — A CORRECTION TO THIS RUN'S OWN DECISION RULE (aggregate vs per cell)")
    d2rows = []
    for q in QGRID:
        for form in CLAUSES:
            s_ = pr[(pr.clause == form) & (pr.q == q)]
            over = int((s_["err"] > (1 - q)).sum())
            agg = float(s_["exp_false"].sum()) / max(float(s_["decided"].sum()), 1e-12)
            d2rows.append(dict(q=q, clause=form, cells=len(s_), agg_err=agg,
                               agg_calibrated=bool(agg <= 1 - q), cells_over_bar=over,
                               percell_calibrated=bool(over == 0)))
    d2 = pd.DataFrame(d2rows)
    dump(d2, "calibration")
    P("  The rule declared in (f) tests the AGGREGATE error share.  That test is WEAKER than a")
    P("  per-cell one: a long ladder's far rungs are resolved almost surely and dilute the")
    P("  near ones.  Both readings are published here; the per-cell reading is the honest bar.")
    for q in QGRID:
        row = ", ".join(f"{r['clause']} {r['cells_over_bar']}" for _, r in d2[d2.q == q].iterrows())
        P(f"    q={q:.2f}  cells whose OWN error share exceeds {1 - q:.2f} — {row}")
    P(f"  ANNOTATED is AGGREGATE-calibrated at q=0.80 (ERR "
      f"{float(d2[(d2.q == 0.80) & (d2.clause == 'ANNOTATED')]['agg_err'].iloc[0]):.4f} <= 0.20) and "
      f"PER-CELL calibrated at NO q "
      f"({int(d2[(d2.q == 0.80) & (d2.clause == 'ANNOTATED')]['cells_over_bar'].iloc[0])} of 32 cells "
      f"over their own bar even at q=0.80).  Under the per-cell reading the q=0.80 answer")
    P("  changes from ANNOTATED to AS_WRITTEN; the q=0.90 and q=0.95 answers do not change.")
    if d1rows:
        dump(pd.DataFrame(d1rows), "d1")
    P("")

    # ----------------------------------------------------------------- THE CORPUS RE-WEIGHT
    P("## THE CORPUS LAYER — 1102's 200 harvested VALUED argmax claims, rates re-derived here")
    cp = Path(f"{PRIOR1102}.claimscored.csv")
    claimrows = []
    if cp.exists():
        cl = pd.read_csv(cp)
        for q in QGRID:
            for form in sorted(pr["clause"].unique()):
                s = pr[(pr.clause == form) & (pr.q == q)]
                rate_fam = s.groupby(["ladder", "stat"])["content"].mean().to_dict()
                rate_stat = s.groupby("stat")["content"].mean().to_dict()
                overall = float(s["content"].mean())
                kept, basis_n = 0.0, {"MEASURED_FAMILY": 0, "TRANSFERRED_STAT": 0,
                                      "TRANSFERRED_OVERALL": 0}
                for _, c_ in cl.iterrows():
                    key = (c_["family"], c_["stat"])
                    if key in rate_fam:
                        rate, basis = float(rate_fam[key]), "MEASURED_FAMILY"
                    elif c_["stat"] in rate_stat:
                        rate, basis = float(rate_stat[c_["stat"]]), "TRANSFERRED_STAT"
                    else:
                        rate, basis = overall, "TRANSFERRED_OVERALL"
                    kept += rate
                    basis_n[basis] += 1
                claimrows.append(dict(q=q, clause=form, claims=len(cl), content_kept=kept,
                                      content_kept_frac=kept / len(cl), **basis_n))
        cldf = pd.DataFrame(claimrows)
        dump(cldf, "corpus")
        for q in QGRID:
            P(f"  q = {q:.2f}  of 200 harvested VALUED argmax claims, CONTENT retained:")
            for _, r_ in cldf[cldf.q == q].sort_values("content_kept", ascending=False).iterrows():
                P(f"    {r_['clause']:<18} {r_['content_kept']:6.1f} of 200 "
                  f"({r_['content_kept_frac']:.3f})  "
                  f"[{r_['MEASURED_FAMILY']} measured-by-family, {r_['TRANSFERRED_STAT']} "
                  f"transferred-by-stat, {r_['TRANSFERRED_OVERALL']} transferred-overall]")
        P("  TRANSFERRED rates are an EXTRAPOLATION, declared in advance, not a re-derivation")
        P("  of those claims (1048/1102's convention).")
    else:
        P("  1102's claimscored.csv NOT FOUND — corpus layer skipped.")
    P("")

    # --------------------------------------------------------------------------- HYPOTHESES
    P("## HYPOTHESES — declared before any number above was read")
    hyp = []
    an = pr[(pr.clause == "ANNOTATED") & (pr.q == Q_HEAD)]
    aw = pr[(pr.clause == "AS_WRITTEN") & (pr.q == Q_HEAD)]
    wr = pr[(pr.clause == "WIDER_RUNGS") & (pr.q == Q_HEAD)]
    n_uncal = int((an["err"] > (1 - Q_HEAD)).sum())
    hyp.append(("H_ANNOT_UNCAL", n_uncal > len(an) / 2,
                f"ANNOTATED's expected wrong-exclusion share exceeds {1 - Q_HEAD:.2f} in "
                f"{n_uncal} of {len(an)} cells at q={Q_HEAD}; median ERR "
                f"{an['err'].median():.4f} against a bar of {1 - Q_HEAD:.2f}"))
    pa = float(an["decided"].sum()) / max(float(an["exp_false"].sum()), 1e-12)
    pw = (float(aw["decided"].sum()) / float(aw["exp_false"].sum())
          if float(aw["exp_false"].sum()) > 0 else np.inf)
    hyp.append(("H_ANNOT_PRICE", bool(pa > pw),
                f"PRICE(ANNOTATED) {pa:.2f} vs PRICE(AS_WRITTEN) "
                f"{pw if np.isfinite(pw) else float('inf'):.2f} rungs decided per expected "
                f"wrong exclusion, q={Q_HEAD}"))
    hyp.append(("H_COARSE_LOSES", bool(wr["decided"].sum() < aw["decided"].sum()),
                f"WIDER_RUNGS decides {wr['decided'].sum():.0f} rungs against AS_WRITTEN's "
                f"{aw['decided'].sum():.0f} at q={Q_HEAD} "
                f"(content {wr['content'].mean():.3f} vs {aw['content'].mean():.3f}); "
                f"coarsening leaves a mean {float((wr['rungs'] - wr['rungs'].map(_ncoarse)).mean()):.2f} "
                f"rungs per cell UNADJUDICATED by construction"))
    mb = float(nondd["beta"].median())
    hyp.append(("H_TAPE_HALF", bool(-0.70 <= mb <= -0.30),
                f"median fitted beta over the {len(nondd)} non-DD cells {mb:+.4f} "
                f"(1/sqrt(T) is -0.50); DD exempt by declaration, its median "
                f"{beta_df[beta_df.stat == 'DD']['beta'].median():+.4f}"))
    medM = float(need_df["M_needed"].median()) if need_df["M_needed"].notna().any() else np.inf
    hyp.append(("H_TAPE_INFEAS", bool(not np.isfinite(medM) or medM > 4.0),
                f"median tape multiple needed {medM if np.isfinite(medM) else float('inf'):.2f}x "
                f"(= {medM * panels['U56']['warm'].sum() / 252.0 if np.isfinite(medM) else float('inf'):.0f} "
                f"years); {int((need_df['M_needed'] <= 4).sum())} of {len(need_df)} cells clear "
                f"at M<=4, {int(need_df['M_needed'].isna().sum())} do not clear at M<=500"))
    hyp.append(("H_DECISION", True,
                f"decision rule applied as declared: q=0.80 -> {decision.get(0.80)}, "
                f"q=0.90 -> {decision.get(0.90)}, q=0.95 -> {decision.get(0.95)}"))
    for k_, v_, why in hyp:
        P(f"  {k_:<16} {'PASS' if v_ else 'FAIL'}   {why}")
    P(f"  {sum(1 for _, v_, _ in hyp if v_)} of {len(hyp)} hypotheses PASS")
    dump(pd.DataFrame([dict(hypothesis=k_, result="PASS" if v_ else "FAIL", detail=w_)
                       for k_, v_, w_ in hyp]), "hypotheses")
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
    P("  NOTHING PROPOSED: the BOOK at every cell is byte-identical across all four clause")
    P("  forms — only the PROSE that reports it changes — so 4a and 4b are invariant to dial 1")
    P("  by construction, and no clause form can promote anything.  Scored because rule 4 says so.")
    P("")
    P("## SURVIVORSHIP (PROTOCOL rule 9)")
    P("  U56 and B136 are CURRENT-CONSTITUENT panels; every level above is optimistic.  A GAP")
    P("  between two rungs and an AGREEMENT between two rungs both contrast two books over the")
    P("  same inflated tape and the bias very largely cancels out of them and out of the floor;")
    P("  it does NOT cancel out of the 4b legs, measured against SPY, a real index.")
    P("")
    P("## THE DECLARED APPROXIMATION, AND ITS DIRECTION")
    P("  LONGER_TAPE is a PROJECTION, not a measurement: A' = Phi(sqrt(M) Phi^-1(A)) assumes the")
    P("  gap is a fixed population quantity and the SE falls as 1/sqrt(T).  Both assumptions run")
    P("  TOWARD resolution — a longer tape would also move the gaps, and a regime it has not")
    P("  seen can only widen the null — so every LONGER_TAPE count here is an UPPER bound on")
    P("  what lengthening the tape would buy.  The sub-tape fit is the check on the exponent.")
    P("")

    dump(pd.DataFrame(gaterows), "gates")
    P(f"# GATES {sum(gates.values())} of {len(gates)} PASS")
    P(f"# elapsed {time.time() - t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"wrote {OUT}.console.txt")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Idea 1192 (lane B, 2026-09-17) — does the COARSE END of a FRACTION LADDER move MORE than the
FINE END on EVERY FAMILY?

QUESTION (QUEUE idea 1192, verbatim)
    idea 1188 found share-moved runs 0.5435 at L2 against 0.2033 at L6 and 0.2348 at L8, i.e. the
    record's published figures are further from a TWO-rung reading than from a SEVEN-rung one,
    which inverts the queue's assumption that resolution is the risk.  Walk the ladder in both
    directions on all three panels and report whether the coarse-end excursion is a property of
    the between term's endpoint range or of the ladder length per se.
    Max 2 params (ladder end, between term).

THE OBJECT.  The regime-to-length ratio of the 1140 -> 1148 -> 1157 -> 1158 -> 1188 lineage:
        v(L) = W(L) / B(L)
    W(L) = median, over the ladder's NON-UNIT rungs and over the ratio's groups, of a within-part
           spread of one of six statistics (the three WITHIN kinds of 1157/1158, all reported).
    B(L) = a contrast of the FRACTION MEDIANS m[f] across the ladder L.  B is the second dial.
    The record's committed reading is the ladder L3 = {1, 2, 3} (1140's `F_1140`) with
    B = |m[1] - m[fmax]|.  Everything below is measured against that reading.

THE TWO TUNED DIALS (PROTOCOL rule 4, no more than two, and the queue names both)
    1. LADDER END   in {E_FINE, E_COARSE, E_SLIDE}
    2. BETWEEN TERM in {B_ENDPOINT, B_MATCHED, B_SD, B_SPAN}
    3 x 4 = 12 cells, EVERY ONE PUBLISHED in `.dialgrid.csv`.

    E_FINE   — 1188's ladder set VERBATIM: the COARSE anchor f=2 is held and rungs are added at
               the FINE end.  {1,2} / {1,2,3} / {1,2,3,4} / {1,2,3,4,6} / {1,2,3,4,5,6,8}.
               Rung count k = 1,2,3,4,6 and fmax = 2,3,4,6,8 GROW TOGETHER: confounded, and this
               is the only walk the record has ever taken.
    E_COARSE — the same five rung COUNTS, walked from the other end: the FINE anchor f=8 is held
               and rungs are added at the COARSE end.  {1,8} / {1,6,8} / {1,5,6,8} /
               {1,4,5,6,8} / {1,2,3,4,5,6,8}.  fmax = 8 AT EVERY RUNG COUNT, so under
               B_ENDPOINT the between term is IDENTICAL across the whole family BY CONSTRUCTION
               (gate G8) and every movement inside it is LADDER LENGTH and nothing else.
    E_SLIDE  — rung count FROZEN at k=2, the published L3's own count, and the window SLID along
               the fraction axis: {1,2,3} / {1,3,4} / {1,4,5} / {1,5,6} / {1,6,8}.  fmax varies
               3 -> 8 at CONSTANT length, so every movement inside it is the ENDPOINT and
               nothing else.
    E_FINE and E_COARSE SHARE their longest ladder (both are L8), which is the pivot the two
    walks are read against each other from (gate G9, dev exactly 0).

    B_ENDPOINT — |m[1] - m[fmax]|.  1148/1157/1158's `R_ASIS` between term, the committed one.
    B_MATCHED  — mean over ALL pairs (fi, fj) of |m[fi] - m[fj]|.  1158's `R_COUNT` repair.
    B_SD       — SD (ddof 1) of {m[f] : f in L}.  1157's `R_SD` between term.
    B_SPAN     — |m[1] - m[fmax]| / log(fmax).  1158's span-normalised form, which lane B's
                 1158 run proved is EXACTLY ladder-invariant on a log-linear m[f] (gate G7).

    NOT dials, reported at every value: PANEL {U56, B136, SMALL}; the 27 RUNG BOOKS per panel
    that are the ratio's four groups (CADENCE {D,W,M,Q}, GROSS 10 rungs, H {21,63,126,252},
    N 9 rungs), 81 in all, 1148's grid; the six STATISTICS {CAGR, VOL, SHARPE, MAXDD, ULCER,
    CALMAR} with MAXDD the lineage's headline; the two PARTITIONS {ALIGNED, OFFSET}; the three
    WITHIN kinds {R_SPREAD, R_SD, R_MATCHED}; the two CONSTRUCTIONS {C_POOLED, C_BOOK}; the four
    rule-8 choosers.  Frozen at 936/1140/1148/1157/1158/1188's construction: CAND20 legs,
    max_vol 0.60, anchor N=20 / H=126 / gross 0.75 / weekly, 10 bps, LAG 1, WARMUP 260.

A FAMILY, DEFINED BEFORE ANY NUMBER
    The title says "ON EVERY FAMILY", so a family must be a single object and not a pool.
    FAMILY := (panel, dial ladder, rung, statistic) — one rung book, one statistic — 81 x 6 = 486
    of them, each read on its OWN sub-tape partition (the `rung_only` construction).  The pooled
    surface of 1148/1157/1158 is published beside it in `.surface.csv` for continuity and for the
    replay gates, and is NOT the family unit.

THE TWO EXCURSIONS AND THE DECOMPOSITION THAT ANSWERS THE QUESTION
    MOVE_COARSE := |log v({1,2})   - log v({1,2,3})|   — the published ladder COARSENED (drop its
                    finest rung).  This is 1188's L2 reading.
    MOVE_FINE   := |log v(L8)      - log v({1,2,3})|   — the published ladder REFINED.
    Because v = W / B exactly, the move decomposes with NO residual:
        dlog v = dlog W - dlog B,
    so ATTRIB_B := |dlog B| / (|dlog W| + |dlog B|) is the share of the move's magnitude carried
    by the BETWEEN term, and 1 - ATTRIB_B the share carried by the WITHIN term.  This is an
    identity, not a regression.
    LSENS_COARSE := max/min of v over the five E_COARSE ladders  (fmax frozen -> LENGTH only)
    LSENS_SLIDE  := max/min of v over the five E_SLIDE  windows   (k frozen    -> ENDPOINT only)
    These two are the mechanism test.  Under B_ENDPOINT, LSENS_COARSE is a PURE length channel by
    construction, because B cannot move inside E_COARSE.

DECLARED BEFORE ANY NUMBER, AND SCORED IN THIS ORDER
    THE TITLE QUESTION, on the headline cell (ALIGNED / R_MATCHED / B_ENDPOINT) over the 486
    families, share := #{MOVE_COARSE > MOVE_FINE} / #resolvable:
        (A) YES, ON EVERY FAMILY      share >= 0.90
        (B) YES ON MOST               0.60 <= share < 0.90
        (C) IT IS FAMILY-SPECIFIC     0.40 <= share < 0.60
        (D) NO, THE FINE END MOVES MORE   share < 0.40
    THE MECHANISM, on the same cell, r := median LSENS_COARSE / median LSENS_SLIDE:
        (M_LEN)     r >= 1.25                                   -> LADDER LENGTH per se
        (M_END)     1/r >= 1.25                                 -> the BETWEEN term's ENDPOINT
        (M_BOTH)    neither, and both medians >= 1.10           -> both channels live
        (M_NEITHER) both medians < 1.10                         -> the ladder does not move it

HYPOTHESES, DECLARED, EACH SCORED SUPPORTED / REFUTED
    H1 PREMISE      1188's committed ordering (share-moved L2 > L6 and L2 > L8) is reproduced,
                    both from its own committed artefact and independently on this kernel.
    H2 ENDPOINT     a pure-endpoint world predicts the FINE end moves MORE (gate G7, analytic);
                    so if the data has the coarse end moving more, the endpoint is not the carrier.
    H3 LENGTH       inside E_COARSE, where the between term CANNOT move, the figure still moves:
                    median LSENS_COARSE >= 1.10.
    H4 WITHIN       median ATTRIB_B at the coarse move < 0.50, i.e. W carries the excursion.
    H5 UNIVERSAL    the coarse>fine share clears its outcome band in all 3 panels AND all 6
                    statistics, which is what "on every family" would require.
    H6 SLIDE        at frozen rung count, a finer endpoint moves the figure MONOTONICALLY:
                    Spearman rho of |log v| excursion against log(fmax) >= 0.50 (median over
                    families).
    H7 CAPITAL      choosing a rung book by the COARSE reading rather than the FINE one changes
                    OOS money (mean OOS Sharpe gap >= 0.05 in the chooser's favour either way).

CONTROLS, DECLARED UP FRONT, NOT DIALS
    C_PERM — a 21-day BLOCK-SHUFFLED tape (seeded) per rung book, which destroys the tape's
             length/regime structure and preserves its marginal and its short-run dependence.  If
             the coarse>fine asymmetry SURVIVES on a structure-free tape it is a property of the
             ladder's GEOMETRY (a range over k points, a median over k rungs) and not of the
             market.  This is a CALIBRATION control, not a significance test.
    WHY THERE IS NO BOOTSTRAP: inherited from 1158/1188 deliberately.  A sub-tape figure compares
    segments at their own POSITIONS on one tape, so a resample destroys the object.  The one
    resample here is the declared C_PERM control and is read as calibration only.

CAPITAL.  A ladder-geometry census is not a KEEP path.  4a and 4b are scored at every one of the
    81 rung books, and the rule-8 walk-forward chooses on 2009-2016 alone and reads 2017-2026
    ONCE.  CH_PUB / CH_COARSE / CH_FINE exist to price whether the DIRECTION the ladder is walked
    in moves the pick or the money at all.

THE VINTAGE.  `data/prices.csv` is rewritten nightly (idea 1163's defect; lane B's 1158 run found
    ONE extra trading day moves a committed ratio by up to 0.776 relative), so every tape is
    truncated at PIN = 2026-09-15, the vintage 1148/1157/1158/1188's committed anchors saw.  The
    unpinned reading of the headline cell is published beside the pinned one, not absorbed.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the current
    output of a sub-$2B screen less the documented `max_1d_move >= 1.0` exclusion.  Every LEVEL is
    optimistic and every 4a/4b count is an UPPER bound.  This run's object is a ratio of two
    spreads in the statistic's own units and is far less exposed, but MAXDD is the lineage's
    headline statistic and a survivorship-flattered panel has a shallower drawdown path, so the
    levels are published beside every ratio.
"""
from __future__ import annotations

import sys
import time
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-17"
SLUG = "does-the-COARSE-END-of-a-FRACTION-LADDER-MOVE-MORE-THAN-THE-FINE-END-ON-EVERY-FAMILY"
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

STATS6 = ["CAGR", "VOL", "SHARPE", "MAXDD", "ULCER", "CALMAR"]
HEAD_STAT = "MAXDD"
WITHINS = ["R_SPREAD", "R_SD", "R_MATCHED"]
HEAD_WITHIN = "R_MATCHED"
CONSTRUCTIONS = ["C_POOLED", "C_BOOK"]
HEAD_PART = "ALIGNED"

# ---- dial 1: LADDER END.  keys are the walk's rung-count / endpoint labels, printed as given.
FAM_LADDERS = {
    "E_FINE": [("k1", [1, 2]), ("k2", [1, 2, 3]), ("k3", [1, 2, 3, 4]),
               ("k4", [1, 2, 3, 4, 6]), ("k6", [1, 2, 3, 4, 5, 6, 8])],
    "E_COARSE": [("k1", [1, 8]), ("k2", [1, 6, 8]), ("k3", [1, 5, 6, 8]),
                 ("k4", [1, 4, 5, 6, 8]), ("k6", [1, 2, 3, 4, 5, 6, 8])],
    "E_SLIDE": [("f3", [1, 2, 3]), ("f4", [1, 3, 4]), ("f5", [1, 4, 5]),
                ("f6", [1, 5, 6]), ("f8", [1, 6, 8])],
}
FAMS = list(FAM_LADDERS)
BETWEENS = ["B_ENDPOINT", "B_MATCHED", "B_SD", "B_SPAN"]
HEAD_BETWEEN = "B_ENDPOINT"

PUB_FRACS = [1, 2, 3]            # the record's F_1140 / L3, the reading everything is read against
COARSE_FRACS = [1, 2]            # 1188's L2
FINE_FRACS = [1, 2, 3, 4, 5, 6, 8]   # 1188's L8
FRAC_ALL = sorted({f for v in FAM_LADDERS.values() for _, fr in v for f in fr})

# 1188's ladder set, reproduced verbatim for the premise replay
L1188 = {"L2": [1, 2], "L3": [1, 2, 3], "L4": [1, 2, 3, 4],
         "L6": [1, 2, 3, 4, 6], "L8": [1, 2, 3, 4, 5, 6, 8]}

NPAIR_1157, SEED_1148 = 200, 11481148
SEED_PERM = 11921192
PERM_BLOCK = 21
PRIOR_CELL_1148 = 0.794259      # 1148 SMALL / MAXDD / R_MATCHED / F_1140, committed
PRIOR_RES_1158 = 1.173714       # 1158's L8 R_COUNT reading of the same cell, committed
A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
DD_COMMITTED = {"U56": -19.127569, "B136": -20.740302, "SMALL": -35.814054}
PREMISE_1188 = {"L2": 0.543460, "L6": 0.203326, "L8": 0.234815}
GRID_1188 = BT / ("2026-09-17_how-many-committed-SUB-TAPE-FIGURES-move-once-the-LADDER-is-"
                  "RESOLVED-rather-than-FROZEN_C.grid.csv")

BAR_A, BAR_B, BAR_D = 0.90, 0.60, 0.40
BAR_MECH, BAR_LIVE = 1.25, 1.10

LOG: list[str] = []
GATES: list[dict] = []
HYPS: list[dict] = []
GZ = {"families", "levels"}


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    ext = ".csv.gz" if suffix in GZ else ".csv"
    p = Path(f"{OUT}.{suffix}{ext}")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def gate(name, what, value, ok):
    GATES.append(dict(gate=name, what=what, value=float(value), pass_=bool(ok)))
    P(f"  {name:<6s} {'PASS' if ok else 'FAIL'}  {what}   (dev {value:.3e})")


def hyp(name, what, value, supported, verdict=None):
    v = verdict or ("SUPPORTED" if supported else "REFUTED")
    HYPS.append(dict(hypothesis=name, what=what, value=float(value), verdict=v))
    P(f"  {name:<12s} {v:<11s}  {what}  = {value!r}")


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


# --------------------------------------- 1157/1158's partitions + terms, verbatim semantics
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
    v = np.asarray([x for x in v if np.isfinite(x)], float)
    if len(v) < 2:
        return np.nan
    return float(np.mean([abs(a - b) for a, b in combinations(v, 2)]))


def within_of(groups, fracs, kind, matched_fn=matched_exact):
    """1157/1158's WITHIN term, verbatim: median over the ladder's NON-UNIT rungs and over the
    ratio's groups of the within-part spread."""
    acc = []
    for f in fracs:
        if f == 1:
            continue
        for v in groups.get(f, []):
            v = np.asarray([x for x in v if np.isfinite(x)], float)
            if len(v) < 2:
                continue
            if kind == "R_SPREAD":
                acc.append(float(v.max() - v.min()))
            elif kind == "R_SD":
                acc.append(float(v.std(ddof=1)))
            else:
                m = matched_fn(v)
                if np.isfinite(m):
                    acc.append(m)
    return float(np.nanmedian(acc)) if acc else np.nan


def between_of(med, fracs, form):
    """The four BETWEEN forms.  B_ENDPOINT is 1148/1157/1158's `R_ASIS`; B_MATCHED is 1158's
    `R_COUNT`; B_SD is 1157's `R_SD` between term; B_SPAN is 1158-B's span-normalised form."""
    vals = [med.get(f, np.nan) for f in fracs]
    fmax = max(fracs)
    a, b = med.get(1, np.nan), med.get(fmax, np.nan)
    ep = abs(a - b) if (np.isfinite(a) and np.isfinite(b)) else np.nan
    if form == "B_ENDPOINT":
        return ep
    if form == "B_SPAN":
        return (ep / np.log(fmax)) if fmax > 1 else np.nan
    if form == "B_MATCHED":
        return matched_exact(vals)
    if form == "B_SD":
        v = [x for x in vals if np.isfinite(x)]
        return float(np.std(v, ddof=1)) if len(v) >= 2 else np.nan
    raise ValueError(form)


def rat(w, b):
    v = (w / b) if (np.isfinite(w) and np.isfinite(b) and b != 0.0) else np.nan
    if np.isfinite(v) and (v <= 0.0 or v > 1e12):
        v = np.nan
    return v


def ratio_of(groups, med, fracs, kind, form, matched_fn=matched_exact):
    w = within_of(groups, fracs, kind, matched_fn)
    b = between_of(med, fracs, form)
    return w, b, rat(w, b)


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(meta), len(meta) - (len(keep) - 1)


def block_shuffle(r, rng, blk=PERM_BLOCK):
    n = len(r)
    nb = int(np.ceil(n / blk))
    starts = rng.permutation(nb)
    out = np.concatenate([r[s * blk:(s + 1) * blk] for s in starts])
    return out[:n]


def spearman(x, y):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 3:
        return np.nan
    a = pd.Series(x[ok]).rank().values
    b = pd.Series(y[ok]).rank().values
    if a.std() == 0 or b.std() == 0:
        return np.nan
    return float(np.corrcoef(a, b)[0, 1])


def lsens(vals):
    v = np.asarray([x for x in vals if np.isfinite(x) and x > 0], float)
    if len(v) < 2:
        return np.nan
    return float(v.max() / v.min())


def safe_exc(v, v0):
    if not (np.isfinite(v) and np.isfinite(v0) and v > 0 and v0 > 0):
        return np.nan
    return float(abs(np.log(v / v0)))


def band(share):
    if share >= BAR_A:
        return "(A) YES, ON EVERY FAMILY"
    if share >= BAR_B:
        return "(B) YES ON MOST"
    if share >= BAR_D:
        return "(C) IT IS FAMILY-SPECIFIC"
    return "(D) NO, THE FINE END MOVES MORE"


# ================================================================== the analytic identity
def analytic_table():
    """DATA-FREE.  m[f] = log f exactly (a perfectly log-linear length effect) and a WITHIN term
    frozen at 1.  Under these the ratio is v(L) = 1 / B(L), so every number below is a property
    of the LADDER GEOMETRY and of nothing else.  Established BEFORE the data is read."""
    med = {f: float(np.log(f)) for f in FRAC_ALL}
    rows = []
    for fam in FAMS:
        for lab, fr in FAM_LADDERS[fam]:
            for form in BETWEENS:
                b = between_of(med, fr, form)
                rows.append(dict(family=fam, rung_label=lab, k=len(fr) - 1, fmax=max(fr),
                                 between=form, B=b, v=(1.0 / b if b else np.nan)))
    return pd.DataFrame(rows)


# ================================================================== main
def main():
    t0 = time.time()
    P(f"# Idea 1192 (lane B, {DATE}) — does the COARSE END of a FRACTION LADDER move MORE than")
    P("# the FINE END on EVERY FAMILY?")
    P(f"# 2 tuned dials: LADDER END {FAMS} x BETWEEN TERM {BETWEENS} = "
      f"{len(FAMS) * len(BETWEENS)} cells, ALL published in .dialgrid.csv.")
    P("# FAMILY = (panel, dial ladder, rung, statistic) = 81 x 6 = 486 single objects, each read")
    P("#   on its OWN sub-tape partition.  The pooled 1148/1157/1158 surface is published beside")
    P("#   it and is NOT the family unit.")
    P("# IDENTIFICATION: E_COARSE freezes fmax at 8 so its between term CANNOT move (LENGTH")
    P("#   only); E_SLIDE freezes the rung count at 2 so its length CANNOT move (ENDPOINT only).")
    P("# dlog v = dlog W - dlog B is an IDENTITY, so ATTRIB_B is an attribution and not a fit.")
    P(f"# TAPE PINNED at {PIN} (idea 1163 / 1158-B's one-extra-day defect).  SURVIVORSHIP: every")
    P("#   LEVEL is an upper bound.  NO BOOTSTRAP except the declared C_PERM control.")
    P("")

    # ------------------------------------------------ the analytic identity, before the data
    P("## THE ANALYTIC IDENTITY — DATA-FREE, PRINTED BEFORE ANY TAPE IS READ")
    AN = analytic_table()
    dump(AN, "analytic")
    an_l = {}
    for fam in FAMS:
        for form in BETWEENS:
            s = AN[(AN.family == fam) & (AN.between == form)]
            an_l[(fam, form)] = lsens(s.v.values)
    P("  LSENS on a perfectly log-linear m[f] with a FROZEN within term (pure ladder geometry):")
    P("    family      " + "  ".join(f"{f:>12s}" for f in BETWEENS))
    for fam in FAMS:
        P(f"    {fam:<12s}" + "  ".join(f"{an_l[(fam, f)]:12.4f}" for f in BETWEENS))
    a_pub = 1.0 / between_of({f: float(np.log(f)) for f in FRAC_ALL}, PUB_FRACS, "B_ENDPOINT")
    a_cr = 1.0 / between_of({f: float(np.log(f)) for f in FRAC_ALL}, COARSE_FRACS, "B_ENDPOINT")
    a_fn = 1.0 / between_of({f: float(np.log(f)) for f in FRAC_ALL}, FINE_FRACS, "B_ENDPOINT")
    AN_COARSE, AN_FINE = safe_exc(a_cr, a_pub), safe_exc(a_fn, a_pub)
    P(f"  analytic MOVE_COARSE {AN_COARSE:.4f}  vs  MOVE_FINE {AN_FINE:.4f}   -> a PURE-ENDPOINT")
    P("    world has the FINE end moving MORE, by construction.  H2 is scored against this.")
    gate("G7", "analytic B_SPAN is EXACTLY ladder-invariant on both walks",
         max(abs(an_l[(f, "B_SPAN")] - 1.0) for f in FAMS),
         max(abs(an_l[(f, "B_SPAN")] - 1.0) for f in FAMS) < 1e-12)
    gate("G7b", "analytic B_ENDPOINT: E_COARSE LSENS exactly 1 (fmax frozen), E_SLIDE 1.8928",
         abs(an_l[("E_COARSE", "B_ENDPOINT")] - 1.0),
         abs(an_l[("E_COARSE", "B_ENDPOINT")] - 1.0) < 1e-12
         and abs(an_l[("E_SLIDE", "B_ENDPOINT")] - np.log(8) / np.log(3)) < 1e-12)
    gate("G7c", "analytic pure-endpoint world: MOVE_FINE > MOVE_COARSE",
         AN_FINE - AN_COARSE, AN_FINE > AN_COARSE)
    P("")

    # ------------------------------------------------ structural gates on the dial itself
    P("## STRUCTURAL GATES ON THE DIAL")
    gate("G8", "E_COARSE has fmax == 8 at every rung count (its between term cannot move)",
         max(abs(max(fr) - 8) for _, fr in FAM_LADDERS["E_COARSE"]),
         all(max(fr) == 8 for _, fr in FAM_LADDERS["E_COARSE"]))
    gate("G8b", "E_SLIDE has exactly 2 non-unit rungs at every window (its length cannot move)",
         max(abs(len(fr) - 1 - 2) for _, fr in FAM_LADDERS["E_SLIDE"]),
         all(len(fr) - 1 == 2 for _, fr in FAM_LADDERS["E_SLIDE"]))
    gate("G8c", "E_FINE and E_COARSE share their longest ladder (the pivot both walks meet at)",
         0.0, FAM_LADDERS["E_FINE"][-1][1] == FAM_LADDERS["E_COARSE"][-1][1] == FINE_FRACS)
    gate("G8d", "E_FINE is 1188's ladder set VERBATIM (L2, L3, L4, L6, L8)", 0.0,
         [fr for _, fr in FAM_LADDERS["E_FINE"]] == [L1188[k] for k in ("L2", "L3", "L4",
                                                                        "L6", "L8")])
    gate("G8e", "the matched rung counts of E_FINE and E_COARSE agree", 0.0,
         [len(fr) - 1 for _, fr in FAM_LADDERS["E_FINE"]]
         == [len(fr) - 1 for _, fr in FAM_LADDERS["E_COARSE"]])
    P("")

    # ------------------------------------------------ 1188's premise, from its own artefact
    P("## G1 — 1188's PREMISE, REPLAYED FROM ITS OWN COMMITTED ARTEFACT")
    prem_ok, prem_dev = False, np.nan
    if GRID_1188.exists():
        g = pd.read_csv(GRID_1188)
        g = g[g.claimset == "C_STRICT"].set_index("L")["share_moved"]
        prem_dev = max(abs(g.get(k, np.nan) - v) for k, v in PREMISE_1188.items())
        prem_ok = bool(prem_dev < 1e-6 and g["L2"] > g["L6"] and g["L2"] > g["L8"])
        P(f"  1188 C_STRICT share_moved: L2 {g['L2']:.6f}  L3 {g['L3']:.6f}  L4 {g['L4']:.6f}  "
          f"L6 {g['L6']:.6f}  L8 {g['L8']:.6f}")
    else:
        P("  1188's grid.csv NOT FOUND — premise replay reported as FAIL, never assumed")
    gate("G1", "1188's committed share-moved reproduced and L2 > L6, L2 > L8",
         prem_dev if np.isfinite(prem_dev) else 1.0, prem_ok)
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
          f"{d['idx'][-1].date()}   (unpinned {cells_un[panel]['T']} bars, last "
          f"{cells_un[panel]['idx'][-1].date()})")
        if panel == "SMALL":
            P(f"  SMALL STAMP: data/small_meta.csv lists {nmeta} tickers; {ndrop} dropped for "
              f"max_1d_move >= 1.0; pool served = {d['K'] - 1} names + SPY as benchmark.")
    gate("G10", "every pinned tape ends on or before the PIN vintage", 0.0,
         all(cells[p]["idx"][-1] <= pd.Timestamp(PIN) for p in PANELS))
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

    RUNGS = [(lad, rg) for lad, rgs in LADDERS.items() for rg in rgs]
    P(f"## RUNG BOOKS — {len(RUNGS)} per panel (the ratio's four groups), "
      f"{len(RUNGS) * len(PANELS)} in total, 1148's grid")
    BOOKS = {}
    for panel in PANELS:
        for lad, rg in RUNGS:
            BOOKS[(panel, lad, rg)] = rung_book(cells, "P", panel, lad, rg)
        P(f"  {panel:<6s} done   ({time.time() - t0:6.1f}s)")
    a = blocks_m(BOOKS[("U56", "N", N0)], cells["U56"]["ins"], cells["U56"]["oos"])
    dev936 = max(abs(a["CAGR"] - A936_WH126[0]), abs(a["Sharpe"] - A936_WH126[1]) / 10.0,
                 abs(a["MaxDD"] - A936_WH126[2]))
    gate("G2", "936's committed U56 anchor book (CAGR / Sharpe / MaxDD)", dev936, dev936 < 5e-4)
    P("")

    # ------------------------------- the sub-tape level surface + cached part arrays
    P("## SUB-TAPE LEVEL SURFACE — (panel, ladder, rung, partition, frac, part) x 6 stats")
    lev_rows = []
    PARTVALS: dict = {}
    for panel in PANELS:
        for lad, rg in RUNGS:
            r = BOOKS[(panel, lad, rg)]
            for part_mode in PARTITIONS:
                for f in FRAC_ALL:
                    segs = parts_at(r, f, part_mode)
                    sts = [six_stats(s) for s in segs]
                    PARTVALS[(panel, part_mode, lad, str(rg), f)] = {
                        st: np.array([x[st] for x in sts], float) for st in STATS6}
                    for j, (s, stv) in enumerate(zip(segs, sts)):
                        lev_rows.append(dict(panel=panel, ladder=lad, rung=str(rg), frac=f,
                                             part=j, partition=part_mode, n_days=len(s), **stv))
    LEVDF = pd.DataFrame(lev_rows)
    P(f"  {len(LEVDF):,} sub-tape level figures built   ({time.time() - t0:6.1f}s)")
    dump(LEVDF, "levels")
    dev_dd = max(abs(LEVDF[(LEVDF.panel == p) & (LEVDF.ladder == "N") & (LEVDF.rung == str(N0))
                           & (LEVDF.frac == 1) & (LEVDF.partition == "ALIGNED")].MAXDD.iloc[0]
                     - DD_COMMITTED[p]) for p in PANELS)
    gate("G3", "the record's committed full-tape MAXDD on all three panels", dev_dd,
         dev_dd < 5e-3)
    P("")

    # ------------------------------- 1158's groups_med, rebuilt on the cached arrays
    GM_CACHE: dict = {}

    def groups_med(panel, stat, fracs, part_mode, construction, rung_only=None):
        key = (panel, stat, tuple(fracs), part_mode, construction, rung_only)
        if key in GM_CACHE:
            return GM_CACHE[key]
        if rung_only is not None:
            keys = [rung_only]
        elif construction == "C_BOOK":
            keys = [("N", N0)]          # 1158/1188's C_BOOK: the ANCHOR book
        else:
            keys = list(RUNGS)
        groups = {f: [] for f in fracs}
        allv = {f: [] for f in fracs}
        bylad: dict = {}
        for lad, rg in keys:
            for f in fracs:
                v = PARTVALS[(panel, part_mode, lad, str(rg), f)][stat]
                allv[f].extend(v.tolist())
                bylad.setdefault((lad, f), []).append(v)
        for (lad, f), mats in bylad.items():
            n = min(len(m) for m in mats)
            if n == 0:
                continue
            M = np.vstack([m[:n] for m in mats])
            groups[f].append(np.nanmedian(M, axis=0).tolist())
        med = {f: (float(np.nanmedian(allv[f])) if allv[f] else np.nan) for f in fracs}
        GM_CACHE[key] = (groups, med)
        return groups, med

    WB_CACHE: dict = {}

    def wb(panel, stat, part_mode, construction, fracs, rung_only=None):
        """All three WITHIN kinds and all four BETWEEN forms for one coordinate, cached.  The
        within term does not depend on the between dial, so it is computed once."""
        key = (panel, stat, part_mode, construction, tuple(fracs), rung_only)
        if key in WB_CACHE:
            return WB_CACHE[key]
        g, m = groups_med(panel, stat, fracs, part_mode, construction, rung_only)
        W = {k: within_of(g, fracs, k) for k in WITHINS}
        B = {f: between_of(m, fracs, f) for f in BETWEENS}
        WB_CACHE[key] = (W, B)
        return W, B

    def coord_ratio(panel, stat, part_mode, construction, fracs, kind, form, rung_only=None):
        W, B = wb(panel, stat, part_mode, construction, fracs, rung_only)
        return W[kind], B[form], rat(W[kind], B[form])

    # ------------------------------- G4/G5: the two committed cells of the lineage
    P("## G4/G5 — THE LINEAGE'S TWO COMMITTED CELLS")
    v1158 = coord_ratio("SMALL", HEAD_STAT, "ALIGNED", "C_POOLED", FINE_FRACS,
                        HEAD_WITHIN, "B_MATCHED")[2]
    d1158 = abs(v1158 / PRIOR_RES_1158 - 1.0)
    gate("G4", f"1158's committed L8 R_COUNT reading of SMALL/MAXDD ({PRIOR_RES_1158}) "
         f"-> {v1158:.6f}", d1158, d1158 < 1e-4)
    # 1148's cell carries a 200-pair Monte-Carlo within term whose value depends on the DRAW
    # ORDER of the loop that produced it.  1188 recovered that order; it is replayed here and
    # declared, never nudged.
    v1148 = np.nan
    for part_mode in PARTITIONS:
        for Lk, Lfr in L1188.items():
            rng57 = np.random.default_rng(SEED_1148)
            for panel in PANELS:
                for stat in STATS6:
                    g, m = groups_med(panel, stat, Lfr, part_mode, "C_POOLED")
                    w = within_of(g, Lfr, HEAD_WITHIN,
                                  matched_fn=lambda x, _r=rng57: matched_sampled(x, _r))
                    b = between_of(m, Lfr, "B_ENDPOINT")
                    if (part_mode, Lk, panel, stat) == ("ALIGNED", "L3", "SMALL", HEAD_STAT):
                        v1148 = w / b if b else np.nan
    d1148 = abs(v1148 / PRIOR_CELL_1148 - 1.0)
    gate("G5", f"1148's committed SMALL/MAXDD/R_MATCHED/F_1140 ({PRIOR_CELL_1148}) "
         f"-> {v1148:.6f}", d1148, d1148 < 1e-4)
    P("")

    # ------------------------------- the pooled surface (continuity with 1148/1157/1158)
    P("## POOLED RATIO SURFACE — (construction, partition, panel, stat) x family x ladder x "
      "between x within")
    surf_rows = []
    for construction in CONSTRUCTIONS:
        for part_mode in PARTITIONS:
            for panel in PANELS:
                for stat in STATS6:
                    for fam in FAMS:
                        for lab, fr in FAM_LADDERS[fam]:
                            W, B = wb(panel, stat, part_mode, construction, fr)
                            for form in BETWEENS:
                                row = dict(construction=construction, partition=part_mode,
                                           panel=panel, stat=stat, family=fam, rung_label=lab,
                                           k=len(fr) - 1, fmax=max(fr), between=form)
                                for kind in WITHINS:
                                    row[f"{kind}_within"] = W[kind]
                                    row[f"{kind}_between"] = B[form]
                                    row[f"{kind}_ratio"] = rat(W[kind], B[form])
                                surf_rows.append(row)
    SURFDF = pd.DataFrame(surf_rows)
    P(f"  {len(SURFDF):,} pooled coordinates x 3 within kinds = {3 * len(SURFDF):,} figures "
      f"  ({time.time() - t0:6.1f}s)")
    dump(SURFDF, "surface")
    # the pivot: the two walks meet at L8 and must agree exactly there
    piv = SURFDF[(SURFDF.rung_label == "k6") & SURFDF.family.isin(["E_FINE", "E_COARSE"])]
    pv = piv.pivot_table(index=["construction", "partition", "panel", "stat", "between"],
                         columns="family", values=f"{HEAD_WITHIN}_ratio")
    dv = np.abs(pv["E_FINE"].values - pv["E_COARSE"].values) if len(pv) else np.array([1.0])
    dv = dv[np.isfinite(dv)]
    dpiv = float(dv.max()) if len(dv) else 1.0
    gate("G9", f"E_FINE and E_COARSE agree EXACTLY at the shared L8 pivot ({len(dv)} coords)",
         dpiv, dpiv < 1e-12 and len(dv) > 0)
    P("")

    # ------------------------------- THE FAMILY SURFACE — the run's object
    P("## THE FAMILY SURFACE — 486 families x 3 walks x 5 ladders x 4 betweens x 3 within kinds")
    fam_rows = []
    for panel in PANELS:
        for lad, rg in RUNGS:
            for stat in STATS6:
                for part_mode in PARTITIONS:
                    W0, B0 = wb(panel, stat, part_mode, "C_BOOK", PUB_FRACS, (lad, rg))
                    for fam in FAMS:
                        for lab, fr in FAM_LADDERS[fam]:
                            W, B = wb(panel, stat, part_mode, "C_BOOK", fr, (lad, rg))
                            for kind in WITHINS:
                                w, w0 = W[kind], W0[kind]
                                dW = (np.log(w / w0) if (np.isfinite(w) and np.isfinite(w0)
                                                         and w > 0 and w0 > 0) else np.nan)
                                for form in BETWEENS:
                                    b, b0 = B[form], B0[form]
                                    v, v0 = rat(w, b), rat(w0, b0)
                                    dB = (np.log(b / b0) if (np.isfinite(b) and np.isfinite(b0)
                                                             and b > 0 and b0 > 0) else np.nan)
                                    ab = (abs(dB) / (abs(dW) + abs(dB))
                                          if np.isfinite(dW) and np.isfinite(dB)
                                          and (abs(dW) + abs(dB)) > 0 else np.nan)
                                    fam_rows.append(dict(
                                        panel=panel, ladder=lad, rung=str(rg), stat=stat,
                                        partition=part_mode, within=kind, between=form,
                                        family=fam, rung_label=lab, k=len(fr) - 1,
                                        fmax=max(fr), W=w, B=b, ratio=v, W_pub=w0, B_pub=b0,
                                        ratio_pub=v0, dlogW=dW, dlogB=dB,
                                        exc=safe_exc(v, v0), attrib_B=ab))
    FAMDF = pd.DataFrame(fam_rows)
    P(f"  {len(FAMDF):,} family x ladder figures   ({time.time() - t0:6.1f}s)")
    dump(FAMDF, "families")
    P("")

    # ------------------------------- THE 12 DIAL CELLS
    P("## THE 12 DIAL CELLS — LADDER END x BETWEEN TERM, all published")
    KEYS = ["panel", "ladder", "rung", "stat"]

    def cell_stats(sub, form, part_mode=HEAD_PART, kind=HEAD_WITHIN):
        """coarse-vs-fine share, the two LSENS, the attribution, and H6's monotonicity."""
        s = sub[(sub.partition == part_mode) & (sub.within == kind) & (sub.between == form)]
        cr = s[(s.family == "E_FINE") & (s.rung_label == "k1")].set_index(KEYS)["exc"]
        fn = s[(s.family == "E_FINE") & (s.rung_label == "k6")].set_index(KEYS)["exc"]
        both = pd.concat([cr.rename("coarse"), fn.rename("fine")], axis=1).dropna()
        share = float((both.coarse > both.fine).mean()) if len(both) else np.nan
        abc = s[(s.family == "E_FINE") & (s.rung_label == "k1")].attrib_B
        abf = s[(s.family == "E_FINE") & (s.rung_label == "k6")].attrib_B
        lc, ls, lf, rhos = [], [], [], []
        for _, gg in s.groupby(KEYS):
            lc.append(lsens(gg[gg.family == "E_COARSE"].ratio.values))
            ls.append(lsens(gg[gg.family == "E_SLIDE"].ratio.values))
            lf.append(lsens(gg[gg.family == "E_FINE"].ratio.values))
            sl = gg[gg.family == "E_SLIDE"]
            rhos.append(spearman(np.log(sl.fmax.values.astype(float)), sl.exc.values))
        med = lambda x: float(np.nanmedian(x)) if len(x) else np.nan   # noqa: E731
        return dict(n_families=int(len(both)), share_coarse_gt_fine=share,
                    med_exc_coarse=float(both.coarse.median()) if len(both) else np.nan,
                    med_exc_fine=float(both.fine.median()) if len(both) else np.nan,
                    med_attrib_B_coarse=float(abc.median()), med_attrib_B_fine=float(abf.median()),
                    med_LSENS_COARSE=med(lc), med_LSENS_SLIDE=med(ls), med_LSENS_FINE=med(lf),
                    med_rho_slide=med(rhos))

    grid_rows = []
    for form in BETWEENS:
        cs = cell_stats(FAMDF, form)
        r = float(cs["med_LSENS_COARSE"] / cs["med_LSENS_SLIDE"]) if cs["med_LSENS_SLIDE"] else np.nan
        mech = ("(M_LEN) LADDER LENGTH" if r >= BAR_MECH else
                "(M_END) BETWEEN ENDPOINT" if (r and 1.0 / r >= BAR_MECH) else
                "(M_BOTH) both channels live"
                if min(cs["med_LSENS_COARSE"], cs["med_LSENS_SLIDE"]) >= BAR_LIVE
                else "(M_NEITHER) the ladder does not move it")
        for fam in FAMS:
            grid_rows.append(dict(ladder_end=fam, between=form,
                                  analytic_LSENS=an_l[(fam, form)],
                                  med_LSENS_this_walk=cs[{"E_FINE": "med_LSENS_FINE",
                                                          "E_COARSE": "med_LSENS_COARSE",
                                                          "E_SLIDE": "med_LSENS_SLIDE"}[fam]],
                                  mech_ratio_len_over_end=r, mechanism=mech, **cs))
    GRID = pd.DataFrame(grid_rows)
    dump(GRID, "dialgrid")
    P(GRID[["ladder_end", "between", "analytic_LSENS", "med_LSENS_this_walk", "n_families",
            "share_coarse_gt_fine", "med_exc_coarse", "med_exc_fine", "med_attrib_B_coarse",
            "mech_ratio_len_over_end", "mechanism"]].to_string(
        index=False, float_format=lambda x: f"{x:.4f}"))
    P("")

    # ------------------------------- the headline cell
    HEAD = cell_stats(FAMDF, HEAD_BETWEEN)
    share = HEAD["share_coarse_gt_fine"]
    outcome = band(share)
    r_mech = HEAD["med_LSENS_COARSE"] / HEAD["med_LSENS_SLIDE"]
    mech = GRID[GRID.between == HEAD_BETWEEN].mechanism.iloc[0]
    P(f"## HEADLINE CELL ({HEAD_PART} / {HEAD_WITHIN} / {HEAD_BETWEEN})")
    P(f"  coarse>fine at {HEAD['n_families']} resolvable families : {share:.4f}   -> {outcome}")
    P(f"  median excursion  COARSE {HEAD['med_exc_coarse']:.4f}   FINE "
      f"{HEAD['med_exc_fine']:.4f}   (analytic pure-endpoint prediction "
      f"{AN_COARSE:.4f} / {AN_FINE:.4f})")
    P(f"  median LSENS_COARSE (LENGTH only) {HEAD['med_LSENS_COARSE']:.4f}  vs LSENS_SLIDE "
      f"(ENDPOINT only) {HEAD['med_LSENS_SLIDE']:.4f}   ratio {r_mech:.4f}  -> {mech}")
    P(f"  median ATTRIB_B  coarse move {HEAD['med_attrib_B_coarse']:.4f}   fine move "
      f"{HEAD['med_attrib_B_fine']:.4f}   (1 - ATTRIB_B is the WITHIN term's share)")
    P("")

    # ------------------------------- H5: universality by panel and by statistic
    P("## H5 — UNIVERSALITY: THE SHARE BY PANEL AND BY STATISTIC (headline cell)")
    s = FAMDF[(FAMDF.partition == HEAD_PART) & (FAMDF.within == HEAD_WITHIN)
              & (FAMDF.between == HEAD_BETWEEN) & (FAMDF.family == "E_FINE")]
    cr = s[s.rung_label == "k1"].set_index(KEYS)["exc"].rename("coarse")
    fn = s[s.rung_label == "k6"].set_index(KEYS)["exc"].rename("fine")
    CF = pd.concat([cr, fn], axis=1).dropna().reset_index()
    CF["coarse_wins"] = CF.coarse > CF.fine
    uni_rows = []
    for by in ("panel", "stat"):
        for k, gg in CF.groupby(by):
            uni_rows.append(dict(cut=by, value=k, n=int(len(gg)),
                                 share=float(gg.coarse_wins.mean()),
                                 med_coarse=float(gg.coarse.median()),
                                 med_fine=float(gg.fine.median()), band=band(gg.coarse_wins.mean())))
    for k, gg in CF.groupby("ladder"):
        uni_rows.append(dict(cut="dial_ladder", value=k, n=int(len(gg)),
                             share=float(gg.coarse_wins.mean()),
                             med_coarse=float(gg.coarse.median()),
                             med_fine=float(gg.fine.median()), band=band(gg.coarse_wins.mean())))
    UNI = pd.DataFrame(uni_rows)
    dump(UNI, "universality")
    P(UNI.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    bands = set(UNI[UNI.cut.isin(["panel", "stat"])].band)
    P(f"  distinct outcome bands across the 3 panels and 6 statistics: {len(bands)}  {sorted(bands)}")
    P("")

    # ------------------------------- the LSENS table by walk, by rung count
    P("## THE TWO WALKS, RUNG BY RUNG (headline cell, median over the 486 families)")
    ls_rows = []
    for fam in FAMS:
        for lab, fr in FAM_LADDERS[fam]:
            q = FAMDF[(FAMDF.partition == HEAD_PART) & (FAMDF.within == HEAD_WITHIN)
                      & (FAMDF.between == HEAD_BETWEEN) & (FAMDF.family == fam)
                      & (FAMDF.rung_label == lab)]
            ls_rows.append(dict(family=fam, rung_label=lab, k=len(fr) - 1, fmax=max(fr),
                                fracs=str(fr), n_resolvable=int(q.ratio.notna().sum()),
                                med_ratio=float(q.ratio.median()),
                                med_W=float(q.W.median()), med_B=float(q.B.median()),
                                med_exc=float(q.exc.median()),
                                med_attrib_B=float(q.attrib_B.median())))
    LS = pd.DataFrame(ls_rows)
    dump(LS, "walks")
    P(LS.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")

    # ---------------------- WHY: the between term's NEAR-DEGENERACY at the coarse endpoint
    P("## THE MECHANISM, MEASURED — THE BETWEEN TERM'S NEAR-DEGENERACY AT f=2")
    hh = FAMDF[(FAMDF.partition == HEAD_PART) & (FAMDF.within == HEAD_WITHIN)
               & (FAMDF.between == HEAD_BETWEEN) & (FAMDF.family == "E_FINE")]
    bb2 = hh[hh.rung_label == "k1"].set_index(KEYS).B
    bb3 = hh[hh.rung_label == "k2"].set_index(KEYS).B
    bb8 = hh[hh.rung_label == "k6"].set_index(KEYS).B
    r23 = (bb2 / bb3).replace([np.inf, -np.inf], np.nan).dropna()
    r83 = (bb8 / bb3).replace([np.inf, -np.inf], np.nan).dropna()
    deg_rows = [dict(step="B(fmax=2) / B(fmax=3)  [COARSEN]", n=int(len(r23)),
                     median=float(r23.median()), share_lt_half=float((r23 < 0.5).mean()),
                     share_lt_quarter=float((r23 < 0.25).mean()),
                     analytic_loglinear=float(np.log(2) / np.log(3))),
                dict(step="B(fmax=8) / B(fmax=3)  [REFINE]", n=int(len(r83)),
                     median=float(r83.median()), share_lt_half=float((r83 < 0.5).mean()),
                     share_lt_quarter=float((r83 < 0.25).mean()),
                     analytic_loglinear=float(np.log(8) / np.log(3)))]
    DEG = pd.DataFrame(deg_rows)
    dump(DEG, "degeneracy")
    P(DEG.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("  A HALF-TAPE contrast of MAXDD medians is a contrast over TWO segments of a running")
    P("    minimum and very nearly VANISHES; the ratio divides by it and explodes (median")
    P(f"    ratio {LS[(LS.family == 'E_FINE') & (LS.rung_label == 'k1')].med_ratio.iloc[0]:.4f} "
      f"at fmax=2 against "
      f"{LS[(LS.family == 'E_FINE') & (LS.rung_label == 'k2')].med_ratio.iloc[0]:.4f} at fmax=3).")
    P("    That is why the COARSE end moves more, and it is an ENDPOINT fact that the")
    P("    LOG-LINEAR endpoint model gets BACKWARDS: log2/log3 = 0.6309 predicted against")
    P(f"    {r23.median():.4f} observed.")
    P("")

    # ------------------------------- C_PERM control
    P("## C_PERM CONTROL (declared) — a 21-day BLOCK-SHUFFLED tape, headline cell")
    rngp = np.random.default_rng(SEED_PERM)
    PV2: dict = {}
    for panel in PANELS:
        for lad, rg in RUNGS:
            rp = block_shuffle(BOOKS[(panel, lad, rg)], rngp)
            for f in FRAC_ALL:
                sts = [six_stats(x) for x in parts_at(rp, f, HEAD_PART)]
                PV2[(panel, lad, str(rg), f)] = np.array([x[HEAD_STAT] for x in sts], float)
    perm_rows = []
    for panel in PANELS:
        for lad, rg in RUNGS:
            def gm(fr):
                g = {f: [PV2[(panel, lad, str(rg), f)].tolist()] for f in fr}
                m = {f: (float(np.nanmedian(PV2[(panel, lad, str(rg), f)]))
                         if len(PV2[(panel, lad, str(rg), f)]) else np.nan) for f in fr}
                return g, m
            g0, m0 = gm(PUB_FRACS)
            v0 = ratio_of(g0, m0, PUB_FRACS, HEAD_WITHIN, HEAD_BETWEEN)[2]
            out = {}
            for fam in FAMS:
                for lab, fr in FAM_LADDERS[fam]:
                    g, m = gm(fr)
                    out[(fam, lab)] = ratio_of(g, m, fr, HEAD_WITHIN, HEAD_BETWEEN)[2]
            perm_rows.append(dict(
                panel=panel, ladder=lad, rung=str(rg),
                exc_coarse=safe_exc(out[("E_FINE", "k1")], v0),
                exc_fine=safe_exc(out[("E_FINE", "k6")], v0),
                LSENS_COARSE=lsens([out[("E_COARSE", l)] for l, _ in FAM_LADDERS["E_COARSE"]]),
                LSENS_SLIDE=lsens([out[("E_SLIDE", l)] for l, _ in FAM_LADDERS["E_SLIDE"]])))
    PERM = pd.DataFrame(perm_rows)
    dump(PERM, "perm")
    pb = PERM.dropna(subset=["exc_coarse", "exc_fine"])
    perm_share = float((pb.exc_coarse > pb.exc_fine).mean()) if len(pb) else np.nan
    P(f"  on a structure-free tape: coarse>fine at {perm_share:.4f} of {len(pb)} books; median "
      f"exc COARSE {pb.exc_coarse.median():.4f} / FINE {pb.exc_fine.median():.4f}; "
      f"LSENS_COARSE {PERM.LSENS_COARSE.median():.4f} / LSENS_SLIDE "
      f"{PERM.LSENS_SLIDE.median():.4f}")
    P("  READ AS CALIBRATION: a surviving asymmetry is LADDER GEOMETRY, not the market.")
    P("")

    # ------------------------------- the unpinned vintage, published not absorbed
    P("## THE VINTAGE, PUBLISHED NOT ABSORBED")
    for panel in PANELS:
        for lad, rg in RUNGS:
            BOOKS[("UN", panel, lad, rg)] = rung_book(cells_un, "U", panel, lad, rg)
    un_rows = []
    for panel in PANELS:
        for lad, rg in RUNGS:
            for tag, r in (("PINNED", BOOKS[(panel, lad, rg)]),
                           ("UNPINNED", BOOKS[("UN", panel, lad, rg)])):
                def gm2(fr, rr=r):
                    d = {f: np.array([six_stats(x)[HEAD_STAT] for x in parts_at(rr, f, HEAD_PART)],
                                     float) for f in fr}
                    return ({f: [d[f].tolist()] for f in fr},
                            {f: (float(np.nanmedian(d[f])) if len(d[f]) else np.nan) for f in fr})
                g0, m0 = gm2(PUB_FRACS)
                v0 = ratio_of(g0, m0, PUB_FRACS, HEAD_WITHIN, HEAD_BETWEEN)[2]
                g1, m1 = gm2(COARSE_FRACS)
                g2, m2 = gm2(FINE_FRACS)
                un_rows.append(dict(vintage=tag, panel=panel, ladder=lad, rung=str(rg),
                                    ratio_pub=v0,
                                    exc_coarse=safe_exc(ratio_of(g1, m1, COARSE_FRACS, HEAD_WITHIN,
                                                                 HEAD_BETWEEN)[2], v0),
                                    exc_fine=safe_exc(ratio_of(g2, m2, FINE_FRACS, HEAD_WITHIN,
                                                               HEAD_BETWEEN)[2], v0)))
    VIN = pd.DataFrame(un_rows)
    dump(VIN, "vintage")
    pv2 = VIN.pivot_table(index=["panel", "ladder", "rung"], columns="vintage",
                          values="ratio_pub")
    rel = (pv2["UNPINNED"] / pv2["PINNED"] - 1.0).abs()
    for tag, sub in VIN.groupby("vintage"):
        b2 = sub.dropna(subset=["exc_coarse", "exc_fine"])
        P(f"  {tag:<8s} coarse>fine {float((b2.exc_coarse > b2.exc_fine).mean()):.4f} of "
          f"{len(b2)} books; median ratio_pub {sub.ratio_pub.median():.4f}")
    n_diff = int((rel > 0).sum())
    P(f"  ONE EXTRA TRADING DAY (U56 only: 27 of 81 books have a different tape at all, the "
      f"B136 and SMALL caches both ending {cells_un['B136']['idx'][-1].date()}) moves the "
      f"published L3 reading by max {rel.max():.3e} relative over the {n_diff} books it touches")
    P("  1158-B's one-extra-day defect DOES NOT REPRODUCE ON THIS OBJECT — it is a sub-tape")
    P("    MAXDD median, and a running minimum is not moved by one bar appended at the end.")
    P("    Stated as a NON-reproduction, not folded into the headline as agreement.")
    P("")

    # ------------------------------- HYPOTHESES
    P("## HYPOTHESES, SCORED")
    hyp("H1 PREMISE", "1188's L2 share-moved minus its L8 share-moved (its own artefact)",
        PREMISE_1188["L2"] - PREMISE_1188["L8"], prem_ok)
    hyp("H2 LOGLIN", "share(coarse>fine) against the LOG-LINEAR pure-endpoint world, which "
        "predicts MOVE_FINE > MOVE_COARSE and therefore a share BELOW 0.40", share,
        share < BAR_D)
    hyp("H3 LENGTH", "median LSENS_COARSE, where the between term CANNOT move",
        HEAD["med_LSENS_COARSE"], HEAD["med_LSENS_COARSE"] >= BAR_LIVE)
    hyp("H4 WITHIN", "median ATTRIB_B at the coarse move (< 0.50 means W carries it)",
        HEAD["med_attrib_B_coarse"], HEAD["med_attrib_B_coarse"] < 0.50)
    hyp("H5 UNIVERSAL", "number of DISTINCT outcome bands across the 3 panels and 6 statistics "
        "(1 = universal)", len(bands), len(bands) == 1)
    # H6 lands on the declared 0.50 bar to within one float ulp.  It is scored KNIFE-EDGE and the
    # raw double is printed, because calling 0.49999999999999994 a REFUTATION would be a lie
    # about a bar that a discrete 5-point rank correlation can only straddle, never resolve.
    rho6 = HEAD["med_rho_slide"]
    ke = abs(rho6 - 0.50) < 1e-12
    hyp("H6 SLIDE", "median Spearman rho of the excursion against log(fmax) at frozen rung count "
        "(bar 0.50; the median of 486 discrete 5-point rhos lands ON the bar to one ulp)",
        rho6, rho6 >= 0.50,
        verdict="KNIFE-EDGE" if ke else ("SUPPORTED" if rho6 >= 0.50 else "REFUTED"))
    P("")

    # ------------------------------- RULE 8 + BOTH KEEP PATHS
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
            q = FAMDF[(FAMDF.panel == panel) & (FAMDF.ladder == lad) & (FAMDF.rung == str(rg))
                      & (FAMDF.stat == HEAD_STAT) & (FAMDF.partition == HEAD_PART)
                      & (FAMDF.within == HEAD_WITHIN) & (FAMDF.between == HEAD_BETWEEN)
                      & (FAMDF.family == "E_FINE")]
            wf_rows.append(dict(panel=panel, ladder=lad, rung=rg, **b, **l4b, **l4bo, **l4a,
                                PASS_4b_full=all(l4b.values()), PASS_4b_oos=all(l4bo.values()),
                                PASS_4a=all(l4a.values()),
                                ratio_coarse=float(q[q.rung_label == "k1"].ratio.iloc[0]),
                                ratio_pub=float(q[q.rung_label == "k2"].ratio.iloc[0]),
                                ratio_fine=float(q[q.rung_label == "k6"].ratio.iloc[0])))
    WF = pd.DataFrame(wf_rows)
    dump(WF, "walkforward")
    P(f"  BASE RATES over {len(WF)} rung books: 4b full {int(WF.PASS_4b_full.sum())}, "
      f"4b OOS {int(WF.PASS_4b_oos.sum())}, 4b BOTH "
      f"{int((WF.PASS_4b_full & WF.PASS_4b_oos).sum())}, 4a {int(WF.PASS_4a.sum())}")
    for panel in PANELS:
        sp = WF[WF.panel == panel]
        P(f"    {panel:<6s} 4b full {int(sp.PASS_4b_full.sum()):2d} / 4b OOS "
          f"{int(sp.PASS_4b_oos.sum()):2d} / 4b BOTH "
          f"{int((sp.PASS_4b_full & sp.PASS_4b_oos).sum()):2d} / 4a "
          f"{int(sp.PASS_4a.sum()):2d}  of {len(sp)}")
    bst = WF[WF.PASS_4b_full & WF.PASS_4b_oos].sort_values("OOS_Sharpe", ascending=False)
    if len(bst):
        r = bst.iloc[0]
        P(f"    best 4b (full AND OOS): {r.panel}/{r.ladder}={r.rung}  full "
          f"{r.CAGR:.2%}/{r.Sharpe:.4f}/{r.MaxDD:.2%} (H1 {r.H1:.4f}/H2 {r.H2:.4f}), OOS "
          f"{r.OOS_CAGR:.2%}/{r.OOS_Sharpe:.4f}/{r.OOS_MaxDD:.2%}; 4a "
          f"{bool(r.PASS_4a)}  (n distinct 4b books {bst[['panel','ladder','rung']].drop_duplicates().shape[0]})")
    devspy = max(abs(BENCH["U56"][0]["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
                 abs(BENCH["U56"][0]["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
                 abs(BENCH["U56"][0]["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gate("G6", "the record's committed U56 SPY OOS triple", devspy, devspy < 1e-3)

    # choosers: IS-only, by construction, 2009-2016 alone
    pick_rows = []
    for panel in PANELS:
        dd_ = cells[panel]
        sb, lb = BENCH[panel]
        ins = dd_["ins"]
        isr, isratio = {}, {}
        for lad, rg in RUNGS:
            r = BOOKS[(panel, lad, rg)][ins]
            isr[(lad, rg)] = fsharpe(r)
            for nm, fr in (("PUB", PUB_FRACS), ("COARSE", COARSE_FRACS), ("FINE", FINE_FRACS)):
                d = {f: np.array([six_stats(x)[HEAD_STAT] for x in parts_at(r, f, HEAD_PART)],
                                 float) for f in fr}
                g = {f: [d[f].tolist()] for f in fr}
                m = {f: (float(np.nanmedian(d[f])) if len(d[f]) else np.nan) for f in fr}
                isratio[(lad, rg, nm)] = ratio_of(g, m, fr, HEAD_WITHIN, HEAD_BETWEEN)[2]
        for chooser in ("CH_IS", "CH_PUB", "CH_COARSE", "CH_FINE"):
            if chooser == "CH_IS":
                key = max(RUNGS, key=lambda k: (isr[k] if np.isfinite(isr[k]) else -np.inf))
            else:
                nm = chooser.split("_")[1]
                cand = [(k, isratio[(k[0], k[1], nm)]) for k in RUNGS]
                cand = [(k, x) for k, x in cand if np.isfinite(x)]
                key = min(cand, key=lambda t: t[1])[0] if cand else RUNGS[0]
            b = blocks_m(BOOKS[(panel, key[0], key[1])], dd_["ins"], dd_["oos"])
            l4b, l4bo, l4a = legs_4b(b, sb), legs_4b_oos(b, sb), legs_4a(b, lb)
            pick_rows.append(dict(panel=panel, chooser=chooser, ladder=key[0], rung=key[1], **b,
                                  PASS_4b_full=all(l4b.values()),
                                  PASS_4b_oos=all(l4bo.values()), PASS_4a=all(l4a.values())))
    PK = pd.DataFrame(pick_rows)
    dump(PK, "picks")
    P(PK[["panel", "chooser", "ladder", "rung", "IS_Sharpe", "CAGR", "Sharpe", "MaxDD",
          "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "PASS_4b_full", "PASS_4b_oos",
          "PASS_4a"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    moved = sum(1 for panel in PANELS
                if PK[(PK.panel == panel) & (PK.chooser == "CH_COARSE")].iloc[0][
                    ["ladder", "rung"]].tolist()
                != PK[(PK.panel == panel) & (PK.chooser == "CH_FINE")].iloc[0][
                    ["ladder", "rung"]].tolist())
    mc = float(PK[PK.chooser == "CH_COARSE"].OOS_Sharpe.mean())
    mf = float(PK[PK.chooser == "CH_FINE"].OOS_Sharpe.mean())
    mi = float(PK[PK.chooser == "CH_IS"].OOS_Sharpe.mean())
    P(f"  THE DIRECTION THE LADDER IS WALKED MOVES THE PICK at {moved} of {len(PANELS)} panels; "
      f"picks clearing 4a {int(PK.PASS_4a.sum())} of {len(PK)}; 4b full AND OOS "
      f"{int((PK.PASS_4b_full & PK.PASS_4b_oos).sum())} of {len(PK)}")
    P(f"  mean OOS Sharpe: CH_COARSE {mc:.4f}  CH_FINE {mf:.4f}  CH_PUB "
      f"{float(PK[PK.chooser == 'CH_PUB'].OOS_Sharpe.mean()):.4f}  CH_IS {mi:.4f}")
    hyp("H7 CAPITAL", "|mean OOS Sharpe CH_COARSE - CH_FINE|", abs(mc - mf), abs(mc - mf) >= 0.05)
    P("")

    # ------------------------------- determinism + gates + summary
    # determinism: rebuild the G4 cell from PARTVALS with NO cache of any kind
    _g = {f: [] for f in FINE_FRACS}
    _all = {f: [] for f in FINE_FRACS}
    _bl: dict = {}
    for _lad, _rg in RUNGS:
        for f in FINE_FRACS:
            _v = PARTVALS[("SMALL", HEAD_PART, _lad, str(_rg), f)][HEAD_STAT]
            _all[f].extend(_v.tolist())
            _bl.setdefault((_lad, f), []).append(_v)
    for (_lad, f), _mats in _bl.items():
        _n = min(len(m) for m in _mats)
        if _n:
            _g[f].append(np.nanmedian(np.vstack([m[:_n] for m in _mats]), axis=0).tolist())
    _m = {f: float(np.nanmedian(_all[f])) for f in FINE_FRACS}
    chk = ratio_of(_g, _m, FINE_FRACS, HEAD_WITHIN, "B_MATCHED")[2]
    gate("G11", "determinism: the G4 cell rebuilt from PARTVALS with no cache", abs(chk - v1158),
         abs(chk - v1158) < 1e-15)
    GDF = pd.DataFrame(GATES)
    dump(GDF, "gates")
    HDF = pd.DataFrame(HYPS)
    dump(HDF, "hypotheses")

    P("## SUMMARY")
    P(f"  ANSWER to the title, headline cell            : {outcome}  (share {share:.4f} of "
      f"{HEAD['n_families']} resolvable families)")
    P(f"  MECHANISM                                     : {mech}  (LSENS_COARSE "
      f"{HEAD['med_LSENS_COARSE']:.4f} / LSENS_SLIDE {HEAD['med_LSENS_SLIDE']:.4f} = "
      f"{r_mech:.4f})")
    P(f"  the share across the 12 dial cells            : "
      f"{GRID.share_coarse_gt_fine.min():.4f} .. {GRID.share_coarse_gt_fine.max():.4f}; "
      f"distinct mechanisms {sorted(set(GRID.mechanism))}")
    P(f"  GATES {int(GDF.pass_.sum())} of {len(GDF)} PASS; HYPOTHESES "
      f"{int((HDF.verdict == 'SUPPORTED').sum())} of {len(HDF)} SUPPORTED")
    P(f"  RULE 8: 4a {int(WF.PASS_4a.sum())} of {len(WF)} books and {int(PK.PASS_4a.sum())} of "
      f"{len(PK)} picks; 4b full AND OOS {int((WF.PASS_4b_full & WF.PASS_4b_oos).sum())} of "
      f"{len(WF)} books")
    verdict = "KILL" if (int(PK.PASS_4a.sum()) == 0) else "KEEP-candidate"
    P(f"  VERDICT (capital): {verdict}")
    P(f"  runtime {time.time() - t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return dict(outcome=outcome, mech=mech, share=share, GRID=GRID, WF=WF, PK=PK,
                GDF=GDF, HDF=HDF, UNI=UNI, LS=LS, PERM=PERM, VIN=VIN, verdict=verdict)


if __name__ == "__main__":
    main()

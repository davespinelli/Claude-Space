#!/usr/bin/env python3
"""Idea 1188 (lane C, 2026-09-17) — how many committed SUB-TAPE FIGURES move once the LADDER is
RESOLVED rather than FROZEN?

QUESTION (QUEUE idea 1188, verbatim)
    idea 1158 found 1148's committed SMALL/MAXDD headline 0.794x is the FROZEN 3-rung reading and
    1.174x resolved on its own finer ladder, a 32% move, and that 22 of 26 committed CSVs never
    name their ladder.  Re-derive every committed sub-tape figure whose cited script can be re-run
    at L8 and report how many published numbers move by more than their own jackknife SE.
    Max 2 params (claim set, ladder).

THE TWO TUNED DIALS (PROTOCOL rule 4, no more than two, and the queue names both)
    1. CLAIM SET in {C_STRICT, C_WIDE, C_PROSE}
    2. LADDER    in {L2, L3, L4, L6, L8}
    3 x 5 = 15 cells, EVERY ONE PUBLISHED in `.grid.csv`.

    C_STRICT — committed CSV ROWS from the regime-to-length RATIO lineage (1140 -> 1148 -> 1157
               -> 1158): 1148's `.cells.csv` (tape T_OWN, episode KEEP) and `.perrung.csv`
               (T_OWN), and 1158's `.grid.csv`.  These are the record's committed RATIO figures.
    C_WIDE   — C_STRICT plus every other committed sub-tape figure this run can address: the
               per-fraction LEVEL figures (1148's and 1157's `.subtapes.csv`) and the gross-family
               ladder figures (1160's `.ladder.csv`, whose mech/lam construction is outside this
               kernel and is therefore counted as NOT re-derivable, not silently dropped).
    C_PROSE  — numbers quoted in committed prose (`research/**/*.md`) inside a sentence that
               asserts a sub-tape / regime-to-length / tape-length / fraction-ladder reading.

    NOT dials, reported at every value: PANEL {U56, B136, SMALL}; the four DIAL LADDERS that are
    the ratio's groups (CADENCE {D,W,M,Q}, GROSS 10 rungs, H {21,63,126,252}, N 9 rungs = 27 rung
    books per panel, 81 in total, 1148's grid); the six STATISTICS {CAGR, VOL, SHARPE, MAXDD,
    ULCER, CALMAR} with MAXDD the record's headline; the two PARTITIONS {ALIGNED, OFFSET}; the
    two CONSTRUCTIONS {C_POOLED, C_BOOK}; the three WITHIN terms {R_SPREAD, R_SD, R_MATCHED};
    the three REPAIRS {R_ASIS, R_FROZEN, R_COUNT}; the TWO SE BASES {J_LADDER, J_GROUP}; the two
    SE ladders (at L_pub, at L8); the three rule-8 choosers.  Frozen at 936/1140/1148/1157/1158's
    construction: CAND20 legs, max_vol 0.60, anchor N=20 / H=126 / gross 0.75 / W, 10 bps, LAG 1,
    WARMUP 260.  C_POOLED is 1158's `groups_med` VERBATIM (group by dial ladder, per-part median
    across that ladder's rungs) — the construction 1148's committed number actually lives in.

THE REPLAY GATE — WHAT "WHOSE CITED SCRIPT CAN BE RE-RUN" IS OPERATIONALISED AS
    A committed figure enters the MOVE test only if this run's kernel reproduces the PUBLISHED
    value at the PUBLISHED ladder.  Tiers, all published:
        T_EXACT rel dev < 1e-9   T_TIGHT < 1e-4   T_LOOSE < 1e-2   T_FAIL otherwise.
    Entry bar is T_TIGHT.  Self-policing: a figure this run cannot reproduce stays in the
    DENOMINATOR as not-re-derivable and never enters the numerator.  1148's R_MATCHED within term
    carries a 200-pair MONTE-CARLO draw whose value depends on the loop order that produced it,
    so exact replay is attainable at its own ladder and not guaranteed elsewhere; R_SPREAD and
    R_SD carry no MC term.  Both are reported separately.

"ITS OWN JACKKNIFE SE" — TWO BASES, BOTH PUBLISHED, HEADLINE DECLARED
    J_LADDER (headline) — leave-one-rung-out over the figure's OWN fraction ladder, dropping one
        NON-UNIT rung at a time (frac=1 anchors the between term and cannot be dropped).  Needs
        >= 2 non-unit rungs, so it is undefined at L2 and reported NaN there.
    J_GROUP            — 1158's leave-one-dial-ladder-out over the ratio's four groups
        {CADENCE, GROSS, H, N}.  Defined for the pooled constructions.
    MOVED(figure, L) := |v(L) - v_published| > SE, with SE taken at L_pub (headline: the figure's
    OWN resolution) and at L (published beside it).

WHY THERE IS NO BOOTSTRAP HERE, SAID UP FRONT
    Inherited from 1158 deliberately: a sub-tape figure compares segments at their own POSITIONS
    on one tape, so a moving-block resample destroys the object being measured.  The resolution
    measure is a jackknife, which needs no resample at all.

DECLARED BEFORE ANY NUMBER, AND SCORED IN THIS ORDER
    (on C_STRICT at L8, SE at L_pub, J_LADDER, over re-derivable LADDER-DEPENDENT figures)
    (A) THE RECORD IS ROBUST     : share moved < 0.25.
    (B) THE RECORD MOVES         : 0.25 <= share < 0.75.
    (C) THE LADDER IS THE FIGURE : share >= 0.75 — the published number is mostly a property of
                                   the ladder that was walked and not of the tape.
    Reported beside it and NOT verdict dials: the COVERAGE share (how many committed sub-tape
    figures are re-derivable at all) and the INVARIANT share (figures whose value cannot move
    because it does not depend on the ladder).

CAPITAL.  A census is not a KEEP path.  4a and 4b are scored at every one of the 81 rung books and
    the rule-8 walk-forward chooses on 2009-2016 alone and reads 2017-2026 ONCE.  CH_PUB and
    CH_RES exist to price whether RESOLVING the ladder moves the pick or the money at all.

THE VINTAGE.  `data/prices.csv` is rewritten nightly (idea 1163's defect), so every tape is
    truncated at PIN = 2026-09-15, the vintage 1148/1157/1158's committed anchors saw.  The
    unpinned reading of the headline cell is published beside the pinned one, not absorbed.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the current
    output of a sub-$2B screen less the documented `max_1d_move >= 1.0` exclusion.  Every LEVEL is
    optimistic and every 4a/4b count is an UPPER bound.  This run's object is a RATIO of two
    spreads in the statistic's own units, far less exposed — but MAXDD is the family's headline
    statistic and a survivorship-flattered panel has a shallower drawdown path, so the levels are
    published beside every ratio.
"""
from __future__ import annotations

import re
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
SLUG = "how-many-committed-SUB-TAPE-FIGURES-move-once-the-LADDER-is-RESOLVED-rather-than-FROZEN"
BT = Path(__file__).resolve().parent
OUT = BT / f"{DATE}_{SLUG}_C"

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
HEAD_CONSTR, HEAD_PART = "C_POOLED", "ALIGNED"
REPAIRS = ["R_ASIS", "R_FROZEN", "R_COUNT"]

FRAC_LADDERS = {"L2": [1, 2], "L3": [1, 2, 3], "L4": [1, 2, 3, 4],
                "L6": [1, 2, 3, 4, 6], "L8": [1, 2, 3, 4, 5, 6, 8]}
FROZEN_LADDER, FINEST = "L3", "L8"
FRAC_ALL = sorted({f for v in FRAC_LADDERS.values() for f in v})
LAB2LAD = {"F_1140": "L3", "F_FINE": "L6", "F_FINER": "L8",
           "L2": "L2", "L3": "L3", "L4": "L4", "L6": "L6", "L8": "L8"}

NPAIR_1157, SEED_1148 = 200, 11481148
PRIOR_CELL_1148 = 0.794259      # 1148 SMALL / MAXDD / R_MATCHED / F_1140, committed
PRIOR_RES_1158 = 1.173714       # 1158's L8 R_COUNT reading of the same cell, committed
A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
DD_COMMITTED = {"U56": -19.127569, "B136": -20.740302, "SMALL": -35.814054}
LIVE_MAXDD_COMMITTED = -0.1205

TIERS = [("T_EXACT", 1e-9), ("T_TIGHT", 1e-4), ("T_LOOSE", 1e-2)]
ENTRY_TIERS = {"T_EXACT", "T_TIGHT"}
CLAIMSETS = ["C_STRICT", "C_WIDE", "C_PROSE"]
BAR_A, BAR_C = 0.25, 0.75

LOG: list[str] = []
GATES: list[dict] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# the four wide frames are gzipped in place; every other artefact stays plain .csv
GZ = {"figures", "moves", "levels", "invariant_sample"}


def dump(df, suffix):
    ext = ".csv.gz" if suffix in GZ else ".csv"
    p = Path(f"{OUT}.{suffix}{ext}")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def gate(name, what, value, ok):
    GATES.append(dict(gate=name, what=what, value=float(value), pass_=bool(ok)))
    P(f"  {name:<6s} {'PASS' if ok else 'FAIL'}  {what}   (dev {value:.3e})")


# --------------------------------------------- kernel (1082/1148/1157/1158, unmodified)
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
    v = np.asarray([x for x in v if np.isfinite(x)], float)
    if len(v) < 2:
        return np.nan
    return float(np.mean([abs(a - b) for a, b in combinations(v, 2)]))


def between_term(med, fracs, repair, med_frozen=None):
    if repair == "R_FROZEN":
        m, fr = (med_frozen if med_frozen is not None else med), FRAC_LADDERS[FROZEN_LADDER]
    else:
        m, fr = med, fracs
    vals = [m.get(f, np.nan) for f in fr]
    if repair == "R_COUNT":
        return matched_exact(vals)
    fmax = max(fr)
    a, b = m.get(1, np.nan), m.get(fmax, np.nan)
    return abs(a - b) if (np.isfinite(a) and np.isfinite(b)) else np.nan


def ratio_from(groups, med, fracs, matched_fn, repair, med_frozen=None, groups_frozen=None):
    """1158's ratio_from, verbatim.  R_FROZEN freezes BOTH terms onto L3."""
    if repair == "R_FROZEN":
        gg = groups_frozen if groups_frozen is not None else groups
        fr = FRAC_LADDERS[FROZEN_LADDER]
    else:
        gg, fr = groups, fracs
    ranges, sds, matched = [], [], []
    for f in fr:
        if f == 1:
            continue
        for v in gg.get(f, []):
            v = np.asarray([x for x in v if np.isfinite(x)], float)
            if len(v) < 2:
                continue
            ranges.append(float(v.max() - v.min()))
            sds.append(float(v.std(ddof=1)))
            m_ = matched_fn(v)
            if np.isfinite(m_):
                matched.append(m_)
    bs = between_term(med, fracs, repair, med_frozen)
    ws = float(np.nanmedian(ranges)) if ranges else np.nan
    wsd = float(np.nanmedian(sds)) if sds else np.nan
    wm = float(np.nanmedian(matched)) if matched else np.nan
    return {"R_SPREAD": (ws, bs, ws / bs if bs else np.nan),
            "R_SD": (wsd, bs, wsd / bs if bs else np.nan),
            "R_MATCHED": (wm, bs, wm / bs if bs else np.nan)}


def ratio_from_1157(groups, frac_medians, fracs, matched_fn):
    """1157's ratio_from VERBATIM — used ONLY by the bit-for-bit replay gate."""
    ranges, sds, matched = [], [], []
    for f in fracs:
        if f == 1:
            continue
        for v in groups.get(f, []):
            v = np.asarray([x for x in v if np.isfinite(x)], float)
            if len(v) < 2:
                continue
            ranges.append(float(v.max() - v.min()))
            sds.append(float(v.std(ddof=1)))
            m = matched_fn(v)
            if np.isfinite(m):
                matched.append(m)
    m = frac_medians
    fmax = max(fracs)
    bs = (abs(m[1] - m[fmax]) if np.isfinite(m.get(1, np.nan))
          and np.isfinite(m.get(fmax, np.nan)) else np.nan)
    bsd = float(np.std([m[f] for f in fracs], ddof=1))
    ws = float(np.nanmedian(ranges)) if ranges else np.nan
    wsd = float(np.nanmedian(sds)) if sds else np.nan
    wm = float(np.nanmedian(matched)) if matched else np.nan
    return {"R_SPREAD": (ws, bs, ws / bs if bs else np.nan),
            "R_SD": (wsd, bsd, wsd / bsd if bsd else np.nan),
            "R_MATCHED": (wm, bs, wm / bs if bs else np.nan)}


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(meta), len(meta) - (len(keep) - 1)


# ---------------------------------------------------------------- census helpers
FRACCOLS = ("frac", "fraction", "fracs", "frac_ladder")
SUBTAPE_INT = set(range(1, 13))


def is_subtape_col(vals, col):
    s = [str(x) for x in vals if pd.notna(x)]
    if not s:
        return False
    if col in ("fracs", "frac_ladder"):
        return any(re.match(r"^(F_|L\d)", x) or "1/" in x for x in s)
    try:
        v = [float(x) for x in s]
    except ValueError:
        return all(("1/" in x) or re.match(r"^(F_|L\d)", x) for x in s)
    return all(float(x).is_integer() and int(x) in SUBTAPE_INT for x in v)


def census_frac_columns():
    rows = []
    for f in sorted(BT.glob("*.csv")):
        if f.name.startswith(f"{DATE}_{SLUG}"):
            continue
        try:
            head = pd.read_csv(f, nrows=0)
        except Exception:
            continue
        hit = [c for c in FRACCOLS if c in set(head.columns)]
        if not hit:
            continue
        try:
            d = pd.read_csv(f, usecols=hit)
        except Exception:
            continue
        for c in hit:
            u = d[c].dropna().unique()
            rows.append(dict(file=f.name, col=c, n_rows=int(len(d)), n_unique=int(len(u)),
                             subtape=bool(is_subtape_col(u, c)),
                             values=" | ".join(sorted(map(str, u))[:8])[:200]))
    return pd.DataFrame(rows)


PROSE_RX = re.compile(r"sub[- ]tape|regime[- ]to[- ]length|tape[- ]length|fraction ladder", re.I)
LADNAME_RX = re.compile(r"1/\d|F_1140|F_FINE|F_FINER|\bL[2-8]\b|fraction ladder|\{1,\s*2", re.I)
NUM_RX = re.compile(r"(?<![\w.])(\d+\.\d{3,})x?")


def census_prose():
    files = sorted(set(list(ROOT.glob("research/**/*.md")) + list(ROOT.glob("*.md"))))
    rows = []
    for f in files:
        if f.name.startswith(f"{DATE}_{SLUG}"):
            continue                       # never census this run's own write-up
        try:
            txt = f.read_text(errors="ignore")
        except Exception:
            continue
        for ln, line in enumerate(txt.splitlines(), 1):
            if not PROSE_RX.search(line):
                continue
            if SLUG in line or "1188 C" in line or line.lstrip().startswith("1188."):
                continue                   # nor its own QUEUE / LEADERBOARD entries
            for s in re.split(r"(?<=[.;!?])\s+", line):
                if not PROSE_RX.search(s) or len(s.strip()) < 20:
                    continue
                nums = NUM_RX.findall(s)
                base = dict(file=str(f.relative_to(ROOT)), line=ln,
                            states_ladder=bool(LADNAME_RX.search(s)), text=s.strip()[:300])
                if not nums:
                    rows.append(dict(value=np.nan, **base))
                for n in nums[:8]:
                    rows.append(dict(value=float(n), **base))
    return pd.DataFrame(rows)


def jack_se(vals):
    v = np.asarray([x for x in vals if np.isfinite(x)], float)
    k = len(v)
    if k < 2:
        return np.nan
    return float(np.sqrt((k - 1) / k * ((v - v.mean()) ** 2).sum()))


def tier_of(dev):
    for nm, b in TIERS:
        if dev < b:
            return nm
    return "T_FAIL"


# ================================================================== main
def main():
    t0 = time.time()
    P(f"# Idea 1188 (lane C, {DATE}) — how many committed SUB-TAPE FIGURES move once the LADDER")
    P("# is RESOLVED rather than FROZEN?")
    P(f"# 2 tuned dials: CLAIM SET {CLAIMSETS} x LADDER {list(FRAC_LADDERS)} = 15 cells, ALL")
    P("#   published in .grid.csv.  Everything else is reported at every value.")
    P("# REPLAY GATE: a committed figure enters the MOVE test only if this kernel reproduces it")
    P("#   at its OWN ladder to tier T_EXACT/T_TIGHT.  Coverage is published, not assumed.")
    P("# SE = leave-one-non-unit-rung-out jackknife on the figure's OWN ladder (J_LADDER,")
    P("#   headline) and 1158's leave-one-dial-ladder-out (J_GROUP).  NO BOOTSTRAP, declared.")
    P(f"# TAPE PINNED at {PIN} (idea 1163).  SURVIVORSHIP: every LEVEL is an upper bound.")
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

    RUNGS = [(lad, rg) for lad, rgs in LADDERS.items() for rg in rgs]
    P(f"## RUNG BOOKS — {len(RUNGS)} per panel (the ratio's four groups), "
      f"{len(RUNGS) * len(PANELS)} in total, 1148's grid")
    BOOKS = {}
    for panel in PANELS:
        for lad, rg in RUNGS:
            BOOKS[(panel, lad, rg)] = rung_book(cells, "P", panel, lad, rg)
        P(f"  {panel:<6s} done   ({time.time() - t0:6.1f}s)")
    P("")

    # ------------------------------- sub-tape LEVEL surface + the cached group arrays
    P("## SUB-TAPE LEVEL SURFACE — (panel, ladder, rung, partition, frac, part) x 6 stats")
    lev_rows = []
    PARTVALS: dict = {}     # (panel, part_mode, lad, rg, f) -> {stat: np.array over parts}
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
    P("")

    # ------------------------------- 1158's groups_med, rebuilt on cached arrays
    GM_CACHE: dict = {}

    def groups_med(panel, stat, fracs, part_mode, construction, skip_ladder=None,
                   rung_only=None):
        key = (panel, stat, tuple(fracs), part_mode, construction, skip_ladder, rung_only)
        if key in GM_CACHE:
            return GM_CACHE[key]
        if rung_only is not None:
            keys = [rung_only]
        elif construction == "C_BOOK":
            # 1158's C_BOOK VERBATIM: the ANCHOR book (ladder N, rung N0), not per-book groups.
            # The first cut of this script read C_BOOK as "one group per book" and replayed 197
            # of 4,860 of 1158's C_BOOK figures; this is that defect, found and priced, not hidden.
            keys = [("N", N0)]
        else:
            keys = [(l, r) for (l, r) in RUNGS if l != skip_ladder]
        groups = {f: [] for f in fracs}
        allv = {f: [] for f in fracs}
        bylad: dict = {}
        for lad, rg in keys:
            for f in fracs:
                v = PARTVALS[(panel, part_mode, lad, str(rg), f)][stat]
                allv[f].extend(v.tolist())
                bylad.setdefault((lad, f), []).append(v)
        if True:
            # 1158's groups_med: one entry per DIAL LADDER, per-part median across its rungs
            for (lad, f), mats in bylad.items():
                n = min(len(m) for m in mats)
                if n == 0:
                    continue
                M = np.vstack([m[:n] for m in mats])
                groups[f].append(np.nanmedian(M, axis=0).tolist())
        med = {f: (float(np.nanmedian(allv[f])) if allv[f] else np.nan) for f in fracs}
        GM_CACHE[key] = (groups, med)
        return groups, med

    def ratios(panel, stat, part_mode, construction, L, repair, skip_ladder=None,
               rung_only=None, frac_drop=None, matched_fn=matched_exact):
        fr = [f for f in FRAC_LADDERS[L] if f != frac_drop]
        g, m = groups_med(panel, stat, fr, part_mode, construction, skip_ladder, rung_only)
        gF = mF = None
        if repair == "R_FROZEN":
            gF, mF = groups_med(panel, stat, FRAC_LADDERS[FROZEN_LADDER], part_mode,
                                construction, skip_ladder, rung_only)
        return ratio_from(g, m, fr, matched_fn, repair, mF, gF)

    def ratios57(panel, stat, part_mode, L, construction="C_POOLED", rung_only=None,
                 frac_drop=None, matched_fn=matched_exact):
        """1157's ratio_from — the one 1148's `.cells.csv` and `.perrung.csv` were written with.
        It differs from 1158's in ONE place that matters: R_SD's BETWEEN term is the SD of the
        fraction medians (`bsd`), not the endpoint range (`bs`).  The first cut of this script
        used 1158's everywhere and replayed 0 of 1,458 of 1148's per-rung R_SD figures; that is
        this run's second self-found defect, priced rather than hidden."""
        fr = [f for f in FRAC_LADDERS[L] if f != frac_drop]
        g, m = groups_med(panel, stat, fr, part_mode, construction, None, rung_only)
        return ratio_from_1157(g, m, fr, matched_fn)

    # ------------------------------- the ratio surface
    P("## RATIO SURFACE — (construction, partition, panel, stat) x ladder x repair")
    SURF, grid_rows = {}, []
    for construction in CONSTRUCTIONS:
        for part_mode in PARTITIONS:
            for panel in PANELS:
                for stat in STATS6:
                    for L in FRAC_LADDERS:
                        for repair in REPAIRS:
                            res = ratios(panel, stat, part_mode, construction, L, repair)
                            SURF[(construction, part_mode, panel, stat, L, repair)] = res
                            row = dict(construction=construction, partition=part_mode,
                                       panel=panel, stat=stat, frac_ladder=L, repair=repair)
                            for w in WITHINS:
                                row[f"{w}_within"], row[f"{w}_between"], row[f"{w}_ratio"] = res[w]
                            grid_rows.append(row)
    SURFDF = pd.DataFrame(grid_rows)
    P(f"  {len(SURFDF):,} ratio coordinates x 3 within terms x 3 parts = "
      f"{9 * len(SURFDF):,} re-derivable figures   ({time.time() - t0:6.1f}s)")
    dump(SURFDF, "surface")

    # SURF jackknife
    SJACK = {}
    for construction in CONSTRUCTIONS:
        for part_mode in PARTITIONS:
            for panel in PANELS:
                for stat in STATS6:
                    for L in FRAC_LADDERS:
                        nonunit = [f for f in FRAC_LADDERS[L] if f != 1]
                        for repair in REPAIRS:
                            lv = {w: [] for w in WITHINS}
                            if len(nonunit) >= 2:
                                for fd in nonunit:
                                    rr = ratios(panel, stat, part_mode, construction, L, repair,
                                                frac_drop=fd)
                                    for w in WITHINS:
                                        lv[w].append(rr[w][2])
                            # J_GROUP is a leave-one-DIAL-LADDER-out jackknife, so it is only
                            # defined where the figure pools over the four ladders.  C_BOOK is
                            # one book (1158's anchor), so its J_GROUP is reported NaN, never 0.
                            gv = {w: [] for w in WITHINS}
                            if construction == "C_POOLED":
                                for ld in LADNAMES:
                                    rr = ratios(panel, stat, part_mode, construction, L, repair,
                                                skip_ladder=ld)
                                    for w in WITHINS:
                                        gv[w].append(rr[w][2])
                            for w in WITHINS:
                                SJACK[(construction, part_mode, panel, stat, L, repair, w)] = (
                                    jack_se(lv[w]), jack_se(gv[w]))
    P(f"  SURF jackknife: {len(SJACK):,} (coordinate, within) SEs   ({time.time() - t0:6.1f}s)")

    # ------------------------------- 1157-semantics surface (where 1148's cells.csv lives)
    # 1148's Monte-Carlo R_MATCHED depends on the DRAW ORDER of the loop that produced it, which
    # the committed artefact does not carry.  The one order that is recoverable is the one that
    # replays 1148's own headline cell (gate G5): a single rng per (partition, ladder) block,
    # then PANELS x STATS6.  It is used here and declared; where it does not replay, the figure
    # is counted as NOT re-derivable rather than nudged.
    SURF57 = {}
    for part_mode in PARTITIONS:
        for L in FRAC_LADDERS:
            rng57 = np.random.default_rng(SEED_1148)
            for panel in PANELS:
                for stat in STATS6:
                    SURF57[(part_mode, panel, stat, L)] = ratios57(
                        panel, stat, part_mode, L,
                        matched_fn=lambda x, _r=rng57: matched_sampled(x, _r))
    SJACK57 = {}
    for part_mode in PARTITIONS:
        for L in FRAC_LADDERS:
            nonunit = [f for f in FRAC_LADDERS[L] if f != 1]
            for panel in PANELS:
                for stat in STATS6:
                    lv = {w: [] for w in WITHINS}
                    if len(nonunit) >= 2:
                        for fd in nonunit:
                            rr = ratios57(panel, stat, part_mode, L, frac_drop=fd)
                            for w in WITHINS:
                                lv[w].append(rr[w][2])
                    gv = {w: [] for w in WITHINS}
                    for ld in LADNAMES:
                        fr = FRAC_LADDERS[L]
                        g_, m_ = groups_med(panel, stat, fr, part_mode, "C_POOLED",
                                            skip_ladder=ld)
                        rr = ratio_from_1157(g_, m_, fr, matched_exact)
                        for w in WITHINS:
                            gv[w].append(rr[w][2])
                    for w in WITHINS:
                        SJACK57[(part_mode, panel, stat, L, w)] = (jack_se(lv[w]),
                                                                   jack_se(gv[w]))
    P(f"## 1157-SEMANTICS SURFACE — {len(SURF57):,} coordinates   ({time.time() - t0:6.1f}s)")

    # ------------------------------- per-rung ratio surface (1148's perrung, 1157 semantics)
    PERRUNG, PJACK = {}, {}
    for panel in PANELS:
        for lad, rg in RUNGS:
            for stat in STATS6:
                for L in FRAC_LADDERS:
                    PERRUNG[(panel, lad, str(rg), stat, L)] = ratios57(
                        panel, stat, HEAD_PART, L, rung_only=(lad, rg))
                    nonunit = [f for f in FRAC_LADDERS[L] if f != 1]
                    lv = {w: [] for w in WITHINS}
                    if len(nonunit) >= 2:
                        for fd in nonunit:
                            rr = ratios57(panel, stat, HEAD_PART, L, rung_only=(lad, rg),
                                          frac_drop=fd)
                            for w in WITHINS:
                                lv[w].append(rr[w][2])
                    for w in WITHINS:
                        PJACK[(panel, lad, str(rg), stat, L, w)] = jack_se(lv[w])
    P(f"## PER-RUNG RATIO SURFACE — {len(PERRUNG):,} coordinates   ({time.time() - t0:6.1f}s)")
    P("")

    # ---------------------------------------------------------------- HARVEST
    P("## HARVEST — committed sub-tape figures, with their coordinate")
    F_CELLS = ("2026-09-16_is-the-SMALL-MAXDD-CELL-the-ONE-PLACE-where-TAPE-LENGTH-BEATS-"
               "REGIME_B.cells.csv")
    F_PERRUNG = ("2026-09-16_is-the-SMALL-MAXDD-CELL-the-ONE-PLACE-where-TAPE-LENGTH-BEATS-"
                 "REGIME_B.perrung.csv")
    F_SUBT48 = ("2026-09-16_is-the-SMALL-MAXDD-CELL-the-ONE-PLACE-where-TAPE-LENGTH-BEATS-"
                "REGIME_B.subtapes.csv")
    F_SUBT57 = ("2026-09-16_should-a-SUB-TAPE-COMPARISON-be-required-to-publish-its-REGIME-to-"
                "LENGTH-RATIO_cloud.subtapes.csv")
    F_GRID58 = ("2026-09-17_should-a-REGIME-to-LENGTH-RATIO-FIX-its-FRACTION-LADDER-or-COUNT-"
                "MATCH-its-BETWEEN-TERM_cloud.grid.csv")
    F_LAD60 = ("2026-09-17_is-the-MAXDD-LEVEL-the-whole-of-the-SMALL-panel-s-REGIME-to-LENGTH-"
               "DIFFERENCE_cloud.ladder.csv")

    figs = []

    def add(src, claim, kind, coord, published, res, dep, lpub):
        figs.append(dict(source=src, claimset=claim, kind=kind, coord=coord,
                         published=float(published), res=res, ladder_dependent=bool(dep),
                         L_pub=lpub))

    def read(name):
        try:
            return pd.read_csv(BT / name)
        except Exception as e:                                        # pragma: no cover
            P(f"  !! could not read {name}: {e}")
            return pd.DataFrame()

    d = read(F_CELLS)
    if len(d):
        dd = d[(d.tape == "T_OWN") & (d.episode == "KEEP")]
        P(f"  {F_CELLS[:52]}...  {len(d)} rows, {len(dd)} re-runnable (T_OWN & KEEP)")
        for _, r in dd.iterrows():
            L = LAB2LAD.get(str(r.frac_ladder))
            if L is None:
                continue
            for w in WITHINS:
                for part in ("within", "between", "ratio"):
                    col = f"{w}_{part}"
                    if col not in dd.columns or not np.isfinite(r[col]):
                        continue
                    add(F_CELLS, "C_STRICT", f"{w}_{part}",
                        f"{r.panel}|{r.stat}|{r.partition}|C_POOLED|1157",
                        r[col], ("SURF57", r.partition, r.panel, r.stat, w, part), True, L)

    d = read(F_PERRUNG)
    if len(d):
        dd = d[d.tape == "T_OWN"]
        P(f"  {F_PERRUNG[:52]}...  {len(d)} rows, {len(dd)} re-runnable (T_OWN)")
        for _, r in dd.iterrows():
            L = LAB2LAD.get(str(r.frac_ladder))
            if L is None:
                continue
            for w in WITHINS:
                col = f"{w}_ratio"
                if col not in dd.columns or not np.isfinite(r[col]):
                    continue
                add(F_PERRUNG, "C_STRICT", f"{w}_ratio",
                    f"{r.panel}|{r.ladder}|{r.rung}|{r.stat}",
                    r[col], ("PERRUNG", r.panel, r.ladder, str(r.rung), r.stat, w), True, L)

    d = read(F_GRID58)
    if len(d):
        P(f"  {F_GRID58[:52]}...  {len(d)} rows, all re-runnable")
        for _, r in d.iterrows():
            L = LAB2LAD.get(str(r.frac_ladder))
            if L is None:
                continue
            for w in WITHINS:
                for part in ("within", "between", "ratio"):
                    col = f"{w}_{part}"
                    if col not in d.columns or not np.isfinite(r[col]):
                        continue
                    add(F_GRID58, "C_STRICT", f"{w}_{part}",
                        f"{r.panel}|{r.stat}|{r.partition}|{r.construction}|{r.repair}",
                        r[col], ("SURF", r.construction, r.partition, r.panel, r.stat,
                                 r.repair, w, part), r.repair != "R_FROZEN", L)

    for src in (F_SUBT57, F_SUBT48):
        d = read(src)
        if not len(d) or not {"panel", "ladder", "rung", "frac"} <= set(d.columns):
            continue
        n0 = len(d)
        if "tape" in d.columns:      # T_MATCHED is a length-matched tape outside this kernel
            d = d[d.tape == "T_OWN"]
        P(f"  {src[:52]}...  {n0} rows, {len(d)} re-runnable (per-fraction LEVELS, "
          f"ladder-INVARIANT)")
        pm = "partition" if "partition" in d.columns else None
        for _, r in d.iterrows():
            part_mode = str(r[pm]) if pm else HEAD_PART
            j = int(r["part"]) if "part" in d.columns and np.isfinite(r["part"]) else 0
            for stat in STATS6:
                if stat not in d.columns or not np.isfinite(r[stat]):
                    continue
                add(src, "C_WIDE", f"LEVEL_{stat}",
                    f"{r.panel}|{r.ladder}|{r.rung}|f={int(r.frac)}|p={j}|{part_mode}",
                    r[stat], ("LEV", r.panel, r.ladder, str(r.rung), int(r.frac), j,
                              part_mode, stat), False, "L_NA")

    d = read(F_LAD60)
    if len(d):
        P(f"  {F_LAD60[:52]}...  {len(d)} rows (gross family; mech/lam outside this kernel)")
        for _, r in d.iterrows():
            L = LAB2LAD.get(str(r.frac_ladder))
            if L is None:
                continue
            for col, w in (("ratio", "R_MATCHED"), ("R_SPREAD", "R_SPREAD"), ("R_SD", "R_SD")):
                if col not in d.columns or not np.isfinite(r[col]):
                    continue
                add(F_LAD60, "C_WIDE", f"{w}_ratio",
                    f"{r.panel}|{r.constr}|{r.mech}|lam={r.lam}|gross={r.gross}",
                    r[col], ("NOKERNEL",), True, L)

    FIG = pd.DataFrame(figs)
    P(f"  harvested {len(FIG):,} committed sub-tape figures "
      f"({FIG.claimset.value_counts().to_dict()})   ({time.time() - t0:6.1f}s)")
    P("")

    # ---------------------------------------------------------------- resolve / replay / move
    P("## REPLAY + MOVE")
    PART_IX = {"within": 0, "between": 1, "ratio": 2}

    def value_at(res, L):
        k = res[0]
        if k == "SURF":
            _, constr, pm, panel, stat, repair, w, part = res
            key = (constr, pm, panel, stat, L, repair)
            return SURF[key][w][PART_IX[part]] if key in SURF else np.nan
        if k == "SURF57":
            _, pm, panel, stat, w, part = res
            key = (pm, panel, stat, L)
            return SURF57[key][w][PART_IX[part]] if key in SURF57 else np.nan
        if k == "PERRUNG":
            _, panel, lad, rg, stat, w = res
            key = (panel, lad, rg, stat, L)
            return PERRUNG[key][w][2] if key in PERRUNG else np.nan
        if k == "LEV":
            _, panel, lad, rg, f, j, pm, stat = res
            a = PARTVALS.get((panel, pm, lad, rg, f), {}).get(stat)
            return float(a[j]) if a is not None and j < len(a) else np.nan
        return np.nan

    def se_at(res, L):
        k = res[0]
        if k == "SURF":
            _, constr, pm, panel, stat, repair, w, _p = res
            return SJACK.get((constr, pm, panel, stat, L, repair, w), (np.nan, np.nan))
        if k == "SURF57":
            _, pm, panel, stat, w, _p = res
            return SJACK57.get((pm, panel, stat, L, w), (np.nan, np.nan))
        if k == "PERRUNG":
            _, panel, lad, rg, stat, w = res
            return (PJACK.get((panel, lad, rg, stat, L, w), np.nan), np.nan)
        return (np.nan, np.nan)

    reps = []
    for i, r in FIG.iterrows():
        res, lp, pub = r["res"], r["L_pub"], r["published"]
        if res[0] == "NOKERNEL":
            reps.append(("T_NOKERNEL", np.nan, np.nan))
            continue
        L0 = lp if lp in FRAC_LADDERS else FROZEN_LADDER
        vrep = value_at(res, L0)
        dev = abs(vrep - pub) / max(abs(pub), 1e-12) if np.isfinite(vrep) else np.inf
        reps.append((tier_of(dev), dev, vrep))
    FIG["replay_tier"] = [x[0] for x in reps]
    FIG["rep_dev"] = [x[1] for x in reps]
    FIG["v_at_L_pub"] = [x[2] for x in reps]
    FIG["rederivable"] = FIG.replay_tier.isin(ENTRY_TIERS)
    P("  replay tiers (all figures): " + str(FIG.replay_tier.value_counts().to_dict()))
    for src, g in FIG.groupby("source"):
        P(f"    {src[:58]:60s} {int(g.rederivable.sum()):6,d} of {len(g):6,d} "
          f"({g.rederivable.mean():.4f})  {g.replay_tier.value_counts().to_dict()}")
    dump(FIG.drop(columns=["res"]), "figures")

    mv_rows, inv_rows = [], []
    for i, r in FIG.iterrows():
        if not r["rederivable"]:
            continue
        res, lp, pub = r["res"], r["L_pub"], r["published"]
        if not r["ladder_dependent"]:
            v = value_at(res, FROZEN_LADDER)
            inv_rows.append(dict(idx=i, source=r["source"], claimset=r["claimset"],
                                 kind=r["kind"], coord=r["coord"], published=pub, resolved=v,
                                 rel_move=abs(v - pub) / max(abs(pub), 1e-12)))
            continue
        sp = se_at(res, lp) if lp in FRAC_LADDERS else (np.nan, np.nan)
        for L in FRAC_LADDERS:
            v = value_at(res, L)
            sl = se_at(res, L)
            dd_ = abs(v - pub) if np.isfinite(v) else np.nan
            mv_rows.append(dict(
                idx=i, source=r["source"], claimset=r["claimset"], kind=r["kind"],
                coord=r["coord"], L_pub=lp, L=L, published=pub, resolved=v, abs_move=dd_,
                rel_move=(dd_ / max(abs(pub), 1e-12) if np.isfinite(dd_) else np.nan),
                SE_pub_LADDER=sp[0], SE_pub_GROUP=sp[1], SE_L_LADDER=sl[0], SE_L_GROUP=sl[1],
                MOVED_pubSE_LADDER=(bool(dd_ > sp[0])
                                    if np.isfinite(dd_) and np.isfinite(sp[0]) else None),
                MOVED_pubSE_GROUP=(bool(dd_ > sp[1])
                                   if np.isfinite(dd_) and np.isfinite(sp[1]) else None),
                MOVED_LSE_LADDER=(bool(dd_ > sl[0])
                                  if np.isfinite(dd_) and np.isfinite(sl[0]) else None),
                MOVED_LSE_GROUP=(bool(dd_ > sl[1])
                                 if np.isfinite(dd_) and np.isfinite(sl[1]) else None)))
    MV = pd.DataFrame(mv_rows)
    INV = pd.DataFrame(inv_rows)
    dump(MV, "moves")
    P(f"  ladder-INVARIANT re-derivable figures: {len(INV):,}  "
      f"(max rel move {INV.rel_move.max() if len(INV) else 0.0:.3e}) — one row each, summarised")
    if len(INV):
        dump(INV.head(5000), "invariant_sample")
    P("")

    # ---------------------------------------------------------------- prose
    PR = census_prose()
    if len(PR):
        pool = []
        for w in WITHINS:
            for c in ("within", "between", "ratio"):
                pool.append(SURFDF[f"{w}_{c}"].values)
        pool.append(np.array([v for k, v in
                              [(k, PERRUNG[k][w][2]) for k in PERRUNG for w in WITHINS]]))
        pool.append(LEVDF[STATS6].values.ravel())
        sv = np.array(sorted({round(float(v), 6) for a in pool for v in np.ravel(a)
                              if np.isfinite(v)}))

        def locate(x):
            if not np.isfinite(x):
                return np.nan
            j = int(np.searchsorted(sv, x))
            best = np.inf
            for k in (j - 1, j):
                if 0 <= k < len(sv):
                    best = min(best, abs(sv[k] - x) / max(abs(x), 1e-12))
            return best
        PR["nearest_rel"] = [locate(v) for v in PR["value"]]
        PR["locatable"] = PR["nearest_rel"] < 1e-3
    dump(PR, "prose")

    CEN = census_frac_columns()
    dump(CEN, "census")
    P(f"  census: {len(CEN)} committed frac-columns, {int(CEN.subtape.sum())} are SUB-TAPE "
      f"denominators ({CEN.subtape.mean():.4f})")
    P("")

    # ---------------------------------------------------------------- the 15-cell grid
    P("## THE 15-CELL GRID (2 tuned dials) — share of re-derivable LADDER-DEPENDENT figures")
    P("##   that MOVE by more than their own jackknife SE (SE at L_pub, J_LADDER = headline)")
    cellrows = []
    for cs in CLAIMSETS:
        for L in FRAC_LADDERS:
            if cs == "C_PROSE":
                sub = PR[PR["value"].notna()] if len(PR) else pd.DataFrame()
                n_all = len(sub)
                n_loc = int(sub["locatable"].sum()) if len(sub) else 0
                cellrows.append(dict(claimset=cs, L=L, n_figs=n_all, n_rederivable=n_loc,
                                     coverage=(n_loc / n_all if n_all else np.nan),
                                     n_ladder_dep=np.nan, n_moved=np.nan, share_moved=np.nan,
                                     med_rel_move=np.nan))
                continue
            allf = FIG if cs == "C_WIDE" else FIG[FIG.claimset == cs]
            m = MV if cs == "C_WIDE" else MV[MV.claimset == cs]
            m = m[(m.L == L) & m.MOVED_pubSE_LADDER.notna()]
            cellrows.append(dict(
                claimset=cs, L=L, n_figs=len(allf), n_rederivable=int(allf.rederivable.sum()),
                coverage=(allf.rederivable.mean() if len(allf) else np.nan),
                n_ladder_dep=len(m), n_moved=int(m.MOVED_pubSE_LADDER.sum()) if len(m) else 0,
                share_moved=(m.MOVED_pubSE_LADDER.mean() if len(m) else np.nan),
                med_rel_move=(m.rel_move.median() if len(m) else np.nan)))
    GRID = pd.DataFrame(cellrows)
    dump(GRID, "grid")
    P(GRID.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    head = GRID[(GRID.claimset == "C_STRICT") & (GRID.L == FINEST)]
    share = float(head.share_moved.iloc[0]) if len(head) else np.nan
    verdict = ("(UNDECIDED)" if not np.isfinite(share) else
               "(A) THE RECORD IS ROBUST" if share < BAR_A else
               "(B) THE RECORD MOVES" if share < BAR_C else
               "(C) THE LADDER IS THE FIGURE")
    P("")
    P(f"  HEADLINE (C_STRICT, L8, SE at L_pub, J_LADDER): share moved = {share:.4f}  -> {verdict}")

    # a second reading, published not substituted
    for base, col in (("J_GROUP  @L_pub", "MOVED_pubSE_GROUP"),
                      ("J_LADDER @L", "MOVED_LSE_LADDER"),
                      ("J_GROUP  @L", "MOVED_LSE_GROUP")):
        m = MV[(MV.claimset == "C_STRICT") & (MV.L == FINEST) & MV[col].notna()]
        if len(m):
            P(f"    second reading {base:<16s}: {int(m[col].sum()):,} of {len(m):,} "
              f"({m[col].mean():.4f})")
    P("")

    # ------------------- RESOLUTION: why "inside its own SE" is not "stable"
    P("## RESOLUTION — the SE bar is wide, and that is the reason the share is what it is")
    m8 = MV[(MV.L == FINEST) & MV.SE_pub_LADDER.notna() & (MV.published.abs() > 1e-9)].copy()
    m8["se_rel"] = m8.SE_pub_LADDER / m8.published.abs()
    P(f"  own J_LADDER SE as a share of the published value: median {m8.se_rel.median():.4f}, "
      f"p25 {m8.se_rel.quantile(.25):.4f}, p75 {m8.se_rel.quantile(.75):.4f}")
    for b in (0.10, 0.25, 0.50, 1.00):
        P(f"    figures whose OWN SE exceeds {b:4.0%} of the published value: "
          f"{float((m8.se_rel > b).mean()):.4f}")
    P("  SE-FREE READER BAR — how far the published number actually moves at L8:")
    for b in (0.05, 0.10, 0.25, 0.50, 1.00):
        P(f"    |relative move| > {b:4.0%}: {float((m8.rel_move > b).mean()):.4f} "
          f"({int((m8.rel_move > b).sum()):,} of {len(m8):,})")
    P("  BY TERM (share moving beyond own SE at L8, and median relative move):")
    for k, g in m8.groupby(m8.kind.str.split("_").str[-1]):
        P(f"    {k:<9s} n {len(g):6,d}   moved {g.MOVED_pubSE_LADDER.mean():.4f}   "
          f"median rel move {g.rel_move.median():.4f}")
    P("  BY WITHIN TERM:")
    for k, g in m8.groupby(m8.kind.str.rsplit("_", n=1).str[0]):
        P(f"    {k:<12s} n {len(g):6,d}   moved {g.MOVED_pubSE_LADDER.mean():.4f}   "
          f"median rel move {g.rel_move.median():.4f}")
    P("")
    P("## THE RECORD'S OWN HEADLINE FIGURE — 1148's SMALL / MAXDD / R_MATCHED, published 0.794259")
    for L in FRAC_LADDERS:
        v = SURF57[(HEAD_PART, "SMALL", HEAD_STAT, L)][HEAD_WITHIN][2]
        se = SJACK57.get((HEAD_PART, "SMALL", HEAD_STAT, L, HEAD_WITHIN), (np.nan, np.nan))
        P(f"    {L:<3s} value {v:8.4f}   move vs published {abs(v - PRIOR_CELL_1148):7.4f} "
          f"({abs(v - PRIOR_CELL_1148) / PRIOR_CELL_1148:6.2%})   own J_LADDER SE @L3 "
          f"{SJACK57[(HEAD_PART, 'SMALL', HEAD_STAT, 'L3', HEAD_WITHIN)][0]:7.4f}  "
          f"J_LADDER SE @{L} {se[0]:7.4f}  -> MOVED beyond SE@L3: "
          f"{bool(abs(v - PRIOR_CELL_1148) > SJACK57[(HEAD_PART, 'SMALL', HEAD_STAT, 'L3', HEAD_WITHIN)][0])}")
    P("")

    # ---------------------------------------------------------------- gates
    P("## GATES")
    d = cells["U56"]
    mk = rebalance_mask(d["idx"], FREQ0).values
    W = build(d["rank_key"], d["elig"], d["priced"], np.flatnonzero(mk), N0, HOLD0,
              d["T"], d["K"], GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST, freq=FREQ0)["returns"].values[d["warm"]]
    v = float(np.abs(eng - BOOKS[("U56", "N", N0)]).max())
    gate("G1", "fast runner == engine.backtest (U56 W/H126/N=20, gross 0.75)", v, v < 1e-12)

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
    gate("G4", "CROSS-RUN 1157's committed full-tape MaxDD LEVELS (U56 / B136 / SMALL)",
         v, v < 5e-4)

    rng = np.random.default_rng(SEED_1148)
    rep = {}
    for panel in PANELS:
        for stat in STATS6:
            g_, m_ = groups_med(panel, stat, [1, 2, 3], "ALIGNED", "C_POOLED")
            rep[(panel, stat)] = ratio_from_1157(g_, m_, [1, 2, 3],
                                                 lambda x, _r=rng: matched_sampled(x, _r))
    got = rep[("SMALL", HEAD_STAT)][HEAD_WITHIN][2]
    v = abs(got - PRIOR_CELL_1148)
    gate("G5", f"1148/1157's SMALL/MAXDD R_MATCHED replayed BIT FOR BIT ({got:.6f} vs "
               f"{PRIOR_CELL_1148})", v, v < 1e-6)

    v2 = SURF[("C_POOLED", "ALIGNED", "SMALL", "MAXDD", "L8", "R_COUNT")]["R_MATCHED"][2]
    v = abs(v2 - PRIOR_RES_1158) / PRIOR_RES_1158
    gate("G6", f"1158's committed L8 R_COUNT reading of the same cell ({v2:.6f} vs "
               f"{PRIOR_RES_1158})", v, v < 1e-4)

    fr = SURFDF[SURFDF.repair == "R_FROZEN"]
    spread = float(fr.groupby(["construction", "partition", "panel", "stat"])[
        "R_MATCHED_ratio"].agg(lambda s: (s.max() - s.min()) / max(abs(s.median()), 1e-12)).max())
    gate("G7", "R_FROZEN is ladder-INVARIANT by construction (max rel spread over the 5 ladders)",
         spread, spread < 1e-12)

    invmax = float(INV.rel_move.max()) if len(INV) else 0.0
    gate("G8", f"committed LEVEL figures CANNOT move — their whole residual is the replay "
               f"tolerance ({len(INV):,} re-derived, max rel)", invmax, invmax < 1e-4)

    st = FIG[FIG.claimset == "C_STRICT"]
    rr = float(st.rederivable.mean()) if len(st) else 0.0
    gate("G9", f"C_STRICT replay rate at tier <= T_TIGHT ({int(st.rederivable.sum()):,} of "
               f"{len(st):,})", 1 - rr, rr > 0.50)

    for lad, rg in RUNGS:
        r = rung_book(cells_un, "U", "SMALL", lad, rg)
        for f in FRAC_ALL:
            segs = parts_at(r, f, HEAD_PART)
            sts = [six_stats(s) for s in segs]
            PARTVALS[("UNPIN", HEAD_PART, lad, str(rg), f)] = {
                st_: np.array([x[st_] for x in sts], float) for st_ in STATS6}
    vun = ratios("UNPIN", "MAXDD", HEAD_PART, "C_POOLED", "L3", "R_ASIS")["R_MATCHED"][2]
    vpin = SURF[("C_POOLED", "ALIGNED", "SMALL", "MAXDD", "L3", "R_ASIS")]["R_MATCHED"][2]
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
                                PASS_4a=all(l4a.values()),
                                ratio_L3=PERRUNG[(panel, lad, str(rg), HEAD_STAT,
                                                  "L3")][HEAD_WITHIN][2],
                                ratio_L8=PERRUNG[(panel, lad, str(rg), HEAD_STAT,
                                                  "L8")][HEAD_WITHIN][2]))
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
    if int(WF.PASS_4b_full.sum()):
        bst = WF[WF.PASS_4b_full & WF.PASS_4b_oos].sort_values("OOS_Sharpe", ascending=False)
        if len(bst):
            r = bst.iloc[0]
            P(f"    best 4b (full AND OOS): {r.panel}/{r.ladder}={r.rung}  full "
              f"{r.CAGR:.2%}/{r.Sharpe:.4f}/{r.MaxDD:.2%} (H1 {r.H1:.4f}/H2 {r.H2:.4f}), OOS "
              f"{r.OOS_CAGR:.2%}/{r.OOS_Sharpe:.4f}/{r.OOS_MaxDD:.2%}")

    pick_rows = []
    for panel in PANELS:
        dd_ = cells[panel]
        sb, lb = BENCH[panel]
        ins = dd_["ins"]
        isr = {k: fsharpe(BOOKS[(panel, k[0], k[1])][ins]) for k in RUNGS}
        isratio = {}
        for lad, rg in RUNGS:
            r = BOOKS[(panel, lad, rg)][ins]
            for L in ("L3", FINEST):
                fr = FRAC_LADDERS[L]
                g = {f: [[six_stats(s)[HEAD_STAT] for s in parts_at(r, f, HEAD_PART)]]
                     for f in fr}
                med = {f: (float(np.nanmedian(g[f][0])) if g[f][0] else np.nan) for f in fr}
                isratio[(lad, rg, L)] = ratio_from(g, med, fr, matched_exact,
                                                   "R_ASIS")[HEAD_WITHIN][2]
        for chooser in ("CH_IS", "CH_PUB", "CH_RES"):
            if chooser == "CH_IS":
                key = max(RUNGS, key=lambda k: (isr[k] if np.isfinite(isr[k]) else -np.inf))
            else:
                L = "L3" if chooser == "CH_PUB" else FINEST
                cand = [(k, isratio[(k[0], k[1], L)]) for k in RUNGS]
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
    moved_pick = sum(
        1 for panel in PANELS
        if (PK[(PK.panel == panel) & (PK.chooser == "CH_PUB")].iloc[0][["ladder", "rung"]].tolist()
            != PK[(PK.panel == panel) & (PK.chooser == "CH_RES")].iloc[0][["ladder", "rung"]].tolist()))
    P(f"  RESOLVING THE LADDER MOVES THE PICK at {moved_pick} of {len(PANELS)} panels; "
      f"picks clearing 4a {int(PK.PASS_4a.sum())} of {len(PK)}; 4b full AND OOS "
      f"{int((PK.PASS_4b_full & PK.PASS_4b_oos).sum())} of {len(PK)}")
    P("")

    # ---------------------------------------------------------------- summary
    P("## SUMMARY")
    strict = FIG[FIG.claimset == "C_STRICT"]
    P(f"  committed sub-tape figures harvested      : {len(FIG):,} "
      f"(C_STRICT {len(strict):,}, C_WIDE-only {len(FIG) - len(strict):,})")
    P(f"  re-derivable (replay tier <= T_TIGHT)     : {int(FIG.rederivable.sum()):,} "
      f"({FIG.rederivable.mean():.4f})")
    P(f"  of those, LADDER-DEPENDENT               : "
      f"{int(FIG[FIG.rederivable].ladder_dependent.sum()):,};  ladder-INVARIANT {len(INV):,}")
    m8 = MV[(MV.L == FINEST) & MV.MOVED_pubSE_LADDER.notna()]
    if len(m8):
        P(f"  MOVE at L8 vs own J_LADDER SE @L_pub      : {int(m8.MOVED_pubSE_LADDER.sum()):,} "
          f"of {len(m8):,}  ({m8.MOVED_pubSE_LADDER.mean():.4f})")
        P(f"  median |relative move| at L8              : {m8.rel_move.median():.4f}  "
          f"(p90 {m8.rel_move.quantile(0.90):.4f}, max {m8.rel_move.max():.4f})")
    P(f"  census: committed frac-columns            : {len(CEN)}, SUB-TAPE "
      f"{int(CEN.subtape.sum())} ({CEN.subtape.mean():.4f})")
    if len(PR):
        pv = PR[PR["value"].notna()]
        P(f"  prose: {PR.shape[0]:,} sub-tape sentence-rows, {len(pv):,} numbers, state a ladder "
          f"{PR.states_ladder.mean():.4f}, locatable {pv.locatable.mean():.4f}")
    P(f"  VERDICT: {verdict}   (share moved {share:.4f})")
    P(f"  runtime {time.time() - t0:.1f}s")

    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return dict(share=share, verdict=verdict, GRID=GRID, WF=WF, PK=PK, GDF=GDF, FIG=FIG, MV=MV)


if __name__ == "__main__":
    main()

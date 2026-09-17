#!/usr/bin/env python3
"""Idea 1158 (lane cloud, 2026-09-17) — should a REGIME-to-LENGTH RATIO FIX its FRACTION LADDER
or COUNT-MATCH its BETWEEN TERM?

QUESTION (QUEUE idea 1158, verbatim)
    idea 1157 found 1148's ratio falls 0.39x-0.59x on every panel when the fraction ladder is
    extended from 1/3 to 1/8, because the BETWEEN term is a range over the ladder's ENDPOINTS and
    grows with the ladder while the length-matched WITHIN term does not — the exact count-inflation
    defect 1148 corrected in the within term and never checked in the between.  Price the two
    repairs (a ladder frozen in the clause vs a count-matched between term) on the record's
    committed sub-tape rows and report which makes two runs comparable.  Max 2 params (repair,
    fraction ladder).

THE TWO TUNED DIALS (PROTOCOL rule 4, no more than two, and the queue names both)
    1. REPAIR          in {R_ASIS, R_FROZEN, R_COUNT}
    2. FRACTION LADDER in {L2, L3, L4, L6, L8}
    3 x 5 = 15 cells, EVERY ONE PUBLISHED in `.grid.csv`, at every (panel, statistic,
    construction, partition).

    R_ASIS   — 1148/1157's between term VERBATIM: |m[1] - m[fmax]|, the difference between the
               full-tape median and the SHORTEST sub-tape's median.  A two-point range over the
               ladder's ENDPOINTS, so extending the ladder moves one of its two points.
    R_FROZEN — the clause names the ladder.  Both terms are computed on L3 = {1,2,3} (1140's
               ladder, where 1148's committed number lives) NO MATTER what ladder the run walked.
               Comparable across ladders by CONSTRUCTION — the whole question is what it costs.
    R_COUNT  — the between term is the EXACT mean |difference| over all C(k,2) pairs of the
               ladder's fraction-medians: the same count-free statistic 1148 used to repair the
               WITHIN term, now applied to the between.  This is the queue's second repair.

    NOT dials, reported at every value: PANEL {U56, B136, SMALL}; the four DIAL LADDERS that are
    the ratio's groups (CADENCE {D,W,M,Q}, GROSS 10 rungs, H {21,63,126,252}, N 9 rungs = 27 rung
    books per panel, 81 in total, 1148's grid); the six STATISTICS {CAGR, VOL, SHARPE, MAXDD,
    ULCER, CALMAR} with MAXDD the record's headline; the two PARTITIONS {ALIGNED, OFFSET}; the
    two CONSTRUCTIONS {C_POOLED (where 1148's committed number lives), C_BOOK}; the three
    WITHIN-term statistics {R_SPREAD, R_SD, R_MATCHED} with R_MATCHED the headline; the
    leave-one-ladder-out jackknife; the three rule-8 choosers.  Frozen at
    936/1140/1148/1157's construction: CAND20 legs, cap INF, max_vol 0.60, anchor N=20 / H=126 /
    gross 0.75 / W, 10 bps, LAG 1, WARMUP 260.

WHY THERE IS NO BOOTSTRAP HERE, SAID UP FRONT
    A regime-to-length ratio compares sub-tapes at their own POSITIONS on one tape.  A moving-block
    resample destroys exactly the object being measured — it makes the between term meaningless
    while leaving the within term almost unchanged, i.e. it would manufacture the run's own answer.
    The resolution measure used instead is a LEAVE-ONE-LADDER-OUT JACKKNIFE over the ratio's own
    four groups, which needs no resample at all, plus the ALIGNED/OFFSET partition as a second
    axis.  This is a declared departure from 1157, which used a 200-rep block bootstrap for a
    different quantity, and it is stated rather than quietly substituted.

DECLARED BEFORE ANY NUMBER, AND SCORED IN THIS ORDER
    COMPARABLE means: two runs that walked DIFFERENT fraction ladders get ratios within 25% of
    each other, i.e. max/min of the ratio over the 5 ladders <= 1.25.  "A majority" means more
    than half of the 18 (panel, statistic) cells at the headline construction and partition.
    (B) COUNT-MATCH THE BETWEEN TERM : R_COUNT comparable at a majority AND its jackknife SE at
                                       the finest ladder is <= 1.25x R_FROZEN's at L3.
    (C) BOTH NEEDED                  : R_COUNT comparable at a majority but its SE is > 1.25x.
    (A) FREEZE THE LADDER            : R_COUNT not comparable at a majority, and R_FROZEN's frozen
                                       level lands within 25% of the L8-resolved R_COUNT level at
                                       a majority — freezing is the only repair and it costs
                                       little.
    (D) NEITHER                      : R_COUNT not comparable at a majority AND R_FROZEN does not
                                       land — the clause needs something neither repair supplies.

    THE RATIO IS NOT A KEEP PATH.  4a and 4b are scored at every book and the rule-8 walk-forward
    chooses on 2009-2016 alone and reads 2017-2026 ONCE.  CH_LOWRATIO and CH_HIGHRATIO exist to
    price whether the repair choice has any capital content at all.

THE VINTAGE.  `data/prices.csv` is rewritten nightly (idea 1163's defect), so every tape here is
    truncated at PIN = 2026-09-15, the vintage 1148/1157's committed anchors saw.  The unpinned
    anchors are published beside the pinned ones, not absorbed.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the current
    output of a sub-$2B screen less the documented `max_1d_move >= 1.0` exclusion.  Every LEVEL is
    optimistic and every 4a/4b count is an UPPER bound.  A RATIO of two spreads in the statistic's
    own units is far less exposed — but it is not immune, because a survivorship-flattered panel
    has a shallower drawdown path and MAXDD is this family's headline statistic, so the levels are
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
SLUG = "should-a-REGIME-to-LENGTH-RATIO-FIX-its-FRACTION-LADDER-or-COUNT-MATCH-its-BETWEEN-TERM"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"
BT = Path(__file__).resolve().parent

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
LADDERS = {"CADENCE": LAD_C, "GROSS": LAD_G, "H": LAD_H, "N": LAD_N}     # alphabetical = 1157's
ANCHOR = dict(N=N0, H=HOLD0, GROSS=GROSS0, CADENCE=FREQ0)

STATS6 = ["CAGR", "VOL", "SHARPE", "MAXDD", "ULCER", "CALMAR"]
HEAD_STAT = "MAXDD"
WITHINS = ["R_SPREAD", "R_SD", "R_MATCHED"]
HEAD_WITHIN = "R_MATCHED"
CONSTRUCTIONS = ["C_POOLED", "C_BOOK"]
HEAD_CONSTR = "C_POOLED"
HEAD_PART = "ALIGNED"

REPAIRS = ["R_ASIS", "R_FROZEN", "R_COUNT"]                              # dial 1
# R_BOTH is NOT a fourth dial value.  It is the PRODUCT of the two repairs the queue names —
# the frozen ladder AND the count-matched between term — and it is computed and published only
# because the pre-declared scoring lands on (D) NEITHER, which leaves the reader asking what the
# combination does.  It is never selected on and never counted in the 15-cell grid.
R_BOTH = "R_BOTH"
FRAC_LADDERS = {"L2": [1, 2], "L3": [1, 2, 3], "L4": [1, 2, 3, 4],
                "L6": [1, 2, 3, 4, 6], "L8": [1, 2, 3, 4, 5, 6, 8]}      # dial 2
FROZEN_LADDER = "L3"                                                     # 1140/1148's ladder
FINEST = "L8"
FRAC_ALL = sorted({f for v in FRAC_LADDERS.values() for f in v})
COMP_BAR = 1.25
SE_BAR = 1.25
LAND_BAR = 0.25

NPAIR_1157, SEED_1148 = 200, 11481148
PRIOR1157 = BT / ("2026-09-16_is-the-SMALL-MAXDD-CELL-the-ONE-PLACE-where-TAPE-LENGTH-"
                  "BEATS-REGIME_B.cells.csv")
PRIOR_CELL_1148 = 0.794259                  # 1148's SMALL / MAXDD / R_MATCHED / F_1140={1,2,3}
A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
DD_COMMITTED = {"U56": -19.127569, "B136": -20.740302, "SMALL": -35.814054}

LOG: list[str] = []
GATES: list[dict] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def gate(name, what, value, ok):
    GATES.append(dict(gate=name, what=what, value=float(value), pass_=bool(ok)))
    P(f"  {name:<5s} {'PASS' if ok else 'FAIL'}  {what}   (dev {value:.3e})")


# ---------------------------------------------------------------- kernel (1082/1157, unmodified)
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
    """1140's six, verbatim from 1157."""
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


# ---------------------------------------------- 1157's partitions and statistics, verbatim
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
    """1157's OWN statistic, kept verbatim so its committed cell can be replayed bit for bit."""
    v = np.asarray([x for x in v if np.isfinite(x)], float)
    if len(v) < 2:
        return np.nan
    if len(v) == 2:
        return float(abs(v[0] - v[1]))
    i = rng.integers(0, len(v), size=(NPAIR_1157, 2))
    i = i[i[:, 0] != i[:, 1]]
    return float(np.abs(v[i[:, 0]] - v[i[:, 1]]).mean())


def matched_exact(v):
    """The EXACT mean |difference| over all C(k,2) pairs.  No Monte-Carlo term."""
    v = np.asarray([x for x in v if np.isfinite(x)], float)
    if len(v) < 2:
        return np.nan
    return float(np.mean([abs(a - b) for a, b in combinations(v, 2)]))


def between_term(med, fracs, repair, med_frozen=None):
    """THE OBJECT UNDER TEST.  `med` maps fraction -> the ladder's median at that fraction."""
    if repair in ("R_FROZEN", R_BOTH):
        m, fr = (med_frozen if med_frozen is not None else med), FRAC_LADDERS[FROZEN_LADDER]
    else:
        m, fr = med, fracs
    vals = [m.get(f, np.nan) for f in fr]
    if repair in ("R_COUNT", R_BOTH):
        return matched_exact(vals)
    fmax = max(fr)
    a, b = m.get(1, np.nan), m.get(fmax, np.nan)
    return abs(a - b) if (np.isfinite(a) and np.isfinite(b)) else np.nan


def ratio_from(groups, med, fracs, matched_fn, repair, med_frozen=None, groups_frozen=None):
    """1148/1157's ratio_from, with the BETWEEN term parameterised by the repair and the WITHIN
    term computed on the SAME ladder the repair declares (R_FROZEN freezes BOTH)."""
    if repair in ("R_FROZEN", R_BOTH):
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
    """1157's ratio_from VERBATIM — used ONLY by the cross-run gate, never by the answer."""
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


# ---------------------------------------------------------------- the census
FRACCOLS = ("frac", "fraction", "fracs", "frac_ladder")


def census_rows():
    """Every committed CSV in research/backtests that carries a sub-tape FRACTION column."""
    rows = []
    for f in sorted(BT.glob("*.csv")):
        if f.name.startswith(f"{DATE}_{SLUG}"):
            continue
        try:
            head = pd.read_csv(f, nrows=0)
        except Exception:
            continue
        cols = set(head.columns)
        hit = [c for c in FRACCOLS if c in cols]
        if not hit:
            continue
        try:
            d = pd.read_csv(f, usecols=hit)
        except Exception:
            continue
        ladders = set()
        if "fracs" in d.columns:
            ladders |= {str(x) for x in d["fracs"].dropna().unique()}
        if "frac_ladder" in d.columns:
            ladders |= {str(x) for x in d["frac_ladder"].dropna().unique()}
        maxf = np.nan
        if "frac" in d.columns:
            v = pd.to_numeric(d["frac"], errors="coerce").dropna()
            maxf = float(v.max()) if len(v) else np.nan
        rows.append(dict(file=f.name, n_rows=len(d), cols="+".join(hit),
                         states_ladder=bool(ladders), n_ladders=len(ladders),
                         ladders=" | ".join(sorted(ladders))[:300], max_frac=maxf))
    return pd.DataFrame(rows)


def census_prose():
    """Committed sentences that assert a regime-to-length reading."""
    files = sorted(set(list(ROOT.glob("research/**/*.md")) + list(ROOT.glob("research/*.md"))))
    rx = re.compile(r"regime[- ]to[- ]length|regime.{0,40}length|length.{0,40}regime", re.I)
    lad = re.compile(r"1/\d|\{[^}]*1,\s*2[^}]*\}|F_1140|F_FINE|F_FINER|fraction ladder", re.I)
    rows = []
    for f in files:
        try:
            txt = f.read_text(errors="ignore")
        except Exception:
            continue
        for ln, line in enumerate(txt.splitlines(), 1):
            if not rx.search(line):
                continue
            for s in re.split(r"(?<=[.;!?])\s+", line):
                if rx.search(s) and len(s.strip()) > 20:
                    rows.append(dict(file=str(f.relative_to(ROOT)), line=ln, text=s.strip()[:500],
                                     states_ladder=bool(lad.search(s)),
                                     states_number=bool(re.search(r"\d\.\d{2,}|\d+\.\d+x", s))))
    return pd.DataFrame(rows)


def main():
    t0 = time.time()
    P(f"# Idea 1158 (lane cloud, {DATE}) — should a REGIME-to-LENGTH RATIO FIX its FRACTION")
    P("# LADDER or COUNT-MATCH its BETWEEN TERM?")
    P(f"# 2 tuned dials: REPAIR {REPAIRS} x FRACTION LADDER {list(FRAC_LADDERS)} = 15 cells, ALL")
    P("#   published at every (panel, statistic, construction, partition).")
    P(f"# NOT dials: PANEL {PANELS}; the four DIAL LADDERS that are the ratio's groups (27 rung")
    P(f"#   books per panel, 81 total, 1148's grid); STATS {STATS6} (headline {HEAD_STAT});")
    P(f"#   PARTITIONS {PARTITIONS}; CONSTRUCTIONS {CONSTRUCTIONS}; WITHIN terms {WITHINS}")
    P(f"#   (headline {HEAD_WITHIN}); the leave-one-ladder-out jackknife; 3 rule-8 choosers.")
    P(f"# FROZEN at 936/1140/1148/1157's construction.  TAPE PINNED at {PIN} (idea 1163).")
    P("# NO BOOTSTRAP, AND THE REASON IS DECLARED: a moving-block resample destroys the very")
    P("#   object a regime-to-length ratio measures, so the resolution measure is a")
    P("#   LEAVE-ONE-LADDER-OUT JACKKNIFE over the ratio's own four groups.  Departure from 1157.")
    P(f"# COMPARABLE := max/min of the ratio over the 5 ladders <= {COMP_BAR}.  Scored in the")
    P("#   declared order (B) COUNT-MATCH, (C) BOTH NEEDED, (A) FREEZE, (D) NEITHER.")
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
                                rank_key=rank_key, elig=elig, warm=warm, ins=ins, oos=oos)
        d = cells[panel]
        P(f"  {panel:<6s} PINNED {d['T']:5d} bars x {d['K']:4d} cols  {d['idx'][0].date()} .. "
          f"{d['idx'][-1].date()}   (unpinned {cells_un[panel]['T']} bars)")
        if panel == "SMALL":
            P(f"  SMALL STAMP: data/small_meta.csv lists {nmeta} tickers; {ndrop} dropped for "
              f"max_1d_move >= 1.0; pool served = {d['K'] - 1} names + SPY as benchmark.")
    P("")

    # ---------------------------------------------------------------- rung books
    P("## RUNG BOOKS — 27 per panel (the ratio's four groups), 81 in total, 1148's grid")
    RB: dict = {}

    def book(store, panel, N, H, gross, cadence):
        key = (id(store), panel, N, H, round(gross, 6), cadence)
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

    def rung_book(store, panel, lad, rg, warm_only=True):
        c = dict(ANCHOR)
        c[lad] = rg
        r = book(store, panel, c["N"], c["H"], c["GROSS"], c["CADENCE"])
        return r[store[panel]["warm"]] if warm_only else r

    nrung = sum(len(v) for v in LADDERS.values())
    for panel in PANELS:
        for lad, rungs in LADDERS.items():
            for rg in rungs:
                rung_book(cells, panel, lad, rg)
    P(f"  built {nrung} rung books x {len(PANELS)} panels = {nrung*len(PANELS)}  "
      f"({time.time()-t0:.0f}s)")
    P("")

    # ---------------------------------------------------------------- gates
    P("## GATES — printed before any result number")
    d = cells["U56"]
    mk = rebalance_mask(d["idx"], FREQ0).values
    W = build(d["rank_key"], d["elig"], d["priced"], np.flatnonzero(mk), N0, HOLD0,
              d["T"], d["K"], GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST, freq=FREQ0)["returns"].values[d["warm"]]
    anc = rung_book(cells, "U56", "N", N0)
    v = float(np.abs(eng - anc).max())
    gate("G1", "fast runner == engine.backtest (U56 W/H126/N=20, gross 0.75)", v, v < 1e-12)

    def triple_dev(store):
        dd_ = store["U56"]
        r = rung_book(store, "U56", "N", N0)
        m = blocks_m(r, dd_["ins"][dd_["warm"]], dd_["oos"][dd_["warm"]])
        a = max(abs(m["CAGR"] - A936_WH126[0]), abs(m["Sharpe"] - A936_WH126[1]),
                abs(m["MaxDD"] - A936_WH126[2]))
        sp = dd_["px"]["SPY"].pct_change().fillna(0.0).values[dd_["warm"]]
        sm = blocks_m(sp, dd_["ins"][dd_["warm"]], dd_["oos"][dd_["warm"]])
        b = max(abs(sm["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
                abs(sm["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
                abs(sm["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
        return a, b

    a_pin, b_pin = triple_dev(cells)
    a_un, b_un = triple_dev(cells_un)
    gate("G2", f"CROSS-RUN the committed U56 W/H126/N=20 triple, PINNED at {PIN}", a_pin,
         a_pin < 5e-5)
    gate("G3", f"CROSS-RUN the committed SPY OOS triple on U56's tape, PINNED at {PIN}", b_pin,
         b_pin < 5e-4)
    P(f"     THE VINTAGE, PUBLISHED NOT ABSORBED: the same two gates on the UNPINNED file read "
      f"{a_un:.3e} and {b_un:.3e}.")

    lv = backtest(d["px"], rules_v2_weights(d["px"]), cost_bps=COST, freq=FREQ0)["returns"].values
    v = abs(fmet(lv[d["warm"]])[2] - LIVE_MAXDD_COMMITTED)
    gate("G4", "live RULES v2 MaxDD == the committed -12.05%", v, v < 5e-4)

    v = max(abs(six_stats(rung_book(cells, p, "N", N0))["MAXDD"] - DD_COMMITTED[p]) for p in PANELS)
    gate("G5", "CROSS-RUN 1157's committed full-tape MaxDD LEVELS (U56 / B136 / SMALL)", v,
         v < 5e-4)

    # ---- the sub-tape table
    def subrows(store, panels=PANELS):
        rows = []
        for panel in panels:
            for lad, rungs in LADDERS.items():
                for rg in rungs:
                    rw = rung_book(store, panel, lad, rg)
                    for part in PARTITIONS:
                        for f in FRAC_ALL:
                            for k, seg in enumerate(parts_at(rw, f, part)):
                                rows.append(dict(panel=panel, ladder=lad, rung=str(rg),
                                                 partition=part, frac=f, part=k,
                                                 n_days=len(seg), **six_stats(seg)))
        return pd.DataFrame(rows)

    SUB = subrows(cells)
    P(f"  sub-tape table: {len(SUB):,} rows  ({time.time()-t0:.0f}s)")

    def groups_med(panel, stat, fracs, partition, sub=None, skip_ladder=None):
        s = sub if sub is not None else SUB
        s = s[(s.partition == partition) & (s.frac.isin(fracs))]
        if panel != "POOLED":
            s = s[s.panel == panel]
        if skip_ladder is not None:
            s = s[s.ladder != skip_ladder]
        groups = {f: [] for f in fracs}
        for (_pn, _lad), g in s.groupby(["panel", "ladder"]):
            for f in fracs:
                groups[f].append(g[g.frac == f].groupby("part")[stat].median().tolist())
        med = {f: float(np.nanmedian(s[s.frac == f][stat])) for f in fracs}
        return groups, med

    # G6 — replay 1148/1157's committed cell bit for bit with THEIR ratio_from and THEIR seed
    rng = np.random.default_rng(SEED_1148)
    rep = {}
    for panel in PANELS + ["POOLED"]:
        for stat in STATS6:
            g_, m_ = groups_med(panel, stat, [1, 2, 3], "ALIGNED")
            rep[(panel, stat)] = ratio_from_1157(g_, m_, [1, 2, 3],
                                                 lambda v, _r=rng: matched_sampled(v, _r))
    got = rep[("SMALL", HEAD_STAT)][HEAD_WITHIN][2]
    v = abs(got - PRIOR_CELL_1148)
    gate("G6", "CROSS-RUN 1148/1157's SMALL/MAXDD R_MATCHED replayed BIT FOR BIT (same groups, "
         "same seed, same loop order)", v, v < 1e-6)
    P(f"     replica {got:.6f} vs committed {PRIOR_CELL_1148:.6f}   |   all panels: "
      + ", ".join(f"{p} {rep[(p, HEAD_STAT)][HEAD_WITHIN][2]:.4f}x" for p in PANELS + ["POOLED"]))

    # G7 — R_ASIS at L3 reproduces that same number with the EXACT statistic (no MC term)
    g_, m_ = groups_med("SMALL", HEAD_STAT, [1, 2, 3], "ALIGNED")
    ex = ratio_from(g_, m_, [1, 2, 3], matched_exact, "R_ASIS")[HEAD_WITHIN][2]
    v = abs(ex - PRIOR_CELL_1148) / PRIOR_CELL_1148
    gate("G7", "R_ASIS at L3 with the EXACT all-pairs statistic is within 5% of the committed "
         "cell (the departure removes noise, not signal)", v, v < 0.05)
    P(f"     exact {ex:.6f} vs committed {PRIOR_CELL_1148:.6f}")

    # G8 — R_FROZEN is ladder-invariant BY CONSTRUCTION; proved, not asserted
    fz = []
    for lname, fr in FRAC_LADDERS.items():
        g2, m2 = groups_med("SMALL", HEAD_STAT, fr, "ALIGNED")
        gF, mF = groups_med("SMALL", HEAD_STAT, FRAC_LADDERS[FROZEN_LADDER], "ALIGNED")
        fz.append(ratio_from(g2, m2, fr, matched_exact, "R_FROZEN", mF, gF)[HEAD_WITHIN][2])
    v = float(np.nanmax(fz) - np.nanmin(fz))
    gate("G8", "R_FROZEN is EXACTLY ladder-invariant by construction (max - min over the 5 "
         "ladders)", v, v < 1e-12)

    # G9 — the queue's premise: R_ASIS falls when the ladder is extended L3 -> L8
    prem = {}
    for panel in PANELS:
        r3 = ratio_from(*groups_med(panel, HEAD_STAT, FRAC_LADDERS["L3"], "ALIGNED"),
                        FRAC_LADDERS["L3"], matched_exact, "R_ASIS")[HEAD_WITHIN][2]
        r8 = ratio_from(*groups_med(panel, HEAD_STAT, FRAC_LADDERS["L8"], "ALIGNED"),
                        FRAC_LADDERS["L8"], matched_exact, "R_ASIS")[HEAD_WITHIN][2]
        prem[panel] = r8 / r3
    v = float(max(prem.values()))
    gate("G9", "1157's premise REPRODUCED: R_ASIS FALLS on every panel when the ladder goes "
         "L3 -> L8 (max ratio < 1)", v, v < 1.0)
    P("     R_ASIS(L8)/R_ASIS(L3) by panel: "
      + ", ".join(f"{p} {prem[p]:.4f}x" for p in PANELS)
      + f"   (1157 committed 0.39x-0.59x)")

    SUB2 = subrows(cells)
    v = float(np.abs(SUB[STATS6].values - SUB2[STATS6].values).max())
    gate("G10", "the whole sub-tape table is deterministic", v, v < 1e-15)
    P("")

    # ---------------------------------------------------------------- the 15-cell grid
    P("## (A) THE 15-CELL GRID (dial 1 x dial 2) — every cell published")
    rows = []
    for constr in CONSTRUCTIONS:
        for part in PARTITIONS:
            for panel in PANELS:
                for stat in STATS6:
                    gF, mF = groups_med(panel, stat, FRAC_LADDERS[FROZEN_LADDER], part)
                    if constr == "C_BOOK":
                        s = SUB[(SUB.partition == part) & (SUB.panel == panel) &
                                (SUB.ladder == "N") & (SUB.rung == str(N0))]
                        gF = {f: [s[s.frac == f].sort_values("part")[stat].tolist()]
                              for f in FRAC_LADDERS[FROZEN_LADDER]}
                        mF = {f: float(np.nanmedian(s[s.frac == f][stat]))
                              for f in FRAC_LADDERS[FROZEN_LADDER]}
                    for lname, fr in FRAC_LADDERS.items():
                        if constr == "C_POOLED":
                            g_, m_ = groups_med(panel, stat, fr, part)
                        else:
                            s = SUB[(SUB.partition == part) & (SUB.panel == panel) &
                                    (SUB.ladder == "N") & (SUB.rung == str(N0))]
                            g_ = {f: [s[s.frac == f].sort_values("part")[stat].tolist()]
                                  for f in fr}
                            m_ = {f: float(np.nanmedian(s[s.frac == f][stat])) for f in fr}
                        for rep_ in REPAIRS:
                            rr = ratio_from(g_, m_, fr, matched_exact, rep_, mF, gF)
                            row = dict(construction=constr, partition=part, panel=panel,
                                       stat=stat, frac_ladder=lname,
                                       fracs="+".join(f"1/{f}" for f in fr), repair=rep_)
                            for w in WITHINS:
                                row[w + "_within"], row[w + "_between"], row[w + "_ratio"] = rr[w]
                            rows.append(row)
    GRID = pd.DataFrame(rows)
    dump(GRID, "grid")

    HEAD = GRID[(GRID.construction == HEAD_CONSTR) & (GRID.partition == HEAD_PART)]
    P(f"  HEADLINE VIEW: construction {HEAD_CONSTR}, partition {HEAD_PART}, within {HEAD_WITHIN}.")
    P(f"  {'panel':<7s}{'stat':<8s}{'repair':<10s}" +
      "".join(f"{l:>9s}" for l in FRAC_LADDERS) + f"{'max/min':>9s}{'comp':>6s}")
    comp_rows = []
    for panel in PANELS:
        for stat in STATS6:
            for rep_ in REPAIRS:
                s = HEAD[(HEAD.panel == panel) & (HEAD.stat == stat) & (HEAD.repair == rep_)]
                vals = {r.frac_ladder: r._asdict()[HEAD_WITHIN + "_ratio"] for r in s.itertuples()}
                arr = np.array([vals[l] for l in FRAC_LADDERS], float)
                fin = arr[np.isfinite(arr) & (arr > 0)]
                rng_ = float(fin.max() / fin.min()) if len(fin) else np.nan
                ok = bool(np.isfinite(rng_) and rng_ <= COMP_BAR)
                comp_rows.append(dict(panel=panel, stat=stat, repair=rep_, max_over_min=rng_,
                                      comparable=ok,
                                      **{f"ratio_{l}": vals[l] for l in FRAC_LADDERS}))
                P(f"  {panel:<7s}{stat:<8s}{rep_:<10s}" +
                  "".join(f"{vals[l]:>9.3f}" for l in FRAC_LADDERS) +
                  f"{rng_:>9.3f}{'Y' if ok else '.':>6s}")
    COMP = pd.DataFrame(comp_rows)
    dump(COMP, "comparability")
    P("")

    P("## (B) COMPARABILITY — does the repair make two runs with DIFFERENT ladders agree?")
    P(f"  bar: max/min of the ratio over the 5 ladders <= {COMP_BAR}")
    for rep_ in REPAIRS:
        s = COMP[COMP.repair == rep_]
        P(f"  {rep_:<10s} comparable at {int(s.comparable.sum()):2d} of {len(s)} (panel, stat) "
          f"cells   median max/min {s.max_over_min.median():.3f}   worst "
          f"{s.max_over_min.max():.3f}")
        sh = s[s.stat == HEAD_STAT]
        P(f"  {'':<10s}   at the headline statistic {HEAD_STAT}: "
          + ", ".join(f"{r.panel} {r.max_over_min:.3f}x{'(Y)' if r.comparable else ''}"
                      for r in sh.itertuples()))
    P("")

    # ---------------------------------------------------------------- jackknife
    P("## (C) THE PRICE OF FREEZING — leave-one-ladder-out jackknife SE of log(ratio)")
    jrows = []
    for panel in PANELS:
        for stat in STATS6:
            gF, mF = groups_med(panel, stat, FRAC_LADDERS[FROZEN_LADDER], HEAD_PART)
            for lname in (FROZEN_LADDER, FINEST):
                fr = FRAC_LADDERS[lname]
                for rep_ in REPAIRS + [R_BOTH]:
                    ps = []
                    for skip in LADDERS:
                        g_, m_ = groups_med(panel, stat, fr, HEAD_PART, skip_ladder=skip)
                        gF2, mF2 = groups_med(panel, stat, FRAC_LADDERS[FROZEN_LADDER],
                                              HEAD_PART, skip_ladder=skip)
                        val = ratio_from(g_, m_, fr, matched_exact, rep_, mF2,
                                         gF2)[HEAD_WITHIN][2]
                        if np.isfinite(val) and val > 0:
                            ps.append(np.log(val))
                    n = len(ps)
                    se = (float(np.sqrt((n - 1) / n * np.sum((np.array(ps) - np.mean(ps)) ** 2)))
                          if n >= 2 else np.nan)
                    g_, m_ = groups_med(panel, stat, fr, HEAD_PART)
                    full = ratio_from(g_, m_, fr, matched_exact, rep_, mF, gF)[HEAD_WITHIN][2]
                    jrows.append(dict(panel=panel, stat=stat, frac_ladder=lname, repair=rep_,
                                      ratio=full, jack_se_log=se, n_pseudo=n))
    JK = pd.DataFrame(jrows)
    dump(JK, "jackknife")
    se_frozen = JK[(JK.repair == "R_FROZEN") & (JK.frac_ladder == FROZEN_LADDER)]
    se_count = JK[(JK.repair == "R_COUNT") & (JK.frac_ladder == FINEST)]
    se_asis = JK[(JK.repair == "R_ASIS") & (JK.frac_ladder == FINEST)]
    P(f"  {'repair / ladder':<22s}{'median SE(log r)':>18s}{'mean':>9s}{'worst':>9s}")
    for nm, s in (("R_FROZEN @ " + FROZEN_LADDER, se_frozen), ("R_COUNT @ " + FINEST, se_count),
                  ("R_ASIS @ " + FINEST, se_asis)):
        P(f"  {nm:<22s}{s.jack_se_log.median():>18.4f}{s.jack_se_log.mean():>9.4f}"
          f"{s.jack_se_log.max():>9.4f}")
    se_ratio = float(se_count.jack_se_log.median() / se_frozen.jack_se_log.median())
    P(f"  R_COUNT@{FINEST} / R_FROZEN@{FROZEN_LADDER} median SE ratio = {se_ratio:.4f} "
      f"(bar {SE_BAR:.2f})")
    se_both = JK[(JK.repair == R_BOTH) & (JK.frac_ladder == FROZEN_LADDER)]
    P(f"  R_BOTH @ {FROZEN_LADDER} (the PRODUCT of the two repairs, published because the")
    P("       pre-declared scoring lands on (D) and the reader will ask — NOT a fourth dial value")
    P(f"       and never selected on): median SE(log r) {se_both.jack_se_log.median():.4f}, "
      f"mean {se_both.jack_se_log.mean():.4f}, worst {se_both.jack_se_log.max():.4f}; "
      f"comparable 18 of 18 by construction (its ladder is frozen).")

    land = []
    for panel in PANELS:
        for stat in STATS6:
            a = JK[(JK.repair == "R_FROZEN") & (JK.frac_ladder == FROZEN_LADDER) &
                   (JK.panel == panel) & (JK.stat == stat)].ratio.iloc[0]
            b = JK[(JK.repair == "R_COUNT") & (JK.frac_ladder == FINEST) &
                   (JK.panel == panel) & (JK.stat == stat)].ratio.iloc[0]
            c = JK[(JK.repair == R_BOTH) & (JK.frac_ladder == FROZEN_LADDER) &
                   (JK.panel == panel) & (JK.stat == stat)].ratio.iloc[0]
            rel = abs(a - b) / b if (np.isfinite(a) and np.isfinite(b) and b) else np.nan
            relc = abs(c - b) / b if (np.isfinite(c) and np.isfinite(b) and b) else np.nan
            land.append(dict(panel=panel, stat=stat, frozen=a, resolved=b, both=c, rel_gap=rel,
                             lands=bool(np.isfinite(rel) and rel <= LAND_BAR),
                             both_rel_gap=relc,
                             both_lands=bool(np.isfinite(relc) and relc <= LAND_BAR)))
    LAND = pd.DataFrame(land)
    dump(LAND, "landing")
    P(f"  DOES FREEZING LAND ON THE RESOLVED VALUE?  R_FROZEN@{FROZEN_LADDER} vs "
      f"R_COUNT@{FINEST}: lands within {LAND_BAR:.0%} at {int(LAND.lands.sum())} of {len(LAND)} "
      f"cells; median relative gap {LAND.rel_gap.median():.4f}")
    for r in LAND[LAND.stat == HEAD_STAT].itertuples():
        P(f"    {HEAD_STAT} {r.panel:<6s} frozen {r.frozen:.4f}x  resolved {r.resolved:.4f}x  "
          f"gap {r.rel_gap:.4f}  {'LANDS' if r.lands else 'MISSES'}   |   R_BOTH {r.both:.4f}x  "
          f"gap {r.both_rel_gap:.4f}  {'LANDS' if r.both_lands else 'MISSES'}")
    P(f"  R_BOTH lands within {LAND_BAR:.0%} of the resolved value at "
      f"{int(LAND.both_lands.sum())} of {len(LAND)} cells; median relative gap "
      f"{LAND.both_rel_gap.median():.4f} (against R_FROZEN's {LAND.rel_gap.median():.4f}).")
    P("")

    # ---------------------------------------------------------------- census
    P("## (D) THE CENSUS — the record's committed sub-tape rows")
    CR = census_rows()
    dump(CR, "census_rows")
    CP = census_prose()
    dump(CP, "census_prose")
    tot = int(CR.n_rows.sum()) if len(CR) else 0
    P(f"  {len(CR)} committed CSVs in research/backtests carry a sub-tape FRACTION column, "
      f"{tot:,} rows in total.")
    P(f"  {int(CR.states_ladder.sum())} of {len(CR)} ({CR.states_ladder.mean():.4f}) also publish "
      f"the LADDER they walked; the rest publish a `frac` and leave the ladder to be inferred.")
    seen = sorted({x for s in CR.ladders for x in s.split(" | ") if x})
    P(f"  DISTINCT committed ladder labels: {len(seen)} -> {seen[:12]}")
    mf = CR.max_frac.dropna()
    if len(mf):
        P(f"  max fraction actually walked: median {mf.median():.0f}, range {mf.min():.0f}"
          f"..{mf.max():.0f} over {len(mf)} files — the axis two runs disagree on.")
    P(f"  PROSE: {len(CP):,} committed sentences assert a regime-to-length reading; "
      f"{CP.states_ladder.mean():.4f} state a ladder and {CP.states_number.mean():.4f} quote a "
      f"number.")

    P("  THE DIRECT ANSWER TO 'WHICH MAKES TWO RUNS COMPARABLE', ON THE LADDERS THE RECORD")
    P("  ACTUALLY WALKED — L3 (1140/1148) and L8 (1157) are both committed, so:")
    for rep_ in REPAIRS:
        gaps = []
        for panel in PANELS:
            for stat in STATS6:
                a = GRID[(GRID.construction == HEAD_CONSTR) & (GRID.partition == HEAD_PART) &
                         (GRID.panel == panel) & (GRID.stat == stat) & (GRID.repair == rep_) &
                         (GRID.frac_ladder == "L3")][HEAD_WITHIN + "_ratio"].iloc[0]
                b = GRID[(GRID.construction == HEAD_CONSTR) & (GRID.partition == HEAD_PART) &
                         (GRID.panel == panel) & (GRID.stat == stat) & (GRID.repair == rep_) &
                         (GRID.frac_ladder == "L8")][HEAD_WITHIN + "_ratio"].iloc[0]
                if np.isfinite(a) and np.isfinite(b) and a > 0 and b > 0:
                    gaps.append(max(a, b) / min(a, b))
        g = np.array(gaps)
        P(f"    {rep_:<10s} L3 vs L8 disagree by a median {np.median(g):.3f}x "
          f"(worst {g.max():.3f}x); within {COMP_BAR} at {int((g <= COMP_BAR).sum())} of {len(g)}")
    P("")

    # ---------------------------------------------------------------- rule 8 + KEEP paths
    P("## RULE 8 WALK-FORWARD AND BOTH KEEP PATHS — 81 rung books, every one published")
    bookrows, benchrows, pickrows = [], [], []
    bench = {}
    for panel in PANELS:
        dd_ = cells[panel]
        w = dd_["warm"]
        spy = dd_["px"]["SPY"].pct_change().fillna(0.0).values[w]
        sb = blocks_m(spy, dd_["ins"][w], dd_["oos"][w])
        lvr = backtest(dd_["px"], rules_v2_weights(dd_["px"]), cost_bps=COST,
                       freq=FREQ0)["returns"].values[w]
        lb = blocks_m(lvr, dd_["ins"][w], dd_["oos"][w])
        bench[panel] = (sb, lb)
        for nm, bb in (("SPY", sb), ("RULES v2 (live)", lb)):
            benchrows.append(dict(panel=panel, name=nm, **bb))
        P(f"  {panel:<6s} SPY {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%} "
          f"(halves {sb['H1']:.4f}/{sb['H2']:.4f}), OOS {sb['OOS_CAGR']:.2%} / "
          f"{sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"  {'':<6s} LIVE {lb['CAGR']:.2%} / {lb['Sharpe']:.4f} / {lb['MaxDD']:.2%}, "
          f"OOS {lb['OOS_CAGR']:.2%} / {lb['OOS_Sharpe']:.4f} / {lb['OOS_MaxDD']:.2%}")
        for lad, rungs in LADDERS.items():
            for rg in rungs:
                r = rung_book(cells, panel, lad, rg)
                b = blocks_m(r, dd_["ins"][w], dd_["oos"][w])
                l4b, l4bo, l4a = legs_4b(b, sb), legs_4b_oos(b, sb), legs_4a(b, lb)
                bookrows.append(dict(panel=panel, ladder=lad, rung=str(rg), **b, **l4b, **l4bo,
                                     **l4a, pass_4b_full=all(l4b.values()),
                                     pass_4b_oos=all(l4bo.values()), pass_4a=all(l4a.values())))
    BK = pd.DataFrame(bookrows)
    dump(BK, "books")
    dump(pd.DataFrame(benchrows), "benchmarks")
    uniq = BK.drop_duplicates(subset=["panel", "ladder", "rung"])
    P(f"  4b FULL {int(BK.pass_4b_full.sum())} of {len(BK)} rung books | 4b OOS "
      f"{int(BK.pass_4b_oos.sum())} | BOTH {int((BK.pass_4b_full & BK.pass_4b_oos).sum())} | "
      f"4a {int(BK.pass_4a.sum())} of {len(BK)}")
    for panel in PANELS:
        s = BK[BK.panel == panel]
        P(f"    {panel:<6s} 4b full {int(s.pass_4b_full.sum()):2d}/{len(s)}  4b OOS "
          f"{int(s.pass_4b_oos.sum()):2d}/{len(s)}  4a {int(s.pass_4a.sum()):2d}/{len(s)}")
    P("  NOTE: the anchor book (N=20/H=126/gross 0.75/W) is a rung of all four ladders, so the 81")
    P("  rung books are 78 DISTINCT books; every duplicate is published, none is double-counted")
    P("  in a claim about distinct books.")
    P("")

    P("  THE THREE CHOOSERS (all choose on 2009-2016 ONLY and read 2017-2026 ONCE):")
    P("    CH_ISSHARPE  — argmax IS Sharpe over the 27 rung books.  The honest incumbent.")
    P("    CH_LOWRATIO  — among the top-9 IS-Sharpe rung books, the one whose OWN C_BOOK")
    P("                   regime-to-length ratio is LOWEST (regime dominates length).")
    P("    CH_HIGHRATIO — its exact opposite, the falsification control.")
    P("  Each is run under EVERY repair, so a pick that moves is a pick the repair moved.")
    for panel in PANELS:
        dd_ = cells[panel]
        w = dd_["warm"]
        ins_w = dd_["ins"][w]
        cand = [(lad, rg) for lad, rungs in LADDERS.items() for rg in rungs]
        isS = {}
        for lad, rg in cand:
            isS[(lad, rg)] = fsharpe(rung_book(cells, panel, lad, rg)[ins_w])
        top = sorted(cand, key=lambda k: -isS[k])[:9]
        for rep_ in REPAIRS:
            bookratio = {}
            for lad, rg in top:
                r_is = rung_book(cells, panel, lad, rg)[ins_w]
                for lname, fr in ((FROZEN_LADDER, FRAC_LADDERS[FROZEN_LADDER]),):
                    pass
                fr = FRAC_LADDERS[FINEST]
                g_ = {f: [[six_stats(seg)[HEAD_STAT]
                           for seg in parts_at(r_is, f, HEAD_PART)]] for f in fr}
                m_ = {f: float(np.nanmedian(g_[f][0])) if len(g_[f][0]) else np.nan for f in fr}
                frF = FRAC_LADDERS[FROZEN_LADDER]
                gF = {f: [[six_stats(seg)[HEAD_STAT]
                           for seg in parts_at(r_is, f, HEAD_PART)]] for f in frF}
                mF = {f: float(np.nanmedian(gF[f][0])) if len(gF[f][0]) else np.nan for f in frF}
                bookratio[(lad, rg)] = ratio_from(g_, m_, fr, matched_exact, rep_, mF,
                                                  gF)[HEAD_WITHIN][2]
            fin = {k: v for k, v in bookratio.items() if np.isfinite(v)}
            for ch in ["CH_ISSHARPE", "CH_LOWRATIO", "CH_HIGHRATIO"]:
                if ch == "CH_ISSHARPE":
                    pick = max(cand, key=lambda k: isS[k])
                elif not fin:
                    pick = max(top, key=lambda k: isS[k])
                elif ch == "CH_LOWRATIO":
                    pick = min(fin, key=lambda k: fin[k])
                else:
                    pick = max(fin, key=lambda k: fin[k])
                r = rung_book(cells, panel, pick[0], pick[1])
                b = blocks_m(r, dd_["ins"][w], dd_["oos"][w])
                sb, lb = bench[panel]
                l4b, l4bo, l4a = legs_4b(b, sb), legs_4b_oos(b, sb), legs_4a(b, lb)
                pickrows.append(dict(panel=panel, repair=rep_, chooser=ch, ladder=pick[0],
                                     rung=str(pick[1]), book_ratio=bookratio.get(pick, np.nan),
                                     IS_Sharpe=b["IS_Sharpe"], OOS_Sharpe=b["OOS_Sharpe"],
                                     OOS_CAGR=b["OOS_CAGR"], OOS_MaxDD=b["OOS_MaxDD"],
                                     SPY_OOS_Sharpe=sb["OOS_Sharpe"],
                                     beats_SPY_OOS=b["OOS_Sharpe"] > sb["OOS_Sharpe"],
                                     pass_4b_full=all(l4b.values()),
                                     pass_4b_oos=all(l4bo.values()), pass_4a=all(l4a.values())))
    PK = pd.DataFrame(pickrows)
    dump(PK, "picks")
    P(f"  {'panel':<7s}{'repair':<10s}{'chooser':<14s}{'pick':<14s}{'IS_S':>8s}{'OOS_S':>8s}"
      f"{'SPY_S':>8s}{'>SPY':>6s}{'4b':>4s}{'4bO':>5s}{'4a':>4s}")
    for r in PK.itertuples():
        P(f"  {r.panel:<7s}{r.repair:<10s}{r.chooser:<14s}{(r.ladder+'='+r.rung):<14s}"
          f"{r.IS_Sharpe:>8.4f}{r.OOS_Sharpe:>8.4f}{r.SPY_OOS_Sharpe:>8.4f}"
          f"{'Y' if r.beats_SPY_OOS else '.':>6s}{'Y' if r.pass_4b_full else '.':>4s}"
          f"{'Y' if r.pass_4b_oos else '.':>5s}{'Y' if r.pass_4a else '.':>4s}")
    moved = 0
    for panel in PANELS:
        for ch in ["CH_LOWRATIO", "CH_HIGHRATIO"]:
            s = PK[(PK.panel == panel) & (PK.chooser == ch)]
            if s[["ladder", "rung"]].drop_duplicates().shape[0] > 1:
                moved += 1
    P(f"  THE REPAIR MOVES THE PICK at {moved} of {2*len(PANELS)} (panel, ratio-chooser) cells.")
    P("")

    # ---------------------------------------------------------------- verdict
    P("## VERDICT AGAINST THE PRE-DECLARED OUTCOMES, SCORED IN THE DECLARED ORDER")
    n_cells = len(COMP[COMP.repair == "R_COUNT"])
    n_count = int(COMP[COMP.repair == "R_COUNT"].comparable.sum())
    n_asis = int(COMP[COMP.repair == "R_ASIS"].comparable.sum())
    n_froz = int(COMP[COMP.repair == "R_FROZEN"].comparable.sum())
    maj = n_count > n_cells / 2
    lands_maj = int(LAND.lands.sum()) > len(LAND) / 2
    P(f"  comparable cells: R_ASIS {n_asis}/{n_cells}, R_FROZEN {n_froz}/{n_cells}, "
      f"R_COUNT {n_count}/{n_cells}   (majority bar {n_cells/2:.1f})")
    P(f"  SE ratio R_COUNT@{FINEST} / R_FROZEN@{FROZEN_LADDER} = {se_ratio:.4f} (bar {SE_BAR:.2f})")
    P(f"  R_FROZEN lands within {LAND_BAR:.0%} of the resolved value at "
      f"{int(LAND.lands.sum())}/{len(LAND)} cells")
    if maj and se_ratio <= SE_BAR:
        outcome = "(B) COUNT-MATCH THE BETWEEN TERM"
    elif maj:
        outcome = "(C) BOTH NEEDED"
    elif lands_maj:
        outcome = "(A) FREEZE THE LADDER"
    else:
        outcome = "(D) NEITHER"
    P(f"  OUTCOME: {outcome}")
    P("")

    dump(pd.DataFrame(GATES), "gates")
    P(f"## GATES {sum(g['pass_'] for g in GATES)} of {len(GATES)} PASS")
    P(f"## DONE in {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return outcome


if __name__ == "__main__":
    main()

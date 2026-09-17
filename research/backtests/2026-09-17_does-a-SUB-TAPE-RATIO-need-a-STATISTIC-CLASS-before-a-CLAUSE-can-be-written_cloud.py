#!/usr/bin/env python3
"""
Idea 1187 (lane cloud, 2026-09-17)
does-a-SUB-TAPE-RATIO-need-a-STATISTIC-CLASS-before-a-CLAUSE-can-be-written

THE QUESTION, AS THE QUEUE PUT IT
---------------------------------
Idea 1158 found that the combined repair (frozen fraction ladder + count-matched between
term) lands on the resolved value at all three MAXDD cells but at only 4 of 18 cells
overall, and OFFERED an explanation it did not test: "on RATIO-valued statistics (SHARPE,
CALMAR) the between term passes near zero and every repair blows up together."  This run
tests that explanation by splitting the record's six sub-tape statistics into LEVEL,
SPREAD and RATIO classes, measuring each class's OWN between-term zero-crossing rate, and
asking whether ONE clause can be written that serves all three.

THE TWO DIALS AND NO MORE (rule 4)
----------------------------------
  dial 1  STATISTIC CLASS  {LEVEL, SPREAD, RATIO}
  dial 2  REPAIR           {R_ASIS, R_FROZEN, R_COUNT, R_BOTH}
  = 12 cells, EVERY ONE PUBLISHED, at every (panel, construction, partition) and every
  fraction ladder.  R_BOTH is 1158's declared product of the two repairs; it is promoted
  to a dial VALUE here (1158 kept it off-grid) because the queue's clause is exactly the
  question "which repair goes in the clause", and a product that is never a candidate
  cannot be one.  That is the only departure from 1158's dial set and it is declared here.

NOT DIALS (fixed, or swept and fully published, never selected on):
  PANEL {U56, B136, SMALL}; the four DIAL LADDERS that are the ratio's groups
  (CADENCE, GROSS, H, N = 27 rung books per panel, 81 total, 1148's grid);
  FRACTION LADDERS {L2, L3, L4, L6, L8}; PARTITIONS {ALIGNED, OFFSET};
  CONSTRUCTIONS {C_POOLED, C_BOOK}; WITHIN terms {R_SPREAD, R_SD, R_MATCHED}
  (headline R_MATCHED); the leave-one-ladder-out jackknife; the four rule-8 choosers.

THE CLASSES, DECLARED BEFORE ANY NUMBER IS COMPUTED
---------------------------------------------------
  LEVEL  = {CAGR, MAXDD}   a location of the equity path, in return units
  SPREAD = {VOL, ULCER}    a dispersion magnitude, non-negative by construction
  RATIO  = {SHARPE, CALMAR} a quotient of a LEVEL by a SPREAD
The split is 2/2/2 and is a property of the statistic's ALGEBRA, not of any number this
run produces.  It is not tuned and it is not re-drawn after the fact.

WHAT "ZERO-CROSSING" MEANS HERE (three measures, all published, one headline)
-----------------------------------------------------------------------------
For a cell the between term B is a contrast of the fraction ladder's medians m_f.
  SCALE    = median_f |m_f|                      (the statistic's own level on this cell)
  zrel     = |B| / SCALE                          scale-free, comparable across statistics
  DEGENERATE (headline) := zrel < 0.05           the between term has stopped resolving
  SIGNFLIP := min_f m_f < 0 < max_f m_f          the medians literally straddle zero
  BLOWUP   := within/between ratio > 10          the published ratio has no finite reading
A class's ZERO-CROSSING RATE is its share of DEGENERATE cells.

WHEN A CLAUSE "SERVES" A CLASS (both legs, because comparability alone is vacuous)
----------------------------------------------------------------------------------
1158's G8 proved R_FROZEN is ladder-invariant BY CONSTRUCTION, so a comparability-only
bar hands R_FROZEN every class for free and answers nothing.  A repair serves a class
only if, over that class's RESOLVABLE cells, it is BOTH
  COMPARABLE : max/min of the ratio over the 5 fraction ladders <= 1.25, AND
  LANDS      : within 25% (relative) of the RESOLVED value,
at a MAJORITY of them.  RESOLVED is 1158's committed target, reproduced here and not
re-chosen: the COUNT-MATCHED between term on the FINEST ladder, R_COUNT at L8 — finest
because a longer ladder resolves more, count-matched because a max-minus-min over a
varying number of points is inflated by the count alone (idea 1155).  RESOLVABLE := the
resolved cell is itself not DEGENERATE and its leave-one-ladder-out jackknife SE is no
larger than the ratio itself.  A cell that is not RESOLVABLE has no target to land on and
is counted as UNPUBLISHABLE, not as a failure.

A TAUTOLOGY, DECLARED RATHER THAN HIDDEN: R_COUNT read at L8 *is* the target, so its
landing leg is 1.000 by construction and is never evidence of anything; it is published
anyway so the reader can see it.  R_COUNT earns or loses a class on comparability alone.
The split is structural and is the whole trade 1158 found: the ladder-FOLLOWING repairs
(R_ASIS, R_COUNT) land but do not stay put, and the ladder-FROZEN ones (R_FROZEN, R_BOTH)
stay put by construction but may land nowhere near the resolved value.

PRE-DECLARED OUTCOMES, SCORED IN THIS ORDER
-------------------------------------------
  (A) ONE CLAUSE    some single repair serves all three classes
  (B) TWO CLAUSES   the best repair serves exactly two; one class needs its own wording
  (C) THREE CLAUSES a different repair serves each class
  (D) NO CLAUSE ON RATIO  no repair serves the RATIO class, in which case the honest
      clause is that ratio-valued sub-tape statistics carry no publishable
      regime-to-length ratio at this tape length at all.

KEEP PATHS AND RULE 8 (protocol, mandatory, and this run is NOT a capital finding)
----------------------------------------------------------------------------------
A statistic-class taxonomy is a reporting-schema result, not a trading rule; it cannot by
itself be a KEEP.  Rule 8 is run anyway and in full: all 81 rung books are scored against
4a (vs live RULES v2) and 4b (vs SPY) on the full tape AND out of sample, parameters
chosen on 2009-2016 and 2017-2026 read once, and four choosers are run — the honest
IS-Sharpe incumbent and one per statistic class — so the reader can see whether the class
distinction moves a single capital decision.  Every book and every pick is published.

SURVIVORSHIP: the SMALL panel is current constituents of a sub-$2B screen (see
data/SMALL_PANEL_README.md); tickers with max_1d_move >= 1.0 in data/small_meta.csv are
dropped first.  Its levels are optimistic and every 4a/4b count on it is an UPPER bound.
TAPE PINNED at 2026-09-15 (idea 1163) so the committed anchors replay bit for bit; the
unpinned reading of the same gates is printed, not absorbed.
"""
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
SLUG = "does-a-SUB-TAPE-RATIO-need-a-STATISTIC-CLASS-before-a-CLAUSE-can-be-written"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

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
ANCHOR = dict(N=N0, H=HOLD0, GROSS=GROSS0, CADENCE=FREQ0)

STATS6 = ["CAGR", "VOL", "SHARPE", "MAXDD", "ULCER", "CALMAR"]
CLASSES = {"LEVEL": ["CAGR", "MAXDD"], "SPREAD": ["VOL", "ULCER"],
           "RATIO": ["SHARPE", "CALMAR"]}                                    # dial 1
CLASS_OF = {s: c for c, ss in CLASSES.items() for s in ss}
WITHINS = ["R_SPREAD", "R_SD", "R_MATCHED"]
HEAD_WITHIN = "R_MATCHED"
CONSTRUCTIONS = ["C_POOLED", "C_BOOK"]
HEAD_CONSTR, HEAD_PART = "C_POOLED", "ALIGNED"

REPAIRS = ["R_ASIS", "R_FROZEN", "R_COUNT", "R_BOTH"]                        # dial 2
FRAC_LADDERS = {"L2": [1, 2], "L3": [1, 2, 3], "L4": [1, 2, 3, 4],
                "L6": [1, 2, 3, 4, 6], "L8": [1, 2, 3, 4, 5, 6, 8]}
FROZEN_LADDER, FINEST = "L3", "L8"
FRAC_ALL = sorted({f for v in FRAC_LADDERS.values() for f in v})

COMP_BAR = 1.25          # 1158's comparability bar, verbatim
LAND_BAR = 0.25          # 1158's landing bar, verbatim
DEGEN_BAR = 0.05         # |B| / SCALE below this = the between term resolves nothing
BLOWUP_BAR = 10.0        # within/between above this = no finite published reading
SE_BAR = 1.0             # jackknife SE larger than the ratio itself = unresolved

# committed anchors this run must replay (cross-run gates)
A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
DD_COMMITTED = {"U56": -19.127569, "B136": -20.740302, "SMALL": -35.814054}
COMP_1158 = {"R_ASIS": 0, "R_FROZEN": 18, "R_COUNT": 2}      # of 18, C_POOLED/ALIGNED
LAND_1158_BOTH = 4                                            # of 18
# 1158's committed C_POOLED/ALIGNED frozen readings, to be reproduced exactly
FROZEN_1158 = {("U56", "SHARPE"): 49.12043648776099, ("SMALL", "MAXDD"): 0.7942591498710535,
               ("U56", "CAGR"): 3.2043376643336035, ("B136", "CALMAR"): 3.420952926773515}

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


# ---------------------------------------------------------------- kernel (1082/1157/1158)
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


# ------------------------------------------- 1157/1158's partitions and ratio, verbatim
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


def matched_exact(v):
    v = np.asarray([x for x in v if np.isfinite(x)], float)
    if len(v) < 2:
        return np.nan
    return float(np.mean([abs(a - b) for a, b in combinations(v, 2)]))


def between_term(med, fracs, repair, med_frozen=None):
    """1158's between_term, with R_BOTH now a first-class dial value."""
    if repair in ("R_FROZEN", "R_BOTH"):
        m, fr = (med_frozen if med_frozen is not None else med), FRAC_LADDERS[FROZEN_LADDER]
    else:
        m, fr = med, fracs
    vals = [m.get(f, np.nan) for f in fr]
    if repair in ("R_COUNT", "R_BOTH"):
        return matched_exact(vals)
    fmax = max(fr)
    a, b = m.get(1, np.nan), m.get(fmax, np.nan)
    return abs(a - b) if (np.isfinite(a) and np.isfinite(b)) else np.nan


def zero_measures(med, fracs, repair, med_frozen=None):
    """The three zero-crossing measures, read off the SAME ladder the repair declares."""
    if repair in ("R_FROZEN", "R_BOTH"):
        m, fr = (med_frozen if med_frozen is not None else med), FRAC_LADDERS[FROZEN_LADDER]
    else:
        m, fr = med, fracs
    vals = np.asarray([m.get(f, np.nan) for f in fr], float)
    vals = vals[np.isfinite(vals)]
    if len(vals) < 2:
        return np.nan, np.nan, False
    scale = float(np.median(np.abs(vals)))
    B = between_term(med, fracs, repair, med_frozen)
    zrel = abs(B) / scale if scale > 0 else np.nan
    return scale, zrel, bool(vals.min() < 0 < vals.max())


def ratio_from(groups, med, fracs, repair, med_frozen=None, groups_frozen=None):
    """1148/1157/1158's ratio_from: WITHIN computed on the SAME ladder the repair declares."""
    if repair in ("R_FROZEN", "R_BOTH"):
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
            m_ = matched_exact(v)
            if np.isfinite(m_):
                matched.append(m_)
    bs = between_term(med, fracs, repair, med_frozen)
    ws = float(np.nanmedian(ranges)) if ranges else np.nan
    wsd = float(np.nanmedian(sds)) if sds else np.nan
    wm = float(np.nanmedian(matched)) if matched else np.nan
    return {"R_SPREAD": (ws, bs, ws / bs if bs else np.nan),
            "R_SD": (wsd, bs, wsd / bs if bs else np.nan),
            "R_MATCHED": (wm, bs, wm / bs if bs else np.nan)}


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(meta), len(meta) - (len(keep) - 1)


def main():
    t0 = time.time()
    P(f"# Idea 1187 (lane cloud, {DATE}) — does a SUB-TAPE RATIO need a STATISTIC CLASS")
    P("# before a CLAUSE can be written?")
    P(f"# 2 tuned dials: STATISTIC CLASS {list(CLASSES)} x REPAIR {REPAIRS} = 12 cells,")
    P("#   EVERY ONE PUBLISHED at every (panel, construction, partition) and fraction ladder.")
    P(f"# CLASSES, declared before any number: " +
      "; ".join(f"{c} = {'+'.join(s)}" for c, s in CLASSES.items()) + " (algebra, not fit).")
    P(f"# NOT dials: PANEL {PANELS}; the four DIAL LADDERS (27 rung books/panel, 81 total);")
    P(f"#   FRACTION LADDERS {list(FRAC_LADDERS)}; PARTITIONS {PARTITIONS};")
    P(f"#   CONSTRUCTIONS {CONSTRUCTIONS}; WITHIN terms {WITHINS} (headline {HEAD_WITHIN});")
    P("#   the leave-one-ladder-out jackknife; the four rule-8 choosers.")
    P(f"# DEGENERATE := |B|/SCALE < {DEGEN_BAR};  SIGNFLIP := medians straddle 0;")
    P(f"#   BLOWUP := within/between > {BLOWUP_BAR};  COMPARABLE := max/min <= {COMP_BAR};")
    P(f"#   LANDS := within {LAND_BAR:.0%} of 1158's RESOLVED target R_COUNT@{FINEST};")
    P("#   (R_COUNT's own landing is 1.000 BY CONSTRUCTION — it is the target — and is")
    P("#   published but never counted as evidence.)  RESOLVABLE := target not")
    P(f"#   DEGENERATE and jackknife SE/|ratio| <= {SE_BAR}.")
    P("# A clause SERVES a class iff COMPARABLE and LANDS at a MAJORITY of its RESOLVABLE")
    P("#   cells.  Comparability alone is vacuous (1158's G8: R_FROZEN is invariant BY")
    P("#   CONSTRUCTION), so the landing leg is not optional.")
    P(f"# TAPE PINNED at {PIN}.  Scored in the declared order (A) ONE, (B) TWO, (C) THREE,")
    P("#   (D) NO CLAUSE ON RATIO.  This is a reporting-schema result, never a KEEP.")
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
            P(f"  SMALL STAMP (SURVIVORSHIP): data/small_meta.csv lists {nmeta} tickers; "
              f"{ndrop} dropped for max_1d_move >= 1.0; pool served = {d['K']-1} names + SPY.")
            P("  Current constituents of the screen only — SMALL levels are OPTIMISTIC and")
            P("  every 4a / 4b count on that panel is an UPPER bound.")
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

    def rung_book(store, panel, lad, rg):
        c = dict(ANCHOR)
        c[lad] = rg
        r = book(store, panel, c["N"], c["H"], c["GROSS"], c["CADENCE"])
        return r[store[panel]["warm"]]

    nrung = sum(len(v) for v in LADDERS.values())
    for panel in PANELS:
        for lad, rungs in LADDERS.items():
            for rg in rungs:
                rung_book(cells, panel, lad, rg)
    P(f"  built {nrung} rung books x {len(PANELS)} panels = {nrung*len(PANELS)}  "
      f"({time.time()-t0:.0f}s).  The anchor book (N=20/H=126/gross 0.75/W) is a rung of all")
    P("  four ladders, so the 81 are 78 DISTINCT books; every duplicate is published and none")
    P("  is counted twice in any claim about distinct books.")
    P("")

    # ---------------------------------------------------------------- gates
    P("## GATES — printed before any result number")
    d = cells["U56"]
    mk = rebalance_mask(d["idx"], FREQ0).values
    W = build(d["rank_key"], d["elig"], d["priced"], np.flatnonzero(mk), N0, HOLD0,
              d["T"], d["K"], GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST, freq=FREQ0)["returns"].values[d["warm"]]
    v = float(np.abs(eng - rung_book(cells, "U56", "N", N0)).max())
    gate("G1", "fast runner == engine.backtest (U56 W/H126/N=20, gross 0.75)", v, v < 1e-12)

    def triple_dev(store):
        dd_ = store["U56"]
        w = dd_["warm"]
        m = blocks_m(rung_book(store, "U56", "N", N0), dd_["ins"][w], dd_["oos"][w])
        a = max(abs(m["CAGR"] - A936_WH126[0]), abs(m["Sharpe"] - A936_WH126[1]),
                abs(m["MaxDD"] - A936_WH126[2]))
        sp = dd_["px"]["SPY"].pct_change().fillna(0.0).values[w]
        sm = blocks_m(sp, dd_["ins"][w], dd_["oos"][w])
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
    gate("G5", "CROSS-RUN 1157/1158's committed full-tape MaxDD LEVELS (U56/B136/SMALL)", v,
         v < 5e-4)

    # ---- the sub-tape table
    def subrows(store):
        rows = []
        for panel in PANELS:
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

    def groups_med(panel, stat, fracs, partition, skip_ladder=None):
        s = SUB[(SUB.partition == partition) & (SUB.frac.isin(fracs))]
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

    # G6 — reproduce 1158's committed C_POOLED/ALIGNED FROZEN readings exactly
    dev = 0.0
    for (pn, st), want in FROZEN_1158.items():
        gF, mF = groups_med(pn, st, FRAC_LADDERS[FROZEN_LADDER], HEAD_PART)
        got = ratio_from(gF, mF, FRAC_LADDERS[FROZEN_LADDER], "R_FROZEN", mF,
                         gF)[HEAD_WITHIN][2]
        dev = max(dev, abs(got - want))
    gate("G6", "CROSS-RUN 1158's committed FROZEN readings at 4 (panel, stat) cells, incl. its "
         "U56/SHARPE blow-up 49.1204", dev, dev < 1e-9)
    P("")

    # ---------------------------------------------------------------- the 12-cell grid
    P("## (A) THE 12-CELL GRID (dial 1 STATISTIC CLASS x dial 2 REPAIR) — every cell published")
    rows = []
    for constr in CONSTRUCTIONS:
        for part in PARTITIONS:
            for panel in PANELS:
                for stat in STATS6:
                    gF, mF = groups_med(panel, stat, FRAC_LADDERS[FROZEN_LADDER], part)
                    if constr == "C_BOOK":
                        # one book per ladder: collapse groups to the per-ladder medians
                        gF = {f: [[np.nanmedian(v) for v in gF[f]]] for f in gF}
                    for lname, fr in FRAC_LADDERS.items():
                        g_, m_ = groups_med(panel, stat, fr, part)
                        if constr == "C_BOOK":
                            g_ = {f: [[np.nanmedian(v) for v in g_[f]]] for f in g_}
                        for rep_ in REPAIRS:
                            out = ratio_from(g_, m_, fr, rep_, mF, gF)
                            scale, zrel, flip = zero_measures(m_, fr, rep_, mF)
                            w, b, r = out[HEAD_WITHIN]
                            rows.append(dict(
                                sclass=CLASS_OF[stat], repair=rep_, construction=constr,
                                partition=part, panel=panel, stat=stat, frac_ladder=lname,
                                fracs="+".join(f"1/{f}" for f in fr),
                                within=w, between=b, ratio=r, scale=scale, zrel=zrel,
                                signflip=flip,
                                degenerate=bool(np.isfinite(zrel) and zrel < DEGEN_BAR),
                                blowup=bool(np.isfinite(r) and abs(r) > BLOWUP_BAR),
                                **{f"{k}_ratio": out[k][2] for k in WITHINS}))
    G = pd.DataFrame(rows)
    dump(G, "grid")
    P(f"  {len(G):,} rows = 3 classes x 4 repairs x 3 panels x 2 stats x 2 constructions "
      f"x 2 partitions x 5 fraction ladders.")
    P("")

    # ---------------------------------------------------------------- zero-crossing rates
    P("## (B) THE HEADLINE: EACH CLASS'S OWN BETWEEN-TERM ZERO-CROSSING RATE")
    P("  DEGENERATE = |between| / SCALE < 0.05, i.e. the between term resolves nothing.")
    P(f"  {'class':<8s}{'repair':<10s}{'n':>6s}{'DEGEN':>8s}{'rate':>8s}{'SIGNFLIP':>10s}"
      f"{'BLOWUP':>8s}{'med zrel':>10s}{'med ratio':>11s}")
    zrows = []
    for cl in CLASSES:
        for rep_ in REPAIRS:
            s = G[(G.sclass == cl) & (G.repair == rep_)]
            zrows.append(dict(sclass=cl, repair=rep_, n=len(s),
                              n_degenerate=int(s.degenerate.sum()),
                              rate_degenerate=float(s.degenerate.mean()),
                              n_signflip=int(s.signflip.sum()),
                              rate_signflip=float(s.signflip.mean()),
                              n_blowup=int(s.blowup.sum()),
                              rate_blowup=float(s.blowup.mean()),
                              med_zrel=float(np.nanmedian(s.zrel)),
                              med_ratio=float(np.nanmedian(s.ratio)),
                              max_ratio=float(np.nanmax(np.abs(s.ratio)))))
            z = zrows[-1]
            P(f"  {cl:<8s}{rep_:<10s}{z['n']:>6d}{z['n_degenerate']:>8d}"
              f"{z['rate_degenerate']:>8.3f}{z['n_signflip']:>10d}{z['n_blowup']:>8d}"
              f"{z['med_zrel']:>10.4f}{z['med_ratio']:>11.4f}")
    Z = pd.DataFrame(zrows)
    dump(Z, "zerocross")
    for cl in CLASSES:
        s = G[G.sclass == cl]
        P(f"  CLASS {cl:<7s} pooled over all four repairs: DEGEN {int(s.degenerate.sum())}/"
          f"{len(s)} = {s.degenerate.mean():.3f}, SIGNFLIP {int(s.signflip.sum())}/{len(s)}, "
          f"BLOWUP {int(s.blowup.sum())}/{len(s)}, median |ratio| "
          f"{np.nanmedian(np.abs(s.ratio)):.4f}")
    P("")

    # ---------------------------------------------------------------- jackknife + resolvable
    P("## (C) THE RESOLVED TARGET AND WHICH CELLS CAN BE LANDED ON AT ALL")
    P("  RESOLVED := R_COUNT at the finest ladder L8 — 1158's committed target, reproduced,")
    P("  not re-chosen.  Its uncertainty is a LEAVE-ONE-LADDER-OUT")
    P("  jackknife over the ratio's own four groups (no resample: a moving-block bootstrap")
    P("  destroys the very serial object a regime-to-length ratio measures — 1158's reason,")
    P("  restated, not re-derived).")
    jrows = []
    for constr in CONSTRUCTIONS:
        for part in PARTITIONS:
            for panel in PANELS:
                for stat in STATS6:
                    fr = FRAC_LADDERS[FINEST]
                    g_, m_ = groups_med(panel, stat, fr, part)
                    if constr == "C_BOOK":
                        g_ = {f: [[np.nanmedian(v) for v in g_[f]]] for f in g_}
                    full = ratio_from(g_, m_, fr, "R_COUNT")[HEAD_WITHIN][2]
                    reps = []
                    for skip in LADDERS:
                        gj, mj = groups_med(panel, stat, fr, part, skip_ladder=skip)
                        if constr == "C_BOOK":
                            gj = {f: [[np.nanmedian(v) for v in gj[f]]] for f in gj}
                        reps.append(ratio_from(gj, mj, fr, "R_COUNT")[HEAD_WITHIN][2])
                    reps = np.asarray([x for x in reps if np.isfinite(x)], float)
                    n = len(reps)
                    se = (np.sqrt((n - 1) / n * np.sum((reps - reps.mean()) ** 2))
                          if n >= 2 else np.nan)
                    _, zr, _ = zero_measures(m_, fr, "R_COUNT")
                    resolvable = bool(np.isfinite(full) and np.isfinite(se) and
                                      np.isfinite(zr) and zr >= DEGEN_BAR and
                                      abs(full) > 0 and se / abs(full) <= SE_BAR)
                    jrows.append(dict(sclass=CLASS_OF[stat], construction=constr,
                                      partition=part, panel=panel, stat=stat,
                                      resolved=full, jack_se=se,
                                      se_over_ratio=se / abs(full) if full else np.nan,
                                      zrel=zr, resolvable=resolvable))
    J = pd.DataFrame(jrows)
    dump(J, "jackknife")
    P(f"  {'class':<8s}{'cells':>7s}{'RESOLVABLE':>12s}{'rate':>8s}{'med SE/|r|':>12s}"
      f"{'med zrel':>10s}")
    for cl in CLASSES:
        s = J[J.sclass == cl]
        P(f"  {cl:<8s}{len(s):>7d}{int(s.resolvable.sum()):>12d}{s.resolvable.mean():>8.3f}"
          f"{np.nanmedian(s.se_over_ratio):>12.4f}{np.nanmedian(s.zrel):>10.4f}")
    P("")

    # ---------------------------------------------------------------- comparability + landing
    P("## (D) DOES A REPAIR SERVE A CLASS?  COMPARABLE **AND** LANDS, on RESOLVABLE cells only")
    key = ["construction", "partition", "panel", "stat"]
    resolved = J.set_index(key)
    crows = []
    for (constr, part, panel, stat), g in G.groupby(key):
        tgt = resolved.loc[(constr, part, panel, stat)]
        for rep_ in REPAIRS:
            s = g[g.repair == rep_]
            v = s.ratio.replace([np.inf, -np.inf], np.nan).dropna()
            comp = (float(v.max() / v.min()) if len(v) == len(FRAC_LADDERS) and v.min() > 0
                    else np.inf)
            # the repair's own published reading = its value on the FROZEN ladder for the
            # frozen repairs, on the FINEST for the ladder-following ones (its best reading)
            lname = FROZEN_LADDER if rep_ in ("R_FROZEN", "R_BOTH") else FINEST
            read = float(s[s.frac_ladder == lname].ratio.iloc[0])
            gap = (abs(read - tgt.resolved) / abs(tgt.resolved)
                   if np.isfinite(read) and np.isfinite(tgt.resolved) and tgt.resolved else np.nan)
            crows.append(dict(sclass=CLASS_OF[stat], repair=rep_, construction=constr,
                              partition=part, panel=panel, stat=stat, reading=read,
                              resolved=float(tgt.resolved), max_over_min=comp,
                              comparable=bool(comp <= COMP_BAR), rel_gap=gap,
                              lands=bool(np.isfinite(gap) and gap <= LAND_BAR),
                              landing_is_tautological=(rep_ == "R_COUNT"),
                              resolvable=bool(tgt.resolvable)))
    C = pd.DataFrame(crows)
    C["serves"] = C.comparable & C.lands
    dump(C, "serves")

    # cross-run gate G7: 1158's comparability counts at the headline config, 18 cells
    head = C[(C.construction == HEAD_CONSTR) & (C.partition == HEAD_PART)]
    dev = max(abs(int(head[head.repair == r].comparable.sum()) - COMP_1158[r])
              for r in COMP_1158)
    gate("G7", "CROSS-RUN 1158's committed comparability counts at C_POOLED/ALIGNED "
         "(R_ASIS 0/18, R_FROZEN 18/18, R_COUNT 2/18)", dev, dev == 0)
    v = abs(int(head[head.repair == "R_BOTH"].lands.sum()) - LAND_1158_BOTH)
    gate("G8", "CROSS-RUN 1158's committed R_BOTH landing count (4 of 18)", v, v == 0)
    dev = float(np.nanmax(np.abs(
        C[C.repair == "R_FROZEN"].groupby(key).max_over_min.max() - 1.0)))
    gate("G9", "R_FROZEN is EXACTLY ladder-invariant by construction (so comparability alone "
         "is vacuous and the landing leg is mandatory)", dev, dev < 1e-12)
    SUB2 = subrows(cells)
    v = float(np.abs(SUB[STATS6].values - SUB2[STATS6].values).max())
    gate("G10", "the whole sub-tape table is deterministic", v, v < 1e-15)
    P("")

    P(f"  {'class':<8s}{'repair':<10s}{'RESOLVABLE':>11s}{'COMPARABLE':>11s}{'LANDS':>7s}"
      f"{'SERVES':>8s}{'rate':>8s}{'majority?':>11s}")
    srows = []
    for cl in CLASSES:
        for rep_ in REPAIRS:
            s = C[(C.sclass == cl) & (C.repair == rep_) & C.resolvable]
            nr = len(s)
            nserve = int(s.serves.sum())
            rate = nserve / nr if nr else np.nan
            maj = bool(nr > 0 and nserve > nr / 2)
            srows.append(dict(sclass=cl, repair=rep_, n_resolvable=nr,
                              n_comparable=int(s.comparable.sum()), n_lands=int(s.lands.sum()),
                              n_serves=nserve, rate=rate, majority=maj))
            P(f"  {cl:<8s}{rep_:<10s}{nr:>11d}{int(s.comparable.sum()):>11d}"
              f"{int(s.lands.sum()):>7d}{nserve:>8d}"
              f"{(f'{rate:.3f}' if nr else '   n/a'):>8s}{('YES' if maj else '.'):>11s}")
    S = pd.DataFrame(srows)
    dump(S, "clause")
    P("")

    # ---------------------------------------------------------------- rule 8 + KEEP paths
    P("## (E) RULE 8 WALK-FORWARD AND BOTH KEEP PATHS — 81 rung books, every one published")
    P("  Parameters chosen on 2009-2016 ONLY; 2017-2026 read once.  4a is judged against the")
    P("  live RULES v2 book, 4b against SPY, on the full tape and again out of sample.")
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
        P(f"  {panel:<6s} SPY  {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%} "
          f"(halves {sb['H1']:.4f}/{sb['H2']:.4f}), OOS {sb['OOS_CAGR']:.2%} / "
          f"{sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"  {'':<6s} LIVE {lb['CAGR']:.2%} / {lb['Sharpe']:.4f} / {lb['MaxDD']:.2%} "
          f"(halves {lb['H1']:.4f}/{lb['H2']:.4f}), OOS {lb['OOS_CAGR']:.2%} / "
          f"{lb['OOS_Sharpe']:.4f} / {lb['OOS_MaxDD']:.2%}")
        for lad, rungs in LADDERS.items():
            for rg in rungs:
                b = blocks_m(rung_book(cells, panel, lad, rg), dd_["ins"][w], dd_["oos"][w])
                l4b, l4bo, l4a = legs_4b(b, sb), legs_4b_oos(b, sb), legs_4a(b, lb)
                bookrows.append(dict(panel=panel, ladder=lad, rung=str(rg), **b, **l4b, **l4bo,
                                     **l4a, pass_4b_full=all(l4b.values()),
                                     pass_4b_oos=all(l4bo.values()), pass_4a=all(l4a.values())))
    BK = pd.DataFrame(bookrows)
    dump(BK, "books")
    dump(pd.DataFrame(benchrows), "benchmarks")
    P(f"  4b FULL {int(BK.pass_4b_full.sum())} of {len(BK)} rung books | 4b OOS "
      f"{int(BK.pass_4b_oos.sum())} | BOTH {int((BK.pass_4b_full & BK.pass_4b_oos).sum())} | "
      f"4a {int(BK.pass_4a.sum())} of {len(BK)}")
    for panel in PANELS:
        s = BK[BK.panel == panel]
        P(f"    {panel:<6s} 4b full {int(s.pass_4b_full.sum()):2d}/{len(s)}  4b OOS "
          f"{int(s.pass_4b_oos.sum()):2d}/{len(s)}  4a {int(s.pass_4a.sum()):2d}/{len(s)}")
    P("")

    P("  THE FOUR CHOOSERS (all choose on 2009-2016 ONLY and read 2017-2026 ONCE):")
    P("    CH_ISSHARPE — argmax IS Sharpe over the 27 rung books.  The honest incumbent.")
    P("    CH_LEVEL / CH_SPREAD / CH_RATIO — among the top-9 IS-Sharpe books, the one whose")
    P("      OWN in-sample regime-to-length ratio is LOWEST when that ratio is read on a")
    P("      statistic of that CLASS (headline statistic of the class: MAXDD / VOL / SHARPE).")
    P("      If the class matters operationally, these three pick different books.")
    CH_STAT = {"CH_LEVEL": "MAXDD", "CH_SPREAD": "VOL", "CH_RATIO": "SHARPE"}
    for panel in PANELS:
        dd_ = cells[panel]
        w = dd_["warm"]
        ins_w = dd_["ins"][w]
        cand = [(lad, rg) for lad, rungs in LADDERS.items() for rg in rungs]
        isS = {k: fsharpe(rung_book(cells, panel, k[0], k[1])[ins_w]) for k in cand}
        top = sorted(cand, key=lambda k: -isS[k])[:9]
        sb, lb = bench[panel]
        for ch in ["CH_ISSHARPE", "CH_LEVEL", "CH_SPREAD", "CH_RATIO"]:
            if ch == "CH_ISSHARPE":
                pick, br = max(cand, key=lambda k: isS[k]), np.nan
            else:
                st = CH_STAT[ch]
                fr = FRAC_LADDERS[FINEST]
                bookratio = {}
                for lad, rg in top:
                    r_is = rung_book(cells, panel, lad, rg)[ins_w]
                    g_ = {f: [[six_stats(seg)[st] for seg in parts_at(r_is, f, HEAD_PART)]]
                          for f in fr}
                    m_ = {f: (float(np.nanmedian(g_[f][0])) if len(g_[f][0]) else np.nan)
                          for f in fr}
                    bookratio[(lad, rg)] = ratio_from(g_, m_, fr, "R_ASIS")[HEAD_WITHIN][2]
                fin = {k: v for k, v in bookratio.items() if np.isfinite(v)}
                pick = (min(fin, key=lambda k: fin[k]) if fin
                        else max(top, key=lambda k: isS[k]))
                br = bookratio.get(pick, np.nan)
            b = blocks_m(rung_book(cells, panel, pick[0], pick[1]), dd_["ins"][w], dd_["oos"][w])
            l4b, l4bo, l4a = legs_4b(b, sb), legs_4b_oos(b, sb), legs_4a(b, lb)
            sc = "-" if ch == "CH_ISSHARPE" else CLASS_OF[CH_STAT[ch]]
            pickrows.append(dict(panel=panel, chooser=ch, sclass=sc,
                ladder=pick[0], rung=str(pick[1]), book_ratio=br,
                IS_Sharpe=b["IS_Sharpe"], OOS_Sharpe=b["OOS_Sharpe"], OOS_CAGR=b["OOS_CAGR"],
                OOS_MaxDD=b["OOS_MaxDD"], CAGR=b["CAGR"], Sharpe=b["Sharpe"],
                MaxDD=b["MaxDD"], H1=b["H1"], H2=b["H2"],
                SPY_OOS_Sharpe=sb["OOS_Sharpe"], SPY_OOS_CAGR=sb["OOS_CAGR"],
                SPY_OOS_MaxDD=sb["OOS_MaxDD"],
                beats_SPY_OOS=b["OOS_Sharpe"] > sb["OOS_Sharpe"],
                pass_4b_full=all(l4b.values()), pass_4b_oos=all(l4bo.values()),
                pass_4a=all(l4a.values())))
    PK = pd.DataFrame(pickrows)
    dump(PK, "picks")
    P(f"  {'panel':<7s}{'chooser':<13s}{'pick':<14s}{'IS_S':>8s}{'OOS_S':>8s}{'SPY_S':>8s}"
      f"{'OOS_CAGR':>10s}{'OOS_DD':>9s}{'>SPY':>6s}{'4b':>4s}{'4bO':>5s}{'4a':>4s}")
    for r in PK.itertuples():
        P(f"  {r.panel:<7s}{r.chooser:<13s}{(r.ladder+'='+r.rung):<14s}{r.IS_Sharpe:>8.4f}"
          f"{r.OOS_Sharpe:>8.4f}{r.SPY_OOS_Sharpe:>8.4f}{r.OOS_CAGR:>10.2%}{r.OOS_MaxDD:>9.2%}"
          f"{'Y' if r.beats_SPY_OOS else '.':>6s}{'Y' if r.pass_4b_full else '.':>4s}"
          f"{'Y' if r.pass_4b_oos else '.':>5s}{'Y' if r.pass_4a else '.':>4s}")
    moved = sum(1 for panel in PANELS
                if PK[(PK.panel == panel) & (PK.chooser != "CH_ISSHARPE")][["ladder", "rung"]]
                .drop_duplicates().shape[0] > 1)
    P(f"  THE STATISTIC CLASS MOVES THE PICK at {moved} of {len(PANELS)} panels.")
    P(f"  4b FULL {int(PK.pass_4b_full.sum())} of {len(PK)} picks | 4b OOS "
      f"{int(PK.pass_4b_oos.sum())} | 4a {int(PK.pass_4a.sum())}.")
    P("")

    # ---------------------------------------------------------------- verdict
    P("## VERDICT AGAINST THE PRE-DECLARED OUTCOMES, SCORED IN THE DECLARED ORDER")
    maj = {cl: set(S[(S.sclass == cl) & S.majority].repair) for cl in CLASSES}
    for cl in CLASSES:
        P(f"  {cl:<7s} served by: {sorted(maj[cl]) if maj[cl] else 'NOTHING'}"
          f"   (resolvable cells {int(S[S.sclass==cl].n_resolvable.iloc[0])} of "
          f"{len(J[J.sclass==cl])})")
    allthree = maj["LEVEL"] & maj["SPREAD"] & maj["RATIO"]
    if allthree:
        outcome = f"(A) ONE CLAUSE — {sorted(allthree)} serves all three classes"
    elif not maj["RATIO"]:
        outcome = "(D) NO CLAUSE ON RATIO — no repair serves the RATIO class"
    else:
        best = max(REPAIRS, key=lambda r: sum(r in maj[cl] for cl in CLASSES))
        ncl = sum(best in maj[cl] for cl in CLASSES)
        outcome = (f"(B) TWO CLAUSES — best repair {best} serves {ncl} of 3 classes"
                   if ncl == 2 else
                   f"(C) THREE CLAUSES — no repair serves more than one class")
    P(f"  OUTCOME: {outcome}")
    P("")

    ok = all(g["pass_"] for g in GATES)
    dump(pd.DataFrame(GATES), "gates")
    P(f"## GATES {sum(g['pass_'] for g in GATES)} of {len(GATES)} PASS")
    P(f"## DONE in {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

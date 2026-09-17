#!/usr/bin/env python3
"""Idea 1160 (cloud lane, 2026-09-17)
   is-the-MAXDD-LEVEL-the-whole-of-the-SMALL-panel-s-REGIME-to-LENGTH-DIFFERENCE

QUEUE PREMISE.  Idea 1157 found the SMALL panel crosses sub-1 on 1148's regime-to-length
ratio before the large-cap panels do, and proposed a reason: SMALL's MaxDD LEVEL is 1.9x
deeper (-35.81% vs U56 -19.13%), so BOTH ratio terms scale with the level and the between
term outgrows the within one.  THE ASK, and it is a real prediction: gross-scale the U56
anchor book until its full-tape MaxDD MATCHES SMALL's, and report whether its
regime-to-length ratio then LANDS on SMALL's.

TUNED DIALS (2, PROTOCOL rule 4 — the queue names both):
    DIAL 1  SCALING TARGET  {S_NONE (unscaled control), S_MAXDD (match SMALL's full-tape
                             MaxDD -35.814%), S_VOL, S_ULCER}
    DIAL 2  FRACTION LADDER {F_1140 = 1/1,1/2,1/3 (1148's own); F_FINE = +1/4,1/6 (1157's
                             headline); F_FINER = +1/5,1/8}
CONTROLS, never selected on and reported at every cell: CONSTRUCTION {C_POOLED = 1148/1157's
own object, in which the ratio's groups are the FOUR DIAL LADDERS and each value is a median
over that ladder's rung books; C_BOOK = the single anchor book's own ratio, which is what the
queue's words literally name}; MECHANISM {M_GROSS = rebuild at a solved gross, the queue's
literal words, running above 1.00 where the target demands it; M_RETURN = multiply the
anchor's NET returns by a solved lambda}; PANEL (donors U56, B136; target SMALL); TAPE
{T_OWN, T_MATCHED}; PARTITION {ALIGNED, OFFSET}.  A full LAMBDA LADDER is run beside the
solved point so scale-dependence is MEASURED, not inferred from two points.

FROZEN at 1140/1148/1157's construction: CAND20 legs [(21,252),(0,126),(0,63)], cap INF,
max_vol 0.60, min hold 126, N=20, W cadence, gross anchor 0.75, LAG 1, warm-up 260, 10 bps,
IS end 2016-12-31, block L=63, 1157's four dial ladders, ALIGNED/OFFSET partitions and its
three ratio definitions.

PRICE VINTAGE, PINNED AND DECLARED.  data/prices.csv gained the 2026-09-16 bar in commit
6f1fcb1 while this lane was running its first idea, so the record's committed U56 triples —
computed on tapes ending 2026-09-15 — no longer reproduce to their own tolerances on the
current file.  EVERY tape here is therefore truncated at PIN = 2026-09-15 (a no-op for B136
and SMALL, which end 2026-09-11), and the UNPINNED reading is reported beside the pinned one
at every headline cell so the vintage's size is published rather than absorbed.  Gates G2/G3
are run BOTH ways and the difference IS the vintage.

ONE DELIBERATE DEPARTURE FROM 1157, DECLARED.  1157's MATCHED within-spread is the mean
|difference| over NPAIR=200 RANDOM pairs drawn from a shared RNG, so it is reproducible only
by replaying its whole loop.  Gate G6 does exactly that, bit for bit, and every number this
run then MOVES is computed with the EXACT mean over all C(k,2) pairs, which for k = 2..8 is
free and carries no Monte-Carlo term.  G7 publishes the size of that swap at all nine
committed (ladder, panel) cells.

THE LANDING RULE, DECLARED BEFORE ANY NUMBER.  Let R_d be the donor's ratio unscaled, R_s the
donor's ratio after scaling, R_T the SMALL target's.  The donor LANDS iff scaling closes at
least HALF the gap: |R_s - R_T| <= 0.5 * |R_d - R_T|.  The premise is CONFIRMED iff the donor
lands on a majority of (construction, ladder, tape, mechanism) cells and REFUTED otherwise.
The bar is fixed here and never re-chosen.

Standalone, deterministic, offline.  Writes only research/backtests/<this stem>.* files.
SURVIVORSHIP (PROTOCOL rule 9): U56 and B136 are CURRENT-constituent lists and the SMALL pool
is the current output of a sub-$2B screen; names with max_1d_move >= 1.0 in
data/small_meta.csv are dropped before anything is computed.
LEVERAGE, STATED NOT BURIED: matching a -35.8% drawdown from a -19.1% book needs roughly
twice the exposure, so S_MAXDD runs the U56 book near gross 1.5 with NEGATIVE cash and NO
financing charge.  That is a DIAGNOSTIC of a ratio's arithmetic, not a proposed book, and
every KEEP-path number for those cells carries the same caveat.
"""
from __future__ import annotations

import sys
import time
import zlib
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
SLUG = "is-the-MAXDD-LEVEL-the-whole-of-the-SMALL-panel-s-REGIME-to-LENGTH-DIFFERENCE"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"
BT = Path(__file__).resolve().parent

PIN = "2026-09-15"                          # the vintage the record's committed anchors saw
LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST, GROSS0, FREQ0, HOLD0, N0 = 10.0, 0.75, "W", 126, 20
LEGS = [(21, 252), (0, 126), (0, 63)]

DONORS = ["U56", "B136"]
TARGET = "SMALL"
PANELS = DONORS + [TARGET]
TAPES = ["T_OWN", "T_MATCHED"]
HEAD_TAPE = "T_OWN"
PARTITIONS = ["ALIGNED", "OFFSET"]
OFFSET_FRACS = (0.0, 1.0 / 3.0, 2.0 / 3.0)

# 1157's four dial ladders — the GROUPS of the pooled construction
LAD_N = [5, 8, 10, 12, 15, 20, 25, 30, 40]
LAD_H = [21, 63, 126, 252]
LAD_G = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]
LAD_C = ["D", "W", "M", "Q"]
LADDERS = {"CADENCE": LAD_C, "GROSS": LAD_G, "H": LAD_H, "N": LAD_N}   # alphabetical = 1157's
ANCHOR = dict(N=N0, H=HOLD0, GROSS=GROSS0, CADENCE=FREQ0)

STATS6 = ["CAGR", "VOL", "SHARPE", "MAXDD", "ULCER", "CALMAR"]
HEAD_STAT = "MAXDD"
FRAC_LADDERS = {"F_1140": [1, 2, 3], "F_FINE": [1, 2, 3, 4, 6], "F_FINER": [1, 2, 3, 4, 5, 6, 8]}
FRAC_ALL = sorted({f for v in FRAC_LADDERS.values() for f in v})
HEAD_LADDER = "F_FINE"
R_HEAD = "R_MATCHED"

CONSTRUCTIONS = ["C_POOLED", "C_BOOK"]
HEAD_CONSTR = "C_POOLED"                    # where 1148/1157's committed number lives
TARGETS = ["S_NONE", "S_MAXDD", "S_VOL", "S_ULCER"]
TARGET_STAT = {"S_MAXDD": "MAXDD", "S_VOL": "VOL", "S_ULCER": "ULCER"}
MECHS = ["M_GROSS", "M_RETURN"]
HEAD_MECH = "M_GROSS"
LAD_L = [0.50, 0.75, 1.00, 1.25, 1.50, 1.75, 2.00, 2.50, 3.00]
LAND_BAR = 0.5

BLOCK, NBOOT, NPAIR_1157 = 63, 200, 200
SEED, SEED_1148 = 11601160, 11481148

PRIOR1157 = BT / ("2026-09-16_is-the-SMALL-MAXDD-CELL-the-ONE-PLACE-where-TAPE-LENGTH-"
                  "BEATS-REGIME_B.cells.csv")
A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
DD_COMMITTED = {"U56": -19.127569, "B136": -20.740302, "SMALL": -35.814054}
PRIOR_CELL_1148 = 0.794259                  # 1148's SMALL / MAXDD / R_MATCHED / F_1140

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
    return SEED + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


# --------------------------------------------- 1082/1098/1150/1157's fast runner, verbatim
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
    ulcer = float(np.sqrt((dd ** 2).mean()))
    return {"CAGR": cagr * 100.0, "VOL": vol * 100.0,
            "SHARPE": (r.mean() * 252.0 / vol if vol else np.nan),
            "MAXDD": mdd * 100.0, "ULCER": ulcer * 100.0,
            "CALMAR": (cagr / abs(mdd) if mdd < 0 else np.nan)}


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


def windows_idx(idx):
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    ins = warm & ~oos
    return warm, ins, oos


def blocks_m(r, ins=None, oos=None):
    c, s, d = fmet(r)
    h = len(r) // 2
    out = dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(r[:h]), H2=fsharpe(r[h:]))
    if ins is not None:
        ic, is_, idd = fmet(r[ins])
        oc, os_, od = fmet(r[oos])
        out.update(IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd,
                   OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)
    return out


def legs_4b(b, sb):
    return {"L_H1": bool(b["H1"] > sb["H1"]), "L_H2": bool(b["H2"] > sb["H2"]),
            "L_OOS": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "L_DD": bool(abs(b["MaxDD"]) <= DD_CAP * abs(sb["MaxDD"])),
            "L_CAGR": bool(b["CAGR"] >= CAGR_FLOOR * sb["CAGR"])}


def legs_4a(b, lb):
    return {"A_H1": bool(b["H1"] > lb["H1"]), "A_H2": bool(b["H2"] > lb["H2"]),
            "A_DD": bool(b["MaxDD"] >= lb["MaxDD"])}


# ------------------------------------------------ 1157's partitions and ratio, verbatim
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
    """THE DEPARTURE: the EXACT mean |difference| over all C(k,2) pairs.  No Monte-Carlo term."""
    v = np.asarray([x for x in v if np.isfinite(x)], float)
    if len(v) < 2:
        return np.nan
    return float(np.mean([abs(a - b) for a, b in combinations(v, 2)]))


def ratio_from(groups, frac_medians, fracs, matched_fn):
    """1148/1157's ratio_from, verbatim except that the pair statistic is injected."""
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
    return px[keep].dropna(how="all").ffill(), len(bad), len(meta)


def main():
    t0 = time.time()
    P(f"# Idea 1160 (cloud lane, {DATE}) — is the MAXDD LEVEL the whole of the SMALL panel's")
    P("#   REGIME-to-LENGTH difference?  1157's proposed reason for SMALL crossing sub-1 first is")
    P("#   that its MaxDD level is 1.9x deeper, so BOTH ratio terms scale and the between term")
    P("#   outgrows.  THE TEST: gross-scale the U56 anchor book to SMALL's MaxDD and ask whether")
    P("#   its ratio LANDS on SMALL's.")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4): SCALING TARGET {TARGETS} x FRACTION LADDER "
      f"{list(FRAC_LADDERS)}.")
    P(f"#   CONTROLS, never selected on: CONSTRUCTION {CONSTRUCTIONS} (C_POOLED is 1148/1157's own")
    P("#   object — the ratio's groups are the FOUR DIAL LADDERS, each value a median over that")
    P("#   ladder's rung books; C_BOOK is the single anchor book the queue's words name),")
    P(f"#   MECHANISM {MECHS}, PANEL (donors {DONORS}, target {TARGET}), TAPE {TAPES},")
    P(f"#   PARTITION {PARTITIONS}, and a LAMBDA LADDER {LAD_L}.")
    P(f"# FROZEN: CAND20 legs {LEGS}, max_vol {MAXVOL}, min hold {HOLD0}, N {N0}, cadence {FREQ0},")
    P(f"#   gross anchor {GROSS0}, LAG {LAG}, warm-up {WARMUP}, {COST} bps, IS end {IS_END}, block {BLOCK}.")
    P("#")
    P(f"# PRICE VINTAGE, PINNED AND DECLARED: data/prices.csv gained the 2026-09-16 bar in commit")
    P(f"#   6f1fcb1 mid-session, so the record's committed U56 triples no longer reproduce to their")
    P(f"#   own tolerances on the current file.  Every tape is truncated at PIN = {PIN} (a no-op")
    P("#   for B136 and SMALL) and gates G2/G3 are run BOTH ways: the difference IS the vintage.")
    P("# ONE DEPARTURE FROM 1157, DECLARED: its MATCHED statistic is 200 RANDOM pairs off a shared")
    P("#   RNG.  G6 replays its whole loop bit for bit; every number this run MOVES then uses the")
    P("#   EXACT mean over all C(k,2) pairs.  G7 publishes the size of that swap at all 9 cells.")
    P("# THE LANDING RULE, DECLARED BEFORE ANY NUMBER: the donor LANDS iff scaling closes at least")
    P(f"#   {LAND_BAR:.0%} of the gap.  PREMISE CONFIRMED iff it lands on a MAJORITY of cells.")
    P("# LEVERAGE, STATED NOT BURIED: S_MAXDD runs U56 near gross 1.5 with NEGATIVE cash and NO")
    P("#   financing charge — a DIAGNOSTIC of a ratio's arithmetic, not a proposed book.")
    P("# SURVIVORSHIP (rule 9): all three panels are current-constituent lists; SMALL most of all.")
    P("")

    gaterows = []

    def gate(name, what, value, ok):
        gaterows.append(dict(gate=name, what=what, value=float(value), pass_=bool(ok)))
        P(f"  [{'PASS' if ok else 'FAIL'}] {name:<5s} {what}: {value:.4e}")

    # ------------------------------------------------------------------------- panels
    P("## PANELS — loaded, PINNED and STAMPED before any result number")
    small, ndrop, nmeta = load_small()
    raw_unpinned = {"U56": load_universe().dropna(how="all").ffill(),
                    "B136": load_universe(broad=True).dropna(how="all").ffill(),
                    "SMALL": small}
    raw = {k: v.loc[:PIN] for k, v in raw_unpinned.items()}
    SMALL_DAYS = raw["SMALL"].index

    def prep(px):
        idx = px.index
        warm, ins, oos = windows_idx(idx)
        sc, elig = mech_scores(px)
        return dict(px=px, idx=idx, K=len(px.columns), T=len(idx),
                    rets=px.pct_change().fillna(0.0).values, priced=px.notna().values,
                    warm=warm, ins=ins, oos=oos, sc=sc, elig=elig,
                    spy_i=list(px.columns).index("SPY"))

    cells, cells_un = {}, {}
    for tape in TAPES:
        for panel in PANELS:
            for store, src in ((cells, raw), (cells_un, raw_unpinned)):
                px = src[panel]
                if tape == "T_MATCHED":
                    px = px.loc[px.index.intersection(SMALL_DAYS)]
                d = prep(px)
                if panel == "SMALL":
                    d["elig"] = d["elig"].copy()
                    d["elig"][:, d["spy_i"]] = False
                store[(tape, panel)] = d
            d = cells[(tape, panel)]
            du = cells_un[(tape, panel)]
            P(f"  {tape:<10s} {panel:<6s} {d['K']:4d} cols, PINNED {d['T']:,} rows "
              f"{d['idx'][0].date()} -> {d['idx'][-1].date()}  warm {d['warm'].sum():,}"
              f"   (unpinned {du['T']:,} rows -> {du['idx'][-1].date()})")
    P(f"  SMALL STAMP: data/small_meta.csv lists {nmeta} tickers; {ndrop} dropped for "
      f"max_1d_move >= 1.0; pool served = {cells[('T_OWN','SMALL')]['K'] - 1} names + SPY as "
      f"benchmark; tape {SMALL_DAYS[0].date()} -> {SMALL_DAYS[-1].date()}.")
    P("")

    # ------------------------------------------------- selections for every rung book
    def cadence_mask(idx, spec):
        return rebalance_mask(idx, spec).values

    SEL: dict = {}

    def selection(store, tape, panel, N, H, freq):
        key = (id(store), tape, panel, N, H, freq)
        if key not in SEL:
            d = store[(tape, panel)]
            reb = np.flatnonzero(cadence_mask(d["idx"], freq))
            SEL[key] = build(-d["sc"], d["elig"], d["priced"], reb, N, H, d["T"], d["K"], 1.0)
        return SEL[key]

    def book(store, tape, panel, N, H, gross, freq):
        d = store[(tape, panel)]
        mk = cadence_mask(d["idx"], freq)
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        W = selection(store, tape, panel, N, H, freq) * gross
        Wl = np.zeros_like(W)
        Wl[LAG:] = W[:-LAG]
        g, tn = nrun(d["rets"], Wl, mkl)
        return (g - tn * COST / 1e4)[d["warm"]]

    def anchor_book(tape, panel, lam=1.0, mech="M_GROSS", store=None):
        store = cells if store is None else store
        if mech == "M_GROSS":
            return book(store, tape, panel, N0, HOLD0, GROSS0 * lam, FREQ0)
        return book(store, tape, panel, N0, HOLD0, GROSS0, FREQ0) * lam

    RB: dict = {}

    def rung_book(tape, panel, lad, rg, lam=1.0, mech="M_GROSS"):
        key = (tape, panel, lad, rg, lam, mech)
        if key not in RB:
            c = dict(ANCHOR)
            c[lad] = rg
            if mech == "M_GROSS":
                RB[key] = book(cells, tape, panel, c["N"], c["H"], c["GROSS"] * lam, c["CADENCE"])
            else:
                RB[key] = book(cells, tape, panel, c["N"], c["H"], c["GROSS"],
                               c["CADENCE"]) * lam
        return RB[key]

    # ------------------------------------------------------------------------- gates
    P("## GATES — printed before any result number")
    d = cells[("T_OWN", "U56")]
    Wg = selection(cells, "T_OWN", "U56", N0, HOLD0, FREQ0) * GROSS0
    eng = backtest(d["px"], pd.DataFrame(Wg, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST, freq=FREQ0)["returns"].values[d["warm"]]
    anc = anchor_book("T_OWN", "U56")
    v = float(np.abs(eng - anc).max())
    gate("G1", "fast runner == engine.backtest (U56 W/H126/N=20, g=0.75)", v, v < 1e-12)

    def triple_dev(store):
        dd_ = store[("T_OWN", "U56")]
        r = anchor_book("T_OWN", "U56", store=store)
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
    gate("G3", f"SPY OOS triple on U56's own tape, PINNED at {PIN}", b_pin, b_pin < 5e-4)
    P(f"     THE VINTAGE, PUBLISHED NOT ABSORBED: the same two gates on the UNPINNED file read "
      f"{a_un:.4e} and {b_un:.4e}")
    P(f"     — a {a_un / a_pin:.0f}x and {b_un / b_pin:.0f}x inflation from ONE extra daily bar "
      f"(2026-09-16, commit 6f1fcb1).  MaxDD (a max over the path) does not move at all; CAGR")
    P("     and Sharpe (means over the path) do.  Idea 522's class, and the reason this run pins.")
    lb = backtest(d["px"], rules_v2_weights(d["px"]), cost_bps=COST,
                  freq="W")["returns"].values[d["warm"]]
    v = abs(blocks_m(lb)["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gate("G4", "live RULES v2 MaxDD == committed -12.05%", v, v < 5e-4)

    anchors = {p: six_stats(anchor_book("T_OWN", p)) for p in PANELS}
    v = max(abs(anchors[p]["MAXDD"] - DD_COMMITTED[p]) for p in PANELS)
    gate("G5", "CROSS-RUN 1157's committed full-tape MaxDD LEVELS (U56 / B136 / SMALL)", v,
         v < 5e-4)
    P("     1157's COMMITTED levels, quoted VERBATIM FROM ITS OWN CSV: "
      + ", ".join(f"{p} {DD_COMMITTED[p]:.4f}%" for p in PANELS)
      + "   |   re-derived: " + ", ".join(f"{p} {anchors[p]['MAXDD']:.4f}%" for p in PANELS))
    P(f"     THE LEVEL GAP THE QUEUE POINTS AT: SMALL / U56 = "
      f"{abs(anchors['SMALL']['MAXDD'] / anchors['U56']['MAXDD']):.4f}x deeper.")

    prior = pd.read_csv(PRIOR1157)
    pr = prior[(prior.tape == "T_OWN") & (prior.partition == "ALIGNED")
               & (prior.episode == "KEEP") & (prior.stat == HEAD_STAT)]
    PRIOR_R = {(r.frac_ladder, r.panel): float(r.R_MATCHED_ratio) for r in pr.itertuples()}
    okp = len(PRIOR_R) == len(FRAC_LADDERS) * len(PANELS)
    gate("G6a", "1157's committed cells.csv present and carrying all 9 (ladder, panel) MAXDD "
         "cells", 0.0 if okp else 1.0, okp)
    for lad in FRAC_LADDERS:
        P(f"       {lad:<8s}" + "  ".join(f"{p} {PRIOR_R[(lad, p)]:.6f}x" for p in PANELS))

    # ------------------------------ the POOLED construction, and the bit-for-bit replica
    P("")
    P("## THE CONSTRUCTION 1148/1157 ACTUALLY USED.  Its ratio is NOT a single book's: the")
    P("##   groups are the FOUR DIAL LADDERS (CADENCE, GROSS, H, N) and each value is a MEDIAN")
    P("##   over that ladder's rung books at one part of the tape.  A run that computes the")
    P("##   single anchor book's ratio is computing a DIFFERENT OBJECT — this run reports both.")
    nrung = sum(len(v) for v in LADDERS.values())

    SUBC: dict = {}

    def subrows_for(tape, lam, mech, panels=PANELS):
        """1157's SUB table at a given scale: one row per (panel, ladder, rung, partition,
        fraction, part).  Memoised — the landing arm asks for the same tables repeatedly."""
        key = (tape, lam, mech, tuple(panels))
        if key in SUBC:
            return SUBC[key]
        rows = []
        for panel in panels:
            for lad, rungs in LADDERS.items():
                for rg in rungs:
                    rw = rung_book(tape, panel, lad, rg, lam, mech)
                    for part in PARTITIONS:
                        for f in FRAC_ALL:
                            for k, seg in enumerate(parts_at(rw, f, part)):
                                rows.append(dict(panel=panel, ladder=lad, rung=rg,
                                                 partition=part, frac=f, part=k,
                                                 n_days=len(seg), **six_stats(seg)))
        SUBC[key] = pd.DataFrame(rows)
        return SUBC[key]

    def pooled_ratio(SUB, panel, stat, fracs, partition, matched_fn):
        s = SUB[(SUB.partition == partition) & (SUB.frac.isin(fracs))]
        s = s if panel == "POOLED" else s[s.panel == panel]
        groups = {f: [] for f in fracs}
        for (_pn, _lad), g in s.groupby(["panel", "ladder"]):
            for f in fracs:
                groups[f].append(g[g.frac == f].groupby("part")[stat].median().tolist())
        med = {f: float(np.nanmedian(s[s.frac == f][stat])) for f in fracs}
        return ratio_from(groups, med, fracs, matched_fn)

    SUB0 = subrows_for("T_OWN", 1.0, "M_GROSS")
    P(f"  built {nrung} rung books x {len(PANELS)} panels x {len(FRAC_ALL)} fractions x "
      f"{len(PARTITIONS)} partitions  ({time.time()-t0:.0f}s)")
    rng = np.random.default_rng(SEED_1148)
    rep = {}
    for panel in PANELS + ["POOLED"]:
        for stat in STATS6:
            rep[(panel, stat)] = pooled_ratio(SUB0, panel, stat, [1, 2, 3], "ALIGNED",
                                              lambda v, _r=rng: matched_sampled(v, _r))
    v = abs(rep[("SMALL", HEAD_STAT)][R_HEAD][2] - PRIOR_CELL_1148)
    gate("G6", "CROSS-RUN 1148/1157's SMALL/MAXDD R_MATCHED replayed BIT FOR BIT (same groups, "
         "same seed, same loop order)", v, v < 1e-6)
    P(f"     replica {rep[('SMALL', HEAD_STAT)][R_HEAD][2]:.6f}x vs committed {PRIOR_CELL_1148:.6f}x"
      f"   |   all panels: "
      + ", ".join(f"{p} {rep[(p, HEAD_STAT)][R_HEAD][2]:.4f}x" for p in PANELS + ["POOLED"]))

    ex_all, sa_all = {}, {}
    for lad, fr in FRAC_LADDERS.items():
        for p in PANELS:
            ex_all[(lad, p)] = pooled_ratio(SUB0, p, HEAD_STAT, fr, "ALIGNED",
                                            matched_exact)[R_HEAD][2]
            sa_all[(lad, p)] = PRIOR_R[(lad, p)]
    v = max(abs(ex_all[k] - sa_all[k]) / sa_all[k] for k in sa_all)
    gate("G7", "the EXACT all-pairs statistic moves all 9 committed (ladder, panel) MAXDD "
         "ratios by < 5% (the departure removes noise, not signal)", v, v < 0.05)
    P("     exact vs committed: " + "  ".join(
        f"{lad}/{p} {ex_all[(lad,p)]:.4f}/{sa_all[(lad,p)]:.4f}"
        for lad in FRAC_LADDERS for p in PANELS))

    def ratio_of(constr, tape, panel, lam, mech, fracs, partition="ALIGNED", SUB=None):
        if constr == "C_POOLED":
            S = SUB if SUB is not None else subrows_for(tape, lam, mech, [panel])
            return pooled_ratio(S, panel, HEAD_STAT, fracs, partition, matched_exact)
        r = anchor_book(tape, panel, lam, mech)
        vals = {f: [six_stats(p) for p in parts_at(r, f, partition)] for f in fracs}
        groups = {f: [[s[HEAD_STAT] for s in vals[f]]] for f in fracs}
        med = {f: float(np.nanmedian([s[HEAD_STAT] for s in vals[f]])) for f in fracs}
        return ratio_from(groups, med, fracs, matched_exact)

    # ------------------------------------------------- ARM 1: the lambda ladder
    P("")
    P("## ARM 1 — the LAMBDA LADDER.  Both ratio terms are in the statistic's OWN UNITS, so a")
    P("##   ratio of them is homogeneous of degree ZERO under exact scaling.  This arm measures")
    P("##   how far from exact the real thing is, on both constructions.")
    ladrows = []
    for constr in CONSTRUCTIONS:
        for mech in MECHS:
            for lam in LAD_L:
                SUBl = subrows_for(HEAD_TAPE, lam, mech) if constr == "C_POOLED" else None
                for panel in PANELS:
                    st = six_stats(anchor_book(HEAD_TAPE, panel, lam, mech))
                    for lad, fr in FRAC_LADDERS.items():
                        rr = ratio_of(constr, HEAD_TAPE, panel, lam, mech, fr, SUB=SUBl)
                        ladrows.append(dict(constr=constr, tape=HEAD_TAPE, panel=panel,
                                            mech=mech, lam=lam, frac_ladder=lad,
                                            gross=GROSS0 * lam if mech == "M_GROSS" else GROSS0,
                                            anchor_MAXDD=st["MAXDD"], anchor_VOL=st["VOL"],
                                            anchor_CAGR=st["CAGR"], anchor_SHARPE=st["SHARPE"],
                                            within=rr[R_HEAD][0], between=rr[R_HEAD][1],
                                            ratio=rr[R_HEAD][2], R_SPREAD=rr["R_SPREAD"][2],
                                            R_SD=rr["R_SD"][2]))
            P(f"  ladder done: {constr} / {mech}  ({time.time()-t0:.0f}s)")
    LD = pd.DataFrame(ladrows)
    dump(LD, "ladder")
    for constr in CONSTRUCTIONS:
        P(f"  {constr} / {HEAD_TAPE} / {HEAD_MECH} / {HEAD_LADDER}: ratio vs lambda "
          "(anchor MaxDD in brackets):")
        for panel in PANELS:
            s = LD[(LD.constr == constr) & (LD.panel == panel) & (LD.mech == HEAD_MECH)
                   & (LD.frac_ladder == HEAD_LADDER)].sort_values("lam")
            P(f"    {panel:<6s} " + "  ".join(f"{r.lam:.2f}:{r.ratio:.3f}[{r.anchor_MAXDD:6.2f}%]"
                                              for r in s.itertuples()))
    P("  ELASTICITIES (d log x / d log lambda; 1.000 == exactly homogeneous of degree 1):")
    elrows = []
    for constr in CONSTRUCTIONS:
        for panel in PANELS:
            for mech in MECHS:
                s = LD[(LD.constr == constr) & (LD.panel == panel) & (LD.mech == mech)
                       & (LD.frac_ladder == HEAD_LADDER)].sort_values("lam")
                x = np.log(s.lam.values)
                e = {}
                for col in ("anchor_MAXDD", "within", "between", "ratio"):
                    y = np.abs(s[col].values.astype(float))
                    ok = np.isfinite(y) & (y > 0)
                    e[col] = float(np.polyfit(x[ok], np.log(y[ok]), 1)[0]) if ok.sum() > 2 else np.nan
                elrows.append(dict(constr=constr, panel=panel, mech=mech, **e))
                if mech == HEAD_MECH:
                    P(f"    {constr:<9s} {panel:<6s} {mech:<9s} LEVEL {e['anchor_MAXDD']:+.4f}   "
                      f"within {e['within']:+.4f}   between {e['between']:+.4f}   "
                      f"RATIO {e['ratio']:+.4f}")
    EL = pd.DataFrame(elrows)
    dump(EL, "elasticity")

    # ------------------------------------------- ARM 2: the solved match and the landing
    P("")
    P("## ARM 2 — THE TEST ITSELF: solve the scale that puts the donor's anchor book on SMALL's")
    P("##   level, then ask whether the donor's ratio LANDS on SMALL's.")

    def solve_lambda(tape, panel, mech, stat, target):
        lo, hi = 0.10, 6.0
        f = lambda L: abs(six_stats(anchor_book(tape, panel, L, mech))[stat])
        t = abs(target)
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if f(mid) < t:
                lo = mid
            else:
                hi = mid
        L = 0.5 * (lo + hi)
        return L, f(L)

    landrows = []
    for tape in TAPES:
        tgt_stats = six_stats(anchor_book(tape, TARGET))
        for donor in DONORS:
            for mech in MECHS:
                for targ in TARGETS:
                    if targ == "S_NONE":
                        lam, hit = 1.0, np.nan
                    else:
                        lam, hit = solve_lambda(tape, donor, mech, TARGET_STAT[targ],
                                                tgt_stats[TARGET_STAT[targ]])
                    st_s = six_stats(anchor_book(tape, donor, lam, mech))
                    for constr in CONSTRUCTIONS:
                        Ss = subrows_for(tape, lam, mech, [donor]) if constr == "C_POOLED" else None
                        S1 = subrows_for(tape, 1.0, mech, [donor]) if constr == "C_POOLED" else None
                        St = subrows_for(tape, 1.0, mech, [TARGET]) if constr == "C_POOLED" else None
                        for lad, fr in FRAC_LADDERS.items():
                            R_s = ratio_of(constr, tape, donor, lam, mech, fr, SUB=Ss)[R_HEAD][2]
                            R_d = ratio_of(constr, tape, donor, 1.0, mech, fr, SUB=S1)[R_HEAD][2]
                            R_T = ratio_of(constr, tape, TARGET, 1.0, mech, fr, SUB=St)[R_HEAD][2]
                            g0, g1 = abs(R_d - R_T), abs(R_s - R_T)
                            landrows.append(dict(
                                constr=constr, tape=tape, donor=donor, mech=mech, target=targ,
                                frac_ladder=lad, lam=lam,
                                gross=(GROSS0 * lam if mech == "M_GROSS" else GROSS0),
                                donor_MAXDD=st_s["MAXDD"], target_MAXDD=tgt_stats["MAXDD"],
                                solved_hit=hit, R_unscaled=R_d, R_scaled=R_s, R_target=R_T,
                                gap_before=g0, gap_after=g1,
                                frac_gap_closed=(1.0 - g1 / g0) if g0 else np.nan,
                                lands=bool(g1 <= LAND_BAR * g0)))
        P(f"  landing arm done for {tape}  ({time.time()-t0:.0f}s)")
    LA = pd.DataFrame(landrows)
    dump(LA, "landing")
    for constr in CONSTRUCTIONS:
        P(f"  {constr}, {HEAD_TAPE}, target S_MAXDD:")
        for r in LA[(LA.constr == constr) & (LA.tape == HEAD_TAPE)
                    & (LA.target == "S_MAXDD")].itertuples():
            P(f"    {r.donor:<5s} {r.mech:<9s} {r.frac_ladder:<8s} lambda {r.lam:.4f} "
              f"(gross {r.gross:.4f})  MaxDD {r.donor_MAXDD:7.3f}% == target "
              f"{r.target_MAXDD:7.3f}%   R {r.R_unscaled:.4f} -> {r.R_scaled:.4f} vs SMALL "
              f"{r.R_target:.4f}   gap {r.gap_before:.4f} -> {r.gap_after:.4f} "
              f"({r.frac_gap_closed:+.1%})  {'LANDS' if r.lands else 'MISSES'}")
    hl = LA[LA.target == "S_MAXDD"]
    P(f"  LANDING TALLY at the pre-registered {LAND_BAR:.0%} bar, target S_MAXDD: "
      f"{int(hl.lands.sum())} of {len(hl)} (constr, tape, donor, mech, ladder) cells; median "
      f"gap closed {hl.frac_gap_closed.median():+.1%}.")
    for targ in TARGETS[1:]:
        s = LA[LA.target == targ]
        P(f"    target {targ:<8s}: {int(s.lands.sum())} of {len(s)} land; median gap closed "
          f"{s.frac_gap_closed.median():+.1%}")
    for constr in CONSTRUCTIONS:
        s = hl[hl.constr == constr]
        P(f"    {constr}: {int(s.lands.sum())} of {len(s)} land; median gap closed "
          f"{s.frac_gap_closed.median():+.1%}")

    # ---------------------------------------------- ARM 3: the moving-block null band
    P("")
    P(f"## ARM 3 — the MOVING-BLOCK NULL ({NBOOT} draws, L={BLOCK}) on the C_BOOK construction.")
    P("##   1157 found the SMALL cell already inside its own 90% band; a residual gap has to")
    P("##   clear the SAME band to mean anything.")
    nullrows = []
    tgt_dd = six_stats(anchor_book(HEAD_TAPE, TARGET))["MAXDD"]
    for panel in PANELS:
        lam = 1.0 if panel == TARGET else solve_lambda(HEAD_TAPE, panel, HEAD_MECH,
                                                       "MAXDD", tgt_dd)[0]
        r = anchor_book(HEAD_TAPE, panel, lam, HEAD_MECH)
        rng2 = np.random.default_rng(seed_of("null", panel))
        n = len(r)
        draws = []
        for _ in range(NBOOT):
            nb = int(np.ceil(n / BLOCK))
            stt = rng2.integers(0, max(n - BLOCK, 1), size=nb)
            idx = (np.concatenate([np.arange(s, s + BLOCK) for s in stt]) % n)[:n]
            rr = r[idx]
            vals = {f: [six_stats(p) for p in parts_at(rr, f, "ALIGNED")]
                    for f in FRAC_LADDERS[HEAD_LADDER]}
            groups = {f: [[s[HEAD_STAT] for s in vals[f]]] for f in FRAC_LADDERS[HEAD_LADDER]}
            med = {f: float(np.nanmedian([s[HEAD_STAT] for s in vals[f]]))
                   for f in FRAC_LADDERS[HEAD_LADDER]}
            draws.append(ratio_from(groups, med, FRAC_LADDERS[HEAD_LADDER],
                                    matched_exact)[R_HEAD][2])
        dr = np.asarray([x for x in draws if np.isfinite(x)], float)
        pt = ratio_of("C_BOOK", HEAD_TAPE, panel, lam, HEAD_MECH, FRAC_LADDERS[HEAD_LADDER])[R_HEAD][2]
        nullrows.append(dict(panel=panel, lam=lam, point=pt, null_median=float(np.median(dr)),
                             p05=float(np.percentile(dr, 5)), p95=float(np.percentile(dr, 95)),
                             share_sub1=float((dr < 1).mean()), n_draws=len(dr)))
        P(f"  {panel:<6s} lambda {lam:.4f}  point {pt:.4f}  null median {np.median(dr):.4f}"
          f"  90% band [{np.percentile(dr,5):.4f}, {np.percentile(dr,95):.4f}]"
          f"  share sub-1 {(dr<1).mean():.3f}")
    NU = pd.DataFrame(nullrows)
    dump(NU, "nulls")
    tb = NU[NU.panel == TARGET].iloc[0]
    overlap = []
    for r in NU[NU.panel != TARGET].itertuples():
        ov = not (r.p95 < tb.p05 or tb.p95 < r.p05)
        overlap.append(ov)
        P(f"  {r.panel} scaled band [{r.p05:.4f}, {r.p95:.4f}] vs SMALL [{tb.p05:.4f}, "
          f"{tb.p95:.4f}] -> {'OVERLAP — not distinguishable' if ov else 'DISJOINT'}")

    # ------------------------------------------------ ARM 4: rule 8 + both KEEP paths
    P("")
    P("## ARM 4 — PROTOCOL rule 8 WALK-FORWARD and BOTH KEEP PATHS on every book this run")
    P("##   builds.  lambda is CHOSEN on the FIRST HALF only (matched to SMALL's IS-half MaxDD)")
    P("##   and the second half is untouched.")
    wfrows = []
    for tape in TAPES:
        dT = cells[(tape, TARGET)]
        insT, oosT = dT["ins"][dT["warm"]], dT["oos"][dT["warm"]]
        rT = anchor_book(tape, TARGET)
        tgt_is = six_stats(rT[insT])["MAXDD"]
        T_is = ratio_of("C_BOOK", tape, TARGET, 1.0, HEAD_MECH, FRAC_LADDERS[HEAD_LADDER])[R_HEAD][2]
        for donor in DONORS:
            d = cells[(tape, donor)]
            warm = d["warm"]
            ins, oos = d["ins"][warm], d["oos"][warm]
            spyw = d["px"]["SPY"].pct_change().fillna(0.0).values[warm]
            lbw = backtest(d["px"], rules_v2_weights(d["px"]), cost_bps=COST,
                           freq="W")["returns"].values[warm]
            sb, lbm = blocks_m(spyw, ins, oos), blocks_m(lbw, ins, oos)
            lo, hi = 0.10, 6.0
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                if abs(six_stats(anchor_book(tape, donor, mid, HEAD_MECH)[ins])["MAXDD"]) < abs(tgt_is):
                    lo = mid
                else:
                    hi = mid
            lam_is = 0.5 * (lo + hi)
            lam_full = solve_lambda(tape, donor, HEAD_MECH, "MAXDD",
                                    six_stats(rT)["MAXDD"])[0]
            for name, lam in (("ANCHOR", 1.0), ("IS_MATCHED", lam_is), ("FULL_MATCHED", lam_full)):
                r = anchor_book(tape, donor, lam, HEAD_MECH)
                b = blocks_m(r, ins, oos)
                l4b, l4a = legs_4b(b, sb), legs_4a(b, lbm)

                def rat(seg):
                    vals = {f: [six_stats(p) for p in parts_at(seg, f, "ALIGNED")]
                            for f in FRAC_LADDERS[HEAD_LADDER]}
                    groups = {f: [[s[HEAD_STAT] for s in vals[f]]]
                              for f in FRAC_LADDERS[HEAD_LADDER]}
                    med = {f: float(np.nanmedian([s[HEAD_STAT] for s in vals[f]]))
                           for f in FRAC_LADDERS[HEAD_LADDER]}
                    return ratio_from(groups, med, FRAC_LADDERS[HEAD_LADDER],
                                      matched_exact)[R_HEAD][2]

                wfrows.append(dict(
                    tape=tape, donor=donor, arm=name, lam=lam, gross=GROSS0 * lam,
                    CAGR=b["CAGR"], Sharpe=b["Sharpe"], MaxDD=b["MaxDD"], H1=b["H1"], H2=b["H2"],
                    OOS_CAGR=b["OOS_CAGR"], OOS_Sharpe=b["OOS_Sharpe"], OOS_MaxDD=b["OOS_MaxDD"],
                    spy_OOS_CAGR=sb["OOS_CAGR"], spy_OOS_Sharpe=sb["OOS_Sharpe"],
                    spy_OOS_MaxDD=sb["OOS_MaxDD"], live_OOS_Sharpe=lbm["OOS_Sharpe"],
                    live_OOS_MaxDD=lbm["OOS_MaxDD"], R_IS=rat(r[ins]), R_OOS=rat(r[oos]),
                    R_target_IS=rat(rT[insT]), R_target_OOS=rat(rT[oosT]),
                    **l4b, **l4a, pass_4b=all(l4b.values()), pass_4a=all(l4a.values())))
                w = wfrows[-1]
                P(f"  {tape:<10s} {donor:<5s} {name:<13s} lambda {lam:.4f} (gross {GROSS0*lam:.4f})"
                  f"  full {b['CAGR']:6.2%} / {b['Sharpe']:.3f} / {b['MaxDD']:7.2%}"
                  f"  halves {b['H1']:.3f}/{b['H2']:.3f}  OOS {b['OOS_CAGR']:6.2%} / "
                  f"{b['OOS_Sharpe']:.3f} / {b['OOS_MaxDD']:7.2%}"
                  f"  4b {'PASS' if all(l4b.values()) else 'FAIL'}"
                  f"  4a {'PASS' if all(l4a.values()) else 'FAIL'}")
                P(f"     {'':34s} ratio IS {w['R_IS']:.4f} vs SMALL IS {w['R_target_IS']:.4f}"
                  f"   |   OOS {w['R_OOS']:.4f} vs SMALL OOS {w['R_target_OOS']:.4f}")
    WF = pd.DataFrame(wfrows)
    dump(WF, "walkforward")
    P("  SPY OOS: " + ", ".join(
        f"{t} {WF[WF.tape==t].spy_OOS_CAGR.iloc[0]:.2%} / "
        f"{WF[WF.tape==t].spy_OOS_Sharpe.iloc[0]:.3f} / {WF[WF.tape==t].spy_OOS_MaxDD.iloc[0]:.2%}"
        for t in TAPES))

    # --------------------------------------------------------------------- hypotheses
    P("")
    P("## HYPOTHESES — declared in the docstring, scored here")
    mono = True
    for panel in PANELS:
        s = LD[(LD.constr == "C_BOOK") & (LD.panel == panel) & (LD.mech == HEAD_MECH)
               & (LD.frac_ladder == HEAD_LADDER)].sort_values("lam")
        mono &= bool((np.diff(np.abs(s.anchor_MAXDD.values)) > 0).all())
    e_head = EL[(EL.panel.isin(DONORS)) & (EL.mech == HEAD_MECH)]
    h = [
        ("H_MONO", "|MaxDD| is monotone increasing in the scale on every panel (the bisection "
         "target is well posed)", mono),
        ("H_MATCH", "a scale exists that hits SMALL's full-tape MaxDD to < 0.01 pp on every "
         "donor-mechanism cell",
         bool((np.abs(hl.donor_MAXDD - hl.target_MAXDD) < 0.01).all())),
        ("H_LAND", f"THE QUEUE'S PREDICTION — the scaled donor LANDS on SMALL's ratio (closes "
         f">= {LAND_BAR:.0%} of the gap) on a MAJORITY of cells", bool(hl.lands.mean() > 0.5)),
        ("H_INVAR", "the ratio is near scale-INVARIANT: |elasticity of the ratio| < 0.15 on "
         "every donor cell against ~0.9 for the level itself",
         bool((e_head["ratio"].abs() < 0.15).all()
              and (e_head["anchor_MAXDD"].abs() > 0.8).all())),
        ("H_HOMO", "the mechanism: BOTH ratio terms are homogeneous of degree ~1 in the scale "
         "(|elasticity - 1| < 0.15 for within AND between)",
         bool(((e_head["within"] - 1).abs() < 0.15).all()
              and ((e_head["between"] - 1).abs() < 0.15).all())),
        ("H_NULL", "the residual donor-vs-SMALL gap after matching clears the moving-block null "
         "band (the bands are DISJOINT)", bool(len(overlap) and not any(overlap))),
        ("H_CONSTR", "the verdict is the same on BOTH constructions (1148/1157's pooled object "
         "and the single anchor book)",
         bool((hl[hl.constr == "C_POOLED"].lands.mean() > 0.5)
              == (hl[hl.constr == "C_BOOK"].lands.mean() > 0.5))),
    ]
    for k, w, ok in h:
        P(f"  [{'YES' if ok else 'NO ':<3s}] {k:<9s} {w}")
    dump(pd.DataFrame([dict(hypothesis=k, statement=w, holds=bool(ok)) for k, w, ok in h]),
         "hypotheses")

    # ------------------------------------------------------------------ the KEEP paths
    P("")
    P("## BOTH KEEP PATHS (PROTOCOL rule 4)")
    P(f"  4a (beat the live book): {int(WF.pass_4a.sum())} of {len(WF)} books.")
    P(f"  4b (capital-worthy):     {int(WF.pass_4b.sum())} of {len(WF)} books.")
    for r in WF.itertuples():
        P(f"    {r.tape:<10s} {r.donor:<5s} {r.arm:<13s} 4b "
          + " ".join(f"{k}={'T' if getattr(r, k) else 'F'}"
                     for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
          + "   4a " + " ".join(f"{k}={'T' if getattr(r, k) else 'F'}"
                                for k in ("A_H1", "A_H2", "A_DD")))
    P("  NOTHING IS PROPOSED.  Every 4b pass here is the INCUMBENT anchor book at its own gross")
    P("  0.75, already in the record; every SCALED book is a LEVERAGED DIAGNOSTIC (gross above 1,")
    P("  negative cash, no financing charge) built to test an arithmetic claim about a ratio.")
    P("  No memo.  RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py untouched (rule 6).")

    dump(pd.DataFrame(gaterows), "gates")
    P("")
    P(f"# done in {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

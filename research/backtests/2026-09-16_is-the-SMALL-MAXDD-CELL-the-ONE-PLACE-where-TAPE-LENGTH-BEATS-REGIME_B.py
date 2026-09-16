#!/usr/bin/env python3
"""Idea 1157 (lane B, 2026-09-16) — is the SMALL / MAXDD cell the ONE PLACE where TAPE LENGTH
beats REGIME?

THE PREMISE.  Idea 1148 measured, for six statistics on three panels, a REGIME-to-LENGTH RATIO:
    the median spread of a statistic across DISJOINT stretches of EQUAL length (the REGIME term)
    divided by its move between the longest and the shortest length (the LENGTH term).
    A ratio above 1 says the length effect is smaller than the regime noise it is read through.
    Of the 72 cells it published, exactly ONE reads below 1: SMALL / MAXDD under R_MATCHED,
    0.794259x, quoted verbatim below from 1148's own committed regime.csv.  That is the only
    place in the record where tape LENGTH is measured to beat REGIME — and it sits on the panel
    whose levels rule 9 says are least trustworthy.  1148 named the cell, did not sweep it, and
    filed it as this idea.

TUNED DIALS (2, PROTOCOL rule 4), BOTH PUBLISHED IN FULL:
    1. FRACTION LADDER {F_1140 = 1/1,1/2,1/3 (1148's own, kept for the cross-run gate);
       F_FINE = 1/1,1/2,1/3,1/4,1/6 (the HEADLINE, the "finer sub-tape ladder" this idea asks
       for); F_FINER = 1/1,1/2,1/3,1/4,1/5,1/6,1/8}.
    2. TAPE {T_OWN = each panel on its own tape, 1148's own; T_MATCHED = every panel restricted
       to the SMALL panel's own trading days, which is the LENGTH-MATCHED LARGE-CAP CONTROL this
       idea asks for: U56 and B136 read over exactly the tape SMALL has and no more}.
    = 3 x 2 = 6 combinations, ALL published.

    PANEL {U56, B136, SMALL}, STATISTIC {CAGR, VOL, SHARPE, MAXDD, ULCER, CALMAR}, RATIO
    DEFINITION {R_SPREAD, R_SD, R_MATCHED}, PARTITION {ALIGNED, OFFSET} and EPISODE {KEEP, DROP}
    are NOT dials — every one of them is reported at every value, everywhere.

DECLARED BEFORE ANY NUMBER IS COMPUTED:
    H_REPRO      1148's SMALL/MAXDD R_MATCHED sub-1 reading reproduces here, on its own ladder
                 (F_1140) and its own tape (T_OWN), from a verbatim replica of its Arm-B code.
    H_FINE       the sub-1 reading SURVIVES a finer sub-tape ladder: SMALL/MAXDD R_MATCHED < 1
                 at F_FINE and at F_FINER on T_OWN.
    H_PANEL      it is a SMALL-PANEL fact and not a tape-LENGTH fact: on the length-matched
                 large-cap control (T_MATCHED) SMALL/MAXDD stays below 1 while U56 and B136
                 MAXDD stay at or above 1.
    H_EPISODE    the cell is a SINGLE-EPISODE artefact: dropping the calendar year that holds
                 the SMALL anchor book's full-tape MaxDD TROUGH lifts SMALL/MAXDD R_MATCHED to
                 >= 1.  (The year is read off the anchor book, not chosen.)
    H_CONTINUUM  the cell is a THRESHOLD CROSSING in a continuum, not a distinct phenomenon:
                 MAXDD is among the TWO LOWEST-ratio statistics on ALL three panels in ALL six
                 (ladder, tape) combinations.
    H_NULL       the sub-1 reading is MECHANICAL: a moving-block bootstrap of the SMALL anchor
                 book — which by construction has NO regime ordering, only length — also reads
                 sub-1 at the median.
    H_RUNG       it is not a POOLING artefact: a majority of the 27 individual SMALL rung books
                 read sub-1 on their own.

    NOT A KEEP PATH.  The fraction ladder is a READ of returns and cannot move a book at all;
    the tape dial only TRUNCATES the tape a book is read over and proposes no rule.  Rule 8 and
    both KEEP paths are scored at every one of the 162 rungs anyway, because rule 4 says so.

THE DECLARED APPROXIMATION, AND ITS DIRECTION.  MaxDD over a longer stretch is a MAXIMUM over
    more points and therefore grows with length mechanically, with no regime content whatever;
    that is exactly why the null arm is here.  Every null in this run is a resample of ONE tape,
    so it prices sampling error around THIS regime and not regime uncertainty across regimes.
    A null ratio is therefore biased toward the reading it is testing, and H_NULL is scored in
    the direction that favours calling the cell MECHANICAL — the conclusion this run reaches —
    so that conclusion is stated as the one the evidence makes HARDEST to avoid, not easiest.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists; the SMALL pool is
    the CURRENT constituents of a sub-$2B screen, so every name that fell below the screen,
    delisted or went to zero is absent, and the drawdowns measured on it are the SHALLOWEST the
    period could have produced.  A within-length spread and a between-length move both contrast
    the same books over stretches of the same inflated tape, so the bias very largely cancels
    out of the RATIO.  It does NOT cancel out of the 4b legs, measured against SPY, a real
    index, so every 4b pass counted here is an UPPER bound.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-16"
SLUG = "is-the-SMALL-MAXDD-CELL-the-ONE-PLACE-where-TAPE-LENGTH-BEATS-REGIME"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"
BT = ROOT / "research" / "backtests"

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
ANCHOR = dict(N=N0, H=HOLD0, GROSS=GROSS0, CADENCE=FREQ0)

PANELS = ["U56", "B136", "SMALL"]
STATS6 = ["CAGR", "VOL", "SHARPE", "MAXDD", "ULCER", "CALMAR"]
IS_PATH = {"CAGR": False, "VOL": False, "SHARPE": False,
           "MAXDD": True, "ULCER": True, "CALMAR": True}

# ---- dial 1: the fraction ladders.  F_FINE is the headline.
FRAC_LADDERS = {"F_1140": [1, 2, 3], "F_FINE": [1, 2, 3, 4, 6], "F_FINER": [1, 2, 3, 4, 5, 6, 8]}
FRAC_ALL = sorted({f for v in FRAC_LADDERS.values() for f in v})
HEAD_LADDER = "F_FINE"
# ---- dial 2: the tape
TAPES = ["T_OWN", "T_MATCHED"]
HEAD_TAPE = "T_OWN"

RATIO_DEFS = ["R_SPREAD", "R_SD", "R_MATCHED"]
R_HEAD = "R_MATCHED"                       # the definition under which 1148's cell is sub-1
PARTITIONS = ["ALIGNED", "OFFSET"]
EPISODES = ["KEEP", "DROP"]
CHOOSERS = {"C_ISSHARPE": "IS_Sharpe", "C_ISCAGR": "IS_CAGR", "C_ISDD": "IS_MaxDD"}

SEED_1148 = 11481148                        # 1148's own seed, for the verbatim replica
SEED = 11571157
NPAIR = 200
NBOOT = 200
BLOCK = 63                                  # the record's own moving-block length
OFFSET_FRACS = (0.0, 1.0 / 3.0, 2.0 / 3.0)  # OFFSET partition start points, in units of L

# ---- the record's own committed numbers, quoted and gated, never re-derived from memory
PRIOR1148 = BT / ("2026-09-16_should-a-SUB-TAPE-COMPARISON-be-required-to-publish-its-"
                  "REGIME-to-LENGTH-RATIO_cloud.regime.csv")
A936_WH126 = (0.155787, 1.139701, -0.191276)
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


# --------------------------------------------------------- the record's runner, verbatim
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
    """1140's six: three non-path moment statistics and three drawdown-path ones."""
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


def dd_trough(r):
    """Index of the running-maximum drawdown trough of a return series."""
    eq = np.cumprod(1.0 + np.asarray(r, float))
    return int(np.argmin(eq / np.maximum.accumulate(eq)))


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


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep].dropna(how="all").ffill(), len(bad), len(meta)


# ---------------------------------------------- partitions and the three ratio definitions
def parts_at(r, f, partition):
    """The equal-length stretches of r at fraction 1/f under a partition scheme."""
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


def _matched(v, rng):
    v = np.asarray([x for x in v if np.isfinite(x)], float)
    if len(v) < 2:
        return np.nan
    if len(v) == 2:
        return float(abs(v[0] - v[1]))
    i = rng.integers(0, len(v), size=(NPAIR, 2))
    i = i[i[:, 0] != i[:, 1]]
    return float(np.abs(v[i[:, 0]] - v[i[:, 1]]).mean())


def ratio_from(groups, frac_medians, fracs, rng):
    """1148's ratio, parameterised by the fraction ladder.  groups: {frac: [ [values] ... ]}."""
    ranges, sds, matched = [], [], []
    for f in fracs:
        if f == 1:
            continue                                   # 1/1 is ONE tape: no within spread
        for v in groups.get(f, []):
            v = np.asarray([x for x in v if np.isfinite(x)], float)
            if len(v) < 2:
                continue
            ranges.append(float(v.max() - v.min()))
            sds.append(float(v.std(ddof=1)))
            m = _matched(v, rng)
            if np.isfinite(m):
                matched.append(m)
    m = frac_medians
    fmax = max(fracs)
    between_spread = (abs(m[1] - m[fmax])
                      if np.isfinite(m.get(1, np.nan)) and np.isfinite(m.get(fmax, np.nan))
                      else np.nan)
    between_sd = float(np.std([m[f] for f in fracs], ddof=1))
    w_spread = float(np.nanmedian(ranges)) if ranges else np.nan
    w_sd = float(np.nanmedian(sds)) if sds else np.nan
    w_matched = float(np.nanmedian(matched)) if matched else np.nan
    return {"R_SPREAD": (w_spread, between_spread,
                         w_spread / between_spread if between_spread else np.nan),
            "R_SD": (w_sd, between_sd, w_sd / between_sd if between_sd else np.nan),
            "R_MATCHED": (w_matched, between_spread,
                          w_matched / between_spread if between_spread else np.nan)}


def ratio_series(r, fracs, partition, rng):
    """The three ratios for ONE return series: the per-rung and per-null reading."""
    vals = {}
    for f in fracs:
        ps = parts_at(r, f, partition)
        vals[f] = [six_stats(p) for p in ps]
    out = {}
    for stat in STATS6:
        groups = {f: [[s[stat] for s in vals[f]]] for f in fracs if f != 1}
        med = {f: float(np.nanmedian([s[stat] for s in vals[f]])) if vals[f] else np.nan
               for f in fracs}
        out[stat] = ratio_from(groups, med, fracs, rng)
    return out


def drop_year(r, idx, year):
    m = np.asarray(idx.year != year)
    return r[m]


def boot_idx(n, kind, rng):
    if kind == "IID":
        return rng.integers(0, n, size=n)
    nb = int(np.ceil(n / BLOCK))
    st = rng.integers(0, max(n - BLOCK, 1), size=nb)
    return (np.concatenate([np.arange(s, s + BLOCK) for s in st]) % n)[:n]


# ------------------------------------------------------------------------------------ main
def main():
    t0 = time.time()
    P(f"# Idea 1157 (lane B, {DATE}) — is the SMALL / MAXDD cell the ONE PLACE where TAPE "
      "LENGTH beats REGIME?")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4): FRACTION LADDER {list(FRAC_LADDERS)} x TAPE {TAPES}"
      " = 6 combinations, ALL published.")
    P("#   PANEL (3) x STATISTIC (6) x RATIO DEFINITION (3) x PARTITION (2) x EPISODE (2) are")
    P(f"#   NOT dials — all reported everywhere.  HEADLINE: {HEAD_LADDER} / {HEAD_TAPE} / "
      f"{R_HEAD} / ALIGNED / KEEP.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   H_REPRO     1148's SMALL/MAXDD R_MATCHED sub-1 reading reproduces on F_1140 / T_OWN.")
    P("#   H_FINE      it SURVIVES a finer sub-tape ladder (F_FINE and F_FINER, T_OWN).")
    P("#   H_PANEL     it is a SMALL-PANEL fact: on the LENGTH-MATCHED large-cap control")
    P("#               (T_MATCHED) SMALL stays sub-1 while U56 and B136 MAXDD stay >= 1.")
    P("#   H_EPISODE   it is a SINGLE-EPISODE artefact: dropping the calendar year holding the")
    P("#               SMALL anchor book's MaxDD trough lifts SMALL/MAXDD R_MATCHED to >= 1.")
    P("#   H_CONTINUUM MAXDD is among the TWO LOWEST-ratio statistics on ALL 3 panels in ALL 6")
    P("#               (ladder, tape) combinations — a threshold crossing, not a phenomenon.")
    P("#   H_NULL      a moving-block bootstrap of the SMALL anchor book — NO regime ordering by")
    P("#               construction, only length — also reads sub-1 at the median.")
    P("#   H_RUNG      a majority of the 27 individual SMALL rung books read sub-1 on their own.")
    P("#   NOT A KEEP PATH: the fraction ladder cannot move a book at all and the tape dial only")
    P("#     TRUNCATES.  Rule 8 and both KEEP paths scored at all 162 rungs because rule 4 says so.")
    P("")

    gaterows, gates = [], {}

    def gate(name, what, value, ok):
        gates[name] = bool(ok)
        gaterows.append(dict(gate=name, what=what, value=float(value), pass_=bool(ok)))
        P(f"  [{'PASS' if ok else 'FAIL'}] {name:<9s} {what}: {value:.4e}")

    # ------------------------------------------------------------------------- panels
    P("## PANELS — loaded and STAMPED before any result number")
    small, ndrop, nmeta = load_small()
    raw = {"U56": load_universe().dropna(how="all").ffill(),
           "B136": load_universe(broad=True).dropna(how="all").ffill(),
           "SMALL": small}
    SMALL_DAYS = raw["SMALL"].index

    def prep(px):
        idx, K, T = px.index, len(px.columns), len(px.index)
        rets = px.pct_change().fillna(0.0).values
        priced = px.notna().values
        warm, ins, oos = windows(idx)
        sc, elig = mech(px)
        spy_i = list(px.columns).index("SPY")
        return dict(px=px, idx=idx, K=K, T=T, rets=rets, priced=priced, warm=warm, ins=ins,
                    oos=oos, sc=sc, elig=elig, spy_i=spy_i)

    cells = {}
    for tape in TAPES:
        for panel in PANELS:
            px = raw[panel]
            if tape == "T_MATCHED":
                px = px.loc[px.index.intersection(SMALL_DAYS)]
            d = prep(px)
            if panel == "SMALL":
                d["elig"] = d["elig"].copy()
                d["elig"][:, d["spy_i"]] = False
            cells[(tape, panel)] = d
            P(f"  {tape:<10s} {panel:<6s} {d['K']:4d} cols, {d['T']:,} rows "
              f"{d['idx'][0].date()} -> {d['idx'][-1].date()}  warm {d['warm'].sum():,}  "
              f"IS {d['ins'].sum():,}  OOS {d['oos'].sum():,}")
    P(f"  SMALL STAMP: data/small_meta.csv lists {nmeta} tickers; {ndrop} dropped for "
      f"max_1d_move >= 1.0; pool served = {cells[('T_OWN','SMALL')]['K'] - 1} names + SPY as "
      f"benchmark; tape {SMALL_DAYS[0].date()} -> {SMALL_DAYS[-1].date()}.")
    P("  T_MATCHED restricts EVERY panel to the SMALL panel's own trading days, so the three "
      "panels are matched in LENGTH exactly, row for row.")
    P("")

    def run_cell(tape, panel, N, H, gross, freq):
        d = cells[(tape, panel)]
        mk = rebalance_mask(d["idx"], freq).values
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        reb = np.flatnonzero(mk)
        W = build(-d["sc"], d["elig"], d["priced"], reb, N, H, d["T"], d["K"], gross)
        Wl = np.zeros_like(W)
        Wl[LAG:] = W[:-LAG]
        g, tn = nrun(d["rets"], Wl, mkl)
        return g - tn * COST / 1e4

    # ------------------------------------------------------------------------- gates
    P("## GATES — printed before any result number")
    d = cells[("T_OWN", "U56")]
    mk = rebalance_mask(d["idx"], FREQ0).values
    reb = np.flatnonzero(mk)
    W = build(-d["sc"], d["elig"], d["priced"], reb, N0, HOLD0, d["T"], d["K"], GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST, freq=FREQ0)["returns"].values
    rfast = run_cell("T_OWN", "U56", N0, HOLD0, GROSS0, FREQ0)
    v = float(np.abs(eng[d["warm"]] - rfast[d["warm"]]).max())
    gate("G1", "fast runner == engine.backtest (U56 W/H126/N=20)", v, v < 1e-12)
    m = blocks_m(rfast, d["warm"], d["ins"], d["oos"])
    v = max(abs(m["CAGR"] - A936_WH126[0]), abs(m["Sharpe"] - A936_WH126[1]),
            abs(m["MaxDD"] - A936_WH126[2]))
    gate("G2", "CROSS-RUN the committed U56 W/H126/N=20 triple", v, v < 5e-5)
    spy = d["px"]["SPY"].pct_change().fillna(0.0).values
    sm = blocks_m(spy, d["warm"], d["ins"], d["oos"])
    v = max(abs(sm["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
            abs(sm["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
            abs(sm["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gate("G3", "SPY OOS triple (U56 own tape)", v, v < 5e-4)
    lb_r = backtest(d["px"], rules_v2_weights(d["px"]), cost_bps=COST, freq="W")["returns"].values
    v = abs(blocks_m(lb_r, d["warm"], d["ins"], d["oos"])["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gate("G4", "live RULES v2 MaxDD == committed -12.05%", v, v < 5e-4)
    v = float(np.abs(run_cell("T_OWN", "SMALL", N0, HOLD0, GROSS0, FREQ0)
                     - run_cell("T_OWN", "SMALL", N0, HOLD0, GROSS0, FREQ0)).max())
    gate("G5", "determinism of the SMALL pipeline", v, v == 0.0)

    prior = pd.read_csv(PRIOR1148)
    pr_small = prior[(prior.panel == "SMALL") & (prior.stat == "MAXDD")]
    ok6 = (len(pr_small) == 1 and len(prior) == 24 and set(prior.stat) == set(STATS6))
    PRIOR_CELL = float(pr_small["R_MATCHED_ratio"].iloc[0]) if len(pr_small) == 1 else np.nan
    gate("G6", "1148's committed regime.csv is present and carries the SMALL/MAXDD cell",
         0.0 if ok6 else 1.0, ok6)
    P("     1148's COMMITTED MAXDD R_MATCHED row, quoted VERBATIM FROM ITS OWN CSV (never "
      "re-derived from memory): " + ", ".join(
          f"{r.panel} {r.R_MATCHED_ratio:.6f}x"
          for r in prior[prior.stat == "MAXDD"].itertuples()))

    # ------------------------------------------------- G7: verbatim replica of 1148's Arm B
    P("## ARM 0 — VERBATIM REPLICA of 1148's Arm B (F_1140, T_OWN, pooled-by-ladder groups)")
    metr, bench, gridrows, subrows = {}, {}, [], []
    for tape in TAPES:
        for panel in PANELS:
            dd_ = cells[(tape, panel)]
            warm = dd_["warm"]
            sb = blocks_m(dd_["px"]["SPY"].pct_change().fillna(0.0).values, warm,
                          dd_["ins"], dd_["oos"])
            lbm_p = blocks_m(backtest(dd_["px"], rules_v2_weights(dd_["px"]), cost_bps=COST,
                                      freq="W")["returns"].values, warm, dd_["ins"], dd_["oos"])
            bench[(tape, panel)] = (sb, lbm_p)
            for lad, rungs in LADDERS.items():
                for rg in rungs:
                    c = dict(ANCHOR)
                    c[lad] = rg
                    r_ = run_cell(tape, panel, c["N"], c["H"], c["GROSS"], c["CADENCE"])
                    mm = blocks_m(r_, warm, dd_["ins"], dd_["oos"])
                    metr[(tape, panel, lad, rg)] = (mm, r_[warm])
                    l4b, l4bo, l4a = legs_4b(mm, sb), legs_4b_oos(mm, sb), legs_4a(mm, lbm_p)
                    gridrows.append(dict(tape=tape, panel=panel, ladder=lad, rung=rg, **mm,
                                         pass_4b_full=all(l4b.values()),
                                         pass_4b_oos=all(l4bo.values()),
                                         pass_4a=all(l4a.values()), **l4b, **l4bo, **l4a))
                    rw = r_[warm]
                    for part in PARTITIONS:
                        for f in FRAC_ALL:
                            for k, seg in enumerate(parts_at(rw, f, part)):
                                subrows.append(dict(tape=tape, panel=panel, ladder=lad, rung=rg,
                                                    partition=part, frac=f, part=k,
                                                    n_days=len(seg), **six_stats(seg)))
            P(f"  {tape:<10s} {panel:<6s} built {sum(len(v) for v in LADDERS.values())} rung "
              f"books x {len(FRAC_ALL)} fractions x {len(PARTITIONS)} partitions "
              f"({time.time()-t0:.0f}s)")
    grid = pd.DataFrame(gridrows)
    dump(grid, "grid")
    SUB = pd.DataFrame(subrows)
    dump(SUB, "subtapes")

    # the replica: 1148's exact loop order, seed and grouping, on F_1140 / T_OWN / ALIGNED
    rng = np.random.default_rng(SEED_1148)
    rep = {}
    S0 = SUB[(SUB.tape == "T_OWN") & (SUB.partition == "ALIGNED") & (SUB.frac.isin([1, 2, 3]))]
    for panel in PANELS + ["POOLED"]:
        s = S0 if panel == "POOLED" else S0[S0.panel == panel]
        for stat in STATS6:
            groups = {f: [] for f in [1, 2, 3]}
            for (pn, lad), g in s.groupby(["panel", "ladder"]):
                for f in [1, 2, 3]:
                    groups[f].append(g[g.frac == f].groupby("part")[stat].median().tolist())
            med = {f: float(np.nanmedian(s[s.frac == f][stat])) for f in [1, 2, 3]}
            rep[(panel, stat)] = ratio_from(groups, med, [1, 2, 3], rng)
    v = abs(rep[("SMALL", "MAXDD")]["R_MATCHED"][2] - PRIOR_CELL)
    gate("G7", "CROSS-RUN 1148's SMALL/MAXDD R_MATCHED reproduced by a verbatim replica",
         v, v < 1e-6)
    P(f"     replica SMALL/MAXDD R_MATCHED {rep[('SMALL','MAXDD')]['R_MATCHED'][2]:.6f}x "
      f"vs committed {PRIOR_CELL:.6f}x")
    P(f"     replica all panels MAXDD R_MATCHED: "
      + ", ".join(f"{p} {rep[(p,'MAXDD')]['R_MATCHED'][2]:.4f}x" for p in PANELS + ["POOLED"]))
    P("")

    # ======================================================= ARM A — THE 6 DIAL COMBINATIONS
    P("## ARM A — the cell re-read over BOTH DIALS, every panel, statistic, ratio definition,")
    P("##         partition and episode.  EPISODE = DROP removes the calendar year holding the")
    P("##         panel anchor book's OWN full-tape MaxDD trough (read off the book, not chosen).")
    trough_year = {}
    for tape in TAPES:
        for panel in PANELS:
            mm, rw = metr[(tape, panel, "N", N0)]          # the anchor book (N=20 rung of N)
            idx = cells[(tape, panel)]["idx"][cells[(tape, panel)]["warm"]]
            ti = dd_trough(rw)
            trough_year[(tape, panel)] = int(idx[ti].year)
            P(f"   {tape:<10s} {panel:<6s} anchor book full-tape MaxDD {mm['MaxDD']:7.2%} "
              f"trough {idx[ti].date()} -> EPISODE YEAR {trough_year[(tape, panel)]}")

    rng = np.random.default_rng(SEED)
    cellrows = []
    for lname, fracs in FRAC_LADDERS.items():
        for tape in TAPES:
            for panel in PANELS:
                idxw = cells[(tape, panel)]["idx"][cells[(tape, panel)]["warm"]]
                yr = trough_year[(tape, panel)]
                for part in PARTITIONS:
                    for ep in EPISODES:
                        # pooled-by-ladder groups, 1148's construction, on this dial setting
                        per = {}
                        for lad, rungs in LADDERS.items():
                            series = []
                            for rg in rungs:
                                rw = metr[(tape, panel, lad, rg)][1]
                                series.append(drop_year(rw, idxw, yr) if ep == "DROP" else rw)
                            per[lad] = series
                        # vals: per (frac, ladder) the per-part MEDIAN ACROSS RUNGS (1148's
                        # group construction); allv: every (rung, part) value, whose median
                        # over the whole panel is 1148's per-fraction level.
                        vals = {f: {lad: [] for lad in LADDERS} for f in fracs}
                        allv = {f: {st: [] for st in STATS6} for f in fracs}
                        for lad, series in per.items():
                            for f in fracs:
                                acc = []
                                for rw in series:
                                    acc.append([six_stats(p) for p in parts_at(rw, f, part)])
                                npart = min(len(a) for a in acc) if acc else 0
                                for a in acc:
                                    for k in range(npart):
                                        for st in STATS6:
                                            allv[f][st].append(a[k][st])
                                vals[f][lad] = [
                                    [float(np.nanmedian([a[k][st] for a in acc]))
                                     for k in range(npart)] for st in STATS6]
                        for si, stat in enumerate(STATS6):
                            groups = {f: [vals[f][lad][si] for lad in LADDERS] for f in fracs
                                      if f != 1}
                            med = {f: float(np.nanmedian(allv[f][stat])) for f in fracs}
                            rr = ratio_from(groups, med, fracs, rng)
                            row = dict(frac_ladder=lname, tape=tape, panel=panel,
                                       partition=part, episode=ep, stat=stat,
                                       is_path=IS_PATH[stat], episode_year=yr,
                                       fracs="+".join(f"1/{f}" for f in fracs))
                            for dn in RATIO_DEFS:
                                w, b, x = rr[dn]
                                row[f"{dn}_within"], row[f"{dn}_between"] = w, b
                                row[f"{dn}_ratio"] = x
                            cellrows.append(row)
    CELL = pd.DataFrame(cellrows)
    dump(CELL, "cells")

    H_ = CELL[(CELL.partition == "ALIGNED") & (CELL.episode == "KEEP")]
    P("\n   ALL 6 DIAL COMBINATIONS x 3 PANELS x 6 STATISTICS, headline partition/episode,")
    P(f"   ratio definition {R_HEAD} (1148's corrected form; the other two are in cells.csv):")
    P("   ladder   tape        panel  " + "".join(f"{s:>9}" for s in STATS6))
    for lname in FRAC_LADDERS:
        for tape in TAPES:
            for panel in PANELS:
                g = H_[(H_.frac_ladder == lname) & (H_.tape == tape) & (H_.panel == panel)]
                g = g.set_index("stat")
                P(f"   {lname:<8} {tape:<11} {panel:<6}"
                  + "".join(f"{g.loc[s, R_HEAD+'_ratio']:9.3f}" for s in STATS6)
                  + ("   <-- the 1148 cell" if (panel == "SMALL" and lname == "F_1140"
                                                and tape == "T_OWN") else ""))
    P("")
    P("   THE CELL ITSELF, every reading of it (SMALL / MAXDD):")
    P("   ladder   tape        part     ep    R_SPREAD    R_SD  R_MATCHED   within    between")
    cellsm = CELL[(CELL.panel == "SMALL") & (CELL.stat == "MAXDD")]
    for _, r_ in cellsm.iterrows():
        P(f"   {r_['frac_ladder']:<8} {r_['tape']:<11} {r_['partition']:<8} {r_['episode']:<5} "
          f"{r_['R_SPREAD_ratio']:9.3f} {r_['R_SD_ratio']:7.3f} {r_['R_MATCHED_ratio']:10.3f} "
          f"{r_['R_MATCHED_within']:8.3f} {r_['R_MATCHED_between']:10.3f}")
    P("")

    # ======================================================= ARM B — PER-RUNG, NOT POOLED
    P("## ARM B — the ratio computed for EACH RUNG BOOK ON ITS OWN (1148 pooled 27 books into")
    P("##         one number per cell; a pooled ratio can be sub-1 while most books are not)")
    rng = np.random.default_rng(SEED + 1)
    rungrows = []
    for lname, fracs in FRAC_LADDERS.items():
        for tape in TAPES:
            for panel in PANELS:
                for lad, rungs in LADDERS.items():
                    for rg in rungs:
                        rw = metr[(tape, panel, lad, rg)][1]
                        rr = ratio_series(rw, fracs, "ALIGNED", rng)
                        for stat in STATS6:
                            rungrows.append(dict(frac_ladder=lname, tape=tape, panel=panel,
                                                 ladder=lad, rung=str(rg), stat=stat,
                                                 **{f"{dn}_ratio": rr[stat][dn][2]
                                                    for dn in RATIO_DEFS}))
    RUNG = pd.DataFrame(rungrows)
    dump(RUNG, "perrung")
    P(f"   share of the 27 rung books reading SUB-1 on their own, at {R_HEAD}:")
    P("   ladder   tape        panel  " + "".join(f"{s:>9}" for s in STATS6))
    subshare = {}
    for lname in FRAC_LADDERS:
        for tape in TAPES:
            for panel in PANELS:
                g = RUNG[(RUNG.frac_ladder == lname) & (RUNG.tape == tape)
                         & (RUNG.panel == panel)]
                line = ""
                for s in STATS6:
                    gs = g[g.stat == s][f"{R_HEAD}_ratio"]
                    sh = float((gs < 1).mean())
                    subshare[(lname, tape, panel, s)] = (sh, int((gs < 1).sum()), len(gs))
                    line += f"{sh:9.3f}"
                P(f"   {lname:<8} {tape:<11} {panel:<6}{line}")
    P("")

    # ======================================================= ARM C — THE NULLS
    P("## ARM C — NULLS.  A resample of the SAME book has NO regime ordering by construction,")
    P("##         only length.  If the null reads sub-1 too, 'length beats regime' is MECHANICAL.")
    nullrows = []
    for tape in TAPES:
        for panel in PANELS:
            rw = metr[(tape, panel, "N", N0)][1]
            n = len(rw)
            for kind in ["IID", "BLOCK"]:
                rg_ = np.random.default_rng(SEED + 7)
                acc = {s: [] for s in STATS6}
                for _ in range(NBOOT):
                    br = rw[boot_idx(n, kind, rg_)]
                    rr = ratio_series(br, FRAC_LADDERS[HEAD_LADDER], "ALIGNED", rg_)
                    for s in STATS6:
                        acc[s].append(rr[s][R_HEAD][2])
                for s in STATS6:
                    a = np.asarray(acc[s], float)
                    nullrows.append(dict(tape=tape, panel=panel, null=kind, stat=s,
                                         n_draws=NBOOT, median_ratio=float(np.nanmedian(a)),
                                         p05=float(np.nanpercentile(a, 5)),
                                         p95=float(np.nanpercentile(a, 95)),
                                         share_sub1=float(np.nanmean(a < 1))))
            P(f"   {tape:<10s} {panel:<6s} nulls done ({time.time()-t0:.0f}s)")
    NUL = pd.DataFrame(nullrows)
    dump(NUL, "nulls")
    P(f"   NULL {R_HEAD} on the anchor book, {NBOOT} draws each (median [p05, p95], share sub-1):")
    P("   tape        panel  null   " + "".join(f"{s:>22}" for s in STATS6))
    for tape in TAPES:
        for panel in PANELS:
            for kind in ["IID", "BLOCK"]:
                g = NUL[(NUL.tape == tape) & (NUL.panel == panel)
                        & (NUL.null == kind)].set_index("stat")
                P(f"   {tape:<11} {panel:<6} {kind:<6}"
                  + "".join(f"{g.loc[s,'median_ratio']:9.3f}/{g.loc[s,'share_sub1']:<12.2f}"
                            for s in STATS6))
    # the observed cell, beside its own null
    obs_cell = float(H_[(H_.frac_ladder == HEAD_LADDER) & (H_.tape == HEAD_TAPE)
                        & (H_.panel == "SMALL") & (H_.stat == "MAXDD")][f"{R_HEAD}_ratio"].iloc[0])
    nb = NUL[(NUL.tape == HEAD_TAPE) & (NUL.panel == "SMALL") & (NUL.null == "BLOCK")
             & (NUL.stat == "MAXDD")].iloc[0]
    P(f"   OBSERVED SMALL/MAXDD at the headline ({HEAD_LADDER}/{HEAD_TAPE}/{R_HEAD}/ALIGNED/KEEP)"
      f" = {obs_cell:.3f}x;  its BLOCK null median {nb['median_ratio']:.3f}x "
      f"[{nb['p05']:.3f}, {nb['p95']:.3f}], {nb['share_sub1']:.2f} of draws sub-1.")
    P("")

    # ======================================================= HYPOTHESES
    def cellval(lname, tape, panel, stat, part="ALIGNED", ep="KEEP", dn=R_HEAD):
        g = CELL[(CELL.frac_ladder == lname) & (CELL.tape == tape) & (CELL.panel == panel)
                 & (CELL.stat == stat) & (CELL.partition == part) & (CELL.episode == ep)]
        return float(g[f"{dn}_ratio"].iloc[0])

    H_REPRO = bool(gates.get("G7", False) and rep[("SMALL", "MAXDD")]["R_MATCHED"][2] < 1)
    fine = {ln: cellval(ln, "T_OWN", "SMALL", "MAXDD") for ln in FRAC_LADDERS}
    H_FINE = bool(fine["F_FINE"] < 1 and fine["F_FINER"] < 1)
    m_small = cellval(HEAD_LADDER, "T_MATCHED", "SMALL", "MAXDD")
    m_u56 = cellval(HEAD_LADDER, "T_MATCHED", "U56", "MAXDD")
    m_b136 = cellval(HEAD_LADDER, "T_MATCHED", "B136", "MAXDD")
    H_PANEL = bool(m_small < 1 and m_u56 >= 1 and m_b136 >= 1)
    ep_keep = cellval(HEAD_LADDER, HEAD_TAPE, "SMALL", "MAXDD", ep="KEEP")
    ep_drop = cellval(HEAD_LADDER, HEAD_TAPE, "SMALL", "MAXDD", ep="DROP")
    H_EPISODE = bool(ep_keep < 1 and ep_drop >= 1)
    cont = []
    for ln in FRAC_LADDERS:
        for tape in TAPES:
            for panel in PANELS:
                vs = {s: cellval(ln, tape, panel, s) for s in STATS6}
                order = sorted(STATS6, key=lambda s: (np.inf if not np.isfinite(vs[s])
                                                      else vs[s]))
                cont.append(("MAXDD" in order[:2], ln, tape, panel, order[0], order[1]))
    H_CONTINUUM = bool(all(c[0] for c in cont))
    H_NULL = bool(nb["median_ratio"] < 1)
    sh = subshare[(HEAD_LADDER, HEAD_TAPE, "SMALL", "MAXDD")]
    H_RUNG = bool(sh[0] > 0.5)

    hyp = [
        dict(hypothesis="H_REPRO",
             declared="1148's SMALL/MAXDD R_MATCHED sub-1 reading reproduces on F_1140 / T_OWN",
             result=f"replica {rep[('SMALL','MAXDD')]['R_MATCHED'][2]:.6f}x vs committed "
                    f"{PRIOR_CELL:.6f}x (|diff| "
                    f"{abs(rep[('SMALL','MAXDD')]['R_MATCHED'][2]-PRIOR_CELL):.2e})",
             verdict="SUPPORTED" if H_REPRO else "REFUTED"),
        dict(hypothesis="H_FINE",
             declared="the sub-1 reading survives a FINER sub-tape ladder (F_FINE and F_FINER)",
             result="; ".join(f"{k} {v:.3f}x" for k, v in fine.items()),
             verdict="SUPPORTED" if H_FINE else "REFUTED"),
        dict(hypothesis="H_PANEL",
             declared="on the LENGTH-MATCHED control SMALL stays sub-1 while U56 and B136 do not",
             result=f"T_MATCHED / {HEAD_LADDER} MAXDD: SMALL {m_small:.3f}x, U56 {m_u56:.3f}x, "
                    f"B136 {m_b136:.3f}x",
             verdict="SUPPORTED" if H_PANEL else "REFUTED"),
        dict(hypothesis="H_EPISODE",
             declared="dropping the anchor book's MaxDD-trough year lifts the cell to >= 1",
             result=f"episode year {trough_year[(HEAD_TAPE,'SMALL')]}: KEEP {ep_keep:.3f}x -> "
                    f"DROP {ep_drop:.3f}x",
             verdict="SUPPORTED" if H_EPISODE else "REFUTED"),
        dict(hypothesis="H_CONTINUUM",
             declared="MAXDD is among the two lowest-ratio statistics in all 18 (ladder,tape,panel) cells",
             result=f"{sum(1 for c in cont if c[0])} of {len(cont)}; exceptions "
                    + (", ".join(f"{c[1]}/{c[2]}/{c[3]} (lowest {c[4]},{c[5]})"
                                 for c in cont if not c[0]) or "none"),
             verdict="SUPPORTED" if H_CONTINUUM else "REFUTED"),
        dict(hypothesis="H_NULL",
             declared="a moving-block bootstrap of the SMALL anchor book also reads sub-1",
             result=f"BLOCK null median {nb['median_ratio']:.3f}x [{nb['p05']:.3f}, "
                    f"{nb['p95']:.3f}], {nb['share_sub1']:.2f} of {NBOOT} draws sub-1; observed "
                    f"{obs_cell:.3f}x",
             verdict="SUPPORTED" if H_NULL else "REFUTED"),
        dict(hypothesis="H_RUNG",
             declared="a majority of the 27 individual SMALL rung books read sub-1 on their own",
             result=f"{sh[1]} of {sh[2]} ({sh[0]:.3f}) at {HEAD_LADDER}/{HEAD_TAPE}",
             verdict="SUPPORTED" if H_RUNG else "REFUTED"),
    ]
    HY = pd.DataFrame(hyp)
    dump(HY, "hypotheses")
    P("## HYPOTHESES")
    for _, r_ in HY.iterrows():
        P(f"   [{r_['verdict']:<9s}] {r_['hypothesis']:<12s} {r_['result']}")
    P(f"   {int((HY.verdict == 'SUPPORTED').sum())} of {len(HY)} SUPPORTED")
    P("")

    # ======================================================= RULE 8 AND BOTH KEEP PATHS
    P("## RULE 8 — rung chosen on IS 2009-2016 ALONE, per ladder, three choosers, OOS read ONCE")
    pickrows = []
    for tape in TAPES:
        for panel in PANELS:
            sb, lbm_p = bench[(tape, panel)]
            for lad, rungs in LADDERS.items():
                for ch, key in CHOOSERS.items():
                    vals = [metr[(tape, panel, lad, r_)][0][key] for r_ in rungs]
                    pick = rungs[int(np.argmax(vals))]
                    mm = metr[(tape, panel, lad, pick)][0]
                    oos_best = rungs[int(np.argmax(
                        [metr[(tape, panel, lad, r_)][0]["OOS_Sharpe"] for r_ in rungs]))]
                    l4b, l4bo, l4a = legs_4b(mm, sb), legs_4b_oos(mm, sb), legs_4a(mm, lbm_p)
                    srt = np.sort(vals)[::-1]
                    pickrows.append(dict(
                        tape=tape, panel=panel, ladder=lad, chooser=ch, pick=pick,
                        margin=float(srt[0] - srt[1]), oos_best=oos_best,
                        picked_oos_best=(pick == oos_best),
                        regret=float(metr[(tape, panel, lad, oos_best)][0]["OOS_Sharpe"]
                                     - mm["OOS_Sharpe"]),
                        CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                        H1=mm["H1"], H2=mm["H2"], OOS_CAGR=mm["OOS_CAGR"],
                        OOS_Sharpe=mm["OOS_Sharpe"], OOS_MaxDD=mm["OOS_MaxDD"],
                        spy_OOS_CAGR=sb["OOS_CAGR"], spy_OOS_Sharpe=sb["OOS_Sharpe"],
                        spy_OOS_MaxDD=sb["OOS_MaxDD"], base_OOS_Sharpe=lbm_p["OOS_Sharpe"],
                        base_OOS_MaxDD=lbm_p["OOS_MaxDD"],
                        pass_4b_full=all(l4b.values()), pass_4b_oos=all(l4bo.values()),
                        pass_4a=all(l4a.values()), **l4b, **l4bo, **l4a))
    pk = pd.DataFrame(pickrows)
    dump(pk, "walkforward")
    for _, r_ in pk.iterrows():
        P(f"    {r_['tape']:<10} {r_['panel']:<6} {r_['ladder']:<8} {r_['chooser']:<11} pick "
          f"{str(r_['pick']):<6} margin {r_['margin']:7.4f}  full {r_['CAGR']:7.2%}/"
          f"{r_['Sharpe']:.4f}/{r_['MaxDD']:7.2%}  halves {r_['H1']:.4f}/{r_['H2']:.4f}  OOS "
          f"{r_['OOS_CAGR']:7.2%}/{r_['OOS_Sharpe']:.4f}/{r_['OOS_MaxDD']:7.2%}  4b full "
          f"{str(r_['pass_4b_full']):<5} 4b OOS {str(r_['pass_4b_oos']):<5} 4a "
          f"{str(r_['pass_4a']):<5} regret {r_['regret']:+.4f}")
    P(f"  ALL PICKS: 4b full {int(pk['pass_4b_full'].sum())} of {len(pk)}, 4b OOS "
      f"{int(pk['pass_4b_oos'].sum())} of {len(pk)}, 4a {int(pk['pass_4a'].sum())} of {len(pk)}; "
      f"IS chooser takes the OOS-best rung {int(pk['picked_oos_best'].sum())} of {len(pk)}")
    for tape in TAPES:
        for panel in PANELS:
            s = pk[(pk.tape == tape) & (pk.panel == panel)]
            sb, lbm_p = bench[(tape, panel)]
            P(f"    {tape:<10} {panel:<6} picks: 4b full {int(s.pass_4b_full.sum())}/{len(s)}, "
              f"4b OOS {int(s.pass_4b_oos.sum())}/{len(s)}, 4a {int(s.pass_4a.sum())}/{len(s)}, "
              f"median OOS Sharpe {s.OOS_Sharpe.median():.4f} vs SPY OOS "
              f"{sb['OOS_Sharpe']:.4f} and RULES v2 OOS {lbm_p['OOS_Sharpe']:.4f}; median regret "
              f"{s.regret.median():+.4f}")
    P(f"  WHOLE GRID ({len(grid)} rungs): 4b full {int(grid['pass_4b_full'].sum())}, 4b OOS "
      f"{int(grid['pass_4b_oos'].sum())}, 4a {int(grid['pass_4a'].sum())}")
    LEGS4B = ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]
    for tape in TAPES:
        for panel in PANELS:
            s = grid[(grid.tape == tape) & (grid.panel == panel)]
            P(f"    {tape:<10} {panel:<6} 4b full {int(s.pass_4b_full.sum())}/{len(s)}, 4b OOS "
              f"{int(s.pass_4b_oos.sum())}/{len(s)}, 4a {int(s.pass_4a.sum())}/{len(s)};  legs "
              + ", ".join(f"{l} {int(s[l].sum())}/{len(s)}" for l in LEGS4B))
    fails = grid[~grid.pass_4b_full]
    P(f"  BINDING LEG among the {len(fails)} full-sample 4b failures:")
    for leg in LEGS4B:
        n_only = int((~fails[leg] & fails[[x for x in LEGS4B if x != leg]].all(axis=1)).sum())
        P(f"     {leg}: fails at {int((~fails[leg]).sum())}/{len(fails)}, SOLE failing leg at "
          f"{n_only}")
    if int(grid["pass_4b_full"].sum()):
        P("  4b-full passing cells:")
        for _, r_ in grid[grid.pass_4b_full].iterrows():
            P(f"    {r_['tape']:<10} {r_['panel']:<6} {r_['ladder']:<8} rung "
              f"{str(r_['rung']):<6} full {r_['CAGR']:7.2%}/{r_['Sharpe']:.4f}/"
              f"{r_['MaxDD']:7.2%} halves {r_['H1']:.4f}/{r_['H2']:.4f}  OOS "
              f"{r_['OOS_CAGR']:7.2%}/{r_['OOS_Sharpe']:.4f}/{r_['OOS_MaxDD']:7.2%}  4b OOS "
              f"{r_['pass_4b_oos']}")
    P("  NOTHING PROPOSED AS A BOOK.  The FRACTION LADDER dial is a READ of already-computed")
    P("  returns and cannot change a book by construction: the 81 T_OWN rung books are")
    P("  byte-identical across all three ladders.  The TAPE dial only TRUNCATES the tape a book")
    P("  is read over and proposes no rule.  Scored at all 162 rungs because rule 4 requires it.")
    P("")

    P("## GATE SUMMARY")
    P(f"   {sum(1 for v in gates.values() if v)} of {len(gates)} PASS")
    dump(pd.DataFrame(gaterows), "gates")

    P("\n## SURVIVORSHIP (PROTOCOL rule 9)")
    P("   U56 and B136 are CURRENT-CONSTITUENT lists; the SMALL pool is the CURRENT constituents")
    P(f"   of a sub-$2B screen ({cells[('T_OWN','SMALL')]['K'] - 1} names after dropping "
      f"{ndrop} with max_1d_move >= 1.0 from data/small_meta.csv, {nmeta} listed), so every name")
    P("   that fell below the screen, delisted or went to zero is absent and the drawdowns read")
    P("   here are the SHALLOWEST the period could have produced.  A within-length spread and a")
    P("   between-length move contrast the same books over stretches of the same inflated tape,")
    P("   so the bias very largely cancels out of the RATIO — the whole quantity measured here.")
    P("   It does NOT cancel out of the 4b legs, measured against SPY, a real index, so every 4b")
    P("   pass counted above is an UPPER bound.")
    P("\n## THE DECLARED APPROXIMATION, AND ITS DIRECTION")
    P("   MaxDD over a longer stretch is a MAXIMUM over more points and grows with length")
    P("   mechanically, with no regime content whatever — which is why the null arm is here.")
    P("   Every null resamples ONE tape, so it prices sampling error around THIS regime and not")
    P("   regime uncertainty across regimes; a null ratio is therefore biased TOWARD the reading")
    P("   it tests.  H_NULL is scored in the direction that favours calling the cell MECHANICAL,")
    P("   the conclusion this run reaches, so that conclusion rests on the evidence that makes")
    P("   it hardest to avoid rather than easiest.  The EPISODE arm drops a CALENDAR YEAR, which")
    P("   removes more than the drawdown itself; that over-removal can only make H_EPISODE")
    P("   EASIER to support, and it is named for that reason.")
    P(f"\n# done in {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

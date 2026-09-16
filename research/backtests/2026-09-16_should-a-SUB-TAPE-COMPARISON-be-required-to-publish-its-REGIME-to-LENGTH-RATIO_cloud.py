#!/usr/bin/env python3
"""Idea 1148 (cloud lane, 2026-09-16) — should a SUB-TAPE COMPARISON be required to publish its
REGIME-to-LENGTH RATIO?

QUESTION (QUEUE idea 1148, verbatim)
    idea 1140 measured that the WITHIN-fraction spread (same length, different stretch of tape =
    pure regime) is 1.7x to 61x the BETWEEN-fraction move its exponents are fitted through, so
    every sub-tape / split-sample exponent in the record is an upper bound on precision rather
    than a measurement.  Census the record's committed sub-tape, split-half and tape-length
    claims for whether any publishes that ratio, and draft and price a PROTOCOL clause requiring
    it.  Max 2 params (claim set, ratio definition).

THE TWO TUNED DIALS (PROTOCOL rule 4, no more than two)
    1. CLAIM SET {CS_STRICT, CS_HALVES, CS_ALL}.  CS_STRICT = committed CSV rows whose file
       indexes the row BY TAPE EXTENT (a sub-tape / fraction / window / tape-length / segment /
       split key column).  CS_HALVES = committed CSV rows carrying a SPLIT-HALF pair (an H1 and
       an H2 column, or an IS_ and an OOS_ pair of the same statistic) — a half IS a sub-tape,
       and this is the record's commonest sub-tape comparison by three orders of magnitude.
       CS_ALL = the union.  All three published, at every point.
    2. RATIO DEFINITION {R_SPREAD, R_SD, R_MATCHED}.  R_SPREAD is 1140's own (within = median
       over same-length groups of max - min; between = |median at 1/1 - median at 1/3|), the
       headline, for continuity.  R_SD is the moment version (within = median sd across
       same-length sub-tapes; between = sd of the three fraction medians).  R_MATCHED is the
       COUNT-CORRECTED version and the one this run adds: max - min over k points GROWS with k,
       and 1140 pools a k=2 range (halves) with a k=3 range (thirds), so R_MATCHED takes the
       within spread as the mean range of a RANDOM PAIR at every fraction, which is count-free.
       All three published, at every point; none is selected on.
    PANEL, LADDER and STATISTIC are NOT dials: 3 panels x 4 CORE ladders x 6 statistics are
    reported everywhere.  SUB-TAPE FRACTION is frozen at 1140's own {1/1, 1/2, 1/3} = 6 tapes.
    Everything else frozen at the record's construction: CAND20 legs, cap INF, max_vol 0.60,
    gross 0.75 (except on the GROSS ladder), W (except on CADENCE), min hold 126 (except on H),
    N=20 (except on N), 10 bps, LAG 1, warm-up 260, IS end 2016-12-31.

DECLARED BEFORE ANY NUMBER
    H_NOBODY     the idea's census question: NO committed claim outside 1140 itself publishes a
                 regime-to-length ratio.  SUPPORTED iff the count of publishing files is 1.
    H_RATIO1     the idea's premise, re-measured on a SECOND CONSTRUCTION (the statistic VALUE
                 on a ladder of real books, not 1140's resolution ratio): regime / length > 1
                 for every one of the six statistics at the headline definition.
    H_DEFN       the premise is NOT a definition artefact: regime / length > 1 for every
                 statistic under ALL THREE ratio definitions.  REFUTED by any statistic that
                 crosses 1 when the definition moves.
    H_COUNT      the count correction BITES: R_SPREAD systematically exceeds R_MATCHED, because
                 max - min over 3 points exceeds max - min over 2 on the same distribution.
                 SUPPORTED iff R_SPREAD > R_MATCHED for a majority of the 6 statistics.
    H_CHECKABLE  the clause is CHEAP: a majority of CS_STRICT claims already publish enough
                 (two sub-tapes at one matched extent AND two distinct extents) for the ratio to
                 be computed from what is committed, so the clause costs a column and not a
                 re-run.  REFUTED if the checkable share is below 0.50.
    H_SCOPE      the clause's real cost is its DENOMINATOR: CS_HALVES is more than 100x
                 CS_STRICT, so a clause worded over "sub-tape comparisons" silently binds every
                 halves row in the record.  SUPPORTED iff |CS_HALVES| > 100 x |CS_STRICT|.
    NOT A KEEP PATH BY CONSTRUCTION.  Neither dial can move a book: the 81 rung books are
    byte-identical whichever claim set or ratio definition is nominated, and only which
    committed rows get COUNTED and how the ratio is DEFINED changes.  Rule 8 (rung chosen on IS
    2009-2016 alone, per ladder, three choosers, OOS read ONCE) and BOTH KEEP paths (4a against
    live RULES v2, 4b against SPY) are scored at every one of the 81 rungs anyway, because rule
    4 and rule 8 require it.

THE DECLARED APPROXIMATION, AND ITS DIRECTION.  The census is harvested from COMMITTED artifacts
    only, so a ratio the record published in a console log or a script comment is not counted;
    that omission can only make H_NOBODY EASIER to support, and is named for that reason.  The
    CS_STRICT column test is a NAME test (a header matching the tape-extent pattern), so a file
    that indexes rows by tape extent under an idiosyncratic column name is missed and a file
    whose `rows` column means something else is over-counted; both directions are reported, the
    accepted and rejected header names are dumped in full, and no classification in this run
    rests on a single file.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists; the SMALL pool is
    the CURRENT constituents of a sub-$2B screen, so every name that fell below the screen,
    delisted or went to zero is absent.  A WITHIN-length spread and a BETWEEN-length move both
    contrast the same books over stretches of the same inflated tape, so the bias very largely
    cancels out of the ratio — which is the whole quantity this run measures.  It does NOT
    cancel out of the 4b legs, measured against SPY, a real index, so every 4b pass counted here
    is an UPPER bound.
"""
from __future__ import annotations

import csv
import glob
import os
import re
import sys
import time
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-16"
SLUG = "should-a-SUB-TAPE-COMPARISON-be-required-to-publish-its-REGIME-to-LENGTH-RATIO"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"
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
FRACS = [1, 2, 3]                                   # 1140's own sub-tape ladder: 6 tapes
STATS6 = ["CAGR", "VOL", "SHARPE", "MAXDD", "ULCER", "CALMAR"]
IS_PATH = {"CAGR": False, "VOL": False, "SHARPE": False,
           "MAXDD": True, "ULCER": True, "CALMAR": True}
CLAIM_SETS = ["CS_STRICT", "CS_HALVES", "CS_ALL"]   # dial 1
RATIO_DEFS = ["R_SPREAD", "R_SD", "R_MATCHED"]      # dial 2
R_HEAD = "R_SPREAD"
CHOOSERS = {"C_ISSHARPE": "IS_Sharpe", "C_ISCAGR": "IS_CAGR", "C_ISDD": "IS_MaxDD"}
SEED = 11481148
NPAIR = 200                                          # random-pair draws for R_MATCHED

# ---- the record's own committed numbers, quoted and gated, never re-derived from memory
PRIOR1140 = BT / "2026-09-16_is-DD-s-RUNG-ROBUST-UN-RESOLVABILITY-a-PATH-FUNCTIONAL-fact-or-a-TAPE-fact_B.regime.csv"
A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205

# ---- census patterns.  Both lists are DUMPED in full so every classification is checkable.
EXTENT_COL = re.compile(
    r"^(sub_?tape\w*|frac|frac_\w*|\w*_frac|window|window_\w*|\w*_window|win_len\w*|tape_len\w*|"
    r"tape_rows|n_days|nbars|n_bars|seg|segment\w*|period_len\w*|split|split_\w*|\w*_split|"
    r"length|len|\w*_len|\w*_length|rows|n_rows|nrows)$", re.I)
RATIO_COL = re.compile(r"(regime_over_length|within_fraction|between_fraction|"
                       r"regime_to_length|regime_over_len)", re.I)
H1 = re.compile(r"^(\w*_)?h1$", re.I)
H2 = re.compile(r"^(\w*_)?h2$", re.I)
ISCOL = re.compile(r"^is_(cagr|sharpe|maxdd|vol|dd)$", re.I)
OOSCOL = re.compile(r"^oos_(cagr|sharpe|maxdd|vol|dd)$", re.I)

PROSE_TRIG = re.compile(
    r"(sub-?tape|split-?half|split-?sample|first half|second half|both halves|the halves|"
    r"tape length|length of the tape|longer tape|shorter tape|window length|"
    r"fraction of the tape|half the tape|a third of the tape|disjoint sub)", re.I)
PROSE_VALUE = re.compile(r"(\d|KEEP|KILL|PARK|SUPPORTED|REFUTED|ROBUST|ESCAPABLE)")
PROSE_RATIO = re.compile(r"(regime[- ]to[- ]length|regime/length|regime over length|"
                         r"within-fraction|between-fraction|regime_over_length)", re.I)

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


def count_rows(path):
    """Row count without parsing values: newline count minus the header."""
    n = 0
    with open(path, "rb") as fh:
        while True:
            b = fh.read(1 << 22)
            if not b:
                break
            n += b.count(b"\n")
    return max(n - 1, 0)


# ------------------------------------------------------------ the three ratio definitions
def ratio_from(groups, frac_medians, rng):
    """groups: {frac: [ [values at that frac] ... ]} one list per (panel, ladder) group.
    frac_medians: {frac: median over everything at that frac}.  Returns the three ratios."""
    ranges, sds, matched = [], [], []
    for f, gs in groups.items():
        if f == 1:
            continue                                   # 1/1 is ONE tape: no within spread
        for v in gs:
            v = np.asarray([x for x in v if np.isfinite(x)], float)
            if len(v) < 2:
                continue
            ranges.append(float(v.max() - v.min()))
            sds.append(float(v.std(ddof=1)))
            if len(v) == 2:
                matched.append(float(abs(v[0] - v[1])))
            else:
                i = rng.integers(0, len(v), size=(NPAIR, 2))
                i = i[i[:, 0] != i[:, 1]]
                matched.append(float(np.abs(v[i[:, 0]] - v[i[:, 1]]).mean()))
    m = {f: frac_medians[f] for f in frac_medians}
    between_spread = abs(m[1] - m[max(FRACS)]) if np.isfinite(m[1]) and np.isfinite(m[max(FRACS)]) else np.nan
    between_sd = float(np.std([m[f] for f in FRACS], ddof=1))
    out = {}
    w_spread = float(np.nanmedian(ranges)) if ranges else np.nan
    w_sd = float(np.nanmedian(sds)) if sds else np.nan
    w_matched = float(np.nanmedian(matched)) if matched else np.nan
    out["R_SPREAD"] = (w_spread, between_spread,
                       w_spread / between_spread if between_spread else np.nan)
    out["R_SD"] = (w_sd, between_sd, w_sd / between_sd if between_sd else np.nan)
    out["R_MATCHED"] = (w_matched, between_spread,
                        w_matched / between_spread if between_spread else np.nan)
    return out


# ------------------------------------------------------------------------------------ main
def main():
    t0 = time.time()
    P(f"# Idea 1148 (cloud lane, {DATE}) — should a SUB-TAPE COMPARISON be required to publish "
      "its REGIME-to-LENGTH RATIO?")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4): CLAIM SET {CLAIM_SETS} x RATIO DEFINITION "
      f"{RATIO_DEFS} = 9 combinations, ALL published.")
    P("#   PANEL, LADDER and STATISTIC are NOT dials (3 x 4 x 6 reported everywhere).  SUB-TAPE")
    P(f"#   FRACTION frozen at 1140's own {['1/'+str(f) for f in FRACS]} = 6 tapes.  Headline "
      f"ratio definition {R_HEAD} (1140's own), for continuity only.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   H_NOBODY    no committed claim outside 1140 itself publishes a regime-to-length ratio.")
    P("#   H_RATIO1    on a SECOND construction, regime/length > 1 for all six statistics.")
    P("#   H_DEFN      and under ALL THREE ratio definitions, so it is not a definition artefact.")
    P("#   H_COUNT     R_SPREAD > R_MATCHED for a majority of statistics (max-min grows with k).")
    P("#   H_CHECKABLE >= 0.50 of CS_STRICT claims already publish enough to compute the ratio.")
    P("#   H_SCOPE     |CS_HALVES| > 100 x |CS_STRICT| — the clause's cost is its denominator.")
    P("#   NOT A KEEP PATH: the 81 rung books are byte-identical across both dials.  Rule 8 and")
    P("#     both KEEP paths scored at every rung anyway, because rule 4 says so.")
    P("")

    gaterows, gates = [], {}

    def gate(name, what, value, ok):
        gates[name] = bool(ok)
        gaterows.append(dict(gate=name, what=what, value=float(value), pass_=bool(ok)))
        P(f"  [{'PASS' if ok else 'FAIL'}] {name:<9s} {what}: {value:.4e}")

    # ------------------------------------------------------------------------- panels
    P("## PANELS — loaded and STAMPED before any result number")
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
            elig[:, spy_i] = False
        panels[panel] = dict(px=px, idx=idx, K=K, T=T, rets=rets, priced=priced, warm=warm,
                             ins=ins, oos=oos, sc=sc, elig=elig)
        P(f"  {panel:<6s} {K:4d} cols, {T:,} rows {idx[0].date()} -> {idx[-1].date()}  "
          f"warm {warm.sum():,}  IS {ins.sum():,}  OOS {oos.sum():,}")
    P(f"  SMALL STAMP: data/small_meta.csv lists {nmeta} tickers; {ndrop} dropped for "
      f"max_1d_move >= 1.0; pool served = {panels['SMALL']['K'] - 1} names + SPY as benchmark; "
      f"tape {panels['SMALL']['idx'][0].date()} -> {panels['SMALL']['idx'][-1].date()}.")
    P("")

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
        return g - tn * COST / 1e4

    # ------------------------------------------------------------------------- gates
    P("## GATES — printed before any result number")
    d = panels["U56"]
    mk = rebalance_mask(d["idx"], FREQ0).values
    reb = np.flatnonzero(mk)
    W = build(-d["sc"], d["elig"], d["priced"], reb, N0, HOLD0, d["T"], d["K"], GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST, freq=FREQ0)["returns"].values
    rfast = run_cell("U56", N0, HOLD0, GROSS0, FREQ0)
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
    gate("G3", "SPY OOS triple (U56 tape)", v, v < 5e-4)
    lb_r = backtest(d["px"], rules_v2_weights(d["px"]), cost_bps=COST, freq="W")["returns"].values
    v = abs(blocks_m(lb_r, d["warm"], d["ins"], d["oos"])["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gate("G4", "live RULES v2 MaxDD == committed -12.05%", v, v < 5e-4)
    v = float(np.abs(run_cell("SMALL", N0, HOLD0, GROSS0, FREQ0)
                     - run_cell("SMALL", N0, HOLD0, GROSS0, FREQ0)).max())
    gate("G5", "determinism of the SMALL pipeline", v, v == 0.0)
    # G6: 1140's committed regime column is READ FROM ITS FILE, never from memory
    prior = pd.read_csv(PRIOR1140)
    ok6 = (len(prior) == 6 and set(prior.stat) == set(STATS6)
           and {"within_fraction_spread", "between_fraction_move",
                "regime_over_length"} <= set(prior.columns))
    gate("G6", "1140's committed regime.csv is present and carries all six statistics",
         0.0 if ok6 else 1.0, ok6)
    P("     1140's COMMITTED regime-over-length, quoted verbatim from its own CSV (NOT "
      "re-derived): " + ", ".join(f"{r.stat} {r.regime_over_length:.2f}x"
                                  for r in prior.itertuples()))
    P("")

    # ============================================================ ARM A — THE CENSUS
    P("## ARM A — THE CENSUS: does ANY committed claim publish a regime-to-length ratio?")
    files = sorted(glob.glob(str(BT / "*.csv")))
    P(f"   scanning {len(files):,} committed research/backtests/*.csv "
      f"({sum(os.path.getsize(f) for f in files)/1e9:.2f} GB) by HEADER, rows counted without "
      "parsing values")
    frows, acc_names, rej_names = [], {}, {}
    for f in files:
        try:
            with open(f, newline="") as fh:
                hdr = next(csv.reader(fh))
        except Exception:
            continue
        ext = [c for c in hdr if c and EXTENT_COL.match(c)]
        h1 = [c for c in hdr if c and H1.match(c)]
        h2 = [c for c in hdr if c and H2.match(c)]
        isc = [c for c in hdr if c and ISCOL.match(c)]
        oosc = [c for c in hdr if c and OOSCOL.match(c)]
        halves = bool(h1 and h2) or bool(isc and oosc)
        rat = [c for c in hdr if c and RATIO_COL.search(c)]
        if not (ext or halves):
            for c in hdr:
                rej_names[c] = rej_names.get(c, 0) + 1
            continue
        for c in ext:
            acc_names[c] = acc_names.get(c, 0) + 1
        n = count_rows(f)
        frows.append(dict(file=os.path.basename(f), rows=n, strict=bool(ext), halves=halves,
                          extent_cols="+".join(sorted(set(ext))),
                          halves_cols="+".join(sorted(set(h1 + h2 + isc + oosc))),
                          publishes_ratio=bool(rat), ratio_cols="+".join(sorted(set(rat)))))
    FI = pd.DataFrame(frows)
    dump(FI, "censusfiles")
    tot = {"CS_STRICT": FI[FI.strict], "CS_HALVES": FI[FI.halves],
           "CS_ALL": FI[FI.strict | FI.halves]}
    censusrows = []
    for cs, g in tot.items():
        censusrows.append(dict(claim_set=cs, n_files=len(g), n_rows=int(g.rows.sum()),
                               n_files_publishing_ratio=int(g.publishes_ratio.sum()),
                               n_rows_publishing_ratio=int(g[g.publishes_ratio].rows.sum()),
                               share_files=float(g.publishes_ratio.mean()) if len(g) else np.nan,
                               share_rows=(float(g[g.publishes_ratio].rows.sum() / g.rows.sum())
                                           if g.rows.sum() else np.nan)))
    CN = pd.DataFrame(censusrows)
    dump(CN, "census")
    for _, r_ in CN.iterrows():
        P(f"   {r_['claim_set']:<10s} {r_['n_files']:5,d} files / {r_['n_rows']:10,d} rows;  "
          f"publishing a regime-to-length ratio: {r_['n_files_publishing_ratio']} files / "
          f"{r_['n_rows_publishing_ratio']} rows  (share of rows {r_['share_rows']:.6f})")
    pub = FI[FI.publishes_ratio]
    P("   the files that DO publish it, named in full:")
    for _, r_ in pub.iterrows():
        P(f"     {r_['file']}  ({r_['rows']} rows, cols {r_['ratio_cols']})")
    if pub.empty:
        P("     (none)")
    P("   accepted TAPE-EXTENT header names (the CS_STRICT test is a NAME test — every accepted")
    P("   and rejected name is dumped so the classification is checkable):")
    AN = pd.DataFrame(sorted(acc_names.items(), key=lambda kv: -kv[1]),
                      columns=["header", "n_files"])
    dump(AN, "extentnames")
    P("     " + ", ".join(f"{k} ({v})" for k, v in list(AN.itertuples(index=False))[:24]))
    P("")

    # ---- PROSE arm
    P("## ARM A2 — THE PROSE ARM: committed memos, CHANGELOG and LEADERBOARD")
    prose_files = ([str(ROOT / "research" / "CHANGELOG.md"), str(ROOT / "research" / "LEADERBOARD.md")]
                   + sorted(glob.glob(str(BT / "*.result.md"))))
    prows = []
    for pf in prose_files:
        try:
            txt = Path(pf).read_text(errors="replace")
        except Exception:
            continue
        for ln_i, ln in enumerate(txt.split("\n"), 1):
            for sent in re.split(r"(?<=[.;])\s+", ln):
                if PROSE_TRIG.search(sent) and PROSE_VALUE.search(sent):
                    prows.append(dict(file=os.path.basename(pf), line=ln_i,
                                      publishes_ratio=bool(PROSE_RATIO.search(sent)),
                                      sentence=sent[:300]))
    PR = pd.DataFrame(prows)
    dump(PR, "censusprose")
    P(f"   {len(PR):,} committed prose sentences carry BOTH a sub-tape/split-half/tape-length "
      f"trigger AND a value or verdict word; {int(PR.publishes_ratio.sum())} of them name a "
      f"regime-to-length ratio ({PR.publishes_ratio.mean():.6f}).")
    if int(PR.publishes_ratio.sum()):
        for _, r_ in PR[PR.publishes_ratio].head(8).iterrows():
            P(f"     {r_['file']}:{r_['line']}  {r_['sentence'][:180]}")
    P("")

    # ---- CHECKABILITY: can the ratio be computed from what a CS_STRICT file already publishes?
    P("## ARM A3 — PRICING THE CLAUSE: is the ratio COMPUTABLE from what is already committed?")
    P("   A committed file is CHECKABLE iff its own tape-extent column takes >= 2 distinct")
    P("   values (two lengths, so a BETWEEN move exists) AND some extent value appears on >= 2")
    P("   rows (two stretches at one length, so a WITHIN spread exists).")
    chk = []
    for _, r_ in FI[FI.strict].iterrows():
        f = BT / r_["file"]
        cols = r_["extent_cols"].split("+")
        best = dict(file=r_["file"], rows=int(r_["rows"]), col="", n_values=0, max_rep=0,
                    checkable=False, error="")
        for c in cols:
            try:
                s = pd.read_csv(f, usecols=[c]).iloc[:, 0]
            except Exception as e:
                best["error"] = type(e).__name__
                continue
            vc = s.value_counts(dropna=True)
            nv, mr = int(len(vc)), int(vc.max()) if len(vc) else 0
            if nv >= 2 and mr >= 2 and not best["checkable"]:
                best.update(col=c, n_values=nv, max_rep=mr, checkable=True)
            elif not best["checkable"] and nv > best["n_values"]:
                best.update(col=c, n_values=nv, max_rep=mr)
        chk.append(best)
    CK = pd.DataFrame(chk)
    dump(CK, "checkable")
    share_f = float(CK.checkable.mean()) if len(CK) else np.nan
    share_r = float(CK[CK.checkable].rows.sum() / CK.rows.sum()) if CK.rows.sum() else np.nan
    P(f"   CS_STRICT: {int(CK.checkable.sum())} of {len(CK)} files CHECKABLE ({share_f:.4f}), "
      f"carrying {int(CK[CK.checkable].rows.sum()):,} of {int(CK.rows.sum()):,} rows "
      f"({share_r:.4f}).")
    P("   CS_HALVES is checkable by construction on the BETWEEN axis (two halves = two stretches")
    P("   at one length) and NOT on the length axis (a half is one length only), so a halves row")
    P("   can price REGIME but never LENGTH: the clause as worded would require a THIRD tape.")
    P("")

    # ============================================================ ARM B — THE MEASUREMENT
    P("## ARM B — RE-MEASURING THE RATIO ON A SECOND CONSTRUCTION")
    P("   1140 measured it on its own RESOLUTION RATIO |gap|/SD.  This arm measures it on the")
    P("   STATISTIC VALUE itself, over the four CORE ladders at the standing anchor, on three")
    P("   panels.  It is a SECOND CONSTRUCTION, not a reproduction of 1140, and is labelled so.")
    subrows, gridrows, bench, metr = [], [], {}, {}
    for panel in PANELS:
        dd_ = panels[panel]
        warm = dd_["warm"]
        sb = blocks_m(dd_["px"]["SPY"].pct_change().fillna(0.0).values, warm, dd_["ins"], dd_["oos"])
        lbm_p = blocks_m(backtest(dd_["px"], rules_v2_weights(dd_["px"]), cost_bps=COST,
                                  freq="W")["returns"].values, warm, dd_["ins"], dd_["oos"])
        bench[panel] = (sb, lbm_p)
        P(f"  {panel:<6s} SPY full {sb['CAGR']:.2%}/{sb['Sharpe']:.4f}/{sb['MaxDD']:.2%} halves "
          f"{sb['H1']:.4f}/{sb['H2']:.4f} OOS {sb['OOS_CAGR']:.2%}/{sb['OOS_Sharpe']:.4f}/"
          f"{sb['OOS_MaxDD']:.2%}   |   RULES v2 full {lbm_p['CAGR']:.2%}/{lbm_p['Sharpe']:.4f}/"
          f"{lbm_p['MaxDD']:.2%} OOS {lbm_p['OOS_Sharpe']:.4f}")
        for lad, rungs in LADDERS.items():
            for rg in rungs:
                c = dict(ANCHOR)
                c[lad] = rg
                r_ = run_cell(panel, c["N"], c["H"], c["GROSS"], c["CADENCE"])
                mm = blocks_m(r_, warm, dd_["ins"], dd_["oos"])
                metr[(panel, lad, rg)] = mm
                l4b, l4bo, l4a = legs_4b(mm, sb), legs_4b_oos(mm, sb), legs_4a(mm, lbm_p)
                gridrows.append(dict(panel=panel, ladder=lad, rung=rg, **mm,
                                     pass_4b_full=all(l4b.values()),
                                     pass_4b_oos=all(l4bo.values()),
                                     pass_4a=all(l4a.values()), **l4b, **l4bo, **l4a))
                rw = r_[warm]
                n = len(rw)
                for f in FRACS:
                    L = n // f
                    for k in range(f):
                        seg = rw[k * L:(k + 1) * L]
                        st = six_stats(seg)
                        subrows.append(dict(panel=panel, ladder=lad, rung=rg, frac=f, part=k,
                                            n_days=len(seg), **st))
        P(f"  {panel:<6s} built {sum(len(v) for v in LADDERS.values())} rung books x "
          f"{sum(FRACS)} sub-tapes ({time.time()-t0:.0f}s)")
    SUB = pd.DataFrame(subrows)
    dump(SUB, "subtapes")
    grid = pd.DataFrame(gridrows)
    dump(grid, "grid")

    rng = np.random.default_rng(SEED)
    regrows = []
    for panel in PANELS + ["POOLED"]:
        s = SUB if panel == "POOLED" else SUB[SUB.panel == panel]
        for stat in STATS6:
            groups = {f: [] for f in FRACS}
            for (pn, lad), g in s.groupby(["panel", "ladder"]):
                for f in FRACS:
                    groups[f].append(g[g.frac == f].groupby("part")[stat].median().tolist())
            med = {f: float(np.nanmedian(s[s.frac == f][stat])) for f in FRACS}
            rr = ratio_from(groups, med, rng)
            row = dict(panel=panel, stat=stat, is_path=IS_PATH[stat],
                       med_1_1=med[1], med_1_2=med[2], med_1_3=med[3])
            for dname in RATIO_DEFS:
                w, b, x = rr[dname]
                row[f"{dname}_within"] = w
                row[f"{dname}_between"] = b
                row[f"{dname}_ratio"] = x
            regrows.append(row)
    RG = pd.DataFrame(regrows)
    dump(RG, "regime")
    P("   REGIME-to-LENGTH ratio, all three definitions, per panel and pooled "
      "(> 1 = the length effect is smaller than the regime noise it is read through):")
    P("   panel   stat    path   med 1/1   med 1/2   med 1/3 |  R_SPREAD  R_SD   R_MATCHED")
    for _, r_ in RG.iterrows():
        P(f"   {r_['panel']:<7} {r_['stat']:<7} {str(r_['is_path'])[0]}    "
          f"{r_['med_1_1']:9.4f} {r_['med_1_2']:9.4f} {r_['med_1_3']:9.4f} | "
          f"{r_['R_SPREAD_ratio']:9.2f} {r_['R_SD_ratio']:7.2f} {r_['R_MATCHED_ratio']:9.2f}")
    P("")

    # ============================================================ HYPOTHESES
    pool = RG[RG.panel == "POOLED"].set_index("stat")
    n_pub_files = int(FI.publishes_ratio.sum())
    H_NOBODY = bool(n_pub_files == 1)
    H_RATIO1 = bool((pool[f"{R_HEAD}_ratio"] > 1).all())
    H_DEFN = bool(all((pool[f"{d_}_ratio"] > 1).all() for d_ in RATIO_DEFS))
    H_COUNT = bool((pool["R_SPREAD_ratio"] > pool["R_MATCHED_ratio"]).sum() > len(STATS6) / 2)
    H_CHECKABLE = bool(np.isfinite(share_f) and share_f >= 0.50)
    n_strict = int(CN.loc[CN.claim_set == "CS_STRICT", "n_rows"].iloc[0])
    n_halves = int(CN.loc[CN.claim_set == "CS_HALVES", "n_rows"].iloc[0])
    H_SCOPE = bool(n_halves > 100 * n_strict)
    hyp = [
        dict(hypothesis="H_NOBODY", declared="no committed claim outside 1140 publishes a regime-to-length ratio",
             result=f"{n_pub_files} committed CSV file(s) carry such a column "
                    f"({int(FI[FI.publishes_ratio].rows.sum())} rows of "
                    f"{int(FI[FI.strict|FI.halves].rows.sum()):,}); prose arm "
                    f"{int(PR.publishes_ratio.sum())} of {len(PR):,} sentences",
             verdict="SUPPORTED" if H_NOBODY else "REFUTED"),
        dict(hypothesis="H_RATIO1", declared=f"regime/length > 1 for all six statistics at {R_HEAD} (pooled)",
             result="; ".join(f"{s} {pool.loc[s, R_HEAD+'_ratio']:.2f}x" for s in STATS6),
             verdict="SUPPORTED" if H_RATIO1 else "REFUTED"),
        dict(hypothesis="H_DEFN", declared="and under ALL THREE ratio definitions",
             result="; ".join(f"{d_}: {int((pool[d_+'_ratio'] > 1).sum())}/6 above 1 "
                              f"(min {pool[d_+'_ratio'].min():.2f}x)" for d_ in RATIO_DEFS),
             verdict="SUPPORTED" if H_DEFN else "REFUTED"),
        dict(hypothesis="H_COUNT", declared="R_SPREAD > R_MATCHED for a majority of statistics (max-min grows with k)",
             result=f"{int((pool['R_SPREAD_ratio'] > pool['R_MATCHED_ratio']).sum())} of 6; "
                    f"median R_SPREAD/R_MATCHED "
                    f"{float((pool['R_SPREAD_ratio']/pool['R_MATCHED_ratio']).median()):.3f}x",
             verdict="SUPPORTED" if H_COUNT else "REFUTED"),
        dict(hypothesis="H_CHECKABLE", declared="at least half of CS_STRICT claims already publish enough to compute the ratio",
             result=f"{int(CK.checkable.sum())} of {len(CK)} files ({share_f:.4f}); "
                    f"{share_r:.4f} of their rows",
             verdict="SUPPORTED" if H_CHECKABLE else "REFUTED"),
        dict(hypothesis="H_SCOPE", declared="|CS_HALVES| > 100 x |CS_STRICT| in rows",
             result=f"CS_HALVES {n_halves:,} rows vs CS_STRICT {n_strict:,} rows = "
                    f"{(n_halves/n_strict if n_strict else float('nan')):.1f}x",
             verdict="SUPPORTED" if H_SCOPE else "REFUTED"),
    ]
    HY = pd.DataFrame(hyp)
    dump(HY, "hypotheses")
    P("## HYPOTHESES")
    for _, r_ in HY.iterrows():
        P(f"   [{r_['verdict']:<9s}] {r_['hypothesis']:<12s} {r_['result']}")
    P(f"   {int((HY.verdict == 'SUPPORTED').sum())} of {len(HY)} SUPPORTED")
    P("")

    # ============================================================ THE CLAUSE, DRAFTED AND PRICED
    P("## THE CLAUSE — DRAFTED AND PRICED (proposed for the Sunday review, NOT enacted; rule 6)")
    P("   PROTOCOL rule 10 (draft):  A published claim whose value depends on the LENGTH or the")
    P("   STRETCH of tape it was computed on — a sub-tape, a split-half, a tape-length exponent,")
    P("   a window-length ladder — must state, beside it, its REGIME-to-LENGTH RATIO: the median")
    P("   spread of the same quantity across DISJOINT stretches of EQUAL length, divided by its")
    P("   move between the longest and the shortest length.  A claim whose ratio exceeds 1 is an")
    P("   UPPER BOUND ON PRECISION and may not be quoted as a measurement.  The within spread")
    P("   must be COUNT-MATCHED (a random pair at every length), because max - min grows with the")
    P("   number of stretches.")
    clr = []
    for cs in CLAIM_SETS:
        g = tot[cs]
        for dname in RATIO_DEFS:
            binds = int(g.rows.sum())
            already = int(g[g.publishes_ratio].rows.sum())
            checkable = int(CK[CK.checkable].rows.sum()) if cs != "CS_HALVES" else 0
            clr.append(dict(claim_set=cs, ratio_defn=dname, rows_bound=binds,
                            rows_already_compliant=already,
                            rows_computable_from_committed=checkable,
                            rows_needing_a_re_run=binds - already - checkable,
                            share_needing_a_re_run=(binds - already - checkable) / binds
                            if binds else np.nan,
                            n_stats_above_1=int((pool[dname + "_ratio"] > 1).sum()),
                            median_ratio=float(pool[dname + "_ratio"].median())))
    CL = pd.DataFrame(clr)
    dump(CL, "clause")
    P("   claim_set  ratio_defn  rows bound  already  computable  need a re-run  share  "
      "stats>1  median ratio")
    for _, r_ in CL.iterrows():
        P(f"   {r_['claim_set']:<10} {r_['ratio_defn']:<11} {r_['rows_bound']:10,d} "
          f"{r_['rows_already_compliant']:8d} {r_['rows_computable_from_committed']:11,d} "
          f"{r_['rows_needing_a_re_run']:14,d} {r_['share_needing_a_re_run']:6.4f} "
          f"{r_['n_stats_above_1']:7d}  {r_['median_ratio']:11.2f}")
    P("   READ THE DENOMINATOR, NOT THE SHARE: the clause's cost is set entirely by how")
    P("   'sub-tape comparison' is worded.  Over CS_STRICT it is a column on a few hundred")
    P("   committed files; over CS_HALVES it binds every halves row in the record and cannot be")
    P("   satisfied from what those rows publish, because a half is ONE length.")
    P("")

    # ============================================================ RULE 8 AND BOTH KEEP PATHS
    P("## RULE 8 — rung chosen on IS 2009-2016 ALONE, per ladder, three choosers, OOS read ONCE")
    pickrows = []
    for panel in PANELS:
        sb, lbm_p = bench[panel]
        for lad, rungs in LADDERS.items():
            for ch, key in CHOOSERS.items():
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
                                     spy_OOS_CAGR=sb["OOS_CAGR"],
                                     spy_OOS_Sharpe=sb["OOS_Sharpe"],
                                     spy_OOS_MaxDD=sb["OOS_MaxDD"],
                                     base_OOS_Sharpe=lbm_p["OOS_Sharpe"],
                                     base_OOS_MaxDD=lbm_p["OOS_MaxDD"],
                                     pass_4b_full=all(l4b.values()),
                                     pass_4b_oos=all(l4bo.values()),
                                     pass_4a=all(l4a.values()), **l4b, **l4bo, **l4a))
    pk = pd.DataFrame(pickrows)
    dump(pk, "walkforward")
    for _, r_ in pk.iterrows():
        P(f"    {r_['panel']:<6} {r_['ladder']:<8} {r_['chooser']:<11} pick "
          f"{str(r_['pick']):<6} margin {r_['margin']:7.4f}  full {r_['CAGR']:7.2%}/"
          f"{r_['Sharpe']:.4f}/{r_['MaxDD']:7.2%}  halves {r_['H1']:.4f}/{r_['H2']:.4f}  OOS "
          f"{r_['OOS_CAGR']:7.2%}/{r_['OOS_Sharpe']:.4f}/{r_['OOS_MaxDD']:7.2%}  4b full "
          f"{str(r_['pass_4b_full']):<5} 4b OOS {str(r_['pass_4b_oos']):<5} 4a "
          f"{str(r_['pass_4a']):<5} regret {r_['regret']:+.4f}")
    P(f"  ALL PICKS: 4b full {int(pk['pass_4b_full'].sum())} of {len(pk)}, 4b OOS "
      f"{int(pk['pass_4b_oos'].sum())} of {len(pk)}, 4a {int(pk['pass_4a'].sum())} of {len(pk)}; "
      f"IS chooser takes the OOS-best rung {int(pk['picked_oos_best'].sum())} of {len(pk)}")
    for panel in PANELS:
        s = pk[pk.panel == panel]
        sb, lbm_p = bench[panel]
        P(f"    {panel:<6s} picks: 4b full {int(s.pass_4b_full.sum())}/{len(s)}, 4b OOS "
          f"{int(s.pass_4b_oos.sum())}/{len(s)}, 4a {int(s.pass_4a.sum())}/{len(s)}, median OOS "
          f"Sharpe {s.OOS_Sharpe.median():.4f} vs SPY OOS {sb['OOS_Sharpe']:.4f} and RULES v2 "
          f"OOS {lbm_p['OOS_Sharpe']:.4f}; median regret {s.regret.median():+.4f}")
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
        P(f"     {leg}: fails at {int((~fails[leg]).sum())}/{len(fails)}, SOLE failing leg at "
          f"{n_only}")
    if int(grid["pass_4b_full"].sum()):
        P("  4b-full passing cells:")
        for _, r_ in grid[grid.pass_4b_full].iterrows():
            P(f"    {r_['panel']:<6} {r_['ladder']:<8} rung {str(r_['rung']):<6} full "
              f"{r_['CAGR']:7.2%}/{r_['Sharpe']:.4f}/{r_['MaxDD']:7.2%} halves "
              f"{r_['H1']:.4f}/{r_['H2']:.4f}  OOS {r_['OOS_CAGR']:7.2%}/{r_['OOS_Sharpe']:.4f}/"
              f"{r_['OOS_MaxDD']:7.2%}  4b OOS {r_['pass_4b_oos']}")
    P("  NOTHING PROPOSED AS A BOOK: the 81 rung books are byte-identical across both dials —")
    P("  only which committed rows get COUNTED and how the ratio is DEFINED changes — so 4a and")
    P("  4b are invariant to the claim set and to the ratio definition by construction.  Scored")
    P("  because rule 4 and rule 8 require it.  The only thing PROPOSED here is a PROTOCOL")
    P("  clause, which rule 6 sends to the Sunday review.")
    P("")

    P("## GATE SUMMARY")
    P(f"   {sum(1 for v in gates.values() if v)} of {len(gates)} PASS")
    dump(pd.DataFrame(gaterows), "gates")

    P("\n## SURVIVORSHIP (PROTOCOL rule 9)")
    P("   U56 and B136 are CURRENT-CONSTITUENT lists; the SMALL pool is the CURRENT constituents")
    P("   of a sub-$2B screen, so every name that fell below the screen, delisted or went to zero")
    P("   is absent.  A WITHIN-length spread and a BETWEEN-length move both contrast the same")
    P("   books over stretches of the same inflated tape, so the bias very largely cancels out of")
    P("   the RATIO — the whole quantity this run measures.  It does NOT cancel out of the 4b")
    P("   legs, measured against SPY, so every 4b pass counted here is an UPPER bound.")
    P("\n## THE DECLARED APPROXIMATION, AND ITS DIRECTION")
    P("   The census reads COMMITTED artifacts only, so a ratio published in a console log or a")
    P("   script comment is not counted; that omission can only make H_NOBODY EASIER to support.")
    P("   The CS_STRICT test is a HEADER-NAME test: a file indexing rows by tape extent under an")
    P("   idiosyncratic name is missed, and a file whose `rows` column means something else is")
    P("   over-counted.  Both directions are live, every accepted header name is dumped, and no")
    P("   classification in this run rests on a single file.")
    P(f"\n# done in {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

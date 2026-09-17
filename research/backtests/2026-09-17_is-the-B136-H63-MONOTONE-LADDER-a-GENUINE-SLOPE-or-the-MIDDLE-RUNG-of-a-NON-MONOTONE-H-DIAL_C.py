#!/usr/bin/env python3
"""Idea 1093 (lane C, 2026-09-17) — is the B136 H=63 MONOTONE LADDER a GENUINE SLOPE, or the
MIDDLE RUNG of a NON-MONOTONE H DIAL?

QUESTION (QUEUE idea 1093, verbatim)
    idea 1086 found the EDGE ladder monotone decreasing in n on B136 at H=63 alone (+11.27 at
    n=5 to +0.40 at n=40), the SLOPE premise 1082 killed, while H=21 and H=126 on the same panel
    both hump.  Re-price that cell against its own DD-matched null at a finer hold ladder and
    report whether the slope is a hold fact or a single-rung accident.  Max 2 params (n, H).

THE TWO TUNED DIALS (PROTOCOL rule 4, no more than two)
    1. N  in {5, 8, 10, 12, 15, 20, 25, 30, 40}            — 1082's / 1086's ladder, unchanged
    2. H  in {21, 42, 52, 63, 76, 90, 126}                 — 1086's 21 and 126 kept so its
                                                             committed columns are reproducible
                                                             (G5, G5c), plus FOUR NEW rungs, two
                                                             of them 63's immediate neighbours
                                                             (52 and 76, ~ +/- 20%)
    9 x 7 = 63 cells per panel, 126 in total, ALL published for the book AND the null.
    SEEDS ARE FROZEN AT 40 (1086's value) and are NOT a dial.  Everything else stays at
    936/1064/1071/1082/1086's construction: cap INF, CAND20 legs, max_vol 0.60, gross 0.75,
    W cadence, 10 bps, LAG 1.

    THE NULL DRAWS STAY PAIRED ACROSS H.  The seed recipe is 1082's verbatim — md5(panel, N,
    "INF", s) with NO H term — so the random rank matrix at a given (panel, N, s) is the SAME
    object at every one of the seven holds, and the min hold is applied to it exactly as it is
    applied to the book.  The H comparison is therefore paired, and the H=21/63/126 columns are
    bit-identical to 1086's, which is what gates G5 and G5c check.

WHAT "EDGE" MEANS HERE — unchanged from 1071/1082/1086, quoted so the four runs read together
    EDGE(n, H) = book CAGR  -  MEDIAN over 40 seeds of the DD-MATCHED null's CAGR,
    where the null is the same machinery with a RANDOM rank matrix and NO eligibility gate, and
    "DD-matched" means the null path is REBUILT at the gross lambda*0.75 that equalises its
    realised |MaxDD| with the book's at that same (n, H).  The CASH convention (r -> lambda*r) is
    carried beside it only so 1071's and 1082's committed numbers stay checkable; REBUILT is the
    headline.  lambda is clipped at 1.0: a draw already DRIER than the book enters unmatched,
    which INFLATES EDGE, and the clipped share is published at every cell (D2).

DECLARED BEFORE ANY NUMBER — what "genuine slope" and "single-rung accident" mean, so neither
can be read off the numbers after the fact
    (a) HOLD FACT (a genuine slope): monotonicity at H=63 is a property of holds NEAR a quarter,
        not of the integer 63.  SIGNATURE — H=52 and H=76, 63's immediate neighbours, are BOTH
        monotone decreasing in n on B136 (H_NEIGHBOUR), AND the H=63 ladder's monotonicity
        survives its own seed noise (H_LUCK: bootstrap P(monotone) >= 0.50).
    (b) SINGLE-RUNG ACCIDENT: H=63 is monotone and nothing around it is (H_NEIGHBOUR FAIL), or
        the H=63 ladder is monotone only in the particular 40 draws 1086 happened to take
        (H_LUCK FAIL).  These are DIFFERENT failures and are reported separately: the first says
        the H axis is rough at this resolution, the second says the object was never resolvable.
    (c) A THIRD outcome, named in advance so it cannot be read as either: the whole finer ladder
        may be monotone (>= 6 of 7 rungs), in which case 1086's "H=63 alone" is an artefact of
        its THREE-POINT H ladder and the queue's framing — 63 as a special middle rung — is
        itself wrong.  H_BAND scores the weaker version of this (>= 4 of 7).
    (d) EDGE IS NOT A KEEP PATH.  Both 4a and 4b are scored at all 126 cells and the rule-8
        walk-forward picks (n, H) on 2009-2016 alone.  A slope that is real and a book that is
        capital-worthy are different claims and this run keeps them apart.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists.  Every level here is
    optimistic and every 4b/4a count is an UPPER bound.  The book-vs-null contrast is drawn from
    the same pool over the same tape, so the bias very largely cancels out of EDGE — but it does
    NOT cancel out of the 4b legs, which are measured against SPY, a real index.
"""
from __future__ import annotations

import hashlib
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

DATE = "2026-09-17"
SLUG = "is-the-B136-H63-MONOTONE-LADDER-a-GENUINE-SLOPE-or-the-MIDDLE-RUNG-of-a-NON-MONOTONE-H-DIAL"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

LAG = 1
WARMUP = 260
MAXVOL = 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST = 10.0
GROSS0 = 0.75
FREQ = "W"
LEGS = [(21, 252), (0, 126), (0, 63)]           # CAND20, 936/1064/1071/1082/1086's construction
CAPNAME = "INF"                                  # frozen, NOT a dial

NS = [5, 8, 10, 12, 15, 20, 25, 30, 40]          # dial 1 — 1082's ladder verbatim
HS = [21, 42, 52, 63, 76, 90, 126]               # dial 2 — the FINER min-hold ladder
NSEED = 40                                       # FROZEN (1086's value, not a dial here)
BISECT = 34
NBOOT = 2000                                     # seed bootstrap of the EDGE ladder
BOOT_SEED = 20260917

PANELS = ["B136", "U56"]                         # B136 is the idea's panel; U56 is the control

# committed cross-run anchors (ideas 936 / 1071 / 1082 / 1086 / 1018+1023)
A936_WH126 = (0.155787, 1.139701, -0.191276)
A1071_N20_NULL_MED_CASH = 0.105068
A1082_EDGE_H126 = {                              # committed REBUILT EDGE ladder at H=126
    "U56": [5.95, 5.35, 6.21, 6.82, 5.22, 5.12, 2.95, 1.55, 0.41],
    "B136": [5.72, 5.24, 8.32, 6.52, 6.83, 4.93, 4.27, 2.81, 1.85],
}
A1086_EDGE = {                                   # 1086's committed null.csv, 4 dp
    ("B136", 21): [8.0742, 4.8415, 5.5438, 4.5974, 3.0719, 4.3979, 3.3695, 1.5937, 0.7994],
    ("B136", 63): [11.2690, 8.8222, 7.6628, 5.1821, 4.4729, 3.3520, 2.1330, 1.4389, 0.3975],
    ("U56", 21): [5.9665, 6.1930, 7.3531, 7.6624, 5.2578, 3.9078, 1.8017, 1.7389, 1.3433],
    ("U56", 63): [6.6369, 8.0702, 6.7987, 5.3577, 4.6305, 2.1233, 2.2713, 2.0750, 0.1465],
}
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


def mdseed(*parts):
    """1082's recipe verbatim — deliberately carries NO H term (see the docstring)."""
    return int(hashlib.md5("|".join(str(x) for x in parts).encode()).hexdigest()[:8], 16)


# ---------------------------------------------------------------- fast runner (gated vs engine)
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
    return (held * rets).sum(axis=1), turn, held


def gross_rescaler(rets, wt, mk):
    """f(lam) -> NET returns of the book REBUILT at gross lam * (this book's gross).
    1082's kernel, unmodified; f(1.0) is gated against nrun() exactly (G1b)."""
    T, N = rets.shape
    mk = mk.copy()
    mk[0] = True
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
    reb = np.flatnonzero(mk)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    A = wt[s0] * (Cp / Cp[s0])
    AR = (A * rets).sum(axis=1)
    S = A.sum(axis=1)
    Wsum = wt[s0].sum(axis=1)
    s0p = reb[np.maximum(seg - 1, 0)]
    Ap = (wt[s0p] * (Cp / Cp[s0p]))[reb]
    Sp = Ap.sum(axis=1)
    Wsp = wt[s0p].sum(axis=1)[reb]
    Ap[0] = 0.0
    Sp[0] = 0.0
    Wsp[0] = 0.0
    Wr = wt[reb]
    c = COST / 1e4

    def f(lam):
        V = 1.0 + lam * (S - Wsum)
        g = lam * AR / V
        Vp = 1.0 + lam * (Sp - Wsp)
        tr = lam * np.abs(Wr - Ap / Vp[:, None]).sum(axis=1)
        out = g.copy()
        out[reb] -= tr * c
        return out

    return f


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


def maxdd(r):
    eq = np.cumprod(1.0 + np.asarray(r, float))
    return float((eq / np.maximum.accumulate(eq) - 1.0).min())


def lagmat(a):
    out = np.zeros_like(a)
    out[LAG:] = a[:-LAG]
    return out


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
    """Target weights under MIN HOLD H and slot count N, cap = INF.  1082's build(), unmodified."""
    W = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
    nsel_by_reb = []
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
        nsel_by_reb.append(len(sel))
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = gross / len(sel)
    return W, np.array(nsel_by_reb)


def build_null(rank_key, priced, reb, N, H, T, K, gross):
    """Same machinery, random ranks, NO eligibility gate (the record's convention).  The rank
    matrix is passed IN so the same draw is reused at every H (paired comparison)."""
    elig = np.ones((T, K), dtype=bool)
    return build(rank_key, elig, priced, reb, N, H, T, K, gross)


def windows(idx):
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    ins = warm & ~oos
    return warm, ins, oos


def blocks(r, warm, ins, oos):
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


def lam_cash(r, target_dd):
    if abs(maxdd(r)) <= abs(target_dd):
        return None
    a, b = 1e-4, 1.0
    for _ in range(BISECT):
        m = 0.5 * (a + b)
        if abs(maxdd(m * r)) > abs(target_dd):
            b = m
        else:
            a = m
    return 0.5 * (a + b)


def lam_rebuilt(f, sl, target_dd):
    if abs(maxdd(f(1.0)[sl])) <= abs(target_dd):
        return None
    a, b = 1e-4, 1.0
    for _ in range(BISECT):
        m = 0.5 * (a + b)
        if abs(maxdd(f(m)[sl])) > abs(target_dd):
            b = m
        else:
            a = m
    return 0.5 * (a + b)


def is_mono(v):
    """1086's test, verbatim: monotone DECREASING over the n ladder, weak inequality."""
    return bool(all(v[i] >= v[i + 1] for i in range(len(v) - 1)))


def main():
    t0 = time.time()
    P(f"# Idea 1093 (lane C, {DATE}) — is the B136 H=63 MONOTONE LADDER a GENUINE SLOPE or the")
    P("# MIDDLE RUNG of a NON-MONOTONE H DIAL?")
    P(f"# 2 tuned dials: N {NS} x H {HS}.  ALL 63 cells per panel reported (126 total).")
    P(f"# FROZEN (not dials): SEEDS {NSEED}, cap {CAPNAME}, CAND20 legs {LEGS}, max_vol {MAXVOL}, "
      f"gross {GROSS0}, cost {COST:.0f} bps, LAG {LAG}, cadence {FREQ}.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   (a) HOLD FACT (genuine slope) = H_NEIGHBOUR PASS (both 52 and 76 monotone on B136)")
    P("#       AND H_LUCK PASS (bootstrap P(monotone at B136 H=63) >= 0.50).")
    P("#   (b) SINGLE-RUNG ACCIDENT = either fails, and the two failures are reported apart: a")
    P("#       rough H axis (neighbours hump) is not the same as an unresolvable ladder.")
    P("#   (c) NAMED IN ADVANCE: >= 6 of 7 rungs monotone would make 1086's 'H=63 alone' an")
    P("#       artefact of its 3-point H ladder and the queue's framing itself wrong.")
    P("#   (d) EDGE IS NOT A KEEP PATH.  4a and 4b scored at all 126 cells; rule 8 picks (n, H)")
    P("#       on 2009-2016 alone and reads 2017-2026 ONCE.")
    P("# The null draws stay PAIRED across H (1082's seed recipe carries no H term), so the")
    P("# H=21/63/126 columns are bit-identical to 1086's — gates G5 and G5c.")
    P("")

    rows, nullrows, gaterows, seedrows = [], [], [], []
    picks, benchrows, bootrows = [], [], []
    gates = {}
    seedmat = {}          # (panel, N, H) -> np.array of NSEED null CAGRs (REBUILT)

    for panel in PANELS:
        px = load_universe(broad=(panel == "B136")).dropna(how="all").ffill()
        idx = px.index
        K = len(px.columns)
        T = len(idx)
        rets = px.pct_change().fillna(0.0).values
        priced = px.notna().values
        mk = rebalance_mask(idx, FREQ).values
        mkl = np.roll(mk, LAG)
        warm, ins, oos = windows(idx)
        sc, elig = mech(px)
        rank_key = -np.nan_to_num(sc, nan=-np.inf)
        rank_key[np.isnan(sc)] = np.inf
        reb = np.flatnonzero(mk)

        spy = px["SPY"].pct_change().fillna(0.0).values
        sb = blocks(spy, warm, ins, oos)
        live = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"].values
        lb = blocks(live, warm, ins, oos)
        live_dd = lb["MaxDD"]
        P(f"## {panel}: {K} columns, {T} days {idx[0].date()}..{idx[-1].date()}, "
          f"{len(reb)} rebalance dates")
        P(f"   SPY        full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%}  "
          f"halves {sb['H1']:.4f}/{sb['H2']:.4f}  OOS {sb['OOS_CAGR']:.2%} / "
          f"{sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"   RULES v2   full {lb['CAGR']:.2%} / {lb['Sharpe']:.4f} / {lb['MaxDD']:.2%}  "
          f"halves {lb['H1']:.4f}/{lb['H2']:.4f}  OOS {lb['OOS_CAGR']:.2%} / "
          f"{lb['OOS_Sharpe']:.4f} / {lb['OOS_MaxDD']:.2%}")
        benchrows += [dict(panel=panel, series="SPY", **sb), dict(panel=panel, series="RULESv2", **lb)]

        # ---- GATES -----------------------------------------------------------------------
        if panel == "U56":
            W20, _ = build(rank_key, elig, priced, reb, 20, 126, T, K, GROSS0)
            wdf = pd.DataFrame(W20, index=idx, columns=px.columns)
            eng = backtest(px, wdf, cost_bps=COST, freq=FREQ)["returns"].values
            g, tn, _ = nrun(rets, lagmat(W20), mkl)
            fast = g - tn * COST / 1e4
            d1 = float(np.abs(fast[WARMUP:] - eng[WARMUP:]).max())
            gates["G1 fast runner == engine.backtest (U56, N=20, H=126, cap INF)"] = (d1, d1 < 1e-12)
            f20 = gross_rescaler(rets, lagmat(W20), mkl)
            d1b = float(np.abs(f20(1.0) - fast).max())
            gates["G1b gross_rescaler(1.0) == nrun (the bisection kernel is the same book)"] = (
                d1b, d1b < 1e-14)
            m = fmet(fast[warm])
            d2 = max(abs(m[0] - A936_WH126[0]), abs(m[1] - A936_WH126[1]), abs(m[2] - A936_WH126[2]))
            gates["G2 CROSS-RUN vs 936/1071/1082/1086's committed W/H126 N=20 triple"] = (d2, d2 < 5e-3)
            d3 = max(abs(sb["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
                     abs(sb["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
                     abs(sb["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
            gates["G3 CROSS-RUN SPY OOS triple"] = (d3, d3 < 5e-4)
            d6 = abs(live_dd - LIVE_MAXDD_COMMITTED)
            gates["G6 live RULES v2 MaxDD == committed -12.05%"] = (d6, d6 < 5e-4)
            rngc = np.random.default_rng(mdseed(panel, 20, CAPNAME, 0))
            rk0 = rngc.random((T, K))
            Wn0, _ = build_null(rk0, priced, reb, 20, 126, T, K, GROSS0)
            fn0 = gross_rescaler(rets, lagmat(Wn0), mkl)
            dds = [abs(maxdd(fn0(l)[warm])) for l in np.linspace(0.1, 1.0, 19)]
            viol = float(max(0.0, max(dds[i] - dds[i + 1] for i in range(len(dds) - 1))))
            gates["G4c |MaxDD| of the REBUILT null is monotone in lambda"] = (viol, viol < 1e-12)
            rngd = np.random.default_rng(mdseed(panel, 20, CAPNAME, 0))
            Wn0b, _ = build_null(rngd.random((T, K)), priced, reb, 20, 126, T, K, GROSS0)
            d7 = float(np.abs(Wn0 - Wn0b).max())
            gates["G7 null draw is deterministic in its seed recipe"] = (d7, d7 == 0.0)

        # ---- the grid --------------------------------------------------------------------
        for N in NS:
            # the null rank matrices for this (panel, N) — drawn ONCE and reused at every H
            rankmats = [np.random.default_rng(mdseed(panel, N, CAPNAME, s)).random((T, K))
                        for s in range(NSEED)]
            for H in HS:
                W, nsel = build(rank_key, elig, priced, reb, N, H, T, K, GROSS0)
                g, tn, _ = nrun(rets, lagmat(W), mkl)
                r = g - tn * COST / 1e4
                b = blocks(r, warm, ins, oos)
                l4b, l4a, l4bo = legs_4b(b, sb), legs_4a(b, lb), legs_4b_oos(b, sb)
                row = dict(panel=panel, N=N, H=H, cap=CAPNAME, mean_nsel=float(nsel.mean()),
                           turnover=float(tn[warm].sum() / (warm.sum() / 252.0)), **b,
                           **l4b, **l4a, **l4bo,
                           pass4b=all(l4b.values()), pass4a=all(l4a.values()),
                           pass4b_oos=all(l4bo.values()))
                row["pass4b_full_and_oos"] = row["pass4b"] and row["pass4b_oos"]

                c_cash, c_reb, c_is, lam_c, lam_r = [], [], [], [], []
                for s in range(NSEED):
                    Wn, _ = build_null(rankmats[s], priced, reb, N, H, T, K, GROSS0)
                    fn = gross_rescaler(rets, lagmat(Wn), mkl)
                    base = fn(1.0)
                    rn = base[warm]
                    lc = lam_cash(rn, b["MaxDD"])
                    if lc is None:
                        c_cash.append(fmet(rn)[0]); lam_c.append(1.0)
                    else:
                        c_cash.append(fmet(lc * rn)[0]); lam_c.append(lc)
                    lr = lam_rebuilt(fn, warm, b["MaxDD"])
                    if lr is None:
                        c_reb.append(fmet(rn)[0]); lam_r.append(1.0)
                    else:
                        c_reb.append(fmet(fn(lr)[warm])[0]); lam_r.append(lr)
                    lri = lam_rebuilt(fn, ins, b["IS_MaxDD"])
                    c_is.append(fmet(base[ins] if lri is None else fn(lri)[ins])[0])
                    seedrows.append(dict(panel=panel, N=N, H=H, seed=s,
                                         null_CAGR_cash=c_cash[-1], null_CAGR_rebuilt=c_reb[-1],
                                         null_IS_CAGR_rebuilt=c_is[-1],
                                         lam_cash=lam_c[-1], lam_rebuilt=lam_r[-1]))
                c_cash, c_reb, c_is = np.array(c_cash), np.array(c_reb), np.array(c_is)
                seedmat[(panel, N, H)] = c_reb.copy()
                med_reb = float(np.median(c_reb))
                nullrows.append(dict(
                    panel=panel, N=N, H=H, cap=CAPNAME, seeds=NSEED,
                    book_CAGR=b["CAGR"], book_MaxDD=b["MaxDD"], book_IS_CAGR=b["IS_CAGR"],
                    null_CAGR_med_rebuilt=med_reb,
                    null_CAGR_med_cash=float(np.median(c_cash)),
                    null_IS_CAGR_med_rebuilt=float(np.median(c_is)),
                    EDGE_pp=100.0 * (b["CAGR"] - med_reb),
                    EDGE_pp_cash=100.0 * (b["CAGR"] - float(np.median(c_cash))),
                    EDGE_IS_pp=100.0 * (b["IS_CAGR"] - float(np.median(c_is))),
                    null_CAGR_sd=float(c_reb.std(ddof=1)),
                    EDGE_se_pp=100.0 * 1.2533 * float(c_reb.std(ddof=1)) / np.sqrt(NSEED),
                    book_pct_of_null=float((c_reb < b["CAGR"]).mean()),
                    lam_median_rebuilt=float(np.median(lam_r)),
                    lam_median_cash=float(np.median(lam_c)),
                    null_already_drier_rebuilt=int(sum(1 for x in lam_r if x == 1.0)),
                    conv_gap_pp=100.0 * (med_reb - float(np.median(c_cash))),
                ))
                row["EDGE_pp"] = 100.0 * (b["CAGR"] - med_reb)
                row["EDGE_pp_cash"] = 100.0 * (b["CAGR"] - float(np.median(c_cash)))
                row["EDGE_IS_pp"] = 100.0 * (b["IS_CAGR"] - float(np.median(c_is)))
                row["book_pct_of_null"] = float((c_reb < b["CAGR"]).mean())
                rows.append(row)
                P(f"   N={N:2d} H={H:3d} done  book {b['CAGR']:.2%} / {b['Sharpe']:.4f} / "
                  f"{b['MaxDD']:.2%}  turn {row['turnover']:.2f}x  "
                  f"EDGE {row['EDGE_pp']:+.3f} pp  ({time.time()-t0:.0f}s)")

        # ---- RULE 8: IS-only choosers pick (N, H) jointly, OOS read ONCE -------------------
        gp = pd.DataFrame([r for r in rows if r["panel"] == panel])
        for cname, key in [("C_ISSHARPE", "IS_Sharpe"), ("C_ISDD", "IS_MaxDD"),
                           ("C_ISEDGE", "EDGE_IS_pp"), ("C_ISCAGR", "IS_CAGR")]:
            pick = gp.sort_values(key, ascending=False).iloc[0]
            picks.append(dict(panel=panel, chooser=cname, N=int(pick["N"]), H=int(pick["H"]),
                              IS_Sharpe=pick["IS_Sharpe"], IS_MaxDD=pick["IS_MaxDD"],
                              IS_EDGE_pp=pick["EDGE_IS_pp"],
                              OOS_CAGR=pick["OOS_CAGR"], OOS_Sharpe=pick["OOS_Sharpe"],
                              OOS_MaxDD=pick["OOS_MaxDD"],
                              full_CAGR=pick["CAGR"], full_Sharpe=pick["Sharpe"],
                              full_MaxDD=pick["MaxDD"], H1=pick["H1"], H2=pick["H2"],
                              spy_OOS_CAGR=sb["OOS_CAGR"], spy_OOS_Sharpe=sb["OOS_Sharpe"],
                              spy_OOS_MaxDD=sb["OOS_MaxDD"],
                              live_OOS_CAGR=lb["OOS_CAGR"], live_OOS_Sharpe=lb["OOS_Sharpe"],
                              live_OOS_MaxDD=lb["OOS_MaxDD"],
                              O_S=pick["O_S"], O_DD=pick["O_DD"], O_CAGR=pick["O_CAGR"],
                              pass4b_oos=bool(pick["pass4b_oos"]),
                              pass4b_full=bool(pick["pass4b"]), pass4a=bool(pick["pass4a"])))

    grid = pd.DataFrame(rows)
    nul = pd.DataFrame(nullrows)
    pk = pd.DataFrame(picks)
    bn = pd.DataFrame(benchrows)
    sd = pd.DataFrame(seedrows)

    # ---- cross-run gates on the shared columns -------------------------------------------
    d5 = 0.0
    for p_ in PANELS:
        s = nul[(nul.panel == p_) & (nul.H == 126)].sort_values("N")
        d5 = max(d5, float(np.abs(s.EDGE_pp.values - np.array(A1082_EDGE_H126[p_])).max()))
    gates["G5 CROSS-RUN 1082's committed H=126 EDGE ladder, both panels"] = (d5, d5 < 5e-3)
    d5c = 0.0
    for (p_, H_), vals in A1086_EDGE.items():
        s = nul[(nul.panel == p_) & (nul.H == H_)].sort_values("N")
        d5c = max(d5c, float(np.abs(s.EDGE_pp.values - np.array(vals)).max()))
    gates["G5c CROSS-RUN 1086's committed H=21 and H=63 EDGE ladders, both panels "
          "(the premise itself)"] = (d5c, d5c < 5e-3)
    u20 = nul[(nul.panel == "U56") & (nul.N == 20) & (nul.H == 126)].iloc[0]
    d5b = abs(u20.null_CAGR_med_cash - A1071_N20_NULL_MED_CASH)
    gates["G5b CROSS-RUN 1071/1082's committed U56 N=20 H=126 null median (CASH)"] = (
        d5b, d5b < 5e-3)
    tspread = float(grid[grid.panel == "B136"].turnover.max() - grid[grid.panel == "B136"].turnover.min())
    gates["G8 the finer H dial is LIVE (B136 turnover spread >= 1.0x/yr across the grid)"] = (
        tspread, tspread >= 1.0)

    P("")
    P("## GATES (printed before any result number)")
    for k, (v, ok) in gates.items():
        P(f"   {'PASS' if ok else 'FAIL'}  {k}: |d| = {v:.3e}")
        gaterows.append(dict(gate=k, value=v, passed=bool(ok)))

    P("")
    P("## THE GRID — book at every (N, H), both panels")
    for panel in PANELS:
        P(f"   --- {panel} ---")
        P("       N   H  nsel   turn    CAGR    Sharpe   MaxDD      H1/H2        OOS C/S/DD"
          "             4b 4a 4bOOS")
        for _, r in grid[grid.panel == panel].sort_values(["N", "H"]).iterrows():
            P(f"      {int(r.N):2d} {int(r.H):3d} {r.mean_nsel:5.1f} {r.turnover:6.2f} "
              f"{r.CAGR:7.2%} {r.Sharpe:8.4f} {r.MaxDD:8.2%}  {r.H1:.3f}/{r.H2:.3f}  "
              f"{r.OOS_CAGR:6.2%}/{r.OOS_Sharpe:.4f}/{r.OOS_MaxDD:7.2%}"
              f"   {int(r.pass4b)}  {int(r.pass4a)}   {int(r.pass4b_oos)}")
        s = grid[grid.panel == panel]
        P(f"      4b full {int(s.pass4b.sum())}/{len(s)}   4b OOS {int(s.pass4b_oos.sum())}/{len(s)}"
          f"   4a {int(s.pass4a.sum())}/{len(s)}")

    P("")
    P(f"## THE EDGE LADDER AT EVERY HOLD — the question itself ({NSEED} seeds, REBUILT)")
    mono = {}
    for panel in PANELS:
        P(f"   --- {panel} ---   EDGE(n, H) in pp    [* = rung committed by 1082/1086]")
        P("        H  " + "".join(f"{n:>9d}" for n in NS)
          + "     argmax   EDGE(5)  EDGE(40)   MONO?  worst up-step")
        for H in HS:
            s = nul[(nul.panel == panel) & (nul.H == H)].set_index("N").reindex(NS)
            v = s.EDGE_pp.values
            se = s.EDGE_se_pp.values
            am = int(s.EDGE_pp.idxmax())
            mk_ = is_mono(v)
            mono[(panel, H)] = mk_
            ups = [(v[i + 1] - v[i]) for i in range(len(v) - 1)]
            wi = int(np.argmax(ups))
            wu = ups[wi]
            wsig = wu / float(np.hypot(se[wi], se[wi + 1]))
            star = "*" if (H in (21, 63, 126)) else " "
            P(f"     {star}{H:3d}  " + "".join(f"{x:>+9.3f}" for x in v)
              + f"     n={am:<3d}  {v[0]:+7.3f}  {v[-1]:+7.3f}    {'YES' if mk_ else 'no '}"
              + f"   {wu:+.3f} pp ({wsig:+.2f} SE) at n={NS[wi]}->{NS[wi+1]}")
        P("        SE  " + "".join(
            f"{x:>9.3f}" for x in nul[(nul.panel == panel) & (nul.H == 63)]
            .set_index("N").reindex(NS).EDGE_se_pp.values) + "     (seed SE at H=63)")
        mh = [H for H in HS if mono[(panel, H)]]
        P(f"      MONOTONE DECREASING at {len(mh)} of {len(HS)} holds: "
          + (", ".join(str(H) for H in mh) if mh else "(none)"))

    P("")
    P(f"## THE SEED BOOTSTRAP — is the monotonicity a lucky draw?  ({NBOOT:,} resamples of the "
      f"{NSEED} seeds, PAIRED across H, independent across n)")
    rng = np.random.default_rng(BOOT_SEED)
    for panel in PANELS:
        # the book is deterministic; only the null median is resampled.  Book CAGR is per (N, H).
        bookNH = {(N, H): float(nul[(nul.panel == panel) & (nul.N == N) & (nul.H == H)]
                                .book_CAGR.iloc[0]) for N in NS for H in HS}
        idxs = {N: rng.integers(0, NSEED, size=(NBOOT, NSEED)) for N in NS}
        E = {}     # (H) -> (NBOOT, len(NS)) bootstrapped EDGE ladders
        for H in HS:
            M = np.empty((NBOOT, len(NS)))
            for j, N in enumerate(NS):
                draws = seedmat[(panel, N, H)][idxs[N]]        # (NBOOT, NSEED), paired across H
                M[:, j] = 100.0 * (bookNH[(N, H)] - np.median(draws, axis=1))
            E[H] = M
        P(f"   --- {panel} ---")
        P("        H   P(monotone)   P(argmax=5)  mean#violations   90% argmax set")
        for H in HS:
            M = E[H]
            dif = np.diff(M, axis=1)
            pm = float((dif <= 0).all(axis=1).mean())
            nv = float((dif > 0).sum(axis=1).mean())
            am = np.array(NS)[M.argmax(axis=1)]
            p5 = float((am == 5).mean())
            vals, cnts = np.unique(am, return_counts=True)
            order = np.argsort(-cnts)
            cum, keep = 0, []
            for o in order:
                keep.append(int(vals[o])); cum += cnts[o]
                if cum >= 0.90 * NBOOT:
                    break
            P(f"      {H:3d}      {pm:7.3f}       {p5:7.3f}        {nv:7.3f}        "
              + "{" + ",".join(str(x) for x in sorted(keep)) + "}")
            bootrows.append(dict(panel=panel, H=H, P_monotone=pm, P_argmax_5=p5,
                                 mean_violations=nv, observed_monotone=bool(mono[(panel, H)]),
                                 argmax_set_90="{" + ",".join(str(x) for x in sorted(keep)) + "}"))

    P("")
    P("## THE H AXIS — argmax n and the ladder's END-TO-END DROP, by hold")
    for panel in PANELS:
        P(f"   --- {panel} ---")
        P("        H   argmax n   EDGE(5)-EDGE(40)   SE    sigmas    turn(n=20)")
        for H in HS:
            s = nul[(nul.panel == panel) & (nul.H == H)].set_index("N").reindex(NS)
            d = float(s.EDGE_pp.iloc[0] - s.EDGE_pp.iloc[-1])
            se = float(np.hypot(s.EDGE_se_pp.iloc[0], s.EDGE_se_pp.iloc[-1]))
            tn = float(grid[(grid.panel == panel) & (grid.N == 20) & (grid.H == H)].turnover.iloc[0])
            P(f"      {H:3d}      n={int(s.EDGE_pp.idxmax()):<3d}      {d:+7.3f} pp      "
              f"{se:.3f}   {d/se:6.2f}      {tn:5.2f}x")

    P("")
    P("## RULE 8 — IS(2009-2016)-only choosers pick (N, H) over 63 cells, OOS(2017-2026) ONCE")
    for _, r in pk.iterrows():
        P(f"   {r.panel} {r.chooser}: picks N={int(r.N)} H={int(r.H)} -> OOS {r.OOS_CAGR:.2%} / "
          f"{r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:.2%}  | SPY OOS {r.spy_OOS_CAGR:.2%} / "
          f"{r.spy_OOS_Sharpe:.4f} / {r.spy_OOS_MaxDD:.2%} | RULES v2 OOS {r.live_OOS_CAGR:.2%} / "
          f"{r.live_OOS_Sharpe:.4f} / {r.live_OOS_MaxDD:.2%} | 4b_OOS {r.pass4b_oos} "
          f"(O_S {r.O_S} O_DD {r.O_DD} O_CAGR {r.O_CAGR}) 4b_full {r.pass4b_full} 4a {r.pass4a}")

    P("")
    P("## HYPOTHESES (declared before the run, scored as written)")
    H_ = []
    bootd = pd.DataFrame(bootrows)

    def pmono(panel, H):
        return float(bootd[(bootd.panel == panel) & (bootd.H == H)].P_monotone.iloc[0])

    g5c_key = ("G5c CROSS-RUN 1086's committed H=21 and H=63 EDGE ladders, both panels "
               "(the premise itself)")
    H_.append(("H_REP the B136 H=63 ladder REPRODUCES 1086's committed column AND is monotone "
               "decreasing in n (the premise as stated)",
               bool(gates[g5c_key][1] and mono[("B136", 63)]),
               f"G5c |d| = {gates[g5c_key][0]:.2e} pp; monotone at B136 H=63: "
               f"{mono[('B136', 63)]}"))
    H_.append(("H_NEIGHBOUR 63's IMMEDIATE NEIGHBOURS H=52 and H=76 are BOTH monotone decreasing "
               "in n on B136 (the HOLD-FACT signature)",
               bool(mono[("B136", 52)] and mono[("B136", 76)]),
               f"H=52 {'MONO' if mono[('B136',52)] else 'humps'}, "
               f"H=76 {'MONO' if mono[('B136',76)] else 'humps'}"))
    H_.append(("H_BAND at least 4 of the 7 B136 holds are monotone decreasing in n",
               bool(sum(1 for H in HS if mono[("B136", H)]) >= 4),
               f"{sum(1 for H in HS if mono[('B136', H)])} of {len(HS)}: "
               + ",".join(str(H) for H in HS if mono[("B136", H)])))
    H_.append(("H_LUCK the B136 H=63 monotonicity survives its OWN seed noise "
               "(bootstrap P(monotone) >= 0.50)",
               bool(pmono("B136", 63) >= 0.50),
               f"P(monotone) = {pmono('B136', 63):.3f} over {NBOOT:,} resamples"))
    b_am = [int(nul[(nul.panel == "B136") & (nul.H == H)].set_index("N").EDGE_pp.idxmax())
            for H in HS]
    H_.append(("H_ARGMAX_MONO on B136 the argmax n is NON-DECREASING in H over the finer ladder "
               "(the hold is a smooth dial)",
               bool(all(b_am[i] <= b_am[i + 1] for i in range(len(b_am) - 1))),
               ", ".join(f"H={H}:{n}" for H, n in zip(HS, b_am))))
    H_.append(("H_U56_NONE U56 has NO monotone hold on the finer ladder (1086's PANEL SPLIT "
               "survives resolution)",
               bool(not any(mono[("U56", H)] for H in HS)),
               f"{sum(1 for H in HS if mono[('U56', H)])} of {len(HS)} monotone on U56"))
    H_.append(("H_TURN turnover falls strictly as H lengthens at every (panel, N) "
               "(the finer dial is doing what a hold does)",
               bool(all(grid[(grid.panel == p_) & (grid.N == n) & (grid.H == HS[i])].turnover.iloc[0]
                        > grid[(grid.panel == p_) & (grid.N == n) & (grid.H == HS[i + 1])].turnover.iloc[0]
                        for p_ in PANELS for n in NS for i in range(len(HS) - 1))),
               f"B136 turnover spread {tspread:.2f}x/yr"))
    H_.append(("H_WF >= 1 rule-8 pick clears 4b OUT OF SAMPLE",
               bool(pk.pass4b_oos.any()), f"{int(pk.pass4b_oos.sum())} of {len(pk)} picks"))
    H_.append(("H_4A no cell clears 4a (the DD leg is a book fact, not an (n, H) fact)",
               bool(not grid.pass4a.any()),
               f"{int(grid.pass4a.sum())} of {len(grid)} cells pass 4a"))
    for name, ok, note in H_:
        P(f"   {'PASS' if ok else 'FAIL'}  {name}  [{note}]")

    P("")
    P("## THE VERDICT ON THE QUEUE'S QUESTION, read off the PRE-DECLARED rules only")
    hf = mono[("B136", 52)] and mono[("B136", 76)] and pmono("B136", 63) >= 0.50
    allmono = sum(1 for H in HS if mono[("B136", H)])
    if allmono >= 6:
        lab = "OUTCOME (c): the WHOLE finer ladder is monotone — '63 alone' was a 3-POINT ARTEFACT"
    elif hf:
        lab = "OUTCOME (a): HOLD FACT — a genuine slope over a band of holds around a quarter"
    else:
        lab = "OUTCOME (b): SINGLE-RUNG ACCIDENT"
    P(f"   {lab}")
    P(f"   neighbours 52/76 monotone: {mono[('B136',52)]}/{mono[('B136',76)]};  "
      f"bootstrap P(mono at 63) = {pmono('B136',63):.3f};  "
      f"{allmono} of {len(HS)} B136 holds monotone")

    # ------------------------------------------------------------------ post-run diagnostics
    P("")
    P("## POST-RUN DIAGNOSTICS — computed AFTER reading the grid and labelled as such, NOT")
    P("## pre-declared hypotheses.")
    diagrows = []
    P("")
    P("   (D1) IS THE SLOPE'S OWN LOCAL STEP DECISIVE?  EDGE at two cells differs only through")
    P("        the two null medians (the books are deterministic), so SE(dEDGE) = hypot(SEa,SEb).")
    for panel in PANELS:
        for H in HS:
            s = nul[(nul.panel == panel) & (nul.H == H)].set_index("N").reindex(NS)
            v, se = s.EDGE_pp.values, s.EDGE_se_pp.values
            nd = sum(1 for i in range(len(v) - 1)
                     if (v[i] - v[i + 1]) > 2 * np.hypot(se[i], se[i + 1]))
            nn = sum(1 for i in range(len(v) - 1)
                     if (v[i + 1] - v[i]) > 2 * np.hypot(se[i], se[i + 1]))
            P(f"        {panel} H={H:3d}: adjacent steps DECISIVELY DOWN {nd} of {len(v)-1}, "
              f"DECISIVELY UP {nn} of {len(v)-1}, rest inside 2 SE")
            diagrows.append(dict(diag="D1_steps", panel=panel, H=H, a=nd, b=nn,
                                 delta_pp=float(v[0] - v[-1]), se_pp=float(np.hypot(se[0], se[-1])),
                                 sigmas=float((v[0] - v[-1]) / np.hypot(se[0], se[-1])),
                                 decisive=bool(abs(v[0] - v[-1]) > 2 * np.hypot(se[0], se[-1]))))
    P("")
    P("   (D2) THE lambda <= 1 CLIP, as 1082/1086 flagged it.  A null draw already DRIER than the")
    P("        book enters unmatched at lambda = 1 with its CAGR understated, which INFLATES")
    P("        EDGE.  Share of draws clipped, by (panel, H, n):")
    for panel in PANELS:
        for H in HS:
            s = nul[(nul.panel == panel) & (nul.H == H)].set_index("N").reindex(NS)
            P(f"        {panel} H={H:3d}: " + "  ".join(
                f"{n}:{v/NSEED:.2f}" for n, v in zip(NS, s.null_already_drier_rebuilt.values)))
            for n, v, e in zip(NS, s.null_already_drier_rebuilt.values, s.EDGE_pp.values):
                diagrows.append(dict(diag="D2_drier_share", panel=panel, H=H, a=n, b=np.nan,
                                     delta_pp=float(e), se_pp=float(v) / NSEED, sigmas=np.nan,
                                     decisive=np.nan))
    P("")
    P("   (D3) THE 4b PASSES AND THEIR MARGIN ON THE BINDING LEG.")
    if not grid.pass4b.any():
        P("        none")
    for _, r in grid[grid.pass4b].iterrows():
        sbp = bn[(bn.panel == r.panel) & (bn.series == "SPY")].iloc[0]
        ddm = 100.0 * (DD_CAP * abs(sbp.MaxDD) - abs(r.MaxDD))
        cgm = 100.0 * (r.CAGR - CAGR_FLOOR * sbp.CAGR)
        reachable = ((pk.panel == r.panel) & (pk.N == r.N) & (pk.H == r.H)).any()
        P(f"        {r.panel} N={int(r.N)} H={int(r.H)}: 4b PASSES full-sample; DD margin "
          f"{ddm:+.3f} pp (|{r.MaxDD:.2%}| vs cap {DD_CAP*abs(sbp.MaxDD):.2%}), CAGR margin "
          f"{cgm:+.3f} pp; 4b OOS {bool(r.pass4b_oos)}; reachable by an IS-only chooser: "
          f"{bool(reachable)}")
        diagrows.append(dict(diag="D3_4b_pass", panel=r.panel, H=int(r.H), a=int(r.N), b=np.nan,
                             delta_pp=ddm, se_pp=cgm, sigmas=np.nan, decisive=bool(reachable)))
    P("        1083 measured the 90% width of a quantity of this kind at 4.1-7.2 pp on this tape;")
    P("        any DD margin far inside that is not decidable here.")

    P("")
    dump(grid, "grid"); dump(nul, "null"); dump(sd, "seeds"); dump(pk, "rule8")
    dump(bootd, "bootstrap"); dump(bn, "benchmarks"); dump(pd.DataFrame(gaterows), "gates")
    dump(pd.DataFrame([dict(hypothesis=n, passed=bool(o), note=t) for n, o, t in H_]),
         "hypotheses")
    dump(pd.DataFrame(diagrows), "diagnostics")
    P(f"# done in {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

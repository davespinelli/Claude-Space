#!/usr/bin/env python3
"""Idea 1172 (lane C, 2026-09-17) — is the EDGE LADDER TRUNCATED at n=5, or does an INTERIOR
PEAK exist BELOW it?

QUESTION (QUEUE idea 1172, verbatim)
    idea 1093 found the B136 argmax sits at n=5, the ladder's LEFT END, at 6 of 7 holds with
    bootstrap P(argmax=5) = 1.000, so every 'peak' the record has published in this family may
    be a boundary and not an interior optimum.  Extend the n ladder below 5 (n in {1, 2, 3, 4,
    5, 8}) at the holds where the argmax is at the edge and report whether an interior peak
    exists at all.  Max 2 params (n, H).

THE TWO TUNED DIALS (PROTOCOL rule 4, no more than two)
    1. N  in {1, 2, 3, 4, 5, 8, 10}       — the queue's set {1,2,3,4,5,8} plus n=10, kept ONLY
                                            so three rungs (5, 8, 10) overlap 1082/1086/1093's
                                            committed ladder and can be gated cell-for-cell.
    2. H  in {21, 42, 52, 63, 76, 90, 126} — 1093's finer hold ladder, UNCHANGED.  The queue
                                            names "the holds where the argmax is at the edge",
                                            which on B136 is H in {21,42,52,63,76,90} (1093's
                                            argmax path 5,5,5,5,5,5,10).  H=126 and the whole
                                            U56 panel are carried as CONTROLS, not dropped: a
                                            left-end argmax that appears everywhere is a
                                            different object from one that appears only where
                                            1093 found it.
    7 x 7 = 49 cells per panel, 98 in total, ALL published for the book AND the null.
    SEEDS ARE FROZEN AT 40 (1086/1093's value) and are NOT a dial.  Everything else stays at
    936/1064/1071/1082/1086/1093's construction: cap INF, CAND20 legs, max_vol 0.60, gross 0.75,
    W cadence, 10 bps, LAG 1.  The null seed recipe is 1082's verbatim — md5(panel, N, "INF", s)
    with NO H term — so every (panel, n, H) cell this run shares with 1093 is bit-comparable
    (gates G5, G5c) and the null draws stay PAIRED across H.

WHAT "EDGE" MEANS HERE — unchanged from 1071/1082/1086/1093, quoted so the five runs read together
    EDGE(n, H) = book CAGR  -  MEDIAN over 40 seeds of the DD-MATCHED null's CAGR,
    where the null is the same machinery with a RANDOM rank matrix and NO eligibility gate, and
    "DD-matched" means the null path is REBUILT at the gross lambda*0.75 that equalises its
    realised |MaxDD| with the book's at that same (n, H).  lambda is CLIPPED AT 1.0: a draw
    already DRIER than the book enters unmatched, which INFLATES EDGE.

    THAT CLIP IS THE WHOLE DANGER OF THIS PARTICULAR QUESTION, so it is priced, not just
    flagged.  Walking n DOWN deepens the book's drawdown (fewer names, same gross), which makes
    the null drier relative to it, which makes the clip bind on MORE draws — a mechanism that
    manufactures a left-end EDGE peak out of nothing.  This run therefore publishes, at every
    cell, BOTH:
        EDGE      — lambda in [1e-4, 1.0], the record's convention, the headline for comparability
        EDGE_SYM  — lambda in [1e-4, 3.0], the SAME bisection with the clip released upward, so a
                    null drier than the book is LEVERED up to the book's drawdown instead of
                    entering understated.  EDGE_SYM is a measurement control, not a proposed
                    book: nothing here levers real capital.
    If the two disagree about where the peak sits, the record's EDGE is the artefact.

DECLARED BEFORE ANY NUMBER — the four outcomes, so none can be read off the numbers after the
fact.  All are scored on B136 over the SIX EDGE HOLDS {21,42,52,63,76,90}, 1093's own set.
    (A) INTERIOR PEAK AT n=5: argmax = 5 at >= 4 of the 6 — n=5 was a genuine interior optimum
        all along and 1093's boundary worry is answered NO.
    (B) STILL TRUNCATED: argmax = 1 at >= 4 of the 6 — there is no interior peak; EDGE rises all
        the way into a ONE-NAME book, and every published 'peak' in this family is a boundary.
    (C) NEW INTERIOR PEAK ELSEWHERE: argmax in {2,3,4,8} at >= 4 of the 6 — a peak exists but
        the record has been quoting the wrong rung.
    (D) NOT RESOLVABLE: no single rung reaches 4 of 6 — the argmax is not a measurable object at
        40 seeds on this axis, which is itself a finding about every argmax the record publishes.
    EDGE IS NOT A KEEP PATH.  4a and 4b are scored at all 98 cells and the rule-8 walk-forward
    picks (n, H) on 2009-2016 alone and reads 2017-2026 ONCE.  A ladder peak and a book worth
    capital are different claims; at n <= 4 they are expected to point opposite ways.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists.  Every level here is
    optimistic and every 4b/4a count is an UPPER bound.  A one-name book drawn from a
    current-constituent list is the most survivorship-flattered object in the whole record and
    its CAGR should be read as an upper bound twice over.
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
SLUG = "is-the-EDGE-LADDER-TRUNCATED-at-n-5-or-does-an-INTERIOR-PEAK-EXIST-BELOW-IT"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

LAG = 1
WARMUP = 260
MAXVOL = 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST = 10.0
GROSS0 = 0.75
FREQ = "W"
LEGS = [(21, 252), (0, 126), (0, 63)]           # CAND20, the record's construction
CAPNAME = "INF"                                  # frozen, NOT a dial

NS = [1, 2, 3, 4, 5, 8, 10]                      # dial 1 — the queue's extension (+10 for gating)
HS = [21, 42, 52, 63, 76, 90, 126]               # dial 2 — 1093's finer hold ladder
EDGE_HOLDS = [21, 42, 52, 63, 76, 90]            # 1093's B136 left-end-argmax holds, pre-declared
NSEED = 40                                       # FROZEN (1086/1093's value, not a dial here)
BISECT = 34
LAMMAX = 3.0                                     # EDGE_SYM's upward clip (measurement control)
NBOOT = 2000
BOOT_SEED = 20260917

PANELS = ["B136", "U56"]

# committed cross-run anchors (ideas 936 / 1071 / 1082 / 1093 / 1018+1023)
A936_WH126 = (0.155787, 1.139701, -0.191276)
A1071_N20_NULL_MED_CASH = 0.105068
A1093_EDGE = {                                   # 1093's committed null.csv, the 3 shared rungs
    ("B136", 21): {5: 8.074181, 8: 4.841524, 10: 5.543762},
    ("B136", 63): {5: 11.268996, 8: 8.822182, 10: 7.662768},
    ("B136", 126): {5: 5.717069, 8: 5.244527, 10: 8.323841},
    ("U56", 21): {5: 5.930208, 8: 6.162706, 10: 7.319234},
    ("U56", 63): {5: 6.598641, 8: 8.029465, 10: 6.776615},
    ("U56", 126): {5: 5.954659, 8: 5.295494, 10: 6.163594},
}
A1093_B136_ARGMAX = {21: 5, 42: 5, 52: 5, 63: 5, 76: 5, 90: 5, 126: 10}
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
    """1082's recipe verbatim — deliberately carries NO H term."""
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
    """Same machinery, random ranks, NO eligibility gate (the record's convention)."""
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


def lam_rebuilt(f, sl, target_dd, hi=1.0):
    """Largest lam <= hi whose REBUILT |MaxDD| does not exceed the book's.  Returns None when the
    draw is already drier than the book at lam = hi (i.e. the clip binds)."""
    if abs(maxdd(f(hi)[sl])) <= abs(target_dd):
        return None
    a, b = 1e-4, hi
    for _ in range(BISECT):
        m = 0.5 * (a + b)
        if abs(maxdd(f(m)[sl])) > abs(target_dd):
            b = m
        else:
            a = m
    return 0.5 * (a + b)


def main():
    t0 = time.time()
    P(f"# Idea 1172 (lane C, {DATE}) — is the EDGE LADDER TRUNCATED at n=5, or does an INTERIOR")
    P("# PEAK exist BELOW it?")
    P(f"# 2 tuned dials: N {NS} x H {HS}.  ALL 49 cells per panel reported (98 total).")
    P(f"# FROZEN (not dials): SEEDS {NSEED}, cap {CAPNAME}, CAND20 legs {LEGS}, max_vol {MAXVOL}, "
      f"gross {GROSS0}, cost {COST:.0f} bps, LAG {LAG}, cadence {FREQ}.")
    P(f"# EDGE HOLDS (1093's B136 left-end-argmax set, pre-declared): {EDGE_HOLDS}.  H=126 and the")
    P("# whole U56 panel are CONTROLS.")
    P("# DECLARED BEFORE ANY NUMBER — scored on B136 over the six EDGE HOLDS:")
    P("#   (A) INTERIOR PEAK AT n=5      : argmax = 5 at >= 4 of 6")
    P("#   (B) STILL TRUNCATED           : argmax = 1 at >= 4 of 6")
    P("#   (C) NEW INTERIOR PEAK ELSEWHERE: argmax in {2,3,4,8} at >= 4 of 6")
    P("#   (D) NOT RESOLVABLE            : no single rung reaches 4 of 6")
    P(f"# EDGE (lambda clipped at 1.0) is the headline for comparability; EDGE_SYM (lambda up to")
    P(f"#   {LAMMAX}) releases the clip UPWARD and is published at every cell, because walking n")
    P("#   down deepens the book's DD and makes the clip bind on more draws — a mechanism that")
    P("#   manufactures a left-end peak.  EDGE_SYM is a measurement control, NOT a book.")
    P("# EDGE IS NOT A KEEP PATH: 4a/4b scored at all 98 cells; rule 8 picks (n,H) on 2009-2016.")
    P("")

    rows, nullrows, gaterows, seedrows = [], [], [], []
    picks, benchrows, bootrows = [], [], []
    gates = {}
    seedmat = {}          # (panel, N, H) -> np.array of NSEED null CAGRs (REBUILT, clip at 1)
    seedmat_sym = {}      # ditto, clip at LAMMAX

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
            gates["G2 CROSS-RUN vs 936/1071/1082/1086/1093's committed W/H126 N=20 triple"] = (
                d2, d2 < 5e-3)
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
            dds = [abs(maxdd(fn0(l)[warm])) for l in np.linspace(0.1, LAMMAX, 30)]
            viol = float(max(0.0, max(dds[i] - dds[i + 1] for i in range(len(dds) - 1))))
            gates[f"G4c |MaxDD| of the REBUILT null is monotone in lambda over [0.1, {LAMMAX}] "
                  "(EDGE_SYM's bisection is well posed)"] = (viol, viol < 1e-12)
            rngd = np.random.default_rng(mdseed(panel, 20, CAPNAME, 0))
            Wn0b, _ = build_null(rngd.random((T, K)), priced, reb, 20, 126, T, K, GROSS0)
            d7 = float(np.abs(Wn0 - Wn0b).max())
            gates["G7 null draw is deterministic in its seed recipe"] = (d7, d7 == 0.0)
            W1, ns1 = build(rank_key, elig, priced, reb, 1, 63, T, K, GROSS0)
            gates["G9 the N=1 book really holds ONE name at every rebalance date"] = (
                float(ns1.max()), int(ns1.max()) == 1 and int(ns1.min()) == 1)
            gsum = W1.sum(axis=1)
            d9b = float(np.abs(gsum[gsum > 0] - GROSS0).max())
            gates["G9b the N=1 book's gross is exactly GROSS0 when invested"] = (d9b, d9b < 1e-12)

        # ---- the grid --------------------------------------------------------------------
        for N in NS:
            rankmats = [np.random.default_rng(mdseed(panel, N, CAPNAME, s)).random((T, K))
                        for s in range(NSEED)]
            for H in HS:
                W, nsel = build(rank_key, elig, priced, reb, N, H, T, K, GROSS0)
                g, tn, _ = nrun(rets, lagmat(W), mkl)
                r = g - tn * COST / 1e4
                b = blocks(r, warm, ins, oos)
                l4b, l4a, l4bo = legs_4b(b, sb), legs_4a(b, lb), legs_4b_oos(b, sb)
                row = dict(panel=panel, N=N, H=H, cap=CAPNAME, mean_nsel=float(nsel.mean()),
                           max_nsel=int(nsel.max()),
                           zero_nsel_share=float((nsel == 0).mean()),
                           turnover=float(tn[warm].sum() / (warm.sum() / 252.0)), **b,
                           **l4b, **l4a, **l4bo,
                           pass4b=all(l4b.values()), pass4a=all(l4a.values()),
                           pass4b_oos=all(l4bo.values()))
                row["pass4b_full_and_oos"] = row["pass4b"] and row["pass4b_oos"]

                c_cash, c_reb, c_is, c_sym = [], [], [], []
                lam_c, lam_r, lam_s = [], [], []
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
                    lr = lam_rebuilt(fn, warm, b["MaxDD"], hi=1.0)
                    if lr is None:
                        c_reb.append(fmet(rn)[0]); lam_r.append(1.0)
                    else:
                        c_reb.append(fmet(fn(lr)[warm])[0]); lam_r.append(lr)
                    ls = lam_rebuilt(fn, warm, b["MaxDD"], hi=LAMMAX)
                    if ls is None:
                        c_sym.append(fmet(fn(LAMMAX)[warm])[0]); lam_s.append(LAMMAX)
                    else:
                        c_sym.append(fmet(fn(ls)[warm])[0]); lam_s.append(ls)
                    lri = lam_rebuilt(fn, ins, b["IS_MaxDD"], hi=1.0)
                    c_is.append(fmet(base[ins] if lri is None else fn(lri)[ins])[0])
                    seedrows.append(dict(panel=panel, N=N, H=H, seed=s,
                                         null_CAGR_cash=c_cash[-1], null_CAGR_rebuilt=c_reb[-1],
                                         null_CAGR_sym=c_sym[-1],
                                         null_IS_CAGR_rebuilt=c_is[-1],
                                         lam_cash=lam_c[-1], lam_rebuilt=lam_r[-1],
                                         lam_sym=lam_s[-1]))
                c_cash = np.array(c_cash); c_reb = np.array(c_reb)
                c_is = np.array(c_is); c_sym = np.array(c_sym)
                seedmat[(panel, N, H)] = c_reb.copy()
                seedmat_sym[(panel, N, H)] = c_sym.copy()
                med_reb = float(np.median(c_reb))
                med_sym = float(np.median(c_sym))
                nullrows.append(dict(
                    panel=panel, N=N, H=H, cap=CAPNAME, seeds=NSEED,
                    book_CAGR=b["CAGR"], book_MaxDD=b["MaxDD"], book_IS_CAGR=b["IS_CAGR"],
                    null_CAGR_med_rebuilt=med_reb,
                    null_CAGR_med_sym=med_sym,
                    null_CAGR_med_cash=float(np.median(c_cash)),
                    null_IS_CAGR_med_rebuilt=float(np.median(c_is)),
                    EDGE_pp=100.0 * (b["CAGR"] - med_reb),
                    EDGE_sym_pp=100.0 * (b["CAGR"] - med_sym),
                    EDGE_pp_cash=100.0 * (b["CAGR"] - float(np.median(c_cash))),
                    EDGE_IS_pp=100.0 * (b["IS_CAGR"] - float(np.median(c_is))),
                    null_CAGR_sd=float(c_reb.std(ddof=1)),
                    EDGE_se_pp=100.0 * 1.2533 * float(c_reb.std(ddof=1)) / np.sqrt(NSEED),
                    EDGE_sym_se_pp=100.0 * 1.2533 * float(c_sym.std(ddof=1)) / np.sqrt(NSEED),
                    book_pct_of_null=float((c_reb < b["CAGR"]).mean()),
                    lam_median_rebuilt=float(np.median(lam_r)),
                    lam_median_sym=float(np.median(lam_s)),
                    lam_median_cash=float(np.median(lam_c)),
                    null_already_drier_rebuilt=int(sum(1 for x in lam_r if x == 1.0)),
                    null_clipped_at_lammax=int(sum(1 for x in lam_s if x == LAMMAX)),
                    conv_gap_pp=100.0 * (med_reb - float(np.median(c_cash))),
                ))
                row["EDGE_pp"] = 100.0 * (b["CAGR"] - med_reb)
                row["EDGE_sym_pp"] = 100.0 * (b["CAGR"] - med_sym)
                row["EDGE_pp_cash"] = 100.0 * (b["CAGR"] - float(np.median(c_cash)))
                row["EDGE_IS_pp"] = 100.0 * (b["IS_CAGR"] - float(np.median(c_is)))
                row["book_pct_of_null"] = float((c_reb < b["CAGR"]).mean())
                row["drier_share"] = float(sum(1 for x in lam_r if x == 1.0)) / NSEED
                rows.append(row)
                P(f"   N={N:2d} H={H:3d} done  book {b['CAGR']:.2%} / {b['Sharpe']:.4f} / "
                  f"{b['MaxDD']:.2%}  turn {row['turnover']:.2f}x  "
                  f"EDGE {row['EDGE_pp']:+.3f} pp  SYM {row['EDGE_sym_pp']:+.3f} pp  "
                  f"drier {row['drier_share']:.2f}  ({time.time()-t0:.0f}s)")

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

    # ---- cross-run gates on the shared rungs ---------------------------------------------
    d5 = 0.0
    for (p_, H_), vals in A1093_EDGE.items():
        s = nul[(nul.panel == p_) & (nul.H == H_)].set_index("N")
        for n_, v_ in vals.items():
            d5 = max(d5, abs(float(s.loc[n_, "EDGE_pp"]) - v_))
    gates["G5 CROSS-RUN 1093's committed EDGE at the 3 shared rungs n in {5,8,10} x "
          "H in {21,63,126}, both panels (the premise itself)"] = (d5, d5 < 5e-3)
    gates["G5b the shared-rung reproduction covers BOTH panels and all 18 cells"] = (
        float(len(A1093_EDGE) * 3), len(A1093_EDGE) * 3 == 18)
    tspread = float(grid[grid.panel == "B136"].turnover.max()
                    - grid[grid.panel == "B136"].turnover.min())
    gates["G8 the dials are LIVE (B136 turnover spread >= 1.0x/yr across the grid)"] = (
        tspread, tspread >= 1.0)
    nspread = float(grid[grid.panel == "B136"].mean_nsel.min())
    gates["G8b the N=1 rung really is one name (min mean_nsel == 1.0)"] = (
        nspread, abs(nspread - 1.0) < 1e-12)

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
    P(f"## THE EXTENDED EDGE LADDER — the question itself ({NSEED} seeds, REBUILT, clip at 1.0)")
    argmax_obs, argmax_sym = {}, {}
    for panel in PANELS:
        P(f"   --- {panel} ---   EDGE(n, H) in pp    [* = one of 1093's EDGE HOLDS on B136]")
        P("        H  " + "".join(f"{n:>9d}" for n in NS)
          + "     argmax   1093argmax   EDGE(1)-EDGE(5)   SE   sigmas")
        for H in HS:
            s = nul[(nul.panel == panel) & (nul.H == H)].set_index("N").reindex(NS)
            v, se = s.EDGE_pp.values, s.EDGE_se_pp.values
            am = int(s.EDGE_pp.idxmax())
            argmax_obs[(panel, H)] = am
            d15 = float(v[NS.index(1)] - v[NS.index(5)])
            se15 = float(np.hypot(se[NS.index(1)], se[NS.index(5)]))
            star = "*" if (panel == "B136" and H in EDGE_HOLDS) else " "
            P(f"     {star}{H:3d}  " + "".join(f"{x:>+9.3f}" for x in v)
              + f"     n={am:<3d}     n={A1093_B136_ARGMAX[H] if panel=='B136' else '-':<3}"
              + f"      {d15:+8.3f} pp    {se15:.3f}  {d15/se15:+6.2f}")
        P("        SE  " + "".join(
            f"{x:>9.3f}" for x in nul[(nul.panel == panel) & (nul.H == 63)]
            .set_index("N").reindex(NS).EDGE_se_pp.values) + "     (seed SE at H=63)")

    P("")
    P(f"## THE SAME LADDER UNDER THE SYMMETRIC MATCH — clip released to lambda <= {LAMMAX}")
    P("   (a null drier than the book is LEVERED to the book's drawdown instead of entering")
    P("    understated.  A measurement control, not a book.)")
    for panel in PANELS:
        P(f"   --- {panel} ---   EDGE_SYM(n, H) in pp")
        P("        H  " + "".join(f"{n:>9d}" for n in NS) + "     argmax   agrees with EDGE?")
        for H in HS:
            s = nul[(nul.panel == panel) & (nul.H == H)].set_index("N").reindex(NS)
            v = s.EDGE_sym_pp.values
            am = int(s.EDGE_sym_pp.idxmax())
            argmax_sym[(panel, H)] = am
            P(f"      {H:3d}  " + "".join(f"{x:>+9.3f}" for x in v)
              + f"     n={am:<3d}    {'YES' if am == argmax_obs[(panel, H)] else 'NO'}")

    P("")
    P(f"## THE SEED BOOTSTRAP — is the argmax a lucky draw?  ({NBOOT:,} resamples of the "
      f"{NSEED} seeds, independent across n)")
    rng = np.random.default_rng(BOOT_SEED)
    for panel in PANELS:
        bookNH = {(N, H): float(nul[(nul.panel == panel) & (nul.N == N) & (nul.H == H)]
                                .book_CAGR.iloc[0]) for N in NS for H in HS}
        idxs = {N: rng.integers(0, NSEED, size=(NBOOT, NSEED)) for N in NS}
        P(f"   --- {panel} ---")
        P("        H   P(argmax=1)  P(argmax=5)  P(argmax INTERIOR)  P(monotone DEC)  "
          "90% argmax set")
        for H in HS:
            M = np.empty((NBOOT, len(NS)))
            for j, N in enumerate(NS):
                draws = seedmat[(panel, N, H)][idxs[N]]
                M[:, j] = 100.0 * (bookNH[(N, H)] - np.median(draws, axis=1))
            am = np.array(NS)[M.argmax(axis=1)]
            p1 = float((am == 1).mean())
            p5 = float((am == 5).mean())
            pobs = float((am == argmax_obs[(panel, H)]).mean())
            pint = float((~np.isin(am, [NS[0], NS[-1]])).mean())
            pm = float((np.diff(M, axis=1) <= 0).all(axis=1).mean())
            vals, cnts = np.unique(am, return_counts=True)
            order = np.argsort(-cnts)
            cum, keep = 0, []
            for o in order:
                keep.append(int(vals[o])); cum += cnts[o]
                if cum >= 0.90 * NBOOT:
                    break
            P(f"      {H:3d}      {p1:7.3f}      {p5:7.3f}           {pint:7.3f}          "
              f"{pm:7.3f}       " + "{" + ",".join(str(x) for x in sorted(keep)) + "}"
              + f"   P(argmax=observed n={argmax_obs[(panel, H)]}) = {pobs:.3f}")
            bootrows.append(dict(panel=panel, H=H, P_argmax_1=p1, P_argmax_5=p5,
                                 P_argmax_observed=pobs,
                                 P_argmax_interior=pint, P_monotone_dec=pm,
                                 observed_argmax=argmax_obs[(panel, H)],
                                 observed_argmax_sym=argmax_sym[(panel, H)],
                                 argmax_set_90="{" + ",".join(str(x) for x in sorted(keep)) + "}"))

    P("")
    P("## WHAT A ONE-NAME BOOK ACTUALLY COSTS — the capital side of the same ladder")
    for panel in PANELS:
        P(f"   --- {panel} ---")
        P("        n   mean CAGR   mean MaxDD   mean Sharpe   worst MaxDD   4b passes   turn")
        for N in NS:
            s = grid[(grid.panel == panel) & (grid.N == N)]
            P(f"      {N:3d}    {s.CAGR.mean():7.2%}     {s.MaxDD.mean():7.2%}      "
              f"{s.Sharpe.mean():6.3f}       {s.MaxDD.min():7.2%}        {int(s.pass4b.sum())}/"
              f"{len(s)}     {s.turnover.mean():5.2f}x")
        sp = bn[(bn.panel == panel) & (bn.series == "SPY")].iloc[0]
        P(f"      SPY    {sp.CAGR:7.2%}     {sp.MaxDD:7.2%}      {sp.Sharpe:6.3f}"
          f"       (4b DD cap {DD_CAP*abs(sp.MaxDD):.2%}, CAGR floor {CAGR_FLOOR*sp.CAGR:.2%})")

    P("")
    P("## RULE 8 — IS(2009-2016)-only choosers pick (N, H) over 49 cells, OOS(2017-2026) ONCE")
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

    def bq(panel, H, col):
        return float(bootd[(bootd.panel == panel) & (bootd.H == H)][col].iloc[0])

    n_at1 = sum(1 for H in EDGE_HOLDS if argmax_obs[("B136", H)] == 1)
    n_at5 = sum(1 for H in EDGE_HOLDS if argmax_obs[("B136", H)] == 5)
    n_int = sum(1 for H in EDGE_HOLDS if argmax_obs[("B136", H)] not in (NS[0], NS[-1]))
    n_new = sum(1 for H in EDGE_HOLDS if argmax_obs[("B136", H)] in (2, 3, 4, 8))

    g5key = ("G5 CROSS-RUN 1093's committed EDGE at the 3 shared rungs n in {5,8,10} x "
             "H in {21,63,126}, both panels (the premise itself)")
    H_.append(("H_REP the three rungs this run shares with 1093 reproduce its committed EDGE to "
               "< 5e-3 pp at all 18 shared cells (the premise is the same object)",
               bool(gates[g5key][1]), f"max |d| = {gates[g5key][0]:.2e} pp over 18 cells"))
    H_.append(("H_INTERIOR the B136 argmax is INTERIOR (not at either end of the extended "
               "ladder) at >= 4 of the 6 EDGE HOLDS",
               bool(n_int >= 4),
               f"{n_int} of 6 interior; argmax path "
               + ",".join(f"H{H}:{argmax_obs[('B136',H)]}" for H in EDGE_HOLDS)))
    H_.append(("H_NOT_ONE the B136 argmax is NOT at the NEW left end n=1 at >= 4 of the 6 EDGE "
               "HOLDS (the ladder was not merely truncated)",
               bool((6 - n_at1) >= 4), f"argmax = 1 at {n_at1} of 6"))
    H_.append(("H_FIVE 1093's rung SURVIVES the extension: argmax = 5 at >= 4 of the 6 EDGE HOLDS",
               bool(n_at5 >= 4), f"argmax = 5 at {n_at5} of 6"))
    H_.append(("H_BOOT the observed argmax survives its own seed noise: bootstrap P(argmax = the "
               "observed rung) >= 0.50 at >= 4 of the 6 EDGE HOLDS",
               bool(sum(1 for H in EDGE_HOLDS
                        if bq("B136", H, "P_argmax_observed") >= 0.50) >= 4),
               ", ".join(f"H{H}: n={argmax_obs[('B136',H)]} "
                         f"P={bq('B136',H,'P_argmax_observed'):.3f}" for H in EDGE_HOLDS)))
    drier_up = sum(1 for H in HS
                   if float(nul[(nul.panel == "B136") & (nul.H == H) & (nul.N == 1)]
                            .null_already_drier_rebuilt.iloc[0])
                   >= float(nul[(nul.panel == "B136") & (nul.H == H) & (nul.N == 10)]
                            .null_already_drier_rebuilt.iloc[0]))
    H_.append(("H_CLIP the lambda<=1 clip binds on MORE null draws as n falls (the predicted "
               "mechanism that could manufacture a left-end peak): drier share at n=1 >= that at "
               "n=10 at >= 5 of the 7 B136 holds",
               bool(drier_up >= 5), f"{drier_up} of 7 holds"))
    sym_agree = sum(1 for H in EDGE_HOLDS if argmax_sym[("B136", H)] == argmax_obs[("B136", H)])
    H_.append((f"H_SYM the SYMMETRIC match (lambda <= {LAMMAX}) gives the SAME B136 argmax at "
               ">= 4 of the 6 EDGE HOLDS (the peak is not the clip)",
               bool(sym_agree >= 4),
               f"{sym_agree} of 6 agree; SYM path "
               + ",".join(f"H{H}:{argmax_sym[('B136',H)]}" for H in EDGE_HOLDS)))
    conc = grid[grid.N <= 4]
    H_.append(("H_4B_CONC NO cell at n <= 4 clears 4b full-sample (concentration buys EDGE, not "
               "capital)", bool(not conc.pass4b.any()),
               f"{int(conc.pass4b.sum())} of {len(conc)} cells at n <= 4 pass 4b"))
    H_.append(("H_TURN turnover falls strictly as H lengthens at every (panel, N)",
               bool(all(grid[(grid.panel == p_) & (grid.N == n) & (grid.H == HS[i])].turnover.iloc[0]
                        > grid[(grid.panel == p_) & (grid.N == n) & (grid.H == HS[i + 1])].turnover.iloc[0]
                        for p_ in PANELS for n in NS for i in range(len(HS) - 1))),
               f"B136 turnover spread {tspread:.2f}x/yr"))
    H_.append(("H_WF >= 1 rule-8 pick clears 4b OUT OF SAMPLE",
               bool(pk.pass4b_oos.any()), f"{int(pk.pass4b_oos.sum())} of {len(pk)} picks"))
    H_.append(("H_4A no cell clears 4a", bool(not grid.pass4a.any()),
               f"{int(grid.pass4a.sum())} of {len(grid)} cells pass 4a"))
    for name, ok, note in H_:
        P(f"   {'PASS' if ok else 'FAIL'}  {name}  [{note}]")

    P("")
    P("## THE VERDICT ON THE QUEUE'S QUESTION, read off the PRE-DECLARED rules only")
    if n_at5 >= 4:
        lab = ("OUTCOME (A): INTERIOR PEAK AT n=5 — the ladder was NOT truncated; n=5 is an "
               "interior optimum")
    elif n_at1 >= 4:
        lab = ("OUTCOME (B): STILL TRUNCATED — no interior peak; EDGE rises into a ONE-NAME book "
               "and every published 'peak' in this family is a boundary")
    elif n_new >= 4:
        lab = ("OUTCOME (C): NEW INTERIOR PEAK ELSEWHERE — a peak exists, at a rung the record "
               "has not been quoting")
    else:
        lab = ("OUTCOME (D): NOT RESOLVABLE — no single rung reaches 4 of 6 EDGE HOLDS at "
               f"{NSEED} seeds")
    P(f"   {lab}")
    P(f"   B136 argmax over the 6 EDGE HOLDS: "
      + ", ".join(f"H={H}: n={argmax_obs[('B136', H)]}" for H in EDGE_HOLDS))
    P(f"   at n=1: {n_at1} of 6;  at n=5: {n_at5} of 6;  interior: {n_int} of 6")

    # ------------------------------------------------------------------ post-run diagnostics
    P("")
    P("## POST-RUN DIAGNOSTICS — computed AFTER reading the grid and labelled as such, NOT")
    P("## pre-declared hypotheses.")
    diagrows = []
    P("")
    P("   (D1) IS THE LEFT-END STEP DECISIVE?  EDGE at two cells differs only through the two")
    P("        null medians (the books are deterministic), so SE(dEDGE) = hypot(SEa, SEb).")
    for panel in PANELS:
        for H in HS:
            s = nul[(nul.panel == panel) & (nul.H == H)].set_index("N").reindex(NS)
            v, se = s.EDGE_pp.values, s.EDGE_se_pp.values
            nd = sum(1 for i in range(len(v) - 1)
                     if (v[i] - v[i + 1]) > 2 * np.hypot(se[i], se[i + 1]))
            nu = sum(1 for i in range(len(v) - 1)
                     if (v[i + 1] - v[i]) > 2 * np.hypot(se[i], se[i + 1]))
            P(f"        {panel} H={H:3d}: adjacent steps DECISIVELY DOWN {nd} of {len(v)-1}, "
              f"DECISIVELY UP {nu} of {len(v)-1}, rest inside 2 SE")
            diagrows.append(dict(diag="D1_steps", panel=panel, H=H, a=nd, b=nu,
                                 delta_pp=float(v[0] - v[-1]),
                                 se_pp=float(np.hypot(se[0], se[-1])),
                                 sigmas=float((v[0] - v[-1]) / np.hypot(se[0], se[-1])),
                                 decisive=bool(abs(v[0] - v[-1]) > 2 * np.hypot(se[0], se[-1]))))
    P("")
    P("   (D2) THE lambda <= 1 CLIP.  Share of the 40 null draws entering UNMATCHED because they")
    P("        are already drier than the book (which INFLATES EDGE), by (panel, H, n):")
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
    P(f"   (D3) THE SYMMETRIC MATCH's OWN CLIP at lambda = {LAMMAX}.  Share of draws still drier")
    P("        than the book at full leverage (EDGE_SYM is inflated at these cells too):")
    for panel in PANELS:
        for H in HS:
            s = nul[(nul.panel == panel) & (nul.H == H)].set_index("N").reindex(NS)
            P(f"        {panel} H={H:3d}: " + "  ".join(
                f"{n}:{v/NSEED:.2f}" for n, v in zip(NS, s.null_clipped_at_lammax.values)))
            for n, v in zip(NS, s.null_clipped_at_lammax.values):
                diagrows.append(dict(diag="D3_lammax_share", panel=panel, H=H, a=n, b=np.nan,
                                     delta_pp=np.nan, se_pp=float(v) / NSEED, sigmas=np.nan,
                                     decisive=np.nan))
    P("")
    P("   (D4) THE 4b PASSES AND THEIR MARGIN ON THE BINDING LEG.")
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
        diagrows.append(dict(diag="D4_4b_pass", panel=r.panel, H=int(r.H), a=int(r.N), b=np.nan,
                             delta_pp=ddm, se_pp=cgm, sigmas=np.nan, decisive=bool(reachable)))
    P("        1083 measured the 90% width of a quantity of this kind at 4.1-7.2 pp on this tape;")
    P("        any DD margin far inside that is not decidable here.")
    P("")
    P("   (D5) WHY G9 AND G8b FAILED, and what the correct reading is.  BOTH gates were")
    P("        MIS-SPECIFIED by this run, not violated by the book: they demanded the N=1 book")
    P("        hold exactly one name at EVERY rebalance date, including the ones where the")
    P("        eligibility gate (200d MA and max_vol) admits NOBODY and the book is correctly in")
    P("        CASH.  The gates are left as published FAILs; the resolving numbers are here.")
    for panel in PANELS:
        s = grid[(grid.panel == panel) & (grid.N == 1)]
        P(f"        {panel} N=1: max names held = {int(s.max_nsel.max())} at every (N=1, H) cell; "
          f"share of rebalance dates holding ZERO (all-cash) = "
          f"{s.zero_nsel_share.min():.3f}-{s.zero_nsel_share.max():.3f}; mean names "
          f"{s.mean_nsel.min():.4f}-{s.mean_nsel.max():.4f}")
        diagrows.append(dict(diag="D5_nsel", panel=panel, H=np.nan, a=int(s.max_nsel.max()),
                             b=np.nan, delta_pp=np.nan, se_pp=float(s.zero_nsel_share.max()),
                             sigmas=float(s.mean_nsel.mean()), decisive=np.nan))
    P("        The N=1 book therefore NEVER holds two names; it holds one or none.  Every EDGE,")
    P("        CAGR and MaxDD figure at n=1 above is that object, and its null is built by the")
    P("        same machinery with the same all-cash dates, so the contrast is like for like.")
    P("")
    P("   (D6) G3 (SPY OOS triple) failed at |d| = 2.894e-03 — the SAME value 1093 published on")
    P("        the same day.  The committed anchor (0.1521 / 0.8713 / -0.3372) predates the")
    P("        2026-09-16 close now in data/prices.csv; the discrepancy is one extra tape day,")
    P("        not a construction difference, and this run reproduces 1093's failure exactly.")

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

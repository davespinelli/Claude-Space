#!/usr/bin/env python3
"""Idea 1064 (cloud lane, 2026-09-16) — is W/H126 a TURNOVER-FREE ROUTE to the MONTHLY BOOK, or a
DIFFERENT BOOK?

QUESTION (QUEUE idea 1064, verbatim)
    idea 936 found the weekly book at min hold 126 reaches 15.58% CAGR on 2.90 turns/yr against
    the monthly book's 15.26% on 4.77, passes 4b, and fails 4a on drawdown (-19.13% vs the live
    -12.05%).  Measure the overlap between the two books' holdings day by day and report whether
    W/H126 is the monthly book reached by another route (overlap near 1) or a genuinely different
    portfolio, and whether a gross rung below 0.75 brings its drawdown inside the live book's
    while keeping 4b.  Max 2 params (gross rung, overlap statistic).

THE TWO DIALS (rule 4, no more than two tuned parameters)
    1. GROSS RUNG   g in {0.75, 0.65, 0.55, 0.45, 0.35}.  0.75 is 936/968/1059's convention and is
       the top of the ladder; everything below it is un-invested CASH (never leverage).
    2. OVERLAP STATISTIC  in {JACCARD, OVERLAP_COEF, WEIGHT_L1}, all three reported at every
       point.  A fourth quantity, the two books' daily NET RETURN CORRELATION, is printed as a
       DIAGNOSTIC of the same object in a different currency, not as a third dial.
    Fixed, NOT dials: NTOP 20, max_vol 0.60, cost 10 bps (PROTOCOL rule 2), LAG 1, the CAND20
    mechanism and the canonical period-end rebalance dates (936's construction verbatim).  The
    books themselves (W/H126, M/H0, W/H0) are the OBJECTS under test, fixed by the queue text.

WHAT IS DECLARED BEFORE ANY NUMBER IS COMPUTED
    (a) The overlap statistic is invariant to the gross rung by construction, because g scales
        every weight uniformly.  The two dials are therefore orthogonal, which is gated (G6), and
        the ladder cannot be used to buy an overlap reading.
    (b) READING RULE for the queue's question, fixed in advance:
          SAME BOOK BY ANOTHER ROUTE  if median JACCARD >= 0.80 AND net-return rho >= 0.95
          DIFFERENT PORTFOLIO         if median JACCARD <= FLOOR + 0.10
          PARTIAL                     otherwise, reported as where on [FLOOR, 1] it sits.
        FLOOR is the i.i.d.-ranking null's own W/H126-vs-M/H0 overlap, and it is also computable
        in closed form for two independent uniform 20-of-K subsets (E[J] = 20/(2K-20) -> 0.217 on
        U56, 0.081 on B136); both are reported.
        The comparand that matters is not only the floor but the CADENCE-ONLY anchor W/H0-vs-M/H0:
        if W/H126-vs-M/H0 is no lower than that, the min-hold constraint has taken the book
        nowhere the ordinary weekly book was not already.
    (c) The gross ladder is ARITHMETIC, not skill: with cash at 0% both the mean and the vol of a
        book's return scale by g, so SHARPE IS INVARIANT ALONG THE LADDER and |MaxDD| falls
        roughly linearly.  A rung therefore cannot be chosen on Sharpe, and any 4a pass it buys is
        bought by holding cash, not by selecting better.  The refutable claim is that the SAME
        de-grossing hands 4a to the gross-matched NULL and to the monthly incumbent as well; if it
        does, 4a's drawdown leg is a gross dial and not a property of the book.

RULE 8.  Every gross rung is scored IS (2009-2016) and read once OOS (2017-2026), against SPY and
    against the live RULES v2 book at the same 10 bps rung.  Two IS-only choosers (C_ISSHARPE,
    C_ISDD) pick a rung on the first half alone; the OOS CAGR/Sharpe/MaxDD of what they pick is
    reported against the default rung, against the baseline and against SPY.

SURVIVORSHIP.  U56 and B136 are current-constituent panels.  The bias is common to the books and
    to the null and flatters both the CAGR floor and the DD cap against SPY, which is a real index.
"""
from __future__ import annotations

import hashlib
import sys
import time
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-16"
SLUG = "is-W-H126-a-TURNOVER-FREE-ROUTE-to-the-MONTHLY-BOOK-or-a-DIFFERENT-BOOK"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

LAG = 1
WARMUP = 260
NTOP = 20
MAXVOL = 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST = 10.0
GROSS0 = 0.75

# ---- the two tuned dials -----------------------------------------------------------------------
GROSSES = [0.75, 0.65, 0.55, 0.45, 0.35]
STATS = ["JACCARD", "OVERLAP_COEF", "WEIGHT_L1"]

PANELS = ["U56", "B136"]
# the objects under test, fixed by the queue text (f, H)
BOOKS = {"W/H126": ("W", 126), "M/H0": ("M", 0), "W/H0": ("W", 0), "M/H5": ("M", 5)}
PAIRS = [("W/H126", "M/H0"), ("W/H0", "M/H0"), ("W/H126", "W/H0"), ("M/H0", "M/H5")]
MECHS = ["CAND20", "R3_84", "MOMONLY"]
LEGSETS = {"CAND20": [(21, 252), (0, 126), (0, 63)],
           "R3_84": [(21, 252), (0, 126), (0, 84)],
           "MOMONLY": [(21, 252)]}
NSEED = 20

# committed cross-run anchors (idea 936 grid.csv, U56/CAND20/0.75/10bps; idea 1059 census)
A936 = {"W/H126": (0.155787, 1.139701, -0.191276, 2.897),
        "M/H0": (0.152627, 1.212106, -0.195069, 4.771),
        "W/H0": (0.127272, 1.060652, -0.183084, 10.792)}
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205        # RULES v2 live book, committed in 936's queue text
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
    return int(hashlib.md5("|".join(str(x) for x in parts).encode()).hexdigest()[:8], 16)


def nrun(rets, wt, mk):
    """GROSS returns and turnover; cost applied outside (gated at G1 against engine.backtest).
    Construction copied verbatim from idea 936's cloud script so the two runs are comparable."""
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


def lag(a):
    out = np.zeros_like(a)
    out[LAG:] = a[:-LAG]
    return out


def lagmask(m):
    out = np.zeros_like(m)
    out[LAG:] = m[:-LAG]
    return out


def legs_composite(px, legs):
    parts = []
    for skip, look in legs:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return sum(parts) / len(parts)


def mech_score(px, mech):
    """961/968/1059/936's selection score (higher = better) and the eligibility gate."""
    comp = legs_composite(px, LEGSETS[mech])
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))      # no vol scaler (KEEP 4b convention)
    elig = (above & (vol20 < MAXVOL)).values
    return sc.values, elig


def minhold_weights(rank_key, elig, priced, reb, H, T, N):
    """Gross-1.0 target weights under a MIN-HOLD constraint (idea 936's construction verbatim)."""
    W = np.zeros((T, N))
    cur = np.full(N, -1, dtype=np.int64)
    for i, t in enumerate(reb):
        held = np.flatnonzero(cur >= 0)
        if len(held):
            young = held[(t - cur[held]) < H]
            young = young[priced[t, young]]
        else:
            young = held
        keep = set(young.tolist())
        need = NTOP - len(keep)
        if need > 0:
            k = rank_key[t].copy()
            k[~(elig[t] & priced[t])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        else:
            take = []
        new_cur = np.full(N, -1, dtype=np.int64)
        for c in keep:
            new_cur[c] = cur[c]
        for c in take:
            new_cur[c] = t
        cur = new_cur
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = 1.0 / len(sel)
    return W


def blocks(r, warm, oos):
    rr = r[warm]
    c, s, d = fmet(rr)
    h = len(rr) // 2
    o = r[oos]
    oc, os_, od = fmet(o)
    ii = r[warm & ~oos]
    ic, is_, idd = fmet(ii)
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]),
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od,
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd)


def legs_4b(b, sb):
    return {"L_H1": bool(b["H1"] > sb["H1"]), "L_H2": bool(b["H2"] > sb["H2"]),
            "L_OOS": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "L_DD": bool(abs(b["MaxDD"]) <= DD_CAP * abs(sb["MaxDD"])),
            "L_CAGR": bool(b["CAGR"] >= CAGR_FLOOR * sb["CAGR"])}


def legs_4a(b, lb):
    """PROTOCOL 4a against the LIVE RULES v2 book: Sharpe higher in BOTH halves and MaxDD no
    worse (MaxDD is negative, so 'no worse' is book >= live)."""
    return {"A_H1": bool(b["H1"] > lb["H1"]), "A_H2": bool(b["H2"] > lb["H2"]),
            "A_DD": bool(b["MaxDD"] >= lb["MaxDD"])}


def legs_4b_oos(b, sb):
    return {"O_S": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "O_DD": bool(abs(b["OOS_MaxDD"]) <= DD_CAP * abs(sb["OOS_MaxDD"])),
            "O_CAGR": bool(b["OOS_CAGR"] >= CAGR_FLOOR * sb["OOS_CAGR"])}


def overlaps(WA, WB, sel):
    """All three overlap statistics, day by day, on the rows selected by `sel`.
    WA/WB are step weight matrices at the SAME gross (the statistics are gross-invariant)."""
    A, B = WA[sel] > 0, WB[sel] > 0
    nA, nB = A.sum(1), B.sum(1)
    inter = (A & B).sum(1)
    union = (A | B).sum(1)
    both = (nA > 0) & (nB > 0)
    jac = np.where(union > 0, inter / np.maximum(union, 1), np.nan)
    ovc = np.where(both, inter / np.maximum(np.minimum(nA, nB), 1), np.nan)
    a = WA[sel] / np.maximum(WA[sel].sum(1, keepdims=True), 1e-12)
    b = WB[sel] / np.maximum(WB[sel].sum(1, keepdims=True), 1e-12)
    wl1 = np.where(both, 1.0 - 0.5 * np.abs(a - b).sum(1), np.nan)
    return {"JACCARD": jac, "OVERLAP_COEF": ovc, "WEIGHT_L1": wl1}


def summ(d, tag):
    out = {}
    for k, v in d.items():
        v = np.asarray(v, float)
        v = v[~np.isnan(v)]
        out[f"{tag}_{k}_median"] = float(np.median(v)) if len(v) else np.nan
        out[f"{tag}_{k}_mean"] = float(v.mean()) if len(v) else np.nan
        out[f"{tag}_{k}_p10"] = float(np.percentile(v, 10)) if len(v) else np.nan
        out[f"{tag}_{k}_p90"] = float(np.percentile(v, 90)) if len(v) else np.nan
    return out


def main():
    t0 = time.time()
    P(f"# Idea 1064 (cloud lane, {DATE}) — is W/H126 a TURNOVER-FREE ROUTE to the MONTHLY BOOK "
      f"or a DIFFERENT BOOK?")
    P(f"# 2 tuned dials: GROSS RUNG {GROSSES} x OVERLAP STATISTIC {STATS}. ALL points reported.")
    P(f"# Fixed (NOT dials): NTOP {NTOP}, max_vol {MAXVOL}, cost {COST:.0f} bps, LAG {LAG}, "
      f"CAND20 mechanism, canonical period-end dates; books W/H126, M/H0, W/H0 fixed by the "
      f"queue text.  R3_84 / MOMONLY are a REPLICATION of the overlap reading, not a dial.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   (a) overlap is gross-invariant by construction (gated G6) -> the dials are orthogonal;")
    P("#   (b) SAME-BOOK if median JACCARD >= 0.80 and net-return rho >= 0.95; DIFFERENT if")
    P("#       median JACCARD <= FLOOR + 0.10; PARTIAL otherwise. The cadence-only anchor is")
    P("#       W/H0-vs-M/H0: if W/H126 is no further from M than W already was, min hold moved")
    P("#       the book nowhere;")
    P("#   (c) the gross ladder is ARITHMETIC: Sharpe is invariant along it and |MaxDD| falls")
    P("#       ~linearly, so any 4a it buys is bought with CASH. The refutable claim is that the")
    P("#       same de-grossing hands 4a to the NULL and to the monthly incumbent too.")
    P(f"# NSEED = {NSEED} gross-matched i.i.d.-ranking nulls per panel, paired across the two")
    P("#   routes from ONE permutation stream per (panel, seed).")
    P("# SURVIVORSHIP: current-constituent panels; the bias is common to books and null.")
    P("")

    PXD = {"U56": load_universe(), "B136": load_universe(broad=True)}
    PAN = {}
    for p, px in PXD.items():
        idx = px.index
        rets = px.pct_change().fillna(0.0).values
        ar = np.arange(len(idx))
        warm = ar >= WARMUP
        oos = np.asarray(idx > pd.Timestamp(IS_END))
        spyr = px["SPY"].pct_change().fillna(0.0).values
        PAN[p] = dict(px=px, idx=idx, rets=rets, warm=warm, oos=oos & warm, T=len(idx),
                      N=px.shape[1], priced=px.notna().values, yrs=warm.sum() / 252.0,
                      spy=blocks(spyr, warm, oos & warm),
                      reb={f: np.flatnonzero(rebalance_mask(idx, f).values) for f in ("W", "M")},
                      mask={f: rebalance_mask(idx, f).values for f in ("W", "M")})
        P(f"  {p}: {px.shape[1]} cols x {len(idx)} days, {idx[0].date()} -> {idx[-1].date()}; "
          f"SPY full {PAN[p]['spy']['CAGR']:.2%} / {PAN[p]['spy']['Sharpe']:.4f} / "
          f"{PAN[p]['spy']['MaxDD']:.2%}, OOS {PAN[p]['spy']['OOS_CAGR']:.2%} / "
          f"{PAN[p]['spy']['OOS_Sharpe']:.4f} / {PAN[p]['spy']['OOS_MaxDD']:.2%}")

    SCORE = {}
    for p, m in product(PANELS, MECHS):
        sc, el = mech_score(PXD[p], m)
        with np.errstate(invalid="ignore"):
            key = -np.nan_to_num(sc, nan=-np.inf)
        key[np.isnan(sc)] = np.inf
        SCORE[(p, m)] = (key, el)

    PERM = {}
    for p, s in product(PANELS, range(NSEED)):
        rng = np.random.default_rng(mdseed("PERM1064", p, s, PAN[p]["T"], PAN[p]["N"]))
        PERM[(p, s)] = rng.random((PAN[p]["T"], PAN[p]["N"])).astype(np.float32)

    # gross-1.0 step weights for every (panel, mech, book) and for every (panel, seed, book)
    WB1 = {}
    for p, m in product(PANELS, MECHS):
        for bname, (f, H) in BOOKS.items():
            WB1[(p, m, bname)] = minhold_weights(*SCORE[(p, m)], PAN[p]["priced"],
                                                 PAN[p]["reb"][f], H, PAN[p]["T"], PAN[p]["N"])
    WN1 = {}
    for p, s in product(PANELS, range(NSEED)):
        el = np.ones_like(PAN[p]["priced"])
        for bname, (f, H) in BOOKS.items():
            WN1[(p, s, bname)] = minhold_weights(PERM[(p, s)], el, PAN[p]["priced"],
                                                 PAN[p]["reb"][f], H, PAN[p]["T"], PAN[p]["N"])
    P(f"  built {len(WB1)} book weight matrices + {len(WN1)} null ones "
      f"[{time.time()-t0:.0f}s]")

    # the LIVE RULES v2 book (gross 0.75, weekly, 10 bps) on each panel
    LIVE = {}
    for p in PANELS:
        lv = backtest(PXD[p], rules_v2_weights(PXD[p]), cost_bps=COST, freq="W")
        LIVE[p] = blocks(lv["returns"].values, PAN[p]["warm"], PAN[p]["oos"])
        LIVE[p]["turn_yr"] = float(lv["turnover"].values[PAN[p]["warm"]].sum() / PAN[p]["yrs"])

    # ================================================================== GATES
    P("=" * 100)
    P("REPRODUCTION GATES")
    P("=" * 100)
    gates = {}

    pan = PAN["U56"]
    w1 = GROSS0 * WB1[("U56", "CAND20", "W/H126")]
    gr, tt = nrun(pan["rets"], lag(w1), lagmask(pan["mask"]["W"]))
    mine = gr - tt * COST / 1e4
    eng = backtest(PXD["U56"], pd.DataFrame(w1, index=pan["idx"], columns=PXD["U56"].columns),
                   cost_bps=COST, freq="W")
    d1 = float(np.abs(mine[WARMUP:] - eng["returns"].values[WARMUP:]).max())
    gates["G1"] = (d1 < 1e-12, f"OUTSIDE-cost runner == engine.backtest at {COST:.0f} bps on the "
                               f"W/H126 book: max|dret| {d1:.2e}")

    # G2: reproduce idea 936's three committed U56/CAND20 books at gross 0.75
    d2, det = 0.0, []
    for bname in ("W/H126", "M/H0", "W/H0"):
        f = BOOKS[bname][0]
        W = GROSS0 * WB1[("U56", "CAND20", bname)]
        g_, t_ = nrun(pan["rets"], lag(W), lagmask(pan["mask"][f]))
        r = g_ - t_ * COST / 1e4
        c, s, dd = fmet(r[pan["warm"]])
        ty = float(t_[pan["warm"]].sum() / pan["yrs"])
        a = A936[bname]
        dd_ = max(abs(c - a[0]), abs(s - a[1]), abs(dd - a[2]), abs(ty - a[3]) / a[3])
        d2 = max(d2, dd_)
        det.append(f"{bname} {c:.4%}/{s:.4f}/{dd:.2%}/{ty:.2f}pa vs "
                   f"{a[0]:.4%}/{a[1]:.4f}/{a[2]:.2%}/{a[3]:.2f}pa")
    gates["G2"] = (d2 < 5e-3, "CROSS-RUN reproduces idea 936's committed U56/CAND20 books at "
                              f"gross {GROSS0}: " + "; ".join(det) + f"  max|d| {d2:.2e}")

    sp = PAN["U56"]["spy"]
    d3 = max(abs(sp["OOS_CAGR"] - SPY_OOS_COMMITTED[0]), abs(sp["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
             abs(sp["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gates["G3"] = (d3 < 5e-4, f"CROSS-RUN SPY OOS at {IS_END}: {sp['OOS_CAGR']:.4f} / "
                              f"{sp['OOS_Sharpe']:.4f} / {sp['OOS_MaxDD']:.4f} vs committed "
                              f"{SPY_OOS_COMMITTED} (max|d| {d3:.2e})")

    d4 = abs(LIVE["U56"]["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gates["G4"] = (d4 < 2e-3, f"the LIVE RULES v2 book reproduces its committed MaxDD: "
                              f"{LIVE['U56']['MaxDD']:.2%} vs {LIVE_MAXDD_COMMITTED:.2%} "
                              f"(|d| {d4:.2e}); live full {LIVE['U56']['CAGR']:.2%} / "
                              f"{LIVE['U56']['Sharpe']:.4f}, halves {LIVE['U56']['H1']:.3f} / "
                              f"{LIVE['U56']['H2']:.3f}, turnover {LIVE['U56']['turn_yr']:.2f}/yr")

    # G5: M/H0 == M/H5 identically (936's grid shows the same numbers) -> overlap ceiling 1.000
    o5 = overlaps(WB1[("U56", "CAND20", "M/H0")], WB1[("U56", "CAND20", "M/H5")], pan["warm"])
    c5 = min(float(np.nanmin(o5[s])) for s in STATS)
    gates["G5"] = (c5 > 0.999, "CEILING: the two books 936 reports as IDENTICAL (M/H0, M/H5) "
                               f"overlap at 1.000 on every statistic, every day (min {c5:.6f})")

    # G6: the overlap statistics are invariant to the gross rung (the two dials are orthogonal)
    d6 = 0.0
    for g in GROSSES:
        oa = overlaps(g * WB1[("U56", "CAND20", "W/H126")], g * WB1[("U56", "CAND20", "M/H0")],
                      pan["warm"])
        ob = overlaps(GROSS0 * WB1[("U56", "CAND20", "W/H126")],
                      GROSS0 * WB1[("U56", "CAND20", "M/H0")], pan["warm"])
        for s in STATS:
            d6 = max(d6, float(np.nanmax(np.abs(oa[s] - ob[s]))))
    gates["G6"] = (d6 < 1e-9, "ORTHOGONALITY: every overlap statistic is identical at all "
                              f"{len(GROSSES)} gross rungs (max|d| {d6:.2e})")

    g7 = 0.0
    for g in GROSSES:
        W = g * WB1[("U56", "CAND20", "W/H126")]
        sm = W.sum(axis=1)
        g7 = max(g7, float(np.abs(np.where(sm > 0, sm, g) - g).max()))
    gates["G7"] = (g7 < 1e-12, f"gross-matched everywhere invested at every rung: max|sum(w)-g| "
                               f"= {g7:.2e}")

    for k in sorted(gates, key=lambda s: int(s[1:])):
        ok, msg = gates[k]
        P(f"  {k} {'PASS' if ok else 'FAIL'}  {msg}")
    NG = sum(1 for v in gates.values() if v[0])
    P(f"GATES: {NG} of {len(gates)} pass.")
    P("")

    # ================================================================== (A) OVERLAP
    P("=" * 100)
    P("(A) DAY-BY-DAY HOLDINGS OVERLAP — 3 statistics x 4 book pairs x 3 mechanisms x 2 panels")
    P("=" * 100)
    orows = []
    for p, m, (a, b) in product(PANELS, MECHS, PAIRS):
        pan = PAN[p]
        WA, WB = WB1[(p, m, a)], WB1[(p, m, b)]
        h = np.flatnonzero(pan["warm"])
        half = h[:len(h) // 2], h[len(h) // 2:]
        sel_full = pan["warm"]
        sel_h1 = np.zeros_like(sel_full); sel_h1[half[0]] = True
        sel_h2 = np.zeros_like(sel_full); sel_h2[half[1]] = True
        row = dict(kind="BOOK", panel=p, mech=m, pair=f"{a} vs {b}", seed=-1)
        for tag, sel in (("full", sel_full), ("H1", sel_h1), ("H2", sel_h2), ("OOS", pan["oos"])):
            row.update(summ(overlaps(WA, WB, sel), tag))
        fa, fb = BOOKS[a][0], BOOKS[b][0]
        ga, ta = nrun(pan["rets"], lag(GROSS0 * WA), lagmask(pan["mask"][fa]))
        gb, tb = nrun(pan["rets"], lag(GROSS0 * WB), lagmask(pan["mask"][fb]))
        ra, rb = ga - ta * COST / 1e4, gb - tb * COST / 1e4
        row["ret_rho"] = float(np.corrcoef(ra[pan["warm"]], rb[pan["warm"]])[0, 1])
        row["ret_rho_OOS"] = float(np.corrcoef(ra[pan["oos"]], rb[pan["oos"]])[0, 1])
        orows.append(row)
    for p, s, (a, b) in product(PANELS, range(NSEED), PAIRS):
        pan = PAN[p]
        WA, WB = WN1[(p, s, a)], WN1[(p, s, b)]
        row = dict(kind="NULL", panel=p, mech="NULL", pair=f"{a} vs {b}", seed=s)
        row.update(summ(overlaps(WA, WB, pan["warm"]), "full"))
        row.update(summ(overlaps(WA, WB, pan["oos"]), "OOS"))
        fa, fb = BOOKS[a][0], BOOKS[b][0]
        ga, ta = nrun(pan["rets"], lag(GROSS0 * WA), lagmask(pan["mask"][fa]))
        gb, tb = nrun(pan["rets"], lag(GROSS0 * WB), lagmask(pan["mask"][fb]))
        ra, rb = ga - ta * COST / 1e4, gb - tb * COST / 1e4
        row["ret_rho"] = float(np.corrcoef(ra[pan["warm"]], rb[pan["warm"]])[0, 1])
        orows.append(row)
    OV = pd.DataFrame(orows)
    dump(OV, "overlap")

    P("")
    P(f"Median overlap statistic, U56 / CAND20 (books) and the i.i.d. null (median over "
      f"{NSEED} seeds):")
    P(f"{'pair':<22}" + "".join(f"{s:>16}" for s in STATS) + f"{'ret_rho':>10}")
    for p in PANELS:
        for a, b in PAIRS:
            bk = OV[(OV.kind == "BOOK") & (OV.panel == p) & (OV.mech == "CAND20")
                    & (OV.pair == f"{a} vs {b}")].iloc[0]
            P(f"  {p:<5}{a+' vs '+b:<16}" + "".join(f"{bk[f'full_{s}_median']:>16.4f}" for s in STATS)
              + f"{bk['ret_rho']:>10.4f}")
        nl = OV[(OV.kind == "NULL") & (OV.panel == p)]
        for a, b in PAIRS:
            q = nl[nl.pair == f"{a} vs {b}"]
            P(f"  {p:<5}{'NULL '+a+' vs '+b:<16}"
              + "".join(f"{q[f'full_{s}_median'].median():>16.4f}" for s in STATS)
              + f"{q['ret_rho'].median():>10.4f}")

    # closed-form independent-subset floor
    cf = {p: NTOP / (2.0 * PAN[p]["N"] - NTOP) for p in PANELS}
    P("")
    P("Closed-form floor for two INDEPENDENT uniform 20-of-K subsets (E[inter]/E[union]): "
      + ", ".join(f"{p} K={PAN[p]['N']} -> {cf[p]:.4f}" for p in PANELS))

    # ================================================================== (B) GROSS LADDER
    P("")
    P("=" * 100)
    P("(B) THE GROSS LADDER — every rung, both KEEP paths, books and gross-matched null")
    P("=" * 100)
    grows = []
    for p, m, bname, g in product(PANELS, MECHS, BOOKS, GROSSES):
        pan = PAN[p]
        f = BOOKS[bname][0]
        W = g * WB1[(p, m, bname)]
        gr, t = nrun(pan["rets"], lag(W), lagmask(pan["mask"][f]))
        r = gr - t * COST / 1e4
        ty = float(t[pan["warm"]].sum() / pan["yrs"])
        b = blocks(r, pan["warm"], pan["oos"])
        l4b, l4a, lo = legs_4b(b, pan["spy"]), legs_4a(b, LIVE[p]), legs_4b_oos(b, pan["spy"])
        grows.append(dict(kind="BOOK", panel=p, mech=m, book=bname, gross=g, seed=-1,
                          turn_yr=ty, drag_bp=ty * COST, **b, **l4b, **l4a, **lo,
                          pass4b=all(l4b.values()), pass4a=all(l4a.values()),
                          pass4b_oos=all(lo.values())))
    for p, s, bname, g in product(PANELS, range(NSEED), BOOKS, GROSSES):
        pan = PAN[p]
        f = BOOKS[bname][0]
        W = g * WN1[(p, s, bname)]
        gr, t = nrun(pan["rets"], lag(W), lagmask(pan["mask"][f]))
        r = gr - t * COST / 1e4
        ty = float(t[pan["warm"]].sum() / pan["yrs"])
        b = blocks(r, pan["warm"], pan["oos"])
        l4b, l4a, lo = legs_4b(b, pan["spy"]), legs_4a(b, LIVE[p]), legs_4b_oos(b, pan["spy"])
        grows.append(dict(kind="NULL", panel=p, mech="NULL", book=bname, gross=g, seed=s,
                          turn_yr=ty, drag_bp=ty * COST, **b, **l4b, **l4a, **lo,
                          pass4b=all(l4b.values()), pass4a=all(l4a.values()),
                          pass4b_oos=all(lo.values())))
    G = pd.DataFrame(grows)
    dump(G, "ladder")

    for p in PANELS:
        P("")
        P(f"--- {p}: CAND20 books on the gross ladder (10 bps).  LIVE RULES v2: "
          f"{LIVE[p]['CAGR']:.2%} / {LIVE[p]['Sharpe']:.4f} / {LIVE[p]['MaxDD']:.2%}, halves "
          f"{LIVE[p]['H1']:.3f}/{LIVE[p]['H2']:.3f}; SPY {PAN[p]['spy']['CAGR']:.2%} / "
          f"{PAN[p]['spy']['Sharpe']:.4f} / {PAN[p]['spy']['MaxDD']:.2%}")
        P(f"{'book':<8}{'gross':>7}{'CAGR':>9}{'Sharpe':>9}{'MaxDD':>9}{'H1':>7}{'H2':>7}"
          f"{'oCAGR':>9}{'oSh':>7}{'oDD':>9}{'4b':>5}{'4a':>5}{'4bOOS':>7}  failed legs")
        for bname, g in product(BOOKS, GROSSES):
            q = G[(G.kind == "BOOK") & (G.panel == p) & (G.mech == "CAND20")
                  & (G.book == bname) & (G.gross == g)].iloc[0]
            fb = [k for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR") if not q[k]]
            fa = [k for k in ("A_H1", "A_H2", "A_DD") if not q[k]]
            P(f"{bname:<8}{g:>7.2f}{q['CAGR']:>9.2%}{q['Sharpe']:>9.4f}{q['MaxDD']:>9.2%}"
              f"{q['H1']:>7.3f}{q['H2']:>7.3f}{q['OOS_CAGR']:>9.2%}{q['OOS_Sharpe']:>7.3f}"
              f"{q['OOS_MaxDD']:>9.2%}{str(q['pass4b']):>5}{str(q['pass4a']):>5}"
              f"{str(q['pass4b_oos']):>7}  4b:{','.join(fb) or '-'} 4a:{','.join(fa) or '-'}")

    P("")
    P("Null 4a / 4b pass rate along the SAME ladder (20 seeds per cell) — if de-grossing hands 4a")
    P("to a coin flip, 4a's drawdown leg is a GROSS DIAL and not a property of the book:")
    P(f"{'panel':<6}{'book':<8}" + "".join(f"{('g='+format(g,'.2f')):>14}" for g in GROSSES))
    for p, bname in product(PANELS, ("W/H126", "M/H0")):
        r4a = [G[(G.kind == "NULL") & (G.panel == p) & (G.book == bname)
                 & (G.gross == g)]["pass4a"].mean() for g in GROSSES]
        r4b = [G[(G.kind == "NULL") & (G.panel == p) & (G.book == bname)
                 & (G.gross == g)]["pass4b"].mean() for g in GROSSES]
        P(f"{p:<6}{bname:<8}" + "".join(f"{a:>7.3f}/{b:<6.3f}" for a, b in zip(r4a, r4b))
          + "   (4a / 4b)")

    # ================================================================== (C) RULE 8
    P("")
    P("=" * 100)
    P("(C) RULE 8 WALK-FORWARD — the gross rung chosen on 2009-2016 alone, read once on 2017-2026")
    P("=" * 100)
    wrows = []
    for p, m, bname in product(PANELS, MECHS, ("W/H126", "M/H0", "W/H0")):
        sub = G[(G.kind == "BOOK") & (G.panel == p) & (G.mech == m) & (G.book == bname)]
        # C_ISSHARPE: max IS Sharpe (ties -> highest gross, declared).  C_ISDD: the HIGHEST rung
        # whose IS MaxDD is no worse than the live book's IS MaxDD (the 4a-targeting chooser).
        c1 = sub.sort_values(["IS_Sharpe", "gross"], ascending=[False, False]).iloc[0]
        ok = sub[sub.IS_MaxDD >= LIVE[p]["IS_MaxDD"]]
        c2 = (ok.sort_values("gross", ascending=False).iloc[0] if len(ok)
              else sub.sort_values("gross").iloc[0])
        dflt = sub[sub.gross == GROSS0].iloc[0]
        best_oos = sub.sort_values("OOS_Sharpe", ascending=False).iloc[0]
        for cname, c in (("C_ISSHARPE", c1), ("C_ISDD", c2), ("DEFAULT_0.75", dflt)):
            wrows.append(dict(panel=p, mech=m, book=bname, chooser=cname, pick=c["gross"],
                              IS_Sharpe=c["IS_Sharpe"], IS_MaxDD=c["IS_MaxDD"],
                              OOS_CAGR=c["OOS_CAGR"], OOS_Sharpe=c["OOS_Sharpe"],
                              OOS_MaxDD=c["OOS_MaxDD"],
                              spy_OOS_CAGR=PAN[p]["spy"]["OOS_CAGR"],
                              spy_OOS_Sharpe=PAN[p]["spy"]["OOS_Sharpe"],
                              spy_OOS_MaxDD=PAN[p]["spy"]["OOS_MaxDD"],
                              live_OOS_CAGR=LIVE[p]["OOS_CAGR"],
                              live_OOS_Sharpe=LIVE[p]["OOS_Sharpe"],
                              live_OOS_MaxDD=LIVE[p]["OOS_MaxDD"],
                              pass4b=bool(c["pass4b"]), pass4a=bool(c["pass4a"]),
                              pass4b_oos=bool(c["pass4b_oos"]),
                              oos_best_gross=best_oos["gross"],
                              hit=bool(c["gross"] == best_oos["gross"])))
    WF = pd.DataFrame(wrows)
    dump(WF, "walkforward")
    P(f"{'panel':<6}{'mech':<9}{'book':<8}{'chooser':<13}{'pick':>6}{'oosBest':>9}{'hit':>6}"
      f"{'OOS_CAGR':>10}{'OOS_Sh':>8}{'OOS_DD':>9}{'4a':>6}{'4b':>6}{'4bOOS':>7}")
    for _, r in WF.iterrows():
        P(f"{r['panel']:<6}{r['mech']:<9}{r['book']:<8}{r['chooser']:<13}{r['pick']:>6.2f}"
          f"{r['oos_best_gross']:>9.2f}{str(r['hit']):>6}{r['OOS_CAGR']:>10.2%}"
          f"{r['OOS_Sharpe']:>8.3f}{r['OOS_MaxDD']:>9.2%}{str(r['pass4a']):>6}"
          f"{str(r['pass4b']):>6}{str(r['pass4b_oos']):>7}")
    for p in PANELS:
        P(f"  {p} OOS comparands: SPY {PAN[p]['spy']['OOS_CAGR']:.2%} / "
          f"{PAN[p]['spy']['OOS_Sharpe']:.4f} / {PAN[p]['spy']['OOS_MaxDD']:.2%};  LIVE RULES v2 "
          f"{LIVE[p]['OOS_CAGR']:.2%} / {LIVE[p]['OOS_Sharpe']:.4f} / {LIVE[p]['OOS_MaxDD']:.2%}")
    P(f"  chooser hit rate (IS pick == OOS-best rung): "
      + ", ".join(f"{c} {WF[WF.chooser==c]['hit'].mean():.3f}"
                  for c in ("C_ISSHARPE", "C_ISDD", "DEFAULT_0.75"))
      + f"  (a 1-of-{len(GROSSES)} coin flip is {1/len(GROSSES):.3f})")

    # ================================================================== (D') THE CROSSING
    P("")
    P("=" * 100)
    P("(D') WHERE THE TWO CONSTRAINTS CROSS — derived from the reported rungs, no new dial")
    P("=" * 100)
    P("g_DD  = the highest gross whose |MaxDD| is inside the live book's (linear in g, exact to")
    P("        the ladder's own scaling); g_CAGR = the LOWEST gross still clearing 4b's CAGR")
    P("        floor (0.70 x SPY).  A rung satisfying the queue's question needs g <= g_DD AND")
    P("        g >= g_CAGR; if g_CAGR > g_DD the window is EMPTY and the gap is reported in pp.")
    crows = []
    for p, m, bname in product(PANELS, MECHS, ("W/H126", "M/H0", "W/H0")):
        sub = G[(G.kind == "BOOK") & (G.panel == p) & (G.mech == m)
                & (G.book == bname)].sort_values("gross")
        r0 = sub[sub.gross == GROSS0].iloc[0]
        gdd = GROSS0 * abs(LIVE[p]["MaxDD"]) / abs(r0["MaxDD"])
        floor_c = CAGR_FLOOR * PAN[p]["spy"]["CAGR"]
        gg, cc = sub["gross"].values, sub["CAGR"].values
        gcagr = float(np.interp(floor_c, cc, gg)) if cc.min() <= floor_c <= cc.max() else (
            np.nan if floor_c > cc.max() else float(gg.min()))
        dd_at_gcagr = r0["MaxDD"] * gcagr / GROSS0
        crows.append(dict(panel=p, mech=m, book=bname, g_DD=gdd, g_CAGR=gcagr,
                          window_empty=bool(not (gcagr <= gdd)),
                          MaxDD_at_g_CAGR=dd_at_gcagr, live_MaxDD=LIVE[p]["MaxDD"],
                          gap_pp=100.0 * (abs(dd_at_gcagr) - abs(LIVE[p]["MaxDD"]))))
    C = pd.DataFrame(crows)
    dump(C, "crossing")
    P(f"{'panel':<6}{'mech':<9}{'book':<8}{'g_DD':>7}{'g_CAGR':>8}{'window':>9}"
      f"{'MaxDD@g_CAGR':>14}{'live':>9}{'gap pp':>9}")
    for _, r in C.iterrows():
        P(f"{r['panel']:<6}{r['mech']:<9}{r['book']:<8}{r['g_DD']:>7.3f}{r['g_CAGR']:>8.3f}"
          f"{('EMPTY' if r['window_empty'] else 'open'):>9}{r['MaxDD_at_g_CAGR']:>14.2%}"
          f"{r['live_MaxDD']:>9.2%}{r['gap_pp']:>9.2f}")

    # ================================================================== (D) HYPOTHESES
    P("")
    P("=" * 100)
    P("(D) THE DECLARED HYPOTHESES")
    P("=" * 100)
    hyp = []
    u = OV[(OV.kind == "BOOK") & (OV.panel == "U56") & (OV.mech == "CAND20")]
    jac_wh = float(u[u.pair == "W/H126 vs M/H0"]["full_JACCARD_median"].iloc[0])
    rho_wh = float(u[u.pair == "W/H126 vs M/H0"]["ret_rho"].iloc[0])
    jac_cad = float(u[u.pair == "W/H0 vs M/H0"]["full_JACCARD_median"].iloc[0])
    floor = float(OV[(OV.kind == "NULL") & (OV.panel == "U56")
                     & (OV.pair == "W/H126 vs M/H0")]["full_JACCARD_median"].median())
    same = jac_wh >= 0.80 and rho_wh >= 0.95
    diff = jac_wh <= floor + 0.10
    hyp.append(dict(id="H_SAME", statement="W/H126 IS the monthly book by another route "
                    "(median JACCARD >= 0.80 AND net-return rho >= 0.95)",
                    value=f"JACCARD {jac_wh:.4f}, rho {rho_wh:.4f}",
                    verdict="PASS" if same else "FAIL"))
    hyp.append(dict(id="H_DIFF", statement="W/H126 is a GENUINELY DIFFERENT portfolio "
                    f"(median JACCARD <= null floor {floor:.4f} + 0.10)",
                    value=f"JACCARD {jac_wh:.4f} vs bar {floor+0.10:.4f}",
                    verdict="PASS" if diff else "FAIL"))
    hyp.append(dict(id="H_MINHOLD_MOVES", statement="the MIN-HOLD constraint moves the book "
                    "further from M than the ordinary weekly book already was "
                    "(JACCARD[W/H126 vs M] < JACCARD[W/H0 vs M])",
                    value=f"{jac_wh:.4f} vs {jac_cad:.4f}",
                    verdict="PASS" if jac_wh < jac_cad else "FAIL"))
    # H_RUNG: is there a rung that brings W/H126's MaxDD inside the live book's AND keeps 4b?
    sub = G[(G.kind == "BOOK") & (G.panel == "U56") & (G.mech == "CAND20") & (G.book == "W/H126")]
    win = sub[(sub.MaxDD >= LIVE["U56"]["MaxDD"]) & sub.pass4b]
    hyp.append(dict(id="H_RUNG", statement="a gross rung below 0.75 brings W/H126's MaxDD inside "
                    f"the live book's ({LIVE['U56']['MaxDD']:.2%}) while KEEPING 4b",
                    value=("rungs " + ", ".join(f"{g:.2f}" for g in sorted(win.gross))
                           if len(win) else "no rung on the ladder does both"),
                    verdict="PASS" if len(win) else "FAIL"))
    # H_ARITH: Sharpe invariant along the ladder (declared (c))
    sp_span = float(sub.Sharpe.max() - sub.Sharpe.min())
    hyp.append(dict(id="H_ARITH", statement="the gross ladder is ARITHMETIC: full-sample Sharpe "
                    "span across the five rungs is under 0.05",
                    value=f"span {sp_span:.4f} ({sub.Sharpe.min():.4f} - {sub.Sharpe.max():.4f})",
                    verdict="PASS" if sp_span < 0.05 else "FAIL"))
    # H_NULL4A: does the same de-grossing hand 4a to the null?
    nl = G[(G.kind == "NULL") & (G.panel == "U56") & (G.book == "W/H126")]
    n075 = float(nl[nl.gross == GROSS0]["pass4a"].mean())
    nlow = float(nl[nl.gross == min(GROSSES)]["pass4a"].mean())
    hyp.append(dict(id="H_NULL4A", statement="de-grossing hands 4a to the gross-matched NULL too "
                    "(null 4a pass rate at the lowest rung >= 0.50)",
                    value=f"null 4a {n075:.3f} at g={GROSS0} -> {nlow:.3f} at g={min(GROSSES)}",
                    verdict="PASS" if nlow >= 0.50 else "FAIL"))
    # H_NULL4B (reported, not pre-registered as a KEEP condition): is 4b itself a gross-rung
    # object for the coin flip?  If the null's 4b pass rate moves by >= 0.25 along the ladder,
    # then any single-rung 4b pass is read in a cell whose base rate the rung chose.
    nb = [float(nl[nl.gross == g]["pass4b"].mean()) for g in GROSSES]
    hyp.append(dict(id="H_NULL4B", statement="4b's base rate is itself a GROSS-RUNG object: the "
                    "gross-matched null's 4b pass rate moves by >= 0.25 along the same ladder",
                    value="null 4b " + " / ".join(f"{x:.3f}" for x in nb)
                          + f" over g={GROSSES} (span {max(nb)-min(nb):.3f})",
                    verdict="PASS" if (max(nb) - min(nb)) >= 0.25 else "FAIL"))
    # H_4A_LEG: the queue text says W/H126 "fails 4a on drawdown".  Which legs actually fail?
    r075 = sub[sub.gross == GROSS0].iloc[0]
    failed = [k for k in ("A_H1", "A_H2", "A_DD") if not r075[k]]
    hyp.append(dict(id="H_4A_LEG", statement="the queue's premise — W/H126 fails 4a on DRAWDOWN "
                    "ALONE at gross 0.75 (A_DD the only failing leg)",
                    value=f"failing 4a legs: {','.join(failed) or 'none'}; book halves "
                          f"{r075['H1']:.3f}/{r075['H2']:.3f} vs live {LIVE['U56']['H1']:.3f}/"
                          f"{LIVE['U56']['H2']:.3f}",
                    verdict="PASS" if failed == ["A_DD"] else "FAIL"))
    H = pd.DataFrame(hyp)
    dump(H, "hypotheses")
    for _, r in H.iterrows():
        P(f"  {r['id']:<16} {r['verdict']:<5} {r['statement']}")
        P(f"  {'':<16}       -> {r['value']}")

    dump(pd.DataFrame([dict(gate=k, pass_=v[0], detail=v[1]) for k, v in sorted(gates.items())]),
         "gates")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    P(f"\n[done in {time.time()-t0:.0f}s]")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

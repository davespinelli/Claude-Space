#!/usr/bin/env python3
"""Idea 1086 (cloud lane, 2026-09-16) — is the EDGE HUMP a MIN-HOLD artefact?

QUESTION (QUEUE idea 1086, verbatim)
    1082 found EDGE over the DD-matched null peaks at n=12 (U56) / n=10 (B136) and falls away
    below it, at a FROZEN min hold of 126 days.  At n=5 a 126-day hold locks 5 names for half a
    year, so the fall below the peak may be a STALENESS fact rather than a thinness-of-ranking
    fact.  Re-run 1082's ladder at H in {21, 63, 126} and report whether the peak moves LEFT as
    the hold shortens.  Max 2 params (n, H).

THE TWO TUNED DIALS (PROTOCOL rule 4, no more than two)
    1. N  in {5, 8, 10, 12, 15, 20, 25, 30, 40}          — 1082's ladder, unchanged
    2. H  in {21, 63, 126}                               — the min hold, 1082's frozen 126 plus
                                                           a quarter and a month
    9 x 3 = 27 cells per panel, 54 in total, ALL published for the book AND the null.
    SEEDS ARE FROZEN AT 40 — they were 1082's second dial and are NOT a dial here, because this
    idea's two dials are N and H.  Everything else stays at 936/1064/1071/1082's construction:
    cap INF, CAND20 legs, max_vol 0.60, gross 0.75, W cadence, 10 bps, LAG 1.

    THE NULL DRAWS ARE PAIRED ACROSS H BY CONSTRUCTION.  The seed recipe is 1082's verbatim —
    md5(panel, N, "INF", s) with NO H term — so the random rank matrix at a given (panel, N, s)
    is the SAME object at H = 21, 63 and 126, and the min hold is then applied to it exactly as
    it is applied to the book.  Two consequences, both wanted: the H comparison is paired and
    carries less noise than independent draws would, and the H=126 column is BIT-IDENTICAL to
    1082's, which is what gate G5 checks against its committed numbers.

WHAT "EDGE" MEANS HERE — unchanged from 1082, quoted so the two runs read against each other
    EDGE(n, H) = 100 * ( CAGR_book(n, H) - median_seeds CAGR_null(n, H) ) in pp, where every null
    path is REBUILT at the gross lambda*0.75 that equalises its realised |MaxDD| with the book's
    at that same (n, H).  The CASH convention (r -> lambda*r) is carried beside it only so
    1071's and 1082's committed numbers stay checkable; REBUILT is the headline.

DECLARED BEFORE ANY NUMBER — what would make the queue's framing right, and what would refute it
    (a) STALENESS story (the queue's): the fall in EDGE below n=12 is the 126-day lock, not the
        ranking.  At n=5 the book holds 5 names for half a year and cannot act on the composite
        it just computed.  SIGNATURE: the EDGE peak moves LEFT as H shortens, and EDGE(5) RISES
        as H falls.  If H=21 puts the peak at or below n=8 on both panels, the queue is right and
        1082's CEILING reading is an artefact of its own frozen dial.
    (b) CEILING story (1082's verdict): the top of the composite's ranking is thin while
        idiosyncratic variance explodes, so concentrating past some n buys noise.  SIGNATURE: the
        peak stays put in n as H moves, and EDGE(5) does not rise materially.
    (c) A THIRD outcome is possible and is named in advance so it cannot be read as either:
        shortening H may raise EDGE at EVERY n (a pure turnover/freshness level effect) without
        moving the peak at all.  That would refute the queue's mechanism while still showing the
        min hold matters, and it would be reported as such.
    (d) EDGE IS NOT A KEEP PATH.  Both 4a and 4b are scored at every one of the 54 cells and the
        rule-8 walk-forward picks (n, H) on 2009-2016 alone.  An edge that rises while 4b stays
        shut is real and is not capital.

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

DATE = "2026-09-16"
SLUG = "is-the-EDGE-HUMP-a-MIN-HOLD-artefact"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

LAG = 1
WARMUP = 260
MAXVOL = 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST = 10.0
GROSS0 = 0.75
FREQ = "W"
LEGS = [(21, 252), (0, 126), (0, 63)]          # CAND20, 936/1064/1071/1082's construction
CAPNAME = "INF"                                 # frozen, NOT a dial

NS = [5, 8, 10, 12, 15, 20, 25, 30, 40]         # dial 1 — 1082's ladder verbatim
HS = [21, 63, 126]                              # dial 2 — the min hold
NSEED = 40                                      # FROZEN (1082's second dial, not one here)
BISECT = 34

PANELS = ["U56", "B136"]

# committed cross-run anchors (ideas 936 / 1071 / 1082 / 1018+1023)
A936_WH126 = (0.155787, 1.139701, -0.191276)
A1071_N20_NULL_MED_CASH = 0.105068
A1082_EDGE_H126 = {                             # committed REBUILT EDGE ladder at H=126, 40 seeds
    "U56": [5.95, 5.35, 6.21, 6.82, 5.22, 5.12, 2.95, 1.55, 0.41],
    "B136": [5.72, 5.24, 8.32, 6.52, 6.83, 4.93, 4.27, 2.81, 1.85],
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
    matrix is passed IN so the same draw can be reused at every H (paired comparison)."""
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


def main():
    t0 = time.time()
    P(f"# Idea 1086 (cloud lane, {DATE}) — is the EDGE HUMP a MIN-HOLD artefact?")
    P(f"# 2 tuned dials: N {NS} x H {HS}.  ALL 27 cells per panel reported (54 total).")
    P(f"# FROZEN (not dials): SEEDS {NSEED}, cap {CAPNAME}, CAND20 legs {LEGS}, max_vol {MAXVOL}, "
      f"gross {GROSS0}, cost {COST:.0f} bps, LAG {LAG}, cadence {FREQ}.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   (a) STALENESS (the queue's): the fall below n=12 is the 126-day lock.  SIGNATURE — the")
    P("#       peak moves LEFT as H shortens AND EDGE(5) rises as H falls.")
    P("#   (b) CEILING (1082's verdict): the top of the ranking is thin.  SIGNATURE — the peak")
    P("#       stays put in n as H moves and EDGE(5) does not rise materially.")
    P("#   (c) NAMED IN ADVANCE so it cannot be read as either: a pure LEVEL effect, where a")
    P("#       shorter H raises EDGE at EVERY n without moving the peak.  That refutes the")
    P("#       queue's mechanism while still showing the hold matters.")
    P("#   (d) EDGE IS NOT A KEEP PATH.  4a and 4b are scored at all 54 cells; rule 8 picks")
    P("#       (n, H) on 2009-2016 alone.")
    P("# The null draws are PAIRED across H: 1082's seed recipe carries no H term, so the same")
    P("# random rank matrix is re-used at every hold and the H=126 column is bit-identical to")
    P("# 1082's (gate G5).")
    P("")

    rows, nullrows, gaterows, seedrows = [], [], [], []
    picks, benchrows = [], []
    gates = {}

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
            gates["G2 CROSS-RUN vs 936/1071/1082's committed W/H126 N=20 triple"] = (d2, d2 < 5e-3)
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

    # G5 — CROSS-RUN against 1082's committed H=126 EDGE ladder
    d5 = 0.0
    for p_ in PANELS:
        s = nul[(nul.panel == p_) & (nul.H == 126)].sort_values("N")
        d5 = max(d5, float(np.abs(s.EDGE_pp.values - np.array(A1082_EDGE_H126[p_])).max()))
    gates["G5 CROSS-RUN 1082's committed H=126 EDGE ladder, both panels"] = (d5, d5 < 5e-3)
    u20 = nul[(nul.panel == "U56") & (nul.N == 20) & (nul.H == 126)].iloc[0]
    d5b = abs(u20.null_CAGR_med_cash - A1071_N20_NULL_MED_CASH)
    gates["G5b CROSS-RUN 1071/1082's committed U56 N=20 H=126 null median (CASH)"] = (
        d5b, d5b < 5e-3)
    tspread = float(grid[grid.panel == "U56"].turnover.max() - grid[grid.panel == "U56"].turnover.min())
    gates["G8 the H dial is LIVE (U56 turnover spread >= 1.0x/yr across the grid)"] = (
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
    for panel in PANELS:
        P(f"   --- {panel} ---   EDGE(n, H) in pp")
        P("        H  " + "".join(f"{n:>9d}" for n in NS) + "     argmax   EDGE(5)  EDGE(20)")
        for H in HS:
            s = nul[(nul.panel == panel) & (nul.H == H)].set_index("N").reindex(NS)
            am = int(s.EDGE_pp.idxmax())
            P(f"      {H:3d}  " + "".join(f"{v:>+9.3f}" for v in s.EDGE_pp.values)
              + f"     n={am:<3d}  {s.EDGE_pp[5]:+7.3f}  {s.EDGE_pp[20]:+7.3f}")
        P("        SE  " + "".join(
            f"{v:>9.3f}" for v in nul[(nul.panel == panel) & (nul.H == 126)]
            .set_index("N").reindex(NS).EDGE_se_pp.values) + "     (seed SE at H=126)")

    P("")
    P("## DOES THE PEAK MOVE LEFT AS THE HOLD SHORTENS?")
    peaks = {}
    for panel in PANELS:
        row = []
        for H in HS:
            s = nul[(nul.panel == panel) & (nul.H == H)].set_index("N")
            row.append(int(s.EDGE_pp.idxmax()))
        peaks[panel] = row
        P(f"   {panel}: argmax n at H = " + ", ".join(f"{H}->{n}" for H, n in zip(HS, row)))
    P("   (queue's STALENESS signature: this row is non-increasing left to right as H falls,")
    P("    i.e. reading HS from the right, the peak moves to a SMALLER n as the hold shortens.)")

    P("")
    P("## THE LEVEL EFFECT — does a shorter hold raise EDGE at EVERY n? (outcome (c))")
    for panel in PANELS:
        P(f"   --- {panel} ---   EDGE(n, 21) - EDGE(n, 126) in pp, by n")
        a = nul[(nul.panel == panel) & (nul.H == 21)].set_index("N").reindex(NS).EDGE_pp
        c = nul[(nul.panel == panel) & (nul.H == 126)].set_index("N").reindex(NS).EDGE_pp
        d = a - c
        P("        n   " + "".join(f"{n:>9d}" for n in NS))
        P("      dEDGE " + "".join(f"{v:>+9.3f}" for v in d.values))
        P(f"      n with dEDGE > 0: {int((d > 0).sum())} of {len(NS)};  mean {d.mean():+.3f} pp;  "
          f"median {d.median():+.3f} pp")

    P("")
    P("## RULE 8 — IS(2009-2016)-only choosers pick (N, H) over 27 cells, OOS(2017-2026) ONCE")
    for _, r in pk.iterrows():
        P(f"   {r.panel} {r.chooser}: picks N={int(r.N)} H={int(r.H)} -> OOS {r.OOS_CAGR:.2%} / "
          f"{r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:.2%}  | SPY OOS {r.spy_OOS_CAGR:.2%} / "
          f"{r.spy_OOS_Sharpe:.4f} / {r.spy_OOS_MaxDD:.2%} | RULES v2 OOS {r.live_OOS_CAGR:.2%} / "
          f"{r.live_OOS_Sharpe:.4f} / {r.live_OOS_MaxDD:.2%} | 4b_OOS {r.pass4b_oos} "
          f"(O_S {r.O_S} O_DD {r.O_DD} O_CAGR {r.O_CAGR}) 4b_full {r.pass4b_full} 4a {r.pass4a}")

    P("")
    P("## HYPOTHESES (declared before the run, scored as written)")
    H_ = []
    for panel in PANELS:
        pr = peaks[panel]
        H_.append((f"H_LEFT[{panel}] the EDGE peak moves LEFT (to smaller n) as H shortens "
                   f"126 -> 63 -> 21 (weakly, the queue's staleness signature)",
                   bool(pr[0] <= pr[1] <= pr[2]),
                   "argmax " + ", ".join(f"H={H}:{n}" for H, n in zip(HS, pr))))
        H_.append((f"H_E5[{panel}] EDGE(5) RISES as H falls from 126 to 21",
                   bool(float(nul[(nul.panel == panel) & (nul.H == 21) & (nul.N == 5)].EDGE_pp.iloc[0])
                        > float(nul[(nul.panel == panel) & (nul.H == 126) & (nul.N == 5)]
                                .EDGE_pp.iloc[0])),
                   " -> ".join(
                       f"H={H}: {float(nul[(nul.panel==panel)&(nul.H==H)&(nul.N==5)].EDGE_pp.iloc[0]):+.3f}"
                       for H in HS)))
        for H in HS:
            s = nul[(nul.panel == panel) & (nul.H == H)].set_index("N").reindex(NS).EDGE_pp.values
            H_.append((f"H_HUMP[{panel},H={H}] EDGE is a HUMP (NOT monotone decreasing in n over "
                       f"5..40) — 1082's shape survives this hold",
                       bool(not all(s[i] >= s[i + 1] for i in range(len(s) - 1))),
                       " -> ".join(f"{v:+.2f}" for v in s)))
    H_.append(("H_TURN a shorter hold turns the book over MORE at every (panel, N) "
               "(the H dial is doing what a hold does)",
               bool(all(grid[(grid.panel == p_) & (grid.N == n) & (grid.H == 21)].turnover.iloc[0]
                        > grid[(grid.panel == p_) & (grid.N == n) & (grid.H == 126)].turnover.iloc[0]
                        for p_ in PANELS for n in NS)),
               f"U56 turnover spread {tspread:.2f}x/yr"))
    H_.append(("H_WF >= 1 rule-8 pick clears 4b OUT OF SAMPLE",
               bool(pk.pass4b_oos.any()), f"{int(pk.pass4b_oos.sum())} of {len(pk)} picks"))
    H_.append(("H_4A no cell clears 4a (the DD leg is a book fact, not an (n, H) fact)",
               bool(not grid.pass4a.any()),
               f"{int(grid.pass4a.sum())} of {len(grid)} cells pass 4a"))
    H_.append(("H_ISHOLD the IS-only choosers agree on H (the hold is choosable out of sample)",
               bool(all(len(set(pk[pk.panel == p_].H)) == 1 for p_ in PANELS)),
               "; ".join(f"{p_}: " + ",".join(str(int(x)) for x in pk[pk.panel == p_].H)
                         for p_ in PANELS)))
    for name, ok, note in H_:
        P(f"   {'PASS' if ok else 'FAIL'}  {name}  [{note}]")

    # ------------------------------------------------------------------ post-run diagnostics
    P("")
    P("## POST-RUN DIAGNOSTICS — computed AFTER reading the grid and labelled as such, NOT")
    P("## pre-declared hypotheses.")
    diagrows = []
    P("")
    P("   (D1) IS ANY PEAK MOVEMENT DECISIVE?  EDGE at two cells differs only through the two")
    P("        null medians (the books are deterministic), so SE(dEDGE) = sqrt(SE_a^2 + SE_b^2).")
    for panel in PANELS:
        for H in HS:
            s = nul[(nul.panel == panel) & (nul.H == H)].set_index("N")
            am = int(s.EDGE_pp.idxmax())
            for other in (5, 20):
                if other == am:
                    continue
                d = float(s.loc[am, "EDGE_pp"] - s.loc[other, "EDGE_pp"])
                se = float(np.hypot(s.loc[am, "EDGE_se_pp"], s.loc[other, "EDGE_se_pp"]))
                P(f"        {panel} H={H:3d}: EDGE({am}) - EDGE({other}) = {d:+.3f} +/- {se:.3f} "
                  f"pp = {d/se:5.2f} SE -> {'DECISIVE' if abs(d) > 2*se else 'NOT decisive'}")
                diagrows.append(dict(diag="D1_edge_delta", panel=panel, H=H, a=am, b=other,
                                     delta_pp=d, se_pp=se, sigmas=d / se,
                                     decisive=bool(abs(d) > 2 * se)))
    P("")
    P("   (D2) THE lambda <= 1 CLIP, as 1082 flagged it.  A null draw already DRIER than the")
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
    dump(bn, "benchmarks"); dump(pd.DataFrame(gaterows), "gates")
    dump(pd.DataFrame([dict(hypothesis=n, passed=bool(o), note=t) for n, o, t in H_]),
         "hypotheses")
    dump(pd.DataFrame(diagrows), "diagnostics")
    P(f"# done in {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

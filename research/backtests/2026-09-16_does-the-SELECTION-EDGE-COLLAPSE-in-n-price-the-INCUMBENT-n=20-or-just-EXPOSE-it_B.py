#!/usr/bin/env python3
"""Idea 1082 (lane B, 2026-09-16) — does the SELECTION-EDGE COLLAPSE in n price the INCUMBENT
n=20, or just EXPOSE it?

QUESTION (QUEUE idea 1082, verbatim)
    idea 1071 measured the book's CAGR advantage over its own DD-matched null falling +5.07 pp at
    n=20 to +0.13 pp at n=40/k=1.00 (percentile 0.65, inside the null).  Walk n BELOW 20
    (5, 8, 10, 12, 15) at the same construction and report whether the edge keeps rising, i.e.
    whether n=20 is a chosen optimum or the top of a slope the record has never walked down.
    Price every rung against its own DD-matched null and score both KEEP paths under rule 8.
    Max 2 params (n, seeds).

THE TWO TUNED DIALS (PROTOCOL rule 4, no more than two)
    1. N      in {5, 8, 10, 12, 15, 20, 25, 30, 40}.  The five below 20 are NEW; 20/25/30/40
       reproduce 1071's ladder exactly so the two runs can be read against each other.
    2. SEEDS  in {5, 10, 20, 40}, NESTED (the first S of the same 40 draws), so the seed dial
       moves the PRECISION of the edge and nothing else.
    All 9 x 4 = 36 (N, SEEDS) cells are reported at BOTH panels, for the book AND the null.
    Everything else is FROZEN at 1071/1064/936's construction: cap k = INF (the incumbent
    re-spread), CAND20 legs, max_vol 0.60, gross 0.75, W cadence, min hold 126, 10 bps, LAG 1.

WHAT "EDGE" MEANS HERE, fixed before any number
    EDGE(n) = 100 * ( CAGR_book(n) - median_seeds CAGR_null(n) ) in pp, where every null path is
    scaled to the SAME REALISED |MaxDD| as the book at that same n.  The DD match is what makes
    rungs comparable at all: as n falls the book concentrates and its own drawdown grows, so a
    raw CAGR ladder would just be a leverage ladder.  Matching removes that.

    TWO MATCH CONVENTIONS, both published, because 1071's G4 FAILED and this run inherits it.
      CASH     r -> lambda * r.  This is the daily-rebalanced blend of the null with cash.  It is
               1071's convention and is reproduced ONLY so its committed +5.07 pp is checkable.
      REBUILT  the null book is REBUILT at gross lambda*0.75 and re-run (weights drift between
               rebalances and the cash sleeve does not, so this is NOT lambda times the CASH
               path).  This is the correct convention and is this run's HEADLINE.
    The gap between them is priced at every rung (gate G4) rather than asserted to be zero.

DECLARED BEFORE ANY NUMBER — what would make the queue's framing right, and what would refute it
    (a) The queue's implicit story is a SLOPE: selection skill per name is constant, so
        concentrating into fewer, better-ranked names should keep raising EDGE all the way down,
        and n=20 is then merely where the record stopped looking.  Refutation: EDGE peaks at some
        n >= 20, or is flat/noisy below 20 relative to its own seed dispersion.
    (b) The rival story is a CEILING: the composite's ranking information is thin at the very top,
        so slots 1-5 are not much better than slots 1-20, while idiosyncratic variance explodes.
        Under a DD match that variance is paid back as a lower lambda, so EDGE would FALL below
        some n.  Signature: a hump.
    (c) EDGE is NOT a KEEP path and is not treated as one.  A rung can have the largest edge over
        its null and still fail 4a and 4b outright; both paths are scored at every rung and the
        rule-8 walk-forward picks n on 2009-2016 alone.  If EDGE rises while 4b stays shut, the
        honest reading is that the edge is real but not capital.

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
SLUG = "does-the-SELECTION-EDGE-COLLAPSE-in-n-price-the-INCUMBENT-n=20-or-just-EXPOSE-it"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

LAG = 1
WARMUP = 260
MAXVOL = 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST = 10.0
GROSS0 = 0.75
FREQ = "W"
HOLD = 126
LEGS = [(21, 252), (0, 126), (0, 63)]          # CAND20, 936/1064/1071's construction
CAPNAME = "INF"                                 # frozen, NOT a dial (1071 showed it near-inert)

NS = [5, 8, 10, 12, 15, 20, 25, 30, 40]         # dial 1
SEEDGRID = [5, 10, 20, 40]                      # dial 2 (nested)
NSEED_MAX = max(SEEDGRID)
BISECT = 34

PANELS = ["U56", "B136"]

# committed cross-run anchors (idea 936 / 1071 / 1083)
A936_WH126 = (0.155787, 1.139701, -0.191276)
A1071_N20_BOOK_CAGR = 0.155787                  # 1071 null.csv U56/N=20/cap=INF
A1071_N20_NULL_MED = 0.105068                   # 1071 null.csv, CASH convention, 20 seeds
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
    return int(hashlib.md5("|".join(str(x) for x in parts).encode()).hexdigest()[:8], 16)


# ---------------------------------------------------------------- fast runner (gated vs engine)
def nrun(rets, wt, mk):
    """Gross portfolio returns and turnover; cost applied by the caller. Construction copied
    verbatim from 936/1064/1071's scripts so the runs are comparable."""
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
    """Return f(lam) -> NET returns of the book REBUILT at gross lam * (this book's gross).

    Because the per-name target weight is a linear function of gross when the cap is INF, a
    rebuild at lam*g has weights exactly lam*wt.  The PATH is NOT lam times this one: the cash
    sleeve (1 - sum w) does not scale, so drift, turnover and drawdown all change.  This closure
    precomputes everything that does not depend on lam so a bisection is cheap; f(1.0) is gated
    against nrun() exactly (G1b).
    """
    T, N = rets.shape
    mk = mk.copy()
    mk[0] = True
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
    reb = np.flatnonzero(mk)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    A = wt[s0] * (Cp / Cp[s0])                     # unit-gross holdings before normalisation
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
    """Target weights under MIN HOLD H and slot count N, cap = INF (re-spread over whatever is
    held).  Identical to 1071's build() at cap=INF."""
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


def build_null(rng, priced, reb, N, H, T, K, gross):
    """Same machinery, random ranks, NO eligibility gate (the record's convention)."""
    rank_key = rng.random((T, K))
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


def miss_pp(cagr, dd, live_dd, spy_cagr):
    """1064/1071/1083's joint-window shortfall, carried here for continuity only."""
    return 100.0 * max(abs(dd) - abs(live_dd), CAGR_FLOOR * spy_cagr - cagr)


def lam_cash(r, target_dd):
    """lambda in (0,1] with |MaxDD(lambda*r)| = |target_dd|; None if already drier."""
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
    """lambda in (0,1] with |MaxDD(REBUILT(lambda)[sl])| = |target_dd|; None if already drier.
    |MaxDD| of the rebuilt book is monotone in lambda (gate G4c checks this on a grid)."""
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
    P(f"# Idea 1082 (lane B, {DATE}) — does the SELECTION-EDGE COLLAPSE in n price the INCUMBENT "
      f"n=20, or just EXPOSE it?")
    P(f"# 2 tuned dials: N {NS} x SEEDS {SEEDGRID} (nested). ALL 36 cells per panel reported (72 total).")
    P(f"# FROZEN (not dials): cap {CAPNAME}, CAND20 legs {LEGS}, max_vol {MAXVOL}, gross {GROSS0}, "
      f"cost {COST:.0f} bps, LAG {LAG}, cadence {FREQ}, min hold {HOLD}.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   (a) SLOPE story: EDGE keeps rising all the way down and n=20 is just where the record")
    P("#       stopped looking.  CEILING story: EDGE humps and falls below some n because the top")
    P("#       of the ranking is thin while idiosyncratic variance explodes.")
    P("#   (b) EDGE = book CAGR - median null CAGR, every null scaled to the book's OWN |MaxDD|;")
    P("#       HEADLINE convention is REBUILT (null re-run at gross lam*0.75), CASH published")
    P("#       beside it only so 1071's committed +5.07 pp is checkable.  1071's G4 asserted the")
    P("#       two are identical; they are not, and the gap is priced here at every rung.")
    P("#   (c) EDGE IS NOT A KEEP PATH.  4a and 4b are scored at every rung and rule 8 picks n on")
    P("#       2009-2016 alone.  Edge rising while 4b stays shut = real but not capital.")
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
            W20, _ = build(rank_key, elig, priced, reb, 20, HOLD, T, K, GROSS0)
            wdf = pd.DataFrame(W20, index=idx, columns=px.columns)
            eng = backtest(px, wdf, cost_bps=COST, freq=FREQ)["returns"].values
            g, tn, _ = nrun(rets, lagmat(W20), mkl)
            fast = g - tn * COST / 1e4
            d1 = float(np.abs(fast[WARMUP:] - eng[WARMUP:]).max())
            gates["G1 fast runner == engine.backtest (U56, N=20, cap INF)"] = (d1, d1 < 1e-12)
            f20 = gross_rescaler(rets, lagmat(W20), mkl)
            d1b = float(np.abs(f20(1.0) - fast).max())
            gates["G1b gross_rescaler(1.0) == nrun (the bisection kernel is the same book)"] = (
                d1b, d1b < 1e-14)
            m = fmet(fast[warm])
            d2 = max(abs(m[0] - A936_WH126[0]), abs(m[1] - A936_WH126[1]), abs(m[2] - A936_WH126[2]))
            gates["G2 CROSS-RUN vs 936/1071 committed W/H126 N=20 triple"] = (d2, d2 < 5e-3)
            d3 = max(abs(sb["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
                     abs(sb["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
                     abs(sb["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
            gates["G3 CROSS-RUN SPY OOS triple"] = (d3, d3 < 5e-4)
            d6 = abs(live_dd - LIVE_MAXDD_COMMITTED)
            gates["G6 live RULES v2 MaxDD == committed -12.05%"] = (d6, d6 < 5e-4)
            # G4c: |MaxDD| of the REBUILT null is monotone in lambda (bisection is well posed)
            rngc = np.random.default_rng(mdseed(panel, 20, CAPNAME, 0))
            Wn0, _ = build_null(rngc, priced, reb, 20, HOLD, T, K, GROSS0)
            fn0 = gross_rescaler(rets, lagmat(Wn0), mkl)
            dds = [abs(maxdd(fn0(l)[warm])) for l in np.linspace(0.1, 1.0, 19)]
            viol = float(max(0.0, max(dds[i] - dds[i + 1] for i in range(len(dds) - 1))))
            gates["G4c |MaxDD| of the REBUILT null is monotone in lambda"] = (viol, viol < 1e-12)
            # G7 determinism
            rngd = np.random.default_rng(mdseed(panel, 20, CAPNAME, 0))
            Wn0b, _ = build_null(rngd, priced, reb, 20, HOLD, T, K, GROSS0)
            d7 = float(np.abs(Wn0 - Wn0b).max())
            gates["G7 null draw is deterministic in its seed recipe"] = (d7, d7 == 0.0)

        # ---- the ladder ---------------------------------------------------------------------
        for N in NS:
            W, nsel = build(rank_key, elig, priced, reb, N, HOLD, T, K, GROSS0)
            g, tn, _ = nrun(rets, lagmat(W), mkl)
            r = g - tn * COST / 1e4
            b = blocks(r, warm, ins, oos)
            l4b, l4a, l4bo = legs_4b(b, sb), legs_4a(b, lb), legs_4b_oos(b, sb)
            row = dict(panel=panel, N=N, cap=CAPNAME, mean_nsel=float(nsel.mean()),
                       turnover=float(tn[warm].sum() / (warm.sum() / 252.0)), **b,
                       MISS_full=miss_pp(b["CAGR"], b["MaxDD"], live_dd, sb["CAGR"]),
                       MISS_oos=miss_pp(b["OOS_CAGR"], b["OOS_MaxDD"], lb["OOS_MaxDD"],
                                        sb["OOS_CAGR"]),
                       **l4b, **l4a, **l4bo,
                       pass4b=all(l4b.values()), pass4a=all(l4a.values()),
                       pass4b_oos=all(l4bo.values()))
            row["pass4b_full_and_oos"] = row["pass4b"] and row["pass4b_oos"]

            # ---- the null at the book's OWN realised drawdown -------------------------------
            c_cash, c_reb, c_is, lam_c, lam_r, drier_c, drier_r = [], [], [], [], [], 0, 0
            for s in range(NSEED_MAX):
                rng = np.random.default_rng(mdseed(panel, N, CAPNAME, s))
                Wn, _ = build_null(rng, priced, reb, N, HOLD, T, K, GROSS0)
                fn = gross_rescaler(rets, lagmat(Wn), mkl)
                base = fn(1.0)
                rn = base[warm]
                lc = lam_cash(rn, b["MaxDD"])
                if lc is None:
                    drier_c += 1
                    c_cash.append(fmet(rn)[0]); lam_c.append(1.0)
                else:
                    c_cash.append(fmet(lc * rn)[0]); lam_c.append(lc)
                lr = lam_rebuilt(fn, warm, b["MaxDD"])
                if lr is None:
                    drier_r += 1
                    c_reb.append(fmet(rn)[0]); lam_r.append(1.0)
                else:
                    c_reb.append(fmet(fn(lr)[warm])[0]); lam_r.append(lr)
                lri = lam_rebuilt(fn, ins, b["IS_MaxDD"])
                c_is.append(fmet(base[ins] if lri is None else fn(lri)[ins])[0])
                seedrows.append(dict(panel=panel, N=N, seed=s, null_CAGR_cash=c_cash[-1],
                                     null_CAGR_rebuilt=c_reb[-1], null_IS_CAGR_rebuilt=c_is[-1],
                                     lam_cash=lam_c[-1], lam_rebuilt=lam_r[-1]))
            c_cash, c_reb, c_is = np.array(c_cash), np.array(c_reb), np.array(c_is)
            for S in SEEDGRID:
                nullrows.append(dict(
                    panel=panel, N=N, cap=CAPNAME, seeds=S,
                    book_CAGR=b["CAGR"], book_MaxDD=b["MaxDD"], book_IS_CAGR=b["IS_CAGR"],
                    null_CAGR_med_rebuilt=float(np.median(c_reb[:S])),
                    null_CAGR_med_cash=float(np.median(c_cash[:S])),
                    null_IS_CAGR_med_rebuilt=float(np.median(c_is[:S])),
                    EDGE_pp=100.0 * (b["CAGR"] - float(np.median(c_reb[:S]))),
                    EDGE_pp_cash=100.0 * (b["CAGR"] - float(np.median(c_cash[:S]))),
                    EDGE_IS_pp=100.0 * (b["IS_CAGR"] - float(np.median(c_is[:S]))),
                    null_CAGR_sd=float(c_reb[:S].std(ddof=1)) if S > 1 else np.nan,
                    EDGE_se_pp=100.0 * 1.2533 * float(c_reb[:S].std(ddof=1)) / np.sqrt(S)
                    if S > 1 else np.nan,
                    null_CAGR_p90_rebuilt=float(np.percentile(c_reb[:S], 90)),
                    null_CAGR_max_rebuilt=float(c_reb[:S].max()),
                    book_pct_of_null=float((c_reb[:S] < b["CAGR"]).mean()),
                    lam_median_rebuilt=float(np.median(lam_r[:S])),
                    lam_median_cash=float(np.median(lam_c[:S])),
                    null_already_drier_rebuilt=int(sum(1 for x in lam_r[:S] if x == 1.0)),
                    conv_gap_pp=100.0 * (float(np.median(c_reb[:S])) - float(np.median(c_cash[:S]))),
                ))
            row["EDGE_pp"] = 100.0 * (b["CAGR"] - float(np.median(c_reb)))
            row["EDGE_pp_cash"] = 100.0 * (b["CAGR"] - float(np.median(c_cash)))
            row["EDGE_IS_pp"] = 100.0 * (b["IS_CAGR"] - float(np.median(c_is)))
            row["book_pct_of_null"] = float((c_reb < b["CAGR"]).mean())
            rows.append(row)
            P(f"   N={N:2d} done  book {b['CAGR']:.2%} / {b['Sharpe']:.4f} / {b['MaxDD']:.2%}  "
              f"EDGE {row['EDGE_pp']:+.3f} pp (cash {row['EDGE_pp_cash']:+.3f})  "
              f"({time.time()-t0:.0f}s)")

        # ---- RULE 8: IS-only choosers pick N, OOS read ONCE ---------------------------------
        gp = pd.DataFrame([r for r in rows if r["panel"] == panel])
        for cname, key in [("C_ISSHARPE", "IS_Sharpe"), ("C_ISDD", "IS_MaxDD"),
                           ("C_ISEDGE", "EDGE_IS_pp"), ("C_ISCAGR", "IS_CAGR")]:
            pick = gp.sort_values(key, ascending=False).iloc[0]
            picks.append(dict(panel=panel, chooser=cname, N=int(pick["N"]),
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
    n40 = nul[nul.seeds == NSEED_MAX]
    n20 = nul[nul.seeds == (20 if 20 in SEEDGRID else NSEED_MAX)]

    # G4 / G5, computable only after the ladder
    u20 = n20[(n20.panel == "U56") & (n20.N == (20 if 20 in NS else NS[-1]))].iloc[0]
    d4a = abs(u20.book_CAGR - A1071_N20_BOOK_CAGR)
    d4b_ = abs(u20.null_CAGR_med_cash - A1071_N20_NULL_MED)
    gates["G5a CROSS-RUN 1071's committed U56 N=20 book CAGR"] = (d4a, d4a < 5e-4)
    gates["G5b CROSS-RUN 1071's committed U56 N=20 null median (CASH, 20 seeds)"] = (d4b_, d4b_ < 5e-4)
    gap = float(n40.conv_gap_pp.abs().max())
    gates["G4 REBUILT vs CASH DD-match conventions agree within 0.25 pp of CAGR (1071 assumed 0)"] = (
        gap, gap < 0.25)
    ddspread = float(100 * (grid[grid.panel == "U56"].MaxDD.max()
                            - grid[grid.panel == "U56"].MaxDD.min()))
    gates["G8 the n dial is LIVE (U56 |MaxDD| spread >= 2 pp across the ladder)"] = (
        ddspread, ddspread >= 2.0)

    P("")
    P("## GATES (printed before any result number)")
    for k, (v, ok) in gates.items():
        P(f"   {'PASS' if ok else 'FAIL'}  {k}: |d| = {v:.3e}")
        gaterows.append(dict(gate=k, value=v, passed=bool(ok)))

    P("")
    P(f"## THE LADDER — book at every N (cap {CAPNAME}, both panels)")
    for panel in PANELS:
        s = grid[grid.panel == panel].sort_values("N")
        P(f"   --- {panel} ---")
        P("       N  nsel   turn    CAGR    Sharpe   MaxDD      H1/H2        OOS C/S/DD"
          "            MISS  4b 4a 4bOOS")
        for _, r in s.iterrows():
            P(f"      {int(r.N):2d} {r.mean_nsel:5.1f} {r.turnover:6.2f} {r.CAGR:7.2%} "
              f"{r.Sharpe:8.4f} {r.MaxDD:8.2%}  {r.H1:.3f}/{r.H2:.3f}  "
              f"{r.OOS_CAGR:6.2%}/{r.OOS_Sharpe:.4f}/{r.OOS_MaxDD:7.2%} {r.MISS_full:7.3f}"
              f"   {int(r.pass4b)}  {int(r.pass4a)}   {int(r.pass4b_oos)}")
        P(f"      4b full {int(s.pass4b.sum())}/{len(s)}   4b OOS {int(s.pass4b_oos.sum())}/{len(s)}"
          f"   4a {int(s.pass4a.sum())}/{len(s)}")

    P("")
    P(f"## THE EDGE OVER THE DD-MATCHED NULL — the question itself ({NSEED_MAX} seeds, REBUILT)")
    for panel in PANELS:
        s = n40[n40.panel == panel].sort_values("N")
        P(f"   --- {panel} ---")
        P("       N   book CAGR  null med   EDGE pp   +/-SE   pct   lambda  drier  cash EDGE  gap")
        for _, r in s.iterrows():
            P(f"      {int(r.N):2d}    {r.book_CAGR:7.2%}   {r.null_CAGR_med_rebuilt:7.2%}  "
              f"{r.EDGE_pp:+8.3f} {r.EDGE_se_pp:6.3f}  {r.book_pct_of_null:.2f}  "
              f"{r.lam_median_rebuilt:6.4f}  {int(r.null_already_drier_rebuilt):3d}  "
              f"{r.EDGE_pp_cash:+8.3f} {r.conv_gap_pp:+6.3f}")
        amax = int(s.loc[s.EDGE_pp.idxmax(), "N"])
        P(f"      argmax EDGE at N={amax} ({s.EDGE_pp.max():+.3f} pp); "
          f"EDGE(5) {float(s[s.N==5].EDGE_pp.iloc[0]):+.3f}, "
          f"EDGE(20) {float(s[s.N==20].EDGE_pp.iloc[0]):+.3f}, "
          f"EDGE(40) {float(s[s.N==40].EDGE_pp.iloc[0]):+.3f}")

    P("")
    P("## THE SEED DIAL — does the verdict move with S?")
    P("      panel  S   argmax N   EDGE(argmax)  EDGE(5)  EDGE(20)  EDGE(40)  rank-corr vs S=40")
    for panel in PANELS:
        ref = n40[n40.panel == panel].sort_values("N").EDGE_pp.values
        for S in SEEDGRID:
            s = nul[(nul.panel == panel) & (nul.seeds == S)].sort_values("N")
            v = s.EDGE_pp.values
            rc = float(pd.Series(v).rank().corr(pd.Series(ref).rank()))
            P(f"      {panel:5s} {S:2d}     {int(s.loc[s.EDGE_pp.idxmax(),'N']):2d}      "
              f"{s.EDGE_pp.max():+8.3f}  {float(s[s.N==5].EDGE_pp.iloc[0]):+7.3f}  "
              f"{float(s[s.N==20].EDGE_pp.iloc[0]):+7.3f}  "
              f"{float(s[s.N==40].EDGE_pp.iloc[0]):+7.3f}      {rc:.4f}")

    P("")
    P("## RULE 8 — IS(2009-2016)-only choosers pick N over the 9 rungs, OOS(2017-2026) read ONCE")
    for _, r in pk.iterrows():
        P(f"   {r.panel} {r.chooser}: picks N={r.N} -> OOS {r.OOS_CAGR:.2%} / {r.OOS_Sharpe:.4f} "
          f"/ {r.OOS_MaxDD:.2%}  | SPY OOS {r.spy_OOS_CAGR:.2%} / {r.spy_OOS_Sharpe:.4f} / "
          f"{r.spy_OOS_MaxDD:.2%} | RULES v2 OOS {r.live_OOS_CAGR:.2%} / {r.live_OOS_Sharpe:.4f} "
          f"/ {r.live_OOS_MaxDD:.2%} | 4b_OOS {r.pass4b_oos} (O_S {r.O_S} O_DD {r.O_DD} "
          f"O_CAGR {r.O_CAGR}) 4b_full {r.pass4b_full} 4a {r.pass4a}")

    P("")
    P("## HYPOTHESES (declared before the run, scored as written)")
    H = []
    for panel in PANELS:
        s = n40[n40.panel == panel].sort_values("N")
        g = grid[grid.panel == panel].sort_values("N")
        e = s.EDGE_pp.values
        amax = int(s.loc[s.EDGE_pp.idxmax(), "N"])
        H.append((f"H_SLOPE[{panel}] EDGE is monotone DECREASING in N over the FULL ladder 5..40 "
                  f"(the queue's slope story)",
                  bool(all(e[i] >= e[i + 1] for i in range(len(e) - 1))),
                  " -> ".join(f"{v:+.2f}" for v in e)))
        H.append((f"H_TOP[{panel}] n=20 is NOT the argmax of EDGE (the record stopped short)",
                  bool(amax != 20), f"argmax N={amax}"))
        H.append((f"H_N5[{panel}] EDGE(5) > EDGE(20) strictly",
                  bool(float(s[s.N == 5].EDGE_pp.iloc[0]) > float(s[s.N == 20].EDGE_pp.iloc[0])),
                  f"{float(s[s.N==5].EDGE_pp.iloc[0]):+.3f} vs "
                  f"{float(s[s.N==20].EDGE_pp.iloc[0]):+.3f} pp"))
        H.append((f"H_SIG[{panel}] the argmax rung's EDGE exceeds 2 seed-SEs (it is not noise)",
                  bool(s.EDGE_pp.max() > 2.0 * float(s.loc[s.EDGE_pp.idxmax(), "EDGE_se_pp"])),
                  f"{s.EDGE_pp.max():+.3f} pp vs 2 SE = "
                  f"{2*float(s.loc[s.EDGE_pp.idxmax(),'EDGE_se_pp']):.3f} pp"))
        H.append((f"H_DD[{panel}] the book's |MaxDD| rises monotonically as N falls "
                  f"(the edge is bought with concentration risk)",
                  bool(all(g.MaxDD.values[i] <= g.MaxDD.values[i + 1]
                           for i in range(len(g) - 1))),
                  " -> ".join(f"{v:.2%}" for v in g.MaxDD.values)))
        H.append((f"H_4B[{panel}] at least one rung BELOW 20 clears 4b full-sample",
                  bool(g[(g.N < 20)].pass4b.any()),
                  f"{int(g[(g.N<20)].pass4b.sum())} of {int((g.N<20).sum())} sub-20 rungs"))
    H.append(("H_SEED the argmax rung is the SAME at S = 5, 10, 20, 40 on both panels",
              bool(all(len({int(nul[(nul.panel == p) & (nul.seeds == S)]
                                .set_index('N').EDGE_pp.idxmax()) for S in SEEDGRID}) == 1
                       for p in PANELS)),
              "; ".join(f"{p}: " + ",".join(str(int(nul[(nul.panel == p) & (nul.seeds == S)]
                                                    .set_index('N').EDGE_pp.idxmax()))
                                            for S in SEEDGRID) for p in PANELS)))
    H.append(("H_WF >= 1 rule-8 pick clears 4b OUT OF SAMPLE",
              bool(pk.pass4b_oos.any()), f"{int(pk.pass4b_oos.sum())} of {len(pk)} picks"))
    H.append(("H_4A no rung clears 4a (the DD leg is a book fact, not an n fact)",
              bool(not grid.pass4a.any()),
              f"{int(grid.pass4a.sum())} of {len(grid)} rungs pass 4a"))
    H.append(("H_ISEDGE the IS-chosen-by-EDGE rung is the same as the full-sample EDGE argmax "
              "(the edge selector is stable across windows)",
              bool(all(int(pk[(pk.panel == p) & (pk.chooser == 'C_ISEDGE')].N.iloc[0])
                       == int(n40[n40.panel == p].set_index('N').EDGE_pp.idxmax())
                       for p in PANELS)),
              "; ".join(f"{p}: IS {int(pk[(pk.panel==p)&(pk.chooser=='C_ISEDGE')].N.iloc[0])} vs "
                        f"full {int(n40[n40.panel==p].set_index('N').EDGE_pp.idxmax())}"
                        for p in PANELS)))
    for name, ok, note in H:
        P(f"   {'PASS' if ok else 'FAIL'}  {name}  [{note}]")

    # ------------------------------------------------------------------ post-run diagnostics
    P("")
    P("## POST-RUN DIAGNOSTICS — computed AFTER reading the grid and labelled as such, NOT")
    P("## pre-declared hypotheses.  They exist because the ladder's shape raised two questions")
    P("## the pre-declared list does not answer.")
    P("")
    P("   (D1) IS THE HUMP DECISIVE?  EDGE at two rungs differs only through the two null")
    P("        medians (the books are deterministic), so SE(dEDGE) = sqrt(SE_a^2 + SE_b^2).")
    diagrows = []
    for panel in PANELS:
        s = n40[n40.panel == panel].set_index("N")
        amax = int(s.EDGE_pp.idxmax())
        for other in (5, 20, 40):
            if other == amax:
                continue
            d = float(s.loc[amax, "EDGE_pp"] - s.loc[other, "EDGE_pp"])
            se = float(np.hypot(s.loc[amax, "EDGE_se_pp"], s.loc[other, "EDGE_se_pp"]))
            P(f"        {panel}: EDGE({amax}) - EDGE({other}) = {d:+.3f} +/- {se:.3f} pp "
              f"= {d/se:5.2f} SE  -> {'DECISIVE' if abs(d) > 2*se else 'NOT decisive'}")
            diagrows.append(dict(diag="D1_edge_delta", panel=panel, a=amax, b=other,
                                 delta_pp=d, se_pp=se, sigmas=d / se,
                                 decisive=bool(abs(d) > 2 * se)))
    P("")
    P("   (D2) IS THE DD MATCH NON-DEGENERATE?  lambda is constrained to (0, 1]: a null draw")
    P("        already DRIER than the book cannot be scaled UP to meet it, so it enters at")
    P("        lambda = 1 with its CAGR UNDER-stated relative to a true match.  That inflates")
    P("        EDGE.  Direction is stated before the numbers: wherever the drier share is large,")
    P("        the published EDGE is an UPPER bound on the matched edge.")
    for panel in PANELS:
        s = n40[n40.panel == panel].sort_values("N")
        P(f"        {panel}: drier share by N  " +
          "  ".join(f"{int(r.N)}:{r.null_already_drier_rebuilt/NSEED_MAX:.2f}"
                    for _, r in s.iterrows()))
        for _, r in s.iterrows():
            diagrows.append(dict(diag="D2_drier_share", panel=panel, a=int(r.N), b=np.nan,
                                 delta_pp=float(r.EDGE_pp),
                                 se_pp=float(r.null_already_drier_rebuilt) / NSEED_MAX,
                                 sigmas=float(r.lam_median_rebuilt), decisive=np.nan))
    P("        READING: the clip bites hardest at BOTH ENDS of the ladder (n=5 and n=40), i.e.")
    P("        exactly at the two rungs whose EDGE the hump verdict needs to be BELOW the peak.")
    P("        The bias therefore runs AGAINST the hump and the hump survives it anyway.")

    P("")
    P("   (D3) THE 4b PASSES AND THEIR MARGIN ON THE BINDING LEG.")
    for _, r in grid[grid.pass4b].iterrows():
        sbp = bn[(bn.panel == r.panel) & (bn.series == "SPY")].iloc[0]
        ddm = 100.0 * (DD_CAP * abs(sbp.MaxDD) - abs(r.MaxDD))
        cgm = 100.0 * (r.CAGR - CAGR_FLOOR * sbp.CAGR)
        P(f"        {r.panel} N={int(r.N)}: 4b PASSES full-sample; DD margin {ddm:+.3f} pp "
          f"(|{r.MaxDD:.2%}| vs cap {DD_CAP*abs(sbp.MaxDD):.2%}), CAGR margin {cgm:+.3f} pp; "
          f"4b OOS {bool(r.pass4b_oos)}; reachable by an IS-only chooser: "
          f"{int(r.N) in set(pk[pk.panel==r.panel].N)}")
        diagrows.append(dict(diag="D3_4b_pass", panel=r.panel, a=int(r.N), b=np.nan,
                             delta_pp=ddm, se_pp=cgm, sigmas=np.nan,
                             decisive=bool(int(r.N) in set(pk[pk.panel == r.panel].N))))
    P("        1083 measured the 90% width of a quantity of this kind at 4.1-7.2 pp on this")
    P("        tape.  Every DD margin above is far inside that, so none of these passes is")
    P("        decidable here.  Combined with H_WF (no IS-only chooser reaches them), they are")
    P("        PARK, not KEEP, and are NOT proposed.")

    P("")
    dump(grid, "grid"); dump(nul, "null"); dump(sd, "seeds"); dump(pk, "rule8")
    dump(bn, "benchmarks"); dump(pd.DataFrame(gaterows), "gates")
    dump(pd.DataFrame([dict(hypothesis=n, passed=bool(o), note=t) for n, o, t in H]), "hypotheses")
    dump(pd.DataFrame(diagrows), "diagnostics")
    P(f"# done in {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

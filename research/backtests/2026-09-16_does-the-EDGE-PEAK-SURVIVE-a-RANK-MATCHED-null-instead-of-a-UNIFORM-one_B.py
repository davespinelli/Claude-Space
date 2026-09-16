#!/usr/bin/env python3
"""Idea 1085 (lane B, 2026-09-16) — does the EDGE PEAK survive a RANK-MATCHED null instead of a
UNIFORM one?

QUESTION (QUEUE idea 1085, verbatim)
    1082's null draws names UNIFORMLY from everything priced, with no eligibility gate, so EDGE(n)
    mixes selection skill with the 200d/vol gate's own contribution and the mix changes with n.
    Re-price the same 9 rungs against a null that draws uniformly from the ELIGIBLE set only, and
    report how much of the +6.8/+8.3 pp peak is gate rather than rank.  Max 2 params (n, null gate).

THE TWO TUNED DIALS (PROTOCOL rule 4, no more than two)
    1. N        in {5, 8, 10, 12, 15, 20, 25, 30, 40} — 1082's ladder, unchanged.
    2. NULLGATE in {OPEN, ELIG}.
         OPEN  random ranks, elig = ALL PRICED.  1082's / 1071's / the record's convention.
               Reproduced under 1082's EXACT seed recipe so it must agree to machine precision
               (gate G9); it is the control, not a new measurement.
         ELIG  random ranks, elig = the BOOK'S OWN eligibility mask (px > 200d MA AND 20d
               annualised vol < 0.60).  The null now gets the gate for free and differs from the
               book ONLY in how it ORDERS the survivors.  This is the RANK-MATCHED null.
    Everything else FROZEN at 1082/1071/936's construction: cap INF, CAND20 legs
    [(21,252),(0,126),(0,63)], max_vol 0.60, gross 0.75, W cadence, min hold 126, 10 bps, LAG 1,
    40 seeds, REBUILT DD-match convention as the headline.  SEEDS is NOT a dial here (it was
    1082's second dial and is frozen at 40); the nested S = 10/20/40 table below is published as
    a RESOLUTION diagnostic and no verdict is read off it.
    All 9 x 2 = 18 (N, NULLGATE) cells are reported at BOTH panels.  Nothing is hidden.

THE DECOMPOSITION, fixed before any number
    Every null path is scaled to the SAME REALISED |MaxDD| as the BOOK at that same n, so the two
    arms are matched to the identical target and their difference is exactly the difference of the
    two null medians.  Define, in pp of CAGR:

        EDGE_OPEN(n) = 100 * ( CAGR_book(n) - median_s CAGR_nullOPEN(n, s) )   <- 1082's number
        EDGE_ELIG(n) = 100 * ( CAGR_book(n) - median_s CAGR_nullELIG(n, s) )   <- RANK-ONLY edge
        GATE(n)      = EDGE_OPEN(n) - EDGE_ELIG(n)
                     = 100 * ( median_s CAGR_nullELIG - median_s CAGR_nullOPEN )

    GATE(n) is the 200d/vol gate's OWN contribution at that rung, priced on a DD-matched basis and
    with the ranking held at chance.  EDGE_ELIG(n) is what is left for the composite's RANKING.
    The queue's charge is that GATE(n) is not constant in n, so the shape of EDGE_OPEN is partly
    the shape of the gate.  That is measured here, not assumed either way.

DECLARED BEFORE ANY NUMBER — what would vindicate the queue and what would refute it
    (a) The queue's charge is right if GATE(n) VARIES materially across the ladder AND the
        EDGE_ELIG ladder has a different shape (different argmax, or no hump at all).
    (b) The charge is wrong — the peak is a rank fact — if GATE(n) is roughly flat and the
        EDGE_ELIG ladder keeps its argmax with the peak-vs-far-side contrast still decisive
        against the seed SE.
    (c) A third outcome is live and is NOT a refutation of either: GATE(n) is large and flat, in
        which case the record's headline EDGE numbers are BIASED UP by a constant the record never
        named, while the SHAPE conclusion of 1082 survives intact.  That would be a correction to
        the LEVEL of every committed EDGE figure without touching its argmax.
    (d) EDGE IS NOT A KEEP PATH.  The BOOK is byte-identical to 1082's at every rung, so 4a, 4b
        and the rule-8 walk-forward can only reproduce; they are re-run and re-reported in full
        because PROTOCOL rule 8 requires it, and because the null gate DOES move one thing that
        matters — which rung an EDGE-based IS-only chooser picks.  Both EDGE choosers are carried.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists.  Every level here is
    optimistic and every 4b/4a count is an UPPER bound.  EDGE_OPEN, EDGE_ELIG and GATE are all
    within-pool contrasts over the same tape, so the bias very largely cancels out of them; it
    does NOT cancel out of the 4b legs, which are measured against SPY, a real index.
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
SLUG = "does-the-EDGE-PEAK-SURVIVE-a-RANK-MATCHED-null-instead-of-a-UNIFORM-one"
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
LEGS = [(21, 252), (0, 126), (0, 63)]
CAPNAME = "INF"

NS = [5, 8, 10, 12, 15, 20, 25, 30, 40]          # dial 1
GATESET = ["OPEN", "ELIG"]                        # dial 2
NSEED = 40                                        # FROZEN (1082's second dial, retired here)
SNEST = [10, 20, 40]                              # resolution diagnostic only
BISECT = 34

PANELS = ["U56", "B136"]

# committed cross-run anchors
A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
# idea 1082's committed EDGE ladder (40 seeds, REBUILT) — the OPEN arm must reproduce it EXACTLY
A1082_EDGE = {
    ("U56", 5): 5.950388, ("U56", 8): 5.350913, ("U56", 10): 6.205435, ("U56", 12): 6.820183,
    ("U56", 15): 5.215202, ("U56", 20): 5.118123, ("U56", 25): 2.952601, ("U56", 30): 1.545652,
    ("U56", 40): 0.413535,
    ("B136", 5): 5.717069, ("B136", 8): 5.244527, ("B136", 10): 8.323841, ("B136", 12): 6.519566,
    ("B136", 15): 6.833751, ("B136", 20): 4.932357, ("B136", 25): 4.269150, ("B136", 30): 2.810900,
    ("B136", 40): 1.853232,
}
A1082_ARGMAX = {"U56": 12, "B136": 10}
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
    """f(lam) -> NET returns of this book REBUILT at gross lam * its own gross (cap INF, so the
    per-name target is linear in gross).  The PATH is not lam times f(1.0): the cash sleeve does
    not scale.  Verbatim from 1082 so the two runs' nulls are the same object."""
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
    """Target weights under MIN HOLD H and slot count N, cap INF.  Identical to 1071's / 1082's."""
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


def build_null(rng, elig_real, priced, reb, N, H, T, K, gross, gate):
    """Random ranks.  gate OPEN = no eligibility gate (1082's convention, the record's).
    gate ELIG = the BOOK'S OWN gate, so the null differs from the book only in ORDERING."""
    rank_key = rng.random((T, K))
    elig = elig_real if gate == "ELIG" else np.ones((T, K), dtype=bool)
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


def lam_rebuilt(f, sl, target_dd):
    """lambda in (0,1] with |MaxDD(REBUILT(lambda)[sl])| = |target_dd|; None if already drier."""
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


def se_med(x):
    """SE of a median of S iid draws, the record's 1.2533*sigma/sqrt(S) convention."""
    x = np.asarray(x, float)
    return 1.2533 * x.std(ddof=1) / np.sqrt(len(x))


def spearman(a, b):
    """Rank correlation without scipy (no ties expected here; average ranks if there are)."""
    ra = pd.Series(a).rank().values
    rb = pd.Series(b).rank().values
    return float(np.corrcoef(ra, rb)[0, 1])


def main():
    t0 = time.time()
    P(f"# Idea 1085 (lane B, {DATE}) — does the EDGE PEAK survive a RANK-MATCHED null instead of "
      f"a UNIFORM one?")
    P(f"# 2 tuned dials: N {NS} x NULLGATE {GATESET}. ALL 18 cells per panel reported (36 total).")
    P(f"# FROZEN (not dials): seeds {NSEED}, cap {CAPNAME}, CAND20 legs {LEGS}, max_vol {MAXVOL}, "
      f"gross {GROSS0}, cost {COST:.0f} bps, LAG {LAG}, cadence {FREQ}, min hold {HOLD}.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   EDGE_OPEN = book CAGR - median DD-matched null drawn from ALL PRICED (1082's null).")
    P("#   EDGE_ELIG = book CAGR - median DD-matched null drawn from the BOOK'S OWN ELIGIBLE set")
    P("#               (px > 200d MA AND 20d vol < 0.60).  This is the RANK-ONLY edge.")
    P("#   GATE      = EDGE_OPEN - EDGE_ELIG = the 200d/vol gate's own DD-matched contribution.")
    P("#   (a) queue VINDICATED if GATE varies materially in n AND the EDGE_ELIG ladder changes")
    P("#       shape (argmax moves, or the hump goes).")
    P("#   (b) queue REFUTED if GATE is ~flat and EDGE_ELIG keeps 1082's argmax with the")
    P("#       peak-vs-far-side contrast still decisive against the seed SE.")
    P("#   (c) THIRD outcome, neither: GATE large AND flat -> every committed EDGE LEVEL in the")
    P("#       record is biased up by a constant nobody named, while 1082's SHAPE survives.")
    P("#   (d) EDGE IS NOT A KEEP PATH.  The book is byte-identical to 1082's, so 4a/4b/rule 8")
    P("#       can only reproduce; they are re-run in full anyway (rule 8) and BOTH EDGE-based")
    P("#       IS-only choosers (OPEN and ELIG) are carried, since the gate CAN move the pick.")
    P("")

    rows, nullrows, gaterows, seedrows, nestrows = [], [], [], [], []
    picks, benchrows, eligrows = [], [], []
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
        rebw = reb[reb >= WARMUP]

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

        # ---- HOW MUCH DOES THE GATE ACTUALLY BIND? (a property of the tape, not of any rung) ---
        ne = (elig & priced)[rebw].sum(axis=1)
        npr = priced[rebw].sum(axis=1)
        eligrows.append(dict(panel=panel, reb_dates=int(len(rebw)),
                             mean_priced=float(npr.mean()), mean_eligible=float(ne.mean()),
                             mean_elig_share=float((ne / npr).mean()),
                             min_eligible=int(ne.min()), p05_eligible=float(np.percentile(ne, 5)),
                             frac_reb_elig_lt_5=float((ne < 5).mean()),
                             frac_reb_elig_lt_20=float((ne < 20).mean()),
                             frac_reb_elig_lt_40=float((ne < 40).mean())))
        P(f"   GATE BINDING: {ne.mean():.1f} of {npr.mean():.1f} names eligible at the median "
          f"rebalance ({(ne/npr).mean():.1%}); min {int(ne.min())}; "
          f"share of rebalances with <40 eligible {(ne < 40).mean():.1%}")

        # ---- GATES ---------------------------------------------------------------------------
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
            gates["G2 CROSS-RUN vs 936/1071/1082 committed W/H126 N=20 triple"] = (d2, d2 < 5e-3)
            d3 = max(abs(sb["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
                     abs(sb["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
                     abs(sb["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
            gates["G3 CROSS-RUN SPY OOS triple"] = (d3, d3 < 5e-4)
            d6 = abs(live_dd - LIVE_MAXDD_COMMITTED)
            gates["G6 live RULES v2 MaxDD == committed -12.05%"] = (d6, d6 < 5e-4)
            rngc = np.random.default_rng(mdseed(panel, 20, CAPNAME, 0))
            Wn0, _ = build_null(rngc, elig, priced, reb, 20, HOLD, T, K, GROSS0, "OPEN")
            fn0 = gross_rescaler(rets, lagmat(Wn0), mkl)
            dds = [abs(maxdd(fn0(l)[warm])) for l in np.linspace(0.1, 1.0, 19)]
            viol = float(max(0.0, max(dds[i] - dds[i + 1] for i in range(len(dds) - 1))))
            gates["G4c |MaxDD| of the REBUILT null is monotone in lambda"] = (viol, viol < 1e-12)
            rngd = np.random.default_rng(mdseed(panel, 20, CAPNAME, "ELIG", 0))
            We0, _ = build_null(rngd, elig, priced, reb, 20, HOLD, T, K, GROSS0, "ELIG")
            rnge = np.random.default_rng(mdseed(panel, 20, CAPNAME, "ELIG", 0))
            We0b, _ = build_null(rnge, elig, priced, reb, 20, HOLD, T, K, GROSS0, "ELIG")
            d7 = float(np.abs(We0 - We0b).max())
            gates["G7 the ELIG null draw is deterministic in its seed recipe"] = (d7, d7 == 0.0)
            dg = float(np.abs(We0 - Wn0).max())
            gates["G10 the two null ARMS are genuinely different books (max |dW| > 0)"] = (dg, dg > 0)
            # G11: every name the ELIG null ever OPENS a new position in was eligible that day.
            # (Held names may age out of eligibility under the min hold — that is the book's own
            # behaviour and is matched.)  Checked on the opening rebalance rows only.
            bad = 0
            prev = np.zeros(K, dtype=bool)
            for t in reb:
                now = We0[t] > 0
                opened = now & ~prev
                bad += int((opened & ~(elig[t] & priced[t])).sum())
                prev = now
            gates["G11 every ELIG-null OPENING is an eligible name that day"] = (
                float(bad), bad == 0)

        # ---- the ladder ----------------------------------------------------------------------
        for N in NS:
            W, nsel = build(rank_key, elig, priced, reb, N, HOLD, T, K, GROSS0)
            g, tn, _ = nrun(rets, lagmat(W), mkl)
            r = g - tn * COST / 1e4
            b = blocks(r, warm, ins, oos)
            l4b, l4a, l4bo = legs_4b(b, sb), legs_4a(b, lb), legs_4b_oos(b, sb)
            row = dict(panel=panel, N=N, cap=CAPNAME, mean_nsel=float(nsel.mean()),
                       turnover=float(tn[warm].sum() / (warm.sum() / 252.0)), **b,
                       **l4b, **l4a, **l4bo,
                       pass4b=all(l4b.values()), pass4a=all(l4a.values()),
                       pass4b_oos=all(l4bo.values()))
            row["pass4b_full_and_oos"] = row["pass4b"] and row["pass4b_oos"]

            per = {}
            for gate in GATESET:
                c_full, c_is, lam_r, nsel_null = [], [], [], []
                raw_c, raw_d, raw_s = [], [], []
                for s in range(NSEED):
                    sd = (mdseed(panel, N, CAPNAME, s) if gate == "OPEN"
                          else mdseed(panel, N, CAPNAME, "ELIG", s))
                    rng = np.random.default_rng(sd)
                    Wn, nn = build_null(rng, elig, priced, reb, N, HOLD, T, K, GROSS0, gate)
                    nsel_null.append(float(nn.mean()))
                    fn = gross_rescaler(rets, lagmat(Wn), mkl)
                    base = fn(1.0)
                    rc, rs, rd = fmet(base[warm])       # UNMATCHED: immune to the lambda<=1 clip
                    raw_c.append(rc); raw_s.append(rs); raw_d.append(rd)
                    lr = lam_rebuilt(fn, warm, b["MaxDD"])
                    c_full.append(fmet(base[warm] if lr is None else fn(lr)[warm])[0])
                    lam_r.append(1.0 if lr is None else lr)
                    lri = lam_rebuilt(fn, ins, b["IS_MaxDD"])
                    c_is.append(fmet(base[ins] if lri is None else fn(lri)[ins])[0])
                    seedrows.append(dict(panel=panel, N=N, nullgate=gate, seed=s,
                                         null_CAGR_rebuilt=c_full[-1],
                                         null_IS_CAGR_rebuilt=c_is[-1], lam_rebuilt=lam_r[-1],
                                         null_raw_CAGR=rc, null_raw_MaxDD=rd, null_raw_Sharpe=rs,
                                         null_mean_nsel=nsel_null[-1]))
                c_full, c_is = np.array(c_full), np.array(c_is)
                raw_c, raw_d, raw_s = np.array(raw_c), np.array(raw_d), np.array(raw_s)
                per[gate] = (c_full, c_is)
                nullrows.append(dict(
                    panel=panel, N=N, nullgate=gate, seeds=NSEED,
                    book_CAGR=b["CAGR"], book_MaxDD=b["MaxDD"], book_IS_CAGR=b["IS_CAGR"],
                    book_mean_nsel=float(nsel.mean()), null_mean_nsel=float(np.mean(nsel_null)),
                    null_CAGR_med=float(np.median(c_full)),
                    null_IS_CAGR_med=float(np.median(c_is)),
                    EDGE_pp=100.0 * (b["CAGR"] - float(np.median(c_full))),
                    EDGE_IS_pp=100.0 * (b["IS_CAGR"] - float(np.median(c_is))),
                    EDGE_se_pp=100.0 * se_med(c_full),
                    null_CAGR_sd=float(c_full.std(ddof=1)),
                    null_CAGR_p90=float(np.percentile(c_full, 90)),
                    null_CAGR_max=float(c_full.max()),
                    book_pct_of_null=float((c_full < b["CAGR"]).mean()),
                    lam_median=float(np.median(lam_r)),
                    null_already_drier=int(sum(1 for x in lam_r if x == 1.0)),
                    null_raw_CAGR_med=float(np.median(raw_c)),
                    null_raw_MaxDD_med=float(np.median(raw_d)),
                    null_raw_Sharpe_med=float(np.median(raw_s)),
                    null_raw_CAGR_se=100.0 * se_med(raw_c),
                ))
                for S in SNEST:
                    nestrows.append(dict(panel=panel, N=N, nullgate=gate, seeds=S,
                                         EDGE_pp=100.0 * (b["CAGR"] - float(np.median(c_full[:S]))),
                                         EDGE_se_pp=100.0 * se_med(c_full[:S])))
                row[f"EDGE_{gate}_pp"] = 100.0 * (b["CAGR"] - float(np.median(c_full)))
                row[f"EDGE_IS_{gate}_pp"] = 100.0 * (b["IS_CAGR"] - float(np.median(c_is)))
                row[f"EDGE_se_{gate}_pp"] = 100.0 * se_med(c_full)
                row[f"drier_{gate}"] = int(sum(1 for x in lam_r if x == 1.0))
                row[f"raw_CAGR_{gate}"] = float(np.median(raw_c))
                row[f"raw_MaxDD_{gate}"] = float(np.median(raw_d))
                row[f"raw_Sharpe_{gate}"] = float(np.median(raw_s))
                row[f"raw_CAGR_se_{gate}_pp"] = 100.0 * se_med(raw_c)
            row["GATE_pp"] = row["EDGE_OPEN_pp"] - row["EDGE_ELIG_pp"]
            row["GATE_IS_pp"] = row["EDGE_IS_OPEN_pp"] - row["EDGE_IS_ELIG_pp"]
            row["GATE_se_pp"] = float(np.hypot(row["EDGE_se_OPEN_pp"], row["EDGE_se_ELIG_pp"]))
            row["GATE_share"] = (row["GATE_pp"] / row["EDGE_OPEN_pp"]
                                 if row["EDGE_OPEN_pp"] != 0 else np.nan)
            # the SAME contrast with NO DD match at all: immune to the lambda<=1 clip, which
            # bites the two arms at different rates.  Sign convention matched to GATE_pp.
            row["GATE_raw_pp"] = 100.0 * (row["raw_CAGR_ELIG"] - row["raw_CAGR_OPEN"])
            row["GATE_raw_se_pp"] = float(np.hypot(row["raw_CAGR_se_OPEN_pp"],
                                                   row["raw_CAGR_se_ELIG_pp"]))
            row["GATE_raw_dd_pp"] = 100.0 * (abs(row["raw_MaxDD_ELIG"])
                                             - abs(row["raw_MaxDD_OPEN"]))
            rows.append(row)
            P(f"   N={N:2d} done  book {b['CAGR']:.2%} / {b['Sharpe']:.4f} / {b['MaxDD']:.2%}  "
              f"EDGE_OPEN {row['EDGE_OPEN_pp']:+.3f}  EDGE_ELIG {row['EDGE_ELIG_pp']:+.3f}  "
              f"GATE {row['GATE_pp']:+.3f} pp  ({time.time()-t0:.0f}s)")

        # ---- RULE 8: IS-only choosers pick N, OOS read ONCE ----------------------------------
        gp = pd.DataFrame([r for r in rows if r["panel"] == panel])
        for cname, key, asc in [("C_ISSHARPE", "IS_Sharpe", False), ("C_ISDD", "IS_MaxDD", False),
                                ("C_ISCAGR", "IS_CAGR", False),
                                ("C_ISEDGE_OPEN", "EDGE_IS_OPEN_pp", False),
                                ("C_ISEDGE_ELIG", "EDGE_IS_ELIG_pp", False)]:
            pick = gp.sort_values(key, ascending=asc).iloc[0]
            picks.append(dict(panel=panel, chooser=cname, N=int(pick["N"]),
                              IS_Sharpe=pick["IS_Sharpe"], IS_MaxDD=pick["IS_MaxDD"],
                              IS_EDGE_OPEN_pp=pick["EDGE_IS_OPEN_pp"],
                              IS_EDGE_ELIG_pp=pick["EDGE_IS_ELIG_pp"],
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
    nest = pd.DataFrame(nestrows)
    eg = pd.DataFrame(eligrows)

    # G9: the OPEN arm must reproduce 1082's committed EDGE ladder to machine precision
    d9 = max(abs(float(grid[(grid.panel == p) & (grid.N == n)].EDGE_OPEN_pp.iloc[0]) - v)
             for (p, n), v in A1082_EDGE.items())
    gates["G9 CROSS-RUN the OPEN arm reproduces 1082's 18 committed EDGE figures"] = (d9, d9 < 1e-5)
    ddspread = float(100 * (grid[grid.panel == "U56"].MaxDD.max()
                            - grid[grid.panel == "U56"].MaxDD.min()))
    gates["G8 the n dial is LIVE (U56 |MaxDD| spread >= 2 pp across the ladder)"] = (
        ddspread, ddspread >= 2.0)
    gsp = float(grid.GATE_pp.abs().max())
    gates["G12 the NULL GATE dial is LIVE (some |GATE| > 0.25 pp somewhere)"] = (gsp, gsp > 0.25)

    P("")
    P("## GATES (printed before any result number)")
    for k, (v, ok) in gates.items():
        P(f"   {'PASS' if ok else 'FAIL'}  {k}: |d| = {v:.3e}")
        gaterows.append(dict(gate=k, value=v, passed=bool(ok)))

    P("")
    P(f"## HOW MUCH THE GATE BINDS (a tape fact; both null arms see it)")
    for _, r in eg.iterrows():
        P(f"   {r.panel:5s} {r.mean_eligible:6.1f} of {r.mean_priced:6.1f} eligible "
          f"({r.mean_elig_share:.1%}) at the mean rebalance; min {int(r.min_eligible)}, "
          f"p05 {r.p05_eligible:.0f}; rebalances with <5/<20/<40 eligible "
          f"{r.frac_reb_elig_lt_5:.1%}/{r.frac_reb_elig_lt_20:.1%}/{r.frac_reb_elig_lt_40:.1%}")

    P("")
    P(f"## THE LADDER — book at every N (unchanged from 1082 by construction; rule-4 scoring)")
    for panel in PANELS:
        s = grid[grid.panel == panel].sort_values("N")
        P(f"   --- {panel} ---")
        P("       N  nsel   turn    CAGR    Sharpe   MaxDD      H1/H2        OOS C/S/DD"
          "             4b 4a 4bOOS")
        for _, r in s.iterrows():
            P(f"      {int(r.N):2d} {r.mean_nsel:5.1f} {r.turnover:6.2f} {r.CAGR:7.2%} "
              f"{r.Sharpe:8.4f} {r.MaxDD:8.2%}  {r.H1:.3f}/{r.H2:.3f}  "
              f"{r.OOS_CAGR:6.2%}/{r.OOS_Sharpe:.4f}/{r.OOS_MaxDD:7.2%}"
              f"      {int(r.pass4b)}  {int(r.pass4a)}   {int(r.pass4b_oos)}")
        P(f"      4b full {int(s.pass4b.sum())}/{len(s)}   4b OOS {int(s.pass4b_oos.sum())}/{len(s)}"
          f"   4a {int(s.pass4a.sum())}/{len(s)}")

    P("")
    P(f"## THE QUESTION ITSELF — EDGE under each null gate, and the GATE's own share "
      f"({NSEED} seeds, REBUILT)")
    for panel in PANELS:
        s = grid[grid.panel == panel].sort_values("N")
        P(f"   --- {panel} ---")
        P("       N   book CAGR  nullOPEN  nullELIG  EDGE_OPEN  EDGE_ELIG     GATE  +/-SE  share"
          "   drierO/E")
        for _, r in s.iterrows():
            no = float(nul[(nul.panel == panel) & (nul.N == r.N)
                           & (nul.nullgate == "OPEN")].null_CAGR_med.iloc[0])
            ne_ = float(nul[(nul.panel == panel) & (nul.N == r.N)
                            & (nul.nullgate == "ELIG")].null_CAGR_med.iloc[0])
            P(f"      {int(r.N):2d}    {r.CAGR:7.2%}   {no:7.2%}   {ne_:7.2%}  "
              f"{r.EDGE_OPEN_pp:+9.3f}  {r.EDGE_ELIG_pp:+9.3f} {r.GATE_pp:+8.3f} "
              f"{r.GATE_se_pp:6.3f} {r.GATE_share:6.1%}   {int(r.drier_OPEN):2d}/{int(r.drier_ELIG):2d}")
        aO = int(s.loc[s.EDGE_OPEN_pp.idxmax(), "N"])
        aE = int(s.loc[s.EDGE_ELIG_pp.idxmax(), "N"])
        P(f"      argmax EDGE_OPEN N={aO} ({s.EDGE_OPEN_pp.max():+.3f} pp)   "
          f"argmax EDGE_ELIG N={aE} ({s.EDGE_ELIG_pp.max():+.3f} pp)")
        P(f"      GATE range over the ladder: {s.GATE_pp.min():+.3f} .. {s.GATE_pp.max():+.3f} pp "
          f"(spread {s.GATE_pp.max()-s.GATE_pp.min():.3f} pp), median share of EDGE_OPEN "
          f"{s.GATE_share.median():.1%}")

    P("")
    P("## HYPOTHESES (declared before the run, scored as written)")
    hyp = []

    def H(name, ok, detail):
        hyp.append(dict(hypothesis=name, passed=bool(ok), detail=detail))
        P(f"   {'PASS' if ok else 'FAIL'}  {name}  [{detail}]")

    for panel in PANELS:
        s = grid[grid.panel == panel].sort_values("N").set_index("N")
        eO, eE, ga = s.EDGE_OPEN_pp, s.EDGE_ELIG_pp, s.GATE_pp
        aO, aE = int(eO.idxmax()), int(eE.idxmax())
        H(f"H_ARGMAX[{panel}] the EDGE argmax is UNCHANGED by the null gate", aE == aO,
          f"OPEN argmax N={aO} (1082 committed {A1082_ARGMAX[panel]}), ELIG argmax N={aE}")
        seP = float(np.hypot(s.EDGE_se_ELIG_pp.loc[aE], s.EDGE_se_ELIG_pp.loc[40]))
        dpk = float(eE.loc[aE] - eE.loc[40])
        H(f"H_HUMP[{panel}] under ELIG the peak still beats the far side decisively (>2 SE)",
          dpk > 2 * seP, f"EDGE_ELIG({aE}) - EDGE_ELIG(40) = {dpk:+.3f} +/- {seP:.3f} pp = "
                         f"{dpk/seP:.2f} SE")
        H(f"H_SIG[{panel}] the ELIG peak itself exceeds 2 seed-SEs (rank skill is not noise)",
          float(eE.loc[aE]) > 2 * float(s.EDGE_se_ELIG_pp.loc[aE]),
          f"{eE.loc[aE]:+.3f} pp vs 2 SE = {2*s.EDGE_se_ELIG_pp.loc[aE]:.3f} pp")
        H(f"H_GATEPOS[{panel}] GATE > 0 at EVERY rung (the gate helps everywhere)",
          bool((ga > 0).all()), f"{int((ga>0).sum())} of {len(ga)} rungs positive; "
                                f"min {ga.min():+.3f} pp at N={int(ga.idxmin())}")
        gsprd = float(ga.max() - ga.min())
        gse = float(np.hypot(s.GATE_se_pp.max(), s.GATE_se_pp.min()))
        H(f"H_GATEFLAT[{panel}] GATE is FLAT in n (ladder spread <= 2 SE) — if it FAILS the "
          f"queue's 'the mix changes with n' is vindicated",
          gsprd <= 2 * gse, f"spread {gsprd:.3f} pp vs 2 SE = {2*gse:.3f} pp "
                            f"({ga.min():+.3f} at N={int(ga.idxmin())} .. {ga.max():+.3f} at "
                            f"N={int(ga.idxmax())})")
        H(f"H_HALF[{panel}] the GATE is at least HALF of the peak EDGE_OPEN",
          float(ga.loc[aO]) >= 0.5 * float(eO.loc[aO]),
          f"GATE({aO}) {ga.loc[aO]:+.3f} pp vs half of EDGE_OPEN({aO}) {0.5*eO.loc[aO]:.3f} pp "
          f"= {ga.loc[aO]/eO.loc[aO]:.1%} of it")
        H(f"H_SLOPE[{panel}] under ELIG the EDGE ladder is monotone DECREASING in n "
          f"(the queue's ORIGINAL slope story, re-tested on the fairer null)",
          bool(all(eE.iloc[i] >= eE.iloc[i + 1] for i in range(len(eE) - 1))),
          " -> ".join(f"{v:+.2f}" for v in eE.values))
        H(f"H_RANKORDER[{panel}] the two ladders agree on the ORDER of all 9 rungs "
          f"(Spearman == 1)",
          abs(spearman(eO.values, eE.values) - 1.0) < 1e-12,
          f"Spearman {spearman(eO.values, eE.values):.4f}")

    H("H_WF >= 1 rule-8 pick clears 4b OUT OF SAMPLE",
      bool(pk.pass4b_oos.any()), f"{int(pk.pass4b_oos.sum())} of {len(pk)} picks")
    H("H_EDGEPICK the two EDGE-based IS-only choosers pick the SAME rung on both panels",
      bool((pk[pk.chooser == "C_ISEDGE_OPEN"].N.values
            == pk[pk.chooser == "C_ISEDGE_ELIG"].N.values).all()),
      "; ".join(f"{p}: OPEN {int(pk[(pk.panel==p)&(pk.chooser=='C_ISEDGE_OPEN')].N.iloc[0])} vs "
                f"ELIG {int(pk[(pk.panel==p)&(pk.chooser=='C_ISEDGE_ELIG')].N.iloc[0])}"
                for p in PANELS))
    H("H_4A no rung clears 4a (the DD leg is a book fact, not an n fact)",
      not bool(grid.pass4a.any()), f"{int(grid.pass4a.sum())} of {len(grid)} rungs pass 4a")

    P("")
    P("## RULE 8 — N chosen on IS (2009-2016) ONLY, OOS (2017-2026) read ONCE")
    P("    panel chooser         N   IS_S   IS_EDGE O/E      OOS C/S/DD           SPY OOS C/S/DD"
      "         4bOOS")
    for _, r in pk.iterrows():
        P(f"    {r.panel:5s} {r.chooser:14s} {int(r.N):2d} {r.IS_Sharpe:6.3f}  "
          f"{r.IS_EDGE_OPEN_pp:+6.2f}/{r.IS_EDGE_ELIG_pp:+6.2f}  "
          f"{r.OOS_CAGR:6.2%}/{r.OOS_Sharpe:.4f}/{r.OOS_MaxDD:7.2%}  "
          f"{r.spy_OOS_CAGR:6.2%}/{r.spy_OOS_Sharpe:.4f}/{r.spy_OOS_MaxDD:7.2%}   "
          f"{int(r.pass4b_oos)}  (O_S {int(r.O_S)} O_DD {int(r.O_DD)} O_CAGR {int(r.O_CAGR)})")

    P("")
    P("## POST-RUN DIAGNOSTICS — computed AFTER reading the grid and labelled as such, NOT")
    P("## pre-declared hypotheses.")
    diags = []

    def D(tag, panel, k, v, note):
        diags.append(dict(tag=tag, panel=panel, key=k, value=v, note=note))

    P("")
    P("   (D1) PEAK-vs-NEIGHBOUR DECISIVENESS under BOTH nulls.  EDGE at two rungs differs only")
    P("        through the null medians (the books are deterministic), so SE(dEDGE) = hypot.")
    for panel in PANELS:
        s = grid[grid.panel == panel].sort_values("N").set_index("N")
        for gate in GATESET:
            e = s[f"EDGE_{gate}_pp"]
            se = s[f"EDGE_se_{gate}_pp"]
            a = int(e.idxmax())
            for other in [5, 20, 40]:
                if other == a:
                    continue
                d = float(e.loc[a] - e.loc[other])
                ss = float(np.hypot(se.loc[a], se.loc[other]))
                P(f"        {panel:5s} {gate:4s}: EDGE({a}) - EDGE({other}) = {d:+7.3f} +/- "
                  f"{ss:.3f} pp = {d/ss:6.2f} SE  -> "
                  f"{'DECISIVE' if abs(d) > 2*ss else 'NOT decisive'}")
                D("D1", panel, f"{gate}:{a}-{other}", d / ss,
                  "DECISIVE" if abs(d) > 2 * ss else "NOT decisive")

    P("")
    P("   (D2) THE lambda CLIP.  lambda is capped at 1: a null draw already DRIER than the book")
    P("        enters unmatched with its CAGR under-stated, which INFLATES EDGE.  Where the drier")
    P("        share is large the published EDGE is an UPPER bound.  Both arms shown.")
    for panel in PANELS:
        s = grid[grid.panel == panel].sort_values("N")
        P(f"        {panel:5s} OPEN drier/40 by N: " +
          "  ".join(f"{int(r.N)}:{int(r.drier_OPEN):2d}" for _, r in s.iterrows()))
        P(f"        {panel:5s} ELIG drier/40 by N: " +
          "  ".join(f"{int(r.N)}:{int(r.drier_ELIG):2d}" for _, r in s.iterrows()))
        D("D2", panel, "OPEN_drier_total", float(s.drier_OPEN.sum()), "")
        D("D2", panel, "ELIG_drier_total", float(s.drier_ELIG.sum()), "")

    P("")
    P("   (D3) RESOLUTION.  The nested S = 10/20/40 EDGE table (seeds are FROZEN at 40 here and")
    P("        no verdict is read off this; it says only how tight the 40-seed numbers are).")
    for panel in PANELS:
        for gate in GATESET:
            t = nest[(nest.panel == panel) & (nest.nullgate == gate)]
            am = {S: int(t[t.seeds == S].sort_values("EDGE_pp").N.iloc[-1]) for S in SNEST}
            P(f"        {panel:5s} {gate:4s} argmax at S=10/20/40: "
              f"{am[10]}/{am[20]}/{am[40]}   mean SE at S=40 "
              f"{t[t.seeds==40].EDGE_se_pp.mean():.3f} pp")
            D("D3", panel, f"{gate}_argmax_S10_S20_S40", float(am[40]),
              f"{am[10]}/{am[20]}/{am[40]}")

    P("")
    P("   (D5) THE CLIP-FREE CONTROL.  The lambda <= 1 clip bites the two arms at DIFFERENT")
    P("        rates (D2), and a clipped draw has its CAGR under-stated, which INFLATES that")
    P("        arm's EDGE.  So a GATE computed from MATCHED medians is confounded wherever the")
    P("        two drier counts differ.  Below is the SAME contrast with NO DD MATCH at all —")
    P("        both nulls simply run at gross 0.75.  It cannot be a clip artefact.  It is not a")
    P("        risk-matched comparison either, so its drawdown column is reported beside it.")
    P("        GATE_raw > 0 means the ELIG null EARNS MORE unmatched (gate is worth something);")
    P("        GATE_raw < 0 means gating to eligible names and picking at random earns LESS.")
    for panel in PANELS:
        s = grid[grid.panel == panel].sort_values("N")
        P(f"        --- {panel} ---")
        P("          N   rawOPEN C/DD/S       rawELIG C/DD/S       GATE_raw  +/-SE    dDD"
          "   GATE_matched")
        for _, r in s.iterrows():
            P(f"         {int(r.N):2d}  {r.raw_CAGR_OPEN:6.2%}/{r.raw_MaxDD_OPEN:7.2%}/"
              f"{r.raw_Sharpe_OPEN:.3f}  {r.raw_CAGR_ELIG:6.2%}/{r.raw_MaxDD_ELIG:7.2%}/"
              f"{r.raw_Sharpe_ELIG:.3f}  {r.GATE_raw_pp:+8.3f} {r.GATE_raw_se_pp:6.3f} "
              f"{r.GATE_raw_dd_pp:+6.2f}   {r.GATE_pp:+8.3f}")
            D("D5", panel, f"GATE_raw_N{int(r.N)}", float(r.GATE_raw_pp),
              f"{'DECISIVE' if abs(r.GATE_raw_pp) > 2*r.GATE_raw_se_pp else 'NOT decisive'}; "
              f"dDD {r.GATE_raw_dd_pp:+.2f} pp; matched GATE {r.GATE_pp:+.3f}")
        agree = int(((s.GATE_raw_pp > 0) == (s.GATE_pp > 0)).sum())
        P(f"          SIGN AGREEMENT between the matched GATE and the clip-free GATE_raw: "
          f"{agree} of {len(s)} rungs")
        P(f"          GATE_raw mean {s.GATE_raw_pp.mean():+.3f} pp, range {s.GATE_raw_pp.min():+.3f}"
          f" .. {s.GATE_raw_pp.max():+.3f}; the ELIG null is DRIER at "
          f"{int((s.GATE_raw_dd_pp < 0).sum())} of {len(s)} rungs")
        D("D5", panel, "sign_agreement", float(agree), f"of {len(s)} rungs")
        D("D5", panel, "GATE_raw_mean_pp", float(s.GATE_raw_pp.mean()), "")

    P("")
    P("   (D4) WHAT THE GATE IS WORTH IN ITS OWN RIGHT, read off the null medians alone:")
    for panel in PANELS:
        s = grid[grid.panel == panel].sort_values("N")
        P(f"        {panel:5s} GATE mean {s.GATE_pp.mean():+.3f} pp, median "
          f"{s.GATE_pp.median():+.3f}, sd across rungs {s.GATE_pp.std(ddof=1):.3f}; "
          f"mean share of EDGE_OPEN {s.GATE_share.mean():.1%}")
        D("D4", panel, "GATE_mean_pp", float(s.GATE_pp.mean()), "")
        D("D4", panel, "GATE_sd_across_rungs_pp", float(s.GATE_pp.std(ddof=1)), "")
        D("D4", panel, "GATE_mean_share", float(s.GATE_share.mean()), "")

    P("")
    dump(grid, "grid")
    dump(nul, "null")
    dump(sd, "seeds")
    dump(nest, "resolution")
    dump(pk, "rule8")
    dump(bn, "benchmarks")
    dump(eg, "eligibility")
    dump(pd.DataFrame(gaterows), "gates")
    dump(pd.DataFrame(hyp), "hypotheses")
    dump(pd.DataFrame(diags), "diagnostics")
    P(f"# done in {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

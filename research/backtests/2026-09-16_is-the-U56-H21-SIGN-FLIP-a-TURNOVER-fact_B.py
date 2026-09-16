#!/usr/bin/env python3
"""Idea 1106 (lane B, 2026-09-16) — is the U56 H=21 SIGN FLIP a TURNOVER fact?

QUESTION (QUEUE idea 1106, verbatim)
    idea 1097 found GATE = EDGE_OPEN - EDGE_ELIG is negative at 81 of 94 committed cells but
    POSITIVE at 6 of 9 rungs in one slice, U56 at min hold 21, where the ELIG null is the
    EASIER comparand.  A 21-day hold lets a random ordering re-draw four times as often, so the
    200d/vol gate's cost to a random book should scale with re-draw frequency.  Walk H below 21
    (5, 10, 21) and price GATE against realised null turnover.  Max 2 params (H, panel).

THE TWO TUNED DIALS (PROTOCOL rule 4, no more than two)
    1. H (min hold, in index positions = trading days) walked at {5, 10, 21}.  On a WEEKLY
       cadence the rebalance dates are ~5 trading days apart, so these rungs are "the null
       re-draws every 1 / 2 / 4 rebalances".  H=5 is the floor: nothing is ever young at the
       next rebalance, so the ordering is re-drawn in full every week.
       The record's committed H=63 and H=126 rungs are CARRIED AS CONTEXT, not tuned: they are
       1086's own coordinates, re-run byte-identically and used as cross-run reproduction gates
       (G5/G6).  Including them makes the H axis a 5-rung ladder instead of a 3-rung one at no
       cost in degrees of freedom — nothing about them is chosen here.
    2. PANEL in {U56, B136}.  1097's flip lives on U56 only; B136 is the out-of-slice test of
       whether the flip is a property of re-draw frequency (which B136 has MORE of: its H=21
       book turns 9.54x/yr against U56's 8.05x) or a property of that one panel.

    THE N LADDER IS NOT A DIAL.  N in {5,8,10,12,15,20,25,30,40} is taken exactly as 1082/1086
    committed it, and every rung is published.  Everything else is frozen at 1082/1085/1086's
    construction: cap INF, REBUILT DD-match, 40 seeds, 34 bisection steps, CAND20 legs
    [(21,252),(0,126),(0,63)], max_vol 0.60, gross 0.75, W cadence, 10 bps, LAG 1.
    The null SEED RECIPE is 1097's verbatim — md5(panel, N, "INF", s) for OPEN and
    md5(panel, N, "INF", "ELIG", s) for ELIG — and it does NOT contain H.  That is deliberate
    and load-bearing: the SAME 40 random orderings are replayed at every rung, so a move in
    GATE along the H axis is the min hold moving, not a different draw.

THE TWO NULLS (1085's alphabet, unchanged)
    OPEN  random ranks, elig = ALL PRICED.  The convention every committed EDGE figure in the
          record was measured under.
    ELIG  random ranks, elig = the BOOK'S OWN gate (px > 200d MA AND 20d ann. vol < 0.60).  The
          null gets the gate for free and differs from the book only in how it ORDERS survivors.
    GATE = EDGE_OPEN - EDGE_ELIG.  GATE < 0 <=> the ELIG null is the HARDER comparand <=> the
    committed (OPEN) figure is a LOWER bound on rank skill.  GATE > 0 is the sign flip 1106 asks
    about: the gate-free null is harder, i.e. the 200d/vol gate is HELPING a random ordering.

WHAT "REALISED NULL TURNOVER" MEANS, fixed before any number
    NTURN_raw      the null book's annualised one-way turnover at gross 0.75 (lam = 1), median
                   over the 40 seeds, measured by EVALUATING THE BOOK AT lam = 1.  This is the
                   re-draw-frequency quantity 1106 names.
    NTURN_matched  the turnover actually CHARGED after the DD-match rebuild at lam.  Reported
                   because it, not NTURN_raw, is what the 10 bps is levied on.
                   DEFECT FOUND AND FIXED IN THIS RUN'S FIRST PASS, recorded because it would
                   have been invisible: turnover is NOT exactly lam * the lam=1 turnover.  The
                   rebuild's cost term is lam * |W - A/V(lam)| and the cash sleeve inside V does
                   not scale, so NTURN_matched / lam is only an approximation of NTURN_raw
                   (max deviation measured at gate G1d below).  The first pass computed
                   NTURN_raw that way; it now comes from a direct lam = 1 evaluation, and G1d
                   PUBLISHES the size of the error the shortcut would have carried instead of
                   asserting a linearity that does not hold.
    DTURN          NTURN_raw(OPEN) - NTURN_raw(ELIG).  1106's mechanism in one number: the
                   claim is that the gate's cost to a random book is a turnover cost, so the
                   gate-free null must be turning over MORE, and more so as H falls.
    NEW_per_reb    names newly taken per rebalance date, median over seeds — the literal
                   re-draw count, reported alongside turnover so "re-draws four times as often"
                   is checked and not assumed.

DECLARED BEFORE ANY NUMBER — what vindicates 1106's premise and what refutes it
    H_TURNOVER   the premise.  Spearman(GATE_pp, NTURN_raw(OPEN)) > 0 POOLED and > 0 WITHIN
                 EACH PANEL.  REFUTED by a non-positive pooled rho, or by the two panels
                 disagreeing in sign (which would make GATE a panel fact wearing a turnover
                 costume).
    H_DTURN      the named mechanism.  DTURN > 0 at every cell (the gate-free null turns over
                 more) AND Spearman(GATE_pp, DTURN) > 0.  REFUTED by either failing.
    H_MONOTONE   on U56, mean GATE_pp rises monotonically as H falls 126 -> 63 -> 21 -> 10 -> 5.
                 REFUTED by any inversion between adjacent rungs.
    H_FLIP_EXTENDS  U56 carries MORE positive-GATE cells at H=10 and H=5 than the 6 of 9 it
                 carries at H=21.  This is the sharpest form of the premise and the one a
                 turnover story most clearly predicts.  REFUTED by fewer.
    H_PANEL      the premise is panel-free.  B136's nulls re-draw MORE than U56's at every rung,
                 so if GATE is a turnover fact B136 must flip positive at H=5/10 too.  REFUTED
                 if B136 stays negative at every rung of the walk while U56 flips.
    H_REDRAW     "a 21-day hold lets a random ordering re-draw four times as often" is checked
                 literally: NEW_per_reb at H=5 is ~4x NEW_per_reb at H=21.  REFUTED by a ratio
                 outside [3, 5].

    EDGE IS NOT A KEEP PATH AND THIS RUN CANNOT MOVE ONE by changing the null: at each cell the
    BOOK is byte-identical across the two gates, so 4a and 4b see only the H dial.  Both paths
    are scored at all 90 cells anyway because rule 4 requires it, and rule 8's walk-forward is
    run on the H axis this idea actually walks.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists.  Every level here
    is optimistic and every 4a/4b count is an UPPER bound.  EDGE_OPEN, EDGE_ELIG, GATE and
    DTURN are within-pool contrasts over the same tape and the bias very largely cancels out of
    them; it does NOT cancel out of the 4b legs, which are measured against SPY, a real index.
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
SLUG = "is-the-U56-H21-SIGN-FLIP-a-TURNOVER-fact"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

LAG = 1
WARMUP = 260
MAXVOL = 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST = 10.0
GROSS0 = 0.75
FREQ = "W"
LEGS = [(21, 252), (0, 126), (0, 63)]
CAPNAME = "INF"
SEEDS = 40
BISECT = 34
DECISIVE_K = 2.0

PANELS = ["U56", "B136"]                 # dial 2
H_WALK = [5, 10, 21]                     # dial 1 — the new rungs
H_CONTEXT = [63, 126]                    # 1086's committed rungs, carried as gates
H_ALL = H_WALK + H_CONTEXT
NS = [5, 8, 10, 12, 15, 20, 25, 30, 40]  # 1082/1086's committed ladder — NOT a dial
GATESET = ["OPEN", "ELIG"]

A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = {"U56": (0.1521, 0.8713, -0.3372), "B136": (0.1533, 0.8767, -0.3372)}
LIVE_MAXDD_COMMITTED = {"U56": -0.1205, "B136": -0.1224}
SRC_1097 = (ROOT / "research" / "backtests"
            / "2026-09-16_RE-READ-every-committed-EDGE-FIGURE-as-a-LOWER-BOUND_B.grid.csv")

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


# ---------------------------------------------------------------- fast runner (1097 verbatim)
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


def gross_rescaler(rets, wt, mk):
    """f(lam) -> NET returns of the book REBUILT at gross lam*g; g(lam) also returns the
    realised turnover path, which is exactly lam * the lam=1 turnover."""
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

    def f(lam, want_turn=False):
        V = 1.0 + lam * (S - Wsum)
        g = lam * AR / V
        Vp = 1.0 + lam * (Sp - Wsp)
        tr = lam * np.abs(Wr - Ap / Vp[:, None]).sum(axis=1)
        out = g.copy()
        out[reb] -= tr * c
        if want_turn:
            tpath = np.zeros(T)
            tpath[reb] = tr
            return out, tpath
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


def build(rank_key, elig, priced, reb, N, cap, H, T, K, gross):
    """1097's build() verbatim, with ONE addition: new_by_reb, the count of names newly TAKEN
    at each rebalance (the literal re-draw count).  W is computed identically, so every
    cross-run reproduction gate below is unaffected."""
    W = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
    nsel_by_reb, gross_by_reb, new_by_reb = [], [], []
    per_cap = cap * gross / N if np.isfinite(cap) else np.inf
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
        new_by_reb.append(len(take))
        stop = reb[i + 1] if i + 1 < len(reb) else T
        if len(sel):
            w = min(gross / len(sel), per_cap)
            W[t:stop, sel] = w
            gross_by_reb.append(w * len(sel))
        else:
            gross_by_reb.append(0.0)
    return W, np.array(nsel_by_reb), np.array(gross_by_reb), np.array(new_by_reb)


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


def lam_rebuilt(f, sl, target_dd, it):
    if abs(maxdd(f(1.0)[sl])) <= abs(target_dd):
        return None
    a, b = 1e-4, 1.0
    for _ in range(it):
        m = 0.5 * (a + b)
        if abs(maxdd(f(m)[sl])) > abs(target_dd):
            b = m
        else:
            a = m
    return 0.5 * (a + b)


def se_median(x):
    x = np.asarray(x, float)
    return 100.0 * 1.2533 * x.std(ddof=1) / np.sqrt(len(x))


def spear(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 3:
        return np.nan
    return float(pd.Series(x[ok]).rank().corr(pd.Series(y[ok]).rank()))


def ann_turn(tpath, mask):
    return float(tpath[mask].sum() / (mask.sum() / 252.0))


def main():
    t0 = time.time()
    P(f"# Idea 1106 (lane B, {DATE}) — is the U56 H=21 SIGN FLIP a TURNOVER fact?")
    P(f"# 2 tuned dials: H {H_WALK} (walked) x PANEL {PANELS}.  1086's committed H {H_CONTEXT}")
    P("#   are CARRIED AS CONTEXT and used as cross-run reproduction gates, not tuned.")
    P(f"# The N ladder {NS} is 1082/1086's committed coordinate set, NOT a dial; all rungs shown.")
    P(f"# FROZEN: CAND20 legs {LEGS}, cap INF, REBUILT DD-match, {SEEDS} seeds, {BISECT} bisection")
    P(f"#   steps, max_vol {MAXVOL}, gross {GROSS0}, cost {COST:.0f} bps, LAG {LAG}, cadence {FREQ}.")
    P("# The null SEED RECIPE contains NO H, so the SAME 40 orderings are replayed at every rung:")
    P("#   a move in GATE along H is the min hold moving, not a different draw.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   H_TURNOVER     Spearman(GATE_pp, NTURN_raw OPEN) > 0 pooled AND within each panel.")
    P("#   H_DTURN        DTURN = NTURN(OPEN) - NTURN(ELIG) > 0 at every cell AND")
    P("#                  Spearman(GATE_pp, DTURN) > 0.")
    P("#   H_MONOTONE     U56 mean GATE_pp rises monotonically as H falls 126->63->21->10->5.")
    P("#   H_FLIP_EXTENDS U56 carries MORE positive-GATE cells at H=10 and H=5 than the 6/9 at 21.")
    P("#   H_PANEL        B136 (whose nulls re-draw MORE) must flip positive too if GATE is a")
    P("#                  turnover fact.  Negative at every B136 rung while U56 flips REFUTES it.")
    P("#   H_REDRAW       NEW_per_reb(H=5) / NEW_per_reb(H=21) inside [3, 5] ('four times as often').")
    P("# EDGE IS NOT A KEEP PATH; the book is identical across gates.  4a/4b scored at all 90")
    P("#   cells regardless, and rule 8 is walked on the H axis this idea walks.")
    P("")

    rows, benchrows = [], []
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
        sc, elig_real = mech(px)
        rank_key = -np.nan_to_num(sc, nan=-np.inf)
        rank_key[np.isnan(sc)] = np.inf
        reb = np.flatnonzero(mk)
        ALLP = np.ones((T, K), dtype=bool)

        spy = px["SPY"].pct_change().fillna(0.0).values
        sb = blocks(spy, warm, ins, oos)
        live = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"].values
        lb = blocks(live, warm, ins, oos)
        P(f"\n## {panel}: {K} columns, {T} days {idx[0].date()}..{idx[-1].date()}, "
          f"{len(reb)} rebalance dates ({len(reb[reb >= WARMUP])} after warm-up)")
        P(f"   SPY        full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%}  "
          f"halves {sb['H1']:.4f}/{sb['H2']:.4f}  OOS {sb['OOS_CAGR']:.2%} / "
          f"{sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"   RULES v2   full {lb['CAGR']:.2%} / {lb['Sharpe']:.4f} / {lb['MaxDD']:.2%}  "
          f"halves {lb['H1']:.4f}/{lb['H2']:.4f}  OOS {lb['OOS_CAGR']:.2%} / "
          f"{lb['OOS_Sharpe']:.4f} / {lb['OOS_MaxDD']:.2%}")
        benchrows += [dict(panel=panel, series="SPY", **sb), dict(panel=panel, series="RULESv2", **lb)]

        # ---- construction gates, printed before any result number ------------------------
        if panel == "U56":
            W20, _, _, _ = build(rank_key, elig_real, priced, reb, 20, np.inf, 126, T, K, GROSS0)
            wdf = pd.DataFrame(W20, index=idx, columns=px.columns)
            eng = backtest(px, wdf, cost_bps=COST, freq=FREQ)["returns"].values
            gg, tn = nrun(rets, lagmat(W20), mkl)
            fast = gg - tn * COST / 1e4
            d = float(np.abs(fast[WARMUP:] - eng[WARMUP:]).max())
            gates["G1 fast runner == engine.backtest (U56, N=20, H=126)"] = (d, d < 1e-12)
            f20 = gross_rescaler(rets, lagmat(W20), mkl)
            d = float(np.abs(f20(1.0) - fast).max())
            gates["G1b gross_rescaler(1.0) == nrun (bisection kernel is the same book)"] = (d, d < 1e-14)
            _, tp = f20(1.0, want_turn=True)
            d = float(np.abs(tp - tn).max())
            gates["G1c rescaler turnover path == nrun turnover path at lam=1"] = (d, d < 1e-14)
            _, tp2 = f20(0.5, want_turn=True)
            d = float(np.abs(tp2 - 0.5 * tn).max())
            rel = d / float(np.abs(tn).max())
            P(f"   [MEASURED, not a pass/fail] turnover is NOT exactly linear in lam: "
              f"max |turn(0.5) - 0.5*turn(1.0)| = {d:.3e} ({rel:.3%} of peak rebalance turnover). "
              f"NTURN_raw is therefore taken from a DIRECT lam=1 evaluation, never by dividing "
              f"the matched path by lam.")
            gates["G1d NTURN_raw is read at lam=1, so nrun and rescaler agree exactly there"] = (
                float(np.abs(tp - tn).max()), float(np.abs(tp - tn).max()) < 1e-14)
            m = fmet(fast[warm])
            d = max(abs(m[i] - A936_WH126[i]) for i in range(3))
            gates["G2 CROSS-RUN 936/1071/1082 committed W/H126 N=20 triple"] = (d, d < 5e-3)
        sc_ = SPY_OOS_COMMITTED[panel]
        d = max(abs(sb["OOS_CAGR"] - sc_[0]), abs(sb["OOS_Sharpe"] - sc_[1]),
                abs(sb["OOS_MaxDD"] - sc_[2]))
        gates[f"G3 CROSS-RUN SPY OOS triple ({panel})"] = (d, d < 5e-4)
        d = abs(lb["MaxDD"] - LIVE_MAXDD_COMMITTED[panel])
        gates[f"G4 live RULES v2 MaxDD == committed ({panel})"] = (d, d < 5e-4)

        # ---- the H walk ------------------------------------------------------------------
        for Hh in H_ALL:
            for N in NS:
                Wb, nsel, grs, nnew = build(rank_key, elig_real, priced, reb, N, np.inf, Hh,
                                            T, K, GROSS0)
                gb, tb = nrun(rets, lagmat(Wb), mkl)
                rb = gb - tb * COST / 1e4
                b = blocks(rb, warm, ins, oos)
                l4b, l4a, l4bo = legs_4b(b, sb), legs_4a(b, lb), legs_4b_oos(b, sb)
                rebw = reb[reb >= WARMUP]
                keep_mask = np.isin(reb, rebw)

                out = dict(panel=panel, H=Hh, N=N, rung=("WALK" if Hh in H_WALK else "CONTEXT"),
                           mean_nsel=float(nsel[keep_mask].mean()),
                           mean_gross=float(grs[keep_mask].mean()),
                           book_new_per_reb=float(nnew[keep_mask].mean()),
                           turnover=ann_turn(tb, warm), **b, **l4b, **l4a, **l4bo,
                           pass4b=all(l4b.values()), pass4a=all(l4a.values()),
                           pass4b_oos=all(l4bo.values()))
                out["pass4b_full_and_oos"] = out["pass4b"] and out["pass4b_oos"]

                for gate in GATESET:
                    cs, isv, oosv, nt, ntm, nw, lams, drier = [], [], [], [], [], [], [], 0
                    for s in range(SEEDS):
                        sd = (mdseed(panel, N, CAPNAME, s) if gate == "OPEN"
                              else mdseed(panel, N, CAPNAME, "ELIG", s))
                        rk = np.random.default_rng(sd).random((T, K))
                        eg = elig_real if gate == "ELIG" else ALLP
                        Wn, _, _, nnw = build(rk, eg, priced, reb, N, np.inf, Hh, T, K, GROSS0)
                        fn = gross_rescaler(rets, lagmat(Wn), mkl)
                        lam = lam_rebuilt(fn, warm, b["MaxDD"], BISECT)
                        if lam is None:
                            drier += 1
                            lam = 1.0
                        rr, tp = fn(lam, want_turn=True)
                        _, tp1 = fn(1.0, want_turn=True)      # NTURN_raw at lam = 1, not tp/lam
                        cs.append(fmet(rr[warm])[0])
                        isv.append(fmet(rr[ins])[0])
                        oosv.append(fmet(rr[oos])[0])
                        ntm.append(ann_turn(tp, warm))
                        nt.append(ann_turn(tp1, warm))
                        nw.append(float(nnw[keep_mask].mean()))
                        lams.append(lam)
                    cs, isv, oosv = np.array(cs), np.array(isv), np.array(oosv)
                    out[f"EDGE_{gate}_pp"] = 100.0 * (b["CAGR"] - float(np.median(cs)))
                    out[f"EDGE_IS_{gate}_pp"] = 100.0 * (b["IS_CAGR"] - float(np.median(isv)))
                    out[f"EDGE_OOS_{gate}_pp"] = 100.0 * (b["OOS_CAGR"] - float(np.median(oosv)))
                    out[f"EDGE_se_{gate}_pp"] = se_median(cs)
                    out[f"null_med_{gate}"] = float(np.median(cs))
                    out[f"NTURN_raw_{gate}"] = float(np.median(nt))
                    out[f"NTURN_matched_{gate}"] = float(np.median(ntm))
                    out[f"NEW_per_reb_{gate}"] = float(np.median(nw))
                    out[f"lam_med_{gate}"] = float(np.median(lams))
                    out[f"drier_{gate}"] = drier
                out["GATE_pp"] = out["EDGE_OPEN_pp"] - out["EDGE_ELIG_pp"]
                out["GATE_IS_pp"] = out["EDGE_IS_OPEN_pp"] - out["EDGE_IS_ELIG_pp"]
                out["GATE_OOS_pp"] = out["EDGE_OOS_OPEN_pp"] - out["EDGE_OOS_ELIG_pp"]
                out["DTURN"] = out["NTURN_raw_OPEN"] - out["NTURN_raw_ELIG"]
                out["DTURN_matched"] = out["NTURN_matched_OPEN"] - out["NTURN_matched_ELIG"]
                out["DNEW"] = out["NEW_per_reb_OPEN"] - out["NEW_per_reb_ELIG"]
                out["GATE_se_pp"] = float(np.hypot(out["EDGE_se_OPEN_pp"], out["EDGE_se_ELIG_pp"]))
                out["GATE_decisive"] = bool(abs(out["GATE_pp"]) > DECISIVE_K * out["GATE_se_pp"])
                out["dec_OPEN"] = bool(abs(out["EDGE_OPEN_pp"]) > DECISIVE_K * out["EDGE_se_OPEN_pp"])
                out["dec_ELIG"] = bool(abs(out["EDGE_ELIG_pp"]) > DECISIVE_K * out["EDGE_se_ELIG_pp"])
                rows.append(out)
                P(f"   {panel:<4s} H={Hh:<3d} N={N:<2d} [{out['rung']:<7s}] "
                  f"OPEN {out['EDGE_OPEN_pp']:+7.3f} ELIG {out['EDGE_ELIG_pp']:+7.3f} "
                  f"GATE {out['GATE_pp']:+7.3f} (+-{DECISIVE_K*out['GATE_se_pp']:.3f})  "
                  f"nturn O {out['NTURN_raw_OPEN']:5.2f} E {out['NTURN_raw_ELIG']:5.2f} "
                  f"D {out['DTURN']:+5.2f}  new/reb O {out['NEW_per_reb_OPEN']:5.2f}  "
                  f"t={time.time()-t0:5.0f}s")

    G = pd.DataFrame(rows)

    # ---- cross-run reproduction gates ---------------------------------------------------
    c97 = pd.read_csv(SRC_1097)
    c97 = c97[c97.family == "A"][["panel", "N", "H", "EDGE_OPEN_pp", "EDGE_ELIG_pp", "GATE_pp",
                                  "CAGR", "MaxDD", "turnover"]]
    m = G.merge(c97, on=["panel", "N", "H"], suffixes=("", "_97"))
    d = max(float((m.EDGE_OPEN_pp - m.EDGE_OPEN_pp_97).abs().max()),
            float((m.EDGE_ELIG_pp - m.EDGE_ELIG_pp_97).abs().max()))
    gates[f"G5 CROSS-RUN reproduce 1097's {len(m)} committed EDGE_OPEN/ELIG figures (H 21/63/126)"] = (d, d < 1e-9)
    d = max(float((m.CAGR - m.CAGR_97).abs().max()), float((m.MaxDD - m.MaxDD_97).abs().max()),
            float((m.turnover - m.turnover_97).abs().max()))
    gates[f"G6 CROSS-RUN reproduce 1097's {len(m)} book CAGR / MaxDD / turnover triples"] = (d, d < 1e-9)
    u21 = G[(G.panel == "U56") & (G.H == 21)]
    npos = int((u21.GATE_pp > 0).sum())
    gates["G7 CROSS-RUN 1097's headline: U56 H=21 carries 6 of 9 POSITIVE GATE rungs"] = (
        abs(npos - 6), npos == 6)
    d = float(G.mean_gross.sub(GROSS0).abs().max())
    gates[f"G8 every book sits at gross {GROSS0} (cap INF, no de-grossing)"] = (d, d < 1e-12)

    P("\n## GATES")
    gaterows = []
    for k, (v, ok) in gates.items():
        P(f"   [{'PASS' if ok else 'FAIL'}] {k}: {v:.2e}")
        gaterows.append(dict(gate=k, value=v, passed=ok))
    P(f"   {sum(1 for _, o in gates.values() if o)} of {len(gates)} PASS")

    # ---------------------------------------------------------------- the answer ----------
    P(f"\n## THE H WALK — {len(G)} cells (2 panels x {len(H_ALL)} H x {len(NS)} N), both gates")
    P("   H    panel  pos/9  mean GATE   mean NTURN(OPEN)  mean NTURN(ELIG)  mean DTURN  "
      "mean NEW/reb(OPEN)")
    rung = []
    for panel in PANELS:
        for Hh in H_ALL:
            s = G[(G.panel == panel) & (G.H == Hh)]
            r = dict(panel=panel, H=Hh, rung=("WALK" if Hh in H_WALK else "CONTEXT"), k=len(s),
                     n_pos=int((s.GATE_pp > 0).sum()),
                     n_pos_decisive=int(((s.GATE_pp > 0) & s.GATE_decisive).sum()),
                     n_neg_decisive=int(((s.GATE_pp < 0) & s.GATE_decisive).sum()),
                     mean_GATE=float(s.GATE_pp.mean()), median_GATE=float(s.GATE_pp.median()),
                     min_GATE=float(s.GATE_pp.min()), max_GATE=float(s.GATE_pp.max()),
                     mean_NTURN_OPEN=float(s.NTURN_raw_OPEN.mean()),
                     mean_NTURN_ELIG=float(s.NTURN_raw_ELIG.mean()),
                     mean_DTURN=float(s.DTURN.mean()),
                     mean_NEW_OPEN=float(s.NEW_per_reb_OPEN.mean()),
                     mean_NEW_ELIG=float(s.NEW_per_reb_ELIG.mean()),
                     mean_book_turn=float(s.turnover.mean()),
                     mean_EDGE_OPEN=float(s.EDGE_OPEN_pp.mean()),
                     mean_EDGE_ELIG=float(s.EDGE_ELIG_pp.mean()),
                     spearman_GATE_NTURN=spear(s.GATE_pp, s.NTURN_raw_OPEN),
                     spearman_GATE_DTURN=spear(s.GATE_pp, s.DTURN))
            rung.append(r)
            P(f"   {Hh:<4d} {panel:<6s} {r['n_pos']}/9    {r['mean_GATE']:+8.3f}   "
              f"{r['mean_NTURN_OPEN']:12.3f}    {r['mean_NTURN_ELIG']:12.3f}    "
              f"{r['mean_DTURN']:+9.3f}   {r['mean_NEW_OPEN']:12.3f}")
    R = pd.DataFrame(rung)

    # ---- H_TURNOVER ---------------------------------------------------------------------
    P("\n## H_TURNOVER — does GATE track realised null turnover?")
    rho_pool = spear(G.GATE_pp, G.NTURN_raw_OPEN)
    P(f"   POOLED ({len(G)} cells)  Spearman(GATE_pp, NTURN_raw OPEN) = {rho_pool:+.4f}")
    rho_panel = {}
    for panel in PANELS:
        s = G[G.panel == panel]
        rho_panel[panel] = spear(s.GATE_pp, s.NTURN_raw_OPEN)
        P(f"   {panel:<5s} ({len(s)} cells)  rho = {rho_panel[panel]:+.4f}")
    P("   within-rung (H, panel) rho, 9 N-points each — the turnover variation there is the")
    P("   N axis, not the H axis, so these are the premise's own within-slice test:")
    for _, r in R.iterrows():
        P(f"     {r['panel']:<5s} H={int(r['H']):<3d}  rho(GATE, NTURN) {r['spearman_GATE_NTURN']:+.4f}  "
          f"rho(GATE, DTURN) {r['spearman_GATE_DTURN']:+.4f}")
    H_TURNOVER = bool(rho_pool > 0 and all(v > 0 for v in rho_panel.values()))
    P(f"   H_TURNOVER -> {'SUPPORTED' if H_TURNOVER else 'REFUTED'}")

    # ---- H_DTURN ------------------------------------------------------------------------
    P("\n## H_DTURN — is the gate-free null the one that turns over more?")
    npos_d = int((G.DTURN > 0).sum())
    rho_d = spear(G.GATE_pp, G.DTURN)
    P(f"   DTURN > 0 at {npos_d} of {len(G)} cells.  mean {G.DTURN.mean():+.4f}, "
      f"range [{G.DTURN.min():+.4f}, {G.DTURN.max():+.4f}] turns/yr")
    P(f"   Spearman(GATE_pp, DTURN) pooled = {rho_d:+.4f}")
    for panel in PANELS:
        s = G[G.panel == panel]
        P(f"     {panel:<5s} DTURN > 0 at {int((s.DTURN > 0).sum())}/{len(s)}, "
          f"mean {s.DTURN.mean():+.4f}, rho(GATE, DTURN) {spear(s.GATE_pp, s.DTURN):+.4f}")
    H_DTURN = bool(npos_d == len(G) and rho_d > 0)
    P(f"   H_DTURN -> {'SUPPORTED' if H_DTURN else 'REFUTED'}")

    # ---- H_MONOTONE / H_FLIP_EXTENDS ----------------------------------------------------
    P("\n## H_MONOTONE / H_FLIP_EXTENDS — U56 down the H ladder (126 -> 5)")
    u = R[R.panel == "U56"].set_index("H").loc[[126, 63, 21, 10, 5]]
    seq = u.mean_GATE.tolist()
    P("   H:      " + "  ".join(f"{h:>8d}" for h in [126, 63, 21, 10, 5]))
    P("   meanGATE" + "  ".join(f"{v:>+8.3f}" for v in seq))
    P("   pos/9:  " + "  ".join(f"{int(v):>8d}" for v in u.n_pos.tolist()))
    P("   NTURN:  " + "  ".join(f"{v:>8.3f}" for v in u.mean_NTURN_OPEN.tolist()))
    H_MONO = all(seq[i + 1] > seq[i] for i in range(len(seq) - 1))
    P(f"   H_MONOTONE -> {'SUPPORTED' if H_MONO else 'REFUTED'} "
      f"({sum(1 for i in range(len(seq)-1) if seq[i+1] <= seq[i])} inversions)")
    p21, p10, p5 = int(u.loc[21, "n_pos"]), int(u.loc[10, "n_pos"]), int(u.loc[5, "n_pos"])
    H_FLIP = bool(p10 > p21 and p5 > p21)
    P(f"   H_FLIP_EXTENDS: U56 positive-GATE rungs H=21 {p21}/9 -> H=10 {p10}/9 -> H=5 {p5}/9 "
      f"-> {'SUPPORTED' if H_FLIP else 'REFUTED'}")

    # ---- H_PANEL ------------------------------------------------------------------------
    P("\n## H_PANEL — B136 re-draws MORE than U56 at every rung; does it flip too?")
    for Hh in H_ALL:
        a = R[(R.panel == "U56") & (R.H == Hh)].iloc[0]
        c = R[(R.panel == "B136") & (R.H == Hh)].iloc[0]
        P(f"   H={Hh:<4d} U56  NTURN {a['mean_NTURN_OPEN']:6.3f}  pos {int(a['n_pos'])}/9  "
          f"meanGATE {a['mean_GATE']:+7.3f}   |   B136 NTURN {c['mean_NTURN_OPEN']:6.3f}  "
          f"pos {int(c['n_pos'])}/9  meanGATE {c['mean_GATE']:+7.3f}")
    b136_pos = int(R[(R.panel == "B136") & (R.H.isin(H_WALK))].n_pos.sum())
    u56_pos = int(R[(R.panel == "U56") & (R.H.isin(H_WALK))].n_pos.sum())
    b_more_turn = bool((R[R.panel == "B136"].set_index("H").mean_NTURN_OPEN
                        > R[R.panel == "U56"].set_index("H").mean_NTURN_OPEN).all())
    H_PANEL = bool(b136_pos > 0)
    P(f"   B136's null turnover exceeds U56's at EVERY rung: {b_more_turn}")
    P(f"   positive-GATE cells over the WALK rungs: U56 {u56_pos}/27, B136 {b136_pos}/27")
    P(f"   H_PANEL -> {'SUPPORTED' if H_PANEL else 'REFUTED'} "
      "(REFUTED = the flip is a PANEL fact, not a turnover fact)")
    P("   POST-HOC, LABELLED AS POST-HOC AND NOT COUNTED IN THE HYPOTHESIS TALLY (D1): the")
    P("   declared wording of H_PANEL asks only whether B136 flips ANYWHERE, which is a weaker")
    P("   question than the premise needs.  The DIRECTIONAL cross-panel contrast is the one that")
    P("   bites, and it runs the wrong way: B136's nulls re-draw MORE than U56's at every one of")
    P("   the 5 rungs, yet B136's mean GATE is MORE NEGATIVE than U56's at every one of them.")
    P("   Two panels, matched on everything but composition, order themselves by panel and not by")
    P("   turnover.  Stated as an observation, not as a pre-declared test.")

    # ---- H_REDRAW -----------------------------------------------------------------------
    P("\n## H_REDRAW — is 'four times as often' literally true?")
    rr_rows = []
    for panel in PANELS:
        for gate in GATESET:
            a5 = R[(R.panel == panel) & (R.H == 5)].iloc[0][f"mean_NEW_{gate}"]
            a21 = R[(R.panel == panel) & (R.H == 21)].iloc[0][f"mean_NEW_{gate}"]
            a126 = R[(R.panel == panel) & (R.H == 126)].iloc[0][f"mean_NEW_{gate}"]
            rr_rows.append(dict(panel=panel, gate=gate, new_H5=a5, new_H21=a21, new_H126=a126,
                                ratio_5_over_21=a5 / a21 if a21 else np.nan,
                                ratio_5_over_126=a5 / a126 if a126 else np.nan))
            P(f"   {panel:<5s} {gate:<4s} NEW/reb  H=5 {a5:6.3f}  H=21 {a21:6.3f}  "
              f"H=126 {a126:6.3f}   ratio 5/21 = {a5/a21:5.3f}x, 5/126 = {a5/a126:5.3f}x")
    RR = pd.DataFrame(rr_rows)
    H_REDRAW = bool(((RR.ratio_5_over_21 >= 3.0) & (RR.ratio_5_over_21 <= 5.0)).all())
    P(f"   H_REDRAW (ratio 5/21 inside [3,5] at all four panel x gate arms) -> "
      f"{'SUPPORTED' if H_REDRAW else 'REFUTED'}")

    # ---- what DOES explain GATE? --------------------------------------------------------
    P("\n## WHAT MOVES GATE, if not turnover — the same cells re-read against the alternatives")
    alts = []
    for lab, col in [("NTURN_raw_OPEN (the premise)", "NTURN_raw_OPEN"),
                     ("DTURN = NTURN(OPEN) - NTURN(ELIG)", "DTURN"),
                     ("NEW_per_reb_OPEN (literal re-draws)", "NEW_per_reb_OPEN"),
                     ("book turnover", "turnover"),
                     ("N (slot count)", "N"),
                     ("H (min hold)", "H"),
                     ("EDGE_OPEN_pp (the level itself)", "EDGE_OPEN_pp"),
                     ("mean_nsel (names actually held)", "mean_nsel")]:
        alts.append(dict(explanator=lab, rho_pooled=spear(G.GATE_pp, G[col]),
                         rho_U56=spear(G[G.panel == "U56"].GATE_pp, G[G.panel == "U56"][col]),
                         rho_B136=spear(G[G.panel == "B136"].GATE_pp, G[G.panel == "B136"][col])))
        a = alts[-1]
        P(f"   rho(GATE, {lab:<36s}) pooled {a['rho_pooled']:+.4f}  "
          f"U56 {a['rho_U56']:+.4f}  B136 {a['rho_B136']:+.4f}")
    A = pd.DataFrame(alts)
    wr = R.spearman_GATE_NTURN
    P("   POST-HOC, LABELLED (D2) — 'turnover' is TWO axes and they pull opposite ways.  The")
    P("   pooled and U56 rho above are ACROSS-rung (the H axis).  WITHIN a rung, where the only")
    P("   turnover variation is the N axis, rho(GATE, NTURN) is NEGATIVE at "
      f"{int((wr < 0).sum())} of {len(wr)} (panel, H) slices "
      f"(range {wr.min():+.4f} to {wr.max():+.4f}).")
    P("   So more null turnover raises GATE when it comes from a shorter hold and LOWERS it when")
    P("   it comes from a smaller book.  A single 'GATE scales with re-draw frequency' claim")
    P("   cannot hold both signs; 'turnover' is not the variable.")

    # ---- rule 8 walk-forward ------------------------------------------------------------
    P("\n## RULE 8 WALK-FORWARD — parameters chosen on 2009-2016 ONLY, 2017-2026 untouched")
    P("   Two IS choosers, both declared before the numbers: C_SHARPE picks the (H, N) with the")
    P("   highest IS Sharpe; C_EDGE picks the highest IS EDGE_OPEN, the record's own convention.")
    wf = []
    for panel in PANELS:
        s = G[G.panel == panel]
        spyb = [r for r in benchrows if r["panel"] == panel and r["series"] == "SPY"][0]
        livb = [r for r in benchrows if r["panel"] == panel and r["series"] == "RULESv2"][0]
        for cname, col in [("C_SHARPE", "IS_Sharpe"), ("C_EDGE", "EDGE_IS_OPEN_pp")]:
            pick = s.loc[s[col].idxmax()]
            wf.append(dict(panel=panel, chooser=cname, pick_H=int(pick["H"]), pick_N=int(pick["N"]),
                           IS_Sharpe=pick["IS_Sharpe"], IS_CAGR=pick["IS_CAGR"],
                           OOS_CAGR=pick["OOS_CAGR"], OOS_Sharpe=pick["OOS_Sharpe"],
                           OOS_MaxDD=pick["OOS_MaxDD"],
                           base_OOS_CAGR=livb["OOS_CAGR"], base_OOS_Sharpe=livb["OOS_Sharpe"],
                           base_OOS_MaxDD=livb["OOS_MaxDD"],
                           spy_OOS_CAGR=spyb["OOS_CAGR"], spy_OOS_Sharpe=spyb["OOS_Sharpe"],
                           spy_OOS_MaxDD=spyb["OOS_MaxDD"],
                           O_S=bool(pick["O_S"]), O_DD=bool(pick["O_DD"]),
                           O_CAGR=bool(pick["O_CAGR"]),
                           OOS_4b=bool(pick["O_S"] and pick["O_DD"] and pick["O_CAGR"]),
                           GATE_pp=pick["GATE_pp"], GATE_OOS_pp=pick["GATE_OOS_pp"],
                           EDGE_OOS_OPEN_pp=pick["EDGE_OOS_OPEN_pp"],
                           EDGE_OOS_ELIG_pp=pick["EDGE_OOS_ELIG_pp"],
                           oos_argmax_H=int(s.loc[s.OOS_Sharpe.idxmax(), "H"]),
                           oos_argmax_N=int(s.loc[s.OOS_Sharpe.idxmax(), "N"]),
                           oos_argmax_Sharpe=float(s.OOS_Sharpe.max())))
            w = wf[-1]
            P(f"   {panel:<5s} {cname:<8s} IS pick H={w['pick_H']:<3d} N={w['pick_N']:<2d} "
              f"(IS Sharpe {w['IS_Sharpe']:.4f})")
            P(f"          OOS  book  CAGR {w['OOS_CAGR']:7.2%}  Sharpe {w['OOS_Sharpe']:.4f}  "
              f"MaxDD {w['OOS_MaxDD']:7.2%}")
            P(f"          OOS  base  CAGR {w['base_OOS_CAGR']:7.2%}  Sharpe {w['base_OOS_Sharpe']:.4f}  "
              f"MaxDD {w['base_OOS_MaxDD']:7.2%}   (RULES v2, live)")
            P(f"          OOS  SPY   CAGR {w['spy_OOS_CAGR']:7.2%}  Sharpe {w['spy_OOS_Sharpe']:.4f}  "
              f"MaxDD {w['spy_OOS_MaxDD']:7.2%}")
            P(f"          OOS 4b legs  O_S {w['O_S']}  O_DD {w['O_DD']}  O_CAGR {w['O_CAGR']}  "
              f"-> {'PASS' if w['OOS_4b'] else 'FAIL'}")
            P(f"          OOS GATE at the picked cell {w['GATE_OOS_pp']:+.3f} pp "
              f"(full-sample {w['GATE_pp']:+.3f} pp); true OOS Sharpe argmax is "
              f"H={w['oos_argmax_H']} N={w['oos_argmax_N']} at {w['oos_argmax_Sharpe']:.4f}")
    WF = pd.DataFrame(wf)
    P("   GATE is a statement about the COMPARAND, not the book, so the walk-forward above is")
    P("   the H dial's own OOS test; the two gates cannot move it.  Reported for completeness:")
    for panel in PANELS:
        s = G[G.panel == panel]
        P(f"     {panel:<5s} OOS GATE <= 0 at {int((s.GATE_OOS_pp <= 0).sum())}/{len(s)} cells "
          f"(full-sample {int((s.GATE_pp <= 0).sum())}/{len(s)}); "
          f"sign agrees full vs OOS at "
          f"{int((np.sign(s.GATE_pp) == np.sign(s.GATE_OOS_pp)).sum())}/{len(s)}")

    # ---- both KEEP paths ----------------------------------------------------------------
    P("\n## BOTH KEEP PATHS at all 90 cells (PROTOCOL rule 4)")
    P(f"   4a (beat the book: Sharpe > RULES v2 in BOTH halves, MaxDD no worse): "
      f"{int(G.pass4a.sum())} of {len(G)}")
    for leg in ["A_H1", "A_H2", "A_DD"]:
        P(f"      {leg}: {int(G[leg].sum())}/{len(G)}")
    P(f"   4b (capital-worthy, full sample): {int(G.pass4b.sum())} of {len(G)}")
    for leg in ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]:
        P(f"      {leg}: {int(G[leg].sum())}/{len(G)}")
    P(f"   4b on the OOS window alone: {int(G.pass4b_oos.sum())} of {len(G)}")
    for leg in ["O_S", "O_DD", "O_CAGR"]:
        P(f"      {leg}: {int(G[leg].sum())}/{len(G)}")
    P(f"   4b FULL and OOS together: {int(G.pass4b_full_and_oos.sum())} of {len(G)}")
    for Hh in H_ALL:
        s = G[G.H == Hh]
        P(f"      H={Hh:<4d} 4a {int(s.pass4a.sum())}/{len(s)}  4b {int(s.pass4b.sum())}/{len(s)}  "
          f"4b-OOS {int(s.pass4b_oos.sum())}/{len(s)}  best full Sharpe {s.Sharpe.max():.4f}, "
          f"best MaxDD {s.MaxDD.max():.2%}")
    # ---- which leg binds, and by how much -----------------------------------------------
    LEGS4B = ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]
    fails = G[~G.pass4b]
    P(f"   BINDING LEG among the {len(fails)} full-sample 4b FAILURES:")
    for leg in LEGS4B:
        n_only = int((~fails[leg] & fails[[x for x in LEGS4B if x != leg]].all(axis=1)).sum())
        P(f"      {leg}: fails at {int((~fails[leg]).sum())}/{len(fails)}, "
          f"SOLE failing leg at {n_only}")
    # margins at the cells that DO pass, so the passes are read with their own headroom
    sp = {p: [r for r in benchrows if r["panel"] == p and r["series"] == "SPY"][0] for p in PANELS}
    G["dd_margin_pp"] = [100.0 * (DD_CAP * abs(sp[p]["MaxDD"]) - abs(d))
                         for p, d in zip(G.panel, G.MaxDD)]
    G["cagr_margin_pp"] = [100.0 * (c - CAGR_FLOOR * sp[p]["CAGR"])
                           for p, c in zip(G.panel, G.CAGR)]
    ps = G[G.pass4b_full_and_oos]
    P(f"   The {len(ps)} cells passing 4b FULL and OOS, read with their own headroom "
      f"(cap = {DD_CAP:.0%} of SPY MaxDD, floor = {CAGR_FLOOR:.0%} of SPY CAGR):")
    P(f"      drawdown headroom  min {ps.dd_margin_pp.min():+.2f} pp, median "
      f"{ps.dd_margin_pp.median():+.2f}, max {ps.dd_margin_pp.max():+.2f}")
    P(f"      CAGR headroom      min {ps.cagr_margin_pp.min():+.2f} pp, median "
      f"{ps.cagr_margin_pp.median():+.2f}, max {ps.cagr_margin_pp.max():+.2f}")
    for Hh in H_ALL:
        s = ps[ps.H == Hh]
        if len(s):
            P(f"      H={Hh:<4d} {len(s):2d} passes, DD headroom median {s.dd_margin_pp.median():+.2f} pp, "
              f"CAGR headroom median {s.cagr_margin_pp.median():+.2f} pp")
    P("   Idea 1083 measured the 90% width of the drawdown-margin quantity itself at 4.1-7.2 pp")
    P("   on this tape, which is wider than every headroom above: these passes are not resolved")
    P("   by this tape, and NOTHING here is proposed as capital.")
    P("   NEW vs ALREADY COMMITTED: H=21/63/126 are 1082/1086/1097's own cells, re-run here and")
    P("   reproduced at G5/G6.  The only NEW books this run adds are the H=5 and H=10 rungs.")
    newp = ps[ps.H.isin([5, 10])]
    P(f"      new-rung 4b passes (full AND OOS): {len(newp)} of {int((G.H.isin([5,10])).sum())} "
      f"new cells; {int((newp.panel == 'U56').sum())} on U56, "
      f"{int((newp.panel == 'B136').sum())} on B136")

    # ---- hypotheses table ---------------------------------------------------------------
    hyp = [dict(hypothesis="H_TURNOVER", declared="rho(GATE, NTURN_raw OPEN) > 0 pooled and in both panels",
                result=f"pooled {rho_pool:+.4f}, U56 {rho_panel['U56']:+.4f}, B136 {rho_panel['B136']:+.4f}",
                verdict="SUPPORTED" if H_TURNOVER else "REFUTED"),
           dict(hypothesis="H_DTURN", declared="DTURN > 0 at every cell AND rho(GATE, DTURN) > 0",
                result=f"DTURN>0 at {npos_d}/{len(G)}, rho {rho_d:+.4f}",
                verdict="SUPPORTED" if H_DTURN else "REFUTED"),
           dict(hypothesis="H_MONOTONE", declared="U56 mean GATE rises monotonically 126->5",
                result=" -> ".join(f"{v:+.3f}" for v in seq),
                verdict="SUPPORTED" if H_MONO else "REFUTED"),
           dict(hypothesis="H_FLIP_EXTENDS", declared="U56 positive-GATE count higher at H=10 and H=5 than 6/9 at H=21",
                result=f"H=21 {p21}/9, H=10 {p10}/9, H=5 {p5}/9",
                verdict="SUPPORTED" if H_FLIP else "REFUTED"),
           dict(hypothesis="H_PANEL", declared="B136 (more null turnover) flips positive somewhere on the walk",
                result=f"B136 positive-GATE cells over walk rungs {b136_pos}/27 (U56 {u56_pos}/27)",
                verdict="SUPPORTED" if H_PANEL else "REFUTED"),
           dict(hypothesis="H_REDRAW", declared="NEW_per_reb(H=5)/NEW_per_reb(H=21) inside [3,5]",
                result=f"ratios {', '.join(f'{v:.2f}' for v in RR.ratio_5_over_21)}",
                verdict="SUPPORTED" if H_REDRAW else "REFUTED")]
    HY = pd.DataFrame(hyp)
    P("\n## HYPOTHESES")
    for _, r in HY.iterrows():
        P(f"   [{r['verdict']:<9s}] {r['hypothesis']:<15s} {r['result']}")

    dump(G, "grid")
    dump(R, "rungs")
    dump(A, "explanators")
    dump(WF, "walkforward")
    dump(HY, "hypotheses")
    dump(pd.DataFrame(gaterows), "gates")
    dump(pd.DataFrame(benchrows), "benchmarks")
    dump(RR, "redraw")

    P("\n## SURVIVORSHIP (PROTOCOL rule 9)")
    P("   U56 and B136 are CURRENT-CONSTITUENT lists.  Every level is optimistic and every")
    P("   4a/4b count is an UPPER bound.  GATE, DTURN and the EDGE contrasts are within-pool")
    P("   over one tape and the bias very largely cancels out of them; it does NOT cancel out")
    P("   of the 4b legs, which are measured against SPY, a real index.")
    P(f"\n# done in {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

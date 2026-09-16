#!/usr/bin/env python3
"""Idea 1059 (cloud lane, 2026-09-16) — is the 4b PASS RATE's WEEKLY PEAK a COST-RUNG object?

QUESTION (QUEUE idea 1059, verbatim)
    idea 968 found the 4b pass rate is single-peaked at WEEKLY (U56 0.333 -> 0.833 -> 0.205 ->
    0.044 across D/W/M/Q), because L_CAGR is a turnover rebate that eases with holding length
    while L_DD tightens.  Walk the cost rung (0, 10, 25, 50 bps) and report where the peak
    moves; if it slides to D at 0 bps and to Q at 50 bps, PROTOCOL's 10 bps is choosing the
    winning cadence.  Max 2 params (cost rung, cadence ladder).

THE OBJECT.  968's headline profile is a PASS RATE: over one (panel, gross) cell, the fraction
    of a fixed book population that clears all five 4b legs.  The population is 6 mechanism arms
    x the cadence's own phase family (P members) + the canonical calendar period-end, so
    n = 6 x (P+1) = 12 / 36 / 132 / 384 at D / W / M / Q.  This run rebuilds that EXACT
    population and re-prices it at four cost rungs.  Nothing else changes: same panels, same
    mechanisms, same phases, same gross, same warm-up, same 4b definition, same null.

THE ARITHMETIC, DECLARED BEFORE ANY NUMBER (a prediction, not a post-hoc story).
    Cost enters the book's returns only through realised turnover: r_net = r_gross - turn*c/1e4.
    Turnover falls steeply with holding length (968 measured 22.4 / 9.0 / 4.1 / 2.2 turns per
    year at D / W / M / Q on U56), so the ANNUAL DRAG of a rung c is roughly c x turn_yr:
        rung      D        W        M        Q
        0 bps     0        0        0        0
        10 bps   224 bp    90 bp    41 bp    22 bp
        25 bps   561 bp   226 bp   102 bp    56 bp
        50 bps  1121 bp   452 bp   205 bp   111 bp
    Every 4b leg is read against SPY, which pays NO turnover cost at any rung.  So raising the
    rung shifts all five legs against the fast cadences and leaves the slow ones nearly intact.
    The queue's prediction (peak at D when cost is free, at Q when cost is punitive) is the
    NAIVE reading of that arithmetic.  It can fail in two distinct ways, and both are reportable:
      (a) at 0 bps the fast cadences may STILL fail, because L_DD is a drawdown fact and not a
          cost fact — 968 already found the null's L_DD saturated at 0 bps;
      (b) at 50 bps the slow cadences may fail TOO, because Q's own drag (111 bp/yr) is still
          large against a 70%-of-SPY CAGR floor, so the peak can collapse to NOTHING rather
          than slide to Q.
    A peak that MOVES makes 10 bps a cadence chooser.  A peak that STAYS at W makes the weekly
    result a book fact.  A peak that DIES makes it neither.

THE TWO DIALS (rule 4, no more than two tuned parameters)
    1. COST RUNG    {0, 10, 25, 50} bps   (the queue's own ladder)
    2. CADENCE      {D, W, M, Q}          (968's own ladder)
    Everything else is the census population, fixed at 968's committed values.  GROSS is NOT a
    third dial: the headline is 968's own 0.75 throughout, and 0.50 / 1.00 are printed as
    robustness only, never selected on.  ALL 4 x 4 grid points are reported.

RULE 8.  A walk-forward that chooses the cadence on 2009-2016 alone (IS Sharpe, and a second
    IS-only chooser on the IS 4b leg count) and evaluates 2017-2026 untouched, at every rung,
    against SPY and against the live RULES v2 book priced at the SAME rung.  Both KEEP paths.

SURVIVORSHIP.  U56 and B136 are current-constituent panels.  The bias is common to books and to
    the null and flatters BOTH the CAGR floor and the DD cap against SPY, which is a real index.
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
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-16"
SLUG = "is-the-4b-PASS-RATE-s-WEEKLY-PEAK-a-COST-RUNG-object"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

LAG = 1
WARMUP = 260
NTOP = 20
MAXVOL = 0.60
BAND = 0.03
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70

# ---- the two tuned dials ----------------------------------------------------------------------
COSTS = [0.0, 10.0, 25.0, 50.0]
CADENCES = ["D", "W", "M", "Q"]
COST_HEAD = 10.0                                 # PROTOCOL rule 2
PLEN = {"D": 1, "W": 5, "M": 21, "Q": 63}        # trading days per period (961/968's grid)

GROSSES = [0.50, 0.75, 1.00]
GROSS_HEAD = 0.75                                # 961/968's own headline, NOT a dial
PANELS = ["U56", "B136"]
MECHS = ["CAND20", "R3_55", "R3_84", "NOR3", "MOMONLY", "BAND03"]
LEGSETS = {"CAND20": [(21, 252), (0, 126), (0, 63)],
           "R3_55": [(21, 252), (0, 126), (0, 55)],
           "R3_84": [(21, 252), (0, 126), (0, 84)],
           "NOR3": [(21, 252), (0, 126)],
           "MOMONLY": [(21, 252)]}
LEGS = ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]

NSEED = 20
CAND20_PUB = (0.1266, 1.0921, -0.1831)
G3_TOL = (5e-3, 3.3e-2, 5e-3)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
# 968's committed 10 bps / gross 0.75 pass-rate profile — the object this run walks.
PUB_968_PASS = {"U56": [0.333, 0.833, 0.205, 0.044], "B136": [0.000, 0.028, 0.000, 0.000]}
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


# ====================================================================== runner (gated at G1)
def nrun(rets, wt, mk):
    """GROSS returns and turnover.  Cost is applied OUTSIDE (r - turn*c/1e4) so one run prices
    every rung; G1 gates that against engine.backtest, which charges cost inside."""
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


# ====================================================================== the books
def legs_composite(px, legs):
    parts = []
    for skip, look in legs:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return sum(parts) / len(parts)


def mech_w1(px, mech):
    """Gross-1.0 target weights for one mechanism arm — 961/968's construction, verbatim."""
    if mech == "BAND03":
        e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
        ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        return ew.where(band_state(px, BAND), 0.0).values
    comp = legs_composite(px, LEGSETS[mech])
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))       # no vol scaler (KEEP 4b convention)
    elig = sc.where(above & (vol20 < MAXVOL))
    rank = elig.rank(axis=1, ascending=False)
    sel = (rank <= NTOP).astype(float)
    k = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(k, axis=0).fillna(0.0).values


def null_w1(px, seed):
    """Gross-1.0 weights for a COIN FLIP: NTOP names drawn uniformly from those priced that day,
    equal weighted.  Selection is destroyed; the cadence, the gross and the tape are inherited."""
    ok = px.notna().values
    T, N = ok.shape
    rng = np.random.default_rng(mdseed("NULL", seed, T, N))
    W = np.zeros((T, N))
    for i in range(T):
        idx = np.flatnonzero(ok[i])
        if len(idx) == 0:
            continue
        k = min(NTOP, len(idx))
        pick = rng.choice(idx, size=k, replace=False)
        W[i, pick] = 1.0 / k
    return W


# ====================================================================== 4b / 4a
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


def legs_4b_oos(b, sb):
    """The OOS-only reading of 4b used by rule 8: the OOS window is the whole sample."""
    return {"L_OOS_S": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "L_OOS_DD": bool(abs(b["OOS_MaxDD"]) <= DD_CAP * abs(sb["OOS_MaxDD"])),
            "L_OOS_CAGR": bool(b["OOS_CAGR"] >= CAGR_FLOOR * sb["OOS_CAGR"])}


def main():
    t0 = time.time()
    P(f"# Idea 1059 (cloud lane, {DATE}) — is the 4b PASS RATE's WEEKLY PEAK a COST-RUNG object?")
    P(f"# 2 tuned dials: COST RUNG {COSTS} bps x CADENCE {CADENCES} = "
      f"{len(COSTS)*len(CADENCES)} points, ALL reported, none selected.")
    P(f"# Census population (NOT a dial, 968's verbatim): {len(MECHS)} mechanisms x "
      f"{len(PANELS)} panels x the cadence's own phase family (P = {PLEN}) + the CANONICAL "
      f"period-end.  HEADLINE gross {GROSS_HEAD}; {GROSSES} all printed, never selected on.")
    P("# DECLARED BEFORE ANY NUMBER: cost enters only through realised turnover and SPY pays")
    P("#   none of it, so every rung shifts all five legs against the FAST cadences.  The naive")
    P("#   reading predicts the peak slides D (0 bps) -> Q (50 bps).  It can fail two ways:")
    P("#   (a) 0 bps does not rescue D because L_DD is a drawdown fact, not a cost fact;")
    P("#   (b) 50 bps does not spare Q because Q still pays ~111 bp/yr against a cost-free SPY,")
    P("#   so the peak can DIE rather than slide.  All three outcomes are reportable.")
    P(f"# NSEED = {NSEED} gross-matched null books per (panel, gross, cadence), re-priced at")
    P("#   every rung off the SAME draws.  SURVIVORSHIP: current-constituent panels; the bias is")
    P("#   common to books and null and flatters both L_CAGR and L_DD against a real SPY series.")
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
        PAN[p] = dict(px=px, idx=idx, rets=rets, ar=ar, warm=warm, oos=oos & warm,
                      spy=blocks(spyr, warm, oos & warm), T=len(idx),
                      yrs=warm.sum() / 252.0)
        P(f"  {p}: {px.shape[1]} cols x {len(idx)} days, {idx[0].date()} -> {idx[-1].date()}; "
          f"SPY full {PAN[p]['spy']['CAGR']:.2%} / {PAN[p]['spy']['Sharpe']:.4f} / "
          f"{PAN[p]['spy']['MaxDD']:.2%}  (SPY pays no turnover at any rung)")

    W1 = {(p, m): mech_w1(PXD[p], m) for p in PANELS for m in MECHS}
    NW1 = {(p, s): null_w1(PXD[p], s) for p in PANELS for s in range(NSEED)}

    def phase_masks(p, cad):
        """The cadence's phase family plus the CANONICAL calendar period-end (968's verbatim)."""
        ar, idx = PAN[p]["ar"], PAN[p]["idx"]
        P_ = PLEN[cad]
        out = [(q, (ar % P_) == q) for q in range(P_)]
        out.append((-1, rebalance_mask(idx, cad).values))
        return out

    # ================================================================== GATES
    P("=" * 100)
    P("REPRODUCTION GATES")
    P("=" * 100)
    gates = {}

    d1r = d1t = 0.0
    for m, cad in product(["CAND20", "NOR3", "BAND03"], CADENCES):
        px = PXD["U56"]
        w = GROSS_HEAD * W1[("U56", m)]
        mk = rebalance_mask(px.index, cad).values
        gr, mt = nrun(PAN["U56"]["rets"], lag(w), lagmask(mk))
        mine = gr - mt * COST_HEAD / 1e4
        eng = backtest(px, pd.DataFrame(w, index=px.index, columns=px.columns),
                       cost_bps=COST_HEAD, freq=cad)
        d1r = max(d1r, float(np.abs(mine[WARMUP:] - eng["returns"].values[WARMUP:]).max()))
        d1t = max(d1t, float(np.abs(mt[WARMUP:] - eng["turnover"].values[WARMUP:]).max()))
    gates["G1"] = (d1r < 1e-12 and d1t < 1e-12,
                   f"OUTSIDE-cost runner == engine.backtest(cost inside), 3 books x "
                   f"{len(CADENCES)} cadences at {COST_HEAD:.0f} bps: max|dret| {d1r:.2e}, "
                   f"max|dturn| {d1t:.2e}")

    d2 = float(np.abs(W1[("U56", "BAND03")]
                      - rules_v2_weights(PXD["U56"], BAND, GROSS_HEAD).values / GROSS_HEAD).max())
    gates["G2"] = (d2 == 0.0, f"BAND03 == rules_v2_weights/gross exactly: max|d| {d2:.2e}")

    gr, tt = nrun(PAN["U56"]["rets"], lag(GROSS_HEAD * W1[("U56", "CAND20")]),
                  lagmask(rebalance_mask(PXD["U56"].index, "W").values))
    trip = fmet((gr - tt * COST_HEAD / 1e4)[PAN["U56"]["warm"]])
    dl = [abs(trip[i] - CAND20_PUB[i]) for i in range(3)]
    gates["G3"] = (all(d <= t for d, t in zip(dl, G3_TOL)),
                   f"CROSS-RUN CAND20 weekly @{GROSS_HEAD} @{COST_HEAD:.0f}bps: {trip[0]:.4%} / "
                   f"{trip[1]:.4f} / {trip[2]:.2%} vs committed 12.66% / 1.0921 / -18.31% "
                   f"(|d| {dl[0]:.4f}/{dl[1]:.4f}/{dl[2]:.4f}, 961's own tolerance)")

    sp = PAN["U56"]["spy"]
    d4 = max(abs(sp["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
             abs(sp["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
             abs(sp["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gates["G4"] = (d4 < 5e-4, f"CROSS-RUN SPY OOS at {IS_END}: {sp['OOS_CAGR']:.4f} / "
                              f"{sp['OOS_Sharpe']:.4f} / {sp['OOS_MaxDD']:.4f} vs committed "
                              f"{SPY_OOS_COMMITTED} (max|d| {d4:.2e})")

    why6 = []
    for p, cad in product(PANELS, CADENCES):
        fam = [m for q, m in phase_masks(p, cad) if q >= 0]
        cov = np.sum(np.vstack(fam).astype(int), axis=0)
        if len(fam) != PLEN[cad] or cov.min() != 1 or cov.max() != 1:
            why6.append(f"{p}/{cad}")
    gates["G6"] = (not why6, "PHASE CONSTRUCTION: every cadence's family has exactly P members "
                             "and partitions the tape (each day in exactly one phase) at all "
                             f"{len(PANELS)*len(CADENCES)} (panel, cadence) points")

    a = nrun(PAN["U56"]["rets"], lag(0.75 * NW1[("U56", 0)]),
             lagmask(rebalance_mask(PXD["U56"].index, "M").values))[0]
    b = nrun(PAN["U56"]["rets"], lag(0.75 * NW1[("U56", 0)]),
             lagmask(rebalance_mask(PXD["U56"].index, "M").values))[0]
    nw2 = null_w1(PXD["U56"], 0)
    gates["G7"] = (float(np.abs(a - b).max()) == 0.0
                   and float(np.abs(nw2 - NW1[("U56", 0)]).max()) == 0.0,
                   "determinism: null weights and runs rebuild bit-for-bit off process-stable "
                   f"md5 seeds (seed ref {mdseed('NULL', 0, PAN['U56']['T'], PXD['U56'].shape[1])})")

    d8 = 0.0
    for p, g in product(PANELS, GROSSES):
        for cad in CADENCES:
            mk = (PAN[p]["ar"] % PLEN[cad]) == 0
            bw = (g * W1[(p, "CAND20")])[mk].sum(axis=1)
            nw = (g * NW1[(p, 0)])[mk].sum(axis=1)
            live = bw > 0
            if live.any():
                d8 = max(d8, float(np.abs(nw[live] - g).max()))
    gates["G8"] = (d8 < 1e-12, f"the null is gross-matched: max|null invested weight - gross| on "
                               f"the decision grid = {d8:.2e}")

    # G5 (cross-run of 968's committed pass-rate profile) and G9 (cost monotonicity) need the
    # census; they are filled in after (A) and printed with the rest.

    # ================================================================== (A) the census
    rows = []
    for p, cad, g, m in product(PANELS, CADENCES, GROSSES, MECHS):
        pan = PAN[p]
        w = lag(g * W1[(p, m)])
        for q, mk in phase_masks(p, cad):
            gr, t = nrun(pan["rets"], w, lagmask(mk))
            ty = float(t[pan["warm"]].sum() / pan["yrs"])
            for c in COSTS:
                r = gr - t * c / 1e4
                bl = blocks(r, pan["warm"], pan["oos"])
                lg = legs_4b(bl, pan["spy"])
                rows.append(dict(panel=p, cadence=cad, gross=g, mech=m, phase=q,
                                 canonical=int(q < 0), kind="BOOK", seed=-1, cost=c,
                                 turn_yr=ty, drag_bp=ty * c, **bl, **lg,
                                 pass4b=all(lg.values()),
                                 nfail=sum(1 for v in lg.values() if not v)))
    for p, cad, g, s in product(PANELS, CADENCES, GROSSES, range(NSEED)):
        pan = PAN[p]
        w = lag(g * NW1[(p, s)])
        mk = rebalance_mask(pan["idx"], cad).values
        gr, t = nrun(pan["rets"], w, lagmask(mk))
        ty = float(t[pan["warm"]].sum() / pan["yrs"])
        for c in COSTS:
            r = gr - t * c / 1e4
            bl = blocks(r, pan["warm"], pan["oos"])
            lg = legs_4b(bl, pan["spy"])
            rows.append(dict(panel=p, cadence=cad, gross=g, mech="NULL", phase=-1, canonical=1,
                             kind="NULL", seed=s, cost=c, turn_yr=ty, drag_bp=ty * c, **bl, **lg,
                             pass4b=all(lg.values()),
                             nfail=sum(1 for v in lg.values() if not v)))
    CEN = pd.DataFrame(rows)

    # ---- G5: reproduce 968's committed 10 bps pass-rate profile exactly
    g5d, g5s = 0.0, []
    for p in PANELS:
        got = []
        for cad in CADENCES:
            s = CEN[(CEN.kind == "BOOK") & (CEN.panel == p) & (CEN.gross == GROSS_HEAD)
                    & (CEN.cadence == cad) & (CEN.cost == COST_HEAD)]
            got.append(float(s.pass4b.mean()))
        g5d = max(g5d, max(abs(got[i] - PUB_968_PASS[p][i]) for i in range(4)))
        g5s.append(f"{p} " + " / ".join(f"{x:.3f}" for x in got) + " vs committed "
                   + " / ".join(f"{x:.3f}" for x in PUB_968_PASS[p]))
    gates["G5"] = (g5d < 1e-3, "CROSS-RUN 968's committed 10 bps / gross 0.75 4b PASS-RATE "
                               "profile (D/W/M/Q): " + "; ".join(g5s) + f"  max|d| {g5d:.2e}")

    # ---- G9: the outside-cost re-pricing is monotone in the rung for every single book
    bk = CEN[CEN.kind == "BOOK"].sort_values("cost")
    key = ["panel", "cadence", "gross", "mech", "phase"]
    bad = 0
    for _, grp in bk.groupby(key, sort=False):
        v = grp.CAGR.values
        if np.any(np.diff(v) > 1e-12):
            bad += 1
    gates["G9"] = (bad == 0, f"cost monotonicity: CAGR is non-increasing in the rung for "
                             f"{len(bk)//len(COSTS):,} of {len(bk)//len(COSTS):,} books "
                             f"({bad} violations) — the outside-cost re-pricing is exact")

    for k in sorted(gates, key=lambda s: int(s[1:])):
        ok, msg = gates[k]
        P(f"  {k} {'PASS' if ok else 'FAIL'}  {msg}")
    P(f"GATES: {sum(1 for v in gates.values() if v[0])} of {len(gates)} pass.")
    P("")

    P("=" * 100)
    P("(A) THE CENSUS — every cost rung x cadence x gross x mechanism x panel x phase book")
    P("=" * 100)
    dump(CEN, "census")
    P(f"  {int((CEN.kind=='BOOK').sum()):,} book rows + {int((CEN.kind=='NULL').sum()):,} null "
      f"rows = {len(CEN)//len(COSTS):,} distinct books x {len(COSTS)} rungs.")
    P("")

    # ================================================================== (B) the pass-rate surface
    P("=" * 100)
    P("(B) THE COST x CADENCE SURFACE — 4b PASS RATE (ALL 16 grid points, both panels)")
    P("=" * 100)
    prof = []
    for kind, p, g, c, cad in product(["BOOK", "NULL"], PANELS, GROSSES, COSTS, CADENCES):
        s = CEN[(CEN.kind == kind) & (CEN.panel == p) & (CEN.gross == g)
                & (CEN.cost == c) & (CEN.cadence == cad)]
        prof.append(dict(kind=kind, panel=p, gross=g, cost=c, cadence=cad, n=len(s),
                         pass4b=float(s.pass4b.mean()),
                         **{lg: float((~s[lg]).mean()) for lg in LEGS},
                         turn_yr=float(s.turn_yr.mean()), drag_bp=float(s.drag_bp.mean()),
                         MaxDD=float(s.MaxDD.mean()), CAGR=float(s.CAGR.mean())))
    PR = pd.DataFrame(prof)
    dump(PR, "surface")

    def surface(kind, g):
        return PR[(PR.kind == kind) & (PR.gross == g)].pivot_table(
            index=["panel", "cost"], columns="cadence", values="pass4b")[CADENCES]

    for kind in ["BOOK", "NULL"]:
        P(f"  {kind}S — 4b pass rate, gross {GROSS_HEAD} (rows = cost rung, cols = cadence):")
        for line in surface(kind, GROSS_HEAD).to_string(
                float_format=lambda x: f"{x:.3f}").split("\n"):
            P("    " + line)
        P("")
    P("  BOOKS — 4b pass rate at the other two gross levels (robustness, never selected on):")
    for g in [x for x in GROSSES if x != GROSS_HEAD]:
        P(f"    gross {g}:")
        for line in surface("BOOK", g).to_string(float_format=lambda x: f"{x:.3f}").split("\n"):
            P("      " + line)
    P("")

    # ---- the argmax walk ----
    P("  THE ARGMAX WALK (where the peak sits at each rung; ties listed):")
    arg = []
    for kind, p, g in product(["BOOK", "NULL"], PANELS, GROSSES):
        for c in COSTS:
            s = PR[(PR.kind == kind) & (PR.panel == p) & (PR.gross == g) & (PR.cost == c)]
            v = s.set_index("cadence").pass4b[CADENCES]
            mx = v.max()
            win = [cd for cd in CADENCES if v[cd] >= mx - 1e-12]
            arg.append(dict(kind=kind, panel=p, gross=g, cost=c, peak=mx,
                            argmax="+".join(win) if mx > 0 else "NONE",
                            ntied=len(win) if mx > 0 else 0,
                            unimodal=bool(all(np.diff(np.sign(np.diff(v.values))) <= 0)),
                            **{f"pass_{cd}": float(v[cd]) for cd in CADENCES}))
    AG = pd.DataFrame(arg)
    dump(AG, "argmax")
    for kind in ["BOOK", "NULL"]:
        t = AG[(AG.kind == kind) & (AG.gross == GROSS_HEAD)]
        P(f"    {kind}S gross {GROSS_HEAD}: " + " | ".join(
            f"{r.panel} {r.cost:.0f}bps -> {r.argmax} ({r.peak:.3f})" for r in t.itertuples()))
    P("")

    # ================================================================== (C) hypotheses
    P("=" * 100)
    P("(C) PRE-REGISTERED HYPOTHESES")
    P("=" * 100)
    H = {}
    u = AG[(AG.kind == "BOOK") & (AG.panel == "U56") & (AG.gross == GROSS_HEAD)].set_index("cost")

    a0, a50 = u.loc[0.0, "argmax"], u.loc[50.0, "argmax"]
    H["H_SLIDE"] = (a0 == "D" and a50 == "Q",
                    f"the queue's naive prediction — peak at D at 0 bps and at Q at 50 bps on "
                    f"U56/gross {GROSS_HEAD}: got 0 bps -> {a0}, 50 bps -> {a50}")

    moved = len({u.loc[c, "argmax"] for c in COSTS}) > 1
    H["H_MOVE"] = (moved, "the peak MOVES at all across the rung ladder (the weak form: if it "
                          "does not, PROTOCOL's 10 bps is not choosing the cadence): argmaxes "
                          + " -> ".join(f"{c:.0f}bps {u.loc[c,'argmax']}" for c in COSTS))

    uni = bool(u.unimodal.all())
    H["H_PEAK"] = (uni, "the profile stays SINGLE-PEAKED in cadence at every rung: "
                        + " ".join(f"{c:.0f}bps {'uni' if u.loc[c,'unimodal'] else 'MULTI'}"
                                   for c in COSTS))

    nu = AG[(AG.kind == "NULL") & (AG.panel == "U56") & (AG.gross == GROSS_HEAD)].set_index("cost")
    same = sum(1 for c in COSTS if nu.loc[c, "argmax"] == u.loc[c, "argmax"])
    H["H_NULL"] = (same >= 3, "a gross-matched COIN FLIP shows the same peak location at >=3 of "
                              f"4 rungs (i.e. the peak is a cadence/cost object, not a book "
                              f"object): agree at {same} of 4; null argmaxes "
                              + " -> ".join(f"{c:.0f}bps {nu.loc[c,'argmax']}" for c in COSTS))

    # H_DRAG: is the peak's location predicted by a constant DRAG BUDGET?
    # The 0 bps rung is EXCLUDED by construction: its drag is identically 0 at every cadence, so
    # a drag ratio against it is degenerate (infinite) and says nothing about the peak.  Stated
    # here rather than dropped silently; the 0 bps peak is reported everywhere else.
    dr = []
    for c in [x for x in COSTS if x > 0]:
        cd = u.loc[c, "argmax"].split("+")[0]
        if cd == "NONE":
            continue
        row = PR[(PR.kind == "BOOK") & (PR.panel == "U56") & (PR.gross == GROSS_HEAD)
                 & (PR.cost == c) & (PR.cadence == cd)]
        dr.append((c, cd, float(row.drag_bp.iloc[0])))
    if len(dr) >= 2:
        dv = [d for _, _, d in dr]
        spread = max(dv) / max(min(dv), 1e-9)
        H["H_DRAG"] = (spread <= 2.0, "the winning cadence's own annual DRAG is roughly constant "
                                      f"across the POSITIVE rungs (<=2x spread; 0 bps excluded, "
                                      f"its drag is identically 0): "
                                      + ", ".join(f"{c:.0f}bps {cd} {d:.0f}bp/yr"
                                                  for c, cd, d in dr)
                                      + f" -> spread {spread:.2f}x")
    else:
        H["H_DRAG"] = (False, "the winning cadence's own annual DRAG: fewer than 2 rungs have any "
                              "passing cadence at all — the peak died before it could slide")

    # ================================================================== (D) rule 8
    P("")
    P("=" * 100)
    P("(D) RULE 8 WALK-FORWARD — cadence chosen on 2009-2016 ALONE, evaluated on 2017-2026")
    P("=" * 100)
    P("    Choosers (IS-only, canonical phase, legal at the split): C_ISSHARPE = best IS Sharpe;")
    P("    C_ISLEGS = most 4b legs cleared IS (tie -> IS Sharpe).  The live RULES v2 comparand is")
    P("    priced at the SAME rung as the candidate; SPY pays no cost at any rung.")
    wf = []
    for p, g, c, m in product(PANELS, GROSSES, COSTS, MECHS):
        pan = PAN[p]
        cand = {}
        for cad in CADENCES:
            s = CEN[(CEN.kind == "BOOK") & (CEN.panel == p) & (CEN.gross == g) & (CEN.cost == c)
                    & (CEN.mech == m) & (CEN.cadence == cad) & (CEN.canonical == 1)]
            cand[cad] = s.iloc[0]
        # live RULES v2 at this rung (BAND03 @ gross 0.75, weekly, canonical) — the 4a comparand
        v2 = CEN[(CEN.kind == "BOOK") & (CEN.panel == p) & (CEN.gross == GROSS_HEAD)
                 & (CEN.cost == c) & (CEN.mech == "BAND03") & (CEN.cadence == "W")
                 & (CEN.canonical == 1)].iloc[0]
        is_sh = {cad: cand[cad].IS_Sharpe for cad in CADENCES}
        pick_s = max(CADENCES, key=lambda cd: is_sh[cd])
        is_legs = {}
        for cad in CADENCES:
            r = cand[cad]
            is_legs[cad] = sum([r.IS_Sharpe > pan["spy"]["IS_Sharpe"],
                                abs(r.IS_MaxDD) <= DD_CAP * abs(pan["spy"]["IS_MaxDD"]),
                                r.IS_CAGR >= CAGR_FLOOR * pan["spy"]["IS_CAGR"]])
        pick_l = max(CADENCES, key=lambda cd: (is_legs[cd], is_sh[cd]))
        oos_best = max(CADENCES, key=lambda cd: cand[cd].OOS_Sharpe)
        for chooser, pick in [("C_ISSHARPE", pick_s), ("C_ISLEGS", pick_l)]:
            r = cand[pick]
            ol = legs_4b_oos(r, pan["spy"])
            wf.append(dict(panel=p, gross=g, cost=c, mech=m, chooser=chooser, pick=pick,
                           oos_best=oos_best, hit=bool(pick == oos_best),
                           OOS_CAGR=float(r.OOS_CAGR), OOS_Sharpe=float(r.OOS_Sharpe),
                           OOS_MaxDD=float(r.OOS_MaxDD),
                           spy_OOS_CAGR=pan["spy"]["OOS_CAGR"],
                           spy_OOS_Sharpe=pan["spy"]["OOS_Sharpe"],
                           spy_OOS_MaxDD=pan["spy"]["OOS_MaxDD"],
                           v2_OOS_CAGR=float(v2.OOS_CAGR), v2_OOS_Sharpe=float(v2.OOS_Sharpe),
                           v2_OOS_MaxDD=float(v2.OOS_MaxDD),
                           CAGR=float(r.CAGR), Sharpe=float(r.Sharpe), MaxDD=float(r.MaxDD),
                           H1=float(r.H1), H2=float(r.H2),
                           **{lg: bool(r[lg]) for lg in LEGS}, **ol,
                           pass4b=bool(r.pass4b), pass4b_oos=all(ol.values()),
                           pass4a=bool(r.H1 > v2.H1 and r.H2 > v2.H2
                                       and r.MaxDD >= v2.MaxDD)))
    WF = pd.DataFrame(wf)
    dump(WF, "walkforward")

    P("")
    P("    OOS by rung x chooser, gross 0.75, both panels (means over the 6 mechanisms):")
    t = WF[WF.gross == GROSS_HEAD].groupby(["panel", "chooser", "cost"]).agg(
        n=("pick", "size"), hit=("hit", "mean"), OOS_CAGR=("OOS_CAGR", "mean"),
        OOS_Sharpe=("OOS_Sharpe", "mean"), OOS_MaxDD=("OOS_MaxDD", "mean"),
        spy_S=("spy_OOS_Sharpe", "mean"), v2_S=("v2_OOS_Sharpe", "mean"),
        p4b=("pass4b", "mean"), p4b_oos=("pass4b_oos", "mean"), p4a=("pass4a", "mean"))
    for line in t.to_string(float_format=lambda x: f"{x:.3f}").split("\n"):
        P("      " + line)
    P("")
    P("    the IS chooser's PICK by rung (does an IS-only chooser find the rung's peak cadence?):")
    for p, ch in product(PANELS, ["C_ISSHARPE", "C_ISLEGS"]):
        for c in COSTS:
            s = WF[(WF.panel == p) & (WF.chooser == ch) & (WF.cost == c)
                   & (WF.gross == GROSS_HEAD)]
            picks = s.pick.value_counts().to_dict()
            peak = u.loc[c, "argmax"] if p == "U56" else AG[
                (AG.kind == "BOOK") & (AG.panel == p) & (AG.gross == GROSS_HEAD)
                & (AG.cost == c)].argmax.iloc[0]
            P(f"      {p} {ch} {c:5.0f}bps picks {picks}  full-sample peak {peak}  "
              f"hit {s.hit.mean():.3f}  OOS 4b {s.pass4b_oos.mean():.3f}")
    P("")

    ws = WF[(WF.gross == GROSS_HEAD) & (WF.cost == COST_HEAD) & (WF.chooser == "C_ISSHARPE")]
    H["H_RULE8"] = (bool(ws.pass4b_oos.mean() >= 0.5),
                    f"at PROTOCOL's own rung ({COST_HEAD:.0f} bps, gross {GROSS_HEAD}), the "
                    f"IS-Sharpe cadence chooser's pick clears the OOS reading of 4b in at least "
                    f"half of the {len(ws)} (panel, mechanism) cells: got "
                    f"{ws.pass4b_oos.mean():.3f} ({int(ws.pass4b_oos.sum())} of {len(ws)}), "
                    f"hit rate on the OOS-best cadence {ws.hit.mean():.3f}")

    P("=" * 100)
    P("HYPOTHESES")
    P("=" * 100)
    for k, (ok, msg) in H.items():
        P(f"  {k:10s} {'PASS' if ok else 'FAIL'}  {msg}")
    P(f"HYPOTHESES: {sum(1 for v in H.values() if v[0])} of {len(H)} pass.")
    pd.DataFrame([dict(hypothesis=k, verdict="PASS" if v[0] else "FAIL", detail=v[1])
                  for k, v in H.items()]).to_csv(f"{OUT}.hypotheses.csv", index=False)
    pd.DataFrame([dict(gate=k, verdict="PASS" if v[0] else "FAIL", detail=v[1])
                  for k, v in gates.items()]).to_csv(f"{OUT}.gates.csv", index=False)

    # ================================================================== (E) KEEP paths
    P("")
    P("=" * 100)
    P("(E) BOTH KEEP PATHS — every rung, gross 0.75, canonical phase, 6 mechanisms x 2 panels")
    P("=" * 100)
    kp = []
    for p, c in product(PANELS, COSTS):
        s = CEN[(CEN.kind == "BOOK") & (CEN.panel == p) & (CEN.gross == GROSS_HEAD)
                & (CEN.cost == c) & (CEN.canonical == 1)]
        v2 = s[(s.mech == "BAND03") & (s.cadence == "W")].iloc[0]
        n4a = int(((s.H1 > v2.H1) & (s.H2 > v2.H2) & (s.MaxDD >= v2.MaxDD)).sum())
        kp.append(dict(panel=p, cost=c, n=len(s), pass4b=int(s.pass4b.sum()), pass4a=n4a,
                       both=int((((s.H1 > v2.H1) & (s.H2 > v2.H2) & (s.MaxDD >= v2.MaxDD))
                                 & s.pass4b).sum())))
    KP = pd.DataFrame(kp)
    dump(KP, "keeppaths")
    for line in KP.to_string(index=False).split("\n"):
        P("    " + line)
    P("")
    winners = CEN[(CEN.kind == "BOOK") & (CEN.cost == COST_HEAD) & (CEN.gross == GROSS_HEAD)
                  & (CEN.canonical == 1) & (CEN.pass4b)]
    P(f"    canonical-phase 4b passers at {COST_HEAD:.0f} bps / gross {GROSS_HEAD}: "
      f"{len(winners)} of {len(CEN[(CEN.kind=='BOOK') & (CEN.cost==COST_HEAD) & (CEN.gross==GROSS_HEAD) & (CEN.canonical==1)])}")
    if len(winners):
        for line in winners[["panel", "cadence", "mech", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                             "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]].to_string(
                index=False, float_format=lambda x: f"{x:.4f}").split("\n"):
            P("      " + line)
    P("")
    P(f"Runtime {time.time()-t0:.1f}s.")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

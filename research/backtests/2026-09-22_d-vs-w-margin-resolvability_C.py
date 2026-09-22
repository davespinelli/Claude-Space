#!/usr/bin/env python3
"""Idea 1062 (lane C, 2026-09-22) — is the D-vs-W MARGIN at 10 bps RESOLVABLE AT ALL?

QUESTION (QUEUE idea 1062, the line at the SMALLER file offset, verbatim)
    idea 1059 found PROTOCOL's rung is decisive at exactly one boundary: between 0 and 10 bps
    DAILY's 4b pass rate falls 0.833 -> 0.333 while WEEKLY does not move, and at 25 bps D is
    0.000.  Solve for the rung at which D's pass rate crosses W's on a fine ladder
    (2/5/7.5/10/15 bps), and measure that crossing's own sampling width against the 12-book
    denominator D's cell carries.  If the width spans the whole 0-25 bps range, 968's weekly
    headline is a one-book-margin claim.  Max 2 params (rung ladder, denominator).

    NOTE ON THE LABEL.  Two lines in '## Open' carry the number 1062 (standing defect 932).
    This script answers the one at the SMALLER file offset, slug
    `is-the-D-vs-W-MARGIN-at-10-bps-RESOLVABLE-at-ALL`.  The other 1062
    (`is-the-QUARTER-END-REBALANCE-PENALTY-...`) is untouched and stays OPEN.

THE OBJECT, STATED EXACTLY.  968/1059's headline is a PASS RATE: over one (panel, gross) cell,
    the fraction of a fixed book population that clears all five 4b legs.  The population at
    cadence X is 6 mechanism arms x (that cadence's own P phase members + the CANONICAL calendar
    period-end), so n = 6*(P+1) = 12 at D and 36 at W.  The headline "weekly beats daily at
    10 bps" is therefore a comparison of a 12-denominator rate against a 36-denominator rate.
    One book at D is worth 1/12 = 0.0833 of pass rate; one book at W is worth 1/36 = 0.0278.

WHAT IS ACTUALLY BEING MEASURED, DECLARED BEFORE ANY NUMBER.
    A pass rate over n books is not n independent draws.  The 6 mechanism arms share a panel, a
    tape, a warm-up, a gross and (at D) very nearly a holding pattern; the P phase members of one
    mechanism are the SAME rule started on different days.  So the honest denominator is closer
    to 6 (mechanisms) than to 12 or 36, and the phase family is a within-arm replicate, not an
    independent book.  This run therefore reports THREE denominators and never selects one:
      DEN_FULL    6 mech x (P+1) phases  — 1059's own population (D n=12, W n=36).  UNMATCHED:
                  D and W are scored on different-sized populations.
      DEN_CANON   the CANONICAL period-end alone, 6 mech — MATCHED at n=6 for every cadence, so
                  D and W are scored on the same six rules started the same way.
      DEN_PHASE   the P phase members alone, no canonical (D n=6, W n=30).
    and clusters every interval estimate BY MECHANISM, because that is the level at which the
    books are actually distinct.

THE ARITHMETIC, DECLARED BEFORE ANY NUMBER (a prediction, not a post-hoc story).
    Cost enters only through realised turnover; SPY, which every 4b leg is read against, pays
    none of it.  1059 measured ~22.4 turns/yr at D and ~9.0 at W on U56, so the annual drag of a
    rung c is ~2.24c bp at D and ~0.90c bp at W.  The DIFFERENCE in drag is ~1.34c bp/yr.  If the
    D-vs-W margin were a pure cost object, it would be ZERO at c = 0 and grow LINEARLY in c, and
    a crossing rung c* would be the point where 1.34c bp/yr eats D's CAGR headroom over the
    0.70*SPY floor.  Two ways this can fail, both reportable:
      (a) the margin is a STEP, not a ramp: with n = 12 the rate can only move in 0.0833 jumps,
          so c* is not a point but the INTERVAL between the two rungs that bracket one book's
          flip, and that interval can be wide enough to swallow the whole ladder;
      (b) the margin is non-zero at c = 0, in which case it is not a cost object at all and
          1059's "10 bps is a cadence chooser" reading is mis-attributed.

THE TWO DIALS (rule 4, no more than two tuned parameters)
    1. COST-RUNG LADDER  {0, 2, 5, 7.5, 10, 15, 25, 50} bps — the queue's fine ladder
       {2, 5, 7.5, 10, 15} plus PROTOCOL's 0/10/25/50 so 1059's cells are reproduced in place.
    2. DENOMINATOR       {DEN_FULL, DEN_CANON, DEN_PHASE}
    ALL 8 x 3 = 24 grid points are reported, at every panel and gross.  PANEL {U56, B136},
    GROSS {0.50, 0.75, 1.00} and the 6 MECHANISM arms are REPORTED, NEVER SELECTED ON.
    Cadences M and Q are carried at gross 0.75 for continuity with 968/1059, not tuned.

RULE 8.  A walk-forward that chooses the CADENCE on 2009-2016 alone (two IS-only choosers: IS
    Sharpe, and the IS 4b leg count) at every rung and every denominator, and evaluates
    2017-2026 untouched against SPY and against the live RULES v2 book priced at the SAME rung.
    Both KEEP paths are evaluated at every grid point: 4a against live RULES v2 on the book's own
    panel at the book's own rung, 4b against SPY.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-CONSTITUENT panels.  The bias is common to every
    cadence in the comparison, so it cancels in a D-vs-W MARGIN, but it flatters both the CAGR
    floor and the DD cap against SPY, which is a real index, in every absolute figure printed.
"""
from __future__ import annotations

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

DATE = "2026-09-22"
SLUG = "d-vs-w-margin-resolvability"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

LAG = 1
WARMUP = 260
NTOP = 20
MAXVOL = 0.60
BAND = 0.03
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70

# ---- DIAL 1: the fine cost ladder -------------------------------------------------------------
COSTS = [0.0, 2.0, 5.0, 7.5, 10.0, 15.0, 25.0, 50.0]
COST_HEAD = 10.0                                  # PROTOCOL rule 2
PUB_RUNGS = [0.0, 10.0, 25.0, 50.0]               # 1059's own ladder, a subset of ours
# ---- DIAL 2: the denominator ------------------------------------------------------------------
DENOMS = ["DEN_FULL", "DEN_CANON", "DEN_PHASE"]
DEN_HEAD = "DEN_FULL"                             # 1059's own; reported first, not preferred

CADENCES = ["D", "W", "M", "Q"]
PAIR = ["D", "W"]                                 # the margin this idea is about
PLEN = {"D": 1, "W": 5, "M": 21, "Q": 63}
GROSSES = [0.50, 0.75, 1.00]
GROSS_HEAD = 0.75
PANELS = ["U56", "B136"]
MECHS = ["CAND20", "R3_55", "R3_84", "NOR3", "MOMONLY", "BAND03"]
LEGSETS = {"CAND20": [(21, 252), (0, 126), (0, 63)],
           "R3_55": [(21, 252), (0, 126), (0, 55)],
           "R3_84": [(21, 252), (0, 126), (0, 84)],
           "NOR3": [(21, 252), (0, 126)],
           "MOMONLY": [(21, 252)]}
LEGS = ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]

NBOOT = 2000
BOOT_SEED = 106200
CAND20_PUB = (0.1266, 1.0921, -0.1831)
G3_TOL = (5e-3, 3.3e-2, 5e-3)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
PUB_1059_PASS = {"U56": {0.0: [0.833, 0.833, None, None], 10.0: [0.333, 0.833, 0.205, 0.044],
                         25.0: [0.000, None, None, None]},
                 "B136": {10.0: [0.000, 0.028, 0.000, 0.000]}}
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ====================================================================== runner (gated at G1)
def nrun(rets, wt, mk):
    """GROSS returns and turnover.  Cost is applied OUTSIDE (r - turn*c/1e4) so ONE run prices
    every rung on the ladder; G1 gates that against engine.backtest, which charges cost inside.
    Verbatim from idea 1059's committed script so the two runs are the same object."""
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


# ====================================================================== the books (1059 verbatim)
def legs_composite(px, legs):
    parts = []
    for skip, look in legs:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return sum(parts) / len(parts)


def mech_w1(px, mech):
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


# ====================================================================== 4a / 4b
def blocks(r, warm, oos):
    rr = r[warm]
    c, s, d = fmet(rr)
    h = len(rr) // 2
    oc, os_, od = fmet(r[oos])
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
    """PROTOCOL 4a: Sharpe > live RULES v2 in BOTH halves AND MaxDD no worse."""
    return {"A_H1": bool(b["H1"] > lb["H1"]), "A_H2": bool(b["H2"] > lb["H2"]),
            "A_DD": bool(b["MaxDD"] >= lb["MaxDD"])}


def wilson(k, n, z=1.959963984540054):
    if n == 0:
        return (np.nan, np.nan)
    p = k / n
    d = 1.0 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def main():
    t0 = time.time()
    P(f"# Idea 1062 (lane C, {DATE}) — is the D-vs-W MARGIN at 10 bps RESOLVABLE AT ALL?")
    P(f"# DIAL 1 = COST-RUNG LADDER {COSTS} bps ({len(COSTS)} rungs).")
    P(f"# DIAL 2 = DENOMINATOR {DENOMS}.  ALL {len(COSTS)*len(DENOMS)} grid points reported.")
    P(f"# REPORTED, NEVER SELECTED ON: panel {PANELS}, gross {GROSSES}, "
      f"{len(MECHS)} mechanism arms, cadences {CADENCES}.")
    P("# DECLARED BEFORE ANY NUMBER: a pass rate over n books is NOT n independent draws — the")
    P("#   P phase members of one mechanism are the SAME rule started on different days, so the")
    P("#   honest cluster is the MECHANISM (6), not the book (12 at D, 36 at W).  Every interval")
    P("#   in this run is therefore reported twice: a naive Wilson interval at the published")
    P("#   denominator, and a MECHANISM-CLUSTERED bootstrap.  If the margin is a pure cost")
    P("#   object it is ZERO at 0 bps and grows ~linearly; if it is a STEP on a 12-book grid the")
    P("#   crossing is an INTERVAL, not a point.  Both outcomes are reportable.")
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
                      spy=blocks(spyr, warm, oos & warm), T=len(idx), yrs=warm.sum() / 252.0)
        P(f"  {p}: {px.shape[1]} cols x {len(idx)} days, {idx[0].date()} -> {idx[-1].date()}; "
          f"SPY full {PAN[p]['spy']['CAGR']:.2%} / {PAN[p]['spy']['Sharpe']:.4f} / "
          f"{PAN[p]['spy']['MaxDD']:.2%}; SPY OOS {PAN[p]['spy']['OOS_CAGR']:.2%} / "
          f"{PAN[p]['spy']['OOS_Sharpe']:.4f} / {PAN[p]['spy']['OOS_MaxDD']:.2%}")

    W1 = {(p, m): mech_w1(PXD[p], m) for p in PANELS for m in MECHS}

    # ---- the LIVE RULES v2 book, priced at every rung on each panel (the 4a comparand) --------
    LIVE = {}
    for p in PANELS:
        w = rules_v2_weights(PXD[p], BAND, GROSS_HEAD).values
        gr, t = nrun(PAN[p]["rets"], lag(w), lagmask(rebalance_mask(PAN[p]["idx"], "W").values))
        for c in COSTS:
            LIVE[(p, c)] = blocks(gr - t * c / 1e4, PAN[p]["warm"], PAN[p]["oos"])
        lb = LIVE[(p, COST_HEAD)]
        P(f"  LIVE RULES v2 {p} @{COST_HEAD:.0f}bps: {lb['CAGR']:.2%} / {lb['Sharpe']:.4f} / "
          f"{lb['MaxDD']:.2%}  (halves {lb['H1']:.4f} / {lb['H2']:.4f}; OOS "
          f"{lb['OOS_CAGR']:.2%} / {lb['OOS_Sharpe']:.4f} / {lb['OOS_MaxDD']:.2%})")
    P("")

    def phase_masks(p, cad):
        """1059's verbatim population: the cadence's P phase members + the CANONICAL period-end
        (labelled -1)."""
        ar, idx = PAN[p]["ar"], PAN[p]["idx"]
        P_ = PLEN[cad]
        out = [(q, (ar % P_) == q) for q in range(P_)]
        out.append((-1, rebalance_mask(idx, cad).values))
        return out

    # ================================================================== GATES
    P("=" * 100)
    P("REPRODUCTION GATES — printed BEFORE any hypothesis is read")
    P("=" * 100)
    gates = {}

    d1r = d1t = 0.0
    for m, cad, c in product(["CAND20", "NOR3", "BAND03"], PAIR, [7.5, 15.0]):
        px = PXD["U56"]
        w = GROSS_HEAD * W1[("U56", m)]
        mk = rebalance_mask(px.index, cad).values
        gr, mt = nrun(PAN["U56"]["rets"], lag(w), lagmask(mk))
        mine = gr - mt * c / 1e4
        eng = backtest(px, pd.DataFrame(w, index=px.index, columns=px.columns),
                       cost_bps=c, freq=cad)
        d1r = max(d1r, float(np.abs(mine[WARMUP:] - eng["returns"].values[WARMUP:]).max()))
        d1t = max(d1t, float(np.abs(mt[WARMUP:] - eng["turnover"].values[WARMUP:]).max()))
    gates["G1"] = (d1r < 1e-12 and d1t < 1e-12,
                   f"OUTSIDE-cost runner == engine.backtest (cost inside) at the NEW fine rungs "
                   f"7.5 and 15 bps, 3 books x {len(PAIR)} cadences: max|dret| {d1r:.2e}, "
                   f"max|dturn| {d1t:.2e}")

    d2 = float(np.abs(W1[("U56", "BAND03")]
                      - rules_v2_weights(PXD["U56"], BAND, GROSS_HEAD).values / GROSS_HEAD).max())
    gates["G2"] = (d2 == 0.0, f"BAND03 == rules_v2_weights/gross EXACTLY: max|d| {d2:.2e}")

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

    # G4b ISOLATES the channel G4 measures: 1059 ran on 2026-09-16 and the committed price cache
    # has since grown.  Truncating THIS tape to 1059's own last date and re-reading SPY OOS says
    # whether the G4 residual is the VINTAGE or a construction difference.  This is a DIAGNOSTIC,
    # not a loosened gate: G4 above keeps its original 5e-4 tolerance and its original verdict.
    cut = pd.Timestamp("2026-09-16")
    pxc = PXD["U56"].loc[:cut]
    arc = np.arange(len(pxc))
    spc = blocks(pxc["SPY"].pct_change().fillna(0.0).values, arc >= WARMUP,
                 np.asarray(pxc.index > pd.Timestamp(IS_END)) & (arc >= WARMUP))
    d4b = max(abs(spc["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
              abs(spc["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
              abs(spc["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gates["G4b"] = (d4b < d4, f"VINTAGE ISOLATION for G4: this tape ends {PAN['U56']['idx'][-1].date()}, "
                              f"1059's ended {cut.date()} ({len(PXD['U56']) - len(pxc)} extra sessions). "
                              f"TRUNCATED to 1059's last date SPY OOS reads {spc['OOS_CAGR']:.4f} / "
                              f"{spc['OOS_Sharpe']:.4f} / {spc['OOS_MaxDD']:.4f}, max|d| {d4b:.2e} "
                              f"vs the untruncated {d4:.2e} — the G4 residual is the PRICE-CACHE "
                              f"VINTAGE, and it SHRINKS when the vintage is matched" if d4b < d4 else
                              f"VINTAGE ISOLATION for G4: truncation does NOT shrink the residual "
                              f"({d4b:.2e} vs {d4:.2e}) — the G4 failure is NOT a vintage effect")

    why6 = []
    for p, cad in product(PANELS, CADENCES):
        fam = [m for q, m in phase_masks(p, cad) if q >= 0]
        cov = np.sum(np.vstack(fam).astype(int), axis=0)
        if len(fam) != PLEN[cad] or cov.min() != 1 or cov.max() != 1:
            why6.append(f"{p}/{cad}")
    gates["G6"] = (not why6, "PHASE CONSTRUCTION: every cadence's family has exactly P members "
                             "and partitions the tape (each day in exactly one phase) at all "
                             f"{len(PANELS)*len(CADENCES)} (panel, cadence) points")

    gates["G10"] = (set(PUB_RUNGS).issubset(set(COSTS)),
                    f"the fine ladder {COSTS} CONTAINS 1059's published rungs {PUB_RUNGS}, so "
                    f"its cells are reproduced IN PLACE, not interpolated")

    # ================================================================== (A) the census
    P("")
    rows = []
    for p in PANELS:
        pan = PAN[p]
        for cad in CADENCES:
            for g in GROSSES:
                if cad not in PAIR and g != GROSS_HEAD:
                    continue           # M/Q carried at the headline gross only, for continuity
                for m in MECHS:
                    w = lag(g * W1[(p, m)])
                    for q, mk in phase_masks(p, cad):
                        grr, t = nrun(pan["rets"], w, lagmask(mk))
                        ty = float(t[pan["warm"]].sum() / pan["yrs"])
                        for c in COSTS:
                            r = grr - t * c / 1e4
                            bl = blocks(r, pan["warm"], pan["oos"])
                            l4b = legs_4b(bl, pan["spy"])
                            l4a = legs_4a(bl, LIVE[(p, c)])
                            rows.append(dict(panel=p, cadence=cad, gross=g, mech=m, phase=q,
                                             canonical=int(q < 0), cost=c, turn_yr=ty,
                                             drag_bp=ty * c, **bl, **l4b, **l4a,
                                             pass4b=all(l4b.values()), pass4a=all(l4a.values()),
                                             nfail=sum(1 for v in l4b.values() if not v)))
    CEN = pd.DataFrame(rows)

    # ---- G5: reproduce 1059's committed pass-rate cells at DEN_FULL, gross 0.75 --------------
    g5d, g5s = 0.0, []
    for p in PANELS:
        for c, prof in PUB_1059_PASS[p].items():
            got = []
            for i, cad in enumerate(CADENCES):
                s = CEN[(CEN.panel == p) & (CEN.gross == GROSS_HEAD) & (CEN.cadence == cad)
                        & (CEN.cost == c)]
                got.append(float(s.pass4b.mean()) if len(s) else np.nan)
                if prof[i] is not None and len(s):
                    g5d = max(g5d, abs(got[-1] - prof[i]))
            g5s.append(f"{p}@{c:g}bps " + "/".join("na" if np.isnan(x) else f"{x:.3f}"
                                                   for x in got)
                       + " vs committed " + "/".join("-" if v is None else f"{v:.3f}"
                                                     for v in prof))
    gates["G5"] = (g5d < 1e-3, "CROSS-RUN 1059's committed 4b PASS-RATE cells (D/W/M/Q, gross "
                               f"{GROSS_HEAD}, DEN_FULL): " + "; ".join(g5s) + f"  max|d| {g5d:.2e}")

    bad = 0
    key = ["panel", "cadence", "gross", "mech", "phase"]
    for _, grp in CEN.sort_values("cost").groupby(key, sort=False):
        if np.any(np.diff(grp.CAGR.values) > 1e-12):
            bad += 1
    nbk = len(CEN) // len(COSTS)
    gates["G9"] = (bad == 0, f"cost monotonicity: CAGR non-increasing in the rung for "
                             f"{nbk - bad:,} of {nbk:,} books ({bad} violations) — the "
                             f"outside-cost re-pricing is exact on the FINE ladder too")

    d11 = 0.0
    for p in PANELS:
        s = CEN[(CEN.panel == p) & (CEN.cost == 0.0)]
        d11 = max(d11, float(np.abs(s.drag_bp).max()))
    gates["G11"] = (d11 == 0.0, f"the 0 bps rung charges nothing: max|drag| {d11:.2e} bp/yr")

    for k in sorted(gates, key=lambda s: (int(s[1:].rstrip("ab")), s)):
        ok, msg = gates[k]
        P(f"  {k} {'PASS' if ok else 'FAIL'}  {msg}")
    P(f"GATES: {sum(1 for v in gates.values() if v[0])} of {len(gates)} pass.")
    P("")

    P("=" * 100)
    P("(A) THE CENSUS — every (panel, cadence, gross, mechanism, phase) book x fine rung")
    P("=" * 100)
    dump(CEN, "census")
    P(f"  {nbk:,} distinct books x {len(COSTS)} rungs = {len(CEN):,} rows.")
    P("")

    # ================================================================== (B) the fine surface
    def sub(p, g, cad, c, den):
        s = CEN[(CEN.panel == p) & (CEN.gross == g) & (CEN.cadence == cad) & (CEN.cost == c)]
        if den == "DEN_CANON":
            s = s[s.canonical == 1]
        elif den == "DEN_PHASE":
            s = s[s.canonical == 0]
        return s

    P("=" * 100)
    P("(B) THE FINE COST LADDER x DENOMINATOR SURFACE — 4b pass rate, ALL grid points")
    P("=" * 100)
    surf = []
    for p, g, den, c, cad in product(PANELS, GROSSES, DENOMS, COSTS, CADENCES):
        if cad not in PAIR and g != GROSS_HEAD:
            continue
        s = sub(p, g, cad, c, den)
        if not len(s):
            continue
        k = int(s.pass4b.sum())
        lo, hi = wilson(k, len(s))
        surf.append(dict(panel=p, gross=g, denom=den, cost=c, cadence=cad, n=len(s), k=k,
                         pass4b=k / len(s), wilson_lo=lo, wilson_hi=hi,
                         pass4a=float(s.pass4a.mean()),
                         **{lg: float((~s[lg]).mean()) for lg in LEGS},
                         turn_yr=float(s.turn_yr.mean()), drag_bp=float(s.drag_bp.mean()),
                         CAGR=float(s.CAGR.mean()), MaxDD=float(s.MaxDD.mean())))
    SURF = pd.DataFrame(surf)
    dump(SURF, "surface")

    for p in PANELS:
        for den in DENOMS:
            t = SURF[(SURF.panel == p) & (SURF.gross == GROSS_HEAD) & (SURF.denom == den)]
            t = t.pivot_table(index="cost", columns="cadence", values="pass4b")
            cols = [c for c in CADENCES if c in t.columns]
            P(f"  {p} gross {GROSS_HEAD} {den} (n: " + ", ".join(
                f"{cad}={int(SURF[(SURF.panel==p)&(SURF.gross==GROSS_HEAD)&(SURF.denom==den)&(SURF.cadence==cad)].n.iloc[0])}"
                for cad in cols) + ")  4b pass rate by rung:")
            for line in t[cols].to_string(float_format=lambda x: f"{x:.4f}").split("\n"):
                P("    " + line)
            P("")

    # ================================================================== (C) the margin & crossing
    P("=" * 100)
    P("(C) THE D-vs-W MARGIN M(c) = pass4b(W) - pass4b(D), AND ITS CROSSING RUNG")
    P("=" * 100)
    P("  A 'crossing' needs a sign change.  M(c) is reported at every rung; c* is located by")
    P("  LINEAR INTERPOLATION between the two bracketing rungs where M changes sign, and the")
    P("  BRACKET ITSELF is printed beside it because a step function has no interior point.")
    marg = []
    for p, g, den in product(PANELS, GROSSES, DENOMS):
        for c in COSTS:
            sd, sw = sub(p, g, "D", c, den), sub(p, g, "W", c, den)
            if not len(sd) or not len(sw):
                continue
            pd_, pw = sd.pass4b.mean(), sw.pass4b.mean()
            marg.append(dict(panel=p, gross=g, denom=den, cost=c, nD=len(sd), nW=len(sw),
                             passD=pd_, passW=pw, M=pw - pd_,
                             books_D=int(sd.pass4b.sum()), books_W=int(sw.pass4b.sum()),
                             one_book_D=1.0 / len(sd), one_book_W=1.0 / len(sw),
                             M_in_D_books=(pw - pd_) * len(sd)))
    MG = pd.DataFrame(marg)
    dump(MG, "margin")

    cross = []
    for p, g, den in product(PANELS, GROSSES, DENOMS):
        t = MG[(MG.panel == p) & (MG.gross == g) & (MG.denom == den)].sort_values("cost")
        if not len(t):
            continue
        cs, ms = t.cost.values, t.M.values
        cstar, lo_b, hi_b, note = np.nan, np.nan, np.nan, ""
        for i in range(len(cs) - 1):
            if ms[i] <= 0 < ms[i + 1] or (ms[i] == 0 and ms[i + 1] > 0):
                lo_b, hi_b = cs[i], cs[i + 1]
                cstar = cs[i] if ms[i + 1] == ms[i] else cs[i] + (0 - ms[i]) * (cs[i + 1] - cs[i]) / (ms[i + 1] - ms[i])
                note = "M leaves zero between these rungs"
                break
        if np.isnan(cstar):
            note = ("M > 0 at EVERY rung on the ladder (no crossing; W already ahead at 0 bps)"
                    if (ms > 0).all() else
                    "M <= 0 at EVERY rung on the ladder (no crossing; D never falls behind)")
        cross.append(dict(panel=p, gross=g, denom=den, c_star=cstar, bracket_lo=lo_b,
                          bracket_hi=hi_b, M_at_0=ms[0], M_at_10=float(t[t.cost == 10.0].M.iloc[0]),
                          M_max=ms.max(), c_at_Mmax=float(cs[int(np.argmax(ms))]), note=note))
    CR = pd.DataFrame(cross)
    dump(CR, "crossing")
    P("  CROSSING TABLE (all panel x gross x denominator cells):")
    for line in CR.to_string(index=False, float_format=lambda x: f"{x:.4f}").split("\n"):
        P("    " + line)
    P("")

    # ================================================================== (D) resolvability
    P("=" * 100)
    P("(D) RESOLVABILITY — is M(c) bigger than its own sampling width?")
    P("=" * 100)
    P("  TWO RULERS, both printed, neither selected:")
    P("   (i)  NAIVE: independent Wilson intervals at the PUBLISHED denominators (D n, W n).")
    P("   (ii) MECHANISM-CLUSTERED BOOTSTRAP: resample the 6 MECHANISM ARMS with replacement")
    P(f"        ({NBOOT:,} draws, seed {BOOT_SEED}), carrying each arm's WHOLE phase family at")
    P("        BOTH cadences together, which is the level at which the books are distinct.")
    rng = np.random.default_rng(BOOT_SEED)
    res = []
    for p, g, den in product(PANELS, GROSSES, DENOMS):
        base = CEN[(CEN.panel == p) & (CEN.gross == g) & (CEN.cadence.isin(PAIR))]
        if den == "DEN_CANON":
            base = base[base.canonical == 1]
        elif den == "DEN_PHASE":
            base = base[base.canonical == 0]
        if not len(base):
            continue
        draws = rng.integers(0, len(MECHS), size=(NBOOT, len(MECHS)))
        for c in COSTS:
            s = base[base.cost == c]
            byD = {m: s[(s.mech == m) & (s.cadence == "D")].pass4b.values for m in MECHS}
            byW = {m: s[(s.mech == m) & (s.cadence == "W")].pass4b.values for m in MECHS}
            nD = sum(len(byD[m]) for m in MECHS)
            nW = sum(len(byW[m]) for m in MECHS)
            kD = sum(int(byD[m].sum()) for m in MECHS)
            kW = sum(int(byW[m].sum()) for m in MECHS)
            M = kW / nW - kD / nD
            dlo, dhi = wilson(kD, nD)
            wlo, whi = wilson(kW, nW)
            bs = np.empty(NBOOT)
            for b in range(NBOOT):
                ms_ = [MECHS[j] for j in draws[b]]
                bd = np.concatenate([byD[m] for m in ms_])
                bw = np.concatenate([byW[m] for m in ms_])
                bs[b] = bw.mean() - bd.mean()
            blo, bhi = np.percentile(bs, [2.5, 97.5])
            res.append(dict(panel=p, gross=g, denom=den, cost=c, nD=nD, nW=nW, M=M,
                            naive_overlap=bool(dhi >= wlo and whi >= dlo),
                            naive_decisive=bool(dhi < wlo or whi < dlo),
                            D_lo=dlo, D_hi=dhi, W_lo=wlo, W_hi=whi,
                            boot_lo=blo, boot_hi=bhi, boot_sd=float(bs.std(ddof=1)),
                            boot_decisive=bool(blo > 0 or bhi < 0),
                            boot_p_ge0=float((bs <= 0).mean()),
                            M_in_D_books=M * nD))
    RS = pd.DataFrame(res)
    dump(RS, "resolvability")

    for p in PANELS:
        t = RS[(RS.panel == p) & (RS.gross == GROSS_HEAD)]
        P(f"  {p}, gross {GROSS_HEAD} — M(c) with both rulers:")
        show = t[["denom", "cost", "nD", "nW", "M", "M_in_D_books", "naive_decisive",
                  "boot_lo", "boot_hi", "boot_decisive"]]
        for line in show.to_string(index=False,
                                   float_format=lambda x: f"{x:.4f}").split("\n"):
            P("    " + line)
        P("")

    P("  THE RESOLVABLE RANGE — the rungs at which the D-vs-W margin is DECISIVE:")
    ranges = []
    for p, g, den in product(PANELS, GROSSES, DENOMS):
        t = RS[(RS.panel == p) & (RS.gross == g) & (RS.denom == den)].sort_values("cost")
        if not len(t):
            continue
        nd = t[t.naive_decisive].cost.values
        bd = t[t.boot_decisive].cost.values
        ranges.append(dict(panel=p, gross=g, denom=den,
                           naive_decisive_rungs="none" if not len(nd) else
                           "/".join(f"{x:g}" for x in nd),
                           boot_decisive_rungs="none" if not len(bd) else
                           "/".join(f"{x:g}" for x in bd),
                           n_naive=len(nd), n_boot=len(bd), n_rungs=len(t),
                           spans_0_25=bool(len(bd) == 0)))
    RG = pd.DataFrame(ranges)
    dump(RG, "resolvable_range")
    for line in RG.to_string(index=False).split("\n"):
        P("    " + line)
    P("")

    # ---- the queue's own falsifier -------------------------------------------------------
    hi = RS[(RS.panel == "U56") & (RS.gross == GROSS_HEAD) & (RS.denom == DEN_HEAD)]
    in025 = hi[(hi.cost >= 0) & (hi.cost <= 25.0)]
    span = not bool(in025.boot_decisive.any())
    P(f"  QUEUE'S OWN FALSIFIER — 'if the width spans the whole 0-25 bps range, 968's weekly")
    P(f"  headline is a one-book-margin claim': on U56 / gross {GROSS_HEAD} / {DEN_HEAD} the")
    P(f"  mechanism-clustered interval covers 0 at {int((~in025.boot_decisive).sum())} of "
      f"{len(in025)} rungs in [0, 25] bps -> SPANS THE RANGE: {span}")
    P("")

    P("=" * 100)
    P("(D2) WHICH BOOKS ACTUALLY FLIP — the margin's mechanism-level anatomy")
    P("=" * 100)
    P(f"  U56, gross {GROSS_HEAD}, {DEN_HEAD}: 4b pass COUNT per mechanism arm at each rung")
    P("  (D counts out of 2 books per arm, W out of 6; the margin is the difference of the")
    P("   column means, so this table IS the margin, un-aggregated.)")
    an = []
    for m, c in product(MECHS, COSTS):
        row = dict(mech=m, cost=c)
        for cad in PAIR:
            s = sub("U56", GROSS_HEAD, cad, c, DEN_HEAD)
            s = s[s.mech == m]
            row[f"{cad}_pass"] = int(s.pass4b.sum())
            row[f"{cad}_n"] = len(s)
            row[f"{cad}_turn"] = float(s.turn_yr.mean())
            row[f"{cad}_CAGR"] = float(s.CAGR.mean())
            row[f"{cad}_bind"] = "|".join(lg for lg in LEGS if (~s[lg]).any())
        an.append(row)
    AN = pd.DataFrame(an)
    dump(AN, "anatomy")
    for line in AN.to_string(index=False, float_format=lambda x: f"{x:.3f}").split("\n"):
        P("    " + line)
    P("")
    tD = float(AN[AN.cost == 0.0].D_turn.mean())
    tW = float(AN[AN.cost == 0.0].W_turn.mean())
    P(f"  REALISED TURNOVER, U56 gross {GROSS_HEAD}: D {tD:.2f} turns/yr, W {tW:.2f} turns/yr, "
      f"ratio {tD/tW:.2f}x.  A rung c therefore costs D ~{tD*1:.2f}c bp/yr and W ~{tW*1:.2f}c "
      f"bp/yr; the DIFFERENTIAL drag is ~{(tD-tW):.2f}c bp/yr, i.e. "
      f"{(tD-tW)*COST_HEAD:.0f} bp/yr at {COST_HEAD:g} bps.")
    P("  PRE-DECLARED PREDICTION CHECK: a pure cost object is ZERO at 0 bps and grows in c.")
    m0 = float(MG[(MG.panel=='U56')&(MG.gross==GROSS_HEAD)&(MG.denom==DEN_HEAD)&(MG.cost==0.0)].M.iloc[0])
    P(f"    U56 gross {GROSS_HEAD} {DEN_HEAD}: M(0) = {m0:+.4f} -> "
      f"{'CONSISTENT with a pure cost object' if abs(m0) < 1e-12 else 'NOT a pure cost object: the margin is already non-zero at 0 bps'}")
    for p_ in PANELS:
        for g_ in GROSSES:
            mm = MG[(MG.panel==p_)&(MG.gross==g_)&(MG.denom==DEN_HEAD)&(MG.cost==0.0)]
            if len(mm):
                v = float(mm.M.iloc[0])
                P(f"    {p_} gross {g_:.2f} {DEN_HEAD}: M(0) = {v:+.4f}"
                  + ("" if abs(v) < 1e-12 else "   <-- NON-ZERO AT ZERO COST"))
    P("")

    # ================================================================== (E) KEEP paths
    P("=" * 100)
    P("(E) BOTH KEEP PATHS AT EVERY GRID POINT")
    P("=" * 100)
    kp = []
    for p, g, den, c, cad in product(PANELS, GROSSES, DENOMS, COSTS, CADENCES):
        if cad not in PAIR and g != GROSS_HEAD:
            continue
        s = sub(p, g, cad, c, den)
        if not len(s):
            continue
        kp.append(dict(panel=p, gross=g, denom=den, cost=c, cadence=cad, n=len(s),
                       n4a=int(s.pass4a.sum()), n4b=int(s.pass4b.sum()),
                       nBOTH=int((s.pass4a & s.pass4b).sum())))
    KP = pd.DataFrame(kp)
    dump(KP, "keep_paths")
    P(f"  4a TOTAL {int(KP.n4a.sum())} of {int(KP.n.sum())} scored cells; "
      f"4b TOTAL {int(KP.n4b.sum())}; BOTH {int(KP.nBOTH.sum())}.")
    P("  (DEN_FULL / DEN_CANON / DEN_PHASE partition the same books three ways, so these totals")
    P("   double-count by construction; the per-denominator tables below are the honest read.)")
    for den in DENOMS:
        t = KP[(KP.denom == den) & (KP.gross == GROSS_HEAD)]
        P(f"  {den} gross {GROSS_HEAD}: 4a {int(t.n4a.sum())} of {int(t.n.sum())}, "
          f"4b {int(t.n4b.sum())}, BOTH {int(t.nBOTH.sum())}")
    fb = CEN[(CEN.pass4b) & (~CEN.pass4a)]
    P(f"  BINDING 4b LEGS on the {int((~CEN.pass4b).sum()):,} 4b failures (share of failures): "
      + ", ".join(f"{lg} {float((~CEN[~CEN.pass4b][lg]).mean()):.3f}" for lg in LEGS))
    P(f"  4a is {int(CEN.pass4a.sum())} of {len(CEN):,} book-rungs; the DD leg fails on "
      f"{float((~CEN.A_DD).mean()):.3f} of them.")
    P("")

    # ================================================================== (F) rule 8
    P("=" * 100)
    P("(F) RULE 8 — CADENCE CHOSEN ON 2009-2016 ALONE, 2017-2026 READ ONCE")
    P("=" * 100)
    P("  Two IS-only choosers, neither of which reads a row on or after 2017-01-01:")
    P("    C_ISSHARPE  pick the cadence with the highest MEAN IS Sharpe over its population")
    P("    C_ISLEGS    pick the cadence with the most IS 4b legs cleared (IS window only)")
    P("  and, as the zero-parameter comparand, C_FROZEN = W (968's published answer, held fixed).")
    wf = []
    for p, g, den, c in product(PANELS, GROSSES, DENOMS, COSTS):
        cells = {}
        for cad in PAIR:
            s = sub(p, g, cad, c, den)
            if not len(s):
                continue
            isl = np.zeros(len(s))
            isl += (s.IS_Sharpe.values > LIVE[(p, c)]["IS_Sharpe"]).astype(float)
            isl += (np.abs(s.IS_MaxDD.values) <= DD_CAP * abs(PAN[p]["spy"]["IS_MaxDD"])).astype(float)
            isl += (s.IS_CAGR.values >= CAGR_FLOOR * PAN[p]["spy"]["IS_CAGR"]).astype(float)
            cells[cad] = dict(is_sharpe=float(s.IS_Sharpe.mean()), is_legs=float(isl.mean()),
                              oos_cagr=float(s.OOS_CAGR.mean()),
                              oos_sharpe=float(s.OOS_Sharpe.mean()),
                              oos_dd=float(s.OOS_MaxDD.mean()),
                              oos4b=float(((s.OOS_Sharpe.values > PAN[p]["spy"]["OOS_Sharpe"])
                                           & (np.abs(s.OOS_MaxDD.values) <= DD_CAP * abs(PAN[p]["spy"]["OOS_MaxDD"]))
                                           & (s.OOS_CAGR.values >= CAGR_FLOOR * PAN[p]["spy"]["OOS_CAGR"])).mean()))
        if len(cells) < 2:
            continue
        picks = {"C_ISSHARPE": max(cells, key=lambda k: cells[k]["is_sharpe"]),
                 "C_ISLEGS": max(cells, key=lambda k: cells[k]["is_legs"]),
                 "C_FROZEN": "W"}
        for ch, pick in picks.items():
            e = cells[pick]
            wf.append(dict(panel=p, gross=g, denom=den, cost=c, chooser=ch, pick=pick,
                           IS_Sharpe_D=cells["D"]["is_sharpe"], IS_Sharpe_W=cells["W"]["is_sharpe"],
                           IS_margin=cells["W"]["is_sharpe"] - cells["D"]["is_sharpe"],
                           OOS_CAGR=e["oos_cagr"], OOS_Sharpe=e["oos_sharpe"],
                           OOS_MaxDD=e["oos_dd"], OOS_4b_rate=e["oos4b"],
                           LIVE_OOS_Sharpe=LIVE[(p, c)]["OOS_Sharpe"],
                           LIVE_OOS_CAGR=LIVE[(p, c)]["OOS_CAGR"],
                           LIVE_OOS_MaxDD=LIVE[(p, c)]["OOS_MaxDD"],
                           SPY_OOS_Sharpe=PAN[p]["spy"]["OOS_Sharpe"],
                           SPY_OOS_CAGR=PAN[p]["spy"]["OOS_CAGR"],
                           SPY_OOS_MaxDD=PAN[p]["spy"]["OOS_MaxDD"],
                           beats_live=bool(e["oos_sharpe"] > LIVE[(p, c)]["OOS_Sharpe"]),
                           beats_spy_sharpe=bool(e["oos_sharpe"] > PAN[p]["spy"]["OOS_Sharpe"])))
    WF = pd.DataFrame(wf)
    dump(WF, "walkforward")
    P("  PICK AGREEMENT — how often each IS chooser lands on W (968's published answer):")
    for ch in ["C_ISSHARPE", "C_ISLEGS"]:
        t = WF[WF.chooser == ch]
        P(f"    {ch}: picks W at {int((t.pick=='W').sum())} of {len(t)} grid points "
          f"({float((t.pick=='W').mean()):.3f}); mean IS margin (W-D) {float(t.IS_margin.mean()):+.4f}")
    P("  OOS, mean over grid points (2017-2026, read ONCE):")
    for ch in ["C_ISSHARPE", "C_ISLEGS", "C_FROZEN"]:
        t = WF[WF.chooser == ch]
        P(f"    {ch:<11} OOS CAGR {float(t.OOS_CAGR.mean()):.2%}  Sharpe "
          f"{float(t.OOS_Sharpe.mean()):.4f}  MaxDD {float(t.OOS_MaxDD.mean()):.2%}  "
          f"4b-OOS rate {float(t.OOS_4b_rate.mean()):.3f}  beats live {float(t.beats_live.mean()):.3f}  "
          f"beats SPY Sharpe {float(t.beats_spy_sharpe.mean()):.3f}")
    t = WF[WF.chooser == "C_FROZEN"]
    P(f"    COMPARANDS (mean over the same grid): live RULES v2 OOS "
      f"{float(t.LIVE_OOS_CAGR.mean()):.2%} / {float(t.LIVE_OOS_Sharpe.mean()):.4f} / "
      f"{float(t.LIVE_OOS_MaxDD.mean()):.2%};  SPY OOS {float(t.SPY_OOS_CAGR.mean()):.2%} / "
      f"{float(t.SPY_OOS_Sharpe.mean()):.4f} / {float(t.SPY_OOS_MaxDD.mean()):.2%}")
    P("  DOES THE IS CHOOSER AGREE WITH THE OOS TRUTH?  (per grid point, both cadences scored)")
    agree = []
    for p, g, den, c in product(PANELS, GROSSES, DENOMS, COSTS):
        t = WF[(WF.panel == p) & (WF.gross == g) & (WF.denom == den) & (WF.cost == c)]
        if len(t) < 3:
            continue
        sd = sub(p, g, "D", c, den).OOS_Sharpe.mean()
        sw = sub(p, g, "W", c, den).OOS_Sharpe.mean()
        truth = "W" if sw > sd else "D"
        for ch in ["C_ISSHARPE", "C_ISLEGS", "C_FROZEN"]:
            agree.append(dict(chooser=ch, hit=int(t[t.chooser == ch].pick.iloc[0] == truth)))
    AG = pd.DataFrame(agree)
    for ch in ["C_ISSHARPE", "C_ISLEGS", "C_FROZEN"]:
        t = AG[AG.chooser == ch]
        P(f"    {ch:<11} names the OOS-better cadence at {int(t.hit.sum())} of {len(t)} "
          f"grid points ({float(t.hit.mean()):.3f})")
    P("")

    P("=" * 100)
    P("VERDICT")
    P("=" * 100)
    hi_ = RS[(RS.panel == "U56") & (RS.gross == GROSS_HEAD) & (RS.denom == DEN_HEAD)
             & (RS.cost == COST_HEAD)].iloc[0]
    P(f"  U56 / gross {GROSS_HEAD} / {DEN_HEAD} / {COST_HEAD:g} bps: M = {hi_.M:+.4f} "
      f"({hi_.M_in_D_books:+.2f} D-books of {int(hi_.nD)}); naive Wilson decisive "
      f"{bool(hi_.naive_decisive)}; mechanism-clustered 95% CI "
      f"[{hi_.boot_lo:+.4f}, {hi_.boot_hi:+.4f}] decisive {bool(hi_.boot_decisive)}")
    P(f"  runtime {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"wrote {OUT.name}.console.txt")


if __name__ == "__main__":
    main()

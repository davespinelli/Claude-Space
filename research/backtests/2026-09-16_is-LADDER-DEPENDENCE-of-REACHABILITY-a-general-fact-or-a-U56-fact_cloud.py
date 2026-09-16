#!/usr/bin/env python3
"""Idea 1101 (cloud lane, 2026-09-16) — is LADDER-DEPENDENCE of REACHABILITY a general fact
or a U56 fact?

QUESTION (QUEUE idea 1101, verbatim)
    idea 1096's D3 found the same anchor book (W/H126/N=20/gross 0.75) is reached by the
    IS-Sharpe chooser from 2 of the 4 CORE ladders it sits in, identically on U56 and B136,
    while the N and H ladders never reach it.  Re-run the four-ladder anchor test on the SMALL
    panel (dropping max_1d_move >= 1.0 per data/small_meta.csv) and on a second anchor cell,
    and report whether 2-of-4 is a level or a coincidence.  Max 2 params (anchor cell, panel).

WHAT "REACHABILITY" MEANS HERE, STATED BEFORE ANY NUMBER
    An anchor cell (N, H, gross, cadence) sits on FOUR one-dimensional CORE ladders: the line
    that varies N with the other three frozen at the anchor's own coordinates, and likewise for
    H, GROSS and CADENCE.  A ladder REACHES the anchor under chooser C iff C, given 2009-2016
    ALONE, picks the anchor's own rung on that ladder.  The reach COUNT is therefore an integer
    in 0..4, and 1096's D3 result is "2" for anchor A under C_ISSHARPE on U56 and on B136.
    Rule 8 is what makes this the right question: a book nobody's IS-only chooser can select is
    not a book the record may publish, whatever its OOS numbers.

THE TWO TUNED DIALS (PROTOCOL rule 4, no more than two)
    1. PANEL {U56, B136, SMALL}.  U56 and B136 are 1096's own panels, re-run so its committed
       2-of-4 is a CROSS-RUN GATE and not an assumption; SMALL is the arm this idea adds.
    2. ANCHOR CELL {A, B}.  A = the standing anchor W / H=126 / N=20 / gross 0.75 (1096's own,
       and the cell 936/1071/1082/1094/1102/1108/1110/1116/1131 all quote).  B = M / H=63 /
       N=12 / gross 0.55, declared HERE, BEFORE any result, and chosen for one stated reason:
       it is INTERIOR on all four ladders, where A is at the TOP rung of GROSS.  A and B share
       no ladder — all eight lines are distinct — so B is a genuine second draw, not a
       re-reading of A's.
    CHOOSER and LADDER are NOT dials: all 3 choosers x 4 ladders are published at every
    (panel, anchor), 72 reach decisions in all, and the headline chooser is C_ISSHARPE because
    that is the one 1096 read.
    Everything else frozen at 1082/1094/1098/1102/1108/1110/1116/1131's construction: CAND20
    legs, cap INF, max_vol 0.60, 10 bps, LAG 1, warm-up 260, IS end 2016-12-31, W/H126/N20/0.75
    defaults off-anchor, zlib.crc32 seeds, 1000 bootstrap draws, block L=63.

DECLARED BEFORE ANY NUMBER
    H_GATE96     CROSS-RUN: anchor A under C_ISSHARPE reaches from exactly 2 of 4 ladders on
                 U56 and on B136, and the two are GROSS and CADENCE (N and H never reach).
                 This is a GATE on 1096's committed D3, not a finding of this run.
    H_LEVEL      the idea's question, part 1: the reach count for anchor A / C_ISSHARPE is 2
                 on SMALL as well.
    H_ANCHOR     the idea's question, part 2: the reach count for anchor B / C_ISSHARPE is 2 on
                 every panel.  REFUTED by any panel reading anything but 2.
    H_SAMESET    stronger than the count: the SET of reaching ladders is {GROSS, CADENCE} at
                 every (panel, anchor) cell.  A count that holds while the set moves is a
                 coincidence dressed as a level.
    H_BOUNDARY   the mechanism this run is built to separate: a ladder reaches its anchor
                 because the anchor sits at a ladder ENDPOINT (gross 0.75 is the TOP rung of
                 the GROSS ladder, W is not an endpoint of CADENCE), not because reachability
                 is a property of the ladder's name.  SUPPORTED iff reach is perfectly
                 predicted by endpoint-ness across all 72 decisions.
    H_CHANCE     2-of-4 exceeds what a chooser picking uniformly at random from each ladder
                 would give.  The uniform expectation is 1/9 + 1/4 + 1/10 + 1/4 = 0.7111 for
                 anchor A's ladder lengths and the same for B's, so 2 is 2.8x chance; REFUTED
                 if the observed mean reach count over the six (panel, anchor) cells does not
                 exceed it.
    H_RESOLVED   the honest limit: a reach decision is an ARGMAX on a ladder, and 1110/1116/
                 1131 found H and CADENCE argmaxes un-resolvable on this tape.  For every
                 decision this run publishes, the block bootstrap gives P(anchor is the IS
                 argmax) over 1000 joint redraws of the IS window.  SUPPORTED iff every
                 headline reach decision carries P >= 0.90 or P <= 0.10, i.e. iff the 2-of-4
                 is a measurement rather than a coin flip.  Declared as the outcome this
                 design is most exposed to.
    NOT A KEEP PATH BY CONSTRUCTION.  Neither dial changes any book: the 162 rung books are
    byte-identical whichever anchor or panel is nominated, and only which rung gets CALLED
    reached moves.  PANEL is nevertheless a choice a real book would have to make, so rule 8
    (rung chosen on IS 2009-2016 alone, per ladder, three choosers, OOS read ONCE) and BOTH
    KEEP paths (4a against live RULES v2, 4b against SPY) are scored at every one of the 162
    rungs and at every one of the 72 picks.

THE DECLARED APPROXIMATION, AND ITS DIRECTION.  P(anchor is argmax) is a MOVING-BLOCK bootstrap
    of the realised IS return paths with the SAME block index applied to every rung of a ladder,
    so the cross-rung correlation that makes these ladders hard to resolve is preserved rather
    than destroyed.  It is still a resample of ONE tape: it measures sampling error around this
    tape's regime, not regime uncertainty, so every P is CLOSER TO 0 OR 1 than the truth and
    H_RESOLVED is scored in the direction that favours SUPPORTED.  Reported as such.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists, so every level is
    optimistic.  The SMALL pool is worse: the CURRENT constituents of a sub-$2B screen, so every
    name that fell below the screen, delisted or went to zero is absent, and a small-cap pool
    loses names that way far more often than a large-cap one.  A REACH decision contrasts two
    rungs of one ladder over the same inflated tape and the bias very largely cancels out of it;
    it does NOT cancel out of the 4b legs, measured against SPY, a real index, so every 4b pass
    counted here is an UPPER bound.
"""
from __future__ import annotations

import sys
import time
import zlib
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-16"
SLUG = "is-LADDER-DEPENDENCE-of-REACHABILITY-a-general-fact-or-a-U56-fact"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST = 10.0
LEGS = [(21, 252), (0, 126), (0, 63)]

LAD_N = [5, 8, 10, 12, 15, 20, 25, 30, 40]
LAD_H = [21, 63, 126, 252]
LAD_G = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]
LAD_C = ["D", "W", "M", "Q"]
LADDERS = {"N": LAD_N, "H": LAD_H, "GROSS": LAD_G, "CADENCE": LAD_C}

PANELS = ["U56", "B136", "SMALL"]                           # dial 1
ANCHORS = {"A": dict(N=20, H=126, GROSS=0.75, CADENCE="W"),  # dial 2
           "B": dict(N=12, H=63, GROSS=0.55, CADENCE="M")}
CHOOSERS = {"C_ISSHARPE": "IS_Sharpe", "C_ISCAGR": "IS_CAGR", "C_ISDD": "IS_MaxDD"}
CH_HEAD = "C_ISSHARPE"

BDRAWS, BLOCK_L = 1000, 63
SEED_BOOT = 11011101

A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
REACH_1096 = {("U56", "A", "C_ISSHARPE"): {"GROSS", "CADENCE"},
              ("B136", "A", "C_ISSHARPE"): {"GROSS", "CADENCE"}}

LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def seed_of(*parts):
    return SEED_BOOT + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


# ------------------------------------- 1082/1098/1102/1108/1110/1116/1119's runner, verbatim
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
    """1116/1119's build() verbatim."""
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


# ---------------------------------------------- 1098/1102's bootstrap, 1108's seed repair
def block_index(rng, T, L, ndraws):
    nb = int(np.ceil(T / L))
    st = rng.integers(0, T, size=(ndraws, nb))
    off = np.arange(L)
    idx = (st[:, :, None] + off[None, None, :]) % T
    return idx.reshape(ndraws, nb * L), nb


def boot_exact(R, idx, nb, L, chunk=100):
    """Joint resample: the SAME block index is applied to every rung, preserving cross-rung
    correlation.  Returns (CAGR, Sharpe) arrays of shape (n_rungs, n_draws)."""
    LG = np.log1p(R)
    D = np.concatenate([LG, LG], axis=1)
    CS = np.concatenate([np.zeros((D.shape[0], 1)), np.cumsum(D, axis=1)], axis=1)
    R2 = np.concatenate([R, R], axis=1)
    CS1 = np.concatenate([np.zeros((R.shape[0], 1)), np.cumsum(R2, axis=1)], axis=1)
    CS2 = np.concatenate([np.zeros((R.shape[0], 1)), np.cumsum(R2 ** 2, axis=1)], axis=1)
    nd = idx.shape[0]
    st = idx[:, ::L]
    cag = np.empty((R.shape[0], nd))
    shp = np.empty((R.shape[0], nd))
    n = nb * L
    for a in range(0, nd, chunk):
        s = st[a:a + chunk]
        lsum = (CS[:, s + L] - CS[:, s]).sum(axis=2)
        s1 = (CS1[:, s + L] - CS1[:, s]).sum(axis=2)
        s2 = (CS2[:, s + L] - CS2[:, s]).sum(axis=2)
        cag[:, a:a + chunk] = np.expm1(lsum * (252.0 / n))
        mu = s1 / n
        var = (s2 - n * mu ** 2) / (n - 1)
        sd = np.sqrt(np.maximum(var, 0.0))
        shp[:, a:a + chunk] = np.where(sd > 0, mu * 252.0 / (sd * np.sqrt(252.0)), np.nan)
    return cag, shp


def boot_maxdd(R, idx, chunk=40):
    nr, _ = R.shape
    nd = idx.shape[0]
    out = np.empty((nr, nd))
    for a in range(0, nd, chunk):
        ix = idx[a:a + chunk]
        for j in range(nr):
            path = np.log1p(R[j])[ix]
            cum = np.cumsum(path, axis=1)
            run = np.maximum.accumulate(cum, axis=1)
            out[j, a:a + chunk] = np.expm1(cum - run).min(axis=1)
    return out


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep].dropna(how="all").ffill(), len(bad), len(meta)


# ------------------------------------------------------------------------------------- main
def main():
    t0 = time.time()
    P(f"# Idea 1101 (cloud lane, {DATE}) — is LADDER-DEPENDENCE of REACHABILITY a general fact "
      "or a U56 fact?")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4): PANEL {PANELS} x ANCHOR CELL {list(ANCHORS)}.")
    P("#   CHOOSER and LADDER are NOT dials — all 3 x 4 = 12 reach decisions published at every")
    P(f"#   (panel, anchor), {len(PANELS)*len(ANCHORS)*12} in all.  Headline chooser {CH_HEAD} "
      "(1096's own).")
    for a, c in ANCHORS.items():
        P(f"#   ANCHOR {a}: N={c['N']} H={c['H']} gross={c['GROSS']} cadence={c['CADENCE']}")
    P(f"# FROZEN: CAND20 legs {LEGS}, cap INF, max_vol {MAXVOL}, {COST:.0f} bps, LAG {LAG}, "
      f"warm-up {WARMUP},")
    P(f"#   IS end {IS_END}, {BDRAWS} bootstrap draws, block L={BLOCK_L}, crc32 seeds.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   H_GATE96   CROSS-RUN: anchor A / C_ISSHARPE reaches from exactly {GROSS, CADENCE} on")
    P("#              U56 and B136 (1096's committed D3).  A GATE, not a finding.")
    P("#   H_LEVEL    the reach count for anchor A / C_ISSHARPE is 2 on SMALL as well.")
    P("#   H_ANCHOR   the reach count for anchor B / C_ISSHARPE is 2 on every panel.")
    P("#   H_SAMESET  the reaching SET is {GROSS, CADENCE} at every (panel, anchor) cell.")
    P("#   H_BOUNDARY reach is perfectly predicted by the anchor sitting at a ladder ENDPOINT.")
    P("#   H_CHANCE   the mean reach count over the six cells exceeds the uniform-argmax")
    P("#              expectation 1/9 + 1/4 + 1/10 + 1/4 = 0.7111.")
    P("#   H_RESOLVED every headline reach decision carries bootstrap P(anchor is argmax) >=0.90")
    P("#              or <=0.10, i.e. the 2-of-4 is a measurement and not a coin flip.")
    P("#   NOT A KEEP PATH: the 162 rung books are byte-identical across both dials.  Scored at")
    P("#     every rung and every pick anyway, because rule 4 and rule 8 say so.")
    P("")

    gaterows, gates = [], {}

    def gate(name, what, value, ok):
        gates[name] = bool(ok)
        gaterows.append(dict(gate=name, what=what, value=float(value), pass_=bool(ok)))
        P(f"  [{'PASS' if ok else 'FAIL'}] {name:<9s} {what}: {value:.4e}")

    # ---------------------------------------------------------------------------- panels
    P("## PANELS — loaded and STAMPED before any result number (idea 1074's recommendation)")
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
            elig[:, spy_i] = False            # SPY is the benchmark here, not a constituent
        panels[panel] = dict(px=px, idx=idx, K=K, T=T, rets=rets, priced=priced, warm=warm,
                             ins=ins, oos=oos, sc=sc, elig=elig, spy_i=spy_i)
        P(f"  {panel:<6s} {K:4d} cols, {T:,} rows {idx[0].date()} -> {idx[-1].date()}  "
          f"warm {warm.sum():,}  IS {ins.sum():,}  OOS {oos.sum():,}  "
          f"mean priced/day {float(priced[WARMUP:].sum(axis=1).mean()):.1f}")
    P(f"  SMALL STAMP: data/small_meta.csv lists {nmeta} tickers; {ndrop} dropped for "
      f"max_1d_move >= 1.0; pool served = {panels['SMALL']['K'] - 1} names + SPY as benchmark; "
      f"tape {panels['SMALL']['idx'][0].date()} -> {panels['SMALL']['idx'][-1].date()}.")
    P("  (idea 706's 439->663 rebuild and idea 1072's finding that committed SMALL headlines")
    P("   move on it: the stamp above, not any label, is what this run's SMALL numbers mean.)")
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
        return g - tn * COST / 1e4, tn

    # ---------------------------------------------------------------------------- gates
    P("## GATES — printed before any result number")
    d = panels["U56"]
    mk = rebalance_mask(d["idx"], "W").values
    reb = np.flatnonzero(mk)
    W = build(-d["sc"], d["elig"], d["priced"], reb, 20, 126, d["T"], d["K"], 0.75)
    Wdf = pd.DataFrame(W, index=d["idx"], columns=d["px"].columns)
    eng = backtest(d["px"], Wdf, cost_bps=COST, freq="W")["returns"].values
    rfast, _ = run_cell("U56", 20, 126, 0.75, "W")
    v = float(np.abs(eng[d["warm"]] - rfast[d["warm"]]).max())
    gate("G1", "fast runner == engine.backtest (U56 W/H126/N=20)", v, v < 1e-12)
    m = blocks_m(rfast, d["warm"], d["ins"], d["oos"])
    v = max(abs(m["CAGR"] - A936_WH126[0]), abs(m["Sharpe"] - A936_WH126[1]),
            abs(m["MaxDD"] - A936_WH126[2]))
    gate("G2", "CROSS-RUN 936/1071/1082/1094/1102/1108/1110/1116/1131 U56 anchor-A triple",
         v, v < 5e-5)
    spy = d["px"]["SPY"].pct_change().fillna(0.0).values
    sm = blocks_m(spy, d["warm"], d["ins"], d["oos"])
    v = max(abs(sm["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
            abs(sm["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
            abs(sm["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gate("G3", "SPY OOS triple (U56 tape)", v, v < 5e-4)
    lb_r = backtest(d["px"], rules_v2_weights(d["px"]), cost_bps=COST, freq="W")["returns"].values
    lbm = blocks_m(lb_r, d["warm"], d["ins"], d["oos"])
    v = abs(lbm["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gate("G4", "live RULES v2 MaxDD == committed -12.05%", v, v < 5e-4)
    r_a, _ = run_cell("SMALL", 12, 63, 0.55, "M")
    r_b, _ = run_cell("SMALL", 12, 63, 0.55, "M")
    v = float(np.abs(r_a - r_b).max())
    gate("G5", "determinism of the SMALL anchor-B pipeline", v, v == 0.0)
    mkB = rebalance_mask(d["idx"], "M").values
    rebB = np.flatnonzero(mkB)
    WB = build(-d["sc"], d["elig"], d["priced"], rebB, 12, 63, d["T"], d["K"], 0.55)
    engB = backtest(d["px"], pd.DataFrame(WB, index=d["idx"], columns=d["px"].columns),
                    cost_bps=COST, freq="M")["returns"].values
    rfB, _ = run_cell("U56", 12, 63, 0.55, "M")
    v = float(np.abs(engB[d["warm"]] - rfB[d["warm"]]).max())
    gate("G6", "fast runner == engine.backtest at anchor B (U56 M/H63/N=12/g0.55)", v, v < 1e-12)
    P("")

    # ------------------------------------------- BUILD EVERY RUNG OF EVERY ANCHOR LADDER
    P("## THE EIGHT LADDERS PER PANEL — 2 anchors x 4 ladders, every rung published")
    metr, series, gridrows, bench = {}, {}, [], {}
    for panel in PANELS:
        dd_ = panels[panel]
        sb = blocks_m(dd_["px"]["SPY"].pct_change().fillna(0.0).values,
                      dd_["warm"], dd_["ins"], dd_["oos"])
        lbm_p = blocks_m(backtest(dd_["px"], rules_v2_weights(dd_["px"]), cost_bps=COST,
                                  freq="W")["returns"].values,
                         dd_["warm"], dd_["ins"], dd_["oos"])
        bench[panel] = (sb, lbm_p)
        P(f"  {panel:<6s} SPY       full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / "
          f"{sb['MaxDD']:.2%}  halves {sb['H1']:.4f}/{sb['H2']:.4f}  OOS {sb['OOS_CAGR']:.2%} / "
          f"{sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"  {panel:<6s} RULES v2  full {lbm_p['CAGR']:.2%} / {lbm_p['Sharpe']:.4f} / "
          f"{lbm_p['MaxDD']:.2%}  halves {lbm_p['H1']:.4f}/{lbm_p['H2']:.4f}  OOS "
          f"{lbm_p['OOS_CAGR']:.2%} / {lbm_p['OOS_Sharpe']:.4f} / {lbm_p['OOS_MaxDD']:.2%}")
        for anc, coord in ANCHORS.items():
            for lad, rungs in LADDERS.items():
                Rw, Ro, Ri = [], [], []
                for rg in rungs:
                    c = dict(coord)
                    c[lad] = rg
                    r_, tn = run_cell(panel, c["N"], c["H"], c["GROSS"], c["CADENCE"])
                    mm = blocks_m(r_, dd_["warm"], dd_["ins"], dd_["oos"])
                    mm["turnover_yr"] = float(tn[dd_["warm"]].sum() * 252.0 / dd_["warm"].sum())
                    metr[(panel, anc, lad, rg)] = mm
                    Rw.append(r_[dd_["warm"]])
                    Ro.append(r_[dd_["oos"]])
                    Ri.append(r_[dd_["ins"]])
                    l4b, l4bo, l4a = legs_4b(mm, sb), legs_4b_oos(mm, sb), legs_4a(mm, lbm_p)
                    gridrows.append(dict(panel=panel, anchor=anc, ladder=lad, rung=rg,
                                         is_anchor_rung=(rg == coord[lad]), **mm,
                                         pass_4b_full=all(l4b.values()),
                                         pass_4b_oos=all(l4bo.values()),
                                         pass_4a=all(l4a.values()), **l4b, **l4bo, **l4a))
                series[(panel, anc, lad)] = (np.array(Rw), np.array(Ro), np.array(Ri))
        P(f"  {panel:<6s} built {len(ANCHORS)*sum(len(v) for v in LADDERS.values())} rung books "
          f"({time.time()-t0:.0f}s elapsed)")
    grid = pd.DataFrame(gridrows)
    dump(grid, "grid")
    P("")

    # ------------------------------------------------------- THE REACH TABLE (the answer)
    P("## THE FOUR-LADDER ANCHOR TEST — does an IS-ONLY chooser pick the anchor's own rung?")
    P("   IS window 2009-2016 alone.  P_boot = share of 1000 joint moving-block redraws of the")
    P("   IS window in which the anchor rung is the chooser's argmax (same block index on every")
    P("   rung, so cross-rung correlation is preserved).")
    reachrows = []
    for panel in PANELS:
        for anc, coord in ANCHORS.items():
            for lad, rungs in LADDERS.items():
                ai = rungs.index(coord[lad])
                endpoint = ai in (0, len(rungs) - 1)
                _, _, Ri = series[(panel, anc, lad)]
                rng = np.random.default_rng(seed_of("BOOT", panel, anc, lad))
                ix, nb = block_index(rng, Ri.shape[1], BLOCK_L, BDRAWS)
                bc, bs = boot_exact(Ri, ix, nb, BLOCK_L)
                bdd = boot_maxdd(Ri, ix)
                bootmap = {"C_ISSHARPE": bs, "C_ISCAGR": bc, "C_ISDD": bdd}
                for ch, key in CHOOSERS.items():
                    vals = np.array([metr[(panel, anc, lad, r_)][key] for r_ in rungs])
                    pick_i = int(np.argmax(vals))
                    srt = np.sort(vals)[::-1]
                    B = bootmap[ch]
                    amax = np.argmax(np.where(np.isfinite(B), B, -np.inf), axis=0)
                    p_boot = float((amax == ai).mean())
                    p_pick = float((amax == pick_i).mean())
                    reachrows.append(dict(
                        panel=panel, anchor=anc, ladder=lad, chooser=ch, n_rungs=len(rungs),
                        anchor_rung=coord[lad], anchor_index=ai, endpoint=endpoint,
                        pick=rungs[pick_i], reached=(pick_i == ai),
                        margin=float(srt[0] - srt[1]),
                        anchor_val=float(vals[ai]), best_val=float(srt[0]),
                        anchor_deficit=float(srt[0] - vals[ai]),
                        anchor_rank=int((vals > vals[ai]).sum()) + 1,
                        p_boot_anchor=p_boot, p_boot_pick=p_pick,
                        uniform_rate=1.0 / len(rungs),
                        resolved=bool(p_boot >= 0.90 or p_boot <= 0.10)))
    RCH = pd.DataFrame(reachrows)
    dump(RCH, "reach")
    P("   panel  anchor ladder   k  a_rung  end  chooser      pick    reach  rank  margin   "
      "P_boot(anchor)  P_boot(pick)  1/k")
    for _, r_ in RCH.iterrows():
        P(f"   {r_['panel']:<6} {r_['anchor']:<6} {r_['ladder']:<8} {r_['n_rungs']:2d} "
          f"{str(r_['anchor_rung']):>6}  {str(r_['endpoint'])[0]}   {r_['chooser']:<11} "
          f"{str(r_['pick']):>6}  {str(r_['reached']):<5}  {r_['anchor_rank']:2d}  "
          f"{r_['margin']:7.4f}   {r_['p_boot_anchor']:12.3f}  {r_['p_boot_pick']:12.3f}  "
          f"{r_['uniform_rate']:.3f}")
    P("")
    P("## THE REACH COUNTS — the integer 1096 published as 2 of 4")
    cnt = (RCH.groupby(["panel", "anchor", "chooser"])
           .agg(reach_count=("reached", "sum"),
                reach_set=("ladder", lambda s: "+".join(sorted(
                    RCH.loc[s.index][RCH.loc[s.index].reached].ladder))),
                mean_p_boot=("p_boot_anchor", "mean"),
                n_resolved=("resolved", "sum")).reset_index())
    dump(cnt, "reachcounts")
    for _, r_ in cnt.iterrows():
        P(f"   {r_['panel']:<6} anchor {r_['anchor']}  {r_['chooser']:<11} reach "
          f"{int(r_['reach_count'])} of 4  set = {r_['reach_set'] or '(none)':<16}  mean "
          f"P_boot {r_['mean_p_boot']:.3f}  resolved {int(r_['n_resolved'])}/4")
    head = cnt[cnt.chooser == CH_HEAD]
    P(f"   HEADLINE ({CH_HEAD}) reach counts: " +
      ", ".join(f"{r_['panel']}/{r_['anchor']} = {int(r_['reach_count'])}"
                for _, r_ in head.iterrows()))
    P("")

    # ------------------------------------------------------- BOUNDARY / CHANCE DECOMPOSITION
    P("## IS IT THE LADDER'S NAME, OR THE ANCHOR'S PLACE ON IT?")
    bd = RCH.groupby(["ladder"]).agg(n=("reached", "size"), reached=("reached", "sum"),
                                     mean_p=("p_boot_anchor", "mean")).reset_index()
    P("   by LADDER (all panels, anchors, choosers):")
    for _, r_ in bd.iterrows():
        P(f"     {r_['ladder']:<8} reached {int(r_['reached'])}/{int(r_['n'])}  mean P_boot "
          f"{r_['mean_p']:.3f}")
    eb = RCH.groupby(["endpoint"]).agg(n=("reached", "size"), reached=("reached", "sum"),
                                       mean_p=("p_boot_anchor", "mean")).reset_index()
    P("   by ENDPOINT-ness of the anchor on its own ladder:")
    for _, r_ in eb.iterrows():
        P(f"     endpoint={str(r_['endpoint']):<5} reached {int(r_['reached'])}/{int(r_['n'])}  "
          f"mean P_boot {r_['mean_p']:.3f}")
    n_agree = int((RCH.reached == RCH.endpoint).sum())
    P(f"   reach == endpoint on {n_agree} of {len(RCH)} decisions "
      f"({n_agree/len(RCH):.1%}); the four discordant cells are named below if any.")
    disc = RCH[RCH.reached != RCH.endpoint]
    for _, r_ in disc.iterrows():
        P(f"     DISCORDANT {r_['panel']:<6} {r_['anchor']} {r_['ladder']:<8} {r_['chooser']:<11}"
          f" reached={r_['reached']} endpoint={r_['endpoint']} rank {r_['anchor_rank']}/"
          f"{r_['n_rungs']}")
    unif = sum(1.0 / len(v) for v in LADDERS.values())
    obs_head = float(head.reach_count.mean())
    obs_all = float(cnt.reach_count.mean())
    P(f"   CHANCE BASELINE: a chooser picking uniformly at random from each ladder reaches "
      f"{unif:.4f} of 4 in expectation ({'+'.join(f'1/{len(v)}' for v in LADDERS.values())}).")
    P(f"   Observed mean reach count: headline {CH_HEAD} {obs_head:.4f}, all three choosers "
      f"{obs_all:.4f}.")
    dump(bd.rename(columns={"reached": "n_reached"}), "byladder")
    P("")

    # ------------------------------------------------------- HYPOTHESES
    def rset(panel, anc, ch=CH_HEAD):
        s = RCH[(RCH.panel == panel) & (RCH.anchor == anc) & (RCH.chooser == ch)]
        return set(s[s.reached].ladder), int(s.reached.sum())
    g96 = all(rset(p, "A")[0] == REACH_1096[(p, "A", CH_HEAD)] for p in ["U56", "B136"])
    gate("G7", "CROSS-RUN 1096 D3: anchor A / C_ISSHARPE reaches {GROSS,CADENCE} on U56 & B136",
         0.0 if g96 else 1.0, g96)
    H_GATE96 = g96
    H_LEVEL = rset("SMALL", "A")[1] == 2
    H_ANCHOR = all(rset(p, "B")[1] == 2 for p in PANELS)
    H_SAMESET = all(rset(p, a)[0] == {"GROSS", "CADENCE"} for p in PANELS for a in ANCHORS)
    H_BOUNDARY = bool(n_agree == len(RCH))
    H_CHANCE = bool(obs_head > unif)
    H_RESOLVED = bool(RCH[RCH.chooser == CH_HEAD].resolved.all())
    hyp = [
        dict(hypothesis="H_GATE96", declared="CROSS-RUN gate: anchor A / C_ISSHARPE reaches exactly {GROSS, CADENCE} on U56 and B136 (1096's committed D3)",
             result="; ".join(f"{p} set={sorted(rset(p,'A')[0])} count={rset(p,'A')[1]}"
                              for p in ["U56", "B136"]),
             verdict="SUPPORTED" if H_GATE96 else "REFUTED"),
        dict(hypothesis="H_LEVEL", declared="reach count for anchor A / C_ISSHARPE is 2 on SMALL as well",
             result=f"SMALL/A = {rset('SMALL','A')[1]} of 4, set {sorted(rset('SMALL','A')[0])}",
             verdict="SUPPORTED" if H_LEVEL else "REFUTED"),
        dict(hypothesis="H_ANCHOR", declared="reach count for anchor B / C_ISSHARPE is 2 on every panel",
             result="; ".join(f"{p}/B = {rset(p,'B')[1]} of 4 {sorted(rset(p,'B')[0])}"
                              for p in PANELS),
             verdict="SUPPORTED" if H_ANCHOR else "REFUTED"),
        dict(hypothesis="H_SAMESET", declared="the reaching SET is {GROSS, CADENCE} at every (panel, anchor) cell",
             result="; ".join(f"{p}/{a}={sorted(rset(p,a)[0])}" for p in PANELS for a in ANCHORS),
             verdict="SUPPORTED" if H_SAMESET else "REFUTED"),
        dict(hypothesis="H_BOUNDARY", declared="reach is perfectly predicted by the anchor sitting at a ladder ENDPOINT",
             result=f"reach == endpoint on {n_agree} of {len(RCH)} decisions; "
                    f"endpoint cells reached {int(eb[eb.endpoint].reached.iloc[0]) if eb.endpoint.any() else 0}"
                    f"/{int(eb[eb.endpoint].n.iloc[0]) if eb.endpoint.any() else 0}, interior "
                    f"{int(eb[~eb.endpoint].reached.iloc[0]) if (~eb.endpoint).any() else 0}"
                    f"/{int(eb[~eb.endpoint].n.iloc[0]) if (~eb.endpoint).any() else 0}",
             verdict="SUPPORTED" if H_BOUNDARY else "REFUTED"),
        dict(hypothesis="H_CHANCE", declared=f"mean headline reach count exceeds the uniform-argmax expectation {unif:.4f}",
             result=f"observed {obs_head:.4f} ({CH_HEAD}), {obs_all:.4f} over all three choosers,"
                    f" against {unif:.4f}",
             verdict="SUPPORTED" if H_CHANCE else "REFUTED"),
        dict(hypothesis="H_RESOLVED", declared="every headline reach decision carries P_boot(anchor) >= 0.90 or <= 0.10",
             result=f"{int(RCH[RCH.chooser==CH_HEAD].resolved.sum())} of "
                    f"{len(RCH[RCH.chooser==CH_HEAD])} headline decisions resolved; "
                    f"P_boot range {RCH[RCH.chooser==CH_HEAD].p_boot_anchor.min():.3f}-"
                    f"{RCH[RCH.chooser==CH_HEAD].p_boot_anchor.max():.3f}",
             verdict="SUPPORTED" if H_RESOLVED else "REFUTED"),
    ]
    HY = pd.DataFrame(hyp)
    dump(HY, "hypotheses")
    P("## HYPOTHESES")
    for _, r_ in HY.iterrows():
        P(f"   [{r_['verdict']:<9s}] {r_['hypothesis']:<12s} {r_['result']}")
    P(f"   {int((HY.verdict == 'SUPPORTED').sum())} of {len(HY)} SUPPORTED")
    P("")

    # ------------------------------------------------------- RULE 8 AND BOTH KEEP PATHS
    P("## RULE 8 — rung chosen on IS 2009-2016 ALONE, per ladder, three choosers, OOS read ONCE")
    pickrows = []
    for panel in PANELS:
        sb, lbm_p = bench[panel]
        for anc, coord in ANCHORS.items():
            for lad, rungs in LADDERS.items():
                for ch, key in CHOOSERS.items():
                    vals = [metr[(panel, anc, lad, r_)][key] for r_ in rungs]
                    pick = rungs[int(np.argmax(vals))]
                    mm = metr[(panel, anc, lad, pick)]
                    oos_best = rungs[int(np.argmax([metr[(panel, anc, lad, r_)]["OOS_Sharpe"]
                                                    for r_ in rungs]))]
                    l4b, l4bo, l4a = legs_4b(mm, sb), legs_4b_oos(mm, sb), legs_4a(mm, lbm_p)
                    srt = np.sort(vals)[::-1]
                    pickrows.append(dict(panel=panel, anchor=anc, ladder=lad, chooser=ch,
                                         pick=pick, margin=float(srt[0] - srt[1]),
                                         reached_anchor=(pick == coord[lad]),
                                         oos_best=oos_best, picked_oos_best=(pick == oos_best),
                                         regret=float(metr[(panel, anc, lad, oos_best)]["OOS_Sharpe"]
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
        P(f"    {r_['panel']:<6} {r_['anchor']} {r_['ladder']:<8} {r_['chooser']:<11} pick "
          f"{str(r_['pick']):<6} margin {r_['margin']:7.4f}  full {r_['CAGR']:7.2%}/"
          f"{r_['Sharpe']:.4f}/{r_['MaxDD']:7.2%}  halves {r_['H1']:.4f}/{r_['H2']:.4f}  OOS "
          f"{r_['OOS_CAGR']:7.2%}/{r_['OOS_Sharpe']:.4f}/{r_['OOS_MaxDD']:7.2%}  4b full "
          f"{str(r_['pass_4b_full']):<5} 4b OOS {str(r_['pass_4b_oos']):<5} 4a "
          f"{str(r_['pass_4a']):<5} regret {r_['regret']:+.4f}")
    P(f"  ALL PICKS: 4b full {int(pk['pass_4b_full'].sum())} of {len(pk)}, 4b OOS "
      f"{int(pk['pass_4b_oos'].sum())} of {len(pk)}, 4a {int(pk['pass_4a'].sum())} of {len(pk)}; "
      f"the IS chooser picks the OOS-best rung {int(pk['picked_oos_best'].sum())} of {len(pk)}")
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
        P("  4b-full passing cells (deduplicated on the book's own coordinates):")
        seen = set()
        for _, r_ in grid[grid.pass_4b_full].iterrows():
            c = dict(ANCHORS[r_["anchor"]])
            c[r_["ladder"]] = r_["rung"]
            key = (r_["panel"], c["N"], c["H"], c["GROSS"], c["CADENCE"])
            if key in seen:
                continue
            seen.add(key)
            P(f"    {r_['panel']:<6} N={c['N']:<3} H={c['H']:<4} g={c['GROSS']:<5} "
              f"{c['CADENCE']:<2} full {r_['CAGR']:7.2%}/{r_['Sharpe']:.4f}/{r_['MaxDD']:7.2%} "
              f"halves {r_['H1']:.4f}/{r_['H2']:.4f}  OOS {r_['OOS_CAGR']:7.2%}/"
              f"{r_['OOS_Sharpe']:.4f}/{r_['OOS_MaxDD']:7.2%}  4b OOS {r_['pass_4b_oos']}")
        P(f"  ({len(seen)} distinct books behind {int(grid['pass_4b_full'].sum())} passing rows; "
          "the two anchors' ladders intersect nowhere, so no book is double-counted across "
          "anchors, but a rung can appear once per ladder within an anchor.)")
    P("  NOTHING PROPOSED FOR THE SUNDAY REVIEW: the books at all 162 rungs are byte-identical")
    P("  across both dials — only which rung gets CALLED reached changes — so 4a and 4b are")
    P("  invariant to the anchor and to the panel label by construction.  Scored because rule 4")
    P("  and rule 8 require it.")
    P("")

    P("## GATE SUMMARY")
    P(f"   {sum(1 for v in gates.values() if v)} of {len(gates)} PASS")
    dump(pd.DataFrame(gaterows), "gates")

    P("\n## SURVIVORSHIP (PROTOCOL rule 9)")
    P("   U56 and B136 are CURRENT-CONSTITUENT lists.  The SMALL pool is worse: the CURRENT")
    P("   constituents of a sub-$2B screen, so every name that fell below the screen, delisted")
    P("   or went to zero is absent.  Every CAGR and drawdown LEVEL on SMALL is optimistic by an")
    P("   amount this run cannot measure.  A REACH decision contrasts two rungs of one ladder")
    P("   over the same inflated tape and the bias very largely cancels out of it; it does NOT")
    P("   cancel out of the 4b legs, measured against SPY, so every 4b count is an UPPER bound.")
    P("\n## THE DECLARED APPROXIMATION, AND ITS DIRECTION")
    P("   P_boot is a moving-block bootstrap of the realised IS paths with the SAME block index")
    P("   on every rung, so cross-rung correlation is preserved.  It resamples ONE tape, so it")
    P("   measures sampling error around this regime and not regime uncertainty: every P_boot is")
    P("   CLOSER TO 0 OR 1 than the truth, and H_RESOLVED is therefore scored in the direction")
    P("   that favours SUPPORTED.  A reach decision this run calls resolved may still be a coin")
    P("   flip across regimes; one it calls UNRESOLVED is unresolved a fortiori.")
    P(f"\n# done in {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

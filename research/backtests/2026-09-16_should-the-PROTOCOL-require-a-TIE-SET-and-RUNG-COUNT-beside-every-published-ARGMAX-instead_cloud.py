#!/usr/bin/env python3
"""Idea 1133 (cloud lane, idea 2 of 2, 2026-09-16) — should the PROTOCOL require a TIE SET and
RUNG COUNT beside every published ARGMAX instead?

QUESTION (QUEUE idea 1133, verbatim)
    idea 1117 killed the ladder-identity ban and named the claim-keyed alternative: quote the
    gap, the floor AND the rung count, and the tie set at the declared q.  Draft that clause and
    price it against the record's 32 committed argmaxes at both rung sets, reporting how many
    claims it restates rather than deletes.  Max 2 params (claim set, bar).

THE CLAUSE, DRAFTED (stated for the Sunday review, NOT enacted — PROTOCOL rule 6 forbids this
run from editing PROTOCOL.md, and it does not)
    PROPOSED PROTOCOL 4c — EVERY PUBLISHED ARGMAX CARRIES ITS OWN RESOLUTION.
    "A result that names the best rung of a ladder shall quote, beside it and in the same
     sentence: (i) the GAP from the peak to the runner-up, in the statistic's own units;
     (ii) the ladder's RESOLUTION FLOOR at the declared confidence q; (iii) the ladder's RUNG
     COUNT and its end rungs; and (iv) the TIE SET at that q — every rung the bootstrap cannot
     separate from the peak.  Where the tie set holds more than one rung, the result is
     published AS THE TIE SET and not as a rung.  Where the tie set is the whole ladder, no
     argmax is published at all."
    Nothing in the clause reads a whole-ladder flag, so — unlike 1117's ladder-identity ban —
    its trigger is defined at ANY rung count.  That is exactly what this run prices.

WHAT IS TUNED AND WHAT IS NOT (PROTOCOL rule 4)
    Exactly TWO dials: CLAIM SET {CS_ALL32, CS_DECIDED, CS_HCAD} x BAR {B_QUOTE, B_TIESET,
    B_DECIDE} = 9 combinations, ALL published, EACH at BOTH rung sets.
    RUNG SET {CORE, EXT} is NOT a dial and nothing is selected on it — 1118 established that
    P(INF_FLOOR) FALLS as rungs are added and 1117 died on exactly that dependence, so both
    levels are reported at every point and the movement between them IS the result.
    PANEL, LADDER and STATISTIC are not dials: all 2 x 4 x 4 = 32 cells are reported everywhere.
    q is not a dial: q=0.90 headline (1102/1110/1116/1117's own), never moved.
    Frozen at 1082/1094/1098/1102/1108/1110/1116/1117/1118's construction: CAND20 legs, cap INF,
    max_vol 0.60, gross 0.75, min hold 126, N=20, W, 10 bps, LAG 1, warm-up 260, IS end
    2016-12-31, block L=63, 1000 draws, crc32 seeds.

THE RUNG SETS (1116/1110's CORE and 1118's EXT, verbatim; N and GROSS are identical in both)
    N        [5,8,10,12,15,20,25,30,40]                          9  ->  9
    H        [21,63,126,252]  ->  [21,42,63,84,126,168,210,252,378]        4  ->  9
    GROSS    [0.30 .. 0.75 step 0.05]                           10  -> 10
    CADENCE  [D,W,M,Q]  ->  [D,2D,W,2W,M,2M,Q,2Q,4Q]             4  ->  9

THE THREE BARS (dial 2) — three strengths of the SAME clause
    B_QUOTE   the four quantities must be quoted; NOTHING is deleted.  Every claim is RESTATED,
              carrying its gap / floor / rung count / tie set.
    B_TIESET  as B_QUOTE, and a claim whose tie set holds > 1 rung is RESTATED AS THE TIE SET
              (wider, not gone); only a claim whose tie set is the WHOLE LADDER is DELETED,
              because it then asserts nothing about the ladder at all.
    B_DECIDE  the strict reading: only a DECIDED argmax (tie set = {peak}) may be published as a
              rung; every other argmax is DELETED as a rung claim.

DECLARED BEFORE ANY NUMBER
    (a) H_RESTATES  — the clause RESTATES strictly more claims than it DELETES at all 9 dial
                      points, at BOTH rung sets.  This is the idea's own framing and the whole
                      case for a claim-keyed clause over 1117's ban.
    (b) H_STABLE    — the clause's DELETE count is rung-stable where 1117's ban was not: over
                      the 9 points, max |deleted_CORE - deleted_EXT| <= 6 of 32, i.e. at most
                      HALF the 12-of-32 swing that killed the ban.
    (c) H_NO_ZERO   — the clause is never vacuous: at B_TIESET and B_DECIDE on CS_ALL32 it
                      deletes at least one claim at BOTH rung sets.  1117's ban barred 0 of 32
                      at EXT, and that emptiness was its fatal defect.
    (d) H_WIDENS    — the clause's COST is width, not silence: median tie-set size GROWS from
                      CORE to EXT on the two ladders whose rung count changes (H, CADENCE).
    (e) H_DECIDED_SURVIVE — the record's DECIDED cells survive as rung claims under ALL THREE
                      bars at BOTH rung sets.  They are decided at CORE by construction; whether
                      they stay decided when rungs are added is the open half.
    (f) THE CLAUSE IS NOT A KEEP PATH.  4a and 4b are scored at every rung of every ladder at
        both rung sets, and rule 8 picks the rung per ladder on IS 2009-2016 ALONE under three
        choosers with OOS 2017-2026 read once.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT panels, so every 4b figure
    below is an upper bound.  Gaps, floors and tie sets are within-panel contrasts between two
    books over the same inflated tape and the bias very largely cancels out of them — which is
    why this run's headline is a clause-pricing claim and not a capital claim.
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
SLUG = "should-the-PROTOCOL-require-a-TIE-SET-and-RUNG-COUNT-beside-every-published-ARGMAX-instead"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST, GROSS0, FREQ0, HOLD0, N0 = 10.0, 0.75, "W", 126, 20
LEGS = [(21, 252), (0, 126), (0, 63)]

LAD_N = [5, 8, 10, 12, 15, 20, 25, 30, 40]
LAD_G = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]
RUNGSETS = {
    "CORE": {"N": LAD_N, "H": [21, 63, 126, 252], "GROSS": LAD_G,
             "CADENCE": ["D", "W", "M", "Q"]},
    "EXT": {"N": LAD_N, "H": [21, 42, 63, 84, 126, 168, 210, 252, 378], "GROSS": LAD_G,
            "CADENCE": ["D", "2D", "W", "2W", "M", "2M", "Q", "2Q", "4Q"]},
}
LADDERS = ["N", "H", "GROSS", "CADENCE"]
PANELS = ["U56", "B136"]
STATS = ["S_FULL", "S_OOS", "CAGR", "DD"]
STATCOL = {"S_FULL": "Sharpe", "S_OOS": "OOS_Sharpe", "CAGR": "CAGR", "DD": "MaxDD"}
SCALE = {"S_FULL": 1.0, "S_OOS": 1.0, "CAGR": 100.0, "DD": 100.0}
UNITS = {"S_FULL": "Sharpe", "S_OOS": "Sharpe", "CAGR": "pp of CAGR", "DD": "pp of MaxDD"}
CLAIMSETS = ["CS_ALL32", "CS_DECIDED", "CS_HCAD"]          # dial 1
BARS = ["B_QUOTE", "B_TIESET", "B_DECIDE"]                 # dial 2
CHOOSERS = ["C_ISSHARPE", "C_ISCAGR", "C_ISDD"]
Q_HEAD, L_HEAD, BDRAWS = 0.90, 63, 1000
SEED_BOOT = 11331133

# 1117's committed ban counts, for the rung-stability contrast (never for selection)
BAN1117 = {"CS_ALL32": (12, 0), "CS_HCAD": (12, 0)}        # (CORE, EXT) barred of 32 / of 16

A936_WH126 = (0.155787, 1.139701, -0.191276)
A1098_U56_N12 = (0.1771, 1.1692, -0.2017)
A1098_B136_N15 = (0.1678, 1.0682, -0.1966)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205

LOG: list[str] = []


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


# ---------------------------------------- 1082/1098/1102/1108/1118's fast runner, verbatim
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


def cadence_mask(idx, spec):
    """1118's construction verbatim: engine.rebalance_mask for D/W/M/Q (gate G7), and
    '<k><BASE>' keeps every k-th bar of that base schedule.  engine.py is NOT modified."""
    if spec in ("D", "W", "M", "Q"):
        return rebalance_mask(idx, spec).values.copy()
    k, base = int(spec[:-1]), spec[-1]
    hit = np.flatnonzero(rebalance_mask(idx, base).values)
    m = np.zeros(len(idx), dtype=bool)
    m[hit[::k]] = True
    return m


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


# ------------------------------------------------- 1098/1102/1108's bootstrap, crc32 seeds
def block_index(rng, T, L, ndraws):
    nb = int(np.ceil(T / L))
    st = rng.integers(0, T, size=(ndraws, nb))
    off = np.arange(L)
    idx = (st[:, :, None] + off[None, None, :]) % T
    return idx.reshape(ndraws, nb * L), nb


def boot_exact(R, idx, nb, L, chunk=100):
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
    nr = R.shape[0]
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


def floor_from_agreement(gaps, agree, q):
    """1098/1102's floor: the smallest |gap| above which every larger-gap pair agrees >= q."""
    gaps, agree = np.asarray(gaps, float), np.asarray(agree, float)
    un = agree < q
    largest_un = float(gaps[un].max()) if un.any() else 0.0
    ok = (~un) & (gaps > largest_un)
    return (float(gaps[ok].min()) if ok.any() else float("inf")), largest_un, int(un.sum())


def main():
    t0 = time.time()
    P(f"# Idea 1133 (cloud lane, idea 2 of 2, {DATE}) — should the PROTOCOL require a TIE SET")
    P("#   and RUNG COUNT beside every published ARGMAX instead?")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4): CLAIM SET {CLAIMSETS} x BAR {BARS} = "
      f"{len(CLAIMSETS)*len(BARS)} points, ALL published, EACH at BOTH rung sets.")
    P("#   RUNG SET {CORE, EXT} is NOT a dial and nothing is selected on it — 1117 died on rung")
    P("#   dependence, so both levels are reported everywhere and the movement IS the result.")
    P("#   PANEL, LADDER and STATISTIC are not dials (all 32 cells reported everywhere).")
    P(f"#   q is not a dial: q={Q_HEAD} throughout, 1102/1110/1116/1117's own.")
    P(f"# FROZEN: CAND20 legs {LEGS}, cap INF, max_vol {MAXVOL}, gross {GROSS0}, cadence "
      f"{FREQ0}, min hold {HOLD0}, N {N0},")
    P(f"#   {COST:.0f} bps, LAG {LAG}, warm-up {WARMUP}, IS end {IS_END}, block L={L_HEAD}, "
      f"{BDRAWS} draws, crc32 seeds — each except where it is the ladder.")
    P("# THE CLAUSE, DRAFTED (stated for Sunday review, NOT enacted — rule 6):")
    P("#   PROPOSED 4c: a result naming the best rung of a ladder shall quote beside it the")
    P("#   GAP to the runner-up, the ladder's RESOLUTION FLOOR at q, the RUNG COUNT and end")
    P("#   rungs, and the TIE SET at q.  A tie set of > 1 rung is published AS THE TIE SET and")
    P("#   not as a rung; a tie set spanning the whole ladder publishes no argmax at all.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   (a) H_RESTATES  restates > deletes at all 9 dial points, at BOTH rung sets.")
    P("#   (b) H_STABLE    max |deleted_CORE - deleted_EXT| <= 6 of 32 (half 1117's 12-of-32).")
    P("#   (c) H_NO_ZERO   deletes >= 1 at BOTH rung sets under B_TIESET and B_DECIDE (CS_ALL32).")
    P("#   (d) H_WIDENS    median tie-set size GROWS CORE -> EXT on H and CADENCE.")
    P("#   (e) H_DECIDED_SURVIVE  the record's DECIDED cells survive under all 3 bars, both sets.")
    P("#   (f) THE CLAUSE IS NOT A KEEP PATH: 4a/4b at every rung, rule 8 per ladder.")
    P("")

    gates, gaterows = {}, []
    gridrows, benchrows, cellrows, pairrows, pickrows = [], [], [], [], []
    panels, metr, series = {}, {}, {}

    P("## GATES — printed before any result number")
    for panel in PANELS:
        px = load_universe(broad=(panel == "B136")).dropna(how="all").ffill()
        idx, K, T = px.index, len(px.columns), len(px.index)
        panels[panel] = dict(px=px, idx=idx, K=K, T=T, rets=px.pct_change().fillna(0.0).values,
                             priced=px.notna().values)
        warm, ins, oos = windows(idx)
        sc, elig = mech(px)
        panels[panel].update(warm=warm, ins=ins, oos=oos, sc=sc, elig=elig)
        P(f"  {panel}: {K} names, {T:,} rows {idx[0].date()} -> {idx[-1].date()}, "
          f"warm {warm.sum():,}, IS {ins.sum():,}, OOS {oos.sum():,}")

    def run_cell(panel, N, H, gross, freq):
        d = panels[panel]
        mk = cadence_mask(d["idx"], freq)
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        reb = np.flatnonzero(mk)
        W = build(-d["sc"], d["elig"], d["priced"], reb, N, H, d["T"], d["K"], gross)
        Wl = np.zeros_like(W)
        Wl[LAG:] = W[:-LAG]
        g, tn = nrun(d["rets"], Wl, mkl)
        return g - tn * COST / 1e4, tn

    d = panels["U56"]
    mk = rebalance_mask(d["idx"], FREQ0).values
    reb = np.flatnonzero(mk)
    W = build(-d["sc"], d["elig"], d["priced"], reb, N0, HOLD0, d["T"], d["K"], GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST, freq=FREQ0)["returns"].values
    rfast, _ = run_cell("U56", N0, HOLD0, GROSS0, FREQ0)
    g1 = float(np.abs(eng[d["warm"]] - rfast[d["warm"]]).max())
    gates["G1  fast runner == engine.backtest (U56 W/H126/N=20)"] = (g1, g1 < 1e-12)
    m = blocks_m(rfast, d["warm"], d["ins"], d["oos"])
    g2 = max(abs(m["CAGR"] - A936_WH126[0]), abs(m["Sharpe"] - A936_WH126[1]),
             abs(m["MaxDD"] - A936_WH126[2]))
    gates["G2  CROSS-RUN committed U56 W/H126/N=20 triple"] = (g2, g2 < 5e-5)
    spy = d["px"]["SPY"].pct_change().fillna(0.0).values
    sm = blocks_m(spy, d["warm"], d["ins"], d["oos"])
    g3 = max(abs(sm["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
             abs(sm["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
             abs(sm["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gates["G3  CROSS-RUN SPY OOS triple"] = (g3, g3 < 5e-4)
    r12, _ = run_cell("U56", 12, HOLD0, GROSS0, FREQ0)
    m12 = blocks_m(r12, d["warm"], d["ins"], d["oos"])
    g4 = max(abs(m12["CAGR"] - A1098_U56_N12[0]), abs(m12["Sharpe"] - A1098_U56_N12[1]),
             abs(m12["MaxDD"] - A1098_U56_N12[2]))
    gates["G4  CROSS-RUN 1098/1102's committed U56 n=12 triple"] = (g4, g4 < 5e-4)
    db = panels["B136"]
    r15, _ = run_cell("B136", 15, HOLD0, GROSS0, FREQ0)
    m15 = blocks_m(r15, db["warm"], db["ins"], db["oos"])
    g4b = max(abs(m15["CAGR"] - A1098_B136_N15[0]), abs(m15["Sharpe"] - A1098_B136_N15[1]),
              abs(m15["MaxDD"] - A1098_B136_N15[2]))
    gates["G4b CROSS-RUN 1098/1102's committed B136 n=15 triple"] = (g4b, g4b < 5e-4)
    lb_r = backtest(d["px"], rules_v2_weights(d["px"]), cost_bps=COST, freq="W")["returns"].values
    lbm = blocks_m(lb_r, d["warm"], d["ins"], d["oos"])
    g5 = abs(lbm["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gates["G5  live RULES v2 MaxDD == committed -12.05%"] = (g5, g5 < 5e-4)
    r12b, _ = run_cell("U56", 12, HOLD0, GROSS0, FREQ0)
    g6 = float(np.abs(r12 - r12b).max())
    gates["G6  determinism of the cell pipeline"] = (g6, g6 == 0.0)
    g7 = 0
    for c in ("D", "W", "M", "Q"):
        g7 += int((cadence_mask(d["idx"], c) != rebalance_mask(d["idx"], c).values).sum())
    gates["G7  cadence_mask == engine.rebalance_mask on D/W/M/Q (differing bars)"] = (
        float(g7), g7 == 0)
    g7b = 0
    for base, k in (("W", 2), ("M", 2), ("Q", 2), ("Q", 4)):
        spec = f"{k}{base}"
        hit = np.flatnonzero(rebalance_mask(d["idx"], base).values)
        g7b += int(cadence_mask(d["idx"], spec).sum() - len(hit[::k]))
    gates["G7b every extended cadence rung is a k-th-bar subset of an engine schedule"] = (
        float(g7b), g7b == 0)
    g8 = int(len(set(RUNGSETS["CORE"]["H"]) - set(RUNGSETS["EXT"]["H"])) +
             len(set(RUNGSETS["CORE"]["CADENCE"]) - set(RUNGSETS["EXT"]["CADENCE"])))
    gates["G8  EXT NESTS CORE on every ladder (rungs in CORE but not EXT)"] = (float(g8), g8 == 0)

    # ------------------------------------------------- BUILD EVERY RUNG OF EVERY LADDER ONCE
    P("")
    P("## THE BOOKS — the union of both rung sets, every rung published")
    bench = {}
    for panel in PANELS:
        dd_ = panels[panel]
        sb = blocks_m(dd_["px"]["SPY"].pct_change().fillna(0.0).values,
                      dd_["warm"], dd_["ins"], dd_["oos"])
        lbp = blocks_m(backtest(dd_["px"], rules_v2_weights(dd_["px"]), cost_bps=COST,
                                freq="W")["returns"].values, dd_["warm"], dd_["ins"], dd_["oos"])
        bench[panel] = (sb, lbp)
        benchrows.append(dict(panel=panel, series="SPY", **sb))
        benchrows.append(dict(panel=panel, series="RULESv2_live", **lbp))
        P(f"  {panel} SPY       full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%}  "
          f"halves {sb['H1']:.4f}/{sb['H2']:.4f}  OOS {sb['OOS_CAGR']:.2%} / "
          f"{sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"  {panel} RULES v2  full {lbp['CAGR']:.2%} / {lbp['Sharpe']:.4f} / {lbp['MaxDD']:.2%}"
          f"  OOS {lbp['OOS_CAGR']:.2%} / {lbp['OOS_Sharpe']:.4f} / {lbp['OOS_MaxDD']:.2%}")
        for lad in LADDERS:
            allr = list(RUNGSETS["EXT"][lad])
            for rung in allr:
                N, H, g_, f_ = N0, HOLD0, GROSS0, FREQ0
                if lad == "N":
                    N = rung
                elif lad == "H":
                    H = rung
                elif lad == "GROSS":
                    g_ = rung
                else:
                    f_ = rung
                r, tn = run_cell(panel, N, H, g_, f_)
                mm = blocks_m(r, dd_["warm"], dd_["ins"], dd_["oos"])
                metr[(panel, lad, rung)] = mm
                series[(panel, lad, rung)] = (r[dd_["warm"]], r[dd_["oos"]])
                l4b, l4o, l4a = legs_4b(mm, sb), legs_4b_oos(mm, sb), legs_4a(mm, lbp)
                gridrows.append(dict(panel=panel, ladder=lad, rung=str(rung), N=N, H=H, gross=g_,
                                     freq=f_, in_CORE=bool(rung in RUNGSETS["CORE"][lad]),
                                     turnover=float(tn[dd_["warm"]].sum() /
                                                    (dd_["warm"].sum() / 252.0)),
                                     **mm, pass_4b_full=all(l4b.values()),
                                     pass_4b_oos=all(l4o.values()), pass_4a=all(l4a.values()),
                                     **l4b, **l4o, **l4a))
            P(f"  {panel} {lad:<8} {len(allr)} rungs (CORE {len(RUNGSETS['CORE'][lad])}): "
              + " ".join(f"{metr[(panel, lad, r_)]['Sharpe']:.4f}" for r_ in allr))
    grid = pd.DataFrame(gridrows)
    sp = float(grid["Sharpe"].max() - grid["Sharpe"].min())
    gates["G9  the ladders are live (Sharpe spread over every book)"] = (sp, sp > 0.05)

    ok = 0
    P("")
    for k, (v, good) in gates.items():
        P(f"  {'PASS' if good else 'FAIL'}  {k}: {v:.3e}")
        gaterows.append(dict(gate=k, value=v, passed=bool(good)))
        ok += bool(good)
    P(f"  {ok} of {len(gates)} gates pass")
    dump(pd.DataFrame(gaterows), "gates")
    dump(grid, "grid")
    dump(pd.DataFrame(benchrows), "benchmarks")

    # ---------------------------------------- THE 32 CELLS x 2 RUNG SETS: THE FOUR QUANTITIES
    P("")
    P("## THE FOUR QUANTITIES THE CLAUSE DEMANDS — 32 committed argmaxes x 2 rung sets")
    P("   gap (peak vs runner-up), resolution floor at q=0.90, rung count, tie set at q")
    for rs in ("CORE", "EXT"):
        for panel in PANELS:
            for lad in LADDERS:
                rungs = RUNGSETS[rs][lad]
                Rw = np.vstack([series[(panel, lad, r_)][0] for r_ in rungs])
                Ro = np.vstack([series[(panel, lad, r_)][1] for r_ in rungs])
                rng = np.random.default_rng(seed_of(panel, lad, rs, L_HEAD))
                ixw, nbw = block_index(rng, Rw.shape[1], L_HEAD, BDRAWS)
                ixo, nbo = block_index(rng, Ro.shape[1], L_HEAD, BDRAWS)
                bcw, bsw = boot_exact(Rw, ixw, nbw, L_HEAD)
                _, bso = boot_exact(Ro, ixo, nbo, L_HEAD)
                bdd = boot_maxdd(Rw, ixw)
                boots = {"S_FULL": bsw, "S_OOS": bso, "CAGR": bcw * 100.0, "DD": bdd * 100.0}
                for stat in STATS:
                    v = np.array([metr[(panel, lad, r_)][STATCOL[stat]] for r_ in rungs]) \
                        * SCALE[stat]
                    bm = boots[stat]
                    gaps, agr = [], []
                    for i, j in combinations(range(len(rungs)), 2):
                        g0 = v[i] - v[j]
                        dbv = bm[i] - bm[j]
                        dbv = dbv[np.isfinite(dbv)]
                        a_ = float((np.sign(dbv) == np.sign(g0)).mean()) if len(dbv) else np.nan
                        gaps.append(abs(g0))
                        agr.append(a_)
                        pairrows.append(dict(rung_set=rs, panel=panel, ladder=lad, stat=stat,
                                             rung_i=str(rungs[i]), rung_j=str(rungs[j]),
                                             gap=g0, abs_gap=abs(g0), agreement=a_,
                                             resolved=bool(a_ >= Q_HEAD)))
                    gaps, agr = np.array(gaps), np.array(agr)
                    flo, lun, nun = floor_from_agreement(gaps, agr, Q_HEAD)
                    order = np.argsort(-v, kind="stable")
                    peak, runner = int(order[0]), int(order[1])
                    pgap = float(v[peak] - v[runner])
                    spread = float(v.max() - v.min())
                    tie = [str(rungs[peak])]
                    for j in range(len(rungs)):
                        if j == peak:
                            continue
                        dbv = bm[peak] - bm[j]
                        dbv = dbv[np.isfinite(dbv)]
                        a_ = float((np.sign(dbv) == np.sign(v[peak] - v[j])).mean()) \
                            if len(dbv) else 0.0
                        if a_ < Q_HEAD:
                            tie.append(str(rungs[j]))
                    cellrows.append(dict(
                        rung_set=rs, panel=panel, ladder=lad, stat=stat, units=UNITS[stat],
                        rung_count=len(rungs), end_rungs=f"{rungs[0]}..{rungs[-1]}",
                        peak=str(rungs[peak]), runner_up=str(rungs[runner]), gap=pgap,
                        spread=spread, floor=flo, floor_capped=min(flo, spread),
                        floor_infinite=bool(not np.isfinite(flo)),
                        rel_floor=min(flo, spread) / spread if spread > 0 else np.nan,
                        n_unresolved=nun, n_pairs=len(gaps), largest_unresolved=lun,
                        tie_size=len(tie), tie_set=";".join(tie),
                        decided=bool(len(tie) == 1),
                        whole_ladder=bool(len(tie) == len(rungs))))
        P(f"   {rs} rung set done ({time.time()-t0:.0f}s)")
    cells = pd.DataFrame(cellrows)
    dump(cells, "cells")
    dump(pd.DataFrame(pairrows), "pairs")

    P("")
    P("   rungset panel  ladder   stat     peak     gap        floor      k   tie set")
    for _, r_ in cells.iterrows():
        fs = "INF" if r_.floor_infinite else f"{r_.floor:.4f}"
        P(f"   {r_.rung_set:<7} {r_.panel:<6} {r_.ladder:<8} {r_.stat:<8} {r_.peak:<8} "
          f"{r_.gap:+9.4f}  {fs:>9}  {r_.rung_count:2d}   {r_.tie_set}")

    # -------------------------------------------------- THE CLAUSE PRICED: 9 POINTS x 2 SETS
    P("")
    P("## THE CLAUSE PRICED — 9 dial points, EACH at both rung sets")
    dec_core = set(zip(cells[(cells.rung_set == "CORE") & cells.decided].panel,
                       cells[(cells.rung_set == "CORE") & cells.decided].ladder,
                       cells[(cells.rung_set == "CORE") & cells.decided].stat))

    def claim_mask(df, cs):
        if cs == "CS_ALL32":
            return pd.Series(True, index=df.index)
        if cs == "CS_HCAD":
            return df.ladder.isin(["H", "CADENCE"])
        return pd.Series([(p, l, s) in dec_core for p, l, s in zip(df.panel, df.ladder, df.stat)],
                         index=df.index)

    def disposition(row, bar):
        if bar == "B_QUOTE":
            return "RESTATED_AS_IS" if row.decided else "RESTATED_WITH_NUMBERS"
        if bar == "B_TIESET":
            if row.decided:
                return "RESTATED_AS_IS"
            return "DELETED" if row.whole_ladder else "RESTATED_AS_TIE_SET"
        return "RESTATED_AS_IS" if row.decided else "DELETED"

    pricerows, disprows = [], []
    for cs in CLAIMSETS:
        for bar in BARS:
            for rs in ("CORE", "EXT"):
                sub = cells[cells.rung_set == rs]
                sub = sub[claim_mask(sub, cs)]
                disp = [disposition(r_, bar) for _, r_ in sub.iterrows()]
                for (_, r_), dsp in zip(sub.iterrows(), disp):
                    disprows.append(dict(claim_set=cs, bar=bar, rung_set=rs, panel=r_.panel,
                                         ladder=r_.ladder, stat=r_.stat, peak=r_.peak,
                                         tie_size=r_.tie_size, disposition=dsp))
                n = len(sub)
                nd = sum(x == "DELETED" for x in disp)
                pricerows.append(dict(
                    claim_set=cs, bar=bar, rung_set=rs, n_claims=n,
                    restated_as_is=sum(x == "RESTATED_AS_IS" for x in disp),
                    restated_with_numbers=sum(x == "RESTATED_WITH_NUMBERS" for x in disp),
                    restated_as_tie_set=sum(x == "RESTATED_AS_TIE_SET" for x in disp),
                    restated_total=n - nd, deleted=nd,
                    restate_share=(n - nd) / n if n else np.nan,
                    median_tie_size=float(sub.tie_size.median()) if n else np.nan))
    price = pd.DataFrame(pricerows)
    dump(price, "clause")
    dump(pd.DataFrame(disprows), "disposition")
    P("   claim set   bar        set   n   as-is  +numbers  as-tie-set  DELETED  restate share")
    for _, r_ in price.iterrows():
        P(f"   {r_.claim_set:<11} {r_.bar:<10} {r_.rung_set:<5} {r_.n_claims:2d}  "
          f"{r_.restated_as_is:5d}  {r_.restated_with_numbers:8d}  {r_.restated_as_tie_set:10d}  "
          f"{r_.deleted:7d}  {r_.restate_share:12.4f}")

    # (a) H_RESTATES
    H_RESTATES = bool((price.restated_total > price.deleted).all())
    nbad = int((price.restated_total <= price.deleted).sum())
    P("")
    P(f"   (a) H_RESTATES  restates > deletes at {len(price)-nbad} of {len(price)} "
      f"(point x rung set) rows -> {'SUPPORTED' if H_RESTATES else 'REFUTED'}")

    # (b) H_STABLE, against 1117's own swing
    stab = price.pivot_table(index=["claim_set", "bar"], columns="rung_set",
                             values="deleted").reset_index()
    stab["swing"] = (stab["CORE"] - stab["EXT"]).abs()
    dump(stab, "stability")
    H_STABLE = bool(stab["swing"].max() <= 6)
    P(f"   (b) H_STABLE    DELETE count CORE -> EXT, all 9 dial points:")
    for _, r_ in stab.iterrows():
        P(f"       {r_.claim_set:<11} {r_.bar:<10} {int(r_.CORE):2d} -> {int(r_.EXT):2d}   "
          f"swing {int(r_.swing)}")
    P(f"       max swing {int(stab['swing'].max())} of 32 against 1117's ban's "
      f"{BAN1117['CS_ALL32'][0]} -> {BAN1117['CS_ALL32'][1]} (swing "
      f"{abs(BAN1117['CS_ALL32'][0]-BAN1117['CS_ALL32'][1])}) -> "
      f"{'SUPPORTED' if H_STABLE else 'REFUTED'}")

    # (c) H_NO_ZERO
    z = price[(price.claim_set == "CS_ALL32") & (price.bar.isin(["B_TIESET", "B_DECIDE"]))]
    H_NO_ZERO = bool((z.deleted >= 1).all())
    P(f"   (c) H_NO_ZERO   CS_ALL32 deletes at both rung sets under both strict bars: "
      + ", ".join(f"{r_.bar}/{r_.rung_set}={int(r_.deleted)}" for _, r_ in z.iterrows())
      + f" -> {'SUPPORTED' if H_NO_ZERO else 'REFUTED'}")

    # (d) H_WIDENS
    wid = cells.groupby(["ladder", "rung_set"]).tie_size.median().unstack()
    H_WIDENS = bool(wid.loc["H", "EXT"] > wid.loc["H", "CORE"] and
                    wid.loc["CADENCE", "EXT"] > wid.loc["CADENCE", "CORE"])
    P("   (d) H_WIDENS    median tie-set size by ladder, CORE -> EXT:")
    for lad in LADDERS:
        P(f"       {lad:<8} {wid.loc[lad,'CORE']:.1f} -> {wid.loc[lad,'EXT']:.1f}   "
          f"(rungs {len(RUNGSETS['CORE'][lad])} -> {len(RUNGSETS['EXT'][lad])})")
    P(f"       -> {'SUPPORTED' if H_WIDENS else 'REFUTED'}")

    # (e) H_DECIDED_SURVIVE
    ext_dec = set(zip(cells[(cells.rung_set == "EXT") & cells.decided].panel,
                      cells[(cells.rung_set == "EXT") & cells.decided].ladder,
                      cells[(cells.rung_set == "EXT") & cells.decided].stat))
    survive = len(dec_core & ext_dec)
    H_DECIDED_SURVIVE = bool(survive == len(dec_core) and len(dec_core) > 0)
    P(f"   (e) H_DECIDED_SURVIVE  the record DECIDES {len(dec_core)} of 32 at CORE and "
      f"{len(ext_dec)} of 32 at EXT; {survive} of the CORE-decided stay decided at EXT -> "
      f"{'SUPPORTED' if H_DECIDED_SURVIVE else 'REFUTED'}")
    for p_, l_, s_ in sorted(dec_core):
        P(f"       CORE-decided {p_:<6} {l_:<8} {s_:<8} "
          f"{'still decided at EXT' if (p_,l_,s_) in ext_dec else 'BECOMES A TIE SET at EXT'}")

    # ----------------------------------------------------- RULE 8 AND BOTH KEEP PATHS
    P("")
    P("## RULE 8 (walk-forward) AND BOTH KEEP PATHS — the clause is not a keep path")
    for panel in PANELS:
        sb, lbp = bench[panel]
        for rs in ("CORE", "EXT"):
            for lad in LADDERS:
                rungs = RUNGSETS[rs][lad]
                gp = grid[(grid.panel == panel) & (grid.ladder == lad) &
                          (grid.rung.isin([str(x) for x in rungs]))]
                for ch in CHOOSERS:
                    key = {"C_ISSHARPE": "IS_Sharpe", "C_ISCAGR": "IS_CAGR",
                           "C_ISDD": "IS_MaxDD"}[ch]
                    r_ = gp.sort_values(key, ascending=False).iloc[0]
                    pickrows.append(dict(
                        rung_set=rs, panel=panel, ladder=lad, chooser=ch, pick=r_.rung,
                        CAGR=r_.CAGR, Sharpe=r_.Sharpe, MaxDD=r_.MaxDD, H1=r_.H1, H2=r_.H2,
                        OOS_CAGR=r_.OOS_CAGR, OOS_Sharpe=r_.OOS_Sharpe, OOS_MaxDD=r_.OOS_MaxDD,
                        pass_4b_full=bool(r_.pass_4b_full), pass_4b_oos=bool(r_.pass_4b_oos),
                        pass_4a=bool(r_.pass_4a), spy_OOS_Sharpe=sb["OOS_Sharpe"],
                        live_OOS_Sharpe=lbp["OOS_Sharpe"],
                        regret=float(gp.OOS_Sharpe.max() - r_.OOS_Sharpe)))
    pk = pd.DataFrame(pickrows)
    dump(pk, "walkforward")
    P(f"   {len(pk)} IS picks (rung chosen on 2009-2016 alone, OOS read once): 4b full "
      f"{int(pk.pass_4b_full.sum())}, 4b OOS {int(pk.pass_4b_oos.sum())}, 4a "
      f"{int(pk.pass_4a.sum())}, median OOS Sharpe {pk.OOS_Sharpe.median():.4f}, median regret "
      f"{pk.regret.median():+.4f}")
    P(f"   whole grid, {len(grid)} books: 4b full {int(grid.pass_4b_full.sum())}, 4b OOS "
      f"{int(grid.pass_4b_oos.sum())}, 4a {int(grid.pass_4a.sum())}")
    P("   every 4b-passing book, both panels:")
    for _, r_ in grid[grid.pass_4b_full | grid.pass_4b_oos].iterrows():
        P(f"     {r_.panel:<6} {r_.ladder:<8} rung {r_.rung:<5} full {r_.CAGR:7.2%} / "
          f"{r_.Sharpe:.4f} / {r_.MaxDD:7.2%}  halves {r_.H1:.4f}/{r_.H2:.4f}  OOS "
          f"{r_.OOS_CAGR:7.2%} / {r_.OOS_Sharpe:.4f} / {r_.OOS_MaxDD:7.2%}   4b full "
          f"{'Y' if r_.pass_4b_full else 'n'}  4b OOS {'Y' if r_.pass_4b_oos else 'n'}  4a "
          f"{'Y' if r_.pass_4a else 'n'}  {'[CORE]' if r_.in_CORE else '[EXT-only]'}")
    for _, r_ in pd.DataFrame(benchrows).iterrows():
        P(f"     BENCH {r_.panel:<6} {r_.series:<14} full {r_.CAGR:7.2%} / {r_.Sharpe:.4f} / "
          f"{r_.MaxDD:7.2%}  halves {r_.H1:.4f}/{r_.H2:.4f}  OOS {r_.OOS_CAGR:7.2%} / "
          f"{r_.OOS_Sharpe:.4f} / {r_.OOS_MaxDD:7.2%}")

    hyp = pd.DataFrame([
        dict(hypothesis="H_RESTATES", result="SUPPORTED" if H_RESTATES else "REFUTED",
             detail=f"restates > deletes at {len(price)-nbad} of {len(price)} rows"),
        dict(hypothesis="H_STABLE", result="SUPPORTED" if H_STABLE else "REFUTED",
             detail=f"max CORE->EXT delete swing {int(stab['swing'].max())} of 32 "
                    f"vs 1117's ban's 12"),
        dict(hypothesis="H_NO_ZERO", result="SUPPORTED" if H_NO_ZERO else "REFUTED",
             detail=";".join(f"{r_.bar}/{r_.rung_set}={int(r_.deleted)}"
                             for _, r_ in z.iterrows())),
        dict(hypothesis="H_WIDENS", result="SUPPORTED" if H_WIDENS else "REFUTED",
             detail=f"H {wid.loc['H','CORE']:.1f}->{wid.loc['H','EXT']:.1f}, CADENCE "
                    f"{wid.loc['CADENCE','CORE']:.1f}->{wid.loc['CADENCE','EXT']:.1f}"),
        dict(hypothesis="H_DECIDED_SURVIVE",
             result="SUPPORTED" if H_DECIDED_SURVIVE else "REFUTED",
             detail=f"{survive} of {len(dec_core)} CORE-decided still decided at EXT"),
    ])
    dump(hyp, "hypotheses")
    P("")
    P("## HYPOTHESES")
    for _, r_ in hyp.iterrows():
        P(f"   {r_.hypothesis:<20} {r_.result:<10} {r_.detail}")
    P(f"   {int((hyp.result=='SUPPORTED').sum())} of {len(hyp)} supported")
    P("")
    P("# SURVIVORSHIP (rule 9): U56 and B136 are CURRENT-CONSTITUENT panels, so every 4b figure")
    P("#   above is an upper bound.  Gaps, floors and tie sets are within-panel contrasts over")
    P("#   one tape and the bias very largely cancels out of them.")
    P(f"# done in {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

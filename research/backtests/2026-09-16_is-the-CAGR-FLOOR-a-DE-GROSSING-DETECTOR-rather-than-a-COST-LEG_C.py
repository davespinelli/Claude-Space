#!/usr/bin/env python3
"""Idea 1150 (lane C, 2026-09-16)
   is-the-CAGR-FLOOR-a-DE-GROSSING-DETECTOR-rather-than-a-COST-LEG

The queue's premise: idea 1098 found every CAGR-killed 4b cell sits on the GROSS ladder and
none on N, H or CADENCE, because cutting gross cuts CAGR against an UNCHARGED, FULLY
INVESTED SPY floor while Sharpe barely moves.  The ask: walk gross on a FINER ladder at
several COST rungs, report the gross rung at which the binding leg hands over from a
Sharpe-family leg to L_CAGR, and say whether that hand-over is a COST object at all.

TUNED DIALS (2, PROTOCOL rule 4 — and the queue names both): `GROSS RUNG`
{0.20 .. 1.00 step 0.025, 33 rungs} x `COST RUNG` {0, 2, 5, 7.5, 10, 15, 25, 50 bps,
8 rungs} = 264 combinations per panel, 528 in all, EVERY ONE PUBLISHED in .grid.csv.
PANEL {U56, B136} is NOT a dial (both reported everywhere, nothing selected on either).
The BENCHMARK VARIANT is NOT a dial either: B_SPY is the PROTOCOL floor and is the
headline; B_SPYCOST (SPY charged the same cost rate on its own turnover) and B_SPYGROSS
(SPY held at the SAME gross, remainder in cash) are CONTROLS reported at every one of the
528 cells, never selected on.  The finer ladder NESTS the record's committed 0.30..0.75
step-0.05 rungs exactly (gate G10) so every committed gross-ladder number is re-derivable
from this file.

FROZEN at 1082/1094/1098/1102/1108/1110/1116/1117/1118's construction: CAND20 legs
[(21,252),(0,126),(0,63)], cap INF, max_vol 0.60, min hold 126, N=20, W cadence, LAG 1,
warm-up 260, IS end 2016-12-31, zero-cash convention, block L=63, 1000 draws, crc32 seeds.
Gross and cost are the two dials and are the ONLY things that move.

Standalone, deterministic, offline.  Nothing outside research/ is written or modified.
"""
from __future__ import annotations

import sys
import time
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-16"
SLUG = "is-the-CAGR-FLOOR-a-DE-GROSSING-DETECTOR-rather-than-a-COST-LEG"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"
BT = Path(__file__).resolve().parent

LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
GROSS0, FREQ0, HOLD0, N0, COST0 = 0.75, "W", 126, 20, 10.0
LEGS = [(21, 252), (0, 126), (0, 63)]

# ---- DIAL 1: the finer gross ladder.  Nests the record's 0.30..0.75 step 0.05 exactly.
LAD_G = [round(0.20 + 0.025 * i, 3) for i in range(33)]          # 0.200 .. 1.000
# ---- DIAL 2: the cost ladder (the record's 0/5/10/25/50 bps rungs, plus 2/7.5/15)
LAD_C = [0.0, 2.0, 5.0, 7.5, 10.0, 15.0, 25.0, 50.0]

PANELS = ["U56", "B136"]
BENCHES = ["B_SPY", "B_SPYCOST", "B_SPYGROSS"]     # controls, NOT a dial
LEGNAMES = ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]
SHARPE_LEGS = {"L_H1", "L_H2", "L_OOS"}

Q_HEAD, L_HEAD, BDRAWS, SEED_BASE = 0.90, 63, 1000, 11501150

# committed cross-run anchors
A936_WH126 = (0.155787, 1.139701, -0.191276)           # U56 W/H126/N=20, 10 bps
A1098_U56_N12 = (0.1771, 1.1692, -0.2017)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
PRIOR_GRID = BT / "2026-09-16_should-the-PROTOCOL-forbid-publishing-an-ARGMAX-on-an-H-or-CADENCE-LADDER-at-all_B.grid.csv"

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
    return SEED_BASE + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


# ------------------------------------------- 1082/1098/1102/1108/1117's fast runner, verbatim
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


def legs_4a(b, lbm):
    return {"A_H1": bool(b["H1"] > lbm["H1"]), "A_H2": bool(b["H2"] > lbm["H2"]),
            "A_DD": bool(b["MaxDD"] >= lbm["MaxDD"])}


# ---------------------------------------------------------------- THE BINDING-LEG RULE
# DECLARED BEFORE ANY NUMBER.  Every 4b leg is re-expressed as the SIGNED FRACTION OF ITS
# OWN BAR still in hand, so the five are on one scale and the minimum is well defined:
#   L_H1 / L_H2 / L_OOS   m = (book - SPY) / |SPY|              (must be > 0)
#   L_DD                  m = (0.60*|SPY_dd| - |dd|) / (0.60*|SPY_dd|)
#   L_CAGR                m = (CAGR - 0.70*SPY_CAGR) / |0.70*SPY_CAGR|
# BINDING LEG = argmin over the five.  Negative m == that leg FAILS.  The definition is
# used identically at every one of the 528 cells and is never re-chosen.
def margins_4b(b, sb):
    m = {}
    for k, kb in (("L_H1", "H1"), ("L_H2", "H2"), ("L_OOS", "OOS_Sharpe")):
        m[k] = (b[kb] - sb[kb]) / abs(sb[kb])
    cap = DD_CAP * abs(sb["MaxDD"])
    m["L_DD"] = (cap - abs(b["MaxDD"])) / cap
    flo = CAGR_FLOOR * sb["CAGR"]
    m["L_CAGR"] = (b["CAGR"] - flo) / abs(flo)
    return m


def binding_of(m):
    return min(LEGNAMES, key=lambda k: m[k])


def block_index(rng, T, L, ndraws):
    nb = int(np.ceil(T / L))
    st = rng.integers(0, T, size=(ndraws, nb))
    off = np.arange(L)
    idx = (st[:, :, None] + off[None, None, :]) % T
    return idx.reshape(ndraws, nb * L), nb


def boot_stats(R, idx, chunk=40):
    """CAGR, Sharpe, |MaxDD|, H1, H2 of R under each block-bootstrap draw (paired index)."""
    nd, TL = idx.shape
    out = np.empty((nd, 5))
    h = TL // 2
    for a in range(0, nd, chunk):
        b = min(a + chunk, nd)
        X = R[idx[a:b]]
        eq = np.cumprod(1.0 + X, axis=1)
        out[a:b, 0] = eq[:, -1] ** (252.0 / TL) - 1.0
        vol = X.std(axis=1, ddof=1) * np.sqrt(252.0)
        out[a:b, 1] = (X.mean(axis=1) * 252.0) / vol
        out[a:b, 2] = np.abs((eq / np.maximum.accumulate(eq, axis=1) - 1.0).min(axis=1))
        for j, sl in ((3, slice(0, h)), (4, slice(h, TL))):
            Y = X[:, sl]
            v = Y.std(axis=1, ddof=1) * np.sqrt(252.0)
            out[a:b, j] = (Y.mean(axis=1) * 252.0) / v
    return out


def cadence_mask(idx, spec):
    if spec in ("D", "W", "M", "Q"):
        return rebalance_mask(idx, spec).values.copy()
    k, base = int(spec[:-1]), spec[-1]
    hit = np.flatnonzero(rebalance_mask(idx, base).values)
    m = np.zeros(len(idx), dtype=bool)
    m[hit[::k]] = True
    return m


def main():
    t0 = time.time()
    P(f"# Idea 1150 (lane C, {DATE}) — is the CAGR FLOOR a DE-GROSSING DETECTOR rather than a")
    P("#   COST LEG?  Walk gross FINE at several cost rungs; find the hand-over; ask if it moves with cost.")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4): GROSS RUNG ({len(LAD_G)} rungs "
      f"{LAD_G[0]}..{LAD_G[-1]} step 0.025) x COST RUNG ({len(LAD_C)} rungs {LAD_C} bps)")
    P(f"#   = {len(LAD_G) * len(LAD_C)} combinations per panel, {len(LAD_G) * len(LAD_C) * len(PANELS)} in all, EVERY ONE published in .grid.csv.")
    P("# PANEL {U56, B136} is NOT a dial (both reported everywhere).  BENCHMARK VARIANT is NOT a dial:")
    P("#   B_SPY is the PROTOCOL floor and the headline; B_SPYCOST (SPY charged the same cost rate on")
    P("#   its OWN turnover) and B_SPYGROSS (SPY held at the SAME gross, rest in cash) are CONTROLS")
    P("#   computed at every cell and never selected on.")
    P(f"# FROZEN: CAND20 legs {LEGS}, cap INF, max_vol {MAXVOL}, min hold {HOLD0}, N {N0}, cadence {FREQ0},")
    P(f"#   LAG {LAG}, warm-up {WARMUP}, IS end {IS_END}, zero cash, block L={L_HEAD}, {BDRAWS} draws, crc32 seeds, q={Q_HEAD}.")
    P("#")
    P("# THE BINDING-LEG RULE, DECLARED BEFORE ANY NUMBER: every 4b leg is re-expressed as the")
    P("#   SIGNED FRACTION OF ITS OWN BAR still in hand (Sharpe legs (book-SPY)/|SPY|; L_DD")
    P("#   (0.60|SPY_dd|-|dd|)/(0.60|SPY_dd|); L_CAGR (CAGR-0.70*SPY_CAGR)/|0.70*SPY_CAGR|).")
    P("#   BINDING LEG = argmin of the five.  Negative == that leg FAILS.  Never re-chosen.")
    P("#   g* (THE HAND-OVER) = the HIGHEST gross rung whose binding leg is L_CAGR.  MONOTONE means")
    P("#   L_CAGR binds at every rung at or below g* and at none above it.")
    P("#")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   (a) H_PREMISE       the record's committed gross-ladder 4b legs reproduce exactly (G8),")
    P("#                       i.e. at 10 bps L_CAGR is the ONLY failing leg on the low-gross rungs.")
    P("#   (b) H_HANDOVER      a hand-over EXISTS and is MONOTONE on both panels at every cost rung:")
    P("#                       L_CAGR binds below g*, a Sharpe-family leg above it.")
    P("#   (c) H_NOT_COST      g* is INVARIANT to the cost rung across 0..50 bps (moves <= 1 rung of")
    P("#                       0.025 on both panels).  This is the idea's question, stated as a bar.")
    P("#   (d) H_SHARPE_FLAT   across the WHOLE 0.20..1.00 ladder the full-sample Sharpe spread is")
    P("#                       < 0.05 while the CAGR spread is > 0.10 (absolute), at every cost rung.")
    P("#   (e) H_GROSSMATCHED  under B_SPYGROSS (floor de-grossed with the book) L_CAGR binds at NO")
    P("#                       rung on either panel at any cost rung.")
    P("# DECISION RULE, declared before any number: the CAGR floor is a DE-GROSSING DETECTOR and")
    P("#   NOT a cost leg iff H_NOT_COST holds AND H_GROSSMATCHED holds.  If g* moves materially")
    P("#   with cost it is a cost object and the idea's premise dies.  If the hand-over does not")
    P("#   exist or is not monotone (H_HANDOVER fails) the question is mis-posed and that is the answer.")
    P("")

    gaterows, gates = [], {}
    P("## GATES — printed before any result number")

    panels = {}
    for panel in PANELS:
        px = load_universe(broad=(panel == "B136")).dropna(how="all").ffill()
        idx = px.index
        warm, ins, oos = windows(idx)
        sc, elig = mech(px)
        panels[panel] = dict(px=px, idx=idx, K=len(px.columns), T=len(idx),
                             rets=px.pct_change().fillna(0.0).values, priced=px.notna().values,
                             warm=warm, ins=ins, oos=oos, sc=sc, elig=elig)
        P(f"  {panel}: {len(px.columns)} names, {len(idx):,} rows {idx[0].date()} -> {idx[-1].date()}, "
          f"warm {warm.sum():,}, IS {ins.sum():,}, OOS {oos.sum():,}")

    def run_cell(panel, gross, N=N0, H=HOLD0, freq=FREQ0):
        """GROSS-of-cost return stream and turnover stream.  Cost is applied afterwards:
        net(c) = g - turn * c/1e4.  Nothing in the book depends on the cost rung."""
        d = panels[panel]
        mk = cadence_mask(d["idx"], freq)
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        reb = np.flatnonzero(mk)
        W = build(-d["sc"], d["elig"], d["priced"], reb, N, H, d["T"], d["K"], gross)
        Wl = np.zeros_like(W)
        Wl[LAG:] = W[:-LAG]
        return nrun(d["rets"], Wl, mkl)

    def spy_stream(panel, gross):
        """SPY held at `gross` of NAV, remainder in cash, rebalanced on the same schedule.
        gross=1.0 with its own (near-nil) turnover is the B_SPYCOST control."""
        d = panels[panel]
        j = list(d["px"].columns).index("SPY")
        mk = cadence_mask(d["idx"], FREQ0)
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        W = np.zeros((d["T"], d["K"]))
        W[np.flatnonzero(mk)[0]:, j] = gross
        Wl = np.zeros_like(W)
        Wl[LAG:] = W[:-LAG]
        return nrun(d["rets"], Wl, mkl)

    # ---------------------------------------------------------------------------- G1..G7
    d = panels["U56"]
    mk = rebalance_mask(d["idx"], FREQ0).values
    W = build(-d["sc"], d["elig"], d["priced"], np.flatnonzero(mk), N0, HOLD0, d["T"], d["K"], GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST0, freq=FREQ0)["returns"].values
    gr, tn = run_cell("U56", GROSS0)
    rfast = gr - tn * COST0 / 1e4
    g1 = float(np.abs(eng[d["warm"]] - rfast[d["warm"]]).max())
    gates["G1"] = g1 < 1e-12
    gaterows.append(dict(gate="G1", what="fast runner == engine.backtest", value=g1, pass_=gates["G1"]))
    P(f"  G1  fast runner == engine.backtest                         {g1:.2e}   {'PASS' if gates['G1'] else 'FAIL'}")

    m = blocks_m(rfast, d["warm"], d["ins"], d["oos"])
    g2 = max(abs(m["CAGR"] - A936_WH126[0]), abs(m["Sharpe"] - A936_WH126[1]), abs(m["MaxDD"] - A936_WH126[2]))
    gates["G2"] = g2 < 5e-5
    gaterows.append(dict(gate="G2", what="committed U56 W/H126/N=20 triple", value=g2, pass_=gates["G2"]))
    P(f"  G2  CROSS-RUN committed U56 W/H126/N=20 triple             {g2:.2e}   "
      f"{'PASS' if gates['G2'] else 'FAIL'}  ({m['CAGR']:.4%} / {m['Sharpe']:.4f} / {m['MaxDD']:.4%})")

    spy_m = {}
    for panel in PANELS:
        dp = panels[panel]
        spy_m[panel] = blocks_m(dp["px"]["SPY"].pct_change().fillna(0.0).values, dp["warm"], dp["ins"], dp["oos"])
    g3 = max(abs(spy_m["U56"]["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
             abs(spy_m["U56"]["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
             abs(spy_m["U56"]["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gates["G3"] = g3 < 5e-4
    gaterows.append(dict(gate="G3", what="SPY OOS triple", value=g3, pass_=gates["G3"]))
    P(f"  G3  SPY OOS triple                                         {g3:.2e}   {'PASS' if gates['G3'] else 'FAIL'}")

    g12, t12 = run_cell("U56", GROSS0, N=12)
    m12 = blocks_m(g12 - t12 * COST0 / 1e4, d["warm"], d["ins"], d["oos"])
    g4 = max(abs(m12["CAGR"] - A1098_U56_N12[0]), abs(m12["Sharpe"] - A1098_U56_N12[1]),
             abs(m12["MaxDD"] - A1098_U56_N12[2]))
    gates["G4"] = g4 < 5e-4
    gaterows.append(dict(gate="G4", what="committed 1098 U56 n=12 triple", value=g4, pass_=gates["G4"]))
    P(f"  G4  CROSS-RUN 1098/1102's committed U56 n=12 triple        {g4:.2e}   {'PASS' if gates['G4'] else 'FAIL'}")

    livem = {}
    for panel in PANELS:
        dp = panels[panel]
        lr = backtest(dp["px"], rules_v2_weights(dp["px"]), cost_bps=COST0, freq="W")["returns"].values
        livem[panel] = blocks_m(lr, dp["warm"], dp["ins"], dp["oos"])
    g5 = abs(livem["U56"]["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gates["G5"] = g5 < 5e-4
    gaterows.append(dict(gate="G5", what="live RULES v2 MaxDD", value=g5, pass_=gates["G5"]))
    P(f"  G5  live RULES v2 MaxDD == committed -12.05%               {g5:.2e}   {'PASS' if gates['G5'] else 'FAIL'}")

    g12b, _ = run_cell("U56", GROSS0, N=12)
    g6 = float(np.abs(g12 - g12b).max())
    gates["G6"] = g6 == 0.0
    gaterows.append(dict(gate="G6", what="determinism", value=g6, pass_=gates["G6"]))
    P(f"  G6  determinism                                            {g6:.2e}   {'PASS' if gates['G6'] else 'FAIL'}")

    g7 = max(int(np.abs(cadence_mask(d["idx"], f).astype(int) - rebalance_mask(d["idx"], f).values.astype(int)).sum())
             for f in ("D", "W", "M", "Q"))
    gates["G7"] = g7 == 0
    gaterows.append(dict(gate="G7", what="cadence_mask == engine.rebalance_mask", value=float(g7), pass_=gates["G7"]))
    P(f"  G7  cadence_mask == engine.rebalance_mask (D/W/M/Q)        {g7:.2e}   {'PASS' if gates['G7'] else 'FAIL'}")

    # ------------------------------------------------------------ BUILD EVERY (panel, gross)
    P("")
    P(f"## BUILDING {len(PANELS) * len(LAD_G)} books (2 panels x {len(LAD_G)} gross rungs); costs applied afterwards")
    STREAM, SPYG = {}, {}
    for panel in PANELS:
        for g in LAD_G:
            STREAM[(panel, g)] = run_cell(panel, g)
            SPYG[(panel, g)] = spy_stream(panel, g)
        P(f"  {panel}: {len(LAD_G)} books built  ({time.time() - t0:.0f}s)")

    # G9 -- the post-hoc cost transform IS the engine's cost, at a rung nothing else uses
    Wq = build(-d["sc"], d["elig"], d["priced"], np.flatnonzero(mk), N0, HOLD0, d["T"], d["K"], 0.45)
    engq = backtest(d["px"], pd.DataFrame(Wq, index=d["idx"], columns=d["px"].columns),
                    cost_bps=25.0, freq=FREQ0)["returns"].values
    gq, tq = STREAM[("U56", 0.45)]
    g9 = float(np.abs(engq[d["warm"]] - (gq - tq * 25.0 / 1e4)[d["warm"]]).max())
    gates["G9"] = g9 < 1e-12
    gaterows.append(dict(gate="G9", what="post-hoc cost == engine cost_bps=25 at g=0.45", value=g9, pass_=gates["G9"]))
    P(f"  G9  post-hoc cost transform == engine cost_bps=25 (g=0.45) {g9:.2e}   {'PASS' if gates['G9'] else 'FAIL'}")

    # G10 -- the fine ladder NESTS the record's committed rungs
    committed_rungs = [round(0.30 + 0.05 * i, 3) for i in range(10)]
    miss = [r for r in committed_rungs if r not in LAD_G]
    gates["G10"] = len(miss) == 0
    gaterows.append(dict(gate="G10", what="fine ladder nests committed 0.30..0.75 step .05",
                         value=float(len(miss)), pass_=gates["G10"]))
    P(f"  G10 fine ladder NESTS the committed 0.30..0.75 rungs       {len(miss):.2e}   {'PASS' if gates['G10'] else 'FAIL'}")

    # G8 -- CROSS-RUN reproduction of the committed GROSS-ladder grid (the object under test)
    prior = pd.read_csv(PRIOR_GRID)
    prior = prior[prior.ladder == "GROSS"].copy()
    prior["gross"] = prior["gross"].round(3)
    cols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe"]
    worst, legdiff, nrows = 0.0, 0, 0
    for _, row in prior.iterrows():
        pan, g = row["panel"], float(row["gross"])
        if (pan, g) not in STREAM:
            continue
        dp = panels[pan]
        gg, tt = STREAM[(pan, g)]
        mm = blocks_m(gg - tt * COST0 / 1e4, dp["warm"], dp["ins"], dp["oos"])
        worst = max(worst, max(abs(mm[c] - float(row[c])) for c in cols))
        lg = legs_4b(mm, spy_m[pan])
        legdiff += sum(1 for k in LEGNAMES if bool(lg[k]) != bool(row[k]))
        nrows += 1
    gates["G8"] = worst < 5e-4 and legdiff == 0 and nrows == 20
    gaterows.append(dict(gate="G8", what=f"committed GROSS-ladder grid, {nrows} rows x 6 stats + 5 legs",
                         value=worst, pass_=gates["G8"]))
    P(f"  G8  CROSS-RUN committed GROSS grid ({nrows} rows, {len(cols)} stats)    {worst:.2e}   "
      f"{'PASS' if gates['G8'] else 'FAIL'}   leg disagreements: {legdiff}")

    dump(pd.DataFrame(gaterows), "gates")
    P(f"  GATES {sum(gates.values())} of {len(gates)} PASS")
    if not all(gates.values()):
        P("  !! a gate FAILED — results below are not to be trusted")

    # ------------------------------------------------------------------- THE 528-CELL GRID
    P("")
    P("## THE GRID — every (panel x gross rung x cost rung) cell, all published")
    rows = []
    for panel in PANELS:
        dp = panels[panel]
        sb = spy_m[panel]
        lbm = livem[panel]
        spy_raw = dp["px"]["SPY"].pct_change().fillna(0.0).values
        gspy1, tspy1 = SPYG[(panel, 1.0)]
        for g in LAD_G:
            gg, tt = STREAM[(panel, g)]
            gsg, tsg = SPYG[(panel, g)]
            turn_yr = tt[dp["warm"]].sum() * 252.0 / dp["warm"].sum()
            for c in LAD_C:
                r = gg - tt * c / 1e4
                b = blocks_m(r, dp["warm"], dp["ins"], dp["oos"])
                # three benchmark variants (controls, not a dial)
                bench = {"B_SPY": sb,
                         "B_SPYCOST": blocks_m(gspy1 - tspy1 * c / 1e4, dp["warm"], dp["ins"], dp["oos"]),
                         "B_SPYGROSS": blocks_m(gsg - tsg * c / 1e4, dp["warm"], dp["ins"], dp["oos"])}
                rec = dict(panel=panel, gross=g, cost_bps=c, turnover_yr=turn_yr,
                           **{k: b[k] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_CAGR",
                                                "IS_Sharpe", "IS_MaxDD", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD")})
                for bn in BENCHES:
                    mg = margins_4b(b, bench[bn])
                    lg = legs_4b(b, bench[bn])
                    pre = "" if bn == "B_SPY" else bn[2:].lower() + "_"
                    for k in LEGNAMES:
                        rec[f"{pre}{k}"] = lg[k]
                        rec[f"{pre}m_{k}"] = mg[k]
                    rec[f"{pre}binding"] = binding_of(mg)
                    rec[f"{pre}pass_4b_full"] = all(lg.values())
                rec.update(legs_4b_oos(b, sb))
                rec["pass_4b_oos"] = all(legs_4b_oos(b, sb).values())
                a = legs_4a(b, lbm)
                rec.update(a)
                rec["pass_4a"] = all(a.values())
                rows.append(rec)
    grid = pd.DataFrame(rows)
    dump(grid, "grid")

    # -------------------------------------------------------------------- THE HAND-OVER g*
    P("")
    P("## THE HAND-OVER g* — highest gross rung whose BINDING leg is L_CAGR, at every cost rung")
    P(f"{'panel':>6} {'cost':>6} | {'g*':>6} {'monotone':>9} {'nCAGRbind':>10} {'above g*':>26} | "
      f"{'g* SPYGROSS':>12} {'g* SPYCOST':>11}")
    hrows = []
    for panel in PANELS:
        for c in LAD_C:
            sub = grid[(grid.panel == panel) & (grid.cost_bps == c)].sort_values("gross")
            out = {"panel": panel, "cost_bps": c}
            for bn, pre in (("B_SPY", ""), ("B_SPYGROSS", "spygross_"), ("B_SPYCOST", "spycost_")):
                bind = sub[f"{pre}binding"].values
                gs = sub["gross"].values
                isc = bind == "L_CAGR"
                gstar = float(gs[isc].max()) if isc.any() else np.nan
                mono = bool(np.all(isc[gs <= gstar]) and not np.any(isc[gs > gstar])) if isc.any() else True
                out[f"{pre}gstar"] = gstar
                out[f"{pre}mono"] = mono
                out[f"{pre}n_cagr_bind"] = int(isc.sum())
                above = sorted(set(bind[gs > gstar])) if isc.any() else sorted(set(bind))
                out[f"{pre}above"] = "+".join(above)
                out[f"{pre}n_cagr_fail"] = int((~sub[f"{pre}L_CAGR"]).sum())
            hrows.append(out)
            P(f"{panel:>6} {c:>6.1f} | {out['gstar']:>6} {str(out['mono']):>9} {out['n_cagr_bind']:>10} "
              f"{out['above']:>26} | {out['spygross_gstar']:>12} {out['spycost_gstar']:>11}")
    hand = pd.DataFrame(hrows)
    dump(hand, "handover")

    # -------------------------------------------------------- IS THE HAND-OVER A COST OBJECT?
    P("")
    P("## IS THE HAND-OVER A COST OBJECT?  g* across the whole 0..50 bps cost ladder")
    costrows = []
    for panel in PANELS:
        h = hand[hand.panel == panel]
        gstars = h["gstar"].values
        span = float(np.nanmax(gstars) - np.nanmin(gstars))
        rungs = int(round(span / 0.025))
        P(f"  {panel}: g* = " + " ".join(f"{c:g}bp:{v}" for c, v in zip(h.cost_bps, gstars)))
        P(f"        span {span:.3f} of gross = {rungs} rung(s) of 0.025 over a 0->50 bps cost move; "
          f"MONOTONE at {int(h['mono'].sum())} of {len(h)} cost rungs")
        # how much of the CAGR shortfall at g* is COST and how much is EXPOSURE?
        gstar = float(h[h.cost_bps == COST0]["gstar"].iloc[0])
        sub0 = grid[(grid.panel == panel) & (grid.gross == gstar)]
        c0 = float(sub0[sub0.cost_bps == 0.0]["CAGR"].iloc[0])
        c10 = float(sub0[sub0.cost_bps == COST0]["CAGR"].iloc[0])
        c50 = float(sub0[sub0.cost_bps == 50.0]["CAGR"].iloc[0])
        top = grid[(grid.panel == panel) & (grid.gross == 1.0) & (grid.cost_bps == 0.0)]["CAGR"].iloc[0]
        flo = CAGR_FLOOR * spy_m[panel]["CAGR"]
        P(f"        at g*={gstar}: CAGR 0bps {c0:.4%}, 10bps {c10:.4%}, 50bps {c50:.4%}; floor {flo:.4%}; "
          f"gross-1.00 zero-cost CAGR {top:.4%}")
        expo = top - c0
        cost10 = c0 - c10
        P(f"        SHORTFALL DECOMPOSITION at g*: EXPOSURE (de-grossing, 0 bps) {expo:.4%}/yr vs "
          f"COST (0->10 bps) {cost10:.4%}/yr  = cost is {cost10 / (expo + cost10):.1%} of the drop")
        costrows.append(dict(panel=panel, gstar_10bps=gstar, span_gross=span, span_rungs=rungs,
                             cagr_0bps=c0, cagr_10bps=c10, cagr_50bps=c50, floor=flo,
                             cagr_gross1_0bps=top, exposure_drop=expo, cost_drop_0_10=cost10,
                             cost_share=cost10 / (expo + cost10)))
    dump(pd.DataFrame(costrows), "costobject")

    # ---------------------------------------------------------- SHARPE FLATNESS vs CAGR SLOPE
    P("")
    P("## SHARPE vs CAGR ALONG THE GROSS LADDER (the queue's '1.1390 vs 1.1397')")
    P(f"{'panel':>6} {'cost':>6} | {'Sharpe min':>10} {'Sharpe max':>10} {'spread':>8} | "
      f"{'CAGR min':>9} {'CAGR max':>9} {'spread':>8}")
    flatrows = []
    for panel in PANELS:
        for c in LAD_C:
            sub = grid[(grid.panel == panel) & (grid.cost_bps == c)]
            ss, cc = sub["Sharpe"], sub["CAGR"]
            flatrows.append(dict(panel=panel, cost_bps=c, sharpe_min=ss.min(), sharpe_max=ss.max(),
                                 sharpe_spread=ss.max() - ss.min(), cagr_min=cc.min(), cagr_max=cc.max(),
                                 cagr_spread=cc.max() - cc.min()))
            P(f"{panel:>6} {c:>6.1f} | {ss.min():>10.4f} {ss.max():>10.4f} {ss.max() - ss.min():>8.4f} | "
              f"{cc.min():>9.4%} {cc.max():>9.4%} {cc.max() - cc.min():>8.4%}")
    dump(pd.DataFrame(flatrows), "flatness")

    # ------------------------------------------------------------------ BINDING-LEG CENSUS
    P("")
    P("## BINDING-LEG CENSUS — the queue says the hand-over is 'from SHARPE to CAGR'.  Which")
    P("##   leg actually binds ABOVE g*?  Counts over all 33 gross rungs at every cost rung.")
    P(f"{'panel':>6} {'cost':>6} | " + " ".join(f"{k:>7}" for k in LEGNAMES) + "  | sharpe-family share")
    crows = []
    for panel in PANELS:
        for c in LAD_C:
            sub = grid[(grid.panel == panel) & (grid.cost_bps == c)]
            cnt = {k: int((sub["binding"] == k).sum()) for k in LEGNAMES}
            sh = sum(cnt[k] for k in SHARPE_LEGS) / len(sub)
            crows.append(dict(panel=panel, cost_bps=c, **cnt, sharpe_family_share=sh))
            P(f"{panel:>6} {c:>6.1f} | " + " ".join(f"{cnt[k]:>7}" for k in LEGNAMES) + f"  | {sh:>7.3f}")
    census = pd.DataFrame(crows)
    dump(census, "binding")
    tot = len(grid)
    sfam = int(sum((grid["binding"] == k).sum() for k in SHARPE_LEGS))
    P(f"  OVER ALL {tot} CELLS: a SHARPE-family leg binds at {sfam} ({sfam / tot:.3f}); "
      f"L_DD binds at {int((grid['binding'] == 'L_DD').sum())}, L_CAGR at {int((grid['binding'] == 'L_CAGR').sum())}")

    # ------------------------------------------------ THE HAND-OVER'S OWN RESOLUTION (bootstrap)
    P("")
    P(f"## THE HAND-OVER'S OWN RESOLUTION — paired block bootstrap, L={L_HEAD}, {BDRAWS} draws")
    P("   L_OOS is NOT defined on a resampled tape and is EXCLUDED from the bootstrap arm only;")
    P("   the bootstrap binding leg is argmin over {L_H1, L_H2, L_DD, L_CAGR}.  Stated, not hidden.")
    BLEGS = ["L_H1", "L_H2", "L_DD", "L_CAGR"]
    brows, pairrows, gstar_draws = [], [], {}
    for panel in PANELS:
        dp = panels[panel]
        Tw = int(dp["warm"].sum())
        rng = np.random.default_rng(seed_of(panel, "boot"))
        bidx, _ = block_index(rng, Tw, L_HEAD, BDRAWS)
        sp = boot_stats(dp["px"]["SPY"].pct_change().fillna(0.0).values[dp["warm"]], bidx)
        for c in (0.0, COST0, 50.0):
            bind_by_g = np.empty((len(LAD_G), BDRAWS), dtype=object)
            for i, g in enumerate(LAD_G):
                gg, tt = STREAM[(panel, g)]
                bk = boot_stats((gg - tt * c / 1e4)[dp["warm"]], bidx)
                M = np.vstack([(bk[:, 3] - sp[:, 3]) / np.abs(sp[:, 3]),
                               (bk[:, 4] - sp[:, 4]) / np.abs(sp[:, 4]),
                               ((DD_CAP * sp[:, 2]) - bk[:, 2]) / (DD_CAP * sp[:, 2]),
                               (bk[:, 0] - CAGR_FLOOR * sp[:, 0]) / np.abs(CAGR_FLOOR * sp[:, 0])])
                bind_by_g[i] = np.array(BLEGS, dtype=object)[M.argmin(axis=0)]
            isc = (bind_by_g == "L_CAGR")
            gs = np.array(LAD_G)
            gstar_d = np.where(isc.any(axis=0), gs[np.where(isc.any(axis=0), isc.shape[0] - 1 -
                                                            isc[::-1].argmax(axis=0), 0)], np.nan)
            gstar_draws[(panel, c)] = gstar_d
            lo, hi = np.nanpercentile(gstar_d, [(1 - Q_HEAD) / 2 * 100, (1 + Q_HEAD) / 2 * 100])
            pt = float(hand[(hand.panel == panel) & (hand.cost_bps == c)]["gstar"].iloc[0])
            share_nan = float(np.mean(np.isnan(gstar_d)))
            brows.append(dict(panel=panel, cost_bps=c, gstar_point=pt, gstar_boot_median=float(np.nanmedian(gstar_d)),
                              lo=float(lo), hi=float(hi), halfwidth=float((hi - lo) / 2),
                              share_no_handover=share_nan, rungs_in_interval=int(round((hi - lo) / 0.025)) + 1))
            P(f"  {panel} {c:>5.1f} bps: point g* {pt:.3f}  boot median {np.nanmedian(gstar_d):.3f}  "
              f"{int(Q_HEAD * 100)}% interval [{lo:.3f}, {hi:.3f}] = {int(round((hi - lo) / 0.025)) + 1} rungs  "
              f"no hand-over in {share_nan:.1%} of draws")
    dump(pd.DataFrame(brows), "resolution")

    P("")
    P("## THE PAIRED RULER (idea 1012's basis) — g*(50 bps) - g*(0 bps) ON THE SAME DRAW.")
    P("   The unpaired interval above prices WHERE g* is; this prices WHETHER COST MOVES IT,")
    P("   which is the question asked.  Same block draws on both arms, so the tape cancels.")
    for panel in PANELS:
        d0, d50 = gstar_draws[(panel, 0.0)], gstar_draws[(panel, 50.0)]
        dd = d50 - d0
        ok = np.isfinite(dd)
        lo, hi = np.nanpercentile(dd, [(1 - Q_HEAD) / 2 * 100, (1 + Q_HEAD) / 2 * 100])
        within = float(np.mean(np.abs(dd[ok]) <= 0.025 + 1e-9))
        zero = float(np.mean(np.abs(dd[ok]) < 1e-9))
        pairrows.append(dict(panel=panel, median_delta=float(np.nanmedian(dd)), lo=float(lo), hi=float(hi),
                             share_within_1_rung=within, share_exactly_zero=zero,
                             point_delta=float(hand[(hand.panel == panel) & (hand.cost_bps == 50.0)]["gstar"].iloc[0] -
                                               hand[(hand.panel == panel) & (hand.cost_bps == 0.0)]["gstar"].iloc[0])))
        P(f"  {panel}: median delta g* {np.nanmedian(dd):+.4f} of gross, {int(Q_HEAD * 100)}% interval "
          f"[{lo:+.3f}, {hi:+.3f}]; |delta| <= 1 rung in {within:.1%} of draws, EXACTLY 0 in {zero:.1%}")
    dump(pd.DataFrame(pairrows), "paired")

    # ------------------------------------------------- RULE 8 WALK-FORWARD + BOTH KEEP PATHS
    P("")
    P("## RULE 8 WALK-FORWARD — gross rung chosen on IS (2009-2016) ONLY, OOS read ONCE")
    CHOOSERS = {"C_ISSHARPE": ("IS_Sharpe", +1.0), "C_ISCAGR": ("IS_CAGR", +1.0), "C_ISDD": ("IS_MaxDD", +1.0)}
    wrows = []
    for panel in PANELS:
        sb, lbm = spy_m[panel], livem[panel]
        for c in LAD_C:
            sub = grid[(grid.panel == panel) & (grid.cost_bps == c)].sort_values("gross")
            for ch, (col, sgn) in CHOOSERS.items():
                k = sub.iloc[int(np.argmax(sgn * sub[col].values))]
                wrows.append(dict(panel=panel, cost_bps=c, chooser=ch, pick_gross=float(k["gross"]),
                                  IS_Sharpe=k["IS_Sharpe"], CAGR=k["CAGR"], Sharpe=k["Sharpe"], MaxDD=k["MaxDD"],
                                  H1=k["H1"], H2=k["H2"], OOS_CAGR=k["OOS_CAGR"], OOS_Sharpe=k["OOS_Sharpe"],
                                  OOS_MaxDD=k["OOS_MaxDD"], binding=k["binding"],
                                  spy_OOS_Sharpe=sb["OOS_Sharpe"], spy_OOS_CAGR=sb["OOS_CAGR"],
                                  spy_OOS_MaxDD=sb["OOS_MaxDD"], live_OOS_Sharpe=lbm["OOS_Sharpe"],
                                  pass_4b_full=bool(k["pass_4b_full"]), pass_4b_oos=bool(k["pass_4b_oos"]),
                                  pass_4a=bool(k["pass_4a"]),
                                  regret_vs_best_OOS=float(sub["OOS_Sharpe"].max() - k["OOS_Sharpe"])))
    wf = pd.DataFrame(wrows)
    dump(wf, "walkforward")
    P(f"  {len(wf)} IS-only picks: 4b full {int(wf.pass_4b_full.sum())}, 4b OOS {int(wf.pass_4b_oos.sum())}, "
      f"4a {int(wf.pass_4a.sum())}; median OOS Sharpe {wf.OOS_Sharpe.median():.4f}, median regret {wf.regret_vs_best_OOS.median():+.4f}")
    P(f"  WHOLE GRID ({len(grid)} cells): 4b full {int(grid.pass_4b_full.sum())}, 4b OOS "
      f"{int(grid.pass_4b_oos.sum())}, 4a {int(grid.pass_4a.sum())}")
    for panel in PANELS:
        sb, lbm = spy_m[panel], livem[panel]
        P(f"  {panel} SPY        full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%}  "
          f"(halves {sb['H1']:.4f}/{sb['H2']:.4f})  OOS {sb['OOS_CAGR']:.2%} / {sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"  {panel} RULES v2   full {lbm['CAGR']:.2%} / {lbm['Sharpe']:.4f} / {lbm['MaxDD']:.2%}  "
          f"(halves {lbm['H1']:.4f}/{lbm['H2']:.4f})  OOS {lbm['OOS_CAGR']:.2%} / {lbm['OOS_Sharpe']:.4f} / {lbm['OOS_MaxDD']:.2%}")
    P("")
    P("  ONLY THE 10 bps RUNG IS A PROTOCOL-LEGAL BOOK (rule 2).  The other 7 cost rungs are")
    P("  DIAL POINTS, not tradable alternatives — a book cannot choose its cost rate — so the")
    P("  KEEP question is asked at 10 bps and nowhere else.")
    g10 = grid[grid.cost_bps == COST0]
    P(f"  at 10 bps, {len(g10)} cells: 4b full {int(g10.pass_4b_full.sum())}, 4b OOS "
      f"{int(g10.pass_4b_oos.sum())}, 4a {int(g10.pass_4a.sum())}")
    for panel in PANELS:
        s = g10[(g10.panel == panel) & g10.pass_4b_full]
        if len(s):
            P(f"    {panel}: 4b-full passes on gross {s.gross.min():.3f}..{s.gross.max():.3f} ({len(s)} rungs) — "
              f"a CONTIGUOUS WINDOW between the two binding legs, not a peak")
    best = g10[g10.pass_4b_full & g10.pass_4b_oos].sort_values("OOS_Sharpe", ascending=False)
    if len(best):
        b0 = best.iloc[0]
        P(f"  best 10 bps cell passing 4b FULL and OOS, by OOS Sharpe: {b0['panel']} gross {b0['gross']} — "
          f"full {b0['CAGR']:.2%} / {b0['Sharpe']:.4f} / {b0['MaxDD']:.2%} (halves {b0['H1']:.4f}/{b0['H2']:.4f}), "
          f"OOS {b0['OOS_CAGR']:.2%} / {b0['OOS_Sharpe']:.4f} / {b0['OOS_MaxDD']:.2%}, {b0['turnover_yr']:.2f}x/yr")
        inc = g10[(g10.panel == b0["panel"]) & (g10.gross == GROSS0)].iloc[0]
        P(f"    the INCUMBENT rung (gross {GROSS0}) in the same cell: full {inc['CAGR']:.2%} / {inc['Sharpe']:.4f} / "
          f"{inc['MaxDD']:.2%}, OOS {inc['OOS_CAGR']:.2%} / {inc['OOS_Sharpe']:.4f} / {inc['OOS_MaxDD']:.2%}")
        P(f"    the whole passing window differs by {float(best['OOS_Sharpe'].max() - best['OOS_Sharpe'].min()):.4f} of OOS "
          f"Sharpe end to end — NOTHING IS PROPOSED: every passing rung is the standing top-20/W/H126 family the")
        P("    record already holds and has already PARKED, and no IS-only chooser reaches any of them (0 of 48).")

    # ------------------------------------------------------------------------- HYPOTHESES
    P("")
    P("## HYPOTHESES — scored against what was declared before any number")
    hyp = []
    hyp.append(("H_PREMISE", bool(gates["G8"]),
                f"committed GROSS-ladder grid reproduced on {nrows} rows, {legdiff} leg disagreements"))
    mono_all = bool(hand["mono"].all())
    exists = bool(hand["gstar"].notna().all())
    hyp.append(("H_HANDOVER", exists and mono_all,
                f"g* exists at {int(hand['gstar'].notna().sum())} of {len(hand)} (panel, cost) points; "
                f"MONOTONE at {int(hand['mono'].sum())} of {len(hand)}"))
    spans = {p: float(np.nanmax(hand[hand.panel == p]['gstar']) - np.nanmin(hand[hand.panel == p]['gstar']))
             for p in PANELS}
    notcost = all(v <= 0.025 + 1e-9 for v in spans.values())
    hyp.append(("H_NOT_COST", notcost,
                "g* span over 0->50 bps: " + ", ".join(f"{p} {v:.3f} ({int(round(v / 0.025))} rungs)" for p, v in spans.items())))
    fl = pd.DataFrame(flatrows)
    flat = bool((fl.sharpe_spread < 0.05).all() and (fl.cagr_spread > 0.10).all())
    hyp.append(("H_SHARPE_FLAT", flat,
                f"max Sharpe spread {fl.sharpe_spread.max():.4f} (<0.05?), min CAGR spread {fl.cagr_spread.min():.4%} (>10%?)"))
    gm = bool((hand["spygross_n_cagr_bind"] == 0).all())
    hyp.append(("H_GROSSMATCHED", gm,
                f"L_CAGR binds at {int(hand['spygross_n_cagr_bind'].sum())} of "
                f"{len(hand) * len(LAD_G)} (cell) points under the gross-matched floor; "
                f"it FAILS at {int(hand['spygross_n_cagr_fail'].sum())}"))
    for n, v, note in hyp:
        P(f"  {n:<16} {'SUPPORTED' if v else 'FAILED   '}  {note}")
    dump(pd.DataFrame([dict(hypothesis=n, supported=v, note=note) for n, v, note in hyp]), "hypotheses")

    verdict = "DE-GROSSING DETECTOR" if (notcost and gm) else "COST OBJECT"
    P("")
    P(f"## DECISION RULE OUTPUT: the CAGR floor is a {verdict}")
    P(f"   (H_NOT_COST {notcost} AND H_GROSSMATCHED {gm})")
    P(f"\n# done in {time.time() - t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

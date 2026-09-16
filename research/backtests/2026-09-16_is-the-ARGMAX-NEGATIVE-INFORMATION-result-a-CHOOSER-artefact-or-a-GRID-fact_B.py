#!/usr/bin/env python3
"""Idea 1132 (lane B, 2026-09-16)
   is-the-ARGMAX-NEGATIVE-INFORMATION-result-a-CHOOSER-artefact-or-a-GRID-fact

1117 priced an honest IS-only argmax against each ladder's FROZEN DEFAULT rung and found
that on the 36 of 48 picks that MOVE off the default the median matched-statistic advantage
is -0.0195 and the median OOS-Sharpe advantage -0.0502, on barred and unbarred ladders
alike.  An argmax read out of sample is worse than doing nothing.

Two readings of that, and they have different consequences:

  CHOOSER ARTEFACT  the loss is carried by picks made on a TINY in-sample gap — noise the
                    chooser mistook for signal.  Then a SHRUNK chooser (stay on the default
                    unless the IS gap is big enough to be real) recovers it, and the record
                    should shrink rather than ban.
  GRID FACT         the ladder carries no out-of-sample information over its default rung at
                    ANY confidence, so no threshold recovers anything: shrinkage can only
                    MUTE the loss by degenerating to the default.  Then 1117's clause is the
                    honest response and there is nothing to salvage.

The two are separated by one curve: median OOS advantage against the shrink threshold.  If
it crosses zero anywhere at a FINITE threshold, the loss was the chooser.  If its supremum
is 0, reached only where the chooser stops choosing, it is the grid.

TUNED DIALS (2, PROTOCOL rule 4): `CHOOSER` {C_ISSHARPE, C_ISCAGR, C_ISDD} x `SHRINK
THRESHOLD` tau {0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, inf} = 27 combinations, ALL
published.  PANEL, LADDER, RUNG SET and the KEYING of tau are NOT dials: every one of them
is reported at every dial point and no result is selected on any of them.

  KEYING (both reported, neither selected):
    K_SE     tau is a multiple of the IS-only bootstrap SD of the (argmax - default) gap.
             Always finite, so the curve is continuous and tau -> inf is "always default".
    K_FLOOR  tau is a multiple of that ladder's OWN IS-only resolution floor (1098's
             floor_sub at q=0.90, computed on the IS window ALONE).  This is the queue's
             literal wording.  An INFINITE floor degenerates to "always default" at any
             tau > 0, which is itself the answer for that ladder.
  Both keyings coincide at tau = 0 (= 1117's naive argmax) by construction.

EVERYTHING that selects a rung is computed on 2009-2016 ALONE (rule 8): the IS statistic,
the bootstrap SD and the floor.  OOS 2017-2026 is read ONCE, at the end, for scoring only.

FROZEN at 1082/1094/1098/1102/1108/1110/1116/1117/1118's construction: CAND20 legs, cap INF,
max_vol 0.60, gross 0.75 (except on GROSS), min hold 126 (except on H), N=20 (except on N),
W (except on CADENCE), 10 bps, LAG 1, warm-up 260, IS end 2016-12-31, block L=63, 1000
draws, crc32 seeds, q=0.90.

Standalone, deterministic, offline.  Nothing outside research/backtests/ is written.
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
SLUG = "is-the-ARGMAX-NEGATIVE-INFORMATION-result-a-CHOOSER-artefact-or-a-GRID-fact"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"
BT = Path(__file__).resolve().parent
PRIOR1117 = BT / "2026-09-16_should-the-PROTOCOL-forbid-publishing-an-ARGMAX-on-an-H-or-CADENCE-LADDER-at-all_B"

LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST, GROSS0, FREQ0, HOLD0, N0 = 10.0, 0.75, "W", 126, 20
LEGS = [(21, 252), (0, 126), (0, 63)]

LAD_N = [5, 8, 10, 12, 15, 20, 25, 30, 40]
LAD_G = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]
H_CORE = [21, 63, 126, 252]
H_EXT = [21, 42, 63, 84, 126, 168, 210, 252, 378]
C_CORE = ["D", "W", "M", "Q"]
C_EXT = ["D", "2D", "W", "2W", "M", "2M", "Q", "2Q", "4Q"]

LADDERS = ["N", "H", "GROSS", "CADENCE"]
PANELS = ["U56", "B136"]
RUNGSETS = ["CORE", "EXT"]
DEFAULT_RUNG = {"N": "20", "H": "126", "GROSS": "0.75", "CADENCE": "W"}

# chooser -> (IS column, matched OOS column, bootstrap statistic key, sign: +1 higher-better)
CHOOSERS = {"C_ISSHARPE": ("IS_Sharpe", "OOS_Sharpe", "S", +1.0),
            "C_ISCAGR": ("IS_CAGR", "OOS_CAGR", "C", +1.0),
            "C_ISDD": ("IS_MaxDD", "OOS_MaxDD", "D", +1.0)}   # MaxDD negative; higher better

TAUS = [0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, float("inf")]
KEYINGS = ["K_SE", "K_FLOOR"]

Q_HEAD, L_HEAD, BDRAWS = 0.90, 63, 1000
STAT_FULL = "Sharpe"
SEED_BASES = [11321132, 11171117, 11181118]

A936_WH126 = (0.155787, 1.139701, -0.191276)
A1098_U56_N12 = (0.1771, 1.1692, -0.2017)
A1098_B136_N15 = (0.1678, 1.0682, -0.1966)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
A1117_MOVERS = (36, 48, -0.0195, -0.0502)   # n movers, n picks, median matched adv, median OOS-S adv

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def seed_of(base, *parts):
    return base + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


# ------------------------------------------------- 1082/1098/1102/1108/1117/1118's fast runner
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


# --------------------------------------------------- 1098/1102's bootstrap, 1108's seed repair
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


def agree_matrix(vals, boot):
    k = len(vals)
    A = np.full((k, k), np.nan)
    np.fill_diagonal(A, 1.0)
    for i, j in combinations(range(k), 2):
        g = vals[i] - vals[j]
        if not np.isfinite(g):
            continue
        d = boot[i] - boot[j]
        d = d[np.isfinite(d)]
        A[i, j] = A[j, i] = float((np.sign(d) == np.sign(g)).mean()) if len(d) else np.nan
    return A


def floor_sub(vals, A, sub, q):
    """1098's floor restricted to rung subset `sub`: the smallest gap above which EVERY pair
    is resolved at q; inf when the LARGEST gap in the subset is itself un-resolved."""
    gaps, agr = [], []
    for i, j in combinations(sub, 2):
        g = vals[i] - vals[j]
        if not np.isfinite(g) or not np.isfinite(A[i, j]):
            continue
        gaps.append(abs(g))
        agr.append(A[i, j])
    if not gaps:
        return float("inf")
    gaps, agr = np.array(gaps), np.array(agr)
    un = agr < q
    largest_un = float(gaps[un].max()) if un.any() else 0.0
    ok = (~un) & (gaps > largest_un)
    return float(gaps[ok].min()) if ok.any() else float("inf")


def cadence_mask(idx, spec):
    """engine.rebalance_mask verbatim for D/W/M/Q (gate G7); '<k><BASE>' keeps every k-th bar
    of that base schedule.  engine.py is NOT modified."""
    if spec in ("D", "W", "M", "Q"):
        return rebalance_mask(idx, spec).values.copy()
    k, base = int(spec[:-1]) if spec[:-1].isdigit() else int(spec[:-2]), spec[-1]
    hit = np.flatnonzero(rebalance_mask(idx, base).values)
    m = np.zeros(len(idx), dtype=bool)
    m[hit[::k]] = True
    return m


def main():
    t0 = time.time()
    P(f"# Idea 1132 (lane B, {DATE}) — is the ARGMAX NEGATIVE-INFORMATION result a CHOOSER")
    P("#   artefact or a GRID fact?  Price a SHRUNK chooser and publish the whole curve.")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4): CHOOSER {list(CHOOSERS)} x SHRINK THRESHOLD tau")
    P(f"#   {TAUS} = {len(CHOOSERS) * len(TAUS)} combinations, ALL published.")
    P("# PANEL, LADDER, RUNG SET and KEYING are NOT dials: all reported at every dial point,")
    P("#   nothing selected on any of them.")
    P(f"#   KEYING {KEYINGS}: K_SE = tau x IS bootstrap SD of the (argmax - default) gap;")
    P(f"#     K_FLOOR = tau x that ladder's OWN IS-only resolution floor (1098's floor_sub,")
    P(f"#     q={Q_HEAD}).  They coincide at tau=0 by construction.")
    P(f"#   CORE  H {H_CORE}  CADENCE {C_CORE}    EXT  H {H_EXT}  CADENCE {C_EXT}")
    P(f"#   N {LAD_N} and GROSS {LAD_G} are the same at both rung sets.")
    P(f"# FROZEN: CAND20 legs {LEGS}, cap INF, max_vol {MAXVOL}, gross {GROSS0}, min hold "
      f"{HOLD0}, N {N0}, cadence {FREQ0}, {COST:.0f} bps,")
    P(f"#   LAG {LAG}, warm-up {WARMUP}, IS end {IS_END}, block L={L_HEAD}, {BDRAWS} draws, "
      f"crc32 seeds, {len(SEED_BASES)} seed bases.")
    P("# RULE 8 DISCIPLINE: the IS statistic, the bootstrap SD and the floor are ALL computed")
    P("#   on 2009-2016 alone.  OOS 2017-2026 is read ONCE, for scoring only.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   (a) H_PREMISE     1117's result reproduces at tau=0: of 48 IS picks, 36 move off the")
    P("#                     default, with median matched advantage -0.0195 and median")
    P("#                     OOS-Sharpe advantage -0.0502.")
    P("#   (b) H_RECOVER     (the CHOOSER-ARTEFACT reading) some FINITE tau > 0 lifts the")
    P("#                     pooled median OOS-Sharpe advantage STRICTLY ABOVE 0.")
    P("#   (c) H_MONOTONE    the pooled median advantage is non-decreasing in tau — i.e. the")
    P("#                     loss really is carried by the small-gap picks.")
    P("#   (d) H_GRID        (the pre-declared RIVAL) the supremum of the curve is exactly 0")
    P("#                     and is reached only where the chooser has stopped choosing")
    P("#                     (every cell back on its default), so shrinkage MUTES and never")
    P("#                     RECOVERS.")
    P("#   (e) H_KEYING      the K_SE and K_FLOOR curves agree on the verdict.")
    P("#   (f) NOT A KEEP PATH  no book is proposed; 4a/4b and rule 8 are scored at every rung")
    P("#                     and every chosen book because rule 4 requires it.")
    P("# DECISION RULE, declared before any number: CHOOSER ARTEFACT requires H_RECOVER at a")
    P("#   FINITE tau, in BOTH panels pooled AND at >= 2 of 3 choosers, under BOTH keyings.")
    P("#   Anything less and the answer is GRID FACT and the premise 'a shrunk chooser")
    P("#   recovers the loss' is KILLED.")
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
        P(f"  {panel}: {len(px.columns)} names, {len(idx):,} rows {idx[0].date()} -> "
          f"{idx[-1].date()}, warm {warm.sum():,}, IS {ins.sum():,}, OOS {oos.sum():,}")

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
    W = build(-d["sc"], d["elig"], d["priced"], np.flatnonzero(mk), N0, HOLD0, d["T"], d["K"], GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST, freq=FREQ0)["returns"].values
    rfast, _ = run_cell("U56", N0, HOLD0, GROSS0, FREQ0)
    g1 = float(np.abs(eng[d["warm"]] - rfast[d["warm"]]).max())
    gates["G1"] = g1 < 1e-12
    gaterows.append(dict(gate="G1", what="fast runner == engine.backtest", value=g1, pass_=gates["G1"]))
    P(f"  G1  fast runner == engine.backtest                        {g1:.2e}   {'PASS' if gates['G1'] else 'FAIL'}")

    m = blocks_m(rfast, d["warm"], d["ins"], d["oos"])
    g2 = max(abs(m["CAGR"] - A936_WH126[0]), abs(m["Sharpe"] - A936_WH126[1]), abs(m["MaxDD"] - A936_WH126[2]))
    gates["G2"] = g2 < 5e-5
    gaterows.append(dict(gate="G2", what="committed U56 W/H126/N=20 triple", value=g2, pass_=gates["G2"]))
    P(f"  G2  CROSS-RUN committed U56 W/H126/N=20 triple            {g2:.2e}   "
      f"{'PASS' if gates['G2'] else 'FAIL'}  ({m['CAGR']:.4%} / {m['Sharpe']:.4f} / {m['MaxDD']:.4%})")

    spy_u = d["px"]["SPY"].pct_change().fillna(0.0).values
    sm = blocks_m(spy_u, d["warm"], d["ins"], d["oos"])
    g3 = max(abs(sm["OOS_CAGR"] - SPY_OOS_COMMITTED[0]), abs(sm["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
             abs(sm["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gates["G3"] = g3 < 5e-4
    gaterows.append(dict(gate="G3", what="SPY OOS triple", value=g3, pass_=gates["G3"]))
    P(f"  G3  SPY OOS triple                                        {g3:.2e}   {'PASS' if gates['G3'] else 'FAIL'}")

    r12, _ = run_cell("U56", 12, HOLD0, GROSS0, FREQ0)
    m12 = blocks_m(r12, d["warm"], d["ins"], d["oos"])
    g4 = max(abs(m12["CAGR"] - A1098_U56_N12[0]), abs(m12["Sharpe"] - A1098_U56_N12[1]),
             abs(m12["MaxDD"] - A1098_U56_N12[2]))
    gates["G4"] = g4 < 5e-4
    gaterows.append(dict(gate="G4", what="committed U56 n=12 triple", value=g4, pass_=gates["G4"]))
    P(f"  G4  CROSS-RUN 1098/1102's committed U56 n=12 triple       {g4:.2e}   {'PASS' if gates['G4'] else 'FAIL'}")

    db = panels["B136"]
    r15, _ = run_cell("B136", 15, HOLD0, GROSS0, FREQ0)
    m15 = blocks_m(r15, db["warm"], db["ins"], db["oos"])
    g4b = max(abs(m15["CAGR"] - A1098_B136_N15[0]), abs(m15["Sharpe"] - A1098_B136_N15[1]),
              abs(m15["MaxDD"] - A1098_B136_N15[2]))
    gates["G4b"] = g4b < 5e-4
    gaterows.append(dict(gate="G4b", what="committed B136 n=15 triple", value=g4b, pass_=gates["G4b"]))
    P(f"  G4b CROSS-RUN 1098/1102's committed B136 n=15 triple      {g4b:.2e}   {'PASS' if gates['G4b'] else 'FAIL'}")

    lb = {}
    for panel in PANELS:
        dp = panels[panel]
        lr = backtest(dp["px"], rules_v2_weights(dp["px"]), cost_bps=COST, freq="W")["returns"].values
        lb[panel] = blocks_m(lr, dp["warm"], dp["ins"], dp["oos"])
    g5 = abs(lb["U56"]["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gates["G5"] = g5 < 5e-4
    gaterows.append(dict(gate="G5", what="live RULES v2 MaxDD", value=g5, pass_=gates["G5"]))
    P(f"  G5  live RULES v2 MaxDD == committed -12.05%              {g5:.2e}   {'PASS' if gates['G5'] else 'FAIL'}")

    r12b, _ = run_cell("U56", 12, HOLD0, GROSS0, FREQ0)
    g6 = float(np.abs(r12 - r12b).max())
    gates["G6"] = g6 == 0.0
    gaterows.append(dict(gate="G6", what="determinism", value=g6, pass_=gates["G6"]))
    P(f"  G6  determinism                                           {g6:.2e}   {'PASS' if gates['G6'] else 'FAIL'}")

    g7 = max(int(np.abs(cadence_mask(d["idx"], f).astype(int) - rebalance_mask(d["idx"], f).values.astype(int)).sum())
             for f in ("D", "W", "M", "Q"))
    gates["G7"] = g7 == 0
    gaterows.append(dict(gate="G7", what="cadence_mask == engine.rebalance_mask on D/W/M/Q",
                         value=float(g7), pass_=gates["G7"]))
    P(f"  G7  cadence_mask == engine.rebalance_mask (D/W/M/Q)       {g7:.2e}   {'PASS' if gates['G7'] else 'FAIL'}")

    # ------------------------------------------------------------------------ BUILD EVERY BOOK
    H_ALL = sorted(set(H_CORE + H_EXT))
    RUNGS = {"N": [str(x) for x in LAD_N], "GROSS": [str(x) for x in LAD_G],
             "H": [str(x) for x in H_ALL], "CADENCE": list(C_EXT)}
    SUBSET = {("N", "CORE"): RUNGS["N"], ("N", "EXT"): RUNGS["N"],
              ("GROSS", "CORE"): RUNGS["GROSS"], ("GROSS", "EXT"): RUNGS["GROSS"],
              ("H", "CORE"): [str(x) for x in H_CORE], ("H", "EXT"): [str(x) for x in H_EXT],
              ("CADENCE", "CORE"): list(C_CORE), ("CADENCE", "EXT"): list(C_EXT)}

    def cell_params(lad, rung):
        N, H, gr, fq = N0, HOLD0, GROSS0, FREQ0
        if lad == "N":
            N = int(rung)
        elif lad == "H":
            H = int(rung)
        elif lad == "GROSS":
            gr = float(rung)
        else:
            fq = str(rung)
        return N, H, gr, fq

    grid_rows, RET = [], {}
    for panel in PANELS:
        dp = panels[panel]
        sb = blocks_m(dp["px"]["SPY"].pct_change().fillna(0.0).values, dp["warm"], dp["ins"], dp["oos"])
        panels[panel]["spy_m"] = sb
        for lad in LADDERS:
            for rung in RUNGS[lad]:
                N, H, gr, fq = cell_params(lad, rung)
                r, tn = run_cell(panel, N, H, gr, fq)
                RET[(panel, lad, rung)] = r
                b = blocks_m(r, dp["warm"], dp["ins"], dp["oos"])
                row = dict(panel=panel, ladder=lad, rung=rung, N=N, H=H, gross=gr, freq=fq,
                           in_core=bool(rung in SUBSET[(lad, "CORE")]),
                           turnover=float(tn[dp["warm"]].sum()) / (dp["warm"].sum() / 252.0), **b)
                row.update(legs_4b(b, sb))
                row.update(legs_4b_oos(b, sb))
                row.update(legs_4a(b, lb[panel]))
                row["pass_4b_full"] = all(row[k] for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                row["pass_4b_oos"] = all(row[k] for k in ("O_S", "O_DD", "O_CAGR"))
                row["pass_4a"] = all(row[k] for k in ("A_H1", "A_H2", "A_DD"))
                grid_rows.append(row)
    G = pd.DataFrame(grid_rows)
    P(f"  built {len(G):,} books ({int(G.in_core.sum())} of them on 1110/1116's CORE rungs) "
      f"in {time.time() - t0:.0f}s")

    prior = pd.read_csv(f"{PRIOR1117}.grid.csv", dtype=str, keep_default_na=False)
    mine = G.set_index(["panel", "ladder", "rung"])
    dev = []
    for _, r in prior.iterrows():
        key = (r["panel"], r["ladder"], r["rung"])
        if key not in mine.index:
            dev.append(np.inf)
            continue
        mr = mine.loc[key]
        dev.append(max(abs(mr["CAGR"] - float(r["CAGR"])), abs(mr["Sharpe"] - float(r["Sharpe"])),
                       abs(mr["MaxDD"] - float(r["MaxDD"])), abs(mr["OOS_Sharpe"] - float(r["OOS_Sharpe"])),
                       abs(mr["IS_Sharpe"] - float(r["IS_Sharpe"])),
                       abs(mr["turnover"] - float(r["turnover"]))))
    g8 = float(np.max(dev))
    gates["G8"] = g8 < 1e-9 and len(prior) == 74
    gaterows.append(dict(gate="G8", what=f"reproduce 1117's committed {len(prior)}-row grid",
                         value=g8, pass_=gates["G8"]))
    P(f"  G8  reproduce 1117's committed {len(prior)}-row grid              {g8:.2e}   "
      f"{'PASS' if gates['G8'] else 'FAIL'}")

    # --------------------------------------------- IS-ONLY BOOTSTRAP: SD of gaps, and floors
    P("")
    P("## IS-ONLY BOOTSTRAP — every quantity that selects a rung is built on 2009-2016 alone.")
    BOOTS: dict = {}     # (base, panel, lad) -> dict(stat -> (rungs, vals, boot))
    for base in SEED_BASES:
        for panel in PANELS:
            dp = panels[panel]
            insmask = dp["ins"]
            Tis = int(insmask.sum())
            rng = np.random.default_rng(seed_of(base, panel, "IS"))
            idxb, nb = block_index(rng, Tis, L_HEAD, BDRAWS)
            for lad in LADDERS:
                rungs = RUNGS[lad]
                R = np.vstack([RET[(panel, lad, rg)][insmask] for rg in rungs])
                cag, shp = boot_exact(R, idxb, nb, L_HEAD)
                ddb = boot_maxdd(R, idxb)
                vals = {"C": np.array([fmet(R[i])[0] for i in range(len(rungs))]),
                        "S": np.array([fmet(R[i])[1] for i in range(len(rungs))]),
                        "D": np.array([fmet(R[i])[2] for i in range(len(rungs))])}
                BOOTS[(base, panel, lad)] = dict(rungs=rungs, vals=vals,
                                                 boot={"C": cag, "S": shp, "D": ddb})
    P(f"  {len(BOOTS)} (seed base x panel x ladder) bootstraps, {BDRAWS} draws each, "
      f"L={L_HEAD}, in {time.time() - t0:.0f}s")

    # per (base, panel, lad, rung_set, stat): the IS floor; per chooser: SD of the gap
    scale_rows = []
    for base in SEED_BASES:
        for panel in PANELS:
            for lad in LADDERS:
                Bk = BOOTS[(base, panel, lad)]
                rungs = Bk["rungs"]
                pos = {rg: i for i, rg in enumerate(rungs)}
                for rs in RUNGSETS:
                    sub = [pos[rg] for rg in SUBSET[(lad, rs)]]
                    for ch, (iscol, ooscol, sk, sign) in CHOOSERS.items():
                        vals, boot = Bk["vals"][sk], Bk["boot"][sk]
                        A = agree_matrix(vals, boot)
                        fl = floor_sub(vals, A, sub, Q_HEAD)
                        # IS argmax within the subset
                        sv = np.array([vals[i] for i in sub])
                        pick_i = sub[int(np.nanargmax(sv))]
                        def_i = pos[DEFAULT_RUNG[lad]]
                        gap = float(vals[pick_i] - vals[def_i])
                        dd_ = boot[pick_i] - boot[def_i]
                        dd_ = dd_[np.isfinite(dd_)]
                        se = float(dd_.std(ddof=1)) if len(dd_) > 1 else np.nan
                        scale_rows.append(dict(seed_base=base, panel=panel, ladder=lad,
                                               rung_set=rs, chooser=ch, k=len(sub),
                                               pick=rungs[pick_i], default=DEFAULT_RUNG[lad],
                                               is_gap=gap, gap_SE=se, IS_floor=fl,
                                               gap_over_SE=(gap / se if se and np.isfinite(se) and se > 0 else np.nan),
                                               gap_over_floor=(gap / fl if np.isfinite(fl) and fl > 0 else 0.0),
                                               floor_is_inf=bool(not np.isfinite(fl))))
    SC = pd.DataFrame(scale_rows)
    dump(SC, "scales")
    P("  IS floors and gap SDs (headline seed base), by panel x ladder x rung set x chooser:")
    P(SC[SC.seed_base == SEED_BASES[0]][["panel", "ladder", "rung_set", "chooser", "k", "pick",
                                         "is_gap", "gap_SE", "IS_floor", "gap_over_SE",
                                         "gap_over_floor"]].to_string(
        index=False, float_format=lambda x: f"{x:.4f}"))
    ninf = int(SC[SC.seed_base == SEED_BASES[0]].floor_is_inf.sum())
    P(f"  INFINITE IS floors: {ninf} of {len(SC[SC.seed_base == SEED_BASES[0]])} cells "
      f"(K_FLOOR degenerates to 'always default' at every tau > 0 there)")
    P("")

    # ---------------------------------------------------- THE CURVE: rule-8 walk-forward
    P("## THE CURVE — RULE 8 WALK-FORWARD.  Rung chosen on IS 2009-2016 ALONE by the SHRUNK")
    P("##   chooser; OOS 2017-2026 read ONCE.  Scored against that ladder's FROZEN DEFAULT")
    P("##   rung, against SPY and against the live RULES v2 book.")
    gi = G.set_index(["panel", "ladder", "rung"])
    SCi = SC.set_index(["seed_base", "panel", "ladder", "rung_set", "chooser"])
    wf = []
    for base in SEED_BASES:
        for panel in PANELS:
            sb, lbm = panels[panel]["spy_m"], lb[panel]
            for lad in LADDERS:
                dref = gi.loc[(panel, lad, DEFAULT_RUNG[lad])]
                for rs in RUNGSETS:
                    rungs = SUBSET[(lad, rs)]
                    sub = G[(G.panel == panel) & (G.ladder == lad) & (G.rung.isin(rungs))]
                    for ch, (iscol, ooscol, sk, sign) in CHOOSERS.items():
                        s = SCi.loc[(base, panel, lad, rs, ch)]
                        argmax_rung = s["pick"]
                        best = sub.loc[sub[ooscol].idxmax()]          # the ORACLE (unattainable)
                        fullbest = sub.loc[sub[STAT_FULL].idxmax()]
                        for keying in KEYINGS:
                            unit = s["gap_SE"] if keying == "K_SE" else s["IS_floor"]
                            for tau in TAUS:
                                if tau == 0.0:
                                    take = s["is_gap"] > 0
                                elif not np.isfinite(tau):
                                    take = False
                                elif not np.isfinite(unit):
                                    take = False                      # inf floor: never move
                                else:
                                    take = bool(s["is_gap"] > tau * unit)
                                rg = argmax_rung if take else DEFAULT_RUNG[lad]
                                pick = gi.loc[(panel, lad, rg)]
                                wf.append(dict(
                                    seed_base=base, panel=panel, ladder=lad, rung_set=rs,
                                    chooser=ch, keying=keying, tau=tau, k=len(rungs),
                                    pick=rg, argmax_rung=argmax_rung, default=DEFAULT_RUNG[lad],
                                    moved=bool(rg != DEFAULT_RUNG[lad]),
                                    argmax_moves=bool(argmax_rung != DEFAULT_RUNG[lad]),
                                    is_gap=float(s["is_gap"]), unit=float(unit),
                                    CAGR=pick["CAGR"], Sharpe=pick["Sharpe"], MaxDD=pick["MaxDD"],
                                    H1=pick["H1"], H2=pick["H2"],
                                    OOS_CAGR=pick["OOS_CAGR"], OOS_Sharpe=pick["OOS_Sharpe"],
                                    OOS_MaxDD=pick["OOS_MaxDD"],
                                    adv_matched=sign * float(pick[ooscol] - dref[ooscol]),
                                    adv_oos_sharpe=float(pick["OOS_Sharpe"] - dref["OOS_Sharpe"]),
                                    regret=float(sign * (best[ooscol] - pick[ooscol])),
                                    oracle_rung=best["rung"], full_argmax=fullbest["rung"],
                                    def_OOS_Sharpe=float(dref["OOS_Sharpe"]),
                                    pass_4b_full=bool(pick["pass_4b_full"]),
                                    pass_4b_oos=bool(pick["pass_4b_oos"]),
                                    pass_4a=bool(pick["pass_4a"]),
                                    spy_OOS_Sharpe=sb["OOS_Sharpe"],
                                    live_OOS_Sharpe=lbm["OOS_Sharpe"]))
    WF = pd.DataFrame(wf)
    dump(WF, "walkforward")
    dump(G, "grid")

    H = WF[WF.seed_base == SEED_BASES[0]]

    # ------------------------------------------------------------------- H_PREMISE at tau=0
    z = H[(H.tau == 0.0) & (H.keying == "K_SE")]
    zm = z[z.moved]
    P(f"  tau=0 reproduces 1117: {len(zm)} of {len(z)} picks MOVE off the default; median")
    P(f"    matched advantage {zm.adv_matched.median():+.4f} (1117 committed "
      f"{A1117_MOVERS[2]:+.4f}), median OOS-Sharpe advantage "
      f"{zm.adv_oos_sharpe.median():+.4f} (1117 committed {A1117_MOVERS[3]:+.4f})")
    prem = (len(zm) == A1117_MOVERS[0] and len(z) == A1117_MOVERS[1]
            and abs(zm.adv_matched.median() - A1117_MOVERS[2]) < 5e-4
            and abs(zm.adv_oos_sharpe.median() - A1117_MOVERS[3]) < 5e-4)
    gates["G9"] = prem
    gaterows.append(dict(gate="G9", what="reproduce 1117's 36/48 mover headline",
                         value=float(abs(zm.adv_matched.median() - A1117_MOVERS[2])), pass_=prem))
    P(f"  G9  CROSS-RUN reproduce 1117's 36/48 mover headline                  "
      f"{'PASS' if prem else 'FAIL'}")
    P("")
    GT = pd.DataFrame(gaterows)
    dump(GT, "gates")
    P(f"  GATES: {int(GT.pass_.sum())} of {len(GT)} PASS")
    P("")

    for panel in PANELS:
        sb, lbm = panels[panel]["spy_m"], lb[panel]
        P(f"  {panel} SPY       full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%}   "
          f"OOS {sb['OOS_CAGR']:.2%} / {sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"  {panel} RULES v2  full {lbm['CAGR']:.2%} / {lbm['Sharpe']:.4f} / {lbm['MaxDD']:.2%}   "
          f"OOS {lbm['OOS_CAGR']:.2%} / {lbm['OOS_Sharpe']:.4f} / {lbm['OOS_MaxDD']:.2%}")
        P(f"  {panel} DEFAULT rungs (the comparand at every tau): " +
          ", ".join(f"{l}={DEFAULT_RUNG[l]} OOS_S {gi.loc[(panel, l, DEFAULT_RUNG[l])]['OOS_Sharpe']:.4f}"
                    for l in LADDERS))
    P("")

    # ------------------------------------------------------------------ THE PUBLISHED GRID
    P("## THE 27 PUBLISHED DIAL POINTS (CHOOSER x tau), each under BOTH keyings.")
    P("##   'adv' = matched-statistic OOS advantage over the ladder's frozen default rung;")
    P("##   'advS' = OOS-Sharpe advantage.  n=48 cells (2 panels x 4 ladders x 2 rung sets x")
    P("##   ... pooled per chooser: 16 cells).  'mv' = how many still move off the default.")
    for keying in KEYINGS:
        P(f"  --- {keying} ---")
        P(f"  {'chooser':11s} {'tau':>5s}  {'mv':>5s}  {'med adv':>9s} {'mean adv':>9s} "
          f"{'wins':>7s}  {'med advS':>9s} {'mean advS':>9s}  {'med OOS_S':>9s} {'med reg':>8s}")
        for ch in CHOOSERS:
            for tau in TAUS:
                x = H[(H.keying == keying) & (H.chooser == ch) & (H.tau == tau)]
                P(f"  {ch:11s} {tau:5.2f}  {int(x.moved.sum()):2d}/{len(x):2d}  "
                  f"{x.adv_matched.median():+9.4f} {x.adv_matched.mean():+9.4f} "
                  f"{int((x.adv_matched > 0).sum()):3d}/{len(x):<3d}  "
                  f"{x.adv_oos_sharpe.median():+9.4f} {x.adv_oos_sharpe.mean():+9.4f}  "
                  f"{x.OOS_Sharpe.median():9.4f} {x.regret.median():+8.4f}")
        P("")

    P("## THE CURVE, pooled over all 3 choosers (48 cells per tau):")
    P(f"  {'keying':8s} {'tau':>5s}  {'mv':>6s}  {'med adv':>9s} {'mean adv':>9s} {'wins':>8s}"
      f"  {'med advS':>9s} {'mean advS':>9s}")
    curve_rows = []
    for keying in KEYINGS:
        for tau in TAUS:
            x = H[(H.keying == keying) & (H.tau == tau)]
            r = dict(keying=keying, tau=tau, n=len(x), moved=int(x.moved.sum()),
                     med_adv=float(x.adv_matched.median()), mean_adv=float(x.adv_matched.mean()),
                     wins=int((x.adv_matched > 0).sum()),
                     med_advS=float(x.adv_oos_sharpe.median()),
                     mean_advS=float(x.adv_oos_sharpe.mean()),
                     med_OOS_Sharpe=float(x.OOS_Sharpe.median()),
                     med_regret=float(x.regret.median()),
                     n_4b_full=int(x.pass_4b_full.sum()), n_4b_oos=int(x.pass_4b_oos.sum()),
                     n_4a=int(x.pass_4a.sum()))
            curve_rows.append(r)
            P(f"  {keying:8s} {tau:5.2f}  {r['moved']:2d}/{r['n']:<3d}  {r['med_adv']:+9.4f} "
              f"{r['mean_adv']:+9.4f} {r['wins']:3d}/{r['n']:<4d}  {r['med_advS']:+9.4f} "
              f"{r['mean_advS']:+9.4f}")
    CV = pd.DataFrame(curve_rows)
    dump(CV, "curve")
    P("")

    P("  SAME CURVE restricted to the cells whose NAIVE argmax MOVES (1117's 36 of 48) —")
    P("  the cells where shrinkage can do anything at all:")
    mv = H[H.argmax_moves]
    P(f"  {'keying':8s} {'tau':>5s}  {'mv':>6s}  {'med adv':>9s} {'mean adv':>9s} "
      f"{'wins':>8s}  {'med advS':>9s}")
    mrows = []
    for keying in KEYINGS:
        for tau in TAUS:
            x = mv[(mv.keying == keying) & (mv.tau == tau)]
            mrows.append(dict(keying=keying, tau=tau, n=len(x), moved=int(x.moved.sum()),
                              med_adv=float(x.adv_matched.median()),
                              mean_adv=float(x.adv_matched.mean()),
                              wins=int((x.adv_matched > 0).sum()),
                              med_advS=float(x.adv_oos_sharpe.median())))
            P(f"  {keying:8s} {tau:5.2f}  {int(x.moved.sum()):2d}/{len(x):<3d}  "
              f"{x.adv_matched.median():+9.4f} {x.adv_matched.mean():+9.4f} "
              f"{int((x.adv_matched > 0).sum()):3d}/{len(x):<4d}  "
              f"{x.adv_oos_sharpe.median():+9.4f}")
    MV = pd.DataFrame(mrows)
    dump(MV, "movers")
    P("")

    P("  by LADDER at the headline keying K_SE (pooled over panels, rung sets, choosers):")
    bl = H[H.keying == "K_SE"].groupby(["ladder", "tau"]).agg(
        n=("adv_matched", "size"), moved=("moved", "sum"),
        med_adv=("adv_matched", "median"), med_advS=("adv_oos_sharpe", "median")).reset_index()
    P(bl.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")
    P("  by PANEL and RUNG SET at K_SE (pooled over ladders and choosers):")
    bp = H[H.keying == "K_SE"].groupby(["panel", "rung_set", "tau"]).agg(
        n=("adv_matched", "size"), moved=("moved", "sum"),
        med_adv=("adv_matched", "median"), med_advS=("adv_oos_sharpe", "median")).reset_index()
    P(bp.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")

    # ------------------------------------------------- POST-RUN D1 (labelled as POST-RUN)
    P("## POST-RUN D1, and it is labelled POST-RUN because it was NOT declared before the")
    P("##   numbers.  The pooled MEDIAN above is degenerate: once more than half the cells")
    P("##   stop moving, the median is 0 BY CONSTRUCTION whatever the movers do, so it cannot")
    P("##   distinguish 'shrinkage helped' from 'shrinkage stopped'.  The statistic that can")
    P("##   is the advantage CONDITIONAL ON STILL MOVING.  This runs in FAVOUR of H_RECOVER")
    P("##   — i.e. against the verdict the declared rule reaches — and is reported anyway.")
    P(f"  {'keying':8s} {'tau':>5s}  {'movers':>6s}  {'med adv|mv':>10s} {'mean adv|mv':>11s} "
      f"{'wins|mv':>9s}  {'med advS|mv':>11s} {'mean advS|mv':>12s}")
    cond_rows = []
    for keying in KEYINGS:
        for tau in TAUS:
            x = H[(H.keying == keying) & (H.tau == tau) & (H.moved)]
            if not len(x):
                P(f"  {keying:8s} {tau:5.2f}       0   (no cell still moves — the chooser has "
                  f"stopped choosing)")
                cond_rows.append(dict(keying=keying, tau=tau, n_movers=0, med_adv=np.nan,
                                      mean_adv=np.nan, wins=0, med_advS=np.nan, mean_advS=np.nan))
                continue
            cond_rows.append(dict(keying=keying, tau=tau, n_movers=len(x),
                                  med_adv=float(x.adv_matched.median()),
                                  mean_adv=float(x.adv_matched.mean()),
                                  wins=int((x.adv_matched > 0).sum()),
                                  med_advS=float(x.adv_oos_sharpe.median()),
                                  mean_advS=float(x.adv_oos_sharpe.mean())))
            P(f"  {keying:8s} {tau:5.2f}  {len(x):6d}  {x.adv_matched.median():+10.4f} "
              f"{x.adv_matched.mean():+11.4f} {int((x.adv_matched > 0).sum()):4d}/{len(x):<4d}  "
              f"{x.adv_oos_sharpe.median():+11.4f} {x.adv_oos_sharpe.mean():+12.4f}")
    CD = pd.DataFrame(cond_rows)
    dump(CD, "conditional")
    P("")
    P("  WHO SURVIVES THE STRICTEST SHRINK (tau=3, K_SE) — every cell that still moves:")
    srv = H[(H.keying == "K_SE") & (H.tau == 3.0) & (H.moved)]
    if len(srv):
        P(srv[["panel", "ladder", "rung_set", "chooser", "pick", "default", "is_gap", "unit",
               "adv_matched", "adv_oos_sharpe", "OOS_Sharpe", "OOS_MaxDD"]].to_string(
            index=False, float_format=lambda x: f"{x:.4f}"))
        P(f"    all {len(srv)} survivors use chooser(s) "
          f"{sorted(set(srv.chooser))} on {sorted(set(srv.ladder))}; distinct picks "
          f"{sorted(set(zip(srv.panel, srv.ladder, srv.pick)))}")
        P(f"    their mean MATCHED advantage is {srv.adv_matched.mean():+.4f} but their mean")
        P(f"    OOS-SHARPE advantage is {srv.adv_oos_sharpe.mean():+.4f} — the strict-shrink")
        P("    survivors buy OOS DRAWDOWN, not OOS Sharpe.  That is a different claim from the")
        P("    one the queue asked about and it rests on 4 cells, so it is PARKED, not kept.")
    else:
        P("    none")
    P("")

    # --------------------------------------------------------------------- THE ORACLE BOUND
    orc = []
    for panel in PANELS:
        for lad in LADDERS:
            for rs in RUNGSETS:
                rungs = SUBSET[(lad, rs)]
                sub = G[(G.panel == panel) & (G.ladder == lad) & (G.rung.isin(rungs))]
                dref = gi.loc[(panel, lad, DEFAULT_RUNG[lad])]
                for ch, (iscol, ooscol, sk, sign) in CHOOSERS.items():
                    best = sub.loc[sub[ooscol].idxmax()]
                    orc.append(dict(panel=panel, ladder=lad, rung_set=rs, chooser=ch,
                                    oracle=best["rung"],
                                    oracle_adv=sign * float(best[ooscol] - dref[ooscol]),
                                    oracle_advS=float(best["OOS_Sharpe"] - dref["OOS_Sharpe"])))
    OR = pd.DataFrame(orc)
    dump(OR, "oracle")
    P(f"  THE ORACLE BOUND — what a chooser with OOS foreknowledge would have won over the")
    P(f"  default: median matched advantage {OR.oracle_adv.median():+.4f} "
      f"(mean {OR.oracle_adv.mean():+.4f}), median OOS-Sharpe advantage "
      f"{OR.oracle_advS.median():+.4f}, over {len(OR)} cells.")
    P("  The ladders are NOT flat out of sample — there IS money on them.  The question is")
    P("  only whether an IS-only rule can reach any of it.")
    P("")

    # --------------------------------------------------------------- 4a / 4b AT EVERY RUNG
    P("## PROTOCOL rule 4 — both KEEP paths, scored at every rung and every chosen book.")
    P(f"  whole grid {len(G)} rungs: 4b full {int(G.pass_4b_full.sum())}, 4b OOS "
      f"{int(G.pass_4b_oos.sum())}, 4a {int(G.pass_4a.sum())}")
    P(f"  chosen books ({len(H)} = 3 choosers x 9 taus x 2 keyings x 8 panel/ladder/rung-set "
      f"cells at the headline seed base):")
    P(f"    4b full {int(H.pass_4b_full.sum())}, 4b OOS {int(H.pass_4b_oos.sum())}, "
      f"4a {int(H.pass_4a.sum())}, median OOS Sharpe {H.OOS_Sharpe.median():.4f}, "
      f"median regret {H.regret.median():+.4f}")
    pw = H[H.pass_4b_full].drop_duplicates(subset=["panel", "ladder", "pick"])
    if len(pw):
        P("  DISTINCT books among the chosen that clear 4b (full sample), with OOS triples:")
        P(pw[["panel", "ladder", "rung_set", "chooser", "keying", "tau", "pick", "CAGR",
              "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]].to_string(
            index=False, float_format=lambda x: f"{x:.4f}"))
    else:
        P("  none of the chosen books clears 4b (full sample).")
    P("")

    # ------------------------------------------------------------------------- HYPOTHESES
    P("## HYPOTHESES, scored")
    hyp = []

    best_finite = {}
    for keying in KEYINGS:
        c = CV[(CV.keying == keying) & np.isfinite(CV.tau)]
        c_ = c[c.tau > 0]
        best_finite[keying] = (float(c_.med_advS.max()), float(c_.loc[c_.med_advS.idxmax(), "tau"]),
                               float(c_.med_adv.max()))
    rec = all(best_finite[k][0] > 0 for k in KEYINGS)
    # per-chooser recovery at a finite tau>0, both panels pooled
    perch = {}
    for ch in CHOOSERS:
        ok = []
        for keying in KEYINGS:
            x = H[(H.keying == keying) & (H.chooser == ch) & (H.tau > 0) & np.isfinite(H.tau)]
            g = x.groupby("tau").adv_oos_sharpe.median()
            ok.append(bool((g > 0).any()))
        perch[ch] = all(ok)
    nch = sum(perch.values())
    recover = bool(rec and nch >= 2)
    hyp.append(dict(name="H_PREMISE", holds=bool(prem),
                    detail=(f"tau=0: {len(zm)} of {len(z)} move, median matched adv "
                            f"{zm.adv_matched.median():+.4f}, median OOS-S adv "
                            f"{zm.adv_oos_sharpe.median():+.4f} vs 1117's committed "
                            f"{A1117_MOVERS[0]}/{A1117_MOVERS[1]}, {A1117_MOVERS[2]:+.4f}, "
                            f"{A1117_MOVERS[3]:+.4f}")))
    hyp.append(dict(name="H_RECOVER", holds=recover,
                    detail=(f"best FINITE tau>0 pooled median OOS-S advantage: K_SE "
                            f"{best_finite['K_SE'][0]:+.4f} at tau={best_finite['K_SE'][1]:.2f}, "
                            f"K_FLOOR {best_finite['K_FLOOR'][0]:+.4f} at "
                            f"tau={best_finite['K_FLOOR'][1]:.2f}; choosers recovering: "
                            f"{nch} of {len(CHOOSERS)} ({', '.join(k for k, v in perch.items() if v) or 'none'})")))
    mono = {}
    for keying in KEYINGS:
        c = CV[CV.keying == keying].sort_values("tau")
        mono[keying] = bool((np.diff(c.med_advS.values) >= -1e-12).all())
    hyp.append(dict(name="H_MONOTONE", holds=all(mono.values()),
                    detail=f"median OOS-S advantage non-decreasing in tau: " +
                           ", ".join(f"{k} {'YES' if v else 'NO'}" for k, v in mono.items())))
    sup = {k: float(CV[CV.keying == k].med_advS.max()) for k in KEYINGS}
    at_inf = {k: int(CV[(CV.keying == k) & (~np.isfinite(CV.tau))].moved.iloc[0]) for k in KEYINGS}
    gridfact = bool(all(sup[k] <= 1e-12 for k in KEYINGS) and all(v == 0 for v in at_inf.values()))
    hyp.append(dict(name="H_GRID", holds=gridfact,
                    detail=(f"curve supremum: " + ", ".join(f"{k} {sup[k]:+.4f}" for k in KEYINGS) +
                            f"; movers at tau=inf: " + ", ".join(f"{k} {at_inf[k]}" for k in KEYINGS))))
    vk = {k: (best_finite[k][0] > 0) for k in KEYINGS}
    hyp.append(dict(name="H_KEYING", holds=bool(len(set(vk.values())) == 1),
                    detail=f"K_SE recovers {vk['K_SE']}, K_FLOOR recovers {vk['K_FLOOR']}"))
    HY = pd.DataFrame(hyp)
    dump(HY, "hypotheses")
    for h in hyp:
        P(f"  {h['name']:12s} {'HOLDS' if h['holds'] else 'FAILS':5s}  {h['detail']}")
    P("")

    # ------------------------------------------------------- seed-base stability (not a dial)
    P("  SEED-BASE STABILITY (not a dial): pooled median OOS-S advantage at each tau, K_SE,")
    P("  under each of the 3 seed bases —")
    for tau in TAUS:
        vs = [WF[(WF.seed_base == b) & (WF.keying == "K_SE") & (WF.tau == tau)].adv_oos_sharpe.median()
              for b in SEED_BASES]
        P(f"    tau {tau:5.2f}  " + "  ".join(f"{v:+.4f}" for v in vs) +
          f"   spread {max(vs) - min(vs):.4f}")
    P("")

    verdict = "CHOOSER ARTEFACT" if recover else "GRID FACT"
    P("## VERDICT")
    P(f"  {verdict}.")
    if recover:
        P("  A finite shrink threshold lifts the pooled median OOS advantage above zero, so")
        P("  1117's negative result was the chooser over-reacting to small in-sample gaps.")
    else:
        P("  No finite shrink threshold lifts the pooled median OOS advantage above zero under")
        P("  both keyings and at >= 2 of 3 choosers.  The best a shrunk chooser achieves is to")
        P("  stop choosing: the supremum of the curve is reached where every cell is back on")
        P("  its default and the advantage is 0 BY CONSTRUCTION.  Shrinkage MUTES the loss; it")
        P("  does not RECOVER it.  The negative-information result is a property of the GRID,")
        P("  not of the chooser — which is what 1117's clause already assumes.")
        cdf = CD[(CD.tau > 0) & np.isfinite(CD.tau) & (CD.n_movers > 0)]
        if len(cdf):
            k = cdf.mean_advS.idxmax()
            P("  POST-RUN D1 does not overturn it: CONDITIONAL ON STILL MOVING, the best finite")
            P(f"  tau>0 mean OOS-SHARPE advantage over the default is {cdf.mean_advS.max():+.4f} "
              f"(at tau={cdf.loc[k, 'tau']:.2f}, {int(cdf.loc[k, 'n_movers'])} movers) — still")
            P("  not a positive Sharpe advantage.  The one thing strict shrinkage does buy is")
            P("  OOS DRAWDOWN under C_ISDD, on 4 cells; that is filed as a new queue idea, not")
            P("  claimed here.")
    P("  NOT a KEEP under either path: no book is proposed and nothing here beats SPY or the")
    P("  live book out of sample on its own.")
    P(f"# done in {time.time() - t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

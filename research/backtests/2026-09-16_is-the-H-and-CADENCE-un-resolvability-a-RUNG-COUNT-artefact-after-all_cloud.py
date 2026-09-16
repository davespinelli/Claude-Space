#!/usr/bin/env python3
"""Idea 1118 (cloud lane, idea 2 of 2, 2026-09-16)
   is-the-H-and-CADENCE-un-resolvability-a-RUNG-COUNT-artefact-after-all

1116 found H and CADENCE carry an infinite resolution floor at all four statistics on both
large panels while N and GROSS almost never do — and its two un-resolvable ladders are
EXACTLY its two 4-rung ladders, its two resolvable ones EXACTLY its 9- and 10-rung ladders.
Rung count and ladder identity are confounded 2-2 by construction.  This run breaks the
confound in the only way that breaks it: it extends H to 9 rungs (two different spacings)
and CADENCE to 9, re-runs 1116's 4x4 decomposition, and then — the decisive arm — computes
the WHOLE rung-count curve P(INF_FLOOR | ladder, m) by enumerating EVERY subset of size
m = 3..k of every ladder, so N, GROSS, H and CADENCE are compared at MATCHED rung count.

TUNED DIALS (2, PROTOCOL rule 4): H GRID {H4, H9, H9_LOG} x CADENCE SET {C4, C9} =
6 combinations, ALL published.  PANEL, LADDER and STATISTIC are not dials.  The subset
enumeration is exhaustive, not sampled, so nothing is selected there either.

A FINDING ABOUT THE IDEA'S OWN INSTRUCTION, recorded before any number: `engine.rebalance_mask`
serves exactly FOUR cadences (D, W, M, Q), so "extend CADENCE to as many cadences as
engine.rebalance_mask serves" cannot be executed literally — it is already at its maximum.
This run therefore builds the extra cadences ON TOP of engine's own masks, without touching
engine.py, and gates the construction against it (G7).

FROZEN at 1082/1094/1098/1102/1108/1110/1116's construction: CAND20 legs, cap INF,
max_vol 0.60, gross 0.75 (except on GROSS), min hold 126 (except on H), N=20 (except on N),
W (except on CADENCE), 10 bps, LAG 1, warm-up 260, IS end 2016-12-31, block L=63, 1000 draws,
crc32 seeds, q=0.90 headline.

Standalone, deterministic, offline.
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
SLUG = "is-the-H-and-CADENCE-un-resolvability-a-RUNG-COUNT-artefact-after-all"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"
BT = Path(__file__).resolve().parent
PRIOR1110 = BT / "2026-09-16_what-does-the-RECORD-LOSE-if-the-FLOOR-CLAUSE-is-ENACTED-AS-WRITTEN_C"

LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST, GROSS0, FREQ0, HOLD0, N0 = 10.0, 0.75, "W", 126, 20
LEGS = [(21, 252), (0, 126), (0, 63)]

LAD_N = [5, 8, 10, 12, 15, 20, 25, 30, 40]                                   # 1116's, 9 rungs
LAD_G = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]         # 1116's, 10 rungs
H_GRIDS = {                                                     # dial 1 — every grid nests H4
    "H4": [21, 63, 126, 252],                                                # 1116's, 4 rungs
    "H9": [21, 42, 63, 84, 126, 168, 210, 252, 378],                         # linear, 9 rungs
    "H9_LOG": [10, 21, 42, 63, 89, 126, 178, 252, 356],                      # log, 9 rungs
}
C_SETS = {                                                      # dial 2 — C9 nests C4
    "C4": ["D", "W", "M", "Q"],                                              # 1116's, engine's
    "C9": ["D", "2D", "W", "2W", "M", "2M", "Q", "2Q", "4Q"],                # 9 rungs
}
STATS = ["S_FULL", "S_OOS", "CAGR", "DD"]
SCALE = {"S_FULL": 1.0, "S_OOS": 1.0, "CAGR": 100.0, "DD": 100.0}
STATCOL = {"S_FULL": "Sharpe", "S_OOS": "OOS_Sharpe", "CAGR": "CAGR", "DD": "MaxDD"}
LADDERS = ["N", "H", "GROSS", "CADENCE"]
PANELS = ["U56", "B136"]
CHOOSERS = ["C_ISSHARPE", "C_ISCAGR", "C_ISDD"]

Q_HEAD, L_HEAD, BDRAWS = 0.90, 63, 1000
SEED_BOOT = 11181118
SEED_BASES = [11181118, 11161116, 11191119, 11091109, 10821082, 10981098, 11021102, 11081108]

# 1119's committed per-ladder INF_FLOOR redraw RANGES at the CORE rungs (its 8-base arm)
R1119 = {"U56": {"N": (0, 1), "H": (3, 4), "GROSS": (1, 2), "CADENCE": (4, 4)},
         "B136": {"N": (2, 2), "H": (4, 4), "GROSS": (0, 0), "CADENCE": (3, 4)}}

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


def seed_of(base, *parts):
    return base + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


# ------------------------------------------------- 1082/1098/1102/1108's fast runner, verbatim
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
    """Symmetric agreement matrix: P(bootstrap sign == observed sign) for every rung pair."""
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
        return float("inf"), 0.0
    gaps, agr = np.array(gaps), np.array(agr)
    un = agr < q
    largest_un = float(gaps[un].max()) if un.any() else 0.0
    ok = (~un) & (gaps > largest_un)
    return (float(gaps[ok].min()) if ok.any() else float("inf")), largest_un


def eta2_rows(tab):
    """Share of the binary table's total SS explained by its ROWS (1116's ETA2)."""
    tab = np.asarray(tab, float)
    gm = tab.mean()
    sst = ((tab - gm) ** 2).sum()
    if sst <= 0:
        return np.nan
    ssb = tab.shape[1] * ((tab.mean(axis=1) - gm) ** 2).sum()
    return float(ssb / sst)


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 3:
        return np.nan
    ra = pd.Series(a[m]).rank().values
    rb = pd.Series(b[m]).rank().values
    ra, rb = ra - ra.mean(), rb - rb.mean()
    den = np.sqrt((ra ** 2).sum() * (rb ** 2).sum())
    return float((ra * rb).sum() / den) if den else np.nan


# ------------------------------------------------------------------ cadences engine won't serve
def cadence_mask(idx, spec):
    """engine.rebalance_mask verbatim for D/W/M/Q (gate G7); '<k><BASE>' keeps every k-th bar
    of that base schedule.  engine.rebalance_mask serves FOUR cadences and no more, so every
    extra rung is built on top of it rather than inside it — engine.py is not modified."""
    if spec in ("D", "W", "M", "Q"):
        return rebalance_mask(idx, spec).values.copy()
    k, base = int(spec[:-1]) if spec[:-1].isdigit() else int(spec[:-2]), spec[-1]
    hit = np.flatnonzero(rebalance_mask(idx, base).values)
    m = np.zeros(len(idx), dtype=bool)
    m[hit[::k]] = True
    return m


CAD_ORDER = {"D": 1, "2D": 2, "W": 5, "2W": 10, "M": 21, "2M": 42, "Q": 63, "2Q": 126, "4Q": 252}


def main():
    t0 = time.time()
    P(f"# Idea 1118 (cloud lane, idea 2 of 2, {DATE}) — is the H and CADENCE un-resolvability")
    P("#   a RUNG-COUNT artefact after all?")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4): H GRID {list(H_GRIDS)} x CADENCE SET {list(C_SETS)}")
    P(f"#   = {len(H_GRIDS) * len(C_SETS)} combinations, ALL published.  PANEL, LADDER, "
      "STATISTIC are not dials.  Every H grid NESTS 1116's H4; C9 nests C4.")
    for k, v in H_GRIDS.items():
        P(f"#   {k:8s} {v}")
    for k, v in C_SETS.items():
        P(f"#   {k:8s} {v}")
    P("# RECORDED BEFORE ANY NUMBER — THE IDEA'S INSTRUCTION IS NOT LITERALLY EXECUTABLE:")
    P("#   `engine.rebalance_mask` serves exactly FOUR cadences (D, W, M, Q).  1116's CADENCE")
    P("#   ladder is ALREADY 'as many cadences as engine.rebalance_mask serves'.  C9 is built")
    P("#   ON TOP of engine's own masks (every k-th bar of a base schedule), gated against it")
    P("#   at G7; engine.py, baseline.py, scan.py, bot.py and RULES.md are NOT modified.")
    P(f"# FROZEN: CAND20 legs {LEGS}, cap INF, max_vol {MAXVOL}, gross {GROSS0}, min hold "
      f"{HOLD0}, N {N0}, cadence {FREQ0},")
    P(f"#   {COST:.0f} bps, LAG {LAG}, warm-up {WARMUP}, IS end {IS_END}, block L={L_HEAD}, "
      f"{BDRAWS} draws, crc32 seeds, q={Q_HEAD}, {len(SEED_BASES)} seed bases.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   (a) H_ROWS_CONSTANT  the per-ladder INF_FLOOR rows (of 4) do NOT change when H and")
    P("#                        CADENCE go from 4 rungs to 9 — the idea's literal question.")
    P("#   (b) H_COUNT          rung count carries it: at MATCHED rung count m the four")
    P("#                        ladders' P(INF_FLOOR) agree within 0.20 at every m.")
    P("#   (c) H_IDENTITY       identity carries it: at EVERY matched m >= 4, H and CADENCE")
    P("#                        have a higher P(INF_FLOOR) than N and GROSS.")
    P("#   (d) H_MONO_COUNT     P(INF_FLOOR) rises monotonically in m for every ladder.")
    P("#   (e) H_AXIS_SURVIVES  ETA2_LAD > ETA2_STAT at all 6 dial points on both panels.")
    P("#   (f) H_DISTANCE       1108's alternative: rank-correlation between a ladder's")
    P("#                        SPREAD-OVER-PAIR-NOISE and its INF_FLOOR count beats rung")
    P("#                        count's, over the 8 (panel x ladder) rows at the 9-rung grids.")
    P("#   (g) NOT A KEEP PATH  no book is proposed; 4a/4b and rule 8 scored at every rung")
    P("#                        because rule 4 requires it.")
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
    g4 = max(abs(m12["CAGR"] - A1098_U56_N12[0]), abs(m12["Sharpe"] - A1098_U56_N12[1]), abs(m12["MaxDD"] - A1098_U56_N12[2]))
    gates["G4"] = g4 < 5e-4
    gaterows.append(dict(gate="G4", what="committed U56 n=12 triple", value=g4, pass_=gates["G4"]))
    P(f"  G4  CROSS-RUN 1098/1102's committed U56 n=12 triple       {g4:.2e}   {'PASS' if gates['G4'] else 'FAIL'}")

    db = panels["B136"]
    r15, _ = run_cell("B136", 15, HOLD0, GROSS0, FREQ0)
    m15 = blocks_m(r15, db["warm"], db["ins"], db["oos"])
    g4b = max(abs(m15["CAGR"] - A1098_B136_N15[0]), abs(m15["Sharpe"] - A1098_B136_N15[1]), abs(m15["MaxDD"] - A1098_B136_N15[2]))
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
    gaterows.append(dict(gate="G7", what="cadence_mask == engine.rebalance_mask on all four engine cadences",
                         value=float(g7), pass_=gates["G7"]))
    P(f"  G7  cadence_mask == engine.rebalance_mask (D/W/M/Q)       {g7:.2e}   {'PASS' if gates['G7'] else 'FAIL'}")
    P("      (and engine.rebalance_mask raises on anything else — the four are all it serves)")

    # ------------------------------------------------------------------------ BUILD EVERY BOOK
    H_ALL = sorted(set(sum(H_GRIDS.values(), [])))
    C_ALL = C_SETS["C9"]
    RUNGS = {"N": [str(x) for x in LAD_N], "GROSS": [str(x) for x in LAD_G],
             "H": [str(x) for x in H_ALL], "CADENCE": list(C_ALL)}

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
                           in_1116=bool((lad == "N") or (lad == "GROSS")
                                        or (lad == "H" and int(rung) in H_GRIDS["H4"])
                                        or (lad == "CADENCE" and rung in C_SETS["C4"])),
                           turnover=float(tn[dp["warm"]].sum()) / (dp["warm"].sum() / 252.0), **b)
                row.update(legs_4b(b, sb))
                row.update(legs_4b_oos(b, sb))
                row.update(legs_4a(b, lb[panel]))
                row["pass_4b_full"] = all(row[k] for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                row["pass_4b_oos"] = all(row[k] for k in ("O_S", "O_DD", "O_CAGR"))
                row["pass_4a"] = all(row[k] for k in ("A_H1", "A_H2", "A_DD"))
                grid_rows.append(row)
    G = pd.DataFrame(grid_rows)
    P(f"  built {len(G):,} books ({int(G.in_1116.sum())} of them 1116's own rungs) "
      f"in {time.time() - t0:.0f}s")

    prior = pd.read_csv(f"{PRIOR1110}.grid.csv", dtype=str, keep_default_na=False)
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
                       abs(mr["turnover"] - float(r["turnover"]))))
    g8 = float(np.max(dev))
    gates["G8"] = g8 < 1e-9 and len(prior) == 54
    gaterows.append(dict(gate="G8", what=f"reproduce 1110's committed {len(prior)}-row CORE grid", value=g8, pass_=gates["G8"]))
    P(f"  G8  reproduce 1110's committed {len(prior)}-row CORE grid         {g8:.2e}   {'PASS' if gates['G8'] else 'FAIL'}")

    # -------------------------------------------------------- BOOTSTRAP, per panel per ladder
    _VCACHE: dict = {}

    def vals_of(panel, lad, rungs, stat):
        key = (panel, lad, tuple(rungs), stat)
        if key not in _VCACHE:
            gi = G.set_index(["panel", "ladder", "rung"])[STATCOL[stat]]
            _VCACHE[key] = np.array([gi.loc[(panel, lad, r)] for r in rungs], float) * SCALE[stat]
        return _VCACHE[key]

    AGR = {}                       # (base, panel, ladder, stat) -> agreement matrix over RUNGS
    for base in SEED_BASES:
        for panel in PANELS:
            dp = panels[panel]
            for lad in LADDERS:
                rl = RUNGS[lad]
                Rw = np.array([RET[(panel, lad, r)][dp["warm"]] for r in rl])
                Ro = np.array([RET[(panel, lad, r)][dp["oos"]] for r in rl])
                rng = np.random.default_rng(seed_of(base, panel, lad, "warm"))
                iw, nbw = block_index(rng, Rw.shape[1], L_HEAD, BDRAWS)
                cagb, shpb = boot_exact(Rw, iw, nbw, L_HEAD)
                ddb = boot_maxdd(Rw, iw)
                rng2 = np.random.default_rng(seed_of(base, panel, lad, "oos"))
                io, nbo = block_index(rng2, Ro.shape[1], L_HEAD, BDRAWS)
                _, shpo = boot_exact(Ro, io, nbo, L_HEAD)
                bo = {"S_FULL": shpb, "S_OOS": shpo, "CAGR": cagb * 100.0, "DD": ddb * 100.0}
                for stat in STATS:
                    AGR[(base, panel, lad, stat)] = agree_matrix(vals_of(panel, lad, rl, stat), bo[stat])
        P(f"  bootstrap base {base} done at {time.time() - t0:.0f}s")

    def inf_flag(base, panel, lad, rungs, stat):
        rl = RUNGS[lad]
        sub = [rl.index(r) for r in rungs]
        v = vals_of(panel, lad, rl, stat)
        flo, _ = floor_sub(v, AGR[(base, panel, lad, stat)], sub, Q_HEAD)
        return (not np.isfinite(flo)), flo

    # G9 — 1119's committed redraw ranges, at 1116's own rungs, over 8 bases
    rng_rows, inside = [], 0
    for base in SEED_BASES:
        for panel in PANELS:
            for lad in LADDERS:
                core = {"N": RUNGS["N"], "GROSS": RUNGS["GROSS"],
                        "H": [str(x) for x in H_GRIDS["H4"]], "CADENCE": C_SETS["C4"]}[lad]
                cnt = sum(inf_flag(base, panel, lad, core, s)[0] for s in STATS)
                lo, hi = R1119[panel][lad]
                ok = lo <= cnt <= hi
                inside += ok
                rng_rows.append(dict(base=base, panel=panel, ladder=lad, inf_count=cnt,
                                     committed_lo=lo, committed_hi=hi, inside=ok))
    RG = pd.DataFrame(rng_rows)
    g9 = inside / len(RG)
    gates["G9"] = g9 >= 0.75
    gaterows.append(dict(gate="G9", what="CORE per-ladder INF_FLOOR counts inside 1119's committed redraw ranges",
                         value=g9, pass_=gates["G9"]))
    P(f"  G9  CORE counts inside 1119's committed redraw ranges     {g9:.4f}   "
      f"{'PASS' if gates['G9'] else 'FAIL'}  ({inside} of {len(RG)} panel x ladder x base)")
    dump(RG, "redrawranges")

    g10 = float(min(np.nanmax(vals_of(p, l, RUNGS[l], s)) - np.nanmin(vals_of(p, l, RUNGS[l], s))
                    for p in PANELS for l in LADDERS for s in STATS))
    gates["G10"] = g10 > 0
    gaterows.append(dict(gate="G10", what="every ladder x statistic live", value=g10, pass_=gates["G10"]))
    P(f"  G10 every ladder x statistic is LIVE (min spread)         {g10:.2e}   {'PASS' if gates['G10'] else 'FAIL'}")
    P(f"  GATES: {sum(gates.values())} of {len(gates)} PASS")
    dump(pd.DataFrame(gaterows), "gates")
    P("")

    # ------------------------------------------------- THE 6 DIAL POINTS: 1116's DECOMPOSITION
    P("## THE DECOMPOSITION AT ALL 6 DIAL POINTS (H GRID x CADENCE SET), headline base "
      f"{SEED_BASES[0]}, q={Q_HEAD}")
    dec_rows, cell_rows = [], []
    for hg, hrungs in H_GRIDS.items():
        for cs, crungs in C_SETS.items():
            rung_of = {"N": RUNGS["N"], "GROSS": RUNGS["GROSS"],
                       "H": [str(x) for x in hrungs], "CADENCE": list(crungs)}
            for base in SEED_BASES:
                for panel in PANELS:
                    tab = np.zeros((4, 4))
                    for a, lad in enumerate(LADDERS):
                        for b_, stat in enumerate(STATS):
                            fl, flo = inf_flag(base, panel, lad, rung_of[lad], stat)
                            tab[a, b_] = float(fl)
                            if base == SEED_BASES[0]:
                                cell_rows.append(dict(h_grid=hg, c_set=cs, panel=panel, ladder=lad,
                                                      stat=stat, k=len(rung_of[lad]),
                                                      inf_floor=bool(fl), floor=flo))
                    dec_rows.append(dict(h_grid=hg, c_set=cs, base=base, panel=panel,
                                         eta2_lad=eta2_rows(tab), eta2_stat=eta2_rows(tab.T),
                                         inf_total=int(tab.sum()),
                                         **{f"row_{l}": int(tab[i].sum()) for i, l in enumerate(LADDERS)},
                                         k_H=len(rung_of["H"]), k_C=len(rung_of["CADENCE"])))
    D = pd.DataFrame(dec_rows)
    dump(D, "decomposition")
    dump(pd.DataFrame(cell_rows), "cells")
    head = D[D.base == SEED_BASES[0]]
    P(head[["h_grid", "c_set", "panel", "k_H", "k_C", "row_N", "row_H", "row_GROSS",
            "row_CADENCE", "inf_total", "eta2_lad", "eta2_stat"]].to_string(
        index=False, float_format=lambda x: f"{x:.4f}"))
    P("")
    P(f"  over all {len(SEED_BASES)} seed bases (median per dial point x panel):")
    med = D.groupby(["h_grid", "c_set", "panel"])[["row_N", "row_H", "row_GROSS", "row_CADENCE",
                                                   "eta2_lad", "eta2_stat"]].median().reset_index()
    P(med.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")

    # ------------------------------------------------- THE CONFOUND BREAKER: MATCHED RUNG COUNT
    P("## THE CONFOUND BREAKER — P(INF_FLOOR | ladder, m) over EVERY subset of size m")
    sub_rows = []
    MATCH = {"N": RUNGS["N"], "GROSS": RUNGS["GROSS"],
             "H": [str(x) for x in H_GRIDS["H9"]], "CADENCE": C_SETS["C9"]}
    for panel in PANELS:
        for lad in LADDERS:
            rl = RUNGS[lad]
            full = MATCH[lad]
            pos = [rl.index(r) for r in full]
            k = len(full)
            for stat in STATS:
                v = vals_of(panel, lad, rl, stat)
                A = AGR[(SEED_BASES[0], panel, lad, stat)]
                for m_ in range(3, k + 1):
                    n_inf = n_tot = 0
                    for comb in combinations(pos, m_):
                        flo, _ = floor_sub(v, A, list(comb), Q_HEAD)
                        n_tot += 1
                        n_inf += (not np.isfinite(flo))
                    sub_rows.append(dict(panel=panel, ladder=lad, stat=stat, m=m_,
                                         subsets=n_tot, inf=n_inf, p_inf=n_inf / n_tot))
    S = pd.DataFrame(sub_rows)
    dump(S, "rungcount")
    piv = S.groupby(["ladder", "m"])["p_inf"].mean().unstack(0)
    P("  P(INF_FLOOR) averaged over 2 panels x 4 statistics, by ladder and rung count m:")
    P(piv.to_string(float_format=lambda x: f"{x:.4f}"))
    P("")
    matched = S[S.m == 4].groupby("ladder")["p_inf"].mean()
    P("  AT MATCHED m = 4 (1116's own rung count for H and CADENCE):")
    P("    " + "  ".join(f"{l} {matched[l]:.4f}" for l in LADDERS))
    spread4 = float(matched.max() - matched.min())
    P(f"    spread across ladders at m=4: {spread4:.4f}")
    m9 = S[S.m == 9].groupby("ladder")["p_inf"].mean()
    P("  AT MATCHED m = 9 (H9 / C9 / N's own 9; GROSS subsampled to 9):")
    P("    " + "  ".join(f"{l} {m9[l]:.4f}" for l in LADDERS))
    P("")

    # ------------------------------------------------------ 1108's ALTERNATIVE: SPREAD / NOISE
    P("## 1108's ALTERNATIVE PREDICTOR — ladder SPREAD over PAIR NOISE, at the 9-rung grids")
    snr_rows = []
    for panel in PANELS:
        for lad in LADDERS:
            rl = RUNGS[lad]
            full = MATCH[lad]
            pos = [rl.index(r) for r in full]
            cnt = 0
            snrs = []
            for stat in STATS:
                v = vals_of(panel, lad, rl, stat)
                A = AGR[(SEED_BASES[0], panel, lad, stat)]
                flo, _ = floor_sub(v, A, pos, Q_HEAD)
                cnt += (not np.isfinite(flo))
                sp = float(np.nanmax(v[pos]) - np.nanmin(v[pos]))
                gaps = [abs(v[i] - v[j]) for i, j in combinations(pos, 2)]
                snrs.append(sp / np.median(gaps) if np.median(gaps) > 0 else np.nan)
            snr_rows.append(dict(panel=panel, ladder=lad, k=len(full), inf_count=cnt,
                                 snr=float(np.nanmean(snrs))))
    SN = pd.DataFrame(snr_rows)
    dump(SN, "distance")
    P(SN.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    rho_snr = spearman(SN["snr"].values, SN["inf_count"].values)
    rho_k = spearman(SN["k"].values.astype(float), SN["inf_count"].values)
    P(f"  Spearman(spread/median-gap, INF count) = {rho_snr:+.4f}   "
      f"Spearman(rung count, INF count) = {rho_k:+.4f}   (8 panel x ladder rows, k is 9/10)")
    P("")

    # -------------------------------------------------------- RULE 8 AND BOTH KEEP PATHS (r.4)
    P("## RULE 8 WALK-FORWARD AND BOTH KEEP PATHS")
    wf = []
    for panel in PANELS:
        sb = panels[panel]["spy_m"]
        for hg, hrungs in H_GRIDS.items():
            for cs, crungs in C_SETS.items():
                rung_of = {"N": RUNGS["N"], "GROSS": RUNGS["GROSS"],
                           "H": [str(x) for x in hrungs], "CADENCE": list(crungs)}
                for lad in LADDERS:
                    sub = G[(G.panel == panel) & (G.ladder == lad) & (G.rung.isin(rung_of[lad]))]
                    for ch in CHOOSERS:
                        col = {"C_ISSHARPE": "IS_Sharpe", "C_ISCAGR": "IS_CAGR", "C_ISDD": "IS_MaxDD"}[ch]
                        pick = sub.loc[sub[col].idxmax()]
                        best = sub.loc[sub["OOS_Sharpe"].idxmax()]
                        wf.append(dict(h_grid=hg, c_set=cs, panel=panel, ladder=lad, chooser=ch,
                                       pick=pick["rung"], new_rung=not bool(pick["in_1116"]),
                                       CAGR=pick["CAGR"], Sharpe=pick["Sharpe"], MaxDD=pick["MaxDD"],
                                       H1=pick["H1"], H2=pick["H2"], OOS_CAGR=pick["OOS_CAGR"],
                                       OOS_Sharpe=pick["OOS_Sharpe"], OOS_MaxDD=pick["OOS_MaxDD"],
                                       pass_4b_full=bool(pick["pass_4b_full"]),
                                       pass_4b_oos=bool(pick["pass_4b_oos"]), pass_4a=bool(pick["pass_4a"]),
                                       regret=float(best["OOS_Sharpe"] - pick["OOS_Sharpe"]),
                                       spy_OOS_Sharpe=sb["OOS_Sharpe"]))
    WF = pd.DataFrame(wf)
    dump(WF, "walkforward")
    dump(G, "grid")
    for panel in PANELS:
        sb, lbm = panels[panel]["spy_m"], lb[panel]
        P(f"  {panel} SPY       full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%}   "
          f"OOS {sb['OOS_CAGR']:.2%} / {sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"  {panel} RULES v2  full {lbm['CAGR']:.2%} / {lbm['Sharpe']:.4f} / {lbm['MaxDD']:.2%}   "
          f"OOS {lbm['OOS_CAGR']:.2%} / {lbm['OOS_Sharpe']:.4f} / {lbm['OOS_MaxDD']:.2%}")
    P(f"  IS picks (all dial points): {len(WF)} — 4b full {int(WF.pass_4b_full.sum())}, "
      f"4b OOS {int(WF.pass_4b_oos.sum())}, 4a {int(WF.pass_4a.sum())}, "
      f"median OOS Sharpe {WF.OOS_Sharpe.median():.4f}, median regret {WF.regret.median():+.4f}")
    for hg in H_GRIDS:
        w = WF[WF.h_grid == hg]
        P(f"    H grid {hg:8s}: 4b full {int(w.pass_4b_full.sum())}/{len(w)}, "
          f"median OOS Sharpe {w.OOS_Sharpe.median():.4f}, regret {w.regret.median():+.4f}")
    for cs in C_SETS:
        w = WF[WF.c_set == cs]
        P(f"    cadence {cs:6s}: 4b full {int(w.pass_4b_full.sum())}/{len(w)}, "
          f"median OOS Sharpe {w.OOS_Sharpe.median():.4f}, regret {w.regret.median():+.4f}")
    P(f"  whole grid {len(G)} rungs: 4b full {int(G.pass_4b_full.sum())}, "
      f"4b OOS {int(G.pass_4b_oos.sum())}, 4a {int(G.pass_4a.sum())}; on rungs 1116 never tested "
      f"{int(G[~G.in_1116].pass_4b_full.sum())} of {int((~G.in_1116).sum())}")
    P("")

    # ----------------------------------------------------------------------------- HYPOTHESES
    h4c4 = head[(head.h_grid == "H4") & (head.c_set == "C4")].set_index("panel")
    h9c9 = head[(head.h_grid == "H9") & (head.c_set == "C9")].set_index("panel")
    rows_const = all(int(h4c4.loc[p, f"row_{l}"]) == int(h9c9.loc[p, f"row_{l}"])
                     for p in PANELS for l in LADDERS)
    detail = "; ".join(f"{p} 4-rung " + "/".join(str(int(h4c4.loc[p, f'row_{l}'])) for l in LADDERS)
                       + " -> 9-rung " + "/".join(str(int(h9c9.loc[p, f'row_{l}'])) for l in LADDERS)
                       for p in PANELS)
    ident_ok = all(S[(S.m == mm) & (S.ladder.isin(["H", "CADENCE"]))].p_inf.mean() >
                   S[(S.m == mm) & (S.ladder.isin(["N", "GROSS"]))].p_inf.mean()
                   for mm in range(4, 10))
    mono_ok = all(S[S.ladder == l].groupby("m")["p_inf"].mean().diff().dropna().ge(-1e-12).all()
                  for l in LADDERS)
    axis_ok = bool((head["eta2_lad"] > head["eta2_stat"]).all())
    H = {
        "H_ROWS_CONSTANT": (rows_const, detail),
        "H_COUNT": (spread4 <= 0.20, f"spread across ladders at matched m=4 is {spread4:.4f} "
                                     f"(N {matched['N']:.4f}, H {matched['H']:.4f}, "
                                     f"GROSS {matched['GROSS']:.4f}, CADENCE {matched['CADENCE']:.4f})"),
        "H_IDENTITY": (ident_ok, "H+CADENCE P(INF) above N+GROSS at every matched m 4..9: "
                                 + ", ".join(f"m={mm} {S[(S.m == mm) & S.ladder.isin(['H', 'CADENCE'])].p_inf.mean():.3f} "
                                             f"vs {S[(S.m == mm) & S.ladder.isin(['N', 'GROSS'])].p_inf.mean():.3f}"
                                             for mm in range(4, 10))),
        "H_MONO_COUNT": (mono_ok, "P(INF) non-decreasing in m for all four ladders"),
        "H_AXIS_SURVIVES": (axis_ok, f"ETA2_LAD > ETA2_STAT at {int((head['eta2_lad'] > head['eta2_stat']).sum())} "
                                     f"of {len(head)} dial point x panel cells"),
        "H_DISTANCE": (abs(rho_snr) > abs(rho_k), f"|rho(spread/gap)| {abs(rho_snr):.4f} vs "
                                                  f"|rho(rung count)| {abs(rho_k):.4f}"),
    }
    P("## HYPOTHESES, declared before any number")
    for k, (ok, why) in H.items():
        P(f"  {'SUPPORTED' if ok else 'REFUTED  '}  {k:16s} {why}")
    P(f"  {sum(1 for v in H.values() if v[0])} of {len(H)} SUPPORTED")
    dump(pd.DataFrame([dict(hypothesis=k, supported=v[0], evidence=v[1]) for k, v in H.items()]), "hypotheses")

    P(f"\n# done in {time.time() - t0:.0f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

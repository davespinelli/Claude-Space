#!/usr/bin/env python3
"""Idea 1109 (cloud lane, idea 1 of 2, 2026-09-16)
   does-any-committed-GRID-EDGE-ARGMAX-survive-being-read-as-a-BOUNDARY-PICK

1102's D1 found all 6 of its RESOLVED argmaxes sit at ladder ENDS of the monotone GROSS
dial.  This run censuses the record's COMMITTED argmax claims — the 32 (panel x ladder x
statistic) peaks 1102 and 1110 published, re-derived here from the tape and gated against
their committed CSVs — for which sit at a ladder END, re-reads those as BOUNDARY PICKS, and
then does the one thing that decides the re-reading: it EXTENDS each ladder past the end the
argmax sits on and asks whether the peak MOVES.  A peak that moves outward was never an
optimum; it was a statement about where the grid stopped.

TUNED DIALS (2, PROTOCOL rule 4): CLAIM SET {CS_ALL32, CS_RESOLVED, CS_DECIDED} x EDGE RULE
{E_END, E_OUTER2} = 6 combinations, ALL published.  PANEL, LADDER and STATISTIC are not
dials — all 32 cells are reported under every combination.  The EXTENSION set is NOT a dial:
it is pre-registered below, fixed before any number was read, and never selected on.

FROZEN at 1082/1094/1098/1102/1108/1110's construction: CAND20 legs [(21,252),(0,126),(0,63)],
cap INF, max_vol 0.60, gross 0.75 (except on GROSS), W cadence (except on CADENCE), min hold
126 (except on H), N=20 (except on N), 10 bps, LAG 1, warm-up 260, IS end 2016-12-31, block
L=63, 1000 draws, crc32 seeds (1108's repair), q=0.90 headline.

Standalone, deterministic, offline.  Writes <stem>.{grid,census,claimsets,extension,
walkforward,gates,hypotheses}.csv beside itself.
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
SLUG = "does-any-committed-GRID-EDGE-ARGMAX-survive-being-read-as-a-BOUNDARY-PICK"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"
BT = Path(__file__).resolve().parent
PRIOR1110 = BT / "2026-09-16_what-does-the-RECORD-LOSE-if-the-FLOOR-CLAUSE-is-ENACTED-AS-WRITTEN_C"

LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST, GROSS0, FREQ0, HOLD0, N0 = 10.0, 0.75, "W", 126, 20
LEGS = [(21, 252), (0, 126), (0, 63)]

# ---- the record's CORE ladders (1102/1110's, verbatim) and this run's PRE-REGISTERED extensions
LAD_N = [5, 8, 10, 12, 15, 20, 25, 30, 40]
LAD_H = [21, 63, 126, 252]
LAD_G = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]
LAD_C = ["D", "W", "M", "Q"]
CORE = {"N": LAD_N, "H": LAD_H, "GROSS": LAD_G, "CADENCE": LAD_C}
# low-end extension, high-end extension.  GROSS stops at 1.00 (PROTOCOL rule 2: no leverage).
# CADENCE cannot be extended BELOW daily — engine.rebalance_mask serves no finer bar.
EXT_LO = {"N": [3, 4], "H": [5, 10], "GROSS": [0.20, 0.25], "CADENCE": []}
EXT_HI = {"N": [50, 60], "H": [378, 504], "GROSS": [0.80, 0.85, 0.90, 0.95, 1.00],
          "CADENCE": ["2Q", "4Q"]}

STATS = ["S_FULL", "S_OOS", "CAGR", "DD"]
SCALE = {"S_FULL": 1.0, "S_OOS": 1.0, "CAGR": 100.0, "DD": 100.0}   # 1102's published units
PANELS = ["U56", "B136"]
CHOOSERS = ["C_ISSHARPE", "C_ISCAGR", "C_ISDD"]

CLAIMSETS = ["CS_ALL32", "CS_RESOLVED", "CS_DECIDED"]      # dial 1
EDGERULES = ["E_END", "E_OUTER2"]                          # dial 2
Q_HEAD, L_HEAD, BDRAWS = 0.90, 63, 1000
SEED_BOOT = 11091109

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


def legs_4a(b, lb):
    return {"A_H1": bool(b["H1"] > lb["H1"]), "A_H2": bool(b["H2"] > lb["H2"]),
            "A_DD": bool(b["MaxDD"] >= lb["MaxDD"])}


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


def floor_from_agreement(gaps, agree, q):
    """1098's floor: the smallest gap above which EVERY pair is resolved at q. inf if the
    largest gap in the ladder is itself un-resolved."""
    gaps = np.asarray(gaps, float)
    agree = np.asarray(agree, float)
    un = agree < q
    largest_un = float(gaps[un].max()) if un.any() else 0.0
    ok = (~un) & (gaps > largest_un)
    flo = float(gaps[ok].min()) if ok.any() else float("inf")
    return flo, largest_un, int(un.sum())


def agree_of(vals, boot, q):
    """Per-ladder floor and the symmetric agreement matrix behind it."""
    k = len(vals)
    A = np.full((k, k), np.nan)
    np.fill_diagonal(A, 1.0)
    gaps, agr = [], []
    for i, j in combinations(range(k), 2):
        g = vals[i] - vals[j]
        if not np.isfinite(g):
            continue
        d = boot[i] - boot[j]
        d = d[np.isfinite(d)]
        a = float((np.sign(d) == np.sign(g)).mean()) if len(d) else np.nan
        A[i, j] = A[j, i] = a
        gaps.append(abs(g))
        agr.append(a)
    flo, lun, nun = floor_from_agreement(np.array(gaps), np.array(agr), q)
    return A, flo, lun, nun


def tie_set(vals, peak, flo):
    s = {peak}
    for j in range(len(vals)):
        if np.isfinite(vals[j]) and abs(vals[peak] - vals[j]) < flo:
            s.add(j)
    return sorted(s)


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 3:
        return np.nan
    ra = pd.Series(a[m]).rank().values
    rb = pd.Series(b[m]).rank().values
    ra = ra - ra.mean()
    rb = rb - rb.mean()
    den = np.sqrt((ra ** 2).sum() * (rb ** 2).sum())
    return float((ra * rb).sum() / den) if den else np.nan


# ------------------------------------------------------------------- cadence beyond D/W/M/Q
def cadence_mask(idx, spec):
    """engine.rebalance_mask for D/W/M/Q, verbatim (gate G7).  '<k>Q' keeps every k-th
    quarter-end, i.e. the cadences engine.rebalance_mask does NOT serve.  Nothing finer than
    'D' exists on a daily bar, so the CADENCE ladder has NO low-end extension."""
    if spec in ("D", "W", "M", "Q"):
        return rebalance_mask(idx, spec).values.copy()
    assert spec.endswith("Q")
    k = int(spec[:-1])
    base = np.flatnonzero(rebalance_mask(idx, "Q").values)
    m = np.zeros(len(idx), dtype=bool)
    m[base[::k]] = True
    return m


def main():
    t0 = time.time()
    P(f"# Idea 1109 (cloud lane, idea 1 of 2, {DATE}) — does any committed GRID-EDGE ARGMAX")
    P("#   survive being read as a BOUNDARY PICK?")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4): CLAIM SET {CLAIMSETS} x EDGE RULE {EDGERULES}")
    P(f"#   = {len(CLAIMSETS) * len(EDGERULES)} combinations, ALL published.  PANEL, LADDER, "
      "STATISTIC are not dials (all 32 cells reported under each).")
    P("# NOT A DIAL: the EXTENSION set, fixed before any number was read —")
    for lad in CORE:
        P(f"#   {lad:8s} CORE {CORE[lad]}  +LO {EXT_LO[lad]}  +HI {EXT_HI[lad]}")
    P("#   GROSS stops at 1.00 (PROTOCOL rule 2, no leverage); CADENCE has NO low-end "
      "extension (nothing is finer than a daily bar).")
    P(f"# FROZEN: CAND20 legs {LEGS}, cap INF, max_vol {MAXVOL}, gross {GROSS0}, cadence "
      f"{FREQ0}, min hold {HOLD0}, N {N0},")
    P(f"#   {COST:.0f} bps, LAG {LAG}, warm-up {WARMUP}, IS end {IS_END}, block L={L_HEAD}, "
      f"{BDRAWS} draws, crc32 seeds, q={Q_HEAD}.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   (a) H_EDGE_MAJORITY   > 50% of the 32 committed argmaxes sit at a ladder END.")
    P("#   (b) H_EDGE_EXCESS     that share exceeds the random-argmax null share (mean 2/k).")
    P("#   (c) H_RESOLVED_EDGE   1102's D1 reproduces: EVERY RESOLVED argmax is a ladder end.")
    P("#   (d) H_MONO            a majority of EDGE cells sit on a monotone ladder "
      "(|Spearman(rung, stat)| >= 0.70), i.e. carry no interior optimum.")
    P("#   (e) H_EXT_MOVES       extending the binding end moves the argmax OUTWARD in a "
      "majority of EDGE cells — the published optimum was a grid-edge statement.")
    P("#   (f) H_SPREAD_TRIVIAL  a majority of EDGE cells have whole-ladder spread BELOW "
      "their own resolution floor (the argmax decides nothing at all).")
    P("#   (g) NOT A KEEP PATH   this run proposes no book; 4a/4b and rule 8 are scored at "
      "every rung anyway because rule 4 requires it.")
    P("")

    gaterows, gates = [], {}

    # ------------------------------------------------------------------------------- PANELS
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

    # G1 fast runner == engine.backtest
    mk = rebalance_mask(d["idx"], FREQ0).values
    W = build(-d["sc"], d["elig"], d["priced"], np.flatnonzero(mk), N0, HOLD0, d["T"], d["K"], GROSS0)
    Wdf = pd.DataFrame(W, index=d["idx"], columns=d["px"].columns)
    eng = backtest(d["px"], Wdf, cost_bps=COST, freq=FREQ0)["returns"].values
    rfast, tn0 = run_cell("U56", N0, HOLD0, GROSS0, FREQ0)
    g1 = float(np.abs(eng[d["warm"]] - rfast[d["warm"]]).max())
    gates["G1"] = g1 < 1e-12
    gaterows.append(dict(gate="G1", what="fast runner == engine.backtest (U56 W/H126/N20)", value=g1, pass_=gates["G1"]))
    P(f"  G1  fast runner == engine.backtest                        {g1:.2e}   {'PASS' if gates['G1'] else 'FAIL'}")

    # G2 committed anchor triple
    m = blocks_m(rfast, d["warm"], d["ins"], d["oos"])
    g2 = max(abs(m["CAGR"] - A936_WH126[0]), abs(m["Sharpe"] - A936_WH126[1]), abs(m["MaxDD"] - A936_WH126[2]))
    gates["G2"] = g2 < 5e-5
    gaterows.append(dict(gate="G2", what="CROSS-RUN committed U56 W/H126/N=20 triple", value=g2, pass_=gates["G2"]))
    P(f"  G2  CROSS-RUN committed U56 W/H126/N=20 triple            {g2:.2e}   "
      f"{'PASS' if gates['G2'] else 'FAIL'}  ({m['CAGR']:.4%} / {m['Sharpe']:.4f} / {m['MaxDD']:.4%})")

    # G3 SPY OOS
    spy_u = d["px"]["SPY"].pct_change().fillna(0.0).values
    sm = blocks_m(spy_u, d["warm"], d["ins"], d["oos"])
    g3 = max(abs(sm["OOS_CAGR"] - SPY_OOS_COMMITTED[0]), abs(sm["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
             abs(sm["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gates["G3"] = g3 < 5e-4
    gaterows.append(dict(gate="G3", what="SPY OOS triple", value=g3, pass_=gates["G3"]))
    P(f"  G3  SPY OOS triple                                        {g3:.2e}   {'PASS' if gates['G3'] else 'FAIL'}")

    # G4 / G4b committed n=12 / n=15
    r12, _ = run_cell("U56", 12, HOLD0, GROSS0, FREQ0)
    m12 = blocks_m(r12, d["warm"], d["ins"], d["oos"])
    g4 = max(abs(m12["CAGR"] - A1098_U56_N12[0]), abs(m12["Sharpe"] - A1098_U56_N12[1]), abs(m12["MaxDD"] - A1098_U56_N12[2]))
    gates["G4"] = g4 < 5e-4
    gaterows.append(dict(gate="G4", what="CROSS-RUN 1098/1102 committed U56 n=12 triple", value=g4, pass_=gates["G4"]))
    P(f"  G4  CROSS-RUN 1098/1102's committed U56 n=12 triple       {g4:.2e}   {'PASS' if gates['G4'] else 'FAIL'}")

    db = panels["B136"]
    r15, _ = run_cell("B136", 15, HOLD0, GROSS0, FREQ0)
    m15 = blocks_m(r15, db["warm"], db["ins"], db["oos"])
    g4b = max(abs(m15["CAGR"] - A1098_B136_N15[0]), abs(m15["Sharpe"] - A1098_B136_N15[1]), abs(m15["MaxDD"] - A1098_B136_N15[2]))
    gates["G4b"] = g4b < 5e-4
    gaterows.append(dict(gate="G4b", what="CROSS-RUN 1098/1102 committed B136 n=15 triple", value=g4b, pass_=gates["G4b"]))
    P(f"  G4b CROSS-RUN 1098/1102's committed B136 n=15 triple      {g4b:.2e}   {'PASS' if gates['G4b'] else 'FAIL'}")

    # G5 live RULES v2 drawdown
    lb = {}
    for panel in PANELS:
        dp = panels[panel]
        lr = backtest(dp["px"], rules_v2_weights(dp["px"]), cost_bps=COST, freq="W")["returns"].values
        lb[panel] = blocks_m(lr, dp["warm"], dp["ins"], dp["oos"])
    g5 = abs(lb["U56"]["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gates["G5"] = g5 < 5e-4
    gaterows.append(dict(gate="G5", what="live RULES v2 MaxDD -12.05% on U56", value=g5, pass_=gates["G5"]))
    P(f"  G5  live RULES v2 MaxDD == committed -12.05%              {g5:.2e}   {'PASS' if gates['G5'] else 'FAIL'}")

    # G6 determinism
    r12b, _ = run_cell("U56", 12, HOLD0, GROSS0, FREQ0)
    g6 = float(np.abs(r12 - r12b).max())
    gates["G6"] = g6 == 0.0
    gaterows.append(dict(gate="G6", what="determinism (same cell twice)", value=g6, pass_=gates["G6"]))
    P(f"  G6  determinism                                           {g6:.2e}   {'PASS' if gates['G6'] else 'FAIL'}")

    # G7 custom cadence mask == engine.rebalance_mask on D/W/M/Q
    g7 = max(int(np.abs(cadence_mask(d["idx"], f).astype(int) - rebalance_mask(d["idx"], f).values.astype(int)).sum())
             for f in LAD_C)
    gates["G7"] = g7 == 0
    gaterows.append(dict(gate="G7", what="cadence_mask == engine.rebalance_mask on D/W/M/Q", value=float(g7), pass_=gates["G7"]))
    P(f"  G7  cadence_mask == engine.rebalance_mask (D/W/M/Q)       {g7:.2e}   {'PASS' if gates['G7'] else 'FAIL'}")

    # ------------------------------------------------------------------------- THE FULL GRID
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
        spy = dp["px"]["SPY"].pct_change().fillna(0.0).values
        sb = blocks_m(spy, dp["warm"], dp["ins"], dp["oos"])
        panels[panel]["spy_m"] = sb
        for lad in CORE:
            rungs = EXT_LO[lad] + CORE[lad] + EXT_HI[lad]
            for rung in rungs:
                N, H, gr, fq = cell_params(lad, rung)
                r, tn = run_cell(panel, N, H, gr, fq)
                RET[(panel, lad, str(rung))] = r
                b = blocks_m(r, dp["warm"], dp["ins"], dp["oos"])
                row = dict(panel=panel, ladder=lad, rung=str(rung), in_core=rung in CORE[lad],
                           N=N, H=H, gross=gr, freq=fq,
                           turnover=float(tn[dp["warm"]].sum()) / (dp["warm"].sum() / 252.0), **b)
                row.update(legs_4b(b, sb))
                row.update(legs_4b_oos(b, sb))
                row.update(legs_4a(b, lb[panel]))
                row["pass_4b_full"] = all(row[k] for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                row["pass_4b_oos"] = all(row[k] for k in ("O_S", "O_DD", "O_CAGR"))
                row["pass_4a"] = all(row[k] for k in ("A_H1", "A_H2", "A_DD"))
                grid_rows.append(row)
    G = pd.DataFrame(grid_rows)
    P(f"  built {len(G):,} books ({len(G[G.in_core]):,} CORE + {len(G[~G.in_core]):,} EXTENSION) "
      f"in {time.time() - t0:.0f}s")

    # G8/G9 reproduction of 1110's committed grid and 1102/1110's committed peaks
    prior_grid = pd.read_csv(f"{PRIOR1110}.grid.csv", dtype=str, keep_default_na=False)
    pg = prior_grid.copy()
    for c in ("turnover", "CAGR", "Sharpe", "MaxDD", "OOS_Sharpe"):
        pg[c] = pg[c].astype(float)
    mine = G[G.in_core].set_index(["panel", "ladder", "rung"])
    dev = []
    for _, r in pg.iterrows():
        key = (r["panel"], r["ladder"], r["rung"])
        if key not in mine.index:
            dev.append(np.inf)
            continue
        mrow = mine.loc[key]
        dev.append(max(abs(mrow["CAGR"] - r["CAGR"]), abs(mrow["Sharpe"] - r["Sharpe"]),
                       abs(mrow["MaxDD"] - r["MaxDD"]), abs(mrow["OOS_Sharpe"] - r["OOS_Sharpe"]),
                       abs(mrow["turnover"] - r["turnover"])))
    g8 = float(np.max(dev))
    gates["G8"] = g8 < 1e-9 and len(pg) == 54
    gaterows.append(dict(gate="G8", what=f"reproduce 1110's committed grid ({len(pg)} rows, 5 cols each)",
                         value=g8, pass_=gates["G8"]))
    P(f"  G8  reproduce 1110's committed {len(pg)}-row CORE grid         {g8:.2e}   "
      f"{'PASS' if gates['G8'] else 'FAIL'}")

    # --------------------------------------------------------- CORE census: peaks and floors
    STATCOL = {"S_FULL": "Sharpe", "S_OOS": "OOS_Sharpe", "CAGR": "CAGR", "DD": "MaxDD"}
    census, boots = [], {}
    for panel in PANELS:
        dp = panels[panel]
        for lad in CORE:
            allr = EXT_LO[lad] + CORE[lad] + EXT_HI[lad]
            Rw = np.array([RET[(panel, lad, str(x))][dp["warm"]] for x in allr])
            Ro = np.array([RET[(panel, lad, str(x))][dp["oos"]] for x in allr])
            rng = np.random.default_rng(seed_of(panel, lad, "warm"))
            iw, nbw = block_index(rng, Rw.shape[1], L_HEAD, BDRAWS)
            cagb, shpb = boot_exact(Rw, iw, nbw, L_HEAD)
            ddb = boot_maxdd(Rw, iw)
            rng2 = np.random.default_rng(seed_of(panel, lad, "oos"))
            io, nbo = block_index(rng2, Ro.shape[1], L_HEAD, BDRAWS)
            _, shpo = boot_exact(Ro, io, nbo, L_HEAD)
            boots[(panel, lad)] = dict(rungs=allr, S_FULL=shpb, S_OOS=shpo,
                                       CAGR=cagb * 100.0, DD=ddb * 100.0)
    P(f"  bootstrap done at {time.time() - t0:.0f}s ({BDRAWS} draws, L={L_HEAD})")

    def census_one(panel, lad, stat, rung_set):
        """Peak, floor, tie set and boundary reading of one ladder restricted to rung_set."""
        allr = boots[(panel, lad)]["rungs"]
        pos = [allr.index(x) for x in rung_set]
        vals = np.array([G[(G.panel == panel) & (G.ladder == lad) & (G.rung == str(x))][STATCOL[stat]].iloc[0]
                         for x in rung_set], float) * SCALE[stat]
        bt = boots[(panel, lad)][stat][pos, :]
        A, flo, lun, nun = agree_of(vals, bt, Q_HEAD)
        pk = int(np.nanargmax(vals))
        srt = np.sort(vals)[::-1]
        gap = float(srt[0] - srt[1])
        spread = float(np.nanmax(vals) - np.nanmin(vals))
        ties = tie_set(vals, pk, flo)
        rho = spearman(np.arange(len(vals)), vals)
        return dict(peak_i=pk, peak=str(rung_set[pk]), k=len(rung_set), gap=gap, spread=spread,
                    floor=flo, n_unres=nun, tie_n=len(ties),
                    tie_set=str([str(rung_set[j]) for j in ties]), rho=rho, vals=vals)

    for panel in PANELS:
        for lad in CORE:
            for stat in STATS:
                c = census_one(panel, lad, stat, CORE[lad])
                k = c["k"]
                census.append(dict(panel=panel, ladder=lad, stat=stat, k=k, peak=c["peak"],
                                   peak_i=c["peak_i"],
                                   E_END=bool(c["peak_i"] in (0, k - 1)),
                                   E_OUTER2=bool(c["peak_i"] in (0, 1, k - 2, k - 1)),
                                   gap=c["gap"], spread=c["spread"], floor=c["floor"],
                                   resolved=bool(np.isfinite(c["floor"])),
                                   decided=bool(c["tie_n"] == 1), tie_n=c["tie_n"],
                                   tie_set=c["tie_set"], rho=c["rho"],
                                   monotone=bool(abs(c["rho"]) >= 0.70),
                                   spread_lt_floor=bool(c["spread"] < c["floor"]),
                                   gap_lt_floor=bool(c["gap"] < c["floor"]),
                                   null_end=2.0 / k, null_outer2=min(4.0, k) / k))
    C = pd.DataFrame(census)

    # G9 — the committed peaks
    cross = pd.read_csv(f"{PRIOR1110}.cross1102.csv", dtype=str, keep_default_na=False)
    mism, gapdev = 0, []
    cix = C.set_index(["panel", "ladder", "stat"])
    for _, r in cross.iterrows():
        key = (r["panel"], r["ladder"], r["stat"])
        mp = cix.loc[key, "peak"]
        cp = r["peak_1102"]
        same = (mp == cp) or (abs(float(mp) - float(cp)) < 1e-9 if _isnum(mp) and _isnum(cp) else False)
        mism += 0 if same else 1
        gapdev.append(abs(float(cix.loc[key, "gap"]) - float(r["gap_1102"])))
    g9 = float(np.max(gapdev))
    gates["G9"] = mism == 0 and g9 < 1e-6 and len(cross) == 32
    gaterows.append(dict(gate="G9", what=f"reproduce 1102/1110's {len(cross)} committed peaks and gaps",
                         value=g9, pass_=gates["G9"]))
    P(f"  G9  reproduce 1102/1110's {len(cross)} committed argmaxes       {g9:.2e}   "
      f"{'PASS' if gates['G9'] else 'FAIL'}  ({mism} peak mismatches)")

    # G10 — every ladder is live (non-zero spread at every statistic)
    g10 = float(C["spread"].min())
    gates["G10"] = g10 > 0
    gaterows.append(dict(gate="G10", what="every ladder x statistic has a live spread", value=g10, pass_=gates["G10"]))
    P(f"  G10 every ladder x statistic is LIVE (min spread)         {g10:.2e}   {'PASS' if gates['G10'] else 'FAIL'}")
    P(f"  GATES: {sum(gates.values())} of {len(gates)} PASS")
    dump(pd.DataFrame(gaterows), "gates")
    P("")

    # -------------------------------------------------------------- THE 6 PUBLISHED DIAL POINTS
    P("## THE CENSUS — all 6 dial points (CLAIM SET x EDGE RULE), every one published")
    sets = {"CS_ALL32": C,
            "CS_RESOLVED": C[C.resolved],
            "CS_DECIDED": C[C.decided]}
    crows = []
    for cs in CLAIMSETS:
        sub = sets[cs]
        for er in EDGERULES:
            nullcol = "null_end" if er == "E_END" else "null_outer2"
            n = len(sub)
            e = int(sub[er].sum()) if n else 0
            crows.append(dict(claimset=cs, edge_rule=er, claims=n, edge=e,
                              share=(e / n if n else np.nan),
                              null_share=float(sub[nullcol].mean()) if n else np.nan,
                              excess=((e / n) - float(sub[nullcol].mean())) if n else np.nan,
                              mono_edge=int(sub[sub[er]]["monotone"].sum()) if n else 0,
                              spread_lt_floor=int(sub[sub[er]]["spread_lt_floor"].sum()) if n else 0))
    CS = pd.DataFrame(crows)
    P(CS.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(CS, "claimsets")
    P("")

    # --------------------------------------------------------------------- THE EXTENSION ARM
    P("## THE EXTENSION ARM — does the peak MOVE when the binding end is extended?")
    ext_rows = []
    for _, r in C.iterrows():
        lad, panel, stat = r["ladder"], r["panel"], r["stat"]
        allr = EXT_LO[lad] + CORE[lad] + EXT_HI[lad]
        c2 = census_one(panel, lad, stat, allr)
        core_peak = r["peak"]
        new_peak = c2["peak"]
        moved = new_peak != core_peak
        outward = moved and (new_peak in [str(x) for x in EXT_LO[lad] + EXT_HI[lad]])
        side = ("LO" if r["peak_i"] == 0 else "HI") if r["E_END"] else ""
        extendable = bool(EXT_LO[lad]) if side == "LO" else (bool(EXT_HI[lad]) if side == "HI" else None)
        ext_rows.append(dict(panel=panel, ladder=lad, stat=stat, core_k=r["k"], core_peak=core_peak,
                             edge=bool(r["E_END"]), side=side, extendable=extendable,
                             ext_k=c2["k"], ext_peak=new_peak, moved=bool(moved),
                             moved_outward=bool(outward), ext_gap=c2["gap"], ext_spread=c2["spread"],
                             ext_floor=c2["floor"], ext_tie_n=c2["tie_n"], ext_rho=c2["rho"]))
    E = pd.DataFrame(ext_rows)
    dump(E, "extension")
    edge = E[E.edge & (E.extendable == True)]  # noqa: E712
    P(f"  EDGE cells with an extendable side: {len(edge)} of {int(E.edge.sum())} edge cells "
      f"({int((E.edge & (E.extendable == False)).sum())} sit on the one end that cannot be "  # noqa: E712
      "extended — CADENCE's daily bar)")
    P(f"  peak MOVES on extension:           {int(edge.moved.sum())} of {len(edge)}")
    P(f"  peak moves ONTO a NEW rung:        {int(edge.moved_outward.sum())} of {len(edge)}")
    inter = E[~E.edge]
    P(f"  INTERIOR cells (control) that move: {int(inter.moved.sum())} of {len(inter)}")
    P("")
    P("  per cell (EDGE cells only):")
    P(edge[["panel", "ladder", "stat", "core_k", "core_peak", "side", "ext_k", "ext_peak",
            "moved", "moved_outward", "ext_spread", "ext_floor"]].to_string(
        index=False, float_format=lambda x: f"{x:.4f}"))
    P("")

    P("## THE FULL 32-CELL CENSUS")
    P(C[["panel", "ladder", "stat", "k", "peak", "peak_i", "E_END", "E_OUTER2", "gap", "spread",
         "floor", "resolved", "decided", "tie_n", "rho", "monotone", "spread_lt_floor"]].to_string(
        index=False, float_format=lambda x: f"{x:.4f}"))
    dump(C.drop(columns=[]), "census")
    dump(G, "grid")
    P("")

    # ------------------------------------------------------- RULE 8 + BOTH KEEP PATHS (rule 4)
    P("## RULE 8 WALK-FORWARD AND BOTH KEEP PATHS")
    wf = []
    for panel in PANELS:
        dp = panels[panel]
        sb = dp["spy_m"]
        for lad in CORE:
            for scope, rungs in (("CORE", CORE[lad]), ("EXTENDED", EXT_LO[lad] + CORE[lad] + EXT_HI[lad])):
                sub = G[(G.panel == panel) & (G.ladder == lad) & (G.rung.isin([str(x) for x in rungs]))]
                for ch in CHOOSERS:
                    col = {"C_ISSHARPE": "IS_Sharpe", "C_ISCAGR": "IS_CAGR", "C_ISDD": "IS_MaxDD"}[ch]
                    pick = sub.loc[sub[col].idxmax()]
                    best_oos = sub.loc[sub["OOS_Sharpe"].idxmax()]
                    wf.append(dict(panel=panel, ladder=lad, scope=scope, chooser=ch,
                                   pick=pick["rung"], pick_is_new_rung=not bool(pick["in_core"]),
                                   OOS_CAGR=pick["OOS_CAGR"], OOS_Sharpe=pick["OOS_Sharpe"],
                                   OOS_MaxDD=pick["OOS_MaxDD"], CAGR=pick["CAGR"],
                                   Sharpe=pick["Sharpe"], MaxDD=pick["MaxDD"],
                                   H1=pick["H1"], H2=pick["H2"],
                                   pass_4b_full=bool(pick["pass_4b_full"]),
                                   pass_4b_oos=bool(pick["pass_4b_oos"]), pass_4a=bool(pick["pass_4a"]),
                                   regret=float(best_oos["OOS_Sharpe"] - pick["OOS_Sharpe"]),
                                   spy_OOS_Sharpe=sb["OOS_Sharpe"], spy_OOS_CAGR=sb["OOS_CAGR"],
                                   spy_OOS_MaxDD=sb["OOS_MaxDD"]))
    WF = pd.DataFrame(wf)
    dump(WF, "walkforward")
    for panel in PANELS:
        sb, lbm = panels[panel]["spy_m"], lb[panel]
        P(f"  {panel} SPY       full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%}   "
          f"OOS {sb['OOS_CAGR']:.2%} / {sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"  {panel} RULES v2  full {lbm['CAGR']:.2%} / {lbm['Sharpe']:.4f} / {lbm['MaxDD']:.2%}   "
          f"OOS {lbm['OOS_CAGR']:.2%} / {lbm['OOS_Sharpe']:.4f} / {lbm['OOS_MaxDD']:.2%}")
    for scope in ("CORE", "EXTENDED"):
        w = WF[WF.scope == scope]
        P(f"  IS picks, {scope:8s}: {len(w)} picks — 4b full {int(w.pass_4b_full.sum())}, "
          f"4b OOS {int(w.pass_4b_oos.sum())}, 4a {int(w.pass_4a.sum())}, "
          f"median OOS Sharpe {w.OOS_Sharpe.median():.4f}, median regret {w.regret.median():+.4f}, "
          f"picks landing on a NEW rung {int(w.pick_is_new_rung.sum())}")
    for scope, mask in (("CORE", G.in_core), ("EXTENDED", pd.Series(True, index=G.index))):
        g = G[mask]
        P(f"  whole grid, {scope:8s}: {len(g)} rungs — 4b full {int(g.pass_4b_full.sum())}, "
          f"4b OOS {int(g.pass_4b_oos.sum())}, 4a {int(g.pass_4a.sum())}")
    both = G[G.pass_4b_full & G.pass_4b_oos]
    P(f"  4b full AND OOS: {len(both)} of {len(G)} rungs; on NEW (extension) rungs "
      f"{int((~both.in_core).sum())} of {int((~G.in_core).sum())}")
    P("")

    # ----------------------------------------------------------------------------- HYPOTHESES
    a32 = CS[(CS.claimset == "CS_ALL32") & (CS.edge_rule == "E_END")].iloc[0]
    res = CS[(CS.claimset == "CS_RESOLVED") & (CS.edge_rule == "E_END")].iloc[0]
    edge_end = C[C.E_END]
    H = {
        "H_EDGE_MAJORITY": (a32["share"] > 0.50, f"{a32['edge']}/{a32['claims']} = {a32['share']:.4f}"),
        "H_EDGE_EXCESS": (a32["excess"] > 0, f"share {a32['share']:.4f} vs null {a32['null_share']:.4f} "
                                             f"(excess {a32['excess']:+.4f})"),
        "H_RESOLVED_EDGE": (res["claims"] > 0 and res["edge"] == res["claims"],
                            f"{res['edge']}/{res['claims']} resolved argmaxes at a ladder end"),
        "H_MONO": (len(edge_end) > 0 and edge_end["monotone"].mean() > 0.50,
                   f"{int(edge_end['monotone'].sum())}/{len(edge_end)} edge cells monotone (|rho|>=0.70)"),
        "H_EXT_MOVES": (len(edge) > 0 and edge["moved"].mean() > 0.50,
                        f"{int(edge['moved'].sum())}/{len(edge)} extendable edge peaks move"),
        "H_SPREAD_TRIVIAL": (len(edge_end) > 0 and edge_end["spread_lt_floor"].mean() > 0.50,
                             f"{int(edge_end['spread_lt_floor'].sum())}/{len(edge_end)} edge cells "
                             "have spread below their own floor"),
    }
    P("## HYPOTHESES, declared before any number")
    for k, (ok, why) in H.items():
        P(f"  {'SUPPORTED' if ok else 'REFUTED  '}  {k:18s} {why}")
    P(f"  {sum(1 for v in H.values() if v[0])} of {len(H)} SUPPORTED")
    dump(pd.DataFrame([dict(hypothesis=k, supported=v[0], evidence=v[1]) for k, v in H.items()]), "hypotheses")

    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    P(f"\n# done in {time.time() - t0:.0f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


def _isnum(x):
    try:
        float(x)
        return True
    except (TypeError, ValueError):
        return False


if __name__ == "__main__":
    main()

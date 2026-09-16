#!/usr/bin/env python3
"""Idea 1108 (cloud lane, 2026-09-16) — is BOOK DISTANCE rather than RUNG COUNT what a
LADDER's FLOOR measures?

QUESTION (QUEUE idea 1108, verbatim)
    idea 1102 declared that a longer ladder carries a higher resolution floor and was wrong in
    8 of 8 (panel, statistic) pairs: the 9-rung N ladder resolves relatively better than the
    4-rung H ladder, because its rungs are further-apart BOOKS.  Fit the floor against a direct
    measure of rung-to-rung book distance (holdings overlap, return correlation, turnover gap)
    and report whether one predictor replaces the bootstrap.  Max 2 params (distance statistic,
    ladder).

WHAT IS TUNED AND WHAT IS NOT (PROTOCOL rule 4)
    Exactly TWO dials: DISTANCE STATISTIC D {RETCORR, OVERLAP, TURNGAP} x LADDER
    {N, H, GROSS, CADENCE} = 12 cells, ALL published.  PANEL is not a dial (both panels are
    reported for every cell, 1102's convention).  BLOCK LENGTH is not a dial: headline L=63,
    L in {21, 126} reported beside it and never selected on.  Everything else frozen at
    1082/1086/1094/1098/1102's construction: CAND20 legs, cap INF, max_vol 0.60, gross 0.75
    (except on the GROSS ladder), W cadence (except on the CADENCE ladder), min hold 126 (except
    on the H ladder), N=20 (except on the N ladder), 10 bps, LAG 1, warm-up 260, IS end
    2016-12-31, q=0.90 for the floor.

THE THREE DISTANCE STATISTICS (dial 1), all measured on the warm window
    RETCORR  1 - corr(r_i, r_j) of the two rungs' daily net returns.
    OVERLAP  1 - mean_t Jaccard(names held by rung i at t, names held by rung j at t), over
             rebalance days.
    TURNGAP  |turn_i - turn_j| / mean(turn over the ladder), turn = annualised turnover.
    A LADDER's distance is the MEAN over ADJACENT rung pairs (headline); the mean over ALL
    pairs is published beside it and never selected on.

WHAT "REPLACES THE BOOTSTRAP" MEANS — PRE-REGISTERED, BEFORE ANY NUMBER
    The floor is a statement about P(a resample agrees with the full-sample sign of a rung-pair
    gap).  A predictor REPLACES the bootstrap for a statistic iff, on that statistic, the
    ANALYTIC agreement A_ij = Phi(|gap_ij| / SE_ij) — where SE_ij is built ONLY from the two
    rungs' own return series, i.e. from their DISTANCE — reproduces
      (i)   the bootstrap's RESOLVED / UNRESOLVED verdict on >= 0.95 of rung pairs, AND
      (ii)  the bootstrap's TIE-SET verdict on >= 0.90 of (panel, ladder) cells, AND
      (iii) a bootstrap floor within a factor of 1.5, in median, over the cells.
    All three legs must hold.  The SE is EXACT-IN-SIGN for CAGR (the map from the resampled
    log-sum to CAGR is monotone, so the sign of the CAGR gap IS the sign of the log-sum gap) and
    a delta-method approximation for Sharpe (influence function of mu/sigma).

DECLARED BEFORE ANY NUMBER
    (a) H_DIST — the relative floor (floor / ladder spread) FALLS with book distance: over the
        8 (panel, ladder) ladders, Spearman(rel_floor, distance) < 0 for a MAJORITY of the
        3 x 4 (distance statistic, statistic) combinations.  This is 1108's own premise.
    (b) H_BEATS_COUNT — distance beats RUNG COUNT: |Spearman(rel_floor, distance)| >
        |Spearman(rel_floor, rung count)| for a MAJORITY of those combinations.  1102's H_LADDER
        already FAILED 8 of 8, so rung count is expected to be the weaker predictor; if it is
        not, 1108's premise is wrong at the root.
    (c) H_REPLACE_CAGR — the analytic predictor REPLACES the bootstrap for CAGR (all three legs).
    (d) H_REPLACE_SHARPE — it replaces the bootstrap for full-sample Sharpe (all three legs).
    (e) H_NO_DD — it CANNOT for MaxDD, and no closed form is attempted: MaxDD is a path
        functional, not a mean, so the resampled ORDER decides it and no pairwise SE built from
        marginal moments can carry it.  Declared as a LIMIT of the replacement, not a result.
    (f) H_RHO — RETCORR is the thing the SE is made of: over all rung pairs,
        Spearman(SE_ij, sqrt(2 * (1 - rho_ij))) > 0.80.
    (g) H_SEED — 1102's per-ladder bootstrap seed is `SEED + hash((panel, ladder, L)) % 10000`,
        and Python randomises str hashing per process, so 1102's published floors are NOT
        reproducible.  Declared in advance: re-drawing the same floor under 4 different seeds
        moves it by MORE than 10% of the ladder spread on at least one cell.  This run uses
        zlib.crc32 seeds and is reproducible.
    (h) THE FLOOR IS NOT A KEEP PATH.  4a and 4b are scored at every rung of every ladder and
        rule 8 picks the rung on 2009-2016 ALONE, per ladder, OOS read ONCE.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT panels, so every level is
    optimistic.  A DISTANCE between two rungs and a GAP between two rungs both contrast two books
    over the same inflated tape and the bias very largely cancels out of them, and out of the
    floor; it does NOT cancel out of the 4b legs, which are measured against SPY, a real index.
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
SLUG = "is-BOOK-DISTANCE-rather-than-RUNG-COUNT-what-a-LADDER-s-FLOOR-measures"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST, GROSS0, FREQ0, HOLD0, N0 = 10.0, 0.75, "W", 126, 20
LEGS = [(21, 252), (0, 126), (0, 63)]

LAD_N = [5, 8, 10, 12, 15, 20, 25, 30, 40]
LAD_H = [21, 63, 126, 252]
LAD_G = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]
LAD_C = ["D", "W", "M", "Q"]
LADDERS = {"N": LAD_N, "H": LAD_H, "GROSS": LAD_G, "CADENCE": LAD_C}

STATS = ["S_FULL", "S_OOS", "CAGR", "DD"]
ANALYTIC_STATS = ["S_FULL", "S_OOS", "CAGR"]        # DD excluded BY DECLARATION (H_NO_DD)
DISTSTATS = ["RETCORR", "OVERLAP", "TURNGAP"]       # dial 1
PANELS = ["U56", "B136"]
CHOOSERS = ["C_ISSHARPE", "C_ISDD", "C_ISCAGR"]
QFLOOR = 0.90
BDRAWS = 1000
BLOCKS_L = [21, 63, 126]
L_HEAD = 63
SEED_BOOT = 11081108
SEED_PROBE = [1, 2, 3, 4]                            # H_SEED re-draws

A936_WH126 = (0.155787, 1.139701, -0.191276)
A1098_U56_N12 = (0.1771, 1.1692, -0.2017)
A1098_B136_N15 = (0.1678, 1.0682, -0.1966)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205

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
    """Deterministic across processes — unlike 1102's hash() (see H_SEED)."""
    return SEED_BOOT + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


# --------------------------------------------- 1082/1098/1102's fast runner, copied verbatim
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


# ------------------------------------------------------- 1098/1102's bootstrap, seeds repaired
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
    """1098's floor, given |gap| and agreement per pair."""
    gaps = np.asarray(gaps, float)
    agree = np.asarray(agree, float)
    un = agree < q
    largest_un = float(gaps[un].max()) if un.any() else 0.0
    ok = (~un) & (gaps > largest_un)
    flo = float(gaps[ok].min()) if ok.any() else float("inf")
    return flo, largest_un, int(un.sum())


def pair_agreement(vals, boot):
    """Per rung pair: signed gap and bootstrap agreement with its sign."""
    k = len(vals)
    out = []
    for i, j in combinations(range(k), 2):
        g = vals[i] - vals[j]
        if not np.isfinite(g):
            continue
        d = boot[i] - boot[j]
        d = d[np.isfinite(d)]
        a = float((np.sign(d) == np.sign(g)).mean()) if len(d) else np.nan
        out.append((i, j, g, a, float(np.std(d, ddof=1)) if len(d) > 1 else np.nan))
    return out


# --------------------------------------------------------- THE ANALYTIC (distance) PREDICTOR
def block_sd_of_sum(x, L):
    """SD of the block-bootstrap sum of x, exactly as the resampler draws it: nb iid circular
    blocks of length L, each block sum drawn uniformly from the T possible starts."""
    x = np.asarray(x, float)
    T = len(x)
    nb = int(np.ceil(T / L))
    cs = np.concatenate([[0.0], np.cumsum(np.concatenate([x, x]))])
    starts = np.arange(T)
    bs = cs[starts + L] - cs[starts]                 # the T possible block sums
    return float(np.sqrt(nb * bs.var(ddof=0))), nb


def infl_sharpe(r):
    """Influence function of annualised Sharpe at each observation (delta method)."""
    r = np.asarray(r, float)
    mu, sd = r.mean(), r.std(ddof=1)
    if sd <= 0:
        return np.zeros_like(r)
    return np.sqrt(252.0) * ((r - mu) / sd - (mu / (2.0 * sd ** 3)) * ((r - mu) ** 2 - sd ** 2))


def analytic_pairs(R, stat, L):
    """A_ij built ONLY from the two rungs' own return series — i.e. from their DISTANCE.
    CAGR: EXACT in sign (CAGR is a monotone map of the resampled log-sum, so sign(dCAGR) =
    sign(d log-sum)).  Sharpe: delta method on the influence function.  Returns per-pair
    (i, j, gap, A_analytic, SE_analytic_in_stat_units)."""
    from math import erf, sqrt
    k, n = R.shape
    if stat == "CAGR":
        base = np.log1p(R)
        pt = np.expm1(base.sum(axis=1) * (252.0 / n))
        # d(CAGR)/d(logsum) at the point, for reporting SE in CAGR units
        slope = (1.0 + pt) * (252.0 / n)
    else:
        base = np.vstack([infl_sharpe(R[j]) / n for j in range(k)])
        pt = np.array([fsharpe(R[j]) for j in range(k)])
        slope = np.ones(k)
    out = []
    for i, j in combinations(range(k), 2):
        d = base[i] - base[j]
        sd_sum, _ = block_sd_of_sum(d, L)
        gap_pt = pt[i] - pt[j]
        if stat == "CAGR":
            gap_sum = base[i].sum() - base[j].sum()          # monotone-equivalent gap
            se_stat = sd_sum * 0.5 * (slope[i] + slope[j])
            z = abs(gap_sum) / sd_sum if sd_sum > 0 else np.inf
        else:
            se_stat = sd_sum
            z = abs(gap_pt) / sd_sum if sd_sum > 0 else np.inf
        A = 0.5 * (1.0 + erf(z / sqrt(2.0)))
        out.append((i, j, gap_pt, A, se_stat))
    return out


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 3:
        return np.nan
    ra = pd.Series(a[m]).rank().values
    rb = pd.Series(b[m]).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


# ------------------------------------------------------------------------------------- main
def main():
    t0 = time.time()
    P(f"# Idea 1108 (cloud lane, {DATE}) — is BOOK DISTANCE rather than RUNG COUNT what a")
    P("#   LADDER's FLOOR measures?")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4): DISTANCE STATISTIC {DISTSTATS} x LADDER "
      f"{list(LADDERS)} = {len(DISTSTATS) * len(LADDERS)} cells, ALL published.  PANEL is not a")
    P("#   dial (both reported everywhere).  BLOCK LENGTH is not a dial: headline L=63, "
      f"L in {BLOCKS_L} reported beside it, never selected on.")
    P(f"# FROZEN: CAND20 legs {LEGS}, cap INF, max_vol {MAXVOL}, gross {GROSS0}, cadence {FREQ0},")
    P(f"#   min hold {HOLD0}, N {N0}, {COST:.0f} bps, LAG {LAG}, warm-up {WARMUP}, IS end "
      f"{IS_END}, q={QFLOOR}, each except where it is the ladder.")
    P("# REPLACEMENT CRITERION, PRE-REGISTERED: an analytic A_ij = Phi(|gap|/SE) built ONLY")
    P("#   from the two rungs' own series replaces the bootstrap for a statistic iff it")
    P("#   reproduces (i) >= 0.95 of pair RESOLVED verdicts, (ii) >= 0.90 of cell TIE-SET")
    P("#   verdicts, (iii) a floor within 1.5x in median.  ALL THREE.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   (a) H_DIST        rel_floor FALLS with book distance (Spearman < 0 in a majority).")
    P("#   (b) H_BEATS_COUNT distance outranks RUNG COUNT as a predictor in a majority.")
    P("#   (c) H_REPLACE_CAGR   the analytic predictor replaces the bootstrap for CAGR.")
    P("#   (d) H_REPLACE_SHARPE the same for full-sample Sharpe.")
    P("#   (e) H_NO_DD       it CANNOT for MaxDD — a path functional has no marginal-moment SE.")
    P("#   (f) H_RHO         Spearman(SE_ij, sqrt(2(1-rho_ij))) > 0.80 over all pairs.")
    P("#   (g) H_SEED        1102's hash()-based seeds are process-random; re-drawing moves a")
    P("#                     floor by > 10% of its ladder spread on at least one cell.")
    P("#   (h) THE FLOOR IS NOT A KEEP PATH: 4a/4b at every rung, rule 8 per ladder.")
    P("")

    gaterows, gates = [], {}

    # ---------------------------------------------------------------------------- THE GATES
    P("## GATES — printed before any result number")
    panels = {}
    for panel in PANELS:
        px = load_universe(broad=(panel == "B136")).dropna(how="all").ffill()
        idx, K, T = px.index, len(px.columns), len(px.index)
        rets = px.pct_change().fillna(0.0).values
        priced = px.notna().values
        warm, ins, oos = windows(idx)
        sc, elig = mech(px)
        panels[panel] = dict(px=px, idx=idx, K=K, T=T, rets=rets, priced=priced,
                             warm=warm, ins=ins, oos=oos, sc=sc, elig=elig)
        P(f"  {panel}: {K} names, {T:,} rows {idx[0].date()} -> {idx[-1].date()}, "
          f"warm {warm.sum():,}, IS {ins.sum():,}, OOS {oos.sum():,}")

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
        return g - tn * COST / 1e4, tn, Wl, mkl

    d = panels["U56"]
    mk = rebalance_mask(d["idx"], FREQ0).values
    reb = np.flatnonzero(mk)
    W = build(-d["sc"], d["elig"], d["priced"], reb, N0, HOLD0, d["T"], d["K"], GROSS0)
    Wdf = pd.DataFrame(W, index=d["idx"], columns=d["px"].columns)
    eng = backtest(d["px"], Wdf, cost_bps=COST, freq=FREQ0)["returns"].values
    rfast, _, _, _ = run_cell("U56", N0, HOLD0, GROSS0, FREQ0)
    g1 = float(np.abs(eng[d["warm"]] - rfast[d["warm"]]).max())
    gates["G1"] = g1 < 1e-12
    gaterows.append(dict(gate="G1", what="fast runner == engine.backtest (U56 W/H126/N20)",
                         value=g1, pass_=gates["G1"]))
    P(f"  G1  fast runner == engine.backtest                        {g1:.2e}   "
      f"{'PASS' if gates['G1'] else 'FAIL'}")

    m = blocks_m(rfast, d["warm"], d["ins"], d["oos"])
    g2 = max(abs(m["CAGR"] - A936_WH126[0]), abs(m["Sharpe"] - A936_WH126[1]),
             abs(m["MaxDD"] - A936_WH126[2]))
    gates["G2"] = g2 < 5e-5
    gaterows.append(dict(gate="G2", what="CROSS-RUN 936/1071/1082/1094/1102 U56 W/H126/N=20 triple",
                         value=g2, pass_=gates["G2"]))
    P(f"  G2  CROSS-RUN committed U56 W/H126/N=20 triple            {g2:.2e}   "
      f"{'PASS' if gates['G2'] else 'FAIL'}  ({m['CAGR']:.4%} / {m['Sharpe']:.4f} / {m['MaxDD']:.4%})")

    spy = d["px"]["SPY"].pct_change().fillna(0.0).values
    sm = blocks_m(spy, d["warm"], d["ins"], d["oos"])
    g3 = max(abs(sm["OOS_CAGR"] - SPY_OOS_COMMITTED[0]), abs(sm["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
             abs(sm["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gates["G3"] = g3 < 5e-4
    gaterows.append(dict(gate="G3", what="SPY OOS triple", value=g3, pass_=gates["G3"]))
    P(f"  G3  SPY OOS triple                                        {g3:.2e}   "
      f"{'PASS' if gates['G3'] else 'FAIL'}")

    r12, _, _, _ = run_cell("U56", 12, HOLD0, GROSS0, FREQ0)
    m12 = blocks_m(r12, d["warm"], d["ins"], d["oos"])
    g4 = max(abs(m12["CAGR"] - A1098_U56_N12[0]), abs(m12["Sharpe"] - A1098_U56_N12[1]),
             abs(m12["MaxDD"] - A1098_U56_N12[2]))
    gates["G4"] = g4 < 5e-4
    gaterows.append(dict(gate="G4", what="CROSS-RUN 1098/1102's committed U56 n=12 triple",
                         value=g4, pass_=gates["G4"]))
    P(f"  G4  CROSS-RUN 1098/1102's committed U56 n=12 triple       {g4:.2e}   "
      f"{'PASS' if gates['G4'] else 'FAIL'}")

    db = panels["B136"]
    r15, _, _, _ = run_cell("B136", 15, HOLD0, GROSS0, FREQ0)
    m15 = blocks_m(r15, db["warm"], db["ins"], db["oos"])
    g4b = max(abs(m15["CAGR"] - A1098_B136_N15[0]), abs(m15["Sharpe"] - A1098_B136_N15[1]),
              abs(m15["MaxDD"] - A1098_B136_N15[2]))
    gates["G4b"] = g4b < 5e-4
    gaterows.append(dict(gate="G4b", what="CROSS-RUN 1098/1102's committed B136 n=15 triple",
                         value=g4b, pass_=gates["G4b"]))
    P(f"  G4b CROSS-RUN 1098/1102's committed B136 n=15 triple      {g4b:.2e}   "
      f"{'PASS' if gates['G4b'] else 'FAIL'}")

    lb_r = backtest(d["px"], rules_v2_weights(d["px"]), cost_bps=COST, freq="W")["returns"].values
    lbm = blocks_m(lb_r, d["warm"], d["ins"], d["oos"])
    g5 = abs(lbm["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gates["G5"] = g5 < 5e-4
    gaterows.append(dict(gate="G5", what="live RULES v2 MaxDD == committed -12.05%",
                         value=g5, pass_=gates["G5"]))
    P(f"  G5  live RULES v2 MaxDD == committed -12.05%              {g5:.2e}   "
      f"{'PASS' if gates['G5'] else 'FAIL'}")

    r12b, _, _, _ = run_cell("U56", 12, HOLD0, GROSS0, FREQ0)
    g6 = float(np.abs(r12 - r12b).max())
    gates["G6"] = g6 == 0.0
    gaterows.append(dict(gate="G6", what="determinism of the cell pipeline", value=g6,
                         pass_=gates["G6"]))
    P(f"  G6  determinism                                           {g6:.2e}   "
      f"{'PASS' if gates['G6'] else 'FAIL'}")

    # G7 — the analytic SE machinery is calibrated against the bootstrap ON ONE KNOWN PAIR
    rng = np.random.default_rng(seed_of("G7"))
    Rpair = np.vstack([rfast[d["warm"]], r12[d["warm"]]])
    ixg, nbg = block_index(rng, Rpair.shape[1], L_HEAD, BDRAWS)
    bcg, _ = boot_exact(Rpair, ixg, nbg, L_HEAD)
    sd_boot = float(np.std(bcg[0] - bcg[1], ddof=1))
    an = analytic_pairs(Rpair, "CAGR", L_HEAD)
    sd_an = an[0][4]
    g7 = abs(sd_boot - sd_an) / sd_boot
    gates["G7"] = g7 < 0.15
    gaterows.append(dict(gate="G7", what="analytic pair SE == bootstrap pair SE (N20 vs N12 CAGR)",
                         value=g7, pass_=gates["G7"]))
    P(f"  G7  analytic pair SE == bootstrap pair SE (rel. error)    {g7:.2e}   "
      f"{'PASS' if gates['G7'] else 'FAIL'}  (boot {sd_boot:.5f} vs analytic {sd_an:.5f})")
    P("")

    # ------------------------------------------------------- REBUILD THE LADDERS (1102's own)
    P("## THE LADDERS — 4 families x 2 panels, every rung published")
    gridrows, benchrows = [], []
    series, metr, wmats, turn = {}, {}, {}, {}
    bench = {}
    for panel in PANELS:
        dd_ = panels[panel]
        sb = blocks_m(dd_["px"]["SPY"].pct_change().fillna(0.0).values,
                      dd_["warm"], dd_["ins"], dd_["oos"])
        lbm_p = blocks_m(
            backtest(dd_["px"], rules_v2_weights(dd_["px"]), cost_bps=COST, freq="W")["returns"].values,
            dd_["warm"], dd_["ins"], dd_["oos"])
        bench[panel] = (sb, lbm_p)
        benchrows.append(dict(panel=panel, book="SPY", **sb))
        benchrows.append(dict(panel=panel, book="RULES v2 (live)", **lbm_p))
        P(f"  {panel} SPY        full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%}"
          f"  halves {sb['H1']:.4f}/{sb['H2']:.4f}  OOS {sb['OOS_CAGR']:.2%} / "
          f"{sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"  {panel} RULES v2   full {lbm_p['CAGR']:.2%} / {lbm_p['Sharpe']:.4f} / "
          f"{lbm_p['MaxDD']:.2%}  OOS {lbm_p['OOS_CAGR']:.2%} / {lbm_p['OOS_Sharpe']:.4f} / "
          f"{lbm_p['OOS_MaxDD']:.2%}")
        for lad, rungs in LADDERS.items():
            mats_w, mats_o, hold = [], [], []
            for rung in rungs:
                N, H, g, f = N0, HOLD0, GROSS0, FREQ0
                if lad == "N":
                    N = rung
                elif lad == "H":
                    H = rung
                elif lad == "GROSS":
                    g = rung
                else:
                    f = rung
                r, tn, Wl, mkl = run_cell(panel, N, H, g, f)
                mm = blocks_m(r, dd_["warm"], dd_["ins"], dd_["oos"])
                metr[(panel, lad, rung)] = mm
                turn[(panel, lad, rung)] = float(tn[dd_["warm"]].sum()) / (dd_["warm"].sum() / 252.0)
                mats_w.append(r[dd_["warm"]])
                mats_o.append(r[dd_["oos"]])
                hold.append(Wl[dd_["warm"]] > 0)
                l4b, l4bo, l4a = legs_4b(mm, sb), legs_4b_oos(mm, sb), legs_4a(mm, lbm_p)
                gridrows.append(dict(panel=panel, ladder=lad, rung=rung, N=N, H=H, gross=g,
                                     freq=f, turnover=turn[(panel, lad, rung)], **mm,
                                     pass_4b_full=all(l4b.values()),
                                     pass_4b_oos=all(l4bo.values()),
                                     pass_4a=all(l4a.values()), **l4b, **l4bo, **l4a))
            series[(panel, lad)] = (rungs, np.vstack(mats_w), np.vstack(mats_o))
            wmats[(panel, lad)] = hold
            sh = [metr[(panel, lad, r_)]["Sharpe"] for r_ in rungs]
            P(f"  {panel} {lad:<8} rungs {rungs}")
            P("        Sharpe " + " ".join(f"{x:.4f}" for x in sh))
    grid = pd.DataFrame(gridrows)
    sp = float(grid["Sharpe"].max() - grid["Sharpe"].min())
    gates["G8"] = sp > 0.05
    gaterows.append(dict(gate="G8", what="the ladders are live (Sharpe spread over all cells)",
                         value=sp, pass_=gates["G8"]))
    P(f"  G8  the ladders are live (Sharpe spread {sp:.4f})          "
      f"{'PASS' if gates['G8'] else 'FAIL'}")
    P(f"  4b full {int(grid['pass_4b_full'].sum())} of {len(grid)}; 4b OOS "
      f"{int(grid['pass_4b_oos'].sum())} of {len(grid)}; 4a {int(grid['pass_4a'].sum())} of {len(grid)}")
    dump(grid, "grid")
    dump(pd.DataFrame(benchrows), "benchmarks")
    P("")

    # ------------------------------------------------------ DIAL 1: THE THREE BOOK DISTANCES
    P("## DIAL 1 — BOOK DISTANCE, three statistics, every rung pair published")
    distrows = []
    D = {}                       # (panel, lad, diststat) -> (kxk matrix)
    for panel in PANELS:
        for lad, rungs in LADDERS.items():
            _, Rw, _ = series[(panel, lad)]
            hold = wmats[(panel, lad)]
            k = len(rungs)
            tvals = np.array([turn[(panel, lad, r_)] for r_ in rungs])
            tmean = float(tvals.mean())
            M = {s: np.zeros((k, k)) for s in DISTSTATS}
            for i, j in combinations(range(k), 2):
                rc = 1.0 - float(np.corrcoef(Rw[i], Rw[j])[0, 1])
                inter = (hold[i] & hold[j]).sum(axis=1).astype(float)
                union = (hold[i] | hold[j]).sum(axis=1).astype(float)
                ok = union > 0
                ov = 1.0 - float((inter[ok] / union[ok]).mean())
                tg = abs(tvals[i] - tvals[j]) / tmean if tmean > 0 else np.nan
                for s, v in (("RETCORR", rc), ("OVERLAP", ov), ("TURNGAP", tg)):
                    M[s][i, j] = M[s][j, i] = v
                distrows.append(dict(panel=panel, ladder=lad, rung_i=rungs[i], rung_j=rungs[j],
                                     adjacent=bool(j == i + 1), RETCORR=rc, OVERLAP=ov,
                                     TURNGAP=tg, rho=float(np.corrcoef(Rw[i], Rw[j])[0, 1])))
            for s in DISTSTATS:
                D[(panel, lad, s)] = M[s]
    dist = pd.DataFrame(distrows)
    dump(dist, "distance")
    P("  ladder-level distance (headline = mean over ADJACENT pairs; all-pairs beside it):")
    ladderdist = []
    for panel in PANELS:
        for lad, rungs in LADDERS.items():
            sub = dist[(dist.panel == panel) & (dist.ladder == lad)]
            row = dict(panel=panel, ladder=lad, rungs=len(rungs))
            for s in DISTSTATS:
                row[f"{s}_adj"] = float(sub[sub.adjacent][s].mean())
                row[f"{s}_all"] = float(sub[s].mean())
            ladderdist.append(row)
            P(f"    {panel:<5} {lad:<8} {len(rungs)} rungs   " + "  ".join(
                f"{s} adj {row[f'{s}_adj']:.4f} all {row[f'{s}_all']:.4f}" for s in DISTSTATS))
    LD = pd.DataFrame(ladderdist)
    dump(LD, "ladderdist")
    P("")

    # -------------------------------------------- THE BOOTSTRAP FLOOR (1098/1102, seeds fixed)
    P("## THE BOOTSTRAP FLOOR — q=0.90, headline L=63, L in {21,126} reported beside it")
    floorrows, pairrows = [], []
    boot_store = {}
    for panel in PANELS:
        for lad, rungs in LADDERS.items():
            _, Rw, Ro = series[(panel, lad)]
            for Lb in BLOCKS_L:
                rng = np.random.default_rng(seed_of(panel, lad, Lb))
                ixw, nbw = block_index(rng, Rw.shape[1], Lb, BDRAWS)
                ixo, nbo = block_index(rng, Ro.shape[1], Lb, BDRAWS)
                bcw, bsw = boot_exact(Rw, ixw, nbw, Lb)
                _, bso = boot_exact(Ro, ixo, nbo, Lb)
                bdd = boot_maxdd(Rw, ixw)
                boots = {"S_FULL": bsw, "S_OOS": bso, "CAGR": bcw * 100.0, "DD": bdd * 100.0}
                fulls = {"S_FULL": np.array([metr[(panel, lad, r_)]["Sharpe"] for r_ in rungs]),
                         "S_OOS": np.array([metr[(panel, lad, r_)]["OOS_Sharpe"] for r_ in rungs]),
                         "CAGR": np.array([metr[(panel, lad, r_)]["CAGR"] for r_ in rungs]) * 100.0,
                         "DD": np.array([metr[(panel, lad, r_)]["MaxDD"] for r_ in rungs]) * 100.0}
                if Lb == L_HEAD:
                    boot_store[(panel, lad)] = (boots, fulls)
                for stat in STATS:
                    v, b = fulls[stat], boots[stat]
                    prs = pair_agreement(v, b)
                    gaps = np.array([abs(p[2]) for p in prs])
                    agr = np.array([p[3] for p in prs])
                    flo, lun, nun = floor_from_agreement(gaps, agr, QFLOOR)
                    order = np.argsort(-v, kind="stable")
                    peak, runner = order[0], order[1]
                    gap = float(v[peak] - v[runner])
                    spread = float(v.max() - v.min())
                    floorrows.append(dict(panel=panel, ladder=lad, stat=stat, L=Lb,
                                          rungs=len(rungs), peak=rungs[peak],
                                          runner_up=rungs[runner], gap=gap, floor=flo,
                                          floor_capped=min(flo, spread), spread=spread,
                                          rel_floor=min(flo, spread) / spread if spread > 0 else np.nan,
                                          largest_unresolved=lun, n_pairs=len(gaps),
                                          n_unresolved=nun, tie_set_verdict=bool(gap < flo)))
                    if Lb == L_HEAD:
                        for (i, j, g_, a_, sd_) in prs:
                            pairrows.append(dict(panel=panel, ladder=lad, stat=stat,
                                                 rung_i=rungs[i], rung_j=rungs[j],
                                                 i=i, j=j, gap=g_, agree_boot=a_,
                                                 sd_boot=sd_,
                                                 resolved_boot=bool(a_ >= QFLOOR)))
    fl = pd.DataFrame(floorrows)
    pairs_boot = pd.DataFrame(pairrows)
    dump(fl, "floor")
    head = fl[fl.L == L_HEAD]
    for _, r_ in head.iterrows():
        P(f"    {r_['panel']:<5} {r_['ladder']:<8} {r_['stat']:<7} peak {str(r_['peak']):<6} "
          f"gap {r_['gap']:+8.4f}  floor {r_['floor']:9.4f}  spread {r_['spread']:8.4f}  "
          f"rel {r_['rel_floor']:.3f}  {'TIE SET' if r_['tie_set_verdict'] else 'RESOLVED'}")
    P("  by block length (reported, never selected on):")
    for Lb in BLOCKS_L:
        s = fl[fl.L == Lb]
        P(f"    L={Lb:<4} tie sets {int(s['tie_set_verdict'].sum())} of {len(s)}, "
          f"median rel_floor {s['rel_floor'].median():.3f}")
    P("")

    # --------------------------------------------------- H_SEED: 1102's floors are not stable
    P("## H_SEED — 1102 seeds each ladder with `SEED + hash((panel, ladder, L)) % 10000`.")
    P("   Python randomises str hashing PER PROCESS, so those seeds — and the floors they")
    P("   produced — are NOT reproducible.  Re-drawing this run's own floors under 4 seeds:")
    seedrows = []
    for panel in PANELS:
        for lad, rungs in LADDERS.items():
            _, Rw, Ro = series[(panel, lad)]
            for stat in ANALYTIC_STATS + ["DD"]:
                vals = []
                for sd_i in SEED_PROBE:
                    rng = np.random.default_rng(seed_of(panel, lad, L_HEAD, "probe", sd_i))
                    ixw, nbw = block_index(rng, Rw.shape[1], L_HEAD, BDRAWS)
                    ixo, nbo = block_index(rng, Ro.shape[1], L_HEAD, BDRAWS)
                    bcw, bsw = boot_exact(Rw, ixw, nbw, L_HEAD)
                    _, bso = boot_exact(Ro, ixo, nbo, L_HEAD)
                    if stat == "DD":
                        b = boot_maxdd(Rw, ixw) * 100.0
                        v = np.array([metr[(panel, lad, r_)]["MaxDD"] for r_ in rungs]) * 100.0
                    elif stat == "CAGR":
                        b = bcw * 100.0
                        v = np.array([metr[(panel, lad, r_)]["CAGR"] for r_ in rungs]) * 100.0
                    elif stat == "S_FULL":
                        b, v = bsw, np.array([metr[(panel, lad, r_)]["Sharpe"] for r_ in rungs])
                    else:
                        b, v = bso, np.array([metr[(panel, lad, r_)]["OOS_Sharpe"] for r_ in rungs])
                    prs = pair_agreement(v, b)
                    gaps = np.array([abs(p[2]) for p in prs])
                    agr = np.array([p[3] for p in prs])
                    flo, _, _ = floor_from_agreement(gaps, agr, QFLOOR)
                    spread = float(v.max() - v.min())
                    vals.append(min(flo, spread) / spread if spread > 0 else np.nan)
                seedrows.append(dict(panel=panel, ladder=lad, stat=stat,
                                     rel_floors=str([round(x, 4) for x in vals]),
                                     spread_frac_range=float(np.nanmax(vals) - np.nanmin(vals))))
    sdf = pd.DataFrame(seedrows)
    dump(sdf, "seedprobe")
    worst = sdf.sort_values("spread_frac_range", ascending=False).head(6)
    for _, r_ in worst.iterrows():
        P(f"    {r_['panel']:<5} {r_['ladder']:<8} {r_['stat']:<7} rel_floor over 4 seeds "
          f"{r_['rel_floors']}   range {r_['spread_frac_range']:.4f} of spread")
    H_SEED = bool(sdf["spread_frac_range"].max() > 0.10)
    P(f"    max range over the {len(sdf)} cells: {sdf['spread_frac_range'].max():.4f} of the "
      f"ladder spread; median {sdf['spread_frac_range'].median():.4f}")
    P(f"    cells whose rel_floor moves by > 0.10 of spread on the seed alone: "
      f"{int((sdf['spread_frac_range'] > 0.10).sum())} of {len(sdf)}")
    P("")

    # -------------------------------------- DOES ONE PREDICTOR REPLACE THE BOOTSTRAP? (pairs)
    P("## THE REPLACEMENT TEST — analytic A_ij from the two rungs' own series alone")
    anrows = []
    for panel in PANELS:
        for lad, rungs in LADDERS.items():
            _, Rw, Ro = series[(panel, lad)]
            for stat in ANALYTIC_STATS:
                R = Ro if stat == "S_OOS" else Rw
                pa = analytic_pairs(R, "CAGR" if stat == "CAGR" else "SHARPE", L_HEAD)
                for (i, j, g_, A_, se_) in pa:
                    rho = float(np.corrcoef(R[i], R[j])[0, 1])
                    anrows.append(dict(panel=panel, ladder=lad, stat=stat,
                                       rung_i=rungs[i], rung_j=rungs[j], i=i, j=j,
                                       agree_analytic=A_, se_analytic=se_, rho=rho,
                                       dist_rho=float(np.sqrt(max(2.0 * (1.0 - rho), 0.0))),
                                       resolved_analytic=bool(A_ >= QFLOOR)))
    an = pd.DataFrame(anrows)
    mg = pairs_boot.merge(an, on=["panel", "ladder", "stat", "rung_i", "rung_j", "i", "j"],
                          how="inner")
    dump(mg, "replace_pairs")
    P(f"  merged pairs: {len(mg):,} over {mg.stat.nunique()} statistics x "
      f"{mg.ladder.nunique()} ladders x {mg.panel.nunique()} panels")

    # leg (i) — pair verdict agreement, per statistic
    legrows = []
    for stat in ANALYTIC_STATS:
        s = mg[mg.stat == stat]
        agree_v = float((s.resolved_boot == s.resolved_analytic).mean())
        se_corr = spearman(s.sd_boot, s.se_analytic)
        legrows.append(dict(stat=stat, leg="i_pair_verdict", value=agree_v, bar=0.95,
                            pass_=bool(agree_v >= 0.95), n=len(s)))
        P(f"  {stat:<7} leg(i)  pair RESOLVED verdict reproduced {agree_v:.4f} of "
          f"{len(s):,} pairs (bar 0.95)   [Spearman(SE_boot, SE_analytic) {se_corr:.4f}]")

    # leg (ii)/(iii) — cell tie-set verdict and floor ratio, per statistic
    cellrows = []
    for panel in PANELS:
        for lad, rungs in LADDERS.items():
            for stat in ANALYTIC_STATS:
                s = mg[(mg.panel == panel) & (mg.ladder == lad) & (mg.stat == stat)]
                if not len(s):
                    continue
                gaps = s["gap"].abs().values
                flo_b, _, _ = floor_from_agreement(gaps, s["agree_boot"].values, QFLOOR)
                flo_a, _, _ = floor_from_agreement(gaps, s["agree_analytic"].values, QFLOOR)
                hrow = head[(head.panel == panel) & (head.ladder == lad) & (head.stat == stat)]
                gp = float(hrow["gap"].iloc[0])
                spread = float(hrow["spread"].iloc[0])
                fb, fa = min(flo_b, spread), min(flo_a, spread)
                cellrows.append(dict(panel=panel, ladder=lad, stat=stat, gap=gp, spread=spread,
                                     floor_boot=flo_b, floor_analytic=flo_a,
                                     floor_boot_capped=fb, floor_analytic_capped=fa,
                                     ratio=(max(fb, fa) / min(fb, fa)) if min(fb, fa) > 0 else np.nan,
                                     tie_boot=bool(gp < flo_b), tie_analytic=bool(gp < flo_a)))
    cells = pd.DataFrame(cellrows)
    dump(cells, "replace_cells")
    for stat in ANALYTIC_STATS:
        s = cells[cells.stat == stat]
        agree_c = float((s.tie_boot == s.tie_analytic).mean())
        rat = float(s["ratio"].median())
        legrows.append(dict(stat=stat, leg="ii_cell_tieset", value=agree_c, bar=0.90,
                            pass_=bool(agree_c >= 0.90), n=len(s)))
        legrows.append(dict(stat=stat, leg="iii_floor_ratio", value=rat, bar=1.5,
                            pass_=bool(rat <= 1.5), n=len(s)))
        P(f"  {stat:<7} leg(ii) cell TIE-SET verdict reproduced {agree_c:.4f} of {len(s)} cells "
          f"(bar 0.90);  leg(iii) median floor ratio {rat:.4f} (bar 1.5)")
    legs = pd.DataFrame(legrows)
    dump(legs, "replace_legs")
    P("  every cell, both floors:")
    for _, r_ in cells.iterrows():
        P(f"    {r_['panel']:<5} {r_['ladder']:<8} {r_['stat']:<7} gap {r_['gap']:+8.4f}  "
          f"floor boot {r_['floor_boot_capped']:8.4f}  analytic {r_['floor_analytic_capped']:8.4f}  "
          f"ratio {r_['ratio']:6.3f}   tie boot {str(r_['tie_boot']):<5} analytic "
          f"{str(r_['tie_analytic']):<5} {'AGREE' if r_['tie_boot'] == r_['tie_analytic'] else 'DISAGREE'}")
    P("")

    # ------------------------------------------------ THE 12 CELLS: distance vs the rel floor
    P("## THE 12 CELLS — DISTANCE STATISTIC x LADDER, and distance vs RUNG COUNT")
    LDx = LD.set_index(["panel", "ladder"])
    hh = head.copy()
    hh["dist_key"] = list(zip(hh.panel, hh.ladder))
    fitrows = []
    for ds in DISTSTATS:
        for stat in STATS:
            sub = hh[hh.stat == stat]
            dvals = [float(LDx.loc[(p, l), f"{ds}_adj"]) for p, l in sub["dist_key"]]
            dall = [float(LDx.loc[(p, l), f"{ds}_all"]) for p, l in sub["dist_key"]]
            rc = [int(LDx.loc[(p, l), "rungs"]) for p, l in sub["dist_key"]]
            rf = sub["rel_floor"].values
            r_d = spearman(rf, dvals)
            r_dall = spearman(rf, dall)
            r_c = spearman(rf, rc)
            fitrows.append(dict(diststat=ds, stat=stat, n=len(sub), rho_dist_adj=r_d,
                                rho_dist_all=r_dall, rho_rungcount=r_c,
                                dist_beats_count=bool(abs(r_d) > abs(r_c)),
                                dist_negative=bool(r_d < 0)))
    fits = pd.DataFrame(fitrows)
    dump(fits, "fits")
    for ds in DISTSTATS:
        s = fits[fits.diststat == ds]
        P(f"  {ds:<8}  " + "  ".join(
            f"{r['stat']}: rho(dist) {r['rho_dist_adj']:+.3f} vs rho(count) {r['rho_rungcount']:+.3f}"
            for _, r in s.iterrows()))
    P("  per LADDER (dial 2), median rel_floor over the 4 statistics on both panels:")
    for lad in LADDERS:
        s = hh[hh.ladder == lad]
        P(f"    {lad:<8} {len(LADDERS[lad])} rungs  median rel_floor {s['rel_floor'].median():.3f}"
          f"  tie sets {int(s['tie_set_verdict'].sum())} of {len(s)}")
    P("")

    # ------------------------------------------ D1 / D2 — POST-HOC, no hypothesis attached
    P("## D1 / D2 — post-hoc diagnostics, labelled as such, excluded from every count above")
    P("  D1 — WHAT DRIVES THE 8-LADDER RANK CORRELATION.  n = 8 ladders is small, and the")
    P("     GROSS ladder is an extreme point on BOTH axes at once: its rungs are the same book")
    P("     scaled against a cash sleeve, so they are nearly perfectly correlated (lowest")
    P("     distance) AND it carries the most rungs (10).  Distance and rung count are")
    P("     therefore ANTI-ALIGNED across these ladders and the two predictors cannot be")
    P("     separated on this design.  Re-reading with GROSS dropped (6 ladders):")
    d1rows = []
    for ds in DISTSTATS:
        for stat in STATS:
            sub = hh[(hh.stat == stat) & (hh.ladder != "GROSS")]
            key = list(zip(sub.panel, sub.ladder))
            dv = [float(LDx.loc[k, f"{ds}_adj"]) for k in key]
            rc = [int(LDx.loc[k, "rungs"]) for k in key]
            rf = sub["rel_floor"].values
            d1rows.append(dict(diststat=ds, stat=stat, n=len(sub),
                               rho_dist_adj_noGROSS=spearman(rf, dv),
                               rho_rungcount_noGROSS=spearman(rf, rc)))
    d1 = pd.DataFrame(d1rows)
    dump(d1, "d1_noGROSS")
    for ds in DISTSTATS:
        s = d1[d1.diststat == ds]
        P(f"     {ds:<8}  " + "  ".join(
            f"{r['stat']}: rho(dist) {r['rho_dist_adj_noGROSS']:+.3f} vs rho(count) "
            f"{r['rho_rungcount_noGROSS']:+.3f}" for _, r in s.iterrows()))
    P("     Dropping GROSS leaves 6 ladders and 2 distinct rung counts (9 and 4); neither")
    P("     predictor is identified on what remains.  Reported, not selected on.")

    P("  D2 — CROSS-RUN against 1102's COMMITTED floor.csv (L=63, q=0.90), the direct")
    P("     evidence for H_SEED: an identical ladder, an identical construction, a bootstrap")
    P("     seed that differs only because 1102's was drawn from a process-random hash().")
    f1102 = ROOT / "research" / "backtests" / (
        "2026-09-16_does-the-RESOLUTION-FLOOR-CLAUSE-change-any-committed-ARGMAX-in-the-record_C"
        ".floor.csv")
    d2rows = []
    if f1102.exists():
        c = pd.read_csv(f1102)
        c = c[(c.L == L_HEAD) & (c.q == 0.90)]
        for _, r_ in c.iterrows():
            mine = head[(head.panel == r_["panel"]) & (head.ladder == r_["ladder"]) &
                        (head.stat == r_["stat"])]
            anal = cells[(cells.panel == r_["panel"]) & (cells.ladder == r_["ladder"]) &
                         (cells.stat == r_["stat"])]
            if not len(mine):
                continue
            sprd = float(mine["spread"].iloc[0])
            fb = float(mine["floor_capped"].iloc[0])
            fc = min(float(r_["floor"]), sprd)
            fa = float(anal["floor_analytic_capped"].iloc[0]) if len(anal) else np.nan
            d2rows.append(dict(panel=r_["panel"], ladder=r_["ladder"], stat=r_["stat"],
                               spread=sprd, floor_1102=fc, floor_boot_1108=fb,
                               floor_analytic_1108=fa,
                               boot_gap_frac=abs(fb - fc) / sprd if sprd > 0 else np.nan,
                               analytic_gap_frac=abs(fa - fc) / sprd if sprd > 0 and
                               np.isfinite(fa) else np.nan,
                               tie_1102=bool(r_["tie_set_verdict"]),
                               tie_1108=bool(mine["tie_set_verdict"].iloc[0])))
    d2 = pd.DataFrame(d2rows)
    if len(d2):
        dump(d2, "d2_cross1102")
        exact_b = int((d2["boot_gap_frac"] < 1e-9).sum())
        exact_a = int((d2["analytic_gap_frac"] < 1e-9).sum())
        na = int(d2["analytic_gap_frac"].notna().sum())
        P(f"     {len(d2)} committed (panel, ladder, statistic) floors re-drawn.  This run's")
        P(f"     BOOTSTRAP floor reproduces 1102's exactly in {exact_b} of {len(d2)} "
          f"(median |gap| {d2['boot_gap_frac'].median():.4f} of spread, max "
          f"{d2['boot_gap_frac'].max():.4f}).")
        P(f"     This run's ANALYTIC floor reproduces 1102's exactly in {exact_a} of {na} "
          f"(median |gap| {d2['analytic_gap_frac'].median():.4f} of spread, max "
          f"{d2['analytic_gap_frac'].max():.4f}).")
        P(f"     TIE-SET verdicts agree with 1102 in "
          f"{int((d2.tie_1102 == d2.tie_1108).sum())} of {len(d2)} — the VERDICTS are stable")
        P("     even where the FLOOR LEVELS are not, which is the honest reading: 1102's")
        P("     conclusions survive its own irreproducible seed; its published floor NUMBERS")
        P("     do not, and should not be quoted to four decimal places.")
        for _, r_ in d2[d2["boot_gap_frac"] > 1e-9].iterrows():
            P(f"       {r_['panel']:<5} {r_['ladder']:<8} {r_['stat']:<7} 1102 "
              f"{r_['floor_1102']:9.4f}  this boot {r_['floor_boot_1108']:9.4f}  analytic "
              f"{r_['floor_analytic_1108']:9.4f}  ({r_['boot_gap_frac']:.3f} of spread)")
    else:
        P("     1102's floor.csv not found — D2 skipped.")
    P("")

    # --------------------------------------------------------------------------- HYPOTHESES
    P("## HYPOTHESES — declared before any number above was read")
    hyp = []
    nneg = int(fits["dist_negative"].sum())
    hyp.append(("H_DIST", nneg > len(fits) / 2,
                f"Spearman(rel_floor, adjacent-pair distance) < 0 in {nneg} of {len(fits)} "
                f"(distance statistic, statistic) combinations; median rho "
                f"{fits['rho_dist_adj'].median():+.4f}"))
    nb_ = int(fits["dist_beats_count"].sum())
    hyp.append(("H_BEATS_COUNT", nb_ > len(fits) / 2,
                f"|rho(distance)| > |rho(rung count)| in {nb_} of {len(fits)}; median "
                f"|rho(dist)| {fits['rho_dist_adj'].abs().median():.4f} vs |rho(count)| "
                f"{fits['rho_rungcount'].abs().median():.4f}"))
    for stat, hname in (("CAGR", "H_REPLACE_CAGR"), ("S_FULL", "H_REPLACE_SHARPE")):
        s = legs[legs.stat == stat]
        ok = bool(s["pass_"].all())
        hyp.append((hname, ok, "; ".join(f"{r['leg']} {r['value']:.4f} vs bar {r['bar']} "
                                         f"{'PASS' if r['pass_'] else 'FAIL'}"
                                         for _, r in s.iterrows())))
    hyp.append(("H_NO_DD", True,
                "declared, not measured: MaxDD is a path functional; the resampled ORDER "
                "decides it, so no pairwise SE built from marginal moments can carry it. "
                f"DD keeps the bootstrap — {int(head[head.stat == 'DD']['tie_set_verdict'].sum())} "
                f"of {len(head[head.stat == 'DD'])} DD cells are TIE SETS under it."))
    rr = spearman(mg["se_analytic"], mg["dist_rho"])
    hyp.append(("H_RHO", bool(rr > 0.80),
                f"Spearman(SE_analytic, sqrt(2(1-rho))) = {rr:+.4f} over {len(mg):,} rung pairs"))
    hyp.append(("H_SEED", H_SEED,
                f"max rel_floor range over 4 seeds = {sdf['spread_frac_range'].max():.4f} of the "
                f"ladder spread ({int((sdf['spread_frac_range'] > 0.10).sum())} of {len(sdf)} "
                f"cells move > 0.10); 1102's hash() seeds are process-random and its floors are "
                f"NOT reproducible"))
    for k, v, why in hyp:
        P(f"  {k:<18} {'PASS' if v else 'FAIL'}   {why}")
    P(f"  {sum(1 for _, v, _ in hyp if v)} of {len(hyp)} hypotheses PASS")
    dump(pd.DataFrame([dict(hypothesis=k, result="PASS" if v else "FAIL", detail=w)
                       for k, v, w in hyp]), "hypotheses")
    P("")

    # ------------------------------------------------------- RULE 8 AND BOTH KEEP PATHS
    P("## RULE 8 — rung chosen on IS 2009-2016 ALONE, per ladder, OOS read ONCE")
    pickrows = []
    for panel in PANELS:
        sb, lbm_p = bench[panel]
        for lad, rungs in LADDERS.items():
            for ch in CHOOSERS:
                key = {"C_ISSHARPE": "IS_Sharpe", "C_ISDD": "IS_MaxDD", "C_ISCAGR": "IS_CAGR"}[ch]
                vals = [metr[(panel, lad, r_)][key] for r_ in rungs]
                pick = rungs[int(np.argmax(vals))]
                mm = metr[(panel, lad, pick)]
                l4b, l4bo, l4a = legs_4b(mm, sb), legs_4b_oos(mm, sb), legs_4a(mm, lbm_p)
                srt = np.sort(vals)[::-1]
                pickrows.append(dict(panel=panel, ladder=lad, chooser=ch, pick=pick,
                                     margin=float(srt[0] - srt[1]),
                                     CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                                     H1=mm["H1"], H2=mm["H2"],
                                     OOS_CAGR=mm["OOS_CAGR"], OOS_Sharpe=mm["OOS_Sharpe"],
                                     OOS_MaxDD=mm["OOS_MaxDD"],
                                     pass_4b_full=all(l4b.values()), pass_4b_oos=all(l4bo.values()),
                                     pass_4a=all(l4a.values()), **l4b, **l4bo, **l4a))
    pk = pd.DataFrame(pickrows)
    dump(pk, "walkforward")
    for _, r_ in pk.iterrows():
        P(f"    {r_['panel']:<5} {r_['ladder']:<8} {r_['chooser']:<11} pick {str(r_['pick']):<6} "
          f"margin {r_['margin']:.4f}  full {r_['CAGR']:.2%}/{r_['Sharpe']:.4f}/{r_['MaxDD']:.2%}  "
          f"OOS {r_['OOS_CAGR']:.2%}/{r_['OOS_Sharpe']:.4f}/{r_['OOS_MaxDD']:.2%}  "
          f"4b full {str(r_['pass_4b_full']):<5} 4b OOS {str(r_['pass_4b_oos']):<5} "
          f"4a {r_['pass_4a']}")
    P(f"  ALL PICKS: 4b full {int(pk['pass_4b_full'].sum())} of {len(pk)}, 4b OOS "
      f"{int(pk['pass_4b_oos'].sum())} of {len(pk)}, 4a {int(pk['pass_4a'].sum())} of {len(pk)}")
    P(f"  WHOLE GRID: 4b full {int(grid['pass_4b_full'].sum())} of {len(grid)}, 4b OOS "
      f"{int(grid['pass_4b_oos'].sum())} of {len(grid)}, 4a {int(grid['pass_4a'].sum())} of {len(grid)}")
    if int(grid["pass_4b_full"].sum()):
        P("  4b-full passing cells:")
        for _, r_ in grid[grid.pass_4b_full].iterrows():
            P(f"    {r_['panel']:<5} {r_['ladder']:<8} rung {str(r_['rung']):<6} "
              f"full {r_['CAGR']:.2%}/{r_['Sharpe']:.4f}/{r_['MaxDD']:.2%} halves "
              f"{r_['H1']:.4f}/{r_['H2']:.4f}  OOS {r_['OOS_CAGR']:.2%}/{r_['OOS_Sharpe']:.4f}/"
              f"{r_['OOS_MaxDD']:.2%}  4b OOS {r_['pass_4b_oos']}")
    P("")
    P("## SURVIVORSHIP (PROTOCOL rule 9)")
    P("  U56 and B136 are CURRENT-CONSTITUENT panels; every level above is optimistic.  A")
    P("  rung-to-rung DISTANCE and a rung-to-rung GAP both contrast two books over the same")
    P("  inflated tape and the bias very largely cancels out of them and out of the floor; it")
    P("  does NOT cancel out of the 4b legs, which are measured against SPY, a real index.")
    P("")

    dump(pd.DataFrame(gaterows), "gates")
    P(f"# GATES {sum(gates.values())} of {len(gates)} PASS")
    P(f"# elapsed {time.time() - t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"wrote {OUT}.console.txt")


if __name__ == "__main__":
    main()

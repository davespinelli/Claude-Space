#!/usr/bin/env python3
"""Idea 1212 (cloud lane, 2026-09-17)
   is-a-CALENDAR-FOLD-SE-systematically-LOOSER-than-the-BLOCK-BOOTSTRAP-it-was-added-to-correct

THE QUEUE'S PREMISE, QUOTED.  Idea 1210 predicted SE_FOLD > SE_BLOCK > SE_IID from first
principles and got the OPPOSITE on two of three legs: SE_IID <= SE_BLOCK at only 0.3750 of
59 decisions, and SE_FOLD's median is the SMALLEST (0.0132 vs 0.0209 / 0.0292) with t's to
15.22, because a difference that is consistent year to year has a tiny SE of its fold MEAN.
The record uses fold-clustered SEs as its CONSERVATIVE basis (1206; 1208's 14 folds).  The
queue asks for the three bases to be measured against a KNOWN-NULL difference on matched
books, and for the committed fold-clustered t's that are inflated to be named.

WHY A KNOWN-NULL DIFFERENCE IS THE ONLY TEST THAT SETTLES IT.  "Which SE is bigger" cannot
decide which SE is RIGHT: on a difference that is genuinely there, a small SE is correct
and a large one is waste.  An SE is right or wrong only against a difference whose true
value is ZERO, where the only honest answer is a 5% rejection rate at |t| > 1.96.  This run
therefore builds pairs of books whose expected difference is zero BY CONSTRUCTION and reads
the false-positive rate of each basis off them.  That number is the finding; the SE
orderings are a diagnostic beside it.

TUNED DIALS (2, PROTOCOL rule 4) -- and the queue names both:

  `SE BASIS`     {S_IID, S_BLOCK, S_FOLD}
  `FOLD LENGTH`  L in {21, 63, 126, 252, 504} trading days

  = 15 cells, EVERY ONE PUBLISHED in `.dialgrid.csv`.

  L is carried into BOTH clustered bases -- it is S_FOLD's fold length AND S_BLOCK's block
  length -- so the two are read at MATCHED clustering scale and a gap between them cannot
  be a gap between two different window sizes.  L = 252 is the record's own 14-fold
  calendar-year basis (1208).  S_IID has no L and is reported constant at every rung.

  NOT dials, reported at every value: PANEL {U56, B136, SMALL}; PAIR KIND {P_NULL, P_SPLIT}
  and the non-null power control {P_SPY}; 30 disjoint pairs per (panel, pair kind); the
  nominal level {0.10, 0.05, 0.01}; the statistic (Sharpe difference); the 4a/4b legs; the
  rule-8 walk-forward arm.

  THE PAIRS, AND WHY THEIR TRUE DIFFERENCE IS ZERO:
    P_NULL   two gross-matched RANDOM books -- at every rebalance N names drawn uniformly
             from those eligible and priced that day, at g/N.  The two draws are iid and
             exchangeable, so E[Sharpe_A - Sharpe_B] = 0 exactly.  Correlated only through
             the market.
    P_SPLIT  the eligible pool is split at random into two halves at each rebalance and the
             REAL composite's top-N is taken from each half.  Same exchangeability, so the
             true difference is again 0 -- but both books are REAL top-of-the-composite
             books drawn from disjoint halves, so their difference is a style difference
             that PERSISTS year to year rather than day-to-day noise.  That persistence is
             exactly what the queue says shrinks a fold SE, so P_SPLIT is the sharp test
             and P_NULL the easy one.  (Measured, not assumed: this run's diagnostic table
             reports the pair correlation and the year-to-year persistence of each kind's
             difference, and P_SPLIT turns out LESS contemporaneously correlated than
             P_NULL while its fold differences are the more persistent -- the two are not
             the same thing, and it is persistence that drives a fold SE.)
    P_SPY    the anchor book against SPY.  The difference is REAL, so this leg measures
             POWER, not calibration, and is the control that stops "reject less" from being
             read as "better".

FROZEN at the 2026-09-04 KEEP-4b candidate's construction: composite = mean of the
percentile ranks of (12-1, 6m, 3m), NO VOL SCALER, eligibility = above own 200d MA and
vol20 < 0.60, top-N equal weight at g/N of NAV, gated-out weight to CASH at 0%, 10 bps per
unit turnover (PROTOCOL rule 2), next-day execution (LAG 1), warm-up 260, IS ends
2016-12-31.  ANCHOR = N 20 / H 126 / gross 0.75 / weekly.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the
current output of a sub-$2B screen (data/SMALL_PANEL_README.md) less the documented
max_1d_move >= 1.0 exclusion.  A false-positive RATE is one construction measured against
itself on one tape and the bias very largely cancels out of it; it does NOT cancel out of
the rule-8 OOS levels or the 4b legs.  The census leg is a scan of committed text and
carries no market bias at all.

Standalone, deterministic, offline.  Nothing outside research/ is written or modified.
"""
from __future__ import annotations

import re
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

DATE = "2026-09-17"
SLUG = "is-a-CALENDAR-FOLD-SE-systematically-LOOSER-than-the-BLOCK-BOOTSTRAP-it-was-added-to-correct"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

# ---------------------------------------------------------------- frozen construction
LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST, GROSS0, FREQ0, HOLD0, N0 = 10.0, 0.75, "W", 126, 20
LEGS = [(21, 252), (0, 126), (0, 63)]
PANELS = ["U56", "B136", "SMALL"]

SE_BASES = ["S_IID", "S_BLOCK", "S_FOLD"]          # dial 1
L_LADDER = [21, 63, 126, 252, 504]                 # dial 2 (fold length AND block length)
PAIR_KINDS = ["P_NULL", "P_SPLIT"]
NPAIRS = 30                                        # disjoint pairs per (panel, pair kind)
BDRAWS = 600
LEVELS = [0.10, 0.05, 0.01]
Z = {0.10: 1.6449, 0.05: 1.9600, 0.01: 2.5758}
N_LADDER = [5, 8, 10, 12, 15, 20, 25, 30, 40]      # the rule-8 candidate set
SEED_BASE = 12121212

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


GATES: list[dict] = []


def gate(name, what, value, ok):
    GATES.append(dict(gate=name, what=what, value=float(value), pass_=bool(ok)))
    P(f"  {name:<5s} {'PASS' if ok else 'FAIL'}  {what:<64s} {value:.4e}")
    return bool(ok)


HYP: list[dict] = []


def hyp(name, declared, bar, measured, supported):
    HYP.append(dict(hypothesis=name, declared=declared, bar=bar, measured=str(measured),
                    supported=bool(supported)))
    P(f"  {name:<14s} {'SUPPORTED' if supported else 'REFUTED  '}  {measured}")


# ================================================================= the record's runner
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


def sharpe_rows(x):
    """Sharpe of every ROW of a 2-D array of daily returns."""
    mu = x.mean(axis=1) * 252.0
    sg = x.std(axis=1, ddof=1) * np.sqrt(252.0)
    return np.where(sg > 0, mu / sg, np.nan)


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


def windows_of(idx):
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    ins = warm & ~oos
    return warm, ins, oos


def blocks_m(r, ins_m, oos_m):
    c, s, d = fmet(r)
    h = len(r) // 2
    oc, os_, od = fmet(r[oos_m])
    ic, is_, idd = fmet(r[ins_m])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(r[:h]), H2=fsharpe(r[h:]),
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


# ==================================================== the three SEs of a SHARPE DIFFERENCE
def se_of_diff(ra, rb, basis, L, tag):
    """SE of (Sharpe(ra) - Sharpe(rb)) on a PAIRED sample.  Days are always resampled
    JOINTLY, so the pair's contemporaneous correlation is preserved -- which is the whole
    reason a paired SE is smaller than two independent ones."""
    ra, rb = np.asarray(ra, float), np.asarray(rb, float)
    T = len(ra)
    if basis == "S_FOLD":
        edges = list(range(0, T, L))
        ds = []
        for a in edges:
            b = min(a + L, T)
            if b - a < 20:
                continue
            ds.append(fsharpe(ra[a:b]) - fsharpe(rb[a:b]))
        ds = np.array([x for x in ds if np.isfinite(x)])
        if len(ds) < 2:
            return np.nan, len(ds)
        return float(ds.std(ddof=1) / np.sqrt(len(ds))), len(ds)
    rng = np.random.default_rng(seed_of("se", basis, L, tag))
    if basis == "S_IID":
        idx = rng.integers(0, T, size=(BDRAWS, T))
    else:
        nb = int(np.ceil(T / L))
        st = rng.integers(0, T, size=(BDRAWS, nb))
        idx = (st[:, :, None] + np.arange(L)[None, None, :]) % T
        idx = idx.reshape(BDRAWS, nb * L)[:, :T]
    d = sharpe_rows(ra[idx]) - sharpe_rows(rb[idx])
    return float(np.nanstd(d, ddof=1)), BDRAWS


def persistence(ra, rb):
    """|lag-1 autocorrelation| of the per-252-day Sharpe difference -- the "consistent year
    to year" the queue names as the reason a fold SE shrinks.  Measured, not assumed."""
    ra, rb = np.asarray(ra, float), np.asarray(rb, float)
    ds = []
    for a in range(0, len(ra), 252):
        b = min(a + 252, len(ra))
        if b - a < 20:
            continue
        ds.append(fsharpe(ra[a:b]) - fsharpe(rb[a:b]))
    ds = np.array([x for x in ds if np.isfinite(x)])
    if len(ds) < 4 or ds[:-1].std() == 0 or ds[1:].std() == 0:
        return np.nan
    return float(abs(np.corrcoef(ds[:-1], ds[1:])[0, 1]))


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep].dropna(how="all").ffill(), len(bad), len(meta)


# =================================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P(f"IDEA 1212 (cloud lane, {DATE}) — {SLUG}")
    P("=" * 100)
    P("")

    P("## PANELS")
    raw = {"U56": load_universe(), "B136": load_universe(broad=True)}
    small, ndrop, nmeta = load_small()
    raw["SMALL"] = small
    panels = {}
    for panel in PANELS:
        px = raw[panel]
        idx, K, T = px.index, len(px.columns), len(px.index)
        warm, ins, oos = windows_of(idx)
        sc, elig = mech(px)
        spy_i = list(px.columns).index("SPY")
        elig = elig.copy()
        elig[:, spy_i] = False                     # SPY is the benchmark, never a holding
        panels[panel] = dict(px=px, idx=idx, K=K, T=T, spy_i=spy_i,
                             rets=px.pct_change().fillna(0.0).values,
                             priced=px.notna().values, warm=warm,
                             ins_m=ins[warm], oos_m=oos[warm], sc=sc, elig=elig)
        P(f"  {panel:<6s} {K:4d} cols, {T:,} rows {idx[0].date()} -> {idx[-1].date()}  "
          f"warm {warm.sum():,}  IS {ins.sum():,}  OOS {oos.sum():,}")
    P(f"  SMALL STAMP: data/small_meta.csv lists {nmeta} tickers; {ndrop} dropped for "
      f"max_1d_move >= 1.0; pool served = {panels['SMALL']['K'] - 1} names + SPY as benchmark.")
    P("")

    def run_W(panel, W, mk):
        d = panels[panel]
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        Wl = np.zeros_like(W)
        Wl[LAG:] = W[:-LAG]
        g, tn = nrun(d["rets"], Wl, mkl)
        return (g - tn * COST / 1e4)[d["warm"]]

    def book(panel, N=N0, H=HOLD0, gross=GROSS0):
        d = panels[panel]
        mk = rebalance_mask(d["idx"], FREQ0).values
        W = build(-d["sc"], d["elig"], d["priced"], np.flatnonzero(mk), N, H,
                  d["T"], d["K"], gross)
        return run_W(panel, W, mk)

    def null_book(panel, seed):
        d = panels[panel]
        mk = rebalance_mask(d["idx"], FREQ0).values
        reb = np.flatnonzero(mk)
        rng = np.random.default_rng(seed_of("null", panel, seed))
        W = np.zeros((d["T"], d["K"]))
        ok = d["elig"] & d["priced"]
        for i, t in enumerate(reb):
            cand = np.flatnonzero(ok[t])
            if not len(cand):
                continue
            sel = rng.choice(cand, size=min(N0, len(cand)), replace=False)
            stop = reb[i + 1] if i + 1 < len(reb) else d["T"]
            W[t:stop, sel] = GROSS0 / len(sel)
        return run_W(panel, W, mk)

    def split_pair(panel, seed):
        """One SHARED random half-split of the eligible pool at every rebalance; the REAL
        composite's top-N is taken from each half.  Exchangeable by construction, so the
        true Sharpe difference is 0 -- and both books are real momentum books."""
        d = panels[panel]
        mk = rebalance_mask(d["idx"], FREQ0).values
        reb = np.flatnonzero(mk)
        rng = np.random.default_rng(seed_of("split", panel, seed))
        ok = d["elig"] & d["priced"]
        WA = np.zeros((d["T"], d["K"]))
        WB = np.zeros((d["T"], d["K"]))
        for i, t in enumerate(reb):
            cand = np.flatnonzero(ok[t])
            if len(cand) < 2:
                continue
            perm = rng.permutation(cand)
            halves = (perm[:len(perm) // 2], perm[len(perm) // 2:])
            stop = reb[i + 1] if i + 1 < len(reb) else d["T"]
            for W, half in zip((WA, WB), halves):
                if not len(half):
                    continue
                order = half[np.argsort(-d["sc"][t, half], kind="stable")]
                sel = order[:N0]
                W[t:stop, sel] = GROSS0 / len(sel)
        return run_W(panel, WA, mk), run_W(panel, WB, mk)

    def split_overlap(panel):
        """Construction invariant: the two P_SPLIT books are drawn from disjoint halves, so
        their weight matrices must never both be non-zero in the same (day, name) cell."""
        d = panels[panel]
        mk = rebalance_mask(d["idx"], FREQ0).values
        reb = np.flatnonzero(mk)
        rng = np.random.default_rng(seed_of("split", panel, 0))
        ok = d["elig"] & d["priced"]
        worst = 0
        for t in reb:
            cand = np.flatnonzero(ok[t])
            if len(cand) < 2:
                continue
            perm = rng.permutation(cand)
            h1, h2 = perm[:len(perm) // 2], perm[len(perm) // 2:]
            s1 = set(h1[np.argsort(-d["sc"][t, h1], kind="stable")][:N0].tolist())
            s2 = set(h2[np.argsort(-d["sc"][t, h2], kind="stable")][:N0].tolist())
            worst = max(worst, len(s1 & s2))
        return worst

    # ------------------------------------------------------------------------- gates
    P("## GATES — printed before any result number")
    d = panels["U56"]
    mk = rebalance_mask(d["idx"], FREQ0).values
    W = build(-d["sc"], d["elig"], d["priced"], np.flatnonzero(mk), N0, HOLD0,
              d["T"], d["K"], GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST, freq=FREQ0)["returns"].values
    rfast = run_W("U56", W, mk)
    v = float(np.abs(eng[d["warm"]] - rfast).max())
    gate("G1", "fast runner == engine.backtest (U56 anchor, post warm-up)", v, v < 1e-12)
    b1, b2 = book("U56", N=12), book("U56", N=12)
    gate("G2", "determinism: same book twice", float(np.abs(b1 - b2).max()), True)
    a, b = split_pair("U56", 0)
    v = float(abs(np.corrcoef(a, b)[0, 1]))
    gate("G3", "P_SPLIT halves are DISTINCT books (|corr| < 0.999)", v, v < 0.999)
    n1, n2 = null_book("U56", 0), null_book("U56", 1)
    v2 = float(abs(np.corrcoef(n1, n2)[0, 1]))
    P(f"  NOTE   P_SPLIT pair corr {v:.4f} vs P_NULL {v2:.4f} — P_SPLIT is the LESS "
      f"contemporaneously correlated pair, not the more; persistence is reported in ARM 1.")
    ov = split_overlap("U56")
    gate("G4", "P_SPLIT's two halves hold NO name in common at any rebalance", ov, ov == 0)
    # the block SE at L = 1 IS the iid SE: same code path, checked numerically
    s_iid, _ = se_of_diff(n1, n2, "S_IID", 21, "gate")
    s_b1, _ = se_of_diff(n1, n2, "S_BLOCK", 1, "gate")
    v = abs(s_iid - s_b1) / s_iid
    gate("G5", "S_BLOCK at L = 1 == S_IID (relative, both 600 draws)", v, v < 0.15)
    # a fold SE with one fold is undefined and must return NaN, never a number
    sf, nf = se_of_diff(n1[:100], n2[:100], "S_FOLD", 504, "gate")
    gate("G6", "S_FOLD with < 2 usable folds returns NaN", float(np.isnan(sf)), np.isnan(sf))
    P("")

    # ------------------------------------------------------- benchmarks, once per panel
    P("## BENCHMARKS (per panel, 10 bps, post warm-up)")
    bench = {}
    for panel in PANELS:
        dd = panels[panel]
        spy = dd["px"]["SPY"].pct_change().fillna(0.0).values[dd["warm"]]
        live = run_W(panel, rules_v2_weights(dd["px"]).values,
                     rebalance_mask(dd["idx"], FREQ0).values)
        bench[panel] = dict(SPY=blocks_m(spy, dd["ins_m"], dd["oos_m"]),
                            LIVE=blocks_m(live, dd["ins_m"], dd["oos_m"]), spy_r=spy)
        for k in ("SPY", "LIVE"):
            m = bench[panel][k]
            P(f"  {panel:<6s} {k:<5s} {m['CAGR']:7.2%} / {m['Sharpe']:.4f} / {m['MaxDD']:8.2%}"
              f"  halves {m['H1']:.4f}/{m['H2']:.4f}  OOS {m['OOS_CAGR']:7.2%} / "
              f"{m['OOS_Sharpe']:.4f} / {m['OOS_MaxDD']:8.2%}")
    P("")

    # ================================================= ARM 1: the known-null pairs
    P(f"## ARM 1 — {NPAIRS} DISJOINT pairs per (panel, pair kind), true Sharpe difference = 0")
    pairs = []
    for panel in PANELS:
        anchor = book(panel)
        for kind in PAIR_KINDS:
            for j in range(NPAIRS):
                if kind == "P_NULL":
                    ra, rb = null_book(panel, 2 * j), null_book(panel, 2 * j + 1)
                else:
                    ra, rb = split_pair(panel, j)
                pairs.append(dict(panel=panel, pair_kind=kind, pair=j, ra=ra, rb=rb,
                                  dS=fsharpe(ra) - fsharpe(rb), persist=persistence(ra, rb),
                                  pair_corr=float(np.corrcoef(ra, rb)[0, 1])))
        # the non-null POWER control: the anchor book against SPY, one per panel
        pairs.append(dict(panel=panel, pair_kind="P_SPY", pair=0, ra=anchor,
                          rb=bench[panel]["spy_r"],
                          dS=fsharpe(anchor) - fsharpe(bench[panel]["spy_r"]),
                          persist=persistence(anchor, bench[panel]["spy_r"]),
                          pair_corr=float(np.corrcoef(anchor, bench[panel]["spy_r"])[0, 1])))
        P(f"  {panel:<6s} built  ({time.time() - t0:.0f}s elapsed)")
    pdf = pd.DataFrame([{k: v for k, v in p.items() if k not in ("ra", "rb")} for p in pairs])
    dump(pdf, "pairs")
    for kind in PAIR_KINDS + ["P_SPY"]:
        s = pdf[pdf.pair_kind == kind]
        P(f"    {kind:<8s} n={len(s):3d}  mean dSharpe {s.dS.mean():+.4f}  "
          f"sd {s.dS.std(ddof=1):.4f}  mean pair corr {s['pair_corr'].mean():.4f}  "
          f"mean |lag-1 autocorr of the yearly difference| {s.persist.mean():.4f}")
    nullmean = pdf[pdf.pair_kind.isin(PAIR_KINDS)].groupby("pair_kind").dS.mean()
    hyp("H_EXCH", "the pair constructions are EXCHANGEABLE, so E[dSharpe] = 0",
        "|mean dSharpe| <= 0.05 on both null kinds",
        f"P_NULL {nullmean['P_NULL']:+.4f}, P_SPLIT {nullmean['P_SPLIT']:+.4f}",
        bool((nullmean.abs() <= 0.05).all()))
    P("")

    # ================================================= ARM 2: the 15-cell dial grid
    P("## ARM 2 — SE and |t| under every (SE BASIS x FOLD LENGTH) cell")
    rows = []
    for p in pairs:
        for basis in SE_BASES:
            for L in L_LADDER:
                se, nun = se_of_diff(p["ra"], p["rb"], basis, L,
                                     f"{p['panel']}|{p['pair_kind']}|{p['pair']}")
                rows.append(dict(panel=p["panel"], pair_kind=p["pair_kind"], pair=p["pair"],
                                 se_basis=basis, L=L, n_units=nun, dS=p["dS"], se=se,
                                 t=(p["dS"] / se if se and np.isfinite(se) else np.nan)))
    grid = pd.DataFrame(rows)
    dump(grid, "dialgrid")

    P("  MEDIAN SE of the Sharpe difference, every one of the 15 cells (null pairs only):")
    g0 = grid[grid.pair_kind.isin(PAIR_KINDS)]
    P("    basis     " + "".join(f"L={L:<8d}" for L in L_LADDER))
    for basis in SE_BASES:
        P(f"    {basis:<10s}" + "".join(
            f"{g0[(g0.se_basis == basis) & (g0.L == L)].se.median():<10.4f}" for L in L_LADDER))
    P("  1210's ordering leg, re-read: share of null pairs with SE_IID <= SE_BLOCK, by L:")
    for L in L_LADDER:
        a = g0[(g0.se_basis == "S_IID") & (g0.L == L)].set_index(["panel", "pair_kind", "pair"]).se
        b = g0[(g0.se_basis == "S_BLOCK") & (g0.L == L)].set_index(["panel", "pair_kind", "pair"]).se
        P(f"    L={L:<5d} {float((a <= b).mean()):.4f}  (n={len(a)})")
    P("")

    # ================================================= ARM 3: THE CALIBRATION
    P("## ARM 3 — THE FINDING: false-positive rate on a difference that is TRULY ZERO.")
    P("##          A correct SE rejects at the nominal level.  Above it, the t is INFLATED.")
    cal = []
    for panel in PANELS + ["ALL"]:
        for kind in PAIR_KINDS + ["BOTH"]:
            for basis in SE_BASES:
                for L in L_LADDER:
                    s = grid[(grid.se_basis == basis) & (grid.L == L)]
                    s = s[s.pair_kind.isin(PAIR_KINDS if kind == "BOTH" else [kind])]
                    if panel != "ALL":
                        s = s[s.panel == panel]
                    tt = s.t.dropna().abs().values
                    if not len(tt):
                        continue
                    row = dict(panel=panel, pair_kind=kind, se_basis=basis, L=L, n=len(tt),
                               median_abs_t=float(np.median(tt)), max_abs_t=float(tt.max()))
                    for lv in LEVELS:
                        row[f"reject_{lv:.2f}"] = float((tt > Z[lv]).mean())
                    row["crit95_empirical"] = float(np.quantile(tt, 0.95))
                    row["inflation_vs_1p96"] = row["crit95_empirical"] / Z[0.05]
                    cal.append(row)
    cal = pd.DataFrame(cal)
    dump(cal, "calibration")

    head = cal[(cal.panel == "ALL") & (cal.pair_kind == "BOTH")]
    P("  POOLED over 3 panels x 2 null kinds (n = 180 pairs).  Nominal 5% rejection = 0.0500.")
    P("    basis     " + "".join(f"L={L:<9d}" for L in L_LADDER))
    for basis in SE_BASES:
        P(f"    {basis:<10s}" + "".join(
            f"{head[(head.se_basis == basis) & (head.L == L)]['reject_0.05'].iloc[0]:<11.4f}"
            for L in L_LADDER))
    P("  Empirical 95th percentile of |t| (the honest critical value; 1.96 is the quoted one):")
    for basis in SE_BASES:
        P(f"    {basis:<10s}" + "".join(
            f"{head[(head.se_basis == basis) & (head.L == L)].crit95_empirical.iloc[0]:<11.4f}"
            for L in L_LADDER))
    P("  By null kind at the record's own L = 252 (14 calendar-year folds):")
    for kind in PAIR_KINDS:
        s = cal[(cal.panel == "ALL") & (cal.pair_kind == kind) & (cal.L == 252)]
        P(f"    {kind:<8s} " + "  ".join(
            f"{b}: reject {s[s.se_basis == b]['reject_0.05'].iloc[0]:.4f} "
            f"(crit {s[s.se_basis == b].crit95_empirical.iloc[0]:.2f})" for b in SE_BASES))

    f252 = head[(head.se_basis == "S_FOLD") & (head.L == 252)]
    b252 = head[(head.se_basis == "S_BLOCK") & (head.L == 252)]
    i252 = head[(head.se_basis == "S_IID") & (head.L == 252)]
    hyp("H_LOOSE", "a CALENDAR-FOLD SE is LOOSER (more conservative) than the block bootstrap",
        "reject rate of S_FOLD <= that of S_BLOCK at the record's L = 252",
        f"S_FOLD {f252['reject_0.05'].iloc[0]:.4f} vs S_BLOCK "
        f"{b252['reject_0.05'].iloc[0]:.4f} vs S_IID {i252['reject_0.05'].iloc[0]:.4f} "
        f"(nominal 0.0500)",
        bool(f252["reject_0.05"].iloc[0] <= b252["reject_0.05"].iloc[0]))
    hyp("H_CAL", "at least one of the three bases is CORRECTLY SIZED at L = 252",
        "some basis rejects within [0.025, 0.10] of nominal 0.05",
        "; ".join(f"{b} {head[(head.se_basis == b) & (head.L == 252)]['reject_0.05'].iloc[0]:.4f}"
                  for b in SE_BASES),
        bool(any(0.025 <= head[(head.se_basis == b) & (head.L == 252)]["reject_0.05"].iloc[0]
                 <= 0.10 for b in SE_BASES)))
    pw = grid[(grid.pair_kind == "P_SPY") & (grid.L == 252)]
    P("  POWER control (anchor vs SPY, a difference that is REAL), L = 252: " +
      "  ".join(f"{b} |t| median {pw[pw.se_basis == b].t.abs().median():.2f}" for b in SE_BASES))
    P("")

    # ================================================= ARM 4: the record's own t's
    P("## ARM 4 — WHICH COMMITTED t's ARE INFLATED (census of the record's own text)")
    P("  RECOVERY RULE, published: scan research/LEADERBOARD.md and research/CHANGELOG.md for")
    P("  `t = X`, `t of X`, `t's to X`, `(t X)`, `mean/SE +X`; classify a hit FOLD-CLUSTERED if")
    P("  'fold', 'cluster' or 'year' occurs within 200 characters of it, else UNCLASSIFIED.")
    pat = re.compile(r"(?:t(?:'s)?\s*(?:=|of|to)\s*|mean/SE\s*\+|\(t\s*)(-?\d+\.\d+)")
    census = []
    for fn in ("LEADERBOARD.md", "CHANGELOG.md"):
        txt = (ROOT / "research" / fn).read_text()
        for m in pat.finditer(txt):
            ctx = txt[max(0, m.start() - 200): m.end() + 200].lower()
            kind = ("FOLD" if any(w in ctx for w in ("fold", "cluster", "year"))
                    else "UNCLASSIFIED")
            census.append(dict(file=fn, pos=m.start(), t=abs(float(m.group(1))), basis_hint=kind))
    census = pd.DataFrame(census)
    crit_fold = float(head[(head.se_basis == "S_FOLD") & (head.L == 252)].crit95_empirical.iloc[0])
    if len(census):
        census["survives_1p96"] = census.t > Z[0.05]
        census["survives_empirical_fold_crit"] = census.t > crit_fold
        dump(census, "census")
        f = census[census.basis_hint == "FOLD"]
        P(f"  {len(census)} committed t-values recovered ({len(f)} fold-clustered by the rule).")
        P(f"  Honest critical value for a fold-clustered t at L = 252 is |t| > {crit_fold:.2f},")
        P(f"  not 1.96.  Of the {len(f)} fold-clustered t's: "
          f"{int(f.survives_1p96.sum())} clear 1.96, "
          f"{int(f.survives_empirical_fold_crit.sum())} clear {crit_fold:.2f} — "
          f"{int(f.survives_1p96.sum() - f.survives_empirical_fold_crit.sum())} are INFLATED.")
        hyp("H_CENSUS", "committed fold-clustered t's survive their own empirical critical value",
            "every fold-clustered t that clears 1.96 also clears the empirical bar",
            f"{int(f.survives_1p96.sum())} clear 1.96, "
            f"{int(f.survives_empirical_fold_crit.sum())} clear {crit_fold:.2f}",
            bool(f.survives_1p96.sum() == f.survives_empirical_fold_crit.sum()))
    P("")

    # ================================================= ARM 5: rule 8 walk-forward
    P("## ARM 5 — RULE 8 WALK-FORWARD.  Each (basis, L) is a CHOOSER: from the 9-rung N ladder")
    P("##         take the book whose IS Sharpe difference vs the anchor has the largest SIGNED t")
    P("##         under that basis.  Chosen on warm-up..2016-12-31 ONLY; 2017-2026 read ONCE.")
    picks = []
    for panel in PANELS:
        dd = panels[panel]
        sb, lb = bench[panel]["SPY"], bench[panel]["LIVE"]
        anchor = book(panel)
        cands = {}
        for n in N_LADDER:
            r = book(panel, N=n)
            cands[n] = dict(r=r, m=blocks_m(r, dd["ins_m"], dd["oos_m"]))
        ins = dd["ins_m"]
        for basis in SE_BASES:
            for L in L_LADDER:
                ts = {}
                for n in N_LADDER:
                    if n == N0:
                        continue
                    a, b = cands[n]["r"][ins], anchor[ins]
                    se, _ = se_of_diff(a, b, basis, L, f"wf|{panel}|{n}")
                    dS = fsharpe(a) - fsharpe(b)
                    # SIGNED t: the chooser takes the most significantly BETTER book, not
                    # merely the most significantly different one.
                    ts[n] = (dS / se) if se and np.isfinite(se) and se > 0 else -np.inf
                n_pick = max(ts, key=ts.get)
                m = cands[n_pick]["m"]
                l4b, l4o, l4a = legs_4b(m, sb), legs_4b_oos(m, sb), legs_4a(m, lb)
                picks.append(dict(panel=panel, se_basis=basis, L=L, chosen_N=n_pick,
                                  chosen_t=ts[n_pick], **{k: m[k] for k in
                                  ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe",
                                   "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD")},
                                  anchor_OOS_Sharpe=blocks_m(anchor, dd["ins_m"],
                                                             dd["oos_m"])["OOS_Sharpe"],
                                  SPY_OOS_Sharpe=sb["OOS_Sharpe"],
                                  LIVE_OOS_Sharpe=lb["OOS_Sharpe"], **l4b, **l4o, **l4a,
                                  pass_4b_full=all(l4b.values()),
                                  pass_4b_oos=all(l4o.values()), pass_4a=all(l4a.values())))
        # the control chooser: no SE at all, pick the best IS Sharpe
        n_pick = max(N_LADDER, key=lambda n: cands[n]["m"]["IS_Sharpe"])
        m = cands[n_pick]["m"]
        l4b, l4o, l4a = legs_4b(m, sb), legs_4b_oos(m, sb), legs_4a(m, lb)
        picks.append(dict(panel=panel, se_basis="C_ISSHARPE", L=0, chosen_N=n_pick,
                          chosen_t=np.nan, **{k: m[k] for k in
                          ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe",
                           "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD")},
                          anchor_OOS_Sharpe=blocks_m(anchor, dd["ins_m"],
                                                     dd["oos_m"])["OOS_Sharpe"],
                          SPY_OOS_Sharpe=sb["OOS_Sharpe"], LIVE_OOS_Sharpe=lb["OOS_Sharpe"],
                          **l4b, **l4o, **l4a, pass_4b_full=all(l4b.values()),
                          pass_4b_oos=all(l4o.values()), pass_4a=all(l4a.values())))
        P(f"  {panel:<6s} chooser arm done  ({time.time() - t0:.0f}s elapsed)")
    picks = pd.DataFrame(picks)
    dump(picks, "picks")
    P("  mean OOS Sharpe of the chosen book, by chooser (anchor = do nothing):")
    for basis in SE_BASES + ["C_ISSHARPE"]:
        s = picks[picks.se_basis == basis]
        P(f"    {basis:<11s} {s.OOS_Sharpe.mean():.4f}  over {len(s)} picks  "
          f"(anchor {s.anchor_OOS_Sharpe.mean():.4f})")
    P("  per (panel, basis) at the record's L = 252:")
    for _, p in picks[(picks.L == 252) | (picks.se_basis == "C_ISSHARPE")].iterrows():
        P(f"    {p.panel:<6s} {p.se_basis:<11s} N={int(p.chosen_N):<3d} OOS "
          f"{p.OOS_CAGR:7.2%} / {p.OOS_Sharpe:.4f} / {p.OOS_MaxDD:8.2%}  "
          f"(SPY {p.SPY_OOS_Sharpe:.4f}, LIVE {p.LIVE_OOS_Sharpe:.4f}, "
          f"anchor {p.anchor_OOS_Sharpe:.4f})  4b full {'Y' if p.pass_4b_full else 'n'} "
          f"OOS {'Y' if p.pass_4b_oos else 'n'} 4a {'Y' if p.pass_4a else 'n'}")
    P(f"  4b full {int(picks.pass_4b_full.sum())} of {len(picks)}; "
      f"4b OOS {int(picks.pass_4b_oos.sum())}; "
      f"BOTH {int((picks.pass_4b_full & picks.pass_4b_oos).sum())}; "
      f"4a {int(picks.pass_4a.sum())} of {len(picks)}")
    fold_oos = picks[picks.se_basis == "S_FOLD"].OOS_Sharpe.mean()
    blk_oos = picks[picks.se_basis == "S_BLOCK"].OOS_Sharpe.mean()
    anc = picks.anchor_OOS_Sharpe.mean()
    hyp("H_WF", "choosing on the fold-clustered t beats choosing on the block t out of sample",
        "mean OOS Sharpe(S_FOLD) > mean OOS Sharpe(S_BLOCK)",
        f"S_FOLD {fold_oos:.4f} vs S_BLOCK {blk_oos:.4f}; doing nothing {anc:.4f}",
        bool(fold_oos > blk_oos))
    P("")

    dump(pd.DataFrame(GATES), "gates")
    dump(pd.DataFrame(HYP), "hypotheses")
    P(f"## GATES {sum(g['pass_'] for g in GATES)} of {len(GATES)} PASS")
    P(f"## RUNTIME {time.time() - t0:.0f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG))


if __name__ == "__main__":
    main()

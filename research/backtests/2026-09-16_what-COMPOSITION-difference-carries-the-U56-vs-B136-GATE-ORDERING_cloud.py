#!/usr/bin/env python3
"""Idea 1112 (cloud lane, 2026-09-16) — what COMPOSITION difference carries the U56-vs-B136
GATE ORDERING?

QUESTION (QUEUE idea 1112, verbatim)
    idea 1106 killed turnover as the explanation for the H=21 sign flip and found instead that
    B136's nulls re-draw MORE than U56's at all 5 min-hold rungs while B136's mean GATE is MORE
    NEGATIVE at all 5, i.e. the panels order by composition.  Cross the two panels' overlap, cap
    mix and gate-pass rate against GATE at matched (N, H) and report which one carries the
    ordering.  Max 2 params (matching variable, panel pair).

WHAT GATE IS (1085/1097's alphabet, unchanged)
    OPEN  null: random ranks, elig = ALL PRICED.  The convention every committed EDGE figure in
          the record was measured under.
    ELIG  null: random ranks, elig = the BOOK'S OWN gate (px > 200d MA AND 20d ann vol < 0.60).
    EDGE_x = 100 * (book CAGR - median over seeds of null-x CAGR), the null DD-matched to the
          book by the REBUILT gross rescaler (1085's convention).
    GATE = EDGE_OPEN - EDGE_ELIG.  GATE < 0 <=> the gated null is the HARDER comparand.
          1106's D1: mean GATE is more negative on B136 than on U56 at all five H rungs.

THE TWO TUNED DIALS (PROTOCOL rule 4, no more than two)
    1. MATCH — the matching variable that defines each 56-name panel family drawn out of B136:
         NONE      B136 itself (nothing matched)
         SIZE      SPY + 55 uniformly random of the other 135 (matches POOL SIZE K only)
         ETFSHARE  the 36 ETFs + 20 random of the 80 single stocks B136 adds to U56
                   (matches POOL SIZE and ETF SHARE; swaps only megacap IDENTITY)
         GATEPASS  SPY + 55 of the other 135 drawn to match U56's pool-mean gate-pass rate
                   (matches POOL SIZE and GATE-PASS RATE)
       Six independent draws per random family, every draw published.
    2. PANEL PAIR — the contrast the gap is read across:
         COMMITTED  (U56@A, B136@B), exactly the pair 1106 reports the ordering for
         VINTAGE    (U56@A, U56@B), the SAME 56 tickers off the two price files the record's
                    two panels actually load from.  This arm is not decoration: see below.

    N and H ARE NOT DIALS.  N in {5, 10, 20, 40} and H in {5, 21, 126} are 1082/1086/1097/1106's
    committed coordinates, taken as given; every one of the 12 (N, H) coords is published for
    every panel instance.  Everything else is frozen at 1085/1097/1106's construction: cap INF,
    REBUILT DD-match, 40 seeds, 34 bisection steps, max_vol 0.60, gross 0.75, W cadence, 10 bps,
    LAG 1, CAND20 legs [(21,252),(0,126),(0,63)], warm-up 260 rows.

THE VINTAGE ARM, AND WHY IT IS HERE (found while checking the tapes, before any GATE was run)
    `load_universe()` serves U56 out of data/prices.csv.  `load_universe(broad=True)` cannot:
    80 of the 136 broad tickers are absent from prices.csv, so `load_prices` raises and
    `load_universe` falls back to the separate weekly cache data/prices_broad.csv.  The two
    files DISAGREE on the 56 tickers they share: 51 of 56 columns differ, max relative price
    difference 3.63% (NVDA), max single-day return difference 723 bps, mean |return difference|
    1.94 bps/day, and the files end on different days (2026-09-15 vs 2026-09-11).
    So the record's "U56 vs B136" is a comparison across TWO PRICE VINTAGES as well as two
    compositions, and VINTAGE has to be priced before any composition claim is identified.
    It is measured here as its own step and is reported whatever it comes to.

THE COMMON TAPE (declared before any number)
    Every panel instance below is evaluated on the INTERSECTION of the two files' indexes
    (2008-01-02 .. 2026-09-11), so K and T are identical across the vintage pair and the null
    seed recipe draws the SAME 40 random orderings for U56@A and U56@B.  The vintage step is
    therefore the prices moving and nothing else.
    `U56@A_NATIVE` (U56 on prices.csv's own 4,705-row index, exactly as 1106 ran it) is carried
    ONLY as a cross-run reproduction gate and is excluded from every analysis row.

THE DECOMPOSITION (fixed before any number).  U56@A -> B136@B in four additive steps:
    VINTAGE   GATE(U56@A)      - GATE(U56@B)       same tickers, different price file
    IDENTITY  GATE(U56@B)      - GATE(B56ETF@B)    matched K and ETF share; megacaps swapped
                                                   for 20 other large caps
    ETFSHARE  GATE(B56ETF@B)   - GATE(B56SZ@B)     matched K; ETF share 0.643 -> B136's 0.265
    POOLSIZE  GATE(B56SZ@B)    - GATE(B136@B)      matched composition; K 56 -> 136
    The four sum to the committed gap by construction, so the shares are a partition and not a
    regression.  GATEPASS is NOT in the chain (it is not nested in it); it is read as its own
    matched family and as a rank correlation across all 21 instances.

DECLARED BEFORE ANY NUMBER — what each candidate carrier needs
    H_ORDER    the premise, re-measured: GATE(U56@A) > GATE(B136@B) at every (N, H) coord.
               REFUTED by any coord that inverts.
    H_OVERLAP  overlap carries the ordering.  Pre-registered as REFUTED BY CONSTRUCTION if
               U56 is a subset of B136 (overlap share 1.000 has no variation to carry an
               ordering); the subset test is run and printed either way.
    H_POOLSIZE the POOLSIZE step carries >= 50% of |committed gap| at a majority of coords.
    H_ETFSHARE the ETFSHARE step does (this is the queue's "cap mix" read as the ETF-vs-single
               -name mix, the only cap-like axis these two committed panels differ on).
    H_IDENT    the IDENTITY step does.
    H_GATEPASS Spearman(GATE, pool-mean gate-pass rate) across the 21 instances is the same sign
               at every coord AND |rho| >= 0.5 AND larger in absolute value than rho against K
               and against ETF share.
    H_VINTAGE  the vintage step is negligible: |VINTAGE| < 10% of |committed gap| at a majority
               of coords.  REFUTED means the committed ordering is not identified as composition.
    H_RESOLVED the largest step exceeds 2x its own seed SE at a majority of coords (paired over
               the 40 shared seeds where the two arms share a seed recipe, independent hypot
               otherwise).

    GATE IS A STATEMENT ABOUT THE COMPARAND, NOT THE BOOK, so neither KEEP path can be moved by
    changing the null.  What this run DOES move is the PANEL, which is a real dial a book would
    have to choose, so 4a and 4b are scored at all 252 analysis cells and rule 8 is walked over
    (panel instance, N, H) with the panel chosen on 2009-2016 only.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists and so is every
    subset drawn from them.  Every level here is optimistic and every 4a/4b count is an UPPER
    bound.  GATE and the four steps are within-pool contrasts over one tape and the bias very
    largely cancels out of them; it does NOT cancel out of the 4b legs, which are measured
    against SPY, a real index.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-16"
SLUG = "what-COMPOSITION-difference-carries-the-U56-vs-B136-GATE-ORDERING"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

LAG = 1
WARMUP = 260
MAXVOL = 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST = 10.0
GROSS0 = 0.75
FREQ = "W"
LEGS = [(21, 252), (0, 126), (0, 63)]
CAPNAME = "INF"
SEEDS = 40
BISECT = 34
DECISIVE_K = 2.0
NDRAW = 6                                  # draws per random panel family
GP_TRIES = 20000                           # candidate draws per GATEPASS instance

NS = [5, 10, 20, 40]                       # committed coordinate set, NOT a dial
HS = [5, 21, 126]                          # committed coordinate set, NOT a dial
GATESET = ["OPEN", "ELIG"]
EXCLUDE = {"BTC-USD", "ETH-USD"}

A936_WH126 = (0.155787, 1.139701, -0.191276)
SRC_1106 = (ROOT / "research" / "backtests"
            / "2026-09-16_is-the-U56-H21-SIGN-FLIP-a-TURNOVER-fact_B.grid.csv")

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


# ---------------------------------------------------------------- kernels (1097/1106 verbatim)
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


def gross_rescaler(rets, wt, mk):
    T, N = rets.shape
    mk = mk.copy()
    mk[0] = True
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
    reb = np.flatnonzero(mk)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    A = wt[s0] * (Cp / Cp[s0])
    AR = (A * rets).sum(axis=1)
    S = A.sum(axis=1)
    Wsum = wt[s0].sum(axis=1)
    s0p = reb[np.maximum(seg - 1, 0)]
    Ap = (wt[s0p] * (Cp / Cp[s0p]))[reb]
    Sp = Ap.sum(axis=1)
    Wsp = wt[s0p].sum(axis=1)[reb]
    Ap[0] = 0.0
    Sp[0] = 0.0
    Wsp[0] = 0.0
    Wr = wt[reb]
    c = COST / 1e4

    def f(lam, want_turn=False):
        V = 1.0 + lam * (S - Wsum)
        g = lam * AR / V
        Vp_ = 1.0 + lam * (Sp - Wsp)
        tr = lam * np.abs(Wr - Ap / Vp_[:, None]).sum(axis=1)
        out = g.copy()
        out[reb] -= tr * c
        if want_turn:
            tpath = np.zeros(T)
            tpath[reb] = tr
            return out, tpath
        return out

    return f


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


def maxdd(r):
    eq = np.cumprod(1.0 + np.asarray(r, float))
    return float((eq / np.maximum.accumulate(eq) - 1.0).min())


def lagmat(a):
    out = np.zeros_like(a)
    out[LAG:] = a[:-LAG]
    return out


def legs_composite(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return sum(parts) / len(parts)


def mech(px):
    """Composite score and the book's own eligibility gate, computed WITHIN the given pool
    (the composite is a cross-sectional rank, so it is pool-dependent by construction; the
    200d/vol gate is per-name and is not)."""
    comp = legs_composite(px)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    return sc.values, (above & (vol20 < MAXVOL)).values


def build(rank_key, elig, priced, reb, N, cap, H, T, K, gross):
    """1097/1106's build() verbatim."""
    W = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
    nsel_by_reb, gross_by_reb, new_by_reb = [], [], []
    per_cap = cap * gross / N if np.isfinite(cap) else np.inf
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
        nsel_by_reb.append(len(sel))
        new_by_reb.append(len(take))
        stop = reb[i + 1] if i + 1 < len(reb) else T
        if len(sel):
            w = min(gross / len(sel), per_cap)
            W[t:stop, sel] = w
            gross_by_reb.append(w * len(sel))
        else:
            gross_by_reb.append(0.0)
    return W, np.array(nsel_by_reb), np.array(gross_by_reb), np.array(new_by_reb)


def windows(idx):
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    ins = warm & ~oos
    return warm, ins, oos


def blocks(r, warm, ins, oos):
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


def lam_rebuilt(f, sl, target_dd, it):
    if abs(maxdd(f(1.0)[sl])) <= abs(target_dd):
        return None
    a, b = 1e-4, 1.0
    for _ in range(it):
        m = 0.5 * (a + b)
        if abs(maxdd(f(m)[sl])) > abs(target_dd):
            b = m
        else:
            a = m
    return 0.5 * (a + b)


def se_median(x):
    x = np.asarray(x, float)
    return 100.0 * 1.2533 * x.std(ddof=1) / np.sqrt(len(x))


def spear(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 3:
        return np.nan
    return float(pd.Series(x[ok]).rank().corr(pd.Series(y[ok]).rank()))


def ann_turn(tpath, mask):
    return float(tpath[mask].sum() / (mask.sum() / 252.0))


# ---------------------------------------------------------------- panel construction ---------
def panel_family():
    """Build every panel instance.  Returns (instances, meta) where each instance carries its
    own price frame slice, its TICKER-SET KEY (the null seed recipe's panel field) and its
    composition statistics.  The seed key is the TICKER SET, not the vintage, so the vintage
    pair replays identical orderings."""
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    ETFS = set(U["broad"]) | set(U["sectors"]) | set(U["bonds_fx_commod"])
    u_t = sorted({t for g in U.values() for t in g} - EXCLUDE)
    b_t = sorted(json.loads((ROOT / "research" / "universe_broad.json").read_text()))

    A = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)
    B = pd.read_csv(ROOT / "data" / "prices_broad.csv", index_col=0, parse_dates=True)
    A = A.loc["2008-01-01":]
    B = B.loc["2008-01-01":]
    common = A.index.intersection(B.index)

    fa = A[u_t].loc[common].dropna(how="all").ffill()
    fb = B[b_t].loc[common].dropna(how="all").ffill()
    assert fa.index.equals(fb.index), "common tape mismatch"
    nat = A[u_t].dropna(how="all").ffill()                 # U56 on its NATIVE 4,705-row index

    P(f"## TAPES.  prices.csv {A.shape[0]} rows to {A.index[-1].date()}; "
      f"prices_broad.csv {B.shape[0]} rows to {B.index[-1].date()}; "
      f"COMMON TAPE {len(fa)} rows {fa.index[0].date()}..{fa.index[-1].date()}")
    sh = [t for t in u_t if t in b_t]
    reldiff = ((A.loc[common, sh] - B.loc[common, sh]).abs() / A.loc[common, sh].abs()).max()
    ra = A.loc[common, sh].pct_change()
    rb = B.loc[common, sh].pct_change()
    P(f"## PRICE VINTAGE.  U56 is a SUBSET of B136: {len(sh)} of {len(u_t)} shared "
      f"(subset = {set(u_t) <= set(b_t)}).  Of those, "
      f"{int((reldiff > 1e-6).sum())} columns DISAGREE between the two files; "
      f"max relative price diff {reldiff.max():.4%} ({reldiff.idxmax()}), "
      f"max |return diff| {float((ra - rb).abs().max().max()):.4f}, "
      f"mean |return diff| {float((ra - rb).abs().mean().mean()) * 1e4:.3f} bps/day")

    # per-name gate-pass rate on the B vintage (the vintage every drawn family lives on)
    gp_b = ((fb > fb.rolling(200).mean())
            & (fb.pct_change().rolling(20).std() * np.sqrt(252) < MAXVOL))
    gp_b = gp_b.where(fb.notna())
    gp_name = gp_b.iloc[WARMUP:].mean(axis=0)              # per-name pass rate, warm days only
    target_gp = float(gp_name[u_t].mean())
    others = [t for t in b_t if t != "SPY"]
    addstk = [t for t in b_t if t not in u_t]               # the 80 single stocks B136 adds
    u_etfs = [t for t in u_t if t in ETFS]

    inst = []

    def add(label, frame, tickers, key, family, draw, vintage):
        inst.append(dict(label=label, frame=frame[list(tickers)], key=key, family=family,
                         draw=draw, vintage=vintage, tickers=list(tickers)))

    add("U56@A", fa, u_t, "U56", "REF_U56", -1, "A")
    add("U56@B", fb, u_t, "U56", "VINTAGE", -1, "B")
    add("B136@B", fb, b_t, "B136", "NONE", -1, "B")
    for r in range(NDRAW):
        rng = np.random.default_rng(mdseed("SIZE", r))
        pick = ["SPY"] + sorted(rng.choice(others, 55, replace=False).tolist())
        add(f"B56SZ{r}@B", fb, sorted(pick), f"B56SZ{r}", "SIZE", r, "B")
    for r in range(NDRAW):
        rng = np.random.default_rng(mdseed("ETFSHARE", r))
        pick = u_etfs + sorted(rng.choice(addstk, 20, replace=False).tolist())
        add(f"B56ETF{r}@B", fb, sorted(pick), f"B56ETF{r}", "ETFSHARE", r, "B")
    for r in range(NDRAW):
        rng = np.random.default_rng(mdseed("GATEPASS", r))
        best, bestd = None, np.inf
        pool = np.array(others)
        gpv = gp_name[others].values
        for _ in range(GP_TRIES):
            ix = rng.choice(len(pool), 55, replace=False)
            m = (gpv[ix].sum() + gp_name["SPY"]) / 56.0
            d = abs(m - target_gp)
            if d < bestd:
                best, bestd = ix, d
        pick = ["SPY"] + sorted(pool[best].tolist())
        add(f"B56GP{r}@B", fb, sorted(pick), f"B56GP{r}", "GATEPASS", r, "B")
    # Seed key "U56", NOT a separate one: 1106 drew its U56 orderings from md5("U56", N, "INF", s)
    # on this very 4,705-row tape, so keying the native twin the same way is what makes G3 a
    # REPRODUCTION of 1106's EDGE figures rather than a fresh draw.  (This run's first pass
    # keyed it "U56NAT" and G3 failed at 1.03 pp for exactly that reason; the failure was a gate
    # specification error, not a discrepancy, and is recorded here rather than quietly removed.)
    add("U56@A_NATIVE", nat, u_t, "U56", "GATE_ONLY", -1, "A")

    meta = []
    for d in inst:
        tk = d["tickers"]
        f = d["frame"]
        rr = f.pct_change().iloc[WARMUP:]
        C = rr.corr().values
        iu = np.triu_indices(len(tk), 1)
        gpn = ((f > f.rolling(200).mean())
               & (f.pct_change().rolling(20).std() * np.sqrt(252) < MAXVOL))
        gpn = gpn.where(f.notna()).iloc[WARMUP:]
        meta.append(dict(label=d["label"], family=d["family"], draw=d["draw"],
                         vintage=d["vintage"], seed_key=d["key"], K=len(tk),
                         etf_share=len([t for t in tk if t in ETFS]) / len(tk),
                         ovl_in_U56=len([t for t in tk if t in u_t]) / len(tk),
                         ovl_of_U56=len([t for t in tk if t in u_t]) / len(u_t),
                         gate_pass=float(np.nanmean(gpn.values)),
                         rbar=float(np.nanmean(C[iu]))))
    return inst, pd.DataFrame(meta), target_gp, set(u_t) <= set(b_t)


def main():
    t0 = time.time()
    P(f"# Idea 1112 (cloud lane, {DATE}) — what COMPOSITION difference carries the U56-vs-B136")
    P("#   GATE ORDERING?")
    P("# 2 tuned dials: MATCH {NONE, SIZE, ETFSHARE, GATEPASS} x PANEL PAIR {COMMITTED, VINTAGE}.")
    P(f"#   {NDRAW} independent draws per random family, every draw published.")
    P(f"# NOT dials: N {NS} and H {HS} are 1082/1086/1097/1106's committed coordinates; all")
    P(f"#   {len(NS)*len(HS)} coords published for every panel instance.")
    P(f"# FROZEN: CAND20 legs {LEGS}, cap INF, REBUILT DD-match, {SEEDS} seeds, {BISECT} bisection")
    P(f"#   steps, max_vol {MAXVOL}, gross {GROSS0}, cost {COST:.0f} bps, LAG {LAG}, cadence {FREQ}.")
    P("# The null SEED RECIPE keys on the TICKER SET, not the vintage, so U56@A and U56@B replay")
    P("#   the SAME 40 orderings and the VINTAGE step is the prices moving and nothing else.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   H_ORDER     GATE(U56@A) > GATE(B136@B) at every (N, H) coord.")
    P("#   H_OVERLAP   pre-registered REFUTED BY CONSTRUCTION if U56 is a subset of B136.")
    P("#   H_POOLSIZE  the POOLSIZE step carries >=50% of |committed gap| at a majority of coords.")
    P("#   H_ETFSHARE  the ETFSHARE step does (the queue's 'cap mix').")
    P("#   H_IDENT     the IDENTITY step does.")
    P("#   H_GATEPASS  rho(GATE, gate-pass) same sign at every coord, |rho| >= 0.5, and larger")
    P("#               than |rho| against K and against ETF share.")
    P("#   H_VINTAGE   |VINTAGE step| < 10% of |committed gap| at a majority of coords.")
    P("#   H_RESOLVED  the largest step > 2x its own seed SE at a majority of coords.")
    P("# GATE is a statement about the COMPARAND; the PANEL is a real dial, so 4a/4b are scored")
    P("#   at every analysis cell and rule 8 is walked over (panel instance, N, H).")
    P("")

    inst, M, target_gp, is_subset = panel_family()
    P(f"\n## {len(inst)} PANEL INSTANCES (the last is a reproduction gate only). "
      f"GATEPASS target = U56's pool-mean gate-pass rate {target_gp:.4f}")
    P("   label          family    K   etf_share  ovl_in_U56  gate_pass   rbar   vintage")
    for _, r in M.iterrows():
        P(f"   {r['label']:<14s} {r['family']:<9s} {r['K']:<3d} {r['etf_share']:9.4f}  "
          f"{r['ovl_in_U56']:10.4f}  {r['gate_pass']:9.4f}  {r['rbar']:6.4f}   {r['vintage']}")

    gates = {}
    gates["G0 U56 is a SUBSET of B136 (so overlap has no variation to carry an ordering)"] = (
        0.0 if is_subset else 1.0, bool(is_subset))

    rows, benchrows, seedrows = [], [], []
    for d in inst:
        label, px, key = d["label"], d["frame"], d["key"]
        idx = px.index
        K = len(px.columns)
        T = len(idx)
        rets = px.pct_change().fillna(0.0).values
        priced = px.notna().values
        mk = rebalance_mask(idx, FREQ).values
        mkl = np.roll(mk, LAG)
        warm, ins, oos = windows(idx)
        sc, elig_real = mech(px)
        rank_key = -np.nan_to_num(sc, nan=-np.inf)
        rank_key[np.isnan(sc)] = np.inf
        reb = np.flatnonzero(mk)
        rebw = reb[reb >= WARMUP]
        keep_mask = np.isin(reb, rebw)
        ALLP = np.ones((T, K), dtype=bool)

        spy = px["SPY"].pct_change().fillna(0.0).values
        sb = blocks(spy, warm, ins, oos)
        live = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"].values
        lb = blocks(live, warm, ins, oos)
        benchrows += [dict(label=label, series="SPY", **sb),
                      dict(label=label, series="RULESv2_on_panel", **lb)]
        P(f"\n## {label}: K={K}, T={T} {idx[0].date()}..{idx[-1].date()}, "
          f"{len(rebw)} rebalance dates after warm-up")
        P(f"   SPY      full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%}  "
          f"OOS {sb['OOS_CAGR']:.2%} / {sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"   RULESv2  full {lb['CAGR']:.2%} / {lb['Sharpe']:.4f} / {lb['MaxDD']:.2%}  "
          f"OOS {lb['OOS_CAGR']:.2%} / {lb['OOS_Sharpe']:.4f} / {lb['OOS_MaxDD']:.2%}")

        if label == "U56@A_NATIVE":
            Wg, _, _, _ = build(rank_key, elig_real, priced, reb, 20, np.inf, 126, T, K, GROSS0)
            wdf = pd.DataFrame(Wg, index=idx, columns=px.columns)
            eng = backtest(px, wdf, cost_bps=COST, freq=FREQ)["returns"].values
            gg, tn = nrun(rets, lagmat(Wg), mkl)
            fast = gg - tn * COST / 1e4
            dv = float(np.abs(fast[WARMUP:] - eng[WARMUP:]).max())
            gates["G1 fast runner == engine.backtest (U56@A_NATIVE, N=20, H=126)"] = (dv, dv < 1e-12)
            f20 = gross_rescaler(rets, lagmat(Wg), mkl)
            dv = float(np.abs(f20(1.0) - fast).max())
            gates["G1b gross_rescaler(1.0) == nrun (the bisection kernel is the same book)"] = (
                dv, dv < 1e-14)
            m = fmet(fast[warm])
            dv = max(abs(m[i] - A936_WH126[i]) for i in range(3))
            gates["G2 CROSS-RUN 936/1071/1082 committed W/H126 N=20 triple"] = (dv, dv < 5e-3)

        for Hh in HS:
            for N in NS:
                Wb, nsel, grs, nnew = build(rank_key, elig_real, priced, reb, N, np.inf, Hh,
                                            T, K, GROSS0)
                gb, tb = nrun(rets, lagmat(Wb), mkl)
                rb = gb - tb * COST / 1e4
                b = blocks(rb, warm, ins, oos)
                l4b, l4a, l4bo = legs_4b(b, sb), legs_4a(b, lb), legs_4b_oos(b, sb)
                out = dict(label=label, family=d["family"], draw=d["draw"], vintage=d["vintage"],
                           seed_key=key, K=K, H=Hh, N=N,
                           mean_nsel=float(nsel[keep_mask].mean()),
                           mean_gross=float(grs[keep_mask].mean()),
                           zero_share=float((nsel[keep_mask] == 0).mean()),
                           gross_when_held=float(grs[keep_mask][nsel[keep_mask] > 0].mean()),
                           book_new_per_reb=float(nnew[keep_mask].mean()),
                           turnover=ann_turn(tb, warm), **b, **l4b, **l4a, **l4bo,
                           pass4b=all(l4b.values()), pass4a=all(l4a.values()),
                           pass4b_oos=all(l4bo.values()))
                out["pass4b_full_and_oos"] = out["pass4b"] and out["pass4b_oos"]
                for gate in GATESET:
                    cs, isv, oosv, nt, lams, drier = [], [], [], [], [], 0
                    for s in range(SEEDS):
                        sd = (mdseed(key, N, CAPNAME, s) if gate == "OPEN"
                              else mdseed(key, N, CAPNAME, "ELIG", s))
                        rk = np.random.default_rng(sd).random((T, K))
                        eg = elig_real if gate == "ELIG" else ALLP
                        Wn, _, _, _ = build(rk, eg, priced, reb, N, np.inf, Hh, T, K, GROSS0)
                        fn = gross_rescaler(rets, lagmat(Wn), mkl)
                        lam = lam_rebuilt(fn, warm, b["MaxDD"], BISECT)
                        if lam is None:
                            drier += 1
                            lam = 1.0
                        rr, tp = fn(lam, want_turn=True)
                        _, tp1 = fn(1.0, want_turn=True)
                        cs.append(fmet(rr[warm])[0])
                        isv.append(fmet(rr[ins])[0])
                        oosv.append(fmet(rr[oos])[0])
                        nt.append(ann_turn(tp1, warm))
                        lams.append(lam)
                    cs, isv, oosv = np.array(cs), np.array(isv), np.array(oosv)
                    for s in range(SEEDS):
                        seedrows.append(dict(label=label, H=Hh, N=N, gate=gate, seed=s,
                                             null_CAGR=float(cs[s]), null_IS_CAGR=float(isv[s]),
                                             null_OOS_CAGR=float(oosv[s])))
                    out[f"EDGE_{gate}_pp"] = 100.0 * (b["CAGR"] - float(np.median(cs)))
                    out[f"EDGE_IS_{gate}_pp"] = 100.0 * (b["IS_CAGR"] - float(np.median(isv)))
                    out[f"EDGE_OOS_{gate}_pp"] = 100.0 * (b["OOS_CAGR"] - float(np.median(oosv)))
                    out[f"EDGE_se_{gate}_pp"] = se_median(cs)
                    out[f"null_med_{gate}"] = float(np.median(cs))
                    out[f"NTURN_raw_{gate}"] = float(np.median(nt))
                    out[f"lam_med_{gate}"] = float(np.median(lams))
                    out[f"drier_{gate}"] = drier
                out["GATE_pp"] = out["EDGE_OPEN_pp"] - out["EDGE_ELIG_pp"]
                out["GATE_IS_pp"] = out["EDGE_IS_OPEN_pp"] - out["EDGE_IS_ELIG_pp"]
                out["GATE_OOS_pp"] = out["EDGE_OOS_OPEN_pp"] - out["EDGE_OOS_ELIG_pp"]
                out["GATE_se_pp"] = float(np.hypot(out["EDGE_se_OPEN_pp"], out["EDGE_se_ELIG_pp"]))
                out["GATE_decisive"] = bool(abs(out["GATE_pp"]) > DECISIVE_K * out["GATE_se_pp"])
                rows.append(out)
                P(f"   {label:<14s} H={Hh:<3d} N={N:<2d} OPEN {out['EDGE_OPEN_pp']:+7.3f} "
                  f"ELIG {out['EDGE_ELIG_pp']:+7.3f} GATE {out['GATE_pp']:+7.3f} "
                  f"(+-{DECISIVE_K*out['GATE_se_pp']:.3f})  CAGR {b['CAGR']:6.2%} "
                  f"MaxDD {b['MaxDD']:7.2%}  t={time.time()-t0:5.0f}s")

    G = pd.DataFrame(rows)
    SD = pd.DataFrame(seedrows)
    AN = G[G.label != "U56@A_NATIVE"].copy()          # analysis rows
    NAT = G[G.label == "U56@A_NATIVE"].copy()

    # ---- cross-run reproduction gates ---------------------------------------------------
    c06 = pd.read_csv(SRC_1106, dtype=str, keep_default_na=False)   # idea 1105's read fix
    for c in ["H", "N"]:
        c06[c] = c06[c].astype(int)
    for c in ["EDGE_OPEN_pp", "EDGE_ELIG_pp", "GATE_pp", "CAGR", "MaxDD", "turnover"]:
        c06[c] = c06[c].astype(float)
    cu = c06[c06.panel == "U56"][["N", "H", "EDGE_OPEN_pp", "EDGE_ELIG_pp", "GATE_pp",
                                  "CAGR", "MaxDD", "turnover"]]
    m = NAT.merge(cu, on=["N", "H"], suffixes=("", "_06"))
    dv = max(float((m.EDGE_OPEN_pp - m.EDGE_OPEN_pp_06).abs().max()),
             float((m.EDGE_ELIG_pp - m.EDGE_ELIG_pp_06).abs().max()))
    gates[f"G3 CROSS-RUN reproduce 1106's {len(m)} U56 EDGE_OPEN/ELIG figures (native tape)"] = (
        dv, dv < 1e-9)
    dv = max(float((m.CAGR - m.CAGR_06).abs().max()), float((m.MaxDD - m.MaxDD_06).abs().max()),
             float((m.turnover - m.turnover_06).abs().max()))
    gates[f"G4 CROSS-RUN reproduce 1106's {len(m)} U56 book CAGR/MaxDD/turnover triples"] = (
        dv, dv < 1e-9)
    cb = c06[c06.panel == "B136"][["N", "H", "EDGE_OPEN_pp", "EDGE_ELIG_pp", "GATE_pp",
                                   "CAGR", "MaxDD", "turnover"]]
    mb = AN[AN.label == "B136@B"].merge(cb, on=["N", "H"], suffixes=("", "_06"))
    dv = max(float((mb.EDGE_OPEN_pp - mb.EDGE_OPEN_pp_06).abs().max()),
             float((mb.EDGE_ELIG_pp - mb.EDGE_ELIG_pp_06).abs().max()))
    gates[f"G5 CROSS-RUN reproduce 1106's {len(mb)} B136 EDGE figures (its tape IS the common one)"] = (
        dv, dv < 1e-9)
    dv = float(AN.gross_when_held.sub(GROSS0).abs().max())
    gates[f"G6 every book sits at gross {GROSS0} on every date it holds anything "
          f"(cap INF, no de-grossing)"] = (dv, dv < 1e-12)
    P(f"   [MEASURED, not pass/fail] a 56-name subpanel CAN go fully to cash where B136 cannot: "
      f"the share of post-warm-up rebalance dates with ZERO eligible names runs "
      f"{AN.zero_share.min():.4%} to {AN.zero_share.max():.4%} across the {len(AN)} analysis "
      f"cells (max on {AN.loc[AN.zero_share.idxmax(), 'label']}), against "
      f"{float(AN[AN.label == 'B136@B'].zero_share.max()):.4%} on B136.  This run's first pass "
      f"gated on MEAN gross being exactly {GROSS0} and FAILED at 5.69e-03 for exactly this "
      f"reason: the gate, not the book, was wrong, and the corrected gate below tests gross on "
      f"the dates the book is invested.")
    ua, ub = AN[AN.label == "U56@A"], AN[AN.label == "U56@B"]
    dv = float(abs(ua.K.iloc[0] - ub.K.iloc[0]))
    gates["G7 the VINTAGE pair shares K and the tape, so it replays identical null orderings"] = (
        dv, dv == 0.0 and len(ua) == len(ub))
    dv = float(AN.groupby("label").size().std())
    gates[f"G8 every analysis instance carries all {len(NS)*len(HS)} coords"] = (dv, dv == 0.0)

    P("\n## GATES")
    gaterows = []
    for k, (v, ok) in gates.items():
        P(f"   [{'PASS' if ok else 'FAIL'}] {k}: {v:.2e}")
        gaterows.append(dict(gate=k, value=v, passed=ok))
    P(f"   {sum(1 for _, o in gates.values() if o)} of {len(gates)} PASS")

    # ---------------------------------------------------------------- H_ORDER -------------
    P("\n## H_ORDER — re-measure 1106's D1 ordering at every committed coord")
    P("   coord      GATE(U56@A)  GATE(B136@B)   gap   ordered?")
    ordr = []
    for Hh in HS:
        for N in NS:
            a = float(ua[(ua.H == Hh) & (ua.N == N)].GATE_pp.iloc[0])
            bb = float(AN[(AN.label == "B136@B") & (AN.H == Hh) & (AN.N == N)].GATE_pp.iloc[0])
            ordr.append(dict(H=Hh, N=N, gate_U56A=a, gate_B136=bb, gap=a - bb, ordered=a > bb))
            P(f"   H={Hh:<3d} N={N:<2d}  {a:+10.3f}   {bb:+10.3f}  {a-bb:+8.3f}   "
              f"{'yes' if a > bb else 'NO'}")
    OR = pd.DataFrame(ordr)
    H_ORDER = bool(OR.ordered.all())
    P(f"   ordered at {int(OR.ordered.sum())} of {len(OR)} coords; mean gap {OR.gap.mean():+.3f} pp")
    P(f"   H_ORDER -> {'SUPPORTED' if H_ORDER else 'REFUTED'}")

    # ---------------------------------------------------------------- decomposition -------
    P("\n## THE FOUR-STEP DECOMPOSITION of the committed gap (family means over the 6 draws)")
    P("   Each step is a difference of GATE between two panels differing in ONE axis; the four")
    P("   sum to the committed gap by construction.")

    def fam_gate(fam, Hh, N, col="GATE_pp"):
        s = AN[(AN.family == fam) & (AN.H == Hh) & (AN.N == N)]
        return float(s[col].mean()), float(s[col].std(ddof=1)) if len(s) > 1 else np.nan, len(s)

    def seed_arr(label, Hh, N, gate):
        s = SD[(SD.label == label) & (SD.H == Hh) & (SD.N == N) & (SD.gate == gate)]
        return s.sort_values("seed").null_CAGR.values

    dec = []
    for Hh in HS:
        for N in NS:
            gA = float(ua[(ua.H == Hh) & (ua.N == N)].GATE_pp.iloc[0])
            gB = float(ub[(ub.H == Hh) & (ub.N == N)].GATE_pp.iloc[0])
            gE, sE, nE = fam_gate("ETFSHARE", Hh, N)
            gS, sS, nS = fam_gate("SIZE", Hh, N)
            gG, sG, nG = fam_gate("GATEPASS", Hh, N)
            g136 = float(AN[(AN.label == "B136@B") & (AN.H == Hh) & (AN.N == N)].GATE_pp.iloc[0])
            steps = dict(VINTAGE=gA - gB, IDENTITY=gB - gE, ETFSHARE=gE - gS, POOLSIZE=gS - g136)
            gap = gA - g136
            # paired SE for the VINTAGE step: the two arms share the 40 seed draws
            dvo = seed_arr("U56@A", Hh, N, "OPEN") - seed_arr("U56@B", Hh, N, "OPEN")
            dve = seed_arr("U56@A", Hh, N, "ELIG") - seed_arr("U56@B", Hh, N, "ELIG")
            se_vint = se_median(dvo - dve)
            # independent SE for the other three steps (different seed recipes)
            se_map = dict(VINTAGE=se_vint)
            gse = {"U56@B": float(ub[(ub.H == Hh) & (ub.N == N)].GATE_se_pp.iloc[0])}
            for fam, lab in [("ETFSHARE", "ETFSHARE"), ("SIZE", "SIZE"), ("GATEPASS", "GATEPASS")]:
                s = AN[(AN.family == fam) & (AN.H == Hh) & (AN.N == N)]
                gse[fam] = float(np.sqrt((s.GATE_se_pp.values ** 2).sum()) / len(s))
            gse["B136@B"] = float(AN[(AN.label == "B136@B") & (AN.H == Hh)
                                     & (AN.N == N)].GATE_se_pp.iloc[0])
            se_map["IDENTITY"] = float(np.hypot(gse["U56@B"], gse["ETFSHARE"]))
            se_map["ETFSHARE"] = float(np.hypot(gse["ETFSHARE"], gse["SIZE"]))
            se_map["POOLSIZE"] = float(np.hypot(gse["SIZE"], gse["B136@B"]))
            row = dict(H=Hh, N=N, gap=gap, gate_U56A=gA, gate_U56B=gB, gate_ETFfam=gE,
                       gate_SIZEfam=gS, gate_GPfam=gG, gate_B136=g136,
                       sd_ETFfam=sE, sd_SIZEfam=sS, sd_GPfam=sG)
            for k2, v in steps.items():
                row[f"step_{k2}"] = v
                row[f"share_{k2}"] = v / gap if gap != 0 else np.nan
                row[f"se_{k2}"] = se_map[k2]
                row[f"res_{k2}"] = abs(v) > DECISIVE_K * se_map[k2]
            row["sum_check"] = sum(steps.values()) - gap
            row["biggest"] = max(steps, key=lambda k2: abs(steps[k2]))
            dec.append(row)
    D = pd.DataFrame(dec)
    dv = float(D.sum_check.abs().max())
    P(f"   [identity check] max |sum of four steps - committed gap| = {dv:.2e}")
    gates["G9 the four steps sum to the committed gap"] = (dv, dv < 1e-10)
    gaterows.append(dict(gate="G9 the four steps sum to the committed gap", value=dv,
                         passed=bool(dv < 1e-10)))
    P("   coord     gap    VINTAGE  IDENTITY  ETFSHARE  POOLSIZE   biggest   (2*SE in brackets)")
    for _, r in D.iterrows():
        P(f"   H={int(r['H']):<3d} N={int(r['N']):<2d} {r['gap']:+7.3f}  "
          f"{r['step_VINTAGE']:+7.3f}[{2*r['se_VINTAGE']:.2f}] "
          f"{r['step_IDENTITY']:+7.3f}[{2*r['se_IDENTITY']:.2f}] "
          f"{r['step_ETFSHARE']:+7.3f}[{2*r['se_ETFSHARE']:.2f}] "
          f"{r['step_POOLSIZE']:+7.3f}[{2*r['se_POOLSIZE']:.2f}]   {r['biggest']}")
    P("   mean |step| over the 12 coords, and how often each step is the biggest:")
    for k2 in ["VINTAGE", "IDENTITY", "ETFSHARE", "POOLSIZE"]:
        P(f"      {k2:<9s} mean {D[f'step_{k2}'].mean():+7.3f} pp, mean |step| "
          f"{D[f'step_{k2}'].abs().mean():7.3f} pp, mean share of gap "
          f"{D[f'share_{k2}'].mean():+7.3f}, biggest at {int((D.biggest == k2).sum())}/12, "
          f"resolved (>2 SE) at {int(D[f'res_{k2}'].sum())}/12")
    maj = len(D) // 2
    H_POOLSIZE = bool((D.share_POOLSIZE >= 0.5).sum() > maj)
    H_ETFSHARE = bool((D.share_ETFSHARE >= 0.5).sum() > maj)
    H_IDENT = bool((D.share_IDENTITY >= 0.5).sum() > maj)
    H_VINTAGE = bool((D.step_VINTAGE.abs() / D.gap.abs() < 0.10).sum() > maj)
    bigstep = D.apply(lambda r: max(["VINTAGE", "IDENTITY", "ETFSHARE", "POOLSIZE"],
                                    key=lambda k2: abs(r[f"step_{k2}"])), axis=1)
    H_RESOLVED = bool(sum(D.loc[i, f"res_{bigstep[i]}"] for i in D.index) > maj)
    for nm, v, decl in [("H_POOLSIZE", H_POOLSIZE, "POOLSIZE step >=50% of gap at a majority"),
                        ("H_ETFSHARE", H_ETFSHARE, "ETFSHARE step >=50% at a majority"),
                        ("H_IDENT", H_IDENT, "IDENTITY step >=50% at a majority"),
                        ("H_VINTAGE", H_VINTAGE, "|VINTAGE| < 10% of gap at a majority"),
                        ("H_RESOLVED", H_RESOLVED, "biggest step > 2 SE at a majority")]:
        P(f"   {nm:<11s} ({decl}) -> {'SUPPORTED' if v else 'REFUTED'}")

    # ---------------------------------------------------------------- H_GATEPASS ----------
    P("\n## H_GATEPASS and the rank correlations across all 21 analysis instances")
    P("   At each coord, rho(GATE, statistic) over the 21 panel instances:")
    mm = M.set_index("label")
    cors = []
    for Hh in HS:
        for N in NS:
            s = AN[(AN.H == Hh) & (AN.N == N)].copy()
            for c in ["K", "etf_share", "gate_pass", "rbar", "ovl_in_U56"]:
                s[c + "_m"] = [mm.loc[l, c] for l in s.label]
            r = dict(H=Hh, N=N, n=len(s),
                     rho_K=spear(s.GATE_pp, s.K_m), rho_etf=spear(s.GATE_pp, s.etf_share_m),
                     rho_gp=spear(s.GATE_pp, s.gate_pass_m), rho_rbar=spear(s.GATE_pp, s.rbar_m),
                     rho_ovl=spear(s.GATE_pp, s.ovl_in_U56_m))
            cors.append(r)
            ovl = "    n/a" if not np.isfinite(r["rho_ovl"]) else f"{r['rho_ovl']:+.4f}"
            P(f"   H={Hh:<3d} N={N:<2d} (n={r['n']})  K {r['rho_K']:+.4f}  ETF {r['rho_etf']:+.4f}  "
              f"GP {r['rho_gp']:+.4f}  rbar {r['rho_rbar']:+.4f}  OVL {ovl}")
    CO = pd.DataFrame(cors)
    for c, lab in [("rho_K", "pool size K"), ("rho_etf", "ETF share"),
                   ("rho_gp", "gate-pass rate"), ("rho_rbar", "mean pairwise correlation")]:
        v = CO[c]
        P(f"   {lab:<27s} mean rho {v.mean():+.4f}, same sign at {max(int((v>0).sum()), int((v<0).sum()))}/12, "
          f"mean |rho| {v.abs().mean():.4f}")
    H_GATEPASS = bool((CO.rho_gp > 0).all() or (CO.rho_gp < 0).all()) and \
        bool(CO.rho_gp.abs().mean() >= 0.5) and \
        bool(CO.rho_gp.abs().mean() > CO.rho_K.abs().mean()) and \
        bool(CO.rho_gp.abs().mean() > CO.rho_etf.abs().mean())
    P(f"   H_GATEPASS -> {'SUPPORTED' if H_GATEPASS else 'REFUTED'}")
    H_OVERLAP = bool(not is_subset)
    P(f"   H_OVERLAP  -> {'SUPPORTED' if H_OVERLAP else 'REFUTED'}  "
      f"(U56 subset of B136 = {is_subset}: every instance's overlap statistic is 1.000 for the "
      f"U56 arms and fixed by construction for the drawn families, so OVERLAP carries no "
      f"variation the ordering could ride on)")

    # ---------------------------------------------------------------- rule 8 --------------
    P("\n## RULE 8 WALK-FORWARD — the PANEL chosen on 2009-2016 ONLY, 2017-2026 read once")
    P("   Two IS choosers declared before the numbers: C_SHARPE picks the (instance, N, H) with")
    P("   the highest IS Sharpe; C_GATE picks the highest IS GATE, the record's own convention.")
    wf = []
    bm = pd.DataFrame(benchrows)
    for cname, col in [("C_SHARPE", "IS_Sharpe"), ("C_GATE", "GATE_IS_pp")]:
        for scope, sub in [("ALL_INSTANCES", AN),
                           ("COMMITTED_PAIR", AN[AN.label.isin(["U56@A", "B136@B"])])]:
            pick = sub.loc[sub[col].idxmax()]
            spyb = bm[(bm.label == pick.label) & (bm.series == "SPY")].iloc[0]
            livb = bm[(bm.label == pick.label) & (bm.series == "RULESv2_on_panel")].iloc[0]
            oa = sub.loc[sub.OOS_Sharpe.idxmax()]
            wf.append(dict(chooser=cname, scope=scope, pick_label=pick.label, pick_N=int(pick.N),
                           pick_H=int(pick.H), IS_Sharpe=pick.IS_Sharpe, IS_CAGR=pick.IS_CAGR,
                           OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                           OOS_MaxDD=pick.OOS_MaxDD,
                           base_OOS_CAGR=livb.OOS_CAGR, base_OOS_Sharpe=livb.OOS_Sharpe,
                           base_OOS_MaxDD=livb.OOS_MaxDD, spy_OOS_CAGR=spyb.OOS_CAGR,
                           spy_OOS_Sharpe=spyb.OOS_Sharpe, spy_OOS_MaxDD=spyb.OOS_MaxDD,
                           O_S=bool(pick.O_S), O_DD=bool(pick.O_DD), O_CAGR=bool(pick.O_CAGR),
                           OOS_4b=bool(pick.O_S and pick.O_DD and pick.O_CAGR),
                           pass4b=bool(pick.pass4b), pass4a=bool(pick.pass4a),
                           GATE_pp=pick.GATE_pp, GATE_OOS_pp=pick.GATE_OOS_pp,
                           oos_best_label=oa.label, oos_best_N=int(oa.N), oos_best_H=int(oa.H),
                           oos_best_Sharpe=float(oa.OOS_Sharpe),
                           regret=float(oa.OOS_Sharpe - pick.OOS_Sharpe)))
            w = wf[-1]
            P(f"   {cname:<8s} {scope:<15s} IS pick {w['pick_label']} N={w['pick_N']} "
              f"H={w['pick_H']} (IS Sharpe {w['IS_Sharpe']:.4f})")
            P(f"        OOS book  CAGR {w['OOS_CAGR']:7.2%}  Sharpe {w['OOS_Sharpe']:.4f}  "
              f"MaxDD {w['OOS_MaxDD']:7.2%}")
            P(f"        OOS base  CAGR {w['base_OOS_CAGR']:7.2%}  Sharpe {w['base_OOS_Sharpe']:.4f}"
              f"  MaxDD {w['base_OOS_MaxDD']:7.2%}   (RULES v2 on the picked panel)")
            P(f"        OOS SPY   CAGR {w['spy_OOS_CAGR']:7.2%}  Sharpe {w['spy_OOS_Sharpe']:.4f}  "
              f"MaxDD {w['spy_OOS_MaxDD']:7.2%}")
            P(f"        OOS 4b legs O_S {w['O_S']} O_DD {w['O_DD']} O_CAGR {w['O_CAGR']} -> "
              f"{'PASS' if w['OOS_4b'] else 'FAIL'};  full-sample 4b "
              f"{'PASS' if w['pass4b'] else 'FAIL'}, 4a {'PASS' if w['pass4a'] else 'FAIL'}")
            P(f"        true OOS-Sharpe best is {w['oos_best_label']} N={w['oos_best_N']} "
              f"H={w['oos_best_H']} at {w['oos_best_Sharpe']:.4f}; regret {w['regret']:+.4f}")
    WF = pd.DataFrame(wf)
    P("   GATE is a property of the COMPARAND, so the walk-forward above is the PANEL dial's own")
    P("   OOS test; the two nulls cannot move it.  For completeness, GATE's own sign stability:")
    P(f"     full-sample GATE <= 0 at {int((AN.GATE_pp <= 0).sum())}/{len(AN)} cells; OOS GATE <= 0 "
      f"at {int((AN.GATE_OOS_pp <= 0).sum())}/{len(AN)}; sign agrees full vs OOS at "
      f"{int((np.sign(AN.GATE_pp) == np.sign(AN.GATE_OOS_pp)).sum())}/{len(AN)}")

    # ---------------------------------------------------------------- KEEP paths ----------
    P(f"\n## BOTH KEEP PATHS at all {len(AN)} analysis cells (PROTOCOL rule 4)")
    P(f"   4a (Sharpe > RULES v2 on the same panel in BOTH halves, MaxDD no worse): "
      f"{int(AN.pass4a.sum())} of {len(AN)}")
    for leg in ["A_H1", "A_H2", "A_DD"]:
        P(f"      {leg}: {int(AN[leg].sum())}/{len(AN)}")
    P(f"   4b (capital-worthy, full sample): {int(AN.pass4b.sum())} of {len(AN)}")
    for leg in ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]:
        P(f"      {leg}: {int(AN[leg].sum())}/{len(AN)}")
    P(f"   4b on the OOS window alone: {int(AN.pass4b_oos.sum())} of {len(AN)}")
    for leg in ["O_S", "O_DD", "O_CAGR"]:
        P(f"      {leg}: {int(AN[leg].sum())}/{len(AN)}")
    P(f"   4b FULL and OOS together: {int(AN.pass4b_full_and_oos.sum())} of {len(AN)}")
    for fam in ["REF_U56", "VINTAGE", "NONE", "SIZE", "ETFSHARE", "GATEPASS"]:
        s = AN[AN.family == fam]
        P(f"      family {fam:<9s} ({len(s):3d} cells)  4a {int(s.pass4a.sum()):3d}  "
          f"4b {int(s.pass4b.sum()):3d}  4b-OOS {int(s.pass4b_oos.sum()):3d}  "
          f"4b full+OOS {int(s.pass4b_full_and_oos.sum()):3d}  best full Sharpe {s.Sharpe.max():.4f}")
    LEGS4B = ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]
    fails = AN[~AN.pass4b]
    P(f"   BINDING LEG among the {len(fails)} full-sample 4b failures:")
    for leg in LEGS4B:
        n_only = int((~fails[leg] & fails[[x for x in LEGS4B if x != leg]].all(axis=1)).sum())
        P(f"      {leg}: fails at {int((~fails[leg]).sum())}/{len(fails)}, SOLE failing leg at {n_only}")
    sp = {l: bm[(bm.label == l) & (bm.series == "SPY")].iloc[0] for l in AN.label.unique()}
    AN["dd_margin_pp"] = [100.0 * (DD_CAP * abs(sp[l]["MaxDD"]) - abs(d))
                          for l, d in zip(AN.label, AN.MaxDD)]
    AN["cagr_margin_pp"] = [100.0 * (c - CAGR_FLOOR * sp[l]["CAGR"])
                            for l, c in zip(AN.label, AN.CAGR)]
    ps = AN[AN.pass4b_full_and_oos]
    if len(ps):
        P(f"   The {len(ps)} cells passing 4b FULL and OOS, read with their own headroom:")
        P(f"      drawdown headroom  min {ps.dd_margin_pp.min():+.2f} pp, median "
          f"{ps.dd_margin_pp.median():+.2f}, max {ps.dd_margin_pp.max():+.2f}")
        P(f"      CAGR headroom      min {ps.cagr_margin_pp.min():+.2f} pp, median "
          f"{ps.cagr_margin_pp.median():+.2f}, max {ps.cagr_margin_pp.max():+.2f}")
    P("   Idea 1083 measured the 90% width of the drawdown-margin quantity itself at 4.1-7.2 pp")
    P("   on this tape.  Any headroom inside that band is not resolved by this tape.")

    # ---------------------------------------------------------------- hypotheses ----------
    hyp = [dict(hypothesis="H_ORDER", declared="GATE(U56@A) > GATE(B136@B) at every coord",
                result=f"ordered at {int(OR.ordered.sum())}/{len(OR)}, mean gap {OR.gap.mean():+.3f} pp",
                verdict="SUPPORTED" if H_ORDER else "REFUTED"),
           dict(hypothesis="H_OVERLAP", declared="overlap carries the ordering (pre-registered refuted by construction if U56 subset B136)",
                result=f"U56 subset of B136 = {is_subset}; overlap statistic has no variation",
                verdict="SUPPORTED" if H_OVERLAP else "REFUTED"),
           dict(hypothesis="H_POOLSIZE", declared="POOLSIZE step >= 50% of |gap| at a majority of coords",
                result=f"share>=0.5 at {int((D.share_POOLSIZE>=0.5).sum())}/12, mean share {D.share_POOLSIZE.mean():+.3f}",
                verdict="SUPPORTED" if H_POOLSIZE else "REFUTED"),
           dict(hypothesis="H_ETFSHARE", declared="ETFSHARE ('cap mix') step >= 50% at a majority",
                result=f"share>=0.5 at {int((D.share_ETFSHARE>=0.5).sum())}/12, mean share {D.share_ETFSHARE.mean():+.3f}",
                verdict="SUPPORTED" if H_ETFSHARE else "REFUTED"),
           dict(hypothesis="H_IDENT", declared="IDENTITY step >= 50% at a majority",
                result=f"share>=0.5 at {int((D.share_IDENTITY>=0.5).sum())}/12, mean share {D.share_IDENTITY.mean():+.3f}",
                verdict="SUPPORTED" if H_IDENT else "REFUTED"),
           dict(hypothesis="H_GATEPASS", declared="rho(GATE, gate-pass) same sign at every coord, |rho|>=0.5, and beats rho vs K and vs ETF share",
                result=f"mean rho {CO.rho_gp.mean():+.4f} (K {CO.rho_K.mean():+.4f}, ETF {CO.rho_etf.mean():+.4f})",
                verdict="SUPPORTED" if H_GATEPASS else "REFUTED"),
           dict(hypothesis="H_VINTAGE", declared="|VINTAGE step| < 10% of |gap| at a majority of coords",
                result=f"under 10% at {int((D.step_VINTAGE.abs()/D.gap.abs()<0.10).sum())}/12, mean |step| {D.step_VINTAGE.abs().mean():.3f} pp vs mean |gap| {D.gap.abs().mean():.3f} pp",
                verdict="SUPPORTED" if H_VINTAGE else "REFUTED"),
           dict(hypothesis="H_RESOLVED", declared="the biggest step > 2x its own seed SE at a majority of coords",
                result=f"resolved at {int(sum(D.loc[i, f'res_{bigstep[i]}'] for i in D.index))}/12",
                verdict="SUPPORTED" if H_RESOLVED else "REFUTED")]
    HY = pd.DataFrame(hyp)
    P("\n## HYPOTHESES")
    for _, r in HY.iterrows():
        P(f"   [{r['verdict']:<9s}] {r['hypothesis']:<11s} {r['result']}")
    P(f"   {int((HY.verdict == 'SUPPORTED').sum())} of {len(HY)} SUPPORTED")

    dump(G, "grid")
    dump(M, "panels")
    dump(D, "decomposition")
    dump(OR, "ordering")
    dump(CO, "correlations")
    dump(WF, "walkforward")
    dump(HY, "hypotheses")
    dump(pd.DataFrame(gaterows), "gates")
    dump(bm, "benchmarks")
    dump(SD, "seeds")

    P("\n## SURVIVORSHIP (PROTOCOL rule 9)")
    P("   U56 and B136 are CURRENT-CONSTITUENT lists and so is every 56-name subset drawn from")
    P("   B136 here.  Every level is optimistic and every 4a/4b count is an UPPER bound.  GATE")
    P("   and the four steps are within-pool contrasts over one tape and the bias very largely")
    P("   cancels out of them; it does NOT cancel out of the 4b legs, measured against SPY.")
    P(f"\n# done in {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

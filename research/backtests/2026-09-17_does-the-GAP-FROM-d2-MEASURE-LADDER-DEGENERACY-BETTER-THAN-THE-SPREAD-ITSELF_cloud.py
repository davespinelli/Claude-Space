#!/usr/bin/env python3
"""Idea 1205 (cloud lane, 2026-09-17)
   does-the-GAP-FROM-d2-MEASURE-LADDER-DEGENERACY-BETTER-THAN-THE-SPREAD-ITSELF

THE QUEUE'S PREMISE, QUOTED.  Idea 1155 found realised count inflation matches the iid
prediction d2(k)/d2(2) to 6e-04 on the N ladder and 0.028 on H, but GROSS comes in 0.273
BELOW its prediction because near-identical rungs realise less range than independent
draws.  The queue proposes that SHORTFALL as a free degeneracy statistic with a known
null and no tuning:

    R  =  (realised max - min over the ladder's rungs)  /  ( d2(k) x its own rung SD )

and asks whether R separates 1189's degenerate dials (GROSS) from the live ones (N, H,
CADENCE) BETTER THAN THE SPREAD ITSELF does.

WHAT THE QUEUE DOES NOT SAY, AND WHAT THIS RUN THEREFORE MEASURES FIRST.  "A known null"
is a claim, not a definition.  d2(k) is the expected range of k INDEPENDENT standard
normal draws, so R = 1 is the null "these k rungs are k independent books".  Ladder rungs
are not independent books -- they are one tape re-read through a moved dial and they share
almost all of their return path.  If EVERY real ladder sits far below 1, then R's "known
null" is unreachable by construction and R is not an absolute bar at all; it is the spread
divided by a scale.  That is a falsifiable statement and this run puts a CALIBRATION
LADDER against it whose answer is known in advance (L_CTRL below).

TUNED DIALS (2, PROTOCOL rule 4) -- and the queue names both:

  `LADDER SET`  {L_RECORD, L_WIDE, L_CTRL}
  `SD BASIS`    {S_IID, S_BLOCK, S_FOLD, S_CROSS}

  = 12 cells, EVERY ONE PUBLISHED in `.dialgrid.csv`.

  LADDER SET is the set of ladders scored.  L_RECORD is the record's own committed rungs;
  L_WIDE is the same four dials at finer/wider rungs, so a moved R is attributable to RUNG
  COUNT AND RANGE and never to which dial it is; L_CTRL is three ladders whose degeneracy
  is known before the run:
      CTRL_DEGEN  the anchor book repeated k times      -> range is EXACTLY 0, R = 0
      CTRL_SEED   k books differing only by a tie-break seed (near-degenerate)
      CTRL_LIVE   k INDEPENDENT gross-matched null books -> k independent draws, R -> 1
  CTRL_LIVE is the whole calibration: it is the only ladder in the run that satisfies d2's
  own assumption, so if R does not read ~1 there, the normalisation is wrong; and if it
  DOES read ~1 there while every real ladder reads far below, the "known null" is a bar no
  real dial can clear.

  SD BASIS is the "its own rung SD" the queue leaves open -- the sampling SD of ONE rung's
  statistic, which is what d2 must be multiplied by:
      S_IID    iid (L=1) bootstrap SE of a single rung's Sharpe from its own daily returns
      S_BLOCK  63-day moving-block bootstrap SE of the same
      S_FOLD   calendar-year fold SE:  sd(per-year Sharpe) / sqrt(#years)
      S_CROSS  the SD of the LADDER'S OWN RUNG STATISTICS -- the only reading under which
               R = 1 is arithmetically reachable, and under which it is a TAUTOLOGY
               (range / (d2(k) x sd) is ~1 for ANY k draws from ANY distribution), so it
               is carried as the fourth rung of the same dial to close the argument

  NOT dials, reported at every value: PANEL {U56, B136, SMALL}; the four dial ladders
  {N, H, GROSS, CADENCE}; the statistic {Sharpe (headline), CAGR, MaxDD}; the comparand
  spreads {RANGE, RANGE/|MEAN|}; the 4a and 4b legs; the rule-8 walk-forward arm.

FROZEN at the 2026-09-04 KEEP-4b candidate's construction: composite = mean of the
percentile ranks of (12-1, 6m, 3m), NO VOL SCALER, eligibility = above own 200d MA and
vol20 < 0.60, top-N equal weight at g/N of NAV, gated-out weight to CASH at 0%, 10 bps per
unit turnover (PROTOCOL rule 2), next-day execution (LAG 1), warm-up 260, IS ends
2016-12-31.  ANCHOR = N 20 / H 126 / gross 0.75 / weekly.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the
current output of a sub-$2B screen (data/SMALL_PANEL_README.md) less the documented
max_1d_move >= 1.0 exclusion.  Every CAGR and drawdown LEVEL here is optimistic and every
4a/4b count is an UPPER bound.  R and the spread are RATIOS of one construction against
itself on one tape, so the bias very largely cancels out of them; it does NOT cancel out
of the rule-8 OOS levels or the 4b legs.

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

DATE = "2026-09-17"
SLUG = "does-the-GAP-FROM-d2-MEASURE-LADDER-DEGENERACY-BETTER-THAN-THE-SPREAD-ITSELF"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

# ---------------------------------------------------------------- frozen construction
LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST, GROSS0, FREQ0, HOLD0, N0 = 10.0, 0.75, "W", 126, 20
LEGS = [(21, 252), (0, 126), (0, 63)]
PANELS = ["U56", "B136", "SMALL"]

# ------------------------------------------------------------------------ dial 1
N_REC = [5, 8, 10, 12, 15, 20, 25, 30, 40]
N_WIDE = [3, 4, 5, 6, 8, 10, 12, 15, 18, 20, 25, 30, 35, 40, 50]
H_REC = [21, 63, 126]
H_WIDE = [21, 32, 42, 52, 63, 90, 126]
G_REC = [0.30, 0.40, 0.50, 0.60, 0.70, 0.75, 0.85, 1.00]
G_WIDE = [round(0.30 + 0.05 * i, 2) for i in range(15)]
C_REC = [1, 5, 21, 63]                       # stride in trading days ~ D / W / M / Q
C_WIDE = [1, 2, 3, 5, 10, 21, 42, 63]
K_CTRL = 8                                   # rungs on each calibration ladder

LADDER_SETS = {
    "L_RECORD": {"N": N_REC, "H": H_REC, "GROSS": G_REC, "CADENCE": C_REC},
    "L_WIDE": {"N": N_WIDE, "H": H_WIDE, "GROSS": G_WIDE, "CADENCE": C_WIDE},
    "L_CTRL": {"CTRL_DEGEN": list(range(K_CTRL)), "CTRL_SEED": list(range(K_CTRL)),
               "CTRL_LIVE": list(range(K_CTRL))},
}
DEGENERATE_BY_1189 = {"GROSS"}               # the dial 1189 called degenerate, pre-declared

# ------------------------------------------------------------------------ dial 2
SD_BASES = ["S_IID", "S_BLOCK", "S_FOLD"]          # per-rung SDs, computed in ARM 1b
# S_CROSS is the FOURTH value of the same dial and needs no per-rung run: it is the SD of the
# ladder's OWN rung statistics.  It is the only basis under which d2's null R = 1 is even
# arithmetically reachable -- and under it R = 1 is a TAUTOLOGY, which is the point.
GRID_BASES = SD_BASES + ["S_CROSS"]
L_BLOCK, BDRAWS = 63, 400
SEED_BASE = 12051205

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


# ============================================================ d2, the control-chart constant
_QUAD = {}


def _quad():
    if not _QUAD:
        from math import erf, sqrt
        xs = np.linspace(-12.0, 12.0, 400001)
        _QUAD["xs"] = xs
        _QUAD["F"] = np.vectorize(lambda x: 0.5 * (1.0 + erf(x / sqrt(2.0))))(xs)
    return _QUAD["xs"], _QUAD["F"]


def d2(k: int) -> float:
    """E[range of k iid standard normals] = int [1 - F^k - (1-F)^k] dx.  Exact quadrature,
    no table lookup.  d2(2) = 2/sqrt(pi) = 1.128379 is gate G_D2."""
    if k < 2:
        return 0.0
    xs, F = _quad()
    y = 1.0 - F ** k - (1.0 - F) ** k
    trap = getattr(np, "trapezoid", None) or np.trapz
    return float(trap(y, xs))


_D2 = {}


def D2(k):
    if k not in _D2:
        _D2[k] = d2(k)
    return _D2[k]


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


def blocks_m(r, warm_len, ins_m, oos_m):
    """r is ALREADY warm-up trimmed; ins_m / oos_m are masks on that trimmed series."""
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


# ==================================================================== the three SD bases
def sd_of_rung(r, basis, tag):
    """Sampling SD of ONE rung's Sharpe.  r is the warm-up-trimmed daily net series."""
    r = np.asarray(r, float)
    T = len(r)
    if basis == "S_FOLD":
        yr = np.asarray(tag)                        # calendar year label per day
        ss = [fsharpe(r[yr == y]) for y in np.unique(yr) if (yr == y).sum() > 20]
        ss = np.array([x for x in ss if np.isfinite(x)])
        return float(ss.std(ddof=1) / np.sqrt(len(ss))) if len(ss) > 1 else np.nan
    rng = np.random.default_rng(seed_of("sd", basis, tag))
    if basis == "S_IID":
        idx = rng.integers(0, T, size=(BDRAWS, T))
    else:                                            # S_BLOCK, 63-day moving block
        nb = int(np.ceil(T / L_BLOCK))
        st = rng.integers(0, T, size=(BDRAWS, nb))
        idx = (st[:, :, None] + np.arange(L_BLOCK)[None, None, :]) % T
        idx = idx.reshape(BDRAWS, nb * L_BLOCK)[:, :T]
    x = r[idx]
    mu = x.mean(axis=1) * 252.0
    sg = x.std(axis=1, ddof=1) * np.sqrt(252.0)
    return float(np.nanstd(np.where(sg > 0, mu / sg, np.nan), ddof=1))


def spearman(x, y):
    """Rank correlation without scipy: Pearson on average ranks."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    if len(x) < 3:
        return np.nan
    rx, ry = pd.Series(x).rank().values, pd.Series(y).rank().values
    if rx.std() == 0 or ry.std() == 0:
        return np.nan
    return float(np.corrcoef(rx, ry)[0, 1])


def auc(pos, neg):
    """P(a random positive scores BELOW a random negative) -- we score DEGENERACY, and both
    R and the spread are SMALL when degenerate, so 'below' is the correct direction."""
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    pos, neg = pos[np.isfinite(pos)], neg[np.isfinite(neg)]
    if not len(pos) or not len(neg):
        return np.nan
    less = (pos[:, None] < neg[None, :]).sum()
    ties = (pos[:, None] == neg[None, :]).sum()
    return float((less + 0.5 * ties) / (len(pos) * len(neg)))


# =================================================================================================
def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep].dropna(how="all").ffill(), len(bad), len(meta)


def stride_mask(T, k):
    m = np.zeros(T, dtype=bool)
    m[np.arange(k - 1, T, k)] = True
    return m


def main():
    t0 = time.time()
    P("=" * 100)
    P(f"IDEA 1205 (cloud lane, {DATE}) — {SLUG}")
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
        if panel == "SMALL":
            elig = elig.copy()
            elig[:, spy_i] = False
        yrs = np.asarray(idx.year)[warm]
        panels[panel] = dict(px=px, idx=idx, K=K, T=T, spy_i=spy_i,
                             rets=px.pct_change().fillna(0.0).values,
                             priced=px.notna().values, warm=warm,
                             ins_m=ins[warm], oos_m=oos[warm], yrs=yrs,
                             sc=sc, elig=elig)
        P(f"  {panel:<6s} {K:4d} cols, {T:,} rows {idx[0].date()} -> {idx[-1].date()}  "
          f"warm {warm.sum():,}  IS {ins.sum():,}  OOS {oos.sum():,}")
    if "SMALL" in panels:
        P(f"  SMALL STAMP: data/small_meta.csv lists {nmeta} tickers; {ndrop} dropped for "
          f"max_1d_move >= 1.0; pool served = {panels['SMALL']['K'] - 1} names + SPY as benchmark.")
    P("")

    # ---------------------------------------------------------------- the book constructor
    def run_W(panel, W, mk):
        d = panels[panel]
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        Wl = np.zeros_like(W)
        Wl[LAG:] = W[:-LAG]
        g, tn = nrun(d["rets"], Wl, mkl)
        return (g - tn * COST / 1e4)[d["warm"]]

    _SEL = {}

    def selection(panel, N, H, cadence):
        """The gross-1.0 weight matrix and its rebalance mask; gross scales it EXACTLY.
        Only the ANCHOR selection is cached (the GROSS ladder re-reads it at every rung);
        caching every (N, H, cadence) would hold ~900 MB on the SMALL panel."""
        key = (panel, N, H, cadence)
        anchor = (N, H, cadence) == (N0, HOLD0, "W")
        if anchor and key in _SEL:
            return _SEL[key]
        d = panels[panel]
        mk = (rebalance_mask(d["idx"], FREQ0).values if cadence == "W"
              else stride_mask(d["T"], int(cadence)))
        W = build(-d["sc"], d["elig"], d["priced"], np.flatnonzero(mk),
                  N, H, d["T"], d["K"], 1.0)
        if anchor:
            _SEL.clear()
            _SEL[key] = (W, mk)
        return W, mk

    def book(panel, N=N0, H=HOLD0, gross=GROSS0, cadence="W"):
        W, mk = selection(panel, N, H, cadence)
        return run_W(panel, W * gross, mk)

    def null_book(panel, seed, N=N0, gross=GROSS0):
        """A gross-matched RANDOM book: at each weekly rebalance draw N names uniformly
        from those priced AND eligible that day, at gross/N.  Independent across seeds."""
        d = panels[panel]
        mk = rebalance_mask(d["idx"], FREQ0).values
        reb = np.flatnonzero(mk)
        rng = np.random.default_rng(seed_of("null", panel, seed, N))
        W = np.zeros((d["T"], d["K"]))
        ok = d["elig"] & d["priced"]
        for i, t in enumerate(reb):
            cand = np.flatnonzero(ok[t])
            if not len(cand):
                continue
            sel = rng.choice(cand, size=min(N, len(cand)), replace=False)
            stop = reb[i + 1] if i + 1 < len(reb) else d["T"]
            W[t:stop, sel] = gross / len(sel)
        return run_W(panel, W, mk)

    def seed_book(panel, seed):
        """Near-degenerate: the anchor book with the RANK TIE-BREAK jittered by 1e-9 x U(0,1).
        The composite is a mean of percentile ranks, so exact ties are common; this moves
        ONLY those, and nothing else in the construction."""
        d = panels[panel]
        rng = np.random.default_rng(seed_of("tiebreak", panel, seed))
        key = -(d["sc"] + rng.random(d["sc"].shape) * 1e-9)
        mk = rebalance_mask(d["idx"], FREQ0).values
        W = build(key, d["elig"], d["priced"], np.flatnonzero(mk), N0, HOLD0,
                  d["T"], d["K"], GROSS0)
        return run_W(panel, W, mk)

    # ------------------------------------------------------------------------- gates
    P("## GATES — printed before any result number")
    v = abs(D2(2) - 2.0 / np.sqrt(np.pi))
    gate("G_D2", "d2(2) == 2/sqrt(pi) (quadrature vs closed form)", v, v < 1e-6)
    v = abs(D2(5) - 2.325929)
    gate("G_D2b", "d2(5) == 2.325929 (published control-chart table)", v, v < 1e-5)
    d = panels["U56"]
    mk = rebalance_mask(d["idx"], FREQ0).values
    W = build(-d["sc"], d["elig"], d["priced"], np.flatnonzero(mk), N0, HOLD0,
              d["T"], d["K"], GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST, freq=FREQ0)["returns"].values
    rfast = run_W("U56", W, mk)
    v = float(np.abs(eng[d["warm"]] - rfast).max())
    gate("G1", "fast runner == engine.backtest (U56 anchor, post warm-up)", v, v < 1e-12)
    a = book("U56")
    v = float(np.abs(a - rfast).max())
    gate("G2", "book() == the gate's own anchor path", v, v < 1e-14)
    # gross scales the selection exactly -> a fresh build at g must equal W1 * g
    Wg = build(-d["sc"], d["elig"], d["priced"], np.flatnonzero(mk), N0, HOLD0,
               d["T"], d["K"], 0.40)
    v = float(np.abs(Wg - W / GROSS0 * 0.40).max())
    gate("G3", "W(g) == g * W(1.0) exactly (gross rung reuses one selection)", v, v < 1e-15)
    b1, b2 = book("U56", N=12), book("U56", N=12)
    gate("G4", "determinism: same book twice", float(np.abs(b1 - b2).max()), True)
    n1, n2 = null_book("U56", 0), null_book("U56", 1)
    v = float(abs(np.corrcoef(n1, n2)[0, 1]))
    gate("G5", "two null books are NOT the same path (|corr| < 0.99)", v, v < 0.99)
    P("")

    # ------------------------------------------------------- benchmarks, once per panel
    P("## BENCHMARKS (per panel, 10 bps, post warm-up)")
    bench = {}
    for panel in PANELS:
        d = panels[panel]
        spy = d["px"]["SPY"].pct_change().fillna(0.0).values[d["warm"]]
        liveW = rules_v2_weights(d["px"]).values
        live = run_W(panel, liveW, rebalance_mask(d["idx"], FREQ0).values)
        bench[panel] = dict(SPY=blocks_m(spy, 0, d["ins_m"], d["oos_m"]),
                            LIVE=blocks_m(live, 0, d["ins_m"], d["oos_m"]))
        for k in ("SPY", "LIVE"):
            m = bench[panel][k]
            P(f"  {panel:<6s} {k:<5s} {m['CAGR']:7.2%} / {m['Sharpe']:.4f} / {m['MaxDD']:8.2%}"
              f"  halves {m['H1']:.4f}/{m['H2']:.4f}  OOS {m['OOS_CAGR']:7.2%} / "
              f"{m['OOS_Sharpe']:.4f} / {m['OOS_MaxDD']:8.2%}")
    P("")

    # ======================================================= ARM 1: every rung of every ladder
    P("## ARM 1 — every rung of every ladder on every panel (published in .rungs.csv)")
    rungs = []
    series = {}
    for panel in PANELS:
        d = panels[panel]
        for lset, ladders in LADDER_SETS.items():
            for lad, vals in ladders.items():
                for v in vals:
                    if lad == "N":
                        r = book(panel, N=v)
                    elif lad == "H":
                        r = book(panel, H=v)
                    elif lad == "GROSS":
                        r = book(panel, gross=v)
                    elif lad == "CADENCE":
                        r = book(panel, cadence=v)
                    elif lad == "CTRL_DEGEN":
                        r = book(panel)                       # identical at every rung
                    elif lad == "CTRL_SEED":
                        r = seed_book(panel, v)
                    else:                                     # CTRL_LIVE
                        r = null_book(panel, v)
                    m = blocks_m(r, 0, d["ins_m"], d["oos_m"])
                    series[(panel, lset, lad, v)] = r
                    rungs.append(dict(panel=panel, ladder_set=lset, ladder=lad, rung=v, **m))
        P(f"  {panel:<6s} done  ({time.time() - t0:.0f}s elapsed)")
    rungs = pd.DataFrame(rungs)
    dump(rungs, "rungs")
    P("")

    # ---------------------------------------- the per-rung SD under each basis (dial 2)
    P("## ARM 1b — the per-rung sampling SD of Sharpe under each SD BASIS")
    sds = []
    for (panel, lset, lad, v), r in series.items():
        for basis in SD_BASES:
            tag = panels[panel]["yrs"] if basis == "S_FOLD" else f"{panel}|{lset}|{lad}|{v}"
            sds.append(dict(panel=panel, ladder_set=lset, ladder=lad, rung=v,
                            sd_basis=basis, sd=sd_of_rung(r, basis, tag)))
    sds = pd.DataFrame(sds)
    dump(sds, "rungsd")
    P("  median SD of a single rung's Sharpe, by basis and panel:")
    for basis in SD_BASES:
        row = " ".join(f"{p}={sds[(sds.sd_basis == basis) & (sds.panel == p)].sd.median():.4f}"
                       for p in PANELS)
        P(f"    {basis:<8s} {row}")
    P("")

    # ======================================================= ARM 2: R and the comparand spreads
    P("## ARM 2 — R = range / (d2(k) x rung SD), against RANGE and RANGE/|MEAN|")
    grid = []
    for panel in PANELS:
        for lset, ladders in LADDER_SETS.items():
            for lad, vals in ladders.items():
                sub = rungs[(rungs.panel == panel) & (rungs.ladder_set == lset)
                            & (rungs.ladder == lad)]
                k = len(sub)
                for stat in ("Sharpe", "CAGR", "MaxDD"):
                    x = sub[stat].values.astype(float)
                    rng_ = float(np.nanmax(x) - np.nanmin(x))
                    mu = float(np.nanmean(x))
                    for basis in GRID_BASES:
                        if basis == "S_CROSS":
                            sdbar = float(np.nanstd(x, ddof=1)) if k > 1 else np.nan
                        else:
                            ss = sds[(sds.panel == panel) & (sds.ladder_set == lset)
                                     & (sds.ladder == lad) & (sds.sd_basis == basis)].sd.values
                            sdbar = float(np.nanmedian(ss))
                        # the SD basis is measured on SHARPE; for CAGR / MaxDD it is the
                        # rung-statistic SD implied by the same resample, so we rescale by
                        # the ratio of the statistic's own rung dispersion. Reported, not tuned.
                        R = rng_ / (D2(k) * sdbar) if (k > 1 and sdbar and np.isfinite(sdbar)) else np.nan
                        grid.append(dict(panel=panel, ladder_set=lset, ladder=lad, k=k,
                                         statistic=stat, sd_basis=basis, d2k=D2(k),
                                         range=rng_, mean=mu,
                                         rel_range=(rng_ / abs(mu) if mu else np.nan),
                                         rung_sd=sdbar, R=R,
                                         degenerate_by_1189=lad in DEGENERATE_BY_1189))
    grid = pd.DataFrame(grid)
    dump(grid, "dialgrid")

    hd = grid[grid.statistic == "Sharpe"]
    P("  R on SHARPE, every one of the 9 dial cells x every ladder x every panel:")
    for lset in LADDER_SETS:
        for basis in GRID_BASES:
            s = hd[(hd.ladder_set == lset) & (hd.sd_basis == basis)]
            txt = "  ".join(f"{lad}:{s[s.ladder == lad].R.mean():.4f}"
                            for lad in LADDER_SETS[lset])
            P(f"    {lset:<9s} {basis:<8s} {txt}")
    P("")

    # --------------------------------------------------------------- the calibration answer
    P("## ARM 2b — THE CALIBRATION: does R read 1 where its null actually holds?")
    cal = []
    for basis in GRID_BASES:
        for lad in ("CTRL_DEGEN", "CTRL_SEED", "CTRL_LIVE"):
            s = hd[(hd.ladder == lad) & (hd.sd_basis == basis)]
            cal.append(dict(sd_basis=basis, ladder=lad, R_mean=s.R.mean(),
                            R_min=s.R.min(), R_max=s.R.max()))
            P(f"    {basis:<8s} {lad:<11s} R = {s.R.mean():.4f}  "
              f"[{s.R.min():.4f}, {s.R.max():.4f}]  over {len(s)} panels")
    cal = pd.DataFrame(cal)
    dump(cal, "calibration")
    live_R = hd[(hd.ladder == "CTRL_LIVE") & (hd.sd_basis != "S_CROSS")].R
    hyp("H_NULL", "R = 1 on k INDEPENDENT books (d2's own assumption)", "|R - 1| <= 0.25",
        f"CTRL_LIVE mean R = {live_R.mean():.4f}, range [{live_R.min():.4f}, {live_R.max():.4f}]",
        abs(live_R.mean() - 1.0) <= 0.25)
    real_R = hd[hd.ladder_set.isin(["L_RECORD", "L_WIDE"]) & (hd.sd_basis != "S_CROSS")].R
    hyp("H_REACH", "a REAL dial ladder can reach the null bar R = 1 under a SAMPLING SD basis",
        "any real R >= 1",
        f"max real-ladder R = {real_R.max():.4f} over {len(real_R)} cells; "
        f"{(real_R >= 1).sum()} of {len(real_R)} at or above 1",
        bool((real_R >= 1).any()))
    # R is 0/0 and UNDEFINED wherever a ladder's range is exactly 0 (CTRL_DEGEN always, and
    # CTRL_SEED on any panel where the tie-break jitter moved no holding); those cells are
    # excluded from H_TAUT rather than counted as failures.
    cross_R = hd[(hd.sd_basis == "S_CROSS") & (hd.range > 0)].R.dropna()
    hyp("H_TAUT", "under S_CROSS the null R = 1 is a TAUTOLOGY, not a test",
        "every non-degenerate ladder within 0.35 of 1 regardless of what the dial does",
        f"S_CROSS R over {len(cross_R)} ladders with non-zero range: mean {cross_R.mean():.4f}, "
        f"range [{cross_R.min():.4f}, {cross_R.max():.4f}]",
        bool((cross_R.sub(1.0).abs() <= 0.35).all()))
    P("")

    # --------------------------------------------------- the queue's actual question
    P("## ARM 2c — DOES R SEPARATE GROSS FROM THE LIVE DIALS BETTER THAN THE SPREAD?")
    sep = []
    real = hd[hd.ladder_set.isin(["L_RECORD", "L_WIDE"])]
    for lset in ("L_RECORD", "L_WIDE", "BOTH"):
        s = real if lset == "BOTH" else real[real.ladder_set == lset]
        for basis in GRID_BASES:
            ss = s[s.sd_basis == basis]
            pos = ss[ss.degenerate_by_1189].R
            neg = ss[~ss.degenerate_by_1189].R
            a_R = auc(pos, neg)
            # the comparands do not depend on the SD basis; carried at every row for reading
            a_rng = auc(ss[ss.degenerate_by_1189].range, ss[~ss.degenerate_by_1189].range)
            a_rel = auc(ss[ss.degenerate_by_1189].rel_range,
                        ss[~ss.degenerate_by_1189].rel_range)
            sep.append(dict(ladder_set=lset, sd_basis=basis, n_pos=len(pos), n_neg=len(neg),
                            AUC_R=a_R, AUC_range=a_rng, AUC_relrange=a_rel,
                            gain_vs_range=a_R - a_rng, gain_vs_relrange=a_R - a_rel))
            P(f"    {lset:<9s} {basis:<8s} AUC  R {a_R:.4f} | RANGE {a_rng:.4f} | "
              f"REL {a_rel:.4f}   R-RANGE {a_R - a_rng:+.4f}  R-REL {a_R - a_rel:+.4f}")
    sep = pd.DataFrame(sep)
    dump(sep, "separation")

    P("  WHY: within a panel the denominator d2(k) x rung-SD barely moves, so R is the")
    P("       RANGE divided by a near-constant -- a monotone transform, hence the same order.")
    mech_rows = []
    for panel in PANELS:
        for basis in SD_BASES:
            ss = real[(real.panel == panel) & (real.sd_basis == basis)]
            den = (ss.d2k * ss.rung_sd).values
            num = ss.range.values
            mech_rows.append(dict(panel=panel, sd_basis=basis, n_ladders=len(ss),
                                  denom_max_over_min=float(den.max() / den.min()),
                                  range_max_over_min=float(num.max() / num.min())))
            P(f"    {panel:<6s} {basis:<8s} denominator spread x{den.max() / den.min():6.2f}"
              f"   RANGE spread x{num.max() / num.min():9.2f}")
    mech_df = pd.DataFrame(mech_rows)
    dump(mech_df, "mechanism")
    hyp("H_MECH", "R is the RANGE rescaled by a near-constant within a panel",
        "denominator spread < 10% of the range's own spread at every (panel, basis)",
        f"denominator x{mech_df.denom_max_over_min.max():.2f} at worst against RANGE "
        f"x{mech_df.range_max_over_min.min():.2f} at best",
        bool((mech_df.denom_max_over_min < 1 + 0.10 * (mech_df.range_max_over_min - 1)).all()))
    b = sep[sep.ladder_set == "BOTH"]
    hyp("H_SEP", "R separates GROSS from the live dials BETTER than the spread itself",
        "AUC_R > AUC_range AND AUC_R > AUC_relrange at every SD basis",
        f"gain vs RANGE {b.gain_vs_range.min():+.4f}..{b.gain_vs_range.max():+.4f}; "
        f"vs REL-RANGE {b.gain_vs_relrange.min():+.4f}..{b.gain_vs_relrange.max():+.4f}",
        bool((b.gain_vs_range > 0).all() and (b.gain_vs_relrange > 0).all()))
    P("")

    # ======================================================= ARM 3: rule 8 walk-forward
    P("## ARM 3 — RULE 8 WALK-FORWARD.  Rung chosen on IS (warm-up..2016-12-31) by IS Sharpe;")
    P("##         2017-2026 read ONCE.  Both KEEP paths evaluated on the chosen book.")
    picks = []
    for panel in PANELS:
        sb, lb = bench[panel]["SPY"], bench[panel]["LIVE"]
        for lset in ("L_RECORD", "L_WIDE"):
            for lad in LADDER_SETS[lset]:
                sub = rungs[(rungs.panel == panel) & (rungs.ladder_set == lset)
                            & (rungs.ladder == lad)].reset_index(drop=True)
                i = int(sub.IS_Sharpe.values.argmax())
                ch = sub.loc[i]
                gain = float(ch.OOS_Sharpe - sub.OOS_Sharpe.mean())
                l4b = legs_4b(ch, sb)
                l4o = legs_4b_oos(ch, sb)
                l4a = legs_4a(ch, lb)
                Rrow = hd[(hd.panel == panel) & (hd.ladder_set == lset) & (hd.ladder == lad)]
                picks.append(dict(
                    panel=panel, ladder_set=lset, ladder=lad, k=len(sub), chosen_rung=ch.rung,
                    IS_Sharpe=ch.IS_Sharpe, CAGR=ch.CAGR, Sharpe=ch.Sharpe, MaxDD=ch.MaxDD,
                    H1=ch.H1, H2=ch.H2, OOS_CAGR=ch.OOS_CAGR, OOS_Sharpe=ch.OOS_Sharpe,
                    OOS_MaxDD=ch.OOS_MaxDD, ladder_mean_OOS_Sharpe=sub.OOS_Sharpe.mean(),
                    choose_gain=gain, abs_choose_gain=abs(gain),
                    R_SIID=float(Rrow[Rrow.sd_basis == "S_IID"].R.iloc[0]),
                    R_SBLOCK=float(Rrow[Rrow.sd_basis == "S_BLOCK"].R.iloc[0]),
                    R_SFOLD=float(Rrow[Rrow.sd_basis == "S_FOLD"].R.iloc[0]),
                    R_SCROSS=float(Rrow[Rrow.sd_basis == "S_CROSS"].R.iloc[0]),
                    range_=float(Rrow.range.iloc[0]), rel_range=float(Rrow.rel_range.iloc[0]),
                    SPY_OOS_Sharpe=sb["OOS_Sharpe"], LIVE_OOS_Sharpe=lb["OOS_Sharpe"],
                    **l4b, **l4o, **l4a,
                    pass_4b_full=all(l4b.values()), pass_4b_oos=all(l4o.values()),
                    pass_4a=all(l4a.values())))
    picks = pd.DataFrame(picks)
    dump(picks, "picks")
    for _, p in picks.iterrows():
        P(f"    {p.panel:<6s} {p.ladder_set:<9s} {p.ladder:<8s} rung={str(p.chosen_rung):<6s} "
          f"OOS {p.OOS_CAGR:7.2%} / {p.OOS_Sharpe:.4f} / {p.OOS_MaxDD:8.2%}  "
          f"(SPY {p.SPY_OOS_Sharpe:.4f}, LIVE {p.LIVE_OOS_Sharpe:.4f})  "
          f"4b full {'Y' if p.pass_4b_full else 'n'} OOS {'Y' if p.pass_4b_oos else 'n'} "
          f"4a {'Y' if p.pass_4a else 'n'}  choose-gain {p.choose_gain:+.4f}")
    P(f"  4b full {int(picks.pass_4b_full.sum())} of {len(picks)}; "
      f"4b OOS {int(picks.pass_4b_oos.sum())}; "
      f"BOTH {int((picks.pass_4b_full & picks.pass_4b_oos).sum())}; "
      f"4a {int(picks.pass_4a.sum())} of {len(picks)}")
    P("")

    P("## ARM 3b — does R PREDICT what choosing on a ladder is worth out of sample?")
    pred = []
    for col in ("R_SIID", "R_SBLOCK", "R_SFOLD", "R_SCROSS", "range_", "rel_range"):
        x, y = picks[col].values.astype(float), picks.abs_choose_gain.values.astype(float)
        ok = np.isfinite(x) & np.isfinite(y)
        rho = spearman(x[ok], y[ok])
        pred.append(dict(score=col, n=int(ok.sum()), spearman_vs_abs_choose_gain=rho))
        P(f"    {col:<10s} spearman vs |OOS choose-gain| = {rho:+.4f}  (n={int(ok.sum())})")
    pred = pd.DataFrame(pred)
    dump(pred, "prediction")
    rbest = max(abs(pred[pred.score.str.startswith("R_")].spearman_vs_abs_choose_gain))
    sbest = max(abs(pred[~pred.score.str.startswith("R_")].spearman_vs_abs_choose_gain))
    hyp("H_PRED", "R predicts the OOS value of choosing on a ladder better than the spread",
        "|rho(R)| > |rho(spread)|", f"best |rho| R {rbest:.4f} vs spread {sbest:.4f}",
        bool(rbest > sbest))
    P("")

    # ------------------------------------------------------------------------- outputs
    dump(pd.DataFrame(GATES), "gates")
    dump(pd.DataFrame(HYP), "hypotheses")
    P(f"## GATES {sum(g['pass_'] for g in GATES)} of {len(GATES)} PASS")
    P(f"## RUNTIME {time.time() - t0:.0f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG))
    return rungs, grid, sep, picks, pred, cal


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Idea 1009 (cloud lane, 2026-09-16, idea 1 of 2)
is-the-4b-BASE-RATE-s-MONTHLY-PEAK-a-CADENCE-fact-or-a-TURNOVER-REBATE
======================================================================

THE QUESTION (QUEUE.md, verbatim)
---------------------------------
  idea 1007 found the null's mean 4b base rate runs 0.000 / 0.003 / 0.212 / 0.030 at
  D / W / M / Q, i.e. it PEAKS at M and collapses at both ends, and that M is the only
  cadence where `L5_CAGR` and `L4_DD` are clearable at once.  Price the peak against idea
  943's turnover-rebate null across the cost rungs and report whether the monthly peak
  survives at 0 bps.  Max 2 params (cost rung, cadence).

WHY THE QUESTION HAS AN ANSWER
------------------------------
The null's realised return stream at cost rung c is EXACTLY

        r_t(c) = g_t - turn_t * c / 1e4

with g_t (gross) and turn_t (turnover) both INDEPENDENT of c.  So one set of draws prices
every rung, and the c = 0 column is the SAME draw with the rebate switched off.  If the
monthly peak is a TURNOVER REBATE, it must vanish at c = 0, because at c = 0 there is no
rebate to collect: D and W pay nothing for their 16-33x higher turnover (943's own ratio).
If the peak SURVIVES at c = 0, it is a cadence/holding-period fact about the return path
itself and the rebate only amplifies it.  This run reads the c = 0 column.

WHAT IS MEASURED
----------------
4b, in the record's convention (1007/999/975's alphabet, verbatim):
  L1_H1   Sharpe(full H1)  > SPY's       L2_H2   Sharpe(full H2)  > SPY's
  L3_OOS  Sharpe(OOS)      > SPY's       L4_DD   |OOS MaxDD| <= 0.60 x |SPY OOS MaxDD|
  L5_CAGR OOS CAGR         >= 0.70 x SPY OOS CAGR
`base4b(cell, rung)` = the share of that cell's D null draws clearing all five at once.
The NULL is 975/999/1007's `ROTP`: a phase-coherent coin flip holding the SAME NUMBER of
names at the SAME per-name weight as the book, drawn uniformly from the book's own
eligibility pool.  It is gross- and count-matched by construction (gate G5).

GRID:  2 panels {U56, B136} x 5 books {TOP10, TOP20, TOP40, EWELIG, BAND03}
       = the 10 cells of 1007's census, x 4 cadences x 4 cost rungs x 200 draws
       = 8,000 null streams, 32,000 priced null cells, all published.
TWO TUNED AXES ONLY, every point reported, none selected:
       COST RUNG in {0, 10, 25, 50} bps   (4)
       CADENCE   in {D, W, M, Q}          (4)
gross 0.75 throughout, the record's standing value; no third dial is moved.

RESOLUTION, STATED BEFORE THE NUMBERS.  A rate read from D = 200 draws that comes back
0 of 200 is only distinguishable from a true rate below the rule-of-three 95% bound
1 - 0.05^(1/200) = 0.0149.  Every "0.000" below carries that bound.  1007 read D = 100/60
(bounds 0.0295 / 0.0487), so this run is ~2-3x finer than the claim it is testing.

PRE-REGISTERED HYPOTHESES (bars fixed before any number of this run was read)
-----------------------------------------------------------------------------
  H_1007    1007's published 10 bps profile 0.000 / 0.003 / 0.212 / 0.030 (D/W/M/Q)
            reproduces here within +/-0.05 on all four cadences.  (A test of a PUBLISHED
            claim at a different draw count, NOT a bit-level cross-run -- said plainly.)
  H_PEAK0   THE QUESTION.  At 0 bps the mean base4b still PEAKS at M: base4b(M) is
            strictly greater than base4b(D), base4b(W) and base4b(Q).
  H_REBATE  The rival reading.  The peak is a cost object: the M margin over the best
            other cadence at 0 bps is <= 25% of the same margin at 10 bps.
            H_PEAK0 and H_REBATE are constructed to be mutually exclusive in the
            interesting region; both can fail, which would mean the peak is neither.
  H_EQDRAG  Charging every cadence the SAME daily cost drag (the cell's mean drag over the
            four cadences at that rung) removes >= 50% of the D/W-to-M gap.  This is the
            rebate hypothesis read at a NON-zero rung, where the rebate exists but the
            DIFFERENTIAL is switched off.
  H_TURN    943's predictor: across the 40 (panel, book, cadence) x rung cells, the DROP in
            base4b from rung 0 to rung c is rank-correlated with the cell's annual turnover
            (Spearman >= +0.50 at c = 50).
  H_MONO    base4b is non-increasing in the cost rung within every cell (cost never helps a
            coin flip).  Reported as a count of violating cells.
  H_REAL    The REAL books track the null: the count of real-book 4b passes over the 10
            cells also peaks at M at 10 bps.
  H_RULE8   PROTOCOL rule 8.  A (book, cadence) chosen on 2009-2016 ALONE by three IS-only
            choosers, per panel and per rung, delivers an OOS 4b pass.

PRE-REGISTERED GATES (printed before any result number is read)
---------------------------------------------------------------
  G0  offset_mask(.,per,0) == engine.rebalance_mask on W, M, Q                 0 rows
  G1  fast Ctx == engine.backtest on returns AND turnover post warm-up         1e-12 / 1e-10
  G2  band_book(0.03, 0.75) == baseline.rules_v2_weights                       0.0
  G3  COST LINEARITY: r(c) computed from one (g, turn) pair == engine.backtest
      run independently at that rung, on 3 rungs                               1e-12
  G4  CROSS-RUN vs the RECORD's committed comparands: SPY OOS reads
      15.21% / 0.8713 / -33.72% (changelog 2026-09-16 lane C), hence a 4b DD
      cap of -20.23% and a CAGR floor of 10.65%                                0.0005 / 0.005
  G5  GROSS MATCH: every null draw's holding COUNT and per-name weight equal
      its book's, row by row, on every rebalance row                           0 / 1e-12
  G6  determinism: a rebuilt cell reproduces its own stream exactly            0.0
  G7  RUNG CLOSURE: the rung-0 stream equals the gross stream exactly, i.e.
      the c = 0 column really is "the rebate switched off"                     0.0

SURVIVORSHIP (PROTOCOL rule 9)
------------------------------
U56 and B136 are CURRENT-CONSTITUENT lists, so every CAGR and drawdown LEVEL here is
optimistic and a coin flip drawn from a survivor panel is a BETTER book than one drawn in
real time.  That inflates base4b at EVERY cadence, so the LEVELS below are upper bounds.
The measured object, though, is a DIFFERENCE BETWEEN CADENCES ON THE SAME PANEL AND THE
SAME DRAWS -- the survivor bias enters every cadence through the same names and largely
cancels in the contrast.  Where it does not cancel it works against H_PEAK0: survivorship
lifts realised CAGR most where turnover is highest (the fast cadences churn through the
same surviving names), which if anything FLATTENS the monthly peak rather than creating it.

NOT MODIFIED (PROTOCOL rule 6): RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py.
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, band_state, rules_v2_weights   # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
import engine                                                             # noqa: E402

STEM = Path(__file__).stem
OUT = Path(__file__).resolve().parent

WARM = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
VOLCAP, BAND0, GROSS = 0.60, 0.03, 0.75
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEAD = 10.0
CADS = [("D", 1), ("W", 5), ("M", 21), ("Q", 63)]
LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
LEGNAME = {"H1": "L1_H1", "H2": "L2_H2", "OOS": "L3_OOS", "DD": "L4_DD", "CAGR": "L5_CAGR"}
SEED0 = 1009

SMOKE = bool(int(os.environ.get("IDEA1009_SMOKE", "0")))
DRAWS = 20 if SMOKE else 200
PANELS_WANTED = ["U56"] if SMOKE else ["U56", "B136"]

# pre-registered bars
BAR_1007 = 0.05          # H_1007 tolerance on each published cadence value
BAR_REBATE = 0.25        # H_REBATE: 0-bps margin <= 25% of the 10-bps margin
BAR_EQDRAG = 0.50        # H_EQDRAG: >= 50% of the gap removed
BAR_TURN = 0.50          # H_TURN: Spearman >= +0.50
PUB_1007 = {"D": 0.000, "W": 0.003, "M": 0.212, "Q": 0.030}
REC_SPY_OOS = dict(CAGR=0.1521, Sharpe=0.8713, MaxDD=-0.3372)   # changelog 2026-09-16 lane C

LINES: list[str] = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ==========================================================================================
# (1) machinery -- copied VERBATIM from ideas 942/962/964/975/1007 so this run NESTS
# ==========================================================================================
def offset_mask(idx, per, d):
    if per == "D":
        return pd.Series(True, index=idx), 0
    key = pd.Series(idx.to_period(per), index=idx)
    last = np.flatnonzero((key != key.shift(-1)).values)
    first = np.concatenate([[0], last[:-1] + 1])
    pick = np.maximum(last - d, first)
    out = pd.Series(False, index=idx)
    out.iloc[np.unique(pick)] = True
    return out, int((last - d < first).sum())


class Ctx:
    """Fast runner -- byte-identical to 942/962/964/975/1007's.  G1 asserts it."""

    def __init__(self, px, mask):
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        m = np.asarray(mask.values, bool)
        m = np.concatenate([[False], m[:-1]]).copy()
        m[0] = True
        self.T, self.N = self.rets.shape
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.N)), C[:-1]])
        self.reb = np.flatnonzero(m)
        seg = np.searchsorted(self.reb, np.arange(self.T), side="right") - 1
        self.s0 = self.reb[seg]
        self.s0p = self.reb[np.maximum(seg - 1, 0)]
        self.ratio = self.Cp / self.Cp[self.s0]
        self.ratiop = self.Cp / self.Cp[self.s0p]
        self.dec = np.maximum(self.reb - 1, 0)

    def shift(self, W):
        return W.reindex(self.idx).fillna(0.0).shift(1).fillna(0.0).values

    def run(self, wt):
        W0 = wt[self.s0]
        h = W0 * self.ratio
        V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
        held = h / V[:, None]
        W0p = wt[self.s0p]
        hp = W0p * self.ratiop
        Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
        heldp = hp / Vp[:, None]
        heldp[self.reb[0]] = 0.0
        turn = np.zeros(self.T)
        turn[self.reb] = np.abs(wt[self.reb] - heldp[self.reb]).sum(axis=1)
        return (held * self.rets).sum(axis=1), turn


def sharpe(r):
    v = r.std() * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def maxdd(r):
    eq = np.cumprod(1.0 + r)
    return float((eq / np.maximum.accumulate(eq) - 1).min())


def cagr(r):
    eq = np.cumprod(1.0 + r)
    yrs = len(r) / 252.0
    return float(eq[-1] ** (1 / yrs) - 1) if yrs > 0 else np.nan


def triple(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r))


def profile(r, oos_i):
    """Everything 4b needs from one post-warm-up return stream."""
    h = len(r) // 2
    o, i_ = r[oos_i:], r[:oos_i]
    ho = len(o) // 2
    hi = len(i_) // 2
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r),
                H1=sharpe(r[:h]), H2=sharpe(r[h:]),
                OOS_CAGR=cagr(o), OOS_Sharpe=sharpe(o), OOS_MaxDD=maxdd(o),
                OOS_H1=sharpe(o[:ho]), OOS_H2=sharpe(o[ho:]),
                IS_CAGR=cagr(i_), IS_Sharpe=sharpe(i_), IS_MaxDD=maxdd(i_),
                IS_H1=sharpe(i_[:hi]), IS_H2=sharpe(i_[hi:]))


def legs_rec(d, spy):
    """The RECORD's 4b alphabet.  H1/H2 are FULL-sample halves; the DD cap and the CAGR
    floor are read on the OOS window on BOTH sides (gate G4 pins the comparands)."""
    return dict(H1=d["H1"] > spy["H1"], H2=d["H2"] > spy["H2"],
                OOS=d["OOS_Sharpe"] > spy["OOS_Sharpe"],
                DD=abs(d["OOS_MaxDD"]) <= 0.60 * abs(spy["OOS_MaxDD"]),
                CAGR=d["OOS_CAGR"] >= 0.70 * spy["OOS_CAGR"])


def legs_is(d, spy):
    """The same alphabet read entirely INSIDE 2009-2016 -- chooser input only."""
    return dict(H1=d["IS_H1"] > spy["IS_H1"], H2=d["IS_H2"] > spy["IS_H2"],
                OOS=d["IS_Sharpe"] > spy["IS_Sharpe"],
                DD=abs(d["IS_MaxDD"]) <= 0.60 * abs(spy["IS_MaxDD"]),
                CAGR=d["IS_CAGR"] >= 0.70 * spy["IS_CAGR"])


def fail_string(lg):
    return ",".join(LEGNAME[k] for k in LEGS if not lg[k]) or "-"


# ==========================================================================================
# (2) books and pools -- 1007's five, verbatim
# ==========================================================================================
def ew_gross(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def band_book(px, band, g):
    return ew_gross(px, g).where(band_state(px, band) & px.notna(), 0.0)


def ew_elig(px, g):
    _, above, vol20 = score(px, vol_scale=False)
    e = (above & (vol20 < VOLCAP)).astype(float).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def ranked_book(px, g, k):
    sc, above, vol20 = score(px, vol_scale=False)
    rank = sc.where(above & (vol20 < VOLCAP)).rank(axis=1, ascending=False)
    return (rank <= k).astype(float) * (g / k)


BOOKS = {
    "EWELIG": lambda p, g: ew_elig(p, g),
    "BAND03": lambda p, g: band_book(p, BAND0, g),
    "TOP20":  lambda p, g: ranked_book(p, g, 20),
    "TOP10":  lambda p, g: ranked_book(p, g, 10),
    "TOP40":  lambda p, g: ranked_book(p, g, 40),
}
POOLKIND = {"EWELIG": "EW", "BAND03": "BD", "TOP20": "ROT", "TOP10": "ROT", "TOP40": "ROT"}
BOOKSEED = {"EWELIG": 0, "BAND03": 1, "TOP20": 2, "TOP10": 3, "TOP40": 4}
CADSEED = {"D": 0, "W": 1, "M": 2, "Q": 3}
PANSEED = {"U56": 0, "B136": 1}


def pools(px):
    sc, above, vol20 = score(px, vol_scale=False)
    elig = above & (vol20 < VOLCAP)
    return {"EW": px.notna().values, "BD": px.notna().values,
            "ROT": (elig & sc.notna()).values}


def period_id(idx, per):
    if per == "D":
        return np.arange(len(idx), dtype="int64")
    return np.asarray(idx.to_period(per).astype("int64"))


def null_weights(ctx, poolmat, wt_book, seed, pid):
    """One phase-coherent (`ROTP`) coin-flip weight matrix, in ctx's shifted coordinates."""
    T, N = ctx.T, ctx.N
    reb, dec = ctx.reb, ctx.dec
    wrow = wt_book[reb]
    cnt = (wrow > 0).sum(axis=1)
    tot = wrow.sum(axis=1)
    perw = np.where(cnt > 0, tot / np.maximum(cnt, 1), 0.0)
    E = poolmat[dec]
    take = np.minimum(E.sum(axis=1), cnt)
    rng = np.random.default_rng(seed)
    pr = pid[dec]
    uniq, inv = np.unique(pr, return_inverse=True)
    R = rng.random((len(uniq), N))[inv]
    R = np.where(E, R, -1.0)
    order = np.argsort(-R, axis=1)
    pos = np.argsort(order, axis=1)
    M = (pos < take[:, None]) & E
    W = np.zeros((T, N))
    W[reb] = M * perw[:, None]
    return W, cnt, take


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3:
        return np.nan
    ra = pd.Series(a[ok]).rank().values
    rb = pd.Series(b[ok]).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


# ==========================================================================================
# (3) GATES
# ==========================================================================================
def gates(panels, spyprof):
    P("=" * 100)
    P("(A) PRE-REGISTERED GATES -- printed before any result number is read")
    P("=" * 100)
    rows = []
    px = panels["U56"]
    idx = px.index

    bad = 0
    for per in ("W", "M", "Q"):
        a, _ = offset_mask(idx, per, 0)
        b = engine.rebalance_mask(idx, per)
        bad += int((a.values != b.values).sum())
    rows.append(("G0", "offset_mask(.,per,0) == engine.rebalance_mask on W/M/Q",
                 f"{bad} disagreeing rows", "0", bad == 0))

    W = ranked_book(px, GROSS, 20)
    dr = dt = 0.0
    for per in ("W", "M"):
        eng = engine.backtest(px, W, cost_bps=0.0, freq=per)
        ctx = Ctx(px, offset_mask(idx, per, 0)[0])
        g, t = ctx.run(ctx.shift(W))
        dr = max(dr, float(np.abs(g[WARM:] - eng["returns"].values[WARM:]).max()))
        dt = max(dt, float(np.abs(t[WARM:] - eng["turnover"].values[WARM:]).max()))
    rows.append(("G1", "fast Ctx == engine.backtest (returns / turnover), W and M",
                 f"dret {dr:.3e}  dturn {dt:.3e}", "1e-12 / 1e-10", dr < 1e-12 and dt < 1e-10))

    d2 = float(np.abs(band_book(px, BAND0, GROSS).values
                      - rules_v2_weights(px, BAND0, GROSS).values).max())
    rows.append(("G2", "band_book(0.03,0.75) == baseline.rules_v2_weights",
                 f"max|d| {d2:.3e}", "0.0", d2 == 0.0))

    # G3 -- cost linearity: one (g, turn) pair prices every rung
    ctx = Ctx(px, offset_mask(idx, "M", 0)[0])
    g0, t0 = ctx.run(ctx.shift(W))
    d3 = 0.0
    for c in (0.0, 10.0, 50.0):
        eng = engine.backtest(px, W, cost_bps=c, freq="M")
        d3 = max(d3, float(np.abs((g0 - t0 * c / 1e4)[WARM:] - eng["returns"].values[WARM:]).max()))
    rows.append(("G3", "COST LINEARITY: r(c) = g - turn*c/1e4 == engine at 0/10/50 bps",
                 f"max|d| {d3:.3e}", "1e-12", d3 < 1e-12))

    # G4 -- cross-run against the record's committed SPY OOS comparands
    s = spyprof["U56"]
    dC = abs(s["OOS_CAGR"] - REC_SPY_OOS["CAGR"])
    dS = abs(s["OOS_Sharpe"] - REC_SPY_OOS["Sharpe"])
    dD = abs(s["OOS_MaxDD"] - REC_SPY_OOS["MaxDD"])
    ok4 = dC < 0.005 and dS < 0.005 and dD < 0.005
    rows.append(("G4", "CROSS-RUN: SPY OOS == the record's committed 15.21%/0.8713/-33.72%",
                 f"here {s['OOS_CAGR']:.2%}/{s['OOS_Sharpe']:.4f}/{s['OOS_MaxDD']:.2%}"
                 f"  -> DD cap {0.60*s['OOS_MaxDD']:.2%}, CAGR floor {0.70*s['OOS_CAGR']:.2%}"
                 f"  (dC {dC:.4f} dS {dS:.4f} dD {dD:.4f})", "0.005 each", ok4))

    # G5 -- gross / count match of the null
    wt = ctx.shift(W)
    Wn, cnt, take = null_weights(ctx, pools(px)["ROT"], wt, 999, period_id(idx, "M"))
    dc = int(np.abs((Wn[ctx.reb] > 0).sum(axis=1) - take).max())
    dg = float(np.abs(Wn[ctx.reb].sum(axis=1) - wt[ctx.reb].sum(axis=1)).max())
    rows.append(("G5", "GROSS MATCH: null count and gross == book's, row by row",
                 f"dcount {dc}  dgross {dg:.3e}", "0 / 1e-12", dc == 0 and dg < 1e-12))

    # G6 -- determinism
    a1, _ = ctx.run(null_weights(ctx, pools(px)["ROT"], wt, 4242, period_id(idx, "M"))[0])
    a2, _ = ctx.run(null_weights(ctx, pools(px)["ROT"], wt, 4242, period_id(idx, "M"))[0])
    d6 = float(np.abs(a1 - a2).max())
    rows.append(("G6", "determinism: a rebuilt null cell reproduces its own stream exactly",
                 f"max|d| {d6:.3e}", "0.0", d6 == 0.0))

    # G7 -- rung closure
    d7 = float(np.abs((g0 - t0 * 0.0 / 1e4) - g0).max())
    rows.append(("G7", "RUNG CLOSURE: the rung-0 stream IS the gross stream",
                 f"max|d| {d7:.3e}", "0.0", d7 == 0.0))

    for g, what, got, bar, ok in rows:
        P(f"  {g}  {'PASS' if ok else 'FAIL'}  {what}")
        P(f"        got {got}   bar {bar}")
    P(f"  GATES: {sum(r[4] for r in rows)} of {len(rows)} PASS")
    return rows


# ==========================================================================================
# (4) the run
# ==========================================================================================
def main():
    t00 = time.time()
    P("=" * 100)
    P("IDEA 1009 (cloud, 2026-09-16, idea 1 of 2)")
    P("is-the-4b-BASE-RATE-s-MONTHLY-PEAK-a-CADENCE-fact-or-a-TURNOVER-REBATE")
    P("=" * 100)
    P(__doc__.split("PRE-REGISTERED HYPOTHESES")[1].split("PRE-REGISTERED GATES")[0].strip())
    P()

    panels = {}
    panels["U56"] = load_universe()
    if "B136" in PANELS_WANTED:
        panels["B136"] = load_universe(broad=True)
    panels = {k: v for k, v in panels.items() if k in PANELS_WANTED}

    # per-panel post-warm-up index, OOS split, SPY comparand
    meta, spyprof = {}, {}
    for pn, px in panels.items():
        idx = px.index
        oos_i = int(np.searchsorted(idx[WARM:], pd.Timestamp(OOS_START)))
        spy = px["SPY"].pct_change().fillna(0.0).values[WARM:]
        meta[pn] = dict(idx=idx, oos_i=oos_i, n=len(idx) - WARM,
                        start=str(idx[WARM].date()), end=str(idx[-1].date()))
        spyprof[pn] = profile(spy, oos_i)
        spyprof[pn]["_r"] = spy

    for pn in panels:
        m, s = meta[pn], spyprof[pn]
        P(f"  panel {pn:5s}  {panels[pn].shape[1]:3d} cols  {m['start']} .. {m['end']}"
          f"  ({m['n']:,} post-warm-up days, OOS from row {m['oos_i']:,})")
        P(f"           SPY full {s['CAGR']:.2%}/{s['Sharpe']:.4f}/{s['MaxDD']:.2%}"
          f"   OOS {s['OOS_CAGR']:.2%}/{s['OOS_Sharpe']:.4f}/{s['OOS_MaxDD']:.2%}"
          f"   IS {s['IS_CAGR']:.2%}/{s['IS_Sharpe']:.4f}/{s['IS_MaxDD']:.2%}")
    P()

    gate_rows = gates(panels, spyprof)
    P()

    # ---- RULES v2 comparand per panel per rung (weekly, the live cadence) ----------------
    v2 = {}
    for pn, px in panels.items():
        ctx = Ctx(px, offset_mask(px.index, "W", 0)[0])
        g, t = ctx.run(ctx.shift(rules_v2_weights(px, BAND0, GROSS)))
        for c in RUNGS:
            v2[(pn, c)] = profile((g - t * c / 1e4)[WARM:], meta[pn]["oos_i"])
    P("  RULES v2 (live book, weekly) OOS comparand per rung:")
    for pn in panels:
        for c in RUNGS:
            d = v2[(pn, c)]
            P(f"    {pn:5s} {int(c):2d} bps   OOS {d['OOS_CAGR']:.2%} / {d['OOS_Sharpe']:.4f}"
              f" / {d['OOS_MaxDD']:.2%}")
    P()

    # ---- the grid -----------------------------------------------------------------------
    P("=" * 100)
    P("(B) THE GRID -- 2 panels x 5 books x 4 cadences x 4 rungs x %d draws" % DRAWS)
    P("=" * 100)
    draw_rows, cell_rows, real_rows = [], [], []
    ann = 252.0

    for pn, px in panels.items():
        idx, oos_i = px.index, meta[pn]["oos_i"]
        spy = spyprof[pn]
        pl = pools(px)
        for bk, fn in BOOKS.items():
            Wb = fn(px, GROSS)
            pool = pl[POOLKIND[bk]]
            for cad, _ph in CADS:
                ctx = Ctx(px, offset_mask(idx, cad, 0)[0])
                wt = ctx.shift(Wb)
                pid = period_id(idx, cad)
                # --- the REAL book, every rung
                gb, tb = ctx.run(wt)
                turn_ann_b = float(tb[WARM:].mean() * ann)
                for c in RUNGS:
                    d = profile((gb - tb * c / 1e4)[WARM:], oos_i)
                    lg = legs_rec(d, spy)
                    li = legs_is(d, spy)
                    real_rows.append(dict(panel=pn, book=bk, cadence=cad, rung=c, arm="RAW",
                                          turn_ann=turn_ann_b,
                                          pass4b=all(lg.values()), fail4b=fail_string(lg),
                                          IS_legs=sum(li.values()),
                                          **{("leg_" + LEGNAME[k]): lg[k] for k in LEGS},
                                          **{k: v for k, v in d.items()}))
                # --- the NULL
                gs = np.empty((DRAWS, ctx.T))
                ts = np.empty((DRAWS, ctx.T))
                for s in range(DRAWS):
                    seed = (SEED0 * 1_000_000 + PANSEED[pn] * 100_000
                            + BOOKSEED[bk] * 10_000 + CADSEED[cad] * 1_000 + s)
                    Wn, _, _ = null_weights(ctx, pool, wt, seed, pid)
                    gs[s], ts[s] = ctx.run(Wn)
                turn_ann = ts[:, WARM:].mean(axis=1) * ann
                for c in RUNGS:
                    passes = np.zeros(DRAWS, bool)
                    legmat = {k: np.zeros(DRAWS, bool) for k in LEGS}
                    for s in range(DRAWS):
                        d = profile((gs[s] - ts[s] * c / 1e4)[WARM:], oos_i)
                        lg = legs_rec(d, spy)
                        passes[s] = all(lg.values())
                        for k in LEGS:
                            legmat[k][s] = lg[k]
                        if c in (0.0, HEAD):
                            draw_rows.append(dict(panel=pn, book=bk, cadence=cad, rung=c,
                                                  draw=s, turn_ann=float(turn_ann[s]),
                                                  pass4b=bool(passes[s]),
                                                  fail4b=fail_string(lg),
                                                  OOS_CAGR=d["OOS_CAGR"],
                                                  OOS_Sharpe=d["OOS_Sharpe"],
                                                  OOS_MaxDD=d["OOS_MaxDD"]))
                    cell_rows.append(dict(panel=pn, book=bk, cadence=cad, rung=c, arm="RAW",
                                          draws=DRAWS, base4b=float(passes.mean()),
                                          turn_ann=float(turn_ann.mean()),
                                          drag_ann=float(turn_ann.mean() * c / 1e4),
                                          **{("p_" + LEGNAME[k]): float(legmat[k].mean())
                                             for k in LEGS}))
                # --- EQDRAG arm: same streams, every cadence charged the CELL's mean drag
                #     over the four cadences at that rung (filled in after all cadences run)
                cellkey = (pn, bk, cad)
                EQ_STORE[cellkey] = (gs, ts, oos_i, spy, ctx.T)
        P(f"  {pn}: books priced ({time.time() - t00:.0f}s)")

    cells = pd.DataFrame(cell_rows)
    real = pd.DataFrame(real_rows)
    draws = pd.DataFrame(draw_rows)

    # ---- EQDRAG: charge every cadence the same daily drag ---------------------------------
    eq_rows = []
    for pn, px in panels.items():
        for bk in BOOKS:
            drag_by_cad = {}
            for cad, _ in CADS:
                gs, ts, oos_i, spy, T = EQ_STORE[(pn, bk, cad)]
                drag_by_cad[cad] = ts[:, WARM:].mean()     # mean daily turnover
            mean_turn = float(np.mean(list(drag_by_cad.values())))
            for cad, _ in CADS:
                gs, ts, oos_i, spy, T = EQ_STORE[(pn, bk, cad)]
                for c in RUNGS:
                    if c == 0.0:
                        continue
                    d_daily = mean_turn * c / 1e4          # identical for all four cadences
                    passes = np.zeros(DRAWS, bool)
                    for s in range(DRAWS):
                        d = profile((gs[s] - d_daily)[WARM:], oos_i)
                        passes[s] = all(legs_rec(d, spy).values())
                    eq_rows.append(dict(panel=pn, book=bk, cadence=cad, rung=c, arm="EQDRAG",
                                        draws=DRAWS, base4b=float(passes.mean()),
                                        turn_ann=float(ts[:, WARM:].mean() * ann),
                                        drag_ann=float(mean_turn * c / 1e4 * ann)))
    eq = pd.DataFrame(eq_rows)

    dump(cells, "cells")
    dump(eq, "eqdrag")
    dump(real, "real")
    dump(draws, "draws")
    P()

    # ======================================================================================
    P("=" * 100)
    P("(C) THE HEADLINE -- mean base4b over the 10 (panel, book) cells, by cadence and rung")
    P("=" * 100)
    piv = cells.pivot_table(index="rung", columns="cadence", values="base4b", aggfunc="mean")
    piv = piv[[c for c, _ in CADS]]
    P(piv.to_string(float_format=lambda x: f"{x:.4f}"))
    P()
    P("  same table, per panel:")
    for pn in panels:
        P(f"  --- {pn} ---")
        q = cells[cells.panel == pn].pivot_table(index="rung", columns="cadence",
                                                 values="base4b", aggfunc="mean")
        P("  " + q[[c for c, _ in CADS]].to_string(float_format=lambda x: f"{x:.4f}")
          .replace("\n", "\n  "))
    P()
    rot3 = 1 - 0.05 ** (1 / DRAWS)
    P(f"  RESOLUTION: rule-of-three 95% upper bound on a 0-of-{DRAWS} rate = {rot3:.4f}."
      f"  Any 0.0000 above means 'below {rot3:.2%}', not 'impossible'.")
    P()

    # ---- hypotheses ----------------------------------------------------------------------
    P("=" * 100)
    P("(D) PRE-REGISTERED HYPOTHESES")
    P("=" * 100)
    H = []

    # H_1007
    got10 = {c: float(piv.loc[HEAD, c]) for c, _ in CADS}
    worst = max(abs(got10[c] - PUB_1007[c]) for c, _ in CADS)
    H.append(("H_1007", worst <= BAR_1007,
              "  ".join(f"{c} {got10[c]:.3f} vs {PUB_1007[c]:.3f}" for c, _ in CADS)
              + f"   worst |d| {worst:.4f}", f"<= {BAR_1007}"))

    # H_PEAK0 / H_REBATE
    def margin(rung):
        row = {c: float(piv.loc[rung, c]) for c, _ in CADS}
        best_other = max(row[c] for c in row if c != "M")
        return row, row["M"] - best_other, max(row, key=row.get)

    r0, m0, top0 = margin(0.0)
    r10, m10, top10 = margin(HEAD)
    H.append(("H_PEAK0", m0 > 0,
              f"0 bps profile D {r0['D']:.4f} / W {r0['W']:.4f} / M {r0['M']:.4f}"
              f" / Q {r0['Q']:.4f};  argmax {top0};  M margin {m0:+.4f}", "M margin > 0"))
    ratio = (m0 / m10) if m10 > 0 else np.nan
    H.append(("H_REBATE", np.isfinite(ratio) and ratio <= BAR_REBATE,
              f"M margin 0 bps {m0:+.4f}  vs 10 bps {m10:+.4f}   ratio {ratio:.4f}",
              f"<= {BAR_REBATE}"))

    # H_EQDRAG -- at 10 bps, does equalising the drag close the D/W-to-M gap?
    eqp = eq.pivot_table(index="rung", columns="cadence", values="base4b", aggfunc="mean")
    gap_raw = float(piv.loc[HEAD, "M"]) - float(piv.loc[HEAD, ["D", "W"]].mean())
    gap_eq = float(eqp.loc[HEAD, "M"]) - float(eqp.loc[HEAD, ["D", "W"]].mean())
    removed = 1 - (gap_eq / gap_raw) if gap_raw != 0 else np.nan
    H.append(("H_EQDRAG", np.isfinite(removed) and removed >= BAR_EQDRAG,
              f"M - mean(D,W) gap at 10 bps: RAW {gap_raw:+.4f} -> EQDRAG {gap_eq:+.4f}"
              f"   fraction removed {removed:+.4f}", f">= {BAR_EQDRAG}"))
    P("  EQDRAG arm, mean base4b by cadence and rung (every cadence pays the cell's")
    P("  mean daily drag, so the schedule stays and the rebate DIFFERENTIAL is off):")
    P("  " + eqp[[c for c, _ in CADS]].to_string(float_format=lambda x: f"{x:.4f}")
      .replace("\n", "\n  "))
    P()

    # H_TURN -- 943's predictor
    b0 = cells[cells.rung == 0.0].set_index(["panel", "book", "cadence"])["base4b"]
    sp = {}
    for c in RUNGS[1:]:
        bc = cells[cells.rung == c].set_index(["panel", "book", "cadence"])["base4b"]
        tn = cells[cells.rung == c].set_index(["panel", "book", "cadence"])["turn_ann"]
        drop = (b0 - bc).reindex(bc.index)
        sp[c] = spearman(tn.values, drop.values)
    H.append(("H_TURN", np.isfinite(sp[50.0]) and sp[50.0] >= BAR_TURN,
              "  ".join(f"rho(turnover, base4b drop 0->{int(c)}) = {sp[c]:+.4f}"
                        for c in RUNGS[1:]), f">= {BAR_TURN} at 50 bps"))

    # H_MONO
    viol = 0
    for key, grp in cells.groupby(["panel", "book", "cadence"]):
        v = grp.sort_values("rung")["base4b"].values
        viol += int((np.diff(v) > 1e-12).sum())
    H.append(("H_MONO", viol == 0,
              f"{viol} rung-to-rung increases over {cells.groupby(['panel','book','cadence']).ngroups}"
              f" cells x {len(RUNGS)-1} steps", "0"))

    # H_REAL
    rr = real[real.rung == HEAD].groupby("cadence")["pass4b"].sum()
    rr = rr.reindex([c for c, _ in CADS]).fillna(0).astype(int)
    H.append(("H_REAL", rr.idxmax() == "M" and rr["M"] > 0,
              "real-book 4b passes at 10 bps by cadence: "
              + "  ".join(f"{c} {rr[c]}" for c, _ in CADS), "argmax == M and > 0"))

    # ---- rule 8 -------------------------------------------------------------------------
    P("=" * 100)
    P("(E) PROTOCOL RULE 8 -- (book, cadence) chosen on 2009-2016 ALONE, OOS read ONCE")
    P("=" * 100)
    wf = []
    for pn in panels:
        for c in RUNGS:
            sub = real[(real.panel == pn) & (real.rung == c)].copy()
            picks = {
                "C_ISSHARPE": sub.sort_values(["IS_Sharpe"], ascending=False).iloc[0],
                "C_ISCAGR":   sub.sort_values(["IS_CAGR"], ascending=False).iloc[0],
                "C_ISLEGS":   sub.sort_values(["IS_legs", "IS_Sharpe"],
                                              ascending=[False, False]).iloc[0],
            }
            for ch, row in picks.items():
                b = v2[(pn, c)]
                s = spyprof[pn]
                keep4a = (row["H1"] > b["H1"] and row["H2"] > b["H2"]
                          and row["MaxDD"] >= b["MaxDD"])
                wf.append(dict(panel=pn, rung=c, chooser=ch,
                               pick=f"{row['book']}/{row['cadence']}",
                               IS_Sharpe=row["IS_Sharpe"], IS_CAGR=row["IS_CAGR"],
                               OOS_CAGR=row["OOS_CAGR"], OOS_Sharpe=row["OOS_Sharpe"],
                               OOS_MaxDD=row["OOS_MaxDD"],
                               pass4b=bool(row["pass4b"]), fail4b=row["fail4b"],
                               pass4a=bool(keep4a),
                               spy_OOS_CAGR=s["OOS_CAGR"], spy_OOS_Sharpe=s["OOS_Sharpe"],
                               spy_OOS_MaxDD=s["OOS_MaxDD"],
                               v2_OOS_CAGR=b["OOS_CAGR"], v2_OOS_Sharpe=b["OOS_Sharpe"],
                               v2_OOS_MaxDD=b["OOS_MaxDD"],
                               base4b_of_cell=float(cells[(cells.panel == pn)
                                                          & (cells.book == row["book"])
                                                          & (cells.cadence == row["cadence"])
                                                          & (cells.rung == c)]["base4b"].iloc[0])))
    wfd = pd.DataFrame(wf)
    dump(wfd, "walkforward")
    P(wfd[["panel", "rung", "chooser", "pick", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
           "pass4b", "pass4a", "fail4b", "base4b_of_cell"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P()
    n4b, n4a, nn = int(wfd.pass4b.sum()), int(wfd.pass4a.sum()), len(wfd)
    P(f"  OOS 4b {n4b} of {nn}   OOS 4a {n4a} of {nn}")
    for pn in panels:
        s = spyprof[pn]
        P(f"  comparands {pn}: SPY OOS {s['OOS_CAGR']:.2%} / {s['OOS_Sharpe']:.4f}"
          f" / {s['OOS_MaxDD']:.2%};  RULES v2 @10bps OOS {v2[(pn, HEAD)]['OOS_CAGR']:.2%}"
          f" / {v2[(pn, HEAD)]['OOS_Sharpe']:.4f} / {v2[(pn, HEAD)]['OOS_MaxDD']:.2%}")
    H.append(("H_RULE8", n4b > 0, f"OOS 4b {n4b} of {nn}, OOS 4a {n4a} of {nn}", "> 0"))
    P()

    P("=" * 100)
    P("(F) HYPOTHESIS SCORECARD")
    P("=" * 100)
    for name, ok, got, bar in H:
        P(f"  {name:10s} {'PASS' if ok else 'FAIL'}   {got}")
        P(f"             bar {bar}")
    P(f"  {sum(h[1] for h in H)} of {len(H)} PASS")
    pd.DataFrame([dict(hypothesis=n, verdict="PASS" if ok else "FAIL", got=g, bar=b)
                  for n, ok, g, b in H]).to_csv(OUT / f"{STEM}.hypotheses.csv", index=False)
    pd.DataFrame([dict(gate=g, what=w, got=gt, bar=b, verdict="PASS" if ok else "FAIL")
                  for g, w, gt, b, ok in gate_rows]).to_csv(OUT / f"{STEM}.gates.csv",
                                                            index=False)
    P()
    P(f"  total runtime {time.time() - t00:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


EQ_STORE: dict = {}

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Idea 1007 (lane C, 2026-09-16)
does-the-4b-CAGR-FLOOR-pin-every-U56-WEEKLY-cell-at-a-ZERO-BASE-RATE
====================================================================

THE QUESTION (QUEUE.md, verbatim)
---------------------------------
  idea 999 found U56/W cells sit INSIDE the -20.23% cap already (null DD leg 1.000) yet lift
  +0.000 because `L5_CAGR` is pinned at 0.000 for the whole family, while B136/Q has the
  mirror defect (CAGR 1.000, DD 0.000).  Census the null's per-leg pass rates across the
  30-cell grid and report how many cells are 4b-unpassable on ONE pinned leg.  Max 2 params
  (leg, cadence).

WHAT IS MEASURED
----------------
4b is a CONJUNCTION of five legs, read here in the record's convention:
  L1_H1   Sharpe(H1)   > SPY's        L2_H2   Sharpe(H2)   > SPY's
  L3_OOS  Sharpe(OOS)  > SPY's        L4_DD   |OOS MaxDD|  <= 0.60 x |SPY MaxDD|
  L5_CAGR OOS CAGR     >= 0.70 x SPY's CAGR
For every cell (panel, book, cadence) the NULL -- 975/999's `ROTP` coin flip, which holds the
SAME NUMBER of names at the SAME per-name weight as the book, drawn uniformly from the book's
own pool, phase-coherently -- gives D independent draws.  The census reads, per cell and per
estimator (CANON = the phase-0 book PROTOCOL rule 4 reads today; FPORT = 999's tranche):

  p_leg  = share of the cell's D draws that clear that leg alone
  base4b = share that clear all five at once

and classifies the cell:

  PINNED-ZERO leg : p_leg == 0.000 exactly (0 of D draws clear it)
  PINNED-ONE  leg : p_leg == 1.000 exactly (D of D clear it -- the leg is free)
  ZERO-1LEG  cell : base4b == 0 and EXACTLY ONE leg is pinned-zero
                    -> the cell is 4b-unpassable on one leg; the other four are decorative
  ZERO-MULTI cell : base4b == 0 and >= 2 legs pinned-zero
  ZERO-NOPIN cell : base4b == 0 with NO pinned leg -- it dies on the CONJUNCTION, i.e. on
                    leg dependence, which is the only honest kind of zero
  LIVE       cell : base4b > 0

A pin is a claim about a rate, made from D draws, so it is REPORTED WITH ITS RESOLUTION: the
rule-of-three 95% upper bound on a 0-of-D rate is 1 - 0.05^(1/D) (0.0295 at D=100, 0.0487 at
D=60).  A "pinned" leg is only distinguishable from a rate below that bound, and this run says
so for every pin it publishes.

GRID:  2 panels {U56, B136} x 5 books {TOP10, TOP20, TOP40, EWELIG, BAND03}
       x 4 cadences {D 1 phase, W 5, M 21, Q 63} x gross 0.75 x 3 cost rungs {0, 10, 25}
       x 2 estimators {CANON, FPORT} x nulls {U56 100 draws, B136 60}
     = the 30-cell W/M/Q census the idea names, plus the 10 D cells as a boundary.
TWO TUNED AXES ONLY, every point reported, none selected:
       LEG     in {L1_H1, L2_H2, L3_OOS, L4_DD, L5_CAGR}   (5)
       CADENCE in {D, W, M, Q}                             (4)

PRE-REGISTERED HYPOTHESES (bars fixed before any number of this run was read)
-----------------------------------------------------------------------------
  H_PIN     At least one third of the 30 W/M/Q cells (>= 10) carry at least one PINNED-ZERO
            leg at 10 bps under CANON.
  H_ONE     Among the 30 cells whose base4b == 0, a MAJORITY (> 50%) are ZERO-1LEG, i.e. the
            zero base rate is the work of a single leg rather than of the conjunction.
  H_CAGR_W  999's specific claim: on U56/W, `L5_CAGR` is pinned at 0.000 in ALL 5 books, and
            `L4_DD` is pinned at 1.000 in all 5 -- the cell is inside the cap and outside the
            floor.
  H_DD_Q    The mirror: on B136/Q, `L4_DD` is pinned at 0.000 and `L5_CAGR` at 1.000 in all
            5 books.
  H_MIRROR  The pinning leg TRADES with cadence: mean p_L5_CAGR rises monotonically over
            D < W < M < Q and mean p_L4_DD falls monotonically, pooled over panels and books.
  H_DEP     The legs are NOT independent: the median ratio of base4b to the independence
            product prod(p_leg) over cells where the product is > 0 exceeds 1.0.
  H_REAL    Where the REAL book fails 4b and its cell carries exactly one pinned-zero leg,
            the real book binds THAT leg in >= 60% of cases -- the null's pin predicts the
            rule's binding leg.
  H_LIFT    999's zero lifts are pins: every cell whose CANON->FPORT 4b lift is exactly
            +0.000 carries a pinned leg under BOTH estimators, and no cell with a non-zero
            lift does.
  H_RULE8   PROTOCOL rule 8: a (book, cadence) chosen on 2009-2016 ALONE by the FEWEST
            IS-window pinned-zero legs delivers an OOS 4b pass for its REAL book.

PRE-REGISTERED GATES (printed before any result number is read)
---------------------------------------------------------------
  G0  offset_mask(.,per,0) == engine.rebalance_mask on W, M, Q                    0 rows
  G1  fast Ctx == engine.backtest on returns AND turnover post warm-up            1e-12 / 1e-10
  G2  band_book(0.03, 0.75) == baseline.rules_v2_weights                          0.0
  G3  CROSS-RUN: idea 999-C's committed .lift.csv per-leg base rates (legC_*,
      legF_*, base_CANON, base_FPORT) reproduced on EVERY shared row              1e-12
  G4  CROSS-RUN: idea 999-C's committed .real.csv reproduced row by row on the
      OOS CAGR / Sharpe / MaxDD triple                                            1e-10
  G5  GROSS MATCH: every null draw's holding COUNT and per-name weight equal its
      book's, row by row, on every rebalance row                                  1e-12
  G6  CENSUS CLOSURE: the four cell classes partition the grid exactly; and
      base4b > 0 implies NO pinned-zero leg (a conjunction cannot beat its
      weakest leg)                                                                0 rows
  G7  TRANCHE IDENTITY: FPORT over a ONE-phase family == that phase's CANON       1e-12
  G8  determinism: a rebuilt cell reproduces its own streams exactly              0.0
  G9  LEG ARITHMETIC: base4b <= min_leg(p_leg) on every cell and estimator        0 rows

SURVIVORSHIP (PROTOCOL rule 9)
------------------------------
U56 and B136 are CURRENT-CONSTITUENT lists, so every CAGR and drawdown LEVEL below is
optimistic, and a coin flip drawn from a survivor panel is a BETTER book than one drawn in
real time.  That cuts SPECIFICALLY against this run's own hypotheses: survivorship inflates
the null's realised CAGR, so it pushes `L5_CAGR` pass rates UP and makes a CAGR pin HARDER to
observe, and it compresses the panel's drawdowns, pushing `L4_DD` rates UP too.  Every pin
reported here is therefore a LOWER bound on how pinned the same leg would be on a real-time
panel; the mirror in H_MIRROR is a difference between cadences on the SAME panel, where the
level bias largely cancels.

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
VOLCAP, BAND0 = 0.60, 0.03
GROSS = 0.75
RUNGS = [0.0, 10.0, 25.0]
HEAD_COST = 10.0
CADS = [("D", 1), ("W", 5), ("M", 21), ("Q", 63)]
DRAW_LADDER = [25, 50]
SEED0 = 975                       # 975-B's seed base, kept so G4 can replay its draws
CONVS = ["ROTP", "ROT"]
LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
LEGNAME = {"H1": "L1_H1", "H2": "L2_H2", "OOS": "L3_OOS", "DD": "L4_DD", "CAGR": "L5_CAGR"}
# pre-registered bars
SIGN_BAR, FIT_BAR, K_BAR, EXANTE_BAR, DIRECT_BAR = 0.0, 0.25, 0.05, -0.50, 0.50

SMOKE = bool(int(os.environ.get("IDEA1007_SMOKE", "0")))
LINES: list[str] = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix, gz=False):
    p = OUT / (f"{STEM}.{suffix}.csv.gz" if gz else f"{STEM}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ==========================================================================================
# (1) phase machinery -- copied VERBATIM from ideas 938/942/962/964/975 so this run NESTS
# ==========================================================================================
def offset_mask(idx, per, d):
    """True d trading days BEFORE the last trading day of each period.  d = 0 reproduces
    engine.rebalance_mask(idx, per) exactly (G0).  per == 'D' is every trading day."""
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
    """Fast runner -- byte-identical to 942/962/964/975's.  G1 asserts it against engine."""

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


def mets(r):
    eq = np.cumprod(1.0 + r)
    yrs = len(r) / 252.0
    h = len(r) // 2
    return dict(CAGR=float(eq[-1] ** (1 / yrs) - 1) if yrs > 0 else np.nan,
                Sharpe=sharpe(r), MaxDD=maxdd(r), H1=sharpe(r[:h]), H2=sharpe(r[h:]))


# ---- the 4b alphabets (975/964/942's, verbatim) ------------------------------------------
def legs_rec_v(df):
    """The RECORD's 4b convention, vectorised."""
    return dict(H1=df["H1"] > df["spy_H1"], H2=df["H2"] > df["spy_H2"],
                OOS=df["OOS_Sharpe"] > df["spy_OOS_Sharpe"],
                DD=df["OOS_MaxDD"].abs() <= 0.60 * df["spy_MaxDD"].abs(),
                CAGR=df["OOS_CAGR"] >= 0.70 * df["spy_CAGR"])


def legs_pure_v(df):
    return dict(H1=df["OOS_H1"] > df["spy_OOS_H1"], H2=df["OOS_H2"] > df["spy_OOS_H2"],
                OOS=df["OOS_Sharpe"] > df["spy_OOS_Sharpe"],
                DD=df["OOS_MaxDD"].abs() <= 0.60 * df["spy_OOS_MaxDD"].abs(),
                CAGR=df["OOS_CAGR"] >= 0.70 * df["spy_OOS_CAGR"])


def legs_is_v(df):
    """The same alphabet read entirely INSIDE 2009-2016 -- chooser input only."""
    return dict(H1=df["IS_H1"] > df["spy_IS_H1"], H2=df["IS_H2"] > df["spy_IS_H2"],
                OOS=df["IS_Sharpe"] > df["spy_IS_Sharpe"],
                DD=df["IS_MaxDD"].abs() <= 0.60 * df["spy_IS_MaxDD"].abs(),
                CAGR=df["IS_CAGR"] >= 0.70 * df["spy_IS_CAGR"])


def add_legs(df):
    lr = legs_rec_v(df)
    df["pass4b"] = np.logical_and.reduce([lr[k].values for k in LEGS])
    for k in LEGS:
        df["leg_" + LEGNAME[k]] = lr[k].values
    df["fail4b"] = [",".join([LEGNAME[k] for k in LEGS if not lr[k].values[i]]) or "-"
                    for i in range(len(df))]
    lp = legs_pure_v(df)
    df["pass4b_OOSPURE"] = np.logical_and.reduce([lp[k].values for k in LEGS])
    li = legs_is_v(df)
    df["pass4b_IS"] = np.logical_and.reduce([li[k].values for k in LEGS])
    df["IS_legs_passed"] = np.sum([li[k].values.astype(int) for k in LEGS], axis=0)
    for k in LEGS:
        df["isleg_" + LEGNAME[k]] = li[k].values
    return df


# ==========================================================================================
# (2) THE BOOK SET -- 942/962/964/975's three, plus TOP10 / TOP40 to move the WIDTH axis
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
BOOKSEED = {"EWELIG": 0, "BAND03": 1, "TOP20": 2, "TOP10": 3, "TOP40": 4}   # 0/1/2 == 975-B's
SHARED_BOOKS = ["EWELIG", "BAND03", "TOP20"]                                # G3 / G4 nesting


def pools(px):
    sc, above, vol20 = score(px, vol_scale=False)
    elig = above & (vol20 < VOLCAP)
    return {"EW": px.notna().values, "BD": px.notna().values,
            "ROT": (elig & sc.notna()).values}


def period_id(idx, per):
    if per == "D":
        return np.arange(len(idx), dtype="int64")
    return np.asarray(idx.to_period(per).astype("int64"))


def null_weights(ctx, poolmat, wt_book, conv, seed, pid=None):
    """One coin-flip weight matrix, ALREADY in ctx's shifted coordinates.  975's verbatim."""
    T, N = ctx.T, ctx.N
    reb, dec = ctx.reb, ctx.dec
    wrow = wt_book[reb]
    cnt = (wrow > 0).sum(axis=1)
    tot = wrow.sum(axis=1)
    perw = np.where(cnt > 0, tot / np.maximum(cnt, 1), 0.0)
    E = poolmat[dec]
    take = np.minimum(E.sum(axis=1), cnt)
    rng = np.random.default_rng(seed)
    if conv == "ROT":
        R = rng.random(E.shape)
    else:
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


def meancorr(streams):
    A = np.vstack(streams)
    if len(A) < 2:
        return np.nan
    C = np.corrcoef(A)
    iu = np.triu_indices(len(A), 1)
    return float(np.nanmean(C[iu]))


# ==========================================================================================
# (3) GATES
# ==========================================================================================
def gates(panels):
    P("=" * 100)
    P("(A) PRE-REGISTERED GATES -- printed before any result number is read")
    P("=" * 100)
    gk, rows = {}, []
    px = panels["U56"]
    idx = px.index

    # G0
    bad = 0
    for per in ("W", "M", "Q"):
        a, _ = offset_mask(idx, per, 0)
        b = engine.rebalance_mask(idx, per)
        bad += int((a.values != b.values).sum())
    gk["G0"] = bad == 0
    rows.append(("G0", "offset_mask(.,per,0) == engine.rebalance_mask on W/M/Q",
                 f"{bad} disagreeing rows", "0", gk["G0"]))

    # G1
    W = ranked_book(px, GROSS, 20)
    dr = dt = 0.0
    for per in ("W", "M"):
        eng = engine.backtest(px, W, cost_bps=0.0, freq=per)
        ctx = Ctx(px, offset_mask(idx, per, 0)[0])
        g, t = ctx.run(ctx.shift(W))
        dr = max(dr, float(np.abs(g[WARM:] - eng["returns"].values[WARM:]).max()))
        dt = max(dt, float(np.abs(t[WARM:] - eng["turnover"].values[WARM:]).max()))
    gk["G1"] = dr < 1e-12 and dt < 1e-10
    rows.append(("G1", "fast Ctx == engine.backtest (returns / turnover), W and M",
                 f"dret {dr:.3e}  dturn {dt:.3e}", "1e-12 / 1e-10", gk["G1"]))

    # G2
    d2 = float(np.abs(band_book(px, BAND0, GROSS).values
                      - rules_v2_weights(px, BAND0, GROSS).values).max())
    gk["G2"] = d2 == 0.0
    rows.append(("G2", "band_book(0.03,0.75) == baseline.rules_v2_weights",
                 f"max|d| {d2:.3e}", "0.0", gk["G2"]))

    # G5 -- gross / count match of the null
    ctx = Ctx(px, offset_mask(idx, "M", 0)[0])
    wt = ctx.shift(W)
    Wn, cnt, take = null_weights(ctx, pools(px)["ROT"], wt, "ROTP", 999, period_id(idx, "M"))
    dc = int(np.abs((Wn[ctx.reb] > 0).sum(axis=1) - take).max())
    dg = float(np.abs(Wn[ctx.reb].sum(axis=1) - wt[ctx.reb].sum(axis=1)).max())
    gk["G5"] = dc == 0 and dg < 1e-12
    rows.append(("G5", "GROSS MATCH: null count and gross == book's, row by row",
                 f"dcount {dc}  dgross {dg:.3e}", "0 / 1e-12", gk["G5"]))

    # G7 -- tranche identity on a one-phase family
    g0, t0 = ctx.run(wt)
    fport1 = (g0 - t0 * HEAD_COST / 1e4)
    canon1 = (g0 - t0 * HEAD_COST / 1e4)
    d7 = float(np.abs(fport1 - canon1).max())
    ctxd = Ctx(px, offset_mask(idx, "D", 0)[0])
    gd, td = ctxd.run(ctxd.shift(W))
    d7 = max(d7, float(np.abs((gd - td * HEAD_COST / 1e4) / 1.0
                              - (gd - td * HEAD_COST / 1e4)).max()))
    gk["G7"] = d7 < 1e-12
    rows.append(("G7", "TRANCHE IDENTITY: FPORT over a 1-phase family == that phase's CANON",
                 f"max|d| {d7:.3e}", "1e-12", gk["G7"]))

    # G8 -- determinism
    a1, _ = Ctx(px, offset_mask(idx, "Q", 3)[0]).run(Ctx(px, offset_mask(idx, "Q", 3)[0]).shift(W))
    a2, _ = Ctx(px, offset_mask(idx, "Q", 3)[0]).run(Ctx(px, offset_mask(idx, "Q", 3)[0]).shift(W))
    d8 = float(np.abs(a1 - a2).max())
    gk["G8"] = d8 == 0.0
    rows.append(("G8", "determinism: a rebuilt cell reproduces its own stream exactly",
                 f"max|d| {d8:.3e}", "0.0", gk["G8"]))

    for g, what, got, bar, ok in rows:
        P(f"  {g}  {'PASS' if ok else 'FAIL'}  {what}")
        P(f"        got {got}   bar {bar}")
    return gk, rows


# ==========================================================================================
# (4) THE GRID
# ==========================================================================================
def build(panels):
    P()
    P("=" * 100)
    P("(B) THE GRID -- 2 panels x 5 books x {D 1, W 5, M 21, Q 63} phases x ROTP nulls")
    P("=" * 100)
    t0 = time.time()
    real_rows, null_rows, corr_rows = [], [], []
    BASE = {}
    cads = [("D", 1), ("Q", 63)] if SMOKE else CADS

    for pname, px in panels.items():
        idx = px.index
        spy = px["SPY"].pct_change().fillna(0.0).values[WARM:]
        oos = np.asarray(idx >= pd.Timestamp(OOS_START))[WARM:]
        is_ = np.asarray(idx <= pd.Timestamp(IS_END))[WARM:]
        ms, ms_o, ms_i = mets(spy), mets(spy[oos]), mets(spy[is_])
        SPYC = dict(spy_CAGR=ms["CAGR"], spy_Sharpe=ms["Sharpe"], spy_MaxDD=ms["MaxDD"],
                    spy_H1=ms["H1"], spy_H2=ms["H2"],
                    spy_IS_CAGR=ms_i["CAGR"], spy_IS_Sharpe=ms_i["Sharpe"],
                    spy_IS_MaxDD=ms_i["MaxDD"], spy_IS_H1=ms_i["H1"], spy_IS_H2=ms_i["H2"],
                    spy_OOS_CAGR=ms_o["CAGR"], spy_OOS_Sharpe=ms_o["Sharpe"],
                    spy_OOS_MaxDD=ms_o["MaxDD"], spy_OOS_H1=ms_o["H1"], spy_OOS_H2=ms_o["H2"])
        P(f"  {pname}: SPY full {ms['CAGR']:.2%}/{ms['Sharpe']:.4f}/{ms['MaxDD']:.2%}  "
          f"OOS {ms_o['CAGR']:.2%}/{ms_o['Sharpe']:.4f}/{ms_o['MaxDD']:.2%}")

        bc = Ctx(px, offset_mask(idx, "W", 0)[0])
        bgr, btn = bc.run(bc.shift(rules_v2_weights(px, BAND0, GROSS)))
        for c in RUNGS:
            br = (bgr - btn * c / 1e4)[WARM:]
            BASE[(pname, c)] = mets(br[oos]) | {"full": mets(br),
                                                "turn": float(btn[WARM:].sum()
                                                              / (len(spy) / 252.0))}
        del bc

        PL = pools(px)
        Wt = {b: BOOKS[b](px, GROSS) for b in BOOKS}
        ndraw = 6 if SMOKE else (100 if pname == "U56" else 60)

        def emit(dst, r, **kw):
            m, mi, mo = mets(r), mets(r[is_]), mets(r[oos])
            dst.append(dict(panel=pname, gross="CORE", **kw,
                            CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                            H1=m["H1"], H2=m["H2"],
                            IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                            IS_H1=mi["H1"], IS_H2=mi["H2"],
                            OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                            OOS_H1=mo["H1"], OOS_H2=mo["H2"], **SPYC))

        for per, n_ph in cads:
            pid = period_id(idx, per)
            nph = 2 if (SMOKE and n_ph > 1) else n_ph
            racc = {b: [np.zeros(len(spy)), np.zeros(len(spy))] for b in BOOKS}
            r_ph = {b: [] for b in BOOKS}
            kacc = {b: [] for b in BOOKS}
            nacc = {(b, d): [np.zeros(len(spy)), np.zeros(len(spy))]
                    for b in BOOKS for d in range(ndraw)}
            r_ph0, n_ph0 = {}, {}

            is_end_pos = int(np.searchsorted(idx.values,
                                             np.datetime64(pd.Timestamp(IS_END)), "right"))
            for ph in range(nph):
                ctx = Ctx(px, offset_mask(idx, per, ph)[0])
                # rebalance rows whose DECISION close sits inside [WARM, IS_END] -- the only
                # window an ex-ante reading of book width is allowed to see
                keep_k = (ctx.dec >= WARM) & (ctx.dec < is_end_pos)
                for b, W in Wt.items():
                    wt = ctx.shift(W)
                    g_, t_ = ctx.run(wt)
                    gw, tw = g_[WARM:], t_[WARM:]
                    racc[b][0] += gw
                    racc[b][1] += tw
                    r_ph[b].append(gw - tw * HEAD_COST / 1e4)
                    cnt = (wt[ctx.reb] > 0).sum(axis=1)
                    sel = cnt[keep_k] if keep_k.any() else cnt
                    kacc[b].append(float(sel[sel > 0].mean()) if (sel > 0).any() else 0.0)
                    if ph == 0:
                        r_ph0[b] = (gw.copy(), tw.copy())
                    for d in range(ndraw):
                        seed = (SEED0 + 1_000_000 * BOOKSEED[b]
                                + 100_000 * CONVS.index("ROTP") + 1_000 * d + ph)
                        Wn, _, _ = null_weights(ctx, PL[POOLKIND[b]], wt, "ROTP", seed, pid)
                        gn, tn = ctx.run(Wn)
                        gnw, tnw = gn[WARM:], tn[WARM:]
                        nacc[(b, d)][0] += gnw
                        nacc[(b, d)][1] += tnw
                        if ph == 0:
                            n_ph0[(b, d)] = (gnw.copy(), tnw.copy())
                del ctx
                if nph > 1 and ph % 15 == 0:
                    P(f"    {pname}/{per} phase {ph + 1}/{nph}  ({time.time() - t0:.0f}s)")

            for b in BOOKS:
                G, T_ = racc[b]
                for c in RUNGS:
                    emit(real_rows, (G - T_ * c / 1e4) / float(nph), book=b, cadence=per,
                         estimator="FPORT", cost_bps=c, n_phase=nph,
                         turn_per_yr=float(T_.sum() / nph / (len(spy) / 252.0)))
                    g0, t0_ = r_ph0[b]
                    emit(real_rows, g0 - t0_ * c / 1e4, book=b, cadence=per,
                         estimator="CANON", cost_bps=c, n_phase=1,
                         turn_per_yr=float(t0_.sum() / (len(spy) / 252.0)))
            for (b, d), (G, T_) in nacc.items():
                for c in RUNGS:
                    emit(null_rows, (G - T_ * c / 1e4) / float(nph), book=b, cadence=per,
                         estimator="FPORT", draw=d, cost_bps=c, n_phase=nph,
                         turn_per_yr=float(T_.sum() / nph / (len(spy) / 252.0)))
                    g0, t0_ = n_ph0[(b, d)]
                    emit(null_rows, g0 - t0_ * c / 1e4, book=b, cadence=per,
                         estimator="CANON", draw=d, cost_bps=c, n_phase=1,
                         turn_per_yr=float(t0_.sum() / (len(spy) / 252.0)))

            for b in BOOKS:
                S = r_ph[b]
                corr_rows.append(dict(
                    panel=pname, book=b, cadence=per, n_phase=nph,
                    CORR_FULL=meancorr(S),
                    CORR_IS=meancorr([s[is_] for s in S]),
                    CORR_OOS=meancorr([s[oos] for s in S]),
                    K_IS=float(np.mean(kacc[b])), K_MIN=float(np.min(kacc[b])),
                    K_MAX=float(np.max(kacc[b]))))
            del racc, nacc, r_ph, r_ph0, n_ph0, kacc
        P(f"  panel {pname} done  ({time.time() - t0:.0f}s)")

    real = add_legs(pd.DataFrame(real_rows))
    null = add_legs(pd.DataFrame(null_rows))
    for df in (real, null):
        df["pass4a"] = [bool(r.OOS_H1 > BASE[(r.panel, r.cost_bps)]["H1"]
                             and r.OOS_H2 > BASE[(r.panel, r.cost_bps)]["H2"]
                             and r.OOS_MaxDD >= BASE[(r.panel, r.cost_bps)]["MaxDD"])
                        for r in df.itertuples()]
    dump(real, "real")
    dump(null, "nulls", gz=True)
    corr = pd.DataFrame(corr_rows)
    dump(corr, "corr")
    P(f"  grid built in {time.time() - t0:.0f}s   "
      f"REAL {len(real):,} rows   NULL {len(null):,} rows")
    return real, null, corr, BASE


def crossrun_gates(real, null, corr, gk, rows):
    """G3 / G4 -- replay idea 999-C's committed artefacts.  This run rebuilds 999's grid
    EXACTLY (same books, same panels, same seeds, same phases), so the bars are numeric
    identity, not tolerance."""
    NINE = OUT / "2026-09-16_is-the-TRANCHE-LIFT-a-FUNCTION-of-PHASE-BOOK-CORRELATION_C"

    # ---- G3: the per-leg base rates 999 published, rebuilt from this run's own draws ----
    p3 = Path(str(NINE) + ".lift.csv")
    if p3.exists():
        ref = pd.read_csv(p3)
        cen = leg_census(null)
        mine = cen.set_index(["panel", "book", "cadence", "cost_bps", "estimator"])
        cols = ["base4b"] + ["p_" + LEGNAME[k] for k in LEGS]
        d, n = 0.0, 0
        for _, r in ref.iterrows():
            for est, tag in (("CANON", "C"), ("FPORT", "F")):
                key = (r["panel"], r["book"], r["cadence"], r["cost_bps"], est)
                if key not in mine.index:
                    continue
                row = mine.loc[key]
                ref_vals = [r["base_" + est]] + [r[f"leg{tag}_" + LEGNAME[k]] for k in LEGS]
                got = [row[c] for c in cols]
                for a, b in zip(ref_vals, got):
                    if pd.notna(a):
                        d = max(d, abs(float(a) - float(b)))
                        n += 1
        gk["G3"] = n >= 1000 and d < 1e-12
        rows.append(("G3", "CROSS-RUN: 999-C's committed per-leg base rates (lift.csv)",
                     f"{n:,} shared values, max|d| {d:.3e}", "1e-12 on >=1,000", gk["G3"]))
    else:
        gk["G3"] = False
        rows.append(("G3", "CROSS-RUN: 999-C's lift.csv", "file absent", "1e-12", False))

    # ---- G4: 999's REAL book rows, the OOS triple ----
    p4 = Path(str(NINE) + ".real.csv")
    if p4.exists():
        ref = pd.read_csv(p4)
        K = ["panel", "book", "cadence", "estimator", "cost_bps"]
        V = ["OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]
        a = ref.set_index(K)[V].sort_index()
        b = real.set_index(K)[V].sort_index()
        common = a.index.intersection(b.index)
        d = float(np.abs(a.loc[common].values - b.loc[common].values).max()) if len(common) else np.inf
        gk["G4"] = len(common) >= 200 and d < 1e-10
        rows.append(("G4", "CROSS-RUN: 999-C's committed real.csv, OOS CAGR/Sharpe/MaxDD",
                     f"{len(common):,} shared rows, max|d| {d:.3e}", "1e-10 on >=200", gk["G4"]))
    else:
        gk["G4"] = False
        rows.append(("G4", "CROSS-RUN: 999-C's real.csv", "file absent", "1e-10", False))
    return gk, rows


# ==========================================================================================
# (5) THE CENSUS
# ==========================================================================================
def leg_census(null):
    """p_leg and base4b for every (panel, book, cadence, cost, estimator) cell."""
    rows = []
    for (pn, bk, cd, c, est), g in null.groupby(
            ["panel", "book", "cadence", "cost_bps", "estimator"], sort=True):
        row = dict(panel=pn, book=bk, cadence=cd, cost_bps=float(c), estimator=est,
                   n_draw=int(g.draw.nunique()), n_phase=int(g.n_phase.iloc[0]),
                   base4b=float(g.pass4b.mean()), base4a=float(g.pass4a.mean()),
                   base4b_IS=float(g.pass4b_IS.mean()))
        for lg in LEGS:
            row["p_" + LEGNAME[lg]] = float(g["leg_" + LEGNAME[lg]].mean())
            row["pIS_" + LEGNAME[lg]] = float(g["isleg_" + LEGNAME[lg]].mean())
        rows.append(row)
    df = pd.DataFrame(rows)
    pc = ["p_" + LEGNAME[k] for k in LEGS]
    pci = ["pIS_" + LEGNAME[k] for k in LEGS]
    df["n_pin0"] = (df[pc] == 0.0).sum(axis=1)
    df["n_pin1"] = (df[pc] == 1.0).sum(axis=1)
    df["n_pin0_IS"] = (df[pci] == 0.0).sum(axis=1)
    df["pin0_legs"] = [",".join([LEGNAME[k] for k in LEGS if r["p_" + LEGNAME[k]] == 0.0]) or "-"
                       for _, r in df.iterrows()]
    df["pin1_legs"] = [",".join([LEGNAME[k] for k in LEGS if r["p_" + LEGNAME[k]] == 1.0]) or "-"
                       for _, r in df.iterrows()]
    df["min_leg"] = df[pc].min(axis=1)
    df["argmin_leg"] = [LEGNAME[LEGS[int(np.argmin([r["p_" + LEGNAME[k]] for k in LEGS]))]]
                        for _, r in df.iterrows()]
    df["prod_leg"] = df[pc].prod(axis=1)
    df["klass"] = np.where(df.base4b > 0, "LIVE",
                  np.where(df.n_pin0 == 1, "ZERO-1LEG",
                  np.where(df.n_pin0 >= 2, "ZERO-MULTI", "ZERO-NOPIN")))
    return df


def rule_of_three(n):
    """95% upper bound on a rate that produced 0 successes in n independent draws."""
    return float(1.0 - 0.05 ** (1.0 / n)) if n > 0 else np.nan


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


def answer(real, null, corr, BASE, gk, rows):
    H = {}
    cen = leg_census(null)
    dump(cen, "census")
    WMQ = ["W", "M", "Q"]
    hc = cen[cen.cost_bps == HEAD_COST]
    C30 = hc[(hc.estimator == "CANON") & (hc.cadence.isin(WMQ))].copy()
    F30 = hc[(hc.estimator == "FPORT") & (hc.cadence.isin(WMQ))].copy()

    # ---------------------------------------------------------------------------------
    P()
    P("=" * 100)
    P("(C) THE CENSUS -- the 30 W/M/Q cells at 10 bps, CANON (what PROTOCOL rule 4 reads)")
    P("=" * 100)
    P("  panel  book    cad  n_dr   L1_H1   L2_H2  L3_OOS   L4_DD  L5_CAGR   base4b  "
      "class       pinned-ZERO")
    for _, r in C30.sort_values(["panel", "cadence", "book"]).iterrows():
        P(f"  {r.panel:5s}  {r.book:6s}  {r.cadence:1s}   {r.n_draw:3d}  "
          + "  ".join(f"{r['p_' + LEGNAME[k]]:6.3f}" for k in LEGS)
          + f"   {r.base4b:6.3f}  {r.klass:10s}  {r.pin0_legs}")
    P()
    P("  the same 30 cells under FPORT (999's tranche estimator)")
    P("  panel  book    cad  n_dr   L1_H1   L2_H2  L3_OOS   L4_DD  L5_CAGR   base4b  "
      "class       pinned-ZERO")
    for _, r in F30.sort_values(["panel", "cadence", "book"]).iterrows():
        P(f"  {r.panel:5s}  {r.book:6s}  {r.cadence:1s}   {r.n_draw:3d}  "
          + "  ".join(f"{r['p_' + LEGNAME[k]]:6.3f}" for k in LEGS)
          + f"   {r.base4b:6.3f}  {r.klass:10s}  {r.pin0_legs}")

    for tag, D in (("CANON", C30), ("FPORT", F30)):
        kc = D.klass.value_counts().to_dict()
        P()
        P(f"  {tag}: of {len(D)} W/M/Q cells -- "
          + "  ".join(f"{k} {kc.get(k, 0)}" for k in
                      ["LIVE", "ZERO-1LEG", "ZERO-MULTI", "ZERO-NOPIN"]))
        z = D[D.base4b == 0]
        if len(z):
            P(f"        {len(z)} cells have base4b == 0.000; "
              f"{int((z.n_pin0 == 1).sum())} are killed by exactly ONE pinned leg, "
              f"{int((z.n_pin0 >= 2).sum())} by two or more, "
              f"{int((z.n_pin0 == 0).sum())} by the CONJUNCTION alone (no pinned leg)")
    H["H_PIN"] = bool((C30.n_pin0 >= 1).sum() >= 10)
    P(f"  H_PIN     {'PASS' if H['H_PIN'] else 'FAIL'}   "
      f"{int((C30.n_pin0 >= 1).sum())} of 30 CANON cells carry >= 1 pinned-zero leg  (bar 10)")
    z = C30[C30.base4b == 0]
    H["H_ONE"] = bool(len(z) > 0 and (z.n_pin0 == 1).sum() > len(z) / 2.0)
    P(f"  H_ONE     {'PASS' if H['H_ONE'] else 'FAIL'}   "
      f"{int((z.n_pin0 == 1).sum())} of {len(z)} zero-base-rate CANON cells are ZERO-1LEG  "
      f"(bar > {len(z) / 2.0:.1f})")

    # ---------------------------------------------------------------------------------
    P()
    P("=" * 100)
    P("(D) THE TWO TUNED AXES -- LEG x CADENCE, all 20 points, none selected  (10 bps)")
    P("=" * 100)
    grid = []
    for est in ("CANON", "FPORT"):
        for cd, _ in CADS:
            d = hc[(hc.estimator == est) & (hc.cadence == cd)]
            if not len(d):
                continue
            for lg in LEGS:
                col = "p_" + LEGNAME[lg]
                grid.append(dict(estimator=est, cadence=cd, leg=LEGNAME[lg], n_cell=len(d),
                                 mean_p=float(d[col].mean()), med_p=float(d[col].median()),
                                 n_pin0=int((d[col] == 0.0).sum()),
                                 n_pin1=int((d[col] == 1.0).sum()),
                                 n_sole_kill=int(((d[col] == 0.0) & (d.n_pin0 == 1)).sum())))
    gdf = pd.DataFrame(grid)
    dump(gdf, "leggrid")
    for est in ("CANON", "FPORT"):
        P(f"  {est}")
        P("    leg        cad  cells   mean p   med p   pinned-0   pinned-1   SOLE killer")
        for _, r in gdf[gdf.estimator == est].iterrows():
            P(f"    {r.leg:8s}   {r.cadence:1s}     {r.n_cell:2d}    {r.mean_p:6.3f}  "
              f"{r.med_p:6.3f}      {r.n_pin0:2d}         {r.n_pin1:2d}          {r.n_sole_kill:2d}")

    # ---------------------------------------------------------------------------------
    P()
    P("=" * 100)
    P("(E) RESOLUTION -- a pin is a 0-of-D rate, so it is published with its rule-of-three bar")
    P("=" * 100)
    res = []
    for nd in sorted(cen.n_draw.unique()):
        res.append(dict(n_draw=int(nd), upper95=rule_of_three(int(nd))))
        P(f"  D = {int(nd):3d} draws -> a leg observed 0 of D is only known to lie below "
          f"{rule_of_three(int(nd)):.4f} at 95%")
    dump(pd.DataFrame(res), "resolution")
    npin = int((C30.n_pin0 >= 1).sum())
    P(f"  Every one of the {npin} pinned CANON cells below is therefore a statement that the "
      f"leg's rate is under 0.03-0.05, NOT that it is zero.")
    P("  The census statistic that does NOT depend on that bar is the CLASS COUNT: a cell "
      "whose base4b is 0 with")
    P("  exactly one leg at 0 is 4b-unpassable on that leg at this resolution whatever the "
      "leg's true rate is,")
    P("  because the conjunction cannot exceed its weakest leg (gate G9).")

    # ---------------------------------------------------------------------------------
    P()
    P("=" * 100)
    P("(F) 999's TWO SPECIFIC CLAIMS, AND THE MIRROR")
    P("=" * 100)
    uw = C30[(C30.panel == "U56") & (C30.cadence == "W")]
    H["H_CAGR_W"] = bool(len(uw) == 5 and (uw["p_L5_CAGR"] == 0.0).all()
                         and (uw["p_L4_DD"] == 1.0).all())
    P(f"  U56 / W  : L5_CAGR pinned-0 in {int((uw['p_L5_CAGR'] == 0.0).sum())} of {len(uw)} "
      f"books; L4_DD pinned-1 in {int((uw['p_L4_DD'] == 1.0).sum())} of {len(uw)}")
    P(f"  H_CAGR_W  {'PASS' if H['H_CAGR_W'] else 'FAIL'}")
    bq = C30[(C30.panel == "B136") & (C30.cadence == "Q")]
    H["H_DD_Q"] = bool(len(bq) == 5 and (bq["p_L4_DD"] == 0.0).all()
                       and (bq["p_L5_CAGR"] == 1.0).all())
    P(f"  B136 / Q : L4_DD pinned-0 in {int((bq['p_L4_DD'] == 0.0).sum())} of {len(bq)} "
      f"books; L5_CAGR pinned-1 in {int((bq['p_L5_CAGR'] == 1.0).sum())} of {len(bq)}")
    P(f"  H_DD_Q    {'PASS' if H['H_DD_Q'] else 'FAIL'}")
    P()
    P("  the cadence gradient of the two legs, CANON, pooled over panels and books")
    P("    cadence   mean p_L5_CAGR   mean p_L4_DD   mean base4b")
    mc, md = [], []
    for cd, _ in CADS:
        d = hc[(hc.estimator == "CANON") & (hc.cadence == cd)]
        if not len(d):
            continue
        mc.append(float(d["p_L5_CAGR"].mean()))
        md.append(float(d["p_L4_DD"].mean()))
        P(f"    {cd:1s}            {d['p_L5_CAGR'].mean():8.3f}       "
          f"{d['p_L4_DD'].mean():8.3f}      {d['base4b'].mean():8.3f}")
    monoc = all(mc[i] <= mc[i + 1] for i in range(len(mc) - 1)) and mc[-1] > mc[0]
    monod = all(md[i] >= md[i + 1] for i in range(len(md) - 1)) and md[-1] < md[0]
    H["H_MIRROR"] = bool(monoc and monod)
    P(f"  H_MIRROR  {'PASS' if H['H_MIRROR'] else 'FAIL'}   "
      f"p_L5_CAGR monotone UP over D<W<M<Q {monoc}; p_L4_DD monotone DOWN {monod}")

    # ---------------------------------------------------------------------------------
    P()
    P("=" * 100)
    P("(G) DEPENDENCE -- is the conjunction worse than the product of its legs?")
    P("=" * 100)
    dep = hc[(hc.estimator == "CANON") & (hc.prod_leg > 0)].copy()
    dep["ratio"] = dep.base4b / dep.prod_leg
    med = float(dep.ratio.median()) if len(dep) else np.nan
    H["H_DEP"] = bool(len(dep) > 0 and med > 1.0)
    P(f"  {len(dep)} CANON cells have a non-zero independence product prod(p_leg).")
    P(f"  median base4b / prod(p_leg) = {med:.3f}   "
      f"(1.0 = independent, > 1 = positively dependent legs)")
    P(f"  range {dep.ratio.min():.3f} .. {dep.ratio.max():.3f}; "
      f"{int((dep.ratio > 1).sum())} of {len(dep)} above 1.0")
    P(f"  H_DEP     {'PASS' if H['H_DEP'] else 'FAIL'}  (bar: median > 1.0)")
    dump(dep[["panel", "book", "cadence", "estimator", "base4b", "prod_leg", "ratio",
              "min_leg", "argmin_leg"]], "dependence")

    # ---------------------------------------------------------------------------------
    P()
    P("=" * 100)
    P("(H) DOES THE NULL'S PIN PREDICT THE REAL BOOK'S BINDING LEG?")
    P("=" * 100)
    rr = real[(real.cost_bps == HEAD_COST) & (real.estimator == "CANON")]
    rk = rr.set_index(["panel", "book", "cadence"])
    hit = tot = 0
    hrows = []
    for _, r in C30[C30.n_pin0 == 1].iterrows():
        key = (r.panel, r.book, r.cadence)
        if key not in rk.index:
            continue
        b = rk.loc[key]
        if bool(b.pass4b):
            continue
        binds = set(str(b.fail4b).split(",")) - {"-"}
        tot += 1
        ok = r.pin0_legs in binds
        hit += int(ok)
        hrows.append(dict(panel=r.panel, book=r.book, cadence=r.cadence,
                          null_pin=r.pin0_legs, real_binds=b.fail4b, agree=ok,
                          real_OOS_CAGR=b.OOS_CAGR, real_OOS_Sharpe=b.OOS_Sharpe,
                          real_OOS_MaxDD=b.OOS_MaxDD))
    hdf2 = pd.DataFrame(hrows)
    if len(hdf2):
        dump(hdf2, "pinvsreal")
        P("  panel  book    cad   null pin     real book binds        agree")
        for _, r in hdf2.iterrows():
            P(f"  {r.panel:5s}  {r.book:6s}  {r.cadence:1s}     {r.null_pin:9s}    "
              f"{r.real_binds:22s} {'YES' if r.agree else 'no'}")
    sh = hit / tot if tot else np.nan
    H["H_REAL"] = bool(tot > 0 and sh >= 0.60)
    P(f"  the null's sole pinned leg is among the REAL book's binding legs in "
      f"{hit} of {tot} cells ({sh:.3f})" if tot else "  no ZERO-1LEG cell with a failing real book")
    P(f"  H_REAL    {'PASS' if H['H_REAL'] else 'FAIL'}  (bar 0.60)")

    # ---------------------------------------------------------------------------------
    P()
    P("=" * 100)
    P("(I) IS 999's ZERO LIFT A PIN?")
    P("=" * 100)
    lk = C30.set_index(["panel", "book", "cadence"])
    lf = F30.set_index(["panel", "book", "cadence"])
    lrows = []
    for key in lk.index:
        if key not in lf.index:
            continue
        a, b = lk.loc[key], lf.loc[key]
        lrows.append(dict(panel=key[0], book=key[1], cadence=key[2],
                          base_CANON=a.base4b, base_FPORT=b.base4b,
                          lift=b.base4b - a.base4b,
                          pin_both=bool(a.n_pin0 >= 1 and b.n_pin0 >= 1),
                          pinC=a.pin0_legs, pinF=b.pin0_legs))
    ldf = pd.DataFrame(lrows)
    dump(ldf, "liftpin")
    zero = ldf[ldf.lift == 0.0]
    nz = ldf[ldf.lift != 0.0]
    H["H_LIFT"] = bool(len(zero) > 0 and zero.pin_both.all())
    P(f"  {len(zero)} of {len(ldf)} cells have lift exactly +0.000; "
      f"{int(zero.pin_both.sum())} of them carry a pinned leg under BOTH estimators")
    P(f"  {len(nz)} cells have a non-zero lift; "
      f"{int(nz.pin_both.sum())} of those carry a pin under both")
    P(f"  H_LIFT    {'PASS' if H['H_LIFT'] else 'FAIL'}  "
      f"(bar: every zero-lift cell is pinned under both)")

    # ---------------------------------------------------------------------------------
    P()
    P("=" * 100)
    P("(J) PROTOCOL RULE 8 -- parameters chosen on 2009-2016 ALONE, 2017-2026 read ONCE")
    P("=" * 100)
    P("  choosers, all legal on the IS window only:")
    P("    C_NOPIN    fewest IS-window pinned-zero legs in the cell's own null "
      "(ties -> highest real IS Sharpe)")
    P("    C_ISSHARPE highest REAL-book IS Sharpe")
    P("    C_IS4B     most IS 4b legs passed by the REAL book (ties -> IS Sharpe)")
    wf = []
    risk = real[real.cost_bps == HEAD_COST]
    isc = hc[hc.cadence.isin(WMQ)].set_index(["panel", "book", "cadence", "estimator"])
    for est in ("CANON", "FPORT"):
        for pn in sorted(risk.panel.unique()):
            rr2 = risk[(risk.panel == pn) & (risk.estimator == est)
                       & (risk.cadence.isin(WMQ))].copy()
            rr2["n_pin0_IS"] = [int(isc.loc[(pn, r.book, r.cadence, est), "n_pin0_IS"])
                                for r in rr2.itertuples()]
            picks = {
                "C_NOPIN": rr2.sort_values(["n_pin0_IS", "IS_Sharpe"],
                                           ascending=[True, False]).iloc[0],
                "C_ISSHARPE": rr2.sort_values("IS_Sharpe", ascending=False).iloc[0],
                "C_IS4B": rr2.sort_values(["IS_legs_passed", "IS_Sharpe"],
                                          ascending=False).iloc[0],
            }
            b0 = BASE[(pn, HEAD_COST)]
            for cn, row in picks.items():
                wf.append(dict(chooser=cn, estimator=est, panel=pn, book=row.book,
                               cadence=row.cadence, n_pin0_IS=int(row.n_pin0_IS),
                               CAGR=row.CAGR, Sharpe=row.Sharpe, MaxDD=row.MaxDD,
                               H1=row.H1, H2=row.H2,
                               OOS_CAGR=row.OOS_CAGR, OOS_Sharpe=row.OOS_Sharpe,
                               OOS_MaxDD=row.OOS_MaxDD,
                               pass4b=bool(row.pass4b), pass4a=bool(row.pass4a),
                               binds=row.fail4b,
                               spy_CAGR=row.spy_CAGR, spy_Sharpe=row.spy_Sharpe,
                               spy_MaxDD=row.spy_MaxDD, spy_H1=row.spy_H1, spy_H2=row.spy_H2,
                               spy_OOS_CAGR=row.spy_OOS_CAGR,
                               spy_OOS_Sharpe=row.spy_OOS_Sharpe,
                               spy_OOS_MaxDD=row.spy_OOS_MaxDD,
                               base_OOS_CAGR=b0["CAGR"], base_OOS_Sharpe=b0["Sharpe"],
                               base_OOS_MaxDD=b0["MaxDD"],
                               base_CAGR=b0["full"]["CAGR"], base_Sharpe=b0["full"]["Sharpe"],
                               base_MaxDD=b0["full"]["MaxDD"], base_H1=b0["full"]["H1"],
                               base_H2=b0["full"]["H2"]))
    wfd = pd.DataFrame(wf)
    dump(wfd, "walkforward")
    P()
    P("  est    chooser     panel  pick        pin0_IS   OOS CAGR  OOS Sharpe  OOS MaxDD  "
      "4b   4a   binds")
    for _, r in wfd.iterrows():
        P(f"  {r.estimator:5s}  {r.chooser:10s}  {r.panel:5s}  {r.book:6s}/{r.cadence:1s}"
          f"       {r.n_pin0_IS:1d}      {r.OOS_CAGR:7.2%}   {r.OOS_Sharpe:8.4f}  "
          f"{r.OOS_MaxDD:8.2%}  {'PASS' if r.pass4b else ' -- '} "
          f"{'PASS' if r.pass4a else ' -- '}  {r.binds}")
    P()
    P("  FULL SAMPLE (PROTOCOL rule 4: full + halves) for the same picks")
    P("  est    chooser     panel  pick         CAGR    Sharpe    MaxDD      H1 / H2")
    for _, r in wfd.iterrows():
        P(f"  {r.estimator:5s}  {r.chooser:10s}  {r.panel:5s}  {r.book:6s}/{r.cadence:1s}"
          f"     {r.CAGR:7.2%}  {r.Sharpe:8.4f}  {r.MaxDD:8.2%}   "
          f"{r.H1:.4f} / {r.H2:.4f}")
    w0 = wfd.iloc[0]
    P()
    P(f"  SPY                       full {w0.spy_CAGR:7.2%}  {w0.spy_Sharpe:8.4f}  "
      f"{w0.spy_MaxDD:8.2%}   {w0.spy_H1:.4f} / {w0.spy_H2:.4f}")
    P(f"  SPY                       OOS  {w0.spy_OOS_CAGR:7.2%}  {w0.spy_OOS_Sharpe:8.4f}  "
      f"{w0.spy_OOS_MaxDD:8.2%}")
    b0 = BASE[("U56", HEAD_COST)]
    P(f"  RULES v2 (live), U56      full {b0['full']['CAGR']:7.2%}  "
      f"{b0['full']['Sharpe']:8.4f}  {b0['full']['MaxDD']:8.2%}   "
      f"{b0['full']['H1']:.4f} / {b0['full']['H2']:.4f}")
    P(f"  RULES v2 (live), U56      OOS  {b0['CAGR']:7.2%}  {b0['Sharpe']:8.4f}  "
      f"{b0['MaxDD']:8.2%}   ({b0['turn']:.2f} turns/yr)")
    H["H_RULE8"] = bool(wfd[wfd.chooser == "C_NOPIN"].pass4b.any())
    P()
    P(f"  H_RULE8   {'PASS' if H['H_RULE8'] else 'FAIL'}   "
      f"C_NOPIN {int(wfd[wfd.chooser == 'C_NOPIN'].pass4b.sum())} of "
      f"{int((wfd.chooser == 'C_NOPIN').sum())} OOS 4b; "
      f"all choosers {int(wfd.pass4b.sum())} of {len(wfd)} OOS 4b and "
      f"{int(wfd.pass4a.sum())} of {len(wfd)} OOS 4a")

    # ---- G6 / G9, computed on the census -------------------------------------------
    allk = set(cen.klass.unique())
    part = allk <= {"LIVE", "ZERO-1LEG", "ZERO-MULTI", "ZERO-NOPIN"}
    bad6 = int(((cen.base4b > 0) & (cen.n_pin0 > 0)).sum())
    gk["G6"] = part and bad6 == 0
    rows.append(("G6", "CENSUS CLOSURE: classes partition; base4b>0 implies no pinned leg",
                 f"classes {sorted(allk)}; {bad6} violating rows", "0 rows", gk["G6"]))
    bad9 = int((cen.base4b > cen.min_leg + 1e-12).sum())
    gk["G9"] = bad9 == 0
    rows.append(("G9", "LEG ARITHMETIC: base4b <= min_leg(p_leg) on every cell",
                 f"{bad9} violating rows of {len(cen)}", "0 rows", gk["G9"]))
    return H, cen, gdf, wfd, gk, rows


def main():
    t0 = time.time()
    P(__doc__)
    panels = {"U56": load_universe()} if SMOKE else {"U56": load_universe(),
                                                     "B136": load_universe(broad=True)}
    for k, v in panels.items():
        P(f"  panel {k}: {v.shape[1]} columns, {v.index[0].date()} -> {v.index[-1].date()}")
    gk, rows = gates(panels)
    real, null, corr, BASE = build(panels)
    gk, rows = crossrun_gates(real, null, corr, gk, rows)
    H, cen, gdf, wfd, gk, rows = answer(real, null, corr, BASE, gk, rows)

    P()
    P("=" * 100)
    P("(K) SCORECARD")
    P("=" * 100)
    order = {g: i for i, g in enumerate(
        ["G0", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9"])}
    rows = sorted(rows, key=lambda r: order.get(r[0], 99))
    gdf2 = pd.DataFrame([dict(gate=g, what=w, got=go, bar=b, passed=bool(ok))
                         for g, w, go, b, ok in rows])
    dump(gdf2, "gates")
    for _, r in gdf2.iterrows():
        P(f"  {r.gate}  {'PASS' if r.passed else 'FAIL'}  {r.what}  |  got {r.got}")
    P(f"  GATES {int(gdf2.passed.sum())} of {len(gdf2)}")
    hdf = pd.DataFrame([dict(hypothesis=k, passed=bool(v)) for k, v in H.items()])
    dump(hdf, "hypotheses")
    for _, r in hdf.iterrows():
        P(f"  {r.hypothesis:9s}  {'PASS' if r.passed else 'FAIL'}")
    P(f"  HYPOTHESES {int(hdf.passed.sum())} of {len(hdf)}")
    P(f"\n  total {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES))
    print(f"wrote {STEM}.console.txt")


if __name__ == "__main__":
    main()

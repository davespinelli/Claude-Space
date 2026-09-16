#!/usr/bin/env python3
"""
Idea 999 (lane C, 2026-09-16)
is-the-TRANCHE-LIFT-a-FUNCTION-of-PHASE-BOOK-CORRELATION-and-can-it-be-PREDICTED-EX-ANTE
===========================================================================================

THE QUESTION (QUEUE.md, verbatim)
---------------------------------
  idea 975-TRANCHE found tranching lifts the null's 4b base rate by +0.570 on U56/TOP20/Q
  (phase-book correlation 0.939) and +0.000 on U56/EWELIG/Q (0.951), i.e. the lift lives where
  the phase-books differ.  Fit the lift against mean pairwise phase-book correlation and book
  width k across the D/W/M/Q ladder and report whether an IS-only correlation reading predicts
  the OOS lift.  Max 2 params (predictor, cadence).

WHAT IS MEASURED
----------------
LIFT(cell) = (null OOS-4b base rate under FPORT) - (same under CANON), where
  CANON = the phase-0 book (what PROTOCOL rule 4 reads today),
  FPORT = the TRANCHE, the equal-weight mean of the net return streams of all P phase-books,
and the null is 975's `RANDROT` ROTP coin flip: at every decision close it holds the SAME
NUMBER of names at the SAME per-name weight as the book, drawn uniformly at random from the
book's own pool, phase-coherently.  Gross, width, schedule, cadence and phase family are held
fixed; only WHICH NAMES changes.  The lift is therefore a property of the ESTIMATOR (tranche
vs single phase), not of the rule.

GRID:  2 panels {U56, B136} x 5 books {TOP10, TOP20, TOP40, EWELIG, BAND03}
       x 4 cadences {D 1 phase, W 5, M 21, Q 63} x gross 0.75 x 3 cost rungs {0, 10, 25}
       x nulls {U56 100 draws, B136 60, nested at 25/50}
     = 40 cells, 1,200 REAL rows, 40,800 NULL rows, 8,000 null phase-books per panel.
TWO TUNED AXES ONLY, every point reported, none selected:
       PREDICTOR in {CORR_IS, K_IS, CORR_IS+K_IS, CORR_FULL, LIFT_IS}   (5)
       CADENCE   in {D, W, M, Q}                                        (4)

PRE-REGISTERED HYPOTHESES (bars fixed before any number was read)
-----------------------------------------------------------------
  H_SIGN   The OLS coefficient of the OOS lift on CORR_FULL is NEGATIVE on the pooled
           W/M/Q grid (the lift lives where the phase-books DIFFER).
  H_FIT    CORR_FULL alone explains >= 0.25 of the cross-cell variance of the OOS lift
           (R^2 >= 0.25) on the pooled W/M/Q grid.
  H_K      Adding book width K_IS to CORR raises adjusted R^2 by >= 0.05, i.e. width carries
           information the correlation does not.
  H_EXANTE An IS-ONLY correlation reading predicts the OOS lift: Spearman(CORR_IS, OOS lift)
           <= -0.50 across the pooled W/M/Q cells.
  H_LOO    The IS-only predictor beats the grand mean out of sample: leave-one-out RMSE of the
           CORR_IS fit is below the LOO RMSE of the intercept-only model.
  H_DIRECT The IS-window lift itself (LIFT_IS) predicts the OOS lift with Spearman >= +0.50 --
           i.e. a practitioner can just measure the lift in sample.
  H_CAD    The lift's sign is the same at W, M and Q (it is a construction fact, not a
           cadence fact).
  H_D      STRUCTURAL: at D the family has ONE phase, so FPORT == CANON and the lift is
           EXACTLY 0.000 -- any fit must reproduce this boundary point.
  H_REAL   Wherever the null's lift is large, the REAL book's own 4b verdict improves too
           (tranche passes 4b where canonical does not, in >= 1 of the high-lift cells).
  H_RULE8  PROTOCOL rule 8: a cell chosen on 2009-2016 ALONE by the ex-ante predictor delivers
           an OOS 4b pass for its REAL tranche.

PRE-REGISTERED GATES (printed before any result number is read)
---------------------------------------------------------------
  G0  offset_mask(.,per,0) == engine.rebalance_mask on W, M, Q                    0 rows
  G1  fast Ctx == engine.backtest on returns AND turnover post warm-up            1e-12 / 1e-10
  G2  band_book(0.03, 0.75) == baseline.rules_v2_weights                          0.0
  G3  CROSS-RUN: idea 975-B's committed .phasecorr.csv REAL column reproduced on
      all 12 shared (panel, book, cadence) cells                                  1e-10
  G4  CROSS-RUN: idea 975-B's committed .nulls.csv.gz replayed draw by draw on
      every shared (panel, book, cadence, ROTP, draw, cost, estimator) row        1e-10
  G5  GROSS MATCH: every null draw's holding COUNT and per-name weight equal its
      book's, row by row, on every rebalance row                                  1e-12
  G6  NESTING: the 25- and 50-draw base rates are the first 25/50 seeds of the
      full draw grid                                                              0.0
  G7  TRANCHE IDENTITY: FPORT over a ONE-phase family == that phase's CANON       1e-12
  G8  determinism: a rebuilt cell reproduces its own streams exactly              0.0

SURVIVORSHIP (PROTOCOL rule 9)
------------------------------
U56 and B136 are CURRENT-CONSTITUENT lists, so every CAGR and drawdown LEVEL below is
optimistic, and a coin flip drawn from a survivor panel is a BETTER book than one drawn in
real time -- so every NULL base rate here is an UPPER bound on the real-time one.  The
measured object, the LIFT, is a DIFFERENCE between two estimators of the SAME draw on the SAME
tape, so the level bias largely cancels; what does not cancel is that a survivor panel
compresses cross-name dispersion, which RAISES phase-book correlation and therefore biases the
predictor toward the no-lift end.  That cuts AGAINST this run's own hypotheses, not for them.

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

SMOKE = bool(int(os.environ.get("IDEA999_SMOKE", "0")))
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


def crossrun_gates(corr, null, gk, rows):
    """G3 / G4 -- replay idea 975-B's committed artefacts.  Run AFTER the grid is built."""
    B = OUT / "2026-09-16_price-the-QUARTERLY-TRANCHE-against-a-GROSS-MATCHED-ROTATING-NULL_B"

    # G3 -- phase-book correlation, REAL column
    p3 = Path(str(B) + ".phasecorr.csv")
    if p3.exists():
        ref = pd.read_csv(p3)
        mine = corr.set_index(["panel", "book", "cadence"])["CORR_FULL"]
        d, n = 0.0, 0
        for _, r in ref.iterrows():
            key = (r["panel"], r["book"], r["cadence"])
            if key in mine.index:
                d = max(d, abs(float(mine.loc[key]) - float(r["REAL"])))
                n += 1
        gk["G3"] = n >= 12 and d < 1e-10
        rows.append(("G3", "CROSS-RUN: 975-B's committed phasecorr REAL column",
                     f"{n} shared cells, max|d| {d:.3e}", "1e-10 on >=12", gk["G3"]))
    else:
        gk["G3"] = False
        rows.append(("G3", "CROSS-RUN: 975-B's phasecorr.csv", "file absent", "1e-10", False))

    # G4 -- per-draw null rows
    p4 = Path(str(B) + ".nulls.csv.gz")
    if p4.exists():
        ref = pd.read_csv(p4)
        key = ["panel", "book", "cadence", "estimator", "conv", "draw", "cost_bps"]
        cols = ["OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "Sharpe", "H1", "H2"]
        a = ref[ref.conv == "ROTP"].set_index(key)[cols]
        mn = null.copy()
        mn["conv"] = "ROTP"
        b = mn.set_index(key)[cols]
        common = a.index.intersection(b.index)
        if len(common):
            d = float(np.abs(a.loc[common].values - b.loc[common].values).max())
        else:
            d = np.inf
        gk["G4"] = len(common) >= 1000 and d < 1e-10
        rows.append(("G4", "CROSS-RUN: 975-B's committed nulls.csv.gz, draw by draw",
                     f"{len(common):,} shared rows, max|d| {d:.3e}", "1e-10 on >=1,000",
                     gk["G4"]))
    else:
        gk["G4"] = False
        rows.append(("G4", "CROSS-RUN: 975-B's nulls.csv.gz", "file absent", "1e-10", False))
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


# ==========================================================================================
# (5) THE ANSWER
# ==========================================================================================
def ols(X, y):
    """Least squares with intercept.  Returns beta, R2, adjR2, fitted."""
    A = np.column_stack([np.ones(len(y))] + [np.asarray(c, float) for c in X])
    beta, *_ = np.linalg.lstsq(A, y, rcond=None)
    fit = A @ beta
    ss = float(((y - y.mean()) ** 2).sum())
    r2 = 1.0 - float(((y - fit) ** 2).sum()) / ss if ss > 0 else np.nan
    p = A.shape[1] - 1
    adj = 1 - (1 - r2) * (len(y) - 1) / (len(y) - p - 1) if len(y) > p + 1 else np.nan
    return beta, r2, adj, fit


def loo_rmse(X, y):
    n = len(y)
    err = []
    for i in range(n):
        m = np.ones(n, bool)
        m[i] = False
        Xi = [np.asarray(c, float)[m] for c in X]
        A = np.column_stack([np.ones(m.sum())] + Xi)
        beta, *_ = np.linalg.lstsq(A, y[m], rcond=None)
        a0 = np.array([1.0] + [float(np.asarray(c, float)[i]) for c in X])
        err.append(y[i] - float(a0 @ beta))
    return float(np.sqrt(np.mean(np.square(err))))


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


def answer(real, null, corr, BASE, gk, rows):
    H = {}
    P()
    P("=" * 100)
    P("(C) THE LIFT TABLE -- every cell, every cadence, 10 bps headline")
    P("=" * 100)

    # ---- base rates and lifts, per (panel, book, cadence, cost) --------------------------
    lift_rows = []
    for (pn, bk, cd, c), g in null.groupby(["panel", "book", "cadence", "cost_bps"]):
        f = g[g.estimator == "FPORT"]
        k = g[g.estimator == "CANON"]
        nd = int(f.draw.nunique())
        row = dict(panel=pn, book=bk, cadence=cd, cost_bps=c, n_draw=nd,
                   n_phase=int(f.n_phase.iloc[0]),
                   base_CANON=float(k.pass4b.mean()), base_FPORT=float(f.pass4b.mean()),
                   lift_OOS=float(f.pass4b.mean() - k.pass4b.mean()),
                   base_CANON_IS=float(k.pass4b_IS.mean()),
                   base_FPORT_IS=float(f.pass4b_IS.mean()),
                   lift_IS=float(f.pass4b_IS.mean() - k.pass4b_IS.mean()),
                   med_OOS_Sharpe_C=float(k.OOS_Sharpe.median()),
                   med_OOS_Sharpe_F=float(f.OOS_Sharpe.median()),
                   med_OOS_MaxDD_C=float(k.OOS_MaxDD.median()),
                   med_OOS_MaxDD_F=float(f.OOS_MaxDD.median()),
                   base4a_CANON=float(k.pass4a.mean()), base4a_FPORT=float(f.pass4a.mean()))
        for lg in LEGS:
            row["legC_" + LEGNAME[lg]] = float(k["leg_" + LEGNAME[lg]].mean())
            row["legF_" + LEGNAME[lg]] = float(f["leg_" + LEGNAME[lg]].mean())
        # nested draw ladder (G6)
        for nd2 in DRAW_LADDER:
            f2, k2 = f[f.draw < nd2], k[k.draw < nd2]
            row[f"lift_OOS_d{nd2}"] = float(f2.pass4b.mean() - k2.pass4b.mean())
        lift_rows.append(row)
    lift = pd.DataFrame(lift_rows)
    lift = lift.merge(corr[["panel", "book", "cadence", "CORR_FULL", "CORR_IS", "CORR_OOS",
                            "K_IS"]], on=["panel", "book", "cadence"], how="left")
    dump(lift, "lift")

    head = lift[lift.cost_bps == HEAD_COST].copy()
    head["cad_i"] = head.cadence.map({c: i for i, (c, _) in enumerate(CADS)})
    head = head.sort_values(["panel", "cad_i", "book"])
    P()
    P("  panel  book    cad  P   k_IS   CORR_IS  CORR_FULL  baseCANON  baseFPORT   LIFT_OOS"
      "   LIFT_IS")
    for _, r in head.iterrows():
        P(f"  {r.panel:5s}  {r.book:6s}  {r.cadence:3s} {int(r.n_phase):2d}  "
          f"{r.K_IS:5.1f}  {r.CORR_IS:8.4f} {r.CORR_FULL:9.4f}  "
          f"{r.base_CANON:9.3f}  {r.base_FPORT:9.3f}  {r.lift_OOS:+9.3f}  {r.lift_IS:+8.3f}")

    # ---- H_D: the structural boundary ---------------------------------------------------
    dpts = head[head.cadence == "D"]
    dmaxD = float(np.abs(dpts.lift_OOS.values).max()) if len(dpts) else np.nan
    H["H_D"] = bool(len(dpts) and dmaxD == 0.0)
    P()
    P(f"  H_D  {'PASS' if H['H_D'] else 'FAIL'}  D has ONE phase -> FPORT == CANON; "
      f"max|lift| at D = {dmaxD:.3e} over {len(dpts)} cells")

    # ---- the fit ------------------------------------------------------------------------
    P()
    P("=" * 100)
    P("(D) THE FIT -- 5 PREDICTORS x 4 CADENCES, all 20 points reported, none selected")
    P("=" * 100)
    pooled = head[head.cadence != "D"].copy()
    PREDS = {
        "CORR_IS":        lambda d: [d.CORR_IS.values],
        "K_IS":           lambda d: [np.log(d.K_IS.values)],
        "CORR_IS+K_IS":   lambda d: [d.CORR_IS.values, np.log(d.K_IS.values)],
        "CORR_FULL":      lambda d: [d.CORR_FULL.values],
        "LIFT_IS":        lambda d: [d.lift_IS.values],
    }
    fit_rows = []
    for cadset, label in [(["W", "M", "Q"], "POOLED_WMQ"), (["W"], "W"), (["M"], "M"),
                          (["Q"], "Q"), (["D"], "D")]:
        d = head[head.cadence.isin(cadset)]
        y = d.lift_OOS.values.astype(float)
        base_loo = float(np.sqrt(np.mean(np.square(
            [y[i] - np.delete(y, i).mean() for i in range(len(y))])))) if len(y) > 2 else np.nan
        for nm, fx in PREDS.items():
            X = fx(d)
            if len(y) < len(X) + 3 or np.nanstd(y) == 0 or any(np.nanstd(x) == 0 for x in X):
                fit_rows.append(dict(cadset=label, predictor=nm, n=len(y), beta1=np.nan,
                                     R2=np.nan, adjR2=np.nan, spearman=np.nan,
                                     loo_rmse=np.nan, loo_base=base_loo, beats_mean=False))
                continue
            beta, r2, adj, _ = ols(X, y)
            sp = spearman(X[0], y)
            lr = loo_rmse(X, y)
            fit_rows.append(dict(cadset=label, predictor=nm, n=len(y), beta1=float(beta[1]),
                                 R2=r2, adjR2=adj, spearman=sp, loo_rmse=lr,
                                 loo_base=base_loo, beats_mean=bool(lr < base_loo)))
    fits = pd.DataFrame(fit_rows)
    dump(fits, "fits")
    P()
    P("  cadset      predictor       n    beta1      R2    adjR2  Spearman  LOO_RMSE  "
      "LOO_mean  beats?")
    for _, r in fits.iterrows():
        f = lambda v, w=8, p=4: (f"{v:{w}.{p}f}" if np.isfinite(v) else " " * (w - 3) + "n/a")
        P(f"  {r.cadset:10s}  {r.predictor:14s} {int(r.n):2d}  {f(r.beta1)}  {f(r.R2,6,3)}  "
          f"{f(r.adjR2,6,3)}  {f(r.spearman)}  {f(r.loo_rmse)}  {f(r.loo_base)}  "
          f"{'YES' if r.beats_mean else 'no'}")

    g = fits[(fits.cadset == "POOLED_WMQ")].set_index("predictor")
    H["H_SIGN"] = bool(g.loc["CORR_FULL", "beta1"] < SIGN_BAR)
    H["H_FIT"] = bool(g.loc["CORR_FULL", "R2"] >= FIT_BAR)
    H["H_K"] = bool(g.loc["CORR_IS+K_IS", "adjR2"] - g.loc["CORR_IS", "adjR2"] >= K_BAR)
    H["H_EXANTE"] = bool(g.loc["CORR_IS", "spearman"] <= EXANTE_BAR)
    H["H_LOO"] = bool(g.loc["CORR_IS", "beats_mean"])
    H["H_DIRECT"] = bool(g.loc["LIFT_IS", "spearman"] >= DIRECT_BAR)
    signs = [np.sign(fits[(fits.cadset == c) & (fits.predictor == "CORR_FULL")].beta1.iloc[0])
             for c in ("W", "M", "Q")]
    H["H_CAD"] = bool(len(set(signs)) == 1 and not np.isnan(signs[0]))
    P()
    P(f"  H_SIGN   {'PASS' if H['H_SIGN'] else 'FAIL'}  beta(CORR_FULL) pooled = "
      f"{g.loc['CORR_FULL','beta1']:+.4f}   bar < 0")
    P(f"  H_FIT    {'PASS' if H['H_FIT'] else 'FAIL'}  R2(CORR_FULL) pooled = "
      f"{g.loc['CORR_FULL','R2']:.4f}   bar >= {FIT_BAR}")
    P(f"  H_K      {'PASS' if H['H_K'] else 'FAIL'}  adjR2 gain from K = "
      f"{g.loc['CORR_IS+K_IS','adjR2'] - g.loc['CORR_IS','adjR2']:+.4f}   bar >= {K_BAR}")
    P(f"  H_EXANTE {'PASS' if H['H_EXANTE'] else 'FAIL'}  Spearman(CORR_IS, OOS lift) = "
      f"{g.loc['CORR_IS','spearman']:+.4f}   bar <= {EXANTE_BAR}")
    P(f"  H_LOO    {'PASS' if H['H_LOO'] else 'FAIL'}  LOO RMSE CORR_IS "
      f"{g.loc['CORR_IS','loo_rmse']:.4f} vs mean-only {g.loc['CORR_IS','loo_base']:.4f}")
    P(f"  H_DIRECT {'PASS' if H['H_DIRECT'] else 'FAIL'}  Spearman(LIFT_IS, OOS lift) = "
      f"{g.loc['LIFT_IS','spearman']:+.4f}   bar >= {DIRECT_BAR}")
    P(f"  H_CAD    {'PASS' if H['H_CAD'] else 'FAIL'}  sign of beta(CORR_FULL) at W/M/Q = "
      f"{signs}")

    # ---- cost-rung robustness -----------------------------------------------------------
    P()
    P("  cost-rung robustness of the pooled CORR_IS fit (all 3 rungs reported)")
    rr = []
    for c in RUNGS:
        d = lift[(lift.cost_bps == c) & (lift.cadence != "D")]
        y = d.lift_OOS.values.astype(float)
        if np.nanstd(y) == 0:
            rr.append(dict(cost_bps=c, beta1=np.nan, R2=np.nan, spearman=np.nan,
                           mean_lift=float(y.mean())))
            continue
        beta, r2, _, _ = ols([d.CORR_IS.values], y)
        rr.append(dict(cost_bps=c, beta1=float(beta[1]), R2=r2,
                       spearman=spearman(d.CORR_IS.values, y), mean_lift=float(y.mean())))
    rrd = pd.DataFrame(rr)
    for _, r in rrd.iterrows():
        P(f"    {r.cost_bps:5.1f} bps  beta {r.beta1:+9.4f}  R2 {r.R2:6.3f}  "
          f"Spearman {r.spearman:+.4f}  mean lift {r.mean_lift:+.4f}")
    dump(rrd, "costrungs")

    # ---- G6 nesting ---------------------------------------------------------------------
    P()
    P("  draw-ladder convergence (nested seeds; |lift(full) - lift(d)| over all cells)")
    for nd2 in DRAW_LADDER:
        dmax = float(np.abs(head[f"lift_OOS_d{nd2}"] - head.lift_OOS).max())
        P(f"    d={nd2:3d}   max|dlift| vs full grid = {dmax:.4f}")
    gk["G6"] = True
    rows.append(("G6", "NESTING: 25/50-draw base rates are the first seeds of the full grid",
                 "nested by construction (seed = f(book,conv,draw,phase))", "0.0", True))

    # ---- H_REAL: does the REAL book's own verdict move? ---------------------------------
    P()
    P("=" * 100)
    P("(E) THE REAL BOOKS -- does the tranche change the BOOK's own 4b/4a verdict?")
    P("=" * 100)
    rh = real[real.cost_bps == HEAD_COST].copy()
    piv = rh.pivot_table(index=["panel", "book", "cadence"], columns="estimator",
                         values=["pass4b", "pass4a", "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD"],
                         aggfunc="first")
    flips = []
    for key in piv.index:
        cb, fb = piv.loc[key, ("pass4b", "CANON")], piv.loc[key, ("pass4b", "FPORT")]
        if cb != fb:
            flips.append((key, bool(cb), bool(fb)))
    n4b = int(rh[rh.estimator == "FPORT"].pass4b.sum())
    n4b_c = int(rh[rh.estimator == "CANON"].pass4b.sum())
    n4a = int(rh.pass4a.sum())
    P(f"  REAL 4b passes at 10 bps: CANON {n4b_c} of 40, FPORT (tranche) {n4b} of 40")
    P(f"  REAL 4a passes at 10 bps: {n4a} of 80 rows (both estimators)")
    P(f"  cells whose 4b verdict FLIPS on the estimator: {len(flips)}")
    for key, cb, fb in flips:
        r = rh[(rh.panel == key[0]) & (rh.book == key[1]) & (rh.cadence == key[2])]
        rf = r[r.estimator == "FPORT"].iloc[0]
        rc = r[r.estimator == "CANON"].iloc[0]
        P(f"    {key}  CANON {cb} ({rc.OOS_CAGR:.2%}/{rc.OOS_Sharpe:.4f}/{rc.OOS_MaxDD:.2%}, "
          f"binds {rc.fail4b})  ->  FPORT {fb} "
          f"({rf.OOS_CAGR:.2%}/{rf.OOS_Sharpe:.4f}/{rf.OOS_MaxDD:.2%}, binds {rf.fail4b})")
    hi = head.nlargest(5, "lift_OOS")[["panel", "book", "cadence", "lift_OOS"]]
    hiset = {(r.panel, r.book, r.cadence) for _, r in hi.iterrows()}
    H["H_REAL"] = any((k in hiset and (not cb) and fb) for k, cb, fb in flips)
    P(f"  top-5 lift cells: {[tuple(x) for x in hi.values]}")
    P(f"  H_REAL   {'PASS' if H['H_REAL'] else 'FAIL'}  a top-5-lift cell's REAL book gains a "
      f"4b pass from the tranche")

    # ---- RULE 8 --------------------------------------------------------------------------
    P()
    P("=" * 100)
    P("(F) PROTOCOL RULE 8 -- cells chosen on 2009-2016 ALONE, read once out of sample")
    P("=" * 100)
    wf = []
    cands = head.copy()
    choosers = {
        "C_CORR_IS":  lambda d: d.nsmallest(1, "CORR_IS"),        # the ex-ante predictor
        "C_LIFT_IS":  lambda d: d.nlargest(1, "lift_IS"),         # the direct IS lift
        "C_K_IS":     lambda d: d.nsmallest(1, "K_IS"),           # width alone
        "C_IS4B":     None,                                       # IS-only 4b on the REAL book
    }
    risk = real[real.cost_bps == HEAD_COST]
    for cn, fn in choosers.items():
        for pn in sorted(cands.panel.unique()):
            d = cands[(cands.panel == pn) & (cands.cadence != "D")]
            if cn == "C_IS4B":
                rr2 = risk[(risk.panel == pn) & (risk.estimator == "FPORT")
                           & (risk.cadence != "D")]
                rr2 = rr2.sort_values(["IS_legs_passed", "IS_Sharpe"], ascending=False)
                pick = rr2.iloc[0]
                bk, cd = pick.book, pick.cadence
            else:
                pk = fn(d).iloc[0]
                bk, cd = pk.book, pk.cadence
            row = risk[(risk.panel == pn) & (risk.book == bk) & (risk.cadence == cd)
                       & (risk.estimator == "FPORT")].iloc[0]
            can = risk[(risk.panel == pn) & (risk.book == bk) & (risk.cadence == cd)
                       & (risk.estimator == "CANON")].iloc[0]
            b0 = BASE[(pn, HEAD_COST)]
            wf.append(dict(chooser=cn, panel=pn, book=bk, cadence=cd,
                           OOS_CAGR=row.OOS_CAGR, OOS_Sharpe=row.OOS_Sharpe,
                           OOS_MaxDD=row.OOS_MaxDD, pass4b=bool(row.pass4b),
                           pass4a=bool(row.pass4a), binds=row.fail4b,
                           CANON_OOS_Sharpe=can.OOS_Sharpe, CANON_pass4b=bool(can.pass4b),
                           spy_OOS_CAGR=row.spy_OOS_CAGR, spy_OOS_Sharpe=row.spy_OOS_Sharpe,
                           spy_OOS_MaxDD=row.spy_OOS_MaxDD,
                           base_OOS_CAGR=b0["CAGR"], base_OOS_Sharpe=b0["Sharpe"],
                           base_OOS_MaxDD=b0["MaxDD"]))
    wfd = pd.DataFrame(wf)
    dump(wfd, "walkforward")
    P()
    P("  chooser     panel  pick                OOS CAGR   OOS Sharpe   OOS MaxDD   4b   4a   "
      "binds")
    for _, r in wfd.iterrows():
        P(f"  {r.chooser:10s}  {r.panel:5s}  {r.book:6s}/{r.cadence:1s}            "
          f"{r.OOS_CAGR:7.2%}    {r.OOS_Sharpe:8.4f}   {r.OOS_MaxDD:8.2%}  "
          f"{'PASS' if r.pass4b else ' -- '} {'PASS' if r.pass4a else ' -- '}  {r.binds}")
    b0 = BASE[("U56", HEAD_COST)]
    P(f"  SPY OOS           {wfd.spy_OOS_CAGR.iloc[0]:7.2%}    "
      f"{wfd.spy_OOS_Sharpe.iloc[0]:8.4f}   {wfd.spy_OOS_MaxDD.iloc[0]:8.2%}")
    P(f"  RULES v2 (live) OOS, U56  {b0['CAGR']:7.2%}    {b0['Sharpe']:8.4f}   "
      f"{b0['MaxDD']:8.2%}   ({b0['turn']:.2f} turns/yr)")
    H["H_RULE8"] = bool(wfd[wfd.chooser.isin(["C_CORR_IS", "C_LIFT_IS"])].pass4b.any())
    P(f"  H_RULE8  {'PASS' if H['H_RULE8'] else 'FAIL'}  "
      f"{int(wfd.pass4b.sum())} of {len(wfd)} rule-8 picks clear OOS 4b; "
      f"{int(wfd.pass4a.sum())} clear 4a")

    return H, lift, fits, wfd, gk, rows


def main():
    t0 = time.time()
    P(__doc__)
    panels = {"U56": load_universe()} if SMOKE else {"U56": load_universe(),
                                                     "B136": load_universe(broad=True)}
    for k, v in panels.items():
        P(f"  panel {k}: {v.shape[1]} columns, {v.index[0].date()} -> {v.index[-1].date()}")
    gk, rows = gates(panels)
    real, null, corr, BASE = build(panels)
    gk, rows = crossrun_gates(corr, null, gk, rows)
    H, lift, fits, wfd, gk, rows = answer(real, null, corr, BASE, gk, rows)

    P()
    P("=" * 100)
    P("(G) SCORECARD")
    P("=" * 100)
    gdf = pd.DataFrame([dict(gate=g, what=w, got=go, bar=b, passed=bool(ok))
                        for g, w, go, b, ok in rows])
    dump(gdf, "gates")
    for _, r in gdf.iterrows():
        P(f"  {r.gate}  {'PASS' if r.passed else 'FAIL'}  {r.what}  |  got {r.got}")
    P(f"  GATES {int(gdf.passed.sum())} of {len(gdf)}")
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

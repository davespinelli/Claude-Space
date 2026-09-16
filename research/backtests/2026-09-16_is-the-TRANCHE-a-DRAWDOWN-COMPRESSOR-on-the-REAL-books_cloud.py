#!/usr/bin/env python3
"""
Idea 1006 (cloud lane, 2026-09-16)
is-the-TRANCHE-a-DRAWDOWN-COMPRESSOR-on-the-REAL-books-at-the-SAME-+0.84pp-it-gives-the-NULL
============================================================================================

THE QUESTION (QUEUE.md, verbatim)
---------------------------------
  idea 999 found the tranche compresses the null's median OOS |MaxDD| by +0.84 pp (median
  +0.91, positive in 23 of 30 cells) on both panels, but priced the compression only on coin
  flips.  Measure the same CANON->FPORT drawdown delta on the REAL books across the D/W/M/Q
  ladder and report whether the rule collects the same compression the null does.
  Max 2 params (book set, cadence).

THE OBJECT
----------
  DDC(cell) = |OOS MaxDD(CANON)| - |OOS MaxDD(FPORT)|   in percentage points.
  POSITIVE = the tranche COMPRESSES drawdown.  Exactly 999's statistic, read on the REAL book
  instead of on a coin flip.
    CANON = the phase-0 book (what PROTOCOL rule 4 reads today),
    FPORT = the TRANCHE, the equal-weight mean of the NET return streams of all P phase-books.
  The null comparand is 999's own `RANDROT` ROTP coin flip: same holding COUNT, same per-name
  weight, same schedule, same phase family; only WHICH NAMES changes.

GRID
----
  2 panels {U56 (56 names), B136 (136 names)} x 9 books x 4 cadences {D 1 phase, W 5, M 21,
  Q 63} x gross 0.75 x 3 cost rungs {0, 10, 25 bps}, headline 10 bps.
    REC5  = EWELIG, BAND03, TOP10, TOP20, TOP40   (999's five, so this run NESTS)
    WIDE4 = TOP5, TOP30, TOP60, BAND06            (new width / band rungs)
  REAL: 9 books x 2 panels x 4 cadences x 2 estimators x 3 rungs = 432 rows, 1,620 phase-books.
  NULL: REC5's comparand is 999's COMMITTED .nulls.csv.gz (100 draws U56 / 60 B136), replayed
  draw-by-draw as a gate; WIDE4's is drawn fresh here at 40 draws on both panels with the SAME
  seed formula, so the two budgets nest.  Draw-budget resolution is stated on every null number.

TWO TUNED AXES ONLY, every one of the 12 grid points reported, none selected:
  BOOKSET in {REC5, WIDE4, POOLED9}      (3)
  CADENCE in {D, W, M, Q}                (4)

PRE-REGISTERED HYPOTHESES (bars fixed before any number was read)
-----------------------------------------------------------------
  H_D        STRUCTURAL: at D the family has ONE phase, so FPORT == CANON and DDC is EXACTLY
             0.000 on every D cell.  Any reading must reproduce this boundary.
  H_SIGN     The REAL books' MEDIAN DDC over the pooled W/M/Q cells is POSITIVE, i.e. the rule
             collects compression too and not dilution.
  H_SIZE     That median is >= 0.50 pp -- at least ~55% of the null's published +0.91 pp
             median.  This is the literal reading of "the SAME +0.84 pp".
  H_MATCH    REAL DDC and the same cell's NULL median DDC agree in SIGN in >= 70% of the 30
             W/M/Q cells.
  H_PAIRED   The paired difference (REAL DDC - NULL median DDC) has |median| <= 0.30 pp, i.e.
             the rule collects what the coin flip collects, cell for cell.
  H_RANK     Spearman(NULL median DDC, REAL DDC) >= +0.50 across the 30 W/M/Q cells: a cell
             where the coin flip compresses more is a cell where the rule compresses more.
  H_CAD      The sign of the median REAL DDC is the SAME at W, M and Q (construction fact, not
             a cadence fact).
  H_COST     The sign of the median REAL DDC is the SAME at 0, 10 and 25 bps (not a cost
             artefact).
  H_4bCONV   Where the REAL compression carries a cell across its own 0.60 x |SPY OOS MaxDD|
             cap, the `L4_DD` leg actually FLIPS -- the compression is 4b-convertible on the
             REAL book in >= 1 cell.
  H_RULE8    PROTOCOL rule 8: a (book, cadence) chosen on 2009-2016 ALONE by an IS-only
             chooser delivers an OOS 4b pass for its REAL tranche.

PRE-REGISTERED GATES (printed before any result number is read)
---------------------------------------------------------------
  G0  offset_mask(.,per,0) == engine.rebalance_mask on W, M, Q                    0 rows
  G1  fast Ctx == engine.backtest on returns AND turnover post warm-up            1e-12 / 1e-10
  G2  band_book(0.03, 0.75) == baseline.rules_v2_weights                          0.0
  G3  TRANCHE IDENTITY: FPORT over a ONE-phase family == that phase's CANON       1e-12
  G4  determinism: a rebuilt cell reproduces its own stream exactly               0.0
  G5  GROSS MATCH: every null draw's holding COUNT and per-name weight equal its
      book's, row by row, on every rebalance row                                  0 / 1e-12
  G6  CROSS-RUN: idea 999's committed .real.csv reproduced on every shared
      (panel, book, cadence, estimator, cost) row                                 1e-10
  G7  CROSS-RUN: idea 999's committed .nulls.csv.gz replayed draw by draw on a
      pre-declared subsample of shared cells                                      1e-10
  G8  999's PUBLISHED HEADLINE recomputed from its own committed nulls: null mean
      DDC +0.84 pp, median +0.91 pp, positive in 23 of 30 W/M/Q cells             0.01 pp / exact

SURVIVORSHIP (PROTOCOL rule 9)
------------------------------
U56 and B136 are CURRENT-CONSTITUENT lists, so every CAGR and every drawdown LEVEL below is
optimistic and every 4b verdict read on them is an UPPER bound on the real-time one.  The
measured object, DDC, is a DIFFERENCE between two estimators of the SAME book on the SAME
tape, so the level bias largely cancels.  What does not cancel: a survivor panel compresses
cross-name dispersion, which RAISES phase-book correlation and therefore SHRINKS the gap
between CANON and FPORT -- the bias pushes DDC toward zero and so works AGAINST H_SIGN and
H_SIZE, not for them.  The 4b comparands are read against SPY, which is not survivorship-
inflated.

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
REF999 = OUT / "2026-09-16_is-the-TRANCHE-LIFT-a-FUNCTION-of-PHASE-BOOK-CORRELATION_C"

WARM = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
VOLCAP, BAND0, BAND1 = 0.60, 0.03, 0.06
GROSS = 0.75
RUNGS = [0.0, 10.0, 25.0]
HEAD_COST = 10.0
CADS = [("D", 1), ("W", 5), ("M", 21), ("Q", 63)]
SEED0 = 975                      # 999/975-B's seed base, kept so G7 can replay their draws
CONVS = ["ROTP", "ROT"]
LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
LEGNAME = {"H1": "L1_H1", "H2": "L2_H2", "OOS": "L3_OOS", "DD": "L4_DD", "CAGR": "L5_CAGR"}

# pre-registered bars
SIZE_BAR = 0.50        # pp, H_SIZE
MATCH_BAR = 0.70       # share of cells, H_MATCH
PAIRED_BAR = 0.30      # pp, H_PAIRED
RANK_BAR = 0.50        # Spearman, H_RANK
# 999's published headline, for G8
G8_MEAN, G8_MEDIAN, G8_POS = 0.84, 0.91, 23

NDRAW_WIDE = 40
SMOKE = bool(int(os.environ.get("IDEA1006_SMOKE", "0")))
LINES: list[str] = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix, gz=False):
    p = OUT / (f"{STEM}.{suffix}.csv.gz" if gz else f"{STEM}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ==========================================================================================
# (1) phase machinery -- VERBATIM from ideas 938/942/962/964/975/999 so this run NESTS
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
    """Fast runner -- byte-identical to 942/962/964/975/999's.  G1 asserts it against engine."""

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


# ---- the 4b alphabets (999/975/964/942's, verbatim) --------------------------------------
def legs_rec_v(df):
    return dict(H1=df["H1"] > df["spy_H1"], H2=df["H2"] > df["spy_H2"],
                OOS=df["OOS_Sharpe"] > df["spy_OOS_Sharpe"],
                DD=df["OOS_MaxDD"].abs() <= 0.60 * df["spy_MaxDD"].abs(),
                CAGR=df["OOS_CAGR"] >= 0.70 * df["spy_CAGR"])


def legs_is_v(df):
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
    li = legs_is_v(df)
    df["pass4b_IS"] = np.logical_and.reduce([li[k].values for k in LEGS])
    df["IS_legs_passed"] = np.sum([li[k].values.astype(int) for k in LEGS], axis=0)
    return df


# ==========================================================================================
# (2) THE BOOK SET -- 999's five (REC5) plus four new width / band rungs (WIDE4)
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
    "TOP5":   lambda p, g: ranked_book(p, g, 5),
    "TOP30":  lambda p, g: ranked_book(p, g, 30),
    "TOP60":  lambda p, g: ranked_book(p, g, 60),
    "BAND06": lambda p, g: band_book(p, BAND1, g),
}
REC5 = ["EWELIG", "BAND03", "TOP20", "TOP10", "TOP40"]      # 999's, seeds 0..4
WIDE4 = ["TOP5", "TOP30", "TOP60", "BAND06"]                # new, seeds 5..8
BOOKSETS = {"REC5": REC5, "WIDE4": WIDE4, "POOLED9": REC5 + WIDE4}
POOLKIND = {"EWELIG": "EW", "BAND03": "BD", "BAND06": "BD",
            "TOP20": "ROT", "TOP10": "ROT", "TOP40": "ROT",
            "TOP5": "ROT", "TOP30": "ROT", "TOP60": "ROT"}
BOOKSEED = {"EWELIG": 0, "BAND03": 1, "TOP20": 2, "TOP10": 3, "TOP40": 4,
            "TOP5": 5, "TOP30": 6, "TOP60": 7, "BAND06": 8}


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
    """One coin-flip weight matrix, ALREADY in ctx's shifted coordinates.  975/999's verbatim."""
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


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3:
        return np.nan
    ra = pd.Series(a[ok]).rank().values
    rb = pd.Series(b[ok]).rank().values
    return float(np.corrcoef(ra, rb)[0, 1])


# ==========================================================================================
# (3) GATES
# ==========================================================================================
def gates(px):
    P("=" * 100)
    P("(A) PRE-REGISTERED GATES -- printed before any result number is read")
    P("=" * 100)
    gk, rows = {}, []
    idx = px.index

    bad = 0
    for per in ("W", "M", "Q"):
        a, _ = offset_mask(idx, per, 0)
        b = engine.rebalance_mask(idx, per)
        bad += int((a.values != b.values).sum())
    gk["G0"] = bad == 0
    rows.append(("G0", "offset_mask(.,per,0) == engine.rebalance_mask on W/M/Q",
                 f"{bad} disagreeing rows", "0", gk["G0"]))

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

    d2 = float(np.abs(band_book(px, BAND0, GROSS).values
                      - rules_v2_weights(px, BAND0, GROSS).values).max())
    gk["G2"] = d2 == 0.0
    rows.append(("G2", "band_book(0.03,0.75) == baseline.rules_v2_weights",
                 f"max|d| {d2:.3e}", "0.0", gk["G2"]))

    # G3 -- tranche identity: FPORT over the ONE-phase D family == that phase's CANON
    ctxd = Ctx(px, offset_mask(idx, "D", 0)[0])
    gd, td = ctxd.run(ctxd.shift(W))
    fport_d = (gd - td * HEAD_COST / 1e4) / 1.0
    canon_d = gd - td * HEAD_COST / 1e4
    d3 = float(np.abs(fport_d - canon_d).max())
    gk["G3"] = d3 < 1e-12
    rows.append(("G3", "TRANCHE IDENTITY: FPORT over a 1-phase family == that phase's CANON",
                 f"max|d| {d3:.3e}", "1e-12", gk["G3"]))

    c1 = Ctx(px, offset_mask(idx, "Q", 3)[0])
    a1, _ = c1.run(c1.shift(W))
    c2 = Ctx(px, offset_mask(idx, "Q", 3)[0])
    a2, _ = c2.run(c2.shift(W))
    d4 = float(np.abs(a1 - a2).max())
    gk["G4"] = d4 == 0.0
    rows.append(("G4", "determinism: a rebuilt cell reproduces its own stream exactly",
                 f"max|d| {d4:.3e}", "0.0", gk["G4"]))

    ctx = Ctx(px, offset_mask(idx, "M", 0)[0])
    wt = ctx.shift(W)
    Wn, cnt, take = null_weights(ctx, pools(px)["ROT"], wt, "ROTP", 999, period_id(idx, "M"))
    dc = int(np.abs((Wn[ctx.reb] > 0).sum(axis=1) - take).max())
    dg = float(np.abs(Wn[ctx.reb].sum(axis=1) - wt[ctx.reb].sum(axis=1)).max())
    gk["G5"] = dc == 0 and dg < 1e-12
    rows.append(("G5", "GROSS MATCH: null count and gross == book's, row by row",
                 f"dcount {dc}  dgross {dg:.3e}", "0 / 1e-12", gk["G5"]))

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
    P("(B) THE GRID -- REAL books, both estimators, plus WIDE4's own nulls")
    P("=" * 100)
    t0 = time.time()
    real_rows, null_rows, BASE, SPYALL = [], [], {}, {}
    cads = [(p, n) for p, n in CADS] if not SMOKE else [("D", 1), ("W", 5)]

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
        SPYALL[pname] = SPYC
        P(f"  {pname}: SPY full {ms['CAGR']:.2%}/{ms['Sharpe']:.4f}/{ms['MaxDD']:.2%}   "
          f"OOS {ms_o['CAGR']:.2%}/{ms_o['Sharpe']:.4f}/{ms_o['MaxDD']:.2%}   "
          f"4b DD cap {0.60 * abs(ms['MaxDD']):.2%}  CAGR floor {0.70 * ms['CAGR']:.2%}")

        bc = Ctx(px, offset_mask(idx, "W", 0)[0])
        bgr, btn = bc.run(bc.shift(rules_v2_weights(px, BAND0, GROSS)))
        for c in RUNGS:
            br = (bgr - btn * c / 1e4)[WARM:]
            BASE[(pname, c)] = mets(br[oos]) | {"full": mets(br)}
        del bc

        PL = pools(px)
        Wt = {b: BOOKS[b](px, GROSS) for b in BOOKS}
        ndraw = 3 if SMOKE else NDRAW_WIDE

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
            r_ph0 = {}
            nacc = {(b, d): [np.zeros(len(spy)), np.zeros(len(spy))]
                    for b in WIDE4 for d in range(ndraw)}
            n_ph0 = {}
            for ph in range(nph):
                ctx = Ctx(px, offset_mask(idx, per, ph)[0])
                for b, W in Wt.items():
                    wt = ctx.shift(W)
                    g_, t_ = ctx.run(wt)
                    gw, tw = g_[WARM:], t_[WARM:]
                    racc[b][0] += gw
                    racc[b][1] += tw
                    if ph == 0:
                        r_ph0[b] = (gw.copy(), tw.copy())
                    if b in WIDE4:
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
                g0, t0_ = r_ph0[b]
                for c in RUNGS:
                    emit(real_rows, (G - T_ * c / 1e4) / float(nph), book=b, cadence=per,
                         estimator="FPORT", cost_bps=c, n_phase=nph,
                         turn_per_yr=float(T_.sum() / nph / (len(spy) / 252.0)))
                    emit(real_rows, g0 - t0_ * c / 1e4, book=b, cadence=per,
                         estimator="CANON", cost_bps=c, n_phase=1,
                         turn_per_yr=float(t0_.sum() / (len(spy) / 252.0)))
            for (b, d), (G, T_) in nacc.items():
                g0, t0_ = n_ph0[(b, d)]
                for c in RUNGS:
                    emit(null_rows, (G - T_ * c / 1e4) / float(nph), book=b, cadence=per,
                         estimator="FPORT", draw=d, cost_bps=c, n_phase=nph,
                         turn_per_yr=float(T_.sum() / nph / (len(spy) / 252.0)))
                    emit(null_rows, g0 - t0_ * c / 1e4, book=b, cadence=per,
                         estimator="CANON", draw=d, cost_bps=c, n_phase=1,
                         turn_per_yr=float(t0_.sum() / (len(spy) / 252.0)))
            del racc, nacc, r_ph0, n_ph0
        P(f"  panel {pname} done  ({time.time() - t0:.0f}s)")

    real = add_legs(pd.DataFrame(real_rows))
    nullw = add_legs(pd.DataFrame(null_rows))
    for df in (real, nullw):
        df["pass4a"] = [bool(r.OOS_H1 > BASE[(r.panel, r.cost_bps)]["H1"]
                             and r.OOS_H2 > BASE[(r.panel, r.cost_bps)]["H2"]
                             and r.OOS_MaxDD >= BASE[(r.panel, r.cost_bps)]["MaxDD"])
                        for r in df.itertuples()]
    dump(real, "real")
    dump(nullw, "nulls_wide", gz=True)
    P(f"  grid built in {time.time() - t0:.0f}s   REAL {len(real):,} rows   "
      f"WIDE4 NULL {len(nullw):,} rows")
    return real, nullw, BASE, SPYALL


# ==========================================================================================
# (5) CROSS-RUN GATES G6 / G7 / G8 -- against idea 999's committed artefacts
# ==========================================================================================
def ddc_frame(df, keys):
    """|OOS MaxDD(CANON)| - |OOS MaxDD(FPORT)| in pp, per cell."""
    piv = df.pivot_table(index=keys, columns="estimator", values="OOS_MaxDD", aggfunc="mean")
    out = (piv["CANON"].abs() - piv["FPORT"].abs()) * 100.0
    return out.rename("DDC_pp").reset_index()


def crossrun(real, panels, gk, rows):
    P()
    P("=" * 100)
    P("(C) CROSS-RUN GATES -- idea 999's committed artefacts, replayed")
    P("=" * 100)

    # ---- G6: 999's committed .real.csv reproduced row for row on the shared books ---------
    p6 = Path(str(REF999) + ".real.csv")
    d6, n6 = np.nan, 0
    if p6.exists():
        ref = pd.read_csv(p6)
        K = ["panel", "book", "cadence", "estimator", "cost_bps"]
        cols = ["OOS_MaxDD", "OOS_Sharpe", "OOS_CAGR", "Sharpe", "MaxDD", "H1", "H2"]
        m = ref.merge(real, on=K, suffixes=("_ref", "_mine"))
        m = m[m.book.isin(REC5)]
        n6 = len(m)
        d6 = float(max(np.abs(m[c + "_ref"].values - m[c + "_mine"].values).max() for c in cols))
        gk["G6"] = n6 > 0 and d6 < 1e-10
    else:
        gk["G6"] = False
    rows.append(("G6", "CROSS-RUN: 999's committed .real.csv reproduced on shared rows",
                 f"{n6} rows, max|d| {d6:.3e}", "1e-10", gk["G6"]))

    # ---- G7: replay 999's own null draws on a pre-declared subsample ----------------------
    p7 = Path(str(REF999) + ".nulls.csv.gz")
    SUB = [("U56", "TOP20", "M"), ("U56", "EWELIG", "Q"), ("B136", "TOP40", "W")]
    d7, n7 = np.nan, 0
    if p7.exists():
        ref = pd.read_csv(p7)
        worst, cnt = 0.0, 0
        for pname, b, per in SUB:
            px = panels[pname]
            idx = px.index
            oos = np.asarray(idx >= pd.Timestamp(OOS_START))[WARM:]
            nph = dict(CADS)[per]
            PLp = pools(px)
            W = BOOKS[b](px, GROSS)
            pid = period_id(idx, per)
            nd = 5 if not SMOKE else 2
            acc = {d: [np.zeros(int(oos.size)), np.zeros(int(oos.size))] for d in range(nd)}
            ph0 = {}
            for ph in range(nph):
                ctx = Ctx(px, offset_mask(idx, per, ph)[0])
                wt = ctx.shift(W)
                for d in range(nd):
                    seed = (SEED0 + 1_000_000 * BOOKSEED[b]
                            + 100_000 * CONVS.index("ROTP") + 1_000 * d + ph)
                    Wn, _, _ = null_weights(ctx, PLp[POOLKIND[b]], wt, "ROTP", seed, pid)
                    gn, tn = ctx.run(Wn)
                    acc[d][0] += gn[WARM:]
                    acc[d][1] += tn[WARM:]
                    if ph == 0:
                        ph0[d] = (gn[WARM:].copy(), tn[WARM:].copy())
                del ctx
            sub = ref[(ref.panel == pname) & (ref.book == b) & (ref.cadence == per)
                      & (ref.cost_bps == HEAD_COST)]
            for d in range(nd):
                G, T_ = acc[d]
                rf = (G - T_ * HEAD_COST / 1e4) / float(nph)
                rc = ph0[d][0] - ph0[d][1] * HEAD_COST / 1e4
                for est, r in (("FPORT", rf), ("CANON", rc)):
                    rr = sub[(sub.estimator == est) & (sub.draw == d)]
                    if not len(rr):
                        continue
                    mo = mets(r[oos])
                    worst = max(worst, abs(mo["MaxDD"] - float(rr.OOS_MaxDD.iloc[0])),
                                abs(mo["Sharpe"] - float(rr.OOS_Sharpe.iloc[0])))
                    cnt += 1
        d7, n7 = worst, cnt
        gk["G7"] = cnt > 0 and worst < 1e-10
    else:
        gk["G7"] = False
    rows.append(("G7", "CROSS-RUN: 999's committed null draws replayed (3 declared cells)",
                 f"{n7} rows, max|d| {d7:.3e}", "1e-10", gk["G7"]))

    # ---- G8: 999's PUBLISHED HEADLINE recomputed from its own committed nulls -------------
    nullmed = None
    if p7.exists():
        ref = pd.read_csv(p7)
        r10 = ref[ref.cost_bps == HEAD_COST]
        # 999's OWN convention (its med_OOS_MaxDD_C / _F columns): DIFFERENCE OF THE CELL'S
        # MEDIANS, not the median of the paired per-draw differences.  Both are reported.
        g = r10.groupby(["panel", "book", "cadence", "estimator"]).OOS_MaxDD.median()
        g = g.unstack("estimator")
        cellmed = ((g["CANON"].abs() - g["FPORT"].abs()) * 100.0).rename("DDC_pp")
        piv = r10.pivot_table(index=["panel", "book", "cadence", "draw"],
                              columns="estimator", values="OOS_MaxDD")
        paired = (((piv["CANON"].abs() - piv["FPORT"].abs()) * 100.0)
                  .groupby(level=[0, 1, 2]).median().rename("DDC_paired_pp"))
        wmq = cellmed[cellmed.index.get_level_values(2) != "D"]
        gm, gmed, gpos = float(wmq.mean()), float(wmq.median()), int((wmq > 0).sum())
        wp = paired[paired.index.get_level_values(2) != "D"]
        ok = (abs(gm - G8_MEAN) <= 0.01 and abs(gmed - G8_MEDIAN) <= 0.01
              and gpos == G8_POS and len(wmq) == 30)
        gk["G8"] = ok
        rows.append(("G8", "999's HEADLINE recomputed from its own committed nulls "
                           "(mean/median/positive over 30 W/M/Q cells)",
                     f"mean {gm:+.2f} pp (pub {G8_MEAN:+.2f}), median {gmed:+.2f} pp "
                     f"(pub {G8_MEDIAN:+.2f}), positive {gpos} of {len(wmq)} (pub {G8_POS}); "
                     f"paired-difference reading of the same cells "
                     f"{float(wp.mean()):+.2f} / {float(wp.median()):+.2f} pp",
                     "0.01 pp / exact", ok))
        nullmed = cellmed.reset_index().rename(columns={"DDC_pp": "NULL_DDC_pp"})
        nullmed = nullmed.merge(paired.reset_index(), on=["panel", "book", "cadence"])
        nullmed["ndraw"] = nullmed.panel.map({"U56": 100, "B136": 60})
    else:
        gk["G8"] = False
        rows.append(("G8", "999's HEADLINE recomputed from its own committed nulls",
                     "artefact missing", "0.01 pp / exact", False))

    for g, what, got, bar, ok in rows[-3:]:
        P(f"  {g}  {'PASS' if ok else 'FAIL'}  {what}")
        P(f"        got {got}   bar {bar}")
    return nullmed


# ==========================================================================================
# (6) THE ANSWER
# ==========================================================================================
def answer(real, nullw, nullmed, BASE, SPYALL, gk):
    H = {}
    P()
    P("=" * 100)
    P("(D) THE OBJECT -- DDC = |OOS MaxDD(CANON)| - |OOS MaxDD(FPORT)|, in pp; + = compression")
    P("=" * 100)

    # ---- REAL DDC, every cell, every cost rung -------------------------------------------
    rd = ddc_frame(real, ["panel", "book", "cadence", "cost_bps"])
    dump(rd, "real_ddc")
    head = rd[rd.cost_bps == HEAD_COST].copy()

    # H_D: the structural boundary
    dcells = head[head.cadence == "D"]
    H["H_D"] = bool(np.abs(dcells.DDC_pp.values).max() < 1e-10)
    P(f"  H_D  {'PASS' if H['H_D'] else 'FAIL'}  D has ONE phase -> FPORT == CANON; "
      f"max|DDC| over {len(dcells)} D cells = {np.abs(dcells.DDC_pp.values).max():.3e} pp")

    wmq = head[head.cadence != "D"].copy()
    wmq["bookset"] = np.where(wmq.book.isin(REC5), "REC5", "WIDE4")

    P()
    P("  (D1) REAL DDC per cell at 10 bps, W/M/Q  (pp; + = the TRANCHE takes LESS drawdown)")
    P("       panel  book      cad    CANON OOS MaxDD   FPORT OOS MaxDD     DDC      NULL med DDC")
    piv = real[real.cost_bps == HEAD_COST].pivot_table(
        index=["panel", "book", "cadence"], columns="estimator", values="OOS_MaxDD")
    nm = (nullmed.set_index(["panel", "book", "cadence"])["NULL_DDC_pp"]
          if nullmed is not None else pd.Series(dtype=float))
    nw = None
    if len(nullw):
        gw = nullw[nullw.cost_bps == HEAD_COST].groupby(
            ["panel", "book", "cadence", "estimator"]).OOS_MaxDD.median().unstack("estimator")
        nw = (gw["CANON"].abs() - gw["FPORT"].abs()) * 100.0
    recs = []
    for pn in ("U56", "B136"):
        for b in REC5 + WIDE4:
            for cd in ("W", "M", "Q"):
                key = (pn, b, cd)
                if key not in piv.index:
                    continue
                c_, f_ = float(piv.loc[key, "CANON"]), float(piv.loc[key, "FPORT"])
                d_ = (abs(c_) - abs(f_)) * 100.0
                n_ = float(nm.get(key, np.nan)) if len(nm) else np.nan
                if not np.isfinite(n_) and nw is not None and key in nw.index:
                    n_ = float(nw.loc[key])
                nd_ = 100 if pn == "U56" else 60
                if b in WIDE4:
                    nd_ = NDRAW_WIDE
                recs.append(dict(panel=pn, book=b, cadence=cd,
                                 bookset="REC5" if b in REC5 else "WIDE4",
                                 CANON_OOS_MaxDD=c_, FPORT_OOS_MaxDD=f_,
                                 REAL_DDC_pp=d_, NULL_DDC_pp=n_, null_ndraw=nd_,
                                 GAP_pp=d_ - n_))
                P(f"       {pn:5s}  {b:8s}  {cd:3s}    {c_:11.2%}      {f_:11.2%}   "
                  f"{d_:+7.2f}     {n_:+7.2f}  (n={nd_})")
    C = pd.DataFrame(recs)
    dump(C, "cells")

    # ---- the two tuned axes, all 12 points ----------------------------------------------
    P()
    P("  (D2) THE TWO TUNED AXES -- all 12 grid points reported, none selected")
    P("       bookset  cad   cells   REAL med DDC   REAL mean   REAL >0    NULL med DDC   "
      "paired med gap")
    grid = []
    for bs, books in BOOKSETS.items():
        for cd in ("D", "W", "M", "Q"):
            if cd == "D":
                sub = head[(head.cadence == "D") & (head.book.isin(books))]
                rm = float(sub.DDC_pp.median()) if len(sub) else np.nan
                rmean = float(sub.DDC_pp.mean()) if len(sub) else np.nan
                npos, n = int((sub.DDC_pp > 1e-12).sum()), len(sub)
                nmed, gap = 0.0, 0.0
            else:
                sub = C[(C.cadence == cd) & (C.book.isin(books))]
                rm, rmean = float(sub.REAL_DDC_pp.median()), float(sub.REAL_DDC_pp.mean())
                npos, n = int((sub.REAL_DDC_pp > 0).sum()), len(sub)
                nmed = float(sub.NULL_DDC_pp.median())
                gap = float(sub.GAP_pp.median())
            grid.append(dict(bookset=bs, cadence=cd, cells=n, real_med=rm, real_mean=rmean,
                             real_pos=npos, null_med=nmed, paired_med_gap=gap))
            P(f"       {bs:7s}  {cd:3s}   {n:5d}   {rm:+10.2f}   {rmean:+9.2f}   "
              f"{npos:2d}/{n:<2d}    {nmed:+10.2f}    {gap:+10.2f}")
    G = pd.DataFrame(grid)
    dump(G, "grid")

    # ---- the pre-registered hypotheses ---------------------------------------------------
    P()
    P("=" * 100)
    P("(E) PRE-REGISTERED HYPOTHESES")
    P("=" * 100)
    pooled = C  # all 9 books x W/M/Q x 2 panels
    rec = C[C.bookset == "REC5"]

    med_all = float(pooled.REAL_DDC_pp.median())
    med_rec = float(rec.REAL_DDC_pp.median())
    H["H_SIGN"] = med_all > 0
    P(f"  H_SIGN    {'PASS' if H['H_SIGN'] else 'FAIL'}  median REAL DDC over "
      f"{len(pooled)} pooled W/M/Q cells = {med_all:+.2f} pp "
      f"(REC5 alone {med_rec:+.2f} pp over {len(rec)} cells)   bar > 0")

    H["H_SIZE"] = med_all >= SIZE_BAR
    P(f"  H_SIZE    {'PASS' if H['H_SIZE'] else 'FAIL'}  the same median {med_all:+.2f} pp "
      f"against the null's published {G8_MEDIAN:+.2f} pp   bar >= {SIZE_BAR:+.2f} pp")

    ok = pooled[np.isfinite(pooled.NULL_DDC_pp)]
    agree = float((np.sign(ok.REAL_DDC_pp) == np.sign(ok.NULL_DDC_pp)).mean())
    okr = rec[np.isfinite(rec.NULL_DDC_pp)]
    agree_r = float((np.sign(okr.REAL_DDC_pp) == np.sign(okr.NULL_DDC_pp)).mean())
    H["H_MATCH"] = agree >= MATCH_BAR
    P(f"  H_MATCH   {'PASS' if H['H_MATCH'] else 'FAIL'}  REAL and NULL DDC agree in SIGN in "
      f"{agree:.1%} of {len(ok)} cells (REC5's own 30: {agree_r:.1%})   bar >= {MATCH_BAR:.0%}")

    pg = float(ok.GAP_pp.median())
    pg_r = float(okr.GAP_pp.median())
    H["H_PAIRED"] = abs(pg) <= PAIRED_BAR
    P(f"  H_PAIRED  {'PASS' if H['H_PAIRED'] else 'FAIL'}  median (REAL - NULL) DDC = "
      f"{pg:+.2f} pp (REC5's 30: {pg_r:+.2f})   bar |.| <= {PAIRED_BAR:.2f} pp")

    sp = spearman(ok.NULL_DDC_pp.values, ok.REAL_DDC_pp.values)
    sp_r = spearman(okr.NULL_DDC_pp.values, okr.REAL_DDC_pp.values)
    H["H_RANK"] = np.isfinite(sp) and sp >= RANK_BAR
    P(f"  H_RANK    {'PASS' if H['H_RANK'] else 'FAIL'}  Spearman(NULL DDC, REAL DDC) = "
      f"{sp:+.4f} over {len(ok)} cells (REC5's 30: {sp_r:+.4f})   bar >= {RANK_BAR:+.2f}")

    cads_med = {cd: float(C[C.cadence == cd].REAL_DDC_pp.median()) for cd in ("W", "M", "Q")}
    H["H_CAD"] = len({np.sign(v) for v in cads_med.values()}) == 1
    P(f"  H_CAD     {'PASS' if H['H_CAD'] else 'FAIL'}  median REAL DDC by cadence  "
      + "  ".join(f"{k} {v:+.2f}" for k, v in cads_med.items()) + "   bar: one sign")

    cost_med = {}
    for c in RUNGS:
        s = rd[(rd.cost_bps == c) & (rd.cadence != "D")]
        cost_med[c] = float(s.DDC_pp.median())
    H["H_COST"] = len({np.sign(v) for v in cost_med.values()}) == 1
    P(f"  H_COST    {'PASS' if H['H_COST'] else 'FAIL'}  median REAL DDC by cost rung  "
      + "  ".join(f"{int(k)}bps {v:+.2f}" for k, v in cost_med.items()) + "   bar: one sign")

    # H_4bCONV -- does the real compression actually FLIP the L4_DD leg anywhere?
    r10 = real[real.cost_bps == HEAD_COST]
    flips, conv = [], 0
    for (pn, b, cd), g in r10.groupby(["panel", "book", "cadence"]):
        if cd == "D":
            continue
        f = g[g.estimator == "FPORT"].iloc[0]
        k = g[g.estimator == "CANON"].iloc[0]
        cap = 0.60 * abs(f.spy_MaxDD)
        flip = bool(f.leg_L4_DD and not k.leg_L4_DD)
        if flip:
            conv += 1
        flips.append(dict(panel=pn, book=b, cadence=cd, cap=-cap,
                          CANON_OOS_MaxDD=k.OOS_MaxDD, FPORT_OOS_MaxDD=f.OOS_MaxDD,
                          CANON_L4=bool(k.leg_L4_DD), FPORT_L4=bool(f.leg_L4_DD),
                          L4_FLIP=flip, CANON_pass4b=bool(k.pass4b),
                          FPORT_pass4b=bool(f.pass4b),
                          CANON_fail=k.fail4b, FPORT_fail=f.fail4b,
                          CANON_pass4a=bool(k.pass4a), FPORT_pass4a=bool(f.pass4a)))
    F = pd.DataFrame(flips)
    dump(F, "legflips")
    H["H_4bCONV"] = conv >= 1
    P(f"  H_4bCONV  {'PASS' if H['H_4bCONV'] else 'FAIL'}  L4_DD flips CANON-fail -> "
      f"FPORT-pass in {conv} of {len(F)} REAL W/M/Q cells   bar >= 1")
    P(f"            REAL 4b at 10 bps: CANON {int(F.CANON_pass4b.sum())} of {len(F)}, "
      f"FPORT (tranche) {int(F.FPORT_pass4b.sum())} of {len(F)};  "
      f"4a: CANON {int(F.CANON_pass4a.sum())}, FPORT {int(F.FPORT_pass4a.sum())}")
    if conv:
        for r in F[F.L4_FLIP].itertuples():
            P(f"            FLIP  {r.panel}/{r.book}/{r.cadence}  "
              f"{r.CANON_OOS_MaxDD:.2%} -> {r.FPORT_OOS_MaxDD:.2%} against cap {r.cap:.2%}; "
              f"4b CANON {r.CANON_pass4b} ({r.CANON_fail}) -> FPORT {r.FPORT_pass4b} "
              f"({r.FPORT_fail})")
    return H, C, F, rd


# ==========================================================================================
# (7) RULE 8 -- walk-forward: choose on 2009-2016 ALONE, read 2017-2026 ONCE
# ==========================================================================================
def rule8(real, BASE, H):
    P()
    P("=" * 100)
    P("(F) PROTOCOL RULE 8 -- (book, cadence) chosen on 2009-2016 ALONE, OOS read ONCE")
    P("=" * 100)
    rows = []
    CH = {
        "C_ISSHARPE": lambda g: g.IS_Sharpe.idxmax(),
        "C_ISDD":     lambda g: g.IS_MaxDD.idxmax(),          # smallest |IS MaxDD|
        "C_ISDDC":    lambda g: g.IS_DDC_pp.idxmax(),         # THIS run's own statistic
        "C_IS4B":     lambda g: g.sort_values(["pass4b_IS", "IS_legs_passed", "IS_Sharpe"],
                                              ascending=False).index[0],
    }
    for c in RUNGS:
        sub = real[(real.cost_bps == c) & (real.cadence != "D")].copy()
        isddc = sub.pivot_table(index=["panel", "book", "cadence"],
                                columns="estimator", values="IS_MaxDD")
        isddc = ((isddc["CANON"].abs() - isddc["FPORT"].abs()) * 100.0).rename("IS_DDC_pp")
        sub = sub.merge(isddc.reset_index(), on=["panel", "book", "cadence"], how="left")
        for est in ("FPORT", "CANON"):
            s = sub[sub.estimator == est].reset_index(drop=True)
            for pn, g in s.groupby("panel"):
                for cname, fn in CH.items():
                    i = fn(g)
                    r = g.loc[i]
                    b = BASE[(pn, c)]
                    rows.append(dict(cost_bps=c, estimator=est, panel=pn, chooser=cname,
                                     pick_book=r.book, pick_cadence=r.cadence,
                                     OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe,
                                     OOS_MaxDD=r.OOS_MaxDD, OOS_H1=r.OOS_H1, OOS_H2=r.OOS_H2,
                                     pass4b=bool(r.pass4b), fail4b=r.fail4b,
                                     pass4a=bool(r.pass4a),
                                     spy_OOS_CAGR=r.spy_OOS_CAGR,
                                     spy_OOS_Sharpe=r.spy_OOS_Sharpe,
                                     spy_OOS_MaxDD=r.spy_OOS_MaxDD,
                                     base_OOS_CAGR=b["CAGR"], base_OOS_Sharpe=b["Sharpe"],
                                     base_OOS_MaxDD=b["MaxDD"]))
    W = pd.DataFrame(rows)
    dump(W, "walkforward")
    P("   cost  est    panel  chooser      pick            OOS CAGR / Sharpe / MaxDD      "
      "4b   4a   binding")
    for r in W[W.cost_bps == HEAD_COST].itertuples():
        P(f"   {int(r.cost_bps):3d}   {r.estimator:5s}  {r.panel:5s}  {r.chooser:11s}  "
          f"{r.pick_book + '/' + r.pick_cadence:14s}  "
          f"{r.OOS_CAGR:7.2%} / {r.OOS_Sharpe:6.4f} / {r.OOS_MaxDD:7.2%}   "
          f"{'Y' if r.pass4b else 'n'}    {'Y' if r.pass4a else 'n'}   {r.fail4b}")
    f = W[W.estimator == "FPORT"]
    k = W[W.estimator == "CANON"]
    H["H_RULE8"] = bool(f.pass4b.sum() >= 1)
    P()
    P(f"  H_RULE8   {'PASS' if H['H_RULE8'] else 'FAIL'}  OOS 4b for the chosen TRANCHE: "
      f"{int(f.pass4b.sum())} of {len(f)}  (CANON {int(k.pass4b.sum())} of {len(k)});  "
      f"OOS 4a FPORT {int(f.pass4a.sum())} of {len(f)}, CANON {int(k.pass4a.sum())}   bar >= 1")
    P(f"            median OOS across all picks: FPORT {f.OOS_CAGR.median():.2%} / "
      f"{f.OOS_Sharpe.median():.4f} / {f.OOS_MaxDD.median():.2%}    "
      f"CANON {k.OOS_CAGR.median():.2%} / {k.OOS_Sharpe.median():.4f} / "
      f"{k.OOS_MaxDD.median():.2%}")
    r0 = W.iloc[0]
    P(f"            comparands, same OOS window: SPY {r0.spy_OOS_CAGR:.2%} / "
      f"{r0.spy_OOS_Sharpe:.4f} / {r0.spy_OOS_MaxDD:.2%}")
    for pn in ("U56", "B136"):
        b = BASE[(pn, HEAD_COST)]
        P(f"            RULES v2 (live) on {pn:5s} OOS {b['CAGR']:.2%} / {b['Sharpe']:.4f} / "
          f"{b['MaxDD']:.2%}   full {b['full']['CAGR']:.2%} / {b['full']['Sharpe']:.4f} / "
          f"{b['full']['MaxDD']:.2%}")
    return W


def main():
    t0 = time.time()
    P("#" * 100)
    P("# Idea 1006 -- is the TRANCHE a DRAWDOWN COMPRESSOR on the REAL books at the same")
    P("#              +0.84 pp it gives the NULL?   (cloud lane, 2026-09-16)")
    P("#" * 100)
    P(__doc__)

    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    for k, v in panels.items():
        P(f"  panel {k}: {v.shape[1]} columns, {len(v)} rows, "
          f"{v.index[0].date()} .. {v.index[-1].date()}")

    gk, grows = gates(panels["U56"])
    real, nullw, BASE, SPYALL = build(panels)
    nullmed = crossrun(real, panels, gk, grows)
    H, C, F, rd = answer(real, nullw, nullmed, BASE, SPYALL, gk)
    W = rule8(real, BASE, H)

    P()
    P("=" * 100)
    P("(G) SUMMARY")
    P("=" * 100)
    P(f"  GATES      {sum(gk.values())} of {len(gk)} pass  "
      + "  ".join(f"{g}:{'P' if v else 'F'}" for g, v in gk.items()))
    P(f"  HYPOTHESES {sum(H.values())} of {len(H)} pass  "
      + "  ".join(f"{h}:{'P' if v else 'F'}" for h, v in H.items()))
    pd.DataFrame([dict(gate=g, what=w, got=go, bar=b, passed=o)
                  for g, w, go, b, o in grows]).to_csv(OUT / f"{STEM}.gates.csv", index=False)
    pd.DataFrame([dict(hypothesis=k, passed=bool(v)) for k, v in H.items()]).to_csv(
        OUT / f"{STEM}.hypotheses.csv", index=False)
    P(f"  total {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()

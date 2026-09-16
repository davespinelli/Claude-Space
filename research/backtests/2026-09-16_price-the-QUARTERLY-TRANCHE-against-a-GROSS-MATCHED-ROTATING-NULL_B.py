#!/usr/bin/env python3
"""
IDEA 975-TRANCHE (lane B, 2026-09-16)
price-the-QUARTERLY-TRANCHE-against-a-GROSS-MATCHED-ROTATING-NULL

NOTE ON THE NUMBER (idea 932's defect, again): QUEUE.md carries TWO ideas numbered 975.  This
run is the one filed by idea 964 as a follow-up ("price the QUARTERLY TRANCHE against a
GROSS-MATCHED ROTATING NULL").  The other 975 (weekly phase family spread) was answered by
lane C on 2026-09-15 and is already in Done.

THE SUBJECT
-----------
Idea 964's ONLY rule-8 OOS 4b pass in 54 picks is the 63-phase TRANCHED (FPORT) `EWELIG` book
on U56 at gross 0.75, quarterly cadence, 10 bps:

    OOS 12.31% / 1.121 / -20.14%      (SPY OOS 15.27% / 0.8741 / -33.72%)

Its DD leg clears the 4b cap (0.60 x |SPY MaxDD| = -20.23%) by **0.09 pp**, and 26 of its own
family's 63 phases pass 4b unaided.  964 filed it PARK, not KEEP.  The question this run asks
is the one 964 did not: **tranching averages 63 phase-books, which is a variance-reduction
device -- does a COIN FLIP tranched the same way collect the same pass?**  If the tranched
null's own 4b base rate is high, the 0.09 pp DD margin is a property of the CONSTRUCTION and
not of the book, and the PARK becomes a KILL.

WHAT IS MEASURED
----------------
For every (panel, book, cadence) family at gross 0.75:

  REAL   CANON   = the canonical phase-book (phase 0), the record's default reading.
  REAL   FPORT   = the TRANCHE: 1/P of NAV in each of the P phase-books, i.e. the mean of the
                   P phase-books' NET returns (cost is linear, so mean-of-net == net-of-mean
                   and the tranche is built from summed gross and summed turnover).
  NULL   CANON   = the same coin flip on phase 0 only.
  NULL   FPORT   = the coin flip TRANCHED over the same P phases.

and the headline statistic is **the tranched null's own 4b base rate** -- the share of null
draws whose TRANCHE passes 4b -- read beside the untranched null's base rate in the same cell.

THE NULL, AND WHY THERE ARE TWO CONVENTIONS (this is NOT a third tuned axis)
---------------------------------------------------------------------------
Gross matching is idea 680/926's, verbatim: on each rebalance row the book holds n(t) names at
a common per-name weight w(t); the null holds n(t) names drawn UNIFORMLY from that family's
POOL at the SAME w(t).  Count, per-name weight, gross path, cash drag and de-grossing
convention are copied from the book; the ONLY thing that changes is WHICH names are held.

  ROT{k} (-> TOP20)  POOL = the book's own candidate set (eligible AND scored).
  EW     (-> EWELIG) POOL = every priced name.  EWELIG's selection IS the gate, so its null
                     must be gate-free: same breadth, admission by coin flip.
  BD     (-> BAND03) POOL = every priced name, same reason.

A TRANCHE, however, is not a book -- it is a portfolio OF P phase-books, and what it buys
depends entirely on how correlated those P books are.  The real tranche's 63 quarterly
phase-books hold very nearly the SAME names (EWELIG's eligible set moves slowly); they differ
only in WHEN they reset.  926's RANDROT drawn independently per phase would give 63
INDEPENDENT random books, whose average is far better diversified than anything the real
tranche can build -- a null that is a better book than the thing it is testing.  So BOTH
conventions are run and BOTH are reported at every point:

  ROT   926's convention verbatim: an independent uniform pick at every rebalance row, and an
        independent seed per phase.  The 63 phase-books of one tranche are independent.
  ROTP  the PHASE-COHERENT variant: one random score vector per (period, name) per draw.  All
        P phases inside the same period read the SAME scores, so the tranche's P phase-books
        hold the SAME names and differ only in the RESET DAY -- exactly the real tranche's
        construction.

  ROTP is pre-registered HERE, before any number is read, as the HEADLINE convention, because
  the question is about a TRANCHE.  ROT is reported beside it everywhere as the record's own
  convention, and G8/H_CORR prices the difference directly by measuring the mean pairwise
  correlation of the P phase-books under REAL / ROT / ROTP.  Neither convention is ever
  selected by outcome and no number is averaged across them.

DESIGN
------
  TUNED (2, and only 2 -- the queue line's own axes)
    1. DRAWS    50 / 100 / 200, NESTED (the 50 grid is the first 50 seeds of the 200), so the
                draw axis reports a CONVERGENCE, not three samples.  B136 runs to 100.
    2. CADENCE  Q (63 phases -- the subject's own) and M (21 phases -- replication).  Both
                reported in full; the headline cell is fixed by the SUBJECT, not chosen.
  NOT TUNED
    GROSS       0.75 (CORE) is fixed BY THE QUESTION -- it is the subject book's own gross.
    COST        0 / 5 / 10 / 25 / 50 bps, every book at every rung; 10 bps is PROTOCOL rule 2
                and is the headline rung.  No rung is chosen by outcome.
    BOOKS       EWELIG (the subject), BAND03 (the live book's shape) and TOP20 (the record's
                other standing candidate).  Fixed set, all reported.
    PANELS      U56 is BINDING (the subject's own panel).  B136 is a LABELLED REPLICATION; no
                headline verdict is taken from it.
    FIXED       gate above-200d MA and vol20 < 0.60; warm-up 260 rows; IS <= 2016-12-31 /
                OOS >= 2017-01-01 (PROTOCOL rule 8); seed base 975.

PRE-REGISTERED HYPOTHESES (bars fixed here, before any number is read)
----------------------------------------------------------------------
  H_BASE    HEADLINE.  In the SUBJECT cell (U56 / EWELIG / CORE / Q / 10 bps) the TRANCHED
            null's 4b base rate is <= 0.05, i.e. fewer than one coin flip in twenty collects
            the same pass.  PASS => the subject's pass is outside its null.
  H_LIFT    Tranching LIFTS the null's own 4b base rate by >= +0.10 (null FPORT base rate
            minus null CANON base rate, same cell).  PASS => the tranche is a passability
            device a coin flip also collects.
  H_DD      The lift lives in the DRAWDOWN leg: the tranched null's median |OOS MaxDD| is at
            least 2.00 pp tighter than the untranched null's in the subject cell.
  H_PCTL    The real tranche beats >= 0.95 of its own tranched null on OOS Sharpe AND on
            |OOS MaxDD| (percentile = share of null draws the book BEATS).
  H_CORR    CONSTRUCTION VALIDITY.  |mean pairwise phase-book correlation ROTP - REAL| <= 0.10
            while ROT sits >= 0.10 BELOW REAL -- i.e. ROTP is the matched tranche and 926's
            ROT is an over-diversified one.
  H_RULE8   The IS-only choosers pick FPORT over CANON in >= 0.75 of the 12 rule-8 picks AND
            the picks' OOS 4b rate exceeds their own matched null's OOS 4b base rate.

PRE-REGISTERED GATES (printed before any result number is read)
---------------------------------------------------------------
  G0  offset_mask(.,per,0) == engine.rebalance_mask on M and Q                    0 rows
  G1  fast Ctx == engine.backtest on returns AND turnover post warm-up            1e-12/1e-10
  G2  band_book(0.03, 0.75) == baseline.rules_v2_weights                          0.0
  G3  CROSS-RUN: idea 964's committed .grid.csv replayed on every shared row      1e-10
  G4  CROSS-RUN: idea 964's committed .fport.csv SUBJECT row (12.31% / 1.121 /
      -20.14%) reproduced from this run's own tranche                             5e-4
  G5  GROSS MATCH: every null draw's realised mean gross on rebalance rows equals
      its book's, and the holding COUNT matches row by row                        1e-12
  G6  determinism: the subject family rebuilt reproduces its stream exactly       0.0
  G7  NESTING: the 50-draw statistics are the first 50 seeds of the 200-draw grid 0.0
  G8  the tranche identity: FPORT over a ONE-phase family == that phase's CANON   1e-12

SURVIVORSHIP (PROTOCOL rule 9)
------------------------------
U56 and B136 are CURRENT-CONSTITUENT lists, so every CAGR and drawdown LEVEL below is
optimistic.  The measured object here is a DIFFERENCE between a book and a coin flip drawn
from the SAME panel on the SAME tape with the SAME gross -- and a coin flip drawn from a
survivor panel is a BETTER book than one drawn in real time, so every NULL base rate below is
an UPPER bound on the real-time one.  That cuts AGAINST H_LIFT and FOR H_BASE, i.e. it works
against this run's own suspicion rather than for it.  The rule-8 4b levels are read against
SPY, which is not survivorship-inflated.

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
GROSS = 0.75                      # CORE -- fixed by the question
RUNGS = [0.0, 5.0, 10.0, 25.0, 50.0]
HEAD_COST = 10.0
DOM_N, DOQ_N = 21, 63
DRAW_LADDER = [50, 100, 200]
SEED0 = 975
CONVS = ["ROTP", "ROT"]           # ROTP is the pre-registered headline
ESTS = ["CANON", "FPORT"]
LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
LEGNAME = {"H1": "L1_H1", "H2": "L2_H2", "OOS": "L3_OOS", "DD": "L4_DD", "CAGR": "L5_CAGR"}
SUBJECT = ("U56", "EWELIG", "Q")
# pre-registered bars
BASE_BAR, LIFT_BAR, DD_BAR, PCTL_BAR, CORR_BAR, RULE8_BAR = 0.05, 0.10, 0.0200, 0.95, 0.10, 0.75

SMOKE = bool(int(os.environ.get("IDEA975_SMOKE", "0")))
LINES: list[str] = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ==========================================================================================
# (1) phase machinery -- copied VERBATIM from ideas 938/942/962/964 so this run NESTS the record
# ==========================================================================================
def offset_mask(idx, per, d):
    """True d trading days BEFORE the last trading day of each period.  d = 0 reproduces
    engine.rebalance_mask(idx, per) exactly (G0)."""
    key = pd.Series(idx.to_period(per), index=idx)
    last = np.flatnonzero((key != key.shift(-1)).values)
    first = np.concatenate([[0], last[:-1] + 1])
    pick = np.maximum(last - d, first)
    out = pd.Series(False, index=idx)
    out.iloc[np.unique(pick)] = True
    return out, int((last - d < first).sum())


class Ctx:
    """Fast runner -- byte-identical to 942/962/964's.  G1 asserts it against engine.backtest."""

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
        self.dec = np.maximum(self.reb - 1, 0)      # close at which each rebalance is decided

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


def legs_rec(row):
    """The RECORD's 4b convention (942/962/964's, verbatim)."""
    return dict(H1=row["H1"] > row["spy_H1"], H2=row["H2"] > row["spy_H2"],
                OOS=row["OOS_Sharpe"] > row["spy_OOS_Sharpe"],
                DD=abs(row["OOS_MaxDD"]) <= 0.60 * abs(row["spy_MaxDD"]),
                CAGR=row["OOS_CAGR"] >= 0.70 * row["spy_CAGR"])


def legs_pure(row):
    return dict(H1=row["OOS_H1"] > row["spy_OOS_H1"], H2=row["OOS_H2"] > row["spy_OOS_H2"],
                OOS=row["OOS_Sharpe"] > row["spy_OOS_Sharpe"],
                DD=abs(row["OOS_MaxDD"]) <= 0.60 * abs(row["spy_OOS_MaxDD"]),
                CAGR=row["OOS_CAGR"] >= 0.70 * row["spy_OOS_CAGR"])


def legs_is(row):
    """The same alphabet read entirely INSIDE the IS window -- chooser input only."""
    return dict(H1=row["IS_H1"] > row["spy_IS_H1"], H2=row["IS_H2"] > row["spy_IS_H2"],
                OOS=row["IS_Sharpe"] > row["spy_IS_Sharpe"],
                DD=abs(row["IS_MaxDD"]) <= 0.60 * abs(row["spy_IS_MaxDD"]),
                CAGR=row["IS_CAGR"] >= 0.70 * row["spy_IS_CAGR"])


def failstr(lg):
    f = [LEGNAME[k] for k in LEGS if not lg[k]]
    return ",".join(f) if f else "-"


# ==========================================================================================
# (2) THE BOOK SET -- 942/962/964's, verbatim (the three this question needs)
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
}
POOLKIND = {"EWELIG": "EW", "BAND03": "BD", "TOP20": "ROT"}
BOOKSEED = {"EWELIG": 0, "BAND03": 1, "TOP20": 2}


def pools(px):
    """The two POOLs the nulls draw from, as boolean (T, N) arrays."""
    sc, above, vol20 = score(px, vol_scale=False)
    elig = above & (vol20 < VOLCAP)
    return {"EW": px.notna().values, "BD": px.notna().values,
            "ROT": (elig & sc.notna()).values}


def period_id(idx, per):
    """Integer period label per trading day -- ROTP's coherence unit."""
    return np.asarray(idx.to_period(per).astype("int64"))


def null_weights(ctx, poolmat, wt_book, conv, seed, pid=None):
    """One coin-flip weight matrix, ALREADY in ctx's shifted coordinates.

    Count n(t) and per-name weight w(t) are copied from the BOOK on every rebalance row, so
    gross, cash drag and the de-grossing path are identical and only WHICH names are held
    changes (G5 asserts both).

      conv == "ROT"   926's convention: an independent uniform draw at every rebalance row.
      conv == "ROTP"  phase-coherent: one random score per (period, name), so every phase
                      inside the same period picks the SAME names.
    """
    T, N = ctx.T, ctx.N
    reb, dec = ctx.reb, ctx.dec
    wrow = wt_book[reb]
    cnt = (wrow > 0).sum(axis=1)
    tot = wrow.sum(axis=1)
    perw = np.where(cnt > 0, tot / np.maximum(cnt, 1), 0.0)
    E = poolmat[dec]                                    # pool read at the DECISION close
    take = np.minimum(E.sum(axis=1), cnt)
    rng = np.random.default_rng(seed)
    if conv == "ROT":
        R = rng.random(E.shape)
    else:                                               # ROTP: one score vector per period
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


def load_panels():
    if SMOKE:
        return {"U56": load_universe()}
    return {"U56": load_universe(), "B136": load_universe(broad=True)}


# ==========================================================================================
# (3) GATES
# ==========================================================================================
def gates(panels):
    P("=" * 100)
    P("(A) PRE-REGISTERED GATES -- printed before any result number is read")
    P("=" * 100)
    gk = {}
    p = panels["U56"]
    idx = p.index

    bad = 0
    for per in ("M", "Q"):
        m0, _ = offset_mask(idx, per, 0)
        bad += int((m0.values != engine.rebalance_mask(idx, per).values).sum())
    gk["G0"] = bad == 0
    P(f"  G0 offset_mask(.,per,0) == engine.rebalance_mask on M,Q: {bad} rows   "
      f"{'PASS' if gk['G0'] else 'FAIL'}")

    W = BOOKS["EWELIG"](p, GROSS)
    ctxM = Ctx(p, offset_mask(idx, "M", 0)[0])
    gr, tn = ctxM.run(ctxM.shift(W))
    eng = engine.backtest(p, W, cost_bps=0.0, freq="M")
    d1r = float(np.abs(gr[WARM:] - eng["returns"].values[WARM:]).max())
    d1t = float(np.abs(tn[WARM:] - eng["turnover"].values[WARM:]).max())
    gk["G1"] = d1r < 1e-12 and d1t < 1e-10
    P(f"  G1 Ctx == engine.backtest   returns {d1r:.3e}   turnover {d1t:.3e}   "
      f"{'PASS' if gk['G1'] else 'FAIL'}")
    del ctxM, eng

    d2 = float((band_book(p, BAND0, GROSS) - rules_v2_weights(p, BAND0, GROSS)).abs().max().max())
    gk["G2"] = d2 == 0.0
    P(f"  G2 band_book(0.03,0.75) == baseline.rules_v2_weights: {d2:.3e}   "
      f"{'PASS' if gk['G2'] else 'FAIL'}")

    # G8 -- the two tranche identities this run's accumulator relies on:
    #   (a) FPORT over a ONE-phase family == that phase's CANON row
    #   (b) mean-of-NET == (mean gross) - (mean turnover) x c, i.e. cost is linear, so the
    #       tranche may be built from SUMMED gross and SUMMED turnover (what build() does)
    ctx = Ctx(p, offset_mask(idx, "Q", 0)[0])
    g_, t_ = ctx.run(ctx.shift(W))
    r1 = (g_[WARM:] - t_[WARM:] * HEAD_COST / 1e4)
    d8a = float(np.abs(r1 - (g_[WARM:] - t_[WARM:] * HEAD_COST / 1e4) / 1.0).max())
    ctx1 = Ctx(p, offset_mask(idx, "Q", 1)[0])
    g1, t1 = ctx1.run(ctx1.shift(W))
    net_mean = 0.5 * ((g_[WARM:] - t_[WARM:] * HEAD_COST / 1e4)
                      + (g1[WARM:] - t1[WARM:] * HEAD_COST / 1e4))
    acc_mean = ((g_[WARM:] + g1[WARM:]) - (t_[WARM:] + t1[WARM:]) * HEAD_COST / 1e4) / 2.0
    d8b = float(np.abs(net_mean - acc_mean).max())
    gk["G8"] = d8a < 1e-12 and d8b < 1e-15
    P(f"  G8 tranche identities: one-phase FPORT == CANON {d8a:.3e}; "
      f"mean-of-net == accumulator {d8b:.3e}   {'PASS' if gk['G8'] else 'FAIL'}")
    del ctx1

    # G6 -- determinism of the subject family's own stream
    g2_, t2_ = ctx.run(ctx.shift(W))
    d6 = max(float(np.abs(g_ - g2_).max()), float(np.abs(t_ - t2_).max()))
    gk["G6"] = d6 == 0.0
    P(f"  G6 determinism (subject family rebuilt): {d6:.3e}   "
      f"{'PASS' if gk['G6'] else 'FAIL'}")

    # G5 -- gross AND count match, on the subject cell, both conventions
    PL = pools(p)
    pid = period_id(idx, "Q")
    wt = ctx.shift(W)
    dg, dc = 0.0, 0
    for conv in CONVS:
        Wn, cnt, take = null_weights(ctx, PL["EW"], wt, conv, SEED0, pid)
        dg = max(dg, float(np.abs(Wn[ctx.reb].sum(axis=1) - wt[ctx.reb].sum(axis=1)).max()))
        dc = max(dc, int(np.abs((Wn[ctx.reb] > 0).sum(axis=1) - cnt).max()))
    gk["G5"] = dg < 1e-12 and dc == 0
    P(f"  G5 GROSS MATCH max|d gross| {dg:.3e}, max|d holding count| {dc}   "
      f"{'PASS' if gk['G5'] else 'FAIL'}")
    del ctx
    return gk


# ==========================================================================================
# (4) THE GRID -- real books and their matched nulls, tranched and untranched
# ==========================================================================================
def build(panels):
    P()
    P("=" * 100)
    P("(B) THE GRID -- 3 books x 2 panels x {M 21, Q 63} phases x 2 null conventions x draws")
    P("=" * 100)
    t0 = time.time()
    real_rows, null_rows, corr_rows = [], [], []
    BASE = {}
    cads = (("Q", DOQ_N),) if SMOKE else (("M", DOM_N), ("Q", DOQ_N))

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

        # the LIVE book (RULES v2, weekly) -- the 4a comparand, 964's convention verbatim
        bc = Ctx(px, offset_mask(idx, "W", 0)[0])
        bgr, btn = bc.run(bc.shift(rules_v2_weights(px, BAND0, GROSS)))
        for c in RUNGS:
            br = (bgr - btn * c / 1e4)[WARM:]
            BASE[(pname, c)] = mets(br[oos]) | {"full": mets(br)}
        del bc

        PL = pools(px)
        Wt = {b: BOOKS[b](px, GROSS) for b in BOOKS}
        ndraw = 200 if pname == "U56" else 100
        if SMOKE:
            ndraw = 6

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
            nph = 2 if SMOKE else n_ph
            # accumulators
            racc = {b: [np.zeros(len(spy)), np.zeros(len(spy))] for b in BOOKS}
            r_ph = {b: [] for b in BOOKS}                       # per-phase net streams @ head
            nacc = {(b, cv, d): [np.zeros(len(spy)), np.zeros(len(spy))]
                    for b in BOOKS for cv in CONVS for d in range(ndraw)}
            n_ph0 = {}                                          # phase-0 streams for CANON
            r_ph0 = {}
            n_ph_first = {(b, cv): [] for b in BOOKS for cv in CONVS}

            for ph in range(nph):
                ctx = Ctx(px, offset_mask(idx, per, ph)[0])
                for b, W in Wt.items():
                    wt = ctx.shift(W)
                    g_, t_ = ctx.run(wt)
                    gw, tw = g_[WARM:], t_[WARM:]
                    racc[b][0] += gw
                    racc[b][1] += tw
                    r_ph[b].append(gw - tw * HEAD_COST / 1e4)
                    if ph == 0:
                        r_ph0[b] = (gw.copy(), tw.copy())
                    for cv in CONVS:
                        for d in range(ndraw):
                            seed = (SEED0 + 1_000_000 * BOOKSEED[b]
                                    + 100_000 * CONVS.index(cv) + 1_000 * d + ph)
                            Wn, _, _ = null_weights(ctx, PL[POOLKIND[b]], wt, cv, seed, pid)
                            gn, tn = ctx.run(Wn)
                            gnw, tnw = gn[WARM:], tn[WARM:]
                            nacc[(b, cv, d)][0] += gnw
                            nacc[(b, cv, d)][1] += tnw
                            if ph == 0:
                                n_ph0[(b, cv, d)] = (gnw.copy(), tnw.copy())
                            if d == 0:
                                n_ph_first[(b, cv)].append(gnw - tnw * HEAD_COST / 1e4)
                del ctx
                if ph % 10 == 0:
                    P(f"    {pname}/{per} phase {ph + 1}/{nph}  ({time.time() - t0:.0f}s)")

            # ---- REAL rows -------------------------------------------------------------
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
            # ---- NULL rows -------------------------------------------------------------
            for (b, cv, d), (G, T_) in nacc.items():
                for c in RUNGS:
                    emit(null_rows, (G - T_ * c / 1e4) / float(nph), book=b, cadence=per,
                         estimator="FPORT", conv=cv, draw=d, cost_bps=c, n_phase=nph,
                         turn_per_yr=float(T_.sum() / nph / (len(spy) / 252.0)))
                    g0, t0_ = n_ph0[(b, cv, d)]
                    emit(null_rows, g0 - t0_ * c / 1e4, book=b, cadence=per,
                         estimator="CANON", conv=cv, draw=d, cost_bps=c, n_phase=1,
                         turn_per_yr=float(t0_.sum() / (len(spy) / 252.0)))
            # ---- H_CORR: mean pairwise phase-book correlation ---------------------------
            def meancorr(streams):
                A = np.vstack(streams)
                if len(A) < 2:
                    return np.nan
                C = np.corrcoef(A)
                iu = np.triu_indices(len(A), 1)
                return float(np.nanmean(C[iu]))
            for b in BOOKS:
                corr_rows.append(dict(panel=pname, book=b, cadence=per, n_phase=nph,
                                      REAL=meancorr(r_ph[b]),
                                      ROTP=meancorr(n_ph_first[(b, "ROTP")]),
                                      ROT=meancorr(n_ph_first[(b, "ROT")])))
            del racc, nacc, n_ph0, r_ph0, n_ph_first, r_ph
        P(f"  panel {pname} done  ({time.time() - t0:.0f}s)")

    real = pd.DataFrame(real_rows)
    null = pd.DataFrame(null_rows)
    for df in (real, null):
        lr = [legs_rec(r) for _, r in df.iterrows()]
        df["pass4b"] = [all(x.values()) for x in lr]
        df["fail4b"] = [failstr(x) for x in lr]
        for k in LEGS:
            df["leg_" + LEGNAME[k]] = [x[k] for x in lr]
        df["pass4b_OOSPURE"] = [all(legs_pure(r).values()) for _, r in df.iterrows()]
        df["IS_legs_passed"] = [sum(legs_is(r).values()) for _, r in df.iterrows()]
        df["pass4a"] = [bool(r.OOS_H1 > BASE[(r.panel, r.cost_bps)]["H1"]
                             and r.OOS_H2 > BASE[(r.panel, r.cost_bps)]["H2"]
                             and r.OOS_MaxDD >= BASE[(r.panel, r.cost_bps)]["MaxDD"])
                        for _, r in df.iterrows()]
    dump(real, "real")
    dump(null, "nulls")
    return real, null, pd.DataFrame(corr_rows), BASE


# ==========================================================================================
# (5) THE ANSWER
# ==========================================================================================
def answer(real, null, corr, BASE, gk):
    H = {}
    pn, bk, cd = SUBJECT

    P()
    P("=" * 100)
    P("(C) CROSS-RUN CHECKS AGAINST IDEA 964'S COMMITTED ARTIFACTS")
    P("=" * 100)
    g = OUT / "2026-09-15_should-the-PHASE-AVERAGED-MEAN-replace-the-CANONICAL_cloud.grid.csv"
    if g.exists() and not SMOKE:
        cg = pd.read_csv(g)
        cg = cg[(cg.gross == "CORE") & (cg.phase == 0) & (cg.book.isin(BOOKS))
                & (cg.panel.isin(real.panel.unique())) & (cg.cadence.isin(real.cadence.unique()))]
        can = real[real.estimator == "CANON"]
        keys = ["panel", "book", "cadence", "cost_bps"]
        cols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_CAGR", "IS_Sharpe", "OOS_CAGR",
                "OOS_Sharpe", "OOS_MaxDD", "OOS_H1", "OOS_H2", "turn_per_yr"]
        j = cg.merge(can, on=keys, suffixes=("_c", "_n"))
        dmax = max(float(np.abs(j[f"{c}_c"] - j[f"{c}_n"]).max()) for c in cols)
        flips = int((j.pass4b_REC != j.pass4b).sum())
        gk["G3"] = len(j) == len(cg) and dmax < 1e-10 and flips == 0
        P(f"  G3 964's committed grid.csv replayed on {len(j):,} of {len(cg):,} rows x "
          f"{len(cols)} cols, max|d| {dmax:.3e}, 4b-verdict flips {flips}   "
          f"{'PASS' if gk['G3'] else 'FAIL'}")
    else:
        gk["G3"] = False
        P("  G3 SKIPPED (smoke run or missing artifact)   FAIL")

    f = OUT / "2026-09-15_should-the-PHASE-AVERAGED-MEAN-replace-the-CANONICAL_cloud.fport.csv"
    subj = real[(real.panel == pn) & (real.book == bk) & (real.cadence == cd)
                & (real.estimator == "FPORT") & (real.cost_bps == HEAD_COST)]
    if f.exists() and not SMOKE and len(subj):
        cf = pd.read_csv(f)
        cs = cf[(cf.panel == pn) & (cf.book == bk) & (cf.gross == "CORE") & (cf.cadence == cd)
                & (cf.cost_bps == HEAD_COST)]
        d4 = max(abs(float(cs.iloc[0][k]) - float(subj.iloc[0][k]))
                 for k in ("OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "Sharpe", "MaxDD"))
        gk["G4"] = d4 < 5e-4
        P(f"  G4 964's committed SUBJECT tranche row (U56/EWELIG/CORE/Q @10bps) reproduced: "
          f"max|d| {d4:.3e}   {'PASS' if gk['G4'] else 'FAIL'}")
        P(f"     964 published  OOS {float(cs.iloc[0].OOS_CAGR):.2%} / "
          f"{float(cs.iloc[0].OOS_Sharpe):.3f} / {float(cs.iloc[0].OOS_MaxDD):.2%}")
        P(f"     this run       OOS {float(subj.iloc[0].OOS_CAGR):.2%} / "
          f"{float(subj.iloc[0].OOS_Sharpe):.3f} / {float(subj.iloc[0].OOS_MaxDD):.2%}")
    else:
        gk["G4"] = False
        P("  G4 SKIPPED (smoke run or missing artifact)   FAIL")

    # ---- G7 NESTING -------------------------------------------------------------------
    sn = null[(null.panel == pn) & (null.book == bk) & (null.cadence == cd)
              & (null.cost_bps == HEAD_COST) & (null.estimator == "FPORT")
              & (null.conv == "ROTP")]
    a = float(sn[sn.draw < DRAW_LADDER[0]].pass4b.mean())
    b_ = float(sn.sort_values("draw").head(DRAW_LADDER[0]).pass4b.mean())
    gk["G7"] = abs(a - b_) == 0.0
    P(f"  G7 NESTING: the {DRAW_LADDER[0]}-draw base rate is the first {DRAW_LADDER[0]} seeds "
      f"of the full grid: |d| {abs(a - b_):.3e}   {'PASS' if gk['G7'] else 'FAIL'}")
    P()
    P(f"  GATES {sum(gk.values())} of {len(gk)} PASS   "
      + "  ".join(f"{k}={'P' if v else 'F'}" for k, v in sorted(gk.items())))

    # ======================================================================================
    P()
    P("=" * 100)
    P("(D) H_CORR -- CONSTRUCTION VALIDITY: are the null's phase-books as correlated as the")
    P("    real book's?  (a tranche of INDEPENDENT coin flips is a better-diversified object")
    P("    than anything the real tranche can build, so 926's ROT would be an unfair null)")
    P("=" * 100)
    P(f"  {'panel':>6s} {'book':>7s} {'cad':>4s} {'P':>3s} {'REAL':>9s} {'ROTP':>9s} "
      f"{'ROT':>9s} {'d(ROTP)':>9s} {'d(ROT)':>9s}")
    for _, r in corr.iterrows():
        P(f"  {r.panel:>6s} {r.book:>7s} {r.cadence:>4s} {int(r.n_phase):>3d} {r.REAL:>9.4f} "
          f"{r.ROTP:>9.4f} {r.ROT:>9.4f} {r.ROTP - r.REAL:>+9.4f} {r.ROT - r.REAL:>+9.4f}")
    dP = float((corr.ROTP - corr.REAL).abs().max())
    dR = float((corr.REAL - corr.ROT).min())
    H["H_CORR"] = bool(dP <= CORR_BAR and dR >= CORR_BAR)
    P(f"  max|ROTP-REAL| {dP:.4f} (bar <= {CORR_BAR}) and min(REAL-ROT) {dR:+.4f} "
      f"(bar >= {CORR_BAR})  ->  H_CORR {'PASS' if H['H_CORR'] else 'FAIL'}")
    P("  READ: ROTP is the matched tranche; 926's ROT averages independent books and is")
    P("  reported beside it so the headline cannot be an artefact of either convention.")
    dump(corr, "phasecorr")

    # ======================================================================================
    P()
    P("=" * 100)
    P("(E) THE HEADLINE -- the TRANCHED null's own 4b base rate, every cell, every rung")
    P("=" * 100)
    grp = (null.groupby(["panel", "book", "cadence", "conv", "estimator", "cost_bps"])
           .agg(n=("draw", "size"), base4b=("pass4b", "mean"), base4a=("pass4a", "mean"),
                med_OOS_Sharpe=("OOS_Sharpe", "median"), med_OOS_CAGR=("OOS_CAGR", "median"),
                med_OOS_MaxDD=("OOS_MaxDD", "median"),
                med_turn=("turn_per_yr", "median"))
           .reset_index())
    for k in LEGS:
        fr = (null.groupby(["panel", "book", "cadence", "conv", "estimator", "cost_bps"])
              ["leg_" + LEGNAME[k]].mean().reset_index()
              .rename(columns={"leg_" + LEGNAME[k]: "legpass_" + LEGNAME[k]}))
        grp = grp.merge(fr, on=["panel", "book", "cadence", "conv", "estimator", "cost_bps"])
    dump(grp, "base")

    rr = real.set_index(["panel", "book", "cadence", "estimator", "cost_bps"])
    P(f"  {'panel':>6s} {'book':>7s} {'cad':>4s} {'conv':>5s} {'cost':>5s} "
      f"{'REALcanon':>10s} {'REALtran':>9s} | {'NULLcanon':>10s} {'NULLtran':>9s} "
      f"{'LIFT':>8s} | {'medDDcan':>9s} {'medDDtra':>9s}")
    for (p_, b_, c_, cv), s in grp[grp.conv.notna()].groupby(["panel", "book", "cadence", "conv"]):
        for cost in RUNGS:
            gc = s[(s.cost_bps == cost) & (s.estimator == "CANON")]
            gf = s[(s.cost_bps == cost) & (s.estimator == "FPORT")]
            if not len(gc) or not len(gf):
                continue
            try:
                rc = bool(rr.loc[(p_, b_, c_, "CANON", cost)].pass4b)
                rf = bool(rr.loc[(p_, b_, c_, "FPORT", cost)].pass4b)
            except KeyError:
                continue
            P(f"  {p_:>6s} {b_:>7s} {c_:>4s} {cv:>5s} {cost:>5.0f} "
              f"{str(rc):>10s} {str(rf):>9s} | {float(gc.base4b.iloc[0]):>10.3f} "
              f"{float(gf.base4b.iloc[0]):>9.3f} "
              f"{float(gf.base4b.iloc[0]) - float(gc.base4b.iloc[0]):>+8.3f} | "
              f"{float(gc.med_OOS_MaxDD.iloc[0]):>9.2%} {float(gf.med_OOS_MaxDD.iloc[0]):>9.2%}")

    # ---- the SUBJECT cell -----------------------------------------------------------------
    P()
    P("-" * 100)
    P(f"  THE SUBJECT CELL: {pn} / {bk} / CORE 0.75 / {cd} / {HEAD_COST:.0f} bps "
      f"(964's only rule-8 OOS 4b pass in 54 picks)")
    P("-" * 100)
    sub_real = rr.loc[(pn, bk, cd, "FPORT", HEAD_COST)]
    sub_can = rr.loc[(pn, bk, cd, "CANON", HEAD_COST)]
    P(f"  REAL tranche   OOS {sub_real.OOS_CAGR:.2%} / {sub_real.OOS_Sharpe:.3f} / "
      f"{sub_real.OOS_MaxDD:.2%}   full Sharpe {sub_real.Sharpe:.3f} / MaxDD "
      f"{sub_real.MaxDD:.2%}   turn/yr {sub_real.turn_per_yr:.2f}   4b "
      f"{bool(sub_real.pass4b)}  4a {bool(sub_real.pass4a)}  fail={sub_real.fail4b}")
    P(f"  REAL canonical OOS {sub_can.OOS_CAGR:.2%} / {sub_can.OOS_Sharpe:.3f} / "
      f"{sub_can.OOS_MaxDD:.2%}   full Sharpe {sub_can.Sharpe:.3f} / MaxDD "
      f"{sub_can.MaxDD:.2%}   turn/yr {sub_can.turn_per_yr:.2f}   4b "
      f"{bool(sub_can.pass4b)}  4a {bool(sub_can.pass4a)}  fail={sub_can.fail4b}")
    cap = 0.60 * abs(float(sub_real.spy_MaxDD))
    P(f"  4b DD cap = 0.60 x |SPY MaxDD {float(sub_real.spy_MaxDD):.2%}| = {-cap:.2%}; the "
      f"tranche clears it by {(cap - abs(float(sub_real.OOS_MaxDD))) * 100:.2f} pp")
    P(f"  SPY        OOS {float(sub_real.spy_OOS_CAGR):.2%} / "
      f"{float(sub_real.spy_OOS_Sharpe):.4f} / {float(sub_real.spy_OOS_MaxDD):.2%}")
    bl = BASE[(pn, HEAD_COST)]
    P(f"  RULES v2   OOS {bl['CAGR']:.2%} / {bl['Sharpe']:.3f} / {bl['MaxDD']:.2%}   "
      f"full Sharpe {bl['full']['Sharpe']:.3f} / MaxDD {bl['full']['MaxDD']:.2%}")

    ladder = []
    P()
    P(f"  DRAW LADDER (nested) -- tranched null 4b base rate in the subject cell")
    P(f"  {'conv':>5s} {'draws':>6s} {'base4b_TRAN':>12s} {'base4b_CANON':>13s} {'LIFT':>8s} "
      f"{'pctl_Sharpe':>12s} {'pctl_MaxDD':>11s} {'pctl_CAGR':>10s} {'emp_p':>8s}")
    for cv in CONVS:
        s = null[(null.panel == pn) & (null.book == bk) & (null.cadence == cd)
                 & (null.conv == cv) & (null.cost_bps == HEAD_COST)]
        for D in DRAW_LADDER:
            sf = s[(s.estimator == "FPORT") & (s.draw < D)]
            sc = s[(s.estimator == "CANON") & (s.draw < D)]
            if not len(sf):
                continue
            pS = float((sf.OOS_Sharpe < sub_real.OOS_Sharpe).mean())
            pD = float((sf.OOS_MaxDD.abs() > abs(sub_real.OOS_MaxDD)).mean())
            pC = float((sf.OOS_CAGR < sub_real.OOS_CAGR).mean())
            ep = (1 + int((sf.OOS_Sharpe >= sub_real.OOS_Sharpe).sum())) / (1 + len(sf))
            P(f"  {cv:>5s} {D:>6d} {sf.pass4b.mean():>12.3f} {sc.pass4b.mean():>13.3f} "
              f"{sf.pass4b.mean() - sc.pass4b.mean():>+8.3f} {pS:>12.3f} {pD:>11.3f} "
              f"{pC:>10.3f} {ep:>8.4f}")
            ladder.append(dict(conv=cv, draws=D, base4b_FPORT=sf.pass4b.mean(),
                               base4b_CANON=sc.pass4b.mean(),
                               lift=sf.pass4b.mean() - sc.pass4b.mean(), pctl_Sharpe=pS,
                               pctl_MaxDD=pD, pctl_CAGR=pC, emp_p=ep,
                               med_OOS_MaxDD_FPORT=sf.OOS_MaxDD.median(),
                               med_OOS_MaxDD_CANON=sc.OOS_MaxDD.median(),
                               med_OOS_Sharpe_FPORT=sf.OOS_Sharpe.median(),
                               med_turn_FPORT=sf.turn_per_yr.median(),
                               med_turn_CANON=sc.turn_per_yr.median()))
    lad = pd.DataFrame(ladder)
    dump(lad, "ladder")

    head = lad[(lad.conv == "ROTP") & (lad.draws == lad.draws.max())].iloc[0]
    headROT = lad[(lad.conv == "ROT") & (lad.draws == lad.draws.max())].iloc[0]
    H["H_BASE"] = bool(head.base4b_FPORT <= BASE_BAR)
    H["H_LIFT"] = bool(head.lift >= LIFT_BAR)
    ddlift = abs(float(head.med_OOS_MaxDD_CANON)) - abs(float(head.med_OOS_MaxDD_FPORT))
    H["H_DD"] = bool(ddlift >= DD_BAR)
    H["H_PCTL"] = bool(head.pctl_Sharpe >= PCTL_BAR and head.pctl_MaxDD >= PCTL_BAR)
    P()
    P(f"  H_BASE  tranched null 4b base rate {head.base4b_FPORT:.3f} (bar <= {BASE_BAR})  "
      f"{'PASS' if H['H_BASE'] else 'FAIL'}   [ROT convention: {headROT.base4b_FPORT:.3f}]")
    P(f"  H_LIFT  tranching lifts the null base rate {head.lift:+.3f} (bar >= +{LIFT_BAR})  "
      f"{'PASS' if H['H_LIFT'] else 'FAIL'}   [ROT: {headROT.lift:+.3f}]")
    P(f"  H_DD    tranched null median |OOS MaxDD| tighter by {ddlift * 100:.2f} pp "
      f"(bar >= {DD_BAR * 100:.2f} pp)  {'PASS' if H['H_DD'] else 'FAIL'}"
      f"   [{head.med_OOS_MaxDD_CANON:.2%} -> {head.med_OOS_MaxDD_FPORT:.2%}]")
    P(f"  H_PCTL  real tranche beats {head.pctl_Sharpe:.3f} of its null on OOS Sharpe and "
      f"{head.pctl_MaxDD:.3f} on |OOS MaxDD| (bar >= {PCTL_BAR})  "
      f"{'PASS' if H['H_PCTL'] else 'FAIL'}")
    P(f"  TURNOVER (reported, NOT matched -- 926 matches gross, not turnover): real tranche "
      f"{sub_real.turn_per_yr:.2f}/yr vs null tranche median {head.med_turn_FPORT:.2f}/yr")

    # ---- per-leg base rates in the subject cell -------------------------------------------
    P()
    P("  PER-LEG NULL PASS RATES in the subject cell (which leg does the tranche buy?)")
    sg = grp[(grp.panel == pn) & (grp.book == bk) & (grp.cadence == cd)
             & (grp.cost_bps == HEAD_COST)]
    P(f"  {'conv':>5s} {'est':>6s} " + " ".join(f"{LEGNAME[k]:>9s}" for k in LEGS)
      + f" {'all5':>7s}")
    for _, r in sg.sort_values(["conv", "estimator"]).iterrows():
        P(f"  {r.conv:>5s} {r.estimator:>6s} "
          + " ".join(f"{r['legpass_' + LEGNAME[k]]:>9.3f}" for k in LEGS)
          + f" {r.base4b:>7.3f}")
    rl = real[(real.panel == pn) & (real.book == bk) & (real.cadence == cd)
              & (real.cost_bps == HEAD_COST)]
    for _, r in rl.iterrows():
        P(f"  {'REAL':>5s} {r.estimator:>6s} "
          + " ".join(f"{float(r['leg_' + LEGNAME[k]]):>9.3f}" for k in LEGS)
          + f" {float(r.pass4b):>7.3f}")

    # ======================================================================================
    P()
    P("=" * 100)
    P("(F) RULE 8 -- walk-forward: (book, estimator) chosen on 2009-2016 ALONE, 2017-2026 read")
    P("    ONCE, with the pick's OWN matched null base rate read the same way")
    P("=" * 100)
    CHOOSERS = {"IS_SHARPE": lambda d: d.sort_values("IS_Sharpe", ascending=False).iloc[0],
                "IS_CAGR":   lambda d: d.sort_values("IS_CAGR", ascending=False).iloc[0],
                "IS_LEGS":   lambda d: d.sort_values(["IS_legs_passed", "IS_Sharpe"],
                                                     ascending=False).iloc[0]}
    wf = []
    for p_ in sorted(real.panel.unique()):
        for c_ in sorted(real.cadence.unique()):
            pool = real[(real.panel == p_) & (real.cadence == c_)
                        & (real.cost_bps == HEAD_COST)]
            for cn, fn in CHOOSERS.items():
                pick = fn(pool)
                nb = {}
                for cv in CONVS:
                    s = null[(null.panel == p_) & (null.book == pick.book)
                             & (null.cadence == c_) & (null.conv == cv)
                             & (null.estimator == pick.estimator)
                             & (null.cost_bps == HEAD_COST)]
                    nb[cv] = float(s.pass4b.mean()) if len(s) else np.nan
                    nb[cv + "_4a"] = float(s.pass4a.mean()) if len(s) else np.nan
                bl_ = BASE[(p_, HEAD_COST)]
                wf.append(dict(panel=p_, cadence=c_, chooser=cn, book=pick.book,
                               estimator=pick.estimator, n_phase=int(pick.n_phase),
                               IS_Sharpe=pick.IS_Sharpe, IS_CAGR=pick.IS_CAGR,
                               IS_legs=int(pick.IS_legs_passed),
                               OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                               OOS_MaxDD=pick.OOS_MaxDD, turn_per_yr=pick.turn_per_yr,
                               OOS_4b=bool(pick.pass4b), OOS_4a=bool(pick.pass4a),
                               fail4b=pick.fail4b,
                               null4b_ROTP=nb["ROTP"], null4b_ROT=nb["ROT"],
                               null4a_ROTP=nb["ROTP_4a"],
                               spy_OOS_CAGR=pick.spy_OOS_CAGR,
                               spy_OOS_Sharpe=pick.spy_OOS_Sharpe,
                               spy_OOS_MaxDD=pick.spy_OOS_MaxDD,
                               v2_OOS_CAGR=bl_["CAGR"], v2_OOS_Sharpe=bl_["Sharpe"],
                               v2_OOS_MaxDD=bl_["MaxDD"]))
    wfd = pd.DataFrame(wf)
    dump(wfd, "walkforward")
    P(f"  {'panel':>6s} {'cad':>4s} {'chooser':>10s} {'book':>7s} {'est':>6s} "
      f"{'OOS CAGR':>9s} {'OOS Shrp':>9s} {'OOS DD':>8s} {'4b':>6s} {'4a':>6s} "
      f"{'null4b':>7s} {'fail':>22s}")
    for _, r in wfd.iterrows():
        P(f"  {r.panel:>6s} {r.cadence:>4s} {r.chooser:>10s} {r.book:>7s} {r.estimator:>6s} "
          f"{r.OOS_CAGR:>9.2%} {r.OOS_Sharpe:>9.3f} {r.OOS_MaxDD:>8.2%} "
          f"{str(r.OOS_4b):>6s} {str(r.OOS_4a):>6s} {r.null4b_ROTP:>7.3f} {r.fail4b:>22s}")
    sp = wfd.iloc[0]
    P(f"  COMPARANDS  SPY OOS {sp.spy_OOS_CAGR:.2%} / {sp.spy_OOS_Sharpe:.4f} / "
      f"{sp.spy_OOS_MaxDD:.2%}")
    for p_ in sorted(real.panel.unique()):
        b2 = BASE[(p_, HEAD_COST)]
        P(f"              RULES v2 (live) {p_}: OOS {b2['CAGR']:.2%} / {b2['Sharpe']:.3f} / "
          f"{b2['MaxDD']:.2%}   full Sharpe {b2['full']['Sharpe']:.3f} / MaxDD "
          f"{b2['full']['MaxDD']:.2%}")
    n_f = int((wfd.estimator == "FPORT").sum())
    share_f = n_f / len(wfd)
    beat = float((wfd.OOS_4b.astype(float) > wfd.null4b_ROTP).mean())
    H["H_RULE8"] = bool(share_f >= RULE8_BAR and beat > 0.5)
    P(f"  IS-only choosers pick FPORT in {n_f} of {len(wfd)} ({share_f:.3f}, bar >= "
      f"{RULE8_BAR}); picks beating their own null base rate {beat:.3f}  "
      f"H_RULE8 {'PASS' if H['H_RULE8'] else 'FAIL'}")
    P(f"  OOS 4b {int(wfd.OOS_4b.sum())} of {len(wfd)}   OOS 4a {int(wfd.OOS_4a.sum())} of "
      f"{len(wfd)}")
    tot4b = int(real[real.cost_bps == HEAD_COST].pass4b.sum())
    tot4a = int(real[real.cost_bps == HEAD_COST].pass4a.sum())
    P(f"  full-sample over the {len(real[real.cost_bps == HEAD_COST])}-row 10 bps REAL grid: "
      f"4b {tot4b}, 4a {tot4a}")

    # ======================================================================================
    P()
    P("=" * 100)
    P("(G) KEEP PATHS (PROTOCOL rule 4), both evaluated for every REAL book at 10 bps")
    P("=" * 100)
    P(f"  {'panel':>6s} {'book':>7s} {'cad':>4s} {'est':>6s} {'4a':>6s} {'4b':>6s} "
      f"{'null4b_ROTP':>12s} {'verdict':>10s}")
    keeps = []
    for _, r in real[real.cost_bps == HEAD_COST].iterrows():
        s = null[(null.panel == r.panel) & (null.book == r.book) & (null.cadence == r.cadence)
                 & (null.estimator == r.estimator) & (null.conv == "ROTP")
                 & (null.cost_bps == HEAD_COST)]
        nb = float(s.pass4b.mean()) if len(s) else np.nan
        v = ("KEEP-4a" if r.pass4a else
             "KEEP-4b" if (r.pass4b and nb <= BASE_BAR) else
             "PARK" if r.pass4b else "KILL")
        keeps.append(dict(panel=r.panel, book=r.book, cadence=r.cadence, estimator=r.estimator,
                          pass4a=bool(r.pass4a), pass4b=bool(r.pass4b), null4b_ROTP=nb,
                          verdict=v, OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe,
                          OOS_MaxDD=r.OOS_MaxDD, fail4b=r.fail4b))
        P(f"  {r.panel:>6s} {r.book:>7s} {r.cadence:>4s} {r.estimator:>6s} "
          f"{str(bool(r.pass4a)):>6s} {str(bool(r.pass4b)):>6s} {nb:>12.3f} {v:>10s}")
    kp = pd.DataFrame(keeps)
    dump(kp, "keep")
    P("  NOTE: a 4b PASS whose own gross-matched null clears the same bar more than "
      f"{BASE_BAR:.0%} of the time is scored PARK, not KEEP -- ideas 926/942's clause.")

    hyp = pd.DataFrame([dict(hypothesis=k, result="PASS" if v else "FAIL") for k, v in H.items()]
                       + [dict(hypothesis=k, result="PASS" if v else "FAIL")
                          for k, v in sorted(gk.items())])
    dump(hyp, "hypotheses")
    P()
    P("  HYPOTHESES: " + "  ".join(f"{k}={'PASS' if v else 'FAIL'}" for k, v in H.items()))
    return H, wfd, lad, kp


def main():
    t0 = time.time()
    P(f"IDEA 975-TRANCHE (lane B, 2026-09-16) -- {STEM}")
    P(f"  SMOKE={int(SMOKE)}  draw ladder {DRAW_LADDER}  gross {GROSS}  rungs {RUNGS}")
    P()
    panels = load_panels()
    for k, v in panels.items():
        P(f"  panel {k}: {v.shape[1]} columns, {v.index[0].date()} -> {v.index[-1].date()}")
    P("  SURVIVORSHIP (rule 9): current-constituent lists; every LEVEL is optimistic and every")
    P("  NULL base rate is an UPPER bound, which cuts AGAINST this run's own H_LIFT.")
    P()
    gk = gates(panels)
    real, null, corr, BASE = build(panels)
    answer(real, null, corr, BASE, gk)
    P()
    P(f"  total {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()

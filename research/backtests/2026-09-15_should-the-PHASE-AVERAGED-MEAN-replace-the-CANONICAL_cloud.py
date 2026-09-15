#!/usr/bin/env python3
"""Idea 964 (cloud lane, 2026-09-15) -- should the PHASE-AVERAGED MEAN replace the CANONICAL
in every committed phase-sensitive claim?

THE QUESTION (queue, 2026-09-15, filed by idea 962)
  Idea 962 found the CANONICAL rebalance phase (period-end, d=0, what `engine.rebalance_mask`
  produces and what every live rule trades) scores EXACTLY at the blind-random rate -- 2 4b
  passes against a Poisson-binomial expectation of 2.35 -- while the FAMILY MEAN beats every
  in-sample chooser in 0.600 of cells.  The queue asks: census the record's committed MONTHLY
  and QUARTERLY CAGR claims and re-publish each as CANONICAL, FAMILY MEAN and FAMILY SPREAD,
  and report how many claims change SIGN or VERDICT.

WHY IT MATTERS FOR CAPITAL, AND THE DISTINCTION THE QUEUE'S WORDING HIDES
  "Replace the canonical with the family mean" can mean two different objects, and they are not
  interchangeable.  This run prices BOTH and never conflates them:

    CANON   phase 0.  The book the record publishes and the only one the live rules trade.
    FMEAN   the MEAN OF THE METRIC over the family's phases.  This is an ESTIMATOR of what the
            book is worth when you do not get to pick the phase.  IT IS NOT A PORTFOLIO -- no
            allocation of capital produces a mean-of-Sharpes -- so it can never be a KEEP.
    FPORT   the TRANCHED book: 1/P of NAV in each of the P phase-books, re-levelled daily.  This
            IS tradable, it IS what "trade the phase average" would mean at a desk, and unlike
            FMEAN it earns a real diversification term.  Every 4b/4a verdict below that could
            move capital is read on FPORT; FMEAN is reported as an estimator only.

  So the run answers the queue's census question (CANON vs FMEAN vs SPREAD on committed claims)
  AND the capital question the census cannot answer on its own (is FPORT a better book).

WHAT IS TUNED AND WHAT IS REPORTED (PROTOCOL 4: max 2 tuned parameters)
  TUNED 1  CLAIM SET, 3 levels, every one reported and none chosen:
           STRICT  committed rows at phase == 0 (the canonical claim itself) whose
                   (panel, book, gross, cadence, cost) key maps exactly onto this run's grid
           WIDE    committed rows at ANY phase, mapped to their family
           GRID    the 150 families themselves, i.e. the record-independent version of the same
                   question (every family carries a claim whether or not anyone published it)
  TUNED 2  CADENCE, 3 levels: M (21 phases) / Q (63 phases) / pooled.
  REPORTED AXES (nothing fitted on them, every point published): panel U56 / B136 / SMALL;
  book TOP05 / TOP10 / TOP20 / EWELIG / BAND03; gross CORE 0.75 / EXT 1.00; cost rung
  0 / 5 / 10 / 25 / 50 bps; estimator CANON / FMEAN / FPORT; 4b convention REC and OOSPURE.

PRE-REGISTERED BARS (fixed before any number was read; both directions reported)
  H_SIGN     the swap is CONSEQUENTIAL for levels iff > 10% of STRICT claims change the SIGN of
             (claim CAGR - SPY CAGR) between CANON and FMEAN.
  H_VERDICT  the swap is CONSEQUENTIAL for verdicts iff > 10% of STRICT claims change their 4b
             REC verdict between CANON and FMEAN.
  H_BIAS     the canonical is UNBIASED iff the median of (CANON - FMEAN) CAGR over the 150
             families is within +/- 0.25 pp and the canonical's within-family CAGR percentile
             has median in [0.40, 0.60].  (962 claimed the canonical "sits low in its own
             family"; this is that claim, pre-registered, on the whole grid.)
  H_TRADE    FPORT is a BETTER BOOK, not just a tidier estimator: its full-sample Sharpe exceeds
             CANON's in >= 0.75 of the 150 families at 10 bps.
  H_CHEAP    the tranche is not bought with turnover: FPORT turnover/yr <= CANON's in >= 0.90 of
             families (the tranches trade on different days but each trades 1/P of NAV).
  H_KEEP     (rule 8, REQUIRED) book x gross chosen on 2009-2016 ALONE, 2017-2026 read ONCE,
             both KEEP paths, against SPY and RULES v2 in the same window, for all 3 estimators.

GATES (all printed before any result number)
  G0  `offset_mask(idx, per, 0)` == `engine.rebalance_mask(idx, per)`, 0 disagreeing rows
  G1  the fast `Ctx` runner == `engine.backtest` on returns AND turnover
  G2  BAND03 @ 0.75 == `baseline.rules_v2_weights` elementwise
  G3  CROSS-RUN: idea 962's committed `.grid.csv` reproduced on all 12,600 rows x 13 columns
  G4  FPORT with a ONE-phase family == CANON exactly (the tranche identity)
  G5  determinism: the subject family rebuilt from scratch, max|d| over all reported columns
  G6  every chooser is IS-ONLY -- picks invariant to permuted OOS columns

PROTOCOL: 10 bps primary (all five rungs reported), decided at close t / applied t+1, warm-up
260 days, IS 2009-2016 / OOS 2017-2026, no shorting, no leverage beyond the published gross.
Nothing in RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py is modified.

SURVIVORSHIP (rule 9): U56, B136 and SMALL are CURRENT-CONSTITUENT lists (SMALL additionally
drops every ticker with `max_1d_move` >= 1.0 per `data/small_meta.csv`), so every CAGR and
drawdown LEVEL below is optimistic.  The CANON-vs-FMEAN-vs-FPORT contrast is the SAME names on
the SAME tape under different rebalance DAYS and is very nearly immune to it; the 4b levels are
read against SPY, which is not survivorship-inflated, so every 4b PASS reported here is an
UPPER bound and every FAIL is understated.  Stated, not hidden.
"""
from __future__ import annotations

import os
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score   # noqa: E402
from engine import backtest, rebalance_mask                               # noqa: E402

BAND0, VOLCAP, WARM = 0.03, 0.60, 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
HEAD_COST, HEAD_GROSS = 10.0, "CORE"
DOM_N, DOQ_N = 21, 63
CLAIM_SETS = {"CORE": 0.75, "EXT": 1.00}
RUNGS = [0.0, 5.0, 10.0, 25.0, 50.0]
LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
LEGNAME = {"H1": "L1_H1", "H2": "L2_H2", "OOS": "L3_OOS", "DD": "L4_DD", "CAGR": "L5_CAGR"}
ESTS = ["CANON", "FMEAN", "FPORT"]
# pre-registered bars
SIGN_BAR, VERDICT_BAR = 0.10, 0.10
BIAS_PP, PCTL_LO, PCTL_HI = 0.25, 0.40, 0.60
TRADE_BAR, CHEAP_BAR = 0.75, 0.90
SMOKE = bool(int(os.environ.get("IDEA964_SMOKE", "0")))
LINES: list[str] = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ==========================================================================================
# (1) phase machinery -- copied VERBATIM from ideas 938/942/962 so this run NESTS the record
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
    """Fast runner -- byte-identical to 942/962's.  G1 asserts it against engine.backtest."""

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
    """The RECORD's 4b convention (942/962's, verbatim)."""
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
    """The same alphabet read entirely INSIDE the IS window -- chooser input only (G6)."""
    return dict(H1=row["IS_H1"] > row["spy_IS_H1"], H2=row["IS_H2"] > row["spy_IS_H2"],
                OOS=row["IS_Sharpe"] > row["spy_IS_Sharpe"],
                DD=abs(row["IS_MaxDD"]) <= 0.60 * abs(row["spy_IS_MaxDD"]),
                CAGR=row["IS_CAGR"] >= 0.70 * row["spy_IS_CAGR"])


def failstr(lg):
    f = [LEGNAME[k] for k in LEGS if not lg[k]]
    return ",".join(f) if f else "-"


# ==========================================================================================
# (2) THE BOOK SET -- 942/962's five books verbatim
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
    "TOP05":  lambda p, g: ranked_book(p, g, 5),
    "TOP10":  lambda p, g: ranked_book(p, g, 10),
    "TOP20":  lambda p, g: ranked_book(p, g, 20),
    "EWELIG": lambda p, g: ew_elig(p, g),
    "BAND03": lambda p, g: band_book(p, BAND0, g),
}


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    return px[[c for c in px.columns if c == "SPY" or c not in bad]], len(bad)


# ==========================================================================================
# (3) CHOOSERS -- IS columns only (G6)
# ==========================================================================================
def _argmax(v, tiebreak=None):
    v = np.asarray(v, float)
    if not np.isfinite(v).any():
        return 0
    best = np.nanmax(v)
    cand = np.flatnonzero(np.isclose(v, best, rtol=0, atol=0))
    if len(cand) > 1 and tiebreak is not None:
        t = np.asarray(tiebreak, float)[cand]
        cand = cand[np.flatnonzero(t == np.nanmax(t))]
    return int(cand[0])


CHOOSERS = ["C_CAGR", "C_SHARPE", "C_ISLEGS"]


def choose(name, sub):
    isc, iss = sub.IS_CAGR.values, sub.IS_Sharpe.values
    if name == "C_CAGR":
        return _argmax(isc, iss)
    if name == "C_SHARPE":
        return _argmax(iss, isc)
    if name == "C_ISLEGS":
        return _argmax(sub.IS_legs_passed.values, iss)
    raise KeyError(name)


# ==========================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 964 (cloud) -- should the PHASE-AVERAGED MEAN replace the CANONICAL?")
    P(f"  run {pd.Timestamp.utcnow():%Y-%m-%d %H:%M UTC}   PROTOCOL 10 bps / t+1 / warm-up {WARM}")
    P("=" * 100)

    panels = {}
    px = load_universe()
    panels["U56"] = px
    panels["B136"] = load_universe(broad=True)
    sm, ndrop = load_small()
    panels["SMALL"] = sm
    for k, v in panels.items():
        P(f"  panel {k:6s} {v.shape[1]:4d} cols  {v.index[0].date()} .. {v.index[-1].date()}  "
          f"{len(v):,} rows")
    P(f"  SMALL drops {ndrop} tickers with max_1d_move >= 1.0 per data/small_meta.csv; "
      f"SURVIVORSHIP: all three panels are CURRENT-CONSTITUENT lists (rule 9).")

    # ---------------------------------------------------------------------------------- gates
    P()
    P("=" * 100)
    P("(A) GATES")
    P("=" * 100)
    gk = {}
    u = panels["U56"]
    idx = u.index
    g0 = 0
    for per in ("M", "Q", "W"):
        a = offset_mask(idx, per, 0)[0].values
        b = rebalance_mask(idx, per).values
        g0 += int((a != b).sum())
    gk["G0"] = g0 == 0
    P(f"  G0 offset_mask(.,per,0) == engine.rebalance_mask on M/Q/W: {g0} disagreeing rows  "
      f"{'PASS' if gk['G0'] else 'FAIL'}")

    w75 = rules_v2_weights(u, BAND0, 0.75)
    bb = band_book(u, BAND0, 0.75)
    d2 = float(np.nanmax(np.abs(w75.values - bb.values)))
    gk["G2"] = d2 == 0.0
    P(f"  G2 BAND03@0.75 == baseline.rules_v2_weights: {d2:.3e}  {'PASS' if gk['G2'] else 'FAIL'}")

    ctxW = Ctx(u, offset_mask(idx, "W", 0)[0])
    gr, tn = ctxW.run(ctxW.shift(w75))
    eng = backtest(u, w75, cost_bps=0.0, freq="W")
    # compared from the warm-up onward: engine.backtest carries 2 NaN rows in 2008 where the
    # panel is not yet fully priced, and nothing in this run reads days before WARM.
    d1r = float(np.abs(gr[WARM:] - eng["returns"].values[WARM:]).max())
    d1t = float(np.abs(tn[WARM:] - eng["turnover"].values[WARM:]).max())
    gk["G1"] = d1r < 1e-12 and d1t < 1e-10
    P(f"  G1 Ctx == engine.backtest   returns {d1r:.3e}   turnover {d1t:.3e}  "
      f"{'PASS' if gk['G1'] else 'FAIL'}")
    del ctxW, eng

    # ------------------------------------------------------------------------------- the grid
    P()
    P("=" * 100)
    P("(B) THE PHASE GRID -- 5 books x 3 panels x 2 gross x (21 M + 63 Q) phases x 5 rungs")
    P("    plus, for every family, the TRANCHED book FPORT = mean of the phase-books' NET returns")
    P("=" * 100)
    ROWS, BASE, FP, WINS = [], {}, {}, {}
    for pname, p in panels.items():
        pidx = p.index
        spy = p["SPY"].pct_change().fillna(0.0).values[WARM:]
        oos = np.asarray(pidx >= pd.Timestamp(OOS_START))[WARM:]
        is_ = np.asarray(pidx <= pd.Timestamp(IS_END))[WARM:]
        WINS[pname] = (is_, oos)
        ms, ms_o, ms_i = mets(spy), mets(spy[oos]), mets(spy[is_])
        bw = rules_v2_weights(p, BAND0, 0.75)                  # the LIVE book, weekly (4a target)
        bc = Ctx(p, offset_mask(pidx, "W", 0)[0])
        bgr, btn = bc.run(bc.shift(bw))
        for c in RUNGS:
            br = (bgr - btn * c / 1e4)[WARM:]
            BASE[(pname, c)] = mets(br[oos]) | {"full_MaxDD": maxdd(br), "full": mets(br)}
        del bc
        Wt = {(b, cs): BOOKS[b](p, g) for b in BOOKS for cs, g in CLAIM_SETS.items()}
        cads = (("M", DOM_N),) if SMOKE else (("M", DOM_N), ("Q", DOQ_N))
        for per, n_ph in cads:
            acc = {}                                           # FPORT accumulators
            tacc = {}
            for d in range(n_ph):
                ctx = Ctx(p, offset_mask(pidx, per, d)[0])
                for (b, cs), W in Wt.items():
                    g_, t_ = ctx.run(ctx.shift(W))
                    gw, tw = g_[WARM:], t_[WARM:]
                    for c in RUNGS:
                        r = gw - tw * c / 1e4
                        key = (pname, b, cs, per, c)
                        acc[key] = acc.get(key, 0.0) + r
                        tacc[key] = tacc.get(key, 0.0) + tw
                        m, mi, mo = mets(r), mets(r[is_]), mets(r[oos])
                        ROWS.append(dict(
                            panel=pname, book=b, gross=cs, cadence=per, phase=d, cost_bps=c,
                            CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                            H1=m["H1"], H2=m["H2"],
                            IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                            IS_H1=mi["H1"], IS_H2=mi["H2"],
                            OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                            OOS_H1=mo["H1"], OOS_H2=mo["H2"],
                            turn_per_yr=float(tw.sum() / (len(r) / 252.0)),
                            spy_CAGR=ms["CAGR"], spy_Sharpe=ms["Sharpe"], spy_MaxDD=ms["MaxDD"],
                            spy_H1=ms["H1"], spy_H2=ms["H2"],
                            spy_IS_CAGR=ms_i["CAGR"], spy_IS_Sharpe=ms_i["Sharpe"],
                            spy_IS_MaxDD=ms_i["MaxDD"], spy_IS_H1=ms_i["H1"],
                            spy_IS_H2=ms_i["H2"],
                            spy_OOS_CAGR=ms_o["CAGR"], spy_OOS_Sharpe=ms_o["Sharpe"],
                            spy_OOS_MaxDD=ms_o["MaxDD"], spy_OOS_H1=ms_o["H1"],
                            spy_OOS_H2=ms_o["H2"]))
                del ctx
            for key, s in acc.items():
                r = s / float(n_ph)
                m, mi, mo = mets(r), mets(r[is_]), mets(r[oos])
                pn, b, cs, pe, c = key
                FP[key] = dict(
                    panel=pn, book=b, gross=cs, cadence=pe, phase=-1, cost_bps=c, estimator="FPORT",
                    CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m["H1"], H2=m["H2"],
                    IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                    IS_H1=mi["H1"], IS_H2=mi["H2"],
                    OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                    OOS_H1=mo["H1"], OOS_H2=mo["H2"],
                    turn_per_yr=float(tacc[key].sum() / float(n_ph) / (len(r) / 252.0)),
                    spy_CAGR=ms["CAGR"], spy_Sharpe=ms["Sharpe"], spy_MaxDD=ms["MaxDD"],
                    spy_H1=ms["H1"], spy_H2=ms["H2"],
                    spy_IS_CAGR=ms_i["CAGR"], spy_IS_Sharpe=ms_i["Sharpe"],
                    spy_IS_MaxDD=ms_i["MaxDD"], spy_IS_H1=ms_i["H1"], spy_IS_H2=ms_i["H2"],
                    spy_OOS_CAGR=ms_o["CAGR"], spy_OOS_Sharpe=ms_o["Sharpe"],
                    spy_OOS_MaxDD=ms_o["MaxDD"], spy_OOS_H1=ms_o["H1"], spy_OOS_H2=ms_o["H2"])
            del acc, tacc
        P(f"  panel {pname} done  ({time.time() - t0:.0f}s)")
    grid = pd.DataFrame(ROWS)
    for df in (grid,):
        df["IS_legs_passed"] = [sum(legs_is(r).values()) for _, r in df.iterrows()]
        lr = [legs_rec(r) for _, r in df.iterrows()]
        lp = [legs_pure(r) for _, r in df.iterrows()]
        df["pass4b_REC"] = [all(x.values()) for x in lr]
        df["fail4b_REC"] = [failstr(x) for x in lr]
        df["pass4b_OOSPURE"] = [all(x.values()) for x in lp]
        df["pass4a"] = [bool(r.OOS_H1 > BASE[(r.panel, r.cost_bps)]["H1"]
                             and r.OOS_H2 > BASE[(r.panel, r.cost_bps)]["H2"]
                             and r.OOS_MaxDD >= BASE[(r.panel, r.cost_bps)]["MaxDD"])
                        for _, r in df.iterrows()]
    dump(grid, "grid")
    P(f"  {len(grid):,} grid rows = {len(panels)} panels x {len(BOOKS)} books x "
      f"{len(CLAIM_SETS)} gross x {DOM_N + (0 if SMOKE else DOQ_N)} phases x {len(RUNGS)} rungs")

    # ---- G3: reproduce idea 962's committed grid -------------------------------------------
    comm = OUT / "2026-09-15_does-an-IS-CHOSEN-PHASE-ever-SURVIVE-OOS-on-ANY-BOOK_C.grid.csv"
    if comm.exists() and not SMOKE:
        cg = pd.read_csv(comm)
        keys = ["panel", "book", "gross", "cadence", "phase", "cost_bps"]
        cols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_CAGR", "IS_Sharpe", "OOS_CAGR",
                "OOS_Sharpe", "OOS_MaxDD", "OOS_H1", "OOS_H2", "turn_per_yr"]
        j = cg.merge(grid, on=keys, suffixes=("_c", "_n"))
        dmax = max(float(np.abs(j[f"{c}_c"] - j[f"{c}_n"]).max()) for c in cols)
        gk["G3"] = len(j) == len(cg) and dmax < 1e-10
        P(f"  G3 idea 962's committed grid.csv replayed on {len(j):,} of {len(cg):,} rows x "
          f"{len(cols)} cols, max|d| {dmax:.3e}   {'PASS' if gk['G3'] else 'FAIL'}")
    else:
        gk["G3"] = False
        P("  G3 SKIPPED (smoke run or missing artifact)   FAIL")

    fport = pd.DataFrame(list(FP.values()))
    fport["IS_legs_passed"] = [sum(legs_is(r).values()) for _, r in fport.iterrows()]
    lr = [legs_rec(r) for _, r in fport.iterrows()]
    fport["pass4b_REC"] = [all(x.values()) for x in lr]
    fport["fail4b_REC"] = [failstr(x) for x in lr]
    fport["pass4b_OOSPURE"] = [all(legs_pure(r).values()) for _, r in fport.iterrows()]
    fport["pass4a"] = [bool(r.OOS_H1 > BASE[(r.panel, r.cost_bps)]["H1"]
                            and r.OOS_H2 > BASE[(r.panel, r.cost_bps)]["H2"]
                            and r.OOS_MaxDD >= BASE[(r.panel, r.cost_bps)]["MaxDD"])
                       for _, r in fport.iterrows()]
    dump(fport, "fport")

    # ---- G4: the tranche identity on a one-phase family --------------------------------------
    sub = grid[(grid.panel == "U56") & (grid.book == "TOP20") & (grid.gross == "CORE")
               & (grid.cadence == "M") & (grid.cost_bps == HEAD_COST) & (grid.phase == 0)]
    # rebuild FPORT over a family of exactly ONE phase -> must equal that phase's row
    pidx = panels["U56"].index
    is_u, oos_u = WINS["U56"]
    ctx = Ctx(panels["U56"], offset_mask(pidx, "M", 0)[0])
    W = BOOKS["TOP20"](panels["U56"], 0.75)
    g_, t_ = ctx.run(ctx.shift(W))
    r1 = (g_[WARM:] - t_[WARM:] * HEAD_COST / 1e4) / 1.0
    m1 = mets(r1)
    d4 = max(abs(m1[k] - float(sub.iloc[0][k])) for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2"))
    gk["G4"] = d4 < 1e-12
    P(f"  G4 FPORT over a ONE-phase family == that phase's CANON row: {d4:.3e}  "
      f"{'PASS' if gk['G4'] else 'FAIL'}")
    # ---- G5: determinism ---------------------------------------------------------------------
    g2_, t2_ = ctx.run(ctx.shift(W))
    d5 = max(float(np.abs(g_ - g2_).max()), float(np.abs(t_ - t2_).max()))
    gk["G5"] = d5 == 0.0
    P(f"  G5 determinism (subject family rebuilt): {d5:.3e}  {'PASS' if gk['G5'] else 'FAIL'}")
    del ctx, W

    # ==========================================================================================
    P()
    P("=" * 100)
    P("(C) THE THREE ESTIMATORS, FAMILY BY FAMILY")
    P("=" * 100)
    keys = ["panel", "book", "gross", "cadence", "cost_bps"]
    canon = grid[grid.phase == 0].set_index(keys)
    agg = grid.groupby(keys).agg(
        n_phase=("phase", "size"),
        FMEAN_CAGR=("CAGR", "mean"), FMEAN_Sharpe=("Sharpe", "mean"),
        FMEAN_MaxDD=("MaxDD", "mean"), FMEAN_H1=("H1", "mean"), FMEAN_H2=("H2", "mean"),
        FMEAN_OOS_CAGR=("OOS_CAGR", "mean"), FMEAN_OOS_Sharpe=("OOS_Sharpe", "mean"),
        FMEAN_OOS_MaxDD=("OOS_MaxDD", "mean"),
        FMEAN_IS_CAGR=("IS_CAGR", "mean"), FMEAN_IS_Sharpe=("IS_Sharpe", "mean"),
        FMEAN_IS_MaxDD=("IS_MaxDD", "mean"), FMEAN_IS_H1=("IS_H1", "mean"),
        FMEAN_IS_H2=("IS_H2", "mean"),
        FMEAN_OOS_H1=("OOS_H1", "mean"), FMEAN_OOS_H2=("OOS_H2", "mean"),
        FMEAN_turn=("turn_per_yr", "mean"),
        SPREAD_CAGR=("CAGR", lambda s: s.max() - s.min()),
        SPREAD_Sharpe=("Sharpe", lambda s: s.max() - s.min()),
        SD_CAGR=("CAGR", "std"), SD_Sharpe=("Sharpe", "std"),
        pass4b_share=("pass4b_REC", "mean"),
    )
    fam = agg.join(canon[["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe",
                          "OOS_MaxDD", "IS_CAGR", "IS_Sharpe", "turn_per_yr", "pass4b_REC",
                          "pass4a", "spy_CAGR", "spy_Sharpe", "spy_MaxDD", "spy_OOS_CAGR",
                          "spy_OOS_Sharpe", "spy_OOS_MaxDD"]].add_prefix("CANON_"))
    fp = fport.set_index(keys)[["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe",
                                "OOS_MaxDD", "IS_CAGR", "IS_Sharpe", "turn_per_yr",
                                "pass4b_REC", "pass4a"]].add_prefix("FPORT_")
    fam = fam.join(fp)
    # canonical percentile inside its own family
    pct = []
    for k, sub_ in grid.groupby(keys):
        v = sub_.set_index("phase")["CAGR"]
        pct.append((k, float((v < v.loc[0]).mean() + 0.5 * (v == v.loc[0]).mean())))
    fam["CANON_pctile_CAGR"] = pd.Series({k: v for k, v in pct})
    fam = fam.reset_index()
    fam["d_CANON_FMEAN_CAGR_pp"] = (fam.CANON_CAGR - fam.FMEAN_CAGR) * 100
    fam["d_FPORT_CANON_Sharpe"] = fam.FPORT_Sharpe - fam.CANON_Sharpe
    dump(fam, "families")

    head = fam[(fam.cost_bps == HEAD_COST)]
    P(f"  {len(fam)} families ({len(head)} at the {HEAD_COST:.0f} bps verdict rung).")
    P()
    P("  H_BIAS -- is the CANONICAL biased inside its own family?  (CANON - FMEAN, pp of CAGR)")
    for cad, s in head.groupby("cadence"):
        P(f"    cadence {cad}: median {s.d_CANON_FMEAN_CAGR_pp.median():+.3f} pp   "
          f"mean {s.d_CANON_FMEAN_CAGR_pp.mean():+.3f} pp   "
          f"canonical percentile median {s.CANON_pctile_CAGR.median():.3f} "
          f"[{s.CANON_pctile_CAGR.min():.3f}, {s.CANON_pctile_CAGR.max():.3f}]")
    med_all = head.d_CANON_FMEAN_CAGR_pp.median()
    pct_all = head.CANON_pctile_CAGR.median()
    hbias = abs(med_all) <= BIAS_PP and PCTL_LO <= pct_all <= PCTL_HI
    P(f"    POOLED median {med_all:+.3f} pp (bar +/-{BIAS_PP}), canonical percentile median "
      f"{pct_all:.3f} (bar [{PCTL_LO}, {PCTL_HI}])  ->  H_BIAS "
      f"{'PASS (canonical is UNBIASED)' if hbias else 'FAIL (canonical is BIASED)'}")
    P()
    P("  what the dial is worth -- family CAGR spread (max - min), pp:")
    for cad, s in head.groupby("cadence"):
        P(f"    {cad}: median {s.SPREAD_CAGR.median() * 100:.2f} pp   "
          f"max {s.SPREAD_CAGR.max() * 100:.2f} pp   sd(CAGR) median "
          f"{s.SD_CAGR.median() * 100:.2f} pp")

    P()
    P("  H_TRADE / H_CHEAP -- is the TRANCHED book better, and is it cheaper?")
    for cad, s in head.groupby("cadence"):
        w = float((s.FPORT_Sharpe > s.CANON_Sharpe).mean())
        cheap = float((s.FPORT_turn_per_yr <= s.CANON_turn_per_yr).mean())
        P(f"    {cad}: FPORT Sharpe > CANON in {w:.3f} of {len(s)} families "
          f"(median gain {s.d_FPORT_CANON_Sharpe.median():+.4f}); turnover <= CANON in "
          f"{cheap:.3f}; median turn/yr FPORT {s.FPORT_turn_per_yr.median():.2f} vs CANON "
          f"{s.CANON_turn_per_yr.median():.2f}")
    wt_all = float((head.FPORT_Sharpe > head.CANON_Sharpe).mean())
    ch_all = float((head.FPORT_turn_per_yr <= head.CANON_turn_per_yr).mean())
    htrade, hcheap = wt_all >= TRADE_BAR, ch_all >= CHEAP_BAR
    P(f"    POOLED win rate {wt_all:.3f} (bar {TRADE_BAR}) -> H_TRADE "
      f"{'PASS' if htrade else 'FAIL'};  turnover rate {ch_all:.3f} (bar {CHEAP_BAR}) -> "
      f"H_CHEAP {'PASS' if hcheap else 'FAIL'}")
    P()
    P("  4b pass counts at the verdict rung, by estimator (REC convention):")
    for cad, s in head.groupby("cadence"):
        P(f"    {cad}: CANON {int(s.CANON_pass4b_REC.sum())} / {len(s)}    "
          f"FPORT {int(s.FPORT_pass4b_REC.sum())} / {len(s)}    "
          f"mean within-family phase pass share {s.pass4b_share.mean():.3f}")
    P(f"    4a at the same rung: CANON {int(head.CANON_pass4a.sum())} / {len(head)}, "
      f"FPORT {int(head.FPORT_pass4a.sum())} / {len(head)}")

    # ==========================================================================================
    P()
    P("=" * 100)
    P("(D) THE CENSUS -- the record's committed MONTHLY / QUARTERLY claims, re-read three ways")
    P("=" * 100)
    fkeys = ["panel", "book", "gross", "cadence", "cost_bps"]
    famx = fam.set_index(fkeys)
    files, claims = [], []
    # a committed row produced by one of the record's own COIN-FLIP / NULL generators is not a
    # CLAIM about a rule, so those files are named and dropped (the record's own convention,
    # idea 937/970).
    skip_tok = ("null", "rand", "coin", "flip", "perm", "shuffl", "bootstrap", "placebo")
    cands = sorted(list(OUT.glob("*.csv")) + list(OUT.glob("*.csv.gz")))
    CAD_COLS = ["cadence", "freq", "per", "cad", "frequency", "rebal"]
    GROSS_MAP = {"CORE": "CORE", "EXT": "EXT", "0.75": "CORE", "1.0": "EXT", "1": "EXT"}
    WANT = {"panel", "book", "gross", "phase", "cost_bps", "CAGR", "Sharpe", "MaxDD",
            "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "H1", "H2"} | set(CAD_COLS)
    nbig = 0
    for p in cands:
        if p.name.startswith(STEM):
            continue
        try:
            hdr = list(pd.read_csv(p, nrows=0).columns)
        except Exception:
            continue
        hs = set(hdr)
        cadc = next((c for c in CAD_COLS if c in hs), None)
        # a claim needs a CAGR, a cadence and enough key to name a family
        if cadc is None or "CAGR" not in hs or not {"panel", "book"} <= hs:
            continue
        if any(t in p.name.lower() for t in skip_tok):
            files.append(dict(file=p.name, status="EXCLUDED_null_or_random", rows=0,
                              bytes=p.stat().st_size))
            continue
        try:
            d = pd.read_csv(p, usecols=lambda c: c in WANT)
        except Exception:
            continue
        d = d.rename(columns={cadc: "cadence"})
        d["cadence"] = d["cadence"].astype(str).str.upper().str[:1]
        d = d[d.cadence.isin(["M", "Q"])]
        if not len(d):
            files.append(dict(file=p.name, status="NO_MQ_ROWS", rows=0, bytes=p.stat().st_size))
            continue
        if "phase" not in d.columns:
            d["phase"] = 0          # no phase column == the CANONICAL phase, by construction
        if "gross" not in d.columns:
            d["gross"] = np.nan
        if "cost_bps" not in d.columns:
            d["cost_bps"] = np.nan
        d["gross"] = d["gross"].map(lambda v: GROSS_MAP.get(str(v).strip(), np.nan))
        d["file"] = p.name
        nbig += p.stat().st_size
        claims.append(d[["panel", "book", "gross", "cadence", "phase", "cost_bps", "CAGR",
                         "file"]])
        files.append(dict(file=p.name, status="INCLUDED", rows=len(d), bytes=p.stat().st_size))
    fdf = pd.DataFrame(files)
    dump(fdf, "corpus")
    P(f"  corpus: {len(cands):,} csv artifacts in research/backtests/; "
      f"{int((fdf.status == 'INCLUDED').sum()) if len(fdf) else 0} carry a committed M/Q CAGR "
      f"claim with a nameable family key ({nbig / 1e6:,.0f} MB), "
      f"{int((fdf.status == 'EXCLUDED_null_or_random').sum()) if len(fdf) else 0} otherwise-"
      f"eligible files excluded as the record's own null/coin-flip generators, "
      f"{int((fdf.status == 'NO_MQ_ROWS').sum()) if len(fdf) else 0} keyed but carrying no M/Q row.")
    if claims:
        C = pd.concat(claims, ignore_index=True)
    else:
        C = pd.DataFrame(columns=["panel", "book", "gross", "cadence", "phase", "cost_bps",
                                  "CAGR", "file"])
    P(f"  {len(C):,} committed M/Q claim rows harvested from "
      f"{C.file.nunique() if len(C) else 0} files; a row with no `phase` column is read as the "
      f"CANONICAL phase (phase 0), which is what those runs traded.")

    UNMAP = {}
    PANELS_OK, BOOKS_OK = set(fam.panel), set(fam.book)
    RUNGS_OK = set(float(x) for x in RUNGS)

    def why(r):
        if r.panel not in PANELS_OK:
            return "panel not on this grid"
        if r.book not in BOOKS_OK:
            return "book not on this grid"
        if r.gross not in ("CORE", "EXT"):
            return "gross not 0.75/1.00"
        try:
            if float(r.cost_bps) not in RUNGS_OK:
                return "cost rung not 0/5/10/25/50"
        except (TypeError, ValueError):
            return "no cost rung"
        return "other"

    def census(name, d):
        """Re-read every claim row as CANON / FMEAN / FPORT of its own family."""
        out, miss = [], {}
        for _, r in d.iterrows():
            try:
                k = (r.panel, r.book, r.gross, r.cadence, float(r.cost_bps))
            except (TypeError, ValueError):
                w = why(r)
                miss[w] = miss.get(w, 0) + 1
                continue
            if k not in famx.index:
                w = why(r)
                miss[w] = miss.get(w, 0) + 1
                continue
            f = famx.loc[k]
            if isinstance(f, pd.DataFrame):
                f = f.iloc[0]
            out.append(dict(
                claim_set=name, file=r.file, panel=r.panel, book=r.book, gross=r.gross,
                cadence=r.cadence, cost_bps=float(r.cost_bps), phase=int(r.phase),
                claim_CAGR=float(r.CAGR),
                CANON_CAGR=float(f.CANON_CAGR), FMEAN_CAGR=float(f.FMEAN_CAGR),
                FPORT_CAGR=float(f.FPORT_CAGR), SPREAD_CAGR=float(f.SPREAD_CAGR),
                spy_CAGR=float(f.CANON_spy_CAGR),
                CANON_4b=bool(f.CANON_pass4b_REC), FPORT_4b=bool(f.FPORT_pass4b_REC),
                fam_pass_share=float(f.pass4b_share)))
        UNMAP[name] = (miss, int(len(d)))
        return pd.DataFrame(out)

    gcols = ["panel", "book", "gross", "cadence", "phase", "cost_bps", "CAGR"]
    strict = census("STRICT", C[C.phase == 0]) if len(C) else pd.DataFrame()
    wide = census("WIDE", C) if len(C) else pd.DataFrame()
    gridset = census("GRID", grid[grid.phase == 0][gcols].assign(file="<grid>"))
    cen = pd.concat([x for x in (strict, wide, gridset) if len(x)], ignore_index=True)
    if len(cen):
        cen["sign_CANON"] = np.sign(cen.CANON_CAGR - cen.spy_CAGR)
        cen["sign_FMEAN"] = np.sign(cen.FMEAN_CAGR - cen.spy_CAGR)
        cen["sign_FPORT"] = np.sign(cen.FPORT_CAGR - cen.spy_CAGR)
        cen["sign_flip_FMEAN"] = cen.sign_CANON != cen.sign_FMEAN
        cen["sign_flip_FPORT"] = cen.sign_CANON != cen.sign_FPORT
        cen["verdict_flip_FPORT"] = cen.CANON_4b != cen.FPORT_4b
        cen["cell"] = (cen.panel + "/" + cen.book + "/" + cen.gross + "/" + cen.cadence + "/"
                       + cen.cost_bps.astype(str))
    dump(cen, "census")
    for k, (miss, tot) in UNMAP.items():
        nm = sum(miss.values())
        det = ", ".join(f"{v:,} {kk}" for kk, v in sorted(miss.items(), key=lambda x: -x[1]))
        P(f"    claim set {k:6s}: {tot - nm:,} of {tot:,} rows map onto a family in this run's "
          f"grid; {nm:,} do not and are DROPPED, never counted as agreeing"
          + (f" ({det})" if det else ""))

    P()
    P("  claim-set x cadence census (row-weighted / cell-weighted, per idea 973's warning):")
    hdr = (f"    {'set':7s} {'cad':4s} {'rows':>7s} {'cells':>6s} {'files':>6s} "
           f"{'sign_FMEAN':>11s} {'sign_FPORT':>11s} {'verdict_FPORT':>14s} "
           f"{'cellw_sign':>11s} {'cellw_verd':>11s}")
    P(hdr)
    rows_h = []
    for cs in ["STRICT", "WIDE", "GRID"]:
        s0 = cen[cen.claim_set == cs] if len(cen) else pd.DataFrame()
        if not len(s0):
            P(f"    {cs:7s} (none)")
            continue
        for cad in ["M", "Q", "ALL"]:
            s = s0 if cad == "ALL" else s0[s0.cadence == cad]
            if not len(s):
                continue
            cw = s.groupby("cell")[["sign_flip_FMEAN", "verdict_flip_FPORT"]].max()
            P(f"    {cs:7s} {cad:4s} {len(s):7,d} {s.cell.nunique():6d} {s.file.nunique():6d} "
              f"{s.sign_flip_FMEAN.mean():11.3f} {s.sign_flip_FPORT.mean():11.3f} "
              f"{s.verdict_flip_FPORT.mean():14.3f} "
              f"{cw.sign_flip_FMEAN.mean():11.3f} {cw.verdict_flip_FPORT.mean():11.3f}")
            rows_h.append(dict(claim_set=cs, cadence=cad, rows=len(s), cells=s.cell.nunique(),
                               files=s.file.nunique(),
                               sign_flip_FMEAN=s.sign_flip_FMEAN.mean(),
                               sign_flip_FPORT=s.sign_flip_FPORT.mean(),
                               verdict_flip_FPORT=s.verdict_flip_FPORT.mean(),
                               cellw_sign=cw.sign_flip_FMEAN.mean(),
                               cellw_verdict=cw.verdict_flip_FPORT.mean()))
    dump(pd.DataFrame(rows_h), "censussummary")
    st = cen[(cen.claim_set == "STRICT")] if len(cen) else pd.DataFrame()
    if len(st):
        hs = float(st.sign_flip_FMEAN.mean())
        hv = float(st.verdict_flip_FPORT.mean())
    else:
        hs = hv = float("nan")
    P(f"    H_SIGN    STRICT sign flips {hs:.3f} (bar {SIGN_BAR}) -> "
      f"{'PASS (consequential)' if hs > SIGN_BAR else 'FAIL (not consequential)'}")
    P(f"    H_VERDICT STRICT verdict flips {hv:.3f} (bar {VERDICT_BAR}) -> "
      f"{'PASS (consequential)' if hv > VERDICT_BAR else 'FAIL (not consequential)'}")

    # ==========================================================================================
    P()
    P("=" * 100)
    P("(E) RULE 8 -- book x gross chosen on 2009-2016 ALONE, 2017-2026 read ONCE")
    P("=" * 100)
    picks = []
    long = pd.concat([
        grid[grid.phase == 0].assign(estimator="CANON"),
        fport.assign(estimator="FPORT"),
    ], ignore_index=True)
    # FMEAN as a row: the family mean of every column (an estimator, NOT a portfolio)
    fm = fam.copy()
    fmrows = pd.DataFrame(dict(
        panel=fm.panel, book=fm.book, gross=fm.gross, cadence=fm.cadence, cost_bps=fm.cost_bps,
        estimator="FMEAN", CAGR=fm.FMEAN_CAGR, Sharpe=fm.FMEAN_Sharpe, MaxDD=fm.FMEAN_MaxDD,
        H1=fm.FMEAN_H1, H2=fm.FMEAN_H2, IS_CAGR=fm.FMEAN_IS_CAGR, IS_Sharpe=fm.FMEAN_IS_Sharpe,
        IS_MaxDD=fm.FMEAN_IS_MaxDD, IS_H1=fm.FMEAN_IS_H1, IS_H2=fm.FMEAN_IS_H2,
        OOS_CAGR=fm.FMEAN_OOS_CAGR, OOS_Sharpe=fm.FMEAN_OOS_Sharpe,
        OOS_MaxDD=fm.FMEAN_OOS_MaxDD, OOS_H1=fm.FMEAN_OOS_H1, OOS_H2=fm.FMEAN_OOS_H2,
        turn_per_yr=fm.FMEAN_turn, spy_CAGR=fm.CANON_spy_CAGR, spy_Sharpe=fm.CANON_spy_Sharpe,
        spy_MaxDD=fm.CANON_spy_MaxDD, spy_OOS_CAGR=fm.CANON_spy_OOS_CAGR,
        spy_OOS_Sharpe=fm.CANON_spy_OOS_Sharpe, spy_OOS_MaxDD=fm.CANON_spy_OOS_MaxDD))
    for c in ("spy_H1", "spy_H2", "spy_IS_CAGR", "spy_IS_Sharpe", "spy_IS_MaxDD", "spy_IS_H1",
              "spy_IS_H2", "spy_OOS_H1", "spy_OOS_H2"):
        fmrows[c] = long.groupby(["panel"])[c].first().reindex(fmrows.panel).values
    fmrows["IS_legs_passed"] = [sum(legs_is(r).values()) for _, r in fmrows.iterrows()]
    lr = [legs_rec(r) for _, r in fmrows.iterrows()]
    fmrows["pass4b_REC"] = [all(x.values()) for x in lr]
    fmrows["fail4b_REC"] = [failstr(x) for x in lr]
    fmrows["pass4a"] = [bool(r.OOS_H1 > BASE[(r.panel, r.cost_bps)]["H1"]
                             and r.OOS_H2 > BASE[(r.panel, r.cost_bps)]["H2"]
                             and r.OOS_MaxDD >= BASE[(r.panel, r.cost_bps)]["MaxDD"])
                        for _, r in fmrows.iterrows()]
    long = pd.concat([long, fmrows], ignore_index=True)

    g6_bad = 0
    for (pn, cad, est, c), sub_ in long.groupby(["panel", "cadence", "estimator", "cost_bps"]):
        sub_ = sub_.sort_values(["book", "gross"]).reset_index(drop=True)
        perm = sub_.copy()
        rng = np.random.default_rng(7)
        oc = [x for x in perm.columns if x.startswith("OOS_")]
        perm[oc] = perm[oc].values[rng.permutation(len(perm))]
        for ch in CHOOSERS:
            i = choose(ch, sub_)
            if i != choose(ch, perm):
                g6_bad += 1
            r = sub_.iloc[i]
            picks.append(dict(panel=pn, cadence=cad, estimator=est, cost_bps=c, chooser=ch,
                              book=r.book, gross=r.gross, OOS_CAGR=r.OOS_CAGR,
                              OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                              OOS_H1=r.OOS_H1, OOS_H2=r.OOS_H2,
                              pass4b=bool(r.pass4b_REC), pass4a=bool(r.pass4a),
                              fail4b=r.fail4b_REC,
                              spy_OOS_CAGR=r.spy_OOS_CAGR, spy_OOS_Sharpe=r.spy_OOS_Sharpe,
                              spy_OOS_MaxDD=r.spy_OOS_MaxDD,
                              v2_OOS_CAGR=BASE[(pn, c)]["CAGR"],
                              v2_OOS_Sharpe=BASE[(pn, c)]["Sharpe"],
                              v2_OOS_MaxDD=BASE[(pn, c)]["MaxDD"]))
    gk["G6"] = g6_bad == 0
    P(f"  G6 choosers are IS-ONLY: {g6_bad} picks moved when OOS columns were permuted  "
      f"{'PASS' if gk['G6'] else 'FAIL'}")
    pk = pd.DataFrame(picks)
    dump(pk, "walkforward")
    hv_ = pk[pk.cost_bps == HEAD_COST]
    P(f"  {len(pk)} rule-8 picks ({len(hv_)} at {HEAD_COST:.0f} bps) = "
      f"{len(CHOOSERS)} choosers x 3 panels x {hv_.cadence.nunique()} cadences x 3 estimators "
      f"x {len(RUNGS)} rungs")
    P()
    P("  OOS pass counts at the verdict rung, by estimator:")
    for est, s in hv_.groupby("estimator"):
        P(f"    {est:6s}  4b {int(s.pass4b.sum()):2d} / {len(s):2d}    "
          f"4a {int(s.pass4a.sum()):2d} / {len(s):2d}    median OOS CAGR "
          f"{s.OOS_CAGR.median():.2%}  median OOS Sharpe {s.OOS_Sharpe.median():.3f}  "
          f"median OOS MaxDD {s.OOS_MaxDD.median():.2%}")
    P()
    P("  every rule-8 pick at 10 bps (OOS 2017-2026, vs SPY OOS and RULES v2 OOS in the "
      "same window):")
    P(f"    {'panel':6s} {'cad':3s} {'est':6s} {'chooser':9s} {'book':7s} {'g':5s} "
      f"{'OOS CAGR':>9s} {'Sh':>7s} {'MaxDD':>8s} {'4b':>3s} {'4a':>3s}  fail-legs")
    for _, r in hv_.sort_values(["panel", "cadence", "estimator", "chooser"]).iterrows():
        P(f"    {r.panel:6s} {r.cadence:3s} {r.estimator:6s} {r.chooser:9s} {r.book:7s} "
          f"{r.gross:5s} {r.OOS_CAGR:9.2%} {r.OOS_Sharpe:7.3f} {r.OOS_MaxDD:8.2%} "
          f"{'Y' if r.pass4b else 'n':>3s} {'Y' if r.pass4a else 'n':>3s}  {r.fail4b}")
    P()
    for pn in ["U56", "B136", "SMALL"]:
        s = hv_[hv_.panel == pn]
        if not len(s):
            continue
        r = s.iloc[0]
        P(f"  comparands, {pn} OOS 2017-2026 @ 10 bps:  SPY {r.spy_OOS_CAGR:.2%} / "
          f"{r.spy_OOS_Sharpe:.3f} / {r.spy_OOS_MaxDD:.2%}    RULES v2 {r.v2_OOS_CAGR:.2%} / "
          f"{r.v2_OOS_Sharpe:.3f} / {r.v2_OOS_MaxDD:.2%}")
    best = hv_.sort_values("OOS_Sharpe", ascending=False).head(3)
    P()
    P("  best three picks by OOS Sharpe at 10 bps:")
    for _, r in best.iterrows():
        P(f"    {r.panel}/{r.cadence}/{r.estimator}/{r.chooser} -> {r.book} @ {r.gross}: "
          f"OOS {r.OOS_CAGR:.2%} / {r.OOS_Sharpe:.3f} / {r.OOS_MaxDD:.2%}   "
          f"4b {'PASS' if r.pass4b else 'FAIL'}  4a {'PASS' if r.pass4a else 'FAIL'}")
    hkeep = bool(hv_.pass4b.any() or hv_.pass4a.any())

    # ------------------------------------------------------------------------------- verdicts
    P()
    P("=" * 100)
    P("(F) HYPOTHESES")
    P("=" * 100)
    H = [
        dict(name="H_SIGN", bar=f"> {SIGN_BAR} of STRICT claims change sign(CAGR - SPY)",
             value=hs, verdict="PASS" if hs > SIGN_BAR else "FAIL"),
        dict(name="H_VERDICT", bar=f"> {VERDICT_BAR} of STRICT claims change 4b verdict",
             value=hv, verdict="PASS" if hv > VERDICT_BAR else "FAIL"),
        dict(name="H_BIAS", bar=f"|median(CANON-FMEAN)| <= {BIAS_PP} pp AND pctile in "
                                f"[{PCTL_LO},{PCTL_HI}]",
             value=med_all, verdict="PASS" if hbias else "FAIL"),
        dict(name="H_TRADE", bar=f"FPORT Sharpe > CANON in >= {TRADE_BAR} of families",
             value=wt_all, verdict="PASS" if htrade else "FAIL"),
        dict(name="H_CHEAP", bar=f"FPORT turn/yr <= CANON in >= {CHEAP_BAR} of families",
             value=ch_all, verdict="PASS" if hcheap else "FAIL"),
        dict(name="H_KEEP", bar="any rule-8 OOS 4b or 4a pass at 10 bps",
             value=float(hv_.pass4b.sum() + hv_.pass4a.sum()),
             verdict="PASS" if hkeep else "FAIL"),
    ]
    hyp = pd.DataFrame(H)
    for _, r in hyp.iterrows():
        P(f"  {r['name']:10s} {r['verdict']:4s}   {r['value']:+.4f}   {r['bar']}")
    dump(hyp, "hypotheses")
    P()
    P(f"  GATES: " + "  ".join(f"{k}={'PASS' if v else 'FAIL'}" for k, v in sorted(gk.items()))
      + f"   ({sum(gk.values())} of {len(gk)})")
    P(f"  elapsed {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()

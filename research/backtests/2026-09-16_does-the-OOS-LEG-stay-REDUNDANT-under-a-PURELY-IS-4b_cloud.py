#!/usr/bin/env python3
"""
Idea 972 (cloud lane, 2026-09-16)
DOES THE OOS LEG STAY REDUNDANT UNDER A PURELY IN-SAMPLE 4b?

  4b has five legs.  In the record's standard form (`LS_REC`) two of them read the FULL
  sample's halves and three read the OOS window:
      L1_H1   Sharpe(H1 of the full post-warm-up sample) > SPY's H1
      L2_H2   Sharpe(H2)                                  > SPY's H2
      L3_OOS  OOS Sharpe                                  > SPY's OOS Sharpe
      L4_DD   |OOS MaxDD|                                 <= 0.60 x |SPY full MaxDD|
      L5_CAGR OOS CAGR                                    >= 0.70 x SPY full CAGR

  Idea 942 blamed L3_OOS's redundancy -- P(all five legs) / P(the other four) = 1.0000 --
  on the WINDOW OVERLAP between the full sample's second half and the OOS window.  Idea 970
  killed that explanation: moving the halves INSIDE 2009-2016 (`LS_970`) leaves the ratio at
  1.0000 on U56/M and U56/Q, so the overlap is not what makes L3_OOS free.

  The queue asks the obvious next question: read the DD and CAGR legs IN-SAMPLE TOO -- a
  FULLY IN-SAMPLE 4b (`LS_ISALL`) plus ONE UNTOUCHED OOS READ -- and report WHICH LEG, IF
  ANY, EVER CHANGES A VERDICT.

THE ESTIMATOR.  For a leg L inside a leg set, the REDUNDANCY RATIO is
      R(L) = P(all five legs) / P(the other four)
over the published row population.  R(L) = 1.0000 means L NEVER binds: every book that
clears the other four clears L too, so the leg carries no information and the bar is really
a four-leg bar.  R(L) < 1 means L refuses somebody, and the count of those rows
(`n_binding`) is literally "how many verdicts this leg changes".

TUNED AXES -- exactly two, as the queue line allows, every level reported, none selected:
  (1) leg set : LS_REC   -- the record's standard 4b (halves full-sample, L3/L4/L5 on OOS)
                LS_970   -- 970's: halves moved inside 2009-2016, L3/L4/L5 still on OOS
                LS_ISALL -- the queue's ask: ALL FIVE legs read on 2009-2016 alone
  (2) panel   : U56 / B136 / SMALL
Everything else -- book, gross, cadence, rebalance phase, cost rung -- is a REPORTED ladder
of 13,500 rows, published in full.  Nothing is chosen on any of it.

PRE-REGISTERED HYPOTHESES (bars fixed before any number was read):
  H_970    : 970's finding reproduces -- R(L3_OOS) = 1.0000 under LS_970 on U56 at M and Q.
  H_ISRED  : under LS_ISALL the Sharpe leg STAYS redundant -- R(L3_SHARPE) >= 0.95 on every
             panel.  PASS means reading the leg in sample does not rescue it.
  H_BIND   : >= 1 leg BINDS under LS_ISALL on >= 1 panel (n_binding >= 1).  This is the
             queue's literal question, "which leg, if any, ever changes a verdict".
  H_SAME   : the fully-IS 4b verdict agrees with the record's OOS 4b verdict on >= 0.90 of
             rows.  FAIL means an IS-only 4b is NOT a usable stand-in for the real bar.
  H_ORDER  : the BINDING ORDER of the five legs (which refuses most rows) is the same in
             sample and out -- Spearman(rank_IS, rank_OOS) >= +0.50.
  H_R8     : an IS-only 4b chooser reaches OOS 4b in >= 1 of its picks.
  H_4A     : >= 1 OOS 4a anywhere in this run.

GATES (printed before any hypothesis number):
  G0  offset_mask(idx, per, d) == engine.rebalance_mask(idx, per) at d = 0, on D/W/M/Q
  G1  the fast Ctx runner == engine.backtest on returns AND turnover, post warm-up
  G2  BAND03 @ 0.75 == baseline.rules_v2_weights elementwise
  G3  CROSS-RUN: idea 993's committed 13,500-row ladder reproduced column by column --
      the SAME axes, the SAME phases, the SAME cost rungs, rebuilt from scratch
  G4  LEG IDENTITY: this run's LS_REC verdict == 993's committed `pass4b` column on all
      13,500 rows (0 disagreements) -- proof the leg set being varied is the record's
  G5  determinism: one ladder cell rebuilt from scratch
  G6  SMALL panel hygiene: the max_1d_move >= 1.0 drop count from data/small_meta.csv
  G7  WINDOW DISJOINTNESS: the IS and OOS masks share 0 trading days on every panel

PROTOCOL: 10 bps primary (0/5/10/25/50 all built), decided at close t / applied t+1
(LAG 1), warm-up 260 days, IS 2009-2016 / OOS 2017-2026 read ONCE, no shorting, no leverage
beyond the published gross.  Rule 8 walk-forward is carried explicitly: three IS-ONLY
choosers pick (book, gross) inside each (panel, cadence) on 2009-2016 alone, the OOS window
is read once, and OOS CAGR / Sharpe / MaxDD are reported against SPY and against the live
RULES v2 baseline.  Both KEEP paths (4a against RULES v2, 4b against SPY) are evaluated at
EVERY grid point.  Nothing in RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py is
modified.

SURVIVORSHIP (rule 9): U56, B136 and SMALL are CURRENT-CONSTITUENT lists (SMALL additionally
drops every ticker with max_1d_move >= 1.0 per data/small_meta.csv).  Every CAGR and drawdown
LEVEL is optimistic and every 4b and 4a count is an UPPER bound, most severely on SMALL.  The
measured object is a REDUNDANCY RATIO -- a ratio of two pass rates over the same rows on the
same tape -- so a bias that lifts both numerator and denominator largely cancels; what does
NOT cancel is that an optimistic panel pushes MORE rows over every level bar at once, which
makes a leg look MORE redundant than it is.  Every R(L) reported here is therefore an UPPER
bound on redundancy, i.e. a CONSERVATIVE reading of how often a leg binds.

  SMOKE=1 trims the phase families and the cost ladder for wiring checks only.
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
from baseline import load_universe, rules_v2_weights, band_state, score  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

SMOKE = os.environ.get("SMOKE") == "1"

# ---- reported constants (never tuned) ---------------------------------------------------
WARM = 260
LAG = 1
BAND0 = 0.03
VOLCAP = 0.60
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
HEAD_COST = 10.0
RUNGS = [0.0, 5.0, 10.0, 25.0, 50.0] if not SMOKE else [10.0]
GROSSES = {"CORE": 0.75, "EXT": 1.00}
CADENCES = {"D": 1, "W": 5, "M": 21, "Q": 63} if not SMOKE else {"D": 1, "W": 5, "M": 3, "Q": 3}
CADORDER = ["D", "W", "M", "Q"]
PANELS = ["U56", "B136", "SMALL"]

LEGKEYS = ["H1", "H2", "SHARPE", "DD", "CAGR"]
LEGNAME = {"H1": "L1_H1", "H2": "L2_H2", "SHARPE": "L3_OOS", "DD": "L4_DD",
           "CAGR": "L5_CAGR"}
LEGSETS = ["LS_REC", "LS_970", "LS_ISALL"]
HEAD_LEGSET = "LS_ISALL"
CHOOSERS = ["C_IS4B", "C_ISSHARPE", "C_ISCAGR"]

# pre-registered bars
BAR_ISRED = 0.95
BAR_SAME = 0.90
BAR_ORDER = 0.50

PARENT_LADDER = OUT / "2026-09-16_is-REFUSAL-COST-a-CADENCE-object_cloud.ladder.csv"
G3_COLS = ["turn_per_yr", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_CAGR", "IS_Sharpe",
           "IS_MaxDD", "IS_H1", "IS_H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]
G3_TOL = 1e-9

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# =========================================================================================
# (1) engine machinery -- the record's form, verbatim
# =========================================================================================
def offset_mask(idx, per, d=0):
    if per == "D":
        return pd.Series(True, index=idx)
    key = pd.Series(idx.to_period({"W": "W", "M": "M", "Q": "Q"}[per]), index=idx)
    last = np.flatnonzero((key != key.shift(-1)).values)
    first = np.concatenate([[0], last[:-1] + 1])
    pick = np.maximum(last - d, first)
    out = pd.Series(False, index=idx)
    out.iloc[np.unique(pick)] = True
    return out


class Ctx:
    def __init__(self, px, mask):
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


def shift1(W, idx):
    return W.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values


def sharpe(r):
    """Zero-variance series -> Sharpe 0.0 by convention (the record's, see 993's FB_CASH)."""
    v = r.std() * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else 0.0


def maxdd(r):
    eq = np.cumprod(1.0 + r)
    return float((eq / np.maximum.accumulate(eq) - 1).min())


def mets(r):
    eq = np.cumprod(1.0 + r)
    yrs = len(r) / 252.0
    h = len(r) // 2
    return dict(CAGR=float(eq[-1] ** (1 / yrs) - 1) if yrs > 0 else np.nan,
                Sharpe=sharpe(r), MaxDD=maxdd(r), H1=sharpe(r[:h]), H2=sharpe(r[h:]))


# ---- the book set, verbatim from 942/962/964/976/980/981/984/986/993/996 ----------------
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
BOOKORDER = list(BOOKS)


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    return px[[c for c in px.columns if c == "SPY" or c not in bad]], len(bad)


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


def _argmax(v, tiebreak=None):
    v = np.asarray(v, float)
    if not np.isfinite(v).any():
        return None
    best = np.nanmax(v)
    cand = np.flatnonzero(v == best)
    if len(cand) > 1 and tiebreak is not None:
        t = np.asarray(tiebreak, float)[cand]
        cand = cand[np.flatnonzero(t == np.nanmax(t))]
    return int(cand[0])


# =========================================================================================
# (2) main
# =========================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 972 (cloud lane, 2026-09-16) -- DOES THE OOS LEG STAY REDUNDANT UNDER A PURELY "
      "IS 4b?")
    P("=" * 100)
    P(f"  SMOKE={SMOKE}  headline cost {HEAD_COST:.0f} bps  LAG={LAG}  WARM={WARM}")
    P(f"  tuned axes: leg set {LEGSETS} x panel {PANELS} -- ALL reported, none selected")
    P(f"  reported ladder (not tuned): book {BOOKORDER} x gross {list(GROSSES)} x cadence "
      f"{CADORDER} x phase {[CADENCES[c] for c in CADORDER]} x cost {RUNGS}")
    P(f"  R(L) = P(all five legs) / P(the other four).  R = 1.0000 means L never binds.")

    PX = {}
    PX["U56"] = load_universe()
    PX["B136"] = load_universe(broad=True)
    PX["SMALL"], n_dropped = load_small()
    P()
    for k, v in PX.items():
        P(f"  {k:6s} {v.shape[1]:4d} cols  {v.index[0].date()} .. {v.index[-1].date()}  "
          f"({len(v):,} rows)")
    P(f"  SMALL dropped {n_dropped} tickers with max_1d_move >= 1.0 (data/small_meta.csv)")

    # ---------------------------------------------------------------- gates A
    P()
    P("-" * 100)
    P("GATES -- printed before any hypothesis number")
    P("-" * 100)
    gates = []
    u56 = PX["U56"]
    bad = sum(int((offset_mask(u56.index, per).values != rebalance_mask(u56.index, per).values
                   ).sum()) for per in CADORDER)
    gates.append(dict(gate="G0", what="offset_mask(.,per,0) == engine.rebalance_mask D/W/M/Q",
                      value=float(bad), bar=0.0, ok=bad == 0))
    P(f"  G0  masks vs engine.rebalance_mask         : {bad} disagreeing rows")

    Wb = BOOKS["BAND03"](u56, 0.75)
    ref = backtest(u56, Wb, cost_bps=HEAD_COST, freq="W")
    cx = Ctx(u56, offset_mask(u56.index, "W"))
    r0, t0v = ctxrun = cx.run(shift1(Wb, u56.index))
    n0 = r0 - t0v * HEAD_COST / 1e4
    g1 = max(float(np.abs(n0[WARM:] - ref["returns"].values[WARM:]).max()),
             float(np.abs(t0v[WARM:] - ref["turnover"].values[WARM:]).max()))
    gates.append(dict(gate="G1", what="fast Ctx == engine.backtest (returns and turnover)",
                      value=g1, bar=1e-10, ok=g1 < 1e-10))
    P(f"  G1  Ctx vs engine.backtest                 : max|d| {g1:.3e}")

    g2 = float(np.abs(Wb.values - rules_v2_weights(u56).values).max())
    gates.append(dict(gate="G2", what="BAND03@0.75 == baseline.rules_v2_weights",
                      value=g2, bar=1e-12, ok=g2 < 1e-12))
    P(f"  G2  BAND03@0.75 vs rules_v2_weights        : max|d| {g2:.3e}")

    g7 = 0
    for p in PANELS:
        idx = PX[p].index
        g7 += int((np.asarray(idx <= pd.Timestamp(IS_END))
                   & np.asarray(idx >= pd.Timestamp(OOS_START))).sum())
    gates.append(dict(gate="G7", what="IS and OOS masks share 0 trading days on every panel",
                      value=float(g7), bar=0.0, ok=g7 == 0))
    P(f"  G7  IS/OOS window overlap                  : {g7} shared trading days")
    gates.append(dict(gate="G6", what="SMALL max_1d_move>=1.0 tickers dropped",
                      value=float(n_dropped), bar=1.0, ok=n_dropped >= 1))
    P(f"  G6  SMALL hygiene drop count               : {n_dropped}")

    # ---------------------------------------------------------------- build the ladder
    P()
    P("=" * 100)
    P("(A) THE LADDER -- 13,500 rows rebuilt from scratch (993's own axes)")
    P("=" * 100)
    rows = []
    NET = {}
    for pname in PANELS:
        px = PX[pname]
        idx = px.index
        rspy = px["SPY"].pct_change().fillna(0.0).values
        isw = np.asarray(idx <= pd.Timestamp(IS_END))[WARM:]
        osw = np.asarray(idx >= pd.Timestamp(OOS_START))
        spy_f = mets(rspy[WARM:])
        spy_is = mets(rspy[WARM:][isw])
        spy_o = mets(rspy[osw])
        v2n = backtest(px, rules_v2_weights(px), cost_bps=HEAD_COST, freq="W")["returns"].values
        v2 = mets(v2n[WARM:])
        tw = {(b, gn): shift1(BOOKS[b](px, gv), idx)
              for b in BOOKORDER for gn, gv in GROSSES.items()}
        for cad in CADORDER:
            for ph in range(CADENCES[cad]):
                c = Ctx(px, offset_mask(idx, cad, ph))
                for b in BOOKORDER:
                    for gn in GROSSES:
                        r, tu = c.run(tw[(b, gn)])
                        for cb in RUNGS:
                            net = r - tu * cb / 1e4
                            mf, mi, mo = mets(net[WARM:]), mets(net[WARM:][isw]), mets(net[osw])
                            rows.append(dict(
                                panel=pname, book=b, gross=gn, cadence=cad, phase=ph,
                                cost_bps=cb,
                                turn_per_yr=float(tu[WARM:].sum() / (len(tu[WARM:]) / 252.0)),
                                CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"],
                                H1=mf["H1"], H2=mf["H2"],
                                IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"],
                                IS_MaxDD=mi["MaxDD"], IS_H1=mi["H1"], IS_H2=mi["H2"],
                                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                OOS_MaxDD=mo["MaxDD"],
                                spy_CAGR=spy_f["CAGR"], spy_Sharpe=spy_f["Sharpe"],
                                spy_MaxDD=spy_f["MaxDD"], spy_H1=spy_f["H1"],
                                spy_H2=spy_f["H2"],
                                spy_IS_CAGR=spy_is["CAGR"], spy_IS_Sharpe=spy_is["Sharpe"],
                                spy_IS_MaxDD=spy_is["MaxDD"], spy_IS_H1=spy_is["H1"],
                                spy_IS_H2=spy_is["H2"],
                                spy_OOS_CAGR=spy_o["CAGR"], spy_OOS_Sharpe=spy_o["Sharpe"],
                                spy_OOS_MaxDD=spy_o["MaxDD"],
                                v2_Sharpe=v2["Sharpe"], v2_MaxDD=v2["MaxDD"],
                                v2_H1=v2["H1"], v2_H2=v2["H2"],
                                pass4a=bool(mf["H1"] > v2["H1"] and mf["H2"] > v2["H2"]
                                            and mf["MaxDD"] >= v2["MaxDD"])))
                            if cb == HEAD_COST and ph == 0:
                                NET[(pname, b, gn, cad)] = net
        P(f"  {pname:6s} done ({time.time()-t0:.0f}s, {len(rows):,} rows so far)")
    L = pd.DataFrame(rows)

    # ---- the three leg sets ---------------------------------------------------------
    def legmat(L, ls):
        if ls == "LS_REC":
            h1 = L.H1.values > L.spy_H1.values
            h2 = L.H2.values > L.spy_H2.values
        else:
            h1 = L.IS_H1.values > L.spy_IS_H1.values
            h2 = L.IS_H2.values > L.spy_IS_H2.values
        if ls == "LS_ISALL":
            sh = L.IS_Sharpe.values > L.spy_IS_Sharpe.values
            dd = np.abs(L.IS_MaxDD.values) <= DD_CAP * np.abs(L.spy_IS_MaxDD.values)
            cg = L.IS_CAGR.values >= CAGR_FLOOR * L.spy_IS_CAGR.values
        else:
            sh = L.OOS_Sharpe.values > L.spy_OOS_Sharpe.values
            dd = np.abs(L.OOS_MaxDD.values) <= DD_CAP * np.abs(L.spy_MaxDD.values)
            cg = L.OOS_CAGR.values >= CAGR_FLOOR * L.spy_CAGR.values
        return dict(H1=h1, H2=h2, SHARPE=sh, DD=dd, CAGR=cg)

    LEGM = {}
    for ls in LEGSETS:
        m = legmat(L, ls)
        LEGM[ls] = m
        allp = np.ones(len(L), bool)
        for k in LEGKEYS:
            allp &= m[k]
            L[f"{ls}_leg_{k}"] = m[k]
        L[f"{ls}_pass"] = allp
    L["fail_legs_REC"] = [",".join(LEGNAME[k] for k in LEGKEYS if not LEGM["LS_REC"][k][i])
                          or "-" for i in range(len(L))]
    dump(L, "ladder.csv")

    # ---------------------------------------------------------------- G3 / G4 / G5
    g3, g3n, g4, g4n = np.inf, "parent ladder not found", np.inf, "n/a"
    if PARENT_LADDER.exists():
        PL = pd.read_csv(PARENT_LADDER)
        key = ["panel", "book", "gross", "cadence", "phase", "cost_bps"]
        m = L.merge(PL, on=key, suffixes=("", "_p"))
        d = [float(np.abs(m[c].values - m[c + "_p"].values).max()) for c in G3_COLS
             if c + "_p" in m.columns]
        g3 = max(d) if d else np.inf
        g3n = f"{len(m):,} rows x {len(d)} cols"
        if "pass4b" in m.columns:
            g4 = float((m["LS_REC_pass"].values != m["pass4b"].values).sum())
            g4n = f"{len(m):,} rows"
    gates.append(dict(gate="G3", what=f"CROSS-RUN idea 993's 13,500-row ladder ({g3n})",
                      value=g3, bar=G3_TOL, ok=g3 < G3_TOL))
    P(f"  G3  cross-run vs 993's committed ladder    : max|d| {g3:.3e}  [{g3n}]")
    gates.append(dict(gate="G4", what=f"LS_REC verdict == 993's committed pass4b ({g4n})",
                      value=g4, bar=0.0, ok=g4 == 0))
    P(f"  G4  LS_REC verdict vs 993's pass4b column  : {g4:.0f} disagreements  [{g4n}]")

    cx = Ctx(u56, offset_mask(u56.index, "M", 0))
    rr, tt = cx.run(shift1(BOOKS["TOP20"](u56, 0.75), u56.index))
    g5 = float(np.abs((rr - tt * HEAD_COST / 1e4) - NET[("U56", "TOP20", "CORE", "M")]).max())
    gates.append(dict(gate="G5", what="determinism: one ladder cell rebuilt", value=g5,
                      bar=0.0, ok=g5 == 0.0))
    P(f"  G5  determinism (U56/TOP20/CORE/M ph 0)    : max|d| {g5:.3e}")
    G = pd.DataFrame(gates).sort_values("gate").reset_index(drop=True)
    dump(G, "gates.csv")
    P(f"  GATES: {int(G.ok.sum())} of {len(G)} PASS")

    # ================================================================== (B) redundancy
    P()
    P("=" * 100)
    P("(B) THE REDUNDANCY RATIO  R(L) = P(all five) / P(the other four)")
    P("=" * 100)

    def redrows(sub, tag_cols):
        out = []
        for ls in LEGSETS:
            m = {k: sub[f"{ls}_leg_{k}"].values for k in LEGKEYS}
            allp = sub[f"{ls}_pass"].values
            n_all = int(allp.sum())
            for k in LEGKEYS:
                other = np.ones(len(sub), bool)
                for j in LEGKEYS:
                    if j != k:
                        other &= m[j]
                n_other = int(other.sum())
                n_bind = int((other & ~m[k]).sum())
                out.append(dict(**tag_cols, leg_set=ls, leg=LEGNAME[k], n_rows=len(sub),
                                n_all5=n_all, n_other4=n_other, n_binding=n_bind,
                                R=(n_all / n_other) if n_other else np.nan,
                                leg_pass_rate=float(m[k].mean())))
        return out

    RR = []
    for pname in PANELS:
        for cad in CADORDER:
            s = L[(L.panel == pname) & (L.cadence == cad) & (L.cost_bps == HEAD_COST)]
            RR += redrows(s, dict(panel=pname, cadence=cad, scope="panel_cadence"))
        s = L[(L.panel == pname) & (L.cost_bps == HEAD_COST)]
        RR += redrows(s, dict(panel=pname, cadence="ALL", scope="panel"))
    RR += redrows(L[L.cost_bps == HEAD_COST], dict(panel="ALL", cadence="ALL", scope="pooled"))
    RD = pd.DataFrame(RR)
    dump(RD, "redundancy.csv")

    P("  R(L) per panel, pooled over cadence, 10 bps (NaN = the other four never all hold):")
    pv = RD[RD.scope == "panel"].pivot_table(index=["leg_set", "leg"], columns="panel",
                                             values="R").reindex(columns=PANELS)
    P("   " + pv.to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n   "))
    P()
    P("  n_binding (rows where the other four hold and THIS leg refuses), per panel, 10 bps:")
    pb = RD[RD.scope == "panel"].pivot_table(index=["leg_set", "leg"], columns="panel",
                                             values="n_binding").reindex(columns=PANELS)
    P("   " + pb.to_string(float_format=lambda x: f"{x:.0f}").replace("\n", "\n   "))
    P()
    P("  n_other4 (the denominator), per panel, 10 bps:")
    pn = RD[RD.scope == "panel"].pivot_table(index=["leg_set", "leg"], columns="panel",
                                             values="n_other4").reindex(columns=PANELS)
    P("   " + pn.to_string(float_format=lambda x: f"{x:.0f}").replace("\n", "\n   "))

    P()
    P("  970's own cells -- U56 at M and Q, LS_970, R(L3_OOS):")
    for cad in ["M", "Q"]:
        r = RD[(RD.scope == "panel_cadence") & (RD.panel == "U56") & (RD.cadence == cad)
               & (RD.leg_set == "LS_970") & (RD.leg == "L3_OOS")]
        if len(r):
            r = r.iloc[0]
            P(f"    U56/{cad}: R {r.R if np.isfinite(r.R) else float('nan'):.4f}  "
              f"all5 {int(r.n_all5)} / other4 {int(r.n_other4)}  n_binding {int(r.n_binding)}")

    # ---- agreement between the fully-IS verdict and the record's OOS verdict -------------
    P()
    P("=" * 100)
    P("(C) DOES THE FULLY-IS 4b AGREE WITH THE RECORD'S OOS 4b?")
    P("=" * 100)
    arows = []
    for pname in PANELS + ["ALL"]:
        for cb in RUNGS:
            s = L[(L.cost_bps == cb)] if pname == "ALL" else L[(L.panel == pname)
                                                               & (L.cost_bps == cb)]
            a, b = s.LS_ISALL_pass.values, s.LS_REC_pass.values
            arows.append(dict(panel=pname, cost_bps=cb, n=len(s),
                              agree=float((a == b).mean()),
                              is_pass=int(a.sum()), rec_pass=int(b.sum()),
                              both=int((a & b).sum()),
                              is_only=int((a & ~b).sum()), rec_only=int((~a & b).sum())))
    AG = pd.DataFrame(arows)
    dump(AG, "agreement.csv")
    P("   " + AG[AG.cost_bps == HEAD_COST].to_string(
        index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n   "))

    # ---- binding order --------------------------------------------------------------
    P()
    P("  BINDING ORDER -- how many rows each leg REFUSES outright (1 - pass rate), 10 bps:")
    ordrows = []
    for pname in PANELS:
        s = L[(L.panel == pname) & (L.cost_bps == HEAD_COST)]
        for ls in LEGSETS:
            for k in LEGKEYS:
                ordrows.append(dict(panel=pname, leg_set=ls, leg=LEGNAME[k],
                                    fail_rate=float(1.0 - s[f"{ls}_leg_{k}"].mean())))
    OD = pd.DataFrame(ordrows)
    dump(OD, "binding_order.csv")
    po = OD.pivot_table(index=["panel", "leg"], columns="leg_set",
                        values="fail_rate").reindex(columns=LEGSETS)
    P("   " + po.to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n   "))
    rhos = []
    for pname in PANELS:
        a = [OD[(OD.panel == pname) & (OD.leg_set == "LS_ISALL")
                & (OD.leg == LEGNAME[k])].fail_rate.iloc[0] for k in LEGKEYS]
        b = [OD[(OD.panel == pname) & (OD.leg_set == "LS_REC")
                & (OD.leg == LEGNAME[k])].fail_rate.iloc[0] for k in LEGKEYS]
        rhos.append(spearman(a, b))
        P(f"    {pname:6s} Spearman(IS fail rate, OOS fail rate) over the 5 legs = "
          f"{rhos[-1]:+.4f}")

    # ================================================================== (D) rule 8
    P()
    P("=" * 100)
    P("(D) RULE 8 -- (book, gross) chosen on 2009-2016 ALONE, OOS read ONCE")
    P("=" * 100)
    picks = []
    Lc = L[(L.cost_bps == HEAD_COST) & (L.phase == 0)]
    for pname in PANELS:
        for cad in CADORDER:
            sub = Lc[(Lc.panel == pname) & (Lc.cadence == cad)].reset_index(drop=True)
            nlegs = sum(sub[f"LS_ISALL_leg_{k}"].astype(int) for k in LEGKEYS)
            for ch in CHOOSERS:
                if ch == "C_IS4B":
                    i = _argmax(nlegs.values, sub.IS_Sharpe.values)
                elif ch == "C_ISSHARPE":
                    i = _argmax(sub.IS_Sharpe.values, sub.IS_CAGR.values)
                else:
                    i = _argmax(sub.IS_CAGR.values, sub.IS_Sharpe.values)
                r = sub.iloc[i]
                picks.append(dict(panel=pname, cadence=cad, chooser=ch, book=r.book,
                                  gross=r.gross, IS_legs=int(nlegs.iloc[i]),
                                  IS_pass4b=bool(r.LS_ISALL_pass),
                                  CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD,
                                  H1=r.H1, H2=r.H2,
                                  OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe,
                                  OOS_MaxDD=r.OOS_MaxDD,
                                  OOS_4b=bool(r.LS_REC_pass), OOS_4a=bool(r.pass4a),
                                  fail_legs=r.fail_legs_REC,
                                  spy_OOS_CAGR=r.spy_OOS_CAGR,
                                  spy_OOS_Sharpe=r.spy_OOS_Sharpe,
                                  spy_OOS_MaxDD=r.spy_OOS_MaxDD,
                                  v2_Sharpe=r.v2_Sharpe, v2_MaxDD=r.v2_MaxDD))
    WF = pd.DataFrame(picks)
    dump(WF, "walkforward.csv")
    P(f"  OOS 4b {int(WF.OOS_4b.sum())} of {len(WF)} picks | OOS 4a {int(WF.OOS_4a.sum())}")
    P("   " + WF[["panel", "cadence", "chooser", "book", "gross", "IS_legs", "IS_pass4b",
                  "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "OOS_4b", "OOS_4a", "fail_legs"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n   "))
    P()
    P(f"  ladder-wide at 10 bps: OOS 4b (LS_REC) "
      f"{int(L[L.cost_bps==HEAD_COST].LS_REC_pass.sum()):,} of "
      f"{len(L[L.cost_bps==HEAD_COST]):,} | OOS 4a "
      f"{int(L[L.cost_bps==HEAD_COST].pass4a.sum()):,}")

    # ================================================================== (E) hypotheses
    P()
    P("=" * 100)
    P("(E) PRE-REGISTERED HYPOTHESES")
    P("=" * 100)
    hyp = []

    def H(tag, what, val, bar, ok, note=""):
        hyp.append(dict(H=tag, what=what, value=val, bar=bar, passed=bool(ok), note=note))
        P(f"  {tag:9s} {'PASS' if ok else 'FAIL'} at "
          f"{val if np.isfinite(val) else float('nan'):.4f}  (bar {bar})  {what}")
        if note:
            P(f"            {note}")

    def getR(scope, panel, cad, ls, leg):
        r = RD[(RD.scope == scope) & (RD.panel == panel) & (RD.cadence == cad)
               & (RD.leg_set == ls) & (RD.leg == leg)]
        return r.iloc[0] if len(r) else None

    rm = getR("panel_cadence", "U56", "M", "LS_970", "L3_OOS")
    rq = getR("panel_cadence", "U56", "Q", "LS_970", "L3_OOS")
    ok970 = bool(rm is not None and rq is not None
                 and rm.n_other4 > 0 and rq.n_other4 > 0
                 and abs(rm.R - 1.0) < 1e-12 and abs(rq.R - 1.0) < 1e-12)
    H("H_970", "970's R(L3_OOS) = 1.0000 under LS_970 on U56 at M and Q",
      float(min(rm.R, rq.R)) if (rm is not None and np.isfinite(rm.R)
                                 and np.isfinite(rq.R)) else np.nan,
      1.0, ok970,
      f"U56/M R {rm.R:.4f} (all5 {int(rm.n_all5)}/other4 {int(rm.n_other4)}, "
      f"binding {int(rm.n_binding)}); U56/Q R {rq.R:.4f} "
      f"(all5 {int(rq.n_all5)}/other4 {int(rq.n_other4)}, binding {int(rq.n_binding)})")

    vals, notes = [], []
    for pname in PANELS:
        r = getR("panel", pname, "ALL", "LS_ISALL", "L3_OOS")
        vals.append(r.R if r is not None else np.nan)
        notes.append(f"{pname} R {r.R:.4f} binding {int(r.n_binding)}/{int(r.n_other4)}")
    okis = all((np.isnan(v) or v >= BAR_ISRED) for v in vals) and not all(np.isnan(v)
                                                                         for v in vals)
    H("H_ISRED", "under LS_ISALL the Sharpe leg stays redundant (R >= 0.95) on every panel",
      float(np.nanmin(vals)) if np.isfinite(np.nanmin(vals)) else np.nan,
      BAR_ISRED, okis, "; ".join(notes))

    bindtot = RD[(RD.scope == "panel") & (RD.leg_set == "LS_ISALL")]
    nb = int(bindtot.n_binding.sum())
    worst = bindtot.sort_values("n_binding", ascending=False).iloc[0]
    H("H_BIND", ">= 1 leg binds under LS_ISALL on >= 1 panel", float(nb), 1.0, nb >= 1,
      "binding by leg (summed over panels): " + ", ".join(
          f"{lg} {int(bindtot[bindtot.leg==lg].n_binding.sum())}"
          for lg in [LEGNAME[k] for k in LEGKEYS])
      + f" | worst single cell {worst.leg} on {worst.panel} ({int(worst.n_binding)})")

    ag = AG[(AG.panel == "ALL") & (AG.cost_bps == HEAD_COST)].iloc[0]
    H("H_SAME", "fully-IS 4b agrees with the record's OOS 4b on >= 0.90 of rows",
      float(ag.agree), BAR_SAME, ag.agree >= BAR_SAME,
      f"IS-pass {int(ag.is_pass)} / OOS-pass {int(ag.rec_pass)} / both {int(ag.both)} of "
      f"{int(ag.n):,}; IS-only {int(ag.is_only)}, OOS-only {int(ag.rec_only)}")

    mr = float(np.nanmin(rhos)) if np.any(np.isfinite(rhos)) else np.nan
    H("H_ORDER", "binding order is the same IS and OOS (Spearman >= +0.50 on every panel)",
      mr, BAR_ORDER, np.isfinite(mr) and mr >= BAR_ORDER,
      "per panel: " + ", ".join(f"{p} {r:+.4f}" for p, r in zip(PANELS, rhos)))

    n4b = int(WF.OOS_4b.sum())
    H("H_R8", ">= 1 OOS 4b among the IS-only choosers' picks", float(n4b), 1.0, n4b >= 1,
      f"{n4b} of {len(WF)} picks; by chooser " + ", ".join(
          f"{c} {int(WF[WF.chooser==c].OOS_4b.sum())}" for c in CHOOSERS))
    n4a = int(L.pass4a.sum())
    H("H_4A", ">= 1 OOS 4a anywhere in this run", float(n4a), 1.0, n4a >= 1,
      f"{n4a:,} of {len(L):,} ladder rows; at 10 bps "
      f"{int(L[L.cost_bps==HEAD_COST].pass4a.sum()):,} of "
      f"{len(L[L.cost_bps==HEAD_COST]):,}")
    HY = pd.DataFrame(hyp)
    dump(HY, "hypotheses.csv")
    P(f"  HYPOTHESES: {int(HY.passed.sum())} of {len(HY)} PASS")

    # ---- cost robustness of the headline reading ----------------------------------------
    P()
    P("  COST ROBUSTNESS -- R(L3_OOS) under LS_ISALL, per panel x cost rung:")
    crows = []
    for pname in PANELS:
        for cb in RUNGS:
            s = L[(L.panel == pname) & (L.cost_bps == cb)]
            m = {k: s[f"LS_ISALL_leg_{k}"].values for k in LEGKEYS}
            other = np.ones(len(s), bool)
            for j in LEGKEYS:
                if j != "SHARPE":
                    other &= m[j]
            n_o = int(other.sum())
            crows.append(dict(panel=pname, cost_bps=cb, n_other4=n_o,
                              n_binding=int((other & ~m["SHARPE"]).sum()),
                              R=(int((other & m["SHARPE"]).sum()) / n_o) if n_o else np.nan))
    CR = pd.DataFrame(crows)
    dump(CR, "cost_robustness.csv")
    P("   " + CR.pivot_table(index="cost_bps", columns="panel", values="R")
      .reindex(columns=PANELS).to_string(float_format=lambda x: f"{x:.4f}")
      .replace("\n", "\n   "))

    P()
    P("  SURVIVORSHIP (rule 9): U56/B136/SMALL are current-constituent lists; SMALL drops "
      f"{n_dropped} names with max_1d_move >= 1.0. Every LEVEL is optimistic and every 4b/4a "
      "count is an UPPER bound. R(L) is a ratio of two pass rates over the same rows on the "
      "same tape, so a bias lifting both largely cancels; what does not cancel is that an "
      "optimistic panel pushes MORE rows over every level bar at once, so every R reported "
      "here is an UPPER bound on redundancy and a CONSERVATIVE reading of how often a leg "
      "binds.")
    P(f"  elapsed {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

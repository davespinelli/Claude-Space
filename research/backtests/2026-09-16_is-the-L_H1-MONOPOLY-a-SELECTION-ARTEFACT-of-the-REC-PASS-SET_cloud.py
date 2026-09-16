#!/usr/bin/env python3
"""Idea 1003 (cloud lane, 2026-09-16) -- is the `L_H1` MONOPOLY a SELECTION ARTEFACT of the
REC 4b PASS SET?

THE PRIOR RESULT (idea 971, lane B, committed 2026-09-16)
  Moving 4b's two Sharpe halves inside the in-sample window destroys REC 4b passes, and 143 of
  144 destroyed books bind on `L_H1` ALONE.  The gross-matched rotating coin flip does NOT share
  that leg: it binds on `L_H1` only 0.356 of the time and on `L_H2` 0.707.  971 read the gap as
  SELECTION -- a book that passed REC 4b is, by construction, a book with a strong SECOND half.
  That reading has never been measured directly, and it matters: if 4b as written selects
  late-sample books, then every 4b pass in the record is partly a bet that the last third of the
  tape keeps behaving like the last third of the tape.

WHAT THIS RUN DOES
  Measures the H1/H2 Sharpe ASYMMETRY of the 4b pass set against THE SAME PANEL'S OWN
  POPULATION of books, on idea 970/971's committed 900-row ladder, and against the asymmetry of
  the coin flip's OWN pass set.  Three questions, in order:
    (a) is the pass set late-sample-tilted relative to the population it was drawn from?
    (b) does the SAME tilt appear in the null's pass set -- i.e. is it the BAR, not the books?
    (c) does an IS-only chooser that prefers BALANCED halves do better or worse out of sample
        than one that prefers the highest IS Sharpe?

TUNED DIALS (exactly 2; every level ALWAYS reported, none is ever used to choose anything)
  1. PASS SET   `P_4B`     rows clearing REC 4b at the rung being read;
                `P_4A`     rows clearing 4a (beat-the-book) -- a second, differently-defined bar;
                `P_NULL4B` the coin flip's OWN pass set: `RANDROT` draws that clear REC 4b;
                `P_ALL`    the CONTROL -- the whole ladder population, nothing selected.
  2. ASYMMETRY  `A_DIFF`   S(H2) - S(H1);
                `A_MARGIN` (S(H2) - SPY(H2)) - (S(H1) - SPY(H1)), i.e. net of the bar itself;
                `A_RATIO`  S(H2) / S(H1), read only where S(H1) > 0.10 (reported n);
                `A_RANK`   pctile of S(H2) minus pctile of S(H1), both inside the row's OWN
                           (panel, cost) population -- unit-free and outlier-proof.

REPORTED, NEVER FITTED
  PANEL {U56, B136, SMALL663}, BOOK {TOP5, TOP10, TOP20, EWELIG, BAND03}, GROSS {0.50, 0.65,
  0.75, 1.00}, CADENCE {W, M, Q}, COST {0, 5, 10, 25, 50} bps with 10 BINDING (PROTOCOL rule 2).
  Idea 970/971's committed ladder, fixed before any number here was read.  The null sub-grid is
  3 panels x 5 books x {0.75, 1.00} gross x 3 cadences x 200 draws.

PRE-REGISTERED HYPOTHESES (bars fixed before any number was read)
  H_LATE   4b selects late-sample books.  PASS iff the median `A_DIFF` of `P_4B` exceeds the
           median of `P_ALL` on >= 2 of 3 panels at 10 bps AND the pooled gap is > 0.
  H_MONO   971's leg reading reproduces here.  PASS iff, over REC 4b FAIL rows at 10 bps,
           `L_H1` fails strictly more often than `L_H2`.
  H_SPY    the mechanism is the BAR's own halves, not the books.  PASS iff SPY's H1 Sharpe
           exceeds its H2 Sharpe on >= 2 of 3 panels (a harder first half mechanically leaves a
           pass set with strong second halves).
  H_NULL   the tilt is a property of the BAR and not of the rules.  PASS iff `P_NULL4B`'s median
           `A_DIFF` gap over its own null population is > 0 and within 0.10 of the books' gap.
  H_STAT   the answer does not depend on the statistic.  PASS iff all four asymmetry statistics
           put the `P_4B` - `P_ALL` pooled gap on the SAME side of zero.
  H_RULE8  preferring BALANCED in-sample halves is not free.  PASS iff `C_ISSYM`'s OOS 4b count
           is >= `C_ISSHARPE`'s over the 9 (panel, cadence) slots.

RULE 8 (walk-forward, mandatory -- PROTOCOL rule 8)
  (book, gross) is chosen inside each (panel, cadence) on 2009-2016 ALONE by three IS-only
  choosers -- `C_IS4B` (IS 4b passers first, then IS Sharpe), `C_ISSHARPE` (IS Sharpe), and
  `C_ISSYM` (the smallest |IS_H2 - IS_H1|, this idea's statistic used as a selector).  2017-2026
  is then read ONCE.  OOS CAGR / Sharpe / MaxDD are reported against the RULES v2 live baseline
  and against SPY, and BOTH KEEP paths are scored on every pick.  G6 proves the choosers are
  IS-only by permuting the OOS return rows.

GATES
  G0  rebalance masks == `engine.rebalance_mask` on W/M/Q.  Bar 0 rows.
  G1  closed-form runner == `engine.backtest` on returns AND turnover @10 bps.  Bar 1e-12.
  G2  BAND03 @0.75 weights == `baseline.rules_v2_weights(px, 0.03, 0.75)`.  Bar 0.0 exact.
  G3  CROSS-RUN: this run's 900-row ladder vs idea 971's committed `.grid.csv` (CAGR, Sharpe,
      MaxDD, OOS_Sharpe, REC_H1, REC_H2).  Bar 1e-09, reported per panel, never tuned away.
  G3b CROSS-RUN of the VERDICT column vs 971's `p4b_REC_REC5`.  Bar 0 disagreements.
  G4  GROSS MATCH: every null draw's target gross and holding count equal the book's on every
      decision row (bar 0.0), and realised annual turnover > 0.5x the book's.
  G5  determinism: a redrawn null is bit-for-bit identical.
  G6  every rule-8 chooser is IS-ONLY: picks invariant to permuted OOS return rows.
  G7  SUBSET ALGEBRA: every pass set is a subset of its own population (0 stray rows), and the
      four asymmetry statistics agree in SIGN with `A_DIFF` on >= 0.95 of rows where `A_RATIO`
      is defined -- so a sign difference in the ANSWER cannot be a definition artefact.

SURVIVORSHIP (PROTOCOL rule 9)
  U56 / B136 / SMALL663 are CURRENT-constituent lists (SMALL663 additionally drops the 52
  tickers with `max_1d_move` >= 1.0 per `data/small_meta.csv`).  Survivorship bias is itself
  LATE-SAMPLE tilted -- a current constituent is one that survived TO today -- so the measured
  H2-minus-H1 asymmetry is an UPPER bound in LEVEL on every panel.  The measured object is a
  DIFFERENCE between a pass set and its own panel's population on the same tape, which removes
  the panel-wide component; what it cannot remove is any interaction between survivorship and
  the 4b bar itself, and that is stated as a limit, not corrected for.

COSTS 10 bps per unit turnover binding; weights decided at close t, applied at close t+1.
"""
from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys
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

WARMUP, LAG = 260, 1
VOLCAP, BAND0 = 0.60, 0.03
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COSTS = [0.0, 5.0, 10.0, 25.0, 50.0]
PROTO_COST = 10.0
GROSS_GRID = [0.50, 0.65, 0.75, 1.00]
BOOKS = ["TOP5", "TOP10", "TOP20", "EWELIG", "BAND03"]
CADENCES = ["W", "M", "Q"]
PANELS = ["U56", "B136", "SMALL663"]

LEGS = ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")

DRAWS = 200
SEED0 = 1003
NULL_GROSS = [0.75, 1.00]    # the null sub-grid (the record's CORE / EXT rungs)
STAT_NAMES = ["A_DIFF", "A_MARGIN", "A_RATIO", "A_RANK"]
PASSSETS = ["P_4B", "P_4A", "P_NULL4B", "P_ALL"]
NULL_BAR = 0.10              # H_NULL

PRIOR_GRID = OUT / "2026-09-16_is-the-2009-2012-HALF-the-leg-that-kills-every-DISJOINT-4b-pass_B.grid.csv"
G3_BAR = 1e-9

SMOKE = bool(int(os.environ.get("IDEA1003_SMOKE", "0")))
if SMOKE:
    DRAWS = 6

LOG: list[str] = []
G4_ROWS: list[dict] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def seed_of(*parts) -> int:
    return int(hashlib.md5("|".join(str(x) for x in parts).encode()).hexdigest()[:16], 16) % (2 ** 32)


def head_sha():
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                              capture_output=True, text=True).stdout.strip() or "unknown"
    except Exception:
        return "unknown"


# =================================================================================================
# runner (gated at G1) -- closed-form equivalent of engine.backtest's day loop
# =================================================================================================
class Ctx:
    def __init__(self, rets, applied):
        T, N = rets.shape
        self.rets, self.T = rets, T
        C = np.cumprod(1.0 + rets, axis=0)
        self.Cp = np.vstack([np.ones((1, N)), C[:-1]])
        self.reb = np.flatnonzero(applied)
        seg = np.searchsorted(self.reb, np.arange(T), side="right") - 1
        self.s0 = self.reb[seg]
        self.s0p = self.reb[np.maximum(seg - 1, 0)]
        self.R = self.Cp / self.Cp[self.s0]
        self.Rp = self.Cp[self.reb] / self.Cp[self.s0p[self.reb]]

    def run(self, wt, cost):
        """wt = TARGET WEIGHTS already lagged and already carrying gross."""
        A = wt[self.s0]
        AR = A * self.R
        V = 1.0 + (AR.sum(axis=1) - A.sum(axis=1))
        port = (AR * self.rets).sum(axis=1) / V
        Ap = wt[self.s0p[self.reb]]
        ARp = Ap * self.Rp
        Vp = 1.0 + (ARp.sum(axis=1) - Ap.sum(axis=1))
        heldp = ARp / Vp[:, None]
        heldp[0] = 0.0
        turn = np.zeros(self.T)
        turn[self.reb] = np.abs(wt[self.reb] - heldp).sum(axis=1)
        return port - turn * cost / 1e4, turn


def lag_weights(W):
    wt = np.roll(W, LAG, axis=0).copy()
    wt[:LAG] = 0.0
    return wt


def applied_from_decision(dec):
    a = np.roll(dec, LAG)
    a[:LAG] = False
    a[0] = True
    return a


def fmet(r):
    r = np.asarray(r, float)
    if len(r) < 60:
        return np.nan, np.nan, np.nan
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


# =================================================================================================
class Panel:
    def __init__(self, name, px):
        self.name, self.px, self.idx = name, px, px.index
        self.rets = np.nan_to_num(px.pct_change().values, nan=0.0, posinf=0.0, neginf=0.0)
        self.T = len(self.idx)
        self.warm = np.arange(self.T) >= WARMUP
        wpos = np.flatnonzero(self.warm)
        self.oos = np.asarray(self.idx >= pd.Timestamp(OOS_START)) & self.warm
        self.is_ = self.warm & np.asarray(self.idx <= pd.Timestamp(IS_END))
        h = len(wpos) // 2
        self.h1 = np.zeros(self.T, bool); self.h1[wpos[:h]] = True
        self.h2 = np.zeros(self.T, bool); self.h2[wpos[h:]] = True
        ipos = np.flatnonzero(self.is_)
        hi = len(ipos) // 2
        self.is_h1 = np.zeros(self.T, bool); self.is_h1[ipos[:hi]] = True
        self.is_h2 = np.zeros(self.T, bool); self.is_h2[ipos[hi:]] = True

        spy = np.nan_to_num(px["SPY"].pct_change().values, nan=0.0)
        self.spy = spy
        self.spy_full = fmet(spy[self.warm])
        self.spy_oos = fmet(spy[self.oos])
        self.spy_is = fmet(spy[self.is_])
        self.spy_h1 = fmet(spy[self.h1])[1]
        self.spy_h2 = fmet(spy[self.h2])[1]
        self.spy_ish1 = fmet(spy[self.is_h1])[1]
        self.spy_ish2 = fmet(spy[self.is_h2])[1]

        self.priced = px.notna().values
        above = px > px.rolling(200).mean()
        vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        self.elig = (above & (vol20 < VOLCAP) & px.notna()).values
        self.dec = {c: rebalance_mask(self.idx, c).values.copy() for c in CADENCES}
        self.app = {c: applied_from_decision(self.dec[c]) for c in CADENCES}
        self.ctx = {c: Ctx(self.rets, self.app[c]) for c in CADENCES}
        self.books = {}
        for g in GROSS_GRID:
            self.books[g] = build_books(px, g)[0]
        bw = lag_weights(rules_v2_weights(px, BAND0, 0.75).values)
        self.base_r = {c_: self.ctx["W"].run(bw, c_)[0] for c_ in COSTS}
        self.years = self.warm.sum() / 252.0


def build_books(px, g):
    sc, above, vol20 = score(px, vol_scale=False)
    elig = above & (vol20 < VOLCAP) & px.notna()
    rank = sc.where(elig).rank(axis=1, ascending=False)
    bk = {}
    for k in (5, 10, 20):
        bk[f"TOP{k}"] = ((rank <= k).astype(float) * (g / k)).values
    n_el = elig.sum(axis=1).replace(0, np.nan)
    bk["EWELIG"] = (elig.astype(float).div(n_el, axis=0).fillna(0.0) * g).values
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    bk["BAND03"] = ew.where(band_state(px, BAND0) & px.notna(), 0.0).values
    return bk, elig.values


def stats_of(pn, r):
    c, s, dd = fmet(r[pn.warm])
    oc, os_, odd = fmet(r[pn.oos])
    ic, is_, idd = fmet(r[pn.is_])
    return dict(CAGR=c, Sharpe=s, MaxDD=dd, OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=odd,
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd,
                H1=fmet(r[pn.h1])[1], H2=fmet(r[pn.h2])[1],
                IS_H1=fmet(r[pn.is_h1])[1], IS_H2=fmet(r[pn.is_h2])[1])


def legs_4b(pn, st):
    return dict(L_H1=bool(st["H1"] > pn.spy_h1),
                L_H2=bool(st["H2"] > pn.spy_h2),
                L_OOS=bool(st["OOS_Sharpe"] > pn.spy_oos[1]),
                L_DD=bool(abs(st["MaxDD"]) <= DD_CAP * abs(pn.spy_full[2])),
                L_CAGR=bool(st["CAGR"] >= CAGR_FLOOR * pn.spy_full[0]))


def legs_4b_is(pn, st):
    """The same five legs read on 2009-2016 ALONE -- the only version a rule-8 chooser may see."""
    return dict(L_H1=bool(st["IS_H1"] > pn.spy_ish1),
                L_H2=bool(st["IS_H2"] > pn.spy_ish2),
                L_OOS=True,
                L_DD=bool(abs(st["IS_MaxDD"]) <= DD_CAP * abs(pn.spy_is[2])),
                L_CAGR=bool(st["IS_CAGR"] >= CAGR_FLOOR * pn.spy_is[0]))


def pass_4a(pn, r, bst):
    return bool(fmet(r[pn.h1])[1] > fmet(bst[pn.h1])[1] and fmet(r[pn.h2])[1] > fmet(bst[pn.h2])[1]
                and fmet(r[pn.warm])[2] >= fmet(bst[pn.warm])[2])


def draw_null(buf, pn, W, dec, rng):
    """Gross-matched ROTATING coin flip (`RANDROT`, ideas 680/926/931/942/970/971).

    ONE documented extension over 971's copy, forced by this run pricing WIDE books and not
    only TOP20: when the book holds MORE names than the eligibility pool has (EWELIG and
    BAND03 routinely do), the pool is widened with the remaining PRICED names so the draw's
    holding count still equals the book's exactly (gated at G4, `dk` = 0).  On every TOP-k
    book, where k <= |elig| always, the draw is 971's construction untouched."""
    buf[:] = 0.0
    held = W > 0
    kcount = held.sum(axis=1)
    gross = W.sum(axis=1)
    for i in np.flatnonzero(dec):
        k = int(kcount[i])
        if k == 0:
            continue
        pool = np.flatnonzero(pn.elig[i])
        if len(pool) < k:                                    # widen with the priced remainder
            extra = np.setdiff1d(np.flatnonzero(pn.priced[i]), pool, assume_unique=False)
            pool = np.concatenate([pool, extra]) if len(extra) else pool
        if len(pool) == 0:
            continue
        k = min(k, len(pool))
        pick = rng.choice(pool, size=k, replace=False)
        buf[i, pick] = gross[i] / k
    return buf


def pct_in(book_val, draw_vals, stat):
    """The book's percentile INSIDE its own null: the share of draws it beats, x100.
    Higher is better for Sharpe / CAGR / OOS_Sharpe; for MaxDD 'beats' = shallower."""
    d = np.asarray(draw_vals, float)
    d = d[np.isfinite(d)]
    if len(d) == 0 or not np.isfinite(book_val):
        return np.nan
    if stat == "MaxDD":
        return 100.0 * float(np.mean(abs(book_val) < np.abs(d)))
    return 100.0 * float(np.mean(book_val > d))




# =================================================================================================
# asymmetry statistics
# =================================================================================================
def add_asym(df, spy_h1, spy_h2):
    """The four asymmetry statistics.  `A_RANK` is computed inside each (panel, cost) population,
    which is why it is added on the FULL frame and never on a selected subset."""
    d = df.copy()
    d["A_DIFF"] = d.H2 - d.H1
    d["A_MARGIN"] = (d.H2 - d.panel.map(spy_h2)) - (d.H1 - d.panel.map(spy_h1))
    d["A_RATIO"] = np.where(d.H1 > 0.10, d.H2 / d.H1.where(d.H1 > 0.10), np.nan)
    d["A_RANK"] = np.nan
    for (pk, cst), idx in d.groupby(["panel", "cost"]).groups.items():
        s = d.loc[idx]
        d.loc[idx, "A_RANK"] = (s.H2.rank(pct=True) - s.H1.rank(pct=True)) * 100.0
    return d


def summarise(pop, sel, tag, panel, cost, n_pop):
    out = []
    for st in STAT_NAMES:
        v, p = sel[st].dropna(), pop[st].dropna()
        out.append(dict(passset=tag, panel=panel, cost=cost, statistic=st,
                        n=len(v), n_pop=n_pop,
                        median=float(v.median()) if len(v) else np.nan,
                        mean=float(v.mean()) if len(v) else np.nan,
                        pop_median=float(p.median()) if len(p) else np.nan,
                        gap=float(v.median() - p.median()) if len(v) and len(p) else np.nan,
                        share_pos=float((v > 0).mean()) if len(v) else np.nan,
                        share_above_pop=float((v > p.median()).mean()) if len(v) and len(p) else np.nan))
    return out


# =================================================================================================
def main():
    P("=" * 100)
    P("IDEA 1003 (cloud) -- is the `L_H1` MONOPOLY a SELECTION ARTEFACT of the REC 4b PASS SET?")
    P(f"tree {head_sha()}   draws {DRAWS}   costs {COSTS} (10 bps binding)   smoke={SMOKE}")
    P("=" * 100)

    px = {"U56": load_universe(), "B136": load_universe(broad=True)}
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    px["SMALL663"] = sm[[c for c in sm.columns if c == "SPY" or c not in bad]]
    P(f"\nPANELS  (SMALL663 screen: {len(sm.columns) - px['SMALL663'].shape[1]} tickers with "
      f"max_1d_move >= 1.0 dropped)")
    pnl = {k: Panel(k, px[k]) for k in PANELS}
    SPY_H1 = {k: pnl[k].spy_h1 for k in PANELS}
    SPY_H2 = {k: pnl[k].spy_h2 for k in PANELS}
    for k in PANELS:
        p = pnl[k]
        P(f"  {k:9s} {p.px.shape[1]-1:4d} names + SPY   {p.idx[0].date()} -> {p.idx[-1].date()}"
          f"   SPY H1 {p.spy_h1:.4f}  H2 {p.spy_h2:.4f}  (H1-H2 {p.spy_h1 - p.spy_h2:+.4f})"
          f"   H2 starts {p.idx[np.flatnonzero(p.h2)[0]].date()}")

    # ---------------------------------------------------------------- ladder
    P("\n" + "-" * 100)
    P("THE LADDER  (3 panels x 5 books x 4 gross x 3 cadences x 5 cost rungs = 900 rows)")
    P("-" * 100)
    lad = []
    for pk in PANELS:
        pn = pnl[pk]
        for bk in BOOKS:
            for g in GROSS_GRID:
                W = lag_weights(pn.books[g][bk])
                for cad in CADENCES:
                    r_, t_ = pn.ctx[cad].run(W, 0.0)
                    for cst in COSTS:
                        r = r_ - t_ * cst / 1e4
                        st = stats_of(pn, r)
                        lg = legs_4b(pn, st)
                        lgi = legs_4b_is(pn, st)
                        row = dict(panel=pk, book=bk, gross=g, cadence=cad, cost=cst,
                                   turnover=t_[pn.warm].sum() / pn.years, **st, **lg)
                        row["pass4b"] = all(lg.values())
                        row["pass4a"] = pass_4a(pn, r, pn.base_r[cst])
                        row["IS_pass4b"] = all(lgi.values())
                        lad.append(row)
    LAD = add_asym(pd.DataFrame(lad), SPY_H1, SPY_H2)
    l10 = LAD[LAD.cost == PROTO_COST]
    P(f"  {len(LAD):,} rows.  at 10 bps: 4b PASS {int(l10.pass4b.sum())} of {len(l10)},"
      f"  4a PASS {int(l10.pass4a.sum())}")
    dump(LAD, "ladder.csv")

    # ---------------------------------------------------------------- 971's leg reading
    P("\n" + "-" * 100)
    P("THE LEG CENSUS  (which 4b leg fails, over the ladder's REC 4b FAIL rows)")
    P("-" * 100)
    legrows = []
    for cst in COSTS:
        s = LAD[(LAD.cost == cst) & (~LAD.pass4b)]
        row = dict(cost=cst, n_fail=len(s))
        for lg in LEGS:
            row[f"fail_{lg}"] = float((~s[lg]).mean()) if len(s) else np.nan
        row["sole_L_H1"] = float(((~s.L_H1) & s.L_H2 & s.L_OOS & s.L_DD & s.L_CAGR).mean()) if len(s) else np.nan
        row["sole_L_H2"] = float((s.L_H1 & (~s.L_H2) & s.L_OOS & s.L_DD & s.L_CAGR).mean()) if len(s) else np.nan
        legrows.append(row)
    LEGC = pd.DataFrame(legrows)
    dump(LEGC, "legcensus.csv")
    P("  " + LEGC.to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n  "))

    # ---------------------------------------------------------------- nulls
    P("\n" + "-" * 100)
    P(f"THE NULL  (`RANDROT` gross-matched rotating coin flip; 3 x 5 x {len(NULL_GROSS)} x 3 cells"
      f" x {DRAWS} draws)")
    P("-" * 100)
    need = [(pk, bk, g, cad) for pk in PANELS for bk in BOOKS for g in NULL_GROSS for cad in CADENCES]
    ndrows = []
    for n_i, (pk, bk, g, cad) in enumerate(need):
        pn = pnl[pk]
        dec = pn.dec[cad]
        buf = np.zeros_like(pn.books[g][bk])
        for d in range(DRAWS):
            rng = np.random.default_rng(seed_of(SEED0, pk, bk, g, cad, d))
            Wn = draw_null(buf, pn, pn.books[g][bk], dec, rng).copy()
            if d == 0:
                dm = np.flatnonzero(dec)
                G4_ROWS.append(dict(cell=f"{pk}/{bk}/{g:.2f}/{cad}",
                                    dgross=float(np.abs(Wn[dm].sum(1) - pn.books[g][bk][dm].sum(1)).max()),
                                    dk=int(np.abs((Wn[dm] > 0).sum(1) - (pn.books[g][bk][dm] > 0).sum(1)).max())))
            r_, t_ = pn.ctx[cad].run(lag_weights(Wn), 0.0)
            r = r_ - t_ * PROTO_COST / 1e4
            st = stats_of(pn, r)
            lg = legs_4b(pn, st)
            ndrows.append(dict(panel=pk, book=bk, gross=g, cadence=cad, cost=PROTO_COST, draw=d,
                               turnover=t_[pn.warm].sum() / pn.years, **st, **lg,
                               pass4b=all(lg.values())))
        if (n_i + 1) % 15 == 0 or n_i == len(need) - 1:
            P(f"  {n_i + 1:3d}/{len(need)} cells built")
    ND = add_asym(pd.DataFrame(ndrows), SPY_H1, SPY_H2)
    dump(ND[["panel", "book", "gross", "cadence", "draw", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
             "OOS_Sharpe", "turnover", "pass4b", "A_DIFF", "A_MARGIN", "A_RATIO", "A_RANK"]],
         "null_draws.csv")
    P(f"  {len(ND):,} draws.  null 4b base rate {ND.pass4b.mean():.4f} "
      f"({int(ND.pass4b.sum())} of {len(ND)})")
    for lg in LEGS:
        P(f"    null fail rate {lg:7s} {(~ND[lg]).mean():.4f}")

    # ---------------------------------------------------------------- the answer
    P("\n" + "=" * 100)
    P("THE ANSWER -- H1/H2 asymmetry of each PASS SET against its own population")
    P("=" * 100)
    rows = []
    for cst in COSTS:
        book_pop = LAD[LAD.cost == cst]
        null_pop = ND if cst == PROTO_COST else None
        for panel in ["POOLED"] + PANELS:
            bp = book_pop if panel == "POOLED" else book_pop[book_pop.panel == panel]
            rows += summarise(bp, bp, "P_ALL", panel, cst, len(bp))
            rows += summarise(bp, bp[bp.pass4b], "P_4B", panel, cst, len(bp))
            rows += summarise(bp, bp[bp.pass4a], "P_4A", panel, cst, len(bp))
            if null_pop is not None:
                np_ = null_pop if panel == "POOLED" else null_pop[null_pop.panel == panel]
                rows += summarise(np_, np_, "P_NULLALL", panel, cst, len(np_))
                rows += summarise(np_, np_[np_.pass4b], "P_NULL4B", panel, cst, len(np_))
    ANS = pd.DataFrame(rows)
    dump(ANS, "answer.csv")

    def cell(tag, panel, st, col="gap", cst=PROTO_COST):
        s = ANS[(ANS.passset == tag) & (ANS.panel == panel) & (ANS.statistic == st) & (ANS.cost == cst)]
        return float(s[col].iloc[0]) if len(s) else np.nan

    P("\n  A_DIFF = Sharpe(H2) - Sharpe(H1), 10 bps.  'gap' = pass-set median - population median")
    hdr = f"  {'panel':10s} {'n(4b)':>6s} {'P_ALL med':>10s} {'P_4B med':>9s} {'gap':>8s} " \
          f"{'P_4A med':>9s} {'gap':>8s} {'NULL med':>9s} {'N4B med':>8s} {'gap':>8s}"
    P(hdr); P("  " + "-" * (len(hdr) - 2))
    for panel in ["POOLED"] + PANELS:
        g = lambda t, c: cell(t, panel, "A_DIFF", c)
        n4b = int(ANS[(ANS.passset == "P_4B") & (ANS.panel == panel) & (ANS.statistic == "A_DIFF")
                      & (ANS.cost == PROTO_COST)].n.iloc[0])
        P(f"  {panel:10s} {n4b:6d} {g('P_ALL','median'):10.4f} {g('P_4B','median'):9.4f} "
          f"{g('P_4B','gap'):+8.4f} {g('P_4A','median'):9.4f} {g('P_4A','gap'):+8.4f} "
          f"{g('P_NULLALL','median'):9.4f} {g('P_NULL4B','median'):8.4f} {g('P_NULL4B','gap'):+8.4f}")

    P("\n  POOLED gap (pass set median - population median) by STATISTIC, 10 bps:")
    P(f"  {'statistic':10s} {'P_4B':>10s} {'P_4A':>10s} {'P_NULL4B':>10s}")
    for st in STAT_NAMES:
        P(f"  {st:10s} {cell('P_4B','POOLED',st):+10.4f} {cell('P_4A','POOLED',st):+10.4f} "
          f"{cell('P_NULL4B','POOLED',st):+10.4f}")

    P("\n  COST LADDER (POOLED A_DIFF gap of P_4B, and its n):")
    for cst in COSTS:
        s = ANS[(ANS.passset == "P_4B") & (ANS.panel == "POOLED") & (ANS.statistic == "A_DIFF")
                & (ANS.cost == cst)]
        P(f"    {cst:5.1f} bps   n {int(s.n.iloc[0]):3d}   gap {float(s.gap.iloc[0]):+.4f}"
          f"   median {float(s['median'].iloc[0]):+.4f}")

    # ---------------------------------------------------------------- rule 8
    P("\n" + "=" * 100)
    P("RULE 8 -- WALK-FORWARD  (choose on 2009-2016 alone; 2017-2026 read ONCE)")
    P("=" * 100)
    wf = walkforward(pnl, LAD)
    dump(wf, "walkforward.csv")
    P("\n  " + wf[["panel", "cadence", "chooser", "book", "gross", "IS_asym", "OOS_CAGR",
                   "OOS_Sharpe", "OOS_MaxDD", "OOS_pass4b", "OOS_pass4a"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n  "))
    for ch in ["C_IS4B", "C_ISSHARPE", "C_ISSYM"]:
        w = wf[wf.chooser == ch]
        P(f"\n  {ch:11s} OOS 4b {int(w.OOS_pass4b.sum())} of {len(w)}   OOS 4a {int(w.OOS_pass4a.sum())} of {len(w)}"
          f"   median OOS CAGR {w.OOS_CAGR.median():.2%}  Sharpe {w.OOS_Sharpe.median():.4f}"
          f"  MaxDD {w.OOS_MaxDD.median():.2%}")
    P("\n  BENCHMARKS on the same OOS window:")
    for pk in PANELS:
        p = pnl[pk]
        bs = fmet(p.base_r[PROTO_COST][p.oos])
        P(f"    {pk:9s} SPY {p.spy_oos[0]:7.2%} / {p.spy_oos[1]:.4f} / {p.spy_oos[2]:7.2%}"
          f"    RULES v2 (live) {bs[0]:7.2%} / {bs[1]:.4f} / {bs[2]:7.2%}")

    # ---------------------------------------------------------------- hypotheses
    P("\n" + "=" * 100)
    P("PRE-REGISTERED HYPOTHESES")
    P("=" * 100)
    hy = []

    def H(n, ok, detail):
        hy.append(dict(hypothesis=n, verdict="PASS" if ok else "FAIL", detail=detail))
        P(f"  {n:9s} {'PASS' if ok else 'FAIL'}   {detail}")

    per_panel = {pk: cell("P_4B", pk, "A_DIFF") for pk in PANELS}
    npos = sum(1 for v in per_panel.values() if np.isfinite(v) and v > 0)
    pooled = cell("P_4B", "POOLED", "A_DIFF")
    H("H_LATE", npos >= 2 and pooled > 0,
      f"pooled A_DIFF gap {pooled:+.4f}; positive on {npos} of 3 panels (" +
      ", ".join(f"{k} {v:+.4f}" for k, v in per_panel.items()) + ")")
    lf = LEGC[LEGC.cost == PROTO_COST].iloc[0]
    H("H_MONO", float(lf.fail_L_H1) > float(lf.fail_L_H2),
      f"REC 4b FAIL rows at 10 bps (n={int(lf.n_fail)}): L_H1 {lf.fail_L_H1:.4f} vs "
      f"L_H2 {lf.fail_L_H2:.4f}; sole-binder L_H1 {lf.sole_L_H1:.4f} vs L_H2 {lf.sole_L_H2:.4f}")
    nspy = sum(1 for pk in PANELS if pnl[pk].spy_h1 > pnl[pk].spy_h2)
    H("H_SPY", nspy >= 2,
      "SPY H1 > H2 on " + f"{nspy} of 3 panels (" +
      ", ".join(f"{pk} {pnl[pk].spy_h1:.4f}/{pnl[pk].spy_h2:.4f}" for pk in PANELS) + ")")
    gnull = cell("P_NULL4B", "POOLED", "A_DIFF")
    H("H_NULL", np.isfinite(gnull) and gnull > 0 and abs(gnull - pooled) <= NULL_BAR,
      f"null pass-set gap {gnull:+.4f} vs books' {pooled:+.4f} (|d| {abs(gnull - pooled):.4f}, bar {NULL_BAR})")
    signs = {np.sign(cell("P_4B", "POOLED", st)) for st in STAT_NAMES}
    H("H_STAT", len(signs) == 1,
      "pooled P_4B gap by statistic: " + ", ".join(f"{st} {cell('P_4B','POOLED',st):+.4f}" for st in STAT_NAMES))
    n_sym = int(wf[wf.chooser == "C_ISSYM"].OOS_pass4b.sum())
    n_shp = int(wf[wf.chooser == "C_ISSHARPE"].OOS_pass4b.sum())
    H("H_RULE8", n_sym >= n_shp, f"C_ISSYM OOS 4b {n_sym} vs C_ISSHARPE {n_shp} of 9 slots each")
    dump(pd.DataFrame(hy), "hypotheses.csv")

    # ---------------------------------------------------------------- gates
    P("\n" + "=" * 100)
    P("GATES")
    P("=" * 100)
    gates = run_gates(pnl, LAD, ND, need)
    dump(gates, "gates.csv")
    P(f"\n  {int((gates.verdict == 'PASS').sum())} of {len(gates)} gates PASS")

    (OUT / f"{STEM}.log.txt").write_text("\n".join(LOG) + "\n")
    print(f"\nwrote {STEM}.log.txt")


# =================================================================================================
def walkforward(pnl, LAD):
    l10 = LAD[LAD.cost == PROTO_COST]
    rows = []
    for pk in PANELS:
        pn = pnl[pk]
        for cad in CADENCES:
            sub = l10[(l10.panel == pk) & (l10.cadence == cad)].copy()
            sub["IS_asym"] = sub.IS_H2 - sub.IS_H1
            picks = {
                "C_IS4B": sub.sort_values(["IS_pass4b", "IS_Sharpe"], ascending=[False, False]).iloc[0],
                "C_ISSHARPE": sub.sort_values("IS_Sharpe", ascending=False).iloc[0],
                "C_ISSYM": sub.assign(_a=sub.IS_asym.abs()).sort_values(["_a", "IS_Sharpe"],
                                                                        ascending=[True, False]).iloc[0],
            }
            for ch, p in picks.items():
                W = lag_weights(pn.books[p.gross][p.book])
                r_, t_ = pn.ctx[cad].run(W, 0.0)
                r = r_ - t_ * PROTO_COST / 1e4
                oc, os_, odd = fmet(r[pn.oos])
                bo = fmet(pn.base_r[PROTO_COST][pn.oos])
                legs = dict(L_H1=bool(fmet(r[pn.h1])[1] > pn.spy_h1),
                            L_H2=bool(fmet(r[pn.h2])[1] > pn.spy_h2),
                            L_OOS=bool(os_ > pn.spy_oos[1]),
                            L_DD=bool(abs(odd) <= DD_CAP * abs(pn.spy_oos[2])),
                            L_CAGR=bool(oc >= CAGR_FLOOR * pn.spy_oos[0]))
                rows.append(dict(panel=pk, cadence=cad, chooser=ch, book=p.book, gross=p.gross,
                                 IS_Sharpe=p.IS_Sharpe, IS_asym=p.IS_asym, IS_pass4b=bool(p.IS_pass4b),
                                 OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=odd,
                                 SPY_OOS_CAGR=pn.spy_oos[0], SPY_OOS_Sharpe=pn.spy_oos[1],
                                 SPY_OOS_MaxDD=pn.spy_oos[2],
                                 BASE_OOS_CAGR=bo[0], BASE_OOS_Sharpe=bo[1], BASE_OOS_MaxDD=bo[2],
                                 **legs, OOS_pass4b=all(legs.values()),
                                 OOS_pass4a=bool(os_ > bo[1] and odd >= bo[2])))
    return pd.DataFrame(rows)


def run_gates(pnl, LAD, ND, need):
    g = []

    def G(n, ok, detail):
        g.append(dict(gate=n, verdict="PASS" if ok else "FAIL", detail=detail))
        P(f"  {n:5s} {'PASS' if ok else 'FAIL'}  {detail}")

    pn = pnl["U56"]
    bad = sum(int((pn.dec[c] != rebalance_mask(pn.idx, c).values).sum()) for c in CADENCES)
    G("G0", bad == 0, f"rebalance masks == engine.rebalance_mask on W/M/Q ({bad} rows differ)")

    worst_r = worst_t = 0.0
    for cad in ("W", "M"):
        for bk in ("TOP20", "BAND03"):
            Wdf = pd.DataFrame(pn.books[0.75][bk], index=pn.idx, columns=pn.px.columns)
            eng = backtest(pn.px, Wdf, cost_bps=PROTO_COST, freq=cad)
            r, t = pn.ctx[cad].run(lag_weights(pn.books[0.75][bk]), PROTO_COST)
            m = pn.warm
            worst_r = max(worst_r, float(np.abs(np.asarray(eng["returns"])[m] - r[m]).max()))
            worst_t = max(worst_t, float(np.abs(np.asarray(eng["turnover"])[m] - t[m]).max()))
    G("G1", worst_r < 1e-12 and worst_t < 1e-12,
      f"fast Ctx == engine.backtest post-warm-up: dret {worst_r:.3e}  dturn {worst_t:.3e}")

    d2 = float(np.abs(pn.books[0.75]["BAND03"] - rules_v2_weights(pn.px, BAND0, 0.75).values).max())
    G("G2", d2 == 0.0, f"BAND03@0.75 == baseline.rules_v2_weights: max|d| {d2:.3e}")

    if PRIOR_GRID.exists():
        pg = pd.read_csv(PRIOR_GRID)
        cols = ["CAGR", "Sharpe", "MaxDD", "OOS_Sharpe"]
        m = LAD.merge(pg[["panel", "book", "gross", "cadence", "cost"] + cols +
                         ["REC_H1", "REC_H2", "p4b_REC_REC5"]],
                      on=["panel", "book", "gross", "cadence", "cost"], suffixes=("", "_p"))
        per = {pk: max([float(np.abs(m[m.panel == pk][c] - m[m.panel == pk][f"{c}_p"]).max()) for c in cols] +
                       [float(np.abs(m[m.panel == pk].H1 - m[m.panel == pk].REC_H1).max()),
                        float(np.abs(m[m.panel == pk].H2 - m[m.panel == pk].REC_H2).max())])
               for pk in PANELS}
        worst = max(per.values())
        G("G3", worst < G3_BAR, f"cross-run vs idea 971 grid.csv ({len(m):,} rows): " +
          "  ".join(f"{k} {v:.3e}" for k, v in per.items()) + f"   bar {G3_BAR:.0e}")
        dis = {pk: int((m[m.panel == pk].pass4b != m[m.panel == pk].p4b_REC_REC5).sum()) for pk in PANELS}
        G("G3b", sum(dis.values()) == 0,
          "cross-run VERDICT vs 971's p4b_REC_REC5: " + "  ".join(f"{k} {v}" for k, v in dis.items()) +
          " disagreements")
    else:
        G("G3", False, f"prior grid {PRIOR_GRID.name} not found")

    g4 = pd.DataFrame(G4_ROWS)
    tr = []
    for pk, bk, gg, cad in need:
        nd = ND[(ND.panel == pk) & (ND.book == bk) & (ND.gross == gg) & (ND.cadence == cad)]
        bt = float(LAD[(LAD.cost == PROTO_COST) & (LAD.panel == pk) & (LAD.book == bk) &
                       (LAD.gross == gg) & (LAD.cadence == cad)].turnover.iloc[0])
        tr.append(float(nd.turnover.median()) / bt if bt > 0 else np.nan)
    G("G4", float(g4.dgross.max()) < 1e-12 and int(g4.dk.max()) == 0 and np.nanmin(tr) > 0.5,
      f"null gross match max|dgross| {g4.dgross.max():.3e}, max dk {int(g4.dk.max())}, "
      f"min null/book realised turnover ratio {np.nanmin(tr):.3f} (bar 0.5)")

    pk, bk, gg, cad = need[0]
    p0 = pnl[pk]
    buf = np.zeros_like(p0.books[gg][bk])
    rng = np.random.default_rng(seed_of(SEED0, pk, bk, gg, cad, 0))
    Wn = draw_null(buf, p0, p0.books[gg][bk], p0.dec[cad], rng).copy()
    r_, t_ = p0.ctx[cad].run(lag_weights(Wn), 0.0)
    r = r_ - t_ * PROTO_COST / 1e4
    ref = ND[(ND.panel == pk) & (ND.book == bk) & (ND.gross == gg) & (ND.cadence == cad) &
             (ND.draw == 0)].Sharpe.iloc[0]
    d5 = float(abs(fmet(r[p0.warm])[1] - ref))
    G("G5", d5 == 0.0, f"determinism: redrawn null draw 0 of {pk}/{bk}/{gg:.2f}/{cad} max|dSharpe| {d5:.3e}")

    import copy
    rng6 = np.random.default_rng(6)
    same = True
    lad2 = []
    for pk_ in PANELS:
        p = pnl[pk_]
        q = copy.copy(p)
        rr = p.rets.copy()
        oi = np.flatnonzero(p.oos)
        rr[oi] = rr[rng6.permutation(oi)]
        q.rets = rr
        q.ctx = {c: Ctx(rr, p.app[c]) for c in CADENCES}
        for bk_ in BOOKS:
            for gg_ in GROSS_GRID:
                W = lag_weights(q.books[gg_][bk_])
                for cad_ in CADENCES:
                    r_, t_ = q.ctx[cad_].run(W, 0.0)
                    r = r_ - t_ * PROTO_COST / 1e4
                    st = stats_of(q, r)
                    lad2.append(dict(panel=pk_, book=bk_, gross=gg_, cadence=cad_, **st,
                                     IS_pass4b=all(legs_4b_is(q, st).values())))
    L2 = pd.DataFrame(lad2)
    L2["IS_asym"] = L2.IS_H2 - L2.IS_H1
    A = LAD[LAD.cost == PROTO_COST].copy()
    A["IS_asym"] = A.IS_H2 - A.IS_H1
    for pk_ in PANELS:
        for cad_ in CADENCES:
            a = A[(A.panel == pk_) & (A.cadence == cad_)]
            b = L2[(L2.panel == pk_) & (L2.cadence == cad_)]
            pairs = [(a.sort_values(["IS_pass4b", "IS_Sharpe"], ascending=[False, False]).iloc[0],
                      b.sort_values(["IS_pass4b", "IS_Sharpe"], ascending=[False, False]).iloc[0]),
                     (a.sort_values("IS_Sharpe", ascending=False).iloc[0],
                      b.sort_values("IS_Sharpe", ascending=False).iloc[0]),
                     (a.assign(_x=a.IS_asym.abs()).sort_values(["_x", "IS_Sharpe"], ascending=[True, False]).iloc[0],
                      b.assign(_x=b.IS_asym.abs()).sort_values(["_x", "IS_Sharpe"], ascending=[True, False]).iloc[0])]
            for pa, pb in pairs:
                same &= (pa.book == pb.book and pa.gross == pb.gross)
    G("G6", same, "rule-8 choosers (incl. C_ISSYM) invariant to permuted OOS return rows (IS-only)")

    l = LAD[LAD.cost == PROTO_COST]
    stray = int((l[l.pass4b].index.difference(l.index)).size) + int((ND[ND.pass4b].index.difference(ND.index)).size)
    d = l.dropna(subset=["A_RATIO"])
    agree = float((np.sign(d.A_RATIO - 1.0) == np.sign(d.A_DIFF)).mean()) if len(d) else np.nan
    agree2 = float((np.sign(l.A_MARGIN) == np.sign(l.A_DIFF)).mean())
    G("G7", stray == 0 and agree >= 0.95,
      f"subset algebra {stray} stray rows; sign(A_RATIO-1)==sign(A_DIFF) on {agree:.4f} of "
      f"{len(d)} rows; sign(A_MARGIN)==sign(A_DIFF) on {agree2:.4f} (A_MARGIN shifts by the "
      f"benchmark's own asymmetry, so it is REPORTED not gated)")
    return pd.DataFrame(g)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Idea 971 (lane B, 2026-09-16) -- is the 2009-2012 HALF the leg that kills every DISJOINT 4b pass?

THE PRIOR RESULT (idea 970, lane B, committed 2026-09-15)
  942 proposed CLAUSE (i): the rule-8 OOS window must be DISJOINT from 4b's second half, so
  the 4b halves are taken INSIDE the in-sample window (2009-2016 split in two).  970 priced
  it on a 900-row grid (3 panels x 5 books x 4 gross x 3 cadences x 5 cost rungs) and found:
    * the disjoint split destroys 2 of 12 REC passes at 10 bps and creates 2, net zero;
    * the ONE STRICT committed pass it destroys (U56/TOP20/g0.75/W at 10 bps) fails on
      `L_H1` ALONE, with a 2009-2012 Sharpe of 0.757;
    * the DISJ null's `L_H1` base rate is 0.730 on U56/M against 0.000 weekly.
  So the clause's whole bite may be arithmetic about ONE window: 2009-2012, the recovery tape,
  where SPY's own Sharpe is extreme and almost nothing clears it.

WHAT THIS RUN DOES
  Censuses the BINDING LEG of every DISJ-DESTROYED and DISJ-CREATED book on 970's own 900-row
  grid, then MOVES THE WINDOW START.  If clause (i) is a rule about leg independence, its
  destruction should survive sliding the in-sample window forward; if it is a test of the
  2009-2012 recovery tape, destruction should collapse as soon as that tape leaves `L_H1`.

  A row can only be destroyed or created through a SHARPE leg: `L_DD`, `L_CAGR` and `L_OOS`
  are read on the FULL sample under every split rule, so they are identical in the REC and
  DISJ columns by construction.  The census is therefore a census of WHICH Sharpe leg, and
  the window-start dial is the instrument that names the tape behind it.

TUNED DIALS (exactly 2; every level ALWAYS reported, none is ever used to choose anything)
  1. WINDOW START  w in {2009, 2010, 2011, 2012, 2013}-01-01.  DISJ_w reads `L_H1`/`L_H2` as
     the two halves of [max(w, warm-up), 2016-12-31].  w=2009 reproduces 970's DISJ exactly
     (gated, G3b).  At w=2012 the 2009-2012 recovery tape has left the book entirely.
  2. LEG SET       REC5 = (L_H1, L_H2, L_OOS, L_DD, L_CAGR) -- the record's own bar;
                   FOUR = REC5 minus L_OOS -- idea 972's finding that L_OOS never binds;
                   SHARPE2 = (L_H1, L_H2) -- the clause's own object, isolated.

REPORTED, NEVER FITTED
  PANEL {U56, B136, SMALL663}, BOOK {TOP5, TOP10, TOP20, EWELIG, BAND03}, GROSS {0.50, 0.65,
  0.75, 1.00}, COST RUNG {0, 5, 10, 25, 50} bps with 10 BINDING (PROTOCOL rule 2).  These are
  the record's own committed ladders (idea 937 / 970), fixed before any number here was read.

PRE-REGISTERED HYPOTHESES (bars fixed before any number was read)
  H_H1     the binding leg of DISJ destruction is `L_H1`.  PASS iff, pooled over the 5 cost
           rungs at w=2009 under REC5, >= 0.50 of DESTROYED rows have `L_H1` in their binding
           set.  (970 read 1 of 1 on its single STRICT committed pass.)
  H_TAPE   destruction is a property of the 2009-2012 tape, not of the rule.  PASS iff the
           pooled destroyed count at w=2012 is <= 0.50x the count at w=2009 (REC5, all rungs).
  H_SPY    the mechanism is SPY's OWN first-half Sharpe.  PASS iff, on >= 2 of 3 panels,
           SPY's DISJ `L_H1` reference Sharpe is (a) the MAXIMUM over the 5 window starts and
           (b) strictly greater than SPY's own DISJ `L_H2` reference at w=2009.
  H_NULLH1 the same leg carries destruction on a gross-matched COIN FLIP.  PASS iff the
           MEDIAN over the 9 (panel, cadence) null cells of the share of destroyed draws whose
           binding set contains `L_H1` is >= 0.50 at w=2009, REC5.
  H_RULE8  the clause is not verdict-neutral out of sample: moving the window start changes
           what rule 8 certifies.  PASS iff the OOS 4b pass count over the walk-forward picks
           differs by >= 1 between at least two window starts (REC5, 10 bps).

RULE 8 (walk-forward, mandatory -- PROTOCOL rule 8)
  (book, gross) is chosen on the IN-SAMPLE window ALONE by three IS-only choosers, per
  (panel, cadence, window start) -- the chooser sees [w, 2016-12-31] and nothing else.
  2017-2026 is then read ONCE.  OOS CAGR / Sharpe / MaxDD are reported against the RULES v2
  baseline and against SPY, and BOTH KEEP paths (4a and 4b) are scored on every pick under
  every (window start, leg set).  G6 proves the choosers are IS-only by permuting OOS rows.

GATES
  G1  closed-form runner == `engine.backtest` @10 bps, 3 books x 3 cadences.  Bar 1e-12.
  G2  BAND03 @0.75 weights == `baseline.rules_v2_weights(px, 0.03, 0.75)`.  Bar 0.0 exact.
  G3a CROSS-RUN: this run's REC grid statistics vs idea 970's committed `grid.csv`, all 900
      rows (CAGR, Sharpe, MaxDD, OOS_Sharpe).  Bar 1e-09.  `data/prices.csv` is restated
      nightly (idea 974's G3 defect), so a miss here is REPORTED, never tuned away.
  G3b CROSS-RUN of the VERDICTS: this run's `p4b_DISJ2009` and `p4b_REC` vs 970's committed
      columns on all 900 rows.  Bar 0 disagreements.
  G4  GROSS MATCH: every null's gross and holding count equal the reference book's on every
      decision row (bar 0.0) and realised annual turnover > 0.5x (idea 931's defect).
  G5  determinism: a redrawn null is bit-for-bit identical; and the null stream reproduces
      idea 970's committed `nulls.csv` Sharpe column (same seeds, same construction).
  G6  every rule-8 chooser is IS-ONLY: picks invariant to permuted OOS return columns.
  G7  DISJOINTNESS at every window start: |H1 n H2| = |H2 n OOS| = |H1 n OOS| = 0 rows, and
      under REC the H2 n OOS overlap is non-zero (the defect clause (i) was written for).
  G8  LEG ALGEBRA: on all 900 rows and every window start, the DD / CAGR / OOS legs are
      IDENTICAL between REC and DISJ (bar 0 disagreements) -- so every created and destroyed
      row is a SHARPE-leg event by construction, which is what makes the census well posed.

SURVIVORSHIP (PROTOCOL rule 9)
  U56 / B136 / SMALL663 are CURRENT-constituent lists, so every CAGR and drawdown LEVEL here
  is optimistic and every null base rate is an UPPER bound.  The measured object is the SAME
  books on the SAME tape under different WINDOW DEFINITIONS, so the created/destroyed contrast
  and the binding-leg census are untouched by it; the walk-forward LEVELS are not.

COSTS 10 bps per unit turnover binding; weights decided at close t applied at close t+1.
"""
from __future__ import annotations

import hashlib
import os
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

WSTARTS = ["2009-01-01", "2010-01-01", "2011-01-01", "2012-01-01", "2013-01-01"]
WTAG = {w: "DISJ" + w[:4] for w in WSTARTS}
ALL_LEGS = ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")
LEGSETS = {"REC5": ALL_LEGS,
           "FOUR": ("L_H1", "L_H2", "L_DD", "L_CAGR"),
           "SHARPE2": ("L_H1", "L_H2")}

DRAWS = 200
SEED0 = 970                  # idea 970's seed base, so the null stream reproduces (G5)
NULL_BOOK, NULL_GROSS = "TOP20", 0.75

H1_BAR = 0.50                # H_H1
TAPE_BAR = 0.50              # H_TAPE
NULLH1_BAR = 0.50            # H_NULLH1

PRIOR = OUT / "2026-09-15_does-4b-SURVIVE-a-DISJOINT-HALVES-SPLIT_B.grid.csv"
PRIOR_NULLS = OUT / "2026-09-15_does-4b-SURVIVE-a-DISJOINT-HALVES-SPLIT_B.nulls.csv"
G3A_BAR = 1e-9

SMOKE = bool(int(os.environ.get("IDEA971_SMOKE", "0")))
if SMOKE:
    DRAWS = 4

LOG: list[str] = []


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
    """The tape, the REC window set, one DISJ window set per window start, and SPY's legs."""

    def __init__(self, name, px):
        self.name, self.px, self.idx = name, px, px.index
        self.rets = np.nan_to_num(px.pct_change().values, nan=0.0, posinf=0.0, neginf=0.0)
        self.T = len(self.idx)
        self.warm = np.arange(self.T) >= WARMUP
        wpos = np.flatnonzero(self.warm)

        self.oos = np.asarray(self.idx >= pd.Timestamp(OOS_START)) & self.warm
        self.is_ = self.warm & np.asarray(self.idx <= pd.Timestamp(IS_END))

        h = len(wpos) // 2                       # REC halves: the FULL post-warm-up sample
        self.rec_h1 = np.zeros(self.T, bool); self.rec_h1[wpos[:h]] = True
        self.rec_h2 = np.zeros(self.T, bool); self.rec_h2[wpos[h:]] = True
        self.rec_h2_start = self.idx[wpos[h]]

        self.win = {"REC": (self.rec_h1, self.rec_h2)}
        self.iswin = {}                          # the chooser's IS window per window start
        self.wstart_date = {}
        for w in WSTARTS:
            m = self.is_ & np.asarray(self.idx >= pd.Timestamp(w))
            self.iswin[w] = m
            ipos = np.flatnonzero(m)
            hi = len(ipos) // 2
            a = np.zeros(self.T, bool); a[ipos[:hi]] = True
            b = np.zeros(self.T, bool); b[ipos[hi:]] = True
            self.win[WTAG[w]] = (a, b)
            self.wstart_date[w] = (self.idx[ipos[0]], self.idx[ipos[hi]], self.idx[ipos[-1]])

        spy = np.nan_to_num(px["SPY"].pct_change().values, nan=0.0)
        self.spy = spy
        self.spy_full = fmet(spy[self.warm])
        self.spy_oos_s = fmet(spy[self.oos])[1]
        self.spy_leg = {s: (fmet(spy[a])[1], fmet(spy[b])[1]) for s, (a, b) in self.win.items()}

        self.priced = px.notna().values
        above = px > px.rolling(200).mean()
        vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        self.elig = (above & (vol20 < VOLCAP) & px.notna()).values
        self.dec = {c: rebalance_mask(self.idx, c).values.copy() for c in CADENCES}
        self.app = {c: applied_from_decision(self.dec[c]) for c in CADENCES}
        self.ctx = {c: Ctx(self.rets, self.app[c]) for c in CADENCES}
        bw = lag_weights(rules_v2_weights(px, BAND0, 0.75).values)     # the live book = the 4a bar
        self.base_r = {c_: self.ctx["W"].run(bw, c_)[0] for c_ in COSTS}


SPLITS = ["REC"] + [WTAG[w] for w in WSTARTS]


def stats_of(pn, r):
    c, s, dd = fmet(r[pn.warm])
    oc, os_, odd = fmet(r[pn.oos])
    out = dict(CAGR=c, Sharpe=s, MaxDD=dd, OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=odd)
    for sp, (a, b) in pn.win.items():
        out[f"{sp}_H1"] = fmet(r[a])[1]
        out[f"{sp}_H2"] = fmet(r[b])[1]
    return out


def legs_4b(pn, st, sp):
    """The five 4b legs under split rule `sp`.  L_DD / L_CAGR / L_OOS are FULL-sample under
    every split rule, so only the two Sharpe legs move with the window start (gated at G8)."""
    return dict(L_H1=bool(st[f"{sp}_H1"] > pn.spy_leg[sp][0]),
                L_H2=bool(st[f"{sp}_H2"] > pn.spy_leg[sp][1]),
                L_OOS=bool(st["OOS_Sharpe"] > pn.spy_oos_s),
                L_DD=bool(abs(st["MaxDD"]) <= DD_CAP * abs(pn.spy_full[2])),
                L_CAGR=bool(st["CAGR"] >= CAGR_FLOOR * pn.spy_full[0]))


def pass_4a(pn, r, bst, sp):
    """4a: Sharpe > the LIVE RULES v2 book in BOTH halves of this split rule, MaxDD no worse."""
    a, b = pn.win[sp]
    return bool(fmet(r[a])[1] > fmet(bst[a])[1] and fmet(r[b])[1] > fmet(bst[b])[1]
                and fmet(r[pn.warm])[2] >= fmet(bst[pn.warm])[2])


def build_books(px, g):
    """The record's five book templates at gross g, as TARGET WEIGHT matrices (unlagged)."""
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


def draw_null(buf, pn, W, dec, rng):
    """Gross-matched ROTATING coin flip (idea 680/926/931/942/970's RANDROT, unmodified)."""
    buf[:] = 0.0
    held = W > 0
    kcount = held.sum(axis=1)
    gross = W.sum(axis=1)
    for i in np.flatnonzero(dec):
        k = int(kcount[i])
        if k == 0:
            continue
        pool = np.flatnonzero(pn.elig[i])
        if len(pool) == 0:
            pool = np.flatnonzero(pn.priced[i])
        if len(pool) == 0:
            continue
        k = min(k, len(pool))
        pick = rng.choice(pool, size=k, replace=False)
        buf[i, pick] = gross[i] / k
    return buf


def binding(legs, legset):
    return ",".join(l for l in legset if not legs[l])


# =================================================================================================
def main():
    LOG.clear()
    sha = head_sha()
    P("=" * 100)
    P("IDEA 971 (lane B) -- is the 2009-2012 HALF the leg that kills every DISJOINT 4b pass?")
    P(f"sha {sha} | draws {DRAWS} | binding rung {PROTO_COST:.0f} bps | smoke {SMOKE}")
    P(f"window starts (TUNED dial 1): {', '.join(WSTARTS)}")
    P(f"leg sets     (TUNED dial 2): {', '.join(LEGSETS)}")
    P("=" * 100)

    P("\nloading panels ...")
    px = {"U56": load_universe(), "B136": load_universe(broad=True)}
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    px["SMALL663"] = sm[[c for c in sm.columns if c == "SPY" or c not in bad]]
    n_drop = len(sm.columns) - px["SMALL663"].shape[1]
    pans = {k: Panel(k, v) for k, v in px.items()}
    for k, p in pans.items():
        P(f"  {k}: {p.px.shape[1]} cols x {p.T} rows, {p.idx[0].date()} -> {p.idx[-1].date()}")

    W = {}
    for k in PANELS:
        for g in GROSS_GRID:
            bk, _ = build_books(pans[k].px, g)
            for b, w in bk.items():
                W[(k, b, g)] = w

    # ------------------------------------------------------------------ GATES -----------------
    P("\n" + "-" * 100)
    P("GATES (printed before any result number)")
    P("-" * 100)
    gates = {}
    g1 = 0.0
    for b in ("TOP20", "EWELIG", "BAND03"):
        for c in CADENCES:
            w = W[("U56", b, 0.75)]
            mine = pans["U56"].ctx[c].run(lag_weights(w), PROTO_COST)[0]
            eng = backtest(px["U56"], pd.DataFrame(w, index=px["U56"].index, columns=px["U56"].columns),
                           cost_bps=PROTO_COST, freq=c)["returns"].values
            g1 = max(g1, float(np.abs(mine[WARMUP:] - eng[WARMUP:]).max()))
    gates["G1"] = g1 < 1e-12
    P(f"  G1  closed-form runner == engine.backtest, 3 books x 3 cadences: max|d| = {g1:.3e}  "
      f"[{'PASS' if gates['G1'] else 'FAIL'}]")

    g2 = float(np.abs(W[("U56", "BAND03", 0.75)] - rules_v2_weights(px["U56"], BAND0, 0.75).values).max())
    gates["G2"] = g2 == 0.0
    P(f"  G2  BAND03@0.75 == baseline.rules_v2_weights: max|d| = {g2:.3e}  "
      f"[{'PASS' if gates['G2'] else 'FAIL'}]")

    ok7 = True
    P("  G7  window sets, per panel and window start:")
    for k in PANELS:
        q = pans[k]
        orec = int((q.rec_h2 & q.oos).sum())
        ok7 = ok7 and orec > 0
        P(f"      {k}: REC H2 starts {q.rec_h2_start.date()}, REC H2 n OOS = {orec} days "
          f"(the defect clause (i) was written for)")
        for w in WSTARTS:
            a, b = q.win[WTAG[w]]
            o1, o2, o3 = int((a & b).sum()), int((b & q.oos).sum()), int((a & q.oos).sum())
            ok7 = ok7 and o1 == 0 and o2 == 0 and o3 == 0
            d0, dm, d1 = q.wstart_date[w]
            P(f"        {WTAG[w]}: H1 {d0.date()}->, H2 {dm.date()}->{d1.date()}; "
              f"overlaps {o1}/{o2}/{o3}; SPY legs H1 {q.spy_leg[WTAG[w]][0]:.3f} / "
              f"H2 {q.spy_leg[WTAG[w]][1]:.3f}")
    gates["G7"] = ok7
    P(f"  G7  disjointness at every window start  [{'PASS' if ok7 else 'FAIL'}]")
    P(f"      SMALL663 screen: {n_drop} tickers with max_1d_move >= 1.0 dropped")

    # SPY's own reference legs -- the mechanism H_SPY tests
    spy_rows = []
    for k in PANELS:
        q = pans[k]
        row = dict(panel=k, REC_H1=q.spy_leg["REC"][0], REC_H2=q.spy_leg["REC"][1],
                   OOS=q.spy_oos_s, FULL_Sharpe=q.spy_full[1], FULL_CAGR=q.spy_full[0],
                   FULL_MaxDD=q.spy_full[2])
        for w in WSTARTS:
            row[f"{WTAG[w]}_H1"] = q.spy_leg[WTAG[w]][0]
            row[f"{WTAG[w]}_H2"] = q.spy_leg[WTAG[w]][1]
        spy_rows.append(row)
    spywin = pd.DataFrame(spy_rows)
    P("\n  SPY's own reference Sharpe in every window (the bar each leg must clear):")
    P(spywin.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    dump(spywin, "spywindows.csv")

    buf = np.zeros_like(pans["U56"].rets)
    wref = W[("U56", NULL_BOOK, NULL_GROSS)]
    q = pans["U56"]
    gm, km, tmin = 0.0, 0, 1e9
    for d in range(3):
        rg = np.random.default_rng(seed_of("U56", "M", d))
        nw = draw_null(buf, q, wref, q.dec["M"], rg)
        gm = max(gm, float(np.abs(nw[q.dec["M"]].sum(axis=1) - wref[q.dec["M"]].sum(axis=1)).max()))
        km = max(km, int(np.abs((nw[q.dec["M"]] > 0).sum(axis=1) - (wref[q.dec["M"]] > 0).sum(axis=1)).max()))
        tmin = min(tmin, q.ctx["M"].run(lag_weights(nw), PROTO_COST)[1][q.warm].sum() / (q.warm.sum() / 252.0))
    gates["G4"] = gm < 1e-12 and km == 0 and tmin > 0.5
    P(f"\n  G4  gross match on 3 draws: max|d gross| = {gm:.3e}, max|d count| = {km}, "
      f"min realised annual turnover = {tmin:.2f}x  [{'PASS' if gates['G4'] else 'FAIL'}]")

    a_ = draw_null(np.zeros_like(q.rets), q, wref, q.dec["M"], np.random.default_rng(seed_of("U56", "M", 7)))
    b_ = draw_null(np.zeros_like(q.rets), q, wref, q.dec["M"], np.random.default_rng(seed_of("U56", "M", 7)))
    g5a = float(np.abs(a_ - b_).max()) == 0.0
    P(f"  G5a determinism / seed reproducibility: max|d| = {np.abs(a_ - b_).max():.3e}  "
      f"[{'PASS' if g5a else 'FAIL'}]")

    # ------------------------------------------------------------- THE BOOK GRID --------------
    ncell = len(PANELS) * len(BOOKS) * len(GROSS_GRID) * len(CADENCES) * len(COSTS)
    P("\n" + "-" * 100)
    P(f"BOOK GRID -- {ncell:,} book rows, each scored under REC and {len(WSTARTS)} DISJ window starts")
    P("-" * 100)
    rows = []
    for k in PANELS:
        q = pans[k]
        for b in BOOKS:
            for g in GROSS_GRID:
                wl = lag_weights(W[(k, b, g)])
                for c in CADENCES:
                    r_full, turn = q.ctx[c].run(wl, 0.0)
                    ann_turn = turn[q.warm].sum() / (q.warm.sum() / 252.0)
                    for cost in COSTS:
                        r = r_full - turn * cost / 1e4
                        st = stats_of(q, r)
                        row = dict(panel=k, book=b, gross=g, cadence=c, cost=cost,
                                   turnover=ann_turn, CAGR=st["CAGR"], Sharpe=st["Sharpe"],
                                   MaxDD=st["MaxDD"], OOS_CAGR=st["OOS_CAGR"],
                                   OOS_Sharpe=st["OOS_Sharpe"], OOS_MaxDD=st["OOS_MaxDD"])
                        for sp in SPLITS:
                            lg = legs_4b(q, st, sp)
                            row[f"{sp}_H1"] = st[f"{sp}_H1"]
                            row[f"{sp}_H2"] = st[f"{sp}_H2"]
                            for ln, v in lg.items():
                                row[f"{sp}_{ln}"] = v
                            for ls, legset in LEGSETS.items():
                                row[f"p4b_{sp}_{ls}"] = all(lg[l] for l in legset)
                            row[f"p4a_{sp}"] = pass_4a(q, r, q.base_r[cost], sp)
                        rows.append(row)
    grid = pd.DataFrame(rows)
    dump(grid, "grid.csv")

    # G8 -- leg algebra: the non-Sharpe legs never move with the window start
    dis8 = 0
    for w in WSTARTS:
        for ln in ("L_OOS", "L_DD", "L_CAGR"):
            dis8 += int((grid[f"REC_{ln}"] != grid[f"{WTAG[w]}_{ln}"]).sum())
    gates["G8"] = dis8 == 0
    P(f"\n  G8  LEG ALGEBRA: DD / CAGR / OOS identical between REC and every DISJ_w on "
      f"{len(grid):,} rows x {len(WSTARTS)} starts: {dis8} disagreements  "
      f"[{'PASS' if gates['G8'] else 'FAIL'}]")

    # G3 -- cross-run against idea 970's committed grid
    if PRIOR.exists():
        pr = pd.read_csv(PRIOR)
        key = ["panel", "book", "gross", "cadence", "cost"]
        m = grid.merge(pr, on=key, suffixes=("", "_970"))
        d3 = {c: float(np.abs(m[c] - m[f"{c}_970"]).max()) for c in
              ("CAGR", "Sharpe", "MaxDD", "OOS_Sharpe")}
        g3a = (len(m) == len(grid)) and max(d3.values()) < G3A_BAR
        gates["G3a"] = g3a
        P(f"  G3a CROSS-RUN vs idea 970's committed grid.csv on {len(m):,} matched rows: "
          + ", ".join(f"{c} {v:.3e}" for c, v in d3.items())
          + f"  (bar {G3A_BAR:.0e})  [{'PASS' if g3a else 'FAIL'}]")
        if not g3a:
            P("      NOT tuned away: data/prices.csv is restated nightly (idea 974's G3 defect); "
              "the VERDICT cross-run G3b is the binding reproduction test.")
        dis_rec = int((m["p4b_REC_REC5"].astype(bool) != m["p4b_REC"].astype(bool)).sum())
        dis_dis = int((m["p4b_DISJ2009_REC5"].astype(bool) != m["p4b_DISJ"].astype(bool)).sum())
        gates["G3b"] = dis_rec == 0 and dis_dis == 0
        P(f"  G3b CROSS-RUN of the VERDICTS vs 970: p4b_REC {dis_rec} disagreements, "
          f"p4b_DISJ2009 vs its p4b_DISJ {dis_dis} disagreements of {len(m):,}  "
          f"[{'PASS' if gates['G3b'] else 'FAIL'}]")
    else:
        gates["G3a"] = gates["G3b"] = False
        P("  G3  idea 970's committed grid.csv not found  [FAIL]")

    at10 = grid[grid.cost == PROTO_COST]
    P(f"\n  4b PASS counts at {PROTO_COST:.0f} bps over {len(at10)} book rows, by split rule x leg set:")
    tab = pd.DataFrame({ls: {sp: int(at10[f"p4b_{sp}_{ls}"].sum()) for sp in SPLITS}
                        for ls in LEGSETS})
    tab["4a"] = {sp: int(at10[f"p4a_{sp}"].sum()) for sp in SPLITS}
    P(tab.to_string())
    P("\n  4b PASS counts (REC5) over the whole 900-row grid, by cost rung:")
    tabc = pd.DataFrame({sp: grid.groupby("cost")[f"p4b_{sp}_REC5"].sum().astype(int) for sp in SPLITS})
    P(tabc.to_string())

    # ------------------------------------------- CREATED / DESTROYED + BINDING LEG ------------
    P("\n" + "-" * 100)
    P("THE CENSUS -- every DESTROYED and CREATED book on the 900-row grid, with its BINDING LEG")
    P("-" * 100)
    brows, crows = [], []
    for ls, legset in LEGSETS.items():
        for w in WSTARTS:
            sp = WTAG[w]
            for cost in COSTS:
                sub = grid[grid.cost == cost]
                rec = sub[f"p4b_REC_{ls}"].values
                dis = sub[f"p4b_{sp}_{ls}"].values
                dest = np.flatnonzero(rec & ~dis)
                crea = np.flatnonzero(~rec & dis)
                for i in dest:
                    r = sub.iloc[i]
                    lg = {l: bool(r[f"{sp}_{l}"]) for l in ALL_LEGS}
                    brows.append(dict(legset=ls, wstart=w, cost=cost, kind="DESTROYED",
                                      panel=r.panel, book=r.book, gross=r.gross, cadence=r.cadence,
                                      binding=binding(lg, legset),
                                      rec_h1=r["REC_H1"], rec_h2=r["REC_H2"],
                                      disj_h1=r[f"{sp}_H1"], disj_h2=r[f"{sp}_H2"],
                                      spy_h1=pans[r.panel].spy_leg[sp][0],
                                      spy_h2=pans[r.panel].spy_leg[sp][1]))
                for i in crea:
                    r = sub.iloc[i]
                    lg = {l: bool(r[f"REC_{l}"]) for l in ALL_LEGS}
                    brows.append(dict(legset=ls, wstart=w, cost=cost, kind="CREATED",
                                      panel=r.panel, book=r.book, gross=r.gross, cadence=r.cadence,
                                      binding=binding(lg, legset),
                                      rec_h1=r["REC_H1"], rec_h2=r["REC_H2"],
                                      disj_h1=r[f"{sp}_H1"], disj_h2=r[f"{sp}_H2"],
                                      spy_h1=pans[r.panel].spy_leg[sp][0],
                                      spy_h2=pans[r.panel].spy_leg[sp][1]))
                crows.append(dict(legset=ls, wstart=w, cost=cost, rec_passes=int(rec.sum()),
                                  destroyed=len(dest), created=len(crea), after=int(dis.sum()),
                                  destroyed_share=(len(dest) / rec.sum()) if rec.sum() else np.nan,
                                  net=len(crea) - len(dest)))
    bind = pd.DataFrame(brows)
    cd = pd.DataFrame(crows)
    dump(bind, "binding.csv")
    dump(cd, "created_destroyed.csv")

    P("\n  created / destroyed by WINDOW START (rows pooled over the 5 cost rungs), per leg set:")
    piv = cd.groupby(["legset", "wstart"]).agg(rec_passes=("rec_passes", "sum"),
                                               destroyed=("destroyed", "sum"),
                                               created=("created", "sum"),
                                               after=("after", "sum")).reset_index()
    piv["destroyed_share"] = piv.destroyed / piv.rec_passes.replace(0, np.nan)
    piv["net"] = piv.created - piv.destroyed
    P(piv.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    P(f"\n  created / destroyed at the binding rung ({PROTO_COST:.0f} bps) only:")
    P(cd[cd.cost == PROTO_COST].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    P("\n  BINDING-LEG CENSUS -- what actually flips, by window start (REC5, all rungs pooled):")
    if len(bind):
        bl = bind[bind.legset == "REC5"]
        for kind in ("DESTROYED", "CREATED"):
            sub = bl[bl.kind == kind]
            if not len(sub):
                P(f"    {kind}: 0 rows at any window start")
                continue
            t = sub.groupby(["wstart", "binding"]).size().unstack(fill_value=0)
            P(f"    {kind} ({len(sub)} rows):")
            P("      " + t.to_string().replace("\n", "\n      "))
        P("\n  every DESTROYED / CREATED row at the binding rung (REC5):")
        show = bl[(bl.cost == PROTO_COST)][["wstart", "kind", "panel", "book", "gross", "cadence",
                                            "binding", "rec_h1", "rec_h2", "disj_h1", "disj_h2",
                                            "spy_h1", "spy_h2"]]
        P("    " + (show.to_string(index=False, float_format=lambda x: f"{x:.3f}")
                    if len(show) else "(none)").replace("\n", "\n    "))
    else:
        P("    0 created or destroyed rows anywhere on the grid")

    P("\n  MECHANISM -- the destroyed share against SPY's OWN first-half bar, by window start")
    P("  (REC5, pooled over the 5 cost rungs; SPY's bar is panel-invariant except on SMALL663,")
    P("   whose tape starts 2010 -- the U56 column is printed and the SMALL663 one is in "
      "spywindows.csv)")
    mech = piv[piv.legset == "REC5"][["wstart", "rec_passes", "destroyed", "created",
                                      "destroyed_share"]].copy()
    mech["SPY_H1_bar"] = [pans["U56"].spy_leg[WTAG[w]][0] for w in mech.wstart]
    mech["SPY_H2_bar"] = [pans["U56"].spy_leg[WTAG[w]][1] for w in mech.wstart]
    mech["half_len_days"] = [int(pans["U56"].win[WTAG[w]][0].sum()) for w in mech.wstart]
    P(mech.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    def spearman(a, b):                      # rank-then-Pearson; scipy is not installed here
        ra, rb = pd.Series(a).rank(), pd.Series(b).rank()
        return float(ra.corr(rb))
    rho = spearman(mech.destroyed_share, mech.SPY_H1_bar)
    rho_len = spearman(mech.destroyed_share, mech.half_len_days)
    P(f"  Spearman(destroyed_share, SPY's H1 bar) = {rho:+.3f} over {len(mech)} window starts; "
      f"Spearman(destroyed_share, half length) = {rho_len:+.3f}")
    dump(mech, "mechanism.csv")

    # ------------------------------------------------------------- THE NULL -------------------
    P("\n" + "-" * 100)
    P(f"NULL GRID -- {len(PANELS)*len(CADENCES)*DRAWS:,} gross-matched rotating coin flips at "
      f"{PROTO_COST:.0f} bps, scored under REC and every DISJ window start")
    P("-" * 100)
    nrows = []
    for k in PANELS:
        q = pans[k]
        wref = W[(k, NULL_BOOK, NULL_GROSS)]
        buf = np.zeros_like(q.rets)
        for c in CADENCES:
            rng = np.random.default_rng(seed_of(k, c, "stream", SEED0))
            for d in range(DRAWS):
                nw = draw_null(buf, q, wref, q.dec[c], rng)
                r = q.ctx[c].run(lag_weights(nw), PROTO_COST)[0]
                st = stats_of(q, r)
                row = dict(panel=k, cadence=c, draw=d, CAGR=st["CAGR"], Sharpe=st["Sharpe"],
                           MaxDD=st["MaxDD"], OOS_Sharpe=st["OOS_Sharpe"])
                for sp in SPLITS:
                    lg = legs_4b(q, st, sp)
                    for ln, v in lg.items():
                        row[f"{sp}_{ln}"] = v
                    for ls, legset in LEGSETS.items():
                        row[f"p4b_{sp}_{ls}"] = all(lg[l] for l in legset)
                nrows.append(row)
        P(f"  {k}: done")
    nulls = pd.DataFrame(nrows)
    nulls.to_csv(OUT / f"{STEM}.nulls.csv.gz", index=False, compression="gzip")
    P(f"  wrote {STEM}.nulls.csv.gz  ({len(nulls):,} rows, {len(nulls.columns)} cols)")

    # G5b -- the null stream reproduces idea 970's committed draws
    if PRIOR_NULLS.exists() and not SMOKE:
        pn970 = pd.read_csv(PRIOR_NULLS)
        mm = nulls.merge(pn970[["panel", "cadence", "draw", "Sharpe", "CAGR", "MaxDD"]],
                         on=["panel", "cadence", "draw"], suffixes=("", "_970"))
        d5 = max(float(np.abs(mm[c] - mm[f"{c}_970"]).max()) for c in ("Sharpe", "CAGR", "MaxDD"))
        g5b = len(mm) == len(nulls) and d5 < 1e-9
        P(f"  G5b null stream reproduces idea 970's committed nulls.csv on {len(mm):,} draws: "
          f"max|d| = {d5:.3e}  [{'PASS' if g5b else 'FAIL'}]")
        if not g5b:
            P("      (same seeds and construction; a miss is the nightly prices.csv restatement, "
              "reported not tuned away)")
    else:
        g5b = g5a
        P("  G5b skipped (smoke run or 970's nulls.csv absent)")
    gates["G5"] = g5a and g5b

    nb_rows = []
    for (k, c), gs in nulls.groupby(["panel", "cadence"]):
        for ls, legset in LEGSETS.items():
            for w in WSTARTS:
                sp = WTAG[w]
                rec = gs[f"p4b_REC_{ls}"].values
                dis = gs[f"p4b_{sp}_{ls}"].values
                dest = rec & ~dis
                crea = ~rec & dis
                nh1 = int((dest & ~gs[f"{sp}_L_H1"].values).sum())
                nh2 = int((dest & ~gs[f"{sp}_L_H2"].values).sum())
                nb_rows.append(dict(panel=k, cadence=c, legset=ls, wstart=w, draws=len(gs),
                                    base_REC=float(rec.mean()), base_DISJ=float(dis.mean()),
                                    destroyed=int(dest.sum()), created=int(crea.sum()),
                                    dest_share=(dest.sum() / rec.sum()) if rec.sum() else np.nan,
                                    bind_H1=(nh1 / dest.sum()) if dest.sum() else np.nan,
                                    bind_H2=(nh2 / dest.sum()) if dest.sum() else np.nan))
    nb = pd.DataFrame(nb_rows)
    dump(nb, "nullbinding.csv")
    P("\n  null 4b base rates and destruction, REC5, by window start (median over the 9 cells):")
    med = nb[nb.legset == "REC5"].groupby("wstart")[
        ["base_REC", "base_DISJ", "dest_share", "bind_H1", "bind_H2"]].median()
    P(med.to_string(float_format=lambda x: f"{x:.3f}"))
    P("\n  per-cell null leg base rates at w=2009 vs w=2012 (REC5):")
    lp = nulls.groupby(["panel", "cadence"])[
        ["REC_L_H1", "REC_L_H2", "DISJ2009_L_H1", "DISJ2009_L_H2",
         "DISJ2012_L_H1", "DISJ2012_L_H2"]].mean()
    P(lp.to_string(float_format=lambda x: f"{x:.3f}"))
    dump(lp.reset_index(), "nulllegrates.csv")

    # ---------------------------------------------------- RULE 8 WALK-FORWARD -----------------
    P("\n" + "-" * 100)
    P("RULE 8 WALK-FORWARD -- (book, gross) chosen on the IS window ALONE, 2017-2026 read ONCE")
    P("-" * 100)
    CH = ["CH_SHARPE", "CH_CAGR", "CH_CALMAR"]
    wf_rows = []
    for k in PANELS:
        q = pans[k]
        spy_oos = fmet(q.spy[q.oos])
        base_oos = fmet(q.base_r[PROTO_COST][q.oos])
        for c in CADENCES:
            streams = {}
            for b in BOOKS:
                for g in GROSS_GRID:
                    streams[(b, g)] = q.ctx[c].run(lag_weights(W[(k, b, g)]), PROTO_COST)[0]
            for w in WSTARTS:
                m = q.iswin[w]
                cand = [(b, g, r) + fmet(r[m]) for (b, g), r in streams.items()]
                for ch in CH:
                    if ch == "CH_SHARPE":
                        pick = max(cand, key=lambda x: (-1e9 if np.isnan(x[4]) else x[4]))
                    elif ch == "CH_CAGR":
                        pick = max(cand, key=lambda x: (-1e9 if np.isnan(x[3]) else x[3]))
                    else:
                        pick = max(cand, key=lambda x: (-1e9 if (np.isnan(x[3]) or x[5] == 0)
                                                        else x[3] / abs(x[5])))
                    b, g, r = pick[0], pick[1], pick[2]
                    st = stats_of(q, r)
                    row = dict(panel=k, cadence=c, wstart=w, chooser=ch, pick_book=b, pick_gross=g,
                               OOS_CAGR=st["OOS_CAGR"], OOS_Sharpe=st["OOS_Sharpe"],
                               OOS_MaxDD=st["OOS_MaxDD"],
                               SPY_OOS_CAGR=spy_oos[0], SPY_OOS_Sharpe=spy_oos[1],
                               SPY_OOS_MaxDD=spy_oos[2], BASE_OOS_CAGR=base_oos[0],
                               BASE_OOS_Sharpe=base_oos[1], BASE_OOS_MaxDD=base_oos[2])
                    for sp in ("REC", WTAG[w]):
                        lg = legs_4b(q, st, sp)
                        tag = "REC" if sp == "REC" else "DISJ"
                        for ls, legset in LEGSETS.items():
                            row[f"p4b_{tag}_{ls}"] = all(lg[l] for l in legset)
                        row[f"fail_{tag}"] = binding(lg, ALL_LEGS)
                        row[f"p4a_{tag}"] = pass_4a(q, r, q.base_r[PROTO_COST], sp)
                    wf_rows.append(row)
    wf = pd.DataFrame(wf_rows)
    dump(wf, "walkforward.csv")
    P(wf[["panel", "cadence", "wstart", "chooser", "pick_book", "pick_gross", "OOS_CAGR",
          "OOS_Sharpe", "OOS_MaxDD", "p4b_REC_REC5", "p4b_DISJ_REC5", "p4a_REC", "p4a_DISJ"]]
      .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    P(f"\n  rule-8 OOS pass counts over {len(wf)} picks ({len(WSTARTS)} window starts x "
      f"{len(PANELS)} panels x {len(CADENCES)} cadences x {len(CH)} choosers):")
    wfw = wf.groupby("wstart").agg(picks=("pick_book", "size"),
                                   p4b_REC=("p4b_REC_REC5", "sum"),
                                   p4b_DISJ=("p4b_DISJ_REC5", "sum"),
                                   p4a_REC=("p4a_REC", "sum"), p4a_DISJ=("p4a_DISJ", "sum"),
                                   OOS_Sharpe_med=("OOS_Sharpe", "median"),
                                   OOS_CAGR_med=("OOS_CAGR", "median"))
    P(wfw.to_string(float_format=lambda x: f"{x:.3f}"))
    best = wf.loc[wf.OOS_Sharpe.idxmax()]
    P(f"\n  best OOS pick: {best.panel}/{best.cadence}/w{best.wstart[:4]}/{best.chooser} -> "
      f"{best.pick_book}@g{best.pick_gross}   OOS {best.OOS_CAGR:.2%} / {best.OOS_Sharpe:.3f} / "
      f"{best.OOS_MaxDD:.2%}")
    P(f"    vs SPY OOS   {best.SPY_OOS_CAGR:.2%} / {best.SPY_OOS_Sharpe:.3f} / {best.SPY_OOS_MaxDD:.2%}")
    P(f"    vs RULES v2  {best.BASE_OOS_CAGR:.2%} / {best.BASE_OOS_Sharpe:.3f} / {best.BASE_OOS_MaxDD:.2%}")
    P(f"    4b REC {bool(best.p4b_REC_REC5)} / DISJ {bool(best.p4b_DISJ_REC5)}; "
      f"4a REC {bool(best.p4a_REC)} / DISJ {bool(best.p4a_DISJ)}")
    P(f"  how often the window start changes the PICK itself: "
      f"{wf.groupby(['panel','cadence','chooser']).pick_book.nunique().gt(1).sum()} of "
      f"{wf.groupby(['panel','cadence','chooser']).ngroups} (panel, cadence, chooser) slots "
      f"take a different BOOK at some window start")

    # G6 -- the choosers are IS-only
    q = pans["U56"]
    rng = np.random.default_rng(6)
    vals = q.px.values.copy()
    oos_rows = np.flatnonzero(q.oos)
    vals[oos_rows] = vals[oos_rows][rng.permutation(len(oos_rows))]
    q2 = Panel("U56perm", pd.DataFrame(vals, index=q.idx, columns=q.px.columns))
    mismatch = 0
    for c in CADENCES:
        for w in WSTARTS:
            picks = {}
            for tag, qq in (("orig", q), ("perm", q2)):
                cand = []
                for b in BOOKS:
                    for g in GROSS_GRID:
                        ww = W[("U56", b, g)] if tag == "orig" else build_books(qq.px, g)[0][b]
                        r = qq.ctx[c].run(lag_weights(ww), PROTO_COST)[0]
                        cand.append((b, g, fmet(r[qq.iswin[w]])[1]))
                picks[tag] = max(cand, key=lambda x: (-1e9 if np.isnan(x[2]) else x[2]))[:2]
            mismatch += int(picks["orig"] != picks["perm"])
    gates["G6"] = mismatch == 0
    P(f"\n  G6  CH_SHARPE pick invariant to permuted OOS rows, U56 x 3 cadences x "
      f"{len(WSTARTS)} window starts: {mismatch} mismatches  [{'PASS' if gates['G6'] else 'FAIL'}]")

    # ------------------------------------------------------------ HYPOTHESES -----------------
    P("\n" + "-" * 100)
    P("PRE-REGISTERED HYPOTHESES")
    P("-" * 100)
    hyp = []

    d09 = bind[(bind.legset == "REC5") & (bind.wstart == WSTARTS[0]) & (bind.kind == "DESTROYED")]
    if len(d09):
        sh = float(d09.binding.str.contains("L_H1").mean())
        hyp.append(("H_H1", f"L_H1 in the binding set on {int(d09.binding.str.contains('L_H1').sum())} "
                            f"of {len(d09)} DESTROYED rows at w=2009 = {sh:.3f}", sh >= H1_BAR,
                    f">= {H1_BAR}"))
    else:
        hyp.append(("H_H1", "0 DESTROYED rows at w=2009 -- undefined", False, f">= {H1_BAR}"))

    n09 = int(cd[(cd.legset == "REC5") & (cd.wstart == WSTARTS[0])].destroyed.sum())
    n12 = int(cd[(cd.legset == "REC5") & (cd.wstart == "2012-01-01")].destroyed.sum())
    hyp.append(("H_TAPE", f"destroyed pooled over rungs: w=2009 {n09} -> w=2012 {n12} "
                          f"(ratio {n12/n09:.3f})" if n09 else
                f"destroyed w=2009 {n09} -- undefined",
                (n09 > 0 and n12 <= TAPE_BAR * n09), f"w2012 <= {TAPE_BAR} x w2009"))

    npan = 0
    for k in PANELS:
        q = pans[k]
        h1s = [q.spy_leg[WTAG[w]][0] for w in WSTARTS]
        if (np.argmax(h1s) == 0) and (h1s[0] > q.spy_leg[WTAG[WSTARTS[0]]][1]):
            npan += 1
    hyp.append(("H_SPY", f"SPY's DISJ L_H1 bar is maximal at w=2009 AND above its own L_H2 on "
                         f"{npan} of {len(PANELS)} panels", npan >= 2, ">= 2 of 3 panels"))

    nb09 = nb[(nb.legset == "REC5") & (nb.wstart == WSTARTS[0])]["bind_H1"].dropna()
    mednull = float(nb09.median()) if len(nb09) else np.nan
    hyp.append(("H_NULLH1", f"median over {len(nb09)} defined null cells of the share of destroyed "
                            f"draws binding on L_H1 = {mednull:.3f}",
                (not np.isnan(mednull)) and mednull >= NULLH1_BAR, f">= {NULLH1_BAR}"))

    counts = wfw["p4b_DISJ"].astype(int).tolist()
    hyp.append(("H_RULE8", f"OOS 4b pass counts by window start = {counts} "
                           f"(spread {max(counts)-min(counts)})",
                (max(counts) - min(counts)) >= 1, "spread >= 1"))

    for name, txt, ok, bar in hyp:
        P(f"  {name:9s} [{'PASS' if ok else 'FAIL'}]  bar {bar:24s}  {txt}")
    dump(pd.DataFrame([dict(hypothesis=n, statement=t, verdict=("PASS" if o else "FAIL"), bar=b)
                       for n, t, o, b in hyp]), "hypotheses.csv")

    P("\n  GATES: " + "  ".join(f"{k}={'PASS' if v else 'FAIL'}" for k, v in sorted(gates.items()))
      + f"   ({sum(gates.values())} of {len(gates)})")
    dump(pd.DataFrame([dict(gate=k, verdict=("PASS" if v else "FAIL")) for k, v in sorted(gates.items())]),
         "gates.csv")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"\nwrote {STEM}.console.txt")


if __name__ == "__main__":
    main()

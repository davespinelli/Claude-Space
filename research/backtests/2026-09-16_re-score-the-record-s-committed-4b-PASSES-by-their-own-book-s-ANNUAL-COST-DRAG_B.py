#!/usr/bin/env python3
"""Idea 930 (lane B, 2026-09-16) -- re-score the record's committed 4b PASSES by their own
book's ANNUAL COST DRAG.

THE CLAIM THIS RUN SCORES
  Idea 926 (lane B, 2026-09-15) published: "the null 4b base rate is a function of cost x
  realised turnover, not of the cost rung: no cell keeps a base rate above 5% past ~100 bp/yr
  of drag, and PROTOCOL's 10 bps buys 161 bp/yr on a weekly book but only 73 on a monthly one."
  If that is right, then a committed 4b PASS carried by a LOW-DRAG book is worth less than one
  carried by a high-drag book, because in the low-drag region a gross-matched coin flip clears
  the same bar often enough that the pass is not evidence.  This run recovers every committed
  4b PASS's cell, computes ITS OWN book's annual drag, and reports how many sit BELOW the line.

DRAG, DEFINED ONCE
  drag (bp/yr) = realised annual two-sided turnover  x  cost rung (bps).
  A weekly book turning over 16.1x of NAV a year pays 161 bp/yr at PROTOCOL's 10 bps.  Drag is
  MEASURED from the same turnover series `engine.backtest` charges, never assumed (gate G1).

THE TWO READINGS OF "BELOW THE LINE", BOTH PRINTED
  DIRECT     a committed pass is BELOW THE LINE iff its OWN cell's gross-matched null clears all
             five 4b legs at least `bar` of the time at 10 bps.  No model, no fit.
  DRAG-LINE  D*(bar) = the largest drag at which ANY (cell, cost rung) point still has null 4b
             base rate >= bar, fitted on the 90-cell x 5-rung surface.  A pass is BELOW THE LINE
             iff its cell's 10 bps drag < D*(bar).  This is 926's claim used as a PREDICTOR.
  H_PREDICT asks whether the drag line reproduces the direct reading cell by cell.  Drag is the
  EXPLANATORY variable; the direct reading is the measurement.

TUNED DIALS (exactly 2, per the queue; every level ALWAYS reported, none chooses anything)
  1. CLAIM SET  STRICT  claim units naming EXACTLY ONE panel and EXACTLY ONE book (cadence and
                        gross taken from the text where named exactly once, else the record's
                        canonical W / 0.75)
                WIDE    any unit naming >= 1 panel and >= 1 book, expanded to the full cross
                        product of everything it names
                STRUCT  the CONTROL -- every structurally 4b-passing cell of the reproducible
                        90-cell ladder at 10 bps, harvested from PRICES and not from TEXT
  2. DRAG LINE  bar in {0.05, 0.10, 0.25} -- the null 4b base rate above which a coin flip is
                said to "still clear the bar".  926's headline uses 0.05.

REPORTED, NEVER FITTED
  PANEL {U56, B136} x BOOK {TOP5, TOP10, TOP20, EWELIG, BAND03} x GROSS {0.50, 0.75, 1.00} x
  CADENCE {W, M, Q} = 90 cells.  COST RUNGS {0, 5, 10, 25, 50} bps are the MECHANISM AXIS that
  traces the drag curve, not a dial: 10 bps stays PROTOCOL-binding for every verdict and for
  rule 8.  Next-day execution throughout.

PRE-REGISTERED HYPOTHESES (bars fixed before any number was read)
  H_MONO     drag explains the null base rate.  PASS iff Spearman rho(drag, null 4b base rate)
             <= -0.50 over the 450 (cell, rung) points.
  H_NOTRUNG  it is drag, not the RUNG.  PASS iff |rho(drag, base)| exceeds |rho(rung, base)|
             measured on the same 450 points.
  H_WITHIN   the ordering is not a cadence LABEL.  PASS iff rho(drag, base) <= -0.30 inside
             EACH of W, M and Q separately.
  H_100      926's ~100 bp/yr line reproduces.  PASS iff D*(0.05) is in [50, 200] bp/yr.
  H_CADENCE  926's cadence arithmetic reproduces.  PASS iff the median book drag at 10 bps is
             within +/-25% of 161 bp/yr on W and of 73 bp/yr on M.
  H_BELOW    the record's committed passes sit BELOW the line.  PASS iff >= 0.50 of STRICT
             resolvable passes are BELOW under the DIRECT reading at bar 0.05.
  H_PREDICT  the drag line reproduces the direct reading.  PASS iff the two agree on >= 0.80 of
             STRICT cells at bar 0.05.
  H_CLAIM    the answer does not depend on the claim set.  PASS iff |STRICT - WIDE| <= 0.10.
  H_STRUCT   text-harvested passes behave like price-harvested ones.  PASS iff
             |STRICT - STRUCT| <= 0.10.
  H_RULE8    a chooser that prefers HIGH-drag (high-turnover) books is not worse out of sample.
             PASS iff C_ISDRAG's OOS 4b count >= C_ISSHARPE's.

RULE 8 (walk-forward, mandatory -- PROTOCOL rule 8)
  (book, gross) is chosen inside each (panel, cadence) on 2009-2016 ALONE by three IS-only
  choosers -- C_ISSHARPE (IS Sharpe), C_IS4B (IS-window 4b legs first, then IS Sharpe) and
  C_ISDRAG (highest IS realised drag, then IS Sharpe).  2017-2026 is then read ONCE.  OOS
  CAGR / Sharpe / MaxDD are reported against the RULES v2 live baseline and against SPY, and
  BOTH KEEP paths are scored on every pick.  G6 proves the choosers are IS-only by permuting
  the OOS return rows.

GATES (printed before any result number)
  G0  rebalance masks == `engine.rebalance_mask` on W/M/Q.  Bar 0 rows.
  G1  closed-form `Ctx` == `engine.backtest` on returns AND turnover at 10 AND 25 bps.
  G2  BAND03 @0.75 == `baseline.rules_v2_weights(px, 0.03, 0.75)`.  Bar 0.0 exact.
  G3  CROSS-RUN: SPY's OOS triple vs the record's committed 15.2102% / 0.8711 / -33.7173%.
  G4  GROSS MATCH: every null draw's target gross AND holding count equal the book's on every
      decision row.  Bar 0.0 on both.
  G5  DETERMINISM: a redrawn null is bit-for-bit identical (md5-derived seeds).
  G6  every rule-8 chooser is IS-ONLY: picks invariant to permuted OOS/full rows.
  G7  CROSS-RUN of the SAME 90-cell ladder's structural 4b count at 10 bps against idea 969's
      committed 10 of 90 (same tree, same books, same day).  Bar 0 disagreements.
  G8  COST LINEARITY: net(c) == gross - turnover*c/1e4 exactly, so "drag" is the quantity the
      backtester actually charges.  Bar 1e-12 over every rung.

SURVIVORSHIP (PROTOCOL rule 9)
  U56 and B136 are CURRENT-constituent lists.  Every CAGR and drawdown LEVEL is optimistic and
  every 4b count is an UPPER bound.  A coin flip drawn from a survivor panel is a BETTER book
  than one drawn in real time, so every NULL base rate here is also an UPPER bound -- which cuts
  AGAINST this run's own headline: measured live, the coin flip would clear 4b LESS often, so
  fewer committed passes would sit below the line than printed.
"""
from __future__ import annotations
import hashlib
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state          # noqa: E402
from engine import backtest, rebalance_mask                               # noqa: E402

COST, LAG, WARMUP = 10.0, 1, 260                 # PROTOCOL rule 2 binding cost
RUNGS = [0.0, 5.0, 10.0, 25.0, 50.0]             # mechanism axis, NOT a dial
MAXVOL, BAND = 0.60, 0.03
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BARS = [0.05, 0.10, 0.25]                        # dial 2 -- drag line
CLAIMSETS = ["STRICT", "WIDE", "STRUCT"]         # dial 1 -- claim set

SMOKE = os.environ.get("SMOKE", "") == "1"
DRAWS = 20 if SMOKE else 200

PANELS = ["U56", "B136"]
BOOKS = ["TOP5", "TOP10", "TOP20", "EWELIG", "BAND03"]
GROSSES = [0.50, 0.75, 1.00]
CADENCES = ["W", "M", "Q"]
LEGS = ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]
IS_LEGS = ["I_H1", "I_H2", "I_DD", "I_CAGR"]

CANON_GROSS, CANON_CADENCE = 0.75, "W"
GROSS_NAME = {"CORE": 0.75, "FULL": 1.00, "HALF": 0.50}
SPY_OOS_PUB = (0.152102, 0.8711, -0.337173)      # G3, committed by ideas 1018/1023
G3_TOL = (2e-3, 2e-2, 2e-3)
G7_LADDER_4B = 10                                # G7, committed by idea 969 (lane B) today
PUB_DRAG_W, PUB_DRAG_M = 161.0, 73.0             # 926's committed cadence drags at 10 bps

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


def head_sha() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                              capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return "unknown"


def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 3:
        return np.nan
    rx = pd.Series(x[ok]).rank().values
    ry = pd.Series(y[ok]).rank().values
    if rx.std() == 0 or ry.std() == 0:
        return np.nan
    return float(np.corrcoef(rx, ry)[0, 1])


# =================================================================================================
# runner -- returns GROSS returns and turnover; any cost rung is a linear subtraction (gate G8)
# =================================================================================================
class Ctx:
    """Closed-form equivalent of `engine.backtest`'s day loop for ONE rebalance schedule.
    Gated at G1 against `engine.backtest` on returns AND turnover at two cost rungs."""

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

    def run(self, wt):
        """-> (GROSS portfolio returns, turnover).  net(c) = gross - turnover * c / 1e4."""
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
        return port, turn


def lag_weights(W1):
    wt = np.roll(W1, LAG, axis=0).copy()
    wt[:LAG] = 0.0
    return wt


def applied_from_decision(dec):
    a = np.roll(dec, LAG)
    a[:LAG] = False
    a[0] = True
    return a


def fmet(r):
    r = np.asarray(r, float)
    if len(r) < 2:
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
        self.rets = px.pct_change().fillna(0.0).values
        self.T = len(self.idx)
        self.warm = np.arange(self.T) >= WARMUP
        self.oos_m = np.asarray(self.idx >= pd.Timestamp(OOS_START))
        self.is_m = self.warm & np.asarray(self.idx <= pd.Timestamp(IS_END))
        wpos = np.flatnonzero(self.warm)
        h = len(wpos) // 2
        self.h1 = np.zeros(self.T, bool); self.h1[wpos[:h]] = True
        self.h2 = np.zeros(self.T, bool); self.h2[wpos[h:]] = True
        ipos = np.flatnonzero(self.is_m)
        ih = len(ipos) // 2
        self.ih1 = np.zeros(self.T, bool); self.ih1[ipos[:ih]] = True
        self.ih2 = np.zeros(self.T, bool); self.ih2[ipos[ih:]] = True
        self.yrs_warm = self.warm.sum() / 252.0
        self.yrs_is = self.is_m.sum() / 252.0
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.priced = px.notna().values
        above = px > px.rolling(200).mean()
        vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        self.elig = (above & (vol20 < MAXVOL) & px.notna()).values
        self.dec = {c: rebalance_mask(self.idx, c).values.copy() for c in CADENCES}
        self.app = {c: applied_from_decision(self.dec[c]) for c in CADENCES}
        self.ctx = {c: Ctx(self.rets, self.app[c]) for c in CADENCES}
        self.spy_full = fmet(self.spy[self.warm])
        self.spy_h1 = fmet(self.spy[self.h1])[1]
        self.spy_h2 = fmet(self.spy[self.h2])[1]
        self.spy_oos = fmet(self.spy[self.oos_m])
        self.spy_is = fmet(self.spy[self.is_m])
        self.spy_ih1 = fmet(self.spy[self.ih1])[1]
        self.spy_ih2 = fmet(self.spy[self.ih2])[1]


def oos_legs(pn, r):
    """PROTOCOL 4b's five legs.  SPY is a buy-and-hold benchmark and is charged no cost."""
    c, s, dd = fmet(r[pn.warm])
    os_ = fmet(r[pn.oos_m])[1]
    sh1, sh2 = fmet(r[pn.h1])[1], fmet(r[pn.h2])[1]
    return dict(L_H1=sh1 > pn.spy_h1, L_H2=sh2 > pn.spy_h2, L_OOS=os_ > pn.spy_oos[1],
                L_DD=abs(dd) <= DD_CAP * abs(pn.spy_full[2]),
                L_CAGR=c >= CAGR_FLOOR * pn.spy_full[0]), (c, s, dd), sh1, sh2


def is_legs(pn, r):
    ic, isharpe, idd = fmet(r[pn.is_m])
    return dict(I_H1=fmet(r[pn.ih1])[1] > pn.spy_ih1, I_H2=fmet(r[pn.ih2])[1] > pn.spy_ih2,
                I_DD=abs(idd) <= DD_CAP * abs(pn.spy_is[2]),
                I_CAGR=ic >= CAGR_FLOOR * pn.spy_is[0]), (ic, isharpe, idd)


# =================================================================================================
# books -- unit-gross weight rows (gross applied by the caller)
# =================================================================================================
def book_w1(px, book, elig):
    if book == "BAND03":
        e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
        ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        return ew.where(band_state(px, BAND), 0.0).values
    if book == "EWELIG":
        E = elig.astype(float)
        k = E.sum(axis=1)
        out = np.zeros_like(E)
        nz = k > 0
        out[nz] = E[nz] / k[nz, None]
        return out
    n = int(book[3:])
    mom = (px.shift(21) / px.shift(252) - 1).rank(axis=1, pct=True)
    r6 = (px / px.shift(126) - 1).rank(axis=1, pct=True)
    r3 = (px / px.shift(63) - 1).rank(axis=1, pct=True)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = ((mom + r6 + r3) / 3) * (0.5 + 0.5 * above.astype(float))
    rank = sc.where(above & (vol20 < MAXVOL)).rank(axis=1, ascending=False)
    sel = (rank <= n).astype(float)
    k = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(k, axis=0).fillna(0.0).values


def draw_picks(buf, pn, W1, dec, rng):
    """RANDROT -- the gross-matched rotating coin flip (926's convention).  On every DECISION row
    it holds exactly as many equally weighted names as the book holds that day, at the book's own
    row sum, drawn from the names passing the BOOK'S OWN gate (gated at G4).  Where the book holds
    more names than the gate admits (BAND03 routinely does), the pool is widened with the
    remaining PRICED names so the holding count still matches exactly."""
    buf[:] = 0.0
    held = W1 > 0
    kcount = held.sum(axis=1)
    rowsum = W1.sum(axis=1)
    for i in np.flatnonzero(dec):
        k = int(kcount[i])
        if k == 0:
            continue
        pool = np.flatnonzero(pn.elig[i])
        if len(pool) < k:
            extra = np.setdiff1d(np.flatnonzero(pn.priced[i]), pool, assume_unique=False)
            if len(extra):
                pool = np.concatenate([pool, extra])
        if len(pool) == 0:
            continue
        k = min(k, len(pool))
        buf[i, rng.choice(pool, size=k, replace=False)] = rowsum[i] / k
    return buf


# =================================================================================================
# HARVEST -- the record's committed 4b PASS claims (same matcher as ideas 969 / 998)
# =================================================================================================
PAN_RX = {"U56": r"\bU56\b", "B136": r"\bB136\b", "SMALL663": r"\bSMALL(?:663|483)?\b"}
BOOK_RX = {"TOP5": r"\bTOP0?5\b", "TOP10": r"\bTOP10\b", "TOP20": r"\b(?:TOP20|CAND20)\b",
           "EWELIG": r"\bEWELIG\b", "BAND03": r"\bBAND03\b"}
CAD_RX = {"W": r"(?<![A-Za-z])W(?:EEKLY|eekly)?(?![A-Za-z])|\bweekly\b",
          "M": r"(?<![A-Za-z])M(?:ONTHLY|onthly)?(?![A-Za-z])|\bmonthly\b",
          "Q": r"(?<![A-Za-z])Q(?:UARTERLY|uarterly)?(?![A-Za-z])|\bquarterly\b"}
GROSS_RX = r"(?:gross\s*|g|@)\s*([01]\.\d{2})"
PASS_RX = re.compile(r"4b", re.I)
ASSERT_RX = re.compile(r"KEEP-candidate|\b4b\s+PASS|PASS(?:ES)?\b|\bpasses\b|\bclears?\b", re.I)


def harvest():
    lb = [l for l in (ROOT / "research" / "LEADERBOARD.md").read_text().split("\n")
          if l.startswith("|") and not l.startswith("|---")][1:]
    cl = [p for p in (ROOT / "research" / "CHANGELOG.md").read_text().split("\n\n") if p.strip()]
    units = [("LEADERBOARD", i, t) for i, t in enumerate(lb)] + \
            [("CHANGELOG", i, t) for i, t in enumerate(cl)]
    rows = []
    for src, i, t in units:
        if not (PASS_RX.search(t) and ASSERT_RX.search(t)):
            continue
        pans = sorted(k for k, v in PAN_RX.items() if re.search(v, t))
        bks = sorted(k for k, v in BOOK_RX.items() if re.search(v, t))
        cads = sorted(k for k, v in CAD_RX.items() if re.search(v, t))
        gs = sorted({float(x) for x in re.findall(GROSS_RX, t) if float(x) in GROSSES})
        for nm, gv in GROSS_NAME.items():
            if re.search(rf"\b{nm}\b", t) and gv not in gs:
                gs.append(gv)
        rows.append(dict(source=src, unit=i, n_panel=len(pans), n_book=len(bks), n_cad=len(cads),
                         n_gross=len(gs), panels="|".join(pans), books="|".join(bks),
                         cads="|".join(cads), grosses="|".join(f"{g:.2f}" for g in sorted(gs)),
                         text=t[:300].replace("\n", " ")))
    return pd.DataFrame(rows), len(units)


def resolve(cen, claimset):
    cells = []
    for _, r in cen.iterrows():
        pans = [p for p in r.panels.split("|") if p]
        bks = [b for b in r.books.split("|") if b]
        cads = [c for c in r.cads.split("|") if c]
        gs = [float(x) for x in r.grosses.split("|") if x]
        if not pans or not bks:
            continue
        if claimset == "STRICT":
            if len(pans) != 1 or len(bks) != 1:
                continue
            cads = cads if len(cads) == 1 else [CANON_CADENCE]
            gs = gs if len(gs) == 1 else [CANON_GROSS]
        else:
            cads = cads or [CANON_CADENCE]
            gs = gs or [CANON_GROSS]
        for p in pans:
            for b in bks:
                for g in gs:
                    for c in cads:
                        cells.append(dict(panel=p, book=b, gross=float(g), cadence=c,
                                          source=r.source, unit=int(r.unit)))
    return pd.DataFrame(cells)


# =================================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 930 (lane B) -- re-score the record's committed 4b PASSES by their own book's")
    P("                     ANNUAL COST DRAG  (drag bp/yr = realised annual turnover x cost bps)")
    P(f"tree {head_sha()}   draws {DRAWS}   rungs {RUNGS} bps   10 bps BINDING   smoke={SMOKE}")
    P("=" * 100)

    px = {"U56": load_universe(), "B136": load_universe(broad=True)}
    pnl = {k: Panel(k, px[k]) for k in PANELS}
    P("\nPANELS")
    for k in PANELS:
        p = pnl[k]
        P(f"  {k:5s} {p.px.shape[1]-1:4d} names + SPY   {p.idx[0].date()} -> {p.idx[-1].date()}   "
          f"OOS starts {p.idx[np.flatnonzero(p.oos_m)[0]].date()}")
        P(f"        SPY full {p.spy_full[0]:7.2%} / {p.spy_full[1]:.4f} / {p.spy_full[2]:7.2%}   "
          f"OOS {p.spy_oos[0]:7.2%} / {p.spy_oos[1]:.4f} / {p.spy_oos[2]:7.2%}   "
          f"H1 {p.spy_h1:.4f}  H2 {p.spy_h2:.4f}")

    W1 = {(p, b): book_w1(pnl[p].px, b, pnl[p].elig) for p in PANELS for b in BOOKS}

    # ------------------------------------------------------------------ GATES (before results)
    P("\n" + "-" * 100)
    P("GATES")
    P("-" * 100)
    gate = {}

    g0 = 0
    for p in PANELS:
        for c in CADENCES:
            g0 += int((pnl[p].dec[c] != rebalance_mask(pnl[p].idx, c).values).sum())
    gate["G0"] = g0 == 0
    P(f"  G0  rebalance masks == engine.rebalance_mask       : {g0} disagreeing rows   "
      f"{'PASS' if gate['G0'] else 'FAIL'}")

    g1r = g1t = g8 = 0.0
    for p in PANELS:
        for b in ("TOP20", "BAND03"):
            for c in ("W", "M"):
                Wg = W1[(p, b)] * 0.75
                fr, ft = pnl[p].ctx[c].run(lag_weights(Wg))
                for cst in (10.0, 25.0):
                    ref = backtest(pnl[p].px,
                                   pd.DataFrame(Wg, index=pnl[p].idx, columns=pnl[p].px.columns),
                                   cost_bps=cst, freq=c)
                    net = fr - ft * cst / 1e4
                    g1r = max(g1r, float(np.abs(net - ref["returns"].values).max()))
                    g1t = max(g1t, float(np.abs(ft - ref["turnover"].values).max()))
                    g8 = max(g8, float(np.abs((net + ft * cst / 1e4) - fr).max()))
    gate["G1"] = g1r < 1e-12 and g1t < 1e-12
    P(f"  G1  Ctx == engine.backtest @10 and @25 bps (r / t) : {g1r:.3e} / {g1t:.3e}   "
      f"{'PASS' if gate['G1'] else 'FAIL'}")
    gate["G8"] = g8 < 1e-12
    P(f"  G8  COST LINEARITY net(c) == gross - turn*c/1e4    : {g8:.3e}   "
      f"{'PASS' if gate['G8'] else 'FAIL'}")

    g2 = 0.0
    for p in PANELS:
        ref = rules_v2_weights(pnl[p].px, BAND, 0.75).values
        g2 = max(g2, float(np.abs(W1[(p, "BAND03")] * 0.75 - ref).max()))
    gate["G2"] = g2 == 0.0
    P(f"  G2  BAND03@0.75 == baseline.rules_v2_weights       : {g2:.3e}   "
      f"{'PASS' if gate['G2'] else 'FAIL'}")

    d3 = tuple(abs(a - b) for a, b in zip(pnl["U56"].spy_oos, SPY_OOS_PUB))
    gate["G3"] = all(d < t for d, t in zip(d3, G3_TOL))
    P(f"  G3  CROSS-RUN SPY OOS triple vs the record         : "
      f"{pnl['U56'].spy_oos[0]:.4%} / {pnl['U56'].spy_oos[1]:.4f} / {pnl['U56'].spy_oos[2]:.4%}  "
      f"vs 15.2102% / 0.8711 / -33.7173%   max|d| {max(d3):.2e}   "
      f"{'PASS' if gate['G3'] else 'FAIL'}")

    # ------------------------------------------------------------------ the ladder x rungs
    P("\n" + "-" * 100)
    P(f"THE LADDER  (90 cells x {len(RUNGS)} cost rungs = {90*len(RUNGS)} points).  "
      f"DRAG = realised annual turnover x rung.")
    P("-" * 100)
    lad = []
    for p in PANELS:
        pn = pnl[p]
        for b in BOOKS:
            for g in GROSSES:
                wt = lag_weights(W1[(p, b)] * g)
                for c in CADENCES:
                    gr, tn = pn.ctx[c].run(wt)
                    ty = float(tn[pn.warm].sum()) / pn.yrs_warm
                    ty_is = float(tn[pn.is_m].sum()) / pn.yrs_is
                    for rung in RUNGS:
                        r = gr - tn * rung / 1e4
                        lg, full, sh1, sh2 = oos_legs(pn, r)
                        oos = fmet(r[pn.oos_m])
                        row = dict(panel=p, book=b, gross=g, cadence=c, rung=rung,
                                   turn_yr=ty, turn_yr_IS=ty_is,
                                   drag_bp=ty * rung, drag_bp_IS=ty_is * rung,
                                   CAGR=full[0], Sharpe=full[1], MaxDD=full[2],
                                   SH_H1=sh1, SH_H2=sh2,
                                   OOS_CAGR=oos[0], OOS_Sharpe=oos[1], OOS_MaxDD=oos[2],
                                   **{k: bool(v) for k, v in lg.items()})
                        row["p4b"] = bool(all(lg[k] for k in LEGS))
                        if rung == COST:
                            ilg, ism = is_legs(pn, r)
                            row.update({k: bool(v) for k, v in ilg.items()})
                            row.update(IS_CAGR=ism[0], IS_Sharpe=ism[1], IS_MaxDD=ism[2],
                                       p4b_IS=bool(all(ilg[k] for k in IS_LEGS)))
                        lad.append(row)
    lad = pd.DataFrame(lad)
    L10 = lad[lad.rung == COST].reset_index(drop=True)
    n4b = int(L10.p4b.sum())
    gate["G7"] = n4b == G7_LADDER_4B
    P(f"  structural 4b PASS cells @10 bps: {n4b} of {len(L10)}")
    P(f"  G7  CROSS-RUN ladder 4b count vs idea 969's 10/90  : {n4b} vs {G7_LADDER_4B}   "
      f"{'PASS' if gate['G7'] else 'FAIL'}")
    P("\n  BOOK DRAG at 10 bps (bp/yr), median over panel x book x gross:")
    for c in CADENCES:
        s = L10[L10.cadence == c]
        P(f"    {c}  median {s.drag_bp.median():7.1f}   range {s.drag_bp.min():6.1f} .. "
          f"{s.drag_bp.max():7.1f}   (turnover {s.turn_yr.median():5.2f}x/yr)")
    P("  REPORTED reconciliation against 926's committed 161 (W) / 73 (M) bp/yr -- gross is a "
      "linear scale on turnover, so the median over a gross ladder is not the same object:")
    for c in CADENCES:
        s = L10[L10.cadence == c]
        P(f"    {c}  median drag by gross: "
          + "   ".join(f"@{g:.2f} {s[s.gross==g].drag_bp.median():7.1f}" for g in GROSSES))

    # ------------------------------------------------------------------ the nulls
    P("\n" + "-" * 100)
    P(f"THE NULLS  (RANDROT, gross-matched; {DRAWS} draws x "
      f"{len(PANELS)*len(BOOKS)*len(CADENCES)} (panel,book,cadence) families x {len(GROSSES)} "
      f"gross x {len(RUNGS)} rungs)")
    P("-" * 100)
    nullstat = []
    base4b = {}          # (p,b,g,c,rung) -> null 4b base rate
    baseleg = {}         # (p,b,g,c,rung) -> {leg: base rate}
    base_is = {}         # (p,b,g,c) -> IS 4b base rate at 10 bps
    g4_dg = g4_dk = 0.0
    g5_ok = True
    for p in PANELS:
        pn = pnl[p]
        buf = np.zeros_like(pn.rets)
        for b in BOOKS:
            Wb = W1[(p, b)]
            for c in CADENCES:
                dec = pn.dec[c]
                decidx = np.flatnonzero(dec)
                acc = {(g, rung, leg): 0 for g in GROSSES for rung in RUNGS
                       for leg in LEGS + ["4B"]}
                acc_is = {g: 0 for g in GROSSES}
                nty = {g: [] for g in GROSSES}
                sig = set()
                for d in range(DRAWS):
                    sd = seed_of(p, b, c, "RANDROT", d)
                    draw_picks(buf, pn, Wb, dec, np.random.default_rng(sd))
                    sig.add(hashlib.md5(buf[decidx].tobytes()).hexdigest())
                    if d == 0:
                        g4_dg = max(g4_dg, float(np.abs(buf[decidx].sum(axis=1)
                                                        - Wb[decidx].sum(axis=1)).max()))
                        g4_dk = max(g4_dk, float(np.abs((buf[decidx] > 0).sum(axis=1)
                                                        - (Wb[decidx] > 0).sum(axis=1)).max()))
                    for g in GROSSES:
                        gr, tn = pn.ctx[c].run(lag_weights(buf * g))
                        nty[g].append(float(tn[pn.warm].sum()) / pn.yrs_warm)
                        for rung in RUNGS:
                            r = gr - tn * rung / 1e4
                            lg, _f, _1, _2 = oos_legs(pn, r)
                            for leg in LEGS:
                                acc[(g, rung, leg)] += int(lg[leg])
                            acc[(g, rung, "4B")] += int(all(lg[k] for k in LEGS))
                            if rung == COST:
                                ilg, _i = is_legs(pn, r)
                                acc_is[g] += int(all(ilg[k] for k in IS_LEGS))
                for g in GROSSES:
                    base_is[(p, b, g, c)] = acc_is[g] / DRAWS
                    for rung in RUNGS:
                        base4b[(p, b, g, c, rung)] = acc[(g, rung, "4B")] / DRAWS
                        baseleg[(p, b, g, c, rung)] = {leg: acc[(g, rung, leg)] / DRAWS
                                                       for leg in LEGS}
                        nullstat.append(dict(panel=p, book=b, gross=g, cadence=c, rung=rung,
                                             draws=DRAWS, distinct=len(sig),
                                             degenerate=bool(len(sig) < 0.5 * DRAWS),
                                             null_turn_yr=float(np.median(nty[g])),
                                             null_drag_bp=float(np.median(nty[g])) * rung,
                                             base4b=acc[(g, rung, "4B")] / DRAWS,
                                             **{leg: acc[(g, rung, leg)] / DRAWS for leg in LEGS}))
                if b == "TOP20" and c == "M":
                    a = draw_picks(np.zeros_like(pn.rets), pn, Wb, dec,
                                   np.random.default_rng(seed_of(p, b, c, "RANDROT", 0)))
                    g5_ok &= hashlib.md5(a[decidx].tobytes()).hexdigest() in sig
        P(f"  {p}: nulls built  ({time.time()-t0:.0f}s elapsed)")
    nullstat = pd.DataFrame(nullstat)
    gate["G4"] = g4_dg < 1e-12 and g4_dk == 0
    P(f"  G4  GROSS MATCH (row sum / holding count)          : {g4_dg:.3e} / {g4_dk:.0f}   "
      f"{'PASS' if gate['G4'] else 'FAIL'}")
    gate["G5"] = g5_ok
    P(f"  G5  DETERMINISM (redrawn null identical)           : "
      f"{'PASS' if gate['G5'] else 'FAIL'}")
    P(f"  degenerate null families (< 50% distinct draws)    : "
      f"{int(nullstat.drop_duplicates(['panel','book','gross','cadence']).degenerate.sum())} of "
      f"{len(nullstat.drop_duplicates(['panel','book','gross','cadence']))}")

    # ------------------------------------------------------------------ the drag curve
    P("\n" + "=" * 100)
    P("THE DRAG CURVE  (450 (cell, rung) points; BOOK drag on the x axis, NULL 4b base rate on y)")
    P("=" * 100)
    surf = lad[["panel", "book", "gross", "cadence", "rung", "turn_yr", "drag_bp", "p4b"]].copy()
    surf["base4b"] = [base4b[(r.panel, r.book, r.gross, r.cadence, r.rung)]
                      for _, r in surf.iterrows()]
    surf = surf.merge(nullstat[["panel", "book", "gross", "cadence", "rung",
                                "null_turn_yr", "null_drag_bp", "degenerate"]],
                      on=["panel", "book", "gross", "cadence", "rung"], how="left")
    rho_drag = spearman(surf.drag_bp, surf.base4b)
    rho_rung = spearman(surf.rung, surf.base4b)
    rho_turn = spearman(surf.turn_yr, surf.base4b)
    rho_ndrag = spearman(surf.null_drag_bp, surf.base4b)
    P(f"  Spearman rho(BOOK drag, null 4b base rate) = {rho_drag:+.4f}   "
      f"rho(rung, base) = {rho_rung:+.4f}   rho(turnover, base) = {rho_turn:+.4f}")
    P(f"  Spearman rho(NULL's OWN drag, base)        = {rho_ndrag:+.4f}   "
      f"(the null churns more than the book: median null turnover "
      f"{surf.null_turn_yr.median():.2f}x/yr vs book {surf.turn_yr.median():.2f}x/yr)")
    P("\n  base rate by BOOK-drag decile:")
    surf["dec"] = pd.qcut(surf.drag_bp.rank(method="first"), 10, labels=False)
    for d, s in surf.groupby("dec"):
        P(f"    decile {int(d)+1:2d}  drag {s.drag_bp.min():7.1f} .. {s.drag_bp.max():8.1f} bp/yr"
          f"   mean base4b {s.base4b.mean():.4f}   max {s.base4b.max():.4f}   "
          f"share >= 0.05 {(s.base4b >= 0.05).mean():.3f}")
    P("\n  within-cadence rho(BOOK drag, base):")
    within = {}
    for c in CADENCES:
        s = surf[surf.cadence == c]
        within[c] = spearman(s.drag_bp, s.base4b)
        P(f"    {c}  rho {within[c]:+.4f}  ({len(s)} points)")

    P("\n  DECOMPOSITION (reported, no bar -- the rung-0 column has drag identically 0 for EVERY")
    P("  cell, so pooling it makes the x axis degenerate; and 18 of 90 null families are")
    P("  idea 998's DEGENERATE construction).  rho(., null 4b base rate) on each subset:")
    for lbl, d in [("ALL 450 points", surf),
                   ("non-degenerate nulls", surf[~surf.degenerate.astype(bool)]),
                   ("rung > 0 (drag axis non-trivial)", surf[surf.rung > 0]),
                   ("rung > 0 AND non-degenerate", surf[(surf.rung > 0) & (~surf.degenerate.astype(bool))]),
                   ("the BINDING rung only (10 bps)", surf[surf.rung == COST])]:
        P(f"    {lbl:34s} n {len(d):3d}   rho(drag) {spearman(d.drag_bp, d.base4b):+.4f}   "
          f"rho(rung) {spearman(d.rung, d.base4b):+.4f}   "
          f"rho(turnover) {spearman(d.turn_yr, d.base4b):+.4f}")

    DSTAR = {}
    P("\n  D*(bar) = largest BOOK drag at which ANY (cell, rung) point still has base4b >= bar:")
    for bar in BARS:
        hit = surf[surf.base4b >= bar]
        DSTAR[bar] = float(hit.drag_bp.max()) if len(hit) else 0.0
        nd = hit[~hit.degenerate.astype(bool)]
        P(f"    bar {bar:.2f}   D* {DSTAR[bar]:8.1f} bp/yr   "
          f"({len(hit):3d} of {len(surf)} points at or above the bar; "
          f"95th pct of their drag {np.percentile(hit.drag_bp,95) if len(hit) else 0:7.1f})"
          f"   D* on NON-DEGENERATE nulls only {(nd.drag_bp.max() if len(nd) else 0.0):7.1f}")
    P(f"    NOTE: D* is a MAX over points, so it is set by ONE cell.  The cell setting D*(0.05) "
      f"is:")
    _h = surf[surf.base4b >= 0.05]
    if len(_h):
        _c = _h.loc[_h.drag_bp.idxmax()]
        P(f"      {_c.panel} / {_c.book} @{_c.gross:.2f} / {_c.cadence} at the {_c.rung:.0f} bps "
          f"rung, base4b {_c.base4b:.3f}, degenerate={bool(_c.degenerate)}")
    P("\n  cells where a coin flip clears ALL FIVE 4b legs >= 5% of the time AT THE BINDING "
      "10 bps RUNG:")
    t10 = surf[(surf.rung == COST) & (surf.base4b >= 0.05)].sort_values("drag_bp")
    P(f"    {len(t10)} of {int((surf.rung == COST).sum())} cells")
    for _, r in t10.iterrows():
        P(f"      {r.panel:5s} {r.book:7s} @{r.gross:.2f} {r.cadence}   drag {r.drag_bp:6.1f} bp/yr"
          f"   base4b {r.base4b:.3f}   degenerate={bool(r.degenerate)}")

    # ------------------------------------------------------------------ harvest + score
    P("\n" + "=" * 100)
    P("THE RECORD'S COMMITTED 4b PASSES, RE-SCORED BY THEIR OWN BOOK'S DRAG")
    P("=" * 100)
    cen, n_units = harvest()
    P(f"  claim units scanned {n_units:,}   units asserting a 4b pass {len(cen):,}   "
      f"naming >=1 panel AND >=1 book {int(((cen.n_panel>0)&(cen.n_book>0)).sum()):,}")
    unres = int((cen.panels.str.contains("SMALL663")).sum())
    P(f"  units naming SMALL663 (not priced here, counted unresolvable): {unres}")

    L10i = L10.set_index(["panel", "book", "gross", "cadence"])
    ans, cellrows = [], []
    sets = {}
    for cs in CLAIMSETS:
        if cs == "STRUCT":
            u = L10[L10.p4b][["panel", "book", "gross", "cadence"]].drop_duplicates()
            n_claimcells = len(u)
        else:
            cc = resolve(cen, cs)
            cc = cc[cc.panel.isin(PANELS)]
            n_claimcells = len(cc)
            u = cc[["panel", "book", "gross", "cadence"]].drop_duplicates()
        sets[cs] = u
        rows = []
        for _, r in u.iterrows():
            key = (r.panel, r.book, r.gross, r.cadence)
            drag = float(L10i.loc[key, "drag_bp"])
            d = dict(claimset=cs, panel=r.panel, book=r.book, gross=r.gross, cadence=r.cadence,
                     turn_yr=float(L10i.loc[key, "turn_yr"]), drag_bp=drag,
                     p4b_here=bool(L10i.loc[key, "p4b"]),
                     base4b_10bp=base4b[(r.panel, r.book, r.gross, r.cadence, COST)])
            for bar in BARS:
                d[f"direct_{bar}"] = bool(d["base4b_10bp"] >= bar)
                d[f"dragline_{bar}"] = bool(drag < DSTAR[bar])
            rows.append(d)
        rows = pd.DataFrame(rows)
        cellrows.append(rows)
        row = dict(claimset=cs, n_claimcells=n_claimcells, n_cells=len(rows),
                   median_drag_bp=float(rows.drag_bp.median()),
                   p4b_here=float(rows.p4b_here.mean()) if len(rows) else np.nan)
        for bar in BARS:
            row[f"below_direct_{bar}"] = float(rows[f"direct_{bar}"].mean()) if len(rows) else np.nan
            row[f"below_dragline_{bar}"] = float(rows[f"dragline_{bar}"].mean()) if len(rows) else np.nan
            row[f"agree_{bar}"] = float((rows[f"direct_{bar}"] == rows[f"dragline_{bar}"]).mean()) \
                if len(rows) else np.nan
        ans.append(row)
        P(f"\n  {cs}  ({n_claimcells:,} claim-cells -> {len(rows)} distinct cells)   "
          f"median book drag {row['median_drag_bp']:.1f} bp/yr   "
          f"structurally 4b here {row['p4b_here']:.3f}")
        for bar in BARS:
            P(f"    bar {bar:.2f}   BELOW THE LINE  direct {row[f'below_direct_{bar}']:.3f}   "
              f"drag-line {row[f'below_dragline_{bar}']:.3f}   agreement "
              f"{row[f'agree_{bar}']:.3f}")
    ans = pd.DataFrame(ans)
    cellrows = pd.concat(cellrows, ignore_index=True)

    # ------------------------------------------------------------------ hypotheses
    P("\n" + "-" * 100)
    P("PRE-REGISTERED HYPOTHESES")
    P("-" * 100)
    A = ans.set_index("claimset")
    H = {}
    H["H_MONO"] = bool(rho_drag <= -0.50)
    P(f"  H_MONO     rho(drag, base4b) <= -0.50         : {rho_drag:+.4f}   "
      f"{'PASS' if H['H_MONO'] else 'FAIL'}")
    H["H_NOTRUNG"] = bool(abs(rho_drag) > abs(rho_rung))
    P(f"  H_NOTRUNG  |rho(drag)| > |rho(rung)|          : {abs(rho_drag):.4f} vs "
      f"{abs(rho_rung):.4f}   {'PASS' if H['H_NOTRUNG'] else 'FAIL'}")
    H["H_WITHIN"] = bool(all(within[c] <= -0.30 for c in CADENCES))
    P(f"  H_WITHIN   rho <= -0.30 inside EACH cadence   : "
      + "  ".join(f"{c} {within[c]:+.3f}" for c in CADENCES)
      + f"   {'PASS' if H['H_WITHIN'] else 'FAIL'}")
    H["H_100"] = bool(50.0 <= DSTAR[0.05] <= 200.0)
    P(f"  H_100      D*(0.05) in [50, 200] bp/yr        : {DSTAR[0.05]:.1f}   "
      f"{'PASS' if H['H_100'] else 'FAIL'}")
    mw = float(L10[L10.cadence == "W"].drag_bp.median())
    mm = float(L10[L10.cadence == "M"].drag_bp.median())
    H["H_CADENCE"] = bool(abs(mw - PUB_DRAG_W) <= 0.25 * PUB_DRAG_W and
                          abs(mm - PUB_DRAG_M) <= 0.25 * PUB_DRAG_M)
    P(f"  H_CADENCE  W/M median drag within 25% of 161/73: {mw:.1f} / {mm:.1f}   "
      f"{'PASS' if H['H_CADENCE'] else 'FAIL'}")
    H["H_BELOW"] = bool(A.loc["STRICT", "below_direct_0.05"] >= 0.50)
    P(f"  H_BELOW    STRICT below (direct, 0.05) >= 0.50: "
      f"{A.loc['STRICT','below_direct_0.05']:.3f}   {'PASS' if H['H_BELOW'] else 'FAIL'}")
    H["H_PREDICT"] = bool(A.loc["STRICT", "agree_0.05"] >= 0.80)
    P(f"  H_PREDICT  direct vs drag-line agree >= 0.80  : {A.loc['STRICT','agree_0.05']:.3f}   "
      f"{'PASS' if H['H_PREDICT'] else 'FAIL'}")
    dc = abs(A.loc["STRICT", "below_direct_0.05"] - A.loc["WIDE", "below_direct_0.05"])
    H["H_CLAIM"] = bool(dc <= 0.10)
    P(f"  H_CLAIM    |STRICT - WIDE| <= 0.10            : {dc:.3f}   "
      f"{'PASS' if H['H_CLAIM'] else 'FAIL'}")
    ds = abs(A.loc["STRICT", "below_direct_0.05"] - A.loc["STRUCT", "below_direct_0.05"])
    H["H_STRUCT"] = bool(ds <= 0.10)
    P(f"  H_STRUCT   |STRICT - STRUCT| <= 0.10          : {ds:.3f}   "
      f"{'PASS' if H['H_STRUCT'] else 'FAIL'}")

    # ------------------------------------------------------------------ RULE 8
    P("\n" + "=" * 100)
    P("RULE 8 -- WALK-FORWARD (picks on 2009-2016 ALONE; 2017-2026 read ONCE; 10 bps binding)")
    P("=" * 100)

    def pick(p, c, chooser, ladder):
        cands = [(b, g) for b in BOOKS for g in GROSSES]

        def key(bg):
            b, g = bg
            r = ladder.loc[(p, b, g, c)]
            if chooser == "C_ISSHARPE":
                return (r.IS_Sharpe,)
            if chooser == "C_IS4B":
                return (int(r.p4b_IS), r.IS_Sharpe)
            return (r.drag_bp_IS, r.IS_Sharpe)             # C_ISDRAG -- highest IS drag
        return max(cands, key=key)

    CHOOSERS = ["C_ISSHARPE", "C_IS4B", "C_ISDRAG"]
    rng6 = np.random.default_rng(seed_of("G6"))
    lad_perm = L10.copy()
    for col in ("OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "CAGR", "Sharpe", "MaxDD",
                "SH_H1", "SH_H2"):
        lad_perm[col] = rng6.permutation(lad_perm[col].values)
    lk = L10i
    lk_perm = lad_perm.set_index(["panel", "book", "gross", "cadence"])
    g6 = all(pick(p, c, ch, lk) == pick(p, c, ch, lk_perm)
             for p in PANELS for c in CADENCES for ch in CHOOSERS)
    gate["G6"] = g6
    P(f"  G6  choosers are IS-ONLY (picks invariant to permuted OOS/full rows): "
      f"{'PASS' if g6 else 'FAIL'}")

    wf = []
    for p in PANELS:
        pn = pnl[p]
        bw = rules_v2_weights(pn.px, BAND, 0.75).values
        grb, tnb = pn.ctx["W"].run(lag_weights(bw))
        rb = grb - tnb * COST / 1e4
        b_oos = fmet(rb[pn.oos_m]); b_full = fmet(rb[pn.warm])
        b_h1, b_h2 = fmet(rb[pn.h1])[1], fmet(rb[pn.h2])[1]
        b_drag = float(tnb[pn.warm].sum()) / pn.yrs_warm * COST
        for c in CADENCES:
            for ch in CHOOSERS:
                b, g = pick(p, c, ch, lk)
                r = lk.loc[(p, b, g, c)]
                keep4b = bool(all(r[k] for k in LEGS))
                keep4a = bool(r.SH_H1 > b_h1 and r.SH_H2 > b_h2 and r.MaxDD >= b_full[2])
                wf.append(dict(panel=p, cadence=c, chooser=ch, pick=f"{b}@{g:.2f}",
                               drag_bp=float(r.drag_bp), drag_bp_IS=float(r.drag_bp_IS),
                               base4b_10bp=base4b[(p, b, g, c, COST)],
                               below_direct=bool(base4b[(p, b, g, c, COST)] >= 0.05),
                               OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                               SPY_OOS_CAGR=pn.spy_oos[0], SPY_OOS_Sharpe=pn.spy_oos[1],
                               SPY_OOS_MaxDD=pn.spy_oos[2], BASE_OOS_CAGR=b_oos[0],
                               BASE_OOS_Sharpe=b_oos[1], BASE_OOS_MaxDD=b_oos[2],
                               BASE_drag_bp=b_drag, keep4b=keep4b, keep4a=keep4a))
    wf = pd.DataFrame(wf)
    P("\n  panel cad  chooser      pick          drag   OOS CAGR / Sharpe / MaxDD        "
      "baseline OOS               SPY OOS                 4b 4a null4b")
    for _, r in wf.iterrows():
        P(f"  {r.panel:5s} {r.cadence:3s}  {r.chooser:11s}  {r['pick']:12s} {r.drag_bp:6.0f}  "
          f"{r.OOS_CAGR:7.2%} / {r.OOS_Sharpe:6.3f} / {r.OOS_MaxDD:7.2%}   "
          f"{r.BASE_OOS_CAGR:6.2%} / {r.BASE_OOS_Sharpe:5.3f} / {r.BASE_OOS_MaxDD:7.2%}   "
          f"{r.SPY_OOS_CAGR:6.2%} / {r.SPY_OOS_Sharpe:5.3f} / {r.SPY_OOS_MaxDD:7.2%}   "
          f"{'Y' if r.keep4b else 'n'}  {'Y' if r.keep4a else 'n'}  {r.base4b_10bp:.3f}")
    P(f"\n  OOS 4b PASS: {int(wf.keep4b.sum())} of {len(wf)}    OOS 4a PASS: "
      f"{int(wf.keep4a.sum())} of {len(wf)}")
    for ch in CHOOSERS:
        s = wf[wf.chooser == ch]
        P(f"    {ch:11s} 4b {int(s.keep4b.sum())}/{len(s)}   4a {int(s.keep4a.sum())}/{len(s)}   "
          f"mean OOS Sharpe {s.OOS_Sharpe.mean():.3f}   mean drag {s.drag_bp.mean():6.0f} bp/yr   "
          f"picks below the line {int(s.below_direct.sum())}/{len(s)}")
    H["H_RULE8"] = int(wf[wf.chooser == "C_ISDRAG"].keep4b.sum()) >= \
                   int(wf[wf.chooser == "C_ISSHARPE"].keep4b.sum())
    P(f"  H_RULE8    C_ISDRAG OOS 4b >= C_ISSHARPE's    : "
      f"{int(wf[wf.chooser=='C_ISDRAG'].keep4b.sum())} vs "
      f"{int(wf[wf.chooser=='C_ISSHARPE'].keep4b.sum())}   "
      f"{'PASS' if H['H_RULE8'] else 'FAIL'}")

    # full-sample ladder KEEP counts (both paths), reported
    P("\n  FULL-SAMPLE ladder @10 bps, BOTH KEEP paths over all 90 cells:")
    tot4a = 0
    for p in PANELS:
        pn = pnl[p]
        bw = rules_v2_weights(pn.px, BAND, 0.75).values
        grb, tnb = pn.ctx["W"].run(lag_weights(bw))
        rb = grb - tnb * COST / 1e4
        b_full = fmet(rb[pn.warm]); b_h1, b_h2 = fmet(rb[pn.h1])[1], fmet(rb[pn.h2])[1]
        s = L10[L10.panel == p]
        tot4a += int(((s.SH_H1 > b_h1) & (s.SH_H2 > b_h2) & (s.MaxDD >= b_full[2])).sum())
        P(f"    {p}  RULES v2 (live) full {b_full[0]:.2%} / {b_full[1]:.4f} / {b_full[2]:.2%}   "
          f"halves {b_h1:.3f} / {b_h2:.3f}   drag {float(tnb[pn.warm].sum())/pn.yrs_warm*COST:.0f} bp/yr")
    P(f"    4b {n4b} of {len(L10)}    4a {tot4a} of {len(L10)}")

    # ------------------------------------------------------------------ verdict
    P("\n" + "=" * 100)
    P(f"GATES {sum(gate.values())} of {len(gate)} PASS   "
      + "  ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in sorted(gate.items())))
    P(f"HYPOTHESES {sum(H.values())} of {len(H)} PASS   "
      + "  ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in H.items()))
    P("=" * 100)

    dump(lad, "ladder.csv"); dump(nullstat, "nulls.csv"); dump(surf, "dragcurve.csv")
    dump(cellrows, "cells.csv"); dump(cen, "census.csv"); dump(ans, "answer.csv")
    dump(wf, "walkforward.csv")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    P(f"\nelapsed {time.time()-t0:.0f}s")
    return dict(lad=lad, ans=ans, wf=wf, gate=gate, H=H, surf=surf, DSTAR=DSTAR)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Idea 998 (cloud lane, 2026-09-16) -- re-score the record's COMMITTED 4b PASSES against
their own PER-LEG NULL PERCENTILES.

THE PRIOR RESULT (idea 975-TRANCHE)
  A 4b pass can have a null 4b base rate of 0.000 and STILL sit at the 0.090 percentile of that
  same null on OOS Sharpe and 0.000 on OOS CAGR.  The two numbers are not in conflict: the base
  rate goes to zero as soon as ONE leg is unpassable in a cell, so "the coin flip never passes"
  can be true while "the coin flip out-earns this book" is ALSO true.  A base rate is therefore
  not a certification, and the record has been quoting it as one.

WHAT THIS RUN DOES
  1. HARVESTS every committed claim in LEADERBOARD.md and CHANGELOG.md that ASSERTS a 4b PASS
     and names a panel and a book.
  2. RESOLVES each to a reproducible cell (panel, book, gross, cadence) at PROTOCOL's 10 bps.
  3. Rebuilds THAT cell's gross-matched rotating null (`RANDROT`, the record's own construction,
     200 draws, md5 seeds) and reads, per cell: the null's PER-LEG base rates, the null's 4b base
     rate, and the BOOK's percentile inside its own null on four statistics.
  4. Reports how many committed passes sit BELOW their own null's median -- the question asked.

TUNED DIALS (exactly 2; every level ALWAYS reported, none is ever used to choose anything)
  1. CLAIM SET   STRICT  claim units naming EXACTLY ONE panel and EXACTLY ONE book (gross and
                         cadence taken from the text where named, else the record's canonical
                         CORE=0.75 / W);
                 WIDE    any unit naming >= 1 panel and >= 1 book, expanded to the full cross
                         product of everything it names;
                 STRUCT  the CONTROL -- every structurally 4b-passing cell of the reproducible
                         900-row ladder at 10 bps, harvested from PRICES and not from TEXT.
  2. STATISTIC   OOS_Sharpe (the question's own), Sharpe, CAGR, MaxDD -- the book's percentile
                 inside its own cell's null, all four published for every claim set.

REPORTED, NEVER FITTED
  PANEL {U56, B136, SMALL663}, BOOK {TOP5, TOP10, TOP20, EWELIG, BAND03}, GROSS {0.50, 0.65,
  0.75, 1.00}, CADENCE {W, M, Q}, COST {0, 5, 10, 25, 50} bps with 10 BINDING (PROTOCOL rule 2).
  These are idea 970/971's committed ladders, fixed before any number here was read.

PRE-REGISTERED HYPOTHESES (bars fixed before any number was read)
  H_MEDIAN  a committed 4b pass beats the coin flip it is quoted against.  PASS iff >= 0.50 of
            STRICT resolvable passes sit AT OR ABOVE their own null's median OOS Sharpe.
  H_ZERO    a null 4b base rate of 0.000 certifies the book.  PASS iff, over cells whose null 4b
            base rate is 0.000, the MEDIAN book percentile on OOS Sharpe is >= 50.
  H_ONELEG  a zero base rate is carried by ONE unpassable leg.  PASS iff in >= 0.50 of the
            zero-base-rate cells exactly one leg has a null pass rate < 0.05.
  H_CLAIM   the answer does not depend on the claim set.  PASS iff the share-above-median on
            OOS Sharpe differs by <= 0.10 between STRICT and WIDE.
  H_STAT    the answer does not depend on the statistic.  PASS iff all four statistics put the
            STRICT share-above-median on the SAME side of 0.50.
  H_REPRO   the harvested passes are passes on this tree.  PASS iff >= 0.50 of resolvable STRICT
            cells pass 4b structurally here at 10 bps.
  H_DEGEN   the answer does not rest on cells whose null is degenerate.  PASS iff dropping every
            cell with fewer than 50% distinct draws moves the STRICT share-below-median on OOS
            Sharpe by <= 0.10.  (Degeneracy is a CONSTRUCTION DEFECT this run found, not a dial:
            a holding-count-matched rotating draw has nothing to choose when the book already
            holds the whole eligible pool, so on `EWELIG` the null IS the book.)
  H_RULE8   an IS-only PERCENTILE chooser certifies at least as often out of sample as an
            IS-only LEVEL chooser.  PASS iff C_ISPCT's OOS 4b count >= C_ISSHARPE's.

RULE 8 (walk-forward, mandatory -- PROTOCOL rule 8)
  (book, gross) is chosen inside each (panel, cadence) on 2009-2016 ALONE by three IS-only
  choosers -- C_IS4B (IS 4b passers first, then IS Sharpe), C_ISSHARPE (IS Sharpe), C_ISPCT (the
  highest IS percentile inside its OWN cell's null on IS Sharpe, i.e. this idea's statistic used
  as a selector).  2017-2026 is then read ONCE.  OOS CAGR / Sharpe / MaxDD are reported against
  the RULES v2 live baseline and against SPY, and BOTH KEEP paths are scored on every pick.
  G6 proves the choosers are IS-only by permuting the OOS return rows.

GATES
  G0  rebalance masks == `engine.rebalance_mask` on W/M/Q.  Bar 0 rows.
  G1  closed-form runner == `engine.backtest` on returns AND turnover @10 bps.  Bar 1e-12.
  G2  BAND03 @0.75 weights == `baseline.rules_v2_weights(px, 0.03, 0.75)`.  Bar 0.0 exact.
  G3  CROSS-RUN: this run's 900-row ladder vs idea 971's committed `.grid.csv` (CAGR, Sharpe,
      MaxDD, OOS_Sharpe, REC_H1, REC_H2).  Bar 1e-09, REPORTED per panel and never tuned away:
      `data/prices.csv` is restated nightly (idea 971's own G3 defect), so U56 may miss.
  G3b CROSS-RUN of the VERDICT column: this run's REC 4b pass flag vs 971's `p4b_REC_REC5`.
      Bar 0 disagreements.
  G4  GROSS MATCH: every null draw's target gross and holding count equal the book's on every
      decision row (bar 0.0), and realised annual turnover > 0.5x the book's.
  G5  determinism: a redrawn null is bit-for-bit identical.
  G6  every rule-8 chooser is IS-ONLY: picks invariant to permuted OOS return rows.
  G7  PERCENTILE CALIBRATION: scoring a DRAW against the remaining draws of its own null gives a
      median percentile inside [45, 55] -- the estimator this run's whole answer rests on is
      unbiased under the null by construction.  THIS GATE FAILED ON THE FIRST CUT (median 35.68,
      3,925 self-scored draws) and the failure is the degenerate-null defect above: under a
      strict `>` every tied draw scores 0.  The estimator was corrected to MID-RANK (ties count
      half), which is the standard unbiased convention, and the degenerate cells are censused
      and the whole answer re-read without them.  The correction was made because the gate
      failed, not because the answer moved.

SURVIVORSHIP (PROTOCOL rule 9)
  U56 / B136 / SMALL663 are CURRENT-constituent lists (SMALL663 additionally drops the 52
  tickers with `max_1d_move` >= 1.0 per `data/small_meta.csv`).  Every CAGR and drawdown LEVEL
  and every 4b count here is optimistic, most severely on SMALL663.  The measured object is a
  PERCENTILE of a book inside a null drawn from the SAME surviving panel on the SAME tape, so the
  bias lifts book and null together and largely cancels in the percentile; the rule-8 LEVELS and
  the null base rates are NOT protected and are UPPER bounds.

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
CANON_GROSS, CANON_CADENCE = 0.75, "W"
GROSS_NAME = {"CORE": 0.75, "EXT": 1.00}

LEGS = ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")
STATS = ["OOS_Sharpe", "Sharpe", "CAGR", "MaxDD"]
CLAIMSETS = ["STRICT", "WIDE", "STRUCT"]

DRAWS = 200
SEED0 = 998
ZERO_LEG_BAR = 0.05          # H_ONELEG: "unpassable" leg
DEGEN_BAR = 0.50             # a null with < 50% distinct draws is DEGENERATE (censused, G7)
MEDIAN_BAR = 0.50            # H_MEDIAN / H_REPRO
CLAIM_BAR = 0.10             # H_CLAIM

PRIOR_GRID = OUT / "2026-09-16_is-the-2009-2012-HALF-the-leg-that-kills-every-DISJOINT-4b-pass_B.grid.csv"
G3_BAR = 1e-9

SMOKE = bool(int(os.environ.get("IDEA998_SMOKE", "0")))
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
    """The book's percentile INSIDE its own null: the share of draws it beats, x100, on the
    MID-RANK convention (ties count half).  Higher is better for Sharpe / CAGR / OOS_Sharpe;
    for MaxDD 'beats' = shallower.

    The mid-rank is not a taste: the strict-`>` version FAILED G7 at a median of 35.68 on
    3,925 self-scored draws, because 36 of this run's 157 cells have a DEGENERATE null --
    `EWELIG` holds every eligible name, so a holding-count-matched draw has nothing left to
    choose and all 200 draws are IDENTICAL.  Under strict `>` every tied draw scores 0 and the
    estimator the whole answer rests on is biased DOWN.  Mid-rank restores the calibration
    (G7 median 50.00) and the degenerate cells are censused and reported separately."""
    d = np.asarray(draw_vals, float)
    d = d[np.isfinite(d)]
    if len(d) == 0 or not np.isfinite(book_val):
        return np.nan
    if stat == "MaxDD":
        b, dd = abs(book_val), np.abs(d)
        return 100.0 * float(np.mean(b < dd) + 0.5 * np.mean(b == dd))
    return 100.0 * float(np.mean(book_val > d) + 0.5 * np.mean(book_val == d))


# =================================================================================================
# HARVEST -- the record's committed 4b PASS claims
# =================================================================================================
PAN_RX = {"U56": r"\bU56\b", "B136": r"\bB136\b", "SMALL663": r"\bSMALL(?:663|483)?\b"}
BOOK_RX = {"TOP5": r"\bTOP0?5\b", "TOP10": r"\bTOP10\b", "TOP20": r"\bTOP20\b",
           "EWELIG": r"\bEWELIG\b", "BAND03": r"\bBAND03\b"}
CAD_RX = {"W": r"(?<![A-Za-z])W(?:EEKLY|eekly)?(?![A-Za-z])|\bweekly\b",
          "M": r"(?<![A-Za-z])M(?:ONTHLY|onthly)?(?![A-Za-z])|\bmonthly\b",
          "Q": r"(?<![A-Za-z])Q(?:UARTERLY|uarterly)?(?![A-Za-z])|\bquarterly\b"}
GROSS_RX = r"(?:gross\s*|g|@)\s*([01]\.\d{2})"
PASS_RX = re.compile(r"4b", re.I)
ASSERT_RX = re.compile(r"KEEP-candidate|\b4b\s+PASS|PASS(?:ES)?\b|\bpasses\b|\bclears?\b", re.I)


def harvest():
    """Claim units = LEADERBOARD table rows + CHANGELOG paragraphs. Returns the raw census."""
    lb = [l for l in (ROOT / "research" / "LEADERBOARD.md").read_text().split("\n")
          if l.startswith("|") and not l.startswith("|---")]
    lb = lb[1:]                                              # drop the header row
    cl = [p for p in (ROOT / "research" / "CHANGELOG.md").read_text().split("\n\n") if p.strip()]
    units = [("LEADERBOARD", i, t) for i, t in enumerate(lb)] + \
            [("CHANGELOG", i, t) for i, t in enumerate(cl)]
    rows = []
    for src, i, t in units:
        if not (PASS_RX.search(t) and ASSERT_RX.search(t)):
            continue
        pans = [k for k, v in PAN_RX.items() if re.search(v, t)]
        bks = [k for k, v in BOOK_RX.items() if re.search(v, t)]
        cads = [k for k, v in CAD_RX.items() if re.search(v, t)]
        gs = sorted({float(x) for x in re.findall(GROSS_RX, t) if float(x) in GROSS_GRID})
        for nm, gv in GROSS_NAME.items():
            if re.search(rf"\b{nm}\b", t) and gv not in gs:
                gs.append(gv)
        rows.append(dict(source=src, unit=i, n_panel=len(pans), n_book=len(bks),
                         n_cad=len(cads), n_gross=len(gs),
                         panels="|".join(sorted(pans)), books="|".join(sorted(bks)),
                         cads="|".join(sorted(cads)), grosses="|".join(f"{g:.2f}" for g in sorted(gs)),
                         text=t[:400].replace("\n", " ")))
    return pd.DataFrame(rows), len(units)


def resolve(cen, claimset):
    """Claim units -> (panel, book, gross, cadence) cells under one claim-set rule."""
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
        else:                                                # WIDE: expand everything named
            cads = cads or [CANON_CADENCE]
            gs = gs or [CANON_GROSS]
        for p in pans:
            for b in bks:
                for g in gs:
                    for c in cads:
                        cells.append((p, b, float(g), c, r.source, int(r.unit)))
    return cells


# =================================================================================================
def main():
    P("=" * 100)
    P("IDEA 998 (cloud) -- re-score the record's COMMITTED 4b PASSES against their own")
    P("                   PER-LEG NULL PERCENTILES")
    P(f"tree {head_sha()}   draws {DRAWS}   costs {COSTS} (10 bps binding)   smoke={SMOKE}")
    P("=" * 100)

    # ---------------------------------------------------------------- panels
    px = {"U56": load_universe(), "B136": load_universe(broad=True)}
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    px["SMALL663"] = sm[[c for c in sm.columns if c == "SPY" or c not in bad]]
    P(f"\nPANELS  (SMALL663 screen: {len(sm.columns) - px['SMALL663'].shape[1]} tickers with "
      f"max_1d_move >= 1.0 dropped)")
    pnl = {}
    for k in PANELS:
        pnl[k] = Panel(k, px[k])
        p = pnl[k]
        P(f"  {k:9s} {p.px.shape[1]-1:4d} names + SPY   {p.idx[0].date()} -> {p.idx[-1].date()}   "
          f"SPY full {p.spy_full[0]:7.2%} / {p.spy_full[1]:.4f} / {p.spy_full[2]:7.2%}   "
          f"SPY OOS {p.spy_oos[0]:7.2%} / {p.spy_oos[1]:.4f} / {p.spy_oos[2]:7.2%}")

    # ---------------------------------------------------------------- the ladder
    P("\n" + "-" * 100)
    P("THE REPRODUCIBLE LADDER  (3 panels x 5 books x 4 gross x 3 cadences x 5 cost rungs)")
    P("-" * 100)
    lad, NET, TURN = [], {}, {}
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
                                   turnover=t_[pn.warm].sum() / pn.years, **st)
                        row.update({k: v for k, v in lg.items()})
                        row["pass4b"] = all(lg.values())
                        row["pass4a"] = pass_4a(pn, r, pn.base_r[cst])
                        row["IS_pass4b"] = all(lgi.values())
                        lad.append(row)
                        if cst == PROTO_COST:
                            NET[(pk, bk, g, cad)] = r
                            TURN[(pk, bk, g, cad)] = t_
    LAD = pd.DataFrame(lad)
    P(f"  {len(LAD):,} rows.  4b PASS at 10 bps: {int(LAD.loc[LAD.cost == PROTO_COST, 'pass4b'].sum())} "
      f"of {int((LAD.cost == PROTO_COST).sum())}   4a PASS: "
      f"{int(LAD.loc[LAD.cost == PROTO_COST, 'pass4a'].sum())}")
    dump(LAD, "ladder.csv")

    # ---------------------------------------------------------------- harvest
    P("\n" + "-" * 100)
    P("THE HARVEST  (LEADERBOARD.md rows + CHANGELOG.md paragraphs asserting a 4b PASS)")
    P("-" * 100)
    CEN, n_units = harvest()
    P(f"  {n_units:,} claim units scanned; {len(CEN):,} assert a 4b PASS")
    P(f"  naming a panel: {int((CEN.n_panel > 0).sum()):,}   naming a book: {int((CEN.n_book > 0).sum()):,}"
      f"   naming BOTH: {int(((CEN.n_panel > 0) & (CEN.n_book > 0)).sum()):,}")
    P(f"  of those, naming a CADENCE: {int(((CEN.n_panel > 0) & (CEN.n_book > 0) & (CEN.n_cad == 1)).sum()):,}"
      f"   naming a GROSS: {int(((CEN.n_panel > 0) & (CEN.n_book > 0) & (CEN.n_gross == 1)).sum()):,}")
    P(f"  UNRESOLVABLE (no panel or no book named): "
      f"{int(len(CEN) - ((CEN.n_panel > 0) & (CEN.n_book > 0)).sum()):,} "
      f"({(len(CEN) - ((CEN.n_panel > 0) & (CEN.n_book > 0)).sum()) / max(len(CEN), 1):.1%} of asserted passes)")
    dump(CEN, "census.csv")

    claim_cells = {}
    for cs in ("STRICT", "WIDE"):
        cells = resolve(CEN, cs)
        claim_cells[cs] = cells
        uniq = sorted({c[:4] for c in cells})
        P(f"  {cs:7s}: {len(cells):,} claim->cell resolutions over {len(uniq)} DISTINCT cells")
    struct = sorted({(r.panel, r.book, r.gross, r.cadence)
                     for _, r in LAD[(LAD.cost == PROTO_COST) & LAD.pass4b].iterrows()})
    claim_cells["STRUCT"] = [(a, b, c, d, "STRUCT", -1) for (a, b, c, d) in struct]
    P(f"  STRUCT : {len(struct)} structurally 4b-passing cells of the ladder at 10 bps (the CONTROL)")

    need = sorted({c[:4] for cs in CLAIMSETS for c in claim_cells[cs]})
    P(f"\n  NULLS TO BUILD: {len(need)} distinct cells x {DRAWS} draws = {len(need) * DRAWS:,} backtests")

    # ---------------------------------------------------------------- nulls
    P("\n" + "-" * 100)
    P("THE NULLS  (`RANDROT` gross-matched rotating coin flip, md5 seeds, 200 draws per cell)")
    P("-" * 100)
    NULL, DRAWROWS = {}, []
    G4 = G4_ROWS
    for n_i, (pk, bk, g, cad) in enumerate(need):
        pn = pnl[pk]
        W = lag_weights(pn.books[g][bk])
        dec = pn.dec[cad]
        buf = np.zeros_like(W)
        rng_master = np.random.default_rng(seed_of(SEED0, pk, bk, g, cad))
        recs = []
        for d in range(DRAWS):
            rng = np.random.default_rng(seed_of(SEED0, pk, bk, g, cad, d))
            Wn = draw_null(buf, pn, pn.books[g][bk], dec, rng).copy()
            if d == 0:                                       # G4 gross match on DECISION rows
                dm = np.flatnonzero(dec)
                G4.append(dict(cell=f"{pk}/{bk}/{g:.2f}/{cad}",
                               dgross=float(np.abs(Wn[dm].sum(1) - pn.books[g][bk][dm].sum(1)).max()),
                               dk=int(np.abs((Wn[dm] > 0).sum(1) - (pn.books[g][bk][dm] > 0).sum(1)).max())))
            r_, t_ = pn.ctx[cad].run(lag_weights(Wn), 0.0)
            r = r_ - t_ * PROTO_COST / 1e4
            st = stats_of(pn, r)
            lg = legs_4b(pn, st)
            recs.append(dict(draw=d, turnover=t_[pn.warm].sum() / pn.years, **st,
                             **lg, pass4b=all(lg.values())))
        nd = pd.DataFrame(recs)
        NULL[(pk, bk, g, cad)] = nd
        nd2 = nd.copy(); nd2["panel"], nd2["book"], nd2["gross"], nd2["cadence"] = pk, bk, g, cad
        DRAWROWS.append(nd2)
        if (n_i + 1) % 10 == 0 or n_i == len(need) - 1:
            P(f"  {n_i + 1:3d}/{len(need)} cells built")
    ND = pd.concat(DRAWROWS, ignore_index=True)
    dump(ND[["panel", "book", "gross", "cadence", "draw", "CAGR", "Sharpe", "MaxDD",
             "OOS_Sharpe", "H1", "H2", "turnover", "pass4b"]], "null_draws.csv")

    # ---------------------------------------------------------------- per-cell scoring
    P("\n" + "-" * 100)
    P("PER-CELL SCORING  (null per-leg base rates; the book's percentile inside its own null)")
    P("-" * 100)
    lad10 = LAD[LAD.cost == PROTO_COST].set_index(["panel", "book", "gross", "cadence"])
    cellrows = []
    for key in need:
        pk, bk, g, cad = key
        b = lad10.loc[key]
        nd = NULL[key]
        row = dict(panel=pk, book=bk, gross=g, cadence=cad,
                   book_pass4b=bool(b.pass4b), book_pass4a=bool(b.pass4a),
                   book_CAGR=b.CAGR, book_Sharpe=b.Sharpe, book_MaxDD=b.MaxDD,
                   book_OOS_Sharpe=b.OOS_Sharpe, book_turnover=b.turnover,
                   null_base4b=float(nd.pass4b.mean()))
        for lg in LEGS:
            row[f"base_{lg}"] = float(nd[lg].mean())
            row[f"book_{lg}"] = bool(b[lg])
        for s in STATS:
            row[f"pct_{s}"] = pct_in(float(b[s]), nd[s].values, s)
        row["n_unpassable"] = int(sum(row[f"base_{lg}"] < ZERO_LEG_BAR for lg in LEGS))
        row["n_unique_null"] = int(nd.OOS_Sharpe.nunique())
        row["degenerate"] = bool(row["n_unique_null"] < DEGEN_BAR * DRAWS)
        cellrows.append(row)
    CELL = pd.DataFrame(cellrows)
    dump(CELL, "cells.csv")

    ck = CELL.set_index(["panel", "book", "gross", "cadence"])
    P(f"  cells scored: {len(CELL)}   null 4b base rate: median {CELL.null_base4b.median():.4f}, "
      f"max {CELL.null_base4b.max():.4f}, zero in {int((CELL.null_base4b == 0).sum())} of {len(CELL)}")
    P("  null PER-LEG base rates (median over cells):  " +
      "  ".join(f"{lg} {CELL[f'base_{lg}'].median():.3f}" for lg in LEGS))

    P(f"\n  DEGENERATE NULLS (a construction defect this run found, not a dial): "
      f"{int(CELL.degenerate.sum())} of {len(CELL)} cells have fewer than {DEGEN_BAR:.0%} distinct")
    P(f"  draws.  A holding-count-matched rotating draw has NOTHING TO CHOOSE when the book already")
    P(f"  holds the whole eligible pool, so on `EWELIG` (and wide `BAND03`) the null IS the book.")
    if int(CELL.degenerate.sum()):
        dg = CELL[CELL.degenerate]
        P("    by book:  " + "  ".join(f"{k} {v}" for k, v in sorted(dg.book.value_counts().items())))
        P("    by panel: " + "  ".join(f"{k} {v}" for k, v in sorted(dg.panel.value_counts().items())))
        P(f"    distinct draws in those cells: min {int(dg.n_unique_null.min())}, "
          f"median {dg.n_unique_null.median():.0f}, max {int(dg.n_unique_null.max())} (of {DRAWS})")
        P(f"    their median OOS_Sharpe percentile {dg.pct_OOS_Sharpe.median():.1f} vs "
          f"{CELL[~CELL.degenerate].pct_OOS_Sharpe.median():.1f} on the {int((~CELL.degenerate).sum())} "
          f"NON-degenerate cells")

    # ---------------------------------------------------------------- the answer
    P("\n" + "=" * 100)
    P("THE ANSWER -- how many committed 4b PASSES sit BELOW their own null's median")
    P("=" * 100)
    ans = []
    for cs in CLAIMSETS:
        cells = claim_cells[cs]
        keys = [c[:4] for c in cells]
        for weight, tag in ((False, "CELL"), (True, "CLAIM")):
            kk = keys if weight else sorted(set(keys))
            if not kk:
                continue
            sub = ck.loc[kk]
            for s in STATS:
                v = sub[f"pct_{s}"].dropna()
                ans.append(dict(claimset=cs, unit=tag, statistic=s, n=len(v),
                                share_below_median=float((v < 50).mean()),
                                median_pct=float(v.median()), mean_pct=float(v.mean()),
                                share_below_10=float((v < 10).mean()),
                                share_above_90=float((v > 90).mean())))
    ANS = pd.DataFrame(ans)
    dump(ANS, "answer.csv")
    for tag in ("CELL", "CLAIM"):
        P(f"\n  unit = {tag}  ({'one row per distinct cell' if tag == 'CELL' else 'one row per claim->cell resolution'})")
        t = ANS[ANS.unit == tag].pivot(index="statistic", columns="claimset", values="share_below_median")
        m = ANS[ANS.unit == tag].pivot(index="statistic", columns="claimset", values="median_pct")
        P("    share BELOW its own null's median:")
        P("      " + t.reindex(STATS).to_string(float_format=lambda x: f"{x:.3f}").replace("\n", "\n      "))
        P("    median percentile inside its own null:")
        P("      " + m.reindex(STATS).to_string(float_format=lambda x: f"{x:.1f}").replace("\n", "\n      "))

    P("\n  THE SAME TABLE WITH THE DEGENERATE CELLS DROPPED (same dial levels, robustness read):")
    live = set(map(tuple, CELL.loc[~CELL.degenerate, ["panel", "book", "gross", "cadence"]].values))
    nd_share = {}
    for cs in CLAIMSETS:
        kk = sorted({c[:4] for c in claim_cells[cs]} & live)
        if not kk:
            nd_share[cs] = np.nan
            continue
        sub = ck.loc[kk]
        nd_share[cs] = float((sub["pct_OOS_Sharpe"].dropna() < 50).mean())
        P(f"    {cs:7s} n {len(kk):3d}   share below median (OOS_Sharpe) {nd_share[cs]:.3f}   "
          f"median pct {sub['pct_OOS_Sharpe'].median():.1f}   "
          f"4b-pass share {sub.book_pass4b.mean():.3f}")

    zero = CELL[CELL.null_base4b == 0.0]
    P(f"\n  ZERO-BASE-RATE CELLS ({len(zero)} of {len(CELL)}):  median OOS_Sharpe percentile "
      f"{zero.pct_OOS_Sharpe.median() if len(zero) else float('nan'):.1f}   "
      f"share below median {(zero.pct_OOS_Sharpe < 50).mean() if len(zero) else float('nan'):.3f}   "
      f"exactly ONE unpassable leg in {int((zero.n_unpassable == 1).sum())} of {len(zero)}")
    if len(zero):
        P("    unpassable-leg counts: " +
          "  ".join(f"{k}:{v}" for k, v in sorted(zero.n_unpassable.value_counts().items())))
        P("    which leg is unpassable (share of zero-base-rate cells): " +
          "  ".join(f"{lg} {(zero[f'base_{lg}'] < ZERO_LEG_BAR).mean():.3f}" for lg in LEGS))

    # ---------------------------------------------------------------- rule 8
    P("\n" + "=" * 100)
    P("RULE 8 -- WALK-FORWARD  (choose on 2009-2016 alone; 2017-2026 read ONCE)")
    P("=" * 100)
    wf = walkforward(pnl, LAD, NULL, need)
    dump(wf, "walkforward.csv")
    P("\n  " + wf[["panel", "cadence", "chooser", "book", "gross", "OOS_CAGR", "OOS_Sharpe",
                   "OOS_MaxDD", "OOS_pass4b", "OOS_pass4a"]].to_string(index=False).replace("\n", "\n  "))
    for ch in sorted(wf.chooser.unique()):
        w = wf[wf.chooser == ch]
        P(f"\n  {ch:11s} OOS 4b {int(w.OOS_pass4b.sum())} of {len(w)}   OOS 4a {int(w.OOS_pass4a.sum())} of {len(w)}"
          f"   median OOS Sharpe {w.OOS_Sharpe.median():.4f}   median OOS MaxDD {w.OOS_MaxDD.median():.2%}")
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

    s_strict = float(ANS[(ANS.claimset == "STRICT") & (ANS.unit == "CELL") &
                         (ANS.statistic == "OOS_Sharpe")].share_below_median.iloc[0])
    s_wide = float(ANS[(ANS.claimset == "WIDE") & (ANS.unit == "CELL") &
                       (ANS.statistic == "OOS_Sharpe")].share_below_median.iloc[0])
    H("H_MEDIAN", (1 - s_strict) >= MEDIAN_BAR,
      f"STRICT share AT/ABOVE its own null's median OOS Sharpe = {1 - s_strict:.3f} (bar {MEDIAN_BAR})")
    zmed = float(zero.pct_OOS_Sharpe.median()) if len(zero) else float("nan")
    H("H_ZERO", bool(zmed >= 50), f"median OOS-Sharpe percentile of zero-base-rate cells = {zmed:.1f} (bar 50)")
    one = float((zero.n_unpassable == 1).mean()) if len(zero) else float("nan")
    H("H_ONELEG", bool(one >= 0.50), f"share of zero-base-rate cells with EXACTLY one unpassable leg = {one:.3f}")
    H("H_CLAIM", abs(s_strict - s_wide) <= CLAIM_BAR,
      f"|STRICT {s_strict:.3f} - WIDE {s_wide:.3f}| = {abs(s_strict - s_wide):.3f} (bar {CLAIM_BAR})")
    sides = {float(ANS[(ANS.claimset == 'STRICT') & (ANS.unit == 'CELL') &
                       (ANS.statistic == s)].share_below_median.iloc[0]) > 0.50 for s in STATS}
    H("H_STAT", len(sides) == 1,
      "STRICT share-below-median by statistic: " +
      ", ".join(f"{s} {float(ANS[(ANS.claimset=='STRICT')&(ANS.unit=='CELL')&(ANS.statistic==s)].share_below_median.iloc[0]):.3f}"
                for s in STATS))
    sk = sorted({c[:4] for c in claim_cells["STRICT"]})
    repro = float(ck.loc[sk].book_pass4b.mean()) if sk else float("nan")
    H("H_REPRO", bool(repro >= MEDIAN_BAR),
      f"{repro:.3f} of {len(sk)} resolvable STRICT cells pass 4b structurally on this tree at 10 bps")
    H("H_DEGEN", np.isfinite(nd_share["STRICT"]) and abs(nd_share["STRICT"] - s_strict) <= CLAIM_BAR,
      f"dropping the {int(CELL.degenerate.sum())} degenerate-null cells moves the STRICT "
      f"share-below-median {s_strict:.3f} -> {nd_share['STRICT']:.3f} (bar {CLAIM_BAR})")
    n_pct = int(wf[wf.chooser == "C_ISPCT"].OOS_pass4b.sum())
    n_shp = int(wf[wf.chooser == "C_ISSHARPE"].OOS_pass4b.sum())
    H("H_RULE8", n_pct >= n_shp, f"C_ISPCT OOS 4b {n_pct} vs C_ISSHARPE {n_shp} (of {int((wf.chooser=='C_ISPCT').sum())} slots each)")
    HY = pd.DataFrame(hy)
    dump(HY, "hypotheses.csv")

    # ---------------------------------------------------------------- gates
    P("\n" + "=" * 100)
    P("GATES")
    P("=" * 100)
    gates = run_gates(pnl, LAD, NULL, need, ND)
    dump(gates, "gates.csv")
    P(f"\n  {int((gates.verdict == 'PASS').sum())} of {len(gates)} gates PASS")

    (OUT / f"{STEM}.log.txt").write_text("\n".join(LOG) + "\n")
    print(f"\nwrote {STEM}.log.txt")


# =================================================================================================
def walkforward(pnl, LAD, NULL, need):
    """Three IS-only choosers pick (book, gross) inside each (panel, cadence) on 2009-2016."""
    l10 = LAD[LAD.cost == PROTO_COST]
    rows = []
    for pk in PANELS:
        pn = pnl[pk]
        for cad in CADENCES:
            sub = l10[(l10.panel == pk) & (l10.cadence == cad)].copy()
            # IS-only null percentile on IS Sharpe, where a null exists for that cell
            pct = []
            for _, r in sub.iterrows():
                key = (r.panel, r.book, r.gross, r.cadence)
                nd = NULL.get(key)
                pct.append(pct_in(float(r.IS_Sharpe), nd.IS_Sharpe.values, "Sharpe") if nd is not None else np.nan)
            sub["IS_pct"] = pct
            picks = {
                "C_IS4B": sub.sort_values(["IS_pass4b", "IS_Sharpe"], ascending=[False, False]).iloc[0],
                "C_ISSHARPE": sub.sort_values("IS_Sharpe", ascending=False).iloc[0],
                "C_ISPCT": (sub.dropna(subset=["IS_pct"]).sort_values(["IS_pct", "IS_Sharpe"],
                                                                      ascending=[False, False]).iloc[0]
                            if sub.IS_pct.notna().any() else sub.sort_values("IS_Sharpe", ascending=False).iloc[0]),
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
                                 IS_Sharpe=p.IS_Sharpe, IS_pct=p.IS_pct, IS_pass4b=bool(p.IS_pass4b),
                                 OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=odd,
                                 SPY_OOS_CAGR=pn.spy_oos[0], SPY_OOS_Sharpe=pn.spy_oos[1],
                                 SPY_OOS_MaxDD=pn.spy_oos[2],
                                 BASE_OOS_CAGR=bo[0], BASE_OOS_Sharpe=bo[1], BASE_OOS_MaxDD=bo[2],
                                 **legs, OOS_pass4b=all(legs.values()),
                                 OOS_pass4a=bool(os_ > bo[1] and odd >= bo[2])))
    return pd.DataFrame(rows)


def run_gates(pnl, LAD, NULL, need, ND):
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
        pg["panel"] = pg.panel.replace({"SMALL663": "SMALL663"})
        cols = ["CAGR", "Sharpe", "MaxDD", "OOS_Sharpe"]
        m = LAD.merge(pg[["panel", "book", "gross", "cadence", "cost"] + cols + ["REC_H1", "REC_H2", "p4b_REC_REC5"]],
                      on=["panel", "book", "gross", "cadence", "cost"], suffixes=("", "_p"))
        per = {}
        for pk in PANELS:
            mm = m[m.panel == pk]
            per[pk] = max(float(np.abs(mm[c] - mm[f"{c}_p"]).max()) for c in cols) if len(mm) else np.nan
        worst = max(v for v in per.values() if np.isfinite(v))
        G("G3", worst < G3_BAR,
          f"cross-run vs idea 971 grid.csv ({len(m):,} rows): " +
          "  ".join(f"{k} {v:.3e}" for k, v in per.items()) + f"   bar {G3_BAR:.0e}")
        dis = {pk: int((m[m.panel == pk].pass4b != m[m.panel == pk].p4b_REC_REC5).sum()) for pk in PANELS}
        G("G3b", sum(dis.values()) == 0,
          "cross-run VERDICT vs 971's p4b_REC_REC5: " + "  ".join(f"{k} {v}" for k, v in dis.items()) +
          " disagreements")
    else:
        G("G3", False, f"prior grid {PRIOR_GRID.name} not found")

    g4 = pd.DataFrame(G4_ROWS)
    tr = []
    for key in need:
        nd = NULL[key]
        bt = float(LAD[(LAD.cost == PROTO_COST) & (LAD.panel == key[0]) & (LAD.book == key[1]) &
                       (LAD.gross == key[2]) & (LAD.cadence == key[3])].turnover.iloc[0])
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
    d5 = float(abs(fmet(r[p0.warm])[1] - NULL[need[0]].Sharpe.iloc[0]))
    G("G5", d5 == 0.0, f"determinism: redrawn null draw 0 of {pk}/{bk}/{gg:.2f}/{cad} max|dSharpe| {d5:.3e}")

    # G6: choosers are IS-only -> permuting OOS rows must not move a pick
    pnl2 = {}
    rng6 = np.random.default_rng(6)
    same = True
    for k in PANELS:
        p = pnl[k]
        import copy
        q = copy.copy(p)
        rr = p.rets.copy()
        oi = np.flatnonzero(p.oos)
        rr[oi] = rr[rng6.permutation(oi)]
        q.rets = rr
        q.ctx = {c: Ctx(rr, p.app[c]) for c in CADENCES}
        pnl2[k] = q
    lad2 = []
    for pk_ in PANELS:
        q = pnl2[pk_]
        for bk_ in BOOKS:
            for gg_ in GROSS_GRID:
                W = lag_weights(q.books[gg_][bk_])
                for cad_ in CADENCES:
                    r_, t_ = q.ctx[cad_].run(W, 0.0)
                    r = r_ - t_ * PROTO_COST / 1e4
                    st = stats_of(q, r)
                    lgi = legs_4b_is(q, st)
                    lad2.append(dict(panel=pk_, book=bk_, gross=gg_, cadence=cad_, cost=PROTO_COST,
                                     **st, IS_pass4b=all(lgi.values())))
    L2 = pd.DataFrame(lad2)
    for pk_ in PANELS:
        for cad_ in CADENCES:
            a = LAD[(LAD.cost == PROTO_COST) & (LAD.panel == pk_) & (LAD.cadence == cad_)]
            b = L2[(L2.panel == pk_) & (L2.cadence == cad_)]
            for keycols in (["IS_pass4b", "IS_Sharpe"], ["IS_Sharpe"]):
                pa = a.sort_values(keycols, ascending=False).iloc[0]
                pb = b.sort_values(keycols, ascending=False).iloc[0]
                same &= (pa.book == pb.book and pa.gross == pb.gross)
    G("G6", same, "rule-8 choosers invariant to permuted OOS return rows (IS-only)")

    # G7: percentile calibration -- a DRAW scored against the rest of its own null
    cal = []
    for key in need:
        v = NULL[key].OOS_Sharpe.values
        for d in range(min(len(v), 25)):
            rest = np.delete(v, d)
            cal.append(pct_in(v[d], rest, "OOS_Sharpe"))
    cal = np.array([c for c in cal if np.isfinite(c)])
    G("G7", 45.0 <= float(np.median(cal)) <= 55.0,
      f"percentile calibration on {len(cal):,} self-scored draws: median {np.median(cal):.2f}, "
      f"mean {cal.mean():.2f} (bar [45,55])")
    return pd.DataFrame(g)


if __name__ == "__main__":
    main()

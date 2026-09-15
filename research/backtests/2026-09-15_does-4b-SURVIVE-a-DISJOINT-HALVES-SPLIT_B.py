#!/usr/bin/env python3
"""Idea 970 (lane B, 2026-09-15) -- does 4b SURVIVE a DISJOINT-HALVES SPLIT?

THE PRIOR RESULT (idea 942, committed 2026-09-15, cloud)
  PROTOCOL 4b reads THREE Sharpe legs: H1, H2 and rule-8 OOS.  942 measured the windows and
  found 4b's H2 window is **100.0% contained inside** the rule-8 OOS window (OOS is 91.2% H2):
  the full sample starts at the warm-up and ends 2026, so the halfway row falls in late 2017,
  while OOS starts 2017-01-01.  Dropping L_OOS changed the joint verdict on **0 of 1,500**
  gross-matched null draws.  The third leg is one window counted twice.

  942 proposed, and did NOT apply (PROTOCOL rule 6), CLAUSE (i):
    "The out-of-sample window must be disjoint from the second half used by rule 4b.  Either
     the 4b halves are taken inside the in-sample window (2009-2016 split in two), or the
     halves are dropped and 4b reads IS and OOS.  A 4b verdict whose H2 and OOS windows
     overlap is reported as a two-leg verdict."

WHAT THIS RUN DOES
  Prices clause (i).  It rebuilds the record's own 4b grid, scores every book under the
  record's convention AND under both of clause (i)'s forms, and reports **which committed 4b
  passes are DESTROYED and which are CREATED** by making the legs disjoint -- then asks the
  question that decides whether the clause is worth adopting: does a disjoint split give 4b
  back any power to tell a rule from a coin flip?  A reshuffle that destroys some passes and
  creates others while leaving the null's base rate where it was is cosmetic.

THE THREE SPLIT RULES (TUNED DIAL 1, all levels always reported, none ever chosen)
  REC      the record's convention.  H1/H2 = the two halves of the post-warm-up FULL sample;
           OOS = 2017-01-01 ->.  H2 and OOS overlap; this is what every committed 4b pass in
           the record was read under.
  DISJ     clause (i) form A.  H1/H2 = the two halves of the IN-SAMPLE window (warm-up ->
           2016-12-31); OOS untouched.  Three genuinely disjoint windows, each half ~4 years.
  TWOLEG   clause (i) form B.  The halves are dropped: 4b reads IS Sharpe and OOS Sharpe.
  L_DD and L_CAGR are read on the FULL sample under all three, so every difference between
  the three columns is a difference in the SHARPE legs and nothing else.

CADENCE (TUNED DIAL 2, all levels always reported)  W / M / Q.

REPORTED, NEVER FITTED
  PANEL {U56, B136, SMALL663}, BOOK {TOP5, TOP10, TOP20, EWELIG, BAND03}, GROSS {0.50, 0.65,
  0.75, 1.00}, COST RUNG {0, 5, 10, 25, 50} bps with 10 BINDING (PROTOCOL rule 2).  The gross
  and cost ladders are the record's own committed ones (idea 937), fixed before any number
  here was read.  CLAIM SET {STRICT, WIDE} is NOT a tuned dial: both are always printed side
  by side and neither is ever used to choose anything -- the honest answer is the interval.

PRE-REGISTERED HYPOTHESES (bars fixed before any number was read)
  H_DESTROY   the disjoint split destroys a material share of the record's re-priceable
              committed 4b passes.  PASS iff destroyed / reproduced >= 0.25 under DISJ at
              10 bps, STRICT.
  H_SYM       the split is a RESHUFFLE, not a tightening: it creates about as many passes as
              it destroys.  PASS iff |created - destroyed| / reproduced <= 0.10 (DISJ, 10 bps,
              STRICT).  H_DESTROY and H_SYM can both pass; they are different questions.
  H_NULL      a disjoint split buys back discriminating power.  PASS iff the MEDIAN over the
              9 (panel, cadence) null cells of base_rate(DISJ) / base_rate(REC) <= 0.50.
  H_INDEP     with the windows made disjoint, the OOS leg stops being redundant.  PASS iff
              P(all 5 legs) / P(the other 4) <= 0.95 under DISJ in >= 5 of the 9 null cells
              where it is defined.  (942 read exactly 1.0000 under REC.)

RULE 8 (walk-forward, mandatory)
  (book, gross) is chosen on the IN-SAMPLE window 2009-2016 ALONE by three IS-only choosers,
  per (panel, cadence, split rule); 2017-2026 is then read ONCE.  OOS CAGR / Sharpe / MaxDD
  are reported against the RULES v2 baseline and against SPY, and BOTH KEEP paths (4a and 4b)
  are scored on every pick.  G6 proves every chooser is IS-only by permuting the OOS columns.

GATES
  G1  closed-form runner == `engine.backtest` @10 bps, 3 books x 3 cadences.  Bar 1e-12.
  G2  BAND03 @0.75 weights == `baseline.rules_v2_weights(px, 0.03, 0.75)`.  Bar 0.0 exact.
  G3  CROSS-RUN against idea 942's committed console: (a) the H2/OOS window overlap it
      published (H2 100.0% inside OOS, OOS 91.2% H2) and (b) its committed U56/CAND20 monthly
      OOS triple 17.53% / 1.305 / -19.51%.
  G4  GROSS MATCH: every null's target gross and holding count equal the book's on every
      decision row (bar 0.0) and its realised annual turnover is > 0.5x (idea 931's defect).
  G5  determinism: the null grid is regenerated from the same seeds, bit-for-bit.
  G6  every rule-8 chooser is IS-ONLY: picks invariant to permuted OOS return columns.
  G7  DISJOINTNESS: under DISJ, |H1 n H2| = |H2 n OOS| = |H1 n OOS| = 0 rows on every panel,
      and under REC the H2 n OOS overlap is non-zero (the defect being priced).
  G8  CENSUS CORPUS stamped with (commit sha, file count, byte count, row count) beside every
      denominator -- idea 894's clause, applied voluntarily.

SURVIVORSHIP (PROTOCOL 9)
  U56 / B136 / SMALL663 are CURRENT-constituent lists, so every CAGR and drawdown LEVEL here
  is optimistic and every null base rate is an UPPER bound (a coin flip drawn from a survivor
  panel is a better book than one drawn in real time).  The created/destroyed contrast is the
  SAME books on the SAME tape under two window definitions, so it is untouched by it.

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
SPLITS = ["REC", "DISJ", "TWOLEG"]
PANELS = ["U56", "B136", "SMALL663"]
DRAWS = 200
SEED0 = 970
NULL_BOOK = "TOP20"          # the gross-matched reference book, the record's convention
NULL_GROSS = 0.75

DESTROY_BAR = 0.25           # H_DESTROY
SYM_BAR = 0.10               # H_SYM
NULL_RATIO_BAR = 0.50        # H_NULL
INDEP_BAR, INDEP_CELLS = 0.95, 5   # H_INDEP

# cross-run reproduction targets (G3).  The record carries TWO committed U56/TOP20/M OOS
# triples because it carries two TOP20 constructions -- idea 944's G3b defect: a FIXED g/n book
# (de-gross when fewer than n names are eligible) and a RE-SPREAD g/k(t) one.  Both are
# reproduced here and named, rather than one being called a miss.
PUB_OVERLAP_H2_IN_OOS = 1.000
PUB_OVERLAP_OOS_IS_H2 = 0.912
PUB_TOP20_M_OOS_DEGROSS = (0.1667, 1.283, -0.1951)      # idea 951, committed
PUB_TOP20_M_OOS_RESPREAD = (0.1753, 1.305, -0.1951)     # idea 942, committed
G3_TOL = (6e-4, 2e-3, 6e-4)

SMOKE = bool(int(os.environ.get("IDEA970_SMOKE", "0")))
if SMOKE:
    DRAWS = 6

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
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
# runner (gated at G1) -- closed form equivalent of engine.backtest's day loop
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
    """Holds the tape, the three window sets, and SPY's reference legs under each split rule."""

    def __init__(self, name, px):
        self.name, self.px, self.idx = name, px, px.index
        self.rets = np.nan_to_num(px.pct_change().values, nan=0.0, posinf=0.0, neginf=0.0)
        self.T = len(self.idx)
        self.warm = np.arange(self.T) >= WARMUP
        wpos = np.flatnonzero(self.warm)

        self.oos = np.zeros(self.T, bool)
        self.oos[np.asarray(self.idx >= pd.Timestamp(OOS_START)) & self.warm] = True
        self.is_ = self.warm & np.asarray(self.idx <= pd.Timestamp(IS_END))

        h = len(wpos) // 2                       # REC halves: the FULL post-warm-up sample
        self.rec_h1 = np.zeros(self.T, bool); self.rec_h1[wpos[:h]] = True
        self.rec_h2 = np.zeros(self.T, bool); self.rec_h2[wpos[h:]] = True

        ipos = np.flatnonzero(self.is_)          # DISJ halves: INSIDE the IS window
        hi = len(ipos) // 2
        self.dis_h1 = np.zeros(self.T, bool); self.dis_h1[ipos[:hi]] = True
        self.dis_h2 = np.zeros(self.T, bool); self.dis_h2[ipos[hi:]] = True
        self.rec_h2_start = self.idx[wpos[h]]
        self.dis_h2_start = self.idx[ipos[hi]]

        self.win = {
            "REC": (self.rec_h1, self.rec_h2),
            "DISJ": (self.dis_h1, self.dis_h2),
            "TWOLEG": (self.is_, None),
        }
        spy = np.nan_to_num(px["SPY"].pct_change().values, nan=0.0)
        self.spy = spy
        self.spy_full = fmet(spy[self.warm])
        self.spy_oos_s = fmet(spy[self.oos])[1]
        self.spy_leg = {}
        for s, (a, b) in self.win.items():
            self.spy_leg[s] = (fmet(spy[a])[1], (fmet(spy[b])[1] if b is not None else np.nan))

        self.priced = px.notna().values
        above = px > px.rolling(200).mean()
        vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        self.elig = (above & (vol20 < VOLCAP) & px.notna()).values
        self.dec = {c: rebalance_mask(self.idx, c).values.copy() for c in CADENCES}
        self.app = {c: applied_from_decision(self.dec[c]) for c in CADENCES}
        self.ctx = {c: Ctx(self.rets, self.app[c]) for c in CADENCES}
        # RULES v2 baseline (live book) on this panel, weekly, at the binding rung -- the 4a bar
        bw = lag_weights(rules_v2_weights(px, BAND0, 0.75).values)
        self.base_r = {}
        for c_ in COSTS:
            self.base_r[c_] = self.ctx["W"].run(bw, c_)[0]


def stats_of(pn, r):
    """Every statistic 4a / 4b need, under all three split rules, from one return stream."""
    c, s, dd = fmet(r[pn.warm])
    oc, os_, odd = fmet(r[pn.oos])
    out = dict(CAGR=c, Sharpe=s, MaxDD=dd, OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=odd)
    for sp, (a, b) in pn.win.items():
        out[f"{sp}_H1"] = fmet(r[a])[1]
        out[f"{sp}_H2"] = fmet(r[b])[1] if b is not None else np.nan
    return out


def legs_4b(pn, st, sp):
    """4b under split rule `sp`.  L_DD and L_CAGR are FULL-sample under all three."""
    l1 = st[f"{sp}_H1"] > pn.spy_leg[sp][0]
    l2 = True if sp == "TWOLEG" else (st[f"{sp}_H2"] > pn.spy_leg[sp][1])
    lo = st["OOS_Sharpe"] > pn.spy_oos_s
    ld = abs(st["MaxDD"]) <= DD_CAP * abs(pn.spy_full[2])
    lc = st["CAGR"] >= CAGR_FLOOR * pn.spy_full[0]
    return dict(L_H1=bool(l1), L_H2=bool(l2), L_OOS=bool(lo), L_DD=bool(ld), L_CAGR=bool(lc))


def pass_4a(pn, r, bst, sp):
    """4a: Sharpe > the LIVE RULES v2 book in BOTH halves (of this split rule) and MaxDD no
    worse.  TWOLEG reads the single IS window in place of the two halves."""
    a, b = pn.win[sp]
    ok = fmet(r[a])[1] > fmet(bst[a])[1]
    if b is not None:
        ok = ok and fmet(r[b])[1] > fmet(bst[b])[1]
    return bool(ok and fmet(r[pn.warm])[2] >= fmet(bst[pn.warm])[2])


# =================================================================================================
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
    """Gross-matched ROTATING coin flip (idea 680/926/931/942's RANDROT, unmodified).

    On every DECISION row it holds exactly as many equally weighted names as the book holds
    that day, at the book's own per-name weight, drawn uniformly from the book's OWN
    eligibility pool.  Gross, holding count and cash drag match row by row (G4); only WHICH
    names are held differs.  Written on the DECISION rows -- writing on the APPLICATION rows
    leaves the null in pure cash (idea 931's committed defect, caught here by G4's turnover).
    """
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


# =================================================================================================
# CENSUS of the record's committed 4b PASS rows
# =================================================================================================
PASSCOLS = ["pass4b", "p4b", "keep4b", "is4b", "pass_4b", "b4b", "x4b"]
PANEL_ALIAS = {"u56": "U56", "u_56": "U56", "core": "U56", "universe": "U56", "u56core": "U56",
               "b136": "B136", "broad": "B136", "b_136": "B136", "broad136": "B136",
               "small663": "SMALL663", "small": "SMALL663", "small439": "SMALL663",
               "small716": "SMALL663", "small485": "SMALL663"}
BOOK_ALIAS = {"top5": "TOP5", "top05": "TOP5", "cand5": "TOP5",
              "top10": "TOP10", "cand10": "TOP10",
              "top20": "TOP20", "cand20": "TOP20", "top_20": "TOP20",
              "ewelig": "EWELIG", "ewall": "EWELIG", "ew": "EWELIG", "elig": "EWELIG",
              "band03": "BAND03", "band3": "BAND03", "band": "BAND03", "rulesv2": "BAND03",
              "v2": "BAND03"}
CAD_ALIAS = {"w": "W", "week": "W", "weekly": "W", "m": "M", "month": "M", "monthly": "M",
             "q": "Q", "quarter": "Q", "quarterly": "Q"}


def _norm(x):
    return str(x).strip().lower().replace("-", "").replace(" ", "").replace("/", "")


def _snap(v, grid, tol):
    d = np.abs(np.asarray(grid)[None, :] - np.asarray(v, float)[:, None])
    j = d.argmin(axis=1)
    out = np.asarray(grid, float)[j]
    return np.where(d[np.arange(len(j)), j] <= tol, out, np.nan)


def census(grid_idx):
    """Harvest every committed 4b PASS row that names its own cell, and map it onto the grid.

    STRICT: panel, book, cadence, gross and cost must ALL be present in the file's schema and
            map EXACTLY (gross and cost to a grid rung within 1e-3).
    WIDE  : adds nearest-snap of gross (within 0.15) and cost (nearest rung), and PROTOCOL's
            own defaults (gross 0.75, cost 10 bps) where the file's schema carries no such
            column.  Deliberately generous; printed beside STRICT, never chosen between.

    Rows from the record's own COIN-FLIP artifacts (`.draws.`/`.nulls.` files, or files
    carrying a `draw` column) are EXCLUDED and counted separately -- idea 937 found 28.9% of
    the record's committed monthly 4b passes were null draws, and including them would
    measure this run's own object.
    """
    files = sorted(OUT.glob("*.csv"))
    n_files = n_bytes = n_rows = 0
    passes = excluded = 0
    mapped = {"STRICT": [], "WIDE": []}
    miss = {"panel": 0, "book": 0, "cadence": 0, "gross": 0, "cost": 0}
    for f in files:
        try:
            head = pd.read_csv(f, nrows=0)
        except Exception:
            continue
        cols = {c.strip().lower(): c for c in head.columns}
        pc = next((cols[c] for c in PASSCOLS if c in cols), None)
        if pc is None or not any(c in cols for c in ("panel", "book", "cadence", "freq")):
            continue
        try:
            df = pd.read_csv(f, low_memory=False)
        except Exception:
            continue
        n_files += 1
        n_bytes += f.stat().st_size
        n_rows += len(df)
        flag = df[pc]
        if flag.dtype == object:
            keep = flag.astype(str).str.strip().str.lower().isin(["true", "1", "pass", "yes"])
        else:
            keep = pd.to_numeric(flag, errors="coerce").fillna(0) > 0.5
        sub = df[keep.values]
        if len(sub) == 0:
            continue
        is_null_art = ("draw" in cols or ".draws." in f.name or ".nulls." in f.name
                       or "null" in f.name.lower())
        if is_null_art:
            excluded += len(sub)
            continue
        passes += len(sub)
        n = len(sub)
        pan = (sub[cols["panel"]].map(lambda x: PANEL_ALIAS.get(_norm(x))) if "panel" in cols
               else pd.Series([None] * n, index=sub.index))
        bk = (sub[cols["book"]].map(lambda x: BOOK_ALIAS.get(_norm(x))) if "book" in cols
              else pd.Series([None] * n, index=sub.index))
        ck = next((k for k in ("cadence", "freq") if k in cols), None)
        cd = (sub[cols[ck]].map(lambda x: CAD_ALIAS.get(_norm(x))) if ck
              else pd.Series([None] * n, index=sub.index))
        gk = next((k for k in ("gross", "g") if k in cols), None)
        gr = pd.to_numeric(sub[cols[gk]], errors="coerce") if gk else pd.Series([np.nan] * n, index=sub.index)
        ck2 = next((k for k in ("cost", "cost_bps", "bps", "rung") if k in cols), None)
        ct = pd.to_numeric(sub[cols[ck2]], errors="coerce") if ck2 else pd.Series([np.nan] * n, index=sub.index)
        miss["panel"] += int(pan.isna().sum()); miss["book"] += int(bk.isna().sum())
        miss["cadence"] += int(cd.isna().sum()); miss["gross"] += int(gr.isna().sum())
        miss["cost"] += int(ct.isna().sum())

        gS = _snap(gr.values, GROSS_GRID, 1e-3)
        cS = _snap(ct.values, COSTS, 1e-3)
        okS = pan.notna().values & bk.notna().values & cd.notna().values & ~np.isnan(gS) & ~np.isnan(cS)
        for i in np.flatnonzero(okS):
            key = (pan.iloc[i], bk.iloc[i], float(gS[i]), cd.iloc[i], float(cS[i]))
            if key in grid_idx:
                mapped["STRICT"].append((f.name,) + key)
        grW = np.where(np.isnan(gr.values), 0.75, gr.values)
        ctW = np.where(np.isnan(ct.values), PROTO_COST, ct.values)
        cdW = cd.fillna("W")            # PROTOCOL rule 3's own baseline_freq, stated
        gW = _snap(grW, GROSS_GRID, 0.15)
        cW = _snap(ctW, COSTS, 1e9)
        okW = pan.notna().values & bk.notna().values & ~np.isnan(gW)
        for i in np.flatnonzero(okW):
            key = (pan.iloc[i], bk.iloc[i], float(gW[i]), cdW.iloc[i], float(cW[i]))
            if key in grid_idx:
                mapped["WIDE"].append((f.name,) + key)
    return mapped, dict(files=n_files, bytes=n_bytes, rows=n_rows, passes=passes,
                        excluded_null_rows=excluded, miss=miss)


# =================================================================================================
def main():
    LOG.clear()
    sha = head_sha()
    P("=" * 100)
    P("IDEA 970 (lane B) -- does 4b SURVIVE a DISJOINT-HALVES SPLIT?")
    P(f"sha {sha} | draws {DRAWS} | binding rung {PROTO_COST:.0f} bps | smoke {SMOKE}")
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
    P("GATES")
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

    pn = pans["U56"]
    ov = int((pn.rec_h2 & pn.oos).sum())
    a_h2_in_oos = ov / pn.rec_h2.sum()
    a_oos_is_h2 = ov / pn.oos.sum()
    r_cand = pn.ctx["M"].run(lag_weights(W[("U56", "TOP20", 0.75)]), PROTO_COST)[0]
    oc, os_, odd = fmet(r_cand[pn.oos])
    d3 = [abs(oc - PUB_TOP20_M_OOS_DEGROSS[0]), abs(os_ - PUB_TOP20_M_OOS_DEGROSS[1]),
          abs(odd - PUB_TOP20_M_OOS_DEGROSS[2])]
    # the RE-SPREAD twin of the same book: g/k(t) instead of a fixed g/20
    sc_, ab_, v20_ = score(pn.px, vol_scale=False)
    el_ = ab_ & (v20_ < VOLCAP) & pn.px.notna()
    rk_ = sc_.where(el_).rank(axis=1, ascending=False)
    sel_ = (rk_ <= 20).astype(float)
    wres = (0.75 * sel_.div(sel_.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)).values
    rc2 = pn.ctx["M"].run(lag_weights(wres), PROTO_COST)[0]
    oc2, os2, odd2 = fmet(rc2[pn.oos])
    d3c = [abs(oc2 - PUB_TOP20_M_OOS_RESPREAD[0]), abs(os2 - PUB_TOP20_M_OOS_RESPREAD[1]),
           abs(odd2 - PUB_TOP20_M_OOS_RESPREAD[2])]
    g3a = abs(a_h2_in_oos - PUB_OVERLAP_H2_IN_OOS) < 0.02 and abs(a_oos_is_h2 - PUB_OVERLAP_OOS_IS_H2) < 0.03
    g3b = all(d <= t for d, t in zip(d3, G3_TOL))
    g3c = all(d <= t for d, t in zip(d3c, G3_TOL))
    gates["G3"] = g3a and g3b and g3c
    P(f"  G3a 942's window overlap: H2 {a_h2_in_oos:.1%} inside OOS (published {PUB_OVERLAP_H2_IN_OOS:.1%}), "
      f"OOS {a_oos_is_h2:.1%} is H2 (published {PUB_OVERLAP_OOS_IS_H2:.1%})  [{'PASS' if g3a else 'FAIL'}]")
    P(f"  G3b DE-GROSS U56/TOP20/M OOS {oc:.2%} / {os_:.3f} / {odd:.2%} vs idea 951's committed "
      f"{PUB_TOP20_M_OOS_DEGROSS[0]:.2%} / {PUB_TOP20_M_OOS_DEGROSS[1]:.3f} / "
      f"{PUB_TOP20_M_OOS_DEGROSS[2]:.2%}; |d| = {d3[0]:.2e} / {d3[1]:.2e} / {d3[2]:.2e}  "
      f"[{'PASS' if g3b else 'FAIL'}]")
    P(f"  G3c RE-SPREAD twin  OOS {oc2:.2%} / {os2:.3f} / {odd2:.2%} vs idea 942's committed "
      f"{PUB_TOP20_M_OOS_RESPREAD[0]:.2%} / {PUB_TOP20_M_OOS_RESPREAD[1]:.3f} / "
      f"{PUB_TOP20_M_OOS_RESPREAD[2]:.2%}; |d| = {d3c[0]:.2e} / {d3c[1]:.2e} / {d3c[2]:.2e}  "
      f"[{'PASS' if g3c else 'FAIL'}]")
    P("      (the two committed triples are the SAME cell under idea 944's G3b de-gross / re-spread "
      "split;\n       every book in this run is the FIXED g/n de-gross construction)")

    buf = np.zeros_like(pn.rets)
    wref = W[("U56", NULL_BOOK, NULL_GROSS)]
    gm, km, tmin = 0.0, 0, 1e9
    for d in range(3):
        rg = np.random.default_rng(seed_of("U56", "M", d))
        nw = draw_null(buf, pn, wref, pn.dec["M"], rg)
        gm = max(gm, float(np.abs(nw[pn.dec["M"]].sum(axis=1) - wref[pn.dec["M"]].sum(axis=1)).max()))
        km = max(km, int(np.abs((nw[pn.dec["M"]] > 0).sum(axis=1) - (wref[pn.dec["M"]] > 0).sum(axis=1)).max()))
        _, tt = pn.ctx["M"].run(lag_weights(nw), PROTO_COST)
        tmin = min(tmin, tt[pn.warm].sum() / (pn.warm.sum() / 252.0))
    gates["G4"] = gm < 1e-12 and km == 0 and tmin > 0.5
    P(f"  G4  gross match on 3 draws: max|d gross| = {gm:.3e}, max|d count| = {km}, "
      f"min realised annual turnover = {tmin:.2f}x  [{'PASS' if gates['G4'] else 'FAIL'}]")

    a = draw_null(np.zeros_like(pn.rets), pn, wref, pn.dec["M"], np.random.default_rng(seed_of("U56", "M", 7)))
    b_ = draw_null(np.zeros_like(pn.rets), pn, wref, pn.dec["M"], np.random.default_rng(seed_of("U56", "M", 7)))
    gates["G5"] = float(np.abs(a - b_).max()) == 0.0
    P(f"  G5  determinism / seed reproducibility: max|d| = {np.abs(a - b_).max():.3e}  "
      f"[{'PASS' if gates['G5'] else 'FAIL'}]")

    ok7 = True
    for k in PANELS:
        q = pans[k]
        o1 = int((q.dis_h1 & q.dis_h2).sum()); o2 = int((q.dis_h2 & q.oos).sum()); o3 = int((q.dis_h1 & q.oos).sum())
        orec = int((q.rec_h2 & q.oos).sum())
        ok7 = ok7 and o1 == 0 and o2 == 0 and o3 == 0 and orec > 0
        P(f"  G7  {k}: DISJ overlaps H1nH2 {o1}, H2nOOS {o2}, H1nOOS {o3} (all must be 0); "
          f"REC H2nOOS {orec} days = the defect being priced")
        P(f"      REC H2 starts {q.rec_h2_start.date()}, DISJ H2 starts {q.dis_h2_start.date()}, "
          f"OOS starts {OOS_START}")
    gates["G7"] = ok7
    P(f"  G7  disjointness  [{'PASS' if ok7 else 'FAIL'}]")
    P(f"      SMALL663 screen: {n_drop} tickers with max_1d_move >= 1.0 dropped")

    # ------------------------------------------------------- THE BOOK GRID --------------------
    P("\n" + "-" * 100)
    P(f"BOOK GRID -- {len(PANELS)} panels x {len(BOOKS)} books x {len(GROSS_GRID)} gross x "
      f"{len(CADENCES)} cadences x {len(COSTS)} rungs = "
      f"{len(PANELS)*len(BOOKS)*len(GROSS_GRID)*len(CADENCES)*len(COSTS):,} book rows, "
      f"each scored under {len(SPLITS)} split rules")
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
                                   turnover=ann_turn, **st)
                        for sp in SPLITS:
                            lg = legs_4b(q, st, sp)
                            row[f"p4b_{sp}"] = all(lg.values())
                            row[f"fail_{sp}"] = ",".join(x for x, v in lg.items() if not v) or ""
                            row[f"p4a_{sp}"] = pass_4a(q, r, q.base_r[cost], sp)
                        rows.append(row)
    grid = pd.DataFrame(rows)
    dump(grid, "grid.csv")

    gidx = set(zip(grid.panel, grid.book, grid.gross, grid.cadence, grid.cost))
    gmap = {kk: i for i, kk in enumerate(zip(grid.panel, grid.book, grid.gross, grid.cadence, grid.cost))}

    at10 = grid[grid.cost == PROTO_COST]
    P(f"\n  4b PASS counts at {PROTO_COST:.0f} bps, over {len(at10)} book rows:")
    for sp in SPLITS:
        P(f"    {sp:7s}  4b {int(at10[f'p4b_{sp}'].sum()):4d} / {len(at10)}   "
          f"4a {int(at10[f'p4a_{sp}'].sum()):4d} / {len(at10)}")
    P("\n  by cadence (TUNED dial 2), 4b passes at 10 bps:")
    tab = at10.groupby("cadence")[[f"p4b_{s}" for s in SPLITS]].sum().astype(int)
    tab["n"] = at10.groupby("cadence").size()
    P(tab.to_string())
    P("\n  by cost rung (reported, 10 bps binding), 4b passes:")
    tabc = grid.groupby("cost")[[f"p4b_{s}" for s in SPLITS]].sum().astype(int)
    tabc["n"] = grid.groupby("cost").size()
    P(tabc.to_string())
    P("\n  by panel, 4b passes at 10 bps:")
    tabp = at10.groupby("panel")[[f"p4b_{s}" for s in SPLITS]].sum().astype(int)
    tabp["n"] = at10.groupby("panel").size()
    P(tabp.to_string())

    # created / destroyed on the WHOLE GRID (not just the census)
    P("\n" + "-" * 100)
    P("CREATED AND DESTROYED -- the whole rebuilt grid, every rung")
    P("-" * 100)
    cd_rows = []
    for cost in COSTS:
        sub = grid[grid.cost == cost]
        for sp in ("DISJ", "TWOLEG"):
            dest = int((sub["p4b_REC"] & ~sub[f"p4b_{sp}"]).sum())
            crea = int((~sub["p4b_REC"] & sub[f"p4b_{sp}"]).sum())
            base = int(sub["p4b_REC"].sum())
            cd_rows.append(dict(cost=cost, split=sp, rec_passes=base, destroyed=dest, created=crea,
                                after=int(sub[f"p4b_{sp}"].sum()),
                                destroyed_share=dest / base if base else np.nan,
                                net=crea - dest))
    cdf = pd.DataFrame(cd_rows)
    P(cdf.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    dump(cdf, "created_destroyed.csv")

    # ---- the object 942 named: is the H2 leg the OOS leg under another name? ------------------
    P("\n" + "-" * 100)
    P("ONE WINDOW COUNTED TWICE -- how much of the H2 leg is the OOS leg, on the BOOKS")
    P("-" * 100)
    ov_rows = []
    for k in PANELS:
        for c in CADENCES:
            s = grid[(grid.panel == k) & (grid.cadence == c)]
            row = dict(panel=k, cadence=c, n=len(s))
            for sp in ("REC", "DISJ"):
                h2 = s[f"{sp}_H2"].values
                oo = s["OOS_Sharpe"].values
                m = ~np.isnan(h2) & ~np.isnan(oo)
                row[f"corr_{sp}"] = float(np.corrcoef(h2[m], oo[m])[0, 1]) if m.sum() > 2 else np.nan
                l2 = h2 > pans[k].spy_leg[sp][1]
                lo = oo > pans[k].spy_oos_s
                row[f"legagree_{sp}"] = float((l2 == lo).mean())
            ov_rows.append(row)
    ovd = pd.DataFrame(ov_rows)
    P(ovd.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    P(f"\n  pooled over {len(grid)} book rows: corr(H2 Sharpe, OOS Sharpe) REC "
      f"{np.corrcoef(grid['REC_H2'], grid['OOS_Sharpe'])[0,1]:.4f} -> DISJ "
      f"{np.corrcoef(grid['DISJ_H2'], grid['OOS_Sharpe'])[0,1]:.4f}")
    dump(ovd, "window_overlap.csv")

    # ------------------------------------------------------------ THE CENSUS ------------------
    P("\n" + "-" * 100)
    P("CENSUS -- the record's committed 4b PASS rows, re-scored under clause (i)")
    P("-" * 100)
    mapped, meta_c = census(gidx)
    P(f"  corpus: sha {sha}, {meta_c['files']:,} eligible committed csv files, "
      f"{meta_c['bytes']:,} bytes, {meta_c['rows']:,} rows, {meta_c['passes']:,} committed 4b PASS rows "
      f"(coin-flip/draw files excluded)   [G8]")
    P(f"  unmappable field counts: {meta_c['miss']}")
    gates["G8"] = meta_c["files"] > 0

    cen_rows = []
    for cs in ("STRICT", "WIDE"):
        m = mapped[cs]
        if not m:
            P(f"  {cs}: 0 rows mapped")
            continue
        cells = pd.DataFrame(m, columns=["file", "panel", "book", "gross", "cadence", "cost"])
        cells["i"] = [gmap[(p, b, g, c, ct)] for p, b, g, c, ct in
                      zip(cells.panel, cells.book, cells.gross, cells.cadence, cells.cost)]
        for cost_filter in (None, PROTO_COST):
            cc = cells if cost_filter is None else cells[cells.cost == cost_filter]
            if len(cc) == 0:
                continue
            g_ = grid.iloc[cc["i"].values]
            repro = int(g_["p4b_REC"].sum())
            for sp in ("DISJ", "TWOLEG"):
                dest = int((g_["p4b_REC"].values & ~g_[f"p4b_{sp}"].values).sum())
                crea = int((~g_["p4b_REC"].values & g_[f"p4b_{sp}"].values).sum())
                cen_rows.append(dict(claim_set=cs, rung=("ALL" if cost_filter is None else f"{cost_filter:.0f}"),
                                     committed_rows=len(cc), distinct_cells=cc.drop_duplicates(
                                         ["panel", "book", "gross", "cadence", "cost"]).shape[0],
                                     reproduced_REC=repro, split=sp, destroyed=dest, created=crea,
                                     surviving=repro - dest,
                                     destroyed_share=dest / repro if repro else np.nan))
    cen = pd.DataFrame(cen_rows)
    if len(cen):
        P(cen.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
        dump(cen, "census.csv")
    for cs in ("STRICT", "WIDE"):
        if mapped[cs]:
            dump(pd.DataFrame(mapped[cs], columns=["file", "panel", "book", "gross", "cadence", "cost"]),
                 f"mapped_{cs}.csv")

    # ------------------------------------------------------------- THE NULL -------------------
    P("\n" + "-" * 100)
    P(f"NULL GRID -- {len(PANELS)} panels x {len(CADENCES)} cadences x {DRAWS} gross-matched "
      f"coin flips = {len(PANELS)*len(CADENCES)*DRAWS:,} null books, scored at {PROTO_COST:.0f} bps "
      f"under all three split rules")
    P("-" * 100)
    nrows = []
    for k in PANELS:
        q = pans[k]
        wref = W[(k, NULL_BOOK, NULL_GROSS)]
        buf = np.zeros_like(q.rets)
        for c in CADENCES:
            dec = q.dec[c]
            rng = np.random.default_rng(seed_of(k, c, "stream", SEED0))
            for d in range(DRAWS):
                nw = draw_null(buf, q, wref, dec, rng)
                r = q.ctx[c].run(lag_weights(nw), PROTO_COST)[0]
                st = stats_of(q, r)
                row = dict(panel=k, cadence=c, draw=d, CAGR=st["CAGR"], Sharpe=st["Sharpe"],
                           MaxDD=st["MaxDD"], OOS_Sharpe=st["OOS_Sharpe"])
                for sp in SPLITS:
                    lg = legs_4b(q, st, sp)
                    row[f"p4b_{sp}"] = all(lg.values())
                    for lname, v in lg.items():
                        row[f"{sp}_{lname}"] = v
                    row[f"p4b_{sp}_noOOS"] = all(v for x, v in lg.items() if x != "L_OOS")
                nrows.append(row)
        P(f"  {k}: done")
    nulls = pd.DataFrame(nrows)
    dump(nulls, "nulls.csv")

    br = nulls.groupby(["panel", "cadence"])[[f"p4b_{s}" for s in SPLITS]].mean()
    br["ratio_DISJ_over_REC"] = np.where(br["p4b_REC"] > 0, br["p4b_DISJ"] / br["p4b_REC"], np.nan)
    br["ratio_TWOLEG_over_REC"] = np.where(br["p4b_REC"] > 0, br["p4b_TWOLEG"] / br["p4b_REC"], np.nan)
    P("\n  4b base rate of a gross-matched coin flip, by split rule:")
    P(br.to_string(float_format=lambda x: f"{x:.3f}"))
    dump(br.reset_index(), "baserates.csv")

    P("\n  per-leg null base rates (the leg census 942 ran under REC only):")
    leg_tab = nulls.groupby(["panel", "cadence"])[
        [f"{s}_{l}" for s in SPLITS for l in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")]].mean()
    P(leg_tab.to_string(float_format=lambda x: f"{x:.3f}"))
    dump(leg_tab.reset_index(), "legrates.csv")

    # redundancy of the OOS leg under each split rule
    P("\n  REDUNDANCY of the OOS leg: P(all 5) / P(the other 4), by split rule")
    red_rows = []
    for (k, c), gsub in nulls.groupby(["panel", "cadence"]):
        row = dict(panel=k, cadence=c)
        for sp in SPLITS:
            den = gsub[f"p4b_{sp}_noOOS"].mean()
            row[sp] = (gsub[f"p4b_{sp}"].mean() / den) if den > 0 else np.nan
        red_rows.append(row)
    red = pd.DataFrame(red_rows)
    P(red.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(red, "redundancy.csv")

    # ---------------------------------------------------- RULE 8 WALK-FORWARD -----------------
    P("\n" + "-" * 100)
    P("RULE 8 WALK-FORWARD -- (book, gross) chosen on 2009-2016 ALONE, 2017-2026 read ONCE")
    P("-" * 100)
    CH = ["CH_SHARPE", "CH_CAGR", "CH_CALMAR"]
    wf_rows = []
    for k in PANELS:
        q = pans[k]
        spy_oos = fmet(q.spy[q.oos])
        base_oos = fmet(q.base_r[PROTO_COST][q.oos])
        for c in CADENCES:
            cand = []
            for b in BOOKS:
                for g in GROSS_GRID:
                    r = q.ctx[c].run(lag_weights(W[(k, b, g)]), PROTO_COST)[0]
                    ic, is_, idd = fmet(r[q.is_])
                    cand.append((b, g, r, ic, is_, idd))
            for ch in CH:
                if ch == "CH_SHARPE":
                    pick = max(cand, key=lambda x: (-1e9 if np.isnan(x[4]) else x[4]))
                elif ch == "CH_CAGR":
                    pick = max(cand, key=lambda x: (-1e9 if np.isnan(x[3]) else x[3]))
                else:
                    pick = max(cand, key=lambda x: (-1e9 if (np.isnan(x[3]) or x[5] == 0) else x[3] / abs(x[5])))
                b, g, r = pick[0], pick[1], pick[2]
                st = stats_of(q, r)
                row = dict(panel=k, cadence=c, chooser=ch, pick_book=b, pick_gross=g,
                           OOS_CAGR=st["OOS_CAGR"], OOS_Sharpe=st["OOS_Sharpe"], OOS_MaxDD=st["OOS_MaxDD"],
                           SPY_OOS_CAGR=spy_oos[0], SPY_OOS_Sharpe=spy_oos[1], SPY_OOS_MaxDD=spy_oos[2],
                           BASE_OOS_CAGR=base_oos[0], BASE_OOS_Sharpe=base_oos[1], BASE_OOS_MaxDD=base_oos[2])
                for sp in SPLITS:
                    lg = legs_4b(q, st, sp)
                    row[f"p4b_{sp}"] = all(lg.values())
                    row[f"fail_{sp}"] = ",".join(x for x, v in lg.items() if not v) or ""
                    row[f"p4a_{sp}"] = pass_4a(q, r, q.base_r[PROTO_COST], sp)
                wf_rows.append(row)
    wf = pd.DataFrame(wf_rows)
    dump(wf, "walkforward.csv")
    P(wf[["panel", "cadence", "chooser", "pick_book", "pick_gross", "OOS_CAGR", "OOS_Sharpe",
          "OOS_MaxDD", "p4b_REC", "p4b_DISJ", "p4b_TWOLEG", "p4a_REC", "p4a_DISJ"]]
      .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    P("\n  rule-8 OOS pass counts over %d picks:" % len(wf))
    for sp in SPLITS:
        P(f"    {sp:7s}  4b {int(wf[f'p4b_{sp}'].sum()):3d} / {len(wf)}    "
          f"4a {int(wf[f'p4a_{sp}'].sum()):3d} / {len(wf)}")
    best = wf.loc[wf.OOS_Sharpe.idxmax()]
    P(f"\n  best OOS pick: {best.panel}/{best.cadence}/{best.chooser} -> {best.pick_book}@g{best.pick_gross} "
      f"OOS {best.OOS_CAGR:.2%} / {best.OOS_Sharpe:.3f} / {best.OOS_MaxDD:.2%}")
    P(f"    vs SPY OOS   {best.SPY_OOS_CAGR:.2%} / {best.SPY_OOS_Sharpe:.3f} / {best.SPY_OOS_MaxDD:.2%}")
    P(f"    vs RULES v2  {best.BASE_OOS_CAGR:.2%} / {best.BASE_OOS_Sharpe:.3f} / {best.BASE_OOS_MaxDD:.2%}")
    P(f"    4b REC {bool(best.p4b_REC)} / DISJ {bool(best.p4b_DISJ)} / TWOLEG {bool(best.p4b_TWOLEG)}; "
      f"4a REC {bool(best.p4a_REC)} / DISJ {bool(best.p4a_DISJ)}")

    # G6 -- the choosers are IS-only
    q = pans["U56"]
    rng = np.random.default_rng(6)
    px_perm = q.px.copy()
    oos_rows = np.flatnonzero(q.oos)
    vals = px_perm.values.copy()
    perm = rng.permutation(len(oos_rows))
    vals[oos_rows] = vals[oos_rows][perm]
    q2 = Panel("U56perm", pd.DataFrame(vals, index=q.idx, columns=q.px.columns))
    mismatch = 0
    for c in CADENCES:
        picks = {}
        for tag, qq in (("orig", q), ("perm", q2)):
            cand = []
            for b in BOOKS:
                for g in GROSS_GRID:
                    ww = W[("U56", b, g)] if tag == "orig" else build_books(qq.px, g)[0][b]
                    r = qq.ctx[c].run(lag_weights(ww), PROTO_COST)[0]
                    cand.append((b, g, fmet(r[qq.is_])[1]))
            picks[tag] = max(cand, key=lambda x: (-1e9 if np.isnan(x[2]) else x[2]))[:2]
        mismatch += int(picks["orig"] != picks["perm"])
    gates["G6"] = mismatch == 0
    P(f"\n  G6  CH_SHARPE pick invariant to permuted OOS rows on U56, 3 cadences: "
      f"{mismatch} mismatches  [{'PASS' if gates['G6'] else 'FAIL'}]")

    # ------------------------------------------------------------ HYPOTHESES -----------------
    P("\n" + "-" * 100)
    P("PRE-REGISTERED HYPOTHESES")
    P("-" * 100)
    hyp = []
    srow = cen[(cen.claim_set == "STRICT") & (cen.rung == f"{PROTO_COST:.0f}") & (cen.split == "DISJ")] \
        if len(cen) else pd.DataFrame()
    if len(srow):
        rr = srow.iloc[0]
        val = rr.destroyed_share
        hyp.append(("H_DESTROY", f"destroyed {int(rr.destroyed)} of {int(rr.reproduced_REC)} reproduced "
                                 f"committed passes = {val:.3f}", val >= DESTROY_BAR, f">= {DESTROY_BAR}"))
        sym = abs(rr.created - rr.destroyed) / rr.reproduced_REC if rr.reproduced_REC else np.nan
        hyp.append(("H_SYM", f"|created {int(rr.created)} - destroyed {int(rr.destroyed)}| / "
                             f"{int(rr.reproduced_REC)} = {sym:.3f}", sym <= SYM_BAR, f"<= {SYM_BAR}"))
    else:
        hyp.append(("H_DESTROY", "no STRICT rows mapped at the binding rung", False, f">= {DESTROY_BAR}"))
        hyp.append(("H_SYM", "no STRICT rows mapped at the binding rung", False, f"<= {SYM_BAR}"))
    ratios = br["ratio_DISJ_over_REC"].dropna()
    med = float(ratios.median()) if len(ratios) else np.nan
    hyp.append(("H_NULL", f"median base_rate(DISJ)/base_rate(REC) over {len(ratios)} defined cells = {med:.3f}",
                (med <= NULL_RATIO_BAR) if not np.isnan(med) else False, f"<= {NULL_RATIO_BAR}"))
    dd = red["DISJ"].dropna()
    ncells = int((dd <= INDEP_BAR).sum())
    hyp.append(("H_INDEP", f"P(all 5)/P(other 4) <= {INDEP_BAR} under DISJ in {ncells} of "
                           f"{len(dd)} defined cells", ncells >= INDEP_CELLS, f">= {INDEP_CELLS} cells"))
    for name, txt, ok, bar in hyp:
        P(f"  {name:10s} [{'PASS' if ok else 'FAIL'}]  bar {bar:16s}  {txt}")
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

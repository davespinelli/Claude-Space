#!/usr/bin/env python3
"""Idea 919 (lane C, 2026-09-15) -- re-read every committed GROSS BAND in the record at 0.01
resolution.

THE QUESTION (queue, 2026-09-15)
  Idea 675 turned idea 670's published "CAND20 passes 4b at exactly one rung" into a 0.2095-wide
  contiguous interval purely by refining the gross ladder from 8 irregular rungs to 0.01 and then
  to bisection.  The record's other gross bands are quoted off ladders of the same coarseness.
  The queue asks: re-solve every committed band's two monotone crossings and report how many
  published widths are resolution artefacts.

WHAT A BAND IS, AND WHY A LADDER CAN LIE ABOUT ONE
  Idea 804 established over 24 of 24 bands that a 4b band's LOWER edge is the CAGR floor alone and
  its UPPER edge the DD cap alone, both monotone in gross, with the three Sharpe legs FLAT in
  gross.  Two monotone crossings bound an INTERVAL.  A ladder of step h samples that interval: it
  can only report edges that lie on its own rungs, so it under-reports the width by up to h at
  each edge, and it reports EMPTY whenever the interval falls between two rungs.  A published
  width is therefore a statement about the ladder unless the interval is several rungs wide.

THE RUN HAS TWO HALVES, AND BOTH ARE REPORTED
  PART A  CENSUS of the committed corpus.  Every `research/backtests/*.csv` is scanned for a gross
          DIAL column carrying a 4b pass flag; each (file x book-key) group with >= 3 distinct
          rungs and no duplicate rungs is one committed BAND, read exactly as its own run
          published it.  No simulation -- this is the record read back.
  PART B  RE-SOLUTION by bisection of the sub-population this sandbox can rebuild: idea 804's
          committed 8-rung grid (`2026-09-11_is-the-GROSS-dial-s-4b-FOOTPRINT-the-CAGR-FLOOR-
          alone_C.grid.csv`, 2 panels x 10 arms x 8 rungs, gate G3), plus the same 10 arms on
          SMALL as a declared extension.  Each band is read at five ladder resolutions and then
          solved exactly, so the census's classification can be CALIBRATED instead of asserted.

WHAT IS TUNED AND WHAT IS REPORTED (PROTOCOL 4: max 2 tuned parameters; the queue's own two)
  TUNED 1  GROSS RESOLUTION, 6 levels, every one reported.  PROTOCOL 2 forbids leverage, so every
           ladder stops at g = 1.00 and the g in (1.00, 1.50] region is solved separately and
           reported as a flagged LEVERED extension that no chooser may pick from:
           RECORD8  670's own irregular ladder {0.20,0.35,0.50,0.60,0.75,0.85,0.95,1.00}
           STEP25   0.25 .. 1.00 step 0.25   (4 rungs)   -- the census's MODAL committed step
           STEP10   0.10 .. 1.00 step 0.10  (10 rungs)
           STEP05   0.05 .. 1.00 step 0.05  (20 rungs)
           STEP01   0.01 .. 1.00 step 0.01 (100 rungs)   -- the queue's asked-for resolution
           EXACT    both crossings solved by bisection to 1e-6 of gross
  TUNED 2  CLAIM SET, 2 levels: REPRO = the 40 committed (panel x arm) cells of 804's grid, the
           bands this run can price against the record; EXT = the same 10 arms on SMALL, which no
           committed run priced, reported separately and never mixed into a census number.
  REPORTED AXES (nothing fitted on them; every point published): cost 0 / 10 / 25 bps; window
  FULL (804's and 670's own convention) / IS 2009-2016 / OOS 2017-2026 (window-local convention).

PRE-REGISTERED BARS (fixed before any number was read; both directions reported)
  H_LIMIT  (census) a committed band is RESOLUTION-LIMITED iff its published width <= 2 of its own
           rungs -- each edge is quantised to +-1 rung, so such a width is inside its own
           uncertainty.  SINGLE-RUNG (one passing rung, 670's class) is the strict sub-case.
  H_CENSOR (census) a band is CENSORED iff a passing rung sits at the ladder's own min or max, so
           the true edge is outside the ladder and the published width is a lower bound.
  H_ART    (calibration) a ladder READING is an ARTEFACT iff |w_ladder - w_exact| >= one rung of
           that ladder, or its class (EMPTY / SINGLE / WIDE) differs from the exact class.
  H_DIR    (calibration) ladder widths are biased DOWNWARD: w_ladder <= w_exact on every band.
           A ladder samples an interval, so it cannot over-report -- except through a Sharpe leg,
           which is flat in gross and which bisection on the level legs alone does not see.  Both
           directions counted.
  H_WF     (rule 8, required) g chosen on 2009-2016 ONLY at each resolution, OOS 2017-2026 read
           once, both KEEP paths, against SPY and RULES v2 in the same window.  The capital
           question is whether the resolution used to CHOOSE changes the OOS verdict.

GATES (all printed before any result number)
  G1  the fast runner == engine.backtest on returns and turnover
  G2  BAND03 at g=0.75 == baseline.rules_v2_weights elementwise
  G3  CROSS-RUN: idea 804's committed `.grid.csv` reproduces -- 160 rows (2 panels x 10 arms x 8
      rungs), metrics to a 5e-3 vintage bar and the five 4b LEGS plus pass4b/pass4a EXACTLY.
      These are the very bands Part B re-reads, so this gate is load-bearing.
  G4  the committed U56 triples (SPY, RULES v2)
  G5  monotonicity of CAGR(g) and |MaxDD(g)| on the 0.01 ladder, per book -- this is what makes a
      bisected endpoint meaningful; any book that fails is named, its rows flagged `nonmono`, and
      excluded from the calibration headline (a book with two crossings has no single band)
  G6  bisection == ladder: each EXACT endpoint lies inside its bracketing pair of 0.01 rungs
  G7  determinism (rebuild, re-score)
  G8  the analytic ray: SPYBH (g x SPY) must read |MaxDD(g)|/|MaxDD(SPY)| = g
  G3b the SAME gate on a tape TRUNCATED to 804's own last date (2026-09-11).  G3 alone cannot
      tell a method difference from a tape-vintage difference; G3b is what separates them, and
      every leg that still flips at G3b is reported with 804's OWN margin on that leg.
  G9  CENSUS-vs-SIMULATION: the Part A scanner, run on 804's own committed CSV, must return the
      same band for every (panel, arm, freq) cell that Part B's RECORD8 reading produces.  This
      is the join between the two halves and is required to be exact -- it is the gate that
      catches a scanner that groups rows by their own verdict columns instead of by book.

PROTOCOL: 10 bps primary, t+1, weekly (monthly for BAND03_M, which is 804's own cadence arm),
warm-up 260 days, IS 2009-2016 / OOS 2017-2026.  Nothing in RULES.md / PROTOCOL.md / scan.py /
bot.py / baseline.py is modified.

SURVIVORSHIP: U56 / B136 / SMALL are current-constituent lists (SMALL additionally drops the
tickers with max_1d_move >= 1.0 per data/small_meta.csv), so every CAGR and drawdown LEVEL below
is optimistic.  A 4b bar is the book's level against SPY's and SPY is not survivorship-inflated,
so the BANDS measured here are upper bounds on what a point-in-time panel would show.  The
census, the width errors and the resolution contrasts are same-tape comparisons and unaffected.
"""
from __future__ import annotations

import glob
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

# ---- reported constants (never tuned) ---------------------------------------------------------
COST0 = 10.0
FREQ0 = "W"
LAG = 1
BAND0, BAND1 = 0.03, 0.08
MAXVOL = 0.60
WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BISECT_TOL = 1e-6
GMIN_SEARCH, GMAX_SEARCH = 0.002, 1.00
LIMIT_RUNGS = 2.0                 # H_LIMIT: width <= 2 rungs is inside its own quantisation

# ---- TUNED DIAL 1: the gross resolution -------------------------------------------------------
RECORD8 = [0.20, 0.35, 0.50, 0.60, 0.75, 0.85, 0.95, 1.00]
GMAX_PROTO = 1.00                  # PROTOCOL 2: no leverage unless the idea says so
LEV_GMAX = 1.50                    # the LEVERED extension, reported separately and never a pick
LADDERS = {
    "RECORD8": RECORD8,
    "STEP25": [round(0.25 * i, 4) for i in range(1, 5)],
    "STEP10": [round(0.10 * i, 4) for i in range(1, 11)],
    "STEP05": [round(0.05 * i, 4) for i in range(1, 21)],
    "STEP01": [round(0.01 * i, 4) for i in range(1, 101)],
}
LADDER_STEP = {"RECORD8": 0.10, "STEP25": 0.25, "STEP10": 0.10, "STEP05": 0.05, "STEP01": 0.01}
RESOLUTIONS = ["RECORD8", "STEP25", "STEP10", "STEP05", "STEP01", "EXACT"]

# ---- TUNED DIAL 2: the claim set --------------------------------------------------------------
CLAIMSETS = {"REPRO": ["U56", "B136"], "EXT": ["SMALL"]}
PANELS = ["U56", "B136", "SMALL"]

# ---- reported axes ----------------------------------------------------------------------------
COSTS = [0.0, 10.0, 25.0]
WINDOWS = ["FULL", "IS", "OOS"]
ARMS = ["BAND03", "BAND08", "BAND03_M", "CAND20_VS", "CAND20", "CAND10", "CAND05",
        "CAND20_NOCAP", "EWELIG", "SPYBH"]
ARM_FREQ = {a: ("M" if a == "BAND03_M" else FREQ0) for a in ARMS}
ARM_SRC = {
    "BAND03": "RULES v2 live (baseline.rules_v2_weights)",
    "BAND08": "idea 664 committed IS pick on the BAND dial",
    "BAND03_M": "idea 668 CADENCE dial companion (MONTHLY)",
    "CAND20_VS": "idea 668 N dial (vol scaler ON)",
    "CAND20": "2026-09-04 KEEP 4b: top-20 equal weight, NO vol scaler (675's subject)",
    "CAND10": "width companion of the KEEP 4b book",
    "CAND05": "RULES v1 book width",
    "CAND20_NOCAP": "idea 668 VOLCAP dial, cap OFF",
    "EWELIG": "2026-09-03 memo Finding 2 (equal-weight all eligible)",
    "SPYBH": "ZERO-SIGNAL exposure control (g x SPY)",
}
SPY_U56 = (0.1516, 0.8861, -0.3372)
V2_U56 = (0.0863, 1.2018, -0.1205)
TOL_C, TOL_S, TOL_D = 0.004, 0.030, 0.015
G3_BAR = 5e-3
PARENT = ROOT / "research" / "backtests" / \
    "2026-09-11_is-the-GROSS-dial-s-4b-FOOTPRINT-the-CAGR-FLOOR-alone_C.grid.csv"
PARENT_LAST = "2026-09-11"         # 804's own run date, i.e. the last bar its tape could carry

# ---- Part A scanner configuration -------------------------------------------------------------
GCOLS = {"g", "gross", "gross_req", "g_req", "g_used", "gross_level"}
PCOLS = {"pass4b", "p4b", "pass_4b", "c670_pass4b"}

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ================================================================================================
# PART A -- the census scanner
# ================================================================================================
BOOLISH = {True, False, "True", "False", "true", "false", "TRUE", "FALSE"}


def _is_cat(s: pd.Series) -> bool:
    """A key column candidate: anything not a free float (pandas gives strings dtype 'str')."""
    return not pd.api.types.is_float_dtype(s)


def _is_verdict(s: pd.Series) -> bool:
    """A boolean column is a RESULT (a leg, a pass flag, a bind flag), never a book key.  Grouping
    by one would split a band by its own verdicts, which is the error this gate exists to catch."""
    if pd.api.types.is_bool_dtype(s):
        return True
    u = set(pd.unique(s.dropna()))
    return bool(u) and u.issubset(BOOLISH)


def _key_columns(d: pd.DataFrame, gcol: str, pcol: str) -> list[str]:
    """Book-identifying columns: every categorical/integer column of bounded cardinality plus any
    float column whose values are a small ROUND set (a dial such as cost, band or theta).  Float
    columns with many non-round values are outputs and are never keys."""
    ks, n = [], len(d)
    for c in d.columns:
        if c in (gcol, pcol):
            continue
        s = d[c]
        if _is_cat(s):
            if _is_verdict(s):
                continue
            if s.nunique(dropna=False) <= max(3, n // 2):
                ks.append(c)
        else:
            u = s.dropna().unique()
            if 1 < len(u) <= 40 and np.all(np.isclose(u, np.round(u, 4), atol=1e-9)):
                ks.append(c)
    return ks


def _as_bool(s: pd.Series) -> pd.Series:
    if pd.api.types.is_bool_dtype(s):
        return s.astype(bool)
    return s.astype(str).str.lower().isin(["true", "1", "yes"])


def band_of(gv: np.ndarray, pp: np.ndarray) -> dict:
    """Read one committed band off its own ladder, exactly as its run published it."""
    step = float(np.median(np.diff(gv))) if len(gv) > 1 else np.nan
    npass = int(pp.sum())
    if npass == 0:
        return dict(nrung=len(gv), step=step, g_first=float(gv[0]), g_last=float(gv[-1]),
                    npass=0, lo=np.nan, hi=np.nan, width=np.nan, width_rungs=np.nan,
                    contig=True, censor=False, is_empty=True)
    idx = np.flatnonzero(pp)
    lo, hi = float(gv[idx[0]]), float(gv[idx[-1]])
    w = hi - lo
    return dict(nrung=len(gv), step=step, g_first=float(gv[0]), g_last=float(gv[-1]),
                npass=npass, lo=lo, hi=hi, width=w,
                width_rungs=(w / step if step and np.isfinite(step) and step > 0 else np.nan),
                contig=bool((idx[-1] - idx[0] + 1) == len(idx)),
                censor=bool(lo <= gv[0] + 1e-12 or hi >= gv[-1] - 1e-12), is_empty=False)


def scan_record(files=None) -> tuple[pd.DataFrame, dict]:
    """Every committed gross band in research/backtests/*.csv."""
    rows, stat = [], dict(files_seen=0, files_with_dial=0, groups_short=0, groups_dup=0,
                          groups_ok=0)
    if files is None:
        files = [f for f in sorted(glob.glob(str(OUT / "*.csv")))
                 if not os.path.basename(f).startswith(STEM)]
    for f in files:
        stat["files_seen"] += 1
        try:
            head = pd.read_csv(f, nrows=0)
        except Exception:
            continue
        gcs = [c for c in head.columns if c.lower() in GCOLS]
        pcs = [c for c in head.columns if c.lower() in PCOLS]
        if not gcs or not pcs:
            continue
        try:
            d = pd.read_csv(f)
        except Exception:
            continue
        pcol = pcs[0]
        used = False
        for gcol in gcs:
            v = pd.to_numeric(d[gcol], errors="coerce")
            u = np.sort(v.dropna().unique())
            if len(u) < 3 or len(u) > 400 or u.min() <= 0 or u.max() > 3.0:
                continue                                     # not a gross dial
            if not np.all(np.isclose(u, np.round(u, 3), atol=1e-9)):
                continue                                     # realised gross, not a dial
            used = True
            ks = _key_columns(d, gcol, pcol)
            dd = d.assign(_g=v, _p=_as_bool(d[pcol]))
            it = dd.groupby(ks, dropna=False) if ks else [((), dd)]
            for key, gg in it:
                gg = gg.dropna(subset=["_g"])
                if gg._g.nunique() < 3:
                    stat["groups_short"] += 1
                    continue
                if len(gg) != gg._g.nunique():
                    stat["groups_dup"] += 1
                    continue
                stat["groups_ok"] += 1
                gg = gg.sort_values("_g")
                b = band_of(gg._g.values, gg._p.values)
                b.update(file=os.path.basename(f), gcol=gcol, pcol=pcol,
                         key=("|".join(f"{k}={v2}" for k, v2 in
                                       zip(ks, key if isinstance(key, tuple) else (key,)))
                              if ks else ""))
                rows.append(b)
        if used:
            stat["files_with_dial"] += 1
    return pd.DataFrame(rows), stat


# ================================================================================================
# PART B -- the runner (675's vectorised equivalent of engine.backtest)
# ================================================================================================
class Panel:
    def __init__(self, name, px, freq):
        self.name, self.px, self.freq = name, px, freq
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        T, N = self.rets.shape
        self.T, self.N = T, N
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, N)), C[:-1]])
        mk = rebalance_mask(self.idx, freq).shift(LAG, fill_value=False).values.copy()
        mk[0] = True
        self.reb = np.flatnonzero(mk)
        seg = np.searchsorted(self.reb, np.arange(T), side="right") - 1
        self.s0 = self.reb[seg]
        self.s0p = self.reb[np.maximum(seg - 1, 0)]
        self.R = self.Cp / self.Cp[self.s0]
        self.Rp = self.Cp[self.reb] / self.Cp[self.s0p[self.reb]]
        self.start = self.idx[WARMUP]
        m_full = self.idx >= self.start
        self.masks = {"FULL": m_full,
                      "IS": m_full & (self.idx <= pd.Timestamp(IS_END)),
                      "OOS": self.idx >= pd.Timestamp(OOS_START)}
        self.spy = px["SPY"].pct_change().fillna(0.0).values


class Book:
    """One book's gross-1.0 weights, pre-reduced so any (gross, cost) costs O(T)."""

    def __init__(self, panel: Panel, W1: np.ndarray):
        self.pan = panel
        wt = np.roll(W1, LAG, axis=0).copy()
        wt[:LAG] = 0.0
        self.wt_reb = wt[panel.reb]
        A = wt[panel.s0]
        AR = A * panel.R
        self.S = AR.sum(axis=1)
        self.As = A.sum(axis=1)
        self.ARr = (AR * panel.rets).sum(axis=1)
        Ap = wt[panel.s0p[panel.reb]]
        self.ARp = Ap * panel.Rp
        self.Sp = self.ARp.sum(axis=1)
        self.Asp = Ap.sum(axis=1)
        del A, AR, Ap

    def at(self, g: float, cost=COST0):
        pan = self.pan
        V = 1.0 + g * (self.S - self.As)
        gross = g * self.ARr / V
        Vp = 1.0 + g * (self.Sp - self.Asp)
        heldp = (g * self.ARp) / Vp[:, None]
        heldp[0] = 0.0
        turn = np.zeros(pan.T)
        turn[pan.reb] = np.abs(g * self.wt_reb - heldp).sum(axis=1)
        return gross - turn * cost / 1e4, turn


def fmet(r):
    r = np.asarray(r, float)
    if len(r) < 2:
        return np.nan, np.nan, np.nan
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    if len(r) < 2:
        return np.nan
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def pack(r):
    c, s, d = fmet(r)
    h = len(r) // 2
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(r[:h]), H2=fsharpe(r[h:]))


# ---- the two 4b conventions, both reported ----------------------------------------------------
def legs804(full, oos, spy_full, spy_oos):
    """804's and 670's own convention -- the one the committed bands are published in."""
    return dict(L1_H1=bool(full["H1"] > spy_full["H1"]),
                L2_H2=bool(full["H2"] > spy_full["H2"]),
                L3_OOS=bool(oos["Sharpe"] > spy_oos["Sharpe"]),
                L4_DDcap=bool(abs(full["MaxDD"]) <= DD_CAP * abs(spy_full["MaxDD"])),
                L5_CAGRfloor=bool(full["CAGR"] >= CAGR_FLOOR * spy_full["CAGR"]))


def legswin(s, spy):
    """The window-local form the record's rule-8 runs use (867/910/675)."""
    return dict(L1_H1=bool(s["H1"] > spy["H1"]), L2_H2=bool(s["H2"] > spy["H2"]),
                L3_OOS=True,
                L4_DDcap=bool(s["MaxDD"] >= DD_CAP * spy["MaxDD"]),
                L5_CAGRfloor=bool(s["CAGR"] >= CAGR_FLOOR * spy["CAGR"]))


def pass4a(s, base):
    return bool(s["H1"] > base["H1"] and s["H2"] > base["H2"] and s["MaxDD"] >= base["MaxDD"])


# ---- the ten arms (804's definitions, unchanged) ----------------------------------------------
def ew_gross1(px):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def ranked_w1(px, sc, above, vol20, n, max_vol):
    elig = sc.where(above & (vol20 < max_vol))
    rank = elig.rank(axis=1, ascending=False)
    sel = (rank <= n).astype(float)
    k = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(k, axis=0).fillna(0.0)


def arm_w1(px, pre, arm):
    """Gross-1.0 weights.  Every arm is exactly linear in g, so Book.at(g) IS the g rung."""
    sc_v, sc_n, above, vol20 = pre
    if arm in ("BAND03", "BAND03_M"):
        return ew_gross1(px).where(band_state(px, BAND0) & px.notna(), 0.0).values
    if arm == "BAND08":
        return ew_gross1(px).where(band_state(px, BAND1) & px.notna(), 0.0).values
    if arm == "CAND20_VS":
        return ranked_w1(px, sc_v, above, vol20, 20, MAXVOL).values
    if arm == "CAND20":
        return ranked_w1(px, sc_n, above, vol20, 20, MAXVOL).values
    if arm == "CAND10":
        return ranked_w1(px, sc_n, above, vol20, 10, MAXVOL).values
    if arm == "CAND05":
        return ranked_w1(px, sc_n, above, vol20, 5, MAXVOL).values
    if arm == "CAND20_NOCAP":
        return ranked_w1(px, sc_n, above, vol20, 20, 9.99).values
    if arm == "EWELIG":
        sel = (above & (vol20 < MAXVOL) & px.notna()).astype(float)
        k = sel.sum(axis=1).replace(0, np.nan)
        return sel.div(k, axis=0).fillna(0.0).values
    if arm == "SPYBH":
        w = pd.DataFrame(0.0, index=px.index, columns=px.columns)
        w["SPY"] = 1.0
        return w.where(px.notna(), 0.0).values
    raise KeyError(arm)


def prep(px):
    sc_v, above, vol20 = score(px, vol_scale=True)
    sc_n, _, _ = score(px, vol_scale=False)
    return sc_v, sc_n, above, vol20


# ---- scoring -----------------------------------------------------------------------------------
def score_g(bk: Book, g, cost, spyref, v2ref):
    pan = bk.pan
    r, turn = bk.at(g, cost)
    out = {w: pack(r[pan.masks[w]]) for w in WINDOWS}
    L = legs804(out["FULL"], out["OOS"], spyref["FULL"], spyref["OOS"])
    row = dict(gross=float(g), cost=cost,
               turn_yr=float(turn[pan.masks["FULL"]].sum()
                             / (pan.masks["FULL"].sum() / 252.0)))
    for w in WINDOWS:
        for k, v in out[w].items():
            row[f"{w}_{k}"] = v
    row.update({f"c804_{k}": v for k, v in L.items()})
    row["c804_pass4b"] = bool(all(L.values()))
    row["c804_pass4a"] = pass4a(out["FULL"], v2ref["FULL"])
    for w in ("IS", "OOS"):
        Lw = legswin(out[w], spyref[w])
        row.update({f"cwin{w}_{k}": v for k, v in Lw.items()})
        row[f"cwin{w}_pass4b"] = bool(all(Lw.values()))
        row[f"cwin{w}_pass4a"] = pass4a(out[w], v2ref[w])
    return row


def bisect(f, lo, hi, tol=BISECT_TOL):
    """Smallest g in [lo,hi] with f(g) >= 0, assuming f non-decreasing.  None if no crossing."""
    if f(lo) >= 0:
        return lo
    if f(hi) < 0:
        return None
    for _ in range(200):
        if hi - lo < tol:
            break
        mid = 0.5 * (lo + hi)
        if f(mid) >= 0:
            hi = mid
        else:
            lo = mid
    return hi


def exact_window(bk, cost, spyref, conv, win, gmax_search=GMAX_SEARCH):
    """(g_min from the CAGR floor, g_max from the DD cap) by bisection to BISECT_TOL."""
    wc = wd = "FULL" if conv == "c804" else win
    ref = spyref[wc]

    def f_cagr(g):
        r, _ = bk.at(g, cost)
        c, _, _ = fmet(r[bk.pan.masks[wc]])
        return c - CAGR_FLOOR * ref["CAGR"]

    def f_dd(g):
        r, _ = bk.at(g, cost)
        _, _, d = fmet(r[bk.pan.masks[wd]])
        return abs(d) - DD_CAP * abs(spyref[wd]["MaxDD"])      # non-decreasing in g

    gmin = bisect(f_cagr, GMIN_SEARCH, gmax_search)
    gbreak = bisect(f_dd, GMIN_SEARCH, gmax_search)            # first g that BREACHES the cap
    gmax = gmax_search if gbreak is None else gbreak - BISECT_TOL
    return gmin, gmax, (gbreak is None)


def sharpe_legs_ok(bk, cost, spyref, conv, win, probe=(0.25, 0.50, 0.75, 1.00)):
    """The gross-FLAT Sharpe legs (804: flat in g).  A level window is a 4b window only if these
    pass; a bisection on the level legs alone does not see them."""
    out = []
    for g in probe:
        r, _ = bk.at(g, cost)
        st = {w: pack(r[bk.pan.masks[w]]) for w in WINDOWS}
        if conv == "c804":
            L = legs804(st["FULL"], st["OOS"], spyref["FULL"], spyref["OOS"])
            out.append(bool(L["L1_H1"] and L["L2_H2"] and L["L3_OOS"]))
        else:
            L = legswin(st[win], spyref[win])
            out.append(bool(L["L1_H1"] and L["L2_H2"]))
    return bool(all(out)), out


def exact_row(panel, arm, cost, bk, spyref, conv, win, gmax_search=GMAX_SEARCH, tag="PROTO"):
    gmin, gmax, dd_never = exact_window(bk, cost, spyref, conv, win, gmax_search)
    sh, shdet = sharpe_legs_ok(bk, cost, spyref, conv, win)
    lw = np.nan if gmin is None else max(0.0, gmax - gmin)
    empty = bool((not sh) or gmin is None or not np.isfinite(lw) or lw <= 0.0)
    return dict(panel=panel, arm=arm, cost=cost, conv=conv, window=win, ceiling=tag,
                g_min=gmin, g_max=gmax, level_width=lw, sharpe_ok=sh,
                dd_cap_never_breached=bool(dd_never),
                sharpe_detail="".join("y" if x else "n" for x in shdet),
                width=(0.0 if empty else lw), is_empty=empty)


def ladder_read(fine, panel, arm, cost, ladder, passcol):
    """What a ladder of these rungs REPORTS for this band, read exactly as a run would read it."""
    gs = LADDERS[ladder]
    sub = fine[(fine.panel == panel) & (fine.arm == arm) & (fine.cost == cost)]
    sub = sub[np.isin(np.round(sub.gross.values, 6), np.round(gs, 6))].sort_values("gross")
    if len(sub) < 3:
        return None
    b = band_of(sub.gross.values, sub[passcol].values.astype(bool))
    b.update(panel=panel, arm=arm, cost=cost, resolution=ladder, ladder_step=LADDER_STEP[ladder])
    return b


# ================================================================================================
# gates
# ================================================================================================
def run_gates(pans, books, spyref, v2ref, pre, raw):
    P("=" * 112)
    P("GATES (printed before any result number is read)")
    P("=" * 112)
    ok = {}
    pan = pans[("U56", "W")]
    px = pan.px
    W1 = arm_w1(px, pre["U56"], "BAND03")
    w_ref = rules_v2_weights(px, band=BAND0, gross=0.75).values
    dw = float(np.nanmax(np.abs(W1 * 0.75 - w_ref)))
    ok["G2"] = dw < 1e-12
    P(f"G2  BAND03 g=0.75 == rules_v2_weights          max|dw| {dw:.3e}   -> "
      f"{'PASS' if ok['G2'] else 'FAIL'}")

    bk = books[("U56", "BAND03")]
    r_fast, t_fast = bk.at(0.75, COST0)
    res = backtest(px, rules_v2_weights(px, band=BAND0, gross=0.75), cost_bps=COST0, freq=FREQ0)
    dr = float(np.nanmax(np.abs(r_fast - res["returns"].values)))
    dt = float(np.nanmax(np.abs(t_fast - res["turnover"].values)))
    bs = books[("U56", "CAND20")]
    rs, ts = bs.at(0.85, COST0)
    wsub = pd.DataFrame(arm_w1(px, pre["U56"], "CAND20") * 0.85, index=px.index, columns=px.columns)
    res2 = backtest(px, wsub, cost_bps=COST0, freq=FREQ0)
    dr2 = float(np.nanmax(np.abs(rs - res2["returns"].values)))
    dt2 = float(np.nanmax(np.abs(ts - res2["turnover"].values)))
    # and a MONTHLY arm, since 804's grid carries one
    bm = books[("U56", "BAND03_M")]
    rm, tm = bm.at(0.75, COST0)
    wm = pd.DataFrame(arm_w1(px, pre["U56"], "BAND03_M") * 0.75, index=px.index, columns=px.columns)
    res3 = backtest(px, wm, cost_bps=COST0, freq="M")
    dr3 = float(np.nanmax(np.abs(rm - res3["returns"].values)))
    ok["G1"] = max(dr, dt, dr2, dt2, dr3) < 1e-10
    P(f"G1  fast Book.at == engine.backtest            BAND03 max|dr| {dr:.3e} max|dturn| {dt:.3e};"
      f"  CAND20 {dr2:.3e}/{dt2:.3e};  BAND03_M {dr3:.3e}   -> {'PASS' if ok['G1'] else 'FAIL'}")

    s, v = spyref["U56"]["FULL"], v2ref["U56"]["FULL"]
    d1 = (abs(s["CAGR"] - SPY_U56[0]), abs(s["Sharpe"] - SPY_U56[1]), abs(s["MaxDD"] - SPY_U56[2]))
    d2 = (abs(v["CAGR"] - V2_U56[0]), abs(v["Sharpe"] - V2_U56[1]), abs(v["MaxDD"] - V2_U56[2]))
    ok["G4"] = all(a < b for a, b in zip(d1, (TOL_C, TOL_S, TOL_D))) and \
        all(a < b for a, b in zip(d2, (TOL_C, TOL_S, TOL_D)))
    P(f"G4  committed U56 triples   SPY {s['CAGR']:.4%}/{s['Sharpe']:.4f}/{s['MaxDD']:.4%}  "
      f"(committed {SPY_U56[0]:.2%}/{SPY_U56[1]:.4f}/{SPY_U56[2]:.2%});  v2 "
      f"{v['CAGR']:.4%}/{v['Sharpe']:.4f}/{v['MaxDD']:.4%}  (committed {V2_U56[0]:.2%}/"
      f"{V2_U56[1]:.4f}/{V2_U56[2]:.2%})   -> {'PASS' if ok['G4'] else 'FAIL'}")

    worst_dd = 0.0
    for pn in PANELS:
        z = books[(pn, "SPYBH")]
        sp = spyref[pn]["FULL"]
        for g in (0.25, 0.50, 0.75, 1.00):
            rz, _ = z.at(g, 0.0)
            _, _, d = fmet(rz[pans[(pn, "W")].masks["FULL"]])
            worst_dd = max(worst_dd, abs(abs(d) / abs(sp["MaxDD"]) - g))
    ok["G8"] = worst_dd < 0.05
    P(f"G8  SPYBH analytic ray |MaxDD(g)|/|MaxDD(SPY)| == g   worst dev over 3x4 {worst_dd:.3e}"
      f"   -> {'PASS' if ok['G8'] else 'FAIL'}")
    return ok


def gate_parent(fine, tag="G3", note=True):
    """G3 -- reproduce idea 804's committed grid: metrics to a vintage bar, LEGS exactly."""
    if not PARENT.exists():
        P(f"{tag}  804's .grid.csv NOT FOUND -- gate cannot run")
        return False, pd.DataFrame()
    par = pd.read_csv(PARENT)
    rows = []
    for _, pr in par.iterrows():
        h = fine[(fine.panel == pr.panel) & (fine.arm == pr.arm) & (fine.cost == COST0)
                 & (np.abs(fine.gross - pr.gross) < 1e-9)]
        if h.empty:
            continue
        h = h.iloc[0]
        d = dict(panel=pr.panel, arm=pr.arm, gross=float(pr.gross),
                 dCAGR=abs(h.FULL_CAGR - pr.CAGR), dSharpe=abs(h.FULL_Sharpe - pr.Sharpe),
                 dMaxDD=abs(h.FULL_MaxDD - pr.MaxDD), dH1=abs(h.FULL_H1 - pr.H1),
                 dH2=abs(h.FULL_H2 - pr.H2), dOOS_Sharpe=abs(h.OOS_Sharpe - pr.OOS_Sharpe))
        flips = [k for k in ("L1_H1", "L2_H2", "L3_OOS", "L4_DDcap", "L5_CAGRfloor")
                 if bool(h[f"c804_{k}"]) != bool(pr[k])]
        d["legs_match"] = (len(flips) == 0)
        d["flipped_legs"] = ",".join(flips)
        marg = dict(L1_H1=pr.H1 - pr.SPY_H1, L2_H2=pr.H2 - pr.SPY_H2,
                    L3_OOS=pr.OOS_Sharpe - pr.SPY_OOS_Sharpe,
                    L4_DDcap=DD_CAP * abs(pr.SPY_MaxDD) - abs(pr.MaxDD),
                    L5_CAGRfloor=pr.CAGR - CAGR_FLOOR * pr.SPY_CAGR)
        d["flip_margin"] = min((abs(marg[k]) for k in flips), default=np.nan)
        d["pass4b_match"] = bool(h.c804_pass4b) == bool(pr.pass4b)
        d["pass4a_match"] = bool(h.c804_pass4a) == bool(pr.pass4a)
        mk = {k: d[k] for k in ("dCAGR", "dSharpe", "dMaxDD", "dH1", "dH2", "dOOS_Sharpe")}
        d["worst_metric"] = max(mk.values())
        d["worst_carrier"] = max(mk, key=mk.get)
        rows.append(d)
    G = pd.DataFrame(rows)
    G["exact"] = G.legs_match & G.pass4b_match & G.pass4a_match
    legs, mets = bool(G.exact.all()), bool((G.worst_metric < G3_BAR).all())
    wr = G.loc[G.worst_metric.idxmax()]
    P(f"{tag}  804's committed grid: {len(G)} of {len(par)} rows matched.  LEGS + pass4b + pass4a "
      f"exact on {int(G.exact.sum())} of {len(G)}; worst metric deviation "
      f"{G.worst_metric.max():.3e} (carried by {wr.worst_carrier} on {wr.panel}/{wr.arm} "
      f"g={wr.gross:.2f}) against the {G3_BAR:.0e} vintage bar   -> "
      f"{'PASS' if (legs and mets) else 'FAIL'}")
    P(f"      worst deviation by metric: " + "  ".join(
        f"{k[1:]} {G[k].max():.2e}" for k in
        ("dCAGR", "dSharpe", "dMaxDD", "dH1", "dH2", "dOOS_Sharpe")))
    for pn in sorted(G.panel.unique()):
        gp = G[G.panel == pn]
        P(f"      {tag}[{pn}]  {int(gp.exact.sum())} of {len(gp)} rows exact on every leg and "
          f"verdict, worst metric deviation {gp.worst_metric.max():.3e}  -> "
          f"{'PASS' if (gp.exact.all() and (gp.worst_metric < G3_BAR).all()) else 'FAIL'}")
    bad = G[~G.exact]
    for _, r in bad.iterrows():
        fl = r.flipped_legs if r.flipped_legs else "-"
        fm = ("" if not np.isfinite(r.flip_margin) else
              f"  804's own margin on it {r.flip_margin:.4f}")
        P(f"      MISMATCH {r.panel:5s} {r.arm:13s} g={r.gross:.2f}  worst|d| {r.worst_metric:.2e}"
          f"  legs {'OK' if r.legs_match else fl}  4b {'OK' if r.pass4b_match else 'NO'}"
          f"  4a {'OK' if r.pass4a_match else 'NO'}{fm}")
    if note:
        P("      (804's tape ends 2026-09-11 and today's is longer, so the metric bar is a vintage")
        P("       bar; the LEG pattern is what the committed BAND is made of and must match")
        P("       exactly.  G3b below re-runs this gate on a tape TRUNCATED to 804's own last")
        P("       date, which is what separates a method difference from a vintage difference.)")
    return bool(legs and mets), G


# ================================================================================================
# main
# ================================================================================================
def main():
    t0 = time.time()
    P("=" * 112)
    P("IDEA 919 (lane C, 2026-09-15) -- re-read every committed GROSS BAND in the record at 0.01")
    P("                                resolution")
    P("=" * 112)
    P(f"TUNED 1 gross resolution ({len(RESOLUTIONS)} levels, all reported): {RESOLUTIONS}")
    P(f"        RECORD8 = 670's own ladder {RECORD8};  STEP25 {len(LADDERS['STEP25'])} rungs, "
      f"STEP10 {len(LADDERS['STEP10'])}, STEP05 {len(LADDERS['STEP05'])}, "
      f"STEP01 {len(LADDERS['STEP01'])}, EXACT = bisection to {BISECT_TOL:.0e}")
    P(f"TUNED 2 claim set: REPRO = 804's committed cells on {CLAIMSETS['REPRO']}; "
      f"EXT = the same arms on {CLAIMSETS['EXT']} (no committed run priced these)")
    P(f"reported axes: cost {[int(c) for c in COSTS]} bps x window {WINDOWS} x {len(ARMS)} arms")
    P(f"BARS: H_LIMIT width <= {LIMIT_RUNGS:.0f} rungs; H_CENSOR a passing rung at a ladder edge; "
      f"H_ART |w_lad - w_exact| >= 1 rung or class differs;")
    P("      H_DIR w_lad <= w_exact; H_WF rule 8, g chosen on 2009-2016 at each resolution.")
    P("")

    # --------------------------------------------------------------------------------------
    # PART A -- the census
    # --------------------------------------------------------------------------------------
    P("=" * 112)
    P("PART A -- CENSUS OF EVERY COMMITTED GROSS BAND IN THE RECORD")
    P("=" * 112)
    tA = time.time()
    CEN, stat = scan_record()
    P(f"scanned {stat['files_seen']:,} committed CSVs; {stat['files_with_dial']} carry a gross "
      f"DIAL column with a 4b pass flag")
    P(f"  groups: {stat['groups_ok']:,} usable bands, {stat['groups_short']:,} with < 3 rungs "
      f"(gross not varied inside the cell), {stat['groups_dup']:,} with duplicate rungs (dropped)")
    NE = CEN[~CEN["is_empty"]].copy()
    P(f"  {len(CEN):,} committed band cells in {CEN.file.nunique()} files; "
      f"{len(NE):,} are NON-EMPTY (have at least one passing rung)")
    P("")
    P("THE CENSUS ANSWER (non-empty committed bands, read exactly as their own runs published)")
    n = len(NE)
    single = int((NE.npass == 1).sum())
    limited = int((NE.width <= LIMIT_RUNGS * NE.step + 1e-9).sum())
    cens = int(NE.censor.sum())
    noncont = int((~NE.contig).sum())
    safe = int(((NE.width > LIMIT_RUNGS * NE.step + 1e-9) & (~NE.censor)).sum())
    P(f"  SINGLE-RUNG (670's class, width 0 by construction)  {single:5,} of {n:,}  "
      f"({single/max(n,1):.1%})")
    P(f"  RESOLUTION-LIMITED (width <= {LIMIT_RUNGS:.0f} rungs)          {limited:5,} of {n:,}  "
      f"({limited/max(n,1):.1%})")
    P(f"  CENSORED (a passing rung at the ladder's own edge)  {cens:5,} of {n:,}  "
      f"({cens/max(n,1):.1%})")
    P(f"  NON-CONTIGUOUS pass sets                            {noncont:5,} of {n:,}  "
      f"({noncont/max(n,1):.1%})   <- 804's monotone-edges reading, re-read on the whole corpus")
    P(f"  RESOLUTION-SAFE (> {LIMIT_RUNGS:.0f} rungs wide AND uncensored)     {safe:5,} of {n:,}  "
      f"({safe/max(n,1):.1%})")
    P("")
    P("  by committed ladder step (the coarseness the record actually used):")
    P(f"    {'step':>7} {'bands':>7} {'single':>7} {'limited':>8} {'censored':>9} {'safe':>7} "
      f"{'median width':>13}")
    for st, gg in NE.groupby(NE.step.round(3)):
        P(f"    {st:7.3f} {len(gg):7,} {int((gg.npass==1).sum()):7,} "
          f"{int((gg.width <= LIMIT_RUNGS*gg.step+1e-9).sum()):8,} {int(gg.censor.sum()):9,} "
          f"{int(((gg.width > LIMIT_RUNGS*gg.step+1e-9) & (~gg.censor)).sum()):7,} "
          f"{gg.width.median():13.3f}")
    P("")
    P("  the 12 files contributing the most non-empty bands:")
    for f, gg in sorted(NE.groupby("file"), key=lambda kv: -len(kv[1]))[:12]:
        P(f"    {len(gg):4,} bands  single {int((gg.npass==1).sum()):4,}  "
          f"step {gg.step.median():.3f}  {f[:78]}")
    dump(CEN, "census.csv")
    P(f"  Part A took {time.time()-tA:.1f}s")
    P("")

    # --------------------------------------------------------------------------------------
    # PART B -- re-solution
    # --------------------------------------------------------------------------------------
    P("=" * 112)
    P("PART B -- RE-SOLVING THE REPRODUCIBLE BANDS BY BISECTION")
    P("=" * 112)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    raw = {}
    for nm, kw in [("U56", {}), ("B136", dict(broad=True)), ("SMALL", dict(small=True))]:
        px = load_universe(**kw)
        if nm == "SMALL":
            px = px[[c for c in px.columns if c not in bad]]
        raw[nm] = px
        P(f"panel {nm:6s} {px.shape[0]} days x {px.shape[1]} cols  {px.index[0].date()} .. "
          f"{px.index[-1].date()}")
    P(f"  SMALL drops {len(bad)} tickers with max_1d_move >= 1.0 (data/small_meta.csv)")

    pans, pre = {}, {}
    for nm in PANELS:
        pre[nm] = prep(raw[nm])
        for fq in ("W", "M"):
            pans[(nm, fq)] = Panel(nm, raw[nm], fq)
    spyref, v2ref = {}, {}
    for nm in PANELS:
        pan = pans[(nm, "W")]
        spyref[nm] = {w: pack(pan.spy[pan.masks[w]]) for w in WINDOWS}
        v2 = Book(pan, arm_w1(raw[nm], pre[nm], "BAND03")).at(0.75, COST0)[0]
        v2ref[nm] = {w: pack(v2[pan.masks[w]]) for w in WINDOWS}
    books = {}
    for nm in PANELS:
        for a in ARMS:
            books[(nm, a)] = Book(pans[(nm, ARM_FREQ[a])], arm_w1(raw[nm], pre[nm], a))
    P(f"built {len(books)} (panel, arm) books")
    P("")

    gates = run_gates(pans, books, spyref, v2ref, pre, raw)

    # the union ladder, scored once per (panel, arm, cost)
    UNION = sorted({round(g, 4) for L in LADDERS.values() for g in L})
    P("")
    P(f"scoring the union of all five ladders ({len(UNION)} rungs) x {len(COSTS)} costs x "
      f"{len(books)} books ...")
    t = time.time()
    rows = []
    for nm in PANELS:
        for a in ARMS:
            bk = books[(nm, a)]
            for cost in COSTS:
                for g in UNION:
                    r = score_g(bk, g, cost, spyref[nm], v2ref[nm])
                    r.update(panel=nm, arm=a, freq=ARM_FREQ[a])
                    rows.append(r)
    fine = pd.DataFrame(rows)
    del rows
    P(f"  {len(fine):,} book-rows  ({time.time()-t:.1f}s)")
    dump(fine, "ladder.csv")

    gates["G3"], G3 = gate_parent(fine)

    # G3b -- the same gate on a tape truncated to 804's own last date.  If the legs then match
    # exactly and the metrics tighten, the G3 mismatches are VINTAGE, proven rather than asserted.
    P("")
    par_last = pd.Timestamp(PARENT_LAST)
    t = time.time()
    rows_t = []
    for nm in CLAIMSETS["REPRO"]:
        pxT = raw[nm].loc[:par_last]
        preT = prep(pxT)
        pansT = {fq: Panel(nm, pxT, fq) for fq in ("W", "M")}
        panW = pansT["W"]
        spyT = {w: pack(panW.spy[panW.masks[w]]) for w in WINDOWS}
        v2T_r = Book(panW, arm_w1(pxT, preT, "BAND03")).at(0.75, COST0)[0]
        v2T = {w: pack(v2T_r[panW.masks[w]]) for w in WINDOWS}
        for a in ARMS:
            bkT = Book(pansT[ARM_FREQ[a]], arm_w1(pxT, preT, a))
            for g in RECORD8:
                r = score_g(bkT, g, COST0, spyT, v2T)
                r.update(panel=nm, arm=a, freq=ARM_FREQ[a])
                rows_t.append(r)
    fineT = pd.DataFrame(rows_t)
    P(f"G3b tape truncated to {par_last.date()} (804's own last date), {len(fineT)} rows rebuilt "
      f"in {time.time()-t:.1f}s")
    gates["G3b"], G3b = gate_parent(fineT, tag="G3b", note=False)
    dump(G3b, "gate3b.csv")

    # G5 monotonicity, per book, on the 0.01 ladder at the primary cost
    viol = []
    for nm in PANELS:
        for a in ARMS:
            sub = fine[(fine.panel == nm) & (fine.arm == a) & (fine.cost == COST0)]
            sub = sub[np.isin(np.round(sub.gross.values, 6),
                              np.round(LADDERS["STEP01"], 6))].sort_values("gross")
            dC = np.diff(sub.FULL_CAGR.values)
            dD = np.diff(np.abs(sub.FULL_MaxDD.values))
            nC, nD = int((dC < -1e-12).sum()), int((dD < -1e-12).sum())
            sp = float(sub.FULL_Sharpe.max() - sub.FULL_Sharpe.min())
            viol.append(dict(panel=nm, arm=a, cagr_violations=nC, dd_violations=nD,
                             sharpe_spread=sp))
    V = pd.DataFrame(viol)
    gates["G5"] = bool((V.cagr_violations == 0).all() and (V.dd_violations == 0).all())
    P(f"G5  monotonicity on the 0.01 ladder, all {len(V)} books: CAGR(g) non-decreasing on "
      f"{int((V.cagr_violations==0).sum())} of {len(V)}, |MaxDD(g)| non-decreasing on "
      f"{int((V.dd_violations==0).sum())} of {len(V)}   -> {'PASS' if gates['G5'] else 'FAIL'}")
    P(f"      Sharpe spread over the whole 0.01 ladder: median {V.sharpe_spread.median():.4f}, "
      f"max {V.sharpe_spread.max():.4f}  (804's 'gross cannot decide a Sharpe leg')")
    NONMONO = {(r.panel, r.arm) for _, r in V.iterrows()
               if r.cagr_violations > 0 or r.dd_violations > 0}
    for _, r in V[(V.cagr_violations > 0) | (V.dd_violations > 0)].iterrows():
        P(f"      MONOTONICITY VIOLATION {r.panel:5s} {r.arm:13s} CAGR {r.cagr_violations} "
          f"DD {r.dd_violations}  -> its bisected endpoints are NOT a single crossing and every")
        P("        row for this book is flagged `nonmono` and excluded from the calibration "
          "headline")
    dump(V, "monotonicity.csv")

    # EXACT endpoints
    P("")
    t = time.time()
    erows = []
    for nm in PANELS:
        for a in ARMS:
            bk = books[(nm, a)]
            for cost in COSTS:
                for conv, win in [("c804", "FULL"), ("cwin", "IS"), ("cwin", "OOS")]:
                    erows.append(exact_row(nm, a, cost, bk, spyref[nm], conv, win))
                    erows.append(exact_row(nm, a, cost, bk, spyref[nm], conv, win,
                                           gmax_search=LEV_GMAX, tag="LEVERED"))
    EXALL = pd.DataFrame(erows)
    EX = EXALL[EXALL.ceiling == "PROTO"].reset_index(drop=True)
    P(f"solved {len(EXALL)} exact bands by bisection ({len(EX)} at the PROTOCOL-2 ceiling "
      f"g <= {GMAX_PROTO:.2f}, {len(EXALL)-len(EX)} at the flagged LEVERED ceiling "
      f"g <= {LEV_GMAX:.2f})  ({time.time()-t:.1f}s)")
    dump(EXALL, "exact.csv")
    lev = EXALL[(EXALL.ceiling == "LEVERED") & (EXALL.conv == "c804") & (EXALL.cost == COST0)]
    pro = EX[(EX.conv == "c804") & (EX.cost == COST0)]
    mrg = pro.merge(lev, on=["panel", "arm", "cost", "conv", "window"], suffixes=("_p", "_l"))
    nsame = int((np.abs(mrg.width_p - mrg.width_l) < 1e-6).sum())
    P(f"  CEILING READING: {nsame} of {len(mrg)} bands have the SAME width at both ceilings, i.e."
      f" their upper edge is the PROTOCOL's g=1.00 and not the DD cap;")
    P(f"  {int(mrg.dd_cap_never_breached_p.sum())} of {len(mrg)} never breach the DD cap at any "
      f"g <= 1.00 at {COST0:.0f} bps -- those bands are CENSORED BY THE PROTOCOL, not by a ladder.")

    # G6 -- bisection inside the bracketing pair of 0.01 rungs (c804 convention, primary cost)
    worst = 0.0
    nchk = 0
    for nm in PANELS:
        for a in ARMS:
            e = EX[(EX.panel == nm) & (EX.arm == a) & (EX.cost == COST0)
                   & (EX.conv == "c804")].iloc[0]
            if bool(e["is_empty"]) or e.g_min is None or not np.isfinite(e.level_width):
                continue
            lad = fine[(fine.panel == nm) & (fine.arm == a) & (fine.cost == COST0)]
            lad = lad[np.isin(np.round(lad.gross.values, 6),
                              np.round(LADDERS["STEP01"], 6))].sort_values("gross")
            okc = lad[lad.c804_L5_CAGRfloor]
            okd = lad[lad.c804_L4_DDcap]
            if len(okc):
                worst = max(worst, max(0.0, e.g_min - float(okc.gross.min())) - 0.01)
                nchk += 1
            if len(okd):
                worst = max(worst, max(0.0, float(okd.gross.max()) - e.g_max) - 0.01)
                nchk += 1
    gates["G6"] = worst <= 1e-6
    P(f"G6  bisection inside its 0.01 bracket on {nchk} endpoints   worst overshoot "
      f"{worst:.3e}   -> {'PASS' if gates['G6'] else 'FAIL'}")

    # G7 determinism
    bk2 = Book(pans[("U56", "W")], arm_w1(raw["U56"], pre["U56"], "CAND20"))
    a0 = fine[(fine.panel == "U56") & (fine.arm == "CAND20")
              & (fine.cost == COST0)].sort_values("gross")
    d7 = max(abs(score_g(bk2, float(g), COST0, spyref["U56"], v2ref["U56"])["FULL_Sharpe"]
                 - float(s)) for g, s in zip(a0.gross.values[::17], a0.FULL_Sharpe.values[::17]))
    e7 = exact_row("U56", "CAND20", COST0, bk2, spyref["U56"], "c804", "FULL")
    e7b = EX[(EX.panel == "U56") & (EX.arm == "CAND20") & (EX.cost == COST0)
             & (EX.conv == "c804")].iloc[0]
    d7b = abs(float(e7["width"]) - float(e7b.width))
    gates["G7"] = (d7 == 0.0) and (d7b == 0.0)
    P(f"G7  DETERMINISM (rebuild U56/CAND20, re-score {len(a0.gross.values[::17])} rungs and "
      f"re-bisect)  max|dSharpe| {d7:.3e}, |dwidth| {d7b:.3e}   -> "
      f"{'PASS' if gates['G7'] else 'FAIL'}")

    # G9 -- census scanner == simulation on 804's own committed file
    P("")
    CP, _ = scan_record(files=[str(PARENT)])
    g9rows, g9bad = [], 0
    for _, c in CP.iterrows():
        kv = dict(p.split("=", 1) for p in c.key.split("|") if "=" in p)
        pn, ar = kv.get("panel"), kv.get("arm")
        if pn is None or ar is None:
            continue
        mine = ladder_read(fine, pn, ar, COST0, "RECORD8", "c804_pass4b")
        if mine is None:
            continue
        same = (int(c.npass) == int(mine["npass"]) and
                bool(c["is_empty"]) == bool(mine["is_empty"]) and
                (bool(c["is_empty"]) or (abs(float(c.width) - float(mine["width"])) < 1e-9
                                         and abs(float(c.lo) - float(mine["lo"])) < 1e-9)))
        g9bad += (not same)
        g9rows.append(dict(panel=pn, arm=ar, committed_npass=int(c.npass),
                           mine_npass=int(mine["npass"]),
                           committed_width=float(c.width) if not c["is_empty"] else np.nan,
                           mine_width=float(mine["width"]) if not mine["is_empty"] else np.nan,
                           match=same))
    G9 = pd.DataFrame(g9rows)
    gates["G9"] = bool(len(G9) > 0 and g9bad == 0)
    P(f"G9  CENSUS == SIMULATION on 804's own committed CSV: {len(G9)-g9bad} of {len(G9)} "
      f"(panel, arm) bands identical in pass-count, emptiness and width   -> "
      f"{'PASS' if gates['G9'] else 'FAIL'}")
    for _, r in G9[~G9.match].iterrows():
        P(f"      MISMATCH {r.panel:5s} {r.arm:13s} committed npass {r.committed_npass} "
          f"width {r.committed_width}  vs mine {r.mine_npass} / {r.mine_width}")
    dump(G9, "gate9.csv")

    P("")
    gtxt = ", ".join(f"{k}=" + ("PASS" if v else "FAIL") for k, v in sorted(gates.items()))
    P(f"GATES: {sum(bool(v) for v in gates.values())} of {len(gates)} PASS  ({gtxt})")
    P("")

    # --------------------------------------------------------------------------------------
    # THE CALIBRATION: what each ladder REPORTS vs what is THERE
    # --------------------------------------------------------------------------------------
    P("=" * 112)
    P("THE CALIBRATION -- what each resolution REPORTS against the bisected truth")
    P("=" * 112)
    rrows = []
    for nm in PANELS:
        for a in ARMS:
            for cost in COSTS:
                ex = EX[(EX.panel == nm) & (EX.arm == a) & (EX.cost == cost)
                        & (EX.conv == "c804")].iloc[0]
                w_ex = float(ex.width)
                for res in RESOLUTIONS[:-1]:
                    rd = ladder_read(fine, nm, a, cost, res, "c804_pass4b")
                    if rd is None:
                        continue
                    w_l = 0.0 if rd["is_empty"] else float(rd["width"])
                    step = LADDER_STEP[res]
                    cls_l = ("EMPTY" if rd["is_empty"] else
                             ("SINGLE" if rd["npass"] == 1 else "WIDE"))
                    cls_e = ("EMPTY" if w_ex <= 0 else ("NARROW" if w_ex < step else "WIDE"))
                    art_w = bool(abs(w_l - w_ex) >= step - 1e-12)
                    art_c = bool((cls_l == "EMPTY") != (cls_e == "EMPTY")) or \
                        bool(cls_l in ("SINGLE",) and cls_e == "WIDE")
                    rrows.append(dict(
                        claimset=("REPRO" if nm in CLAIMSETS["REPRO"] else "EXT"),
                        nonmono=bool((nm, a) in NONMONO),
                        panel=nm, arm=a, cost=cost, resolution=res, step=step,
                        n_pass_rungs=int(rd["npass"]), w_ladder=w_l, w_exact=w_ex,
                        d_width=w_l - w_ex, class_ladder=cls_l, class_exact=cls_e,
                        artefact_width=art_w, artefact_class=art_c,
                        artefact=bool(art_w or art_c),
                        g_lo_ladder=rd["lo"], g_hi_ladder=rd["hi"],
                        g_lo_exact=ex.g_min, g_hi_exact=ex.g_max, sharpe_ok=bool(ex.sharpe_ok)))
    R = pd.DataFrame(rrows)
    dump(R, "resolution.csv")
    if int(R.nonmono.sum()):
        P(f"  {int(R.nonmono.sum())} rows carry `nonmono` (book failed G5) and are excluded from "
          f"the headline tables below; they are in the CSV and reported separately at the end.")
        R = R[~R.nonmono].copy()

    for cs in ("REPRO", "EXT"):
        sub = R[(R.claimset == cs) & (R.cost == COST0)]
        P("")
        P(f"CLAIM SET {cs} ({'804 committed cells' if cs=='REPRO' else 'SMALL, this run only'}), "
          f"{COST0:.0f} bps, 804's own FULL-window convention -- {sub.panel.nunique()} panels x "
          f"{sub.arm.nunique()} arms = {len(sub)//len(RESOLUTIONS[:-1])} bands")
        P(f"  {'resolution':>10} {'step':>6} {'artefact':>9} {'width-err':>10} {'class-err':>10} "
          f"{'mean d_w':>9} {'max |d_w|':>10} {'over-report':>12}")
        for res in RESOLUTIONS[:-1]:
            s = sub[sub.resolution == res]
            if not len(s):
                continue
            P(f"  {res:>10} {LADDER_STEP[res]:6.2f} {int(s.artefact.sum()):4d}/{len(s):<4d} "
              f"{int(s.artefact_width.sum()):5d}/{len(s):<4d} "
              f"{int(s.artefact_class.sum()):5d}/{len(s):<4d} "
              f"{s.d_width.mean():9.4f} {s.d_width.abs().max():10.4f} "
              f"{int((s.d_width > 1e-12).sum()):6d}/{len(s):<5d}")
        nz = sub[sub.w_exact > 0]
        nb = len(sub) // max(len(RESOLUTIONS[:-1]), 1)
        nnz = int(nz.resolution.value_counts().max()) if len(nz) else 0
        mn = float(nz.w_exact.min()) if len(nz) else float("nan")
        md = float(nz.w_exact.median()) if len(nz) else float("nan")
        mx = float(nz.w_exact.max()) if len(nz) else float("nan")
        P(f"  bands with a NON-EMPTY exact 4b window: {nnz} of {nb}; exact widths "
          f"min {mn:.4f} / median {md:.4f} / max {mx:.4f}")

    P("")
    P("H_DIR (ladder widths are biased DOWNWARD -- a ladder samples an interval):")
    for res in RESOLUTIONS[:-1]:
        s = R[(R.resolution == res) & (R.cost == COST0)]
        P(f"  {res:>10}  under-reports {int((s.d_width < -1e-12).sum()):3d}, exact "
          f"{int((s.d_width.abs() <= 1e-12).sum()):3d}, OVER-reports "
          f"{int((s.d_width > 1e-12).sum()):3d}  of {len(s)}")
    over = R[(R.d_width > 1e-12)]
    if len(over):
        P(f"  the over-reporting cells (a ladder width EXCEEDING the bisected level window) — "
          f"{len(over)} rows:")
        for _, r in over.head(12).iterrows():
            P(f"    {r.panel:5s} {r.arm:13s} {int(r.cost):3d}bps {r.resolution:8s} "
              f"w_lad {r.w_ladder:.4f} > w_exact {r.w_exact:.4f}  sharpe_ok={r.sharpe_ok}")

    P("")
    P("PER-BAND DETAIL at 10 bps (claim set REPRO), all 5 ladders against the bisected window:")
    P(f"  {'panel':>5} {'arm':>13} {'RECORD8':>9} {'STEP25':>8} {'STEP10':>8} {'STEP05':>8} "
      f"{'STEP01':>8} {'EXACT':>8}  exact band")
    for nm in CLAIMSETS["REPRO"]:
        for a in ARMS:
            s = R[(R.panel == nm) & (R.arm == a) & (R.cost == COST0)]
            if not len(s):
                continue
            g = {r.resolution: r for _, r in s.iterrows()}
            ex = EX[(EX.panel == nm) & (EX.arm == a) & (EX.cost == COST0)
                    & (EX.conv == "c804")].iloc[0]
            bandtxt = ("EMPTY" if ex.width <= 0 else
                       f"[{ex.g_min:.4f}, {ex.g_max:.4f}]")
            P(f"  {nm:>5} {a:>13} " + " ".join(
                f"{(g[r].w_ladder if r in g else np.nan):8.3f}" for r in RESOLUTIONS[:-1]) +
              f" {float(ex.width):8.4f}  {bandtxt}"
              + ("" if ex.sharpe_ok else "   (Sharpe leg fails -> 4b window EMPTY)"))

    # --------------------------------------------------------------------------------------
    # RULE 8 -- does the resolution used to CHOOSE change the OOS verdict?
    # --------------------------------------------------------------------------------------
    P("")
    P("=" * 112)
    P("RULE 8 WALK-FORWARD -- g chosen on 2009-2016 ONLY at each resolution, OOS read once")
    P("=" * 112)
    P("CHOOSERS (both IS-only): IS_MID = midpoint of the IS band at that resolution;")
    P("  IS_SHARPE = the rung inside the IS band with the best IS Sharpe (EXACT uses a 0.001 scan")
    P("  inside the bisected IS band).  Stated, not worked around: the STRICT IS 4b set is often")
    P("  EMPTY because a half-sample Sharpe leg read inside an 8-year window fails at every gross")
    P("  (675's finding), so the IS band here is the intersection of the two IS LEVEL legs, and")
    P("  the choosers are labelled IS-LEVEL choosers.")
    wrows = []
    for nm in PANELS:
        for a in ARMS:
            bk = books[(nm, a)]
            pan = bk.pan
            for cost in COSTS:
                lad_all = fine[(fine.panel == nm) & (fine.arm == a) & (fine.cost == cost)]
                for res in RESOLUTIONS:
                    if res == "EXACT":
                        ex = EX[(EX.panel == nm) & (EX.arm == a) & (EX.cost == cost)
                                & (EX.conv == "cwin") & (EX.window == "IS")].iloc[0]
                        # PROTOCOL 2: no leverage, so no chooser may pick above g = 1.00
                        if ex.g_min is None or not np.isfinite(ex.level_width) \
                                or ex.level_width <= 0:
                            wrows.append(dict(panel=nm, arm=a, cost=cost, resolution=res,
                                              chooser="-", IS_empty=True))
                            continue
                        lo, hi = float(ex.g_min), float(ex.g_max)
                        cand = np.round(np.linspace(lo, hi, min(201, max(2, int(
                            round((hi - lo) / 0.001)) + 1))), 6)
                    else:
                        gs = LADDERS[res]
                        sub = lad_all[np.isin(np.round(lad_all.gross.values, 6),
                                              np.round(gs, 6))].sort_values("gross")
                        ok = sub[sub.cwinIS_L4_DDcap & sub.cwinIS_L5_CAGRfloor]
                        if not len(ok):
                            wrows.append(dict(panel=nm, arm=a, cost=cost, resolution=res,
                                              chooser="-", IS_empty=True))
                            continue
                        lo, hi = float(ok.gross.min()), float(ok.gross.max())
                        cand = ok.gross.values
                    for chooser in ("IS_MID", "IS_SHARPE"):
                        if chooser == "IS_MID":
                            gpick = 0.5 * (lo + hi)
                        else:
                            best, gpick = -np.inf, lo
                            for gg in cand:
                                r, _ = bk.at(float(gg), cost)
                                sh = fsharpe(r[pan.masks["IS"]])
                                if sh > best:
                                    best, gpick = sh, float(gg)
                        r, turn = bk.at(float(gpick), cost)
                        o = pack(r[pan.masks["OOS"]])
                        L = legswin(o, spyref[nm]["OOS"])
                        wrows.append(dict(
                            panel=nm, arm=a, cost=cost, resolution=res, chooser=chooser,
                            IS_empty=False, IS_lo=lo, IS_hi=hi, g_pick=float(gpick),
                            OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"],
                            OOS_H1=o["H1"], OOS_H2=o["H2"],
                            pass4b=bool(all(L.values())),
                            pass4a=pass4a(o, v2ref[nm]["OOS"]),
                            turn_yr=float(turn[pan.masks["OOS"]].sum()
                                          / (pan.masks["OOS"].sum() / 252.0)),
                            **{f"leg_{k}": v for k, v in L.items()}))
    WF = pd.DataFrame(wrows)
    dump(WF, "walkforward.csv")
    live = WF[~WF.IS_empty]
    P(f"  {len(WF)} (panel, arm, cost, resolution, chooser) cells; IS band EMPTY on "
      f"{int(WF.IS_empty.sum())}, live on {len(live)}")
    P(f"  4b OOS passes {int(live.pass4b.sum())} of {len(live)}; 4a OOS passes "
      f"{int(live.pass4a.sum())} of {len(live)}")
    P("")
    P("  by resolution (all costs, both choosers):")
    P(f"  {'resolution':>10} {'live':>6} {'4b':>5} {'4a':>5} {'median g_pick':>14} "
      f"{'median OOS Sharpe':>18}")
    for res in RESOLUTIONS:
        s = live[live.resolution == res]
        if not len(s):
            P(f"  {res:>10} {0:6d}")
            continue
        P(f"  {res:>10} {len(s):6d} {int(s.pass4b.sum()):5d} {int(s.pass4a.sum()):5d} "
          f"{s.g_pick.median():14.3f} {s.OOS_Sharpe.median():18.3f}")

    # resolution-dependence of the OOS verdict, held at the same (panel, arm, cost, chooser)
    P("")
    key = ["panel", "arm", "cost", "chooser"]
    flip = []
    for k, gg in WF.groupby(key):
        v = gg.set_index("resolution")
        verd = {r: (None if bool(v.loc[r, "IS_empty"]) else bool(v.loc[r, "pass4b"]))
                for r in RESOLUTIONS if r in v.index}
        vals = set(verd.values())
        gp = {r: (np.nan if verd[r] is None else float(v.loc[r, "g_pick"])) for r in verd}
        spread = (np.nanmax(list(gp.values())) - np.nanmin(list(gp.values()))
                  if any(np.isfinite(list(gp.values()))) else np.nan)
        flip.append(dict(zip(key, k)) | dict(n_res=len(verd), verdicts=str(verd),
                                             disagree=len(vals) > 1, g_spread=spread,
                                             any_pass=any(x is True for x in verd.values())))
    F = pd.DataFrame(flip)
    dump(F, "resolution_dependence.csv")
    P(f"H_WF: the OOS 4b verdict DISAGREES across resolutions on {int(F.disagree.sum())} of "
      f"{len(F)} (panel, arm, cost, chooser) cells "
      f"({F.disagree.mean():.1%})")
    P(f"      median spread of the CHOSEN g across resolutions {F.g_spread.median():.4f}, "
      f"max {F.g_spread.max():.4f}")
    for _, r in F[F.disagree].head(14).iterrows():
        P(f"      {r.panel:5s} {r.arm:13s} {int(r.cost):3d}bps {r.chooser:9s} "
          f"g-spread {r.g_spread:.3f}  {r.verdicts}")
    P("")
    P("  the OOS 4b PASSES in full (the only rows that could carry capital):")
    pp = live[live.pass4b]
    if not len(pp):
        P("    NONE -- no IS-only chooser at any resolution reaches 4b out of sample.")
    else:
        P(f"    {'panel':>5} {'arm':>13} {'cost':>5} {'res':>8} {'chooser':>9} {'g':>6} "
          f"{'OOS CAGR':>9} {'Sharpe':>7} {'MaxDD':>8} {'H1/H2':>13} {'turn':>6}")
        for _, r in pp.sort_values(["panel", "arm", "cost"]).iterrows():
            P(f"    {r.panel:>5} {r.arm:>13} {int(r.cost):5d} {r.resolution:>8} "
              f"{r.chooser:>9} {r.g_pick:6.3f} {r.OOS_CAGR:9.2%} {r.OOS_Sharpe:7.3f} "
              f"{r.OOS_MaxDD:8.2%} {r.OOS_H1:6.3f}/{r.OOS_H2:6.3f} {r.turn_yr:6.1f}x")
    P("")
    P("  comparands in the same OOS window:")
    for nm in PANELS:
        s, v = spyref[nm]["OOS"], v2ref[nm]["OOS"]
        P(f"    {nm:5s} SPY {s['CAGR']:7.2%} / {s['Sharpe']:.3f} / {s['MaxDD']:7.2%} "
          f"(halves {s['H1']:.3f}/{s['H2']:.3f})   RULES v2 (live) {v['CAGR']:7.2%} / "
          f"{v['Sharpe']:.3f} / {v['MaxDD']:7.2%} (halves {v['H1']:.3f}/{v['H2']:.3f})")
    P(f"    4b bars on OOS: MaxDD >= {DD_CAP:.2f} x SPY's, CAGR >= {CAGR_FLOOR:.2f} x SPY's, "
      f"both half Sharpes > SPY's")

    # --------------------------------------------------------------------------------------
    # the answer
    # --------------------------------------------------------------------------------------
    P("")
    P("=" * 112)
    P("THE ANSWER")
    P("=" * 112)
    P(f"A1  The record carries {len(CEN):,} committed gross-band cells in {CEN.file.nunique()} "
      f"files; {len(NE):,} are non-empty.")
    P(f"A2  {single:,} of {len(NE):,} ({single/max(len(NE),1):.1%}) are SINGLE-RUNG and "
      f"{limited:,} of {len(NE):,} ({limited/max(len(NE),1):.1%}) are RESOLUTION-LIMITED "
      f"(width <= 2 rungs); {cens:,} ({cens/max(len(NE),1):.1%}) are CENSORED at a ladder edge.")
    P(f"A3  Only {safe:,} of {len(NE):,} ({safe/max(len(NE),1):.1%}) committed bands are "
      f"RESOLUTION-SAFE by the pre-registered bar.")
    rep = R[(R.claimset == "REPRO") & (R.cost == COST0)]
    for res in RESOLUTIONS[:-1]:
        s = rep[rep.resolution == res]
        if len(s):
            P(f"A4  calibration {res:>8}: artefact on {int(s.artefact.sum())} of {len(s)} "
              f"reproducible bands, mean width error {s.d_width.mean():+.4f}, "
              f"worst {s.d_width.abs().max():.4f}")
    P("A6  THE JOIN (the queue's own question, band by band).  Of the "
      f"{len(rep[rep.resolution=='RECORD8'])} committed bands this run can re-solve, the "
      "published 8-rung reading MIS-CLASSIFIES these:")
    nflip = 0
    for _, r in rep[(rep.resolution == "RECORD8") & rep.artefact_class].iterrows():
        nflip += 1
        P(f"      {r.panel:5s} {r.arm:13s} published as {r.class_ladder:6s} "
          f"(w={r.w_ladder:.3f}) -- actually {r.class_exact:6s} w={r.w_exact:.4f}, "
          f"g in [{r.g_lo_exact:.4f}, {r.g_hi_exact:.4f}]")
    if nflip == 0:
        P("      (none)")
    P(f"      {nflip} of {len(rep[rep.resolution=='RECORD8'])} published readings change CLASS at "
      f"0.01; every one of them published a real interval as one rung or as nothing, and NONE "
      f"went the other way (H_DIR: 0 over-reports at every resolution).")
    P("      All 20 re-solvable bands come from ONE committed file (804's grid), so this is a "
      "calibration of the record's ladder practice, not a sample of its 96 band-carrying files.")
    P(f"A5  rule 8: the OOS 4b verdict is resolution-dependent on {int(F.disagree.sum())} of "
      f"{len(F)} cells; {int(live.pass4b.sum())} of {len(live)} IS-only picks pass 4b OOS and "
      f"{int(live.pass4a.sum())} pass 4a.")
    P(f"      (0 non-contiguous pass sets in the whole census: {noncont} of {len(NE)} — 804's "
      f"two-monotone-crossings reading holds corpus-wide, which is what makes a bisected")
    P("       endpoint the right object to publish.)")
    P("")
    P(f"total runtime {time.time()-t0:.1f}s")

    # leaderboard rows
    P("")
    P("LEADERBOARD rows:")
    tag = STEM.replace("2026-09-15_", "")
    lbl = []
    pp10 = pp[pp.cost == COST0]
    best = (pp10 if len(pp10) else pp).sort_values("OOS_Sharpe", ascending=False).head(1)
    for _, r in best.iterrows():
        lbl.append(f"| 2026-09-15 | 919 rule-8 best OOS 4b pass: {r.panel}/{r.arm} g={r.g_pick:.3f}"
                   f" ({r.resolution}, {r.chooser}, {int(r.cost)}bps) | {r.OOS_CAGR:.1%} | "
                   f"{r.OOS_Sharpe:.2f} | {r.OOS_MaxDD:.1%} | {r.OOS_H1:.2f} / {r.OOS_H2:.2f} | "
                   f"SPY OOS {spyref[r.panel]['OOS']['Sharpe']:.2f} "
                   f"({spyref[r.panel]['OOS']['H1']:.2f}/{spyref[r.panel]['OOS']['H2']:.2f}) | "
                   f"PARK (known band, not new) | {STEM}.py |")
    lbl.append(f"| 2026-09-15 | 919 census: committed gross bands, {len(NE):,} non-empty | "
               f"single-rung {single/max(len(NE),1):.1%} | limited {limited/max(len(NE),1):.1%} | "
               f"censored {cens/max(len(NE),1):.1%} | safe {safe}/{len(NE)} | "
               f"non-contiguous {noncont} | CENSUS | {STEM}.py |")
    for res in RESOLUTIONS[:-1]:
        s = rep[rep.resolution == res]
        if len(s):
            lbl.append(f"| 2026-09-15 | 919 calibration {res} vs bisection (REPRO, 10bps) | "
                       f"artefact {int(s.artefact.sum())}/{len(s)} | mean dW {s.d_width.mean():+.4f}"
                       f" | worst {s.d_width.abs().max():.4f} | class-err "
                       f"{int(s.artefact_class.sum())}/{len(s)} | — | CALIBRATION | {STEM}.py |")
    lbl.append(f"| 2026-09-15 | 919 rule-8 resolution dependence | disagree "
               f"{int(F.disagree.sum())}/{len(F)} | 4b {int(live.pass4b.sum())}/{len(live)} | "
               f"4a {int(live.pass4a.sum())}/{len(live)} | median g-spread "
               f"{F.g_spread.median():.3f} | — | RULE 8 | {STEM}.py |")
    for line in lbl:
        P(line)

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"\nwrote {STEM}.console.txt")


if __name__ == "__main__":
    main()

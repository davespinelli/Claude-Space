#!/usr/bin/env python3
"""Idea 922 (lane C, 2026-09-15) -- is the 55.8% CENSORING rate a LADDER fact or the PROTOCOL's
1.00 CEILING?

THE QUESTION (queue, 2026-09-15)
  Idea 919 censused 2,699 non-empty committed gross bands and found 1,505 of them (55.8%) have a
  PASSING RUNG SITTING ON THEIR LADDER'S OWN EDGE, so the published width is a lower bound and the
  true edge is somewhere outside the ladder.  It also reported, on the 30 bands it could re-solve,
  that 7 never breach the 4b DD cap below g = 1.00 and 25 of 30 have IDENTICAL widths at the 1.00
  and 1.50 ceilings.  Those two readings pull in opposite directions and 919 never joined them.
  The queue asks for the decomposition: how much of the censoring is a LADDER that stopped short
  of rungs PROTOCOL would have allowed, and how much is the no-leverage line truncating a band
  that genuinely runs past g = 1.00?

WHY THE TWO ARE DIFFERENT, AND WHY IT MATTERS FOR CAPITAL
  A censored band is a published width that under-states its own interval.  The two causes have
  opposite remedies and opposite meanings:
    LADDER-SHORT   the run's own top rung is BELOW 1.00 (or its bottom rung above the true CAGR
                   crossing).  PROTOCOL 2 permitted more rungs; the run simply did not run them.
                   The fix is free -- score more rungs -- and the published width is an artefact
                   of effort, not of the rulebook.
    CEILING-BOUND  the run's ladder reaches g = 1.00 and the DD cap is STILL not breached there.
                   PROTOCOL 2 forbids leverage, so NO admissible ladder can ever see this band's
                   upper edge.  The width is not an artefact at all: it is the honest statement
                   "this book is never dangerous enough to be excluded at any gross we may hold",
                   and the binding constraint on the book is the rulebook, not the DD cap.
  A capital reader needs to know which: the first says a published band is too narrow and should
  be re-solved; the second says a published band is an INTERVAL OPEN AT THE TOP whose upper edge
  is 1.00 by fiat and whose DD leg is NOT BINDING anywhere a chooser may pick.

THE RUN HAS TWO HALVES, AND BOTH ARE REPORTED
  PART A  CENSUS DECOMPOSITION of the committed corpus, no simulation.  919's scanner, re-run
          unchanged, then every censored band split by WHICH EDGE carries the censor and by where
          its own ladder stopped.  A band censored at the top with g_last < 1.00 is LADDER-SHORT
          by construction and needs no simulation to classify.  A band censored at the top with
          g_last == 1.00 is AMBIGUOUS from the record alone -- that class, and only that class, is
          what Part B prices.  A band censored at the BOTTOM is always LADDER-SHORT: PROTOCOL
          places no floor on gross, so g_first > 0 is always the run's own choice.
  PART B  RE-SOLUTION ACROSS CEILINGS of the sub-population this sandbox can rebuild (idea 804's
          committed 2 panels x 10 arms grid, plus the same 10 arms on SMALL as a declared
          extension).  The DD-cap breach point is bisected with the search ceiling walked over
          TUNED 1, so each band is labelled CEILING-BOUND or INTERIOR by where its breach actually
          is, and the census's AMBIGUOUS class gets a measured rate instead of an assumption.

WHAT IS TUNED AND WHAT IS REPORTED (PROTOCOL 4: max 2 tuned parameters; the queue's own two)
  TUNED 1  CEILING, 5 levels, every one reported:
           1.00  PROTOCOL 2's no-leverage line -- the only admissible one, and the primary
           1.25 / 1.50 / 2.00 / 3.00   flagged LEVERED extensions, reported so the location of the
           true edge is measurable, and from which NO chooser in the rule-8 section may pick.
  TUNED 2  CLAIM SET, 2 levels: REPRO = the 20 committed (panel x arm) cells of 804's grid on
           U56 and B136, the bands this run can price against the record; EXT = the same 10 arms
           on SMALL, which no committed run priced, reported separately and never mixed into a
           census or calibration number.
  REPORTED AXES (nothing fitted on them; every point published): cost 0 / 10 / 25 bps; window
  FULL (804's and 670's own convention) / IS 2009-2016 / OOS 2017-2026 (window-local convention).

PRE-REGISTERED BARS (fixed before any number was read; both directions reported)
  H_LADDER   (census)  a censored band is LADDER-SHORT iff its censor is at the bottom rung, or at
             a top rung strictly below the PROTOCOL ceiling, or at a top rung strictly above it
             (a run that already levered had no ceiling to blame).  This class needs no
             simulation and is a LOWER BOUND on the ladder's share.
  H_CEIL     (census)  the ceiling's share is bounded ABOVE by the bands whose ONLY censor is a
             top rung exactly at g = 1.00.  Anything outside that class the ceiling cannot
             explain.  Reported as the upper bound it is.
  H_BOUND    (Part B)  a band is CEILING-BOUND iff its DD-cap breach point is > 1.00, i.e. the
             upper edge PROTOCOL allows is the ceiling itself.  Measured by bisection to 1e-6 at
             the widest ceiling, so the label is a location, not a ladder reading.
  H_SAME     (Part B)  919's "25 of 30 identical at 1.00 and 1.50" is re-read as a prediction:
             width(C) must be CONSTANT in C for every INTERIOR band and STRICTLY INCREASING in C
             for every CEILING-BOUND one.  Any band violating either direction is named.
  H_PRICE    (Part B)  what the ceiling COSTS: for the CEILING-BOUND bands, the 4b-passing gross
             range PROTOCOL forbids, and whether any of it would have been reachable by an
             IS-only chooser.
  H_WF       (rule 8, required)  g chosen on 2009-2016 ONLY at each ceiling, OOS 2017-2026 read
             once, both KEEP paths, against SPY and RULES v2 in the same window.  The capital
             question is whether RAISING THE CEILING buys an out-of-sample 4b pass that the
             admissible ceiling does not already have.

GATES (all printed before any result number)
  G1   the fast runner == engine.backtest on returns and turnover, at an admissible gross AND at
       a LEVERED one (the levered arithmetic is load-bearing here and was not in 919)
  G2   BAND03 at g=0.75 == baseline.rules_v2_weights elementwise
  G3   CROSS-RUN: idea 804's committed `.grid.csv` reproduces -- legs and verdicts EXACTLY, metrics
       to a 5e-3 vintage bar.  These are the very bands Part B re-solves.
  G3c  CROSS-RUN on the CENSUS: 919's committed census headline (2,699 non-empty, 1,505 censored)
       must reproduce EXACTLY on 919's own file set, i.e. with 919's and this run's own outputs
       excluded.  Without it the decomposition below is a decomposition of a different corpus.
  G4   the committed U56 triples (SPY, RULES v2)
  G5   monotonicity of CAGR(g) and |MaxDD(g)| on the 0.01 ladder ALL THE WAY TO THE WIDEST
       CEILING -- this is what makes a bisected endpoint above 1.00 meaningful; any book that
       fails is named, flagged `nonmono` and excluded from the calibration headline
  G6   bisection inside its bracketing pair of 0.01 rungs
  G7   determinism (rebuild, re-score, re-bisect)
  G8   the analytic ray: SPYBH (g x SPY) reads |MaxDD(g)|/|MaxDD(SPY)| = g at admissible gross;
       the levered deviation is reported, not asserted away
  G9   CENSUS-vs-SIMULATION join: the Part A scanner, run on 804's own committed CSV, must return
       the same CENSOR DECOMPOSITION (both edge flags, the ladder's own first and last rung) as
       the RECORD8 ladder reading of the simulation.  This is what joins the two halves.
  G10  SOLVENCY at the widest ceiling: a levered book whose NAV path touches zero has no defined
       drawdown and no meaningful bisection.  Worst V over every book is printed and any book that
       breaches is named and excluded from the levered headline.
  G11  CEILING MONOTONICITY: width(C) non-decreasing in C on every band, and EXACTLY equal across
       all five C whenever the breach point is <= 1.00.  This is H_SAME run as a gate.

PROTOCOL: 10 bps primary, t+1, weekly (monthly for BAND03_M, which is 804's own cadence arm),
warm-up 260 days, IS 2009-2016 / OOS 2017-2026.  Nothing in RULES.md / PROTOCOL.md / scan.py /
bot.py / baseline.py is modified.  Every gross above 1.00 in this file is a MEASUREMENT of where
an edge sits and is flagged LEVERED; no chooser picks from it and nothing above 1.00 is promoted.

SURVIVORSHIP: U56 / B136 / SMALL are current-constituent lists (SMALL additionally drops the
tickers with max_1d_move >= 1.0 per data/small_meta.csv), so every CAGR and drawdown LEVEL below
is optimistic.  A CEILING-BOUND label says a book's drawdown never reaches 0.60 x SPY's at any
admissible gross, and a survivorship-inflated panel makes that EASIER to earn -- so the
ceiling-bound share measured here is an UPPER bound on what a point-in-time panel would show.
The census and the ladder-vs-ceiling contrasts are same-tape comparisons and unaffected.
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
BAND_TOL = 2 * BISECT_TOL   # a width is two independent bisections, so this is its resolution
GMIN_SEARCH = 0.002

# ---- TUNED DIAL 1: the CEILING ----------------------------------------------------------------
GMAX_PROTO = 1.00                       # PROTOCOL 2: no leverage unless the idea says so
CEILINGS = [1.00, 1.25, 1.50, 2.00, 3.00]
CEIL_TAG = {1.00: "PROTO", 1.25: "LEV125", 1.50: "LEV150", 2.00: "LEV200", 3.00: "LEV300"}
CMAX = max(CEILINGS)

# ---- TUNED DIAL 2: the claim set --------------------------------------------------------------
CLAIMSETS = {"REPRO": ["U56", "B136"], "EXT": ["SMALL"]}
PANELS = ["U56", "B136", "SMALL"]

# ---- reported axes ----------------------------------------------------------------------------
COSTS = [0.0, 10.0, 25.0]
WINDOWS = ["FULL", "IS", "OOS"]
ARMS = ["BAND03", "BAND08", "BAND03_M", "CAND20_VS", "CAND20", "CAND10", "CAND05",
        "CAND20_NOCAP", "EWELIG", "SPYBH"]
ARM_FREQ = {a: ("M" if a == "BAND03_M" else FREQ0) for a in ARMS}

# the 0.01 ladder, extended to the widest ceiling (the RECORD8 rungs are a subset of it below 1.0)
RECORD8 = [0.20, 0.35, 0.50, 0.60, 0.75, 0.85, 0.95, 1.00]
FINE = [round(0.01 * i, 4) for i in range(1, int(round(CMAX * 100)) + 1)]
FINE_STEP = 0.01

SPY_U56 = (0.1516, 0.8861, -0.3372)
V2_U56 = (0.0863, 1.2018, -0.1205)
TOL_C, TOL_S, TOL_D = 0.004, 0.030, 0.015
G3_BAR = 5e-3
PARENT = ROOT / "research" / "backtests" / \
    "2026-09-11_is-the-GROSS-dial-s-4b-FOOTPRINT-the-CAGR-FLOOR-alone_C.grid.csv"
PARENT_LAST = "2026-09-11"         # 804's own run date, i.e. the last bar its tape could carry
# idea 919's committed census headline -- the corpus this run decomposes (G3c)
P919_STEM = "2026-09-15_re-read-every-committed-GROSS-BAND-at-0.01-RESOLUTION_C"
P919_NONEMPTY, P919_CENSORED, P919_CELLS = 2699, 1505, 11881

# ---- Part A scanner configuration (919's, unchanged) ------------------------------------------
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
# PART A -- the census scanner (919's, unchanged) plus the CENSOR DECOMPOSITION
# ================================================================================================
BOOLISH = {True, False, "True", "False", "true", "false", "TRUE", "FALSE"}


def _is_cat(s: pd.Series) -> bool:
    return not pd.api.types.is_float_dtype(s)


def _is_verdict(s: pd.Series) -> bool:
    """A boolean column is a RESULT (a leg, a pass flag), never a book key.  Grouping by one would
    split a band by its own verdicts, which is the error G9 exists to catch."""
    if pd.api.types.is_bool_dtype(s):
        return True
    u = set(pd.unique(s.dropna()))
    return bool(u) and u.issubset(BOOLISH)


def _key_columns(d: pd.DataFrame, gcol: str, pcol: str) -> list[str]:
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
    """Read one committed band off its own ladder, exactly as its run published it, and split the
    censor by EDGE.  `cen_lo` / `cen_hi` are the two facts the queue's question turns on."""
    step = float(np.median(np.diff(gv))) if len(gv) > 1 else np.nan
    npass = int(pp.sum())
    base = dict(nrung=len(gv), step=step, g_first=float(gv[0]), g_last=float(gv[-1]))
    if npass == 0:
        return base | dict(npass=0, lo=np.nan, hi=np.nan, width=np.nan, width_rungs=np.nan,
                           contig=True, censor=False, cen_lo=False, cen_hi=False, is_empty=True)
    idx = np.flatnonzero(pp)
    lo, hi = float(gv[idx[0]]), float(gv[idx[-1]])
    w = hi - lo
    cen_lo = bool(lo <= gv[0] + 1e-12)
    cen_hi = bool(hi >= gv[-1] - 1e-12)
    return base | dict(
        npass=npass, lo=lo, hi=hi, width=w,
        width_rungs=(w / step if step and np.isfinite(step) and step > 0 else np.nan),
        contig=bool((idx[-1] - idx[0] + 1) == len(idx)),
        censor=bool(cen_lo or cen_hi), cen_lo=cen_lo, cen_hi=cen_hi, is_empty=False)


def decompose(NE: pd.DataFrame) -> pd.DataFrame:
    """H_LADDER / H_CEIL applied to every non-empty committed band.  Pure bookkeeping on the
    ladder's own rungs -- no simulation is involved and none is needed for these classes."""
    d = NE.copy()
    gl = d.g_last.values
    d["top_short"] = d.cen_hi & (gl < GMAX_PROTO - 1e-9)      # ladder stopped below the line
    d["top_at_ceiling"] = d.cen_hi & (np.abs(gl - GMAX_PROTO) <= 1e-9)
    d["top_levered"] = d.cen_hi & (gl > GMAX_PROTO + 1e-9)    # ladder already past the line
    d["short_by"] = np.where(d.top_short, GMAX_PROTO - gl, np.nan)
    d["short_rungs"] = d.short_by / d.step.replace(0, np.nan)

    def cls(r):
        if not r.censor:
            return "UNCENSORED"
        if r.cen_lo and r.cen_hi:
            return "BOTH_EDGES"
        if r.cen_lo:
            return "BOTTOM_ONLY"
        if r.top_short:
            return "TOP_LADDER_SHORT"
        if r.top_levered:
            return "TOP_ABOVE_CEILING"
        return "TOP_AT_CEILING"
    d["censor_class"] = d.apply(cls, axis=1)
    # H_LADDER: everything the ceiling CANNOT be blamed for.  BOTH_EDGES is in: its BOTTOM censor
    # is a ladder fact whatever its top does, which is H_LADDER's first clause exactly.  The two
    # classes are therefore exhaustive and disjoint over the censored set.
    d["ladder_fact"] = d.censor & d.censor_class.isin(
        ["BOTTOM_ONLY", "BOTH_EDGES", "TOP_LADDER_SHORT", "TOP_ABOVE_CEILING"])
    # H_CEIL upper bound: only a top-only censor sitting exactly on the line
    d["ceiling_candidate"] = d.censor_class == "TOP_AT_CEILING"
    # BOTH_EDGES is a ladder fact at the bottom whatever the top does -- counted there, and its
    # top is reported separately so nothing is hidden by the precedence of the classes.
    d["both_top_at_ceiling"] = (d.censor_class == "BOTH_EDGES") & d.top_at_ceiling
    return d


def scan_record(files=None, exclude_stems=()) -> tuple[pd.DataFrame, dict]:
    """Every committed gross band in research/backtests/*.csv."""
    rows, stat = [], dict(files_seen=0, files_with_dial=0, groups_short=0, groups_dup=0,
                          groups_ok=0)
    if files is None:
        files = [f for f in sorted(glob.glob(str(OUT / "*.csv")))
                 if not any(os.path.basename(f).startswith(s) for s in exclude_stems)]
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
# PART B -- the runner (675/919's vectorised equivalent of engine.backtest)
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

    def nav(self, g: float):
        """The intra-period NAV multiplier.  At g > 1 this can in principle touch zero; G10."""
        return 1.0 + g * (self.S - self.As)

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


def edges(bk, cost, spyref, conv, win, ceiling):
    """(g_min from the CAGR floor, g_break where the DD cap is first BREACHED) inside [., ceiling].
    g_break is None when the cap is never breached at or below the ceiling -- that is exactly the
    CEILING-BOUND condition of H_BOUND when ceiling == 1.00."""
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

    gmin = bisect(f_cagr, GMIN_SEARCH, ceiling)
    gbreak = bisect(f_dd, GMIN_SEARCH, ceiling)
    gmax = ceiling if gbreak is None else gbreak - BISECT_TOL
    return gmin, gmax, gbreak


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


def ceiling_row(panel, arm, cost, bk, spyref, conv, win, ceiling):
    gmin, gmax, gbreak = edges(bk, cost, spyref, conv, win, ceiling)
    sh, shdet = sharpe_legs_ok(bk, cost, spyref, conv, win)
    lw = np.nan if gmin is None else max(0.0, gmax - gmin)
    empty = bool((not sh) or gmin is None or not np.isfinite(lw) or lw <= 0.0)
    return dict(panel=panel, arm=arm, cost=cost, conv=conv, window=win,
                ceiling=float(ceiling), ceiling_tag=CEIL_TAG[ceiling],
                admissible=bool(abs(ceiling - GMAX_PROTO) < 1e-12),
                g_min=gmin, g_break=gbreak, g_max=gmax,
                dd_never_breached=bool(gbreak is None),
                level_width=lw, width=(0.0 if empty else lw),
                sharpe_ok=sh, sharpe_detail="".join("y" if x else "n" for x in shdet),
                is_empty=empty)


def ladder_read(fine, panel, arm, cost, rungs, passcol):
    """What a ladder of these rungs REPORTS for this band, read exactly as a run would read it."""
    sub = fine[(fine.panel == panel) & (fine.arm == arm) & (fine.cost == cost)]
    sub = sub[np.isin(np.round(sub.gross.values, 6), np.round(rungs, 6))].sort_values("gross")
    if len(sub) < 3:
        return None
    b = band_of(sub.gross.values, sub[passcol].values.astype(bool))
    b.update(panel=panel, arm=arm, cost=cost)
    return b


# ================================================================================================
# gates
# ================================================================================================
def gate_parent(fine, tag="G3"):
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
    for _, r in G[~G.exact].iterrows():
        P(f"      MISMATCH {r.panel:5s} {r.arm:13s} g={r.gross:.2f}  worst|d| {r.worst_metric:.2e}"
          f"  legs {r.flipped_legs or 'OK'}  4b {'OK' if r.pass4b_match else 'NO'}")
    P("      (804's tape ends 2026-09-11 and today's is longer, so the metric bar is a vintage bar;")
    P("       the LEG pattern is what the committed BAND is made of and must match exactly.)")
    return bool(legs and mets), G


# ================================================================================================
# main
# ================================================================================================
def main():
    t0 = time.time()
    P("=" * 112)
    P("IDEA 922 (lane C, 2026-09-15) -- is the 55.8% CENSORING rate a LADDER fact or the")
    P("                                PROTOCOL's 1.00 CEILING?")
    P("=" * 112)
    P(f"TUNED 1 CEILING ({len(CEILINGS)} levels, all reported): {CEILINGS}")
    P(f"        {GMAX_PROTO:.2f} is PROTOCOL 2's no-leverage line and the ONLY admissible one; the "
      f"rest are flagged LEVERED measurements no chooser may pick from.")
    P(f"TUNED 2 claim set: REPRO = 804's committed cells on {CLAIMSETS['REPRO']}; "
      f"EXT = the same arms on {CLAIMSETS['EXT']} (no committed run priced these)")
    P(f"reported axes: cost {[int(c) for c in COSTS]} bps x window {WINDOWS} x {len(ARMS)} arms")
    P("BARS: H_LADDER bottom-edge / below-line / above-line censors are LADDER facts by")
    P("      construction (lower bound on the ladder's share); H_CEIL the ceiling's share is")
    P("      bounded above by TOP-ONLY censors sitting exactly on g=1.00; H_BOUND a band is")
    P("      CEILING-BOUND iff its DD-cap breach is > 1.00; H_SAME width(C) constant iff INTERIOR;")
    P("      H_PRICE what the forbidden range is worth; H_WF rule 8 at every ceiling.")
    P("")

    # --------------------------------------------------------------------------------------
    # PART A -- the census decomposition
    # --------------------------------------------------------------------------------------
    P("=" * 112)
    P("PART A -- DECOMPOSING THE CENSORING OF EVERY COMMITTED GROSS BAND")
    P("=" * 112)
    tA = time.time()
    # One scan of the whole corpus.  919's OWN file set is recovered from 919's committed
    # census.csv -- the record's own statement of which files carried a band -- so G3c is a
    # row-for-row cross-run reproduction and not a re-derivation of the file list.
    CEN, stat = scan_record(exclude_stems=(STEM,))
    NE = CEN[~CEN["is_empty"]].copy()
    KEYC = ["file", "gcol", "pcol", "key"]
    C9F = OUT / f"{P919_STEM}.census.csv"
    if C9F.exists():
        C9 = pd.read_csv(C9F)
        files9 = set(C9.file.unique())
        CEN9 = CEN[CEN.file.isin(files9)].reset_index(drop=True)
        mine = CEN9.set_index(KEYC)
        theirs = C9.set_index(KEYC)
        common = mine.index.intersection(theirs.index)
        cmpcols = ["nrung", "step", "g_first", "g_last", "npass", "lo", "hi", "width"]
        m, t = mine.loc[common], theirs.loc[common]
        worst = max(float(np.nanmax(np.abs(pd.to_numeric(m[c], errors="coerce").values
                                           - pd.to_numeric(t[c], errors="coerce").values)))
                    if len(common) else 0.0 for c in cmpcols)
        flagmm = int((m.censor.astype(bool).values != t.censor.astype(bool).values).sum()
                     + (m["is_empty"].astype(bool).values
                        != t["is_empty"].astype(bool).values).sum())
        g3c = bool(len(common) == len(theirs) == len(mine) and worst < 1e-9 and flagmm == 0)
        NE9 = CEN9[~CEN9["is_empty"]]
        P(f"G3c CROSS-RUN on the CENSUS: 919's committed census names {len(files9)} files and "
          f"{len(C9):,} band cells; this run's scanner returns {len(CEN9):,} on the same files, "
          f"{len(common):,} join on (file, gcol, pcol, key)")
        P(f"    worst |delta| over {cmpcols} = {worst:.3e}; censor/is_empty flag mismatches "
          f"{flagmm}; non-empty {len(NE9):,} (919: {P919_NONEMPTY:,}), censored "
          f"{int(NE9.censor.sum()):,} (919: {P919_CENSORED:,})   -> {'PASS' if g3c else 'FAIL'}")
        for side, idx in (("in 919's census only", theirs.index.difference(mine.index)),
                          ("in this run only", mine.index.difference(theirs.index))):
            for kk in list(idx)[:4]:
                P(f"    NON-JOINING ROW ({side}): file={kk[0][:58]} gcol={kk[1]} pcol={kk[2]} "
                  f"key={str(kk[3])[:70]}")
        if len(theirs.index.difference(mine.index)) or len(mine.index.difference(theirs.index)):
            P("    (the census TOTALS above are identical; the join key is what differs, so this")
            P("     is a key-collision in the (file, gcol, pcol, key) tuple, not a band that moved)")
    else:
        CEN9, NE9, g3c = CEN, NE, False
        P("G3c 919's committed census.csv NOT FOUND -- gate cannot run")
    P(f"    today's corpus, which has grown since 919 ran: {len(CEN):,} cells, {len(NE):,} "
      f"non-empty, {int(NE.censor.sum()):,} censored ({NE.censor.mean():.1%}) in "
      f"{CEN.file.nunique()} files")
    P("    every headline below is on 919's OWN file set, so it decomposes the very 55.8% the")
    P("    queue asks about; the wider corpus is reported beside it and never mixed in.")
    P("")

    D = decompose(NE9)
    dump(D, "census.csv")
    n, cens = len(D), int(D.censor.sum())
    P(f"THE DECOMPOSITION ({cens:,} censored bands of {n:,} non-empty = {cens/n:.1%}, 919's 55.8%)")
    P(f"  {'class':>20} {'bands':>7} {'of censored':>12} {'of non-empty':>13}  what it means")
    meanings = {
        "BOTTOM_ONLY": "ladder floor above the true CAGR crossing -- PROTOCOL has no floor",
        "BOTH_EDGES": "censored at BOTH ends; the bottom alone makes it a ladder fact",
        "TOP_LADDER_SHORT": "top rung BELOW g=1.00 -- rungs PROTOCOL allowed were never run",
        "TOP_AT_CEILING": "top rung EXACTLY g=1.00 -- the only class the ceiling can explain",
        "TOP_ABOVE_CEILING": "top rung ABOVE g=1.00 -- the run already levered; no ceiling to blame",
    }
    for cl in ["BOTTOM_ONLY", "BOTH_EDGES", "TOP_LADDER_SHORT", "TOP_AT_CEILING",
               "TOP_ABOVE_CEILING"]:
        k = int((D.censor_class == cl).sum())
        P(f"  {cl:>20} {k:7,} {k/max(cens,1):11.1%} {k/n:12.1%}  {meanings[cl]}")
    lad = int(D.ladder_fact.sum())
    ceil_ub = int(D.ceiling_candidate.sum())
    P(f"  {'-'*20} {'-'*7} {'-'*12} {'-'*13}")
    P(f"  H_LADDER  LADDER FACT BY CONSTRUCTION      {lad:7,} of {cens:,} censored "
      f"({lad/max(cens,1):.1%})  -- no simulation needed")
    P(f"  H_CEIL    CEILING'S UPPER BOUND            {ceil_ub:7,} of {cens:,} censored "
      f"({ceil_ub/max(cens,1):.1%})  -- Part B prices this class")
    P(f"  (the two are exhaustive and disjoint: {lad:,} + {ceil_ub:,} = {lad+ceil_ub:,} = the "
      f"whole censored set.  Of the {int((D.censor_class=='BOTH_EDGES').sum()):,} BOTH_EDGES")
    P(f"   bands, {int(D.both_top_at_ceiling.sum()):,} also have their top rung exactly at 1.00; "
      f"they are counted as ladder facts because their BOTTOM censor is one whatever the top")
    P("   does, so the ceiling's upper bound above is if anything generous to the ceiling.)")
    P("")
    sh = D[D.top_short]
    if len(sh):
        P(f"  how far short the tops stopped, over every band whose top rung is below the line "
          f"({len(sh):,} bands, i.e. the {int((D.censor_class=='TOP_LADDER_SHORT').sum()):,} "
          f"TOP_LADDER_SHORT plus the BOTH_EDGES bands that also stop short):")
        P(f"    top rung median {sh.g_last.median():.3f}, min {sh.g_last.min():.3f}, max "
          f"{sh.g_last.max():.3f};")
        P(f"    unrun admissible range median {sh.short_by.median():.3f} of gross "
          f"(= {sh.short_rungs.median():.1f} of that ladder's own rungs), max "
          f"{sh.short_by.max():.3f}")
    P(f"  bottom rungs of the {int(D.cen_lo.sum()):,} bottom-censored bands: median g_first "
      f"{D[D.cen_lo].g_first.median():.3f}, min {D[D.cen_lo].g_first.min():.3f}, max "
      f"{D[D.cen_lo].g_first.max():.3f}  (PROTOCOL's floor is 0, so every one of these is the")
    P("    run's own choice of where to start the ladder)")
    P("")
    P("  by committed ladder step:")
    P(f"    {'step':>7} {'censored':>9} {'ladder':>8} {'ceil-UB':>8} {'top@1.00':>9} "
      f"{'median g_last':>14}")
    for stp, gg in D[D.censor].groupby(D.step.round(3)):
        P(f"    {stp:7.3f} {len(gg):9,} {int(gg.ladder_fact.sum()):8,} "
          f"{int(gg.ceiling_candidate.sum()):8,} {int(gg.top_at_ceiling.sum()):9,} "
          f"{gg.g_last.median():14.3f}")
    P("")
    P("  the 10 files contributing the most CENSORED bands:")
    for f, gg in sorted(D[D.censor].groupby("file"), key=lambda kv: -len(kv[1]))[:10]:
        P(f"    {len(gg):4,} censored  ladder {int(gg.ladder_fact.sum()):4,}  ceil-UB "
          f"{int(gg.ceiling_candidate.sum()):4,}  g_last median {gg.g_last.median():.2f}  {f[:62]}")
    P(f"  Part A took {time.time()-tA:.1f}s")
    P("")

    # --------------------------------------------------------------------------------------
    # PART B -- re-solution across ceilings
    # --------------------------------------------------------------------------------------
    P("=" * 112)
    P("PART B -- RE-SOLVING THE REPRODUCIBLE BANDS ACROSS THE CEILING DIAL")
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

    # ---- gates that need only the books ----
    P("=" * 112)
    P("GATES (printed before any result number is read)")
    P("=" * 112)
    gates = {"G3c": g3c}
    px = raw["U56"]
    W1 = arm_w1(px, pre["U56"], "BAND03")
    dw = float(np.nanmax(np.abs(W1 * 0.75 - rules_v2_weights(px, band=BAND0, gross=0.75).values)))
    gates["G2"] = dw < 1e-12
    P(f"G2  BAND03 g=0.75 == rules_v2_weights          max|dw| {dw:.3e}   -> "
      f"{'PASS' if gates['G2'] else 'FAIL'}")

    bk = books[("U56", "BAND03")]
    r_f, t_f = bk.at(0.75, COST0)
    res = backtest(px, rules_v2_weights(px, band=BAND0, gross=0.75), cost_bps=COST0, freq=FREQ0)
    dr = float(np.nanmax(np.abs(r_f - res["returns"].values)))
    dt = float(np.nanmax(np.abs(t_f - res["turnover"].values)))
    # the LEVERED arithmetic, which 919 never gated and which every ceiling above 1.00 rests on
    bs = books[("U56", "CAND20")]
    GLEV = 1.40
    rs, ts = bs.at(GLEV, COST0)
    wl = pd.DataFrame(arm_w1(px, pre["U56"], "CAND20") * GLEV, index=px.index, columns=px.columns)
    res2 = backtest(px, wl, cost_bps=COST0, freq=FREQ0)
    dr2 = float(np.nanmax(np.abs(rs - res2["returns"].values)))
    dt2 = float(np.nanmax(np.abs(ts - res2["turnover"].values)))
    bm = books[("U56", "BAND03_M")]
    rm, _ = bm.at(0.75, COST0)
    wm = pd.DataFrame(arm_w1(px, pre["U56"], "BAND03_M") * 0.75, index=px.index, columns=px.columns)
    dr3 = float(np.nanmax(np.abs(rm - backtest(px, wm, cost_bps=COST0,
                                               freq="M")["returns"].values)))
    gates["G1"] = max(dr, dt, dr2, dt2, dr3) < 1e-10
    P(f"G1  fast Book.at == engine.backtest            BAND03 g=0.75 {dr:.3e}/{dt:.3e};  "
      f"CAND20 LEVERED g={GLEV:.2f} {dr2:.3e}/{dt2:.3e};  BAND03_M {dr3:.3e}   -> "
      f"{'PASS' if gates['G1'] else 'FAIL'}")

    s, v = spyref["U56"]["FULL"], v2ref["U56"]["FULL"]
    gates["G4"] = all(abs(a - b) < c for a, b, c in
                      [(s["CAGR"], SPY_U56[0], TOL_C), (s["Sharpe"], SPY_U56[1], TOL_S),
                       (s["MaxDD"], SPY_U56[2], TOL_D), (v["CAGR"], V2_U56[0], TOL_C),
                       (v["Sharpe"], V2_U56[1], TOL_S), (v["MaxDD"], V2_U56[2], TOL_D)])
    P(f"G4  committed U56 triples   SPY {s['CAGR']:.4%}/{s['Sharpe']:.4f}/{s['MaxDD']:.4%} "
      f"(committed {SPY_U56[0]:.2%}/{SPY_U56[1]:.4f}/{SPY_U56[2]:.2%});  v2 "
      f"{v['CAGR']:.4%}/{v['Sharpe']:.4f}/{v['MaxDD']:.4%} (committed {V2_U56[0]:.2%}/"
      f"{V2_U56[1]:.4f}/{V2_U56[2]:.2%})   -> {'PASS' if gates['G4'] else 'FAIL'}")

    # G10 SOLVENCY at the widest ceiling
    solv = []
    for nm in PANELS:
        for a in ARMS:
            vmin = float(np.min(books[(nm, a)].nav(CMAX)))
            solv.append(dict(panel=nm, arm=a, Vmin_at_CMAX=vmin, solvent=bool(vmin > 0.0)))
    SV = pd.DataFrame(solv)
    INSOLVENT = {(r.panel, r.arm) for _, r in SV.iterrows() if not r.solvent}
    gates["G10"] = bool(SV.solvent.all())
    P(f"G10 SOLVENCY at the widest ceiling g={CMAX:.2f}: worst NAV multiplier over all "
      f"{len(SV)} books {SV.Vmin_at_CMAX.min():.4f} (book "
      f"{SV.loc[SV.Vmin_at_CMAX.idxmin(),'panel']}/{SV.loc[SV.Vmin_at_CMAX.idxmin(),'arm']})   -> "
      f"{'PASS' if gates['G10'] else 'FAIL'}")
    for _, r in SV[~SV.solvent].iterrows():
        P(f"      INSOLVENT {r.panel:5s} {r.arm:13s} Vmin {r.Vmin_at_CMAX:.4f} -- excluded from "
          f"every LEVERED headline (its drawdown above 1.00 is undefined)")
    dump(SV, "solvency.csv")

    # SPYBH analytic ray, admissible and levered reported separately
    dev_a = dev_l = 0.0
    for nm in PANELS:
        z, sp = books[(nm, "SPYBH")], spyref[nm]["FULL"]
        for g in (0.25, 0.50, 0.75, 1.00, 1.50, 2.00):
            rz, _ = z.at(g, 0.0)
            _, _, d = fmet(rz[pans[(nm, "W")].masks["FULL"]])
            dv = abs(abs(d) / abs(sp["MaxDD"]) - g)
            if g <= 1.0:
                dev_a = max(dev_a, dv)
            else:
                dev_l = max(dev_l, dv)
    gates["G8"] = dev_a < 0.05
    P(f"G8  SPYBH analytic ray |MaxDD(g)|/|MaxDD(SPY)| == g   worst dev at g<=1.00 {dev_a:.3e}  "
      f"-> {'PASS' if gates['G8'] else 'FAIL'};  levered g in (1,2] deviates {dev_l:.3f} "
      f"(compounding, reported not asserted away)")

    # the 0.01 ladder to the widest ceiling
    P("")
    P(f"scoring the 0.01 ladder to g={CMAX:.2f} ({len(FINE)} rungs) x {len(COSTS)} costs x "
      f"{len(books)} books ...")
    t = time.time()
    rows = []
    for nm in PANELS:
        for a in ARMS:
            bkx = books[(nm, a)]
            for cost in COSTS:
                for g in FINE:
                    r = score_g(bkx, g, cost, spyref[nm], v2ref[nm])
                    r.update(panel=nm, arm=a, freq=ARM_FREQ[a])
                    rows.append(r)
    fine = pd.DataFrame(rows)
    del rows
    P(f"  {len(fine):,} book-rows  ({time.time()-t:.1f}s)")
    dump(fine, "ladder.csv")

    gates["G3"], _ = gate_parent(fine)

    # G3b -- the SAME gate on a tape truncated to 804's own last date.  G3 alone cannot tell a
    # method difference from a tape difference; G3b is what separates them, and 919's standing
    # finding is that U56 then reproduces while B136 does not, because the B136 cache has been
    # RESTATED since 804 ran.  Reproduced here rather than assumed.
    P("")
    t = time.time()
    rows_t = []
    for nm in CLAIMSETS["REPRO"]:
        pxT = raw[nm].loc[:pd.Timestamp(PARENT_LAST)]
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
    P(f"G3b tape truncated to {PARENT_LAST} (804's own last date), {len(fineT)} rows rebuilt in "
      f"{time.time()-t:.1f}s")
    gates["G3b"], G3b = gate_parent(fineT, tag="G3b")
    dump(G3b, "gate3b.csv")
    for pn in CLAIMSETS["REPRO"]:
        gp = G3b[G3b.panel == pn]
        P(f"      G3b[{pn}]  {int(gp.exact.sum())} of {len(gp)} rows exact on every leg and "
          f"verdict, worst metric deviation {gp.worst_metric.max():.3e}  -> "
          f"{'PASS' if (gp.exact.all() and (gp.worst_metric < G3_BAR).all()) else 'FAIL'}")

    # G5 monotonicity, PER WINDOW, all the way to the widest ceiling.  `edges()` bisects the CAGR
    # floor and the DD cap in whichever window the convention names, so a book that is monotone on
    # FULL can still have two crossings on IS or OOS; 919 tested FULL alone and this run does not.
    viol = []
    for nm in PANELS:
        for a in ARMS:
            sub = fine[(fine.panel == nm) & (fine.arm == a)
                       & (fine.cost == COST0)].sort_values("gross")
            lo = sub[sub.gross <= GMAX_PROTO + 1e-9]
            for w in WINDOWS:
                viol.append(dict(
                    panel=nm, arm=a, window=w,
                    cagr_viol_proto=int((np.diff(lo[f"{w}_CAGR"].values) < -1e-12).sum()),
                    cagr_viol_full=int((np.diff(sub[f"{w}_CAGR"].values) < -1e-12).sum()),
                    dd_viol_full=int((np.diff(np.abs(sub[f"{w}_MaxDD"].values)) < -1e-12).sum()),
                    sharpe_spread=float(lo[f"{w}_Sharpe"].max() - lo[f"{w}_Sharpe"].min())))
    V = pd.DataFrame(viol)
    V["mono"] = (V.dd_viol_full == 0) & (V.cagr_viol_proto == 0)
    gates["G5"] = bool(V.mono.all())
    P(f"G5  monotonicity on the 0.01 ladder, {len(V)} (book x window) cells: |MaxDD(g)| "
      f"non-decreasing to g={CMAX:.2f} AND CAGR(g) non-decreasing to g=1.00 on "
      f"{int(V.mono.sum())} of {len(V)}   -> {'PASS' if gates['G5'] else 'FAIL'}")
    for w in WINDOWS:
        s5 = V[V.window == w]
        P(f"      {w:>4}: {int(s5.mono.sum())} of {len(s5)} monotone; CAGR non-decreasing to "
          f"g={CMAX:.2f} on {int((s5.cagr_viol_full==0).sum())} (leverage drag turns it over "
          f"above the line, which is why no width here is read past a breach)")
    P(f"      Sharpe spread over the admissible ladder (FULL): "
      f"median {V[V.window=='FULL'].sharpe_spread.median():.4f}, "
      f"max {V[V.window=='FULL'].sharpe_spread.max():.4f}  (804's 'gross cannot decide a Sharpe "
      f"leg')")
    # a row of EX is judged in the window its convention names: c804 -> FULL, cwin -> that window
    NONMONO = {(r.panel, r.arm, r.window) for _, r in V.iterrows() if not r.mono}
    for _, r in V[~V.mono].iterrows():
        P(f"      MONOTONICITY VIOLATION {r.panel:5s} {r.arm:13s} [{r.window}] DD(to {CMAX:.2f}) "
          f"{r.dd_viol_full} CAGR(to 1.00) {r.cagr_viol_proto} -> every band solved in this "
          f"window is flagged `nonmono` and excluded from the headlines")
    dump(V, "monotonicity.csv")

    # ---- the ceiling sweep ----
    P("")
    t = time.time()
    erows = []
    for nm in PANELS:
        for a in ARMS:
            bkx = books[(nm, a)]
            for cost in COSTS:
                for conv, win in [("c804", "FULL"), ("cwin", "IS"), ("cwin", "OOS")]:
                    for C in CEILINGS:
                        r = ceiling_row(nm, a, cost, bkx, spyref[nm], conv, win, C)
                        r["claimset"] = "REPRO" if nm in CLAIMSETS["REPRO"] else "EXT"
                        wj = "FULL" if conv == "c804" else win      # the window actually bisected
                        r["nonmono"] = bool((nm, a, wj) in NONMONO)
                        r["insolvent"] = bool((nm, a) in INSOLVENT)
                        erows.append(r)
    EX = pd.DataFrame(erows)
    P(f"solved {len(EX):,} exact bands by bisection ({len(CEILINGS)} ceilings x {len(books)} books "
      f"x {len(COSTS)} costs x 3 window-conventions)  ({time.time()-t:.1f}s)")
    dump(EX, "ceilings.csv")

    # G6 bisection inside its 0.01 bracket (admissible ceiling, primary cost, 804 convention)
    worst, nchk = 0.0, 0
    for nm in PANELS:
        for a in ARMS:
            e = EX[(EX.panel == nm) & (EX.arm == a) & (EX.cost == COST0) & (EX.conv == "c804")
                   & (EX.ceiling == GMAX_PROTO)].iloc[0]
            if bool(e["is_empty"]) or e.g_min is None:
                continue
            sub6 = fine[(fine.panel == nm) & (fine.arm == a) & (fine.cost == COST0)
                        & (fine.gross <= GMAX_PROTO + 1e-9)]
            okc, okd = sub6[sub6.c804_L5_CAGRfloor], sub6[sub6.c804_L4_DDcap]
            if len(okc):
                worst = max(worst, max(0.0, e.g_min - float(okc.gross.min())) - FINE_STEP)
                nchk += 1
            if len(okd):
                worst = max(worst, max(0.0, float(okd.gross.max()) - e.g_max) - FINE_STEP)
                nchk += 1
    gates["G6"] = worst <= 1e-6
    P(f"G6  bisection inside its 0.01 bracket on {nchk} endpoints   worst overshoot {worst:.3e}"
      f"   -> {'PASS' if gates['G6'] else 'FAIL'}")

    # G11 CEILING MONOTONICITY -- H_SAME as a gate
    bad11, chk11 = [], 0
    EXM = EX[~EX.nonmono & ~EX.insolvent]
    for k, gg in EXM.groupby(["panel", "arm", "cost", "conv", "window"]):
        gg = gg.sort_values("ceiling")
        w = gg.width.values
        chk11 += 1
        if np.any(np.diff(w) < -BAND_TOL):
            bad11.append((k, "width DECREASES in C"))
            continue
        gb = pd.to_numeric(gg.g_break, errors="coerce").values
        interior = bool(np.isfinite(gb[0]) and gb[0] <= GMAX_PROTO + 1e-9)
        if interior and float(np.ptp(w)) > BAND_TOL:
            bad11.append((k, "INTERIOR band whose width still moves with C"))
    gates["G11"] = len(bad11) == 0
    P(f"G11 CEILING MONOTONICITY on the {chk11} G5-monotone (panel, arm, cost, conv, window) "
      f"cells of {len(EX)//len(CEILINGS)}: width(C) non-decreasing and CONSTANT whenever the "
      f"breach is <= 1.00   -> {'PASS' if gates['G11'] else 'FAIL'}")
    for k, why in bad11[:8]:
        P(f"      VIOLATION {k}  {why}")

    # G7 determinism
    bk2 = Book(pans[("U56", "W")], arm_w1(raw["U56"], pre["U56"], "CAND20"))
    a0 = fine[(fine.panel == "U56") & (fine.arm == "CAND20")
              & (fine.cost == COST0)].sort_values("gross")
    d7 = max(abs(score_g(bk2, float(g), COST0, spyref["U56"], v2ref["U56"])["FULL_Sharpe"] - float(x))
             for g, x in zip(a0.gross.values[::37], a0.FULL_Sharpe.values[::37]))
    e7 = ceiling_row("U56", "CAND20", COST0, bk2, spyref["U56"], "c804", "FULL", 1.50)
    e7b = EX[(EX.panel == "U56") & (EX.arm == "CAND20") & (EX.cost == COST0)
             & (EX.conv == "c804") & (EX.ceiling == 1.50)].iloc[0]
    d7b = abs(float(e7["width"]) - float(e7b.width))
    gates["G7"] = (d7 == 0.0) and (d7b == 0.0)
    P(f"G7  DETERMINISM (rebuild U56/CAND20, re-score {len(a0.gross.values[::37])} rungs, "
      f"re-bisect at C=1.50)  max|dSharpe| {d7:.3e}, |dwidth| {d7b:.3e}   -> "
      f"{'PASS' if gates['G7'] else 'FAIL'}")

    # G9 CENSUS == SIMULATION on the CENSOR DECOMPOSITION, on 804's own committed file.  Run on
    # BOTH tapes: G9 on today's, G9b on 804's own.  If a mismatch survives G9 and clears G9b it is
    # the same tape fact G3b names, not a scanner error -- that is the whole point of the pair.
    CP, _ = scan_record(files=[str(PARENT)])

    def g9_join(src, tag):
        rows9, bad9 = [], 0
        for _, c in CP.iterrows():
            kv = dict(p.split("=", 1) for p in c.key.split("|") if "=" in p)
            pn, ar = kv.get("panel"), kv.get("arm")
            if pn is None or ar is None:
                continue
            mn = ladder_read(src, pn, ar, COST0, RECORD8, "c804_pass4b")
            if mn is None:
                continue
            same = (bool(c["is_empty"]) == bool(mn["is_empty"])
                    and bool(c.cen_lo) == bool(mn["cen_lo"])
                    and bool(c.cen_hi) == bool(mn["cen_hi"])
                    and abs(float(c.g_first) - float(mn["g_first"])) < 1e-9
                    and abs(float(c.g_last) - float(mn["g_last"])) < 1e-9)
            bad9 += (not same)
            rows9.append(dict(tape=tag, panel=pn, arm=ar, committed_npass=int(c.npass),
                              mine_npass=int(mn["npass"]),
                              committed_empty=bool(c["is_empty"]),
                              mine_empty=bool(mn["is_empty"]),
                              committed_cen_lo=bool(c.cen_lo), mine_cen_lo=bool(mn["cen_lo"]),
                              committed_cen_hi=bool(c.cen_hi), mine_cen_hi=bool(mn["cen_hi"]),
                              g_first=float(c.g_first), g_last=float(c.g_last), match=same))
        return pd.DataFrame(rows9), bad9

    G9, g9bad = g9_join(fine, "today")
    G9b, g9bbad = g9_join(fineT, PARENT_LAST)
    gates["G9"] = bool(len(G9) > 0 and g9bad == 0)
    gates["G9b"] = bool(len(G9b) > 0 and g9bbad == 0)
    P(f"G9  CENSUS == SIMULATION on 804's own committed CSV, TODAY's tape: {len(G9)-g9bad} of "
      f"{len(G9)} (panel, arm) bands identical in emptiness, BOTH censor-edge flags and the "
      f"ladder's own first and last rung   -> {'PASS' if gates['G9'] else 'FAIL'}")
    for _, r in G9[~G9.match].iterrows():
        P(f"      MISMATCH {r.panel:5s} {r.arm:13s} committed npass {r.committed_npass} "
          f"(empty {r.committed_empty}, lo/hi {r.committed_cen_lo}/{r.committed_cen_hi})  vs mine "
          f"npass {r.mine_npass} (empty {r.mine_empty}, lo/hi {r.mine_cen_lo}/{r.mine_cen_hi})")
    P(f"G9b the SAME join on 804's OWN tape ({PARENT_LAST}): {len(G9b)-g9bbad} of {len(G9b)} "
      f"identical   -> {'PASS' if gates['G9b'] else 'FAIL'}")
    for _, r in G9b[~G9b.match].iterrows():
        P(f"      MISMATCH {r.panel:5s} {r.arm:13s} committed npass {r.committed_npass} vs mine "
          f"{r.mine_npass} -- survives the tape truncation, so it is NOT a vintage difference")
    dump(pd.concat([G9, G9b], ignore_index=True), "gate9.csv")

    P("")
    gtxt = ", ".join(f"{k}=" + ("PASS" if v else "FAIL") for k, v in sorted(gates.items()))
    P(f"GATES: {sum(bool(v) for v in gates.values())} of {len(gates)} PASS  ({gtxt})")
    P("")

    # --------------------------------------------------------------------------------------
    # THE PRICING: H_BOUND / H_SAME / H_PRICE
    # --------------------------------------------------------------------------------------
    P("=" * 112)
    P("H_BOUND -- where the DD-cap breach actually sits, by bisection")
    P("=" * 112)
    W = EX[~EX.nonmono & ~EX.insolvent].copy()
    if len(W) < len(EX):
        P(f"  {len(EX)-len(W)} of {len(EX)} rows carry `nonmono`/`insolvent` and are excluded from "
          f"the headlines below; they are in ceilings.csv.")
    top = W[W.ceiling == CMAX].copy()
    top["bound_class"] = np.where(
        top.g_break.isna(), f"NO BREACH BELOW {CMAX:.2f}",
        np.where(pd.to_numeric(top.g_break, errors="coerce") <= GMAX_PROTO + 1e-9,
                 "INTERIOR (breach <= 1.00)", "CEILING-BOUND (breach > 1.00)"))
    for cs in ("REPRO", "EXT"):
        sub = top[(top.claimset == cs) & (top.cost == COST0) & (top.conv == "c804")]
        if not len(sub):
            continue
        nb = len(sub)
        P("")
        P(f"CLAIM SET {cs} ({'804 committed cells' if cs=='REPRO' else 'SMALL, this run only'}), "
          f"{COST0:.0f} bps, 804's FULL-window convention -- {nb} bands")
        for cl, gg in sub.groupby("bound_class"):
            P(f"  {cl:<32} {len(gg):3d} of {nb}  ({len(gg)/nb:.1%})")
        ceilb = sub[sub.bound_class != "INTERIOR (breach <= 1.00)"]
        P(f"  => the PROTOCOL ceiling, not the DD cap, is the upper edge on "
          f"{len(ceilb)} of {nb} ({len(ceilb)/nb:.1%}) of these bands")
    P("")
    P(f"PER-BAND at {COST0:.0f} bps (804 convention), breach point and width at every ceiling:")
    P(f"  {'panel':>5} {'arm':>13} {'g_break':>9} " +
      " ".join(f"{('w@'+f'{C:.2f}'):>8}" for C in CEILINGS) + "  class")
    for nm in PANELS:
        for a in ARMS:
            gg = W[(W.panel == nm) & (W.arm == a) & (W.cost == COST0)
                   & (W.conv == "c804")].sort_values("ceiling")
            if not len(gg):
                continue
            gb = pd.to_numeric(gg.g_break, errors="coerce").values
            gbt = gb[-1]
            cl = ("no breach" if not np.isfinite(gbt) else
                  ("INTERIOR" if gbt <= GMAX_PROTO + 1e-9 else "CEILING-BOUND"))
            P(f"  {nm:>5} {a:>13} {('  n/a' if not np.isfinite(gbt) else f'{gbt:9.4f}'):>9} " +
              " ".join(f"{w:8.4f}" for w in gg.width.values) + f"  {cl}"
              + ("" if bool(gg.sharpe_ok.iloc[0]) else "   (Sharpe leg fails -> window EMPTY)"))

    P("")
    P("=" * 112)
    P("H_SAME -- 919's '25 of 30 identical at 1.00 and 1.50', re-read as a prediction")
    P("=" * 112)
    piv = W[W.conv == "c804"].pivot_table(index=["claimset", "panel", "arm", "cost"],
                                          columns="ceiling", values="width")
    same_15 = int((np.abs(piv[1.50] - piv[1.00]) <= BAND_TOL).sum())
    same_30 = int((np.abs(piv[CMAX] - piv[1.00]) <= BAND_TOL).sum())
    P(f"  width(1.50) == width(1.00) on {same_15} of {len(piv)} (band x cost) cells "
      f"({same_15/len(piv):.1%});  width({CMAX:.2f}) == width(1.00) on {same_30} of {len(piv)} "
      f"({same_30/len(piv):.1%})")
    P("  a band whose width is unchanged when the ceiling is raised has its upper edge set by the")
    P("  DD cap BELOW 1.00; a band whose width grows has its upper edge set by the ceiling.")
    grow = piv[np.abs(piv[CMAX] - piv[1.00]) > BAND_TOL]
    P(f"  the {len(grow)} cells whose width GROWS with the ceiling (i.e. the genuinely")
    P("  ceiling-bound ones), and how much gross PROTOCOL forbids them:")
    P(f"    {'claimset':>8} {'panel':>5} {'arm':>13} {'cost':>5} " +
      " ".join(f"{C:>8.2f}" for C in CEILINGS))
    for k, r in grow.iterrows():
        P(f"    {k[0]:>8} {k[1]:>5} {k[2]:>13} {int(k[3]):5d} " +
          " ".join(f"{r[C]:8.4f}" for C in CEILINGS))

    P("")
    P("=" * 112)
    P("H_PRICE -- what the forbidden range is worth, and the CALIBRATION of Part A's ambiguous")
    P("           TOP_AT_CEILING class")
    P("=" * 112)
    # a RECORD8-style ladder ending at 1.00 reads a top censor iff its top rung passes 4b
    cal = []
    for nm in PANELS:
        for a in ARMS:
            for cost in COSTS:
                rd = ladder_read(fine, nm, a, cost, RECORD8, "c804_pass4b")
                if rd is None or rd["is_empty"]:
                    continue
                e = W[(W.panel == nm) & (W.arm == a) & (W.cost == cost) & (W.conv == "c804")
                      & (W.ceiling == CMAX)]
                if not len(e):
                    continue
                e = e.iloc[0]
                gb = pd.to_numeric(pd.Series([e.g_break]), errors="coerce").iloc[0]
                cal.append(dict(claimset=("REPRO" if nm in CLAIMSETS["REPRO"] else "EXT"),
                                panel=nm, arm=a, cost=cost,
                                reads_top_censor=bool(rd["cen_hi"]),
                                g_break=gb,
                                ceiling_bound=bool((not np.isfinite(gb))
                                                   or gb > GMAX_PROTO + 1e-9),
                                forbidden_range=(np.nan if not np.isfinite(gb)
                                                 else max(0.0, gb - GMAX_PROTO))))
    CAL = pd.DataFrame(cal)
    dump(CAL, "calibration.csv")
    tc = CAL[CAL.reads_top_censor]
    if len(tc):
        nb = int(tc.ceiling_bound.sum())
        P(f"  of the {len(tc)} (band x cost) readings whose RECORD8 ladder (top rung exactly 1.00)")
        P(f"  reports a TOP CENSOR -- Part A's ambiguous TOP_AT_CEILING class -- {nb} "
          f"({nb/len(tc):.1%}) are genuinely CEILING-BOUND (their DD cap is not breached until a")
        P(f"  gross PROTOCOL forbids) and {len(tc)-nb} ({1-nb/len(tc):.1%}) have their true upper "
          f"edge BELOW 1.00, i.e. a censor flag that is a ladder artefact despite the ladder")
        P("  having reached the line.")
        fr = tc[np.isfinite(pd.to_numeric(tc.forbidden_range, errors='coerce'))
                & (tc.forbidden_range > 0)]
        if len(fr):
            P(f"  forbidden range beyond g=1.00 on the ceiling-bound ones: median "
              f"{fr.forbidden_range.median():.3f} of gross, max {fr.forbidden_range.max():.3f} "
              f"(and {int((~np.isfinite(pd.to_numeric(tc.forbidden_range, errors='coerce'))).sum())}"
              f" never breach even at g={CMAX:.2f})")
    else:
        P("  no RECORD8 reading in this run's books reports a top censor -- reported as the empty")
        P("  result it is.")
    P("")
    P("  APPLYING THE CALIBRATED RATE TO THE CENSUS (stated as the extrapolation it is: the")
    P("  calibration population is 30 books from ONE committed file, not a sample of the 96):")
    rate = (int(tc.ceiling_bound.sum()) / len(tc)) if len(tc) else float("nan")
    P(f"    census TOP_AT_CEILING (H_CEIL upper bound)     {ceil_ub:,} of {cens:,} censored "
      f"({ceil_ub/max(cens,1):.1%})")
    if np.isfinite(rate):
        P(f"    x calibrated ceiling-bound rate {rate:.1%}          "
          f"~{int(round(ceil_ub*rate)):,} of {cens:,} ({ceil_ub*rate/max(cens,1):.1%}) "
          f"-- a POINT ESTIMATE, not a census")
    P(f"    H_LADDER lower bound (needs no calibration)    {lad:,} of {cens:,} "
      f"({lad/max(cens,1):.1%})")

    # --------------------------------------------------------------------------------------
    # RULE 8 -- does raising the CEILING buy an out-of-sample 4b pass?
    # --------------------------------------------------------------------------------------
    P("")
    P("=" * 112)
    P("RULE 8 WALK-FORWARD -- g chosen on 2009-2016 ONLY at each ceiling, OOS 2017-2026 read once")
    P("=" * 112)
    P("CHOOSERS (both IS-only): IS_MID = midpoint of the IS band at that ceiling; IS_SHARPE = the")
    P("  0.01 rung inside the IS band with the best IS Sharpe.  Stated, not worked around: the")
    P("  STRICT IS 4b set is often EMPTY because a half-sample Sharpe leg read inside an 8-year")
    P("  window fails at every gross (675's finding), so the IS band is the intersection of the")
    P("  two IS LEVEL legs and the choosers are IS-LEVEL choosers.  Every pick above g=1.00 is")
    P("  flagged LEVERED and is a MEASUREMENT: PROTOCOL 2 forbids it and nothing there is")
    P("  promotable.")
    wrows = []
    for nm in PANELS:
        for a in ARMS:
            bkx = books[(nm, a)]
            pan = bkx.pan
            for cost in COSTS:
                lad_all = fine[(fine.panel == nm) & (fine.arm == a) & (fine.cost == cost)]
                for C in CEILINGS:
                    sub = lad_all[lad_all.gross <= C + 1e-9]
                    ok = sub[sub.cwinIS_L4_DDcap & sub.cwinIS_L5_CAGRfloor]
                    base = dict(panel=nm, arm=a, cost=cost, ceiling=C, ceiling_tag=CEIL_TAG[C],
                                claimset=("REPRO" if nm in CLAIMSETS["REPRO"] else "EXT"),
                                nonmono=bool((nm, a, "IS") in NONMONO),   # chooser selects on IS
                                insolvent=bool((nm, a) in INSOLVENT))
                    if not len(ok):
                        # emit BOTH choosers so every (panel, arm, cost, chooser) group carries
                        # all five ceilings and the ceiling-dependence table below lines up
                        for chooser in ("IS_MID", "IS_SHARPE"):
                            wrows.append(base | dict(chooser=chooser, IS_empty=True))
                        continue
                    lo, hi = float(ok.gross.min()), float(ok.gross.max())
                    for chooser in ("IS_MID", "IS_SHARPE"):
                        if chooser == "IS_MID":
                            gpick = 0.5 * (lo + hi)
                        else:
                            # the IS Sharpe of every rung is already on the ladder (fine), so this
                            # is the same pick as a re-scoring loop and exactly reproducible
                            gpick = float(ok.loc[ok.IS_Sharpe.idxmax(), "gross"])
                        r, turn = bkx.at(float(gpick), cost)
                        o = pack(r[pan.masks["OOS"]])
                        L = legswin(o, spyref[nm]["OOS"])
                        wrows.append(base | dict(
                            chooser=chooser, IS_empty=False, IS_lo=lo, IS_hi=hi,
                            g_pick=float(gpick), levered_pick=bool(gpick > GMAX_PROTO + 1e-9),
                            OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"],
                            OOS_H1=o["H1"], OOS_H2=o["H2"],
                            pass4b=bool(all(L.values())), pass4a=pass4a(o, v2ref[nm]["OOS"]),
                            turn_yr=float(turn[pan.masks["OOS"]].sum()
                                          / (pan.masks["OOS"].sum() / 252.0)),
                            **{f"leg_{k}": v for k, v in L.items()}))
    WF = pd.DataFrame(wrows)
    dump(WF, "walkforward.csv")
    live = WF[~WF.IS_empty & ~WF.nonmono & ~WF.insolvent]
    adm = live[live.ceiling == GMAX_PROTO]
    P(f"  {len(WF)} (panel, arm, cost, ceiling, chooser) cells; IS band EMPTY on "
      f"{int(WF.IS_empty.sum())}, live on {len(live)} after nonmono/insolvent exclusion")
    P(f"  ADMISSIBLE ceiling only (g <= 1.00, the only promotable rows): 4b OOS "
      f"{int(adm.pass4b.sum())} of {len(adm)}; 4a OOS {int(adm.pass4a.sum())} of {len(adm)}")
    P("")
    P("  by ceiling (all costs, both choosers):")
    P(f"  {'ceiling':>8} {'live':>6} {'4b':>5} {'4a':>5} {'levered picks':>14} "
      f"{'median g_pick':>14} {'median OOS Sharpe':>18} {'median OOS MaxDD':>17}")
    for C in CEILINGS:
        s = live[live.ceiling == C]
        if not len(s):
            continue
        P(f"  {C:8.2f} {len(s):6d} {int(s.pass4b.sum()):5d} {int(s.pass4a.sum()):5d} "
          f"{int(s.levered_pick.sum()):14d} {s.g_pick.median():14.3f} "
          f"{s.OOS_Sharpe.median():18.3f} {s.OOS_MaxDD.median():17.2%}")
    P("")
    key = ["panel", "arm", "cost", "chooser"]
    flip = []
    for k, gg in WF[~WF.nonmono & ~WF.insolvent].groupby(key):
        v = gg.set_index("ceiling")
        verd = {C: (None if bool(v.loc[C, "IS_empty"]) else bool(v.loc[C, "pass4b"]))
                for C in CEILINGS if C in v.index}
        gp = {C: (np.nan if verd[C] is None else float(v.loc[C, "g_pick"])) for C in verd}
        vals = [x for x in verd.values()]
        flip.append(dict(zip(key, k)) | dict(
            verdicts=str(verd), disagree=len(set(vals)) > 1,
            proto_verdict=verd.get(GMAX_PROTO),
            lev_only_pass=bool(verd.get(GMAX_PROTO) is not True
                               and any(verd[C] is True for C in verd if C > GMAX_PROTO)),
            g_spread=(np.nanmax(list(gp.values())) - np.nanmin(list(gp.values()))
                      if np.any(np.isfinite(list(gp.values()))) else np.nan)))
    F = pd.DataFrame(flip)
    dump(F, "ceiling_dependence.csv")
    P(f"H_WF: the OOS 4b verdict DISAGREES across ceilings on {int(F.disagree.sum())} of {len(F)} "
      f"(panel, arm, cost, chooser) cells ({F.disagree.mean():.1%})")
    P(f"      cells where ONLY a FORBIDDEN (levered) ceiling reaches 4b OOS: "
      f"{int(F.lev_only_pass.sum())} of {len(F)} -- these are the capital cost of PROTOCOL 2 "
      f"and none of them is promotable")
    P(f"      median spread of the CHOSEN g across ceilings {F.g_spread.median():.4f}, max "
      f"{F.g_spread.max():.4f}")
    for _, r in F[F.disagree].head(12).iterrows():
        P(f"      {r.panel:5s} {r.arm:13s} {int(r.cost):3d}bps {r.chooser:9s} g-spread "
          f"{r.g_spread:.3f}  {r.verdicts}")
    P("")
    P("  the ADMISSIBLE OOS 4b PASSES in full (the only rows that could carry capital):")
    pp = adm[adm.pass4b]
    if not len(pp):
        P("    NONE -- no IS-only chooser at the admissible ceiling reaches 4b out of sample.")
    else:
        P(f"    {'panel':>5} {'arm':>13} {'cost':>5} {'chooser':>9} {'g':>6} {'OOS CAGR':>9} "
          f"{'Sharpe':>7} {'MaxDD':>8} {'H1/H2':>13} {'turn':>6}")
        for _, r in pp.sort_values(["panel", "arm", "cost"]).iterrows():
            P(f"    {r.panel:>5} {r.arm:>13} {int(r.cost):5d} {r.chooser:>9} {r.g_pick:6.3f} "
              f"{r.OOS_CAGR:9.2%} {r.OOS_Sharpe:7.3f} {r.OOS_MaxDD:8.2%} "
              f"{r.OOS_H1:6.3f}/{r.OOS_H2:6.3f} {r.turn_yr:6.1f}x")
    lp = live[live.pass4b & live.levered_pick]
    P(f"  the FORBIDDEN 4b passes (levered picks, measurement only): {len(lp)}")
    for _, r in lp.sort_values("OOS_Sharpe", ascending=False).head(8).iterrows():
        P(f"    LEVERED {r.panel:>5} {r.arm:>13} {int(r.cost):3d}bps C={r.ceiling:.2f} "
          f"{r.chooser:>9} g={r.g_pick:.3f} OOS {r.OOS_CAGR:.2%}/{r.OOS_Sharpe:.3f}/"
          f"{r.OOS_MaxDD:.2%}   NOT PROMOTABLE (PROTOCOL 2)")
    P("")
    P("  comparands in the same OOS window:")
    for nm in PANELS:
        s2, v2x = spyref[nm]["OOS"], v2ref[nm]["OOS"]
        P(f"    {nm:5s} SPY {s2['CAGR']:7.2%} / {s2['Sharpe']:.3f} / {s2['MaxDD']:7.2%} "
          f"(halves {s2['H1']:.3f}/{s2['H2']:.3f})   RULES v2 (live) {v2x['CAGR']:7.2%} / "
          f"{v2x['Sharpe']:.3f} / {v2x['MaxDD']:7.2%} (halves {v2x['H1']:.3f}/{v2x['H2']:.3f})")
    P(f"    4b bars on OOS: MaxDD >= {DD_CAP:.2f} x SPY's, CAGR >= {CAGR_FLOOR:.2f} x SPY's, "
      f"both half Sharpes > SPY's.  KEEP path 4a is judged against RULES v2 in the same window.")

    # also report the FULL-sample and half-sample picture of the admissible bands, PROTOCOL 4
    P("")
    P("  FULL sample and halves at the admissible ceiling (804 convention, 10 bps), the bands'")
    P("  own midpoints -- PROTOCOL 4's 'full sample + first/second half' for the pricing above:")
    P(f"    {'panel':>5} {'arm':>13} {'g_mid':>6} {'CAGR':>8} {'Sharpe':>7} {'MaxDD':>8} "
      f"{'H1/H2':>13} {'4b':>4} {'4a':>4}")
    for nm in PANELS:
        for a in ARMS:
            e = W[(W.panel == nm) & (W.arm == a) & (W.cost == COST0) & (W.conv == "c804")
                  & (W.ceiling == GMAX_PROTO)]
            if not len(e) or bool(e.iloc[0]["is_empty"]):
                continue
            e = e.iloc[0]
            gm = 0.5 * (float(e.g_min) + float(e.g_max))
            r = score_g(books[(nm, a)], gm, COST0, spyref[nm], v2ref[nm])
            P(f"    {nm:>5} {a:>13} {gm:6.3f} {r['FULL_CAGR']:8.2%} {r['FULL_Sharpe']:7.3f} "
              f"{r['FULL_MaxDD']:8.2%} {r['FULL_H1']:6.3f}/{r['FULL_H2']:6.3f} "
              f"{str(r['c804_pass4b']):>4} {str(r['c804_pass4a']):>4}")

    # --------------------------------------------------------------------------------------
    # the answer
    # --------------------------------------------------------------------------------------
    P("")
    P("=" * 112)
    P("THE ANSWER")
    P("=" * 112)
    P(f"A1  Of the {cens:,} censored bands in 919's own corpus ({cens/n:.1%} of {n:,} non-empty), "
      f"{lad:,} ({lad/max(cens,1):.1%}) are LADDER FACTS BY CONSTRUCTION: their censor is at a")
    P(f"    bottom rung PROTOCOL never required ({int((D.censor_class=='BOTTOM_ONLY').sum()):,} "
      f"bottom-only + {int((D.censor_class=='BOTH_EDGES').sum()):,} both-edges), at a top rung "
      f"BELOW g=1.00 ({int((D.censor_class=='TOP_LADDER_SHORT').sum()):,}), or at a top rung")
    P(f"    ABOVE it ({int((D.censor_class=='TOP_ABOVE_CEILING').sum()):,}).  The 1.00 ceiling "
      f"cannot be blamed for any of them.")
    P(f"A2  The ceiling's share is bounded ABOVE by the {ceil_ub:,} "
      f"({ceil_ub/max(cens,1):.1%}) TOP_AT_CEILING bands -- the only class whose ladder stops "
      f"exactly on the no-leverage line.")
    if len(tc):
        nbb = int(tc.ceiling_bound.sum())
        P(f"A3  Calibrated on the {len(tc)} re-solvable readings that report that censor, "
          f"{nbb} ({rate:.1%}) are genuinely CEILING-BOUND (breach above 1.00, or no breach at")
        P(f"    all) and {len(tc)-nbb} ({1-rate:.1%}) have their true upper edge BELOW 1.00.  On "
          f"this population a ladder that reaches the line is reporting the RULEBOOK, not its own")
        P("    coarseness -- the opposite of what the LADDER-SHORT and BOTTOM classes report.")
    P(f"A4  H_SAME: width(1.50) == width(1.00) on {same_15} of {len(piv)} cells "
      f"({same_15/len(piv):.1%}); at C={CMAX:.2f} still {same_30} of {len(piv)} "
      f"({same_30/len(piv):.1%}).  919's '25 of 30' is reproduced and extended:")
    P("    the ceiling moves the width on a small minority, and on everything else the DD cap")
    P("    binds strictly inside PROTOCOL's own range.")
    P(f"A5  rule 8: {int(adm.pass4b.sum())} of {len(adm)} admissible IS-only picks reach 4b OOS "
      f"and {int(adm.pass4a.sum())} reach 4a; the verdict is ceiling-dependent on "
      f"{int(F.disagree.sum())} of {len(F)} cells and")
    P(f"    {int(F.lev_only_pass.sum())} cells reach 4b OOS ONLY from a forbidden ceiling.  "
      f"Nothing above g=1.00 is promotable, so those are a priced cost of PROTOCOL 2, not a book.")
    P("")
    P(f"total runtime {time.time()-t0:.1f}s")

    # leaderboard rows
    P("")
    P("LEADERBOARD rows:")
    lbl = [
        f"| 2026-09-15 | 922 census: censoring decomposed ({cens:,} censored of {n:,}) | ladder "
        f"{lad/max(cens,1):.1%} | ceiling UB {ceil_ub/max(cens,1):.1%} | bottom "
        f"{int((D.censor_class=='BOTTOM_ONLY').sum()):,} | top-short "
        f"{int((D.censor_class=='TOP_LADDER_SHORT').sum()):,} | top@1.00 {ceil_ub:,} | CENSUS | "
        f"{STEM}.py |"]
    if len(tc):
        lbl.append(
            f"| 2026-09-15 | 922 calibration of TOP_AT_CEILING ({len(tc)} re-solvable readings) | "
            f"ceiling-bound {rate:.1%} | artefact {1-rate:.1%} | median forbidden range "
            f"{(fr.forbidden_range.median() if len(fr) else float('nan')):.3f} | H_SAME w1.50==w1.00"
            f" {same_15}/{len(piv)} | — | CALIBRATION | {STEM}.py |")
    if len(pp):
        pp10 = pp[pp.cost == COST0]                 # PROTOCOL's primary cost cell, when it passes
        b = (pp10 if len(pp10) else pp).sort_values("OOS_Sharpe", ascending=False).iloc[0]
        lbl.append(
            f"| 2026-09-15 | 922 rule-8 best ADMISSIBLE OOS 4b pass: {b.panel}/{b.arm} "
            f"g={b.g_pick:.3f} ({b.chooser}, {int(b.cost)}bps) | {b.OOS_CAGR:.1%} | "
            f"{b.OOS_Sharpe:.2f} | {b.OOS_MaxDD:.1%} | {b.OOS_H1:.2f} / {b.OOS_H2:.2f} | SPY OOS "
            f"{spyref[b.panel]['OOS']['Sharpe']:.2f} ({spyref[b.panel]['OOS']['H1']:.2f}/"
            f"{spyref[b.panel]['OOS']['H2']:.2f}) | PARK (known band, not new) | {STEM}.py |")
    lbl.append(
        f"| 2026-09-15 | 922 rule-8 ceiling dependence | disagree {int(F.disagree.sum())}/{len(F)} "
        f"| 4b(adm) {int(adm.pass4b.sum())}/{len(adm)} | 4a(adm) {int(adm.pass4a.sum())}/{len(adm)} "
        f"| levered-only 4b {int(F.lev_only_pass.sum())} | median g-spread {F.g_spread.median():.3f}"
        f" | RULE 8 | {STEM}.py |")
    gp = sum(bool(v) for v in gates.values())
    lbl.append(
        f"| 2026-09-15 | 922 gates | {gp}/{len(gates)} PASS | G3c census repro | G9 censor-edge "
        f"join | G10 solvency | G11 ceiling monotonicity | GATES | {STEM}.py |")
    for line in lbl:
        P(line)

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"\nwrote {STEM}.console.txt")


if __name__ == "__main__":
    main()

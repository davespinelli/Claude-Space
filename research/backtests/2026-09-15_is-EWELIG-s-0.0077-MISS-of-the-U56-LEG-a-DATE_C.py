#!/usr/bin/env python3
"""Idea 925 (lane C, 2026-09-15) -- is EWELIG's 0.0077 MISS of the U56 IS-H1 SHARPE leg a DATE?

THE QUESTION (queue, 2026-09-15)
  Idea 922 priced the 2x2 {eligibility gate on/off} x {top-20/equal-weight} on U56's ISH1_HALF
  window and concluded CONCENTRATION is not the carrier of CAND20's leg failure, because the
  de-concentrated arm EWELIG still fails the leg at 0 of 30 gross rungs.  But at the published
  g = 0.75, 10 bps its margin is 0.8301 against SPY's 0.8378 -- a MISS OF 0.0077 OF SHARPE.
  Idea 806's standing clause says a margin smaller than the book's own rebalance-offset spread
  is a DATE, not a verdict.  Measure the spread and re-read the verdict.

WHAT A "DATE" MEANS HERE, EXACTLY
  Both the subject and the comparand are held at their own conventions, per idea 891/893:
    the BOOK is re-run on its own weekly cadence moved k trading days later (k = 0 IS the
    published calendar, i.e. `engine.rebalance_mask(idx, "W")`);
    SPY is BUY-AND-HOLD and has no rebalance calendar at all, so it is NOT offset.  The spread
    measured below is therefore a property of the book's calendar and of nothing else.
  MARGIN  = book statistic at k = 0 minus SPY's, in Sharpe points (signed; here it is negative --
            the leg is a MISS, which is the whole point: 806's clause was written for passes and
            this run applies it to a FAILURE, where it says the same thing).
  SPREAD  = max - min of the BOOK's own statistic across the offset grid.
  RATIO   = |margin| / spread.  RATIO < 1 => the published verdict is inside its own calendar
            noise => a DATE.  RATIO >= 1 => a verdict.
  A ratio below 1 does NOT by itself mean the leg would PASS on some calendar: the whole spread
  could sit below SPY.  So H_FLIP below tests the strictly stronger, capital-relevant form.

WHAT IS TUNED AND WHAT IS REPORTED (PROTOCOL 4: max 2 tuned parameters -- the queue names both)
  TUNED 1  OFFSET GRID, 3 levels, every point reported:
           SHIFT5  k = 0..4, the weekly mask shifted k trading days later (891/893's own axis;
                   k = 0 is the published calendar, gated at G2)
           PHASE5  the 5 phases of a 5-trading-day cycle, `arange(T) % 5 == k` (the axis idea 919
                   and the 2026-09-15 knife-edge run used; a DIFFERENT enumeration of "which day
                   of the week you trade", because it drifts through holidays)
           ALT3    k = 0, 2, 4 of SHIFT5 -- a coarser grid, to show whether the measured spread
                   is an artefact of grid resolution
  TUNED 2  PANEL, 3 levels: U56 (the subject's home panel) / B136 / SMALL.
  REPORTED AXES (nothing fitted on them; every point published):
           gross 0.05..1.50 step 0.05 (30 rungs); cost 0 / 10 / 25 / 50 bps;
           arms EWELIG (subject), CAND20, CAND20_NG, EWALL, BAND03, SPYBH;
           windows FULL / IS / OOS / ISH1_HALF (the leg itself) / ISH2_HALF.

PRE-REGISTERED BARS (fixed before any number below the gates was read; both directions reported)
  H_DATE   THE QUEUE'S QUESTION.  At U56 / ISH1_HALF / g = 0.75 / 10 bps, EWELIG's |margin|
           is SMALLER than its own offset spread.  PASS = the miss is a DATE.
  H_FLIP   the strictly stronger form: at that same cell the leg actually FLIPS -- EWELIG's
           ISH1_HALF Sharpe exceeds SPY's on at least 1 of the 5 SHIFT5 offsets.  Reported on
           every grid.  H_DATE without H_FLIP means "unresolved", not "passes".
  H_LADDER the date-ness is not a single-rung fact: at U56 / 10 bps, at least 15 of the 30 gross
           rungs have >= 1 offset clearing the leg (922's published count at k = 0 is 0 of 30).
  H_CAND20 922's OWN headline survives its own clause: CAND20's ISH1_HALF margin (-0.1078) is
           LARGER than CAND20's offset spread at the same cell, on all 3 grids (ratio >= 1).
  H_PANEL  the answer travels: H_DATE reads the same for EWELIG on B136 and on SMALL.
  H_COST   the spread is a calendar fact, not a cost artefact: EWELIG's ISH1_HALF spread at
           0 bps is within 2x of its spread at 10 bps.
  H_WF     (rule 8, REQUIRED) arm x gross chosen on 2009-2016 ALONE at each offset, 2017-2026
           read ONCE; both KEEP paths, against SPY and RULES v2 in the same window.  The 5-offset
           ENSEMBLE book (equal-weight average of the 5 SHIFT5 sleeves' net returns) is carried
           as a reported control: it is what a trader who refuses to pick a date actually owns.

GATES (all printed before any result number)
  G1  the fast runner == `engine.backtest` on net returns AND turnover (EWELIG, U56, g=0.75)
  G2  SHIFT5 k=0 mask == `engine.rebalance_mask(idx,"W")` elementwise; the 5 PHASE5 masks
      partition the index exactly (every day in exactly one phase)
  G3  CROSS-RUN: idea 922's committed `.factorial.csv` U56/ISH1_HALF row reproduces at k = 0 --
      CAND20 0.730026, EWELIG 0.830068, CAND20_NG 0.912347, EWALL 1.038372, SPY 0.837753
  G4  the committed U56 triples (SPY, RULES v2)
  G5  BAND03 == `baseline.rules_v2_weights` elementwise
  G6  determinism (rebuild the subject cell, compare)
  G7  FALSIFICATION of the spread machinery: SPYBH must show an offset spread of ~0; a non-zero
      spread there would mean the dial is measuring something other than the rebalance calendar.
      AS PRE-REGISTERED THIS GATE FAILS, and the bar is the thing that was wrong: at g < 1 SPYBH
      is a CONSTANT-MIX book (g in SPY, 1-g in cash) that rebalances back to target on its own
      calendar, so it trades weekly and a spread is correct.  The bar is left standing as written
      and G7b reads the same falsification at g = 1.00, which is the real never-trades cell.

PROTOCOL: 10 bps primary, t+1 execution, weekly cadence, warm-up 260 days, IS 2009-2016 /
OOS 2017-2026.  Nothing in RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py is modified.

SURVIVORSHIP: U56 / B136 / SMALL are current-constituent lists (SMALL additionally drops the
tickers with `max_1d_move` >= 1.0 per `data/small_meta.csv`), so every CAGR and drawdown LEVEL
here is optimistic -- the books' and the comparands' alike.  The reported object is a RATIO of a
margin to a spread computed on the SAME book and the SAME days, which is far less exposed; the
leg verdicts and the rule-8 triples are levels read against SPY, which is not survivorship-
inflated, so those are upper bounds.  Stated, not hidden.

Deterministic, standalone, no network.
Run: python research/backtests/2026-09-15_is-EWELIG-s-0.0077-MISS-of-the-U56-LEG-a-DATE_C.py
"""
from __future__ import annotations

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
FREQ = "W"
LAG = 1
BAND0 = 0.03
MAXVOL = 0.60
WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
PUBLISHED_G = 0.75
LEG = "ISH1_HALF"                 # the leg the question is about
LADDER_BAR = 15                   # H_LADDER: >= 15 of 30 gross rungs
COST_BAR = 2.0                    # H_COST: within 2x

GROSS30 = [round(0.05 * i, 4) for i in range(1, 31)]
COSTS = [0.0, 10.0, 25.0, 50.0]
PANELS = ["U56", "B136", "SMALL"]
ARMS = ["EWELIG", "CAND20", "CAND20_NG", "EWALL", "BAND03", "SPYBH"]
ARM_SRC = {
    "EWELIG": "THE SUBJECT: 922's de-concentrated arm (gate ON, equal-weight every eligible name)",
    "CAND20": "922's subject / the 2026-09-04 KEEP 4b book (gate ON, top-20 EW, no vol scaler)",
    "CAND20_NG": "gate OFF, top-20 EW on the same score",
    "EWALL": "gate OFF, equal-weight every priced name = the panel index",
    "BAND03": "RULES v2 live (baseline.rules_v2_weights)",
    "SPYBH": "g x SPY, the never-trades control (G7)",
}

# offset grids: the TUNED dial.  values are (kind, k) pairs; ("shift", 0) IS the published cal.
SHIFT_KS = [0, 1, 2, 3, 4]
PHASE_KS = [0, 1, 2, 3, 4]
SCHEDS = [("shift", k) for k in SHIFT_KS] + [("phase", k) for k in PHASE_KS]
OFFGRIDS = {
    "SHIFT5": [("shift", k) for k in SHIFT_KS],
    "PHASE5": [("phase", k) for k in PHASE_KS],
    "ALT3": [("shift", k) for k in (0, 2, 4)],
}
OFF_HEAD = "SHIFT5"
PUBLISHED_SCHED = ("shift", 0)

WINDOWS = ["FULL", "IS", "OOS", "ISH1_HALF", "ISH2_HALF"]

# committed comparands (ideas 670/675/922, U56 panel)
SPY_U56 = (0.1516, 0.8861, -0.3372)
V2_U56 = (0.0863, 1.2018, -0.1205)
TOL_C, TOL_S, TOL_D = 0.004, 0.030, 0.015
# idea 922's committed .factorial.csv U56 / ISH1_HALF row (g=0.75, 10 bps) -- G3
FAC922 = {"CAND20": 0.7300262445175577, "EWELIG": 0.83006824812557,
          "CAND20_NG": 0.912346919742853, "EWALL": 1.0383720520796034,
          "SPY": 0.8377534152899397}
G3_BAR = 5e-4
PARENT922 = OUT / "2026-09-15_why-is-the-IS-H1-SHARPE-leg-UNPASSABLE-for-CAND20-on-U56_cloud.factorial.csv"

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ================================================================================================
# calendars
# ================================================================================================
def sched_mask(idx, kind, k):
    """The book's rebalance calendar.

    shift : the published weekly mask (last trading day of each ISO week) moved k trading days
            later.  k = 0 IS the published calendar (gated at G2).
    phase : the k-th phase of a 5-trading-day cycle (a different enumeration of the same dial).
    """
    if kind == "shift":
        m = rebalance_mask(idx, FREQ)
        return m if k == 0 else m.shift(k, fill_value=False)
    if kind == "phase":
        return pd.Series(np.arange(len(idx)) % 5 == k, index=idx)
    raise KeyError(kind)


def sname(s):
    return f"{s[0]}{s[1]}"


# ================================================================================================
# runner (the record's vectorised equivalent of engine.backtest; gated at G1)
# ================================================================================================
class Panel:
    def __init__(self, name, px, sched):
        self.name, self.px, self.sched = name, px, sched
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        T, N = self.rets.shape
        self.T, self.N = T, N
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, N)), C[:-1]])
        mk = sched_mask(self.idx, *sched).shift(LAG, fill_value=False).values.copy()
        mk[0] = True
        self.reb = np.flatnonzero(mk)
        seg = np.searchsorted(self.reb, np.arange(T), side="right") - 1
        self.s0 = self.reb[seg]
        self.s0p = self.reb[np.maximum(seg - 1, 0)]
        self.R = self.Cp / self.Cp[self.s0]
        self.Rp = self.Cp[self.reb] / self.Cp[self.s0p[self.reb]]
        self.start = self.idx[WARMUP]
        m_full = np.asarray(self.idx >= self.start)
        w = {"FULL": m_full,
             "IS": m_full & np.asarray(self.idx <= pd.Timestamp(IS_END)),
             "OOS": np.asarray(self.idx >= pd.Timestamp(OOS_START))}
        # the leg window: the trading-day halves of the IS window (922's own definition).  The
        # split is a COUNT split on a mask that does not move with the offset, so k cannot move it.
        ispos = np.flatnonzero(w["IS"])
        h = len(ispos) // 2
        ish1 = np.zeros(T, bool); ish1[ispos[:h]] = True
        ish2 = np.zeros(T, bool); ish2[ispos[h:]] = True
        w["ISH1_HALF"], w["ISH2_HALF"] = ish1, ish2
        self.masks = w
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


def legswin(s, spy):
    """The window-local 4b form used by the record's rule-8 runs (867/910/918/922)."""
    return dict(L1_H1=bool(s["H1"] > spy["H1"]), L2_H2=bool(s["H2"] > spy["H2"]), L3_OOS=True,
                L4_DDcap=bool(s["MaxDD"] >= DD_CAP * spy["MaxDD"]),
                L5_CAGRfloor=bool(s["CAGR"] >= CAGR_FLOOR * spy["CAGR"]))


def pass4b(s, spy):
    return all(legswin(s, spy).values())


def pass4a(s, base):
    return bool(s["H1"] > base["H1"] and s["H2"] > base["H2"] and s["MaxDD"] >= base["MaxDD"])


# ================================================================================================
# the arms (verbatim from idea 922; NOT re-specified here)
# ================================================================================================
def ew_gross1(px):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def ranked_w1(sc, n):
    rank = sc.rank(axis=1, ascending=False)
    sel = (rank <= n).astype(float)
    k = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(k, axis=0).fillna(0.0)


def arm_w1(px, pre, arm):
    sc_n, above, vol20 = pre
    if arm == "BAND03":
        return ew_gross1(px).where(band_state(px, BAND0) & px.notna(), 0.0).values
    if arm == "CAND20":
        return ranked_w1(sc_n.where(above & (vol20 < MAXVOL)), 20).values
    if arm == "EWELIG":
        sel = (above & (vol20 < MAXVOL) & px.notna()).astype(float)
        k = sel.sum(axis=1).replace(0, np.nan)
        return sel.div(k, axis=0).fillna(0.0).values
    if arm == "CAND20_NG":
        return ranked_w1(sc_n.where(px.notna()), 20).values
    if arm == "EWALL":
        return ew_gross1(px).values
    if arm == "SPYBH":
        w = pd.DataFrame(0.0, index=px.index, columns=px.columns)
        w["SPY"] = 1.0
        return w.where(px.notna(), 0.0).values
    raise KeyError(arm)


def prep(px):
    sc_n, above, vol20 = score(px, vol_scale=False)
    return sc_n, above, vol20


# ================================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 925 (lane C, 2026-09-15) -- is EWELIG's 0.0077 MISS of the U56 IS-H1 leg a DATE?")
    P("=" * 100)
    P("CLAUSE (idea 806, as applied here): RATIO = |margin at the published calendar| / (max-min")
    P("  of the BOOK's own statistic across the offset grid).  RATIO < 1 => a DATE.  SPY is")
    P("  buy-and-hold and is NOT offset -- it has no rebalance calendar.")
    P(f"2 TUNED DIALS: OFFSET GRID {list(OFFGRIDS)} x PANEL {PANELS}.  All 9 points reported.")
    P(f"REPORTED: gross {GROSS30[0]}..{GROSS30[-1]} x{len(GROSS30)} | cost {COSTS} bps | "
      f"arms {ARMS} | windows {WINDOWS}")
    P("")

    # ---------------- panels ----------------
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    raw, pre = {}, {}
    for nm, kw in [("U56", {}), ("B136", dict(broad=True)), ("SMALL", dict(small=True))]:
        px = load_universe(**kw)
        if nm == "SMALL":
            px = px[[c for c in px.columns if c not in bad]]
        raw[nm] = px
        pre[nm] = prep(px)
        P(f"panel {nm:6s} {px.shape[0]} days x {px.shape[1]} cols  {px.index[0].date()} .. "
          f"{px.index[-1].date()}")
    P(f"  SMALL drops {len(bad)} tickers with max_1d_move >= 1.0 (data/small_meta.csv)")
    P("")

    # ================================ GATES ================================
    P("=" * 100)
    P("GATES (printed before any result number)")
    P("=" * 100)
    gates = []

    # G1 fast runner == engine.backtest
    pxU = raw["U56"]
    W1 = arm_w1(pxU, pre["U56"], "EWELIG")
    panW = Panel("U56", pxU, PUBLISHED_SCHED)
    bkW = Book(panW, W1)
    r_fast, t_fast = bkW.at(PUBLISHED_G, COST0)
    eng = backtest(pxU, pd.DataFrame(W1 * PUBLISHED_G, index=pxU.index, columns=pxU.columns),
                   cost_bps=COST0, freq=FREQ)
    # engine.backtest emits NaN on the pre-warm-up rows where its own shift(1) has no weights;
    # every number in this run is read on the post-warm-up FULL window, so the gate is read there
    # (the same convention idea 922's G1 used).
    mfull = panW.masks["FULL"]
    d_r = float(np.abs(r_fast[mfull] - eng["returns"].values[mfull]).max())
    d_t = float(np.abs(t_fast[mfull] - eng["turnover"].values[mfull]).max())
    g1 = bool(d_r < 1e-10 and d_t < 1e-10)
    P(f"G1 runner  fast == engine.backtest (EWELIG, U56, g={PUBLISHED_G}, {COST0:.0f} bps): "
      f"max|dret| {d_r:.2e}  max|dturn| {d_t:.2e}  -> {'PASS' if g1 else 'FAIL'}")
    gates.append(dict(gate="G1_runner", detail=f"dret {d_r:.3e} dturn {d_t:.3e}", passed=g1))

    # G2 calendars
    ok_shift0 = bool(sched_mask(pxU.index, "shift", 0).equals(rebalance_mask(pxU.index, FREQ)))
    ph = np.vstack([sched_mask(pxU.index, "phase", k).values for k in PHASE_KS])
    ok_part = bool((ph.sum(axis=0) == 1).all())
    cnts = {f"shift{k}": int(sched_mask(pxU.index, "shift", k).sum()) for k in SHIFT_KS}
    cnts.update({f"phase{k}": int(sched_mask(pxU.index, "phase", k).sum()) for k in PHASE_KS})
    g2 = ok_shift0 and ok_part
    P(f"G2 mask    shift k=0 == engine.rebalance_mask: {ok_shift0} | phase masks partition the "
      f"index: {ok_part} -> {'PASS' if g2 else 'FAIL'}")
    P(f"           rebalance-day counts {cnts}")
    gates.append(dict(gate="G2_mask", detail=str(cnts), passed=g2))

    # G5 BAND03 == baseline
    b03 = pd.DataFrame(arm_w1(pxU, pre["U56"], "BAND03"), index=pxU.index, columns=pxU.columns)
    d_b = float((b03 * 0.75 - rules_v2_weights(pxU, BAND0, 0.75)).abs().max().max())
    g5 = bool(d_b < 1e-12)
    P(f"G5 band03  == baseline.rules_v2_weights elementwise: max|d| {d_b:.2e} -> "
      f"{'PASS' if g5 else 'FAIL'}")
    gates.append(dict(gate="G5_band03", detail=f"{d_b:.3e}", passed=g5))

    # G4 committed U56 triples
    spyU = pack(panW.spy[panW.masks["FULL"]])
    v2bk = Book(panW, arm_w1(pxU, pre["U56"], "BAND03"))
    rv2, _ = v2bk.at(0.75, COST0)
    v2U = pack(rv2[panW.masks["FULL"]])
    g4s = (abs(spyU["CAGR"] - SPY_U56[0]) < TOL_C and abs(spyU["Sharpe"] - SPY_U56[1]) < TOL_S
           and abs(spyU["MaxDD"] - SPY_U56[2]) < TOL_D)
    g4v = (abs(v2U["CAGR"] - V2_U56[0]) < TOL_C and abs(v2U["Sharpe"] - V2_U56[1]) < TOL_S
           and abs(v2U["MaxDD"] - V2_U56[2]) < TOL_D)
    g4 = bool(g4s and g4v)
    P(f"G4 triples SPY  mine ({spyU['CAGR']:.4f},{spyU['Sharpe']:.4f},{spyU['MaxDD']:.4f}) vs "
      f"committed {SPY_U56} -> {'PASS' if g4s else 'FAIL'}")
    P(f"           v2   mine ({v2U['CAGR']:.4f},{v2U['Sharpe']:.4f},{v2U['MaxDD']:.4f}) vs "
      f"committed {V2_U56} -> {'PASS' if g4v else 'FAIL'}")
    gates.append(dict(gate="G4_triples", detail=f"spy {g4s} v2 {g4v}", passed=g4))

    # G3 cross-run reproduction of 922's factorial row (at the published calendar)
    rep = {}
    for a in ["CAND20", "EWELIG", "CAND20_NG", "EWALL"]:
        bk = Book(panW, arm_w1(pxU, pre["U56"], a))
        r, _ = bk.at(PUBLISHED_G, COST0)
        rep[a] = fsharpe(r[panW.masks[LEG]])
    rep["SPY"] = fsharpe(panW.spy[panW.masks[LEG]])
    worst = max(abs(rep[k] - FAC922[k]) for k in FAC922)
    g3 = bool(worst < G3_BAR)
    P(f"G3 cross   idea 922 .factorial.csv U56/{LEG} (g={PUBLISHED_G}, {COST0:.0f} bps), worst "
      f"|d| {worst:.2e} (bar {G3_BAR:g}) -> {'PASS' if g3 else 'FAIL'}")
    for k in ["CAND20", "EWELIG", "CAND20_NG", "EWALL", "SPY"]:
        P(f"           {k:<10} mine {rep[k]:.6f}  committed {FAC922[k]:.6f}  "
          f"d {rep[k]-FAC922[k]:+.2e}")
    if PARENT922.exists():
        pf = pd.read_csv(PARENT922)
        row = pf[(pf.panel == "U56") & (pf.subwin == LEG)]
        P(f"           parent file present, {len(row)} matching row(s) read directly from disk")
    gates.append(dict(gate="G3_crossrun922", detail=f"worst {worst:.3e}", passed=g3))

    # G6 determinism
    bk2 = Book(Panel("U56", pxU, PUBLISHED_SCHED), arm_w1(pxU, pre["U56"], "EWELIG"))
    r2, _ = bk2.at(PUBLISHED_G, COST0)
    g6 = bool(np.abs(r2 - r_fast).max() == 0.0)
    P(f"G6 determ  subject cell rebuilt bit-identical: {'PASS' if g6 else 'FAIL'}")
    gates.append(dict(gate="G6_determinism", detail="exact", passed=g6))

    # ================================ THE OFFSET WALK ================================
    P("")
    P("=" * 100)
    P("THE OFFSET WALK -- every (panel x schedule x arm x gross x cost x window) cell")
    P("=" * 100)
    rows = []
    for nm in PANELS:
        px = raw[nm]
        W1s = {a: arm_w1(px, pre[nm], a) for a in ARMS}
        for sc in SCHEDS:
            pan = Panel(nm, px, sc)
            spyw = {w: pack(pan.spy[pan.masks[w]]) for w in WINDOWS}
            for a in ARMS:
                bk = Book(pan, W1s[a])
                for g in GROSS30:
                    for c in COSTS:
                        r, turn = bk.at(g, c)
                        rec = dict(panel=nm, sched_kind=sc[0], sched_k=sc[1], sched=sname(sc),
                                   arm=a, gross=g, cost=c,
                                   turnover_yr=float(turn[pan.masks["FULL"]].sum()
                                                     / (pan.masks["FULL"].sum() / 252.0)))
                        for w in WINDOWS:
                            s = pack(r[pan.masks[w]])
                            for k, v in s.items():
                                rec[f"{w}_{k}"] = v
                            rec[f"{w}_leg"] = bool(s["Sharpe"] > spyw[w]["Sharpe"])
                            rec[f"{w}_margin"] = s["Sharpe"] - spyw[w]["Sharpe"]
                            rec[f"{w}_4b"] = pass4b(s, spyw[w])
                        rows.append(rec)
            del pan
        P(f"  panel {nm:6s} done  ({len(rows):,} rows cumulative, {time.time()-t0:.0f}s)")
    lad = pd.DataFrame(rows)
    dump(lad, "ladder.csv")

    # SPY reference (offset-invariant by construction) for every panel/window
    spyref = {}
    for nm in PANELS:
        pan = Panel(nm, raw[nm], PUBLISHED_SCHED)
        spyref[nm] = {w: pack(pan.spy[pan.masks[w]]) for w in WINDOWS}
        del pan

    # G7 falsification: SPYBH's spread must be ~0
    sp = lad[(lad.arm == "SPYBH") & (lad.cost == COST0) & np.isclose(lad.gross, PUBLISHED_G)
             & lad.sched.isin([sname(s) for s in OFFGRIDS[OFF_HEAD]])]
    g7spr = {nm: float(sp[sp.panel == nm][f"{LEG}_Sharpe"].max()
                       - sp[sp.panel == nm][f"{LEG}_Sharpe"].min()) for nm in PANELS}
    g7 = bool(max(g7spr.values()) < 1e-9)
    P(f"G7 falsify SPYBH (never trades after day 1) offset spread on {LEG}: "
      + "  ".join(f"{k} {v:.2e}" for k, v in g7spr.items())
      + f" -> {'PASS' if g7 else 'FAIL'}")
    gates.append(dict(gate="G7_spybh_zero_spread", detail=str(g7spr), passed=g7))
    if not g7:
        P("   G7 FAILS AS PRE-REGISTERED, and the bar was mis-specified, not the machinery: at")
        P("   g < 1 the SPYBH arm is a CONSTANT-MIX book (0.75 SPY / 0.25 cash) that rebalances")
        P("   back to target on its own calendar, so it DOES trade weekly and a calendar spread is")
        P("   correct.  Only g = 1.00 is the never-trades cell.  G7b reads it there; the failed")
        P("   bar is left standing as written.")
    sp1 = lad[(lad.arm == "SPYBH") & (lad.cost == COST0) & np.isclose(lad.gross, 1.0)
              & lad.sched.isin([sname(s) for s in OFFGRIDS[OFF_HEAD]])]
    g7bspr = {nm: float(sp1[sp1.panel == nm][f"{LEG}_Sharpe"].max()
                        - sp1[sp1.panel == nm][f"{LEG}_Sharpe"].min()) for nm in PANELS}
    g7b = bool(max(g7bspr.values()) < 1e-9)
    P(f"G7b falsify SPYBH at g=1.00 (the true never-trades cell) spread on {LEG}: "
      + "  ".join(f"{k} {v:.2e}" for k, v in g7bspr.items())
      + f" -> {'PASS' if g7b else 'FAIL'}")
    gates.append(dict(gate="G7b_spybh_g1_zero_spread", detail=str(g7bspr), passed=g7b))
    gdf = pd.DataFrame(gates)
    dump(gdf, "gates.csv")
    P(f"GATES: {int(gdf.passed.sum())} of {len(gdf)} PASS")

    # ================================ THE CLAUSE ================================
    P("")
    P("=" * 100)
    P("THE CLAUSE -- margin at the published calendar vs the book's own offset spread")
    P("=" * 100)
    clause = []
    for nm in PANELS:
        for a in ARMS:
            for g in GROSS30:
                for c in COSTS:
                    for w in WINDOWS:
                        base = lad[(lad.panel == nm) & (lad.arm == a) & np.isclose(lad.gross, g)
                                   & (lad.cost == c)]
                        pub = base[base.sched == sname(PUBLISHED_SCHED)]
                        if pub.empty:
                            continue
                        mg = float(pub[f"{w}_margin"].iloc[0])
                        for gname, ks in OFFGRIDS.items():
                            sub = base[base.sched.isin([sname(s) for s in ks])]
                            vals = sub[f"{w}_Sharpe"].values
                            spread = float(np.nanmax(vals) - np.nanmin(vals))
                            legs = sub[f"{w}_leg"].values
                            clause.append(dict(
                                panel=nm, arm=a, gross=g, cost=c, window=w, offgrid=gname,
                                n_off=len(ks), margin=mg, spread=spread,
                                ratio=(abs(mg) / spread if spread > 0 else np.inf),
                                is_date=bool(spread > 0 and abs(mg) < spread),
                                leg_pub=bool(pub[f"{w}_leg"].iloc[0]),
                                n_leg_pass=int(np.sum(legs)), n_leg_fail=int(np.sum(~legs)),
                                flips=bool(0 < int(np.sum(legs)) < len(legs)),
                                sharpe_lo=float(np.nanmin(vals)), sharpe_hi=float(np.nanmax(vals)),
                                spy_sharpe=float(spyref[nm][w]["Sharpe"])))
    CL = pd.DataFrame(clause)
    dump(CL, "clause.csv")

    def cell(nm, a, w=LEG, g=PUBLISHED_G, c=COST0, grid=OFF_HEAD):
        r = CL[(CL.panel == nm) & (CL.arm == a) & (CL.window == w) & np.isclose(CL.gross, g)
               & (CL.cost == c) & (CL.offgrid == grid)]
        return r.iloc[0]

    # ---- H_DATE ----
    P("")
    P("-" * 100)
    P(f"H_DATE   EWELIG, U56, {LEG}, g={PUBLISHED_G}, {COST0:.0f} bps -- is the miss a DATE?")
    P("-" * 100)
    P(f"{'offgrid':<8} {'margin':>9} {'spread':>9} {'ratio':>8} {'sharpe range':>22} "
      f"{'SPY':>8} {'verdict':>9}")
    h_date = {}
    for gname in OFFGRIDS:
        r = cell("U56", "EWELIG", grid=gname)
        h_date[gname] = bool(r.is_date)
        P(f"{gname:<8} {r.margin:>+9.4f} {r.spread:>9.4f} {r.ratio:>8.3f} "
          f"[{r.sharpe_lo:.4f}, {r.sharpe_hi:.4f}] {r.spy_sharpe:>8.4f} "
          f"{'DATE' if r.is_date else 'VERDICT':>9}")
    H_DATE = h_date[OFF_HEAD]
    _v = ("PASS -- the 0.0077 miss is INSIDE the book's own calendar spread" if H_DATE
          else "FAIL -- the miss is larger than the calendar spread, so it is a VERDICT")
    P(f"H_DATE ({OFF_HEAD}, headline): {_v}")
    P(f"  all 3 grids agree: {len(set(h_date.values())) == 1}   {h_date}")

    # ---- H_FLIP ----
    P("")
    P("-" * 100)
    P("H_FLIP   the stronger form: does the LEG ITSELF flip on any offset? (>= 1 of 5 on SHIFT5)")
    P("-" * 100)
    P(f"{'offgrid':<8} {'n_pass':>7} {'n_off':>6} {'flips':>7}   per-offset Sharpe (leg bar "
      f"{spyref['U56'][LEG]['Sharpe']:.4f})")
    h_flip = {}
    for gname in OFFGRIDS:
        r = cell("U56", "EWELIG", grid=gname)
        h_flip[gname] = int(r.n_leg_pass)
        det = lad[(lad.panel == "U56") & (lad.arm == "EWELIG") & (lad.cost == COST0)
                  & np.isclose(lad.gross, PUBLISHED_G)
                  & lad.sched.isin([sname(s) for s in OFFGRIDS[gname]])]
        s = "  ".join(f"{a}:{b:.4f}{'*' if c else ''}"
                      for a, b, c in zip(det.sched, det[f"{LEG}_Sharpe"], det[f"{LEG}_leg"]))
        P(f"{gname:<8} {int(r.n_leg_pass):>7} {int(r.n_off):>6} {str(bool(r.flips)):>7}   {s}")
    H_FLIP = h_flip[OFF_HEAD] >= 1
    P(f"H_FLIP ({OFF_HEAD}): {'PASS' if H_FLIP else 'FAIL'} -- {h_flip[OFF_HEAD]} of "
      f"{len(OFFGRIDS[OFF_HEAD])} offsets clear the leg   (* = clears)")

    # ---- H_LADDER ----
    P("")
    P("-" * 100)
    P(f"H_LADDER not a single-rung fact: of 30 gross rungs (U56, {COST0:.0f} bps), how many have "
      f">= 1 offset clearing the leg?  (bar {LADDER_BAR})")
    P("-" * 100)
    lrow = []
    for gname in OFFGRIDS:
        for a in ARMS:
            sub = CL[(CL.panel == "U56") & (CL.arm == a) & (CL.window == LEG)
                     & (CL.cost == COST0) & (CL.offgrid == gname)]
            n_any = int((sub.n_leg_pass > 0).sum())
            n_all = int((sub.n_leg_fail == 0).sum())
            n_pub = int(sub.leg_pub.sum())
            n_date = int(sub.is_date.sum())
            lrow.append(dict(offgrid=gname, arm=a, n_rungs=len(sub), n_pub_pass=n_pub,
                             n_any_offset_pass=n_any, n_all_offset_pass=n_all, n_date=n_date))
    LD = pd.DataFrame(lrow)
    dump(LD, "ladder_counts.csv")
    P(f"{'offgrid':<8} {'arm':<11} {'pub':>5} {'any-off':>8} {'all-off':>8} {'is_date':>8}")
    for _, r in LD.iterrows():
        P(f"{r.offgrid:<8} {r.arm:<11} {r.n_pub_pass:>5} {r.n_any_offset_pass:>8} "
          f"{r.n_all_offset_pass:>8} {r.n_date:>8}")
    # 922's own H_CONC bar ("EWELIG clears the leg at >= 15 of 30 rungs") re-read CALENDAR BY
    # CALENDAR -- the published k = 0 reading is the one 922 committed.
    P("")
    P(f"  922's H_CONC bar re-read per calendar (U56, {COST0:.0f} bps): rungs of 30 clearing the "
      f"leg, bar 15")
    P(f"  {'sched':<10} {'EWELIG':>8} {'CAND20':>8} {'CAND20_NG':>10} {'EWALL':>8} "
      f"{'H_CONC would read':>20}")
    conc = []
    for sc in SCHEDS:
        sn = sname(sc)
        c = {}
        for a in ["EWELIG", "CAND20", "CAND20_NG", "EWALL"]:
            sub = lad[(lad.panel == "U56") & (lad.arm == a) & (lad.cost == COST0)
                      & (lad.sched == sn)]
            c[a] = int(sub[f"{LEG}_leg"].sum())
        hc = bool(c["CAND20"] == 0 and c["EWELIG"] >= LADDER_BAR)
        conc.append(dict(sched=sn, **c, H_CONC=hc))
        P(f"  {sn:<10} {c['EWELIG']:>8} {c['CAND20']:>8} {c['CAND20_NG']:>10} {c['EWALL']:>8} "
          f"{('PASS -- CONCENTRATION IS THE CARRIER' if hc else 'FAIL (922 published this)'):>20}")
    CC = pd.DataFrame(conc)
    dump(CC, "hconc_by_calendar.csv")
    P(f"  922's H_CONC verdict flips on {int(CC.H_CONC.sum())} of {len(CC)} calendars "
      f"({int(CC[CC.sched.str.startswith('shift')].H_CONC.sum())} of 5 SHIFT5, "
      f"{int(CC[CC.sched.str.startswith('phase')].H_CONC.sum())} of 5 PHASE5)")
    n_any_ew = int(LD[(LD.offgrid == OFF_HEAD) & (LD.arm == "EWELIG")].n_any_offset_pass.iloc[0])
    H_LADDER = n_any_ew >= LADDER_BAR
    P(f"H_LADDER: {'PASS' if H_LADDER else 'FAIL'} -- EWELIG {n_any_ew} of 30 rungs have an "
      f"offset that clears (922 published 0 of 30 at the published calendar)")

    # ---- H_CAND20 ----
    P("")
    P("-" * 100)
    P("H_CAND20 does 922's OWN headline survive its own clause?  (CAND20 ratio >= 1 on all grids)")
    P("-" * 100)
    h_c20 = {}
    for gname in OFFGRIDS:
        r = cell("U56", "CAND20", grid=gname)
        h_c20[gname] = float(r.ratio)
        P(f"{gname:<8} margin {r.margin:>+8.4f}  spread {r.spread:.4f}  ratio {r.ratio:>6.3f}  "
          f"n_leg_pass {int(r.n_leg_pass)} of {int(r.n_off)}  -> "
          f"{'DATE' if r.is_date else 'VERDICT'}")
    H_CAND20 = all(v >= 1.0 for v in h_c20.values())
    P(f"H_CAND20: {'PASS -- CAND20 fails the leg on every calendar' if H_CAND20 else 'FAIL'}")

    # ---- H_PANEL ----
    P("")
    P("-" * 100)
    P("H_PANEL  does the answer travel?  EWELIG on every panel x every grid")
    P("-" * 100)
    P(f"{'panel':<7} {'offgrid':<8} {'margin':>9} {'spread':>9} {'ratio':>8} {'n_pass':>7} "
      f"{'verdict':>9}")
    h_panel = {}
    for nm in PANELS:
        for gname in OFFGRIDS:
            r = cell(nm, "EWELIG", grid=gname)
            if gname == OFF_HEAD:
                h_panel[nm] = bool(r.is_date)
            P(f"{nm:<7} {gname:<8} {r.margin:>+9.4f} {r.spread:>9.4f} {r.ratio:>8.3f} "
              f"{int(r.n_leg_pass):>7} {'DATE' if r.is_date else 'VERDICT':>9}")
    H_PANEL = len(set(h_panel.values())) == 1
    P(f"H_PANEL: {'PASS -- same reading on all 3 panels' if H_PANEL else 'FAIL -- panel-dependent'}"
      f"   {h_panel}")

    # ---- H_COST ----
    P("")
    P("-" * 100)
    P(f"H_COST   is the spread a CALENDAR fact or a COST artefact?  (0 bps within {COST_BAR}x of "
      f"{COST0:.0f} bps)")
    P("-" * 100)
    P(f"{'panel':<7} {'arm':<11} {'cost':>6} {'spread':>9} {'margin':>9} {'ratio':>8}")
    for nm in PANELS:
        for a in ["EWELIG", "CAND20"]:
            for c in COSTS:
                r = CL[(CL.panel == nm) & (CL.arm == a) & (CL.window == LEG)
                       & np.isclose(CL.gross, PUBLISHED_G) & (CL.cost == c)
                       & (CL.offgrid == OFF_HEAD)].iloc[0]
                P(f"{nm:<7} {a:<11} {c:>6.0f} {r.spread:>9.4f} {r.margin:>+9.4f} {r.ratio:>8.3f}")
    s0 = float(CL[(CL.panel == "U56") & (CL.arm == "EWELIG") & (CL.window == LEG)
                  & np.isclose(CL.gross, PUBLISHED_G) & (CL.cost == 0.0)
                  & (CL.offgrid == OFF_HEAD)].spread.iloc[0])
    s10 = float(cell("U56", "EWELIG").spread)
    H_COST = bool(max(s0, s10) / max(min(s0, s10), 1e-12) <= COST_BAR)
    P(f"H_COST: {'PASS' if H_COST else 'FAIL'} -- 0 bps spread {s0:.4f} vs 10 bps {s10:.4f} "
      f"(ratio {max(s0,s10)/max(min(s0,s10),1e-12):.2f}x, bar {COST_BAR}x)")

    # ================================ RULE 8 (walk-forward) ================================
    P("")
    P("=" * 100)
    P("H_WF -- RULE 8: parameters chosen on IS 2009-2016 ONLY, OOS 2017-2026 read ONCE")
    P("=" * 100)
    P("Choosers (all IS-only, no OOS number touched): BEST_IS_SHARPE (arm x gross at each offset),")
    P("BEST_IS_4b (first arm x gross clearing window-local 4b in IS), and the PUBLISHED book")
    P("(EWELIG at g=0.75) carried unchosen.  Each is read OOS on its own offset AND as the")
    P("5-sleeve ENSEMBLE (equal-weight average of the SHIFT5 sleeves' net returns).")
    wf = []
    keep = []          # the RE-READ: full 4b leg tables for the two subject books, per calendar
    for nm in PANELS:
        px = raw[nm]
        W1s = {a: arm_w1(px, pre[nm], a) for a in ARMS if a != "SPYBH"}
        pans = {sname(s): Panel(nm, px, s) for s in OFFGRIDS[OFF_HEAD]}
        # net-return series for every (sched, arm, gross) at 10 bps
        series = {}
        for sn, pan in pans.items():
            for a, W in W1s.items():
                bk = Book(pan, W)
                for g in GROSS30:
                    r, _ = bk.at(g, COST0)
                    series[(sn, a, g)] = r
        pan0 = pans[sname(PUBLISHED_SCHED)]
        m_is, m_oos = pan0.masks["IS"], pan0.masks["OOS"]
        spy_is, spy_oos = pack(pan0.spy[m_is]), pack(pan0.spy[m_oos])
        v2_is = pack(series[(sname(PUBLISHED_SCHED), "BAND03", 0.75)][m_is])
        v2_oos = pack(series[(sname(PUBLISHED_SCHED), "BAND03", 0.75)][m_oos])
        for sn in pans:
            cand = [(a, g) for a in W1s for g in GROSS30]
            is_st = {(a, g): pack(series[(sn, a, g)][m_is]) for a, g in cand}
            picks = {}
            picks["BEST_IS_SHARPE"] = max(cand, key=lambda k: (is_st[k]["Sharpe"]
                                                               if np.isfinite(is_st[k]["Sharpe"])
                                                               else -9e9))
            p4b = [k for k in cand if pass4b(is_st[k], spy_is)]
            picks["BEST_IS_4b"] = (max(p4b, key=lambda k: is_st[k]["Sharpe"]) if p4b else None)
            picks["PUBLISHED_EWELIG"] = ("EWELIG", PUBLISHED_G)
            for chooser, pk in picks.items():
                if pk is None:
                    wf.append(dict(panel=nm, sched=sn, chooser=chooser, arm=None, gross=np.nan,
                                   is_empty=True))
                    continue
                a, g = pk
                o = pack(series[(sn, a, g)][m_oos])
                lg = legswin(o, spy_oos)
                wf.append(dict(panel=nm, sched=sn, chooser=chooser, arm=a, gross=g, is_empty=False,
                               IS_Sharpe=is_st[pk]["Sharpe"], OOS_CAGR=o["CAGR"],
                               OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"], OOS_H1=o["H1"],
                               OOS_H2=o["H2"], **{f"OOS_{k}": v for k, v in lg.items()},
                               OOS_4b=all(lg.values()), OOS_4a=pass4a(o, v2_oos),
                               spy_CAGR=spy_oos["CAGR"], spy_Sharpe=spy_oos["Sharpe"],
                               spy_MaxDD=spy_oos["MaxDD"], v2_Sharpe=v2_oos["Sharpe"],
                               v2_MaxDD=v2_oos["MaxDD"], ensemble=False))
        # the ENSEMBLE control: average the 5 sleeves of each (arm, gross), then choose IS-only
        ens = {}
        for a in W1s:
            for g in GROSS30:
                ens[(a, g)] = np.mean([series[(sname(s), a, g)] for s in OFFGRIDS[OFF_HEAD]],
                                      axis=0)
        is_e = {k: pack(v[m_is]) for k, v in ens.items()}
        cand = list(ens)
        picks = {"BEST_IS_SHARPE": max(cand, key=lambda k: (is_e[k]["Sharpe"]
                                                            if np.isfinite(is_e[k]["Sharpe"])
                                                            else -9e9))}
        p4b = [k for k in cand if pass4b(is_e[k], spy_is)]
        picks["BEST_IS_4b"] = (max(p4b, key=lambda k: is_e[k]["Sharpe"]) if p4b else None)
        picks["PUBLISHED_EWELIG"] = ("EWELIG", PUBLISHED_G)
        for chooser, pk in picks.items():
            if pk is None:
                wf.append(dict(panel=nm, sched="ENSEMBLE5", chooser=chooser, arm=None,
                               gross=np.nan, is_empty=True, ensemble=True))
                continue
            a, g = pk
            o = pack(ens[pk][m_oos])
            lg = legswin(o, spy_oos)
            wf.append(dict(panel=nm, sched="ENSEMBLE5", chooser=chooser, arm=a, gross=g,
                           is_empty=False, IS_Sharpe=is_e[pk]["Sharpe"], OOS_CAGR=o["CAGR"],
                           OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"], OOS_H1=o["H1"],
                           OOS_H2=o["H2"], **{f"OOS_{k}": v for k, v in lg.items()},
                           OOS_4b=all(lg.values()), OOS_4a=pass4a(o, v2_oos),
                           spy_CAGR=spy_oos["CAGR"], spy_Sharpe=spy_oos["Sharpe"],
                           spy_MaxDD=spy_oos["MaxDD"], v2_Sharpe=v2_oos["Sharpe"],
                           v2_MaxDD=v2_oos["MaxDD"], ensemble=True))
        P(f"  panel {nm:6s} walk-forward done  ({time.time()-t0:.0f}s)   "
          f"OOS SPY {spy_oos['CAGR']:.2%}/{spy_oos['Sharpe']:.3f}/{spy_oos['MaxDD']:.2%}  "
          f"RULES v2 {v2_oos['CAGR']:.2%}/{v2_oos['Sharpe']:.3f}/{v2_oos['MaxDD']:.2%}")

        # ---- the RE-READ: every 4b leg with its own MARGIN, for the two subject books, on each
        # ---- SHIFT5 calendar and on the 5-sleeve ENSEMBLE (which has no calendar to pick).
        m_full = pan0.masks["FULL"]
        spy_full = pack(pan0.spy[m_full])
        v2_full = pack(series[(sname(PUBLISHED_SCHED), "BAND03", 0.75)][m_full])
        SPYW = {"FULL": spy_full, "IS": spy_is, "OOS": spy_oos}
        V2W = {"FULL": v2_full, "IS": v2_is, "OOS": v2_oos}
        MSK = {"FULL": m_full, "IS": m_is, "OOS": m_oos}
        for a in ["EWELIG", "CAND20"]:
            srcs = {sname(s): series[(sname(s), a, PUBLISHED_G)] for s in OFFGRIDS[OFF_HEAD]}
            srcs["ENSEMBLE5"] = ens[(a, PUBLISHED_G)]
            for sn, r in srcs.items():
                for w in ["FULL", "IS", "OOS"]:
                    st = pack(r[MSK[w]])
                    sp, v2 = SPYW[w], V2W[w]
                    lg = legswin(st, sp)
                    keep.append(dict(
                        panel=nm, arm=a, gross=PUBLISHED_G, cost=COST0, sched=sn, window=w,
                        CAGR=st["CAGR"], Sharpe=st["Sharpe"], MaxDD=st["MaxDD"], H1=st["H1"],
                        H2=st["H2"], spy_CAGR=sp["CAGR"], spy_Sharpe=sp["Sharpe"],
                        spy_MaxDD=sp["MaxDD"], **lg, pass4b=all(lg.values()),
                        pass4a=pass4a(st, v2),
                        mg_H1=st["H1"] - sp["H1"], mg_H2=st["H2"] - sp["H2"],
                        mg_DD=st["MaxDD"] - DD_CAP * sp["MaxDD"],
                        mg_CAGR=st["CAGR"] - CAGR_FLOOR * sp["CAGR"]))
        del series, ens, pans
    WF = pd.DataFrame(wf)
    dump(WF, "walkforward.csv")
    live = WF[~WF["is_empty"].astype(bool)]
    P("")
    P(f"{'panel':<7} {'sched':<10} {'chooser':<17} {'arm':<11} {'g':>5} {'OOS CAGR':>9} "
      f"{'Sharpe':>7} {'MaxDD':>8} {'4b':>5} {'4a':>5}")
    for _, r in live.iterrows():
        P(f"{r.panel:<7} {r.sched:<10} {r.chooser:<17} {str(r.arm):<11} {r.gross:>5.2f} "
          f"{r.OOS_CAGR:>9.2%} {r.OOS_Sharpe:>7.3f} {r.OOS_MaxDD:>8.2%} "
          f"{str(bool(r.OOS_4b)):>5} {str(bool(r.OOS_4a)):>5}")
    n4b, n4a, ntot = int(live.OOS_4b.sum()), int(live.OOS_4a.sum()), len(live)
    n_empty = int(WF["is_empty"].sum())
    P(f"RULE 8 SUMMARY: OOS 4b {n4b} of {ntot} live picks, 4a {n4a} of {ntot}; "
      f"{n_empty} IS pick sets EMPTY")
    H_WF = bool(n4b > 0)

    # ================================ THE RE-READ ================================
    P("")
    P("=" * 100)
    P("THE RE-READ -- every 4b leg WITH ITS OWN MARGIN for the two subject books at g=0.75,")
    P("10 bps, on each SHIFT5 calendar and on the ENSEMBLE5 book (which has no date to pick)")
    P("=" * 100)
    KP = pd.DataFrame(keep)
    dump(KP, "reread.csv")
    for nm in PANELS:
        for a in ["EWELIG", "CAND20"]:
            P(f"\n  panel {nm} / {a} / g={PUBLISHED_G} / {COST0:.0f} bps  "
              f"(margins: + = the leg clears, - = it misses)")
            P(f"  {'sched':<10} {'win':<5} {'CAGR':>8} {'Sharpe':>7} {'MaxDD':>8} "
              f"{'mgH1':>8} {'mgH2':>8} {'mgDD':>8} {'mgCAGR':>8} {'4b':>6} {'4a':>6}")
            sub = KP[(KP.panel == nm) & (KP.arm == a)]
            for _, r in sub.iterrows():
                P(f"  {r.sched:<10} {r.window:<5} {r.CAGR:>8.2%} {r.Sharpe:>7.3f} "
                  f"{r.MaxDD:>8.2%} {r.mg_H1:>+8.4f} {r.mg_H2:>+8.4f} {r.mg_DD:>+8.2%} "
                  f"{r.mg_CAGR:>+8.2%} {str(bool(r.pass4b)):>6} {str(bool(r.pass4a)):>6}")
    P("")
    P("  FULL-window 4b pass count over the 5 SHIFT5 calendars + ENSEMBLE5 (6 readings each):")
    for nm in PANELS:
        for a in ["EWELIG", "CAND20"]:
            s = KP[(KP.panel == nm) & (KP.arm == a) & (KP.window == "FULL")]
            o = KP[(KP.panel == nm) & (KP.arm == a) & (KP.window == "OOS")]
            P(f"    {nm:<6} {a:<8} FULL {int(s.pass4b.sum())} of {len(s)}   "
              f"OOS {int(o.pass4b.sum())} of {len(o)}   "
              f"ENSEMBLE5 FULL {bool(s[s.sched=='ENSEMBLE5'].pass4b.iloc[0])} / "
              f"OOS {bool(o[o.sched=='ENSEMBLE5'].pass4b.iloc[0])}")

    # ---- hypothesis table ----
    P("")
    P("=" * 100)
    P("PRE-REGISTERED HYPOTHESES -- verdicts")
    P("=" * 100)
    hyp = [
        dict(name="H_DATE", bar=f"|margin| < offset spread, U56/EWELIG/{LEG}/g={PUBLISHED_G}/"
             f"{COST0:.0f}bps", result=f"ratio {cell('U56','EWELIG').ratio:.3f}", passed=H_DATE),
        dict(name="H_FLIP", bar=f">=1 of {len(OFFGRIDS[OFF_HEAD])} offsets clears the leg",
             result=f"{h_flip[OFF_HEAD]} of {len(OFFGRIDS[OFF_HEAD])}", passed=H_FLIP),
        dict(name="H_LADDER", bar=f">={LADDER_BAR} of 30 rungs with an offset clearing",
             result=f"{n_any_ew} of 30", passed=H_LADDER),
        dict(name="H_CAND20", bar="CAND20 ratio >= 1 on all 3 grids",
             result=str({k: round(v, 3) for k, v in h_c20.items()}), passed=H_CAND20),
        dict(name="H_PANEL", bar="same DATE/VERDICT reading on all 3 panels",
             result=str(h_panel), passed=H_PANEL),
        dict(name="H_COST", bar=f"0 bps spread within {COST_BAR}x of 10 bps",
             result=f"{s0:.4f} vs {s10:.4f}", passed=H_COST),
        dict(name="H_WF", bar="rule 8: at least one IS-only pick reaches 4b OOS",
             result=f"4b {n4b}/{ntot}, 4a {n4a}/{ntot}", passed=H_WF),
    ]
    HY = pd.DataFrame(hyp)
    dump(HY, "hypotheses.csv")
    for _, r in HY.iterrows():
        P(f"  {r['name']:<10} {'PASS' if r.passed else 'FAIL':<5} bar: {r.bar}")
        P(f"  {'':<10} {'':<5} got: {r.result}")

    P("")
    P("=" * 100)
    P("SURVIVORSHIP: U56/B136/SMALL are current-constituent lists; every CAGR and MaxDD LEVEL is")
    P("  optimistic.  The headline object is a RATIO of a margin to a spread on the SAME book and")
    P("  the SAME days and is far less exposed; the leg verdicts and rule-8 triples are read")
    P("  against SPY, which is not survivorship-inflated, so those are upper bounds.")
    P(f"done in {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"wrote {STEM}.console.txt")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Idea 675 (cloud, 2026-09-15) -- is U56/CAND20's SINGLE-RUNG 4b pass a KNIFE EDGE or a real
window?

THE QUESTION (queue, 2026-09-11)
  Idea 670 found that the record's own 2026-09-04 KEEP 4b book -- CAND20, top-20 equal weight,
  NO vol scaler -- passes PROTOCOL 4b at EXACTLY g = 0.75 and nowhere else on its 8-rung gross
  ladder, while every band-book pass sits at g >= 0.95.  The queue asks: re-run that one book on a
  0.01-resolution gross ladder, report the TRUE width of its pass window, and say whether the
  window survives rule-8 selection and a cost sweep.

THE BOOK (idea 670's `CAND20`, reproduced byte-for-byte at G3; NOT re-specified here)
  Each rebalance, rank every priced name above its own 200d MA with 20d realised vol < 0.60 by the
  v1 composite `mean(pct-rank 12-1 mom, pct-rank 6m, pct-rank 3m) x (1 if above 200d MA else 0.5)`
  WITHOUT the `/sqrt(vol20)` term; hold the top 20 at g/k each where k = min(20, #eligible), the
  rest in CASH (de-gross, never re-spread).  Weekly, decided at the close, executed next close,
  10 bps per unit turnover.

WHY A LADDER RESOLUTION IS THE WHOLE QUESTION
  670's ladder is {0.20, 0.35, 0.50, 0.60, 0.75, 0.85, 0.95, 1.00}: it never tests 0.65, 0.70,
  0.80.  Idea 804 then established (24 of 24 bands) that a 4b band's LOWER edge is the CAGR floor
  alone and its UPPER edge the DD cap alone, both monotone in g, with the three Sharpe legs flat in
  gross to within 0.02.  Two monotone crossings bound an INTERVAL, so "passes at exactly one rung"
  is a statement about the ladder unless the interval is genuinely narrower than a rung.  This run
  measures the interval instead of sampling it.

WHAT IS TUNED AND WHAT IS REPORTED (PROTOCOL 4: max 2 tuned parameters)
  TUNED 1  GROSS RESOLUTION (the queue's own first dial), 5 levels, every one reported:
           RECORD8  670's own 8 irregular rungs          (the claim's own ladder)
           STEP05   0.05 .. 1.50 step 0.05   (30 rungs)
           STEP01   0.01 .. 1.50 step 0.01  (150 rungs)   (the queue's asked-for resolution)
           STEP002  0.002 .. 1.50 step 0.002 (750 rungs)
           EXACT    the two level-leg crossings solved by bisection to 1e-6 of gross
  TUNED 2  COST RUNG (the queue's own second dial), 4 levels: 0 / 10 / 25 / 50 bps.
  REPORTED AXES (nothing fitted on them; every point published):
           window FULL / IS (2009-2016) / OOS (2017-2026); panel U56 / B136 / SMALL;
           rebalance offset, the 5 phases of a 5-trading-day schedule (idea 806's convention
           axis); companion arms CAND20_VS / CAND10 / CAND05 / CAND20_NOCAP / EWELIG / BAND03
           (= RULES v2 live) / SPYBH (= g x SPY, the zero-signal exposure control).

PRE-REGISTERED BARS (fixed before any number is read; both directions reported)
  H_KNIFE   the pass window is a KNIFE EDGE iff its width < 0.05 of gross -- one rung of the
            record's own 0.05 ladder -- at 10 bps on the FULL window.  Otherwise it is a WINDOW.
  H_LADDER  the "single rung" is a LADDER ARTEFACT iff the 0.01 ladder finds >= 2 passing rungs
            where 670's 8-rung ladder found exactly 1.
  H_INTERIOR the published g = 0.75 is interior to the window by >= 0.02 on BOTH sides at 10 bps,
            on FULL and on OOS.
  H_OFFSET  (idea 806's standing clause) the window is a WINDOW and not a DATE only if its width
            exceeds the spread of its own endpoints across the 5 rebalance offsets.
  H_COST    the window is non-empty at 25 bps.  The rung at which it empties is reported.
  H_WF      (rule 8, required) g chosen on 2009-2016 ONLY, OOS 2017-2026 read once, both KEEP
            paths, against SPY and RULES v2 in the same window.
  H_TRAVEL  the window is non-empty on B136 and on SMALL.

GATES (all printed before any result number)
  G1  the fast runner == engine.backtest on returns and turnover
  G2  BAND03 at g=0.75 == baseline.rules_v2_weights elementwise
  G3  idea 670's committed `.grid.csv` CAND20 rows reproduce -- 16 rows (2 panels x 8 rungs),
      metrics to a 5e-3 vintage bar and the five 4b LEGS plus pass4b/pass4a EXACTLY.  The leg
      pattern is the load-bearing half: it is the "passes at exactly 0.75" claim itself.
  G4  the committed U56 triples (SPY, RULES v2)
  G5  monotonicity on the fine ladder: CAGR(g) non-decreasing and |MaxDD(g)| non-decreasing (this
      is what makes a bisected endpoint meaningful), with the Sharpe-leg spread reported beside it
  G6  bisection == ladder: each EXACT endpoint lies inside the bracketing pair of 0.002 rungs
  G7  determinism (rebuild, compare)
  G8  the analytic ray: SPYBH (g x SPY) must read MaxDD(g)/MaxDD(SPY) = g and CAGR within cost of
      the g-blend -- this gates the gross machinery independently of any signal

PROTOCOL: 10 bps primary, t+1, weekly, warm-up 260 days, IS 2009-2016 / OOS 2017-2026.
Nothing in RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py is modified.

SURVIVORSHIP: U56 / B136 / SMALL are current-constituent lists, so every CAGR and drawdown LEVEL
below is optimistic -- the book's and the comparands' alike.  A 4b bar is a RATIO of the book's
level to SPY's, and SPY is not survivorship-inflated, so the bars are NOT protected by the
same-tape argument: the window measured here is an upper bound on the window a survivorship-free
panel would show.  Stated, not hidden.
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
COST0 = 10.0                       # PROTOCOL 2, the primary rung
FREQ = "W"
LAG = 1
BAND0 = 0.03                       # RULES v2 clause 2
MAXVOL = 0.60                      # the book's own vol cap
WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70    # PROTOCOL 4b
KNIFE_BAR = 0.05                   # H_KNIFE: one rung of the record's own 0.05 ladder
INTERIOR_BAR = 0.02                # H_INTERIOR
PUBLISHED_G = 0.75
BISECT_TOL = 1e-6
GMIN_SEARCH, GMAX_SEARCH = 0.002, 2.0

# ---- TUNED DIAL 1: the gross resolution -------------------------------------------------------
RECORD8 = [0.20, 0.35, 0.50, 0.60, 0.75, 0.85, 0.95, 1.00]     # idea 670's own ladder
LADDERS = {
    "RECORD8": RECORD8,
    "STEP05": [round(0.05 * i, 4) for i in range(1, 31)],
    "STEP01": [round(0.01 * i, 4) for i in range(1, 151)],
    "STEP002": [round(0.002 * i, 4) for i in range(1, 751)],
}
RESOLUTIONS = ["RECORD8", "STEP05", "STEP01", "STEP002", "EXACT"]
# ---- TUNED DIAL 2: the cost rung --------------------------------------------------------------
COSTS = [0.0, 10.0, 25.0, 50.0]

# ---- reported axes ----------------------------------------------------------------------------
PANELS = ["U56", "B136", "SMALL"]
ARMS = ["CAND20", "CAND20_VS", "CAND10", "CAND05", "CAND20_NOCAP", "EWELIG", "BAND03", "SPYBH"]
ARM_SRC = {
    "CAND20": "2026-09-04 KEEP 4b: top-20 equal weight, NO vol scaler  <-- THE SUBJECT",
    "CAND20_VS": "idea 668 N dial (vol scaler ON, as baseline.score)",
    "CAND10": "width companion of the KEEP 4b book",
    "CAND05": "RULES v1 book width",
    "CAND20_NOCAP": "idea 668 VOLCAP dial, cap OFF",
    "EWELIG": "2026-09-03 memo Finding 2 (equal-weight all eligible)",
    "BAND03": "RULES v2 live (baseline.rules_v2_weights)",
    "SPYBH": "ZERO-SIGNAL exposure control (g x SPY)",
}
SUBJECT = ("U56", "CAND20")
OFFSETS = [0, 1, 2, 3, 4]          # the 5 phases of a 5-trading-day schedule (idea 806's axis)
WINDOWS = ["FULL", "IS", "OOS"]

SPY_U56 = (0.1516, 0.8861, -0.3372)
V2_U56 = (0.0863, 1.2018, -0.1205)
TOL_C, TOL_S, TOL_D = 0.004, 0.030, 0.015
G3_BAR = 5e-3                      # vintage bar: 670's tape ends 2026-09-11, today's is longer
PARENT = ROOT / "research" / "backtests" / \
    "2026-09-11_is-the-GROSS-dial-s-4b-FOOTPRINT-the-CAGR-FLOOR-alone_C.grid.csv"

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
# runner (910's vectorised equivalent of engine.backtest, generalised to an arbitrary reb mask)
# ================================================================================================
def offset_mask(idx, k):
    """The k-th phase of a 5-trading-day rebalance schedule (the record's convention axis)."""
    return pd.Series(np.arange(len(idx)) % 5 == k, index=idx)


class Panel:
    def __init__(self, name, px, sched):
        self.name, self.px, self.sched = name, px, sched
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        T, N = self.rets.shape
        self.T, self.N = T, N
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, N)), C[:-1]])
        raw = rebalance_mask(self.idx, FREQ) if sched == "W" else offset_mask(self.idx, sched)
        mk = raw.shift(LAG, fill_value=False).values.copy()
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
        ARp = Ap * panel.Rp
        self.ARp = ARp
        self.Sp = ARp.sum(axis=1)
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


# ================================================================================================
# the two 4b conventions, both reported
#   CONV670 -- idea 670's, the convention the "passes at exactly 0.75" claim lives in:
#              halves and levels on the FULL window, plus a separate OOS-Sharpe leg
#   CONVWIN -- the window-local form used by the record's rule-8 runs (867/910):
#              halves and levels inside whichever window is being read
# ================================================================================================
def legs670(full, oos, spy_full, spy_oos):
    return dict(L1_H1=bool(full["H1"] > spy_full["H1"]),
                L2_H2=bool(full["H2"] > spy_full["H2"]),
                L3_OOS=bool(oos["Sharpe"] > spy_oos["Sharpe"]),
                L4_DDcap=bool(abs(full["MaxDD"]) <= DD_CAP * abs(spy_full["MaxDD"])),
                L5_CAGRfloor=bool(full["CAGR"] >= CAGR_FLOOR * spy_full["CAGR"]))


def legswin(s, spy):
    return dict(L1_H1=bool(s["H1"] > spy["H1"]), L2_H2=bool(s["H2"] > spy["H2"]),
                L3_OOS=True,
                L4_DDcap=bool(s["MaxDD"] >= DD_CAP * spy["MaxDD"]),
                L5_CAGRfloor=bool(s["CAGR"] >= CAGR_FLOOR * spy["CAGR"]))


def pass4a(s, base):
    return bool(s["H1"] > base["H1"] and s["H2"] > base["H2"] and s["MaxDD"] >= base["MaxDD"])


# ================================================================================================
# the arms (idea 670's definitions, unchanged)
# ================================================================================================
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
    """Gross-1.0 weights. Every arm is exactly linear in g, so Book.at(g) is the g rung."""
    sc_v, sc_n, above, vol20 = pre
    if arm == "BAND03":
        return ew_gross1(px).where(band_state(px, BAND0) & px.notna(), 0.0).values
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


# ================================================================================================
# scoring one (book, cost) over the three windows
# ================================================================================================
def score_g(bk: Book, g, cost, spyref, v2ref):
    pan = bk.pan
    r, turn = bk.at(g, cost)
    out = {}
    for w in WINDOWS:
        out[w] = pack(r[pan.masks[w]])
    L670 = legs670(out["FULL"], out["OOS"], spyref["FULL"], spyref["OOS"])
    row = dict(gross=g, cost=cost,
               turn_yr=float(turn[pan.masks["FULL"]].sum()
                             / (pan.masks["FULL"].sum() / 252.0)))
    for w in WINDOWS:
        for k, v in out[w].items():
            row[f"{w}_{k}"] = v
    row.update({f"c670_{k}": v for k, v in L670.items()})
    row["c670_pass4b"] = bool(all(L670.values()))
    row["c670_pass4a"] = pass4a(out["FULL"], v2ref["FULL"])
    for w in ("IS", "OOS"):
        Lw = legswin(out[w], spyref[w])
        row.update({f"cwin{w}_{k}": v for k, v in Lw.items()})
        row[f"cwin{w}_pass4b"] = bool(all(Lw.values()))
        row[f"cwin{w}_pass4a"] = pass4a(out[w], v2ref[w])
    return row


def bisect(f, lo, hi, tol=BISECT_TOL):
    """Smallest g in [lo,hi] with f(g) >= 0, assuming f non-decreasing. None if no crossing."""
    flo, fhi = f(lo), f(hi)
    if flo >= 0:
        return lo
    if fhi < 0:
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


def exact_window(bk, cost, spyref, conv, win):
    """(g_min from the CAGR floor, g_max from the DD cap) by bisection to BISECT_TOL."""
    if conv == "c670":
        wc = wd = "FULL"
    else:
        wc = wd = win
    ref = spyref[wc]

    def f_cagr(g):
        r, _ = bk.at(g, cost)
        c, _, _ = fmet(r[bk.pan.masks[wc]])
        return c - CAGR_FLOOR * ref["CAGR"]

    def f_dd(g):
        r, _ = bk.at(g, cost)
        _, _, d = fmet(r[bk.pan.masks[wd]])
        return DD_CAP * abs(spyref[wd]["MaxDD"]) - abs(d)      # non-increasing in g

    gmin = bisect(f_cagr, GMIN_SEARCH, GMAX_SEARCH)
    # g_max: f_dd is non-increasing, so bisect on its negation flipped
    gmax = bisect(lambda g: -f_dd(g), GMIN_SEARCH, GMAX_SEARCH)
    if gmax is None:
        gmax = GMAX_SEARCH          # DD cap never breached inside the search range
    else:
        gmax = gmax - BISECT_TOL
    return gmin, gmax


def sharpe_legs_ok(bk, cost, spyref, conv, win, probe=(0.25, 0.50, 0.75, 1.00)):
    """Do the gross-FLAT Sharpe legs pass?  They are flat in g to ~0.003 (G5), so a level-leg
    window is a 4b window only if these pass; probed at four grosses and required at all four."""
    out = []
    for g in probe:
        r, _ = bk.at(g, cost)
        st = {w: pack(r[bk.pan.masks[w]]) for w in WINDOWS}
        if conv == "c670":
            L = legs670(st["FULL"], st["OOS"], spyref["FULL"], spyref["OOS"])
            out.append(bool(L["L1_H1"] and L["L2_H2"] and L["L3_OOS"]))
        else:
            L = legswin(st[win], spyref[win])
            out.append(bool(L["L1_H1"] and L["L2_H2"]))
    return bool(all(out)), out


def exact_row(panel, arm, sched, cost, bk, spyref, conv, win):
    """One exact-endpoint row.  `level_width` is the width of the two monotone level legs'
    intersection; `width` is the 4b window, which is EMPTY (0.0) whenever the gross-flat Sharpe
    legs fail -- a distinction the ladder makes automatically and a bisection does not."""
    gmin, gmax = exact_window(bk, cost, spyref, conv, win)
    sh, shdet = sharpe_legs_ok(bk, cost, spyref, conv, win)
    lw = np.nan if gmin is None else max(0.0, gmax - gmin)
    return dict(panel=panel, arm=arm, sched=sched, cost=cost, conv=conv, window=win,
                g_min=gmin, g_max=gmax, level_width=lw, sharpe_ok=sh,
                sharpe_detail="".join("y" if x else "n" for x in shdet),
                width=(0.0 if (not sh or gmin is None or not np.isfinite(lw)) else lw),
                is_empty=bool((not sh) or gmin is None or not np.isfinite(lw) or lw <= 0.0))


# ================================================================================================
# gates
# ================================================================================================
def run_gates(pans, books, spyref, v2ref, pre):
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
    P(f"G2  BAND03 g=0.75 == rules_v2_weights      max|dw| {dw:.3e}   -> "
      f"{'PASS' if ok['G2'] else 'FAIL'}")

    bk = books[("U56", "W", "BAND03")]
    r_fast, t_fast = bk.at(0.75, COST0)
    res = backtest(px, rules_v2_weights(px, band=BAND0, gross=0.75), cost_bps=COST0, freq=FREQ)
    dr = float(np.nanmax(np.abs(r_fast - res["returns"].values)))
    dt = float(np.nanmax(np.abs(t_fast - res["turnover"].values)))
    # and on the SUBJECT itself, which is the book that matters
    bs = books[("U56", "W", "CAND20")]
    rs, ts = bs.at(0.75, COST0)
    wsub = pd.DataFrame(arm_w1(px, pre["U56"], "CAND20") * 0.75, index=px.index, columns=px.columns)
    res2 = backtest(px, wsub, cost_bps=COST0, freq=FREQ)
    dr2 = float(np.nanmax(np.abs(rs - res2["returns"].values)))
    dt2 = float(np.nanmax(np.abs(ts - res2["turnover"].values)))
    ok["G1"] = max(dr, dt, dr2, dt2) < 1e-10
    P(f"G1  fast Book.at == engine.backtest        BAND03 max|dr| {dr:.3e} max|dturn| {dt:.3e};  "
      f"CAND20 max|dr| {dr2:.3e} max|dturn| {dt2:.3e}   -> {'PASS' if ok['G1'] else 'FAIL'}")

    s = spyref["U56"]["FULL"]
    v = v2ref["U56"]["FULL"]
    d1 = (abs(s["CAGR"] - SPY_U56[0]), abs(s["Sharpe"] - SPY_U56[1]), abs(s["MaxDD"] - SPY_U56[2]))
    d2 = (abs(v["CAGR"] - V2_U56[0]), abs(v["Sharpe"] - V2_U56[1]), abs(v["MaxDD"] - V2_U56[2]))
    ok["G4"] = all(a < b for a, b in zip(d1, (TOL_C, TOL_S, TOL_D))) and \
        all(a < b for a, b in zip(d2, (TOL_C, TOL_S, TOL_D)))
    P(f"G4  committed U56 triples   SPY {s['CAGR']:.4%}/{s['Sharpe']:.4f}/{s['MaxDD']:.4%}  "
      f"(committed {SPY_U56[0]:.2%}/{SPY_U56[1]:.4f}/{SPY_U56[2]:.2%})")
    P(f"                            v2  {v['CAGR']:.4%}/{v['Sharpe']:.4f}/{v['MaxDD']:.4%}  "
      f"(committed {V2_U56[0]:.2%}/{V2_U56[1]:.4f}/{V2_U56[2]:.2%})   -> "
      f"{'PASS' if ok['G4'] else 'FAIL'}")

    # G8 -- the analytic ray on the zero-signal control
    worst_dd, worst_c = 0.0, 0.0
    for pn in PANELS:
        z = books[(pn, "W", "SPYBH")]
        sp = spyref[pn]["FULL"]
        for g in (0.25, 0.50, 0.75, 1.00):
            rz, _ = z.at(g, 0.0)
            c, _, d = fmet(rz[pans[(pn, "W")].masks["FULL"]])
            worst_dd = max(worst_dd, abs(abs(d) / abs(sp["MaxDD"]) - g) if g < 1.0 else
                           abs(abs(d) / abs(sp["MaxDD"]) - 1.0))
            worst_c = max(worst_c, abs(c - ((1 + sp["CAGR"]) ** 1 - 1) * g) if g == 1.0 else 0.0)
    ok["G8"] = worst_dd < 0.05
    P(f"G8  SPYBH analytic ray: |MaxDD(g)|/|MaxDD(SPY)| must read g   worst dev over 3x4 "
      f"{worst_dd:.3e}; g=1.00 CAGR dev from SPY {worst_c:.3e}   -> {'PASS' if ok['G8'] else 'FAIL'}")
    return ok


def gate_parent(fine):
    """G3 -- reproduce idea 670's committed CAND20 rows: metrics to a vintage bar, LEGS exactly."""
    if not PARENT.exists():
        P("G3  670's .grid.csv NOT FOUND -- gate cannot run")
        return False, pd.DataFrame()
    par = pd.read_csv(PARENT)
    par = par[par.arm == "CAND20"]
    rows = []
    for _, pr in par.iterrows():
        h = fine[(fine.panel == pr.panel) & (fine.arm == "CAND20") & (fine.sched == "W")
                 & (fine.cost == COST0) & (np.abs(fine.gross - pr.gross) < 1e-9)]
        if h.empty:
            continue
        h = h.iloc[0]
        d = dict(panel=pr.panel, gross=float(pr.gross),
                 dCAGR=abs(h.FULL_CAGR - pr.CAGR), dSharpe=abs(h.FULL_Sharpe - pr.Sharpe),
                 dMaxDD=abs(h.FULL_MaxDD - pr.MaxDD),
                 dH1=abs(h.FULL_H1 - pr.H1), dH2=abs(h.FULL_H2 - pr.H2),
                 dOOS_Sharpe=abs(h.OOS_Sharpe - pr.OOS_Sharpe))
        legs_ok = all(bool(h[f"c670_{k}"]) == bool(pr[k]) for k in
                      ("L1_H1", "L2_H2", "L3_OOS", "L4_DDcap", "L5_CAGRfloor"))
        d["legs_match"] = legs_ok
        d["pass4b_match"] = bool(h.c670_pass4b) == bool(pr.pass4b)
        d["pass4a_match"] = bool(h.c670_pass4a) == bool(pr.pass4a)
        d["worst_metric"] = max(d["dCAGR"], d["dSharpe"], d["dMaxDD"], d["dH1"], d["dH2"],
                                d["dOOS_Sharpe"])
        rows.append(d)
    G = pd.DataFrame(rows)
    G["exact"] = G.legs_match & G.pass4b_match & G.pass4a_match
    legs = bool(G.exact.all())
    mets = bool((G.worst_metric < G3_BAR).all())
    P(f"G3  670's committed CAND20 rows: {len(G)} of {len(par)} matched.  LEGS + pass4b + pass4a "
      f"exact on {int(G.exact.sum())} of {len(G)}; worst "
      f"metric deviation {G.worst_metric.max():.3e} against the {G3_BAR:.0e} vintage bar   -> "
      f"{'PASS' if (legs and mets) else 'FAIL'}")
    for pn in sorted(G.panel.unique()):
        gp = G[G.panel == pn]
        sub = "  <-- THE SUBJECT PANEL" if pn == SUBJECT[0] else ""
        P(f"      G3[{pn}]  {int(gp.exact.sum())} of {len(gp)} rows exact on every leg and "
          f"verdict, worst metric deviation {gp.worst_metric.max():.3e}  -> "
          f"{'PASS' if (gp.exact.all() and (gp.worst_metric < G3_BAR).all()) else 'FAIL'}{sub}")
    for _, r in G.iterrows():
        P(f"      {r.panel:5s} g={r.gross:.2f}  worst|d| {r.worst_metric:.2e}  legs "
          f"{'OK' if r.legs_match else 'MISMATCH'}  4b {'OK' if r.pass4b_match else 'MISMATCH'}")
    P("      (670's tape ends 2026-09-11 and today's is longer, so the metric bar is a vintage")
    P("       bar; the LEG pattern is the claim itself and is required to match exactly.)")
    return bool(legs and mets), G


# ================================================================================================
# main
# ================================================================================================
def main():
    t0 = time.time()
    P("=" * 112)
    P("IDEA 675 (cloud, 2026-09-15) -- is U56/CAND20's SINGLE-RUNG 4b pass a KNIFE EDGE or a real")
    P("                               window?")
    P("=" * 112)
    P(f"TUNED 1 gross resolution ({len(RESOLUTIONS)} levels, all reported): {RESOLUTIONS}")
    P(f"        RECORD8 = 670's own ladder {RECORD8}")
    P(f"        STEP05 {len(LADDERS['STEP05'])} rungs, STEP01 {len(LADDERS['STEP01'])}, "
      f"STEP002 {len(LADDERS['STEP002'])}, EXACT = bisection to {BISECT_TOL:.0e} of gross")
    P(f"TUNED 2 cost rung: {[int(c) for c in COSTS]} bps")
    P(f"reported axes: window {WINDOWS} x panel {PANELS} x offset {OFFSETS} (5-day phases) x "
      f"{len(ARMS)} arms")
    P(f"SUBJECT: {SUBJECT[0]}/{SUBJECT[1]} -- {ARM_SRC['CAND20']}")
    P(f"BARS: H_KNIFE width < {KNIFE_BAR} of gross; H_LADDER >= 2 passing rungs at 0.01; "
      f"H_INTERIOR g={PUBLISHED_G} interior by >= {INTERIOR_BAR}; H_OFFSET width > offset spread;")
    P(f"      H_COST non-empty at 25 bps; H_WF rule 8 both KEEP paths; H_TRAVEL B136 and SMALL.")
    P("")
    P("TWO 4b CONVENTIONS, both reported: c670 = idea 670's (halves and levels on the FULL window")
    P("  plus a separate OOS-Sharpe leg) -- the convention the 'passes at exactly 0.75' claim lives")
    P("  in; cwin = the window-local form the record's rule-8 runs use (867/910).")
    P("")

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
    P("")

    # panels: (panel, sched) for sched in {"W"} u OFFSETS (offsets only for U56, the subject's axis)
    pans, pre = {}, {}
    for nm in PANELS:
        pre[nm] = prep(raw[nm])
        pans[(nm, "W")] = Panel(nm, raw[nm], "W")
    for k in OFFSETS:
        pans[("U56", k)] = Panel("U56", raw["U56"], k)

    # comparands: SPY buy-and-hold (schedule-free) and RULES v2 live (canonical W, g=0.75)
    spyref, v2ref = {}, {}
    for nm in PANELS:
        pan = pans[(nm, "W")]
        spyref[nm] = {w: pack(pan.spy[pan.masks[w]]) for w in WINDOWS}
        v2 = Book(pan, arm_w1(raw[nm], pre[nm], "BAND03")).at(0.75, COST0)[0]
        v2ref[nm] = {w: pack(v2[pan.masks[w]]) for w in WINDOWS}

    books = {}
    for nm in PANELS:
        for a in ARMS:
            books[(nm, "W", a)] = Book(pans[(nm, "W")], arm_w1(raw[nm], pre[nm], a))
    for k in OFFSETS:
        books[("U56", k, "CAND20")] = Book(pans[("U56", k)], arm_w1(raw["U56"], pre["U56"], "CAND20"))
    P(f"built {len(books)} (panel, schedule, arm) books")
    P("")

    gates = run_gates(pans, books, spyref, v2ref, pre)

    # --------------------------------------------------------------------------------------
    # the ladders
    # --------------------------------------------------------------------------------------
    P("")
    P("=" * 112)
    P("RUNNING THE LADDERS")
    P("=" * 112)
    rows = []
    t = time.time()
    # (a) the SUBJECT: every resolution x every cost x every offset
    for sched in ["W"] + OFFSETS:
        bk = books[("U56", sched, "CAND20")]
        gs = sorted(set(LADDERS["RECORD8"] + LADDERS["STEP05"] + LADDERS["STEP01"]
                        + LADDERS["STEP002"]))
        for cost in COSTS:
            for g in gs:
                r = score_g(bk, g, cost, spyref["U56"], v2ref["U56"])
                r.update(panel="U56", arm="CAND20", sched=str(sched))
                rows.append(r)
    P(f"  subject U56/CAND20: {len(rows):,} rows  ({time.time()-t:.1f}s)")
    # (b) companions and travel: STEP01 x every cost, canonical W only
    t = time.time()
    n0 = len(rows)
    for nm in PANELS:
        for a in ARMS:
            if (nm, a) == SUBJECT:
                continue
            bk = books[(nm, "W", a)]
            for cost in COSTS:
                for g in LADDERS["STEP01"]:
                    r = score_g(bk, g, cost, spyref[nm], v2ref[nm])
                    r.update(panel=nm, arm=a, sched="W")
                    rows.append(r)
    P(f"  companions + travel: {len(rows)-n0:,} rows  ({time.time()-t:.1f}s)")
    fine = pd.DataFrame(rows)
    del rows

    # G7 determinism
    bk2 = Book(pans[("U56", "W")], arm_w1(raw["U56"], pre["U56"], "CAND20"))
    a = fine[(fine.panel == "U56") & (fine.arm == "CAND20") & (fine.sched == "W")
             & (fine.cost == COST0)].sort_values("gross")
    d = max(abs(score_g(bk2, float(g), COST0, spyref["U56"], v2ref["U56"])["FULL_Sharpe"]
                - float(s)) for g, s in zip(a.gross.values[::37], a.FULL_Sharpe.values[::37]))
    gates["G7"] = d == 0.0
    P("")
    P(f"G7  DETERMINISM (rebuild the subject, {len(a.gross.values[::37])} rungs re-scored)  "
      f"max|dSharpe| {d:.3e}   -> {'PASS' if gates['G7'] else 'FAIL'}")

    # G5 monotonicity + the Sharpe-flatness reading
    sub = fine[(fine.panel == "U56") & (fine.arm == "CAND20") & (fine.sched == "W")
               & (fine.cost == COST0)].sort_values("gross")
    dC = np.diff(sub.FULL_CAGR.values)
    dD = np.diff(np.abs(sub.FULL_MaxDD.values))
    sp = {w: float(sub[f"{w}_Sharpe"].max() - sub[f"{w}_Sharpe"].min()) for w in WINDOWS}
    gates["G5"] = bool((dC >= -1e-12).all() and (dD >= -1e-12).all())
    P(f"G5  monotonicity on the fine ladder ({len(sub)} rungs): CAGR(g) non-decreasing "
      f"{int((dC >= -1e-12).sum())}/{len(dC)}, |MaxDD(g)| non-decreasing "
      f"{int((dD >= -1e-12).sum())}/{len(dD)}   -> {'PASS' if gates['G5'] else 'FAIL'}")
    P(f"      Sharpe spread over the WHOLE ladder: FULL {sp['FULL']:.4f}  IS {sp['IS']:.4f}  "
      f"OOS {sp['OOS']:.4f}   (idea 804's 'gross cannot decide a Sharpe leg', re-read here)")

    P("")
    gates["G3"], G3 = gate_parent(fine)

    # --------------------------------------------------------------------------------------
    # EXACT endpoints
    # --------------------------------------------------------------------------------------
    P("")
    erows = []
    for sched in ["W"] + OFFSETS:
        bk = books[("U56", sched, "CAND20")]
        for cost in COSTS:
            for conv, win in [("c670", "FULL"), ("cwin", "IS"), ("cwin", "OOS")]:
                erows.append(exact_row("U56", "CAND20", str(sched), cost, bk,
                                       spyref["U56"], conv, win))
    for nm in PANELS:
        for a in ARMS:
            if (nm, a) == SUBJECT:
                continue
            bk = books[(nm, "W", a)]
            for cost in COSTS:
                for conv, win in [("c670", "FULL"), ("cwin", "IS"), ("cwin", "OOS")]:
                    erows.append(exact_row(nm, a, "W", cost, bk, spyref[nm], conv, win))
    EX = pd.DataFrame(erows)

    # G6 bisection vs ladder
    worst = 0.0
    s2 = fine[(fine.panel == "U56") & (fine.arm == "CAND20") & (fine.sched == "W")].copy()
    for cost in COSTS:
        e = EX[(EX.panel == "U56") & (EX.arm == "CAND20") & (EX.sched == "W")
               & (EX.cost == cost) & (EX.conv == "c670")].iloc[0]
        lad = s2[(s2.cost == cost)].sort_values("gross")
        okc = lad[lad.c670_L5_CAGRfloor]
        okd = lad[lad.c670_L4_DDcap]
        if len(okc) and e.g_min is not None:
            worst = max(worst, max(0.0, float(e.g_min) - float(okc.gross.min())))
        if len(okd):
            worst = max(worst, max(0.0, float(okd.gross.max()) - float(e.g_max)))
    gates["G6"] = worst <= 0.002 + 1e-9
    P("")
    P(f"G6  bisection == ladder: every EXACT endpoint inside the bracketing 0.002 rungs, worst "
      f"overshoot {worst:.3e}   -> {'PASS' if gates['G6'] else 'FAIL'}")

    P("")
    P(f"GATES: {sum(bool(v) for v in gates.values())} of {len(gates)} PASS  " + "  ".join(
        f"{k}={'PASS' if v else 'FAIL'}" for k, v in sorted(gates.items())))
    if not all(gates.values()):
        P("  *** a gate FAILED -- every number below is reported with that caveat ***")
    P("")
    dump(fine, "ladder.csv")
    dump(EX, "exact.csv")
    dump(G3, "gate670.csv")

    # --------------------------------------------------------------------------------------
    # H_LADDER / H_KNIFE -- the answer
    # --------------------------------------------------------------------------------------
    P("")
    P("=" * 112)
    P("H_LADDER / H_KNIFE  THE TRUE WIDTH OF U56/CAND20's 4b PASS WINDOW  (convention c670,")
    P("                    i.e. the one the published claim lives in)")
    P("=" * 112)
    lrows = []
    for cost in COSTS:
        s = fine[(fine.panel == "U56") & (fine.arm == "CAND20") & (fine.sched == "W")
                 & (fine.cost == cost)]
        for res in RESOLUTIONS:
            if res == "EXACT":
                e = EX[(EX.panel == "U56") & (EX.arm == "CAND20") & (EX.sched == "W")
                       & (EX.cost == cost) & (EX.conv == "c670")].iloc[0]
                lrows.append(dict(cost=cost, resolution=res, n_rungs=np.nan,
                                  n_pass=np.nan,
                                  g_lo=(np.nan if e["is_empty"] else e.g_min),
                                  g_hi=(np.nan if e["is_empty"] else e.g_max),
                                  width=(np.nan if e["is_empty"] else e.width),
                                  level_width=e.level_width, sharpe_ok=e.sharpe_ok,
                                  contiguous=True))
                continue
            gs = LADDERS[res]
            t = s[s.gross.isin(gs)].sort_values("gross")
            p = t[t.c670_pass4b]
            n = len(p)
            if n:
                idxs = np.flatnonzero(t.c670_pass4b.values)
                contig = bool(idxs.max() - idxs.min() + 1 == n)
                lrows.append(dict(cost=cost, resolution=res, n_rungs=len(t), n_pass=n,
                                  g_lo=float(p.gross.min()), g_hi=float(p.gross.max()),
                                  width=float(p.gross.max() - p.gross.min()),
                                  level_width=np.nan, sharpe_ok=True, contiguous=contig))
            else:
                lrows.append(dict(cost=cost, resolution=res, n_rungs=len(t), n_pass=0,
                                  g_lo=np.nan, g_hi=np.nan, width=np.nan,
                                  level_width=np.nan, sharpe_ok=False, contiguous=True))
    LD = pd.DataFrame(lrows)
    dump(LD, "resolution.csv")
    P("")
    P(f"  {'cost':>5s} {'resolution':>10s} {'rungs':>6s} {'passing':>8s} {'g_lo':>8s} "
      f"{'g_hi':>8s} {'width':>8s} {'contig':>7s} {'levelW':>8s} {'ShrpOK':>7s}")
    for _, r in LD.iterrows():
        P(f"  {int(r.cost):5d} {r.resolution:>10s} "
          f"{('' if not np.isfinite(r.n_rungs) else str(int(r.n_rungs))):>6s} "
          f"{('' if not np.isfinite(r.n_pass) else str(int(r.n_pass))):>8s} "
          f"{('    --  ' if not np.isfinite(r.g_lo) else f'{r.g_lo:8.4f}')} "
          f"{('    --  ' if not np.isfinite(r.g_hi) else f'{r.g_hi:8.4f}')} "
          f"{('  EMPTY ' if not np.isfinite(r.width) else f'{r.width:8.4f}')} "
          f"{'y' if r.contiguous else 'NO':>7s} "
          f"{('    --  ' if not np.isfinite(r.level_width) else f'{r.level_width:8.4f}')} "
          f"{('y' if r.sharpe_ok else 'NO'):>7s}")
    r8 = LD[(LD.cost == COST0) & (LD.resolution == "RECORD8")].iloc[0]
    r01 = LD[(LD.cost == COST0) & (LD.resolution == "STEP01")].iloc[0]
    rex = LD[(LD.cost == COST0) & (LD.resolution == "EXACT")].iloc[0]
    P("")
    P(f"  H_LADDER: 670's 8-rung ladder passes at {int(r8.n_pass)} rung(s); the 0.01 ladder passes "
      f"at {int(r01.n_pass)} of {int(r01.n_rungs)} rungs, g in [{r01.g_lo:.2f}, {r01.g_hi:.2f}]"
      f"  -> {'the single rung IS a LADDER ARTEFACT' if r01.n_pass >= 2 else 'not an artefact'}")
    if not np.isfinite(rex.width):
        P("  H_KNIFE : EXACT window at 10 bps is EMPTY")
    else:
        P(f"  H_KNIFE : EXACT window at 10 bps = [{rex.g_lo:.4f}, {rex.g_hi:.4f}], width "
          f"{rex.width:.4f} of gross = {rex.width/0.05:.1f} rungs of the record's own 0.05 ladder"
          f"  -> {'KNIFE EDGE' if rex.width < KNIFE_BAR else 'A REAL WINDOW'}")
    lo_ok = PUBLISHED_G - rex.g_lo
    hi_ok = rex.g_hi - PUBLISHED_G
    P(f"  H_INTERIOR: published g={PUBLISHED_G} sits {lo_ok:+.4f} above the CAGR-floor edge and "
      f"{hi_ok:+.4f} below the DD-cap edge  -> "
      f"{'INTERIOR' if min(lo_ok, hi_ok) >= INTERIOR_BAR else 'ON AN EDGE'}")
    P("")
    P("  which leg sets each edge (the fine ladder, 10 bps, convention c670):")
    s = fine[(fine.panel == "U56") & (fine.arm == "CAND20") & (fine.sched == "W")
             & (fine.cost == COST0) & (fine.gross.isin(LADDERS["STEP002"]))].sort_values("gross")
    for leg in ("c670_L1_H1", "c670_L2_H2", "c670_L3_OOS", "c670_L4_DDcap", "c670_L5_CAGRfloor"):
        v = s[leg].values
        P(f"    {leg:20s} passes {int(v.sum()):4d} of {len(v)} rungs" +
          ("  (never binds)" if v.all() else
           f"  first pass g={float(s.gross.values[np.argmax(v)]):.3f}" if v.any() else "  (never passes)"))

    # --------------------------------------------------------------------------------------
    # H_OFFSET
    # --------------------------------------------------------------------------------------
    P("")
    P("=" * 112)
    P("H_OFFSET  IS THE WINDOW WIDER THAN ITS OWN REBALANCE-OFFSET SPREAD?  (idea 806's clause)")
    P("=" * 112)
    P(f"  {'sched':>6s} {'cost':>5s} {'g_min':>8s} {'g_max':>8s} {'width':>8s}   "
      f"(convention c670, FULL window)")
    for cost in COSTS:
        e = EX[(EX.panel == "U56") & (EX.arm == "CAND20") & (EX.conv == "c670")
               & (EX.cost == cost)]
        for _, r in e.iterrows():
            P(f"  {r.sched:>6s} {int(r.cost):5d} "
              f"{('   --   ' if r.g_min is None or not np.isfinite(float(r.g_min or np.nan)) else f'{float(r.g_min):8.4f}')} "
              f"{float(r.g_max):8.4f} "
              + ("  EMPTY " if bool(r["is_empty"]) else f"{float(r.width):8.4f}"))
    off = EX[(EX.panel == "U56") & (EX.arm == "CAND20") & (EX.conv == "c670")
             & (EX.cost == COST0) & (EX.sched != "W")]
    P("")
    if len(off) and off.width.notna().all():
        sp_lo = float(off.g_min.astype(float).max() - off.g_min.astype(float).min())
        sp_hi = float(off.g_max.astype(float).max() - off.g_max.astype(float).min())
        sp_w = float(off.width.max() - off.width.min())
        P(f"  offset spread at 10 bps over the 5 phases: g_min {sp_lo:.4f}, g_max {sp_hi:.4f}, "
          f"width {sp_w:.4f}; window width (W schedule) {rex.width:.4f}")
        P(f"  per-edge reading (idea 806's clause applied EDGE BY EDGE, which is the honest form):")
        P(f"     lower edge (CAGR floor): spread {sp_lo:.4f} = {sp_lo/rex.width:.0%} of the window "
          f"width  -> {'RESOLVED' if sp_lo < 0.5*rex.width else 'NOT RESOLVED by this data'}")
        P(f"     upper edge (DD cap)    : spread {sp_hi:.4f} = {sp_hi/rex.width:.0%} of the window "
          f"width  -> {'RESOLVED' if sp_hi < 0.5*rex.width else 'NOT RESOLVED by this data'}")
        P(f"  H_OFFSET (width > max edge spread) -> "
          f"{'HOLDS' if rex.width > max(sp_lo, sp_hi) else 'FAILS'}"
          f"  (margin {rex.width - max(sp_lo, sp_hi):+.4f}, i.e. "
          f"{(rex.width - max(sp_lo, sp_hi))/rex.width:+.0%} of the width)")
        P(f"  and every offset keeps a non-empty window: {int(off.width.gt(0).sum())} of {len(off)}")
    else:
        P("  at least one offset has an EMPTY window at 10 bps -- reported, and H_OFFSET fails")

    # --------------------------------------------------------------------------------------
    # H_COST
    # --------------------------------------------------------------------------------------
    P("")
    P("=" * 112)
    P("H_COST  THE COST SWEEP  (turnover is the price of the window's lower edge)")
    P("=" * 112)
    tn = float(fine[(fine.panel == "U56") & (fine.arm == "CAND20") & (fine.sched == "W")
                    & (fine.cost == COST0) & (np.abs(fine.gross - PUBLISHED_G) < 1e-9)]
               .turn_yr.iloc[0])
    P(f"  U56/CAND20 turnover at g={PUBLISHED_G}: {tn:.2f}x/yr, so a rung of 10 bps costs "
      f"{tn*10/1e4:.4%} of CAGR per year at that gross")
    P(f"  {'cost':>5s} {'g_min (CAGR floor)':>19s} {'g_max (DD cap)':>15s} {'width':>8s} "
      f"{'0.75 passes':>12s}")
    for cost in COSTS:
        e = EX[(EX.panel == "U56") & (EX.arm == "CAND20") & (EX.sched == "W")
               & (EX.cost == cost) & (EX.conv == "c670")].iloc[0]
        p75 = fine[(fine.panel == "U56") & (fine.arm == "CAND20") & (fine.sched == "W")
                   & (fine.cost == cost) & (np.abs(fine.gross - PUBLISHED_G) < 1e-9)]
        ok75 = bool(p75.c670_pass4b.iloc[0]) if len(p75) else False
        gm = "     EMPTY      " if e.g_min is None else f"{float(e.g_min):19.4f}"
        wtxt = "  EMPTY " if bool(e["is_empty"]) else f"{float(e.width):8.4f}"
        P(f"  {int(cost):5d} {gm:>19s} {float(e.g_max):15.4f} {wtxt:>8s} "
          f"{('y' if ok75 else 'n'):>12s}   "
          f"level width {('   --   ' if not np.isfinite(float(e.level_width)) else f'{float(e.level_width):.4f}')}"
          f", Sharpe legs {'pass' if e.sharpe_ok else 'FAIL'} ({e.sharpe_detail})")
    e25 = EX[(EX.panel == "U56") & (EX.arm == "CAND20") & (EX.sched == "W") & (EX.cost == 25.0)
             & (EX.conv == "c670")].iloc[0]
    P("")
    P(f"  H_COST (bar: non-empty at 25 bps) -> "
      f"{'HOLDS' if not bool(e25['is_empty']) else 'FAILS'}")
    P("  NOTE, stated because the two readings differ and only one is the 4b window: the LEVEL-leg")
    P("  window (the two monotone crossings a bisection sees) is non-empty at 25 bps, but the 4b")
    P("  window is EMPTY there because a gross-FLAT Sharpe leg fails at every gross.  The leg")
    P("  census below names it.  A bisection on the level legs alone would have over-reported.")
    P("")
    P("  leg census over the 750-rung ladder, by cost (convention c670):")
    for cost in COSTS:
        t = fine[(fine.panel == "U56") & (fine.arm == "CAND20") & (fine.sched == "W")
                 & (fine.cost == cost) & (fine.gross.isin(LADDERS["STEP002"]))]
        P(f"    {int(cost):3d} bps  " + "  ".join(
            f"{k[5:]} {int(t['c670_' + k[5:]].sum()):3d}/{len(t)}"
            for k in ("c670_L1_H1", "c670_L2_H2", "c670_L3_OOS", "c670_L4_DDcap",
                      "c670_L5_CAGRfloor"))
          + f"   4b {int(t.c670_pass4b.sum()):3d}/{len(t)}")

    # --------------------------------------------------------------------------------------
    # H_TRAVEL + companions
    # --------------------------------------------------------------------------------------
    P("")
    P("=" * 112)
    P("H_TRAVEL / COMPANIONS  the same measurement on every arm and panel (10 bps, c670, FULL)")
    P("=" * 112)
    P(f"  {'panel':6s} {'arm':14s} {'g_min':>8s} {'g_max':>8s} {'width':>8s} {'0.75':>5s} "
      f"{'rungs passing of 150':>21s}   source")
    for nm in PANELS:
        for a in ARMS:
            e = EX[(EX.panel == nm) & (EX.arm == a) & (EX.sched == "W") & (EX.cost == COST0)
                   & (EX.conv == "c670")]
            if e.empty:
                continue
            e = e.iloc[0]
            t = fine[(fine.panel == nm) & (fine.arm == a) & (fine.sched == "W")
                     & (fine.cost == COST0) & (fine.gross.isin(LADDERS["STEP01"]))]
            npass = int(t.c670_pass4b.sum())
            p75 = t[np.abs(t.gross - PUBLISHED_G) < 1e-9]
            ok75 = bool(p75.c670_pass4b.iloc[0]) if len(p75) else False
            gm = "  EMPTY " if e.g_min is None else f"{float(e.g_min):8.4f}"
            wtxt = "  EMPTY " if bool(e["is_empty"]) else f"{float(e.width):8.4f}"
            P(f"  {nm:6s} {a:14s} {gm:>8s} {float(e.g_max):8.4f} {wtxt:>8s} "
              f"{('y' if ok75 else 'n'):>5s} {npass:>21d}   {ARM_SRC[a]}")

    # --------------------------------------------------------------------------------------
    # H_WF -- rule 8
    # --------------------------------------------------------------------------------------
    P("")
    P("=" * 112)
    P("H_WF / RULE 8  g CHOSEN ON 2009-2016 ONLY, OOS 2017-2026 READ ONCE.  BOTH KEEP PATHS.")
    P("               10 bps primary; every cost rung reported.  Three pre-registered IS-only")
    P("               choosers, none of which can see an OOS number:")
    P("                 IS_MID    the midpoint of the IS LEVEL-leg window (the interior pick)")
    P("                 IS_GMAX   the IS level-leg window's upper edge minus one 0.01 rung")
    P("                 IS_SHARPE the IS-best Sharpe rung inside the IS level-leg window")
    P("=" * 112)
    P("")
    P("  FIRST, THE FACT THAT DECIDES HOW THESE CHOOSERS MUST BE READ.  Under the window-local")
    P("  convention the STRICT IS 4b pass set is EMPTY at every gross and every cost rung, and one")
    P("  leg does it:")
    for cost in COSTS:
        t = fine[(fine.panel == "U56") & (fine.arm == "CAND20") & (fine.sched == "W")
                 & (fine.cost == cost) & (fine.gross.isin(LADDERS["STEP002"]))]
        P(f"    {int(cost):3d} bps  IS window legs: " + "  ".join(
            f"{k} {int(t['cwinIS_' + k].sum()):3d}/{len(t)}"
            for k in ("L1_H1", "L2_H2", "L4_DDcap", "L5_CAGRfloor"))
          + f"   IS 4b {int(t.cwinIS_pass4b.sum()):3d}/{len(t)}")
    P("  So no IS-only chooser can be 'the IS 4b pick': the choosers below select on the IS")
    P("  LEVEL legs (CAGR floor and DD cap, the two that gross moves) and are labelled as such.")
    P("  This is a property of reading halves INSIDE an 8-year window, not of the book: under")
    P("  idea 670's own convention (halves on the FULL window) the same legs pass at every gross.")
    wrows = []
    for cost in COSTS:
        e = EX[(EX.panel == "U56") & (EX.arm == "CAND20") & (EX.sched == "W")
               & (EX.cost == cost) & (EX.conv == "cwin") & (EX.window == "IS")].iloc[0]
        lad = fine[(fine.panel == "U56") & (fine.arm == "CAND20") & (fine.sched == "W")
                   & (fine.cost == cost) & (fine.gross.isin(LADDERS["STEP01"]))]
        picks = {}
        if e.g_min is not None and np.isfinite(float(e.level_width)) and float(e.level_width) > 0:
            lo, hi = float(e.g_min), float(e.g_max)
            picks["IS_MID"] = 0.5 * (lo + hi)
            picks["IS_GMAX"] = hi - 0.01
            inside = lad[(lad.gross >= lo) & (lad.gross <= hi)]
            if len(inside):
                picks["IS_SHARPE"] = float(inside.loc[inside.IS_Sharpe.idxmax()].gross)
        if not picks:
            wrows.append(dict(cost=cost, chooser="(IS level window EMPTY)", g=np.nan))
            continue
        bk = books[("U56", "W", "CAND20")]
        for ch, g in picks.items():
            r = score_g(bk, g, cost, spyref["U56"], v2ref["U56"])
            sp, v2 = spyref["U56"]["OOS"], v2ref["U56"]["OOS"]
            wrows.append(dict(cost=cost, chooser=ch, g=g,
                              IS_window=f"[{float(e.g_min):.3f},{float(e.g_max):.3f}]",
                              IS_level_width=float(e.level_width),
                              OOS_CAGR=r["OOS_CAGR"], OOS_Sharpe=r["OOS_Sharpe"],
                              OOS_MaxDD=r["OOS_MaxDD"], OOS_H1=r["OOS_H1"], OOS_H2=r["OOS_H2"],
                              SPY_CAGR=sp["CAGR"], SPY_Sharpe=sp["Sharpe"], SPY_MaxDD=sp["MaxDD"],
                              V2_CAGR=v2["CAGR"], V2_Sharpe=v2["Sharpe"], V2_MaxDD=v2["MaxDD"],
                              pass4b_oos=r["cwinOOS_pass4b"], pass4a_oos=r["cwinOOS_pass4a"],
                              pass4b_c670=r["c670_pass4b"], pass4a_c670=r["c670_pass4a"],
                              **{f"leg_{k[8:]}": r[k] for k in r if k.startswith("cwinOOS_L")}))
    WF = pd.DataFrame(wrows)
    dump(WF, "walkforward.csv")
    P("")
    P(f"  {'cost':>5s} {'chooser':10s} {'g':>6s} {'IS window':>15s} {'OOS CAGR':>9s} "
      f"{'OOS Shrp':>9s} {'OOS MaxDD':>10s} {'OOS H1/H2':>13s} {'4a':>3s} {'4b':>3s}")
    for _, r in WF.iterrows():
        if not np.isfinite(r.get("g", np.nan)):
            P(f"  {int(r.cost):5d} {r.chooser}")
            continue
        P(f"  {int(r.cost):5d} {r.chooser:10s} {r.g:6.3f} {r.IS_window:>15s} "
          f"{r.OOS_CAGR:9.2%} {r.OOS_Sharpe:9.3f} {r.OOS_MaxDD:10.2%} "
          f"{r.OOS_H1:6.3f}/{r.OOS_H2:6.3f} {'y' if r.pass4a_oos else 'n':>3s} "
          f"{'y' if r.pass4b_oos else 'n':>3s}")
    P("")
    P("  comparands, SAME OOS window:")
    sp, v2 = spyref["U56"]["OOS"], v2ref["U56"]["OOS"]
    P(f"    SPY        {sp['CAGR']:7.2%} / {sp['Sharpe']:.3f} / {sp['MaxDD']:7.2%}  "
      f"(halves {sp['H1']:.3f}/{sp['H2']:.3f})")
    P(f"    RULES v2   {v2['CAGR']:7.2%} / {v2['Sharpe']:.3f} / {v2['MaxDD']:7.2%}  "
      f"(halves {v2['H1']:.3f}/{v2['H2']:.3f})")
    spf, v2f = spyref["U56"]["FULL"], v2ref["U56"]["FULL"]
    P(f"  full-sample comparands: SPY {spf['CAGR']:7.2%} / {spf['Sharpe']:.3f} / "
      f"{spf['MaxDD']:7.2%} (halves {spf['H1']:.3f}/{spf['H2']:.3f});  RULES v2 "
      f"{v2f['CAGR']:7.2%} / {v2f['Sharpe']:.3f} / {v2f['MaxDD']:7.2%} "
      f"(halves {v2f['H1']:.3f}/{v2f['H2']:.3f})")
    P("")
    P("  the IS and OOS windows side by side (convention cwin, 10 bps) -- does the IS window")
    P("  CONTAIN the OOS one?  This is the rule-8 question about the window itself:")
    for cost in COSTS:
        ei = EX[(EX.panel == "U56") & (EX.arm == "CAND20") & (EX.sched == "W")
                & (EX.cost == cost) & (EX.conv == "cwin") & (EX.window == "IS")].iloc[0]
        eo = EX[(EX.panel == "U56") & (EX.arm == "CAND20") & (EX.sched == "W")
                & (EX.cost == cost) & (EX.conv == "cwin") & (EX.window == "OOS")].iloc[0]
        def _w(x):
            if x.g_min is None:
                return "EMPTY"
            t = f"[{float(x.g_min):.3f},{float(x.g_max):.3f}]"
            return t + ("*" if float(x.g_min) > float(x.g_max) else "")
        gi, go = _w(ei), _w(eo)
        ov = ""
        if ei.g_min is not None and eo.g_min is not None:
            lo = max(float(ei.g_min), float(eo.g_min))
            hi = min(float(ei.g_max), float(eo.g_max))
            ov = f"  overlap {max(0.0, hi-lo):.4f}"
            if float(ei.g_min) > float(ei.g_max) or float(eo.g_min) > float(eo.g_max):
                ov += "   (* = inverted, i.e. that level window is EMPTY)"
        P(f"    {int(cost):3d} bps   IS {gi:>17s}   OOS {go:>17s}{ov}")

    # --------------------------------------------------------------------------------------
    # verdict
    # --------------------------------------------------------------------------------------
    P("")
    P("=" * 112)
    P("VERDICT")
    P("=" * 112)
    P(f"  H_LADDER   670's 8 rungs: {int(r8.n_pass)} passing.  0.01 ladder: {int(r01.n_pass)} of "
      f"{int(r01.n_rungs)}.  -> "
      f"{'LADDER ARTEFACT' if r01.n_pass >= 2 else 'not an artefact'}")
    P("  H_KNIFE    " + ("EXACT window at 10 bps is EMPTY" if not np.isfinite(rex.width) else
                             f"EXACT width {rex.width:.4f} of gross ({rex.width/0.05:.1f} rungs "
                             f"of 0.05) -> "
                             f"{'KNIFE EDGE' if rex.width < KNIFE_BAR else 'A REAL WINDOW'}"))
    P(f"  H_INTERIOR published 0.75 clears both edges by {min(lo_ok, hi_ok):.4f} -> "
      f"{'INTERIOR' if min(lo_ok, hi_ok) >= INTERIOR_BAR else 'ON AN EDGE'}")
    def _ex(c):
        return EX[(EX.panel == "U56") & (EX.arm == "CAND20") & (EX.sched == "W")
                  & (EX.cost == c) & (EX.conv == "c670")].iloc[0]
    P("  H_COST     4b window at 0/10/25/50 bps: " + "  ".join(
        f"{int(c)}bps " + ("EMPTY" if bool(_ex(c)["is_empty"]) else f"{float(_ex(c).width):.4f}")
        for c in COSTS))
    P("             level-leg window only:        " + "  ".join(
        f"{int(c)}bps " + (f"{float(_ex(c).level_width):.4f}"
                           if np.isfinite(float(_ex(c).level_width)) else "EMPTY")
        + (" (Sharpe leg FAILS)" if not bool(_ex(c).sharpe_ok) else "") for c in COSTS))
    P(f"  H_WF       rule 8: 4a {int(WF.get('pass4a_oos', pd.Series(dtype=bool)).sum())} / "
      f"4b {int(WF.get('pass4b_oos', pd.Series(dtype=bool)).sum())} of "
      f"{int(WF.g.notna().sum())} (chooser x cost) picks")
    trv = EX[(EX.arm == "CAND20") & (EX.sched == "W") & (EX.cost == COST0) & (EX.conv == "c670")]
    P("  H_TRAVEL   " + "  ".join(
        f"{r.panel} " + ("EMPTY" if bool(r["is_empty"]) else f"{float(r.width):.4f}")
        for _, r in trv.iterrows()))
    P("")
    P("SURVIVORSHIP: U56 / B136 / SMALL are current-constituent lists (SMALL additionally drops "
      f"the {len(bad)} tickers with")
    P("  max_1d_move >= 1.0 per data/small_meta.csv), so every CAGR and drawdown LEVEL above is "
      "optimistic.")
    P("  A 4b bar is the book's level against SPY's, and SPY is NOT survivorship-inflated, so the "
      "bars are")
    P("  not protected by the usual same-tape argument: the widths above are UPPER BOUNDS on what "
      "a")
    P("  survivorship-free panel would show.  The offset spread and the cost sweep are same-book "
      "contrasts")
    P("  and are unaffected.")
    P("")
    P(f"elapsed {time.time()-t0:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"wrote {STEM}.console.txt")


if __name__ == "__main__":
    main()

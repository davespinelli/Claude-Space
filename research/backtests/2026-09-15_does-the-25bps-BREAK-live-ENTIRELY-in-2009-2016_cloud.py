#!/usr/bin/env python3
"""Idea 918 (cloud, 2026-09-15) -- does the 25 bps BREAK of the FULL-WINDOW 4b READING live
ENTIRELY in 2009-2016?

THE QUESTION (queue, 2026-09-15)
  Idea 675 found the standing TOP20 book's 4b gross window EMPTY at 25 bps -- and not by a
  squeeze: the two monotone LEVEL legs still bracket 0.0979 of gross there, while `L1_H1` (the
  2009-2016 half Sharpe against SPY's) fails at 0 of 750 grosses, a gross-FLAT leg.  At the same
  cost the OOS-ONLY reading of the same book is still [0.6440, 0.8274] wide.  The queue asks:
  census every committed cost-rung KILL in the record for which HALF carries the failure.

WHAT IS CENSUSED (a PRICE census, not a prose census)
  A "cost-rung KILL" is a committed grid CELL -- (panel, arm, gross) -- that clears PROTOCOL 4b at
  the record's own primary rung (10 bps) and fails it at a higher rung.  Each KILL is attributed to
  the leg(s) that FLIP between the two rungs:
        L1_H1        first half of the FULL window   (2009 -> the sample midpoint)   <- "2009-2016"
        L2_H2        second half of the FULL window
        L3_OOS       the separate OOS Sharpe leg (2017-2026)
        L4_DDcap     level leg, MaxDD <= 60% of SPY's       (FULL window)
        L5_CAGRfloor level leg, CAGR  >= 70% of SPY's       (FULL window)
  Every cell is re-scored here from prices; nothing is read out of committed prose.

  Beside the flip census the run publishes, for every cell in the 10 bps pass set, each leg's OWN
  CLOSING PRICE -- the cost rung at which that leg stops passing -- so "which half carries it" is a
  number in basis points, not a category.  (This is the per-leg form idea 921 asks the record for;
  921 stays open, this run supplies the per-leg closing prices for the cells it censuses.)

WHAT IS TUNED AND WHAT IS REPORTED (PROTOCOL 4: max 2 tuned parameters)
  TUNED 1  CLAIM SET (the queue's own first dial), 3 levels, every one reported:
           RECORD8  670's own 8 irregular gross rungs x 8 arms, U56            (the claim's ladder)
           CORE30   0.05..1.50 step 0.05 (30 rungs) x 8 arms, U56
           WIDE     the same 30 rungs x 8 arms x 3 panels (U56, B136, SMALL)
  TUNED 2  COST RUNG (the queue's own second dial): the KILL rung c in {25, 50} bps against the
           10 bps reference, with the 0 -> 10 rung reported beside it as a control.
  REPORTED AXES (nothing fitted on them; every point published): window FULL / IS / OOS; the two
           4b conventions (c670 = FULL halves + a separate OOS leg, the convention 670's claim
           lives in; cwin = the window-local form 867/910 use); a 41-rung cost ladder 0..100 bps
           step 2.5 on the pass set; per-half turnover and per-half cost slope.

PRE-REGISTERED BARS (fixed before any number is read; both directions reported)
  H_ENTIRELY  the 25 bps break "lives entirely in 2009-2016" iff, across the census, EVERY
              cost-rung KILL at 25 bps flips L1_H1 (i.e. the H1 leg is present in every flip set).
  H_MOSTLY    the weaker reading: >= 0.80 of 25 bps KILLs flip L1_H1.  Both are scored.
  H_OOSLIVES  the OOS-only (cwinOOS) reading of the same cells survives the same rung in >= 0.80
              of the cells whose FULL reading dies -- the queue's "OOS window is still wide" claim
              generalised past the one book.
  H_SLOPE     the mechanism is TURNOVER: the H1 leg carries the break because H1 turnover exceeds
              H2 turnover.  Falsified if the per-half cost slopes are within 10% while the break
              is still H1's -- in which case the carrier is the MARGIN, not the slope.
  H_WF        (rule 8, required) gross chosen on 2009-2016 ONLY by three IS-only choosers, OOS
              2017-2026 read once, both KEEP paths, against SPY and RULES v2 in the same window.

GATES (all printed before any result number)
  G1  the fast runner == engine.backtest on returns and turnover (BAND03 and the subject)
  G2  BAND03 at g=0.75 == baseline.rules_v2_weights elementwise
  G3  the COST-LINEARITY identity this run's whole cost ladder rests on:
      r(c) == r(0) - turnover * c/1e4 elementwise, against a fresh engine.backtest at c
  G4  idea 675's committed headline reproduces: U56/CAND20 c670 window [0.6241, 0.8337] at 10 bps
      and L1_H1 failing at 0 of 150 grosses at 25 bps
  G5  the committed U56 triples (SPY, RULES v2)
  G6  cost monotonicity: CAGR and Sharpe non-increasing in cost on every census cell
  G7  determinism (rebuild the census, compare)

PROTOCOL: 10 bps primary, t+1, weekly, warm-up 260 days, IS 2009-2016 / OOS 2017-2026.
Nothing in RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py is modified.

SURVIVORSHIP: U56 / B136 / SMALL are current-constituent lists, so every CAGR and drawdown LEVEL
below is optimistic -- the book's and the comparands' alike.  A 4b bar is a RATIO of the book's
level to SPY's and SPY is not survivorship-inflated, so the bars are NOT protected by the
same-tape argument; a closing price measured here is an UPPER bound on the closing price a
survivorship-free panel would show.  SMALL additionally drops every ticker with max_1d_move >= 1.0
per data/small_meta.csv.  Stated, not hidden.
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
COST0 = 10.0                       # PROTOCOL 2, the primary rung and the census reference
FREQ = "W"
LAG = 1
BAND0 = 0.03
MAXVOL = 0.60
WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70    # PROTOCOL 4b
PUBLISHED_G = 0.75
BISECT_TOL = 1e-6
GMIN_SEARCH, GMAX_SEARCH = 0.002, 2.0

# ---- TUNED DIAL 1: the claim set --------------------------------------------------------------
RECORD8 = [0.20, 0.35, 0.50, 0.60, 0.75, 0.85, 0.95, 1.00]     # idea 670's own ladder
STEP05 = [round(0.05 * i, 4) for i in range(1, 31)]
STEP01 = [round(0.01 * i, 4) for i in range(1, 151)]           # only for the G4 reproduction
CLAIMSETS = {
    "RECORD8": dict(panels=["U56"], grosses=RECORD8),
    "CORE30": dict(panels=["U56"], grosses=STEP05),
    "WIDE": dict(panels=["U56", "B136", "SMALL"], grosses=STEP05),
}
CLAIMSET_ORDER = ["RECORD8", "CORE30", "WIDE"]

# ---- TUNED DIAL 2: the cost rung --------------------------------------------------------------
KILL_RUNGS = [25.0, 50.0]          # the queue's own rung is 25; 50 reported beside it
CONTROL_RUNG = (0.0, 10.0)         # the 0 -> 10 rung, reported as a control
COST_LADDER = [round(2.5 * i, 4) for i in range(0, 41)]        # 0 .. 100 bps, per-leg closing price

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
WINDOWS = ["FULL", "IS", "OOS"]
LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DDcap", "L5_CAGRfloor"]

SPY_U56 = (0.1516, 0.8861, -0.3372)
V2_U56 = (0.0863, 1.2018, -0.1205)
TOL_C, TOL_S, TOL_D = 0.004, 0.030, 0.015
G675_WINDOW = (0.6241, 0.8337)     # idea 675's committed c670 FULL window at 10 bps, U56/CAND20
G675_BAR = 5e-3                    # vintage bar: 675's tape ends 2026-09-15, same day, so tight

# pre-registered bar levels
ENTIRELY_BAR = 1.00
MOSTLY_BAR = 0.80
OOSLIVES_BAR = 0.80
SLOPE_BAR = 0.10

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
# runner (the vectorised equivalent of engine.backtest used by ideas 910 / 675, unchanged)
# ================================================================================================
class Panel:
    def __init__(self, name, px):
        self.name, self.px = name, px
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        T, N = self.rets.shape
        self.T, self.N = T, N
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, N)), C[:-1]])
        mk = rebalance_mask(self.idx, FREQ).shift(LAG, fill_value=False).values.copy()
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
        # the two HALVES of the FULL window, as _row()/pack() cut them (by row count)
        nf = int(m_full.sum())
        pos = np.flatnonzero(m_full)
        self.half_lo = pos[: nf // 2]
        self.half_hi = pos[nf // 2:]
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

    def raw(self, g: float):
        """(gross-of-cost returns, turnover) at this gross.  r(cost) = r0 - turn*cost/1e4 EXACTLY
        (gated at G3), which is what makes a 41-rung cost ladder affordable on the whole census."""
        pan = self.pan
        V = 1.0 + g * (self.S - self.As)
        gross = g * self.ARr / V
        Vp = 1.0 + g * (self.Sp - self.Asp)
        heldp = (g * self.ARp) / Vp[:, None]
        heldp[0] = 0.0
        turn = np.zeros(pan.T)
        turn[pan.reb] = np.abs(g * self.wt_reb - heldp).sum(axis=1)
        return gross, turn

    def at(self, g: float, cost=COST0):
        r0, turn = self.raw(g)
        return r0 - turn * cost / 1e4, turn


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
# the two 4b conventions (both reported), identical to idea 675's
# ================================================================================================
def legs670(full, oos, spy_full, spy_oos):
    return dict(L1_H1=bool(full["H1"] > spy_full["H1"]),
                L2_H2=bool(full["H2"] > spy_full["H2"]),
                L3_OOS=bool(oos["Sharpe"] > spy_oos["Sharpe"]),
                L4_DDcap=bool(abs(full["MaxDD"]) <= DD_CAP * abs(spy_full["MaxDD"])),
                L5_CAGRfloor=bool(full["CAGR"] >= CAGR_FLOOR * spy_full["CAGR"]))


def margins670(full, oos, spy_full, spy_oos):
    """The same five legs as SIGNED MARGINS (>0 == passing).  Their zero crossing in cost is the
    leg's closing price."""
    return dict(L1_H1=full["H1"] - spy_full["H1"],
                L2_H2=full["H2"] - spy_full["H2"],
                L3_OOS=oos["Sharpe"] - spy_oos["Sharpe"],
                L4_DDcap=DD_CAP * abs(spy_full["MaxDD"]) - abs(full["MaxDD"]),
                L5_CAGRfloor=full["CAGR"] - CAGR_FLOOR * spy_full["CAGR"])


def legswin(s, spy):
    return dict(L1_H1=bool(s["H1"] > spy["H1"]), L2_H2=bool(s["H2"] > spy["H2"]),
                L3_OOS=True,
                L4_DDcap=bool(s["MaxDD"] >= DD_CAP * spy["MaxDD"]),
                L5_CAGRfloor=bool(s["CAGR"] >= CAGR_FLOOR * spy["CAGR"]))


def pass4a(s, base):
    return bool(s["H1"] > base["H1"] and s["H2"] > base["H2"] and s["MaxDD"] >= base["MaxDD"])


# ================================================================================================
# the arms (idea 670's / 675's definitions, unchanged)
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
# scoring one cell at one cost, from the pre-computed (r0, turn)
# ================================================================================================
def score_cost(pan, r0, turn, cost, spyref, v2ref):
    r = r0 - turn * cost / 1e4
    st = {w: pack(r[pan.masks[w]]) for w in WINDOWS}
    L = legs670(st["FULL"], st["OOS"], spyref["FULL"], spyref["OOS"])
    M = margins670(st["FULL"], st["OOS"], spyref["FULL"], spyref["OOS"])
    row = dict(cost=cost)
    for w in WINDOWS:
        for k, v in st[w].items():
            row[f"{w}_{k}"] = v
    row.update({f"c670_{k}": v for k, v in L.items()})
    row.update({f"m670_{k}": v for k, v in M.items()})
    row["c670_pass4b"] = bool(all(L.values()))
    row["c670_pass4a"] = pass4a(st["FULL"], v2ref["FULL"])
    for w in ("IS", "OOS"):
        Lw = legswin(st[w], spyref[w])
        row.update({f"cwin{w}_{k}": v for k, v in Lw.items()})
        row[f"cwin{w}_pass4b"] = bool(all(Lw.values()))
        row[f"cwin{w}_pass4a"] = pass4a(st[w], v2ref[w])
    return row


def bisect_up(f, lo, hi, tol=BISECT_TOL):
    """Smallest x in [lo,hi] with f(x) >= 0, f non-decreasing.  None if no crossing."""
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


def exact_window(bk, cost, spyref, conv="c670", win="FULL"):
    """(g_min from the CAGR floor, g_max from the DD cap) by bisection -- 675's machinery."""
    wc = wd = "FULL" if conv == "c670" else win
    ref = spyref[wc]

    def f_cagr(g):
        r, _ = bk.at(g, cost)
        c, _, _ = fmet(r[bk.pan.masks[wc]])
        return c - CAGR_FLOOR * ref["CAGR"]

    def f_dd(g):
        r, _ = bk.at(g, cost)
        _, _, d = fmet(r[bk.pan.masks[wd]])
        return abs(d) - DD_CAP * abs(spyref[wd]["MaxDD"])       # non-decreasing in g

    gmin = bisect_up(f_cagr, GMIN_SEARCH, GMAX_SEARCH)
    gmax = bisect_up(f_dd, GMIN_SEARCH, GMAX_SEARCH)
    gmax = GMAX_SEARCH if gmax is None else gmax - BISECT_TOL
    return gmin, gmax


# ================================================================================================
# gates
# ================================================================================================
def run_gates(pans, books, spyref, v2ref, pre, raw):
    P("=" * 112)
    P("GATES (printed before any result number is read)")
    P("=" * 112)
    ok = {}
    pan = pans["U56"]
    px = pan.px

    W1 = arm_w1(px, pre["U56"], "BAND03")
    w_ref = rules_v2_weights(px, band=BAND0, gross=0.75).values
    dw = float(np.nanmax(np.abs(W1 * 0.75 - w_ref)))
    ok["G2"] = dw < 1e-12
    P(f"G2  BAND03 g=0.75 == rules_v2_weights          max|dw| {dw:.3e}   -> "
      f"{'PASS' if ok['G2'] else 'FAIL'}")

    bk = books[("U56", "BAND03")]
    r_fast, t_fast = bk.at(0.75, COST0)
    res = backtest(px, rules_v2_weights(px, band=BAND0, gross=0.75), cost_bps=COST0, freq=FREQ)
    dr = float(np.nanmax(np.abs(r_fast - res["returns"].values)))
    dt = float(np.nanmax(np.abs(t_fast - res["turnover"].values)))
    bs = books[("U56", "CAND20")]
    rs, ts = bs.at(0.75, COST0)
    wsub = pd.DataFrame(arm_w1(px, pre["U56"], "CAND20") * 0.75, index=px.index, columns=px.columns)
    res2 = backtest(px, wsub, cost_bps=COST0, freq=FREQ)
    dr2 = float(np.nanmax(np.abs(rs - res2["returns"].values)))
    dt2 = float(np.nanmax(np.abs(ts - res2["turnover"].values)))
    ok["G1"] = max(dr, dt, dr2, dt2) < 1e-10
    P(f"G1  fast Book.at == engine.backtest            BAND03 |dr| {dr:.3e} |dturn| {dt:.3e}; "
      f"CAND20 |dr| {dr2:.3e} |dturn| {dt2:.3e}   -> {'PASS' if ok['G1'] else 'FAIL'}")

    # G3 -- the cost-linearity identity the whole ladder rests on, against a fresh engine run
    r0, turn = bs.raw(0.75)
    worst = 0.0
    for c in (25.0, 50.0, 100.0):
        eng = backtest(px, wsub, cost_bps=c, freq=FREQ)["returns"].values
        worst = max(worst, float(np.nanmax(np.abs((r0 - turn * c / 1e4) - eng))))
    ok["G3"] = worst < 1e-12
    P(f"G3  r(c) == r(0) - turn*c/1e4 vs engine        max|d| over c in 25/50/100 bps "
      f"{worst:.3e}   -> {'PASS' if ok['G3'] else 'FAIL'}")

    # G4 -- idea 675's committed headline
    gmin, gmax = exact_window(bs, COST0, spyref["U56"])
    d_lo, d_hi = abs(gmin - G675_WINDOW[0]), abs(gmax - G675_WINDOW[1])
    n_h1_fail = 0
    for g in STEP01:
        r, t = bs.raw(g)
        rc = r - t * 25.0 / 1e4
        st = pack(rc[pan.masks["FULL"]])
        if not (st["H1"] > spyref["U56"]["FULL"]["H1"]):
            n_h1_fail += 1
    ok["G4"] = (d_lo < G675_BAR and d_hi < G675_BAR and n_h1_fail == len(STEP01))
    P(f"G4  675's committed headline                   window [{gmin:.4f}, {gmax:.4f}] vs "
      f"[{G675_WINDOW[0]}, {G675_WINDOW[1]}] (|d| {d_lo:.2e}/{d_hi:.2e}); L1_H1 fails at "
      f"{n_h1_fail} of {len(STEP01)} grosses at 25 bps   -> {'PASS' if ok['G4'] else 'FAIL'}")

    s = spyref["U56"]["FULL"]
    v = v2ref["U56"]["FULL"]
    d1 = (abs(s["CAGR"] - SPY_U56[0]), abs(s["Sharpe"] - SPY_U56[1]), abs(s["MaxDD"] - SPY_U56[2]))
    d2 = (abs(v["CAGR"] - V2_U56[0]), abs(v["Sharpe"] - V2_U56[1]), abs(v["MaxDD"] - V2_U56[2]))
    ok["G5"] = all(a < b for a, b in zip(d1, (TOL_C, TOL_S, TOL_D))) and \
        all(a < b for a, b in zip(d2, (TOL_C, TOL_S, TOL_D)))
    P(f"G5  committed U56 triples                      SPY {s['CAGR']:.4%}/{s['Sharpe']:.4f}/"
      f"{s['MaxDD']:.4%}  v2 {v['CAGR']:.4%}/{v['Sharpe']:.4f}/{v['MaxDD']:.4%}   -> "
      f"{'PASS' if ok['G5'] else 'FAIL'}")
    return ok


# ================================================================================================
# the census
# ================================================================================================
def build_census(pans, books, spyref, v2ref):
    """Every (panel, arm, gross) cell on the WIDE ladder at every cost rung on the ladder."""
    rows = []
    for pn in PANELS:
        pan = pans[pn]
        for arm in ARMS:
            bk = books[(pn, arm)]
            for g in STEP05:
                r0, turn = bk.raw(g)
                tf = turn[pan.masks["FULL"]]
                yrs = pan.masks["FULL"].sum() / 252.0
                t_lo = float(turn[pan.half_lo].sum() / (len(pan.half_lo) / 252.0))
                t_hi = float(turn[pan.half_hi].sum() / (len(pan.half_hi) / 252.0))
                for c in COST_LADDER:
                    row = score_cost(pan, r0, turn, c, spyref[pn], v2ref[pn])
                    row.update(panel=pn, arm=arm, gross=g, turn_yr=float(tf.sum() / yrs),
                               turn_H1=t_lo, turn_H2=t_hi)
                    rows.append(row)
    return pd.DataFrame(rows)


def cellkey(df):
    return list(zip(df.panel, df.arm, df.gross))


def flip_census(C, ref_cost, kill_cost, claimset):
    """Every cell that passes 4b (c670) at ref_cost and fails at kill_cost, with the flip set."""
    spec = CLAIMSETS[claimset]
    sub = C[C.panel.isin(spec["panels"]) & C.gross.isin(spec["grosses"])]
    a = sub[sub.cost == ref_cost].set_index(["panel", "arm", "gross"])
    b = sub[sub.cost == kill_cost].set_index(["panel", "arm", "gross"])
    common = a.index.intersection(b.index)
    a, b = a.loc[common], b.loc[common]
    passers = a.index[a.c670_pass4b.values]
    rows = []
    for key in passers:
        ra, rb = a.loc[key], b.loc[key]
        flipped = [L for L in LEGS if bool(ra[f"c670_{L}"]) and not bool(rb[f"c670_{L}"])]
        rows.append(dict(claimset=claimset, ref_cost=ref_cost, kill_cost=kill_cost,
                         panel=key[0], arm=key[1], gross=key[2],
                         killed=not bool(rb.c670_pass4b),
                         flip="+".join(flipped) if flipped else "NONE",
                         n_flip=len(flipped),
                         H1_in_flip=("L1_H1" in flipped),
                         oos_ref=bool(ra.cwinOOS_pass4b), oos_kill=bool(rb.cwinOOS_pass4b),
                         is_ref=bool(ra.cwinIS_pass4b), is_kill=bool(rb.cwinIS_pass4b),
                         **{f"m_{L}_ref": float(ra[f"m670_{L}"]) for L in LEGS},
                         **{f"m_{L}_kill": float(rb[f"m670_{L}"]) for L in LEGS},
                         turn_yr=float(ra.turn_yr), turn_H1=float(ra.turn_H1),
                         turn_H2=float(ra.turn_H2)))
    return pd.DataFrame(rows)


def closing_prices(C, passers):
    """For every cell in the 10 bps pass set, each leg's OWN closing price: the first rung of the
    41-rung ladder at which that leg stops passing (NaN = still passing at 100 bps)."""
    rows = []
    idx = C.set_index(["panel", "arm", "gross", "cost"]).sort_index()
    for (pn, arm, g) in passers:
        rec = dict(panel=pn, arm=arm, gross=g)
        for L in LEGS:
            close = np.nan
            for c in COST_LADDER:
                if not bool(idx.loc[(pn, arm, g, c), f"c670_{L}"]):
                    close = c
                    break
            rec[f"close_{L}"] = close
        alive = [L for L in LEGS if not np.isfinite(rec[f"close_{L}"])]
        finite = {L: rec[f"close_{L}"] for L in LEGS if np.isfinite(rec[f"close_{L}"])}
        rec["close_4b"] = min(finite.values()) if finite else np.nan
        rec["first_leg"] = min(finite, key=finite.get) if finite else "NONE<=100bps"
        rec["n_alive_100bps"] = len(alive)
        rows.append(rec)
    return pd.DataFrame(rows)


# ================================================================================================
# rule 8
# ================================================================================================
def rule8(pans, books, spyref, v2ref):
    """Three IS-ONLY choosers of gross, evaluated once on 2017-2026.  No OOS number touches the
    choice.  Reported at every cost rung in {0, 10, 25, 50}."""
    rows = []
    for pn in PANELS:
        pan = pans[pn]
        bk = books[(pn, "CAND20")]
        for cost in [0.0, COST0] + KILL_RUNGS:
            # IS-window level window (bisected on the IS mask alone)
            gi_lo, gi_hi = exact_window(bk, cost, spyref[pn], conv="cwin", win="IS")
            picks = {}
            if gi_lo is not None and gi_hi > gi_lo:
                picks["PICK_ISMID"] = 0.5 * (gi_lo + gi_hi)
                picks["PICK_ISLO"] = gi_lo + 0.02
            # IS max-Sharpe over the 30-rung ladder, subject to the IS 4b legs
            best, bestg = -np.inf, None
            for g in STEP05:
                r, t = bk.raw(g)
                rc = r - t * cost / 1e4
                st = pack(rc[pan.masks["IS"]])
                Lw = legswin(st, spyref[pn]["IS"])
                if all(Lw.values()) and np.isfinite(st["Sharpe"]) and st["Sharpe"] > best:
                    best, bestg = st["Sharpe"], g
            if bestg is not None:
                picks["PICK_ISMAXS"] = bestg
            picks["PICK_LIVE"] = PUBLISHED_G          # zero-parameter control (fits nothing)
            for nm, g in picks.items():
                r, t = bk.raw(g)
                rc = r - t * cost / 1e4
                oos = pack(rc[pan.masks["OOS"]])
                full = pack(rc[pan.masks["FULL"]])
                Lo = legswin(oos, spyref[pn]["OOS"])
                rows.append(dict(panel=pn, cost=cost, chooser=nm, gross=g,
                                 IS_win_lo=gi_lo, IS_win_hi=gi_hi,
                                 OOS_CAGR=oos["CAGR"], OOS_Sharpe=oos["Sharpe"],
                                 OOS_MaxDD=oos["MaxDD"], OOS_H1=oos["H1"], OOS_H2=oos["H2"],
                                 FULL_CAGR=full["CAGR"], FULL_Sharpe=full["Sharpe"],
                                 FULL_MaxDD=full["MaxDD"],
                                 **{f"OOS_{k}": v for k, v in Lo.items()},
                                 OOS_pass4b=bool(all(Lo.values())),
                                 OOS_pass4a=pass4a(oos, v2ref[pn]["OOS"]),
                                 SPY_OOS_CAGR=spyref[pn]["OOS"]["CAGR"],
                                 SPY_OOS_Sharpe=spyref[pn]["OOS"]["Sharpe"],
                                 SPY_OOS_MaxDD=spyref[pn]["OOS"]["MaxDD"],
                                 V2_OOS_CAGR=v2ref[pn]["OOS"]["CAGR"],
                                 V2_OOS_Sharpe=v2ref[pn]["OOS"]["Sharpe"],
                                 V2_OOS_MaxDD=v2ref[pn]["OOS"]["MaxDD"]))
    return pd.DataFrame(rows)


# ================================================================================================
def main():
    t0 = time.time()
    P("=" * 112)
    P("IDEA 918 (cloud, 2026-09-15) -- does the 25 bps BREAK of the FULL-WINDOW 4b READING live")
    P("                               ENTIRELY in 2009-2016?")
    P("=" * 112)
    P(f"TUNED 1 claim set (3 levels, all reported): {CLAIMSET_ORDER}")
    P(f"        RECORD8 = 670's own ladder {RECORD8} (U56)")
    P(f"        CORE30  = {len(STEP05)} rungs 0.05..1.50 (U56);  WIDE = the same x {PANELS}")
    P(f"TUNED 2 kill rung: {[int(c) for c in KILL_RUNGS]} bps against the {int(COST0)} bps "
      f"reference; control rung {int(CONTROL_RUNG[0])} -> {int(CONTROL_RUNG[1])}")
    P(f"reported: windows {WINDOWS}; conventions c670 / cwin; cost ladder "
      f"{COST_LADDER[0]}..{COST_LADDER[-1]} bps step 2.5 ({len(COST_LADDER)} rungs); "
      f"{len(ARMS)} arms")
    P(f"SUBJECT: {SUBJECT[0]}/{SUBJECT[1]} -- {ARM_SRC['CAND20']}")
    P(f"BARS: H_ENTIRELY every 25 bps KILL flips L1_H1; H_MOSTLY >= {MOSTLY_BAR:.0%}; "
      f"H_OOSLIVES >= {OOSLIVES_BAR:.0%} of dead cells keep the OOS-only reading;")
    P(f"      H_SLOPE per-half cost slopes differ by > {SLOPE_BAR:.0%} (turnover mechanism); "
      f"H_WF rule 8, three IS-only choosers, both KEEP paths.")
    P("")

    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    rawpx = {}
    for nm, kw in [("U56", {}), ("B136", dict(broad=True)), ("SMALL", dict(small=True))]:
        px = load_universe(**kw)
        if nm == "SMALL":
            px = px[[c for c in px.columns if c not in bad]]
        rawpx[nm] = px
        P(f"panel {nm:6s} {px.shape[0]} days x {px.shape[1]} cols  {px.index[0].date()} .. "
          f"{px.index[-1].date()}")
    P(f"  SMALL drops {len(bad)} tickers with max_1d_move >= 1.0 (data/small_meta.csv)")
    P("")

    pans, pre = {}, {}
    for nm in PANELS:
        pre[nm] = prep(rawpx[nm])
        pans[nm] = Panel(nm, rawpx[nm])
    spyref, v2ref = {}, {}
    for nm in PANELS:
        pan = pans[nm]
        spyref[nm] = {w: pack(pan.spy[pan.masks[w]]) for w in WINDOWS}
        v2 = Book(pan, arm_w1(rawpx[nm], pre[nm], "BAND03")).at(0.75, COST0)[0]
        v2ref[nm] = {w: pack(v2[pan.masks[w]]) for w in WINDOWS}
    books = {}
    for nm in PANELS:
        for a in ARMS:
            books[(nm, a)] = Book(pans[nm], arm_w1(rawpx[nm], pre[nm], a))
    P(f"built {len(books)} (panel, arm) books")
    P("")

    gates = run_gates(pans, books, spyref, v2ref, pre, rawpx)

    P("")
    P("=" * 112)
    P(f"(A) THE CENSUS GRID -- {len(PANELS)} panels x {len(ARMS)} arms x {len(STEP05)} grosses x "
      f"{len(COST_LADDER)} cost rungs")
    P("=" * 112)
    C = build_census(pans, books, spyref, v2ref)
    P(f"  {len(C):,} scored cells")
    # G6 cost monotonicity
    mono_bad = 0
    for _, gdf in C.groupby(["panel", "arm", "gross"]):
        z = gdf.sort_values("cost")
        if (np.diff(z.FULL_CAGR.values) > 1e-12).any() or (np.diff(z.FULL_Sharpe.values) > 1e-9).any():
            mono_bad += 1
    gates["G6"] = mono_bad == 0
    P(f"G6  cost monotonicity (CAGR and Sharpe non-increasing in cost): {mono_bad} violating "
      f"cells of {C.groupby(['panel','arm','gross']).ngroups}   -> "
      f"{'PASS' if gates['G6'] else 'FAIL'}")
    dump(C[C.cost.isin([0.0, 10.0, 25.0, 50.0])], "census.csv")

    P("")
    P("=" * 112)
    P("(B) THE FLIP CENSUS -- which LEG (hence which HALF) carries every cost-rung KILL")
    P("=" * 112)
    FL = []
    for cs in CLAIMSET_ORDER:
        for kc in KILL_RUNGS:
            FL.append(flip_census(C, COST0, kc, cs))
        FL.append(flip_census(C, CONTROL_RUNG[0], CONTROL_RUNG[1], cs))
    F = pd.concat(FL, ignore_index=True)
    dump(F, "flips.csv")
    P("")
    P("  claimset  ref->kill   passers  KILLED  | flip sets (count)")
    P("  " + "-" * 104)
    for cs in CLAIMSET_ORDER:
        for (rc, kc) in [(COST0, k) for k in KILL_RUNGS] + [CONTROL_RUNG]:
            z = F[(F.claimset == cs) & (F.ref_cost == rc) & (F.kill_cost == kc)]
            if not len(z):
                P(f"  {cs:9s} {int(rc):3d}->{int(kc):3d} bps   (no 4b passers at the reference "
                  f"rung)")
                continue
            k = z[z.killed]
            vc = k.flip.value_counts()
            sets = ", ".join(f"{a}={b}" for a, b in vc.items()) if len(vc) else "(none killed)"
            P(f"  {cs:9s} {int(rc):3d}->{int(kc):3d} bps   {len(z):7d}  {len(k):6d}  | {sets}")
    P("")
    P("  H_ENTIRELY / H_MOSTLY -- share of KILLS whose flip set contains L1_H1:")
    hdr_rows = []
    for cs in CLAIMSET_ORDER:
        for kc in KILL_RUNGS:
            k = F[(F.claimset == cs) & (F.ref_cost == COST0) & (F.kill_cost == kc) & F.killed]
            if not len(k):
                P(f"    {cs:9s} {int(kc)} bps: no KILLS (nothing to attribute)")
                continue
            share = float(k.H1_in_flip.mean())
            only = float((k.flip == "L1_H1").mean())
            oos_lives = float(k.oos_kill.mean())
            P(f"    {cs:9s} {int(kc):3d} bps: {len(k):4d} kills | H1 in flip {share:.4f} "
              f"| H1 ALONE {only:.4f} | OOS-only reading still passes {oos_lives:.4f} "
              f"| H_ENTIRELY {'PASS' if share >= ENTIRELY_BAR else 'FAIL'} "
              f"| H_MOSTLY {'PASS' if share >= MOSTLY_BAR else 'FAIL'} "
              f"| H_OOSLIVES {'PASS' if oos_lives >= OOSLIVES_BAR else 'FAIL'}")
            hdr_rows.append(dict(claimset=cs, kill_cost=kc, n=len(k), h1_share=share,
                                 h1_alone=only, oos_lives=oos_lives))
    dump(pd.DataFrame(hdr_rows), "bars.csv")

    P("")
    P("=" * 112)
    P("(C) PER-LEG CLOSING PRICES on the 10 bps pass set (which leg closes FIRST, in bps)")
    P("=" * 112)
    ten = C[(C.cost == COST0) & C.c670_pass4b]
    passers = cellkey(ten)
    P(f"  10 bps 4b pass set: {len(passers)} cells "
      f"({', '.join(f'{p}={n}' for p, n in ten.panel.value_counts().items())})")
    CP = closing_prices(C, passers)
    if len(CP):
        dump(CP, "closing.csv")
        P("")
        P("  first leg to close, over the whole pass set:")
        for a, b in CP.first_leg.value_counts().items():
            P(f"    {a:16s} {b:5d}  ({b / len(CP):.4f})")
        P("")
        P("  per-leg closing price (bps), median over the pass set (NaN = alive at 100 bps):")
        for L in LEGS:
            v = CP[f"close_{L}"]
            P(f"    {L:14s} median {v.median():7.2f}  min {v.min():7.2f}  max {v.max():7.2f}  "
              f"alive-at-100bps {int(v.isna().sum()):4d} of {len(v)}")
        P(f"  4b closing price: median {CP.close_4b.median():.2f} bps, "
          f"min {CP.close_4b.min():.2f}, max {CP.close_4b.max():.2f}")
        P("")
        P("  the SUBJECT (U56/CAND20), every gross in its 10 bps pass set:")
        z = CP[(CP.panel == "U56") & (CP.arm == "CAND20")].sort_values("gross")
        for _, r in z.iterrows():
            P(f"    g={r.gross:.2f}  first={r.first_leg:14s} 4b closes {r.close_4b:6.2f} bps  | "
              + "  ".join(f"{L.split('_')[0]}={r[f'close_{L}']:6.2f}" for L in LEGS))

    P("")
    P("=" * 112)
    P("(D) THE MECHANISM -- is the H1 carry a TURNOVER fact or a MARGIN fact? (H_SLOPE)")
    P("=" * 112)
    # per-half cost slope: d(Sharpe_half)/d(cost) measured on the ladder, per cell
    mech = []
    for (pn, arm, g), z in C.groupby(["panel", "arm", "gross"]):
        z = z.sort_values("cost")
        c = z.cost.values
        s1 = z.FULL_H1.values
        s2 = z.FULL_H2.values
        sl1 = np.polyfit(c, s1, 1)[0] * 10.0        # Sharpe per 10 bps
        sl2 = np.polyfit(c, s2, 1)[0] * 10.0
        r10 = z[z.cost == COST0].iloc[0]
        mech.append(dict(panel=pn, arm=arm, gross=g, slope_H1=sl1, slope_H2=sl2,
                         turn_H1=r10.turn_H1, turn_H2=r10.turn_H2,
                         margin_H1=r10.m670_L1_H1, margin_H2=r10.m670_L2_H2,
                         be_H1=(r10.m670_L1_H1 / -sl1 * 10.0 + COST0) if sl1 < 0 else np.nan,
                         be_H2=(r10.m670_L2_H2 / -sl2 * 10.0 + COST0) if sl2 < 0 else np.nan))
    MK = pd.DataFrame(mech)
    dump(MK, "mechanism.csv")
    P("  per-half ANNUAL TURNOVER and per-half COST SLOPE (Sharpe per 10 bps), median by panel:")
    P("    panel   turn_H1  turn_H2   ratio | slope_H1  slope_H2   ratio | margin_H1 margin_H2")
    for pn in PANELS:
        z = MK[MK.panel == pn]
        tr = z.turn_H1.median() / z.turn_H2.median()
        sr = z.slope_H1.median() / z.slope_H2.median()
        P(f"    {pn:6s} {z.turn_H1.median():8.2f} {z.turn_H2.median():8.2f} {tr:7.3f} | "
          f"{z.slope_H1.median():+9.5f} {z.slope_H2.median():+9.5f} {sr:7.3f} | "
          f"{z.margin_H1.median():+9.4f} {z.margin_H2.median():+9.4f}")
    zs = MK[MK.panel == "U56"]
    slope_gap = abs(zs.slope_H1.median() / zs.slope_H2.median() - 1.0)
    P(f"  H_SLOPE: |slope_H1/slope_H2 - 1| on U56 = {slope_gap:.4f} vs bar {SLOPE_BAR} -> "
      f"{'TURNOVER mechanism admissible' if slope_gap > SLOPE_BAR else 'FALSIFIED: the slopes are within the bar, so the carrier is the MARGIN, not the slope'}")
    P("")
    P("  the SUBJECT's own decomposition at g=0.75 (U56/CAND20):")
    r = MK[(MK.panel == "U56") & (MK.arm == "CAND20") & (MK.gross == 0.75)].iloc[0]
    P(f"    margin_H1 {r.margin_H1:+.4f} vs margin_H2 {r.margin_H2:+.4f} at 10 bps; "
      f"slope {r.slope_H1:+.5f} / {r.slope_H2:+.5f} per 10 bps")
    P(f"    breakeven cost: H1 {r.be_H1:.2f} bps, H2 {r.be_H2:.2f} bps  "
      f"(turnover {r.turn_H1:.2f} vs {r.turn_H2:.2f} x/yr)")

    P("")
    P("=" * 112)
    P("(E) RULE 8 -- gross chosen on 2009-2016 ONLY, 2017-2026 read once (both KEEP paths)")
    P("=" * 112)
    W = rule8(pans, books, spyref, v2ref)
    dump(W, "walkforward.csv")
    P("")
    P("  panel  cost  chooser        g     OOS CAGR  Sharpe   MaxDD  | SPY OOS            | "
      "RULES v2 OOS        | 4b  4a")
    for _, r in W.iterrows():
        P(f"  {r.panel:6s} {int(r.cost):3d}  {r.chooser:12s} {r.gross:.3f}  "
          f"{r.OOS_CAGR:8.2%} {r.OOS_Sharpe:7.3f} {r.OOS_MaxDD:7.2%}  | "
          f"{r.SPY_OOS_CAGR:6.2%}/{r.SPY_OOS_Sharpe:.3f}/{r.SPY_OOS_MaxDD:7.2%} | "
          f"{r.V2_OOS_CAGR:6.2%}/{r.V2_OOS_Sharpe:.3f}/{r.V2_OOS_MaxDD:7.2%} | "
          f"{'Y' if r.OOS_pass4b else 'n'}   {'Y' if r.OOS_pass4a else 'n'}")
    P("")
    for cost in [0.0, COST0] + KILL_RUNGS:
        z = W[W.cost == cost]
        P(f"  at {int(cost):3d} bps: 4b {int(z.OOS_pass4b.sum())} of {len(z)} picks, "
          f"4a {int(z.OOS_pass4a.sum())} of {len(z)}")

    P("")
    P("=" * 112)
    P("(F) DETERMINISM (G7) and VERDICT")
    P("=" * 112)
    C2 = build_census(pans, books, spyref, v2ref)
    num = C.select_dtypes(include=[float]).values
    num2 = C2.select_dtypes(include=[float]).values
    d = float(np.nanmax(np.abs(num - num2))) if num.shape == num2.shape else np.inf
    gates["G7"] = d == 0.0
    P(f"G7  determinism (census rebuilt): max|d| {d:.3e}   -> {'PASS' if gates['G7'] else 'FAIL'}")
    P("")
    P(f"GATES: {sum(bool(v) for v in gates.values())} of {len(gates)} PASS  "
      + "  ".join(f"{k}={'PASS' if v else 'FAIL'}" for k, v in sorted(gates.items())))
    P(f"elapsed {time.time() - t0:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    return C, F, CP, MK, W


if __name__ == "__main__":
    main()

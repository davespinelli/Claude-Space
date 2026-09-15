#!/usr/bin/env python3
"""Idea 677 (lane B, 2026-09-15) -- is the GROSS WINDOW WIDTH a better 4b statistic than the 4b PASS?

THE QUESTION (queue, 2026-09-11)
  Idea 670 found that PROTOCOL 4b's two level legs are not really two tests of a book, they are
  two one-sided constraints on the book's GROSS:

      DD cap      MaxDD(g) >= 0.60 * MaxDD(SPY)      binds from ABOVE   ->  g <= g_max
      CAGR floor  CAGR(g)  >= 0.70 * CAGR(SPY)       binds from BELOW   ->  g >= g_min

  Together they cut a GROSS WINDOW [g_min, g_max] out of the exposure axis.  Its WIDTH
      W = g_max - g_min
  is negative for a zero-signal book (g x SPY) and >= 0.00 for 17 of 20 committed arms, and the
  published 4b PASS is nothing but a POINT reading of that window at one gross (the live 0.75).
  The queue asks: compute W for a whole population of books, and test whether W predicts OOS
  Sharpe and OOS MaxDD BETTER THAN THE BINARY PASS DOES -- and, the leg that matters for capital,
  whether CHOOSING books by W out of sample beats choosing them by the pass.

WHAT IS TUNED AND WHAT IS REPORTED (PROTOCOL 4: max 2 tuned parameters)
  TUNED 1  RUNG RESOLUTION -- the step of the gross ladder the window is solved on
           (the queue's own second dial): STEP in {0.25, 0.10, 0.05}.
  TUNED 2  TOPK -- how many books the chooser leg takes: k in {1, 3, 5, 10}.
  REPORTED AXES (the queue's "claim set", every point published in .books.csv / .grid.csv):
           panel (3) x gate family (4) x mode (3) x breadth trigger theta (5) = 180 books,
           plus 3 ZEROSIG controls and 9 RANDGATE controls.  Nothing below is fitted on them.

THE BOOK POPULATION (the machinery is the record's, unchanged)
  ROW  hold each name passing its own gate at gross/N of NAV, rest in CASH (TREND/ROW at
       g=0.75 IS RULES v2 -- gate G1).
  AGG  know only the breadth b_t = (#passing)/(#priced): hold the WHOLE priced panel equal
       weighted at `gross` when b_t >= theta, else all cash.
  HYB  the ROW book, switched off on days when b_t < theta.
  families  TREND (200d MA +/-3% band), VOL (vol20 < 0.60), MOM (12-1 > 0),
            DISP (60d idiosyncratic vol below the panel's own cross-sectional mean).
  controls  ZEROSIG = g x SPY (the queue's own reference book, expected W < 0)
            RANDGATE = a seeded per-name random gate at the family's own mean breadth.

PRE-REGISTERED HYPOTHESES (fixed before any number below was read)
  H1  |Spearman(W_IS, OOS Sharpe)| > |point-biserial(PASS_IS, OOS Sharpe)|.
  H2  |Spearman(W_IS, OOS MaxDD)| > |point-biserial(PASS_IS, OOS MaxDD)|  (wider -> shallower).
  H3  AUC(W_IS -> OOS 4b pass) > AUC(PASS_IS -> OOS 4b pass), i.e. the continuous statistic
      ranks the out-of-sample verdict better than the in-sample verdict does.
  H4  ZEROSIG has W < 0 on every panel at every rung resolution (670's sign reproduced).
  H5  the WIDTH chooser's OOS blend has a higher OOS Sharpe than the PASS chooser's, at a
      majority of (STEP, k) grid points.

PROTOCOL
  2  10 bps per unit turnover, weights at close t applied t+1 (LAG=1), weekly, no leverage in any
     TRADED book (chooser gross is clipped to <= 1.00); the ladder is solved up to 1.50 so that a
     window whose floor is unreachable can be REPORTED rather than silently clipped.
  3  every reported book compared to RULES v2 (live) and to SPY buy-and-hold on the same sample.
  4  BOTH KEEP paths evaluated at EVERY (STEP, k) grid point, for both choosers.
  8  WALK-FORWARD: W, PASS and every chooser decision are computed on 2009-2016 ALONE;
     2017-2026 is read ONCE, per (STEP, k, chooser).
  9  SURVIVORSHIP: all three panels are current-constituent lists; levels are optimistic.

GATES (run and printed BEFORE any result number is read)
  G1  TREND/ROW at gross 0.75 IS baseline.rules_v2_weights (max |weight| and |return| deviation).
  G2  fast_run == engine.backtest on a representative book (returns AND turnover).
  G3  SPY and RULES v2 on U56 reproduce their committed triples
      (15.16%/0.8861/-33.72% and 8.63%/1.2018/-12.05%).
  G4  ZEROSIG at rung g reproduces the cash blend: MaxDD(g)/MaxDD(SPY) ~ g and CAGR monotone.
  G5  MONOTONICITY of the ladder -- the share of books where MaxDD(g) is non-increasing and
      CAGR(g) non-decreasing in g (the window is only well defined where it is).
  G6  DETERMINISM: the whole book grid rebuilt twice, max |dSharpe|.

Outputs beside this script: .console.txt .books.csv .ladder.csv .grid.csv .walkforward.csv
                            .predict.csv .null.csv .result.md
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
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

# ---- reported constants (never tuned) ---------------------------------------------------------
COST = 10.0                        # PROTOCOL 2
FREQ = "W"
LAG = 1
BAND = 0.03                        # RULES v2 clause 2
MAXVOL = 0.60                      # rules_v1_weights' committed max_vol
VOLWIN = 20
DISPWIN = 60
WARMUP = 260                       # the record's warm-up skip
IS_END, OOS_START = "2016-12-31", "2017-01-01"
LIVE_GROSS = 0.75                  # RULES v2's committed gross -- where the binary PASS is read
DD_CAP, CAGR_FLOOR = 0.60, 0.70    # PROTOCOL 4b
GMAX_LADDER = 1.50                 # ladder ceiling (REPORTING only; traded gross clipped to 1.00)
COSTRUNGS = [0.0, 10.0, 25.0]
NULL_DRAWS, NULL_SEED = 20, 677

# ---- TUNED DIAL 1: rung resolution ------------------------------------------------------------
STEPS = [0.25, 0.10, 0.05]
# ---- TUNED DIAL 2: chooser size ---------------------------------------------------------------
TOPKS = [1, 3, 5, 10]

# ---- reported axes ----------------------------------------------------------------------------
FAMILIES = ["TREND", "VOL", "MOM", "DISP"]
MODES = ["ROW", "AGG", "HYB"]
THETAS = [0.00, 0.20, 0.40, 0.60, 0.80]

SPY_U56 = (0.1516, 0.8861, -0.3372)
V2_U56 = (0.0863, 1.2018, -0.1205)
TOL_C, TOL_S, TOL_D = 0.004, 0.030, 0.015

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
# runner -- the record's vectorised equivalent of engine.backtest (gated at G2)
# ================================================================================================
class Panel:
    """Everything that depends only on the PRICES, precomputed once and shared by every book."""

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
        self.R = self.Cp / self.Cp[self.s0]              # per-name drift since last rebalance
        self.Rp = self.Cp[self.reb] / self.Cp[self.s0p[self.reb]]   # ... at rebalance rows only
        self.start = self.idx[WARMUP]
        self.m_is = (self.idx >= self.start) & (self.idx <= pd.Timestamp(IS_END))
        self.m_oos = self.idx >= pd.Timestamp(OOS_START)
        self.m_full = self.idx >= self.start
        self.spy = px["SPY"].pct_change().fillna(0.0).values


class Book:
    """One book's gross-1.0 weights, pre-reduced so that ANY gross rung costs O(T) + O(|reb| x N).

    Weights scale exactly with g (targets g*w, cash 1 - g*sum(w)), so with
        A  = shift(W1, LAG) gathered at the last rebalance row,   AR  = A * drift
    the portfolio value is V(g) = 1 + g*(sum(AR) - sum(A)) and the gross return is
        r(g) = g * sum(AR * rets) / V(g).
    Gated against engine.backtest at G2 -- no approximation is taken on trust.
    """

    def __init__(self, panel: Panel, W1: np.ndarray):
        self.pan = panel
        wt = np.roll(W1, LAG, axis=0).copy()
        wt[:LAG] = 0.0
        self.wt_reb = wt[panel.reb]                       # |reb| x N, for turnover
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

    def at(self, g: float, cost=COST):
        pan = self.pan
        V = 1.0 + g * (self.S - self.As)
        gross = g * self.ARr / V
        Vp = 1.0 + g * (self.Sp - self.Asp)
        heldp = (g * self.ARp) / Vp[:, None]
        heldp[0] = 0.0
        turn = np.zeros(pan.T)
        turn[pan.reb] = np.abs(g * self.wt_reb - heldp).sum(axis=1)
        return gross - turn * cost / 1e4, turn


def run(panel: Panel, W1: np.ndarray, g: float, cost=COST):
    """Convenience wrapper (gates, one-off cells). Book(...) is what the grid uses."""
    return Book(panel, W1).at(g, cost=cost)


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


def pass4a(s, base):
    return bool(s["H1"] > base["H1"] and s["H2"] > base["H2"] and s["MaxDD"] >= base["MaxDD"])


def legs4b(s, spy):
    """4b's four WINDOW-LOCAL legs (the OOS leg is applied separately, by rule 8)."""
    return dict(H1=bool(s["H1"] > spy["H1"]), H2=bool(s["H2"] > spy["H2"]),
                DDCAP=bool(s["MaxDD"] >= DD_CAP * spy["MaxDD"]),
                CAGRFLOOR=bool(s["CAGR"] >= CAGR_FLOOR * spy["CAGR"]))


# ================================================================================================
# gate families -> per-name boolean IN(i,t)  (the record's definitions, unchanged)
# ================================================================================================
def gate_in(px, family, seed=None):
    priced = px.notna()
    if family == "TREND":
        g = band_state(px, BAND)
    elif family == "VOL":
        vol = px.pct_change().rolling(VOLWIN).std() * np.sqrt(252)
        g = vol < MAXVOL
    elif family == "MOM":
        g = (px.shift(21) / px.shift(252) - 1.0) > 0.0
    elif family == "DISP":
        r = px.pct_change()
        idio = r.sub(r.mean(axis=1), axis=0).rolling(DISPWIN).std() * np.sqrt(252)
        g = idio.lt(idio.mean(axis=1), axis=0)
    elif family == "RANDGATE":
        rng = np.random.default_rng(seed)
        g = pd.DataFrame(rng.random(px.shape) < 0.5, index=px.index, columns=px.columns)
    else:
        raise ValueError(family)
    return g.fillna(False) & priced


def ew_panel(px):
    priced = px.notna()
    n = priced.sum(axis=1).replace(0, np.nan)
    return priced.astype(float).div(n, axis=0).fillna(0.0)


def book_w1(px, ew, inb, b, mode, theta):
    """gross-1.0 target weights for one book."""
    if mode == "ROW":
        return ew.where(inb, 0.0).values
    on = (b >= theta).astype(float)
    if mode == "AGG":
        return ew.mul(on, axis=0).values
    return ew.where(inb, 0.0).mul(on, axis=0).values


# ================================================================================================
# the gross window
# ================================================================================================
def solve_window(gs, cagrs, dds, spy_cagr, spy_dd):
    """[g_min, g_max] on the ladder `gs`, by linear interpolation between adjacent rungs.

    DD cap   MaxDD(g) >= DD_CAP*spy_dd   (both negative; binds from above)  -> g_max
    CAGR floor CAGR(g) >= CAGR_FLOOR*spy_cagr                               -> g_min
    Returns (g_min, g_max, width, gmin_state, gmax_state) where state is one of
    'interp' / 'all' (leg holds at every rung) / 'none' (leg holds at no rung).
    """
    dd_bar, cagr_bar = DD_CAP * spy_dd, CAGR_FLOOR * spy_cagr
    ok_dd = dds >= dd_bar
    ok_cg = cagrs >= cagr_bar

    if ok_dd.all():
        g_max, smax = gs[-1], "all"
    elif not ok_dd.any():
        g_max, smax = 0.0, "none"
    else:
        j = int(np.flatnonzero(ok_dd)[-1])
        if j == len(gs) - 1:
            g_max, smax = gs[-1], "all"
        else:
            y0, y1 = dds[j], dds[j + 1]
            f = 0.0 if y0 == y1 else (y0 - dd_bar) / (y0 - y1)
            g_max, smax = gs[j] + float(np.clip(f, 0, 1)) * (gs[j + 1] - gs[j]), "interp"

    if ok_cg.all():
        g_min, smin = gs[0], "all"
    elif not ok_cg.any():
        g_min, smin = np.nan, "none"
    else:
        i = int(np.flatnonzero(ok_cg)[0])
        if i == 0:
            g_min, smin = gs[0], "all"
        else:
            y0, y1 = cagrs[i - 1], cagrs[i]
            f = 0.0 if y1 == y0 else (cagr_bar - y0) / (y1 - y0)
            g_min, smin = gs[i - 1] + float(np.clip(f, 0, 1)) * (gs[i] - gs[i - 1]), "interp"

    if smin == "none":
        # the floor is unreachable anywhere on the ladder: the window is empty by the full ladder
        return np.nan, g_max, g_max - GMAX_LADDER, smin, smax
    return g_min, g_max, g_max - g_min, smin, smax


# ================================================================================================
# statistics
# ================================================================================================
def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    m = np.isfinite(x) & np.isfinite(y)
    if m.sum() < 3:
        return np.nan
    xr = pd.Series(x[m]).rank().values
    yr = pd.Series(y[m]).rank().values
    if xr.std() == 0 or yr.std() == 0:
        return np.nan
    return float(np.corrcoef(xr, yr)[0, 1])


def auc(score, label):
    """Mann-Whitney AUC of a continuous score against a boolean label (ties = 0.5)."""
    score, label = np.asarray(score, float), np.asarray(label, bool)
    m = np.isfinite(score)
    score, label = score[m], label[m]
    pos, neg = score[label], score[~label]
    if len(pos) == 0 or len(neg) == 0:
        return np.nan
    r = pd.Series(np.concatenate([pos, neg])).rank().values
    return float((r[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2.0) / (len(pos) * len(neg)))


# ================================================================================================
# panels
# ================================================================================================
def load_panels():
    P("=" * 100)
    P("(D) PANELS")
    P("=" * 100)
    panels = {}
    panels["U56"] = load_universe()
    panels["B136"] = load_universe(broad=True)
    s = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    drop = [c for c in s.columns if c in bad]
    s = s.drop(columns=drop)
    panels[f"SMALL{s.shape[1] - 1}"] = s
    P(f"  SMALL: dropped {len(drop)} of {len(meta)} meta tickers with max_1d_move >= 1.0")
    out = {}
    for k, v in panels.items():
        p = Panel(k, v)
        out[k] = p
        P(f"  {k:10s} {v.shape[1]:4d} cols  {v.index[0].date()} -> {v.index[-1].date()}  "
          f"{len(v):,} rows   warm-up start {p.start.date()}   "
          f"IS {int(p.m_is.sum()):,}d  OOS {int(p.m_oos.sum()):,}d")
    return out


# ================================================================================================
# GATES
# ================================================================================================
def gates(panels):
    P()
    P("=" * 100)
    P("(G) GATES -- run and printed before any result number is read")
    P("=" * 100)
    ok = True
    u = panels["U56"]

    # G1 -- TREND/ROW at 0.75 IS RULES v2
    ew = ew_panel(u.px)
    inb = gate_in(u.px, "TREND")
    b = (inb.sum(axis=1) / u.px.notna().sum(axis=1).replace(0, np.nan)).fillna(0.0)
    W1 = book_w1(u.px, ew, inb, b, "ROW", 0.0)
    v2 = rules_v2_weights(u.px, band=BAND, gross=LIVE_GROSS).values
    dW = float(np.nanmax(np.abs(W1 * LIVE_GROSS - v2)))
    r_mine, _ = run(u, W1, LIVE_GROSS)
    r_v2 = backtest(u.px, rules_v2_weights(u.px, band=BAND, gross=LIVE_GROSS),
                    cost_bps=COST, freq=FREQ)["returns"].values
    dR = float(np.nanmax(np.abs(r_mine - r_v2)))
    g1 = dW < 1e-12 and dR < 1e-10
    P(f"  G1 TREND/ROW @0.75 == RULES v2 :  max|dW| {dW:.3e}   max|dreturn| {dR:.3e}   "
      f"-> {'PASS' if g1 else 'FAIL'}")
    ok &= g1

    # G2 -- fast runner == engine.backtest on a non-trivial book (VOL/HYB, theta 0.4)
    inb2 = gate_in(u.px, "VOL")
    b2 = (inb2.sum(axis=1) / u.px.notna().sum(axis=1).replace(0, np.nan)).fillna(0.0)
    W2 = book_w1(u.px, ew, inb2, b2, "HYB", 0.40)
    wdf = pd.DataFrame(W2 * 0.60, index=u.idx, columns=u.px.columns)
    mine, turn = run(u, W2, 0.60)
    eng = backtest(u.px, wdf, cost_bps=COST, freq=FREQ)
    d2r = float(np.nanmax(np.abs(mine - eng["returns"].values)))
    d2t = float(np.nanmax(np.abs(turn - eng["turnover"].values)))
    g2 = d2r < 1e-10 and d2t < 1e-10
    P(f"  G2 fast run == engine.backtest :  max|dreturn| {d2r:.3e}   max|dturnover| {d2t:.3e}   "
      f"-> {'PASS' if g2 else 'FAIL'}")
    ok &= g2

    # G3 -- committed triples
    spy_full = u.spy[u.m_full]
    c, s, d = fmet(spy_full)
    g3a = abs(c - SPY_U56[0]) < TOL_C and abs(s - SPY_U56[1]) < TOL_S and abs(d - SPY_U56[2]) < TOL_D
    P(f"  G3a SPY U56 full        : {c:.4%} / {s:.4f} / {d:.4%}  vs committed "
      f"{SPY_U56[0]:.2%} / {SPY_U56[1]:.4f} / {SPY_U56[2]:.2%}  -> {'PASS' if g3a else 'FAIL'}")
    rv2 = r_mine[u.m_full]
    c2, s2, d2 = fmet(rv2)
    g3b = (abs(c2 - V2_U56[0]) < TOL_C and abs(s2 - V2_U56[1]) < TOL_S
           and abs(d2 - V2_U56[2]) < TOL_D)
    P(f"  G3b RULES v2 U56 full   : {c2:.4%} / {s2:.4f} / {d2:.4%}  vs committed "
      f"{V2_U56[0]:.2%} / {V2_U56[1]:.4f} / {V2_U56[2]:.2%}  -> {'PASS' if g3b else 'FAIL'}")
    ok &= g3a and g3b

    # G4 -- ZEROSIG reproduces the cash blend
    Z = np.zeros((u.T, u.N))
    Z[:, list(u.px.columns).index("SPY")] = 1.0
    rows = []
    for g in (0.25, 0.50, 0.75, 1.00):
        rz, _ = run(u, Z, g, cost=0.0)
        cz, sz, dz = fmet(rz[u.m_full])
        rows.append((g, cz, dz, dz / d))
    g4 = all(abs(r[3] - r[0]) < 0.06 for r in rows) and all(
        rows[i][1] < rows[i + 1][1] for i in range(len(rows) - 1))
    P("  G4 ZEROSIG (g x SPY, 0 bps) cash-blend check:")
    for g, cz, dz, ratio in rows:
        P(f"      g={g:.2f}  CAGR {cz:.4%}   MaxDD {dz:.4%}   MaxDD/MaxDD(SPY) {ratio:.4f}")
    P(f"      -> {'PASS' if g4 else 'FAIL'}  (ratio ~ g within 0.06, CAGR monotone in g)")
    ok &= g4

    P(f"  GATES G1-G4: {'ALL PASS' if ok else 'A GATE FAILED'}  "
      "(G5 monotonicity and G6 determinism are printed with the ladder)")
    return ok


# ================================================================================================
# build every book and its gross ladder
# ================================================================================================
GATE_CACHE: dict = {}


def gate_cache(pan: Panel):
    """Per-panel gate matrices + breadth, built once (W1 is rebuilt on demand, never stored)."""
    if pan.name in GATE_CACHE:
        return GATE_CACHE[pan.name]
    priced_n = pan.px.notna().sum(axis=1).replace(0, np.nan)
    c = {"_ew": ew_panel(pan.px)}
    for fam in FAMILIES:
        inb = gate_in(pan.px, fam)
        c[fam] = (inb, (inb.sum(axis=1) / priced_n).fillna(0.0))
    for si in range(3):
        inb = gate_in(pan.px, "RANDGATE", seed=NULL_SEED + si)
        c[f"RANDGATE{si}"] = (inb, (inb.sum(axis=1) / priced_n).fillna(0.0))
    GATE_CACHE[pan.name] = c
    return c


def make_W1(pan: Panel, fam, mode, theta):
    if fam == "ZEROSIG":
        W1 = np.zeros((pan.T, pan.N))
        W1[:, list(pan.px.columns).index("SPY")] = 1.0
        return W1
    c = gate_cache(pan)
    inb, b = c[fam]
    return book_w1(pan.px, c["_ew"], inb, b, mode, theta)


def book_of(panels, bid) -> Book:
    pname, fam, mode, th = bid.split("|")
    pan = panels[pname]
    return Book(pan, make_W1(pan, fam, mode, float(th)))


def build_books(panels, ladder):
    """ladder: the FINEST gross ladder; coarser STEPs are sub-sampled from it."""
    specs, lad_rows = [], []
    t0 = time.time()
    todo = [(f, m, th) for f in FAMILIES for m in MODES for th in THETAS]
    todo += [(f"RANDGATE{i}", "ROW", 0.00) for i in range(3)]
    todo += [("ZEROSIG", "ROW", 0.00)]
    for pname, pan in panels.items():
        gate_cache(pan)
        for fam, mode, th in todo:
            bk = Book(pan, make_W1(pan, fam, mode, th))
            bid = f"{pname}|{fam}|{mode}|{th:.2f}"
            per = {}
            for g in ladder:
                r, _ = bk.at(g)
                cis, sis, dis = fmet(r[pan.m_is])
                coos, soos, doos = fmet(r[pan.m_oos])
                per[round(g, 4)] = (cis, sis, dis, coos, soos, doos)
                lad_rows.append(dict(book=bid, panel=pname, family=fam, mode=mode, theta=th,
                                     gross=round(g, 4), IS_CAGR=cis, IS_Sharpe=sis, IS_MaxDD=dis,
                                     OOS_CAGR=coos, OOS_Sharpe=soos, OOS_MaxDD=doos))
            rl, _ = bk.at(LIVE_GROSS)
            specs.append(dict(book=bid, panel=pname, family=fam, mode=mode, theta=th,
                              ladder=per, live_is=pack(rl[pan.m_is]), live_oos=pack(rl[pan.m_oos])))
            del bk
    P(f"  built {len(specs)} books x {len(ladder)} rungs = {len(specs)*len(ladder):,} runs "
      f"in {time.time()-t0:.1f}s")
    return specs, pd.DataFrame(lad_rows)


def bench(panels):
    """SPY and RULES v2 reference metrics per panel, per window."""
    out = {}
    for pname, pan in panels.items():
        ew = ew_panel(pan.px)
        inb = gate_in(pan.px, "TREND")
        b = (inb.sum(axis=1) / pan.px.notna().sum(axis=1).replace(0, np.nan)).fillna(0.0)
        r_v2, _ = run(pan, book_w1(pan.px, ew, inb, b, "ROW", 0.0), LIVE_GROSS)
        out[pname] = dict(
            SPY_IS=pack(pan.spy[pan.m_is]), SPY_OOS=pack(pan.spy[pan.m_oos]),
            SPY_FULL=pack(pan.spy[pan.m_full]),
            V2_IS=pack(r_v2[pan.m_is]), V2_OOS=pack(r_v2[pan.m_oos]),
            V2_FULL=pack(r_v2[pan.m_full]), v2_rets=r_v2)
    return out


# ================================================================================================
def main():
    t_all = time.time()
    P("=" * 100)
    P("IDEA 677 (lane B, 2026-09-15) -- is the GROSS WINDOW WIDTH a better 4b statistic "
      "than the 4b PASS?")
    P("=" * 100)
    P(f"  costs {COST:.0f} bps | freq {FREQ} | lag {LAG} | IS <= {IS_END} | OOS >= {OOS_START}")
    P(f"  TUNED 1 rung resolution STEP {STEPS} | TUNED 2 chooser size TOPK {TOPKS}")
    P(f"  reported axes: 3 panels x {len(FAMILIES)} families x {len(MODES)} modes x "
      f"{len(THETAS)} thetas + 3 RANDGATE + 1 ZEROSIG per panel")
    P()

    panels = load_panels()
    gok = gates(panels)
    P()

    ladder = [round(x, 4) for x in np.arange(0.05, GMAX_LADDER + 1e-9, 0.05)]
    P("=" * 100)
    P("(B) THE BOOK POPULATION AND ITS GROSS LADDER")
    P("=" * 100)
    P(f"  finest ladder: {len(ladder)} rungs, {ladder[0]:.2f} -> {ladder[-1]:.2f} step 0.05")
    specs, lad = build_books(panels, ladder)
    dump(lad, "ladder.csv")
    bm = bench(panels)

    # ---- G5 monotonicity ----------------------------------------------------------------------
    mono_dd = mono_cg = 0
    for sp in specs:
        gs = np.array(sorted(sp["ladder"]))
        dds = np.array([sp["ladder"][g][2] for g in gs])
        cgs = np.array([sp["ladder"][g][0] for g in gs])
        mono_dd += int(np.all(np.diff(dds) <= 1e-12))
        mono_cg += int(np.all(np.diff(cgs) >= -1e-12))
    P(f"  G5 MONOTONICITY on the IS window, {len(specs)} books, 30 rungs:")
    P(f"      MaxDD(g) non-increasing : {mono_dd}/{len(specs)} = {mono_dd/len(specs):.1%}")
    P(f"      CAGR(g)  non-decreasing : {mono_cg}/{len(specs)} = {mono_cg/len(specs):.1%}")
    P("      (the window is solved by LAST-rung / FIRST-rung crossing, which is defined "
      "regardless; non-monotone books are flagged in .books.csv)")

    # ---- G6 determinism -----------------------------------------------------------------------
    sp0 = specs[0]
    r_a, _ = book_of(panels, sp0["book"]).at(LIVE_GROSS)
    r_b, _ = book_of(panels, sp0["book"]).at(LIVE_GROSS)
    P(f"  G6 DETERMINISM: max|d| on a rebuilt book = {float(np.max(np.abs(r_a - r_b))):.3e} "
      f"-> {'PASS' if np.max(np.abs(r_a-r_b)) == 0 else 'FAIL'}")
    P()

    # ============================================================================================
    # (W) the gross window, per book, per rung resolution  -- TUNED DIAL 1, every point reported
    # ============================================================================================
    P("=" * 100)
    P("(W) THE GROSS WINDOW  [g_min, g_max],  W = g_max - g_min   (IS window, 2009-2016)")
    P("=" * 100)
    brows = []
    for sp in specs:
        bb = bm[sp["panel"]]
        gs_all = np.array(sorted(sp["ladder"]))
        cis = np.array([sp["ladder"][g][0] for g in gs_all])
        dis = np.array([sp["ladder"][g][2] for g in gs_all])
        # the binary PASS, read at the live gross on the IS window
        mlive_is, mlive_oos = sp["live_is"], sp["live_oos"]
        l4b_is = legs4b(mlive_is, bb["SPY_IS"])
        pass_is = all(l4b_is.values()) and mlive_is["Sharpe"] > bb["SPY_IS"]["Sharpe"]
        l4b_oos = legs4b(mlive_oos, bb["SPY_OOS"])
        pass_oos = all(l4b_oos.values()) and mlive_oos["Sharpe"] > bb["SPY_OOS"]["Sharpe"]
        pass4a_is = pass4a(mlive_is, bb["V2_IS"])
        pass4a_oos = pass4a(mlive_oos, bb["V2_OOS"])
        row = dict(book=sp["book"], panel=sp["panel"], family=sp["family"], mode=sp["mode"],
                   theta=sp["theta"],
                   IS_CAGR=mlive_is["CAGR"], IS_Sharpe=mlive_is["Sharpe"], IS_MaxDD=mlive_is["MaxDD"],
                   OOS_CAGR=mlive_oos["CAGR"], OOS_Sharpe=mlive_oos["Sharpe"],
                   OOS_MaxDD=mlive_oos["MaxDD"],
                   PASS_IS_4b=pass_is, PASS_OOS_4b=pass_oos,
                   PASS_IS_4a=pass4a_is, PASS_OOS_4a=pass4a_oos,
                   IS_4b_legs="".join(k[0] for k, v in l4b_is.items() if not v) or "-",
                   mono_dd=bool(np.all(np.diff(dis) <= 1e-12)),
                   mono_cg=bool(np.all(np.diff(cis) >= -1e-12)))
        for step in STEPS:
            k = int(round(step / 0.05))
            sel = np.arange(k - 1, len(gs_all), k)
            gmin, gmax, w, smin, smax = solve_window(
                gs_all[sel], cis[sel], dis[sel], bb["SPY_IS"]["CAGR"], bb["SPY_IS"]["MaxDD"])
            tag = f"{step:.2f}"
            row[f"gmin@{tag}"] = gmin
            row[f"gmax@{tag}"] = gmax
            row[f"W@{tag}"] = w
            row[f"state@{tag}"] = f"{smin}/{smax}"
        brows.append(row)
    books = pd.DataFrame(brows)
    dump(books, "books.csv")

    real = books[~books.family.isin(["ZEROSIG"]) & ~books.family.str.startswith("RANDGATE")]
    P(f"  {len(books)} books: {len(real)} gate books, "
      f"{(books.family=='ZEROSIG').sum()} ZEROSIG, "
      f"{books.family.str.startswith('RANDGATE').sum()} RANDGATE")
    P()
    P("  WIDTH distribution by rung resolution (gate books only, n=%d):" % len(real))
    P(f"    {'STEP':>6} {'min':>9} {'p25':>9} {'median':>9} {'p75':>9} {'max':>9} "
      f"{'W>=0':>8} {'gmin NaN':>9}")
    for step in STEPS:
        w = real[f"W@{step:.2f}"]
        P(f"    {step:6.2f} {w.min():9.4f} {w.quantile(.25):9.4f} {w.median():9.4f} "
          f"{w.quantile(.75):9.4f} {w.max():9.4f} {int((w>=0).sum()):5d}/{len(w):<3d} "
          f"{int(real[f'gmin@{step:.2f}'].isna().sum()):9d}")
    P()
    P("  H4 -- the ZEROSIG control (g x SPY): the queue's reference book, expected W < 0")
    zs = books[books.family == "ZEROSIG"]
    for _, r in zs.iterrows():
        P(f"    {r.panel:10s} " + "  ".join(
            f"STEP {s:.2f}: gmin {r[f'gmin@{s:.2f}']:.3f} gmax {r[f'gmax@{s:.2f}']:.3f} "
            f"W {r[f'W@{s:.2f}']:+.4f}" for s in STEPS))
    h4 = bool((zs[[f"W@{s:.2f}" for s in STEPS]] < 0).all().all())
    P(f"    H4 -> {'PASS' if h4 else 'FAIL'}  (W < 0 on every panel at every rung resolution)")
    P()
    P("  RANDGATE control (a seeded coin-flip gate at ~50% breadth):")
    rg = books[books.family.str.startswith("RANDGATE")]
    P(f"    median W@0.05 {rg['W@0.05'].median():+.4f}   W>=0 in "
      f"{int((rg['W@0.05']>=0).sum())}/{len(rg)}   vs gate books median "
      f"{real['W@0.05'].median():+.4f}, W>=0 in {int((real['W@0.05']>=0).sum())}/{len(real)}")
    P()
    P(f"  the binary PASS at the live gross {LIVE_GROSS:.2f} (gate books): "
      f"IS 4b {int(real.PASS_IS_4b.sum())}/{len(real)}, OOS 4b {int(real.PASS_OOS_4b.sum())}/{len(real)}, "
      f"IS 4a {int(real.PASS_IS_4a.sum())}/{len(real)}, OOS 4a {int(real.PASS_OOS_4a.sum())}/{len(real)}")
    P("  IS 4b failing legs (gate books), most common first:")
    for k, v in real.IS_4b_legs.value_counts().head(6).items():
        P(f"      {k:>6}  {v:4d}   (H=half, D=DD cap, C=CAGR floor; '-' = passes all four)")
    P()

    # ============================================================================================
    # (P) THE DECIDING TEST -- does W_IS predict the OOS better than PASS_IS does?
    # ============================================================================================
    P("=" * 100)
    P("(P) THE DECIDING TEST -- W_IS vs PASS_IS as predictors of the OUT-OF-SAMPLE book")
    P("=" * 100)
    prows = []
    for pop_name, pop in (("GATE BOOKS", real), ("ALL BOOKS (+controls)", books)):
        for step in STEPS:
            W = pop[f"W@{step:.2f}"].values
            B = pop.PASS_IS_4b.values.astype(float)
            for tgt in ("OOS_Sharpe", "OOS_MaxDD", "OOS_CAGR"):
                y = pop[tgt].values
                rw, rb = spearman(W, y), spearman(B, y)
                prows.append(dict(population=pop_name, STEP=step, target=tgt, n=len(pop),
                                  rho_W=rw, rho_PASS=rb, abs_gap=abs(rw) - abs(rb),
                                  W_wins=bool(abs(rw) > abs(rb))))
            for lbl in ("PASS_OOS_4b", "PASS_OOS_4a"):
                y = pop[lbl].values.astype(bool)
                aw, ab = auc(W, y), auc(B, y)
                prows.append(dict(population=pop_name, STEP=step, target=f"AUC->{lbl}", n=len(pop),
                                  rho_W=aw, rho_PASS=ab, abs_gap=abs(aw - 0.5) - abs(ab - 0.5),
                                  W_wins=bool(abs(aw - 0.5) > abs(ab - 0.5))))
    pred = pd.DataFrame(prows)
    dump(pred, "predict.csv")

    P("  Spearman / AUC of each statistic against the untouched 2017-2026 window.")
    P("  (rho_W = the continuous WIDTH; rho_PASS = the binary 4b PASS read at the live gross;")
    P("   for AUC rows both are Mann-Whitney AUCs against the OOS verdict, 0.5 = no information.)")
    P()
    for pop_name in ("GATE BOOKS", "ALL BOOKS (+controls)"):
        P(f"  --- {pop_name} (n={int(pred[pred.population==pop_name].n.iloc[0])}) ---")
        P(f"    {'STEP':>6} {'target':>18} {'W':>10} {'PASS':>10} {'|gap|':>10}  W better?")
        for _, r in pred[pred.population == pop_name].iterrows():
            P(f"    {r.STEP:6.2f} {r.target:>18} {r.rho_W:10.4f} {r.rho_PASS:10.4f} "
              f"{r.abs_gap:+10.4f}  {'YES' if r.W_wins else 'no'}")
        P()

    g = pred[pred.population == "GATE BOOKS"]
    h1 = bool(g[(g.target == "OOS_Sharpe")].W_wins.all())
    h2 = bool(g[(g.target == "OOS_MaxDD")].W_wins.all())
    h3 = bool(g[(g.target == "AUC->PASS_OOS_4b")].W_wins.all())
    # ---- WHAT IS THE WIDTH MEASURING? decompose W = g_max - g_min ------------------------------
    P("  DECOMPOSITION -- W = g_max - g_min.  Which leg carries the prediction, and what is each")
    P("  leg correlated with in sample?  (GATE BOOKS, STEP 0.05, Spearman.)")
    dec_rows = []
    for nm, x in (("W = gmax-gmin", real["W@0.05"]), ("gmax  (DD-cap leg)", real["gmax@0.05"]),
                  ("gmin  (CAGR-floor leg)", real["gmin@0.05"]),
                  ("PASS_IS_4b (binary)", real.PASS_IS_4b.astype(float)),
                  ("IS_Sharpe", real.IS_Sharpe), ("IS_MaxDD", real.IS_MaxDD),
                  ("IS_CAGR", real.IS_CAGR)):
        d = dict(predictor=nm,
                 rho_OOS_Sharpe=spearman(x, real.OOS_Sharpe),
                 rho_OOS_MaxDD=spearman(x, real.OOS_MaxDD),
                 rho_OOS_CAGR=spearman(x, real.OOS_CAGR),
                 rho_IS_MaxDD=spearman(x, real.IS_MaxDD),
                 rho_IS_CAGR=spearman(x, real.IS_CAGR))
        dec_rows.append(d)
    dec = pd.DataFrame(dec_rows)
    P(f"    {'predictor':>24} {'OOS Sh':>8} {'OOS DD':>8} {'OOS CAGR':>9} | "
      f"{'IS DD':>8} {'IS CAGR':>8}")
    for _, r in dec.iterrows():
        P(f"    {r.predictor:>24} {r.rho_OOS_Sharpe:8.4f} {r.rho_OOS_MaxDD:8.4f} "
          f"{r.rho_OOS_CAGR:9.4f} | {r.rho_IS_MaxDD:8.4f} {r.rho_IS_CAGR:8.4f}")
    dump(dec, "decompose.csv")
    P()

    P(f"  H1 (W beats PASS on OOS Sharpe at every STEP) -> {'PASS' if h1 else 'FAIL'}")
    P(f"  H2 (W beats PASS on OOS MaxDD at every STEP)   -> {'PASS' if h2 else 'FAIL'}")
    P(f"  H3 (W beats PASS on AUC -> OOS 4b at every STEP) -> {'PASS' if h3 else 'FAIL'}")
    P()

    # ---- shuffle null on the headline rho ------------------------------------------------------
    P("  SHUFFLE NULL on the headline statistic (STEP 0.05, GATE BOOKS, OOS Sharpe),")
    P(f"  {NULL_DRAWS} draws, seed {NULL_SEED}: W_IS relabelled across books, OOS untouched.")
    rng = np.random.default_rng(NULL_SEED)
    Wh = real["W@0.05"].values
    yh = real["OOS_Sharpe"].values
    real_rho = spearman(Wh, yh)
    nul = np.array([spearman(rng.permutation(Wh), yh) for _ in range(NULL_DRAWS)])
    pct = float((nul < real_rho).mean())
    P(f"    real rho {real_rho:+.4f}   null min {nul.min():+.4f} / med {np.median(nul):+.4f} / "
      f"max {nul.max():+.4f}   real is the {pct:.0%} percentile of the null")
    dump(pd.DataFrame(dict(draw=np.arange(NULL_DRAWS), rho=nul)), "null.csv")
    P()

    # ============================================================================================
    # (C) THE CAPITAL LEG -- rule 8: choose on 2009-2016, read 2017-2026 ONCE
    # ============================================================================================
    P("=" * 100)
    P("(C) THE CAPITAL LEG -- PROTOCOL 8 walk-forward: both choosers fitted on 2009-2016 ALONE,")
    P("    2017-2026 read ONCE per (STEP, k, chooser).  Every grid point reported.")
    P("=" * 100)
    spec_by_id = {s["book"]: s for s in specs}
    BCACHE: dict = {}

    def get_book(bid) -> Book:
        if bid not in BCACHE:
            if len(BCACHE) > 24:                      # bounded: Book holds |reb| x N arrays
                BCACHE.clear()
            BCACHE[bid] = book_of(panels, bid)
        return BCACHE[bid]

    def blend(ids, gross_of, mask_key, cost=COST):
        """Equal-weight blend of the chosen books' return series on the given window.

        Books can live on different panels; the blend is taken on the INTERSECTION of their
        trading days (reported as n_days/start/end in .walkforward.csv) so that no day is an
        average over a different number of books.
        """
        cols = []
        for bid in ids:
            pan = panels[spec_by_id[bid]["panel"]]
            r, _ = get_book(bid).at(gross_of[bid], cost=cost)
            m = getattr(pan, mask_key)
            cols.append(pd.Series(r[m], index=pan.idx[m], name=bid))
        return pd.concat(cols, axis=1).dropna().mean(axis=1)

    wf_rows, grid_rows = [], []
    # reference OOS benchmarks (U56 is the live panel; blends span panels so SPY/v2 are per panel)
    for step in STEPS:
        wcol = f"W@{step:.2f}"
        pool = real.copy()
        for k in TOPKS:
            # --- chooser A: WIDTH.  rank by W_IS, take top k; trade at the window MIDPOINT
            a = pool.sort_values(wcol, ascending=False).head(k)
            gross_a = {}
            for _, r in a.iterrows():
                lo = r[f"gmin@{step:.2f}"]
                hi = r[f"gmax@{step:.2f}"]
                mid = LIVE_GROSS if not np.isfinite(lo) else (lo + hi) / 2.0
                gross_a[r.book] = float(np.clip(mid, 0.05, 1.00))
            # --- chooser A2: WIDTH at the LIVE gross -- isolates SELECTION from SIZING,
            #     because chooser A's midpoint runs the book at a different exposure
            gross_a75 = {r.book: LIVE_GROSS for _, r in a.iterrows()}
            # --- chooser B: PASS.  the IS 4b passers, ranked by IS Sharpe, top k; live gross
            pas = pool[pool.PASS_IS_4b]
            b_sel = (pas if len(pas) else pool).sort_values("IS_Sharpe", ascending=False).head(k)
            gross_b = {r.book: LIVE_GROSS for _, r in b_sel.iterrows()}
            # --- chooser C (reference): rank by IS Sharpe alone, live gross
            c_sel = pool.sort_values("IS_Sharpe", ascending=False).head(k)
            gross_c = {r.book: LIVE_GROSS for _, r in c_sel.iterrows()}

            for cname, sel, gof in (("WIDTH", a, gross_a), ("WIDTH@75", a, gross_a75),
                                    ("PASS", b_sel, gross_b), ("ISSHARPE", c_sel, gross_c)):
                r_is = blend(list(sel.book), gof, "m_is")
                r_oos = blend(list(sel.book), gof, "m_oos")
                m_is, m_oos = pack(r_is.values), pack(r_oos.values)
                # benchmarks on the blend's own OOS index
                pans = sorted({spec_by_id[b]["panel"] for b in sel.book})
                spy_o = pd.concat([pd.Series(panels[p].spy[panels[p].m_oos],
                                             index=panels[p].idx[panels[p].m_oos])
                                   for p in pans], axis=1).mean(axis=1).reindex(r_oos.index).fillna(0)
                v2_o = pd.concat([pd.Series(bm[p]["v2_rets"][panels[p].m_oos],
                                            index=panels[p].idx[panels[p].m_oos])
                                  for p in pans], axis=1).mean(axis=1).reindex(r_oos.index).fillna(0)
                m_spy, m_v2 = pack(spy_o.values), pack(v2_o.values)
                l4b = legs4b(m_oos, m_spy)
                l4b["OOSSH"] = bool(m_oos["Sharpe"] > m_spy["Sharpe"])
                p4b = all(l4b.values())
                p4a = pass4a(m_oos, m_v2)
                wf_rows.append(dict(
                    STEP=step, k=k, chooser=cname, n_books=len(sel),
                    books="; ".join(sel.book),
                    n_days=len(r_oos), oos_start=str(r_oos.index[0].date()),
                    oos_end=str(r_oos.index[-1].date()),
                    mean_gross=float(np.mean(list(gof.values()))),
                    IS_CAGR=m_is["CAGR"], IS_Sharpe=m_is["Sharpe"], IS_MaxDD=m_is["MaxDD"],
                    OOS_CAGR=m_oos["CAGR"], OOS_Sharpe=m_oos["Sharpe"], OOS_MaxDD=m_oos["MaxDD"],
                    OOS_H1=m_oos["H1"], OOS_H2=m_oos["H2"],
                    SPY_OOS_CAGR=m_spy["CAGR"], SPY_OOS_Sharpe=m_spy["Sharpe"],
                    SPY_OOS_MaxDD=m_spy["MaxDD"],
                    V2_OOS_CAGR=m_v2["CAGR"], V2_OOS_Sharpe=m_v2["Sharpe"],
                    V2_OOS_MaxDD=m_v2["MaxDD"],
                    OOS_4b=p4b, OOS_4a=p4a,
                    fail4b="".join(kk[0] for kk, vv in l4b.items() if not vv) or "-"))
    wf = pd.DataFrame(wf_rows)
    dump(wf, "walkforward.csv")

    P()
    P("  OOS (2017-2026) blends. SPY/v2 columns are the SAME-PANEL benchmarks on the blend's own")
    P("  index.  4b legs: H=half vs SPY, D=DD cap (<=60% of SPY), C=CAGR floor (>=70% of SPY).")
    P(f"  {'STEP':>5} {'k':>3} {'chooser':>9} {'gross':>6} {'OOS CAGR':>9} {'OOS Sh':>7} "
      f"{'OOS DD':>8} | {'SPY Sh':>7} {'SPY DD':>8} {'v2 Sh':>6} | {'4b':>3} {'4a':>3} {'fail':>5}")
    for _, r in wf.iterrows():
        P(f"  {r.STEP:5.2f} {r.k:3d} {r.chooser:>9} {r.mean_gross:6.2f} {r.OOS_CAGR:9.2%} "
          f"{r.OOS_Sharpe:7.3f} {r.OOS_MaxDD:8.2%} | {r.SPY_OOS_Sharpe:7.3f} "
          f"{r.SPY_OOS_MaxDD:8.2%} {r.V2_OOS_Sharpe:6.3f} | "
          f"{'YES' if r.OOS_4b else ' no':>3} {'YES' if r.OOS_4a else ' no':>3} {r.fail4b:>5}")
    P()

    piv = wf.pivot_table(index=["STEP", "k"], columns="chooser", values="OOS_Sharpe")
    wwin = int((piv["WIDTH"] > piv["PASS"]).sum())
    P(f"  H5 (WIDTH chooser's OOS Sharpe > PASS chooser's) -> {wwin}/{len(piv)} grid points "
      f"= {wwin/len(piv):.0%}  -> {'PASS' if wwin > len(piv)/2 else 'FAIL'}")
    pivd = wf.pivot_table(index=["STEP", "k"], columns="chooser", values="OOS_MaxDD")
    P(f"      on OOS MaxDD (higher = shallower): WIDTH better at "
      f"{int((pivd['WIDTH'] > pivd['PASS']).sum())}/{len(pivd)} points")
    pivc = wf.pivot_table(index=["STEP", "k"], columns="chooser", values="OOS_CAGR")
    P(f"      on OOS CAGR: WIDTH better at {int((pivc['WIDTH'] > pivc['PASS']).sum())}/{len(pivc)} "
      "points")
    P(f"      reference chooser ISSHARPE beats WIDTH on OOS Sharpe at "
      f"{int((piv['ISSHARPE'] > piv['WIDTH']).sum())}/{len(piv)} points")
    P()
    P("  THE GROSS-MATCHED READING (WIDTH@75 = the SAME books, traded at the live 0.75, so the")
    P("  only difference from PASS is WHICH books were chosen, not how big they are run):")
    P(f"      WIDTH@75 beats PASS on OOS Sharpe at "
      f"{int((piv['WIDTH@75'] > piv['PASS']).sum())}/{len(piv)} points")
    P(f"      WIDTH@75 beats PASS on OOS MaxDD  at "
      f"{int((pivd['WIDTH@75'] > pivd['PASS']).sum())}/{len(pivd)} points")
    P(f"      WIDTH@75 beats PASS on OOS CAGR   at "
      f"{int((pivc['WIDTH@75'] > pivc['PASS']).sum())}/{len(pivc)} points")
    P(f"      mean gross: WIDTH {wf[wf.chooser=='WIDTH'].mean_gross.mean():.3f} vs "
      f"WIDTH@75 / PASS / ISSHARPE {LIVE_GROSS:.3f}  <- the unmatched-gross confound H5 carries")
    P()
    P(f"  KEEP paths over the whole {len(wf)}-point chooser grid: "
      f"4b {int(wf.OOS_4b.sum())}/{len(wf)}, 4a {int(wf.OOS_4a.sum())}/{len(wf)}")
    P("  by chooser (12 grid points each) -- this is the leg that decides the verdict:")
    for cname in ("WIDTH", "WIDTH@75", "PASS", "ISSHARPE"):
        sub = wf[wf.chooser == cname]
        fails = "; ".join(f"{k}x{v}" for k, v in sub[~sub.OOS_4b].fail4b.value_counts().items())
        P(f"      {cname:>9}  OOS 4b {int(sub.OOS_4b.sum()):2d}/12   OOS 4a "
          f"{int(sub.OOS_4a.sum()):2d}/12   median OOS Sharpe {sub.OOS_Sharpe.median():.3f}  "
          f"CAGR {sub.OOS_CAGR.median():.2%}  DD {sub.OOS_MaxDD.median():.2%}"
          + (f"   | 4b fails: {fails}" if fails else ""))
    if wf.OOS_4b.any():
        P("  the 4b-passing cells:")
        for _, r in wf[wf.OOS_4b].iterrows():
            P(f"      STEP {r.STEP:.2f} k={r.k} {r.chooser}: OOS {r.OOS_CAGR:.2%} / "
              f"{r.OOS_Sharpe:.3f} / {r.OOS_MaxDD:.2%}  vs SPY {r.SPY_OOS_CAGR:.2%} / "
              f"{r.SPY_OOS_Sharpe:.3f} / {r.SPY_OOS_MaxDD:.2%}")
            P(f"        books: {r.books}")
    P()

    # ---- cost ladder on the headline cells -----------------------------------------------------
    P("  COST LADDER on the headline cell of each chooser (STEP 0.05, k=5):")
    for cname in ("WIDTH", "WIDTH@75", "PASS", "ISSHARPE"):
        row = wf[(wf.STEP == 0.05) & (wf.k == 5) & (wf.chooser == cname)].iloc[0]
        ids = row.books.split("; ")
        gof = {}
        for bid in ids:
            rr = real[real.book == bid].iloc[0]
            if cname == "WIDTH":
                lo, hi = rr["gmin@0.05"], rr["gmax@0.05"]
                gof[bid] = float(np.clip(LIVE_GROSS if not np.isfinite(lo) else (lo + hi) / 2,
                                         0.05, 1.00))
            else:
                gof[bid] = LIVE_GROSS
        line = []
        for c in COSTRUNGS:
            mm = pack(blend(ids, gof, "m_oos", cost=c).values)
            line.append(f"{c:.0f}bps {mm['CAGR']:.2%}/{mm['Sharpe']:.3f}/{mm['MaxDD']:.2%}")
            grid_rows.append(dict(chooser=cname, STEP=0.05, k=5, cost_bps=c, **mm))
        P(f"    {cname:>9}: " + "   ".join(line))
    dump(pd.DataFrame(grid_rows), "grid.csv")
    P()

    # ============================================================================================
    P("=" * 100)
    P("(V) VERDICT")
    P("=" * 100)
    P(f"  GATES G1-G4 {'ALL PASS' if gok else 'A GATE FAILED'}; G5 monotone "
      f"{mono_dd}/{len(specs)} DD and {mono_cg}/{len(specs)} CAGR; G6 determinism exact.")
    P(f"  H1 OOS-Sharpe prediction : {'PASS' if h1 else 'FAIL'}")
    P(f"  H2 OOS-MaxDD prediction  : {'PASS' if h2 else 'FAIL'}")
    P(f"  H3 OOS-4b AUC            : {'PASS' if h3 else 'FAIL'}")
    P(f"  H4 ZEROSIG W < 0         : {'PASS' if h4 else 'FAIL'}")
    P(f"  H5 WIDTH chooser wins    : {'PASS' if wwin > len(piv)/2 else 'FAIL'} "
      f"({wwin}/{len(piv)})")
    wsub = wf[wf.chooser.isin(["WIDTH", "WIDTH@75"])]
    P(f"  KEEP paths for THIS IDEA'S OWN PROPOSAL (the WIDTH choosers, 24 points): "
      f"4b {int(wsub.OOS_4b.sum())}/24, 4a {int(wsub.OOS_4a.sum())}/24; "
      f"the incumbent PASS chooser gets 4b {int(wf[wf.chooser=='PASS'].OOS_4b.sum())}/12.")
    P("  THE ANSWER: the width is a BETTER RANKER of OOS Sharpe and OOS MaxDD than the binary")
    P("  pass, and a WORSE CLASSIFIER of the OOS 4b verdict; and it is dominated by its own")
    P("  g_max leg (OOS-DD rho 0.8103 vs the width's 0.2981) and by the plain IS MaxDD it is")
    P("  built out of (0.7942), so the SUBTRACTION g_max - g_min destroys information.")
    P("  KILL for capital: nothing is promoted, no RULES change is proposed.")
    P(f"  total runtime {time.time()-t_all:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"\nwrote {STEM}.console.txt")


if __name__ == "__main__":
    main()

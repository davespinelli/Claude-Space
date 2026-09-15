#!/usr/bin/env python3
"""Idea 924 (lane C, 2026-09-15) -- is the U56 EQUAL-WEIGHT INDEX's +0.2006 Sharpe EDGE over SPY
in the 2009-2013 leg window a COMPOSITION fact (the panel carries 36 ETFs, 12 of them not even
equity) or a WEIGHTING / SIZE fact?

WHY THIS MATTERS.  Idea 922's whole 2x2 is a set of DEDUCTIONS from one number: on U56, in the
leg window (ISH1_HALF, 2009-01-13 .. 2013-01-07, 1,003 days), at g=0.75 and 10 bps, `EWALL`
-- equal weight every priced name in the panel -- reads Sharpe 1.0384 against SPY's 0.8378,
i.e. +0.2006.  The eligibility filter then gives back -0.1953 and concentration -0.1130.  If the
+0.2006 is made by the PANEL (a 56-name list that is 43% equity ETFs, 21% bonds/gold/commodities
and only 36% single stocks) rather than by any rule, then the record's U56 "headroom" is a
property of a universe file, not of anything promotable, and every deduction from it inherits
that.  This run decomposes the +0.2006 and reports the share.

THE TWO TUNED PARAMETERS (the queue's own; every level reported, nothing hidden):
  TUNED 1  SLEEVE, 8 levels -- ALL56 (= 922's EWALL), ALL55 (SPY dropped as a constituent),
           ETF36, SINGLE20 (the mega-caps), EQ44 (equities only: equity ETFs + singles),
           EQETF24, NONEQ12 (bonds / fx / commodities), SPYONLY (the exposure control).
           The three-way partition EQETF24 + SINGLE20 + NONEQ12 == ALL56 is gated (G6).
  TUNED 2  WEIGHTING, 3 levels -- EW (equal), IVOL (inverse 60d vol), VT (EW scaled to SPY's
           own trailing 60d vol, never levered).
Everything else is a reported constant: g=0.75 headline plus a 20-rung no-leverage gross ladder,
costs {0, 10, 25, 50} bps, weekly cadence, t+1 execution, 260-day warm-up, IS/OOS 2016-12-31.

PRE-REGISTERED HYPOTHESES (bars fixed before the numbers were read):
  H_PANEL    composition carries the edge: the non-equity sleeve's Shapley share of the +0.2006
             is >= 0.50.  (If it is, the headroom is the universe file.)
  H_SIZE     equal-weighting / size inside US large caps carries it: RSP (the equal-weight S&P
             500, a TRADED instrument already in the panel) beats SPY by >= 0.10 of the 0.2006
             in the leg window, i.e. >= 50% of the gap comes from re-weighting the same 500 names.
  H_SINGLES  the mega-cap single-name sleeve is the carrier: SINGLE20/EW beats SPY in the leg
             window by >= 0.10.
  H_ROBUST   whatever carries it in the leg window carries it in >= 10 of the 14 sub-windows.
  H_KEEP     some (sleeve, weighting) cell clears PROTOCOL 4b on FULL, IS and OOS.

GATES (a failure is published, never relaxed):
  G1  the fast runner == `engine.backtest` (returns and turnover) on ALL56/EW at g=0.75.
  G2  CROSS-RUN: idea 922's published leg-window numbers -- EWALL 1.0384, SPY 0.8378, +0.2006.
  G3  the committed U56 FULL triples: SPY (0.1516, 0.8861, -0.3372), RULES v2 (0.0863, 1.2018,
      -0.1205) -- idea 670/675, re-read here.
  G4  the leg window is 922's: 2009-01-13 .. 2013-01-07, 1,003 days.
  G5  the Shapley values over the three sleeves sum to the total edge (residual < 1e-12).
  G6  the sleeve partition is exhaustive and disjoint against research/universe.json.
  G7  Sharpe's scale-freeness on this panel: max |dSharpe| across the 20-rung gross ladder.

SURVIVORSHIP: U56 is a current-constituent list (research/universe.json), so every CAGR and
drawdown LEVEL is optimistic.  The decomposition is a same-days contrast between sub-panels of
one list, far less exposed; the verdicts against SPY are levels read against an index that is
not survivorship-inflated, so those are upper bounds.  Stated, not hidden.

Run: python3 research/backtests/2026-09-15_is-the-U56-EW-INDEX-s-PLUS-0.2006-EDGE-over-SPY-a-COMPOSITION-fact_C.py
"""
from __future__ import annotations

import itertools
import json
import math
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
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

# ---- reported constants (never tuned) ---------------------------------------------------------
COST0 = 10.0
FREQ = "W"
LAG = 1
WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
PUBLISHED_G = 0.75
VOL_WIN = 60                       # the IVOL / VT lookback, one constant shared by both arms
GROSS20 = [round(0.05 * i, 4) for i in range(1, 21)]      # 0.05 .. 1.00, PROTOCOL 2: no leverage
COSTS = [0.0, 10.0, 25.0, 50.0]

# idea 922's committed leg-window readings (U56, g=0.75, 10 bps, ISH1_HALF)
G2_EWALL, G2_SPY, G2_EDGE = 1.0384, 0.8378, 0.2006
G2_TOL = 0.005
SPY_U56 = (0.1516, 0.8861, -0.3372)      # committed triple, idea 670/675
V2_U56 = (0.0863, 1.2018, -0.1205)
TOL_C, TOL_S, TOL_D = 0.004, 0.030, 0.015
LEG_FIRST, LEG_LAST, LEG_N = "2009-01-13", "2013-01-07", 1003

# pre-registered bars
BAR_PANEL_SHARE = 0.50
BAR_SIZE = 0.10
BAR_SINGLES = 0.10
BAR_ROBUST = 10

WEIGHTINGS = ["EW", "IVOL", "VT"]
SLEEVES = ["ALL56", "ALL55", "ETF36", "SINGLE20", "EQ44", "EQETF24", "NONEQ12", "SPYONLY"]

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
# runner (the record's vectorised equivalent of engine.backtest; gated at G1)
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
        m_full = np.asarray(self.idx >= self.start)
        yr = self.idx.year
        w = {"FULL": m_full,
             "IS": m_full & np.asarray(self.idx <= pd.Timestamp(IS_END)),
             "OOS": np.asarray(self.idx >= pd.Timestamp(OOS_START))}
        ispos = np.flatnonzero(w["IS"])
        h = len(ispos) // 2
        ish1 = np.zeros(T, bool); ish1[ispos[:h]] = True
        ish2 = np.zeros(T, bool); ish2[ispos[h:]] = True
        w["ISH1_HALF"], w["ISH2_HALF"] = ish1, ish2          # 922's leg window is ISH1_HALF
        w["CAL0912"] = m_full & (yr >= 2009) & (yr <= 2012)
        w["CAL0910"] = m_full & (yr >= 2009) & (yr <= 2010)
        w["CAL1112"] = m_full & (yr >= 2011) & (yr <= 2012)
        w["CAL1316"] = m_full & (yr >= 2013) & (yr <= 2016)
        for y in range(2009, 2017):
            w[f"Y{y}"] = m_full & (yr == y)
        self.masks = w
        self.spy = px["SPY"].pct_change().fillna(0.0).values


SUBWINS = ["ISH1_HALF", "ISH2_HALF", "CAL0912", "CAL0910", "CAL1112", "CAL1316"] + \
          [f"Y{y}" for y in range(2009, 2017)]
WINDOWS = ["FULL", "IS", "OOS"] + SUBWINS
LEG = "ISH1_HALF"


class Book:
    """One book's gross-1.0 weights, pre-reduced so any (gross, cost) costs O(T).

    Rows of W1 may sum to LESS than 1 (the VT arm de-grosses); the drift algebra below carries
    the cash leg exactly as engine.backtest does (gated at G1 on a full-gross book and at G1b
    on a VT book)."""

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
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(r[:h]), H2=fsharpe(r[h:]),
                mu=float(np.mean(r) * 252.0), sd=float(np.std(r, ddof=1) * np.sqrt(252.0)))


def pass4b(s, spy):
    """PROTOCOL 4b, window-local form used by the record's rule-8 runs."""
    return dict(L1_H1=bool(s["H1"] > spy["H1"]), L2_H2=bool(s["H2"] > spy["H2"]),
                L3_S=bool(s["Sharpe"] > spy["Sharpe"]),
                L4_DDcap=bool(s["MaxDD"] >= DD_CAP * spy["MaxDD"]),
                L5_CAGRfloor=bool(s["CAGR"] >= CAGR_FLOOR * spy["CAGR"]))


def pass4a(s, base):
    return bool(s["H1"] > base["H1"] and s["H2"] > base["H2"] and s["MaxDD"] >= base["MaxDD"])


# ================================================================================================
# the sleeves and the weightings
# ================================================================================================
def sleeve_cols(px):
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    have = list(px.columns)
    g = {k: [t for t in v if t in have] for k, v in U.items()}
    eqetf = g["broad"] + g["sectors"]
    single = g["megacap"]
    noneq = g["bonds_fx_commod"]
    d = {
        "ALL56": have,
        "ALL55": [c for c in have if c != "SPY"],
        "ETF36": eqetf + noneq,
        "SINGLE20": single,
        "EQ44": eqetf + single,
        "EQETF24": eqetf,
        "NONEQ12": noneq,
        "SPYONLY": ["SPY"],
    }
    return d, eqetf, single, noneq


def w_ew(px, cols):
    e = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    e[cols] = px[cols].notna().astype(float)
    return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0).values


def w_ivol(px, cols):
    vol = px.pct_change().rolling(VOL_WIN).std() * math.sqrt(252.0)
    iv = (1.0 / vol.clip(lower=0.02))
    e = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    e[cols] = iv[cols].where(px[cols].notna()).fillna(0.0)
    e = e.where(e > 0, 0.0)
    W = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    # before VOL_WIN closes exist, fall back to equal weight so the arm is defined everywhere
    ewf = pd.DataFrame(w_ew(px, cols), index=px.index, columns=px.columns)
    return W.where(W.sum(axis=1).gt(0.0), ewf).values


def w_vt(px, cols):
    """EW scaled so the book's own trailing-60d vol matches SPY's; never levered (scaler <= 1)."""
    EW = w_ew(px, cols)
    rets = px.pct_change().fillna(0.0).values
    pr = pd.Series((EW * rets).sum(axis=1), index=px.index)
    bv = pr.rolling(VOL_WIN).std() * math.sqrt(252.0)
    sv = px["SPY"].pct_change().rolling(VOL_WIN).std() * math.sqrt(252.0)
    sc = (sv / bv.clip(lower=1e-6)).clip(upper=1.0).fillna(1.0).values
    return EW * sc[:, None]


WFN = {"EW": w_ew, "IVOL": w_ivol, "VT": w_vt}


# ================================================================================================
def main():
    P("=" * 96)
    P("IDEA 924 (lane C, 2026-09-15) -- is the U56 EQUAL-WEIGHT INDEX's +0.2006 EDGE over SPY")
    P("a COMPOSITION fact?   TUNED: sleeve (8) x weighting (3).  All levels reported.")
    P("=" * 96)

    px = load_universe()
    pan = Panel("U56", px)
    cols, eqetf, single, noneq = sleeve_cols(px)
    P(f"\nPanel U56: {px.shape[1]} columns, {px.shape[0]:,} days "
      f"{px.index[0].date()} .. {px.index[-1].date()}")
    for k in SLEEVES:
        P(f"  {k:<9} n={len(cols[k]):>3}  {', '.join(cols[k][:8])}{' ...' if len(cols[k]) > 8 else ''}")

    legmask = pan.masks[LEG]
    legidx = pan.idx[legmask]
    P(f"\nLeg window ({LEG}): {legidx[0].date()} .. {legidx[-1].date()}  ({legmask.sum():,} days)")

    # ---- books -------------------------------------------------------------------------------
    books = {}
    for sl, wg in itertools.product(SLEEVES, WEIGHTINGS):
        books[(sl, wg)] = Book(pan, WFN[wg](px, cols[sl]))
    P(f"\nBuilt {len(books)} books ({len(SLEEVES)} sleeves x {len(WEIGHTINGS)} weightings).")

    # SPY buy-and-hold reference (unlevered, no costs -- the PROTOCOL comparand) ---------------
    spyref = {w: pack(pan.spy[pan.masks[w]]) for w in WINDOWS}
    v2 = backtest(px, rules_v2_weights(px), cost_bps=COST0, freq=FREQ)["returns"].values
    v2ref = {w: pack(v2[pan.masks[w]]) for w in WINDOWS}

    # ================================ GATES ====================================================
    gates = []
    W1 = WFN["EW"](px, cols["ALL56"])
    ref = backtest(px, pd.DataFrame(PUBLISHED_G * W1, index=px.index, columns=px.columns),
                   cost_bps=COST0, freq=FREQ)
    mfull = pan.masks["FULL"]      # engine.backtest's row 0 is NaN by construction (it shifts the
    # already-filled weight frame), so the comparison is made on the post-warm-up window that every
    # reported statistic in this run uses -- same convention as idea 922's G1.
    fr, ft = books[("ALL56", "EW")].at(PUBLISHED_G, COST0)
    d1 = float(np.abs(fr[mfull] - ref["returns"].values[mfull]).max())
    d1t = float(np.abs(ft[mfull] - ref["turnover"].values[mfull]).max())
    gates.append(dict(gate="G1 fast runner == engine.backtest (ALL56/EW @ g=0.75, FULL window)",
                      stat=f"max|dret| {d1:.3e}  max|dturn| {d1t:.3e}", passed=bool(d1 < 1e-12 and d1t < 1e-12)))

    W1v = WFN["VT"](px, cols["ALL56"])
    refv = backtest(px, pd.DataFrame(PUBLISHED_G * W1v, index=px.index, columns=px.columns),
                    cost_bps=COST0, freq=FREQ)
    frv, ftv = books[("ALL56", "VT")].at(PUBLISHED_G, COST0)
    d1b = float(np.abs(frv[mfull] - refv["returns"].values[mfull]).max())
    gates.append(dict(gate="G1b fast runner == engine.backtest on a DE-GROSSED book (ALL56/VT)",
                      stat=f"max|dret| {d1b:.3e}", passed=bool(d1b < 1e-12)))

    s_ewall = pack(books[("ALL56", "EW")].at(PUBLISHED_G, COST0)[0][legmask])
    edge = s_ewall["Sharpe"] - spyref[LEG]["Sharpe"]
    ok2 = (abs(s_ewall["Sharpe"] - G2_EWALL) < G2_TOL and abs(spyref[LEG]["Sharpe"] - G2_SPY) < G2_TOL
           and abs(edge - G2_EDGE) < G2_TOL)
    gates.append(dict(gate="G2 CROSS-RUN: idea 922's leg-window EWALL / SPY / edge",
                      stat=f"EWALL {s_ewall['Sharpe']:.4f} vs {G2_EWALL}; SPY {spyref[LEG]['Sharpe']:.4f} "
                           f"vs {G2_SPY}; edge {edge:+.4f} vs {G2_EDGE:+.4f}", passed=bool(ok2)))

    c, s, d = fmet(pan.spy[pan.masks["FULL"]])
    c2, s2, d2 = fmet(v2[pan.masks["FULL"]])
    ok3 = (abs(c - SPY_U56[0]) < TOL_C and abs(s - SPY_U56[1]) < TOL_S and abs(d - SPY_U56[2]) < TOL_D
           and abs(c2 - V2_U56[0]) < TOL_C and abs(s2 - V2_U56[1]) < TOL_S and abs(d2 - V2_U56[2]) < TOL_D)
    gates.append(dict(gate="G3 committed U56 FULL triples (SPY, RULES v2)",
                      stat=f"SPY {c:.4f}/{s:.4f}/{d:.4f} vs {SPY_U56}; v2 {c2:.4f}/{s2:.4f}/{d2:.4f} vs {V2_U56}",
                      passed=bool(ok3)))

    ok4 = (str(legidx[0].date()) == LEG_FIRST and str(legidx[-1].date()) == LEG_LAST
           and int(legmask.sum()) == LEG_N)
    gates.append(dict(gate="G4 leg window is 922's",
                      stat=f"{legidx[0].date()} .. {legidx[-1].date()}  n={legmask.sum()} "
                           f"vs {LEG_FIRST} .. {LEG_LAST} n={LEG_N}", passed=bool(ok4)))

    part = sorted(eqetf + single + noneq)
    ok6 = (part == sorted(cols["ALL56"]) and len(set(eqetf) & set(single)) == 0
           and len(set(eqetf) & set(noneq)) == 0 and len(set(single) & set(noneq)) == 0)
    gates.append(dict(gate="G6 sleeve partition exhaustive and disjoint",
                      stat=f"|EQETF24|={len(eqetf)} + |SINGLE20|={len(single)} + |NONEQ12|={len(noneq)} "
                           f"= {len(part)} vs |ALL56|={len(cols['ALL56'])}", passed=bool(ok6)))

    lad = [pack(books[("ALL56", "EW")].at(g, COST0)[0][legmask])["Sharpe"] for g in GROSS20]
    g7 = float(max(lad) - min(lad))
    gates.append(dict(gate="G7 Sharpe scale-freeness over the 20-rung gross ladder (ALL56/EW, leg)",
                      stat=f"max-min {g7:.4f} over g in [0.05, 1.00] at 10 bps", passed=bool(g7 < 0.05)))

    # ================================ the grid =================================================
    P("\n" + "=" * 96)
    P(f"THE GRID -- {len(SLEEVES)} sleeves x {len(WEIGHTINGS)} weightings, every cell reported")
    P("=" * 96)
    rows = []
    for (sl, wg), bk in books.items():
        for cost in COSTS:
            for g in GROSS20:
                r, turn = bk.at(g, cost)
                for w in WINDOWS:
                    s = pack(r[pan.masks[w]])
                    sp, bs = spyref[w], v2ref[w]
                    legs = pass4b(s, sp)
                    rows.append(dict(sleeve=sl, weighting=wg, gross=g, cost=cost, window=w,
                                     n=int(pan.masks[w].sum()), CAGR=s["CAGR"], Sharpe=s["Sharpe"],
                                     MaxDD=s["MaxDD"], H1=s["H1"], H2=s["H2"], vol=s["sd"],
                                     spySharpe=sp["Sharpe"], edge=s["Sharpe"] - sp["Sharpe"],
                                     turnover=float(turn[pan.masks[w]].sum() / (pan.masks[w].sum() / 252.0)),
                                     **legs, pass4b=bool(all(legs.values())), pass4a=pass4a(s, bs)))
    grid = pd.DataFrame(rows)
    dump(grid, "grid.csv")

    hl = grid[(grid.gross == PUBLISHED_G) & (grid.cost == COST0) & (grid.window == LEG)]
    hl = hl.set_index(["sleeve", "weighting"]).sort_index()
    P(f"\nLEG WINDOW ({LEG}, {LEG_N} days, g={PUBLISHED_G}, {COST0:.0f} bps) "
      f"-- SPY Sharpe {spyref[LEG]['Sharpe']:.4f}, vol {spyref[LEG]['sd']:.2%}, CAGR {spyref[LEG]['CAGR']:.2%}")
    P(f"{'sleeve':<9} {'wgt':<5} {'Sharpe':>8} {'edge':>9} {'CAGR':>8} {'vol':>7} {'MaxDD':>8}")
    for (sl, wg), r in hl.iterrows():
        P(f"{sl:<9} {wg:<5} {r.Sharpe:>8.4f} {r.edge:>+9.4f} {r.CAGR:>8.2%} {r.vol:>7.2%} {r.MaxDD:>8.2%}")

    # ================================ the decomposition ========================================
    P("\n" + "=" * 96)
    P("DECOMPOSITION 1 -- SHAPLEY over the three disjoint sleeves (order-independent)")
    P("=" * 96)
    parts = {"EQETF24": eqetf, "SINGLE20": single, "NONEQ12": noneq}
    names = list(parts)
    vsub = {}
    for k in range(1, 4):
        for comb in itertools.combinations(names, k):
            c_ = sorted(set().union(*[parts[x] for x in comb]))
            bkc = Book(pan, w_ew(px, c_))
            for wname in [LEG] + [w for w in WINDOWS if w != LEG]:
                vsub[(comb, wname)] = pack(bkc.at(PUBLISHED_G, COST0)[0][pan.masks[wname]])["Sharpe"] \
                    - spyref[wname]["Sharpe"]
    srows = []
    for wname in WINDOWS:
        v = {(): 0.0}
        for k in range(1, 4):
            for comb in itertools.combinations(names, k):
                v[comb] = vsub[(comb, wname)]
        phi = {}
        for i in names:
            tot = 0.0
            others = [x for x in names if x != i]
            for k in range(0, 3):
                for S in itertools.combinations(others, k):
                    wgt = math.factorial(k) * math.factorial(2 - k) / math.factorial(3)
                    a = tuple(x for x in names if x in set(S) | {i})
                    b = tuple(x for x in names if x in set(S))
                    tot += wgt * (v[a] - v[b])
            phi[i] = tot
        total = v[tuple(names)]
        srows.append(dict(window=wname, total_edge=total, **{f"phi_{k}": phi[k] for k in names},
                          residual=total - sum(phi.values()),
                          **{f"share_{k}": (phi[k] / total if total else np.nan) for k in names}))
    sh = pd.DataFrame(srows)
    dump(sh, "shapley.csv")
    resid = float(sh.residual.abs().max())
    gates.append(dict(gate="G5 Shapley values sum to the total edge (all windows)",
                      stat=f"max |residual| {resid:.3e}", passed=bool(resid < 1e-12)))
    shl = sh[sh.window == LEG].iloc[0]
    P(f"Leg window total edge {shl.total_edge:+.4f}   =   "
      f"EQETF24 {shl.phi_EQETF24:+.4f} + SINGLE20 {shl.phi_SINGLE20:+.4f} + NONEQ12 {shl.phi_NONEQ12:+.4f}"
      f"   (residual {shl.residual:.1e})")
    P(f"Shares: EQETF24 {shl.share_EQETF24:6.1%}   SINGLE20 {shl.share_SINGLE20:6.1%}   "
      f"NONEQ12 {shl.share_NONEQ12:6.1%}")
    P("\nShapley by window (share of that window's own total edge):")
    P(f"{'window':<11} {'total':>8} {'EQETF24':>9} {'SINGLE20':>9} {'NONEQ12':>9}  "
      f"{'sh_EQ':>7} {'sh_SG':>7} {'sh_NE':>7}")
    for _, r in sh.iterrows():
        P(f"{r.window:<11} {r.total_edge:>+8.4f} {r.phi_EQETF24:>+9.4f} {r.phi_SINGLE20:>+9.4f} "
          f"{r.phi_NONEQ12:>+9.4f}  {r.share_EQETF24:>7.1%} {r.share_SINGLE20:>7.1%} {r.share_NONEQ12:>7.1%}")

    # ---- DECOMPOSITION 2: the chain (weighting/size -> equity breadth -> non-equity) ----------
    P("\n" + "=" * 96)
    P("DECOMPOSITION 2 -- the CHAIN: weighting/size (RSP vs SPY, a TRADED instrument) ->")
    P("                   equity breadth (EQ44/EW vs RSP) -> non-equity sleeve (ALL56 vs EQ44)")
    P("=" * 96)
    rsp = pd.Series(px["RSP"].pct_change().fillna(0.0).values, index=px.index)
    crows = []
    for wname in WINDOWS:
        m = pan.masks[wname]
        s_spy = spyref[wname]["Sharpe"]
        s_rsp = fsharpe(rsp.values[m])
        s_eq44 = pack(books[("EQ44", "EW")].at(PUBLISHED_G, COST0)[0][m])["Sharpe"]
        s_all = pack(books[("ALL56", "EW")].at(PUBLISHED_G, COST0)[0][m])["Sharpe"]
        # reverse order: non-equity first, then breadth, then weighting
        s_spy_plus_noneq = pack(Book(pan, w_ew(px, ["SPY"] + noneq)).at(PUBLISHED_G, COST0)[0][m])["Sharpe"]
        crows.append(dict(window=wname, SPY=s_spy, RSP=s_rsp, EQ44=s_eq44, ALL56=s_all,
                          A_weight_size=s_rsp - s_spy, B_equity_breadth=s_eq44 - s_rsp,
                          C_nonequity=s_all - s_eq44, total=s_all - s_spy,
                          rev_A_nonequity=s_spy_plus_noneq - s_spy,
                          rev_rest=s_all - s_spy_plus_noneq))
    ch = pd.DataFrame(crows)
    dump(ch, "chain.csv")
    P(f"{'window':<11} {'SPY':>7} {'RSP':>7} {'EQ44':>7} {'ALL56':>7} | {'A size':>8} {'B breadth':>10} "
      f"{'C non-eq':>9} {'total':>8} | {'rev: non-eq 1st':>15} {'rev rest':>9}")
    for _, r in ch.iterrows():
        P(f"{r.window:<11} {r.SPY:>7.3f} {r.RSP:>7.3f} {r.EQ44:>7.3f} {r.ALL56:>7.3f} | "
          f"{r.A_weight_size:>+8.4f} {r.B_equity_breadth:>+10.4f} {r.C_nonequity:>+9.4f} {r.total:>+8.4f} | "
          f"{r.rev_A_nonequity:>+15.4f} {r.rev_rest:>+9.4f}")

    # ---- DECOMPOSITION 3: leave-one-name-out on the leg window --------------------------------
    P("\n" + "=" * 96)
    P("DECOMPOSITION 3 -- LEAVE-ONE-NAME-OUT of EWALL (leg window, g=0.75, 10 bps)")
    P("=" * 96)
    loo = []
    base_leg = s_ewall["Sharpe"]
    for t in cols["ALL56"]:
        rest = [c for c in cols["ALL56"] if c != t]
        sv = pack(Book(pan, w_ew(px, rest)).at(PUBLISHED_G, COST0)[0][legmask])["Sharpe"]
        grp = ("NONEQ12" if t in noneq else "SINGLE20" if t in single else "EQETF24")
        loo.append(dict(ticker=t, sleeve=grp, Sharpe_without=sv, delta=base_leg - sv,
                        solo=fsharpe(px[t].pct_change().fillna(0.0).values[legmask])))
    loodf = pd.DataFrame(loo).sort_values("delta", ascending=False)
    dump(loodf, "leaveoneout.csv")
    P(f"EWALL leg Sharpe {base_leg:.4f}.  delta = how much the name CONTRIBUTES (drop it and lose this).")
    P("  top 8 contributors:   " + ", ".join(f"{r.ticker}({r.sleeve[:3]}) {r.delta:+.4f}"
                                             for _, r in loodf.head(8).iterrows()))
    P("  top 8 detractors:     " + ", ".join(f"{r.ticker}({r.sleeve[:3]}) {r.delta:+.4f}"
                                             for _, r in loodf.tail(8).iterrows()))
    P("  mean |delta| by sleeve: " + ", ".join(
        f"{k} {v:.4f}" for k, v in loodf.groupby('sleeve').delta.apply(lambda x: x.abs().mean()).items()))

    # ---- DECOMPOSITION 4: the survivorship read -----------------------------------------------
    P("\n" + "=" * 96)
    P("DECOMPOSITION 4 -- the SURVIVORSHIP read: SINGLE20/EW (20 names that are mega-caps in 2026,")
    P("held from 2009) against RSP (equal-weight S&P 500, a TRADED instrument, no survivorship)")
    P("=" * 96)
    srv = []
    for wname in WINDOWS:
        m = pan.masks[wname]
        s_single = pack(books[("SINGLE20", "EW")].at(PUBLISHED_G, COST0)[0][m])["Sharpe"]
        s_rsp = fsharpe(rsp.values[m])
        s_spy = spyref[wname]["Sharpe"]
        srv.append(dict(window=wname, SINGLE20=s_single, RSP=s_rsp, SPY=s_spy,
                        weighting_leg=s_rsp - s_spy, selection_leg=s_single - s_rsp,
                        total=s_single - s_spy))
    sv = pd.DataFrame(srv)
    dump(sv, "survivorship.csv")
    P(f"{'window':<11} {'SINGLE20':>9} {'RSP':>7} {'SPY':>7} | {'weighting/size':>15} "
      f"{'selection':>10} {'total':>8}")
    for _, r in sv.iterrows():
        P(f"{r.window:<11} {r.SINGLE20:>9.3f} {r.RSP:>7.3f} {r.SPY:>7.3f} | {r.weighting_leg:>+15.4f} "
          f"{r.selection_leg:>+10.4f} {r.total:>+8.4f}")

    # ================================ hypotheses ===============================================
    P("\n" + "=" * 96)
    P("PRE-REGISTERED HYPOTHESES")
    P("=" * 96)
    hyps = []
    share_ne = float(shl.share_NONEQ12)
    hyps.append(dict(h="H_PANEL non-equity sleeve Shapley share >= 0.50",
                     stat=f"share {share_ne:.1%} (phi {shl.phi_NONEQ12:+.4f} of {shl.total_edge:+.4f})",
                     passed=bool(share_ne >= BAR_PANEL_SHARE)))
    a_size = float(ch[ch.window == LEG].A_weight_size.iloc[0])
    hyps.append(dict(h=f"H_SIZE RSP - SPY >= {BAR_SIZE} in the leg window",
                     stat=f"{a_size:+.4f} ({a_size / G2_EDGE:.1%} of the +0.2006)",
                     passed=bool(a_size >= BAR_SIZE)))
    e_single = float(hl.loc[("SINGLE20", "EW")].edge)
    hyps.append(dict(h=f"H_SINGLES SINGLE20/EW edge over SPY >= {BAR_SINGLES} in the leg window",
                     stat=f"{e_single:+.4f}", passed=bool(e_single >= BAR_SINGLES)))
    sub = grid[(grid.gross == PUBLISHED_G) & (grid.cost == COST0) & (grid.window.isin(SUBWINS))]
    carrier = "NONEQ12" if share_ne >= max(float(shl.share_EQETF24), float(shl.share_SINGLE20)) else \
              ("EQETF24" if float(shl.share_EQETF24) >= float(shl.share_SINGLE20) else "SINGLE20")
    shsub = sh[sh.window.isin(SUBWINS)]
    nrob = int((shsub[f"phi_{carrier}"] > 0).sum())
    hyps.append(dict(h=f"H_ROBUST the leg-window carrier ({carrier}) has phi > 0 in >= {BAR_ROBUST} of 14 sub-windows",
                     stat=f"{nrob} of {len(shsub)}", passed=bool(nrob >= BAR_ROBUST)))
    keepcells = grid[(grid.cost == COST0) & (grid.window.isin(["FULL", "IS", "OOS"])) & grid.pass4b]
    kc = keepcells.groupby(["sleeve", "weighting", "gross"]).window.nunique()
    kc3 = kc[kc == 3]
    hyps.append(dict(h="H_KEEP some (sleeve, weighting, gross) clears 4b on FULL, IS and OOS",
                     stat=f"{len(kc3)} of {len(SLEEVES) * len(WEIGHTINGS) * len(GROSS20)} cells",
                     passed=bool(len(kc3) > 0)))
    hy = pd.DataFrame(hyps)
    dump(hy, "hypotheses.csv")
    for _, r in hy.iterrows():
        P(f"  [{'PASS' if r.passed else 'FAIL'}] {r.h}\n         {r.stat}")

    # ================================ rule 8 ===================================================
    P("\n" + "=" * 96)
    P("RULE 8 WALK-FORWARD -- (sleeve, weighting) chosen on 2009-2016 ONLY, 2017-2026 read once")
    P("=" * 96)
    gsel = grid[(grid.cost == COST0)]
    isd = gsel[gsel.window == "IS"].set_index(["sleeve", "weighting", "gross"])
    oosd = gsel[gsel.window == "OOS"].set_index(["sleeve", "weighting", "gross"])
    fulld = gsel[gsel.window == "FULL"].set_index(["sleeve", "weighting", "gross"])
    sp_oos, sp_is = spyref["OOS"], spyref["IS"]
    b_oos = v2ref["OOS"]
    P(f"SPY OOS {sp_oos['CAGR']:.2%} / {sp_oos['Sharpe']:.3f} / {sp_oos['MaxDD']:.2%}   "
      f"(4b DD cap {DD_CAP * sp_oos['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR * sp_oos['CAGR']:.2%})")
    P(f"RULES v2 OOS {b_oos['CAGR']:.2%} / {b_oos['Sharpe']:.3f} / {b_oos['MaxDD']:.2%}")

    selectors = {
        "PICK_IS_SHARPE": lambda d: d.Sharpe.idxmax(),
        "PICK_IS_4b_THEN_SHARPE": lambda d: (d[d.pass4b].Sharpe.idxmax() if d.pass4b.any() else d.Sharpe.idxmax()),
        "PICK_IS_CALMAR": lambda d: (d.CAGR / d.MaxDD.abs()).idxmax(),
        "PICK_IS_SHARPE_g075": lambda d: d[d.index.get_level_values("gross") == PUBLISHED_G].Sharpe.idxmax(),
        "PICK_LIVE_EWALL": lambda d: ("ALL56", "EW", PUBLISHED_G),
    }
    wf = []
    for selname, fn in selectors.items():
        for pool, poolname in [(isd, "ALLCELLS"), (isd[isd.index.get_level_values("sleeve") != "SPYONLY"],
                                                   "NO_SPYONLY")]:
            key = fn(pool)
            o, i_, f_ = oosd.loc[key], isd.loc[key], fulld.loc[key]
            wf.append(dict(selector=selname, pool=poolname, sleeve=key[0], weighting=key[1], gross=key[2],
                           IS_Sharpe=i_.Sharpe, IS_4b=bool(i_.pass4b),
                           OOS_CAGR=o.CAGR, OOS_Sharpe=o.Sharpe, OOS_MaxDD=o.MaxDD,
                           OOS_4b=bool(o.pass4b), OOS_4a=bool(o.pass4a),
                           FULL_CAGR=f_.CAGR, FULL_Sharpe=f_.Sharpe, FULL_MaxDD=f_.MaxDD,
                           FULL_4b=bool(f_.pass4b), FULL_4a=bool(f_.pass4a)))
    wfdf = pd.DataFrame(wf)
    dump(wfdf, "walkforward.csv")
    P(f"\n{'selector':<24} {'pool':<11} {'pick':<24} {'IS Sh':>7} | {'OOS CAGR':>9} {'OOS Sh':>7} "
      f"{'OOS DD':>8} {'4b':>4} {'4a':>4}")
    for _, r in wfdf.iterrows():
        P(f"{r.selector:<24} {r.pool:<11} {r.sleeve + '/' + r.weighting + '/' + str(r.gross):<24} "
          f"{r.IS_Sharpe:>7.3f} | {r.OOS_CAGR:>9.2%} {r.OOS_Sharpe:>7.3f} {r.OOS_MaxDD:>8.2%} "
          f"{str(r.OOS_4b):>4} {str(r.OOS_4a):>4}")
    P(f"\nOOS 4b {int(wfdf.OOS_4b.sum())} of {len(wfdf)}, OOS 4a {int(wfdf.OOS_4a.sum())} of {len(wfdf)}")

    # all-window KEEP census
    P("\nKEEP census at 10 bps (every (sleeve, weighting, gross) cell, all 3 windows):")
    cen = grid[(grid.cost == COST0) & grid.window.isin(["FULL", "IS", "OOS"])]
    for w in ["FULL", "IS", "OOS"]:
        cw = cen[cen.window == w]
        P(f"  {w:<5} 4b {int(cw.pass4b.sum()):>3} of {len(cw)}   4a {int(cw.pass4a.sum()):>3} of {len(cw)}")
    if len(kc3):
        P(f"\n  cells clearing 4b on ALL THREE windows ({len(kc3)}):")
        keepr = []
        for (sl, wg, g) in kc3.index:
            f_, i_, o = fulld.loc[(sl, wg, g)], isd.loc[(sl, wg, g)], oosd.loc[(sl, wg, g)]
            keepr.append(dict(sleeve=sl, weighting=wg, gross=g,
                              FULL_CAGR=f_.CAGR, FULL_Sharpe=f_.Sharpe, FULL_MaxDD=f_.MaxDD,
                              FULL_H1=f_.H1, FULL_H2=f_.H2,
                              IS_Sharpe=i_.Sharpe, OOS_CAGR=o.CAGR, OOS_Sharpe=o.Sharpe, OOS_MaxDD=o.MaxDD,
                              FULL_4a=bool(f_.pass4a), OOS_4a=bool(o.pass4a)))
        kdf = pd.DataFrame(keepr).sort_values("FULL_Sharpe", ascending=False)
        dump(kdf, "keep.csv")
        for _, r in kdf.head(20).iterrows():
            P(f"    {r.sleeve:<9} {r.weighting:<5} g={r.gross:<5} FULL {r.FULL_CAGR:>7.2%}/{r.FULL_Sharpe:.3f}/"
              f"{r.FULL_MaxDD:>7.2%} (H {r.FULL_H1:.3f}/{r.FULL_H2:.3f})  OOS {r.OOS_CAGR:>7.2%}/"
              f"{r.OOS_Sharpe:.3f}/{r.OOS_MaxDD:>7.2%}  4a F/O {r.FULL_4a}/{r.OOS_4a}")
    else:
        dump(pd.DataFrame(columns=["sleeve"]), "keep.csv")

    # cost sensitivity of the headline edge
    P("\nCOST SENSITIVITY of the leg-window edge (ALL56/EW minus SPY, g=0.75):")
    for cst in COSTS:
        e = grid[(grid.sleeve == "ALL56") & (grid.weighting == "EW") & (grid.gross == PUBLISHED_G)
                 & (grid.cost == cst) & (grid.window == LEG)].edge.iloc[0]
        P(f"  {cst:>5.0f} bps  edge {e:+.4f}")

    # ================================ gates out ================================================
    P("\n" + "=" * 96)
    P("GATES")
    P("=" * 96)
    gdf = pd.DataFrame(gates)
    dump(gdf, "gates.csv")
    for _, r in gdf.iterrows():
        P(f"  [{'PASS' if r.passed else 'FAIL'}] {r.gate}\n         {r.stat}")
    P(f"\nGATES {int(gdf.passed.sum())} of {len(gdf)} PASS")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"\nwrote {STEM}.console.txt")


if __name__ == "__main__":
    main()

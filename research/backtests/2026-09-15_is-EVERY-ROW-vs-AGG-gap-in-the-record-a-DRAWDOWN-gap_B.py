#!/usr/bin/env python3
"""Idea 662 (lane B, 2026-09-15) -- is EVERY ROW-vs-AGG gap in the record a DRAWDOWN gap?

THE QUESTION (queue, 2026-09-10)
  Idea 655 priced row-level vs aggregate-only resolution live on ONE gate family (the RULES v2
  200d +/-3% band).  It found AGG buys +3.77 pp (U56) and +5.39 pp (B136) of OOS CAGR and pays
  13.27 and 9.43 pp of extra MaxDD, so all six rule-8 picks beat SPY's OOS Sharpe and only the
  WHICH-names modes clear 4b's DD cap.  The queue asks whether that trade -- resolution buys
  drawdown control, aggregation buys return -- is a PROPERTY OF THE RESOLUTION or a property of
  THAT ONE GATE.  Re-run the record's committed gate families split into per-name and
  panel-aggregate form and report whether the resolution premium is ALWAYS paid in drawdown.

THE THREE MODES (identical construction in every family -- this is the whole design)
  ROW  knows WHICH names pass the gate: hold each passing name at gross/N of NAV, N = names
       priced that day, the rest of the book in CASH.  (In the TREND family this IS RULES v2.)
  AGG  knows only HOW MANY pass -- the breadth b_t = (# passing)/(# priced) -- and never which:
       hold the WHOLE priced panel equal-weighted at `gross` when b_t >= theta, else all cash.
  HYB  knows both: the ROW book, switched off entirely on days when b_t < theta.

THE FOUR GATE FAMILIES (per-name thresholds are COMMITTED CONSTANTS or dial-free cross-sectional
statistics -- none of them is tuned here; only theta and gross are tuned, PROTOCOL 4's max of 2)
  TREND  name is inside its own 200d MA +/-3% band          (baseline.band_state, RULES v2 cl.2)
  VOL    name's 20d realised ann. vol < 0.60                (rules_v1_weights' max_vol constant)
  MOM    name's 12-1 momentum px[t-21]/px[t-252] - 1 > 0    (baseline.score's `mom` leg)
  DISP   name's 60d IDIOSYNCRATIC vol (std of r_i - panel mean r) is below the panel's OWN
         cross-sectional MEAN of that statistic that day    (dial-free; breadth moves with the
         cross-sectional skew of dispersion, which is the point of a dispersion gate)

PRE-REGISTERED HYPOTHESES (fixed before any number below was read)
  H1  For EVERY family x panel, the rule-8 AGG pick has HIGHER OOS CAGR than the ROW pick.
  H2  For EVERY family x panel, the rule-8 AGG pick has WORSE OOS MaxDD than the ROW pick.
  H3  Across the whole matched-gross grid, every cell where AGG buys CAGR over ROW also pays
      drawdown ("no free resolution premium").
  H4  4b's DD cap is what separates the modes: ROW/HYB clear it where AGG does not.
  H5  4a passes are ~absent in every family (655 found 3/126).

PROTOCOL
  2  10 bps per unit turnover, weights at close t applied t+1 (LAG=1), weekly, no leverage/shorts.
  3  every book compared to RULES v2 (live) and to SPY buy-and-hold on the same sample.
  4  BOTH KEEP paths evaluated at EVERY grid point; 2 tuned params (theta, gross); family, panel
     and mode are REPORTED AXES, every point published in the .grid.csv.
  8  walk-forward: (theta, gross) fitted on 2009-2016 by IS Sharpe, 2017-2026 read ONCE.
  9  SURVIVORSHIP: all three panels are current-constituent lists; levels are optimistic.

GATES (run and printed BEFORE any result number is read)
  G1  TREND/ROW at gross 0.75 IS baseline.rules_v2_weights (weights and returns).
  G2  fast_run == engine.backtest (returns and turnover) on a representative book.
  G3  AGG at theta=0.00 is the SAME buy-and-hold panel in all four families.
  G4  HYB at theta=0.00 == ROW in every family.
  G5  an always-TRUE per-name gate makes ROW == AGG(theta=0) (the ROW machinery reduces).
  G6  SPY and RULES v2 on U56 reproduce their committed triples (15.16%/0.8861/-33.72% and
      8.63%/1.2018/-12.05%).

Outputs beside this script: .console.txt .grid.csv .walkforward.csv .pairs.csv .result.md
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
COST = 10.0                       # PROTOCOL 2
FREQ = "W"
LAG = 1
BAND = 0.03                       # RULES v2 clause 2
MAXVOL = 0.60                     # rules_v1_weights' committed max_vol
VOLWIN = 20                       # rules_v1/score's vol window
DISPWIN = 60                      # idiosyncratic-vol window
WARMUP = 260                      # the record's warm-up skip
IS_END, OOS_START = "2016-12-31", "2017-01-01"
COSTRUNGS = [0.0, 10.0, 25.0]

# ---- tuned dial 1: the breadth trigger --------------------------------------------------------
THETAS = [0.00, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90]
# ---- tuned dial 2: the gross ladder ----------------------------------------------------------
GROSSES = [0.50, 0.75, 1.00]

FAMILIES = ["TREND", "VOL", "MOM", "DISP"]
MODES = ["ROW", "AGG", "HYB"]

# committed record triples this run must reproduce (G6)
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
    P(f"  wrote {p.name}  ({len(df):,} rows)")


# ================================================================================================
# runner (the record's vectorised equivalent of engine.backtest; gated at G2)
# ================================================================================================
def fast_run(prices, weights, mask, lag=LAG):
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(lag).fillna(0.0).values
    mk = mask.shift(lag, fill_value=False).values.copy()
    mk[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mk)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return pd.Series((held * rets).sum(axis=1), index=idx), pd.Series(turn, index=idx)


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
    """PROTOCOL 4a: Sharpe > live rules in BOTH halves, MaxDD no worse."""
    return bool(s["H1"] > base["H1"] and s["H2"] > base["H2"] and s["MaxDD"] >= base["MaxDD"])


def legs4b(s, spy, oos_sh):
    """PROTOCOL 4b legs, named so a failure can be attributed."""
    return dict(H1=bool(s["H1"] > spy["H1"]), H2=bool(s["H2"] > spy["H2"]),
                OOS=bool(oos_sh > spy["OOS_Sharpe"]),
                DDCAP=bool(s["MaxDD"] >= 0.60 * spy["MaxDD"]),
                CAGRFLOOR=bool(s["CAGR"] >= 0.70 * spy["CAGR"]))


# ================================================================================================
# gate families -> per-name boolean IN(i,t)
# ================================================================================================
def gate_in(px, family):
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
    elif family == "ALLTRUE":                      # G5 control only
        g = pd.DataFrame(True, index=px.index, columns=px.columns)
    else:
        raise ValueError(family)
    return g.fillna(False) & priced


def breadth_of(px, inb):
    priced = px.notna()
    return (inb.sum(axis=1) / priced.sum(axis=1).replace(0, np.nan)).fillna(0.0)


def ew_panel(px, gross):
    priced = px.notna()
    n = priced.sum(axis=1).replace(0, np.nan)
    return gross * priced.astype(float).div(n, axis=0).fillna(0.0)


def book(px, inb, b, mode, theta, gross):
    ew = ew_panel(px, gross)
    if mode == "ROW":
        return ew.where(inb, 0.0)
    on = (b >= theta).astype(float)
    if mode == "AGG":
        return ew.mul(on, axis=0)
    return ew.where(inb, 0.0).mul(on, axis=0)      # HYB


# ================================================================================================
# panels
# ================================================================================================
def load_panels():
    P("=" * 100)
    P("(D) PANELS")
    P("=" * 100)
    panels = {}
    u = load_universe()
    panels[f"U56"] = u
    b = load_universe(broad=True)
    panels["B136"] = b
    s = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    drop = [c for c in s.columns if c in bad]
    s = s.drop(columns=drop)
    panels[f"SMALL{s.shape[1] - 1}"] = s
    P(f"  SMALL: dropped {len(drop)} of {len(meta)} meta tickers with max_1d_move >= 1.0")
    for k, v in panels.items():
        P(f"  {k:10s} {v.shape[1]:4d} cols  {v.index[0].date()} -> {v.index[-1].date()}  "
          f"{len(v):,} rows  (SPY {'in' if 'SPY' in v.columns else 'MISSING'})")
    return panels


# ================================================================================================
# GATES
# ================================================================================================
def gates(panels):
    P()
    P("=" * 100)
    P("(G) GATES -- run before any result number is read")
    P("=" * 100)
    ok = True
    px = panels["U56"]
    mask = rebalance_mask(px.index, FREQ)

    # G1 -- TREND/ROW at 0.75 IS RULES v2
    inb = gate_in(px, "TREND")
    w_row = book(px, inb, breadth_of(px, inb), "ROW", 0.0, 0.75)
    w_v2 = rules_v2_weights(px, band=BAND, gross=0.75)
    dw = float(np.nanmax(np.abs(w_row.values - w_v2.values)))
    r1, t1 = fast_run(px, w_row, mask)
    r2, t2 = fast_run(px, w_v2, mask)
    dr = float(np.nanmax(np.abs((r1 - r2).values)))
    g1 = dw < 1e-12 and dr < 1e-12
    ok &= g1
    P(f"  G1 TREND/ROW(g=0.75) == rules_v2_weights : max|dW| {dw:.3e}  max|dR| {dr:.3e}   "
      f"{'PASS' if g1 else 'FAIL'}")

    # G2 -- fast_run == engine.backtest
    eng = backtest(px, w_row, cost_bps=COST, freq=FREQ)
    fr, ft = fast_run(px, w_row, mask)
    fin = eng["returns"].notna() & np.isfinite(fr)
    dR = float(np.nanmax(np.abs((eng["returns"][fin] - (fr - ft * COST / 1e4)[fin]).values)))
    dT = float(np.nanmax(np.abs((eng["turnover"][fin] - ft[fin]).values)))
    g2 = dR < 1e-12 and dT < 1e-12
    ok &= g2
    P(f"  G2 fast_run == engine.backtest           : max|dR| {dR:.3e}  max|dTurn| {dT:.3e}  "
      f"over {int(fin.sum()):,} finite rows   {'PASS' if g2 else 'FAIL'}")

    # G3 -- AGG(theta=0) identical across families
    ref = None
    worst = 0.0
    for f in FAMILIES:
        i_f = gate_in(px, f)
        w = book(px, i_f, breadth_of(px, i_f), "AGG", 0.00, 1.00)
        if ref is None:
            ref = w
        else:
            worst = max(worst, float(np.nanmax(np.abs(w.values - ref.values))))
    g3 = worst < 1e-15
    ok &= g3
    P(f"  G3 AGG(theta=0) same in all 4 families   : max|dW| {worst:.3e}   "
      f"{'PASS' if g3 else 'FAIL'}")

    # G4 -- HYB(theta=0) == ROW in every family
    worst = 0.0
    for f in FAMILIES:
        i_f = gate_in(px, f)
        b_f = breadth_of(px, i_f)
        worst = max(worst, float(np.nanmax(np.abs(
            book(px, i_f, b_f, "HYB", 0.00, 1.00).values
            - book(px, i_f, b_f, "ROW", 0.00, 1.00).values))))
    g4 = worst < 1e-15
    ok &= g4
    P(f"  G4 HYB(theta=0) == ROW in every family   : max|dW| {worst:.3e}   "
      f"{'PASS' if g4 else 'FAIL'}")

    # G5 -- an always-true gate makes ROW the buy-and-hold panel
    i_t = gate_in(px, "ALLTRUE")
    w_t = book(px, i_t, breadth_of(px, i_t), "ROW", 0.0, 1.00)
    w_bh = book(px, i_t, breadth_of(px, i_t), "AGG", 0.00, 1.00)
    d5 = float(np.nanmax(np.abs(w_t.values - w_bh.values)))
    g5 = d5 < 1e-15
    ok &= g5
    P(f"  G5 ALLTRUE/ROW == AGG(theta=0)           : max|dW| {d5:.3e}   "
      f"{'PASS' if g5 else 'FAIL'}")

    # G6 -- committed triples
    start = px.index[WARMUP]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    v2r, v2t = fast_run(px, rules_v2_weights(px), mask)
    v2 = (v2r - v2t * COST / 1e4).loc[start:]
    hits = []
    for nm, r, tgt in (("SPY", spy, SPY_U56), ("RULES v2", v2, V2_U56)):
        c, s, d = fmet(r)
        good = abs(c - tgt[0]) < TOL_C and abs(s - tgt[1]) < TOL_S and abs(d - tgt[2]) < TOL_D
        hits.append(good)
        P(f"  G6 {nm:9s} U56  {c:7.2%} / {s:.4f} / {d:7.2%}   committed "
          f"{tgt[0]:7.2%} / {tgt[1]:.4f} / {tgt[2]:7.2%}   {'PASS' if good else 'FAIL'}")
    g6 = all(hits)
    ok &= g6
    P(f"  GATES: {'ALL PASS' if ok else 'A GATE FAILED -- results below are reported as suspect'}")
    return ok


# ================================================================================================
# the grid
# ================================================================================================
def run_grid(panels):
    P()
    P("=" * 100)
    P("(A) THE GRID -- 4 families x 3 modes x theta x gross x panel, both KEEP paths at every point")
    P("=" * 100)
    rows, refs = [], {}
    for pname, px in panels.items():
        t0 = time.time()
        mask = rebalance_mask(px.index, FREQ)
        start = px.index[WARMUP]
        keep = px.index >= start
        oos = px.index >= pd.Timestamp(OOS_START)
        isw = px.index <= pd.Timestamp(IS_END)

        spy_full = px["SPY"].pct_change().fillna(0.0)
        spy = pack(spy_full[keep].values)
        spy["OOS_Sharpe"] = fsharpe(spy_full[keep & oos].values)
        spy["OOS_CAGR"], _, spy["OOS_MaxDD"] = fmet(spy_full[keep & oos].values)
        v2r, v2t = fast_run(px, rules_v2_weights(px), mask)
        v2_full = (v2r - v2t * COST / 1e4)
        v2 = pack(v2_full[keep].values)
        v2["OOS_Sharpe"] = fsharpe(v2_full[keep & oos].values)
        v2["OOS_CAGR"], _, v2["OOS_MaxDD"] = fmet(v2_full[keep & oos].values)
        refs[pname] = dict(SPY=spy, V2=v2)

        P(f"  --- {pname} ({px.shape[1]} cols, {start.date()} -> {px.index[-1].date()}) ---")
        P(f"      SPY  CAGR {spy['CAGR']:7.2%}  Sharpe {spy['Sharpe']:.4f}  MaxDD {spy['MaxDD']:7.2%}"
          f"  H1/H2 {spy['H1']:.4f}/{spy['H2']:.4f}  OOS {spy['OOS_CAGR']:7.2%}/{spy['OOS_Sharpe']:.4f}"
          f"/{spy['OOS_MaxDD']:7.2%}")
        P(f"      V2   CAGR {v2['CAGR']:7.2%}  Sharpe {v2['Sharpe']:.4f}  MaxDD {v2['MaxDD']:7.2%}"
          f"  H1/H2 {v2['H1']:.4f}/{v2['H2']:.4f}  OOS {v2['OOS_CAGR']:7.2%}/{v2['OOS_Sharpe']:.4f}"
          f"/{v2['OOS_MaxDD']:7.2%}")
        P(f"      4b bars: DD cap {0.60 * spy['MaxDD']:7.2%}   CAGR floor {0.70 * spy['CAGR']:7.2%}")

        for fam in FAMILIES:
            inb = gate_in(px, fam)
            b = breadth_of(px, inb)
            bk = b[keep]
            P(f"      {fam:5s} breadth: mean {bk.mean():.3f}  p10 {bk.quantile(0.10):.3f}  "
              f"p50 {bk.median():.3f}  p90 {bk.quantile(0.90):.3f}  "
              f"days>=0.50 {float((bk >= 0.50).mean()):.3f}")
            for mode in MODES:
                thetas = [0.00] if mode == "ROW" else THETAS
                for th in thetas:
                    for g in GROSSES:
                        rr, tt = fast_run(px, book(px, inb, b, mode, th, g), mask)
                        full = (rr - tt * COST / 1e4).values
                        m = pack(full[keep])
                        oc, osh, odd = fmet(full[keep & oos])
                        ic, ish, idd = fmet(full[keep & isw])
                        legs = legs4b(m, spy, osh)
                        rows.append(dict(
                            panel=pname, family=fam, mode=mode, theta=th, gross=g, cost=COST,
                            CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                            H1=m["H1"], H2=m["H2"],
                            IS_CAGR=ic, IS_Sharpe=ish, IS_MaxDD=idd,
                            OOS_CAGR=oc, OOS_Sharpe=osh, OOS_MaxDD=odd,
                            turn_x_yr=float(tt[keep].sum()) / (int(keep.sum()) / 252.0),
                            days_on=float((b[keep] >= th).mean()) if mode != "ROW" else 1.0,
                            pass4a=pass4a(m, v2), pass4b=all(legs.values()),
                            fail4b="+".join(k for k, v in legs.items() if not v) or "-"))
        P(f"      ({time.time() - t0:.1f}s)")
    G = pd.DataFrame(rows)
    P()
    P(f"  grid points {len(G):,}   4a {int(G.pass4a.sum())}   4b {int(G.pass4b.sum())}   "
      f"BOTH {int((G.pass4a & G.pass4b).sum())}")
    return G, refs


# ================================================================================================
# (B) the matched contrast: AGG vs ROW at the same gross
# ================================================================================================
def pairs(G):
    P()
    P("=" * 100)
    P("(B) THE MATCHED CONTRAST -- AGG(theta,g) and HYB(theta,g) against ROW(g), same family,")
    P("    same panel, same gross.  H3: every cell that BUYS CAGR also PAYS drawdown.")
    P("=" * 100)
    out = []
    row = G[G["mode"] == "ROW"].set_index(["panel", "family", "gross"])
    for _, r in G[G["mode"] != "ROW"].iterrows():
        base = row.loc[(r.panel, r.family, r.gross)]
        for tag, cc, dd, ss in (("FULL", "CAGR", "MaxDD", "Sharpe"),
                                ("OOS", "OOS_CAGR", "OOS_MaxDD", "OOS_Sharpe")):
            out.append(dict(panel=r.panel, family=r.family, mode=r["mode"], theta=r.theta,
                            gross=r.gross, leg=tag,
                            d_CAGR=r[cc] - base[cc], d_MaxDD=r[dd] - base[dd],
                            d_Sharpe=r[ss] - base[ss],
                            buys_CAGR=bool(r[cc] > base[cc]), pays_DD=bool(r[dd] < base[dd]),
                            row_CAGR=base[cc], row_MaxDD=base[dd], alt_CAGR=r[cc],
                            alt_MaxDD=r[dd]))
    Pr = pd.DataFrame(out)
    # theta=0.00 AGG cells are the buy-and-hold control, kept in the CSV, excluded from the
    # "is the premium paid" census only where the comparison is degenerate (HYB theta=0 == ROW).
    live = Pr[~((Pr["mode"] == "HYB") & (Pr.theta == 0.00))]
    for leg in ("FULL", "OOS"):
        L = live[live.leg == leg]
        for mode in ("AGG", "HYB"):
            M = L[L["mode"] == mode]
            buys = M[M.buys_CAGR]
            free = buys[~buys.pays_DD]
            P(f"  {leg:4s} {mode}: {len(M):4d} cells   buys CAGR over ROW {len(buys):4d}   "
              f"of those, pays DD {len(buys) - len(free):4d}   FREE (buys CAGR, no DD cost) "
              f"{len(free):4d}")
    P()
    P("  by family x panel (OOS leg, AGG only, all thetas/grosses pooled):")
    L = live[(live.leg == "OOS") & (live["mode"] == "AGG")]
    for (pn, fam), M in L.groupby(["panel", "family"]):
        buys = M[M.buys_CAGR]
        free = buys[~buys.pays_DD]
        P(f"    {pn:10s} {fam:5s} n={len(M):3d}  buys {len(buys):3d}  free {len(free):3d}  "
          f"median dCAGR {M.d_CAGR.median():+7.2%}  median dMaxDD {M.d_MaxDD.median():+7.2%}")
    return Pr


# ================================================================================================
# (C) PROTOCOL rule 8
# ================================================================================================
def walkforward(panels, G, refs):
    P()
    P("=" * 100)
    P("(C) PROTOCOL RULE 8 -- (theta, gross) fitted on 2009-2016 by IS Sharpe, 2017-2026 read ONCE")
    P("=" * 100)
    wf = []
    for pname, px in panels.items():
        mask = rebalance_mask(px.index, FREQ)
        start = px.index[WARMUP]
        keep = px.index >= start
        oos = px.index >= pd.Timestamp(OOS_START)
        spy, v2 = refs[pname]["SPY"], refs[pname]["V2"]
        P(f"  --- {pname} ---   SPY OOS {spy['OOS_CAGR']:7.2%}/{spy['OOS_Sharpe']:.4f}/"
          f"{spy['OOS_MaxDD']:7.2%}   V2 OOS {v2['OOS_CAGR']:7.2%}/{v2['OOS_Sharpe']:.4f}/"
          f"{v2['OOS_MaxDD']:7.2%}")
        for fam in FAMILIES:
            inb = gate_in(px, fam)
            b = breadth_of(px, inb)
            for mode in MODES:
                S = G[(G.panel == pname) & (G.family == fam) & (G["mode"] == mode)]
                top = S.IS_Sharpe.max()
                tied = S[np.isclose(S.IS_Sharpe, top, rtol=0, atol=1e-12)]
                pick = S.loc[S.IS_Sharpe.idxmax()]        # grid-order tie convention (idea 846)
                rung = {}
                for c in COSTRUNGS:
                    rr, tt = fast_run(px, book(px, inb, b, mode, pick.theta, pick.gross), mask)
                    fullr = (rr - tt * c / 1e4).values
                    m = pack(fullr[keep])
                    oc, osh, odd = fmet(fullr[keep & oos])
                    legs = legs4b(m, spy, osh)
                    rung[c] = dict(p4a=pass4a(m, v2), p4b=all(legs.values()),
                                   fail="+".join(k for k, v in legs.items() if not v) or "-")
                wf.append(dict(panel=pname, family=fam, mode=mode,
                               pick_theta=float(pick.theta), pick_gross=float(pick.gross),
                               n_tied_IS=int(len(tied)), IS_Sharpe=float(pick.IS_Sharpe),
                               OOS_CAGR=float(pick.OOS_CAGR), OOS_Sharpe=float(pick.OOS_Sharpe),
                               OOS_MaxDD=float(pick.OOS_MaxDD),
                               SPY_OOS_CAGR=spy["OOS_CAGR"], SPY_OOS_Sharpe=spy["OOS_Sharpe"],
                               SPY_OOS_MaxDD=spy["OOS_MaxDD"],
                               V2_OOS_CAGR=v2["OOS_CAGR"], V2_OOS_Sharpe=v2["OOS_Sharpe"],
                               V2_OOS_MaxDD=v2["OOS_MaxDD"],
                               beats_SPY_OOS=bool(pick.OOS_Sharpe > spy["OOS_Sharpe"]),
                               beats_V2_OOS=bool(pick.OOS_Sharpe > v2["OOS_Sharpe"]),
                               full_4a=bool(pick.pass4a), full_4b=bool(pick.pass4b),
                               fail4b=pick.fail4b,
                               p4b_0=rung[0.0]["p4b"], p4b_10=rung[10.0]["p4b"],
                               p4b_25=rung[25.0]["p4b"], p4a_10=rung[10.0]["p4a"]))
                P(f"      {fam:5s} {mode:4s} pick th={pick.theta:.2f} g={pick.gross:.2f} "
                  f"(IS Sh {pick.IS_Sharpe:.4f}, {len(tied)} tied) -> OOS {pick.OOS_CAGR:7.2%} / "
                  f"{pick.OOS_Sharpe:.4f} / {pick.OOS_MaxDD:7.2%}   4a {'Y' if pick.pass4a else 'n'}"
                  f" 4b {'Y' if pick.pass4b else 'n'} [{pick.fail4b}]   "
                  f"4b@0/10/25 {int(rung[0.0]['p4b'])}/{int(rung[10.0]['p4b'])}/{int(rung[25.0]['p4b'])}")
    W = pd.DataFrame(wf)
    P()
    P("  rule-8 picks: AGG vs ROW, per family x panel (the queue's question, out of sample)")
    P(f"  {'panel':10s} {'family':6s} {'ROW OOS CAGR/MaxDD':>26s} {'AGG OOS CAGR/MaxDD':>26s} "
      f"{'dCAGR':>8s} {'dMaxDD':>8s}  H1  H2")
    h1n = h2n = tot = 0
    for (pn, fam), M in W.groupby(["panel", "family"]):
        r = M[M["mode"] == "ROW"].iloc[0]
        a = M[M["mode"] == "AGG"].iloc[0]
        dc, dd = a.OOS_CAGR - r.OOS_CAGR, a.OOS_MaxDD - r.OOS_MaxDD
        tot += 1
        h1n += dc > 0
        h2n += dd < 0
        P(f"  {pn:10s} {fam:6s} {r.OOS_CAGR:12.2%} / {r.OOS_MaxDD:9.2%} "
          f"{a.OOS_CAGR:12.2%} / {a.OOS_MaxDD:9.2%} {dc:+8.2%} {dd:+8.2%}  "
          f"{'Y' if dc > 0 else 'n'}   {'Y' if dd < 0 else 'n'}")
    P(f"  H1 (AGG buys OOS CAGR)      : {h1n}/{tot}")
    P(f"  H2 (AGG pays OOS drawdown)  : {h2n}/{tot}")
    return W


# ================================================================================================
def verdict(G, Pr, W):
    P()
    P("=" * 100)
    P("(V) HYPOTHESES AND VERDICT")
    P("=" * 100)
    tot = W.groupby(["panel", "family"]).ngroups
    h1 = h2 = 0
    for (_, _), M in W.groupby(["panel", "family"]):
        r = M[M["mode"] == "ROW"].iloc[0]
        a = M[M["mode"] == "AGG"].iloc[0]
        h1 += a.OOS_CAGR > r.OOS_CAGR
        h2 += a.OOS_MaxDD < r.OOS_MaxDD
    live = Pr[(Pr.leg == "OOS") & (Pr["mode"] == "AGG")]
    buys = live[live.buys_CAGR]
    free = buys[~buys.pays_DD]
    ddcap = G[(~G.pass4b) & (G.fail4b.str.contains("DDCAP"))]
    P(f"  H1 AGG pick buys OOS CAGR in every family x panel : {h1}/{tot}  "
      f"{'PASS' if h1 == tot else 'REFUTED'}")
    P(f"  H2 AGG pick pays OOS drawdown in every cell       : {h2}/{tot}  "
      f"{'PASS' if h2 == tot else 'REFUTED'}")
    P(f"  H3 no FREE premium anywhere on the grid (OOS)     : {len(free)}/{len(buys)} free  "
      f"{'PASS' if len(free) == 0 else 'REFUTED'}")
    P(f"  H4 DDCAP is the modal 4b blocker                  : {len(ddcap):,} of "
      f"{int((~G.pass4b).sum()):,} 4b failures name DDCAP")
    for mode in MODES:
        S = G[G["mode"] == mode]
        P(f"       {mode:4s} n={len(S):4d}  4a {int(S.pass4a.sum()):3d}  4b {int(S.pass4b.sum()):3d}"
          f"  DDCAP-blocked {int(S.fail4b.str.contains('DDCAP').sum()):4d}")
    P(f"  H5 4a is ~absent                                  : {int(G.pass4a.sum())}/{len(G)}")
    P()
    keepers = W[(W.full_4b) & (W.p4b_0) & (W.p4b_10) & (W.p4b_25)]
    P(f"  rule-8 picks clearing 4b at ALL cost rungs: {len(keepers)} of {len(W)}")
    if len(keepers):
        for _, k in keepers.iterrows():
            P(f"     {k.panel:10s} {k.family:5s} {k['mode']:4s} th={k.pick_theta:.2f} "
              f"g={k.pick_gross:.2f}  OOS {k.OOS_CAGR:7.2%}/{k.OOS_Sharpe:.4f}/{k.OOS_MaxDD:7.2%}")
    P(f"  rule-8 picks clearing 4a at 10 bps       : {int(W.p4a_10.sum())} of {len(W)}")
    return dict(h1=h1, h2=h2, tot=tot, free=len(free), buys=len(buys))


def main():
    t0 = time.time()
    P("=" * 100)
    P(f"Idea 662 -- is EVERY ROW-vs-AGG gap in the record a DRAWDOWN gap?  (lane B, "
      f"{pd.Timestamp.today().date()})")
    P("=" * 100)
    P(__doc__.split("Outputs beside")[0].strip())
    panels = load_panels()
    ok = gates(panels)
    G, refs = run_grid(panels)
    Pr = pairs(G)
    W = walkforward(panels, G, refs)
    v = verdict(G, Pr, W)
    P()
    P("=" * 100)
    P("(O) OUTPUTS")
    P("=" * 100)
    dump(G, "grid.csv")
    dump(Pr, "pairs.csv")
    dump(W, "walkforward.csv")
    P(f"  gates {'ALL PASS' if ok else 'FAILED'}   total runtime {time.time() - t0:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"wrote {STEM}.console.txt")


if __name__ == "__main__":
    main()

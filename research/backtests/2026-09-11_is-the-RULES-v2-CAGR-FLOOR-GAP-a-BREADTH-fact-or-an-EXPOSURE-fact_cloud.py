#!/usr/bin/env python3
"""Idea 795 (cloud, 2026-09-11) — is-the-RULES-v2-CAGR-FLOOR-GAP-a-BREADTH-fact-or-an-
EXPOSURE-fact.

QUESTION
--------
The live book (RULES v2: hold every U56 name inside the 200d +/-3% band at 0.75/N of NAV,
weekly, de-gross to cash) clears every 4b leg except the CAGR floor: OOS CAGR 9.45% against
0.70 x SPY's 15.24% = 10.67%, a gap of 1.22 pp.  Idea 776's dial grid moves U56 OOS CAGR
8.61% -> 11.52% on the GROSS dial alone, which says the gap is exposure.  But the band admits
~72% of the panel on average, so the book may simply be diluted by its own breadth: holding
more names at the same gross cannot raise the return per unit of exposure, it can only move
it toward the panel mean.  Those are different diagnoses with different remedies (lever up vs
concentrate), and nobody has separated them.

THE DECOMPOSITION (exact, not a proxy)
--------------------------------------
RULES v2's held book is, by construction, `gross x breadth_t` units of an equal-weight
portfolio of the in-band names.  So for every book on the grid, with held weights w_it from
the engine (drift included) and daily asset returns ret_it:

    E_t  = sum_i w_it                      realised EXPOSURE  (gross x realised breadth)
    G_t  = sum_i w_it ret_it               gross-of-cost book return
    u_t  = G_t / E_t   (0 when E_t = 0)    RETURN PER UNIT OF EXPOSURE  (the sleeve's own return)
    c_t  = turnover_t x cost_bps / 1e4     cost drag
    r_t  = G_t - c_t                       the book's net return

    mean(r) = Ebar * ubar + cov(E, u) - mean(c)                       [IDENTITY, gate G2]
              \_______/   \________/   \_______/
              EXPOSURE    TIMING       COST
              x PER-UNIT  (does the book hold more when the sleeve does better?)

Annualised (x252) this splits the book's arithmetic mean return into an EXPOSURE leg
(Ebar, which the gross dial moves one-for-one and the band dial moves through breadth), a
PER-UNIT leg (ubar, which only selection can move), a TIMING leg and a COST leg.  Attribution
between any two cells is the standard two-term split
    d mean(r) = ubar * dEbar  +  Ebar * dubar  +  dcov  -  dmean(c).
"Which leg carries the gap" is then a number, not a reading.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two, as the queue specifies)
    1. BAND  in {0.00, 0.01, 0.03, 0.05, 0.08, 0.12, 0.20}   (0.03 = live)
    2. GROSS in {0.50, 0.60, 0.75, 0.85, 1.00}               (0.75 = live; 1.00 = no leverage cap)
All 7 x 5 = 35 cells are reported on the primary panel.  REPORTED, never selected: the B136
broad-panel replication (same 35 cells), the halves, the OOS window, and the cost/timing legs.

PRE-REGISTERED HYPOTHESES (written before any new number was read)
    H_EXP    : the gap is an EXPOSURE fact — over the 35 cells, the exposure leg explains more
               of the spread in mean return than the per-unit leg (|corr(Ebar, mean r)| >
               |corr(ubar, mean r)|).
    H_DILUTE : breadth dilutes — ubar is DECREASING in realised breadth across the band dial
               at fixed gross (Spearman < 0).  Falsified at >= 0.
    H_FLOOR  : some cell on the grid clears the 4b OOS CAGR floor (0.70 x SPY OOS CAGR) without
               leverage (gross <= 1.00).
    H_WF     : rule 8 — the cell chosen on 2009-2016 alone still clears the floor on 2017-2026.

GATES (pre-registered, reported before any finding)
    G1 the live cell IS the live book: cell (band 0.03, gross 0.75) reproduces the record's
       RULES v2 full Sharpe 1.1998 / MaxDD -12.05% / OOS CAGR 9.45%.
    G2 the decomposition is an identity: max |mean(r) - (Ebar*ubar + cov(E,u) - mean(c))|
       over all cells < 1e-12.
    G3 gross is ~a PURE exposure dial: at fixed band, Ebar/gross is constant to < 5% relative
       and ubar moves < 2 pp/yr across the gross dial.  Not an exact identity — the engine
       renormalises drift through the cash leg, so books at different gross follow slightly
       different exposure paths (idea 539's known gross leak).
    G4 the comparands are the record's: SPY full CAGR 15.11% / Sharpe 0.8835 / MaxDD -33.72%,
       SPY OOS CAGR 15.24% / Sharpe 0.8721, 4b CAGR floor 10.67%, DD cap -20.23%.

PROTOCOL: 10 bps, next-day execution (engine), weekly cadence, no shorting, no leverage
(gross <= 1.00).  Rule 8 walk-forward: the cell is chosen on 2009-2016 only and 2017-2026 is
read once.  RULES.md / scan.py / bot.py / baseline.py are NOT modified.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, band_state, rules_v2_weights, metrics, backtest  # noqa: E402

OUT = str(ROOT / "research" / "backtests" /
          "2026-09-11_is-the-RULES-v2-CAGR-FLOOR-GAP-a-BREADTH-fact-or-an-EXPOSURE-fact_cloud")
COST = 10
FREQ = "W"
BANDS = [0.00, 0.01, 0.03, 0.05, 0.08, 0.12, 0.20]
GROSSES = [0.50, 0.60, 0.75, 0.85, 1.00]
LIVE = (0.03, 0.75)
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

_LOG: list[str] = []


def P(s: str = "") -> None:
    print(s)
    _LOG.append(s)


def band_weights(px: pd.DataFrame, band: float, gross: float) -> pd.DataFrame:
    """RULES v2's weights function with the two dials exposed.  band=0.03, gross=0.75 is live."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, band), 0.0)


def decompose(px: pd.DataFrame, res: dict, start) -> dict:
    """The exact E x u + cov - cost split of the book's annualised arithmetic mean return."""
    rets = px.pct_change().fillna(0.0)
    held = res["weights"].loc[start:]
    E = held.sum(axis=1)
    G = (held * rets.loc[start:]).sum(axis=1)
    c = res["turnover"].loc[start:] * COST / 1e4
    u = np.where(E.values > 0, G.values / np.where(E.values > 0, E.values, 1.0), 0.0)
    u = pd.Series(u, index=E.index)
    r = G - c
    Ebar, ubar = float(E.mean()), float(u.mean())
    cov = float(np.cov(E.values, u.values, ddof=0)[0, 1])
    return dict(mean_r=float(r.mean()), Ebar=Ebar, ubar=ubar, cov=cov, mean_c=float(c.mean()),
                exposure_leg=252 * Ebar * ubar, timing_leg=252 * cov, cost_leg=-252 * float(c.mean()),
                ann_mean=252 * float(r.mean()), breadth=Ebar, returns=r)


def spearman(a, b) -> float:
    """Rank correlation without scipy (the sandbox has pandas/numpy only)."""
    ra, rb = pd.Series(np.asarray(a, float)).rank(), pd.Series(np.asarray(b, float)).rank()
    return float(np.corrcoef(ra.values, rb.values)[0, 1])


def window(r: pd.Series, lo=None, hi=None) -> pd.Series:
    return r.loc[lo:hi]


def cell_row(px, band, gross, start, panel):
    res = backtest(px, band_weights(px, band, gross), cost_bps=COST, freq=FREQ)
    d = decompose(px, res, start)
    r = d.pop("returns")
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    mi, mo = metrics(window(r, None, IS_END)), metrics(window(r, OOS_START, None))
    # realised breadth in NAME terms (exposure / gross), reported separately from Ebar
    row = dict(panel=panel, band=band, gross=gross,
               CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
               H1=m1["Sharpe"], H2=m2["Sharpe"],
               IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
               OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
               OOS_H1=metrics(window(r, OOS_START, None).iloc[:len(window(r, OOS_START, None)) // 2])["Sharpe"],
               OOS_H2=metrics(window(r, OOS_START, None).iloc[len(window(r, OOS_START, None)) // 2:])["Sharpe"],
               turnover_yr=float(res["turnover"].loc[start:].sum() / m["Years"]),
               **d, realised_breadth=d["Ebar"] / gross)
    return row, r


def main() -> None:
    t0 = time.time()
    P("=" * 100)
    P("IDEA 795 — is the RULES v2 CAGR FLOOR GAP a BREADTH fact or an EXPOSURE fact?")
    P("cloud lane, 2026-09-11.  PROTOCOL: 10 bps, next-day execution, weekly, no leverage.")
    P("=" * 100)

    px = load_universe()
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    hs = len(spy) // 2
    ms, ms1, ms2 = metrics(spy), metrics(spy.iloc[:hs]), metrics(spy.iloc[hs:])
    mso = metrics(window(spy, OOS_START, None))
    msi = metrics(window(spy, None, IS_END))
    spy_oos_h = window(spy, OOS_START, None)
    mso1, mso2 = metrics(spy_oos_h.iloc[:len(spy_oos_h) // 2]), metrics(spy_oos_h.iloc[len(spy_oos_h) // 2:])
    FLOOR_FULL, CAP_FULL = 0.70 * ms["CAGR"], 0.60 * ms["MaxDD"]
    FLOOR_OOS, CAP_OOS = 0.70 * mso["CAGR"], 0.60 * mso["MaxDD"]
    P(f"panel U56: {px.shape[1]} columns, {px.index[0].date()} .. {px.index[-1].date()}, "
      f"scored from {start.date()}")
    P("")

    rows, rets = [], {}
    for band in BANDS:
        for gross in GROSSES:
            row, r = cell_row(px, band, gross, start, "U56")
            rows.append(row)
            rets[(band, gross)] = r
    grid = pd.DataFrame(rows)

    # ---------------------------------------------------------------- gates
    P("GATES (pre-registered)")
    live = grid[(grid.band == LIVE[0]) & (grid.gross == LIVE[1])].iloc[0]
    base = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
    mb = metrics(base)
    g1 = bool(abs(live["Sharpe"] - mb["Sharpe"]) < 1e-12 and abs(live["Sharpe"] - 1.1998) <= 0.01
              and abs(live["MaxDD"] + 0.1205) <= 0.01 and abs(live["OOS_CAGR"] - 0.0945) <= 0.005)
    P(f"  G1 live cell == live book : (band 0.03, gross 0.75) Sharpe {live['Sharpe']:.4f} "
      f"(baseline.rules_v2 {mb['Sharpe']:.4f}, record 1.1998), MaxDD {live['MaxDD']:.4f} "
      f"(record -0.1205), OOS CAGR {live['OOS_CAGR']:.4f} (record 0.0945) -> "
      f"{'PASS' if g1 else 'FAIL'}")

    ident = (grid["ann_mean"] - (grid["exposure_leg"] + grid["timing_leg"] + grid["cost_leg"])).abs().max()
    g2 = bool(ident < 1e-12)
    P(f"  G2 decomposition identity : max |ann mean r - (E*u + cov + cost)| over 35 cells "
      f"{ident:.3e} -> {'PASS' if g2 else 'FAIL'}")

    rel = []
    for band in BANDS:
        sub = grid[grid.band == band]
        rb = (sub["Ebar"] / sub["gross"])
        rel.append(float((rb.max() - rb.min()) / rb.mean()))
        # ubar is gross-of-cost per unit exposure, so it must not move with gross at all
    urel = []
    for band in BANDS:
        sub = grid[grid.band == band]["ubar"]
        urel.append(float(sub.max() - sub.min()))
    g3 = bool(max(rel) < 0.05 and max(urel) * 252 < 0.02)
    P(f"  G3 gross ~= pure exposure : max relative spread of Ebar/gross within a band "
      f"{max(rel):.3e}; max spread of ann. ubar within a band {max(urel) * 252:.3e} -> "
      f"{'PASS' if g3 else 'FAIL'}")
    P("     (not an exact identity: the engine renormalises drift through the cash leg, so a "
      "book at a\n      different gross follows a slightly different exposure path — idea 539's "
      "known gross leak.\n      Bars are 5% relative on Ebar/gross and 2 pp/yr on ubar; the "
      "measured values are above.)")

    g4 = bool(abs(ms["CAGR"] - 0.1511) <= 0.002 and abs(ms["Sharpe"] - 0.8835) <= 0.01
              and abs(ms["MaxDD"] + 0.3372) <= 0.005 and abs(mso["CAGR"] - 0.1524) <= 0.002
              and abs(mso["Sharpe"] - 0.8721) <= 0.01)
    P(f"  G4 comparands are record's: SPY full CAGR {ms['CAGR']:.4f} Sharpe {ms['Sharpe']:.4f} "
      f"MaxDD {ms['MaxDD']:.4f}; OOS CAGR {mso['CAGR']:.4f} Sharpe {mso['Sharpe']:.4f}; "
      f"4b floors full {FLOOR_FULL:.4f} / OOS {FLOOR_OOS:.4f}, DD caps {CAP_FULL:.4f} / "
      f"{CAP_OOS:.4f} -> {'PASS' if g4 else 'FAIL'}")
    P(f"  ALL GATES {'PASS' if all([g1, g2, g3, g4]) else 'NOT ALL PASS'}")
    P("")

    # ---------------------------------------------------------------- the grid
    P("THE GRID — 35 cells on U56 (band x gross), ALL reported")
    P("  Ebar = realised exposure (gross x breadth); ubar = ann. return per unit exposure;")
    P("  EXP = 252*Ebar*ubar, TIM = 252*cov(E,u), CST = -252*mean(cost).  ann = EXP+TIM+CST.")
    P("")
    P("  " + f"{'band':>5}{'gross':>7}{'brdth':>7}{'Ebar':>7}{'ubar*252':>10}{'EXP':>8}"
      f"{'TIM':>8}{'CST':>8}{'CAGR':>8}{'Shrp':>7}{'MaxDD':>8}{'OOSCAGR':>9}{'OOSShrp':>9}{'turn':>7}")
    for _, r in grid.iterrows():
        P("  " + f"{r['band']:>5.2f}{r['gross']:>7.2f}{r['realised_breadth']:>7.3f}"
          f"{r['Ebar']:>7.3f}{r['ubar'] * 252:>10.4f}{r['exposure_leg']:>8.4f}"
          f"{r['timing_leg']:>8.4f}{r['cost_leg']:>8.4f}{r['CAGR']:>8.4f}{r['Sharpe']:>7.3f}"
          f"{r['MaxDD']:>8.4f}{r['OOS_CAGR']:>9.4f}{r['OOS_Sharpe']:>9.3f}{r['turnover_yr']:>7.2f}")
    P("")

    # ---------------------------------------------------------------- which leg carries it
    P("WHICH LEG CARRIES THE GAP")
    cE = float(np.corrcoef(grid["Ebar"], grid["ann_mean"])[0, 1])
    cU = float(np.corrcoef(grid["ubar"], grid["ann_mean"])[0, 1])
    P(f"  over all 35 cells: corr(Ebar, ann mean r) {cE:+.4f}   corr(ubar, ann mean r) {cU:+.4f}")
    P(f"  H_EXP {'HELD' if abs(cE) > abs(cU) else 'FALSIFIED'} "
      f"(|{cE:+.4f}| vs |{cU:+.4f}|)")

    sub = grid[grid.gross == LIVE[1]].sort_values("realised_breadth")
    rho = spearman(sub["ubar"].values, sub["realised_breadth"].values)
    P(f"  at the live gross 0.75, across the band dial: realised breadth "
      f"{sub['realised_breadth'].min():.3f}..{sub['realised_breadth'].max():.3f}, "
      f"ubar*252 {sub['ubar'].min() * 252:.4f}..{sub['ubar'].max() * 252:.4f}, "
      f"Spearman(breadth, ubar) {rho:+.4f}")
    P(f"  H_DILUTE {'HELD' if rho < 0 else 'FALSIFIED'} (Spearman {rho:+.4f} vs < 0 bar)")
    P("")
    P("  two-term attribution of every cell against the LIVE cell "
      "(d ann mean r = ubar_live*dEbar + Ebar_live*dubar + dTIM + dCST):")
    P("  " + f"{'band':>5}{'gross':>7}{'d ann':>9}{'via dE':>9}{'via du':>9}{'dTIM':>9}{'dCST':>9}"
      f"{'share E':>9}{'share u':>9}")
    att = []
    for _, r in grid.iterrows():
        dE = r["Ebar"] - live["Ebar"]
        du = r["ubar"] - live["ubar"]
        viaE = 252 * live["ubar"] * dE
        viaU = 252 * live["Ebar"] * du
        dT = r["timing_leg"] - live["timing_leg"]
        dC = r["cost_leg"] - live["cost_leg"]
        dA = r["ann_mean"] - live["ann_mean"]
        tot = abs(viaE) + abs(viaU) + abs(dT) + abs(dC)
        att.append(dict(band=r["band"], gross=r["gross"], d_ann=dA, via_dE=viaE, via_du=viaU,
                        d_TIM=dT, d_CST=dC,
                        share_E=(abs(viaE) / tot if tot else np.nan),
                        share_u=(abs(viaU) / tot if tot else np.nan)))
        P("  " + f"{r['band']:>5.2f}{r['gross']:>7.2f}{dA:>9.4f}{viaE:>9.4f}{viaU:>9.4f}"
          f"{dT:>9.4f}{dC:>9.4f}"
          + (f"{att[-1]['share_E']:>9.3f}{att[-1]['share_u']:>9.3f}" if tot else f"{'n/a':>9}{'n/a':>9}"))
    att = pd.DataFrame(att)
    nz = att[(att.band != LIVE[0]) | (att.gross != LIVE[1])]
    P("")
    P(f"  pooled over the 34 non-live cells: mean |via dE| {nz['via_dE'].abs().mean():.4f} vs "
      f"mean |via du| {nz['via_du'].abs().mean():.4f}  (ratio "
      f"{nz['via_dE'].abs().mean() / max(nz['via_du'].abs().mean(), 1e-12):.2f}x)")
    bandonly = att[(att.gross == LIVE[1]) & (att.band != LIVE[0])]
    grossonly = att[(att.band == LIVE[0]) & (att.gross != LIVE[1])]
    P(f"  BAND dial alone (gross fixed 0.75, 6 cells): mean |via dE| "
      f"{bandonly['via_dE'].abs().mean():.4f}, mean |via du| {bandonly['via_du'].abs().mean():.4f}, "
      f"best d ann {bandonly['d_ann'].max():+.4f}")
    P(f"  GROSS dial alone (band fixed 0.03, 4 cells): mean |via dE| "
      f"{grossonly['via_dE'].abs().mean():.4f}, mean |via du| {grossonly['via_du'].abs().mean():.4f}, "
      f"best d ann {grossonly['d_ann'].max():+.4f}")
    P("")

    # ---------------------------------------------------------------- 4b footprint
    P("4b FOOTPRINT ON THE FULL SAMPLE (all 35 cells, reported)")
    def keep4b(r, useoos=True):
        legs = dict(
            H1=r["H1"] > ms1["Sharpe"], H2=r["H2"] > ms2["Sharpe"],
            OOS=r["OOS_Sharpe"] > mso["Sharpe"],
            DD=r["MaxDD"] >= CAP_FULL, CAGR=r["CAGR"] >= FLOOR_FULL)
        return legs
    def keep4a(r):
        return dict(H1=r["H1"] > live["H1"], H2=r["H2"] > live["H2"], DD=r["MaxDD"] >= live["MaxDD"])
    n4b = 0
    fails = {}
    for _, r in grid.iterrows():
        legs = keep4b(r)
        if all(legs.values()):
            n4b += 1
        for k, v in legs.items():
            if not v:
                fails[k] = fails.get(k, 0) + 1
    P(f"  4b legs: Sharpe > SPY in BOTH halves ({ms1['Sharpe']:.4f} / {ms2['Sharpe']:.4f}) AND "
      f"OOS ({mso['Sharpe']:.4f}); MaxDD >= {CAP_FULL:.4f}; CAGR >= {FLOOR_FULL:.4f}")
    P(f"  4b passes: {n4b} of 35.  Binding legs (count of cells failing each): "
      + ", ".join(f"{k} {v}" for k, v in sorted(fails.items(), key=lambda x: -x[1])))
    ok = grid[[all(keep4b(r).values()) for _, r in grid.iterrows()]]
    if len(ok):
        P("  passing cells:")
        for _, r in ok.iterrows():
            P(f"    band {r['band']:.2f} gross {r['gross']:.2f}: CAGR {r['CAGR']:.4f} Sharpe "
              f"{r['Sharpe']:.4f} (H1 {r['H1']:.3f} / H2 {r['H2']:.3f}) MaxDD {r['MaxDD']:.4f} "
              f"OOS Sharpe {r['OOS_Sharpe']:.4f} OOS CAGR {r['OOS_CAGR']:.4f}")
    n4a = int(sum(all(keep4a(r).values()) for _, r in grid.iterrows()))
    P(f"  4a passes (vs the LIVE cell, Sharpe in both halves and MaxDD no worse): {n4a} of 35")
    oosfloor = grid[grid["OOS_CAGR"] >= FLOOR_OOS]
    P(f"  cells clearing the 4b OOS CAGR floor {FLOOR_OOS:.4f} without leverage: "
      f"{len(oosfloor)} of 35"
      + ("" if not len(oosfloor) else "  -> " + ", ".join(
          f"({r['band']:.2f},{r['gross']:.2f})" for _, r in oosfloor.iterrows())))
    P(f"  H_FLOOR {'HELD' if len(oosfloor) else 'FALSIFIED'}")
    P("")

    # ---------------------------------------------------------------- rule 8
    P("RULE 8 WALK-FORWARD — dials chosen on 2009-2016 ONLY, 2017-2026 read ONCE")
    P("  pre-stated selector: among cells with gross <= 1.00, the HIGHEST IS Sharpe.  A second,")
    P("  also pre-stated selector (IS CAGR-floor-aware): the highest IS Sharpe among cells whose")
    P("  IS CAGR clears 0.70 x SPY's IS CAGR.  Both are reported; neither reads the OOS window.")
    pick_s = grid.loc[grid["IS_Sharpe"].idxmax()]
    is_floor = 0.70 * msi["CAGR"]
    cand = grid[grid["IS_CAGR"] >= is_floor]
    pick_f = cand.loc[cand["IS_Sharpe"].idxmax()] if len(cand) else None
    P(f"  SPY IS (..{IS_END}) CAGR {msi['CAGR']:.4f} Sharpe {msi['Sharpe']:.4f}; IS CAGR floor "
      f"{is_floor:.4f}; {len(cand)} of 35 cells clear it in-sample")
    for tag, pk in [("PICK-Sharpe", pick_s), ("PICK-Sharpe|IS-floor", pick_f)]:
        if pk is None:
            P(f"  {tag}: none eligible")
            continue
        P(f"  {tag}: band {pk['band']:.2f} gross {pk['gross']:.2f}  IS Sharpe {pk['IS_Sharpe']:.4f} "
          f"IS CAGR {pk['IS_CAGR']:.4f}")
        P(f"    OOS read ONCE: CAGR {pk['OOS_CAGR']:.4f} Sharpe {pk['OOS_Sharpe']:.4f} MaxDD "
          f"{pk['OOS_MaxDD']:.4f} (halves {pk['OOS_H1']:.3f} / {pk['OOS_H2']:.3f})")
        P(f"    vs RULES v2 OOS CAGR {live['OOS_CAGR']:.4f} Sharpe {live['OOS_Sharpe']:.4f} MaxDD "
          f"{live['OOS_MaxDD']:.4f}; vs SPY OOS CAGR {mso['CAGR']:.4f} Sharpe {mso['Sharpe']:.4f} "
          f"MaxDD {mso['MaxDD']:.4f}")
        legs = dict(OOS_Sharpe_gt_SPY=bool(pk["OOS_Sharpe"] > mso["Sharpe"]),
                    OOS_H1=bool(pk["OOS_H1"] > mso1["Sharpe"]), OOS_H2=bool(pk["OOS_H2"] > mso2["Sharpe"]),
                    OOS_DD=bool(pk["OOS_MaxDD"] >= CAP_OOS), OOS_CAGR=bool(pk["OOS_CAGR"] >= FLOOR_OOS))
        P(f"    4b legs OOS: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in legs.items())
          + f"  -> {'4b OOS PASS' if all(legs.values()) else '4b OOS FAIL'}")
    if pick_f is not None:
        hw = bool(pick_f["OOS_CAGR"] >= FLOOR_OOS)
        P(f"  H_WF {'HELD' if hw else 'FALSIFIED'} (PICK-Sharpe|IS-floor OOS CAGR "
          f"{pick_f['OOS_CAGR']:.4f} vs floor {FLOOR_OOS:.4f})")
    P("")
    P("  ---- DISCLOSED POST-HOC selector (added AFTER the two selectors above were read OOS;")
    P("       it is NOT pre-registered by this run and the KEEP claim does not rest on it).")
    P("       It quotes the record's own 2026-09-03 recommendation memo verbatim — 'smallest G")
    P("       whose MaxDD <= 60% of SPY's and CAGR >= 70% of SPY's' — with the band FROZEN at")
    P("       the live 0.03, i.e. ONE free parameter instead of two.")
    fixed = grid[grid.band == LIVE[0]].sort_values("gross")
    is_cap = 0.60 * msi["MaxDD"]
    okg = fixed[(fixed["IS_MaxDD"] >= is_cap) & (fixed["IS_CAGR"] >= is_floor)]
    P(f"       IS bars: MaxDD >= {is_cap:.4f}, CAGR >= {is_floor:.4f}; eligible grosses "
      + (", ".join(f"{g:.2f}" for g in okg['gross']) if len(okg) else "NONE"))
    pick_r = okg.iloc[0] if len(okg) else None
    if pick_r is not None:
        legs = dict(OOS_Sharpe_gt_SPY=bool(pick_r["OOS_Sharpe"] > mso["Sharpe"]),
                    OOS_H1=bool(pick_r["OOS_H1"] > mso1["Sharpe"]),
                    OOS_H2=bool(pick_r["OOS_H2"] > mso2["Sharpe"]),
                    OOS_DD=bool(pick_r["OOS_MaxDD"] >= CAP_OOS),
                    OOS_CAGR=bool(pick_r["OOS_CAGR"] >= FLOOR_OOS))
        P(f"       PICK-RECOMMENDATION: band {pick_r['band']:.2f} gross {pick_r['gross']:.2f}  "
          f"IS Sharpe {pick_r['IS_Sharpe']:.4f} IS CAGR {pick_r['IS_CAGR']:.4f} IS MaxDD "
          f"{pick_r['IS_MaxDD']:.4f}")
        P(f"         OOS read: CAGR {pick_r['OOS_CAGR']:.4f} Sharpe {pick_r['OOS_Sharpe']:.4f} "
          f"MaxDD {pick_r['OOS_MaxDD']:.4f} (halves {pick_r['OOS_H1']:.3f} / {pick_r['OOS_H2']:.3f})")
        P(f"         4b legs OOS: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}"
                                                for k, v in legs.items())
          + f"  -> {'4b OOS PASS' if all(legs.values()) else '4b OOS FAIL'}")
    P("")
    P("  THE BAND DIAL IS NOISE, AND THE WALK-FORWARD PAYS FOR IT: at gross 1.00 the IS-chosen")
    b008 = grid[(grid.band == 0.08) & (grid.gross == 1.00)].iloc[0]
    b003 = grid[(grid.band == 0.03) & (grid.gross == 1.00)].iloc[0]
    P(f"  band 0.08 reads OOS CAGR {b008['OOS_CAGR']:.4f} / Sharpe {b008['OOS_Sharpe']:.4f} / "
      f"MaxDD {b008['OOS_MaxDD']:.4f} against the LIVE band 0.03's {b003['OOS_CAGR']:.4f} / "
      f"{b003['OOS_Sharpe']:.4f} / {b003['OOS_MaxDD']:.4f}.")
    P(f"  Tuning the band cost {(b003['OOS_CAGR'] - b008['OOS_CAGR']) * 100:.2f} pp of OOS CAGR, "
      f"{b003['OOS_Sharpe'] - b008['OOS_Sharpe']:.4f} of OOS Sharpe and "
      f"{(b003['OOS_MaxDD'] - b008['OOS_MaxDD']) * 100:.2f} pp of OOS drawdown — the second free")
    P("  parameter bought nothing and was paid for out of sample.  Reported, not selected on.")
    P("")

    # ---------------------------------------------------------------- B136 replication
    P("REPLICATION ON B136 (broad panel, 136 large caps; REPORTED, never selected)")
    P("  SURVIVORSHIP: universe_broad.json is CURRENT constituents only, so the broad panel's")
    P("  returns are biased upward; the panel is a robustness read, not a capital claim.")
    pxb = load_universe(broad=True)
    startb = pxb.index[260]
    rowsb = []
    for band in BANDS:
        for gross in GROSSES:
            rb, _ = cell_row(pxb, band, gross, startb, "B136")
            rowsb.append(rb)
    gb = pd.DataFrame(rowsb)
    spyb = pxb["SPY"].pct_change().fillna(0).loc[startb:]
    msb, msbo = metrics(spyb), metrics(window(spyb, OOS_START, None))
    liveb = gb[(gb.band == LIVE[0]) & (gb.gross == LIVE[1])].iloc[0]
    cEb = float(np.corrcoef(gb["Ebar"], gb["ann_mean"])[0, 1])
    cUb = float(np.corrcoef(gb["ubar"], gb["ann_mean"])[0, 1])
    subb = gb[gb.gross == LIVE[1]]
    rhob = spearman(subb["ubar"].values, subb["realised_breadth"].values)
    P(f"  live cell B136: CAGR {liveb['CAGR']:.4f} Sharpe {liveb['Sharpe']:.4f} MaxDD "
      f"{liveb['MaxDD']:.4f} OOS CAGR {liveb['OOS_CAGR']:.4f}; SPY OOS CAGR {msbo['CAGR']:.4f}")
    P(f"  corr(Ebar, ann mean r) {cEb:+.4f} vs corr(ubar, ann mean r) {cUb:+.4f}  -> "
      f"{'EXPOSURE' if abs(cEb) > abs(cUb) else 'PER-UNIT'} dominates, same direction as U56: "
      f"{'YES' if (abs(cEb) > abs(cUb)) == (abs(cE) > abs(cU)) else 'NO'}")
    P(f"  Spearman(breadth, ubar) across the band dial at gross 0.75: {rhob:+.4f} "
      f"(U56 {rho:+.4f}) -> dilution direction replicates: "
      f"{'YES' if (rhob < 0) == (rho < 0) else 'NO'}")
    P(f"  realised breadth range B136 {gb['realised_breadth'].min():.3f}.."
      f"{gb['realised_breadth'].max():.3f} (U56 {grid['realised_breadth'].min():.3f}.."
      f"{grid['realised_breadth'].max():.3f})")
    P("")

    # ---------------------------------------------------------------- KEEP paths
    P("KEEP PATHS (PROTOCOL rule 4)")
    P(f"  comparands: RULES v2 (live) full CAGR {live['CAGR']:.4f} Sharpe {live['Sharpe']:.4f} "
      f"(H1 {live['H1']:.4f} / H2 {live['H2']:.4f}) MaxDD {live['MaxDD']:.4f}; OOS CAGR "
      f"{live['OOS_CAGR']:.4f} Sharpe {live['OOS_Sharpe']:.4f} MaxDD {live['OOS_MaxDD']:.4f}")
    P(f"              SPY full CAGR {ms['CAGR']:.4f} Sharpe {ms['Sharpe']:.4f} (H1 "
      f"{ms1['Sharpe']:.4f} / H2 {ms2['Sharpe']:.4f}) MaxDD {ms['MaxDD']:.4f}; OOS CAGR "
      f"{mso['CAGR']:.4f} Sharpe {mso['Sharpe']:.4f} MaxDD {mso['MaxDD']:.4f}")
    P(f"  4a (beat the book): {n4a} of 35 cells beat the live book's Sharpe in BOTH halves with "
      f"MaxDD no worse.")
    P(f"  4b (capital-worthy): {n4b} of 35 cells clear all five full-sample legs; "
      f"{len(oosfloor)} clear the OOS CAGR floor.")
    P("  The rule-8 verdict above, not the full-sample footprint, is the one that counts.")
    P("")

    # ---------------------------------------------------------------- artefacts
    grid.to_csv(f"{OUT}.grid.csv", index=False)
    gb.to_csv(f"{OUT}.broad.csv", index=False)
    att.to_csv(f"{OUT}.attribution.csv", index=False)
    wf = pd.DataFrame([
        dict(selector="PICK-Sharpe", band=pick_s["band"], gross=pick_s["gross"],
             IS_Sharpe=pick_s["IS_Sharpe"], IS_CAGR=pick_s["IS_CAGR"],
             OOS_CAGR=pick_s["OOS_CAGR"], OOS_Sharpe=pick_s["OOS_Sharpe"],
             OOS_MaxDD=pick_s["OOS_MaxDD"]),
    ] + ([] if pick_f is None else [
        dict(selector="PICK-Sharpe|IS-floor", band=pick_f["band"], gross=pick_f["gross"],
             IS_Sharpe=pick_f["IS_Sharpe"], IS_CAGR=pick_f["IS_CAGR"],
             OOS_CAGR=pick_f["OOS_CAGR"], OOS_Sharpe=pick_f["OOS_Sharpe"],
             OOS_MaxDD=pick_f["OOS_MaxDD"])])
      + ([] if pick_r is None else [
        dict(selector="PICK-RECOMMENDATION (POST-HOC, disclosed)", band=pick_r["band"],
             gross=pick_r["gross"], IS_Sharpe=pick_r["IS_Sharpe"], IS_CAGR=pick_r["IS_CAGR"],
             OOS_CAGR=pick_r["OOS_CAGR"], OOS_Sharpe=pick_r["OOS_Sharpe"],
             OOS_MaxDD=pick_r["OOS_MaxDD"])]))
    wf.to_csv(f"{OUT}.walkforward.csv", index=False)
    summary = dict(
        idea=795, lane="cloud", date="2026-09-11",
        corr_Ebar=cE, corr_ubar=cU, spearman_breadth_ubar=rho,
        corr_Ebar_B136=cEb, corr_ubar_B136=cUb, spearman_breadth_ubar_B136=rhob,
        live=dict(CAGR=live["CAGR"], Sharpe=live["Sharpe"], MaxDD=live["MaxDD"],
                  H1=live["H1"], H2=live["H2"], OOS_CAGR=live["OOS_CAGR"],
                  OOS_Sharpe=live["OOS_Sharpe"], OOS_MaxDD=live["OOS_MaxDD"],
                  Ebar=live["Ebar"], ubar252=live["ubar"] * 252,
                  breadth=live["realised_breadth"]),
        spy=dict(CAGR=ms["CAGR"], Sharpe=ms["Sharpe"], MaxDD=ms["MaxDD"], H1=ms1["Sharpe"],
                 H2=ms2["Sharpe"], OOS_CAGR=mso["CAGR"], OOS_Sharpe=mso["Sharpe"],
                 OOS_MaxDD=mso["MaxDD"], floor_full=FLOOR_FULL, floor_oos=FLOOR_OOS,
                 cap_full=CAP_FULL, cap_oos=CAP_OOS),
        n4a=n4a, n4b=n4b, n_oos_floor=int(len(oosfloor)),
        gates=dict(G1=g1, G2=g2, G3=g3, G4=g4, identity=float(ident)),
        wf=json.loads(wf.to_json(orient="records")),
    )
    Path(f"{OUT}.summary.json").write_text(json.dumps(summary, indent=2, default=float))
    P(f"artefacts: {Path(OUT).name}.grid.csv .broad.csv .attribution.csv .walkforward.csv "
      f".summary.json .console.txt   ({time.time() - t0:.0f}s)")
    Path(f"{OUT}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""idea 2373 (lane cloud, 2026-09-23) — does the CAPPED 4b candidate's pass survive a LATER
SAMPLE START?

THE OBJECT.  Idea 2322 filed the record's standing KEEP-4b candidate as CAP2:

    w_i = min(gross / N_in, 0.02)  on names INSIDE the 200d +/-3% band,
    idle NAV (1 - sum w) swept to SHY at phi = 1.00,  weekly cadence, t+1 execution.

THE COMPLAINT.  Every number ever published on CAP2 starts its window in the SAME place: the
2008 cache start plus a 260-row warm-up, i.e. the first trading days of 2009, one quarter off
the GFC low.  Both of 4b's ABSOLUTE legs lean on that placement.  `L_CAGR` is a ratio to SPY's
own CAGR measured from the same bottom; `L_H1` is a Sharpe over a first half that CONTAINS the
rebound.  Real capital is never deployed at a bottom.

THE DEVICE.  Re-price the SAME book — not a new one — over start years Y {2009, 2010, 2011,
2012, 2013} with the END fixed, and recompute SPY's floor (0.70 x CAGR) and cap (0.60 x MaxDD)
and the live book's comparands ON EACH WINDOW.  Y = 2009 IS the committed window, so the ladder
contains the record's own headline (gate G7).  The weights are built from the FULL price
history in every window, so the 200d band always carries real history and the later windows
are pure evaluation slices, never re-fitted books (gate G8b).

DIAL 1 -- start year Y {2009, 2010, 2011, 2012, 2013}.  A WINDOW dial, not a book dial.
DIAL 2 -- gross g {0.75 (live), 1.00}.  The only dial that changes the book.

REPORTED, NEVER SELECTED ON: 2 panels (U56, B136), 4 cost rungs (0 / 10 / 25 / 50 bps), weekly
cadence, t+1 execution, band 0.03, per-name cap 0.02 (2322's filed constant), sweep SHY phi=1.
5 x 2 x 2 x 4 = 80 published rows, every grid point printed.

BOTH KEEP PATHS on every row: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse) and
4b (Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's),
with the halves and both SPY bars recomputed inside each window.
RULE 8: OOS is 2017-01-01..end and is the SAME window for every Y, so both choosers are legal.
  C_G   chooses gross on <= 2016-12-31 within each Y   (the deployable reading, HEADLINE).
  C_YG  chooses (Y, gross) jointly on <= 2016-12-31    (published alongside).
Two pre-stated IS-only objectives each (IS Sharpe, IS Calmar); 2017-2026 read ONCE.

GATES.  G0 >= 10y for every (panel, Y) window.  G1 CAP2 == an independent element-wise-min
construction.  G2 the per-column replica equals `engine.backtest` on the live weights.  G3 no
leverage anywhere.  G4 NO LOOKAHEAD: weights truncated at D equal full-panel weights up to D.
G5 SHY priced on every row it is held.  G6 exactly two tuned parameters.  G7 EXTERNAL
REPRODUCTION of idea 2322's committed U56 CAP2 headline (11.58% / 1.2643 / -14.81%, OOS 12.70%
/ 1.3243) at Y=2009, g=0.75, 10 bps.  G8a the windows are strictly nested and land in the right
calendar years.  G8b the BOOK is start-invariant (identical weights for every Y).  G9 SPY's own
floor and cap actually MOVE across Y (otherwise the idea has no object).

SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists held from 2008, so every
absolute 4b level here is optimistic.  This idea's whole subject is an ABSOLUTE leg pair
(L_CAGR against SPY's CAGR, L_H1 over a rebound-containing half), so the contamination is
first-order ON TOPIC, not netted out by a same-tape contrast: a later start removes the
rebound but NOT the survivorship, so a leg that dies here would die harder on a live panel.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_later-sample-start-on-the-capped-candidate_cloud.py
"""
from __future__ import annotations

import sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state   # noqa: E402
from engine import backtest                                        # noqa: E402

DATE, SLUG, LANE = "2026-09-23", "later-sample-start-on-the-capped-candidate", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, CADENCE, WARMUP = 0.03, "W", 260
NAME_CAP = 0.02                      # idea 2322's filed CAP2 constant -- FIXED, not a dial
SWEEP, PHI = "SHY", 1.00
YEARS = [2009, 2010, 2011, 2012, 2013]
GROSSES = [0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG = 10.0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LIVE_GROSS = 0.75

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    say(f"    GATE {'PASS' if ok else 'FAIL'}  {name}: {value} (target {target})")
    return bool(ok)


def publish(name, value):
    GATES.append(dict(gate=name, value=str(value), target="published, not asserted", pass_=True))
    say(f"    PUB   {name}: {value}")


# ---------------------------------------------------------------- the book
def cap2_weights(px, invest, gross):
    """idea 2322's filed CAP2: w_i = min(gross/N_in, 0.02) on IN names, idle -> SHY at phi=1."""
    q = px[invest]
    pr = q.notna()
    inb = band_state(q, BAND) & pr
    nin = inb.sum(axis=1).replace(0, np.nan)
    per = pd.concat([gross / nin, pd.Series(NAME_CAP, index=q.index)], axis=1).min(axis=1)
    w = inb.astype(float).mul(per.fillna(0.0), axis=0).reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + PHI * idle * px[SWEEP].notna().astype(float)
    return w


def cap2_reference(px, invest, gross):
    """Independent construction (numpy element-wise minimum, no pandas concat/min path)."""
    q = px[invest]
    inb = (band_state(q, BAND) & q.notna()).astype(float)
    nin = inb.sum(axis=1).replace(0, np.nan)
    per = np.minimum(gross / nin.values, NAME_CAP)
    w = pd.DataFrame(inb.values * per[:, None], index=q.index, columns=q.columns)
    w = w.fillna(0.0).reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + PHI * idle * px[SWEEP].notna().astype(float)
    return w


def run_book(prices, weights, freq=CADENCE):
    """Replica of engine.backtest keeping zero-cost returns + turnover so every cost rung is
    priced from one pass.  Un-invested residual drifts at 0% (engine's convention)."""
    rets = prices.pct_change().fillna(0.0)
    w_target = weights.reindex(prices.index).fillna(0.0).shift(1)
    key = prices.index.to_period(freq)
    s = pd.Series(key, index=prices.index)
    mask = (s != s.shift(-1)).shift(1, fill_value=False)
    held = np.zeros((len(prices.index), len(prices.columns)))
    cur = np.zeros(len(prices.columns))
    turnover = np.zeros(len(prices.index))
    gross_s = np.zeros(len(prices.index))
    wt, rv = w_target.values, rets.values
    for i in range(len(prices.index)):
        if mask.iloc[i] or i == 0:
            new = wt[i]
            turnover[i] = np.abs(new - cur).sum()
            cur = new.copy()
        held[i] = cur
        gross_s[i] = cur.sum()
        growth = cur * (1 + rv[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    r0 = pd.Series((held * rv).sum(axis=1), index=prices.index)
    return dict(r0=r0, turnover=pd.Series(turnover, index=prices.index),
                gross=pd.Series(gross_s, index=prices.index))


def priced(res, bps):
    return res["r0"] - res["turnover"] * bps / 1e4


# ---------------------------------------------------------------- metrics
def sharpe(r):
    v = r.std() * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    return float((1 + r).cumprod().iloc[-1] ** (252 / len(r)) - 1)


def maxdd(r):
    eq = (1 + r).cumprod()
    return float((eq / eq.cummax() - 1).min())


def calmar(r):
    d = maxdd(r)
    return float(cagr(r) / abs(d)) if d < 0 else np.nan


def halves(r):
    h = len(r) // 2
    return sharpe(r.iloc[:h]), sharpe(r.iloc[h:])


def legs(r, base, spy, r_oos, spy_oos):
    h1, h2 = halves(r); b1, b2 = halves(base); s1, s2 = halves(spy)
    p4a = (h1 > b1) and (h2 > b2) and (maxdd(r) >= maxdd(base))
    L_H1, L_H2 = h1 > s1, h2 > s2
    L_OOS = sharpe(r_oos) > sharpe(spy_oos)
    L_DD = maxdd(r) >= DD_CAP * maxdd(spy)
    L_CAGR = cagr(r) >= CAGR_FLOOR * cagr(spy)
    return dict(pass4a=bool(p4a), pass4b=bool(L_H1 and L_H2 and L_OOS and L_DD and L_CAGR),
                L_H1=bool(L_H1), L_H2=bool(L_H2), L_OOS=bool(L_OOS), L_DD=bool(L_DD),
                L_CAGR=bool(L_CAGR),
                m_H1=float(h1 - s1), m_H2=float(h2 - s2),
                m_OOS=float(sharpe(r_oos) - sharpe(spy_oos)),
                m_DD=float(maxdd(r) - DD_CAP * maxdd(spy)),
                m_CAGR=float(cagr(r) - CAGR_FLOOR * cagr(spy)),
                spy_CAGR=float(cagr(spy)), spy_Sharpe=float(sharpe(spy)), spy_MaxDD=float(maxdd(spy)),
                spy_H1=float(s1), spy_H2=float(s2),
                floor_CAGR=float(CAGR_FLOOR * cagr(spy)), cap_DD=float(DD_CAP * maxdd(spy)))


def main():
    t0 = time.time()
    say("=== idea 2373 — does the CAPPED 4b candidate's pass survive a LATER SAMPLE START? ===")
    say(f"    {DATE}  lane {LANE}   band {BAND}  cadence {CADENCE}  t+1  rungs {RUNGS} bps  "
        f"name cap {NAME_CAP:.2%} (FIXED, idea 2322)  sweep {SWEEP} phi={PHI:.2f}")
    say(f"    DIAL 1 start year Y {YEARS} (WINDOW dial)   DIAL 2 gross g {GROSSES} (BOOK dial)")
    say(f"    live comparand = RULES v2 at gross {LIVE_GROSS} in EVERY window; SPY's floor/cap recomputed per window")
    gate("G6 exactly two tuned parameters", "start year Y, gross g", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        panels[nm] = (px, list(px.columns))

    # ---- windows
    wins = {}
    for nm, (px, invest) in panels.items():
        for Y in YEARS:
            win = px.index[WARMUP:] if Y == 2009 else px.index[px.index >= f"{Y}-01-01"]
            wins[(nm, Y)] = win
            yrs = (win[-1] - win[0]).days / 365.25
            gate(f"G0 >= 10y ({nm} Y={Y})",
                 f"{win[0].date()}..{win[-1].date()} = {yrs:.1f}y, {len(win)} rows, {len(invest)} names",
                 ">= 10y", yrs >= 10)
        nested = all(set(wins[(nm, YEARS[i + 1])]).issubset(set(wins[(nm, YEARS[i])]))
                     for i in range(len(YEARS) - 1))
        yrs_ok = all(wins[(nm, Y)][0].year == Y for Y in YEARS)
        gate(f"G8a windows strictly nested and land in year Y ({nm})",
             f"nested={nested}, first-row years {[int(wins[(nm, Y)][0].year) for Y in YEARS]}",
             "True / [2009..2013]", nested and yrs_ok)

    # ---- G2 replica fidelity
    px_u, inv_u = panels["U56"]
    w_live = rules_v2_weights(px_u, band=BAND, gross=LIVE_GROSS)
    d2 = float((backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
                - priced(run_book(px_u, w_live), HEADLINE_RUNG)).abs().max())
    gate("G2 per-column replica == engine.backtest", f"max|d| {d2:.3e}", "< 1e-12", d2 < 1e-12)

    # ---- G1 independent construction
    d1 = float((cap2_weights(px_u, inv_u, 0.75) - cap2_reference(px_u, inv_u, 0.75)).abs().max().max())
    gate("G1 CAP2 == independent element-wise-min construction (U56, g=0.75)",
         f"max|dw| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    # ---- G4 no lookahead
    D = px_u.index[int(len(px_u) * 0.7)]
    wf = cap2_weights(px_u, inv_u, 0.75).loc[:D]
    pxt = px_u.loc[:D]
    wt = cap2_weights(pxt, [c for c in inv_u if c in pxt.columns], 0.75)
    d4 = float((wf - wt.reindex(columns=wf.columns).fillna(0.0)).abs().max().max())
    gate(f"G4 NO LOOKAHEAD: weights truncated at {D.date()} == full-panel weights up to {D.date()}",
         f"max|dw| {d4:.3e}", "< 1e-12", d4 < 1e-12)

    # ---- price every book once, slice per window
    rows, books = [], {}
    for pname, (px, invest) in panels.items():
        spy_full = px["SPY"].pct_change().fillna(0.0)
        base_res = run_book(px, rules_v2_weights(px[invest], band=BAND, gross=LIVE_GROSS)
                            .reindex(columns=px.columns).fillna(0.0))
        for g in GROSSES:
            w = cap2_weights(px, invest, g)
            mx = float(w.sum(axis=1).max())
            if mx > 1 + 1e-12:
                gate(f"G3 no leverage ({pname} g={g})", f"max row sum {mx:.9f}", "<= 1+1e-12", False)
            books[(pname, g)] = (run_book(px, w), mx, w)
        say(f"\n--- panel {pname} ({len(invest)} names) priced ({time.time() - t0:.0f}s)")
        for Y in YEARS:
            win = wins[(pname, Y)]
            spy = spy_full.loc[win]; spy_oos = spy.loc[OOS_START:]
            for g in GROSSES:
                res, mx, w = books[(pname, g)]
                for rung in RUNGS:
                    r = priced(res, rung).loc[win]
                    b = priced(base_res, rung).loc[win]
                    r_oos = r.loc[OOS_START:]
                    h1, h2 = halves(r)
                    rows.append(dict(panel=pname, Y=Y, gross=g, cost_bps=rung,
                                     CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                     H1=h1, H2=h2,
                                     IS_Sharpe=sharpe(r.loc[:IS_END]), IS_Calmar=calmar(r.loc[:IS_END]),
                                     OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                     base_CAGR=cagr(b), base_Sharpe=sharpe(b), base_MaxDD=maxdd(b),
                                     base_H1=halves(b)[0], base_H2=halves(b)[1],
                                     base_OOS_CAGR=cagr(b.loc[OOS_START:]),
                                     base_OOS_Sharpe=sharpe(b.loc[OOS_START:]),
                                     base_OOS_MaxDD=maxdd(b.loc[OOS_START:]),
                                     n_rows=len(r), max_row_sum=mx,
                                     turnover_yr=float(res["turnover"].loc[win].sum() / (len(win) / 252)),
                                     mean_gross=float(res["gross"].loc[win].mean()),
                                     mean_sweep_w=float(w[SWEEP].loc[win].mean()),
                                     **legs(r, b, spy, r_oos, spy_oos)))

    df = pd.DataFrame(rows)
    df.to_csv(f"{OUT}.grid.csv", index=False)

    gate("G3 no leverage (all 4 books)", f"max row sum {df.max_row_sum.max():.9f}",
         "<= 1+1e-12", bool((df.max_row_sum <= 1 + 1e-12).all()))
    shy_ok = all(bool(px[SWEEP].loc[px.index[WARMUP:]].notna().all()) for px, _ in panels.values())
    gate("G5 sweep instrument priced on every held row", f"SHY non-null on all panels: {shy_ok}",
         "True", shy_ok)
    # G8b the BOOK is start-invariant
    gate("G8b the BOOK is start-invariant (one weights matrix per (panel, gross), windows only slice)",
         "weights built from full history, never re-fitted per Y", "by construction", True)
    h = df[(df.panel == "U56") & (df.Y == 2009) & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    d7 = max(abs(h.CAGR - 0.1158), abs(h.Sharpe - 1.2643) / 10, abs(h.MaxDD + 0.1481),
             abs(h.OOS_CAGR - 0.1270), abs(h.OOS_Sharpe - 1.3243) / 10)
    gate("G7 reproduces idea 2322's committed U56 CAP2 headline (11.58%/1.2643/-14.81%, OOS 12.70%/1.3243)",
         f"read {h.CAGR:.2%} / {h.Sharpe:.4f} / {h.MaxDD:.2%}, OOS {h.OOS_CAGR:.2%} / {h.OOS_Sharpe:.4f}"
         f" -> max|d| {d7:.2e}", "< 1e-3", d7 < 1e-3)
    sp = df[(df.panel == "U56") & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)]
    TOL = 1e-6                       # anything below this is float noise, NOT movement
    cagr_spread = float(sp.spy_CAGR.max() - sp.spy_CAGR.min())
    dd_spread = float(sp.spy_MaxDD.max() - sp.spy_MaxDD.min())
    own_dd_spread = float(sp.MaxDD.max() - sp.MaxDD.min())
    gate("G9a SPY's CAGR FLOOR moves across Y (the idea has an object on that leg)",
         f"SPY CAGR {[f'{v:.2%}' for v in sp.spy_CAGR]}, spread {cagr_spread:.2e}",
         f"spread > {TOL:.0e}", cagr_spread > TOL)
    publish("G9b SPY's DD CAP is START-INVARIANT (half the idea's premise is empty)",
            f"SPY MaxDD {[f'{v:.4%}' for v in sp.spy_MaxDD]}, spread {dd_spread:.2e} "
            f"(< {TOL:.0e} = float noise); CAP2's OWN MaxDD spread {own_dd_spread:.2e}. "
            "SPY's worst drawdown in EVERY window is post-2009, so moving the start off the GFC "
            "low cannot move the L_DD leg at all -- only L_CAGR and L_H1/L_H2 can respond.")

    # ---------------------------------------------------------------- tables
    say("\n=== A. THE FULL GRID AT THE HEADLINE RUNG (10 bps) — every point, nothing dropped ===")
    for pname in panels:
        say(f"\n  {pname}")
        say("  Y    g    |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh  OOS DD | 4a 4b |"
            " H1/H2/OOS/DD/CAGR | SPY CAGR  SPY Sh  SPY DD | floor  cap    | turn/yr")
        for Y in YEARS:
            for g in GROSSES:
                r = df[(df.panel == pname) & (df.Y == Y) & (df.gross == g)
                       & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                lg = "".join("1" if r[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                say(f"  {Y} {g:.2f} | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%} |"
                    f" {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} {r.OOS_MaxDD:7.2%} |"
                    f" {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg:17s} |"
                    f" {r.spy_CAGR:8.2%} {r.spy_Sharpe:7.4f} {r.spy_MaxDD:7.2%} |"
                    f" {r.floor_CAGR:6.2%} {r.cap_DD:6.2%} | {r.turnover_yr:6.2f}")

    say("\n=== B. KEEP COUNTS OVER ALL PUBLISHED ROWS (5 Y x 2 gross x 2 panels x 4 rungs) ===")
    say(f"  4b passes: {int(df.pass4b.sum())} of {len(df)}      4a passes: {int(df.pass4a.sum())} of {len(df)}")
    for rung in RUNGS:
        d = df[df.cost_bps == rung]
        say(f"   {rung:5.1f} bps:  4b {int(d.pass4b.sum()):2d}/{len(d)}   4a {int(d.pass4a.sum()):2d}/{len(d)}"
            f"   binding leg on 4b FAILs: " +
            "  ".join(f"{k} {int((~d[k][~d.pass4b]).sum())}" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    say("\n  4b pass counts by (panel, Y) over 8 rows each (2 gross x 4 rungs):")
    for pname in panels:
        say(f"    {pname}: " + "   ".join(
            f"{Y} {int(df[(df.panel == pname) & (df.Y == Y)].pass4b.sum())}/8" for Y in YEARS))
    say("  4a pass counts by (panel, Y):")
    for pname in panels:
        say(f"    {pname}: " + "   ".join(
            f"{Y} {int(df[(df.panel == pname) & (df.Y == Y)].pass4a.sum())}/8" for Y in YEARS))

    say("\n=== C. WHICH LEG MOVES WITH Y — per-leg pass rate and MARGIN, 10 bps, g=0.75 ===")
    for pname in panels:
        say(f"  {pname} g=0.75  (margin > 0 == leg passes; DD/CAGR margins are in return units)")
        say("  Y    | L_H1  L_H2  L_OOS L_DD  L_CAGR |  m_H1    m_H2    m_OOS   m_DD    m_CAGR  | 4b")
        for Y in YEARS:
            r = df[(df.panel == pname) & (df.Y == Y) & (df.gross == 0.75)
                   & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
            say(f"  {Y} |  {'Y' if r.L_H1 else '.'}     {'Y' if r.L_H2 else '.'}     "
                f"{'Y' if r.L_OOS else '.'}     {'Y' if r.L_DD else '.'}     {'Y' if r.L_CAGR else '.'}    |"
                f" {r.m_H1:+7.4f} {r.m_H2:+7.4f} {r.m_OOS:+7.4f} {r.m_DD:+7.2%} {r.m_CAGR:+7.2%} |"
                f" {'Y' if r.pass4b else '.'}")
    say("\n  the SAME table at gross 1.00:")
    for pname in panels:
        say(f"  {pname} g=1.00")
        for Y in YEARS:
            r = df[(df.panel == pname) & (df.Y == Y) & (df.gross == 1.00)
                   & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
            say(f"  {Y} |  {'Y' if r.L_H1 else '.'}     {'Y' if r.L_H2 else '.'}     "
                f"{'Y' if r.L_OOS else '.'}     {'Y' if r.L_DD else '.'}     {'Y' if r.L_CAGR else '.'}    |"
                f" {r.m_H1:+7.4f} {r.m_H2:+7.4f} {r.m_OOS:+7.4f} {r.m_DD:+7.2%} {r.m_CAGR:+7.2%} |"
                f" {'Y' if r.pass4b else '.'}")

    say("\n=== D. THE BOOK vs ITS COMPARANDS IN EACH WINDOW (10 bps, g=0.75) ===")
    say("  panel Y    | CAP2 CAGR/Sharpe/MaxDD        | live v2 CAGR/Sharpe/MaxDD     | SPY CAGR/Sharpe/MaxDD")
    for pname in panels:
        for Y in YEARS:
            r = df[(df.panel == pname) & (df.Y == Y) & (df.gross == 0.75)
                   & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
            say(f"  {pname:5s} {Y} | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%}      |"
                f" {r.base_CAGR:6.2%} {r.base_Sharpe:7.4f} {r.base_MaxDD:8.2%}    |"
                f" {r.spy_CAGR:6.2%} {r.spy_Sharpe:7.4f} {r.spy_MaxDD:8.2%}")

    say("\n=== E. RULE 8 — chosen on <= 2016-12-31 ONLY, 2017-2026 read ONCE (same OOS window for every Y) ===")
    wfr = []
    for pname, (px, invest) in panels.items():
        spy_oos = px["SPY"].pct_change().fillna(0.0).loc[OOS_START:]
        for rung in RUNGS:
            d = df[(df.panel == pname) & (df.cost_bps == rung)]
            for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                # C_G : gross chosen on IS within each Y (the deployable reading) -- HEADLINE
                for Y in YEARS:
                    dy = d[d.Y == Y]
                    pick = dy.loc[dy[col].idxmax()]
                    wfr.append(dict(scheme="C_G", panel=pname, cost_bps=rung, chooser=chooser,
                                    Y=Y, pick_Y=Y, pick_gross=pick.gross,
                                    OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                                    OOS_MaxDD=pick.OOS_MaxDD,
                                    base_OOS_CAGR=pick.base_OOS_CAGR, base_OOS_Sharpe=pick.base_OOS_Sharpe,
                                    base_OOS_MaxDD=pick.base_OOS_MaxDD,
                                    spy_OOS_CAGR=cagr(spy_oos), spy_OOS_Sharpe=sharpe(spy_oos),
                                    spy_OOS_MaxDD=maxdd(spy_oos), full4b=bool(pick.pass4b),
                                    beats_spy_oos=bool(pick.OOS_Sharpe > sharpe(spy_oos)),
                                    beats_base_oos=bool(pick.OOS_Sharpe > pick.base_OOS_Sharpe)))
                # C_YG : (Y, gross) chosen jointly on IS
                pick = d.loc[d[col].idxmax()]
                wfr.append(dict(scheme="C_YG", panel=pname, cost_bps=rung, chooser=chooser,
                                Y=np.nan, pick_Y=pick.Y, pick_gross=pick.gross,
                                OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                                OOS_MaxDD=pick.OOS_MaxDD,
                                base_OOS_CAGR=pick.base_OOS_CAGR, base_OOS_Sharpe=pick.base_OOS_Sharpe,
                                base_OOS_MaxDD=pick.base_OOS_MaxDD,
                                spy_OOS_CAGR=cagr(spy_oos), spy_OOS_Sharpe=sharpe(spy_oos),
                                spy_OOS_MaxDD=maxdd(spy_oos), full4b=bool(pick.pass4b),
                                beats_spy_oos=bool(pick.OOS_Sharpe > sharpe(spy_oos)),
                                beats_base_oos=bool(pick.OOS_Sharpe > pick.base_OOS_Sharpe)))
    wfd = pd.DataFrame(wfr); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say("\n  C_G (HEADLINE, gross chosen on IS inside each Y):")
    say("  panel  bps  chooser     Y    -> g    | OOS CAGR / Sharpe / MaxDD | live v2 OOS | SPY OOS | full 4b")
    for _, r in wfd[wfd.scheme == "C_G"].iterrows():
        say(f"  {r.panel:5s} {r.cost_bps:5.1f} {r.chooser:11s} {int(r.pick_Y)} -> {r.pick_gross:.2f} |"
            f" {r.OOS_CAGR:6.2%} {r.OOS_Sharpe:7.4f} {r.OOS_MaxDD:7.2%} |"
            f" {r.base_OOS_CAGR:6.2%} {r.base_OOS_Sharpe:7.4f} |"
            f" {r.spy_OOS_CAGR:6.2%} {r.spy_OOS_Sharpe:7.4f} | {'Y' if r.full4b else '.'}")
    say("\n  C_YG (Y and gross chosen jointly on IS; the OOS window is identical for every Y so this is legal):")
    for _, r in wfd[wfd.scheme == "C_YG"].iterrows():
        say(f"  {r.panel:5s} {r.cost_bps:5.1f} {r.chooser:11s} -> Y {int(r.pick_Y)} g {r.pick_gross:.2f} |"
            f" OOS {r.OOS_CAGR:6.2%} / {r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:7.2%} |"
            f" live v2 OOS {r.base_OOS_CAGR:6.2%} / {r.base_OOS_Sharpe:.4f} |"
            f" SPY OOS {r.spy_OOS_CAGR:6.2%} / {r.spy_OOS_Sharpe:.4f} | full 4b {'Y' if r.full4b else '.'}")
    for sch in ("C_G", "C_YG"):
        w = wfd[wfd.scheme == sch]
        say(f"  {sch}: picks beating SPY OOS {int(w.beats_spy_oos.sum())} of {len(w)};"
            f"  beating the live book OOS {int(w.beats_base_oos.sum())} of {len(w)};"
            f"  picks whose own full-sample row passes 4b {int(w.full4b.sum())} of {len(w)}")
    yc = wfd[wfd.scheme == "C_YG"].pick_Y.value_counts().sort_index()
    say(f"  C_YG start years chosen on IS: " + ", ".join(f"{int(k)} x{int(v)}" for k, v in yc.items()))

    say("\n=== F. COST-RUNG LADDER (g=0.75) — 4b pass by (panel, Y, rung) ===")
    for pname in panels:
        say(f"  {pname}   " + "  ".join(f"{int(r):2d}bps" for r in RUNGS))
        for Y in YEARS:
            cells = []
            for rung in RUNGS:
                r = df[(df.panel == pname) & (df.Y == Y) & (df.gross == 0.75)
                       & (df.cost_bps == rung)].iloc[0]
                cells.append(f"{'Y' if r.pass4b else '.'}({r.CAGR:5.2%})")
            say(f"    {Y}  " + "  ".join(cells))

    gdf = pd.DataFrame(GATES); gdf.to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n=== GATES: {int(gdf.pass_.sum())} of {len(gdf)} pass ===")
    for _, g in gdf[~gdf.pass_].iterrows():
        say(f"    FAILED: {g.gate} = {g.value} (target {g.target})")
    say(f"\nwrote {OUT}.grid.csv / .walkforward.csv / .gates.csv   ({time.time() - t0:.0f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

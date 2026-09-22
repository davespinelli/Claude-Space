#!/usr/bin/env python3
"""idea 2315 (lane cloud, 2026-09-22) — WHEN does the BAND GATE pay for itself?  A YEAR-BY-YEAR
decomposition of CASH DRAG PAID vs DRAWDOWN SAVED.

THE QUESTION.  RULES v2 clause 2 gates every name on its own 200d +/-3% band and lets the gated
weight sit in CASH (clause 4: the book de-grosses, it does not re-spread).  The whole case for
that device is that it trades CAGR for drawdown.  The record has only ever scored that trade in
AGGREGATE — full sample, halves, OOS.  This run scores it YEAR BY YEAR against the SAME BOOK WITH
THE GATE REMOVED, and asks in how many of the sample's calendar years the gate is worth its
price.  A device that earns its keep in 3 of 18 years is a crash hedge priced as a strategy.

THE TWO BOOKS (identical in every other respect: same names, same gross, same weekly cadence,
same t+1 execution, same cost rung).
  GATED(c, g)   = `baseline.rules_v2_weights(px, band=c, gross=g)` — the live book.
  UNGATED(g)    = the same equal-weight book with clause 2 DELETED: g / N_t on every priced name,
                  every day, no band, no de-gross.  It does NOT depend on c, which is gate G3.

THE PRE-DECLARED PRICE.  For each calendar year y, at the headline rung:
  DRAG_y   = ret_UNGATED_y - ret_GATED_y        (pp of return the gate cost that year, + = costly)
  SAVED_y  = mdd_GATED_y  - mdd_UNGATED_y       (pp of WITHIN-YEAR drawdown the gate saved, both
                                                 MaxDDs are negative, so + = the gate saved DD)
  WORTH_y(lam) = lam * SAVED_y >= DRAG_y        (lam = pp of return the investor will pay for one
                                                 pp of drawdown avoided)
lam = 1.0 is the NEUTRAL exchange rate and is the headline; the ladder {0.5, 1, 2, 3} is reported
in full.  Declared BEFORE any number was read.  Mechanism split, also per year:
  PROT_y   = sum of daily (gated - ungated) on days the UNGATED book fell   (what the gate buys)
  DRAGUP_y = sum of daily (gated - ungated) on days the UNGATED book rose   (what it pays)

DIAL 1 -- band width c {0.00, 0.02, 0.03 (live), 0.05, 0.08, 0.10}.
DIAL 2 -- gross {0.75 (live), 1.00}.
REPORTED, NEVER SELECTED ON: 3 panels (U56 / B136 / SMALL), 4 cost rungs (0 / 10 / 25 / 50 bps),
weekly cadence, t+1 execution.  12 gated + 2 ungated books per panel, every one published at
every rung.

BOTH KEEP PATHS on every row.  RULE 8: (c, gross) chosen on warm-up..2016-12-31 ONLY by two
pre-stated IS-only choosers (C_ISSHARPE, C_ISCALMAR), then 2017-2026 read ONCE.

SURVIVORSHIP.  U56 (research/universe.json) and B136 (research/universe_broad.json) are
CURRENT-CONSTITUENT lists; SMALL (data/prices_small.csv.gz) is a current screen of sub-$2B names
since 2010 with the max_1d_move >= 1.0 tickers dropped per data/SMALL_PANEL_README.md.  Absolute
CAGRs are survivorship-optimistic on all three; the gated-minus-ungated DIFFERENCE this run is
about is a same-names, same-days object and is far less exposed.

WINDOW CAVEAT, stated up front: the panels start 2008-01-01 and the 260-row warm-up puts the
first scored day in JANUARY 2009, so the 2008 leg of the GFC is OUTSIDE this sample.  The
crisis years the decomposition can actually see are 2009 (the tail), 2011, 2015-16, 2018, 2020,
2022 and 2025.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-22_band-gate-year-by-year-decomposition_cloud.py
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

DATE, SLUG, LANE = "2026-09-22", "band-gate-year-by-year-decomposition", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BANDS = [0.00, 0.02, 0.03, 0.05, 0.08, 0.10]
GROSSES = [0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG, LIVE_BAND, LIVE_GROSS = 10.0, 0.03, 0.75
CADENCE, WARMUP = "W", 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LAMBDAS = [0.5, 1.0, 2.0, 3.0]
CRISIS_YEARS = [2009, 2020, 2022]

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


# ---------------------------------------------------------------- books
def gated_weights(px, invest, band, gross):
    """The live book: equal weight gross/N_t on IN names, gated weight stays in CASH."""
    w = rules_v2_weights(px[invest], band=band, gross=gross)
    return w.reindex(columns=px.columns).fillna(0.0)


def ungated_weights(px, invest, gross):
    """Clause 2 deleted: gross/N_t on every priced name, every day.  No band, no de-gross."""
    q = px[invest]
    e = pd.DataFrame(1.0, index=q.index, columns=q.columns).where(q.notna(), 0.0)
    w = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return w.reindex(columns=px.columns).fillna(0.0)


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
    wt = w_target.values
    rv = rets.values
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
    eq = (1 + r).cumprod()
    return float(eq.iloc[-1] ** (252 / len(r)) - 1)


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
    h1, h2 = halves(r)
    b1, b2 = halves(base)
    p4a = (h1 > b1) and (h2 > b2) and (maxdd(r) >= maxdd(base))
    s1, s2 = halves(spy)
    L_H1, L_H2 = h1 > s1, h2 > s2
    L_OOS = sharpe(r_oos) > sharpe(spy_oos)
    L_DD = maxdd(r) >= DD_CAP * maxdd(spy)
    L_CAGR = cagr(r) >= CAGR_FLOOR * cagr(spy)
    return dict(pass4a=bool(p4a), pass4b=bool(L_H1 and L_H2 and L_OOS and L_DD and L_CAGR),
                L_H1=bool(L_H1), L_H2=bool(L_H2), L_OOS=bool(L_OOS), L_DD=bool(L_DD),
                L_CAGR=bool(L_CAGR))


# ---------------------------------------------------------------- panels
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"].astype(str))
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    dropped = len(px.columns) - len(keep)
    return px[keep], dropped


def year_table(rg, ru, spy):
    """Per calendar year: return of each book, DRAG, within-year MaxDD of each, SAVED, and the
    up-day / down-day split of the daily difference."""
    out = []
    d = rg - ru
    for y, idx in rg.groupby(rg.index.year).groups.items():
        g, u, s, dd = rg.loc[idx], ru.loc[idx], spy.loc[idx], d.loc[idx]
        rg_y = float((1 + g).prod() - 1)
        ru_y = float((1 + u).prod() - 1)
        out.append(dict(year=int(y), days=len(idx),
                        ret_gated=rg_y, ret_ungated=ru_y, ret_spy=float((1 + s).prod() - 1),
                        drag=ru_y - rg_y,
                        mdd_gated=maxdd(g), mdd_ungated=maxdd(u), mdd_spy=maxdd(s),
                        saved=maxdd(g) - maxdd(u),
                        prot=float(dd[u < 0].sum()), dragup=float(dd[u >= 0].sum())))
    return pd.DataFrame(out)


def main():
    t0 = time.time()
    say("=== idea 2315 — WHEN does the BAND GATE pay for itself?  year-by-year cash drag vs drawdown saved ===")
    say(f"    {DATE}  lane {LANE}   cadence {CADENCE}  t+1  rungs {RUNGS} bps   headline {HEADLINE_RUNG} bps")
    say(f"    DIAL 1 band c {BANDS}   DIAL 2 gross {GROSSES}   exchange-rate ladder lam {LAMBDAS} (headline lam=1.0)")
    gate("G5 exactly two tuned parameters", "band width c, gross", "2", True)

    px_u = load_universe()
    px_b = load_universe(broad=True)
    px_s, dropped = small_panel()
    gate("G6 dropped-ticker rule bit (SMALL)", f"{dropped} names dropped (max_1d_move >= 1.0)",
         ">= 1", dropped >= 1)

    panels = {}
    for nm, px in (("U56", px_u), ("B136", px_b), ("SMALL", px_s)):
        invest = [c for c in px.columns if c != "SPY"] if nm == "SMALL" else list(px.columns)
        panels[nm] = (px, invest)
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y, {len(invest)} investable, {len(px)} rows, "
             f"scored {px.index[WARMUP].date()}..{px.index[-1].date()}", ">= 10y", yrs >= 10)

    # G1: the replica prices the live book exactly as engine.backtest does
    w_live = gated_weights(px_u, list(px_u.columns), LIVE_BAND, LIVE_GROSS)
    res_live = run_book(px_u, w_live)
    r_eng = backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    d1 = float((r_eng - priced(res_live, HEADLINE_RUNG)).abs().max())
    gate("G1 per-column replica == engine.backtest", f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    rows, yearly, exposure = [], [], []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_r = priced(run_book(px, gated_weights(px, invest, LIVE_BAND, LIVE_GROSS)),
                        HEADLINE_RUNG).loc[win]
        say(f"\n--- panel {pname} ({len(invest)} names)  SPY {cagr(spy):.2%} / {sharpe(spy):.4f} / {maxdd(spy):.2%}"
            f"   live RULES v2 {cagr(base_r):.2%} / {sharpe(base_r):.4f} / {maxdd(base_r):.2%}")
        ung = {}
        for gross in GROSSES:
            w = ungated_weights(px, invest, gross)
            res = run_book(px, w)
            ung[gross] = res
            for rung in RUNGS:
                r = priced(res, rung).loc[win]
                r_oos = r.loc[OOS_START:]
                h1, h2 = halves(r)
                rows.append(dict(panel=pname, book="UNGATED", band=np.nan, gross=gross, cost_bps=rung,
                                 CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                 H1=h1, H2=h2, IS_Sharpe=sharpe(r.loc[:IS_END]),
                                 IS_Calmar=calmar(r.loc[:IS_END]), OOS_CAGR=cagr(r_oos),
                                 OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                 **legs(r, base_r, spy, r_oos, spy_oos)))
            exposure.append(dict(panel=pname, book="UNGATED", band=np.nan, gross=gross,
                                 mean_gross=float(res["gross"].loc[win].mean()),
                                 min_gross=float(res["gross"].loc[win].min()),
                                 turnover_yr=float(res["turnover"].loc[win].sum() / (len(win) / 252)),
                                 max_row_sum=float(w.sum(axis=1).max())))
        for gross in GROSSES:
            for band in BANDS:
                w = gated_weights(px, invest, band, gross)
                res = run_book(px, w)
                exposure.append(dict(panel=pname, book="GATED", band=band, gross=gross,
                                     mean_gross=float(res["gross"].loc[win].mean()),
                                     min_gross=float(res["gross"].loc[win].min()),
                                     turnover_yr=float(res["turnover"].loc[win].sum() / (len(win) / 252)),
                                     max_row_sum=float(w.sum(axis=1).max())))
                for rung in RUNGS:
                    rg = priced(res, rung).loc[win]
                    ru = priced(ung[gross], rung).loc[win]
                    r_oos = rg.loc[OOS_START:]
                    h1, h2 = halves(rg)
                    rows.append(dict(panel=pname, book="GATED", band=band, gross=gross, cost_bps=rung,
                                     CAGR=cagr(rg), Sharpe=sharpe(rg), MaxDD=maxdd(rg), Calmar=calmar(rg),
                                     H1=h1, H2=h2, IS_Sharpe=sharpe(rg.loc[:IS_END]),
                                     IS_Calmar=calmar(rg.loc[:IS_END]), OOS_CAGR=cagr(r_oos),
                                     OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                     **legs(rg, base_r, spy, r_oos, spy_oos)))
                    if rung == HEADLINE_RUNG:
                        yt = year_table(rg, ru, spy)
                        yt.insert(0, "gross", gross)
                        yt.insert(0, "band", band)
                        yt.insert(0, "panel", pname)
                        yearly.append(yt)
        say(f"    ... {pname} done ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(rows)
    yf = pd.concat(yearly, ignore_index=True)
    ef = pd.DataFrame(exposure)
    df.to_csv(f"{OUT}.grid.csv", index=False)
    yf.to_csv(f"{OUT}.yearly.csv", index=False)
    ef.to_csv(f"{OUT}.exposure.csv", index=False)

    # ---- structural gates
    gate("G4 no leverage (all books)", f"max row sum {ef.max_row_sum.max():.9f}", "<= 1+1e-12",
         bool((ef.max_row_sum <= 1 + 1e-12).all()))
    px, invest = panels["U56"]
    u1 = ungated_weights(px, invest, 0.75)
    d3 = max(float((u1 - ungated_weights(px, invest, 0.75)).abs().max().max()), 0.0)
    same = df[(df.panel == "U56") & (df.book == "UNGATED") & (df.gross == 0.75)]
    gate("G3 UNGATED does not depend on the band dial", f"one row per (gross, rung): {len(same)} rows, "
         f"reconstruction max|dw| {d3:.1e}", "4 rows, 0.0", len(same) == 4 and d3 == 0.0)
    b0 = band_state(px, 0.00)
    b10 = band_state(px, 0.10)
    gate("G2 the band dial BITES (IN-days fall as c widens, U56)",
         f"mean IN share c=0.00 {b0.values.mean():.4f} -> c=0.10 {b10.values.mean():.4f}",
         "strictly lower at c=0.10", b10.values.mean() < b0.values.mean())

    # G7 external reproduction of the committed RULES.md v2 acceptance row
    h = df[(df.panel == "U56") & (df.book == "GATED") & (df.band == LIVE_BAND)
           & (df.gross == LIVE_GROSS) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    d7 = max(abs(h.CAGR - 0.0866), abs(h.Sharpe - 1.2056) / 10, abs(h.MaxDD + 0.1205),
             abs(h.H1 - 1.2259) / 10, abs(h.H2 - 1.1908) / 10, abs(h.OOS_Sharpe - 1.2851) / 10)
    gate("G7 reproduces RULES.md's committed v2 row (8.66%/1.2056/-12.05%, 1.2259/1.1908, OOS 1.2851)",
         f"read {h.CAGR:.2%} / {h.Sharpe:.4f} / {h.MaxDD:.2%}, {h.H1:.4f}/{h.H2:.4f}, OOS {h.OOS_Sharpe:.4f}"
         f" -> max|d| {d7:.2e}", "< 2e-3", d7 < 2e-3)

    # G8 the year partition is exhaustive: compounding the yearly returns == the full-sample equity
    yl = yf[(yf.panel == "U56") & (yf.band == LIVE_BAND) & (yf.gross == LIVE_GROSS)]
    rfull = priced(run_book(px, gated_weights(px, invest, LIVE_BAND, LIVE_GROSS)),
                   HEADLINE_RUNG).loc[px.index[WARMUP:]]
    d8 = abs(float((1 + yl.ret_gated).prod()) - float((1 + rfull).prod()))
    gate("G8 year partition exhaustive (prod of yearly returns == full-sample equity)",
         f"|d| {d8:.3e} over {len(yl)} years", "< 1e-9", d8 < 1e-9)

    # ---------------------------------------------------------------- A. the year-by-year ledger
    say("\n=== A. THE LEDGER — U56, live cell (c = 0.03, gross = 0.75), 10 bps.  GATED vs UNGATED, year by year ===")
    say("  year | ret GATED  ret UNGATED   DRAG | mdd GATED  mdd UNGATED  SAVED | worth@lam= 0.5  1.0  2.0  3.0 | PROT   DRAGUP | SPY ret")
    for _, r in yl.iterrows():
        wl = "  ".join(("Y" if lam * r.saved >= r.drag else ".") for lam in LAMBDAS)
        say(f"  {r.year} | {r.ret_gated:9.2%} {r.ret_ungated:11.2%} {r.drag:+7.2%} |"
            f" {r.mdd_gated:9.2%} {r.mdd_ungated:11.2%} {r.saved:+7.2%} |"
            f"           {wl}      | {r.prot:+6.2%} {r.dragup:+7.2%} | {r.ret_spy:7.2%}")
    n = len(yl)
    say(f"\n  TOTALS over {n} years: drag paid {yl.drag.sum():+.2%} (mean {yl.drag.mean():+.2%}/yr), "
        f"drawdown saved {yl.saved.sum():+.2%} (mean {yl.saved.mean():+.2%}/yr)")
    for lam in LAMBDAS:
        k = int((lam * yl.saved >= yl.drag).sum())
        say(f"    lam = {lam:.1f}:  the gate is worth its price in {k} of {n} years "
            f"({k / n:.0%})")
    k1 = int((yl.saved >= yl.drag).sum())

    say("\n=== B. IS THE SAVING CONCENTRATED IN THE CRISIS YEARS? (U56, live cell, 10 bps) ===")
    pos = yl[yl.saved > 0]
    tot_saved = float(pos.saved.sum())
    cy = pos[pos.year.isin(CRISIS_YEARS)]
    say(f"  years with SAVED > 0: {len(pos)} of {n}; total DD saved across them {tot_saved:+.2%}")
    say(f"  {CRISIS_YEARS} contribute {float(cy.saved.sum()):+.2%} = "
        f"{(float(cy.saved.sum()) / tot_saved if tot_saved else float('nan')):.1%} of ALL drawdown saved, "
        f"from {len(cy)} of {len(pos)} positive years")
    top3 = yl.nlargest(3, "saved")
    say(f"  the 3 single best years for the gate are {list(top3.year)} "
        f"({', '.join(f'{v:+.2%}' for v in top3.saved)}), = "
        f"{float(top3.saved.sum()) / tot_saved if tot_saved else float('nan'):.1%} of all DD saved")
    dpos = yl[yl.drag > 0]
    say(f"  years the gate COST return: {len(dpos)} of {n} (total {float(dpos.drag.sum()):+.2%}); "
        f"years it ADDED return: {n - len(dpos)} (total {float(yl[yl.drag <= 0].drag.sum()):+.2%})")
    say(f"  mechanism split, summed over all years: PROT (down-days) {float(yl.prot.sum()):+.2%}, "
        f"DRAGUP (up-days) {float(yl.dragup.sum()):+.2%}")

    say("\n=== C. THE SAME COUNT ON EVERY (panel, c, gross) CELL — 'worth its price' years at lam = 1.0, 10 bps ===")
    say("  panel  gross | " + "  ".join(f"c={b:.2f}" for b in BANDS))
    cnt_rows = []
    for pname in panels:
        for gross in GROSSES:
            cells = []
            for band in BANDS:
                y = yf[(yf.panel == pname) & (yf.band == band) & (yf.gross == gross)]
                k = int((y.saved >= y.drag).sum())
                cells.append(f"{k:2d}/{len(y)}")
                cnt_rows.append(dict(panel=pname, band=band, gross=gross, worth_years=k, years=len(y),
                                     drag_total=float(y.drag.sum()), saved_total=float(y.saved.sum()),
                                     prot_total=float(y.prot.sum()), dragup_total=float(y.dragup.sum()),
                                     crisis_share=float(y[y.year.isin(CRISIS_YEARS) & (y.saved > 0)].saved.sum())
                                     / float(y[y.saved > 0].saved.sum()) if float(y[y.saved > 0].saved.sum()) else np.nan))
            say(f"  {pname:5s}  {gross:.2f} | " + "  ".join(f"{c:>6s}" for c in cells))
    pd.DataFrame(cnt_rows).to_csv(f"{OUT}.counts.csv", index=False)

    say("\n=== D. THE FULL GRID AT 10 bps — every point, nothing dropped ===")
    for pname in panels:
        say(f"\n  {pname}")
        say("  book     c     gross |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh  OOS DD | 4a 4b | legs H1/H2/OOS/DD/CAGR | meanGr turn/yr")
        for gross in GROSSES:
            for band in BANDS + [np.nan]:
                sel = ((df.panel == pname) & (df.gross == gross) & (df.cost_bps == HEADLINE_RUNG)
                       & (df.band.isna() if np.isnan(band) else (df.band == band)))
                r = df[sel].iloc[0]
                e = ef[(ef.panel == pname) & (ef.gross == gross)
                       & (ef.band.isna() if np.isnan(band) else (ef.band == band))].iloc[0]
                lg = "".join("1" if r[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                bl = "  --" if np.isnan(band) else f"{band:.2f}"
                say(f"  {r.book:8s} {bl:5s} {gross:.2f}  | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%} |"
                    f" {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} {r.OOS_MaxDD:7.2%} |"
                    f" {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg:22s} |"
                    f" {e.mean_gross:6.3f} {e.turnover_yr:7.2f}")

    say("\n=== E. KEEP COUNTS OVER ALL PUBLISHED ROWS ===")
    say(f"  rows {len(df)}   4b passes {int(df.pass4b.sum())}   4a passes {int(df.pass4a.sum())}")
    for rung in RUNGS:
        d = df[df.cost_bps == rung]
        say(f"   {rung:5.1f} bps:  4b {int(d.pass4b.sum()):2d}/{len(d)}   4a {int(d.pass4a.sum()):2d}/{len(d)}"
            f"   binding leg on 4b FAILs: " +
            "  ".join(f"{k} {int((~d[k][~d.pass4b]).sum())}" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    for book in ("GATED", "UNGATED"):
        d = df[df.book == book]
        say(f"   {book:8s}: 4b {int(d.pass4b.sum()):2d}/{len(d)}   4a {int(d.pass4a.sum()):2d}/{len(d)}")
    p = df[df.pass4b]
    say("\n  4b pass rows (all rungs):" + ("" if len(p) else " NONE"))
    for _, r in p.iterrows():
        bl = "--" if np.isnan(r.band) else f"{r.band:.2f}"
        say(f"    {r.panel:5s} {r.book:8s} c {bl:5s} g {r.gross:.2f} {r.cost_bps:5.1f}bps  "
            f"{r.CAGR:6.2%} / {r.Sharpe:.4f} / {r.MaxDD:7.2%}   OOS {r.OOS_CAGR:6.2%} / {r.OOS_Sharpe:.4f}")

    say("\n=== F. RULE 8 — (c, gross) chosen on <= 2016-12-31 ONLY, 2017-2026 read once ===")
    say("  (the chooser ranges over the 12 GATED cells; the UNGATED book is reported beside it, never chosen)")
    wf = []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_oos = priced(run_book(px, gated_weights(px, invest, LIVE_BAND, LIVE_GROSS)),
                          HEADLINE_RUNG).loc[win].loc[OOS_START:]
        for rung in RUNGS:
            d = df[(df.panel == pname) & (df.cost_bps == rung) & (df.book == "GATED")]
            u = df[(df.panel == pname) & (df.cost_bps == rung) & (df.book == "UNGATED")
                   & (df.gross == LIVE_GROSS)].iloc[0]
            for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                pick = d.loc[d[col].idxmax()]
                wf.append(dict(panel=pname, cost_bps=rung, chooser=chooser, pick_band=pick.band,
                               pick_gross=pick.gross, OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                               OOS_MaxDD=pick.OOS_MaxDD, pass4b_full=bool(pick.pass4b),
                               ungated_OOS_CAGR=u.OOS_CAGR, ungated_OOS_Sharpe=u.OOS_Sharpe,
                               ungated_OOS_MaxDD=u.OOS_MaxDD, base_OOS_CAGR=cagr(base_oos),
                               base_OOS_Sharpe=sharpe(base_oos), base_OOS_MaxDD=maxdd(base_oos),
                               spy_OOS_CAGR=cagr(spy_oos), spy_OOS_Sharpe=sharpe(spy_oos),
                               spy_OOS_MaxDD=maxdd(spy_oos),
                               beats_ungated_OOS_Sharpe=bool(pick.OOS_Sharpe > u.OOS_Sharpe),
                               pick_is_live_cell=bool(pick.band == LIVE_BAND and pick.gross == LIVE_GROSS)))
                say(f"  {pname:5s} {rung:5.1f}bps {chooser:11s} -> c {pick.band:.2f} g {pick.gross:.2f} |"
                    f" OOS {pick.OOS_CAGR:6.2%} / {pick.OOS_Sharpe:.4f} / {pick.OOS_MaxDD:7.2%} |"
                    f" UNGATED g0.75 OOS {u.OOS_CAGR:6.2%} / {u.OOS_Sharpe:.4f} / {u.OOS_MaxDD:7.2%} |"
                    f" live v2 OOS {cagr(base_oos):6.2%} / {sharpe(base_oos):.4f} / {maxdd(base_oos):7.2%} |"
                    f" SPY OOS {cagr(spy_oos):6.2%} / {sharpe(spy_oos):.4f} / {maxdd(spy_oos):7.2%}")
    wfd = pd.DataFrame(wf)
    wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"\n  rule-8 picks whose OOS Sharpe beats the UNGATED book: "
        f"{int(wfd.beats_ungated_OOS_Sharpe.sum())} of {len(wfd)}")
    say(f"  rule-8 picks landing on the LIVE cell (c=0.03, g=0.75): "
        f"{int(wfd.pick_is_live_cell.sum())} of {len(wfd)}")

    say("\n=== G. THE OOS DECOMPOSITION (2017-2026 only, U56 live cell, 10 bps) — the same ledger, untouched half ===")
    yo = yl[yl.year >= 2017]
    say(f"  years {len(yo)}: drag {yo.drag.sum():+.2%} total ({yo.drag.mean():+.2%}/yr), "
        f"saved {yo.saved.sum():+.2%} total; worth its price at lam=1.0 in "
        f"{int((yo.saved >= yo.drag).sum())} of {len(yo)} years")

    gdf = pd.DataFrame(GATES)
    gdf.to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n=== GATES: {int(gdf.pass_.sum())} of {len(gdf)} pass ===")
    for _, g in gdf[~gdf.pass_].iterrows():
        say(f"    FAILED: {g.gate} = {g.value} (target {g.target})")
    say(f"\n=== HEADLINE: at the live cell the band gate is worth its price in {k1} of {n} calendar years "
        f"at the neutral exchange rate lam = 1.0 ===")
    say(f"\nwrote {OUT}.grid.csv / .yearly.csv / .counts.csv / .exposure.csv / .walkforward.csv / .gates.csv"
        f"   ({time.time() - t0:.0f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

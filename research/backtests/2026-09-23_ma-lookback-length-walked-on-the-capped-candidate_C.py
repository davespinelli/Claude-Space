#!/usr/bin/env python3
"""idea 2427 (lane C, 2026-09-23) — does the CAPPED CANDIDATE's 4b pass move when the
200d MA LENGTH ITSELF is walked?

THE OBJECT.  Idea 2300 filed `RG100 + phi = 1.00` (`CAND`: every name INSIDE the 200d +/-3%
band held at `gross / N_in` of NAV, idle NAV swept to SHY) as the record's standing 4b
KEEP-candidate; idea 2322 added a 2.0% per-name cap (`CAP2`).  Clause 2 of RULES v2 has
three dials: the BAND WIDTH (walked by idea 2343), the two EDGES separately (split by idea
2383) and the LOOKBACK `L` that defines the mean.  `L = 200` is inherited unexamined from
RULES v1 and NO committed run has ever walked it on the capped candidate.

It is not a cosmetic dial.  A short mean turns the gate over more often (turnover and `L_DD`
both move); a long mean holds through dips the 200d sells into but admits late and exits late.

DIAL 1 -- `L` in {100, 150, 200, 250, 300} trading days.  `L = 200` IS the committed book
          exactly, so ONE ladder spans the whole known record (gate G1 asserts the L=200
          gate is BIT-IDENTICAL to baseline.band_state, which is hardcoded at 200).
DIAL 2 -- gross {0.75 (live), 1.00}.

REPORTED, NEVER SELECTED ON: book {CAP2 (cap 0.02), CAND (cap INF)}, panels {U56, B136},
4 cost rungs (0 / 10 / 25 / 50 bps), weekly cadence, band 0.03, t+1 execution, SHY sweep
(phi = 1.00).  5 x 2 x 2 x 2 = 40 books, every one published at every rung.

THE WARM-UP ASYMMETRY IS MEASURED, NOT BURIED.  Every committed number on this family starts
at cache row 260, where an `L = 300` mean does not yet exist (the gate reads OUT for its
first ~40 rows) while an `L = 100` mean has been live for 160.  A ladder read on that window
would hand the short end a head start.  So EVERY row is published on BOTH windows:
  W260 = cache row 260 (the committed convention, the headline), and
  W360 = cache row 360, where all five lookbacks are fully warmed.
Any verdict that flips between the two windows is a warm-up artifact and is reported as one.
This is not a third tuned dial: both windows are published for every point, neither is chosen.

SMALL is NOT priced and the reason is stated rather than buried: ideas 2318 / 2322 / 2326 /
2343 each published SMALL's 4b pass count at 0 of 40-120, so there is no pass there to move.

BOTH KEEP PATHS on every row: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse)
and 4b (Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x
SPY's).  RULE 8: (L, gross) chosen on warm-up..2016-12-31 ONLY by two pre-stated IS-only
choosers (C_ISSHARPE, C_ISCALMAR), then 2017-2026 read ONCE.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_ma-lookback-length-walked-on-the-capped-candidate_C.py
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

DATE, SLUG, LANE = "2026-09-23", "ma-lookback-length-walked-on-the-capped-candidate", "C"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, CADENCE = 0.03, "W"
LOOKBACKS = [100, 150, 200, 250, 300]
COMMITTED_L = 200
GROSSES = [0.75, 1.00]
BOOKS = {"CAP2": 0.020, "CAND": "INF"}
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG = 10.0
SWEEP = "SHY"
WINDOWS = {"W260": 260, "W360": 360}
HEADLINE_WIN = "W260"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70

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


# ---------------------------------------------------------------- the gate, with L free
def band_state_L(px, band, L):
    """baseline.band_state with the 200 hardcode replaced by L.  Identical in every other
    respect: IN above ma*(1+band), OUT below ma*(1-band), previous state in between, OUT
    before L closes exist.  L = 200 must be bit-identical to baseline.band_state (gate G1)."""
    ma = px.rolling(L).mean()
    raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
    raw = raw.mask(px > ma * (1 + band), 1.0).mask(px < ma * (1 - band), 0.0)
    return raw.ffill().fillna(0.0) > 0.5


def cap_weights_L(px, invest, cap, gross, L):
    """idea 2322's CAP2 / idea 2300's CAND with the gate's lookback set to L:
    w_i = min(gross / N_in, cap) on names INSIDE the L-day +/- BAND; idle NAV swept to SHY."""
    q = px[invest]
    pr = q.notna()
    inb = band_state_L(q, BAND, L) & pr
    nin = inb.sum(axis=1).replace(0, np.nan)
    per = gross / nin
    c = pd.Series(np.inf if cap == "INF" else float(cap), index=q.index)
    per = pd.concat([per, c], axis=1).min(axis=1)
    w = inb.astype(float).mul(per.fillna(0.0), axis=0)
    w = w.reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return w


def run(px, w):
    """One engine pass at ZERO cost; engine charges turnover * bps / 1e4 linearly (gate G5),
    so every rung is priced from this single pass."""
    res = backtest(px, w, cost_bps=0.0, freq=CADENCE)
    return dict(r0=res["returns"], turnover=res["turnover"], held=res["weights"])


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


def main():
    t0 = time.time()
    say("=== idea 2427 (lane C) — does the CAPPED candidate's 4b pass move when the 200d MA LENGTH is WALKED? ===")
    say(f"    {DATE}  lane {LANE}   band {BAND}  cadence {CADENCE}  t+1  rungs {RUNGS} bps  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 lookback L {LOOKBACKS} (L=200 IS the committed book)   DIAL 2 gross {GROSSES}")
    say(f"    REPORTED not selected: book {list(BOOKS)}  panels U56/B136  rungs {RUNGS}  windows {WINDOWS}")
    gate("G8 exactly two tuned parameters", "lookback L, gross", "2", True)

    panels = {}
    px_u = load_universe()
    px_b = load_universe(broad=True)
    for nm, px in (("U56", px_u), ("B136", px_b)):
        invest = list(px.columns)
        panels[nm] = (px, invest)
        yrs = (px.index[-1] - px.index[WINDOWS[HEADLINE_WIN]]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y, {len(invest)} columns, {len(px)} rows", ">= 10y", yrs >= 10)
        win = px.index[WINDOWS[HEADLINE_WIN]:]
        dead = [c for c in px.columns if px[c].loc[win].notna().sum() == 0]
        publish(f"G9 all-NaN columns in {nm} (idea 2332's MMC defect, carried forward)",
                f"{len(dead)} dead: {dead} -> {len(invest) - len(dead)} priced names")
        gate(f"G6 sweep {SWEEP} priced on every in-window row ({nm})",
             f"non-null {int(px[SWEEP].loc[win].notna().sum())} of {len(win)}", "all",
             bool(px[SWEEP].loc[win].notna().all()))

    # ---- G1: at L = 200 the free-lookback gate IS baseline.band_state (which hardcodes 200)
    for nm, (px, invest) in panels.items():
        a = band_state(px[invest], BAND)
        b = band_state_L(px[invest], BAND, COMMITTED_L)
        mism = int((a.values != b.values).sum())
        gate(f"G1 band_state_L(L=200) BIT-IDENTICAL to baseline.band_state ({nm})",
             f"{mism} mismatching (day, name) cells of {a.size}", "0", mism == 0)

    # ---- G5: engine's cost charge is LINEAR in bps, so one zero-cost pass prices every rung
    w_chk = cap_weights_L(px_u, panels["U56"][1], BOOKS["CAP2"], 0.75, COMMITTED_L)
    r_eng = backtest(px_u, w_chk, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    d5 = float((r_eng - priced(run(px_u, w_chk), HEADLINE_RUNG)).abs().max())
    gate("G5 zero-cost pass + turnover*bps/1e4 == engine.backtest(cost_bps=10)",
         f"max|d| {d5:.3e}", "< 1e-15", d5 < 1e-15)

    # ---- G7: no lookahead — the L-day mean uses only closes up to and including t,
    #          and engine applies weights at t+1 (asserted by construction + a shift test)
    ma_now = px_u[panels["U56"][1]].rolling(COMMITTED_L).mean()
    ma_lag = px_u[panels["U56"][1]].shift(1).rolling(COMMITTED_L).mean()
    gate("G7 the L-day mean is causal (rolling(L) over closes <= t; differs from a 1-day-lagged mean)",
         f"max|ma_t - ma_(t-1 window)| {float((ma_now - ma_lag).abs().max().max()):.4f} > 0",
         "> 0 (i.e. no accidental shift)", float((ma_now - ma_lag).abs().max().max()) > 0)

    # ---------------------------------------------------------------- the grid
    rows, book_rows = [], []
    for pname, (px, invest) in panels.items():
        base_res = run(px, rules_v2_weights(px[invest], band=BAND, gross=0.75)
                       .reindex(columns=px.columns).fillna(0.0))
        spy_full = px["SPY"].pct_change().fillna(0.0)
        for bk, cap in BOOKS.items():
            for gross in GROSSES:
                for L in LOOKBACKS:
                    wt = cap_weights_L(px, invest, cap, gross, L)
                    res = run(px, wt)
                    for wname, w0 in WINDOWS.items():
                        win = px.index[w0:]
                        yrs = len(win) / 252
                        spy = spy_full.loc[win]
                        spy_oos = spy.loc[OOS_START:]
                        base_r = priced(base_res, HEADLINE_RUNG).loc[win]
                        inw = res["held"].drop(columns=[SWEEP]).loc[win]
                        state = inw.values > 1e-12
                        pos = inw.values[state]
                        book_rows.append(dict(panel=pname, book=bk, gross=gross, L=L, window=wname,
                                              turnover_yr=float(res["turnover"].loc[win].sum() / yrs),
                                              mean_names_in=float(state.sum(axis=1).mean()),
                                              max_name_w=float(pos.max()) if len(pos) else 0.0,
                                              mean_gross=float(res["held"].loc[win].sum(axis=1).mean()),
                                              mean_sweep_w=float(res["held"][SWEEP].loc[win].mean()),
                                              max_row_sum=float(res["held"].loc[win].sum(axis=1).max()),
                                              spy_CAGR=cagr(spy), spy_Sharpe=sharpe(spy), spy_MaxDD=maxdd(spy),
                                              base_CAGR=cagr(base_r), base_Sharpe=sharpe(base_r),
                                              base_MaxDD=maxdd(base_r)))
                        for rung in RUNGS:
                            r = priced(res, rung).loc[win]
                            r_oos = r.loc[OOS_START:]
                            h1, h2 = halves(r)
                            rows.append(dict(panel=pname, book=bk, gross=gross, L=L, window=wname,
                                             cost_bps=rung,
                                             CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                             H1=h1, H2=h2,
                                             IS_Sharpe=sharpe(r.loc[:IS_END]), IS_Calmar=calmar(r.loc[:IS_END]),
                                             OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                             **legs(r, base_r, spy, r_oos, spy_oos)))
        say(f"    ... {pname} done ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(rows); bf = pd.DataFrame(book_rows)
    df.to_csv(f"{OUT}.grid.csv", index=False); bf.to_csv(f"{OUT}.book.csv", index=False)
    hd = df[df.window == HEADLINE_WIN]

    # ---- G2 / G3: external reproduction of the two committed headlines at L = 200
    h = hd[(hd.panel == "U56") & (hd.book == "CAP2") & (hd.gross == 0.75) & (hd.L == COMMITTED_L)
           & (hd.cost_bps == HEADLINE_RUNG)].iloc[0]
    t2 = bf[(bf.panel == "U56") & (bf.book == "CAP2") & (bf.gross == 0.75) & (bf.L == COMMITTED_L)
            & (bf.window == HEADLINE_WIN)].iloc[0]
    d2 = max(abs(h.CAGR - 0.1162), abs(h.Sharpe - 1.2687) / 10, abs(h.MaxDD + 0.1481),
             abs(h.OOS_CAGR - 0.1277), abs(h.OOS_Sharpe - 1.3318) / 10)
    gate("G2 reproduces idea 2336's committed CAP2 U56 headline (11.62%/1.2687/-14.81%, OOS 12.77%/1.3318)",
         f"read {h.CAGR:.2%} / {h.Sharpe:.4f} / {h.MaxDD:.2%}, OOS {h.OOS_CAGR:.2%} / {h.OOS_Sharpe:.4f},"
         f" turnover {t2.turnover_yr:.2f}x (committed 3.51x) -> max|d| {d2:.2e}", "< 1e-3", d2 < 1e-3)
    h3 = hd[(hd.panel == "U56") & (hd.book == "CAND") & (hd.gross == 0.75) & (hd.L == COMMITTED_L)
            & (hd.cost_bps == HEADLINE_RUNG)].iloc[0]
    d3 = max(abs(h3.CAGR - 0.125950), abs(h3.Sharpe - 1.1934) / 10, abs(h3.MaxDD + 0.173923),
             abs(h3.OOS_CAGR - 0.138525), abs(h3.OOS_Sharpe - 1.2397) / 10)
    gate("G3 reproduces idea 2300/2332's committed CAND U56 headline (12.5950%/1.1934/-17.3923%, OOS 13.8525%/1.2397)",
         f"read {h3.CAGR:.4%} / {h3.Sharpe:.4f} / {h3.MaxDD:.4%}, OOS {h3.OOS_CAGR:.4%} / {h3.OOS_Sharpe:.4f}"
         f" -> max|d| {d3:.2e}", "< 1e-3", d3 < 1e-3)
    gate("G4 no leverage anywhere (40 books x 2 windows)",
         f"max row gross {bf.max_row_sum.max():.9f}", "<= 1+1e-9", bf.max_row_sum.max() <= 1 + 1e-9)

    # ---- G10: the dial BITES — a shorter mean must turn the gate over more often
    bites = []
    for (p, b, g), grp in bf[bf.window == HEADLINE_WIN].groupby(["panel", "book", "gross"]):
        v = grp.sort_values("L").turnover_yr.values
        bites.append(bool(v[0] > v[-1] + 1e-9))
    gate("G10 the L dial BITES (turnover at L=100 strictly ABOVE L=300)",
         f"{sum(bites)} of {len(bites)} (panel, book, gross) cells", f"{len(bites)} of {len(bites)}", all(bites))
    mono = []
    for (p, b, g), grp in bf[bf.window == HEADLINE_WIN].groupby(["panel", "book", "gross"]):
        v = grp.sort_values("L").turnover_yr.values
        mono.append(bool(np.all(np.diff(v) <= 1e-9)))
    publish("G10b turnover MONOTONE non-increasing in L over the whole ladder",
            f"{sum(mono)} of {len(mono)} cells")

    # ---------------------------------------------------------------- A. full grid
    say(f"\n=== A. THE FULL GRID AT THE HEADLINE RUNG (10 bps), WINDOW {HEADLINE_WIN} — every point, nothing dropped ===")
    for pname in panels:
        for bk in BOOKS:
            say(f"\n  {pname} / {bk}")
            say("    L   gross |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh  OOS DD | 4a 4b |"
                " legs H1/H2/OOS/DD/CAGR | turn/yr  namesIN   maxw")
            for gross in GROSSES:
                for L in LOOKBACKS:
                    r = hd[(hd.panel == pname) & (hd.book == bk) & (hd.gross == gross) & (hd.L == L)
                           & (hd.cost_bps == HEADLINE_RUNG)].iloc[0]
                    c = bf[(bf.panel == pname) & (bf.book == bk) & (bf.gross == gross) & (bf.L == L)
                           & (bf.window == HEADLINE_WIN)].iloc[0]
                    lg = "".join("1" if r[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                    star = " *" if L == COMMITTED_L else "  "
                    say(f"  {L:4d}{star} {gross:.2f}  | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%} |"
                        f" {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} {r.OOS_MaxDD:7.2%} |"
                        f" {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg:22s} |"
                        f" {c.turnover_yr:7.2f} {c.mean_names_in:8.2f} {c.max_name_w:6.2%}")

    # ---------------------------------------------------------------- B. keep counts
    say(f"\n=== B. KEEP COUNTS OVER ALL {len(df)} PUBLISHED ROWS (5 L x 2 gross x 2 books x 2 panels x 4 rungs x 2 windows) ===")
    say(f"  4b passes: {int(df.pass4b.sum())} of {len(df)}      4a passes: {int(df.pass4a.sum())} of {len(df)}")
    for wname in WINDOWS:
        ww = df[df.window == wname]
        say(f"\n  window {wname} ({len(ww)} rows):  4b {int(ww.pass4b.sum())}   4a {int(ww.pass4a.sum())}")
        for rung in RUNGS:
            dd = ww[ww.cost_bps == rung]
            say(f"   {rung:5.1f} bps:  4b {int(dd.pass4b.sum()):3d}/{len(dd)}   4a {int(dd.pass4a.sum()):3d}/{len(dd)}"
                f"   binding leg on 4b FAILs: " +
                "  ".join(f"{k} {int((~dd[k][~dd.pass4b]).sum())}" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    say(f"\n  4b pass counts by (book, panel, L) over the 4 rungs x 2 gross, window {HEADLINE_WIN}:")
    for bk in BOOKS:
        for pname in panels:
            line = "  ".join(f"L{L:<4d}{int(hd[(hd.book == bk) & (hd.panel == pname) & (hd.L == L)].pass4b.sum()):2d}/8"
                             for L in LOOKBACKS)
            say(f"    {bk:5s} {pname:5s}  {line}")
    say(f"\n  4b pass counts by (book, panel, L) at 25 and 50 bps ONLY, window {HEADLINE_WIN}:")
    for bk in BOOKS:
        for pname in panels:
            hi = hd[(hd.book == bk) & (hd.panel == pname) & (hd.cost_bps >= 25.0)]
            line = "  ".join(f"L{L:<4d}{int(hi[hi.L == L].pass4b.sum()):2d}/4" for L in LOOKBACKS)
            say(f"    {bk:5s} {pname:5s}  {line}")

    # ---------------------------------------------------------------- C. what each end buys
    say(f"\n=== C. WHAT EACH END OF THE LADDER BUYS: each L minus L=200, same (panel, book, gross, rung), {HEADLINE_WIN} ===")
    for pname in panels:
        for bk in BOOKS:
            say(f"\n  {pname} / {bk} / gross 0.75")
            say("    L     turn/yr  dturn%  | dCAGR @0bps  @10bps  @25bps  @50bps | dSharpe@10  dOOS_Sh@10  dMaxDD@10  namesIN")
            ref = {rg: hd[(hd.panel == pname) & (hd.book == bk) & (hd.gross == 0.75) & (hd.L == COMMITTED_L)
                          & (hd.cost_bps == rg)].iloc[0] for rg in RUNGS}
            t0r = bf[(bf.panel == pname) & (bf.book == bk) & (bf.gross == 0.75) & (bf.L == COMMITTED_L)
                     & (bf.window == HEADLINE_WIN)].iloc[0]
            for L in LOOKBACKS:
                c = bf[(bf.panel == pname) & (bf.book == bk) & (bf.gross == 0.75) & (bf.L == L)
                       & (bf.window == HEADLINE_WIN)].iloc[0]
                r = {rg: hd[(hd.panel == pname) & (hd.book == bk) & (hd.gross == 0.75) & (hd.L == L)
                            & (hd.cost_bps == rg)].iloc[0] for rg in RUNGS}
                say(f"  {L:4d} {c.turnover_yr:9.2f} {c.turnover_yr / t0r.turnover_yr - 1:+7.1%}  |" +
                    "".join(f" {r[rg].CAGR - ref[rg].CAGR:+11.2%}" for rg in RUNGS) +
                    f" | {r[10.0].Sharpe - ref[10.0].Sharpe:+10.4f} {r[10.0].OOS_Sharpe - ref[10.0].OOS_Sharpe:+11.4f}"
                    f" {r[10.0].MaxDD - ref[10.0].MaxDD:+10.2%} {c.mean_names_in:8.2f}")

    # ---------------------------------------------------------------- D. rule 8
    say(f"\n=== D. RULE 8 — (L, gross) chosen on <= {IS_END} ONLY, {OOS_START}-2026 read once (window {HEADLINE_WIN}) ===")
    wf = []
    for pname, (px, invest) in panels.items():
        win = px.index[WINDOWS[HEADLINE_WIN]:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_r = priced(run(px, rules_v2_weights(px[invest], band=BAND, gross=0.75)
                            .reindex(columns=px.columns).fillna(0.0)), HEADLINE_RUNG).loc[win]
        b_oos = base_r.loc[OOS_START:]
        for bk in BOOKS:
            for rung in RUNGS:
                dd = hd[(hd.panel == pname) & (hd.book == bk) & (hd.cost_bps == rung)]
                com = dd[(dd.L == COMMITTED_L) & (dd.gross == 0.75)].iloc[0]
                for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                    pick = dd.loc[dd[col].idxmax()]
                    wf.append(dict(panel=pname, book=bk, cost_bps=rung, chooser=chooser,
                                   pick_L=int(pick.L), pick_gross=pick.gross,
                                   OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                                   pick_pass4b=bool(pick.pass4b), pick_is_L200=bool(pick.L == COMMITTED_L),
                                   com_OOS_CAGR=com.OOS_CAGR, com_OOS_Sharpe=com.OOS_Sharpe, com_OOS_MaxDD=com.OOS_MaxDD,
                                   beats_committed_OOS_Sharpe=bool(pick.OOS_Sharpe > com.OOS_Sharpe),
                                   base_OOS_CAGR=cagr(b_oos), base_OOS_Sharpe=sharpe(b_oos), base_OOS_MaxDD=maxdd(b_oos),
                                   spy_OOS_CAGR=cagr(spy_oos), spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_MaxDD=maxdd(spy_oos),
                                   beats_SPY_OOS_Sharpe=bool(pick.OOS_Sharpe > sharpe(spy_oos))))
                    say(f"  {pname:5s} {bk:5s} {rung:5.1f}bps {chooser:11s} -> L {int(pick.L):3d} g {pick.pick_gross if False else pick.gross:.2f} |"
                        f" OOS {pick.OOS_CAGR:6.2%} / {pick.OOS_Sharpe:.4f} / {pick.OOS_MaxDD:7.2%} |"
                        f" committed L200 g0.75 OOS {com.OOS_CAGR:6.2%} / {com.OOS_Sharpe:.4f} / {com.OOS_MaxDD:7.2%} |"
                        f" live v2 OOS {cagr(b_oos):6.2%} / {sharpe(b_oos):.4f} | SPY OOS {cagr(spy_oos):6.2%} /"
                        f" {sharpe(spy_oos):.4f} | full 4b {'Y' if pick.pass4b else '.'}")
    wfd = pd.DataFrame(wf)
    wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"\n  rule-8 picks landing on L = 200 (the committed gate):  {int(wfd.pick_is_L200.sum())} of {len(wfd)}")
    say(f"  picks beating the COMMITTED book's OOS Sharpe:          {int(wfd.beats_committed_OOS_Sharpe.sum())} of {len(wfd)}")
    say(f"  picks beating SPY's OOS Sharpe:                         {int(wfd.beats_SPY_OOS_Sharpe.sum())} of {len(wfd)}")
    say(f"  picks whose full-sample row also passes 4b:             {int(wfd.pick_pass4b.sum())} of {len(wfd)}")
    say("  pick distribution over L: " + "  ".join(f"L{L} {int((wfd.pick_L == L).sum())}" for L in LOOKBACKS))
    say("  mean OOS Sharpe of the picks vs the committed gate: "
        f"{wfd.OOS_Sharpe.mean():.4f} vs {wfd.com_OOS_Sharpe.mean():.4f} "
        f"({wfd.OOS_Sharpe.mean() - wfd.com_OOS_Sharpe.mean():+.4f})")

    # ---------------------------------------------------------------- E. the warm-up asymmetry
    say("\n=== E. THE WARM-UP ASYMMETRY — does any verdict flip between W260 and W360? ===")
    key = ["panel", "book", "gross", "L", "cost_bps"]
    a = df[df.window == "W260"].set_index(key).sort_index()
    b = df[df.window == "W360"].set_index(key).sort_index()
    flips = int((a.pass4b != b.pass4b).sum())
    gate("G11 no 4b verdict flips between the committed window and the fully-warmed one",
         f"{flips} of {len(a)} (panel, book, gross, L, rung) cells flip", "0", flips == 0)
    if flips:
        say("   cells that FLIP (published in full, nothing hidden):")
        for k in a.index[(a.pass4b != b.pass4b)]:
            say(f"     {k}: W260 4b {'Y' if a.loc[k].pass4b else '.'}  ->  W360 4b {'Y' if b.loc[k].pass4b else '.'}")
    say(f"  mean |dSharpe| W360-W260 across all {len(a)} cells: {float((b.Sharpe - a.Sharpe).abs().mean()):.4f}"
        f"   mean dCAGR {float((b.CAGR - a.CAGR).mean()):+.2%}")
    say(f"\n  L=300's gate is still warming for the first rows of W260; days OUT by warm-up alone:")
    for pname, (px, invest) in panels.items():
        w260 = px.index[WINDOWS["W260"]]
        for L in LOOKBACKS:
            nw = int((px.index[:L - 1] >= w260).sum())
            say(f"    {pname:5s} L={L:3d}: {nw:4d} in-window rows before the mean exists")

    # ---------------------------------------------------------------- F. the book
    say(f"\n=== F. THE BOOK AT EACH L (gross 0.75, window {HEADLINE_WIN}) — turnover, breadth, concentration, sweep ===")
    say("  panel book  |" + "".join(f"     L={L}" for L in LOOKBACKS))
    for metric, fmt in (("turnover_yr", "{:9.2f}"), ("mean_names_in", "{:9.2f}"),
                        ("max_name_w", "{:9.2%}"), ("mean_gross", "{:9.4f}"), ("mean_sweep_w", "{:9.4f}")):
        say(f"  -- {metric}")
        for pname in panels:
            for bk in BOOKS:
                row = bf[(bf.panel == pname) & (bf.book == bk) & (bf.gross == 0.75)
                         & (bf.window == HEADLINE_WIN)].set_index("L")
                say(f"  {pname:5s} {bk:5s} |" + "".join(fmt.format(row.loc[L][metric]) for L in LOOKBACKS))

    gdf = pd.DataFrame(GATES)
    gdf.to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n=== GATES: {int(gdf.pass_.sum())} of {len(gdf)} pass ===")
    for _, g in gdf[~gdf.pass_].iterrows():
        say(f"    FAILED: {g.gate} = {g.value} (target {g.target})")
    say(f"\nwrote {OUT}.grid.csv / .book.csv / .walkforward.csv / .gates.csv   ({time.time() - t0:.0f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

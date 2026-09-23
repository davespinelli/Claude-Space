#!/usr/bin/env python3
"""idea 2318 (lane cloud, 2026-09-23) — DOES THE KEEP-4b CANDIDATE SURVIVE THE BAND-WIDTH LADDER,
OR IS IT A 3% ARTEFACT?

THE OBJECT.  Idea 2300 filed `RG100 + phi = 1.00` as the record's standing 4b KEEP-candidate:
every name INSIDE the 200d +/-3% band (RULES v2 clause 2, with hysteresis) held at `gross / N_in`
of NAV, the residual `1 - sum(w)` swept to SHY.  EVERY cell of it was priced at ONE band width,
the live clause-2 constant c = 0.03.  The re-gross scale `N / N_in` is a DIRECT function of how
many names the band holds IN, so c moves the candidate's CONCENTRATION (max per-name weight) and
its CASH SWEEP at the same time -- the one dial the candidate has never been read on.  Idea 2343
swept the MA LENGTH L at c = 0.03 and found a plateau; idea 2241 priced the two EDGES separately
at c = 0.03.  The WIDTH itself is the gap.

    w_i = gross / N_in(c)  on names IN the 200d +/-c band,   idle NAV -> SHY (phi = 1.00)

DIAL 1 -- band width c {0.00, 0.02, 0.03, 0.05, 0.08, 0.12} (the record's standing ladder).
          c = 0.03 IS the committed candidate; c = 0.00 is the degenerate no-hysteresis gate
          (IN strictly above the MA, OUT strictly below), which the ladder must span to be honest.
DIAL 2 -- gross {0.75 (live), 1.00}.

REPORTED, NEVER SELECTED ON: 3 panels (U56 / B136 / SMALL), 4 cost rungs (0 / 10 / 25 / 50 bps),
weekly cadence, t+1 execution, MA length L = 200 (the live constant), sweep instrument SHY.
6 x 2 x 3 = 36 books, every one published at every rung = 144 rows.

BOTH KEEP PATHS on every row: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse) and
4b (Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's).
RULE 8: (c, gross) chosen on warm-up..2016-12-31 ONLY by two pre-stated IS-only choosers
(C_ISSHARPE, C_ISCALMAR), then 2017-2026 read ONCE.

THE RIDGE-OR-PLATEAU QUESTION is the deliverable: if 4b passes at c = 0.03 and nowhere else the
candidate is a DRAW; if it passes on a contiguous interior run of widths it is a BOOK.

GATES.  G0 >= 10y per panel.  G1 the per-column replica == `engine.backtest`.  G2 the c = 0.03
band is BIT-IDENTICAL to `baseline.band_state` (the live clause-2 object).  G3 the c = 0.03 book
is BIT-IDENTICAL to an independently constructed RG100 + phi = 1.  G4 no leverage anywhere.
G5 the c dial BITES (mean time-IN and turnover differ across c).  G6 SHY priced on every row it
is held.  G7 SMALL dropped-ticker rule bit.  G8 exactly two tuned parameters.  G9 EXTERNAL
REPRODUCTION of idea 2300's committed U56 headline (12.55% / 1.1896 / -17.39%, OOS 13.77% / 1.2332).

SURVIVORSHIP CAVEAT (binding on every B136 and SMALL row below): `universe_broad.json` and the
sub-$2B SMALL pool are CURRENT constituents of their screens, so both panels are survivorship-
biased upward.  U56 is the panel the live book trades and carries the same caveat more mildly.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_band-width-ladder-on-the-4b-candidate_cloud.py
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

DATE, SLUG, LANE = "2026-09-23", "band-width-ladder-on-the-4b-candidate", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

MA_LEN, CADENCE = 200, "W"
WARMUP = 260            # the record's scored-window convention (idea 2300 and every committed row)
WIDTHS = [0.00, 0.02, 0.03, 0.05, 0.08, 0.12]
GROSSES = [0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG = 10.0
LIVE_C = 0.03
SWEEP = "SHY"
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


# ---------------------------------------------------------------- the gate, generalised in c
def band_state_c(px, c, L=MA_LEN):
    """RULES v2 clause 2 with the band WIDTH as a parameter.  IN above ma*(1+c), OUT below
    ma*(1-c), previous state in between, OUT before L closes exist.  At c = 0.03 this is
    `baseline.band_state` verbatim (asserted by G2); at c = 0.00 the in-between region is empty
    and the gate is the bare MA crossing with no hysteresis."""
    ma = px.rolling(L).mean()
    raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
    raw = raw.mask(px > ma * (1 + c), 1.0).mask(px < ma * (1 - c), 0.0)
    return raw.ffill().fillna(0.0) > 0.5


def rg100_weights(px, invest, c, gross):
    """The candidate at band width c: w_i = gross / N_in on IN names, idle NAV -> SHY (phi = 1)."""
    q = px[invest]
    pr = q.notna()
    inb = band_state_c(q, c) & pr
    nin = inb.sum(axis=1).replace(0, np.nan)
    per = (gross / nin).fillna(0.0)
    w = inb.astype(float).mul(per, axis=0).reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return w


def rg100_reference(px, invest, gross):
    """Independent construction of idea 2300's RG100 + phi = 1 at c = 0.03 (scale form, not the
    per-name form above), built on `baseline.band_state` rather than on band_state_c."""
    q = px[invest]
    pr = q.notna()
    e = pd.DataFrame(1.0, index=q.index, columns=q.columns).where(pr, 0.0)
    N = e.sum(axis=1).replace(0, np.nan)
    inb = band_state(q, LIVE_C) & pr
    nin = inb.sum(axis=1).replace(0, np.nan)
    dg = (gross * e.div(N, axis=0).fillna(0.0)).where(inb, 0.0)
    scale = (N / nin).replace([np.inf, -np.inf], np.nan).fillna(1.0)
    w = dg.mul(scale, axis=0).reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return w


# ---------------------------------------------------------------- engine replica
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


def scored(res, win, rung):
    return priced(res, rung).loc[win]


# ---------------------------------------------------------------- panels
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"].astype(str))
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    dropped = len(px.columns) - len(keep)
    px = px[keep]
    shy = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)[SWEEP]
    px = pd.concat([px, shy.reindex(px.index, method="ffill").rename(SWEEP)], axis=1)
    return px, dropped


def main():
    t0 = time.time()
    say("=== idea 2318 — DOES THE KEEP-4b CANDIDATE SURVIVE THE BAND-WIDTH LADDER? ===")
    say(f"    {DATE}  lane {LANE}   MA {MA_LEN}d  cadence {CADENCE}  t+1  rungs {RUNGS} bps  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 band width c {WIDTHS}   DIAL 2 gross {GROSSES}")
    say("    SURVIVORSHIP: B136 and SMALL are CURRENT constituents of their screens (biased upward).")
    gate("G8 exactly two tuned parameters", "band width c, gross", "2", True)

    px_u = load_universe()
    px_b = load_universe(broad=True)
    px_s, dropped = small_panel()
    gate("G7 dropped-ticker rule bit (SMALL)", f"{dropped} names dropped (max_1d_move >= 1.0)",
         ">= 1", dropped >= 1)

    panels = {}
    for nm, px in (("U56", px_u), ("B136", px_b), ("SMALL", px_s)):
        invest = [c for c in px.columns if c not in ("SPY", SWEEP)] if nm == "SMALL" else list(px.columns)
        panels[nm] = (px, invest)
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y, {len(invest)} investable, {len(px)} rows",
             ">= 10y", yrs >= 10)

    # G2: band_state_c(0.03) is the live clause-2 object, bit for bit
    d2 = int((band_state_c(px_u, LIVE_C) != band_state(px_u, LIVE_C)).sum().sum())
    gate("G2 band_state_c(c=0.03) == baseline.band_state (live clause 2)", f"{d2} differing cells",
         "0", d2 == 0)

    # G1: the replica prices the live book exactly as engine.backtest does
    w_live = rules_v2_weights(px_u, band=LIVE_C, gross=0.75)
    res_live = run_book(px_u, w_live)
    r_eng = backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    d1 = float((r_eng - priced(res_live, HEADLINE_RUNG)).abs().max())
    gate("G1 per-column replica == engine.backtest", f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    # G3: the c = 0.03 book is the committed candidate, independently constructed
    pxq, invq = panels["U56"]
    d3 = float((rg100_weights(pxq, invq, LIVE_C, 0.75) - rg100_reference(pxq, invq, 0.75)).abs().max().max())
    gate("G3 c=0.03 book == RG100 + phi=1 (independent construction, U56)", f"max|dw| {d3:.3e}",
         "< 1e-12", d3 < 1e-12)

    rows, expo_rows = [], []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_res = run_book(px, rules_v2_weights(px[invest], band=LIVE_C, gross=0.75)
                            .reindex(columns=px.columns).fillna(0.0))
        base_r = scored(base_res, win, HEADLINE_RUNG)
        say(f"\n--- panel {pname}  ({len(invest)} names)  SPY {cagr(spy):.2%} / {sharpe(spy):.4f} / {maxdd(spy):.2%}"
            f"   live RULES v2 {cagr(base_r):.2%} / {sharpe(base_r):.4f} / {maxdd(base_r):.2%}")
        say(f"    4b bars on this panel: DD cap {DD_CAP * maxdd(spy):.2%}   CAGR floor {CAGR_FLOOR * cagr(spy):.2%}")
        for gross in GROSSES:
            for c in WIDTHS:
                w = rg100_weights(px, invest, c, gross)
                mx = float(w.sum(axis=1).max())
                if mx > 1 + 1e-12:
                    gate(f"G4 no leverage ({pname} c={c} g={gross})", f"max row sum {mx:.9f}",
                         "<= 1+1e-12", False)
                res = run_book(px, w)
                nm_w = w.drop(columns=[SWEEP]).loc[win]
                pos = nm_w.values[nm_w.values > 0]
                inb = band_state_c(px[invest], c) & px[invest].notna()
                nin = inb.sum(axis=1).loc[win]
                npr = px[invest].notna().sum(axis=1).loc[win]
                flips = int((inb.astype(int).diff().abs().sum(axis=1)).loc[win].sum())
                expo_rows.append(dict(panel=pname, c=c, gross=gross,
                                      time_in_share=float((nin / npr.replace(0, np.nan)).mean()),
                                      median_N_in=float(nin.median()), min_N_in=float(nin.min()),
                                      days_all_out=int((nin == 0).sum()),
                                      gate_flips=flips,
                                      max_name_w=float(pos.max()) if len(pos) else 0.0,
                                      p99_name_w=float(np.percentile(pos, 99)) if len(pos) else 0.0,
                                      med_name_w=float(np.median(pos)) if len(pos) else 0.0,
                                      mean_gross=float(res["gross"].loc[win].mean()),
                                      mean_sweep_w=float(w[SWEEP].loc[win].mean()),
                                      turnover_yr=float(res["turnover"].loc[win].sum() / (len(win) / 252)),
                                      max_row_sum=mx))
                for rung in RUNGS:
                    r = scored(res, win, rung)
                    r_oos = r.loc[OOS_START:]
                    h1, h2 = halves(r)
                    lg = legs(r, base_r, spy, r_oos, spy_oos)
                    rows.append(dict(panel=pname, c=c, gross=gross, cost_bps=rung,
                                     CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                     H1=h1, H2=h2,
                                     IS_Sharpe=sharpe(r.loc[:IS_END]), IS_Calmar=calmar(r.loc[:IS_END]),
                                     OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                     **lg))
        say(f"    ... {pname} done ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(rows)
    ef = pd.DataFrame(expo_rows)
    df.to_csv(f"{OUT}.grid.csv", index=False)
    ef.to_csv(f"{OUT}.exposure.csv", index=False)

    ok4 = bool((ef.max_row_sum <= 1 + 1e-12).all())
    gate("G4 no leverage (all 36 books)", f"max row sum {ef.max_row_sum.max():.9f}", "<= 1+1e-12", ok4)
    shy_ok = True
    for pname, (pxp, _) in panels.items():
        shy_ok &= bool(pxp[SWEEP].loc[pxp.index[WARMUP:]].notna().all())
    gate("G6 sweep instrument priced on every held row", f"SHY non-null on all panels: {shy_ok}",
         "True", shy_ok)

    # G5 the dial bites: both time-IN and gate churn must move along c
    spans, mono = [], []
    for (pname, gross), g in ef.groupby(["panel", "gross"]):
        v = g.set_index("c").reindex(WIDTHS).time_in_share.values
        f = g.set_index("c").reindex(WIDTHS).gate_flips.values
        spans.append(f"{pname}/g{gross:.2f} timeIN {v[0]:.3f}->{v[-1]:.3f} flips {f[0]:.0f}->{f[-1]:.0f}")
        mono.append(bool(np.ptp(v) > 1e-6 and np.ptp(f) > 0))
    gate("G5 the c dial BITES (time-IN share AND gate churn vary along the ladder)",
         f"{sum(mono)} of {len(mono)} (panel, gross) cells move on both", "6 of 6", all(mono))
    publish("G5b end-to-end bite (c = 0.00 -> 0.12)", "  ".join(spans))

    # G9 external reproduction of idea 2300's committed U56 headline
    h = df[(df.panel == "U56") & (df.c == LIVE_C) & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    d9 = max(abs(h.CAGR - 0.1255), abs(h.Sharpe - 1.1896) / 10, abs(h.MaxDD + 0.1739),
             abs(h.OOS_CAGR - 0.1377), abs(h.OOS_Sharpe - 1.2332) / 10)
    gate("G9 reproduces idea 2300's committed U56 headline (12.55%/1.1896/-17.39%, OOS 13.77%/1.2332)",
         f"read {h.CAGR:.2%} / {h.Sharpe:.4f} / {h.MaxDD:.2%}, OOS {h.OOS_CAGR:.2%} / {h.OOS_Sharpe:.4f}"
         f" -> max|d| {d9:.2e}", "< 1e-3", d9 < 1e-3)

    # ---------------------------------------------------------------- headline tables
    say("\n=== A. THE FULL GRID AT THE HEADLINE RUNG (10 bps) — every point, nothing dropped ===")
    for pname in panels:
        say(f"\n  {pname}")
        say("     c  gross |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh  OOS DD | 4a 4b | H1/H2/OOS/DD/CAGR | time-IN maxw  turn/yr")
        for gross in GROSSES:
            for c in WIDTHS:
                r = df[(df.panel == pname) & (df.c == c) & (df.gross == gross)
                       & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                e = ef[(ef.panel == pname) & (ef.c == c) & (ef.gross == gross)].iloc[0]
                lg = "".join("1" if r[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                star = " <= LIVE" if c == LIVE_C else ""
                say(f"  {c:5.2f} {gross:.2f}  | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%} |"
                    f" {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} {r.OOS_MaxDD:7.2%} |"
                    f" {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg:17s} |"
                    f" {e.time_in_share:6.3f} {e.max_name_w:5.2%} {e.turnover_yr:7.2f}{star}")

    say("\n=== B. KEEP COUNTS OVER ALL 144 PUBLISHED ROWS (6 c x 2 gross x 3 panels x 4 rungs) ===")
    say(f"  4b passes: {int(df.pass4b.sum())} of {len(df)}      4a passes: {int(df.pass4a.sum())} of {len(df)}")
    for rung in RUNGS:
        d = df[df.cost_bps == rung]
        say(f"   {rung:5.1f} bps:  4b {int(d.pass4b.sum()):2d}/{len(d)}   4a {int(d.pass4a.sum()):2d}/{len(d)}"
            f"   binding leg on 4b FAILs: " +
            "  ".join(f"{k} {int((~d[k][~d.pass4b]).sum())}" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    for pname in panels:
        d = df[df.panel == pname]
        say(f"   panel {pname:5s}:  4b {int(d.pass4b.sum()):2d}/{len(d)}   4a {int(d.pass4a.sum()):2d}/{len(d)}")
    say("\n  4b pass rows (all rungs):")
    p = df[df.pass4b]
    if len(p) == 0:
        say("    NONE")
    else:
        for _, r in p.iterrows():
            say(f"    {r.panel:5s} c {r.c:.2f} g {r.gross:.2f} {r.cost_bps:5.1f}bps  "
                f"{r.CAGR:6.2%} / {r.Sharpe:.4f} / {r.MaxDD:7.2%}   OOS {r.OOS_CAGR:6.2%} / {r.OOS_Sharpe:.4f}")

    say("\n=== C. RIDGE OR PLATEAU?  4b pass count by c, over all panels/gross/rungs (24 rows per c) ===")
    for c in WIDTHS:
        d = df[df.c == c]
        byp = "  ".join(f"{pn} {int(df[(df.c == c) & (df.panel == pn)].pass4b.sum())}/{len(df[(df.c == c) & (df.panel == pn)])}"
                        for pn in panels)
        say(f"  c {c:5.2f}:  4b {int(d.pass4b.sum()):2d}/{len(d)}   4a {int(d.pass4a.sum()):2d}/{len(d)}   [{byp}]")
    # the verdict, mechanically: is the pass set at the headline rung contiguous and interior?
    for pname in panels:
        for gross in GROSSES:
            sub = df[(df.panel == pname) & (df.gross == gross) & (df.cost_bps == HEADLINE_RUNG)]
            ps = sub.set_index("c").reindex(WIDTHS).pass4b.astype(bool).values
            idx = [i for i, v in enumerate(ps) if v]
            shape = ("NONE" if not idx else
                     ("CONTIGUOUS" if idx == list(range(idx[0], idx[-1] + 1)) else "BROKEN"))
            width = len(idx)
            say(f"  {pname:5s} g {gross:.2f} @10bps: pass set {''.join('Y' if v else '.' for v in ps)}"
                f"  ({width} of {len(WIDTHS)} widths, {shape}; live c=0.03 is index 2)")

    say("\n=== D. WHAT WIDTH COSTS: the committed c = 0.03 minus each rung, U56 g = 0.75, 10 bps ===")
    ref = df[(df.panel == "U56") & (df.c == LIVE_C) & (df.gross == 0.75) & (df.cost_bps == 10.0)].iloc[0]
    for c in WIDTHS:
        r = df[(df.panel == "U56") & (df.c == c) & (df.gross == 0.75) & (df.cost_bps == 10.0)].iloc[0]
        e = ef[(ef.panel == "U56") & (ef.c == c) & (ef.gross == 0.75)].iloc[0]
        say(f"  c {c:5.2f}  dCAGR {r.CAGR - ref.CAGR:+6.2%}  dSharpe {r.Sharpe - ref.Sharpe:+7.4f}"
            f"  dMaxDD {r.MaxDD - ref.MaxDD:+6.2%}  dOOS_Sh {r.OOS_Sharpe - ref.OOS_Sharpe:+7.4f}"
            f"  | time-IN {e.time_in_share:.3f}  mean gross {e.mean_gross:.3f}  mean SHY {e.mean_sweep_w:.3f}"
            f"  maxw {e.max_name_w:.2%}  flips {e.gate_flips:.0f}  turn/yr {e.turnover_yr:.2f}")

    say("\n=== E. RULE 8 — (c, gross) chosen on <= 2016-12-31 ONLY, 2017-2026 read once ===")
    wf = []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_r = scored(run_book(px, rules_v2_weights(px[invest], band=LIVE_C, gross=0.75)
                                 .reindex(columns=px.columns).fillna(0.0)), win, HEADLINE_RUNG)
        b_oos = base_r.loc[OOS_START:]
        for rung in RUNGS:
            d = df[(df.panel == pname) & (df.cost_bps == rung)]
            for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                pick = d.loc[d[col].idxmax()]
                wf.append(dict(panel=pname, cost_bps=rung, chooser=chooser,
                               pick_c=pick.c, pick_gross=pick.gross,
                               OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                               base_OOS_CAGR=cagr(b_oos), base_OOS_Sharpe=sharpe(b_oos), base_OOS_MaxDD=maxdd(b_oos),
                               spy_OOS_CAGR=cagr(spy_oos), spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_MaxDD=maxdd(spy_oos),
                               full4b=bool(pick.pass4b), pick_is_live=(abs(pick.c - LIVE_C) < 1e-12)))
                say(f"  {pname:5s} {rung:5.1f}bps {chooser:11s} -> c {pick.c:.2f} g {pick.gross:.2f} |"
                    f" OOS {pick.OOS_CAGR:6.2%} / {pick.OOS_Sharpe:.4f} / {pick.OOS_MaxDD:7.2%} |"
                    f" live v2 OOS {cagr(b_oos):6.2%} / {sharpe(b_oos):.4f} / {maxdd(b_oos):7.2%} |"
                    f" SPY OOS {cagr(spy_oos):6.2%} / {sharpe(spy_oos):.4f} / {maxdd(spy_oos):7.2%} |"
                    f" full-sample 4b {'Y' if pick.pass4b else '.'}")
    wfd = pd.DataFrame(wf)
    wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"\n  rule-8 picks landing on c = 0.03 (the committed width): {int(wfd.pick_is_live.sum())} of {len(wfd)}")
    say(f"  picks whose OOS Sharpe beats SPY's: {int((wfd.OOS_Sharpe > wfd.spy_OOS_Sharpe).sum())} of {len(wfd)};"
        f"  beats the live book's: {int((wfd.OOS_Sharpe > wfd.base_OOS_Sharpe).sum())} of {len(wfd)}")
    say("  pick distribution over c: " + "  ".join(f"c{c:.2f} {int((wfd.pick_c == c).sum())}" for c in WIDTHS))
    say("  pick distribution over gross: " + "  ".join(f"g{g:.2f} {int((wfd.pick_gross == g).sum())}" for g in GROSSES))
    # what the chooser's pick costs against the incumbent, OOS, at the headline rung
    say("\n  COST OF CHOOSING (OOS, 10 bps, against the committed c = 0.03 / g = 0.75 cell):")
    for pname in panels:
        inc = df[(df.panel == pname) & (df.c == LIVE_C) & (df.gross == 0.75) & (df.cost_bps == 10.0)].iloc[0]
        for chooser in ("C_ISSHARPE", "C_ISCALMAR"):
            k = wfd[(wfd.panel == pname) & (wfd.cost_bps == 10.0) & (wfd.chooser == chooser)].iloc[0]
            say(f"   {pname:5s} {chooser:11s} pick c {k.pick_c:.2f} g {k.pick_gross:.2f}:"
                f" dOOS_CAGR {k.OOS_CAGR - inc.OOS_CAGR:+6.2%}  dOOS_Sharpe {k.OOS_Sharpe - inc.OOS_Sharpe:+7.4f}"
                f"  dOOS_MaxDD {k.OOS_MaxDD - inc.OOS_MaxDD:+6.2%}")

    say("\n=== F. EXPOSURE AND CONCENTRATION ALONG THE WIDTH LADDER (all panels, g = 0.75) ===")
    say("  panel     c   time-IN  medN_in minN_in all-out   flips   median   p99     max    mean gross  mean SHY  turn/yr")
    for pname in panels:
        for c in WIDTHS:
            e = ef[(ef.panel == pname) & (ef.c == c) & (ef.gross == 0.75)].iloc[0]
            say(f"  {pname:5s} {c:5.2f} {e.time_in_share:8.3f} {e.median_N_in:8.0f} {e.min_N_in:7.0f}"
                f" {e.days_all_out:7.0f} {e.gate_flips:7.0f} {e.med_name_w:8.2%} {e.p99_name_w:6.2%} {e.max_name_w:6.2%}"
                f" {e.mean_gross:11.3f} {e.mean_sweep_w:9.3f} {e.turnover_yr:9.2f}")

    gdf = pd.DataFrame(GATES)
    gdf.to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n=== GATES: {int(gdf.pass_.sum())} of {len(gdf)} pass ===")
    for _, g in gdf[~gdf.pass_].iterrows():
        say(f"    FAILED: {g.gate} = {g.value} (target {g.target})")
    say(f"\nwrote {OUT}.grid.csv / .exposure.csv / .walkforward.csv / .gates.csv"
        f"   ({time.time() - t0:.0f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

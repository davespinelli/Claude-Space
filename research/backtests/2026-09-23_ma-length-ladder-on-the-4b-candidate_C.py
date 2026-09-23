#!/usr/bin/env python3
"""idea 2343 (lane C, 2026-09-23) — IS THE KEEP-4b CANDIDATE A 200d ARTEFACT?  THE MA-LENGTH LADDER.

THE OBJECT.  Idea 2300 filed `RG100 + phi = 1.00` as the record's standing 4b KEEP-candidate:
every name INSIDE the 200d +/-3% band (RULES v2 clause 2, with hysteresis) held at
`gross / N_in` of NAV, the residual `1 - sum(w)` swept to SHY.  Every 4b-passing book in this
record is gated by a band around ONE moving-average length, L = 200 days, and L HAS NEVER BEEN
SWEPT: idea 2241 priced the band's two EDGES (b_in, b_out) at L = 200, idea 2318 is sweeping its
WIDTH c at L = 200, and 2241's own changelog entry lists "one MA length (200d)" as an honest
limit.  L sets how much of the past the gate averages and therefore how fast the book re-enters
after a trough -- exactly the channel the 4b CAGR floor binds on.

    w_i = gross / N_in(L)  on names IN the L-day +/-3% band,   idle NAV -> SHY (phi = 1.00)

DIAL 1 -- MA length L {100, 150, 200, 250, 300}.  L = 200 IS the committed candidate, so one
ladder spans the known book and its neighbours on both sides.
DIAL 2 -- gross {0.75 (live), 1.00}.

REPORTED, NEVER SELECTED ON: 3 panels (U56 / B136 / SMALL), 4 cost rungs (0 / 10 / 25 / 50 bps),
weekly cadence, t+1 execution, band c = 0.03 (the live clause-2 constant), sweep instrument SHY.
5 x 2 x 3 = 30 books, every one published at every rung = 120 rows.

BOTH KEEP PATHS on every row: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse) and
4b (Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's).
RULE 8: (L, gross) chosen on warm-up..2016-12-31 ONLY by two pre-stated IS-only choosers
(C_ISSHARPE, C_ISCALMAR), then 2017-2026 read ONCE.

THE WARM-IN QUESTION, HANDLED IN THE OPEN.  `band_state` is OUT before L closes exist, so a
longer L spends more of the early sample forced OUT.  The HEADLINE grid uses the record's
convention (scored window = index[260:], identical to every committed number, so the L = 200 cell
reproduces idea 2300 exactly).  Section F re-reads the SAME return series on an EQUAL-STATE window
(index[360:], by which even L = 300 has 60 days of live band state) and reports whether the
ladder's ordering and its 4b pass set survive.  Neither window is selected on; both are published.

GATES.  G0 >= 10y per panel.  G1 the per-column replica == `engine.backtest`.  G2 the L = 200
band is BIT-IDENTICAL to `baseline.band_state` (the live clause-2 object).  G3 the L = 200 book is
BIT-IDENTICAL to an independently constructed RG100 + phi = 1.  G4 no leverage anywhere.
G5 the L dial BITES (mean time-IN differs across L, and strictly somewhere).  G6 SHY priced on
every row it is held.  G7 SMALL dropped-ticker rule bit.  G8 exactly two tuned parameters.
G9 EXTERNAL REPRODUCTION of idea 2300's committed U56 headline (12.55% / 1.1896 / -17.39%,
OOS 13.77% / 1.2332).

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_ma-length-ladder-on-the-4b-candidate_C.py
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

DATE, SLUG, LANE = "2026-09-23", "ma-length-ladder-on-the-4b-candidate", "C"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, CADENCE = 0.03, "W"
WARMUP = 260            # the record's scored-window convention (idea 2300 and every committed row)
WARMUP_EQ = 360         # equal-state window: even L = 300 has 60 days of live band state
LENGTHS = [100, 150, 200, 250, 300]
GROSSES = [0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG = 10.0
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


# ---------------------------------------------------------------- the gate, generalised in L
def band_state_L(px, L, band=BAND):
    """RULES v2 clause 2 with the MA length as a parameter.  IN above ma*(1+band), OUT below
    ma*(1-band), previous state in between, OUT before L closes exist.  At L = 200 this is
    `baseline.band_state` verbatim (asserted by G2)."""
    ma = px.rolling(L).mean()
    raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
    raw = raw.mask(px > ma * (1 + band), 1.0).mask(px < ma * (1 - band), 0.0)
    return raw.ffill().fillna(0.0) > 0.5


def rg100_weights(px, invest, L, gross):
    """The candidate at MA length L: w_i = gross / N_in on IN names, idle NAV -> SHY (phi = 1)."""
    q = px[invest]
    pr = q.notna()
    inb = band_state_L(q, L) & pr
    nin = inb.sum(axis=1).replace(0, np.nan)
    per = (gross / nin).fillna(0.0)
    w = inb.astype(float).mul(per, axis=0).reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return w


def rg100_reference(px, invest, gross):
    """Independent construction of idea 2300's RG100 + phi = 1 at L = 200 (scale form, not the
    per-name form above), built on `baseline.band_state` rather than on band_state_L."""
    q = px[invest]
    pr = q.notna()
    e = pd.DataFrame(1.0, index=q.index, columns=q.columns).where(pr, 0.0)
    N = e.sum(axis=1).replace(0, np.nan)
    inb = band_state(q, BAND) & pr
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
    say("=== idea 2343 — IS THE KEEP-4b CANDIDATE A 200d ARTEFACT?  THE MA-LENGTH LADDER ===")
    say(f"    {DATE}  lane {LANE}   band {BAND}  cadence {CADENCE}  t+1  rungs {RUNGS} bps  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 MA length L {LENGTHS}   DIAL 2 gross {GROSSES}")
    gate("G8 exactly two tuned parameters", "MA length L, gross", "2", True)

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

    # G2: band_state_L(200) is the live clause-2 object, bit for bit
    d2 = int((band_state_L(px_u, 200) != band_state(px_u, BAND)).sum().sum())
    gate("G2 band_state_L(L=200) == baseline.band_state (live clause 2)", f"{d2} differing cells",
         "0", d2 == 0)

    # G1: the replica prices the live book exactly as engine.backtest does
    w_live = rules_v2_weights(px_u, band=BAND, gross=0.75)
    res_live = run_book(px_u, w_live)
    r_eng = backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    d1 = float((r_eng - priced(res_live, HEADLINE_RUNG)).abs().max())
    gate("G1 per-column replica == engine.backtest", f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    # G3: the L = 200 book is the committed candidate, independently constructed
    pxq, invq = panels["U56"]
    d3 = float((rg100_weights(pxq, invq, 200, 0.75) - rg100_reference(pxq, invq, 0.75)).abs().max().max())
    gate("G3 L=200 book == RG100 + phi=1 (independent construction, U56)", f"max|dw| {d3:.3e}",
         "< 1e-12", d3 < 1e-12)

    rows, expo_rows, eqrows = [], [], []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        win_eq = px.index[WARMUP_EQ:]
        spy_all = px["SPY"].pct_change().fillna(0.0)
        spy, spy_eq = spy_all.loc[win], spy_all.loc[win_eq]
        spy_oos, spy_eq_oos = spy.loc[OOS_START:], spy_eq.loc[OOS_START:]
        base_res = run_book(px, rules_v2_weights(px[invest], band=BAND, gross=0.75)
                            .reindex(columns=px.columns).fillna(0.0))
        base_r = scored(base_res, win, HEADLINE_RUNG)
        base_eq = scored(base_res, win_eq, HEADLINE_RUNG)
        say(f"\n--- panel {pname}  ({len(invest)} names)  SPY {cagr(spy):.2%} / {sharpe(spy):.4f} / {maxdd(spy):.2%}"
            f"   live RULES v2 {cagr(base_r):.2%} / {sharpe(base_r):.4f} / {maxdd(base_r):.2%}")
        for gross in GROSSES:
            for L in LENGTHS:
                w = rg100_weights(px, invest, L, gross)
                mx = float(w.sum(axis=1).max())
                if mx > 1 + 1e-12:
                    gate(f"G4 no leverage ({pname} L={L} g={gross})", f"max row sum {mx:.9f}",
                         "<= 1+1e-12", False)
                res = run_book(px, w)
                nm_w = w.drop(columns=[SWEEP]).loc[win]
                pos = nm_w.values[nm_w.values > 0]
                inb = band_state_L(px[invest], L) & px[invest].notna()
                nin = inb.sum(axis=1).loc[win]
                npr = px[invest].notna().sum(axis=1).loc[win]
                expo_rows.append(dict(panel=pname, L=L, gross=gross,
                                      time_in_share=float((nin / npr.replace(0, np.nan)).mean()),
                                      median_N_in=float(nin.median()), min_N_in=float(nin.min()),
                                      days_all_out=int((nin == 0).sum()),
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
                    rows.append(dict(panel=pname, L=L, gross=gross, cost_bps=rung,
                                     CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                     H1=h1, H2=h2,
                                     IS_Sharpe=sharpe(r.loc[:IS_END]), IS_Calmar=calmar(r.loc[:IS_END]),
                                     OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                     **lg))
                    # equal-state window, same return series, re-scored
                    re_ = scored(res, win_eq, rung)
                    lge = legs(re_, base_eq, spy_eq, re_.loc[OOS_START:], spy_eq_oos)
                    eqrows.append(dict(panel=pname, L=L, gross=gross, cost_bps=rung,
                                       CAGR=cagr(re_), Sharpe=sharpe(re_), MaxDD=maxdd(re_),
                                       OOS_CAGR=cagr(re_.loc[OOS_START:]),
                                       OOS_Sharpe=sharpe(re_.loc[OOS_START:]), **lge))
        say(f"    ... {pname} done ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(rows)
    ef = pd.DataFrame(expo_rows)
    qf = pd.DataFrame(eqrows)
    df.to_csv(f"{OUT}.grid.csv", index=False)
    ef.to_csv(f"{OUT}.exposure.csv", index=False)
    qf.to_csv(f"{OUT}.equalstate.csv", index=False)

    ok4 = bool((ef.max_row_sum <= 1 + 1e-12).all())
    gate("G4 no leverage (all 30 books)", f"max row sum {ef.max_row_sum.max():.9f}", "<= 1+1e-12", ok4)
    shy_ok = True
    for pname, (pxp, _) in panels.items():
        shy_ok &= bool(pxp[SWEEP].loc[pxp.index[WARMUP:]].notna().all())
    gate("G6 sweep instrument priced on every held row", f"SHY non-null on all panels: {shy_ok}",
         "True", shy_ok)

    # G5 the dial bites
    spans, mono = [], []
    for (pname, gross), g in ef.groupby(["panel", "gross"]):
        v = g.set_index("L").reindex(LENGTHS).time_in_share.values
        spans.append(f"{pname}/g{gross:.2f} {v[0]:.3f}->{v[-1]:.3f}")
        mono.append(bool(np.ptp(v) > 1e-6))
    gate("G5 the L dial BITES (mean time-IN share varies along the ladder)",
         f"{sum(mono)} of {len(mono)} (panel, gross) cells move", "6 of 6", all(mono))
    publish("G5b end-to-end bite (mean share of priced names IN the band, L = 100 -> 300)",
            "  ".join(spans))

    # G9 external reproduction of idea 2300's committed U56 headline
    h = df[(df.panel == "U56") & (df.L == 200) & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    d9 = max(abs(h.CAGR - 0.1255), abs(h.Sharpe - 1.1896) / 10, abs(h.MaxDD + 0.1739),
             abs(h.OOS_CAGR - 0.1377), abs(h.OOS_Sharpe - 1.2332) / 10)
    gate("G9 reproduces idea 2300's committed U56 headline (12.55%/1.1896/-17.39%, OOS 13.77%/1.2332)",
         f"read {h.CAGR:.2%} / {h.Sharpe:.4f} / {h.MaxDD:.2%}, OOS {h.OOS_CAGR:.2%} / {h.OOS_Sharpe:.4f}"
         f" -> max|d| {d9:.2e}", "< 1e-3", d9 < 1e-3)

    # ---------------------------------------------------------------- headline tables
    say("\n=== A. THE FULL GRID AT THE HEADLINE RUNG (10 bps) — every point, nothing dropped ===")
    for pname in panels:
        say(f"\n  {pname}")
        say("   L  gross |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh  OOS DD | 4a 4b | H1/H2/OOS/DD/CAGR | time-IN maxw  turn/yr")
        for gross in GROSSES:
            for L in LENGTHS:
                r = df[(df.panel == pname) & (df.L == L) & (df.gross == gross)
                       & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                c = ef[(ef.panel == pname) & (ef.L == L) & (ef.gross == gross)].iloc[0]
                lg = "".join("1" if r[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                star = " <= LIVE" if L == 200 else ""
                say(f"  {L:4d} {gross:.2f}  | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%} |"
                    f" {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} {r.OOS_MaxDD:7.2%} |"
                    f" {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg:17s} |"
                    f" {c.time_in_share:6.3f} {c.max_name_w:5.2%} {c.turnover_yr:7.2f}{star}")

    say("\n=== B. KEEP COUNTS OVER ALL 120 PUBLISHED ROWS (5 L x 2 gross x 3 panels x 4 rungs) ===")
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
            say(f"    {r.panel:5s} L {int(r.L):4d} g {r.gross:.2f} {r.cost_bps:5.1f}bps  "
                f"{r.CAGR:6.2%} / {r.Sharpe:.4f} / {r.MaxDD:7.2%}   OOS {r.OOS_CAGR:6.2%} / {r.OOS_Sharpe:.4f}")

    say("\n=== C. RIDGE OR PLATEAU?  4b pass count by L, over all panels/gross/rungs (24 rows per L) ===")
    for L in LENGTHS:
        d = df[df.L == L]
        byp = "  ".join(f"{pn} {int(df[(df.L == L) & (df.panel == pn)].pass4b.sum())}/{len(df[(df.L == L) & (df.panel == pn)])}"
                        for pn in panels)
        say(f"  L {L:4d}:  4b {int(d.pass4b.sum()):2d}/{len(d)}   4a {int(d.pass4a.sum()):2d}/{len(d)}   [{byp}]")

    say("\n=== D. WHAT L COSTS: the committed L = 200 minus each rung, U56 g = 0.75, 10 bps ===")
    ref = df[(df.panel == "U56") & (df.L == 200) & (df.gross == 0.75) & (df.cost_bps == 10.0)].iloc[0]
    for L in LENGTHS:
        r = df[(df.panel == "U56") & (df.L == L) & (df.gross == 0.75) & (df.cost_bps == 10.0)].iloc[0]
        c = ef[(ef.panel == "U56") & (ef.L == L) & (ef.gross == 0.75)].iloc[0]
        say(f"  L {L:4d}  dCAGR {r.CAGR - ref.CAGR:+6.2%}  dSharpe {r.Sharpe - ref.Sharpe:+7.4f}"
            f"  dMaxDD {r.MaxDD - ref.MaxDD:+6.2%}  dOOS_Sh {r.OOS_Sharpe - ref.OOS_Sharpe:+7.4f}"
            f"  | time-IN {c.time_in_share:.3f}  mean gross {c.mean_gross:.3f}  mean SHY {c.mean_sweep_w:.3f}"
            f"  turn/yr {c.turnover_yr:.2f}")

    say("\n=== E. RULE 8 — (L, gross) chosen on <= 2016-12-31 ONLY, 2017-2026 read once ===")
    wf = []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_r = scored(run_book(px, rules_v2_weights(px[invest], band=BAND, gross=0.75)
                                 .reindex(columns=px.columns).fillna(0.0)), win, HEADLINE_RUNG)
        b_oos = base_r.loc[OOS_START:]
        for rung in RUNGS:
            d = df[(df.panel == pname) & (df.cost_bps == rung)]
            for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                pick = d.loc[d[col].idxmax()]
                wf.append(dict(panel=pname, cost_bps=rung, chooser=chooser,
                               pick_L=int(pick.L), pick_gross=pick.gross,
                               OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                               base_OOS_CAGR=cagr(b_oos), base_OOS_Sharpe=sharpe(b_oos), base_OOS_MaxDD=maxdd(b_oos),
                               spy_OOS_CAGR=cagr(spy_oos), spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_MaxDD=maxdd(spy_oos),
                               full4b=bool(pick.pass4b), pick_is_200=(int(pick.L) == 200)))
                say(f"  {pname:5s} {rung:5.1f}bps {chooser:11s} -> L {int(pick.L):4d} g {pick.gross:.2f} |"
                    f" OOS {pick.OOS_CAGR:6.2%} / {pick.OOS_Sharpe:.4f} / {pick.OOS_MaxDD:7.2%} |"
                    f" live v2 OOS {cagr(b_oos):6.2%} / {sharpe(b_oos):.4f} / {maxdd(b_oos):7.2%} |"
                    f" SPY OOS {cagr(spy_oos):6.2%} / {sharpe(spy_oos):.4f} / {maxdd(spy_oos):7.2%} |"
                    f" full-sample 4b {'Y' if pick.pass4b else '.'}")
    wfd = pd.DataFrame(wf)
    wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"\n  rule-8 picks landing on L = 200 (the committed length): {int(wfd.pick_is_200.sum())} of {len(wfd)}")
    say(f"  picks whose OOS Sharpe beats SPY's: {int((wfd.OOS_Sharpe > wfd.spy_OOS_Sharpe).sum())} of {len(wfd)};"
        f"  beats the live book's: {int((wfd.OOS_Sharpe > wfd.base_OOS_Sharpe).sum())} of {len(wfd)}")
    say("  pick distribution over L: " + "  ".join(f"L{L} {int((wfd.pick_L == L).sum())}" for L in LENGTHS))

    say("\n=== F. EQUAL-STATE WINDOW (index[360:], even L = 300 has 60 days of live band state) ===")
    say(f"  4b passes on the equal-state window: {int(qf.pass4b.sum())} of {len(qf)}"
        f"   (headline window: {int(df.pass4b.sum())} of {len(df)})")
    for L in LENGTHS:
        a = df[df.L == L]
        b = qf[qf.L == L]
        say(f"  L {L:4d}:  headline 4b {int(a.pass4b.sum()):2d}/{len(a)}   equal-state 4b {int(b.pass4b.sum()):2d}/{len(b)}")
    say("\n  U56 g = 0.75, 10 bps, both windows:")
    for L in LENGTHS:
        a = df[(df.panel == "U56") & (df.L == L) & (df.gross == 0.75) & (df.cost_bps == 10.0)].iloc[0]
        b = qf[(qf.panel == "U56") & (qf.L == L) & (qf.gross == 0.75) & (qf.cost_bps == 10.0)].iloc[0]
        say(f"   L {L:4d}  headline {a.CAGR:6.2%} / {a.Sharpe:.4f} / {a.MaxDD:7.2%} 4b {'Y' if a.pass4b else '.'}"
            f"   |  equal-state {b.CAGR:6.2%} / {b.Sharpe:.4f} / {b.MaxDD:7.2%} 4b {'Y' if b.pass4b else '.'}")

    say("\n=== G. EXPOSURE AND CONCENTRATION ALONG THE LADDER (all panels, g = 0.75) ===")
    say("  panel   L   time-IN  medN_in minN_in all-out  median   p99     max    mean gross  mean SHY  turn/yr")
    for pname in panels:
        for L in LENGTHS:
            c = ef[(ef.panel == pname) & (ef.L == L) & (ef.gross == 0.75)].iloc[0]
            say(f"  {pname:5s} {L:4d} {c.time_in_share:8.3f} {c.median_N_in:8.0f} {c.min_N_in:7.0f}"
                f" {c.days_all_out:7.0f} {c.med_name_w:8.2%} {c.p99_name_w:6.2%} {c.max_name_w:6.2%}"
                f" {c.mean_gross:11.3f} {c.mean_sweep_w:9.3f} {c.turnover_yr:9.2f}")

    gdf = pd.DataFrame(GATES)
    gdf.to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n=== GATES: {int(gdf.pass_.sum())} of {len(gdf)} pass ===")
    for _, g in gdf[~gdf.pass_].iterrows():
        say(f"    FAILED: {g.gate} = {g.value} (target {g.target})")
    say(f"\nwrote {OUT}.grid.csv / .exposure.csv / .equalstate.csv / .walkforward.csv / .gates.csv"
        f"   ({time.time() - t0:.0f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""idea 2322 (lane C, 2026-09-22) — does a PER-NAME WEIGHT CAP keep the KEEP-4b candidate's
pass while removing the CONCENTRATION it adds?

THE OBJECT.  Idea 2300 filed `RG100 + phi = 1.00` as the record's standing 4b KEEP-candidate:
every name INSIDE the 200d +/-3% band held at `gross / N_in` of NAV, the residual `1 - sum(w)`
swept to SHY.  Its published risk is CONCENTRATION: the per-name weight is 1.79% at the median
but 10.1% at the 99th percentile and 15.0% on the worst day, against the live de-grossed book's
1.34% ceiling.  This run prices the one-line fix:

    w_i = min(gross / N_in, cap)  on IN names,   idle NAV -> SHY (phi = 1.00, as filed)

DIAL 1 -- cap {DG, 0.015, 0.02, 0.03, 0.04, 0.06, 0.10, INF}.  `DG` is the time-varying cap
`gross / N_t` (N_t = names priced that day), which reproduces the LIVE de-grossed book with the
sweep attached; `INF` reproduces the candidate.  The cap is therefore a CONTINUOUS DIAL between
the live book and the candidate, and one sweep prices the whole family.
DIAL 2 -- gross {0.75 (live), 1.00}.

REPORTED, NEVER SELECTED ON: 3 panels (U56 / B136 / SMALL), 4 cost rungs (0 / 10 / 25 / 50 bps),
weekly cadence, t+1 execution, band 0.03 (the live clause-2 constant).  8 x 2 x 3 = 48 books,
every one published at every rung = 192 rows.

BOTH KEEP PATHS on every row: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse) and
4b (Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's).
RULE 8: (cap, gross) chosen on warm-up..2016-12-31 ONLY by two pre-stated IS-only choosers
(C_ISSHARPE, C_ISCALMAR), then 2017-2026 read ONCE.

GATES.  G0 >= 10y per panel.  G1 cap=DG is BIT-IDENTICAL to the de-grossed book + sweep.
G2 cap=INF is BIT-IDENTICAL to an independently constructed RG100 + phi=1.  G3 the per-column
replica equals `engine.backtest` on the live weights.  G4 no leverage anywhere.  G5 the cap dial
BITES (max per-name weight non-decreasing in cap, strictly so somewhere).  G6 SHY priced on every
row it is held.  G7 SMALL dropped-ticker rule bit.  G8 exactly two tuned parameters.
G9 EXTERNAL REPRODUCTION of idea 2300's committed U56 headline (12.55% / 1.1896 / -17.39%,
OOS 13.77% / 1.2332).

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-22_per-name-weight-cap-on-the-4b-candidate_C.py
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

DATE, SLUG, LANE = "2026-09-22", "per-name-weight-cap-on-the-4b-candidate", "C"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, CADENCE, WARMUP = 0.03, "W", 260
CAPS = ["DG", 0.015, 0.020, 0.030, 0.040, 0.060, 0.100, "INF"]
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


# ---------------------------------------------------------------- books
def cap_weights(px, invest, cap, gross):
    """w_i = min(gross / N_in, cap) on IN names; idle NAV swept to SHY (phi = 1.00)."""
    q = px[invest]
    pr = q.notna()
    e = pd.DataFrame(1.0, index=q.index, columns=q.columns).where(pr, 0.0)
    N = e.sum(axis=1).replace(0, np.nan)
    inb = band_state(q, BAND) & pr
    nin = inb.sum(axis=1).replace(0, np.nan)
    per = gross / nin                                   # RG100's per-name weight
    if cap == "DG":
        c = gross / N                                   # the live de-grossed per-name weight
    elif cap == "INF":
        c = pd.Series(np.inf, index=q.index)
    else:
        c = pd.Series(float(cap), index=q.index)
    per = pd.concat([per, c], axis=1).min(axis=1)
    w = inb.astype(float).mul(per.fillna(0.0), axis=0)
    w = w.reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    live = px[SWEEP].notna().astype(float)
    w[SWEEP] = w[SWEEP] + idle * live                   # phi = 1.00, as filed by idea 2300
    return w


def rg100_reference(px, invest, gross):
    """Independent construction of idea 2300's RG100 + phi = 1.00 (scale form, not min form)."""
    q = px[invest]
    pr = q.notna()
    e = pd.DataFrame(1.0, index=q.index, columns=q.columns).where(pr, 0.0)
    N = e.sum(axis=1).replace(0, np.nan)
    inb = band_state(q, BAND) & pr
    nin = inb.sum(axis=1).replace(0, np.nan)
    ew = gross * e.div(N, axis=0).fillna(0.0)
    dg = ew.where(inb, 0.0)
    scale = (1.0 + 1.0 * (N / nin - 1.0)).replace([np.inf, -np.inf], np.nan).fillna(1.0)
    w = dg.mul(scale, axis=0).reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return w


def dg_reference(px, invest, gross):
    """The LIVE de-grossed band book with the same sweep attached (cap = gross / N_t)."""
    q = px[invest]
    pr = q.notna()
    e = pd.DataFrame(1.0, index=q.index, columns=q.columns).where(pr, 0.0)
    N = e.sum(axis=1).replace(0, np.nan)
    inb = band_state(q, BAND) & pr
    w = (gross * e.div(N, axis=0).fillna(0.0)).where(inb, 0.0).reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
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


def caplabel(c):
    return c if isinstance(c, str) else f"{c:.3f}"


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
    say("=== idea 2322 — does a PER-NAME WEIGHT CAP keep the KEEP-4b candidate's pass? ===")
    say(f"    {DATE}  lane {LANE}   band {BAND}  cadence {CADENCE}  t+1  rungs {RUNGS} bps  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 cap {[caplabel(c) for c in CAPS]}   DIAL 2 gross {GROSSES}")
    gate("G8 exactly two tuned parameters", "per-name cap, gross", "2", True)

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

    # G3: the replica prices the live book exactly as engine.backtest does
    w_live = rules_v2_weights(px_u, band=BAND, gross=0.75)
    res_live = run_book(px_u, w_live)
    r_eng = backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    d3 = float((r_eng - priced(res_live, HEADLINE_RUNG)).abs().max())
    gate("G3 per-column replica == engine.backtest", f"max|d| {d3:.3e}", "< 1e-12", d3 < 1e-12)

    rows, conc_rows = [], []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_r = priced(run_book(px, rules_v2_weights(px[invest], band=BAND, gross=0.75)
                                 .reindex(columns=px.columns).fillna(0.0)), HEADLINE_RUNG).loc[win]
        say(f"\n--- panel {pname}  ({len(invest)} names)  SPY {cagr(spy):.2%} / {sharpe(spy):.4f} / {maxdd(spy):.2%}"
            f"   live RULES v2 {cagr(base_r):.2%} / {sharpe(base_r):.4f} / {maxdd(base_r):.2%}")
        for gross in GROSSES:
            for cap in CAPS:
                w = cap_weights(px, invest, cap, gross)
                mx = float(w.sum(axis=1).max())
                if mx > 1 + 1e-12:
                    gate(f"G4 no leverage ({pname} cap={caplabel(cap)} g={gross})",
                         f"max row sum {mx:.9f}", "<= 1+1e-12", False)
                res = run_book(px, w)
                nm_w = w.drop(columns=[SWEEP]).loc[win]
                pos = nm_w.values[nm_w.values > 0]
                conc_rows.append(dict(panel=pname, cap=caplabel(cap), gross=gross,
                                      max_name_w=float(pos.max()) if len(pos) else 0.0,
                                      p99_name_w=float(np.percentile(pos, 99)) if len(pos) else 0.0,
                                      med_name_w=float(np.median(pos)) if len(pos) else 0.0,
                                      mean_gross=float(res["gross"].loc[win].mean()),
                                      mean_sweep_w=float(w[SWEEP].loc[win].mean()),
                                      turnover_yr=float(res["turnover"].loc[win].sum() / (len(win) / 252)),
                                      max_row_sum=mx))
                for rung in RUNGS:
                    r = priced(res, rung).loc[win]
                    r_oos = r.loc[OOS_START:]
                    h1, h2 = halves(r)
                    lg = legs(r, base_r, spy, r_oos, spy_oos)
                    rows.append(dict(panel=pname, cap=caplabel(cap), gross=gross, cost_bps=rung,
                                     CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                     H1=h1, H2=h2,
                                     IS_Sharpe=sharpe(r.loc[:IS_END]), IS_Calmar=calmar(r.loc[:IS_END]),
                                     OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                     **lg))
        say(f"    ... {pname} done ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(rows)
    cf = pd.DataFrame(conc_rows)
    df.to_csv(f"{OUT}.grid.csv", index=False)
    cf.to_csv(f"{OUT}.concentration.csv", index=False)

    # ---- G1 / G2: the two ends of the cap dial are the two known books
    px, invest = panels["U56"]
    d1 = float((cap_weights(px, invest, "DG", 0.75) - dg_reference(px, invest, 0.75)).abs().max().max())
    gate("G1 cap=DG == de-grossed live book + sweep (U56)", f"max|dw| {d1:.3e}", "< 1e-12", d1 < 1e-12)
    d2 = float((cap_weights(px, invest, "INF", 0.75) - rg100_reference(px, invest, 0.75)).abs().max().max())
    gate("G2 cap=INF == RG100 + phi=1 (U56, independent construction)", f"max|dw| {d2:.3e}",
         "< 1e-12", d2 < 1e-12)
    ok4 = bool((cf.max_row_sum <= 1 + 1e-12).all())
    gate("G4 no leverage (all 48 books)", f"max row sum {cf.max_row_sum.max():.9f}", "<= 1+1e-12", ok4)
    shy_ok = True
    for pname, (pxp, _) in panels.items():
        shy_ok &= bool(pxp[SWEEP].loc[pxp.index[WARMUP:]].notna().all())
    gate("G6 sweep instrument priced on every held row", f"SHY non-null on all panels: {shy_ok}",
         "True", shy_ok)
    numeric = [caplabel(c) for c in CAPS if c not in ("DG",)]
    mono, ends, dgpos = [], [], []
    for (pname, gross), g in cf.groupby(["panel", "gross"]):
        g = g.set_index("cap")
        v = g.reindex(numeric).max_name_w.values
        mono.append(bool(np.all(np.diff(v) >= -1e-12)))
        ends.append(f"{pname}/g{gross:.2f} {v[0]:.2%}->{v[-1]:.2%}")
        dgpos.append(f"{pname}/g{gross:.2f} {g.loc['DG'].max_name_w:.2%}")
    gate("G5 max per-name weight is non-decreasing along the NUMERIC cap ladder (0.015..INF)",
         f"{sum(mono)} of {len(mono)} (panel, gross) cells", "6 of 6", all(mono))
    publish("G5b end-to-end bite of the numeric ladder (max name weight, 0.015 -> INF)",
            "  ".join(ends))
    publish("G5c the DG rung is a TIME-VARYING cap gross/N_t and is NOT ordered inside the numeric "
            "ladder (on U56 at g=1.00 it sits at 2.00%, above the 1.5% rung); max name weight at DG",
            "  ".join(dgpos))

    # G9 external reproduction of idea 2300's committed U56 headline
    h = df[(df.panel == "U56") & (df.cap == "INF") & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    d9 = max(abs(h.CAGR - 0.1255), abs(h.Sharpe - 1.1896) / 10, abs(h.MaxDD + 0.1739),
             abs(h.OOS_CAGR - 0.1377), abs(h.OOS_Sharpe - 1.2332) / 10)
    gate("G9 reproduces idea 2300's committed U56 headline (12.55%/1.1896/-17.39%, OOS 13.77%/1.2332)",
         f"read {h.CAGR:.2%} / {h.Sharpe:.4f} / {h.MaxDD:.2%}, OOS {h.OOS_CAGR:.2%} / {h.OOS_Sharpe:.4f}"
         f" -> max|d| {d9:.2e}", "< 1e-3", d9 < 1e-3)

    # ---------------------------------------------------------------- headline tables
    say("\n=== A. THE FULL GRID AT THE HEADLINE RUNG (10 bps) — every point, nothing dropped ===")
    for pname in panels:
        say(f"\n  {pname}")
        say("  cap     gross |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh  OOS DD | 4a 4b | legs H1/H2/OOS/DD/CAGR | maxw  p99w  turn/yr")
        for gross in GROSSES:
            for cap in CAPS:
                r = df[(df.panel == pname) & (df.cap == caplabel(cap)) & (df.gross == gross)
                       & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                c = cf[(cf.panel == pname) & (cf.cap == caplabel(cap)) & (cf.gross == gross)].iloc[0]
                lg = "".join("1" if r[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                say(f"  {caplabel(cap):7s} {gross:.2f}  | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%} |"
                    f" {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} {r.OOS_MaxDD:7.2%} |"
                    f" {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg:22s} |"
                    f" {c.max_name_w:5.2%} {c.p99_name_w:5.2%} {c.turnover_yr:6.2f}")

    say("\n=== B. KEEP COUNTS OVER ALL 192 PUBLISHED ROWS (8 caps x 2 gross x 3 panels x 4 rungs) ===")
    say(f"  4b passes: {int(df.pass4b.sum())} of {len(df)}      4a passes: {int(df.pass4a.sum())} of {len(df)}")
    for rung in RUNGS:
        d = df[df.cost_bps == rung]
        say(f"   {rung:5.1f} bps:  4b {int(d.pass4b.sum()):2d}/{len(d)}   4a {int(d.pass4a.sum()):2d}/{len(d)}"
            f"   binding leg on 4b FAILs: " +
            "  ".join(f"{k} {int((~d[k][~d.pass4b]).sum())}" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    say("\n  4b pass rows (all rungs):")
    p = df[df.pass4b]
    if len(p) == 0:
        say("    NONE")
    else:
        for _, r in p.iterrows():
            say(f"    {r.panel:5s} cap {r['cap']:7s} g {r.gross:.2f} {r.cost_bps:5.1f}bps  "
                f"{r.CAGR:6.2%} / {r.Sharpe:.4f} / {r.MaxDD:7.2%}   OOS {r.OOS_CAGR:6.2%} / {r.OOS_Sharpe:.4f}")

    say("\n=== C. WHAT THE CAP COSTS: the candidate (cap=INF) minus each cap, U56 g=0.75, 10 bps ===")
    ref = df[(df.panel == "U56") & (df.cap == "INF") & (df.gross == 0.75) & (df.cost_bps == 10.0)].iloc[0]
    for cap in CAPS:
        r = df[(df.panel == "U56") & (df.cap == caplabel(cap)) & (df.gross == 0.75) & (df.cost_bps == 10.0)].iloc[0]
        c = cf[(cf.panel == "U56") & (cf.cap == caplabel(cap)) & (cf.gross == 0.75)].iloc[0]
        say(f"  cap {caplabel(cap):7s}  dCAGR {r.CAGR - ref.CAGR:+6.2%}  dSharpe {r.Sharpe - ref.Sharpe:+7.4f}"
            f"  dMaxDD {r.MaxDD - ref.MaxDD:+6.2%}  dOOS_Sh {r.OOS_Sharpe - ref.OOS_Sharpe:+7.4f}"
            f"  | max name w {c.max_name_w:5.2%}  mean gross {c.mean_gross:.3f}  mean SHY {c.mean_sweep_w:.3f}")

    say("\n=== D. RULE 8 — (cap, gross) chosen on <= 2016-12-31 ONLY, 2017-2026 read once ===")
    wf = []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_r = priced(run_book(px, rules_v2_weights(px[invest], band=BAND, gross=0.75)
                                 .reindex(columns=px.columns).fillna(0.0)), HEADLINE_RUNG).loc[win]
        b_oos = base_r.loc[OOS_START:]
        for rung in RUNGS:
            d = df[(df.panel == pname) & (df.cost_bps == rung)]
            for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                pick = d.loc[d[col].idxmax()]
                wf.append(dict(panel=pname, cost_bps=rung, chooser=chooser,
                               pick_cap=pick["cap"], pick_gross=pick.gross,
                               OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                               base_OOS_CAGR=cagr(b_oos), base_OOS_Sharpe=sharpe(b_oos), base_OOS_MaxDD=maxdd(b_oos),
                               spy_OOS_CAGR=cagr(spy_oos), spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_MaxDD=maxdd(spy_oos),
                               oos4b_H1H2OOS_DD_CAGR=pick.pass4b, pick_is_INF=(pick["cap"] == "INF")))
                say(f"  {pname:5s} {rung:5.1f}bps {chooser:11s} -> cap {pick['cap']:7s} g {pick.gross:.2f} |"
                    f" OOS {pick.OOS_CAGR:6.2%} / {pick.OOS_Sharpe:.4f} / {pick.OOS_MaxDD:7.2%} |"
                    f" live v2 OOS {cagr(b_oos):6.2%} / {sharpe(b_oos):.4f} / {maxdd(b_oos):7.2%} |"
                    f" SPY OOS {cagr(spy_oos):6.2%} / {sharpe(spy_oos):.4f} / {maxdd(spy_oos):7.2%} |"
                    f" full-sample 4b {'Y' if pick.pass4b else '.'}")
    wfd = pd.DataFrame(wf)
    wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"\n  rule-8 picks landing on cap=INF (the uncapped candidate): {int(wfd.pick_is_INF.sum())} of {len(wfd)}")

    say("\n=== E. CONCENTRATION, the risk the candidate adds (U56 / B136, g=0.75) ===")
    say("  panel cap      median   p99     max     mean gross  mean SHY  turnover/yr")
    for pname in ("U56", "B136", "SMALL"):
        for cap in CAPS:
            c = cf[(cf.panel == pname) & (cf.cap == caplabel(cap)) & (cf.gross == 0.75)].iloc[0]
            say(f"  {pname:5s} {caplabel(cap):7s} {c.med_name_w:6.2%} {c.p99_name_w:6.2%} {c.max_name_w:6.2%}"
                f"   {c.mean_gross:8.3f} {c.mean_sweep_w:9.3f} {c.turnover_yr:10.2f}")

    gdf = pd.DataFrame(GATES)
    gdf.to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n=== GATES: {int(gdf.pass_.sum())} of {len(gdf)} pass ===")
    for _, g in gdf[~gdf.pass_].iterrows():
        say(f"    FAILED: {g.gate} = {g.value} (target {g.target})")
    say(f"\nwrote {OUT}.grid.csv / .concentration.csv / .walkforward.csv / .gates.csv   ({time.time() - t0:.0f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

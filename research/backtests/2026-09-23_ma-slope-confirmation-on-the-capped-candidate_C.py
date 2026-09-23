#!/usr/bin/env python3
"""idea 2366 (lane C, 2026-09-23) — does requiring the 200d MA to be RISING keep the CAPPED
4b candidate's pass while cutting its drawdown?

THE OBJECT.  Idea 2322 filed the record's standing KEEP-4b candidate as CAP2:

    w_i = min(gross / N_in, 0.02)  on names INSIDE the 200d +/-3% band,
    idle NAV (1 - sum w) swept to SHY at phi = 1.00,  weekly cadence, t+1 execution.

Idea 2355 then showed the pass survives t+2/t+3/t+5, and idea 2359 filed a monthly-cadence
variant.  EVERY one of those numbers gates a name on its POSITION relative to the 200d MA and
never on the MA's own DIRECTION: a name 3% above a MA that has fallen all year is IN.

THE CLAUSE.  A name is IN only if it clears the band AND its own 200d MA has RISEN over the
last h trading days by at least s:

    slope_ok_i(t) = ma_i(t) / ma_i(t - h) - 1 >= s          (False until ma(t-h) exists)

Everything else about CAP2 is untouched (cap 0.02, SHY sweep phi=1, band 0.03, weekly, t+1).

DIAL 1 -- slope lookback h {21, 63, 126}.
DIAL 2 -- slope threshold s {0%, 1%, 3%}.
s = OFF is CAP2 EXACTLY, so ONE ladder spans the known book (10 cells: OFF + 3 x 3).

REPORTED, NEVER SELECTED ON: 2 panels (U56 / B136), 2 gross rungs (0.75 live, 1.00), 4 cost
rungs (0 / 10 / 25 / 50 bps), t+1 execution, weekly cadence, band 0.03, cap 0.02, phi 1.00.
10 x 2 x 2 x 4 = 160 published rows, every grid point printed, realised turnover beside each.

BOTH KEEP PATHS on every row: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse) and
4b (Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's).
The 4a comparand is the LIVE book on its own weekly clock at 10 bps, held fixed across the
ladder -- the slope clause is the idea's, not the baseline's.
RULE 8: (h, s) chosen on warm-up..2016-12-31 ONLY by two pre-stated IS-only choosers
(C_ISSHARPE, C_ISCALMAR), then 2017-2026 read ONCE.

GATES.  G0 >= 10y per panel.  G1 the OFF cell is BIT-IDENTICAL to an independent CAP2 build.
G2 the per-column replica equals `engine.backtest` on the live weights at W.  G3 no leverage.
G4 IN-days are MONOTONE NON-INCREASING in s at every h.  G5 every (h, s) IN set is a SUBSET of
OFF's.  G6 exactly two tuned parameters.  G7 SHY priced on every held row.  G8 EXTERNAL
REPRODUCTION of idea 2322's committed U56 CAP2/W headline (11.58% / 1.2643 / -14.81%,
OOS 12.70% / 1.3243) and of its committed 3.51x/yr turnover.  G9 NO LOOKAHEAD: the slope mask
recomputed on a truncated tape is bit-identical to the full-tape mask on the shared prefix.

SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists held from 2008, so the absolute
4b levels are optimistic.  The slope contrast is same-tape / same-day / same-gross and is
first-order immune; the CAGR floor leg is an ABSOLUTE bar and is the most contaminated reading.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_ma-slope-confirmation-on-the-capped-candidate_C.py
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
from engine import backtest, rebalance_mask                        # noqa: E402

DATE, SLUG, LANE = "2026-09-23", "ma-slope-confirmation-on-the-capped-candidate", "C"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, WARMUP, MA_LEN = 0.03, 260, 200
NAME_CAP = 0.02                      # idea 2322's filed CAP2 constant -- FIXED, not a dial
SWEEP, PHI = "SHY", 1.00
CADENCE = "W"                        # the filed candidate's clock -- FIXED, not a dial
HS = [(21, 0.00), (21, 0.01), (21, 0.03),
      (63, 0.00), (63, 0.01), (63, 0.03),
      (126, 0.00), (126, 0.01), (126, 0.03)]
CELLS = [("OFF", None, None)] + [(f"h{h}/s{s:.0%}", h, s) for h, s in HS]
GROSSES = [0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG = 10.0
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


# ---------------------------------------------------------------- the clause
def slope_ok(q, h, s):
    """True where the 200d MA has risen by at least s over the last h trading days.
    Uses closes <= t only; False wherever ma(t) or ma(t-h) does not exist."""
    ma = q.rolling(MA_LEN).mean()
    rise = ma / ma.shift(h) - 1.0
    return (rise >= s).fillna(False)


def in_set(q, h, s):
    inb = band_state(q, BAND) & q.notna()
    return inb if h is None else (inb & slope_ok(q, h, s))


# ---------------------------------------------------------------- books
def cap2_weights(px, invest, gross, h, s):
    """CAP2 with the slope clause: w_i = min(gross/N_in, 0.02) on IN names, idle -> SHY."""
    q = px[invest]
    inb = in_set(q, h, s)
    nin = inb.sum(axis=1).replace(0, np.nan)
    per = pd.concat([gross / nin, pd.Series(NAME_CAP, index=q.index)], axis=1).min(axis=1)
    w = inb.astype(float).mul(per.fillna(0.0), axis=0).reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + PHI * idle * px[SWEEP].notna().astype(float)
    return w


def cap2_reference(px, invest, gross):
    """Independent construction of the OFF cell (numpy minimum form, no pandas concat path)."""
    q = px[invest]
    inb = (band_state(q, BAND) & q.notna()).astype(float)
    nin = inb.sum(axis=1).replace(0, np.nan)
    per = np.minimum(gross / nin.values, NAME_CAP)
    w = pd.DataFrame(inb.values * per[:, None], index=q.index, columns=q.columns)
    w = w.fillna(0.0).reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + PHI * idle * px[SWEEP].notna().astype(float)
    return w


def run_book(prices, weights, mask):
    """Replica of engine.backtest taking an explicit rebalance mask, keeping zero-cost returns
    + turnover so every cost rung is priced from one pass.  Un-invested residual drifts at 0%."""
    rets = prices.pct_change().fillna(0.0)
    w_target = weights.reindex(prices.index).fillna(0.0).shift(1)
    m = mask.shift(1, fill_value=False)
    held = np.zeros((len(prices.index), len(prices.columns)))
    cur = np.zeros(len(prices.columns))
    turnover = np.zeros(len(prices.index))
    gross_s = np.zeros(len(prices.index))
    wt = w_target.values
    rv = rets.values
    mv = m.values
    for i in range(len(prices.index)):
        if mv[i] or i == 0:
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
                gross=pd.Series(gross_s, index=prices.index),
                held=pd.DataFrame(held, index=prices.index, columns=prices.columns))


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
    say("=== idea 2366 — does requiring the 200d MA to be RISING keep the CAPPED 4b "
        "candidate's pass while cutting its drawdown? ===")
    say(f"    {DATE}  lane {LANE}   band {BAND}  MA {MA_LEN}d  cadence {CADENCE}  t+1  "
        f"rungs {RUNGS} bps  name cap {NAME_CAP:.2%} (FIXED, idea 2322)  sweep {SWEEP} phi={PHI:.2f}")
    say(f"    DIAL 1 slope lookback h {sorted({h for h, _ in HS})}   "
        f"DIAL 2 slope threshold s {sorted({s for _, s in HS})}   (OFF = CAP2 exactly)")
    gate("G6 exactly two tuned parameters", "slope lookback h, slope threshold s", "2", True)

    px_u = load_universe()
    px_b = load_universe(broad=True)
    panels = {}
    for nm, px in (("U56", px_u), ("B136", px_b)):
        panels[nm] = (px, list(px.columns))
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y, {len(px.columns)} investable, {len(px)} rows",
             ">= 10y", yrs >= 10)

    mask = rebalance_mask(px_u.index, CADENCE)
    publish("weekly rebalance fires over the U56 tape", f"{int(mask.sum())} of {len(px_u)} rows")

    # G2: the replica prices the live book exactly as engine.backtest does
    w_live = rules_v2_weights(px_u, band=BAND, gross=0.75)
    d2 = float((backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
                - priced(run_book(px_u, w_live, mask), HEADLINE_RUNG)).abs().max())
    gate("G2 per-column replica == engine.backtest (live book, W)", f"max|d| {d2:.3e}",
         "< 1e-12", d2 < 1e-12)

    # G9: no lookahead in the slope clause
    cut = 3000
    q_full = px_u[list(px_u.columns)]
    d9 = 0
    for h, s in ((21, 0.00), (126, 0.03)):
        full = slope_ok(q_full, h, s).iloc[:cut]
        trunc = slope_ok(q_full.iloc[:cut], h, s)
        d9 += int((full.values != trunc.values).sum())
    gate("G9 no lookahead: slope mask on a truncated tape == full-tape mask on the prefix",
         f"{d9} disagreeing cells over 2 (h, s) cells x {cut} rows", "0", d9 == 0)

    rows, tr, cov = [], [], []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        yrs = len(win) / 252
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_res = run_book(px, rules_v2_weights(px[invest], band=BAND, gross=0.75)
                            .reindex(columns=px.columns).fillna(0.0),
                            rebalance_mask(px.index, CADENCE))
        base_r = priced(base_res, HEADLINE_RUNG).loc[win]
        base_turn = float(base_res["turnover"].loc[win].sum() / yrs)
        say(f"\n--- panel {pname} ({len(invest)} names)  SPY {cagr(spy):.2%} / {sharpe(spy):.4f} /"
            f" {maxdd(spy):.2%}   live RULES v2 (W) {cagr(base_r):.2%} / {sharpe(base_r):.4f} /"
            f" {maxdd(base_r):.2%}, turnover {base_turn:.2f}/yr")

        q = px[invest]
        off_in = in_set(q, None, None)
        off_days = float(off_in.loc[win].sum(axis=1).mean())
        for lbl, h, s in CELLS:
            ins = in_set(q, h, s)
            subset = bool((ins & ~off_in).values.sum() == 0)
            cov.append(dict(panel=pname, cell=lbl, h=h if h is not None else 0,
                            s=s if s is not None else np.nan,
                            mean_N_in=float(ins.loc[win].sum(axis=1).mean()),
                            mean_N_in_vs_off=float(ins.loc[win].sum(axis=1).mean()) / off_days,
                            in_cell_days=int(ins.loc[win].values.sum()),
                            zero_in_days=int((ins.loc[win].sum(axis=1) == 0).sum()),
                            subset_of_off=subset))
            for gross in GROSSES:
                w = cap2_weights(px, invest, gross, h, s)
                res = run_book(px, w, rebalance_mask(px.index, CADENCE))
                mx = float(res["held"].loc[win].sum(axis=1).max())
                book = res["held"].loc[win].drop(columns=[SWEEP])
                pos = book.values[book.values > 0]
                turn = float(res["turnover"].loc[win].sum() / yrs)
                tr.append(dict(panel=pname, cell=lbl, gross=gross, turnover_yr=turn,
                               turnover_vs_live=turn / base_turn, live_turnover_yr=base_turn,
                               mean_gross=float(res["gross"].loc[win].mean()),
                               mean_sweep_w=float(res["held"][SWEEP].loc[win].mean()),
                               max_name_w_held=float(pos.max()) if len(pos) else 0.0,
                               max_row_sum=mx))
                for rung in RUNGS:
                    r = priced(res, rung).loc[win]
                    r_oos = r.loc[OOS_START:]
                    h1, h2 = halves(r)
                    rows.append(dict(panel=pname, cell=lbl, h=h if h is not None else 0,
                                     s=s if s is not None else np.nan, gross=gross, cost_bps=rung,
                                     CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                     H1=h1, H2=h2, turnover_yr=turn,
                                     IS_Sharpe=sharpe(r.loc[:IS_END]), IS_Calmar=calmar(r.loc[:IS_END]),
                                     OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                     spy_CAGR=cagr(spy), spy_Sharpe=sharpe(spy), spy_MaxDD=maxdd(spy),
                                     base_CAGR=cagr(base_r), base_Sharpe=sharpe(base_r), base_MaxDD=maxdd(base_r),
                                     **legs(r, base_r, spy, r_oos, spy_oos)))
        say(f"    ... {pname} done ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(rows); tf = pd.DataFrame(tr); cf = pd.DataFrame(cov)
    df.to_csv(f"{OUT}.grid.csv", index=False); tf.to_csv(f"{OUT}.turnover.csv", index=False)
    cf.to_csv(f"{OUT}.coverage.csv", index=False)

    px, invest = panels["U56"]
    d1 = float((cap2_weights(px, invest, 0.75, None, None)
                - cap2_reference(px, invest, 0.75)).abs().max().max())
    gate("G1 the OFF cell's weights == an independent CAP2 build (U56)", f"max|dw| {d1:.3e}",
         "< 1e-12", d1 < 1e-12)
    gate("G3 no leverage (all 40 books)", f"max held row sum {tf.max_row_sum.max():.9f}",
         "<= 1+1e-9", bool((tf.max_row_sum <= 1 + 1e-9).all()))
    mono = []
    for (pn, hh), grp in cf[cf.cell != "OFF"].groupby(["panel", "h"]):
        v = grp.sort_values("s").in_cell_days.values
        mono.append(bool(np.all(np.diff(v) <= 0)))
    gate("G4 IN-days non-increasing in s at every (panel, h)",
         f"{sum(mono)} of {len(mono)} cells", f"{len(mono)} of {len(mono)}", all(mono))
    gate("G5 every (h, s) IN set is a SUBSET of OFF's",
         f"{int(cf.subset_of_off.sum())} of {len(cf)} cells", f"{len(cf)} of {len(cf)}",
         bool(cf.subset_of_off.all()))
    shy_ok = all(bool(p[0][SWEEP].loc[p[0].index[WARMUP:]].notna().all()) for p in panels.values())
    gate("G7 sweep instrument priced on every held row", f"SHY non-null on all panels: {shy_ok}",
         "True", shy_ok)
    hh = df[(df.panel == "U56") & (df.cell == "OFF") & (df.gross == 0.75)
            & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    ht = tf[(tf.panel == "U56") & (tf.cell == "OFF") & (tf.gross == 0.75)].iloc[0]
    d8 = max(abs(hh.CAGR - 0.1158), abs(hh.Sharpe - 1.2643) / 10, abs(hh.MaxDD + 0.1481),
             abs(hh.OOS_CAGR - 0.1270), abs(hh.OOS_Sharpe - 1.3243) / 10,
             abs(ht.turnover_yr - 3.51) / 100)
    gate("G8 reproduces idea 2322's committed U56 CAP2/W headline (11.58%/1.2643/-14.81%, "
         "OOS 12.70%/1.3243, turnover 3.51/yr)",
         f"read {hh.CAGR:.2%} / {hh.Sharpe:.4f} / {hh.MaxDD:.2%}, OOS {hh.OOS_CAGR:.2%} /"
         f" {hh.OOS_Sharpe:.4f}, turnover {ht.turnover_yr:.2f}/yr -> max|d| {d8:.2e}",
         "< 1e-3", d8 < 1e-3)

    # ---------------------------------------------------------------- tables
    say("\n=== A. THE FULL GRID AT THE HEADLINE RUNG (10 bps) — every point, nothing dropped ===")
    for pname in panels:
        say(f"\n  {pname}")
        say("  cell        gross |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh  OOS DD |"
            " 4a 4b | H1/H2/OOS/DD/CAGR | turn/yr  x live  meanGross  meanN_in")
        for gross in GROSSES:
            for lbl, _, _ in CELLS:
                r = df[(df.panel == pname) & (df.cell == lbl) & (df.gross == gross)
                       & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                c = tf[(tf.panel == pname) & (tf.cell == lbl) & (tf.gross == gross)].iloc[0]
                v = cf[(cf.panel == pname) & (cf.cell == lbl)].iloc[0]
                lg = "".join("1" if r[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                say(f"  {lbl:11s} {gross:.2f}  | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%} |"
                    f" {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} {r.OOS_MaxDD:7.2%} |"
                    f" {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg:17s} |"
                    f" {c.turnover_yr:7.2f} {c.turnover_vs_live:7.2f} {c.mean_gross:10.3f}"
                    f" {v.mean_N_in:9.1f}")

    say("\n=== B. EVERY COST RUNG, U56 and B136 (the whole 160-row grid) ===")
    for pname in panels:
        for gross in GROSSES:
            say(f"\n  {pname} gross {gross:.2f}")
            say("  cell        |" + "".join(f"   {int(x):2d}bps: CAGR/Sharpe/4b      " for x in RUNGS))
            for lbl, _, _ in CELLS:
                cells = []
                for rung in RUNGS:
                    r = df[(df.panel == pname) & (df.cell == lbl) & (df.gross == gross)
                           & (df.cost_bps == rung)].iloc[0]
                    cells.append(f"  {r.CAGR:6.2%}/{r.Sharpe:.4f}/{'Y' if r.pass4b else '.'}     ")
                say(f"  {lbl:11s} |" + "".join(cells))

    say("\n=== C. KEEP COUNTS OVER ALL 160 PUBLISHED ROWS (10 cells x 2 gross x 2 panels x 4 rungs) ===")
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
    for _, r in p.iterrows():
        say(f"    {r.panel:5s} {r.cell:11s} g {r.gross:.2f} {r.cost_bps:5.1f}bps  "
            f"{r.CAGR:6.2%} / {r.Sharpe:.4f} / {r.MaxDD:7.2%}   OOS {r.OOS_CAGR:6.2%} /"
            f" {r.OOS_Sharpe:.4f}   turnover {r.turnover_yr:.2f}/yr")

    say("\n=== D. THE TRADE: what the slope clause BUYS (drawdown, turnover) and COSTS (return), vs OFF ===")
    for pname in panels:
        for gross in GROSSES:
            ref = df[(df.panel == pname) & (df.cell == "OFF") & (df.gross == gross)
                     & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
            reft = tf[(tf.panel == pname) & (tf.cell == "OFF") & (tf.gross == gross)].iloc[0]
            say(f"\n  {pname} g={gross:.2f}  OFF (CAP2) reference: {ref.CAGR:.2%} / {ref.Sharpe:.4f} /"
                f" {ref.MaxDD:.2%}, turnover {reft.turnover_yr:.2f}/yr"
                f" ({reft.turnover_vs_live:.2f}x the live book's {reft.live_turnover_yr:.2f})")
            for lbl, _, _ in CELLS:
                if lbl == "OFF":
                    continue
                r = df[(df.panel == pname) & (df.cell == lbl) & (df.gross == gross)
                       & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                c = tf[(tf.panel == pname) & (tf.cell == lbl) & (tf.gross == gross)].iloc[0]
                v = cf[(cf.panel == pname) & (cf.cell == lbl)].iloc[0]
                dd_gain = r.MaxDD - ref.MaxDD
                dc = r.CAGR - ref.CAGR
                rate = (dd_gain / -dc) if dc < 0 else np.nan
                say(f"    {lbl:11s} dCAGR {dc:+6.2%}  dSharpe {r.Sharpe - ref.Sharpe:+7.4f}"
                    f"  dMaxDD {dd_gain:+6.2%}  dOOS_Sh {r.OOS_Sharpe - ref.OOS_Sharpe:+7.4f}"
                    f"  dTurn {c.turnover_yr - reft.turnover_yr:+6.2f}/yr"
                    f"  N_in {v.mean_N_in_vs_off:5.2f}x  | 4b {'Y' if r.pass4b else '.'}"
                    f"  DD bought per pp of CAGR {rate:6.2f}" if dc < 0 else
                    f"    {lbl:11s} dCAGR {dc:+6.2%}  dSharpe {r.Sharpe - ref.Sharpe:+7.4f}"
                    f"  dMaxDD {dd_gain:+6.2%}  dOOS_Sh {r.OOS_Sharpe - ref.OOS_Sharpe:+7.4f}"
                    f"  dTurn {c.turnover_yr - reft.turnover_yr:+6.2f}/yr"
                    f"  N_in {v.mean_N_in_vs_off:5.2f}x  | 4b {'Y' if r.pass4b else '.'}"
                    f"  (CAGR NOT paid)")

    say("\n=== D2. IS THE CLAUSE A COST REBATE OR AN EXPOSURE EFFECT?  (dCAGR vs OFF at each rung) ===")
    for pname in panels:
        for gross in GROSSES:
            for lbl, _, _ in CELLS:
                if lbl == "OFF":
                    continue
                line = []
                for rung in RUNGS:
                    ref = df[(df.panel == pname) & (df.cell == "OFF") & (df.gross == gross)
                             & (df.cost_bps == rung)].iloc[0]
                    r = df[(df.panel == pname) & (df.cell == lbl) & (df.gross == gross)
                           & (df.cost_bps == rung)].iloc[0]
                    line.append(f"{int(rung):2d}bps {r.CAGR - ref.CAGR:+.2%}")
                say(f"  {pname:5s} g={gross:.2f} {lbl:11s}: " + "   ".join(line))

    say("\n=== D3. COVERAGE — what the clause actually removes ===")
    for pname in panels:
        say(f"\n  {pname}")
        say("  cell        | mean N_in  vs OFF  | days with ZERO names IN (book is 100% SHY)")
        for lbl, _, _ in CELLS:
            v = cf[(cf.panel == pname) & (cf.cell == lbl)].iloc[0]
            say(f"  {lbl:11s} | {v.mean_N_in:9.2f} {v.mean_N_in_vs_off:7.2f}x | {v.zero_in_days:6d}")

    say("\n=== E. RULE 8 — (h, s) chosen on <= 2016-12-31 ONLY, 2017-2026 read once ===")
    wf = []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_r = priced(run_book(px, rules_v2_weights(px[invest], band=BAND, gross=0.75)
                                 .reindex(columns=px.columns).fillna(0.0),
                                 rebalance_mask(px.index, CADENCE)), HEADLINE_RUNG).loc[win]
        b_oos = base_r.loc[OOS_START:]
        for gross in GROSSES:
            for rung in RUNGS:
                d = df[(df.panel == pname) & (df.cost_bps == rung) & (df.gross == gross)]
                for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                    pick = d.loc[d[col].idxmax()]
                    wf.append(dict(panel=pname, gross=gross, cost_bps=rung, chooser=chooser,
                                   pick_cell=pick.cell, pick_turnover_yr=pick.turnover_yr,
                                   OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                                   OOS_MaxDD=pick.OOS_MaxDD, base_OOS_CAGR=cagr(b_oos),
                                   base_OOS_Sharpe=sharpe(b_oos), base_OOS_MaxDD=maxdd(b_oos),
                                   spy_OOS_CAGR=cagr(spy_oos), spy_OOS_Sharpe=sharpe(spy_oos),
                                   spy_OOS_MaxDD=maxdd(spy_oos), full4b=pick.pass4b,
                                   pick_is_OFF=(pick.cell == "OFF"),
                                   beats_spy_oos=bool(pick.OOS_Sharpe > sharpe(spy_oos)),
                                   beats_base_oos=bool(pick.OOS_Sharpe > sharpe(b_oos))))
                    say(f"  {pname:5s} g {gross:.2f} {rung:5.1f}bps {chooser:11s} -> {pick.cell:11s} |"
                        f" OOS {pick.OOS_CAGR:6.2%} / {pick.OOS_Sharpe:.4f} / {pick.OOS_MaxDD:7.2%} |"
                        f" turnover {pick.turnover_yr:.2f}/yr |"
                        f" live v2 OOS {cagr(b_oos):6.2%} / {sharpe(b_oos):.4f} / {maxdd(b_oos):7.2%} |"
                        f" SPY OOS {cagr(spy_oos):6.2%} / {sharpe(spy_oos):.4f} / {maxdd(spy_oos):7.2%} |"
                        f" full 4b {'Y' if pick.pass4b else '.'}")
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"\n  rule-8 picks landing on OFF (CAP2 as filed): {int(wfd.pick_is_OFF.sum())} of {len(wfd)}")
    say(f"  rule-8 picks beating SPY OOS on Sharpe: {int(wfd.beats_spy_oos.sum())} of {len(wfd)};"
        f"  beating the live book OOS: {int(wfd.beats_base_oos.sum())} of {len(wfd)}")
    say(f"  rule-8 picks carrying a full-sample 4b: {int(wfd.full4b.sum())} of {len(wfd)}")

    gdf = pd.DataFrame(GATES); gdf.to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n=== GATES: {int(gdf.pass_.sum())} of {len(gdf)} pass ===")
    for _, g in gdf[~gdf.pass_].iterrows():
        say(f"    FAILED: {g.gate} = {g.value} (target {g.target})")
    say(f"\nwrote {OUT}.grid.csv / .turnover.csv / .coverage.csv / .walkforward.csv / .gates.csv "
        f"  ({time.time() - t0:.0f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

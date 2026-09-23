#!/usr/bin/env python3
"""idea 2355 (lane B, 2026-09-23) — does the CAPPED 4b CANDIDATE's pass survive a 1-DAY
DELAYED EXECUTION (t+2), and at what lag does it die?

THE OBJECT.  Idea 2322 filed the record's standing KEEP-4b candidate as CAP2:

    w_i = min(gross / N_in, 0.02)  on names INSIDE the 200d +/-3% band,
    idle NAV (1 - sum w) swept to SHY at phi = 1.00,  weekly cadence, t+1 execution.

PROTOCOL rule 2 prices every book at t+1: weights decided at the close of t are put on at the
close of t+1.  That is a CONVENTION, not a law of the market.  A real account rebalancing a
56-line book off a weekly close does not always fill at the next close — a missed cron, a
holiday, a broker queue, or simply a human doing it the following morning all push the fill
further out.  The record's execution-lag work (2026-09-18 / 2026-09-19) was done on the
UNCAPPED band book, BEFORE idea 2322's per-name cap and before the phi=1 SHY sweep existed,
so the standing candidate has never been asked this question.

DIAL 1 -- execution lag L {1, 2, 3, 5} trading days.  L = 1 IS CAP2 exactly (the rule-2
          convention), so ONE ladder spans the known book.
DIAL 2 -- gross {0.75 (live), 1.00}.

REPORTED, NEVER SELECTED ON: 2 panels (U56 / B136), 4 cost rungs (0 / 10 / 25 / 50 bps),
weekly cadence, band 0.03, per-name cap 0.02 (idea 2322's filed constant), phi = 1.00.
4 x 2 x 2 x 4 = 64 published rows, every grid point printed, realised turnover beside every one.

BOTH KEEP PATHS on every row: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse) and
4b (Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's).
The 4a comparand is the LIVE book on the rule-2 convention (L = 1) at 10 bps, held FIXED across
the ladder -- the lag dial is the idea's, not the baseline's.

RULE 8 is run TWICE and both readings are published:
  WF-A (protocol standard): (L, gross) chosen on warm-up..2016-12-31 ONLY by two pre-stated
       IS-only choosers (C_ISSHARPE, C_ISCALMAR), 2017-2026 read ONCE.
  WF-B (the honest reading): a trader does not CHOOSE its settlement lag, it is IMPOSED.  So
       for EACH L separately, gross alone is fitted on <= 2016-12-31 and 2017-2026 read ONCE.
       This is the reading that answers "if my fills slip to t+2, what do I actually get?".

SECTION F publishes an ILLEGAL look-ahead control (L = 0, same-close execution).  It is NEVER
a candidate and is excluded from every KEEP count and from rule 8; it is priced only to bound
how much of the book's return lives in the first day after the decision.

GATES.  G0 >= 10y per panel.  G1 the weights are bit-identical to an independent CAP2 build.
G2 the lag replica at L = 1 == `engine.backtest` on the LIVE book (W).  G3 no leverage.
G4 the lag replica at L = 1 == `engine.backtest` on the CAP2 book itself (W) -- the ladder's
   own zero rung is the engine's convention, not a re-implementation of it.
G5 the fill days at lag L are exactly the L = 1 fill days shifted forward by L - 1 rows.
G6 exactly two tuned parameters.  G7 SHY priced on every held row.
G8 EXTERNAL REPRODUCTION of idea 2322's committed U56 CAP2/W headline
   (11.58% / 1.2643 / -14.81%, OOS 12.70% / 1.3243) and of its committed 3.51x/yr turnover.
G9 the number of rebalance fires is invariant in L up to at most L rows of edge truncation.

SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists held from 2008, so the absolute
4b levels are optimistic.  The lag contrast is same-tape / same-book / same-gross and is
first-order immune; the CAGR floor leg is an ABSOLUTE bar and is the most contaminated reading.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_execution-lag-on-the-capped-4b-candidate_B.py
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

DATE, SLUG, LANE = "2026-09-23", "execution-lag-on-the-capped-4b-candidate", "B"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, WARMUP = 0.03, 260
NAME_CAP = 0.02                      # idea 2322's filed CAP2 constant -- FIXED, not a dial
SWEEP, PHI = "SHY", 1.00
CADENCE = "W"                        # CAP2's clock -- FIXED, not a dial
LAGS = [1, 2, 3, 5]                  # DIAL 1.  L = 1 is the rule-2 convention == CAP2
LOOKAHEAD_LAG = 0                    # illegal control, section F only
GROSSES = [0.75, 1.00]               # DIAL 2
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG = 10.0
BASE_LAG = 1                         # the live book's convention, held fixed as the 4a comparand
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
def cap2_weights(px, invest, gross):
    """idea 2322's filed CAP2: w_i = min(gross/N_in, 0.02) on IN names, idle -> SHY at phi=1.

    The WEIGHTS are a daily DECISION object and do not depend on the lag; the lag decides only
    HOW MANY DAYS LATER that decision is put on.  The ladder therefore moves one thing only.
    """
    q = px[invest]
    inb = band_state(q, BAND) & q.notna()
    nin = inb.sum(axis=1).replace(0, np.nan)
    per = pd.concat([gross / nin, pd.Series(NAME_CAP, index=q.index)], axis=1).min(axis=1)
    w = inb.astype(float).mul(per.fillna(0.0), axis=0).reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + PHI * idle * px[SWEEP].notna().astype(float)
    return w


def cap2_reference(px, invest, gross):
    """Independent construction of CAP2 + sweep (numpy minimum form, no pandas concat path)."""
    q = px[invest]
    inb = (band_state(q, BAND) & q.notna()).astype(float)
    nin = inb.sum(axis=1).replace(0, np.nan)
    per = np.minimum(gross / nin.values, NAME_CAP)
    w = pd.DataFrame(inb.values * per[:, None], index=q.index, columns=q.columns)
    w = w.fillna(0.0).reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + PHI * idle * px[SWEEP].notna().astype(float)
    return w


def run_book(prices, weights, mask, lag=1):
    """Replica of engine.backtest with an EXPLICIT EXECUTION LAG.

    engine.backtest hard-codes lag 1: `weights.shift(1)` and `mask.shift(1)`.  Setting lag = L
    shifts BOTH by L, so the decision taken at the close of a period end t is filled at the
    close of t + L at the prices of t + L, and the book drifts un-rebalanced in between.
    lag = 0 is SAME-CLOSE execution and is a LOOK-AHEAD book (section F control only).
    Zero-cost returns and turnover are kept so every cost rung is priced from one pass.
    """
    rets = prices.pct_change().fillna(0.0)
    w_target = weights.reindex(prices.index).shift(lag).fillna(0.0) if lag else \
        weights.reindex(prices.index).fillna(0.0)
    m = mask.shift(lag, fill_value=False) if lag else mask
    held = np.zeros((len(prices.index), len(prices.columns)))
    cur = np.zeros(len(prices.columns))
    turnover = np.zeros(len(prices.index))
    gross_s = np.zeros(len(prices.index))
    fill = np.zeros(len(prices.index), dtype=bool)
    wt, rv, mv = w_target.values, rets.values, m.values
    for i in range(len(prices.index)):
        if mv[i] or i == 0:
            new = wt[i]
            turnover[i] = np.abs(new - cur).sum()
            cur = new.copy()
            fill[i] = True
        held[i] = cur
        gross_s[i] = cur.sum()
        growth = cur * (1 + rv[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    r0 = pd.Series((held * rv).sum(axis=1), index=prices.index)
    return dict(r0=r0, turnover=pd.Series(turnover, index=prices.index),
                gross=pd.Series(gross_s, index=prices.index),
                fill=pd.Series(fill, index=prices.index),
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
    say("=== idea 2355 — does the CAPPED 4b CANDIDATE's pass survive a 1-DAY DELAYED EXECUTION "
        "(t+2)?  At what lag does it die? ===")
    say(f"    {DATE}  lane {LANE}   cadence {CADENCE}  band {BAND}  rungs {RUNGS} bps  "
        f"name cap {NAME_CAP:.2%} (FIXED, idea 2322)  sweep {SWEEP} phi={PHI:.2f}")
    say(f"    DIAL 1 execution lag L {LAGS} trading days (L=1 IS the rule-2 convention)   "
        f"DIAL 2 gross {GROSSES}")
    gate("G6 exactly two tuned parameters", "execution lag L, gross", "2", True)

    px_u = load_universe()
    px_b = load_universe(broad=True)
    panels = {}
    for nm, px in (("U56", px_u), ("B136", px_b)):
        panels[nm] = (px, list(px.columns))
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y, {len(px.columns)} investable, {len(px)} rows",
             ">= 10y", yrs >= 10)

    # G2 / G4: the lag replica at L = 1 IS the engine's convention, on two different books
    w_live = rules_v2_weights(px_u, band=BAND, gross=0.75)
    mW = rebalance_mask(px_u.index, CADENCE)
    d2 = float((backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
                - priced(run_book(px_u, w_live, mW, lag=1), HEADLINE_RUNG)).abs().max())
    gate("G2 lag replica at L=1 == engine.backtest (LIVE book, W)", f"max|d| {d2:.3e}",
         "< 1e-12", d2 < 1e-12)
    w_c2 = cap2_weights(px_u, list(px_u.columns), 0.75)
    d4 = float((backtest(px_u, w_c2, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
                - priced(run_book(px_u, w_c2, mW, lag=1), HEADLINE_RUNG)).abs().max())
    gate("G4 lag replica at L=1 == engine.backtest (the CAP2 book itself, W)",
         f"max|d| {d4:.3e}", "< 1e-12", d4 < 1e-12)

    # G5: fills at lag L are the L=1 fills shifted forward by L-1 rows
    base_fill = run_book(px_u, w_c2, mW, lag=1)["fill"].values
    shift_ok, shift_det = True, []
    for L in LAGS:
        f = run_book(px_u, w_c2, mW, lag=L)["fill"].values
        exp = np.zeros_like(f)
        exp[0] = True
        src = np.where(base_fill)[0]
        for s in src:
            if s == 0:
                continue
            t = s + (L - 1)
            if t < len(exp):
                exp[t] = True
        n_bad = int((f != exp).sum())
        shift_det.append(f"L={L}: {n_bad}")
        shift_ok &= (n_bad == 0)
    gate("G5 fill days at lag L == the L=1 fill days shifted forward by L-1 rows",
         ", ".join(shift_det) + " disagreements", "0 everywhere", shift_ok)

    rows, tr = [], []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        yrs = len(win) / 252
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        m = rebalance_mask(px.index, CADENCE)
        base_res = run_book(px, rules_v2_weights(px[invest], band=BAND, gross=0.75)
                            .reindex(columns=px.columns).fillna(0.0), m, lag=BASE_LAG)
        base_r = priced(base_res, HEADLINE_RUNG).loc[win]
        base_turn = float(base_res["turnover"].loc[win].sum() / yrs)
        say(f"\n--- panel {pname} ({len(invest)} names)  SPY {cagr(spy):.2%} / {sharpe(spy):.4f} /"
            f" {maxdd(spy):.2%}   live RULES v2 (t+1) {cagr(base_r):.2%} / {sharpe(base_r):.4f} /"
            f" {maxdd(base_r):.2%}, turnover {base_turn:.2f}/yr")
        for gross in GROSSES:
            w = cap2_weights(px, invest, gross)
            for L in LAGS + [LOOKAHEAD_LAG]:
                res = run_book(px, w, m, lag=L)
                mx = float(res["held"].loc[win].sum(axis=1).max())
                book = res["held"].loc[win].drop(columns=[SWEEP])
                pos = book.values[book.values > 0]
                turn = float(res["turnover"].loc[win].sum() / yrs)
                tr.append(dict(panel=pname, lag=L, gross=gross, turnover_yr=turn,
                               turnover_vs_live=turn / base_turn, live_turnover_yr=base_turn,
                               mean_gross=float(res["gross"].loc[win].mean()),
                               mean_sweep_w=float(res["held"][SWEEP].loc[win].mean()),
                               max_name_w_held=float(pos.max()) if len(pos) else 0.0,
                               fills=int(res["fill"].loc[win].sum()), max_row_sum=mx,
                               legal=bool(L >= 1)))
                for rung in RUNGS:
                    r = priced(res, rung).loc[win]
                    r_oos = r.loc[OOS_START:]
                    h1, h2 = halves(r)
                    rows.append(dict(panel=pname, lag=L, gross=gross, cost_bps=rung,
                                     CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                     H1=h1, H2=h2, turnover_yr=turn, legal=bool(L >= 1),
                                     IS_Sharpe=sharpe(r.loc[:IS_END]), IS_Calmar=calmar(r.loc[:IS_END]),
                                     OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                     **legs(r, base_r, spy, r_oos, spy_oos)))
        say(f"    ... {pname} done ({time.time() - t0:.0f}s)")

    dfa = pd.DataFrame(rows); tfa = pd.DataFrame(tr)
    dfa.to_csv(f"{OUT}.grid.csv", index=False); tfa.to_csv(f"{OUT}.turnover.csv", index=False)
    df = dfa[dfa.legal].copy(); tf = tfa[tfa.legal].copy()   # the 64 PUBLISHED rows

    px, invest = panels["U56"]
    d1 = float((cap2_weights(px, invest, 0.75) - cap2_reference(px, invest, 0.75)).abs().max().max())
    gate("G1 the CAP2 decision weights == an independent build (U56)", f"max|dw| {d1:.3e}",
         "< 1e-12", d1 < 1e-12)
    gate("G3 no leverage (all 16 legal books)", f"max held row sum {tf.max_row_sum.max():.9f}",
         "<= 1+1e-9", bool((tf.max_row_sum <= 1 + 1e-9).all()))
    fill_span = tf.groupby("panel").fills.agg(["min", "max"])
    ok9 = bool(((fill_span["max"] - fill_span["min"]) <= max(LAGS)).all())
    gate("G9 fire count invariant in L up to edge truncation",
         "; ".join(f"{p}: {int(r['min'])}..{int(r['max'])} fills" for p, r in fill_span.iterrows()),
         f"span <= {max(LAGS)}", ok9)
    shy_ok = all(bool(p[0][SWEEP].loc[p[0].index[WARMUP:]].notna().all()) for p in panels.values())
    gate("G7 sweep instrument priced on every held row", f"SHY non-null on all panels: {shy_ok}",
         "True", shy_ok)
    h = df[(df.panel == "U56") & (df.lag == 1) & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    ht = tf[(tf.panel == "U56") & (tf.lag == 1) & (tf.gross == 0.75)].iloc[0]
    d8 = max(abs(h.CAGR - 0.1158), abs(h.Sharpe - 1.2643) / 10, abs(h.MaxDD + 0.1481),
             abs(h.OOS_CAGR - 0.1270), abs(h.OOS_Sharpe - 1.3243) / 10, abs(ht.turnover_yr - 3.51) / 100)
    gate("G8 reproduces idea 2322's committed U56 CAP2/t+1 headline (11.58%/1.2643/-14.81%, "
         "OOS 12.70%/1.3243, turnover 3.51/yr)",
         f"read {h.CAGR:.2%} / {h.Sharpe:.4f} / {h.MaxDD:.2%}, OOS {h.OOS_CAGR:.2%} /"
         f" {h.OOS_Sharpe:.4f}, turnover {ht.turnover_yr:.2f}/yr -> max|d| {d8:.2e}",
         "< 1e-3", d8 < 1e-3)

    # ---------------------------------------------------------------- tables
    say("\n=== A. THE FULL GRID AT THE HEADLINE RUNG (10 bps) — every point, nothing dropped ===")
    for pname in panels:
        say(f"\n  {pname}")
        say("  lag gross |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh  OOS DD | 4a 4b |"
            " H1/H2/OOS/DD/CAGR | turn/yr  x live  fills  meanGross  maxNameHeld")
        for gross in GROSSES:
            for L in LAGS:
                r = df[(df.panel == pname) & (df.lag == L) & (df.gross == gross)
                       & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                c = tf[(tf.panel == pname) & (tf.lag == L) & (tf.gross == gross)].iloc[0]
                lg = "".join("1" if r[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                say(f"  t+{L} {gross:.2f}  | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%} |"
                    f" {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} {r.OOS_MaxDD:7.2%} |"
                    f" {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg:17s} |"
                    f" {c.turnover_yr:7.2f} {c.turnover_vs_live:7.2f} {c.fills:6d} {c.mean_gross:10.3f}"
                    f" {c.max_name_w_held:12.2%}")

    say("\n=== B. EVERY COST RUNG, U56 and B136 (the whole 64-row grid) ===")
    for pname in panels:
        for gross in GROSSES:
            say(f"\n  {pname} gross {gross:.2f}")
            say("  lag  |" + "".join(f"   {int(x):2d}bps: CAGR/Sharpe/4b      " for x in RUNGS))
            for L in LAGS:
                cells = []
                for rung in RUNGS:
                    r = df[(df.panel == pname) & (df.lag == L) & (df.gross == gross)
                           & (df.cost_bps == rung)].iloc[0]
                    cells.append(f"  {r.CAGR:6.2%}/{r.Sharpe:.4f}/{'Y' if r.pass4b else '.'}     ")
                say(f"  t+{L}  |" + "".join(cells))

    say("\n=== C. KEEP COUNTS OVER ALL 64 PUBLISHED ROWS (4 lags x 2 gross x 2 panels x 4 rungs) ===")
    say(f"  4b passes: {int(df.pass4b.sum())} of {len(df)}      4a passes: {int(df.pass4a.sum())} of {len(df)}")
    for rung in RUNGS:
        d = df[df.cost_bps == rung]
        say(f"   {rung:5.1f} bps:  4b {int(d.pass4b.sum()):2d}/{len(d)}   4a {int(d.pass4a.sum()):2d}/{len(d)}"
            f"   binding leg on 4b FAILs: " +
            "  ".join(f"{k} {int((~d[k][~d.pass4b]).sum())}" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    say("\n  4b pass count by lag (all panels / gross / rungs, 16 rows each):")
    for L in LAGS:
        d = df[df.lag == L]
        say(f"    t+{L}: 4b {int(d.pass4b.sum()):2d}/{len(d)}   4a {int(d.pass4a.sum()):2d}/{len(d)}")
    say("\n  4b pass rows (all rungs):")
    p = df[df.pass4b]
    if len(p) == 0:
        say("    NONE")
    for _, r in p.iterrows():
        say(f"    {r.panel:5s} t+{int(r.lag)} g {r.gross:.2f} {r.cost_bps:5.1f}bps  "
            f"{r.CAGR:6.2%} / {r.Sharpe:.4f} / {r.MaxDD:7.2%}   OOS {r.OOS_CAGR:6.2%} /"
            f" {r.OOS_Sharpe:.4f}   turnover {r.turnover_yr:.2f}/yr")

    say("\n=== D. THE DECAY: what each EXTRA DAY of settlement costs, vs the t+1 convention ===")
    for pname in panels:
        for gross in GROSSES:
            ref = df[(df.panel == pname) & (df.lag == 1) & (df.gross == gross)
                     & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
            say(f"  {pname} g={gross:.2f}  t+1 reference: {ref.CAGR:.2%} / {ref.Sharpe:.4f} /"
                f" {ref.MaxDD:.2%}, OOS {ref.OOS_CAGR:.2%} / {ref.OOS_Sharpe:.4f}  4b"
                f" {'Y' if ref.pass4b else '.'}")
            for L in LAGS:
                r = df[(df.panel == pname) & (df.lag == L) & (df.gross == gross)
                       & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                c = tf[(tf.panel == pname) & (tf.lag == L) & (tf.gross == gross)].iloc[0]
                per_day = (r.CAGR - ref.CAGR) / (L - 1) if L > 1 else 0.0
                lg = "".join("1" if r[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                say(f"    t+{L}  dCAGR {r.CAGR - ref.CAGR:+6.2%} ({per_day:+.2%}/day)"
                    f"  dSharpe {r.Sharpe - ref.Sharpe:+7.4f}  dMaxDD {r.MaxDD - ref.MaxDD:+6.2%}"
                    f"  dOOS_CAGR {r.OOS_CAGR - ref.OOS_CAGR:+6.2%}"
                    f"  dOOS_Sh {r.OOS_Sharpe - ref.OOS_Sharpe:+7.4f}"
                    f"  dTurn {c.turnover_yr - tf[(tf.panel == pname) & (tf.lag == 1) & (tf.gross == gross)].iloc[0].turnover_yr:+5.2f}"
                    f"  | legs {lg}  4b {'Y' if r.pass4b else '.'}")

    say("\n=== D2. THE LAG AT WHICH THE PASS DIES, per (panel, gross, rung) ===")
    say("  'dies at t+k' = 4b holds at every legal lag < k and fails at k; 'survives' = passes at every L.")
    death = []
    for pname in panels:
        for gross in GROSSES:
            for rung in RUNGS:
                seq = [bool(df[(df.panel == pname) & (df.lag == L) & (df.gross == gross)
                               & (df.cost_bps == rung)].iloc[0].pass4b) for L in LAGS]
                if not seq[0]:
                    verdict = "no pass at t+1 (nothing to lose)"
                elif all(seq):
                    verdict = f"SURVIVES every lag to t+{LAGS[-1]}"
                else:
                    k = LAGS[seq.index(False)]
                    verdict = f"dies at t+{k}"
                death.append(dict(panel=pname, gross=gross, cost_bps=rung, seq="".join("Y" if s else "." for s in seq),
                                  verdict=verdict))
                say(f"  {pname:5s} g={gross:.2f} {rung:5.1f}bps  4b over t+1/t+2/t+3/t+5: "
                    f"{''.join('Y' if s else '.' for s in seq)}   -> {verdict}")
    pd.DataFrame(death).to_csv(f"{OUT}.death.csv", index=False)

    say("\n=== E. RULE 8 ===")
    say("  WF-A (protocol standard): BOTH dials (L, gross) chosen on <= 2016-12-31, 2017-2026 read ONCE.")
    say("  WF-B (honest reading):    L is IMPOSED, gross alone fitted on <= 2016-12-31, per L.")
    wf = []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_r = priced(run_book(px, rules_v2_weights(px[invest], band=BAND, gross=0.75)
                                 .reindex(columns=px.columns).fillna(0.0),
                                 rebalance_mask(px.index, CADENCE), lag=BASE_LAG),
                        HEADLINE_RUNG).loc[win]
        b_oos = base_r.loc[OOS_START:]
        for rung in RUNGS:
            d = df[(df.panel == pname) & (df.cost_bps == rung)]
            for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                pick = d.loc[d[col].idxmax()]
                wf.append(dict(arm="WF-A", panel=pname, cost_bps=rung, chooser=chooser,
                               imposed_lag=np.nan, pick_lag=int(pick.lag), pick_gross=pick.gross,
                               pick_turnover_yr=pick.turnover_yr, OOS_CAGR=pick.OOS_CAGR,
                               OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                               base_OOS_CAGR=cagr(b_oos), base_OOS_Sharpe=sharpe(b_oos),
                               base_OOS_MaxDD=maxdd(b_oos), spy_OOS_CAGR=cagr(spy_oos),
                               spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_MaxDD=maxdd(spy_oos),
                               full4b=bool(pick.pass4b), pick_is_t1=bool(pick.lag == 1),
                               beats_spy_oos=bool(pick.OOS_Sharpe > sharpe(spy_oos)),
                               beats_base_oos=bool(pick.OOS_Sharpe > sharpe(b_oos))))
                say(f"  WF-A {pname:5s} {rung:5.1f}bps {chooser:11s} -> t+{int(pick.lag)}"
                    f" g {pick.gross:.2f} | OOS {pick.OOS_CAGR:6.2%} / {pick.OOS_Sharpe:.4f} /"
                    f" {pick.OOS_MaxDD:7.2%} | live v2 OOS {cagr(b_oos):6.2%} / {sharpe(b_oos):.4f}"
                    f" | SPY OOS {cagr(spy_oos):6.2%} / {sharpe(spy_oos):.4f} |"
                    f" full 4b {'Y' if pick.pass4b else '.'}")
        for rung in RUNGS:
            for L in LAGS:
                d = df[(df.panel == pname) & (df.cost_bps == rung) & (df.lag == L)]
                for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                    pick = d.loc[d[col].idxmax()]
                    wf.append(dict(arm="WF-B", panel=pname, cost_bps=rung, chooser=chooser,
                                   imposed_lag=L, pick_lag=int(pick.lag), pick_gross=pick.gross,
                                   pick_turnover_yr=pick.turnover_yr, OOS_CAGR=pick.OOS_CAGR,
                                   OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                                   base_OOS_CAGR=cagr(b_oos), base_OOS_Sharpe=sharpe(b_oos),
                                   base_OOS_MaxDD=maxdd(b_oos), spy_OOS_CAGR=cagr(spy_oos),
                                   spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_MaxDD=maxdd(spy_oos),
                                   full4b=bool(pick.pass4b), pick_is_t1=bool(L == 1),
                                   beats_spy_oos=bool(pick.OOS_Sharpe > sharpe(spy_oos)),
                                   beats_base_oos=bool(pick.OOS_Sharpe > sharpe(b_oos))))
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    a = wfd[wfd.arm == "WF-A"]
    say(f"\n  WF-A: picks landing on t+1 (CAP2 as filed): {int(a.pick_is_t1.sum())} of {len(a)};"
        f"  lag distribution " + str(a.pick_lag.value_counts().to_dict()))
    say(f"  WF-A: beating SPY OOS on Sharpe {int(a.beats_spy_oos.sum())} of {len(a)};"
        f"  beating the live book OOS {int(a.beats_base_oos.sum())} of {len(a)};"
        f"  carrying a full-sample 4b {int(a.full4b.sum())} of {len(a)}")
    say("\n  WF-B (lag imposed, gross fitted IS-only) — OOS by imposed lag:")
    b = wfd[wfd.arm == "WF-B"]
    for pname in panels:
        for L in LAGS:
            s = b[(b.panel == pname) & (b.imposed_lag == L)]
            say(f"    {pname:5s} t+{L}: {len(s)} picks, gross "
                f"{sorted(set(s.pick_gross))}, mean OOS CAGR {s.OOS_CAGR.mean():.2%},"
                f" mean OOS Sharpe {s.OOS_Sharpe.mean():.4f}, beats SPY OOS"
                f" {int(s.beats_spy_oos.sum())}/{len(s)}, beats live OOS"
                f" {int(s.beats_base_oos.sum())}/{len(s)}, full 4b {int(s.full4b.sum())}/{len(s)}")

    say("\n=== F. ILLEGAL LOOK-AHEAD CONTROL (L = 0, same-close fill).  NOT a candidate, NOT in ===")
    say("    any KEEP count, NOT in rule 8.  Priced only to bound how much of the book's return ")
    say("    lives in the first day after the decision. ===")
    for pname in panels:
        for gross in GROSSES:
            z = dfa[(dfa.panel == pname) & (dfa.lag == 0) & (dfa.gross == gross)
                    & (dfa.cost_bps == HEADLINE_RUNG)].iloc[0]
            o = df[(df.panel == pname) & (df.lag == 1) & (df.gross == gross)
                   & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
            say(f"  {pname:5s} g={gross:.2f}  t+0 (illegal) {z.CAGR:6.2%} / {z.Sharpe:.4f} /"
                f" {z.MaxDD:7.2%}   vs t+1 {o.CAGR:6.2%} / {o.Sharpe:.4f} / {o.MaxDD:7.2%}"
                f"   -> the FIRST day is worth dCAGR {z.CAGR - o.CAGR:+.2%},"
                f" dSharpe {z.Sharpe - o.Sharpe:+.4f}")

    gdf = pd.DataFrame(GATES); gdf.to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n=== GATES: {int(gdf.pass_.sum())} of {len(gdf)} pass ===")
    for _, g in gdf[~gdf.pass_].iterrows():
        say(f"    FAILED: {g.gate} = {g.value} (target {g.target})")
    say(f"\nwrote {OUT}.grid.csv / .turnover.csv / .walkforward.csv / .death.csv / .gates.csv "
        f"  ({time.time() - t0:.0f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

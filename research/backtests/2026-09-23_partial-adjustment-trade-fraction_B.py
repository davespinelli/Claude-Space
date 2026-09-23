#!/usr/bin/env python3
"""idea 2391 (lane B, 2026-09-23) — does PARTIAL-ADJUSTMENT TRADE-FRACTION DAMPING cut the
CAPPED candidate's 3.51x turnover where the DEADBAND and the HOLD FLOOR could not?

THE OBJECT.  Idea 2300 filed `RG100 + phi = 1.00` (`CAND`: every name INSIDE the 200d +/-3%
band held at `gross / N_in` of NAV, idle NAV swept to SHY) as the record's standing 4b
KEEP-candidate; idea 2322 added a 2.0% per-name cap (`CAP2`).  CAP2 runs at 3.51 turns/yr
against the live book's 1.77, and turnover is the ONLY stated blocker on its adoption.

The record has now KILLED both DISCRETE turnover devices on this exact book:
  * idea 2328's weight-drift NO-TRADE BAND — at 100% held-set fidelity it removes only
    3.51 -> 3.07 turns/yr; every deep cut sits at broken fidelity;
  * idea 2351's MINIMUM HOLDING PERIOD — KILL as the adoption fix.
Both are DEADBANDS: a name either trades in full or not at all, so neither cuts anything
until it has already broken the held set.

THE THIRD CLASSICAL DEVICE IS LINEAR AND HAS NEVER BEEN PRICED ANYWHERE IN THIS RECORD:

    at each weekly rebalance, move EVERY risk name a fixed fraction lam of the way to target
        w_new_i = w_held_i + lam * (w_target_i - w_held_i)
    and let SHY absorb the residual (phi = 1.00), so w_SHY = 1 - sum(risk weights).

It shrinks every trade — entries, exits and re-sizings alike — instead of suppressing a
subset, so it pays in LAG rather than in fidelity.

THE IDEA'S OWN COST IS MEASURED, NOT ASSUMED.  A name the 200d band gates OUT has target 0
and is therefore only ever sold FRACTIONALLY: its weight decays as (1 - lam)^k and never
reaches zero.  Section E publishes the resulting STUB MASS (share of NAV held in names whose
target is 0 that day), the effective number of names held, and the max per-name weight — the
concentration CAP2 exists to hold down — at every rung of the ladder.

DIAL 1 -- lam {1.00, 0.85, 0.70, 0.55, 0.40, 0.25, 0.10}.  lam = 1.00 IS the undamped book
          and must reproduce engine.backtest bit-for-bit (gate G1).
DIAL 2 -- gross {0.75 (live), 1.00}.

REPORTED, NEVER SELECTED ON: book {CAP2 (cap 0.02), CAND (cap INF)}, panels {U56, B136},
4 cost rungs (0 / 10 / 25 / 50 bps), weekly cadence, band 0.03, t+1 execution, sweep SHY.
7 x 2 x 2 x 2 = 56 books, every one published at every rung = 224 rows.
SMALL is NOT priced and the reason is stated rather than buried: ideas 2318 / 2322 / 2326 /
2343 each published SMALL's 4b pass count at 0 of 40-120, so there is no pass there for a
turnover device to keep.

BOTH KEEP PATHS on every row: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse)
and 4b (Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x
SPY's).  RULE 8: (lam, gross) chosen on warm-up..2016-12-31 ONLY by two pre-stated IS-only
choosers (C_ISSHARPE, C_ISCALMAR), then 2017-2026 read ONCE.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_partial-adjustment-trade-fraction_B.py
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

DATE, SLUG, LANE = "2026-09-23", "partial-adjustment-trade-fraction", "B"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, CADENCE, WARMUP = 0.03, "W", 260
LAMS = [1.00, 0.85, 0.70, 0.55, 0.40, 0.25, 0.10]
GROSSES = [0.75, 1.00]
BOOKS = {"CAP2": 0.020, "CAND": "INF"}          # cap value; CAND = idea 2300's RG100 + phi
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


# ---------------------------------------------------------------- the target book
def cap_weights(px, invest, cap, gross):
    """idea 2322's CAP2 / idea 2300's CAND: w_i = min(gross / N_in, cap) on names INSIDE the
    200d +/- BAND; idle NAV swept to SHY (phi = 1.00).  cap='INF' is the uncapped candidate."""
    q = px[invest]
    pr = q.notna()
    inb = band_state(q, BAND) & pr
    nin = inb.sum(axis=1).replace(0, np.nan)
    per = gross / nin
    c = pd.Series(np.inf if cap == "INF" else float(cap), index=q.index)
    per = pd.concat([per, c], axis=1).min(axis=1)
    w = inb.astype(float).mul(per.fillna(0.0), axis=0)
    w = w.reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return w


# ---------------------------------------------------------------- the damped backtester
def run_book(prices, weights, lam=1.0, freq=CADENCE, sweep=SWEEP):
    """engine.backtest with a PARTIAL-ADJUSTMENT (trade-fraction) damper on the risk names.

    At a rebalance every risk name moves a fraction lam of the way from its drifted weight to
    its target; SHY is then set to 1 - sum(risk weights), which is exactly its own target when
    lam = 1 -- so lam = 1 is bit-identical to engine.backtest (gate G1).  Zero-cost returns and
    turnover are kept separately so every cost rung is priced from one pass.  The un-invested
    residual drifts at 0% (engine convention).
    """
    cols = list(prices.columns)
    si = cols.index(sweep)
    risk = np.ones(len(cols), dtype=bool); risk[si] = False
    rets = prices.pct_change().fillna(0.0)
    w_target = weights.reindex(prices.index).fillna(0.0).shift(1)
    key = prices.index.to_period(freq)
    s = pd.Series(key, index=prices.index)
    mask = (s != s.shift(-1)).shift(1, fill_value=False).values
    shy_live = prices[sweep].notna().shift(1, fill_value=False).values

    n = len(prices.index)
    held = np.zeros((n, len(cols)))
    stub = np.zeros(n)                  # NAV held in names whose TARGET is 0 today (any day)
    stub_rb = np.full(n, np.nan)        # ... measured POST-TRADE, on rebalance days only
    cur = np.zeros(len(cols))
    turnover = np.zeros(n); gross_s = np.zeros(n); lev = np.zeros(n)
    # NaN targets (row 0, where engine.backtest's own shift(1) leaves a NaN row) are read as
    # ZERO, i.e. "hold nothing yet".  A partial adjustment is RECURSIVE -- unlike
    # engine.backtest's full reset, a NaN target would poison `cur` for the whole path -- so the
    # NaN must be resolved here rather than absorbed.  The affected rows are the first two of
    # the raw panel, 260 rows before the reported window opens; G1 compares the two paths with
    # pandas' skipna max, exactly as idea 2328's damped replica did.
    wt = np.nan_to_num(w_target.values, nan=0.0); rv = rets.values
    for i in range(n):
        if mask[i] or i == 0:
            tgt = wt[i]
            new = cur.copy()
            new[risk] = cur[risk] + lam * (tgt[risk] - cur[risk])
            srisk = new[risk].sum()
            if srisk > 1.0:                       # never lever: scale the risk sleeve back
                lev[i] = srisk
                new[risk] *= 1.0 / srisk
                srisk = 1.0
            new[si] = max(0.0, 1.0 - srisk) if shy_live[i] else 0.0
            turnover[i] = np.abs(new - cur).sum()
            cur = new
            stub_rb[i] = cur[risk & (tgt <= 1e-15)].sum()
        held[i] = cur
        z = risk & (wt[i] <= 1e-15)               # target-zero risk names still held
        stub[i] = cur[z].sum()
        gross_s[i] = cur.sum()
        growth = cur * (1 + rv[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    return dict(r0=pd.Series((held * rv).sum(axis=1), index=prices.index),
                turnover=pd.Series(turnover, index=prices.index),
                gross=pd.Series(gross_s, index=prices.index),
                stub=pd.Series(stub, index=prices.index),
                stub_rb=pd.Series(stub_rb, index=prices.index),
                held=pd.DataFrame(held, index=prices.index, columns=cols),
                lev_events=int((lev > 1.0).sum()))


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
    say("=== idea 2391 (lane B) — does PARTIAL-ADJUSTMENT TRADE-FRACTION DAMPING cut the CAPPED candidate's turnover? ===")
    say(f"    {DATE}  lane {LANE}   band {BAND}  cadence {CADENCE}  t+1  rungs {RUNGS} bps  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 trade fraction lam {LAMS}   DIAL 2 gross {GROSSES}")
    say(f"    REPORTED not selected: book {list(BOOKS)}  panels U56/B136  rungs {RUNGS}")
    gate("G8 exactly two tuned parameters", "trade fraction lam, gross", "2", True)

    panels = {}
    px_u = load_universe()
    px_b = load_universe(broad=True)
    for nm, px in (("U56", px_u), ("B136", px_b)):
        invest = list(px.columns)
        panels[nm] = (px, invest)
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y, {len(invest)} columns, {len(px)} rows", ">= 10y", yrs >= 10)
        win = px.index[WARMUP:]
        dead = [c for c in px.columns if px[c].loc[win].notna().sum() == 0]
        publish(f"G9 all-NaN columns in {nm} (idea 2332's MMC defect, carried forward)",
                f"{len(dead)} dead: {dead} -> {len(invest) - len(dead)} priced names")
        gate(f"G6 sweep {SWEEP} priced on every in-window row ({nm})",
             f"non-null {int(px[SWEEP].loc[win].notna().sum())} of {len(win)}", "all",
             bool(px[SWEEP].loc[win].notna().all()))

    # ---- G1: at lam = 1 the damped replica IS engine.backtest
    for bk, cap in BOOKS.items():
        w1 = cap_weights(px_u, panels["U56"][1], cap, 0.75)
        r_eng = backtest(px_u, w1, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
        d1 = float((r_eng - priced(run_book(px_u, w1, 1.0), HEADLINE_RUNG)).abs().max())
        gate(f"G1 lam=1 replica == engine.backtest ({bk}, U56, g=0.75)", f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    # ---- G7: NO LOOKAHEAD.  Truncating the price panel must not move any earlier held weight.
    cut = px_u.index[int(len(px_u) * 0.70)]
    q = px_u.loc[:cut]
    full = run_book(px_u, cap_weights(px_u, panels["U56"][1], 0.020, 0.75), 0.55)["held"].loc[:cut]
    trunc = run_book(q, cap_weights(q, list(q.columns), 0.020, 0.75), 0.55)["held"]
    d7 = float((full - trunc.reindex_like(full)).abs().max().max())
    gate("G7 no lookahead (panel truncated at 70%, lam=0.55, CAP2/U56)", f"max|dw| {d7:.3e}", "< 1e-12", d7 < 1e-12)

    # ---------------------------------------------------------------- the grid
    rows, tr_rows = [], []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        yrs = len(win) / 252
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_r = priced(run_book(px, rules_v2_weights(px[invest], band=BAND, gross=0.75)
                                 .reindex(columns=px.columns).fillna(0.0), 1.0), HEADLINE_RUNG).loc[win]
        base_t = run_book(px, rules_v2_weights(px[invest], band=BAND, gross=0.75)
                          .reindex(columns=px.columns).fillna(0.0), 1.0)["turnover"].loc[win].sum() / yrs
        say(f"\n--- panel {pname}  ({len(invest)} columns)  SPY {cagr(spy):.2%} / {sharpe(spy):.4f} / {maxdd(spy):.2%}"
            f"   live RULES v2 {cagr(base_r):.2%} / {sharpe(base_r):.4f} / {maxdd(base_r):.2%}  turnover {base_t:.2f}x")
        publish(f"G10 live RULES v2 turnover on {pname}, MEASURED here on the same tape, same weekly"
                f" cadence and same sum|dw| convention as every book in this run"
                f" (the record quotes 1.77x/yr for the live book from an EARLIER convention; this run"
                f" does NOT reproduce that number and reports its own instead)", f"{base_t:.4f}x/yr")
        for bk, cap in BOOKS.items():
            for gross in GROSSES:
                wt = cap_weights(px, invest, cap, gross)
                ref_state = None
                for lam in LAMS:
                    res = run_book(px, wt, lam)
                    inw = res["held"].drop(columns=[SWEEP]).loc[win]
                    state = (inw.values > 1e-12)
                    if lam == 1.00:
                        ref_state = state
                    fid = float((state == ref_state).mean())
                    pos = inw.values[inw.values > 1e-12]
                    risk_nav = inw.values.sum(axis=1)
                    stub_share = float((res["stub"].loc[win].values / np.where(risk_nav > 0, risk_nav, np.nan)).mean())
                    tr_rows.append(dict(panel=pname, book=bk, gross=gross, lam=lam,
                                        turnover_yr=float(res["turnover"].loc[win].sum() / yrs),
                                        base_turnover_yr=base_t,
                                        heldset_fidelity=fid,
                                        mean_names_in=float(state.sum(axis=1).mean()),
                                        stub_nav=float(res["stub"].loc[win].mean()),
                                        stub_rb_nav=float(res["stub_rb"].loc[win].mean(skipna=True)),
                                        stub_share_of_risk=stub_share,
                                        max_name_w=float(pos.max()) if len(pos) else 0.0,
                                        med_name_w=float(np.median(pos)) if len(pos) else 0.0,
                                        p99_name_w=float(np.quantile(pos, 0.99)) if len(pos) else 0.0,
                                        mean_gross=float(res["gross"].loc[win].mean()),
                                        mean_sweep_w=float(res["held"][SWEEP].loc[win].mean()),
                                        max_row_sum=float(res["gross"].max()),
                                        lev_events=res["lev_events"]))
                    for rung in RUNGS:
                        r = priced(res, rung).loc[win]
                        r_oos = r.loc[OOS_START:]
                        h1, h2 = halves(r)
                        rows.append(dict(panel=pname, book=bk, gross=gross, lam=lam, cost_bps=rung,
                                         CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                         H1=h1, H2=h2,
                                         IS_Sharpe=sharpe(r.loc[:IS_END]), IS_Calmar=calmar(r.loc[:IS_END]),
                                         OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                         **legs(r, base_r, spy, r_oos, spy_oos)))
        say(f"    ... {pname} done ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(rows); tf = pd.DataFrame(tr_rows)
    df.to_csv(f"{OUT}.grid.csv", index=False); tf.to_csv(f"{OUT}.turnover.csv", index=False)

    # ---- G2 / G3: external reproduction of the two committed headlines at lam = 1
    h = df[(df.panel == "U56") & (df.book == "CAP2") & (df.gross == 0.75) & (df.lam == 1.00)
           & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    t2 = tf[(tf.panel == "U56") & (tf.book == "CAP2") & (tf.gross == 0.75) & (tf.lam == 1.00)].iloc[0]
    d2 = max(abs(h.CAGR - 0.1162), abs(h.Sharpe - 1.2687) / 10, abs(h.MaxDD + 0.1481),
             abs(h.OOS_CAGR - 0.1277), abs(h.OOS_Sharpe - 1.3318) / 10)
    gate("G2 reproduces idea 2336's committed CAP2 U56 headline (11.62%/1.2687/-14.81%, OOS 12.77%/1.3318)",
         f"read {h.CAGR:.2%} / {h.Sharpe:.4f} / {h.MaxDD:.2%}, OOS {h.OOS_CAGR:.2%} / {h.OOS_Sharpe:.4f},"
         f" turnover {t2.turnover_yr:.2f}x (committed 3.51x) -> max|d| {d2:.2e}", "< 1e-3", d2 < 1e-3)
    h3 = df[(df.panel == "U56") & (df.book == "CAND") & (df.gross == 0.75) & (df.lam == 1.00)
            & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    d3 = max(abs(h3.CAGR - 0.125950), abs(h3.Sharpe - 1.1934) / 10, abs(h3.MaxDD + 0.173923),
             abs(h3.OOS_CAGR - 0.138525), abs(h3.OOS_Sharpe - 1.2397) / 10)
    gate("G3 reproduces idea 2300/2332's committed CAND U56 headline (12.5950%/1.1934/-17.3923%, OOS 13.8525%/1.2397)",
         f"read {h3.CAGR:.4%} / {h3.Sharpe:.4f} / {h3.MaxDD:.4%}, OOS {h3.OOS_CAGR:.4%} / {h3.OOS_Sharpe:.4f}"
         f" -> max|d| {d3:.2e}", "< 1e-3", d3 < 1e-3)
    gate("G4 no leverage anywhere (56 books)", f"max row gross {tf.max_row_sum.max():.9f};"
         f" risk-sleeve rescale events {int(tf.lev_events.sum())}", "<= 1+1e-12", tf.max_row_sum.max() <= 1 + 1e-12)

    # ---- G5: the dial BITES on turnover
    bites, mono = [], []
    for (p, b, g), grp in tf.groupby(["panel", "book", "gross"]):
        v = grp.sort_values("lam", ascending=False).turnover_yr.values   # lam 1.00 -> 0.10
        bites.append(v[-1] < v[0] - 1e-9)
        mono.append(bool(np.all(np.diff(v) <= 1e-9)))
    gate("G5 the lam dial BITES (turnover at lam=0.10 strictly below lam=1.00)",
         f"{sum(bites)} of {len(bites)} (panel, book, gross) cells", f"{len(bites)} of {len(bites)}", all(bites))
    publish("G5b turnover MONOTONE non-increasing as lam falls", f"{sum(mono)} of {len(mono)} cells")

    # ---- G11: lam = 1 has NO stub POST-TRADE by construction.  The DAILY stub is non-zero even
    # at lam = 1 because a name gated OUT mid-week is not sold until the next rebalance -- that is
    # WEEKLY CADENCE, not damping, and the two must not be conflated.  The gate is therefore on the
    # post-trade measure and the cadence floor is published beside it.
    z = tf[tf.lam == 1.00].stub_rb_nav.abs().max()
    gate("G11 lam=1.00 carries zero POST-TRADE stub (a gated-OUT name is sold in full at the rebalance)",
         f"max post-trade stub NAV {z:.3e}", "< 1e-12", z < 1e-12)
    publish("G11b the DAILY stub floor at lam=1.00 is pure weekly-cadence drift, not damping",
            "  ".join(f"{r.panel}/{r.book} {r.stub_nav:.4%}"
                      for _, r in tf[(tf.lam == 1.00) & (tf.gross == 0.75)].iterrows()))

    # ---------------------------------------------------------------- A. full grid
    say("\n=== A. THE FULL GRID AT THE HEADLINE RUNG (10 bps) — every point, nothing dropped ===")
    for pname in panels:
        for bk in BOOKS:
            say(f"\n  {pname} / {bk}")
            say("   lam    gross |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh  OOS DD | 4a 4b |"
                " legs H1/H2/OOS/DD/CAGR | turn/yr  fidelity  stubNAV   maxw")
            for gross in GROSSES:
                for lam in LAMS:
                    r = df[(df.panel == pname) & (df.book == bk) & (df.gross == gross) & (df.lam == lam)
                           & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                    c = tf[(tf.panel == pname) & (tf.book == bk) & (tf.gross == gross) & (tf.lam == lam)].iloc[0]
                    lg = "".join("1" if r[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                    say(f"  {lam:.2f}   {gross:.2f}  | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%} |"
                        f" {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} {r.OOS_MaxDD:7.2%} |"
                        f" {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg:22s} |"
                        f" {c.turnover_yr:7.2f} {c.heldset_fidelity:9.4%} {c.stub_nav:8.4%} {c.max_name_w:6.2%}")

    # ---------------------------------------------------------------- B. keep counts
    say(f"\n=== B. KEEP COUNTS OVER ALL {len(df)} PUBLISHED ROWS (7 lam x 2 gross x 2 books x 2 panels x 4 rungs) ===")
    say(f"  4b passes: {int(df.pass4b.sum())} of {len(df)}      4a passes: {int(df.pass4a.sum())} of {len(df)}")
    for rung in RUNGS:
        dd = df[df.cost_bps == rung]
        say(f"   {rung:5.1f} bps:  4b {int(dd.pass4b.sum()):3d}/{len(dd)}   4a {int(dd.pass4a.sum()):3d}/{len(dd)}"
            f"   binding leg on 4b FAILs: " +
            "  ".join(f"{k} {int((~dd[k][~dd.pass4b]).sum())}" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    say("\n  4b pass counts by (book, panel, lam) over the 4 rungs x 2 gross:")
    for bk in BOOKS:
        for pname in panels:
            line = "  ".join(f"lam{lam:.2f} {int(df[(df.book == bk) & (df.panel == pname) & (df.lam == lam)].pass4b.sum()):2d}/8"
                             for lam in LAMS)
            say(f"    {bk:5s} {pname:5s}  {line}")
    say("\n  4b pass counts by (book, panel, lam) at 25 and 50 bps ONLY — the rungs the family fails on:")
    for bk in BOOKS:
        for pname in panels:
            hi = df[(df.book == bk) & (df.panel == pname) & (df.cost_bps >= 25.0)]
            line = "  ".join(f"lam{lam:.2f} {int(hi[hi.lam == lam].pass4b.sum()):2d}/4" for lam in LAMS)
            say(f"    {bk:5s} {pname:5s}  {line}")

    # ---------------------------------------------------------------- C. what the damper buys
    say("\n=== C. WHAT THE DAMPER BUYS: each lam minus lam=1.00, same (panel, book, gross, rung) ===")
    for pname in panels:
        for bk in BOOKS:
            say(f"\n  {pname} / {bk} / gross 0.75   (live RULES v2 turnover"
                f" {tf[(tf.panel == pname)].base_turnover_yr.iloc[0]:.2f}x/yr)")
            say("   lam      turn/yr  dturn%  | dCAGR @0bps  @10bps  @25bps  @50bps | dSharpe@10  dOOS_Sh@10  dMaxDD@10  fidelity")
            ref = {rg: df[(df.panel == pname) & (df.book == bk) & (df.gross == 0.75) & (df.lam == 1.00)
                          & (df.cost_bps == rg)].iloc[0] for rg in RUNGS}
            t1r = tf[(tf.panel == pname) & (tf.book == bk) & (tf.gross == 0.75) & (tf.lam == 1.00)].iloc[0]
            for lam in LAMS:
                c = tf[(tf.panel == pname) & (tf.book == bk) & (tf.gross == 0.75) & (tf.lam == lam)].iloc[0]
                r = {rg: df[(df.panel == pname) & (df.book == bk) & (df.gross == 0.75) & (df.lam == lam)
                            & (df.cost_bps == rg)].iloc[0] for rg in RUNGS}
                say(f"  {lam:.2f} {c.turnover_yr:10.2f} {c.turnover_yr / t1r.turnover_yr - 1:+7.1%}  |" +
                    "".join(f" {r[rg].CAGR - ref[rg].CAGR:+11.2%}" for rg in RUNGS) +
                    f" | {r[10.0].Sharpe - ref[10.0].Sharpe:+10.4f} {r[10.0].OOS_Sharpe - ref[10.0].OOS_Sharpe:+11.4f}"
                    f" {r[10.0].MaxDD - ref[10.0].MaxDD:+10.2%} {c.heldset_fidelity:9.4%}")

    # ---- the price of a turn, and whether the live book's turnover is reachable at all
    say("\n  THE PRICE OF A TURN (gross 0.75, 10 bps): dCAGR per turn/yr removed, and the lam that")
    say("  first brings turnover at or below the LIVE book's own rate:")
    for pname in panels:
        for bk in BOOKS:
            t1r = tf[(tf.panel == pname) & (tf.book == bk) & (tf.gross == 0.75) & (tf.lam == 1.00)].iloc[0]
            ref = df[(df.panel == pname) & (df.book == bk) & (df.gross == 0.75) & (df.lam == 1.00)
                     & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
            reach = None
            for lam in LAMS:
                c = tf[(tf.panel == pname) & (tf.book == bk) & (tf.gross == 0.75) & (tf.lam == lam)].iloc[0]
                if reach is None and c.turnover_yr <= t1r.base_turnover_yr:
                    r = df[(df.panel == pname) & (df.book == bk) & (df.gross == 0.75) & (df.lam == lam)
                           & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                    reach = (lam, c.turnover_yr, r.CAGR - ref.CAGR, r.Sharpe - ref.Sharpe, bool(r.pass4b))
            lo = tf[(tf.panel == pname) & (tf.book == bk) & (tf.gross == 0.75) & (tf.lam == LAMS[-1])].iloc[0]
            rlo = df[(df.panel == pname) & (df.book == bk) & (df.gross == 0.75) & (df.lam == LAMS[-1])
                     & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
            slope = (rlo.CAGR - ref.CAGR) / (lo.turnover_yr - t1r.turnover_yr) if lo.turnover_yr != t1r.turnover_yr else np.nan
            say(f"    {pname:5s} {bk:5s}  lam1 {t1r.turnover_yr:5.2f}x -> lam{LAMS[-1]:.2f} {lo.turnover_yr:5.2f}x |"
                f" dCAGR {rlo.CAGR - ref.CAGR:+.2%}  => {-slope:+.4%} of CAGR per turn/yr removed |"
                f" live-book rate {t1r.base_turnover_yr:.2f}x reached at "
                + (f"lam {reach[0]:.2f} ({reach[1]:.2f}x, dCAGR {reach[2]:+.2%}, dSharpe {reach[3]:+.4f},"
                   f" 4b {'PASS' if reach[4] else 'FAIL'})" if reach else "NO lam on this ladder"))

    # ---------------------------------------------------------------- D. rule 8
    say("\n=== D. RULE 8 — (lam, gross) chosen on <= 2016-12-31 ONLY, 2017-2026 read once ===")
    wf = []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_r = priced(run_book(px, rules_v2_weights(px[invest], band=BAND, gross=0.75)
                                 .reindex(columns=px.columns).fillna(0.0), 1.0), HEADLINE_RUNG).loc[win]
        b_oos = base_r.loc[OOS_START:]
        for bk in BOOKS:
            for rung in RUNGS:
                dd = df[(df.panel == pname) & (df.book == bk) & (df.cost_bps == rung)]
                und = dd[(dd.lam == 1.00) & (dd.gross == 0.75)].iloc[0]
                for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                    pick = dd.loc[dd[col].idxmax()]
                    wf.append(dict(panel=pname, book=bk, cost_bps=rung, chooser=chooser,
                                   pick_lam=pick.lam, pick_gross=pick.gross,
                                   OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                                   pick_pass4b=bool(pick.pass4b), pick_is_undamped=bool(pick.lam == 1.00),
                                   und_OOS_CAGR=und.OOS_CAGR, und_OOS_Sharpe=und.OOS_Sharpe,
                                   beats_undamped_OOS_Sharpe=bool(pick.OOS_Sharpe > und.OOS_Sharpe),
                                   base_OOS_CAGR=cagr(b_oos), base_OOS_Sharpe=sharpe(b_oos), base_OOS_MaxDD=maxdd(b_oos),
                                   spy_OOS_CAGR=cagr(spy_oos), spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_MaxDD=maxdd(spy_oos),
                                   beats_SPY_OOS_Sharpe=bool(pick.OOS_Sharpe > sharpe(spy_oos)),
                                   beats_LIVE_OOS_Sharpe=bool(pick.OOS_Sharpe > sharpe(b_oos))))
                    say(f"  {pname:5s} {bk:5s} {rung:5.1f}bps {chooser:11s} -> lam {pick.lam:.2f} g {pick.gross:.2f} |"
                        f" OOS {pick.OOS_CAGR:6.2%} / {pick.OOS_Sharpe:.4f} / {pick.OOS_MaxDD:7.2%} |"
                        f" undamped lam1 g0.75 OOS {und.OOS_CAGR:6.2%} / {und.OOS_Sharpe:.4f} |"
                        f" live v2 OOS {cagr(b_oos):6.2%} / {sharpe(b_oos):.4f} | SPY OOS {cagr(spy_oos):6.2%} /"
                        f" {sharpe(spy_oos):.4f} | full 4b {'Y' if pick.pass4b else '.'}")
    wfd = pd.DataFrame(wf)
    wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"\n  rule-8 picks landing on lam = 1.00 (the undamped book): {int(wfd.pick_is_undamped.sum())} of {len(wfd)}")
    say(f"  picks beating the UNDAMPED book's OOS Sharpe: {int(wfd.beats_undamped_OOS_Sharpe.sum())} of {len(wfd)}")
    say(f"  picks beating SPY's OOS Sharpe:               {int(wfd.beats_SPY_OOS_Sharpe.sum())} of {len(wfd)}")
    say(f"  picks beating LIVE RULES v2's OOS Sharpe:     {int(wfd.beats_LIVE_OOS_Sharpe.sum())} of {len(wfd)}")
    say(f"  picks whose full-sample row also passes 4b:   {int(wfd.pick_pass4b.sum())} of {len(wfd)}")
    say("  pick distribution over lam: " + "  ".join(f"lam{lam:.2f} {int((wfd.pick_lam == lam).sum())}" for lam in LAMS))
    agree = []
    for (bk, rung, ch), g in wfd.groupby(["book", "cost_bps", "chooser"]):
        agree.append(g.pick_lam.nunique() == 1 and g.pick_gross.nunique() == 1)
    say(f"  the two panels pick the SAME (lam, gross): {sum(agree)} of {len(agree)} (book, rung, chooser) cells")

    # ---------------------------------------------------------------- E. the idea's own cost
    say("\n=== E. THE IDEA'S OWN COST — the STUB a fractional sale leaves behind (gross 0.75) ===")
    say("  (stubNAV = mean share of NAV held in names whose TARGET is 0 that day; fidelity vs the lam=1 held set)")
    for label, col, fmt in (("POST-TRADE stub NAV (the unfinished sale; 0 at lam=1 by construction)", "stub_rb_nav", "{:8.4%}"),
                            ("daily stub NAV (post-trade stub PLUS the weekly-cadence floor)", "stub_nav", "{:8.4%}"),
                            ("stub as share of the RISK sleeve", "stub_share_of_risk", "{:8.4%}"),
                            ("held-set fidelity vs lam=1", "heldset_fidelity", "{:8.4%}"),
                            ("mean names held IN", "mean_names_in", "{:8.2f}"),
                            ("max per-name weight (CAP2 exists to hold this down)", "max_name_w", "{:8.2%}"),
                            ("99th pct per-name weight", "p99_name_w", "{:8.2%}"),
                            ("mean book gross", "mean_gross", "{:8.4f}"),
                            ("mean SHY sweep weight", "mean_sweep_w", "{:8.4f}")):
        say(f"\n  {label}:")
        say("  panel book    " + "".join(f"  lam{lam:.2f}" for lam in LAMS))
        for pname in panels:
            for bk in BOOKS:
                row = tf[(tf.panel == pname) & (tf.book == bk) & (tf.gross == 0.75)].set_index("lam")
                say(f"  {pname:5s} {bk:5s}  " + "".join(" " + fmt.format(row.loc[lam][col]) for lam in LAMS))

    # ---------------------------------------------------------------- F. the decisive read
    say("\n=== F. THE DECISIVE READ — JOINT 4b ON BOTH PANELS AT THE LIVE GROSS (0.75), by lam and rung ===")
    say("  (a device that keeps the candidate's pass must keep it on BOTH panels at the SAME lam and rung)")
    for bk in BOOKS:
        say(f"\n  {bk}:  lam  |" + "".join(f"  {rg:>4.0f}bps " for rg in RUNGS)
            + " | turn/yr U56  B136 | dCAGR@10 U56   B136 | dSharpe@10 U56    B136")
        for lam in LAMS:
            cells, tt, dc, ds = [], [], [], []
            for rg in RUNGS:
                ok = True
                for pname in panels:
                    r = df[(df.panel == pname) & (df.book == bk) & (df.gross == 0.75) & (df.lam == lam)
                           & (df.cost_bps == rg)].iloc[0]
                    ok = ok and bool(r.pass4b)
                cells.append("BOTH" if ok else " .  ")
            for pname in panels:
                c = tf[(tf.panel == pname) & (tf.book == bk) & (tf.gross == 0.75) & (tf.lam == lam)].iloc[0]
                r = df[(df.panel == pname) & (df.book == bk) & (df.gross == 0.75) & (df.lam == lam)
                       & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                ref = df[(df.panel == pname) & (df.book == bk) & (df.gross == 0.75) & (df.lam == 1.00)
                         & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                tt.append(c.turnover_yr); dc.append(r.CAGR - ref.CAGR); ds.append(r.Sharpe - ref.Sharpe)
            say(f"       {lam:.2f} |" + "".join(f"  {c}   " for c in cells)
                + f" |  {tt[0]:5.2f} {tt[1]:5.2f} |   {dc[0]:+7.2%} {dc[1]:+7.2%} |    {ds[0]:+8.4f} {ds[1]:+8.4f}")
    say("\n  The turnover the record set out to cut: CAP2 lam=1.00 runs at"
        f" {tf[(tf.panel == 'U56') & (tf.book == 'CAP2') & (tf.gross == 0.75) & (tf.lam == 1.00)].iloc[0].turnover_yr:.2f}x (U56) /"
        f" {tf[(tf.panel == 'B136') & (tf.book == 'CAP2') & (tf.gross == 0.75) & (tf.lam == 1.00)].iloc[0].turnover_yr:.2f}x (B136).")

    gdf = pd.DataFrame(GATES)
    gdf.to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n=== GATES: {int(gdf.pass_.sum())} of {len(gdf)} pass ===")
    for _, g in gdf[~gdf.pass_].iterrows():
        say(f"    FAILED: {g.gate} = {g.value} (target {g.target})")
    say(f"\nwrote {OUT}.grid.csv / .turnover.csv / .walkforward.csv / .gates.csv   ({time.time() - t0:.0f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""idea 2404 (lane B, 2026-09-23) — does the DAMPER's MaxDD/CAGR change come from LAG or from
UNPAID COST?

THE OBJECT.  Idea 2300 filed `RG100 + phi = 1.00` (`CAND`: every name INSIDE the 200d +/-3%
band held at `gross / N_in` of NAV, idle NAV swept to SHY) as the record's standing 4b
KEEP-candidate; idea 2322 added a 2.0% per-name cap (`CAP2`).  Idea 2391 (lane B run 39) then
filed the record's first PARTIAL-ADJUSTMENT damper at `lam = 0.40`: at each weekly rebalance
move EVERY risk name a fraction `lam` of the way to target, SHY absorbing the residual.  It
measured, at 10 bps, CAGR **+0.17 pp (U56) / +0.22 pp (B136)** and MaxDD **2.11 pp / 2.43 pp
WORSE**, and attributed the CAGR to "the un-traded distance is un-charged".

THAT ATTRIBUTION WAS NEVER TESTED.  A damped book differs from its undamped anchor in TWO
ways at once:
  (i)  COST   — it trades less, so it pays a smaller bill;
  (ii) LAG    — it HOLDS A DIFFERENT PORTFOLIO (it re-enters slowly after a band flip and
                exits slowly into a fall), so its gross return path is different too.
Run 39 read only the sum.

THE TEST — AN EXACT ADDITIVE IDENTITY, NOT A REGRESSION.  This record prices every book as
`priced(rung) = r0 - turnover * rung / 1e4`, so the two channels separate ALGEBRAICALLY.  For
each (panel, book, gross, lam) four books are priced from ONE pair of passes:

    U   (anchor)   r0_U - to_U * rung/1e4      undamped holdings, undamped bill
    LAG            r0_D - to_U * rung/1e4      DAMPED holdings,   undamped bill   <- lag alone
    COST           r0_U - to_D * rung/1e4      undamped holdings, DAMPED bill     <- cost alone
    D   (run 39)   r0_D - to_D * rung/1e4      both

`(D - U) == (LAG - U) + (COST - U)` holds EXACTLY on the return series (gate G14, asserted at
1e-18), so the split is a decomposition rather than an estimate.  CAGR / Sharpe / MaxDD are
NON-LINEAR in the return path, so their three deltas are published WITH the interaction
residual `total - lag - cost` rather than being asserted to add up.  At rung 0 the cost channel
is identically zero by construction (`LAG == D`, `COST == U`, gate G15) — so whatever MaxDD
difference survives at 0 bps is PURE LAG, which is exactly what the idea asked for.

DIAL 1 -- lam   {1.00, 0.85, 0.70, 0.55, 0.40, 0.25, 0.10}
DIAL 2 -- gross {0.50, 0.75, 1.00}      (0.75 is LIVE and carries every headline verdict)
and no others.  At lam = 1.00 the damper is the identity and all four books coincide with
`engine.backtest` bit-for-bit (gate G1).

REPORTED, NEVER SELECTED ON: books {CAP2 (cap 0.02), CAND (cap INF)}; panels {U56, B136};
4 cost rungs (0 / 10 / 25 / 50 bps); weekly cadence; band 0.03; t+1 execution; sweep SHY.
7 lam x 3 gross x 2 books x 2 panels = 84 damped passes -> 4 variants x 4 rungs = 1344 rows,
every one published.  SMALL is NOT priced and the reason is stated rather than buried: ideas
2318 / 2322 / 2326 / 2343 each published SMALL's 4b pass count at 0 of 40-120, so there is no
pass there for this decomposition to explain.

BOTH KEEP PATHS on every row: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse)
and 4b (Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x
SPY's).  The live RULES v2 baseline is priced at THE SAME RUNG as the row it judges (stated
explicitly: idea 2391/2412 held the baseline at 10 bps for every rung; charging both sides the
same tape is the stricter and the more defensible convention, and the 10 bps column is
identical under both).  RULE 8: (lam, gross) chosen on warm-up..2016-12-31 ONLY by two
pre-stated IS-only choosers (C_ISSHARPE, C_ISCALMAR), then 2017-2026 read ONCE.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_damper-lag-vs-unpaid-cost_B.py
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

DATE, SLUG, LANE = "2026-09-23", "damper-lag-vs-unpaid-cost", "B"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, CADENCE, WARMUP = 0.03, "W", 260
LAMS = [1.00, 0.85, 0.70, 0.55, 0.40, 0.25, 0.10]
GROSSES = [0.50, 0.75, 1.00]
LIVE_GROSS = 0.75
BOOKS = {"CAP2": 0.020, "CAND": "INF"}
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG = 10.0
VARIANTS = ["U", "LAG", "COST", "D"]
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


# ---------------------------------------------------------------- idea 2391's damper
def run_book(prices, weights, lam=1.0, freq=CADENCE, sweep=SWEEP):
    """engine.backtest with idea 2391's SYMMETRIC partial-adjustment damper on the risk names:
    at a rebalance every risk name moves a fraction `lam` of the distance to its target and SHY
    is set to 1 - sum(risk weights), which is exactly its own target when lam = 1 -- so lam=1.00
    is bit-identical to engine.backtest (gate G1).  The ZERO-COST return path `r0` and the
    turnover path are returned SEPARATELY, which is what makes the cost/lag split exact.

    NaN targets (the first rows, where engine.backtest's own shift(1) leaves a NaN row) are read
    as ZERO.  A partial adjustment is RECURSIVE -- unlike engine.backtest's full reset a NaN
    target would poison `cur` for the whole path -- so the NaN is resolved here rather than
    absorbed.  The affected rows are the first two of the raw panel, 260 rows before the
    reported window opens.
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
    stub = np.zeros(n)
    stub_rb = np.full(n, np.nan)
    buys = np.zeros(n); sells = np.zeros(n)
    cur = np.zeros(len(cols))
    turnover = np.zeros(n); gross_s = np.zeros(n); lev = np.zeros(n)
    wt = np.nan_to_num(w_target.values, nan=0.0); rv = rets.values
    for i in range(n):
        if mask[i] or i == 0:
            tgt = wt[i]
            new = cur.copy()
            new[risk] = cur[risk] + lam * (tgt - cur)[risk]
            srisk = new[risk].sum()
            if srisk > 1.0:                       # never lever: scale the risk sleeve back
                lev[i] = srisk
                new[risk] *= 1.0 / srisk
                srisk = 1.0
            new[si] = max(0.0, 1.0 - srisk) if shy_live[i] else 0.0
            dd = new - cur
            turnover[i] = np.abs(dd).sum()
            buys[i] = dd[risk].clip(min=0.0).sum(); sells[i] = (-dd[risk]).clip(min=0.0).sum()
            cur = new
            stub_rb[i] = cur[risk & (tgt <= 1e-15)].sum()
        held[i] = cur
        stub[i] = cur[risk & (wt[i] <= 1e-15)].sum()
        gross_s[i] = cur.sum()
        growth = cur * (1 + rv[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    return dict(r0=pd.Series((held * rv).sum(axis=1), index=prices.index),
                turnover=pd.Series(turnover, index=prices.index),
                buys=pd.Series(buys, index=prices.index),
                sells=pd.Series(sells, index=prices.index),
                gross=pd.Series(gross_s, index=prices.index),
                stub=pd.Series(stub, index=prices.index),
                stub_rb=pd.Series(stub_rb, index=prices.index),
                held=pd.DataFrame(held, index=prices.index, columns=cols),
                lev_events=int((lev > 1.0).sum()))


def priced(res, bps):
    return res["r0"] - res["turnover"] * bps / 1e4


def variant(rD, rU, which, bps):
    """The four books of the decomposition, from ONE damped pass and ONE undamped pass."""
    r0 = rD["r0"] if which in ("LAG", "D") else rU["r0"]
    to = rD["turnover"] if which in ("COST", "D") else rU["turnover"]
    return r0 - to * bps / 1e4


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
    say("=== idea 2404 (lane B, run 43) — does the DAMPER's MaxDD/CAGR change come from LAG or from UNPAID COST? ===")
    say(f"    {DATE}  lane {LANE}   band {BAND}  cadence {CADENCE}  t+1  rungs {RUNGS} bps  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 lam {LAMS}   DIAL 2 gross {GROSSES}  (live {LIVE_GROSS} carries every verdict)")
    say(f"    REPORTED not selected: book {list(BOOKS)}  panels U56/B136  rungs {RUNGS}  variants {VARIANTS}")
    say("    CONVENTION STATED, NOT BURIED: the live RULES v2 4a baseline is priced at THE SAME RUNG as the")
    say("    row it judges (2391/2412 pinned it at 10 bps); the 10 bps column is identical under both.")
    gate("G8 exactly two tuned parameters", "lam, gross", "2", True)

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

    # ---- G1: at lam = 1 the damper is the identity
    for bk, cap in BOOKS.items():
        w1 = cap_weights(px_u, panels["U56"][1], cap, LIVE_GROSS)
        r_eng = backtest(px_u, w1, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
        d1 = float((r_eng - priced(run_book(px_u, w1, 1.0), HEADLINE_RUNG)).abs().max())
        gate(f"G1 lam=1 replica == engine.backtest ({bk}, U56, g={LIVE_GROSS})", f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    # ---- G7: NO LOOKAHEAD.
    cut = px_u.index[int(len(px_u) * 0.70)]
    q = px_u.loc[:cut]
    full = run_book(px_u, cap_weights(px_u, panels["U56"][1], 0.020, LIVE_GROSS), 0.40)["held"].loc[:cut]
    trunc = run_book(q, cap_weights(q, list(q.columns), 0.020, LIVE_GROSS), 0.40)["held"]
    d7 = float((full - trunc.reindex_like(full)).abs().max().max())
    gate("G7 no lookahead (panel truncated at 70%, lam=0.40, CAP2/U56)", f"max|dw| {d7:.3e}", "< 1e-12", d7 < 1e-12)

    # ---------------------------------------------------------------- the grid
    rows, tr_rows = [], []
    id_err = 0.0; zero_err = 0.0
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        yrs = len(win) / 252
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        bw = rules_v2_weights(px[invest], band=BAND, gross=LIVE_GROSS).reindex(columns=px.columns).fillna(0.0)
        bres = run_book(px, bw, 1.0)
        base_by_rung = {rg: priced(bres, rg).loc[win] for rg in RUNGS}
        base_t = bres["turnover"].loc[win].sum() / yrs
        say(f"\n--- panel {pname}  ({len(invest)} columns)  SPY {cagr(spy):.2%} / {sharpe(spy):.4f} / {maxdd(spy):.2%}"
            f"   live RULES v2 @10bps {cagr(base_by_rung[10.0]):.2%} / {sharpe(base_by_rung[10.0]):.4f}"
            f" / {maxdd(base_by_rung[10.0]):.2%}  turnover {base_t:.2f}x")
        for bk, cap in BOOKS.items():
            for gross in GROSSES:
                wt = cap_weights(px, invest, cap, gross)
                anchor = run_book(px, wt, 1.00)
                to_U = anchor["turnover"].loc[win].sum() / yrs
                for lam in LAMS:
                    res = anchor if lam == 1.00 else run_book(px, wt, lam)
                    inw = res["held"].drop(columns=[SWEEP]).loc[win]
                    state = (inw.values > 1e-12)
                    ref_state = (anchor["held"].drop(columns=[SWEEP]).loc[win].values > 1e-12)
                    pos = inw.values[inw.values > 1e-12]
                    to_D = res["turnover"].loc[win].sum() / yrs
                    tr_rows.append(dict(panel=pname, book=bk, gross=gross, lam=lam,
                                        turnover_yr=to_D, anchor_turnover_yr=to_U,
                                        turnover_saved_yr=to_U - to_D,
                                        buy_yr=float(res["buys"].loc[win].sum() / yrs),
                                        sell_yr=float(res["sells"].loc[win].sum() / yrs),
                                        base_turnover_yr=base_t,
                                        heldset_fidelity=float((state == ref_state).mean()),
                                        mean_names_in=float(state.sum(axis=1).mean()),
                                        stub_nav=float(res["stub"].loc[win].mean()),
                                        stub_rb_nav=float(res["stub_rb"].loc[win].mean(skipna=True)),
                                        max_name_w=float(pos.max()) if len(pos) else 0.0,
                                        mean_gross=float(res["gross"].loc[win].mean()),
                                        mean_sweep_w=float(res["held"][SWEEP].loc[win].mean()),
                                        max_row_sum=float(res["gross"].max()),
                                        lev_events=res["lev_events"],
                                        # the naive "unpaid cost" the record has been quoting, in pp/yr
                                        **{f"rebate_pp_{int(rg)}": (to_U - to_D) * rg / 1e4 * 100 for rg in RUNGS}))
                    for rung in RUNGS:
                        # exact additive identity on the RETURN SERIES
                        rr = {v: variant(res, anchor, v, rung).loc[win] for v in VARIANTS}
                        id_err = max(id_err, float(((rr["D"] - rr["U"])
                                                    - ((rr["LAG"] - rr["U"]) + (rr["COST"] - rr["U"]))).abs().max()))
                        if rung == 0.0:
                            zero_err = max(zero_err, float((rr["LAG"] - rr["D"]).abs().max()),
                                           float((rr["COST"] - rr["U"]).abs().max()))
                        base_r = base_by_rung[rung]
                        for v in VARIANTS:
                            r = rr[v]
                            r_oos = r.loc[OOS_START:]
                            h1, h2 = halves(r)
                            rows.append(dict(panel=pname, book=bk, gross=gross, lam=lam, cost_bps=rung,
                                             variant=v,
                                             CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                             H1=h1, H2=h2,
                                             IS_Sharpe=sharpe(r.loc[:IS_END]), IS_Calmar=calmar(r.loc[:IS_END]),
                                             OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                             **legs(r, base_r, spy, r_oos, spy_oos)))
        say(f"    ... {pname} done ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(rows); tf = pd.DataFrame(tr_rows)
    df.to_csv(f"{OUT}.grid.csv", index=False); tf.to_csv(f"{OUT}.turnover.csv", index=False)

    def pick(d, **kw):
        q = d
        for k, v in kw.items():
            q = q[q[k] == v]
        return q.iloc[0]

    # ---- the decomposition's own gates
    gate("G14 the split is an EXACT identity on returns: (D-U) == (LAG-U) + (COST-U) over every published cell",
         f"max|residual| over {len(df) // 4} (panel,book,gross,lam,rung) cells = {id_err:.3e}", "< 1e-15", id_err < 1e-15)
    gate("G15 at 0 bps the COST channel is identically zero (LAG == D and COST == U)",
         f"max|d| {zero_err:.3e}", "== 0", zero_err == 0.0)

    # ---- G2 / G3 / G3b: external reproduction of three committed headlines
    h = pick(df, panel="U56", book="CAP2", gross=LIVE_GROSS, lam=1.00, cost_bps=HEADLINE_RUNG, variant="D")
    t2 = pick(tf, panel="U56", book="CAP2", gross=LIVE_GROSS, lam=1.00)
    d2 = max(abs(h.CAGR - 0.1162), abs(h.Sharpe - 1.2687) / 10, abs(h.MaxDD + 0.1481),
             abs(h.OOS_CAGR - 0.1277), abs(h.OOS_Sharpe - 1.3318) / 10)
    gate("G2 reproduces idea 2336's committed CAP2 U56 headline (11.62%/1.2687/-14.81%, OOS 12.77%/1.3318)",
         f"read {h.CAGR:.2%} / {h.Sharpe:.4f} / {h.MaxDD:.2%}, OOS {h.OOS_CAGR:.2%} / {h.OOS_Sharpe:.4f},"
         f" turnover {t2.turnover_yr:.2f}x (committed 3.51x) -> max|d| {d2:.2e}", "< 1e-3", d2 < 1e-3)
    h3 = pick(df, panel="U56", book="CAND", gross=LIVE_GROSS, lam=1.00, cost_bps=HEADLINE_RUNG, variant="D")
    d3 = max(abs(h3.CAGR - 0.125950), abs(h3.Sharpe - 1.1934) / 10, abs(h3.MaxDD + 0.173923),
             abs(h3.OOS_CAGR - 0.138525), abs(h3.OOS_Sharpe - 1.2397) / 10)
    gate("G3 reproduces idea 2300/2332's committed CAND U56 headline (12.5950%/1.1934/-17.3923%, OOS 13.8525%/1.2397)",
         f"read {h3.CAGR:.4%} / {h3.Sharpe:.4f} / {h3.MaxDD:.4%}, OOS {h3.OOS_CAGR:.4%} / {h3.OOS_Sharpe:.4f}"
         f" -> max|d| {d3:.2e}", "< 1e-3", d3 < 1e-3)
    h4 = pick(df, panel="U56", book="CAP2", gross=LIVE_GROSS, lam=0.40, cost_bps=HEADLINE_RUNG, variant="D")
    t4 = pick(tf, panel="U56", book="CAP2", gross=LIVE_GROSS, lam=0.40)
    d4 = max(abs(h4.CAGR - 0.1179), abs(h4.Sharpe - 1.2538) / 10, abs(h4.MaxDD + 0.1692),
             abs(h4.OOS_CAGR - 0.1298), abs(h4.OOS_Sharpe - 1.3091) / 10, abs(t4.turnover_yr - 2.34) / 100)
    gate("G3b reproduces idea 2391's committed SYM lam=0.40 headline (11.79%/1.2538/-16.92%, OOS 12.98%/1.3091, 2.34x)",
         f"read {h4.CAGR:.2%} / {h4.Sharpe:.4f} / {h4.MaxDD:.2%}, OOS {h4.OOS_CAGR:.2%} / {h4.OOS_Sharpe:.4f},"
         f" turnover {t4.turnover_yr:.2f}x -> max|d| {d4:.2e}", "< 1e-3", d4 < 1e-3)
    gate("G4 no leverage anywhere", f"max row gross {tf.max_row_sum.max():.9f};"
         f" risk-sleeve rescale events {int(tf.lev_events.sum())}", "<= 1+1e-12", tf.max_row_sum.max() <= 1 + 1e-12)
    bites = []
    for (p, b, g), grp in tf.groupby(["panel", "book", "gross"]):
        v = grp.sort_values("lam", ascending=False).turnover_yr.values
        bites.append(v[-1] < v[0] - 1e-9)
    gate("G5 the lam dial BITES on turnover (lam=0.10 strictly below lam=1.00)",
         f"{sum(bites)} of {len(bites)} (panel, book, gross) ladders", f"{len(bites)} of {len(bites)}", all(bites))
    gate("G16 at lam = 1.00 all four variants coincide (the damper is the identity)",
         f"max spread of CAGR over variants at lam=1 "
         f"{df[df.lam == 1.00].groupby(['panel','book','gross','cost_bps']).CAGR.apply(lambda s: s.max()-s.min()).max():.3e}",
         "< 1e-15",
         float(df[df.lam == 1.00].groupby(["panel", "book", "gross", "cost_bps"]).CAGR
               .apply(lambda s: s.max() - s.min()).max()) < 1e-15)

    # ---------------------------------------------------------------- A. THE SPLIT
    say("\n=== A. THE SPLIT — CAGR, Sharpe and MaxDD of the damped book decomposed into LAG and COST, every rung ===")
    say("    total = D - U ;  lag = LAG - U (damped holdings, UNDAMPED bill) ;  cost = COST - U (undamped holdings, DAMPED bill)")
    say("    interaction = total - lag - cost, non-zero ONLY because CAGR/Sharpe/MaxDD are non-linear in the path.")
    for pname in panels:
        for bk in BOOKS:
            say(f"\n  {pname} / {bk} / gross {LIVE_GROSS}  (LIVE)")
            say("   rung  lam  |   dCAGR: total     lag    cost   inter |  dSharpe: total     lag    cost   inter |"
                "  dMaxDD: total     lag    cost   inter | rebate pp/yr")
            for rung in RUNGS:
                for lam in LAMS:
                    if lam == 1.00:
                        continue
                    g = {v: pick(df, panel=pname, book=bk, gross=LIVE_GROSS, lam=lam, cost_bps=rung, variant=v)
                         for v in VARIANTS}
                    c = pick(tf, panel=pname, book=bk, gross=LIVE_GROSS, lam=lam)
                    out = [f"  {rung:5.1f} {lam:.2f} |"]
                    for k, sc in (("CAGR", 100), ("Sharpe", 1), ("MaxDD", 100)):
                        tot = (g["D"][k] - g["U"][k]) * sc
                        lg = (g["LAG"][k] - g["U"][k]) * sc
                        ct = (g["COST"][k] - g["U"][k]) * sc
                        out.append(f" {tot:+8.4f} {lg:+7.4f} {ct:+7.4f} {tot - lg - ct:+7.4f} |")
                    out.append(f" {c[f'rebate_pp_{int(rung)}']:+8.4f}")
                    say("".join(out))

    say("\n  THE SAME SPLIT AT gross 0.50 AND 1.00 (robustness, never selected on) — dCAGR pp only, 10 bps:")
    for pname in panels:
        for bk in BOOKS:
            for gross in GROSSES:
                line = []
                for lam in LAMS:
                    if lam == 1.00:
                        continue
                    g = {v: pick(df, panel=pname, book=bk, gross=gross, lam=lam, cost_bps=HEADLINE_RUNG, variant=v)
                         for v in VARIANTS}
                    line.append(f"{lam:.2f} tot{(g['D'].CAGR - g['U'].CAGR) * 100:+.2f}"
                                f"/lag{(g['LAG'].CAGR - g['U'].CAGR) * 100:+.2f}"
                                f"/cost{(g['COST'].CAGR - g['U'].CAGR) * 100:+.2f}")
                say(f"    {pname:5s} {bk:5s} g{gross:.2f}  " + "  ".join(line))

    # ---------------------------------------------------------------- B. the 0 bps column = pure lag
    say("\n=== B. THE 0 bps COLUMN IS PURE LAG BY CONSTRUCTION — this is the idea's direct question ===")
    say("    At 0 bps the bill is identically zero for BOTH books, so every difference below is HOLDINGS, not cost.")
    for pname in panels:
        for bk in BOOKS:
            say(f"\n  {pname} / {bk} / gross {LIVE_GROSS}")
            say("    lam  |  CAGR@0   dCAGR@0 |  Sharpe@0  dSharpe@0 |  MaxDD@0   dMaxDD@0 | OOS Sh@0  dOOS@0 | turn/yr  fidelity  names  stubNAV")
            u = pick(df, panel=pname, book=bk, gross=LIVE_GROSS, lam=1.00, cost_bps=0.0, variant="U")
            for lam in LAMS:
                d = pick(df, panel=pname, book=bk, gross=LIVE_GROSS, lam=lam, cost_bps=0.0, variant="D")
                c = pick(tf, panel=pname, book=bk, gross=LIVE_GROSS, lam=lam)
                say(f"   {lam:.2f}  | {d.CAGR:7.2%} {(d.CAGR - u.CAGR) * 100:+8.3f}pp | {d.Sharpe:8.4f}"
                    f" {d.Sharpe - u.Sharpe:+10.4f} | {d.MaxDD:8.2%} {(d.MaxDD - u.MaxDD) * 100:+9.3f}pp |"
                    f" {d.OOS_Sharpe:7.4f} {d.OOS_Sharpe - u.OOS_Sharpe:+7.4f} | {c.turnover_yr:7.2f}"
                    f" {c.heldset_fidelity:8.4%} {c.mean_names_in:6.1f} {c.stub_nav:8.4%}")

    # ---------------------------------------------------------------- C. run 39's headline, audited
    say("\n=== C. RUN 39's HEADLINE CLAIM, AUDITED CELL BY CELL (lam = 0.40, 10 bps, live gross) ===")
    say("    run 39 published CAGR +0.17 pp (U56) / +0.22 pp (B136) and MaxDD 2.11 / 2.43 pp WORSE, and attributed")
    say("    the CAGR to 'the un-traded distance is un-charged'.  Here is the audit:")
    for pname in panels:
        for bk in BOOKS:
            g = {v: pick(df, panel=pname, book=bk, gross=LIVE_GROSS, lam=0.40, cost_bps=HEADLINE_RUNG, variant=v)
                 for v in VARIANTS}
            c = pick(tf, panel=pname, book=bk, gross=LIVE_GROSS, lam=0.40)
            tot = (g["D"].CAGR - g["U"].CAGR) * 100; lg = (g["LAG"].CAGR - g["U"].CAGR) * 100
            ct = (g["COST"].CAGR - g["U"].CAGR) * 100
            dtot = (g["D"].MaxDD - g["U"].MaxDD) * 100; dlg = (g["LAG"].MaxDD - g["U"].MaxDD) * 100
            dct = (g["COST"].MaxDD - g["U"].MaxDD) * 100
            say(f"\n  {pname} / {bk}:  turnover {c.anchor_turnover_yr:.2f}x -> {c.turnover_yr:.2f}x"
                f"  (saved {c.turnover_saved_yr:.2f}x/yr = {c.rebate_pp_10:.4f} pp/yr of bill at 10 bps)")
            say(f"      dCAGR   total {tot:+.4f} pp  =  LAG {lg:+.4f}  +  COST {ct:+.4f}  +  interaction {tot - lg - ct:+.4f}"
                f"   -> cost share {ct / tot if abs(tot) > 1e-12 else float('nan'):+.2%} of the total")
            say(f"      dMaxDD  total {dtot:+.4f} pp  =  LAG {dlg:+.4f}  +  COST {dct:+.4f}  +  interaction {dtot - dlg - dct:+.4f}")
            say(f"      dSharpe total {g['D'].Sharpe - g['U'].Sharpe:+.4f}  =  LAG {g['LAG'].Sharpe - g['U'].Sharpe:+.4f}"
                f"  +  COST {g['COST'].Sharpe - g['U'].Sharpe:+.4f}"
                f"  +  interaction {(g['D'].Sharpe - g['U'].Sharpe) - (g['LAG'].Sharpe - g['U'].Sharpe) - (g['COST'].Sharpe - g['U'].Sharpe):+.4f}")

    # ---------------------------------------------------------------- D. attribution census
    say("\n=== D. ATTRIBUTION CENSUS OVER EVERY DAMPED CELL (6 lam x 3 gross x 2 books x 2 panels x 4 rungs = 288) ===")
    cen = []
    for pname in panels:
        for bk in BOOKS:
            for gross in GROSSES:
                for lam in LAMS:
                    if lam == 1.00:
                        continue
                    for rung in RUNGS:
                        g = {v: pick(df, panel=pname, book=bk, gross=gross, lam=lam, cost_bps=rung, variant=v)
                             for v in VARIANTS}
                        cen.append(dict(panel=pname, book=bk, gross=gross, lam=lam, cost_bps=rung,
                                        dCAGR=(g["D"].CAGR - g["U"].CAGR) * 100,
                                        lagCAGR=(g["LAG"].CAGR - g["U"].CAGR) * 100,
                                        costCAGR=(g["COST"].CAGR - g["U"].CAGR) * 100,
                                        dMaxDD=(g["D"].MaxDD - g["U"].MaxDD) * 100,
                                        lagMaxDD=(g["LAG"].MaxDD - g["U"].MaxDD) * 100,
                                        costMaxDD=(g["COST"].MaxDD - g["U"].MaxDD) * 100,
                                        dSharpe=g["D"].Sharpe - g["U"].Sharpe,
                                        lagSharpe=g["LAG"].Sharpe - g["U"].Sharpe,
                                        costSharpe=g["COST"].Sharpe - g["U"].Sharpe))
    cf = pd.DataFrame(cen); cf.to_csv(f"{OUT}.split.csv", index=False)
    for rung in RUNGS:
        q = cf[cf.cost_bps == rung]
        say(f"\n  {rung:5.1f} bps  (n = {len(q)} damped cells)")
        for k in ("CAGR", "MaxDD", "Sharpe"):
            t, l, c = q[f"d{k}"], q[f"lag{k}"], q[f"cost{k}"]
            say(f"    d{k:<7s} median total {t.median():+9.4f}   median LAG {l.median():+9.4f}"
                f"   median COST {c.median():+9.4f}   |  cells where |LAG| > |COST|: {int((l.abs() > c.abs()).sum())}/{len(q)}"
                f"   LAG sign -/0/+ {int((l < 0).sum())}/{int((l == 0).sum())}/{int((l > 0).sum())}")
    say("\n  THE DRAWDOWN QUESTION, STATED PLAINLY: how many damped cells have a WORSE MaxDD purely from LAG?")
    for rung in RUNGS:
        q = cf[cf.cost_bps == rung]
        say(f"    {rung:5.1f} bps: MaxDD worse from LAG alone in {int((q.lagMaxDD < 0).sum())}/{len(q)} cells"
            f"  (from COST alone {int((q.costMaxDD < 0).sum())}/{len(q)}; total worse {int((q.dMaxDD < 0).sum())}/{len(q)})")

    # ---------------------------------------------------------------- E. KEEP counts
    say(f"\n=== E. KEEP COUNTS OVER ALL {len(df)} PUBLISHED ROWS ===")
    say(f"  4b passes: {int(df.pass4b.sum())} of {len(df)}      4a passes: {int(df.pass4a.sum())} of {len(df)}")
    for rung in RUNGS:
        dd = df[df.cost_bps == rung]
        say(f"   {rung:5.1f} bps:  4b {int(dd.pass4b.sum()):3d}/{len(dd)}   4a {int(dd.pass4a.sum()):3d}/{len(dd)}"
            f"   binding leg on 4b FAILs: " +
            "  ".join(f"{k} {int((~dd[k][~dd.pass4b]).sum())}" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    say("\n  4b pass counts by (book, panel, variant, lam) over 4 rungs x 3 gross (max 12), at every lam:")
    for bk in BOOKS:
        for pname in panels:
            for v in VARIANTS:
                line = "  ".join(f"{lam:.2f} {int(df[(df.book == bk) & (df.panel == pname) & (df.variant == v) & (df.lam == lam)].pass4b.sum()):2d}/12"
                                 for lam in LAMS)
                say(f"    {bk:5s} {pname:5s} {v:5s}  {line}")
    say("\n  JOINT BOTH-PANEL 4b at the LIVE gross (a cell counts only if U56 AND B136 both pass), by variant and lam:")
    for bk in BOOKS:
        for v in VARIANTS:
            line = []
            for lam in LAMS:
                n = 0
                for rung in RUNGS:
                    a = pick(df, panel="U56", book=bk, gross=LIVE_GROSS, lam=lam, cost_bps=rung, variant=v)
                    b = pick(df, panel="B136", book=bk, gross=LIVE_GROSS, lam=lam, cost_bps=rung, variant=v)
                    n += int(bool(a.pass4b and b.pass4b))
                line.append(f"{lam:.2f} {n}/4")
            say(f"    {bk:5s} {v:5s}  " + "  ".join(line))

    # ---------------------------------------------------------------- F. rule 8
    say("\n=== F. RULE 8 — (lam, gross) chosen on <= 2016-12-31 ONLY, 2017-2026 read ONCE ===")
    say("    Two pre-stated IS-only choosers, applied to the REAL book D (the one a lane would actually adopt).")
    wf = []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        bw = rules_v2_weights(px[invest], band=BAND, gross=LIVE_GROSS).reindex(columns=px.columns).fillna(0.0)
        bres = run_book(px, bw, 1.0)
        for bk in BOOKS:
            for rung in RUNGS:
                b_oos = priced(bres, rung).loc[win].loc[OOS_START:]
                dd = df[(df.panel == pname) & (df.book == bk) & (df.cost_bps == rung) & (df.variant == "D")]
                und = dd[(dd.lam == 1.00) & (dd.gross == LIVE_GROSS)].iloc[0]
                for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                    p = dd.loc[dd[col].idxmax()]
                    wf.append(dict(panel=pname, book=bk, cost_bps=rung, chooser=chooser,
                                   pick_lam=p.lam, pick_gross=p.gross,
                                   OOS_CAGR=p.OOS_CAGR, OOS_Sharpe=p.OOS_Sharpe, OOS_MaxDD=p.OOS_MaxDD,
                                   pick_pass4b=bool(p.pass4b), pick_is_undamped=bool(p.lam == 1.00),
                                   und_OOS_CAGR=und.OOS_CAGR, und_OOS_Sharpe=und.OOS_Sharpe, und_OOS_MaxDD=und.OOS_MaxDD,
                                   base_OOS_CAGR=cagr(b_oos), base_OOS_Sharpe=sharpe(b_oos), base_OOS_MaxDD=maxdd(b_oos),
                                   spy_OOS_CAGR=cagr(spy_oos), spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_MaxDD=maxdd(spy_oos),
                                   beats_undamped_OOS_Sharpe=bool(p.OOS_Sharpe > und.OOS_Sharpe),
                                   beats_base_OOS_Sharpe=bool(p.OOS_Sharpe > sharpe(b_oos)),
                                   beats_spy_OOS_Sharpe=bool(p.OOS_Sharpe > sharpe(spy_oos))))
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say("   panel book  rung  chooser     -> pick (lam,gross) | OOS CAGR  OOS Sh  OOS DD | undamped OOS | RULES v2 OOS | SPY OOS | 4b")
    for _, r in wfd.iterrows():
        say(f"   {r.panel:5s} {r.book:5s} {r.cost_bps:5.1f} {r.chooser:11s} -> ({r.pick_lam:.2f}, {r.pick_gross:.2f})"
            f"   | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} {r.OOS_MaxDD:7.2%} |"
            f" {r.und_OOS_CAGR:6.2%}/{r.und_OOS_Sharpe:.4f} | {r.base_OOS_CAGR:6.2%}/{r.base_OOS_Sharpe:.4f}"
            f" | {r.spy_OOS_CAGR:6.2%}/{r.spy_OOS_Sharpe:.4f} | {'Y' if r.pick_pass4b else '.'}")
    say(f"\n  picks landing on the UNDAMPED incumbent (lam = 1.00): {int(wfd.pick_is_undamped.sum())} of {len(wfd)}")
    say(f"  picks beating the undamped anchor OOS on Sharpe:      {int(wfd.beats_undamped_OOS_Sharpe.sum())} of {len(wfd)}")
    say(f"  picks beating live RULES v2 OOS on Sharpe:            {int(wfd.beats_base_OOS_Sharpe.sum())} of {len(wfd)}")
    say(f"  picks beating SPY OOS on Sharpe:                      {int(wfd.beats_spy_OOS_Sharpe.sum())} of {len(wfd)}")
    say(f"  picks carrying a full-sample 4b pass:                 {int(wfd.pick_pass4b.sum())} of {len(wfd)}")
    say("  lam chosen, count: " + "  ".join(f"{l:.2f} x{int((wfd.pick_lam == l).sum())}" for l in LAMS))
    say("  gross chosen, count: " + "  ".join(f"{g:.2f} x{int((wfd.pick_gross == g).sum())}" for g in GROSSES))

    # ---------------------------------------------------------------- gates + log
    gf = pd.DataFrame(GATES); gf.to_csv(f"{OUT}.gates.csv", index=False)
    npass = int(gf.pass_.sum()); ntot = len(gf)
    say(f"\n=== GATES: {npass} of {ntot} pass ===")
    for _, g in gf.iterrows():
        if not g.pass_:
            say(f"    FAILED: {g.gate}")
    say(f"\n[done in {time.time() - t0:.0f}s]  rows {len(df)}  turnover rows {len(tf)}  split rows {len(cf)}")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

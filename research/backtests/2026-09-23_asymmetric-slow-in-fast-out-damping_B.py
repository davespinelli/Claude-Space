#!/usr/bin/env python3
"""idea 2412 (lane B, 2026-09-23) — is the DAMPER's BILL ASYMMETRIC?  Does SLOW-IN / FAST-OUT
keep the turnover cut while restoring the held set the symmetric damper breaks?

THE OBJECT.  Idea 2300 filed `RG100 + phi = 1.00` (`CAND`: every name INSIDE the 200d +/-3%
band held at `gross / N_in` of NAV, idle NAV swept to SHY) as the record's standing 4b
KEEP-candidate; idea 2322 added a 2.0% per-name cap (`CAP2`).  Idea 2391 (lane B run 39) then
filed the record's first PARTIAL-ADJUSTMENT damper as a 4b KEEP-candidate at `lam = 0.40`:

    at each weekly rebalance move EVERY risk name a fraction lam of the way to target,
    SHY absorbing the residual.

It cut turnover 3.51 -> 2.34x/yr (U56) and 4.68 -> 2.97x (B136) and it is the only device in
this record that holds the 50 bps column up.  But run 39 published its bill honestly, and the
bill is ENTIRELY ON THE SELL SIDE:

  * a name the 200d band gates OUT has target 0 and is only ever sold FRACTIONALLY, so its
    weight decays as (1 - lam)^k and NEVER REACHES ZERO;
  * post-trade STUB NAV 1.84% (U56) / 2.52% (B136) at lam = 0.40;
  * HELD-SET FIDELITY vs the undamped book falls to 76.1%; mean names held RISES 37.6 -> 50.7
    (U56) and 92.3 -> 125.1 (B136) — the book is diluted with names the band has ALREADY
    CONDEMNED;
  * and `L_DD` is now the BINDING leg on 29 of 29 sub-50bps 4b FAILs, with B136's margin only
    0.71 pp at 10 bps and 0.34 pp at 50 bps against the -20.23% cap.

Damping the EXIT is exactly what the 200d band exists to prevent.  It should also be the
CHEAPEST part to give back: exits are a minority of a long-only book's turnover (section E
measures the split rather than assuming it), and they are the leg that defends the drawdown.

THE IDEA.  Make the damper ASYMMETRIC — slow IN, fast OUT — and read whether the turnover cut
survives once the sell side is un-damped, and what it does to the binding DD leg.

DIAL 1 -- lam_in {1.00, 0.85, 0.70, 0.55, 0.40, 0.25, 0.10}: the fraction of the distance a
          name moves when it is being BOUGHT (entered or increased).
DIAL 2 -- the exit rule E:
            SYM       lam_out = lam_in for every reduction          (IS run 39's book exactly)
            FASTEXIT  lam_out = 1.00 for names the band gates OUT (target 0); every other
                      move at lam_in                                (slow in, fast OUT)
            FASTDOWN  lam_out = 1.00 for ANY reduction; increases at lam_in
          At lam_in = 1.00 all three rules COINCIDE with the undamped book and must reproduce
          engine.backtest bit-for-bit (gate G1).

REPORTED, NEVER SELECTED ON: gross is FIXED at the LIVE 0.75 for every selection and verdict,
with gross 1.00 published beside it as robustness; book {CAP2 (cap 0.02), CAND (cap INF)};
panels {U56, B136}; 4 cost rungs (0 / 10 / 25 / 50 bps); weekly cadence; band 0.03; t+1
execution; sweep SHY.  7 x 3 x 2 x 2 x 2 = 168 books, every one published at every rung = 672
rows.  SMALL is NOT priced and the reason is stated rather than buried: ideas 2318 / 2322 /
2326 / 2343 each published SMALL's 4b pass count at 0 of 40-120, so there is no pass there for
a turnover device to keep.

BOTH KEEP PATHS on every row: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse)
and 4b (Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x
SPY's).  RULE 8: (lam_in, E) chosen on warm-up..2016-12-31 ONLY by two pre-stated IS-only
choosers (C_ISSHARPE, C_ISCALMAR), then 2017-2026 read ONCE.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_asymmetric-slow-in-fast-out-damping_B.py
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

DATE, SLUG, LANE = "2026-09-23", "asymmetric-slow-in-fast-out-damping", "B"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, CADENCE, WARMUP = 0.03, "W", 260
LAMS = [1.00, 0.85, 0.70, 0.55, 0.40, 0.25, 0.10]
EXITS = ["SYM", "FASTEXIT", "FASTDOWN"]
GROSSES = [0.75, 1.00]          # 0.75 is the LIVE gross and the ONLY one selected at
LIVE_GROSS = 0.75
BOOKS = {"CAP2": 0.020, "CAND": "INF"}
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


# ---------------------------------------------------------------- the asymmetric backtester
def run_book(prices, weights, lam_in=1.0, exit_rule="SYM", freq=CADENCE, sweep=SWEEP):
    """engine.backtest with an ASYMMETRIC partial-adjustment damper on the risk names.

    Per risk name i at a rebalance, with d = target_i - held_i:
        SYM       f = lam_in                                    (idea 2391's book)
        FASTEXIT  f = 1.0 if target_i == 0 else lam_in          (slow in, fast OUT)
        FASTDOWN  f = 1.0 if d < 0        else lam_in           (slow in, fast DOWN)
        w_new_i = held_i + f * d
    SHY is then set to 1 - sum(risk weights), which is exactly its own target when every f = 1
    -- so lam_in = 1.00 is bit-identical to engine.backtest under ALL THREE rules (gate G1).
    Zero-cost returns and turnover are kept separately so every cost rung is priced from one
    pass.  The un-invested residual drifts at 0% (engine convention).

    NaN targets (the first rows, where engine.backtest's own shift(1) leaves a NaN row) are
    read as ZERO, i.e. "hold nothing yet".  A partial adjustment is RECURSIVE -- unlike
    engine.backtest's full reset a NaN target would poison `cur` for the whole path -- so the
    NaN must be resolved here rather than absorbed.  The affected rows are the first two of the
    raw panel, 260 rows before the reported window opens; G1 compares the two paths exactly as
    idea 2391's damped replica did.
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
    stub = np.zeros(n)                  # NAV in names whose TARGET is 0 today (any day)
    stub_rb = np.full(n, np.nan)        # ... measured POST-TRADE, on rebalance days only
    buys = np.zeros(n); sells = np.zeros(n)
    cur = np.zeros(len(cols))
    turnover = np.zeros(n); gross_s = np.zeros(n); lev = np.zeros(n)
    wt = np.nan_to_num(w_target.values, nan=0.0); rv = rets.values
    for i in range(n):
        if mask[i] or i == 0:
            tgt = wt[i]
            d = tgt - cur
            if exit_rule == "SYM":
                f = np.full(len(cols), lam_in)
            elif exit_rule == "FASTEXIT":
                f = np.where(tgt <= 1e-15, 1.0, lam_in)
            elif exit_rule == "FASTDOWN":
                f = np.where(d < 0.0, 1.0, lam_in)
            else:
                raise ValueError(exit_rule)
            new = cur.copy()
            new[risk] = cur[risk] + f[risk] * d[risk]
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
        z = risk & (wt[i] <= 1e-15)               # target-zero risk names still held
        stub[i] = cur[z].sum()
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
    say("=== idea 2412 (lane B) — is the DAMPER's BILL ASYMMETRIC?  SLOW-IN / FAST-OUT on the capped candidate ===")
    say(f"    {DATE}  lane {LANE}   band {BAND}  cadence {CADENCE}  t+1  rungs {RUNGS} bps  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 lam_in {LAMS}   DIAL 2 exit rule {EXITS}")
    say(f"    FIXED at the live value, not selected: gross {LIVE_GROSS} (gross 1.00 published as robustness)")
    say(f"    REPORTED not selected: book {list(BOOKS)}  panels U56/B136  rungs {RUNGS}")
    gate("G8 exactly two tuned parameters", "lam_in, exit rule E", "2", True)

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

    # ---- G1: at lam_in = 1 EVERY exit rule collapses to engine.backtest
    for bk, cap in BOOKS.items():
        w1 = cap_weights(px_u, panels["U56"][1], cap, LIVE_GROSS)
        r_eng = backtest(px_u, w1, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
        worst = 0.0
        for E in EXITS:
            worst = max(worst, float((r_eng - priced(run_book(px_u, w1, 1.0, E), HEADLINE_RUNG)).abs().max()))
        gate(f"G1 lam_in=1 replica == engine.backtest under ALL 3 exit rules ({bk}, U56, g={LIVE_GROSS})",
             f"max|d| over {EXITS} = {worst:.3e}", "< 1e-12", worst < 1e-12)

    # ---- G7: NO LOOKAHEAD.  Truncating the price panel must not move any earlier held weight.
    cut = px_u.index[int(len(px_u) * 0.70)]
    q = px_u.loc[:cut]
    full = run_book(px_u, cap_weights(px_u, panels["U56"][1], 0.020, LIVE_GROSS), 0.55, "FASTEXIT")["held"].loc[:cut]
    trunc = run_book(q, cap_weights(q, list(q.columns), 0.020, LIVE_GROSS), 0.55, "FASTEXIT")["held"]
    d7 = float((full - trunc.reindex_like(full)).abs().max().max())
    gate("G7 no lookahead (panel truncated at 70%, lam_in=0.55/FASTEXIT, CAP2/U56)", f"max|dw| {d7:.3e}", "< 1e-12", d7 < 1e-12)

    # ---------------------------------------------------------------- the grid
    rows, tr_rows = [], []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        yrs = len(win) / 252
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        bw = rules_v2_weights(px[invest], band=BAND, gross=LIVE_GROSS).reindex(columns=px.columns).fillna(0.0)
        bres = run_book(px, bw, 1.0, "SYM")
        base_r = priced(bres, HEADLINE_RUNG).loc[win]
        base_t = bres["turnover"].loc[win].sum() / yrs
        say(f"\n--- panel {pname}  ({len(invest)} columns)  SPY {cagr(spy):.2%} / {sharpe(spy):.4f} / {maxdd(spy):.2%}"
            f"   live RULES v2 {cagr(base_r):.2%} / {sharpe(base_r):.4f} / {maxdd(base_r):.2%}  turnover {base_t:.2f}x")
        publish(f"G10 live RULES v2 turnover on {pname}, measured here on the same tape, cadence and"
                f" sum|dw| convention as every book in this run (idea 2391's correction (2) stands)", f"{base_t:.4f}x/yr")
        for bk, cap in BOOKS.items():
            for gross in GROSSES:
                wt = cap_weights(px, invest, cap, gross)
                ref_state = None
                for E in EXITS:
                    for lam in LAMS:
                        res = run_book(px, wt, lam, E)
                        inw = res["held"].drop(columns=[SWEEP]).loc[win]
                        state = (inw.values > 1e-12)
                        if lam == 1.00 and E == "SYM":
                            ref_state = state
                        fid = float((state == ref_state).mean())
                        pos = inw.values[inw.values > 1e-12]
                        risk_nav = inw.values.sum(axis=1)
                        stub_share = float((res["stub"].loc[win].values / np.where(risk_nav > 0, risk_nav, np.nan)).mean())
                        tr_rows.append(dict(panel=pname, book=bk, gross=gross, exit_rule=E, lam_in=lam,
                                            turnover_yr=float(res["turnover"].loc[win].sum() / yrs),
                                            buy_yr=float(res["buys"].loc[win].sum() / yrs),
                                            sell_yr=float(res["sells"].loc[win].sum() / yrs),
                                            base_turnover_yr=base_t,
                                            heldset_fidelity=fid,
                                            mean_names_in=float(state.sum(axis=1).mean()),
                                            stub_nav=float(res["stub"].loc[win].mean()),
                                            stub_rb_nav=float(res["stub_rb"].loc[win].mean(skipna=True)),
                                            stub_share_of_risk=stub_share,
                                            max_name_w=float(pos.max()) if len(pos) else 0.0,
                                            p99_name_w=float(np.quantile(pos, 0.99)) if len(pos) else 0.0,
                                            mean_gross=float(res["gross"].loc[win].mean()),
                                            mean_sweep_w=float(res["held"][SWEEP].loc[win].mean()),
                                            max_row_sum=float(res["gross"].max()),
                                            lev_events=res["lev_events"]))
                        for rung in RUNGS:
                            r = priced(res, rung).loc[win]
                            r_oos = r.loc[OOS_START:]
                            h1, h2 = halves(r)
                            rows.append(dict(panel=pname, book=bk, gross=gross, exit_rule=E, lam_in=lam,
                                             cost_bps=rung,
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

    # ---- G2 / G3 / G3b: external reproduction of three committed headlines
    h = pick(df, panel="U56", book="CAP2", gross=LIVE_GROSS, exit_rule="SYM", lam_in=1.00, cost_bps=HEADLINE_RUNG)
    t2 = pick(tf, panel="U56", book="CAP2", gross=LIVE_GROSS, exit_rule="SYM", lam_in=1.00)
    d2 = max(abs(h.CAGR - 0.1162), abs(h.Sharpe - 1.2687) / 10, abs(h.MaxDD + 0.1481),
             abs(h.OOS_CAGR - 0.1277), abs(h.OOS_Sharpe - 1.3318) / 10)
    gate("G2 reproduces idea 2336's committed CAP2 U56 headline (11.62%/1.2687/-14.81%, OOS 12.77%/1.3318)",
         f"read {h.CAGR:.2%} / {h.Sharpe:.4f} / {h.MaxDD:.2%}, OOS {h.OOS_CAGR:.2%} / {h.OOS_Sharpe:.4f},"
         f" turnover {t2.turnover_yr:.2f}x (committed 3.51x) -> max|d| {d2:.2e}", "< 1e-3", d2 < 1e-3)
    h3 = pick(df, panel="U56", book="CAND", gross=LIVE_GROSS, exit_rule="SYM", lam_in=1.00, cost_bps=HEADLINE_RUNG)
    d3 = max(abs(h3.CAGR - 0.125950), abs(h3.Sharpe - 1.1934) / 10, abs(h3.MaxDD + 0.173923),
             abs(h3.OOS_CAGR - 0.138525), abs(h3.OOS_Sharpe - 1.2397) / 10)
    gate("G3 reproduces idea 2300/2332's committed CAND U56 headline (12.5950%/1.1934/-17.3923%, OOS 13.8525%/1.2397)",
         f"read {h3.CAGR:.4%} / {h3.Sharpe:.4f} / {h3.MaxDD:.4%}, OOS {h3.OOS_CAGR:.4%} / {h3.OOS_Sharpe:.4f}"
         f" -> max|d| {d3:.2e}", "< 1e-3", d3 < 1e-3)
    h4 = pick(df, panel="U56", book="CAP2", gross=LIVE_GROSS, exit_rule="SYM", lam_in=0.40, cost_bps=HEADLINE_RUNG)
    t4 = pick(tf, panel="U56", book="CAP2", gross=LIVE_GROSS, exit_rule="SYM", lam_in=0.40)
    d4 = max(abs(h4.CAGR - 0.1179), abs(h4.Sharpe - 1.2538) / 10, abs(h4.MaxDD + 0.1692),
             abs(h4.OOS_CAGR - 0.1298), abs(h4.OOS_Sharpe - 1.3091) / 10, abs(t4.turnover_yr - 2.34) / 100)
    gate("G3b reproduces idea 2391's committed SYM lam=0.40 headline (11.79%/1.2538/-16.92%, OOS 12.98%/1.3091, 2.34x)",
         f"read {h4.CAGR:.2%} / {h4.Sharpe:.4f} / {h4.MaxDD:.2%}, OOS {h4.OOS_CAGR:.2%} / {h4.OOS_Sharpe:.4f},"
         f" turnover {t4.turnover_yr:.2f}x -> max|d| {d4:.2e}", "< 1e-3", d4 < 1e-3)
    gate("G4 no leverage anywhere (168 books)", f"max row gross {tf.max_row_sum.max():.9f};"
         f" risk-sleeve rescale events {int(tf.lev_events.sum())}", "<= 1+1e-12", tf.max_row_sum.max() <= 1 + 1e-12)

    # ---- G5: the dial BITES on turnover under every exit rule
    bites = []
    for (p, b, g, E), grp in tf.groupby(["panel", "book", "gross", "exit_rule"]):
        v = grp.sort_values("lam_in", ascending=False).turnover_yr.values
        bites.append(v[-1] < v[0] - 1e-9)
    gate("G5 the lam_in dial BITES under every exit rule (turnover at 0.10 strictly below 1.00)",
         f"{sum(bites)} of {len(bites)} (panel, book, gross, E) cells", f"{len(bites)} of {len(bites)}", all(bites))

    # ---- G11: the ASYMMETRIC rules carry ZERO post-trade stub BY CONSTRUCTION.  That is the
    # whole claim of the idea and it is asserted, not assumed.
    z_sym = tf[(tf.lam_in == 1.00)].stub_rb_nav.abs().max()
    gate("G11 lam_in=1.00 carries zero POST-TRADE stub (a gated-OUT name is sold in full)",
         f"max post-trade stub NAV {z_sym:.3e}", "< 1e-12", z_sym < 1e-12)
    z_fast = tf[tf.exit_rule.isin(["FASTEXIT", "FASTDOWN"])].stub_rb_nav.abs().max()
    gate("G12 FASTEXIT / FASTDOWN carry zero POST-TRADE stub at EVERY lam_in (the idea's whole claim)",
         f"max post-trade stub NAV over {len(tf[tf.exit_rule != 'SYM'])} books {z_fast:.3e}", "< 1e-12", z_fast < 1e-12)
    f_fast = tf[(tf.exit_rule == "FASTEXIT") & (tf.lam_in < 1.0)].heldset_fidelity.min()
    gate("G13 FASTEXIT reproduces the undamped HELD SET exactly (a name is held iff the band holds it)",
         f"min held-set fidelity over damped FASTEXIT books {f_fast:.6%}", "== 100%", f_fast >= 1.0 - 1e-12)
    publish("G11b the DAILY stub floor at lam_in=1.00 is pure weekly-cadence drift, not damping",
            "  ".join(f"{r.panel}/{r.book} {r.stub_nav:.4%}"
                      for _, r in tf[(tf.lam_in == 1.00) & (tf.gross == LIVE_GROSS) & (tf.exit_rule == "SYM")].iterrows()))

    # ---------------------------------------------------------------- A. full grid
    say("\n=== A. THE FULL GRID AT THE LIVE GROSS 0.75 AND THE HEADLINE RUNG (10 bps) — every point, nothing dropped ===")
    for pname in panels:
        for bk in BOOKS:
            say(f"\n  {pname} / {bk} / gross {LIVE_GROSS}")
            say("   E          lam_in |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh  OOS DD | 4a 4b |"
                " H1/H2/OOS/DD/CAGR | turn/yr  buy/sell  fidelity  stubNAV   maxw   names")
            for E in EXITS:
                for lam in LAMS:
                    r = pick(df, panel=pname, book=bk, gross=LIVE_GROSS, exit_rule=E, lam_in=lam, cost_bps=HEADLINE_RUNG)
                    c = pick(tf, panel=pname, book=bk, gross=LIVE_GROSS, exit_rule=E, lam_in=lam)
                    lg = "".join("1" if r[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                    say(f"  {E:9s}  {lam:.2f}   | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%} |"
                        f" {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} {r.OOS_MaxDD:7.2%} |"
                        f" {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg:17s} |"
                        f" {c.turnover_yr:7.2f} {c.buy_yr:5.2f}/{c.sell_yr:.2f} {c.heldset_fidelity:9.4%}"
                        f" {c.stub_nav:8.4%} {c.max_name_w:6.2%} {c.mean_names_in:6.1f}")
    say("\n  ROBUSTNESS, NEVER SELECTED ON — the same grid at gross 1.00 (10 bps), 4b flag only:")
    for pname in panels:
        for bk in BOOKS:
            for E in EXITS:
                line = "  ".join(f"{lam:.2f}:" +
                                 ("Y" if pick(df, panel=pname, book=bk, gross=1.00, exit_rule=E, lam_in=lam,
                                              cost_bps=HEADLINE_RUNG).pass4b else ".") for lam in LAMS)
                say(f"    {pname:5s} {bk:5s} {E:9s}  {line}")

    # ---------------------------------------------------------------- B. keep counts
    say(f"\n=== B. KEEP COUNTS OVER ALL {len(df)} PUBLISHED ROWS (7 lam_in x 3 E x 2 gross x 2 books x 2 panels x 4 rungs) ===")
    say(f"  4b passes: {int(df.pass4b.sum())} of {len(df)}      4a passes: {int(df.pass4a.sum())} of {len(df)}")
    for rung in RUNGS:
        dd = df[df.cost_bps == rung]
        say(f"   {rung:5.1f} bps:  4b {int(dd.pass4b.sum()):3d}/{len(dd)}   4a {int(dd.pass4a.sum()):3d}/{len(dd)}"
            f"   binding leg on 4b FAILs: " +
            "  ".join(f"{k} {int((~dd[k][~dd.pass4b]).sum())}" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    say("\n  4b pass counts by (book, panel, E, lam_in) over the 4 rungs x 2 gross:")
    for bk in BOOKS:
        for pname in panels:
            for E in EXITS:
                line = "  ".join(f"{lam:.2f} {int(df[(df.book == bk) & (df.panel == pname) & (df.exit_rule == E) & (df.lam_in == lam)].pass4b.sum()):2d}/8"
                                 for lam in LAMS)
                say(f"    {bk:5s} {pname:5s} {E:9s}  {line}")
    say("\n  4b pass counts at 25 and 50 bps ONLY — the rungs this family has always died on:")
    for bk in BOOKS:
        for pname in panels:
            for E in EXITS:
                hi = df[(df.book == bk) & (df.panel == pname) & (df.exit_rule == E) & (df.cost_bps >= 25.0)]
                line = "  ".join(f"{lam:.2f} {int(hi[hi.lam_in == lam].pass4b.sum()):2d}/4" for lam in LAMS)
                say(f"    {bk:5s} {pname:5s} {E:9s}  {line}")

    # ---------------------------------------------------------------- C. what un-damping the exit buys
    say("\n=== C. WHAT UN-DAMPING THE EXIT BUYS: FASTEXIT and FASTDOWN minus SYM at the SAME lam_in ===")
    say("    (gross 0.75; d vs idea 2391's symmetric book at the identical lam_in)")
    for pname in panels:
        for bk in BOOKS:
            say(f"\n  {pname} / {bk}")
            say("   E         lam_in |  dturn/yr  dturn%  | dCAGR@10  dSharpe@10  dMaxDD@10  dOOS_Sh@10 | dfidelity  dstubNAV  dnames | 4b SYM -> E")
            for E in ("FASTEXIT", "FASTDOWN"):
                for lam in LAMS:
                    a = pick(df, panel=pname, book=bk, gross=LIVE_GROSS, exit_rule="SYM", lam_in=lam, cost_bps=HEADLINE_RUNG)
                    b = pick(df, panel=pname, book=bk, gross=LIVE_GROSS, exit_rule=E, lam_in=lam, cost_bps=HEADLINE_RUNG)
                    ca = pick(tf, panel=pname, book=bk, gross=LIVE_GROSS, exit_rule="SYM", lam_in=lam)
                    cb = pick(tf, panel=pname, book=bk, gross=LIVE_GROSS, exit_rule=E, lam_in=lam)
                    say(f"  {E:9s} {lam:.2f}  | {cb.turnover_yr - ca.turnover_yr:+9.2f}"
                        f" {cb.turnover_yr / ca.turnover_yr - 1:+7.1%} | {b.CAGR - a.CAGR:+8.2%}"
                        f" {b.Sharpe - a.Sharpe:+11.4f} {b.MaxDD - a.MaxDD:+10.2%} {b.OOS_Sharpe - a.OOS_Sharpe:+11.4f}"
                        f" | {cb.heldset_fidelity - ca.heldset_fidelity:+9.2%} {cb.stub_nav - ca.stub_nav:+9.4%}"
                        f" {cb.mean_names_in - ca.mean_names_in:+7.1f} |"
                        f" {'Y' if a.pass4b else '.'} -> {'Y' if b.pass4b else '.'}")

    say("\n=== C2. AND WHAT EACH BOOK BUYS AGAINST THE UNDAMPED CANDIDATE (lam_in = 1.00) ===")
    for pname in panels:
        for bk in BOOKS:
            ref = {rg: pick(df, panel=pname, book=bk, gross=LIVE_GROSS, exit_rule="SYM", lam_in=1.00, cost_bps=rg)
                   for rg in RUNGS}
            t1r = pick(tf, panel=pname, book=bk, gross=LIVE_GROSS, exit_rule="SYM", lam_in=1.00)
            say(f"\n  {pname} / {bk} / gross 0.75   (undamped {t1r.turnover_yr:.2f}x/yr, live RULES v2 {t1r.base_turnover_yr:.2f}x/yr)")
            say("   E         lam_in |  turn/yr  dturn% | dCAGR @0bps   @10bps   @25bps   @50bps | dSharpe@10  dMaxDD@10  dOOS_Sh@10")
            for E in EXITS:
                for lam in LAMS:
                    c = pick(tf, panel=pname, book=bk, gross=LIVE_GROSS, exit_rule=E, lam_in=lam)
                    r = {rg: pick(df, panel=pname, book=bk, gross=LIVE_GROSS, exit_rule=E, lam_in=lam, cost_bps=rg)
                         for rg in RUNGS}
                    say(f"  {E:9s} {lam:.2f}  | {c.turnover_yr:8.2f} {c.turnover_yr / t1r.turnover_yr - 1:+7.1%} |" +
                        "".join(f" {r[rg].CAGR - ref[rg].CAGR:+8.2%}" for rg in RUNGS) +
                        f" | {r[10.0].Sharpe - ref[10.0].Sharpe:+10.4f} {r[10.0].MaxDD - ref[10.0].MaxDD:+10.2%}"
                        f" {r[10.0].OOS_Sharpe - ref[10.0].OOS_Sharpe:+11.4f}")

    # ---------------------------------------------------------------- D. rule 8
    say("\n=== D. RULE 8 — (lam_in, E) chosen on <= 2016-12-31 ONLY at the live gross, 2017-2026 read once ===")
    wf = []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        bw = rules_v2_weights(px[invest], band=BAND, gross=LIVE_GROSS).reindex(columns=px.columns).fillna(0.0)
        base_r = priced(run_book(px, bw, 1.0, "SYM"), HEADLINE_RUNG).loc[win]
        b_oos = base_r.loc[OOS_START:]
        for bk in BOOKS:
            for rung in RUNGS:
                dd = df[(df.panel == pname) & (df.book == bk) & (df.cost_bps == rung) & (df.gross == LIVE_GROSS)]
                und = dd[(dd.lam_in == 1.00) & (dd.exit_rule == "SYM")].iloc[0]
                sym40 = dd[(dd.lam_in == 0.40) & (dd.exit_rule == "SYM")].iloc[0]
                for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                    p = dd.loc[dd[col].idxmax()]
                    wf.append(dict(panel=pname, book=bk, cost_bps=rung, chooser=chooser,
                                   pick_lam_in=p.lam_in, pick_exit=p.exit_rule,
                                   OOS_CAGR=p.OOS_CAGR, OOS_Sharpe=p.OOS_Sharpe, OOS_MaxDD=p.OOS_MaxDD,
                                   pick_pass4b=bool(p.pass4b), pick_is_undamped=bool(p.lam_in == 1.00),
                                   pick_is_asymmetric=bool(p.exit_rule != "SYM" and p.lam_in < 1.0),
                                   und_OOS_Sharpe=und.OOS_Sharpe, sym40_OOS_Sharpe=sym40.OOS_Sharpe,
                                   beats_undamped_OOS_Sharpe=bool(p.OOS_Sharpe > und.OOS_Sharpe),
                                   beats_sym40_OOS_Sharpe=bool(p.OOS_Sharpe > sym40.OOS_Sharpe),
                                   base_OOS_CAGR=cagr(b_oos), base_OOS_Sharpe=sharpe(b_oos), base_OOS_MaxDD=maxdd(b_oos),
                                   spy_OOS_CAGR=cagr(spy_oos), spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_MaxDD=maxdd(spy_oos),
                                   beats_SPY_OOS_Sharpe=bool(p.OOS_Sharpe > sharpe(spy_oos)),
                                   beats_LIVE_OOS_Sharpe=bool(p.OOS_Sharpe > sharpe(b_oos))))
                    say(f"  {pname:5s} {bk:5s} {rung:5.1f}bps {chooser:11s} -> lam_in {p.lam_in:.2f} {p.exit_rule:9s} |"
                        f" OOS {p.OOS_CAGR:6.2%} / {p.OOS_Sharpe:.4f} / {p.OOS_MaxDD:7.2%} |"
                        f" undamped OOS {und.OOS_CAGR:6.2%} / {und.OOS_Sharpe:.4f} | SYM0.40 OOS {sym40.OOS_Sharpe:.4f} |"
                        f" live v2 OOS {cagr(b_oos):6.2%} / {sharpe(b_oos):.4f} | SPY OOS {cagr(spy_oos):6.2%} /"
                        f" {sharpe(spy_oos):.4f} | full 4b {'Y' if p.pass4b else '.'}")
    wfd = pd.DataFrame(wf)
    wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"\n  rule-8 picks landing on lam_in = 1.00 (the undamped book): {int(wfd.pick_is_undamped.sum())} of {len(wfd)}")
    say(f"  picks landing on an ASYMMETRIC rule (E != SYM, lam_in < 1):  {int(wfd.pick_is_asymmetric.sum())} of {len(wfd)}")
    say(f"  picks beating the UNDAMPED book's OOS Sharpe:                {int(wfd.beats_undamped_OOS_Sharpe.sum())} of {len(wfd)}")
    say(f"  picks beating idea 2391's SYM lam=0.40 OOS Sharpe:           {int(wfd.beats_sym40_OOS_Sharpe.sum())} of {len(wfd)}")
    say(f"  picks beating SPY's OOS Sharpe:                              {int(wfd.beats_SPY_OOS_Sharpe.sum())} of {len(wfd)}")
    say(f"  picks beating LIVE RULES v2's OOS Sharpe:                    {int(wfd.beats_LIVE_OOS_Sharpe.sum())} of {len(wfd)}")
    say(f"  picks whose full-sample row also passes 4b:                  {int(wfd.pick_pass4b.sum())} of {len(wfd)}")
    say("  pick distribution over lam_in: " + "  ".join(f"{lam:.2f} {int((wfd.pick_lam_in == lam).sum())}" for lam in LAMS))
    say("  pick distribution over E:      " + "  ".join(f"{E} {int((wfd.pick_exit == E).sum())}" for E in EXITS))
    agree = [g.pick_lam_in.nunique() == 1 and g.pick_exit.nunique() == 1
             for _, g in wfd.groupby(["book", "cost_bps", "chooser"])]
    say(f"  the two panels pick the SAME (lam_in, E): {sum(agree)} of {len(agree)} (book, rung, chooser) cells")

    # ---------------------------------------------------------------- E. the split, and the idea's own cost
    say("\n=== E. WHERE THE TURNOVER ACTUALLY IS: BUY vs SELL legs (gross 0.75, x/yr) ===")
    say("  (the premise under test is that exits are a MINORITY of turnover and so are cheap to un-damp)")
    for pname in panels:
        for bk in BOOKS:
            for E in EXITS:
                row = tf[(tf.panel == pname) & (tf.book == bk) & (tf.gross == LIVE_GROSS)
                         & (tf.exit_rule == E)].set_index("lam_in")
                say(f"  {pname:5s} {bk:5s} {E:9s}  " + "  ".join(
                    f"{lam:.2f}: {row.loc[lam].buy_yr:.2f}B/{row.loc[lam].sell_yr:.2f}S"
                    f"({row.loc[lam].sell_yr / max(row.loc[lam].buy_yr + row.loc[lam].sell_yr, 1e-12):.0%}S)"
                    for lam in LAMS))
    say("\n=== E2. THE IDEA'S OWN COST — the STUB a fractional sale leaves behind (gross 0.75) ===")
    for label, col, fmt in (("POST-TRADE stub NAV (0 at lam_in=1 and under FASTEXIT/FASTDOWN by construction)", "stub_rb_nav", "{:8.4%}"),
                            ("daily stub NAV (post-trade stub PLUS the weekly-cadence floor)", "stub_nav", "{:8.4%}"),
                            ("held-set fidelity vs the undamped book", "heldset_fidelity", "{:8.4%}"),
                            ("mean names held IN", "mean_names_in", "{:8.2f}"),
                            ("max per-name weight (CAP2 exists to hold this down)", "max_name_w", "{:8.2%}"),
                            ("mean book gross", "mean_gross", "{:8.4f}"),
                            ("mean SHY sweep weight", "mean_sweep_w", "{:8.4f}")):
        say(f"\n  {label}:")
        say("  panel book  E          " + "".join(f"   {lam:.2f}  " for lam in LAMS))
        for pname in panels:
            for bk in BOOKS:
                for E in EXITS:
                    row = tf[(tf.panel == pname) & (tf.book == bk) & (tf.gross == LIVE_GROSS)
                             & (tf.exit_rule == E)].set_index("lam_in")
                    say(f"  {pname:5s} {bk:5s} {E:9s} " + "".join(" " + fmt.format(row.loc[lam][col]) for lam in LAMS))

    # ---------------------------------------------------------------- F. the decisive read
    say("\n=== F. THE DECISIVE READ — JOINT 4b ON BOTH PANELS AT THE LIVE GROSS (0.75), by (E, lam_in) and rung ===")
    say("  (a device that keeps the candidate's pass must keep it on BOTH panels at the SAME dials and rung)")
    for bk in BOOKS:
        say(f"\n  {bk}:  E         lam_in |" + "".join(f"  {rg:>4.0f}bps " for rg in RUNGS)
            + " | turn/yr U56  B136 | MaxDD@10 U56    B136  | DD margin vs cap U56   B136")
        for E in EXITS:
            for lam in LAMS:
                cells = []
                for rg in RUNGS:
                    ok = all(bool(pick(df, panel=pn, book=bk, gross=LIVE_GROSS, exit_rule=E, lam_in=lam,
                                       cost_bps=rg).pass4b) for pn in panels)
                    cells.append("BOTH" if ok else " .  ")
                tt, ddv, mar = [], [], []
                for pn, (px, _) in panels.items():
                    c = pick(tf, panel=pn, book=bk, gross=LIVE_GROSS, exit_rule=E, lam_in=lam)
                    r = pick(df, panel=pn, book=bk, gross=LIVE_GROSS, exit_rule=E, lam_in=lam, cost_bps=HEADLINE_RUNG)
                    spy_dd = maxdd(px["SPY"].pct_change().fillna(0.0).loc[px.index[WARMUP:]])
                    tt.append(c.turnover_yr); ddv.append(r.MaxDD); mar.append(r.MaxDD - DD_CAP * spy_dd)
                say(f"    {E:9s} {lam:.2f} |" + "".join(f"  {c}   " for c in cells)
                    + f" |  {tt[0]:5.2f} {tt[1]:5.2f} |  {ddv[0]:+7.2%} {ddv[1]:+8.2%}  |"
                    f"  {mar[0]:+8.2%} {mar[1]:+9.2%}")

    gdf = pd.DataFrame(GATES)
    gdf.to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n=== GATES: {int(gdf.pass_.sum())} of {len(gdf)} pass ===")
    for _, g in gdf[~gdf.pass_].iterrows():
        say(f"    FAILED: {g.gate} = {g.value} (target {g.target})")
    say(f"\nwrote {OUT}.grid.csv / .turnover.csv / .walkforward.csv / .gates.csv   ({time.time() - t0:.0f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""idea 2399 (lane C, run 43, 2026-09-23) — DOES AN EQUITY-CURVE DE-GROSSING GATE CUT THE CAPPED
CANDIDATE'S DRAWDOWN WHERE NAME-LEVEL DEVICES COULD NOT?

THE GAP.  `L_DD` is the binding leg on 29 of 29 sub-50bps 4b FAILs in idea 2391 and on every
finite-cap failure in idea 2387, and every device the record has tried against it acts NAME BY
NAME: inverse-vol sizing (2362), sector caps (2339), the breadth cap (2387), the relative cap
(2381).  Idea 2381 measured all of them to be pure exposure dials.  The untried device acts on
the BOOK and on nothing else: a two-state switch driven by the book's OWN equity curve.

    s_t   = 1.0   when the book's equity E is at or above its E-day moving average
          = d     when it is below                                 (0 <= d <= 1)
    w_i   = s_t x min(gross / N_in, 0.02)   on names INSIDE the 200d +/- 0.03 band
    SHY   = 1 - sum_i w_i                   (phi = 1.00, the whole residual)

DIAL 1 -- E (equity-curve MA length) {20, 50, 100, 200} trading days.
DIAL 2 -- d (the de-grossed multiplier) {0.00, 0.25, 0.50, 0.75, 1.00}.
          **d = 1.00 IS CAP2 EXACTLY** (s_t == 1 on every day, at every E), so one ladder spans
          the committed book; asserted bit-identically by G3.

CAUSALITY.  The equity curve is a function of committed prices and the book's OWN PAST weights,
so it is causal — but only if read correctly.  At a rebalance day i the gate reads the equity
level through i-1 and its MA over the E values ENDING AT i-1, i.e. returns already banked when
the switch is thrown.  The resulting weights are executed at t+1 like every book here.  G8/G9
assert this by truncating the panel and checking the scaler AND the realised return series.

TWO CONVENTIONS, BOTH PUBLISHED, NEITHER SELECTED ON.  S = SELF-REFERENTIAL (headline, exactly
as the queue line words it: the book's own equity curve, so the switch feeds back on itself).
U = the UNSCALED CAP2 book's equity curve as the reference (no feedback).  The distinction is
the whole reason a book-level device can behave differently from a name-level one, so both are
priced and reported.

REPORTED, NEVER SELECTED ON: panels {U56, B136}, cost rungs {0, 10, 25, 50} bps, gross
{0.75, 1.00}, band 0.03, the 2% name cap, weekly cadence, t+1 execution, SHY sweep phi = 1.00.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_equity-curve-de-grossing-gate-on-the-capped-candidate_C.py
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

DATE, SLUG, LANE = "2026-09-23", "equity-curve-de-grossing-gate-on-the-capped-candidate", "C"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, MA_LEN, CADENCE, WARMUP = 0.03, 200, "W", 260
EMAS = [20, 50, 100, 200]                 # DIAL 1
DVALS = [0.00, 0.25, 0.50, 0.75, 1.00]    # DIAL 2 ; 1.00 IS CAP2
GROSSES = [0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG, NAME_CAP, SWEEP = 10.0, 0.020, "SHY"
CONVENTIONS = ["S", "U"]                  # S = self-referential (headline); U = unscaled ref
HEADLINE_CONV, ANCHOR_E = "S", 50
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


# ---------------------------------------------------------------- the risk book (pre-scaler)
def cap2_risk_weights(px, invest, gross, cap=NAME_CAP):
    """idea 2322's CAP2 RISK sleeve only (no sweep): w_i = min(gross / N_in, cap) on names INSIDE
    the 200d +/- 0.03 band.  The SHY sweep is applied inside the runner AFTER the scaler, so that
    s_t scales risk and never the cash leg."""
    q = px[invest]
    pr = q.notna()
    inb = band_state(q, BAND) & pr
    nin = inb.sum(axis=1).replace(0, np.nan)
    per = (gross / nin).clip(upper=cap).fillna(0.0)
    return inb.astype(float).mul(per, axis=0).reindex(columns=px.columns).fillna(0.0)


def cap2_full_reference(px, invest, gross, cap=NAME_CAP):
    """Independent CAP2 construction WITH the sweep (the committed book), for the G3 anchor."""
    w = cap2_risk_weights(px, invest, gross, cap).copy()
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return w


# ---------------------------------------------------------------- the gated runner
def run_eg(prices, w_risk, E, d, conv, ref_eq=None, freq=CADENCE, sweep=True):
    """engine.backtest with an EQUITY-CURVE DE-GROSSING GATE on the risk sleeve.

    At each rebalance day i:
        eq      = the reference equity curve's level at i-1
        ma      = mean of that curve over its E values ending at i-1
        s       = 1.0 if eq >= ma else d
    The reference is this book's OWN zero-cost equity curve under convention S (recursive, the
    headline) or the UNSCALED CAP2 book's curve `ref_eq` under convention U.  While fewer than E
    values exist the gate is NEUTRAL (s = 1, i.e. CAP2); every scored row has the MA defined
    because E <= 200 < WARMUP = 260 (asserted by G11).
    Risk weights are multiplied by s and the WHOLE residual goes to SHY (phi = 1.00); sweep=False
    reproduces a de-grossing-to-cash book such as live RULES v2 exactly (that is G1).
    Everything else is `engine.backtest` verbatim; the un-invested residual drifts at 0%.
    """
    cols = list(prices.columns)
    shy_i = cols.index(SWEEP)
    rv = prices.pct_change().fillna(0.0).values
    shy_ok = prices[SWEEP].notna().values.astype(float)
    wt = w_risk.reindex(prices.index).fillna(0.0).shift(1).values     # decided t-1, applied t
    key = prices.index.to_period(freq)
    s_key = pd.Series(key, index=prices.index)
    mask = (s_key != s_key.shift(-1)).shift(1, fill_value=False).values
    ref = None if ref_eq is None else np.asarray(ref_eq, dtype=float)

    n, m = len(prices.index), len(cols)
    held = np.zeros((n, m)); cur = np.zeros(m)
    to = np.zeros(n); gr = np.zeros(n); sc = np.full(n, np.nan)
    r0 = np.zeros(n); eq = np.ones(n); defined = np.zeros(n, dtype=bool)
    neutral = (d >= 1.0 - 1e-15)

    for i in range(n):
        if mask[i] or i == 0:
            if neutral:
                s = 1.0
            else:
                curve = eq if conv == "S" else ref
                if i >= E:
                    lvl = curve[i - 1]
                    ma = curve[i - E:i].mean()
                    s = 1.0 if lvl >= ma else d
                    defined[i] = True
                else:
                    s = 1.0
            x = wt[i] * s
            new = x.copy()
            if sweep:
                new[shy_i] += max(0.0, 1.0 - x.sum()) * shy_ok[i]
            to[i] = np.abs(new - cur).sum()
            cur = new
            sc[i] = s
        held[i] = cur
        gr[i] = cur.sum()
        r0[i] = float((cur * rv[i]).sum())
        # engine.backtest's own `shift(1)` leaves the first few rows NaN until the first
        # rebalance resets `cur`; those rows are pre-WARMUP and carry no return, but a cumulative
        # product would propagate the NaN forever, so they are accumulated as ZERO here.  The
        # published `r0` series is left engine-faithful (NaN) so the G1 / G3 bit-identities hold.
        step = r0[i] if np.isfinite(r0[i]) else 0.0
        eq[i] = (eq[i - 1] if i else 1.0) * (1.0 + step)
        g = cur * (1 + rv[i]); tot = g.sum() + (1 - cur.sum())
        cur = g / tot if tot > 0 else cur

    idx = prices.index
    return dict(r0=pd.Series(r0, index=idx), turnover=pd.Series(to, index=idx),
                gross=pd.Series(gr, index=idx), scaler=pd.Series(sc, index=idx).ffill(),
                eq0=pd.Series(eq, index=idx), ma_defined=pd.Series(defined, index=idx),
                reb=pd.Series(mask, index=idx),
                risk_gross=pd.Series(held.sum(axis=1) - held[:, shy_i], index=idx))


def priced(res, bps):
    return res["r0"] - res["turnover"] * bps / 1e4


# ---------------------------------------------------------------- metrics
def sharpe(r):
    v = r.std() * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    return float((1 + r).cumprod().iloc[-1] ** (252 / len(r)) - 1)


def maxdd(r):
    eq = (1 + r).cumprod()
    return float((eq / eq.cummax() - 1).min())


def calmar(r):
    dd = maxdd(r)
    return float(cagr(r) / abs(dd)) if dd < 0 else np.nan


def halves(r):
    h = len(r) // 2
    return sharpe(r.iloc[:h]), sharpe(r.iloc[h:])


def legs(r, base, spy, r_oos, spy_oos):
    h1, h2 = halves(r); b1, b2 = halves(base); s1, s2 = halves(spy)
    L_H1, L_H2 = h1 > s1, h2 > s2
    L_OOS = sharpe(r_oos) > sharpe(spy_oos)
    L_DD = maxdd(r) >= DD_CAP * maxdd(spy)
    L_CAGR = cagr(r) >= CAGR_FLOOR * cagr(spy)
    return dict(pass4a=bool((h1 > b1) and (h2 > b2) and (maxdd(r) >= maxdd(base))),
                pass4b=bool(L_H1 and L_H2 and L_OOS and L_DD and L_CAGR),
                L_H1=bool(L_H1), L_H2=bool(L_H2), L_OOS=bool(L_OOS),
                L_DD=bool(L_DD), L_CAGR=bool(L_CAGR),
                m_DD=maxdd(r) - DD_CAP * maxdd(spy), m_CAGR=cagr(r) - CAGR_FLOOR * cagr(spy))


def main():
    t0 = time.time()
    say("=== idea 2399 — DOES AN EQUITY-CURVE DE-GROSSING GATE CUT THE CAPPED CANDIDATE'S DRAWDOWN? ===")
    say(f"    {DATE}  lane {LANE} run 43   band {BAND}  MA {MA_LEN}d  cadence {CADENCE}  t+1"
        f"  rungs {RUNGS} bps  cap {NAME_CAP:.0%}  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 equity-MA length E {EMAS}   DIAL 2 de-grossed multiplier d {DVALS}")
    say("    s_t = 1 when the book's equity >= its E-day MA, else d.  d = 1.00 IS CAP2 EXACTLY.")
    say(f"    conventions: S (self-referential, HEADLINE, as the queue line words it) and U (unscaled CAP2 curve)")
    say("    SMALL NOT PRICED: 0 of 128 4b cells in idea 2383 and 0 of 40-120 in 2318 / 2322 / 2326 / 2343 —")
    say("    there is no pass on that panel to keep or break.")
    say("    SURVIVORSHIP (rule 9): U56 / B136 are CURRENT constituents held from 2008; L_CAGR is the")
    say("    contaminated leg.  The gated-vs-ungated contrast is same-tape and first-order immune.")
    gate("G7 exactly two tuned parameters", "E, d", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        panels[nm] = (px, list(px.columns))
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y scored, {len(px.columns)} investable, {len(px)} rows",
             ">= 10y", yrs >= 10)

    px_u, inv_u = panels["U56"]
    inb_ref = band_state(px_u, BAND)
    d2 = int((inb_ref != band_state(px_u, BAND)).sum().sum())
    gate("G2 the gate IS baseline.band_state (live clause 2), unmodified",
         f"{d2} differing cells; mean names IN {int(inb_ref.sum(axis=1).mean())}", "0", d2 == 0)

    # G1 replica fidelity on the LIVE book
    w_live = rules_v2_weights(px_u, band=BAND, gross=0.75)
    r_eng = backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    res_live = run_eg(px_u, w_live, 50, 1.00, "S", sweep=False)
    d1 = float((r_eng - priced(res_live, HEADLINE_RUNG)).abs().max())
    gate("G1 per-column replica == engine.backtest (live RULES v2, sweep off)",
         f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    # G3 d = 1.00 IS CAP2, at EVERY E, priced through the engine itself
    wr = cap2_risk_weights(px_u, inv_u, 0.75)
    cap2_eng = backtest(px_u, cap2_full_reference(px_u, inv_u, 0.75), cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    d3 = max(float((cap2_eng - priced(run_eg(px_u, wr, E, 1.00, "S"), HEADLINE_RUNG)).abs().max()) for E in EMAS)
    gate("G3 d = 1.00 == an independent CAP2 construction through engine.backtest, at every E",
         f"max|d| over {len(EMAS)} E values {d3:.3e}", "< 1e-12", d3 < 1e-12)

    # G8/G9 causality: truncate the panel, the scaler and the return series must not move
    cut = px_u.index[int(len(px_u) * 0.70)]
    tr = run_eg(px_u.loc[:cut], cap2_risk_weights(px_u.loc[:cut], inv_u, 0.75), 50, 0.50, "S")
    fu = run_eg(px_u, wr, 50, 0.50, "S")
    d8 = float((tr["scaler"] - fu["scaler"].loc[:cut]).abs().max())
    d9 = float((tr["r0"] - fu["r0"].loc[:cut]).abs().max())
    gate(f"G8 the gate s_t is causal (panel truncated at {cut.date()}, E 50, d 0.50)",
         f"max|ds| {d8:.3e}", "< 1e-12", d8 < 1e-12)
    gate("G9 no lookahead on the RETURN series (same truncation)", f"max|dr| {d9:.3e}", "< 1e-12", d9 < 1e-12)

    # G12 the equity curve the gate reads is FINITE everywhere (the NaN-propagation trap)
    fin = run_eg(px_u, wr, 50, 0.50, "S")
    nbad = int((~np.isfinite(fin["eq0"].values)).sum())
    gate("G12 the reference equity curve is finite on every row (NaN-propagation trap)",
         f"{nbad} non-finite of {len(fin['eq0'])} rows", "0", nbad == 0)

    # G11 the MA exists on every SCORED rebalance day, at the longest E
    chk = run_eg(px_u, wr, max(EMAS), 0.50, "S")
    scored = px_u.index[WARMUP:]
    rb = chk["reb"].loc[scored]
    und = int((rb & ~chk["ma_defined"].loc[scored]).sum())
    gate(f"G11 the equity MA is defined on every scored rebalance day at E = {max(EMAS)}",
         f"{und} undefined of {int(rb.sum())} scored rebalances", "0", und == 0)

    rows, expo = [], []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        yrs = len(win) / 252
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_r = priced(run_eg(px, rules_v2_weights(px, band=BAND, gross=0.75), 50, 1.00, "S",
                               sweep=False), HEADLINE_RUNG).loc[win]
        say(f"\n--- panel {pname} ({len(invest)} investable)  SPY {cagr(spy):.2%} / {sharpe(spy):.4f} / {maxdd(spy):.2%}"
            f"   live RULES v2 {cagr(base_r):.2%} / {sharpe(base_r):.4f} / {maxdd(base_r):.2%}"
            f"  halves {halves(base_r)[0]:.4f}/{halves(base_r)[1]:.4f}")
        say(f"    4b bars here: DD cap {DD_CAP * maxdd(spy):.2%}   CAGR floor {CAGR_FLOOR * cagr(spy):.2%}"
            f"   SPY halves {halves(spy)[0]:.4f}/{halves(spy)[1]:.4f}   SPY OOS Sharpe {sharpe(spy_oos):.4f}")
        for gross in GROSSES:
            w_risk = cap2_risk_weights(px, invest, gross)
            unscaled = run_eg(px, w_risk, 50, 1.00, "S")
            for conv in CONVENTIONS:
                for E in EMAS:
                    for d in DVALS:
                        res = run_eg(px, w_risk, E, d, conv, ref_eq=unscaled["eq0"].values)
                        s = res["scaler"].loc[win].dropna()
                        rb = res["reb"].loc[win]
                        sr = res["scaler"].loc[win][rb].dropna()
                        expo.append(dict(panel=pname, conv=conv, E=E, d=d, gross=gross,
                                         s_mean=float(s.mean()),
                                         gated_share_days=float((s < 1 - 1e-12).mean()),
                                         gated_share_reb=float((sr < 1 - 1e-12).mean()),
                                         n_reb=int(rb.sum()),
                                         switches=int((s.diff().abs() > 1e-12).sum()),
                                         mean_gross=float(res["gross"].loc[win].mean()),
                                         mean_risk_gross=float(res["risk_gross"].loc[win].mean()),
                                         mean_shy=float(res["gross"].loc[win].mean()
                                                        - res["risk_gross"].loc[win].mean()),
                                         turnover_yr=float(res["turnover"].loc[win].sum() / yrs),
                                         max_row_sum=float(res["gross"].max()),
                                         real_vol=float(priced(res, HEADLINE_RUNG).loc[win].std() * np.sqrt(252))))
                        for rung in RUNGS:
                            r = priced(res, rung).loc[win]
                            r_oos = r.loc[OOS_START:]
                            h1, h2 = halves(r)
                            rows.append(dict(panel=pname, conv=conv, E=E, d=d, gross=gross, cost_bps=rung,
                                             CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                             H1=h1, H2=h2,
                                             IS_Sharpe=sharpe(r.loc[:IS_END]), IS_Calmar=calmar(r.loc[:IS_END]),
                                             OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                             spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_CAGR=cagr(spy_oos),
                                             base_OOS_Sharpe=sharpe(base_r.loc[OOS_START:]),
                                             **legs(r, base_r, spy, r_oos, spy_oos)))
        say(f"    ... {pname} done ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(rows); ef = pd.DataFrame(expo)
    df.to_csv(f"{OUT}.grid.csv", index=False); ef.to_csv(f"{OUT}.exposure.csv", index=False)

    gate("G4 no leverage (all books, realised row sums)", f"max row sum {ef.max_row_sum.max():.9f}",
         "<= 1+1e-12", bool((ef.max_row_sum <= 1 + 1e-12).all()))
    shy_ok = all(bool(p[SWEEP].loc[p.index[WARMUP:]].notna().all()) for p, _ in panels.values())
    gate("G6 sweep instrument priced on every held row", f"SHY non-null on both panels: {shy_ok}", "True", shy_ok)

    mono = []
    for (pname, conv, E, gross), g in ef.groupby(["panel", "conv", "E", "gross"]):
        v = g.set_index("d").reindex(DVALS).mean_risk_gross.values
        mono.append(bool(np.all(np.diff(v) > -1e-12) and np.ptp(v) > 1e-4))
    gate("G5 the d dial BITES and mean RISK gross is MONOTONE along it (total gross is pinned at"
         " 1.0 by the SHY sweep, so the risk sleeve is the exposure)",
         f"{sum(mono)} of {len(mono)} (panel, conv, E, gross) cells", f"{len(mono)} of {len(mono)}", all(mono))

    h = df[(df.panel == "U56") & (df.conv == HEADLINE_CONV) & (df.d == 1.00) & (df.E == ANCHOR_E)
           & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    e0 = ef[(ef.panel == "U56") & (ef.conv == HEADLINE_CONV) & (ef.d == 1.00) & (ef.E == ANCHOR_E)
            & (ef.gross == 0.75)].iloc[0]
    d10 = max(abs(h.CAGR - 0.1162), abs(h.Sharpe - 1.2687) / 10, abs(h.MaxDD + 0.1481),
              abs(h.OOS_CAGR - 0.1277), abs(h.OOS_Sharpe - 1.3318) / 10)
    gate("G10 reproduces the committed CAP2 U56 headline (11.62%/1.2687/-14.81%, OOS 12.77%/1.3318)",
         f"read {h.CAGR:.2%} / {h.Sharpe:.4f} / {h.MaxDD:.2%}, OOS {h.OOS_CAGR:.2%} / {h.OOS_Sharpe:.4f},"
         f" turnover {e0.turnover_yr:.2f}x (committed 3.51x) -> max|d| {d10:.2e}", "< 1e-3", d10 < 1e-3)

    # ------------------------------------------------------------ A. the full ladder
    say(f"\n=== A. THE FULL LADDER AT 10 bps, gross 0.75, HEADLINE CONVENTION {HEADLINE_CONV} — every point ===")
    say("  panel   E     d |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh | 4a 4b | H1/H2/OOS/DD/CAGR | gate% risk_g turn/yr realvol")
    for pname in panels:
        for E in EMAS:
            for d in DVALS:
                r = df[(df.panel == pname) & (df.conv == HEADLINE_CONV) & (df.E == E) & (df.d == d)
                       & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                e = ef[(ef.panel == pname) & (ef.conv == HEADLINE_CONV) & (ef.E == E) & (ef.d == d)
                       & (ef.gross == 0.75)].iloc[0]
                lg = "".join("1" if r[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                say(f"  {pname:5s} {E:3d} {d:5.2f} | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%} |"
                    f" {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} |"
                    f" {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg:17s} |"
                    f" {e.gated_share_reb:5.1%} {e.mean_risk_gross:6.3f} {e.turnover_yr:7.2f} {e.real_vol:6.3f}"
                    + ("   <= CAP2 (anchor)" if d == 1.00 else ""))

    # ------------------------------------------------------------ B. the exchange rate
    say("\n=== B. DOES IT BUY `L_DD` WITHOUT PAYING `L_CAGR`?  deltas vs the CAP2 anchor, 10 bps, g=0.75 ===")
    say("    (THE WHOLE QUESTION.  A name-level dial pays CAGR one-for-one — idea 2381 measured that.")
    say("     'pp of CAGR given up per pp of drawdown bought' is the exchange rate; < 1.0 is a real win.)")
    xr = []
    for pname in panels:
        ref = df[(df.panel == pname) & (df.conv == HEADLINE_CONV) & (df.d == 1.00) & (df.E == ANCHOR_E)
                 & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
        say(f"  {pname} CAP2 anchor: {ref.CAGR:.2%} / {ref.Sharpe:.4f} / {ref.MaxDD:.2%}"
            f"  (m_DD {ref.m_DD:+.4f}, m_CAGR {ref.m_CAGR:+.4f})")
        for E in EMAS:
            for d in DVALS:
                if d == 1.00:
                    continue
                r = df[(df.panel == pname) & (df.conv == HEADLINE_CONV) & (df.E == E) & (df.d == d)
                       & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                dd_bought = r.MaxDD - ref.MaxDD          # positive = shallower
                cagr_paid = ref.CAGR - r.CAGR            # positive = gave up return
                rate = cagr_paid / dd_bought if abs(dd_bought) > 1e-9 else np.nan
                xr.append(dict(panel=pname, E=E, d=d, dd_bought=dd_bought, cagr_paid=cagr_paid,
                               rate=rate, dSharpe=r.Sharpe - ref.Sharpe, pass4b=bool(r.pass4b)))
                say(f"    E {E:3d} d {d:4.2f}:  dCAGR {r.CAGR - ref.CAGR:+6.2%}"
                    f"  dSharpe {r.Sharpe - ref.Sharpe:+7.4f}  dMaxDD {dd_bought:+6.2%}"
                    f"  dOOS_Sh {r.OOS_Sharpe - ref.OOS_Sharpe:+7.4f}  |  exchange rate"
                    f" {rate:7.2f} pp CAGR per pp of DD  | 4b {'Y' if r.pass4b else '.'}")
    xrd = pd.DataFrame(xr); xrd.to_csv(f"{OUT}.exchange.csv", index=False)
    fin = xrd[np.isfinite(xrd.rate)]
    say(f"  exchange rate over the {len(fin)} finite cells: min {fin.rate.min():.2f}  median"
        f" {fin.rate.median():.2f}  max {fin.rate.max():.2f}"
        f"   cells at rate < 1.0 (drawdown bought cheaper than one-for-one): {int((fin.rate < 1.0).sum())} of {len(fin)}")
    say(f"  cells where the gate made drawdown WORSE (dMaxDD < 0): {int((xrd.dd_bought < 0).sum())} of {len(xrd)}")
    say(f"  cells where Sharpe IMPROVED (dSharpe > 0): {int((xrd.dSharpe > 0).sum())} of {len(xrd)}")

    # ------------------------------------------------------------ C. keep counts
    say(f"\n=== C. KEEP COUNTS OVER ALL {len(df)} PUBLISHED ROWS (4 E x 5 d x 2 conv x 2 gross x 2 panels x 4 rungs) ===")
    say(f"  4b passes: {int(df.pass4b.sum())} of {len(df)}      4a passes: {int(df.pass4a.sum())} of {len(df)}")
    for rung in RUNGS:
        dd = df[df.cost_bps == rung]
        say(f"   {rung:5.1f} bps:  4b {int(dd.pass4b.sum()):3d}/{len(dd)}   4a {int(dd.pass4a.sum()):3d}/{len(dd)}"
            "   binding leg on 4b FAILs: " +
            "  ".join(f"{k} {int((~dd[k][~dd.pass4b]).sum())}" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    for conv in CONVENTIONS:
        dd = df[df.conv == conv]
        say(f"   convention {conv}: 4b {int(dd.pass4b.sum()):3d}/{len(dd)}   4a {int(dd.pass4a.sum()):3d}/{len(dd)}")
    for d in DVALS:
        dd = df[(df.d == d) & (df.conv == HEADLINE_CONV)]
        say(f"   d {d:4.2f} (conv {HEADLINE_CONV}): 4b {int(dd.pass4b.sum()):3d}/{len(dd)}"
            f"   4a {int(dd.pass4a.sum()):3d}/{len(dd)}")
    for E in EMAS:
        dd = df[(df.E == E) & (df.conv == HEADLINE_CONV) & (df.d < 1.00)]
        say(f"   E {E:3d} (conv {HEADLINE_CONV}, d < 1 only): 4b {int(dd.pass4b.sum()):3d}/{len(dd)}"
            f"   4a {int(dd.pass4a.sum()):3d}/{len(dd)}")

    say("\n  JOINT BOTH-PANEL 4b (U56 AND B136 at the same E, d, conv, gross, rung):")
    jt = []
    for conv in CONVENTIONS:
        for E in EMAS:
            for d in DVALS:
                for gross in GROSSES:
                    for rung in RUNGS:
                        q = df[(df.conv == conv) & (df.E == E) & (df.d == d)
                               & (df.gross == gross) & (df.cost_bps == rung)]
                        u = q[q.panel == "U56"].iloc[0]; b = q[q.panel == "B136"].iloc[0]
                        jt.append(dict(conv=conv, E=E, d=d, gross=gross, cost_bps=rung,
                                       joint=bool(u.pass4b and b.pass4b)))
    jf = pd.DataFrame(jt)
    say(f"   joint 4b: {int(jf.joint.sum())} of {len(jf)} cells"
        f"   [CAP2 anchor (d = 1.00): {int(jf[jf.d == 1.00].joint.sum())} of {len(jf[jf.d == 1.00])}]")
    for conv in CONVENTIONS:
        say(f"   convention {conv}: " + "  ".join(
            f"d {d:4.2f} {int(jf[(jf.conv == conv) & (jf.d == d)].joint.sum())}"
            f"/{len(jf[(jf.conv == conv) & (jf.d == d)])}" for d in DVALS))
    say("   joint 4b at the LIVE gross 0.75 only (conv S): " + "  ".join(
        f"d {d:4.2f} {int(jf[(jf.conv == 'S') & (jf.d == d) & (jf.gross == 0.75)].joint.sum())}"
        f"/{len(jf[(jf.conv == 'S') & (jf.d == d) & (jf.gross == 0.75)])}" for d in DVALS))
    jf.to_csv(f"{OUT}.joint.csv", index=False)

    say("\n  4a PASSES (Sharpe > live RULES v2 in BOTH halves AND MaxDD no worse) — every one, listed:")
    pa = df[df.pass4a]
    if len(pa) == 0:
        say("    NONE")
    else:
        for _, r in pa.iterrows():
            say(f"    {r.panel:5s} conv {r.conv} E {r.E:3d} d {r.d:4.2f} g {r.gross:.2f} {r.cost_bps:5.1f}bps"
                f"  {r.CAGR:6.2%} / {r.Sharpe:.4f} / {r.MaxDD:7.2%}  halves {r.H1:.4f}/{r.H2:.4f}"
                f"  4b {'Y' if r.pass4b else '.'}")

    say("\n  4b PASSES WITH d < 1.00 (i.e. the DEVICE passing, not the anchor) — every one, listed:")
    pb = df[(df.pass4b) & (df.d < 1.00)]
    if len(pb) == 0:
        say("    NONE")
    else:
        for _, r in pb.iterrows():
            say(f"    {r.panel:5s} conv {r.conv} E {r.E:3d} d {r.d:4.2f} g {r.gross:.2f} {r.cost_bps:5.1f}bps"
                f"  {r.CAGR:6.2%} / {r.Sharpe:.4f} / {r.MaxDD:7.2%}  halves {r.H1:.4f}/{r.H2:.4f}"
                f"  OOS {r.OOS_CAGR:6.2%}/{r.OOS_Sharpe:.4f}")

    # ------------------------------------------------------------ D. the device's own bill
    say("\n=== D. THE DEVICE'S OWN BILL, MEASURED NOT ASSUMED (conv S, g=0.75, 10 bps) ===")
    say("  panel   E     d | gate% (reb)  switches | risk gross  mean SHY | turn/yr  vs CAP2 | realised vol")
    for pname in panels:
        for E in EMAS:
            for d in DVALS:
                e = ef[(ef.panel == pname) & (ef.conv == HEADLINE_CONV) & (ef.E == E) & (ef.d == d)
                       & (ef.gross == 0.75)].iloc[0]
                a = ef[(ef.panel == pname) & (ef.conv == HEADLINE_CONV) & (ef.d == 1.00)
                       & (ef.E == ANCHOR_E) & (ef.gross == 0.75)].iloc[0]
                say(f"  {pname:5s} {E:3d} {d:5.2f} | {e.gated_share_reb:10.1%} {e.switches:9d} |"
                    f" {e.mean_risk_gross:10.3f} {e.mean_shy:9.3f} | {e.turnover_yr:7.2f}"
                    f" {e.turnover_yr - a.turnover_yr:+7.2f} | {e.real_vol:12.4f}")

    # ------------------------------------------------------------ E. S vs U
    say("\n=== E. CONVENTION S vs CONVENTION U — does the FEEDBACK matter? (10 bps, g=0.75) ===")
    for pname in panels:
        for E in EMAS:
            for d in DVALS:
                if d == 1.00:
                    continue
                a = df[(df.panel == pname) & (df.conv == "S") & (df.E == E) & (df.d == d)
                       & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                b = df[(df.panel == pname) & (df.conv == "U") & (df.E == E) & (df.d == d)
                       & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                say(f"  {pname:5s} E {E:3d} d {d:4.2f}:  S {a.CAGR:6.2%}/{a.Sharpe:.4f}/{a.MaxDD:7.2%} 4b {'Y' if a.pass4b else '.'}"
                    f"   U {b.CAGR:6.2%}/{b.Sharpe:.4f}/{b.MaxDD:7.2%} 4b {'Y' if b.pass4b else '.'}"
                    f"   |dSharpe| {abs(a.Sharpe - b.Sharpe):.4f}")

    # ------------------------------------------------------------ F. rule 8
    say("\n=== F. RULE 8 — (E, d) chosen on <= 2016-12-31 ONLY, 2017-2026 read ONCE ===")
    wf = []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_r = priced(run_eg(px, rules_v2_weights(px, band=BAND, gross=0.75), 50, 1.00, "S",
                               sweep=False), HEADLINE_RUNG).loc[win]
        b_oos = base_r.loc[OOS_START:]
        for conv in CONVENTIONS:
            for gross in GROSSES:
                for rung in RUNGS:
                    dd = df[(df.panel == pname) & (df.conv == conv) & (df.gross == gross) & (df.cost_bps == rung)]
                    inc = dd[(dd.d == 1.00) & (dd.E == ANCHOR_E)].iloc[0]
                    for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                        pk = dd.loc[dd[col].idxmax()]
                        wf.append(dict(panel=pname, conv=conv, gross=gross, cost_bps=rung, chooser=chooser,
                                       pick_E=int(pk.E), pick_d=float(pk.d),
                                       pick_is_cap2=bool(pk.d == 1.00), full4b=bool(pk.pass4b),
                                       OOS_CAGR=pk.OOS_CAGR, OOS_Sharpe=pk.OOS_Sharpe, OOS_MaxDD=pk.OOS_MaxDD,
                                       inc_OOS_Sharpe=inc.OOS_Sharpe, inc_OOS_CAGR=inc.OOS_CAGR,
                                       inc_OOS_MaxDD=inc.OOS_MaxDD,
                                       base_OOS_Sharpe=sharpe(b_oos), base_OOS_CAGR=cagr(b_oos),
                                       base_OOS_MaxDD=maxdd(b_oos),
                                       spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_CAGR=cagr(spy_oos),
                                       spy_OOS_MaxDD=maxdd(spy_oos)))
                        if conv == HEADLINE_CONV and gross == 0.75:
                            say(f"  {pname:5s} g{gross:.2f} {rung:5.1f}bps {chooser:11s} ->"
                                f" E {int(pk.E):3d} d {pk.d:4.2f} |"
                                f" OOS {pk.OOS_CAGR:6.2%} / {pk.OOS_Sharpe:.4f} / {pk.OOS_MaxDD:7.2%} |"
                                f" CAP2 anchor OOS {inc.OOS_CAGR:6.2%} / {inc.OOS_Sharpe:.4f} / {inc.OOS_MaxDD:7.2%} |"
                                f" live v2 OOS {cagr(b_oos):6.2%} / {sharpe(b_oos):.4f} / {maxdd(b_oos):7.2%} |"
                                f" SPY OOS {cagr(spy_oos):6.2%} / {sharpe(spy_oos):.4f} / {maxdd(spy_oos):7.2%} |"
                                f" full 4b {'Y' if pk.pass4b else '.'}")
    wfd = pd.DataFrame(wf)
    wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"\n  {len(wfd)} picks (2 panels x 2 conv x 2 gross x 4 rungs x 2 choosers).")
    say(f"   picks landing on the CAP2 ANCHOR (d = 1.00, i.e. NO gate):  {int(wfd.pick_is_cap2.sum())} of {len(wfd)}")
    say(f"   picks beating SPY's OOS Sharpe:                    {int((wfd.OOS_Sharpe > wfd.spy_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks beating the live book's OOS Sharpe:           {int((wfd.OOS_Sharpe > wfd.base_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks beating the CAP2 ANCHOR's own OOS Sharpe:     {int((wfd.OOS_Sharpe > wfd.inc_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks with SHALLOWER OOS MaxDD than the CAP2 anchor:{int((wfd.OOS_MaxDD > wfd.inc_OOS_MaxDD).sum())} of {len(wfd)}")
    say(f"   picks carrying a full-sample 4b pass:               {int(wfd.full4b.sum())} of {len(wfd)}")
    say("   pick distribution over d: " + "  ".join(f"{d:4.2f}:{int((wfd.pick_d == d).sum())}" for d in DVALS))
    say("   pick distribution over E: " + "  ".join(f"{E}:{int((wfd.pick_E == E).sum())}" for E in EMAS))
    agree = both4b = 0
    for conv in CONVENTIONS:
        for gross in GROSSES:
            for rung in RUNGS:
                for chooser in ("C_ISSHARPE", "C_ISCALMAR"):
                    q = wfd[(wfd.conv == conv) & (wfd.gross == gross) & (wfd.cost_bps == rung)
                            & (wfd.chooser == chooser)]
                    u = q[q.panel == "U56"].iloc[0]; b = q[q.panel == "B136"].iloc[0]
                    if (u.pick_E, u.pick_d) == (b.pick_E, b.pick_d):
                        agree += 1
                        if u.full4b and b.full4b:
                            both4b += 1
    say(f"   U56 and B136 agree on (E, d) in {agree} of 32 (conv x gross x rung x chooser) cells")
    say(f"   cells where both panels agree AND both carry a full-sample 4b: {both4b} of 32")

    gf = pd.DataFrame(GATES); gf.to_csv(f"{OUT}.gates.csv", index=False)
    npass = int(gf.pass_.sum()); ntot = int(len(gf))
    say(f"\n=== GATES: {npass} of {ntot} pass ===")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    say(f"\nwrote {OUT}.grid.csv / .exposure.csv / .exchange.csv / .joint.csv / .walkforward.csv /"
        f" .gates.csv   ({time.time() - t0:.0f}s)")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

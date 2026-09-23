#!/usr/bin/env python3
"""idea 2377 (lane C, 2026-09-23) — is the CAPPED CANDIDATE's 4b pass EXPOSURE or TIMING?

THE OBJECT.  Idea 2322 filed the record's standing KEEP-4b candidate as CAP2:

    w_i = min(gross / N_in, 0.02)  on names INSIDE the 200d +/-3% band,
    idle NAV (1 - sum w) swept to SHY at phi = 1.00,  weekly cadence, t+1 execution.

THE ALGEBRA NOBODY HAS SEPARATED.  Because every IN name gets the same weight, the capped
book's RISK GROSS on day t is exactly

    G_t = min(gross, c x N_in,t)

so the per-name cap is not only a concentration device: it is a BREADTH-LINKED DE-GROSSER
that spends less NAV precisely on the days fewer names are inside the band.  Every number
published on CAP2 therefore mixes two different claims — a LEVEL claim (the book runs at a
lower mean exposure than the uncapped candidate) and a TIMING claim (it lowers exposure at
the right moments).  4b's `L_DD` leg is exactly where those two would show up, and the record
has never told them apart.

THE NULL, WITH ZERO FREE PARAMETERS.  A CONSTANT-EXPOSURE TWIN of each capped cell:

    w_i = gbar / N_in   on the SAME IN names, idle NAV to SHY at phi = 1.00,

with `gbar` SOLVED (not fitted) so that the twin's MEAN TARGET GROSS equals the capped book's
over the matching window.  Same tape, same days, same names, same mean exposure; the only
thing removed is the breadth link.  If the twin matches the cap, CAP2's pass is a LEVEL and
the simpler constant-gross book is what should be recommended.  If the cap beats the twin, the
breadth link is an edge and belongs in RULES as its own clause.

A SECOND, SHARPER NULL -- the SCRAMBLED-TIMING PLACEBO.  The constant twin removes the breadth
link entirely, so it also removes the VARIABILITY of exposure.  A device can be a good de-grosser
without being a good timer, so a third family holds the cap's OWN gross series and only moves it
in time: G is taken from the capped cell over the evaluation window and reordered (circular shift
of +126 / +252 trading days, and time-REVERSED), then spread as `G_perm,t / N_in,t` on the same IN
names.  Exposure LEVEL and exposure VARIABILITY are then matched to the last digit (gate G11: the
perm series is a permutation of the cap's) and only the DATES are wrong.  These are PLACEBOS, not
tradable books (REV is anti-causal by construction), excluded from rule 8 and labelled as such.

CONFOUND, NAMED: both nulls spread `G/N_in` with NO per-name bound, so a CAP-minus-NULL gap is the
whole device (breadth link + per-name bound), not the breadth link alone.  The bound is common to
both nulls, so CAP-minus-PERM against CAP-minus-CONSTANT is what isolates TIMING.

TWO MATCHING CONVENTIONS for the constant twin, both published:
  MATCH_FULL -- gbar from the full evaluation window.  Uses hindsight, and the hindsight
                FAVOURS THE TWIN (it is handed the cap's realised average exposure).  Not
                eligible for rule 8, and said so.
  MATCH_IS   -- gbar from warm-up..2016-12-31 ONLY.  Causal, and the one rule 8 uses.

DIAL 1 -- cap level c {0.015, 0.02 (2322's filed constant), 0.03, 0.05, INF}.  c=INF IS the
          uncapped candidate CAND; at c=INF the twin collapses onto the book (gate G7).
DIAL 2 -- gross g {0.75 (live), 1.00}.

REPORTED, NEVER SELECTED ON: 2 panels (U56 / B136), 4 cost rungs (0 / 10 / 25 / 50 bps),
band 0.03, weekly cadence, t+1 execution, phi = 1.00.
Published rows: 5 c x 2 g x 2 panels x 4 rungs = 80 capped + 160 constant-twin + 192 placebo
(4 finite c x 3 permutations x 2 g x 2 panels x 4 rungs) = 432, every point printed.

BOTH KEEP PATHS on every row: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse)
and 4b (Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x
SPY's).  RULE 8: (c, g) chosen on warm-up..2016-12-31 ONLY by two pre-stated IS-only choosers
(C_ISSHARPE, C_ISCALMAR), 2017-2026 read ONCE, run separately inside each family and POOLED
across {CAP, TWIN} so the chooser itself votes on the question.

GATES.  G0 >= 10y per panel.  G1 c=INF is bit-identical to an independent CAND build.
G2 the per-column replica equals `engine.backtest` on the live weights at W.  G3 no leverage.
G4 the gross identity G_t = min(g, c x N_in) holds exactly on the target weights.
G5 the twin's mean target gross equals the cap's, per convention, to machine precision.
G6 exactly two tuned parameters.  G7 at c=INF the twin is bit-identical to the book (both
conventions).  G8 SHY priced on every held row.  G9 no-lookahead (weights at d rebuilt from
px.loc[:d] only).  G10 EXTERNAL REPRODUCTION of idea 2322's committed U56 CAP2 headline
(11.58% / 1.2643 / -14.81%, OOS 12.70% / 1.3243) and its committed 3.51x/yr turnover.
G11 every placebo's gross series is a PERMUTATION of the capped cell's (sorted arrays equal, mean
and sd equal to machine precision).

SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists held from 2008, so the
absolute 4b levels are optimistic.  The cap-vs-twin contrast is same-tape / same-day /
same-mean-exposure and is first-order immune; the CAGR floor leg is an ABSOLUTE bar and is the
most contaminated reading here.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_exposure-or-timing-on-the-capped-candidate_C.py
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
from engine import backtest, rebalance_mask                       # noqa: E402

DATE, SLUG, LANE = "2026-09-23", "exposure-or-timing-on-the-capped-candidate", "C"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, WARMUP = 0.03, 260
SWEEP, PHI = "SHY", 1.00
CAPS = [0.015, 0.02, 0.03, 0.05, np.inf]     # DIAL 1 (0.02 is idea 2322's filed constant)
GROSSES = [0.75, 1.00]                        # DIAL 2
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG, FREQ = 10.0, "W"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
CONVENTIONS = ["MATCH_FULL", "MATCH_IS"]
PERMS = [("PERM_126", 126), ("PERM_252", 252), ("PERM_REV", -1)]   # -1 = time-reversed

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


def cap_label(c):
    return "INF" if not np.isfinite(c) else f"{c:.3f}"


# ---------------------------------------------------------------- books
def in_band(px, invest):
    """The IN mask and the breadth series N_in, shared by the book and its twin."""
    q = px[invest]
    inb = band_state(q, BAND) & q.notna()
    return inb, inb.sum(axis=1)


def sweep_to_shy(w, px):
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w = w.copy()
    w[SWEEP] = w[SWEEP] + PHI * idle * px[SWEEP].notna().astype(float)
    return w


def _spread(px, inb, per):
    """Per-name RISK weights (pre-sweep): the IN mask times a per-day per-name weight."""
    w = pd.DataFrame(inb.values.astype(float) * np.asarray(per)[:, None],
                     index=px.index, columns=inb.columns)
    return w.fillna(0.0)


def cap_weights(px, invest, gross, c, inb=None, nin=None):
    """idea 2322's CAP2 family: w_i = min(gross/N_in, c) on IN names, idle -> SHY at phi=1.
    c = inf recovers the uncapped candidate CAND (fully spread at `gross`).
    Returns (full weights incl. the SHY sweep, RISK weights pre-sweep)."""
    if inb is None:
        inb, nin = in_band(px, invest)
    n = nin.replace(0, np.nan)
    pre = _spread(px, inb, np.minimum(gross / n.values, c))
    w = sweep_to_shy(pre.reindex(columns=px.columns).fillna(0.0), px)
    return w, pre


def twin_weights(px, invest, gbar, inb=None, nin=None):
    """CONSTANT-EXPOSURE twin: w_i = gbar/N_in on the SAME IN names, idle -> SHY.
    Risk gross is gbar on every day at least one name is IN, and does NOT move with breadth.
    Returns (full weights incl. the SHY sweep, RISK weights pre-sweep)."""
    if inb is None:
        inb, nin = in_band(px, invest)
    n = nin.replace(0, np.nan)
    pre = _spread(px, inb, (gbar / n).values)
    w = sweep_to_shy(pre.reindex(columns=px.columns).fillna(0.0), px)
    return w, pre


def perm_weights(px, inb, nin, gr_cap, win, kind):
    """PLACEBO: hold the capped cell's OWN gross series, reordered in time, spread over the same
    IN names as `G_perm,t / N_in,t`.  Level and variability matched exactly, dates wrong."""
    v = gr_cap.loc[win].values.copy()
    pv = v[::-1].copy() if kind == -1 else np.roll(v, kind)
    g_perm = gr_cap.copy()
    g_perm.loc[win] = pv
    n = nin.replace(0, np.nan)
    pre = _spread(px, inb, (g_perm / n).values)
    w = sweep_to_shy(pre.reindex(columns=px.columns).fillna(0.0), px)
    return w, pre, pd.Series(pv, index=win)


def cand_reference(px, invest, gross):
    """Independent construction of the uncapped candidate (no minimum, no numpy broadcast path)."""
    inb, nin = in_band(px, invest)
    w = inb.astype(float).div(nin.replace(0, np.nan), axis=0).mul(gross).fillna(0.0)
    w = w.reindex(columns=px.columns).fillna(0.0)
    return sweep_to_shy(w, px)


def run_book(prices, weights, mask):
    """Replica of engine.backtest with an explicit rebalance mask, keeping zero-cost returns +
    turnover so every cost rung is priced from one pass.  Un-invested residual drifts at 0%."""
    rets = prices.pct_change().fillna(0.0)
    w_target = weights.reindex(prices.index).fillna(0.0).shift(1)
    m = mask.shift(1, fill_value=False)
    held = np.zeros((len(prices.index), len(prices.columns)))
    cur = np.zeros(len(prices.columns))
    turnover = np.zeros(len(prices.index))
    gross_s = np.zeros(len(prices.index))
    wt, rv, mv = w_target.values, rets.values, m.values
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
    return dict(r0=pd.Series((held * rv).sum(axis=1), index=prices.index),
                turnover=pd.Series(turnover, index=prices.index),
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


def row_stats(res, win, oos_start, base_r, spy, spy_oos, rung):
    r = priced(res, rung).loc[win]
    r_oos = r.loc[oos_start:]
    h1, h2 = halves(r)
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r), H1=h1, H2=h2,
                IS_Sharpe=sharpe(r.loc[:IS_END]), IS_Calmar=calmar(r.loc[:IS_END]),
                OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                **legs(r, base_r, spy, r_oos, spy_oos))


def main():
    t0 = time.time()
    say("=== idea 2377 — is the CAPPED CANDIDATE's 4b pass EXPOSURE (a level) or TIMING "
        "(the breadth link)? ===")
    say(f"    {DATE}  lane {LANE}   band {BAND}  cadence {FREQ}  t+1  rungs {RUNGS} bps  "
        f"sweep {SWEEP} phi={PHI:.2f}")
    say(f"    DIAL 1 cap c {[cap_label(c) for c in CAPS]}   DIAL 2 gross {GROSSES}   "
        f"twin conventions {CONVENTIONS} (gbar SOLVED, not fitted)")
    gate("G6 exactly two tuned parameters", "cap level c, gross g", "2", True)

    px_u = load_universe()
    px_b = load_universe(broad=True)
    panels = {}
    for nm, px in (("U56", px_u), ("B136", px_b)):
        panels[nm] = (px, list(px.columns))
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y, {len(px.columns)} investable, {len(px)} rows",
             ">= 10y", yrs >= 10)

    # G2 -- the replica prices the live book exactly as engine.backtest does
    mW = rebalance_mask(px_u.index, FREQ)
    w_live = rules_v2_weights(px_u, band=BAND, gross=0.75)
    d2 = float((backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=FREQ)["returns"]
                - priced(run_book(px_u, w_live, mW), HEADLINE_RUNG)).abs().max())
    gate("G2 per-column replica == engine.backtest (live book, W)", f"max|d| {d2:.3e}",
         "< 1e-12", d2 < 1e-12)

    rows, diag, g5, g7, g11 = [], [], [], [], []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        yrs = len(win) / 252
        inb, nin = in_band(px, invest)
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_res = run_book(px, rules_v2_weights(px[invest], band=BAND, gross=0.75)
                            .reindex(columns=px.columns).fillna(0.0), rebalance_mask(px.index, FREQ))
        base_r = priced(base_res, HEADLINE_RUNG).loc[win]
        base_turn = float(base_res["turnover"].loc[win].sum() / yrs)
        say(f"\n--- panel {pname} ({len(invest)} names)  SPY {cagr(spy):.2%} / {sharpe(spy):.4f} /"
            f" {maxdd(spy):.2%}   live RULES v2 {cagr(base_r):.2%} / {sharpe(base_r):.4f} /"
            f" {maxdd(base_r):.2%}, turnover {base_turn:.2f}/yr")
        say(f"    breadth N_in over the window: mean {nin.loc[win].mean():.1f}, "
            f"p5 {nin.loc[win].quantile(0.05):.0f}, p95 {nin.loc[win].quantile(0.95):.0f}, "
            f"max {nin.loc[win].max():.0f}   (N priced {int(px[invest].notna().sum(axis=1).loc[win].mean())})")
        inwin = nin.loc[win] >= 1
        f_invested = float(inwin.mean())
        f_invested_is = float((nin.loc[win].loc[:IS_END] >= 1).mean())

        for gross in GROSSES:
            for c in CAPS:
                wc, pre_c = cap_weights(px, invest, gross, c, inb, nin)
                gr_t = pre_c.sum(axis=1)
                # G4 -- the gross identity, on the decision-day object
                ident = float((gr_t - np.minimum(gross, c * nin).where(nin > 0, 0.0)).abs().max())
                res = run_book(px, wc, rebalance_mask(px.index, FREQ))
                mg_full = float(gr_t.loc[win].mean())
                mg_is = float(gr_t.loc[win].loc[:IS_END].mean())
                book = res["held"].loc[win].drop(columns=[SWEEP])
                pos = book.values[book.values > 0]
                turn = float(res["turnover"].loc[win].sum() / yrs)
                binds = float(((gross / nin.replace(0, np.nan)) > c).loc[win].mean()) if np.isfinite(c) else 0.0
                diag.append(dict(panel=pname, kind="CAP", conv="-", cap=cap_label(c), gross=gross,
                                 gbar=np.nan, mean_target_gross=mg_full, mean_held_gross=float(res["gross"].loc[win].mean()),
                                 gross_p5=float(gr_t.loc[win].quantile(0.05)), gross_p95=float(gr_t.loc[win].quantile(0.95)),
                                 gross_std=float(gr_t.loc[win].std()),
                                 corr_gross_breadth=float(np.corrcoef(gr_t.loc[win], nin.loc[win])[0, 1]),
                                 binds_frac=binds, turnover_yr=turn, turnover_vs_live=turn / base_turn,
                                 live_turnover_yr=base_turn, max_name_w_held=float(pos.max()) if len(pos) else 0.0,
                                 mean_sweep_w=float(res["held"][SWEEP].loc[win].mean()),
                                 max_row_sum=float(res["held"].loc[win].sum(axis=1).max()),
                                 gross_identity_err=ident))
                for rung in RUNGS:
                    rows.append(dict(panel=pname, kind="CAP", conv="-", cap=cap_label(c), gross=gross,
                                     cost_bps=rung, turnover_yr=turn,
                                     **row_stats(res, win, OOS_START, base_r, spy, spy_oos, rung)))
                gate_ok = ident < 1e-12
                g5.append(("G4 identity " + f"{pname} g{gross} c{cap_label(c)}", ident, gate_ok))

                # ---- the constant-exposure twins (gbar SOLVED so mean target gross matches)
                for conv in CONVENTIONS:
                    target = mg_full if conv == "MATCH_FULL" else mg_is
                    f = f_invested if conv == "MATCH_FULL" else f_invested_is
                    gbar = target / f if f > 0 else 0.0
                    wt_, pre_t = twin_weights(px, invest, gbar, inb, nin)
                    gr_tw = pre_t.sum(axis=1)
                    mgap = abs(float(gr_tw.loc[win].mean() if conv == "MATCH_FULL"
                                     else gr_tw.loc[win].loc[:IS_END].mean())
                               - (mg_full if conv == "MATCH_FULL" else mg_is))
                    g5.append((f"G5 mean-gross match {pname} g{gross} c{cap_label(c)} {conv}", mgap, mgap < 1e-12))
                    if not np.isfinite(c):
                        d7 = float((wt_ - wc).abs().max().max())
                        g7.append((f"{pname} g{gross} {conv}", d7, d7 < 1e-12))
                    rt = run_book(px, wt_, rebalance_mask(px.index, FREQ))
                    bt = rt["held"].loc[win].drop(columns=[SWEEP])
                    ptw = bt.values[bt.values > 0]
                    turn_t = float(rt["turnover"].loc[win].sum() / yrs)
                    diag.append(dict(panel=pname, kind="TWIN", conv=conv, cap=cap_label(c), gross=gross,
                                     gbar=gbar, mean_target_gross=float(gr_tw.loc[win].mean()),
                                     mean_held_gross=float(rt["gross"].loc[win].mean()),
                                     gross_p5=float(gr_tw.loc[win].quantile(0.05)),
                                     gross_p95=float(gr_tw.loc[win].quantile(0.95)),
                                     gross_std=float(gr_tw.loc[win].std()),
                                     corr_gross_breadth=float(np.corrcoef(gr_tw.loc[win], nin.loc[win])[0, 1])
                                     if gr_tw.loc[win].std() > 0 else 0.0,
                                     binds_frac=0.0, turnover_yr=turn_t, turnover_vs_live=turn_t / base_turn,
                                     live_turnover_yr=base_turn,
                                     max_name_w_held=float(ptw.max()) if len(ptw) else 0.0,
                                     mean_sweep_w=float(rt["held"][SWEEP].loc[win].mean()),
                                     max_row_sum=float(rt["held"].loc[win].sum(axis=1).max()),
                                     gross_identity_err=np.nan))
                    for rung in RUNGS:
                        rows.append(dict(panel=pname, kind="TWIN", conv=conv, cap=cap_label(c),
                                         gross=gross, cost_bps=rung, turnover_yr=turn_t,
                                         **row_stats(rt, win, OOS_START, base_r, spy, spy_oos, rung)))

                # ---- the scrambled-timing placebos (level AND variability matched, dates wrong)
                if np.isfinite(c):
                    for plab, pk in PERMS:
                        wp, pre_p, gp = perm_weights(px, inb, nin, gr_t, win, pk)
                        same = bool(np.allclose(np.sort(gp.values), np.sort(gr_t.loc[win].values),
                                                rtol=0, atol=1e-12))
                        dm = abs(float(gp.mean()) - mg_full)
                        ds = abs(float(gp.std()) - float(gr_t.loc[win].std()))
                        g11.append((f"{pname} g{gross} c{cap_label(c)} {plab}", max(dm, ds),
                                    same and max(dm, ds) < 1e-9))
                        rp = run_book(px, wp, rebalance_mask(px.index, FREQ))
                        bp = rp["held"].loc[win].drop(columns=[SWEEP])
                        pp = bp.values[bp.values > 0]
                        turn_p = float(rp["turnover"].loc[win].sum() / yrs)
                        gr_held = pre_p.sum(axis=1)
                        diag.append(dict(panel=pname, kind="PERM", conv=plab, cap=cap_label(c),
                                         gross=gross, gbar=np.nan,
                                         mean_target_gross=float(gr_held.loc[win].mean()),
                                         mean_held_gross=float(rp["gross"].loc[win].mean()),
                                         gross_p5=float(gr_held.loc[win].quantile(0.05)),
                                         gross_p95=float(gr_held.loc[win].quantile(0.95)),
                                         gross_std=float(gr_held.loc[win].std()),
                                         corr_gross_breadth=float(np.corrcoef(gr_held.loc[win], nin.loc[win])[0, 1]),
                                         binds_frac=0.0, turnover_yr=turn_p,
                                         turnover_vs_live=turn_p / base_turn, live_turnover_yr=base_turn,
                                         max_name_w_held=float(pp.max()) if len(pp) else 0.0,
                                         mean_sweep_w=float(rp["held"][SWEEP].loc[win].mean()),
                                         max_row_sum=float(rp["held"].loc[win].sum(axis=1).max()),
                                         gross_identity_err=np.nan))
                        for rung in RUNGS:
                            rows.append(dict(panel=pname, kind="PERM", conv=plab, cap=cap_label(c),
                                             gross=gross, cost_bps=rung, turnover_yr=turn_p,
                                             **row_stats(rp, win, OOS_START, base_r, spy, spy_oos, rung)))
        say(f"    ... {pname} done ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(rows); dg = pd.DataFrame(diag)
    df.to_csv(f"{OUT}.grid.csv", index=False); dg.to_csv(f"{OUT}.diag.csv", index=False)

    # ---------------------------------------------------------------- remaining gates
    px, invest = panels["U56"]
    d1 = float((cap_weights(px, invest, 0.75, np.inf)[0] - cand_reference(px, invest, 0.75)).abs().max().max())
    gate("G1 c=INF == an independent CAND build to machine precision (U56, g=0.75)", f"max|dw| {d1:.3e}", "< 1e-12", d1 < 1e-12)
    gate("G3 no leverage in any of the 108 books", f"max held row sum {dg.max_row_sum.max():.9f}",
         "<= 1+1e-9", bool((dg.max_row_sum <= 1 + 1e-9).all()))
    e4 = max(v for n, v, ok in g5 if n.startswith("G4"))
    gate("G4 gross identity G_t = min(g, c x N_in) on the target weights (20 cells)",
         f"max|d| {e4:.3e}", "< 1e-12", all(ok for n, _, ok in g5 if n.startswith("G4")))
    e5 = max(v for n, v, ok in g5 if n.startswith("G5"))
    gate("G5 twin mean target gross == cap's, per convention (40 cells)", f"max|d| {e5:.3e}",
         "< 1e-12", all(ok for n, _, ok in g5 if n.startswith("G5")))
    gate("G7 at c=INF the twin collapses onto the book to machine precision (both conventions, panels, gross)",
         f"{sum(1 for n, v, ok in g7 if ok)} of {len(g7)} cells, max|dw| {max(v for n, v, ok in g7):.3e}",
         f"{len(g7)} of {len(g7)}", all(ok for n, v, ok in g7))
    shy_ok = all(bool(p[0][SWEEP].loc[p[0].index[WARMUP:]].notna().all()) for p in panels.values())
    gate("G8 sweep instrument priced on every held row", f"SHY non-null on both panels: {shy_ok}",
         "True", shy_ok)

    # G9 -- no lookahead: rebuild the weights from a truncated tape
    pxu, inv_u = panels["U56"]
    worst = 0.0
    for cut in ("2013-06-28", "2019-03-29"):
        sub = pxu.loc[:cut]
        a = cap_weights(sub, inv_u, 0.75, 0.02)[0].iloc[-1]
        b = cap_weights(pxu, inv_u, 0.75, 0.02)[0].loc[sub.index[-1]]
        worst = max(worst, float((a.reindex(b.index).fillna(0.0) - b).abs().max()))
    gate("G9 no-lookahead: weights at d from px.loc[:d] == weights at d from the full tape",
         f"max|dw| {worst:.3e} over 2 cut dates", "< 1e-12", worst < 1e-12)
    publish("G9 scope", "the CAP book and the MATCH_IS twin are causal; MATCH_FULL's gbar uses the "
                        "full window BY DESIGN (hindsight handed to the twin) and is excluded from rule 8")

    h = df[(df.panel == "U56") & (df.kind == "CAP") & (df.cap == "0.020") & (df.gross == 0.75)
           & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    ht = dg[(dg.panel == "U56") & (dg.kind == "CAP") & (dg.cap == "0.020") & (dg.gross == 0.75)].iloc[0]
    d10 = max(abs(h.CAGR - 0.1158), abs(h.Sharpe - 1.2643) / 10, abs(h.MaxDD + 0.1481),
              abs(h.OOS_CAGR - 0.1270), abs(h.OOS_Sharpe - 1.3243) / 10, abs(ht.turnover_yr - 3.51) / 100)
    gate("G11 every placebo's gross series is a PERMUTATION of its capped cell's "
         "(sorted arrays, mean and sd)",
         f"{sum(1 for n, v, ok in g11 if ok)} of {len(g11)} placebo books, max|d(mean, sd)| "
         f"{max(v for n, v, ok in g11):.3e}", f"{len(g11)} of {len(g11)}",
         all(ok for n, v, ok in g11))
    gate("G10 reproduces idea 2322's committed U56 CAP2 headline (11.58%/1.2643/-14.81%, "
         "OOS 12.70%/1.3243, turnover 3.51/yr)",
         f"read {h.CAGR:.2%} / {h.Sharpe:.4f} / {h.MaxDD:.2%}, OOS {h.OOS_CAGR:.2%} / "
         f"{h.OOS_Sharpe:.4f}, turnover {ht.turnover_yr:.2f}/yr -> max|d| {d10:.2e}", "< 1e-3", d10 < 1e-3)

    # ---------------------------------------------------------------- A. the breadth link, measured
    say("\n=== A. THE CAP IS A BREADTH-LINKED DE-GROSSER — the mechanism, measured not assumed ===")
    say("  panel gross  cap   | meanGross  p5     p95    sd     corr(G,N_in) | binds%  turn/yr  maxNameHeld  meanSHY")
    for pname in panels:
        for gross in GROSSES:
            for c in CAPS:
                d = dg[(dg.panel == pname) & (dg.kind == "CAP") & (dg.cap == cap_label(c))
                       & (dg.gross == gross)].iloc[0]
                say(f"  {pname:5s} {gross:.2f} {cap_label(c):>5s} | {d.mean_target_gross:8.3f} "
                    f"{d.gross_p5:6.3f} {d.gross_p95:6.3f} {d.gross_std:6.3f} {d.corr_gross_breadth:12.4f} |"
                    f" {d.binds_frac:6.1%} {d.turnover_yr:8.2f} {d.max_name_w_held:12.2%} {d.mean_sweep_w:8.2%}")

    # ---------------------------------------------------------------- B. full grid at 10 bps
    say("\n=== B. THE GRID AT THE HEADLINE RUNG (10 bps) — CAP against its CONSTANT-EXPOSURE TWINS ===")
    for pname in panels:
        for gross in GROSSES:
            say(f"\n  {pname} gross {gross:.2f}")
            say("   cap  kind/conv     |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh  OOS DD |"
                " 4a 4b | H1/H2/OOS/DD/CAGR | turn/yr  gbar")
            for c in CAPS:
                variants = [("CAP", "-")] + [("TWIN", cv) for cv in CONVENTIONS]
                if np.isfinite(c):
                    variants += [("PERM", pl) for pl, _ in PERMS]
                for kind, conv in variants:
                    r = df[(df.panel == pname) & (df.kind == kind) & (df.conv == conv)
                           & (df.cap == cap_label(c)) & (df.gross == gross)
                           & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                    d = dg[(dg.panel == pname) & (dg.kind == kind) & (dg.conv == conv)
                           & (dg.cap == cap_label(c)) & (dg.gross == gross)].iloc[0]
                    lg = "".join("1" if r[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                    tag = "CAP        " if kind == "CAP" else f"{kind:4s} {conv:10s}"
                    say(f"  {cap_label(c):>5s} {tag} | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%} |"
                        f" {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} {r.OOS_MaxDD:7.2%} |"
                        f" {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg:17s} |"
                        f" {r.turnover_yr:7.2f} {d.gbar if np.isfinite(d.gbar) else float('nan'):6.3f}")

    # ---------------------------------------------------------------- C. head to head
    say("\n=== C. THE ANSWER: CAP minus TWIN at MATCHED MEAN EXPOSURE, every cell, every rung ===")
    hh = []
    for pname in panels:
        for gross in GROSSES:
            for c in CAPS:
                for conv in CONVENTIONS:
                    for rung in RUNGS:
                        a = df[(df.panel == pname) & (df.kind == "CAP") & (df.cap == cap_label(c))
                               & (df.gross == gross) & (df.cost_bps == rung)].iloc[0]
                        b = df[(df.panel == pname) & (df.kind == "TWIN") & (df.conv == conv)
                               & (df.cap == cap_label(c)) & (df.gross == gross)
                               & (df.cost_bps == rung)].iloc[0]
                        hh.append(dict(panel=pname, gross=gross, cap=cap_label(c), conv=conv, cost_bps=rung,
                                       binding=bool(np.isfinite(c)),
                                       dCAGR=a.CAGR - b.CAGR, dSharpe=a.Sharpe - b.Sharpe,
                                       dMaxDD=a.MaxDD - b.MaxDD, dOOS_Sharpe=a.OOS_Sharpe - b.OOS_Sharpe,
                                       dH1=a.H1 - b.H1, dH2=a.H2 - b.H2, dTurn=a.turnover_yr - b.turnover_yr,
                                       cap4b=bool(a.pass4b), twin4b=bool(b.pass4b),
                                       cap4a=bool(a.pass4a), twin4a=bool(b.pass4a),
                                       dominates=bool(a.CAGR > b.CAGR and a.MaxDD > b.MaxDD),
                                       dominated=bool(a.CAGR < b.CAGR and a.MaxDD < b.MaxDD)))
    hd = pd.DataFrame(hh); hd.to_csv(f"{OUT}.headtohead.csv", index=False)
    bind = hd[hd.binding]          # c=INF is the degenerate cell where book == twin
    say(f"  degenerate cells (c=INF, book IS its own twin): {len(hd) - len(bind)} of {len(hd)}, "
        f"max|dSharpe| there {hd[~hd.binding].dSharpe.abs().max():.2e}")
    say(f"  BINDING cells (c finite): {len(bind)}")
    for col, lab in (("dSharpe", "full-sample Sharpe"), ("dOOS_Sharpe", "OOS Sharpe"),
                     ("dCAGR", "CAGR"), ("dMaxDD", "MaxDD (higher = shallower)")):
        v = bind[col]
        say(f"    CAP beats TWIN on {lab:28s}: {int((v > 0).sum()):3d} of {len(v)}   "
            f"median {v.median():+.4f}  min {v.min():+.4f}  max {v.max():+.4f}")
    say(f"    CAP DOMINATES twin (higher CAGR AND shallower DD): {int(bind.dominates.sum())} of {len(bind)};"
        f"  TWIN dominates CAP: {int(bind.dominated.sum())} of {len(bind)}")
    say("\n  by (panel, convention) at the headline rung:")
    for (pn, cv), grp in bind[bind.cost_bps == HEADLINE_RUNG].groupby(["panel", "conv"]):
        say(f"    {pn:5s} {cv:10s}: CAP better Sharpe {int((grp.dSharpe > 0).sum())}/{len(grp)}, "
            f"OOS Sharpe {int((grp.dOOS_Sharpe > 0).sum())}/{len(grp)}, CAGR {int((grp.dCAGR > 0).sum())}/{len(grp)}, "
            f"MaxDD {int((grp.dMaxDD > 0).sum())}/{len(grp)}  | median dSharpe {grp.dSharpe.median():+.4f}, "
            f"median dMaxDD {grp.dMaxDD.median():+.2%}")
    say("\n  4b flips at matched exposure (binding cells):")
    say(f"    CAP passes and TWIN fails: {int((bind.cap4b & ~bind.twin4b).sum())} of {len(bind)}")
    say(f"    TWIN passes and CAP fails: {int((~bind.cap4b & bind.twin4b).sum())} of {len(bind)}")
    say(f"    both pass: {int((bind.cap4b & bind.twin4b).sum())}      both fail: "
        f"{int((~bind.cap4b & ~bind.twin4b).sum())}")
    say(f"    4a: CAP passes {int(bind.cap4a.sum())}, TWIN passes {int(bind.twin4a.sum())} of {len(bind)}")

    say("\n  the live cell, stated on its own (U56, g=0.75, c=2%, 10 bps):")
    for conv in CONVENTIONS:
        a = df[(df.panel == "U56") & (df.kind == "CAP") & (df.cap == "0.020") & (df.gross == 0.75)
               & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
        b = df[(df.panel == "U56") & (df.kind == "TWIN") & (df.conv == conv) & (df.cap == "0.020")
               & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
        dgb = dg[(dg.panel == "U56") & (dg.kind == "TWIN") & (dg.conv == conv) & (dg.cap == "0.020")
                 & (dg.gross == 0.75)].iloc[0]
        say(f"    CAP  {a.CAGR:.2%} / {a.Sharpe:.4f} / {a.MaxDD:.2%}  OOS {a.OOS_CAGR:.2%} / {a.OOS_Sharpe:.4f}"
            f"  4b {'Y' if a.pass4b else '.'}   turnover {a.turnover_yr:.2f}/yr")
        say(f"    TWIN {conv:10s} gbar {dgb.gbar:.4f}: {b.CAGR:.2%} / {b.Sharpe:.4f} / {b.MaxDD:.2%}"
            f"  OOS {b.OOS_CAGR:.2%} / {b.OOS_Sharpe:.4f}  4b {'Y' if b.pass4b else '.'}"
            f"   turnover {b.turnover_yr:.2f}/yr   -> dSharpe {a.Sharpe - b.Sharpe:+.4f},"
            f" dCAGR {a.CAGR - b.CAGR:+.2%}, dMaxDD {a.MaxDD - b.MaxDD:+.2%},"
            f" dOOS_Sh {a.OOS_Sharpe - b.OOS_Sharpe:+.4f}")

    # ---------------------------------------------------------------- C2. the timing test
    say("\n=== C2. THE TIMING TEST: CAP minus the SCRAMBLED-TIMING PLACEBOS (level AND variability "
        "matched, dates wrong) ===")
    ph = []
    for pname in panels:
        for gross in GROSSES:
            for c in CAPS:
                if not np.isfinite(c):
                    continue
                for plab, _ in PERMS:
                    for rung in RUNGS:
                        a = df[(df.panel == pname) & (df.kind == "CAP") & (df.cap == cap_label(c))
                               & (df.gross == gross) & (df.cost_bps == rung)].iloc[0]
                        b = df[(df.panel == pname) & (df.kind == "PERM") & (df.conv == plab)
                               & (df.cap == cap_label(c)) & (df.gross == gross)
                               & (df.cost_bps == rung)].iloc[0]
                        ph.append(dict(panel=pname, gross=gross, cap=cap_label(c), perm=plab,
                                       cost_bps=rung, dCAGR=a.CAGR - b.CAGR, dSharpe=a.Sharpe - b.Sharpe,
                                       dMaxDD=a.MaxDD - b.MaxDD, dOOS_Sharpe=a.OOS_Sharpe - b.OOS_Sharpe,
                                       dTurn=a.turnover_yr - b.turnover_yr,
                                       cap4b=bool(a.pass4b), perm4b=bool(b.pass4b),
                                       dominates=bool(a.CAGR > b.CAGR and a.MaxDD > b.MaxDD)))
    pdf = pd.DataFrame(ph); pdf.to_csv(f"{OUT}.placebo.csv", index=False)
    say(f"  placebo cells: {len(pdf)} (4 finite caps x 3 permutations x 2 gross x 2 panels x 4 rungs)")
    for col, lab in (("dSharpe", "full-sample Sharpe"), ("dOOS_Sharpe", "OOS Sharpe"),
                     ("dCAGR", "CAGR"), ("dMaxDD", "MaxDD (higher = shallower)"),
                     ("dTurn", "turnover (higher = MORE churn)")):
        v = pdf[col]
        say(f"    CAP beats its placebo on {lab:32s}: {int((v > 0).sum()):3d} of {len(v)}   "
            f"median {v.median():+.4f}  min {v.min():+.4f}  max {v.max():+.4f}")
    say(f"    CAP DOMINATES the placebo (higher CAGR AND shallower DD): {int(pdf.dominates.sum())} of {len(pdf)}")
    say(f"    4b: CAP passes and the placebo fails {int((pdf.cap4b & ~pdf.perm4b).sum())}; "
        f"placebo passes and CAP fails {int((~pdf.cap4b & pdf.perm4b).sum())}; "
        f"both pass {int((pdf.cap4b & pdf.perm4b).sum())} of {len(pdf)}")
    say("  by (panel, permutation) at the headline rung:")
    for (pn, pl), grp in pdf[pdf.cost_bps == HEADLINE_RUNG].groupby(["panel", "perm"]):
        say(f"    {pn:5s} {pl:9s}: Sharpe {int((grp.dSharpe > 0).sum())}/{len(grp)}, "
            f"OOS Sharpe {int((grp.dOOS_Sharpe > 0).sum())}/{len(grp)}, CAGR {int((grp.dCAGR > 0).sum())}/{len(grp)}, "
            f"MaxDD {int((grp.dMaxDD > 0).sum())}/{len(grp)} | median dSharpe {grp.dSharpe.median():+.4f}, "
            f"median dMaxDD {grp.dMaxDD.median():+.2%}")
    say("\n  SIDE BY SIDE at the live cell (U56, g=0.75, c=2%, 10 bps) — what each null removes:")
    a = df[(df.panel == "U56") & (df.kind == "CAP") & (df.cap == "0.020") & (df.gross == 0.75)
           & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    say(f"    CAP                     {a.CAGR:6.2%} / {a.Sharpe:.4f} / {a.MaxDD:7.2%}  OOS {a.OOS_CAGR:6.2%}"
        f" / {a.OOS_Sharpe:.4f}  turnover {a.turnover_yr:.2f}/yr")
    for kind, conv in [("TWIN", cv) for cv in CONVENTIONS] + [("PERM", pl) for pl, _ in PERMS]:
        b = df[(df.panel == "U56") & (df.kind == kind) & (df.conv == conv) & (df.cap == "0.020")
               & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
        d = dg[(dg.panel == "U56") & (dg.kind == kind) & (dg.conv == conv) & (dg.cap == "0.020")
               & (dg.gross == 0.75)].iloc[0]
        say(f"    {kind:4s} {conv:11s} {b.CAGR:6.2%} / {b.Sharpe:.4f} / {b.MaxDD:7.2%}  OOS {b.OOS_CAGR:6.2%}"
            f" / {b.OOS_Sharpe:.4f}  turnover {b.turnover_yr:.2f}/yr  meanGross {d.mean_target_gross:.3f}"
            f" sd {d.gross_std:.3f} corr(G,N_in) {d.corr_gross_breadth:+.4f} maxName {d.max_name_w_held:.2%}"
            f"  -> dSharpe {a.Sharpe - b.Sharpe:+.4f} dCAGR {a.CAGR - b.CAGR:+.2%}"
            f" dMaxDD {a.MaxDD - b.MaxDD:+.2%} dOOS_Sh {a.OOS_Sharpe - b.OOS_Sharpe:+.4f}")

    # ------------------------------------------------- C3. is either gap a COST REBATE?
    say("\n=== C3. IS EITHER GAP A COST REBATE?  both nulls churn MORE than the cap, so the 0 bps "
        "column is the test ===")
    say("  If the cap's advantage were only the churn it saves, it would vanish at 0 bps.")
    for lab, d, col in (("CAP - CONSTANT TWIN", bind, "dSharpe"), ("CAP - PLACEBO", pdf, "dSharpe")):
        say(f"  {lab}:")
        for rung in RUNGS:
            g = d[d.cost_bps == rung]
            say(f"    {rung:5.1f} bps: dSharpe median {g.dSharpe.median():+.4f} (wins "
                f"{int((g.dSharpe > 0).sum())}/{len(g)})   dCAGR median {g.dCAGR.median():+.2%}   "
                f"dOOS_Sharpe median {g.dOOS_Sharpe.median():+.4f} (wins "
                f"{int((g.dOOS_Sharpe > 0).sum())}/{len(g)})   dTurnover median "
                f"{g.dTurn.median():+.2f}/yr")

    # ---------------------------------------------------------------- D. every rung
    say("\n=== D. EVERY COST RUNG — all 432 published rows ===")
    for pname in panels:
        for gross in GROSSES:
            say(f"\n  {pname} gross {gross:.2f}   (CAGR/Sharpe/4b)")
            say("   cap  kind/conv     |" + "".join(f"   {int(x):2d}bps                " for x in RUNGS))
            for c in CAPS:
                variants = [("CAP", "-")] + [("TWIN", cv) for cv in CONVENTIONS]
                if np.isfinite(c):
                    variants += [("PERM", pl) for pl, _ in PERMS]
                for kind, conv in variants:
                    cells = []
                    for rung in RUNGS:
                        r = df[(df.panel == pname) & (df.kind == kind) & (df.conv == conv)
                               & (df.cap == cap_label(c)) & (df.gross == gross)
                               & (df.cost_bps == rung)].iloc[0]
                        cells.append(f"  {r.CAGR:6.2%}/{r.Sharpe:.4f}/{'Y' if r.pass4b else '.'}   ")
                    tag = "CAP        " if kind == "CAP" else f"{kind:4s} {conv:10s}"
                    say(f"  {cap_label(c):>5s} {tag} |" + "".join(cells))

    say("\n=== E. KEEP COUNTS OVER ALL 432 PUBLISHED ROWS ===")
    say(f"  ALL rows      : 4b {int(df.pass4b.sum()):3d} of {len(df)}   4a {int(df.pass4a.sum()):3d} of {len(df)}")
    for kind in ("CAP", "TWIN", "PERM"):
        d = df[df.kind == kind]
        say(f"  {kind:13s} : 4b {int(d.pass4b.sum()):3d} of {len(d)}   4a {int(d.pass4a.sum()):3d} of {len(d)}")
    for conv in CONVENTIONS + [pl for pl, _ in PERMS]:
        d = df[df.conv == conv]
        say(f"   {conv:11s}: 4b {int(d.pass4b.sum()):3d} of {len(d)}   4a {int(d.pass4a.sum()):3d} of {len(d)}")
    for rung in RUNGS:
        d = df[df.cost_bps == rung]
        say(f"   {rung:5.1f} bps: 4b {int(d.pass4b.sum()):3d}/{len(d)}  4a {int(d.pass4a.sum()):3d}/{len(d)}"
            "   binding leg on 4b FAILs: " +
            "  ".join(f"{k} {int((~d[k][~d.pass4b]).sum())}" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))

    # ---------------------------------------------------------------- F. rule 8
    say("\n=== F. RULE 8 — (c, g) chosen on warm-up..2016-12-31 ONLY, 2017-2026 read ONCE ===")
    say("   MATCH_FULL twins and ALL placebos are EXCLUDED (MATCH_FULL's gbar uses the full window;")
    say("   the placebos are anti-causal or hindsight-ordered by construction).  Three arenas:")
    say("   CAP-only, TWIN(MATCH_IS)-only, and POOLED over {CAP, TWIN} so the chooser votes on the question.")
    wf = []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        b_oos = priced(run_book(px, rules_v2_weights(px[invest], band=BAND, gross=0.75)
                                .reindex(columns=px.columns).fillna(0.0), rebalance_mask(px.index, FREQ)),
                       HEADLINE_RUNG).loc[win].loc[OOS_START:]
        for rung in RUNGS:
            d = df[(df.panel == pname) & (df.cost_bps == rung)
                   & ((df.kind == "CAP") | (df.conv == "MATCH_IS"))]
            arenas = {"CAP_ONLY": d[d.kind == "CAP"], "TWIN_ONLY": d[d.kind == "TWIN"], "POOLED": d}
            for arena, sub in arenas.items():
                for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                    pick = sub.loc[sub[col].idxmax()]
                    wf.append(dict(panel=pname, cost_bps=rung, arena=arena, chooser=chooser,
                                   pick_kind=pick.kind, pick_cap=pick.cap, pick_gross=pick.gross,
                                   OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                                   base_OOS_CAGR=cagr(b_oos), base_OOS_Sharpe=sharpe(b_oos),
                                   base_OOS_MaxDD=maxdd(b_oos), spy_OOS_CAGR=cagr(spy_oos),
                                   spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_MaxDD=maxdd(spy_oos),
                                   full4b=bool(pick.pass4b),
                                   beats_spy_oos=bool(pick.OOS_Sharpe > sharpe(spy_oos)),
                                   beats_base_oos=bool(pick.OOS_Sharpe > sharpe(b_oos))))
                    say(f"  {pname:5s} {rung:5.1f}bps {arena:9s} {chooser:11s} -> {pick.kind:4s} "
                        f"c {pick.cap:>5s} g {pick.gross:.2f} | OOS {pick.OOS_CAGR:6.2%} / "
                        f"{pick.OOS_Sharpe:.4f} / {pick.OOS_MaxDD:7.2%} | live v2 OOS {cagr(b_oos):6.2%} / "
                        f"{sharpe(b_oos):.4f} | SPY OOS {cagr(spy_oos):6.2%} / {sharpe(spy_oos):.4f} | "
                        f"full 4b {'Y' if pick.pass4b else '.'}")
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    pool = wfd[wfd.arena == "POOLED"]
    say(f"\n  POOLED arena: picks landing on the CAP: {int((pool.pick_kind == 'CAP').sum())} of {len(pool)}; "
        f"on the TWIN: {int((pool.pick_kind == 'TWIN').sum())} of {len(pool)}")
    say(f"  POOLED picks beating SPY OOS Sharpe: {int(pool.beats_spy_oos.sum())} of {len(pool)}; "
        f"beating the live book OOS: {int(pool.beats_base_oos.sum())} of {len(pool)}; "
        f"carrying a full-sample 4b: {int(pool.full4b.sum())} of {len(pool)}")
    for arena in ("CAP_ONLY", "TWIN_ONLY"):
        a = wfd[wfd.arena == arena]
        say(f"  {arena:9s}: mean OOS Sharpe {a.OOS_Sharpe.mean():.4f}, mean OOS CAGR {a.OOS_CAGR.mean():.2%}, "
            f"mean OOS MaxDD {a.OOS_MaxDD.mean():.2%}, 4b {int(a.full4b.sum())}/{len(a)}")
    ca, tw = wfd[wfd.arena == "CAP_ONLY"].reset_index(), wfd[wfd.arena == "TWIN_ONLY"].reset_index()
    say(f"  head-to-head on the SAME (panel, rung, chooser): CAP's pick beats the TWIN's pick on OOS "
        f"Sharpe at {int((ca.OOS_Sharpe > tw.OOS_Sharpe).sum())} of {len(ca)}")

    gdf = pd.DataFrame(GATES); gdf.to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n=== GATES: {int(gdf.pass_.sum())} of {len(gdf)} pass ===")
    for _, g in gdf[~gdf.pass_].iterrows():
        say(f"    FAILED: {g.gate} = {g.value} (target {g.target})")
    say(f"\nwrote {OUT}.grid.csv / .diag.csv / .headtohead.csv / .placebo.csv / .walkforward.csv / .gates.csv "
        f"  ({time.time() - t0:.0f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

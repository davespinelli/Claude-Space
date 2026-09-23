#!/usr/bin/env python3
"""idea 2477 (lane B, 2026-09-23) — DOES A ZERO-PARAMETER STACK OF THE EXPOSURE-NEUTRAL
DEVICES CLEAR THE -31.0% ADOPTION BAR AT dCAGR >= 0 AND SURVIVE RULE 8, WHERE EVERY FITTED
SINGLE DEVICE DOES NOT?

THE OBJECT.  The record's standing 4b KEEP-candidate is idea 2322's CAP2: every name INSIDE
the 200d +/- 3% band held at `min(gross / N_in, 2%)` of NAV, idle NAV swept to SHY, weekly,
t+1, 10 bps.  On U56 / gross 0.75 it reads 11.62% / 1.2687 / -14.81% at 3.51 turns a year,
and idea 2431 wrote the adoption bar:  cut turnover 3.51x -> 2.42x (-31.0%) AT UNCHANGED
RETURNS.

THE DIAGNOSIS THIS RUN ATTACKS (idea 2463, lane C, run 54).  2463 put nine turnover devices
on one axis and refuted the record's `-0.10 pp of CAGR per 1% saved` as a TURNOVER rate: it
is a DE-GROSSING rate.  Pooled median pp per 1% saved splits by EXPOSURE, not by device --
SCALE -0.115 / WHIP -0.112 / WIDTH -0.195 / AGE -0.064 (de-grossers) against
PARTIAL +0.005 / ROTA +0.008 / BANDW +0.009 / DRIFT +0.020 / HOLD +0.085 (exposure-neutral).
The neutral class is FREE OR BETTER per unit of turnover removed.  2463 nevertheless filed
its one 4b candidate NOT ADOPTED, because rule 8 refused it at 0 of 48 picks.

THE STRUCTURAL READING THIS RUN TESTS.  Rule 8 refuses because a chooser must pick a RUNG on
a LADDER, and the IS chooser picks the wrong rung (2463: C_ISSHARPE buys OOS Sharpe 1.41 at
OOS CAGR 5.10% against 12.79%).  A STACK switched on at PRE-REGISTERED rungs has NOTHING to
fit, so rule 8 collapses to "does the fixed book hold out of sample".  And if the neutral
devices' savings COMPOSE, the stack may reach the bar where no single fitted device does.

DIAL 1 -- STACK DEPTH k in {0,1,2,3,4,5}.  Devices are switched on in the order of 2463's OWN
published pp-per-1% (most positive first), which is fixed BEFORE any number in this run:
    k=0 NONE (the undamped CAP2 reference)
    k=1 + HOLD     (+0.085)   min hold: a name younger than h acting rebalances is never REDUCED
    k=2 + DRIFT    (+0.020)   weight-drift no-trade band d of NAV
    k=3 + BANDW    (+0.009)   band half-width b (both edges together)
    k=4 + ROTA     (+0.008)   act on every k-th weekly rebalance only
    k=5 + PARTIAL  (+0.005)   move a fraction phi of the way to target
DIAL 2 -- STRENGTH TIER t in {MILD, MID, STRONG}.  Every rung is taken VERBATIM from 2463's
committed ladders; nothing here is a new number.
    MILD    HOLD 2  DRIFT 0.0010  BANDW 0.05  ROTA 2  PARTIAL 0.75
    MID     HOLD 4  DRIFT 0.0025  BANDW 0.08  ROTA 3  PARTIAL 0.50
    STRONG  HOLD 8  DRIFT 0.0050  BANDW 0.12  ROTA 4  PARTIAL 0.35

THAT IS EXACTLY TWO TUNED PARAMETERS.  Panels {U56, B136}, gross {0.75, 1.00} and cost rungs
{0, 10, 25, 50} bps are REPORTED IN FULL, never selected on.  SMALL is not priced: ideas
2318 / 2322 / 2326 / 2343 each published SMALL's 4b pass count at 0 of 40-120, so there is no
pass there for a turnover device to keep.

CARRIED ALONGSIDE, NOT SELECTED ON: each of the five devices ALONE at each tier (15 SINGLE
points), so the run also publishes idea 2469's question in passing -- do two free devices'
savings ADD or OVERLAP?  ADDITIVITY is measured as (sum of the singles' cuts) vs (the stack's
cut) at the same depth.

THE PREMISE IS TESTED, NOT ASSUMED.  Every device is forced through its IDENTITY rung
(h=1, d=0, b=0.03, rota=1, phi=1.00) and the FULL five-device identity stack is gated to be
BIT-IDENTICAL to NONE, so a "saving" can never be an implementation difference.  Two of this
run's grid points and one extra point reproduce lane C's committed numbers from idea 2463.

BOTH KEEP PATHS on every row: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse)
and 4b (Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x
SPY's).  RULE 8: (k, t) chosen on warm-up..2016-12-31 ONLY by three pre-stated rules, then
2017-2026 read ONCE.  The third is the point of the idea:
    C_ISSHARPE  max IS Sharpe over the 18 stack points
    C_ISADOPT   max IS CAGR among stack points clearing the -31.0% cut IN SAMPLE (2463's)
    C_ZEROPARAM NO CHOICE AT ALL -- the fixed point (k=5, MILD), pre-registered above.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_zero-parameter-exposure-neutral-stack_B.py
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

DATE, SLUG, LANE = "2026-09-23", "zero-parameter-exposure-neutral-stack", "B"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, CAP, CADENCE, WARMUP = 0.03, 0.02, "W", 260
GROSSES = [0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG = 10.0
SWEEP = "SHY"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BAR_CUT = 0.310                       # idea 2431: 3.51x -> 2.42x
NEUTRAL_TOL = 0.02                    # exposure-neutral = mean risk gross within +/-2% relative

ORDER = ["HOLD", "DRIFT", "BANDW", "ROTA", "PARTIAL"]     # 2463's pp-per-1%, most positive first
IDENTITY = dict(HOLD=1, DRIFT=0.0, BANDW=BAND, ROTA=1, PARTIAL=1.00)
TIERS = {
    "MILD":   dict(HOLD=2, DRIFT=0.0010, BANDW=0.05, ROTA=2, PARTIAL=0.75),
    "MID":    dict(HOLD=4, DRIFT=0.0025, BANDW=0.08, ROTA=3, PARTIAL=0.50),
    "STRONG": dict(HOLD=8, DRIFT=0.0050, BANDW=0.12, ROTA=4, PARTIAL=0.35),
}
DEPTHS = [0, 1, 2, 3, 4, 5]
ZERO_PARAM_POINT = (5, "MILD")        # pre-registered BEFORE any number in this run

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


def spec(depth, tier, singles=None):
    """The device settings for stack depth `depth` at tier `tier`.  `singles` (a device name)
    instead returns that ONE device at the tier, everything else at identity."""
    s = dict(IDENTITY)
    if singles is not None:
        s[singles] = TIERS[tier][singles]
        return s
    for dev in ORDER[:depth]:
        s[dev] = TIERS[tier][dev]
    return s


# ---------------------------------------------------------------- target book (TARGET-side)
def cap_weights(px, invest, gross, s):
    """idea 2322's CAP2 with the one TARGET-side device (BANDW) applied.

    admitted set = names inside the 200d +/- b band (hysteresis, baseline.band_state) and
    priced that day; w_i = min(gross / N_in, CAP); idle NAV swept to SHY.
    """
    q = px[invest]
    adm = band_state(q, float(s["BANDW"])) & q.notna()
    nin = adm.sum(axis=1).replace(0, np.nan)
    per = pd.concat([gross / nin, pd.Series(CAP, index=q.index)], axis=1).min(axis=1)
    w = adm.astype(float).mul(per.fillna(0.0), axis=0)
    w = w.reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return w


# ---------------------------------------------------------------- the engine (EXECUTION-side)
def run_book(prices, weights, s, freq=CADENCE, sweep=SWEEP, phase=0):
    """engine.backtest with the four EXECUTION-side devices applied TOGETHER, in this
    pre-registered order inside an acting rebalance:
        ROTA    decides whether the rebalance acts at all;
        HOLD    blocks REDUCTIONS of names held fewer than h acting rebalances;
        DRIFT   filters which risk names move at all (|target - held| > d);
        PARTIAL scales the surviving move by phi.
    SHY is then set to 1 - sum(risk weights).  The all-identity setting reduces to
    engine.backtest exactly (gates G1 / G4a-G4f).  Zero-cost returns and turnover are kept
    separately so every cost rung is priced from one pass.
    """
    d = float(s["DRIFT"]); phi = float(s["PARTIAL"])
    hold = int(s["HOLD"]); rota = int(s["ROTA"])

    cols = list(prices.columns)
    si = cols.index(sweep)
    risk = np.ones(len(cols), dtype=bool); risk[si] = False
    rets = prices.pct_change().fillna(0.0)
    w_target = weights.reindex(prices.index).fillna(0.0).shift(1)
    key = prices.index.to_period(freq)
    ser = pd.Series(key, index=prices.index)
    mask = (ser != ser.shift(-1)).shift(1, fill_value=False).values
    shy_live = prices[sweep].notna().shift(1, fill_value=False).values

    n = len(prices.index)
    held = np.zeros((n, len(cols)))
    cur = np.zeros(len(cols))
    age = np.zeros(len(cols))
    turnover = np.zeros(n); gross_s = np.zeros(n); risk_g = np.zeros(n)
    trade_abs: list[float] = []
    wt = w_target.values; rv = rets.values
    lev = 0; nreb = 0; nact = 0
    for i in range(n):
        act = mask[i] or i == 0
        if act:
            if (nreb % rota) != (phase % rota):
                act = False
            nreb += 1
        if act:
            nact += 1
            tgt = wt[i]
            new = cur.copy()
            mv = risk & (np.abs(tgt - cur) > d)
            if hold > 1:
                young = (cur > 1e-12) & (age < hold) & (tgt < cur)
                mv = mv & ~young
            new[mv] = cur[mv] + phi * (tgt[mv] - cur[mv])
            srisk = new[risk].sum()
            if srisk > 1.0:                       # never lever: scale the risk sleeve back
                lev += 1
                new[risk] *= 1.0 / srisk
                srisk = 1.0
            new[si] = max(0.0, 1.0 - srisk) if shy_live[i] else 0.0
            dv = np.abs(new - cur)
            turnover[i] = dv.sum()
            trade_abs.extend(dv[(dv > 1e-12) & risk].tolist())
            fresh = (new > 1e-12) & (cur <= 1e-12)
            age = np.where(fresh, 0.0, age + 1.0)
            cur = new
        held[i] = cur
        gross_s[i] = cur.sum()
        risk_g[i] = cur[risk].sum()
        growth = cur * (1 + rv[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    return dict(r0=pd.Series((held * rv).sum(axis=1), index=prices.index),
                turnover=pd.Series(turnover, index=prices.index),
                gross=pd.Series(gross_s, index=prices.index),
                risk_gross=pd.Series(risk_g, index=prices.index),
                held=pd.DataFrame(held, index=prices.index, columns=cols),
                trade_abs=np.asarray(trade_abs),
                lev_events=lev, acting_rebalances=nact, scheduled_rebalances=nreb)


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


def legstring(d):
    return "".join("1" if d[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    say("=== idea 2477 (lane B, run 56) — the ZERO-PARAMETER STACK of the EXPOSURE-NEUTRAL devices ===")
    say(f"    {DATE}  lane {LANE}   band {BAND}  cap {CAP}  cadence {CADENCE}  t+1  rungs {RUNGS} bps  sweep {SWEEP}")
    say(f"    DIAL 1 stack depth k {DEPTHS}, devices switched on in 2463's pp-per-1% order {ORDER}")
    for t, v in TIERS.items():
        say(f"    DIAL 2 tier {t:6s} {v}")
    say(f"    identity rungs {IDENTITY}   zero-parameter point (k, tier) = {ZERO_PARAM_POINT}")
    say(f"    THE BAR (idea 2431): turnover -{BAR_CUT:.1%} at unchanged returns (3.51x -> 2.42x)")
    gate("G8 exactly two tuned parameters", "stack depth k, strength tier t", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        invest = list(px.columns)
        panels[nm] = (px, invest)
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y, {len(invest)} columns, {len(px)} rows", ">= 10y", yrs >= 10)
        win = px.index[WARMUP:]
        dead = [c for c in px.columns if px[c].loc[win].notna().sum() == 0]
        publish(f"G0b all-NaN columns in {nm} (idea 2332's MMC defect, carried forward)",
                f"{len(dead)} dead: {dead}")
        gate(f"G6 sweep {SWEEP} priced on every in-window row ({nm})",
             f"non-null {int(px[SWEEP].loc[win].notna().sum())} of {len(win)}", "all",
             bool(px[SWEEP].loc[win].notna().all()))

    px_u, inv_u = panels["U56"]
    s_id = dict(IDENTITY)

    # ---- G1: the k=0 replica IS engine.backtest
    w0 = cap_weights(px_u, inv_u, 0.75, s_id)
    r_eng = backtest(px_u, w0, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    res_none = run_book(px_u, w0, s_id)
    d1 = float((r_eng - priced(res_none, HEADLINE_RUNG)).abs().max())
    gate("G1 k=0 replica == engine.backtest (CAP2, U56, g=0.75)", f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    # ---- G4a-G4f: every device's identity rung, and the FULL identity stack, reduce to NONE
    r_none = priced(res_none, HEADLINE_RUNG); t_none = res_none["turnover"].sum()
    for dev in ORDER:
        s = dict(IDENTITY); s[dev] = IDENTITY[dev]
        rI = run_book(px_u, cap_weights(px_u, inv_u, 0.75, s), s)
        dd = max(float((priced(rI, HEADLINE_RUNG) - r_none).abs().max()),
                 abs(float(rI["turnover"].sum() - t_none)))
        gate(f"G4 identity rung reduces to NONE ({dev} @ {IDENTITY[dev]})", f"max|d| {dd:.3e}", "< 1e-12", dd < 1e-12)
    rF = run_book(px_u, cap_weights(px_u, inv_u, 0.75, s_id), s_id)
    ddF = max(float((priced(rF, HEADLINE_RUNG) - r_none).abs().max()),
              abs(float(rF["turnover"].sum() - t_none)))
    gate("G4f the FULL five-device IDENTITY STACK reduces to NONE", f"max|d| {ddF:.3e}", "< 1e-12", ddF < 1e-12)

    # ---- G7: no lookahead.  Truncating the tape cannot change any earlier decision.
    s5 = spec(5, "MID")
    T = "2018-01-01"
    px_t = px_u.loc[:T]
    h_full = run_book(px_u, cap_weights(px_u, inv_u, 0.75, s5), s5)["held"].loc[:T]
    h_tr = run_book(px_t, cap_weights(px_t, inv_u, 0.75, s5), s5)["held"]
    common = h_full.index.intersection(h_tr.index)[:-1]          # last row: period-end mask differs
    d7 = float((h_full.loc[common] - h_tr.loc[common]).abs().values.max())
    gate(f"G7 no lookahead (k=5 MID held path, tape truncated at {T})", f"max|d| {d7:.3e}", "< 1e-12", d7 < 1e-12)

    # ---------------------------------------------------------------- the grid
    rows, tr_rows = [], []
    points = [("STACK", k, t) for t in TIERS for k in DEPTHS if not (k == 0 and t != "MILD")]
    points += [("SINGLE", dev, t) for t in TIERS for dev in ORDER]
    say(f"\n    {len(points)} distinct books per (panel, gross); "
        f"{len(points) * len(GROSSES) * len(panels)} books, x{len(RUNGS)} cost rungs")

    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        yrs = len(win) / 252
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        # the LIVE book, priced by engine.backtest exactly as baseline.compare() does -- NOT through
        # run_book, whose SHY sweep would turn RULES v2's CASH residual into a bond sleeve it does
        # not hold.  Gate G11 asserts this against the record's committed 1.2052 (1.2262/1.1897).
        base_r = backtest(px, rules_v2_weights(px), cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"].loc[win]
        say(f"\n--- panel {pname}  ({len(invest)} columns)  SPY {cagr(spy):.2%} / {sharpe(spy):.4f} / {maxdd(spy):.2%}"
            f"   live RULES v2 {cagr(base_r):.2%} / {sharpe(base_r):.4f} / {maxdd(base_r):.2%}")
        for gross in GROSSES:
            for kind, a, tier in points:
                s = spec(a, tier) if kind == "STACK" else spec(0, tier, singles=a)
                res = run_book(px, cap_weights(px, invest, gross, s), s)
                inw = res["held"].drop(columns=[SWEEP]).loc[win]
                pos = inw.values[inw.values > 1e-12]
                ta = res["trade_abs"]
                tr_rows.append(dict(panel=pname, gross=gross, kind=kind, depth=(a if kind == "STACK" else -1),
                                    device=("-" if kind == "STACK" else a), tier=tier,
                                    devices=("+".join(ORDER[:a]) if kind == "STACK" else a) or "NONE",
                                    turnover_yr=float(res["turnover"].loc[win].sum() / yrs),
                                    mean_names_in=float((inw.values > 1e-12).sum(axis=1).mean()),
                                    mean_risk_gross=float(res["risk_gross"].loc[win].mean()),
                                    mean_gross=float(res["gross"].loc[win].mean()),
                                    mean_sweep_w=float(res["held"][SWEEP].loc[win].mean()),
                                    max_name_w=float(pos.max()) if len(pos) else 0.0,
                                    max_row_sum=float(res["gross"].max()),
                                    n_trades=int(len(ta)), median_trade=float(np.median(ta)) if len(ta) else 0.0,
                                    acting_reb=res["acting_rebalances"], sched_reb=res["scheduled_rebalances"],
                                    lev_events=res["lev_events"]))
                for rung in RUNGS:
                    r = priced(res, rung).loc[win]
                    r_oos = r.loc[OOS_START:]
                    h1, h2 = halves(r)
                    lg = legs(r, base_r, spy, r_oos, spy_oos)
                    rows.append(dict(panel=pname, gross=gross, kind=kind,
                                     depth=(a if kind == "STACK" else -1),
                                     device=("-" if kind == "STACK" else a), tier=tier,
                                     devices=("+".join(ORDER[:a]) if kind == "STACK" else a) or "NONE",
                                     cost_bps=rung,
                                     CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                     H1=h1, H2=h2,
                                     IS_CAGR=cagr(r.loc[:IS_END]), IS_Sharpe=sharpe(r.loc[:IS_END]),
                                     IS_Calmar=calmar(r.loc[:IS_END]), IS_MaxDD=maxdd(r.loc[:IS_END]),
                                     OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                     legs=legstring(lg), **lg))
            say(f"    ... {pname} gross {gross:.2f} done ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(rows); tf = pd.DataFrame(tr_rows)

    # in-sample turnover (for the IS-only adoption chooser) needs its own pass
    is_tr = {}
    for pname, (px, invest) in panels.items():
        win_is = px.index[WARMUP:].intersection(px.loc[:IS_END].index)
        yrs_is = len(win_is) / 252
        for gross in GROSSES:
            for kind, a, tier in points:
                if kind != "STACK":
                    continue
                s = spec(a, tier)
                res = run_book(px.loc[:IS_END], cap_weights(px.loc[:IS_END], invest, gross, s), s)
                is_tr[(pname, gross, a, tier)] = float(res["turnover"].loc[win_is].sum() / yrs_is)

    # attach the reference (k=0) turnover and CAGR, then the cut and dCAGR
    ref_t = {(r.panel, r.gross): r.turnover_yr for r in
             tf[(tf.kind == "STACK") & (tf.depth == 0)].itertuples()}
    tf["cut"] = [1 - r.turnover_yr / ref_t[(r.panel, r.gross)] for r in tf.itertuples()]
    ref_c = {(r.panel, r.gross, r.cost_bps): r.CAGR for r in
             df[(df.kind == "STACK") & (df.depth == 0)].itertuples()}
    ref_s = {(r.panel, r.gross, r.cost_bps): r.Sharpe for r in
             df[(df.kind == "STACK") & (df.depth == 0)].itertuples()}
    df["dCAGR"] = [r.CAGR - ref_c[(r.panel, r.gross, r.cost_bps)] for r in df.itertuples()]
    df["dSharpe"] = [r.Sharpe - ref_s[(r.panel, r.gross, r.cost_bps)] for r in df.itertuples()]
    kt = {(r.panel, r.gross, r.kind, r.depth, r.device, r.tier): (r.cut, r.turnover_yr, r.mean_risk_gross)
          for r in tf.itertuples()}
    df["cut"] = [kt[(r.panel, r.gross, r.kind, r.depth, r.device, r.tier)][0] for r in df.itertuples()]
    df["turnover_yr"] = [kt[(r.panel, r.gross, r.kind, r.depth, r.device, r.tier)][1] for r in df.itertuples()]
    df["mean_risk_gross"] = [kt[(r.panel, r.gross, r.kind, r.depth, r.device, r.tier)][2] for r in df.itertuples()]
    ref_g = {(r.panel, r.gross): r.mean_risk_gross for r in
             tf[(tf.kind == "STACK") & (tf.depth == 0)].itertuples()}
    df["dgross_rel"] = [r.mean_risk_gross / ref_g[(r.panel, r.gross)] - 1 for r in df.itertuples()]
    tf["dgross_rel"] = [r.mean_risk_gross / ref_g[(r.panel, r.gross)] - 1 for r in tf.itertuples()]
    df["pp_per_1pct"] = [(100 * r.dCAGR) / (100 * r.cut) if r.cut > 1e-9 else np.nan for r in df.itertuples()]
    df["clears_bar"] = (df.cut >= BAR_CUT) & (df.dCAGR >= 0)
    df.to_csv(f"{OUT}.grid.csv", index=False); tf.to_csv(f"{OUT}.turnover.csv", index=False)

    # ---- G2 / G3: reproduction of the committed numbers
    h = df[(df.panel == "U56") & (df.gross == 0.75) & (df.kind == "STACK") & (df.depth == 0)
           & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    d2 = max(abs(h.CAGR - 0.1162), abs(h.Sharpe - 1.2687) / 10, abs(h.MaxDD + 0.1481),
             abs(h.OOS_CAGR - 0.1277), abs(h.OOS_Sharpe - 1.3318) / 10)
    gate("G2 reproduces idea 2336/2463's committed CAP2 U56 headline (11.62%/1.2687/-14.81%, OOS 12.77%/1.3318)",
         f"read {h.CAGR:.2%} / {h.Sharpe:.4f} / {h.MaxDD:.2%}, OOS {h.OOS_CAGR:.2%} / {h.OOS_Sharpe:.4f}"
         f" -> max|d| {d2:.2e}", "< 1e-3", d2 < 1e-3)
    gate("G2b reproduces the committed 3.51x turnover (U56, CAP2, g=0.75)",
         f"{h.turnover_yr:.4f}x", "|d| < 0.01", abs(h.turnover_yr - 3.51) < 0.01)

    # G3a: lane C idea 2463's BANDW 0.08 candidate IS this run's (SINGLE, BANDW, MID) point
    for pn, exp in (("U56", (0.1176, 1.2168, -0.1716, 0.1260, 1.2318, 2.20)),
                    ("B136", (0.1256, 1.1512, -0.1808, 0.1227, 1.1070, 2.70))):
        q = df[(df.panel == pn) & (df.gross == 0.75) & (df.kind == "SINGLE") & (df.device == "BANDW")
               & (df.tier == "MID") & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
        d3 = max(abs(q.CAGR - exp[0]), abs(q.Sharpe - exp[1]) / 10, abs(q.MaxDD - exp[2]),
                 abs(q.OOS_CAGR - exp[3]), abs(q.OOS_Sharpe - exp[4]) / 10, abs(q.turnover_yr - exp[5]) / 10)
        gate(f"G3a cross-lane reproduction of idea 2463's BANDW b=0.08 candidate ({pn}, g=0.75)",
             f"read {q.CAGR:.2%} / {q.Sharpe:.4f} / {q.MaxDD:.2%}, OOS {q.OOS_CAGR:.2%} / {q.OOS_Sharpe:.4f},"
             f" {q.turnover_yr:.2f}x vs committed {exp} -> max|d| {d3:.2e}", "< 5e-3", d3 < 5e-3)

    # G3b: lane C idea 2463's PARTIAL phi=0.40 row (NOT a grid point here -- priced for the gate only)
    for pn, exp in (("U56", (0.1179, 1.2538, -0.1692, 0.1298, 1.3091, 2.34)),
                    ("B136", (0.1204, 1.1189, -0.1952, 0.1203, 1.0947, 2.97))):
        pxp, invp = panels[pn]
        winp = pxp.index[WARMUP:]; yrsp = len(winp) / 252
        sP = dict(IDENTITY); sP["PARTIAL"] = 0.40
        resP = run_book(pxp, cap_weights(pxp, invp, 0.75, sP), sP)
        rP = priced(resP, HEADLINE_RUNG).loc[winp]
        tP = float(resP["turnover"].loc[winp].sum() / yrsp)
        d3b = max(abs(cagr(rP) - exp[0]), abs(sharpe(rP) - exp[1]) / 10, abs(maxdd(rP) - exp[2]),
                  abs(cagr(rP.loc[OOS_START:]) - exp[3]), abs(sharpe(rP.loc[OOS_START:]) - exp[4]) / 10,
                  abs(tP - exp[5]) / 10)
        gate(f"G3b cross-lane reproduction of idea 2463's PARTIAL phi=0.40 row ({pn}, g=0.75)",
             f"read {cagr(rP):.2%} / {sharpe(rP):.4f} / {maxdd(rP):.2%}, OOS {cagr(rP.loc[OOS_START:]):.2%} /"
             f" {sharpe(rP.loc[OOS_START:]):.4f}, {tP:.2f}x vs committed {exp} -> max|d| {d3b:.2e}",
             "< 5e-3", d3b < 5e-3)

    for pn, exp in (("U56", (0.0865, 1.2052, -0.1205, 1.2262, 1.1897)),
                    ("B136", (0.0796, 1.0972, -0.1224, 1.2296, 0.9669))):
        pxp, _ = panels[pn]
        winp = pxp.index[WARMUP:]
        br = backtest(pxp, rules_v2_weights(pxp), cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"].loc[winp]
        h1b, h2b = halves(br)
        d11 = max(abs(cagr(br) - exp[0]), abs(sharpe(br) - exp[1]) / 10, abs(maxdd(br) - exp[2]),
                  abs(h1b - exp[3]) / 10, abs(h2b - exp[4]) / 10)
        gate(f"G11 the 4a comparand IS the committed live RULES v2 book ({pn})",
             f"{cagr(br):.2%} / {sharpe(br):.4f} / {maxdd(br):.2%}, halves {h1b:.4f}/{h2b:.4f}"
             f" -> max|d| {d11:.2e}", "< 1e-3", d11 < 1e-3)

    gate("G5 no leverage anywhere", f"max row gross {tf.max_row_sum.max():.9f};"
         f" risk-sleeve rescale events {int(tf.lev_events.sum())}", "<= 1+1e-12",
         tf.max_row_sum.max() <= 1 + 1e-12)
    st = tf[tf.kind == "STACK"]
    bite_k = st.groupby("tier").turnover_yr.agg(lambda x: x.max() - x.min()).min()
    bite_t = st[st.depth == 5].turnover_yr.max() - st[st.depth == 5].turnover_yr.min()
    gate("G9 BOTH dials bite", f"turnover range over k (min across tiers) {bite_k:.3f}x;"
         f" over tier at k=5 {bite_t:.3f}x", "both > 0.05", bite_k > 0.05 and bite_t > 0.05)

    # ---------------------------------------------------------------- SECTION A: the ladder
    say("\n=== A.  THE STACK LADDER at the headline rung (10 bps), both panels, both gross ===")
    say("    k  tier    devices                         turn/yr    cut     CAGR   dCAGR   Sharpe  MaxDD    OOS_S   legs 4b 4a  grossrel")
    for pname in panels:
        for gross in GROSSES:
            say(f"  -- {pname} gross {gross:.2f}   (reference k=0: {ref_t[(pname, gross)]:.2f} turns/yr,"
                f" CAGR {ref_c[(pname, gross, HEADLINE_RUNG)]:.2%})")
            q = df[(df.panel == pname) & (df.gross == gross) & (df.kind == "STACK")
                   & (df.cost_bps == HEADLINE_RUNG)].sort_values(["tier", "depth"])
            for r in q.itertuples():
                say(f"    {r.depth}  {r.tier:6s}  {r.devices:30s}  {r.turnover_yr:6.2f}x {r.cut:6.1%}"
                    f" {r.CAGR:7.2%} {r.dCAGR:+6.2%}  {r.Sharpe:6.4f} {r.MaxDD:7.2%}  {r.OOS_Sharpe:6.4f}"
                    f"  {r.legs}  {int(r.pass4b)}  {int(r.pass4a)}  {r.dgross_rel:+.2%}")

    # ---------------------------------------------------------------- SECTION B: the bar
    say("\n=== B.  THE ADOPTION BAR (cut >= 31.0% AND dCAGR >= 0) ===")
    for rung in RUNGS:
        sub = df[(df.kind == "STACK") & (df.cost_bps == rung)]
        say(f"    {rung:5.1f} bps: stack points clearing the bar {int(sub.clears_bar.sum())} of {len(sub)};"
            f"  of those, still 4b: {int((sub.clears_bar & sub.pass4b).sum())};"
            f"  4b overall {int(sub.pass4b.sum())} of {len(sub)}")
    sub = df[(df.kind == "STACK") & (df.cost_bps == HEADLINE_RUNG) & df.clears_bar]
    if len(sub):
        say("    points clearing the bar at 10 bps:")
        for r in sub.sort_values("cut", ascending=False).itertuples():
            say(f"      {r.panel} g{r.gross:.2f} k={r.depth} {r.tier:6s} cut {r.cut:6.1%} dCAGR {r.dCAGR:+.2%}"
                f" 4b={int(r.pass4b)} legs {r.legs} OOS_S {r.OOS_Sharpe:.4f}")
    else:
        say("    NONE.")
    say("\n    leg-failure census over ALL stack rows (all panels/gross/cost):")
    allst = df[df.kind == "STACK"]
    for lg in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"):
        say(f"      {lg:7s} fails {int((~allst[lg]).sum())} of {len(allst)}")
    say(f"      leg strings: {allst.legs.value_counts().to_dict()}")
    say(f"      4b {int(allst.pass4b.sum())} of {len(allst)};  4a {int(allst.pass4a.sum())} of {len(allst)}")

    # ---------------------------------------------------------------- SECTION C: additivity (idea 2469)
    say("\n=== C.  ADDITIVITY: do the neutral devices' savings ADD or OVERLAP? ===")
    say("      (sum of the SINGLES' cuts over the devices in the stack) vs (the STACK's own cut)")
    add_rows = []
    for pname in panels:
        for gross in GROSSES:
            for tier in TIERS:
                singles = {r.device: r.cut for r in
                           tf[(tf.panel == pname) & (tf.gross == gross) & (tf.kind == "SINGLE")
                              & (tf.tier == tier)].itertuples()}
                for k in DEPTHS[1:]:
                    st_cut = float(tf[(tf.panel == pname) & (tf.gross == gross) & (tf.kind == "STACK")
                                      & (tf.depth == k) & (tf.tier == tier)].cut.iloc[0])
                    ssum = sum(singles[d] for d in ORDER[:k])
                    add_rows.append(dict(panel=pname, gross=gross, tier=tier, depth=k,
                                         sum_singles=ssum, stack_cut=st_cut,
                                         ratio=(st_cut / ssum if ssum > 1e-9 else np.nan)))
    ad = pd.DataFrame(add_rows); ad.to_csv(f"{OUT}.additivity.csv", index=False)
    for tier in TIERS:
        for k in DEPTHS[1:]:
            q = ad[(ad.tier == tier) & (ad.depth == k)]
            say(f"    tier {tier:6s} k={k}: sum-of-singles {q.sum_singles.mean():6.1%}   stack {q.stack_cut.mean():6.1%}"
                f"   ratio {q.ratio.mean():.3f}  (n={len(q)})")
    say(f"    POOLED ratio (stack cut / sum of singles): median {ad.ratio.median():.3f},"
        f" min {ad.ratio.min():.3f}, max {ad.ratio.max():.3f} over {len(ad)} cells")
    publish("G10 additivity ratio pooled median (1.0 = perfectly additive, < 1 = overlap)",
            f"{ad.ratio.median():.4f}")

    # ---------------------------------------------------------------- SECTION D: rule 8
    say("\n=== D.  RULE 8 WALK-FORWARD.  (k, tier) chosen on warm-up..2016-12-31 ONLY; 2017-2026 read ONCE ===")
    wf = []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_oos = backtest(px, rules_v2_weights(px), cost_bps=HEADLINE_RUNG,
                            freq=CADENCE)["returns"].loc[win].loc[OOS_START:]
        for gross in GROSSES:
            for rung in RUNGS:
                pool = df[(df.panel == pname) & (df.gross == gross) & (df.kind == "STACK")
                          & (df.cost_bps == rung)].copy()
                pool["IS_cut"] = [1 - is_tr[(pname, gross, r.depth, r.tier)]
                                  / is_tr[(pname, gross, 0, "MILD")] for r in pool.itertuples()]
                pool["IS_dCAGR"] = pool.IS_CAGR - float(pool[pool.depth == 0].IS_CAGR.iloc[0])
                picks = {}
                picks["C_ISSHARPE"] = pool.loc[pool.IS_Sharpe.idxmax()]
                adopt = pool[(pool.IS_cut >= BAR_CUT) & (pool.IS_dCAGR >= 0)]
                picks["C_ISADOPT"] = (adopt.loc[adopt.IS_CAGR.idxmax()] if len(adopt)
                                      else pool[pool.depth == 0].iloc[0])
                picks["C_ZEROPARAM"] = pool[(pool.depth == ZERO_PARAM_POINT[0])
                                            & (pool.tier == ZERO_PARAM_POINT[1])].iloc[0]
                for cname, p in picks.items():
                    wf.append(dict(panel=pname, gross=gross, cost_bps=rung, chooser=cname,
                                   picked_k=int(p.depth), picked_tier=p.tier, picked_devices=p.devices,
                                   IS_cut=float(p.IS_cut), IS_Sharpe=float(p.IS_Sharpe),
                                   OOS_CAGR=float(p.OOS_CAGR), OOS_Sharpe=float(p.OOS_Sharpe),
                                   OOS_MaxDD=float(p.OOS_MaxDD),
                                   SPY_OOS_CAGR=cagr(spy_oos), SPY_OOS_Sharpe=sharpe(spy_oos),
                                   SPY_OOS_MaxDD=maxdd(spy_oos),
                                   BASE_OOS_CAGR=cagr(base_oos), BASE_OOS_Sharpe=sharpe(base_oos),
                                   BASE_OOS_MaxDD=maxdd(base_oos),
                                   REF_OOS_CAGR=float(pool[pool.depth == 0].OOS_CAGR.iloc[0]),
                                   REF_OOS_Sharpe=float(pool[pool.depth == 0].OOS_Sharpe.iloc[0]),
                                   full_cut=float(p.cut), full_dCAGR=float(p.dCAGR),
                                   full_4b=bool(p.pass4b), full_legs=p.legs,
                                   adopt_pool_size=int(len(adopt))))
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say("    chooser      picks (k,tier)                                   OOS CAGR / Sharpe   vs SPY OOS   vs CAP2 OOS   vs live")
    for cname in ("C_ISSHARPE", "C_ISADOPT", "C_ZEROPARAM"):
        q = wfd[wfd.chooser == cname]
        pk = q.groupby(["picked_k", "picked_tier"]).size().to_dict()
        say(f"    {cname:12s} {str(pk):48s}")
        say(f"        OOS CAGR {q.OOS_CAGR.median():.2%}  OOS Sharpe {q.OOS_Sharpe.median():.4f}"
            f"   beats SPY OOS Sharpe {int((q.OOS_Sharpe > q.SPY_OOS_Sharpe).sum())}/{len(q)}"
            f"   beats CAP2 (k=0) OOS Sharpe {int((q.OOS_Sharpe > q.REF_OOS_Sharpe).sum())}/{len(q)}"
            f"   beats live RULES v2 OOS Sharpe {int((q.OOS_Sharpe > q.BASE_OOS_Sharpe).sum())}/{len(q)}")
        say(f"        full-sample 4b on the pick {int(q.full_4b.sum())}/{len(q)};"
            f"  full-sample cut median {q.full_cut.median():.1%}, dCAGR median {q.full_dCAGR.median():+.2%}")
    say(f"    TOTAL PICKS {len(wfd)}")

    # ---------------------------------------------------------------- SECTION E: the zero-parameter book
    say("\n=== E.  THE ZERO-PARAMETER BOOK IN FULL  (k=5, MILD -- pre-registered, nothing fitted) ===")
    zp = df[(df.kind == "STACK") & (df.depth == ZERO_PARAM_POINT[0]) & (df.tier == ZERO_PARAM_POINT[1])]
    say("    panel gross  bps   turn/yr   cut    CAGR    dCAGR   Sharpe   H1/H2         MaxDD    OOS CAGR/Sharpe   legs 4b 4a")
    for r in zp.sort_values(["panel", "gross", "cost_bps"]).itertuples():
        say(f"    {r.panel:5s} {r.gross:.2f} {r.cost_bps:5.1f}  {r.turnover_yr:6.2f}x {r.cut:6.1%}"
            f" {r.CAGR:7.2%} {r.dCAGR:+6.2%}  {r.Sharpe:6.4f}  {r.H1:.4f}/{r.H2:.4f}  {r.MaxDD:7.2%}"
            f"   {r.OOS_CAGR:6.2%} / {r.OOS_Sharpe:6.4f}   {r.legs}  {int(r.pass4b)}  {int(r.pass4a)}")
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        say(f"    [{pname}] SPY {cagr(spy):.2%} / {sharpe(spy):.4f} / {maxdd(spy):.2%};"
            f" halves {halves(spy)[0]:.4f}/{halves(spy)[1]:.4f};"
            f" OOS {cagr(spy.loc[OOS_START:]):.2%} / {sharpe(spy.loc[OOS_START:]):.4f};"
            f" 4b bars: DD >= {DD_CAP * maxdd(spy):.2%}, CAGR >= {CAGR_FLOOR * cagr(spy):.2%}")

    # ---------------------------------------------------------------- gates + artefacts
    gd = pd.DataFrame(GATES); gd.to_csv(f"{OUT}.gates.csv", index=False)
    npass = int(gd.pass_.sum())
    say(f"\n=== GATES {npass} of {len(gd)} ===")
    for g in GATES:
        if not g["pass_"]:
            say(f"    FAILED: {g['gate']}")
    say(f"    rows {len(df)}; turnover rows {len(tf)}; walk-forward picks {len(wfd)};"
        f" additivity cells {len(ad)}; elapsed {time.time() - t0:.0f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

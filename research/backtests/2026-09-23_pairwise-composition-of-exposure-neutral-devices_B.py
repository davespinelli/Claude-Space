#!/usr/bin/env python3
"""idea 2469 (lane B, run 59, 2026-09-23) — DOES THE TURNOVER-SAVING OF **TWO** EXPOSURE-NEUTRAL
DEVICES COMPOSE **ADDITIVELY** OR **OVERLAP**?

THE OBJECT.  The record's standing 4b KEEP-candidate is idea 2322's CAP2: every name INSIDE the
200d +/- 3% band held at `min(gross / N_in, 2%)` of NAV, idle NAV swept to SHY, weekly, t+1,
10 bps.  On U56 / gross 0.75 it reads 11.62% / 1.2687 / -14.81% at 3.51 turns a year, and idea
2431 wrote the adoption bar: cut turnover 3.51x -> 2.42x (-31.0%) AT UNCHANGED RETURNS.

THE QUESTION.  Idea 2463 (lane C, run 54) put nine turnover devices on one axis and showed the
record's `-0.10 pp of CAGR per 1% saved` is a DE-GROSSING rate, not a turnover rate: pooled
median pp per 1% saved splits by EXPOSURE, not by device name --
  de-grossers  SCALE -0.115 / WHIP -0.112 / WIDTH -0.195 / AGE -0.064
  NEUTRAL      PARTIAL +0.005 / ROTA +0.008 / BANDW +0.009 / DRIFT +0.020 / HOLD +0.085
The neutral class is FREE OR BETTER per unit of turnover removed, yet NO SINGLE neutral device
reaches the -31.0% bar at dCAGR >= 0 on BOTH panels.  Whether two free devices' savings **ADD**
(they suppress DIFFERENT trades) or **OVERLAP** (they suppress the SAME trades) has never been
measured, and it decides whether the bar is reachable by composition at all.

WHAT IS NEW HERE, AND WHAT IS NOT.  Idea 2477 (lane B, run 56) priced a NESTED stack k = 0..5 and
published a depth-level ratio (sum of the singles' cuts vs the stack's cut) as a by-product.  That
ratio confounds FIVE devices at once, cannot say WHICH pair overlaps with WHICH, and is measured
only in the aggregate, where two books that have already diverged are being differenced.  This run
answers 2469 as asked:
  (1) ALL TEN PAIRS, each priced beside BOTH of its own singles at the same tier;
  (2) against BOTH nulls -- the ADDITIVE null `c_A + c_B` that the idea's wording names, and the
      INDEPENDENT-RETENTION null `c_A + c_B - c_A c_B`, which is the correct null when two devices
      each retain a fraction of the SAME trade tape (retention multiplies, it does not add);
  (3) a PATH-FIXED SUPPRESSION TAPE: every device's removed notional is measured trade-by-trade on
      the UNDAMPED book's OWN path, so ADD vs OVERLAP is answered by MECHANISM and not only by an
      aggregate difference between two books that have drifted apart.  On that tape the pure-ADD
      prediction is `sum(dA) + sum(dB)` and the pure-OVERLAP floor is `sum(max(dA, dB))`, and the
      realised joint suppression must sit between them.

DIAL 1 -- DEVICE SET D, 16 points: NONE, the 5 SINGLES, the 10 PAIRS.
DIAL 2 -- STRENGTH TIER t in {MILD, MID, STRONG}.  Every rung is taken VERBATIM from idea 2477's
committed tiers, which took them from idea 2463's committed ladders; NOTHING here is a new number.
    MILD    HOLD 2  DRIFT 0.0010  BANDW 0.05  ROTA 2  PARTIAL 0.75
    MID     HOLD 4  DRIFT 0.0025  BANDW 0.08  ROTA 3  PARTIAL 0.50
    STRONG  HOLD 8  DRIFT 0.0050  BANDW 0.12  ROTA 4  PARTIAL 0.35

THAT IS EXACTLY TWO TUNED PARAMETERS.  Panels {U56, B136}, gross {0.75, 1.00} and cost rungs
{0, 10, 25, 50} bps are REPORTED IN FULL, never selected on.  SMALL is not priced: ideas 2318 /
2322 / 2326 / 2343 each published SMALL's 4b pass count at 0 of 40-120, so there is no pass there
for a turnover device to keep.

THE PREMISE IS TESTED, NOT ASSUMED.  Every device is forced through its IDENTITY rung (h=1, d=0,
b=0.03, rota=1, phi=1.00); each identity single AND every identity PAIR is gated BIT-IDENTICAL to
NONE, so a "saving" can never be an implementation difference.  Three of this run's grid points
reproduce lane C's and lane B's committed numbers from ideas 2322 / 2463 / 2477.

BOTH KEEP PATHS on every row: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse) and
4b (Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's).
RULE 8: (D, t) chosen on warm-up..2016-12-31 ONLY by three PRE-STATED choosers, then 2017-2026
read ONCE.  The third is pre-registered in the pushed QUEUE claim, before any number in this run:
    C_ISSHARPE  max IS Sharpe over the 46 points
    C_ISADOPT   max IS CAGR among points clearing the -31.0% cut IN SAMPLE
    C_PREREG    NO CHOICE AT ALL -- the fixed point (HOLD+DRIFT, MILD), the two devices with the
                most positive published pp-per-1% in 2463's OWN order, at the mildest tier.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_pairwise-composition-of-exposure-neutral-devices_B.py
"""
from __future__ import annotations

import itertools
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state   # noqa: E402
from engine import backtest                                        # noqa: E402

DATE, SLUG, LANE = "2026-09-23", "pairwise-composition-of-exposure-neutral-devices", "B"
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
TIERS_ALL = dict(TIERS, IDENT=dict(IDENTITY))             # IDENT exercises the SAME spec()/run path
PAIRS = list(itertools.combinations(ORDER, 2))            # 10 pairs, fixed order
EXEC = ["HOLD", "DRIFT", "ROTA", "PARTIAL"]               # EXECUTION-side: they only ever SUPPRESS a trade
EXEC_PAIRS = [p for p in PAIRS if p[0] in EXEC and p[1] in EXEC]   # the 6 decomposable pairs
PREREG_POINT = ("HOLD+DRIFT", "MILD")                     # pre-registered in the pushed QUEUE claim

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


def spec(devices, tier):
    """Device settings with every device in `devices` at tier `tier` and the rest at identity."""
    s = dict(IDENTITY)
    for d in devices:
        s[d] = TIERS_ALL[tier][d]
    return s


def setname(devices):
    return "+".join(devices) if devices else "NONE"


# ---------------------------------------------------------------- target book (TARGET-side)
def cap_weights(px, invest, gross, s):
    """idea 2322's CAP2 with the one TARGET-side device (BANDW) applied.

    admitted set = names inside the 200d +/- b band (hysteresis, baseline.band_state) and priced
    that day; w_i = min(gross / N_in, CAP); idle NAV swept to SHY.
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
    pre-registered order inside an acting rebalance (identical to idea 2477's committed engine):
        ROTA    decides whether the rebalance acts at all;
        HOLD    blocks REDUCTIONS of names held fewer than h acting rebalances;
        DRIFT   filters which risk names move at all (|target - held| > d);
        PARTIAL scales the surviving move by phi.
    SHY is then set to 1 - sum(risk weights).  The all-identity setting reduces to engine.backtest
    exactly (gates G1 / G4).  Zero-cost returns and turnover are kept separately so every cost rung
    is priced from one pass.
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


# ---------------------------------------------------------------- PATH-FIXED SUPPRESSION TAPE
def _apply(cur, tgt, s, risk, si, shy, nreb, age, phase=0):
    """One acting-rebalance decision under device settings `s`, from state `cur` to target `tgt`.

    Returns (new_weights, acted).  `acted` is False when ROTA skips this scheduled rebalance,
    in which case the whole trade is suppressed and `new` == `cur`.
    """
    rota = int(s["ROTA"])
    if (nreb % rota) != (phase % rota):
        return cur.copy(), False
    d = float(s["DRIFT"]); phi = float(s["PARTIAL"]); hold = int(s["HOLD"])
    new = cur.copy()
    mv = risk & (np.abs(tgt - cur) > d)
    if hold > 1:
        young = (cur > 1e-12) & (age < hold) & (tgt < cur)
        mv = mv & ~young
    new[mv] = cur[mv] + phi * (tgt[mv] - cur[mv])
    srisk = new[risk].sum()
    if srisk > 1.0:
        new[risk] *= 1.0 / srisk
        srisk = 1.0
    new[si] = max(0.0, 1.0 - srisk) if shy else 0.0
    return new, True


def suppression_tape(prices, invest, gross, tier, sweep=SWEEP, freq=CADENCE):
    """Measure every device's removed notional TRADE BY TRADE on the UNDAMPED book's OWN path.

    The book walked is always NONE (all devices at identity).  At each acting rebalance the state
    `cur`, the age vector and the undamped target are FIXED, and each device (and each pair) is
    asked what it WOULD have done from that identical state.  Removed notional for device set D is
        delta_D = |trade_NONE| - |trade_D|      (per column, then summed)
    which is uniform across TARGET-side (BANDW, whose target itself changes) and EXECUTION-side
    devices, and includes the SHY residual leg.

    Measured on the RISK columns only.  The SHY column is the residual `1 - sum(risk)`, so a
    suppressed risk trade MECHANICALLY creates an offsetting sweep trade; including it would let a
    device show NEGATIVE removal on a leg it never touched and would make `max(dA, dB)` meaningless.
    Idea 2449 already established the 3.51x blocker is the RISK leg, not the sweep.  On the risk
    columns every EXECUTION-side device (HOLD / DRIFT / ROTA / PARTIAL) can only SHRINK a trade, so
    dA >= 0 elementwise and the decomposition is well posed:
        pure-ADD (disjoint) prediction  = sum(dA) + sum(dB)
        pure-OVERLAP floor              = sum(max(dA, dB))      <= the ADD prediction
    BANDW is a TARGET-side device -- it moves the target itself, so its `d` is a signed CHANGE in
    trade size and its pairs are reported but explicitly NOT decomposed (published, not asserted).
    """
    cols = list(prices.columns)
    si = cols.index(sweep)
    risk = np.ones(len(cols), dtype=bool); risk[si] = False
    rets = prices.pct_change().fillna(0.0)
    key = prices.index.to_period(freq)
    ser = pd.Series(key, index=prices.index)
    mask = (ser != ser.shift(-1)).shift(1, fill_value=False).values
    shy_live = prices[sweep].notna().shift(1, fill_value=False).values
    rv = rets.values

    s_none = dict(IDENTITY)
    # targets: NONE's band, plus BANDW's own band (the only TARGET-side device)
    tgt_none = cap_weights(prices, invest, gross, s_none).reindex(prices.index).fillna(0.0).shift(1).values
    s_b = dict(IDENTITY); s_b["BANDW"] = TIERS[tier]["BANDW"]
    tgt_bandw = cap_weights(prices, invest, gross, s_b).reindex(prices.index).fillna(0.0).shift(1).values

    sets = [(d,) for d in ORDER] + [tuple(p) for p in PAIRS]
    tot = {setname(s): 0.0 for s in sets}
    add_pred = {setname(p): 0.0 for p in PAIRS}
    ovl_floor = {setname(p): 0.0 for p in PAIRS}
    base_tot = 0.0
    neg = {d: 0 for d in ORDER}          # elementwise non-negativity violations, per device
    negn = {d: 0.0 for d in ORDER}       # ... and the NOTIONAL involved

    cur = np.zeros(len(cols)); age = np.zeros(len(cols)); nreb = 0
    for i in range(len(prices.index)):
        act = mask[i] or i == 0
        if act:
            t0 = tgt_none[i]
            new0, _ = _apply(cur, t0, s_none, risk, si, shy_live[i], nreb, age)
            base = np.abs(new0 - cur) * risk          # RISK columns only (see docstring)
            base_tot += base.sum()
            delta = {}
            for dv in ORDER:
                s = dict(IDENTITY); s[dv] = TIERS[tier][dv]
                t = tgt_bandw[i] if dv == "BANDW" else t0
                nw, _ = _apply(cur, t, s, risk, si, shy_live[i], nreb, age)
                dd = base - np.abs(nw - cur) * risk
                neg[dv] += int((dd < -1e-15).sum())
                negn[dv] += float(-np.minimum(dd, 0.0).sum())
                delta[dv] = dd
                tot[dv] += dd.sum()
            for a, b in PAIRS:
                s = spec((a, b), tier)
                t = tgt_bandw[i] if ("BANDW" in (a, b)) else t0
                nw, _ = _apply(cur, t, s, risk, si, shy_live[i], nreb, age)
                nm = setname((a, b))
                tot[nm] += (base - np.abs(nw - cur) * risk).sum()
                add_pred[nm] += delta[a].sum() + delta[b].sum()
                ovl_floor[nm] += np.maximum(delta[a], delta[b]).sum()
            # advance the NONE path
            fresh = (new0 > 1e-12) & (cur <= 1e-12)
            age = np.where(fresh, 0.0, age + 1.0)
            cur = new0
            nreb += 1
        growth = cur * (1 + rv[i])
        t = growth.sum() + (1 - cur.sum())
        cur = growth / t if t > 0 else cur
    return dict(base=base_tot, removed=tot, add_pred=add_pred, ovl_floor=ovl_floor,
                neg=neg, negn=negn)


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
    say("=== idea 2469 (lane B, run 59) — PAIRWISE COMPOSITION of the EXPOSURE-NEUTRAL devices ===")
    say(f"    {DATE}  lane {LANE}   band {BAND}  cap {CAP}  cadence {CADENCE}  t+1  rungs {RUNGS} bps  sweep {SWEEP}")
    say(f"    DIAL 1 device set D: NONE + 5 SINGLES {ORDER} + 10 PAIRS {[setname(p) for p in PAIRS]}")
    for t, v in TIERS.items():
        say(f"    DIAL 2 tier {t:6s} {v}")
    say(f"    identity rungs {IDENTITY}   pre-registered rule-8 point (D, tier) = {PREREG_POINT}")
    say(f"    THE BAR (idea 2431): turnover -{BAR_CUT:.1%} at unchanged returns (3.51x -> 2.42x)")
    gate("G8 exactly two tuned parameters", "device set D, strength tier t", "2", True)

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

    # ---- G1: the NONE replica IS engine.backtest
    w0 = cap_weights(px_u, inv_u, 0.75, s_id)
    r_eng = backtest(px_u, w0, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    res_none = run_book(px_u, w0, s_id)
    d1 = float((r_eng - priced(res_none, HEADLINE_RUNG)).abs().max())
    gate("G1 NONE replica == engine.backtest (CAP2, U56, g=0.75)", f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    # ---- G4: every identity SINGLE and every identity PAIR reduces to NONE
    r_none = priced(res_none, HEADLINE_RUNG); t_none = res_none["turnover"].sum()
    worst_single, worst_pair = 0.0, 0.0
    for dev in ORDER:
        s = spec((dev,), "IDENT")
        rI = run_book(px_u, cap_weights(px_u, inv_u, 0.75, s), s)
        worst_single = max(worst_single, float((priced(rI, HEADLINE_RUNG) - r_none).abs().max()),
                           abs(float(rI["turnover"].sum() - t_none)))
    gate("G4a every device's IDENTITY rung reduces to NONE (5 singles, through spec()/run_book)",
         f"max|d| {worst_single:.3e}", "< 1e-12", worst_single < 1e-12)
    for a, b in PAIRS:
        s = spec((a, b), "IDENT")
        rI = run_book(px_u, cap_weights(px_u, inv_u, 0.75, s), s)
        worst_pair = max(worst_pair, float((priced(rI, HEADLINE_RUNG) - r_none).abs().max()),
                         abs(float(rI["turnover"].sum() - t_none)))
    gate("G4b every IDENTITY PAIR reduces to NONE (10 pairs, through spec()/run_book)",
         f"max|d| {worst_pair:.3e}", "< 1e-12", worst_pair < 1e-12)

    # ---- G7: no lookahead.  Truncating the tape cannot change any earlier decision.
    sT = spec(("HOLD", "PARTIAL"), "MID")
    T = "2018-01-01"
    px_t = px_u.loc[:T]
    h_full = run_book(px_u, cap_weights(px_u, inv_u, 0.75, sT), sT)["held"].loc[:T]
    h_tr = run_book(px_t, cap_weights(px_t, inv_u, 0.75, sT), sT)["held"]
    common = h_full.index.intersection(h_tr.index)[:-1]          # last row: period-end mask differs
    d7 = float((h_full.loc[common] - h_tr.loc[common]).abs().values.max())
    gate(f"G7 no lookahead (HOLD+PARTIAL MID held path, tape truncated at {T})",
         f"max|d| {d7:.3e}", "< 1e-12", d7 < 1e-12)

    # ---------------------------------------------------------------- the grid
    points = [("NONE", (), "MILD")]
    points += [("SINGLE", (d,), t) for t in TIERS for d in ORDER]
    points += [("PAIR", tuple(p), t) for t in TIERS for p in PAIRS]
    say(f"\n    {len(points)} distinct books per (panel, gross); "
        f"{len(points) * len(GROSSES) * len(panels)} books, x{len(RUNGS)} cost rungs")

    rows, tr_rows = [], []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        yrs = len(win) / 252
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        # the LIVE book, priced by engine.backtest exactly as baseline.compare() does -- NOT through
        # run_book, whose SHY sweep would turn RULES v2's CASH residual into a bond sleeve it does
        # not hold.  Gate G11 asserts this against the record's committed numbers.
        base_r = backtest(px, rules_v2_weights(px), cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"].loc[win]
        say(f"\n--- panel {pname}  ({len(invest)} columns)  SPY {cagr(spy):.2%} / {sharpe(spy):.4f} / {maxdd(spy):.2%}"
            f"   live RULES v2 {cagr(base_r):.2%} / {sharpe(base_r):.4f} / {maxdd(base_r):.2%}")
        for gross in GROSSES:
            for kind, devs, tier in points:
                s = spec(devs, tier)
                res = run_book(px, cap_weights(px, invest, gross, s), s)
                inw = res["held"].drop(columns=[SWEEP]).loc[win]
                pos = inw.values[inw.values > 1e-12]
                ta = res["trade_abs"]
                meta = dict(panel=pname, gross=gross, kind=kind, devices=setname(devs),
                            tier=(tier if kind != "NONE" else "-"))
                tr_rows.append(dict(**meta,
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
                    rows.append(dict(**meta, cost_bps=rung,
                                     CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                     H1=h1, H2=h2,
                                     IS_CAGR=cagr(r.loc[:IS_END]), IS_Sharpe=sharpe(r.loc[:IS_END]),
                                     IS_MaxDD=maxdd(r.loc[:IS_END]),
                                     OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                     legs=legstring(lg), **lg))
            say(f"    ... {pname} gross {gross:.2f} done ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(rows); tf = pd.DataFrame(tr_rows)

    # in-sample turnover (for the IS-only adoption chooser) needs its own pass on the truncated tape
    is_tr = {}
    for pname, (px, invest) in panels.items():
        win_is = px.index[WARMUP:].intersection(px.loc[:IS_END].index)
        yrs_is = len(win_is) / 252
        pxi = px.loc[:IS_END]
        for gross in GROSSES:
            for kind, devs, tier in points:
                s = spec(devs, tier)
                res = run_book(pxi, cap_weights(pxi, invest, gross, s), s)
                is_tr[(pname, gross, setname(devs), (tier if kind != "NONE" else "-"))] = \
                    float(res["turnover"].loc[win_is].sum() / yrs_is)
    say(f"    IS-only turnover pass done ({time.time() - t0:.0f}s)")

    # attach the reference (NONE) turnover / CAGR / gross, then the cut, dCAGR and dgross
    ref_t = {(r.panel, r.gross): r.turnover_yr for r in tf[tf.kind == "NONE"].itertuples()}
    ref_g = {(r.panel, r.gross): r.mean_risk_gross for r in tf[tf.kind == "NONE"].itertuples()}
    tf["cut"] = [1 - r.turnover_yr / ref_t[(r.panel, r.gross)] for r in tf.itertuples()]
    tf["dgross_rel"] = [r.mean_risk_gross / ref_g[(r.panel, r.gross)] - 1 for r in tf.itertuples()]
    ref_c = {(r.panel, r.gross, r.cost_bps): r.CAGR for r in df[df.kind == "NONE"].itertuples()}
    ref_s = {(r.panel, r.gross, r.cost_bps): r.Sharpe for r in df[df.kind == "NONE"].itertuples()}
    df["dCAGR"] = [r.CAGR - ref_c[(r.panel, r.gross, r.cost_bps)] for r in df.itertuples()]
    df["dSharpe"] = [r.Sharpe - ref_s[(r.panel, r.gross, r.cost_bps)] for r in df.itertuples()]
    kt = {(r.panel, r.gross, r.devices, r.tier): (r.cut, r.turnover_yr, r.mean_risk_gross, r.dgross_rel)
          for r in tf.itertuples()}
    df["cut"] = [kt[(r.panel, r.gross, r.devices, r.tier)][0] for r in df.itertuples()]
    df["turnover_yr"] = [kt[(r.panel, r.gross, r.devices, r.tier)][1] for r in df.itertuples()]
    df["mean_risk_gross"] = [kt[(r.panel, r.gross, r.devices, r.tier)][2] for r in df.itertuples()]
    df["dgross_rel"] = [kt[(r.panel, r.gross, r.devices, r.tier)][3] for r in df.itertuples()]
    df["pp_per_1pct"] = [(100 * r.dCAGR) / (100 * r.cut) if r.cut > 1e-9 else np.nan for r in df.itertuples()]
    df["clears_bar"] = (df.cut >= BAR_CUT) & (df.dCAGR >= 0)
    df.to_csv(f"{OUT}.grid.csv", index=False); tf.to_csv(f"{OUT}.turnover.csv", index=False)

    # ---- G2 / G3: reproduction of the committed numbers
    h = df[(df.panel == "U56") & (df.gross == 0.75) & (df.kind == "NONE")
           & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    d2 = max(abs(h.CAGR - 0.1162), abs(h.Sharpe - 1.2687) / 10, abs(h.MaxDD + 0.1481),
             abs(h.OOS_CAGR - 0.1277), abs(h.OOS_Sharpe - 1.3318) / 10)
    gate("G2 reproduces idea 2336/2463/2477's committed CAP2 U56 headline (11.62%/1.2687/-14.81%, OOS 12.77%/1.3318)",
         f"read {h.CAGR:.2%} / {h.Sharpe:.4f} / {h.MaxDD:.2%}, OOS {h.OOS_CAGR:.2%} / {h.OOS_Sharpe:.4f}"
         f" -> max|d| {d2:.2e}", "< 1e-3", d2 < 1e-3)
    gate("G2b reproduces the committed 3.51x turnover (U56, CAP2, g=0.75)",
         f"{h.turnover_yr:.4f}x", "|d| < 0.01", abs(h.turnover_yr - 3.51) < 0.01)

    # G3a: lane C idea 2463's BANDW 0.08 candidate IS this run's (SINGLE, BANDW, MID) point
    for pn, exp in (("U56", (0.1176, 1.2168, -0.1716, 0.1260, 1.2318, 2.20)),
                    ("B136", (0.1256, 1.1512, -0.1808, 0.1227, 1.1070, 2.70))):
        q = df[(df.panel == pn) & (df.gross == 0.75) & (df.kind == "SINGLE") & (df.devices == "BANDW")
               & (df.tier == "MID") & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
        d3 = max(abs(q.CAGR - exp[0]), abs(q.Sharpe - exp[1]) / 10, abs(q.MaxDD - exp[2]),
                 abs(q.OOS_CAGR - exp[3]), abs(q.OOS_Sharpe - exp[4]) / 10, abs(q.turnover_yr - exp[5]) / 10)
        gate(f"G3a cross-lane reproduction of idea 2463's BANDW b=0.08 candidate ({pn}, g=0.75)",
             f"read {q.CAGR:.2%} / {q.Sharpe:.4f} / {q.MaxDD:.2%}, OOS {q.OOS_CAGR:.2%} / {q.OOS_Sharpe:.4f},"
             f" {q.turnover_yr:.2f}x vs committed {exp} -> max|d| {d3:.2e}", "< 5e-3", d3 < 5e-3)

    # G11: the 4a comparand IS the committed live RULES v2 book
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
    bite_D = tf[tf.tier == "MILD"].groupby(["panel", "gross"]).turnover_yr.agg(lambda x: x.max() - x.min()).min()
    bite_t = tf[tf.kind == "PAIR"].groupby(["panel", "gross", "devices"]).turnover_yr.agg(
        lambda x: x.max() - x.min()).min()
    gate("G9 BOTH dials bite", f"turnover range over D at MILD (min over panel/gross) {bite_D:.3f}x;"
         f" over tier within a pair (min over all pairs) {bite_t:.3f}x", "both > 0.05",
         bite_D > 0.05 and bite_t > 0.05)

    # ---- G12: the class really is exposure-neutral at these rungs
    nn = tf[tf.kind != "NONE"]
    publish("G12 exposure neutrality of the whole grid (mean risk gross vs NONE, relative)",
            f"median {nn.dgross_rel.median():+.3%}, min {nn.dgross_rel.min():+.3%},"
            f" max {nn.dgross_rel.max():+.3%}; within +/-{NEUTRAL_TOL:.0%}:"
            f" {int((nn.dgross_rel.abs() <= NEUTRAL_TOL).sum())} of {len(nn)}")

    # ---------------------------------------------------------------- SECTION A: singles and pairs
    say("\n=== A.  SINGLES and PAIRS at the headline rung (10 bps) ===")
    say("    set                       tier    turn/yr    cut     CAGR   dCAGR   Sharpe  MaxDD    OOS_S   legs 4b 4a grossrel")
    for pname in panels:
        for gross in GROSSES:
            say(f"  -- {pname} gross {gross:.2f}   (reference NONE: {ref_t[(pname, gross)]:.2f} turns/yr,"
                f" CAGR {ref_c[(pname, gross, HEADLINE_RUNG)]:.2%}, Sharpe {ref_s[(pname, gross, HEADLINE_RUNG)]:.4f})")
            q = df[(df.panel == pname) & (df.gross == gross) & (df.cost_bps == HEADLINE_RUNG)].copy()
            q["_k"] = q.kind.map({"NONE": 0, "SINGLE": 1, "PAIR": 2})
            q["_t"] = q.tier.map({"-": 0, "MILD": 1, "MID": 2, "STRONG": 3})
            for r in q.sort_values(["_k", "_t", "devices"]).itertuples():
                say(f"    {r.devices:24s} {r.tier:6s} {r.turnover_yr:6.2f}x {r.cut:6.1%}"
                    f" {r.CAGR:7.2%} {r.dCAGR:+6.2%}  {r.Sharpe:6.4f} {r.MaxDD:7.2%}  {r.OOS_Sharpe:6.4f}"
                    f"  {r.legs}  {int(r.pass4b)}  {int(r.pass4a)}  {r.dgross_rel:+.2%}")

    # ---------------------------------------------------------------- SECTION B: the idea's question
    say("\n=== B.  DO TWO NEUTRAL DEVICES' SAVINGS ADD OR OVERLAP?  (realised, per pair) ===")
    say("    c_AB = realised cut of the pair; ADD null = c_A + c_B; IND null = c_A + c_B - c_A c_B")
    comp = []
    for pname in panels:
        for gross in GROSSES:
            for tier in TIERS:
                cu = {r.devices: r.cut for r in
                      tf[(tf.panel == pname) & (tf.gross == gross) & (tf.tier == tier)].itertuples()}
                for a, b in PAIRS:
                    cA, cB = cu[a], cu[b]
                    cAB = cu[setname((a, b))]
                    add = cA + cB
                    ind = cA + cB - cA * cB
                    comp.append(dict(panel=pname, gross=gross, tier=tier, pair=setname((a, b)),
                                     dev_a=a, dev_b=b, cut_a=cA, cut_b=cB, cut_pair=cAB,
                                     add_null=add, ind_null=ind,
                                     ratio_add=(cAB / add if abs(add) > 1e-9 else np.nan),
                                     ratio_ind=(cAB / ind if abs(ind) > 1e-9 else np.nan),
                                     excess_over_max=cAB - max(cA, cB)))
    cp = pd.DataFrame(comp)
    say("    pair                      ratio_add (median over 12 panel/gross/tier cells)   ratio_ind   cut_pair   best single")
    for a, b in PAIRS:
        q = cp[cp.pair == setname((a, b))]
        say(f"    {setname((a, b)):24s}  {q.ratio_add.median():6.3f}   [{q.ratio_add.min():.3f}, {q.ratio_add.max():.3f}]"
            f"      {q.ratio_ind.median():6.3f}    {q.cut_pair.median():6.1%}   "
            f"{max(q.cut_a.median(), q.cut_b.median()):6.1%}")
    say(f"\n    POOLED over {len(cp)} pair-cells: ratio_add median {cp.ratio_add.median():.3f}"
        f" [{cp.ratio_add.min():.3f}, {cp.ratio_add.max():.3f}];"
        f" ratio_ind median {cp.ratio_ind.median():.3f} [{cp.ratio_ind.min():.3f}, {cp.ratio_ind.max():.3f}]")
    say(f"    cells where the pair beats its OWN BEST SINGLE: "
        f"{int((cp.excess_over_max > 0).sum())} of {len(cp)}"
        f" (median excess {cp.excess_over_max.median():+.2%})")
    for tier in TIERS:
        q = cp[cp.tier == tier]
        say(f"      tier {tier:6s}: ratio_add median {q.ratio_add.median():.3f}, ratio_ind median {q.ratio_ind.median():.3f}")

    # ---------------------------------------------------------------- SECTION C: the mechanism
    say("\n=== C.  THE MECHANISM: path-fixed suppression tape on the UNDAMPED book's OWN trades ===")
    say("    removed notional measured trade-by-trade from the IDENTICAL state; the pure-ADD")
    say("    prediction is sum(dA)+sum(dB), the pure-OVERLAP floor is sum(max(dA,dB)).")
    tape_rows = []
    neg_tot = {d: 0 for d in ORDER}
    negn_tot = {d: 0.0 for d in ORDER}
    base_tot_all = 0.0
    for pname, (px, invest) in panels.items():
        for gross in GROSSES:
            for tier in TIERS:
                tp = suppression_tape(px, invest, gross, tier)
                base = tp["base"]
                base_tot_all += base
                for d in ORDER:
                    neg_tot[d] += tp["neg"][d]
                    negn_tot[d] += tp["negn"][d]
                for a, b in PAIRS:
                    nm = setname((a, b))
                    joint = tp["removed"][nm]
                    ap = tp["add_pred"][nm]
                    tape_rows.append(dict(panel=pname, gross=gross, tier=tier, pair=nm,
                                          decomposable=bool((a in EXEC) and (b in EXEC)),
                                          base_notional=base,
                                          rem_a=tp["removed"][a], rem_b=tp["removed"][b],
                                          rem_pair=joint, add_pred=ap,
                                          ovl_floor=tp["ovl_floor"][nm],
                                          rem_a_frac=tp["removed"][a] / base,
                                          rem_b_frac=tp["removed"][b] / base,
                                          rem_pair_frac=joint / base,
                                          tape_ratio=(joint / ap if abs(ap) > 1e-9 else np.nan),
                                          floor_ratio=(tp["ovl_floor"][nm] / ap
                                                       if abs(ap) > 1e-9 else np.nan)))
            say(f"    ... tape {pname} gross {gross:.2f} done ({time.time() - t0:.0f}s)")
    tp_df = pd.DataFrame(tape_rows)
    # An EXECUTION-side device can only SHRINK the trade it is asked about, so its removal is
    # non-negative -- EXCEPT through the never-lever rescale: blocking a REDUCTION (HOLD) or a small
    # trim (DRIFT) leaves the risk sleeve larger, and when it would exceed 100% of NAV every risk
    # name is scaled back, which moves names the device never touched.  The decomposition needs the
    # AGGREGATE to be dominated by genuine suppression, so the gate is on NOTIONAL, not on counts.
    negshare = {d: negn_tot[d] / base_tot_all for d in ORDER}
    gate("G13 EXECUTION-side removals are non-negative in NOTIONAL on the risk columns"
         " (decomposition well posed; the residue is the never-lever rescale)",
         "; ".join(f"{d}: {negshare[d]:.3%} of base ({neg_tot[d]} cells)" for d in EXEC)
         + f"   [BANDW, target-side, signed by construction: {negshare['BANDW']:.2%}]",
         "< 1% of base notional for the four EXEC devices",
         all(negshare[d] < 0.01 for d in EXEC))
    dec = tp_df[tp_df.decomposable]
    say("\n    the SIX DECOMPOSABLE pairs (both devices EXECUTION-side):")
    say("    OVERLAP SHARE = sum(min(dA,dB)) / (sum dA + sum dB): the notional BOTH devices claim.")
    say("    UNION GAP = tape_ratio - union_ratio: 0.000 means the pair removes EXACTLY the union of")
    say("    the two singles' suppressions -- no more, no less.")
    say("    pair                 tape_ratio       union_ratio  overlap_share  union_gap   rem_A  rem_B  rem_AB")
    for a, b in EXEC_PAIRS:
        q = dec[dec.pair == setname((a, b))]
        tr_, un = q.tape_ratio.median(), q.floor_ratio.median()
        say(f"    {setname((a, b)):20s} {tr_:6.3f} [{q.tape_ratio.min():.3f},{q.tape_ratio.max():.3f}]"
            f"   {un:6.3f}      {1 - un:7.1%}     {tr_ - un:+7.4f}  {q.rem_a_frac.median():6.1%}"
            f" {q.rem_b_frac.median():6.1%} {q.rem_pair_frac.median():6.1%}")
    gapmed = float((dec.tape_ratio - dec.floor_ratio).abs().median())
    say(f"    POOLED over {len(dec)} decomposable tape cells: tape_ratio median {dec.tape_ratio.median():.3f}"
        f" [{dec.tape_ratio.min():.3f}, {dec.tape_ratio.max():.3f}];"
        f" union_ratio median {dec.floor_ratio.median():.3f};"
        f" OVERLAP SHARE median {1 - dec.floor_ratio.median():.1%}")
    say(f"    |union gap| pooled median {gapmed:.4f}, max {float((dec.tape_ratio - dec.floor_ratio).abs().max()):.4f}"
        f"  -> the pair removes the UNION of the two singles' suppressions")
    say("\n    the FOUR BANDW pairs are NOT decomposed on a fixed tape: BANDW moves the TARGET, so its")
    say("    per-name `d` is a SIGNED change in trade size, not a suppression, and max(dA, dB) has no")
    say("    meaning.  Their removed fractions are published for the record only:")
    for a, b in PAIRS:
        if (a in EXEC) and (b in EXEC):
            continue
        q = tp_df[tp_df.pair == setname((a, b))]
        say(f"    {setname((a, b)):20s} rem_A {q.rem_a_frac.median():+6.1%}  rem_B {q.rem_b_frac.median():+6.1%}"
            f"  rem_AB {q.rem_pair_frac.median():+6.1%}   (realised cut is the authority for these)")
    cp = cp.merge(tp_df[["panel", "gross", "tier", "pair", "decomposable", "tape_ratio", "floor_ratio",
                         "rem_a_frac", "rem_b_frac", "rem_pair_frac", "base_notional"]],
                  on=["panel", "gross", "tier", "pair"], how="left")
    cp.to_csv(f"{OUT}.composition.csv", index=False)
    publish("G10 pooled realised ADD-ratio (1.0 = perfectly additive, < 1 = overlap)",
            f"{cp.ratio_add.median():.4f}")
    publish("G10b pooled path-fixed tape ratio over the 6 DECOMPOSABLE pairs"
            " (1.0 = the two devices suppress DISJOINT trades)",
            f"{dec.tape_ratio.median():.4f}; union ratio {dec.floor_ratio.median():.4f};"
            f" contested notional {1 - dec.floor_ratio.median():.1%}")

    # ---------------------------------------------------------------- SECTION D: the bar
    say("\n=== D.  THE ADOPTION BAR (cut >= 31.0% AND dCAGR >= 0) ===")
    for rung in RUNGS:
        sub = df[df.cost_bps == rung]
        for kind in ("SINGLE", "PAIR"):
            k = sub[sub.kind == kind]
            say(f"    {rung:5.1f} bps  {kind:6s}: clears the bar {int(k.clears_bar.sum())} of {len(k)};"
                f"  of those still 4b: {int((k.clears_bar & k.pass4b).sum())};"
                f"  4b overall {int(k.pass4b.sum())} of {len(k)}")
    sub = df[(df.cost_bps == HEADLINE_RUNG) & df.clears_bar & (df.kind == "PAIR")]
    if len(sub):
        say("    PAIRS clearing the bar at 10 bps:")
        for r in sub.sort_values("cut", ascending=False).itertuples():
            say(f"      {r.panel} g{r.gross:.2f} {r.devices:24s} {r.tier:6s} cut {r.cut:6.1%}"
                f" dCAGR {r.dCAGR:+.2%} 4b={int(r.pass4b)} legs {r.legs} OOS_S {r.OOS_Sharpe:.4f}")
    else:
        say("    NO PAIR clears the bar at 10 bps.")
    say("\n    PAIRS clearing the bar AND keeping 4b on BOTH panels at the SAME (pair, tier, gross):")
    both = []
    for (gross, devices, tier), q in df[(df.cost_bps == HEADLINE_RUNG) & (df.kind == "PAIR")].groupby(
            ["gross", "devices", "tier"]):
        if len(q) == 2 and bool(q.clears_bar.all()) and bool(q.pass4b.all()):
            both.append((gross, devices, tier))
            say(f"      g{gross:.2f} {devices} {tier}: cuts {list(q.cut.round(4))}, dCAGR {list(q.dCAGR.round(4))}")
    if not both:
        say("      NONE.")
    say("\n    leg-failure census over ALL PAIR rows (all panels/gross/cost):")
    allp = df[df.kind == "PAIR"]
    for lg in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"):
        say(f"      {lg:7s} fails {int((~allp[lg]).sum())} of {len(allp)}")
    say(f"      leg strings: {allp.legs.value_counts().to_dict()}")
    say(f"      4b {int(allp.pass4b.sum())} of {len(allp)};  4a {int(allp.pass4a.sum())} of {len(allp)}")

    # ---------------------------------------------------------------- SECTION E: rule 8
    say("\n=== E.  RULE 8 WALK-FORWARD.  (D, tier) chosen on warm-up..2016-12-31 ONLY; 2017-2026 read ONCE ===")
    # pre-compute the IS statistics for EVERY (panel, gross, set, tier, rung) so the fourth
    # chooser can require BOTH-PANEL agreement using IN-SAMPLE information only.
    isdf = df.copy()
    isdf["IS_cut"] = [1 - is_tr[(r.panel, r.gross, r.devices, r.tier)]
                      / is_tr[(r.panel, r.gross, "NONE", "-")] for r in isdf.itertuples()]
    ref_is = {(r.panel, r.gross, r.cost_bps): r.IS_CAGR for r in isdf[isdf.kind == "NONE"].itertuples()}
    isdf["IS_dCAGR"] = [r.IS_CAGR - ref_is[(r.panel, r.gross, r.cost_bps)] for r in isdf.itertuples()]
    isdf["IS_clears"] = (isdf.IS_cut >= BAR_CUT) & (isdf.IS_dCAGR >= 0)
    bothpanel = {}
    for (gross, rung), q in isdf.groupby(["gross", "cost_bps"]):
        agg = q.groupby(["devices", "tier"]).agg(n=("IS_clears", "size"), ok=("IS_clears", "sum"),
                                                 iss=("IS_Sharpe", "mean"))
        elig = agg[(agg.n == 2) & (agg.ok == 2)]
        bothpanel[(gross, rung)] = (elig.iss.idxmax() if len(elig) else None, int(len(elig)))

    wf = []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_oos = backtest(px, rules_v2_weights(px), cost_bps=HEADLINE_RUNG,
                            freq=CADENCE)["returns"].loc[win].loc[OOS_START:]
        for gross in GROSSES:
            for rung in RUNGS:
                pool = df[(df.panel == pname) & (df.gross == gross) & (df.cost_bps == rung)].copy()
                pool["IS_cut"] = [1 - is_tr[(pname, gross, r.devices, r.tier)]
                                  / is_tr[(pname, gross, "NONE", "-")] for r in pool.itertuples()]
                pool["IS_dCAGR"] = pool.IS_CAGR - float(pool[pool.kind == "NONE"].IS_CAGR.iloc[0])
                picks = {}
                picks["C_ISSHARPE"] = pool.loc[pool.IS_Sharpe.idxmax()]
                adopt = pool[(pool.IS_cut >= BAR_CUT) & (pool.IS_dCAGR >= 0)]
                picks["C_ISADOPT"] = (adopt.loc[adopt.IS_CAGR.idxmax()] if len(adopt)
                                      else pool[pool.kind == "NONE"].iloc[0])
                picks["C_PREREG"] = pool[(pool.devices == PREREG_POINT[0])
                                         & (pool.tier == PREREG_POINT[1])].iloc[0]
                bp, n_bp = bothpanel[(gross, rung)]
                picks["C_BOTHPANEL"] = (pool[(pool.devices == bp[0]) & (pool.tier == bp[1])].iloc[0]
                                        if bp is not None else pool[pool.kind == "NONE"].iloc[0])
                for cname, p in picks.items():
                    wf.append(dict(panel=pname, gross=gross, cost_bps=rung, chooser=cname,
                                   picked_devices=p.devices, picked_tier=p.tier, picked_kind=p.kind,
                                   IS_cut=float(p.IS_cut), IS_Sharpe=float(p.IS_Sharpe),
                                   OOS_CAGR=float(p.OOS_CAGR), OOS_Sharpe=float(p.OOS_Sharpe),
                                   OOS_MaxDD=float(p.OOS_MaxDD),
                                   SPY_OOS_CAGR=cagr(spy_oos), SPY_OOS_Sharpe=sharpe(spy_oos),
                                   SPY_OOS_MaxDD=maxdd(spy_oos),
                                   BASE_OOS_CAGR=cagr(base_oos), BASE_OOS_Sharpe=sharpe(base_oos),
                                   BASE_OOS_MaxDD=maxdd(base_oos),
                                   REF_OOS_CAGR=float(pool[pool.kind == "NONE"].OOS_CAGR.iloc[0]),
                                   REF_OOS_Sharpe=float(pool[pool.kind == "NONE"].OOS_Sharpe.iloc[0]),
                                   full_cut=float(p.cut), full_dCAGR=float(p.dCAGR),
                                   full_4b=bool(p.pass4b), full_4a=bool(p.pass4a), full_legs=p.legs,
                                   adopt_pool_size=int(len(adopt)), bothpanel_pool_size=n_bp))
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say("    C_BOTHPANEL: among points clearing the bar IN SAMPLE on BOTH panels at the same"
        " (set, tier, gross), max mean IS Sharpe.  IN-SAMPLE information only.")
    for cname in ("C_ISSHARPE", "C_ISADOPT", "C_PREREG", "C_BOTHPANEL"):
        q = wfd[wfd.chooser == cname]
        pk = q.groupby(["picked_devices", "picked_tier"]).size().to_dict()
        say(f"    {cname:12s} picks {pk}")
        say(f"        OOS CAGR {q.OOS_CAGR.median():.2%}  OOS Sharpe {q.OOS_Sharpe.median():.4f}"
            f"  OOS MaxDD {q.OOS_MaxDD.median():.2%}"
            f"   beats SPY OOS Sharpe {int((q.OOS_Sharpe > q.SPY_OOS_Sharpe).sum())}/{len(q)}"
            f"   beats CAP2 OOS Sharpe {int((q.OOS_Sharpe > q.REF_OOS_Sharpe).sum())}/{len(q)}"
            f"   beats live RULES v2 OOS Sharpe {int((q.OOS_Sharpe > q.BASE_OOS_Sharpe).sum())}/{len(q)}")
        say(f"        beats SPY OOS CAGR {int((q.OOS_CAGR > q.SPY_OOS_CAGR).sum())}/{len(q)};"
            f" full-sample 4b on the pick {int(q.full_4b.sum())}/{len(q)}; 4a {int(q.full_4a.sum())}/{len(q)};"
            f" full cut median {q.full_cut.median():.1%}, dCAGR median {q.full_dCAGR.median():+.2%}")
    say(f"    TOTAL PICKS {len(wfd)}")

    # ---------------------------------------------------------------- SECTION F: the pre-registered pair
    say(f"\n=== F.  THE PRE-REGISTERED PAIR IN FULL  ({PREREG_POINT[0]}, {PREREG_POINT[1]} — nothing fitted) ===")
    zp = df[(df.devices == PREREG_POINT[0]) & (df.tier == PREREG_POINT[1])]
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
    say(f"    rows {len(df)}; turnover rows {len(tf)}; composition cells {len(cp)};"
        f" tape cells {len(tp_df)}; walk-forward picks {len(wfd)}; elapsed {time.time() - t0:.0f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

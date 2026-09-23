#!/usr/bin/env python3
"""idea 2463 (lane C, 2026-09-23) — WHERE IS THE CAGR-PER-TURNOVER FRONTIER of the
CANDIDATE FAMILY, and where on it does idea 2431's ADOPTION BAR sit?

THE OBJECT.  The record's standing 4b KEEP-candidate is idea 2322's CAP2: every name INSIDE
the 200d +/- 3% band held at `min(gross / N_in, 2%)` of NAV, idle NAV swept to SHY, weekly,
t+1, 10 bps.  On U56 / gross 0.75 it reads 11.62% / 1.2687 / -14.81% at **3.51 turns a year**
against the live book's 1.77x, and idea 2431 wrote the adoption bar the family has to clear:

    cut turnover 3.51x -> 2.42x (-31.0%) AT UNCHANGED RETURNS.

Eleven closed devices have each been priced against that bar ALONE, each quoting an exchange
rate near -0.10 pp of CAGR per 1% of turnover saved, and each killed on its own.  No run has
ever put them on ONE axis.  This run does: it re-implements the family inside one engine, on
one panel, at one cost convention, and publishes the **frontier** — the best CAGR attainable
at each level of turnover saved — plus the bar's position on it.  A frontier answers a
question no single device can: is the -31.0% cut expensive because every device tried so far
was bad, or because the exchange rate is a PROPERTY OF THE BOOK?

DIAL 1 -- DEVICE FAMILY, 9 devices + the undamped reference, re-implemented here:
    NONE      the undamped CAP2 book (reference; every delta is measured against it)
    DRIFT     weight-drift no-trade band d of NAV                     (idea 2328)
    PARTIAL   partial-adjustment trade fraction phi                   (ideas 2391 / 2404)
    HOLD      minimum hold: a name younger than h rebalances is never REDUCED  (idea 2351)
    ROTA      calendar rota: act on every k-th weekly rebalance only   (idea 2408)
    WIDTH     book width: keep the top-K in-band names by distance above the 200d (idea 2467)
    BANDW     band width b (both edges together)                       (idea 2343)
    AGE       admission age: in-band continuously for a sessions before entry (idea 2439)
    WHIP      whipsaw budget: exclude names with >= k band flips in trailing 252d (idea 2447)
    SCALE     the NULL DEVICE: multiply the risk sleeve by s, sweep absorbs (idea 2443/2457)
              -- it cuts turnover by HOLDING LESS and is carried deliberately so the frontier
              can be read against the one "device" that is not a device at all.
DIAL 2 -- STRENGTH RUNG within the device (4-5 rungs each, ladder published in full).

REPORTED, NEVER SELECTED ON: panels {U56, B136}, gross {0.75, 1.00}, cost rungs
{0, 10, 25, 50} bps, weekly cadence, band 0.03 (except on the BANDW ladder), cap 2%, t+1.
38 (device, strength) points x 2 gross x 2 panels = 152 books, each published at 4 rungs
= 608 rows.  SMALL is not priced: ideas 2318 / 2322 / 2326 / 2343 each published SMALL's 4b
pass count at 0 of 40-120, so there is no pass there for a turnover device to keep.

THE PREMISE IS TESTED, NOT ASSUMED, IN TWO PLACES.
  (1) EVERY device is forced through an IDENTITY RUNG (d=0, phi=1, h=1, k=1, K=ALL, b=0.03,
      a=0, whip=inf, s=1.0) and gated to be BIT-IDENTICAL to NONE -- so a "saving" can never
      be an implementation difference (gates G3a-G3i).
  (2) "At unchanged returns" is only meaningful at unchanged EXPOSURE.  Mean risk gross is
      published for every point, and the frontier is read TWICE: once over all points, and
      once over the EXPOSURE-NEUTRAL subset (mean risk gross within +/-2% relative of NONE).

BOTH KEEP PATHS on every row: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse)
and 4b (Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x
SPY's).  RULE 8: (device, strength) chosen on warm-up..2016-12-31 ONLY by three pre-stated
IS-only choosers (C_ISSHARPE, C_ISCALMAR, C_ISADOPT = best IS CAGR among points clearing the
-31.0% cut in-sample), then 2017-2026 read ONCE.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_cagr-per-turnover-frontier_C.py
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

DATE, SLUG, LANE = "2026-09-23", "cagr-per-turnover-frontier", "C"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, CAP, CADENCE, WARMUP = 0.03, 0.02, "W", 260
GROSSES = [0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG = 10.0
SWEEP = "SHY"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BAR_CUT = 0.310                      # idea 2431: 3.51x -> 2.42x
NEUTRAL_TOL = 0.02                   # exposure-neutral = mean risk gross within +/-2% relative

# (device, strength) ladder.  The FIRST rung of every device is its IDENTITY rung (gated).
DEVICES = {
    "NONE":    [None],
    "DRIFT":   [0.0, 0.0010, 0.0025, 0.0050, 0.0100, 0.0175],
    "PARTIAL": [1.00, 0.75, 0.50, 0.35, 0.20],
    "HOLD":    [1, 2, 4, 8, 13],
    "ROTA":    [1, 2, 3, 4, 6, 13],
    "WIDTH":   [0, 32, 16, 8, 4],          # 0 = ALL names (identity)
    "BANDW":   [0.03, 0.05, 0.08, 0.12],
    "AGE":     [0, 5, 10, 21, 42],
    "WHIP":    [0, 12, 8, 6, 4],           # 0 = no budget (identity); rung = max flips allowed
    "SCALE":   [1.00, 0.85, 0.70, 0.55, 0.40],
}
IDENTITY = {k: v[0] for k, v in DEVICES.items()}

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


# ---------------------------------------------------------------- target book (TARGET-side devices)
def cap_weights(px, invest, gross, device="NONE", strength=None):
    """idea 2322's CAP2 with the TARGET-side device applied to the ADMITTED set.

    base admitted set = names inside the 200d +/- band (hysteresis, baseline.band_state) and
    priced that day; w_i = min(gross / N_in, CAP); idle NAV swept to SHY (phi = 1.00).
    """
    q = px[invest]
    pr = q.notna()
    band = strength if device == "BANDW" else BAND
    base = band_state(q, band) & pr
    adm = base
    if device == "AGE" and strength:
        adm = adm & (base.astype(float).rolling(int(strength)).sum() >= int(strength))
    if device == "WHIP" and strength:
        flips = base.ne(base.shift(1)).astype(float).rolling(252).sum()
        adm = adm & (flips < float(strength))
    if device == "WIDTH" and strength:
        dist = q / q.rolling(200).mean() - 1.0
        rk = dist.where(adm).rank(axis=1, ascending=False)
        adm = adm & (rk <= int(strength))
    nin = adm.sum(axis=1).replace(0, np.nan)
    per = pd.concat([gross / nin, pd.Series(CAP, index=q.index)], axis=1).min(axis=1)
    w = adm.astype(float).mul(per.fillna(0.0), axis=0)
    if device == "SCALE" and strength is not None:
        w = w * float(strength)
    w = w.reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return w


# ---------------------------------------------------------------- the engine (EXECUTION-side devices)
def run_book(prices, weights, device="NONE", strength=None, freq=CADENCE, sweep=SWEEP, phase=0):
    """engine.backtest with one EXECUTION-side device.  All identity rungs reduce to
    engine.backtest exactly (gates G1, G3a-G3i).

    DRIFT d   : trade risk name i only when |target_i - held_i| > d.
    PARTIAL p : move a fraction p of the way to target;  new = cur + p*(target - cur).
    HOLD h    : a risk name held for fewer than h acting rebalances is never REDUCED
                (trims and exits blocked; increases and fresh entries always allowed).
    ROTA k    : act on every k-th weekly rebalance date only (phase p, default 0); drift
                in between.  The phase FAMILY is priced in section F, not assumed away.
    SHY is then set to 1 - sum(risk weights), which is exactly its own target when every name
    moves.  Zero-cost returns and turnover are kept separately so every cost rung is priced
    from one pass.  Un-invested residual drifts at 0% (engine convention).
    """
    d = float(strength) if device == "DRIFT" else 0.0
    phi = float(strength) if device == "PARTIAL" else 1.0
    hold = int(strength) if device == "HOLD" else 1
    rota = int(strength) if device == "ROTA" else 1

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
    cur = np.zeros(len(cols))
    age = np.zeros(len(cols))
    turnover = np.zeros(n); gross_s = np.zeros(n); risk_g = np.zeros(n)
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
            turnover[i] = np.abs(new - cur).sum()
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


def frontier(pts):
    """pts = list of (cut, dcagr, label).  Returns the Pareto set: a point survives when no
    other point has BOTH a cut >= its own and a dCAGR > its own (ties broken by cut)."""
    out = []
    for c, y, lab in pts:
        dominated = any((c2 >= c - 1e-12 and y2 > y + 1e-12) or
                        (c2 > c + 1e-12 and y2 >= y - 1e-12) for c2, y2, _ in pts)
        if not dominated:
            out.append((c, y, lab))
    return sorted(out)


def main():
    t0 = time.time()
    say("=== idea 2463 (lane C) — the CAGR-per-TURNOVER FRONTIER of the candidate family ===")
    say(f"    {DATE}  lane {LANE}   band {BAND}  cap {CAP}  cadence {CADENCE}  t+1  rungs {RUNGS} bps"
        f"  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 device family {list(DEVICES)}")
    for k, v in DEVICES.items():
        say(f"      {k:8s} rungs {v}   (identity rung {IDENTITY[k]})")
    say(f"    DIAL 2 strength rung.  REPORTED not selected: panels U56/B136, gross {GROSSES}, rungs {RUNGS}")
    say(f"    THE BAR (idea 2431): turnover -{BAR_CUT:.1%} at unchanged returns (3.51x -> 2.42x)")
    gate("G8 exactly two tuned parameters", "device family, strength rung", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
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

    px_u, inv_u = panels["U56"]

    # ---- G1: the NONE replica IS engine.backtest
    w0 = cap_weights(px_u, inv_u, 0.75)
    r_eng = backtest(px_u, w0, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    d1 = float((r_eng - priced(run_book(px_u, w0), HEADLINE_RUNG)).abs().max())
    gate("G1 NONE replica == engine.backtest (CAP2, U56, g=0.75)", f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    # ---- G3a-G3i: every device's IDENTITY rung is bit-identical to NONE
    r_none = priced(run_book(px_u, w0), HEADLINE_RUNG)
    t_none = run_book(px_u, w0)["turnover"].sum()
    for dev in DEVICES:
        if dev == "NONE":
            continue
        st = IDENTITY[dev]
        wI = cap_weights(px_u, inv_u, 0.75, dev, st)
        rI = run_book(px_u, wI, dev, st)
        dd = max(float((priced(rI, HEADLINE_RUNG) - r_none).abs().max()),
                 abs(float(rI["turnover"].sum() - t_none)))
        gate(f"G3 identity rung reduces to NONE ({dev} @ {st})", f"max|d| {dd:.3e}", "< 1e-12", dd < 1e-12)

    # ---------------------------------------------------------------- the grid
    rows, tr_rows = [], []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        yrs = len(win) / 252
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_r = priced(run_book(px, rules_v2_weights(px[invest], band=BAND, gross=0.75)
                                 .reindex(columns=px.columns).fillna(0.0)), HEADLINE_RUNG).loc[win]
        say(f"\n--- panel {pname}  ({len(invest)} columns)  SPY {cagr(spy):.2%} / {sharpe(spy):.4f} / {maxdd(spy):.2%}"
            f"   live RULES v2 {cagr(base_r):.2%} / {sharpe(base_r):.4f} / {maxdd(base_r):.2%}")
        for gross in GROSSES:
            for dev, ladder in DEVICES.items():
                for st in ladder:
                    if dev != "NONE" and st == IDENTITY[dev]:
                        continue                       # identity rung == NONE, already priced
                    wt = cap_weights(px, invest, gross, dev, st)
                    res = run_book(px, wt, dev, st)
                    inw = res["held"].drop(columns=[SWEEP]).loc[win]
                    pos = inw.values[inw.values > 1e-12]
                    tr_rows.append(dict(panel=pname, gross=gross, device=dev, strength=(np.nan if st is None else float(st)),
                                        turnover_yr=float(res["turnover"].loc[win].sum() / yrs),
                                        mean_names_in=float((inw.values > 1e-12).sum(axis=1).mean()),
                                        mean_risk_gross=float(res["risk_gross"].loc[win].mean()),
                                        mean_gross=float(res["gross"].loc[win].mean()),
                                        mean_sweep_w=float(res["held"][SWEEP].loc[win].mean()),
                                        max_name_w=float(pos.max()) if len(pos) else 0.0,
                                        max_row_sum=float(res["gross"].max()),
                                        acting_reb=res["acting_rebalances"], sched_reb=res["scheduled_rebalances"],
                                        lev_events=res["lev_events"]))
                    for rung in RUNGS:
                        r = priced(res, rung).loc[win]
                        r_oos = r.loc[OOS_START:]
                        h1, h2 = halves(r)
                        rows.append(dict(panel=pname, gross=gross, device=dev,
                                         strength=(np.nan if st is None else float(st)), cost_bps=rung,
                                         CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                         H1=h1, H2=h2,
                                         IS_CAGR=cagr(r.loc[:IS_END]), IS_Sharpe=sharpe(r.loc[:IS_END]),
                                         IS_Calmar=calmar(r.loc[:IS_END]),
                                         OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                         **legs(r, base_r, spy, r_oos, spy_oos)))
            say(f"    ... {pname} gross {gross:.2f} done ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(rows); tf = pd.DataFrame(tr_rows)
    df["strength"] = df.strength.fillna(-1.0); tf["strength"] = tf.strength.fillna(-1.0)
    df.to_csv(f"{OUT}.grid.csv", index=False); tf.to_csv(f"{OUT}.turnover.csv", index=False)

    # ---- G2: external reproduction of the committed CAP2 headline
    h = df[(df.panel == "U56") & (df.gross == 0.75) & (df.device == "NONE") & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    t2 = tf[(tf.panel == "U56") & (tf.gross == 0.75) & (tf.device == "NONE")].iloc[0]
    d2 = max(abs(h.CAGR - 0.1162), abs(h.Sharpe - 1.2687) / 10, abs(h.MaxDD + 0.1481),
             abs(h.OOS_CAGR - 0.1277), abs(h.OOS_Sharpe - 1.3318) / 10)
    gate("G2 reproduces idea 2336's committed CAP2 U56 headline (11.62%/1.2687/-14.81%, OOS 12.77%/1.3318)",
         f"read {h.CAGR:.2%} / {h.Sharpe:.4f} / {h.MaxDD:.2%}, OOS {h.OOS_CAGR:.2%} / {h.OOS_Sharpe:.4f},"
         f" turnover {t2.turnover_yr:.2f}x (committed 3.51x) -> max|d| {d2:.2e}", "< 1e-3", d2 < 1e-3)
    gate("G2b reproduces the committed 3.51x turnover (U56, CAP2, g=0.75)",
         f"{t2.turnover_yr:.4f}x", "|d| < 0.01", abs(t2.turnover_yr - 3.51) < 0.01)
    gate("G4 no leverage anywhere", f"max row gross {tf.max_row_sum.max():.9f};"
         f" risk-sleeve rescale events {int(tf.lev_events.sum())}", "<= 1+1e-12",
         tf.max_row_sum.max() <= 1 + 1e-12)

    # ---- G10 / G11: CROSS-LANE reproduction of the two devices another lane priced TODAY
    for pn, exp in (("U56", (0.1179, 1.2538, -0.1692, 0.1298, 1.3091, 2.34)),
                    ("B136", (0.1204, 1.1189, -0.1952, 0.1203, 1.0947, 2.97))):
        pxp, invp = panels[pn]
        winp = pxp.index[WARMUP:]
        yrsp = len(winp) / 252
        resP = run_book(pxp, cap_weights(pxp, invp, 0.75, "PARTIAL", 0.40), "PARTIAL", 0.40)
        rP = priced(resP, HEADLINE_RUNG).loc[winp]
        tP = float(resP["turnover"].loc[winp].sum() / yrsp)
        dd10 = max(abs(cagr(rP) - exp[0]), abs(sharpe(rP) - exp[1]) / 10, abs(maxdd(rP) - exp[2]),
                   abs(cagr(rP.loc[OOS_START:]) - exp[3]), abs(sharpe(rP.loc[OOS_START:]) - exp[4]) / 10)
        gate(f"G10 reproduces lane B idea 2391's committed PARTIAL lam=0.40 headline ({pn}, g0.75, 10bps:"
             f" {exp[0]:.2%}/{exp[1]:.4f}/{exp[2]:.2%}, OOS {exp[3]:.2%}/{exp[4]:.4f}, {exp[5]:.2f}x)",
             f"read {cagr(rP):.2%} / {sharpe(rP):.4f} / {maxdd(rP):.2%}, OOS {cagr(rP.loc[OOS_START:]):.2%} /"
             f" {sharpe(rP.loc[OOS_START:]):.4f}, {tP:.2f}x -> max|d| {dd10:.2e}", "< 1e-3", dd10 < 1e-3)
    dR = tf[(tf.panel == "U56") & (tf.gross == 0.75) & (tf.device == "DRIFT") & (tf.strength == 0.0175)].iloc[0]
    rR = df[(df.panel == "U56") & (df.gross == 0.75) & (df.device == "DRIFT") & (df.strength == 0.0175)
            & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    n0 = df[(df.panel == "U56") & (df.gross == 0.75) & (df.device == "NONE") & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    t_u56_none = tf[(tf.panel == "U56") & (tf.gross == 0.75) & (tf.device == "NONE")].turnover_yr.iloc[0]
    d11 = max(abs(dR.turnover_yr - 1.85), abs((rR.CAGR - n0.CAGR) - 0.0192))
    gate("G11 reproduces lane B idea 2328's committed DRIFT d=0.0175 row (U56 CAP2 g0.75: 1.85x, -47.3%,"
         " dCAGR@10 +1.92%)",
         f"read {dR.turnover_yr:.2f}x, cut {1 - dR.turnover_yr / t_u56_none:+.1%},"
         f" dCAGR {rR.CAGR - n0.CAGR:+.2%} -> max|d| {d11:.2e}", "< 6e-3", d11 < 6e-3)

    # ---- G5: every device BITES on turnover at its strongest rung
    bites = []
    for (p, g), grp in tf.groupby(["panel", "gross"]):
        t0r = grp[grp.device == "NONE"].turnover_yr.iloc[0]
        for dev in DEVICES:
            if dev == "NONE":
                continue
            v = grp[grp.device == dev].turnover_yr
            bites.append((p, g, dev, bool(v.min() < t0r - 1e-9)))
    gate("G5 every device BITES (its best rung cuts turnover below NONE)",
         f"{sum(b[3] for b in bites)} of {len(bites)} (panel, gross, device) cells",
         f"{len(bites)} of {len(bites)}", all(b[3] for b in bites))

    # ---------------------------------------------------------------- A. the full ladder
    say("\n=== A. THE FULL LADDER AT THE HEADLINE RUNG (10 bps) — every point, nothing dropped ===")
    for pname in panels:
        for gross in GROSSES:
            t0r = tf[(tf.panel == pname) & (tf.gross == gross) & (tf.device == "NONE")].turnover_yr.iloc[0]
            ref = {rg: df[(df.panel == pname) & (df.gross == gross) & (df.device == "NONE")
                          & (df.cost_bps == rg)].iloc[0] for rg in RUNGS}
            say(f"\n  {pname} / gross {gross:.2f}   NONE turnover {t0r:.3f}x   NONE CAGR {ref[10.0].CAGR:.2%}"
                f"  Sharpe {ref[10.0].Sharpe:.4f}  MaxDD {ref[10.0].MaxDD:.2%}")
            say("   device   rung  | turn/yr     cut%  | dCAGR@10  rate(pp/1%) | CAGR   Sharpe   MaxDD  |"
                " OOS CAGR OOS Sh | 4a 4b legs  | riskgross names maxw")
            for dev, ladder in DEVICES.items():
                for st in ladder:
                    if dev != "NONE" and st == IDENTITY[dev]:
                        continue
                    c = tf[(tf.panel == pname) & (tf.gross == gross) & (tf.device == dev)
                           & (tf.strength == (-1.0 if st is None else float(st)))].iloc[0]
                    r = df[(df.panel == pname) & (df.gross == gross) & (df.device == dev)
                           & (df.strength == (-1.0 if st is None else float(st)))
                           & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                    cut = 1 - c.turnover_yr / t0r
                    dc = r.CAGR - ref[10.0].CAGR
                    rate = (dc * 100 / (cut * 100)) if abs(cut) > 1e-9 else np.nan
                    lg = "".join("1" if r[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                    say(f"  {dev:8s} {('-' if st is None else f'{float(st):.4f}'):>7s} | {c.turnover_yr:7.3f} {cut:+8.1%}"
                        f" | {dc:+8.2%} {rate:12.3f} | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:7.2%} |"
                        f" {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:6.4f} | {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'} {lg} |"
                        f"  {c.mean_risk_gross:.3f} {c.mean_names_in:6.2f} {c.max_name_w:5.2%}")

    # ---------------------------------------------------------------- B. the frontier
    say("\n=== B. THE FRONTIER — best dCAGR attainable at each level of turnover saved (10 bps) ===")
    front_rows = []
    for pname in panels:
        for gross in GROSSES:
            t0r = tf[(tf.panel == pname) & (tf.gross == gross) & (tf.device == "NONE")].turnover_yr.iloc[0]
            ref = df[(df.panel == pname) & (df.gross == gross) & (df.device == "NONE")
                     & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
            g0 = tf[(tf.panel == pname) & (tf.gross == gross) & (tf.device == "NONE")].mean_risk_gross.iloc[0]
            pts, pts_neutral = [], []
            for _, c in tf[(tf.panel == pname) & (tf.gross == gross)].iterrows():
                r = df[(df.panel == pname) & (df.gross == gross) & (df.device == c.device)
                       & (df.strength == c.strength) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                cut = 1 - c.turnover_yr / t0r
                y = r.CAGR - ref.CAGR
                lab = f"{c.device}@{c.strength:g}"
                pts.append((cut, y, lab))
                if abs(c.mean_risk_gross / g0 - 1) <= NEUTRAL_TOL:
                    pts_neutral.append((cut, y, lab))
                front_rows.append(dict(panel=pname, gross=gross, device=c.device, strength=c.strength,
                                       cut=cut, dCAGR=y, turnover_yr=c.turnover_yr,
                                       mean_risk_gross=c.mean_risk_gross,
                                       exposure_neutral=bool(abs(c.mean_risk_gross / g0 - 1) <= NEUTRAL_TOL),
                                       pass4a=r.pass4a, pass4b=r.pass4b, Sharpe=r.Sharpe, MaxDD=r.MaxDD,
                                       OOS_Sharpe=r.OOS_Sharpe))
            for label, P in (("ALL POINTS", pts), (f"EXPOSURE-NEUTRAL (risk gross within +/-{NEUTRAL_TOL:.0%})", pts_neutral)):
                F = frontier(P)
                say(f"\n  {pname} / gross {gross:.2f} / {label}  ({len(P)} points, {len(F)} on the frontier)"
                    f"   NONE risk gross {g0:.3f}")
                say("     cut      dCAGR    rate(pp per 1% saved)  holder")
                for c, y, lab in F:
                    rate = (y * 100 / (c * 100)) if abs(c) > 1e-9 else np.nan
                    say(f"    {c:+7.1%} {y:+9.2%} {rate:16.3f}          {lab}")
                # the bar
                at_bar = [(c, y, lab) for c, y, lab in P if c >= BAR_CUT - 1e-12]
                if at_bar:
                    best = max(at_bar, key=lambda z: z[1])
                    say(f"    BAR ({BAR_CUT:.1%} cut): {len(at_bar)} of {len(P)} points clear it;"
                        f" BEST dCAGR there {best[1]:+.2%} at cut {best[0]:+.1%} held by {best[2]}"
                        f"  -> exchange rate {best[1] * 100 / (best[0] * 100):.3f} pp per 1%")
                else:
                    say(f"    BAR ({BAR_CUT:.1%} cut): NO point in this set reaches it (max cut {max(c for c, _, _ in P):+.1%})")

    fr = pd.DataFrame(front_rows)
    fr.to_csv(f"{OUT}.frontier.csv", index=False)

    # ---- the bar, pooled
    say("\n=== B2. THE BAR, POOLED OVER ALL 4 (panel, gross) CELLS AT 10 bps ===")
    for neutral in (False, True):
        sub = fr[fr.exposure_neutral] if neutral else fr
        at = sub[sub.cut >= BAR_CUT - 1e-12]
        tag = "EXPOSURE-NEUTRAL" if neutral else "ALL POINTS"
        say(f"  {tag}: {len(at)} of {len(sub)} points clear the -{BAR_CUT:.1%} cut;"
            f" of those, dCAGR >= 0 in {int((at.dCAGR >= 0).sum())}, 4b holds in {int(at.pass4b.sum())},"
            f" 4a holds in {int(at.pass4a.sum())}")
        if len(at):
            b = at.loc[at.dCAGR.idxmax()]
            say(f"    best dCAGR at the bar: {b.dCAGR:+.2%} ({b.device}@{b.strength:g}, {b.panel}, gross {b.gross:.2f},"
                f" cut {b.cut:+.1%}, turnover {b.turnover_yr:.2f}x, risk gross {b.mean_risk_gross:.3f},"
                f" 4b {'Y' if b.pass4b else '.'}, 4a {'Y' if b.pass4a else '.'})")

    # ---- the exchange rate, per device
    say("\n=== B3. EXCHANGE RATE BY DEVICE (pp of CAGR per 1% of turnover saved, 10 bps) ===")
    say("    the record quotes ~-0.10 for each of the eleven closed devices; this is the family's own read")
    say("  device   |" + "".join(f"  {p}/g{g:.2f}" for p in panels for g in GROSSES) + "   pooled median")
    for dev in DEVICES:
        if dev == "NONE":
            continue
        cells, allr = [], []
        for p in panels:
            for g in GROSSES:
                s = fr[(fr.panel == p) & (fr.gross == g) & (fr.device == dev) & (fr.cut > 1e-9)]
                rr = (s.dCAGR * 100 / (s.cut * 100)) if len(s) else pd.Series(dtype=float)
                cells.append(float(rr.median()) if len(rr) else np.nan)
                allr += list(rr)
        say(f"  {dev:8s} |" + "".join(f" {c:10.3f}" for c in cells) +
            f"   {np.median(allr) if allr else np.nan:10.3f}")

    # ---------------------------------------------------------------- C. keep counts
    say(f"\n=== C. KEEP COUNTS OVER ALL {len(df)} PUBLISHED ROWS ===")
    say(f"  4b passes: {int(df.pass4b.sum())} of {len(df)}      4a passes: {int(df.pass4a.sum())} of {len(df)}")
    for rung in RUNGS:
        dd = df[df.cost_bps == rung]
        say(f"   {rung:5.1f} bps:  4b {int(dd.pass4b.sum()):3d}/{len(dd)}   4a {int(dd.pass4a.sum()):3d}/{len(dd)}"
            f"   binding leg on 4b FAILs: " +
            "  ".join(f"{k} {int((~dd[k][~dd.pass4b]).sum())}" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    say("\n  4b pass counts by (device, panel) over 4 rungs x 2 gross x its own strength ladder:")
    for dev in DEVICES:
        line = "  ".join(f"{p} {int(df[(df.device == dev) & (df.panel == p)].pass4b.sum()):3d}/"
                         f"{len(df[(df.device == dev) & (df.panel == p)]):3d}" for p in panels)
        say(f"    {dev:8s}  {line}")

    # ---------------------------------------------------------------- D. rule 8
    say("\n=== D. RULE 8 — (device, strength) chosen on <= 2016-12-31 ONLY, 2017-2026 read once ===")
    wf = []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_r = priced(run_book(px, rules_v2_weights(px[invest], band=BAND, gross=0.75)
                                 .reindex(columns=px.columns).fillna(0.0)), HEADLINE_RUNG).loc[win]
        b_oos = base_r.loc[OOS_START:]
        for gross in GROSSES:
            t0r = tf[(tf.panel == pname) & (tf.gross == gross) & (tf.device == "NONE")].turnover_yr.iloc[0]
            for rung in RUNGS:
                dd = df[(df.panel == pname) & (df.gross == gross) & (df.cost_bps == rung)].copy()
                # turnover cut of every point, for the adoption chooser
                cuts = {}
                for _, c in tf[(tf.panel == pname) & (tf.gross == gross)].iterrows():
                    cuts[(c.device, c.strength)] = 1 - c.turnover_yr / t0r
                dd["cut"] = [cuts[(r.device, r.strength)] for _, r in dd.iterrows()]
                und = dd[dd.device == "NONE"].iloc[0]
                choosers = [("C_ISSHARPE", dd.loc[dd.IS_Sharpe.idxmax()]),
                            ("C_ISCALMAR", dd.loc[dd.IS_Calmar.idxmax()])]
                adopt = dd[dd.cut >= BAR_CUT - 1e-12]
                choosers.append(("C_ISADOPT", adopt.loc[adopt.IS_CAGR.idxmax()] if len(adopt) else und))
                for chooser, pick in choosers:
                    wf.append(dict(panel=pname, gross=gross, cost_bps=rung, chooser=chooser,
                                   pick_device=pick.device, pick_strength=pick.strength, pick_cut=float(pick.cut),
                                   OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                                   pick_pass4b=bool(pick.pass4b), pick_pass4a=bool(pick.pass4a),
                                   pick_is_none=bool(pick.device == "NONE"),
                                   und_OOS_CAGR=und.OOS_CAGR, und_OOS_Sharpe=und.OOS_Sharpe,
                                   beats_undamped_OOS_Sharpe=bool(pick.OOS_Sharpe > und.OOS_Sharpe),
                                   base_OOS_CAGR=cagr(b_oos), base_OOS_Sharpe=sharpe(b_oos), base_OOS_MaxDD=maxdd(b_oos),
                                   spy_OOS_CAGR=cagr(spy_oos), spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_MaxDD=maxdd(spy_oos),
                                   beats_SPY_OOS_Sharpe=bool(pick.OOS_Sharpe > sharpe(spy_oos)),
                                   beats_LIVE_OOS_Sharpe=bool(pick.OOS_Sharpe > sharpe(b_oos))))
                    say(f"  {pname:5s} g{gross:.2f} {rung:5.1f}bps {chooser:11s} -> {pick.device:8s}@{pick.strength:<7g}"
                        f" cut {pick.cut:+6.1%} | OOS {pick.OOS_CAGR:6.2%} / {pick.OOS_Sharpe:.4f} / {pick.OOS_MaxDD:7.2%}"
                        f" | NONE OOS {und.OOS_CAGR:6.2%} / {und.OOS_Sharpe:.4f} | live v2 OOS {cagr(b_oos):6.2%} /"
                        f" {sharpe(b_oos):.4f} | SPY OOS {cagr(spy_oos):6.2%} / {sharpe(spy_oos):.4f} |"
                        f" full 4b {'Y' if pick.pass4b else '.'}")
    wfd = pd.DataFrame(wf)
    wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"\n  rule-8 picks landing on NONE (the undamped book): {int(wfd.pick_is_none.sum())} of {len(wfd)}")
    say(f"  picks beating the UNDAMPED book's OOS Sharpe:      {int(wfd.beats_undamped_OOS_Sharpe.sum())} of {len(wfd)}")
    say(f"  picks beating SPY's OOS Sharpe:                    {int(wfd.beats_SPY_OOS_Sharpe.sum())} of {len(wfd)}")
    say(f"  picks beating the LIVE book's OOS Sharpe:          {int(wfd.beats_LIVE_OOS_Sharpe.sum())} of {len(wfd)}")
    say(f"  picks whose full-sample row also passes 4b:        {int(wfd.pick_pass4b.sum())} of {len(wfd)}")
    say("  pick distribution over devices: " +
        "  ".join(f"{d} {int((wfd.pick_device == d).sum())}" for d in DEVICES))
    for ch in ("C_ISSHARPE", "C_ISCALMAR", "C_ISADOPT"):
        s = wfd[wfd.chooser == ch]
        say(f"   {ch:11s} mean OOS Sharpe {s.OOS_Sharpe.mean():.4f} vs NONE {s.und_OOS_Sharpe.mean():.4f}"
            f"  ({int(s.beats_undamped_OOS_Sharpe.sum())} of {len(s)} beat it);"
            f" mean OOS CAGR {s.OOS_CAGR.mean():.2%} vs NONE {s.und_OOS_CAGR.mean():.2%}")

    # ---------------------------------------------------------------- E. cost-rung view of the bar
    say("\n=== E. DOES THE BAR GET CHEAPER AT A HIGHER COST RUNG? (a saving is worth more at 50 bps) ===")
    for pname in panels:
        for gross in GROSSES:
            t0r = tf[(tf.panel == pname) & (tf.gross == gross) & (tf.device == "NONE")].turnover_yr.iloc[0]
            say(f"\n  {pname} / gross {gross:.2f}: best dCAGR among points clearing the -{BAR_CUT:.1%} cut")
            for rung in RUNGS:
                dd = df[(df.panel == pname) & (df.gross == gross) & (df.cost_bps == rung)].copy()
                ref = dd[dd.device == "NONE"].iloc[0]
                cand = []
                for _, r in dd.iterrows():
                    c = tf[(tf.panel == pname) & (tf.gross == gross) & (tf.device == r.device)
                           & (tf.strength == r.strength)].iloc[0]
                    cut = 1 - c.turnover_yr / t0r
                    if cut >= BAR_CUT - 1e-12:
                        cand.append((r.CAGR - ref.CAGR, r.device, r.strength, cut, r.pass4b, r.pass4a))
                if cand:
                    b = max(cand)
                    say(f"    {rung:5.1f} bps: {len(cand):2d} points clear; best dCAGR {b[0]:+.2%}"
                        f" ({b[1]}@{b[2]:g}, cut {b[3]:+.1%}) 4b {'Y' if b[4] else '.'} 4a {'Y' if b[5] else '.'};"
                        f" NONE CAGR {ref.CAGR:.2%}")
                else:
                    say(f"    {rung:5.1f} bps: no point clears the bar")

    # ---------------------------------------------------------------- F. the phase family
    say("\n=== F. IS THE ROTA GAIN A PHASE ARTEFACT?  the whole phase family, 10 bps ===")
    say("    ideas 942 / 963 / 967 warn that a single-phase calendar construction carries a family")
    say("    spread of several pp.  ROTA@k has k phases; sections A/B priced phase 0 ONLY.  Here is")
    say("    every phase of every rota rung, on both panels at gross 0.75.")
    ph_rows = []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        yrs = len(win) / 252
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_r = priced(run_book(px, rules_v2_weights(px[invest], band=BAND, gross=0.75)
                                 .reindex(columns=px.columns).fillna(0.0)), HEADLINE_RUNG).loc[win]
        wt = cap_weights(px, invest, 0.75)
        t0r = tf[(tf.panel == pname) & (tf.gross == 0.75) & (tf.device == "NONE")].turnover_yr.iloc[0]
        ref = df[(df.panel == pname) & (df.gross == 0.75) & (df.device == "NONE")
                 & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
        for k in [r for r in DEVICES["ROTA"] if r != IDENTITY["ROTA"]]:
            for p in range(int(k)):
                res = run_book(px, wt, "ROTA", k, phase=p)
                r = priced(res, HEADLINE_RUNG).loc[win]
                r_oos = r.loc[OOS_START:]
                ph_rows.append(dict(panel=pname, k=int(k), phase=p,
                                    turnover_yr=float(res["turnover"].loc[win].sum() / yrs),
                                    cut=1 - float(res["turnover"].loc[win].sum() / yrs) / t0r,
                                    CAGR=cagr(r), dCAGR=cagr(r) - ref.CAGR, Sharpe=sharpe(r), MaxDD=maxdd(r),
                                    OOS_Sharpe=sharpe(r_oos),
                                    **legs(r, base_r, spy, r_oos, spy_oos)))
    pf = pd.DataFrame(ph_rows)
    pf.to_csv(f"{OUT}.phase.csv", index=False)
    for pname in panels:
        say(f"\n  {pname} / gross 0.75   (NONE CAGR "
            f"{df[(df.panel == pname) & (df.gross == 0.75) & (df.device == 'NONE') & (df.cost_bps == HEADLINE_RUNG)].iloc[0].CAGR:.2%})")
        say("    k   phases | dCAGR  min / median / max |  spread | phase0 dCAGR  phase0 pctile | 4b passes | mean cut")
        for k in sorted(pf[pf.panel == pname].k.unique()):
            g = pf[(pf.panel == pname) & (pf.k == k)]
            p0 = g[g.phase == 0].iloc[0]
            pct = float((g.dCAGR <= p0.dCAGR).mean())
            say(f"   {k:3d}   {len(g):5d}  | {g.dCAGR.min():+6.2%} {g.dCAGR.median():+8.2%} {g.dCAGR.max():+8.2%} |"
                f" {g.dCAGR.max() - g.dCAGR.min():6.2%} | {p0.dCAGR:+12.2%} {pct:14.2f} |"
                f" {int(g.pass4b.sum()):3d}/{len(g):3d}   | {g.cut.mean():+7.1%}")
    say("\n  PHASE-FAMILY VERDICT (the number a rota device may honestly publish is the family MEDIAN,")
    say("  not its phase 0):")
    for pname in panels:
        g13 = pf[(pf.panel == pname) & (pf.k == 13)]
        g6 = pf[(pf.panel == pname) & (pf.k == 6)]
        say(f"    {pname}: ROTA@13 family median dCAGR {g13.dCAGR.median():+.2%} (phase 0 published"
            f" {float(g13[g13.phase == 0].dCAGR.iloc[0]):+.2%}, spread {g13.dCAGR.max() - g13.dCAGR.min():.2%},"
            f" 4b {int(g13.pass4b.sum())}/{len(g13)});  ROTA@6 median {g6.dCAGR.median():+.2%}"
            f" (phase 0 {float(g6[g6.phase == 0].dCAGR.iloc[0]):+.2%}, spread {g6.dCAGR.max() - g6.dCAGR.min():.2%},"
            f" 4b {int(g6.pass4b.sum())}/{len(g6)})")
    gate("G7 rota phase family priced in full (no single-phase headline stands alone)",
         f"{len(pf)} (panel, k, phase) books", "all k phases on both panels",
         len(pf) == 2 * sum(int(k) for k in DEVICES["ROTA"] if k != IDENTITY["ROTA"]))

    gdf = pd.DataFrame(GATES)
    gdf.to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n=== GATES: {int(gdf.pass_.sum())} of {len(gdf)} pass ===")
    for _, g in gdf[~gdf.pass_].iterrows():
        say(f"    FAILED: {g.gate} = {g.value} (target {g.target})")
    say(f"\nwrote {OUT}.grid.csv / .turnover.csv / .frontier.csv / .walkforward.csv / .phase.csv / .gates.csv"
        f"   ({time.time() - t0:.0f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Idea 2300 (lane cloud, 2026-09-22) — is the BAND GATE's DE-GROSS still the RIGHT SIDE of the
trade once CASH EARNS CARRY?

THE PREMISE.  RULES v2 clause 4 sends the gated-out weight to CASH and forbids re-grossing
(idea 81).  Every committed `de-gross beats the device` verdict in this record was measured
with that cash earning EXACTLY 0%, because `engine.backtest` drifts the un-invested residual at
a flat `1 - sum(w)` with no return attached.  Idea 2294 measured the residual at 46.7% of NAV
and found a short-Treasury sweep on it carries 1.73%/yr over 2017-2026.  A device that SPENDS
the idle cash therefore forfeits carry the de-gross arm collects -- so the whole family of
device-vs-de-gross contrasts was scored on a tape where one arm's cash was silently free.

THE EXPERIMENT.  Re-run the record's canonical device-vs-de-gross contrasts with the SWEEP
ATTACHED TO BOTH ARMS and report which committed verdicts MOVE.

DIAL 1 -- DEVICE SET D (a fixed ladder; every rung is a way the record has proposed to spend
the gated-out gross, and each spends only INSIDE the nominal gross budget g = 0.75):
  DG       w_i = (g/N) 1{IN}                       the LIVE clause-4 anchor; spends nothing
  RG50     w_i = (g/N)[1 + 0.5 (N/N_in - 1)]       half re-gross
  RG100    w_i = g / N_in                          full re-gross (idea 81's forbidden book)
  BETA     DG + (g - sum DG) into SPY              the beta sleeve (idea 2221)
  EWALL    w_i = g/N for every priced name         the gate switched OFF entirely
  GROSS100 w_i = (1.00/N) 1{IN}                    spend by raising nominal gross (idea 2119)
DIAL 2 -- SWEEP FRACTION phi {0.00, 0.25, 0.50, 0.75, 1.00} of whatever residual each arm has
left, `1 - sum(w)`, parked in SHY.  phi = 0.00 REPRODUCES the record's committed condition
exactly (gate G5), so every verdict is read twice on the same tape: cash at 0% and cash at
carry.  The instrument is FROZEN a priori to SHY by idea 2294's duration finding; it is NOT a
dial.  6 x 5 = 30 books per panel, EVERY ONE published.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} and COST RUNG {0, 10, 25, 50} bps
(headline 10).  Band 0.03, gross 0.75 (except the GROSS100 rung, whose whole content is gross),
weekly cadence, t+1 and warm-up 260 rows are FROZEN.

THE VERDICT OBJECT.  For every (panel, device, phi, rung) the four committed comparisons
  V_SHARPE  DG.Sharpe > DEV.Sharpe      V_DD   DG.MaxDD > DEV.MaxDD (shallower)
  V_CAGR    DG.CAGR   > DEV.CAGR        V_CALMAR
are read at phi = 0 (the record's basis) and at each phi > 0, and every FLIP is published.
PRE-REGISTERED DIRECTION, stated before any number was read: the sweep pays the arm with the
MOST idle cash, and that is always DG, so carry should STRENGTHEN de-gross.  The finding that
would matter is the opposite sign -- a verdict that de-gross only won because its idle cash was
priced at zero.  Either way the count of moved verdicts is the deliverable.

PROTOCOL: rule 1 (>= 10y); rule 2 (t+1, costs per unit turnover, no leverage -- the sweep is an
ordinary weight column charged ordinary turnover, and sum(w) <= 1 at every grid point, gate G3);
rule 3 (live RULES v2 AND SPY); rule 4 (both KEEP paths at every cell, exactly two tuned
parameters); rule 8 (walk-forward: (device, phi) chosen on warm-up..2016-12-31 ONLY by two
pre-registered IS-only choosers, 2017-2026 read ONCE, with the live book as the zero-parameter
reference); rule 9 (SURVIVORSHIP STATED: U56 and B136 are CURRENT-constituent lists held from
2008, SMALL is a CURRENT sub-$2B screen from 2010 with max_1d_move >= 1.0 tickers DROPPED, so
absolute levels are biased UP; the object here is a WITHIN-PANEL, SAME-DAY contrast between two
arms of the same gate, which is first-order immune -- the KEEP counts are not).
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

A REAL-ACCOUNT VARIANT IS PUBLISHED TOO: a money-market sweep costs nothing to enter or leave,
so the MMF reading rebates the SHY column's own turnover while the book's columns keep paying
the rung.  It is published beside the traded-sleeve reading at every cell, never selected on.

GATES.  G0 >= 10y per panel.  G1 DG at phi = 0 is BIT-IDENTICAL to baseline.rules_v2 on U56.
G2 the per-column replica reproduces engine.backtest bit-for-bit.  G3 NO LEVERAGE: max row sum
<= 1 + 1e-12 at every one of the 90 books.  G4 the device ladder actually SPENDS: mean gross is
DG < RG50 < RG100 and RG100 == BETA == EWALL == g to < 1e-9 on rows where >= 1 name is IN.
G5 phi = 0 reproduces the no-carry basis exactly (SHY column weight == 0 everywhere).  G6 the
phi dial BITES (mean SHY weight strictly increasing in phi on every device).  G7 the rule-8
choosers read no row on or after 2017-01-01.  G8 exactly two tuned parameters.  G9 the SMALL
dropped-ticker rule bit (>= 1 name removed).  G10 bit-identical recompute of the U56 headline
cell.  G11 the sweep instrument is priced on every row it is held.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-22_degross-vs-devices-with-cash-carry_cloud.py
"""
from __future__ import annotations

import sys, time, json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state   # noqa: E402
from engine import backtest                                        # noqa: E402

DATE, SLUG = "2026-09-22", "degross-vs-devices-with-cash-carry"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

BAND, GROSS, CADENCE, WARMUP = 0.03, 0.75, "W", 260
DEVICES = ["DG", "RG50", "RG100", "BETA", "EWALL", "GROSS100"]
PHIS = [0.00, 0.25, 0.50, 0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG = 10.0
SWEEP, BETA_INSTR = "SHY", "SPY"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BOOT_REPS, BOOT_BLOCK, SEED = 400, 63, 20260922

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


def bcol(df, name):
    """Leg columns carry NaN on the SPY reference rows; read them as booleans."""
    return df[name].fillna(False).astype(bool)


# ---------------------------------------------------------------- books
def device_weights(px, invest, device):
    """Every device spends only inside the nominal gross budget; none of them touches cash."""
    q = px[invest]
    pr = q.notna()
    e = pd.DataFrame(1.0, index=q.index, columns=q.columns).where(pr, 0.0)
    N = e.sum(axis=1).replace(0, np.nan)
    inb = band_state(q, BAND) & pr
    nin = inb.sum(axis=1).replace(0, np.nan)
    g = GROSS
    if device == "GROSS100":
        g = 1.00
    ew = g * e.div(N, axis=0).fillna(0.0)
    dg = ew.where(inb, 0.0)
    if device in ("DG", "GROSS100"):
        w = dg
    elif device in ("RG50", "RG100"):
        k = 0.5 if device == "RG50" else 1.0
        scale = (1.0 + k * (N / nin - 1.0)).replace([np.inf, -np.inf], np.nan).fillna(1.0)
        w = dg.mul(scale, axis=0)
    elif device == "EWALL":
        w = ew
    elif device == "BETA":
        w = dg
    else:
        raise ValueError(device)
    w = w.reindex(columns=px.columns).fillna(0.0)
    if device == "BETA":
        idle_gross = (GROSS * (nin.fillna(0) > 0).astype(float) - w.sum(axis=1)).clip(lower=0.0)
        live = px[BETA_INSTR].notna().astype(float)
        w[BETA_INSTR] = w[BETA_INSTR] + idle_gross * live
    return w


def with_sweep(px, w, phi):
    if phi == 0.0:
        return w
    w = w.copy()
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    live = px[SWEEP].notna().astype(float)
    w[SWEEP] = w[SWEEP] + phi * idle * live
    return w


def backtest_percol(prices, weights, freq=CADENCE):
    """Replica of engine.backtest returning PER-COLUMN turnover (zero cost; rungs applied
    afterwards), so the sweep column's own trading cost can be rebated for the MMF reading."""
    rets = prices.pct_change().fillna(0.0)
    w_target = weights.reindex(prices.index).fillna(0.0).shift(1)
    key = prices.index.to_period(freq)
    s = pd.Series(key, index=prices.index)
    mask = (s != s.shift(-1)).shift(1, fill_value=False)
    held = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
    cur = np.zeros(len(prices.columns))
    turnover = pd.Series(0.0, index=prices.index)
    t_sweep = pd.Series(0.0, index=prices.index)
    isw = list(prices.columns).index(SWEEP)
    gross = pd.Series(0.0, index=prices.index)
    for i in range(len(prices.index)):
        if mask.iloc[i] or i == 0:
            new = w_target.iloc[i].values
            d = np.abs(new - cur)
            turnover.iloc[i] = d.sum()
            t_sweep.iloc[i] = d[isw]
            cur = new
        held.iloc[i] = cur
        gross.iloc[i] = cur.sum()
        growth = cur * (1 + rets.iloc[i].values)
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    r0 = (held * rets).sum(axis=1)
    return dict(r0=r0, turnover=turnover, t_sweep=t_sweep, gross=gross)


def priced(res, bps, mmf=False):
    to = res["turnover"] - (res["t_sweep"] if mmf else 0.0)
    return res["r0"] - to * bps / 1e4


# ---------------------------------------------------------------- metrics / KEEP paths
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
                L_H1=bool(L_H1), L_H2=bool(L_H2), L_OOS=bool(L_OOS), L_DD=bool(L_DD), L_CAGR=bool(L_CAGR))


def boot_sharpe_diff(a, b, reps=BOOT_REPS, block=BOOT_BLOCK, seed=SEED):
    rng = np.random.default_rng(seed)
    x, y = a.values, b.values
    n = len(x)
    nb = int(np.ceil(n / block))
    obs = sharpe(a) - sharpe(b)
    out = np.empty(reps)
    for i in range(reps):
        st = rng.integers(0, n, nb)
        idx = np.concatenate([(np.arange(s, s + block) % n) for s in st])[:n]
        xs, ys = x[idx], y[idx]
        sx = xs.mean() * 252 / (xs.std() * np.sqrt(252)) if xs.std() > 0 else np.nan
        sy = ys.mean() * 252 / (ys.std() * np.sqrt(252)) if ys.std() > 0 else np.nan
        out[i] = sx - sy
    se = float(np.nanstd(out))
    return float(obs), se, (float(obs / se) if se > 0 else np.nan)


# ---------------------------------------------------------------- panels
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"].astype(str))
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    dropped = len(px.columns) - len(keep)
    px = px[keep]
    # SHY is NOT a sub-$2B constituent: it is joined as a SLEEVE instrument only (never
    # investable, never part of the gate), reindexed onto the small panel's trading days.
    shy = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)[SWEEP]
    px = pd.concat([px, shy.reindex(px.index, method="ffill").rename(SWEEP)], axis=1)
    return px, dropped


def main():
    t0 = time.time()
    say("=== idea 2300 — is the band gate's DE-GROSS still the right side once CASH EARNS CARRY? ===")
    say(f"    {DATE}  lane cloud   band {BAND}  gross {GROSS}  cadence {CADENCE}  t+1  rungs {RUNGS} bps")
    say(f"    DIAL 1 device set {DEVICES}   DIAL 2 phi {PHIS}   sweep instrument {SWEEP} (frozen a priori)")
    gate("G8 exactly two tuned parameters", "device set D, sweep fraction phi", "2", True)

    px_u = load_universe()
    px_b = load_universe(broad=True)
    px_s, dropped = small_panel()
    gate("G9 dropped-ticker rule bit (SMALL)", f"{dropped} names dropped (max_1d_move >= 1.0)", ">= 1", dropped >= 1)

    panels = {}
    for nm, px in (("U56", px_u), ("B136", px_b), ("SMALL", px_s)):
        invest = [c for c in px.columns if c not in ("SPY", SWEEP)] if nm == "SMALL" else list(px.columns)
        panels[nm] = (px, invest)
        say(f"    {nm:5s} {len(invest)} investable names, {px.index[0].date()}..{px.index[-1].date()}, {len(px)} rows")

    # ---- G1 / G2
    w_live = rules_v2_weights(px_u, band=BAND, gross=GROSS)
    res_live = backtest_percol(px_u, w_live)
    r_eng = backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    d2 = float((r_eng - priced(res_live, HEADLINE_RUNG)).abs().max())
    gate("G2 per-column replica == engine.backtest", f"max|d| {d2:.3e}", "< 1e-12", d2 < 1e-12)
    res_dg = backtest_percol(px_u, device_weights(px_u, list(px_u.columns), "DG"))
    d1 = float((res_dg["r0"] - res_live["r0"]).abs().max())
    gate("G1 DG(phi=0) == baseline.rules_v2 on U56", f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    grid, boot_rows, store, base_cache = [], [], {}, {}
    for pname, (px, invest) in panels.items():
        say(f"\n--- PANEL {pname} ---")
        idx = px.index
        win = idx[WARMUP:]
        oos_mask = win >= pd.Timestamp(OOS_START)
        is_mask = win <= pd.Timestamp(IS_END)
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        gate(f"G0 sample >= 10y ({pname})", f"{len(win)/252:.1f} yr", ">= 10", len(win) / 252 >= 10)
        gate(f"G11 sweep instrument priced ({pname})", f"{SWEEP} first price {px[SWEEP].first_valid_index().date()}",
             f"<= window start {win[0].date()}", px[SWEEP].first_valid_index() <= win[0])

        base_res = backtest_percol(px, rules_v2_weights(px, band=BAND, gross=GROSS))
        base_cache[pname] = base_res
        base = {c: priced(base_res, c).loc[win] for c in RUNGS}

        # rows where at least one name is IN: the only rows on which the device ladder's gross
        # identities can hold (with nothing IN, every device is 100% cash by construction)
        q = px[invest]
        live_rows = ((band_state(q, BAND) & q.notna()).sum(axis=1).loc[win] > 0)
        publish(f"rows with >= 1 name IN ({pname})", f"{int(live_rows.sum())} of {len(live_rows)}")

        mean_gross_dev, mean_sweep = {}, {}
        for dev in DEVICES:
            w0 = device_weights(px, invest, dev)
            for phi in PHIS:
                w = with_sweep(px, w0, phi)
                mx = float(w.sum(axis=1).max())
                if phi == PHIS[-1]:
                    gate(f"G3 no leverage ({pname} {dev} phi={phi})", f"max row sum {mx:.9f}", "<= 1+1e-12",
                         mx <= 1 + 1e-12)
                res = backtest_percol(px, w)
                mean_gross_dev[(dev, phi)] = float(res["gross"].loc[win][live_rows].mean())
                mean_sweep[(dev, phi)] = float(w[SWEEP].loc[win].mean()) if phi > 0 else 0.0
                for rung in RUNGS:
                    for mmf in (False, True):
                        r = priced(res, rung, mmf=mmf).loc[win]
                        store[(pname, dev, phi, rung, mmf)] = r
                        rec = dict(panel=pname, device=dev, phi=phi, cost_bps=rung, mmf=mmf,
                                   CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                   H1=halves(r)[0], H2=halves(r)[1],
                                   OOS_CAGR=cagr(r[oos_mask]), OOS_Sharpe=sharpe(r[oos_mask]),
                                   OOS_MaxDD=maxdd(r[oos_mask]), IS_Sharpe=sharpe(r[is_mask]),
                                   turnover_yr=float(res["turnover"].loc[win].sum() / (len(win) / 252)),
                                   sweep_turnover_yr=float(res["t_sweep"].loc[win].sum() / (len(win) / 252)),
                                   mean_gross=float(res["gross"].loc[win].mean()),
                                   mean_sweep_w=mean_sweep[(dev, phi)])
                        rec.update({f"FULL_{k}": v for k, v in legs(r, base[rung], spy, r[oos_mask], spy[oos_mask]).items()})
                        rec.update({f"OOS_{k}": v for k, v in legs(r[oos_mask], base[rung][oos_mask], spy[oos_mask],
                                                                  r[oos_mask], spy[oos_mask]).items()})
                        grid.append(rec)

        # G4 / G5 / G6
        ok4 = (mean_gross_dev[("DG", 0.0)] < mean_gross_dev[("RG50", 0.0)] < mean_gross_dev[("RG100", 0.0)]
               and abs(mean_gross_dev[("RG100", 0.0)] - mean_gross_dev[("EWALL", 0.0)]) < 1e-3
               and abs(mean_gross_dev[("BETA", 0.0)] - mean_gross_dev[("EWALL", 0.0)]) < 1e-3)
        gate(f"G4 device ladder spends ({pname})",
             " ".join(f"{d}:{mean_gross_dev[(d, 0.0)]:.4f}" for d in DEVICES),
             "DG < RG50 < RG100 == BETA == EWALL", ok4)
        gate(f"G5 phi=0 is the no-carry basis ({pname})",
             f"max sweep weight at phi=0 {max(mean_sweep[(d, 0.0)] for d in DEVICES):.3e}", "== 0",
             max(mean_sweep[(d, 0.0)] for d in DEVICES) == 0.0)
        ok6 = all(all(mean_sweep[(d, PHIS[i])] < mean_sweep[(d, PHIS[i + 1])] for i in range(len(PHIS) - 1))
                  for d in DEVICES)
        gate(f"G6 phi dial bites ({pname})", " ".join(f"{d}:{mean_sweep[(d, 1.0)]:.4f}" for d in DEVICES),
             "mean sweep weight strictly increasing in phi", ok6)

        # paired bootstrap: DG minus each device, at phi = 0 and phi = 1, headline rung
        for dev in DEVICES[1:]:
            for phi in (0.0, 1.0):
                obs, se, t = boot_sharpe_diff(store[(pname, "DG", phi, HEADLINE_RUNG, False)],
                                              store[(pname, dev, phi, HEADLINE_RUNG, False)])
                boot_rows.append(dict(panel=pname, device=dev, phi=phi, d_Sharpe_DG_minus_DEV=obs, SE=se, t=t))

        grid.append(dict(panel=pname, device="SPY", phi=np.nan, cost_bps=0.0, mmf=False,
                         CAGR=cagr(spy), Sharpe=sharpe(spy), MaxDD=maxdd(spy), Calmar=calmar(spy),
                         H1=halves(spy)[0], H2=halves(spy)[1], OOS_CAGR=cagr(spy[oos_mask]),
                         OOS_Sharpe=sharpe(spy[oos_mask]), OOS_MaxDD=maxdd(spy[oos_mask]),
                         IS_Sharpe=sharpe(spy[is_mask]), turnover_yr=0.0, sweep_turnover_yr=0.0,
                         mean_gross=1.0, mean_sweep_w=0.0))

    G = pd.DataFrame(grid)
    B = pd.DataFrame(boot_rows)
    nbooks = len(G[(G.device != "SPY") & (~G.mmf)])
    gate("G5b all books published", f"{nbooks} rows = 3 panels x 6 devices x 5 phi x 4 rungs", "360", nbooks == 360)

    # ---------------------------------------------------------------- the verdict table
    say("\n=== THE COMMITTED VERDICT, READ TWICE: cash at 0% (phi=0) and cash at carry ===")
    vrows = []
    for pname in panels:
        for dev in DEVICES[1:]:
            for rung in RUNGS:
                for mmf in (False, True):
                    base_dg = store[(pname, "DG", 0.0, rung, mmf)]
                    base_dev = store[(pname, dev, 0.0, rung, mmf)]
                    v0 = dict(SHARPE=sharpe(base_dg) > sharpe(base_dev), DD=maxdd(base_dg) > maxdd(base_dev),
                              CAGR=cagr(base_dg) > cagr(base_dev), CALMAR=calmar(base_dg) > calmar(base_dev))
                    for phi in PHIS:
                        a = store[(pname, "DG", phi, rung, mmf)]
                        b = store[(pname, dev, phi, rung, mmf)]
                        v = dict(SHARPE=sharpe(a) > sharpe(b), DD=maxdd(a) > maxdd(b),
                                 CAGR=cagr(a) > cagr(b), CALMAR=calmar(a) > calmar(b))
                        vrows.append(dict(panel=pname, device=dev, phi=phi, cost_bps=rung, mmf=mmf,
                                          dSharpe=sharpe(a) - sharpe(b), dCAGR=cagr(a) - cagr(b),
                                          dMaxDD=maxdd(a) - maxdd(b), dCalmar=calmar(a) - calmar(b),
                                          **{f"V_{k}": bool(v[k]) for k in v},
                                          **{f"FLIP_{k}": bool(v[k] != v0[k]) for k in v}))
    V = pd.DataFrame(vrows)
    head = V[(V.cost_bps == HEADLINE_RUNG) & (~V.mmf)]
    say(head[["panel", "device", "phi", "dSharpe", "dCAGR", "dMaxDD", "V_SHARPE", "V_DD", "V_CAGR",
              "V_CALMAR", "FLIP_SHARPE", "FLIP_DD", "FLIP_CAGR", "FLIP_CALMAR"]].to_string(
        index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n=== HOW MANY COMMITTED VERDICTS MOVE WHEN CASH EARNS CARRY? ===")
    for rung in RUNGS:
        for mmf in (False, True):
            sub = V[(V.cost_bps == rung) & (V.mmf == mmf) & (V.phi > 0)]
            n = len(sub)
            say(f"    {rung:4.0f} bps {'MMF ' if mmf else 'TRAD'}: "
                + "  ".join(f"{k} {int(sub[f'FLIP_{k}'].sum())}/{n}" for k in ("SHARPE", "DD", "CAGR", "CALMAR")))
    fl = V[(V.phi > 0) & (V[["FLIP_SHARPE", "FLIP_DD", "FLIP_CAGR", "FLIP_CALMAR"]].any(axis=1))]
    if len(fl):
        say("    every flipped cell:")
        say(fl[["panel", "device", "phi", "cost_bps", "mmf", "dSharpe", "dCAGR", "dMaxDD",
                "FLIP_SHARPE", "FLIP_DD", "FLIP_CAGR", "FLIP_CALMAR"]].to_string(
            index=False, float_format=lambda x: f"{x:.4f}"))
    else:
        say("    NONE — no committed device-vs-de-gross verdict moves at any (panel, device, phi, rung).")

    say("\n=== DOES CARRY WIDEN OR NARROW DE-GROSS's MARGIN?  (d = DG - DEV, 10 bps, traded sleeve) ===")
    piv = head.pivot_table(index=["panel", "device"], columns="phi", values="dSharpe")
    say(piv.to_string(float_format=lambda x: f"{x:+.4f}"))
    say("    (a MORE POSITIVE number at phi=1.00 than at phi=0.00 means carry STRENGTHENS de-gross)")
    widen = int(((piv[1.00] - piv[0.00]) > 0).sum())
    say(f"    margin widens in DG's favour at {widen} of {len(piv)} (panel, device) cells at 10 bps")

    say("\n=== PAIRED BLOCK BOOTSTRAP on DG - DEV Sharpe (10 bps, traded sleeve) ===")
    say(B.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- rule 8
    say("\n=== RULE 8 WALK-FORWARD — (device, phi) chosen on <= 2016-12-31 ONLY, 2017-2026 read ONCE ===")
    wf = []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        oos_mask = win >= pd.Timestamp(OOS_START)
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        base_res = base_cache[pname]
        for rung in RUNGS:
            bo = priced(base_res, rung).loc[win][oos_mask]
            cand = {(d, p): store[(pname, d, p, rung, False)] for d in DEVICES for p in PHIS}
            isw = {k: v[~oos_mask] for k, v in cand.items()}
            if rung == HEADLINE_RUNG and pname == "U56":
                gate("G7 choosers read no OOS row", f"max IS date {max(v.index.max() for v in isw.values()).date()}",
                     f"<= {IS_END}", max(v.index.max() for v in isw.values()) <= pd.Timestamp(IS_END))
            for cname, key in (("C_ISSHARPE", sharpe), ("C_ISCALMAR", calmar)):
                pick = max(isw, key=lambda k: (key(isw[k]) if np.isfinite(key(isw[k])) else -1e9))
                ro = cand[pick][oos_mask]
                lg = legs(ro, bo, spy[oos_mask], ro, spy[oos_mask])
                wf.append(dict(panel=pname, cost_bps=rung, chooser=cname, pick_device=pick[0], pick_phi=pick[1],
                               OOS_CAGR=cagr(ro), OOS_Sharpe=sharpe(ro), OOS_MaxDD=maxdd(ro),
                               BASE_OOS_Sharpe=sharpe(bo), BASE_OOS_CAGR=cagr(bo), BASE_OOS_MaxDD=maxdd(bo),
                               SPY_OOS_Sharpe=sharpe(spy[oos_mask]), SPY_OOS_CAGR=cagr(spy[oos_mask]),
                               SPY_OOS_MaxDD=maxdd(spy[oos_mask]), **{f"OOS_{k}": v for k, v in lg.items()}))
            for label, pick in (("C_ZEROPARAM(live DG phi=0)", ("DG", 0.0)), ("C_ZEROPARAM(DG phi=1 sweep)", ("DG", 1.0))):
                ro = cand[pick][oos_mask]
                lg = legs(ro, bo, spy[oos_mask], ro, spy[oos_mask])
                wf.append(dict(panel=pname, cost_bps=rung, chooser=label, pick_device=pick[0], pick_phi=pick[1],
                               OOS_CAGR=cagr(ro), OOS_Sharpe=sharpe(ro), OOS_MaxDD=maxdd(ro),
                               BASE_OOS_Sharpe=sharpe(bo), BASE_OOS_CAGR=cagr(bo), BASE_OOS_MaxDD=maxdd(bo),
                               SPY_OOS_Sharpe=sharpe(spy[oos_mask]), SPY_OOS_CAGR=cagr(spy[oos_mask]),
                               SPY_OOS_MaxDD=maxdd(spy[oos_mask]), **{f"OOS_{k}": v for k, v in lg.items()}))
    W = pd.DataFrame(wf)
    say(W[W.cost_bps == HEADLINE_RUNG][["panel", "chooser", "pick_device", "pick_phi", "OOS_CAGR", "OOS_Sharpe",
                                        "OOS_MaxDD", "BASE_OOS_Sharpe", "SPY_OOS_Sharpe", "OOS_pass4a",
                                        "OOS_pass4b"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- KEEP paths
    say("\n=== BOTH KEEP PATHS, EVERY CELL ===")
    for rung in RUNGS:
        for mmf in (False, True):
            sub = G[(G.cost_bps == rung) & (G.mmf == mmf) & (G.device != "SPY")]
            say(f"    {rung:4.0f} bps {'MMF ' if mmf else 'TRAD'}: "
                f"4a FULL {int(bcol(sub, 'FULL_pass4a').sum())} of {len(sub)}"
                f"   4b FULL {int(bcol(sub, 'FULL_pass4b').sum())} of {len(sub)}"
                f"   4a OOS {int(bcol(sub, 'OOS_pass4a').sum())} of {len(sub)}"
                f"   4b OOS {int(bcol(sub, 'OOS_pass4b').sum())} of {len(sub)}")
    p4b = G[(G.device != "SPY") & bcol(G, "FULL_pass4b")]
    if len(p4b):
        say("    4b FULL passers:")
        say(p4b[["panel", "device", "phi", "cost_bps", "mmf", "CAGR", "Sharpe", "MaxDD", "OOS_Sharpe"]].to_string(
            index=False, float_format=lambda x: f"{x:.4f}"))
    else:
        say("    4b FULL passers: NONE")
    fails = G[(G.cost_bps == HEADLINE_RUNG) & (~G.mmf) & (G.device != "SPY") & (~bcol(G, "FULL_pass4b"))]
    say(f"    binding legs on the {len(fails)} FULL 4b failures at 10 bps, traded sleeve "
        f"(count of cells the leg FAILS): "
        + json.dumps({k: int((~bcol(fails, k)).sum()) for k in
                      ["FULL_L_H1", "FULL_L_H2", "FULL_L_OOS", "FULL_L_DD", "FULL_L_CAGR"]}))

    # G10 recompute
    px, invest = panels["U56"]
    r2 = priced(backtest_percol(px, with_sweep(px, device_weights(px, invest, "DG"), 1.0)), HEADLINE_RUNG).loc[px.index[WARMUP:]]
    d10 = float((r2 - store[("U56", "DG", 1.0, HEADLINE_RUNG, False)]).abs().max())
    gate("G10 headline cell recompute", f"max|d| {d10:.3e}", "< 1e-12", d10 < 1e-12)

    OUT.mkdir(parents=True, exist_ok=True)
    G.to_csv(OUT / "grid.csv", index=False)
    V.to_csv(OUT / "verdicts.csv", index=False)
    B.to_csv(OUT / "bootstrap.csv", index=False)
    W.to_csv(OUT / "walkforward.csv", index=False)
    pd.DataFrame(GATES).to_csv(OUT / "gates.csv", index=False)
    say(f"\n    wrote {OUT}  ({time.time() - t0:.1f}s)")
    say(f"    GATES: {sum(1 for g in GATES if g['pass_'])} pass / {sum(1 for g in GATES if not g['pass_'])} fail")
    (OUT / "console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

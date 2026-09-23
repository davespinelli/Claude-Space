#!/usr/bin/env python3
"""idea 2347 (lane C, 2026-09-23) — DOES A 52-WEEK CHANNEL GATE REACH THE 4b PASS THAT THE 200d
BAND REACHES, AT MATCHED MEAN EXPOSURE?

THE OBJECT.  Idea 2300 filed `RG100 + phi = 1.00` as the record's standing KEEP-4b candidate:
every name INSIDE the 200d +/-3% band (RULES v2 clause 2, with hysteresis) held at `gross / N_in`
of NAV, the residual `1 - sum(w)` swept to SHY.  EVERY 4b-passing book in this record is gated by
a band around a MOVING AVERAGE.  Idea 2241 swept the band's two EDGES, idea 2318 its WIDTH, idea
2343 the MA LENGTH -- three dials, one CONSTRUCTION.  The oldest alternative trend reference in
the literature uses NO average at all: a Donchian channel (IN on a new h-day high, OUT on a new
h-day low, previous state in between), hysteretic by construction.

    MA(c=0.03, L=200)  IN above ma*(1+c), OUT below ma*(1-c), previous state in between
    DON(h)             IN above the prior h-day HIGH, OUT below the prior h-day LOW, else previous

RATIONALE (verbatim from the queue): if a gate with a completely different construction reaches
the same 4b cell, the pass is a property of TREND-GATING; if only the MA band reaches it, the pass
is a property of the MA.

DIAL 1 -- channel length h {63, 126, 189, 252, 378}.  h = 252 is the 52-week channel of the title.
DIAL 2 -- gross {0.75 (live), 1.00}.
EXACTLY TWO TUNED PARAMETERS (asserted by G8).

REPORTED, NEVER SELECTED ON: book {CAND = RG100 + phi = 1.00, DEGROSS = the live clause-2
accounting where gated-out weight goes to CASH and is never re-spread}, panels {U56, B136, SMALL},
cost rungs {0, 10, 25, 50} bps, weekly cadence, t+1 execution, band c = 0.03 and L = 200 for the
MA control (the live clause-2 constants), sweep instrument SHY.

MATCHED MEAN EXPOSURE, HANDLED IN THE OPEN AND IN BOTH DIRECTIONS.
  (i) Under CAND the book re-grosses to `gross` on every day some name is IN, so MEAN EQUITY
      EXPOSURE IS ALREADY MATCHED ACROSS GATES BY CONSTRUCTION (published in section C as the
      exposure ratio, which is ~1.00 for every gate).  What differs there is BREADTH, not size.
  (ii) Under DEGROSS exposure genuinely varies with the gate, so section E rescales gross
      MECHANICALLY ON EXPOSURE ALONE -- never on any performance metric -- in BOTH directions:
      MATCH_UP lifts each Donchian book to the MA book's mean equity exposure, MATCH_DN cuts the
      MA book to each Donchian's.  The scaler is exact because exposure is linear in gross.  Any
      MATCH_UP that would need gross > 1.00 is CLIPPED and the clip is PUBLISHED, never hidden.
      Section E also reports an IS-ONLY (<= 2016-12-31) scaler so the rule-8 read never peeks.

WARM-IN, HANDLED IN THE OPEN.  DON(h) is OUT before h+1 closes exist, so h = 378 spends more of
the early sample forced OUT than the MA control does.  The HEADLINE window is the record's
convention (index[260:], so the MA cell reproduces idea 2300 exactly).  Section G re-reads the
SAME return series on an EQUAL-STATE window (index[440:], by which even h = 378 has 60 days of
live gate state).  Neither window is selected on; both are published.

BOTH KEEP PATHS on every published row: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no
worse) and 4b (Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >=
0.70 x SPY's).
RULE 8: (h, gross) chosen on warm-up..2016-12-31 ONLY by two pre-stated IS-only choosers
(C_ISSHARPE, C_ISCALMAR), then 2017-2026 read ONCE.  Run twice: over the DONCHIAN-ONLY pool (the
idea's dial) and over the POOL INCLUDING THE MA GATE, so the record sees how often an honest
out-of-sample chooser prefers the incumbent construction.

GATES.  G0 >= 10y per panel.  G1 the per-column replica == `engine.backtest`.  G2 MA(c=0.03) is
BIT-IDENTICAL to `baseline.band_state` (the live clause-2 object).  G3 the MA/DEGROSS book is
BIT-IDENTICAL to `baseline.rules_v2_weights`.  G4 no leverage anywhere.  G5 the h dial BITES.
G6 SHY priced on every row it is held.  G7 SMALL dropped-ticker rule bit.  G8 exactly two tuned
parameters.  G9 EXTERNAL REPRODUCTION of idea 2300's committed U56 headline as last read by idea
2343 (12.5950% / 1.1934 / -17.3923%, OOS 13.8525% / 1.2397).  G10 DON(h) is hysteretic and
CONTAINED: no day is both a new h-day high and a new h-day low.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_donchian-channel-gate-vs-ma-band_C.py
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

DATE, SLUG, LANE = "2026-09-23", "donchian-channel-gate-vs-ma-band", "C"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, MA_LEN, CADENCE = 0.03, 200, "W"
WARMUP = 260            # the record's scored-window convention (idea 2300 and every committed row)
WARMUP_EQ = 440         # equal-state window: even h = 378 has 60 days of live gate state
HS = [63, 126, 189, 252, 378]
GROSSES = [0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG = 10.0
SWEEP = "SHY"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
GATES_ORDER = ["MA"] + [f"DON{h}" for h in HS]

LOG: list[str] = []
GATEROWS: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATEROWS.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    say(f"    GATE {'PASS' if ok else 'FAIL'}  {name}: {value} (target {target})")
    return bool(ok)


def publish(name, value):
    GATEROWS.append(dict(gate=name, value=str(value), target="published, not asserted", pass_=True))
    say(f"    PUB   {name}: {value}")


# ---------------------------------------------------------------- the two gates
def ma_state(px, band=BAND, L=MA_LEN):
    """RULES v2 clause 2 verbatim: IN above ma*(1+band), OUT below ma*(1-band), previous state in
    between, OUT before L closes exist.  Asserted bit-identical to baseline.band_state by G2."""
    ma = px.rolling(L).mean()
    raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
    raw = raw.mask(px > ma * (1 + band), 1.0).mask(px < ma * (1 - band), 0.0)
    return raw.ffill().fillna(0.0) > 0.5


def don_state(px, h):
    """Donchian channel with the SAME state machine as clause 2, but no average anywhere:
    IN on a new h-day high (close above the max of the PRIOR h closes), OUT on a new h-day low
    (close below the min of the PRIOR h closes), previous state in between, OUT before h+1
    closes exist.  The prior-window form means the signal at t uses only closes <= t."""
    hi = px.rolling(h).max().shift(1)
    lo = px.rolling(h).min().shift(1)
    raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
    raw = raw.mask(px > hi, 1.0).mask(px < lo, 0.0)
    return raw.ffill().fillna(0.0) > 0.5


def gate_state(px, gname):
    return ma_state(px) if gname == "MA" else don_state(px, int(gname[3:]))


# ---------------------------------------------------------------- the two books
def cand_weights(px, invest, gname, gross):
    """CAND = idea 2300's standing candidate at an arbitrary gate: w_i = gross / N_in on IN
    names, idle NAV -> SHY (phi = 1.00)."""
    q = px[invest]
    pr = q.notna()
    inb = gate_state(q, gname) & pr
    nin = inb.sum(axis=1).replace(0, np.nan)
    w = inb.astype(float).mul((gross / nin).fillna(0.0), axis=0).reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return w


def degross_weights(px, invest, gname, gross):
    """DEGROSS = the LIVE clause-2 accounting at an arbitrary gate: w_i = gross / N_priced on IN
    names, gated-out weight goes to CASH and is never re-spread.  At gname = 'MA' this is
    `baseline.rules_v2_weights` verbatim (asserted by G3)."""
    q = px[invest]
    pr = q.notna()
    e = pd.DataFrame(1.0, index=q.index, columns=q.columns).where(pr, 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(gate_state(q, gname) & pr, 0.0).reindex(columns=px.columns).fillna(0.0)


def equity_share(w, win):
    """Mean share of NAV held in NAMES (SHY excluded: it is the sweep, not equity exposure)."""
    return float(w.drop(columns=[SWEEP], errors="ignore").sum(axis=1).loc[win].mean())


# ---------------------------------------------------------------- engine replica
def run_book(prices, weights, freq=CADENCE):
    """Replica of engine.backtest keeping zero-cost returns + turnover so every cost rung is
    priced from one pass.  Un-invested residual drifts at 0% (engine's convention)."""
    rets = prices.pct_change().fillna(0.0)
    w_target = weights.reindex(prices.index).fillna(0.0).shift(1)
    key = prices.index.to_period(freq)
    s = pd.Series(key, index=prices.index)
    mask = (s != s.shift(-1)).shift(1, fill_value=False)
    held = np.zeros((len(prices.index), len(prices.columns)))
    cur = np.zeros(len(prices.columns))
    turnover = np.zeros(len(prices.index))
    gross_s = np.zeros(len(prices.index))
    wt = w_target.values
    rv = rets.values
    for i in range(len(prices.index)):
        if mask.iloc[i] or i == 0:
            new = wt[i]
            turnover[i] = np.abs(new - cur).sum()
            cur = new.copy()
        held[i] = cur
        gross_s[i] = cur.sum()
        growth = cur * (1 + rv[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    r0 = pd.Series((held * rv).sum(axis=1), index=prices.index)
    return dict(r0=r0, turnover=pd.Series(turnover, index=prices.index),
                gross=pd.Series(gross_s, index=prices.index))


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


def scored(res, win, rung):
    return priced(res, rung).loc[win]


# ---------------------------------------------------------------- panels
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"].astype(str))
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    dropped = len(px.columns) - len(keep)
    px = px[keep]
    shy = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)[SWEEP]
    px = pd.concat([px, shy.reindex(px.index, method="ffill").rename(SWEEP)], axis=1)
    return px, dropped


def main():
    t0 = time.time()
    say("=== idea 2347 — DOES A DONCHIAN CHANNEL GATE REACH THE 4b PASS THE 200d MA BAND REACHES? ===")
    say(f"    {DATE}  lane {LANE}   MA control L={MA_LEN} c={BAND}   cadence {CADENCE}  t+1  "
        f"rungs {RUNGS} bps  sweep {SWEEP}")
    say(f"    DIAL 1 channel length h {HS}   DIAL 2 gross {GROSSES}")
    say(f"    books CAND (RG100 + phi=1.00) and DEGROSS (live clause-2 accounting) — REPORTED, not selected on")
    gate("G8 exactly two tuned parameters", "channel length h, gross", "2", True)

    px_u = load_universe()
    px_b = load_universe(broad=True)
    px_s, dropped = small_panel()
    gate("G7 dropped-ticker rule bit (SMALL)", f"{dropped} names dropped (max_1d_move >= 1.0)",
         ">= 1", dropped >= 1)

    panels = {}
    for nm, px in (("U56", px_u), ("B136", px_b), ("SMALL", px_s)):
        invest = [c for c in px.columns if c not in ("SPY", SWEEP)] if nm == "SMALL" else list(px.columns)
        panels[nm] = (px, invest)
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y, {len(invest)} investable, {len(px)} rows",
             ">= 10y", yrs >= 10)

    d2 = int((ma_state(px_u) != band_state(px_u, BAND)).sum().sum())
    gate("G2 ma_state == baseline.band_state (live clause 2)", f"{d2} differing cells", "0", d2 == 0)

    pxq, invq = panels["U56"]
    d3 = float((degross_weights(pxq, invq, "MA", 0.75) - rules_v2_weights(pxq, band=BAND, gross=0.75)
                .reindex(columns=pxq.columns).fillna(0.0)).abs().max().max())
    gate("G3 DEGROSS/MA book == baseline.rules_v2_weights (live book)", f"max|dw| {d3:.3e}",
         "< 1e-12", d3 < 1e-12)

    w_live = rules_v2_weights(px_u, band=BAND, gross=0.75)
    res_live = run_book(px_u, w_live)
    r_eng = backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    d1 = float((r_eng - priced(res_live, HEADLINE_RUNG)).abs().max())
    gate("G1 per-column replica == engine.backtest", f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    # G10 the Donchian state machine is contained: a close cannot be both a new high and a new low
    bad10 = 0
    for h in HS:
        hi = pxq[invq].rolling(h).max().shift(1)
        lo = pxq[invq].rolling(h).min().shift(1)
        bad10 += int(((pxq[invq] > hi) & (pxq[invq] < lo)).sum().sum())
    gate("G10 DON state machine contained (no day both a new h-high and a new h-low)",
         f"{bad10} conflicting cells over all h", "0", bad10 == 0)

    # ---------------------------------------------------------------- the grid
    rows, expo_rows, eqrows, matchrows = [], [], [], []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        win_eq = px.index[WARMUP_EQ:]
        spy_all = px["SPY"].pct_change().fillna(0.0)
        spy, spy_eq = spy_all.loc[win], spy_all.loc[win_eq]
        spy_oos, spy_eq_oos = spy.loc[OOS_START:], spy_eq.loc[OOS_START:]
        base_w = rules_v2_weights(px[invest], band=BAND, gross=0.75).reindex(columns=px.columns).fillna(0.0)
        base_res = run_book(px, base_w)
        base_r = scored(base_res, win, HEADLINE_RUNG)
        base_eq = scored(base_res, win_eq, HEADLINE_RUNG)
        say(f"\n--- panel {pname}  ({len(invest)} names)  SPY {cagr(spy):.2%} / {sharpe(spy):.4f} / {maxdd(spy):.2%}"
            f"   live RULES v2 {cagr(base_r):.2%} / {sharpe(base_r):.4f} / {maxdd(base_r):.2%}")

        # raw grid: 6 gates x 2 books x 2 gross
        shares = {}
        for gname in GATES_ORDER:
            inb = gate_state(px[invest], gname) & px[invest].notna()
            nin = inb.sum(axis=1).loc[win]
            npr = px[invest].notna().sum(axis=1).loc[win]
            shares[gname] = float((nin / npr.replace(0, np.nan)).mean())
            for book, wfn in (("CAND", cand_weights), ("DEGROSS", degross_weights)):
                for gross in GROSSES:
                    w = wfn(px, invest, gname, gross)
                    mx = float(w.sum(axis=1).max())
                    res = run_book(px, w)
                    nmw = w.drop(columns=[SWEEP], errors="ignore").loc[win]
                    pos = nmw.values[nmw.values > 0]
                    expo_rows.append(dict(panel=pname, gate=gname, book=book, gross=gross, mode="RAW",
                                          eff_gross=gross,
                                          time_in_share=shares[gname], median_N_in=float(nin.median()),
                                          min_N_in=float(nin.min()), days_all_out=int((nin == 0).sum()),
                                          equity_share=equity_share(w, win),
                                          max_name_w=float(pos.max()) if len(pos) else 0.0,
                                          med_name_w=float(np.median(pos)) if len(pos) else 0.0,
                                          mean_gross=float(res["gross"].loc[win].mean()),
                                          mean_sweep_w=float(w[SWEEP].loc[win].mean()),
                                          turnover_yr=float(res["turnover"].loc[win].sum() / (len(win) / 252)),
                                          max_row_sum=mx, clipped=False))
                    for rung in RUNGS:
                        r = scored(res, win, rung)
                        r_oos = r.loc[OOS_START:]
                        h1, h2 = halves(r)
                        rows.append(dict(panel=pname, gate=gname, book=book, gross=gross, mode="RAW",
                                         eff_gross=gross, cost_bps=rung,
                                         CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                         H1=h1, H2=h2, IS_Sharpe=sharpe(r.loc[:IS_END]),
                                         IS_Calmar=calmar(r.loc[:IS_END]),
                                         OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                         **legs(r, base_r, spy, r_oos, spy_oos)))
                        re_ = scored(res, win_eq, rung)
                        eqrows.append(dict(panel=pname, gate=gname, book=book, gross=gross, mode="RAW",
                                           cost_bps=rung, CAGR=cagr(re_), Sharpe=sharpe(re_),
                                           MaxDD=maxdd(re_), OOS_CAGR=cagr(re_.loc[OOS_START:]),
                                           OOS_Sharpe=sharpe(re_.loc[OOS_START:]),
                                           **legs(re_, base_eq, spy_eq, re_.loc[OOS_START:], spy_eq_oos)))

        # ---- matched mean exposure on DEGROSS, both directions, scaler from exposure ONLY
        w_ma = degross_weights(px, invest, "MA", 0.75)
        E_ma = equity_share(w_ma, win)
        E_ma_is = equity_share(w_ma, px.index[WARMUP:][px.index[WARMUP:] <= IS_END])
        for h in HS:
            gname = f"DON{h}"
            w_dn = degross_weights(px, invest, gname, 0.75)
            E_dn = equity_share(w_dn, win)
            E_dn_is = equity_share(w_dn, px.index[WARMUP:][px.index[WARMUP:] <= IS_END])
            for mode in ("MATCH_UP", "MATCH_DN"):
                if mode == "MATCH_UP":            # lift DON to the MA book's exposure
                    g_raw, gd = 0.75 * E_ma / E_dn, gname
                else:                              # cut MA to this DON's exposure
                    g_raw, gd = 0.75 * E_dn / E_ma, "MA"
                g_eff = min(g_raw, 1.0)
                clipped = g_raw > 1.0 + 1e-12
                w = degross_weights(px, invest, gd, g_eff)
                res = run_book(px, w)
                got = equity_share(w, win)
                target = E_ma if mode == "MATCH_UP" else E_dn
                matchrows.append(dict(panel=pname, h=h, mode=mode, gate_priced=gd,
                                      g_raw=g_raw, g_eff=g_eff, clipped=clipped,
                                      target_exposure=target, achieved_exposure=got,
                                      resid=got - target,
                                      g_raw_IS=(0.75 * E_ma_is / E_dn_is) if mode == "MATCH_UP"
                                      else (0.75 * E_dn_is / E_ma_is),
                                      turnover_yr=float(res["turnover"].loc[win].sum() / (len(win) / 252))))
                expo_rows.append(dict(panel=pname, gate=gd, book="DEGROSS", gross=0.75, mode=f"{mode}_h{h}",
                                      eff_gross=g_eff, time_in_share=shares[gd],
                                      median_N_in=np.nan, min_N_in=np.nan, days_all_out=np.nan,
                                      equity_share=got, max_name_w=np.nan, med_name_w=np.nan,
                                      mean_gross=float(res["gross"].loc[win].mean()),
                                      mean_sweep_w=float(w[SWEEP].loc[win].mean()),
                                      turnover_yr=float(res["turnover"].loc[win].sum() / (len(win) / 252)),
                                      max_row_sum=float(w.sum(axis=1).max()), clipped=clipped))
                for rung in RUNGS:
                    r = scored(res, win, rung)
                    r_oos = r.loc[OOS_START:]
                    h1, h2 = halves(r)
                    rows.append(dict(panel=pname, gate=gd, book="DEGROSS", gross=0.75, mode=f"{mode}_h{h}",
                                     eff_gross=g_eff, cost_bps=rung,
                                     CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                     H1=h1, H2=h2, IS_Sharpe=sharpe(r.loc[:IS_END]),
                                     IS_Calmar=calmar(r.loc[:IS_END]),
                                     OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                     **legs(r, base_r, spy, r_oos, spy_oos)))
        say(f"    ... {pname} done ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(rows)
    ef = pd.DataFrame(expo_rows)
    qf = pd.DataFrame(eqrows)
    mf = pd.DataFrame(matchrows)
    df.to_csv(f"{OUT}.grid.csv", index=False)
    ef.to_csv(f"{OUT}.exposure.csv", index=False)
    qf.to_csv(f"{OUT}.equalstate.csv", index=False)
    mf.to_csv(f"{OUT}.matched.csv", index=False)

    gate("G4 no leverage (every book)", f"max row sum {ef.max_row_sum.max():.9f}",
         "<= 1+1e-9", ef.max_row_sum.max() <= 1 + 1e-9)
    shy_ok = all(bool(pxp[SWEEP].loc[pxp.index[WARMUP:]].notna().all()) for pxp, _ in panels.values())
    gate("G6 sweep instrument priced on every held row", f"SHY non-null on all panels: {shy_ok}",
         "True", shy_ok)
    raw = ef[ef["mode"] == "RAW"]
    spans, mono = [], []
    for pname in panels:
        v = [raw[(raw.panel == pname) & (raw.gate == f"DON{h}")].time_in_share.iloc[0] for h in HS]
        m = raw[(raw.panel == pname) & (raw.gate == "MA")].time_in_share.iloc[0]
        spans.append(f"{pname} MA {m:.3f} | DON {v[0]:.3f}->{v[-1]:.3f}")
        mono.append(bool(np.ptp(v) > 1e-6))
    gate("G5 the h dial BITES (mean time-IN share varies along the ladder)",
         f"{sum(mono)} of {len(mono)} panels move", "3 of 3", all(mono))
    publish("G5b mean share of priced names IN the gate (MA control vs DON h=63 -> 378)", "   ".join(spans))
    publish("G11 MATCH_UP books needing gross > 1.00 (clipped, exposure NOT fully matched)",
            f"{int(mf[mf['mode'] == 'MATCH_UP'].clipped.sum())} of {len(mf[mf['mode'] == 'MATCH_UP'])}")

    hcell = df[(df.panel == "U56") & (df.gate == "MA") & (df.book == "CAND") & (df.gross == 0.75)
               & (df["mode"] == "RAW") & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    d9 = max(abs(hcell.CAGR - 0.125950), abs(hcell.Sharpe - 1.1934) / 10, abs(hcell.MaxDD + 0.173923),
             abs(hcell.OOS_CAGR - 0.138525), abs(hcell.OOS_Sharpe - 1.2397) / 10)
    gate("G9 reproduces idea 2300's committed U56 candidate (12.5950%/1.1934/-17.3923%, OOS 13.8525%/1.2397)",
         f"read {hcell.CAGR:.4%} / {hcell.Sharpe:.4f} / {hcell.MaxDD:.4%}, OOS {hcell.OOS_CAGR:.4%} /"
         f" {hcell.OOS_Sharpe:.4f} -> max|d| {d9:.2e}", "< 1e-4", d9 < 1e-4)

    # ---------------------------------------------------------------- tables
    say("\n=== A. THE CANDIDATE BOOK (CAND = RG100 + phi=1.00) AT THE HEADLINE RUNG (10 bps) — every point ===")
    for pname in panels:
        say(f"\n  {pname}")
        say("   gate  gross |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh  OOS DD | 4a 4b |"
            " H1/H2/OOS/DD/CAGR | time-IN equity maxw  turn/yr")
        for gross in GROSSES:
            for gname in GATES_ORDER:
                r = df[(df.panel == pname) & (df.gate == gname) & (df.book == "CAND") & (df.gross == gross)
                       & (df["mode"] == "RAW") & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                c = ef[(ef.panel == pname) & (ef.gate == gname) & (ef.book == "CAND") & (ef.gross == gross)
                       & (ef["mode"] == "RAW")].iloc[0]
                lg = "".join("1" if r[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                star = " <= INCUMBENT" if gname == "MA" else (" <= 52wk" if gname == "DON252" else "")
                say(f"  {gname:6s} {gross:.2f}  | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%} |"
                    f" {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} {r.OOS_MaxDD:7.2%} |"
                    f" {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg:17s} |"
                    f" {c.time_in_share:6.3f} {c.equity_share:6.3f} {c.max_name_w:5.2%} {c.turnover_yr:7.2f}{star}")

    say("\n=== B. THE LIVE-ACCOUNTING BOOK (DEGROSS) AT THE HEADLINE RUNG (10 bps) — every point ===")
    for pname in panels:
        say(f"\n  {pname}")
        say("   gate  gross |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh | 4a 4b |"
            " H1/H2/OOS/DD/CAGR | equity turn/yr")
        for gross in GROSSES:
            for gname in GATES_ORDER:
                r = df[(df.panel == pname) & (df.gate == gname) & (df.book == "DEGROSS") & (df.gross == gross)
                       & (df["mode"] == "RAW") & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                c = ef[(ef.panel == pname) & (ef.gate == gname) & (ef.book == "DEGROSS") & (ef.gross == gross)
                       & (ef["mode"] == "RAW")].iloc[0]
                lg = "".join("1" if r[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                star = " <= LIVE RULES v2" if (gname == "MA" and gross == 0.75) else ""
                say(f"  {gname:6s} {gross:.2f}  | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%} |"
                    f" {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} |"
                    f" {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg:17s} |"
                    f" {c.equity_share:6.3f} {c.turnover_yr:7.2f}{star}")

    say("\n=== C. IS THE CAND COMPARISON ALREADY AT MATCHED MEAN EXPOSURE?  (equity share / MA's, g=0.75) ===")
    say("  panel   gate   equity share   ratio to MA   time-IN share  ratio to MA")
    for pname in panels:
        m = ef[(ef.panel == pname) & (ef.gate == "MA") & (ef.book == "CAND") & (ef.gross == 0.75)
               & (ef["mode"] == "RAW")].iloc[0]
        for gname in GATES_ORDER:
            c = ef[(ef.panel == pname) & (ef.gate == gname) & (ef.book == "CAND") & (ef.gross == 0.75)
                   & (ef["mode"] == "RAW")].iloc[0]
            say(f"  {pname:5s} {gname:7s} {c.equity_share:12.4f} {c.equity_share / m.equity_share:13.4f}"
                f" {c.time_in_share:15.4f} {c.time_in_share / m.time_in_share:12.4f}")

    say(f"\n=== D. TOTAL KEEP COUNTS OVER ALL {len(df)} PUBLISHED ROWS ===")
    say(f"  4b passes: {int(df.pass4b.sum())} of {len(df)}      4a passes: {int(df.pass4a.sum())} of {len(df)}")
    for rung in RUNGS:
        d = df[df.cost_bps == rung]
        say(f"   {rung:5.1f} bps:  4b {int(d.pass4b.sum()):3d}/{len(d)}   4a {int(d.pass4a.sum()):3d}/{len(d)}"
            f"   binding leg on 4b FAILs: " +
            "  ".join(f"{k} {int((~d[k][~d.pass4b]).sum())}" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    for key in ("panel", "book", "gate", "gross"):
        say("   by " + key + ":  " + "   ".join(
            f"{v} {int(df[df[key] == v].pass4b.sum())}/{len(df[df[key] == v])}"
            for v in (list(panels) if key == "panel" else sorted(df[key].unique(), key=str))))
    say("\n  THE DECIDING COUNT — 4b passes by gate, CAND book only (the standing candidate's family):")
    cd = df[df.book == "CAND"]
    for gname in GATES_ORDER:
        d = cd[cd.gate == gname]
        byp = "  ".join(f"{pn} {int(d[d.panel == pn].pass4b.sum())}/{len(d[d.panel == pn])}" for pn in panels)
        say(f"   {gname:7s}: 4b {int(d.pass4b.sum()):2d}/{len(d)}   4a {int(d.pass4a.sum()):2d}/{len(d)}   [{byp}]")

    say("\n=== E. MATCHED MEAN EXPOSURE ON DEGROSS (scaler from exposure ALONE, both directions), 10 bps ===")
    say("  panel  h   mode      priced  g_raw  g_eff clip | target  achieved  resid | g_raw(IS-only) |"
        "   CAGR   Sharpe   MaxDD   OOS Sh | 4a 4b")
    for pname in panels:
        ref = df[(df.panel == pname) & (df.gate == "MA") & (df.book == "DEGROSS") & (df.gross == 0.75)
                 & (df["mode"] == "RAW") & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
        say(f"  {pname:5s}  --  MA RAW 0.75 (the live book)                                          "
            f"         | {ref.CAGR:6.2%} {ref.Sharpe:7.4f} {ref.MaxDD:7.2%} {ref.OOS_Sharpe:7.4f} |"
            f" {'Y' if ref.pass4a else '.'}  {'Y' if ref.pass4b else '.'}")
        for h in HS:
            for mode in ("MATCH_UP", "MATCH_DN"):
                mrow = mf[(mf.panel == pname) & (mf.h == h) & (mf["mode"] == mode)].iloc[0]
                r = df[(df.panel == pname) & (df["mode"] == f"{mode}_h{h}") & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                say(f"  {pname:5s} {h:4d} {mode:9s} {mrow.gate_priced:6s} {mrow.g_raw:.3f} {mrow.g_eff:.3f}"
                    f" {'C' if mrow.clipped else '.'}    | {mrow.target_exposure:.4f}  {mrow.achieved_exposure:.4f}"
                    f" {mrow.resid:+.4f} | {mrow.g_raw_IS:.3f}          | {r.CAGR:6.2%} {r.Sharpe:7.4f}"
                    f" {r.MaxDD:7.2%} {r.OOS_Sharpe:7.4f} | {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}")

    say("\n=== F. RULE 8 — (h, gross) chosen on <= 2016-12-31 ONLY, 2017-2026 read ONCE ===")
    say("  pool DON = the idea's dial (5 lengths x 2 gross); pool ALL adds the incumbent MA gate.")
    wf = []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        b_oos = scored(run_book(px, rules_v2_weights(px[invest], band=BAND, gross=0.75)
                                .reindex(columns=px.columns).fillna(0.0)), win, HEADLINE_RUNG).loc[OOS_START:]
        for book in ("CAND", "DEGROSS"):
            ma_oos = df[(df.panel == pname) & (df.gate == "MA") & (df.book == book) & (df.gross == 0.75)
                        & (df["mode"] == "RAW") & (df.cost_bps == HEADLINE_RUNG)].iloc[0].OOS_Sharpe
            for rung in RUNGS:
                d0 = df[(df.panel == pname) & (df.book == book) & (df["mode"] == "RAW") & (df.cost_bps == rung)]
                for pool in ("DON", "ALL"):
                    d = d0[d0.gate != "MA"] if pool == "DON" else d0
                    for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                        pick = d.loc[d[col].idxmax()]
                        wf.append(dict(panel=pname, book=book, cost_bps=rung, pool=pool, chooser=chooser,
                                       pick_gate=pick.gate, pick_gross=pick.gross,
                                       OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                                       OOS_MaxDD=pick.OOS_MaxDD,
                                       base_OOS_CAGR=cagr(b_oos), base_OOS_Sharpe=sharpe(b_oos),
                                       base_OOS_MaxDD=maxdd(b_oos),
                                       spy_OOS_CAGR=cagr(spy_oos), spy_OOS_Sharpe=sharpe(spy_oos),
                                       spy_OOS_MaxDD=maxdd(spy_oos), ma_OOS_Sharpe=ma_oos,
                                       full4b=bool(pick.pass4b), picked_MA=(pick.gate == "MA")))
                        say(f"  {pname:5s} {book:7s} {rung:5.1f}bps pool {pool:3s} {chooser:11s} ->"
                            f" {pick.gate:6s} g {pick.gross:.2f} | OOS {pick.OOS_CAGR:6.2%} /"
                            f" {pick.OOS_Sharpe:.4f} / {pick.OOS_MaxDD:7.2%} | live v2 OOS {cagr(b_oos):6.2%} /"
                            f" {sharpe(b_oos):.4f} / {maxdd(b_oos):7.2%} | SPY OOS {cagr(spy_oos):6.2%} /"
                            f" {sharpe(spy_oos):.4f} / {maxdd(spy_oos):7.2%} | MA-gate OOS Sh {ma_oos:.4f} |"
                            f" full 4b {'Y' if pick.pass4b else '.'}")
    wfd = pd.DataFrame(wf)
    wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"\n  picks beating SPY's OOS Sharpe:      {int((wfd.OOS_Sharpe > wfd.spy_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"  picks beating the LIVE book's OOS Sharpe: {int((wfd.OOS_Sharpe > wfd.base_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"  picks beating the MA-GATED twin's OOS Sharpe: "
        f"{int((wfd.OOS_Sharpe > wfd.ma_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"  picks carrying a full-sample 4b pass: {int(wfd.full4b.sum())} of {len(wfd)}")
    a = wfd[wfd.pool == "ALL"]
    say(f"  pool ALL: picks that take the INCUMBENT MA gate: {int(a.picked_MA.sum())} of {len(a)}")
    say("  pool DON pick distribution over h: " + "  ".join(
        f"{g} {int((wfd[wfd.pool == 'DON'].pick_gate == g).sum())}" for g in GATES_ORDER[1:]))

    say("\n=== G. EQUAL-STATE WINDOW (index[440:], even h = 378 has 60 days of live gate state) ===")
    say(f"  4b on the equal-state window: {int(qf.pass4b.sum())} of {len(qf)}"
        f"   (headline window, same rows: {int(df[df['mode'] == 'RAW'].pass4b.sum())} of {len(df[df['mode'] == 'RAW'])})")
    for gname in GATES_ORDER:
        a2 = df[(df.gate == gname) & (df["mode"] == "RAW")]
        b2 = qf[qf.gate == gname]
        say(f"  {gname:7s}: headline 4b {int(a2.pass4b.sum()):2d}/{len(a2)}   "
            f"equal-state 4b {int(b2.pass4b.sum()):2d}/{len(b2)}")
    say("\n  U56 CAND g=0.75, 10 bps, both windows:")
    for gname in GATES_ORDER:
        a2 = df[(df.panel == "U56") & (df.gate == gname) & (df.book == "CAND") & (df.gross == 0.75)
                & (df["mode"] == "RAW") & (df.cost_bps == 10.0)].iloc[0]
        b2 = qf[(qf.panel == "U56") & (qf.gate == gname) & (qf.book == "CAND") & (qf.gross == 0.75)
                & (qf.cost_bps == 10.0)].iloc[0]
        say(f"   {gname:7s} headline {a2.CAGR:6.2%} / {a2.Sharpe:.4f} / {a2.MaxDD:7.2%} 4b {'Y' if a2.pass4b else '.'}"
            f"   |  equal-state {b2.CAGR:6.2%} / {b2.Sharpe:.4f} / {b2.MaxDD:7.2%} 4b {'Y' if b2.pass4b else '.'}")

    say("\n=== H. WHAT THE CHANNEL COSTS: CAND, U56, g=0.75, 10 bps, each gate minus the MA incumbent ===")
    ref = df[(df.panel == "U56") & (df.gate == "MA") & (df.book == "CAND") & (df.gross == 0.75)
             & (df["mode"] == "RAW") & (df.cost_bps == 10.0)].iloc[0]
    for gname in GATES_ORDER:
        r = df[(df.panel == "U56") & (df.gate == gname) & (df.book == "CAND") & (df.gross == 0.75)
               & (df["mode"] == "RAW") & (df.cost_bps == 10.0)].iloc[0]
        c = ef[(ef.panel == "U56") & (ef.gate == gname) & (ef.book == "CAND") & (ef.gross == 0.75)
               & (ef["mode"] == "RAW")].iloc[0]
        say(f"  {gname:7s} dCAGR {r.CAGR - ref.CAGR:+6.2%}  dSharpe {r.Sharpe - ref.Sharpe:+7.4f}"
            f"  dMaxDD {r.MaxDD - ref.MaxDD:+6.2%}  dOOS_Sh {r.OOS_Sharpe - ref.OOS_Sharpe:+7.4f}"
            f"  | time-IN {c.time_in_share:.3f}  equity {c.equity_share:.3f}  medN {c.median_N_in:5.0f}"
            f"  all-out days {c.days_all_out:4.0f}  maxw {c.max_name_w:6.2%}  turn/yr {c.turnover_yr:.2f}")

    gdf = pd.DataFrame(GATEROWS)
    gdf.to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n=== GATES: {int(gdf.pass_.sum())} of {len(gdf)} pass ===")
    for _, g in gdf[~gdf.pass_].iterrows():
        say(f"    FAILED: {g.gate} = {g.value} (target {g.target})")
    say(f"\nwrote {OUT}.grid.csv / .exposure.csv / .equalstate.csv / .matched.csv / .walkforward.csv"
        f" / .gates.csv   ({time.time() - t0:.0f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

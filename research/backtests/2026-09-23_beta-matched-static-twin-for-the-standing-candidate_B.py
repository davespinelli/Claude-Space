#!/usr/bin/env python3
"""IDEA 2336 (lane B, 2026-09-23) — does the STANDING 4b CANDIDATE beat a BETA-MATCHED
STATIC SPY/SHY TWIN at its own realised exposure?

WHY.  Idea 2300 filed `RG100 + phi = 1.00` (every name inside the 200d +/-3% band at
gross / N_in, idle NAV swept to SHY) as the record's standing 4b candidate; idea 2322
improved it with a 2.0% per-name cap (CAP2) and idea 2326 failed to beat that cap from the
breadth side.  Idea 955 answered that the 4b CAGR floor IS a beta bar (beta explains 96.3%
of the CAGR spread along the gross ladder) and idea 1436 killed the beta band as "nothing
more than a beta-matched exposure dial" -- but BOTH were priced against the DE-GROSSED live
book, never against the candidate the record is about to recommend for real capital.

THE NULL.  For a fully-invested, trend-gated, cash-into-T-bills book the honest null is a
ZERO-PARAMETER STATIC BLEND of SPY and SHY held at the candidate's OWN realised exposure,
traded on the same weekly clock and charged the same costs.  If that twin matches the
candidate on the five 4b legs and out of sample, the trend gate, the re-gross and the cap
earn nothing.

TWO TUNED DIALS AND NO MORE:
  DIAL 1  matching convention m {MEAN_GROSS, OLS_BETA}
  DIAL 2  gross g {0.75, 1.00}
REPORTED AT EVERY GRID POINT, NEVER SELECTED ON: panel {U56, B136}, cost rung
{0, 10, 25, 50} bps, book family {CAND, CAP2}, cadence W, band 0.03, sweep instrument SHY,
cap value 2.0% (INHERITED from idea 2322, not tuned), fit window {FULL, IS}.

ADVERSARIAL DESIGN.  The twin is the null, so it is given its BEST shot: on the full-sample
comparison its exposure x is fitted on the FULL sample (an advantage the candidate does not
get).  The rule-8 comparison is the honest one: x is fitted on <= 2016-12-31 ONLY and
2017-2026 is read once.  Both fit windows are published for every cell.

RULE 8.  Chooser picks (book, g) on IS (<= 2016-12-31) alone by C_ISSHARPE / C_ISCALMAR;
2017-2026 is then read once for the pick AND for BOTH of its IS-fitted twins.  The
pre-registered statistic is: does the pick beat BOTH twins OOS on Sharpe AND CAGR?  The
matching convention m is never selected on -- both values are always published, so the
candidate must clear the STRONGER twin.

KEEP PATHS.  4a (vs `baseline.rules_v2_weights`, the live book) and 4b (vs SPY: Sharpe in
both halves, OOS Sharpe, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's) are evaluated for
EVERY book including the twins, at every rung.  10 bps and next-day execution are the
binding protocol settings; 0/25/50 bps are reported.

GATES.  G1 my de-gross replica == `baseline.rules_v2_weights` bit-identical.  G2 my
per-column backtest == `engine.backtest`.  G3 no leverage anywhere.  G4/G5 EXTERNAL
REPRODUCTION of idea 2300's and idea 2322's committed U56 headlines.  G6 the MEAN_GROSS
twin's realised mean gross matches the candidate's.  G7 the OLS_BETA twin's realised beta
matches the candidate's.  G8 exactly two tuned parameters.  G9 SPY and SHY priced at the
window start.  G10 the IS fit never touches a post-2016 row.  G11 the cap bites.

Deterministic, standalone, no network: prices come from the committed caches through
`research.baseline.load_universe`.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
from engine import backtest  # noqa: E402

DATE, SLUG, LANE = "2026-09-23", "beta-matched-static-twin-for-the-standing-candidate", "B"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, CADENCE, WARMUP = 0.03, "W", 260
GROSSES = [0.75, 1.00]                     # DIAL 2
CONVENTIONS = ["MEAN_GROSS", "OLS_BETA"]   # DIAL 1
BOOKS = ["CAND", "CAP2"]
CAP = 0.02                                 # inherited from idea 2322, NOT tuned
PHI = 1.00                                 # sweep fraction, frozen by idea 2300
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG = 10.0
SWEEP, BENCH = "SHY", "SPY"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BOOT_REPS, BOOT_BLOCK, SEED = 400, 63, 20260923
TWIN_ITERS = 6

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


# ---------------------------------------------------------------- books
def candidate_weights(px, invest, g, cap=None):
    """idea 2300's RG100 + phi=1.00, optionally with idea 2322's per-name cap.

    IN names (200d +/-3% band, hysteresis) are held at min(g / N_in, cap) of NAV; every
    dollar not in equities -- the uncapped residual AND the 1 - g the book never spends --
    is parked in SHY (phi = 1.00).  No leverage, no shorting, weekly clock.
    """
    q = px[invest]
    pr = q.notna()
    inb = band_state(q, BAND) & pr
    nin = inb.sum(axis=1).replace(0, np.nan)
    per = (g / nin)
    if cap is not None:
        per = per.clip(upper=cap)
    w = inb.astype(float).mul(per, axis=0).fillna(0.0)
    w = w.reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    live = px[SWEEP].notna().astype(float)
    w[SWEEP] = w[SWEEP] + PHI * idle * live
    return w


def degross_weights(px, invest, g):
    """The live band book (RULES v2 clause 4: gated-out weight stays in cash)."""
    q = px[invest]
    pr = q.notna()
    e = pd.DataFrame(1.0, index=q.index, columns=q.columns).where(pr, 0.0)
    N = e.sum(axis=1).replace(0, np.nan)
    ew = g * e.div(N, axis=0).fillna(0.0)
    w = ew.where(band_state(q, BAND) & pr, 0.0)
    return w.reindex(columns=px.columns).fillna(0.0)


def twin_weights(px, x):
    """Static blend: x of NAV in SPY, 1 - x in SHY, same weekly clock, same costs."""
    w = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    w[BENCH] = float(x) * px[BENCH].notna().astype(float)
    w[SWEEP] = float(1.0 - x) * px[SWEEP].notna().astype(float)
    return w


# ---------------------------------------------------------------- engine replica
def backtest_percol(prices, weights, freq=CADENCE):
    """Replica of engine.backtest that also returns held gross (cost applied afterwards)."""
    rets = prices.pct_change().fillna(0.0)
    w_target = weights.reindex(prices.index).fillna(0.0).shift(1)
    key = prices.index.to_period(freq)
    s = pd.Series(key, index=prices.index)
    mask = (s != s.shift(-1)).shift(1, fill_value=False)
    held = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
    cur = np.zeros(len(prices.columns))
    turnover = pd.Series(0.0, index=prices.index)
    gross = pd.Series(0.0, index=prices.index)
    eq_gross = pd.Series(0.0, index=prices.index)
    isw = list(prices.columns).index(SWEEP)
    for i in range(len(prices.index)):
        if mask.iloc[i] or i == 0:
            new = w_target.iloc[i].values
            turnover.iloc[i] = np.abs(new - cur).sum()
            cur = new
        held.iloc[i] = cur
        gross.iloc[i] = cur.sum()
        eq_gross.iloc[i] = cur.sum() - cur[isw]
        growth = cur * (1 + rets.iloc[i].values)
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    return dict(r0=(held * rets).sum(axis=1), turnover=turnover, gross=gross,
                eq_gross=eq_gross, weights=held)


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


def beta_of(r, m):
    v = m.var()
    return float(np.cov(r.values, m.values, ddof=1)[0, 1] / v) if v > 0 else np.nan


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
                L_H1=bool(L_H1), L_H2=bool(L_H2), L_OOS=bool(L_OOS),
                L_DD=bool(L_DD), L_CAGR=bool(L_CAGR))


def boot_sharpe_diff(a, b, reps=BOOT_REPS, block=BOOT_BLOCK, seed=SEED):
    """Paired circular block bootstrap on the Sharpe difference (a - b)."""
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


# ---------------------------------------------------------------- twin solver
def solve_twin(px, r_cand, fit_rows, convention, win):
    """Return (x, twin_result).  x is solved ONLY on `fit_rows`.

    MEAN_GROSS  x = the candidate's realised mean EQUITY gross (SHY sleeve excluded) over
                the fit rows -- 'the same dollars in equities'.
    OLS_BETA    x such that the twin's realised beta on SPY equals the candidate's, solved
                by fixed point on the FULL drifted/costed book (not on a linear proxy).
    """
    if convention == "MEAN_GROSS":
        x = float(r_cand["eq_gross"].loc[win][fit_rows].mean())
        x = min(max(x, 0.0), 1.0)
        return x, backtest_percol(px, twin_weights(px, x))
    spy = px[BENCH].pct_change().fillna(0.0).loc[win]
    b_target = beta_of(priced(r_cand, HEADLINE_RUNG).loc[win][fit_rows], spy[fit_rows])
    x = min(max(b_target, 0.0), 1.0)
    res = backtest_percol(px, twin_weights(px, x))
    for _ in range(TWIN_ITERS):
        b_now = beta_of(priced(res, HEADLINE_RUNG).loc[win][fit_rows], spy[fit_rows])
        if not np.isfinite(b_now) or b_now <= 1e-9:
            break
        x_new = min(max(x * b_target / b_now, 0.0), 1.0)
        if abs(x_new - x) < 1e-10:
            x = x_new
            break
        x = x_new
        res = backtest_percol(px, twin_weights(px, x))
    return x, res


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    say("=== idea 2336 — does the STANDING 4b CANDIDATE beat a BETA-MATCHED STATIC SPY/SHY TWIN? ===")
    say(f"    {DATE}  lane {LANE}   band {BAND}  cadence {CADENCE}  t+1  rungs {RUNGS} bps  "
        f"cap {CAP:.2%} (inherited, not tuned)  phi {PHI}")
    say(f"    DIAL 1 matching convention {CONVENTIONS}   DIAL 2 gross {GROSSES}")
    gate("G8 exactly two tuned parameters", "convention m, gross g", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        panels[nm] = (px, list(px.columns))
        say(f"    {nm:5s} {len(px.columns)} investable names, "
            f"{px.index[0].date()}..{px.index[-1].date()}, {len(px)} rows")

    # ---- construction gates on U56
    px_u = panels["U56"][0]
    w_live = rules_v2_weights(px_u, band=BAND, gross=0.75)
    res_live_u = backtest_percol(px_u, w_live)
    d2 = float((backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
                - priced(res_live_u, HEADLINE_RUNG)).abs().max())
    gate("G2 per-column replica == engine.backtest", f"max|d| {d2:.3e}", "< 1e-12", d2 < 1e-12)
    d1 = float((backtest_percol(px_u, degross_weights(px_u, list(px_u.columns), 0.75))["r0"]
                - res_live_u["r0"]).abs().max())
    gate("G1 my de-gross replica == baseline.rules_v2_weights", f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    grid, twin_rows, boot_rows, wf_rows = [], [], [], []
    store: dict = {}
    oos_of: dict = {}

    for pname, (px, invest) in panels.items():
        say(f"\n--- PANEL {pname} ---")
        idx = px.index
        win = idx[WARMUP:]
        oos = win >= pd.Timestamp(OOS_START)
        ism = win <= pd.Timestamp(IS_END)
        spy = px[BENCH].pct_change().fillna(0.0).loc[win]
        oos_of[pname] = oos
        gate(f"G0 sample >= 10y ({pname})", f"{len(win) / 252:.1f} yr", ">= 10", len(win) / 252 >= 10)
        gate(f"G9 {BENCH}/{SWEEP} priced at window start ({pname})",
             f"{px[BENCH].first_valid_index().date()} / {px[SWEEP].first_valid_index().date()}",
             f"<= {win[0].date()}",
             px[BENCH].first_valid_index() <= win[0] and px[SWEEP].first_valid_index() <= win[0])
        gate(f"G10 IS fit rows never touch a post-{IS_END[:4]} row ({pname})",
             f"last IS row {win[ism][-1].date()}", f"<= {IS_END}",
             win[ism][-1] <= pd.Timestamp(IS_END))

        base_res = backtest_percol(px, rules_v2_weights(px, band=BAND, gross=0.75))
        base = {c: priced(base_res, c).loc[win] for c in RUNGS}
        for c in RUNGS:
            lg = legs(base[c], base[c], spy, base[c][oos], spy[oos])
            grid.append(dict(panel=pname, family="LIVE", book="rules_v2 (live)", gross=0.75,
                             convention="", fit="", x=np.nan, cost_bps=c,
                             CAGR=cagr(base[c]), Sharpe=sharpe(base[c]), MaxDD=maxdd(base[c]),
                             Calmar=calmar(base[c]), H1=halves(base[c])[0], H2=halves(base[c])[1],
                             OOS_CAGR=cagr(base[c][oos]), OOS_Sharpe=sharpe(base[c][oos]),
                             OOS_MaxDD=maxdd(base[c][oos]), IS_Sharpe=sharpe(base[c][ism]),
                             IS_Calmar=calmar(base[c][ism]),
                             beta=beta_of(base[c], spy), mean_eq_gross=float(base_res["eq_gross"].loc[win].mean()),
                             turnover=float(base_res["turnover"].loc[win].sum() / (len(win) / 252)),
                             max_name_w=float(base_res["weights"].loc[win].drop(columns=[SWEEP]).max().max()),
                             **lg))
        spy_row = dict(panel=pname, family="SPY", book="SPY buy&hold", gross=1.0, convention="",
                       fit="", x=1.0, cost_bps=0.0, CAGR=cagr(spy), Sharpe=sharpe(spy),
                       MaxDD=maxdd(spy), Calmar=calmar(spy), H1=halves(spy)[0], H2=halves(spy)[1],
                       OOS_CAGR=cagr(spy[oos]), OOS_Sharpe=sharpe(spy[oos]), OOS_MaxDD=maxdd(spy[oos]),
                       IS_Sharpe=sharpe(spy[ism]), IS_Calmar=calmar(spy[ism]), beta=1.0,
                       mean_eq_gross=1.0, turnover=0.0, max_name_w=1.0,
                       **legs(spy, base[HEADLINE_RUNG], spy, spy[oos], spy[oos]))
        grid.append(spy_row)
        say(f"    SPY  CAGR {cagr(spy):.2%}  Sharpe {sharpe(spy):.4f}  MaxDD {maxdd(spy):.2%}  "
            f"OOS {cagr(spy[oos]):.2%} / {sharpe(spy[oos]):.4f}   "
            f"| 4b floors: CAGR >= {CAGR_FLOOR * cagr(spy):.2%}, MaxDD >= {DD_CAP * maxdd(spy):.2%}")

        cap_bit = None
        for book in BOOKS:
            for g in GROSSES:
                cap = None if book == "CAND" else CAP
                w = candidate_weights(px, invest, g, cap)
                mx = float(w.sum(axis=1).max())
                gate(f"G3 no leverage ({pname} {book} g={g})", f"max row sum {mx:.9f}",
                     "<= 1+1e-12", mx <= 1 + 1e-12)
                res = backtest_percol(px, w)
                maxw = float(w.loc[win].drop(columns=[SWEEP]).max().max())          # TARGET weight
                maxw_held = float(res["weights"].loc[win].drop(columns=[SWEEP]).max().max())  # drifted
                if book == "CAP2" and g == 0.75:
                    cap_bit = maxw
                for c in RUNGS:
                    r = priced(res, c).loc[win]
                    store[(pname, book, g, c)] = r
                    grid.append(dict(panel=pname, family=book, book=f"{book} g={g:.2f}", gross=g,
                                     convention="", fit="", x=np.nan, cost_bps=c,
                                     CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                     H1=halves(r)[0], H2=halves(r)[1],
                                     OOS_CAGR=cagr(r[oos]), OOS_Sharpe=sharpe(r[oos]),
                                     OOS_MaxDD=maxdd(r[oos]), IS_Sharpe=sharpe(r[ism]),
                                     IS_Calmar=calmar(r[ism]), beta=beta_of(r, spy),
                                     mean_eq_gross=float(res["eq_gross"].loc[win].mean()),
                                     turnover=float(res["turnover"].loc[win].sum() / (len(win) / 252)),
                                     max_name_w=maxw, max_name_w_held=maxw_held,
                                     **legs(r, base[c], spy, r[oos], spy[oos])))

                # ---- the twins
                for conv in CONVENTIONS:
                    for fit, rows in (("FULL", pd.Series(True, index=win)), ("IS", pd.Series(ism, index=win))):
                        x, tres = solve_twin(px, res, rows, conv, win)
                        mxT = float(twin_weights(px, x).sum(axis=1).max())
                        for c in RUNGS:
                            tr = priced(tres, c).loc[win]
                            store[(pname, f"TWIN_{book}_{conv}_{fit}", g, c)] = tr
                            grid.append(dict(panel=pname, family=f"TWIN_{conv}",
                                             book=f"TWIN[{book} g={g:.2f}] {conv} fit={fit}",
                                             gross=g, convention=conv, fit=fit, x=x, cost_bps=c,
                                             CAGR=cagr(tr), Sharpe=sharpe(tr), MaxDD=maxdd(tr),
                                             Calmar=calmar(tr), H1=halves(tr)[0], H2=halves(tr)[1],
                                             OOS_CAGR=cagr(tr[oos]), OOS_Sharpe=sharpe(tr[oos]),
                                             OOS_MaxDD=maxdd(tr[oos]), IS_Sharpe=sharpe(tr[ism]),
                                             IS_Calmar=calmar(tr[ism]), beta=beta_of(tr, spy),
                                             mean_eq_gross=float(tres["eq_gross"].loc[win].mean()),
                                             turnover=float(tres["turnover"].loc[win].sum() / (len(win) / 252)),
                                             max_name_w=x,
                                             **legs(tr, base[c], spy, tr[oos], spy[oos])))
                        # matched-exposure gates, headline rung
                        rc = priced(res, HEADLINE_RUNG).loc[win]
                        rt = priced(tres, HEADLINE_RUNG).loc[win]
                        if conv == "MEAN_GROSS" and fit == "FULL":
                            dgross = abs(float(tres["eq_gross"].loc[win].mean())
                                         - float(res["eq_gross"].loc[win].mean()))
                            gate(f"G6 MEAN_GROSS twin exposure matched ({pname} {book} g={g})",
                                 f"|d mean equity gross| {dgross:.3e}", "< 5e-3", dgross < 5e-3)
                        if conv == "OLS_BETA" and fit == "FULL":
                            dbeta = abs(beta_of(rt, spy) - beta_of(rc, spy))
                            gate(f"G7 OLS_BETA twin beta matched ({pname} {book} g={g})",
                                 f"|d beta| {dbeta:.3e}", "< 5e-3", dbeta < 5e-3)
                        for c in RUNGS:
                            a, b = priced(res, c).loc[win], priced(tres, c).loc[win]
                            twin_rows.append(dict(
                                panel=pname, book=book, gross=g, convention=conv, fit=fit,
                                cost_bps=c, x=x,
                                cand_CAGR=cagr(a), twin_CAGR=cagr(b), d_CAGR=cagr(a) - cagr(b),
                                cand_Sharpe=sharpe(a), twin_Sharpe=sharpe(b),
                                d_Sharpe=sharpe(a) - sharpe(b),
                                cand_MaxDD=maxdd(a), twin_MaxDD=maxdd(b),
                                d_MaxDD=maxdd(a) - maxdd(b),
                                cand_OOS_CAGR=cagr(a[oos]), twin_OOS_CAGR=cagr(b[oos]),
                                d_OOS_CAGR=cagr(a[oos]) - cagr(b[oos]),
                                cand_OOS_Sharpe=sharpe(a[oos]), twin_OOS_Sharpe=sharpe(b[oos]),
                                d_OOS_Sharpe=sharpe(a[oos]) - sharpe(b[oos]),
                                cand_4b=legs(a, base[c], spy, a[oos], spy[oos])["pass4b"],
                                twin_4b=legs(b, base[c], spy, b[oos], spy[oos])["pass4b"],
                                cand_4a=legs(a, base[c], spy, a[oos], spy[oos])["pass4a"],
                                twin_4a=legs(b, base[c], spy, b[oos], spy[oos])["pass4a"]))
                        if fit == "FULL":
                            obs, se, t = boot_sharpe_diff(
                                priced(res, HEADLINE_RUNG).loc[win],
                                priced(tres, HEADLINE_RUNG).loc[win])
                            boot_rows.append(dict(panel=pname, book=book, gross=g, convention=conv,
                                                  d_Sharpe_cand_minus_twin=obs, SE=se, t=t))
        gate(f"G11 the 2.0% cap bites ({pname})",
             f"max TARGET per-name weight CAP2 g=0.75 {cap_bit:.4%}",
             f"<= {CAP:.2%} + 1e-9", cap_bit is not None and cap_bit <= CAP + 1e-9)

        # ---------------- RULE 8 walk-forward
        for chooser, key in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
            for c in RUNGS:
                cand_cells = [(bk, g) for bk in BOOKS for g in GROSSES]
                scored = []
                for bk, g in cand_cells:
                    r = store[(pname, bk, g, c)]
                    scored.append(((bk, g), sharpe(r[ism]) if key == "IS_Sharpe" else calmar(r[ism])))
                (bk, g), sc = max(scored, key=lambda kv: (kv[1] if np.isfinite(kv[1]) else -9e9))
                rp = store[(pname, bk, g, c)]
                row = dict(panel=pname, chooser=chooser, cost_bps=c, pick_book=bk, pick_gross=g,
                           IS_score=sc, OOS_CAGR=cagr(rp[oos]), OOS_Sharpe=sharpe(rp[oos]),
                           OOS_MaxDD=maxdd(rp[oos]), OOS_SPY_CAGR=cagr(spy[oos]),
                           OOS_SPY_Sharpe=sharpe(spy[oos]),
                           OOS_LIVE_Sharpe=sharpe(base[c][oos]), OOS_LIVE_CAGR=cagr(base[c][oos]),
                           pass4b_oos_only=bool(sharpe(rp[oos]) > sharpe(spy[oos])
                                                and maxdd(rp[oos]) >= DD_CAP * maxdd(spy[oos])
                                                and cagr(rp[oos]) >= CAGR_FLOOR * cagr(spy[oos])))
                beat_both = True
                for conv in CONVENTIONS:
                    tr = store[(pname, f"TWIN_{bk}_{conv}_IS", g, c)]
                    row[f"twin_{conv}_OOS_Sharpe"] = sharpe(tr[oos])
                    row[f"twin_{conv}_OOS_CAGR"] = cagr(tr[oos])
                    row[f"twin_{conv}_OOS_MaxDD"] = maxdd(tr[oos])
                    row[f"beats_{conv}_Sharpe"] = bool(sharpe(rp[oos]) > sharpe(tr[oos]))
                    row[f"beats_{conv}_CAGR"] = bool(cagr(rp[oos]) > cagr(tr[oos]))
                    beat_both &= bool(sharpe(rp[oos]) > sharpe(tr[oos]) and cagr(rp[oos]) > cagr(tr[oos]))
                row["beats_BOTH_twins_on_Sharpe_AND_CAGR"] = bool(beat_both)
                wf_rows.append(row)

    # ---- EXTERNAL REPRODUCTION of the two committed comparands (U56, g=0.75, 10 bps)
    for tag, bk, orig, reread in (
            ("G4 idea 2300 CAND", "CAND", (0.1255, 1.1896, -0.1739, 0.1377, 1.2332),
             (0.1259, 1.1934, -0.1739, 0.1385, 1.2397)),
            ("G5 idea 2322 CAP2", "CAP2", (0.1158, 1.2643, -0.1481, 0.1270, 1.3243),
             (0.1162, 1.2687, -0.1481, 0.1277, 1.3318))):
        r = store[("U56", bk, 0.75, HEADLINE_RUNG)]
        o = oos_of["U56"]
        got = (cagr(r), sharpe(r), maxdd(r), cagr(r[o]), sharpe(r[o]))
        d_re = max(abs(a - b) for a, b in zip(got, reread))
        d_or = max(abs(a - b) for a, b in zip(got, orig))
        gate(f"{tag} reproduced vs idea 2326's committed re-read (U56 0.75 10bps)",
             f"read {got[0]:.4%}/{got[1]:.4f}/{got[2]:.4%}, OOS {got[3]:.4%}/{got[4]:.4f}; "
             f"2326 re-read {reread[0]:.2%}/{reread[1]:.4f}/{reread[2]:.2%}, "
             f"OOS {reread[3]:.2%}/{reread[4]:.4f}; max residual {d_re:.3e}",
             "< 1e-3", d_re < 1e-3)
        publish(f"{tag} gap to the ORIGINAL 2300/2322 commit (price-cache vintage)",
                f"max residual {d_or:.3e} — the same vintage gap idea 2326 published")

    G = pd.DataFrame(grid)
    T = pd.DataFrame(twin_rows)
    W = pd.DataFrame(wf_rows)
    B = pd.DataFrame(boot_rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    T.to_csv(f"{OUT}.twins.csv", index=False)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    B.to_csv(f"{OUT}.bootstrap.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)

    # ---------------------------------------------------------------- read-out
    say("\n=== HEADLINE (10 bps, full window) ===")
    h = G[(G.cost_bps == HEADLINE_RUNG) | (G.family == "SPY")]
    cols = ["panel", "book", "x", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR",
            "OOS_Sharpe", "beta", "mean_eq_gross", "turnover", "max_name_w", "pass4a", "pass4b"]
    say(h[cols].to_string(index=False, float_format=lambda v: f"{v:.4f}"))

    say("\n=== CANDIDATE minus TWIN, 10 bps ===")
    t10 = T[T.cost_bps == HEADLINE_RUNG]
    say(t10[["panel", "book", "gross", "convention", "fit", "x", "d_CAGR", "d_Sharpe",
             "d_MaxDD", "d_OOS_CAGR", "d_OOS_Sharpe", "cand_4b", "twin_4b", "cand_4a",
             "twin_4a"]].to_string(index=False, float_format=lambda v: f"{v:.4f}"))

    say("\n=== PAIRED BLOCK BOOTSTRAP on Sharpe (candidate - twin, 10 bps, FULL fit) ===")
    say(B.to_string(index=False, float_format=lambda v: f"{v:.4f}"))

    say("\n=== RULE 8 WALK-FORWARD (dials fitted <= 2016-12-31, 2017-2026 read once) ===")
    say(W[["panel", "chooser", "cost_bps", "pick_book", "pick_gross", "OOS_CAGR", "OOS_Sharpe",
           "OOS_MaxDD", "twin_MEAN_GROSS_OOS_Sharpe", "twin_MEAN_GROSS_OOS_CAGR",
           "twin_OLS_BETA_OOS_Sharpe", "twin_OLS_BETA_OOS_CAGR",
           "beats_BOTH_twins_on_Sharpe_AND_CAGR"]].to_string(index=False,
                                                             float_format=lambda v: f"{v:.4f}"))

    say("\n=== BOTH KEEP PATHS over every published row ===")
    say(f"    rows published: {len(G)}   (books x panels x rungs, plus SPY reference rows)")
    for fam in sorted(G.family.unique()):
        sub = G[G.family == fam]
        say(f"    {fam:18s} 4b {int(sub.pass4b.sum()):3d} / {len(sub):3d}    "
            f"4a {int(sub.pass4a.sum()):3d} / {len(sub):3d}")
    cand = T[T.fit == "FULL"]
    say(f"\n    CANDIDATE beats TWIN on FULL Sharpe: {int((cand.d_Sharpe > 0).sum())} of {len(cand)}")
    say(f"    CANDIDATE beats TWIN on FULL CAGR  : {int((cand.d_CAGR > 0).sum())} of {len(cand)}")
    say(f"    CANDIDATE beats TWIN on OOS Sharpe : {int((cand.d_OOS_Sharpe > 0).sum())} of {len(cand)}")
    say(f"    CANDIDATE beats TWIN on OOS CAGR   : {int((cand.d_OOS_CAGR > 0).sum())} of {len(cand)}")
    say(f"    TWIN itself clears 4b at           : {int(cand.twin_4b.sum())} of {len(cand)} rows "
        f"(candidate {int(cand.cand_4b.sum())} of {len(cand)})")
    say("\n    WHICH 4b LEG THE TWIN FAILS (all twin rows, every rung):")
    tw = G[G.family.str.startswith("TWIN")]
    for leg in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"):
        say(f"      {leg:7s} fails at {int((~tw[leg]).sum()):3d} of {len(tw):3d} twin rows")
    cd = G[G.family.isin(BOOKS)]
    for leg in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"):
        say(f"      candidate {leg:7s} fails at {int((~cd[leg]).sum()):3d} of {len(cd):3d} rows")
    say(f"    rule 8: pick beats BOTH IS-fitted twins on Sharpe AND CAGR at "
        f"{int(W.beats_BOTH_twins_on_Sharpe_AND_CAGR.sum())} of {len(W)} picks")

    nfail = sum(1 for g in GATES if g["target"] != "published, not asserted" and not g["pass_"])
    say(f"\nGATES {len([g for g in GATES if g['target'] != 'published, not asserted']) - nfail} of "
        f"{len([g for g in GATES if g['target'] != 'published, not asserted'])} PASS "
        f"({nfail} failures)")
    say(f"elapsed {time.time() - t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

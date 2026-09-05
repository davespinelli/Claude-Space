#!/usr/bin/env python3
"""QUEUE idea 126 — execution-lag-sensitivity-of-the-whole-price-list (lane C, 2026-09-05).

Question (pre-registered, verbatim from QUEUE)
----------------------------------------------
"idea 96 found a per-name stop's drawdown price flips SIGN under a one-bar change of
execution lag (dMaxDD -0.69 pp at t+1, +2.44 pp at t+2) while its own instrument axis moves
it by 0.1-1.3 pp.  Re-price every instrument on idea 74/94's menu (200d gate, 3% band, abs
momentum, de-gross, book-level DD control, entry budget) at lags t+1 / t+2 / next-rebalance
and report which prices are lag-stable.  If the slow instruments are stable and only the fast
ones are not, PROTOCOL can quote a speed threshold; if none are, no price on the menu is
quotable.  Max 2 params."

What is being audited.  Every drawdown "price" this project publishes has the form

    rate = (CAGR_ctl - CAGR_arm) / (|MaxDD_ctl| - |MaxDD_arm|)     pp CAGR per pp MaxDD

computed under ONE execution convention: decide at close t, trade at close t+1 (PROTOCOL
rule 2).  Idea 96 found that for a per-name stop the denominator of that ratio changes SIGN
when the convention moves by a single bar.  A price whose sign depends on a convention that
was never part of the claim is not a price.  This run puts the WHOLE menu — every instrument
idea 94 published — on the lag axis and asks which entries survive it.

THE LAG AXIS (the only thing that changes; everything else is idea 94's, unchanged)
    L1  "t+1"   decide at close t, execute at close t+1.   <- PROTOCOL rule 2, the published one
    L2  "t+2"   decide at close t, execute at close t+2.
    NR  "nr"    decide at rebalance date d, execute at the execution bar of rebalance d+1
                (i.e. nothing moves faster than the rebalance cadence: the same delay is
                applied to scheduled trades, to stop exits and to DD-control de-grossing).
    The lag is applied to EVERY moving part of an arm: the target book, the gate, the
    per-name stop exit, the book-level DD control's own state reading, and the entry budget.
    At L1 the simulator is asserted to reproduce idea 94's `run` to machine precision, so
    this is an audit of that file's numbers and not a re-derivation of them.

LAG-STABILITY (pre-registered before any number below was read)
    For a published row (universe, book, cost, arm) with denominators d_L = dMaxDD at lag L
    and rates r_L:
      SIGN-STABLE(floor)  d_L > floor for ALL THREE lags       (the denominator is measurable)
      RATE-STABLE(tol)    sign-stable AND every r_L finite AND
                          max_L |r_L - r_L1| <= tol * |r_L1|   (the quoted number is the price)
      LAG-STABLE          = RATE-STABLE.  A row that is not lag-stable is NOT QUOTABLE: the
                          honest report is the (dCAGR, dMaxDD) pair plus its lag swing.

Tuned parameters (PROTOCOL rule 4).  TWO, both of the TEST and neither of any trading rule:
    floor  denominator floor in pp, in {0.10, 0.50, 1.00}   (0.10 is idea 94's own floor)
    tol    relative rate tolerance, in {0.25, 0.50, 1.00}
All 9 grid points reported.  (floor=0.10, tol=0.50) is the pre-registered headline: idea 94's
floor unchanged, and a tolerance that lets a quoted price move by half of itself before it is
called unstable — a deliberately GENEROUS bar, so a failure here is not a bar-setting artefact.
No trading parameter is tuned anywhere in this run.

Speed axis (the queue's "if the slow instruments are stable and only the fast ones are not").
Each arm carries a speed measured at L1: dTO = its annual turnover minus the control's, and
its instrument-native trigger count (gate flips per ticker per year, stops per year, DD
episodes per year, budget-binding rebalances per year).  The report regresses lag instability
on dTO (Spearman) and states whether a speed threshold separates stable from unstable rows.

Walk-forward (PROTOCOL rule 8), fixed before any OOS number was read
    S1  idea 94's own selector, unchanged: in each (universe, book, cost) cell, among arms
        that bought >= 1.0 pp of IS MaxDD at L1, pick the LOWEST IS rate.  Evaluate untouched
        on 2017-2026 AT ALL THREE LAGS.
    S2  the same selector restricted to arms that are LAG-STABLE on 2009-2016 DATA ONLY
        (IS-window denominators and rates across the three lags).  The OOS window is never
        consulted by the screen.
    Both report OOS CAGR / Sharpe / MaxDD against the cell's own control, against live
    RULES v1 (re-run at the same lag) and against SPY, and both KEEP paths (4a and 4b) are
    evaluated for every arm at every lag, so a verdict that flips with the lag is visible.

Pre-registered predictions (written before any number was read)
    P1  The lag axis moves dMaxDD by MORE than the instrument axis does (idea 96's finding
        generalises): median |lag swing| > median instrument-family spread.
    P2  FEWER THAN HALF of idea 94's published rates are lag-stable at (0.10, 0.50).
    P3  Instability concentrates in the FAST arms (stops, 200d gate) and the 5-name V1u book;
        the slow arms (band3, ebud) and the 56-name EWall book are the stable ones.
    P4  The lag axis does not manufacture a KEEP: no S1 or S2 pick passes 4b at any lag.

Execution realism (PROTOCOL rule 2): 10 bps per unit turnover charged inside the loop so both
state machines read NET equity, long-only, no leverage, weekly cadence.  L1 IS rule 2; L2 and
NR are the perturbation, reported as such and never as a proposed convention.

SURVIVORSHIP: universe.json and universe_broad.json are current-constituent lists, so every
absolute level is optimistic.  This run reports within-cell differences and the STABILITY of a
sign, which are far less exposed than levels — but a survivorship-free panel could still move
which rows pass.

Deterministic, standalone.  Imports research/baseline.py and idea 94's script; modifies nothing.
"""
import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))

from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

BT = ROOT / "research" / "backtests"
_s94 = importlib.util.spec_from_file_location(
    "i94", BT / "2026-09-04_drawdown-insurance-price-list_B.py")
H = importlib.util.module_from_spec(_s94)
_s94.loader.exec_module(H)

STEM = Path(__file__).stem
OUT = BT / STEM

FREQ, PCOST = H.FREQ, H.PCOST
COSTS = list(H.COSTS)                      # [10, 25] — the rungs idea 94 published
BOOKS = list(H.BOOKS)                      # V1u, TOP20, EWall
ARMS = [a for a in H.arm_specs() if a[0] != "control"]
UNIS = [("universe.json(56)", dict()), ("universe_broad.json", dict(broad=True))]
LAGS = ["t+1", "t+2", "nr"]
IS_END, OOS_START = H.IS_END, H.OOS_START
FLOORS, TOLS = (0.10, 0.50, 1.00), (0.25, 0.50, 1.00)
FLOOR_STAR, TOL_STAR = 0.10, 0.50          # pre-registered headline point

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 70)
pd.set_option("display.max_rows", 4000)


# ---------------------------------------------------------------- lagged simulator
def exec_schedule(index, freq, lag):
    """(exec_flag, dec_i, next_exec) for a lag convention.

    exec_flag[i]  a scheduled rebalance executes at bar i
    dec_i[i]      the row index whose close supplied the decision executed at bar i
                  (target weights AND the DD control's equity reading)
    next_exec[i]  the first execution bar strictly after i (used by NR to delay stop exits
                  to the next scheduled rebalance); -1 if none.
    """
    D = rebalance_mask(index, freq).values
    n = len(index)
    exec_flag = np.zeros(n, dtype=bool)
    dec_i = np.full(n, -1, dtype=int)
    if lag in ("t+1", "t+2"):
        k = 1 if lag == "t+1" else 2
        for i in range(n):
            j = i - k
            if j >= 0 and D[j]:
                exec_flag[i], dec_i[i] = True, j
    elif lag == "nr":
        reb = np.flatnonzero(D)
        for t_, j in enumerate(reb):
            if t_ == 0:
                continue                       # no previous decision to execute yet
            i = j + 1                          # the normal execution bar of rebalance j
            if i < n:
                exec_flag[i], dec_i[i] = True, reb[t_ - 1]
    else:
        raise ValueError(lag)
    next_exec = np.full(n, -1, dtype=int)
    nxt = -1
    for i in range(n - 1, -1, -1):
        next_exec[i] = nxt
        if exec_flag[i]:
            nxt = i
    return exec_flag, dec_i, next_exec


def run_lag(px, W, lag="t+1", m=1.0, stop=None, D=None, k=1.0, reset="recover",
            ebud=None, bps=PCOST, freq=FREQ):
    """idea 94's `run` with the execution convention as a parameter.

    lag='t+1' reproduces it to machine precision (asserted in main()).  Everything else —
    cost accounting, drift, the order of operations inside a bar — is unchanged.
    """
    pxv = px.values
    rets = px.pct_change().fillna(0.0).values
    tgt = (W.reindex(px.index).fillna(0.0) * m).values
    exec_flag, dec_i, next_exec = exec_schedule(px.index, freq, lag)
    nrow, ncol = rets.shape

    cur = np.zeros(ncol)
    peak_p = np.full(ncol, np.nan)
    pend = np.full(ncol, -1, dtype=int)        # per-name bar index at which a stop exit executes
    held = np.zeros((nrow, ncol))
    turn = np.zeros(nrow)
    gross_s = np.zeros(nrow)
    cut = np.zeros(nrow, dtype=bool)
    eq_h = np.ones(nrow)
    pk_h = np.ones(nrow)
    eq, pk, armed, episodes, n_stops, n_bind = 1.0, 1.0, False, 0, 0, 0

    for i in range(nrow):
        due = pend == i                        # 1. stop exits whose delay has elapsed
        if due.any():
            turn[i] += cur[due].sum()
            cur = np.where(due, 0.0, cur)
            pend = np.where(due, -1, pend)
        if exec_flag[i]:                       # 2. scheduled rebalance, decided at dec_i[i]
            j = dec_i[i]
            if D is not None:
                dd = eq_h[j] / pk_h[j] - 1.0   # equity through the DECISION close: no look-ahead
                if not armed and dd < -D:
                    armed, episodes = True, episodes + 1
                elif armed and (dd >= 0.0 if reset == "high" else dd > -D / 2.0):
                    armed = False
            new = tgt[j] * (k if armed else 1.0)
            s = new.sum()
            if s > 1.0:
                new = new / s
            if ebud is not None:               # 3. entry-only budget: exits are free
                d = new - cur
                up = np.clip(d, 0.0, None).sum()
                if up > ebud:
                    new = cur + np.clip(d, None, 0.0) + np.clip(d, 0.0, None) * (ebud / up)
                    n_bind += 1
            turn[i] += np.abs(new - cur).sum()
            cur = new
        cut[i] = armed
        held[i] = cur
        gross_s[i] = cur.sum()
        rp = float((cur * rets[i]).sum()) - turn[i] * bps / 1e4
        eq *= (1.0 + rp)
        pk = max(pk, eq)
        eq_h[i], pk_h[i] = eq, pk
        growth = cur * (1 + rets[i])           # 4. drift
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
        if stop is not None:                   # 5. trailing highs / fire stops
            alive = cur > 1e-9
            p = pxv[i]
            peak_p = np.where(alive, np.fmax(np.where(np.isnan(peak_p), -np.inf, peak_p), p), np.nan)
            hit = alive & np.isfinite(p) & (p < peak_p * (1 - stop)) & (pend < 0)
            if hit.any():
                if lag == "nr":
                    e = next_exec[i]
                    if e >= 0:
                        pend = np.where(hit, e, pend)
                        n_stops += int(hit.sum())
                else:
                    e = i + (1 if lag == "t+1" else 2)
                    if e < nrow:
                        pend = np.where(hit, e, pend)
                        n_stops += int(hit.sum())

    r = pd.Series((held * rets).sum(axis=1), index=px.index) \
        - pd.Series(turn, index=px.index) * bps / 1e4
    return dict(r=r, to=pd.Series(turn, index=px.index), gross=pd.Series(gross_s, index=px.index),
                cut=pd.Series(cut, index=px.index), episodes=episodes, n_stops=n_stops,
                n_bind=n_bind)


# ---------------------------------------------------------------- native instrument speed
def native_speed(px, name, kind, kwargs, gate, years, res):
    """Instrument-native trigger rate, per year (units differ by family — reported, not pooled)."""
    if kind == "gate":
        g = H.gate_mask(px, gate)
        flips = (g.astype(int).diff().abs().sum().sum())
        return float(flips / years / px.shape[1]), "gateflips/tkr/yr"
    if kind == "stop":
        return float(res["n_stops"] / years), "stops/yr"
    if kind == "dd":
        return float(res["episodes"] / years), "ddepisodes/yr"
    if kind == "bud":
        return float(res["n_bind"] / years), "budgetbinds/yr"
    return np.nan, "-"


# ---------------------------------------------------------------- one universe
def do_universe(uname, kw):
    px = load_universe(**kw)
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    bars = H.bars_of(spy)
    ms = metrics(spy)

    print("\n" + "=" * 220)
    print(f"UNIVERSE {uname}: {px.shape[1]} names, {px.index[0].date()} -> {px.index[-1].date()}"
          f" | eval {start.date()} -> {px.index[-1].date()} | IS <= {IS_END} | OOS >= {OOS_START}")
    print(f"SPY  CAGR {ms['CAGR']:.2%}  Sharpe {ms['Sharpe']:.3f}  MaxDD {ms['MaxDD']:.2%}  "
          f"halves {bars['s1']:.3f}/{bars['s2']:.3f}  OOS Sharpe {bars['soos']:.3f}")
    print(f"4b bars: Sharpe > {bars['s1']:.3f}(H1)/{bars['s2']:.3f}(H2)/{bars['soos']:.3f}(OOS), "
          f"MaxDD <= {0.60*abs(ms['MaxDD']):.2%}, CAGR >= {0.70*ms['CAGR']:.2%}")
    print("=" * 220)

    # ---- harness sanity 1: lag='t+1' must reproduce idea 94's run() exactly
    worst_l1 = 0.0
    for b in BOOKS:
        for nm, kind, kwargs, (g, conv) in H.arm_specs():
            W = H.targets(px, b, g, conv)
            a = run_lag(px, W, lag="t+1", bps=PCOST, **kwargs)["r"].loc[start:]
            e = H.run(px, W, bps=PCOST, **kwargs)["r"].loc[start:]
            worst_l1 = max(worst_l1, float((a - e).abs().max()))
    print(f"HARNESS 1 — run_lag(t+1) vs idea 94 run(): max|diff| over {len(BOOKS)*len(H.arm_specs())} "
          f"arm-points = {worst_l1:.3e} ({'EXACT' if worst_l1 < 1e-12 else 'NOT EXACT — UNSAFE'})")
    # ---- harness sanity 2: control at t+1 must reproduce engine.backtest exactly
    worst_e = 0.0
    for b in BOOKS:
        W = H.targets(px, b)
        a = run_lag(px, W, lag="t+1", bps=PCOST)["r"].loc[start:]
        e = backtest(px, W, cost_bps=PCOST, freq=FREQ)["returns"].loc[start:]
        worst_e = max(worst_e, float((a - e).abs().max()))
    print(f"HARNESS 2 — control(t+1) vs engine.backtest: max|diff| = {worst_e:.3e} "
          f"({'EXACT' if worst_e < 1e-12 else 'NOT EXACT — UNSAFE'})")
    assert worst_l1 < 1e-12 and worst_e < 1e-12, "lag harness does not reproduce the published one"

    # ---- live RULES v1 at each lag (the 4a comparator, re-run under the same convention)
    v1 = {}
    for lag in LAGS:
        for c in COSTS:
            v1[(lag, c)] = run_lag(px, rules_v1_weights(px), lag=lag, bps=c)["r"].loc[start:]
    d1 = float((v1[("t+1", 10.0)] - backtest(px, rules_v1_weights(px), cost_bps=10.0,
                                             freq=FREQ)["returns"].loc[start:]).abs().max())
    print(f"HARNESS 3 — RULES v1(t+1) vs engine.backtest: max|diff| = {d1:.3e}")

    rows, rets, ladders, speeds = [], {}, {}, {}
    years = metrics(spy)["Years"]
    for b in BOOKS:
        for lag in LAGS:
            for c in COSTS:
                lad = []
                for m_ in H.LADDER:
                    res = run_lag(px, H.targets(px, b), lag=lag, m=m_, bps=c)
                    r = res["r"].loc[start:]
                    mm = metrics(r)
                    lad.append(dict(m=m_, CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                                    IS_CAGR=metrics(r.loc[:IS_END])["CAGR"],
                                    IS_MaxDD=metrics(r.loc[:IS_END])["MaxDD"],
                                    OOS_CAGR=metrics(r.loc[OOS_START:])["CAGR"],
                                    OOS_MaxDD=metrics(r.loc[OOS_START:])["MaxDD"]))
                ladders[(b, c, lag)] = pd.DataFrame(lad)

                for name, kind, kwargs, (g, conv) in H.arm_specs():
                    W = H.targets(px, b, g, conv)
                    res = run_lag(px, W, lag=lag, bps=c, **kwargs)
                    r = res["r"].loc[start:]
                    rets[(b, name, c, lag)] = r
                    mm = metrics(r)
                    mg = H.margins(r, bars)
                    h1, h2 = H.halves(r)
                    mo, mi = metrics(r.loc[OOS_START:]), metrics(r.loc[:IS_END])
                    to = res["to"].loc[start:].sum() / mm["Years"]
                    if lag == "t+1" and c == PCOST:
                        sp, unit = native_speed(px, name, kind, kwargs, g, years, res)
                        speeds[(b, name)] = (to, sp, unit)
                    rows.append(dict(
                        uni=uname, book=b, arm=name, kind=kind, cost=c, lag=lag,
                        CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                        IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
                        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                        TO=to, gross=res["gross"].loc[start:].mean(),
                        p4a=H.pass4a(r, v1[(lag, c)]),
                        p4b=all(v > 0 for v in mg.values()),
                        f4b=",".join([kk for kk, v in mg.items() if not v > 0]) or "-"))
    df = pd.DataFrame(rows)
    return px, start, df, rets, ladders, bars, spy, v1, speeds


# ---------------------------------------------------------------- the lagged price list
def price_list(uname, rets, ladders):
    out = []
    for b in BOOKS:
        for c in COSTS:
            for lag in LAGS:
                L = ladders[(b, c, lag)]
                slope = {w: H.ladder_slope(L, f"{p}MaxDD", f"{p}CAGR")
                         for w, p in (("full", ""), ("IS", "IS_"), ("OOS", "OOS_"))}
                rc = rets[(b, "control", c, lag)]
                for name, kind, _, _ in ARMS:
                    ra = rets[(b, name, c, lag)]
                    p_f = H.price(rc, ra, slope["full"])
                    p_i = H.price(H.window(rc, "IS"), H.window(ra, "IS"), slope["IS"])
                    p_o = H.price(H.window(rc, "OOS"), H.window(ra, "OOS"), slope["OOS"])
                    out.append(dict(
                        uni=uname, book=b, cost=c, arm=name, kind=kind, lag=lag,
                        dCAGR=p_f["dCAGR"], dMaxDD=p_f["dMaxDD"], rate=p_f["rate"],
                        dSharpe=p_f["dSharpe"], lever=slope["full"],
                        IS_dCAGR=p_i["dCAGR"], IS_dMaxDD=p_i["dMaxDD"], IS_rate=p_i["rate"],
                        OOS_dCAGR=p_o["dCAGR"], OOS_dMaxDD=p_o["dMaxDD"], OOS_rate=p_o["rate"]))
    return pd.DataFrame(out)


def stability(P, floor, tol, win=""):
    """One row per published (uni, book, cost, arm): the three lags collapsed into a verdict."""
    dcol, rcol = f"{win}dMaxDD", f"{win}rate"
    out = []
    for keys, g in P.groupby(["uni", "book", "cost", "arm", "kind"], sort=False):
        g = g.set_index("lag")
        d = {l: float(g.loc[l, dcol]) for l in LAGS}
        r = {l: float(g.loc[l, rcol]) for l in LAGS}
        sign_ok = all(d[l] > floor for l in LAGS)
        r1 = r["t+1"]
        fin = all(np.isfinite(r[l]) for l in LAGS) and np.isfinite(r1) and abs(r1) > 0
        swing_r = (max(r.values()) - min(r.values())) if fin else np.nan
        rel = (max(abs(r[l] - r1) for l in LAGS) / abs(r1)) if fin else np.inf
        out.append(dict(uni=keys[0], book=keys[1], cost=keys[2], arm=keys[3], kind=keys[4],
                        d_t1=d["t+1"], d_t2=d["t+2"], d_nr=d["nr"],
                        d_swing=max(d.values()) - min(d.values()),
                        sign_flip=(min(d.values()) <= 0 < max(d.values())),
                        r_t1=r["t+1"], r_t2=r["t+2"], r_nr=r["nr"], r_swing=swing_r, rel=rel,
                        published=np.isfinite(r1) and d["t+1"] > 0.10,
                        sign_stable=sign_ok, lag_stable=bool(sign_ok and fin and rel <= tol)))
    return pd.DataFrame(out)


# ---------------------------------------------------------------- rule 8
def walk_forward(uname, P, df, rets, bars, spy, v1, S_is):
    """S1 = idea 94's selector at L1.  S2 = the same restricted to IS-lag-stable denominators.
    Both evaluated untouched on OOS AT ALL THREE LAGS."""
    spy_o = metrics(spy.loc[OOS_START:])
    out = []
    for b in BOOKS:
        for c in COSTS:
            cell = P[(P.book == b) & (P.cost == c) & (P.lag == "t+1")]
            stab = S_is[(S_is.book == b) & (S_is.cost == c)].set_index("arm").lag_stable.to_dict()
            base = cell[(cell.IS_dMaxDD >= 1.0) & np.isfinite(cell.IS_rate)]
            for sel, elig in (("S1 idea94", base),
                              ("S2 lag-screened", base[base.arm.map(stab).fillna(False)])):
                if elig.empty:
                    out.append(dict(uni=uname, book=b, cost=c, selector=sel,
                                    pick="NOTHING (no eligible arm)", lag="-", **{k: np.nan for k in
                                    ("IS_rate", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "OOS_dMaxDD",
                                     "ctl_Sharpe", "v1_Sharpe", "spy_Sharpe")},
                                    p4a=False, p4b=False))
                    continue
                pick = elig.sort_values("IS_rate").iloc[0]
                for lag in LAGS:
                    ro = rets[(b, pick.arm, c, lag)].loc[OOS_START:]
                    rc = rets[(b, "control", c, lag)].loc[OOS_START:]
                    mo, mc = metrics(ro), metrics(rc)
                    row = df[(df.book == b) & (df.arm == pick.arm) & (df.cost == c)
                             & (df.lag == lag)].iloc[0]
                    out.append(dict(
                        uni=uname, book=b, cost=c, selector=sel, pick=pick.arm, lag=lag,
                        IS_rate=pick.IS_rate, OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                        OOS_MaxDD=mo["MaxDD"],
                        OOS_dMaxDD=(abs(mc["MaxDD"]) - abs(mo["MaxDD"])) * 100.0,
                        ctl_Sharpe=mc["Sharpe"],
                        v1_Sharpe=metrics(v1[(lag, c)].loc[OOS_START:])["Sharpe"],
                        spy_Sharpe=spy_o["Sharpe"], p4a=bool(row.p4a), p4b=bool(row.p4b)))
    return pd.DataFrame(out)


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    print(__doc__)
    allP, allS, allW, allD, allSpeed = [], [], [], [], []
    for uname, kw in UNIS:
        px, start, df, rets, ladders, bars, spy, v1, speeds = do_universe(uname, kw)
        P = price_list(uname, rets, ladders)
        allP.append(P)
        allD.append(df)

        print(f"\nFULL GRID {uname} — {len(df)} arm-points, ALL REPORTED "
              f"({len(BOOKS)} books x {len(H.arm_specs())} arms x {len(COSTS)} costs x {len(LAGS)} lags)")
        print(df[["book", "arm", "cost", "lag", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                  "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "TO", "gross", "p4a", "p4b", "f4b"]]
              .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

        print(f"\nPRICE LIST BY LAG {uname} — {len(P)} rows, ALL REPORTED "
              f"(rate = pp CAGR surrendered per pp MaxDD bought, vs the same-lag control)")
        print(P[["book", "cost", "arm", "lag", "dCAGR", "dMaxDD", "rate", "dSharpe",
                 "IS_dMaxDD", "IS_rate", "OOS_dMaxDD", "OOS_rate"]]
              .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

        S = stability(P, FLOOR_STAR, TOL_STAR)
        sp = pd.DataFrame([dict(uni=uname, book=b, arm=a, dTO=v[0] - speeds[(b, "control")][0],
                                native=v[1], unit=v[2]) for (b, a), v in speeds.items()
                           if a != "control"])
        S = S.merge(sp, on=["uni", "book", "arm"], how="left")
        allS.append(S)
        allSpeed.append(sp)

        print(f"\nLAG-STABILITY {uname} at the pre-registered headline (floor={FLOOR_STAR} pp, "
              f"tol={TOL_STAR}) — {len(S)} published rows, ALL REPORTED")
        print(S[["book", "cost", "arm", "kind", "d_t1", "d_t2", "d_nr", "d_swing", "sign_flip",
                 "r_t1", "r_t2", "r_nr", "rel", "published", "sign_stable", "lag_stable",
                 "dTO", "native", "unit"]]
              .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

        S_is = stability(P, FLOOR_STAR, TOL_STAR, win="IS_")
        W = walk_forward(uname, P, df, rets, bars, spy, v1, S_is)
        allW.append(W)
        print(f"\nRULE 8 WALK-FORWARD {uname} — instrument chosen on 2009-{IS_END[:4]} only "
              f"(at the published lag t+1), evaluated untouched on {OOS_START[:4]}-2026 at all lags")
        print(W.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
        print(f"[{time.time()-t0:.0f}s]")

    P = pd.concat(allP, ignore_index=True)
    S = pd.concat(allS, ignore_index=True)
    W = pd.concat(allW, ignore_index=True)
    D = pd.concat(allD, ignore_index=True)
    P.to_csv(f"{OUT}.pricelist.csv", index=False)
    S.to_csv(f"{OUT}.stability.csv", index=False)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    D.to_csv(f"{OUT}.grid.csv", index=False)

    # ------------------------------------------------------------ the 9-point parameter grid
    print("\n" + "=" * 220)
    print("PARAMETER GRID (the only two tuned numbers in this run, both of the TEST) — ALL 9 POINTS")
    grid = []
    for fl in FLOORS:
        for to in TOLS:
            s = stability(P, fl, to)
            pub = s[s.published]
            grid.append(dict(floor=fl, tol=to, published=int(pub.shape[0]),
                             sign_stable=int(pub.sign_stable.sum()),
                             lag_stable=int(pub.lag_stable.sum()),
                             pct_lag_stable=100.0 * pub.lag_stable.mean(),
                             sign_flips=int(pub.sign_flip.sum())))
    G = pd.DataFrame(grid)
    G.to_csv(f"{OUT}.paramgrid.csv", index=False)
    print(G.to_string(index=False, float_format=lambda x: f"{x:.1f}"))
    print(f"headline = (floor={FLOOR_STAR}, tol={TOL_STAR})")

    S = stability(P, FLOOR_STAR, TOL_STAR).merge(
        pd.concat(allSpeed, ignore_index=True), on=["uni", "book", "arm"], how="left")
    pub = S[S.published]

    # ------------------------------------------------------------ P1: which axis moves it more
    print("\nP1 — LAG AXIS vs INSTRUMENT AXIS (pp of dMaxDD)")
    inst = []
    for (u, b, c, lag), g in P.groupby(["uni", "book", "cost", "lag"]):
        for kind, gg in g.groupby("kind"):
            if len(gg) > 1:
                inst.append(dict(uni=u, book=b, cost=c, lag=lag, kind=kind,
                                 spread=gg.dMaxDD.max() - gg.dMaxDD.min()))
    I = pd.DataFrame(inst)
    print(f"  lag swing of dMaxDD  : median {pub.d_swing.median():.3f} pp, "
          f"mean {pub.d_swing.mean():.3f}, p90 {pub.d_swing.quantile(0.9):.3f}, max {pub.d_swing.max():.3f}")
    print(f"  instrument-family spread of dMaxDD (within kind, fixed lag): "
          f"median {I.spread.median():.3f} pp, mean {I.spread.mean():.3f}, max {I.spread.max():.3f}")
    print("  by family (median lag swing vs median within-family spread):")
    print(pd.DataFrame({"lag_swing": pub.groupby("kind").d_swing.median(),
                        "family_spread": I.groupby("kind").spread.median()})
          .to_string(float_format=lambda x: f"{x:.3f}"))
    print(f"  P1 {'CONFIRMED' if pub.d_swing.median() > I.spread.median() else 'REFUTED'}")

    # ------------------------------------------------------------ P2: how many prices survive
    print("\nP2 — HOW MANY OF IDEA 94's PUBLISHED PRICES ARE LAG-STABLE")
    print(f"  published rows (finite rate at t+1, dMaxDD > 0.10 pp): {len(pub)} of {len(S)}")
    print(f"  sign-stable across the three lags : {int(pub.sign_stable.sum())} "
          f"({100*pub.sign_stable.mean():.1f}%)")
    print(f"  lag-stable (sign + rate within {TOL_STAR:.0%}) : {int(pub.lag_stable.sum())} "
          f"({100*pub.lag_stable.mean():.1f}%)")
    print(f"  denominators that FLIP SIGN across the lags : {int(pub.sign_flip.sum())}")
    print(f"  P2 {'CONFIRMED' if pub.lag_stable.mean() < 0.5 else 'REFUTED'}")
    for by in ("uni", "book", "kind", "cost"):
        print(f"\n  lag-stable rate by {by}:")
        print(pub.groupby(by).agg(n=("lag_stable", "size"), stable=("lag_stable", "sum"),
                                  pct=("lag_stable", lambda s: 100 * s.mean()),
                                  med_swing=("d_swing", "median"))
              .to_string(float_format=lambda x: f"{x:.1f}"))

    # ------------------------------------------------------------ P3: is there a speed threshold
    print("\nP3 — IS THERE A SPEED THRESHOLD?  (dTO = arm turnover/yr minus control's, at t+1/10bps)")
    print(pub.groupby("arm").agg(n=("lag_stable", "size"), stable=("lag_stable", "sum"),
                                 pct=("lag_stable", lambda s: 100 * s.mean()),
                                 dTO=("dTO", "median"), native=("native", "median"),
                                 med_swing=("d_swing", "median"), flips=("sign_flip", "sum"))
          .sort_values("dTO").to_string(float_format=lambda x: f"{x:.2f}"))
    rho_s = H.spearman(pub.dTO.values, pub.d_swing.values)
    rho_st = H.spearman(pub.dTO.values, pub.lag_stable.astype(float).values)
    print(f"  Spearman(dTO, lag swing of dMaxDD) = {rho_s:.3f}   "
          f"Spearman(dTO, lag_stable) = {rho_st:.3f}")
    gt = pub[pub.kind == "gate"]                 # the one family whose native speeds share units
    print(f"  within the GATE family only (native = gate flips/ticker/yr, n={len(gt)}): "
          f"Spearman(native, lag swing) = {H.spearman(gt.native.values, gt.d_swing.values):.3f}, "
          f"Spearman(native, lag_stable) = "
          f"{H.spearman(gt.native.values, gt.lag_stable.astype(float).values):.3f}")
    print(gt.groupby("arm").agg(n=("lag_stable", "size"), stable=("lag_stable", "sum"),
                                native=("native", "median"), med_swing=("d_swing", "median"))
          .sort_values("native").to_string(float_format=lambda x: f"{x:.2f}"))
    print("\n  how many of the 192 menu rows were PRICEABLE at t+1 at all, by family:")
    print(S.groupby("kind").published.agg(rows="size", published="sum").to_string())
    print(f"  median published price moves {100*pub.rel.median():.0f}% of its own value across "
          f"the three lags (median absolute rate swing {pub.r_swing.median():.3f} pp/pp)")
    if pub.lag_stable.any():
        print(f"  fastest dTO among LAG-STABLE rows   : {pub[pub.lag_stable].dTO.max():.2f}/yr")
        print(f"  slowest dTO among UNSTABLE rows     : {pub[~pub.lag_stable].dTO.min():.2f}/yr")
        sep = pub[pub.lag_stable].dTO.max() < pub[~pub.lag_stable].dTO.min()
        print(f"  a clean speed threshold {'EXISTS' if sep else 'DOES NOT EXIST'} "
              f"(the two dTO ranges {'do not' if sep else 'do'} overlap)")
    else:
        print("  no lag-stable row: no threshold to quote")

    # ------------------------------------------------------------ verdict stability
    print("\nKEEP-PATH VERDICT STABILITY UNDER THE LAG (both paths, every arm)")
    Dv = D.assign(p4a=D.p4a.astype(int), p4b=D.p4b.astype(int))
    v = Dv.pivot_table(index=["uni", "book", "arm", "cost"], columns="lag",
                       values=["p4a", "p4b"], aggfunc="first")
    for path in ("p4a", "p4b"):
        x = v[path]
        flip = (x.nunique(axis=1) > 1)
        print(f"  {path}: passes at t+1 = {int(x['t+1'].sum())}, t+2 = {int(x['t+2'].sum())}, "
              f"nr = {int(x['nr'].sum())} of {len(x)} rows; verdict FLIPS with the lag in "
              f"{int(flip.sum())} rows")
        if flip.any():
            print(x[flip].to_string())

    # ------------------------------------------------------------ P4: rule 8
    print("\nP4 — RULE 8: DOES THE LAG (OR THE LAG SCREEN) MANUFACTURE A KEEP?")
    print(W.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    picks = W[W.lag != "-"]
    print(f"\n  4b passes among selector picks, any lag : {int(picks.p4b.sum())} of {len(picks)}")
    print(f"  4a passes among selector picks, any lag : {int(picks.p4a.sum())} of {len(picks)}")
    print(f"  P4 {'CONFIRMED' if picks.p4b.sum() == 0 else 'REFUTED'}")
    for path in ("p4b", "p4a"):
        gg = picks.groupby(["uni", "book", "cost", "selector", "pick"])[path].agg(["sum", "size"])
        print(f"  {path} of the {len(gg)} distinct selector picks: passes at ALL THREE lags "
              f"{int((gg['sum'] == 3).sum())}, at only 1-2 lags (verdict is a convention artefact) "
              f"{int(((gg['sum'] > 0) & (gg['sum'] < 3)).sum())}, never {int((gg['sum'] == 0).sum())}")
    for sel, g in picks.groupby("selector"):
        print(f"\n  {sel}: mean OOS Sharpe by lag")
        print(g.groupby("lag").agg(n=("OOS_Sharpe", "size"), OOS_Sharpe=("OOS_Sharpe", "mean"),
                                   OOS_CAGR=("OOS_CAGR", "mean"), OOS_MaxDD=("OOS_MaxDD", "mean"),
                                   OOS_dMaxDD=("OOS_dMaxDD", "mean"),
                                   ctl_Sharpe=("ctl_Sharpe", "mean"),
                                   v1_Sharpe=("v1_Sharpe", "mean"),
                                   spy_Sharpe=("spy_Sharpe", "mean"))
              .to_string(float_format=lambda x: f"{x:.3f}"))
    print("\n  OOS purchase (dMaxDD vs same-lag control) of the selected arm, by lag — "
          "does the OOS purchase survive the convention?")
    pv = picks.pivot_table(index=["uni", "book", "cost", "selector", "pick"], columns="lag",
                           values="OOS_dMaxDD", aggfunc="first")
    print(pv.to_string(float_format=lambda x: f"{x:.2f}"))
    neg = (pv < 0).any(axis=1) & (pv > 0).any(axis=1)
    print(f"  selector picks whose OOS purchase FLIPS SIGN across the lags: {int(neg.sum())} of {len(pv)}")
    print(f"\nwrote {OUT.name}.{{pricelist,stability,walkforward,grid,paramgrid}}.csv "
          f"[{time.time()-t0:.0f}s]")


if __name__ == "__main__":
    main()

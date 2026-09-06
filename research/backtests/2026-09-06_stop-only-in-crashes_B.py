#!/usr/bin/env python3
"""QUEUE idea 75 — stop-only-in-crashes (lane B, 2026-09-06).

Question (pre-registered)
-------------------------
Idea 9 / 94 found the per-name 15% trailing stop loses on average, and idea 96 showed
that under the protocol-conformant execution convention it buys NEGATIVE drawdown in
12 of 12 cells: it is the dearest instrument the project owns.  The queue's remaining
defence of it is that its damage is WHIPSAW — it costs money in trending markets and
earns its keep in crashes (idea 9's own year cuts: its 2020 numbers are its worst, its
2022 numbers its best).  If that is true, a stop that is ARMED ONLY IN A CRASH REGIME
and disarmed otherwise should recover the Sharpe the always-on stop gives up while
keeping whatever drawdown protection the stop has.

Pre-registered question: does conditional arming recover the Sharpe the always-on stop
gives up?  Two things must both happen for a YES:
  H1  dSharpe(armed stop) > dSharpe(always-on stop) in a majority of cells, and
  H2  the armed stop's drawdown is PRICEABLE — it buys drawdown (dMaxDD > 0) at a
      CAGR cost no worse than the same book's static-gross lever (idea 66), which is
      the control every drawdown claim in this project has to clear.
The project's prior is against it: idea 6 KILLED a breadth-triggered sleeve, idea 40
KILLED book-level drawdown control, and ideas 55/57/4 found net Sharpe orders by FLIP
RATE (a regime switch adds flips, it does not remove them).  H1 alone is not a KEEP —
the always-on stop is a loser, so "less bad" is not "good".

Design (PROTOCOL rules 1-8)
---------------------------
Universes : u56 = load_universe(); broad = load_universe(broad=True) (136 names).
            Both reported at every arm.  SURVIVORSHIP: current constituents.
Books     : idea 94's three PRE-CHOSEN constructions, imported not re-implemented —
            `v1` (live rules), `top20` (idea 2's 4b KEEP), `ew-band3` (idea 57's).
Params    : exactly TWO tuned dimensions —
            * stop depth S in {10, 15, 20, 25}%,
            * arming regime ARM in {always, spy200, breadth20}.
            Plus the S=none control.  13 arms per (panel, book); ALL reported.
            Cooldown is FIXED at 0 (idea 94's cooldown axis is not re-opened here),
            books / universes / costs are reported at every value and never selected on.
Regimes   : `always`     — armed every day (this must reproduce idea 94 exactly).
            `spy200`     — armed on days where SPY's close is below its own 200d MA.
            `breadth20`  — armed on days where the fraction of panel names above their
                           own 200d MA is at or below its TRAILING (expanding, min 3y)
                           20th percentile.  Expanding, so no look-ahead.
            The regime is read at close i, the same bar the stop trigger is read at,
            and the exit executes at close i+1 (PROTOCOL rule 2, idea 96 section 1).
Costs     : 10 bps (protocol, verdicts read here) and 25 bps, applied analytically —
            exact, because the held path does not depend on cost_bps.
Baseline  : RULES v1 weekly on the same panel (4a) and SPY buy-and-hold (4b).
Rule 8    : (S, ARM) chosen on 2009-2016 IS by Sharpe, 2017-2026 evaluated untouched;
            OOS CAGR/Sharpe/MaxDD reported against the baseline's and SPY's OOS.
Controls  : every arm is priced against (a) its own no-stop control and (b) that
            control de-grossed by a constant g to the SAME MaxDD (idea 66's exact
            lever).  An instrument that cannot beat holding less is not an instrument.

Reproduction gate, asserted before any result is read: with ARM=always this run's
simulator must equal idea 94's `run_stop` to machine precision at every depth, and
with stop=None it must equal `engine.backtest`.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

# --- import idea 94's module (not a re-implementation) ------------------------
_p94 = ROOT / "research" / "backtests" / "2026-09-04_trailing-stop_cloud.py"
_spec = importlib.util.spec_from_file_location("ts94", _p94)
ts94 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ts94)
BOOKS = ts94.BOOKS                      # v1 / top20 / ew-band3, exactly as published
at_cost = ts94.at_cost
m = ts94.m
halves = ts94.halves
turn_per_yr = ts94.turn_per_yr

STOPS = [0.10, 0.15, 0.20, 0.25]
ARMS = ["always", "spy200", "breadth20"]
COSTS = [10, 25]
PROTO_COST = 10
FREQ = "W"
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
BREADTH_Q = 0.20
MIN_HIST = 756                          # 3y before the expanding quantile is usable
SCRIPT = "research/backtests/2026-09-06_stop-only-in-crashes_B.py"
OUT = ROOT / "research" / "backtests" / "2026-09-06_stop-only-in-crashes_B"


# ---------------------------------------------------------------- regimes
def regime(px, arm):
    """Boolean per-day series: is the stop ARMED at close i?  No look-ahead."""
    if arm == "always":
        return pd.Series(True, index=px.index)
    if arm == "spy200":
        spy = px["SPY"]
        return (spy < spy.rolling(200).mean()).fillna(False)
    if arm == "breadth20":
        names = [c for c in px.columns if c != "SPY"]
        p = px[names]
        br = (p > p.rolling(200).mean()).sum(axis=1) / p.notna().sum(axis=1).clip(lower=1)
        q = br.expanding(min_periods=MIN_HIST).quantile(BREADTH_Q)
        return (br <= q).fillna(False)
    raise ValueError(arm)


# ---------------------------------------------------------------- simulator
def run_armed(prices, weights, stop=None, armed=None, cooldown=0, freq=FREQ):
    """idea 94's run_stop with one added gate: the trigger only fires on armed days.

    armed=None (or all-True) must reproduce ts94.run_stop bit-for-bit; asserted in
    harness().  Everything else — the t+1 exit, cash (not redistribution), the
    trailing high since entry — is idea 94's mechanism unchanged.
    """
    rets = prices.pct_change().fillna(0.0).values
    pxv = prices.values
    n = pxv.shape[1]
    w_target = weights.reindex(prices.index).fillna(0.0).shift(1).values
    mask = rebalance_mask(prices.index, freq).shift(1, fill_value=False).values
    arm = np.ones(len(prices), dtype=bool) if armed is None else armed.reindex(prices.index).fillna(False).values

    cur = np.zeros(n)
    peak = np.full(n, np.nan)
    blocked_until = np.zeros(n, dtype=int)
    pending = np.zeros(n, dtype=bool)
    port = np.zeros(len(prices))
    turn = np.zeros(len(prices))
    invested = np.zeros(len(prices))
    n_stops = 0

    for i in range(len(prices)):
        if pending.any():
            turn[i] += cur[pending].sum()
            cur = np.where(pending, 0.0, cur)
            pending[:] = False
        if mask[i] or i == 0:
            new = w_target[i].copy()
            if stop is not None and cooldown > 0:
                new = np.where(blocked_until > i, 0.0, new)
            turn[i] += np.abs(new - cur).sum()
            cur = new
        held = cur.copy()
        invested[i] = held.sum()
        port[i] = float(np.nansum(held * rets[i]))
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        if tot > 0:
            cur = growth / tot
        if stop is not None:
            alive = cur > 1e-9
            p = pxv[i]
            peak = np.where(alive, np.fmax(np.where(np.isnan(peak), -np.inf, peak), p), np.nan)
            hit = alive & np.isfinite(p) & (p < peak * (1 - stop))
            if not arm[i]:
                hit = np.zeros(n, dtype=bool)       # DISARMED: trailing high still tracked
            if hit.any():
                pending |= hit
                n_stops += int(hit.sum())
                blocked_until = np.where(hit, i + 1 + cooldown, blocked_until)

    idx = prices.index
    return (pd.Series(port, index=idx), pd.Series(turn, index=idx),
            pd.Series(invested, index=idx), n_stops)


# ---------------------------------------------------------------- harness
def harness(px):
    w = BOOKS["top20"](px)
    g0, t0, _, ns0 = run_armed(px, w, stop=None)
    ref = backtest(px, w, cost_bps=0, freq=FREQ)
    d = float((g0 - ref["returns"]).abs().max())
    assert d < 1e-12, f"no-stop != engine.backtest ({d:.3e})"
    assert ns0 == 0
    worst = 0.0
    for s in STOPS:
        a = run_armed(px, w, stop=s, armed=None)
        b = ts94.run_stop(px, w, stop=s, cooldown=0)
        worst = max(worst, float((a[0] - b[0]).abs().max()), float((a[1] - b[1]).abs().max()))
        assert a[3] == b[3], f"firing count differs at {s}"
    assert worst < 1e-12, f"ARM=always != idea 94 ({worst:.3e})"
    print(f"harness OK: no-stop==engine.backtest (max|d|={d:.1e}); "
          f"ARM=always==idea94 run_stop (max|d|={worst:.1e}), firing counts identical")


# ---------------------------------------------------------------- pricing
def degross_g(gross, turn, target_dd, cost):
    """Constant g such that the SAME book scaled by g has MaxDD == target_dd (idea 66)."""
    if m(at_cost(gross, turn, cost))[2] >= target_dd:
        return 1.0
    lo, hi = 0.0, 1.0
    for _ in range(60):
        g = (lo + hi) / 2
        if m(at_cost(g * gross, g * turn, cost))[2] < target_dd:
            hi = g
        else:
            lo = g
    return (lo + hi) / 2


def lever_price(gross, turn, cost, dd_ctrl, cagr_ctrl, dd_arm):
    """pp of CAGR the static-gross lever charges per pp of drawdown bought, at dd_arm."""
    if dd_arm <= dd_ctrl:                       # bought no drawdown
        return np.nan
    g = degross_g(gross, turn, dd_arm, cost)
    c_lev = m(at_cost(g * gross, g * turn, cost))[0]
    dd_bought = (dd_arm - dd_ctrl) * 100
    return (cagr_ctrl - c_lev) * 100 / dd_bought if dd_bought > 1e-9 else np.nan


def fail4b(r, spy, oos_sh, spy_oos_sh):
    c, s, dd = m(r); h1, h2 = halves(r)
    sc, ss, sdd = m(spy); s1, s2 = halves(spy)
    bad = []
    if h1 <= s1: bad.append("H1")
    if h2 <= s2: bad.append("H2")
    if oos_sh <= spy_oos_sh: bad.append("OOS")
    if dd < 0.60 * sdd: bad.append("DD")
    if c < 0.70 * sc: bad.append("CAGR")
    return bad


def fail4a(r, base):
    _, _, dd = m(r); h1, h2 = halves(r)
    _, _, bdd = m(base); b1, b2 = halves(base)
    bad = []
    if h1 <= b1: bad.append("H1")
    if h2 <= b2: bad.append("H2")
    if dd < bdd: bad.append("DD")
    return bad


# ---------------------------------------------------------------- main
def main():
    rows, wf_rows, reg_rows = [], [], []
    for pname, broad in (("u56", False), ("broad", True)):
        px = load_universe(broad=broad)
        start = px.index[260]
        if pname == "u56":
            harness(px)
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        base_r = backtest(px, rules_v1_weights(px), cost_bps=PROTO_COST, freq=FREQ)["returns"].loc[start:]

        armed = {a: regime(px, a) for a in ARMS}
        for a in ARMS:
            v = armed[a].loc[start:]
            reg_rows.append(dict(panel=pname, arm=a, armed_frac=float(v.mean()),
                                 armed_days=int(v.sum()),
                                 armed_frac_IS=float(v.loc[:IS_END].mean()),
                                 armed_frac_OOS=float(v.loc[OOS_START:].mean())))

        for bname, wf in BOOKS.items():
            w = wf(px)
            g_c, t_c, inv_c, _ = run_armed(px, w, stop=None)
            g_c, t_c, inv_c = g_c.loc[start:], t_c.loc[start:], inv_c.loc[start:]
            sims = {}
            for s in STOPS:
                for a in ARMS:
                    gg, tt, ii, ns = run_armed(px, w, stop=s, armed=armed[a])
                    sims[(s, a)] = (gg.loc[start:], tt.loc[start:], ii.loc[start:], ns)
            for cost in COSTS:
                r_c = at_cost(g_c, t_c, cost)
                c_c, s_c, dd_c = m(r_c)
                h1c, h2c = halves(r_c)
                oos_c = m(r_c.loc[OOS_START:])[1]
                rows.append(dict(panel=pname, book=bname, cost=cost, stop="none", arm="none",
                                 fires=0, fires_yr=0.0, CAGR=c_c, Sharpe=s_c, MaxDD=dd_c,
                                 H1=h1c, H2=h2c, IS_Sharpe=m(r_c.loc[:IS_END])[1], OOS_Sharpe=oos_c,
                                 OOS_CAGR=m(r_c.loc[OOS_START:])[0], OOS_MaxDD=m(r_c.loc[OOS_START:])[2],
                                 dCAGR=0.0, dSharpe=0.0, dMaxDD=0.0, gross=float(inv_c.mean()),
                                 turn_yr=turn_per_yr(t_c), lever_pp=np.nan,
                                 d_crash_ann=0.0, d_trend_ann=0.0, y2020=0.0, y2022=0.0,
                                 fail4a="|".join(fail4a(r_c, base_r)),
                                 fail4b="|".join(fail4b(r_c, spy, oos_c, m(spy.loc[OOS_START:])[1]))))
                for (s, a), (gg, tt, ii, ns) in sims.items():
                    r = at_cost(gg, tt, cost)
                    c, sh, dd = m(r)
                    h1, h2 = halves(r)
                    oos = m(r.loc[OOS_START:])[1]
                    d = r - r_c                                  # stop minus its own control
                    crash = armed["spy200"].reindex(d.index).fillna(False)
                    rows.append(dict(
                        panel=pname, book=bname, cost=cost, stop=f"{s:.2f}", arm=a,
                        fires=ns, fires_yr=ns / (len(gg) / 252), CAGR=c, Sharpe=sh, MaxDD=dd,
                        H1=h1, H2=h2, IS_Sharpe=m(r.loc[:IS_END])[1], OOS_Sharpe=oos,
                        OOS_CAGR=m(r.loc[OOS_START:])[0], OOS_MaxDD=m(r.loc[OOS_START:])[2],
                        dCAGR=(c - c_c) * 100, dSharpe=sh - s_c, dMaxDD=(dd - dd_c) * 100,
                        gross=float(ii.mean()), turn_yr=turn_per_yr(tt),
                        lever_pp=lever_price(g_c, t_c, cost, dd_c, c_c, dd),
                        d_crash_ann=float(d[crash].mean() * 252 * 100),
                        d_trend_ann=float(d[~crash].mean() * 252 * 100),
                        y2020=(np.prod(1 + r[r.index.year == 2020]) - 1 -
                               (np.prod(1 + r_c[r_c.index.year == 2020]) - 1)) * 100,
                        y2022=(np.prod(1 + r[r.index.year == 2022]) - 1 -
                               (np.prod(1 + r_c[r_c.index.year == 2022]) - 1)) * 100,
                        fail4a="|".join(fail4a(r, base_r)),
                        fail4b="|".join(fail4b(r, spy, oos, m(spy.loc[OOS_START:])[1]))))

                # ---- rule 8: choose (S, ARM) on IS only, read OOS untouched
                cand = {("none", "none"): r_c}
                for (s, a), (gg, tt, _, _) in sims.items():
                    cand[(f"{s:.2f}", a)] = at_cost(gg, tt, cost)
                pick = max(cand, key=lambda k: m(cand[k].loc[:IS_END])[1])
                best_oos = max(cand, key=lambda k: m(cand[k].loc[OOS_START:])[1])
                rp, rc = cand[pick], cand[("none", "none")]
                wf_rows.append(dict(
                    panel=pname, book=bname, cost=cost, pick_stop=pick[0], pick_arm=pick[1],
                    IS_Sharpe=m(rp.loc[:IS_END])[1],
                    OOS_CAGR=m(rp.loc[OOS_START:])[0], OOS_Sharpe=m(rp.loc[OOS_START:])[1],
                    OOS_MaxDD=m(rp.loc[OOS_START:])[2],
                    ctrl_OOS_Sharpe=m(rc.loc[OOS_START:])[1],
                    ctrl_OOS_CAGR=m(rc.loc[OOS_START:])[0],
                    ctrl_OOS_MaxDD=m(rc.loc[OOS_START:])[2],
                    regret=m(rp.loc[OOS_START:])[1] - m(rc.loc[OOS_START:])[1],
                    best_oos_stop=best_oos[0], best_oos_arm=best_oos[1],
                    best_OOS_Sharpe=m(cand[best_oos].loc[OOS_START:])[1],
                    base_OOS_Sharpe=m(base_r.loc[OOS_START:])[1],
                    base_OOS_CAGR=m(base_r.loc[OOS_START:])[0],
                    base_OOS_MaxDD=m(base_r.loc[OOS_START:])[2],
                    spy_OOS_Sharpe=m(spy.loc[OOS_START:])[1],
                    spy_OOS_CAGR=m(spy.loc[OOS_START:])[0],
                    spy_OOS_MaxDD=m(spy.loc[OOS_START:])[2]))
                print(f"  {pname:5s} {bname:8s} {cost:2d}bps  ctrl S={s_c:.3f} DD={dd_c:.1%} "
                      f"| rule8 pick {pick[0]}/{pick[1]} regret {wf_rows[-1]['regret']:+.3f}")

    g = pd.DataFrame(rows)
    wfd = pd.DataFrame(wf_rows)
    rg = pd.DataFrame(reg_rows)
    g.to_csv(f"{OUT}.grid.csv", index=False)
    wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    rg.to_csv(f"{OUT}.regime.csv", index=False)

    pd.set_option("display.width", 200)
    print("\n=== REGIME COVERAGE (post-warmup sample) ===")
    print(rg.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    print("\n=== ALL ARMS (protocol cost 10 bps; every grid point) ===")
    a10 = g[g.cost == PROTO_COST]
    print(a10[["panel", "book", "stop", "arm", "fires_yr", "CAGR", "Sharpe", "MaxDD",
               "dCAGR", "dSharpe", "dMaxDD", "lever_pp", "fail4a", "fail4b"]]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print("\n=== ALL ARMS (25 bps) ===")
    a25 = g[g.cost == 25]
    print(a25[["panel", "book", "stop", "arm", "CAGR", "Sharpe", "MaxDD",
               "dCAGR", "dSharpe", "dMaxDD", "lever_pp", "fail4a", "fail4b"]]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---------------- H1: does arming recover the Sharpe the always-on stop gives up?
    st = g[g.stop != "none"]
    print("\n=== H1 — dSharpe / dMaxDD / dCAGR by arming regime (medians over 12 cells x 4 depths) ===")
    piv = st.groupby(["arm", "stop"]).agg(
        n=("dSharpe", "size"), med_dSharpe=("dSharpe", "median"), dS_gt0=("dSharpe", lambda x: (x > 0).sum()),
        med_dMaxDD=("dMaxDD", "median"), dDD_gt0=("dMaxDD", lambda x: (x > 0).sum()),
        med_dCAGR=("dCAGR", "median"), med_fires_yr=("fires_yr", "median")).reset_index()
    print(piv.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    print("\n=== H1 paired: armed arm minus always-on arm, SAME (panel, book, cost, depth) ===")
    key = ["panel", "book", "cost", "stop"]
    base_al = st[st.arm == "always"].set_index(key)
    h1_rows = []
    for a in ("spy200", "breadth20"):
        sub = st[st.arm == a].set_index(key)
        j = sub.join(base_al, rsuffix="_al")
        h1_rows.append(dict(arm=a, n=len(j),
                            beats_always_Sharpe=int((j.Sharpe > j.Sharpe_al).sum()),
                            med_dSharpe_vs_always=float((j.Sharpe - j.Sharpe_al).median()),
                            beats_ctrl_Sharpe=int((j.dSharpe > 0).sum()),
                            med_dSharpe_vs_ctrl=float(j.dSharpe.median()),
                            buys_DD_vs_ctrl=int((j.dMaxDD > 0).sum()),
                            med_dMaxDD_vs_ctrl=float(j.dMaxDD.median()),
                            med_dCAGR_vs_ctrl=float(j.dCAGR.median()),
                            priceable=int(((j.dMaxDD > 0) & j.lever_pp.notna() &
                                           ((-j.dCAGR / j.dMaxDD.where(j.dMaxDD > 0)) <=
                                            j.lever_pp)).sum())))
    always_self = dict(arm="always", n=len(base_al), beats_always_Sharpe=np.nan,
                       med_dSharpe_vs_always=0.0, beats_ctrl_Sharpe=int((base_al.dSharpe > 0).sum()),
                       med_dSharpe_vs_ctrl=float(base_al.dSharpe.median()),
                       buys_DD_vs_ctrl=int((base_al.dMaxDD > 0).sum()),
                       med_dMaxDD_vs_ctrl=float(base_al.dMaxDD.median()),
                       med_dCAGR_vs_ctrl=float(base_al.dCAGR.median()),
                       priceable=int(((base_al.dMaxDD > 0) & base_al.lever_pp.notna() &
                                      ((-base_al.dCAGR / base_al.dMaxDD.where(base_al.dMaxDD > 0)) <=
                                       base_al.lever_pp)).sum()))
    h1 = pd.DataFrame([always_self] + h1_rows)
    h1.to_csv(f"{OUT}.h1.csv", index=False)
    print(h1.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    print("\n=== H2 — priceability: arms that BUY drawdown at or below the static-gross lever ===")
    pr = st[(st.dMaxDD > 0)].copy()
    pr["paid_pp"] = -pr.dCAGR / pr.dMaxDD
    pr["cheap"] = pr.paid_pp <= pr.lever_pp
    print(f"arms buying any drawdown: {len(pr)} / {len(st)}")
    if len(pr):
        print(pr.groupby("arm").agg(n=("cheap", "size"), cheaper_than_lever=("cheap", "sum"),
                                    med_paid_pp=("paid_pp", "median"),
                                    med_lever_pp=("lever_pp", "median")).to_string(
              float_format=lambda x: f"{x:.3f}"))
        pr.to_csv(f"{OUT}.priceable.csv", index=False)

    print("\n=== THE QUEUE'S PREMISE, measured: where does the always-on stop lose? ===")
    print("annualised return of (stop minus its own control), split by SPY<200dMA regime, 10 bps")
    prem = st[(st.cost == PROTO_COST)].groupby(["arm", "stop"]).agg(
        n=("d_crash_ann", "size"),
        med_d_crash_ann=("d_crash_ann", "median"), crash_gt0=("d_crash_ann", lambda x: (x > 0).sum()),
        med_d_trend_ann=("d_trend_ann", "median"), trend_gt0=("d_trend_ann", lambda x: (x > 0).sum()),
        med_y2020=("y2020", "median"), med_y2022=("y2022", "median")).reset_index()
    print(prem.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    prem.to_csv(f"{OUT}.premise.csv", index=False)

    print("\n=== KEEP paths (4a and 4b), 10 bps, all arms ===")
    p4a = a10[(a10.fail4a == "") & (a10.stop != "none")]
    p4b = a10[(a10.fail4b == "") & (a10.stop != "none")]
    print(f"4a passes: {len(p4a)} / {len(a10[a10.stop!='none'])}")
    if len(p4a):
        print(p4a[["panel", "book", "stop", "arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2"]]
              .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print(f"4b passes: {len(p4b)} / {len(a10[a10.stop!='none'])}")
    if len(p4b):
        print(p4b[["panel", "book", "stop", "arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe"]]
              .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    ctrl4b = a10[(a10.fail4b == "") & (a10.stop == "none")]
    print(f"controls passing 4b (context): {len(ctrl4b)} / {len(a10[a10.stop=='none'])}")

    print("\n=== RULE 8 WALK-FORWARD: params on 2009-2016, 2017-2026 untouched ===")
    print(wfd[["panel", "book", "cost", "pick_stop", "pick_arm", "IS_Sharpe", "OOS_CAGR",
               "OOS_Sharpe", "OOS_MaxDD", "ctrl_OOS_Sharpe", "regret", "best_oos_stop",
               "best_oos_arm", "best_OOS_Sharpe", "base_OOS_Sharpe", "spy_OOS_Sharpe"]]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print(f"\nselector picks a stop in {int((wfd.pick_stop != 'none').sum())}/{len(wfd)} cells; "
          f"picks an ARMED stop in {int((~wfd.pick_arm.isin(['none','always'])).sum())}/{len(wfd)}; "
          f"mean OOS regret vs no-stop control {wfd.regret.mean():+.4f}, "
          f"median {wfd.regret.median():+.4f}")
    w10 = wfd[wfd.cost == PROTO_COST]
    print("\nOOS at 10 bps — selected arm vs RULES v1 baseline vs SPY:")
    print(w10[["panel", "book", "pick_stop", "pick_arm", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
               "base_OOS_CAGR", "base_OOS_Sharpe", "base_OOS_MaxDD",
               "spy_OOS_CAGR", "spy_OOS_Sharpe", "spy_OOS_MaxDD"]]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    print(f"\nwrote {OUT}.grid.csv / .walkforward.csv / .regime.csv / .h1.csv")


if __name__ == "__main__":
    main()

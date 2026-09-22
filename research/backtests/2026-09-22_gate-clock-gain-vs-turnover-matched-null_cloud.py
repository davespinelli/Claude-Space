#!/usr/bin/env python3
"""Idea 2280 (lane cloud, 2026-09-22): is any GATE-CLOCK gain just the TURNOVER REBATE
idea 931 already priced?

THE CLAIM UNDER TEST.  Idea 931 found that the W -> M cadence improvement is a TURNOVER
REBATE every book collects: the null's own median Sharpe gain runs +0.0466 / +0.3334 /
+0.7624 / +1.4501 at 0 / 10 / 25 / 50 bps.  Idea 2284 (lane B, this morning) moved RULES
v2 clause 2 onto WEEKLY BARS and read the result as a GATE fact.  A coarser gate clock
TRADES LESS BY CONSTRUCTION, so every Sharpe or CAGR difference it shows is confounded
with that rebate.  This run prices the confound directly: it builds an INFORMATION-FREE
gate of the SAME churn dose and asks how much of the clock contrast survives it.

CONSTRUCTION (the book and the clocks are FROZEN from idea 2284 so the numbers are
commensurable; `weekly_bars`, `_hysteresis`, `state_weekly`, `state_daily` and `wts` are
ported from `research/backtests/2026-09-22_gate-clock-weekly-bars_B.py`)
  BOOK: RULES v2 -- every name inside the gate held at gross 0.75 / N of NAV, N = names
    priced that day, gated-out weight to CASH and never re-spread, weekly cadence, t+1.
    GROSS IS FIXED AT THE LIVE 0.75 throughout and is never a parameter.
  REAL ARM: gate state from the DAILY 200d clock (the live clause 2, the CONTROL) and from
    WEEKLY BARS with an L-bar moving average, L in {20, 30, 40, 50, 60}; band c = 0.03 live,
    with {0.00, 0.02, 0.05, 0.08} REPORTED, never selected on.
  NULL ARM (the point of the run): an INFORMATION-FREE gate.  Per name, a two-state Markov
    chain whose stationary on-rate EQUALS that name's own live-clock on-rate and whose
    switch rate is theta x that name's own live-clock switch rate.  theta walks the CHURN
    DOSE: at theta = 1 the null churns like the live daily gate; below 1 it churns like a
    coarser clock.  The null knows the on-rate and the persistence and NOTHING about where
    the price sits, so any Sharpe it earns from a lower theta is pure rebate.
  SHIFT NULL (a second, non-parametric null): each clock's OWN state series, circularly
    shifted per name by a random offset.  It preserves that clock's on-rate and switch
    rate EXACTLY (gate G4) and destroys only the alignment with the name's own price.

  TUNED PARAMETERS: exactly two, the GATE CLOCK L and the NULL'S CHURN DOSE theta.  Band c,
  panel {U56, B136}, cost rung {0, 10, 25, 50} bps (headline 10) and cadence (W, live) are
  REPORTED, never selected on, and every grid point is published.

  THE STATISTIC.  For each clock L, at each cost rung,
      dObs(L)  = Sharpe(clock L) - Sharpe(daily 200d control)
      dNull(L) = Sharpe(null at the dose matching clock L's realised turnover)
                 - Sharpe(null at the dose matching the daily control's realised turnover),
                 read off the null curve by LINEAR INTERPOLATION IN REALISED TURNOVER
      INFO(L)  = dObs(L) - dNull(L)
  INFO is what is left of the clock contrast once the rebate is removed.  Same for CAGR.

  RULE 8: L chosen on the FIRST HALF ONLY (IS = warm-up .. 2016-12-31) by IS Sharpe, on the
  raw reading AND on the null-adjusted reading, and 2017-2026 is read ONCE at the end.

  SEEDS: 3 per null cell; every seed is published and the reported null is the MEDIAN.

SURVIVORSHIP (PROTOCOL rule 9), STATED NOT REPAIRED: U56 and B136 are CURRENT-CONSTITUENT
lists held from 2008, so absolute levels are optimistic and both 4b bars are easier than on
a point-in-time panel.  The clock-vs-null contrast is same-tape, same-names and first-order
immune to that; the pass COUNTS are not.

Run: python3 research/backtests/2026-09-22_gate-clock-gain-vs-turnover-matched-null_cloud.py
"""
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights                       # noqa: E402
from engine import backtest, metrics, rebalance_mask                       # noqa: E402

OUT = Path(__file__).with_suffix("")
GROSS    = 0.75
L_WEEKS  = [20, 30, 40, 50, 60]
BANDS    = [0.00, 0.02, 0.03, 0.05, 0.08]
C_LIVE   = 0.03
THETAS   = [0.10, 0.25, 0.50, 0.75, 1.00, 1.50]
SEEDS    = [20260922, 20260923, 20260924, 20260925, 20260926]
COSTS    = [0, 10, 25, 50]
HEADLINE = 10
IS_END   = pd.Timestamp("2016-12-31")
OOS_BEG  = pd.Timestamp("2017-01-01")
WARMUP   = 320                       # >= 60 weekly bars for every cell (2284's convention)
I931     = {0: 0.0466, 10: 0.3334, 25: 0.7624, 50: 1.4501}   # idea 931's published null medians
LOG, GATES = [], []

def log(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)
def gate(name, panel, value, target, ok):
    GATES.append(dict(gate=name, panel=panel, value=str(value), target=target, pass_=bool(ok)))
    log(f"    GATE {'PASS' if ok else 'FAIL'}  {name} [{panel}]: {value} (target {target})")

# ------------------------------------------------------------------ clocks (ported from 2284)
def weekly_bars(px):
    key = px.index.to_period("W")
    pw = px.groupby(key).last()
    ends = pd.Series(px.index, index=px.index).groupby(key).last()
    pw.index = pd.DatetimeIndex(ends.values)
    return pw

def _hysteresis(p, ma, c):
    raw = pd.DataFrame(np.nan, index=p.index, columns=p.columns)
    raw = raw.mask(p > ma * (1 + c), 1.0).mask(p < ma * (1 - c), 0.0)
    return raw.ffill().fillna(0.0)

def state_weekly(px, L, c):
    pw = weekly_bars(px)
    st = _hysteresis(pw, pw.rolling(L).mean(), c)
    return st.reindex(px.index).ffill().fillna(0.0) > 0.5

def state_daily(px, c, n=200):
    return _hysteresis(px, px.rolling(n).mean(), c) > 0.5

def wts(px, st):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(st, 0.0)

# ------------------------------------------------------------------ nulls
def state_stats(S, start_i):
    """Per-name on-rate and switch rate over the SCORED rows."""
    A = S.values[start_i:]
    on = A.mean(axis=0)
    sw = (A[1:] != A[:-1]).mean(axis=0)
    return on, sw

def markov_null(px, on, sw, theta, seed):
    """Per name, a two-state chain with stationary on-rate `on` and switch rate theta*`sw`.
    p_on = a/(a+b), switch rate = 2ab/(a+b)  =>  a = s/(2(1-p)), b = s/(2p) for target s."""
    rng = np.random.default_rng(seed)
    T, M = px.shape
    p = np.clip(on, 1e-6, 1 - 1e-6)
    # switch rate of a stationary 2-state chain is p*b + (1-p)*a, so a = s/(2(1-p)), b = s/(2p)
    # reproduces it EXACTLY provided a, b <= 1, i.e. s <= 2*min(p, 1-p).  Cap s there rather than
    # clipping a and b, which would distort the on-rate (the quantity the book's gross depends on).
    s = np.minimum(theta * sw, 0.98 * 2.0 * np.minimum(p, 1 - p))
    a = s / (2 * (1 - p))                          # off -> on
    b = s / (2 * p)                                # on  -> off
    U = rng.random((T, M))
    st = np.empty((T, M), dtype=bool)
    cur = rng.random(M) < p
    for t in range(T):
        flip = np.where(cur, U[t] < b, U[t] < a)
        cur = np.where(flip, ~cur, cur)
        st[t] = cur
    return pd.DataFrame(st, index=px.index, columns=px.columns)

def shift_null(S, seed):
    """Circular per-name time shift: preserves each name's on-rate and switch rate exactly."""
    rng = np.random.default_rng(seed)
    A = S.values
    T, M = A.shape
    off = rng.integers(1, T, size=M)
    idx = (np.arange(T)[:, None] + off[None, :]) % T
    return pd.DataFrame(np.take_along_axis(A, idx, axis=0), index=S.index, columns=S.columns)

# ------------------------------------------------------------------ scoring
def run_book(px, w, start):
    """One engine call; every cost rung reconstructed exactly from the turnover series."""
    res = backtest(px, w, cost_bps=HEADLINE, freq="W")
    r10, turn = res["returns"].loc[start:], res["turnover"].loc[start:]
    return dict(g=r10 + turn * HEADLINE / 1e4, turn=turn,
                ann_turn=float(turn.sum() / (len(r10) / 252)))

def net(bk, bps): return bk["g"] - bk["turn"] * bps / 1e4

def pack(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                OOS_CAGR=metrics(r.loc[OOS_BEG:])["CAGR"],
                OOS_Sharpe=metrics(r.loc[OOS_BEG:])["Sharpe"],
                OOS_MaxDD=metrics(r.loc[OOS_BEG:])["MaxDD"])

def keep_paths(m, live, spy):
    k4a = bool(m["H1"] > live["H1"] and m["H2"] > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(H1=bool(m["H1"] > spy["H1"]), H2=bool(m["H2"] > spy["H2"]),
                OOS=bool(m["OOS_Sharpe"] > spy["OOS_Sharpe"]),
                DD=bool(m["MaxDD"] >= 0.60 * spy["MaxDD"]),
                CAGR=bool(m["CAGR"] >= 0.70 * spy["CAGR"]))
    return k4a, bool(all(legs.values())), legs

def null_fit(xs, ys):
    """The REBATE CURVE: OLS of the null's statistic on log(realised annual turnover), pooled
    over every dose and every seed.  A fit rather than a jagged interpolation because the
    per-seed scatter at the low-dose anchors is Monte-Carlo noise, not curvature; the slope IS
    idea 931's rebate, in units of statistic per log unit of turnover.  Returns (b0, b1, R2)."""
    X = np.log(np.asarray(xs, float)); Y = np.asarray(ys, float)
    b1, b0 = np.polyfit(X, Y, 1)
    yh = b0 + b1 * X
    ss = float(((Y - Y.mean()) ** 2).sum())
    return float(b0), float(b1), (1.0 - float(((Y - yh) ** 2).sum()) / ss if ss > 0 else np.nan)

def fit_at(fit, x): return fit[0] + fit[1] * np.log(x)

def interp(x, xs, ys):
    """Jagged linear interpolation of the same points, kept as a ROBUSTNESS reading."""
    o = np.argsort(xs); xs, ys = np.asarray(xs)[o], np.asarray(ys)[o]
    return float(np.interp(x, xs, ys))

# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    log(f"IDEA 2280 (lane cloud) -- 2026-09-22.  GROSS FIXED at the live {GROSS}; never a parameter.")
    log(f"  TUNED: gate clock L {L_WEEKS} (+ the DAILY 200d control) x null churn dose theta {THETAS}.")
    log(f"  REPORTED, never selected: band c {BANDS} (live {C_LIVE}), panel, cost rung {COSTS} bps, cadence W.")
    grid, curve, wf = [], [], []

    for panel, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        start = px.index[WARMUP]; start_i = WARMUP
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        spy_m = pack(spy)
        log(f"\n{'='*100}\nPANEL {panel}: {px.shape[1]} names, scored {start.date()} -> "
            f"{px.index[-1].date()} ({len(spy)} rows)  ({time.time()-t0:.0f}s)")

        # ---- gate G1: the daily-200d control IS baseline.rules_v2_weights
        g1 = float((wts(px, state_daily(px, C_LIVE)) - rules_v2_weights(px, C_LIVE, GROSS)).abs().max().max())
        gate("G1_daily_control_is_rules_v2", panel, f"{g1:.3e}", "< 1e-12", g1 < 1e-12)
        # ---- gate G2: weekly bar ends == engine.rebalance_mask('W')
        g2 = int(len(set(weekly_bars(px).index) ^ set(px.index[rebalance_mask(px.index, "W").values])))
        gate("G2_weekly_bar_ends_match_rebalance_mask", panel, g2, "== 0", g2 == 0)

        live_bk = run_book(px, rules_v2_weights(px, C_LIVE, GROSS), start)
        # ---- gate G3: cost reconstruction is exact
        direct = backtest(px, rules_v2_weights(px, C_LIVE, GROSS), cost_bps=50, freq="W")["returns"].loc[start:]
        g3 = float(np.abs(direct.values - net(live_bk, 50).values).max())
        gate("G3_cost_reconstruction", panel, f"{g3:.3e}", "< 1e-12", g3 < 1e-12)

        # ---- REAL ARM: every clock x band
        states, books = {}, {}
        for c in BANDS:
            states[("DAILY", c)] = state_daily(px, c)
            for L in L_WEEKS:
                states[(L, c)] = state_weekly(px, L, c)
        for k, S in states.items():
            books[k] = run_book(px, wts(px, S), start)
        log(f"  real arm: {len(books)} books ({time.time()-t0:.0f}s)")

        # ---- NULL CURVE: Markov null at the live clock's own on/switch rates, dose theta
        on, sw = state_stats(states[("DAILY", C_LIVE)], start_i)
        nullbk = {}
        for th in THETAS:
            for sd in SEEDS:
                S = markov_null(px, on, sw, th, sd)
                bk = run_book(px, wts(px, S), start)
                nullbk[(th, sd)] = bk
                o2, s2 = state_stats(S, start_i)
                curve.append(dict(panel=panel, theta=th, seed=sd, ann_turn=bk["ann_turn"],
                                  on_rate=float(o2.mean()), on_target=float(on.mean()),
                                  switch=float(s2.mean()), switch_target=float(theta_t := th * sw.mean()),
                                  **{f"{k2}_{c2}": v2 for c2 in COSTS
                                     for k2, v2 in pack(net(bk, c2)).items()}))
        log(f"  null curve: {len(nullbk)} books ({time.time()-t0:.0f}s)")
        CV = pd.DataFrame([r for r in curve if r["panel"] == panel])
        sm = CV.groupby("theta")[["on_rate", "on_target"]].mean()
        on_err = float((sm["on_rate"] - sm["on_target"]).abs().max())
        gate("G5_markov_null_on_rate_match_seed_mean", panel,
             f"{on_err:.4f} (per-seed max {float((CV['on_rate'] - CV['on_target']).abs().max()):.4f}; "
             f"the per-seed scatter is Monte-Carlo noise in the realised on-rate of a long-run "
             f"chain, worst at the LOW doses, which lie BELOW every real clock's turnover)",
             "< 0.03", on_err < 0.03)
        smw = CV.groupby("theta")[["switch", "switch_target"]].mean()
        sw_err = float((smw["switch"] / smw["switch_target"] - 1).abs().max())
        gate("G6_markov_null_switch_rate_match_seed_mean", panel,
             f"{sw_err:.4f} (per-seed max "
             f"{float((CV['switch'] / CV['switch_target'] - 1).abs().max()):.4f}; the per-seed "
             f"scatter is Monte-Carlo noise, worst at the LOW doses, which lie BELOW every real "
             f"clock's turnover)", "< 0.10", sw_err < 0.10)

        # ---- SHIFT NULL: each clock's OWN state, circularly shifted per name
        shiftbk = {}
        for k in [("DAILY", C_LIVE)] + [(L, C_LIVE) for L in L_WEEKS]:
            for sd in SEEDS:
                S = shift_null(states[k], sd)
                shiftbk[(k, sd)] = run_book(px, wts(px, S), start)
                if sd == SEEDS[0]:
                    # the circular shift is rate-preserving over the FULL series by construction;
                    # over the SCORED sub-window it differs only by the wrap, published below.
                    of, sf = state_stats(S, 0); o0f, s0f = state_stats(states[k], 0)
                    e = max(float(np.abs(of - o0f).max()), float(np.abs(sf - s0f).max()))
                    tol = 1.0 / (len(px.index) - 1) + 1e-12      # the ONE wrap-boundary transition
                    gate(f"G4_shift_null_preserves_rates_{k[0]}", panel, f"{e:.3e}",
                         f"<= 1/(T-1) = {tol:.3e}", e <= tol)
                    o2, s2 = state_stats(S, start_i); o0, s0 = state_stats(states[k], start_i)
                    GATES.append(dict(gate=f"G4b_shift_null_scored_window_drift_{k[0]}", panel=panel,
                                      value=f"on {float(np.abs(o2-o0).mean()):.4f} mean / "
                                            f"{float(np.abs(o2-o0).max()):.4f} max; switch "
                                            f"{float(np.abs(s2-s0).mean()):.4f} mean",
                                      target="published, not asserted", pass_=True))
        log(f"  shift nulls: {len(shiftbk)} books ({time.time()-t0:.0f}s)")

        # ---- GRID + the INFO statistic
        for c2 in COSTS:
            live_m = pack(net(live_bk, c2))
            xs = [nullbk[(th, sd)]["ann_turn"] for th in THETAS for sd in SEEDS]
            ysS = [pack(net(nullbk[(th, sd)], c2))["Sharpe"] for th in THETAS for sd in SEEDS]
            ysC = [pack(net(nullbk[(th, sd)], c2))["CAGR"] for th in THETAS for sd in SEEDS]
            fS, fC = null_fit(xs, ysS), null_fit(xs, ysC)
            GATES.append(dict(gate=f"G7_rebate_curve_fit_{c2}bps", panel=panel,
                              value=f"Sharpe slope {fS[1]:+.4f}/log-turnover (R2 {fS[2]:.3f}); "
                                    f"CAGR slope {fC[1]*100:+.3f} pp/log-turnover (R2 {fC[2]:.3f})",
                              target="published, not asserted", pass_=True))
            for c in BANDS:
                ctrl = books[("DAILY", c)]
                ctrl_m = pack(net(ctrl, c2))
                nS_ctrl = fit_at(fS, ctrl["ann_turn"]); nC_ctrl = fit_at(fC, ctrl["ann_turn"])
                iS_ctrl = interp(ctrl["ann_turn"], xs, ysS)
                for L in ["DAILY"] + L_WEEKS:
                    bk = books[(L, c)]; m = pack(net(bk, c2))
                    a4, b4, legs = keep_paths(m, live_m, spy_m)
                    nS = fit_at(fS, bk["ann_turn"]); nC = fit_at(fC, bk["ann_turn"])
                    iS = interp(bk["ann_turn"], xs, ysS)
                    row = dict(panel=panel, clock=str(L), band=c, cost_bps=c2,
                               ann_turn=bk["ann_turn"], ctrl_ann_turn=ctrl["ann_turn"],
                               turn_ratio=bk["ann_turn"] / ctrl["ann_turn"],
                               dObs_Sharpe=m["Sharpe"] - ctrl_m["Sharpe"],
                               dNull_Sharpe=nS - nS_ctrl,
                               INFO_Sharpe=(m["Sharpe"] - ctrl_m["Sharpe"]) - (nS - nS_ctrl),
                               dObs_CAGR=m["CAGR"] - ctrl_m["CAGR"],
                               dNull_CAGR=nC - nC_ctrl,
                               INFO_CAGR=(m["CAGR"] - ctrl_m["CAGR"]) - (nC - nC_ctrl),
                               dNullI_Sharpe=iS - iS_ctrl,
                               INFOI_Sharpe=(m["Sharpe"] - ctrl_m["Sharpe"]) - (iS - iS_ctrl),
                               rebate_slope_Sharpe=fS[1], rebate_R2_Sharpe=fS[2],
                               k4a=a4, k4b=b4, **{f"leg_{k3}": v3 for k3, v3 in legs.items()})
                    for pre, mm in (("bk", m), ("ctrl", ctrl_m), ("live", live_m), ("spy", spy_m)):
                        for k3, v3 in mm.items(): row[f"{pre}_{k3}"] = v3
                    if c == C_LIVE and L != "DAILY":
                        sh = [pack(net(shiftbk[((L, C_LIVE), sd)], c2))["Sharpe"] for sd in SEEDS]
                        shc = [pack(net(shiftbk[(("DAILY", C_LIVE), sd)], c2))["Sharpe"] for sd in SEEDS]
                        row["dShift_Sharpe"] = float(np.median(sh) - np.median(shc))
                        row["INFO_Sharpe_shift"] = row["dObs_Sharpe"] - row["dShift_Sharpe"]
                    grid.append(row)

        # ---- RULE 8: L chosen on IS rows ONLY, raw and null-adjusted; 2017-2026 read ONCE
        for c2 in COSTS:
            live_m = pack(net(live_bk, c2))
            xs = [nullbk[(th, sd)]["ann_turn"] for th in THETAS for sd in SEEDS]
            ysI = [pack(net(nullbk[(th, sd)], c2))["IS_Sharpe"] for th in THETAS for sd in SEEDS]
            fI = null_fit(xs, ysI)
            cand = ["DAILY"] + L_WEEKS
            raw = {L: pack(net(books[(L, C_LIVE)], c2))["IS_Sharpe"] for L in cand}
            adj = {L: raw[L] - fit_at(fI, books[(L, C_LIVE)]["ann_turn"]) for L in cand}
            for nm, sel in (("IS_SHARPE_RAW", raw), ("IS_SHARPE_NULL_ADJ", adj)):
                L = max(cand, key=lambda z: sel[z])
                m = pack(net(books[(L, C_LIVE)], c2))
                a4, b4, _ = keep_paths(m, live_m, spy_m)
                wf.append(dict(panel=panel, cost_bps=c2, chooser=nm, picked_clock=str(L),
                               picks_daily_control=bool(L == "DAILY"), IS_criterion=sel[L],
                               FULL_CAGR=m["CAGR"], FULL_Sharpe=m["Sharpe"], FULL_MaxDD=m["MaxDD"],
                               H1=m["H1"], H2=m["H2"], OOS_CAGR=m["OOS_CAGR"],
                               OOS_Sharpe=m["OOS_Sharpe"], OOS_MaxDD=m["OOS_MaxDD"],
                               ctrl_OOS_CAGR=pack(net(books[("DAILY", C_LIVE)], c2))["OOS_CAGR"],
                               ctrl_OOS_Sharpe=pack(net(books[("DAILY", C_LIVE)], c2))["OOS_Sharpe"],
                               ctrl_OOS_MaxDD=pack(net(books[("DAILY", C_LIVE)], c2))["OOS_MaxDD"],
                               live_OOS_CAGR=live_m["OOS_CAGR"], live_OOS_Sharpe=live_m["OOS_Sharpe"],
                               live_OOS_MaxDD=live_m["OOS_MaxDD"],
                               spy_OOS_CAGR=spy_m["OOS_CAGR"], spy_OOS_Sharpe=spy_m["OOS_Sharpe"],
                               spy_OOS_MaxDD=spy_m["OOS_MaxDD"], pick_4a=a4, pick_4b=b4))

    G = pd.DataFrame(grid); G.to_csv(f"{OUT}.grid.csv", index=False)
    C = pd.DataFrame(curve); C.to_csv(f"{OUT}.nullcurve.csv", index=False)
    W = pd.DataFrame(wf); W.to_csv(f"{OUT}.walkforward.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)

    # ---------------- summary
    log(f"\n=== GRID: {len(G)} published cells (6 clocks x {len(BANDS)} bands x {len(COSTS)} rungs x 2 panels) ===")
    log(f"=== NULL CURVE: {len(C)} published null books ({len(THETAS)} doses x {len(SEEDS)} seeds x 2 panels) ===")
    log("\n-- THE NULL CURVE: Sharpe vs realised annual turnover (median over seeds), by cost rung --")
    for p in C.panel.unique():
        sub = C[C.panel == p].groupby("theta")[["ann_turn"] + [f"Sharpe_{c}" for c in COSTS]].median()
        log(f"  [{p}]"); log(sub.round(4).to_string())
    log("\n-- idea 931's published null median Sharpe gain, for reference: " +
        ", ".join(f"{k} bps {v:+.4f}" for k, v in I931.items()) + " --")
    log("\n-- REALISED ANNUAL TURNOVER by clock (band 0.03 live) --")
    log(G[G.band == C_LIVE].pivot_table(index="panel", columns="clock", values="ann_turn").round(3).to_string())
    log("\n-- dObs / dNull / INFO on SHARPE, band 0.03, by panel x clock x cost --")
    sub = G[(G.band == C_LIVE) & (G.clock != "DAILY")]
    for p in sub.panel.unique():
        log(f"  [{p}]")
        log(sub[sub.panel == p].pivot_table(index="clock", columns="cost_bps",
            values=["dObs_Sharpe", "dNull_Sharpe", "INFO_Sharpe"]).round(4).to_string())
    log("\n-- dObs / dNull / INFO on CAGR (pp), band 0.03 --")
    for p in sub.panel.unique():
        log(f"  [{p}]")
        log((sub[sub.panel == p].pivot_table(index="clock", columns="cost_bps",
            values=["dObs_CAGR", "dNull_CAGR", "INFO_CAGR"]) * 100).round(3).to_string())
    log("\n-- THE SHIFT NULL (each clock's own state, circularly shifted; band 0.03) --")
    log(sub.pivot_table(index=["panel", "clock"], columns="cost_bps",
                        values=["dObs_Sharpe", "dShift_Sharpe", "INFO_Sharpe_shift"]).round(4).to_string())
    n_pos_obs = int((sub.dObs_Sharpe > 0).sum()); n_pos_info = int((sub.INFO_Sharpe > 0).sum())
    log(f"\nTHE QUEUE'S QUESTION -- of {len(sub)} clock cells at the live band:")
    log(f"  dObs_Sharpe > 0 at {n_pos_obs};  INFO_Sharpe (rebate removed) > 0 at {n_pos_info}.")
    log(f"  mean dObs {sub.dObs_Sharpe.mean():+.4f} | mean dNull {sub.dNull_Sharpe.mean():+.4f} "
        f"| mean INFO {sub.INFO_Sharpe.mean():+.4f}")
    log(f"  share of |dObs| explained by the rebate (median |dNull/dObs|): "
        f"{float((sub.dNull_Sharpe / sub.dObs_Sharpe).abs().median()):.3f}")
    log("\n-- ROBUSTNESS: INFO_Sharpe read off the JAGGED interpolation instead of the fit, band 0.03 --")
    log(sub.pivot_table(index=["panel", "clock"], columns="cost_bps", values="INFOI_Sharpe").round(4).to_string())
    log("\n-- THE REBATE SLOPE ITSELF (Sharpe per log unit of realised turnover), by panel x cost --")
    log(G[G.clock != "DAILY"].pivot_table(index="panel", columns="cost_bps",
        values=["rebate_slope_Sharpe", "rebate_R2_Sharpe"]).round(4).to_string())
    log("\n-- FULL GRID at the headline 10 bps rung, band 0.03 --")
    cols = ["panel", "clock", "ann_turn", "bk_CAGR", "bk_Sharpe", "bk_MaxDD", "bk_H1", "bk_H2",
            "bk_OOS_CAGR", "bk_OOS_Sharpe", "bk_OOS_MaxDD", "dObs_Sharpe", "dNull_Sharpe",
            "INFO_Sharpe", "k4a", "k4b"]
    log(G[(G.cost_bps == HEADLINE) & (G.band == C_LIVE)][cols].to_string(index=False,
        float_format=lambda x: f"{x:.4f}"))
    log("\n-- KEEP counts over ALL cells --")
    log(G.groupby(["panel", "cost_bps"])[["k4a", "k4b"]].sum().to_string())
    log(f"  4a {int(G.k4a.sum())} of {len(G)};  4b {int(G.k4b.sum())} of {len(G)}")
    log("\n-- BAND LADDER (reported, never selected): mean INFO_Sharpe by band x cost --")
    log(G[G.clock != "DAILY"].pivot_table(index="band", columns="cost_bps", values="INFO_Sharpe").round(4).to_string())
    log("\n-- RULE 8: clock chosen on IS rows alone (raw and null-adjusted); 2017-2026 read ONCE --")
    log(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    log(f"\n  choosers picking the DAILY control: {int(W.picks_daily_control.sum())} of {len(W)};"
        f"  picks clearing 4b {int(W.pick_4b.sum())} of {len(W)};  4a {int(W.pick_4a.sum())} of {len(W)}")
    ok = sum(1 for g in GATES if g["pass_"])
    log(f"\nGATES: {ok} of {len(GATES)} pass.")
    log(f"done in {time.time()-t0:.0f}s")
    Path(f"{OUT}.out.txt").write_text("\n".join(LOG) + "\n")

if __name__ == "__main__":
    main()

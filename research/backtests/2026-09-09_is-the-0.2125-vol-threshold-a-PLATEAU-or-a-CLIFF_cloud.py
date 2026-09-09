#!/usr/bin/env python3
"""Idea 464 — IS THE 0.2125 VOL THRESHOLD A PLATEAU OR A CLIFF?   (cloud, 2026-09-09)

PRE-REGISTERED QUESTION (from QUEUE.md, written before any number here was read)
    Idea 247's 4b KEEP-candidate (`EW_ALL, de-grossed into the RULES v2 band on days when
    SPY vol20 >= theta`, theta = 0.2125) clears the 4b CAGR floor by 0.42 pp @10bps and
    0.13 pp @25bps — under one step of the q grid it was swept on — and only 2 of its 4 q
    points pass.  Sweep theta DIRECTLY IN VOL UNITS on a fine grid and report the width, in
    vol points, of the CONTIGUOUS 4b interval containing the adopted constant, per idea
    401/407's plateau test, before any Sunday review adopts 0.2125.

WHY THE UNIT CHANGE MATTERS.  q is a quantile of the IS vol distribution, so a q-step is a
whole-number-of-days step whose SIZE IN VOL UNITS varies along the distribution (the gap
0.80 -> 0.90 is 0.0538 of vol, the gap 0.60 -> 0.70 is 0.0243).  A margin quoted as "0.6 of
a grid step" is therefore not a margin in the units the rule is written in.  RULES wording
adopts a NUMBER (0.2125), so the robustness question has to be asked in that number's units.

THE BOOK (identical object to idea 247, re-parameterised by theta instead of q)
    W(t) = BAND3-dg weights on ARMED days, EW_ALL weights on disarmed days, both at nominal
    gross 0.75, weekly, next-day execution.  ARMED(t) <=> SPY vol20(t) >= theta, a
    market-wide state known at close t and applied at t+1.  theta is a FIXED constant: no
    quantile, no expanding window, no re-estimation, so IS and OOS coverage are whatever the
    market delivered and are reported, never engineered.

GRID (two tuned parameters and no more: theta and the panel)
    theta   0.060 .. 0.600 step 0.005, then 0.620 .. 0.960 step 0.020 (the coarse tail only
            exists so the interval's upper edge is FOUND, not censored: SPY vol20 tops out at
            0.959), PLUS the incumbent 0.21253315287947144 (idea 247's IS-q80, carried at
            full precision and flagged INCUMBENT) = 128 points
    panels  U56 (fixed ETF/mega-cap), B136 (broad), SMALL439 (sub-$2B less the 44 names with
            max_1d_move >= 1.0 in data/small_meta.csv)
    rungs   10 and 25 bps, BOTH reported at every point, never chosen
    refs    EWALL (theta = +inf, never armed) and BAND3DG (theta = 0, always armed = live
            RULES v2 book) on every panel and rung
    128 x 3 x 2 = 768 grid points, ALL reported to .grid.csv.

THE COMPARAND.  A conditional de-grossing book spends less than 75% of NAV, so each arm is
also priced against a MATCHED-REALISED-GROSS static control (idea 244's channel): EW_ALL at
the nominal gross whose MEAN REALISED gross equals the arm's on the same window.  The solve
is analytic here rather than idea 247's 40-step bisection (gate G5 shows the two agree to
machine precision), because 660 bisections would be 26,400 backtests.

WHAT IS REPORTED (the answer to the queue's question)
  * 4b PASS/FAIL at every theta, plus WHICH BAR BINDS (Sharpe-H1, Sharpe-H2, DD cap, CAGR
    floor) and by how much, in the bar's own units.
  * The CONTIGUOUS 4b interval containing the incumbent: [lo, hi] in vol points, its WIDTH,
    and where the incumbent sits inside it (distance to each edge, and to the nearest edge
    as a fraction of the width).  A CLIFF is an interval whose width is of the order of the
    grid step; a PLATEAU is one many steps wide with the incumbent interior.
  * idea 128's plateau_frac (share of theta points within 0.05 Sharpe of the cell max) on
    the same sweep, for comparability with the record's other adopted constants.
  * The 4a path at every point, against the live RULES v2 book on the same panel/window.
  * RULE 8 (PROTOCOL 8): theta chosen on IS <= 2016-12-31 by IS Sharpe, 2017-01-01.. read
    ONCE.  OOS CAGR/Sharpe/MaxDD vs the RULES v2 baseline, the matched control and SPY; plus
    the OOS-4b interval and whether the IS-chosen theta lands inside it.

SURVIVORSHIP (idea 54, carried): B136 and SMALL439 are CURRENT-constituent lists — names
that died were never in them — so every LEVEL on those two panels is biased upward, and the
bias flatters the ungated/full-gross end of the dial, i.e. the control end.  U56 is a fixed
ETF/mega-cap list and is the least-biased panel; idea 247's candidate is a U56 object, so
read the U56 rows first.  Only the arm-minus-matched-control contrast inside one panel is
load-bearing; no level is.

Costs 10/25 bps per unit turnover; weights decided at close t applied at t+1 (PROTOCOL 2).
Deterministic, no network.  Writes .grid.csv, .interval.csv, .walkforward.csv, .console.txt.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, band_state, rules_v2_weights  # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, rebalance_mask, metrics  # noqa: E402

STAMP = "2026-09-09_is-the-0.2125-vol-threshold-a-PLATEAU-or-a-CLIFF_cloud"
OUT = ROOT / "research" / "backtests"
FREQ = "W"
GROSS = 0.75
RUNGS = [10, 25]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
STEP = 0.005
COARSE = 0.020
# Two-resolution grid: 0.005 through the region where the dial does anything (SPY vol20 runs
# 0.032..0.959, median 0.133), then 0.020 out to 0.960 so the interval's UPPER edge is found
# rather than censored by the grid.  Any width measured in the coarse region carries +/-0.020.
THETAS = ([round(x, 4) for x in np.arange(0.060, 0.600 + 1e-9, STEP)]
          + [round(x, 4) for x in np.arange(0.620, 0.960 + 1e-9, COARSE)])
INCUMBENT = None            # set in main() from the IS q80, at full float precision
PANELS = ["U56", "B136", "SMALL439"]

_console = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _console.append(s)


# ---------------------------------------------------------------- engine twin
def fast_backtest(px, weights, freq=FREQ):
    """Idea 247's simulator, unchanged (gate G1 re-runs it against engine.backtest)."""
    rets = px.pct_change().fillna(0.0).values
    W = weights.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    n = len(px)
    A = np.cumprod(1.0 + rets, axis=0)
    A = np.vstack([np.ones((1, rets.shape[1])), A[:-1]])
    port = np.zeros(n)
    turn = np.zeros(n)
    gross = np.zeros(n)
    cur = np.zeros(rets.shape[1])
    starts = np.flatnonzero(mask)
    for i0, i1 in zip(starts, list(starts[1:]) + [n]):
        w = W[i0]
        turn[i0] = np.abs(w - cur).sum()
        u = w[None, :] * (A[i0:i1] / A[i0][None, :])
        cash = 1.0 - w.sum()
        T = u.sum(axis=1) + cash
        port[i0:i1] = (u * rets[i0:i1]).sum(axis=1) / T
        gross[i0:i1] = u.sum(axis=1) / T
        cur = (u[-1] * (1.0 + rets[i1 - 1])) / (T[-1] * (1.0 + port[i1 - 1]))
    return {"returns0": pd.Series(port, index=px.index),
            "turnover": pd.Series(turn, index=px.index),
            "gross": pd.Series(gross, index=px.index)}


def net(res, bps):
    return res["returns0"] - res["turnover"] * bps / 1e4


def mstats(r):
    m = metrics(r)
    h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


# ---------------------------------------------------------------- books
def ew_weights(px, cols, g=GROSS):
    p = px[cols]
    e = pd.DataFrame(1.0, index=p.index, columns=p.columns).where(p.notna(), 0.0)
    w = g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return w.reindex(columns=px.columns).fillna(0.0)


def band3dg_weights(px, cols, g=GROSS):
    return ew_weights(px, cols, g).where(
        band_state(px[cols], 0.03).reindex(columns=px.columns).fillna(False), 0.0)


def conditional_weights(px, cols, armed, g=GROSS, W=None, B=None):
    """BAND3-dg when armed, EW_ALL when not.  `armed` is a per-day boolean Series.

    W/B may be passed pre-computed (identical objects, cached per panel) — gates G3/G4 call
    it without them and get the same answer.
    """
    a = armed.reindex(px.index).fillna(False)
    if W is None:
        W = ew_weights(px, cols, g)
    if B is None:
        B = band3dg_weights(px, cols, g)
    return B.where(a, axis=0).fillna(0.0) + W.where(~a, axis=0).fillna(0.0)


def spy_vol20(px):
    return px["SPY"].pct_change().rolling(20).std() * np.sqrt(252)


# ------------------------------------------------- analytic matched-gross control
def ew_basket_growth(px, cols, freq=FREQ):
    """x(t) = growth of the EQUAL-WEIGHT basket since its last rebalance.

    For EW_ALL at nominal gross g every name carries weight g/N at the rebalance, so the
    position block is u(t) = (g/N) * A(t)/A(i0) and sum_j u(t) = g * x(t) with x independent
    of g.  Hence realised gross(t) = g*x(t) / (g*x(t) + 1 - g), an EXACT closed form that
    turns the matched-gross solve into a 1-D root find with no backtests (gate G5).
    """
    rets = px.pct_change().fillna(0.0).values
    idx = {c: i for i, c in enumerate(px.columns)}
    take = np.array([idx[c] for c in cols])
    W = ew_weights(px, cols, 1.0).reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    n = len(px)
    A = np.cumprod(1.0 + rets, axis=0)
    A = np.vstack([np.ones((1, rets.shape[1])), A[:-1]])
    x = np.zeros(n)
    starts = np.flatnonzero(mask)
    for i0, i1 in zip(starts, list(starts[1:]) + [n]):
        w = W[i0]
        u = w[None, :] * (A[i0:i1] / A[i0][None, :])
        x[i0:i1] = u.sum(axis=1)
    _ = take
    return pd.Series(x, index=px.index)


def analytic_gross(x, g):
    return (g * x) / (g * x + 1.0 - g)


def solve_matched_g(x_win, target):
    """Nominal g whose MEAN analytic realised gross on the window equals `target`."""
    lo, hi = 1e-6, 1.0 - 1e-9
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if float(analytic_gross(x_win, mid).mean()) < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def panels():
    out = {}
    u = load_universe()
    out["U56"] = (u, [c for c in u.columns])
    b = load_universe(broad=True)
    out["B136"] = (b, [c for c in b.columns])
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    sm = sm[[c for c in sm.columns if c == "SPY" or c not in bad]]
    out["SMALL439"] = (sm, [c for c in sm.columns if c != "SPY"])   # SPY is benchmark only
    return out


# ---------------------------------------------------------------- 4b bookkeeping
def bars_4b(m, mspy):
    """Every 4b bar as a signed MARGIN in its own units (>0 = clears)."""
    return {
        "H1_margin": m["H1"] - mspy["H1"],
        "H2_margin": m["H2"] - mspy["H2"],
        "DD_margin": m["MaxDD"] - 0.60 * mspy["MaxDD"],      # MaxDD is negative
        "CAGR_margin": m["CAGR"] - 0.70 * mspy["CAGR"],
    }


def contiguous_interval(thetas, ok, anchor):
    """[lo, hi] of the contiguous run of True in `ok` that contains `anchor`.

    Returns (lo, hi, width, n_points, anchor_passes).  Edges are the outermost PASSING
    theta values (a conservative reading: the true boundary lies within one grid step).
    """
    t = np.asarray(thetas, dtype=float)
    ok = np.asarray(ok, dtype=bool)
    i = int(np.argmin(np.abs(t - anchor)))
    if not ok[i]:
        return (np.nan, np.nan, 0.0, 0, False)
    lo = i
    while lo - 1 >= 0 and ok[lo - 1]:
        lo -= 1
    hi = i
    while hi + 1 < len(t) and ok[hi + 1]:
        hi += 1
    return (float(t[lo]), float(t[hi]), float(t[hi] - t[lo]), int(hi - lo + 1), True)


def main():
    global INCUMBENT
    PX = panels()
    upx, ucols = PX["U56"]
    INCUMBENT = float(spy_vol20(upx).loc[:IS_END].dropna().quantile(0.80))
    grid = sorted(set(THETAS) | {INCUMBENT})

    say("=== GATES ===")
    st = upx.index[260]
    w2 = rules_v2_weights(upx)
    e_res = engine_backtest(upx, w2, cost_bps=10, freq=FREQ)
    f_res = fast_backtest(upx, w2)
    g1r = float(np.abs((net(f_res, 10) - e_res["returns"]).loc[st:].values).max())
    g1t = float(np.abs((f_res["turnover"] - e_res["turnover"]).loc[st:].values).max())
    say(f"G1 fast_backtest vs engine.backtest (from {st.date()})  max|d ret| = {g1r:.3e}"
        f"  max|d turnover| = {g1t:.3e}")
    assert g1r < 1e-12 and g1t < 1e-12, "G1 FAILED"

    g2 = float(np.abs(band3dg_weights(upx, ucols).values - w2.values).max())
    say(f"G2 band3dg_weights(0.75) == baseline.rules_v2_weights        max|diff| = {g2:.3e}")
    assert g2 == 0.0, "G2 FAILED"

    v = spy_vol20(upx)
    g3 = float(np.abs(conditional_weights(upx, ucols, pd.Series(True, index=upx.index)).values
                      - w2.values).max())
    g4 = float(np.abs(conditional_weights(upx, ucols, pd.Series(False, index=upx.index)).values
                      - ew_weights(upx, ucols).values).max())
    say(f"G3 armed == ALL   == BAND3-dg / live RULES v2                max|diff| = {g3:.3e}")
    say(f"G4 armed == NONE  == EW_ALL                                  max|diff| = {g4:.3e}")
    assert g3 == 0.0 and g4 == 0.0, "G3/G4 FAILED"
    nan_days = int(v.isna().sum())
    say(f"G4b vol20 undefined on the first {nan_days} rows -> those days are DISARMED at every"
        f" theta by construction; all of them precede the 260-day warm-up skip"
        f" ({'inside' if nan_days <= 260 else 'NOT inside'} it).")
    assert nan_days <= 260, "warm-up assumption FAILED"

    # G5: the analytic matched-gross solve vs idea 247's 40-step bisection on backtests
    win_u = upx.index[260:]
    x_u = ew_basket_growth(upx, ucols)
    g5a = max(float(np.abs(analytic_gross(x_u, g) - fast_backtest(upx, ew_weights(upx, ucols, g))["gross"]).max())
              for g in (0.30, 0.68, 0.95))
    tgt = 0.6803
    g_an = solve_matched_g(x_u.reindex(win_u), tgt)
    lo, hi = 0.01, 1.00
    for _ in range(40):                                   # idea 247's exact bisection
        mid = 0.5 * (lo + hi)
        got = float(fast_backtest(upx, ew_weights(upx, ucols, mid))["gross"].reindex(win_u).mean())
        if got < tgt:
            lo = mid
        else:
            hi = mid
    g_bi = 0.5 * (lo + hi)
    say(f"G5 analytic gross(t) vs simulated gross(t)                   max|diff| = {g5a:.3e}")
    say(f"G5 matched-g solve: analytic {g_an:.10f} vs idea-247 bisection {g_bi:.10f}"
        f"  |diff| = {abs(g_an - g_bi):.3e}")
    assert g5a < 1e-12 and abs(g_an - g_bi) < 1e-8, "G5 FAILED"
    say(f"INCUMBENT theta (idea 247's IS q80, full precision) = {INCUMBENT:.14f}"
        f"  (quoted in the memo as 0.2125)")
    say(f"theta grid: {len(grid)} points, {grid[0]:.3f}..{grid[-1]:.3f} step {STEP}"
        f" + the incumbent inserted at full precision")

    # ---------------- GRID
    say("\n=== GRID: 110 thetas x 3 panels x 2 rungs, each vs its matched-gross control ===")
    rows = []
    RET, CRET = {}, {}
    SPYM, BASEM = {}, {}
    for k in PANELS:
        px, cols = PX[k]
        win = px.index[260:]
        x = ew_basket_growth(px, cols).reindex(win)
        vol = spy_vol20(px)
        spy = px["SPY"].pct_change().fillna(0.0).reindex(win)
        mspy = mstats(spy)
        SPYM[k] = mspy
        say(f"\n--- {k}: {len(cols)} held names, {win[0].date()} -> {win[-1].date()} "
            f"({len(win)} days) | SPY {mspy['CAGR']:.2%} / {mspy['Sharpe']:.4f} / "
            f"{mspy['MaxDD']:.2%}, halves {mspy['H1']:.3f}/{mspy['H2']:.3f}")
        EWW = ew_weights(px, cols)                    # cached once per panel
        BW = band3dg_weights(px, cols)
        base_raw = fast_backtest(px, BW)
        ew_raw = fast_backtest(px, EWW)
        for bps in RUNGS:
            BASEM[(k, bps)] = mstats(net(base_raw, bps).reindex(win))
            RET[(k, "BAND3DG", bps)] = net(base_raw, bps).reindex(win)
            RET[(k, "EWALL", bps)] = net(ew_raw, bps).reindex(win)
        for th in grid + ["EWALL", "BAND3DG"]:
            if th == "EWALL":
                r0, name, is_ref = ew_raw, "EWALL", True
            elif th == "BAND3DG":
                r0, name, is_ref = base_raw, "BAND3DG", True
            else:
                armed = (vol >= th).fillna(False)
                r0 = fast_backtest(px, conditional_weights(px, cols, armed, W=EWW, B=BW))
                name, is_ref = f"{th:.6f}", False
            gmean = float(r0["gross"].reindex(win).mean())
            turn_yr = float(r0["turnover"].reindex(win).sum()) / (len(win) / 252)
            gnom = solve_matched_g(x, gmean)
            c0 = fast_backtest(px, EWW * (gnom / GROSS))   # ew_weights is linear in g
            gach = float(c0["gross"].reindex(win).mean())
            armed_share = float((vol >= th).reindex(win).mean()) if not is_ref else (
                1.0 if th == "BAND3DG" else 0.0)
            wis = win[win <= IS_END]
            woos = win[win >= OOS_START]
            for bps in RUNGS:
                r = net(r0, bps).reindex(win)
                c = net(c0, bps).reindex(win)
                RET[(k, name, bps)] = r
                CRET[(k, name, bps)] = c
                m, mc = mstats(r), mstats(c)
                mv2 = BASEM[(k, bps)]
                bb = bars_4b(m, mspy)
                p4a = (m["H1"] > mv2["H1"] and m["H2"] > mv2["H2"] and m["MaxDD"] >= mv2["MaxDD"])
                p4b = all(x_ > 0 for x_ in bb.values())
                binding = min(  # which bar is closest to 0 in its own units
                    bb, key=lambda kk: bb[kk] / {"H1_margin": 1.0, "H2_margin": 1.0,
                                                 "DD_margin": 0.01, "CAGR_margin": 0.01}[kk])
                rows.append(dict(
                    panel=k, theta=(np.nan if is_ref else float(th)), arm=name, ref=is_ref,
                    incumbent=(not is_ref and abs(float(th) - INCUMBENT) < 1e-12),
                    bps=bps, armed_share=armed_share,
                    armed_days=(int((vol >= th).reindex(win).sum()) if not is_ref
                                else (len(win) if th == "BAND3DG" else 0)),
                    armed_share_IS=float((vol >= th).reindex(wis).mean()) if not is_ref else np.nan,
                    armed_share_OOS=float((vol >= th).reindex(woos).mean()) if not is_ref else np.nan,
                    CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m["H1"], H2=m["H2"],
                    gross=gmean, turnover_yr=turn_yr, ctrl_nominal_g=gnom, ctrl_gross=gach,
                    ctrl_Sharpe=mc["Sharpe"], ctrl_CAGR=mc["CAGR"], ctrl_MaxDD=mc["MaxDD"],
                    dSharpe_vs_ctrl=m["Sharpe"] - mc["Sharpe"],
                    dCAGR_vs_ctrl=m["CAGR"] - mc["CAGR"],
                    IS_Sharpe=metrics(r.reindex(wis))["Sharpe"],
                    OOS_CAGR=metrics(r.reindex(woos))["CAGR"],
                    OOS_Sharpe=metrics(r.reindex(woos))["Sharpe"],
                    OOS_MaxDD=metrics(r.reindex(woos))["MaxDD"],
                    pass4a=p4a, pass4b=p4b, binding_bar=binding,
                    beats_ctrl=m["Sharpe"] > mc["Sharpe"],
                    pass4b_and_beats_ctrl=bool(p4b and m["Sharpe"] > mc["Sharpe"]), **bb))
    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    say(f"\nmatched-gross accuracy: max|target - achieved| = "
        f"{float((G.gross - G.ctrl_gross).abs().max()):.3e}")
    say(f"grid points: {len(G)}   4a passes {int(G.pass4a.sum())}   4b passes "
        f"{int(G.pass4b.sum())}   4b AND beats matched control {int(G.pass4b_and_beats_ctrl.sum())}")

    # ---------------- reproduction of idea 247 at the incumbent
    say("\n=== REPRODUCTION: theta = incumbent on U56 vs idea 247's published ISFIX0.8 ===")
    inc = G[(G.panel == "U56") & (G.incumbent)].sort_values("bps")
    pub = {10: (0.11049650448372206, 1.2200874757247075, -0.1549132346464951),
           25: (0.10760182432915188, 1.190588906883643, -0.16047242278606977)}
    for _, r in inc.iterrows():
        c, s, d = pub[int(r.bps)]
        say(f"  {int(r.bps)} bps  CAGR {r.CAGR:.6f} (pub {c:.6f}, d {r.CAGR-c:+.2e})  "
            f"Sharpe {r.Sharpe:.6f} (pub {s:.6f}, d {r.Sharpe-s:+.2e})  "
            f"MaxDD {r.MaxDD:.6f} (pub {d:.6f}, d {r.MaxDD-d:+.2e})")
        assert abs(r.Sharpe - s) < 1e-9 and abs(r.CAGR - c) < 1e-9, "REPRODUCTION FAILED"
    say("  idea 247's candidate reproduced to machine precision — the sweep below is the "
        "same object, re-parameterised.")

    # ---------------- THE ANSWER: contiguous 4b interval around the incumbent
    say("\n=== 4b INTERVAL IN VOL UNITS (the queue's question) ===")
    irows = []
    for k in PANELS:
        for bps in RUNGS:
            sub = G[(G.panel == k) & (~G.ref) & (G.bps == bps)].sort_values("theta")
            th = sub.theta.values
            lo, hi, wid, npts, anchor_ok = contiguous_interval(th, sub.pass4b.values, INCUMBENT)
            lo8, hi8, wid8, npts8, anchor_ok8 = contiguous_interval(
                th, (sub.pass4b & sub.beats_ctrl).values, INCUMBENT)
            # OOS-only 4b (bars re-read on 2017+ against SPY OOS)
            px, cols = PX[k]
            win = px.index[260:]
            woos = win[win >= OOS_START]
            mspy_o = mstats(px["SPY"].pct_change().fillna(0.0).reindex(woos))
            ok_o = []
            for _, rr in sub.iterrows():
                mo = mstats(RET[(k, rr.arm, bps)].reindex(woos))
                ok_o.append(mo["Sharpe"] > mspy_o["Sharpe"]
                            and mo["MaxDD"] >= 0.60 * mspy_o["MaxDD"]
                            and mo["CAGR"] >= 0.70 * mspy_o["CAGR"])
            loo, hio, wido, nptso, anchor_o = contiguous_interval(th, ok_o, INCUMBENT)
            smax = sub.Sharpe.max()
            pf = float((sub.Sharpe >= smax - 0.05).mean())
            inc_row = sub[sub.incumbent].iloc[0]
            d_lo = INCUMBENT - lo if anchor_ok else np.nan
            d_hi = hi - INCUMBENT if anchor_ok else np.nan
            irows.append(dict(
                panel=k, bps=bps, incumbent=INCUMBENT,
                inc_pass4b=bool(inc_row.pass4b), inc_binding_bar=inc_row.binding_bar,
                inc_CAGR_margin=inc_row.CAGR_margin, inc_DD_margin=inc_row.DD_margin,
                inc_H1_margin=inc_row.H1_margin, inc_H2_margin=inc_row.H2_margin,
                lo=lo, hi=hi, width_vol_pts=wid, n_points=npts, steps=wid / STEP,
                dist_to_lo=d_lo, dist_to_hi=d_hi,
                nearest_edge=min(d_lo, d_hi) if anchor_ok else np.nan,
                nearest_edge_frac=(min(d_lo, d_hi) / wid) if (anchor_ok and wid > 0) else np.nan,
                n_pass4b_total=int(sub.pass4b.sum()), n_theta=len(sub),
                bc_lo=lo8, bc_hi=hi8, bc_width=wid8, bc_points=npts8,
                oos_lo=loo, oos_hi=hio, oos_width=wido, oos_points=nptso,
                oos_inc_pass=bool(anchor_o),
                Sharpe_range=float(sub.Sharpe.max() - sub.Sharpe.min()), plateau_frac=pf,
                n_pass4a=int(sub.pass4a.sum())))
    IV = pd.DataFrame(irows)
    IV.to_csv(OUT / f"{STAMP}.interval.csv", index=False)
    say(IV[["panel", "bps", "inc_pass4b", "inc_binding_bar", "lo", "hi", "width_vol_pts",
            "n_points", "nearest_edge", "nearest_edge_frac", "oos_lo", "oos_hi", "oos_width",
            "oos_inc_pass", "bc_lo", "bc_hi", "bc_width", "n_pass4b_total", "n_pass4a",
            "plateau_frac", "Sharpe_range"]].to_string(index=False,
                                                       float_format=lambda x: f"{x:.4f}"))

    # ---------------- WHAT THE FAR END OF THE INTERVAL ACTUALLY IS
    say("\n=== DEGENERACY CHECK: what is the book at the top of the 4b interval? ===")
    say("(a theta above the vol distribution arms almost no days, so the book -> EW_ALL; if "
        "EW_ALL itself passed 4b the interval width would be meaningless)")
    for k in PANELS:
        for bps in RUNGS:
            ew = G[(G.panel == k) & (G.arm == "EWALL") & (G.bps == bps)].iloc[0]
            fails = [b for b in ("H1_margin", "H2_margin", "DD_margin", "CAGR_margin")
                     if ew[b] <= 0]
            sub = G[(G.panel == k) & (~G.ref) & (G.bps == bps)].sort_values("theta")
            iv = IV[(IV.panel == k) & (IV.bps == bps)].iloc[0]
            top = sub[sub.theta == iv.hi] if iv.hi == iv.hi else sub.iloc[0:0]
            bc = sub[sub.dSharpe_vs_ctrl > 0]
            say(f"  {k:9s} {bps:2d}bps  EW_ALL (never armed): 4b {'PASS' if ew.pass4b else 'FAIL'}"
                f" — failing bars {fails if fails else 'none'}; DD {ew.MaxDD:.2%} vs cap "
                f"{0.60*SPYM[k]['MaxDD']:.2%} (margin {ew.DD_margin:+.4f}), CAGR margin "
                f"{ew.CAGR_margin:+.4f}")
            if len(top):
                t0 = top.iloc[0]
                say(f"             top of the 4b interval theta={t0.theta:.3f}: armed "
                    f"{int(t0.armed_days)} of {len(PX[k][0].index[260:])} days "
                    f"({t0.armed_share:.2%}), "
                    f"DD {t0.MaxDD:.2%}, dSharpe vs matched control {t0.dSharpe_vs_ctrl:+.4f}")
            if len(bc):
                say(f"             beats its matched control on theta in "
                    f"[{bc.theta.min():.3f}, {bc.theta.max():.3f}] "
                    f"({len(bc)}/{len(sub)} points)")

    say("\nU56 full-sample sweep every 4th theta (the panel the candidate lives on, 10 bps):")
    sub = G[(G.panel == "U56") & (~G.ref) & (G.bps == 10)].sort_values("theta")
    show = pd.concat([sub.iloc[::4], sub[sub.incumbent]]).drop_duplicates().sort_values("theta")
    say(show[["theta", "armed_share", "armed_share_IS", "armed_share_OOS", "CAGR", "Sharpe",
              "MaxDD", "H1", "H2", "CAGR_margin", "DD_margin", "dSharpe_vs_ctrl",
              "pass4a", "pass4b", "incumbent"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\nU56 10 bps, CLOSE-UP around the incumbent (every grid point 0.16 -> 0.28):")
    cu = sub[(sub.theta >= 0.16) & (sub.theta <= 0.28)]
    say(cu[["theta", "armed_share", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "CAGR_margin",
            "dSharpe_vs_ctrl", "pass4b", "incumbent"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # local slope of the binding bar at the incumbent
    for k in PANELS:
        for bps in RUNGS:
            s2 = G[(G.panel == k) & (~G.ref) & (G.bps == bps)].sort_values("theta")
            i = int(np.argmin(np.abs(s2.theta.values - INCUMBENT)))
            j0, j1 = max(0, i - 2), min(len(s2) - 1, i + 2)
            dth = s2.theta.values[j1] - s2.theta.values[j0]
            dc = s2.CAGR.values[j1] - s2.CAGR.values[j0]
            say(f"  local dCAGR/dtheta at the incumbent, {k} {bps}bps: "
                f"{100*dc/dth:+.2f} pp of CAGR per 1.00 vol point "
                f"({100*dc/dth*0.01:+.3f} pp per 0.01 vol point)")

    # ---------------- RULE 8
    say("\n=== RULE 8 WALK-FORWARD (theta chosen on IS <= 2016-12-31 by IS Sharpe) ===")
    wrows = []
    for k in PANELS:
        px, cols = PX[k]
        win = px.index[260:]
        wis = win[win <= IS_END]
        woos = win[win >= OOS_START]
        mspy_o = mstats(px["SPY"].pct_change().fillna(0.0).reindex(woos))
        for bps in RUNGS:
            sub = G[(G.panel == k) & (~G.ref) & (G.bps == bps)]
            pick = sub.loc[sub.IS_Sharpe.idxmax()]
            mo = mstats(RET[(k, pick.arm, bps)].reindex(woos))
            mco = mstats(CRET[(k, pick.arm, bps)].reindex(woos))
            mv2 = mstats(RET[(k, "BAND3DG", bps)].reindex(woos))
            mew = mstats(RET[(k, "EWALL", bps)].reindex(woos))
            minc = mstats(RET[(k, f"{INCUMBENT:.6f}", bps)].reindex(woos))
            mcinc = mstats(CRET[(k, f"{INCUMBENT:.6f}", bps)].reindex(woos))
            wrows.append(dict(
                panel=k, bps=bps, IS_pick_theta=pick.theta, IS_Sharpe=pick.IS_Sharpe,
                pick_minus_incumbent=pick.theta - INCUMBENT,
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                OOS_ctrl_Sharpe=mco["Sharpe"], OOS_RULESV2_Sharpe=mv2["Sharpe"],
                OOS_RULESV2_CAGR=mv2["CAGR"], OOS_RULESV2_MaxDD=mv2["MaxDD"],
                OOS_EWALL_Sharpe=mew["Sharpe"],
                OOS_SPY_CAGR=mspy_o["CAGR"], OOS_SPY_Sharpe=mspy_o["Sharpe"],
                OOS_SPY_MaxDD=mspy_o["MaxDD"],
                INC_OOS_CAGR=minc["CAGR"], INC_OOS_Sharpe=minc["Sharpe"],
                INC_OOS_MaxDD=minc["MaxDD"], INC_OOS_ctrl_Sharpe=mcinc["Sharpe"],
                pick_beats_ctrl_OOS=mo["Sharpe"] > mco["Sharpe"],
                pick_beats_SPY_OOS=mo["Sharpe"] > mspy_o["Sharpe"],
                pick_beats_RULESV2_OOS=mo["Sharpe"] > mv2["Sharpe"],
                pick_OOS_4b=(mo["Sharpe"] > mspy_o["Sharpe"]
                             and mo["MaxDD"] >= 0.60 * mspy_o["MaxDD"]
                             and mo["CAGR"] >= 0.70 * mspy_o["CAGR"]),
                inc_OOS_4b=(minc["Sharpe"] > mspy_o["Sharpe"]
                            and minc["MaxDD"] >= 0.60 * mspy_o["MaxDD"]
                            and minc["CAGR"] >= 0.70 * mspy_o["CAGR"])))
    W = pd.DataFrame(wrows)
    W.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    say(W[["panel", "bps", "IS_pick_theta", "pick_minus_incumbent", "OOS_CAGR", "OOS_Sharpe",
           "OOS_MaxDD", "OOS_ctrl_Sharpe", "OOS_RULESV2_Sharpe", "OOS_SPY_Sharpe",
           "pick_beats_ctrl_OOS", "pick_beats_SPY_OOS", "pick_OOS_4b", "INC_OOS_Sharpe",
           "inc_OOS_4b"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\nIS-chosen theta lands inside the FULL-sample 4b interval in "
        f"{sum(1 for _, r in W.iterrows() for _, q in IV.iterrows() if q.panel == r.panel and q.bps == r.bps and q.lo <= r.IS_pick_theta <= q.hi)}"
        f"/{len(W)} cells")
    say(f"rule-8 picks clearing 4b OOS: {int(W.pick_OOS_4b.sum())}/{len(W)}   "
        f"beating their matched control OOS: {int(W.pick_beats_ctrl_OOS.sum())}/{len(W)}   "
        f"beating live RULES v2 OOS: {int(W.pick_beats_RULESV2_OOS.sum())}/{len(W)}")
    say(f"incumbent theta clearing 4b OOS: {int(W.inc_OOS_4b.sum())}/{len(W)}")

    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_console) + "\n")
    print(f"\nwrote {STAMP}.grid.csv .interval.csv .walkforward.csv .console.txt")


if __name__ == "__main__":
    main()

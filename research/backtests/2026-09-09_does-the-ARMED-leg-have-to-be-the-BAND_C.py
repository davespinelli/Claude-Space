#!/usr/bin/env python3
"""Idea 465 — DOES THE ARMED LEG HAVE TO BE THE BAND?

Idea 247's 4b KEEP-candidate is a CONDITIONAL book: hold every priced name at 75%/N of NAV,
and on days when SPY's 20-day realised vol is at or above a FIXED threshold theta (the q-th
quantile of SPY vol20 over 2009..2016 only, frozen) de-gross into RULES v2's 200d +/-3% band
instead; gated weight goes to cash, never re-spread.  It beats its MATCHED-REALISED-GROSS
static control by +0.0975 Sharpe full sample (+0.0741 OOS) on U56, which is why it is a
candidate at all.  But the ARMED leg was never varied: it was RULES v2's band3-dg by
inheritance, not by test.

THE QUESTION (queue idea 465).  Price the same fixed-threshold arming with other armed legs —
MA200-dg, BAND6-dg, ABS-dg — and, decisively, with a PLAIN GROSS CUT to the same realised
exposure.  If the plain gross cut matches the band, the edge is DE-GROSSING IN HIGH VOL and
the band is decorative.

THE DECOMPOSITION (the whole point of this run).  Idea 247's +0.0975 is measured against a
STATIC control (EW_ALL at a constant nominal gross, matched to the arm's mean realised gross
over the window).  That control differs from the arm in TWO ways at once: it never times its
exposure to vol, and it never selects names.  So split it, exactly, with a third book:

    CTRL_TIMED(L)  = EW_ALL at 0.75 on disarmed days, EW_ALL at a REDUCED nominal gross on
                     armed days, the reduction solved so its MEAN REALISED GROSS equals arm
                     L's on the same window.  Same exposure, same timing, NO name selection.

    total edge       = S(arm)          - S(CTRL_STATIC)      <- idea 247's +0.0975
    timing edge      = S(CTRL_TIMED)   - S(CTRL_STATIC)      <- de-grossing in high vol
    composition edge = S(arm)          - S(CTRL_TIMED)       <- what the LEG earns
    total = timing + composition, identically.

`GROSSCUT` is carried as a first-class ARM as well (it is CTRL_TIMED(BAND3DG) by
construction — asserted, gate G5), so it is scored on 4a/4b and offered to the rule-8 chooser
on equal terms with the four gate legs.

PRE-REGISTRATION (fixed before any number was read):
  * ARMED LEGS (5).  All de-grossed at nominal 0.75, gated weight to CASH, never re-spread:
      BAND3DG  RULES v2's 200d MA +3%/-3% band with hysteresis (`baseline.band_state`, 0.03)
               — idea 247's incumbent, asserted identical to `baseline.rules_v2_weights` (G2).
      BAND6DG  the same object at 0.06.
      MA200DG  the plain 200d MA gate, NO hysteresis (`band_state` at band=0.0, so the
               warm-up convention is identical; asserted equal to px>ma after warm-up, G6).
      ABSDG    12-month ABSOLUTE momentum, px_t > px_{t-252}.  The queue names "ABS-dg"
               without defining it; this is the definition used here, stated for the record.
      GROSSCUT no cross-sectional gate at all — EW_ALL at the reduced nominal gross that
               matches BAND3DG's mean realised gross at the same q.
    The DISARMED leg is EW_ALL at 0.75 for every arm, exactly as in idea 247.
  * ARMING.  theta = q-th quantile of SPY vol20 over IS (<= 2016-12-31) only, then FROZEN
    (idea 247's ISFIX convention, the one whose IS/OOS coverage is matched by construction).
    The threshold depends on q ALONE, so every leg is armed on exactly the same days —
    the leg is the only thing that varies.  q in {0.60, 0.70, 0.80, 0.90}; q=0.80 is idea
    247's candidate.
  * TWO tuned parameters, no more: the ARMED LEG and q.  Panel (U56, B136, SMALL439) and
    cost rung (10, 25 bps) are REPORTED at every level, never chosen.
        arms (25 per panel per rung) = 5 legs x 4 q, plus 5 unconditional references
                                       (EWALL always; each gate leg always, BAND3DG-always
                                       being the live RULES v2 book)
        150 grid points in total, ALL reported.
  * CONTROLS.  Every arm gets CTRL_STATIC (idea 247's convention) and every conditional arm
    also gets CTRL_TIMED, each solved by fixed-point iteration on nominal gross to 1e-9 of
    the arm's own mean realised gross; the achieved match is printed.  Matching on the FULL
    window uses OOS data, so a second pair of controls is solved on the IS window ONLY and
    frozen — the OOS comparisons in the rule-8 section use those, and are leak-free.
  * BOTH KEEP PATHS on every grid point: 4a vs the live RULES v2 book on the same panel and
    window; 4b vs SPY (Sharpe in both halves, MaxDD <= 0.60x SPY's, CAGR >= 0.70x SPY's).
  * RULE 8.  (leg, q) chosen by IS Sharpe on <= 2016-12-31; 2017-01-01.. read once, reported
    against SPY, the live RULES v2 book, and the IS-matched static and timed controls.
  * UNCERTAINTY.  The headline decomposition (U56, q=0.80, 10 bps) is block-bootstrapped
    (21-day blocks, 2000 draws, seed 465) on the daily return differences.

SURVIVORSHIP (carried from idea 54): B136 and SMALL439 are CURRENT-constituent lists, so
their levels are biased upward.  U56 is a fixed ETF/mega-cap list and is the least biased;
idea 247's candidate is a U56 book, so read U56 first.  Only WITHIN-panel arm-minus-control
contrasts are load-bearing.

Costs 10/25 bps per unit turnover; weights decided at close t applied at close t+1
(PROTOCOL 2).  Deterministic, no network.  Writes .grid.csv, .decomp.csv, .walkforward.csv,
.boot.csv, .console.txt.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, band_state, rules_v2_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, rebalance_mask, metrics  # noqa

STAMP = "2026-09-09_does-the-ARMED-leg-have-to-be-the-BAND_C"
OUT = ROOT / "research" / "backtests"
FREQ = "W"
GROSS = 0.75
RUNGS = [10, 25]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
QS = [0.60, 0.70, 0.80, 0.90]
LEGS = ["BAND3DG", "BAND6DG", "MA200DG", "ABSDG", "GROSSCUT"]
GATE_LEGS = ["BAND3DG", "BAND6DG", "MA200DG", "ABSDG"]
PANELS = ["U56", "B136", "SMALL439"]
HEAD_Q = 0.80          # idea 247's candidate
BOOT_N, BOOT_BLK, SEED = 2000, 21, 465

_console = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); _console.append(s)


# ---------------------------------------------------------------- engine twin
def fast_backtest(px, weights, freq=FREQ):
    rets = px.pct_change().fillna(0.0).values
    W = weights.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    n = len(px)
    A = np.cumprod(1.0 + rets, axis=0)
    A = np.vstack([np.ones((1, rets.shape[1])), A[:-1]])
    port = np.zeros(n); turn = np.zeros(n); gross = np.zeros(n)
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
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


# ---------------------------------------------------------------- books
def ew_weights(px, cols, g=GROSS):
    p = px[cols]
    e = pd.DataFrame(1.0, index=p.index, columns=p.columns).where(p.notna(), 0.0)
    w = g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return w.reindex(columns=px.columns).fillna(0.0)


def gate_mask(px, cols, leg):
    """Per-name boolean: True = the leg HOLDS the name.  All legs are de-grossing gates."""
    p = px[cols]
    if leg == "BAND3DG":
        m = band_state(p, 0.03)
    elif leg == "BAND6DG":
        m = band_state(p, 0.06)
    elif leg == "MA200DG":
        m = band_state(p, 0.0)              # plain 200d MA gate, no hysteresis
    elif leg == "ABSDG":
        m = (p > p.shift(252)) & p.shift(252).notna()   # 12m absolute momentum
    else:
        raise ValueError(leg)
    return m.reindex(columns=px.columns).fillna(False)


def leg_weights(px, cols, leg, g=GROSS):
    return ew_weights(px, cols, g).where(gate_mask(px, cols, leg), 0.0)


def cond_book(px, armed, W_armed, W_dis):
    a = armed.reindex(px.index).fillna(False)
    return W_armed.where(a, axis=0).fillna(0.0) + W_dis.where(~a, axis=0).fillna(0.0)


def spy_vol20(px):
    return px["SPY"].pct_change().rolling(20).std() * np.sqrt(252)


def arming(px, q, is_end=IS_END):
    """ISFIX: theta = q-th quantile of SPY vol20 over IS only, frozen thereafter (causal)."""
    v = spy_vol20(px)
    thr = float(v.loc[:is_end].dropna().quantile(q))
    return (v >= thr).fillna(False), thr


def panels():
    out = {}
    u = load_universe(); out["U56"] = (u, [c for c in u.columns])
    b = load_universe(broad=True); out["B136"] = (b, [c for c in b.columns])
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    sm = sm[[c for c in sm.columns if c == "SPY" or c not in bad]]
    out["SMALL439"] = (sm, [c for c in sm.columns if c != "SPY"])   # SPY = benchmark only
    return out


# ------------------------------------------------------- matched-gross solvers
def _solve(build, target, win, tol=1e-10, iters=14):
    """Solve nominal gross g so that mean realised gross on `win` == target.  Mean realised
    gross is smooth and monotone in g (affine to a very good approximation for the timed
    book, where disarmed days sit at 0.75 whatever g is), so SECANT converges in a few
    evaluations; bisection on [0, 1.5], 45 steps, is the fallback."""
    def f(g):
        r = build(g)
        return float(r["gross"].reindex(win).mean()), r
    g0 = float(np.clip(target, 1e-6, 1.5)); y0, r0 = f(g0)
    if abs(y0 - target) < tol:
        return g0, y0, r0
    g1 = float(np.clip(g0 * 1.05 + 1e-3, 1e-6, 1.5)); y1, r1 = f(g1)
    for _ in range(iters):
        if abs(y1 - target) < tol:
            return g1, y1, r1
        if y1 == y0:
            break
        g2 = g1 - (y1 - target) * (g1 - g0) / (y1 - y0)
        g2 = float(np.clip(g2, 1e-6, 1.5))
        g0, y0, r0 = g1, y1, r1
        g1 = g2; y1, r1 = f(g1)
    if abs(y1 - target) < 1e-9:
        return g1, y1, r1
    lo, hi = 0.0, 1.5                                    # bisection fallback
    for _ in range(45):
        mid = 0.5 * (lo + hi); got, r = f(mid)
        if got < target: lo = mid
        else: hi = mid
    g = 0.5 * (lo + hi); got, r = f(g)
    assert abs(got - target) < 1e-8, f"gross match failed: {got} vs {target}"
    return g, got, r


def solve_static(px, cols, target, win):
    return _solve(lambda g: fast_backtest(px, ew_weights(px, cols, g)), target, win)


def solve_timed(px, cols, armed, target, win):
    Wd = ew_weights(px, cols, GROSS)
    return _solve(
        lambda g: fast_backtest(px, cond_book(px, armed, ew_weights(px, cols, g), Wd)),
        target, win)


def block_boot(d, n=BOOT_N, blk=BOOT_BLK, seed=SEED):
    """Block bootstrap of the annualised Sharpe of a daily difference series."""
    x = np.asarray(d, float); T = len(x)
    nb = int(np.ceil(T / blk))
    rng = np.random.default_rng(seed)
    starts = rng.integers(0, T - blk, size=(n, nb))
    idx = (starts[:, :, None] + np.arange(blk)[None, None, :]).reshape(n, -1)[:, :T]
    s = x[idx]
    mu, sd = s.mean(axis=1), s.std(axis=1, ddof=1)
    return np.sqrt(252) * mu / np.where(sd == 0, np.nan, sd)


# ---------------------------------------------------------------------- main
def main():
    PX = panels()

    # ---------------- GATES
    say("=== GATES ===")
    upx, ucols = PX["U56"]
    st = upx.index[260]
    w2 = rules_v2_weights(upx)
    e_res = engine_backtest(upx, w2, cost_bps=10, freq=FREQ)
    f_res = fast_backtest(upx, w2)
    g1r = float(np.abs((net(f_res, 10) - e_res["returns"]).loc[st:].values).max())
    g1t = float(np.abs((f_res["turnover"] - e_res["turnover"]).loc[st:].values).max())
    say(f"G1 fast_backtest vs engine.backtest (from {st.date()})  max|d returns| = {g1r:.3e}"
        f"  max|d turnover| = {g1t:.3e}")
    assert g1r < 1e-12 and g1t < 1e-12, "G1 FAILED"
    g2 = float(np.abs(leg_weights(upx, ucols, "BAND3DG").values - w2.values).max())
    say(f"G2 leg_weights(BAND3DG, 0.75) == baseline.rules_v2_weights   max|diff| = {g2:.3e}")
    assert g2 == 0.0, "G2 FAILED"
    a_all = pd.Series(True, index=upx.index); a_none = pd.Series(False, index=upx.index)
    Wd = ew_weights(upx, ucols); Wb = leg_weights(upx, ucols, "BAND3DG")
    g3 = float(np.abs(cond_book(upx, a_all, Wb, Wd).values - Wb.values).max())
    g4 = float(np.abs(cond_book(upx, a_none, Wb, Wd).values - Wd.values).max())
    say(f"G3 conditional book with armed==ALL  == the armed leg   max|diff| = {g3:.3e}")
    say(f"G4 conditional book with armed==NONE == EW_ALL          max|diff| = {g4:.3e}")
    assert g3 == 0.0 and g4 == 0.0, "G3/G4 FAILED"
    ma = upx[ucols] > upx[ucols].rolling(200).mean()
    gm = gate_mask(upx, ucols, "MA200DG")[ucols]
    after = upx.index >= upx.index[260]
    g6 = int((gm.loc[after].values != ma.loc[after].fillna(False).values).sum())
    say(f"G6 MA200DG (band_state at 0.0) == plain px>ma after warm-up   disagreements = {g6}")
    assert g6 == 0, "G6 FAILED"

    # ---------------- ARMING (one threshold per q; identical for every leg)
    say("\n=== ARMING (ISFIX: theta = q-th quantile of SPY vol20 on IS <= 2016-12-31, frozen) ===")
    arows = []
    for k in PANELS:
        px, cols = PX[k]
        win = px.index[260:]
        wis = win[win <= IS_END]; woos = win[win >= OOS_START]
        for q in QS:
            a, thr = arming(px, q)
            arows.append(dict(panel=k, q=q, theta=thr,
                              IS_armed_share=float(a.reindex(wis).mean()),
                              OOS_armed_share=float(a.reindex(woos).mean()),
                              armed_days=int(a.reindex(win).sum()), days=len(win)))
    A = pd.DataFrame(arows)
    say(A.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------- GRID
    say("\n=== GRID: 25 arms x 3 panels x 2 rungs = 150 points, ALL reported ===")
    rows, RET, CS, CT, CSis, CTis = [], {}, {}, {}, {}, {}
    for k in PANELS:
        px, cols = PX[k]
        win = px.index[260:]
        wis = win[win <= IS_END]
        spy = px["SPY"].pct_change().fillna(0.0).reindex(win)
        mspy = mstats(spy)
        say(f"\n--- {k}: {len(cols)} held names, {win[0].date()} -> {win[-1].date()} "
            f"({len(win)} days) | SPY {mspy['CAGR']:.2%} / {mspy['Sharpe']:.4f} / "
            f"{mspy['MaxDD']:.2%}, halves {mspy['H1']:.3f}/{mspy['H2']:.3f}")
        Wd = ew_weights(px, cols, GROSS)
        base_v2 = {b: mstats(net(fast_backtest(px, leg_weights(px, cols, "BAND3DG")), b)
                             .reindex(win)) for b in RUNGS}

        # conditional arms
        for q in QS:
            armed, thr = arming(px, q)
            # BAND3DG first: GROSSCUT is defined by its realised gross
            b3 = fast_backtest(px, cond_book(px, armed, leg_weights(px, cols, "BAND3DG"), Wd))
            g_b3 = float(b3["gross"].reindex(win).mean())
            gc_nom, gc_ach, gc_res = solve_timed(px, cols, armed, g_b3, win)
            for leg in LEGS:
                if leg == "BAND3DG":
                    r0 = b3
                elif leg == "GROSSCUT":
                    r0 = gc_res
                else:
                    r0 = fast_backtest(px, cond_book(px, armed, leg_weights(px, cols, leg), Wd))
                gmean = float(r0["gross"].reindex(win).mean())
                gmean_is = float(r0["gross"].reindex(wis).mean())
                turn_yr = float(r0["turnover"].reindex(win).sum()) / (len(win) / 252)
                a_gross = float(r0["gross"].reindex(win)[armed.reindex(win).values].mean())
                sn, sa, s_res = solve_static(px, cols, gmean, win)
                tn, ta, t_res = solve_timed(px, cols, armed, gmean, win)
                sn_i, sa_i, s_res_i = solve_static(px, cols, gmean_is, wis)
                tn_i, ta_i, t_res_i = solve_timed(px, cols, armed, gmean_is, wis)
                if leg == "GROSSCUT":                                   # G5 (identity)
                    g5 = float(np.abs(r0["returns0"].values - t_res["returns0"].values).max())
                    g5g = abs(gmean - g_b3)
                    assert g5 < 1e-8 and g5g < 1e-8, f"G5 FAILED {g5} {g5g}"
                    if k == "U56" and q == HEAD_Q:
                        say(f"G5 GROSSCUT@{q:.2f} IS its own timed control (and matches "
                            f"BAND3DG's realised gross): max|d returns| = {g5:.3e}, "
                            f"|d gross| = {g5g:.3e}")
                name = f"{leg}@{q:.2f}"
                for bps in RUNGS:
                    r = net(r0, bps).reindex(win)
                    cs = net(s_res, bps).reindex(win); ct = net(t_res, bps).reindex(win)
                    RET[(k, name, bps)] = r
                    CS[(k, name, bps)] = cs; CT[(k, name, bps)] = ct
                    CSis[(k, name, bps)] = net(s_res_i, bps).reindex(win)
                    CTis[(k, name, bps)] = net(t_res_i, bps).reindex(win)
                    m, ms, mt = mstats(r), mstats(cs), mstats(ct)
                    mv2 = base_v2[bps]
                    p4a = (m["H1"] > mv2["H1"] and m["H2"] > mv2["H2"]
                           and m["MaxDD"] >= mv2["MaxDD"])
                    p4b = (m["H1"] > mspy["H1"] and m["H2"] > mspy["H2"]
                           and m["MaxDD"] >= 0.60 * mspy["MaxDD"]
                           and m["CAGR"] >= 0.70 * mspy["CAGR"])
                    rows.append(dict(
                        panel=k, arm=name, leg=leg, q=q, bps=bps, theta=thr,
                        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m["H1"],
                        H2=m["H2"], gross=gmean, armed_gross=a_gross, turnover_yr=turn_yr,
                        stat_nom=sn, stat_gross=sa, stat_Sharpe=ms["Sharpe"],
                        stat_CAGR=ms["CAGR"], stat_MaxDD=ms["MaxDD"],
                        timed_nom=tn, timed_gross=ta, timed_Sharpe=mt["Sharpe"],
                        timed_CAGR=mt["CAGR"], timed_MaxDD=mt["MaxDD"],
                        total_edge=m["Sharpe"] - ms["Sharpe"],
                        timing_edge=mt["Sharpe"] - ms["Sharpe"],
                        composition_edge=m["Sharpe"] - mt["Sharpe"],
                        dCAGR_vs_static=m["CAGR"] - ms["CAGR"],
                        dCAGR_vs_timed=m["CAGR"] - mt["CAGR"],
                        pass4a=p4a, pass4b=p4b,
                        pass4b_beats_static=bool(p4b and m["Sharpe"] > ms["Sharpe"]),
                        pass4b_beats_timed=bool(p4b and m["Sharpe"] > mt["Sharpe"])))

        # unconditional references
        for ref in ["EWALL"] + [f"ALW_{g}" for g in GATE_LEGS]:
            W = Wd if ref == "EWALL" else leg_weights(px, cols, ref[4:])
            r0 = fast_backtest(px, W)
            gmean = float(r0["gross"].reindex(win).mean())
            gmean_is = float(r0["gross"].reindex(wis).mean())
            turn_yr = float(r0["turnover"].reindex(win).sum()) / (len(win) / 252)
            sn, sa, s_res = solve_static(px, cols, gmean, win)
            sn_i, sa_i, s_res_i = solve_static(px, cols, gmean_is, wis)
            for bps in RUNGS:
                r = net(r0, bps).reindex(win); cs = net(s_res, bps).reindex(win)
                RET[(k, ref, bps)] = r; CS[(k, ref, bps)] = cs; CT[(k, ref, bps)] = cs
                CSis[(k, ref, bps)] = net(s_res_i, bps).reindex(win)
                CTis[(k, ref, bps)] = CSis[(k, ref, bps)]
                m, ms = mstats(r), mstats(cs)
                mv2 = base_v2[bps]
                p4a = (m["H1"] > mv2["H1"] and m["H2"] > mv2["H2"] and m["MaxDD"] >= mv2["MaxDD"])
                p4b = (m["H1"] > mspy["H1"] and m["H2"] > mspy["H2"]
                       and m["MaxDD"] >= 0.60 * mspy["MaxDD"] and m["CAGR"] >= 0.70 * mspy["CAGR"])
                rows.append(dict(
                    panel=k, arm=ref, leg=ref, q=np.nan, bps=bps, theta=np.nan,
                    CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m["H1"], H2=m["H2"],
                    gross=gmean, armed_gross=np.nan, turnover_yr=turn_yr,
                    stat_nom=sn, stat_gross=sa, stat_Sharpe=ms["Sharpe"], stat_CAGR=ms["CAGR"],
                    stat_MaxDD=ms["MaxDD"], timed_nom=np.nan, timed_gross=np.nan,
                    timed_Sharpe=np.nan, timed_CAGR=np.nan, timed_MaxDD=np.nan,
                    total_edge=m["Sharpe"] - ms["Sharpe"], timing_edge=np.nan,
                    composition_edge=np.nan, dCAGR_vs_static=m["CAGR"] - ms["CAGR"],
                    dCAGR_vs_timed=np.nan, pass4a=p4a, pass4b=p4b,
                    pass4b_beats_static=bool(p4b and m["Sharpe"] > ms["Sharpe"]),
                    pass4b_beats_timed=bool(p4b and m["Sharpe"] > ms["Sharpe"])))

    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    say("\nFULL GRID (all 150 points):")
    say(G[["panel", "arm", "bps", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "gross",
           "armed_gross", "turnover_yr", "stat_Sharpe", "timed_Sharpe", "total_edge",
           "timing_edge", "composition_edge", "pass4a", "pass4b", "pass4b_beats_timed"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\nmatched-gross accuracy: max|target-achieved| static "
        f"{float((G.gross - G.stat_gross).abs().max()):.3e}  timed "
        f"{float((G.gross - G.timed_gross).abs().max(skipna=True)):.3e}")
    say(f"4a passes {int(G.pass4a.sum())}/{len(G)}   4b passes {int(G.pass4b.sum())}/{len(G)}"
        f"   4b AND beats its TIMED control {int(G.pass4b_beats_timed.sum())}/{len(G)}"
        f"   4b AND beats its STATIC control {int(G.pass4b_beats_static.sum())}/{len(G)}")

    # ---------------- THE DECOMPOSITION
    C = G[G.leg.isin(LEGS)].copy()
    say("\n=== DECOMPOSITION: total = timing + composition (Sharpe), 120 conditional points ===")
    say(f"identity check max|total - (timing+composition)| = "
        f"{float((C.total_edge - C.timing_edge - C.composition_edge).abs().max()):.3e}")
    piv = C.groupby(["panel", "leg"]).agg(
        n=("Sharpe", "size"), mean_total=("total_edge", "mean"),
        mean_timing=("timing_edge", "mean"), mean_comp=("composition_edge", "mean"),
        comp_pos=("composition_edge", lambda s: int((s > 0).sum())),
        mean_gross=("gross", "mean"), mean_armed_gross=("armed_gross", "mean")).reset_index()
    say(piv.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\nPer-leg pooled over all 3 panels x 4 q x 2 rungs (24 cells each):")
    for leg in LEGS:
        s = C[C.leg == leg]
        say(f"  {leg:9s} total {s.total_edge.mean():+.4f}  timing {s.timing_edge.mean():+.4f}"
            f"  composition {s.composition_edge.mean():+.4f}"
            f"  (comp>0 in {int((s.composition_edge>0).sum())}/{len(s)},"
            f" median {s.composition_edge.median():+.4f})")
    # A timing/total ratio is only interpretable where the total edge is positive (the
    # denominator crosses zero across panels, so no pooled ratio is quoted).
    pos = C[(C.total_edge > 0) & (C.leg != "GROSSCUT")].copy()
    pos["share"] = pos.timing_edge / pos.total_edge
    say(f"\nTIMING SHARE OF THE TOTAL EDGE, per cell, on the {len(pos)} gate-leg cells with a "
        f"POSITIVE total edge: median {pos.share.median():.1%}, mean {pos.share.mean():.1%}, "
        f"IQR {pos.share.quantile(0.25):.1%}-{pos.share.quantile(0.75):.1%}; "
        f">=50% in {int((pos.share >= 0.5).sum())}/{len(pos)} cells, >=90% in "
        f"{int((pos.share >= 0.9).sum())}/{len(pos)}. (No pooled ratio is quoted: the "
        "denominator changes sign across panels.)")
    hd = C[(C.panel == "U56") & (C.q == HEAD_Q) & (C.bps == 10) & (C.leg == "BAND3DG")].iloc[0]
    say(f"HEADLINE CELL (U56, q=0.80, 10 bps): idea 247's +{hd.total_edge:.4f} splits into "
        f"{hd.timing_edge:+.4f} TIMING ({hd.timing_edge/hd.total_edge:.1%}) and "
        f"{hd.composition_edge:+.4f} COMPOSITION ({hd.composition_edge/hd.total_edge:.1%}).")
    C.to_csv(OUT / f"{STAMP}.decomp.csv", index=False)

    say("\nTHE HEADLINE CELL — idea 247's candidate (U56, q=0.80, 10 bps) and its four rivals:")
    H = G[(G.panel == "U56") & (G.q == HEAD_Q) & (G.bps == 10)]
    say(H[["arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "gross", "armed_gross",
           "turnover_yr", "stat_Sharpe", "timed_Sharpe", "total_edge", "timing_edge",
           "composition_edge", "pass4a", "pass4b"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------- BOOTSTRAP on the headline decomposition
    say(f"\n=== BLOCK BOOTSTRAP of the headline decomposition ({BOOT_N} draws, "
        f"{BOOT_BLK}-day blocks, seed {SEED}) ===")
    brows = []
    for leg in LEGS:
        nm = f"{leg}@{HEAD_Q:.2f}"
        r = RET[("U56", nm, 10)]
        for lbl, comp in (("composition (arm - timed ctrl)", CT[("U56", nm, 10)]),
                          ("total (arm - static ctrl)", CS[("U56", nm, 10)])):
            d = (r - comp).dropna()
            bs = block_boot(d.values)
            pt = float(np.sqrt(252) * d.mean() / d.std(ddof=1))
            brows.append(dict(arm=nm, contrast=lbl, point=pt,
                              lo5=float(np.nanpercentile(bs, 5)),
                              hi95=float(np.nanpercentile(bs, 95)),
                              frac_pos=float(np.mean(bs > 0))))
    B = pd.DataFrame(brows)
    B.to_csv(OUT / f"{STAMP}.boot.csv", index=False)
    say(B.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("(the bootstrapped quantity is the annualised Sharpe of the daily RETURN DIFFERENCE, "
        "not the difference of Sharpes; it tests whether the arm's excess over the control "
        "is distinguishable from zero.)")

    # ---------------- RULE 8
    say("\n=== RULE 8 WALK-FORWARD (leg and q chosen on IS Sharpe <= 2016-12-31; "
        "2017-01-01.. read once; OOS controls are the IS-MATCHED ones, so leak-free) ===")
    wrows = []
    cand = [f"{leg}@{q:.2f}" for leg in LEGS for q in QS]
    for k in PANELS:
        px, cols = PX[k]
        win = px.index[260:]
        wis = win[win <= IS_END]; woos = win[win >= OOS_START]
        spy_o = mstats(px["SPY"].pct_change().fillna(0.0).reindex(woos))
        for bps in RUNGS:
            iss = {nm: metrics(RET[(k, nm, bps)].reindex(wis))["Sharpe"] for nm in cand}
            pick = max(iss, key=iss.get)
            second = sorted(iss, key=iss.get, reverse=True)[1]
            mo = mstats(RET[(k, pick, bps)].reindex(woos))
            mso = mstats(CSis[(k, pick, bps)].reindex(woos))
            mto = mstats(CTis[(k, pick, bps)].reindex(woos))
            mv2 = mstats(RET[(k, "ALW_BAND3DG", bps)].reindex(woos))
            mew = mstats(RET[(k, "EWALL", bps)].reindex(woos))
            inc = f"BAND3DG@{HEAD_Q:.2f}"                # idea 247's candidate, read anyway
            mi = mstats(RET[(k, inc, bps)].reindex(woos))
            mti = mstats(CTis[(k, inc, bps)].reindex(woos))
            msi = mstats(CSis[(k, inc, bps)].reindex(woos))
            wrows.append(dict(
                panel=k, bps=bps, IS_pick=pick, IS_Sharpe=iss[pick], IS_second=second,
                IS_margin=iss[pick] - iss[second],
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                OOS_static_Sharpe=mso["Sharpe"], OOS_timed_Sharpe=mto["Sharpe"],
                OOS_comp_edge=mo["Sharpe"] - mto["Sharpe"],
                OOS_timing_edge=mto["Sharpe"] - mso["Sharpe"],
                OOS_RULESV2_Sharpe=mv2["Sharpe"], OOS_EWALL_Sharpe=mew["Sharpe"],
                OOS_SPY_CAGR=spy_o["CAGR"], OOS_SPY_Sharpe=spy_o["Sharpe"],
                OOS_SPY_MaxDD=spy_o["MaxDD"],
                pick_OOS_4b=(mo["Sharpe"] > spy_o["Sharpe"]
                             and mo["MaxDD"] >= 0.60 * spy_o["MaxDD"]
                             and mo["CAGR"] >= 0.70 * spy_o["CAGR"]),
                pick_beats_timed_OOS=mo["Sharpe"] > mto["Sharpe"],
                INC_OOS_CAGR=mi["CAGR"], INC_OOS_Sharpe=mi["Sharpe"], INC_OOS_MaxDD=mi["MaxDD"],
                INC_OOS_timed_Sharpe=mti["Sharpe"], INC_OOS_static_Sharpe=msi["Sharpe"],
                INC_OOS_comp_edge=mi["Sharpe"] - mti["Sharpe"],
                INC_OOS_timing_edge=mti["Sharpe"] - msi["Sharpe"],
                INC_OOS_4b=(mi["Sharpe"] > spy_o["Sharpe"]
                            and mi["MaxDD"] >= 0.60 * spy_o["MaxDD"]
                            and mi["CAGR"] >= 0.70 * spy_o["CAGR"])))
    W = pd.DataFrame(wrows)
    W.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    say(W[["panel", "bps", "IS_pick", "IS_Sharpe", "IS_second", "IS_margin", "OOS_CAGR",
           "OOS_Sharpe", "OOS_MaxDD", "OOS_static_Sharpe", "OOS_timed_Sharpe",
           "OOS_comp_edge", "OOS_timing_edge", "OOS_RULESV2_Sharpe", "OOS_SPY_Sharpe",
           "pick_OOS_4b", "pick_beats_timed_OOS"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\nidea 247's incumbent (BAND3DG@0.80) read out of sample in every cell, with its "
        "IS-matched controls:")
    say(W[["panel", "bps", "INC_OOS_CAGR", "INC_OOS_Sharpe", "INC_OOS_MaxDD",
           "INC_OOS_static_Sharpe", "INC_OOS_timed_Sharpe", "INC_OOS_comp_edge",
           "INC_OOS_timing_edge", "OOS_SPY_CAGR", "OOS_SPY_Sharpe", "INC_OOS_4b"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\nchooser picks a GATE leg in {int((~W.IS_pick.str.startswith('GROSSCUT')).sum())}"
        f"/{len(W)} cells, GROSSCUT in {int(W.IS_pick.str.startswith('GROSSCUT').sum())}/{len(W)}")
    say(f"picks clearing 4b OOS: {int(W.pick_OOS_4b.sum())}/{len(W)};  "
        f"picks beating their IS-matched TIMED control OOS: "
        f"{int(W.pick_beats_timed_OOS.sum())}/{len(W)}")
    say(f"incumbent OOS composition edge: mean {W.INC_OOS_comp_edge.mean():+.4f}, "
        f">0 in {int((W.INC_OOS_comp_edge>0).sum())}/{len(W)} cells; "
        f"OOS timing edge mean {W.INC_OOS_timing_edge.mean():+.4f}, "
        f">0 in {int((W.INC_OOS_timing_edge>0).sum())}/{len(W)}")

    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_console) + "\n")
    say(f"\nwrote {STAMP}.grid.csv .decomp.csv .boot.csv .walkforward.csv .console.txt")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_console) + "\n")


if __name__ == "__main__":
    main()

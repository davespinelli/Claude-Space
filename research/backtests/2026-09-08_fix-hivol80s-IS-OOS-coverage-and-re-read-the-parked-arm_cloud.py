#!/usr/bin/env python3
"""Idea 247 — FIX hivol80's IS/OOS COVERAGE AND RE-READ THE PARKED ARM.

Idea 246 PARKed `EWall + band3-dg armed only in hivol80` — a book that holds every priced
name at 75%/N and DE-GROSSES into the RULES v2 band only on high-volatility days — for one
reason and one reason only: the arming state is an EXPANDING 80th-percentile quantile of
SPY's 20-day vol, which arms 3.3% of in-sample days against 17.1% of out-of-sample days.
Rule 8 therefore chose that arm on roughly 66 armed IS days, and its OOS win is measured on
a regime the chooser barely saw.  This run replaces the expanding quantile with a FIXED,
pre-registered threshold whose IS and OOS coverage are matched by construction, prices the
result against a MATCHED-REALISED-GROSS static control (idea 244's channel), and asks
whether the 4b pass survives.

Pre-registration (fixed before any number was read):
  * THE BOOK.  W(t) = BAND3-dg weights on ARMED days, EW_ALL weights on disarmed days, both
    at nominal gross 0.75, weekly, next-day execution.  BAND3-dg at g=0.75 IS
    `baseline.rules_v2_weights` (asserted, gate G2); EW_ALL is the same object with the gate
    removed.  Arming is a MARKET-WIDE state (SPY vol20), known at close t, applied at t+1.
  * THE DEFECT.  `hivol80` = SPY vol20 >= its EXPANDING 80th percentile (min 756 days), idea
    75's setting.  An expanding quantile is anchored to a growing history, so its firing rate
    is a function of the sample position, not of the market: it CANNOT have matched coverage.
  * THE FIX — three conventions, all reported:
      EXP80    idea 246's expanding quantile.  Reproduced, not endorsed.
      ISFIX(q) theta = the q-th quantile of SPY vol20 over IS ONLY (<= 2016-12-31), then
               FROZEN for the whole sample.  Causal (uses no OOS information), and its IS
               coverage is exactly 1-q by construction, so any IS/OOS coverage gap that
               remains is a real regime shift and is reported as such.
      FULL(q)  the q-th quantile of the FULL sample.  NON-CAUSAL — declared here as a
               post-hoc DIAGNOSTIC carrying no verdict, included only to show what perfectly
               matched full-sample coverage would have bought.
    q in {0.60, 0.70, 0.80 (idea 246's rate), 0.90}.
  * THE COMPARAND.  A conditional de-grossing book spends less than 75% of NAV, so it must
    not be priced against a book that spends 75%.  For every conditional arm, a MATCHED
    static control is built: EW_ALL at the nominal gross g* solved (bisection, 40 steps) so
    the control's MEAN REALISED gross equals the conditional book's, on the same window.
    The achieved match is printed for every arm.
  * TWO tuned parameters, no more: the arming rate q and the panel.  Cost rung (10, 25 bps)
    is reported at both, never chosen.  Every grid point is reported.
        arms (11)  = EXP80, ISFIX x 4, FULL x 4, plus the two unconditional references
                     (EWALL always, BAND3DG always = live RULES v2)
        panels (3) = U56, B136, SMALL439 (sub-$2B less the 44 with max_1d_move >= 1.0)
        rungs (2)  = 10, 25 bps
    11 x 3 x 2 = 66 grid points, ALL reported, each with its matched-gross control.
  * BOTH KEEP paths on every point: 4a vs the live RULES v2 book on the same panel and
    window; 4b vs SPY.  A pass is additionally marked BEATS-CONTROL or not.
  * Rule 8 (PROTOCOL 8): the arm is chosen on IS <= 2016-12-31 by IS Sharpe among the CAUSAL
    arms only (EXP80 + ISFIX; FULL is barred from the chooser because it is non-causal), and
    2017-01-01.. is read once.  OOS CAGR/Sharpe/MaxDD reported against the same-window
    RULES v2 book, the matched control and SPY.

SURVIVORSHIP (idea 54, carried): B136 and SMALL439 are CURRENT-constituent lists — names
that died were never in them — so every level on those two panels is biased upward.  U56 is
a fixed ETF/mega-cap list and is the least-biased panel; idea 246's PARKed pass was on U56
and broad, so read the U56 column first.  Only the arm-minus-matched-control contrast inside
one panel is load-bearing.

Costs 10/25 bps per unit turnover; weights decided at close t applied at t+1 (PROTOCOL 2).
Deterministic, no network.  Writes .coverage.csv, .grid.csv, .walkforward.csv, .console.txt.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, band_state, rules_v2_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, rebalance_mask, metrics  # noqa

STAMP = "2026-09-08_fix-hivol80s-IS-OOS-coverage-and-re-read-the-parked-arm_cloud"
OUT = ROOT / "research" / "backtests"
FREQ = "W"
GROSS = 0.75
RUNGS = [10, 25]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
MIN_HIST, VOL_Q = 756, 0.80        # idea 75's settings, unchanged
QS = [0.60, 0.70, 0.80, 0.90]

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


def band3dg_weights(px, cols, g=GROSS):
    return ew_weights(px, cols, g).where(
        band_state(px[cols], 0.03).reindex(columns=px.columns).fillna(False), 0.0)


def conditional_weights(px, cols, armed, g=GROSS):
    """BAND3-dg when armed, EW_ALL when not.  `armed` is a per-day boolean Series."""
    a = armed.reindex(px.index).fillna(False)
    W = ew_weights(px, cols, g)
    B = band3dg_weights(px, cols, g)
    return B.where(a, axis=0).fillna(0.0) + W.where(~a, axis=0).fillna(0.0)


def spy_vol20(px):
    return px["SPY"].pct_change().rolling(20).std() * np.sqrt(252)


def arming(px, kind, q=None, is_end=IS_END):
    v = spy_vol20(px)
    if kind == "EXP80":
        thr = v.expanding(min_periods=MIN_HIST).quantile(VOL_Q)
        return (v >= thr).fillna(False), np.nan
    if kind == "ISFIX":
        thr = float(v.loc[:is_end].dropna().quantile(q))       # IS ONLY -> causal
        return (v >= thr).fillna(False), thr
    if kind == "FULL":
        thr = float(v.dropna().quantile(q))                    # NON-CAUSAL diagnostic
        return (v >= thr).fillna(False), thr
    raise ValueError(kind)


def panels():
    out = {}
    u = load_universe(); out["U56"] = (u, list(u.columns))
    b = load_universe(broad=True); out["B136"] = (b, list(b.columns))
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    sm = sm[[c for c in sm.columns if c == "SPY" or c not in bad]]
    out["SMALL439"] = (sm, [c for c in sm.columns if c != "SPY"])   # SPY benchmark only
    return out


def matched_control(px, cols, target_gross, win, bps):
    """EW_ALL at the nominal gross whose MEAN REALISED gross equals `target_gross` on `win`.
    Bisection on nominal g in [0.01, 1.00], 40 steps (realised gross is monotone in g)."""
    lo, hi = 0.01, 1.00
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        r = fast_backtest(px, ew_weights(px, cols, mid))
        got = float(r["gross"].reindex(win).mean())
        if got < target_gross:
            lo = mid
        else:
            hi = mid
    g = 0.5 * (lo + hi)
    r = fast_backtest(px, ew_weights(px, cols, g))
    return g, float(r["gross"].reindex(win).mean()), r


ARMS = ([("EXP80", None)] + [("ISFIX", q) for q in QS] + [("FULL", q) for q in QS]
        + [("EWALL", None), ("BAND3DG", None)])
CAUSAL = {"EXP80", "ISFIX"}
PANELS = ["U56", "B136", "SMALL439"]


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
        f"  max|d turnover| = {g1t:.3e}  (engine NaN rows before its first rebalance: "
        f"{int(e_res['returns'].isna().sum())})")
    assert g1r < 1e-12 and g1t < 1e-12, "G1 FAILED"
    g2 = float(np.abs(band3dg_weights(upx, ucols).values - w2.values).max())
    say(f"G2 band3dg_weights(0.75) vs baseline.rules_v2_weights   max|diff| = {g2:.3e}")
    assert g2 == 0.0, "G2 FAILED"
    a_all = pd.Series(True, index=upx.index)
    g3 = float(np.abs(conditional_weights(upx, ucols, a_all).values - w2.values).max())
    a_none = pd.Series(False, index=upx.index)
    g4 = float(np.abs(conditional_weights(upx, ucols, a_none).values
                      - ew_weights(upx, ucols).values).max())
    say(f"G3 conditional book with armed==ALL  == BAND3-dg   max|diff| = {g3:.3e}")
    say(f"G4 conditional book with armed==NONE == EW_ALL     max|diff| = {g4:.3e}")
    assert g3 == 0.0 and g4 == 0.0, "G3/G4 FAILED"

    # ---------------- COVERAGE: the defect, measured
    say("\n=== COVERAGE: armed share of days, IS vs OOS (the defect idea 247 names) ===")
    crows = []
    for k in PANELS:
        px, cols = PX[k]
        win = px.index[260:]
        wis = win[win <= IS_END]; woos = win[win >= OOS_START]
        for kind, q in ARMS:
            if kind in ("EWALL", "BAND3DG"):
                continue
            a, thr = arming(px, kind, q)
            cis = float(a.reindex(wis).mean()); coos = float(a.reindex(woos).mean())
            crows.append(dict(panel=k, arm=f"{kind}{'' if q is None else q:}", kind=kind, q=q,
                              threshold=thr, IS_days=len(wis), OOS_days=len(woos),
                              IS_armed_share=cis, OOS_armed_share=coos,
                              IS_armed_days=int(a.reindex(wis).sum()),
                              OOS_armed_days=int(a.reindex(woos).sum()),
                              gap=coos - cis, causal=kind in CAUSAL))
    CV = pd.DataFrame(crows)
    CV.to_csv(OUT / f"{STAMP}.coverage.csv", index=False)
    say(CV.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    e = CV[(CV.kind == "EXP80") & (CV.panel == "U56")].iloc[0]
    say(f"\nEXP80 on U56: IS {e.IS_armed_share:.1%} ({e.IS_armed_days} days) vs OOS "
        f"{e.OOS_armed_share:.1%} ({e.OOS_armed_days} days) — idea 246's 3.3%/17.1% reproduced"
        f" on this window; gap {e.gap:+.1%}.")
    isf = CV[(CV.kind == "ISFIX") & (CV.panel == "U56")]
    say("ISFIX on U56 (IS coverage is 1-q by construction; the residual gap is a real regime "
        "shift, not an estimator artefact):")
    for _, r in isf.iterrows():
        say(f"  q={r.q:.2f}  theta={r.threshold:.4f}  IS {r.IS_armed_share:.1%} "
            f"({r.IS_armed_days}d)  OOS {r.OOS_armed_share:.1%} ({r.OOS_armed_days}d)  "
            f"gap {r.gap:+.1%}")
    say(f"mean |IS-OOS gap|: EXP80 {CV[CV.kind=='EXP80'].gap.abs().mean():.1%}   "
        f"ISFIX {CV[CV.kind=='ISFIX'].gap.abs().mean():.1%}   "
        f"FULL {CV[CV.kind=='FULL'].gap.abs().mean():.1%}")

    # ---------------- GRID
    say("\n=== GRID: 11 arms x 3 panels x 2 rungs, each vs its MATCHED-GROSS control ===")
    rows = []
    RET, CRET = {}, {}
    for k in PANELS:
        px, cols = PX[k]
        win = px.index[260:]
        spy = px["SPY"].pct_change().fillna(0.0).reindex(win)
        mspy = mstats(spy)
        say(f"\n--- {k}: {len(cols)} held names, window {win[0].date()} -> {win[-1].date()} "
            f"({len(win)} days) | SPY {mspy['CAGR']:.2%} / {mspy['Sharpe']:.4f} / "
            f"{mspy['MaxDD']:.2%}, halves {mspy['H1']:.3f}/{mspy['H2']:.3f}")
        base_v2 = {bps: mstats(net(fast_backtest(px, band3dg_weights(px, cols)), bps).reindex(win))
                   for bps in RUNGS}
        for kind, q in ARMS:
            name = f"{kind}{'' if q is None else q}"
            if kind == "EWALL":
                W = ew_weights(px, cols)
            elif kind == "BAND3DG":
                W = band3dg_weights(px, cols)
            else:
                a, thr = arming(px, kind, q)
                W = conditional_weights(px, cols, a)
            r0 = fast_backtest(px, W)
            gmean = float(r0["gross"].reindex(win).mean())
            turn_yr = float(r0["turnover"].reindex(win).sum()) / (len(win) / 252)
            gnom, gach, c0 = matched_control(px, cols, gmean, win, RUNGS[0])
            for bps in RUNGS:
                r = net(r0, bps).reindex(win)
                c = net(c0, bps).reindex(win)
                RET[(k, name, bps)] = r; CRET[(k, name, bps)] = c
                m, mc = mstats(r), mstats(c)
                mv2 = base_v2[bps]
                p4a = (m["H1"] > mv2["H1"] and m["H2"] > mv2["H2"] and m["MaxDD"] >= mv2["MaxDD"])
                p4b = (m["H1"] > mspy["H1"] and m["H2"] > mspy["H2"]
                       and m["MaxDD"] >= 0.60 * mspy["MaxDD"] and m["CAGR"] >= 0.70 * mspy["CAGR"])
                rows.append(dict(panel=k, arm=name, kind=kind, q=q, bps=bps,
                                 CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                 H1=m["H1"], H2=m["H2"], gross=gmean, turnover_yr=turn_yr,
                                 ctrl_nominal_g=gnom, ctrl_gross=gach,
                                 ctrl_Sharpe=mc["Sharpe"], ctrl_CAGR=mc["CAGR"],
                                 ctrl_MaxDD=mc["MaxDD"],
                                 dSharpe_vs_ctrl=m["Sharpe"] - mc["Sharpe"],
                                 dCAGR_vs_ctrl=m["CAGR"] - mc["CAGR"],
                                 pass4a=p4a, pass4b=p4b,
                                 pass4b_and_beats_ctrl=bool(p4b and m["Sharpe"] > mc["Sharpe"]),
                                 causal=kind in CAUSAL or kind in ("EWALL", "BAND3DG")))
    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    say("\nfull grid (all 66 points reported):")
    say(G.drop(columns=["kind", "q", "turnover_yr"]).to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\nmatched-gross control accuracy: max|target - achieved| = "
        f"{float((G.gross - G.ctrl_gross).abs().max()):.3e}")
    say(f"4a passes {int(G.pass4a.sum())}/{len(G)}   4b passes {int(G.pass4b.sum())}/{len(G)}"
        f"   4b AND beats its matched control {int(G.pass4b_and_beats_ctrl.sum())}/{len(G)}")
    say(f"arms beating their matched-gross control on Sharpe: {int((G.dSharpe_vs_ctrl>0).sum())}"
        f"/{len(G)}  (mean dSharpe {G.dSharpe_vs_ctrl.mean():+.4f}, "
        f"median {G.dSharpe_vs_ctrl.median():+.4f})")
    for kind in ("EXP80", "ISFIX", "FULL"):
        sub = G[G.kind == kind]
        say(f"  {kind:8s} 4b {int(sub.pass4b.sum())}/{len(sub)}   beats control "
            f"{int((sub.dSharpe_vs_ctrl>0).sum())}/{len(sub)}   mean dSharpe "
            f"{sub.dSharpe_vs_ctrl.mean():+.4f}")

    say("\nTHE PARKED ARM (EXP80, the exact object idea 246 parked) vs its fixed-threshold twins:")
    say(G[(G.kind.isin(["EXP80", "ISFIX"])) & (G.panel.isin(["U56", "B136"]))]
        [["panel", "arm", "bps", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "gross",
          "ctrl_Sharpe", "dSharpe_vs_ctrl", "turnover_yr", "pass4a", "pass4b",
          "pass4b_and_beats_ctrl"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------- OOS read of every 4b point + RULE 8
    say("\n=== RULE 8 WALK-FORWARD (arm chosen on IS <= 2016-12-31 among CAUSAL arms only) ===")
    wrows = []
    for k in PANELS:
        px, cols = PX[k]
        win = px.index[260:]
        wis = win[win <= IS_END]; woos = win[win >= OOS_START]
        spy_o = mstats(px["SPY"].pct_change().fillna(0.0).reindex(woos))
        for bps in RUNGS:
            cand = [f"{kd}{'' if q is None else q}" for kd, q in ARMS if kd in CAUSAL]
            iss = {nm: metrics(RET[(k, nm, bps)].reindex(wis))["Sharpe"] for nm in cand}
            pick = max(iss, key=iss.get)
            mo = mstats(RET[(k, pick, bps)].reindex(woos))
            mco = mstats(CRET[(k, pick, bps)].reindex(woos))
            mv2 = mstats(RET[(k, "BAND3DG", bps)].reindex(woos))
            mew = mstats(RET[(k, "EWALL", bps)].reindex(woos))
            # the arm idea 246 actually parked, read once regardless of the chooser
            me = mstats(RET[(k, "EXP80", bps)].reindex(woos))
            mce = mstats(CRET[(k, "EXP80", bps)].reindex(woos))
            wrows.append(dict(panel=k, bps=bps, IS_pick=pick, IS_Sharpe=iss[pick],
                              OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                              OOS_ctrl_Sharpe=mco["Sharpe"], OOS_RULESV2_Sharpe=mv2["Sharpe"],
                              OOS_EWALL_Sharpe=mew["Sharpe"], OOS_SPY_Sharpe=spy_o["Sharpe"],
                              OOS_SPY_CAGR=spy_o["CAGR"], OOS_SPY_MaxDD=spy_o["MaxDD"],
                              EXP80_OOS_Sharpe=me["Sharpe"], EXP80_OOS_CAGR=me["CAGR"],
                              EXP80_OOS_MaxDD=me["MaxDD"], EXP80_OOS_ctrl_Sharpe=mce["Sharpe"],
                              pick_beats_ctrl_OOS=mo["Sharpe"] > mco["Sharpe"],
                              pick_beats_SPY_OOS=mo["Sharpe"] > spy_o["Sharpe"],
                              pick_beats_RULESV2_OOS=mo["Sharpe"] > mv2["Sharpe"],
                              pick_OOS_4b=(mo["Sharpe"] > spy_o["Sharpe"]
                                           and mo["MaxDD"] >= 0.60 * spy_o["MaxDD"]
                                           and mo["CAGR"] >= 0.70 * spy_o["CAGR"])))
    W = pd.DataFrame(wrows)
    W.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    say(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\nIS chooser picks EXP80 (the defective estimator) in "
        f"{int((W.IS_pick == 'EXP80').sum())}/{len(W)} cells")
    say(f"picks beating their matched-gross control OOS: {int(W.pick_beats_ctrl_OOS.sum())}/{len(W)}")
    say(f"picks beating SPY OOS:                         {int(W.pick_beats_SPY_OOS.sum())}/{len(W)}")
    say(f"picks beating live RULES v2 OOS:               {int(W.pick_beats_RULESV2_OOS.sum())}/{len(W)}")
    say(f"picks clearing 4b OOS:                         {int(W.pick_OOS_4b.sum())}/{len(W)}")

    say("\nEvery 4b-clearing grid point, read once out of sample:")
    krows = []
    for _, rr in G[G.pass4b].iterrows():
        px, cols = PX[rr.panel]
        win = px.index[260:]; woos = win[win >= OOS_START]
        spy_o = mstats(px["SPY"].pct_change().fillna(0.0).reindex(woos))
        mo = mstats(RET[(rr.panel, rr.arm, rr.bps)].reindex(woos))
        mc = mstats(CRET[(rr.panel, rr.arm, rr.bps)].reindex(woos))
        mv2 = mstats(RET[(rr.panel, "BAND3DG", rr.bps)].reindex(woos))
        krows.append(dict(panel=rr.panel, arm=rr.arm, bps=rr.bps, causal=rr.causal,
                          full_CAGR=rr.CAGR, full_Sharpe=rr.Sharpe, full_MaxDD=rr.MaxDD,
                          H1=rr.H1, H2=rr.H2, dSharpe_vs_ctrl=rr.dSharpe_vs_ctrl,
                          OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                          OOS_ctrl_Sharpe=mc["Sharpe"], OOS_RULESV2_Sharpe=mv2["Sharpe"],
                          OOS_SPY_Sharpe=spy_o["Sharpe"],
                          OOS_beats_ctrl=mo["Sharpe"] > mc["Sharpe"],
                          OOS_4b=(mo["Sharpe"] > spy_o["Sharpe"]
                                  and mo["MaxDD"] >= 0.60 * spy_o["MaxDD"]
                                  and mo["CAGR"] >= 0.70 * spy_o["CAGR"])))
    K = pd.DataFrame(krows)
    K.to_csv(OUT / f"{STAMP}.keep.csv", index=False)
    say(K.to_string(index=False, float_format=lambda x: f"{x:.4f}") if len(K) else "  (none)")

    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_console) + "\n")
    say(f"\nwrote {STAMP}.coverage.csv .grid.csv .keep.csv .walkforward.csv .console.txt")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_console) + "\n")


if __name__ == "__main__":
    main()

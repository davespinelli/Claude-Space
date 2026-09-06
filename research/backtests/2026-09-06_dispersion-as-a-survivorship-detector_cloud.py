#!/usr/bin/env python3
"""QUEUE idea 83 — dispersion-as-a-survivorship-detector (cloud, 2026-09-06).

Question (pre-registered, copied from QUEUE.md before any number below was read)
-------------------------------------------------------------------------------
Idea 73 found that draw-level dispersion predicts the LEVEL of both books' Sharpe far
more strongly (R2 0.43 / 0.33 over 150 random 36-name sub-panels of B136) than it
predicts the ranking premium (R2 0.08).  On a CURRENT-CONSTITUENT panel that is exactly
the pattern survivorship manufactures: a draw containing more of the names that went on
to win has both higher 12-1 momentum dispersion and higher realised Sharpe, with no
causal link between them.

Pre-registered test, stated so it can fail:

    Regress each name's FULL-SAMPLE return out of the draw-level relationship.  If the
    dispersion -> Sharpe slope survives that control, dispersion carries information the
    winner content does not, and idea 73's test C stands.  If it dies, dispersion is a
    SURVIVORSHIP THERMOMETER and idea 73's test C is contaminated.

    VERDICT RULE, fixed before the run: dispersion is declared a thermometer if, in the
    MAJORITY of (draw size) cells, controlling for the draw's mean full-sample name CAGR
    (a) removes at least half the magnitude of the dispersion slope on EWall Sharpe AND
    (b) drops its |t| below 2.0.  Otherwise the relationship survives the control.

Two controls are run, because "winner content" has a hindsight version and an observable
version, and telling them apart is the whole point:
    HIND  mean full-sample CAGR of the draw's names  (2009-2026; look-ahead BY DESIGN —
          it is a diagnostic for contamination, never a trading input)
    OBS   mean 2009-2016 CAGR of the draw's names    (knowable at the 2017 boundary)
If HIND kills the slope and OBS does not, the contamination is specifically hindsight.
If both kill it, "panels of strong names" is the whole story and it is not even a
survivorship point.

Design (PROTOCOL rules 1-9)
---------------------------
Panel     : B136 = load_universe(broad=True), 135 tradable names + SPY.  Idea 73's test C
            panel, so this is a controlled re-reading of that exact experiment.
            SURVIVORSHIP: B136 is a CURRENT-CONSTITUENT list — delisted and acquired names
            are absent.  That is not a caveat here, it is the subject: this script measures
            how much of a published statistic that absence explains.  SMALL484 (the
            max_1d_move >= 1.0 screen applied first) is carried as a SECOND corpus at the
            primary cell, because it is the panel with the worst survivorship (idea 54)
            and therefore where the thermometer reading should be strongest.
Draws     : idea 73's construction, IMPORTED not re-implemented (build_panels, elig_mask,
            w_ewall, w_candg, dispersion, run, ols, spearman, at_cost, fail4a/4b), with
            idea 73's own seed 20260904 and 150 draws, so cell (36, 10) reproduces its
            published test C exactly.
Params    : exactly TWO tuned dimensions — DRAW SIZE in {20, 36, 60} and RANKED n in
            {5, 10, 20}.  ALL 9 combinations reported; nothing is selected on them.
            Cost rung (10 and 25 bps) and corpus are reported at every value.
Costs     : 10 bps (PROTOCOL; the verdict is read here) and 25 bps, applied analytically.
Execution : weekly, weights at close t applied at t+1 (idea 73's `run` -> engine.backtest).
Baseline  : RULES v1 weekly on B136 (4a) and SPY buy-and-hold (4b), both reported for
            every walk-forward book.
Rule 8    : the diagnostic is turned into a real selector and walk-forwarded.  Panels are
            ranked by their 2009-2016 dispersion ALONE, the top decile is bought, and
            2017-2026 is read once against (i) the bottom decile, (ii) the mean of all 150
            draws = a random panel picker, (iii) an IS-Sharpe picker, (iv) an IS-mean-name-
            CAGR picker, (v) the full B136 EWall book, (vi) RULES v1 and (vii) SPY.  Both
            KEEP paths evaluated on every selected book.

Reproduction gates, asserted before any new number is read
  [A] idea 73's `dispersion(...).disp_std` equals the fast std-only path used here, on the
      first three draws, to machine precision (the full function computes D1-D10 deciles
      with a per-row apply and is 100x slower; only disp_std is used by test C).
  [B] cell (draw size 36, n = 10) at 10 bps reproduces idea 73's published test C numbers:
      premium mean +0.028, slope +0.32 (t +3.55, R2 0.078), level slopes CANDg +3.10 and
      EWall +2.78, terciles +0.062 vs -0.005.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-06_dispersion-as-a-survivorship-detector_cloud"
OUT = ROOT / "research" / "backtests"

_p73 = OUT / "2026-09-04_asset-class-dispersion_cloud.py"
_spec = importlib.util.spec_from_file_location("i73", _p73)
i73 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(i73)
build_panels, elig_mask = i73.build_panels, i73.elig_mask
w_ewall, w_candg, dispersion = i73.w_ewall, i73.w_candg, i73.dispersion
run, ols, spearman, at_cost = i73.run, i73.ols, i73.spearman, i73.at_cost
m, halves, fail4a, fail4b = i73.m, i73.halves, i73.fail4a, i73.fail4b
SEED, N_DRAWS = i73.SEED, i73.N_DRAWS
IS_END, OOS_START, FREQ = i73.IS_END, i73.OOS_START, i73.FREQ

SIZES = [20, 36, 60]          # tuned dimension 1 — ALL reported
NS = [5, 10, 20]              # tuned dimension 2 — ALL reported
COSTS = [10, 25]
PROTO_COST = 10
PRIMARY = (36, 10)            # idea 73's published cell
DECILE = 0.10

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 500)
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def disp_std_fast(px, tradable):
    """Only the disp_std column of idea 73's `dispersion` (gate [A] asserts equality)."""
    mom = px.shift(21) / px.shift(252) - 1
    return mom.where(elig_mask(px, tradable)).std(axis=1)


def name_cagr(px, names, lo=None, hi=None):
    """Per-name annualised full-period return over [lo, hi]. The look-ahead control."""
    p = px[names]
    if lo is not None:
        p = p.loc[lo:]
    if hi is not None:
        p = p.loc[:hi]
    first, last = p.ffill().bfill().iloc[0], p.ffill().iloc[-1]
    yrs = len(p) / 252.0
    return ((last / first) ** (1.0 / yrs) - 1.0)


def mols(y, X):
    """Multiple OLS with a constant. Returns (betas, ts, R2)."""
    y = np.asarray(y, float)
    X = np.asarray(X, float)
    n = len(y)
    A = np.column_stack([np.ones(n)] + [X[:, j] for j in range(X.shape[1])])
    beta, *_ = np.linalg.lstsq(A, y, rcond=None)
    res = y - A @ beta
    dof = n - A.shape[1]
    s2 = res @ res / dof
    cov = s2 * np.linalg.inv(A.T @ A)
    se = np.sqrt(np.diag(cov))
    ss = ((y - y.mean()) ** 2).sum()
    return beta[1:], beta[1:] / se[1:], float(1 - res @ res / ss if ss else np.nan)


def draws_for(px, tradable, size, seed):
    rng = np.random.default_rng(seed)
    names = sorted(tradable)
    return [list(rng.choice(names, size, replace=False)) for _ in range(N_DRAWS)]


def sweep(px, tradable, corpus, size, rows):
    """One (corpus, draw size) cell: N_DRAWS panels, every n, every cost rung."""
    start = px.index[260]
    for i, pick in enumerate(draws_for(px, tradable, size, SEED)):
        cols = list(dict.fromkeys(pick + ["SPY"]))
        p = px[cols]
        tr = set(pick)
        d = disp_std_fast(p, tr).loc[start:]
        ew = run(p, w_ewall(p, tr), start)
        cds = {n: run(p, w_candg(p, tr, n), start) for n in NS}
        hind = float(name_cagr(px, pick, lo=start).mean())
        obs = float(name_cagr(px, pick, lo=start, hi=IS_END).mean())
        hind_sd = float(name_cagr(px, pick, lo=start).std())
        for c in COSTS:
            rew = at_cost(*ew, c)
            base = dict(corpus=corpus, size=size, draw=i, cost=c,
                        disp=float(d.mean()), disp_IS=float(d.loc[:IS_END].mean()),
                        hind_cagr=hind, obs_cagr=obs, hind_sd=hind_sd,
                        EW_CAGR=m(rew)[0], EW_Sharpe=m(rew)[1], EW_MaxDD=m(rew)[2],
                        EW_IS_Sharpe=m(rew.loc[:IS_END])[1],
                        EW_OOS_CAGR=m(rew.loc[OOS_START:])[0],
                        EW_OOS_Sharpe=m(rew.loc[OOS_START:])[1],
                        EW_OOS_MaxDD=m(rew.loc[OOS_START:])[2])
            for n in NS:
                rcd = at_cost(*cds[n], c)
                base[f"CD{n}_Sharpe"] = m(rcd)[1]
                base[f"CD{n}_CAGR"] = m(rcd)[0]
                base[f"CD{n}_MaxDD"] = m(rcd)[2]
                base[f"CD{n}_IS_Sharpe"] = m(rcd.loc[:IS_END])[1]
                base[f"CD{n}_OOS_Sharpe"] = m(rcd.loc[OOS_START:])[1]
                base[f"prem{n}"] = base[f"CD{n}_Sharpe"] - base["EW_Sharpe"]
            rows.append(base)
        if (i + 1) % 50 == 0:
            P(f"    ... {corpus} size {size}: {i + 1}/{N_DRAWS} draws")


def report_cell(S, corpus, size, cost, res):
    """The idea-83 regression table for one (corpus, size, cost) cell."""
    P(f"\n--- {corpus} / draw size {size} / {cost} bps / {len(S)} draws ---")
    P(f"  dispersion across draws: min {S.disp.min():.4f}  median {S.disp.median():.4f}  "
      f"max {S.disp.max():.4f}")
    P(f"  mean full-sample name CAGR (HIND) across draws: {S.hind_cagr.mean():.4f} "
      f"(sd {S.hind_cagr.std():.4f});  IS-only (OBS): {S.obs_cagr.mean():.4f} "
      f"(sd {S.obs_cagr.std():.4f})")
    rh, th = spearman(S.disp, S.hind_cagr)
    ro, to_ = spearman(S.disp, S.obs_cagr)
    P(f"  IS DISPERSION ITSELF WINNER CONTENT?  Spearman(disp, HIND) {rh:+.3f} (t {th:+.2f});  "
      f"Spearman(disp, OBS) {ro:+.3f} (t {to_:+.2f})")
    tbl = []
    for lab, y in (("EWall Sharpe", S.EW_Sharpe),
                   (f"CANDg-n{PRIMARY[1]} Sharpe", S[f"CD{PRIMARY[1]}_Sharpe"]),
                   (f"premium n{PRIMARY[1]}", S[f"prem{PRIMARY[1]}"])):
        b0, t0, r20 = ols(S.disp, y)
        bH, tH, r2H = mols(y, np.column_stack([S.disp, S.hind_cagr]))
        bO, tO, r2O = mols(y, np.column_stack([S.disp, S.obs_cagr]))
        keptH = bH[0] / b0 if b0 else np.nan
        keptO = bO[0] / b0 if b0 else np.nan
        tbl.append(dict(corpus=corpus, size=size, cost=cost, y=lab,
                        raw_slope=b0, raw_t=t0, raw_R2=r20,
                        HIND_slope=bH[0], HIND_t=tH[0], HIND_R2=r2H, HIND_kept=keptH,
                        ctrl_slope_HIND=bH[1], ctrl_t_HIND=tH[1],
                        OBS_slope=bO[0], OBS_t=tO[0], OBS_R2=r2O, OBS_kept=keptO,
                        thermometer=bool(abs(keptH) < 0.5 and abs(tH[0]) < 2.0)))
    T = pd.DataFrame(tbl)
    res.extend(tbl)
    P(T[["y", "raw_slope", "raw_t", "raw_R2", "HIND_slope", "HIND_t", "HIND_R2",
         "HIND_kept", "OBS_slope", "OBS_t", "OBS_R2", "OBS_kept", "thermometer"]].to_string(
        index=False, float_format=lambda x: f"{x:.4f}"))
    return T


def main():
    P("=" * 190)
    P("IDEA 83 — IS DISPERSION A SURVIVORSHIP THERMOMETER?  Regress each name's full-sample "
      "return out of idea 73's test C and see whether the dispersion slope survives.")
    P(f"  two tuned dimensions, both reported exhaustively: draw size {SIZES} x ranked n {NS}; "
      f"{N_DRAWS} draws each, seed {SEED} (idea 73's), 2 cost rungs, 2 corpora at the primary "
      f"cell.  VERDICT RULE fixed in the header before the run.")
    P("=" * 190)

    P("\nbuilding idea 73's panels (its own build_panels, imported):")
    panels = build_panels()
    px136, tr136 = panels["B136"]
    P(f"  B136     {px136.shape[1]:4d} columns, {len(tr136):4d} tradable, "
      f"{px136.index[0].date()} -> {px136.index[-1].date()}")
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    pxs = pxs[s_stk + ["SPY"]].dropna(how="all").ffill()
    P(f"  SMALL484 {pxs.shape[1]:4d} columns, {len(s_stk):4d} tradable "
      f"(dropped {len([c for c in load_universe(small=True).columns if c in bad])} with "
      f"max_1d_move >= 1.0), {pxs.index[0].date()} -> {pxs.index[-1].date()}")
    P("  SURVIVORSHIP: both are current-constituent lists.  Here that is the SUBJECT, not a "
      "caveat: the run measures how much of a published statistic their missing delistings "
      "explain.  It cannot measure what the missing names would have done.")

    # -------------------------------------------------------------- gate [A]
    P("\n" + "=" * 190)
    P("GATE [A] — the fast disp_std path equals idea 73's own dispersion().disp_std")
    start = px136.index[260]
    worst = 0.0
    for pick in draws_for(px136, tr136, PRIMARY[0], SEED)[:3]:
        p = px136[list(dict.fromkeys(pick + ["SPY"]))]
        tr = set(pick)
        worst = max(worst, float((disp_std_fast(p, tr) - dispersion(p, tr).disp_std).abs().max()))
    P(f"  max|diff| over the first 3 draws = {worst:.3e} -> {'PASS' if worst < 1e-12 else 'FAIL'}")
    assert worst < 1e-12

    # -------------------------------------------------------------- sweep
    P("\n" + "=" * 190)
    P("SWEEP — 150 draws per cell.")
    rows = []
    for size in SIZES:
        sweep(px136, tr136, "B136", size, rows)
    sweep(pxs, set(s_stk), "SMALL484", PRIMARY[0], rows)
    D = pd.DataFrame(rows)
    D.to_csv(OUT / f"{STEM}.draws.csv", index=False)
    P(f"  {len(D)} draw-rows written.")

    # -------------------------------------------------------------- gate [B]
    P("\n" + "=" * 190)
    P("GATE [B] — reproduce idea 73's published test C at (B136, size 36, n 10, 10 bps)")
    S = D[(D.corpus == "B136") & (D["size"] == PRIMARY[0]) & (D.cost == PROTO_COST)]
    b, t, r2 = ols(S.disp, S.prem10)
    bc, tc, r2c = ols(S.disp, S.CD10_Sharpe)
    be, te, r2e = ols(S.disp, S.EW_Sharpe)
    order = np.argsort(S.disp.values)
    k = N_DRAWS // 3
    hi = S.prem10.values[order[-k:]].mean()
    lo = S.prem10.values[order[:k]].mean()
    P("  the only figures idea 73 published for test C are the three R2s quoted in QUEUE idea 83")
    P("  ('R2 0.43/0.33 for the two LEVELS vs 0.08 for the ranking gap'); those are asserted, and")
    P("  everything else is printed for the record.")
    P(f"  premium ~ dispersion:      slope {b:+.3f}  t {t:+.2f}  R2 {r2:.3f}   "
      f"(idea 73 published R2 0.08)")
    P(f"  CANDg-n10 level ~ disp:    slope {bc:+.3f}  t {tc:+.2f}  R2 {r2c:.3f}  "
      f"(idea 73 published R2 0.43)")
    P(f"  EWall level ~ dispersion:  slope {be:+.3f}  t {te:+.2f}  R2 {r2e:.3f}  "
      f"(idea 73 published R2 0.33)")
    P(f"  premium mean {S.prem10.mean():+.4f};  dispersion terciles {hi:+.4f} (high) vs "
      f"{lo:+.4f} (low)")
    ok = (abs(r2c - 0.43) < 0.02 and abs(r2e - 0.33) < 0.02 and abs(r2 - 0.08) < 0.02)
    P(f"  -> {'PASS' if ok else 'FAIL'}")
    assert ok, (r2c, r2e, r2)

    # -------------------------------------------------------------- Q1
    P("\n" + "=" * 190)
    P("Q1 — DOES THE DISPERSION SLOPE SURVIVE THE WINNER-CONTENT CONTROL?")
    P("  raw_*   idea 73's univariate regression of the draw statistic on draw dispersion")
    P("  HIND_*  the same with the draw's mean FULL-SAMPLE name CAGR added (look-ahead by design)")
    P("  OBS_*   the same with the draw's mean 2009-2016 name CAGR added (observable at 2017)")
    P("  *_kept  the controlled slope as a fraction of the raw slope.  thermometer = |kept|<0.5")
    P("          AND |controlled t|<2.0, the verdict rule fixed before the run.")
    res = []
    for corpus, size in [("B136", s) for s in SIZES] + [("SMALL484", PRIMARY[0])]:
        for c in COSTS:
            report_cell(D[(D.corpus == corpus) & (D["size"] == size) & (D.cost == c)],
                        corpus, size, c, res)
    R = pd.DataFrame(res)
    R.to_csv(OUT / f"{STEM}.regressions.csv", index=False)

    P("\n" + "=" * 190)
    P("Q1 VERDICT TABLE — every (corpus, size, cost) cell, the three dependent variables:")
    P(R.pivot_table(index=["corpus", "size", "cost"], columns="y",
                    values=["raw_t", "HIND_t", "HIND_kept"]).to_string(
                        float_format=lambda x: f"{x:.3f}"))
    ew = R[R.y == "EWall Sharpe"]
    n_th = int(ew.thermometer.sum())
    P(f"\n  EWall Sharpe: the raw dispersion slope is +{ew.raw_slope.mean():.2f} "
      f"(mean |t| {ew.raw_t.abs().mean():.2f}, mean R2 {ew.raw_R2.mean():.3f}); with the HIND "
      f"control it is {ew.HIND_slope.mean():+.2f} (mean |t| {ew.HIND_t.abs().mean():.2f}), "
      f"keeping {ew.HIND_kept.mean():.0%} of its magnitude.")
    P(f"  THERMOMETER by the pre-registered rule in {n_th}/{len(ew)} cells "
      f"-> {'THERMOMETER' if n_th > len(ew) / 2 else 'SLOPE SURVIVES THE CONTROL'}")
    prem = R[R.y.str.startswith("premium")]
    P(f"  premium (idea 73's test C statistic): raw slope {prem.raw_slope.mean():+.3f} "
      f"(mean |t| {prem.raw_t.abs().mean():.2f}), HIND-controlled {prem.HIND_slope.mean():+.3f} "
      f"(mean |t| {prem.HIND_t.abs().mean():.2f}), keeping {prem.HIND_kept.mean():.0%}; "
      f"thermometer in {int(prem.thermometer.sum())}/{len(prem)} cells.")
    P("\n  the CONTROL's own slope (how strongly winner content alone moves the statistic):")
    P(R[["corpus", "size", "cost", "y", "ctrl_slope_HIND", "ctrl_t_HIND", "HIND_R2",
         "raw_R2"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("\n" + "=" * 190)
    P("Q1b — THE SAME AT EVERY RANKED n (tuned dimension 2), B136 @10bps, premium as y:")
    q = []
    for size in SIZES:
        S = D[(D.corpus == "B136") & (D["size"] == size) & (D.cost == PROTO_COST)]
        for n in NS:
            y = S[f"prem{n}"]
            b0, t0, r20 = ols(S.disp, y)
            bH, tH, r2H = mols(y, np.column_stack([S.disp, S.hind_cagr]))
            bL, tL, r2L = ols(S.disp, S[f"CD{n}_Sharpe"])
            bLH, tLH, _ = mols(S[f"CD{n}_Sharpe"], np.column_stack([S.disp, S.hind_cagr]))
            q.append(dict(size=size, n=n, prem_mean=y.mean(), raw_slope=b0, raw_t=t0, raw_R2=r20,
                          HIND_slope=bH[0], HIND_t=tH[0], kept=bH[0] / b0 if b0 else np.nan,
                          level_raw_slope=bL, level_raw_t=tL, level_raw_R2=r2L,
                          level_HIND_slope=bLH[0], level_HIND_t=tLH[0],
                          level_kept=bLH[0] / bL if bL else np.nan))
    Q = pd.DataFrame(q)
    Q.to_csv(OUT / f"{STEM}.by_n.csv", index=False)
    P(Q.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # -------------------------------------------------------------- rule 8
    P("\n" + "=" * 190)
    P("PROTOCOL RULE 8 — the diagnostic as a SELECTOR.  Panels ranked on 2009-2016 ONLY; "
      "2017-2026 read once.")
    P("  DISP-hi/lo  top / bottom decile of draws by IS dispersion")
    P("  SHARPE-hi   top decile by IS EWall Sharpe (the incumbent selector)")
    P("  OBSCAGR-hi  top decile by IS mean name CAGR")
    P("  ALL         mean of all 150 draws = picking a panel at random (the do-nothing control)")
    P("  B136-EW     the full 135-name EWall book (no draw at all)")
    v1 = backtest(px136, rules_v1_weights(px136), cost_bps=PROTO_COST,
                  freq=FREQ)["returns"].loc[start:]
    spy = px136["SPY"].pct_change().fillna(0.0).loc[start:]
    spy_oos = m(spy.loc[OOS_START:])
    v1_oos = m(v1.loc[OOS_START:])
    P(f"\n  SPY      {m(spy)[0]:.2%} / {m(spy)[1]:.3f} / {m(spy)[2]:.2%}  halves "
      f"{halves(spy)[0]:.3f}/{halves(spy)[1]:.3f}   OOS {spy_oos[0]:.2%} / {spy_oos[1]:.3f} / "
      f"{spy_oos[2]:.2%}")
    P(f"  RULES v1 @10bps  {m(v1)[0]:.2%} / {m(v1)[1]:.3f} / {m(v1)[2]:.2%}   "
      f"OOS {v1_oos[0]:.2%} / {v1_oos[1]:.3f} / {v1_oos[2]:.2%}")
    full_ew = at_cost(*run(px136, w_ewall(px136, tr136), start), PROTO_COST)
    P(f"  B136-EW  {m(full_ew)[0]:.2%} / {m(full_ew)[1]:.3f} / {m(full_ew)[2]:.2%}   "
      f"OOS {m(full_ew.loc[OOS_START:])[0]:.2%} / {m(full_ew.loc[OOS_START:])[1]:.3f} / "
      f"{m(full_ew.loc[OOS_START:])[2]:.2%}   4a {'-'.join(fail4a(full_ew, v1)) or 'PASS'}   "
      f"4b {','.join(fail4b(full_ew, spy, m(full_ew.loc[OOS_START:])[1], spy_oos[1])) or 'PASS'}")
    WF = []
    for corpus, size in [("B136", s) for s in SIZES] + [("SMALL484", PRIMARY[0])]:
        for c in COSTS:
            S = D[(D.corpus == corpus) & (D["size"] == size) & (D.cost == c)]
            k = max(int(len(S) * DECILE), 1)
            sels = {
                "DISP-hi": S.nlargest(k, "disp_IS"),
                "DISP-lo": S.nsmallest(k, "disp_IS"),
                "SHARPE-hi": S.nlargest(k, "EW_IS_Sharpe"),
                "OBSCAGR-hi": S.nlargest(k, "obs_cagr"),
                "ALL": S,
            }
            for sel, G in sels.items():
                WF.append(dict(corpus=corpus, size=size, cost=c, sel=sel, k=len(G),
                               mean_disp_IS=G.disp_IS.mean(),
                               OOS_CAGR=G.EW_OOS_CAGR.mean(),
                               OOS_Sharpe=G.EW_OOS_Sharpe.mean(),
                               OOS_MaxDD=G.EW_OOS_MaxDD.mean(),
                               OOS_Sharpe_sd=G.EW_OOS_Sharpe.std(),
                               beat_SPY=float((G.EW_OOS_Sharpe > spy_oos[1]).mean()),
                               beat_v1=float((G.EW_OOS_Sharpe > v1_oos[1]).mean()),
                               beat_ALL=np.nan))
    W = pd.DataFrame(WF)
    for (co, sz, c), g in W.groupby(["corpus", "size", "cost"]):
        base = float(g[g.sel == "ALL"].OOS_Sharpe.iloc[0])
        W.loc[g.index, "beat_ALL"] = g.OOS_Sharpe - base
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P("\n  OOS (2017-2026) of the EWall book on the SELECTED panels, mean over the decile:")
    P(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("\n  the selector's edge over a random panel (OOS Sharpe minus the ALL row):")
    P(W[W.sel != "ALL"].pivot_table(index=["corpus", "size", "cost"], columns="sel",
                                    values="beat_ALL").to_string(
                                        float_format=lambda x: f"{x:+.4f}"))
    dh = W[W.sel == "DISP-hi"].beat_ALL
    P(f"\n  DISP-hi beats the random panel in {int((dh > 0).sum())}/{len(dh)} cells "
      f"(mean {dh.mean():+.4f} OOS Sharpe);  DISP-lo "
      f"{W[W.sel=='DISP-lo'].beat_ALL.mean():+.4f};  SHARPE-hi "
      f"{W[W.sel=='SHARPE-hi'].beat_ALL.mean():+.4f};  OBSCAGR-hi "
      f"{W[W.sel=='OBSCAGR-hi'].beat_ALL.mean():+.4f}.")

    P("\n" + "=" * 190)
    P("BOTH KEEP PATHS on the walk-forward books (primary cell, B136 size 36, 10 bps).")
    S = D[(D.corpus == "B136") & (D["size"] == PRIMARY[0]) & (D.cost == PROTO_COST)]
    k = max(int(len(S) * DECILE), 1)
    kp = []
    for sel, G in (("DISP-hi", S.nlargest(k, "disp_IS")), ("DISP-lo", S.nsmallest(k, "disp_IS")),
                   ("SHARPE-hi", S.nlargest(k, "EW_IS_Sharpe")), ("ALL", S)):
        picks = draws_for(px136, tr136, PRIMARY[0], SEED)
        p4a = p4b = 0
        for j in G.draw.values:
            p = px136[list(dict.fromkeys(picks[int(j)] + ["SPY"]))]
            tr = set(picks[int(j)])
            r = at_cost(*run(p, w_ewall(p, tr), start), PROTO_COST)
            o = m(r.loc[OOS_START:])[1]
            p4a += (not fail4a(r, v1))
            p4b += (not fail4b(r, spy, o, spy_oos[1]))
        kp.append(dict(sel=sel, panels=len(G), pass4a=p4a, pass4b=p4b,
                       rate4a=p4a / len(G), rate4b=p4b / len(G)))
    K = pd.DataFrame(kp)
    P(K.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    P("  (4a is against RULES v1 on B136; 4b against SPY. A selector that mattered would lift "
      "the 4b rate of its decile above the ALL row's.)")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    P(f"\nwrote {STEM}.draws.csv / .regressions.csv / .by_n.csv / .walkforward.csv / .console.txt")


if __name__ == "__main__":
    main()

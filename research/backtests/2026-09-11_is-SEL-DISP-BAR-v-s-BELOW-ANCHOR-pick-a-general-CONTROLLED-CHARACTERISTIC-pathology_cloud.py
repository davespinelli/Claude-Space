#!/usr/bin/env python3
"""Idea 715 - "is-SEL-DISP|v's-BELOW-ANCHOR-pick-a-general-CONTROLLED-CHARACTERISTIC-pathology"
(cloud, 2026-09-11).

The question
------------
Idea 540 built four IS-only panel selectors over idea 295's 168-panel MIX ladder and reported
that SEL-DISP|v - `disp` residualised WITHIN STRATUM on log(IS book vol), then argmax'd - lands
BELOW the do-nothing anchor (the arm's mean OOS Sharpe) in 2 of 3 arms: OOS Sharpe 0.3494
(top10) and 0.2852 (top20) against anchors 0.6451 and 0.6860.  It read that as "the control
does not merely remove information, it inverts the ranking".

The queue asks whether that is a property of the CONTROL (a general pathology of controlled
characteristics) or a property of DISP.  This run repeats the selector construction for all
four of idea 284's characteristics - breadth, disp, corr, evol - under four transforms and
both directions, and asks the question the queue asks: **does a controlled characteristic
ever out-pick its own anchor?**

The honest form of that question is NOT "how often does a pick beat the mean".  Over 168
panels an arbitrary pick beats the arm's mean OOS Sharpe at a base rate this run measures
EXACTLY (the arm's own 168 OOS Sharpes are the complete uniform-pick null - no sampling), and
a within-stratum permutation of the characteristic gives the rate for a selector that ranks on
a structureless version of the same variable.  A beat rate inside those bands is not a finding,
and the headline below is written against them, not against 50%.

Design - the record's own books re-read under new selectors, no new dice
-----------------------------------------------------------------------
The object under test is a SELECTOR'S OOS RANKING, and the books it ranks are committed:
idea 533's `.arms.csv` carries all 504 arm-rows of idea 295's MIX ladder (k=40, 21 q rungs x 8
draws = 168 panels, seed 20260909; three books per panel - EWall / top10 / top20 - at gross
0.75, weekly, 10 bps, next-day execution, 260-day warm-up skip) with each panel's four
characteristics and each book's own realised vol, measured separately on full / IS / OOS.
Gates G1-G2 require idea 540's published selector table and idea 295's committed KEEP counts
to come back out of that artefact under this run's own fitters before one new number is read;
gate G3 rebuilds six of the 168 panels FROM TODAY'S PRICE FILES and reports the drift.

Tuned parameters (PROTOCOL rule 4: at most two) - ALL grid points reported
    1. characteristic in {breadth, disp, corr, evol}            (the queue's dial 1)
    2. transform    in {none, dm, residx, ratio}                (the queue's dial 2)
         none    x                            rank on the raw IS characteristic
         dm      x - mean(x | stratum)        within-stratum only, NO vol control; this is the
                 leg that separates "the control" from "the de-meaning", which idea 540's
                 single residx rung could not
         residx  dm(x) - b*dm(log bookvol_IS) idea 540's control, verbatim (FWL residue)
         ratio   x / bookvol_IS               the scale-free restatement of the same control
    Direction (argmax `+` / argmin `-`), arm (EWall/top10/top20) and the 21-stratum resolution
    are INHERITED from idea 540 and are reported axes, never tuned here.
    4 x 4 x 2 x 3 = 96 selector cells, every one published, plus SEL-S (argmax IS Sharpe, the
    record's own selector) and the ANCHOR row per arm.

Rule 8 walk-forward (PROTOCOL rule 8, required)
    Every selector is BUILT ON THE IS WINDOW ONLY (<= 2016-12-31) and read ONCE on the
    untouched OOS window (2017-01-01 .. end).  No selector sees an OOS number.  Each pick is
    reported as OOS CAGR / Sharpe / MaxDD against the do-nothing anchor, against RULES v2 on
    the same calendar, and against SPY on the same calendar, and BOTH KEEP PATHS (4a vs
    RULES v2, 4b vs SPY) are evaluated on every pick from idea 295's committed pass4a/pass4b.

Nulls (this is the part that decides the verdict)
    EXACT   the arm's 168 OOS Sharpes ARE the uniform-pick distribution.  Every pick is
            published with its percentile in that distribution, and the base rate
            P(uniform pick > anchor) is quoted per arm.
    PERM    the characteristic is permuted WITHIN STRATUM 200 times (seed 715) and every
            (transform, direction) selector re-run on the permuted variable, giving a
            per-(arm, transform, direction) band for the pick's OOS Sharpe and for the
            beat-anchor rate.  A real selector inside its own permutation band carries no
            information, whatever side of the anchor it lands on.

SURVIVORSHIP (idea 54, data/SMALL_PANEL_README.md): the small-cap end of the q ladder is the
CURRENT-constituent sub-$2B screen with the 44 max_1d_move >= 1.0 names dropped, and the
large-cap end is the current 136-name broad list; every LEVEL inherited here is optimistic.
The object under test is a selector's OOS RANKING against its own anchor and its own
permutation band, which is a within-ladder contrast, not a level claim.  No book in this file
is a capital candidate and none is proposed as one.

Outputs: .selectors.csv .permutation.csv .pairs.csv .walkforward.csv .keeppaths.csv
         .gate3.csv .console.txt .result.md
"""
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

BT = ROOT / "research" / "backtests"
P533 = BT / "2026-09-09_why-is-evol-the-one-characteristic-that-never-reverses_C"
P540 = BT / "2026-09-11_is-disp-the-SECOND-vol-channel_cloud"
OUT = Path(__file__).with_suffix("")

t0 = time.time()
LOG = []
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


CHARS = ["breadth", "disp", "corr", "evol"]          # tuned param 1
TRANSFORMS = ["none", "dm", "residx", "ratio"]       # tuned param 2
DIRS = ["+", "-"]
ARMS = ["EWall", "top10", "top20"]
NSTRAT = 21                                          # inherited from idea 540
N_PERM = 200
PERM_SEED = 715

# idea 295's ladder constants, needed only by gate G3
COST, FREQ = 10, "W"
K_MIX, N_DRAWS = 40, 8
QS = [round(x / 20, 2) for x in range(21)]
NS = [10, 20]
GROSS = 0.75
WARMUP = 260
IS_END = pd.Timestamp("2016-12-31")
SEED = 20260909

PUB_4A, PUB_4B, PUB_N = 0, 41, 504                   # idea 295/533's committed counts


# ------------------------------------------------- fitters, copied verbatim from idea 533/540
def ols(y, X):
    y = np.asarray(y, float); X = np.asarray(X, float)
    if X.ndim == 1: X = X[:, None]
    ok = np.isfinite(y) & np.isfinite(X).all(axis=1)
    y, X = y[ok], X[ok]
    n = len(y); p = X.shape[1]
    if n < p + 3 or any(np.std(X[:, j]) == 0 for j in range(p)):
        return np.full(p, np.nan), np.full(p, np.nan), n, 0, np.nan
    Z = np.column_stack([np.ones(n), X])
    beta, *_ = np.linalg.lstsq(Z, y, rcond=None)
    resid = y - Z @ beta
    dof = n - p - 1
    s2 = resid @ resid / dof
    XtXi = np.linalg.pinv(Z.T @ Z)
    se = np.sqrt(np.clip(np.diag(XtXi) * s2, 0, None))
    t = np.where(se[1:] > 0, beta[1:] / np.where(se[1:] > 0, se[1:], 1), np.nan)
    sst = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - float(resid @ resid) / sst if sst > 0 else np.nan
    return beta[1:], t, n, dof, r2


def bin_q(qv, nb):
    return np.minimum((np.asarray(qv, float) * nb).astype(int), nb - 1)


def demean(v, strat):
    g = pd.DataFrame(dict(s=strat, v=np.asarray(v, float)))
    return (g.v - g.groupby("s").v.transform("mean")).to_numpy()


def transform(x, lbv, st, meth):
    """The selector's ranking variable. x = IS characteristic, lbv = log(IS book vol)."""
    x = np.asarray(x, float)
    if meth == "none":
        return x
    if meth == "dm":
        return demean(x, st)
    if meth == "residx":
        dx, dv = demean(x, st), demean(lbv, st)
        b, _, _, _, _ = ols(dx, dv)
        return dx - b[0] * dv
    if meth == "ratio":
        with np.errstate(invalid="ignore", divide="ignore"):
            return x / np.exp(lbv)
    raise ValueError(meth)


def pick(v, direction):
    """Index of the selected panel; NaNs never win."""
    v = np.asarray(v, float)
    if not np.isfinite(v).any():
        return -1
    return int(np.nanargmax(v) if direction == "+" else np.nanargmin(v))


def main():
    P("=" * 104)
    P("IDEA 715 - is SEL-DISP|v's below-anchor pick a general CONTROLLED-CHARACTERISTIC pathology?")
    P("           (cloud, 2026-09-11; 4 characteristics x 4 transforms x 2 directions x 3 arms)")
    P("=" * 104)

    A = pd.read_csv(f"{P533}.arms.csv")
    P(f"\n[0] source artefact: {Path(str(P533)).name}.arms.csv  {A.shape[0]} arm-rows x {A.shape[1]} cols")
    P(f"    ladder: k={K_MIX}, {len(QS)} q rungs x {N_DRAWS} draws = {len(QS)*N_DRAWS} panels, seed {SEED}; "
      f"arms {ARMS}; gross {GROSS}, {FREQ}, {COST} bps, next-day execution")
    P(f"    rule 8: IS <= {IS_END.date()}, OOS {IS_END.date()}+1 .. end; selectors see IS ONLY")

    # =========================================================== GATES
    P("\n" + "=" * 104)
    P("GATES - nothing new is read until the parent's committed numbers come back out")
    P("=" * 104)

    # ---- G1: idea 540's four disp selectors, verbatim
    W540 = pd.read_csv(f"{P540}.walkforward.csv")
    g1 = []
    for arm in ARMS:
        sub = A[A.arm == arm].reset_index(drop=True)
        st = bin_q(sub["q"], NSTRAT)
        with np.errstate(invalid="ignore", divide="ignore"):
            lbv = np.log(sub["bookvol_IS"].to_numpy())
        dres = transform(sub["disp_IS"].to_numpy(), lbv, st, "residx")
        mine = {
            "SEL-S   argmax IS Sharpe": int(sub.Sharpe_IS.idxmax()),
            "SEL-DISP+ argmax IS disp": int(sub.disp_IS.idxmax()),
            "SEL-DISP- argmin IS disp": int(sub.disp_IS.idxmin()),
            "SEL-DISP|v argmax IS disp|log(vol)": pick(dres, "+"),
        }
        for name, i in mine.items():
            r = sub.loc[i]
            pub = W540[(W540.arm == arm) & (W540.selector == name)].iloc[0]
            g1.append(dict(arm=arm, selector=name,
                           d_q=abs(float(r.q) - float(pub.q)), d_draw=abs(int(r.draw) - int(pub.draw)),
                           d_OOS_S=abs(float(r.Sharpe_OOS) - float(pub.OOS_Sharpe)),
                           d_OOS_CAGR=abs(float(r.CAGR_OOS) - float(pub.OOS_CAGR)),
                           d_OOS_DD=abs(float(r.MaxDD_OOS) - float(pub.OOS_MaxDD)),
                           d_anchor=abs(float(sub.Sharpe_OOS.mean()) - float(pub.anchor_OOS_S))))
    G1 = pd.DataFrame(g1)
    g1max = float(G1[[c for c in G1.columns if c.startswith("d_")]].to_numpy().max())
    P(f"\n  G1  idea 540's 12 published selector rows re-derive from the arms file: "
      f"max |delta| over (q, draw, OOS CAGR/Sharpe/MaxDD, anchor) = {g1max:.3e}")
    assert g1max < 1e-9, f"G1 FAILED at {g1max:.3e}"
    P("      -> PASS (< 1e-9).  The two below-anchor cells the queue names are confirmed:")
    for arm in ("top10", "top20"):
        sub = A[A.arm == arm].reset_index(drop=True)
        st = bin_q(sub["q"], NSTRAT)
        with np.errstate(invalid="ignore", divide="ignore"):
            lbv = np.log(sub["bookvol_IS"].to_numpy())
        i = pick(transform(sub["disp_IS"].to_numpy(), lbv, st, "residx"), "+")
        P(f"      {arm:6s} SEL-DISP|v OOS Sharpe {sub.loc[i].Sharpe_OOS:.4f} vs anchor "
          f"{sub.Sharpe_OOS.mean():.4f}  (queue quotes "
          f"{'0.3494 vs 0.6451' if arm == 'top10' else '0.2852 vs 0.6860'})")

    # ---- G2: committed KEEP counts and the comparand rows
    n4a, n4b = int(A.pass4a.sum()), int(A.pass4b.sum())
    P(f"\n  G2  committed KEEP counts over the corpus: 4a {n4a}/{len(A)} (published {PUB_4A}), "
      f"4b {n4b}/{len(A)} (published {PUB_4B})")
    assert (n4a, n4b, len(A)) == (PUB_4A, PUB_4B, PUB_N), "G2 FAILED"
    spy_cols = ["SPY_OOS_Sharpe", "SPY_OOS_CAGR", "SPY_OOS_MaxDD", "SPY_Sharpe"]
    v2_cols = ["base_OOS_Sharpe", "base_OOS_CAGR", "base_OOS_MaxDD"]
    spy_sd = float(A[spy_cols].std().max())
    v2_sd = float(A[v2_cols].std().max())
    P(f"      SPY is ONE series and is constant across all {len(A)} rows (max sd {spy_sd:.3e}): "
      f"OOS {A.SPY_OOS_CAGR.iloc[0]:+.4f}/{A.SPY_OOS_Sharpe.iloc[0]:.4f}/"
      f"{A.SPY_OOS_MaxDD.iloc[0]:+.4f}")
    assert spy_sd < 1e-9 and n4a == PUB_4A, "G2 FAILED (SPY comparand drifts)"
    P(f"      CORRECTION TO IDEA 540: RULES v2 is NOT a constant here — it is re-run on EACH "
      f"PANEL'S OWN 40 names, so `base_*` varies across the {len(A)} rows (max sd {v2_sd:.4f}). "
      f"OOS Sharpe mean {A.base_OOS_Sharpe.mean():.4f}, range "
      f"[{A.base_OOS_Sharpe.min():.4f}, {A.base_OOS_Sharpe.max():.4f}]; OOS CAGR mean "
      f"{A.base_OOS_CAGR.mean():+.4f}, MaxDD mean {A.base_OOS_MaxDD.mean():+.4f}.")
    P(f"      Idea 540's console printed `RULES v2 OOS +0.0792/1.0616/-0.1141` as THE comparand; "
      f"that is row 0's panel (q=0.00, draw=0) alone and sits at the "
      f"{float((A.base_OOS_Sharpe <= A.base_OOS_Sharpe.iloc[0]).mean()):.1%} percentile of the "
      f"504. Its per-row `beats_v2` flags are unaffected (they used each row's own base); the "
      f"header line is. This run quotes RULES v2 per row and as a distribution, never as a scalar.")
    P("      -> PASS (on the clause that is assertable), 1 DRIFT RECORDED")

    # ---- G3: rebuild 6 of the 168 panels from today's price files
    P("\n  G3  FRESH REBUILD of 6 of the 168 panels from today's data files (vintage check)")
    G3 = gate3(A)

    # =========================================================== the grid
    P("\n" + "=" * 104)
    P("THE GRID - 96 IS-ONLY selectors (4 characteristics x 4 transforms x 2 directions x 3 arms)")
    P("=" * 104)
    rows, base_rate = [], {}
    for arm in ARMS:
        sub = A[A.arm == arm].reset_index(drop=True)
        st = bin_q(sub["q"], NSTRAT)
        with np.errstate(invalid="ignore", divide="ignore"):
            lbv = np.log(sub["bookvol_IS"].to_numpy())
        oos = sub.Sharpe_OOS.to_numpy()
        anchor_S, anchor_C = float(oos.mean()), float(sub.CAGR_OOS.mean())
        anchor_D = float(sub.MaxDD_OOS.mean())
        base_rate[arm] = float((oos > anchor_S).mean())
        rows.append(dict(arm=arm, char="-", transform="-", direction="-", selector="ANCHOR (arm mean)",
                         q=np.nan, draw=-1, IS_Sharpe=float(sub.Sharpe_IS.mean()),
                         OOS_CAGR=anchor_C, OOS_Sharpe=anchor_S, OOS_MaxDD=anchor_D,
                         anchor_OOS_S=anchor_S, pct=np.nan, beats_anchor=False,
                         v2_OOS_S=float(sub.base_OOS_Sharpe.mean()),
                         v2_OOS_CAGR=float(sub.base_OOS_CAGR.mean()),
                         v2_OOS_DD=float(sub.base_OOS_MaxDD.mean()),
                         beats_v2=bool(anchor_S > sub.base_OOS_Sharpe.mean()),
                         beats_spy=bool(anchor_S > sub.SPY_OOS_Sharpe.iloc[0]),
                         pass4a=False, pass4b=False))
        i = int(sub.Sharpe_IS.idxmax())
        rows.append(sel_row(sub, i, arm, "-", "-", "+", "SEL-S argmax IS Sharpe", oos, anchor_S))
        for ch in CHARS:
            x = sub[f"{ch}_IS"].to_numpy()
            for meth in TRANSFORMS:
                v = transform(x, lbv, st, meth)
                for d in DIRS:
                    i = pick(v, d)
                    rows.append(sel_row(sub, i, arm, ch, meth, d,
                                        f"SEL-{ch}{d}|{meth}", oos, anchor_S))
    S = pd.DataFrame(rows)
    S.to_csv(f"{OUT}.selectors.csv", index=False)

    P("\n  base rate of the EXACT uniform-pick null (the arm's own 168 OOS Sharpes):")
    for arm in ARMS:
        sub = A[A.arm == arm]
        P(f"    {arm:6s} anchor {sub.Sharpe_OOS.mean():.4f}  P(random pick > anchor) = "
          f"{base_rate[arm]:.4f}   min {sub.Sharpe_OOS.min():.4f} / med "
          f"{sub.Sharpe_OOS.median():.4f} / max {sub.Sharpe_OOS.max():.4f}")

    real = S[S.char != "-"]
    P(f"\n  all {len(real)} selector cells (pct = percentile of the pick in its arm's 168 OOS Sharpes):")
    P(real[["arm", "char", "transform", "direction", "q", "draw", "IS_Sharpe", "OOS_CAGR",
            "OOS_Sharpe", "OOS_MaxDD", "anchor_OOS_S", "pct", "beats_anchor", "beats_v2",
            "beats_spy", "pass4a", "pass4b"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("\n  beat-anchor counts by transform (out of 24 cells each: 4 chars x 2 directions x 3 arms):")
    tb = real.groupby("transform").agg(cells=("beats_anchor", "size"),
                                       beat=("beats_anchor", "sum"),
                                       mean_pct=("pct", "mean"),
                                       mean_OOS_S=("OOS_Sharpe", "mean"),
                                       beat_v2=("beats_v2", "sum"),
                                       beat_spy=("beats_spy", "sum"),
                                       p4b=("pass4b", "sum")).reindex(TRANSFORMS)
    P(tb.to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n  beat-anchor counts by characteristic (out of 24 each: 4 transforms x 2 dirs x 3 arms):")
    cb = real.groupby("char").agg(cells=("beats_anchor", "size"), beat=("beats_anchor", "sum"),
                                  mean_pct=("pct", "mean"), mean_OOS_S=("OOS_Sharpe", "mean"),
                                  p4b=("pass4b", "sum")).reindex(CHARS)
    P(cb.to_string(float_format=lambda x: f"{x:.4f}"))

    # =========================================================== the permutation null
    P("\n" + "=" * 104)
    P(f"PERMUTATION NULL - characteristic permuted WITHIN STRATUM {N_PERM}x (seed {PERM_SEED}), "
      "every selector re-run")
    P("=" * 104)
    rng = np.random.default_rng(PERM_SEED)
    perm_rows = []
    for arm in ARMS:
        sub = A[A.arm == arm].reset_index(drop=True)
        st = bin_q(sub["q"], NSTRAT)
        with np.errstate(invalid="ignore", divide="ignore"):
            lbv = np.log(sub["bookvol_IS"].to_numpy())
        oos = sub.Sharpe_OOS.to_numpy()
        anchor = float(oos.mean())
        groups = [np.where(st == s)[0] for s in np.unique(st)]
        for ch in CHARS:
            x0 = sub[f"{ch}_IS"].to_numpy()
            draws = {(m, d): [] for m in TRANSFORMS for d in DIRS}
            for _ in range(N_PERM):
                xp = x0.copy()
                for g in groups:
                    xp[g] = x0[rng.permutation(g)]
                for m in TRANSFORMS:
                    v = transform(xp, lbv, st, m)
                    for d in DIRS:
                        draws[(m, d)].append(oos[pick(v, d)])
            for (m, d), vals in draws.items():
                vals = np.asarray(vals, float)
                cell = S[(S.arm == arm) & (S.char == ch) & (S["transform"] == m) & (S.direction == d)]
                obs = float(cell.OOS_Sharpe.iloc[0])
                perm_rows.append(dict(arm=arm, char=ch, transform=m, direction=d,
                                      obs_OOS_S=obs, perm_mean=float(vals.mean()),
                                      perm_p05=float(np.percentile(vals, 5)),
                                      perm_p95=float(np.percentile(vals, 95)),
                                      perm_beat_rate=float((vals > anchor).mean()),
                                      obs_beats_anchor=bool(obs > anchor),
                                      obs_in_band=bool(np.percentile(vals, 5) <= obs
                                                       <= np.percentile(vals, 95)),
                                      p_two_sided=float(
                                          2 * min((vals <= obs).mean(), (vals >= obs).mean()))))
        P(f"    {arm} done ({time.time()-t0:5.1f}s)")
    PM = pd.DataFrame(perm_rows)
    PM.to_csv(f"{OUT}.permutation.csv", index=False)
    P("\n  permutation summary by transform (96 cells; 'in band' = observed inside its own "
      "[p05, p95]):")
    pt = PM.groupby("transform").agg(cells=("obs_in_band", "size"),
                                     in_band=("obs_in_band", "sum"),
                                     obs_beat=("obs_beats_anchor", "sum"),
                                     perm_beat_rate=("perm_beat_rate", "mean"),
                                     obs_mean=("obs_OOS_S", "mean"),
                                     perm_mean=("perm_mean", "mean")).reindex(TRANSFORMS)
    P(pt.to_string(float_format=lambda x: f"{x:.4f}"))
    P(f"\n  cells that separate from their own null (p < 0.05, two-sided): "
      f"{int((PM.p_two_sided < 0.05).sum())} of {len(PM)}")
    sep = PM[PM.p_two_sided < 0.05].sort_values("p_two_sided")
    if len(sep):
        P(sep.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # =========================================================== controlled vs uncontrolled
    P("\n" + "=" * 104)
    P("THE QUEUE'S QUESTION - does the CONTROL help or hurt, paired against its own uncontrolled twin?")
    P("=" * 104)
    pairs = []
    for arm in ARMS:
        for ch in CHARS:
            for d in DIRS:
                def g(m):
                    return S[(S.arm == arm) & (S.char == ch) & (S["transform"] == m)
                             & (S.direction == d)].iloc[0]
                n_, dm_, rx_, rt_ = g("none"), g("dm"), g("residx"), g("ratio")
                pairs.append(dict(arm=arm, char=ch, direction=d,
                                  none_S=n_.OOS_Sharpe, dm_S=dm_.OOS_Sharpe,
                                  residx_S=rx_.OOS_Sharpe, ratio_S=rt_.OOS_Sharpe,
                                  anchor=n_.anchor_OOS_S,
                                  d_residx_none=rx_.OOS_Sharpe - n_.OOS_Sharpe,
                                  d_residx_dm=rx_.OOS_Sharpe - dm_.OOS_Sharpe,
                                  residx_below_anchor=bool(rx_.OOS_Sharpe < n_.anchor_OOS_S),
                                  none_below_anchor=bool(n_.OOS_Sharpe < n_.anchor_OOS_S)))
    PR = pd.DataFrame(pairs)
    PR.to_csv(f"{OUT}.pairs.csv", index=False)
    P(PR.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n  residx below its arm's anchor in {int(PR.residx_below_anchor.sum())} of {len(PR)} "
      f"(char, direction, arm) cells; the UNCONTROLLED twin below anchor in "
      f"{int(PR.none_below_anchor.sum())} of {len(PR)}")
    P(f"  control vs raw        : mean d(OOS Sharpe) {PR.d_residx_none.mean():+.4f}, "
      f"median {PR.d_residx_none.median():+.4f}, helps in {int((PR.d_residx_none > 0).sum())} of {len(PR)}")
    P(f"  control vs de-meaning : mean d(OOS Sharpe) {PR.d_residx_dm.mean():+.4f}, "
      f"median {PR.d_residx_dm.median():+.4f}, helps in {int((PR.d_residx_dm > 0).sum())} of {len(PR)}")
    P("  (the second line is the one that isolates THE VOL CONTROL from the within-stratum "
      "de-meaning it is bundled with.)")

    # =========================================================== rule 8 / KEEP paths
    P("\n" + "=" * 104)
    P("RULE 8 WALK-FORWARD + BOTH KEEP PATHS - every pick read once on OOS vs RULES v2 and SPY")
    P("=" * 104)
    spS, spC, spD = (float(A.SPY_OOS_Sharpe.iloc[0]), float(A.SPY_OOS_CAGR.iloc[0]),
                     float(A.SPY_OOS_MaxDD.iloc[0]))
    P(f"  SPY on the same OOS calendar (one series, constant): {spC:+.4f}/{spS:.4f}/{spD:+.4f}")
    P(f"  RULES v2 is per-panel: OOS Sharpe mean {A.base_OOS_Sharpe.mean():.4f} "
      f"[{A.base_OOS_Sharpe.min():.4f}, {A.base_OOS_Sharpe.max():.4f}], CAGR mean "
      f"{A.base_OOS_CAGR.mean():+.4f}, MaxDD mean {A.base_OOS_MaxDD.mean():+.4f}; every "
      f"`beats_v2` below compares a pick against RULES v2 ON ITS OWN PANEL, which is the only "
      f"matched reading.")
    WF = S.copy()
    WF["spy_OOS_S"], WF["spy_OOS_CAGR"], WF["spy_OOS_DD"] = spS, spC, spD
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(f"\n  over the {len(real)} characteristic selectors: beat the anchor "
      f"{int(real.beats_anchor.sum())} ({real.beats_anchor.mean():.1%}, exact null "
      f"{np.mean([base_rate[a] for a in ARMS]):.1%}), beat RULES v2 {int(real.beats_v2.sum())}, "
      f"beat SPY {int(real.beats_spy.sum())}; KEEP 4a {int(real.pass4a.sum())}, "
      f"4b {int(real.pass4b.sum())}")
    anch = S[S.selector == "ANCHOR (arm mean)"]
    sels = S[S.selector == "SEL-S argmax IS Sharpe"]
    P(f"  the ANCHOR rows themselves: beat RULES v2 {int(anch.beats_v2.sum())}/3, "
      f"beat SPY {int(anch.beats_spy.sum())}/3")
    P(f"  the record's own SEL-S    : beat anchor {int(sels.beats_anchor.sum())}/3, "
      f"beat RULES v2 {int(sels.beats_v2.sum())}/3, beat SPY {int(sels.beats_spy.sum())}/3, "
      f"4b {int(sels.pass4b.sum())}/3")
    KP = real.groupby(["transform", "direction"]).agg(
        cells=("pass4b", "size"), pass4a=("pass4a", "sum"), pass4b=("pass4b", "sum"),
        beat_anchor=("beats_anchor", "sum"), beat_v2=("beats_v2", "sum"),
        beat_spy=("beats_spy", "sum"))
    KP.to_csv(f"{OUT}.keeppaths.csv")
    P("\n  KEEP paths by (transform, direction):")
    P(KP.to_string())

    # =========================================================== verdict
    P("\n" + "=" * 104)
    P("VERDICT")
    P("=" * 104)
    rx = real[real["transform"] == "residx"]
    rx_beat = int(rx.beats_anchor.sum())
    perm_rx = PM[PM["transform"] == "residx"]
    exp_rx = float(perm_rx.perm_beat_rate.mean()) * len(rx)
    P(f"  a CONTROLLED characteristic (residx) out-picks its own anchor in {rx_beat} of {len(rx)} "
      f"cells; its own within-stratum permutation expects {exp_rx:.1f} and the exact uniform-pick "
      f"null expects {np.mean([base_rate[a] for a in ARMS])*len(rx):.1f}")
    P(f"  {int((PM.p_two_sided < 0.05).sum())} of {len(PM)} selector cells separate from their own "
      f"permutation null at p<0.05 (expected at chance: {0.05*len(PM):.1f})")
    P(f"  KEEP 4a {int(real.pass4a.sum())}/{len(real)}, 4b {int(real.pass4b.sum())}/{len(real)} "
      f"over the characteristic selectors; corpus 4a {n4a}/{len(A)}, 4b {n4b}/{len(A)}")
    verdict = ("KILL" if int(real.pass4a.sum()) == 0 and int(real.pass4b.sum()) <= n4b / len(A) * len(real) * 2
               else "PARK")
    P(f"  VERDICT: {verdict} — see .result.md for the wording.")

    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    P(f"\n  wall {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return S, PM, PR, G1, G3, base_rate, verdict


def sel_row(sub, i, arm, ch, meth, d, name, oos, anchor_S):
    if i < 0:
        return dict(arm=arm, char=ch, transform=meth, direction=d, selector=name,
                    q=np.nan, draw=-1, IS_Sharpe=np.nan, OOS_CAGR=np.nan, OOS_Sharpe=np.nan,
                    OOS_MaxDD=np.nan, anchor_OOS_S=anchor_S, pct=np.nan, beats_anchor=False,
                    v2_OOS_S=np.nan, v2_OOS_CAGR=np.nan, v2_OOS_DD=np.nan,
                    beats_v2=False, beats_spy=False, pass4a=False, pass4b=False)
    r = sub.loc[i]
    return dict(arm=arm, char=ch, transform=meth, direction=d, selector=name,
                q=float(r.q), draw=int(r.draw), IS_Sharpe=float(r.Sharpe_IS),
                OOS_CAGR=float(r.CAGR_OOS), OOS_Sharpe=float(r.Sharpe_OOS),
                OOS_MaxDD=float(r.MaxDD_OOS), anchor_OOS_S=anchor_S,
                pct=float((oos <= r.Sharpe_OOS).mean()),
                beats_anchor=bool(r.Sharpe_OOS > anchor_S),
                v2_OOS_S=float(r.base_OOS_Sharpe), v2_OOS_CAGR=float(r.base_OOS_CAGR),
                v2_OOS_DD=float(r.base_OOS_MaxDD),
                beats_v2=bool(r.Sharpe_OOS > r.base_OOS_Sharpe),
                beats_spy=bool(r.Sharpe_OOS > r.SPY_OOS_Sharpe),
                pass4a=bool(r.pass4a), pass4b=bool(r.pass4b))


# ------------------------------------------------------------------ gate G3: fresh rebuild
def gate3(A, n_check=6):
    """Replay idea 295's seed-20260909 draw, rebuild n_check panels from TODAY'S data files,
    and report the drift of the committed IS-window numbers.  Recorded, not asserted: the
    price panels have a VINTAGE (idea 514) and the full/OOS windows grow every session."""
    import json
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    ETFS = set(U["broad"]) | set(U["sectors"]) | set(U["bonds_fx_commod"])
    pxb = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    BAD = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])   # PROTOCOL: dropped FIRST
    S_STK = [c for c in pxs.columns if c != "SPY" and c not in BAD]
    B_STK = [c for c in pxb.columns if c != "SPY" and c not in ETFS]
    SPY_RAW = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)["SPY"]
    COMMON = pxs.index
    P(f"      small panel {len(BAD)} names with max_1d_move >= 1.0 dropped first, {len(S_STK)} usable; "
      f"large-cap stock pool {len(B_STK)}; common window {COMMON[0].date()}..{COMMON[-1].date()} "
      f"({len(COMMON)} rows)")

    rng = np.random.default_rng(SEED)
    panels = []
    for q in QS:
        ns_ = int(round(q * K_MIX)); nl_ = K_MIX - ns_
        for d in range(N_DRAWS):
            sc = list(rng.choice(S_STK, size=ns_, replace=False)) if ns_ else []
            lc = list(rng.choice(B_STK, size=nl_, replace=False)) if nl_ else []
            panels.append((q, d, sc, lc))

    step = max(1, len(panels) // n_check)
    chosen = panels[::step][:n_check]

    def mk(cols_s, cols_l):
        parts = []
        if cols_s: parts.append(pxs[cols_s])
        if cols_l: parts.append(pxb[cols_l].reindex(COMMON, method="ffill"))
        px = pd.concat(parts, axis=1).reindex(COMMON).dropna(how="all").ffill()
        return px.join(SPY_RAW.reindex(px.index, method="ffill").rename("SPY"))

    def panel_chars(px, cols, elig, lo, hi):
        m = rebalance_mask(px.index, FREQ)
        idx = px.loc[px.index[WARMUP]:].index
        if lo is not None: idx = idx[idx >= lo]
        if hi is not None: idx = idx[idx <= hi]
        rb = idx[m.reindex(idx).fillna(False).values]
        e = elig.loc[rb, cols]; k = len(cols)
        nel = e.sum(axis=1)
        r63 = (px[cols] / px[cols].shift(63) - 1).loc[rb]
        vol20 = (px[cols].pct_change().rolling(20).std() * np.sqrt(252)).loc[rb]
        dr = px[cols].pct_change().loc[idx]
        C = dr.corr().to_numpy(); iu = np.triu_indices(k, 1)
        return dict(breadth=float((nel / k).mean()),
                    disp=float(r63.where(e).std(axis=1, ddof=0).mean()),
                    evol=float(vol20.where(e).mean(axis=1).mean()),
                    corr=float(np.nanmean(C[iu])) if k > 1 else np.nan)

    out = []
    for q, d, sc, lc in chosen:
        px = mk(sc, lc)
        tr = [c for c in px.columns if c != "SPY"]
        start = px.index[WARMUP]
        s, above, vol20 = score(px[tr], vol_scale=False)
        el = s.where(above & (vol20 < 0.60))
        elig = el.notna()
        ch_is = panel_chars(px, tr, elig, None, IS_END)
        rank = el.rank(axis=1, ascending=False)
        e01 = elig.astype(float); cnt = e01.sum(axis=1).replace(0, np.nan)
        specs = [("EWall", (GROSS * e01.div(cnt, axis=0)).reindex(columns=px.columns).fillna(0.0))]
        for n in NS:
            specs.append((f"top{n}", ((rank <= n).astype(float) * (GROSS / n))
                          .reindex(columns=px.columns).fillna(0.0)))
        for arm, w in specs:
            r = backtest(px, w, cost_bps=COST, freq=FREQ)["returns"].loc[start:]
            m_is = metrics(r.loc[:IS_END])
            com = A[(np.isclose(A.q, q)) & (A.draw == d) & (A.arm == arm)]
            if not len(com):
                continue
            com = com.iloc[0]
            out.append(dict(q=q, draw=d, arm=arm,
                            d_Sharpe_IS=abs(m_is["Sharpe"] - float(com.Sharpe_IS)),
                            d_CAGR_IS=abs(m_is["CAGR"] - float(com.CAGR_IS)),
                            d_MaxDD_IS=abs(m_is["MaxDD"] - float(com.MaxDD_IS)),
                            **{f"d_{c}_IS": abs(ch_is[c] - float(com[f"{c}_IS"])) for c in CHARS}))
    G3 = pd.DataFrame(out)
    G3.to_csv(f"{OUT}.gate3.csv", index=False)
    dmax = float(G3[[c for c in G3.columns if c.startswith("d_")]].to_numpy().max())
    P(G3.to_string(index=False, float_format=lambda x: f"{x:.3e}"))
    P(f"      max |delta| on the IS window over {len(G3)} rebuilt books "
      f"(3 arms x {len(G3)//3} panels) = {dmax:.3e}")
    P("      -> " + ("PASS (< 1e-9): the committed ladder reproduces bit-for-bit on today's files."
                     if dmax < 1e-9 else
                     f"DRIFT RECORDED at {dmax:.3e} — panel vintage, reported not asserted."))
    return G3


if __name__ == "__main__":
    main()

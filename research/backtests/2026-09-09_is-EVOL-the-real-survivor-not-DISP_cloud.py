#!/usr/bin/env python3
"""Idea 310 - "is-EVOL-the-real-survivor-not-DISP" (cloud, 2026-09-09).

The question
------------
Idea 284 measured the within-stratum rank-partial of four panel characteristics against OOS
Sharpe at ONE stratum (q = 0.500, k = 40) and published: `disp` SURVIVES the control for the
other three (+0.264 / +0.247 / +0.261 on CAND10 / CAND20 / EWall) while `evol` COLLAPSES
(-0.126 / +0.031 / -0.073, "mediated by the other two").  Idea 293 re-ran the identical
construction over nine strata (q x k) and its committed .strata.csv gives the OPPOSITE mean
ordering across the 27 (stratum x book) points: evol +0.1551, disp +0.0046.

The queue's question is exact: re-fit both partials stratum by stratum, report which of the two
is stable in SIGN and SIZE, and report whether the disagreement is the k = 40 / q = 0.500 cell
alone.

Data
----
Idea 293's committed panel-level artefact
`2026-09-06_does-the-CORR-ordering-hold-off-q-0.5_cloud.panels.csv`
(540 seeded panels = 9 strata x 60 draws, plus 5 NAMED panels which are EXCLUDED from every
within-stratum fit), carrying each panel's four IS characteristics and each book's full-sample,
IS and OOS metrics.  The fit is recomputed here from those inputs -- nothing is copied from
idea 293's fitted column except as a reproduction gate.

Design (fixed before any new number was computed)
-------------------------------------------------
FIXED, never varied (inherited resolution, not dials):
    strata      q in {0.25, 0.50, 0.75} x k in {20, 40, 80}, 60 seeded draws each -- idea 293's
                grid verbatim; the (0.500, 40) cell is idea 284's stratum bit-identically
    books       CAND10, CAND20, EWall -- all three always reported, none selected on
    outcome     OOS Sharpe (2017-01-01..end), characteristics measured on IS (<= 2016-12-31)
    focus       disp and evol; breadth and corr are carried as reported comparands

TUNED PARAMETERS -- exactly two:
    1. CONTROL SET (3):  REC     = the other three characteristics (idea 284/293's control)
                         PLUSN   = the other three + n_elig (panel width, the mechanical
                                   confound the record's own idea 286 names)
                         MINIMAL = only the two characteristics that are neither disp nor evol
                                   (breadth, corr) -- so disp and evol never control each other
    2. ESTIMATOR (2):    RANKPART = rank-partial correlation (the record's estimator verbatim)
                         OLSZ     = OLS t-statistic on z-scored ranks, same control set
    3 x 2 x 9 strata x 3 books x 2 characteristics = 324 fitted partials, ALL reported.

Pre-registered bars, written before any new number was computed
---------------------------------------------------------------
B1  SIGN STABILITY.  Per characteristic, per (control set, estimator): the share of the 27
    (stratum x book) points holding the pooled sign.  "Stable in sign" = >= 24/27 (i.e. at most
    one stratum dissenting in all three books).
B2  SIZE STABILITY.  Per characteristic: mean, SD and range across the 27 points, and the ratio
    |mean| / SD.  "Stable in size" = |mean| / SD >= 1.
B3  IS THE DISAGREEMENT ONE CELL?  Leave-one-stratum-out: recompute the 27-point mean with each
    stratum dropped, and report the ordering (evol vs disp) with and without (q 0.500, k 40).
    The cell is "the whole disagreement" iff dropping it flips the published mean ordering AND
    no other single stratum does.
B4  SEED SPLIT-HALF.  Refit every partial on seeds 0-29 and 30-59 separately (idea 284's own
    replication device) and report sign agreement between halves per characteristic.
B5  RULE 8 (PROTOCOL 8), out-of-sample in TWO directions:
    (a) TIME: characteristics are IS-only (<= 2016) and every book metric read is OOS
        (>= 2017) -- inherited from the construction.
    (b) DRAW: the selector direction is FIT on seeds 0-29 (the sign of that half's partial) and
        APPLIED to seeds 30-59 -- pick the extreme panel of the untouched half in the fitted
        direction, read its OOS book ONCE.  Reported against the half's do-nothing anchor
        (mean OOS Sharpe of the 30 unseen draws), SPY and RULES v2.
B6  BOTH KEEP PATHS on every selected panel-book:
    4a  Sharpe > RULES v2 in BOTH halves AND MaxDD no worse than RULES v2.
    4b  Sharpe > SPY in BOTH halves AND OOS, |MaxDD| <= 60% of SPY's, CAGR >= 70% of SPY's.

Gates (asserted before any verdict is read)
    G1  the RANKPART/REC re-fit reproduces idea 293's committed `rho_partial` on all 108
        (stratum x book x characteristic) rows to < 1e-12.
    G2  the (q 0.500, k 40) cell reproduces idea 284's published disp (+0.264/+0.247/+0.261)
        and evol (-0.126/+0.031/-0.073) to < 1e-3 (its printed precision).
    G3  the seeded panel file carries exactly 9 strata x 60 draws and no NAMED panel enters any
        within-stratum fit.

SURVIVORSHIP: the panels are drawn from SMALL439 and BSTK100, both CURRENT constituents of their
screens, so every panel's return LEVEL is inflated and the KEEP columns inherit that whole; the
44 SMALL439 tickers with max_1d_move >= 1.0 were already dropped by idea 293 before any draw.
This run tests whether a characteristic ORDERS panels inside a fixed cap mix, which the bias
does not create, but a "the ordering is real" verdict is a within-corpus regularity only, never
a tradable edge.

Deterministic, standalone.  Reads only committed artefacts; modifies nothing outside its outputs.
Outputs: .partials.csv .stability.csv .loso.csv .splithalf.csv .walkforward.csv .console.txt .result.md
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd

SRC = REPO / "research" / "backtests" / "2026-09-06_does-the-CORR-ordering-hold-off-q-0.5_cloud"
CHARS = ["breadth", "disp", "corr", "evol"]
FOCUS = ["disp", "evol"]
BOOKS = ["CAND10", "CAND20", "EWall"]
QS = [0.25, 0.50, 0.75]
KS = [20, 40, 80]
CELL284 = (0.50, 40)
CONTROL_SETS = ["REC", "PLUSN", "MINIMAL"]
ESTIMATORS = ["RANKPART", "OLSZ"]
REC_EST, REC_CTRL = "RANKPART", "REC"
N_SEEDS = 60
SIGN_BAR = 24          # B1: >= 24/27 points holding the pooled sign
SIZE_BAR = 1.0         # B2: |mean| / SD
PUB_284 = {"disp": [0.264, 0.247, 0.261], "evol": [-0.126, 0.031, -0.073]}   # CAND10/CAND20/EWall

OUT = Path(__file__).with_suffix("")
LOG = []
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 500)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ---------------------------------------------------------------- estimators
def rk(v):
    v = pd.Series(np.asarray(v, float)).rank().to_numpy()
    return (v - v.mean()) / (v.std() if v.std() > 0 else 1.0)


def rank_partial(y, x, controls):
    """Idea 284/293's estimator verbatim: rank all, residualise on controls, correlate."""
    Y, X = rk(y), rk(x)
    C = np.column_stack([np.ones(len(Y))] + [rk(c) for c in controls])
    B = np.linalg.pinv(C.T @ C) @ C.T
    ry = Y - C @ (B @ Y)
    rx = X - C @ (B @ X)
    if ry.std() == 0 or rx.std() == 0:
        return np.nan, np.nan
    rho = float(np.corrcoef(rx, ry)[0, 1])
    n, p = len(Y), C.shape[1] + 1
    dof = max(1, n - p)
    t = rho * np.sqrt(dof / max(1e-12, 1 - rho ** 2))
    return rho, float(t)


def ols_z(y, x, controls):
    """Same control set, OLS on z-scored ranks; returns the focal beta and its t."""
    Y = rk(y)
    X = np.column_stack([np.ones(len(Y)), rk(x)] + [rk(c) for c in controls])
    XtXi = np.linalg.pinv(X.T @ X)
    b = XtXi @ (X.T @ Y)
    e = Y - X @ b
    n, p = X.shape
    dof = max(1, n - p)
    s2 = float(e @ e) / dof
    se = np.sqrt(np.diag(XtXi) * s2)
    return float(b[1]), float(b[1] / se[1]) if se[1] > 0 else np.nan


def controls_for(char, ctrl, d):
    if ctrl == "REC":
        names = [c for c in CHARS if c != char]
    elif ctrl == "PLUSN":
        names = [c for c in CHARS if c != char] + ["n_elig"]
    else:                                    # MINIMAL: never let disp and evol control each other
        names = [c for c in CHARS if c not in FOCUS]
    cols = []
    for nm in names:
        cols.append(d["n_elig_IS"].to_numpy() if nm == "n_elig" else d[f"{nm}_IS"].to_numpy())
    return names, cols


def fit(char, ctrl, est, d, book):
    names, cols = controls_for(char, ctrl, d)
    y = d[f"{book}_OOS_Sharpe"].to_numpy()
    x = d[f"{char}_IS"].to_numpy()
    if est == "RANKPART":
        v, t = rank_partial(y, x, cols)
    else:
        v, t = ols_z(y, x, cols)
    return v, t, names


# ---------------------------------------------------------------- keep paths
def keep4a(r, book):
    return bool(r[f"{book}_H1"] > r["v2_H1"] and r[f"{book}_H2"] > r["v2_H2"]
                and r[f"{book}_MaxDD"] >= r["v2_MaxDD"])


def bars4b(r, book):
    return {"H1": r[f"{book}_H1"] > r["SPY_H1"], "H2": r[f"{book}_H2"] > r["SPY_H2"],
            "OOS": r[f"{book}_OOS_Sharpe"] > r["SPY_OOS_Sharpe"],
            "DD": abs(r[f"{book}_MaxDD"]) <= 0.60 * abs(r["SPY_MaxDD"]),
            "CAGR": r[f"{book}_CAGR"] >= 0.70 * r["SPY_CAGR"]}


def fail4b(r, book):
    f = [k for k, v in bars4b(r, book).items() if not v]
    return ",".join(f) if f else "-"


# ---------------------------------------------------------------- main
def main():
    P("=" * 170)
    P("Idea 310 is-EVOL-the-real-survivor-not-DISP (cloud) | " + Path(__file__).name)
    P("=" * 170)
    P("Source: idea 293's committed panels.csv (540 seeded panels, 9 strata x 60 draws) + 5 NAMED "
      "panels EXCLUDED from every fit.")
    P(f"DIALS (2): CONTROL SET {CONTROL_SETS} x ESTIMATOR {ESTIMATORS}.  "
      f"Strata (q x k) and the three books are inherited resolution, not dials.")
    P(f"Record's published estimator = {REC_EST}/{REC_CTRL}.  Focus characteristics {FOCUS}; "
      f"breadth and corr reported beside them.")
    P("SURVIVORSHIP: SMALL439/BSTK100 are current constituents; every panel's return level is "
      "inflated and both KEEP columns inherit that whole.")

    pan = pd.read_csv(f"{SRC}.panels.csv")
    seeded = pan[pan.kind != "NAMED"].copy()
    seeded["q"] = seeded["q"].astype(float)
    seeded["k"] = seeded["k"].astype(int)

    # ---------------------------------------------------------- G3
    P("\n" + "=" * 170)
    P("GATES")
    counts = seeded.groupby(["k", "q"]).size()
    ok3 = (len(counts) == 9) and bool((counts == N_SEEDS).all()) and (len(pan) - len(seeded) == 5)
    P(f"  G3 strata {len(counts)} (expect 9), draws per stratum "
      f"{sorted(set(counts.values))} (expect [{N_SEEDS}]), NAMED excluded "
      f"{len(pan) - len(seeded)} (expect 5)  ({'PASS' if ok3 else 'FAIL'})")
    assert ok3

    # ---------------------------------------------------------- the 324 fits
    rows = []
    for ctrl in CONTROL_SETS:
        for est in ESTIMATORS:
            for k in KS:
                for q in QS:
                    d = seeded[(seeded.k == k) & (np.isclose(seeded.q, q))]
                    for book in BOOKS:
                        for char in CHARS:
                            v, t, names = fit(char, ctrl, est, d, book)
                            raw = float(np.corrcoef(rk(d[f"{char}_IS"]),
                                                    rk(d[f"{book}_OOS_Sharpe"]))[0, 1])
                            rows.append(dict(ctrl=ctrl, est=est, k=k, q=q, book=book, char=char,
                                             n=len(d), value=v, t=t, raw_rho=raw,
                                             controls="+".join(names),
                                             is284cell=bool((q, k) == CELL284)))
    F = pd.DataFrame(rows)
    F.to_csv(f"{OUT}.partials.csv", index=False)

    # ---------------------------------------------------------- G1 / G2
    ref = pd.read_csv(f"{SRC}.strata.csv")
    m = F[(F.ctrl == REC_CTRL) & (F.est == REC_EST)].merge(
        ref[["k", "q", "book", "char", "rho_partial"]], on=["k", "q", "book", "char"])
    g1 = float((m.value - m.rho_partial).abs().max())
    P(f"  G1 re-fit vs idea 293's committed rho_partial on {len(m)} rows: max abs diff "
      f"{g1:.3e} ({'PASS' if g1 < 1e-12 else 'FAIL'})")
    assert g1 < 1e-12, g1
    worst = 0.0
    for char in FOCUS:
        for i, book in enumerate(BOOKS):
            v = float(F[(F.ctrl == REC_CTRL) & (F.est == REC_EST) & (F.char == char) &
                        (F.book == book) & (F.k == CELL284[1]) &
                        (np.isclose(F.q, CELL284[0]))].value.iloc[0])
            e = abs(v - PUB_284[char][i])
            worst = max(worst, e)
            P(f"  G2 (q {CELL284[0]}, k {CELL284[1]}) {char:5s} {book:7s} re-fit {v:+.4f} | "
              f"idea 284 published {PUB_284[char][i]:+.3f} | |diff| {e:.5f}")
    P(f"  G2 max |diff| {worst:.3e} ({'PASS' if worst < 1e-3 else 'FAIL'})")
    assert worst < 1e-3, worst
    flush_log()

    # ---------------------------------------------------------- the record's surface
    P("\n" + "=" * 170)
    P(f"THE RECORD'S OWN ESTIMATOR ({REC_EST}/{REC_CTRL}): within-stratum partial by cell "
      f"(27 points per characteristic; the (q 0.50, k 40) row is idea 284's stratum)")
    base = F[(F.ctrl == REC_CTRL) & (F.est == REC_EST)]
    for char in CHARS:
        P(f"\n--- {char} " + "-" * 140)
        P(fmt(base[base.char == char].pivot_table(index=["k", "q"], columns="book", values="value")))
    flush_log()

    # ---------------------------------------------------------- B1 / B2 stability
    P("\n" + "=" * 170)
    P(f"B1/B2  SIGN AND SIZE STABILITY over the 27 (stratum x book) points, every "
      f"(control set, estimator).  Sign bar >= {SIGN_BAR}/27 holding the pooled sign; "
      f"size bar |mean|/SD >= {SIZE_BAR}.")
    st = []
    for ctrl in CONTROL_SETS:
        for est in ESTIMATORS:
            for char in CHARS:
                g = F[(F.ctrl == ctrl) & (F.est == est) & (F.char == char)]
                mu, sd = g.value.mean(), g.value.std()
                sgn = np.sign(mu)
                hold = int((np.sign(g.value) == sgn).sum())
                gx = g[~g.is284cell]
                st.append(dict(ctrl=ctrl, est=est, char=char, n_points=len(g), mean=mu, sd=sd,
                               lo=g.value.min(), hi=g.value.max(), pooled_sign=int(sgn),
                               n_hold_sign=hold, sign_stable=bool(hold >= SIGN_BAR),
                               mean_abs_over_sd=abs(mu) / sd if sd > 0 else np.nan,
                               size_stable=bool(sd > 0 and abs(mu) / sd >= SIZE_BAR),
                               mean_ex284=gx.value.mean(),
                               n_hold_ex284=int((np.sign(gx.value) == sgn).sum()),
                               mean_t=g.t.mean(), n_t_gt2=int((g.t.abs() > 2).sum())))
    S = pd.DataFrame(st)
    S.to_csv(f"{OUT}.stability.csv", index=False)
    P(fmt(S.set_index(["ctrl", "est", "char"])))
    P("\n  FOCUS comparison (disp vs evol), every (control set, estimator):")
    for ctrl in CONTROL_SETS:
        for est in ESTIMATORS:
            a = S[(S.ctrl == ctrl) & (S.est == est) & (S.char == "disp")].iloc[0]
            b = S[(S.ctrl == ctrl) & (S.est == est) & (S.char == "evol")].iloc[0]
            P(f"    {ctrl:7s}/{est:8s}  disp mean {a['mean']:+.4f} sd {a.sd:.4f} sign "
              f"{a.n_hold_sign:2d}/27 |mu|/sd {a.mean_abs_over_sd:.2f}   |   "
              f"evol mean {b['mean']:+.4f} sd {b.sd:.4f} sign {b.n_hold_sign:2d}/27 "
              f"|mu|/sd {b.mean_abs_over_sd:.2f}   -> more stable: "
              f"{'evol' if b.n_hold_sign > a.n_hold_sign else ('disp' if a.n_hold_sign > b.n_hold_sign else 'tie')}")
    flush_log()

    # ---------------------------------------------------------- B3 leave-one-stratum-out
    P("\n" + "=" * 170)
    P("B3  IS THE DISAGREEMENT ONE CELL?  leave-one-stratum-out means over the remaining "
      "24 points (record estimator and every other (control set, estimator))")
    lo = []
    for ctrl in CONTROL_SETS:
        for est in ESTIMATORS:
            g = F[(F.ctrl == ctrl) & (F.est == est)]
            for k in KS:
                for q in QS:
                    sub = g[~((g.k == k) & (np.isclose(g.q, q)))]
                    row = dict(ctrl=ctrl, est=est, dropped_k=k, dropped_q=q,
                               is284=bool((q, k) == CELL284))
                    for char in CHARS:
                        row[f"{char}_mean"] = sub[sub.char == char].value.mean()
                    row["evol_gt_disp"] = bool(row["evol_mean"] > row["disp_mean"])
                    lo.append(row)
    L = pd.DataFrame(lo)
    L.to_csv(f"{OUT}.loso.csv", index=False)
    P(fmt(L.set_index(["ctrl", "est", "dropped_k", "dropped_q"])))
    for ctrl in CONTROL_SETS:
        for est in ESTIMATORS:
            g = F[(F.ctrl == ctrl) & (F.est == est)]
            full_evol, full_disp = g[g.char == "evol"].value.mean(), g[g.char == "disp"].value.mean()
            sub = L[(L.ctrl == ctrl) & (L.est == est)]
            flips = sub[sub.evol_gt_disp != (full_evol > full_disp)]
            P(f"    {ctrl:7s}/{est:8s} full-grid ordering evol {full_evol:+.4f} vs disp "
              f"{full_disp:+.4f} -> {'evol' if full_evol > full_disp else 'disp'} larger; "
              f"strata whose removal FLIPS that ordering: "
              f"{[(int(r.dropped_k), float(r.dropped_q)) for _, r in flips.iterrows()] or 'none'}")
    # how extreme is the 284 cell?
    P("\n  the (q 0.500, k 40) cell against its own grid, record estimator:")
    g = base
    for char in FOCUS:
        gg = g[g.char == char]
        cell = gg[gg.is284cell].value
        rest = gg[~gg.is284cell].value
        z = (cell.mean() - rest.mean()) / rest.std() if rest.std() > 0 else np.nan
        P(f"    {char:5s}: cell mean {cell.mean():+.4f} vs other-24 mean {rest.mean():+.4f} "
          f"(sd {rest.std():.4f}) -> z {z:+.2f}; cell holds the grid sign in "
          f"{int((np.sign(cell) == np.sign(gg.value.mean())).sum())}/3 books")
    flush_log()

    # ---------------------------------------------------------- B4 seed split-half
    P("\n" + "=" * 170)
    P("B4  SEED SPLIT-HALF (seeds 0-29 vs 30-59), record estimator and all dial settings")
    sh = []
    for ctrl in CONTROL_SETS:
        for est in ESTIMATORS:
            for k in KS:
                for q in QS:
                    d = seeded[(seeded.k == k) & (np.isclose(seeded.q, q))]
                    d1, d2 = d[d.seed < N_SEEDS // 2], d[d.seed >= N_SEEDS // 2]
                    for book in BOOKS:
                        for char in FOCUS:
                            v1, _, _ = fit(char, ctrl, est, d1, book)
                            v2, _, _ = fit(char, ctrl, est, d2, book)
                            sh.append(dict(ctrl=ctrl, est=est, k=k, q=q, book=book, char=char,
                                           h1=v1, h2=v2,
                                           same_sign=bool(np.sign(v1) == np.sign(v2)),
                                           is284cell=bool((q, k) == CELL284)))
    H = pd.DataFrame(sh)
    H.to_csv(f"{OUT}.splithalf.csv", index=False)
    P(fmt(H[(H.ctrl == REC_CTRL) & (H.est == REC_EST)]
          .set_index(["char", "k", "q", "book"])[["h1", "h2", "same_sign"]]))
    for ctrl in CONTROL_SETS:
        for est in ESTIMATORS:
            for char in FOCUS:
                g = H[(H.ctrl == ctrl) & (H.est == est) & (H.char == char)]
                P(f"    {ctrl:7s}/{est:8s} {char:5s}: halves agree in sign "
                  f"{int(g.same_sign.sum())}/{len(g)}; mean h1 {g.h1.mean():+.4f}, "
                  f"h2 {g.h2.mean():+.4f}")
    flush_log()

    # ---------------------------------------------------------- B5 rule 8 (draw-wise OOS)
    P("\n" + "=" * 170)
    P("B5  RULE 8.  (a) TIME: characteristics IS-only (<= 2016), every book metric OOS (>= 2017). "
      "(b) DRAW: direction FIT on seeds 0-29, APPLIED to seeds 30-59, read ONCE.")
    wf = []
    for ctrl in CONTROL_SETS:
        for est in ESTIMATORS:
            for k in KS:
                for q in QS:
                    d = seeded[(seeded.k == k) & (np.isclose(seeded.q, q))]
                    d1, d2 = d[d.seed < N_SEEDS // 2], d[d.seed >= N_SEEDS // 2]
                    for book in BOOKS:
                        for char in FOCUS:
                            v1, _, _ = fit(char, ctrl, est, d1, book)
                            direction = 1 if v1 > 0 else -1          # fitted on the unseen-free half
                            idx = (d2[f"{char}_IS"].idxmax() if direction > 0
                                   else d2[f"{char}_IS"].idxmin())
                            r = seeded.loc[idx]
                            anchor = d2[f"{book}_OOS_Sharpe"].mean()
                            wf.append(dict(
                                ctrl=ctrl, est=est, k=k, q=q, book=book, char=char,
                                fit_h1=v1, direction=("HIGH" if direction > 0 else "LOW"),
                                panel=r.panel, seed=int(r.seed),
                                OOS_CAGR=r[f"{book}_OOS_CAGR"], OOS_Sharpe=r[f"{book}_OOS_Sharpe"],
                                OOS_MaxDD=r[f"{book}_OOS_MaxDD"],
                                anchor_OOS_Sharpe=anchor,
                                beats_anchor=bool(r[f"{book}_OOS_Sharpe"] > anchor),
                                spy_OOS_CAGR=r["SPY_OOS_CAGR"], spy_OOS_Sharpe=r["SPY_OOS_Sharpe"],
                                spy_OOS_MaxDD=r["SPY_OOS_MaxDD"],
                                v2_OOS_CAGR=r["v2_OOS_CAGR"], v2_OOS_Sharpe=r["v2_OOS_Sharpe"],
                                v2_OOS_MaxDD=r["v2_OOS_MaxDD"],
                                beats_spy=bool(r[f"{book}_OOS_Sharpe"] > r["SPY_OOS_Sharpe"]),
                                beats_v2=bool(r[f"{book}_OOS_Sharpe"] > r["v2_OOS_Sharpe"]),
                                CAGR=r[f"{book}_CAGR"], Sharpe=r[f"{book}_Sharpe"],
                                MaxDD=r[f"{book}_MaxDD"], H1=r[f"{book}_H1"], H2=r[f"{book}_H2"],
                                keep4a=keep4a(r, book), keep4b=all(bars4b(r, book).values()),
                                fail4b=fail4b(r, book)))
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    P("\n  record estimator (RANKPART/REC), all 18 selector-cells:")
    P(fmt(W[(W.ctrl == REC_CTRL) & (W.est == REC_EST)].set_index(["char", "k", "q", "book"])
          [["fit_h1", "direction", "seed", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
            "anchor_OOS_Sharpe", "beats_anchor", "beats_spy", "beats_v2", "keep4a", "keep4b",
            "fail4b"]]))
    P("\n  summary over all (control set, estimator) settings:")
    for ctrl in CONTROL_SETS:
        for est in ESTIMATORS:
            for char in FOCUS:
                g = W[(W.ctrl == ctrl) & (W.est == est) & (W.char == char)]
                P(f"    {ctrl:7s}/{est:8s} {char:5s}: beats anchor {int(g.beats_anchor.sum())}/{len(g)}, "
                  f"beats SPY {int(g.beats_spy.sum())}/{len(g)}, beats RULES v2 "
                  f"{int(g.beats_v2.sum())}/{len(g)}, mean OOS Sharpe {g.OOS_Sharpe.mean():.4f} "
                  f"(anchor {g.anchor_OOS_Sharpe.mean():.4f}), mean OOS CAGR {g.OOS_CAGR.mean():.4f}, "
                  f"mean OOS MaxDD {g.OOS_MaxDD.mean():.4f}, HIGH-direction picks "
                  f"{int((g.direction == 'HIGH').sum())}/{len(g)}")
    P(f"\n  SPY OOS Sharpe {W.spy_OOS_Sharpe.mean():.4f}, CAGR {W.spy_OOS_CAGR.mean():.4f}, "
      f"MaxDD {W.spy_OOS_MaxDD.mean():.4f}   |   RULES v2 OOS Sharpe {W.v2_OOS_Sharpe.mean():.4f}, "
      f"CAGR {W.v2_OOS_CAGR.mean():.4f}, MaxDD {W.v2_OOS_MaxDD.mean():.4f}")
    flush_log()

    # ---------------------------------------------------------- B6 keep paths
    P("\n" + "=" * 170)
    P("B6  KEEP PATHS on every selected panel-book")
    P(f"  4a {int(W.keep4a.sum())} / {len(W)}   4b {int(W.keep4b.sum())} / {len(W)}   "
      f"BOTH {int((W.keep4a & W.keep4b).sum())} / {len(W)}")
    P("  4b fail-bar frequency: " + ", ".join(f"{k}={v}" for k, v in W.fail4b.value_counts().items()))
    if W.keep4b.any():
        P("\n  every 4b passer:")
        P(fmt(W[W.keep4b].set_index(["ctrl", "est", "char", "k", "q", "book"])
              [["panel", "seed", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe",
                "OOS_MaxDD", "keep4a"]]))
    # the same books' whole-stratum 4b rate, as the base rate the selector must beat
    P("\n  base rate: 4b pass share over ALL 540 panels x 3 books (the pool the selector draws from):")
    tot = 0; pas = 0
    for book in BOOKS:
        n = len(seeded)
        p4 = sum(all(bars4b(r, book).values()) for _, r in seeded.iterrows())
        tot += n; pas += p4
        P(f"    {book:7s} {p4}/{n} = {p4 / n:.3f}")
    P(f"    ALL     {pas}/{tot} = {pas / tot:.3f}")
    flush_log()
    P("\nDone.")
    flush_log()


if __name__ == "__main__":
    main()

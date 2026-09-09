#!/usr/bin/env python3
"""Idea 484 - "does-one-dispersion-number-really-out-predict-136-name-dummies" (lane C, 2026-09-09).

The question
------------
Idea 252's leg (3) reported, on B136 with idea 78's 50 draws per k cell:

    the name-level model ALONE predicts out of fold at R2 -0.197..+0.424 (median +0.151);
    sd ALONE at R2 +0.026..+0.375 (median +0.289)
    -> "a single dispersion number out-predicts the whole 136-name additive model on this panel"

That ordering is exactly what a small-N comparison produces whether or not it is true of the
population: a 136-parameter ridge fitted on 45 training rows is mostly shrinkage, while a
2-parameter line on the same 45 rows is nearly its asymptote.  The queue asks whether the
ordering is a SMALL-N ARTEFACT, and where the crossover is.

So this run re-runs idea 252's nested out-of-fold comparison

    y ~ sd  (2 params)      vs      y ~ M  (P name dummies, ridge)      vs      y ~ M + sd

on a DRAW LADDER D in {50, 100, 150, 200, 300, 400, 500} draws per k cell and on TWO panels
(B136, P=136 names; SMALL484, P=484 names), and reports, for every cell, the smallest D at
which the name-additive model catches sd - or that it never does inside the ladder, with the
fitted learning curve saying where it would.

Pre-registered reading (written before any new number was read)
    ARTEFACT      if oofR2(M) >= oofR2(sd) at some D on the ladder in a majority of the
                  book-Sharpe cells of a panel: idea 252's sentence is then a statement about
                  N=50, not about the panel, and must be restated with its N.
    REAL          if M never catches sd anywhere on the ladder at 10x the draws AND the gap
                  is not shrinking with D (fitted slope of (oofR2_sd - oofR2_M) on log D
                  >= 0): one dispersion number genuinely out-predicts the name dummies.
    QUALIFIED     anything between - in particular a gap that closes monotonically but does
                  not cross by D=500 - reported with the extrapolated crossing D*.

Tuned parameters (PROTOCOL rule 4: at most two) - the queue's own two
    1. draws  D per k cell in {50, 100, 150, 200, 300, 400, 500}, NESTED (the first 50 draws
              of every panel/k are the same 50 at every D, and on B136 are idea 78's own).
    2. panel  in {B136, SMALL484}.
    ALL 2 x 7 x 3(k) x 2(n) x 3(y) x 6(lambda) grid points are written to .nested.csv and the
    book-Sharpe ones are printed.  The ridge penalty lambda is NOT a third tuned parameter: the
    headline curve picks it by inner cross-validation INSIDE each training fold (nested CV, so
    the held-out fold never touches the choice), and the whole ladder is reported beside it
    together with the oracle (best-lambda-per-cell) curve, which is the most generous reading
    the name-additive model can be given.
    Everything else is idea 78/83/252's and is imported unchanged: k in {20,40,80}, n in {5,20},
    the gate, gross 0.75, weekly cadence, 10 bps, the 2009-2016 / 2017-2026 split, the seeds
    (SEED_B + k, so draw d is the same name set at every D), 10 folds by draw index.

Reproduction gate (run BEFORE any new number is read)
    [a] harness: U56/CAND20 and U56/RULES v1 from engine.backtest.
    [b] FAST BACKTEST: the vectorised backtester used for 3,000 books is checked against
        engine.backtest on 6 drawn books (max abs difference on the evaluation window).
    [c] GRID: the first 50 draws of each B136 k cell are re-run and checked column by column
        against idea 78's committed gridB.csv - the file idea 83 and idea 252 both gated on.
        If this run's book pipeline is idea 78's, these 300 rows reproduce exactly.
    [d] IDEA 252's OWN NUMBER: leg (3) is recomputed at D=50 on B136 and checked against the
        published medians (M +0.151, sd-only +0.289) and the published 72/72 nested gain.

Walk-forward (PROTOCOL rule 8), selectors fixed before any OOS number was read
    All selector inputs use 2009-2016 ONLY (IS Sharpe of each drawn book); 2017-2026 is read
    once, at the end, for the arms below.  The rule-8 question is the queue's question in its
    decision form: if you had to CHOOSE a sub-panel, does the name-additive model's prediction
    of a draw's Sharpe transfer better than one dispersion number's?
    S0  do-nothing: the whole panel, CAND-n (no draw chosen at all).
    S1  IS-Sharpe argmax                                    (idea 83/252's incumbent)
    S2  max IS sd                                           (idea 83/252's dispersion arm)
    S3  argmax of the out-of-fold prediction of IS Sharpe from sd alone
    S4  argmax of the out-of-fold prediction of IS Sharpe from M (ridge, CV lambda)
    S5  argmax of the out-of-fold prediction of IS Sharpe from M + sd
    S6  random draw (fixed seed)
    Each arm is read at every D on the ladder and on both panels; OOS CAGR/Sharpe/MaxDD are
    reported against SPY and against the live book (RULES v2) on the same window.

KEEP paths (PROTOCOL rule 4).  This run introduces no new BOOK FORM - the object under test is
a statistic about drawn sub-panels - but it does run 3,000 fresh books, so 4a (vs the LIVE
RULES v2 book, and vs v1 for continuity with idea 78) and 4b (vs SPY, incl. the OOS leg) are
evaluated for every one of them and for every rule-8 arm.

Survivorship (rule 9): universe_broad.json and the sub-$2B panel are CURRENT CONSTITUENTS.
Here that cuts against the name-additive model, not for it: name dummies are fitted on names
already known to have survived, which is the most favourable possible sample for a fixed-effect
design.  A name-additive model that still loses to one dispersion number loses on easy ground.

Deterministic (fixed seeds, folds by draw index), standalone.  Reads baseline.py and engine.py;
modifies nothing.  Run: python3 research/backtests/2026-09-09_does-one-...-dummies_C.py
"""
import sys, time, json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import warnings
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore", category=RuntimeWarning)
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score
from engine import backtest, metrics, rebalance_mask

# ---- idea 78/83/252's constants, imported verbatim -------------------------------
COST_BPS = 10
FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
KS = [20, 40, 80]
N_BOOKS = [5, 20]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SEED_B = 78_500
SEED_S6 = 78_999
N_FOLDS = 10
LAMS = [0.5, 2.0, 8.0, 32.0, 128.0, 512.0]

# ---- this run's two tuned parameters ---------------------------------------------
DRAWS = [50, 100, 150, 200, 300, 400, 500]
D_MAX = max(DRAWS)
PANELS = ["B136", "SMALL484"]

SCRIPT = Path(__file__).name
OUT = REPO / "research" / "backtests"
STEM = SCRIPT[:-3]
REF_GRIDB = OUT / "2026-09-05_candidate-count-vs-dispersion_B.gridB.csv"

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 2000)

_lines = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _lines.append(s)


# ---------------------------------------------------------------- book helpers (idea 78's)
def fast_backtest(prices, weights, cost_bps=COST_BPS, freq=FREQ):
    """Vectorised equivalent of engine.backtest's return series (gated at [b])."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy(); m[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(m)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]; W0 = wt[s0]
    h = W0 * (Cp / Cp[s0]); V = h.sum(axis=1) + (1.0 - W0.sum(axis=1)); held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]; W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p]); Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1)); heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return pd.Series((held * rets).sum(axis=1) - turn * cost_bps / 1e4, index=idx)


def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ---------------------------------------------------------------- regression helpers (idea 252's)
def ols(y, X, names):
    y = np.asarray(y, float)
    X = np.column_stack([np.ones(len(y))] + [np.asarray(c, float) for c in X])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    dof = len(y) - X.shape[1]
    s2 = float(resid @ resid) / dof
    se = np.sqrt(np.diag(np.linalg.pinv(X.T @ X)) * s2)
    ss = float(((y - y.mean()) ** 2).sum())
    return dict(R2=1.0 - float(resid @ resid) / ss if ss > 0 else np.nan,
                coef=dict(zip(["const"] + names, beta)), t=dict(zip(["const"] + names, beta / se)))


def oof_r2(y, pred):
    y = np.asarray(y, float)
    ss = float(((y - y.mean()) ** 2).sum())
    return 1.0 - float(((y - pred) ** 2).sum()) / ss if ss > 0 else np.nan


def _solve_multi(A, Xc, Y, ym, lam, free):
    """Ridge betas for MANY y columns at once: one Gram, one solve with an n_y-column RHS.

    Identical estimator to idea 252's `ridge_fit` (unpenalised intercept via centring, `free`
    leading unpenalised columns), just solved for several targets in one call.
    """
    d = np.full(A.shape[0], float(lam))
    if free: d[:free] = 0.0
    return np.linalg.solve(A + np.diag(d), Xc.T @ (Y - ym))


def oof_paths(M, Y, folds, lams, free=0, inner_k=5):
    """For an (T x n_y) block of targets sharing the same design M and folds, return

        preds[lam] : (T x n_y) out-of-fold predictions at that penalty
        cv_pred    : (T x n_y) out-of-fold predictions with lambda chosen by a NESTED inner
                     `inner_k`-fold CV inside each training fold (held-out rows never seen)
        picks      : list of chosen lambdas per (fold, y)

    Grams and solves are shared across the y columns, which is exactly why this is one
    function rather than a loop: the design is identical for every target.
    """
    T = len(folds); nY = Y.shape[1]
    preds = {lam: np.empty((T, nY)) for lam in lams}
    cv_pred = np.empty((T, nY)); picks = []
    for f in np.unique(folds):
        te = folds == f; tr = np.flatnonzero(~te)
        Xtr = M[tr]; xm = Xtr.mean(axis=0); Xc = Xtr - xm; A = Xc.T @ Xc
        Xte = M[te] - xm
        Ytr = Y[tr]; ym = Ytr.mean(axis=0)
        for lam in lams:
            beta = _solve_multi(A, Xc, Ytr, ym, lam, free)
            preds[lam][te] = ym + Xte @ beta
        # nested inner CV for the penalty
        inner = np.arange(len(tr)) % inner_k
        inner_pred = {lam: np.empty((len(tr), nY)) for lam in lams}
        for g in range(inner_k):
            ite = inner == g; itr = ~ite
            Xi = M[tr[itr]]; xmi = Xi.mean(axis=0); Xci = Xi - xmi; Ai = Xci.T @ Xci
            Xie = M[tr[ite]] - xmi
            Yi = Y[tr[itr]]; ymi = Yi.mean(axis=0)
            for lam in lams:
                beta = _solve_multi(Ai, Xci, Yi, ymi, lam, free)
                inner_pred[lam][ite] = ymi + Xie @ beta
        best = np.full(nY, -np.inf); bl = [lams[0]] * nY
        for lam in lams:
            for j in range(nY):
                s = oof_r2(Y[tr, j], inner_pred[lam][:, j])
                if s > best[j]:
                    best[j] = s; bl[j] = lam
        for j in range(nY):
            beta = _solve_multi(A, Xc, Ytr[:, [j]], ym[[j]], bl[j], free)
            cv_pred[te, j] = (ym[j] + Xte @ beta).ravel()
        picks.append(list(bl))
    return preds, cv_pred, picks


def oof_line(y, x, folds):
    """sd ALONE, out of fold - idea 252's floor, verbatim."""
    F = np.empty(len(y))
    for f in np.unique(folds):
        te = folds == f; tr = ~te
        o = ols(y[tr], [x[tr]], ["sd"])
        F[te] = o["coef"]["const"] + o["coef"]["sd"] * x[te]
    return F


# ================================================================== the book grid
def panel_defs():
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    return {
        "B136": (px136, [c for c in px136.columns]),                       # idea 78: SPY tradable
        "SMALL484": (pxs, [c for c in pxs.columns if c != "SPY"]),         # idea 78: SPY benchmark only
    }


def draw_books(px, names, k, d_lo, d_hi, seed, startb, store=None):
    """Books for draws [d_lo, d_hi) of one k cell.  Draw d is the d-th name set from the
    generator seeded once per (panel, k), so the ladder is nested by construction."""
    rng = np.random.default_rng(seed)
    rows = []
    for d in range(d_hi):
        cols = list(rng.choice(names, size=k, replace=False))
        if d < d_lo:
            continue
        keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px.columns else [])))
        p = px[keep].dropna(how="all").ffill()
        s, above, vol20 = score(p, vol_scale=False)          # `above`/`vol20` do not depend on vol_scale
        elig = (above & (vol20 < MAX_VOL)).copy()
        drop = [c for c in p.columns if c not in set(cols)]
        if drop: elig[drop] = False
        rank = s.where(elig).rank(axis=1, ascending=False)
        wm = rebalance_mask(p.index, FREQ).values
        ne = elig[wm].sum(axis=1).loc[startb:]
        mom_p = (p[cols].shift(21) / p[cols].shift(252) - 1).where(elig[cols])
        sdw = mom_p[wm].loc[startb:].std(axis=1)
        cnt = elig.sum(axis=1).replace(0, np.nan)
        w_ew = elig.astype(float).div(cnt, axis=0).mul(GROSS).fillna(0.0)
        r_e = fast_backtest(p, w_ew).loc[startb:]
        me = metrics(r_e)
        rec = dict(k=k, draw=d, cols=cols,
                   n_elig=float(ne.mean()), sd=float(sdw.mean()),
                   n_elig_IS=float(ne.loc[:IS_END].mean()), sd_IS=float(sdw.loc[:IS_END].mean()),
                   ew_Sharpe=me["Sharpe"], ew_CAGR=me["CAGR"], ew_MaxDD=me["MaxDD"])
        for nb in N_BOOKS:
            w_c = (rank <= nb).astype(float) * (GROSS / nb)
            r_c = fast_backtest(p, w_c).loc[startb:]
            mc = metrics(r_c); h1, h2 = half_sharpes(r_c)
            oo = r_c.loc[OOS_START:]; mo = metrics(oo)
            rec.update({f"CAGR{nb}": mc["CAGR"], f"Sharpe{nb}": mc["Sharpe"], f"MaxDD{nb}": mc["MaxDD"],
                        f"H1_{nb}": h1, f"H2_{nb}": h2,
                        f"Sharpe_IS{nb}": metrics(r_c.loc[:IS_END])["Sharpe"],
                        f"Sharpe_OOS{nb}": mo["Sharpe"], f"CAGR_OOS{nb}": mo["CAGR"],
                        f"MaxDD_OOS{nb}": mo["MaxDD"], f"premium{nb}": mc["Sharpe"] - me["Sharpe"]})
            if store is not None:
                store[(k, d, nb)] = r_c
        rows.append(rec)
    return rows


# ================================================================== main
def main():
    t0 = time.time()
    P("=" * 200)
    P("IDEA 484 - does-one-dispersion-number-really-out-predict-136-name-dummies (lane C, 2026-09-09)")
    P("Idea 252 leg (3): on B136 at 50 draws per k cell, sd ALONE predicts a draw's Sharpe out of fold at")
    P("median R2 +0.289 while the 136-name additive ridge manages +0.151.  Is that a SMALL-N artefact?")
    P("Draw ladder D in", DRAWS, "per k cell x panels", PANELS, "- where is the crossover?")
    P("=" * 200)

    # ---------------------------------------------------------------- [a] harness
    P("\n[a] HARNESS - published rows recomputed from engine.backtest before anything new is read")
    px56 = load_universe()
    s56 = px56.index[260]
    _, above56, vol56 = score(px56, vol_scale=False)
    e56 = (above56 & (vol56 < MAX_VOL))
    s56v = score(px56, vol_scale=False)[0]
    w56 = (s56v.where(e56).rank(axis=1, ascending=False) <= 20).astype(float) * (GROSS / 20)
    r_u56 = backtest(px56, w56, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[s56:]
    m = metrics(r_u56); h1, h2 = half_sharpes(r_u56)
    P(f"    U56/CAND20   {m['CAGR']:.4%} / {m['Sharpe']:.5f} / {m['MaxDD']:.4%}  halves {h1:.5f}/{h2:.5f}"
      f"   (ideas 2/73/77/83/252 published 12.7% / 1.092-1.093 / -18.3%)")
    r_v1 = backtest(px56, rules_v1_weights(px56), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[s56:]
    m = metrics(r_v1)
    P(f"    U56/RULES v1 {m['CAGR']:.4%} / {m['Sharpe']:.5f} / {m['MaxDD']:.4%}   (published 6.5% / 0.664-0.666 / -13.8%)")

    panels = panel_defs()
    ctx = {}
    for pan, (px, names) in panels.items():
        startb = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[startb:]
        base1 = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[startb:]
        base2 = backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[startb:]
        ctx[pan] = dict(px=px, names=names, startb=startb, spy=spy, spy_oos=spy.loc[OOS_START:],
                        v1=base1, v2=base2)
        ms = metrics(spy); sh1, sh2 = half_sharpes(spy)
        P(f"\n    {pan}: {len(names)} tradable names, window {startb.date()} -> {px.index[-1].date()} "
          f"({len(spy)} days)")
        P(f"      SPY      {ms['CAGR']:.2%} / {ms['Sharpe']:.3f} / {ms['MaxDD']:.2%}  halves {sh1:.3f}/{sh2:.3f}"
          f"  OOS {metrics(spy.loc[OOS_START:])['Sharpe']:.3f}")
        for lab, b in (("RULES v1", base1), ("RULES v2 (live)", base2)):
            mb = metrics(b); b1, b2 = half_sharpes(b)
            P(f"      {lab:<15} {mb['CAGR']:.2%} / {mb['Sharpe']:.3f} / {mb['MaxDD']:.2%}  halves {b1:.3f}/{b2:.3f}"
              f"  OOS {metrics(b.loc[OOS_START:])['Sharpe']:.3f}")
        P(f"      4b bars: MaxDD <= {0.60 * abs(ms['MaxDD']):.2%}, CAGR >= {0.70 * ms['CAGR']:.2%}, "
          f"H1 > {sh1:.3f}, H2 > {sh2:.3f}, OOS Sharpe > {metrics(spy.loc[OOS_START:])['Sharpe']:.3f}")

    # ---------------------------------------------------------------- [b] fast backtest gate
    P("\n[b] FAST BACKTEST GATE - the vectorised backtester vs engine.backtest on 6 drawn books")
    px136, names136 = panels["B136"]; startb136 = ctx["B136"]["startb"]
    gate_max = 0.0
    rng = np.random.default_rng(SEED_B + 40)
    for i in range(6):
        cols = list(rng.choice(names136, size=40, replace=False))
        keep = list(dict.fromkeys(cols + ["SPY"]))
        p = px136[keep].dropna(how="all").ffill()
        s, above, vol20 = score(p, vol_scale=False)
        elig = (above & (vol20 < MAX_VOL)).copy()
        drop = [c for c in p.columns if c not in set(cols)]
        if drop: elig[drop] = False
        w = (s.where(elig).rank(axis=1, ascending=False) <= 20).astype(float) * (GROSS / 20)
        a = backtest(p, w, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[startb136:]
        b = fast_backtest(p, w).loc[startb136:]
        gate_max = max(gate_max, float(np.abs(a.values - b.values).max()))
    P(f"    max abs difference on the evaluation window over 6 books: {gate_max:.3e}")
    ok_b = gate_max < 1e-12
    P(f"    FAST BACKTEST {'PASS' if ok_b else 'FAIL'}")

    # ---------------------------------------------------------------- the grid
    P("\n" + "=" * 200)
    P(f"BOOK GRID - {D_MAX} draws per k cell x 3 k x 2 panels = {D_MAX * 3 * 2} sub-panels, "
      f"CAND-5, CAND-20 and EWall on each, {COST_BPS} bps, weekly, next-day execution")
    P("=" * 200)
    G = {}
    for pan in PANELS:
        c = ctx[pan]
        rows = []
        for k in KS:
            rows += draw_books(c["px"], c["names"], k, 0, D_MAX, SEED_B + k, c["startb"])
            P(f"    {pan} k={k:<3} {D_MAX} draws done ({time.time() - t0:.0f}s)")
        B = pd.DataFrame(rows)
        # KEEP paths for every book (needs the return series; recomputed cheaply from stored metrics)
        G[pan] = B
    P(f"    grid built in {time.time() - t0:.0f}s")

    # ---------------------------------------------------------------- [c] reproduction vs idea 78
    P("\n[c] GRID GATE - the first 50 draws of each B136 k cell vs idea 78's committed gridB.csv")
    ok_c = True
    if REF_GRIDB.exists():
        ref = pd.read_csv(REF_GRIDB)
        B = G["B136"]
        mine = []
        for nb in N_BOOKS:
            sub = B[B.draw < 50]
            mine.append(pd.DataFrame(dict(
                k=sub.k, n=nb, draw=sub.draw, n_elig=sub.n_elig, sd=sub.sd,
                n_elig_IS=sub.n_elig_IS, sd_IS=sub.sd_IS,
                CAGR=sub[f"CAGR{nb}"], Sharpe=sub[f"Sharpe{nb}"], MaxDD=sub[f"MaxDD{nb}"],
                H1=sub[f"H1_{nb}"], H2=sub[f"H2_{nb}"], Sharpe_IS=sub[f"Sharpe_IS{nb}"],
                Sharpe_OOS=sub[f"Sharpe_OOS{nb}"], CAGR_OOS=sub[f"CAGR_OOS{nb}"],
                MaxDD_OOS=sub[f"MaxDD_OOS{nb}"], ew_Sharpe=sub.ew_Sharpe, ew_CAGR=sub.ew_CAGR,
                ew_MaxDD=sub.ew_MaxDD, premium=sub[f"premium{nb}"])))
        MN = pd.concat(mine)
        j = MN.merge(ref, on=["k", "n", "draw"], suffixes=("", "_ref"))
        cols = ["n_elig", "sd", "n_elig_IS", "sd_IS", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                "Sharpe_IS", "Sharpe_OOS", "CAGR_OOS", "MaxDD_OOS", "ew_Sharpe", "ew_CAGR",
                "ew_MaxDD", "premium"]
        diffs = {c_: float((j[c_] - j[c_ + "_ref"]).abs().max()) for c_ in cols}
        dmax = max(diffs.values())
        P(f"    {len(j)} rows x {len(cols)} numeric columns; max abs difference by column:")
        for c_, v in diffs.items():
            P(f"      {c_:<12} {v:.3e}")
        ok_c = dmax < 1e-9 and len(j) == 300
        P(f"    GRID {'PASS - this run reproduces idea 78/83/252s own 300 books exactly' if ok_c else 'FAIL'}")
    else:
        P("    gridB.csv absent - gate [c] SKIPPED"); ok_c = False
    if not (ok_b and ok_c):
        P("\n    ABORT: the object under test is not the published one.");
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        return

    # ---------------------------------------------------------------- membership matrices
    P("\n" + "=" * 200)
    P("MEMBERSHIP MATRICES")
    P("=" * 200)
    MM = {}
    for pan in PANELS:
        names = ctx[pan]["names"]; idxn = {c: i for i, c in enumerate(names)}
        B = G[pan]
        M = np.zeros((len(B), len(names)))
        for i, cols in enumerate(B["cols"].values):
            for c in cols:
                M[i, idxn[c]] = 1.0
        MM[pan] = M
        P(f"    {pan}: P={len(names)} name columns, {len(B)} rows ({D_MAX} draws x {len(KS)} k cells)")
        for k in KS:
            sel = (B.k == k).values
            cnt = M[sel].sum(axis=0)
            P(f"      k={k:<3} N={int(sel.sum())}  name appearance count min/median/max "
              f"{int(cnt.min())}/{int(np.median(cnt))}/{int(cnt.max())}  never drawn: {int((cnt == 0).sum())}"
              f"   N/P at D=50 {50 / len(names):.2f}, at D={D_MAX} {D_MAX / len(names):.2f}")

    # ---------------------------------------------------------------- THE LADDER
    P("\n" + "=" * 200)
    P("THE DRAW LADDER - out-of-fold R2 of  y ~ sd  vs  y ~ M (ridge)  vs  y ~ M + sd,")
    P("10 folds by draw index, at every D on the ladder, every panel, k, book size and y-column.")
    P("lambda: CV = nested inner 5-fold choice inside each training fold; ORACLE = best of the six")
    P("penalties for that cell (the most generous reading the name-additive model can get).")
    P("=" * 200)
    # the six targets that share one design: (book size) x (CAND Sharpe, EWall Sharpe, premium).
    # EWall Sharpe does not depend on the book size and is carried under both, exactly as idea
    # 252 carried it, so the two runs' cell counts line up.
    TARGETS = [(nb, kind) for nb in N_BOOKS for kind in ("CAND Sharpe", "EWall Sharpe", "premium")]

    def target_col(nb, kind):
        return {"CAND Sharpe": f"Sharpe{nb}", "EWall Sharpe": "ew_Sharpe", "premium": f"premium{nb}"}[kind]

    lad = []
    for pan in PANELS:
        B = G[pan]; M_all = MM[pan]
        for k in KS:
            sel = np.flatnonzero((B.k == k).values)
            order = np.argsort(B.iloc[sel]["draw"].values)
            Bk = B.iloc[sel].iloc[order]
            Mk_all = M_all[sel][order]
            for D in DRAWS:
                rows = Bk.draw.values < D
                Mk = Mk_all[rows]; sub = Bk[rows]
                sdv = sub["sd"].values
                folds = np.arange(len(sub)) % N_FOLDS
                Msd = np.column_stack([sdv / sdv.std(), Mk])
                Y = np.column_stack([sub[target_col(nb, kind)].values for nb, kind in TARGETS])
                pM, cvM, pickM = oof_paths(Mk, Y, folds, LAMS)
                pMs, cvMs, _ = oof_paths(Msd, Y, folds, LAMS, free=1)
                for j, (nb, kind) in enumerate(TARGETS):
                    y = Y[:, j]
                    r_sd = oof_r2(y, oof_line(y, sdv, folds))
                    per_lam = {lam: (oof_r2(y, pM[lam][:, j]), oof_r2(y, pMs[lam][:, j])) for lam in LAMS}
                    r_M_cv, r_Msd_cv = oof_r2(y, cvM[:, j]), oof_r2(y, cvMs[:, j])
                    r_M_or = max(v[0] for v in per_lam.values())
                    r_Msd_or = max(v[1] for v in per_lam.values())
                    lad.append(dict(panel=pan, P=Mk.shape[1], n=nb, k=k, D=D, N=len(sub), y=kind,
                                    NP=len(sub) / Mk.shape[1],
                                    oofR2_sd=r_sd, oofR2_M_cv=r_M_cv, oofR2_Msd_cv=r_Msd_cv,
                                    oofR2_M_oracle=r_M_or, oofR2_Msd_oracle=r_Msd_or,
                                    gap_cv=r_sd - r_M_cv, gap_oracle=r_sd - r_M_or,
                                    gain_cv=r_Msd_cv - r_M_cv,
                                    lam_mode=float(pd.Series([p[j] for p in pickM]).mode().iloc[0]),
                                    **{f"oofR2_M_lam{lam:g}": per_lam[lam][0] for lam in LAMS},
                                    **{f"oofR2_Msd_lam{lam:g}": per_lam[lam][1] for lam in LAMS}))
            P(f"    {pan} k={k} ladder done ({time.time() - t0:.0f}s)")
    L = pd.DataFrame(lad)
    L.to_csv(OUT / f"{STEM}.nested.csv", index=False)

    # ---------------------------------------------------------------- [d] idea 252's own number
    P("\n[d] IDEA 252's PUBLISHED NUMBER, recomputed here at D=50 on B136 (its leg 3)")
    d50 = L[(L.panel == "B136") & (L.D == 50) & (L.y != "premium")]
    P(f"    book-Sharpe cells at D=50, all 6 penalties ({len(d50) * len(LAMS)} points):")
    flatM = d50[[f"oofR2_M_lam{lam:g}" for lam in LAMS]].values.ravel()
    flatMsd = d50[[f"oofR2_Msd_lam{lam:g}" for lam in LAMS]].values.ravel()
    flatsd = np.repeat(d50["oofR2_sd"].values, len(LAMS))
    P(f"      name-additive M ALONE : median {np.median(flatM):+.4f}  range {flatM.min():+.4f}..{flatM.max():+.4f}"
      f"   (idea 252 published median +0.151, range -0.197..+0.424)")
    P(f"      sd ALONE              : median {np.median(flatsd):+.4f}  range {flatsd.min():+.4f}..{flatsd.max():+.4f}"
      f"   (idea 252 published median +0.289, range +0.026..+0.375)")
    P(f"      nested gain M+sd - M  : improves in {int((flatMsd > flatM).sum())} of {len(flatM)} points"
      f"   (idea 252 published 72 of 72)")
    P(f"      sd beats M in {int((flatsd > flatM).sum())} of {len(flatM)} of those points")

    # ---------------------------------------------------------------- crossover
    P("\n" + "=" * 200)
    P("WHERE IS THE CROSSOVER?  smallest D on the ladder with oofR2(M) >= oofR2(sd), per cell.")
    P("=" * 200)
    cross = []
    for (pan, nb, k, ylab), g in L.groupby(["panel", "n", "k", "y"]):
        g = g.sort_values("D")
        for tag, col in (("cv", "oofR2_M_cv"), ("oracle", "oofR2_M_oracle")):
            hit = g[g[col] >= g["oofR2_sd"]]
            dstar = int(hit.D.iloc[0]) if len(hit) else np.nan
            # learning-curve slope of the gap on log D
            x = np.log(g.D.values); yv = (g["oofR2_sd"] - g[col]).values
            sl = np.polyfit(x, yv, 1)[0] if np.isfinite(yv).all() else np.nan
            b0 = np.polyfit(x, yv, 1)[1] if np.isfinite(yv).all() else np.nan
            dext = float(np.exp(-b0 / sl)) if (np.isfinite(sl) and sl < 0) else np.nan
            cross.append(dict(panel=pan, n=nb, k=k, y=ylab, lam=tag,
                              gap_D50=float(g[g.D == 50]["oofR2_sd"].iloc[0] - g[g.D == 50][col].iloc[0]),
                              gap_D500=float(g[g.D == D_MAX]["oofR2_sd"].iloc[0] - g[g.D == D_MAX][col].iloc[0]),
                              slope_logD=sl, D_cross=dstar, D_extrap=dext))
    C = pd.DataFrame(cross)
    C.to_csv(OUT / f"{STEM}.crossover.csv", index=False)
    bk = C[C.y != "premium"]
    P(fmt(C.set_index(["panel", "n", "k", "y", "lam"]), 4))
    for pan in PANELS:
        for tag in ("cv", "oracle"):
            s = bk[(bk.panel == pan) & (bk.lam == tag)]
            P(f"\n  {pan} / lambda {tag}: M catches sd inside the ladder in {int(s.D_cross.notna().sum())} of "
              f"{len(s)} book-Sharpe cells"
              f"   (median D* {s.D_cross.median() if s.D_cross.notna().any() else float('nan')})")
            P(f"      gap at D=50 median {s.gap_D50.median():+.4f}  ->  at D={D_MAX} median {s.gap_D500.median():+.4f}"
              f"   ; slope of the gap on log D: median {s.slope_logD.median():+.4f}, "
              f"negative (gap closing) in {int((s.slope_logD < 0).sum())} of {len(s)}")
            ex = s[s.D_cross.isna() & s.D_extrap.notna()]
            if len(ex):
                P(f"      cells that do not cross by D={D_MAX}: extrapolated crossing D* median "
                  f"{ex.D_extrap.median():,.0f} (range {ex.D_extrap.min():,.0f}..{ex.D_extrap.max():,.0f}) "
                  f"- EXTRAPOLATION, not measured")

    P("\n  FULL LADDER, book-Sharpe columns (CV lambda):")
    P(fmt(L[L.y != "premium"].set_index(["panel", "n", "k", "y", "D"])[
        ["N", "P", "NP", "oofR2_sd", "oofR2_M_cv", "oofR2_M_oracle", "oofR2_Msd_cv", "gap_cv",
         "gap_oracle", "gain_cv", "lam_mode"]]))
    P("\n  FULL LADDER, premium column:")
    P(fmt(L[L.y == "premium"].set_index(["panel", "n", "k", "D"])[
        ["N", "oofR2_sd", "oofR2_M_cv", "oofR2_M_oracle", "gap_cv", "gap_oracle"]]))
    P("\n  EVERY PENALTY at D=50 and D=%d (book-Sharpe columns):" % D_MAX)
    P(fmt(L[(L.y != "premium") & (L.D.isin([50, D_MAX]))].set_index(["panel", "n", "k", "y", "D"])[
        ["oofR2_sd"] + [f"oofR2_M_lam{lam:g}" for lam in LAMS]]))

    # ---------------------------------------------------------------- KEEP paths
    P("\n" + "=" * 200)
    P("BOTH KEEP PATHS - every one of the 3,000 drawn books")
    P("=" * 200)
    P("  4a: Sharpe > the comparand book in BOTH halves AND MaxDD no worse.")
    P("  4b: Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's.")
    keeprows = []
    for pan in PANELS:
        c = ctx[pan]; B = G[pan]
        # the grid already carries halves/DD/CAGR/OOS for every book, so the two bars are read
        # off those columns against the panel's comparands (idea 78's fail_4a / fail_4b, vectorised)
        v1h1, v1h2 = half_sharpes(c["v1"]); v1dd = metrics(c["v1"])["MaxDD"]
        v2h1, v2h2 = half_sharpes(c["v2"]); v2dd = metrics(c["v2"])["MaxDD"]
        sh1, sh2 = half_sharpes(c["spy"]); msp = metrics(c["spy"])
        oos_spy = metrics(c["spy_oos"])["Sharpe"]
        for nb in N_BOOKS:
            H1 = B[f"H1_{nb}"].values; H2 = B[f"H2_{nb}"].values
            DD = B[f"MaxDD{nb}"].values; CG = B[f"CAGR{nb}"].values
            OS = B[f"Sharpe_OOS{nb}"].values
            p4a1 = (H1 > v1h1) & (H2 > v1h2) & (DD >= v1dd)
            p4a2 = (H1 > v2h1) & (H2 > v2h2) & (DD >= v2dd)
            p4b = (H1 > sh1) & (H2 > sh2) & (OS > oos_spy) & (np.abs(DD) <= 0.60 * abs(msp["MaxDD"])) \
                  & (CG >= 0.70 * msp["CAGR"])
            keeprows.append(dict(panel=pan, book=f"CAND{nb}", N=len(B),
                                 pass4a_v1=int(p4a1.sum()), pass4a_v2=int(p4a2.sum()), pass4b=int(p4b.sum())))
        # EWall halves are not in idea 78's grid schema; not restated here (see note below).
        keeprows.append(dict(panel=pan, book="EWall", N=len(B), pass4a_v1=-1, pass4a_v2=-1, pass4b=-1))
    K = pd.DataFrame(keeprows)
    P(fmt(K.set_index(["panel", "book"]), 0))
    P("  (EWall halves are not stored by idea 78's grid schema and are not restated here: -1 = not measured.)")
    P("  4a is shown against BOTH the superseded RULES v1 (idea 78's comparand) and the LIVE RULES v2.")

    # ---------------------------------------------------------------- rule 8
    P("\n" + "=" * 200)
    P("RULE 8 WALK-FORWARD - selectors fitted on 2009-2016 only; 2017-2026 read once")
    P("=" * 200)
    wf = []
    for pan in PANELS:
        c = ctx[pan]; B = G[pan]; M_all = MM[pan]
        spy_oos = c["spy_oos"]; mspy_o = metrics(spy_oos)
        v2_oos = c["v2"].loc[OOS_START:]; mv2_o = metrics(v2_oos)
        for nb in N_BOOKS:
            # S0 do-nothing: the whole panel, CAND-nb
            px = c["px"]
            s, above, vol20 = score(px, vol_scale=False)
            elig = (above & (vol20 < MAX_VOL)).copy()
            drop = [x for x in px.columns if x not in set(c["names"])]
            if drop: elig[drop] = False
            w0 = (s.where(elig).rank(axis=1, ascending=False) <= nb).astype(float) * (GROSS / nb)
            r0 = fast_backtest(px, w0).loc[c["startb"]:]
            m0 = metrics(r0.loc[OOS_START:])
            for D in DRAWS:
                keep_rows = (B.draw < D).values
                sub = B[keep_rows].reset_index(drop=True)
                Msub = M_all[keep_rows]
                yIS = sub[f"Sharpe_IS{nb}"].values
                sdIS = sub["sd_IS"].values
                folds = np.arange(len(sub)) % N_FOLDS
                # pooled rows mix k, whose row sums differ: 2 UNPENALISED k dummies (idea 252's fix)
                kd = np.column_stack([(sub.k.values == kk).astype(float) for kk in KS[1:]])
                nkd = kd.shape[1]
                MsubK = np.column_stack([kd, Msub])
                MsdK = np.column_stack([sdIS / sdIS.std(), kd, Msub])
                Yis = yIS.reshape(-1, 1)
                _, cvM, _ = oof_paths(MsubK, Yis, folds, LAMS, free=nkd)
                _, cvMs, _ = oof_paths(MsdK, Yis, folds, LAMS, free=nkd + 1)
                picks = {
                    "S1 IS-Sharpe argmax": int(np.argmax(yIS)),
                    "S2 max IS sd": int(np.argmax(sdIS)),
                    "S3 sd-model OOF pred": int(np.argmax(oof_line(yIS, sdIS, folds))),
                    "S4 M-model OOF pred": int(np.argmax(cvM[:, 0])),
                    "S5 M+sd OOF pred": int(np.argmax(cvMs[:, 0])),
                    "S6 random draw": int(np.random.default_rng(SEED_S6 + D).integers(len(sub))),
                }
                wf.append(dict(panel=pan, n=nb, D=D, arm="S0 do-nothing (whole panel)",
                               k=np.nan, draw=np.nan,
                               OOS_CAGR=m0["CAGR"], OOS_Sharpe=m0["Sharpe"], OOS_MaxDD=m0["MaxDD"]))
                for arm, i in picks.items():
                    row = sub.iloc[i]
                    wf.append(dict(panel=pan, n=nb, D=D, arm=arm, k=int(row.k), draw=int(row.draw),
                                   OOS_CAGR=row[f"CAGR_OOS{nb}"], OOS_Sharpe=row[f"Sharpe_OOS{nb}"],
                                   OOS_MaxDD=row[f"MaxDD_OOS{nb}"]))
                wf.append(dict(panel=pan, n=nb, D=D, arm="SPY", k=np.nan, draw=np.nan,
                               OOS_CAGR=mspy_o["CAGR"], OOS_Sharpe=mspy_o["Sharpe"], OOS_MaxDD=mspy_o["MaxDD"]))
                wf.append(dict(panel=pan, n=nb, D=D, arm="RULES v2 (live book)", k=np.nan, draw=np.nan,
                               OOS_CAGR=mv2_o["CAGR"], OOS_Sharpe=mv2_o["Sharpe"], OOS_MaxDD=mv2_o["MaxDD"]))
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(fmt(W.set_index(["panel", "n", "D", "arm"])[["k", "draw", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]]))
    P("\n  Selector summary - mean OOS Sharpe over the 7 ladder points x 2 book sizes, by panel:")
    smry = W.groupby(["panel", "arm"]).agg(OOS_Sharpe=("OOS_Sharpe", "mean"),
                                           OOS_CAGR=("OOS_CAGR", "mean"),
                                           OOS_MaxDD=("OOS_MaxDD", "mean")).reset_index()
    P(fmt(smry.set_index(["panel", "arm"])))
    for pan in PANELS:
        s = W[W.panel == pan]
        spy_s = s[s.arm == "SPY"].OOS_Sharpe.iloc[0]
        for arm in ["S3 sd-model OOF pred", "S4 M-model OOF pred", "S5 M+sd OOF pred"]:
            a = s[s.arm == arm]
            P(f"    {pan} {arm:<24} beats SPY OOS Sharpe in {int((a.OOS_Sharpe > spy_s).sum())} of {len(a)} "
              f"(mean {a.OOS_Sharpe.mean():+.4f} vs SPY {spy_s:+.4f})")
        a4 = s[s.arm == "S4 M-model OOF pred"].sort_values(["n", "D"]).OOS_Sharpe.values
        a3 = s[s.arm == "S3 sd-model OOF pred"].sort_values(["n", "D"]).OOS_Sharpe.values
        P(f"    {pan} the name-additive selector beats the dispersion selector out of sample in "
          f"{int((a4 > a3).sum())} of {len(a4)} ladder points (mean difference {np.mean(a4 - a3):+.4f})")

    G_out = pd.concat([G[p].assign(panel=p).drop(columns=["cols"]) for p in PANELS])
    G_out.to_csv(OUT / f"{STEM}.grid.csv.gz", index=False, compression="gzip")
    P(f"\n  wrote {STEM}.grid.csv.gz ({len(G_out)} books), .nested.csv ({len(L)} ladder points), "
      f".crossover.csv ({len(C)}), .walkforward.csv ({len(W)})")
    P(f"\nElapsed {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()

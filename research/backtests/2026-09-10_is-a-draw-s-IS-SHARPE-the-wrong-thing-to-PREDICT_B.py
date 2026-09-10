#!/usr/bin/env python3
"""Idea 487 - "is-a-draw-s-IS-SHARPE-the-wrong-thing-to-PREDICT" (lane B, 2026-09-10).

The question
------------
Idea 484 re-ran idea 252's nested comparison on a 500-draw-per-k-cell ladder and found the
name-additive ridge WINS THE FIT of a draw's in-sample Sharpe by up to +0.6 out-of-fold R2 and
still LOSES THE CHOICE: no selector's rule-8 pick beats the live book on either panel.  Two very
different things produce that pattern:

    (i)  the selector is fine and the TARGET is wrong - IS Sharpe is fittable but carries no
         information about any later window, so every selector that maximises a prediction of it
         is maximising noise; or
    (ii) the target is fine and 2017-2026 simply did not look like 2009-2016 - a regime story,
         in which case a sub-panel choice is not hopeless, it is just out of sample.

The record cannot tell these apart, because every transfer test it has run scores IS-fitted
predictions on the OOS window, which confounds "is this predictable" with "did the regime hold".
This run separates them by never touching the OOS window for the decisive leg: the IS window is
CUT IN HALF and the models are fitted on the first half's target and scored on the SECOND HALF'S
outcome.  Both halves are in-sample by PROTOCOL rule 8's own definition, so if nothing transfers
across that seam, sub-panel choice is a null on its own training data and the record should stop
selecting on it.

Three legs, the same grid, the same two models, nested:

    FIT        fit y_IS1, score y_IS1   out of fold    - can the target be fitted at all?
    TRANSFER   fit y_IS1, score y_IS2   out of fold    - does the fit describe a LATER window?
                                                         (IS ONLY - no OOS data is read)
    OOS        fit y_IS , score y_OOS   out of fold    - the record's own leg, reported last

Models (idea 252's, unchanged in form):
    sd      y ~ sd                     (2 parameters, OLS, out of fold)
    M       y ~ k-dummies + name dummies (ridge, lambda by nested inner 5-fold CV)
    M+sd    y ~ sd + k-dummies + name dummies (ridge, sd and k unpenalised)
Predictors are measured on the FITTING window only (sd_IS1 for the IS legs, sd_IS for the OOS
leg); name membership is window-free by construction.

Pre-registered reading (written before any new number was read)
---------------------------------------------------------------
Scored over the 36 reported cells (TARGET x PANEL x k x book size); "transfer" statistics are
Spearman rho of the out-of-fold prediction against the later window's outcome, the centred
transfer R2 (level shift between windows removed, which a raw R2 would otherwise dominate), and
the TOP-DECILE SELECTION GAIN - mean later-window outcome of the best-predicted 10% of draws
minus the cell mean, with a two-sample t.

    NULL INSIDE IS   if  median Spearman < 0.10 for ALL THREE models
                     AND centred transfer R2 <= 0 in >= 2/3 of cells
                     AND |t| of the top-decile gain < 2 in >= 2/3 of cells.
                     -> The target is not the problem and the regime is not the problem: a
                        drawn sub-panel's later Sharpe is not predictable from its own earlier
                        Sharpe on this grid.  Sub-panel choice is a null and the record should
                        stop selecting on it.

    TRANSFERS IN IS  if some model clears median Spearman >= 0.20 AND a top-decile gain with
    ONLY             t >= 2 in a majority of cells on the IS1->IS2 leg, while the IS->OOS leg
                     fails the same bar.  -> idea 484's choice failure is REGIME, not
                        predictability; the queue's phrasing is right and IS Sharpe is a
                        defensible target inside a regime.

    TRANSFERS BOTH   if both legs clear that bar -> idea 484's failure is in the selection RULE,
                     not in the target, and the record should re-run the choice.

    SPLIT            anything else, reported as it falls.

Tuned parameters: exactly two - TARGET in {Sharpe, CAGR, premium} and PANEL in {B136,
SMALL484}.  Every grid point is reported.  k in {20,40,80}, book size in {5,20}, D=500 draws per
k cell, 10 folds, the six penalties, the seeds, the 10 bps / weekly / next-day execution and the
2009-2016 / 2017-2026 split are idea 78/252/484's constants, imported verbatim, not dials.

PROTOCOL: 10 bps (rule 2), next-day execution (engine), both KEEP paths on every one of the
3,000 drawn books and on every rule-8 pick (rule 4), walk-forward with everything chosen on
2009-2016 and 2017-2026 read exactly once (rule 8).  SURVIVORSHIP: both panels are current
constituents only (rule 9 / data/SMALL_PANEL_README.md).

Gates fire before any new number is read: the vectorised backtester against engine.backtest, the
live RULES v2 row, this run's reproduction of idea 484's committed 3,000-book grid column by
column, and the IS1/IS2 partition identity.

Deterministic, standalone.  Reads research/baseline.py and products/backtester/engine.py; writes
only files named after itself.
"""
import sys, time, warnings
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
sys.path.insert(0, str(REPO / "products" / "backtester"))
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore", category=RuntimeWarning)
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score
from engine import backtest, metrics, rebalance_mask

# ---- idea 78/252/484's constants, imported verbatim -------------------------------
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
D_MAX = 500

# ---- this run's two tuned parameters ----------------------------------------------
TARGETS = ["Sharpe", "CAGR", "premium"]
PANELS = ["B136", "SMALL484"]

SCRIPT = Path(__file__).name
OUT = REPO / "research" / "backtests"
STEM = SCRIPT[:-3]
REF_GRID = OUT / "2026-09-09_does-one-dispersion-number-really-out-predict-136-name-dummies_C.grid.csv.gz"

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 4000)

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _lines.append(s)


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ---------------------------------------------------------------- book helpers (idea 78's)
def fast_backtest(prices, weights, cost_bps=COST_BPS, freq=FREQ):
    """Vectorised equivalent of engine.backtest's return series (gated below)."""
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


def centred_r2(y, pred):
    """R2 of the prediction after its LEVEL is matched to y's.

    A raw R2 across two different windows is dominated by the level and scale difference between
    the windows (2013-2016 Sharpes are simply higher than 2009-2013's), which is not what the
    question asks: the question is whether the ORDERING and SPREAD the model learned on the first
    window survive into the second.  Matching the mean is the smallest correction that removes the
    level without giving the model a free slope.
    """
    y = np.asarray(y, float); pred = np.asarray(pred, float)
    return oof_r2(y, pred - pred.mean() + y.mean())


def spearman(a, b):
    a = pd.Series(np.asarray(a, float)).rank().values
    b = pd.Series(np.asarray(b, float)).rank().values
    if a.std() == 0 or b.std() == 0:
        return np.nan
    return float(np.corrcoef(a, b)[0, 1])


def rho_t(rho, n):
    """Asymptotic t of a rank correlation: rho * sqrt(n-2) / sqrt(1-rho^2)."""
    if not np.isfinite(rho) or abs(rho) >= 1 or n < 4:
        return np.nan
    return float(rho * np.sqrt(n - 2) / np.sqrt(1 - rho ** 2))


def decile_gain(pred, y2, q=0.10):
    """Mean later-window outcome of the best-predicted q of draws, minus the rest, with Welch t.

    This is the statistic a selector actually spends: "if I keep the top decile my model likes,
    what do I get in the next window?"
    """
    pred = np.asarray(pred, float); y2 = np.asarray(y2, float)
    n = len(pred); m = max(2, int(round(q * n)))
    top = np.argsort(-pred)[:m]
    mask = np.zeros(n, bool); mask[top] = True
    a, b = y2[mask], y2[~mask]
    se = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
    return float(a.mean() - b.mean()), (float((a.mean() - b.mean()) / se) if se > 0 else np.nan), \
        float(a.mean() - y2.mean())


def _solve_multi(A, Xc, Y, ym, lam, free):
    d = np.full(A.shape[0], float(lam))
    if free:
        d[:free] = 0.0
    return np.linalg.solve(A + np.diag(d), Xc.T @ (Y - ym))


def oof_paths(M, Y, folds, lams, free=0, inner_k=5):
    """Idea 484's multi-target out-of-fold ridge, verbatim: one Gram per fold, nested inner CV
    for the penalty, held-out rows never seen.  Returns per-lambda predictions and the CV ones."""
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
    y = np.asarray(y, float); x = np.asarray(x, float)
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
        "B136": (px136, [c for c in px136.columns]),                   # idea 78: SPY tradable
        "SMALL484": (pxs, [c for c in pxs.columns if c != "SPY"]),      # idea 78: SPY benchmark only
    }


def draw_books(px, names, k, d_hi, seed, startb, is1_end):
    """Idea 484's draw_books with the IS window CUT IN HALF: every book also carries its first-
    half-IS and second-half-IS Sharpe/CAGR/premium and its first-half-IS dispersion.  The
    generator, the eligibility, the weights, the costs and the cadence are unchanged, so the
    columns idea 484 published must re-derive exactly (gate [c])."""
    rng = np.random.default_rng(seed)
    rows = []
    for d in range(d_hi):
        cols = list(rng.choice(names, size=k, replace=False))
        keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px.columns else [])))
        p = px[keep].dropna(how="all").ffill()
        s, above, vol20 = score(p, vol_scale=False)
        elig = (above & (vol20 < MAX_VOL)).copy()
        drop = [c for c in p.columns if c not in set(cols)]
        if drop:
            elig[drop] = False
        rank = s.where(elig).rank(axis=1, ascending=False)
        wm = rebalance_mask(p.index, FREQ).values
        ne = elig[wm].sum(axis=1).loc[startb:]
        mom_p = (p[cols].shift(21) / p[cols].shift(252) - 1).where(elig[cols])
        sdw = mom_p[wm].loc[startb:].std(axis=1)
        cnt = elig.sum(axis=1).replace(0, np.nan)
        w_ew = elig.astype(float).div(cnt, axis=0).mul(GROSS).fillna(0.0)
        r_e = fast_backtest(p, w_ew).loc[startb:]
        me = metrics(r_e)
        me1 = metrics(r_e.loc[:is1_end]); me2 = metrics(r_e.loc[:IS_END].loc[is1_end:].iloc[1:])
        rec = dict(k=k, draw=d, cols=cols,
                   n_elig=float(ne.mean()), sd=float(sdw.mean()),
                   n_elig_IS=float(ne.loc[:IS_END].mean()), sd_IS=float(sdw.loc[:IS_END].mean()),
                   sd_IS1=float(sdw.loc[:is1_end].mean()),
                   n_elig_IS1=float(ne.loc[:is1_end].mean()),
                   ew_Sharpe=me["Sharpe"], ew_CAGR=me["CAGR"], ew_MaxDD=me["MaxDD"],
                   ew_Sharpe_IS1=me1["Sharpe"], ew_CAGR_IS1=me1["CAGR"],
                   ew_Sharpe_IS2=me2["Sharpe"], ew_CAGR_IS2=me2["CAGR"])
        for nb in N_BOOKS:
            w_c = (rank <= nb).astype(float) * (GROSS / nb)
            r_c = fast_backtest(p, w_c).loc[startb:]
            mc = metrics(r_c); h1, h2 = half_sharpes(r_c)
            oo = r_c.loc[OOS_START:]; mo = metrics(oo)
            m_is = metrics(r_c.loc[:IS_END])
            m1 = metrics(r_c.loc[:is1_end])
            m2 = metrics(r_c.loc[:IS_END].loc[is1_end:].iloc[1:])
            rec.update({f"CAGR{nb}": mc["CAGR"], f"Sharpe{nb}": mc["Sharpe"], f"MaxDD{nb}": mc["MaxDD"],
                        f"H1_{nb}": h1, f"H2_{nb}": h2,
                        f"Sharpe_IS{nb}": m_is["Sharpe"], f"CAGR_IS{nb}": m_is["CAGR"],
                        f"Sharpe_OOS{nb}": mo["Sharpe"], f"CAGR_OOS{nb}": mo["CAGR"],
                        f"MaxDD_OOS{nb}": mo["MaxDD"], f"premium{nb}": mc["Sharpe"] - me["Sharpe"],
                        f"Sharpe_IS1{nb}": m1["Sharpe"], f"CAGR_IS1{nb}": m1["CAGR"],
                        f"MaxDD_IS1{nb}": m1["MaxDD"],
                        f"Sharpe_IS2{nb}": m2["Sharpe"], f"CAGR_IS2{nb}": m2["CAGR"],
                        f"MaxDD_IS2{nb}": m2["MaxDD"],
                        f"premium_IS1{nb}": m1["Sharpe"] - me1["Sharpe"],
                        f"premium_IS2{nb}": m2["Sharpe"] - me2["Sharpe"],
                        f"premium_IS{nb}": m_is["Sharpe"] - metrics(r_e.loc[:IS_END])["Sharpe"],
                        f"premium_OOS{nb}": mo["Sharpe"] - metrics(r_e.loc[OOS_START:])["Sharpe"]})
        rows.append(rec)
    return rows


def tcol(kind, nb, win):
    """Column name of target `kind` for book size `nb` on window `win`."""
    if kind == "Sharpe":
        return f"Sharpe_{win}{nb}" if win != "FULL" else f"Sharpe{nb}"
    if kind == "CAGR":
        return f"CAGR_{win}{nb}" if win != "FULL" else f"CAGR{nb}"
    if kind == "premium":
        return f"premium_{win}{nb}" if win != "FULL" else f"premium{nb}"
    raise KeyError(kind)


# ================================================================== main
def main():
    t0 = time.time()
    P("=" * 200)
    P("IDEA 487 - is-a-draw-s-IS-SHARPE-the-wrong-thing-to-PREDICT  (lane B, 2026-09-10)")
    P("Idea 484: the name-additive ridge WINS the out-of-fold FIT of a draw's IS Sharpe by up to +0.6 R2")
    P("and still LOSES the rule-8 CHOICE on both panels.  Is the target unpredictable, or did the regime")
    P("change?  Decisive leg never reads 2017-2026: cut the IS window in half, fit on IS1, score on IS2.")
    P(f"Two tuned parameters: TARGET in {TARGETS} x PANEL in {PANELS}.  All grid points reported.")
    P("=" * 200)

    # ---------------------------------------------------------------- [a] harness
    P("\n[a] HARNESS - published rows recomputed from engine.backtest before anything new is read")
    px56 = load_universe()
    s56 = px56.index[260]
    s56v, above56, vol56 = score(px56, vol_scale=False)
    e56 = (above56 & (vol56 < MAX_VOL))
    w56 = (s56v.where(e56).rank(axis=1, ascending=False) <= 20).astype(float) * (GROSS / 20)
    r_u56 = backtest(px56, w56, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[s56:]
    m = metrics(r_u56); h1, h2 = half_sharpes(r_u56)
    P(f"    U56/CAND20   {m['CAGR']:.4%} / {m['Sharpe']:.5f} / {m['MaxDD']:.4%}  halves {h1:.5f}/{h2:.5f}"
      f"   (ideas 2/73/77/83/252/484 published 12.7% / 1.092-1.093 / -18.3%)")
    r_v2_56 = backtest(px56, rules_v2_weights(px56), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[s56:]
    m = metrics(r_v2_56); b1, b2 = half_sharpes(r_v2_56)
    P(f"    U56/RULES v2 (LIVE) {m['CAGR']:.4%} / {m['Sharpe']:.5f} / {m['MaxDD']:.4%}  halves {b1:.5f}/{b2:.5f}"
      f"   (idea 415 G2 published 8.66% / 1.2056 / -12.05%)")

    panels = panel_defs()
    ctx = {}
    for pan, (px, names) in panels.items():
        startb = px.index[260]
        isdays = px.loc[startb:IS_END].index
        is1_end = isdays[len(isdays) // 2 - 1]              # IS cut in half BY TRADING-DAY COUNT
        is2_start = isdays[len(isdays) // 2]
        spy = px["SPY"].pct_change().fillna(0).loc[startb:]
        base1 = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[startb:]
        base2 = backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[startb:]
        ctx[pan] = dict(px=px, names=names, startb=startb, spy=spy, spy_oos=spy.loc[OOS_START:],
                        v1=base1, v2=base2, is1_end=is1_end, is2_start=is2_start, n_is=len(isdays))
        ms = metrics(spy); sh1, sh2 = half_sharpes(spy)
        P(f"\n    {pan}: {len(names)} tradable names, window {startb.date()} -> {px.index[-1].date()} "
          f"({len(spy)} days)")
        P(f"      IS {startb.date()}..{pd.Timestamp(IS_END).date()} = {len(isdays)} days, cut at "
          f"{is1_end.date()}: IS1 {startb.date()}..{is1_end.date()} ({len(isdays) // 2} d), "
          f"IS2 {is2_start.date()}..{pd.Timestamp(IS_END).date()} ({len(isdays) - len(isdays) // 2} d)")
        P(f"      SPY      {ms['CAGR']:.2%} / {ms['Sharpe']:.3f} / {ms['MaxDD']:.2%}  halves {sh1:.3f}/{sh2:.3f}"
          f"  OOS {metrics(spy.loc[OOS_START:])['Sharpe']:.3f}")
        for lab, b in (("RULES v1", base1), ("RULES v2 (live)", base2)):
            mb = metrics(b); q1, q2 = half_sharpes(b)
            P(f"      {lab:<15} {mb['CAGR']:.2%} / {mb['Sharpe']:.3f} / {mb['MaxDD']:.2%}  halves {q1:.3f}/{q2:.3f}"
              f"  OOS {metrics(b.loc[OOS_START:])['Sharpe']:.3f}")
        P(f"      4b bars: MaxDD <= {0.60 * abs(ms['MaxDD']):.2%}, CAGR >= {0.70 * ms['CAGR']:.2%}, "
          f"H1 > {sh1:.3f}, H2 > {sh2:.3f}, OOS Sharpe > {metrics(spy.loc[OOS_START:])['Sharpe']:.3f}")

    # ---------------------------------------------------------------- [b] fast backtest gate
    P("\n[b] GATE 1 - the vectorised backtester vs engine.backtest on 6 drawn B136 books")
    px136, names136 = panels["B136"]; startb136 = ctx["B136"]["startb"]
    gate_max = 0.0
    rng = np.random.default_rng(SEED_B + 40)
    for _ in range(6):
        cols = list(rng.choice(names136, size=40, replace=False))
        keep = list(dict.fromkeys(cols + ["SPY"]))
        p = px136[keep].dropna(how="all").ffill()
        s, above, vol20 = score(p, vol_scale=False)
        elig = (above & (vol20 < MAX_VOL)).copy()
        drop = [c for c in p.columns if c not in set(cols)]
        if drop:
            elig[drop] = False
        w = (s.where(elig).rank(axis=1, ascending=False) <= 20).astype(float) * (GROSS / 20)
        a = backtest(p, w, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[startb136:]
        b = fast_backtest(p, w).loc[startb136:]
        gate_max = max(gate_max, float(np.abs(a.values - b.values).max()))
    ok_b = gate_max < 1e-12
    P(f"    max abs difference over 6 books: {gate_max:.3e}   GATE 1 {'PASS' if ok_b else 'FAIL'}")

    # ---------------------------------------------------------------- the grid
    P("\n" + "=" * 200)
    P(f"BOOK GRID - {D_MAX} draws per k cell x 3 k x 2 panels = {D_MAX * 3 * 2} sub-panels; CAND-5, CAND-20")
    P(f"and EWall on each, {COST_BPS} bps, weekly, next-day execution; every window stated per book.")
    P("=" * 200)
    G = {}
    for pan in PANELS:
        c = ctx[pan]
        rows = []
        for k in KS:
            rows += draw_books(c["px"], c["names"], k, D_MAX, SEED_B + k, c["startb"], c["is1_end"])
            P(f"    {pan} k={k:<3} {D_MAX} draws done ({time.time() - t0:.0f}s)")
        G[pan] = pd.DataFrame(rows)
    P(f"    grid built in {time.time() - t0:.0f}s")

    # ---------------------------------------------------------------- [c] reproduction gate
    P("\n[c] GATE 2 - this run's 3,000 books vs idea 484's COMMITTED grid, column by column")
    ok_c = True
    if REF_GRID.exists():
        ref = pd.read_csv(REF_GRID)
        mine = pd.concat([G[p].assign(panel=p) for p in PANELS], ignore_index=True)
        shared = [c for c in ref.columns if c in mine.columns and c not in ("panel",)]
        ref_k = ref.set_index(["panel", "k", "draw"]).sort_index()
        mine_k = mine.set_index(["panel", "k", "draw"]).sort_index()
        common = ref_k.index.intersection(mine_k.index)
        ref_k = ref_k.loc[common]; mine_k = mine_k.loc[common]
        P(f"    rows: idea 484 {len(ref)}, this run {len(mine)}, compared on {len(common)}; "
          f"shared numeric columns {len(shared) - 2}")
        worst = 0.0; worst_col = ""
        for col in shared:
            if col in ("k", "draw"):
                continue
            d = float(np.abs(ref_k[col].values - mine_k[col].values).max())
            if d > worst:
                worst, worst_col = d, col
            P(f"      {col:<16} max |diff| {d:.3e}")
        ok_c = worst < 1e-12
        P(f"    worst column {worst_col} at {worst:.3e}   GATE 2 {'PASS' if ok_c else 'FAIL'}")
    else:
        ok_c = False
        P(f"    MISSING reference grid {REF_GRID.name}   GATE 2 FAIL")

    # ---------------------------------------------------------------- [d] partition gate
    P("\n[d] GATE 3 - the IS1/IS2 cut is a PARTITION of the IS window (no overlap, no gap, no OOS)")
    ok_d = True
    for pan in PANELS:
        c = ctx[pan]; px = c["px"]
        idx = px.loc[c["startb"]:].index
        i1 = idx[(idx >= c["startb"]) & (idx <= c["is1_end"])]
        i2 = idx[(idx >= c["is2_start"]) & (idx <= pd.Timestamp(IS_END))]
        i3 = idx[idx >= pd.Timestamp(OOS_START)]
        isd = idx[idx <= pd.Timestamp(IS_END)]
        okp = (len(set(i1) & set(i2)) == 0 and len(i1) + len(i2) == len(isd)
               and len(set(i1) | set(i2)) == len(isd) and i2[-1] < i3[0])
        ok_d &= okp
        P(f"    {pan}: IS1 {len(i1)} + IS2 {len(i2)} = {len(i1) + len(i2)} == IS {len(isd)}; "
          f"overlap {len(set(i1) & set(i2))}; IS2 ends {i2[-1].date()} < OOS starts {i3[0].date()}  "
          f"{'PASS' if okp else 'FAIL'}")
    P(f"    GATE 3 {'PASS' if ok_d else 'FAIL'}")

    # ---------------------------------------------------------------- membership matrices
    P("\n" + "=" * 200)
    P("MEMBERSHIP MATRICES (idea 484's, unchanged)")
    P("=" * 200)
    MM = {}
    for pan in PANELS:
        names = ctx[pan]["names"]; idxn = {c: i for i, c in enumerate(names)}
        B = G[pan]
        M = np.zeros((len(B), len(names)))
        for i, cols in enumerate(B["cols"].values):
            for cc in cols:
                M[i, idxn[cc]] = 1.0
        MM[pan] = M
        P(f"    {pan}: P={len(names)} name columns, {len(B)} rows; N/P per k cell {D_MAX / len(names):.2f}")

    # ================================================================ THE THREE LEGS
    P("\n" + "=" * 200)
    P("THE THREE LEGS - one design per (panel, k), targets stacked; 10 folds by draw index.")
    P("  FIT       fit y_IS1, score y_IS1  (can the target be fitted at all?)")
    P("  TRANSFER  fit y_IS1, score y_IS2  (does the fit describe a LATER window?  NO OOS DATA READ)")
    P("  OOS       fit y_IS , score y_OOS  (the record's own leg)")
    P("Statistics: out-of-fold R2 on the fitting window; Spearman rho, CENTRED R2 and TOP-DECILE")
    P("SELECTION GAIN (Welch t) against the scoring window.")
    P("=" * 200)

    legs = []
    for pan in PANELS:
        B = G[pan]; M_all = MM[pan]
        for k in KS:
            sel = np.flatnonzero((B.k == k).values)
            sub = B.iloc[sel].reset_index(drop=True)
            Msub = M_all[sel]
            folds = np.arange(len(sub)) % N_FOLDS
            for leg, fitwin, scorewin, sdcol in (("TRANSFER(IS1->IS2)", "IS1", "IS2", "sd_IS1"),
                                                 ("OOS(IS->OOS)", "IS", "OOS", "sd_IS")):
                sdv = sub[sdcol].values
                # stack the 6 (target x book size) fitting-window columns on one design
                keys = [(kind, nb) for kind in TARGETS for nb in N_BOOKS]
                Yfit = np.column_stack([sub[tcol(kind, nb, fitwin)].values for kind, nb in keys])
                Yscore = np.column_stack([sub[tcol(kind, nb, scorewin)].values for kind, nb in keys])
                Mridge = np.column_stack([Msub])
                _, cvM, _ = oof_paths(Mridge, Yfit, folds, LAMS, free=0)
                Msd = np.column_stack([sdv / sdv.std(), Msub])
                _, cvMs, _ = oof_paths(Msd, Yfit, folds, LAMS, free=1)
                for j, (kind, nb) in enumerate(keys):
                    yf = Yfit[:, j]; ys = Yscore[:, j]
                    preds = {"sd": oof_line(yf, sdv, folds), "M": cvM[:, j], "M+sd": cvMs[:, j]}
                    for mdl, pr in preds.items():
                        g, tg, gm = decile_gain(pr, ys)
                        legs.append(dict(leg=leg, panel=pan, target=kind, n=nb, k=k, model=mdl,
                                         N=len(sub),
                                         fit_oofR2=oof_r2(yf, pr),
                                         fit_rho=spearman(pr, yf),
                                         tr_R2=oof_r2(ys, pr),
                                         tr_R2c=centred_r2(ys, pr),
                                         tr_rho=spearman(pr, ys),
                                         dec_gain=g, dec_t=tg, dec_vs_mean=gm,
                                         argmax_pctile=float((ys <= ys[int(np.argmax(pr))]).mean()),
                                         y_fit_mean=float(yf.mean()), y_score_mean=float(ys.mean()),
                                         y_fit_sd=float(yf.std()), y_score_sd=float(ys.std()),
                                         rho_y1y2=spearman(yf, ys),
                                         t_tr_rho=rho_t(spearman(pr, ys), len(sub)),
                                         t_rho_y1y2=rho_t(spearman(yf, ys), len(sub))))
            P(f"    {pan} k={k:<3} both legs done ({time.time() - t0:.0f}s)")
    L = pd.DataFrame(legs)
    L.to_csv(OUT / f"{STEM}.legs.csv", index=False)

    SHOW = ["N", "fit_oofR2", "fit_rho", "tr_R2", "tr_R2c", "tr_rho", "t_tr_rho", "dec_gain",
            "dec_t", "argmax_pctile", "rho_y1y2", "t_rho_y1y2"]
    P("\nALL GRID POINTS - TRANSFER leg (IS1 -> IS2), no OOS data touched:")
    P(fmt(L[L.leg == "TRANSFER(IS1->IS2)"].set_index(["panel", "target", "n", "k", "model"])[SHOW]))
    P("\nALL GRID POINTS - OOS leg (IS -> 2017-2026), the record's own:")
    P(fmt(L[L.leg == "OOS(IS->OOS)"].set_index(["panel", "target", "n", "k", "model"])[SHOW]))

    P("\nPRE-REGISTERED SCORING - medians over the 36 cells (TARGET x PANEL x k x book size) per leg/model:")
    sc = []
    for leg in L.leg.unique():
        for mdl in ("sd", "M", "M+sd"):
            s = L[(L.leg == leg) & (L.model == mdl)]
            sc.append(dict(leg=leg, model=mdl, cells=len(s),
                           med_fit_oofR2=s.fit_oofR2.median(), med_tr_rho=s.tr_rho.median(),
                           tr_rho_ge_0p20=int((s.tr_rho >= 0.20).sum()),
                           med_tr_R2c=s.tr_R2c.median(),
                           tr_R2c_le_0=int((s.tr_R2c <= 0).sum()),
                           med_dec_gain=s.dec_gain.median(),
                           dec_t_ge_2=int((s.dec_t >= 2).sum()),
                           dec_t_abs_lt_2=int((s.dec_t.abs() < 2).sum()),
                           med_argmax_pctile=s.argmax_pctile.median(),
                           tr_rho_t_ge_2=int((s.t_tr_rho >= 2).sum()),
                           med_rho_y1y2=s.rho_y1y2.median(),
                           rho_y1y2_t_ge_2=int((s.t_rho_y1y2.abs() >= 2).sum())))
    S = pd.DataFrame(sc)
    P(fmt(S.set_index(["leg", "model"])))
    P("\n  rho_y1y2 is the RAW persistence of the target itself across the two windows - the ceiling")
    P("  any selector that predicts window 1 to choose for window 2 can possibly reach.")

    tr = L[L.leg == "TRANSFER(IS1->IS2)"]; oo = L[L.leg == "OOS(IS->OOS)"]
    ncell = len(tr) // 3
    cond_null = (all(tr[tr.model == m].tr_rho.median() < 0.10 for m in ("sd", "M", "M+sd"))
                 and (tr.tr_R2c <= 0).sum() >= (2 / 3) * len(tr)
                 and (tr.dec_t.abs() < 2).sum() >= (2 / 3) * len(tr))
    def clears(df):
        return any((df[df.model == m].tr_rho.median() >= 0.20) and
                   ((df[df.model == m].dec_t >= 2).sum() > 0.5 * ncell) for m in ("sd", "M", "M+sd"))
    cl_tr, cl_oo = clears(tr), clears(oo)
    P(f"\n  bar check: NULL-INSIDE-IS conditions {'ALL MET' if cond_null else 'NOT all met'}"
      f"  (all three median rho < 0.10: "
      f"{all(tr[tr.model == m].tr_rho.median() < 0.10 for m in ('sd', 'M', 'M+sd'))}; "
      f"centred R2 <= 0 in {int((tr.tr_R2c <= 0).sum())}/{len(tr)} (bar {2 / 3 * len(tr):.0f}); "
      f"|dec t| < 2 in {int((tr.dec_t.abs() < 2).sum())}/{len(tr)} (bar {2 / 3 * len(tr):.0f}))")
    P(f"  bar check: TRANSFER leg clears the POSITIVE bar: {cl_tr};  OOS leg clears it: {cl_oo}")
    if cond_null:
        reading = "NULL INSIDE IS"
    elif cl_tr and not cl_oo:
        reading = "TRANSFERS IN IS ONLY (regime, not predictability)"
    elif cl_tr and cl_oo:
        reading = "TRANSFERS BOTH (the selection RULE is the problem)"
    else:
        reading = "SPLIT"
    P(f"  PRE-REGISTERED READING: {reading}")

    # ---------------------------------------------------------------- the ceiling, explicitly
    P("\n" + "=" * 200)
    P("THE CEILING - persistence of the target itself, window 1 -> window 2, every cell")
    P("=" * 200)
    cl = L[L.model == "sd"][["leg", "panel", "target", "n", "k", "rho_y1y2", "t_rho_y1y2",
                             "y_fit_mean", "y_score_mean", "y_fit_sd", "y_score_sd"]]
    P(fmt(cl.set_index(["leg", "panel", "target", "n", "k"])))
    for leg in L.leg.unique():
        s = cl[cl.leg == leg]
        P(f"  {leg:<20} median rho(y1,y2) {s.rho_y1y2.median():+.4f}; positive in "
          f"{int((s.rho_y1y2 > 0).sum())}/{len(s)} cells; |t| >= 2 in "
          f"{int((s.t_rho_y1y2.abs() >= 2).sum())}/{len(s)}; range "
          f"{s.rho_y1y2.min():+.4f}..{s.rho_y1y2.max():+.4f}")
    for leg in L.leg.unique():
        for kind in TARGETS:
            s = cl[(cl.leg == leg) & (cl.target == kind)]
            P(f"    {leg:<20} target {kind:<8} median rho(y1,y2) {s.rho_y1y2.median():+.4f}  "
              f"(|t|>=2 in {int((s.t_rho_y1y2.abs() >= 2).sum())}/{len(s)})")

    # ---------------------------------------------------------------- KEEP paths
    P("\n" + "=" * 200)
    P("BOTH KEEP PATHS - every one of the 3,000 drawn books (PROTOCOL rule 4)")
    P("=" * 200)
    P("  4a: Sharpe > the comparand book in BOTH halves AND MaxDD no worse.")
    P("  4b: Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's.")
    keeprows = []
    bars = {}
    for pan in PANELS:
        c = ctx[pan]; B = G[pan]
        v1h1, v1h2 = half_sharpes(c["v1"]); v1dd = metrics(c["v1"])["MaxDD"]
        v2h1, v2h2 = half_sharpes(c["v2"]); v2dd = metrics(c["v2"])["MaxDD"]
        sh1, sh2 = half_sharpes(c["spy"]); msp = metrics(c["spy"])
        oos_spy = metrics(c["spy_oos"])["Sharpe"]
        bars[pan] = dict(v1h1=v1h1, v1h2=v1h2, v1dd=v1dd, v2h1=v2h1, v2h2=v2h2, v2dd=v2dd,
                         sh1=sh1, sh2=sh2, spydd=msp["MaxDD"], spycagr=msp["CAGR"], oos_spy=oos_spy)
        for nb in N_BOOKS:
            H1 = B[f"H1_{nb}"].values; H2 = B[f"H2_{nb}"].values
            DD = B[f"MaxDD{nb}"].values; CG = B[f"CAGR{nb}"].values
            OS = B[f"Sharpe_OOS{nb}"].values
            p4a1 = (H1 > v1h1) & (H2 > v1h2) & (DD >= v1dd)
            p4a2 = (H1 > v2h1) & (H2 > v2h2) & (DD >= v2dd)
            p4b = (H1 > sh1) & (H2 > sh2) & (OS > oos_spy) & (np.abs(DD) <= 0.60 * abs(msp["MaxDD"])) \
                & (CG >= 0.70 * msp["CAGR"])
            keeprows.append(dict(panel=pan, book=f"CAND{nb}", N=len(B),
                                 pass4a_v1=int(p4a1.sum()), pass4a_v2=int(p4a2.sum()),
                                 pass4b=int(p4b.sum()), pass_BOTH=int((p4a2 & p4b).sum())))
    K = pd.DataFrame(keeprows)
    K.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    P(fmt(K.set_index(["panel", "book"]), 0))

    # ---------------------------------------------------------------- rule 8
    P("\n" + "=" * 200)
    P("RULE 8 WALK-FORWARD - every selector fitted on 2009-2016 ONLY; 2017-2026 read once")
    P("=" * 200)
    P("Selectors: S0 do-nothing (whole panel), S1 IS-Sharpe argmax (the record's incumbent),")
    P("S2 IS1->IS2 PERSISTENCE argmax (this run's: pick the draw whose IS2 outcome the IS1-fitted")
    P("model likes, i.e. the selector the transfer leg says is or is not worth building), S3 sd line,")
    P("S4 M ridge, S5 M+sd ridge, S6 random draw.  S2-S5 pick on OOF predictions of IS data only.")
    wf = []
    for pan in PANELS:
        c = ctx[pan]; B = G[pan]; M_all = MM[pan]
        mspy_o = metrics(c["spy_oos"]); mv2_o = metrics(c["v2"].loc[OOS_START:])
        bb = bars[pan]
        for nb in N_BOOKS:
            px = c["px"]
            s, above, vol20 = score(px, vol_scale=False)
            elig = (above & (vol20 < MAX_VOL)).copy()
            drop = [x for x in px.columns if x not in set(c["names"])]
            if drop:
                elig[drop] = False
            w0 = (s.where(elig).rank(axis=1, ascending=False) <= nb).astype(float) * (GROSS / nb)
            r0 = fast_backtest(px, w0).loc[c["startb"]:]
            m0 = metrics(r0.loc[OOS_START:]); h01, h02 = half_sharpes(r0)
            m0f = metrics(r0)
            for kind in TARGETS:
                for k in KS:
                    sel = np.flatnonzero((B.k == k).values)
                    sub = B.iloc[sel].reset_index(drop=True)
                    Msub = M_all[sel]
                    folds = np.arange(len(sub)) % N_FOLDS
                    yIS = sub[tcol(kind, nb, "IS")].values
                    yIS1 = sub[tcol(kind, nb, "IS1")].values
                    yIS2 = sub[tcol(kind, nb, "IS2")].values
                    sdIS = sub["sd_IS"].values; sdIS1 = sub["sd_IS1"].values
                    Y = np.column_stack([yIS, yIS1])
                    _, cvM, _ = oof_paths(Msub, Y, folds, LAMS, free=0)
                    _, cvMs, _ = oof_paths(np.column_stack([sdIS / sdIS.std(), Msub]), Y, folds,
                                           LAMS, free=1)
                    picks = {
                        "S1 IS-target argmax": int(np.argmax(yIS)),
                        "S2 IS2 argmax on IS1 fit": int(np.argmax(cvM[:, 1])),
                        "S3 sd line OOF pred": int(np.argmax(oof_line(yIS, sdIS, folds))),
                        "S4 M ridge OOF pred": int(np.argmax(cvM[:, 0])),
                        "S5 M+sd ridge OOF pred": int(np.argmax(cvMs[:, 0])),
                        "S6 random draw": int(np.random.default_rng(SEED_S6 + k).integers(len(sub))),
                    }
                    wf.append(dict(panel=pan, target=kind, n=nb, k=k, arm="S0 do-nothing (whole panel)",
                                   draw=np.nan, OOS_CAGR=m0["CAGR"], OOS_Sharpe=m0["Sharpe"],
                                   OOS_MaxDD=m0["MaxDD"], H1=h01, H2=h02, CAGR=m0f["CAGR"],
                                   MaxDD=m0f["MaxDD"], IS2_pctile=np.nan))
                    for arm, i in picks.items():
                        row = sub.iloc[i]
                        wf.append(dict(panel=pan, target=kind, n=nb, k=k, arm=arm, draw=int(row.draw),
                                       OOS_CAGR=row[f"CAGR_OOS{nb}"], OOS_Sharpe=row[f"Sharpe_OOS{nb}"],
                                       OOS_MaxDD=row[f"MaxDD_OOS{nb}"], H1=row[f"H1_{nb}"],
                                       H2=row[f"H2_{nb}"], CAGR=row[f"CAGR{nb}"], MaxDD=row[f"MaxDD{nb}"],
                                       IS2_pctile=float((yIS2 <= yIS2[i]).mean())))
                    wf.append(dict(panel=pan, target=kind, n=nb, k=k, arm="SPY", draw=np.nan,
                                   OOS_CAGR=mspy_o["CAGR"], OOS_Sharpe=mspy_o["Sharpe"],
                                   OOS_MaxDD=mspy_o["MaxDD"], H1=bb["sh1"], H2=bb["sh2"],
                                   CAGR=bb["spycagr"], MaxDD=bb["spydd"], IS2_pctile=np.nan))
                    wf.append(dict(panel=pan, target=kind, n=nb, k=k, arm="RULES v2 (live book)",
                                   draw=np.nan, OOS_CAGR=mv2_o["CAGR"], OOS_Sharpe=mv2_o["Sharpe"],
                                   OOS_MaxDD=mv2_o["MaxDD"], H1=bb["v2h1"], H2=bb["v2h2"],
                                   CAGR=metrics(c["v2"])["CAGR"], MaxDD=bb["v2dd"], IS2_pctile=np.nan))
        P(f"    {pan} rule 8 done ({time.time() - t0:.0f}s)")
    W = pd.DataFrame(wf)
    # KEEP paths on every pick
    for pan in PANELS:
        bb = bars[pan]; m = W.panel == pan
        W.loc[m, "p4a_v2"] = ((W.loc[m, "H1"] > bb["v2h1"]) & (W.loc[m, "H2"] > bb["v2h2"])
                              & (W.loc[m, "MaxDD"] >= bb["v2dd"])).astype(int)
        W.loc[m, "p4a_v1"] = ((W.loc[m, "H1"] > bb["v1h1"]) & (W.loc[m, "H2"] > bb["v1h2"])
                              & (W.loc[m, "MaxDD"] >= bb["v1dd"])).astype(int)
        W.loc[m, "p4b"] = ((W.loc[m, "H1"] > bb["sh1"]) & (W.loc[m, "H2"] > bb["sh2"])
                           & (W.loc[m, "OOS_Sharpe"] > bb["oos_spy"])
                           & (W.loc[m, "MaxDD"].abs() <= 0.60 * abs(bb["spydd"]))
                           & (W.loc[m, "CAGR"] >= 0.70 * bb["spycagr"])).astype(int)
    W["p_BOTH"] = ((W.p4a_v2 == 1) & (W.p4b == 1)).astype(int)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P("\nALL WALK-FORWARD POINTS:")
    P(fmt(W.set_index(["panel", "target", "n", "k", "arm"])[
        ["draw", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "H1", "H2", "CAGR", "MaxDD",
         "IS2_pctile", "p4a_v2", "p4b", "p_BOTH"]]))

    P("\n  Selector summary - mean over the 3 targets x 3 k x 2 book sizes, by panel:")
    smry = W.groupby(["panel", "arm"]).agg(OOS_Sharpe=("OOS_Sharpe", "mean"),
                                           OOS_CAGR=("OOS_CAGR", "mean"),
                                           OOS_MaxDD=("OOS_MaxDD", "mean"),
                                           IS2_pctile=("IS2_pctile", "mean"),
                                           p4a_v2=("p4a_v2", "sum"), p4b=("p4b", "sum"),
                                           p_BOTH=("p_BOTH", "sum"), cells=("arm", "size")).reset_index()
    P(fmt(smry.set_index(["panel", "arm"])))
    sel_arms = ["S1 IS-target argmax", "S2 IS2 argmax on IS1 fit", "S3 sd line OOF pred",
                "S4 M ridge OOF pred", "S5 M+sd ridge OOF pred", "S6 random draw"]
    for pan in PANELS:
        s = W[W.panel == pan]
        spy_s = s[s.arm == "SPY"].OOS_Sharpe.iloc[0]
        v2_s = s[s.arm == "RULES v2 (live book)"].OOS_Sharpe.iloc[0]
        P(f"\n    {pan}: SPY OOS Sharpe {spy_s:+.4f}; live RULES v2 OOS Sharpe {v2_s:+.4f}")
        for arm in sel_arms:
            a = s[s.arm == arm]
            P(f"      {arm:<26} mean OOS Sharpe {a.OOS_Sharpe.mean():+.4f}  beats live book "
              f"{int((a.OOS_Sharpe > v2_s).sum())}/{len(a)}  beats SPY {int((a.OOS_Sharpe > spy_s).sum())}/{len(a)}"
              f"  mean IS2 percentile of the pick {a.IS2_pctile.mean():.3f}")
    tot = len(W[W.arm.isin(sel_arms)])
    P(f"\n  KEEP paths over the {tot} selector picks: 4a(v2) {int(W[W.arm.isin(sel_arms)].p4a_v2.sum())}, "
      f"4a(v1) {int(W[W.arm.isin(sel_arms)].p4a_v1.sum())}, 4b {int(W[W.arm.isin(sel_arms)].p4b.sum())}, "
      f"BOTH {int(W[W.arm.isin(sel_arms)].p_BOTH.sum())}")

    # ---------------------------------------------------------------- verdict
    P("\n" + "=" * 200)
    P("VERDICT")
    P("=" * 200)
    gates = dict(G1_fast=ok_b, G2_repro=ok_c, G3_partition=ok_d)
    P(f"  gates: {gates}")
    P(f"  pre-registered reading: {reading}")
    for leg in L.leg.unique():
        s = L[L.leg == leg]
        P(f"  {leg:<20} median fit oofR2 {s.fit_oofR2.median():+.4f} | median transfer rho "
          f"{s.tr_rho.median():+.4f} | median centred transfer R2 {s.tr_R2c.median():+.4f} | "
          f"median decile gain {s.dec_gain.median():+.4f} (t>=2 in {int((s.dec_t >= 2).sum())}/{len(s)})")
    grid_out = pd.concat([G[p].assign(panel=p).drop(columns=["cols"]) for p in PANELS])
    grid_out.to_csv(OUT / f"{STEM}.grid.csv.gz", index=False, compression="gzip")
    S.to_csv(OUT / f"{STEM}.scoring.csv", index=False)
    P(f"\n  wrote {STEM}.grid.csv.gz ({len(grid_out)} books), .legs.csv ({len(L)}), "
      f".scoring.csv ({len(S)}), .keeppaths.csv ({len(K)}), .walkforward.csv ({len(W)})")
    P(f"\nElapsed {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()

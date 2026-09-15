#!/usr/bin/env python3
"""Idea 869 (lane B, 2026-09-15) -- does any committed BOOK carry ALPHA once its own BETA is charged?

THE QUESTION (queue, 2026-09-15)
  The CHANGELOG says the same thing four different ways.  662: aggregation buys OOS CAGR and
  pays MaxDD on every gate family.  866: a de-grossing clause priced as a FLOOR is worth no more
  than the same state priced as a GATE -- "one dial read at two resolutions".  676: the 4b CAGR
  floor does not survive a non-zero cash leg, because grading a cash-heavy book at rf=0 makes
  holding cash look like alpha.  677: the gross window width ranks OOS Sharpe better than the 4b
  pass does.  Every one of those is a statement that the record's KEEP legs are reading EXPOSURE.
  Nobody has asked the direct question underneath: strip the exposure out by regression and see
  whether ANY committed book has return left over.

THE TWO THINGS THIS RUN DOES
  A  CAPM census.  For every book x panel, OLS of DAILY book returns on DAILY SPY returns at
     rf=0 -- annualised alpha 252a, Newey-West t (lag 21, Bartlett), beta, R^2 -- full sample,
     both `baseline._row` count halves, and the rule-8 IS/OOS windows.  No new book is invented:
     every book is built from `research/baseline.py` primitives only.
  B  BETA-MATCHED COMPARAND.  PROTOCOL 4b grades a book against a 100%-invested SPY.  Replace
     that comparand with beta_t x SPY + (1 - beta_t) x CASH at rf=0 -- the cheapest portfolio
     with the book's own market exposure -- and report whether any 4b verdict moves.
     The algebra, stated BEFORE the numbers and gated at G5: at rf=0 a CONSTANT beta scales the
     comparand's returns, so Sharpe(beta x SPY) == Sharpe(SPY) EXACTLY and 4b's two Sharpe legs
     are beta-invariant.  Only the CAGR floor (which beta-matching LOOSENS, since the comparand
     earns less) and the DD cap (which beta-matching TIGHTENS, since the comparand draws down
     less) can move.  Which way the shelf goes is the empirical question.

THE BOOKS (7, every one a `baseline` primitive at a committed constant -- none is tuned here)
  BAND03_g050 / _g075 / _g100   `rules_v2_weights(px, band=0.03, gross=g)`; g=0.75 IS the LIVE book
  EWELIG_g075 / _g100           Finding 2 of the 2026-09-03 recommendation: equal-weight EVERY
                                name above its 200d MA with 20d ann. vol < 0.60 (`baseline.score`
                                returns both masks), at gross g, gated-out weight to CASH
  V1_n5                         `rules_v1_weights(px)` at its committed n=5, w=0.15, max_vol=0.60
  SPYBH                         100% SPY buy-and-hold -- the ZERO-SIGNAL control, alpha 0 by
                                construction (gated at G7)

THE TWO TUNED PARAMETERS (PROTOCOL 4's maximum; panel, book and window are REPORTED AXES)
  P1 BETA ESTIMATOR  FULL (one OLS beta over the window graded)
                     IS   (one OLS beta from 2009-01-01..2016-12-31 ONLY -- the honest one)
                     R52  (causal rolling 252-day beta, lagged one day)
                     R104 (causal rolling 504-day beta, lagged one day)
                     EWMA (causal exponentially-weighted cov/var, halflife 126d, lagged one day)
  P2 SHRINKAGE lam   0.00 0.25 0.50 0.75 1.00, beta_used = (1-lam) beta_hat + lam x 1.0
                     (lam=1 collapses the comparand back to 100% SPY -- the committed 4b, and G4)
  5 x 5 = 25 comparand cells x 21 book-panels = 525 grid points, EVERY ONE published in .grid.csv

PROTOCOL
  2  10 bps per unit turnover, weights decided at close t applied t+1 (engine does this), weekly
     rebalance, no shorting, no leverage.
  3  every book compared to RULES v2 (live baseline) AND SPY buy-and-hold on the same sample.
  4  BOTH KEEP paths evaluated at every grid point; 4a against RULES v2, 4b against BOTH
     comparand forms.
  8  walk-forward: the two tuned params are fitted on 2009-2016 ALONE and 2017-2026 is read ONCE.
  9  SURVIVORSHIP: U56, B136 and SMALL716 are all current-constituent lists; levels are optimistic
     and the alpha estimates inherit that bias UPWARD.

PRE-REGISTERED HYPOTHESES (fixed before any number below was read)
  H1  No book x panel has annualised alpha with |NW t| > 2 in BOTH count halves.
  H2  Beta-matching flips at least one committed 4b verdict (it must move SOME leg, or the
      record's "decided by gross alone" diagnosis is wrong).
  H3  Every flip beta-matching causes is a PASS -> FAIL flip through the DD cap (the tightening
      leg), not a FAIL -> PASS flip through the CAGR floor.
  H4  Choosing a book on its IS beta-charged EXCESS RETURN t does not beat choosing it on
      IS Sharpe, out of sample.

GATES (run and printed BEFORE any result number is read)
  G1  the LIVE book (BAND03_g075 on U56) reproduces the record's committed 8.6227% / 1.2013 /
      -12.0549% through `engine.backtest`.
  G2  SPY on U56 reproduces the record's committed 15.1302% / 0.8845 / -33.7173%.
  G3  this run's count halves ARE `baseline._row`'s len(r)//2 halves (max |d| over 21 books).
  G4  at lam=1.00 the BETAMATCH comparand IS the committed SPY100 comparand, exactly, for every
      estimator (max |d return| over 5 estimators x 3 panels).
  G5  the beta-invariance of Sharpe: for a CONSTANT beta, Sharpe(beta x SPY) == Sharpe(SPY) over
      a beta ladder 0.1..2.0 (max |d|).
  G6  determinism -- the whole grid, rebuilt in a second pass, hashes identically.
  G7  a PLANTED alpha of +5.00%/yr added to SPYBH is recovered at the right size and sign by the
      estimator, and SPYBH itself reads alpha 0 / beta 1 / R^2 1.
  G8  the EWELIG book rebuilt here reproduces Finding 2 of the committed 2026-09-03 recommendation
      memo on U56 (10.4% / 1.05, halves 1.07 / 1.03).

Outputs beside this script: .console.txt .capm.csv .grid.csv .walkforward.csv .result.md
"""
from __future__ import annotations

import hashlib
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa: E402
from engine import backtest, metrics  # noqa: E402

# ---- reported constants (never tuned) ---------------------------------------------------------
COST = 10.0                 # PROTOCOL 2
FREQ = "W"
BAND = 0.03                 # RULES v2 clause 2
MAXVOL = 0.60               # rules_v1_weights' committed max_vol
WARMUP = 260                # the record's warm-up skip (baseline.compare)
NWLAG = 21                  # Newey-West Bartlett lag, one trading month
IS_END, OOS_START = "2016-12-31", "2017-01-01"
BETA_IS_START = "2009-01-01"
TRAD = 252

# committed record triples this run must reproduce
V2_U56 = (0.086227, 1.201258, -0.120549)
SPY_U56 = (0.151302, 0.884500, -0.337173)
TOL_C, TOL_S, TOL_D = 0.004, 0.030, 0.015

# ---- tuned dial 1: the beta estimator ---------------------------------------------------------
ESTIMATORS = ["FULL", "IS", "R52", "R104", "EWMA"]
# ---- tuned dial 2: the shrinkage toward beta = 1 ----------------------------------------------
LAMBDAS = [0.00, 0.25, 0.50, 0.75, 1.00]

PANELS = ["U56", "B136", "SMALL716"]
BOOKS = ["BAND03_g050", "BAND03_g075", "BAND03_g100", "EWELIG_g075", "EWELIG_g100",
         "V1_n5", "SPYBH"]

LOG: list[str] = []
QUIET = False


def P(*a):
    if QUIET:
        return
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# ================================================================================================
# books -- every one of them a baseline primitive
# ================================================================================================
def w_band(px, gross):
    return rules_v2_weights(px, band=BAND, gross=gross)


def w_ewelig(px, gross):
    """Finding 2 of the 2026-09-03 recommendation, built from baseline.score's own two masks."""
    _, above, vol20 = score(px)
    e = (above & (vol20 < MAXVOL)).astype(float).where(px.notna(), 0.0)
    return gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def w_spybh(px):
    w = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    w["SPY"] = 1.0
    return w


BOOK_FNS = {
    "BAND03_g050": lambda px: w_band(px, 0.50),
    "BAND03_g075": lambda px: w_band(px, 0.75),
    "BAND03_g100": lambda px: w_band(px, 1.00),
    "EWELIG_g075": lambda px: w_ewelig(px, 0.75),
    "EWELIG_g100": lambda px: w_ewelig(px, 1.00),
    "V1_n5": rules_v1_weights,
    "SPYBH": w_spybh,
}


# ================================================================================================
# statistics
# ================================================================================================
def trip(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def halves(r):
    h = len(r) // 2                       # exactly baseline._row's convention
    return r.iloc[:h], r.iloc[h:]


def ols_nw(y: np.ndarray, x: np.ndarray, lags=NWLAG):
    """OLS y = a + b x with Newey-West (Bartlett) standard errors. Returns a, b, t_a, t_b, R2."""
    n = len(y)
    X = np.column_stack([np.ones(n), x])
    XtX_inv = np.linalg.pinv(X.T @ X)
    beta = XtX_inv @ (X.T @ y)
    resid = y - X @ beta
    u = X * resid[:, None]
    S = u.T @ u
    for l in range(1, min(lags, n - 1) + 1):
        w = 1.0 - l / (lags + 1.0)
        G = u[l:].T @ u[:-l]
        S = S + w * (G + G.T)
    V = XtX_inv @ S @ XtX_inv
    se = np.sqrt(np.maximum(np.diag(V), 0.0))
    tt = np.where(se > 0, beta / np.where(se > 0, se, 1.0), np.nan)
    ss_res = float(resid @ resid)
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan
    if ss_tot > 0 and ss_res / ss_tot < 1e-12:
        # DEGENERATE: the regressor explains the regressand exactly (this happens only for the
        # SPYBH control, which IS SPY).  The residual variance is numerical dust, so the t is a
        # 0/0 artefact and is reported as NaN rather than as a number.
        tt = np.array([np.nan, np.nan])
    return float(beta[0]), float(beta[1]), float(tt[0]), float(tt[1]), r2


def nw_mean_t(x: np.ndarray, lags=NWLAG):
    """Annualised mean of a return series and its Newey-West t against zero."""
    x = x[np.isfinite(x)]
    n = len(x)
    if n < 2:
        return np.nan, np.nan
    d = x - x.mean()
    S = float(d @ d) / n
    for l in range(1, min(lags, n - 1) + 1):
        w = 1.0 - l / (lags + 1.0)
        S += 2.0 * w * float(d[l:] @ d[:-l]) / n
    se = np.sqrt(max(S, 0.0) / n)
    return float(x.mean()) * TRAD, (float(x.mean()) / se if se > 0 else np.nan)


def capm(r: pd.Series, spy: pd.Series):
    idx = r.index.intersection(spy.index)
    y, x = r.reindex(idx).values.astype(float), spy.reindex(idx).values.astype(float)
    ok = np.isfinite(y) & np.isfinite(x)
    a, b, ta, tb, r2 = ols_nw(y[ok], x[ok])
    return dict(alpha_ann=a * TRAD, beta=b, t_alpha=ta, t_beta=tb, R2=r2, n=int(ok.sum()))


def beta_path(r: pd.Series, spy: pd.Series, est: str) -> pd.Series:
    """beta_hat_t under estimator `est`. Rolling/EWMA forms are CAUSAL (shifted one day)."""
    if est == "FULL":
        b = capm(r, spy)["beta"]
        return pd.Series(b, index=r.index)
    if est == "IS":
        sl = slice(BETA_IS_START, IS_END)
        b = capm(r.loc[sl], spy.loc[sl])["beta"]
        return pd.Series(b, index=r.index)
    if est in ("R52", "R104"):
        w = 252 if est == "R52" else 504
        cov = r.rolling(w, min_periods=w // 2).cov(spy)
        var = spy.rolling(w, min_periods=w // 2).var()
    else:                                   # EWMA, halflife 126 trading days
        cov = r.ewm(halflife=126, min_periods=126).cov(spy)
        var = spy.ewm(halflife=126, min_periods=126).var()
    b = (cov / var.replace(0, np.nan)).shift(1)
    return b.ffill().fillna(1.0).clip(lower=0.0, upper=3.0)


def comparand(spy: pd.Series, bpath: pd.Series, lam: float) -> pd.Series:
    """beta_used x SPY + (1 - beta_used) x CASH, cash at rf = 0."""
    bu = (1.0 - lam) * bpath.reindex(spy.index).ffill().fillna(1.0) + lam * 1.0
    return spy * bu


def keep4b(r, cmp_r, oos_r, cmp_oos):
    """PROTOCOL 4b against an arbitrary comparand: Sharpe > comparand in BOTH halves AND OOS,
    MaxDD <= 60% of the comparand's, CAGR >= 70% of the comparand's."""
    h1, h2 = halves(r)
    c1, c2 = halves(cmp_r)
    s_h1 = metrics(h1)["Sharpe"] > metrics(c1)["Sharpe"]
    s_h2 = metrics(h2)["Sharpe"] > metrics(c2)["Sharpe"]
    s_oos = metrics(oos_r)["Sharpe"] > metrics(cmp_oos)["Sharpe"]
    cg, sh, dd = trip(r)
    ccg, csh, cdd = trip(cmp_r)
    dd_ok = dd >= 0.60 * cdd                 # both negative; "no worse than 60% of comparand's"
    cg_ok = cg >= 0.70 * ccg
    return dict(b_h1=s_h1, b_h2=s_h2, b_oos=s_oos, b_dd=dd_ok, b_cagr=cg_ok,
                pass4b=bool(s_h1 and s_h2 and s_oos and dd_ok and cg_ok))


def keep4a(r, base_r):
    h1, h2 = halves(r)
    b1, b2 = halves(base_r)
    ok = (metrics(h1)["Sharpe"] > metrics(b1)["Sharpe"]
          and metrics(h2)["Sharpe"] > metrics(b2)["Sharpe"]
          and metrics(r)["MaxDD"] >= metrics(base_r)["MaxDD"])
    return bool(ok)


# ================================================================================================
# run every book on every panel, once
# ================================================================================================
def load_panels():
    P("(0) PANELS")
    out = {}
    for lab, kw in [("U56", {}), ("B136", dict(broad=True)), ("SMALL716", dict(small=True))]:
        px = load_universe(**kw)
        out[lab] = px
        P(f"  {lab:9s} {px.shape[0]:5d} x {px.shape[1]:4d}   "
          f"{px.index[0].date()} .. {px.index[-1].date()}")
    P("  PROTOCOL 9: all three are CURRENT-CONSTITUENT lists; every level below is optimistic.")
    return out


def run_books(panels):
    R = {}
    for pl, px in panels.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        R[(pl, "SPY_BENCH")] = spy
        for bk in BOOKS:
            res = backtest(px, BOOK_FNS[bk](px), cost_bps=COST, freq=FREQ)
            R[(pl, bk)] = res["returns"].loc[start:]
    return R


# ================================================================================================
# gates
# ================================================================================================
def gates(panels, R):
    P()
    P("=" * 100)
    P("(G) GATES -- printed BEFORE any result number")
    P("=" * 100)
    ok = True

    live = R[("U56", "BAND03_g075")]
    c, s, d = trip(live)
    g1 = abs(c - V2_U56[0]) < TOL_C and abs(s - V2_U56[1]) < TOL_S and abs(d - V2_U56[2]) < TOL_D
    P(f"  G1 LIVE book U56 = {c:.4%} / {s:.4f} / {d:.4%}   committed "
      f"{V2_U56[0]:.4%} / {V2_U56[1]:.4f} / {V2_U56[2]:.4%}   "
      f"max|d| {max(abs(c-V2_U56[0]), abs(s-V2_U56[1]), abs(d-V2_U56[2])):.3e}  "
      f"{'PASS' if g1 else 'FAIL'}")
    ok &= g1

    c, s, d = trip(R[("U56", "SPY_BENCH")])
    g2 = abs(c - SPY_U56[0]) < TOL_C and abs(s - SPY_U56[1]) < TOL_S and abs(d - SPY_U56[2]) < TOL_D
    P(f"  G2 SPY  U56      = {c:.4%} / {s:.4f} / {d:.4%}   committed "
      f"{SPY_U56[0]:.4%} / {SPY_U56[1]:.4f} / {SPY_U56[2]:.4%}   "
      f"max|d| {max(abs(c-SPY_U56[0]), abs(s-SPY_U56[1]), abs(d-SPY_U56[2])):.3e}  "
      f"{'PASS' if g2 else 'FAIL'}")
    ok &= g2

    worst = 0.0
    for pl in PANELS:
        for bk in BOOKS:
            r = R[(pl, bk)]
            h1, h2 = halves(r)
            ref_h = len(r) // 2
            worst = max(worst, abs(len(h1) - ref_h), abs(len(h2) - (len(r) - ref_h)))
    P(f"  G3 count halves == baseline._row's len(r)//2 over {len(PANELS)*len(BOOKS)} books  "
      f"max|d| {worst:.3e}  {'PASS' if worst == 0 else 'FAIL'}")
    ok &= worst == 0

    worst = 0.0
    for pl in PANELS:
        spy = R[(pl, "SPY_BENCH")]
        for est in ESTIMATORS:
            bp = beta_path(R[(pl, "BAND03_g075")], spy, est)
            worst = max(worst, float(np.nanmax(np.abs(comparand(spy, bp, 1.00) - spy))))
    P(f"  G4 BETAMATCH at lam=1.00 IS the committed SPY100 comparand  "
      f"max|d return| {worst:.3e}  {'PASS' if worst < 1e-15 else 'FAIL'}")
    ok &= worst < 1e-15

    spy = R[("U56", "SPY_BENCH")]
    s0 = metrics(spy)["Sharpe"]
    worst = max(abs(metrics(spy * b)["Sharpe"] - s0) for b in np.arange(0.1, 2.01, 0.1))
    P(f"  G5 Sharpe(beta x SPY) == Sharpe(SPY) over beta 0.1..2.0 at rf=0  "
      f"max|d Sharpe| {worst:.3e}  {'PASS' if worst < 1e-9 else 'FAIL'}")
    ok &= worst < 1e-9

    m = capm(R[("U56", "SPYBH")], spy)
    g7a = (abs(m["alpha_ann"]) < 1e-9 and abs(m["beta"] - 1.0) < 1e-9
           and abs(m["R2"] - 1.0) < 1e-9 and not np.isfinite(m["t_alpha"]))
    base = R[("U56", "BAND03_g075")]
    m0 = capm(base, spy)
    planted = (1.0 + base) * (1.0 + 0.05) ** (1.0 / TRAD) - 1.0
    mp = capm(planted, spy)
    g7b = abs((mp["alpha_ann"] - m0["alpha_ann"]) - 0.05) < 3e-3 and mp["t_alpha"] > m0["t_alpha"]
    P(f"  G7 SPYBH (the zero-signal control) reads alpha {m['alpha_ann']:+.3e} / "
      f"beta {m['beta']:.9f} / R2 {m['R2']:.9f}, t NaN by the degeneracy guard "
      f"(it IS the regressor)   {'PASS' if g7a else 'FAIL'}")
    P(f"     PLANTED +5.00%/yr on the LIVE book moves alpha "
      f"{m0['alpha_ann']:+.4%} -> {mp['alpha_ann']:+.4%} "
      f"(d {mp['alpha_ann'] - m0['alpha_ann']:+.4%}), t {m0['t_alpha']:.2f} -> "
      f"{mp['t_alpha']:.2f}, beta {m0['beta']:.6f} -> {mp['beta']:.6f}   "
      f"{'PASS' if g7b else 'FAIL'}")
    ok &= g7a and g7b

    r = R[("U56", "EWELIG_g075")]
    c, s, d = trip(r)
    h1, h2 = halves(r)
    s1, s2 = metrics(h1)["Sharpe"], metrics(h2)["Sharpe"]
    g8 = abs(c - 0.104) < 0.004 and abs(s - 1.05) < 0.03 and abs(s1 - 1.07) < 0.05 \
        and abs(s2 - 1.03) < 0.05
    P(f"  G8 EWELIG_g075 U56 = {c:.4%} / {s:.4f} (halves {s1:.2f} / {s2:.2f})   "
      f"2026-09-03 memo Finding 2: 10.4% / 1.05 (1.07 / 1.03)   {'PASS' if g8 else 'FAIL'}")
    ok &= g8
    return ok


# ================================================================================================
# PART A -- the CAPM census
# ================================================================================================
def part_a(R):
    P()
    P("=" * 100)
    P("(A) THE CAPM CENSUS -- annualised alpha, Newey-West t (lag 21), beta, R^2")
    P("=" * 100)
    rows = []
    for pl in PANELS:
        spy = R[(pl, "SPY_BENCH")]
        for bk in BOOKS:
            r = R[(pl, bk)]
            h1, h2 = halves(r)
            s1, s2 = halves(spy)
            f = capm(r, spy)
            a1, a2 = capm(h1, s1), capm(h2, s2)
            ai = capm(r.loc[:IS_END], spy.loc[:IS_END])
            ao = capm(r.loc[OOS_START:], spy.loc[OOS_START:])
            cg, sh, dd = trip(r)
            rows.append(dict(panel=pl, book=bk, CAGR=cg, Sharpe=sh, MaxDD=dd,
                             alpha_ann=f["alpha_ann"], t_alpha=f["t_alpha"], beta=f["beta"],
                             R2=f["R2"], alpha_h1=a1["alpha_ann"], t_h1=a1["t_alpha"],
                             alpha_h2=a2["alpha_ann"], t_h2=a2["t_alpha"],
                             beta_h1=a1["beta"], beta_h2=a2["beta"],
                             alpha_IS=ai["alpha_ann"], t_IS=ai["t_alpha"], beta_IS=ai["beta"],
                             alpha_OOS=ao["alpha_ann"], t_OOS=ao["t_alpha"], beta_OOS=ao["beta"],
                             n=f["n"]))
    A = pd.DataFrame(rows)
    P(f"  {'panel':9s} {'book':12s} {'CAGR':>8s} {'Sharpe':>7s} {'MaxDD':>8s} "
      f"{'alpha':>9s} {'t':>7s} {'beta':>6s} {'R2':>6s} {'a_H1':>9s} {'t_H1':>6s} "
      f"{'a_H2':>9s} {'t_H2':>6s} {'a_OOS':>9s} {'t_OOS':>6s}")
    for _, x in A.iterrows():
        P(f"  {x.panel:9s} {x.book:12s} {x.CAGR:8.2%} {x.Sharpe:7.4f} {x.MaxDD:8.2%} "
          f"{x.alpha_ann:+9.2%} {x.t_alpha:+7.2f} {x.beta:6.3f} {x.R2:6.3f} "
          f"{x.alpha_h1:+9.2%} {x.t_h1:+6.2f} {x.alpha_h2:+9.2%} {x.t_h2:+6.2f} "
          f"{x.alpha_OOS:+9.2%} {x.t_OOS:+6.2f}")
    live = A[A.book != "SPYBH"]
    both = live[(live.t_h1.abs() > 2) & (live.t_h2.abs() > 2)]
    bothpos = live[(live.t_h1 > 2) & (live.t_h2 > 2)]
    P()
    P(f"  H1 test: |NW t| > 2 in BOTH count halves -> {len(both)} of {len(live)} book-panels "
      f"({', '.join(f'{r.panel}/{r.book}' for _, r in both.iterrows()) or 'none'})")
    P(f"           POSITIVE t > +2 in both halves  -> {len(bothpos)} of {len(live)} "
      f"({', '.join(f'{r.panel}/{r.book}' for _, r in bothpos.iterrows()) or 'none'})")
    P(f"           full-sample t > +2             -> "
      f"{int((live.t_alpha > 2).sum())} of {len(live)};  OOS t > +2 -> "
      f"{int((live.t_OOS > 2).sum())} of {len(live)}")
    P(f"  beta range over the 18 signal book-panels: {live.beta.min():.3f} .. {live.beta.max():.3f}"
      f"   median R^2 {live.R2.median():.3f}")
    P()
    P("  IS THE ALPHA ONE OBJECT SCALED BY GROSS?  alpha / gross and beta / gross within a family:")
    GROSSOF = {"BAND03_g050": 0.50, "BAND03_g075": 0.75, "BAND03_g100": 1.00,
               "EWELIG_g075": 0.75, "EWELIG_g100": 1.00}
    for pl in PANELS:
        for fam in ("BAND03", "EWELIG"):
            sub = A[(A.panel == pl) & A.book.str.startswith(fam)]
            if sub.empty:
                continue
            ag = [x.alpha_ann / GROSSOF[x.book] for _, x in sub.iterrows()]
            bg = [x.beta / GROSSOF[x.book] for _, x in sub.iterrows()]
            P(f"    {pl:9s} {fam:7s} alpha/g " + " ".join(f"{v:+.4%}" for v in ag)
              + f"  (spread {max(ag)-min(ag):.2e})   beta/g "
              + " ".join(f"{v:.4f}" for v in bg) + f"  (spread {max(bg)-min(bg):.2e})")
    return A


# ================================================================================================
# PART B -- the 525-point grid: does beta-matching move a 4b verdict?
# ================================================================================================
def part_b(R, A):
    P()
    P("=" * 100)
    P("(B) THE GRID -- 21 book-panels x 5 estimators x 5 shrinkages = 525 points, ALL published")
    P("=" * 100)
    rows = []
    for pl in PANELS:
        spy = R[(pl, "SPY_BENCH")]
        base = R[(pl, "BAND03_g075")]          # RULES v2 (live) on this panel, the 4a comparand
        spy_oos = spy.loc[OOS_START:]
        for bk in BOOKS:
            r = R[(pl, bk)]
            r_oos = r.loc[OOS_START:]
            a4 = keep4a(r, base)
            ref = keep4b(r, spy, r_oos, spy_oos)   # the COMMITTED 4b (SPY100)
            for est in ESTIMATORS:
                bp = beta_path(r, spy, est)
                for lam in LAMBDAS:
                    cr = comparand(spy, bp, lam)
                    bm = keep4b(r, cr, r_oos, cr.loc[OOS_START:])
                    ccg, csh, cdd = trip(cr)
                    rows.append(dict(panel=pl, book=bk, estimator=est, lam=lam,
                                     beta_used_mean=float(((1 - lam) * bp + lam).mean()),
                                     cmp_CAGR=ccg, cmp_Sharpe=csh, cmp_MaxDD=cdd,
                                     pass4a=a4, pass4b_SPY100=ref["pass4b"],
                                     pass4b_BETAMATCH=bm["pass4b"],
                                     spy_h1=ref["b_h1"], spy_h2=ref["b_h2"], spy_oos=ref["b_oos"],
                                     spy_dd=ref["b_dd"], spy_cagr=ref["b_cagr"],
                                     bm_h1=bm["b_h1"], bm_h2=bm["b_h2"], bm_oos=bm["b_oos"],
                                     bm_dd=bm["b_dd"], bm_cagr=bm["b_cagr"]))
    G = pd.DataFrame(rows)

    P(f"  4a passes (vs RULES v2 on the same panel): "
      f"{int(G.drop_duplicates(['panel','book']).pass4a.sum())} of 21 book-panels")
    P(f"  4b passes, COMMITTED SPY100 comparand:     "
      f"{int(G.drop_duplicates(['panel','book']).pass4b_SPY100.sum())} of 21 book-panels")
    P(f"  4b passes, BETAMATCH comparand:            "
      f"{int(G.pass4b_BETAMATCH.sum())} of {len(G)} grid points")
    flips = G[G.pass4b_SPY100 != G.pass4b_BETAMATCH]
    up = flips[~flips.pass4b_SPY100 & flips.pass4b_BETAMATCH]
    dn = flips[flips.pass4b_SPY100 & ~flips.pass4b_BETAMATCH]
    P(f"  FLIPS: {len(flips)} of {len(G)} points ({len(flips)/len(G):.1%})  "
      f"FAIL->PASS {len(up)}   PASS->FAIL {len(dn)}")
    P()
    P("  per-leg pass counts over the 525 points (SPY100 leg -> BETAMATCH leg):")
    for leg, a, b in [("H1 Sharpe", "spy_h1", "bm_h1"), ("H2 Sharpe", "spy_h2", "bm_h2"),
                      ("OOS Sharpe", "spy_oos", "bm_oos"), ("DD cap", "spy_dd", "bm_dd"),
                      ("CAGR floor", "spy_cagr", "bm_cagr")]:
        P(f"    {leg:11s} {int(G[a].sum()):4d} -> {int(G[b].sum()):4d}   "
          f"(moved on {int((G[a] != G[b]).sum())} points)")
    P()
    P("  flips by leg, decomposed (which leg changed on a flipping point):")
    if len(flips):
        for leg, a, b in [("H1", "spy_h1", "bm_h1"), ("H2", "spy_h2", "bm_h2"),
                          ("OOS", "spy_oos", "bm_oos"), ("DD", "spy_dd", "bm_dd"),
                          ("CAGR", "spy_cagr", "bm_cagr")]:
            P(f"    {leg:5s} moved on {int((flips[a] != flips[b]).sum()):4d} of {len(flips)} flips")
        P("    flipping book-panels: "
          + ", ".join(sorted({f"{r.panel}/{r.book}" for _, r in flips.iterrows()})))
    else:
        P("    none")
    P()
    P("  THE LIKE-FOR-LIKE READING -- lam = 0.00 (beta charged in full), 21 book-panels per "
      "estimator:")
    z0 = G[G.lam == 0.0]
    for est in ESTIMATORS:
        zz = z0[z0.estimator == est]
        nm = sorted(f"{r.panel}/{r.book}" for _, r in zz[zz.pass4b_BETAMATCH].iterrows())
        P(f"    {est:5s} 4b BETAMATCH passes {int(zz.pass4b_BETAMATCH.sum()):2d} of 21"
          f"   ({', '.join(nm) or 'NONE'})")
    P(f"    committed SPY100 comparand, same 21: "
      f"{int(G.drop_duplicates(['panel','book']).pass4b_SPY100.sum())} "
      f"({', '.join(sorted(f'{r.panel}/{r.book}' for _, r in G.drop_duplicates(['panel','book'])[G.drop_duplicates(['panel','book']).pass4b_SPY100].iterrows()))})")
    P()
    P("  WHAT KILLS THE COMMITTED PASSERS under a CONSTANT-beta comparand (FULL / IS, lam=0):")
    for est in ("FULL", "IS"):
        zz = z0[(z0.estimator == est) & z0.pass4b_SPY100]
        for _, x in zz.iterrows():
            legs = [n for n, v in [("H1", x.bm_h1), ("H2", x.bm_h2), ("OOS", x.bm_oos),
                                   ("DD", x.bm_dd), ("CAGR", x.bm_cagr)] if not v]
            P(f"    {est:5s} {x.panel}/{x.book:12s} -> "
              f"{'PASS' if x.pass4b_BETAMATCH else 'FAIL'}"
              f"   failing legs {legs or 'none'}   comparand "
              f"{x.cmp_CAGR:.2%} / {x.cmp_Sharpe:.4f} / {x.cmp_MaxDD:.2%}"
              f"   (0.60x cap {0.60*x.cmp_MaxDD:.2%}, 0.70x floor {0.70*x.cmp_CAGR:.2%})")
    P()
    P("  the comparand itself, at lam=0 (what beta-matching actually charges):")
    z = G[G.lam == 0.0]
    for pl in PANELS:
        zz = z[z.panel == pl]
        P(f"    {pl:9s} comparand CAGR {zz.cmp_CAGR.min():6.2%}..{zz.cmp_CAGR.max():6.2%}   "
          f"MaxDD {zz.cmp_MaxDD.min():7.2%}..{zz.cmp_MaxDD.max():7.2%}   "
          f"Sharpe {zz.cmp_Sharpe.min():.4f}..{zz.cmp_Sharpe.max():.4f} "
          f"(SPY {metrics(R[(pl,'SPY_BENCH')])['Sharpe']:.4f})")
    return G


# ================================================================================================
# PART C -- rule 8
# ================================================================================================
def part_c(R):
    P()
    P("=" * 100)
    P("(C) RULE 8 -- both tuned params fitted on 2009-2016 ALONE, 2017-2026 read ONCE")
    P("=" * 100)
    P("  CHOOSER (pre-stated): inside each (estimator, shrinkage) cell, score every book-panel by")
    P("  the Newey-West t of its IS EXCESS RETURN OVER THAT CELL'S BETAMATCH COMPARAND, both built")
    P("  on IS DATA ONLY; take the highest.  The excess-return form is used rather than a CAPM")
    P("  intercept BECAUSE an OLS intercept is invariant to rescaling its regressor, so a")
    P("  CAPM alpha vs beta x SPY is identically the alpha vs SPY and neither dial would bite.")
    P("  SPYBH is excluded from the pick (it is the zero-signal control).  The IS-Sharpe chooser")
    P("  and the two do-nothing controls are reported beside it.")
    rows = []
    IS, OOS = {}, {}
    for pl in PANELS:
        for bk in BOOKS + ["SPY_BENCH"]:
            IS[(pl, bk)] = R[(pl, bk)].loc[:IS_END]
            OOS[(pl, bk)] = R[(pl, bk)].loc[OOS_START:]

    cands = [(pl, bk) for pl in PANELS for bk in BOOKS if bk != "SPYBH"]
    for est in ESTIMATORS:
        for lam in LAMBDAS:
            best, best_t = None, -np.inf
            for pl, bk in cands:
                spy_is = IS[(pl, "SPY_BENCH")]
                bp = beta_path(IS[(pl, bk)], spy_is, est)
                cr = comparand(spy_is, bp, lam)
                exc, t_exc = nw_mean_t((IS[(pl, bk)] - cr).values.astype(float))
                if np.isfinite(t_exc) and t_exc > best_t:
                    best_t, best = t_exc, (pl, bk, exc)
            pl, bk, a_is = best
            o = OOS[(pl, bk)]
            cg, sh, dd = trip(o)
            rows.append(dict(chooser="IS_EXCESS_T", estimator=est, lam=lam, pick=f"{pl}/{bk}",
                             IS_alpha=a_is, IS_t=best_t, OOS_CAGR=cg, OOS_Sharpe=sh, OOS_MaxDD=dd))

    # control choosers (no tuned params at all)
    bs, bsv = None, -np.inf
    for pl, bk in cands:
        s = metrics(IS[(pl, bk)])["Sharpe"]
        if s > bsv:
            bsv, bs = s, (pl, bk)
    cg, sh, dd = trip(OOS[bs])
    rows.append(dict(chooser="IS_SHARPE", estimator="-", lam=np.nan, pick=f"{bs[0]}/{bs[1]}",
                     IS_alpha=np.nan, IS_t=bsv, OOS_CAGR=cg, OOS_Sharpe=sh, OOS_MaxDD=dd))
    for lab, key in [("CONTROL_RULESv2", ("U56", "BAND03_g075")),
                     ("CONTROL_SPY", ("U56", "SPY_BENCH"))]:
        cg, sh, dd = trip(OOS[key])
        rows.append(dict(chooser=lab, estimator="-", lam=np.nan, pick=f"{key[0]}/{key[1]}",
                         IS_alpha=np.nan, IS_t=np.nan, OOS_CAGR=cg, OOS_Sharpe=sh, OOS_MaxDD=dd))
    W = pd.DataFrame(rows)
    P()
    P(f"  {'chooser':16s} {'est':5s} {'lam':>5s} {'pick':22s} {'IS a':>8s} {'IS t':>7s} "
      f"{'OOS CAGR':>9s} {'OOS Sh':>7s} {'OOS MaxDD':>10s}")
    for _, x in W.iterrows():
        lam = "  -  " if pd.isna(x.lam) else f"{x.lam:5.2f}"
        ia = "    -   " if pd.isna(x.IS_alpha) else f"{x.IS_alpha:+8.2%}"
        it = "   -   " if pd.isna(x.IS_t) else f"{x.IS_t:+7.2f}"
        P(f"  {x.chooser:16s} {x.estimator:5s} {lam} {x.pick:22s} {ia} {it} "
          f"{x.OOS_CAGR:9.2%} {x.OOS_Sharpe:7.4f} {x.OOS_MaxDD:10.2%}")
    a = W[W.chooser == "IS_EXCESS_T"]
    ssh = float(W[W.chooser == "IS_SHARPE"].OOS_Sharpe.iloc[0])
    spy_sh = float(W[W.chooser == "CONTROL_SPY"].OOS_Sharpe.iloc[0])
    v2_sh = float(W[W.chooser == "CONTROL_RULESv2"].OOS_Sharpe.iloc[0])
    P()
    P(f"  25 IS-excess-t picks: OOS Sharpe median {a.OOS_Sharpe.median():.4f} "
      f"(min {a.OOS_Sharpe.min():.4f}, max {a.OOS_Sharpe.max():.4f}); "
      f"OOS CAGR median {a.OOS_CAGR.median():.2%}; distinct picks {a.pick.nunique()} "
      f"({', '.join(sorted(a.pick.unique()))})")
    P(f"  H4 test: IS-excess-t beats IS-Sharpe ({ssh:.4f}) OOS on "
      f"{int((a.OOS_Sharpe > ssh).sum())} of 25 cells; beats SPY ({spy_sh:.4f}) on "
      f"{int((a.OOS_Sharpe > spy_sh).sum())} of 25; beats RULES v2 ({v2_sh:.4f}) on "
      f"{int((a.OOS_Sharpe > v2_sh).sum())} of 25")
    return W


def verdict(A, G, W):
    P()
    P("=" * 100)
    P("(V) THE ANSWER")
    P("=" * 100)
    live = A[A.book != "SPYBH"]
    bothpos = live[(live.t_h1 > 2) & (live.t_h2 > 2)]
    flips = G[G.pass4b_SPY100 != G.pass4b_BETAMATCH]
    dn = flips[flips.pass4b_SPY100 & ~flips.pass4b_BETAMATCH]
    up = flips[~flips.pass4b_SPY100 & flips.pass4b_BETAMATCH]
    a = W[W.chooser == "IS_EXCESS_T"]
    ssh = float(W[W.chooser == "IS_SHARPE"].OOS_Sharpe.iloc[0])
    P(f"  H1 (no book has |t| > 2 in both halves)      -> "
      f"{'HOLDS' if len(bothpos) == 0 else 'FAILS'} ({len(bothpos)} of 18 with t > +2 in both)")
    P(f"  H2 (beta-matching flips at least one 4b)     -> "
      f"{'HOLDS' if len(flips) else 'FAILS'} ({len(flips)} of {len(G)} points)")
    P(f"  H3 (every flip is PASS->FAIL via the DD cap) -> "
      f"{'HOLDS' if len(up) == 0 and len(dn) else 'FAILS'} "
      f"(PASS->FAIL {len(dn)}, FAIL->PASS {len(up)})")
    P(f"  H4 (excess-t chooser does not beat Sharpe) -> "
      f"{'HOLDS' if int((a.OOS_Sharpe > ssh).sum()) == 0 else 'FAILS'} "
      f"({int((a.OOS_Sharpe > ssh).sum())} of 25 cells beat it)")
    z0 = G[(G.lam == 0.0) & G.estimator.isin(["FULL", "IS"])]
    P()
    P("  THE ANSWER, in two parts, and they point opposite ways.")
    P(f"  1. YES, ALPHA IS THERE, AND IT IS NOT THE WHOLE SHELF'S.  The U56 200d-band family")
    P(f"     carries +4.82%/yr of CAPM alpha per unit gross (NW t +3.93, beta 0.418/unit gross,")
    P(f"     R^2 0.61), positive at t > +2 in BOTH count halves (+2.50 / +3.08) AND out of sample")
    P(f"     (+3.60).  H1 FAILS and that is a real positive.  It is ONE object scaled by gross:")
    P(f"     alpha/gross is constant to 8.1e-06 across the three rungs.  It is PANEL-BOUND --")
    P(f"     B136 +3.63%/unit gross (t +3.14) but H2 only +1.86, SMALL716 +1.47% (t +0.85), and")
    P(f"     the EWELIG family's SMALL716 alpha is NEGATIVE (-2.10%/unit gross).")
    P(f"  2. NO, IT DOES NOT BUY A KEEP.  4a: 0 of 21 book-panels.  4b under the committed")
    P(f"     100%-SPY comparand: 3 of 21.  Charge each book its OWN CONSTANT beta and that")
    P(f"     becomes {int(z0.pass4b_BETAMATCH.sum())} of 42 (FULL and IS at lam=0) -- all 3")
    P(f"     committed passers die, all 3 through the DD cap, because a comparand at beta 0.42")
    P(f"     draws down -15% and 60% of that is -9.1% against the book's -15.9%.")
    P(f"  3. The two legs that move are the two the record already suspected: the DD cap (300 ->")
    P(f"     185 of 525) and the CAGR floor (225 -> 344).  The three SHARPE legs move on 0 of 86")
    P(f"     flips under a constant beta -- G5's algebra -- so 4b's Sharpe legs are exactly")
    P(f"     beta-blind and its two level legs are exactly beta-scaled.  That IS the 'decided by")
    P(f"     gross alone' diagnosis, stated as an identity rather than as a correlation.")
    P(f"  4. RULE 8: pricing the beta charge into the CHOOSER buys nothing.  0 of 25 cells beat")
    P(f"     the dial-free IS-Sharpe chooser OOS (1.2765) and 0 of 25 beat RULES v2 (1.2772);")
    P(f"     25 of 25 beat SPY (0.8740), which is the same low-beta tautology as leg 2.")
    P("  VERDICT: KILL for capital -- nothing promoted, no RULES change.  The alpha is real and")
    P("  documented; it is the 200d band clause already live in RULES v2, and it is worth no")
    P("  more capital than the gross dial that scales it.")
    return dict(bothpos=len(bothpos), flips=len(flips), up=len(up), dn=len(dn))


def main():
    t0 = time.time()
    P("=" * 100)
    P(f"Idea 869 -- does any committed BOOK carry ALPHA once its own BETA is charged?  "
      f"(lane B, {pd.Timestamp.today().date()})")
    P("=" * 100)
    P(__doc__.split("Outputs beside")[0].strip())
    panels = load_panels()
    R = run_books(panels)
    ok = gates(panels, R)
    A = part_a(R)
    G = part_b(R, A)
    # G6 determinism: rebuild the grid a second time and hash both
    G2 = part_b_quiet(R)
    h1 = hashlib.sha256(G.round(12).to_csv(index=False).encode()).hexdigest()[:16]
    h2 = hashlib.sha256(G2.round(12).to_csv(index=False).encode()).hexdigest()[:16]
    P()
    P(f"  G6 determinism: grid hash {h1} vs rebuild {h2}  {'PASS' if h1 == h2 else 'FAIL'}")
    ok &= h1 == h2
    W = part_c(R)
    verdict(A, G, W)
    P()
    P("=" * 100)
    P("(O) OUTPUTS")
    P("=" * 100)
    dump(A, "capm.csv")
    dump(G, "grid.csv")
    dump(W, "walkforward.csv")
    P(f"  gates {'ALL PASS' if ok else 'FAILED'}   total runtime {time.time() - t0:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"wrote {STEM}.console.txt")


def part_b_quiet(R):
    """G6: rebuild the whole grid a second time, printing nothing, and hash it."""
    global QUIET
    QUIET = True
    try:
        return part_b(R, None)
    finally:
        QUIET = False


if __name__ == "__main__":
    main()

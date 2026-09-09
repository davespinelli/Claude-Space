#!/usr/bin/env python3
"""Idea 533 — why is `evol` the one characteristic that never reverses?

Question (QUEUE 533): idea 295 found breadth, disp and corr all take idea 284's within-stratum
flip at strata >= 7, but `evol` (the eligible set's mean 20d realised vol) keeps its pooled sign
at every grid point, with evol-vs-MaxDD within-stratum t between -8.7 and -6.0.  Test whether
eligible-set vol is carrying a genuine within-panel effect or is simply the characteristic most
collinear with THE BOOK'S OWN realised vol, by residualising it on the book's vol before the
within-stratum fit.

Construction (idea 295's ladder rebuilt verbatim, one column added):
  * the same MIX ladder — k=40 names, a share q from the sub-$2B panel and 1-q from the
    large-cap STOCK pool, 21 q rungs x 8 draws = 168 panels, seed 20260909, one common window;
  * the same three books per panel (EWall control, top10, top20) at gross 0.75, weekly,
    10 bps, next-day execution;
  * the same four characteristics with idea 284's definitions;
  * ADDED: each book's OWN annualised realised vol (`engine.metrics()["Vol"]`) in each window.
    That is the regressor the queue asks for.  It is a property of the BOOK, not of the panel.

The measurement is a 4 x 4 grid and every point is reported:
    resid   in {none, partial, residx, ratio}     tuned param 1 — how the book's vol is removed
    strata  in {3, 5, 7, 21}                      tuned param 2 — stratum resolution (idea 295's)

    none    y ~ x                       within-stratum demeaned (idea 295's published fit)
    partial y ~ x + bookvol             within-stratum demeaned; x's coefficient and its t
    residx  y ~ (x residualised on bookvol)       the queue's literal wording.  By Frisch-Waugh
            the SLOPE equals `partial`'s; the t does not, because y keeps the bookvol variance.
            Both are printed so the difference is visible rather than asserted.
    ratio   y ~ x / bookvol             the scale-free restatement

WHAT A ZERO PARTIAL WOULD AND WOULD NOT MEAN.  The book's realised vol is downstream of the
panel: a higher-vol eligible set mechanically makes a higher-vol book.  Conditioning on it is
therefore a MEDIATOR control, not a confounder control.  If evol's within-stratum effect
survives `none` and dies under `partial`, the honest reading is "the effect runs THROUGH the
book's own vol", i.e. the characteristic is a restatement of an exposure the book already
reports — NOT "the effect is spurious".  Both readings are stated in the verdict; the run does
not claim to separate them beyond what the two extra tests below can do:
  (i) the same residualisation applied to breadth / disp / corr — if only evol dies, evol is the
      vol channel and the others are not;
  (ii) VOL-NORMALISED OUTCOMES (Sharpe is already mean/vol; DDnorm = MaxDD/bookvol,
      CAGRnorm = CAGR/bookvol).  If evol has no within-stratum content in DDnorm, then its
      surviving MaxDD slope is the vol channel and nothing else.

Two reproduction gates, both against committed artefacts:
  G1  the 504 arm-rows must reproduce idea 295's committed `.arms.csv` (same seed, same code
      path) — max |delta| over every shared numeric column.
  G2  the 432 pooled/within slopes must reproduce idea 295's committed `.slopes.csv`, and the
      queue's own premise ("evol keeps its pooled sign at every one of 16 grid points") is
      re-derived from those numbers rather than believed.

Rule 8 (PROTOCOL 8): every slope and every verdict is re-estimated on the FIRST HALF only
(<= 2016-12-31), the verdict fixed there, and the second half (2017-01-01 .. end) read ONCE.
Both KEEP paths (4a vs the live RULES v2 book, 4b vs SPY) are evaluated on every arm-row, and
the books' OOS CAGR / Sharpe / MaxDD are reported against the live baseline and against SPY.

Costs 10 bps, weekly, weights decided at t applied at t+1 (engine).  No network.
SURVIVORSHIP: both ends of the q ladder are CURRENT constituents of their screens, so every
mixed panel inherits that bias and the LEVEL of every number here is optimistic.  The object
under test is a within-stratum SLOPE and its behaviour under a control; no level comparison
across q is claimed as tradable.

Deterministic (seed 20260909), standalone.  `--reuse` re-reads this run's own arm-rows.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = Path(__file__).with_suffix("")
BT = ROOT / "research" / "backtests"
ARMS_295 = BT / "2026-09-09_restate-the-26-characteristic-files-under-the-SIGN-FLIP_cloud.arms.csv"
SLOPES_295 = BT / "2026-09-09_restate-the-26-characteristic-files-under-the-SIGN-FLIP_cloud.slopes.csv"

COST, FREQ = 10, "W"
K_MIX, N_DRAWS = 40, 8
QS = [round(x / 20, 2) for x in range(21)]
NS = [10, 20]
GROSS = 0.75
WARMUP = 260
IS_END = pd.Timestamp("2016-12-31")
SEED = 20260909
CHARS = ["breadth", "disp", "corr", "evol"]
OUTCOMES = ["Sharpe", "CAGR", "MaxDD"]
NORM_OUTCOMES = ["DDnorm", "CAGRnorm"]
RESIDS = ["none", "partial", "residx", "ratio"]      # tuned param 1
STRATA = [3, 5, 7, 21]                               # tuned param 2
T_BAR = 1.960                                        # idea 295's central bar, NOT tuned here
REUSE = "--reuse" in sys.argv

OUT = []
t0 = time.time()
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 500)


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUT.append(s)


say(__doc__.strip().split("\n\n")[0])
say(f"run started {pd.Timestamp.utcnow():%Y-%m-%d %H:%M} UTC")

# ============================================================== A. the ladder (idea 295 rebuilt)
say(f"\n[A] THE LADDER — idea 295's MIX rebuilt verbatim: k={K_MIX}, {len(QS)} q rungs x "
    f"{N_DRAWS} draws = {len(QS)*N_DRAWS} panels, seed {SEED}, plus each book's OWN realised vol.")

U = json.loads((ROOT / "research" / "universe.json").read_text())
ETFS = set(U["broad"]) | set(U["sectors"]) | set(U["bonds_fx_commod"])
pxb = load_universe(broad=True)
pxs = load_universe(small=True)
meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
BAD = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
S_STK = [c for c in pxs.columns if c != "SPY" and c not in BAD]
B_STK = [c for c in pxb.columns if c != "SPY" and c not in ETFS]
SPY_RAW = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)["SPY"]
COMMON = pxs.index
say(f"  small panel: {len(BAD)} tickers with max_1d_move >= 1.0 dropped first, {len(S_STK)} usable; "
    f"large-cap STOCK pool {len(B_STK)} (ETFs excluded)")
say(f"  common window {COMMON[0].date()} .. {COMMON[-1].date()} ({len(COMMON)} rows); "
    f"books top-n for n in {NS} + EWall control, gross {GROSS}; RULES v2 is the 4a comparand")
say(f"  costs {COST} bps, {FREQ}, next-day execution, {WARMUP}-day warm-up skip; "
    f"rule 8 IS <= {IS_END.date()}, OOS {IS_END.date()}+1 .. end")
say("  SURVIVORSHIP: both ends of the q ladder are CURRENT-constituent sets; levels are optimistic, "
    "the WITHIN-stratum slope and its behaviour under the control are what is claimed.")


def mk(cols_s, cols_l):
    parts = []
    if cols_s:
        parts.append(pxs[cols_s])
    if cols_l:
        parts.append(pxb[cols_l].reindex(COMMON, method="ffill"))
    px = pd.concat(parts, axis=1).reindex(COMMON).dropna(how="all").ffill()
    return px.join(SPY_RAW.reindex(px.index, method="ffill").rename("SPY"))


def panel_chars(px, cols, elig, lo, hi):
    """idea 284's four characteristics, verbatim definitions, over a date window."""
    m = rebalance_mask(px.index, FREQ)
    idx = px.loc[px.index[WARMUP]:].index
    if lo is not None:
        idx = idx[idx >= lo]
    if hi is not None:
        idx = idx[idx <= hi]
    rb = idx[m.reindex(idx).fillna(False).values]
    e = elig.loc[rb, cols]
    k = len(cols)
    nel = e.sum(axis=1)
    r63 = (px[cols] / px[cols].shift(63) - 1).loc[rb]
    vol20 = (px[cols].pct_change().rolling(20).std() * np.sqrt(252)).loc[rb]
    dr = px[cols].pct_change().loc[idx]
    C = dr.corr().to_numpy()
    iu = np.triu_indices(k, 1)
    return dict(breadth=float((nel / k).mean()),
                disp=float(r63.where(e).std(axis=1, ddof=0).mean()),
                evol=float(vol20.where(e).mean(axis=1).mean()),
                corr=float(np.nanmean(C[iu])) if k > 1 else np.nan)


rng = np.random.default_rng(SEED)
panels = []
for q in QS:
    ns_ = int(round(q * K_MIX)); nl_ = K_MIX - ns_
    for d in range(N_DRAWS):
        sc = list(rng.choice(S_STK, size=ns_, replace=False)) if ns_ else []
        lc = list(rng.choice(B_STK, size=nl_, replace=False)) if nl_ else []
        panels.append((q, d, sc, lc))

arm_rows = []
for i, (q, d, sc, lc) in enumerate([] if REUSE else panels):
    px = mk(sc, lc)
    tr = [c for c in px.columns if c != "SPY"]
    start = px.index[WARMUP]
    oos_lo = IS_END + pd.Timedelta(days=1)
    s, above, vol20 = score(px[tr], vol_scale=False)
    el = s.where(above & (vol20 < 0.60))
    elig = el.notna()
    ch_full = panel_chars(px, tr, elig, None, None)
    ch_is = panel_chars(px, tr, elig, None, IS_END)
    ch_oos = panel_chars(px, tr, elig, oos_lo, None)

    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    ms, ms_is, ms_oos = metrics(spy), metrics(spy.loc[:IS_END]), metrics(spy.loc[oos_lo:])
    h = len(spy) // 2
    ms1, ms2 = metrics(spy.iloc[:h]), metrics(spy.iloc[h:])
    base = backtest(px, rules_v2_weights(px[tr]).reindex(columns=px.columns).fillna(0.0),
                    cost_bps=COST, freq=FREQ)["returns"].loc[start:]
    mb, mb1, mb2 = metrics(base), metrics(base.iloc[:h]), metrics(base.iloc[h:])
    mb_oos = metrics(base.loc[oos_lo:])

    rank = el.rank(axis=1, ascending=False)
    e01 = elig.astype(float)
    cnt = e01.sum(axis=1).replace(0, np.nan)
    specs = [("EWall", np.nan, (GROSS * e01.div(cnt, axis=0)).reindex(columns=px.columns).fillna(0.0))]
    for n in NS:
        specs.append((f"top{n}", n, ((rank <= n).astype(float) * (GROSS / n))
                      .reindex(columns=px.columns).fillna(0.0)))
    for arm, n, w in specs:
        r = backtest(px, w, cost_bps=COST, freq=FREQ)["returns"].loc[start:]
        m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
        m_is, m_oos = metrics(r.loc[:IS_END]), metrics(r.loc[oos_lo:])
        arm_rows.append(dict(
            q=q, draw=d, arm=arm, n=n,
            **{f"{c}_full": ch_full[c] for c in CHARS},
            **{f"{c}_IS": ch_is[c] for c in CHARS},
            **{f"{c}_OOS": ch_oos[c] for c in CHARS},
            Sharpe_full=m["Sharpe"], CAGR_full=m["CAGR"], MaxDD_full=m["MaxDD"],
            Sharpe_IS=m_is["Sharpe"], CAGR_IS=m_is["CAGR"], MaxDD_IS=m_is["MaxDD"],
            Sharpe_OOS=m_oos["Sharpe"], CAGR_OOS=m_oos["CAGR"], MaxDD_OOS=m_oos["MaxDD"],
            # ---- the added column: the BOOK's own realised vol, per window
            bookvol_full=m["Vol"], bookvol_IS=m_is["Vol"], bookvol_OOS=m_oos["Vol"],
            H1=m1["Sharpe"], H2=m2["Sharpe"],
            pass4a=bool(m1["Sharpe"] > mb1["Sharpe"] and m2["Sharpe"] > mb2["Sharpe"]
                        and m["MaxDD"] >= mb["MaxDD"]),
            pass4b=bool(m1["Sharpe"] > ms1["Sharpe"] and m2["Sharpe"] > ms2["Sharpe"]
                        and m_oos["Sharpe"] > ms_oos["Sharpe"]
                        and m["MaxDD"] >= 0.60 * ms["MaxDD"] and m["CAGR"] >= 0.70 * ms["CAGR"]),
            base_Sharpe=mb["Sharpe"], base_CAGR=mb["CAGR"], base_MaxDD=mb["MaxDD"],
            base_H1=mb1["Sharpe"], base_H2=mb2["Sharpe"],
            base_OOS_Sharpe=mb_oos["Sharpe"], base_OOS_CAGR=mb_oos["CAGR"],
            base_OOS_MaxDD=mb_oos["MaxDD"],
            SPY_Sharpe=ms["Sharpe"], SPY_CAGR=ms["CAGR"], SPY_MaxDD=ms["MaxDD"],
            SPY_H1=ms1["Sharpe"], SPY_H2=ms2["Sharpe"],
            SPY_OOS_Sharpe=ms_oos["Sharpe"], SPY_OOS_CAGR=ms_oos["CAGR"],
            SPY_OOS_MaxDD=ms_oos["MaxDD"]))
    if (i + 1) % 21 == 0:
        say(f"    {i+1}/{len(panels)} panels ({time.time()-t0:6.1f}s)")

if REUSE:
    A = pd.read_csv(f"{STEM}.arms.csv")
    say(f"  --reuse: re-read {len(A)} arm-rows from this run's own artefact (seed {SEED})")
else:
    A = pd.DataFrame(arm_rows)
    A.to_csv(f"{STEM}.arms.csv", index=False)
say(f"  {len(A)} arm-rows over {len(panels)} panels -> {Path(STEM).name}.arms.csv")

# the vol-normalised outcomes
for win in ["full", "IS", "OOS"]:
    A[f"DDnorm_{win}"] = A[f"MaxDD_{win}"] / A[f"bookvol_{win}"]
    A[f"CAGRnorm_{win}"] = A[f"CAGR_{win}"] / A[f"bookvol_{win}"]

# ---------------------------------------------------------------- G1 reproduction gate
say("\n[A1] GATE G1 — do these arm-rows reproduce idea 295's committed .arms.csv?")
if ARMS_295.exists():
    A295 = pd.read_csv(ARMS_295)
    key = ["q", "draw", "arm"]
    shared = [c for c in A295.columns if c in A.columns and c not in key
              and pd.api.types.is_numeric_dtype(A295[c])]
    J = A295.merge(A, on=key, suffixes=("_ref", "_new"))
    d = {c: float(np.nanmax(np.abs(J[f"{c}_ref"].astype(float)
                                   - J[f"{c}_new"].astype(float)))) for c in shared}
    worst = max(d.values())
    G1 = bool(len(J) == len(A295) == len(A) and worst < 1e-9)
    say(f"  rows ref {len(A295)} / new {len(A)} / joined {len(J)}; {len(shared)} shared numeric "
        f"columns; max |delta| = {worst:.3e}  -> G1 {'PASS' if G1 else 'FAIL'}")
    say("  worst five columns: " + ", ".join(
        f"{k}={v:.2e}" for k, v in sorted(d.items(), key=lambda kv: -kv[1])[:5]))
else:
    G1 = False
    say(f"  MISSING {ARMS_295.name} -> G1 cannot be evaluated (reported as FAIL, not skipped)")

# ============================================================== B. premise: idea 295's slopes
def ols(y, X):
    """OLS of y on [1, X]; returns (coefs, ts, n, dof, R2). X is (n, p)."""
    y = np.asarray(y, float)
    X = np.asarray(X, float)
    if X.ndim == 1:
        X = X[:, None]
    ok = np.isfinite(y) & np.isfinite(X).all(axis=1)
    y, X = y[ok], X[ok]
    n = len(y)
    p = X.shape[1]
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


def zs(v):
    v = np.asarray(v, float)
    sd = np.nanstd(v)
    return (v - np.nanmean(v)) / sd if sd > 0 else v * np.nan


def slope_t(x, y):
    """idea 295's helper, verbatim in behaviour: slope of y on standardized x, its t, n."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    n = len(x)
    if n < 5 or np.std(x) == 0:
        return np.nan, np.nan, n
    xs = (x - x.mean()) / x.std(ddof=0)
    b = float(np.cov(xs, y, ddof=1)[0, 1] / np.var(xs, ddof=1))
    resid = y - y.mean() - b * xs
    dof = n - 2
    se = float(np.sqrt((resid @ resid) / dof / (np.sum(xs ** 2))))
    return b, (b / se if se > 0 else np.nan), n


def bin_q(qv, nb):
    return np.minimum((np.asarray(qv, float) * nb).astype(int), nb - 1)


def demean(v, strat):
    g = pd.DataFrame(dict(s=strat, v=np.asarray(v, float)))
    return (g.v - g.groupby("s").v.transform("mean")).to_numpy()


say("\n[B] GATE G2 — idea 295's pooled/within slopes recomputed here, and its PREMISE re-derived.")
rep = []
for win in ["full", "IS", "OOS"]:
    for arm in ["EWall"] + [f"top{n}" for n in NS]:
        sub = A[A.arm == arm]
        for ch in CHARS:
            for oc in OUTCOMES:
                x = sub[f"{ch}_{win}"].to_numpy()
                y = sub[f"{oc}_{win}"].to_numpy()
                bu, tu, nu = slope_t(x, y)
                for nb in STRATA:
                    st = bin_q(sub["q"], nb)
                    bw, tw, nw = slope_t(demean(x, st), demean(y, st))
                    rep.append(dict(window=win, arm=arm, char=ch, outcome=oc, strata=nb,
                                    b_pooled=bu, t_pooled=tu, n=nu, b_within=bw, t_within=tw,
                                    dof_within=nw - nb - 1,
                                    sign_flip=bool(np.isfinite(bu) and np.isfinite(bw)
                                                   and np.sign(bu) != np.sign(bw))))
S = pd.DataFrame(rep)
S.to_csv(f"{STEM}.slopes.csv", index=False)
if SLOPES_295.exists():
    R = pd.read_csv(SLOPES_295)
    k = ["window", "arm", "char", "outcome", "strata"]
    J = R.merge(S, on=k, suffixes=("_ref", "_new"))
    cols = ["b_pooled", "t_pooled", "b_within", "t_within"]
    dd = {c: float(np.nanmax(np.abs(J[f"{c}_ref"] - J[f"{c}_new"]))) for c in cols}
    G2 = bool(len(J) == len(R) == len(S) and max(dd.values()) < 1e-9)
    say(f"  rows ref {len(R)} / new {len(S)} / joined {len(J)}; max |delta| " +
        ", ".join(f"{c}={v:.2e}" for c, v in dd.items()) +
        f"  -> G2 {'PASS' if G2 else 'FAIL'}")
else:
    G2 = False
    say(f"  MISSING {SLOPES_295.name} -> G2 cannot be evaluated (reported as FAIL, not skipped)")

say("\n[B1] THE PREMISE, re-derived from those numbers (full window, 4 strata x 3 arms = 12 "
    "cells per characteristic-outcome):")
prem = []
for ch in CHARS:
    for oc in OUTCOMES:
        sub = S[(S.window == "full") & (S["char"] == ch) & (S.outcome == oc)]
        keeps = int((~sub.sign_flip).sum())
        sig = int((sub.t_within.abs() >= T_BAR).sum())
        prem.append(dict(char=ch, outcome=oc, cells=len(sub), sign_kept=keeps,
                         sign_flipped=int(sub.sign_flip.sum()),
                         within_sig=sig, t_min=sub.t_within.min(), t_max=sub.t_within.max()))
P = pd.DataFrame(prem)
P.to_csv(f"{STEM}.premise.csv", index=False)
say(P.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
ev = S[(S.window == "full") & (S["char"] == "evol")]
evdd = ev[ev.outcome == "MaxDD"]
say(f"\n  evol, full window, all {len(ev)} cells: sign kept in {int((~ev.sign_flip).sum())}, "
    f"flipped in {int(ev.sign_flip.sum())}.")
say(f"  evol vs MaxDD (the queue's quoted cell): within t runs {evdd.t_within.min():.2f} .. "
    f"{evdd.t_within.max():.2f} over {len(evdd)} cells; on EWall alone "
    f"{evdd[evdd.arm=='EWall'].t_within.min():.2f} .. {evdd[evdd.arm=='EWall'].t_within.max():.2f} "
    f"(the queue quotes -8.7 .. -6.0).")

# ============================================================== C. the collinearity itself
say("\n[C] COLLINEARITY — within-stratum correlation of each characteristic with THE BOOK'S OWN "
    "realised vol. This is the quantity the queue names; it is measured, not assumed.")
coll = []
for win in ["full", "IS", "OOS"]:
    for arm in ["EWall"] + [f"top{n}" for n in NS]:
        sub = A[A.arm == arm]
        bv = sub[f"bookvol_{win}"].to_numpy()
        for ch in CHARS:
            x = sub[f"{ch}_{win}"].to_numpy()
            for nb in STRATA:
                st = bin_q(sub["q"], nb)
                xw, bw_ = demean(x, st), demean(bv, st)
                ok = np.isfinite(xw) & np.isfinite(bw_)
                r = float(np.corrcoef(xw[ok], bw_[ok])[0, 1]) if ok.sum() > 3 else np.nan
                rp = float(np.corrcoef(x[np.isfinite(x) & np.isfinite(bv)],
                                       bv[np.isfinite(x) & np.isfinite(bv)])[0, 1])
                coll.append(dict(window=win, arm=arm, char=ch, strata=nb,
                                 corr_pooled=rp, corr_within=r, r2_within=r ** 2))
CO = pd.DataFrame(coll)
CO.to_csv(f"{STEM}.collinearity.csv", index=False)
say(CO[CO.window == "full"].pivot_table(index=["char", "strata"], columns="arm",
                                        values="corr_within")
    .to_string(float_format=lambda x: f"{x:+.3f}"))
say("\n  pooled (across the cap line) correlation with the book's vol, full window:")
say(CO[(CO.window == "full") & (CO.strata == STRATA[0])]
    .pivot_table(index="char", columns="arm", values="corr_pooled")
    .to_string(float_format=lambda x: f"{x:+.3f}"))

# ============================================================== D. the residualisation grid
say(f"\n[D] THE GRID — {len(RESIDS)} residualisations x {len(STRATA)} stratum resolutions, for "
    f"every characteristic x outcome x arm x window. ALL POINTS REPORTED "
    f"({len(RESIDS)*len(STRATA)*len(CHARS)*len(OUTCOMES+NORM_OUTCOMES)*3*3} rows -> .grid.csv).")
say("  none    y ~ x                    (idea 295's published within-stratum fit)")
say("  partial y ~ x + bookvol          (x's coefficient and its own t)")
say("  residx  y ~ resid(x | bookvol)   (the queue's literal wording; FWL => same slope as "
    "partial, different t)")
say("  ratio   y ~ x / bookvol          (scale-free restatement)")
say("  x is standardized inside each cell, so slopes are per-1sd and comparable down a column.")

grid = []
for win in ["full", "IS", "OOS"]:
    for arm in ["EWall"] + [f"top{n}" for n in NS]:
        sub = A[A.arm == arm]
        bv_raw = sub[f"bookvol_{win}"].to_numpy()
        for ch in CHARS:
            x_raw = sub[f"{ch}_{win}"].to_numpy()
            for oc in OUTCOMES + NORM_OUTCOMES:
                y_raw = sub[f"{oc}_{win}"].to_numpy()
                for nb in STRATA:
                    st = bin_q(sub["q"], nb)
                    y = demean(y_raw, st)
                    bv = demean(bv_raw, st)
                    for meth in RESIDS:
                        if meth == "none":
                            x = zs(demean(x_raw, st))
                            b, t, n, dof, r2 = ols(y, x)
                            b, t = b[0], t[0]
                            ctrl_t = np.nan
                        elif meth == "partial":
                            x = zs(demean(x_raw, st))
                            bb, tt, n, dof, r2 = ols(y, np.column_stack([x, zs(bv)]))
                            b, t, ctrl_t = bb[0], tt[0], tt[1]
                        elif meth == "residx":
                            x0 = zs(demean(x_raw, st))
                            bb, _, _, _, _ = ols(x0, zs(bv))
                            xr = x0 - (np.nanmean(x0) + bb[0] * zs(bv)) if np.isfinite(bb[0]) else x0 * np.nan
                            b, t, n, dof, r2 = ols(y, xr)
                            b, t = b[0], t[0]
                            ctrl_t = np.nan
                        else:  # ratio
                            with np.errstate(invalid="ignore", divide="ignore"):
                                xr = zs(demean(x_raw / bv_raw, st))
                            b, t, n, dof, r2 = ols(y, xr)
                            b, t = b[0], t[0]
                            ctrl_t = np.nan
                        grid.append(dict(window=win, arm=arm, char=ch, outcome=oc, strata=nb,
                                         resid=meth, b=b, t=t, n=n, dof=dof, r2=r2,
                                         ctrl_t=ctrl_t,
                                         sig=bool(np.isfinite(t) and abs(t) >= T_BAR)))
G = pd.DataFrame(grid)
G.to_csv(f"{STEM}.grid.csv", index=False)

say("\n--- FULL WINDOW, the three real outcomes, t of the characteristic's within-stratum slope ---")
for oc in OUTCOMES:
    say(f"\n  outcome = {oc}")
    say(G[(G.window == "full") & (G.outcome == oc)]
        .pivot_table(index=["char", "strata"], columns=["arm", "resid"], values="t")
        .reindex(columns=RESIDS, level=1)
        .to_string(float_format=lambda x: f"{x:+7.2f}"))

say("\n--- FULL WINDOW, the VOL-NORMALISED outcomes (test (ii)) ---")
for oc in NORM_OUTCOMES:
    say(f"\n  outcome = {oc}  ({'MaxDD' if oc=='DDnorm' else 'CAGR'} / the book's own vol)")
    say(G[(G.window == "full") & (G.outcome == oc) & (G.resid == "none")]
        .pivot_table(index=["char", "strata"], columns="arm", values="t")
        .to_string(float_format=lambda x: f"{x:+7.2f}"))

say("\n[D1] THE ANSWER, cell by cell: does each characteristic's within-stratum slope SURVIVE the "
    f"control? (|t| >= {T_BAR}; 'none' vs 'partial' on the same cell.)")
surv = []
for win in ["full", "IS", "OOS"]:
    for oc in OUTCOMES:
        for ch in CHARS:
            for nb in STRATA:
                for arm in ["EWall"] + [f"top{n}" for n in NS]:
                    g0 = G[(G.window == win) & (G.outcome == oc) & (G["char"] == ch)
                           & (G.strata == nb) & (G.arm == arm)]
                    a_ = g0[g0.resid == "none"].iloc[0]
                    b_ = g0[g0.resid == "partial"].iloc[0]
                    c_ = g0[g0.resid == "ratio"].iloc[0]
                    surv.append(dict(window=win, outcome=oc, char=ch, strata=nb, arm=arm,
                                     t_none=a_.t, t_partial=b_.t, t_ratio=c_.t,
                                     b_none=a_.b, b_partial=b_.b,
                                     sig_none=bool(a_.sig), sig_partial=bool(b_.sig),
                                     killed=bool(a_.sig and not b_.sig),
                                     shrink=float(abs(b_.b) / abs(a_.b)) if abs(a_.b) > 0 else np.nan))
SV = pd.DataFrame(surv)
SV.to_csv(f"{STEM}.survival.csv", index=False)
say("\n  full window, per characteristic x outcome (12 cells each = 4 strata x 3 arms):")
say(SV[SV.window == "full"].groupby(["char", "outcome"])
    .agg(cells=("killed", "size"), sig_none=("sig_none", "sum"), sig_partial=("sig_partial", "sum"),
         killed=("killed", "sum"), median_shrink=("shrink", "median"))
    .to_string(float_format=lambda x: f"{x:.3f}"))
say("\n  ('sig_none' = the published within-stratum fit is non-zero; 'sig_partial' = it is still "
    "non-zero once the BOOK'S OWN VOL is in the regression; 'killed' = was, is not; "
    "'median_shrink' = |b_partial| / |b_none|.)")
say("\n  the same cells split by ARM, because the arm is where the answer lives:")
say(SV[SV.window == "full"].groupby(["char", "outcome", "arm"])
    .agg(cells=("killed", "size"), sig_none=("sig_none", "sum"),
         sig_partial=("sig_partial", "sum"), killed=("killed", "sum"))
    .to_string())

# ------------------------------------------------------- D2. the arbitration (log-log elasticity)
say("\n[D2] ARBITRATION — the LINEAR partial and the RATIO specifications disagree, so neither is "
    "quoted alone. Drawdown is multiplicative in vol, so the clean form is a LOG-LOG elasticity:")
say("     log|MaxDD| ~ log(char) + log(bookvol), within stratum. The char's coefficient is its "
    "elasticity HOLDING the book's own vol; a ratio outcome cannot separate the two and a linear "
    "control mis-specifies the functional form. Only strictly positive characteristics can enter "
    "(corr and, on some panels, disp go negative) — those cells are reported NA, not dropped "
    "silently.")
logrows = []
for win in ["full", "IS", "OOS"]:
    for arm in ["EWall"] + [f"top{n}" for n in NS]:
        sub = A[A.arm == arm]
        with np.errstate(invalid="ignore", divide="ignore"):
            lbv = np.log(sub[f"bookvol_{win}"].to_numpy())
            ldd = np.log(np.abs(sub[f"MaxDD_{win}"].to_numpy()))
        for ch in CHARS:
            xr = sub[f"{ch}_{win}"].to_numpy()
            frac_pos = float(np.mean(xr > 0))
            with np.errstate(invalid="ignore", divide="ignore"):
                lx = np.log(np.where(xr > 0, xr, np.nan))
            for nb in STRATA:
                st = bin_q(sub["q"], nb)
                y = demean(ldd, st)
                b_r, t_r, n_r, _, _ = ols(y, demean(lx, st))
                bb, tt, n1, _, r2 = ols(y, np.column_stack([demean(lx, st), demean(lbv, st)]))
                logrows.append(dict(window=win, arm=arm, char=ch, strata=nb, frac_positive=frac_pos,
                                    elast_raw=b_r[0], t_raw=t_r[0],
                                    elast_ctrl=bb[0], t_ctrl=tt[0],
                                    elast_bookvol=bb[1], t_bookvol=tt[1], n=n1, r2=r2,
                                    sig_raw=bool(np.isfinite(t_r[0]) and abs(t_r[0]) >= T_BAR),
                                    sig_ctrl=bool(np.isfinite(tt[0]) and abs(tt[0]) >= T_BAR)))
LG = pd.DataFrame(logrows)
LG.to_csv(f"{STEM}.loglog.csv", index=False)
say("\n  full window — elasticity of |MaxDD| wrt the characteristic, with and without log(bookvol):")
say(LG[LG.window == "full"]
    .pivot_table(index=["char", "strata"], columns="arm",
                 values=["elast_raw", "t_raw", "elast_ctrl", "t_ctrl"])
    .reindex(columns=["elast_raw", "t_raw", "elast_ctrl", "t_ctrl"], level=0)
    .to_string(float_format=lambda x: f"{x:+7.2f}"))
say("\n  elasticity of |MaxDD| wrt the BOOK'S OWN vol in the same fits (the mediator itself):")
say(LG[LG.window == "full"].pivot_table(index=["char", "strata"], columns="arm",
                                        values="elast_bookvol")
    .to_string(float_format=lambda x: f"{x:+7.3f}"))
lg_ev = LG[(LG.window == "full") & (LG["char"] == "evol")]
say(f"\n  evol, full window: {int(lg_ev.sig_raw.sum())}/{len(lg_ev)} cells non-zero WITHOUT "
    f"log(bookvol), {int(lg_ev.sig_ctrl.sum())}/{len(lg_ev)} WITH it; per arm: " + ", ".join(
        f"{a} {int(lg_ev[lg_ev.arm==a].sig_ctrl.sum())}/{len(lg_ev[lg_ev.arm==a])}"
        for a in ["EWall", "top10", "top20"]))

# ============================================================== E. rule 8
say("\n[E] RULE 8 — every slope and verdict re-fitted on the FIRST HALF only (<= "
    f"{IS_END.date()}); the second half read ONCE.")
wf = []
for oc in OUTCOMES:
    for ch in CHARS:
        for nb in STRATA:
            for meth in RESIDS:
                for arm in ["EWall"] + [f"top{n}" for n in NS]:
                    gi = G[(G.window == "IS") & (G.outcome == oc) & (G["char"] == ch)
                           & (G.strata == nb) & (G.resid == meth) & (G.arm == arm)].iloc[0]
                    go = G[(G.window == "OOS") & (G.outcome == oc) & (G["char"] == ch)
                           & (G.strata == nb) & (G.resid == meth) & (G.arm == arm)].iloc[0]
                    vis = "NONZERO" if gi.sig else "ZERO"
                    vos = "NONZERO" if go.sig else "ZERO"
                    wf.append(dict(outcome=oc, char=ch, strata=nb, resid=meth, arm=arm,
                                   t_IS=gi.t, t_OOS=go.t, IS_verdict=vis, OOS_verdict=vos,
                                   holds=bool(vis == vos),
                                   sign_holds=bool(np.isfinite(gi.b) and np.isfinite(go.b)
                                                   and np.sign(gi.b) == np.sign(go.b))))
WF = pd.DataFrame(wf)
WF.to_csv(f"{STEM}.walkforward.csv", index=False)
say(f"  {len(WF)} (outcome x char x strata x resid x arm) cells; the IS verdict comes back OOS in "
    f"{int(WF.holds.sum())} ({WF.holds.mean():.1%}), the IS SIGN in {int(WF.sign_holds.sum())} "
    f"({WF.sign_holds.mean():.1%}).")
say("\n  per characteristic x residualisation:")
say(WF.pivot_table(index=["char", "resid"], columns="outcome", values="holds")
    .to_string(float_format=lambda x: f"{x:.3f}"))
say("\n  evol only, every grid point (t_IS -> t_OOS), outcome = MaxDD:")
say(WF[(WF["char"] == "evol") & (WF.outcome == "MaxDD")]
    [["arm", "strata", "resid", "t_IS", "t_OOS", "IS_verdict", "OOS_verdict", "holds"]]
    .to_string(index=False, float_format=lambda x: f"{x:+7.2f}"))

say("\n[E1] THE BOOKS THEMSELVES — OOS CAGR / Sharpe / MaxDD vs the live RULES v2 baseline and "
    "SPY, and BOTH KEEP paths on every arm-row (no selection).")
bk = (A.groupby("arm")
      .agg(rows=("pass4b", "size"), CAGR=("CAGR_full", "median"), Sharpe=("Sharpe_full", "median"),
           MaxDD=("MaxDD_full", "median"), Vol=("bookvol_full", "median"),
           H1=("H1", "median"), H2=("H2", "median"),
           OOS_CAGR=("CAGR_OOS", "median"), OOS_Sharpe=("Sharpe_OOS", "median"),
           OOS_MaxDD=("MaxDD_OOS", "median"),
           pass4a=("pass4a", "mean"), pass4b=("pass4b", "mean"))
      .reset_index())
base_row = dict(arm="RULES v2 (live, same panels)", rows=len(A), CAGR=A.base_CAGR.median(),
                Sharpe=A.base_Sharpe.median(), MaxDD=A.base_MaxDD.median(), Vol=np.nan,
                H1=A.base_H1.median(), H2=A.base_H2.median(), OOS_CAGR=A.base_OOS_CAGR.median(),
                OOS_Sharpe=A.base_OOS_Sharpe.median(), OOS_MaxDD=A.base_OOS_MaxDD.median(),
                pass4a=np.nan, pass4b=np.nan)
spy_row = dict(arm="SPY", rows=len(A), CAGR=A.SPY_CAGR.iloc[0], Sharpe=A.SPY_Sharpe.iloc[0],
               MaxDD=A.SPY_MaxDD.iloc[0], Vol=np.nan, H1=A.SPY_H1.iloc[0], H2=A.SPY_H2.iloc[0],
               OOS_CAGR=A.SPY_OOS_CAGR.iloc[0], OOS_Sharpe=A.SPY_OOS_Sharpe.iloc[0],
               OOS_MaxDD=A.SPY_OOS_MaxDD.iloc[0], pass4a=np.nan, pass4b=np.nan)
BK = pd.concat([bk, pd.DataFrame([base_row, spy_row])], ignore_index=True)
BK.to_csv(f"{STEM}.keeppaths.csv", index=False)
say(BK.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
say(f"\n  4a passes {int(A.pass4a.sum())}/{len(A)} ({A.pass4a.mean():.1%}); "
    f"4b passes {int(A.pass4b.sum())}/{len(A)} ({A.pass4b.mean():.1%}) — no arm of this run is a "
    "KEEP candidate; the run's object is a slope, not a book.")
say("\n  per q rung (median), so the ladder is visible rather than averaged away:")
say(A.pivot_table(index="q", columns="arm", values=["Sharpe_OOS", "bookvol_full", "pass4b"],
                  aggfunc="median").to_string(float_format=lambda x: f"{x:.3f}"))

# ============================================================== F. verdict
say("\n[F] VERDICT")
f_ = SV[(SV.window == "full")]
ev_dd = f_[(f_["char"] == "evol") & (f_.outcome == "MaxDD")]
ev_all = f_[f_["char"] == "evol"]
oth = f_[f_["char"] != "evol"]
ev_ddn = G[(G.window == "full") & (G["char"] == "evol") & (G.outcome == "DDnorm")
           & (G.resid == "none")]
say(f"  evol vs MaxDD: {int(ev_dd.sig_none.sum())}/{len(ev_dd)} cells non-zero WITHOUT the control, "
    f"{int(ev_dd.sig_partial.sum())}/{len(ev_dd)} WITH it; median |b| shrink "
    f"{ev_dd.shrink.median():.3f}.")
say(f"  evol, all outcomes: {int(ev_all.sig_none.sum())}/{len(ev_all)} -> "
    f"{int(ev_all.sig_partial.sum())}/{len(ev_all)}; other three characteristics: "
    f"{int(oth.sig_none.sum())}/{len(oth)} -> {int(oth.sig_partial.sum())}/{len(oth)}.")
say(f"  evol vs the VOL-NORMALISED drawdown (DDnorm), no control: "
    f"{int(ev_ddn.sig.sum())}/{len(ev_ddn)} cells non-zero, |t| max "
    f"{ev_ddn.t.abs().max():.2f}.")
say(f"  within-stratum corr(evol, book vol), full window, median over strata x arms: "
    f"{CO[(CO.window=='full') & (CO['char']=='evol')].corr_within.median():+.3f}; "
    "the other three: " + ", ".join(
        f"{c} {CO[(CO.window=='full') & (CO['char']==c)].corr_within.median():+.3f}"
        for c in CHARS if c != "evol"))
say("  the arm split (this is where the answer lives) — evol vs MaxDD, none -> partial:")
for arm in ["EWall"] + [f"top{n}" for n in NS]:
    z = ev_dd[ev_dd.arm == arm]
    say(f"    {arm:6s}: {int(z.sig_none.sum())}/{len(z)} -> {int(z.sig_partial.sum())}/{len(z)}"
        f"   t_none {z.t_none.min():+6.2f}..{z.t_none.max():+6.2f}"
        f"   t_partial {z.t_partial.min():+6.2f}..{z.t_partial.max():+6.2f}"
        f"   corr(evol, bookvol) within "
        f"{CO[(CO.window=='full') & (CO['char']=='evol') & (CO.arm==arm)].corr_within.min():+.3f}.."
        f"{CO[(CO.window=='full') & (CO['char']=='evol') & (CO.arm==arm)].corr_within.max():+.3f}")
say("  the PREMISE ITSELF — sign-keeping cells per characteristic (full window, 36 each): " +
    ", ".join(f"{c} {int((~S[(S.window=='full') & (S['char']==c)].sign_flip).sum())}/36"
              for c in CHARS))
say(f"  log-log arbitration, evol vs |MaxDD| holding log(book vol): "
    f"{int(lg_ev.sig_ctrl.sum())}/{len(lg_ev)} cells non-zero "
    f"(elasticity {lg_ev.elast_ctrl.min():+.3f}..{lg_ev.elast_ctrl.max():+.3f}); on EWall "
    f"{int(lg_ev[lg_ev.arm=='EWall'].sig_ctrl.sum())}/{len(lg_ev[lg_ev.arm=='EWall'])}.")
say(f"  gates: G1 {'PASS' if G1 else 'FAIL'}, G2 {'PASS' if G2 else 'FAIL'}.")
say("  (The classification of the surviving/dying slopes as MEDIATION vs SPURIOUS is argued in "
    "the .result.md from these numbers; this script reports the numbers.)")

say(f"\ndone in {time.time()-t0:.1f}s")
Path(f"{STEM}.console.txt").write_text("\n".join(OUT) + "\n")

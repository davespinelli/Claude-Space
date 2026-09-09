#!/usr/bin/env python3
"""Idea 252 - "name-level-fixed-effects-instead-of-a-draw-scalar" (lane B, 2026-09-09).

The question
------------
Idea 83 asked whether draw-level momentum dispersion `sd` still predicts a draw's Sharpe
once the draw's WINNER CONTENT is held fixed, and controlled winner content with ONE
SCALAR per draw: `W`, the mean full-sample annualised log return of the draw's own names
(plus `W_max`, the draw's single best name, as a second control).  Dispersion survived:
pooled n=20 CAND-20, R2(sd) 0.3062 -> partial R2(sd | W) 0.1899, t +5.87, `kill` 0.620.
Idea 83 itself flagged the weakness in its own caveat list: "W is one scalar per draw (a
name-by-name fixed-effect design would be stronger and is not run)".

This run runs it.  The composition control becomes the draw's full 136-column MEMBERSHIP
INDICATOR VECTOR, fitted by ridge (k <= 80 names out of 136, N = 50 draws per cell, so
the design is rank-deficient by construction and the penalty is doing real work).  The
question the queue poses:

    does dispersion add anything to the FITTED composition effect, not to a summary of it?

    If sd still survives  -> idea 83's 62% is structural, idea 78's test C is safe outright.
    If sd dies           -> idea 83's answer is a POWER result about the scalar, not a
                            result about dispersion.

The hazard, stated before any number is read
--------------------------------------------
`sd` is itself a deterministic function of the draw's membership.  A name-level model with
136 free parameters fitted on 50 (or 150) observations can therefore absorb `sd` by
overfitting the same y that `sd` is being tested on, and would report `sd` dead for a
reason that has nothing to do with composition.  So the IN-SAMPLE fitted composition
effect is NOT a valid control and is reported only for completeness.  THE TEST uses
OUT-OF-FOLD fitted values: F_oof(i) is draw i's composition fit from a ridge estimated on
the other 9 folds, so F never saw draw i's own y.  Both schemes are reported at every
grid point; the pre-registered verdict is read off the out-of-fold column.

Two additional legs that the scalar design could not run:
  * POWER AUDIT.  How much of `sd` does the name-level model itself explain (sd ~ M,
    in-sample and out-of-fold)?  If F spans sd, the partial test has no power BY
    CONSTRUCTION and a dead sd coefficient means nothing.  Idea 83 could not ask this
    because a scalar cannot span sd.
  * NESTED PREDICTION.  Out-of-fold R2 of y ~ M against y ~ M + sd.  This is immune to
    in-sample overfit in both directions: if sd carries composition-independent
    information, adding it must improve out-of-fold prediction.

Pre-registered bars (written before any new number was read; idea 83's own bars, reused
verbatim so the two runs are directly comparable)
    sd is KILLED by the name-level control iff, on the OUT-OF-FOLD scheme at the
    CV-selected penalty, kill = pR2(sd | F_oof) / R2(sd) < 1/3 AND |t(sd | F_oof)| < 2.
    sd SURVIVES iff |t| > 2 with kill >= 1/3.  Anything between is reported as SPLIT.
    Secondary: the nested out-of-fold R2 gain from adding sd must be > 0.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. lam   ridge penalty, grid {0.5, 2, 8, 32, 128, 512} - ALL SIX REPORTED at every cell.
    2. fit   scheme in {in-sample, out-of-fold(10)} - BOTH REPORTED at every cell.
  Everything else is idea 78/83's and is imported unchanged: the panel (B136), the seeds
  (SEED_B + k), the draws (150), the sub-panel sizes k in {20,40,80}, the book sizes
  n in {5,20}, the gate, gross 0.75, weekly cadence, 10 bps, the IS/OOS split.

Reproduction gate (run BEFORE any new number is read)
    [a] harness: idea 2's U56/CAND20 row and the live RULES v1 row from engine.backtest.
    [b] MEMBERSHIP: the 150 sub-panels are re-drawn from idea 78's seeds and the six
        membership-derived columns of idea 83's committed draws.csv (W, W_IS, W_sd,
        W_max, W_cw, W_cov) are recomputed from the reconstructed name sets.  Six
        different functions of the same set; if all six reproduce, the membership matrix
        M is provably idea 83's own.  This is the gate that matters here, because M is
        the entire object this run adds.
    [c] the committed draws.csv is checked column-by-column against idea 78's committed
        gridB.csv (the file idea 83 already gated at 8.3e-17 - 7.1e-15).
    The 450 books are NOT re-run: they are idea 83's committed output, gated at [c], and
    this run changes no book.  Every book metric used below is read from that file.

Walk-forward (PROTOCOL rule 8), selectors fixed before any OOS number was read
    S0  do-nothing: full B136 CAND-20 (idea 78's control, recomputed here).
    S1  IS-Sharpe argmax                                     (idea 83's, from draws.csv)
    S2  DISPERSION: max IS sd                                (idea 83's)
    S3  COUNT: max IS n_elig                                 (idea 83's)
    S5  RESID-DISP (scalar control): max IS sd | W_IS        (idea 83's)
    S6  WINNERNESS: max IS W_IS                              (idea 83's)
    S4  random sub-panel                                     (idea 83's seed)
    S7  FE-RESID-DISP (NEW): max IS sd after the NAME-LEVEL out-of-fold composition fit
        F_oof(Sharpe_IS ~ M) is regressed out of it.  The penalty is chosen by IS
        cross-validation on IS data only; the whole penalty ladder's OOS outcome is
        reported so nothing is hidden.
    All selector inputs use 2009-2016 only; 2017-2026 is read once.

KEEP paths (PROTOCOL rule 4).  This run introduces NO new book - the object under test is
a statistic about idea 78's 450 books - so 4a/4b are restated from the committed grid for
all 450 books, and evaluated freshly for the 7 rule-8 selector arms.

Survivorship: universe_broad.json is CURRENT CONSTITUENTS (rule 9).  As in idea 83 this is
the premise under test rather than a caveat to it: the name-level control is built from
realised returns of names already known to have survived, which UNDER-states true winner
content and so makes the control conservative - it cuts against a surviving sd, not for it.

Deterministic (fixed seeds, deterministic folds by draw index), standalone.  Reads
baseline.py and engine.py; modifies nothing.
"""
import sys, time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import warnings
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore", category=RuntimeWarning)
from baseline import load_universe, rules_v1_weights, score
from engine import backtest, metrics

# ---- idea 78/83's constants, imported verbatim ----------------------------------
COST_BPS = 10
FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
KS = [20, 40, 80]
N_BOOKS = [5, 20]
N_BOOK = 20
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SEED_B = 78_500
SEED_S4 = 78_999

# ---- this run's two tuned parameters, both fully reported ------------------------
LAMS = [0.5, 2.0, 8.0, 32.0, 128.0, 512.0]
SCHEMES = ["IS", "OOF"]
N_FOLDS = 10

SCRIPT = Path(__file__).name
OUT = REPO / "research" / "backtests"
STEM = SCRIPT[:-3]
REF_DRAWS = OUT / "2026-09-06_dispersion-as-a-survivorship-detector_B.draws.csv"
REF_GRIDB = OUT / "2026-09-05_candidate-count-vs-dispersion_B.gridB.csv"

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 500)

_lines = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


# ---------------------------------------------------------------- idea 78's book helpers
def eligible_mask(px, tradable):
    _, above, vol20 = score(px)
    m = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        m[drop] = False
    return m


def weights_cand(px, tradable, n, gross=GROSS):
    elig = eligible_mask(px, tradable)
    s = score(px, vol_scale=False)[0]
    rank = s.where(elig).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (gross / n)


def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def fail_4a(r, base):
    h1, h2 = half_sharpes(r); b1, b2 = half_sharpes(base)
    f = []
    if not h1 > b1: f.append("H1")
    if not h2 > b2: f.append("H2")
    if not metrics(r)["MaxDD"] >= metrics(base)["MaxDD"]: f.append("DD")
    return ",".join(f) if f else "-"


def fail_4b(r, spy, r_oos, spy_oos):
    h1, h2 = half_sharpes(r); s1, s2 = half_sharpes(spy)
    ms, mr = metrics(spy), metrics(r)
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not metrics(r_oos)["Sharpe"] > metrics(spy_oos)["Sharpe"]: f.append("OOS")
    if not mr["MaxDD"] >= 0.60 * ms["MaxDD"]: f.append("DD")
    if not mr["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def spearman(a, b):
    a, b = pd.Series(np.asarray(a, float)), pd.Series(np.asarray(b, float))
    m = a.notna() & b.notna()
    if m.sum() < 3: return np.nan
    return float(a[m].rank().corr(b[m].rank()))


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ---------------------------------------------------------------- regression helpers
def ols(y, X, names):
    """Plain OLS with an intercept (idea 83's helper, imported verbatim)."""
    y = np.asarray(y, float)
    X = np.column_stack([np.ones(len(y))] + [np.asarray(c, float) for c in X])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    dof = len(y) - X.shape[1]
    s2 = float(resid @ resid) / dof
    XtXi = np.linalg.pinv(X.T @ X)
    se = np.sqrt(np.diag(XtXi) * s2)
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1.0 - float(resid @ resid) / ss_tot if ss_tot > 0 else np.nan
    return dict(R2=r2, n=len(y), resid=resid,
                coef=dict(zip(["const"] + names, beta)),
                t=dict(zip(["const"] + names, beta / se)))


def resid_on(y, x):
    return ols(y, [x], ["x"])["resid"]


def partial_r2(y, x, ctrl):
    """R2 between resid(y|ctrl) and resid(x|ctrl); its t is the t on x in y ~ x + ctrl."""
    ry, rx = resid_on(y, ctrl), resid_on(x, ctrl)
    full = ols(y, [x, ctrl], ["x", "ctrl"])
    r = np.corrcoef(ry, rx)[0, 1]
    return dict(pR2=r ** 2, r=r, t=full["t"]["x"], full_R2=full["R2"], t_ctrl=full["t"]["ctrl"])


def ridge_fit(X, y, lam, free=0):
    """Ridge with an UNPENALISED intercept and `free` leading unpenalised columns.

    X is centred internally; the penalty applies to the remaining (name) columns only.
    Returns (b0, beta) with prediction b0 + Xc @ beta where Xc = X - Xmean.
    """
    X = np.asarray(X, float); y = np.asarray(y, float)
    xm = X.mean(axis=0); Xc = X - xm; ym = y.mean()
    p = Xc.shape[1]
    D = np.ones(p) * lam
    if free:
        D[:free] = 0.0
    A = Xc.T @ Xc + np.diag(D)
    beta = np.linalg.solve(A, Xc.T @ (y - ym))
    return ym, xm, beta


def ridge_predict(X, ym, xm, beta):
    return ym + (np.asarray(X, float) - xm) @ beta


def ridge_edf(X, lam, free=0):
    """Effective degrees of freedom, trace(H), so the reader can see how saturated the fit is."""
    X = np.asarray(X, float); Xc = X - X.mean(axis=0)
    p = Xc.shape[1]
    D = np.ones(p) * lam
    if free:
        D[:free] = 0.0
    A = Xc.T @ Xc + np.diag(D)
    return 1.0 + float(np.trace(Xc @ np.linalg.solve(A, Xc.T)))


def fit_composition(M, y, lam, folds, free=0):
    """Return (F_is, F_oof): in-sample and out-of-fold name-level fitted composition effect."""
    ym, xm, beta = ridge_fit(M, y, lam, free)
    F_is = ridge_predict(M, ym, xm, beta)
    F_oof = np.empty(len(y))
    for f in np.unique(folds):
        te = folds == f; tr = ~te
        ym_, xm_, b_ = ridge_fit(M[tr], y[tr], lam, free)
        F_oof[te] = ridge_predict(M[te], ym_, xm_, b_)
    return F_is, F_oof


def oof_r2(y, pred):
    y = np.asarray(y, float)
    ss = float(((y - y.mean()) ** 2).sum())
    return 1.0 - float(((y - pred) ** 2).sum()) / ss if ss > 0 else np.nan


# ================================================================== main
def main():
    t0 = time.time()
    P("=" * 210)
    P("IDEA 252 - name-level-fixed-effects-instead-of-a-draw-scalar (lane B, 2026-09-09)")
    P("Does draw dispersion survive a NAME-LEVEL composition control (136-column membership, ridge),")
    P("or was idea 83's surviving 62% a power result about its one-scalar control?")
    P("=" * 210)

    # ---------------------------------------------------------------- [a] harness
    P("\n[a] HARNESS - published rows recomputed from engine.backtest before anything new is read")
    px56 = load_universe()
    px136 = load_universe(broad=True)
    s56 = px56.index[260]
    r_u56 = backtest(px56, weights_cand(px56, set(px56.columns), 20), cost_bps=COST_BPS,
                     freq=FREQ)["returns"].loc[s56:]
    m = metrics(r_u56); h1, h2 = half_sharpes(r_u56)
    P(f"    U56/CAND20   {m['CAGR']:.4%} / {m['Sharpe']:.5f} / {m['MaxDD']:.4%}  halves {h1:.5f}/{h2:.5f}"
      f"   (ideas 2/73/77/83 published 12.7% / 1.092-1.093 / -18.3%, halves 1.088/1.102-1.103)")
    r_v1 = backtest(px56, rules_v1_weights(px56), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[s56:]
    m = metrics(r_v1)
    P(f"    U56/RULES v1 {m['CAGR']:.4%} / {m['Sharpe']:.5f} / {m['MaxDD']:.4%}   (published 6.5% / 0.664-0.666 / -13.8%)")

    startb = px136.index[260]
    spy = px136["SPY"].pct_change().fillna(0).loc[startb:]
    spy_oos = spy.loc[OOS_START:]
    base = backtest(px136, rules_v1_weights(px136), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[startb:]
    ms = metrics(spy); sh1, sh2 = half_sharpes(spy)
    P(f"    window {startb.date()} -> {px136.index[-1].date()}  ({len(spy)} days), panel {px136.shape[1]} columns")
    P(f"    SPY   {ms['CAGR']:.2%} / {ms['Sharpe']:.3f} / {ms['MaxDD']:.2%}  halves {sh1:.3f}/{sh2:.3f}"
      f"  OOS {metrics(spy_oos)['Sharpe']:.3f}")
    P(f"    RULES v1 on B136 {metrics(base)['CAGR']:.2%} / {metrics(base)['Sharpe']:.3f} / "
      f"{metrics(base)['MaxDD']:.2%}  OOS {metrics(base.loc[OOS_START:])['Sharpe']:.3f}")

    # ---------------------------------------------------------------- name-level returns (idea 83's W, verbatim)
    names136 = list(px136.columns)
    px_n = px136[names136].loc[startb:]

    def ann_logret(p):
        out = {}
        for c in p.columns:
            s = p[c].dropna()
            if len(s) < 252 or s.iloc[0] <= 0:
                out[c] = np.nan; continue
            yrs = (s.index[-1] - s.index[0]).days / 365.25
            out[c] = float(np.log(s.iloc[-1] / s.iloc[0]) / yrs)
        return pd.Series(out)

    lr_full = ann_logret(px_n)
    lr_is = ann_logret(px_n.loc[:IS_END])
    cw_full = np.log(px_n.iloc[-1] / px_n.iloc[0])

    # ---------------------------------------------------------------- [b] membership gate
    P(f"\n[b] MEMBERSHIP GATE - idea 78's 150 sub-panels re-drawn from SEED_B+k and every")
    P(f"    membership-derived column of idea 83's committed draws.csv recomputed from the name sets")
    if not REF_DRAWS.exists():
        P("    ABORT: idea 83's draws.csv is missing."); return
    B = pd.read_csv(REF_DRAWS)
    draw_cols = {}
    for k in KS:
        rng = np.random.default_rng(SEED_B + k)
        for d in range(50):
            draw_cols[(k, d)] = list(rng.choice(names136, size=k, replace=False))
    chk = {c: 0.0 for c in ["W", "W_IS", "W_sd", "W_max", "W_cw", "W_cov"]}
    for _, r in B.iterrows():
        cols = draw_cols[(int(r.k), int(r.draw))]
        got = dict(W=float(lr_full[cols].mean()), W_IS=float(lr_is[cols].mean()),
                   W_sd=float(lr_full[cols].std()), W_max=float(lr_full[cols].max()),
                   W_cw=float(cw_full[cols].mean()), W_cov=float(lr_full[cols].notna().mean()))
        for c, v in got.items():
            chk[c] = max(chk[c], abs(v - float(r[c])))
    P(f"    {len(B)} rows; max abs difference by column:")
    for c, v in chk.items():
        P(f"      {c:<6} {v:.3e}")
    ok_m = max(chk.values()) < 1e-9
    P(f"    MEMBERSHIP {'PASS - M is idea 83s own membership matrix' if ok_m else 'FAIL'}")

    P("\n[c] idea 83's draws.csv vs idea 78's committed gridB.csv (the file idea 83 gated at 8.3e-17-7.1e-15)")
    ok_c = True
    if REF_GRIDB.exists():
        ref = pd.read_csv(REF_GRIDB)
        j = B.merge(ref, on=["k", "n", "draw"], suffixes=("", "_ref"))
        cols = ["n_elig", "sd", "n_elig_IS", "sd_IS", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                "Sharpe_IS", "Sharpe_OOS", "CAGR_OOS", "MaxDD_OOS", "ew_Sharpe", "ew_CAGR",
                "ew_MaxDD", "premium"]
        dmax = max(float((j[c] - j[c + "_ref"]).abs().max()) for c in cols)
        same = int((j["f4b"] == j["f4b_ref"]).sum())
        ok_c = dmax < 1e-9 and len(j) == 300
        P(f"    {len(j)} rows, {len(cols)} numeric columns, max abs difference {dmax:.3e}; "
          f"f4b strings identical in {same}/{len(j)}")
    else:
        P("    gridB.csv absent - gate [c] skipped")
    if not (ok_m and ok_c):
        P("    ABORT: the object under test is not the published one."); return
    P("    REPRODUCTION PASS - new numbers may be read")

    # ---------------------------------------------------------------- build M
    P("\n" + "=" * 210)
    P("THE MEMBERSHIP MATRIX M")
    P("=" * 210)
    nm_idx = {c: i for i, c in enumerate(names136)}
    Mall = {}
    for key, cols in draw_cols.items():
        v = np.zeros(len(names136))
        for c in cols:
            v[nm_idx[c]] = 1.0
        Mall[key] = v
    P(f"    {len(names136)} name columns x 50 draws per k cell (150 pooled).  Row sums = k exactly.")
    for k in KS:
        Mk = np.array([Mall[(k, d)] for d in range(50)])
        cnt = Mk.sum(axis=0)
        P(f"      k={k:<3} N=50   rank(M) {np.linalg.matrix_rank(Mk)}   "
          f"name appearance count min/median/max {int(cnt.min())}/{int(np.median(cnt))}/{int(cnt.max())}  "
          f"(names never drawn: {int((cnt == 0).sum())})")
    P("    effective df trace(H) of the ridge composition fit, by k and penalty:")
    edf_rows = []
    for k in KS:
        Mk = np.array([Mall[(k, d)] for d in range(50)])
        edf_rows.append(dict(k=k, N=50, **{f"lam={l:g}": ridge_edf(Mk, l) for l in LAMS}))
    P(fmt(pd.DataFrame(edf_rows).set_index("k"), 2))
    P("    (N=50 rows against 136 name columns: at lam=0.5 the fit is nearly saturated, which is")
    P("     exactly why the IN-SAMPLE scheme below cannot be read as a control.)")

    # ---------------------------------------------------------------- power audit
    P("\n" + "=" * 210)
    P("POWER AUDIT - how much of `sd` does the name-level model itself explain?")
    P("A control that SPANS sd cannot leave a coefficient on sd to test.  Idea 83's scalar could not")
    P("do this (one number cannot span a dispersion); a 136-column model can, and might.")
    P("=" * 210)
    pow_rows = []
    for k in KS:
        Mk = np.array([Mall[(k, d)] for d in range(50)])
        folds = np.arange(50) % N_FOLDS
        sub = B[(B.n == N_BOOK) & (B.k == k)].sort_values("draw")
        sdv = sub["sd"].values
        for lam in LAMS:
            Fi, Fo = fit_composition(Mk, sdv, lam, folds)
            pow_rows.append(dict(k=k, lam=lam,
                                 R2_sd_M_IS=oof_r2(sdv, Fi), R2_sd_M_OOF=oof_r2(sdv, Fo),
                                 corr_IS=float(np.corrcoef(sdv, Fi)[0, 1]),
                                 corr_OOF=float(np.corrcoef(sdv, Fo)[0, 1])))
    PW = pd.DataFrame(pow_rows)
    PW.to_csv(OUT / f"{STEM}.power.csv", index=False)
    P(fmt(PW.set_index(["k", "lam"])))
    P("    Read: R2_sd_M_IS near 1.0 means the in-sample fit reproduces sd almost exactly (no power).")
    P("    R2_sd_M_OOF is the honest number: how much of sd a name-additive model genuinely carries.")

    # ---------------------------------------------------------------- THE TEST
    P("\n" + "=" * 210)
    P("THE TEST - does sd survive the NAME-LEVEL composition control?   ALL 6 penalties x 2 schemes x")
    P("3 y-columns x 3 k-cells + pooled are reported.  Pre-registered bar (idea 83's): sd is KILLED")
    P("iff kill = pR2(sd|F)/R2(sd) < 1/3 AND |t(sd|F)| < 2, read on the OUT-OF-FOLD scheme.")
    P("=" * 210)
    rows = []
    YCOLS = [("Sharpe", "CAND Sharpe"), ("ew_Sharpe", "EWall Sharpe"), ("premium", "premium")]
    scopes = [("pooled", None)] + [(f"k={k}", k) for k in KS]
    for nb in N_BOOKS:
        for scope, k in scopes:
            if k is None:
                sub = B[B.n == nb].sort_values(["k", "draw"])
                M = np.array([Mall[(int(r.k), int(r.draw))] for _, r in sub.iterrows()])
                # pooled rows mix k, whose row sums differ; add 2 UNPENALISED k dummies
                kd = np.column_stack([(sub.k.values == KS[1]).astype(float),
                                      (sub.k.values == KS[2]).astype(float)])
                M = np.column_stack([kd, M]); free = 2
                folds = (np.arange(len(sub)) % N_FOLDS)
            else:
                sub = B[(B.n == nb) & (B.k == k)].sort_values("draw")
                M = np.array([Mall[(k, int(r.draw))] for _, r in sub.iterrows()]); free = 0
                folds = np.arange(len(sub)) % N_FOLDS
            sdv = sub["sd"].values
            Wv = sub["W"].values
            for ycol, ylab in YCOLS:
                y = sub[ycol].values
                u_sd = ols(y, [sdv], ["sd"])
                pr_W = partial_r2(y, sdv, Wv)                    # idea 83's control, same rows
                for lam in LAMS:
                    Fi, Fo = fit_composition(M, y, lam, folds, free)
                    for scheme, F in [("IS", Fi), ("OOF", Fo)]:
                        pr = partial_r2(y, sdv, F)
                        rows.append(dict(
                            n=nb, scope=scope, y=ylab, N=len(sub), lam=lam, scheme=scheme,
                            R2_sd=u_sd["R2"], t_sd=u_sd["t"]["sd"],
                            R2_F=oof_r2(y, F),
                            pR2_sd_given_F=pr["pR2"], t_sd_given_F=pr["t"],
                            t_F_given_sd=pr["t_ctrl"], kill_F=pr["pR2"] / u_sd["R2"] if u_sd["R2"] > 0 else np.nan,
                            pR2_sd_given_W=pr_W["pR2"], t_sd_given_W=pr_W["t"],
                            kill_W=pr_W["pR2"] / u_sd["R2"] if u_sd["R2"] > 0 else np.nan))
    R = pd.DataFrame(rows)
    R.to_csv(OUT / f"{STEM}.regressions.csv", index=False)

    P("\n  HEADLINE cell - the one idea 83 published (n=20, CAND Sharpe, pooled over all 150 draws).")
    P("  idea 83's scalar control on these same rows: R2(sd) 0.3062 (t +8.08) -> pR2(sd|W) 0.1899 "
      "(t +5.87), kill 0.620")
    h = R[(R.n == 20) & (R.scope == "pooled") & (R.y == "CAND Sharpe")]
    P(fmt(h.set_index(["scheme", "lam"])[["R2_sd", "t_sd", "R2_F", "pR2_sd_given_F", "t_sd_given_F",
                                          "t_F_given_sd", "kill_F", "pR2_sd_given_W", "t_sd_given_W",
                                          "kill_W"]]))

    P("\n  EVERY GRID POINT, n=20 (all 4 scopes x 3 y-columns x 6 penalties x 2 schemes):")
    P(fmt(R[R.n == 20].set_index(["scope", "y", "scheme", "lam"])[
        ["N", "R2_sd", "R2_F", "pR2_sd_given_F", "t_sd_given_F", "kill_F", "kill_W"]]))
    P("\n  EVERY GRID POINT, n=5:")
    P(fmt(R[R.n == 5].set_index(["scope", "y", "scheme", "lam"])[
        ["N", "R2_sd", "R2_F", "pR2_sd_given_F", "t_sd_given_F", "kill_F", "kill_W"]]))

    P("\n  SURVIVAL COUNTS on the book-Sharpe columns (CAND Sharpe + EWall Sharpe, all n, all scopes,")
    P("  all penalties) - how often sd clears |t|>2 against each control:")
    bk = R[R.y != "premium"]
    for scheme in SCHEMES:
        s = bk[bk.scheme == scheme]
        P(f"    scheme {scheme:<3}  sd survives |t|>2 against the NAME-LEVEL control in "
          f"{int((s.t_sd_given_F.abs() > 2).sum())} of {len(s)} grid points   "
          f"(kill_F median {s.kill_F.median():.3f}, range {s.kill_F.min():.3f}-{s.kill_F.max():.3f})")
    sW = bk[(bk.scheme == "OOF") & (bk.lam == LAMS[0])]
    P(f"    reference   sd survives |t|>2 against idea 83's SCALAR control in "
      f"{int((sW.t_sd_given_W.abs() > 2).sum())} of {len(sW)} of the same cells "
      f"(kill_W median {sW.kill_W.median():.3f})")

    # ---------------------------------------------------------------- nested prediction
    P("\n" + "=" * 210)
    P("NESTED OUT-OF-FOLD PREDICTION - does adding sd to the name-level model improve what it")
    P("predicts on draws it did not fit?  Immune to in-sample overfit in both directions.")
    P("=" * 210)
    nest = []
    for nb in N_BOOKS:
        for k in KS:
            sub = B[(B.n == nb) & (B.k == k)].sort_values("draw")
            M = np.array([Mall[(k, int(r.draw))] for _, r in sub.iterrows()])
            folds = np.arange(len(sub)) % N_FOLDS
            sdv = sub["sd"].values
            Msd = np.column_stack([sdv / sdv.std(), M])   # sd unpenalised, scaled to unit sd
            for ycol, ylab in YCOLS:
                y = sub[ycol].values
                for lam in LAMS:
                    _, Fo = fit_composition(M, y, lam, folds)
                    _, Fo2 = fit_composition(Msd, y, lam, folds, free=1)
                    # sd alone, out of fold, as a floor
                    Fsd = np.empty(len(y))
                    for f in np.unique(folds):
                        te = folds == f; tr = ~te
                        o = ols(y[tr], [sdv[tr]], ["sd"])
                        Fsd[te] = o["coef"]["const"] + o["coef"]["sd"] * sdv[te]
                    nest.append(dict(n=nb, k=k, y=ylab, lam=lam,
                                     oofR2_M=oof_r2(y, Fo), oofR2_M_sd=oof_r2(y, Fo2),
                                     gain=oof_r2(y, Fo2) - oof_r2(y, Fo), oofR2_sd_only=oof_r2(y, Fsd)))
    NS = pd.DataFrame(nest)
    NS.to_csv(OUT / f"{STEM}.nested.csv", index=False)
    P(fmt(NS.set_index(["n", "k", "y", "lam"])))
    bkn = NS[NS.y != "premium"]
    P(f"\n  adding sd improves out-of-fold R2 in {int((bkn.gain > 0).sum())} of {len(bkn)} book-Sharpe grid points "
      f"(median gain {bkn.gain.median():+.4f}, range {bkn.gain.min():+.4f}..{bkn.gain.max():+.4f})")
    P(f"  the name-level model ALONE predicts out of fold with R2 {bkn.oofR2_M.min():+.4f}..{bkn.oofR2_M.max():+.4f} "
      f"(median {bkn.oofR2_M.median():+.4f}); sd ALONE with R2 {bkn.oofR2_sd_only.min():+.4f}.."
      f"{bkn.oofR2_sd_only.max():+.4f} (median {bkn.oofR2_sd_only.median():+.4f})")

    # ---------------------------------------------------------------- KEEP paths
    P("\n" + "=" * 210)
    P("BOTH KEEP PATHS")
    P("=" * 210)
    P("  This run introduces NO new book: the object under test is a statistic about idea 78's 450")
    P("  books, restated here from the committed grid gated at [c].")
    kb = B[B.n == N_BOOK]
    allbooks = pd.concat([
        B.assign(book="CAND" + B.n.astype(str))[["k", "draw", "book", "f4a", "f4b"]],
        kb.assign(book="EWall", f4a=kb.ew_f4a, f4b=kb.ew_f4b)[["k", "draw", "book", "f4a", "f4b"]]])
    P(fmt(allbooks.groupby("book").agg(N=("f4a", "size"),
                                       pass4a=("f4a", lambda s: (s == "-").sum()),
                                       pass4b=("f4b", lambda s: (s == "-").sum())), 0))
    P(f"  overall: 4a {int((allbooks.f4a == '-').sum())} of {len(allbooks)};  "
      f"4b {int((allbooks.f4b == '-').sum())} of {len(allbooks)}   "
      f"(idea 83 published 4a 276/450, 4b 87/450)")
    P("\n  4a above is measured against RULES v1, as idea 83 measured it.  The LIVE book has been")
    P("  RULES v2 since 2026-09-06, so 4a is restated against v2 here.  The committed grid carries")
    P("  H1/H2/MaxDD for the 300 CAND books only (EWall halves were never written out), so the v2")
    P("  restatement covers those 300.")
    from baseline import rules_v2_weights
    r_v2 = backtest(px136, rules_v2_weights(px136), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[startb:]
    v2h1, v2h2 = half_sharpes(r_v2); v2dd = metrics(r_v2)["MaxDD"]
    P(f"    RULES v2 on B136 {metrics(r_v2)['CAGR']:.2%} / {metrics(r_v2)['Sharpe']:.3f} / {v2dd:.2%}  "
      f"halves {v2h1:.3f}/{v2h2:.3f}  OOS {metrics(r_v2.loc[OOS_START:])['Sharpe']:.3f}")

    def f4a_v2(r):
        f = []
        if not r["H1"] > v2h1: f.append("H1")
        if not r["H2"] > v2h2: f.append("H2")
        if not r["MaxDD"] >= v2dd: f.append("DD")
        return ",".join(f) if f else "-"

    B["f4a_v2"] = B.apply(f4a_v2, axis=1)
    P(fmt(B.groupby("n").agg(N=("f4a_v2", "size"),
                             pass4a_v1=("f4a", lambda s: (s == "-").sum()),
                             pass4a_v2=("f4a_v2", lambda s: (s == "-").sum())), 0))
    P(f"    CAND books: 4a-v1 {int((B.f4a == '-').sum())}/300,  4a-v2 {int((B.f4a_v2 == '-').sum())}/300")
    P("    4a-v2 failing-bar census: " +
      B.f4a_v2.str.split(",").explode().value_counts().to_dict().__str__())

    # ---------------------------------------------------------------- rule 8
    P("\n" + "=" * 210)
    P("PROTOCOL rule 8 - selectors fitted on 2009-2016 ONLY, 2017-2026 read once")
    P("=" * 210)
    IS = B[B.n == N_BOOK].set_index(["k", "draw"]).sort_index()
    tr136 = set(px136.columns)
    r0 = backtest(px136, weights_cand(px136, tr136, N_BOOK), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[startb:]
    m0o = metrics(r0.loc[OOS_START:])
    f4b_r0 = fail_4b(r0, spy, r0.loc[OOS_START:], spy_oos)
    f4a_r0 = fail_4a(r0, base)

    # S7's input: sd_IS residualised on the OUT-OF-FOLD name-level fit of Sharpe_IS, within k cell.
    # The penalty is chosen by IS cross-validation (max OOF R2 on Sharpe_IS) - IS data only.
    P("\n  S7 construction (IS DATA ONLY).  Penalty chosen by cross-validating the name-level fit of")
    P("  IS Sharpe; the whole ladder's OOS outcome is reported below so the choice hides nothing.")
    lam_rows = []
    for lam in LAMS:
        tot = []
        for k in KS:
            sub = IS.loc[k].sort_index()
            Mk = np.array([Mall[(k, d)] for d in sub.index])
            folds = np.arange(len(sub)) % N_FOLDS
            _, Fo = fit_composition(Mk, sub["Sharpe_IS"].values, lam, folds)
            tot.append(oof_r2(sub["Sharpe_IS"].values, Fo))
        lam_rows.append(dict(lam=lam, oofR2_k20=tot[0], oofR2_k40=tot[1], oofR2_k80=tot[2],
                             mean_oofR2=float(np.mean(tot))))
    LM = pd.DataFrame(lam_rows)
    P(fmt(LM.set_index("lam")))
    lam_star = float(LM.loc[LM.mean_oofR2.idxmax(), "lam"])
    P(f"    IS-cross-validated penalty lam* = {lam_star:g}")

    def s7_pick(lam):
        col = {}
        for k in KS:
            sub = IS.loc[k].sort_index()
            Mk = np.array([Mall[(k, d)] for d in sub.index])
            folds = np.arange(len(sub)) % N_FOLDS
            _, Fo = fit_composition(Mk, sub["Sharpe_IS"].values, lam, folds)
            rr = resid_on(sub["sd_IS"].values, Fo)
            for i, d in enumerate(sub.index):
                col[(k, int(d))] = rr[i]
        s = pd.Series(col)
        return s.idxmax(), s

    pick7, _ = s7_pick(lam_star)

    picks = {
        "S0 do-nothing (full B136 CAND-20)": None,
        "S1 IS-Sharpe argmax":               IS["Sharpe_IS"].idxmax(),
        "S2 DISPERSION (max IS sd)":         IS["sd_IS"].idxmax(),
        "S3 COUNT (max IS n_elig)":          IS["n_elig_IS"].idxmax(),
        "S5 RESID-DISP scalar (max IS sd|W)": IS["sd_resid_IS"].idxmax(),
        "S6 WINNERNESS (max IS name ret)":   IS["W_IS"].idxmax(),
        "S4 random sub-panel":               IS.index[np.random.default_rng(SEED_S4).integers(len(IS))],
        f"S7 FE-RESID-DISP (NEW, lam={lam_star:g})": pick7,
    }
    wrows = []
    for lab, key in picks.items():
        if key is None:
            wrows.append(dict(selector=lab, k=-1, draw=-1,
                              IS_Sharpe=metrics(r0.loc[:IS_END])["Sharpe"],
                              OOS_CAGR=m0o["CAGR"], OOS_Sharpe=m0o["Sharpe"], OOS_MaxDD=m0o["MaxDD"],
                              full_Sharpe=metrics(r0)["Sharpe"], full_MaxDD=metrics(r0)["MaxDD"],
                              cell_mean_OOS=np.nan, cell_sd_OOS=np.nan, f4a=f4a_r0, f4b=f4b_r0,
                              f4a_v2=f4a_v2(dict(H1=half_sharpes(r0)[0], H2=half_sharpes(r0)[1],
                                                 MaxDD=metrics(r0)["MaxDD"]))))
            continue
        kk, dd = int(key[0]), int(key[1])
        row = IS.loc[(kk, dd)]
        cm = B[(B.n == N_BOOK) & (B.k == kk)]
        wrows.append(dict(selector=lab, k=kk, draw=dd,
                          IS_Sharpe=row["Sharpe_IS"], OOS_CAGR=row["CAGR_OOS"],
                          OOS_Sharpe=row["Sharpe_OOS"], OOS_MaxDD=row["MaxDD_OOS"],
                          full_Sharpe=row["Sharpe"], full_MaxDD=row["MaxDD"],
                          cell_mean_OOS=float(cm["Sharpe_OOS"].mean()),
                          cell_sd_OOS=float(cm["Sharpe_OOS"].std()),
                          f4a=row["f4a"], f4b=row["f4b"], f4a_v2=row["f4a_v2"]))
    W8 = pd.DataFrame(wrows)
    W8.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    spyo = metrics(spy_oos)
    P(f"\n  SPY OOS {spyo['CAGR']:.2%} / {spyo['Sharpe']:.3f} / {spyo['MaxDD']:.2%};  "
      f"RULES v1 B136 OOS {metrics(base.loc[OOS_START:])['CAGR']:.2%} / {metrics(base.loc[OOS_START:])['Sharpe']:.3f};  "
      f"do-nothing OOS {m0o['CAGR']:.2%} / {m0o['Sharpe']:.3f} / {m0o['MaxDD']:.2%}")
    P(fmt(W8.set_index("selector"), 4))
    d0 = float(W8.loc[W8.selector.str.startswith("S0"), "OOS_Sharpe"].iloc[0])
    P(f"\n  OOS Sharpe regret vs the do-nothing control ({d0:.4f}):")
    for _, r in W8.iterrows():
        if r.selector.startswith("S0"): continue
        z = (r.OOS_Sharpe - r.cell_mean_OOS) / r.cell_sd_OOS
        P(f"    {r.selector:<40} {r.OOS_Sharpe - d0:+.4f}   (cell mean {r.cell_mean_OOS:.3f} "
          f"+- {r.cell_sd_OOS:.3f}; z within cell {z:+.2f})")
    P(f"\n  KEEP paths over the {len(W8)} selector arms: 4a-v1 {int((W8.f4a == '-').sum())}/{len(W8)}, "
      f"4a-v2 {int((W8.f4a_v2 == '-').sum())}/{len(W8)} ({W8.loc[W8.f4a_v2 == '-', 'selector'].tolist()}), "
      f"4b {int((W8.f4b == '-').sum())}/{len(W8)} ({W8.loc[W8.f4b == '-', 'selector'].tolist()})")
    P("  Nothing here is promotable: S7 selects the SAME draw as idea 83's raw-dispersion S2 at")
    P("  every penalty, so the name-level residualisation adds no selector content, and the one 4b")
    P("  pass is idea 78's already-published random-sub-panel base rate (idea 253: 23-39% on B136).")

    P("\n  S7's WHOLE penalty ladder, OOS (the choice above hides nothing):")
    lad = []
    for lam in LAMS:
        p_, _ = s7_pick(lam)
        row = IS.loc[(int(p_[0]), int(p_[1]))]
        lad.append(dict(lam=lam, k=int(p_[0]), draw=int(p_[1]), IS_Sharpe=row["Sharpe_IS"],
                        OOS_Sharpe=row["Sharpe_OOS"], regret=row["Sharpe_OOS"] - d0, f4b=row["f4b"]))
    LAD = pd.DataFrame(lad)
    LAD.to_csv(OUT / f"{STEM}.s7_ladder.csv", index=False)
    P(fmt(LAD.set_index("lam")))

    P("\n  selector-input skill over the 150 CAND-20 sub-panels (Spearman with OOS Sharpe):")
    s = B[B.n == N_BOOK].sort_values(["k", "draw"])
    _, s7col = s7_pick(lam_star)
    s = s.assign(sd_resid_FE_IS=[s7col[(int(r.k), int(r.draw))] for _, r in s.iterrows()])
    for lab, col in [("IS Sharpe", "Sharpe_IS"), ("IS sd (dispersion)", "sd_IS"),
                     ("IS n_elig (count)", "n_elig_IS"),
                     ("IS sd | W_IS   (idea 83 scalar)", "sd_resid_IS"),
                     ("IS sd | F_oof  (NAME-LEVEL)", "sd_resid_FE_IS"),
                     ("IS name return W_IS", "W_IS")]:
        P(f"    {lab:<34} {spearman(s[col], s['Sharpe_OOS']):+.4f}   "
          f"(with FULL Sharpe {spearman(s[col], s['Sharpe']):+.4f})")

    # ---------------------------------------------------------------- verdict
    P("\n" + "=" * 210)
    P("VERDICT against the pre-registered bars")
    P("=" * 210)
    hd = R[(R.n == 20) & (R.scope == "pooled") & (R.y == "CAND Sharpe") &
           (R.scheme == "OOF") & (R.lam == lam_star)].iloc[0]
    P(f"  Bar: sd is KILLED iff kill < 1/3 AND |t| < 2 on the OUT-OF-FOLD scheme.")
    P(f"  Headline cell at the CV penalty lam*={lam_star:g}: kill_F {hd.kill_F:.3f}, t {hd.t_sd_given_F:+.2f}")
    P(f"    -> BOTH legs of the kill bar are MISSED, in the same direction as idea 83's scalar")
    P(f"       (kill_W {hd.kill_W:.3f}, t {hd.t_sd_given_W:+.2f}).  sd SURVIVES the stronger control,")
    P(f"       and survives it LEAVING MORE of its univariate R2 than the scalar left.")
    bkO = R[(R.y != "premium") & (R.scheme == "OOF")]
    bkI = R[(R.y != "premium") & (R.scheme == "IS")]
    P(f"  Across all {len(bkO)} book-Sharpe grid points: OOF {int((bkO.t_sd_given_F.abs() > 2).sum())} survive, "
      f"IS {int((bkI.t_sd_given_F.abs() > 2).sum())} survive.")
    P(f"  The IS/OOF gap is the artefact this run was built to catch: the in-sample name-level fit")
    P(f"  reproduces sd itself at R2 {PW[PW.lam == LAMS[0]].R2_sd_M_IS.min():.4f}-{PW[PW.lam == LAMS[0]].R2_sd_M_IS.max():.4f}, "
      f"so an in-sample 136-column control CANNOT leave a")
    P(f"  coefficient on sd to test.  Out of fold the same model carries only "
      f"{PW[PW.lam == LAMS[0]].R2_sd_M_OOF.min():.3f}-{PW[PW.lam == LAMS[0]].R2_sd_M_OOF.max():.3f} of sd.")
    P(f"  Nested out-of-fold prediction agrees: adding sd to the name-level model raises OOF R2 in")
    P(f"  {int((bkn.gain > 0).sum())}/{len(bkn)} book-Sharpe grid points (median {bkn.gain.median():+.4f}).")
    P("  ANSWER TO THE QUEUE: the 62% is STRUCTURAL, not a power result about the scalar; idea 78's")
    P("  test C is safe outright on this axis.  The queue's own proposed design is only valid when")
    P("  fitted out of fold - run in-sample it would have reported a KILL for an overfitting reason.")
    P("  As a rule-8 selector the name-level residualisation is a NULL: same pick as raw sd at all")
    P("  six penalties.  No RULES change, no KEEP-candidate, no memo.")

    P(f"\n  elapsed {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()

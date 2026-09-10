#!/usr/bin/env python3
"""Idea 485 (cloud, 2026-09-10) -- does `sd` still survive the PARTIAL t-test once the control
has DATA?

QUEUE 485: "idea 484 showed the name-additive control's out-of-fold R2 rises 0.20 -> 0.88 (B136)
and -0.08 -> 0.59 (SMALL484) between 50 and 500 draws per k cell, so idea 252's headline partial
test (kill 0.675 at t +6.19) was run against a control with almost no power.  Re-run idea 252's
OWN partial test -- kill = pR2(sd|F_oof)/R2(sd), its pre-registered bar kill < 1/3 AND |t| < 2 --
on the D=500 grid idea 484 committed, at every penalty.  Max 2 params (draws, panel)."

WHAT IS ACTUALLY BEING TESTED
  Idea 252 concluded that draw dispersion `sd` SURVIVES a 136-column name-membership control,
  leaving kill 0.675 of its univariate R2 at t +6.19.  Idea 484 then showed that at N=150 pooled
  rows the control is mostly shrinkage: its own out-of-fold R2 is +0.21 there and +0.88 at
  D=500.  A control that cannot predict the target cannot absorb a predictor of it, so idea
  252's survival is confounded with the control's power.
  H1 (the test)  Re-run idea 252's partial test verbatim on the SAME nested draws at every D on
        the ladder.  If `kill` and |t| fall monotonically as the control gains power, idea 252's
        headline is an N statement like idea 484's; if they are flat, `sd` carries information
        the name-additive design genuinely does not.
        FALSIFIABLE both ways, and the bar is idea 252's OWN, pre-registered, not re-chosen:
        sd is KILLED iff kill < 1/3 AND |t| < 2 on the OUT-OF-FOLD scheme.
  H2 (the power audit beside it)  Report the control's own out-of-fold R2, R2(sd ~ M) out of
        fold, and the effective degrees of freedom at each (D, lambda), so the reader can see
        whether the control has data at the point the verdict is read.
  H3 (the reference)  Idea 83's ONE-SCALAR control (W = the draw's mean full-sample annualised
        log return) is recomputed on the identical rows at every D.  If the scalar's kill is the
        one that moves with D, the record has been reading a power curve as a structure claim.
  H4 (live price)  A surviving partial coefficient is a claim that the part of `sd` ORTHOGONAL
        to name composition is informative.  Make it a chooser: rule 8, IS-only inputs, pick a
        sub-panel by the residualised statistic sd_perp = resid(sd_IS | F_oof) and compare it to
        picking on raw sd, on IS Sharpe, on the name-additive prediction, and to not choosing at
        all.  Score the chosen books out of sample ONCE.  BOTH KEEP paths on every book.

AXES, AND WHAT IS EVER SELECTED ON (PROTOCOL 4, "no more than 2 tuned parameters")
    P1 DRAWS  D in {50, 100, 150, 200, 300, 400, 500} per k cell.  The ladder is NESTED: draw d
              is the same name set at every D (generator seeded once per (panel, k)), so D=50 is
              idea 252's own 150 pooled rows and every larger D is a superset.
    P2 PANEL  B136 (P=136) | SMALL484 (P=483 tradable names, idea 484's own label).
  => 14 (D, panel) points.  At each: 6 penalties x 2 schemes (IS / OUT-OF-FOLD) x 3 targets
     (CAND Sharpe, EWall Sharpe, premium) x 2 book sizes x 4 scopes (pooled + 3 k cells).
     EVERY point is written to .regressions.csv -- 2,016 rows per panel-D pair set.
  REPORTED, NOT TUNED: k, the book sizes, the penalty ladder, the fold count and fold map, the
  gate, gross, cadence, the cost rungs, the 2009-2016/2017-2026 split, the selector set.
  Nothing is chosen by looking at an outcome except inside rule 8.

STATED LIMITATIONS
  * `sd`, the draw statistics and the book metrics at 10 bps are READ from idea 484's committed
    `.grid.csv.gz` and are not re-derived from prices for all 3,000 rows; what IS re-derived
    from prices, for every one of those rows, is the name MEMBERSHIP the design matrix is built
    from -- gate G3 recomputes `sd`, `sd_IS`, `n_elig`, `n_elig_IS` from the regenerated name
    sets and requires them to match the committed grid.  If the membership were wrong the design
    matrix would be wrong and the gate would fail.
  * SURVIVORSHIP: B136 and the small panel are CURRENT-constituent lists (research/universe_broad.json,
    data/SMALL_PANEL_README.md), so their LEVELS are biased upward.  Only within-panel contrasts
    (draw vs draw, model vs model, D vs D on the same rows) are load-bearing.  SMALL484 is idea
    484's panel and is carried here so the test is run on the grid the queue names; it therefore
    still contains the 44 names with max_1d_move >= 1.0 that this lane normally drops.
    THE LIVE LEG THEREFORE ALSO RUNS ON SMALL484, NOT ON THIS LANE'S USUAL SMALL439: the queue
    names idea 484's grid, that grid is SMALL484, and re-drawing 3,000 filtered books to move the
    live leg onto SMALL439 does not fit one run's compute budget.  SMALL439 is still built and its
    SPY / live-book reference rows are printed so the reader can see what the filter changes at
    the panel level; idea 487 (same day, same generator) priced SMALL439 selector books directly.
  * The small panel starts 2010, so its IS window is shorter than B136's.

GATES (run before any new number is read; a failure stops the run)
  G1 fast_backtest == engine.backtest on the drawn books used in the live leg.
  G2 the cost-rung identity r(c) = r(0) - turnover*c/1e4.
  G3 MEMBERSHIP: the regenerated name sets reproduce idea 484's committed `sd`, `sd_IS`,
     `n_elig`, `n_elig_IS` on all 3,000 rows of `.grid.csv.gz`.
  G4 IDEA 252's OWN NUMBER: at D=50, B136, n=20, CAND Sharpe, pooled, the test reproduces the
     published table -- R2(sd) 0.3062 (t +8.08); OOF lambda=2 pR2 0.2067, t +6.19, kill 0.675;
     IS lambda=0.5 kill 0.000 at t -0.10; idea 83's scalar kill_W 0.620 at t +5.87.
  G5 the D ladder is NESTED: the first 50 rows of each (panel, k) cell at D=500 are byte-identical
     to the D=50 rows.

Deterministic, standalone, no network.  Reads only committed artefacts + research/baseline.py.
Writes .console.txt .power.csv .regressions.csv .ladder.csv .grid.csv .walkforward.csv
       .keeppaths.csv
Modifies nothing (RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched).
fast_backtest() and the RidgeOOF nested-CV estimator are idea 484/487's, re-asserted in G1.
"""
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
from baseline import load_universe, rules_v2_weights, score                   # noqa: E402
from engine import backtest, metrics, rebalance_mask                          # noqa: E402

REF484 = OUT / "2026-09-09_does-one-dispersion-number-really-out-predict-136-name-dummies_C.grid.csv.gz"

# ---- idea 78/83/252/484's constants, imported verbatim (never tuned) --------------------------
FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
COST = 10.0
COSTRUNGS = [10.0, 25.0]
KS = [20, 40, 80]
N_BOOKS = [5, 20]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
SEED_B = 78_500
N_FOLDS = 10
LAMS = [0.5, 2.0, 8.0, 32.0, 128.0, 512.0]
DLADDER = [50, 100, 150, 200, 300, 400, 500]          # P1
D_MAX = 500
PANELS = ["B136", "SMALL484"]                          # P2
YCOLS = [("Sharpe", "CAND Sharpe"), ("ew_Sharpe", "EWall Sharpe"), ("premium", "premium")]
SELECTORS = ["S0 do-nothing", "S1 IS Sharpe", "S2 IS sd", "S3 IS sd_perp", "S4 pred M+sd"]
KILL_BAR, T_BAR = 1.0 / 3.0, 2.0                       # idea 83/252's bar, verbatim

_LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:+.4f}")


def dump(df, tag):
    p = OUT / f"{STEM}.{tag}.csv"
    df.to_csv(p, index=False)
    P(f"  [wrote {p.name}  {len(df)} rows]")


# ================================================================================================
# harness (idea 484/487's, gated against engine.backtest in G1)
# ================================================================================================
def fast_backtest(prices, weights, freq=FREQ):
    """Vectorised twin of engine.backtest at ZERO cost, plus the turnover path."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy()
    m[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(m)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return pd.Series((held * rets).sum(axis=1), index=idx), pd.Series(turn, index=idx)


def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


# ================================================================================================
# idea 252's regression helpers, imported verbatim
# ================================================================================================
def ols(y, X, names):
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
    return dict(R2=r2, n=len(y), resid=resid, coef=dict(zip(["const"] + names, beta)),
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
    X = np.asarray(X, float)
    y = np.asarray(y, float)
    xm = X.mean(axis=0)
    Xc = X - xm
    ym = y.mean()
    D = np.ones(Xc.shape[1]) * lam
    if free:
        D[:free] = 0.0
    beta = np.linalg.solve(Xc.T @ Xc + np.diag(D), Xc.T @ (y - ym))
    return ym, xm, beta


def ridge_predict(X, ym, xm, beta):
    return ym + (np.asarray(X, float) - xm) @ beta


def ridge_edf(X, lam, free=0):
    X = np.asarray(X, float)
    Xc = X - X.mean(axis=0)
    D = np.ones(Xc.shape[1]) * lam
    if free:
        D[:free] = 0.0
    return 1.0 + float(np.trace(Xc @ np.linalg.solve(Xc.T @ Xc + np.diag(D), Xc.T)))


def fit_composition(M, y, lam, folds, free=0):
    ym, xm, beta = ridge_fit(M, y, lam, free)
    F_is = ridge_predict(M, ym, xm, beta)
    F_oof = np.empty(len(y))
    for f in np.unique(folds):
        te = folds == f
        tr = ~te
        ym_, xm_, b_ = ridge_fit(M[tr], y[tr], lam, free)
        F_oof[te] = ridge_predict(M[te], ym_, xm_, b_)
    return F_is, F_oof


def oof_r2(y, pred):
    y = np.asarray(y, float)
    ss = float(((y - y.mean()) ** 2).sum())
    return 1.0 - float(((y - pred) ** 2).sum()) / ss if ss > 0 else np.nan


def cv_lambda(M, y, folds, free=0):
    """Idea 252's lambda*: the penalty with the best out-of-fold R2 on these rows."""
    best, bl = -np.inf, LAMS[0]
    for lam in LAMS:
        _, Fo = fit_composition(M, y, lam, folds, free)
        s = oof_r2(y, Fo)
        if s > best:
            best, bl = s, lam
    return bl, best


# ================================================================================================
# panels, draws, membership
# ================================================================================================
def panel_defs():
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    pxk = pxs[[c for c in pxs.columns if c == "SPY" or c not in bad]]
    P(f"    SMALL panel: {len([c for c in pxs.columns if c != 'SPY'])} names cached; "
      f"{len(bad & set(pxs.columns))} have max_1d_move >= 1.0 -> SMALL439 has "
      f"{len([c for c in pxk.columns if c != 'SPY'])} tradable")
    return {
        "B136": (px136, list(px136.columns)),                        # idea 78: SPY tradable
        "SMALL484": (pxs, [c for c in pxs.columns if c != "SPY"]),   # idea 484's panel
        "SMALL439": (pxk, [c for c in pxk.columns if c != "SPY"]),   # this lane's filtered panel
    }


def draw_names(names, k, n_draws, seed):
    """Draw d is the d-th name set from the generator seeded once per (panel, k) -- idea 484's
    construction, unchanged, so the ladder is NESTED by construction."""
    rng = np.random.default_rng(seed)
    return [list(rng.choice(names, size=k, replace=False)) for _ in range(n_draws)]


def draw_stats(px, cols, startb):
    """sd / n_elig for one drawn name set -- the quantities gate G3 checks against idea 484."""
    keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px.columns else [])))
    p = px[keep].dropna(how="all").ffill()
    s, above, vol20 = score(p, vol_scale=False)
    elig = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in p.columns if c not in set(cols)]
    if drop:
        elig[drop] = False
    wm = rebalance_mask(p.index, FREQ).values
    ne = elig[wm].sum(axis=1).loc[startb:]
    mom_p = (p[cols].shift(21) / p[cols].shift(252) - 1).where(elig[cols])
    sdw = mom_p[wm].loc[startb:].std(axis=1)
    return dict(n_elig=float(ne.mean()), sd=float(sdw.mean()),
                n_elig_IS=float(ne.loc[:IS_END].mean()), sd_IS=float(sdw.loc[:IS_END].mean()))


def draw_book(px, cols, nb, startb):
    """The CAND-nb book of one drawn sub-panel: (zero-cost returns, turnover), from startb."""
    keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px.columns else [])))
    p = px[keep].dropna(how="all").ffill()
    s, above, vol20 = score(p, vol_scale=False)
    elig = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in p.columns if c not in set(cols)]
    if drop:
        elig[drop] = False
    rank = s.where(elig).rank(axis=1, ascending=False)
    w = (rank <= nb).astype(float) * (GROSS / nb)
    r0, tu = fast_backtest(p, w)
    return r0.loc[startb:], tu.loc[startb:], w, p


def ann_logret(p):
    out = {}
    for c in p.columns:
        s = p[c].dropna()
        if len(s) < 252 or s.iloc[0] <= 0:
            out[c] = np.nan
            continue
        yrs = (s.index[-1] - s.index[0]).days / 365.25
        out[c] = float(np.log(s.iloc[-1] / s.iloc[0]) / yrs)
    return pd.Series(out)


# ================================================================================================
# MAIN
# ================================================================================================
def main():
    t00 = time.time()
    P("=" * 118)
    P("IDEA 485 (cloud, 2026-09-10) -- does `sd` still survive the PARTIAL t-test once the "
      "control has DATA?")
    P("Idea 252's own test, its own bar, on idea 484's own nested D=500 draws.")
    P("=" * 118)

    PXD = panel_defs()
    ctx = {}
    for pan, (px, names) in PXD.items():
        startb = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[startb:]
        bw = rules_v2_weights(px)
        b0, bt = fast_backtest(px, bw)
        b0, bt = b0.loc[startb:], bt.loc[startb:]
        lr = ann_logret(px[names].loc[startb:])
        ctx[pan] = dict(px=px, names=names, startb=startb, spy=spy, b0=b0, bt=bt, lr=lr)
        ms = metrics(spy)
        s1, s2 = half_sharpes(spy)
        P(f"    {pan:<9} {len(names)} tradable names, {startb.date()} -> {px.index[-1].date()}"
          f"   SPY {ms['CAGR']:.2%} / {ms['Sharpe']:.3f} / {ms['MaxDD']:.2%} "
          f"halves {s1:.3f}/{s2:.3f} OOS {metrics(spy.loc[OOS_START:])['Sharpe']:.3f}")

    # ---------------------------------------------------------------- the committed grid
    P()
    P("=" * 118)
    P("(A) THE GRID -- idea 484's committed D=500 draws")
    P("=" * 118)
    if not REF484.exists():
        P(f"  ABORT: {REF484.name} not found -- the queue's premise is unauditable.")
        return
    G484 = pd.read_csv(REF484)
    P(f"  {REF484.name}: {G484.shape[0]} rows x {G484.shape[1]} columns")
    P(f"  cells: {G484.groupby(['panel','k']).size().to_dict()}")

    # ---------------------------------------------------------------- G3 membership gate
    P()
    P("=" * 118)
    P("(G3) MEMBERSHIP GATE -- the regenerated name sets must reproduce idea 484's own draw")
    P("     statistics on every one of its 3,000 rows, or the design matrix is not its design.")
    P("=" * 118)
    NAMES = {}
    MEM = {}
    t0 = time.time()
    gate_rows = []
    for pan in PANELS:
        c = ctx[pan]
        idxn = {nm: i for i, nm in enumerate(c["names"])}
        for k in KS:
            dn = draw_names(c["names"], k, D_MAX, SEED_B + k)
            NAMES[(pan, k)] = dn
            Mk = np.zeros((D_MAX, len(c["names"])))
            for d, cols in enumerate(dn):
                for nm in cols:
                    Mk[d, idxn[nm]] = 1.0
            MEM[(pan, k)] = Mk
            ref = G484[(G484.panel == pan) & (G484.k == k)].sort_values("draw")
            worst = {}
            for _, r in ref.iterrows():
                got = draw_stats(c["px"], dn[int(r.draw)], c["startb"])
                for col, v in got.items():
                    worst[col] = max(worst.get(col, 0.0), abs(v - float(r[col])))
            gate_rows.append(dict(panel=pan, k=k, n=len(ref), **worst))
    GT = pd.DataFrame(gate_rows)
    P(fmt(GT.set_index(["panel", "k"])))
    statcols = ["n_elig", "sd", "n_elig_IS", "sd_IS"]
    g3max = float(GT[statcols].to_numpy().max())
    g3 = g3max < 1e-9
    P(f"  G3 max abs difference over {int(GT.n.sum())} rows x 4 columns : {g3max:.3e}   "
      f"{'PASS -- M is idea 484s own membership matrix' if g3 else 'FAIL'}")
    P(f"  ({time.time()-t0:.0f}s)")
    if not g3:
        P("  ABORT on G3.")
        return

    # G5 nestedness
    nest = True
    for pan in PANELS:
        for k in KS:
            dn = NAMES[(pan, k)]
            dn50 = draw_names(ctx[pan]["names"], k, 50, SEED_B + k)
            nest &= all(dn[i] == dn50[i] for i in range(50))
    P(f"  G5 the D ladder is NESTED (the first 50 name sets at D=500 are the D=50 sets)   "
      f"{'PASS' if nest else 'FAIL'}")

    # ---------------------------------------------------------------- W, idea 83's scalar
    for pan in PANELS:
        c = ctx[pan]
        for k in KS:
            c.setdefault("W", {})[k] = np.array([float(c["lr"][cols].mean())
                                                 for cols in NAMES[(pan, k)]])

    # ---------------------------------------------------------------- (B) THE POWER AUDIT
    P()
    P("=" * 118)
    P("(B) POWER AUDIT -- does the control have data at the point the verdict is read?")
    P("    R2_F_oof     : the name-additive model's OWN out-of-fold R2 on the target")
    P("    R2_sd_M_oof  : how much of `sd` the name-additive model genuinely carries out of fold")
    P("    edf          : trace(H), the fit's effective degrees of freedom")
    P("=" * 118)
    prows = []
    for pan in PANELS:
        for D in DLADDER:
            sub = G484[(G484.panel == pan)].copy()
            Ms, ys, sds, folds = [], [], [], []
            for k in KS:
                s = sub[(sub.k == k) & (sub.draw < D)].sort_values("draw")
                Ms.append(MEM[(pan, k)][:D])
                ys.append(s["Sharpe20"].values)
                sds.append(s["sd"].values)
            M = np.vstack(Ms)
            kd = np.concatenate([np.full(D, i) for i in range(3)])
            KD = np.column_stack([(kd == 1).astype(float), (kd == 2).astype(float)])
            M = np.column_stack([KD, M])
            y = np.concatenate(ys)
            sdv = np.concatenate(sds)
            fold = np.arange(len(y)) % N_FOLDS
            for lam in LAMS:
                Fi, Fo = fit_composition(M, y, lam, fold, free=2)
                Si, So = fit_composition(M, sdv, lam, fold, free=2)
                prows.append(dict(panel=pan, D=D, N=len(y), lam=lam,
                                  R2_F_is=oof_r2(y, Fi), R2_F_oof=oof_r2(y, Fo),
                                  R2_sd_M_is=oof_r2(sdv, Si), R2_sd_M_oof=oof_r2(sdv, So),
                                  edf=ridge_edf(M, lam, free=2)))
    PW = pd.DataFrame(prows)
    dump(PW, "power")
    P(fmt(PW[PW.lam.isin([0.5, 2.0, 32.0, 512.0])].set_index(["panel", "D", "lam"])[
        ["N", "R2_F_oof", "R2_sd_M_oof", "edf"]]))

    # ---------------------------------------------------------------- (C) THE TEST
    P()
    P("=" * 118)
    P("(C) THE TEST -- idea 252's partial test at every (D, panel, penalty, scheme, target, "
      "book size, scope)")
    P("    BAR (idea 83/252's, verbatim, pre-registered): sd is KILLED iff")
    P("        kill = pR2(sd | F_oof) / R2(sd) < 1/3   AND   |t(sd | F_oof)| < 2")
    P("=" * 118)
    rows = []
    t0 = time.time()
    for pan in PANELS:
        for D in DLADDER:
            for nb in N_BOOKS:
                for scope, k in [("pooled", None)] + [(f"k={kk}", kk) for kk in KS]:
                    if k is None:
                        Ms, folds = [], None
                        parts = []
                        for kk in KS:
                            s = G484[(G484.panel == pan) & (G484.k == kk)
                                     & (G484.draw < D)].sort_values("draw")
                            parts.append(s)
                            Ms.append(MEM[(pan, kk)][:D])
                        sub = pd.concat(parts, ignore_index=True)
                        M = np.vstack(Ms)
                        kd = np.concatenate([np.full(D, i) for i in range(3)])
                        M = np.column_stack([(kd == 1).astype(float), (kd == 2).astype(float), M])
                        free = 2
                        Wv = np.concatenate([ctx[pan]["W"][kk][:D] for kk in KS])
                    else:
                        sub = G484[(G484.panel == pan) & (G484.k == k)
                                   & (G484.draw < D)].sort_values("draw").reset_index(drop=True)
                        M = MEM[(pan, k)][:D]
                        free = 0
                        Wv = ctx[pan]["W"][k][:D]
                    fold = np.arange(len(sub)) % N_FOLDS
                    sdv = sub["sd"].values
                    for ycol, ylab in YCOLS:
                        col = {"Sharpe": f"Sharpe{nb}", "ew_Sharpe": "ew_Sharpe",
                               "premium": f"premium{nb}"}[ycol]
                        y = sub[col].values
                        u = ols(y, [sdv], ["sd"])
                        prW = partial_r2(y, sdv, Wv)
                        lstar, lstar_r2 = cv_lambda(M, y, fold, free)
                        for lam in LAMS:
                            Fi, Fo = fit_composition(M, y, lam, fold, free)
                            for scheme, F in (("IS", Fi), ("OOF", Fo)):
                                pr = partial_r2(y, sdv, F)
                                rows.append(dict(
                                    panel=pan, D=D, n=nb, scope=scope, y=ylab, N=len(sub),
                                    lam=lam, lam_star=lstar, scheme=scheme,
                                    R2_sd=u["R2"], t_sd=u["t"]["sd"], R2_F=oof_r2(y, F),
                                    pR2_sd_given_F=pr["pR2"], t_sd_given_F=pr["t"],
                                    t_F_given_sd=pr["t_ctrl"],
                                    kill_F=pr["pR2"] / u["R2"] if u["R2"] > 0 else np.nan,
                                    pR2_sd_given_W=prW["pR2"], t_sd_given_W=prW["t"],
                                    kill_W=prW["pR2"] / u["R2"] if u["R2"] > 0 else np.nan))
    R = pd.DataFrame(rows)
    R["killed"] = (R.kill_F < KILL_BAR) & (R.t_sd_given_F.abs() < T_BAR)
    dump(R, "regressions")
    P(f"  {len(R)} grid points in {time.time()-t0:.0f}s")

    # -- G4: idea 252's own number ------------------------------------------------------------
    P()
    P("  G4 -- IDEA 252's OWN NUMBER at D=50 (its 150 pooled B136 rows), n=20, CAND Sharpe:")
    h = R[(R.panel == "B136") & (R.D == 50) & (R.n == 20) & (R.scope == "pooled")
          & (R.y == "CAND Sharpe")]
    P(fmt(h.set_index(["scheme", "lam"])[["N", "R2_sd", "t_sd", "R2_F", "pR2_sd_given_F",
                                          "t_sd_given_F", "kill_F", "kill_W", "t_sd_given_W"]]))
    o2 = h[(h.scheme == "OOF") & (h.lam == 2.0)].iloc[0]
    i05 = h[(h.scheme == "IS") & (h.lam == 0.5)].iloc[0]
    checks = [("R2(sd) 0.3062", abs(o2.R2_sd - 0.3062), 5e-4),
              ("t(sd) +8.08", abs(o2.t_sd - 8.08), 5e-3),
              ("OOF lam=2 pR2 0.2067", abs(o2.pR2_sd_given_F - 0.2067), 5e-4),
              ("OOF lam=2 t +6.19", abs(o2.t_sd_given_F - 6.19), 5e-3),
              ("OOF lam=2 kill 0.675", abs(o2.kill_F - 0.675), 5e-4),
              ("IS lam=0.5 kill 0.000", abs(i05.kill_F - 0.000), 5e-4),
              ("IS lam=0.5 t -0.10", abs(i05.t_sd_given_F + 0.10), 5e-3),
              ("scalar kill_W 0.620", abs(o2.kill_W - 0.620), 5e-4),
              ("scalar t_W +5.87", abs(o2.t_sd_given_W - 5.87), 5e-3)]
    g4 = True
    for lab, d, bar in checks:
        P(f"     {lab:<26} |d| {d:.3e}  bar {bar:.0e}  {'PASS' if d < bar else 'FAIL'}")
        g4 &= d < bar
    P(f"  G4 {'PASS -- the test is idea 252s test' if g4 else 'FAIL'}")

    # -- the ladder ---------------------------------------------------------------------------
    P()
    P("  THE LADDER -- idea 252's headline cell (n=20, CAND Sharpe, pooled) at every D,")
    P("  read at the OUT-OF-FOLD scheme, at lambda=2 (idea 252's lambda*) and at each D's own")
    P("  IS-cross-validated lambda*:")
    lad = []
    for pan in PANELS:
        for D in DLADDER:
            s = R[(R.panel == pan) & (R.D == D) & (R.n == 20) & (R.scope == "pooled")
                  & (R.y == "CAND Sharpe") & (R.scheme == "OOF")]
            a = s[s.lam == 2.0].iloc[0]
            b = s[s.lam == s.lam_star].iloc[0]
            lad.append(dict(panel=pan, D=D, N=a.N, R2_sd=a.R2_sd, t_sd=a.t_sd,
                            lam2_R2_F=a.R2_F, lam2_pR2=a.pR2_sd_given_F, lam2_t=a.t_sd_given_F,
                            lam2_kill=a.kill_F,
                            lam_star=b.lam, ls_R2_F=b.R2_F, ls_t=b.t_sd_given_F, ls_kill=b.kill_F,
                            kill_W=a.kill_W, t_W=a.t_sd_given_W,
                            killed_lam2=bool(a.kill_F < KILL_BAR and abs(a.t_sd_given_F) < T_BAR),
                            killed_lamstar=bool(b.kill_F < KILL_BAR and abs(b.t_sd_given_F) < T_BAR)))
    L = pd.DataFrame(lad)
    dump(L, "ladder")
    P(fmt(L.set_index(["panel", "D"])))

    P()
    P("  SURVIVAL COUNTS on the book-Sharpe targets (CAND + EWall Sharpe, both n, all scopes,")
    P("  all penalties), OUT-OF-FOLD scheme -- how often sd clears |t| > 2 against the control:")
    bk = R[(R.y != "premium") & (R.scheme == "OOF")]
    for pan in PANELS:
        for D in DLADDER:
            s = bk[(bk.panel == pan) & (bk.D == D)]
            P(f"    {pan:<9} D={D:<4} sd survives |t|>2 in {int((s.t_sd_given_F.abs()>2).sum()):>3}"
              f" of {len(s):<3}   kill_F median {s.kill_F.median():+.3f} "
              f"[{s.kill_F.min():+.3f}, {s.kill_F.max():+.3f}]   "
              f"KILLED by the full bar {int(s.killed.sum()):>3}/{len(s)}")
    P()
    P("  the same on the PREMIUM target (idea 83 already showed it was near-nil):")
    pm = R[(R.y == "premium") & (R.scheme == "OOF")]
    for pan in PANELS:
        for D in [50, 500]:
            s = pm[(pm.panel == pan) & (pm.D == D)]
            P(f"    {pan:<9} D={D:<4} survives {int((s.t_sd_given_F.abs()>2).sum()):>3} of {len(s)}"
              f"   kill_F median {s.kill_F.median():+.3f}   KILLED {int(s.killed.sum())}/{len(s)}")

    # ---------------------------------------------------------------- (D) LIVE LEG
    P()
    P("=" * 118)
    P("(D) LIVE LEG -- rule 8.  Every selector input is computed on 2009-2016 ONLY; 2017-01-01..")
    P("    is read ONCE.  S3 is the surviving partial coefficient made a chooser: pick the draw")
    P("    with the largest sd_IS residualised on the IS-fitted out-of-fold name-composition.")
    P("=" * 118)
    live = []
    t0 = time.time()
    for pan in PANELS:
        c = ctx[pan]
        for k in KS:
            dn = NAMES[(pan, k)]
            Mk = MEM[(pan, k)]
            stats = G484[(G484.panel == pan) & (G484.k == k)].sort_values("draw")
            fold = np.arange(D_MAX) % N_FOLDS
            for nb in N_BOOKS:
                # IS-ONLY inputs, read off idea 484's committed grid (G3 gates the membership)
                isS = stats[f"Sharpe_IS{nb}"].values
                sd_is = stats["sd_IS"].values
                lstar, _ = cv_lambda(Mk, isS, fold, 0)
                _, Fo = fit_composition(Mk, isS, lstar, fold, 0)
                Msd = np.column_stack([sd_is, Mk])
                lstar2, _ = cv_lambda(Msd, isS, fold, 1)
                _, Fo_msd = fit_composition(Msd, isS, lstar2, fold, 1)
                sd_perp = resid_on(sd_is, Fo)                       # THE H4 STATISTIC
                picks = {"S1 IS Sharpe": int(np.argmax(isS)), "S2 IS sd": int(np.argmax(sd_is)),
                         "S3 IS sd_perp": int(np.argmax(sd_perp)),
                         "S4 pred M+sd": int(np.argmax(Fo_msd))}
                for sel, d in [("S0 do-nothing", -1)] + list(picks.items()):
                    cols = c["names"] if d < 0 else dn[d]
                    r0, tu, _, _ = draw_book(c["px"], cols, nb, c["startb"])
                    for cst in COSTRUNGS:
                        r = r0 - tu * cst / 1e4
                        b = c["b0"] - c["bt"] * cst / 1e4
                        m = metrics(r)
                        h1, h2 = half_sharpes(r)
                        oo = r.loc[OOS_START:]
                        mo = metrics(oo)
                        mb = metrics(b)
                        bh1, bh2 = half_sharpes(b)
                        ms = metrics(c["spy"])
                        sh1, sh2 = half_sharpes(c["spy"])
                        k4a = (h1 > bh1) and (h2 > bh2) and (m["MaxDD"] >= mb["MaxDD"])
                        k4b = (h1 > sh1 and h2 > sh2
                               and mo["Sharpe"] > metrics(c["spy"].loc[OOS_START:])["Sharpe"]
                               and m["MaxDD"] >= 0.60 * ms["MaxDD"]
                               and m["CAGR"] >= 0.70 * ms["CAGR"])
                        live.append(dict(panel=pan, k=k, n=nb, cost=cst, selector=sel,
                                         draw=d, lam_star=lstar,
                                         CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                         H1=h1, H2=h2, IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                                         OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                         OOS_MaxDD=mo["MaxDD"],
                                         base_Sharpe=mb["Sharpe"], base_MaxDD=mb["MaxDD"],
                                         base_OOS_Sharpe=metrics(b.loc[OOS_START:])["Sharpe"],
                                         spy_CAGR=ms["CAGR"], spy_Sharpe=ms["Sharpe"],
                                         spy_MaxDD=ms["MaxDD"],
                                         spy_OOS_Sharpe=metrics(
                                             c["spy"].loc[OOS_START:])["Sharpe"],
                                         keep_4a=k4a, keep_4b=k4b))
        P(f"    {pan:<9} done  ({time.time()-t0:.0f}s cumulative)")
    LV = pd.DataFrame(live)
    dump(LV, "grid")

    # G1/G2 on a live book
    P()
    P("=" * 118)
    P("(G) GATES G1 / G2")
    P("=" * 118)
    c = ctx["B136"]
    cols = NAMES[("B136", 20)][0]
    r0, tu, w, p = draw_book(c["px"], cols, 20, c["startb"])
    e10 = backtest(p, w, cost_bps=10.0, freq=FREQ)["returns"].loc[c["startb"]:]
    d1 = float(np.abs((r0 - tu * 10 / 1e4) - e10).max())
    e25 = backtest(p, w, cost_bps=25.0, freq=FREQ)["returns"].loc[c["startb"]:]
    d2 = float(np.abs((r0 - tu * 25 / 1e4) - e25).max())
    P(f"  G1 fast_backtest == engine.backtest (10 bps)   max|d| {d1:.3e}   "
      f"{'PASS' if d1 < 1e-12 else 'FAIL'}")
    P(f"  G2 cost-rung identity at 25 bps                max|d| {d2:.3e}   "
      f"{'PASS' if d2 < 1e-12 else 'FAIL'}")

    # ---------------------------------------------------------------- walkforward summary
    P()
    P("  RULE 8 -- OOS (2017-01-01..) by selector, pooled over k and n:")
    wf = LV.groupby(["panel", "cost", "selector"]).agg(
        OOS_CAGR=("OOS_CAGR", "median"), OOS_Sharpe=("OOS_Sharpe", "median"),
        OOS_MaxDD=("OOS_MaxDD", "median"), Sharpe=("Sharpe", "median"),
        MaxDD=("MaxDD", "median"),
        beats_base=("OOS_Sharpe", lambda s: np.nan),
        n=("OOS_Sharpe", "size")).reset_index()
    LV["beats_base"] = LV.OOS_Sharpe > LV.base_OOS_Sharpe
    LV["beats_spy"] = LV.OOS_Sharpe > LV.spy_OOS_Sharpe
    wf = LV.groupby(["panel", "cost", "selector"]).agg(
        n=("OOS_Sharpe", "size"), OOS_CAGR=("OOS_CAGR", "median"),
        OOS_Sharpe=("OOS_Sharpe", "median"), OOS_MaxDD=("OOS_MaxDD", "median"),
        beats_base=("beats_base", "sum"), beats_spy=("beats_spy", "sum"),
        k4a=("keep_4a", "sum"), k4b=("keep_4b", "sum")).reset_index()
    dump(wf, "walkforward")
    P(fmt(wf.set_index(["panel", "cost", "selector"])))

    P()
    P("  the reference rows on the same windows:")
    ref = LV.groupby("panel").agg(base_OOS=("base_OOS_Sharpe", "first"),
                                  spy_OOS=("spy_OOS_Sharpe", "first"),
                                  spy_CAGR=("spy_CAGR", "first"),
                                  spy_MaxDD=("spy_MaxDD", "first")).reset_index()
    P(fmt(ref.set_index("panel")))

    P()
    P("-" * 118)
    P("  KEEP PATHS over every scored book")
    P("-" * 118)
    P(f"  books priced : {len(LV)}")
    P(f"  4a passes    : {int(LV.keep_4a.sum())} / {len(LV)}")
    P(f"  4b passes    : {int(LV.keep_4b.sum())} / {len(LV)}")
    P(f"  BOTH         : {int((LV.keep_4a & LV.keep_4b).sum())} / {len(LV)}")
    for pan, s in LV.groupby("panel"):
        P(f"    {pan:<9} 4a {int(s.keep_4a.sum()):>3}/{len(s):<3}  4b {int(s.keep_4b.sum()):>3}"
          f"/{len(s):<3}  BOTH {int((s.keep_4a & s.keep_4b).sum()):>3}")
    if int(LV.keep_4b.sum()):
        P()
        P("  the 4b passers:")
        P(LV[LV.keep_4b][["panel", "k", "n", "cost", "selector", "CAGR", "Sharpe", "MaxDD",
                          "H1", "H2", "OOS_Sharpe", "spy_CAGR", "spy_MaxDD"]].to_string(
            index=False, float_format=lambda x: f"{x:.4f}"))
    kp = LV[["panel", "k", "n", "cost", "selector", "keep_4a", "keep_4b"]]
    dump(kp, "keeppaths")

    P()
    P("=" * 118)
    P(f"  GATES: G1 {'PASS' if d1 < 1e-12 else 'FAIL'}  G2 {'PASS' if d2 < 1e-12 else 'FAIL'}  "
      f"G3 {'PASS' if g3 else 'FAIL'} ({g3max:.3e})  G4 {'PASS' if g4 else 'FAIL'}  "
      f"G5 {'PASS' if nest else 'FAIL'}")
    P(f"  total {time.time()-t00:.0f}s")
    P("=" * 118)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()

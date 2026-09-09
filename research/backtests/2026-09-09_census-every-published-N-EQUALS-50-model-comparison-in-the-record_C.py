#!/usr/bin/env python3
"""Idea 486 - census-every-published-N-EQUALS-50-model-comparison-in-the-record  (lane C, 2026-09-09)

THE QUESTION
  Idea 484 found that a 136-parameter ridge and a 2-parameter line, compared at N=50 rows,
  report an ordering that reverses at N=100 and inverts by 0.60 of out-of-fold R2 at N=500,
  with the low-dimensional side FLAT across the whole ladder.  The queue asks: how much of the
  record is exposed to that?  Census every model-vs-model comparison decided at N <= 100 rows
  where the two sides differ by more than ~10 fitted parameters, and re-read each at the
  largest N its own panel can supply.

TWO TUNED PARAMETERS (the queue's own, both census axes, every grid point reported)
  N floor      Nfloor in {50, 75, 100, 150}
  parameter gap G     in {2, 5, 10, 20}      (a pair is in scope iff  gap > G  and  N <= Nfloor)
  Panel and the draw ladder D are NOT tuned: they are reporting axes, every point published.

WHAT IS A "COMPARISON" (pre-registered, before any count was read)
  A pair of model specifications whose fit statistics are published side by side in the same
  table or sentence, scored on the SAME target and the SAME rows.  p = fitted parameters
  including the intercept.  N = rows the comparison was decided on.  Every published spec set
  found by the scan contributes all of its unordered pairs.

STRUCTURE
  Stage 0  gates - engine baselines, the vectorised backtester, this run's draws against idea
           484's committed grid, and idea 252's own published D=50 numbers.
  Stage 1  CENSUS - a mechanical scan of every committed .py under research/ (idea 483's own
           regexes, whose four counts are reproduced as gate [e]), then a comparison table built
           from committed OUTPUT files wherever a spec/parameter column exists, plus three
           hand-adjudicated entries whose evidence line is recorded in the census CSV.
  Stage 2  RE-READ - every in-scope comparison at the largest N its own panel can supply.
           2a the wide class: idea 252/484's draw ladder extended to D=1000 per k cell (20x idea
              252's N, 2x idea 484's), both panels.  Books for draws 0..499 are idea 484's
              committed grid (gate [c] re-runs 25 draws per cell fresh and requires 0); draws
              500..999 are run here.
           2b everything else: the largest N present in the file's own committed output.
  Stage 3  BOTH KEEP PATHS on all 6,000 books.
  Stage 4  RULE 8 walk-forward, selectors fitted on 2009-2016, 2017-2026 read once.

Costs 10 bps, weekly, next-day execution, no shorting, no leverage.  Deterministic.
RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py are NOT modified by this script.
"""
import sys, time, re, json, itertools
from pathlib import Path
import numpy as np, pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
sys.path.insert(0, str(REPO / "products" / "backtester"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa
from engine import backtest, metrics, rebalance_mask                          # noqa

# ---- idea 78/83/252/484's constants, imported verbatim ----------------------------
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

# ---- this run's census axes (the two tuned parameters) ---------------------------
NFLOORS = [50, 75, 100, 150]
GAPS = [2, 5, 10, 20]

# ---- the re-read ladder (reporting axis, every point published) -------------------
D_REF = 500                       # idea 484's max, and the extent of its committed grid
D_MAX = 1000                      # this run's max
DRAWS = [50, 100, 200, 500, 750, 1000]
PANELS = ["B136", "SMALL484"]

SCRIPT = Path(__file__).name
OUT = REPO / "research" / "backtests"
STEM = SCRIPT[:-3]
REF484 = OUT / "2026-09-09_does-one-dispersion-number-really-out-predict-136-name-dummies_C.grid.csv.gz"
REF483 = OUT / "2026-09-09_which-published-residualisations-are-IN-SAMPLE-fits_cloud.census.csv"

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


# ================================================================== book helpers (idea 78/484's)
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


# ================================================================== regression helpers (idea 252's)
def ols(y, X, names):
    y = np.asarray(y, float)
    X = np.column_stack([np.ones(len(y))] + [np.asarray(c, float) for c in X])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    dof = max(len(y) - X.shape[1], 1)
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
    d = np.full(A.shape[0], float(lam))
    if free: d[:free] = 0.0
    return np.linalg.solve(A + np.diag(d), Xc.T @ (Y - ym))


def oof_paths(M, Y, folds, lams, free=0, inner_k=5):
    """Idea 252/484's estimator verbatim: out-of-fold ridge predictions at every penalty, plus a
    nested inner-CV choice of the penalty inside each training fold."""
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
    F = np.empty(len(y))
    for f in np.unique(folds):
        te = folds == f; tr = ~te
        o = ols(y[tr], [x[tr]], ["sd"])
        F[te] = o["coef"]["const"] + o["coef"]["sd"] * x[te]
    return F


# ================================================================== the book grid (idea 484's)
def panel_defs():
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    return {
        "B136": (px136, [c for c in px136.columns]),
        "SMALL484": (pxs, [c for c in pxs.columns if c != "SPY"]),
    }


def draw_books(px, names, k, d_lo, d_hi, seed, startb):
    """Books for draws [d_lo, d_hi) of one k cell.  Draw d is the d-th name set from the
    generator seeded once per (panel, k), so the ladder is nested by construction and draws
    0..499 are idea 484's own."""
    rng = np.random.default_rng(seed)
    rows = []
    for d in range(d_hi):
        cols = list(rng.choice(names, size=k, replace=False))
        if d < d_lo:
            continue
        keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px.columns else [])))
        p = px[keep].dropna(how="all").ffill()
        s, above, vol20 = score(p, vol_scale=False)
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
        rows.append(rec)
    return rows


def draw_names(names, k, d_lo, d_hi, seed):
    """Just the name sets - no backtest.  Used to rebuild the membership matrix for the draws
    whose book metrics are read from idea 484's committed grid."""
    rng = np.random.default_rng(seed)
    out = []
    for d in range(d_hi):
        cols = list(rng.choice(names, size=k, replace=False))
        if d >= d_lo:
            out.append(cols)
    return out


# ================================================================== STAGE 1: THE CENSUS
# idea 483's own regexes, verbatim, so its four published counts are reproducible here (gate [e])
FIT_RE = re.compile(r"lstsq|polyfit|np\.linalg\.solve|pinv|Ridge\(|ridge_|_ridge|LinearRegression|OLS\(|curve_fit")
FOLD_RE = re.compile(r"KFold|out.?of.?fold|oof|n_folds|fold_id|folds|train_idx|holdout|_is_half|first half.*second half", re.I)
WIDE_RE = re.compile(r"get_dummies|membership|indicator matrix|onehot|one_hot|dummies|M\s*=\s*np\.zeros|design matrix|columns=names|columns=tick")


def mechanical_census():
    rows = []
    for p in sorted((REPO / "research").rglob("*.py")):
        if p.name == SCRIPT:
            continue                                    # skip this file
        try:
            txt = p.read_text(errors="ignore")
        except Exception:
            continue
        fits = len(FIT_RE.findall(txt))
        if not fits:
            continue
        pcount = bool(re.findall(r"np\.zeros\(\(\s*\w+\s*,\s*len\(([A-Za-z_]+)\)\s*\)\)", txt))
        rows.append(dict(file=str(p.relative_to(REPO)), fit_calls=fits,
                         has_fold_machinery=bool(FOLD_RE.search(txt)),
                         wide_design_hint=bool(WIDE_RE.search(txt)),
                         per_name_design=pcount))
    return pd.DataFrame(rows)


def spec_sets():
    """Every published model-vs-model spec set the scan can resolve, with p (fitted parameters
    including the intercept) and N (rows the comparison was decided on).

    `source` says where each number comes from.  MECHANICAL = parsed from the file's own
    committed output; ADJUDICATED = read from the file's committed console at the quoted line,
    because the file printed the table and did not write it to a CSV.  Nothing here is a number
    typed from a memo: every ADJUDICATED entry names the console file and line.
    """
    S = []

    def add(fid, target, N, specs, source, evidence, n_source, note=""):
        S.append(dict(file=fid, target=target, N=N, specs=specs, source=source,
                      evidence=evidence, N_extensible=n_source, note=note))

    # ---- MECHANICAL: committed CSVs carrying a spec/parameter column beside R2 ----------
    f = OUT / "2026-09-08_why-does-the-DD-ranking-die-on-U56_C.decomp.csv"
    if f.exists():
        d = pd.read_csv(f)
        bcols = [c for c in d.columns if c.startswith("b_")]
        for n_, g in d.groupby("n"):
            specs = {r.model: 1 + int(sum(pd.notna(getattr(r, c)) for c in bcols)) for r in g.itertuples()}
            if len(specs) >= 2:
                add("2026-09-08_why-does-the-DD-ranking-die-on-U56_C", "DD-ranking slope", int(n_),
                    specs, "MECHANICAL", f.name, "PANEL-CAPPED (file supplies n=12 and n=186)")

    f = OUT / "2026-09-08_does-modal-share-predict-VARIANCE-not-sign_B.fit.csv"
    if f.exists():
        d = pd.read_csv(f)
        bcols = [c for c in d.columns if c.startswith("b_") and c != "b_intercept"]
        g = d[d.m_min == d.m_min.min()]
        specs = {r.spec: 1 + int(sum(pd.notna(getattr(r, c)) for c in bcols)) for r in g.itertuples()}
        add("2026-09-08_does-modal-share-predict-VARIANCE-not-sign_B", "log resid variance",
            int(g.n.iloc[0]), specs, "MECHANICAL", f.name, "PANEL-CAPPED")

    f = OUT / "2026-09-08_is-168c-s-k-CROSSING-a-SMOOTHING-artefact-end-to-end_cloud.shape.csv"
    if f.exists():
        d = pd.read_csv(f)
        specs = {r.model: int(r.params) for r in d.itertuples()}
        # p is MECHANICAL (the file's own `params` column); N is ADJUDICATED from its console.
        add("2026-09-08_is-168c-s-k-CROSSING-a-SMOOTHING-artefact-end-to-end_cloud", "k-crossing shape",
            352, specs, "MECHANICAL p / ADJUDICATED N",
            f"{f.name} params column; …cloud.console.txt:271 'four shapes, same 352 points'",
            "PANEL-CAPPED")

    f = OUT / "2026-09-06_is-ETF36-a-third-cluster-or-just-a-small-sample_C.shape.csv"
    if f.exists():
        d = pd.read_csv(f)
        # p = 1 intercept + one slope per named term ("linear in s" 1, "step at ..." 1, "+" joins)
        pmap = {m: 1 + (1 if "linear" in m else 0) + (1 if "step" in m else 0) for m in d.model}
        add("2026-09-06_is-ETF36-a-third-cluster-or-just-a-small-sample_C", "reversal ~ ETF share",
            int(d.n.iloc[0]), pmap, "MECHANICAL", f.name, "PANEL-CAPPED")

    f = OUT / "2026-09-06_can-a-panel-property-choose-the-cadence_cloud.decomp.csv"
    if f.exists():
        d = pd.read_csv(f)
        props = OUT / "2026-09-06_can-a-panel-property-choose-the-cadence_cloud.props.csv"
        N = int(len(pd.read_csv(props))) if props.exists() else -1
        specs = {r.spec: int(r.k) + 1 for r in d.itertuples()}
        add("2026-09-06_can-a-panel-property-choose-the-cadence_cloud", "cadence gap", N,
            specs, "MECHANICAL", f.name, "PANEL-CAPPED")

    # ---- ADJUDICATED: printed to the console, never written to a CSV --------------------
    add("2026-09-06_does-the-cash-drag-share-depend-on-the-panel-or-on-the-gate-level_cloud",
        "cash-drag share", 162,
        {"c_bar only": 2, "1+c_bar+panel+family+cadence": 7},
        "ADJUDICATED", "…cloud.console.txt:324 'n=162  R2=0.6098' + the 7 printed terms",
        "PANEL-CAPPED")

    add("2026-09-06_is-phase-sensitivity-a-book-property-or-a-panel-one_cloud",
        "log(phase spread)", 115,
        {"family dummies only": 3, "P1+P2": 3, "family+P1+P2": 5},
        "ADJUDICATED", "…cloud.console.txt:98-103, 5 cadence rows all at n=115",
        "STRATIFIED (5 cadences x 115; pooled N=575 available)")

    # ---- the wide-ridge class: p is the PANEL WIDTH, not a typed number -----------------
    add("2026-09-09_name-level-fixed-effects_B", "draw Sharpe (B136)", 50,
        {"sd alone": 2, "M name-additive ridge": None},          # None -> resolved to panel width
        "ADJUDICATED", "…_B.result.md 'N = 50 rows against 136 name columns'; .nested.csv",
        "DRAW-SOURCED (extensible)")

    add("2026-09-09_does-one-dispersion-number-really-out-predict-136-name-dummies_C",
        "draw Sharpe (B136, SMALL484)", 50,
        {"sd alone": 2, "M name-additive ridge": None},
        "MECHANICAL", "…_C.nested.csv, D=50 rung (the run's own restatement of idea 252 leg 3)",
        "DRAW-SOURCED (extensible)",
        note="NOT INDEPENDENT: idea 484 is the re-read of idea 252's own comparison")

    add("2026-09-09_which-published-residualisations-are-IN-SAMPLE-fits_cloud",
        "sd | control", 200,
        {"NARROW10": 11, "WIDE (panel width)": None},
        "MECHANICAL", "…_cloud.grid.csv width column (p 55/135/439), 200 draw books",
        "DRAW-SOURCED (extensible)")
    return S


def census_pairs(specs, panel_width):
    """Every unordered pair of specs inside each published spec set."""
    rows = []
    for e in specs:
        sp = {k: (panel_width if v is None else v) for k, v in e["specs"].items()}
        for (a, pa), (b, pb) in itertools.combinations(sorted(sp.items()), 2):
            rows.append(dict(file=e["file"], target=e["target"], N=e["N"],
                             spec_lo=a if pa <= pb else b, p_lo=min(pa, pb),
                             spec_hi=b if pa <= pb else a, p_hi=max(pa, pb),
                             gap=abs(pa - pb), source=e["source"], evidence=e["evidence"],
                             N_extensible=e["N_extensible"]))
    return pd.DataFrame(rows)


# ================================================================== main
def main():
    t0 = time.time()
    P("=" * 200)
    P("IDEA 486 - census-every-published-N-EQUALS-50-model-comparison-in-the-record (lane C, 2026-09-09)")
    P("Census every published model-vs-model comparison decided at N <= Nfloor rows whose two sides differ by")
    P("more than G fitted parameters, then re-read each at the largest N its own panel can supply.")
    P(f"Census axes (the two tuned parameters): Nfloor in {NFLOORS}, G in {GAPS} - all {len(NFLOORS)*len(GAPS)} points reported.")
    P(f"Re-read ladder D in {DRAWS} per k cell x panels {PANELS} (reporting axis, every point published).")
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
      f"   (the 2026-09-04 KEEP 4b candidate; published 12.7% / 1.092-1.093 / -18.3%)")
    r_v1 = backtest(px56, rules_v1_weights(px56), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[s56:]
    m1 = metrics(r_v1)
    P(f"    U56/RULES v1 {m1['CAGR']:.4%} / {m1['Sharpe']:.5f} / {m1['MaxDD']:.4%}   (published 6.5% / 0.664-0.666 / -13.8%)")

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
        P(f"\n    {pan}: {len(names)} tradable names, window {startb.date()} -> {px.index[-1].date()} ({len(spy)} days)")
        P(f"      SPY      {ms['CAGR']:.2%} / {ms['Sharpe']:.3f} / {ms['MaxDD']:.2%}  halves {sh1:.3f}/{sh2:.3f}"
          f"  OOS {metrics(spy.loc[OOS_START:])['Sharpe']:.3f}")
        for lab, b in (("RULES v1", base1), ("RULES v2 (live)", base2)):
            mb = metrics(b); b1, b2 = half_sharpes(b)
            P(f"      {lab:<15} {mb['CAGR']:.2%} / {mb['Sharpe']:.3f} / {mb['MaxDD']:.2%}  halves {b1:.3f}/{b2:.3f}"
              f"  OOS {metrics(b.loc[OOS_START:])['Sharpe']:.3f}")
        P(f"      4b bars: MaxDD <= {0.60*abs(ms['MaxDD']):.2%}, CAGR >= {0.70*ms['CAGR']:.2%}, "
          f"H1 > {sh1:.3f}, H2 > {sh2:.3f}, OOS Sharpe > {metrics(spy.loc[OOS_START:])['Sharpe']:.3f}")
    P(f"\n    PANEL INTEGRITY: B136 carries {panels['B136'][0].shape[1]} columns "
      f"(load_universe(broad=True) reaches data/prices_broad.csv only via its exception path), "
      f"SMALL484 carries {panels['SMALL484'][0].shape[1]}.")

    # ---------------------------------------------------------------- [b] fast backtest gate
    P("\n[b] FAST BACKTEST GATE - the vectorised backtester vs engine.backtest on 6 drawn books")
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
        if drop: elig[drop] = False
        w = (s.where(elig).rank(axis=1, ascending=False) <= 20).astype(float) * (GROSS / 20)
        a = backtest(p, w, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[startb136:]
        b = fast_backtest(p, w).loc[startb136:]
        gate_max = max(gate_max, float(np.abs(a.values - b.values).max()))
    ok_b = gate_max < 1e-12
    P(f"    max abs difference over 6 books: {gate_max:.3e}   FAST BACKTEST {'PASS' if ok_b else 'FAIL'}")

    # ================================================================ STAGE 1: CENSUS
    P("\n" + "=" * 200)
    P("STAGE 1 - THE CENSUS")
    P("=" * 200)
    MC = mechanical_census()
    n_fit = len(MC); n_unfold = int((~MC.has_fold_machinery).sum())
    n_wide = int(MC.wide_design_hint.sum()); n_wu = int((MC.wide_design_hint & ~MC.has_fold_machinery).sum())
    P(f"\n[e] MECHANICAL SCAN of every committed .py under research/ (idea 483's regexes, verbatim)")
    P(f"    files with a fit call                       {n_fit}   (idea 483 published 70)")
    P(f"    ... with NO fold/holdout machinery          {n_unfold}   (idea 483 published 66)")
    P(f"    ... with a wide (dummy/design-matrix) hint  {n_wide}   (idea 483 published 5)")
    P(f"    ... wide AND unfolded                       {n_wu}   (idea 483 published 3)")
    ok_e = (n_fit >= 70 and n_unfold >= 66 and n_wide >= 5 and n_wu >= 3)
    P(f"    GATE [e] {'PASS' if ok_e else 'FAIL'} - this run's scanner reproduces idea 483's census "
      f"(counts may exceed it: files committed since).")
    MC.to_csv(OUT / f"{STEM}.census.csv", index=False)

    if not (ok_b and ok_e):
        P("\n    ABORT: the object under test is not the published one.")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        return

    P("\n  THE COMPARISON TABLE - every published model-vs-model spec set the scan resolves.")
    P("  p = fitted parameters including the intercept.  N = rows the comparison was decided on.")
    P("  For the wide-ridge class p is the PANEL WIDTH, resolved from the panel itself, not typed.")
    SS = spec_sets()
    # resolve the wide-ridge widths from the panels actually loaded here
    width = {"2026-09-09_name-level-fixed-effects_B": len(panels["B136"][1]),
             "2026-09-09_does-one-dispersion-number-really-out-predict-136-name-dummies_C": len(panels["B136"][1]),
             "2026-09-09_which-published-residualisations-are-IN-SAMPLE-fits_cloud": len(panels["B136"][1])}
    PAIRS = []
    for e in SS:
        w = width.get(e["file"], np.nan)
        sp = {k: (w if v is None else v) for k, v in e["specs"].items()}
        for (a, pa), (b, pb) in itertools.combinations(sorted(sp.items()), 2):
            PAIRS.append(dict(file=e["file"], target=e["target"], N=e["N"],
                              spec_lo=(a if pa <= pb else b), p_lo=int(min(pa, pb)),
                              spec_hi=(b if pa <= pb else a), p_hi=int(max(pa, pb)),
                              gap=int(abs(pa - pb)), source=e["source"], evidence=e["evidence"],
                              N_extensible=e["N_extensible"], note=e["note"],
                              independent=(e["note"] == "")))
    PR = pd.DataFrame(PAIRS)
    PR.to_csv(OUT / f"{STEM}.pairs.csv", index=False)
    P(f"\n  {len(SS)} published spec sets -> {len(PR)} comparisons, ALL reported:")
    P(fmt(PR[["file", "target", "N", "spec_lo", "p_lo", "spec_hi", "p_hi", "gap", "source"]]
          .assign(file=lambda d: d.file.str.replace("2026-", "", regex=False).str[:52])
          .set_index(["file", "target"]), 0))

    P("\n  CENSUS GRID - comparisons in scope (N <= Nfloor AND gap > G), all 16 points:")
    grid = []
    for nf in NFLOORS:
        for g in GAPS:
            sel = PR[(PR.N <= nf) & (PR.N > 0) & (PR.gap > g)]
            ind = sel[sel.independent]
            grid.append(dict(Nfloor=nf, G=g, in_scope=len(sel), independent=len(ind),
                             files=sel.file.nunique(), independent_files=ind.file.nunique(),
                             extensible=int((sel.N_extensible.str.startswith("DRAW")).sum())))
    GR = pd.DataFrame(grid)
    GR.to_csv(OUT / f"{STEM}.censusgrid.csv", index=False)
    P(fmt(GR.pivot(index="Nfloor", columns="G", values="in_scope"), 0))
    P("\n  (same grid, distinct FILES)")
    P(fmt(GR.pivot(index="Nfloor", columns="G", values="files"), 0))
    P("\n  (same grid, INDEPENDENT comparisons only - idea 484 is the re-read of idea 252's own")
    P("   comparison and is excluded here so the class is not double-counted)")
    P(fmt(GR.pivot(index="Nfloor", columns="G", values="independent"), 0))
    hdl = PR[(PR.N <= 100) & (PR.N > 0) & (PR.gap > 10)]
    P(f"\n  THE QUEUE'S OWN CELL (Nfloor=100, G=10): {len(hdl)} comparisons in "
      f"{hdl.file.nunique()} file(s), {int(hdl.independent.sum())} independent:")
    for r in hdl.itertuples():
        P(f"      {r.file.replace('2026-','')}  |  {r.spec_lo} (p={r.p_lo}) vs {r.spec_hi} (p={r.p_hi})"
          f"  gap {r.gap}  N {r.N}  [{r.N_extensible}]{('  ** ' + r.note) if r.note else ''}")

    # ================================================================ STAGE 2b: the non-wide re-reads
    P("\n" + "=" * 200)
    P("STAGE 2b - RE-READ of every in-scope comparison that is NOT the wide-ridge class,")
    P("at the largest N its own panel can supply, from that file's own committed output.")
    P("=" * 200)
    rr = []

    # (i) DD-ranking: the file itself publishes the same spec at n=12 (cell means) and n=186
    f = OUT / "2026-09-08_why-does-the-DD-ranking-die-on-U56_C.decomp.csv"
    fc = OUT / "2026-09-08_why-does-the-DD-ranking-die-on-U56_C.cellslopes.csv"
    if f.exists() and fc.exists():
        d = pd.read_csv(f); cs = pd.read_csv(fc)
        small = d[d.n == d.n.min()]
        P(f"\n  (i) why-does-the-DD-ranking-die-on-U56: published at n={int(d.n.min())} (cell means) "
          f"and n={int(d.n.max())} (per-cell slopes).  Refit here on the {len(cs)} committed cell slopes:")
        y = cs.slope.values
        for nm, X, names in (("e only", [cs.e.values], ["e"]),
                             ("k only", [cs.k.values], ["k"]),
                             ("e + k", [cs.e.values, cs.k.values], ["e", "k"])):
            o = ols(y, X, names)
            pub = small[small.model == nm]
            r2p = float(pub.R2.iloc[0]) if len(pub) else np.nan
            P(f"      {nm:<8} R2 at n={int(d.n.min())} {r2p:+.4f}  ->  R2 at n={len(cs)} {o['R2']:+.4f}"
              f"   (published large-N row: {float(d[d.n==d.n.max()].R2.iloc[0]):+.4f})")
            rr.append(dict(file="why-does-the-DD-ranking-die-on-U56_C", spec=nm,
                           N_small=int(d.n.min()), R2_small=r2p, N_large=len(cs), R2_large=o["R2"]))
        o1 = ols(y, [cs.e.values], ["e"]); o2 = ols(y, [cs.e.values, cs.k.values], ["e", "k"])
        s1 = float(small[small.model == "e only"].R2.iloc[0]); s2 = float(small[small.model == "e + k"].R2.iloc[0])
        P(f"      ORDERING (e+k over e only): +{s2-s1:.4f} at n={int(d.n.min())}  ->  "
          f"+{o2['R2']-o1['R2']:.4f} at n={len(cs)}   "
          f"{'HOLDS' if (s2>s1)==(o2['R2']>o1['R2']) else 'FLIPS'}")

    # (ii) phase sensitivity: cadence strata at n=115 each; the largest N its panel supplies is
    #      the pool over cadences.  Rebuilt from the file's own committed .books.csv, with the
    #      file's own estimator (ols_r2 on log spread, family dummies vs the two log properties).
    fb = OUT / "2026-09-06_is-phase-sensitivity-a-book-property-or-a-panel-one_cloud.books.csv"
    if fb.exists():
        d = pd.read_csv(fb)
        d = d[np.isfinite(d.spread) & (d.spread > 0)].dropna(subset=["persistence", "elig_turn"])
        d = d[(d.persistence > 0) & (d.elig_turn > 0)]

        def r2_of(sub, use_family, use_pred, use_cad=False):
            y = np.log(sub.spread.values)
            blocks = []
            if use_family:
                blocks.append(pd.get_dummies(sub.family).values[:, 1:].astype(float))
            if use_cad:
                blocks.append(pd.get_dummies(sub.cad).values[:, 1:].astype(float))
            if use_pred:
                blocks.append(np.column_stack([np.log(sub.persistence.values),
                                               np.log(sub.elig_turn.values)]))
            if not blocks:
                return 0.0, 1
            X = np.hstack(blocks)
            o = ols(y, [X[:, j] for j in range(X.shape[1])], [f"x{j}" for j in range(X.shape[1])])
            return o["R2"], X.shape[1] + 1

        P("\n  (ii) is-phase-sensitivity - published per-cadence at n=115 (family dummies p=3 vs the two")
        P("       properties p=3 vs both p=5).  Re-read on the pool, the largest N this panel supplies,")
        P("       with CADENCE fixed effects added to every spec so pooling itself is not the change:")
        P(f"       {'cad':6s} {'n':>5s} {'R2 family':>10s} {'R2 P1+P2':>10s} {'R2 both':>9s}  ordering")
        for cad, s in list(d.groupby("cad")) + [("POOL", d)]:
            if len(s) < 10:
                continue
            uc = (cad == "POOL")
            rf, pf = r2_of(s, True, False, uc)
            rp, pp = r2_of(s, False, True, uc)
            rb, pb_ = r2_of(s, True, True, uc)
            P(f"       {str(cad):6s} {len(s):5d} {rf:10.3f} {rp:10.3f} {rb:9.3f}  "
              f"{'properties > family' if rp > rf else 'family > properties'}"
              f"   (p {pf}/{pp}/{pb_})")
            rr.append(dict(file="is-phase-sensitivity_cloud", spec=f"cad={cad}", N_small=115,
                           R2_small=np.nan, N_large=len(s), R2_large=rb,
                           R2_family=rf, R2_pred=rp))
        P("       The published claim is about which side wins per cadence; the pool row is the same")
        P("       comparison at the largest N, and it is reported whether or not it agrees.")

    if rr:
        pd.DataFrame(rr).to_csv(OUT / f"{STEM}.reread.csv", index=False)

    # ================================================================ STAGE 2a: the wide class
    P("\n" + "=" * 200)
    P(f"STAGE 2a - THE WIDE CLASS re-read at the largest N: draw ladder to D={D_MAX} per k cell")
    P(f"  Books for draws 0..{D_REF-1} are idea 484's committed grid (gate [c]); draws {D_REF}..{D_MAX-1} are run here.")
    P("=" * 200)
    if not REF484.exists():
        P("    idea 484's committed grid is absent - ABORT (the ladder cannot be tied to the record).")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        return
    ref = pd.read_csv(REF484)

    # gate [c]: re-run 25 draws of each k cell on each panel and require an exact match
    P("\n[c] GRID GATE - 25 draws of each k cell on each panel re-run fresh vs idea 484's committed grid")
    numcols = [c for c in ref.columns if c not in ("panel", "k", "draw")]
    worst = 0.0; nrows = 0
    for pan in PANELS:
        c = ctx[pan]
        for k in KS:
            fresh = pd.DataFrame(draw_books(c["px"], c["names"], k, 0, 25, SEED_B + k, c["startb"])).drop(columns=["cols"])
            r = ref[(ref.panel == pan) & (ref.k == k) & (ref.draw < 25)]
            j = fresh.merge(r, on=["k", "draw"], suffixes=("", "_ref"))
            nrows += len(j)
            for col in numcols:
                worst = max(worst, float((j[col] - j[col + "_ref"]).abs().max()))
    ok_c = worst < 1e-12 and nrows == 150
    P(f"    {nrows} rows x {len(numcols)} numeric columns, max abs difference {worst:.3e}   "
      f"GRID {'PASS - the ladder extends idea 484s own draws' if ok_c else 'FAIL'}")
    if not ok_c:
        P("\n    ABORT: the extension is not nested in the published grid.")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        return

    G = {}
    for pan in PANELS:
        c = ctx[pan]
        new = []
        for k in KS:
            new += draw_books(c["px"], c["names"], k, D_REF, D_MAX, SEED_B + k, c["startb"])
            P(f"    {pan} k={k:<3} draws {D_REF}..{D_MAX-1} done ({time.time()-t0:.0f}s)")
        NEW = pd.DataFrame(new).drop(columns=["cols"])
        OLD = ref[ref.panel == pan].drop(columns=["panel"])
        B = pd.concat([OLD, NEW], ignore_index=True).sort_values(["k", "draw"]).reset_index(drop=True)
        # rebuild every draw's name set deterministically (cheap; no backtest)
        colmap = {}
        for k in KS:
            for i, cols in enumerate(draw_names(c["names"], k, 0, D_MAX, SEED_B + k)):
                colmap[(k, i)] = cols
        B["cols"] = [colmap[(int(r.k), int(r.draw))] for r in B.itertuples()]
        G[pan] = B
        P(f"    {pan}: {len(B)} books ({D_MAX} draws x {len(KS)} k cells)")

    # membership matrices
    MM = {}
    for pan in PANELS:
        names = ctx[pan]["names"]; idxn = {c: i for i, c in enumerate(names)}
        B = G[pan]
        M = np.zeros((len(B), len(names)))
        for i, cols in enumerate(B["cols"].values):
            for c_ in cols:
                M[i, idxn[c_]] = 1.0
        MM[pan] = M
        P(f"    {pan}: P={len(names)} name columns, {len(B)} rows; N/P at D=50 {50/len(names):.2f}, "
          f"at D={D_MAX} {D_MAX/len(names):.2f}")

    # ---------------------------------------------------------------- the ladder
    P("\n  THE LADDER - out-of-fold R2 of  y ~ sd  vs  y ~ M (ridge)  vs  y ~ M + sd, 10 folds by draw index.")
    P("  lambda: CV = nested inner 5-fold choice inside each training fold; ORACLE = best of the six penalties.")
    TARGETS = [(nb, kind) for nb in N_BOOKS for kind in ("CAND Sharpe", "EWall Sharpe", "premium")]

    def target_col(nb, kind):
        return {"CAND Sharpe": f"Sharpe{nb}", "EWall Sharpe": "ew_Sharpe", "premium": f"premium{nb}"}[kind]

    lad = []
    for pan in PANELS:
        B = G[pan]; M_all = MM[pan]
        for k in KS:
            sel = np.flatnonzero((B.k == k).values)
            order = np.argsort(B.iloc[sel]["draw"].values)
            Bk = B.iloc[sel].iloc[order]; Mk_all = M_all[sel][order]
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
                    lad.append(dict(panel=pan, P=Mk.shape[1], n=nb, k=k, D=D, N=len(sub), y=kind,
                                    NP=len(sub) / Mk.shape[1],
                                    oofR2_sd=r_sd, oofR2_M_cv=r_M_cv, oofR2_Msd_cv=r_Msd_cv,
                                    oofR2_M_oracle=r_M_or,
                                    gap_cv=r_sd - r_M_cv, gap_oracle=r_sd - r_M_or,
                                    gain_cv=r_Msd_cv - r_M_cv,
                                    **{f"oofR2_M_lam{lam:g}": per_lam[lam][0] for lam in LAMS},
                                    **{f"oofR2_Msd_lam{lam:g}": per_lam[lam][1] for lam in LAMS}))
            P(f"    {pan} k={k} ladder done ({time.time()-t0:.0f}s)")
    L = pd.DataFrame(lad)
    L.to_csv(OUT / f"{STEM}.nested.csv", index=False)

    # ---------------------------------------------------------------- [d] idea 252's own number
    P("\n[d] IDEA 252's PUBLISHED NUMBER (its leg 3), recomputed here at D=50 on B136")
    d50 = L[(L.panel == "B136") & (L.D == 50) & (L.y != "premium")]
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

    # ---------------------------------------------------------------- crossover / max-N read
    P("\n  THE RE-READ AT MAX N - smallest D with oofR2(M) >= oofR2(sd), and the ordering at each end.")
    cross = []
    for (pan, nb, k, ylab), g in L.groupby(["panel", "n", "k", "y"]):
        g = g.sort_values("D")
        for tag, col in (("cv", "oofR2_M_cv"), ("oracle", "oofR2_M_oracle")):
            hit = g[g[col] >= g["oofR2_sd"]]
            dstar = int(hit.D.iloc[0]) if len(hit) else np.nan
            x = np.log(g.D.values); yv = (g["oofR2_sd"] - g[col]).values
            sl = np.polyfit(x, yv, 1)[0] if np.isfinite(yv).all() else np.nan
            cross.append(dict(panel=pan, n=nb, k=k, y=ylab, lam=tag,
                              sd_D50=float(g[g.D == 50]["oofR2_sd"].iloc[0]),
                              sd_Dmax=float(g[g.D == D_MAX]["oofR2_sd"].iloc[0]),
                              M_D50=float(g[g.D == 50][col].iloc[0]),
                              M_Dmax=float(g[g.D == D_MAX][col].iloc[0]),
                              gap_D50=float(g[g.D == 50]["oofR2_sd"].iloc[0] - g[g.D == 50][col].iloc[0]),
                              gap_Dmax=float(g[g.D == D_MAX]["oofR2_sd"].iloc[0] - g[g.D == D_MAX][col].iloc[0]),
                              slope_logD=sl, D_cross=dstar))
    C = pd.DataFrame(cross)
    C.to_csv(OUT / f"{STEM}.crossover.csv", index=False)
    P(fmt(C.set_index(["panel", "n", "k", "y", "lam"]), 4))
    bk = C[C.y != "premium"]
    for pan in PANELS:
        for tag in ("cv", "oracle"):
            s = bk[(bk.panel == pan) & (bk.lam == tag)]
            P(f"\n  {pan} / lambda {tag}: M catches sd inside the ladder in {int(s.D_cross.notna().sum())} of "
              f"{len(s)} book-Sharpe cells (median D* {s.D_cross.median() if s.D_cross.notna().any() else float('nan')})")
            P(f"      sd  median {s.sd_D50.median():+.4f} (D=50) -> {s.sd_Dmax.median():+.4f} (D={D_MAX})   "
              f"[the FLAT side]")
            P(f"      M   median {s.M_D50.median():+.4f} (D=50) -> {s.M_Dmax.median():+.4f} (D={D_MAX})")
            P(f"      gap median {s.gap_D50.median():+.4f} -> {s.gap_Dmax.median():+.4f}; "
              f"sd beats M in {int((s.gap_D50>0).sum())}/{len(s)} at D=50 and "
              f"{int((s.gap_Dmax>0).sum())}/{len(s)} at D={D_MAX}")

    P("\n  FULL LADDER, book-Sharpe columns (CV lambda):")
    P(fmt(L[L.y != "premium"].set_index(["panel", "n", "k", "y", "D"])[
        ["N", "P", "NP", "oofR2_sd", "oofR2_M_cv", "oofR2_M_oracle", "oofR2_Msd_cv", "gap_cv",
         "gap_oracle", "gain_cv"]]))
    P("\n  FULL LADDER, premium column:")
    P(fmt(L[L.y == "premium"].set_index(["panel", "n", "k", "D"])[
        ["N", "oofR2_sd", "oofR2_M_cv", "oofR2_M_oracle", "gap_cv", "gap_oracle"]]))
    P("\n  EVERY PENALTY at D=50 and D=%d (book-Sharpe columns):" % D_MAX)
    P(fmt(L[(L.y != "premium") & (L.D.isin([50, D_MAX]))].set_index(["panel", "n", "k", "y", "D"])[
        ["oofR2_sd"] + [f"oofR2_M_lam{lam:g}" for lam in LAMS]]))

    # ================================================================ STAGE 3: KEEP paths
    P("\n" + "=" * 200)
    P(f"STAGE 3 - BOTH KEEP PATHS on every one of the {sum(len(G[p]) for p in PANELS):,} books")
    P("=" * 200)
    P("  4a: Sharpe > the comparand book in BOTH halves AND MaxDD no worse.")
    P("  4b: Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's.")
    keeprows = []; both_hits = []
    for pan in PANELS:
        c = ctx[pan]; B = G[pan]
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
            p4b = (H1 > sh1) & (H2 > sh2) & (OS > oos_spy) & (np.abs(DD) <= 0.60*abs(msp["MaxDD"])) \
                  & (CG >= 0.70*msp["CAGR"])
            keeprows.append(dict(panel=pan, book=f"CAND{nb}", N=len(B),
                                 pass4a_v1=int(p4a1.sum()), pass4a_v2=int(p4a2.sum()),
                                 pass4b=int(p4b.sum()), both=int((p4a2 & p4b).sum())))
            for i in np.flatnonzero(p4a2 & p4b):
                r = B.iloc[i]
                both_hits.append(dict(panel=pan, book=f"CAND{nb}", k=int(r.k), draw=int(r.draw),
                                      CAGR=r[f"CAGR{nb}"], Sharpe=r[f"Sharpe{nb}"], MaxDD=r[f"MaxDD{nb}"],
                                      H1=r[f"H1_{nb}"], H2=r[f"H2_{nb}"], OOS=r[f"Sharpe_OOS{nb}"]))
        keeprows.append(dict(panel=pan, book="EWall", N=len(B), pass4a_v1=-1, pass4a_v2=-1,
                             pass4b=-1, both=-1))
    K = pd.DataFrame(keeprows)
    K.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    P(fmt(K.set_index(["panel", "book"]), 0))
    P("  (EWall halves are not in idea 78's grid schema and are not restated: -1 = not measured.)")
    P("  4a is shown against BOTH the superseded RULES v1 (idea 78's comparand) and the LIVE RULES v2.")
    if both_hits:
        P(f"\n  Books clearing BOTH paths ({len(both_hits)} of {sum(len(G[p]) for p in PANELS)*2:,} book-rows):")
        P(fmt(pd.DataFrame(both_hits).set_index(["panel", "book", "k", "draw"])))
        P("  These are name lists found by scanning thousands of sub-panels, not rules; see the memo caveat.")

    # ================================================================ STAGE 4: rule 8
    P("\n" + "=" * 200)
    P("STAGE 4 - RULE 8 WALK-FORWARD: selectors fitted on 2009-2016 only; 2017-2026 read once")
    P("=" * 200)
    wf = []
    for pan in PANELS:
        c = ctx[pan]; B = G[pan]; M_all = MM[pan]
        mspy_o = metrics(c["spy_oos"]); mv2_o = metrics(c["v2"].loc[OOS_START:])
        px = c["px"]
        s, above, vol20 = score(px, vol_scale=False)
        elig = (above & (vol20 < MAX_VOL)).copy()
        drop = [x for x in px.columns if x not in set(c["names"])]
        if drop: elig[drop] = False
        for nb in N_BOOKS:
            w0 = (s.where(elig).rank(axis=1, ascending=False) <= nb).astype(float) * (GROSS / nb)
            m0 = metrics(fast_backtest(px, w0).loc[c["startb"]:].loc[OOS_START:])
            for D in DRAWS:
                keep_rows = (B.draw < D).values
                sub = B[keep_rows].reset_index(drop=True)
                Msub = M_all[keep_rows]
                yIS = sub[f"Sharpe_IS{nb}"].values
                sdIS = sub["sd_IS"].values
                folds = np.arange(len(sub)) % N_FOLDS
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
                wf.append(dict(panel=pan, n=nb, D=D, arm="S0 do-nothing (whole panel)", k=np.nan,
                               draw=np.nan, OOS_CAGR=m0["CAGR"], OOS_Sharpe=m0["Sharpe"],
                               OOS_MaxDD=m0["MaxDD"]))
                for arm, i in picks.items():
                    row = sub.iloc[i]
                    wf.append(dict(panel=pan, n=nb, D=D, arm=arm, k=int(row.k), draw=int(row.draw),
                                   OOS_CAGR=row[f"CAGR_OOS{nb}"], OOS_Sharpe=row[f"Sharpe_OOS{nb}"],
                                   OOS_MaxDD=row[f"MaxDD_OOS{nb}"]))
                wf.append(dict(panel=pan, n=nb, D=D, arm="SPY", k=np.nan, draw=np.nan,
                               OOS_CAGR=mspy_o["CAGR"], OOS_Sharpe=mspy_o["Sharpe"], OOS_MaxDD=mspy_o["MaxDD"]))
                wf.append(dict(panel=pan, n=nb, D=D, arm="RULES v2 (live book)", k=np.nan, draw=np.nan,
                               OOS_CAGR=mv2_o["CAGR"], OOS_Sharpe=mv2_o["Sharpe"], OOS_MaxDD=mv2_o["MaxDD"]))
        P(f"    {pan} walk-forward done ({time.time()-t0:.0f}s)")
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(fmt(W.set_index(["panel", "n", "D", "arm"])[["k", "draw", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]]))
    P("\n  Selector summary - mean OOS over the %d ladder points x 2 book sizes, by panel:" % len(DRAWS))
    smry = W.groupby(["panel", "arm"]).agg(OOS_Sharpe=("OOS_Sharpe", "mean"),
                                           OOS_CAGR=("OOS_CAGR", "mean"),
                                           OOS_MaxDD=("OOS_MaxDD", "mean")).reset_index()
    P(fmt(smry.set_index(["panel", "arm"])))
    for pan in PANELS:
        s = W[W.panel == pan]
        spy_s = s[s.arm == "SPY"].OOS_Sharpe.iloc[0]
        v2_s = s[s.arm == "RULES v2 (live book)"].OOS_Sharpe.iloc[0]
        for arm in ["S3 sd-model OOF pred", "S4 M-model OOF pred", "S5 M+sd OOF pred"]:
            a = s[s.arm == arm]
            P(f"    {pan} {arm:<24} beats SPY in {int((a.OOS_Sharpe > spy_s).sum())}/{len(a)}, "
              f"beats live v2 in {int((a.OOS_Sharpe > v2_s).sum())}/{len(a)} "
              f"(mean {a.OOS_Sharpe.mean():+.4f}; SPY {spy_s:+.4f}, v2 {v2_s:+.4f})")
        a4 = s[s.arm == "S4 M-model OOF pred"].sort_values(["n", "D"]).OOS_Sharpe.values
        a3 = s[s.arm == "S3 sd-model OOF pred"].sort_values(["n", "D"]).OOS_Sharpe.values
        P(f"    {pan} the name-additive selector beats the dispersion selector out of sample in "
          f"{int((a4 > a3).sum())} of {len(a4)} ladder points (mean difference {np.mean(a4-a3):+.4f})")

    G_out = pd.concat([G[p].assign(panel=p).drop(columns=["cols"]) for p in PANELS])
    G_out.to_csv(OUT / f"{STEM}.grid.csv.gz", index=False, compression="gzip")
    P(f"\n  wrote {STEM}.census.csv ({len(MC)}), .pairs.csv ({len(PR)}), .censusgrid.csv ({len(GR)}), "
      f".nested.csv ({len(L)}), .crossover.csv ({len(C)}), .keeppaths.csv ({len(K)}), "
      f".walkforward.csv ({len(W)}), .grid.csv.gz ({len(G_out)} books)")
    P(f"\nElapsed {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()

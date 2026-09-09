#!/usr/bin/env python3
"""Idea 512 — put DEGREES OF FREEDOM beside every within-cell t in the record.

Idea 483 (lane C) found that 116 of the record's 134 over-the-bar fit sites are TWO-SIDED
Frisch-Waugh within transforms: the point estimate is unbiased, but a t read with the naive
dof N-2 instead of N-p-1 is overstated by sqrt((N-2)/(N-p-1)) (median 1.0511, max 1.1530
over those sites), which roughly DOUBLES the false-positive rate at |t|>2, and leaving one
out does NOT fix it.  The queue asks to (i) propose (N, p, dof) as required columns beside
any within-cell t, (ii) BACK-FILL them across the record, and (iii) report which published
within-cell claims survive the corrected dof.

Stages
  0. CENSUS   every committed CSV under research/ that publishes a t-statistic; classify the
              producing script as WITHIN (cell-demeaned both sides) or POOLED, and record
              whether N, p (= number of absorbed cells) and G (clusters) are published at all.
  1. BACK-FILL every restatable within-cell t row under four conventions:
                 AS PUBLISHED     the record's own: homoskedastic or cluster SE, NORMAL ref
                 t(N-2)           naive dof
                 t(N-p-1)         the corrected dof the queue asks for
                 CR1 + t(G-1)     the cluster analogue (Liang-Zeger CR1 with K = p+1)
              and report which |t|>2 claims survive.
  2. MONTE CARLO at the record's own (N, p, G) rungs with x and y INDEPENDENT: the realised
              share of draws clearing |t|>2 under each convention (a correct procedure sits
              at 0.05), plus the leave-one-out jackknife arm idea 483 reported as no fix.
  3. FRESH BOOKS — the same question on books this run builds itself, where (N, p) are known
              exactly: 36 ranked arms + 360 random draw books on 3 panels, the within-cell
              transfer t of OOS Sharpe on IS Sharpe at 5 cell granularities, plus the
              PROTOCOL requirements: rule-8 walk-forward (choose on the first half, evaluate
              on the second) and BOTH KEEP paths (4a vs live RULES v2, 4b vs SPY).

Two tuned parameters, and only two: book size n and gross g.  The dof convention and the
cell granularity q are treatment axes, not tuned dials; every grid point is reported.
Monte-Carlo draw count is a precision setting, reported at both levels.

Costs 10 bps, weekly, weights decided at t applied at t+1 (engine).  No network.
SURVIVORSHIP: B136 and the sub-$2B panel are CURRENT constituents only; the small panel
additionally drops every ticker with max_1d_move >= 1.0 in data/small_meta.csv.
"""
from __future__ import annotations
import csv, gzip, math, re, sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights  # noqa
from engine import backtest, metrics  # noqa

STAMP = "2026-09-09_put-DEGREES-OF-FREEDOM-beside-every-within-cell-t_cloud"
OUT = ROOT / "research" / "backtests"
COST, FREQ = 10, "W"
NS = [5, 10, 15, 20, 30, 40]          # tuned param 1: book size
GROSS = [0.75, 1.00]                  # tuned param 2: gross
NDRAW, KDRAW = 60, [5, 20]            # random draw books per panel per k
QBINS = [1, 2, 5, 10, 20]             # cell granularity (treatment axis, not tuned)
MCDRAWS = [200, 1000]                 # precision setting, both reported
ROWCAP = 20000                        # per-CSV harvest cap

_console = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); _console.append(s)

# ------------------------------------------------------------------ distributions (no scipy)
def ncdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def _betacf(a, b, x, itmax=300, eps=3e-14):
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0; d = 1.0 - qab * x / qap
    if abs(d) < 1e-300: d = 1e-300
    d = 1.0 / d; h = d
    for m in range(1, itmax + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-300: d = 1e-300
        c = 1.0 + aa / c
        if abs(c) < 1e-300: c = 1e-300
        d = 1.0 / d; h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-300: d = 1e-300
        c = 1.0 + aa / c
        if abs(c) < 1e-300: c = 1e-300
        d = 1.0 / d; de = d * c; h *= de
        if abs(de - 1.0) < eps: break
    return h

def betai(a, b, x):
    if x <= 0: return 0.0
    if x >= 1: return 1.0
    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x)
    bt = math.exp(lbeta)
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1 - x) / b

def t_p2(t, dof):
    """Two-sided p-value of |t| under Student-t with `dof` degrees of freedom."""
    if not np.isfinite(t) or not np.isfinite(dof) or dof <= 0: return np.nan
    return float(betai(dof / 2.0, 0.5, dof / (dof + t * t)))

def t_crit(dof, alpha=0.05):
    """Two-sided critical value; bisection on t_p2."""
    if not np.isfinite(dof) or dof <= 0: return np.nan
    lo, hi = 0.0, 200.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if t_p2(mid, dof) > alpha: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)

# ------------------------------------------------------------------ the within estimator
def within_fit(d: pd.DataFrame, xcol, ycol, cellcol, clustercol=None, min_cell=4) -> dict:
    """Cell-demeaned OLS of y on x, reported under every dof convention at once."""
    cols = [cellcol, xcol, ycol] + ([clustercol] if clustercol else [])
    d = d[cols].dropna()
    d = d[d.groupby(cellcol)[cellcol].transform("size") >= min_cell].copy()
    N = len(d); P = int(d[cellcol].nunique()) if N else 0
    out = dict(N=N, p=P, dof_naive=N - 2, dof_correct=N - P - 1)
    if N < 20 or P < 2 or N - P - 1 <= 1:
        return {**out, **{k: np.nan for k in
                ("slope", "R2", "t_naive", "t_correct", "inflation", "p_normal", "p_tN2",
                 "p_correct", "t_cluster_pub", "t_cluster_CR1", "G", "p_cluster_pub",
                 "p_cluster_CR1")}}
    x = (d[xcol] - d.groupby(cellcol)[xcol].transform("mean")).values.astype(float)
    y = (d[ycol] - d.groupby(cellcol)[ycol].transform("mean")).values.astype(float)
    sxx = float(x @ x)
    if sxx <= 0:
        return {**out, **{k: np.nan for k in
                ("slope", "R2", "t_naive", "t_correct", "inflation", "p_normal", "p_tN2",
                 "p_correct", "t_cluster_pub", "t_cluster_CR1", "G", "p_cluster_pub",
                 "p_cluster_CR1")}}
    b = float(x @ y) / sxx
    e = y - b * x
    rss = float(e @ e); sst = float(y @ y)
    se_naive = math.sqrt(rss / (N - 2) / sxx)
    se_corr = math.sqrt(rss / (N - P - 1) / sxx)
    t_naive = b / se_naive if se_naive > 0 else np.nan
    t_corr = b / se_corr if se_corr > 0 else np.nan
    res = dict(out, slope=b, R2=1 - rss / sst if sst > 0 else np.nan,
               t_naive=t_naive, t_correct=t_corr,
               inflation=math.sqrt((N - 2) / (N - P - 1)),
               p_normal=2 * (1 - ncdf(abs(t_naive))), p_tN2=t_p2(t_naive, N - 2),
               p_correct=t_p2(t_corr, N - P - 1),
               t_cluster_pub=np.nan, t_cluster_CR1=np.nan, G=np.nan,
               p_cluster_pub=np.nan, p_cluster_CR1=np.nan)
    if clustercol:
        g = pd.DataFrame({"c": d[clustercol].values, "xe": x * e})
        meat = float((g.groupby("c").xe.sum() ** 2).sum())
        G = int(g.c.nunique())
        if meat > 0 and G >= 2:
            se_cl = math.sqrt(meat) / sxx                       # the record's own SE
            cr1 = math.sqrt(G / (G - 1) * (N - 1) / (N - P - 1))  # Liang-Zeger, K = p+1
            res.update(G=G, t_cluster_pub=b / se_cl, t_cluster_CR1=b / (se_cl * cr1),
                       p_cluster_pub=2 * (1 - ncdf(abs(b / se_cl))),
                       p_cluster_CR1=t_p2(b / (se_cl * cr1), G - 1))
    return res

# ------------------------------------------------------------------ stage 0: census
TCOL = re.compile(r"^(t|t_[A-Za-z0-9_]*|[A-Za-z0-9_]*_t|tstat|t_stat|T|OOS_t)$")
GCOL = re.compile(r"^(cells|n_cells|groups|n_groups|ncell)$", re.I)
CLCOL = re.compile(r"^(clusters|n_clusters|files)$", re.I)
NCOL = re.compile(r"^(n|N|rows|n_rows|nobs|n_obs)$", re.I)
WITHIN_RE = re.compile(r"-\s*[A-Za-z_0-9\[\]\"'\.]*\.?groupby\([^\n]{0,80}\.transform\(\s*[\"']mean[\"']\s*\)"
                       r"|within_cell_fit|fe_transform|def\s+within_", re.M)
CLUSTER_RE = re.compile(r"meat|cluster", re.I)
NORMREF_RE = re.compile(r"ncdf\(|norm\.cdf|scipy\.stats\.norm")
TDIST_RE = re.compile(r"stats\.t\.|t\.sf\(|studentt|t_p2|betai")

def _header(p: Path):
    op = gzip.open if p.suffix == ".gz" else open
    with op(p, "rt", errors="ignore") as f:
        return next(csv.reader([f.readline().strip()]))

def census() -> pd.DataFrame:
    rows = []
    src_cache = {}
    for p in sorted(list((ROOT / "research").rglob("*.csv")) + list((ROOT / "research").rglob("*.csv.gz"))):
        if p.name.startswith(STAMP): continue
        try: cols = _header(p)
        except Exception: continue
        tc = [c for c in cols if TCOL.match(c)]
        if not tc: continue
        stem = p.name.split(".")[0]
        src = p.parent / f"{stem}.py"
        if src not in src_cache:
            try: src_cache[src] = src.read_text(errors="ignore") if src.exists() else ""
            except Exception: src_cache[src] = ""
        txt = src_cache[src]
        rows.append(dict(csv=p.name, script=src.name if src.exists() else "(no script found)",
                         t_cols=";".join(tc),
                         has_N=bool([c for c in cols if NCOL.match(c)]),
                         has_p_cells=bool([c for c in cols if GCOL.match(c)]),
                         has_G_clusters=bool([c for c in cols if CLCOL.match(c)]),
                         script_is_within=bool(WITHIN_RE.search(txt)),
                         script_uses_cluster=bool(CLUSTER_RE.search(txt)),
                         script_normal_ref=bool(NORMREF_RE.search(txt)),
                         script_t_dist_ref=bool(TDIST_RE.search(txt))))
    return pd.DataFrame(rows)

# Which estimator each published t column actually is.  Read off the producing source, line
# numbers as committed on 2026-09-09; anything not listed is UNMAPPED and is reported as such,
# because the record's CSV headers do not say which t is which — that is half the finding.
#   WITHIN_OLS      cell-demeaned OLS slope t              correct dof N-p-1
#   CELL_AGG        t over per-cell statistics             correct dof (cells-1), not N-2
#   POOLED          ordinary multi-parameter OLS t         no within charge
EST_MAP = {
    # does-the-IS-WINDOW-DD-CAP...cloud.py:223  t_slope = within_cell_fit()['t'] (cluster on file)
    ("2026-09-08_does-the-IS-WINDOW-DD-CAP-transfer-at-all_cloud.transfer.csv", "t_slope"): "WITHIN_OLS",
    # ...:224  t_rho = within_cell_rank()['t'], a t over `rank_cells` per-cell Spearman rhos
    ("2026-09-08_does-the-IS-WINDOW-DD-CAP-transfer-at-all_cloud.transfer.csv", "t_rho"): "CELL_AGG",
    # why-does-the-DD-ranking-die-on-U56_C.py:214  t = within_cell_fit() (cluster on panel_id)
    ("2026-09-08_why-does-the-DD-ranking-die-on-U56_C.transfer.csv", "t"): "WITHIN_OLS",
    ("2026-09-08_why-does-the-DD-ranking-die-on-U56_C.provenance.csv", "t"): "WITHIN_OLS",
    # ...:181  t_slope / t_rho = per_cell_slopes(), a t over `cells` per-cell slopes/rhos
    ("2026-09-08_why-does-the-DD-ranking-die-on-U56_C.transfer.csv", "t_slope"): "CELL_AGG",
    ("2026-09-08_why-does-the-DD-ranking-die-on-U56_C.transfer.csv", "t_rho"): "CELL_AGG",
    # ...:495  a 3-parameter pooled OLS, no cell transform
    ("2026-09-08_why-does-the-DD-ranking-die-on-U56_C.decomp.csv", "t_e"): "POOLED",
    ("2026-09-08_why-does-the-DD-ranking-die-on-U56_C.decomp.csv", "t_k"): "POOLED",
    # is-the-hole-about-SHARE...cloud.py:434,586  one-sample t on dial-demeaned values (dof N-p)
    ("2026-09-08_is-the-hole-about-SHARE-or-about-PICK-ENTROPY_cloud.conditional.csv", "t_resid"): "WITHIN_MEAN",
}

# Which published column carries the p of THAT t.  Two hazards the record has already walked into:
#  * IS-WINDOW's t_rho is a t over `rank_cells` cells, not over `cells`.
#  * DD-ranking's transfer_row() calls within_cell_fit() and then per_cell_slopes(), and the
#    SECOND dict overwrites `cells` -- so the `cells` published beside the within-OLS `t` in
#    that file belongs to a different estimator and is a LOWER bound on the true p.
PCOL_MAP = {
    ("2026-09-08_does-the-IS-WINDOW-DD-CAP-transfer-at-all_cloud.transfer.csv", "t_rho"): "rank_cells",
}
P_AMBIGUOUS = {("2026-09-08_why-does-the-DD-ranking-die-on-U56_C.transfer.csv", "t")}

def harvest(cen: pd.DataFrame) -> pd.DataFrame:
    """Every published t row from a WITHIN script, with whatever (N, p, G) the record published."""
    rows = []
    for _, r in cen[cen.script_is_within].iterrows():
        p = OUT / r.csv
        if not p.exists():
            cand = list((ROOT / "research").rglob(r.csv))
            if not cand: continue
            p = cand[0]
        try:
            d = pd.read_csv(p, nrows=ROWCAP)
        except Exception:
            continue
        ncol = next((c for c in d.columns if NCOL.match(c)), None)
        gcol = next((c for c in d.columns if GCOL.match(c)), None)
        ccol = next((c for c in d.columns if CLCOL.match(c)), None)
        for tc in r.t_cols.split(";"):
            if tc not in d.columns: continue
            for i, row in d.iterrows():
                t = pd.to_numeric(pd.Series([row[tc]]), errors="coerce").iloc[0]
                if not np.isfinite(t): continue
                pc = PCOL_MAP.get((r.csv, tc), gcol)
                if pc not in d.columns: pc = gcol
                N = pd.to_numeric(pd.Series([row[ncol]]), errors="coerce").iloc[0] if ncol else np.nan
                P = pd.to_numeric(pd.Series([row[pc]]), errors="coerce").iloc[0] if pc else np.nan
                G = pd.to_numeric(pd.Series([row[ccol]]), errors="coerce").iloc[0] if ccol else np.nan
                rows.append(dict(csv=r.csv, script=r.script, t_col=tc, row=i, t_published=float(t),
                                 estimator=EST_MAP.get((r.csv, tc), "UNMAPPED"),
                                 p_col=pc if pc else "", p_ambiguous=(r.csv, tc) in P_AMBIGUOUS,
                                 N=N, p=P, G=G, cluster_SE=bool(r.script_uses_cluster),
                                 normal_ref=bool(r.script_normal_ref)))
    return pd.DataFrame(rows)

def backfill(h: pd.DataFrame) -> pd.DataFrame:
    """(N, p, dof) beside every t, restated under the convention its OWN estimator requires."""
    d = h.copy()
    # dof the estimator actually spends: OLS slope after p cell means -> N-p-1;
    # a one-sample t on cell-demeaned values -> N-p; a t over per-cell statistics -> cells-1.
    dof_c = np.where(d.estimator == "WITHIN_OLS", d.N - d.p - 1,
             np.where(d.estimator == "WITHIN_MEAN", d.N - d.p,
              np.where(d.estimator == "CELL_AGG", d.p - 1, d.N - 2)))
    d["dof_correct"] = dof_c
    d["dof_naive"] = np.where(d.estimator == "CELL_AGG", np.inf, d.N - 2)
    ok = np.isfinite(dof_c.astype(float)) & (pd.Series(dof_c, index=d.index) > 1)
    ok &= np.where(d.estimator == "CELL_AGG", d.p.notna(), d.N.notna() & d.p.notna())
    d["restatable"] = ok
    # the queue's charge sqrt((N-2)/(N-p-1)) rescales the SE; a CELL_AGG t is already computed
    # on `cells` rows, so nothing rescales it -- only its reference distribution changes.
    infl = np.where(d.estimator.isin(["WITHIN_OLS", "WITHIN_MEAN"]) & ok,
                    np.sqrt((d.N - 2) / np.where(dof_c > 0, dof_c, np.nan)), 1.0)
    d["inflation"] = np.where(ok, infl, np.nan)
    d["t_correct"] = np.where(ok, d.t_published / d.inflation, np.nan)
    d["p_as_published"] = [2 * (1 - ncdf(abs(t))) for t in d.t_published]
    d["p_tN2"] = [t_p2(t, n - 2) if np.isfinite(n) else np.nan for t, n in zip(d.t_published, d.N)]
    d["p_correct"] = [t_p2(tc, dof) if np.isfinite(tc) and np.isfinite(dof) else np.nan
                      for tc, dof in zip(d.t_correct, d.dof_correct)]
    # the cluster analogue: CR1 scaling with K = p+1, referred to t(G-1)
    cr1 = np.where(d.G.notna() & ok & (d.G > 1),
                   np.sqrt(d.G / (d.G - 1) * (d.N - 1) / (d.N - d.p - 1)), np.nan)
    d["t_CR1"] = d.t_published / cr1
    d["p_CR1_tG1"] = [t_p2(t, g - 1) if np.isfinite(t) and np.isfinite(g) and g > 1 else np.nan
                      for t, g in zip(d.t_CR1, d.G)]
    # A p that cannot be recovered from the record still admits a BOUND: within_cell_fit keeps
    # only cells with >= 4 rows, so p <= N/4 and the dof charge cannot exceed this.
    pmax = np.floor(d.N / 4.0)
    dof_worst = d.N - pmax - 1
    d["p_upper_bound"] = np.where(d.estimator.isin(["WITHIN_OLS", "WITHIN_MEAN"]), pmax, np.nan)
    d["t_worstcase"] = np.where(d.estimator.isin(["WITHIN_OLS", "WITHIN_MEAN"]) & (dof_worst > 1),
                                d.t_published / np.sqrt((d.N - 2) / dof_worst), np.nan)
    d["over_bar_published"] = d.t_published.abs() > 2
    d["over_bar_correct"] = d.t_correct.abs() > 2
    d["over_bar_worstcase"] = d.t_worstcase.abs() > 2
    # how much dof would have to be spent for the published claim to die at |t|=2
    d["inflation_to_kill"] = d.t_published.abs() / 2.0
    d["pN_to_kill"] = np.where(d.N.notna(),
                               (d.N - 1 - (d.N - 2) / d.inflation_to_kill ** 2) / d.N, np.nan)
    d["sig_published_5pct"] = d.p_as_published < 0.05
    d["sig_correct_5pct"] = d.p_correct < 0.05
    d["sig_CR1_5pct"] = d.p_CR1_tG1 < 0.05
    return d

# ------------------------------------------------------------------ stage 2: Monte Carlo
def mc_rung(N, P, G, draws, seed=0):
    """x, y independent; balanced cells; realised share of draws clearing the 5% bar."""
    rng = np.random.default_rng(seed)
    cell = np.arange(N) % P
    clus = np.arange(N) % G if G and G > 1 else None
    cn = np.bincount(cell, minlength=P).astype(float)
    tc_naive, tc_corr = 2.0, 2.0                       # the record's own |t|>2 bar
    crit_corr = t_crit(N - P - 1)
    hits = dict(naive=0, correct=0, loo=0, cluster_pub=0, cluster_CR1=0, correct_tcrit=0)
    crit_G = t_crit(G - 1) if clus is not None else np.nan
    for _ in range(draws):
        x = rng.standard_normal(N); y = rng.standard_normal(N)
        xm = np.bincount(cell, weights=x, minlength=P) / cn
        ym = np.bincount(cell, weights=y, minlength=P) / cn
        x = x - xm[cell]; y = y - ym[cell]
        sxx = x @ x
        if sxx <= 0: continue
        b = (x @ y) / sxx; e = y - b * x; rss = e @ e
        t_n = b / math.sqrt(rss / (N - 2) / sxx)
        t_c = b / math.sqrt(rss / (N - P - 1) / sxx)
        hits["naive"] += abs(t_n) > tc_naive
        hits["correct"] += abs(t_c) > tc_corr
        hits["correct_tcrit"] += abs(t_c) > crit_corr
        # leave-one-out jackknife SE on the same demeaned design (idea 483's "no fix" arm)
        h = x * x / sxx
        bj = b - (x * e) / (sxx * np.clip(1 - h, 1e-12, None))
        se_j = math.sqrt(((N - 1) / N) * float(((bj - bj.mean()) ** 2).sum()))
        hits["loo"] += abs(b / se_j) > tc_naive if se_j > 0 else 0
        if clus is not None:
            xe = np.bincount(clus, weights=x * e, minlength=G)
            meat = float((xe ** 2).sum())
            if meat > 0:
                se_cl = math.sqrt(meat) / sxx
                hits["cluster_pub"] += abs(b / se_cl) > 2.0
                cr1 = math.sqrt(G / (G - 1) * (N - 1) / (N - P - 1))
                hits["cluster_CR1"] += abs(b / (se_cl * cr1)) > crit_G
    out = {k: v / draws for k, v in hits.items()}
    if clus is None:                       # no cluster arm was run on this rung
        out["cluster_pub"] = out["cluster_CR1"] = np.nan
    return out

# ------------------------------------------------------------------ stage 3: panels and books
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad)

def mom_score(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3

def ranked_weights(px, tickers, n, gross):
    """Top-n by the composite among names above their 200d MA, equal weight, NO vol scaler."""
    sub = px[tickers]
    s = mom_score(sub).where(sub > sub.rolling(200).mean())
    rank = s.rank(axis=1, ascending=False)
    sel = (rank <= n).astype(float)
    cnt = sel.sum(axis=1).replace(0, np.nan)
    w = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    w[tickers] = (gross * sel.div(cnt, axis=0)).fillna(0.0)
    return w

def ew_weights(px, names, gross=1.0):
    w = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    sub = px[names].notna().astype(float)
    w[names] = gross * sub.div(sub.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return w

def three_metrics(r, h):
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    return m, m1, m2

# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say(f"# {STAMP}\n")

    # ---------------- stage 0/1 -----------------------------------------
    cen = census()
    cen.to_csv(OUT / f"{STAMP}.census.csv", index=False)
    say("## 0. CENSUS — what the record publishes beside a t")
    say(f"committed CSVs under research/ carrying a t-statistic column: {len(cen)}")
    w = cen[cen.script_is_within]
    say(f"  ... produced by a script that demeans BOTH sides by a cell (a WITHIN t): {len(w)}")
    say(f"  ... of those, publishing N: {int(w.has_N.sum())}/{len(w)};  p (cells): "
        f"{int(w.has_p_cells.sum())}/{len(w)};  G (clusters): {int(w.has_G_clusters.sum())}/{len(w)}")
    say(f"  ... publishing N AND p (the pair needed to restate the dof): "
        f"{int((w.has_N & w.has_p_cells).sum())}/{len(w)}")
    say(f"  ... referring the t to a NORMAL distribution: {int(w.script_normal_ref.sum())}/{len(w)}; "
        f"using a cluster-robust SE: {int(w.script_uses_cluster.sum())}/{len(w)}")
    say("(classification is a file-level regex on the producing script, so WITHIN is a lower"
        " bound and 'publishes p' an upper bound — a file can publish cells for one t and not another.)\n")

    h = harvest(cen)
    bf = backfill(h) if len(h) else pd.DataFrame()
    if len(bf):
        bf.to_csv(OUT / f"{STAMP}.backfill.csv", index=False)
    say("## 1. BACK-FILL — (N, p, dof) beside every published within-cell t")
    say(f"published t rows harvested from WITHIN scripts: {len(bf)} from "
        f"{bf.csv.nunique() if len(bf) else 0} CSVs")
    if len(bf):
        say("by estimator (read off the producing source; UNMAPPED = the CSV header does not say"
            " which estimator the column is, and neither does the script's own column name):")
        say(bf.groupby("estimator").agg(rows=("t_published", "size"),
                                        restatable=("restatable", "sum"),
                                        N_published=("N", lambda s: int(s.notna().sum())),
                                        p_published=("p", lambda s: int(s.notna().sum())),
                                        G_published=("G", lambda s: int(s.notna().sum()))
                                        ).to_string())
        miss = bf[~bf.restatable]
        say(f"  NOT restatable: {len(miss)} rows — missing N {int(miss.N.isna().sum())}, "
            f"missing p {int(miss.p.isna().sum())}, estimator unidentifiable "
            f"{int((miss.estimator=='UNMAPPED').sum())}")
    r = bf[bf.restatable] if len(bf) else pd.DataFrame()
    if len(r):
        say(f"\n  restatable rows: {len(r)}  "
            f"(WITHIN_OLS {int((r.estimator=='WITHIN_OLS').sum())}, "
            f"CELL_AGG {int((r.estimator=='CELL_AGG').sum())})")
        say(f"  dof lost to the cell means: median p/N {(r.p/r.N).median():.4f}, q90 "
            f"{(r.p/r.N).quantile(0.9):.4f}, max {(r.p/r.N).max():.4f}")
        say(f"  inflation sqrt((N-2)/(N-p-1)): median {r.inflation.median():.4f}, q90 "
            f"{r.inflation.quantile(0.9):.4f}, max {r.inflation.max():.4f}")
        ob = r[r.over_bar_published]
        say(f"\n  published claims over the record's own |t|>2 bar: {len(ob)} of {len(r)} restatable rows")
        say(f"    still over the bar after the dof correction:      {int(ob.over_bar_correct.sum())} "
            f"({ob.over_bar_correct.mean():.1%} survive)  -> {len(ob)-int(ob.over_bar_correct.sum())} FLIP")
        say(f"    still significant at 5% under t(N-p-1):           {int(ob.sig_correct_5pct.sum())}")
        cl = ob[ob.p_CR1_tG1.notna()]
        if len(cl):
            say(f"    cluster rows (G published): {len(cl)}; significant at 5% under CR1 + t(G-1): "
                f"{int(cl.sig_CR1_5pct.sum())} ({cl.sig_CR1_5pct.mean():.1%})")
        say("\n  restated at 5% under the reference the estimator actually requires "
            "(the record refers every one of these to a NORMAL):")
        say(ob.groupby("estimator").agg(over_bar=("t_published", "size"),
                                        sig_as_published=("sig_published_5pct", "sum"),
                                        sig_restated=("sig_correct_5pct", "sum"),
                                        med_dof_naive=("dof_naive", "median"),
                                        med_dof_correct=("dof_correct", "median")).to_string())
        say("\n  every restatable within-t claim over the bar, by source (t_published -> t_correct):")
        g = ob.groupby(["csv", "t_col"]).agg(rows=("t_published", "size"),
                                             med_t_pub=("t_published", lambda s: s.abs().median()),
                                             med_t_corr=("t_correct", lambda s: s.abs().median()),
                                             med_N=("N", "median"), med_p=("p", "median"),
                                             survive=("over_bar_correct", "sum")).reset_index()
        say(g.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
        wo = ob[ob.estimator.isin(["WITHIN_OLS", "WITHIN_MEAN"])]
        if len(wo):
            say(f"\n  WHY nothing moves: the published within-OLS claims are far from the bar."
                f"  |t| median {wo.t_published.abs().median():.2f}, q10 "
                f"{wo.t_published.abs().quantile(0.10):.2f}, min {wo.t_published.abs().min():.2f}")
            say(f"  the dof charge that WOULD kill each claim: p/N median "
                f"{wo.pN_to_kill.median():.3f}, q10 {wo.pN_to_kill.quantile(0.10):.3f}, "
                f"min {wo.pN_to_kill.min():.3f} — against an actual p/N of "
                f"{(wo.p/wo.N).median():.3f} (max {(wo.p/wo.N).max():.3f})")
            say(f"  worst-case bound (p at its ceiling N/4, so the largest charge the >=4-rows-"
                f"per-cell rule allows): still over the bar on "
                f"{int(wo.over_bar_worstcase.sum())}/{len(wo)}")
            amb = wo[wo.p_ambiguous]
            if len(amb):
                say(f"  NOTE: {len(amb)} of those rows carry an AMBIGUOUS p — "
                    f"{amb.csv.iloc[0]} builds its row by dict-updating within_cell_fit() with "
                    f"per_cell_slopes(), which overwrites `cells`, so the published p belongs to "
                    f"the other estimator and is a lower bound. Their restatement is the "
                    f"worst-case column, and they survive it too.")
        flips = ob[~ob.over_bar_correct]
        if len(flips):
            say("\n  the rows that FLIP (|t| crosses 2 downward once p is charged):")
            say(flips[["csv", "t_col", "row", "N", "p", "t_published", "t_correct"]]
                .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
        else:
            say("\n  NO restatable published within-cell claim flips at |t|>2 on the dof charge alone.")
    say("")

    # ---------------- stage 2 -------------------------------------------
    say("## 2. MONTE CARLO at the record's own (N, p) rungs — x and y INDEPENDENT")
    rungs = []
    if len(r):
        rr = r[(r.p >= 2)].copy()
        rr["pn"] = rr.p / rr.N
        for q in [0.1, 0.5, 0.9, 1.0]:
            row = rr.iloc[(rr.pn - rr.pn.quantile(q)).abs().argsort().iloc[0]]
            rungs.append((int(row.N), int(row.p), int(row.G) if np.isfinite(row.G) else 0))
    # idea 483's two rungs, this run's own fresh-book geometry, and the record's two REAL
    # cluster counts (provenance.csv: u56 N=6822 p=833 G=34; small N=4123 p=436 G=24)
    rungs += [(224, 56, 8), (548, 120, 10), (360, 120, 6), (360, 6, 3),
              (6822, 833, 34), (4123, 436, 24)]
    seen, rung_list = set(), []
    for N, P, G in rungs:
        if P >= 2 and N - P - 1 > 5 and (N, P, G) not in seen:
            seen.add((N, P, G)); rung_list.append((N, P, G))
    mc = []
    for D in MCDRAWS:
        for N, P, G in rung_list:
            res = mc_rung(N, P, G, D, seed=11)
            mc.append(dict(draws=D, N=N, p=P, G=G, p_over_N=P / N, **res))
    MC = pd.DataFrame(mc)
    MC.to_csv(OUT / f"{STAMP}.montecarlo.csv", index=False)
    say("share of independent draws clearing the bar (a correct procedure sits at 0.050):")
    say(MC.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\nover all {len(MC)} rungs: naive-dof |t|>2 rate median {MC.naive.median():.4f}, "
        f"corrected-dof |t|>2 rate median {MC.correct.median():.4f}, "
        f"corrected dof at its OWN critical value median {MC.correct_tcrit.median():.4f}, "
        f"leave-one-out median {MC.loo.median():.4f}")
    say("")

    # ---------------- stage 3 -------------------------------------------
    say("## 3. FRESH BOOKS — the same question where (N, p) are known exactly")
    panels = {}
    panels["U56"] = load_universe()
    panels["B136"] = load_universe(broad=True)
    sp, ndrop = small_panel()
    panels[f"SMALL{sp.shape[1]-1}"] = sp
    say(f"small panel: dropped {ndrop} tickers with max_1d_move >= 1.0 per data/small_meta.csv; "
        f"{sp.shape[1]-1} names remain. SURVIVORSHIP: current constituents only.")

    arms, books, wf, keeps = [], [], [], []
    for pname, px in panels.items():
        tickers = [c for c in px.columns if c != "SPY"]
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        base = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
        v1 = backtest(px, rules_v1_weights(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
        h = len(spy) // 2
        ms, ms1, ms2 = three_metrics(spy, h)
        mb, mb1, mb2 = three_metrics(base, h)
        m1_, m11, m12 = three_metrics(v1, h)
        say(f"\n### {pname}: {len(tickers)} names, {px.index[0].date()}..{px.index[-1].date()}, "
            f"scored from {start.date()}")
        say(f"  SPY      {ms['CAGR']:.2%} / {ms['Sharpe']:.4f} / {ms['MaxDD']:.2%}   "
            f"halves {ms1['Sharpe']:.4f} / {ms2['Sharpe']:.4f}")
        say(f"  RULES v2 {mb['CAGR']:.2%} / {mb['Sharpe']:.4f} / {mb['MaxDD']:.2%}   "
            f"halves {mb1['Sharpe']:.4f} / {mb2['Sharpe']:.4f}")
        say(f"  RULES v1 {m1_['CAGR']:.2%} / {m1_['Sharpe']:.4f} / {m1_['MaxDD']:.2%}")

        def record(kind, label, n, gross, ret):
            m, m1, m2 = three_metrics(ret, h)
            p4a = (m1["Sharpe"] > mb1["Sharpe"] and m2["Sharpe"] > mb2["Sharpe"]
                   and m["MaxDD"] >= mb["MaxDD"])
            p4b = (m1["Sharpe"] > ms1["Sharpe"] and m2["Sharpe"] > ms2["Sharpe"]
                   and m["MaxDD"] >= 0.6 * ms["MaxDD"] and m["CAGR"] >= 0.7 * ms["CAGR"])
            row = dict(panel=pname, kind=kind, arm=label, n=n, gross=gross,
                       CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                       H1=m1["Sharpe"], H2=m2["Sharpe"], IS_CAGR=m1["CAGR"], OOS_CAGR=m2["CAGR"],
                       IS_MaxDD=m1["MaxDD"], OOS_MaxDD=m2["MaxDD"],
                       IS_vol=m1["Vol"], pass4a=p4a, pass4b=p4b,
                       SPY_Sharpe=ms["Sharpe"], SPY_CAGR=ms["CAGR"], SPY_MaxDD=ms["MaxDD"],
                       SPY_H1=ms1["Sharpe"], SPY_H2=ms2["Sharpe"], SPY_OOS_CAGR=ms2["CAGR"],
                       SPY_OOS_MaxDD=ms2["MaxDD"],
                       base_Sharpe=mb["Sharpe"], base_CAGR=mb["CAGR"], base_MaxDD=mb["MaxDD"],
                       base_H1=mb1["Sharpe"], base_H2=mb2["Sharpe"], base_OOS_CAGR=mb2["CAGR"],
                       base_OOS_MaxDD=mb2["MaxDD"])
            keeps.append(row)
            return row

        # --- ranked arms: the two tuned parameters -----------------------
        for n in NS:
            for gr in GROSS:
                ret = backtest(px, ranked_weights(px, tickers, n, gr),
                               cost_bps=COST, freq=FREQ)["returns"].loc[start:]
                arms.append(record("RANKED", f"top{n}_g{gr:.2f}", n, gr, ret))
        A = pd.DataFrame([a for a in arms if a["panel"] == pname])
        say("  ranked arms (all 12 grid points; n x gross are the only tuned parameters):")
        say(A[["arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "pass4a", "pass4b"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

        # --- rule 8: choose on the first half, read the second once ------
        pick = A.iloc[int(A.H1.values.argmax())]
        wf.append(dict(panel=pname, selector="IS_Sharpe_argmax", arm=pick.arm,
                       IS_Sharpe=pick.H1, OOS_Sharpe=pick.H2, OOS_CAGR=pick.OOS_CAGR,
                       OOS_MaxDD=pick.OOS_MaxDD, OOS_Sharpe_base=mb2["Sharpe"],
                       OOS_CAGR_base=mb2["CAGR"], OOS_MaxDD_base=mb2["MaxDD"],
                       OOS_Sharpe_SPY=ms2["Sharpe"], OOS_CAGR_SPY=ms2["CAGR"],
                       OOS_MaxDD_SPY=ms2["MaxDD"],
                       OOS_Sharpe_mean_arm=float(A.H2.mean())))
        say(f"  rule 8: IS-Sharpe argmax on the first half picks {pick.arm} "
            f"(IS {pick.H1:.4f}); OOS {pick.OOS_CAGR:.2%} / {pick.H2:.4f} / {pick.OOS_MaxDD:.2%} "
            f"vs RULES v2 {mb2['CAGR']:.2%}/{mb2['Sharpe']:.4f}/{mb2['MaxDD']:.2%} "
            f"vs SPY {ms2['CAGR']:.2%}/{ms2['Sharpe']:.4f}/{ms2['MaxDD']:.2%}")

        # --- random draw books, for the within-cell transfer regression ---
        for k in KDRAW:
            for i in range(NDRAW):
                rng = np.random.default_rng(1000 * k + i)
                names = list(rng.choice(tickers, size=min(k, len(tickers)), replace=False))
                ret = backtest(px, ew_weights(px, names), cost_bps=COST,
                               freq=FREQ)["returns"].loc[start:]
                books.append(record("DRAW", f"draw{k}_{i}", k, 1.00, ret))
        B = pd.DataFrame([b for b in books if b["panel"] == pname])
        say(f"  draw books: {len(B)}  4a {int(B.pass4a.sum())}/{len(B)}  4b {int(B.pass4b.sum())}/{len(B)}"
            f"   ranked arms 4a {int(A.pass4a.sum())}/{len(A)}  4b {int(A.pass4b.sum())}/{len(A)}")

    KP = pd.DataFrame(keeps)
    KP.to_csv(OUT / f"{STAMP}.keeppaths.csv", index=False)
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)

    # --- the within-cell transfer t on this run's own books, every dof convention
    say("\n### the within-cell transfer t of OOS Sharpe on IS Sharpe, this run's 360 draw books")
    say("cells are (panel, k) refined by q quantile bins of the book's OWN in-sample vol, so p")
    say("rises with q on the SAME rows; q is a treatment axis, not a tuned parameter.")
    D = pd.DataFrame(books).copy()
    D["IS_Sharpe"] = D.H1; D["OOS_Sharpe"] = D.H2
    wt = []
    for q in QBINS:
        d = D.copy()
        if q == 1:
            d["cell"] = d.panel + "|" + d.n.astype(str)
        else:
            d["vb"] = d.groupby(["panel", "n"]).IS_vol.transform(
                lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
            d["cell"] = d.panel + "|" + d.n.astype(str) + "|" + d.vb.astype(str)
        res = within_fit(d, "IS_Sharpe", "OOS_Sharpe", "cell", clustercol="panel", min_cell=2)
        wt.append(dict(q=q, **res))
    WT = pd.DataFrame(wt)
    WT.to_csv(OUT / f"{STAMP}.withint.csv", index=False)
    say(WT[["q", "N", "p", "dof_naive", "dof_correct", "slope", "R2", "t_naive", "t_correct",
            "inflation", "p_normal", "p_correct", "G", "t_cluster_pub", "t_cluster_CR1",
            "p_cluster_CR1"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    flip = WT[(WT.t_naive.abs() > 2) & (WT.t_correct.abs() <= 2)]
    say(f"\ngrid points where the dof charge alone crosses the record's |t|>2 bar: {len(flip)}/{len(WT)}")
    flip2 = WT[(WT.p_normal < 0.05) & (WT.p_correct >= 0.05)]
    say(f"grid points where the 5% verdict flips between the published NORMAL reference and "
        f"t(N-p-1): {len(flip2)}/{len(WT)}")
    flip3 = WT[(WT.p_cluster_pub < 0.05) & (WT.p_cluster_CR1 >= 0.05)]
    say(f"grid points where the cluster verdict flips between the record's SE+normal and "
        f"CR1+t(G-1): {len(flip3)}/{len(WT)}")

    say("\n## Rule 8 walk-forward (chosen on the first half, second half read once)")
    say(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\n## Both KEEP paths over every arm this run built")
    say(KP.groupby(["panel", "kind"])[["pass4a", "pass4b"]].agg(["sum", "size"]).to_string())
    say(f"TOTAL 4a {int(KP.pass4a.sum())}/{len(KP)}   4b {int(KP.pass4b.sum())}/{len(KP)}")
    if KP.pass4b.any():
        say("4b passers:")
        say(KP[KP.pass4b][["panel", "kind", "arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say(f"\nruntime {time.time()-t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_console) + "\n")

if __name__ == "__main__":
    main()

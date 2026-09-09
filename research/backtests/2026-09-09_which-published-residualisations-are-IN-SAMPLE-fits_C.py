#!/usr/bin/env python3
"""Idea 483 - WHICH PUBLISHED RESIDUALISATIONS ARE IN-SAMPLE FITS (lane C, 2026-09-09).

Idea 252 showed that the queue's own proposed control - ridge the 136-column membership
matrix and residualise - reports `kill` 0.000 at t -0.10 when it is fitted on the same 50
rows it is tested on, and 0.675 at t +6.19 when the fitted value is taken out of fold,
because the in-sample fit reproduces the regressor itself at R2 0.998-0.9996.  The queue
asks: how much of the record is exposed to that hazard?

The hazard is not "a regression appears in the script".  It is *p fitted parameters
estimated on the same N rows the fitted value is then tested against*.  For an OLS fit on
a design independent of the target, the in-sample R2 has expectation p/N whatever the data
say; the same number is the share of ANY regressor the control can absorb for free.  So
this run measures p and N at every fit in the record, not the presence of a fit.

Design
------
STAGE 0 (--sweep, slow, reproducible): every research/backtests/*.py that contains a
    linear-fit primitive is re-executed under an instrumented numpy - lstsq / solve / pinv
    / inv / polyfit are wrapped and log (N, p, file, line) per call - and inside a write
    sandbox that redirects every write under the repo into a scratch mirror, so the sweep
    cannot touch a committed artefact.  Output: `.runtime.csv` (committed).
STAGE 1 CENSUS: the runtime log is merged with a static AST pass (enclosing function, the
    innermost enclosing loop, out-of-fold and control/residualisation tokens near the call)
    -> `.census.csv`, one row per call site.
STAGE 2 THE LAW: E[R2] = p/N for an in-sample fit against an independent target, verified
    by Monte Carlo at the record's own (N, p) pairs -> `.freeR2.csv`.
STAGE 3 RE-RUN: every censused site above the p>10 bar that is a control fitted on its own
    test rows is refit OUT OF FOLD over the two tuned parameters -> `.rerun.csv`.
STAGE 4 RULE 8 + 4a/4b: the same control used as a SELECTOR on idea 78/83's committed 300
    B136 books - parameters chosen on 2009-2016 only, 2017-2026 untouched -> `.walkforward.csv`.

Two tuned parameters, every point reported: fold count K in {2, 5, 10, 25, 50} and ridge
penalty LAM in {0, 0.5, 2, 8, 32, 128, 512}.  Everything else - panel B136, seeds, draws,
k, n, gate, gross, cadence, cost rung, IS/OOS split - is idea 78/83's, imported unchanged.

No book is re-run: every book metric is read from idea 78's committed gridB.csv, gated
first.  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are untouched.

Usage:  python 2026-09-09_which-published-residualisations-are-IN-SAMPLE-fits_C.py [--sweep]
"""
import ast
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import warnings
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore", category=RuntimeWarning)
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score   # noqa: E402
from engine import backtest, metrics                                            # noqa: E402

# ---- idea 78/83's constants, imported verbatim -----------------------------------------
COST_BPS = 10
FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
KS = [20, 40, 80]
N_BOOK = 20
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SEED_B = 78_500

# ---- this run's two tuned parameters, both fully reported --------------------------------
FOLDS = [2, 5, 10, 25, 50]
LAMS = [0.0, 0.5, 2.0, 8.0, 32.0, 128.0, 512.0]
P_BAR = 10                     # the queue's "more than ~10 fitted parameters" bar
SEED_MC = 483_000
MC_CAP = 400                   # Monte Carlo sizes are capped at constant p/N (reported)

SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"
REF_GRIDB = OUT / "2026-09-05_candidate-count-vs-dispersion_B.gridB.csv"
REF_DRAWS = OUT / "2026-09-06_dispersion-as-a-survivorship-detector_B.draws.csv"
REF_252 = OUT / "2026-09-09_name-level-fixed-effects_B.regressions.csv"
RUNTIME_CSV = OUT / f"{STEM}.runtime.csv.gz"   # 302k rows; gzipped like the record's big panels

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


# =========================================================================================
# STAGE 0 - the instrumented sweep
# =========================================================================================
FIT_PRIM = re.compile(r"lstsq|linalg\.solve|pinv|linalg\.inv|polyfit|\.transform\(")

SITECUSTOMIZE = r'''
"""Instrument every linear fit; sandbox every write.  Written by idea 483's --sweep."""
import os, sys, json, atexit, traceback, io, builtins
ROOT = os.environ["FITROOT"]; MIRROR = os.environ["FITMIRROR"]; LOG = os.environ["FITLOG"]
RECS = []
def _redirect(p):
    try: s = os.fspath(p)
    except Exception: return p
    if not isinstance(s, str): return p
    a = os.path.abspath(s)
    if a.startswith(ROOT + "/"):
        t = os.path.join(MIRROR, a[len(ROOT) + 1:])
        os.makedirs(os.path.dirname(t), exist_ok=True)
        return t
    return p
def _site():
    for fr in reversed(traceback.extract_stack()[:-2]):
        if "/research/backtests/" in fr.filename:
            return os.path.basename(fr.filename), fr.lineno
    return "?", 0
def _rec(op, N, p):
    f, ln = _site(); RECS.append(dict(op=op, N=int(N), p=int(p), file=f, line=int(ln)))
import numpy as np
_lstsq, _solve, _pinv, _inv, _polyfit = (np.linalg.lstsq, np.linalg.solve, np.linalg.pinv,
                                         np.linalg.inv, np.polyfit)
def _sniff_N(p, gram):
    """solve/inv see only a p x p gram; recover N from the caller's own 2-D design."""
    fr = sys._getframe(2)
    for _ in range(4):
        if fr is None: break
        for v in list(fr.f_locals.values()):
            try:
                if v is gram: continue
                if hasattr(v, "ndim") and v.ndim == 2 and v.shape[1] == p and v.shape != gram.shape:
                    return int(v.shape[0])
            except Exception: pass
        fr = fr.f_back
    return -1
def lstsq(a, b, rcond=None):
    A = np.asarray(a); _rec("lstsq", A.shape[0] if A.ndim else 0, A.shape[1] if A.ndim > 1 else 1)
    return _lstsq(a, b, rcond=rcond)
def solve(a, b):
    A = np.asarray(a); pp = A.shape[-1] if A.ndim else 0
    _rec("solve", _sniff_N(pp, A), pp); return _solve(a, b)
def pinv(a, *ar, **kw):
    A = np.asarray(a); pp = A.shape[1] if A.ndim > 1 else 1
    # the record's OLS helpers call pinv(X.T @ X): the argument is a p x p GRAM, so its row
    # count is p, not the sample size.  Recover N from the caller's design, as for solve/inv.
    nn = _sniff_N(pp, A) if (A.ndim == 2 and A.shape[0] == A.shape[1]) else (
        A.shape[0] if A.ndim > 1 else 0)
    _rec("pinv", nn, pp)
    return _pinv(a, *ar, **kw)
def inv(a):
    A = np.asarray(a); pp = A.shape[-1] if A.ndim else 0
    _rec("inv", _sniff_N(pp, A), pp); return _inv(a)
def polyfit(x, y, deg, *ar, **kw):
    _rec("polyfit", len(np.asarray(x)), int(deg) + 1); return _polyfit(x, y, deg, *ar, **kw)
np.linalg.lstsq, np.linalg.solve, np.linalg.pinv, np.linalg.inv, np.polyfit = (
    lstsq, solve, pinv, inv, polyfit)
_open = builtins.open
def _sopen(file, mode="r", *a, **kw):
    if any(c in mode for c in "wxa+"): file = _redirect(file)
    return _open(file, mode, *a, **kw)
builtins.open = _sopen; io.open = _sopen
import pathlib
_wt, _wb, _mkdir = pathlib.Path.write_text, pathlib.Path.write_bytes, pathlib.Path.mkdir
pathlib.Path.write_text = lambda self, *a, **kw: _wt(pathlib.Path(_redirect(self)), *a, **kw)
pathlib.Path.write_bytes = lambda self, *a, **kw: _wb(pathlib.Path(_redirect(self)), *a, **kw)
def _smkdir(self, *a, **kw):
    try:
        return _mkdir(pathlib.Path(_redirect(self)) if str(self).startswith(ROOT)
                      and not self.exists() else self, *a, **kw)
    except Exception: return None
pathlib.Path.mkdir = _smkdir
try:
    import pandas as pd
    _tc, _stc = pd.DataFrame.to_csv, pd.Series.to_csv
    def dtc(self, path_or_buf=None, *a, **kw):
        if isinstance(path_or_buf, (str, os.PathLike)): path_or_buf = _redirect(path_or_buf)
        return _tc(self, path_or_buf, *a, **kw)
    def stc(self, path_or_buf=None, *a, **kw):
        if isinstance(path_or_buf, (str, os.PathLike)): path_or_buf = _redirect(path_or_buf)
        return _stc(self, path_or_buf, *a, **kw)
    pd.DataFrame.to_csv, pd.Series.to_csv = dtc, stc
except Exception: pass
try:
    import pandas as pd
    from pandas.core.groupby.generic import SeriesGroupBy as _SGB, DataFrameGroupBy as _DGB
    def _wrap_transform(cls, label):
        _t = cls.transform
        def transform(self, func, *a, **kw):
            try:
                nm = func if isinstance(func, str) else getattr(func, "__name__", "lambda")
                if nm in ("mean", "lambda", "<lambda>"):
                    _rec("gb_" + label + "_" + ("mean" if nm == "mean" else "lambda"),
                         int(len(self.obj)), int(self.ngroups))
            except Exception: pass
            return _t(self, func, *a, **kw)
        cls.transform = transform
    _wrap_transform(_SGB, "s"); _wrap_transform(_DGB, "d")
except Exception: pass
@atexit.register
def _dump():
    with _open(LOG, "w") as fh: json.dump(RECS, fh)
'''


def sweep(workdir, timeout=900, jobs=3):
    """Re-execute every fit-bearing backtest under instrumentation.  Writes RUNTIME_CSV."""
    work = Path(workdir)
    (work / "inst").mkdir(parents=True, exist_ok=True)
    (work / "logs").mkdir(parents=True, exist_ok=True)
    (work / "mirror").mkdir(parents=True, exist_ok=True)
    (work / "inst" / "sitecustomize.py").write_text(SITECUSTOMIZE)
    files = [f.name for f in sorted(OUT.glob("*.py"))
             if f.name != SCRIPT and FIT_PRIM.search(f.read_text())]
    P(f"    sweep: {len(files)} fit-bearing scripts, {jobs} at a time, timeout {timeout}s each")
    status, running = [], []

    def launch(fn):
        env = dict(os.environ, FITROOT=str(REPO), FITMIRROR=str(work / "mirror"),
                   FITLOG=str(work / "logs" / f"{fn}.json"), PYTHONPATH=str(work / "inst"))
        out = (work / "logs" / f"{fn}.out").open("w")
        return (fn, subprocess.Popen([sys.executable, str(OUT / fn)], cwd=str(REPO), env=env,
                                     stdout=out, stderr=subprocess.STDOUT), out, time.time())

    q = list(files)
    while q or running:
        while q and len(running) < jobs:
            running.append(launch(q.pop(0)))
        time.sleep(2)
        for item in list(running):
            fn, pr, fh, t0 = item
            if pr.poll() is None:
                if time.time() - t0 > timeout:
                    pr.kill(); pr.wait()
                else:
                    continue
            fh.close(); running.remove(item)
            status.append(dict(file=fn, rc=pr.returncode, secs=round(time.time() - t0, 1)))
    recs = []
    for st in status:
        j = work / "logs" / f"{st['file']}.json"
        if j.exists():
            for r in json.loads(j.read_text()):
                r["script"] = st["file"]
                recs.append(r)
        st["logged"] = j.exists()
    pd.DataFrame(status).to_csv(OUT / f"{STEM}.sweepstatus.csv", index=False)
    df = pd.DataFrame(recs)
    df.to_csv(RUNTIME_CSV, index=False)
    P(f"    sweep: {len(status)} scripts, rc==0 on {sum(s['rc'] == 0 for s in status)}, "
      f"{len(df)} instrumented fit calls -> {RUNTIME_CSV.name}")
    return df


# =========================================================================================
# STAGE 1 - static evidence at each call site
# =========================================================================================
OOF_TOK = re.compile(r"out[- _]of[- _]fold|\boof\b|\bfold\b|KFold|cross[_ -]?fit|hold[- ]?out|"
                     r"leave[- ]one[- ]out|\bloo\b|train_idx|te_idx|tr_idx|train\b|\btest_", re.I)
CTRL_TOK = re.compile(r"resid|partial|control|orthogon|demean|residualis|residualiz|net of", re.I)
_CACHE = {}


def _parsed(fname):
    if fname not in _CACHE:
        src = (OUT / fname).read_text()
        _CACHE[fname] = (src, ast.parse(src), src.split("\n"))
    return _CACHE[fname]


def static_site(fname, lineno):
    """Enclosing function, innermost enclosing loop, and the tokens around the call."""
    try:
        src, tree, lines = _parsed(fname)
    except Exception:
        return dict(func="?", loop="", oof_loop=False, oof_near=False, ctrl_near=False, line_src="")
    fn, loop = None, None
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and \
                n.lineno <= lineno <= (n.end_lineno or n.lineno):
            if fn is None or n.lineno > fn.lineno:
                fn = n
        if isinstance(n, (ast.For, ast.While)) and n.lineno <= lineno <= (n.end_lineno or n.lineno):
            if loop is None or n.lineno > loop.lineno:
                loop = n
    loop_hdr = lines[loop.lineno - 1].strip()[:110] if loop is not None else ""
    near = "\n".join(lines[max(0, lineno - 12):lineno + 12])
    return dict(func=fn.name if fn else "<module>", loop=loop_hdr,
                oof_loop=bool(OOF_TOK.search(loop_hdr)), oof_near=bool(OOF_TOK.search(near)),
                ctrl_near=bool(CTRL_TOK.search(near)), line_src=lines[lineno - 1].strip()[:130])


def census(rt):
    """One row per (script, file, line, op, p): call count, N, p/N, evidence."""
    rt = rt[(rt.script != SCRIPT) & (rt.file != SCRIPT)]      # this run is not the record
    rows = []
    for (sc, fl, ln, op, p), g in rt.groupby(["script", "file", "line", "op", "p"]):
        Ns = g["N"][g["N"] > 0]
        st = static_site(fl, int(ln))
        n_med = float(Ns.median()) if len(Ns) else np.nan
        rows.append(dict(script=sc, file=fl, line=int(ln), op=op, p=int(p), calls=len(g),
                         N_med=n_med, N_min=float(Ns.min()) if len(Ns) else np.nan,
                         N_max=float(Ns.max()) if len(Ns) else np.nan,
                         N_unknown=int((g["N"] <= 0).sum()),
                         free_R2=(p / n_med) if n_med and n_med > 0 else np.nan, **st))
    df = pd.DataFrame(rows)
    df["highdim"] = df["p"] > P_BAR
    df["oof_evidence"] = df["oof_loop"] | df["oof_near"]
    return df.sort_values(["p", "free_R2"], ascending=False).reset_index(drop=True)


# =========================================================================================
# STAGE 2 - the p/N law
# =========================================================================================
def free_r2_mc(pairs, draws=200, seed=SEED_MC, design="gauss"):
    """In-sample R2 of a p-column design against an INDEPENDENT target, at the record's own
    (N, p) pairs.  Nothing in the design knows the target, so E[R2] = p/N whatever the data
    say.  design='dummy' uses BALANCED GROUP INDICATORS - the group-mean (fixed-effect)
    residualisation the record performs with groupby().transform('mean'), which never touches
    np.linalg but is the same p-parameter in-sample fit."""
    rng = np.random.default_rng(seed)
    rows = []
    for N0, p0 in pairs:
        if not np.isfinite(N0):
            continue
        N, p = int(N0), int(p0)
        if N > MC_CAP:                       # simulate at the same p/N on a tractable size
            p = max(1, int(round(p * MC_CAP / N)))
            N = MC_CAP
        if N <= p + 1:                       # saturated: the fit reproduces ANY target exactly
            rows.append(dict(design=design, N=N, p=p, pred_pN=min(1.0, p / N),
                             mc_mean_R2=1.0, mc_q90_R2=1.0))
            continue
        r2s = np.empty(draws)
        for d in range(draws):
            if design == "dummy":
                g = np.arange(N) % p
                X = np.zeros((N, p)); X[np.arange(N), g] = 1.0
            else:
                X = np.column_stack([np.ones(N), rng.standard_normal((N, p - 1))]) if p > 1 \
                    else np.ones((N, 1))
            y = rng.standard_normal(N)
            b, *_ = np.linalg.lstsq(X, y, rcond=None)
            e = y - X @ b
            r2s[d] = 1 - e @ e / ((y - y.mean()) @ (y - y.mean()))
        rows.append(dict(design=design, N=N, p=p, pred_pN=p / N,
                         mc_mean_R2=r2s.mean(), mc_q90_R2=np.quantile(r2s, .9)))
    return pd.DataFrame(rows)


# =========================================================================================
# ridge / fold machinery (idea 252's ridge_fit, re-implemented and gated against its output)
# =========================================================================================
def ridge_fit(X, y, lam, free=0):
    """Ridge with an unpenalised intercept and `free` leading unpenalised columns; X is
    centred internally.  Idea 252's `ridge_fit`, re-implemented and gated against its output."""
    X = np.asarray(X, float); y = np.asarray(y, float)
    xm = X.mean(axis=0); Xc = X - xm; ym = y.mean()
    D = np.ones(Xc.shape[1]) * lam
    if free:
        D[:free] = 0.0
    A = Xc.T @ Xc + np.diag(D)
    b = Xc.T @ (y - ym)
    try:
        beta = np.linalg.solve(A, b)                 # lam > 0: A is positive definite
    except np.linalg.LinAlgError:
        beta = np.linalg.pinv(A) @ b                 # lam = 0 with p >= N: minimum-norm OLS
    return ym, xm, beta


def ridge_pred(X, fit):
    ym, xm, beta = fit
    return ym + (np.asarray(X, float) - xm) @ beta


def fitted(X, y, lam, folds, free=0):
    """folds<=1 -> IN-SAMPLE fitted values (fitted on the same rows they are read on).
    folds>=2 -> OUT-OF-FOLD fitted values, deterministic interleaved folds by row index."""
    X = np.asarray(X, float); y = np.asarray(y, float); n = len(y)
    if folds is None or folds <= 1:
        return ridge_pred(X, ridge_fit(X, y, lam, free))
    idx = np.arange(n) % folds
    out = np.empty(n)
    for f in range(folds):
        te = idx == f; tr = ~te
        if tr.sum() < 2:
            out[te] = y[tr].mean() if tr.sum() else y.mean()
            continue
        out[te] = ridge_pred(X[te], ridge_fit(X[tr], y[tr], lam, free))
    return out


def r2(y, yhat):
    y = np.asarray(y, float); yhat = np.asarray(yhat, float)
    ss = ((y - y.mean()) ** 2).sum()
    return 1 - ((y - yhat) ** 2).sum() / ss if ss > 0 else np.nan


def ols(y, X):
    """OLS with an intercept; returns (beta, t-stats, R2)."""
    y = np.asarray(y, float)
    Xm = np.column_stack([np.ones(len(y))] + [np.asarray(c, float) for c in X])
    b, *_ = np.linalg.lstsq(Xm, y, rcond=None)
    e = y - Xm @ b
    dof = len(y) - Xm.shape[1]
    s2 = e @ e / dof if dof > 0 else np.nan
    XtX = np.linalg.pinv(Xm.T @ Xm)
    se = np.sqrt(np.diag(XtX) * s2)
    return b, b / se, r2(y, Xm @ b)


def partial_r2(y, x, ctrl):
    """R2 of x in a model that already contains ctrl (the record's `pR2`), and its t."""
    b0, t0, r_full = ols(y, [x] + ctrl)
    _, _, r_ctrl = ols(y, ctrl) if ctrl else (None, None, 0.0)
    return (r_full - r_ctrl) / (1 - r_ctrl) if r_ctrl < 1 else np.nan, t0[1], r_full, r_ctrl


# =========================================================================================
# helpers for the book leg (idea 78's, imported unchanged)
# =========================================================================================
def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def main():
    t0 = time.time()
    do_sweep = "--sweep" in sys.argv
    P("=" * 210)
    P("Idea 483 - WHICH PUBLISHED RESIDUALISATIONS ARE IN-SAMPLE FITS  (lane C, 2026-09-09)")
    P("A control is dangerous when p fitted parameters are estimated on the same N rows the")
    P("fitted value is tested on; the free R2 is p/N.  This run measures p and N at every fit")
    P("in the record, then refits the ones over the queue's p>10 bar out of fold.")
    P("=" * 210)

    # ------------------------------------------------------------------ STAGE 0
    P("\n[0] RUNTIME SWEEP")
    if do_sweep:
        work = Path(os.environ.get("IDEA483_WORK", "/tmp/idea483_sweep"))
        rt = sweep(work)
    else:
        if not RUNTIME_CSV.exists():
            P(f"    ABORT: {RUNTIME_CSV.name} missing - re-run once with --sweep."); return
        rt = pd.read_csv(RUNTIME_CSV)
        P(f"    reading committed {RUNTIME_CSV.name}: {len(rt)} instrumented fit calls "
          f"in {rt['script'].nunique()} scripts (regenerate with --sweep)")
    st_path = OUT / f"{STEM}.sweepstatus.csv"
    if st_path.exists():
        stt = pd.read_csv(st_path)
        P(f"    sweep status: {len(stt)} scripts executed, rc==0 on {(stt.rc == 0).sum()}, "
          f"nonzero/killed on {(stt.rc != 0).sum()}, median {stt.secs.median():.0f}s, "
          f"total {stt.secs.sum() / 60:.1f} min")
        if (stt.rc != 0).any():
            P("    scripts that did not exit 0 (their fit calls up to the failure are still logged):")
            for _, r in stt[stt.rc != 0].iterrows():
                P(f"      rc={r.rc:<5} {r.secs:>6.0f}s  {r.file}")

    # ------------------------------------------------------------------ STAGE 1
    P("\n[1] CENSUS - every instrumented fit call site in the record")
    cen = census(rt)
    cen.to_csv(OUT / f"{STEM}.census.csv", index=False)
    P(f"    {len(cen)} distinct (script, file, line, op, p) sites, {int(cen.calls.sum())} calls, "
      f"{cen.script.nunique()} scripts")
    P(f"    p distribution over sites: " +
      "  ".join(f"p={int(k)}:{v}" for k, v in cen.p.value_counts().sort_index().items() if k <= 12) +
      f"   p>12: {(cen.p > 12).sum()}")
    known = cen[cen.N_med.notna()]
    P(f"    N recovered at {len(known)}/{len(cen)} sites; free R2 = p/N_median quantiles: " +
      "  ".join(f"q{int(q*100)}={known.free_R2.quantile(q):.4f}" for q in (0.5, 0.9, 0.99, 1.0)))
    P(f"    sites over the queue's p>{P_BAR} bar: {int(cen.highdim.sum())}"
      f"   ({cen[cen.highdim].script.nunique()} scripts)")
    if cen.highdim.any():
        cols = ["script", "line", "op", "p", "calls", "N_med", "free_R2",
                "oof_evidence", "ctrl_near", "func", "line_src"]
        ob = cen[cen.highdim].sort_values("p", ascending=False)
        P(f"\n    the 30 largest of the {len(ob)} sites over the bar (all {len(ob)} are in "
          f"{STEM}.census.csv):")
        P(ob.head(30)[cols].to_string(index=False, max_colwidth=46,
                                      float_format=lambda x: f"{x:.3f}"))
    # ---- 1b: the ARTEFACT census - what the record actually publishes as a "control"
    import gzip
    RES = re.compile(r"resid|orthog|demean", re.I)
    CTL = re.compile(r"ctrl|control", re.I)
    art, ncsv = [], 0
    for f in sorted(OUT.glob("*.csv")) + sorted(OUT.glob("*.csv.gz")):
        if f.name.startswith(STEM):          # this run's own artefacts are not the record
            continue
        ncsv += 1
        try:
            op = gzip.open(f, "rt") if f.suffix == ".gz" else f.open()
            with op as fh:
                head = fh.readline().strip()
        except Exception:
            continue
        cs = [c.strip('"') for c in head.split(",")]
        r = [c for c in cs if RES.search(c)]
        c = [c for c in cs if CTL.search(c)]
        if r or c:
            art.append(dict(file=f.name, resid_cols=";".join(r), ctrl_cols=";".join(c[:6]),
                            n_resid=len(r), n_ctrl=len(c)))
    ART = pd.DataFrame(art)
    ART.to_csv(OUT / f"{STEM}.artefacts.csv", index=False)
    P(f"\n    [1b] ARTEFACT CENSUS - {ncsv} committed CSVs scanned for a published control column:")
    P(f"    {int((ART.n_ctrl > 0).sum())} files carry a control-BOOK column (ctrl/control): a matched")
    P(f"        comparand BACKTEST, which fits no parameters and cannot absorb a regressor.")
    P(f"    {int((ART.n_resid > 0).sum())} files carry a RESIDUAL column; these are the candidates.")
    fitted_scripts = set(cen.script.str[:-3])
    ART["producer_fits"] = ART.file.map(lambda s: any(s.startswith(k) for k in fitted_scripts))
    rr = ART[ART.n_resid > 0]
    P(f"        of those, {int(rr.producer_fits.sum())} were produced by a script the runtime sweep")
    P(f"        saw fit anything at all; the other {int((~rr.producer_fits).sum())} are ARITHMETIC")
    P(f"        residuals (decomposition identities: total - timing - composition), p = 0.")
    P("        residual columns published, by name:")
    P("        " + "  ".join(sorted({c for s in rr.resid_cols for c in s.split(";") if c})[:26]))

    # ---- 1c: what the runtime instrument cannot see, counted statically
    allpy = sorted(OUT.glob("*.py"))
    cov_re = re.compile(r"np\.corrcoef|np\.cov\(|\.cov\(\)|\.corr\(")
    n_cov = sum(1 for f in allpy if f.name != SCRIPT and cov_re.search(f.read_text()))
    n_prim = sum(1 for f in allpy if f.name != SCRIPT and FIT_PRIM.search(f.read_text()))
    P(f"\n    [1c] COVERAGE - {len(allpy) - 1} committed backtest scripts; {n_prim} contain a fit")
    P(f"    primitive or a groupby transform and were swept.  A further {n_cov} compute a")
    P(f"    correlation or covariance beta, which is a TWO-parameter in-sample fit by construction")
    P(f"    (free R2 = 2/N) and so cannot cross the p>{P_BAR} bar however it is counted.")

    # ---- 1d: p>10 is necessary, not sufficient.  Which over-bar sites are ONE-SIDED?
    hi = cen[cen.highdim].copy()
    grp = hi.groupby(["script", "func", "p", "N_med", "op"]).size().rename("twin")
    hi = hi.join(grp, on=["script", "func", "p", "N_med", "op"])
    hi["sided"] = np.where(hi.twin >= 2, "two-sided (within transform)", "ONE-SIDED")
    hi.to_csv(OUT / f"{STEM}.highdim.csv", index=False)
    P("\n    [1d] p>10 IS NECESSARY, NOT SUFFICIENT.  The hazard idea 252 found needs the fitted")
    P("    value to be used ONE-SIDED - as a regressor whose coefficient is then tested, or as a")
    P("    residual read as signal - on the rows it was fitted on.  When the SAME fit is removed")
    P("    from BOTH the regressor and the target (the Frisch-Waugh within transform), the")
    P("    in-sample fit IS the estimator and 'refit it out of fold' is the wrong question; the")
    P("    only cost is p degrees of freedom.  Sites are called two-sided when the same script,")
    P("    function, op, p and N carry two or more fits (x and y demeaned by the same groups).")
    P(hi.groupby(["sided", "op"]).agg(sites=("p", "size"), scripts=("script", "nunique"),
                                      p_min=("p", "min"), p_max=("p", "max"),
                                      free_R2_max=("free_R2", "max")).to_string(
        float_format=lambda x: f"{x:.3f}"))
    one = hi[hi.sided == "ONE-SIDED"]
    P(f"    ONE-SIDED over-bar sites: {len(one)} in {one.script.nunique()} script(s) - "
      f"{', '.join(sorted(one.script.unique()))}")

    P("\n    the 12 sites with the largest free R2 = p/N (the hazard is p/N, not p):")
    P(known.nlargest(12, "free_R2")[["script", "line", "op", "p", "N_med", "free_R2",
                                     "oof_evidence", "ctrl_near", "line_src"]]
      .to_string(index=False, max_colwidth=48, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------------ STAGE 2
    P("\n[2] THE LAW - what an in-sample fit absorbs for free")
    pairs = sorted({(int(r.N_med), int(r.p)) for _, r in known.iterrows()})
    worst = known.nlargest(1, "free_R2").iloc[0]
    bigp = known.nlargest(1, "p").iloc[0]
    pick = sorted({pairs[int(q * (len(pairs) - 1))] for q in (0.0, 0.25, 0.5, 0.75, 0.9, 1.0)}
                  | {(int(worst.N_med), int(worst.p)), (int(bigp.N_med), int(bigp.p)),
                     (150, 138), (50, 136)})
    gbp = known[known.op.str.startswith("gb_")]
    if len(gbp):
        w = gbp.nlargest(1, "free_R2").iloc[0]
        pick = sorted(set(pick) | {(int(w.N_med), int(w.p))})
    mc = pd.concat([free_r2_mc(pick, design="gauss"),
                    free_r2_mc(pick, design="dummy")], ignore_index=True)
    mc.to_csv(OUT / f"{STEM}.freeR2.csv", index=False)
    P(f"    Monte Carlo (200 draws): in-sample R2 of a p-column design against an INDEPENDENT target.")
    P(f"    Sizes above N={MC_CAP} are simulated at the same p/N on {MC_CAP} rows (the law is in p/N).")
    P("    'gauss' = a continuous design, 'dummy' = balanced group indicators (the groupby-mean")
    P("    residualisation).  Both obey E[R2] = p/N; the fit knows nothing about the target.")
    P(mc.pivot_table(index=["N", "p", "pred_pN"], columns="design",
                     values=["mc_mean_R2", "mc_q90_R2"]).to_string(float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------------ the reconstructible panel
    P("\n[a] GATE - idea 78/83's committed grid re-read before anything new is computed")
    if not (REF_GRIDB.exists() and REF_DRAWS.exists()):
        P("    ABORT: idea 78/83's committed CSVs are missing."); return
    G = pd.read_csv(REF_GRIDB)
    B = pd.read_csv(REF_DRAWS)
    px136 = load_universe(broad=True)
    names136 = list(px136.columns)
    startb = px136.index[260]
    px_n = px136[names136].loc[startb:]
    def ann_logret(p):                       # idea 83's, verbatim
        out = {}
        for c in p.columns:
            s = p[c].dropna()
            if len(s) < 252 or s.iloc[0] <= 0:
                out[c] = np.nan; continue
            out[c] = float(np.log(s.iloc[-1] / s.iloc[0]) /
                           ((s.index[-1] - s.index[0]).days / 365.25))
        return pd.Series(out)

    lr_full = ann_logret(px_n)
    draw_cols = {}
    for k in KS:
        rng = np.random.default_rng(SEED_B + k)
        for d in range(50):
            draw_cols[(k, d)] = list(rng.choice(names136, size=k, replace=False))
    dmax = 0.0
    for _, r in B.iterrows():
        cols = draw_cols[(int(r.k), int(r.draw))]
        dmax = max(dmax, abs(float(lr_full[cols].mean()) - float(r["W"])))
    P(f"    [b] membership re-drawn from SEED_B+k and idea 83's W column recomputed: "
      f"max abs diff {dmax:.3e} over {len(B)} rows -> M is idea 83's own membership matrix")
    num = [c for c in G.columns if pd.api.types.is_numeric_dtype(G[c]) and c in B.columns]
    dg = max(float(np.abs(G[c].values - B[c].values).max()) for c in num)
    P(f"    [c] gridB.csv vs draws.csv over {len(num)} shared numeric columns: max abs diff {dg:.3e}")
    nm_idx = {c: i for i, c in enumerate(names136)}
    Mall = {}
    for (k, d), cols in draw_cols.items():
        v = np.zeros(len(names136))
        for c in cols:
            v[nm_idx[c]] = 1.0
        Mall[(k, d)] = v
    P(f"    panel {px136.shape[1]} columns, window {startb.date()} -> {px136.index[-1].date()}, "
      f"{len(names136)} name columns x 50 draws per k cell")

    # ------------------------------------------------------------------ STAGE 3
    P("\n[3] RE-RUN - the record's over-the-bar control, refit OUT OF FOLD over the two tuned parameters")
    P("    Site: the 136-column membership ridge (idea 252's control).  y = a draw's book Sharpe on")
    P("    B136, x = the draw's dispersion sd, control = the ridge fit of y on M (+2 unpenalised k")
    P("    dummies in the pooled scope, idea 252's design).  folds=1 is the IN-SAMPLE fit - fitted on")
    P("    the same rows it is read on; folds>=2 is out of fold.  kill = pR2(sd|F)/R2(sd), idea 252's")
    P("    column: it is the SURVIVING share of sd's univariate R2, and its bar is kill < 1/3.")

    YCOLS = [("Sharpe", "CAND Sharpe"), ("ew_Sharpe", "EWall Sharpe"), ("premium", "premium")]
    SCOPES = [("pooled", None)] + [(f"k={k}", k) for k in KS]

    def cell_rows(nb, k):
        if k is None:
            s = B[B.n == nb].sort_values(["k", "draw"])
            M = np.array([Mall[(int(r.k), int(r.draw))] for _, r in s.iterrows()])
            kd = np.column_stack([(s.k.values == KS[1]).astype(float),
                                  (s.k.values == KS[2]).astype(float)])
            return s, np.column_stack([kd, M]), 2
        s = B[(B.n == nb) & (B.k == k)].sort_values("draw")
        return s, np.array([Mall[(k, int(r.draw))] for _, r in s.iterrows()]), 0

    rows = []
    for nb in (5, 20):
        for scope, k in SCOPES:
            s, M, free = cell_rows(nb, k)
            sdv = s["sd"].values
            # how much of sd ITSELF the control carries - does not depend on y, so fit it once
            sd_on_F = {(lam, K): r2(sdv, fitted(M, sdv, lam, K, free))
                       for lam in LAMS for K in [1] + FOLDS}
            for ycol, ylab in YCOLS:
                yv = s[ycol].values
                _, t_u, r2_u = ols(yv, [sdv])
                for lam in LAMS:
                    for K in [1] + FOLDS:
                        F = fitted(M, yv, lam, K, free)
                        pr2, t_sd, _, _ = partial_r2(yv, sdv, [F])
                        rows.append(dict(n=nb, scope=scope, y=ylab, N=len(s), p=M.shape[1],
                                         lam=lam, folds=K, scheme="IS" if K == 1 else f"OOF{K}",
                                         R2_sd=r2_u, t_sd=t_u[1], R2_F=r2(yv, F),
                                         R2_sd_on_F=sd_on_F[(lam, K)],
                                         pR2_sd_given_F=pr2, t_sd_given_F=t_sd,
                                         kill_F=pr2 / r2_u if r2_u > 0 else np.nan))
    RR = pd.DataFrame(rows)
    RR.to_csv(OUT / f"{STEM}.rerun.csv", index=False)
    P(f"    {len(RR)} grid points = 2 book sizes x 4 scopes x 3 y-columns x {len(LAMS)} penalties "
      f"x {len(FOLDS) + 1} schemes, ALL committed to {STEM}.rerun.csv")

    # --- gate [d]: idea 252's committed regressions.csv reproduced on its own grid
    if REF_252.exists():
        ref = pd.read_csv(REF_252)
        mine = RR[RR.folds.isin([1, 10])].copy()
        mine["scheme252"] = np.where(mine.folds == 1, "IS", "OOF")
        key = ["n", "scope", "y", "lam", "scheme252"]
        ref2 = ref.rename(columns={"scheme": "scheme252"})
        j = mine.merge(ref2, on=key, suffixes=("", "_ref"))
        diffs = {c: float(np.abs(j[c] - j[f"{c}_ref"]).max())
                 for c in ["R2_sd", "t_sd", "R2_F", "pR2_sd_given_F", "t_sd_given_F", "kill_F"]}
        P(f"    [d] idea 252's regressions.csv reproduced on {len(j)}/{len(ref)} of its rows "
          f"(this run's folds=10 == its OOF): max abs diff " +
          "  ".join(f"{c} {v:.2e}" for c, v in diffs.items()))
    else:
        P("    [d] idea 252's regressions.csv absent - gate skipped")

    head = RR[(RR.n == N_BOOK) & (RR.scope == "pooled") & (RR.y == "CAND Sharpe")]
    P(f"\n    HEADLINE CELL (n=20, pooled, CAND Sharpe; N={int(head.N.iloc[0])} rows, "
      f"p={int(head.p.iloc[0])} fitted parameters, p/N = {head.p.iloc[0] / head.N.iloc[0]:.2f}):")
    P(head[["lam", "scheme", "folds", "R2_F", "R2_sd_on_F", "pR2_sd_given_F", "t_sd_given_F",
            "kill_F"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    isr, oofr = RR[RR.folds == 1], RR[RR.folds != 1]
    P(f"\n    ALL {len(RR)} points.  IN-SAMPLE: R2(sd~M) median {isr.R2_sd_on_F.median():.4f}, "
      f"kill median {isr.kill_F.median():.3f}, kill<1/3 on {(isr.kill_F < 1/3).sum()}/{len(isr)}, "
      f"|t(sd|F)|<2 on {(isr.t_sd_given_F.abs() < 2).sum()}/{len(isr)}")
    P(f"    OUT OF FOLD:  R2(sd~M) median {oofr.R2_sd_on_F.median():.4f}, "
      f"kill median {oofr.kill_F.median():.3f}, kill<1/3 on {(oofr.kill_F < 1/3).sum()}/{len(oofr)}, "
      f"|t(sd|F)|<2 on {(oofr.t_sd_given_F.abs() < 2).sum()}/{len(oofr)}")
    P("\n    FOLD-COUNT SENSITIVITY (idea 252 ran K=10 only) - headline cell, kill_F by (lam, K):")
    P(head.pivot_table(index="lam", columns="folds", values="kill_F")
      .to_string(float_format=lambda x: f"{x:.3f}"))
    P("    same, |t(sd|F)|:")
    P(head.assign(at=head.t_sd_given_F.abs()).pivot_table(index="lam", columns="folds", values="at")
      .to_string(float_format=lambda x: f"{x:.2f}"))
    fl = []
    for key, g in RR.groupby(["n", "scope", "y", "lam"], sort=False):
        is_killed = bool(g[g.folds == 1].kill_F.iloc[0] < 1 / 3)
        oof_killed = g[g.folds != 1].kill_F < 1 / 3
        fl.append(dict(zip(["n", "scope", "y", "lam"], key), is_killed=is_killed,
                       oof_killed_all=bool(oof_killed.all()), oof_killed_any=bool(oof_killed.any()),
                       moves=is_killed != bool(oof_killed.any())))
    FL = pd.DataFrame(fl)
    P(f"\n    VERDICT MOVEMENT (bar: kill<1/3 means 'the control kills sd').  The in-sample fit and")
    P(f"    the out-of-fold refit disagree on {int(FL.moves.sum())}/{len(FL)} (n, scope, y, lam) cells:")
    P(f"      in sample the control kills sd on {int(FL.is_killed.sum())}/{len(FL)} cells;")
    P(f"      out of fold it kills sd on {int(FL.oof_killed_any.sum())}/{len(FL)} cells at ANY fold count,")
    P(f"      and on {int(FL.oof_killed_all.sum())}/{len(FL)} at EVERY fold count.")

    # ------------------------------------------------------------------ STAGE 3b
    P("\n[3b] THE OTHER FAMILY - the two-sided within transform, priced instead of refitted")
    P("    A cell-demeaning removes p cell means from x AND from y.  The slope is then the WITHIN")
    P("    estimator and is unbiased, so there is nothing to refit out of fold - but it costs p")
    P("    degrees of freedom, and a t read with dof = N-2 instead of N-p-1 is overstated by")
    P("    sqrt((N-2)/(N-p-1)).  This is the whole exposure of the record's over-bar sites.")
    two = hi[hi.sided != "ONE-SIDED"].dropna(subset=["N_med"]).copy()
    two = two[two.N_med > two.p + 2]
    two["t_inflation"] = np.sqrt((two.N_med - 2) / (two.N_med - two.p - 1))
    P(f"    {len(two)} two-sided over-bar sites with N recovered: t inflation median "
      f"{two.t_inflation.median():.4f}, q90 {two.t_inflation.quantile(0.9):.4f}, "
      f"max {two.t_inflation.max():.4f} (at p={int(two.loc[two.t_inflation.idxmax(), 'p'])}, "
      f"N={int(two.loc[two.t_inflation.idxmax(), 'N_med'])})")
    P("    worst 5 sites by t inflation:")
    P(two.nlargest(5, "t_inflation")[["script", "line", "p", "N_med", "free_R2", "t_inflation"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}", max_colwidth=52))

    rng = np.random.default_rng(SEED_MC + 1)
    mcrows = []
    for _, r in two.nlargest(3, "free_R2").iterrows():
        N, p = int(r.N_med), int(r.p)
        N = min(N, 6000)                                   # cap the simulation, report the cap
        p = max(2, int(round(p * N / max(int(r.N_med), 1))))
        nfp_naive = nfp_corr = nfp_loo = 0
        dr = 200
        for _ in range(dr):
            cell = np.sort(rng.integers(0, p, N))
            x, y = rng.standard_normal(N), rng.standard_normal(N)
            df_ = pd.DataFrame(dict(cell=cell, x=x, y=y))
            mx = df_.groupby("cell").x.transform("mean"); my = df_.groupby("cell").y.transform("mean")
            sz = df_.groupby("cell").x.transform("size")
            xd, yd = x - mx, y - my
            sxx = (xd ** 2).sum()
            b = (xd * yd).sum() / sxx
            e = yd - b * xd
            for dof, hit in (("naive", "n"), ("corr", "c")):
                d_ = (N - 2) if dof == "naive" else (N - p - 1)
                se = np.sqrt((e ** 2).sum() / max(d_, 1) / sxx)
                t = b / se if se > 0 else 0.0
                if abs(t) > 2:
                    if dof == "naive": nfp_naive += 1
                    else: nfp_corr += 1
            keep = sz > 1                                   # leave-one-out cell means
            xl = np.where(keep, (x - mx) * sz / np.maximum(sz - 1, 1), 0.0)
            yl = np.where(keep, (y - my) * sz / np.maximum(sz - 1, 1), 0.0)
            sxxl = (xl ** 2).sum()
            bl = (xl * yl).sum() / sxxl if sxxl > 0 else 0.0
            el = yl - bl * xl
            sel = np.sqrt((el ** 2).sum() / max(N - 2, 1) / sxxl) if sxxl > 0 else np.inf
            if sel > 0 and abs(bl / sel) > 2:
                nfp_loo += 1
        mcrows.append(dict(N=N, p=p, draws=dr, fp_naive_dof=nfp_naive / dr,
                           fp_correct_dof=nfp_corr / dr, fp_leave_one_out=nfp_loo / dr))
    MC2 = pd.DataFrame(mcrows)
    MC2.to_csv(OUT / f"{STEM}.withindof.csv", index=False)
    P("\n    Monte Carlo, x and y INDEPENDENT, cells random (200 draws): share of draws whose")
    P("    within-cell slope clears |t|>2.  A correct procedure sits at 0.05.")
    P(MC2.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------------ STAGE 4
    P("\n[4] RULE 8 - the SAME control as a SELECTOR, parameters chosen on 2009-2016, 2017-2026 untouched")
    spy = px136["SPY"].pct_change().fillna(0).loc[startb:]
    spy_oos = spy.loc[OOS_START:]
    sh1, sh2 = half_sharpes(spy)
    ms = metrics(spy)
    v2 = backtest(px136, rules_v2_weights(px136), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[startb:]
    v1 = backtest(px136, rules_v1_weights(px136), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[startb:]
    b1, b2 = half_sharpes(v2)
    mv2 = metrics(v2)
    P(f"    SPY        {ms['CAGR']:.2%} / {ms['Sharpe']:.3f} / {ms['MaxDD']:.2%}  halves "
      f"{sh1:.3f}/{sh2:.3f}  OOS Sharpe {metrics(spy_oos)['Sharpe']:.3f} "
      f"OOS CAGR {metrics(spy_oos)['CAGR']:.2%} OOS MaxDD {metrics(spy_oos)['MaxDD']:.2%}")
    P(f"    RULES v2   {mv2['CAGR']:.2%} / {mv2['Sharpe']:.3f} / {mv2['MaxDD']:.2%}  halves "
      f"{b1:.3f}/{b2:.3f}  OOS Sharpe {metrics(v2.loc[OOS_START:])['Sharpe']:.3f} "
      f"OOS CAGR {metrics(v2.loc[OOS_START:])['CAGR']:.2%} OOS MaxDD {metrics(v2.loc[OOS_START:])['MaxDD']:.2%}")
    mv1 = metrics(v1)
    P(f"    RULES v1   {mv1['CAGR']:.2%} / {mv1['Sharpe']:.3f} / {mv1['MaxDD']:.2%}  (continuity row)")

    def fails(r):
        """4a against the live RULES v2, 4b against SPY - PROTOCOL 4, on committed columns."""
        f4a = []
        if not r.H1 > b1: f4a.append("H1")
        if not r.H2 > b2: f4a.append("H2")
        if not r.MaxDD >= mv2["MaxDD"]: f4a.append("DD")
        f4b = []
        if not r.H1 > sh1: f4b.append("H1")
        if not r.H2 > sh2: f4b.append("H2")
        if not r.Sharpe_OOS > metrics(spy_oos)["Sharpe"]: f4b.append("OOS")
        if not r.MaxDD >= 0.60 * ms["MaxDD"]: f4b.append("DD")
        if not r.CAGR >= 0.70 * ms["CAGR"]: f4b.append("CAGR")
        return (",".join(f4a) or "-"), (",".join(f4b) or "-")

    P("    Every selector below reads ONLY the IS window (Sharpe_IS, sd_IS, membership); the OOS")
    P("    columns are idea 78's committed 2017-2026 numbers and are touched only to score the pick.")
    P("    CTRL-fit picks the draw with the largest fitted composition; SD-resid picks the draw that")
    P("    most beats what the control predicts for it - the residual the record reads as 'signal'.")
    wf = []
    for K in [1] + FOLDS:
        for lam in LAMS:
            for k in KS:
                cell = B[(B.n == N_BOOK) & (B.k == k)].sort_values("draw").reset_index(drop=True)
                Mc = np.array([Mall[(k, int(r.draw))] for _, r in cell.iterrows()])
                yIS = cell["Sharpe_IS"].values           # IS window only - rule 8
                F = fitted(Mc, yIS, lam, K)
                for nm, sc in (("CTRL-fit", F), ("SD-resid", yIS - F)):
                    r = cell.iloc[int(np.argmax(sc))]
                    f4a, f4b = fails(r)
                    wf.append(dict(selector=nm, scheme="IS" if K == 1 else f"OOF{K}", folds=K,
                                   lam=lam, k=k, draw=int(r.draw), IS_Sharpe=r.Sharpe_IS,
                                   OOS_Sharpe=r.Sharpe_OOS, OOS_CAGR=r.CAGR_OOS,
                                   OOS_MaxDD=r.MaxDD_OOS, full_Sharpe=r.Sharpe, full_MaxDD=r.MaxDD,
                                   OOS_rank=int((cell.Sharpe_OOS > r.Sharpe_OOS).sum()) + 1,
                                   cell_mean_OOS=cell.Sharpe_OOS.mean(), f4a=f4a, f4b=f4b))
    for k in KS:                                        # references that fit nothing
        cell = B[(B.n == N_BOOK) & (B.k == k)].sort_values("draw").reset_index(drop=True)
        for nm, sc in (("RAW-sd (no control)", cell["sd_IS"].values),
                       ("IS-Sharpe argmax (incumbent)", cell["Sharpe_IS"].values)):
            r = cell.iloc[int(np.argmax(sc))]
            f4a, f4b = fails(r)
            wf.append(dict(selector=nm, scheme="none", folds=0, lam=np.nan, k=k, draw=int(r.draw),
                           IS_Sharpe=r.Sharpe_IS, OOS_Sharpe=r.Sharpe_OOS, OOS_CAGR=r.CAGR_OOS,
                           OOS_MaxDD=r.MaxDD_OOS, full_Sharpe=r.Sharpe, full_MaxDD=r.MaxDD,
                           OOS_rank=int((cell.Sharpe_OOS > r.Sharpe_OOS).sum()) + 1,
                           cell_mean_OOS=cell.Sharpe_OOS.mean(), f4a=f4a, f4b=f4b))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(f"    {len(WF)} walk-forward rows = 2 fitted selectors x {len(FOLDS) + 1} schemes x {len(LAMS)}"
      f" penalties x 3 k cells + 2 no-fit references x 3 k cells -> {STEM}.walkforward.csv")
    agg = (WF.groupby(["selector", "scheme"])
             .agg(n=("draw", "size"), OOS_Sharpe=("OOS_Sharpe", "mean"),
                  OOS_CAGR=("OOS_CAGR", "mean"), OOS_MaxDD=("OOS_MaxDD", "mean"),
                  OOS_rank=("OOS_rank", "mean"), pass4a=("f4a", lambda s: (s == "-").sum()),
                  pass4b=("f4b", lambda s: (s == "-").sum())).reset_index())
    P(agg.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    inc = WF[WF.selector.str.startswith("IS-Sharpe")].set_index("k").draw
    rawsd = WF[WF.selector.str.startswith("RAW-sd")].set_index("k").draw
    P("\n    SELECTOR DEGENERACY - does the fitted control pick anything the record did not already have?")
    for sel, ref, refname in (("CTRL-fit", inc, "the IS-Sharpe incumbent"),
                              ("SD-resid", rawsd, "raw sd")):
        for sch in ["IS"] + [f"OOF{K}" for K in FOLDS]:
            s = WF[(WF.selector == sel) & (WF.scheme == sch)]
            same = sum(int(r.draw) == int(ref[r.k]) for _, r in s.iterrows())
            P(f"      {sel:9s} {sch:6s}: same pick as {refname:22s} on {same}/{len(s)} cells   "
              f"mean OOS Sharpe {s.OOS_Sharpe.mean():.4f}  mean OOS rank {s.OOS_rank.mean():.1f}/50")
    P(f"\n    4a passes (vs live RULES v2): {(WF.f4a == '-').sum()}/{len(WF)}     "
      f"4b passes (vs SPY): {(WF.f4b == '-').sum()}/{len(WF)}     "
      f"both: {((WF.f4a == '-') & (WF.f4b == '-')).sum()}/{len(WF)}")
    P(f"    binding 4b bars: " + "  ".join(f"{k}:{v}" for k, v in
      pd.Series([t for s in WF.f4b for t in s.split(",") if t != "-"]).value_counts().items()))

    P("\n" + "=" * 210)
    P(f"elapsed {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()

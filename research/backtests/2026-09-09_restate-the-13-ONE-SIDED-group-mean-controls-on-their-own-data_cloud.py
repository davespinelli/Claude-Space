#!/usr/bin/env python3
"""Idea 511 - RESTATE THE ONE-SIDED GROUP-MEAN CONTROLS ON THEIR OWN DATA (cloud, 2026-09-09).

Idea 483's lane-C runtime census (302,043 instrumented fit calls) found that, outside idea
252's own ridge, the record's only ONE-SIDED over-the-bar controls are
`groupby(...).transform("mean")` demeanings of a SINGLE column, p 12-91, p/N <= 0.167, in
exactly three scripts:

    2026-09-08_census-every-CROSSING-in-the-record-for-dial-heterogeneity_C.py : 148
    2026-09-08_the-mid-tercile-band_cloud.py                                   : 340
    2026-09-08_why-the-035-045-share-window-dips_cloud.py                      : 295

The queue's point: a cell mean that includes the row it is subtracted from is an in-sample
fit, and its leave-one-out restatement is an EXACT per-cell rescaling,

    x_i - mean_{-i}(cell) = m/(m-1) * (x_i - mean(cell)),

bounded but NOT measured, because idea 483's instrument logged (N, p) and not the cell-size
vector m.  This run logs the cell-size vector and restates the published statistics.

Design
------
STAGE 0 (--sweep): each of the three scripts is re-executed under an instrumented pandas
    that (a) logs the full cell-size vector at every transform("mean") call, and (b) at the
    THREE TARGET SITES ONLY substitutes an out-of-fold cell mean, inside a write sandbox
    that mirrors every write under the repo into scratch.  5 fold forms x 3 scripts.
STAGE 1 GATE: the PUBLISHED arm's mirrored artefacts are diffed against the committed ones
    (the harness must reproduce the record before it is allowed to move it).
STAGE 2 CELL SIZES: the logged m vectors -> the exact rescale factor m/(m-1) per row, its
    distribution per site, and the algebraic bound on the demeaned column.
STAGE 3 RESTATEMENT: every numeric cell of every artefact each script writes, PUBLISHED vs
    each out-of-fold form, plus the console numeric-token diff and any verdict-line change.
STAGE 4 RULE 8 + 4a/4b: the same demeaning used as a SELECTOR on idea 78/83's committed 300
    B136 books - parameters (fold form, cell key) chosen on 2009-2016 only, 2017-2026
    untouched - scored against the live RULES v2 (4a) and SPY (4b).

Two tuned parameters, every grid point reported: FOLD FORM in {PUBLISHED, K2, K5, K10, LOO}
and SCRIPT in the three above (STAGE 4 swaps SCRIPT for the CELL KEY, which is what a
selector has instead of a script).  Nothing else is tuned: panel, seeds, draws, k, n, cost
rung and IS/OOS split are idea 78/83's, imported unchanged.

RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are untouched, and no committed
artefact is written: the swept scripts run inside the write sandbox.

Usage:  python 2026-09-09_restate-the-13-ONE-SIDED-group-mean-controls-on-their-own-data_cloud.py [--sweep]
"""
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
from baseline import load_universe, rules_v1_weights, rules_v2_weights   # noqa: E402
from engine import backtest, metrics                                     # noqa: E402

pd.set_option("display.width", 240)

SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"
WORK = Path(os.environ.get("IDEA511_WORK", "/tmp/idea511"))

COST_BPS, FREQ = 10, "W"
KS, N_BOOK = [20, 40, 80], 20
OOS_START = "2017-01-01"
SEED_B = 78_500
REF_DRAWS = OUT / "2026-09-06_dispersion-as-a-survivorship-detector_B.draws.csv"
REF_GRIDB = OUT / "2026-09-05_candidate-count-vs-dispersion_B.gridB.csv"
RUNTIME_CSV = OUT / f"{STEM}.cellsizes.csv"

TARGETS = [
    ("2026-09-08_census-every-CROSSING-in-the-record-for-dial-heterogeneity_C.py", 148),
    ("2026-09-08_the-mid-tercile-band_cloud.py", 340),
    ("2026-09-08_why-the-035-045-share-window-dips_cloud.py", 295),
]
FORMS = ["PUBLISHED", "K2", "K5", "K10", "LOO"]

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


# =========================================================================================
# STAGE 0 - instrumented pandas + write sandbox
# =========================================================================================
SITECUSTOMIZE = r'''
"""Log every groupby-mean cell-size vector; substitute an out-of-fold cell mean at the
target sites; sandbox every write.  Written by idea 511."""
import os, sys, json, atexit, traceback, io, builtins
ROOT = os.environ["FITROOT"]; MIRROR = os.environ["FITMIRROR"]; LOG = os.environ["FITLOG"]
FORM = os.environ["FITFORM"]
TARGETS = {(f, int(l)) for f, l in json.loads(os.environ["FITTARGETS"])}
RECS = []
_GUARD = [False]

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

import numpy as np
import pandas as pd
_tc, _stc = pd.DataFrame.to_csv, pd.Series.to_csv
def dtc(self, path_or_buf=None, *a, **kw):
    if isinstance(path_or_buf, (str, os.PathLike)): path_or_buf = _redirect(path_or_buf)
    return _tc(self, path_or_buf, *a, **kw)
def stc(self, path_or_buf=None, *a, **kw):
    if isinstance(path_or_buf, (str, os.PathLike)): path_or_buf = _redirect(path_or_buf)
    return _stc(self, path_or_buf, *a, **kw)
pd.DataFrame.to_csv, pd.Series.to_csv = dtc, stc

from pandas.core.groupby.generic import SeriesGroupBy as _SGB, DataFrameGroupBy as _DGB
_ts, _td = _SGB.transform, _DGB.transform


def _oof_mean(x, codes, base, form):
    """Cell mean computed WITHOUT the row's own fold.  LOO = each row its own fold.
    Returns (values, cellsize_vector, n_substituted) or (None, sizes, 0) if undefined."""
    n = len(x)
    valid = np.isfinite(x) & (codes >= 0)
    ng = int(codes.max()) + 1 if len(codes) and codes.max() >= 0 else 0
    if ng == 0: return None, np.array([]), 0
    c = np.where(valid, codes, 0)
    w = valid.astype(float)
    m = np.bincount(c, weights=w, minlength=ng)
    S = np.bincount(c, weights=np.where(valid, x, 0.0), minlength=ng)
    sizes = m.copy()
    if form == "LOO":
        denom = m[c] - 1.0
        num = S[c] - np.where(valid, x, 0.0)
    else:
        K = int(form[1:])
        # deterministic within-cell fold id: position of the row inside its own cell mod K
        order = np.argsort(c, kind="stable")
        cnt = np.bincount(c, minlength=ng).astype(int)
        starts = np.concatenate([[0], np.cumsum(cnt)[:-1]])
        rank = np.empty(n, dtype=np.int64)
        rank[order] = np.arange(n) - np.repeat(starts, cnt)
        fold = rank % K
        key = c * K + fold
        mf = np.bincount(key, weights=w, minlength=ng * K)
        Sf = np.bincount(key, weights=np.where(valid, x, 0.0), minlength=ng * K)
        denom = m[c] - mf[key]
        num = S[c] - Sf[key]
    ok = valid & (denom > 0)
    out = np.where(ok, num / np.where(denom > 0, denom, 1.0), base)
    return out, sizes, int(ok.sum())


def _handle(self, label):
    """Log the cell-size vector; return substituted means at a target site, else None."""
    f, ln = _site()
    try:
        base = _ts(self, "mean") if label == "s" else _td(self, "mean")
    except Exception:
        return None
    rec = dict(file=f, line=ln, form=FORM, label=label, N=int(len(self.obj)),
               ngroups=int(self.ngroups), target=int((f, ln) in TARGETS))
    sizes = None
    sub = None
    try:
        codes = np.asarray(self.ngroup().values, dtype=np.int64)
        if label == "s":
            x = np.asarray(self.obj.values, dtype=float)
            b = np.asarray(base.values, dtype=float)
            vals, sizes, nsub = _oof_mean(x, codes, b, "LOO" if FORM == "PUBLISHED" else FORM)
            if (f, ln) in TARGETS and FORM != "PUBLISHED" and vals is not None:
                sub = pd.Series(vals, index=self.obj.index, name=self.obj.name)
                rec["substituted"] = nsub
        else:
            ng = int(codes.max()) + 1 if len(codes) and codes.max() >= 0 else 0
            sizes = np.bincount(np.where(codes >= 0, codes, 0), minlength=max(ng, 1)).astype(float)
    except Exception as e:
        rec["err"] = type(e).__name__
    if sizes is not None and len(sizes):
        s = sizes[sizes > 0]
        big = s[s > 1]                       # m == 1 leaves the demeaned value at 0 either way
        rec.update(m_min=float(s.min()), m_med=float(np.median(s)), m_max=float(s.max()),
                   m_mean=float(s.mean()), n_size1=int((s == 1).sum()),
                   fac_max=float((big / (big - 1)).max()) if len(big) else float("nan"),
                   fac_wmean=float(((big / (big - 1)) * big).sum() / big.sum())
                   if len(big) else float("nan"))
        if rec["target"]:
            v, c2 = np.unique(s.astype(int), return_counts=True)
            rec["sizevec"] = json.dumps({int(a): int(b) for a, b in zip(v, c2)})
    RECS.append(rec)
    return sub


def _wrap(cls, label, orig):
    def transform(self, func, *a, **kw):
        nm = func if isinstance(func, str) else getattr(func, "__name__", "")
        if nm != "mean" or _GUARD[0] or a or kw:
            return orig(self, func, *a, **kw)
        _GUARD[0] = True
        try:
            sub = _handle(self, label)
        except Exception:
            sub = None
        finally:
            _GUARD[0] = False
        if sub is not None:
            return sub
        return orig(self, func, *a, **kw)
    cls.transform = transform


_wrap(_SGB, "s", _ts)
_wrap(_DGB, "d", _td)

@atexit.register
def _dump():
    with _open(LOG, "w") as fh: json.dump(RECS, fh)
'''


def sweep(timeout=2400, jobs=5):
    """Re-execute the three target scripts under all five fold forms, sandboxed."""
    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / "inst").mkdir(exist_ok=True)
    (WORK / "inst" / "sitecustomize.py").write_text(SITECUSTOMIZE)
    jobsq = [(fn, form) for fn, _ in TARGETS for form in FORMS]
    P(f"    sweep: {len(jobsq)} runs = {len(TARGETS)} scripts x {len(FORMS)} fold forms, "
      f"{jobs} at a time, timeout {timeout}s each")
    status, running = [], []

    def launch(fn, form):
        tag = f"{fn[:-3]}__{form}"
        mirror = WORK / "mirror" / tag
        mirror.mkdir(parents=True, exist_ok=True)
        (WORK / "logs").mkdir(exist_ok=True)
        env = dict(os.environ, FITROOT=str(REPO), FITMIRROR=str(mirror),
                   FITLOG=str(WORK / "logs" / f"{tag}.json"), FITFORM=form,
                   FITTARGETS=json.dumps([[f, l] for f, l in TARGETS]),
                   PYTHONPATH=str(WORK / "inst"))
        out = (WORK / "logs" / f"{tag}.out").open("w")
        pr = subprocess.Popen([sys.executable, str(OUT / fn)], cwd=str(REPO), env=env,
                              stdout=out, stderr=subprocess.STDOUT)
        return (fn, form, tag, pr, out, time.time())

    q = list(jobsq)
    while q or running:
        while q and len(running) < jobs:
            running.append(launch(*q.pop(0)))
        time.sleep(3)
        for item in list(running):
            fn, form, tag, pr, fh, t0 = item
            if pr.poll() is None:
                if time.time() - t0 > timeout:
                    pr.kill(); pr.wait()
                else:
                    continue
            fh.close(); running.remove(item)
            secs = round(time.time() - t0, 1)
            status.append(dict(script=fn, form=form, tag=tag, rc=pr.returncode, secs=secs))
            P(f"      {tag:<88s} rc={pr.returncode} {secs:7.1f}s")
    recs = []
    for st in status:
        j = WORK / "logs" / f"{st['tag']}.json"
        st["logged"] = j.exists()
        if j.exists():
            for r in json.loads(j.read_text()):
                r["script"], r["tag"] = st["script"], st["tag"]
                recs.append(r)
    ST = pd.DataFrame(status)
    ST.to_csv(OUT / f"{STEM}.sweepstatus.csv", index=False)
    RT = pd.DataFrame(recs)
    RT.to_csv(RUNTIME_CSV, index=False)
    P(f"    sweep done: rc==0 on {int((ST.rc == 0).sum())}/{len(ST)} runs, "
      f"{len(RT)} logged groupby-mean calls -> {RUNTIME_CSV.name}")
    return ST, RT


# =========================================================================================
# artefact diffing
# =========================================================================================
def _numeric_frame(path):
    """Every numeric column of a CSV, positionally indexed."""
    try:
        df = pd.read_csv(path)
    except Exception:
        return None
    out = {}
    for c in df.columns:
        v = pd.to_numeric(df[c], errors="coerce")
        if v.notna().sum():
            out[c] = v.to_numpy(float)
    return out


def _diff_cells(a, b):
    """(#shared, #moved>1e-9, max abs, max rel, median abs over moved) over numeric columns."""
    if a is None or b is None:
        return dict(shared=0, moved=-1, max_abs=np.nan, max_rel=np.nan, med_abs_moved=np.nan)
    shared = mov = 0
    mx = mr = 0.0
    md = []
    for c in set(a) & set(b):
        x, y = a[c], b[c]
        n = min(len(x), len(y))
        x, y = x[:n], y[:n]
        ok = np.isfinite(x) & np.isfinite(y)
        if not ok.any():
            continue
        d = np.abs(x[ok] - y[ok])
        sc = np.maximum(np.maximum(np.abs(x[ok]), np.abs(y[ok])), 1e-12)
        shared += int(ok.sum())
        m = d > 1e-9
        mov += int(m.sum())
        if m.any():
            mx = max(mx, float(d.max()))
            mr = max(mr, float((d / sc).max()))
            md.append(float(np.median(d[m])))
    if shared == 0:
        return dict(shared=0, moved=-1, max_abs=np.nan, max_rel=np.nan, med_abs_moved=np.nan)
    return dict(shared=shared, moved=mov, max_abs=mx, max_rel=mr,
                med_abs_moved=float(np.median(md)) if md else 0.0)


NUMTOK = re.compile(r"-?\d+\.\d+|-?\d+")


def _console_tokens(path):
    try:
        return NUMTOK.findall(Path(path).read_text())
    except Exception:
        return []


def _mirror_arts(tag, script):
    d = WORK / "mirror" / tag / "research" / "backtests"
    if not d.exists():
        return {}
    return {f.name: f for f in sorted(d.glob(script[:-3] + ".*"))}


# =========================================================================================
# STAGE 4 helpers
# =========================================================================================
def demean(x, cell, form):
    """Within-cell demeaning under a fold form.  PUBLISHED includes the row's own value."""
    codes = pd.factorize(cell)[0]
    ng = codes.max() + 1
    m = np.bincount(codes, minlength=ng).astype(float)
    S = np.bincount(codes, weights=x, minlength=ng)
    mu = S[codes] / m[codes]
    if form == "PUBLISHED":
        return x - mu
    if form == "LOO":
        denom, num = m[codes] - 1.0, S[codes] - x
    else:
        K = int(form[1:])
        order = np.argsort(codes, kind="stable")
        cnt = np.bincount(codes, minlength=ng)
        starts = np.concatenate([[0], np.cumsum(cnt)[:-1]])
        rank = np.empty(len(x), dtype=np.int64)
        rank[order] = np.arange(len(x)) - np.repeat(starts, cnt)
        key = codes * K + (rank % K)
        mf = np.bincount(key, minlength=ng * K).astype(float)
        Sf = np.bincount(key, weights=x, minlength=ng * K)
        denom, num = m[codes] - mf[key], S[codes] - Sf[key]
    good = denom > 0
    return x - np.where(good, num / np.where(good, denom, 1.0), mu)


def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


# =========================================================================================
def main():
    t0 = time.time()
    P("=" * 210)
    P("IDEA 511 - RESTATE THE ONE-SIDED GROUP-MEAN CONTROLS ON THEIR OWN DATA (cloud, 2026-09-09)")
    P("=" * 210)
    P("Question: idea 483 found the record's only ONE-SIDED over-bar controls outside idea 252's")
    P("ridge are 13 groupby-mean demeanings of a single column in 3 scripts, whose leave-one-out")
    P("restatement is an exact per-cell rescale by m/(m-1) - bounded but never measured, because")
    P("the instrument logged (N, p) and not the cell-size vector m.  This run measures m and")
    P("restates every statistic those three scripts publish.")
    P(f"Two tuned parameters: FOLD FORM in {FORMS} x SCRIPT in the 3 target files (STAGE 4 swaps")
    P("SCRIPT for the CELL KEY).  Costs 10 bps, weekly, next-day execution: idea 78/83's, unchanged.")

    if "--sweep" in sys.argv or not RUNTIME_CSV.exists():
        P("\n[0] SWEEP - the three scripts re-executed under instrumented pandas, inside a write sandbox")
        ST, RT = sweep()
    else:
        P("\n[0] SWEEP - reading the committed cell-size log (pass --sweep to re-execute)")
        ST = pd.read_csv(OUT / f"{STEM}.sweepstatus.csv")
        RT = pd.read_csv(RUNTIME_CSV)
    P(ST[["script", "form", "rc", "secs", "logged"]].to_string(index=False, max_colwidth=76))
    if int((ST.rc == 0).sum()) < len(ST):
        P("    NOTE: a non-zero rc means the script aborted; its arm is reported as UNRESOLVED below.")

    # ------------------------------------------------------------------ STAGE 1 - reproduction gate
    P("\n[1] GATE - the PUBLISHED arm must reproduce the committed artefacts before it may move them")
    gate = []
    for fn, _ in TARGETS:
        tag = f"{fn[:-3]}__PUBLISHED"
        arts = _mirror_arts(tag, fn)
        for name, path in arts.items():
            if not name.endswith(".csv"):
                continue
            comm = OUT / name
            if not comm.exists():
                gate.append(dict(script=fn, artefact=name, status="NOT-COMMITTED", **_diff_cells(None, None)))
                continue
            d = _diff_cells(_numeric_frame(comm), _numeric_frame(path))
            gate.append(dict(script=fn, artefact=name,
                             status="REPRODUCED" if d["moved"] == 0 else "MOVED", **d))
    GT = pd.DataFrame(gate)
    if len(GT):
        GT.to_csv(OUT / f"{STEM}.gate.csv", index=False)
        P(GT.to_string(index=False, max_colwidth=76, float_format=lambda x: f"{x:.3e}"))
        P(f"    {int((GT.status == 'REPRODUCED').sum())}/{len(GT)} committed CSV artefacts reproduced "
          f"cell-for-cell by the instrumented PUBLISHED arm.")
    else:
        P("    no artefacts mirrored - the sweep produced nothing to gate.")

    # ------------------------------------------------------------------ STAGE 2 - the cell sizes
    P("\n[2] CELL SIZES - what idea 483's instrument did not log")
    tg = RT[(RT.target == 1) & (RT.form == "PUBLISHED")].copy()
    if len(tg):
        agg = (tg.groupby(["script", "line"])
                 .agg(calls=("N", "size"), N_min=("N", "min"), N_max=("N", "max"),
                      p_min=("ngroups", "min"), p_max=("ngroups", "max"),
                      m_min=("m_min", "min"), m_med=("m_med", "median"), m_max=("m_max", "max"),
                      size1_cells=("n_size1", "max"), fac_max=("fac_max", "max"),
                      fac_wmean=("fac_wmean", "mean")).reset_index())
        agg.to_csv(OUT / f"{STEM}.sites.csv", index=False)
        P("    Per target site: m is the cell size, and the LOO restatement multiplies the demeaned")
        P("    column by m/(m-1) row by row.  fac_max is the largest such factor, fac_wmean the")
        P("    row-weighted mean factor - the whole size of the one-sided exposure.")
        P(agg.to_string(index=False, max_colwidth=72, float_format=lambda x: f"{x:.4f}"))
        allsizes = []
        for _, r in tg.iterrows():
            if isinstance(r.get("sizevec"), str):
                for k, v in json.loads(r["sizevec"]).items():
                    allsizes += [int(k)] * int(v)
        if allsizes:
            a = np.array(allsizes, dtype=float)
            big = a[a > 1]                       # m == 1: LOO undefined, demeaned value 0 either way
            f = big / (big - 1)
            P(f"    pooled over {len(a)} cells at the target sites: m median {np.median(a):.0f}, "
              f"q10 {np.quantile(a, .1):.0f}, min {a.min():.0f}, max {a.max():.0f}; "
              f"factor m/(m-1) over the {len(big)} cells with m>1: median {np.median(f):.4f}, "
              f"q90 {np.quantile(f, .9):.4f}, max {f.max():.4f}")
            P(f"    cells of size 1 (where LOO is undefined and the demeaned value is 0 either way): "
              f"{int((a == 1).sum())}/{len(a)}")
    else:
        P("    no target-site calls logged.")

    P("\n    Non-target groupby-mean calls in the same three scripts (logged, never substituted):")
    nt = RT[(RT.target == 0) & (RT.form == "PUBLISHED")]
    if len(nt):
        P(nt.groupby(["script", "line"]).agg(calls=("N", "size"), N=("N", "max"),
                                             p=("ngroups", "max"), m_min=("m_min", "min"),
                                             m_med=("m_med", "median")).to_string(max_colwidth=72))
    else:
        P("      none")

    # ------------------------------------------------------------------ STAGE 3 - the restatement
    P("\n[3] RESTATEMENT - every numeric cell each script publishes, PUBLISHED vs each out-of-fold form")
    rows = []
    for fn, _ in TARGETS:
        base_tag = f"{fn[:-3]}__PUBLISHED"
        base_arts = _mirror_arts(base_tag, fn)
        base_num = {n: _numeric_frame(p) for n, p in base_arts.items() if n.endswith(".csv")}
        base_con = [n for n in base_arts if n.endswith("console.txt")]
        base_tok = _console_tokens(base_arts[base_con[0]]) if base_con else []
        for form in FORMS:
            if form == "PUBLISHED":
                continue
            tag = f"{fn[:-3]}__{form}"
            rc = ST[(ST.script == fn) & (ST.form == form)]
            arts = _mirror_arts(tag, fn)
            if not len(rc) or int(rc.rc.iloc[0]) != 0 or not arts:
                rows.append(dict(script=fn, form=form, artefacts=0, cells=0, moved=-1,
                                 share_moved=np.nan, max_rel=np.nan, tok=0, tok_moved=-1,
                                 status="UNRESOLVED"))
                continue
            tot = mov = 0
            mx = 0.0
            for n, bn in base_num.items():
                if n not in arts:
                    continue
                d = _diff_cells(bn, _numeric_frame(arts[n]))
                if d["moved"] < 0:
                    continue
                tot += d["shared"]; mov += d["moved"]
                mx = max(mx, 0.0 if not np.isfinite(d["max_rel"]) else d["max_rel"])
            con = [n for n in arts if n.endswith("console.txt")]
            tk = _console_tokens(arts[con[0]]) if con else []
            tmv = -1
            if base_tok and len(tk) == len(base_tok):
                tmv = int(sum(a != b for a, b in zip(base_tok, tk)))
            rows.append(dict(script=fn, form=form, artefacts=len(base_num), cells=tot, moved=mov,
                             share_moved=mov / tot if tot else np.nan, max_rel=mx,
                             tok=len(tk), tok_moved=tmv,
                             status="OK" if tot else "NO-SHARED-CELLS"))
    RS = pd.DataFrame(rows)
    RS.to_csv(OUT / f"{STEM}.restated.csv", index=False)
    P("    cells = numeric artefact cells shared with the PUBLISHED arm; moved = those differing by")
    P("    more than 1e-9; max_rel = largest relative move; tok_moved = console numeric tokens that")
    P("    changed (only comparable when the two consoles have the same token count).")
    P(RS.to_string(index=False, max_colwidth=72, float_format=lambda x: f"{x:.4f}"))
    ok = RS[RS.status == "OK"]
    if len(ok):
        P(f"\n    ALL {len(RS)} grid points = {len(TARGETS)} scripts x {len(FORMS) - 1} out-of-fold forms, "
          f"committed to {STEM}.restated.csv")
        P(f"    Pooled: {int(ok.moved.sum())}/{int(ok.cells.sum())} published numeric cells move "
          f"({ok.moved.sum() / max(ok.cells.sum(), 1):.3%}); largest relative move {ok.max_rel.max():.3e}")
        for fn, _ in TARGETS:
            s = ok[ok.script == fn]
            if len(s):
                P(f"      {fn[:-3]:<74s} moved {int(s.moved.sum())}/{int(s.cells.sum())}  "
                  f"max rel {s.max_rel.max():.3e}  console tokens moved "
                  f"{'/'.join(str(int(v)) for v in s.tok_moved)}")

    # per-artefact detail for the worst form
    det = []
    for fn, _ in TARGETS:
        base_arts = _mirror_arts(f"{fn[:-3]}__PUBLISHED", fn)
        for form in FORMS[1:]:
            arts = _mirror_arts(f"{fn[:-3]}__{form}", fn)
            for n, p in base_arts.items():
                if not n.endswith(".csv") or n not in arts:
                    continue
                d = _diff_cells(_numeric_frame(p), _numeric_frame(arts[n]))
                det.append(dict(script=fn, form=form, artefact=n, **d))
    if det:
        DT = pd.DataFrame(det)
        DT.to_csv(OUT / f"{STEM}.artefactdiff.csv", index=False)
        P(f"\n    per-artefact detail ({len(DT)} rows) -> {STEM}.artefactdiff.csv; worst 8 by max_rel:")
        P(DT.nlargest(8, "max_rel")[["form", "artefact", "shared", "moved", "max_abs", "max_rel"]]
          .to_string(index=False, max_colwidth=64, float_format=lambda x: f"{x:.4e}"))

    # ------------------------------------------------------------------ STAGE 3b - the readings
    P("\n[3b] WHICH PUBLISHED READINGS MOVE - console line diff, PUBLISHED vs each form")
    VERD = re.compile(r"\b(YES|NO|KEEP|KILL|PARK|CONFIRMED|REFUTED|TRUE|FALSE)\b")
    rd = []
    for fn, _ in TARGETS:
        ba = _mirror_arts(f"{fn[:-3]}__PUBLISHED", fn)
        bc = [n for n in ba if n.endswith("console.txt")]
        if not bc:
            continue
        base = Path(ba[bc[0]]).read_text().split("\n")
        for form in FORMS[1:]:
            arts = _mirror_arts(f"{fn[:-3]}__{form}", fn)
            cc = [n for n in arts if n.endswith("console.txt")]
            if not cc:
                continue
            cur = Path(arts[cc[0]]).read_text().split("\n")
            n = min(len(base), len(cur))
            chg = [i for i in range(n) if base[i] != cur[i]]
            vf = sum(1 for i in chg if VERD.findall(base[i]) != VERD.findall(cur[i]))
            rd.append(dict(script=fn, form=form, lines=len(base), changed=len(chg),
                           len_equal=int(len(base) == len(cur)), verdict_lines=vf))
    RD = pd.DataFrame(rd)
    if len(RD):
        RD.to_csv(OUT / f"{STEM}.consolediff.csv", index=False)
        P(RD.to_string(index=False, max_colwidth=76))
        P("    verdict_lines counts console lines whose YES/NO/KEEP/KILL/PARK tokens CHANGE - a")
        P("    published reading that reverses, not just a digit that moves.")
        worst = RD.loc[RD.changed.idxmax()]
        ba = _mirror_arts(f"{worst.script[:-3]}__PUBLISHED", worst.script)
        aa = _mirror_arts(f"{worst.script[:-3]}__{worst.form}", worst.script)
        bl = Path(ba[[n for n in ba if n.endswith('console.txt')][0]]).read_text().split("\n")
        al = Path(aa[[n for n in aa if n.endswith('console.txt')][0]]).read_text().split("\n")
        P(f"\n    worst grid point: {worst.script[:-3]} under {worst.form} - "
          f"{worst.changed} of {worst.lines} console lines change.  First 10 pairs:")
        shown = 0
        for i in range(min(len(bl), len(al))):
            if bl[i] != al[i]:
                P(f"      PUBLISHED | {bl[i][:150]}")
                P(f"      {worst.form:<9s} | {al[i][:150]}")
                shown += 1
                if shown >= 10:
                    break

    # ------------------------------------------------------------------ STAGE 4 - rule 8 + 4a/4b
    P("\n[4] RULE 8 - the same demeaning as a SELECTOR, parameters chosen on 2009-2016, 2017-2026 untouched")
    if not (REF_DRAWS.exists() and REF_GRIDB.exists()):
        P("    ABORT: idea 78/83's committed CSVs are missing.")
    else:
        B = pd.read_csv(REF_DRAWS)
        G = pd.read_csv(REF_GRIDB)
        num = [c for c in G.columns if pd.api.types.is_numeric_dtype(G[c]) and c in B.columns]
        dg = max(float(np.abs(G[c].values - B[c].values).max()) for c in num)
        P(f"    [gate] gridB.csv vs draws.csv over {len(num)} shared numeric columns: max abs diff {dg:.3e}")
        px136 = load_universe(broad=True)
        startb = px136.index[260]
        spy = px136["SPY"].pct_change().fillna(0).loc[startb:]
        v2 = backtest(px136, rules_v2_weights(px136), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[startb:]
        v1 = backtest(px136, rules_v1_weights(px136), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[startb:]
        ms, mv2, mv1 = metrics(spy), metrics(v2), metrics(v1)
        sh1, sh2 = half_sharpes(spy)
        b1, b2 = half_sharpes(v2)
        spy_oos = metrics(spy.loc[OOS_START:])
        v2_oos = metrics(v2.loc[OOS_START:])
        P(f"    SPY       {ms['CAGR']:.2%} / {ms['Sharpe']:.3f} / {ms['MaxDD']:.2%}  halves "
          f"{sh1:.3f}/{sh2:.3f}  OOS {spy_oos['CAGR']:.2%} / {spy_oos['Sharpe']:.3f} / {spy_oos['MaxDD']:.2%}")
        P(f"    RULES v2  {mv2['CAGR']:.2%} / {mv2['Sharpe']:.3f} / {mv2['MaxDD']:.2%}  halves "
          f"{b1:.3f}/{b2:.3f}  OOS {v2_oos['CAGR']:.2%} / {v2_oos['Sharpe']:.3f} / {v2_oos['MaxDD']:.2%}")
        P(f"    RULES v1  {mv1['CAGR']:.2%} / {mv1['Sharpe']:.3f} / {mv1['MaxDD']:.2%}  (continuity row)")

        def fails(r):
            f4a = [t for t, c in (("H1", r.H1 > b1), ("H2", r.H2 > b2),
                                  ("DD", r.MaxDD >= mv2["MaxDD"])) if not c]
            f4b = [t for t, c in (("H1", r.H1 > sh1), ("H2", r.H2 > sh2),
                                  ("OOS", r.Sharpe_OOS > spy_oos["Sharpe"]),
                                  ("DD", r.MaxDD >= 0.60 * ms["MaxDD"]),
                                  ("CAGR", r.CAGR >= 0.70 * ms["CAGR"])) if not c]
            return (",".join(f4a) or "-"), (",".join(f4b) or "-")

        pool = B[B.n == N_BOOK].reset_index(drop=True).copy()
        pool["sd_ter"] = pd.qcut(pool.sd_IS, 3, labels=False, duplicates="drop")
        CELLKEYS = {
            "k": pool.k.astype(str),
            "k x sd_IS tercile": pool.k.astype(str) + "|" + pool.sd_ter.astype(str),
            "sd_IS tercile": pool.sd_ter.astype(str),
        }
        P("\n    The selector reads ONLY the IS window (Sharpe_IS); the OOS columns are idea 78's")
        P("    committed 2017-2026 numbers and are touched only to score the pick.  A pooled argmax")
        P("    over a within-cell demeaned column is exactly where the m/(m-1) rescale can move a")
        P("    choice: cells of different size are rescaled by different factors.")
        wf = []
        x = pool.Sharpe_IS.values.astype(float)
        for cname, ck in CELLKEYS.items():
            sizes = ck.value_counts()
            for form in FORMS:
                d = demean(x, ck.values, form)
                i = int(np.argmax(d))
                r = pool.iloc[i]
                f4a, f4b = fails(r)
                wf.append(dict(cell_key=cname, n_cells=len(sizes), m_min=int(sizes.min()),
                               m_max=int(sizes.max()), form=form, k=int(r.k), draw=int(r.draw),
                               IS_Sharpe=r.Sharpe_IS, OOS_Sharpe=r.Sharpe_OOS, OOS_CAGR=r.CAGR_OOS,
                               OOS_MaxDD=r.MaxDD_OOS, full_Sharpe=r.Sharpe, full_CAGR=r.CAGR,
                               full_MaxDD=r.MaxDD, H1=r.H1, H2=r.H2,
                               OOS_rank=int((pool.Sharpe_OOS > r.Sharpe_OOS).sum()) + 1,
                               f4a=f4a, f4b=f4b))
        i = int(np.argmax(x))
        r = pool.iloc[i]
        f4a, f4b = fails(r)
        wf.append(dict(cell_key="none (incumbent)", n_cells=1, m_min=len(pool), m_max=len(pool),
                       form="RAW IS-Sharpe argmax", k=int(r.k), draw=int(r.draw),
                       IS_Sharpe=r.Sharpe_IS, OOS_Sharpe=r.Sharpe_OOS, OOS_CAGR=r.CAGR_OOS,
                       OOS_MaxDD=r.MaxDD_OOS, full_Sharpe=r.Sharpe, full_CAGR=r.CAGR,
                       full_MaxDD=r.MaxDD, H1=r.H1, H2=r.H2,
                       OOS_rank=int((pool.Sharpe_OOS > r.Sharpe_OOS).sum()) + 1, f4a=f4a, f4b=f4b))
        rng = np.random.default_rng(SEED_B)
        rnd = pool.iloc[rng.integers(0, len(pool), 200)]
        P(f"    reference: mean OOS Sharpe of a RANDOM draw from the same pool {rnd.Sharpe_OOS.mean():.4f} "
          f"(pool mean {pool.Sharpe_OOS.mean():.4f}, best {pool.Sharpe_OOS.max():.4f})")
        WF = pd.DataFrame(wf)
        WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
        P(f"    {len(WF)} walk-forward rows = {len(CELLKEYS)} cell keys x {len(FORMS)} fold forms "
          f"+ 1 incumbent -> {STEM}.walkforward.csv")
        P(WF[["cell_key", "n_cells", "m_min", "m_max", "form", "k", "draw", "IS_Sharpe",
              "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "OOS_rank", "f4a", "f4b"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        sel = WF[WF.form.isin(FORMS)]
        pub = sel[sel.form == "PUBLISHED"].set_index("cell_key").draw
        P("\n    DOES THE FOLD FORM MOVE THE CHOICE?")
        for form in FORMS[1:]:
            s = sel[sel.form == form]
            same = sum(int(r.draw) == int(pub[r.cell_key]) for _, r in s.iterrows())
            P(f"      {form:<10s} same pick as PUBLISHED on {same}/{len(s)} cell keys   "
              f"mean OOS Sharpe {s.OOS_Sharpe.mean():.4f}  mean OOS rank {s.OOS_rank.mean():.1f}/{len(pool)}")
        P(f"      PUBLISHED  mean OOS Sharpe {sel[sel.form == 'PUBLISHED'].OOS_Sharpe.mean():.4f}  "
          f"mean OOS rank {sel[sel.form == 'PUBLISHED'].OOS_rank.mean():.1f}/{len(pool)}")
        KP = WF[["cell_key", "form", "f4a", "f4b"]].copy()
        KP["pass4a"] = (KP.f4a == "-").astype(int)
        KP["pass4b"] = (KP.f4b == "-").astype(int)
        KP.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
        P(f"\n    KEEP PATHS over the {len(WF)} rows: 4a {int(KP.pass4a.sum())}/{len(KP)}   "
          f"4b {int(KP.pass4b.sum())}/{len(KP)}   both {int((KP.pass4a & KP.pass4b).sum())}/{len(KP)}")
        bars = pd.Series([t for s in WF.f4b for t in s.split(",") if t != "-"]).value_counts()
        P("    binding 4b bars: " + "  ".join(f"{k}:{v}" for k, v in bars.items()))

    P("\n" + "=" * 210)
    P(f"elapsed {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()

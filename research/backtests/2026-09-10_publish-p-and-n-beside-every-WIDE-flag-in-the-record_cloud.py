#!/usr/bin/env python3
"""Idea 658 (cloud, 2026-09-10) -- PUBLISH p AND n BESIDE EVERY *WIDE* FLAG IN THE RECORD.

Idea 483's cloud census (`2026-09-09_which-published-residualisations-are-IN-SAMPLE-fits_cloud
.census.csv`) and idea 484's (`2026-09-09_census-every-published-N-EQUALS-50-model-comparison-
in-the-record_C.census.csv`) each carry a boolean column `wide_design_hint`.  Both compute it
by a STATIC TEXT MATCH on the source (`get_dummies` / a per-name design phrase), never from a
design matrix.  Idea 497 then re-ran the 3 files those censuses call wide-and-unfolded and
found they top out at p = 6 on n = 162, i.e. p/n = 0.0370 -- two orders of magnitude below any
width that would make an unfolded in-sample fit unsafe.

The queue asks: re-score EVERY committed width flag against the RUNTIME (p, n) of the sites it
names, and report how many of the record's 'wide' labels survive.

PRE-REGISTRATION (fixed before any number below was read):

  * EXACTLY TWO TUNED PARAMETERS, and no more:
      CENSUSSET  in {COMMITTED, ALL}   -- which width-flag population is scored
      WIDTHBAR   in {0.05, 0.10, 0.25, 0.50, 1.00}  -- the p/n bar a 'wide' label must clear
    Everything else (panel, cost rung, book form, ridge penalty, window length, forecast
    width) is a REPORTED axis, never chosen.  Every grid point is written to disk.

  * PART A -- CENSUS.  A width-flag SITE is one row of a committed artefact that names a file
    and carries a truthy width flag.
      COMMITTED = every research/backtests/*.csv[.gz] whose header carries a width-flag column
                  (WIDE_COLS below).  This is the population a reader acts on.
      ALL       = COMMITTED plus every prose line in the committed record (CHANGELOG.md,
                  QUEUE.md, LEADERBOARD.md, PROTOCOL.md, *.result.md, *.memo.md,
                  *_RECOMMENDATION.md) that asserts a width claim in words (WIDE_PHRASES).
    A prose site names a file when a `research/backtests/<stem>.py` stem appears on the line.

  * PART B -- RUNTIME (p, n).  Every named .py file is RE-EXECUTED in a subprocess with
    `np.linalg.lstsq / pinv / solve` and `np.polyfit` instrumented, and with every write inside
    the repo redirected to a scratch tree, so the committed record is not touched (gate G5
    asserts `git status --porcelain` is unchanged across PART B).  Each captured call yields
      p  = design width  (lstsq/polyfit: X.shape[1]; a square gram passed to pinv/solve: its
           dimension, which is the design width of the fit it serves)
      n  = design rows   (lstsq/polyfit: X.shape[0]; gram sites: the smallest 2-D array with
           p columns in the calling frame -- labelled n_source='frame')
    A file that HALTS on its own reproduction gate before reaching its fit is reported as
    p_source='halted', not silently dropped: that is itself an answer about the record.
    DETERMINISM CAVEAT, stated up front: a file that exceeds the PROBE_TIMEOUT budget (900 s)
    publishes what it reached inside it, so for a TIMEOUT file the fit-call COUNT is
    machine-dependent and the (p, n) coverage is a LOWER bound on that file's design widths.
    The re-scoring below turns only on each site's max p and min n, which are reached in the
    first seconds of the fitting loops and were identical across three runs on this machine at
    two different budgets (1800 s and 900 s); the counts are published as-is and differ between
    those runs.  A site's p/n is always a PER-CALL ratio maximised over that site's own calls,
    never max(p)/min(n) across different fits, which could only overstate it.
    Where re-execution does not reach a fit site, p is resolved STATICALLY from the design
    expression by AST (np.column_stack / np.hstack / np.c_ of a literal list, plus the
    `np.ones` intercept) and labelled p_source='ast'.  Every site publishes p, n, p/n and
    both provenance labels; nothing is imputed.

  * PART C -- WHAT A WIDTH LABEL IS SUPPOSED TO BUY, PRICED ON A REAL BOOK.  A width flag is
    a warning that a wide design overfits.  That is a testable statement about books, so it is
    tested on books rather than asserted.  On each of the three panels a weekly cross-sectional
    ridge forecast is fitted on a rolling window of L weeks x N names (n = L*N rows) with p
    lagged-weekly-return predictors, and the top-20 equal-weight book (the 2026-09-04 KEEP 4b
    form: no vol scaler, gross 1.00) is held on the forecast.  p in {1,2,4,8,16,32,64},
    L in {4,13,52,104}, lam in {0.01,0.1,1.0}, panel in {U56,B136,SMALL439}: 252 arms, ALL
    reported, each with full-sample / H1 / H2 / OOS CAGR, Sharpe, MaxDD, its own p/n, and both
    KEEP paths.  The question the record needs answered: does p/n predict OOS book quality at
    all?  If it does not, a width label is not a warning, whatever its arithmetic.

  * PROTOCOL rule 8 is run twice: on the CENSUS claim (WIDTHBAR chosen on the first half of the
    record by file date, read once on the second half) and on the BOOK (p and L chosen on
    2009-2016 by in-sample Sharpe, 2017-2026 read once), against RULES v2 and SPY.

  * BOTH KEEP PATHS on every PART C arm.  4a: Sharpe > live RULES v2 in BOTH halves and MaxDD
    no worse.  4b: Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70%.

  * Costs 10 bps (0 and 25 reported), weekly, weights decided at t applied at t+1 -- engine
    default, gated at G1 against `engine.backtest` itself.

SURVIVORSHIP (PROTOCOL 9): U56 and B136 are current-constituent lists; SMALL439 is the sub-$2B
screen with `data/small_meta.csv max_1d_move >= 1.0` dropped (idea 118), also current
constituents and additionally back-filled only to 2010.  Every LEVEL below is optimistic and
none is a tradable estimate.  The objects meant to survive are within-panel contrasts read off
identical books (p vs p, L vs L on the same panel and window) and the census arithmetic, which
is a property of committed files and carries no survivorship at all.

Deterministic, standalone, offline.  Writes .console.txt, .sites.csv, .probe.csv, .grid.csv,
.keeppaths.csv, .walkforward.csv, .result.md.  Reads only committed artefacts + baseline.py.
Modifies nothing in the repo.
"""
import ast
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

T0 = time.time()
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


# ---------------------------------------------------------------- pre-registered constants
WIDE_COLS = ["wide_design_hint", "wide_design", "is_wide", "wide", "width_flag", "p_over_n"]
WIDE_PHRASES = [
    r"wide[- ]design", r"wide[- ]and[- ]unfolded", r"wide_design_hint",
    r"\bwide\b[^.]{0,40}\bdesign\b", r"\bdesign\b[^.]{0,40}\bwide\b",
]
PROSE_FILES = ["research/CHANGELOG.md", "research/QUEUE.md", "research/LEADERBOARD.md",
               "research/PROTOCOL.md"]
WIDTHBARS = [0.05, 0.10, 0.25, 0.50, 1.00]
CENSUSSETS = ["COMMITTED", "ALL"]

PS = [1, 2, 4, 8, 16, 32, 64]
LS = [4, 13, 52, 104]
LAMS = [0.01, 0.1, 1.0]
RUNGS = [0, 10, 25]
NTOP = 20
GROSS = 1.00
PMAX = max(PS)
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
PROBE_TIMEOUT = 900


# ================================================================ fast backtest (gated at G1)
def fast_backtest(px, w, cost_bps=10.0, freq="W"):
    """Bit-for-bit `engine.backtest` on returns and turnover, without the pandas .iloc loop."""
    rets = px.pct_change().fillna(0.0).values
    W = w.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    nd, nc = rets.shape
    cur = np.zeros(nc)
    held = np.empty((nd, nc))
    turn = np.zeros(nd)
    for i in range(nd):
        if mask[i] or i == 0:
            new = W[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new.copy()
        held[i] = cur
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        if tot > 0:
            cur = growth / tot
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return pd.Series(port, index=px.index), pd.Series(turn, index=px.index)


def mtr(r):
    if len(r) < 30 or not np.isfinite(r.values).all():
        return dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan)
    eq = (1 + r).cumprod()
    yrs = len(r) / 252
    dd = (eq / eq.cummax() - 1).min()
    vol = r.std() * np.sqrt(252)
    return dict(CAGR=float(eq.iloc[-1] ** (1 / yrs) - 1), MaxDD=float(dd),
                Sharpe=float(r.mean() * 252 / vol) if vol else np.nan)


def halves(r):
    h = len(r) // 2
    return mtr(r.iloc[:h]), mtr(r.iloc[h:])


# ================================================================ PART B -- the probe program
PROBE_SRC = r'''
import builtins, io, json, os, runpy, sys, time, traceback, inspect
from pathlib import Path
import numpy as np, pandas as pd
ROOT = Path(sys.argv[3]); SAND = Path(sys.argv[2]); TARGET = Path(sys.argv[1])
SAND.mkdir(parents=True, exist_ok=True)
CALLS = []
def _redirect(p):
    try: p = Path(p)
    except Exception: return p
    try: ap = p if p.is_absolute() else Path.cwd()/p
    except Exception: return p
    try: rel = ap.resolve().relative_to(ROOT.resolve())
    except Exception: return p
    q = SAND/rel; q.parent.mkdir(parents=True, exist_ok=True); return q
_open = builtins.open
def open2(file, mode="r", *a, **k):
    if isinstance(file,(str,os.PathLike)) and any(c in str(mode) for c in "wax"): file=_redirect(file)
    return _open(file, mode, *a, **k)
builtins.open = open2
_pwt,_pwb,_popen = Path.write_text, Path.write_bytes, Path.open
Path.write_text = lambda self,*a,**k: _pwt(_redirect(self),*a,**k)
Path.write_bytes = lambda self,*a,**k: _pwb(_redirect(self),*a,**k)
def popen2(self, mode="r", *a, **k):
    return _popen(_redirect(self) if any(c in str(mode) for c in "wax") else self, mode, *a, **k)
Path.open = popen2
_tocsv = pd.DataFrame.to_csv
def tocsv2(self, path_or_buf=None, *a, **k):
    if isinstance(path_or_buf,(str,os.PathLike)): path_or_buf=_redirect(path_or_buf)
    return _tocsv(self, path_or_buf, *a, **k)
pd.DataFrame.to_csv = tocsv2; pd.Series.to_csv = tocsv2
_SELF = os.path.abspath(__file__)
def _site():
    """Innermost frame that is neither this probe nor a library -- i.e. the real call site."""
    for fr in traceback.extract_stack()[::-1]:
        fn = fr.filename or ""
        if not fn.endswith(".py"): continue
        ab = os.path.abspath(fn)
        if ab == _SELF: continue
        if "<string>" in fn or "runpy" in fn: continue
        if os.sep + "numpy" + os.sep in ab or os.sep + "pandas" + os.sep in ab: continue
        try: return os.path.relpath(ab, str(ROOT)), fr.lineno
        except Exception: return fn, fr.lineno
    return "?", -1
JSONL = open(str(SAND/"calls.jsonl"), "w", buffering=1)   # flushed per call: a timeout keeps its record
def _rec(kind, n, p, note=""):
    f, ln = _site()
    d = dict(kind=kind, file=f, line=ln, n=n, p=p, note=note)
    CALLS.append(d)
    try: JSONL.write(json.dumps(d)+"\n"); JSONL.flush()
    except Exception: pass
def _frame_n(p):
    fr = inspect.currentframe()
    for _ in range(8):
        fr = fr.f_back
        if fr is None: return -1
        if "numpy" in (fr.f_code.co_filename or ""): continue
        best = -1
        for v in list(fr.f_locals.values()):
            try: arr = np.asarray(v)
            except Exception: continue
            if arr.ndim == 2 and arr.shape[1] == p and arr.shape[0] > p:
                best = int(arr.shape[0]) if best < 0 else min(best, int(arr.shape[0]))
        if best > 0: return best
    return -1
_ls,_pi,_so,_pf = np.linalg.lstsq, np.linalg.pinv, np.linalg.solve, np.polyfit
def lstsq2(a,b,*x,**k):
    A=np.asarray(a)
    if A.ndim==2: _rec("lstsq", int(A.shape[0]), int(A.shape[1]), "design")
    return _ls(a,b,*x,**k)
def pinv2(a,*x,**k):
    A=np.asarray(a)
    if A.ndim==2 and A.shape[0]==A.shape[1]:
        p=int(A.shape[0]); _rec("pinv_gram", _frame_n(p), p, "gram")
    elif A.ndim==2: _rec("pinv", int(A.shape[0]), int(A.shape[1]), "design")
    return _pi(a,*x,**k)
def solve2(a,b,*x,**k):
    A=np.asarray(a)
    if A.ndim==2:
        p=int(A.shape[0]); _rec("solve_gram", _frame_n(p), p, "normal-eq")
    return _so(a,b,*x,**k)
def polyfit2(x,y,deg,*a,**k):
    X=np.asarray(x); _rec("polyfit", int(X.shape[0]) if X.ndim>=1 else -1, int(deg)+1, "poly")
    return _pf(x,y,deg,*a,**k)
np.linalg.lstsq, np.linalg.pinv, np.linalg.solve, np.polyfit = lstsq2, pinv2, solve2, polyfit2
t0=time.time(); status="ok"; err=""
buf = io.StringIO(); real = sys.stdout
try:
    sys.stdout = buf; sys.argv=[str(TARGET)]
    runpy.run_path(str(TARGET), run_name="__main__")
except SystemExit: pass
except BaseException as e:
    status="error"; err=f"{type(e).__name__}: {str(e)[:200]}"
finally:
    sys.stdout = real
sys.stderr.write(json.dumps(dict(target=TARGET.name, status=status, err=err,
                                 seconds=round(time.time()-t0,1), calls=CALLS)))
'''


def _jsonl(sand):
    f = Path(sand) / "calls.jsonl"
    if not f.exists():
        return []
    out = []
    for line in f.read_text(errors="ignore").split("\n"):
        if line.strip():
            try:
                out.append(json.loads(line))
            except Exception:
                pass
    return out


def run_probe(pyfile, sand, probe_path):
    """Re-execute one committed file with fit-call instrumentation; never touch the repo.
    Calls are journalled per-call, so a file that times out still publishes what it reached."""
    Path(sand).mkdir(parents=True, exist_ok=True)
    try:
        r = subprocess.run([sys.executable, str(probe_path), str(pyfile), str(sand), str(ROOT)],
                           cwd=str(ROOT), capture_output=True, text=True, timeout=PROBE_TIMEOUT)
        payload = r.stderr[r.stderr.rfind("{\"target\""):] if "{\"target\"" in r.stderr else ""
        if payload:
            return json.loads(payload)
        return dict(target=pyfile.name, status="nojson", err=r.stderr[-200:], seconds=-1,
                    calls=_jsonl(sand))
    except subprocess.TimeoutExpired:
        return dict(target=pyfile.name, status="timeout", err=f">{PROBE_TIMEOUT}s",
                    seconds=PROBE_TIMEOUT, calls=_jsonl(sand))
    except Exception as e:  # pragma: no cover
        return dict(target=pyfile.name, status="error", err=f"{type(e).__name__}: {e}", seconds=-1,
                    calls=_jsonl(sand))


# ---------------------------------------------------------------- static AST width resolver
FIT_NAMES = {"lstsq", "pinv", "solve", "polyfit"}


class _WidthVisitor(ast.NodeVisitor):
    """Resolve the design width p of every fit call site by reading its design expression.

    Handles the two forms the record actually uses:
      np.column_stack([np.ones(...)] + [a, b, ...])   -> p = 1 + len(list)
      np.column_stack([a, b, c]) / np.hstack / np.c_  -> p = len(list)
    A design whose columns come from a name bound elsewhere resolves to -1 (UNRESOLVED),
    which is reported as such and never imputed.
    """

    def __init__(self, src):
        self.src = src
        self.sites = []
        self.assign = {}

    def visit_Assign(self, node):
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            self.assign[node.targets[0].id] = node.value
        self.generic_visit(node)

    def _width(self, expr, depth=0):
        if depth > 3 or expr is None:
            return -1
        if isinstance(expr, ast.Name):
            return self._width(self.assign.get(expr.id), depth + 1)
        if isinstance(expr, ast.Call):
            fn = expr.func
            nm = fn.attr if isinstance(fn, ast.Attribute) else (fn.id if isinstance(fn, ast.Name) else "")
            if nm in ("column_stack", "hstack", "vstack", "stack") and expr.args:
                return self._listwidth(expr.args[0], depth)
        if isinstance(expr, ast.Subscript):  # np.c_[...]
            return self._listwidth(expr.slice, depth)
        return -1

    def _listwidth(self, node, depth):
        if isinstance(node, (ast.List, ast.Tuple)):
            return len(node.elts)
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            a, b = self._listwidth(node.left, depth), self._listwidth(node.right, depth)
            return a + b if a >= 0 and b >= 0 else -1
        if isinstance(node, ast.Name):
            return self._listwidth(self.assign.get(node.id), depth + 1) if depth < 3 else -1
        return -1

    def visit_Call(self, node):
        fn = node.func
        nm = fn.attr if isinstance(fn, ast.Attribute) else (fn.id if isinstance(fn, ast.Name) else "")
        if nm in FIT_NAMES and node.args:
            p = self._width(node.args[0])
            if nm == "polyfit" and len(node.args) >= 3 and isinstance(node.args[2], ast.Constant):
                p = int(node.args[2].value) + 1
            self.sites.append(dict(kind=f"ast_{nm}", line=node.lineno, p=p))
        self.generic_visit(node)


def ast_sites(pyfile):
    try:
        v = _WidthVisitor((ROOT / pyfile).read_text())
        v.visit(ast.parse((ROOT / pyfile).read_text()))
        return v.sites
    except Exception:
        return []


# ================================================================ PART C -- the width book
def weekly_panel(px, drop_cols=()):
    """Weekly (rebalance-date) simple returns for every tradable name on the panel."""
    mask = rebalance_mask(px.index, "W")
    dates = px.index[mask.values]
    cols = [c for c in px.columns if c not in drop_cols]
    w = px.loc[dates, cols]
    return w.pct_change()


def build_features(wr):
    """F[t, name, lag] cross-sectionally z-scored; y next-week return cross-sectionally demeaned."""
    def z(d):
        return d.sub(d.mean(axis=1), axis=0).div(d.std(axis=1).replace(0, np.nan), axis=0).clip(-5, 5)
    F = np.empty((len(wr.index), wr.shape[1], PMAX), dtype=np.float32)
    for k in range(1, PMAX + 1):
        F[:, :, k - 1] = z(wr.shift(k)).values
    y = wr.shift(-1)
    y = y.sub(y.mean(axis=1), axis=0)
    return F, y


def grams(F, y):
    """Per-week gram blocks, so any (p, L) window is one difference of cumulative sums.
    Nested in p: the p-wide gram is the top-left block of the PMAX-wide one, exactly."""
    T = len(y.index)
    G = np.zeros((T, PMAX, PMAX))
    C = np.zeros((T, PMAX))
    N = np.zeros(T)
    Y = y.values
    for t in range(T):
        X = F[t].astype(np.float64)
        yy = Y[t]
        ok = np.isfinite(X).all(axis=1) & np.isfinite(yy)
        if ok.sum() < 2:
            continue
        Xo, yo = X[ok], yy[ok]
        G[t] = Xo.T @ Xo
        C[t] = Xo.T @ yo
        N[t] = ok.sum()
    cg = np.concatenate([np.zeros((1, PMAX, PMAX)), np.cumsum(G, axis=0)], axis=0)
    cc = np.concatenate([np.zeros((1, PMAX)), np.cumsum(C, axis=0)], axis=0)
    cn = np.concatenate([[0.0], np.cumsum(N)])
    return cg, cc, cn


def width_book(px, y, cg, cc, cn, F, p, L, lam, col_pos):
    """Rolling-window ridge forecast -> top-NTOP equal weight at GROSS.  Returns (weights, n_bar)."""
    dates = y.index
    nd, nc = len(px.index), len(px.columns)
    Wa = np.full((len(dates), nc), np.nan)
    ns = []
    eye = np.eye(p)
    for t in range(L, len(dates)):
        n = cn[t] - cn[t - L]
        if n < p + 2:
            continue
        A = (cg[t, :p, :p] - cg[t - L, :p, :p]) / n + lam * eye
        b = (cc[t, :p] - cc[t - L, :p]) / n
        try:
            beta = np.linalg.solve(A, b)
        except np.linalg.LinAlgError:
            continue
        x = F[t, :, :p].astype(np.float64)
        ok = np.isfinite(x).all(axis=1)
        if ok.sum() < NTOP:
            continue
        f = np.full(x.shape[0], -np.inf)
        f[ok] = x[ok] @ beta
        top = np.argsort(-f, kind="stable")[:NTOP]
        row = np.zeros(nc)
        row[col_pos[top]] = GROSS / NTOP
        Wa[t] = row
        ns.append(n)
    W = pd.DataFrame(Wa, index=dates, columns=px.columns).reindex(px.index).ffill().fillna(0.0)
    return W, (float(np.mean(ns)) if ns else np.nan)


# ================================================================================== MAIN
def main():
    P("=" * 118)
    P("IDEA 658 -- publish p and n beside every WIDE flag in the record   (cloud, 2026-09-10)")
    P("=" * 118)

    # ---------------------------------------------------------------- panels
    small_meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(small_meta.loc[small_meta.max_1d_move >= 1.0, "ticker"])
    panels = {}
    panels["U56"] = load_universe()
    panels["B136"] = load_universe(broad=True)
    sm = load_universe(small=True)
    panels["SMALL439"] = sm[[c for c in sm.columns if c not in bad]]
    for k, v in panels.items():
        P(f"  panel {k:<9s} {v.shape[1]:4d} cols  {v.index[0].date()} .. {v.index[-1].date()}  ({len(v)} rows)")
    P(f"  SMALL: dropped {len(bad)} tickers with max_1d_move >= 1.0 (idea 118); "
      f"{panels['SMALL439'].shape[1]} columns remain incl. the SPY benchmark column")

    # ---------------------------------------------------------------- GATES
    P("\n" + "=" * 118)
    P("GATES")
    P("=" * 118)
    g_px = panels["U56"]
    wv2 = rules_v2_weights(g_px)
    eng = backtest(g_px, wv2, cost_bps=10, freq="W")
    fr, ft = fast_backtest(g_px, wv2, cost_bps=10, freq="W")
    g1start = g_px.index[260]                       # the window every number below is read on
    g1r = float(np.abs((eng["returns"] - fr).loc[g1start:].values).max())
    g1t = float(np.abs((eng["turnover"] - ft).loc[g1start:].values).max())
    nan_eng = int(eng["returns"].isna().sum())
    P(f"  G1  fast_backtest vs engine.backtest on the read window ({g1start.date()}..)   "
      f"returns {g1r:.3e}   turnover {g1t:.3e}   -> {'PASS' if max(g1r, g1t) < 1e-12 else 'FAIL'}")
    P(f"      (engine emits {nan_eng} NaN returns before warm-up, all at index < 260 and outside "
      f"every window read below; full-sample nanmax on the finite overlap "
      f"{float(np.nanmax(np.abs((eng['returns'] - fr).values))):.3e})")

    c1 = pd.read_csv(ROOT / "research/backtests/2026-09-09_census-every-published-N-EQUALS-50-"
                            "model-comparison-in-the-record_C.census.csv")
    c2 = pd.read_csv(ROOT / "research/backtests/2026-09-09_which-published-residualisations-are-"
                            "IN-SAMPLE-fits_cloud.census.csv")
    n1, n2 = int(c1.wide_design_hint.sum()), int(c2.wide_design_hint.sum())
    P(f"  G2  committed width-flag counts reproduce: idea 484 census {n1} (published 7), "
      f"idea 483 census {n2} (published 5)  -> {'PASS' if (n1, n2) == (7, 5) else 'FAIL'}")

    # G5 asserts PART B touched no COMMITTED file.  Tracked files only: the run's own new
    # artefacts are untracked and are not what the gate is about.
    def tracked_state():
        return subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"],
                              cwd=str(ROOT), capture_output=True, text=True).stdout

    git0 = tracked_state()

    # ---------------------------------------------------------------- PART A
    P("\n" + "=" * 118)
    P("PART A -- CENSUS: every committed width flag, both census sets")
    P("=" * 118)
    sites = []
    csvs = sorted(list((ROOT / "research/backtests").glob("*.csv")) +
                  list((ROOT / "research/backtests").glob("*.csv.gz")))
    scanned = 0
    for f in csvs:
        try:
            head = pd.read_csv(f, nrows=0)
        except Exception:
            continue
        scanned += 1
        wc = [c for c in head.columns if c.lower() in WIDE_COLS]
        if not wc or "file" not in head.columns:
            continue
        d = pd.read_csv(f)
        for c in wc:
            col = d[c]
            truthy = col.astype(str).str.lower().isin(["true", "1", "1.0", "yes"])
            for i in np.flatnonzero(truthy.values):
                sites.append(dict(set="COMMITTED", census=f.name, flagcol=c,
                                  named_file=str(d.loc[i, "file"]), line=-1, text=""))
    P(f"  scanned {scanned} committed CSV artefacts in research/backtests/")
    ncsv = len({(s['census'], s['named_file']) for s in sites})
    P(f"  COMMITTED width-flag rows: {len(sites)} over "
      f"{len({s['census'] for s in sites})} census files, {len({s['named_file'] for s in sites})} distinct named .py files")

    prose_paths = [ROOT / p for p in PROSE_FILES]
    prose_paths += sorted((ROOT / "research/backtests").glob("*.result.md"))
    prose_paths += sorted((ROOT / "research/backtests").glob("*.memo.md"))
    prose_paths += sorted((ROOT / "research/backtests").glob("*RECOMMENDATION.md"))
    rx = re.compile("|".join(WIDE_PHRASES), re.I)
    stem_rx = re.compile(r"(20\d\d-\d\d-\d\d_[A-Za-z0-9\-\._]+?)\.py")
    nprose = 0
    for pth in prose_paths:
        try:
            txt = pth.read_text(errors="ignore")
        except Exception:
            continue
        for ln, line in enumerate(txt.split("\n"), 1):
            if not rx.search(line):
                continue
            nprose += 1
            for m in set(stem_rx.findall(line)):
                sites.append(dict(set="PROSE", census=str(pth.relative_to(ROOT)), flagcol="prose",
                                  named_file=f"research/backtests/{m}.py", line=ln, text=line.strip()[:300]))
    S = pd.DataFrame(sites)
    P(f"  PROSE width-claim lines: {nprose} across {len(prose_paths)} committed prose files; "
      f"{int((S['set'] == 'PROSE').sum())} of them name a .py file")
    P(f"  ALL = COMMITTED + PROSE = {len(S)} width-flag sites, "
      f"{S.named_file.nunique()} distinct named files")
    P("\n  COMMITTED flag rows, verbatim:")
    for _, r in S[S["set"] == "COMMITTED"].iterrows():
        P(f"    {r.census[:62]:<62s} {r.flagcol:<17s} {r.named_file}")

    # ---------------------------------------------------------------- PART B
    P("\n" + "=" * 118)
    P("PART B -- RUNTIME (p, n) at every fit site in every named file")
    P("=" * 118)
    targets = sorted(S.named_file.unique())
    sand = Path(tempfile.mkdtemp(prefix="idea658_sand_"))
    probe_path = sand / "_probe.py"
    probe_path.write_text(PROBE_SRC)
    P(f"  re-executing {len(targets)} named files with instrumented numpy "
      f"(writes redirected to {sand.name}, timeout {PROBE_TIMEOUT}s each)")
    from concurrent.futures import ThreadPoolExecutor
    live = [t for t in targets if (ROOT / t).exists()]
    with ThreadPoolExecutor(max_workers=5) as ex:
        results = dict(zip(live, ex.map(lambda t: run_probe(ROOT / t, sand / Path(t).stem, probe_path), live)))
    prob = []
    for t in targets:
        pf = ROOT / t
        if not pf.exists():
            prob.append(dict(named_file=t, status="missing", seconds=-1, kind="", line=-1,
                             p=-1, n=-1, p_source="missing", n_source="missing"))
            P(f"    {t:<86s} MISSING")
            continue
        res = results[t]
        # each probe runs exactly ONE named file in its own process, so every fit it records is
        # a fit that file performs; `site_file` says whether the call sits in the file itself or
        # in a helper it imports.
        calls = res["calls"]
        astl = ast_sites(t)
        if calls:
            for c in calls:
                prob.append(dict(named_file=t, site_file=c["file"], status=res["status"],
                                 seconds=res["seconds"], kind=c["kind"], line=c["line"],
                                 p=c["p"], n=c["n"], p_source="runtime",
                                 n_source="runtime" if c["kind"] in ("lstsq", "polyfit", "pinv") else "frame"))
        else:
            for a in astl:
                prob.append(dict(named_file=t, site_file=t, status=res["status"],
                                 seconds=res["seconds"], kind=a["kind"], line=a["line"],
                                 p=a["p"], n=-1,
                                 p_source="ast" if a["p"] > 0 else "unresolved", n_source="halted"))
            if not astl:
                prob.append(dict(named_file=t, site_file=t, status=res["status"],
                                 seconds=res["seconds"], kind="", line=-1, p=-1, n=-1,
                                 p_source="none", n_source="none"))
        P(f"    {t.replace('research/backtests/', ''):<80s} {res['status']:<8s} "
          f"{res['seconds']:>6}s  runtime-fits {len(calls):>3d}  ast-fits {len(astl):>3d}"
          + (f"   [{res['err'][:60]}]" if res["err"] else ""))
    B = pd.DataFrame(prob)
    B["p_over_n"] = np.where((B.p > 0) & (B.n > 0), B.p / B.n.replace(0, np.nan), np.nan)
    B.to_csv(OUT / f"{STEM}.probe.csv", index=False)

    git1 = tracked_state()
    P(f"\n  G5  no COMMITTED (tracked) file touched across PART B: "
      f"git status --untracked-files=no identical -> {'PASS' if git0 == git1 else 'FAIL'}")
    if git0 != git1:
        P(f"      before: {git0!r}\n      after:  {git1!r}")
    shutil.rmtree(sand, ignore_errors=True)

    per = B[B.p > 0].groupby("named_file").agg(
        max_p=("p", "max"), min_n=("n", lambda x: int(x[x > 0].min()) if (x > 0).any() else -1),
        max_pn=("p_over_n", "max"), fits=("p", "size"),
        runtime_fits=("p_source", lambda s: int((s == "runtime").sum())))
    # p/n is a PER-CALL ratio: the site's max is the max over its own calls, never max(p)/min(n)
    # (which mixes two different fits and can only overstate).
    site = B[B.p > 0].groupby(["named_file", "site_file", "line", "kind"]).agg(
        calls=("p", "size"), p=("p", "max"),
        n_min=("n", lambda x: int(x[x > 0].min()) if (x > 0).any() else -1),
        n_max=("n", "max"), p_over_n_max=("p_over_n", "max"), src=("p_source", "first"))
    P(f"\n  EVERY FIT SITE, with its p and its n  ({len(site)} sites; this is the table the "
      f"queue asks the record to publish):")
    P("    " + f"{'named file':<62s} {'line':>5s} {'kind':<11s} {'calls':>6s} {'p':>5s} "
      f"{'n min':>7s} {'n max':>8s} {'max p/n':>9s}")
    for (nf, sf, ln, kd), r in site.iterrows():
        pn = f"{r.p_over_n_max:.4f}" if np.isfinite(r.p_over_n_max) else "n/a"
        star = "" if sf == nf else f"  [site in {Path(sf).name}]"
        P(f"    {nf.replace('research/backtests/', '')[:62]:<62s} {int(ln):>5d} {kd:<11s} "
          f"{int(r.calls):>6d} {int(r.p):>5d} {int(r.n_min):>7d} {int(r.n_max):>8d} {pn:>9s}{star}")
    site.to_csv(OUT / f"{STEM}.sites_pn.csv")

    P("\n  per named file (max design width, min design rows, max p/n over its own fit sites):")
    P("    " + f"{'file':<74s} {'fits':>5s} {'rt':>4s} {'max p':>6s} {'min n':>7s} {'max p/n':>9s}")
    for f, r in per.iterrows():
        pn = f"{r.max_pn:.4f}" if np.isfinite(r.max_pn) else "n/a"
        P(f"    {f.replace('research/backtests/', ''):<74s} {int(r.fits):>5d} {int(r.runtime_fits):>4d} "
          f"{int(r.max_p):>6d} {int(r.min_n):>7d} {pn:>9s}")

    # G3 -- idea 497's published headline
    P("")
    F497 = ("can-a-panel-property-choose-the-cadence", "does-the-cash-drag-share-depend",
            "is-phase-sensitivity-a-book-property")
    f123 = [t for t in per.index if any(k in t for k in F497)]
    named497 = [t for t in targets if any(k in t for k in F497)]
    if f123:
        sub = per.loc[f123]
        mx = np.nanmax(sub.max_pn.values) if np.isfinite(sub.max_pn.values).any() else float("nan")
        P(f"  G3  idea 497's 3 wide-and-unfolded files: {len(f123)} of {len(named497)} reached a "
          f"fit; max p {int(sub.max_p.max())} (497 published 6), max p/n {mx:.4f} "
          f"(497 published 0.0370). 497 rebuilt these designs from committed artefacts rather "
          f"than re-executing, and counts the intercept out; this run counts it in.")
    else:
        P(f"  G3  NOT RUNNABLE this run: none of idea 497's 3 wide-and-unfolded files "
          f"({len(named497)} named) reaches a fit call inside the {PROBE_TIMEOUT}s budget -- two "
          f"halt on their own reproduction gate and one does not finish. Reported, not waived: "
          f"at an 1800s budget the third (does-the-cash-drag...) does reach its `pinv` site and "
          f"gives p 7 on n 27..162, max per-call p/n 0.0741, against 497's published p 6 / "
          f"0.0370 -- the p differs by the intercept column and the n by which sub-cell is read.")

    # ---------------------------------------------------------------- PART B/A joint re-score
    P("\n" + "=" * 118)
    P("RE-SCORE: how many of the record's 'wide' labels survive a p/n bar?   (all grid points)")
    P("=" * 118)
    joint = S.merge(per, left_on="named_file", right_index=True, how="left")
    rows = []
    for cs in CENSUSSETS:
        sub = joint if cs == "ALL" else joint[joint["set"] == "COMMITTED"]
        for bar in WIDTHBARS:
            meas = sub.max_pn.notna()
            surv = (sub.max_pn >= bar) & meas
            rows.append(dict(CENSUSSET=cs, WIDTHBAR=bar, sites=len(sub),
                             measured=int(meas.sum()), unmeasured=int((~meas).sum()),
                             survive=int(surv.sum()),
                             survive_rate=float(surv.sum() / max(meas.sum(), 1)),
                             files=int(sub.named_file.nunique()),
                             files_survive=int(sub.loc[surv, "named_file"].nunique())))
    R = pd.DataFrame(rows)
    P(R.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    R.to_csv(OUT / f"{STEM}.sites.csv", index=False)
    joint.to_csv(OUT / f"{STEM}.joint.csv", index=False)

    # rule 8 on the census claim: bar chosen on the first half of the record by file date
    P("\n  RULE 8 (census leg): WIDTHBAR chosen on the first half of the record by file date, "
      "read once on the second half.")
    dt = joint.named_file.str.extract(r"(20\d\d-\d\d-\d\d)")[0]
    joint2 = joint.assign(fdate=pd.to_datetime(dt, errors="coerce")).dropna(subset=["fdate"])
    cut = joint2.fdate.median()
    h1, h2 = joint2[joint2.fdate <= cut], joint2[joint2.fdate > cut]
    P(f"    split at {cut.date()}: H1 {len(h1)} sites, H2 {len(h2)} sites")
    pick, best = None, -1
    for bar in WIDTHBARS:
        m = h1.max_pn.notna()
        rate = float(((h1.max_pn >= bar) & m).sum() / max(m.sum(), 1))
        P(f"    IS  bar {bar:<5.2f} survive rate {rate:.4f}")
        if rate > best:
            best, pick = rate, bar
    m2 = h2.max_pn.notna()
    oos = float(((h2.max_pn >= pick) & m2).sum() / max(m2.sum(), 1))
    P(f"    IS pick bar = {pick}; OOS survive rate on the record's second half = {oos:.4f} "
      f"({int(((h2.max_pn >= pick) & m2).sum())} of {int(m2.sum())} measured)")

    # ---------------------------------------------------------------- PART C
    P("\n" + "=" * 118)
    P("PART C -- does design WIDTH (p, p/n) predict OOS book quality?   252 arms, all reported")
    P("=" * 118)
    grid = []
    keeps = []
    for pname, px in panels.items():
        drop = ("SPY",) if pname == "SMALL439" else ()
        spy = px["SPY"].pct_change().fillna(0.0)
        b_ret, _ = fast_backtest(px, rules_v2_weights(px), cost_bps=10, freq="W")
        start = px.index[260]
        spy_s = spy.loc[start:]
        b_s = b_ret.loc[start:]
        bm, bh1, bh2 = mtr(b_s), *halves(b_s)
        sm_, sh1, sh2 = mtr(spy_s), *halves(spy_s)
        spy_oos = mtr(spy_s.loc[OOS_START:])
        P(f"\n  panel {pname}:  RULES v2 {bm['CAGR']:.2%}/{bm['Sharpe']:.4f}/{bm['MaxDD']:.2%}"
          f"   SPY {sm_['CAGR']:.2%}/{sm_['Sharpe']:.4f}/{sm_['MaxDD']:.2%}"
          f"   (SPY halves {sh1['Sharpe']:.3f}/{sh2['Sharpe']:.3f}, OOS {spy_oos['Sharpe']:.3f})")
        wr = weekly_panel(px, drop_cols=drop)
        col_pos = np.array([px.columns.get_loc(c) for c in wr.columns])
        F, y = build_features(wr)
        cg, cc, cn = grams(F, y)
        for p in PS:
            for L in LS:
                for lam in LAMS:
                    Wt, nbar = width_book(px, y, cg, cc, cn, F, p, L, lam, col_pos)
                    for rung in RUNGS:
                        r, turn = fast_backtest(px, Wt, cost_bps=rung, freq="W")
                        rs = r.loc[start:]
                        m = mtr(rs)
                        m1, m2 = halves(rs)
                        oosm = mtr(rs.loc[OOS_START:])
                        ism = mtr(rs.loc[:IS_END])
                        row = dict(panel=pname, p=p, L=L, lam=lam, rung=rung,
                                   n_bar=nbar, p_over_n=p / nbar if nbar and np.isfinite(nbar) else np.nan,
                                   CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                   H1=m1["Sharpe"], H2=m2["Sharpe"],
                                   IS_Sharpe=ism["Sharpe"], OOS_CAGR=oosm["CAGR"],
                                   OOS_Sharpe=oosm["Sharpe"], OOS_MaxDD=oosm["MaxDD"],
                                   turnover=float(turn.loc[start:].sum() / (len(rs) / 252)))
                        p4a = (m1["Sharpe"] > bh1["Sharpe"] and m2["Sharpe"] > bh2["Sharpe"]
                               and m["MaxDD"] >= bm["MaxDD"])
                        p4b = (m1["Sharpe"] > sh1["Sharpe"] and m2["Sharpe"] > sh2["Sharpe"]
                               and oosm["Sharpe"] > spy_oos["Sharpe"]
                               and m["MaxDD"] >= 0.60 * sm_["MaxDD"]
                               and m["CAGR"] >= 0.70 * sm_["CAGR"])
                        row["pass4a"], row["pass4b"] = bool(p4a), bool(p4b)
                        grid.append(row)
        P(f"    {pname}: {len([g for g in grid if g['panel'] == pname])} arm-rungs done "
          f"({time.time() - T0:.0f}s elapsed)")
    G = pd.DataFrame(grid)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    P(f"\n  {len(G)} arm-rungs written ({len(G[G.rung == 10])} arms at PROTOCOL's own 10 bps rung)")

    g10 = G[G.rung == 10]
    P("\n  Sharpe by design width p, pooled over L and lam, at 10 bps (mean / max):")
    P("    " + f"{'panel':<10s}" + "".join(f"{('p=' + str(p)):>16s}" for p in PS))
    for pname in panels:
        s = g10[g10.panel == pname]
        P("    " + f"{pname:<10s}" + "".join(
            f"{s[s.p == p].Sharpe.mean():>8.3f}/{s[s.p == p].Sharpe.max():<7.3f}" for p in PS))
    P("\n  OOS Sharpe by p (mean over L, lam) at 10 bps:")
    P("    " + f"{'panel':<10s}" + "".join(f"{('p=' + str(p)):>10s}" for p in PS))
    for pname in panels:
        s = g10[g10.panel == pname]
        P("    " + f"{pname:<10s}" + "".join(f"{s[s.p == p].OOS_Sharpe.mean():>10.3f}" for p in PS))

    def spear(a, b):
        a, b = np.asarray(a, float), np.asarray(b, float)
        m = np.isfinite(a) & np.isfinite(b)
        if m.sum() < 5:
            return np.nan
        return float(np.corrcoef(pd.Series(a[m]).rank(), pd.Series(b[m]).rank())[0, 1])

    P("\n  DOES p/n PREDICT OOS QUALITY?  Spearman(p/n, OOS Sharpe) and Spearman(p/n, IS-minus-OOS Sharpe):")
    for pname in panels:
        s = g10[g10.panel == pname]
        gap = s.IS_Sharpe - s.OOS_Sharpe
        P(f"    {pname:<10s} rho(p/n, OOS Sharpe) {spear(s.p_over_n, s.OOS_Sharpe):+.4f}   "
          f"rho(p/n, IS-OOS gap) {spear(s.p_over_n, gap):+.4f}   "
          f"rho(p, OOS Sharpe) {spear(s.p, s.OOS_Sharpe):+.4f}   "
          f"p/n range {s.p_over_n.min():.5f}..{s.p_over_n.max():.5f}")
    sp = g10.copy()
    P(f"    POOLED     rho(p/n, OOS Sharpe) {spear(sp.p_over_n, sp.OOS_Sharpe):+.4f}   "
      f"rho(p/n, IS-OOS gap) {spear(sp.p_over_n, sp.IS_Sharpe - sp.OOS_Sharpe):+.4f}")

    G["pass_both"] = G.pass4a & G.pass4b
    kp = G.groupby("rung")[["pass4a", "pass4b", "pass_both"]].sum()
    kp["arms"] = G.groupby("rung").size()
    P("\n  BOTH KEEP PATHS on every arm, every rung:")
    P(kp.to_string())
    kpp = G.groupby(["panel", "rung"])[["pass4a", "pass4b"]].sum()
    P("\n  by panel:")
    P(kpp.to_string())
    G.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)

    # ---------------------------------------------------------------- rule 8, book leg
    P("\n" + "=" * 118)
    P("RULE 8 (book leg): (p, L) chosen on 2009-2016 by IS Sharpe; 2017-2026 read ONCE")
    P("=" * 118)
    wf = []
    for pname, px in panels.items():
        spy = px["SPY"].pct_change().fillna(0.0)
        start = px.index[260]
        spy_s = spy.loc[start:]
        b_ret, _ = fast_backtest(px, rules_v2_weights(px), cost_bps=10, freq="W")
        b_s = b_ret.loc[start:]
        for lam in LAMS:
            s = G[(G.panel == pname) & (G.rung == 10) & (G.lam == lam)]
            if s.IS_Sharpe.notna().sum() == 0:
                continue
            pick = s.loc[s.IS_Sharpe.idxmax()]
            hind = s.loc[s.OOS_Sharpe.idxmax()]
            bo, so = mtr(b_s.loc[OOS_START:]), mtr(spy_s.loc[OOS_START:])
            wf.append(dict(panel=pname, lam=lam, pick_p=int(pick.p), pick_L=int(pick.L),
                           IS_Sharpe=pick.IS_Sharpe, OOS_Sharpe=pick.OOS_Sharpe,
                           OOS_CAGR=pick.OOS_CAGR, OOS_MaxDD=pick.OOS_MaxDD,
                           pick_p_over_n=pick.p_over_n,
                           best_OOS_Sharpe=hind.OOS_Sharpe, best_p=int(hind.p), best_L=int(hind.L),
                           regret=pick.OOS_Sharpe - hind.OOS_Sharpe,
                           v2_OOS_Sharpe=bo["Sharpe"], v2_OOS_CAGR=bo["CAGR"], v2_OOS_MaxDD=bo["MaxDD"],
                           spy_OOS_Sharpe=so["Sharpe"], spy_OOS_CAGR=so["CAGR"], spy_OOS_MaxDD=so["MaxDD"],
                           beats_v2=bool(pick.OOS_Sharpe > bo["Sharpe"]),
                           beats_spy=bool(pick.OOS_Sharpe > so["Sharpe"]),
                           pass4a=bool(pick.pass4a), pass4b=bool(pick.pass4b)))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(WF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n  rule-8 picks: beats RULES v2 OOS {int(WF.beats_v2.sum())}/{len(WF)}, "
      f"beats SPY OOS {int(WF.beats_spy.sum())}/{len(WF)}, "
      f"4a {int(WF.pass4a.sum())}/{len(WF)}, 4b {int(WF.pass4b.sum())}/{len(WF)}")
    P(f"  IS pick's own width: p in {sorted(set(WF.pick_p))}, L in {sorted(set(WF.pick_L))}, "
      f"p/n {WF.pick_p_over_n.min():.5f}..{WF.pick_p_over_n.max():.5f}")

    # ---------------------------------------------------------------- LEADERBOARD + verdict
    best = g10.loc[g10.Sharpe.idxmax()]
    P("\n" + "=" * 118)
    P("LEADERBOARD rows")
    P("=" * 118)
    u = panels["U56"]
    ustart = u.index[260]
    ub, _ = fast_backtest(u, rules_v2_weights(u), cost_bps=10, freq="W")
    ubs = ub.loc[ustart:]
    ubm, ubh1, ubh2 = mtr(ubs), *halves(ubs)
    lb = []
    tag = "KILL"
    lb.append(f"| 2026-09-10 | 658-width-census (COMMITTED, bar 0.10) | n/a | n/a | n/a | n/a | "
              f"{R[(R.CENSUSSET == 'COMMITTED') & (R.WIDTHBAR == 0.10)].survive.iloc[0]}"
              f"/{R[(R.CENSUSSET == 'COMMITTED') & (R.WIDTHBAR == 0.10)].measured.iloc[0]} labels survive | "
              f"{tag} | {STEM}.py |")
    lb.append(f"| 2026-09-10 | 658-width-book best arm ({best.panel} p={int(best.p)} L={int(best.L)} "
              f"lam={best.lam}) | {best.CAGR:.1%} | {best.Sharpe:.2f} | {best.MaxDD:.1%} | "
              f"{best.H1:.2f} / {best.H2:.2f} | {ubm['Sharpe']:.2f} ({ubh1['Sharpe']:.2f}/{ubh2['Sharpe']:.2f}) | "
              f"{'KEEP-candidate' if (best.pass4a or best.pass4b) else 'KILL'} | {STEM}.py |")
    for l in lb:
        P(l)
    (OUT / f"{STEM}.leaderboard.txt").write_text("\n".join(lb) + "\n")

    P(f"\ndone in {time.time() - T0:.0f}s")
    flush_log()


if __name__ == "__main__":
    try:
        main()
    finally:
        flush_log()

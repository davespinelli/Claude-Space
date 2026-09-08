#!/usr/bin/env python3
"""QUEUE idea 428 — census-the-record-s-other-DOLLAR-floors-and-caps (lane C, 2026-09-08).

Question (verbatim from QUEUE)
-----------------------------
"idea 197's census found the LEVEL construction in 7 of 361 scripts, but idea 425 shows the
damaging form is an ABSOLUTE cut on `(px*vol)` in an ELIGIBILITY MASK, not a tilt.  Census every
committed script for absolute cuts on any price-bearing quantity used as a mask (dollar volume,
market cap, notional, price floors) and rank them by the admission-rate share they gate, so the
record knows which files are worth re-running.  Cheap; max 2 params."

What is on trial.  Not a book.  Two things: (i) a COUNT — how many committed scripts carry the
damaging form — and (ii) a RANKING — how much of the panel each such cut actually removes, which
is what decides whether a flagged file is worth re-running.  Idea 425 established the form matters
(+1.23 pp/yr at matched admission on SMALL439); this run asks how much of the record it touches.

The instrument: an ABSOLUTE-CUT DETECTOR, not a regex
-----------------------------------------------------
Idea 197's theorem: a mask is contaminated by the adjustment channel iff it is NOT invariant under
T1: px -> px @ diag(c), c_i > 0.  A comparison `K(px) >= L` is invariant iff K is homogeneous of
degree 0 in the price scale, OR the threshold L scales with the panel (a quantile).  So the
detector is a HOMOGENEITY-DEGREE analysis over the AST, not a name match:

    deg(px) = 1;  deg(share volume, returns, ranks, anything not provably price-borne) = 0
    deg(a*b) = deg(a)+deg(b);  deg(a/b) = deg(a)-deg(b);  rolling/median/shift/quantile preserve
    deg;  pct_change/rank/corr/notna return 0

A Compare node is FLAGGED iff one side has deg >= 1 AND is provably built from a price symbol
(origin tracking, so `q > q.rolling(200).mean()` and other price-vs-price comparisons are exempt),
AND the other side resolves to a dimensionless CONSTANT — a literal, a module constant, a numeric
loop variable, or a parameter whose every call site in the file passes one of those.  Cuts at
level 0 are reported separately: `px > 0` is exactly T1-invariant and is not a leak.

Three buckets are reported so the count has a denominator and a recall floor:
  B1  absolute cut on a price-bearing quantity, level RESOLVED       <- the damaging form
  B2  price-bearing side vs a threshold the analyser could not resolve to a constant  <- adjudicate
  B3  price-bearing side vs another price-bearing side (scale-covariant: `px > ma`)   <- safe
  Z   absolute cut at level 0 (T1-invariant)                                          <- safe

PRE-REGISTERED (fixed before any number in Q2-Q5 was read; Q1 is a census, not a test, and its
counts were necessarily read first — that is stated rather than dressed up as a prediction)
--------------------------------------------------------------------------------------------
P1  RANKING.  Ranked by admission-rate share gated on the panel each file uses, the $1M DV floor
    gates a LARGER share of live ticker-days than a 20d-median PRICE floor calibrated to the
    record's usual $5 level.  (If false, the record's unused cut class is the more dangerous one.)
P2  THE DAMAGE IS THE ADMISSION, NOT THE KEY.  At MATCHED admission rate, the three keys
    (DV = px*vol, VOLSH = vol, PXL = px) admit panels whose CAGR differ; and the two price-bearing
    keys (DV, PXL) land on the SAME side of the price-free key (VOLSH).  Idea 425 measured
    VOLSH > DV by +1.23 pp on SMALL439; P2 predicts VOLSH > PXL as well, in the same sign.
P3  BOOK.  No floor arm clears 4b on SMALL439 at any level or instrument, and the rule-8 chooser's
    OOS pick does not beat SPY.  (SMALL439 is survivorship-biased upward, so a 4b pass there would
    be evidence against the panel, not for the book.)
P4  EXPOSURE.  The count of LEADERBOARD rows sitting under flagged files is the record's exposure;
    it is reported per file and multiplied by the gated share to rank re-run priority.

Design (PROTOCOL rules 1-9)
---------------------------
Panels     SMALL439 and U56 via idea 425's `build_panels`, verbatim.  SURVIVORSHIP: both are
           CURRENT constituents; on SMALL439 the missing delisted cohort is exactly the thin names
           a liquidity floor argues about, so only FLOOR-MINUS-FLOOR contrasts (same book, same
           days, same arms) are read, never a level.  No book is proposed on it.
Books      EWALL (no gate) and MA200 (the incumbent 200d trend gate), gross 0.75, conventions rw
           and dg — 4 book-forms, all reported.
Instrum.   NONE (identity), DV = (px*vol).rolling(20).median(), VOLSH = vol.rolling(20).median(),
           PXL = px.rolling(20).median().  DV/VOLSH need the volume cache -> SMALL439 only;
           PXL runs on both panels.  All floors are applied on a COMMON SUPPORT S (live & all
           three keys finite) so admission rates are matched exactly, not approximately.
Levels     DV in {0, 0.5, 1, 2, 5} $M — 1 is idea 121's proposed PROTOCOL clause.  For each
           non-zero DV level the VOLSH and PXL levels are SOLVED from a pooled-quantile identity
           so total admitted ticker-days match DV's exactly.  The full ladder is printed.
Tuned      EXACTLY TWO: the cut INSTRUMENT (NONE/DV/VOLSH/PXL) and its LEVEL.  Every grid point is
           reported; none is selected outside the rule-8 block, where the level is chosen on
           2010-2016 only.
Costs      0/5/10/25 bps, all reported; PROTOCOL rung 10 bps for verdicts.
Rule 8     Level chosen on 2010..2016 by IS Sharpe within each (panel, instrument, book, conv)
           cell; 2017..2026 read once against SPY, the no-floor control and the incumbent.
Both KEEP  4a vs the live RULES v2 book at the same cost rung; 4b vs SPY + rule 8, on every point.
paths

Outputs: .console.txt, .census.csv, .gating.csv, .ladder.csv, .grid.csv, .walkforward.csv,
         .verdicts.csv, .result.md
"""
import ast
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "research" / "backtests"
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, load_volume, rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-08_census-the-record-s-other-DOLLAR-floors-and-caps_C"
FREQ, GROSS, MAX_VOL = "W", 0.75, 0.60
COSTS = [0, 5, 10, 25]
PROTO_COST = 10
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DV_LEVELS = [0.0, 0.5e6, 1.0e6, 2.0e6, 5.0e6]
PX_REF_LEVEL = 5.0                      # the record's usual price-floor level, for P1
BOOKS = ["EWALL", "MA200"]
CONVS = ["rw", "dg"]

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


# =====================================================================================
# PART 0 — the absolute-cut detector (AST homogeneity analysis)
# =====================================================================================
PRICE1 = re.compile(r"^(px|pxs|price|prices|close|closes|adjclose|adj_close|mcap|marketcap|"
                    r"market_cap|capq|cap_usd|notional|nav)([0-9_].*)?$", re.I)
KEEP_DEG = {"values", "squeeze", "to_frame", "transpose", "rolling", "mean", "median", "sum",
            "min", "max", "shift", "ffill", "bfill", "fillna", "dropna", "reindex", "loc", "iloc",
            "abs", "where", "clip", "ewm", "expanding", "cumsum", "cummax", "cummin", "cumprod",
            "copy", "astype", "sort_index", "stack", "unstack", "quantile", "first", "last",
            "resample", "div", "mul", "sub", "add", "reindex_like", "interpolate", "round",
            "tail", "head", "std", "var"}
FREE_DEG = {"pct_change", "rank", "corr", "cov", "idxmax", "idxmin", "argsort", "notna", "isna",
            "any", "all", "count", "nunique", "value_counts", "eq", "ne", "gt", "lt", "ge", "le",
            "isin", "index", "columns", "dayofweek", "year", "month", "shape", "size", "dtypes",
            "str", "sign", "diff"}
MASKISH = re.compile(r"(mask|elig|sel|admit|tradab|univ|invest|keep|live|avail|allow|floor|cap)",
                     re.I)


def _isnum(x):
    return isinstance(x, ast.Constant) and isinstance(x.value, (int, float)) \
        and not isinstance(x.value, bool)


class Mod:
    """Per-file homogeneity-degree and numeric-constant analysis."""

    def __init__(self, tree):
        self.tree = tree
        self.consts = {}
        for n in tree.body:
            if isinstance(n, ast.Assign) and len(n.targets) == 1 \
               and isinstance(n.targets[0], ast.Name):
                if _isnum(n.value):
                    self.consts[n.targets[0].id] = {n.value.value}
                elif isinstance(n.value, (ast.List, ast.Tuple)) and n.value.elts \
                        and all(_isnum(e) for e in n.value.elts):
                    self.consts[n.targets[0].id] = {e.value for e in n.value.elts}
        for _ in range(2):                                  # numeric loop variables
            for n in ast.walk(tree):
                if isinstance(n, (ast.For, ast.comprehension)):
                    vals = self._numiter(n.iter)
                    if vals and isinstance(n.target, ast.Name):
                        self.consts[n.target.id] = self.consts.get(n.target.id, set()) | vals
        self.funcs = {f.name: f for f in ast.walk(tree) if isinstance(f, ast.FunctionDef)}
        self.callsites = {}
        self._scan_calls()
        self.retdeg = {}
        self._infer_returns()

    # -- numeric-constant resolution ---------------------------------------------------
    def _numiter(self, it, depth=0):
        if depth > 4:
            return None
        if isinstance(it, (ast.List, ast.Tuple)):
            if not it.elts:
                return None
            vals = set()
            for e in it.elts:
                v = self.numconst(e, None)
                if v is None:
                    return None
                vals |= v
            return vals
        if isinstance(it, ast.Name):
            return self.consts.get(it.id)
        if isinstance(it, ast.IfExp):
            a, b = self._numiter(it.body, depth + 1), self._numiter(it.orelse, depth + 1)
            if a is None and b is None:
                return None
            return (a or set()) | (b or set())
        if isinstance(it, ast.Call) and isinstance(it.func, ast.Name) \
                and it.func.id in {"sorted", "list", "tuple", "reversed", "set"} and it.args:
            return self._numiter(it.args[0], depth + 1)
        return None

    def numconst(self, n, sc, depth=0):
        if depth > 12:
            return None
        if _isnum(n):
            return {n.value}
        if isinstance(n, ast.Name):
            if sc is not None and n.id in sc:
                return sc[n.id]
            return self.consts.get(n.id)
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub):
            v = self.numconst(n.operand, sc, depth + 1)
            return None if v is None else {-x for x in v}
        if isinstance(n, ast.BinOp):
            a, b = self.numconst(n.left, sc, depth + 1), self.numconst(n.right, sc, depth + 1)
            if a is None or b is None:
                return None
            out = set()
            for x in a:
                for y in b:
                    try:
                        if isinstance(n.op, ast.Mult):
                            out.add(x * y)
                        elif isinstance(n.op, ast.Add):
                            out.add(x + y)
                        elif isinstance(n.op, ast.Sub):
                            out.add(x - y)
                        elif isinstance(n.op, ast.Div):
                            out.add(x / y)
                        elif isinstance(n.op, ast.Pow):
                            out.add(x ** y)
                        else:
                            return None
                    except Exception:
                        return None
            return out
        return None

    def _scan_calls(self):
        for fname, f in self.funcs.items():
            params = [a.arg for a in f.args.args]
            acc = {p: set() for p in params}
            bad, seen = set(), False
            for d, a in zip(reversed(f.args.defaults), reversed(params)):
                if _isnum(d):
                    acc[a].add(d.value)
                elif d is not None:
                    bad.add(a)
            for n in ast.walk(self.tree):
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) \
                        and n.func.id == fname:
                    seen = True
                    for i, arg in enumerate(n.args):
                        if i >= len(params):
                            break
                        v = self.numconst(arg, None)
                        (bad.add(params[i]) if v is None else acc[params[i]].update(v))
                    for kw in n.keywords:
                        if kw.arg in acc:
                            v = self.numconst(kw.value, None)
                            (bad.add(kw.arg) if v is None else acc[kw.arg].update(v))
            self.callsites[fname] = {p: (None if (p in bad or not acc[p] or not seen) else acc[p])
                                     for p in params}

    # -- homogeneity degree -------------------------------------------------------------
    def _assigns(self, node, sc):
        for _ in range(3):
            for a in ast.walk(node):
                if isinstance(a, ast.Assign) and len(a.targets) == 1 \
                        and isinstance(a.targets[0], ast.Name):
                    sc[a.targets[0].id] = self.pdeg(a.value, sc)

    def _infer_returns(self):
        for _ in range(3):
            for fname, f in self.funcs.items():
                sc = {a.arg: (1 if PRICE1.match(a.arg) else 0) for a in f.args.args}
                self._assigns(f, sc)
                ds = [self.pdeg(r.value, sc) for r in ast.walk(f)
                      if isinstance(r, ast.Return) and r.value is not None]
                ds = [d for d in ds if d is not None]
                self.retdeg[fname] = (ds[0] if ds and all(d == ds[0] for d in ds) else 0)

    def pdeg(self, n, sc, depth=0):
        """Homogeneity degree in the price scale.  Unknown symbols default to 0 (price-free
        unless proven price-borne): this makes the detector CONSERVATIVE — it can miss a cut
        whose key is built by an unresolvable helper, which is why bucket B2 is adjudicated."""
        if depth > 30:
            return 0
        D = lambda x: self.pdeg(x, sc, depth + 1)                          # noqa: E731
        if isinstance(n, ast.Constant):
            return 0
        if isinstance(n, ast.Name):
            if sc is not None and n.id in sc:
                v = sc[n.id]
                return 0 if v is None else v
            if n.id in self.consts:
                return 0
            return 1 if PRICE1.match(n.id) else 0
        if isinstance(n, ast.Attribute):
            if n.attr in FREE_DEG:
                return 0
            if n.attr in KEEP_DEG:
                return D(n.value)
            return 1 if PRICE1.match(n.attr) else 0
        if isinstance(n, ast.Call):
            f = n.func
            if isinstance(f, ast.Attribute):
                if f.attr in FREE_DEG:
                    return 0
                if f.attr in KEEP_DEG:
                    return D(f.value)
                return 0
            if isinstance(f, ast.Name):
                if f.id in {"abs", "float"} and n.args:
                    return D(n.args[0])
                if f.id in self.retdeg:
                    return self.retdeg[f.id] or 0
                return 0
            return 0
        if isinstance(n, ast.BinOp):
            a, b = D(n.left) or 0, D(n.right) or 0
            if isinstance(n.op, ast.Mult):
                return a + b
            if isinstance(n.op, ast.Div):
                return a - b
            if isinstance(n.op, (ast.Add, ast.Sub)):
                return a if a == b else max(a, b)
            if isinstance(n.op, ast.Pow):
                c = self.numconst(n.right, None)
                return a * list(c)[0] if (c and len(c) == 1) else a
            return a
        if isinstance(n, ast.Subscript):
            return D(n.value) or 0
        if isinstance(n, ast.UnaryOp):
            return D(n.operand) or 0
        if isinstance(n, ast.IfExp):
            a, b = D(n.body) or 0, D(n.orelse) or 0
            return a if a == b else max(a, b)
        return 0


def porigin(n, orig):
    """Price base symbols this expression is built from (syntactic + propagated)."""
    out = set()
    for a in ast.walk(n):
        if isinstance(a, ast.Name):
            if PRICE1.match(a.id):
                out.add(a.id)
            out |= orig.get(a.id, set())
        elif isinstance(a, ast.Attribute) and PRICE1.match(a.attr):
            out.add(a.attr)
    return out


def _maskish_context(src_line):
    """Is the flagged comparison wired into an ELIGIBILITY MASK, or into a value/report?"""
    s = src_line
    if re.search(r"\.mask\(|np\.where|\.astype\(float\)", s) and "&" not in s:
        return "TILT/STATE"
    if re.search(r"(^|[^A-Za-z_])(m|sel|mask|elig|live|univ|tradable)\s*&|&\s*\(", s) \
       or re.search(r"^\s*(return|.*=)\s*.*&", s):
        return "MASK"
    if MASKISH.search(s):
        return "MASK"
    return "OTHER"


def scan_file(path):
    src = path.read_text()
    try:
        tree = ast.parse(src)
    except Exception:
        return None, "PARSE_FAIL"
    lines = src.splitlines()
    M = Mod(tree)
    hits = []

    def run(node, sc, numsc, owner, orig):
        M._assigns(node, sc)
        for _ in range(3):
            for a in ast.walk(node):
                if isinstance(a, ast.Assign) and len(a.targets) == 1 \
                        and isinstance(a.targets[0], ast.Name):
                    o = porigin(a.value, orig)
                    if o:
                        orig[a.targets[0].id] = orig.get(a.targets[0].id, set()) | o
        for a in ast.walk(node):
            if not (isinstance(a, ast.Compare) and len(a.ops) == 1
                    and isinstance(a.ops[0], (ast.Gt, ast.GtE, ast.Lt, ast.LtE))):
                continue
            L, R = a.left, a.comparators[0]
            for side, other in ((L, R), (R, L)):
                d = M.pdeg(side, sc)
                if not d or d <= 0:
                    continue
                o = porigin(side, orig)
                if not o:
                    continue
                v = M.numconst(other, numsc)
                d_other = M.pdeg(other, sc)
                if d_other and d_other > 0:
                    bucket, levels = "B3", []                   # price vs price: covariant
                elif v is not None:
                    levels = sorted(v)
                    bucket = "Z" if all(x == 0 for x in levels) else "B1"
                else:
                    bucket, levels = "B2", []
                hits.append(dict(file=path.name, line=a.lineno, owner=owner, bucket=bucket,
                                 deg=d, levels=";".join(f"{x:g}" for x in levels),
                                 origin=",".join(sorted(o)),
                                 context=_maskish_context(lines[a.lineno - 1]),
                                 src=lines[a.lineno - 1].strip()[:170]))
                break
    root_sc, root_orig = {}, {}
    run(tree, root_sc, {}, "<module>", root_orig)
    for fname, f in M.funcs.items():
        sc = {a.arg: (1 if PRICE1.match(a.arg) else 0) for a in f.args.args}
        numsc = {p: v for p, v in M.callsites.get(fname, {}).items() if v is not None}
        for p in numsc:
            sc[p] = 0
        orig = dict(root_orig)
        for a in f.args.args:
            if PRICE1.match(a.arg):
                orig[a.arg] = {a.arg}
        run(f, sc, numsc, fname, orig)
    seen, out = set(), []
    for h in hits:
        if h["line"] in seen:
            continue
        seen.add(h["line"])
        out.append(h)
    return out, "OK"


# =====================================================================================
# engine helpers (idea 425 / the flagged file, verbatim)
# =====================================================================================
def fast_bt(px, w, freq=FREQ):
    idx = px.index
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mask)
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
    return (pd.Series((held * rets).sum(axis=1), index=idx),
            pd.Series(turn, index=idx),
            pd.Series(held.sum(axis=1), index=idx))


def net(gr, tn, bps):
    return gr - tn * bps / 1e4


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def mrow(r):
    m = metrics(r)
    h1, h2 = halves(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


def vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def trend(px, book):
    if book == "EWALL":
        return pd.DataFrame(True, index=px.index, columns=px.columns)
    if book == "MA200":
        return (px > px.rolling(200).mean()).fillna(False)
    raise ValueError(book)


def weights_ewall(px, selectable, g, conv, gross=GROSS):
    live = px.notna() & selectable
    sel = g & live
    num = sel.astype(float)
    den = (live.sum(axis=1) if conv == "dg" else sel.sum(axis=1)).replace(0, np.nan)
    return num.div(den, axis=0).mul(gross).fillna(0.0)


def build_panels():
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in pxs.columns if c == "SPY" or c not in bad]
    pxs = pxs[keep].dropna(how="all").ffill()
    small_tr = {c for c in pxs.columns if c != "SPY"}
    px56 = load_universe()
    tr56 = set(px56.columns)
    P(f"[panels] SMALL439 {len(small_tr)} tradable (+SPY benchmark), "
      f"{pxs.index[0].date()}..{pxs.index[-1].date()}  |  U56 {len(tr56)} tradable, "
      f"{px56.index[0].date()}..{px56.index[-1].date()}")
    return {"SMALL439": (pxs, small_tr), "U56": (px56, tr56)}


def base_mask(px, tradable):
    m = pd.DataFrame(False, index=px.index, columns=px.columns)
    for c in tradable:
        m[c] = True
    return m


# =====================================================================================
T0 = time.time()
P("=" * 118)
P("IDEA 428  census-the-record-s-other-DOLLAR-floors-and-caps   (lane C, 2026-09-08)")
P("=" * 118)

# ------------------------------------------------------------------ Q1 THE CENSUS
P("\n" + "-" * 118)
P("Q1  THE CENSUS — every committed .py under research/ , homogeneity-degree analysis")
P("-" * 118)
FILES = sorted(list((ROOT / "research" / "backtests").glob("*.py")) +
               list((ROOT / "research").glob("*.py")))
crows, n_fail = [], 0
for f in FILES:
    hs, status = scan_file(f)
    if status != "OK":
        n_fail += 1
        crows.append(dict(file=f.name, line=-1, owner="", bucket="PARSE_FAIL", deg=0, levels="",
                          origin="", context="", src=""))
        continue
    crows += hs
C = pd.DataFrame(crows)
C.to_csv(OUT / f"{STEM}.census.csv", index=False)
nb = C.bucket.value_counts()
P(f"  scripts scanned            : {len(FILES)}   (parse failures {n_fail}: "
  f"{', '.join(sorted(C[C.bucket == 'PARSE_FAIL'].file)) or 'none'})")
P(f"  price-bearing comparisons  : {int((C.bucket != 'PARSE_FAIL').sum())}")
for b, lab in (("B1", "ABSOLUTE cut, level resolved      <- the damaging form"),
               ("B2", "threshold unresolved              <- adjudicated below"),
               ("B3", "price vs price (scale-covariant)  <- safe"),
               ("Z", "absolute cut at level 0 (T1-inv.)  <- safe")):
    sub = C[C.bucket == b]
    P(f"    {b:<3} {lab:<52} {len(sub):>5} hits in {sub.file.nunique():>4} files")
B1 = C[C.bucket == "B1"]
P(f"\n  B1 — every absolute cut on a price-bearing quantity at a NON-ZERO level:")
P(f"  {'file':<52}{'line':>6}{'owner':>14}{'levels':>18}  {'context':<10} source")
for _, r in B1.sort_values(["file", "line"]).iterrows():
    P(f"  {r.file[:50]:<52}{r.line:>6}{r.owner[:13]:>14}{r.levels[:17]:>18}  "
      f"{r.context:<10} {r.src[:60]}")
B2 = C[C.bucket == "B2"]
P(f"\n  B2 — {len(B2)} hits the analyser could not resolve to a constant, printed in full so the "
  f"census has no hidden tail:")
P(f"  {'file':<52}{'line':>6}  {'context':<11} source")
for _, r in B2.sort_values(["file", "line"]).iterrows():
    P(f"  {r.file[:50]:<52}{r.line:>6}  {r.context:<11} {r.src[:66]}")

# ---- Q1b: adjudication of every B1 and B2 hit ---------------------------------------
P("\n" + "-" * 118)
P("Q1b ADJUDICATION — every B1 and B2 hit read and classified.  A hit is DAMAGING only if the")
P("    compared quantity is price-borne AND the threshold is a fixed number in price units.")
P("-" * 118)
ADJ_RULES = [
    ("DV_FLOOR", r"dv\s*>=|\(px\s*\*\s*vol\)", "DAMAGING",
     "absolute $ floor on (px*vol) inside an eligibility mask — idea 121/425's construction"),
    ("RATIO_TOL", r"(med|ratio)\b.*1e-0?9|1e-0?9", "SAFE",
     "tolerance on a price/price RATIO (degree 0); analyser lost the cancellation"),
    ("TRAIL_STOP", r"peak|npeak|\bpk\b", "SAFE",
     "trailing stop: price vs a running peak of the same price — covariant under T1"),
    ("MOVING_AVG", r"\bma\b|ma200|\.ma\b|\bma\s*\*", "SAFE",
     "price vs its own moving average — covariant under T1"),
    ("BLOCK_REF", r"block_ref", "SAFE",
     "price vs a stored price reference — covariant under T1"),
    ("OPT_MODEL", r"bs_price|bs_put", "SAFE",
     "option price vs a model price in the same units — covariant under T1"),
    ("NOT_PRICE", r"Sharpe|beats_|OOS_", "SAFE",
     "not a price at all: the origin tag is a propagation false positive"),
]
adj = []
for _, r in pd.concat([B1, B2]).sort_values(["file", "line"]).iterrows():
    tag, verdict, why = "UNADJUDICATED", "UNKNOWN", ""
    for name, pat, v, w in ADJ_RULES:
        if re.search(pat, r.src):
            tag, verdict, why = name, v, w
            break
    adj.append(dict(file=r.file, line=r.line, bucket=r.bucket, context=r.context, rule=tag,
                    verdict=verdict, why=why, src=r.src))
ADJ = pd.DataFrame(adj)
C = C.merge(ADJ[["file", "line", "rule", "verdict"]], on=["file", "line"], how="left")
C.to_csv(OUT / f"{STEM}.census.csv", index=False)
P(f"  {'rule':<12}{'verdict':<11}{'hits':>6}{'files':>7}   why")
for name, pat, v, w in ADJ_RULES:
    sub = ADJ[ADJ.rule == name]
    if len(sub):
        P(f"  {name:<12}{v:<11}{len(sub):>6}{sub.file.nunique():>7}   {w}")
unadj = ADJ[ADJ.verdict == "UNKNOWN"]
P(f"  {'UNADJUDIC.':<12}{'UNKNOWN':<11}{len(unadj):>6}{unadj.file.nunique():>7}   "
  f"{'(none)' if not len(unadj) else 'printed below'}")
for _, r in unadj.iterrows():
    P(f"      {r.file[:56]:<58}{r.line:>6}  {r.src[:60]}")
DAM = ADJ[ADJ.verdict == "DAMAGING"]
P(f"\n  -> DAMAGING form found in {DAM.file.nunique()} of {len(FILES)} committed scripts "
  f"({DAM.file.nunique() / len(FILES):.2%}), {len(DAM)} occurrences:")
for _, r in DAM.iterrows():
    P(f"     {r.file:<62} line {r.line:<6} {r.context}")

# ------------------------------------------------------------------ Q2 exposure
P("\n" + "-" * 118)
P("Q2  EXPOSURE — how many LEADERBOARD rows sit under each flagged file")
P("-" * 118)
LB = (ROOT / "research" / "LEADERBOARD.md").read_text()
lb_rows = [ln for ln in LB.splitlines() if ln.startswith("|") and ln.count("|") >= 9]
exposure = {}
for f in sorted(set(B1.file) | set(B2.file)):
    stem = f[:-3]
    exposure[f] = sum(1 for ln in lb_rows if stem in ln)
P(f"  LEADERBOARD rows parsed: {len(lb_rows)}")
P(f"  {'file':<58}{'bucket':>8}{'adjudged':>10}{'LB rows':>9}")
for f, k in sorted(exposure.items(), key=lambda x: -x[1]):
    b = "B1" if f in set(B1.file) else "B2"
    v = "DAMAGING" if f in set(DAM.file) else "safe"
    P(f"  {f[:56]:<58}{b:>8}{v:>10}{k:>9}")
dam_rows = sum(v for f, v in exposure.items() if f in set(DAM.file))
P(f"\n  RE-RUN BACKLOG from this class: {dam_rows} LEADERBOARD rows, all in "
  f"{DAM.file.nunique()} file(s) — {', '.join(sorted(DAM.file))}")

# ------------------------------------------------------------------ panels + keys
P("\n" + "-" * 118)
P("Q3  THE KEYS — common support, admission ladders, matched-admission calibration")
P("-" * 118)
PANELS = build_panels()
START = {k: v[0].index[260] for k, v in PANELS.items()}
pxS, trS = PANELS["SMALL439"]
px56, tr56 = PANELS["U56"]
sS, s56 = START["SMALL439"], START["U56"]


def keys_for(pname):
    px, tr = PANELS[pname]
    out = {"PXL": px.rolling(20).median()}
    if pname == "SMALL439":
        vol = load_volume(small=True).reindex(index=px.index).reindex(columns=px.columns)
        out["DV"] = (px * vol).rolling(20).median()
        out["VOLSH"] = vol.rolling(20).median()
    return out


KEYS, SUPPORT = {}, {}
for pname in PANELS:
    px, tr = PANELS[pname]
    K = keys_for(pname)
    KEYS[pname] = K
    live = px.notna() & base_mask(px, tr)
    S = live.copy()
    for k in K.values():
        S &= k.notna()
    S = S.loc[START[pname]:]
    SUPPORT[pname] = S
    lv = live.loc[START[pname]:]
    P(f"  [{pname}] live ticker-days {int(lv.values.sum()):>9,}   common support S "
      f"{int(S.values.sum()):>9,} ({S.values.sum() / max(lv.values.sum(), 1):.3%} of live); "
      f"keys {sorted(K)}")


def pooled(pname, key):
    k = KEYS[pname][key].loc[START[pname]:]
    S = SUPPORT[pname]
    return np.sort(k.values[S.values])


POOL = {(p, k): pooled(p, k) for p in PANELS for k in KEYS[p]}


def admit_share(pname, key, level):
    """Share of the common support ADMITTED by `key >= level`."""
    v = POOL[(pname, key)]
    return float((v >= level).mean())


def level_for_share(pname, key, share):
    """Solve level so that `key >= level` admits exactly `share` of the common support."""
    v = POOL[(pname, key)]
    if share >= 1.0:
        return float(v[0]) - 1.0
    i = int(np.floor((1.0 - share) * len(v)))
    i = min(max(i, 0), len(v) - 1)
    return float(v[i])


P("\n  Matched-admission ladder on SMALL439 (levels SOLVED from the pooled-quantile identity;")
P("  the two tuned parameters are the INSTRUMENT and the LEVEL, and every rung is reported):")
P(f"  {'DV level':>12}{'admit share':>13}{'gated share':>13}"
  f"{'VOLSH level (sh)':>19}{'PXL level ($)':>15}{'admit chk':>11}")
LADDER = []
for L in DV_LEVELS:
    sh = admit_share("SMALL439", "DV", L)
    vsl = level_for_share("SMALL439", "VOLSH", sh)
    pxl = level_for_share("SMALL439", "PXL", sh)
    chk = (admit_share("SMALL439", "VOLSH", vsl), admit_share("SMALL439", "PXL", pxl))
    LADDER.append(dict(panel="SMALL439", dv_level=L, admit_share=sh, gated_share=1 - sh,
                       volsh_level=vsl, pxl_level=pxl,
                       volsh_admit=chk[0], pxl_admit=chk[1]))
    P(f"  {L / 1e6:>10.2f}M{sh:>13.4%}{1 - sh:>13.4%}{vsl:>19,.0f}{pxl:>15.2f}"
      f"{max(abs(chk[0] - sh), abs(chk[1] - sh)):>11.1e}")
# U56: PXL only (no volume cache); anchor its ladder on the same admitted shares
for L in DV_LEVELS:
    sh = LADDER[DV_LEVELS.index(L)]["admit_share"]
    pxl = level_for_share("U56", "PXL", sh)
    LADDER.append(dict(panel="U56", dv_level=np.nan, admit_share=sh, gated_share=1 - sh,
                       volsh_level=np.nan, pxl_level=pxl, volsh_admit=np.nan,
                       pxl_admit=admit_share("U56", "PXL", pxl)))
LAD = pd.DataFrame(LADDER)
LAD.to_csv(OUT / f"{STEM}.ladder.csv", index=False)

# ---- P1: the ranking the QUEUE asked for -------------------------------------------
P("\n  P1 RANKING — admission-rate share GATED by each cut, at the levels the record uses:")
P(f"  {'construction':<44}{'panel':>10}{'level':>16}{'gated share of live ticker-days':>34}")
GATING = []
for pname in PANELS:
    live = (PANELS[pname][0].notna() & base_mask(*PANELS[pname])).loc[START[pname]:]
    nlive = float(live.values.sum())
    for key in KEYS[pname]:
        lv = ([1.0e6] if key == "DV" else
              [PX_REF_LEVEL] if key == "PXL" else
              [level_for_share(pname, "VOLSH", admit_share(pname, "DV", 1.0e6))])
        for L in lv:
            k = KEYS[pname][key].loc[START[pname]:]
            adm = (k >= L).fillna(False) & live
            gated = 1.0 - float(adm.values.sum()) / nlive
            lab = {"DV": "(px*vol).rolling(20).median() >= $1M",
                   "VOLSH": "vol.rolling(20).median() >= s*  (price-free)",
                   "PXL": f"px.rolling(20).median() >= ${PX_REF_LEVEL:g}"}[key]
            GATING.append(dict(panel=pname, key=key, level=L, gated_share=gated,
                               construction=lab))
            P(f"  {lab:<44}{pname:>10}{L:>16,.2f}{gated:>34.4%}")
GT = pd.DataFrame(GATING).sort_values("gated_share", ascending=False)
GT.to_csv(OUT / f"{STEM}.gating.csv", index=False)
P(f"\n  P1 verdict: highest gated share is "
  f"{GT.iloc[0].construction} on {GT.iloc[0].panel} at {GT.iloc[0].gated_share:.4%}; "
  f"the $1M DV floor gates "
  f"{float(GT[(GT.key == 'DV')].gated_share.iloc[0]):.4%} vs the ${PX_REF_LEVEL:g} price floor's "
  f"{float(GT[(GT.key == 'PXL') & (GT.panel == 'SMALL439')].gated_share.iloc[0]):.4%} "
  f"on SMALL439.")

# ------------------------------------------------------------------ masks
MASKS = {}
for pname in PANELS:
    px, tr = PANELS[pname]
    S_full = base_mask(px, tr) & px.notna()
    for k in KEYS[pname].values():
        S_full &= k.notna()
    d = {"NONE": S_full}
    for i, L in enumerate(DV_LEVELS):
        if L == 0.0:
            continue
        sh = LADDER[i]["admit_share"]
        tag = f"{L / 1e6:g}M"
        if pname == "SMALL439":
            d[f"DV_{tag}"] = S_full & (KEYS[pname]["DV"] >= L).fillna(False)
            d[f"VOLSH_{tag}"] = S_full & (KEYS[pname]["VOLSH"] >=
                                          level_for_share(pname, "VOLSH", sh)).fillna(False)
        d[f"PXL_{tag}"] = S_full & (KEYS[pname]["PXL"] >=
                                    level_for_share(pname, "PXL", sh)).fillna(False)
    MASKS[pname] = d

# ------------------------------------------------------------------ reproduction gates
P("\n" + "-" * 118)
P("Q4  REPRODUCTION GATES (bind before any new number is read)")
P("-" * 118)
w_probe = weights_ewall(pxS, MASKS["SMALL439"]["NONE"], trend(pxS, "MA200"), "dg")
r_eng = backtest(pxS, w_probe, cost_bps=10.0, freq=FREQ)["returns"]
g_, t_, _ = fast_bt(pxS, w_probe)
P(f"  [a] fast_bt vs engine.backtest        max|diff| = "
  f"{np.abs(r_eng - net(g_, t_, 10)).max():.3e}")
spyS = pxS["SPY"].pct_change().fillna(0).loc[sS:]
mS = mrow(spyS)
P(f"  [b] SPY on the SMALL439 window: {mS['CAGR']:.2%}/{mS['Sharpe']:.3f}/{mS['MaxDD']:.1%} "
  f"halves {mS['H1']:.3f}/{mS['H2']:.3f}   [idea 425 published 14.13%/0.862/-33.7%, 0.891/0.858]")
spy56 = px56["SPY"].pct_change().fillna(0).loc[s56:]
m56 = mrow(spy56)
P(f"  [c] SPY on the U56 window:      {m56['CAGR']:.2%}/{m56['Sharpe']:.3f}/{m56['MaxDD']:.1%} "
  f"halves {m56['H1']:.3f}/{m56['H2']:.3f}")
gv2, tv2, _ = fast_bt(px56, rules_v2_weights(px56))
v2_full = net(gv2, tv2, PROTO_COST)
mv2 = mrow(v2_full.loc[s56:])
P(f"  [d] LIVE RULES v2 on U56 @10bps: {mv2['CAGR']:.2%}/{mv2['Sharpe']:.4f}/{mv2['MaxDD']:.2%}"
  f"   [published 8.66%/1.2056/-12.05%]")
wv1 = rules_v1_weights(pxS.drop(columns=["SPY"])).reindex(columns=pxS.columns).fillna(0.0)
gv1, tv1, _ = fast_bt(pxS, wv1)
mv1 = mrow(net(gv1, tv1, 10).loc[sS:])
P(f"  [e] LIVE RULES v1 on SMALL439 @10bps: {mv1['CAGR']:.2%}/{mv1['Sharpe']:.3f}/"
  f"{mv1['MaxDD']:.1%}   [idea 425 published 8.15%/0.603/-32.8%]")
dvm = MASKS["SMALL439"].get("DV_1M")
P(f"  [f] the flagged construction, rebuilt here: DV $1M admits "
  f"{int((dvm & SUPPORT['SMALL439']).loc[sS:].values.sum()):,} of "
  f"{int(SUPPORT['SMALL439'].values.sum()):,} support ticker-days "
  f"({(dvm & SUPPORT['SMALL439']).loc[sS:].values.sum() / SUPPORT['SMALL439'].values.sum():.4%})")

# ------------------------------------------------------------------ Q5 the grid
P("\n" + "-" * 118)
P("Q5  MAIN GRID — every panel x instrument x level x book x convention x cost rung, all reported")
P("-" * 118)
rows, RET = [], {}
for pname, (px, tr) in PANELS.items():
    st = START[pname]
    for mname, mask in MASKS[pname].items():
        for book in BOOKS:
            g = trend(px, book)
            for conv in CONVS:
                gr, tn, expo = fast_bt(px, weights_ewall(px, mask, g, conv))
                for bps in COSTS:
                    r = net(gr.loc[st:], tn.loc[st:], bps)
                    m = mrow(r)
                    RET[(pname, mname, book, conv, bps)] = r
                    inst = mname.split("_")[0]
                    rows.append(dict(panel=pname, inst=inst, mask=mname, book=book, conv=conv,
                                     bps=bps, CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                                     MaxDD=m["MaxDD"], H1=m["H1"], H2=m["H2"],
                                     turn_yr=float(tn.loc[st:].sum() / (len(r) / 252.0)),
                                     mean_names=float((mask.loc[st:] & (g.loc[st:]) &
                                                       px.loc[st:].notna()).sum(axis=1).mean()),
                                     mean_expo=float(expo.loc[st:].mean())))
G = pd.DataFrame(rows)
G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
P(f"  grid points: {len(G)}  ({G.panel.nunique()} panels x masks x {len(BOOKS)} books x "
  f"{len(CONVS)} conventions x {len(COSTS)} cost rungs)")
P(f"\n  SMALL439 @ {PROTO_COST} bps, by instrument and level (mean over books x conventions):")
P(f"  {'mask':<12}{'admit share':>13}{'CAGR':>9}{'Sharpe':>9}{'MaxDD':>9}{'H1':>8}{'H2':>8}"
  f"{'names/day':>11}")
gs = G[(G.panel == "SMALL439") & (G.bps == PROTO_COST)].groupby("mask", sort=False)
for mname, sub in gs:
    adm = float((MASKS["SMALL439"][mname] & SUPPORT["SMALL439"]).loc[sS:].values.sum()
                / SUPPORT["SMALL439"].values.sum())
    P(f"  {mname:<12}{adm:>13.4%}{sub.CAGR.mean():>9.2%}{sub.Sharpe.mean():>9.3f}"
      f"{sub.MaxDD.mean():>9.1%}{sub.H1.mean():>8.3f}{sub.H2.mean():>8.3f}"
      f"{sub.mean_names.mean():>11.1f}")

# ---- P2: the matched-admission contrast, cell by cell -------------------------------
P("\n  P2  MATCHED-ADMISSION CONTRAST on SMALL439 — same admitted COUNT, three different keys.")
P("  Every (level, book, conv, bps) cell is a paired comparison; all cells reported.")
P(f"  {'level':>8}  {'pair':<16}{'cells':>7}{'key1 wins':>11}{'dCAGR pp':>11}{'dSharpe':>11}"
  f"{'dMaxDD pp':>11}")
P2ROWS = []
for L in DV_LEVELS:
    if L == 0.0:
        continue
    tag = f"{L / 1e6:g}M"
    for a, b in (("VOLSH", "DV"), ("VOLSH", "PXL"), ("DV", "PXL")):
        d = []
        for book in BOOKS:
            for conv in CONVS:
                for bps in COSTS:
                    ra = RET[("SMALL439", f"{a}_{tag}", book, conv, bps)]
                    rb = RET[("SMALL439", f"{b}_{tag}", book, conv, bps)]
                    ma, mb = mrow(ra), mrow(rb)
                    d.append((ma["CAGR"] - mb["CAGR"], ma["Sharpe"] - mb["Sharpe"],
                              ma["MaxDD"] - mb["MaxDD"]))
        d = np.array(d)
        P2ROWS.append(dict(level=L, pair=f"{a}-{b}", cells=len(d),
                           wins=int((d[:, 0] > 0).sum()), dCAGR=d[:, 0].mean(),
                           dSharpe=d[:, 1].mean(), dMaxDD=d[:, 2].mean()))
        P(f"  {L / 1e6:>7.2f}M  {a + ' - ' + b:<16}{len(d):>7}{int((d[:, 0] > 0).sum()):>11}"
          f"{100 * d[:, 0].mean():>11.3f}{d[:, 1].mean():>11.4f}{100 * d[:, 2].mean():>11.3f}")
P2 = pd.DataFrame(P2ROWS)

# ------------------------------------------------------------------ Q6 rule 8
P("\n" + "-" * 118)
P("Q6  RULE 8 WALK-FORWARD — the LEVEL chosen on 2010..2016 only, 2017..2026 read once")
P("-" * 118)
spy_oos = {p: metrics(PANELS[p][0]["SPY"].pct_change().fillna(0).loc[START[p]:]
                      .loc[OOS_START:]) for p in PANELS}
spy_oos_cagr = {p: metrics(PANELS[p][0]["SPY"].pct_change().fillna(0).loc[START[p]:]
                           .loc[OOS_START:])["CAGR"] for p in PANELS}
wfrows = []
for pname in PANELS:
    insts = sorted({m.split("_")[0] for m in MASKS[pname] if m != "NONE"})
    for inst in insts:
        cands = [m for m in MASKS[pname] if m.split("_")[0] == inst]
        for book in BOOKS:
            for conv in CONVS:
                for bps in COSTS:
                    isS = {m: metrics(RET[(pname, m, book, conv, bps)].loc[:IS_END])["Sharpe"]
                           for m in cands}
                    pick = max(isS, key=lambda m: isS[m])
                    ro = RET[(pname, pick, book, conv, bps)].loc[OOS_START:]
                    mo = metrics(ro)
                    nf = RET[(pname, "NONE", book, conv, bps)].loc[OOS_START:]
                    mnf = metrics(nf)
                    best = max(cands, key=lambda m:
                               metrics(RET[(pname, m, book, conv, bps)].loc[OOS_START:])["Sharpe"])
                    wfrows.append(dict(
                        panel=pname, inst=inst, book=book, conv=conv, bps=bps, pick=pick,
                        IS_Sharpe=isS[pick], OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"],
                        OOS_MaxDD=mo["MaxDD"], nofloor_OOS_Sharpe=mnf["Sharpe"],
                        nofloor_OOS_CAGR=mnf["CAGR"], nofloor_OOS_MaxDD=mnf["MaxDD"],
                        oracle_OOS_Sharpe=metrics(RET[(pname, best, book, conv, bps)]
                                                  .loc[OOS_START:])["Sharpe"],
                        spy_OOS_Sharpe=spy_oos[pname]["Sharpe"],
                        spy_OOS_CAGR=spy_oos_cagr[pname]))
WF = pd.DataFrame(wfrows)
WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
P(f"  cells: {len(WF)}   (panel x instrument x book x convention x cost rung)")
P(f"  {'panel':<10}{'inst':<7}{'cells':>7}{'beats no-floor OOS':>20}{'beats SPY OOS':>15}"
  f"{'mean OOS Sh':>13}{'no-floor':>10}{'SPY':>8}{'oracle':>9}")
for (pname, inst), sub in WF.groupby(["panel", "inst"]):
    P(f"  {pname:<10}{inst:<7}{len(sub):>7}"
      f"{int((sub.OOS_Sharpe > sub.nofloor_OOS_Sharpe).sum()):>13}/{len(sub):<6}"
      f"{int((sub.OOS_Sharpe > sub.spy_OOS_Sharpe).sum()):>8}/{len(sub):<6}"
      f"{sub.OOS_Sharpe.mean():>13.3f}{sub.nofloor_OOS_Sharpe.mean():>10.3f}"
      f"{sub.spy_OOS_Sharpe.mean():>8.3f}{sub.oracle_OOS_Sharpe.mean():>9.3f}")
P(f"\n  mean OOS CAGR: pick {WF.OOS_CAGR.mean():.2%}  no-floor {WF.nofloor_OOS_CAGR.mean():.2%}  "
  f"SPY(SMALL window) {spy_oos_cagr['SMALL439']:.2%} / SPY(U56 window) "
  f"{spy_oos_cagr['U56']:.2%}")
P(f"  mean OOS MaxDD: pick {WF.OOS_MaxDD.mean():.1%}  no-floor {WF.nofloor_OOS_MaxDD.mean():.1%}")
P(f"  IS chooser beats the no-floor control on OOS Sharpe in "
  f"{int((WF.OOS_Sharpe > WF.nofloor_OOS_Sharpe).sum())}/{len(WF)} cells; "
  f"picks the OOS-best level in "
  f"{int(np.isclose(WF.OOS_Sharpe, WF.oracle_OOS_Sharpe).sum())}/{len(WF)}.")

# ------------------------------------------------------------------ Q7 both KEEP paths
P("\n" + "-" * 118)
P("Q7  BOTH KEEP PATHS at 10 bps  (4a vs live RULES v2 cost-matched; 4b vs SPY + rule 8)")
P("-" * 118)
mv2_10 = mrow(v2_full.loc[s56:])


def path_verdicts(pname, r_full):
    m = mrow(r_full)
    sp = PANELS[pname][0]["SPY"].pct_change().fillna(0).loc[START[pname]:]
    ms = mrow(sp)
    bad_a = []
    if m["H1"] <= mv2_10["H1"]:
        bad_a.append("H1")
    if m["H2"] <= mv2_10["H2"]:
        bad_a.append("H2")
    if m["MaxDD"] < mv2_10["MaxDD"]:
        bad_a.append("DD")
    bad_b = []
    if m["H1"] <= ms["H1"]:
        bad_b.append("H1")
    if m["H2"] <= ms["H2"]:
        bad_b.append("H2")
    if metrics(r_full.loc[OOS_START:])["Sharpe"] <= metrics(sp.loc[OOS_START:])["Sharpe"]:
        bad_b.append("OOS")
    if m["MaxDD"] < 0.60 * ms["MaxDD"]:
        bad_b.append("DD")
    if m["CAGR"] < 0.70 * ms["CAGR"]:
        bad_b.append("CAGR")
    return bad_a, bad_b


vrows = []
for pname in PANELS:
    for mname in MASKS[pname]:
        for book in BOOKS:
            for conv in CONVS:
                r = RET[(pname, mname, book, conv, PROTO_COST)]
                ba, bb = path_verdicts(pname, r)
                m = mrow(r)
                vrows.append(dict(panel=pname, mask=mname, inst=mname.split("_")[0], book=book,
                                  conv=conv, CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                                  MaxDD=m["MaxDD"], H1=m["H1"], H2=m["H2"],
                                  path4a="KEEP" if not ba else "KILL(" + ",".join(ba) + ")",
                                  path4b="KEEP" if not bb else "KILL(" + ",".join(bb) + ")"))
V = pd.DataFrame(vrows)
V.to_csv(OUT / f"{STEM}.verdicts.csv", index=False)
for pname in PANELS:
    sp = mrow(PANELS[pname][0]["SPY"].pct_change().fillna(0).loc[START[pname]:])
    P(f"  4b bars ({pname} window, SPY): H1 > {sp['H1']:.3f}, H2 > {sp['H2']:.3f}, "
      f"OOS Sharpe > {spy_oos[pname]['Sharpe']:.3f}, MaxDD >= {0.60 * sp['MaxDD']:.1%}, "
      f"CAGR >= {0.70 * sp['CAGR']:.2%}")
P(f"  4a bars (RULES v2 @10bps): H1 > {mv2_10['H1']:.3f}, H2 > {mv2_10['H2']:.3f}, "
  f"MaxDD >= {mv2_10['MaxDD']:.2%}")
P(f"\n  {'panel':<10}{'inst':<7}{'points':>8}{'4a KEEP':>10}{'4b KEEP':>10}   binding bars (4b)")
for (pname, inst), sub in V.groupby(["panel", "inst"]):
    fails = pd.Series([x for s in sub.path4b for x in
                       (s[5:-1].split(",") if s.startswith("KILL") else [])]).value_counts()
    P(f"  {pname:<10}{inst:<7}{len(sub):>8}{int((sub.path4a == 'KEEP').sum()):>10}"
      f"{int((sub.path4b == 'KEEP').sum()):>10}   "
      f"{', '.join(f'{k} {v}' for k, v in fails.items())}")
P(f"\n  TOTAL: 4a KEEP {int((V.path4a == 'KEEP').sum())}/{len(V)};  "
  f"4b KEEP {int((V.path4b == 'KEEP').sum())}/{len(V)}")
if (V.path4b == "KEEP").any():
    P("  4b passes at 10 bps, re-priced at every cost rung (a pass that dies on the ladder is a")
    P("  dial placement, not a book):")
    for _, r in V[V.path4b == "KEEP"].iterrows():
        P(f"    {r.panel}/{r['mask']}/{r.book}/{r.conv}: {r.CAGR:.2%}/{r.Sharpe:.3f}/"
          f"{r.MaxDD:.1%}  H {r.H1:.3f}/{r.H2:.3f}")
        for bps in COSTS:
            rr = RET[(r.panel, r["mask"], r.book, r.conv, bps)]
            ba, bb = path_verdicts(r.panel, rr)
            m = mrow(rr)
            P(f"        {bps:>3} bps: {m['CAGR']:>7.2%}/{m['Sharpe']:>6.3f}/{m['MaxDD']:>7.1%}  "
              f"4b {'KEEP' if not bb else 'KILL(' + ','.join(bb) + ')'}")

# ------------------------------------------------------------------ verdict
P("\n" + "=" * 118)
P("VERDICT")
P("=" * 118)
P(f"  Q1  {len(FILES)} committed scripts scanned, {int((C.bucket != 'PARSE_FAIL').sum())} "
  f"price-bearing comparisons; after adjudicating every B1+B2 hit ({len(ADJ)}), the damaging "
  f"form")
P(f"      (absolute cut on a price-borne quantity in an eligibility mask) appears {len(DAM)} "
  f"times in {DAM.file.nunique()} of {len(FILES)} files; {len(unadj)} hits unadjudicated.")
P(f"  Q2  LEADERBOARD exposure: {sum(exposure.values())} rows under all flagged files, "
  f"{dam_rows} under the DAMAGING ones.")
dv_g = float(GT[(GT.key == 'DV')].gated_share.iloc[0])
px_g = float(GT[(GT.key == 'PXL') & (GT.panel == 'SMALL439')].gated_share.iloc[0])
P(f"  P1  {'CONFIRMED' if dv_g > px_g else 'FALSIFIED'}: $1M DV gates {dv_g:.4%} of SMALL439 "
  f"live ticker-days vs the ${PX_REF_LEVEL:g} price floor's {px_g:.4%}.")
vd = P2[P2.pair == "VOLSH-DV"]
vp = P2[P2.pair == "VOLSH-PXL"]
P(f"  P2  VOLSH-DV mean dCAGR {100 * vd.dCAGR.mean():+.3f} pp "
  f"({int(vd.wins.sum())}/{int(vd.cells.sum())} cells positive); "
  f"VOLSH-PXL {100 * vp.dCAGR.mean():+.3f} pp "
  f"({int(vp.wins.sum())}/{int(vp.cells.sum())}).")
P(f"      {'CONFIRMED' if (vd.dCAGR.mean() > 0 and vp.dCAGR.mean() > 0) else 'SPLIT/FALSIFIED'}: "
  f"the price-free key is on the same side of BOTH price-bearing keys."
  if (vd.dCAGR.mean() > 0) == (vp.dCAGR.mean() > 0) else
  "      FALSIFIED: the two price-bearing keys sit on OPPOSITE sides of the price-free key.")
P(f"  P3  4b KEEP {int((V.path4b == 'KEEP').sum())}/{len(V)}; rule-8 picks beat SPY OOS in "
  f"{int((WF.OOS_Sharpe > WF.spy_OOS_Sharpe).sum())}/{len(WF)} cells.")
P(f"\n  runtime {time.time() - T0:.1f}s")
(OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")

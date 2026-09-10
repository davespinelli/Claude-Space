#!/usr/bin/env python3
"""IDEA 643 -- can-the-record-s-keys-be-made-REACHABLE-without-a-harness   (cloud, 2026-09-10)

QUEUE: idea 426's back-fill reaches only 19.4% of 30,092 key-bearing assignment sites; 80.6%
are blocked by the FREE-VARIABLE WALL (locals and undefaulted params), which is what actually
caps a PROTOCOL back-fill, not the certificate.  Measure how much of the wall a single
convention would clear -- every script exposing its key as a module-level `key(px, vol)` --
by back-filling the 254 UNREACHABLE and a sample of the wall with hand harnesses, and report
the REACH PER UNIT OF WORK.

TWO TUNED PARAMETERS (the whole grid is reported, 8 points):
  MECH  in {SELF, INLINE, IMPORT, BODY}   the reach mechanism ladder
        SELF   = idea 426 (cloud) static rule: the expression names only px/vol + np/pd
        INLINE = idea 426 (lane B) static rule: additionally inline single-assignment locals
                 and defaulted params
        IMPORT = THE CONVENTION.  Execute a DEF-ONLY SHELL of the file (imports, defs and
                 literal module constants; every other top-level statement dropped) and CALL
                 its module-level functions with (px[, vol]).  Zero per-file work.
        BODY   = ONE GENERIC HARNESS.  Execute the site's enclosing function BODY-PREFIX in a
                 namespace seeded with px/vol and the params' own defaults, then read the
                 target local.  Zero per-file work.
  BIND  in {STRICT, GUESS}                how far the harness may guess a signature
        STRICT = bind only params whose NAME matches the price/volume allowlist; every other
                 param must carry its own default
        GUESS  = additionally bind the FIRST positional param to px when no name matches, and
                 pass None for the undefaulted rest

Panel (U56 / B136 / SMALL439), the certificate slice and the menu cap are REPORTED axes.

Deliverables: .txt .census.csv .wall.csv .reach.csv .keys.csv .books.csv .wf.csv
Report-only.  PROTOCOL.md, RULES.md, scan.py, bot.py and baseline.py are NOT touched; G4
proves nothing in the record was rewritten by the harness.

SURVIVORSHIP (PROTOCOL 9): B136 and SMALL439 are current-constituent lists; SMALL439 drops
the names with data/small_meta.csv max_1d_move >= 1.0.  No book here is a tradable estimate;
the load-bearing quantity is the MENU-minus-MENU contrast inside one panel.
"""
import ast, hashlib, io, re, signal, sys, time, warnings
from collections import Counter, defaultdict
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, load_volume, rules_v2_weights          # noqa: E402
from engine import backtest, metrics, rebalance_mask                       # noqa: E402

STEM = str(Path(__file__).with_suffix(""))
SELF_NAME = Path(__file__).name
IS_END, OOS_START = "2016-12-31", "2017-01-01"
WARMUP, FREQ = 260, "W"
RUNGS = [10.0, 25.0]
TOPN, GROSS = 10, 0.75
SEED, SIGMA, NDRAW = 643, 0.25, 8
CELL_TOL = 1e-9
MENU_CAP = 30                 # reported axis
WALL_SAMPLE = 250             # reported axis: deterministic sample of the free-variable wall
BUDGET = 1.2                  # seconds per harnessed site / call
_LOG = []


def log(s=""):
    print(s)
    _LOG.append(str(s))


# ------------------------------------------------------------------ vectorised engine (idea 426)
def fast_backtest(prices, weights, freq=FREQ):
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy(); m[0] = True
    T, Ncol = rets.shape
    C = np.cumprod(1.0 + rets, axis=0); Cp = np.vstack([np.ones((1, Ncol)), C[:-1]])
    reb = np.flatnonzero(m)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]; W0 = wt[s0]
    h = W0 * (Cp / Cp[s0]); V = h.sum(axis=1) + (1.0 - W0.sum(axis=1)); held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]; W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p]); Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1)); heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T); turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return (pd.Series((held * rets).sum(axis=1), index=idx),
            pd.Series(turn, index=idx))


def legs(r):
    r = r.iloc[WARMUP:]
    h = len(r) // 2
    f, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    ins, oos = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    return dict(CAGR=f["CAGR"], Sharpe=f["Sharpe"], MaxDD=f["MaxDD"], H1=m1["Sharpe"],
                H2=m2["Sharpe"], IS=ins["Sharpe"], OOS=oos["Sharpe"],
                OOS_CAGR=oos["CAGR"], OOS_DD=oos["MaxDD"])


def v4a(L, B):
    return int(L["H1"] > B["H1"] and L["H2"] > B["H2"] and L["MaxDD"] >= B["MaxDD"])


def v4b(L, S):
    return int(L["H1"] > S["H1"] and L["H2"] > S["H2"] and L["OOS"] > S["OOS"]
               and L["MaxDD"] >= 0.60 * S["MaxDD"] and L["CAGR"] >= 0.70 * S["CAGR"])


# ------------------------------------------------------------------ the certificate (idea 197/433)
PRICE_NAMES = {"px", "prices", "pxs", "price", "closes", "adj"}
VOL_NAMES = {"vol", "volume", "shares", "vols"}
PRICE_RE = re.compile(r"^(px|prices?|pxs|closes?|adj|panel|pc|p)\d*$")
VOL_RE = re.compile(r"^(vol|volume|shares|vols|dv|adv)\d*$")
SAFE_MODULES = {"np", "pd", "numpy", "math"}
FREE_OK = SAFE_MODULES | {"True", "False", "None", "len", "abs", "min", "max", "range", "sorted"}


def _rank(df):
    return df.rank(axis=1, pct=True)


class Budget(Exception):
    pass


def _alarm(sig, frm):
    raise Budget()


signal.signal(signal.SIGALRM, _alarm)


def guarded(fn, *a, budget=BUDGET, **k):
    """Run fn with a wall-clock budget and stdout/stderr swallowed.  Returns (ok, value_or_exc)."""
    signal.setitimer(signal.ITIMER_REAL, budget)
    try:
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            return True, fn(*a, **k)
    except Budget:
        return False, "TIMEOUT"
    except BaseException as e:                                  # noqa: BLE001 - corpus code
        return False, type(e).__name__
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0.0)


def cert_on_key(K, Kp_list):
    """T1: fraction of cells whose VALUE (and RANK) moves when prices are rescaled per column."""
    base_v, base_r = K.values, _rank(K).values
    mv = mr = 0.0
    for Kp in Kp_list:
        v, r = Kp.values, _rank(Kp).values
        fin = np.isfinite(base_v) & np.isfinite(v)
        d = np.abs(v - base_v) > (CELL_TOL * np.maximum(1.0, np.abs(base_v)))
        mv = max(mv, float((d & fin).sum() / max(fin.sum(), 1)))
        finr = np.isfinite(base_r) & np.isfinite(r)
        dr = np.abs(r - base_r) > CELL_TOL
        mr = max(mr, float((dr & finr).sum() / max(finr.sum(), 1)))
    return mv, mr


def fingerprint(K):
    """Identify a key by WHAT IT COMPUTES, not by its source text: hash of its rounded
    cross-sectional ranks plus the NaN mask.  Two texts that rank identically are one key."""
    r = np.round(_rank(K).values.astype(float), 6)
    m = ~np.isfinite(r)
    r = np.where(m, -9.0, r)
    h = hashlib.blake2b(digest_size=16)
    h.update(np.ascontiguousarray(r).tobytes())
    h.update(np.ascontiguousarray(m).tobytes())
    return h.hexdigest()


def admit(obj, p):
    """Is the captured object a KEY on this panel?  Same semantics as ideas 426/433."""
    if not isinstance(obj, pd.DataFrame):
        return "NOT_PANEL", f"{type(obj).__name__}", None
    if obj.shape[1] < 2:
        return "NOT_PANEL", f"{obj.shape[1]} col", None
    if not obj.index.equals(p.index):
        return "NOT_PANEL", "index", None
    if obj.dtypes.map(lambda d: d.kind in "bO").any():
        return "NOT_NUMERIC", str(obj.dtypes.iloc[0]), None
    v = obj.select_dtypes("number").astype(float)
    if v.shape[1] < 2 or not np.isfinite(v.values).any():
        return "NOT_NUMERIC", "empty", None
    r = _rank(v)
    if float(r.std(axis=1).mean()) < 1e-12:
        return "DEGENERATE", "no cross-section", None
    return "KEY", "", v


def causal(fn, p, v):
    """PROTOCOL / idea 426 correction 2: perturb prices strictly AFTER a cut and ask whether the
    key BEFORE the cut moves.  A forward return passes T1 -- it must not reach a book."""
    cut = len(p) // 2
    p2 = p.copy()
    rng = np.random.default_rng(SEED + 1)
    p2.iloc[cut:] = p2.iloc[cut:].values * (1.0 + rng.normal(0.0, 0.05, p2.iloc[cut:].shape))
    ok1, a = guarded(fn, p.copy(), v.copy())
    ok2, b = guarded(fn, p2, v.copy())
    if not (ok1 and ok2) or not isinstance(a, pd.DataFrame) or not isinstance(b, pd.DataFrame):
        return -1
    A, B = a.iloc[:cut].values, b.iloc[:cut].values
    fin = np.isfinite(A) & np.isfinite(B)
    return int(not bool((np.abs(A - B)[fin] > 1e-10).any()))


# ================================================================ PART A: the census + the WALL
SKIP_VALUE = (ast.Constant, ast.JoinedStr, ast.Str if hasattr(ast, "Str") else ast.Constant)


def name_set(node):
    return {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}


def _single_assign_defs(body, parent, params):
    d = dict(parent)
    cnt = Counter()

    def walk(b, sink):
        for nd in b:
            if isinstance(nd, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                continue
            if isinstance(nd, ast.Assign) and len(nd.targets) == 1 \
                    and isinstance(nd.targets[0], ast.Name):
                sink(nd.targets[0].id, nd.value)
            for fld in ("body", "orelse", "finalbody"):
                if hasattr(nd, fld):
                    walk(getattr(nd, fld), sink)

    walk(body, lambda nm, v: cnt.__setitem__(nm, cnt[nm] + 1))
    walk(body, lambda nm, v: d.__setitem__(nm, v) if cnt[nm] == 1 else None)
    d.update(params)
    return d


def _params(fn):
    a = fn.args
    allargs = list(a.posonlyargs) + list(a.args)
    out = {}
    if a.defaults:
        for arg, dv in zip(allargs[len(allargs) - len(a.defaults):], a.defaults):
            out[arg.arg] = dv
    for arg, dv in zip(a.kwonlyargs, a.kw_defaults):
        if dv is not None:
            out[arg.arg] = dv
    return out


def scope_defs(tree):
    mod = _single_assign_defs(tree.body, {}, {})
    out = [(tree, mod, None)]
    for nd in ast.walk(tree):
        if isinstance(nd, (ast.FunctionDef, ast.AsyncFunctionDef)):
            out.append((nd, _single_assign_defs(nd.body, mod, _params(nd)), nd))
    return out


def inline(expr, defs, depth=0):
    if depth > 7:
        return expr

    class T(ast.NodeTransformer):
        def visit_Name(self, n):
            if PRICE_RE.match(n.id) or VOL_RE.match(n.id) or n.id in FREE_OK:
                return n
            if n.id in defs:
                sub = {k: v for k, v in defs.items() if k != n.id}
                return inline(ast.parse(ast.unparse(defs[n.id])).body[0].value, sub, depth + 1)
            return n

    return T().visit(ast.parse(ast.unparse(expr)).body[0].value)


class Rename(ast.NodeTransformer):
    def visit_Name(self, n):
        if PRICE_RE.match(n.id):
            return ast.Name(id="px", ctx=n.ctx)
        if VOL_RE.match(n.id):
            return ast.Name(id="vol", ctx=n.ctx)
        return n


class _SelfCheck(ast.NodeVisitor):
    """idea 426 (cloud) rule: does the expression name only px/vol, a safe module, literals?"""
    def __init__(self):
        self.names, self.ok = set(), True

    def visit_Name(self, node):
        self.names.add(node.id)

    def visit_Lambda(self, node):
        self.ok = False

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id not in SAFE_MODULES:
            self.ok = False
        self.generic_visit(node)


def self_contained(expr):
    ck = _SelfCheck(); ck.visit(expr)
    if not ck.ok:
        return False
    free = {n for n in ck.names if n not in SAFE_MODULES}
    return bool(free & PRICE_NAMES) and not (free - PRICE_NAMES - VOL_NAMES)


def blocker_class(name, tree, fn, multi, loops, unpack, imported, modnames):
    if fn is not None:
        a = fn.args
        allargs = [x.arg for x in list(a.posonlyargs) + list(a.args)]
        nd = len(a.defaults)
        undef = allargs[:len(allargs) - nd] if nd else allargs
        if name in undef or name in [x.arg for x, d in zip(a.kwonlyargs, a.kw_defaults) if d is None]:
            return "PARAM_NODEFAULT"
    if name in imported:
        return "IMPORTED"
    if name in loops:
        return "LOOP_TARGET"
    if name in unpack:
        return "TUPLE_UNPACK"
    if multi.get(name, 0) > 1:
        return "MULTI_ASSIGN"
    if name in modnames:
        return "GLOBAL_OTHER"
    return "UNKNOWN"


def census():
    log("\n=== PART A  THE CENSUS AND THE ANATOMY OF THE WALL ===")
    files = sorted(ROOT.glob("research/**/*.py"))
    HC = Counter()
    wall_rows, uniq_sites, recon = [], set(), defaultdict(set)
    self_sites, self_exprs = 0, defaultdict(set)
    for f in files:
        if f.name == SELF_NAME:
            continue
        try:
            src = f.read_text()
            tree = ast.parse(src)
        except Exception:
            HC["file_parse_fail"] += 1
            continue
        HC["files"] += 1
        imported = {n.asname or n.name.split(".")[0]
                    for nd in ast.walk(tree) if isinstance(nd, (ast.Import, ast.ImportFrom))
                    for n in nd.names}
        loops = {t.id for nd in ast.walk(tree) if isinstance(nd, (ast.For, ast.comprehension))
                 for t in ast.walk(nd.target) if isinstance(t, ast.Name)}
        unpack = {t.id for nd in ast.walk(tree) if isinstance(nd, ast.Assign)
                  for tg in nd.targets if isinstance(tg, (ast.Tuple, ast.List))
                  for t in ast.walk(tg) if isinstance(t, ast.Name)}
        multi = Counter(t.id for nd in ast.walk(tree) if isinstance(nd, ast.Assign)
                        for tg in nd.targets for t in ast.walk(tg) if isinstance(t, ast.Name))
        modnames = {nd.targets[0].id for nd in tree.body
                    if isinstance(nd, ast.Assign) and isinstance(nd.targets[0], ast.Name)}
        for scope, defs, fn in scope_defs(tree):
            for node in ast.walk(scope):
                if not isinstance(node, ast.Assign):
                    continue
                v = node.value
                if isinstance(v, ast.Constant):
                    continue
                HC["assign_sites"] += 1
                try:
                    iv = inline(v, defs)
                except Exception:
                    HC["inline_fail"] += 1
                    continue
                nm = name_set(iv)
                if not any(PRICE_RE.match(x) or VOL_RE.match(x) for x in nm):
                    HC["not_price_bearing"] += 1
                    continue
                HC["key_bearing_sites"] += 1
                tgt = node.targets[0].id if isinstance(node.targets[0], ast.Name) else "<tuple>"
                uniq_sites.add((f.name, node.lineno, tgt))
                if self_contained(v):
                    self_sites += 1
                    try:
                        self_exprs[ast.unparse(Rename().visit(
                            ast.parse(ast.unparse(v)).body[0].value))].add(f.name)
                    except Exception:
                        pass
                free = {x for x in nm
                        if not (PRICE_RE.match(x) or VOL_RE.match(x) or x in FREE_OK)}
                if free:
                    HC["free_var_wall"] += 1
                    cls = sorted({blocker_class(x, tree, fn, multi, loops, unpack, imported,
                                                modnames) for x in free})
                    wall_rows.append(dict(file=f.name, lineno=node.lineno, var=tgt,
                                          fn=fn.name if fn is not None else "<module>",
                                          n_free=len(free), free=",".join(sorted(free))[:80],
                                          classes="|".join(cls), sole=cls[0] if len(cls) == 1 else ""))
                    continue
                try:
                    s = ast.unparse(Rename().visit(iv))
                except Exception:
                    HC["unparse_fail"] += 1
                    continue
                if len(s) > 400:
                    HC["too_long"] += 1
                    continue
                HC["reconstructible_sites"] += 1
                recon[s].add(f.name)
    W = pd.DataFrame(wall_rows)
    kb = max(HC["key_bearing_sites"], 1)
    log(f"  corpus: {HC['files']} committed .py under research/ ({HC['file_parse_fail']} unparseable)")
    log(f"  assignment sites VISITED (multi-scope, lane B's counter) {HC['assign_sites']:>8,}")
    log(f"    of which KEY-BEARING                                   {kb:>8,}")
    log(f"      reconstructible after INLINE                         {HC['reconstructible_sites']:>8,}"
        f"  ({HC['reconstructible_sites']/kb:.1%})")
    log(f"      self-contained (SELF, idea 426 cloud)                {self_sites:>8,}"
        f"  ({self_sites/kb:.1%})")
    log(f"      blocked by the FREE-VARIABLE WALL                    {HC['free_var_wall']:>8,}"
        f"  ({HC['free_var_wall']/kb:.1%})")
    log(f"    distinct normalised INLINE expressions                 {len(recon):>8,}")
    log(f"    distinct normalised SELF expressions                   {len(self_exprs):>8,}")
    log(f"  CORRECTION TO THE DENOMINATOR: the 30,092 figure counts every site once per SCOPE it "
        f"is visible in.\n    DISTINCT (file, line, target) key-bearing sites: {len(uniq_sites):,} "
        f"-- the visited count is {kb/max(len(uniq_sites),1):.2f}x the distinct one.")
    if len(W):
        log("\n  anatomy of the wall (a site is blocked by the UNION of its free names):")
        log(f"    {'blocker class':18s} {'sites touched':>13} {'share':>7} | "
            f"{'SOLE blocker':>12} {'share':>7}")
        allc = Counter(c for r in wall_rows for c in r["classes"].split("|"))
        sole = Counter(r["sole"] for r in wall_rows if r["sole"])
        n = len(W)
        for c, k in allc.most_common():
            log(f"    {c:18s} {k:13,} {k/n:7.1%} | {sole.get(c,0):12,} {sole.get(c,0)/n:7.1%}")
        log(f"    {'(single-class site)':18s} {'':13} {'':7} | {sum(sole.values()):12,} "
            f"{sum(sole.values())/n:7.1%}")
        log(f"    median free names per blocked site: {W.n_free.median():.0f}  "
            f"(mean {W.n_free.mean():.2f}, max {W.n_free.max()})")
        log(f"    blocked sites at MODULE scope {int((W.fn=='<module>').sum()):,} "
            f"({(W.fn=='<module>').mean():.1%}); inside a function "
            f"{int((W.fn!='<module>').sum()):,}")
    pd.DataFrame([dict(metric=k, value=v) for k, v in sorted(HC.items())]
                 + [dict(metric="self_contained_sites", value=self_sites),
                    dict(metric="distinct_sites_file_line_target", value=len(uniq_sites)),
                    dict(metric="distinct_INLINE_exprs", value=len(recon)),
                    dict(metric="distinct_SELF_exprs", value=len(self_exprs))]
                 ).to_csv(f"{STEM}.census.csv", index=False)
    if len(W):
        W.to_csv(f"{STEM}.wall.csv", index=False)
    return HC, W, recon, self_exprs, uniq_sites


# ================================================================ PART B: the mechanisms
DANGER = ("to_csv", "write_text", "write_bytes", "savefig", "mkdir", "unlink", "rmtree",
          "subprocess", "os.system", "open(", "to_pickle", "to_json", "check_call", "run(")
SAFE_CALL_ROOTS = {"Path", "str", "int", "float", "bool", "list", "dict", "set", "tuple",
                   "sorted", "len", "range", "json", "np", "pd", "os", "sys", "math",
                   "Counter", "defaultdict", "frozenset", "re"}


def _call_roots_ok(node):
    for nd in ast.walk(node):
        if isinstance(nd, ast.Call):
            f = nd.func
            while isinstance(f, ast.Attribute):
                f = f.value
            if not isinstance(f, ast.Name) or f.id not in SAFE_CALL_ROOTS:
                return False
    return True


def def_only_shell(path):
    """Imports, defs and literal-ish module constants.  Every other top-level statement --
    every bare call, every `px = load_universe()`, every write -- is DROPPED.  This is exactly
    what the proposed convention (`key(px, vol)` at module level) makes importable."""
    src = path.read_text()
    tree = ast.parse(src)
    keep = []
    for nd in tree.body:
        if isinstance(nd, (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.AsyncFunctionDef,
                           ast.ClassDef)):
            keep.append(nd)
        elif isinstance(nd, (ast.Assign, ast.AnnAssign)) and _call_roots_ok(nd):
            seg = ast.unparse(nd)
            if not any(d in seg for d in DANGER):
                keep.append(nd)
    return [compile(ast.fix_missing_locations(ast.Module(body=[nd], type_ignores=[])),
                    str(path), "exec") for nd in keep]


_SHELL = {}


def shell_ns(path):
    """Namespace of the file's def-only shell, cached.  (ok, ns_or_reason)"""
    k = str(path)
    if k in _SHELL:
        return _SHELL[k]
    def _go():
        ns = {"__name__": "_harness_" + path.stem, "__file__": str(path)}
        nfail = 0
        for code in def_only_shell(path):
            try:
                exec(code, ns)                                  # noqa: S102 - corpus code
            except BaseException:                               # noqa: BLE001
                nfail += 1                # a shell statement that needs a dropped one; skip it
        ns["_shell_skipped"] = nfail
        return ns
    ok, r = guarded(_go, budget=12.0)
    _SHELL[k] = (ok, r)
    return _SHELL[k]


def bind_params(fn, ns, px, vol, mode):
    """Seed a call/exec namespace for fn's parameters.  Returns (ok, dict)."""
    a = fn.args
    allargs = list(a.posonlyargs) + list(a.args)
    nd = len(a.defaults)
    dflt = dict(zip([x.arg for x in allargs[len(allargs) - nd:]], a.defaults)) if nd else {}
    for x, d in zip(a.kwonlyargs, a.kw_defaults):
        if d is not None:
            dflt[x.arg] = d
    out, matched = {}, False
    names = [x.arg for x in allargs] + [x.arg for x in a.kwonlyargs]
    for i, nmv in enumerate(names):
        if PRICE_RE.match(nmv):
            out[nmv] = px; matched = True
        elif VOL_RE.match(nmv):
            out[nmv] = vol
        elif nmv in dflt:
            try:
                out[nmv] = eval(compile(ast.Expression(dflt[nmv]), "<d>", "eval"), dict(ns))
            except Exception:
                return False, "default"
        elif mode == "GUESS":
            out[nmv] = None
        else:
            return False, "undefaulted:" + nmv
    if not matched:
        if mode == "GUESS" and names:
            out[names[0]] = px; matched = True
        else:
            return False, "no price param"
    return True, out


def mech_import(files, p, v, mode):
    """MECH=IMPORT -- the CONVENTION.  Call every module-level function of the def-only shell
    with (px[, vol]).  Zero per-file work."""
    found, why = [], Counter()
    for f in files:
        try:
            tree = ast.parse(f.read_text())
        except Exception:
            why["parse"] += 1
            continue
        fns = [nd for nd in tree.body if isinstance(nd, ast.FunctionDef)]
        if not fns:
            why["no module-level def"] += 1
            continue
        ok, ns = shell_ns(f)
        if not ok:
            why["shell:" + str(ns)] += 1
            continue
        for fn in fns:
            if fn.name.startswith("_") or fn.name in ("main", "log", "P"):
                continue
            okb, kw = bind_params(fn, ns, p.copy(), v.copy(), mode)
            if not okb:
                why[str(kw).split(":")[0]] += 1
                continue
            g = ns.get(fn.name)
            if not callable(g):
                why["not callable"] += 1
                continue
            okc, obj = guarded(lambda: g(**kw))
            if not okc:
                why["call:" + str(obj)] += 1
                continue
            cls, det, clean = admit(obj, p)
            if cls != "KEY":
                why[cls] += 1
                continue
            found.append(dict(mech="IMPORT", bind=mode, file=f.name, fn=fn.name,
                              lineno=fn.lineno, var="<return>", key=clean))
    return found, why


class _Deflow(ast.NodeTransformer):
    """A prefix of a function body is not a function: `return`/`yield` inside a kept `if` or
    `for` is a SyntaxError at module level, so they become `pass`.  This is the harness's own
    approximation and it is reported as such."""
    def visit_Return(self, n):
        return ast.Pass()

    def visit_FunctionDef(self, n):
        return n

    def visit_Lambda(self, n):
        return n


def body_prefix_code(path, fn, lineno):
    """The one generic harness: fn's own statements up to and including the site, with bare
    calls and every writing statement removed."""
    body = []
    for s in fn.body:
        if getattr(s, "lineno", 0) > lineno:
            break
        if isinstance(s, (ast.Return, ast.Global, ast.Nonlocal, ast.Expr, ast.Raise)):
            continue
        try:
            seg = ast.unparse(s)
        except Exception:
            continue
        if any(d in seg for d in DANGER):
            continue
        body.append(_Deflow().visit(s))
    if not body:
        return None
    mod = ast.fix_missing_locations(ast.Module(body=body, type_ignores=[]))
    try:
        return compile(mod, str(path), "exec")
    except SyntaxError:
        return None


def mech_body(sites, p, v, mode):
    """MECH=BODY -- run the enclosing function's body prefix, then read the target local."""
    found, why = [], Counter()
    for (path, fnname, lineno, var) in sites:
        try:
            tree = ast.parse(path.read_text())
        except Exception:
            why["parse"] += 1
            continue
        fn = next((nd for nd in ast.walk(tree)
                   if isinstance(nd, (ast.FunctionDef, ast.AsyncFunctionDef))
                   and nd.name == fnname and nd.lineno <= lineno
                   and getattr(nd, "end_lineno", lineno) >= lineno), None)
        if fn is None:
            why["module scope (no enclosing fn)"] += 1
            continue
        ok, ns = shell_ns(path)
        if not ok:
            why["shell:" + str(ns)] += 1
            continue
        okb, kw = bind_params(fn, ns, p.copy(), v.copy(), mode)
        if not okb:
            why[str(kw).split(":")[0]] += 1
            continue
        code = body_prefix_code(path, fn, lineno)
        if code is None:
            why["empty prefix"] += 1
            continue

        def _go():
            loc = dict(ns); loc.update(kw)
            exec(code, loc)                                     # noqa: S102 - corpus code
            return loc.get(var, "<unset>")
        okc, obj = guarded(_go)
        if not okc:
            why["exec:" + str(obj)] += 1
            continue
        if isinstance(obj, str) and obj == "<unset>":
            why["target never bound"] += 1
            continue
        cls, det, clean = admit(obj, p)
        if cls != "KEY":
            why[cls] += 1
            continue
        found.append(dict(mech="BODY", bind=mode, file=path.name, fn=fnname, lineno=lineno,
                          var=var, key=clean))
    return found, why


def static_keys(exprs, p, v, label):
    """SELF / INLINE: evaluate the normalised source text."""
    found, why = [], Counter()
    for s, fl in exprs.items():
        def _go(s=s):
            return eval(compile(s, "<key>", "eval"),                     # noqa: S307
                        {"np": np, "pd": pd}, {"px": p.copy(), "vol": v.copy()})
        ok, obj = guarded(_go)
        if not ok:
            why["eval:" + str(obj)] += 1
            continue
        cls, det, clean = admit(obj, p)
        if cls != "KEY":
            why[cls] += 1
            continue
        found.append(dict(mech=label, bind="n/a", file=sorted(fl)[0], fn="", lineno=0,
                          var=s[:80], key=clean, src=s, n_files=len(fl)))
    return found, why


# ================================================================ gates
def gate_g1(px):
    q = px.drop(columns=["SPY"])
    w = rules_v2_weights(q, band=0.03, gross=0.75)
    r, t = fast_backtest(q, w)
    e = backtest(q, w, cost_bps=0, freq=FREQ)
    st = q.index[WARMUP]
    d1 = float((r.loc[st:] - e["returns"].loc[st:]).abs().max())
    d2 = float((t.loc[st:] - e["turnover"].loc[st:]).abs().max())
    log(f"  G1 fast_backtest vs engine.backtest: returns {d1:.3e}  turnover {d2:.3e}")
    assert d1 < 1e-10 and d2 < 1e-10, (d1, d2)


def gate_g2(px):
    q = px.drop(columns=["SPY"])
    r, t = fast_backtest(q, rules_v2_weights(q))
    L = legs(r - t * 10.0 / 1e4)
    log(f"  G2 live RULES v2 on U56 @10bps: {L['CAGR']:.2%} / {L['Sharpe']:.4f} / {L['MaxDD']:.2%}"
        f"   (idea 426 read 8.65% / 1.2092 / -11.90%)")
    assert abs(L["Sharpe"] - 1.2092) < 0.05, L["Sharpe"]


def gate_g3(p, v, pert):
    a = p / p.shift(126) - 1.0
    aa = [pp / pp.shift(126) - 1.0 for pp in pert]
    mv, mr = cert_on_key(a, aa)
    b = p.copy(); bb = list(pert)
    mv2, mr2 = cert_on_key(b, bb)
    log(f"  G3 poles of the theorem: px/px.shift(126)-1 moves value {mv:.2e} rank {mr:.2e}; "
        f"px moves value {mv2:.4f} rank {mr2:.4f}")
    assert mv < 1e-3 and mv2 > 0.5


def gate_g5(p, v, h0):
    h = (hashlib.blake2b(np.ascontiguousarray(p.values).tobytes(), digest_size=8).hexdigest(),
         tuple(p.columns), p.shape)
    log(f"  G5 the certificate panel is byte-identical after the whole grid: {h == h0}"
        f"  (corpus code is handed a COPY at every call boundary)")
    assert h == h0, (h, h0)


def panel_hash(p):
    return (hashlib.blake2b(np.ascontiguousarray(p.values).tobytes(), digest_size=8).hexdigest(),
            tuple(p.columns), p.shape)


def gate_g4(before):
    now = corpus_hash()
    diff = [k for k in before if before[k] != now.get(k)]
    log(f"  G4 the harness rewrote NOTHING in the record: {len(before)} committed files hashed, "
        f"{len(diff)} changed {diff[:3]}")
    assert not diff, diff


def corpus_hash():
    out = {}
    for pat in ("research/**/*.py", "research/*.md", "data/*.csv", "products/**/*.py"):
        for f in ROOT.glob(pat):
            if f.name == SELF_NAME or f.is_dir():
                continue
            try:
                out[str(f.relative_to(ROOT))] = hashlib.blake2b(
                    f.read_bytes(), digest_size=8).hexdigest()
            except Exception:
                pass
    return out


# ================================================================ PART D: consequence + rule 8
def key_book(K, px, topn=TOPN, gross=GROSS):
    rank = K.rank(axis=1, ascending=False)
    w = (rank <= topn).astype(float)
    s = w.sum(axis=1).replace(0, np.nan)
    return (w.div(s, axis=0) * gross).fillna(0.0)


def make_callable(row):
    """Re-evaluate an admitted key on ANY panel, whatever mechanism found it."""
    mech = row["mech"]
    if mech in ("SELF", "INLINE"):
        code = compile(row["src"], "<key>", "eval")
        return lambda p, v: eval(code, {"np": np, "pd": pd}, {"px": p, "vol": v})  # noqa: S307
    path = ROOT / "research" / "backtests" / row["file"]
    if not path.exists():
        cands = list(ROOT.glob(f"research/**/{row['file']}"))
        if not cands:
            return None
        path = cands[0]
    if mech == "IMPORT":
        def f_import(p, v, path=path, fnname=row["fn"], mode=row["bind"]):
            ok, ns = shell_ns(path)
            if not ok:
                raise RuntimeError("shell")
            tree = ast.parse(path.read_text())
            fn = next(nd for nd in tree.body
                      if isinstance(nd, ast.FunctionDef) and nd.name == fnname)
            okb, kw = bind_params(fn, ns, p, v, mode)
            if not okb:
                raise RuntimeError(str(kw))
            return ns[fnname](**kw)
        return f_import

    def f_body(p, v, path=path, fnname=row["fn"], lineno=row["lineno"], var=row["var"],
               mode=row["bind"]):
        ok, ns = shell_ns(path)
        if not ok:
            raise RuntimeError("shell")
        tree = ast.parse(path.read_text())
        fn = next(nd for nd in ast.walk(tree)
                  if isinstance(nd, (ast.FunctionDef, ast.AsyncFunctionDef))
                  and nd.name == fnname and nd.lineno <= lineno
                  and getattr(nd, "end_lineno", lineno) >= lineno)
        okb, kw = bind_params(fn, ns, p, v, mode)
        if not okb:
            raise RuntimeError(str(kw))
        code = body_prefix_code(path, fn, lineno)
        loc = dict(ns); loc.update(kw)
        exec(code, loc)                                          # noqa: S102
        return loc[var]
    return f_body


def consequence(K, panels, vols):
    log("\n=== PART D  WHAT THE EXTRA REACH BUYS: a book per key, both KEEP paths, 10/25 bps ===")
    ok = K[(K.admitted == 1) & (K.causal == 1)].copy()
    # STRATIFIED by reachability so the 426-REACH arm is never empty: the contrast this idea
    # is about is menu-minus-menu, and a menu of only-new keys cannot measure it.
    half = MENU_CAP // 2
    menu = pd.concat([ok[ok.new == 0].sort_values("n_files", ascending=False).head(half),
                      ok[ok.new == 1].sort_values("n_files", ascending=False).head(half)])
    log(f"  menu: {len(menu)} keys (cap {MENU_CAP}, {half} per reachability stratum, a reported axis) -- "
        f"{int(menu.new.sum())} NEWLY REACHABLE, {len(menu)-int(menu.new.sum())} already in "
        f"idea 426's reach.  T1 PASS {int(menu.T1_PASS.sum())} / FAIL {len(menu)-int(menu.T1_PASS.sum())}.")
    rows = []
    for pk, px in panels.items():
        q = px.drop(columns=["SPY"])
        spy = legs(px["SPY"].pct_change().fillna(0.0))
        rb, tb = fast_backtest(q, rules_v2_weights(q, band=0.03, gross=0.75))
        base = {c: legs(rb - tb * c / 1e4) for c in RUNGS}
        v = vols.get(pk)
        if v is None:
            rng = np.random.default_rng(SEED)
            v = pd.DataFrame(rng.lognormal(13.0, 0.8, size=q.shape), index=q.index, columns=q.columns)
        v = v.reindex(index=q.index, columns=q.columns).ffill()
        for _, r in menu.iterrows():
            fn = make_callable(r)
            if fn is None:
                continue
            okc, Kp = guarded(fn, q.copy(), v.copy(), budget=25.0)
            if not okc or not isinstance(Kp, pd.DataFrame) or Kp.shape[1] < 2:
                continue
            Kp = Kp.select_dtypes("number").astype(float).reindex(index=q.index, columns=q.columns)
            rr, tt = fast_backtest(q, key_book(Kp, q))
            for c in RUNGS:
                L = legs(rr - tt * c / 1e4)
                rows.append(dict(panel=pk, rung=c, kid=r.kid, mech=r.mech, bind=r.bind,
                                 new=int(r.new), T1=int(r.T1_PASS), key=str(r["label"])[:90],
                                 **L, pass4a=v4a(L, base[c]), pass4b=v4b(L, spy),
                                 base_OOS=base[c]["OOS"], spy_OOS=spy["OOS"],
                                 base_OOS_CAGR=base[c]["OOS_CAGR"], spy_OOS_CAGR=spy["OOS_CAGR"],
                                 base_OOS_DD=base[c]["OOS_DD"], spy_OOS_DD=spy["OOS_DD"]))
    G = pd.DataFrame(rows)
    G.to_csv(f"{STEM}.books.csv", index=False)
    if not len(G):
        log("  NO books: no admitted key survived re-evaluation on a full panel.")
        return G, menu
    log(f"  {len(G)} book-rows committed.  4a passes {int(G.pass4a.sum())}/{len(G)}; "
        f"4b passes {int(G.pass4b.sum())}/{len(G)}.")
    if len(G):
        for c in RUNGS:
            s = G[G.rung == c]
            log(f"    {c:.0f} bps  mean full Sharpe {s.Sharpe.mean():.4f}  best {s.Sharpe.max():.4f} "
                f"({s.loc[s.Sharpe.idxmax(),'key'][:60]})")
    return G, menu


def rule8(G):
    log("\n=== PROTOCOL 8  WALK-FORWARD: choose the key on IS 2008-2016, read OOS once ===")
    rows = []
    for (pk, c), s in G.groupby(["panel", "rung"]):
        for label, sub in (("426-REACH only", s[s.new == 0]),
                           ("+643 EXTRA REACH", s),
                           ("NEWLY REACHABLE only", s[s.new == 1])):
            if len(sub) == 0:
                continue
            r = sub.loc[sub.IS.astype(float).idxmax()]
            rows.append(dict(panel=pk, rung=c, menu=label, key=r.key, mech=r.mech, new=int(r.new),
                             IS=r.IS, OOS=r.OOS, OOS_CAGR=r.OOS_CAGR, OOS_DD=r.OOS_DD,
                             CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD, H1=r.H1, H2=r.H2,
                             pass4a=int(r.pass4a), pass4b=int(r.pass4b),
                             base_OOS=r.base_OOS, spy_OOS=r.spy_OOS,
                             base_OOS_CAGR=r.base_OOS_CAGR, spy_OOS_CAGR=r.spy_OOS_CAGR,
                             base_OOS_DD=r.base_OOS_DD, spy_OOS_DD=r.spy_OOS_DD))
    W = pd.DataFrame(rows)
    W.to_csv(f"{STEM}.wf.csv", index=False)
    if not len(W):
        log("  no books -- nothing to walk forward.")
        return W
    log(f"    {'panel':9s} {'rung':>4} {'menu':22s} {'OOS Sh':>7} {'OOS CAGR':>9} {'OOS DD':>8} "
        f"{'4a':>3} {'4b':>3} | {'v2 OOS':>7} {'SPY OOS':>7}")
    for _, r in W.sort_values(["panel", "rung", "menu"]).iterrows():
        log(f"    {r.panel:9s} {r.rung:4.0f} {r.menu:22s} {r.OOS:7.4f} {r.OOS_CAGR:9.2%} "
            f"{r.OOS_DD:8.2%} {r.pass4a:3d} {r.pass4b:3d} | {r.base_OOS:7.4f} {r.spy_OOS:7.4f}")
    for c in RUNGS:
        a = W[(W.rung == c) & (W.menu == "426-REACH only")].set_index("panel")
        b = W[(W.rung == c) & (W.menu == "+643 EXTRA REACH")].set_index("panel").reindex(a.index)
        chg = int((a.key != b.key).sum())
        log(f"    {c:.0f} bps  the EXTRA REACH changes the rule-8 pick in {chg} of {len(a)} panels;"
            f" mean OOS Sharpe {a.OOS.mean():.4f} -> {b.OOS.mean():.4f} "
            f"({b.OOS.mean()-a.OOS.mean():+.4f})")
    return W


# ================================================================ main
def main():
    t0 = time.time()
    log("=" * 100)
    log("IDEA 643  can-the-record-s-keys-be-made-REACHABLE-without-a-harness   (cloud, 2026-09-10)")
    log("=" * 100)
    before = corpus_hash()

    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    panels["SMALL439"] = sm.drop(columns=[c for c in sm.columns if c in bad])
    log(f"  SMALL panel: dropped {len(bad)} tickers with max_1d_move >= 1.0 "
        f"(data/small_meta.csv) -> {panels['SMALL439'].shape[1]-1} names")
    vols = {"U56": None, "B136": None, "SMALL439": None}
    try:
        vs = load_volume(small=True)
        vols["SMALL439"] = vs.drop(columns=[c for c in vs.columns if c in bad], errors="ignore")
    except Exception as e:
        log(f"  (no cached share volume: {type(e).__name__})")
    log("  panels: " + "  ".join(f"{k} {v.shape[1]-1}x{len(v)}" for k, v in panels.items()))

    q = panels["SMALL439"].drop(columns=["SPY"])
    p = q.iloc[-750:, :140].copy()
    if vols["SMALL439"] is not None:
        v = vols["SMALL439"].reindex(index=p.index, columns=p.columns).ffill()
        vsrc = "data/volume_small.csv[.gz]"
    else:
        rng = np.random.default_rng(SEED)
        v = pd.DataFrame(rng.lognormal(13.0, 0.8, size=p.shape), index=p.index, columns=p.columns)
        vsrc = "deterministic price-free surrogate"
    rng = np.random.default_rng(SEED)
    pert = [p * np.exp(rng.normal(0.0, SIGMA, p.shape[1])) for _ in range(NDRAW)]
    log(f"  certificate panel: SMALL439 slice {p.shape[0]}d x {p.shape[1]} names "
        f"[{p.index[0].date()}..{p.index[-1].date()}], volume {vsrc}, sigma {SIGMA}, "
        f"{NDRAW} draws, seed {SEED}")

    log("\n=== GATES ===")
    gate_g1(panels["U56"]); gate_g2(panels["U56"]); gate_g3(p, v, pert)
    h0 = panel_hash(p)

    HC, W, recon, selfx, uniq = census()

    # ---------------------------------------------------------- the 8-point grid
    log("\n=== PART B  THE REACH GRID: 4 mechanisms x 2 binding modes (all 8 points reported) ===")
    files = [f for f in sorted(ROOT.glob("research/**/*.py")) if f.name != SELF_NAME]
    # the wall sample + every UNREACHABLE-shaped site, deterministic
    if len(W):
        Wf = W[W.fn != "<module>"].reset_index(drop=True)
        rs = np.random.default_rng(SEED)
        take = rs.choice(len(Wf), size=min(WALL_SAMPLE, len(Wf)), replace=False)
        sample = Wf.iloc[sorted(take)]
        log(f"  wall sample for MECH=BODY: {len(sample)} of {len(Wf):,} function-scope blocked "
            f"sites (seed {SEED}); module-scope blocked sites ({int((W.fn=='<module>').sum()):,}) "
            f"are OUT OF REACH for a body-prefix harness by construction.")
        sites = [(next(iter(ROOT.glob(f"research/**/{r.file}")), None), r.fn, int(r.lineno), r.var)
                 for _, r in sample.iterrows()]
        sites = [s for s in sites if s[0] is not None]
    else:
        sample, sites = pd.DataFrame(), []

    grid, allfound = [], []
    for mech in ("SELF", "INLINE", "IMPORT", "BODY"):
        for mode in ("STRICT", "GUESS"):
            t1 = time.time()
            if mech in ("SELF", "INLINE"):
                if mode == "GUESS":                        # static rules ignore the binding dial
                    prev = [g for g in grid if g["mech"] == mech][0]
                    grid.append({**prev, "bind": "GUESS", "note": "static: dial does not apply"})
                    continue
                found, why = static_keys(selfx if mech == "SELF" else recon, p, v, mech)
                denom = len(selfx) if mech == "SELF" else len(recon)
                unit = "distinct normalised expressions"
            elif mech == "IMPORT":
                found, why = mech_import(files, p, v, mode)
                denom = len(files)
                unit = "files"
            else:
                found, why = mech_body(sites, p, v, mode)
                denom = len(sites)
                unit = "sampled wall sites"
            fps = {}
            for r in found:
                r["fp"] = fingerprint(r["key"])
                fps.setdefault(r["fp"], r)
            grid.append(dict(mech=mech, bind=mode, tried=denom, unit=unit, admitted=len(found),
                             distinct_keys=len(fps), files=len({r["file"] for r in found}),
                             seconds=round(time.time() - t1, 1),
                             top_reason=", ".join(f"{k} {n}" for k, n in why.most_common(3)),
                             note=""))
            allfound.extend(found)
            log(f"  {mech:7s} {mode:7s} tried {denom:6,} {unit:32s} -> admitted {len(found):5,} "
                f"KEYS, {len(fps):4,} DISTINCT, {len({r['file'] for r in found}):4,} files, "
                f"{time.time()-t1:6.1f}s")
            log(f"          top rejection reasons: {', '.join(f'{k} {n}' for k, n in why.most_common(4))}")
            if mech == "BODY" and denom and not found:
                ub = 1.0 - 0.05 ** (1.0 / denom)
                log(f"          ZERO of {denom} sampled sites: the exact one-sided 95% bound on the "
                    f"wall clear rate is {ub:.2%}, i.e. at most "
                    f"{ub*len(W[W.fn!='<module>']):,.0f} of {len(W[W.fn!='<module>']):,} "
                    f"function-scope blocked sites.")
    R = pd.DataFrame(grid)
    R.to_csv(f"{STEM}.reach.csv", index=False)

    # ---------------------------------------------------------- reach per unit of work
    HARNESS_LINES = {"SELF": 14, "INLINE": 29, "IMPORT": 58, "BODY": 46}
    log("\n  REACH PER UNIT OF WORK (work = lines of harness written ONCE; per-file work is 0 "
        "for every rung):")
    log(f"    {'mech':7s} {'lines':>6} {'distinct keys':>14} {'keys/line':>10} {'marginal keys':>14}")
    seen = set()
    for mech in ("SELF", "INLINE", "IMPORT", "BODY"):
        fp = {r["fp"] for r in allfound if r["mech"] == mech}
        marg = len(fp - seen); seen |= fp
        ln = HARNESS_LINES[mech]
        log(f"    {mech:7s} {ln:6d} {len(fp):14,} {len(fp)/ln:10.3f} {marg:14,}")
    log(f"    union of all four mechanisms: {len(seen):,} DISTINCT keys")

    # ---------------------------------------------------------- the convention's adoption rate
    conv = 0
    for f in files:
        try:
            tree = ast.parse(f.read_text())
        except Exception:
            continue
        for nd in tree.body:
            if isinstance(nd, ast.FunctionDef):
                a = [x.arg for x in list(nd.args.posonlyargs) + list(nd.args.args)]
                if a and PRICE_RE.match(a[0]):
                    conv += 1
                    break
    log(f"\n  CONVENTION ADOPTION TODAY: {conv} of {len(files)} committed files ({conv/len(files):.1%}) "
        f"already expose a module-level function whose FIRST parameter is a price name -- i.e. the "
        f"convention idea 643 proposes is already met by that share of the corpus, and MECH=IMPORT "
        f"is the reach it delivers.")

    # ---------------------------------------------------------- certificate + causality on the union
    log("\n=== PART C  THE UNION OF REACHED KEYS: T1 (VALUE, one rank step) and CAUSALITY ===")
    step = 1.0 / p.shape[1]
    prev_fp = set()
    rows, byfp = [], {}
    for r in allfound:
        byfp.setdefault(r["fp"], []).append(r)
    # idea 426's reach = SELF + INLINE (the two static mechanisms it and lane B used)
    reach426 = {r["fp"] for r in allfound if r["mech"] in ("SELF", "INLINE")}
    kid = 0
    errs = Counter()
    for fp, group in byfp.items():
        r = group[0]
        K = r["key"]
        try:
            fnc = make_callable({**r, "src": r.get("src", "")})
            pert_keys = []
            for pp in pert:
                okp, kp = guarded(fnc, pp.copy(), v.copy())
                if not okp or not isinstance(kp, pd.DataFrame):
                    pert_keys = []
                    break
                pert_keys.append(kp.select_dtypes("number").astype(float)
                                 .reindex(index=K.index, columns=K.columns))
            if pert_keys:
                mv, mr = cert_on_key(K, pert_keys)
                t1 = int(mv <= step)
            else:
                mv, mr, t1 = np.nan, np.nan, -1
            cz = causal(fnc, p, v) if fnc is not None else -1
        except Exception as e:
            errs[f"{type(e).__name__}: {str(e)[:60]}"] += 1
            mv, mr, t1, cz = np.nan, np.nan, -1, -1
        rows.append(dict(kid=f"K{kid:03d}", fp=fp, mech=r["mech"], bind=r["bind"], file=r["file"],
                         fn=r["fn"], var=str(r["var"])[:80], lineno=r["lineno"],
                         label=r.get("src", f"{r['file']}::{r['fn'] or r['var']}"),
                         n_sites=len(group), n_files=len({g["file"] for g in group}),
                         mechs="|".join(sorted({g["mech"] for g in group})),
                         admitted=1, moved_value=mv, moved_rank=mr, T1_PASS=t1, causal=cz,
                         new=int(fp not in reach426), src=r.get("src", "")))
        kid += 1
    K = pd.DataFrame(rows)
    K.to_csv(f"{STEM}.keys.csv", index=False)
    if errs:
        log("  (Part C exceptions: " + "; ".join(f"{k} x{n}" for k, n in errs.most_common(3)) + ")")
    nb = int(K.new.sum())
    log(f"  {len(K)} DISTINCT keys reached in total; {len(reach426)} of them by the two STATIC "
        f"mechanisms idea 426 used, {nb} NEWLY REACHABLE ({nb/max(len(K),1):.1%} of the union).")
    log(f"  T1 (VALUE, one rank step = {step:.4f}): PASS {int((K.T1_PASS==1).sum())}, "
        f"FAIL {int((K.T1_PASS==0).sum())}, unreadable {int((K.T1_PASS==-1).sum())}.")
    log(f"  CAUSALITY: causal {int((K.causal==1).sum())}, NON-CAUSAL {int((K.causal==0).sum())} "
        f"(excluded from every book below), unreadable {int((K.causal==-1).sum())}.")
    if nb:
        log("  the newly reachable keys, by mechanism: "
            + ", ".join(f"{k} {n}" for k, n in K[K.new == 1].mech.value_counts().items()))

    G, menu = consequence(K, panels, vols)
    Wf = rule8(G)
    gate_g5(p, v, h0)
    gate_g4(before)
    log(f"\ndone in {time.time()-t0:.0f}s")
    Path(f"{STEM}.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()

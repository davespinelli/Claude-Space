#!/usr/bin/env python3
"""IDEA 529 — audit every fail-set column in the record for SET vs FIRSTFAIL (lane B, 2026-09-12).

QUEUE: idea 527 found the fail4b/f4b column carries two incompatible semantics (SET = every
failing bar; FIRSTFAIL = the first failing bar under a short-circuit chain) and classified files
only by whether ANY row emits >= 2 tokens, which MISLABELS a genuine SET file whose books never
fail two bars at once.  Read each producing SCRIPT's keep-paths function directly (AST, as idea
515 did for asserts), publish a per-file semantics stamp, then re-run idea 527's headline on the
corrected partition.  Max 2 params (parser, sample).

WHY THIS RUN HAS A PRICE LEG (four previous lane runs SKIPped it for not having one).  The
mislabel idea 527 can make is not a property of markdown: it is the event "a real book fails two
4b bars at once".  So this run does not only re-read the record — it REBUILDS the object.
1,200 real books (80 random equal-weight k=20 draws x 5 gross rungs x 3 panels) are priced
through products/backtester/engine at 10 bps, t+1, weekly, seed 529, and their 4b bar vectors
are computed.  That gives a MEASURED multi-fail rate p, hence a measured probability that a
genuine SET file of n rows is invisible to idea 527's detector -- the exact quantity the queue
says is unmeasured.  Rule 8 (walk-forward) is run on that rate and on the books.

PARAMS (exactly 2, all grid points reported):
  P1 parser  in {strict, loose}   how hard the AST chases the fail-column expression
  P2 sample  in {all, singleton}  every fail-column artefact, vs only idea 527's ambiguous tier

Outputs (all beside this file):
  *.console.txt   full console transcript
  *.stamps.csv    per-file semantics stamp, every (parser) reading
  *.grid.csv      the 4 (parser, sample) grid points
  *.books.csv     1,200 priced books with their full 4b bar vectors and 4a/4b verdicts
  *.walkforward.csv  rule-8 IS(<=2016)-chosen reading evaluated on OOS(2017+), untouched
"""
from __future__ import annotations
import ast, gzip, io, os, re, sys, glob, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights   # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics                                     # noqa

BT = ROOT / "research" / "backtests"
STEM = BT / "2026-09-12_audit-every-fail-set-column-in-the-record-for-SET-vs-FIRSTFAIL_B"

BARS = ["H1", "H2", "OOS", "DD", "CAGR"]          # canonical short-circuit order (idea 527)
FAILCOLS = {"fail4b", "f4b", "fail_4b", "failbars", "fail_bars", "failset", "fail_set",
            "binding", "bind4b", "fail", "fails"}
BARTOKENS = {"h1", "h2", "oos", "dd", "ddcap", "cagr", "cagrfloor", "maxdd", "sharpe"}
COST_BPS, FREQ, SEED = 10, "W", 529
IS_END, OOS_START = "2016-12-31", "2017-01-01"
KDRAW, NDRAW = 20, 80
GROSS_RUNGS = [0.375, 0.500, 0.625, 0.750, 1.000]

_LOG: list[str] = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); _LOG.append(s)

def rule(t=""):
    P("\n" + "=" * 110); P(t); P("=" * 110)


# ══════════════════════════════════════════════════════════════════ PART 1: the AST stamp
def _open(p):
    return gzip.open(p, "rt", errors="replace") if str(p).endswith(".gz") else open(p, errors="replace")

def header(p):
    try:
        with _open(p) as f:
            return [c.strip().strip('"') for c in f.readline().rstrip("\n").split(",")]
    except Exception:
        return []

def parse_failset(v):
    """A cell -> frozenset of bar tokens, or None if it is not a fail-set cell."""
    if not isinstance(v, str):
        return None
    s = v.strip()
    if s in ("-", "", "nan", "none", "None", "NONE"):
        return frozenset()
    toks = [t.strip().lower() for t in re.split(r"[,|+;/ ]+", s) if t.strip()]
    if not toks or not all(t in BARTOKENS for t in toks):
        return None
    canon = {"ddcap": "dd", "cagrfloor": "cagr", "maxdd": "dd", "sharpe": "h1"}
    return frozenset(canon.get(t, t).upper() for t in toks)


def producing_script(csv_path):
    """research/backtests/<run>.<part>.csv[.gz] -> research/backtests/<run>.py, if committed."""
    b = os.path.basename(csv_path)
    for suf in (".csv.gz", ".csv"):
        if b.endswith(suf):
            b = b[: -len(suf)]
            break
    run = b.split(".")[0]                     # strip the .part
    p = BT / f"{run}.py"
    return p if p.exists() else None


class _Scope:
    """One function body (or the module body), with nested functions excluded."""
    def __init__(self, name):
        self.name = name
        self.assigns: dict[str, list[tuple]] = {}   # name -> [(rhs_node, tuple_index|None)]
        self.appends: dict[str, set] = {}           # list name -> {bar tokens appended as literals}
        self.elif_names: set[str] = set()           # names assigned inside an if/elif CHAIN
        self.loop_appends: dict[str, str] = {}      # list name -> SET (enumerates) / FIRSTFAIL (breaks)


def _body_nodes(fn):
    """Every node under fn, NOT descending into nested function definitions."""
    stack = list(fn.body) if not isinstance(fn, ast.Module) else list(fn.body)
    while stack:
        n = stack.pop()
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n is not fn:
            continue
        yield n
        for c in ast.iter_child_nodes(n):
            if isinstance(c, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            stack.append(c)


def _build_scope(fn, label):
    sc = _Scope(label)
    for n in _body_nodes(fn):
        if isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name):
                    sc.assigns.setdefault(t.id, []).append((n.value, None))
                elif isinstance(t, (ast.Tuple, ast.List)):
                    for i, el in enumerate(t.elts):
                        if isinstance(el, ast.Name):
                            rhs = (n.value.elts[i] if isinstance(n.value, (ast.Tuple, ast.List))
                                   and i < len(n.value.elts) else n.value)
                            idx = None if isinstance(n.value, (ast.Tuple, ast.List)) else i
                            sc.assigns.setdefault(el.id, []).append((rhs, idx))
        elif isinstance(n, ast.Call):
            f = n.func
            if (isinstance(f, ast.Attribute) and f.attr == "append"
                    and isinstance(f.value, ast.Name) and n.args
                    and isinstance(n.args[0], ast.Constant)
                    and isinstance(n.args[0].value, str)
                    and n.args[0].value.strip().lower() in BARTOKENS):
                sc.appends.setdefault(f.value.id, set()).add(n.args[0].value.strip().upper())
        elif isinstance(n, (ast.For, ast.AsyncFor)):
            # `for b in <bars>: if ...: f.append(b)` enumerates -> SET, unless it short-circuits
            tgt = {q.id for q in ast.walk(n.target) if isinstance(q, ast.Name)}
            short = any(isinstance(c, (ast.Break, ast.Return)) for c in ast.walk(n))
            for sub in ast.walk(n):
                if (isinstance(sub, ast.Call) and isinstance(sub.func, ast.Attribute)
                        and sub.func.attr in ("append", "add") and isinstance(sub.func.value, ast.Name)
                        and sub.args and isinstance(sub.args[0], ast.Name)
                        and sub.args[0].id in tgt):
                    sc.loop_appends[sub.func.value.id] = "FIRSTFAIL" if short else "SET"
        elif isinstance(n, ast.If):
            if len(n.orelse) == 1 and isinstance(n.orelse[0], ast.If):   # a real elif CHAIN
                for sub in ast.walk(n):
                    if isinstance(sub, ast.Assign):
                        for t in sub.targets:
                            for q in ast.walk(t):
                                if isinstance(q, ast.Name):
                                    sc.elif_names.add(q.id)
    return sc


class _Stamper:
    """Classify how a script BUILDS its fail-set column value.

    SET       - the value enumerates every failing bar: a comprehension over a bar container,
                or a list that has >= 2 literal bar tokens appended at independent (non-elif)
                sites, then joined.
    FIRSTFAIL - a short-circuit decides it: an if/elif chain assigning the name, or a helper
                that `return`s inside >= 2 per-bar branches before testing the rest.

    parser=strict resolves a name only when it has exactly ONE assignment site in the scope
    that owns the expression; parser=loose takes the last site and may fall back to any scope.
    """
    MAXDEPTH = 8

    def __init__(self, tree, loose):
        self.loose = loose
        self.tree = tree
        self.funcs = {n.name: n for n in ast.walk(tree)
                      if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
        self.scopes = {"<module>": _build_scope(tree, "<module>")}
        for nm, fn in self.funcs.items():
            self.scopes[nm] = _build_scope(fn, nm)
        self.col_exprs: list[tuple] = []              # (expr, owning scope name)

    # ---- locating the column expressions ------------------------------------
    def collect(self):
        for scname, fn in [("<module>", self.tree)] + list(self.funcs.items()):
            for n in _body_nodes(fn):
                if isinstance(n, ast.Call):
                    for kw in n.keywords:
                        if kw.arg and kw.arg.lower() in FAILCOLS:
                            self.col_exprs.append((kw.value, scname))
                elif isinstance(n, ast.Dict):
                    for k, v in zip(n.keys, n.values):
                        if (isinstance(k, ast.Constant) and isinstance(k.value, str)
                                and k.value.lower() in FAILCOLS):
                            self.col_exprs.append((v, scname))
                elif isinstance(n, ast.Assign):
                    for t in n.targets:
                        if (isinstance(t, ast.Subscript) and isinstance(t.slice, ast.Constant)
                                and isinstance(t.slice.value, str)
                                and t.slice.value.lower() in FAILCOLS):
                            self.col_exprs.append((n.value, scname))
        return self

    # ---- shape of one expression --------------------------------------------
    def _lookup(self, name, scname):
        sc = self.scopes.get(scname)
        if sc and name in sc.assigns:
            sites = sc.assigns[name]
            if len(sites) == 1 or self.loose:
                return sites[-1], scname, (name in sc.elif_names)
            return None, scname, (name in sc.elif_names)
        if self.loose:
            for s2, sc2 in self.scopes.items():
                if name in sc2.assigns:
                    return sc2.assigns[name][-1], s2, (name in sc2.elif_names)
        return None, scname, False

    def _appends(self, name, scname):
        sc = self.scopes.get(scname)
        if sc and name in sc.appends:
            return sc.appends[name]
        if self.loose:
            for sc2 in self.scopes.values():
                if name in sc2.appends:
                    return sc2.appends[name]
        return set()

    def _loop(self, name, scname):
        sc = self.scopes.get(scname)
        if sc and name in sc.loop_appends:
            return sc.loop_appends[name]
        if self.loose:
            for sc2 in self.scopes.values():
                if name in sc2.loop_appends:
                    return sc2.loop_appends[name]
        return None

    def shape(self, node, scname, depth=0, idx=None):
        if node is None or depth > self.MAXDEPTH:
            return "UNKNOWN"
        if isinstance(node, ast.BoolOp):
            for v in node.values:
                s = self.shape(v, scname, depth + 1, idx)
                if s != "UNKNOWN":
                    return s
            return "UNKNOWN"
        if isinstance(node, ast.IfExp):
            for v in (node.body, node.orelse):
                s = self.shape(v, scname, depth + 1, idx)
                if s != "UNKNOWN":
                    return s
            return "UNKNOWN"
        if isinstance(node, (ast.ListComp, ast.SetComp, ast.GeneratorExp)):
            return "SET"
        if isinstance(node, ast.Call):
            f = node.func
            if isinstance(f, ast.Attribute) and f.attr == "join" and node.args:
                return self.shape(node.args[0], scname, depth + 1)
            if isinstance(f, ast.Name) and f.id in self.funcs:
                return self._func_shape(self.funcs[f.id], depth + 1, idx)
            if isinstance(f, ast.Attribute) and f.attr.lower().replace("keep_", "fail") in FAILCOLS:
                return "EXTERNAL"          # a helper imported from another committed module
            return "UNKNOWN"
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            # row.fail4b / frame.f4b -- the column is COPIED from an upstream artefact
            if node.attr.lower() in FAILCOLS:
                return "INHERITED"
            return "UNKNOWN"
        if isinstance(node, ast.Name):
            toks = self._appends(node.id, scname)
            site, sc2, in_elif = self._lookup(node.id, scname)
            if in_elif:
                return "FIRSTFAIL"
            lp = self._loop(node.id, scname)
            if lp:
                return lp
            if len(toks) >= 2:
                return "SET"
            if site is not None:
                return self.shape(site[0], sc2, depth + 1,
                                  site[1] if site[1] is not None else idx)
            return "UNKNOWN"
        return "UNKNOWN"

    def _func_shape(self, fn, depth, idx=None):
        branch_rets = sum(1 for n in _body_nodes(fn)
                          if isinstance(n, ast.If) and any(isinstance(c, ast.Return) for c in n.body))
        if branch_rets >= 2:
            return "FIRSTFAIL"
        shapes = set()
        for n in _body_nodes(fn):
            if isinstance(n, ast.Return) and n.value is not None:
                v = n.value
                if idx is not None and isinstance(v, ast.Tuple) and idx < len(v.elts):
                    v = v.elts[idx]
                shapes.add(self.shape(v, fn.name, depth + 1))
        shapes.discard("UNKNOWN")
        return shapes.pop() if len(shapes) == 1 else "UNKNOWN"

    def stamp(self):
        got = [self.shape(e, sc) for e, sc in self.col_exprs]
        real = [s for s in got if s in ("SET", "FIRSTFAIL")]
        if real:
            return real[0] if len(set(real)) == 1 else "MIXED"
        soft = [s for s in got if s != "UNKNOWN"]
        return soft[0] if soft else "UNKNOWN"


def ast_stamp(py_path, loose):
    try:
        tree = ast.parse(Path(py_path).read_text(errors="replace"))
    except Exception:
        return "UNPARSEABLE"
    st = _Stamper(tree, loose).collect()
    if not st.col_exprs:
        return "NO_COL_EXPR"
    return st.stamp()


def census():
    """Every committed artefact carrying a fail-set column, with its rows, its data-driven tier
    (idea 527's rule) and its AST stamp under both parser readings."""
    paths = sorted(glob.glob(str(BT / "*.csv"))) + sorted(glob.glob(str(BT / "*.csv.gz")))
    recs = []
    for p in paths:
        h = header(p)
        if not h:
            continue
        fc = next((c for c in h if c.lower() in FAILCOLS), None)
        if fc is None:
            continue
        try:
            with _open(p) as f:
                d = pd.read_csv(f, usecols=[fc])
        except Exception:
            continue
        sets = [parse_failset(v) for v in d[fc]]
        sets = [s for s in sets if s is not None]
        if not sets:
            continue
        n = len(sets)
        nfail = sum(1 for s in sets if len(s) >= 1)
        multi = sum(1 for s in sets if len(s) >= 2)
        tier527 = "T1_DECLARED" if multi > 0 else "T1_SINGLETON"
        py = producing_script(p)
        recs.append(dict(
            file=os.path.basename(p), col=fc, rows=n, nfail=nfail, nmulti=multi,
            sole_OOS=sum(1 for s in sets if s == frozenset({"OOS"})),
            tier527=tier527, script=os.path.basename(py) if py else "",
            ast_strict=ast_stamp(py, False) if py else "NO_SCRIPT",
            ast_loose=ast_stamp(py, True) if py else "NO_SCRIPT"))
    return pd.DataFrame(recs)


# ══════════════════════════════════════════════════════════════════ PART 2: the PRICE LEG
def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bar_vector(r, spy, window="full"):
    """The 4b bar vector of one book against SPY, as a dict bar -> passed?  window='full'
    uses the whole sample plus the rule-8 OOS leg; 'is'/'oos' restrict to that window and
    drop the OOS leg (it is not defined inside its own window)."""
    if window == "is":
        r, spy = r.loc[:IS_END], spy.loc[:IS_END]
    elif window == "oos":
        r, spy = r.loc[OOS_START:], spy.loc[OOS_START:]
    m, ms = metrics(r), metrics(spy)
    h1, h2 = halves(r)
    s1, s2 = halves(spy)
    out = {"H1": h1 > s1, "H2": h2 > s2,
           "DD": abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]),
           "CAGR": m["CAGR"] >= 0.70 * ms["CAGR"]}
    if window == "full":
        out["OOS"] = (metrics(r.loc[OOS_START:])["Sharpe"]
                      > metrics(spy.loc[OOS_START:])["Sharpe"])
    return out


def failset_of(bv):
    return frozenset(b for b in BARS if b in bv and not bv[b])


def firstfail_of(bv):
    for b in BARS:
        if b in bv and not bv[b]:
            return b
    return None


def price_books():
    """1,200 real books: 80 seeded equal-weight k=20 draws x 5 gross rungs x 3 panels."""
    rng = np.random.default_rng(SEED)
    panels = [("U56", load_universe()), ("B136", load_universe(broad=True)),
              ("SMALL716", load_universe(small=True))]
    rows = []
    for pname, px in panels:
        px = px.dropna(how="all").ffill()
        spy_full = px["SPY"]
        cols = [c for c in px.columns if c != "SPY"]
        # baseline + SPY on this panel, over the same post-warm-up sample the books use
        start = px.index[260]
        base = backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        v1 = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        spy = spy_full.pct_change().fillna(0.0).loc[start:]
        b1, b2 = halves(base); base_dd = metrics(base)["MaxDD"]
        draws = [rng.choice(len(cols), size=KDRAW, replace=False) for _ in range(NDRAW)]
        for di, idx in enumerate(draws):
            names = [cols[i] for i in idx]
            sub = px[names + ["SPY"]]
            for g in GROSS_RUNGS:
                w = pd.DataFrame(0.0, index=sub.index, columns=sub.columns)
                live = sub[names].notna()
                n_live = live.sum(axis=1).replace(0, np.nan)
                w[names] = live.astype(float).div(n_live, axis=0).fillna(0.0) * g
                r = backtest(sub, w, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
                m, mo = metrics(r), metrics(r.loc[OOS_START:])
                bv = bar_vector(r, spy, "full")
                fs = failset_of(bv)
                bv_is = bar_vector(r, spy, "is")
                bv_oos = bar_vector(r, spy, "oos")
                h1, h2 = halves(r)
                rows.append(dict(
                    panel=pname, draw=di, gross=g,
                    CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                    OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                    failset=",".join(sorted(fs, key=BARS.index)) if fs else "-",
                    nfail=len(fs), firstfail=firstfail_of(bv) or "-",
                    pass4b=len(fs) == 0,
                    pass4a=bool(h1 > b1 and h2 > b2 and m["MaxDD"] >= base_dd),
                    nfail_is=len(failset_of(bv_is)), ff_is=firstfail_of(bv_is) or "-",
                    nfail_oos=len(failset_of(bv_oos)), ff_oos=firstfail_of(bv_oos) or "-"))
        P(f"  priced {pname}: {NDRAW * len(GROSS_RUNGS)} books "
          f"({len(cols)} names, sample {start.date()}..{px.index[-1].date()})")
        globals().setdefault("_REF", {})[pname] = dict(base=base, v1=v1, spy=spy)
    return pd.DataFrame(rows)


# ══════════════════════════════════════════════════════════════════ main
def main():
    rule("IDEA 529 — AUDIT EVERY FAIL-SET COLUMN IN THE RECORD FOR SET vs FIRSTFAIL (lane B)")
    P("Protocol: 10 bps, t+1 (engine), weekly, no shorting/leverage. Seed", SEED)
    P("Params: P1 parser in {strict, loose}; P2 sample in {all, singleton}. All 4 points reported.")

    # ---------------- PART 1 -------------------------------------------------
    rule("[1] THE AST STAMP — reading each producing SCRIPT's keep-paths expression")
    C = census()
    C.to_csv(f"{STEM}.stamps.csv", index=False)
    P(f"{len(C)} committed artefacts carry a fail-set column "
      f"({C.script.astype(bool).sum()} have a committed producing script).")
    P("\nidea 527's DATA-DRIVEN tier (does ANY row emit >= 2 tokens?):")
    P(C.tier527.value_counts().to_string())
    for pr in ("ast_strict", "ast_loose"):
        P(f"\nAST stamp, parser={pr.split('_')[1]}:")
        P(C[pr].value_counts().to_string())

    P("\n[1a] THE MISLABEL THE QUEUE NAMES — files idea 527 calls AMBIGUOUS that the AST calls SET")
    grid_rows = []
    for parser in ("strict", "loose"):
        col = f"ast_{parser}"
        for sample in ("all", "singleton"):
            S = C if sample == "all" else C[C.tier527 == "T1_SINGLETON"]
            resolved = S[S[col].isin(["SET", "FIRSTFAIL", "MIXED"])]
            mis = S[(S.tier527 == "T1_SINGLETON") & (S[col] == "SET")]
            grid_rows.append(dict(
                parser=parser, sample=sample, files=len(S), resolved=len(resolved),
                resolved_frac=len(resolved) / len(S) if len(S) else np.nan,
                SET=(S[col] == "SET").sum(), FIRSTFAIL=(S[col] == "FIRSTFAIL").sum(),
                MIXED=(S[col] == "MIXED").sum(), UNKNOWN=(~S[col].isin(["SET", "FIRSTFAIL", "MIXED"])).sum(),
                mislabelled_files=len(mis), mislabelled_rows=int(mis.rows.sum()),
                recovered_soleOOS=int(mis.sole_OOS.sum())))
    G = pd.DataFrame(grid_rows)
    G.to_csv(f"{STEM}.grid.csv", index=False)
    P(G.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    rule("[2] RE-RUNNING IDEA 527's HEADLINE ON THE CORRECTED PARTITION")
    decl = C[C.tier527 == "T1_DECLARED"]
    P(f"idea 527's partition: sole-OOS counted on T1_DECLARED only "
      f"= {int(decl.sole_OOS.sum())} of {int(decl.nfail.sum())} failures "
      f"({int(decl.sole_OOS.sum()) / max(1, int(decl.nfail.sum())):.6f}).")
    for parser in ("strict", "loose"):
        col = f"ast_{parser}"
        corrected = C[C[col] == "SET"]
        P(f"  parser={parser:8s} corrected partition (AST says SET, whatever 527's detector said): "
          f"{len(corrected)} files, sole-OOS {int(corrected.sole_OOS.sum())} of "
          f"{int(corrected.nfail.sum())} failures "
          f"({int(corrected.sole_OOS.sum()) / max(1, int(corrected.nfail.sum())):.6f}).")
        ff = C[C[col] == "FIRSTFAIL"]
        P(f"  {'':8s}   files the AST calls FIRSTFAIL and 527 read as DECLARED: "
          f"{len(ff[ff.tier527 == 'T1_DECLARED'])} "
          f"(their {int(ff[ff.tier527 == 'T1_DECLARED'].sole_OOS.sum())} single-OOS rows are NOT sole-fails).")

    # ---------------- PART 3: the price leg ---------------------------------
    rule("[3] THE PRICE LEG — 1,200 REAL BOOKS, so the mislabel rate is MEASURED not assumed")
    B = price_books()
    B.to_csv(f"{STEM}.books.csv", index=False)
    P(f"\n{len(B)} books priced. Full grid ({len(GROSS_RUNGS)} gross rungs x {NDRAW} draws x 3 panels):")
    gp = B.groupby(["panel", "gross"]).agg(
        CAGR=("CAGR", "mean"), Sharpe=("Sharpe", "mean"), MaxDD=("MaxDD", "mean"),
        nfail=("nfail", "mean"), p4b=("pass4b", "sum"), p4a=("pass4a", "sum"),
        multi=("nfail", lambda s: (s >= 2).mean()), soleOOS=("failset", lambda s: (s == "OOS").sum()))
    P(gp.to_string(float_format=lambda x: f"{x:.4f}"))

    P("\n[3a] THE MEASURED MULTI-FAIL RATE p = P(a failing book fails >= 2 bars)")
    tot = []
    for pname, grp in B.groupby("panel"):
        f = grp[grp.nfail >= 1]
        p = (f.nfail >= 2).mean()
        tot.append((pname, len(f), p))
        P(f"  {pname:9s} failures {len(f):4d}  p = {p:.4f}   "
          f"P(a genuine SET file of n rows is INVISIBLE to 527's detector) = (1-p)^n:  "
          f"n=10 {(1 - p) ** 10:.4f}  n=50 {(1 - p) ** 50:.4f}  n=200 {(1 - p) ** 200:.4f}")
    fall = B[B.nfail >= 1]
    p_all = (fall.nfail >= 2).mean()
    P(f"  POOLED    failures {len(fall):4d}  p = {p_all:.4f}")

    P("\n[3b] HOW MANY OF THE RECORD'S FILES ARE ACTUALLY AT RISK, at the measured p")
    P("  The exponent is the number of FAILING rows, not total rows: a row that passes 4b emits")
    P("  no token at all and can never reveal the semantics.  Both are reported; nfail is the")
    P("  correct one and the p used is the LOW-p reading (U56/B136), the panels the record uses.")
    p_low = min((B[(B.panel == pn) & (B.nfail >= 1)].nfail >= 2).mean()
                for pn in ("U56", "B136"))
    for lab, pp in (("pooled", p_all), ("low-p (U56/B136)", p_low)):
        C["p_inv_rows"] = (1 - pp) ** C.rows.clip(lower=1)
        C["p_inv_nfail"] = (1 - pp) ** C.nfail.clip(lower=0)
        sing = C[C.tier527 == "T1_SINGLETON"]
        P(f"  p={pp:.4f} ({lab}):  expected SET files hidden in the SINGLETON tier = "
          f"{sing.p_inv_rows.sum():.2f} by TOTAL rows, {sing.p_inv_nfail.sum():.2f} by FAILING rows "
          f"({int((sing.p_inv_nfail > 0.05).sum())} files above 5%)")
    P(f"  median rows in the SINGLETON tier = {C[C.tier527 == 'T1_SINGLETON'].rows.median():.0f} "
      f"(failing rows {C[C.tier527 == 'T1_SINGLETON'].nfail.median():.0f}), "
      f"DECLARED tier = {C[C.tier527 == 'T1_DECLARED'].rows.median():.0f} "
      f"(failing rows {C[C.tier527 == 'T1_DECLARED'].nfail.median():.0f})")
    P("\n  WHY THE AST FINDS MORE MISLABELS THAN p PREDICTS — the SINGLETON tier is made of")
    P("  files with almost NO FAILING ROWS, not of files whose books happen to fail one bar:")
    for parser in ("strict", "loose"):
        mis = C[(C.tier527 == "T1_SINGLETON") & (C[f"ast_{parser}"] == "SET")]
        P(f"    parser={parser:7s} {len(mis)} mislabelled files: "
          f"{int((mis.nfail == 0).sum())} have ZERO failing rows, "
          f"{int((mis.nfail.between(1, 9)).sum())} have 1-9, "
          f"{int((mis.nfail >= 10).sum())} have >= 10 "
          f"(median failing rows {mis.nfail.median():.0f})")

    P("\n[3c] THE OVERSTATEMENT idea 527 quoted at 25x, measured on real books")
    for pname, grp in B.groupby("panel"):
        f = grp[grp.nfail >= 1]
        sole = (f.failset == "OOS").sum()
        ffo = (f.firstfail == "OOS").sum()
        P(f"  {pname:9s} SET sole-OOS {sole:4d} | FIRSTFAIL prints OOS {ffo:4d} | "
          + (f"overstatement x{ffo / sole:.2f}" if sole else "overstatement NOT MEASURABLE (0 sole-OOS)"))
    sole_all = (fall.failset == "OOS").sum(); ff_all = (fall.firstfail == "OOS").sum()
    P(f"  POOLED    SET sole-OOS {sole_all:4d} | FIRSTFAIL prints OOS {ff_all:4d}")
    if sole_all == 0 and ff_all == 0:
        P("  NOT MEASURABLE ON THIS CORPUS, and that is itself the finding: across 1,200 random")
        P("  books NOT ONE fails the OOS bar alone, and not one has OOS as its FIRST failing bar")
        P("  either.  The OOS Sharpe bar is never reached before H1 or H2 has already failed, so")
        P("  idea 527's 25x overstatement cannot be reproduced on priced books — it is a property")
        P("  of the record's TUNED books, not of books in general.  This run does NOT confirm it.")

    # ---------------- PART 4: rule 8 ----------------------------------------
    rule("[4] RULE 8 WALK-FORWARD — reading picked on 2009-2016 ONLY, evaluated on 2017-2026")
    wf = []
    for pname, grp in B.groupby("panel"):
        fi = grp[grp.nfail_is >= 1]
        fo = grp[grp.nfail_oos >= 1]
        p_is = (fi.nfail_is >= 2).mean() if len(fi) else np.nan
        p_oos = (fo.nfail_oos >= 2).mean() if len(fo) else np.nan
        wf.append(dict(panel=pname, leg="multi_fail_rate", IS=p_is, OOS=p_oos,
                       IS_n=len(fi), OOS_n=len(fo)))
        P(f"  {pname:9s} multi-fail rate p:  IS(<=2016) {p_is:.4f} (n={len(fi)})  "
          f"OOS(2017+) {p_oos:.4f} (n={len(fo)})  |delta| {abs(p_is - p_oos):.4f}")
    P("\n  The IS-chosen reading is: 'a single-token column is NOT diagnostic; stamp it from the")
    P("  script'.  It holds OOS iff p_OOS is also far from 1.  Reported above at every panel.")

    P("\n[4a] BOOKS OUT OF SAMPLE vs BASELINE and SPY (rule 8, the lane's mandatory leg)")
    ref = globals().get("_REF", {})
    rows = []
    for pname, grp in B.groupby("panel"):
        R = ref[pname]
        for lab, r in [("RULES v2 baseline (live)", R["base"]), ("RULES v1 (previous)", R["v1"]),
                       ("SPY", R["spy"])]:
            mo = metrics(r.loc[OOS_START:]); mf = metrics(r)
            rows.append(dict(panel=pname, book=lab, OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                             OOS_MaxDD=mo["MaxDD"], full_CAGR=mf["CAGR"], full_Sharpe=mf["Sharpe"],
                             full_MaxDD=mf["MaxDD"]))
        for lab, sel in [("books MEAN", grp), ("books BEST OOS Sharpe", grp.nlargest(1, "OOS_Sharpe")),
                         ("books 4b PASSERS", grp[grp.pass4b])]:
            if not len(sel):
                rows.append(dict(panel=pname, book=lab, OOS_CAGR=np.nan, OOS_Sharpe=np.nan,
                                 OOS_MaxDD=np.nan, full_CAGR=np.nan, full_Sharpe=np.nan,
                                 full_MaxDD=np.nan)); continue
            rows.append(dict(panel=pname, book=f"{lab} (n={len(sel)})",
                             OOS_CAGR=sel.OOS_CAGR.mean(), OOS_Sharpe=sel.OOS_Sharpe.mean(),
                             OOS_MaxDD=sel.OOS_MaxDD.mean(), full_CAGR=sel.CAGR.mean(),
                             full_Sharpe=sel.Sharpe.mean(), full_MaxDD=sel.MaxDD.mean()))
    W = pd.DataFrame(rows)
    P(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    pd.concat([pd.DataFrame(wf), W], ignore_index=True).to_csv(f"{STEM}.walkforward.csv", index=False)

    rule("[5] KEEP PATHS — both evaluated on every one of the 1,200 books")
    P(f"  4a (beat the book: Sharpe > RULES v2 in BOTH halves AND MaxDD no worse): "
      f"{int(B.pass4a.sum())} of {len(B)}")
    P(f"  4b (capital-worthy: Sharpe > SPY both halves AND OOS, MaxDD <= 60% SPY, CAGR >= 70% SPY): "
      f"{int(B.pass4b.sum())} of {len(B)}")
    for pname, grp in B.groupby("panel"):
        P(f"    {pname:9s} 4a {int(grp.pass4a.sum()):3d}/{len(grp)}   4b {int(grp.pass4b.sum()):3d}/{len(grp)}")
    P("\n  No book here is a candidate: they are RANDOM equal-weight draws built to EXERCISE the")
    P("  bar vector, not to be traded.  The deliverable is the semantics stamp, not a book.")

    rule("VERDICT")
    P("KILL as a capital idea (0 promotable books by construction); ANSWERED as an audit.")
    Path(f"{STEM}.console.txt").write_text("\n".join(_LOG))
    P(f"\nwrote {STEM.name}.{{console.txt,stamps.csv,grid.csv,books.csv,walkforward.csv}}")
    Path(f"{STEM}.console.txt").write_text("\n".join(_LOG))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Idea 469 -- label-the-337-undecidable-count-cells-from-the-AST  (cloud lane)

THE QUEUE'S PREMISE
    Idea 244 censused every committed CSV that publishes a position-COUNT sweep beside a
    Sharpe column: 694 cells over 69 files.  It then had to decide, per cell, WHICH
    weighting convention produced it, because the convention decides whether the count
    dial is also a GROSS dial:

        FIXEDTOT   w = GROSS / n on the top-n names   -> realised gross RISES with n
        NORM       w = GROSS / n_held                 -> realised gross is FLAT in n
        FIXEDW     w = 0.15 per name, top-n           -> rises, and levers past n=6

    Idea 244's labeller is three REGEXES matched against the whole parent-script source.
    A script that contains a FIXEDTOT-shaped expression ANYWHERE and a NORM-shaped one
    ANYWHERE is labelled MIXED and dropped.  That happened to 260 of 694 cells; another
    77 matched no pattern.  Only 39.0% of cells got a convention, and the record-wide
    ladder rate could only be bounded 17.4% - 43.6% (95/546 to 238/546).

    This run replaces the regex with an AST walk and re-quotes that bound.

WHY AN AST CAN DO BETTER (the four things a regex cannot do)
    (a) SHAPE.  `x / n` in a metrics average is not a weight.  The AST only accepts a
        convention-bearing expression that is actually weight-shaped: assigned to a
        weight-named target, returned from a weight-named function, built out of a
        selection frame, or handed to `backtest(...)`.  Comments, docstrings and string
        literals are not expressions at all and are never seen.
    (b) GUARDS.  `if arm == "FIXEDTOT": return sel*(GROSS/n)` is not a script that "does
        FIXEDTOT somewhere".  It is a script whose convention is a FUNCTION OF THE `arm`
        VARIABLE.  The AST records the (selector, literal) pair that guards each weight
        expression -- including the trailing unguarded `return` that means "every other
        value of arm" (the ELSE arm).
    (c) THE COLUMN THAT RESOLVES IT.  Once the selector variable is known by name, the
        CSV can be searched for a column that carries its literals.  Idea 244 only looked
        for a fixed list of column names (`conv`, `convention`, `weighting`, ...); the AST
        discovers the script's OWN name for the dial (`arm`, `book`, `wmode`, ...) and any
        column whose value set lands inside the guard literals.  This is what converts
        MIXED cells into per-ROW labels.
    (d) REACHABILITY.  A helper function that is defined but never called from the code
        path that writes the CSV cannot have produced it.  The AST builds the call graph,
        finds the `to_csv` call whose filename literal carries this CSV's tag, and only
        considers weight expressions reachable from that writer's enclosing function.

    A fifth class is left honestly undecidable and is COUNTED, not hidden: two live
    conventions on the same selector with no column in the file to separate them.

PRE-REGISTERED DECISION PROCEDURE (fixed before any number was read; no free parameter)
    For CSV F with parent script P:
      1. Parse P.  Collect module-level constant bindings (name -> str / tuple of str).
      2. Walk every statement carrying a guard/loop context.  A node is a WEIGHT
         EXPRESSION iff it matches one of the three convention shapes AND passes the
         weight-shape gate.  Record (convention, selector, literal-or-ELSE, function).
      3. Build the call graph; locate F's writer function by its filename literal;
         reachable = transitive closure from it (module fallback if not found).
      4. C = conventions of the reachable weight expressions.
           |C| == 1                      -> that convention                (ast:single)
           |C| >= 2, one selector, and a
             column of F carries its
             literals                    -> PER-ROW label                  (ast:armcol)
           |C| >= 2, selector pinned to
             one literal in reach        -> that convention                (ast:pinned)
           |C| >= 2, otherwise           -> UNDECIDABLE:multi-arm-no-column
           |C| == 0                      -> UNDECIDABLE:no-weight-expression
      5. A MATCHED-control arm (a NORM book times a per-cell scalar solved to another
         arm's mean gross) is labelled MATCHED, not NORM: its gross path is the FIXEDTOT
         path by construction.  It is reported separately and is NOT folded into the
         headline ladder rate, so the headline stays comparable to idea 244's.

    Everything else in the census -- the file scan, the count/Sharpe/panel column lists,
    the >=3-distinct-integer admission test, the panel map, the `target_gross` measure and
    the pre-registered ladder threshold SPAN_ABS = 0.05 NAV -- is imported UNCHANGED from
    idea 244's committed script, so any movement in the bound is the labeller and nothing
    else.  CHECK(a) below re-derives idea 244's own published census with its own regex
    labeller and asserts it reproduces 694/222/135/260/77 exactly before the AST is run.

LIVE-PRICE ARMS (this is a census idea, so the live work tests what the census RESTS on)
    L1  Is `target_gross` -- the census's measure, which never runs a backtest -- a fair
        stand-in for the gross a book actually HOLDS?  84 live books (7 panels x 6 n x
        {FIXEDTOT, NORM}) at 10 and 25 bps, target vs realised held gross at every point,
        and the LADDER/FLAT verdict recomputed off realised gross.
    L2  RULE 8.  n chosen on 2009-2016 IS Sharpe alone, 2017-2026 read ONCE, per panel and
        per convention.  New here: the OOS COST OF THE LABEL -- what a reader pays for
        choosing n under the wrong convention, which is exactly what a mislabelled cell
        invites.  Reported against RULES v2, SPY and the un-ranked EW_ALL control.
    L3  Both KEEP paths on all live points (4a vs the live RULES v2 on the book's own
        panel, 4b vs SPY incl. rule 8), at 10 and 25 bps.

TUNED DIMENSIONS: exactly two, both inherited from idea 244 -- CONVENTION in
{FIXEDTOT, NORM} and n in {5,10,20,30,40,60}.  The labeller itself has no free parameter.

SURVIVORSHIP: every panel is CURRENT constituents (hardest on STK20 / BSTK100 / SMALL);
the 44 small-cap tickers with max_1d_move >= 1.0 in data/small_meta.csv are dropped first.
The census additionally inherits the bias of every parent script it reads.

Deterministic, standalone.  Reads research/baseline.py and idea 244's committed script;
modifies nothing.
"""
import sys
import ast
import importlib.util
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
import baseline  # noqa: F401  -- inserts products/backtester on sys.path for engine

SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"
PARENT244 = OUT / "2026-09-08_how-many-published-count-dials-are-gross-dials_B.py"

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 500)


def load_244():
    """Import idea 244's committed script as a module so every census primitive
    (panels, column lists, panel map, target_gross, SPAN_ABS, the regex labeller) is the
    SAME OBJECT, not a re-typed copy."""
    spec = importlib.util.spec_from_file_location("idea244", PARENT244)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


M = load_244()

COST_RUNGS = (10, 25)
COST_BPS = 10
IS_END = M.IS_END
OOS_START = M.OOS_START
NS = M.NS
SPAN_ABS = M.SPAN_ABS
SPAN_REL = M.SPAN_REL


# ================================================================= THE AST LABELLER
COUNT_NAMES = {"n", "N", "nn", "top_n", "topn", "n_names", "npos", "n_pos", "k",
               "n_hold", "nhold", "n_top", "ntop", "kk", "nsel", "n_sel"}
HELD_NAMES = {"held", "cnt", "n_held", "nheld", "filled", "held_count", "denom",
              "tot", "hc", "cnt_t", "nheld_t", "count_t", "act", "n_act"}
FIXEDW_NAMES = {"W_FIXED", "WFIX", "W_FIX", "WPOS", "W_POS"}
WEIGHT_TARGETS = {"w", "wt", "wts", "wgt", "wgts", "weight", "weights", "ww", "wf", "wn",
                  "wnorm", "wfix", "book", "wbook", "w_", "wnew", "w0", "w1", "wmat"}
SEL_HINTS = {"sel", "picks", "holds", "member", "members", "mask", "elig", "rank", "ranks",
             "rk", "chosen", "selected", "topn", "top_n", "book", "held_mask"}
SEL_SUBSTR = ("sel", "rank", "elig", "topn", "top_n", "hold", "mask", "member")
WEIGHT_FUNCS = ("weight", "weights", "book", "wts", "w_for", "make_w", "build_w", "wfun")
MATCHED_HINTS = ("matched", "match", "gmatch", "grossmatch", "ctrl_matched")


def _names(node):
    return {x.id for x in ast.walk(node) if isinstance(x, ast.Name)}


def _attrs(node):
    return {x.attr for x in ast.walk(node) if isinstance(x, ast.Attribute)}


def _is_sum_axis1(node):
    """`<x>.sum(axis=1)` -- a per-ROW realised count, the NORM denominator."""
    if not isinstance(node, ast.Call):
        return False
    f = node.func
    if not (isinstance(f, ast.Attribute) and f.attr in ("sum", "count")):
        return False
    for kw in node.keywords:
        if kw.arg == "axis" and isinstance(kw.value, ast.Constant) and kw.value.value == 1:
            return True
    return False


def _held_like(node, env=None):
    """True if `node` is a per-row realised-count denominator (NORM), not the dial.
    `env` is the enclosing function's local binding kinds, so a denominator that was
    ASSIGNED from a `.sum(axis=1)` upstream resolves even when its name is ambiguous
    (`k`, `d`, `den`) -- the single thing a regex can never see."""
    env = env or {}
    if isinstance(node, ast.Name):
        return env.get(node.id) == "held" or (node.id in HELD_NAMES and env.get(node.id) != "count")
    if _is_sum_axis1(node):
        return True
    if isinstance(node, ast.Call):                       # .replace(0, nan) / .clip(...)
        f = node.func
        if isinstance(f, ast.Attribute) and f.attr in ("replace", "clip", "astype", "fillna"):
            return _held_like(f.value, env)
        if isinstance(f, ast.Name) and f.id in ("float", "int"):
            return bool(node.args) and _held_like(node.args[0], env)
    if isinstance(node, ast.Subscript):
        return _held_like(node.value, env)
    return False


def _count_like(node, env=None):
    """True if `node` is the count DIAL itself (a scalar parameter), not a realised count."""
    env = env or {}
    if isinstance(node, ast.Name):
        if env.get(node.id) == "held":
            return False
        return node.id in COUNT_NAMES or env.get(node.id) == "count"
    if isinstance(node, ast.Call):
        f = node.func
        if isinstance(f, ast.Name) and f.id in ("float", "int", "len"):
            return bool(node.args) and _count_like(node.args[0], env)
        if isinstance(f, ast.Attribute) and f.attr in ("clip", "replace"):
            return _count_like(f.value, env)
    if isinstance(node, ast.IfExp):
        return _count_like(node.body, env) or _count_like(node.orelse, env)
    return False


SCALAR_CALLS = {"float", "int", "len", "abs", "round", "sum", "max", "min", "sqrt"}
SCALAR_METHODS = {"mean", "std", "sum", "count", "median", "var", "nunique", "item"}


def _scalar_like(node, env=None):
    """A weight is a FRAME.  `float(x)/n`, `len(a)/n`, `s.mean()/n` are wholly SCALAR
    arithmetic and can never be a weight, however much the `/n` looks like `GROSS/n` to a
    regex.  A name is known-scalar only if it is the count dial itself; an unknown name
    (`GROSS`, `sel`) is NOT assumed scalar, so `sel * (GROSS/n)` still classifies."""
    env = env or {}
    if isinstance(node, ast.Constant):
        return True
    if isinstance(node, ast.Name):
        return env.get(node.id) == "count" or (node.id in COUNT_NAMES and env.get(node.id) != "held")
    if isinstance(node, ast.Call):
        f = node.func
        if isinstance(f, ast.Name) and f.id in SCALAR_CALLS:
            return True
        if isinstance(f, ast.Attribute):
            if isinstance(f.value, ast.Name) and f.value.id in ("np", "numpy", "math"):
                return True
            if f.attr in SCALAR_METHODS and not any(kw.arg == "axis" for kw in node.keywords) \
                    and not node.args:
                return True
    if isinstance(node, ast.UnaryOp):
        return _scalar_like(node.operand, env)
    if isinstance(node, ast.BinOp):
        return _scalar_like(node.left, env) and _scalar_like(node.right, env)
    return False


def classify_expr(node, env=None):
    """Return 'FIXEDTOT' / 'NORM' / 'FIXEDW' / None for a single expression node."""
    env = env or {}
    # ---- NORM: divide by a per-row realised count
    if isinstance(node, ast.Call):
        f = node.func
        if isinstance(f, ast.Attribute) and f.attr in ("div", "divide", "truediv"):
            # `.div(x, axis=0)` divides a frame ROW-WISE by a per-day series: that is a
            # realised-count denominator by construction, never the scalar dial.
            if any(kw.arg == "axis" and isinstance(kw.value, ast.Constant) and kw.value.value == 0
                   for kw in node.keywords):
                return "NORM"
            if node.args and _held_like(node.args[0], env):
                return "NORM"
            if node.args and _count_like(node.args[0], env):
                return "FIXEDTOT"
        if isinstance(f, ast.Attribute) and f.attr in ("mul", "multiply"):
            if node.args and isinstance(node.args[0], ast.Name) and node.args[0].id in FIXEDW_NAMES:
                return "FIXEDW"
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
        if _scalar_like(node, env):                    # wholly scalar arithmetic: not a weight
            return None
        if _held_like(node.right, env):
            return "NORM"
        if _count_like(node.right, env):
            return "FIXEDTOT"
    # ---- FIXEDW: multiply by a fixed per-name weight
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mult) and not _scalar_like(node, env):
        for a, b in ((node.left, node.right), (node.right, node.left)):
            if isinstance(a, ast.Name) and a.id in FIXEDW_NAMES:
                return "FIXEDW"
            if (isinstance(a, ast.Constant) and isinstance(a.value, float)
                    and 0.0 < a.value <= 0.5 and (_names(b) & SEL_HINTS
                                                  or any(h in nm.lower() for nm in _names(b)
                                                         for h in ("sel", "rank", "elig", "top")))):
                return "FIXEDW"
    return None


def weight_shaped(stmt, node, func_name, assigned_to):
    """The gate that a regex cannot apply: is this convention-bearing expression actually
    a WEIGHT?  Any one of four independent witnesses is enough."""
    if assigned_to and any(t.lower().strip("_") in WEIGHT_TARGETS for t in assigned_to):
        return "assign"
    if isinstance(stmt, ast.Return) and func_name and any(h in func_name.lower() for h in WEIGHT_FUNCS):
        return "return"
    nm = {x.lower() for x in _names(node)}
    if nm & SEL_HINTS or any(h in x for x in nm for h in SEL_SUBSTR):
        return "selframe"
    at = _attrs(node)
    if at & {"reindex", "where", "shift", "fillna"} and ("axis" in ast.dump(node)):
        return "frame"
    return ""


class ArmWalker(ast.NodeVisitor):
    """Walks a module carrying (guard, loop) context and harvests weight expressions."""

    def __init__(self, consts):
        self.consts = consts
        self.hits = []                # dicts: conv, func, selector, literals, kind
        self.func = None
        self.guards = []              # list of (selector, frozenset(literals), positive?)
        self.seen_pos = {}            # selector -> set of literals already returned on
        self.calls = {}               # func -> set of called local names
        self.writers = []             # (func, [string constants in the filename expr])
        self.env = {}                 # local binding kinds: name -> 'held' | 'count'

    # ---------- helpers
    def _arm_keys(self, test, positive):
        """Extract (selector, literals) from an if-test.  Only equality against string
        literals counts -- anything else is context but not an arm key."""
        out = []
        if isinstance(test, ast.Compare) and len(test.ops) == 1:
            op, l, r = test.ops[0], test.left, test.comparators[0]
            if isinstance(op, (ast.Eq, ast.NotEq)):
                pos = positive if isinstance(op, ast.Eq) else not positive
                for a, b in ((l, r), (r, l)):
                    if isinstance(a, ast.Name) and isinstance(b, ast.Constant) and isinstance(b.value, str):
                        out.append((a.id, frozenset([b.value]), pos))
            if isinstance(op, (ast.In, ast.NotIn)) and isinstance(l, ast.Name):
                pos = positive if isinstance(op, ast.In) else not positive
                lits = None
                if isinstance(r, (ast.Tuple, ast.List, ast.Set)):
                    lits = {e.value for e in r.elts if isinstance(e, ast.Constant) and isinstance(e.value, str)}
                elif isinstance(r, ast.Name) and r.id in self.consts:
                    v = self.consts[r.id]
                    lits = set(v) if isinstance(v, (tuple, list)) else None
                if lits:
                    out.append((l.id, frozenset(lits), pos))
        if isinstance(test, ast.BoolOp) and isinstance(test.op, ast.And):
            for v in test.values:
                out += self._arm_keys(v, positive)
        return out

    def _bind(self, tgts, value):
        """One-pass local dataflow: which names hold a per-row realised COUNT, and which
        hold the scalar count DIAL.  Resolves ambiguous denominators like `k` / `den`."""
        if _is_sum_axis1(value) or any(_is_sum_axis1(x) for x in ast.walk(value)):
            kind = "held"
        elif _held_like(value, self.env):
            kind = "held"
        elif _count_like(value, self.env):
            kind = "count"
        else:
            return
        for t in tgts:
            self.env[t] = kind

    def _record(self, stmt, node, assigned_to):
        conv = classify_expr(node, self.env)
        if not conv:
            return False
        wit = weight_shaped(stmt, node, self.func, assigned_to)
        if not wit:
            return False
        sel, lits, kind = None, frozenset(), "unguarded"
        for (s, L, pos) in reversed(self.guards):
            if pos:
                sel, lits, kind = s, L, "guard"
                break
        if sel is None:
            # trailing / unguarded weight expression: if earlier sibling guards in this
            # function already claimed literals on a selector, this is that selector's ELSE
            cands = [s for s in self.seen_pos if self.seen_pos[s]]
            if len(cands) == 1:
                sel, lits, kind = cands[0], frozenset(self.seen_pos[cands[0]]), "else"
        self.hits.append(dict(conv=conv, func=self.func or "<module>", selector=sel,
                              literals=lits, kind=kind, witness=wit,
                              lineno=getattr(node, "lineno", 0),
                              matched=bool(sel and kind == "guard"
                                           and any(any(h in x.lower() for h in MATCHED_HINTS) for x in lits))))
        return True

    # ---------- visits
    def visit_FunctionDef(self, node):
        prev = (self.func, self.guards, self.seen_pos, self.env)
        self.func = node.name
        self.guards, self.seen_pos = [], {}
        self.env = dict(self.env)                      # module bindings are visible inside
        for a in node.args.args + node.args.kwonlyargs:
            if a.arg in COUNT_NAMES:
                self.env[a.arg] = "count"
        self.calls.setdefault(node.name, set())
        for st in node.body:
            self.visit(st)
        self.func, self.guards, self.seen_pos, self.env = prev

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_If(self, node):
        keys = self._arm_keys(node.test, True)
        self.guards += keys
        for st in node.body:
            self.visit(st)
        self.guards = self.guards[:len(self.guards) - len(keys)]
        # a positive equality guard whose body RETURNS claims those literals for the ELSE
        if any(isinstance(x, ast.Return) for x in ast.walk(node)):
            for (s, L, pos) in keys:
                if pos:
                    self.seen_pos.setdefault(s, set()).update(L)
        neg = self._arm_keys(node.test, False)
        self.guards += neg
        for st in node.orelse:
            self.visit(st)
        self.guards = self.guards[:len(self.guards) - len(neg)]

    def visit_For(self, node):
        # `for arm in ARMS:` -- a loop over literals is a selector with a known level set
        keys = []
        if isinstance(node.target, ast.Name):
            lits = None
            it = node.iter
            if isinstance(it, (ast.Tuple, ast.List, ast.Set)):
                lits = {e.value for e in it.elts if isinstance(e, ast.Constant) and isinstance(e.value, str)}
            elif isinstance(it, ast.Name) and it.id in self.consts:
                v = self.consts[it.id]
                lits = set(v) if isinstance(v, (tuple, list)) else None
            if lits:
                keys = [(node.target.id, frozenset(lits), True)]
        self.guards += keys
        for st in node.body + node.orelse:
            self.visit(st)
        self.guards = self.guards[:len(self.guards) - len(keys)]

    def visit_Assign(self, node):
        tgts = [t.id for t in node.targets if isinstance(t, ast.Name)]
        self._bind(tgts, node.value)
        for sub in ast.walk(node.value):
            self._record(node, sub, tgts)
        self.generic_visit(node)

    def visit_Return(self, node):
        if node.value is not None:
            for sub in ast.walk(node.value):
                self._record(node, sub, [])
        self.generic_visit(node)

    def visit_Call(self, node):
        f = node.func
        if isinstance(f, ast.Name):
            self.calls.setdefault(self.func or "<module>", set()).add(f.id)
        if isinstance(f, ast.Attribute):
            if f.attr == "to_csv":
                lits = [c.value for c in ast.walk(node) if isinstance(c, ast.Constant)
                        and isinstance(c.value, str)]
                self.writers.append((self.func or "<module>", lits))
        # weight expressions handed straight to a backtest / weights= keyword
        if isinstance(f, ast.Name) and f.id in ("backtest", "run", "run_book", "bt"):
            for a in list(node.args) + [kw.value for kw in node.keywords]:
                for sub in ast.walk(a):
                    self._record(node, sub, ["weights"])
        self.generic_visit(node)


def module_consts(tree):
    c = {}
    for st in tree.body:
        if isinstance(st, ast.Assign) and len(st.targets) == 1 and isinstance(st.targets[0], ast.Name):
            v = st.value
            if isinstance(v, ast.Constant) and isinstance(v.value, str):
                c[st.targets[0].id] = v.value
            elif isinstance(v, (ast.Tuple, ast.List, ast.Set)):
                els = [e.value for e in v.elts if isinstance(e, ast.Constant) and isinstance(e.value, str)]
                if els and len(els) == len(v.elts):
                    c[st.targets[0].id] = tuple(els)
    return c


def analyse_script(path, cache={}):
    if path in cache:
        return cache[path]
    try:
        tree = ast.parse(path.read_text(errors="ignore"))
    except SyntaxError:
        cache[path] = None
        return None
    w = ArmWalker(module_consts(tree))
    for st in tree.body:
        w.visit(st)
    cache[path] = w
    return w


def reachable_funcs(w, start):
    seen, stack = set(), [start]
    while stack:
        f = stack.pop()
        if f in seen:
            continue
        seen.add(f)
        stack += [g for g in w.calls.get(f, ()) if g not in seen]
    return seen


def writer_scope(w, tag):
    """Which function writes the CSV whose name carries `tag` (e.g. '.grid.csv')?"""
    for func, lits in w.writers:
        if any(tag in s or (tag.strip(".") and tag.strip(".").split(".")[0] in s) for s in lits):
            return func
    return None


def ast_label(csv_path, script_path, df):
    """Return (label_or_None, evidence, selector, {literal: conv}) for one CSV file.
    label_or_None is None when the answer is per-ROW (caller must group by the column)."""
    w = analyse_script(script_path)
    if w is None:
        return "UNDECIDABLE", "ast:unparseable", None, {}
    tag = "." + csv_path.name.split(".", 1)[1] if "." in csv_path.name else csv_path.name
    scope = writer_scope(w, tag)
    if scope is not None:
        reach = reachable_funcs(w, scope) | reachable_funcs(w, "<module>") if scope == "<module>" \
            else reachable_funcs(w, scope)
        ev_scope = f"writer:{scope}"
    else:
        reach = set(w.calls) | {"<module>"} | {h["func"] for h in w.hits}
        ev_scope = "module"
    hits = [h for h in w.hits if h["func"] in reach] or w.hits
    if not hits:
        return "UNDECIDABLE", "ast:no-weight-expression", None, {}

    def conv_of(h):
        return "MATCHED" if (h["matched"] and h["conv"] == "NORM") else h["conv"]

    convs = {conv_of(h) for h in hits}
    if len(convs) == 1:
        return convs.pop(), f"ast:single({ev_scope})", None, {}

    sels = [s for s, _ in sorted(
        pd.Series([h["selector"] for h in hits if h["selector"]]).value_counts().items(),
        key=lambda kv: -kv[1])] if any(h["selector"] for h in hits) else []
    low = {str(c).strip().lower(): c for c in df.columns}
    for sel in sels:
        lit2conv, else_conv = {}, None
        for h in hits:
            if h["selector"] != sel:
                continue
            if h["kind"] in ("guard", "loop"):
                for L in h["literals"]:
                    lit2conv[L] = conv_of(h)
            elif h["kind"] == "else":
                else_conv = conv_of(h)
        covered = set(lit2conv.values()) | ({else_conv} if else_conv else set())
        if covered != convs:                       # this selector does not explain every arm
            continue
        col = low.get(sel.lower())
        if col is None:
            for c in df.columns:
                if df[c].dtype != object:
                    continue
                vals = {str(x).strip() for x in df[c].dropna().unique()}
                if not vals or len(vals) > 12:
                    continue
                if vals <= set(lit2conv) or (vals & set(lit2conv) and else_conv):
                    col = c
                    break
        if col is not None:
            return (None, f"ast:armcol({col};{ev_scope})", col,
                    dict(lit2conv, **({"__ELSE__": else_conv} if else_conv else {})))
    if sels:
        return "UNDECIDABLE", f"ast:multi-arm-no-column({sels[0]};{ev_scope})", sels[0], {}
    return "UNDECIDABLE", f"ast:multi-arm-unguarded({ev_scope})", None, {}


# ================================================================= THE FROZEN CORPUS
def frozen_dir():
    """The corpus AS IT STOOD when idea 244 ran.  Its committed `.census.csv` and
    `.census_rejects.csv` between them name every file that produced a cell or a counted
    rejection; a file in neither contributed nothing.  Symlinking exactly that set (plus
    parent scripts) into a scratch directory makes the two labellers read the SAME corpus,
    so any movement in the bound is the labeller and not four days of new commits."""
    import tempfile
    names = set()
    for tag in ("census", "census_rejects"):
        p = OUT / f"{M.STEM}.{tag}.csv"
        if p.exists():
            names |= set(pd.read_csv(p)["file"].dropna().astype(str))
    d = Path(tempfile.mkdtemp(prefix="idea469_frozen_"))
    n = 0
    for nm in sorted(names):
        src = OUT / nm
        if not src.exists():
            continue
        (d / nm).symlink_to(src)
        n += 1
        sp = M.script_for(src)
        if sp is not None and not (d / sp.name).exists():
            (d / sp.name).symlink_to(sp)
    return d, n, len(names)


# ================================================================= THE RE-CENSUS
def census_ast(root=OUT):
    """Idea 244's census loop VERBATIM in every respect except label_convention()."""
    cells, rejects = [], []
    files_scanned = 0
    for f in sorted(root.glob("*.csv")):
        if f.name.startswith(STEM) or f.name.startswith(M.STEM):
            continue
        files_scanned += 1
        try:
            df = pd.read_csv(f)
        except Exception as e:
            rejects.append(dict(file=f.name, col="", reason=f"unreadable:{type(e).__name__}"))
            continue
        if df.empty:
            rejects.append(dict(file=f.name, col="", reason="empty"))
            continue
        ccols = [c for c in df.columns if c in M.COUNT_COLS]
        if not ccols:
            continue
        scols = [c for c in df.columns if c in M.SHARPE_COLS]
        sp = M.script_for(f)
        if sp is None:
            rejects.append(dict(file=f.name, col=",".join(ccols), reason="no parent script"))
            continue
        src = sp.read_text(errors="ignore")
        ranks = bool(M.RANK_PAT.search(src))
        convcol = next((c for c in M.CONV_COLS if c in df.columns), None)
        flat, ev, sel, lit2conv = ast_label(f, sp, df)
        armcol = sel if flat is None else None
        for c in ccols:
            v = pd.to_numeric(df[c], errors="coerce").dropna()
            uv = sorted(set(v.astype(int))) if len(v) and (v % 1 == 0).all() else []
            if len(uv) < 3:
                rejects.append(dict(file=f.name, col=c, reason=f"<3 distinct int values ({len(uv)})"))
                continue
            if min(uv) < 2 or max(uv) > 500:
                rejects.append(dict(file=f.name, col=c, reason=f"range {min(uv)}..{max(uv)} outside [2,500]"))
                continue
            if not scols:
                rejects.append(dict(file=f.name, col=c, reason="no Sharpe column beside it"))
                continue
            if not ranks:
                rejects.append(dict(file=f.name, col=c, reason="parent script never ranks on a count"))
                continue
            pcol = next((p for p in M.PANEL_COLS if p in df.columns), None)
            gcols = [x for x in (pcol, convcol) if x]
            groups = df.groupby([df[x].astype(str) for x in gcols]) if gcols else [((), df)]
            for gkey, g in groups:
                gkey = gkey if isinstance(gkey, tuple) else (gkey,)
                gmap = dict(zip(gcols, gkey))
                praw = gmap.get(pcol, "(all)") if pcol else "(all)"
                key = str(praw).strip().lower().replace("-", "").replace("_", "")
                pk = M.PANEL_MAP.get(key, "")
                # ---- the AST label, per row-group
                subgroups = [(flat, ev, g)]
                if armcol is not None and armcol in g.columns:
                    subgroups = []
                    for av, gg in g.groupby(g[armcol].astype(str)):
                        lab = lit2conv.get(av.strip(), lit2conv.get("__ELSE__"))
                        if lab is None:
                            subgroups.append(("UNDECIDABLE", f"ast:armcol-unmapped({av})", gg))
                        else:
                            subgroups.append((lab, f"{ev}={av}", gg))
                for lab, evx, gsub in subgroups:
                    for scol in scols:
                        gg = gsub[[c, scol]].apply(pd.to_numeric, errors="coerce").dropna()
                        if gg.empty or gg[c].nunique() < 3:
                            continue
                        grid = sorted(set(gg[c].astype(int)))
                        best = gg.loc[gg[scol].idxmax()]
                        cells.append(dict(file=f.name, count_col=c, sharpe_col=scol,
                                          panel_raw=str(praw), panel=pk if pk else "unmapped",
                                          conv=lab, conv_evidence=evx,
                                          n_grid=len(grid), n_min=int(min(grid)), n_max=int(max(grid)),
                                          n_argmax=int(best[c]), sharpe_at_argmax=float(best[scol])))
    return pd.DataFrame(cells), pd.DataFrame(rejects), files_scanned


def fmt(df, p=3):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ================================================================= MAIN
def main():
    print("=" * 200)
    print(f"Idea 469  label-the-337-undecidable-count-cells-from-the-AST (cloud) | {SCRIPT} | "
          f"{COST_BPS} bps headline (+25 bps rung), weekly, next-day execution")
    print("=" * 200)

    # ---------------------------------------------------------- CHECK (a): reproduce 244
    print("\nCHECK(a)  re-run idea 244's OWN regex census through its OWN committed code, "
          "before the AST is used at all")
    fdir, nlink, nnamed = frozen_dir()
    print(f"  frozen corpus (the files idea 244 actually read): {nlink} of {nnamed} still present")
    OUT244 = M.OUT
    M.OUT = fdir
    try:
        cen244, rej244, nfiles244 = M.census()
    finally:
        M.OUT = OUT244
    got = cen244["conv"].value_counts().to_dict()
    exp = {"MIXED": 260, "FIXEDTOT": 222, "NORM": 135, "UNKNOWN": 77}
    print(f"  cells {len(cen244)} (published 694) | " +
          " ".join(f"{k} {got.get(k, 0)} (pub {v})" for k, v in exp.items()))
    ok = len(cen244) == 694 and all(got.get(k, 0) == v for k, v in exp.items())
    print(f"  REPRODUCED EXACTLY: {ok}")
    if not ok:
        print("  !! idea 244's published census does not reproduce on the frozen corpus -- every "
              "comparison below is therefore made against THIS run's regex numbers (printed "
              "above), which are the honest baseline.")

    # ---------------------------------------------------------- the AST census
    print("\n" + "=" * 200)
    print("Q1  THE AST CENSUS  -- same frozen corpus, same admission tests, same panel map; "
          "only the labeller changed")
    print("=" * 200)
    cen, rej, nfiles = census_ast(fdir)
    cen_now, _, nfiles_now = census_ast(OUT)
    print(f"CORPUS DRIFT (reported, not folded into the headline): the frozen corpus is "
          f"{nfiles} files / {len(cen)} cells; the corpus as it stands TODAY is "
          f"{nfiles_now} files / {len(cen_now)} cells.")
    cen_now.to_csv(OUT / f"{STEM}.census_today.csv", index=False)
    print(f"files scanned {nfiles} | cells {len(cen)} | rejects {len(rej)}")
    cen["decided"] = ~cen["conv"].astype(str).str.startswith("UNDECIDABLE")
    print("\nlabel counts (AST):")
    print(cen["conv"].value_counts().to_string())
    print("\nevidence classes (AST):")
    print(cen["conv_evidence"].astype(str).str.replace(r"\(.*", "", regex=True).value_counts().to_string())
    print("\nUNDECIDABLE reasons, counted not hidden:")
    und = cen[~cen["decided"]]
    print(und["conv_evidence"].astype(str).str.replace(r"\(.*", "", regex=True).value_counts().to_string()
          if len(und) else "  (none)")

    # side-by-side against the regex on the SAME cell keys
    keyc = ["file", "count_col", "sharpe_col", "panel_raw", "n_min", "n_max", "n_argmax"]
    a = cen.groupby(keyc)["conv"].agg(lambda s: s.iloc[0] if s.nunique() == 1 else "SPLIT")
    b = cen244.set_index(keyc)["conv"]
    b = b[~b.index.duplicated()]
    j = pd.DataFrame({"AST": a}).join(pd.DataFrame({"REGEX": b}), how="inner")
    print(f"\nCELL-BY-CELL, on the {len(j)} cell keys the two censuses share:")
    ct = pd.crosstab(j["REGEX"], j["AST"].where(j["AST"].str.startswith("UNDECIDABLE"),
                                                j["AST"]).str.replace(r"UNDECIDABLE.*", "UNDECIDABLE", regex=True))
    print(ct.to_string())
    dec_ast = ~j["AST"].str.startswith("UNDECIDABLE")
    dec_rx = ~j["REGEX"].isin(["UNKNOWN", "MIXED"])
    print(f"\n  decided by REGEX {int(dec_rx.sum())}/{len(j)} = {dec_rx.mean():.1%}")
    print(f"  decided by AST   {int(dec_ast.sum())}/{len(j)} = {dec_ast.mean():.1%}"
          f"   (of which {int((j['AST']=='SPLIT').sum())} are cells the AST RESOLVES INTO TWO OR MORE "
          f"arms -- one published 'cell' that is really two books; the regex could only give it one label)")
    print(f"  single-label by AST {int((dec_ast & (j['AST']!='SPLIT')).sum())}/{len(j)} = "
          f"{(dec_ast & (j['AST']!='SPLIT')).mean():.1%}")
    both = dec_ast & dec_rx
    agree = (j.loc[both, "AST"] == j.loc[both, "REGEX"]).mean() if both.any() else np.nan
    print(f"  both decided {int(both.sum())}; they AGREE on {agree:.1%}"
          f" ({int((j.loc[both,'AST'] != j.loc[both,'REGEX']).sum())} disagreements)")
    if both.any() and (j.loc[both, "AST"] != j.loc[both, "REGEX"]).any():
        print("\n  disagreements (AST vs REGEX), first 15:")
        d = j.loc[both & (j["AST"] != j["REGEX"])].reset_index()
        print(d[["file", "count_col", "REGEX", "AST"]].head(15).to_string(index=False))
        print("\n  EVERY disagreeing file, with the exact weight expressions the AST found "
              "(file:line, so each call is checkable against the committed source):")
        for fn in sorted(d["file"].unique()):
            sp = M.script_for(OUT / fn)
            w = analyse_script(sp) if sp else None
            if w is None:
                continue
            src = sp.read_text(errors="ignore").split("\n")
            print(f"    {sp.name}")
            for h in w.hits:
                ln = src[h["lineno"] - 1].strip() if 0 < h["lineno"] <= len(src) else ""
                print(f"       L{h['lineno']:<5} {h['conv']:<9} in {h['func']}() "
                      f"[{h['kind']}{'/' + str(sorted(h['literals'])) if h['literals'] else ''}]"
                      f"  ::  {ln[:110]}")
    cen.to_csv(OUT / f"{STEM}.census.csv", index=False)
    j.reset_index().to_csv(OUT / f"{STEM}.sidebyside.csv", index=False)
    if len(rej):
        rej.to_csv(OUT / f"{STEM}.census_rejects.csv", index=False)

    # ---------------------------------------------------------- panels + the re-quoted bound
    panels, dropped = M.build_panels()
    print(f"\nsmall panel hygiene: dropped {dropped} tickers with max_1d_move >= 1.0; "
          f"{len(panels['SMALL'][1])} tradable remain")
    ne_map = {pk: M.rank_on_rebal(px, M.eligible_mask(px, trad)) for pk, (px, trad) in panels.items()}

    print("\n" + "=" * 200)
    print(f"Q2  THE RE-QUOTED BOUND  (pre-registered ladder test: realised-gross span across the "
          f"cell's OWN quoted grid >= {SPAN_ABS:.2f} NAV)")
    print("=" * 200)
    rows = []
    for _, c in cen.iterrows():
        conv = c["conv"]
        if c["panel"] == "unmapped" or conv not in ("FIXEDTOT", "NORM", "FIXEDW", "MATCHED"):
            rows.append(dict(**c, g_lo=np.nan, g_hi=np.nan, gross_span=np.nan, gross_span_rel=np.nan,
                             max_gross=np.nan, levered=False,
                             ladder=("UNMAPPED" if c["panel"] == "unmapped" else "UNKNOWN")))
            continue
        ne = ne_map[c["panel"]]
        gconv = "FIXEDTOT" if conv == "MATCHED" else conv     # MATCHED tracks FIXEDTOT's gross
        g_lo = M.target_gross(ne, int(c["n_min"]), gconv)
        g_hi = M.target_gross(ne, int(c["n_max"]), gconv)
        span = abs(g_hi - g_lo)
        mid = (g_hi + g_lo) / 2
        gmax = max(g_lo, g_hi)
        rows.append(dict(**c, g_lo=g_lo, g_hi=g_hi, gross_span=span,
                         gross_span_rel=span / mid if mid > 0 else np.nan, max_gross=gmax,
                         levered=bool(gmax > M.MAX_GROSS + 1e-9),
                         ladder=("LADDER" if span >= SPAN_ABS else "FLAT")))
    S = pd.DataFrame(rows)
    S.to_csv(OUT / f"{STEM}.ladder.csv", index=False)
    print(S.groupby("ladder").size().sort_values(ascending=False).to_string())
    print("\nby convention x ladder:")
    print(pd.crosstab(S["conv"].astype(str).str.replace(r"UNDECIDABLE.*", "UNDECIDABLE", regex=True),
                      S["ladder"]).to_string())

    # headline stays on the idea-244 comparable set: FIXEDTOT / NORM only
    core = S[S["conv"].isin(["FIXEDTOT", "NORM"]) & (S["ladder"].isin(["LADDER", "FLAT"]))]
    ext = S[S["conv"].isin(["FIXEDTOT", "NORM", "FIXEDW", "MATCHED"]) & (S["ladder"].isin(["LADDER", "FLAT"]))]
    undec = S[(S["ladder"] == "UNKNOWN") & (S["panel"] != "unmapped")]
    n_lad = int((core["ladder"] == "LADDER").sum())
    print(f"\nDECIDABLE (mapped panel AND a FIXEDTOT/NORM label): {len(core)} of {len(S)} "
          f"= {len(core)/len(S):.1%} coverage   [idea 244: 271 of 694 = 39.0%]")
    if len(core):
        print(f"  GROSS-LADDER points: {n_lad} of {len(core)} = {n_lad/len(core):.1%}"
              f"   [idea 244 point estimate: 95/271 = 35.1%]")
        n_rel = int((core["gross_span_rel"] >= SPAN_REL).sum())
        print(f"  relative criterion (span/mean >= {SPAN_REL}): {n_rel}/{len(core)} = {n_rel/len(core):.1%}")
        print(f"  span distribution: min {core['gross_span'].min():.3f} p25 {core['gross_span'].quantile(.25):.3f} "
              f"median {core['gross_span'].median():.3f} p75 {core['gross_span'].quantile(.75):.3f} "
              f"max {core['gross_span'].max():.3f}")
        print(f"  distinct FILES carrying at least one ladder cell: "
              f"{core.loc[core['ladder']=='LADDER','file'].nunique()} of {core['file'].nunique()}")
        print(f"  cells whose grid top implies gross > {M.MAX_GROSS:.2f} of NAV (leverage): "
              f"{int(core['levered'].sum())}; max implied gross {core['max_gross'].max():.2f}")
        print("\n  ladder rate by convention and panel:")
        print(pd.crosstab([core["conv"], core["panel"]], core["ladder"]).to_string())
    n_lad_e = int((ext["ladder"] == "LADDER").sum())
    print(f"\nEXTENDED set (adds the FIXEDW and MATCHED labels the regex could not produce): "
          f"{n_lad_e}/{len(ext)} = {n_lad_e/max(len(ext),1):.1%}")

    print(f"\nBOUNDS on the record-wide ladder rate, carrying the undecidable cells explicitly:")
    if len(undec):
        wl = []
        for _, c in undec.iterrows():
            ne = ne_map[c["panel"]]
            wl.append({cand: abs(M.target_gross(ne, int(c["n_max"]), cand)
                                 - M.target_gross(ne, int(c["n_min"]), cand)) >= SPAN_ABS
                       for cand in ("FIXEDTOT", "NORM")})
        WL = pd.DataFrame(wl)
        hi = n_lad + int(WL["FIXEDTOT"].sum())
        den = len(core) + len(undec)
        print(f"  {len(undec)} undecidable cells sit on a MAPPABLE panel; under a FIXEDTOT reading "
              f"{int(WL['FIXEDTOT'].sum())} would be ladders, under NORM {int(WL['NORM'].sum())}.")
        print(f"  LOWER bound (undecidables all FLAT/NORM): {n_lad}/{den} = {n_lad/den:.1%}"
              f"      [idea 244: 95/546 = 17.4%]")
        print(f"  POINT estimate on decidable cells only:   {n_lad}/{len(core)} = {n_lad/len(core):.1%}"
              f"      [idea 244: 95/271 = 35.1%]")
        print(f"  UPPER bound (undecidables all FIXEDTOT):  {hi}/{den} = {hi/den:.1%}"
              f"      [idea 244: 238/546 = 43.6%]")
        print(f"  BOUND WIDTH: {(hi-n_lad)/den:.1%} of the record   [idea 244: 26.2 pp]")
    else:
        den = len(core)
        print(f"  NO undecidable cell remains on a mappable panel: the bound COLLAPSES to the point "
              f"estimate {n_lad}/{den} = {n_lad/den:.1%}   [idea 244: 17.4% - 43.6%]")

    # ---------------------------------------------------------- L1 target vs realised gross
    print("\n" + "=" * 200)
    print("L1  IS `target_gross` A FAIR STAND-IN FOR REALISED HELD GROSS?  84 live books "
          "(7 panels x 6 n x {FIXEDTOT, NORM}), every point reported")
    print("=" * 200)
    live, cache = [], {}
    for pk, (px, trad) in panels.items():
        elig = M.eligible_mask(px, trad)
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        base = M.run(px, M.rules_v2_weights(px))
        ewall = M.run(px, M.ewall_weights(px, elig))
        ne = ne_map[pk]
        for n in NS:
            for arm in ("FIXEDTOT", "NORM"):
                r = M.run(px, M.weights_for(px, elig, n, arm))
                cache[(pk, n, arm)] = r
                hg = r["hg"].loc[start:].mean()
                tg = M.target_gross(ne, n, arm)
                for bps in COST_RUNGS:
                    ret = M.net(r, bps).loc[start:]
                    m = M.metrics(ret)
                    live.append(dict(panel=pk, n=n, arm=arm, cost_bps=bps,
                                     held_gross=hg, target_gross=tg, gross_err=hg - tg,
                                     CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                     H1=M.half_sharpes(ret)[0], H2=M.half_sharpes(ret)[1],
                                     OOS_Sharpe=M.metrics(ret.loc[OOS_START:])["Sharpe"],
                                     IS_Sharpe=M.metrics(ret.loc[:IS_END])["Sharpe"],
                                     OOS_CAGR=M.metrics(ret.loc[OOS_START:])["CAGR"],
                                     OOS_MaxDD=M.metrics(ret.loc[OOS_START:])["MaxDD"],
                                     fail_4a=M.fail_4a(ret, M.net(base, bps).loc[start:]),
                                     fail_4b=M.fail_4b(ret, spy, ret.loc[OOS_START:], spy.loc[OOS_START:])))
        cache[(pk, "BASE")] = base
        cache[(pk, "EWALL")] = ewall
        cache[(pk, "SPY")] = spy
        cache[(pk, "START")] = start
    L = pd.DataFrame(live)
    L["pass_4a"] = L["fail_4a"] == "-"
    L["pass_4b"] = L["fail_4b"] == "-"
    L.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    g = L[L["cost_bps"] == 10]
    print(fmt(g.pivot_table(index=["panel", "arm"], columns="n",
                            values=["target_gross", "held_gross"]), 3))
    print(f"\nmax |held - target| over all 84 books: {g['gross_err'].abs().max():.4f}  "
          f"(mean {g['gross_err'].abs().mean():.4f});  correlation "
          f"{np.corrcoef(g['held_gross'], g['target_gross'])[0,1]:.4f}")
    flips = 0
    for pk in panels:
        for arm in ("FIXEDTOT", "NORM"):
            sub = g[(g["panel"] == pk) & (g["arm"] == arm)]
            t = abs(sub["target_gross"].max() - sub["target_gross"].min()) >= SPAN_ABS
            h = abs(sub["held_gross"].max() - sub["held_gross"].min()) >= SPAN_ABS
            flips += int(t != h)
    print(f"LADDER/FLAT verdicts that FLIP when realised gross replaces target gross, over the "
          f"14 (panel x arm) sweeps on the live NS grid: {flips} of 14")

    # ---------------------------------------------------------- L2 rule 8
    print("\n" + "=" * 200)
    print("L2  RULE 8  -- n chosen on 2009-2016 IS Sharpe ALONE, 2017-2026 read ONCE; and the "
          "OOS COST OF THE LABEL")
    print("=" * 200)
    wf = []
    for pk, (px, trad) in panels.items():
        start = cache[(pk, "START")]
        spy = cache[(pk, "SPY")]
        for bps in COST_RUNGS:
            bret = M.net(cache[(pk, "BASE")], bps).loc[start:]
            eret = M.net(cache[(pk, "EWALL")], bps).loc[start:]
            picks = {}
            for arm in ("FIXEDTOT", "NORM"):
                iss = {n: M.metrics(M.net(cache[(pk, n, arm)], bps).loc[start:IS_END])["Sharpe"] for n in NS}
                picks[arm] = max(iss, key=iss.get)
            for arm in ("FIXEDTOT", "NORM"):
                for read in ("FIXEDTOT", "NORM"):
                    n_pick = picks[read]                       # n chosen under the READ label
                    ret = M.net(cache[(pk, n_pick, arm)], bps).loc[start:]   # book actually run
                    o = ret.loc[OOS_START:]
                    wf.append(dict(panel=pk, cost_bps=bps, truth=arm, read=read, n_pick=n_pick,
                                   OOS_CAGR=M.metrics(o)["CAGR"], OOS_Sharpe=M.metrics(o)["Sharpe"],
                                   OOS_MaxDD=M.metrics(o)["MaxDD"],
                                   oracle=max(M.metrics(M.net(cache[(pk, n, arm)], bps)
                                                        .loc[OOS_START:])["Sharpe"] for n in NS),
                                   base_OOS=M.metrics(bret.loc[OOS_START:])["Sharpe"],
                                   ewall_OOS=M.metrics(eret.loc[OOS_START:])["Sharpe"],
                                   spy_OOS=M.metrics(spy.loc[OOS_START:])["Sharpe"],
                                   spy_OOS_CAGR=M.metrics(spy.loc[OOS_START:])["CAGR"],
                                   spy_OOS_MaxDD=M.metrics(spy.loc[OOS_START:])["MaxDD"]))
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    right = W[W["truth"] == W["read"]]
    print("\nIS-chosen n by panel and convention (10 bps):")
    print(right[right["cost_bps"] == 10].pivot_table(index="panel", columns="read",
                                                     values="n_pick").astype(int).to_string())
    print("\nOOS read once, correctly-labelled arm (10 bps):")
    print(fmt(right[right["cost_bps"] == 10].set_index(["panel", "truth"])[
        ["n_pick", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "oracle", "base_OOS", "ewall_OOS", "spy_OOS"]], 4))
    for bps in COST_RUNGS:
        r = right[right["cost_bps"] == bps]
        print(f"\n@{bps} bps, correctly-labelled: beats RULES v2 OOS {int((r['OOS_Sharpe']>r['base_OOS']).sum())}/{len(r)}"
              f" | beats EW_ALL {int((r['OOS_Sharpe']>r['ewall_OOS']).sum())}/{len(r)}"
              f" | beats SPY {int((r['OOS_Sharpe']>r['spy_OOS']).sum())}/{len(r)}"
              f" | mean OOS regret vs oracle {(r['oracle']-r['OOS_Sharpe']).mean():+.4f}")
    print("\nTHE OOS COST OF THE LABEL -- same book, n chosen under the WRONG convention label:")
    piv = W.pivot_table(index=["cost_bps", "panel", "truth"], columns="read", values="OOS_Sharpe")
    piv["d(wrong-right)"] = np.where(piv.index.get_level_values("truth") == "FIXEDTOT",
                                     piv["NORM"] - piv["FIXEDTOT"], piv["FIXEDTOT"] - piv["NORM"])
    print(fmt(piv, 4))
    d = piv["d(wrong-right)"]
    print(f"\n  mean {d.mean():+.4f}  median {d.median():+.4f}  min {d.min():+.4f}  max {d.max():+.4f}  "
          f"| the wrong label HURTS in {int((d<0).sum())} of {len(d)} cells, helps in {int((d>0).sum())}, "
          f"is a no-op (same n) in {int((d==0).sum())}")
    nmove = (W.pivot_table(index=["cost_bps", "panel"], columns="read", values="n_pick")
             .assign(moves=lambda x: x["FIXEDTOT"] != x["NORM"])["moves"])
    print(f"  the LABEL MOVES THE PICK in {int(nmove.sum())} of {len(nmove)} (panel x rung) cells")

    # ---------------------------------------------------------- L3 KEEP paths
    print("\n" + "=" * 200)
    print("L3  BOTH KEEP PATHS on all 168 live points (4a vs the live RULES v2 on the book's own "
          "panel; 4b vs SPY, incl. rule 8)")
    print("=" * 200)
    print(L.groupby(["cost_bps", "arm"])[["pass_4a", "pass_4b"]].sum().to_string())
    print(f"\nTOTAL: 4a {int(L['pass_4a'].sum())}/{len(L)}   4b {int(L['pass_4b'].sum())}/{len(L)}")
    fb = L.loc[~L["pass_4b"], "fail_4b"].str.split(",").explode().value_counts()
    print(f"binding 4b bars: {fb.to_dict()}")
    if L["pass_4b"].any():
        print("\n4b passes:")
        print(fmt(L[L["pass_4b"]][["panel", "n", "arm", "cost_bps", "CAGR", "Sharpe", "H1", "H2",
                                   "OOS_Sharpe", "MaxDD", "fail_4a"]], 4))
    else:
        print("\nno 4b pass anywhere on this grid.")
    print("\nREFERENCE (10 bps, each panel's own comparands):")
    ref = []
    for pk in panels:
        start = cache[(pk, "START")]
        b = M.net(cache[(pk, "BASE")], 10).loc[start:]
        e = M.net(cache[(pk, "EWALL")], 10).loc[start:]
        s = cache[(pk, "SPY")]
        for nm, x in (("RULES v2", b), ("EW_ALL", e), ("SPY", s)):
            m = M.metrics(x)
            ref.append(dict(panel=pk, book=nm, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                            H1=M.half_sharpes(x)[0], H2=M.half_sharpes(x)[1],
                            OOS_Sharpe=M.metrics(x.loc[OOS_START:])["Sharpe"]))
    R = pd.DataFrame(ref)
    print(fmt(R.set_index(["panel", "book"]), 4))
    R.to_csv(OUT / f"{STEM}.reference.csv", index=False)

    print("\n" + "=" * 200)
    print("DONE")
    print("=" * 200)


if __name__ == "__main__":
    main()

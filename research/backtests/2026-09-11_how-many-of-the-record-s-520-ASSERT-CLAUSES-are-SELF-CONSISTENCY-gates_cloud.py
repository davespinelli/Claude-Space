#!/usr/bin/env python3
"""IDEA 681 (cloud) — how many of the record's 520 ASSERT CLAUSES are SELF-CONSISTENCY gates?

QUESTION (queue).  Idea 516 found 36 of 36 re-executed scripts pass their own gates while 35 of
36 move a published number, because a gate that compares two quantities computed inside the SAME
run cannot see the panel move under it.  Classify every one of idea 515's 520 clauses as
SELF-CONSISTENCY (both sides computed this run) vs REPRODUCTION (one side a committed constant
or a committed artefact) and report the share of the record's gating that is structurally blind
to vintage.  Max 2 params (classifier, sample).

WHY THE CLAUSE SOURCE IS NOT ENOUGH.  Most clauses read `g1 < 1e-09`, `d3b / max(tot3b,1) < 1e-4`
— the interesting side is a local variable.  So the classifier is an AST DATAFLOW closure: for
each clause, resolve every Name on its VALUE side back through the producing script's own
assignments (depth 6, cycle-guarded, over-approximating by unioning every assignment to a name
anywhere in the file), and tag the leaves.  A leaf is ARTEFACT if it is a read call
(read_csv/read_json/read_parquet/read_pickle/read_table/read_text/read_bytes/load/loads/open),
CONST if it is a numeric literal, otherwise COMPUTED.

PARAMETERS — exactly two, every grid point reported, neither tuned on an outcome:
  P1  CLASSIFIER, 3 nested strictnesses for what counts as a COMMITTED CONSTANT (the ARTEFACT
      rule is identical at all three).  Ordering-comparison numeric operands are BARS, never
      values, at all three levels.
        WIDE   : any numeric literal with |v| >= 1e-2 anywhere in the value-side closure.
        MID    : (headline) such a literal in EXPECTED-VALUE POSITION — an operand of `-` or `/`,
                 or a comparand of `==` / `!=`.
        NARROW : MID and the literal is NON-INTEGRAL, i.e. carries hand-copied decimals (1.133).
      NARROW subset MID subset WIDE by construction; the script asserts the nesting.
  P2  SAMPLE, 3 NESTED script subsets ordered by md5(filename) so the sample spans dates rather
      than following them: S38 subset S76 subset S151 (S151 = the whole census).

LEGS.
  [A] The classification itself, 9 grid points (3 classifiers x 3 samples), plus the per-FORM cut
      (tolerance / exact / structural / count / floor) at the headline classifier.
  [B] THE MECHANISM, tested where idea 516 measured it: of the 36 scripts idea 516 re-executed
      (35 of which moved a published number while exiting rc=0), what share of their clauses are
      SELF-CONSISTENCY?  Cross-cut by idea 516's own `cause` column.
  [C] PROTOCOL leg, rule 8 and both KEEP paths.  30 U56 band x gross arms at 10 bps, weekly, t+1;
      4a against the live RULES v2 book, 4b against SPY; band chosen on 2009-2016 alone and
      evaluated on 2017-2026 untouched.  Then the VINTAGE STEP: every arm re-run on the panel
      truncated to its state 2 trading days earlier (the APPEND channel; the restatement channel
      is not reachable offline) — the |delta| a SELF-CONSISTENCY gate is blind to by construction,
      and the count of 4a/4b verdicts it moves.

REPRODUCTION GATES (recorded, NEVER raising — the point of this idea is that a raising gate hides
what is behind it).  Both sides committed, i.e. these are REPRODUCTION gates by this script's own
definition: idea 515's published 520 clauses / 345 tolerance / 87 exact / 46 structural / 40
count / 2 floor / 151 scripts, and idea 516's published 36 re-executed / 35 moved.

Deterministic; no randomness.  Writes <STEM>.{clauses,grid,byform,i516,keeppaths,walkforward,
vintage}.csv and <STEM>.console.txt.  Does not modify RULES.md, PROTOCOL.md, scan.py, bot.py,
baseline.py.
"""
from __future__ import annotations

import ast
import hashlib
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "research" / "backtests"
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))

from baseline import band_state, load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-11_how-many-of-the-record-s-520-ASSERT-CLAUSES-are-SELF-CONSISTENCY-gates_cloud"
CENSUS = OUT / ("2026-09-09_restate-the-record-s-158-REPRODUCTION-GATES-as-TOLERANCES-"
                "in-record-units_C.census.csv")
GATES515 = OUT / ("2026-09-09_restate-the-record-s-158-REPRODUCTION-GATES-as-TOLERANCES-"
                  "in-record-units_C.gates.csv")
I516 = OUT / ("2026-09-11_how-many-of-the-60-rc-0-scripts-SILENTLY-changed-their-own-published-"
              "numbers_B.scripts.csv")

CLASSIFIERS = ["WIDE", "MID", "NARROW"]
HEADLINE = "MID"
SAMPLES = [38, 76, 151]
DEPTH = 6
CONST_FLOOR = 1e-2          # a literal below this is a tolerance, not a published number
COST_BPS, FREQ = 10, "W"
VINTAGE_DAYS = 2            # idea 516's own two-calendar-day step, in trading days

LOG: list[str] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, ok, detail):
    say(f"  GATE {name:<26} {'PASS' if ok else 'FAIL'}   {detail}")
    return bool(ok)


# ========================================================== AST DATAFLOW =====
READ_FUNCS = {"read_csv", "read_json", "read_parquet", "read_pickle", "read_table",
              "read_text", "read_bytes", "read_excel", "load", "loads", "open", "readlines"}
ORDERING = (ast.Lt, ast.LtE, ast.Gt, ast.GtE)

# A read is only a REPRODUCTION leg if it brings in a PRIOR RUN'S OUTPUT.  Reading the price
# panel / universe / meta is an INPUT both sides of the gate share, so it is exactly as
# vintage-sensitive on one side as on the other and leaves the gate self-consistent.
INPUT_PAT = re.compile(r"prices|small_meta|universe|volume|SMALL_PANEL|\bdata\b", re.I)
ARTEFACT_PAT = re.compile(r"backtests|LEADERBOARD|CHANGELOG|QUEUE|PROTOCOL|result\.md|memo|"
                          r"\bOUT\b|\bBT\b|STEM|20\d\d-\d\d-\d\d")
FILEISH_PAT = re.compile(r"\.csv|\.json|\.md|\.gz|\.txt")


def func_name(node: ast.AST) -> str:
    f = node.func
    while isinstance(f, ast.Attribute):
        return f.attr
    return f.id if isinstance(f, ast.Name) else ""


def path_expr(call: ast.Call):
    """The expression naming the file a read call reads (handles `p.read_text()`)."""
    if call.args:
        return call.args[0]
    f = call.func
    return f.value if isinstance(f, ast.Attribute) else None


def path_kind(expr, amap) -> str:
    """INPUT (shared panel/config) vs ARTEFACT (a prior run's committed output)."""
    if expr is None:
        return "ARTEFACT_UNRESOLVED"
    txt, seen, frontier = [], set(), [(expr, 0)]
    while frontier:
        n, d = frontier.pop()
        try:
            txt.append(ast.unparse(n))
        except Exception:
            pass
        if d >= 3:
            continue
        for sub in ast.walk(n):
            if isinstance(sub, ast.Name) and sub.id not in seen:
                seen.add(sub.id)
                for rhs in amap.get(sub.id, [])[:6]:
                    frontier.append((rhs, d + 1))
    blob = " ".join(txt)
    if ARTEFACT_PAT.search(blob):          # names a prior run's output directory or stem
        return "ARTEFACT"
    if INPUT_PAT.search(blob):             # the shared panel / universe / meta
        return "INPUT"
    if FILEISH_PAT.search(blob):
        return "ARTEFACT_UNRESOLVED"
    return "ARTEFACT_UNRESOLVED"


def assign_map(tree: ast.AST) -> dict[str, list[ast.AST]]:
    """name -> every RHS assigned to it anywhere in the file (deliberate over-approximation:
    a clause is called SELF only if NO assignment to any name it reaches is committed)."""
    m: dict[str, list[ast.AST]] = {}
    for node in ast.walk(tree):
        tgts, val = [], None
        if isinstance(node, ast.Assign):
            tgts, val = node.targets, node.value
        elif isinstance(node, (ast.AugAssign, ast.AnnAssign)) and node.value is not None:
            tgts, val = [node.target], node.value
        elif isinstance(node, (ast.For, ast.comprehension)):
            tgts, val = [node.target], getattr(node, "iter", None)
        elif isinstance(node, ast.withitem) and node.optional_vars is not None:
            tgts, val = [node.optional_vars], node.context_expr
        if val is None:
            continue
        for t in tgts:
            for sub in ast.walk(t):
                if isinstance(sub, ast.Name):
                    m.setdefault(sub.id, []).append(val)
    return m


def scan_expr(node: ast.AST, amap=None):
    """One expression: (read kinds, [(value, position)], {names}).  Positions are
    'bar' (numeric operand of an ordering compare), 'diff' (operand of - or /),
    'eq' (comparand of == / !=), 'other'."""
    reads: set[str] = set()
    consts: list[tuple[float, str]] = []
    names: set[str] = set()
    pos: dict[int, str] = {}

    def mark(n, p):
        if isinstance(n, ast.Constant):
            pos[id(n)] = p
        elif isinstance(n, ast.UnaryOp) and isinstance(n.operand, ast.Constant):
            pos[id(n.operand)] = p

    for n in ast.walk(node):
        if isinstance(n, ast.Compare):
            ops = [type(o) for o in n.ops]
            sides = [n.left] + list(n.comparators)
            for o, (a, b) in zip(ops, zip(sides, sides[1:])):
                if o in ORDERING:
                    mark(a, "bar")
                    mark(b, "bar")
                elif o in (ast.Eq, ast.NotEq):
                    mark(a, "eq")
                    mark(b, "eq")
        elif isinstance(n, ast.BinOp) and isinstance(n.op, (ast.Sub, ast.Div)):
            mark(n.left, "diff")
            mark(n.right, "diff")

    for n in ast.walk(node):
        if isinstance(n, ast.Call):
            if func_name(n) in READ_FUNCS:
                reads.add(path_kind(path_expr(n), amap or {}))
        elif isinstance(n, ast.Name):
            names.add(n.id)
        elif isinstance(n, ast.Constant) and isinstance(n.value, (int, float)) \
                and not isinstance(n.value, bool):
            consts.append((float(n.value), pos.get(id(n), "other")))
    return reads, consts, names


def closure(expr: ast.AST, amap: dict[str, list[ast.AST]]):
    """Resolve the value side through the script's own assignments."""
    reads: set[str] = set()
    consts: list[tuple[float, str]] = []
    seen: set[str] = set()
    frontier = [(expr, 0)]
    hops = 0
    while frontier:
        node, d = frontier.pop()
        a, c, nm = scan_expr(node, amap)
        reads |= a
        consts.extend(c)
        if d >= DEPTH:
            continue
        for name in sorted(nm):        # sorted: set iteration order is hash-seed dependent
            if name in seen:
                continue
            seen.add(name)
            for rhs in amap.get(name, [])[:8]:
                hops += 1
                frontier.append((rhs, d + 1))
    return reads, consts, seen, hops


def value_side(clause_node: ast.AST) -> ast.AST:
    """The clause with its ordering BAR removed, so a tolerance is never read as a value."""
    if isinstance(clause_node, ast.Compare) and len(clause_node.ops) == 1 \
            and type(clause_node.ops[0]) in ORDERING:
        left, right = clause_node.left, clause_node.comparators[0]
        lc = isinstance(left, ast.Constant) or (
            isinstance(left, ast.UnaryOp) and isinstance(left.operand, ast.Constant))
        rc = isinstance(right, ast.Constant) or (
            isinstance(right, ast.UnaryOp) and isinstance(right.operand, ast.Constant))
        if rc and not lc:
            return left
        if lc and not rc:
            return right
    return clause_node


def classify(reads: set[str], consts, level: str) -> str:
    if "ARTEFACT" in reads or "ARTEFACT_UNRESOLVED" in reads:
        return "REPRO_ARTEFACT"
    hits = [(v, p) for v, p in consts if p != "bar" and abs(v) >= CONST_FLOOR]
    if level == "MID" or level == "NARROW":
        hits = [(v, p) for v, p in hits if p in ("diff", "eq")]
    if level == "NARROW":
        hits = [(v, p) for v, p in hits if v != round(v)]
    return "REPRO_CONST" if hits else "SELF_CONSISTENCY"


def find_clause(tree: ast.AST, lineno: int, src: str):
    """The census stores (lineno, src); locate the matching node, falling back to a re-parse
    of the recorded source so a clause is never silently skipped."""
    best = None
    for n in ast.walk(tree):
        if isinstance(n, ast.Assert) and n.lineno == lineno:
            best = n.test
            break
    if best is not None:
        for sub in ast.walk(best):
            if isinstance(sub, (ast.Compare, ast.Call)) and ast.unparse(sub) == src:
                return sub, "exact"
        return best, "assert"
    try:
        return ast.parse(src, mode="eval").body, "reparse"
    except SyntaxError:
        return None, "unparsable"


# ======================================================== [A] CLASSIFY ========
def leg_a():
    cen = pd.read_csv(CENSUS)
    say(f"[A] census: {len(cen)} clauses, {cen.script.nunique()} scripts, "
        f"forms {dict(cen.form.value_counts())}")

    trees, amaps = {}, {}
    rows = []
    for _, r in cen.iterrows():
        s = r["script"]
        if s not in trees:
            p = OUT / s
            try:
                t = ast.parse(p.read_text())
            except Exception:
                t = None
            trees[s] = t
            amaps[s] = assign_map(t) if t is not None else {}
        t = trees[s]
        if t is None:
            rows.append(dict(script=s, gate_id=r["gate_id"], lineno=r["lineno"], form=r["form"],
                             unit=r["unit"], src=r["src"], located="missing", reads="",
                             n_const=0, hops=0, **{c: "UNREADABLE" for c in CLASSIFIERS}))
            continue
        node, how = find_clause(t, int(r["lineno"]), str(r["src"]))
        if node is None:
            rows.append(dict(script=s, gate_id=r["gate_id"], lineno=r["lineno"], form=r["form"],
                             unit=r["unit"], src=r["src"], located=how, reads="",
                             n_const=0, hops=0, **{c: "UNREADABLE" for c in CLASSIFIERS}))
            continue
        reads, consts, seen, hops = closure(value_side(node), amaps[s])
        rows.append(dict(script=s, gate_id=r["gate_id"], lineno=r["lineno"], form=r["form"],
                         unit=r["unit"], src=r["src"], located=how, reads="|".join(sorted(reads)),
                         n_const=len(consts), hops=hops,
                         **{c: classify(reads, consts, c) for c in CLASSIFIERS}))
    cl = pd.DataFrame(rows)
    say(f"[A] clause located: {dict(cl.located.value_counts())}")
    say(f"[A] read kinds reached by the value-side closure: {dict(cl.reads.value_counts())}")
    say("[A]   INPUT = the shared price panel / universe / meta: both sides of the gate move with "
        "it, so it leaves the gate SELF-CONSISTENT. Only a prior run's OUTPUT is a REPRODUCTION leg.")

    # nesting of the three classifiers (NARROW subset MID subset WIDE)
    nest_ok = True
    for a, b in (("NARROW", "MID"), ("MID", "WIDE")):
        bad = ((cl[a] != "SELF_CONSISTENCY") & (cl[b] == "SELF_CONSISTENCY")).sum()
        nest_ok &= bad == 0
    say(f"[A] classifier nesting NARROW<=MID<=WIDE violated on {0 if nest_ok else '>0'} clauses")

    order = sorted(cl.script.unique(), key=lambda s: hashlib.md5(s.encode()).hexdigest())
    grid = []
    for k in SAMPLES:
        keep = set(order[:k])
        sub = cl[cl.script.isin(keep)]
        for c in CLASSIFIERS:
            v = sub[c].value_counts()
            n = len(sub)
            grid.append(dict(sample=k, n_scripts=sub.script.nunique(), n_clauses=n, classifier=c,
                             self_consistency=int(v.get("SELF_CONSISTENCY", 0)),
                             repro_const=int(v.get("REPRO_CONST", 0)),
                             repro_artefact=int(v.get("REPRO_ARTEFACT", 0)),
                             unreadable=int(v.get("UNREADABLE", 0)),
                             share_self=v.get("SELF_CONSISTENCY", 0) / n if n else np.nan))
    g = pd.DataFrame(grid)
    say("\n[A] ALL 9 GRID POINTS (share_self = share of clauses blind to vintage)")
    say(g.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    byform = (cl.groupby(["form", HEADLINE]).size().unstack(fill_value=0))
    byform["n"] = byform.sum(axis=1)
    byform["share_self"] = byform.get("SELF_CONSISTENCY", 0) / byform["n"]
    say(f"\n[A] by FORM at classifier={HEADLINE}, full census")
    say(byform.to_string(float_format=lambda x: f"{x:.4f}"))

    # script-level: a script is vintage-blind if ALL of its clauses are SELF
    per = cl.groupby("script")[HEADLINE].apply(lambda s: (s == "SELF_CONSISTENCY").all())
    say(f"\n[A] scripts whose EVERY clause is SELF_CONSISTENCY: {int(per.sum())} / {len(per)} "
        f"({per.mean():.4f})")
    return cl, g, byform, per


# ============================================ [B] THE MECHANISM (idea 516) ====
def leg_b(cl: pd.DataFrame):
    if not I516.exists():
        say("[B] idea 516 scripts.csv absent — leg skipped")
        return pd.DataFrame()
    s516 = pd.read_csv(I516)
    ov = cl[cl.script.isin(set(s516.file))]
    say(f"\n[B] idea 516 re-executed {len(s516)} scripts; {ov.script.nunique()} of them carry "
        f"census clauses ({len(ov)} clauses)")
    if len(ov) == 0:
        return pd.DataFrame()
    v = ov[HEADLINE].value_counts()
    say(f"[B] those clauses at {HEADLINE}: SELF {int(v.get('SELF_CONSISTENCY',0))}  "
        f"CONST {int(v.get('REPRO_CONST',0))}  ARTEFACT {int(v.get('REPRO_ARTEFACT',0))}  "
        f"-> share_self {v.get('SELF_CONSISTENCY',0)/len(ov):.4f}")
    m = ov.merge(s516[["file", "cause", "worst_move"]], left_on="script", right_on="file")
    by = m.groupby("cause").agg(n_clauses=("script", "size"),
                                n_scripts=("script", "nunique"),
                                share_self=(HEADLINE, lambda s: (s == "SELF_CONSISTENCY").mean()),
                                worst_move=("worst_move", "max")).reset_index()
    say("[B] by idea 516's own cause column")
    say(by.to_string(index=False, float_format=lambda x: f"{x:.4g}"))
    return by


def leg_b2(cl: pd.DataFrame):
    """Did the record's gates that DID run fail more often when they were REPRODUCTION gates?
    idea 515 recorded (observed, bar, passed) for every gate it reached, without raising."""
    if not GATES515.exists():
        say("[B2] idea 515 gates.csv absent — leg skipped")
        return pd.DataFrame()
    g = pd.read_csv(GATES515)
    m = cl.merge(g[["script", "gate_id", "observed", "bar", "passed"]],
                 on=["script", "gate_id"], how="inner")
    say(f"\n[B2] {len(m)} of {len(cl)} clauses were actually REACHED by idea 515's re-execution")
    t = m.groupby(HEADLINE).agg(n=("passed", "size"), pass_rate=("passed", "mean"),
                                med_observed=("observed", "median")).reset_index()
    say(t.to_string(index=False, float_format=lambda x: f"{x:.4g}"))
    return t


# ================================================ [C] PROTOCOL / RULE 8 =======
def arm_weights(px, band, gross):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, band), 0.0)


def arm_metrics(px, band, gross, start):
    r = backtest(px, arm_weights(px, band, gross), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    oos = r.loc["2017-01-01":]
    mo = metrics(oos)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"],
                H2=m2["Sharpe"], isS=metrics(r.loc[:"2016-12-31"])["Sharpe"],
                oosC=mo["CAGR"], oosS=mo["Sharpe"], oosD=mo["MaxDD"])


def keep_paths(a, base, spy, spy_oos):
    p4a = int(a["H1"] > base["H1"] and a["H2"] > base["H2"] and a["MaxDD"] >= base["MaxDD"])
    m4a = min(a["H1"] - base["H1"], a["H2"] - base["H2"], a["MaxDD"] - base["MaxDD"])
    legs = [a["H1"] - spy["H1"], a["H2"] - spy["H2"], a["oosS"] - spy_oos["Sharpe"],
            a["MaxDD"] - 0.60 * spy["MaxDD"], a["CAGR"] - 0.70 * spy["CAGR"]]
    p4b = int(all(x > 0 for x in legs[:3]) and legs[3] >= 0 and legs[4] >= 0)
    return p4a, m4a, p4b, min(legs)


def leg_c():
    px = load_universe()
    start = px.index[260]
    say(f"\n[C] U56 panel {px.shape}, {px.index[0].date()} -> {px.index[-1].date()}, "
        f"metrics from {start.date()}, {COST_BPS} bps, freq={FREQ}, t+1 (engine)")
    pxv = px.iloc[:-VINTAGE_DAYS]
    say(f"[C] VINTAGE STEP: panel truncated to {pxv.index[-1].date()} "
        f"({VINTAGE_DAYS} trading days, APPEND channel only)")

    bands = [0.00, 0.01, 0.02, 0.03, 0.05, 0.08]
    grosses = [0.55, 0.75, 0.95, 1.00, 1.10]

    res = {}
    for tag, P in (("now", px), ("vintage", pxv)):
        st = P.index[260]
        base = metrics_pack(P, rules_v2_weights(P), st)
        spy = metrics_pack_series(P["SPY"].pct_change().fillna(0).loc[st:])
        spy_oos = metrics(P["SPY"].pct_change().fillna(0).loc[st:].loc["2017-01-01":])
        rows = []
        for b in bands:
            for g in grosses:
                a = arm_metrics(P, b, g, st)
                p4a, m4a, p4b, m4b = keep_paths(a, base, spy, spy_oos)
                rows.append(dict(band=b, gross=g, **a, pass4a=p4a, margin4a=m4a,
                                 pass4b=p4b, margin4b=m4b))
        res[tag] = (pd.DataFrame(rows), base, spy, spy_oos)

    now, base, spy, spy_oos = res["now"]
    say(f"[C] comparands (now): RULES v2 CAGR {base['CAGR']:.4f} Sharpe {base['Sharpe']:.4f} "
        f"MaxDD {base['MaxDD']:.4f} H1/H2 {base['H1']:.3f}/{base['H2']:.3f}")
    say(f"[C] comparands (now): SPY      CAGR {spy['CAGR']:.4f} Sharpe {spy['Sharpe']:.4f} "
        f"MaxDD {spy['MaxDD']:.4f} H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f}  "
        f"OOS Sharpe {spy_oos['Sharpe']:.4f} CAGR {spy_oos['CAGR']:.4f} MaxDD {spy_oos['MaxDD']:.4f}")
    say(f"[C] ALL {len(now)} ARMS (band x gross), full / halves / OOS, both KEEP paths")
    say(now.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"[C] 4a passes {int(now.pass4a.sum())} / {len(now)}; "
        f"4b passes {int(now.pass4b.sum())} / {len(now)}")

    # rule 8: band chosen on 2009-2016 alone (best IS Sharpe at each gross), evaluated 2017-2026
    wf = []
    for g in grosses:
        sub = now[now.gross == g]
        pick = sub.loc[sub.isS.idxmax()]
        wf.append(dict(gross=g, picked_band=pick["band"], isS=pick["isS"], oosC=pick["oosC"],
                       oosS=pick["oosS"], oosD=pick["oosD"],
                       spy_oosC=spy_oos["CAGR"], spy_oosS=spy_oos["Sharpe"],
                       spy_oosD=spy_oos["MaxDD"],
                       beats_spy_oosS=int(pick["oosS"] > spy_oos["Sharpe"]),
                       pass4a=int(pick["pass4a"]), pass4b=int(pick["pass4b"])))
    wfd = pd.DataFrame(wf)
    say("\n[C] RULE 8 walk-forward — band chosen on 2009-2016 ONLY, evaluated 2017-2026 untouched")
    say(wfd.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # the vintage delta a SELF-CONSISTENCY gate cannot see
    vin, _, _, _ = res["vintage"]
    j = now.merge(vin, on=["band", "gross"], suffixes=("", "_v"))
    for c in ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "oosS", "oosC"]:
        j["d" + c] = j[c] - j[c + "_v"]
    j["flip4a"] = (j.pass4a != j.pass4a_v).astype(int)
    j["flip4b"] = (j.pass4b != j.pass4b_v).astype(int)
    say(f"\n[C] VINTAGE STEP ({VINTAGE_DAYS} trading days) — what a self-consistency gate is blind to")
    say(j[["band", "gross", "dCAGR", "dSharpe", "dMaxDD", "dH1", "dH2", "doosS",
           "flip4a", "flip4b"]].to_string(index=False, float_format=lambda x: f"{x:.3e}"))
    say(f"[C] max |dSharpe| {j.dSharpe.abs().max():.3e}  max |dCAGR| {j.dCAGR.abs().max():.3e}  "
        f"max |dMaxDD| {j.dMaxDD.abs().max():.3e}  "
        f"4a flips {int(j.flip4a.sum())}/{len(j)}  4b flips {int(j.flip4b.sum())}/{len(j)}")
    say(f"[C] every one of these deltas is invisible to a gate whose two sides are both computed "
        f"inside one run: the gate re-computes BOTH on the moved panel.")
    return now, wfd, j, base, spy, spy_oos


def metrics_pack(P, w, st):
    r = backtest(P, w, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[st:]
    return metrics_pack_series(r)


def metrics_pack_series(r):
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=m1["Sharpe"], H2=m2["Sharpe"])


# ===================================================================== MAIN ===
def main():
    say(f"IDEA 681 (cloud) — {STEM}")
    say(f"P1 classifier {CLASSIFIERS} (headline {HEADLINE}); P2 sample {SAMPLES}; "
        f"dataflow depth {DEPTH}; const floor {CONST_FLOOR}")

    say("\nREPRODUCTION GATES (recorded, non-raising; both sides committed)")
    cen = pd.read_csv(CENSUS)
    fc = cen.form.value_counts()
    gate("i515.clauses", len(cen) == 520, f"{len(cen)} vs published 520")
    gate("i515.tolerance", int(fc.get("tolerance", 0)) == 345, f"{int(fc.get('tolerance',0))} vs 345")
    gate("i515.exact", int(fc.get("exact", 0)) == 87, f"{int(fc.get('exact',0))} vs 87")
    gate("i515.structural", int(fc.get("structural", 0)) == 46, f"{int(fc.get('structural',0))} vs 46")
    gate("i515.count", int(fc.get("count", 0)) == 40, f"{int(fc.get('count',0))} vs 40")
    gate("i515.scripts", cen.script.nunique() == 151, f"{cen.script.nunique()} vs 151")
    if I516.exists():
        s516 = pd.read_csv(I516)
        gate("i516.scripts", len(s516) == 36, f"{len(s516)} vs published 36")
        moved = int((s516.worst_move > 5.094e-05).sum())
        gate("i516.moved", moved == 35, f"{moved} vs published 35")

    cl, g, byform, per = leg_a()
    by516 = leg_b(cl)
    reached = leg_b2(cl)
    now, wfd, vin, base, spy, spy_oos = leg_c()

    cl.to_csv(OUT / f"{STEM}.clauses.csv", index=False)
    g.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    byform.to_csv(OUT / f"{STEM}.byform.csv")
    if len(by516):
        by516.to_csv(OUT / f"{STEM}.i516.csv", index=False)
    if len(reached):
        reached.to_csv(OUT / f"{STEM}.reached.csv", index=False)
    now.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    wfd.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    vin.to_csv(OUT / f"{STEM}.vintage.csv", index=False)

    hl = g[(g["sample"] == SAMPLES[-1]) & (g["classifier"] == HEADLINE)].iloc[0]
    say(f"\nHEADLINE ({HEADLINE}, full census): {hl.self_consistency} of {hl.n_clauses} clauses "
        f"({hl.share_self:.4f}) are SELF-CONSISTENCY — structurally blind to vintage; "
        f"{hl.repro_const} committed-constant, {hl.repro_artefact} committed-artefact.")
    say(f"Range over the 9 grid points: share_self "
        f"{g.share_self.min():.4f} .. {g.share_self.max():.4f}")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

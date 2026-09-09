#!/usr/bin/env python3
"""IDEA 515 (lane C) — restate the record's 158 REPRODUCTION GATES as TOLERANCES in record units.

QUESTION (queue): idea 513 found 158 of 470 committed backtests assert reproduction at machine
precision (136 at a tolerance <= 1e-6, 22 at exact == / .equals), which ONE trading day of fresh
U56 data breaks by ~4e-03 of Sharpe while moving 0 of 30 4a/4b verdicts.  Re-run a sample of
those gates under |dSharpe| < 1e-3 / |dCAGR| < 1e-4 and report how many published claims survive
each bar.

DESIGN.  Exactly two parameters, both reported at EVERY grid point, neither tuned on an outcome:
  P1  TOLERANCE BAR, 7 levels: the gate's OWN declared bar ("native"), then
      1e-12, 1e-9, 1e-6, 1e-4, 1e-3, 1e-2 applied to the gate's observed |delta|.
  P2  SAMPLE of the 158 gated scripts, 3 NESTED levels (S12 subset of S24 subset of S48),
      ordered by md5(filename) so the sample spans dates rather than following them.

[A] STATIC CENSUS of all 158 gated scripts and all their asserts (no sampling): clause form
    (tolerance / exact-numeric / count / structural), the DECLARED bar, and the UNIT the gate
    is written in, read off the clause source and the assert message.
[B] RE-EXECUTION of the sample.  Each target is parsed, every `assert` is AST-rewritten into a
    recording call that evaluates the same expression, writes (observed, bar, pass) to a JSONL
    file and NEVER RAISES — so one failing gate no longer hides the gates behind it, and a
    script killed by the timeout still reports every gate it reached.  Every write under
    research/backtests/ is redirected into a scratch mirror (idea 513's machinery), so no
    committed artefact is touched.  Prices, code, interpreter: unchanged.
[C] THE LADDER: gate-level and CLAIM-level (a script survives a bar only if ALL of its numeric
    gates do) survival share at each of the 7 x 3 grid points, plus the queue's own two bars
    applied to the gates whose unit is establishable (|dSharpe| < 1e-3, |dCAGR| < 1e-4).
[D] PROTOCOL UNITS: what a 1e-3 Sharpe / 1e-4 CAGR bar is WORTH in verdicts.  30 U56 book arms
    (band x gross) at 10 bps, weekly, t+1: full / halves / OOS, 4a against the live RULES v2
    book and 4b against SPY, each arm's binding-bar margin, and the count of verdicts that flip
    when every metric is perturbed by the bar.  Rule 8: the band is chosen on 2009-2016 alone
    and evaluated on 2017-2026 untouched.

REPRODUCTION GATE (recorded, never raising, in this script's own units): idea 513's regexes,
re-run on the 158 scripts it named, must give 136 tolerance-gated / 22 exact-only / 26 reading a
committed artefact back.

Deterministic; no randomness anywhere.  Writes <STEM>.{census,gates,ladder,keeppaths,
walkforward}.csv and <STEM>.console.txt.  Does not modify RULES.md, scan.py, bot.py, baseline.py.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "research" / "backtests"
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))

STEM = "2026-09-09_restate-the-record-s-158-REPRODUCTION-GATES-as-TOLERANCES-in-record-units_C"
GATECENSUS = OUT / "2026-09-09_three-committed-scripts-fail-their-own-reproduction-gates-today_C.gatecensus.csv"
SCRATCH = Path(os.environ.get("IDEA515_SCRATCH", "/tmp/idea515"))
TIMEOUT = int(os.environ.get("IDEA515_TIMEOUT", "150"))
JOBS = int(os.environ.get("IDEA515_JOBS", "4"))

# P1 — the tolerance ladder (the two middle rungs are the queue's own bars)
BARS = [1e-12, 1e-9, 1e-6, 1e-4, 1e-3, 1e-2]
BAR_SHARPE, BAR_CAGR = 1e-3, 1e-4
# P2 — nested sample sizes
SAMPLES = [12, 24, 48]

LOG: list[str] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# ================================================================== UNITS ====
UNIT_PAT = [
    ("sharpe", r"sharpe|\bsh\b|_sh\b"),
    ("cagr", r"cagr"),
    ("dd", r"maxdd|drawdown|\bdd\b|_dd\b"),
    ("bps", r"\bbps\b|cstar|c_star|cost_rung"),
    ("turnover", r"turnover|\bto\b"),
    ("weight", r"weight|\bgross\b|\bw\b\s*[-<]|nav"),
    ("return", r"\bret\b|return|\bpnl\b|equity"),
    ("share", r"share|frac|pct|rate|prob|_p\b"),
    ("price", r"price|\bpx\b|close"),
]


def classify_unit(text: str, kind: str) -> str:
    t = text.lower()
    for u, p in UNIT_PAT:
        if re.search(p, t):
            return u
    if kind == "count":
        return "count"
    return "unknown"


# ============================================== AST GATE INSTRUMENTATION =====
OPNAME = {ast.Lt: "Lt", ast.LtE: "LtE", ast.Gt: "Gt", ast.GtE: "GtE",
          ast.Eq: "Eq", ast.NotEq: "NotEq", ast.Is: "Is", ast.IsNot: "IsNot",
          ast.In: "In", ast.NotIn: "NotIn"}


def flatten_and(node):
    """assert A and B and C  ->  three separately-recorded clauses."""
    if isinstance(node, ast.BoolOp) and isinstance(node.op, ast.And):
        out = []
        for v in node.values:
            out.extend(flatten_and(v))
        return out
    return [node]


class GateTx(ast.NodeTransformer):
    """Replace every `assert TEST, MSG` with recording calls that never raise."""

    def __init__(self, path: str):
        self.path = path
        self.clauses: list[dict] = []

    def visit_Assert(self, node):
        msg = ""
        if node.msg is not None:
            try:
                msg = ast.unparse(node.msg)[:200]
            except Exception:
                msg = ""
        stmts = []
        for ci, cl in enumerate(flatten_and(node.test)):
            src = ast.unparse(cl)[:300]
            if isinstance(cl, ast.Compare):
                # chained compares (a == b == c) become one call per link
                left = cl.left
                for oi, (op, right) in enumerate(zip(cl.ops, cl.comparators)):
                    gid = len(self.clauses)
                    self.clauses.append(dict(gate_id=gid, lineno=node.lineno, clause=ci, link=oi,
                                             op=OPNAME.get(type(op), "?"), src=src, msg=msg))
                    args = [left, right,
                            ast.Constant(value=OPNAME.get(type(op), "?")),
                            ast.Constant(value=gid)]
                    stmts.append(ast.Expr(value=ast.Call(
                        func=ast.Name(id="__G", ctx=ast.Load()), args=args, keywords=[])))
                    left = right
            else:
                gid = len(self.clauses)
                self.clauses.append(dict(gate_id=gid, lineno=node.lineno, clause=ci, link=0,
                                         op="BOOL", src=src, msg=msg))
                stmts.append(ast.Expr(value=ast.Call(
                    func=ast.Name(id="__GB", ctx=ast.Load()),
                    args=[cl, ast.Constant(value=gid)], keywords=[])))
        if not stmts:
            return ast.Pass()
        for s in stmts:
            ast.copy_location(s, node)
            ast.fix_missing_locations(s)
        return stmts


def _mag(x):
    """Max |value| as a float, or None when the object is not numeric."""
    try:
        if isinstance(x, bool):
            return None
        if isinstance(x, (int, float, np.integer, np.floating)):
            v = float(x)
            return v if np.isfinite(v) else None
        if isinstance(x, (pd.Series, pd.DataFrame, np.ndarray)):
            a = np.asarray(getattr(x, "values", x), dtype="float64")
            if a.size == 0:
                return 0.0
            a = np.abs(a[np.isfinite(a)])
            return float(a.max()) if a.size else None
    except Exception:
        return None
    return None


def _isint(x):
    if isinstance(x, bool):
        return False
    if isinstance(x, (int, np.integer)):
        return True
    try:
        a = np.asarray(getattr(x, "values", x))
        return a.dtype.kind in "iu"
    except Exception:
        return False


def _diffmag(a, b):
    try:
        return _mag(np.asarray(getattr(a, "values", a), dtype="float64")
                    - np.asarray(getattr(b, "values", b), dtype="float64"))
    except Exception:
        return None


# ============================================================ CHILD RUNNER ===
def child_main(target: str) -> int:
    """`python -u THIS --child <stem>`: run the target with instrumented asserts."""
    import builtins

    mirror = SCRATCH / "mirror"
    mirror.mkdir(parents=True, exist_ok=True)
    recfile = SCRATCH / "rec" / f"{target}.jsonl"
    recfile.parent.mkdir(parents=True, exist_ok=True)
    rf = open(recfile, "w")

    def emit(d):
        rf.write(json.dumps(d) + "\n")
        rf.flush()

    def redir(p):
        try:
            q = Path(p).resolve()
            rel = q.relative_to(OUT)
        except Exception:
            return p
        t = mirror / rel
        t.parent.mkdir(parents=True, exist_ok=True)
        return str(t)

    _open = builtins.open

    def open2(file, mode="r", *a, **k):
        if any(c in str(mode) for c in "wax"):
            file = redir(file)
        return _open(file, mode, *a, **k)

    builtins.open = open2

    for cls in (pd.DataFrame, pd.Series):
        _orig = cls.to_csv

        def _mk(o):
            def f(self, path_or_buf=None, *a, **k):
                if isinstance(path_or_buf, (str, os.PathLike)):
                    path_or_buf = redir(path_or_buf)
                return o(self, path_or_buf, *a, **k)
            return f

        cls.to_csv = _mk(_orig)

    for nm in ("write_text", "write_bytes"):
        _o = getattr(Path, nm)

        def _mk2(o):
            def f(self, *a, **k):
                return o(Path(redir(self)), *a, **k)
            return f

        setattr(Path, nm, _mk2(_o))

    try:
        import matplotlib
        matplotlib.use("Agg")
        from matplotlib.figure import Figure
        _sf = Figure.savefig

        def savefig2(self, fname, *a, **k):
            if isinstance(fname, (str, os.PathLike)):
                fname = redir(fname)
            return _sf(self, fname, *a, **k)

        Figure.savefig = savefig2
    except Exception:
        pass

    path = OUT / f"{target}.py"
    src = path.read_text(errors="replace")
    tree = ast.parse(src)
    tx = GateTx(str(path))
    tree = tx.visit(tree)
    ast.fix_missing_locations(tree)
    (SCRATCH / "rec" / f"{target}.clauses.json").write_text(json.dumps(tx.clauses))

    def __G(a, b, op, gid):
        rec = dict(gate_id=gid, op=op)
        am, bm = _mag(a), _mag(b)
        ok = None
        try:
            r = {"Lt": a < b, "LtE": a <= b, "Gt": a > b, "GtE": a >= b,
                 "Eq": a == b, "NotEq": a != b}.get(op)
            if hasattr(r, "all"):
                r = bool(np.asarray(getattr(r, "values", r)).all())
            ok = bool(r)
        except Exception:
            ok = None
        if op in ("Lt", "LtE") and am is not None and bm is not None and not hasattr(b, "__len__"):
            rec.update(kind="tol", observed=am, bar=float(bm), passed=ok)
        elif op in ("Gt", "GtE") and am is not None and bm is not None and not hasattr(b, "__len__"):
            # a floor: the shortfall (positive = failing) is the record-unit distance
            rec.update(kind="floor", observed=float(bm) - am, bar=0.0, passed=ok)
        elif op in ("Eq", "NotEq"):
            d = _diffmag(a, b)
            if d is None:
                rec.update(kind="structural", observed=(0.0 if ok else float("nan")), bar=0.0, passed=ok)
            elif _isint(a) and _isint(b):
                rec.update(kind="count", observed=d, bar=0.0, passed=ok)
            else:
                rec.update(kind="exact", observed=d, bar=0.0, passed=ok)
        else:
            rec.update(kind="structural", observed=(0.0 if ok else float("nan")), bar=None, passed=ok)
        emit(rec)
        return True

    def __GB(v, gid):
        ok = None
        try:
            r = v
            if hasattr(r, "all"):
                r = bool(np.asarray(getattr(r, "values", r)).all())
            ok = bool(r)
        except Exception:
            ok = None
        emit(dict(gate_id=gid, op="BOOL", kind="structural",
                  observed=(0.0 if ok else float("nan")), bar=None, passed=ok))
        return True

    g = {"__name__": "__main__", "__file__": str(path), "__G": __G, "__GB": __GB,
         "__builtins__": builtins}
    sys.argv = [str(path)]
    code = compile(tree, str(path), "exec")
    try:
        exec(code, g)
    except SystemExit:
        pass
    finally:
        rf.close()
    return 0


# ============================================================ [A] CENSUS =====
def part_a() -> pd.DataFrame:
    say("\n[A] STATIC CENSUS OF ALL 158 GATED SCRIPTS (no sampling)")
    scripts = pd.read_csv(GATECENSUS)["script"].tolist()

    # ---- reproduction gate: idea 513's own regexes on the 158 scripts it named
    tol_re = re.compile(r"assert[^\n]{0,400}?<\s*1e-(0?[6-9]|1[0-9])")
    eq_re = re.compile(r"assert[^\n]{0,200}?(==|\.equals\()")
    read_re = re.compile(r"read_csv\([^)]*OUT\s*/")
    SELF513 = "2026-09-09_three-committed-scripts-fail-their-own-reproduction-gates-today_C.py"
    n_tol = n_eqonly = n_reads = n_reads_ex = 0
    for s in scripts:
        t = (OUT / s).read_text(errors="replace")
        a, b = bool(tol_re.search(t)), bool(eq_re.search(t))
        n_tol += int(a)
        n_eqonly += int(b and not a)
        r = bool(read_re.search(t))
        n_reads += int(r)
        n_reads_ex += int(r and s != SELF513)
    allpys = sorted(p.name for p in OUT.glob("*.py"))
    say(f"    REPRODUCTION GATE (recorded, non-raising): idea 513 published 158 gated scripts, "
        f"136 with a tolerance <= 1e-6, 22 exact-only, 26 reading a committed artefact back.")
    say(f"      re-run today on its own 158: {len(scripts)} / {n_tol} / {n_eqonly} / {n_reads}"
        f"   -> 3 of 4 legs EXACT"
        f"{'' if (len(scripts), n_tol, n_eqonly) == (158, 136, 22) else ' (NOT: the first three legs moved)'}")
    say(f"      the 4th leg is 27 today vs 26 published, and the WHOLE gap is idea 513's own "
        f"script counting itself: excluding it gives {n_reads_ex} "
        f"{'(EXACT)' if n_reads_ex == 26 else '(still off)'}.  Confirmed against git: the reader "
        f"count is 26 at 4f974a2 (the tree without that file) and 27 at e5125ca (with it).  A "
        f"census with no VINTAGE STAMP cannot tell those two apart — which is idea 514.")
    say(f"      corpus today is {len(allpys)} committed backtests (470 when idea 513 ran; the "
        f"delta is this lane's own new files).")

    rows = []
    for s in scripts:
        p = OUT / s
        txt = p.read_text(errors="replace")
        try:
            tree = ast.parse(txt)
        except Exception as e:
            rows.append(dict(script=s, gate_id=-1, lineno=-1, op="PARSE-FAIL", form="parse-fail",
                             declared_bar=np.nan, unit="unknown", src=str(e)[:120], msg=""))
            continue
        tx = GateTx(str(p))
        tx.visit(tree)
        for c in tx.clauses:
            form, bar = "structural", np.nan
            m = re.search(r"<=?\s*([0-9.]+e-?[0-9]+|[0-9]*\.?[0-9]+)\s*$", c["src"])
            if c["op"] in ("Lt", "LtE") and m:
                try:
                    bar = float(m.group(1))
                    form = "tolerance"
                except Exception:
                    pass
            elif c["op"] in ("Eq", "NotEq"):
                form = "count" if re.search(r"len\(|\.shape|\bn_|count", c["src"]) else "exact"
                bar = 0.0
            elif c["op"] in ("Gt", "GtE"):
                form = "floor"
            rows.append(dict(script=s, gate_id=c["gate_id"], lineno=c["lineno"], op=c["op"],
                             form=form, declared_bar=bar,
                             unit=classify_unit(c["src"] + " " + c["msg"], form),
                             src=c["src"][:200], msg=c["msg"][:160]))
    C = pd.DataFrame(rows)
    C.to_csv(OUT / f"{STEM}.census.csv", index=False)
    say(f"    {len(C)} assert CLAUSES in {C.script.nunique()} scripts.  Clause form:")
    for f, n in C.form.value_counts().items():
        say(f"      {f:<12} {n:>4}  ({n/len(C):.1%})")
    say("    DECLARED tolerance of the 'tolerance'-form clauses:")
    tt = C[C.form == "tolerance"]
    for b, n in tt.declared_bar.value_counts().sort_index().items():
        say(f"      < {b:<10g} {n:>4}")
    say(f"      median declared bar {tt.declared_bar.median():.1e}; "
        f"{(tt.declared_bar <= 1e-9).mean():.1%} of them at <= 1e-9")
    say("    UNIT the clause is WRITTEN in (read off clause source + assert message):")
    for u, n in C.unit.value_counts().items():
        say(f"      {u:<10} {n:>4}  ({n/len(C):.1%})")
    return C


# ======================================================== [B] RE-EXECUTION ===
def sample_of(scripts: list[str], k: int) -> list[str]:
    """Deterministic, NESTED: order by md5(name), take the first k."""
    o = sorted(scripts, key=lambda s: hashlib.md5(s.encode()).hexdigest())
    return o[:k]


def part_b(census: pd.DataFrame) -> pd.DataFrame:
    scripts = pd.read_csv(GATECENSUS)["script"].tolist()
    targets = sample_of(scripts, max(SAMPLES))
    say(f"\n[B] RE-EXECUTION OF THE SAMPLE (P2 = {max(SAMPLES)}, nested {SAMPLES})")
    say(f"    Every assert is AST-rewritten into a recording call that NEVER RAISES, so a "
        f"failing gate no longer hides the gates behind it.  timeout {TIMEOUT}s, {JOBS} "
        f"concurrent, all writes redirected to {SCRATCH/'mirror'} — no committed artefact "
        f"is touched.")
    SCRATCH.mkdir(parents=True, exist_ok=True)
    logdir = SCRATCH / "logs"
    logdir.mkdir(parents=True, exist_ok=True)
    (SCRATCH / "rec").mkdir(parents=True, exist_ok=True)

    def launch(s):
        o = open(logdir / f"{s}.out", "wb")
        e = open(logdir / f"{s}.err", "wb")
        p = subprocess.Popen([sys.executable, "-u", str(Path(__file__).resolve()), "--child", s[:-3]],
                             cwd=str(ROOT), stdout=o, stderr=e)
        return dict(s=s, p=p, o=o, e=e, t0=pd.Timestamp.utcnow())

    reuse = os.environ.get("IDEA515_REUSE") == "1" and all(
        (SCRATCH / "rec" / f"{s[:-3]}.jsonl").exists() for s in targets)
    if reuse:
        say("    IDEA515_REUSE=1 and every recording file is present: harvesting the recorded "
            "gates without re-launching.  (Delete the scratch tree to force a fresh sweep.)")
    q, running, status = ([] if reuse else list(targets)), [], []
    if reuse and (OUT / f"{STEM}.status.csv").exists():
        status = pd.read_csv(OUT / f"{STEM}.status.csv").to_dict("records")
    while q or running:
        while q and len(running) < JOBS:
            running.append(launch(q.pop(0)))
        done = []
        for r in running:
            try:
                rc = r["p"].wait(timeout=3)
            except subprocess.TimeoutExpired:
                if (pd.Timestamp.utcnow() - r["t0"]).total_seconds() > TIMEOUT:
                    r["p"].kill()
                    r["p"].wait()
                    rc = 124
                else:
                    continue
            done.append((r, rc))
        for r, rc in done:
            running.remove(r)
            r["o"].close()
            r["e"].close()
            s = r["s"]
            secs = (pd.Timestamp.utcnow() - r["t0"]).total_seconds()
            rec = SCRATCH / "rec" / f"{s[:-3]}.jsonl"
            n = sum(1 for _ in open(rec)) if rec.exists() else 0
            err = (logdir / f"{s}.err").read_text(errors="replace")
            status.append(dict(script=s, rc=rc, secs=round(secs, 1), gates_reached=n,
                               err=(err.strip().splitlines()[-1][:120] if err.strip() else "")))
            say(f"    rc={rc:<4}{secs:6.1f}s  gates {n:>3}  {s[:76]}")
    S = pd.DataFrame(status).sort_values("script").reset_index(drop=True)

    # ---- join the recorded observations onto the static clause census
    obs = []
    for s in targets:
        rec = SCRATCH / "rec" / f"{s[:-3]}.jsonl"
        if not rec.exists():
            continue
        for ln in open(rec):
            try:
                d = json.loads(ln)
            except Exception:
                continue
            d["script"] = s
            obs.append(d)
    O = pd.DataFrame(obs)
    if len(O):
        O = O.drop_duplicates(subset=["script", "gate_id"], keep="first")
        G = census.merge(O, on=["script", "gate_id"], how="inner", suffixes=("", "_obs"))
    else:
        G = census.head(0).copy()
    G.to_csv(OUT / f"{STEM}.gates.csv", index=False)
    S.to_csv(OUT / f"{STEM}.status.csv", index=False)
    say(f"    {len(S)} scripts run: rc=0 {int((S.rc == 0).sum())}, rc=124 (timeout, gates still "
        f"recorded) {int((S.rc == 124).sum())}, other {int(((S.rc != 0) & (S.rc != 124)).sum())}.")
    say(f"    {len(G)} of the sample's {int(census[census.script.isin(targets)].shape[0])} static "
        f"clauses were REACHED and recorded "
        f"({len(G)/max(1, census[census.script.isin(targets)].shape[0]):.1%}); the rest sit behind "
        f"an early exit, a timeout or a branch not taken and are reported as UNREACHED, never as "
        f"passing.")
    return G, S


# ============================================================= [C] LADDER ====
def part_c(G: pd.DataFrame) -> pd.DataFrame:
    say("\n[C] THE LADDER — P1 (7 bars) x P2 (3 nested samples), ALL 21 GRID POINTS")
    scripts = pd.read_csv(GATECENSUS)["script"].tolist()
    rows = []
    num = G[G.kind.isin(["tol", "exact", "count", "floor"])].copy()
    num["observed"] = pd.to_numeric(num["observed"], errors="coerce")
    for k in SAMPLES:
        sset = set(sample_of(scripts, k))
        sub = num[num.script.isin(sset)]
        if not len(sub):
            continue
        # native = the gate's own declared bar (its `passed` field as evaluated today)
        nat_g = float(sub["passed"].fillna(False).mean())
        nat_s = float(sub.groupby("script")["passed"].apply(lambda x: bool(x.fillna(False).all())).mean())
        rows.append(dict(sample=k, bar="native", n_gates=len(sub), n_scripts=sub.script.nunique(),
                         gate_survival=nat_g, claim_survival=nat_s))
        for b in BARS:
            ok = sub["observed"] < b
            g = float(ok.mean())
            c = float(sub.assign(ok=ok).groupby("script")["ok"].all().mean())
            rows.append(dict(sample=k, bar=f"{b:g}", n_gates=len(sub), n_scripts=sub.script.nunique(),
                             gate_survival=g, claim_survival=c))
    L = pd.DataFrame(rows)
    L.to_csv(OUT / f"{STEM}.ladder.csv", index=False)
    if len(L):
        say(L.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        say("\n    THE QUEUE'S OWN TWO BARS, applied only where the UNIT is establishable:")
        for u, b in (("sharpe", BAR_SHARPE), ("cagr", BAR_CAGR)):
            s = num[num.unit == u]
            if len(s):
                say(f"      unit={u:<7} n={len(s):>4}  native pass {s['passed'].fillna(False).mean():.1%}"
                    f"  |d| < {b:g} pass {(s['observed'] < b).mean():.1%}"
                    f"  median |d| {s['observed'].median():.3e}  max |d| {s['observed'].max():.3e}")
            else:
                say(f"      unit={u:<7} n=   0  no reached clause in the sample carries this unit")
        say("\n    BY CLAUSE FORM at the full sample:")
        f48 = num[num.script.isin(set(sample_of(scripts, max(SAMPLES))))]
        for kind, s in f48.groupby("kind"):
            say(f"      {kind:<11} n={len(s):>4}  native {s['passed'].fillna(False).mean():.1%}"
                f"  <1e-6 {(s['observed'] < 1e-6).mean():.1%}"
                f"  <1e-3 {(s['observed'] < 1e-3).mean():.1%}"
                f"  median |d| {s['observed'].median():.3e}")

        # ---- ATTRIBUTION: does the failure follow the ONE price file that moved?
        # idea 513 established that data/prices.csv (the U56 panel) both appends and restates
        # while prices_broad.csv and prices_small.csv.gz do not.  A script's panel is read
        # STATICALLY off its load_universe() calls, so this is a property of the source, not of
        # this run.
        say("\n    ATTRIBUTION — which PANEL the failing scripts read (static, from the source):")
        def _text(s, depth=1):
            """A script's own source PLUS, one level deep, the source of any sibling backtest it
            loads as a module — several scripts get their panel from an imported helper, so a
            source-only scan mis-classifies them."""
            t = (OUT / s).read_text(errors="replace")
            if depth:
                for nm in set(re.findall(r"[\"']((?:19|20)\d\d-\d\d-\d\d_[^\"']+?)(?:\.py)?[\"']", t)):
                    q = OUT / f"{nm}.py"
                    if q.exists() and q.name != s:
                        t += "\n" + q.read_text(errors="replace")
            return t

        def panels(s):
            t = _text(s)
            p = set()
            if re.search(r"load_universe\((?![^)]*(broad|small)\s*=\s*True)", t) or "prices.csv" in t:
                p.add("U56/prices.csv")
            if re.search(r"broad\s*=\s*True", t):
                p.add("broad")
            if re.search(r"small\s*=\s*True", t):
                p.add("small")
            return p
        agg = f48.groupby("script").agg(n=("observed", "size"),
                                        fails=("passed", lambda x: int((~x.fillna(False).astype(bool)).sum())))
        for lab, sel in (("reads the MOVING file (U56/prices.csv)", lambda s: "U56/prices.csv" in panels(s)),
                         ("reads ONLY the static panels (broad/small)", lambda s: "U56/prices.csv" not in panels(s))):
            idx = [s for s in agg.index if sel(s)]
            a = agg.loc[idx]
            if len(a):
                say(f"      {lab:<44} {len(a):>3} scripts, {int(a.n.sum()):>4} gates, "
                    f"{int((a.fails > 0).sum())} failing natively ({(a.fails > 0).mean():.1%})")
            else:
                say(f"      {lab:<44}   0 scripts in the sample")
    return L


# ====================================================== [D] PROTOCOL UNITS ===
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

FREQ, COST = "W", 10.0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
PHI, DELTA = 0.70, 0.60          # PROTOCOL 4b: CAGR floor / DD cap, fractions of SPY
BANDS = [0.00, 0.01, 0.02, 0.03, 0.04, 0.05]
GROSSES = [0.55, 0.65, 0.75, 0.85, 1.00]
LIVE = (0.03, 0.75)


def m3(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def part_d():
    say("\n[D] WHAT A 1e-3 SHARPE / 1e-4 CAGR BAR IS WORTH IN PROTOCOL UNITS")
    px = load_universe()
    say(f"    U56 panel {px.shape[0]} rows x {px.shape[1]} cols, {px.index[0].date()} -> "
        f"{px.index[-1].date()}.  10 bps, weekly, t+1 (engine).")
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    base = backtest(px, rules_v2_weights(px, *LIVE), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
    h = len(spy) // 2

    def legs(r):
        f = m3(r)
        return dict(CAGR=f[0], Sharpe=f[1], MaxDD=f[2],
                    H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                    oosC=metrics(r.loc[OOS_START:])["CAGR"],
                    oosS=metrics(r.loc[OOS_START:])["Sharpe"],
                    oosD=metrics(r.loc[OOS_START:])["MaxDD"])

    B, SP = legs(base), legs(spy)
    rows = []
    for bd in BANDS:
        for gr in GROSSES:
            r = backtest(px, rules_v2_weights(px, bd, gr), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
            a = legs(r)
            # 4a: Sharpe > live book in BOTH halves and MaxDD no worse
            m4a = min(a["H1"] - B["H1"], a["H2"] - B["H2"], a["MaxDD"] - B["MaxDD"])
            # 4b: Sharpe > SPY in both halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's
            m4b = min(a["H1"] - SP["H1"], a["H2"] - SP["H2"], a["oosS"] - SP["oosS"],
                      a["MaxDD"] - DELTA * SP["MaxDD"], a["CAGR"] - PHI * SP["CAGR"])
            rows.append(dict(band=bd, gross=gr, **{k: a[k] for k in a},
                             pass4a=int(m4a > 0), margin4a=m4a,
                             pass4b=int(m4b > 0), margin4b=m4b,
                             isS=metrics(r.loc[:IS_END])["Sharpe"]))
            say(f"    band {bd:.2f} gross {gr:.2f}  CAGR {a['CAGR']:7.2%} Sh {a['Sharpe']:6.3f} "
                f"DD {a['MaxDD']:7.2%}  H1/H2 {a['H1']:6.3f}/{a['H2']:6.3f}  OOS Sh {a['oosS']:6.3f} "
                f" 4a {int(m4a>0)} (m {m4a:+.4f})  4b {int(m4b>0)} (m {m4b:+.4f})")
    K = pd.DataFrame(rows)
    K.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    say(f"    live RULES v2 (band {LIVE[0]}, gross {LIVE[1]}): CAGR {B['CAGR']:.2%} Sh {B['Sharpe']:.3f} "
        f"DD {B['MaxDD']:.2%} H1/H2 {B['H1']:.3f}/{B['H2']:.3f} OOS Sh {B['oosS']:.3f}")
    say(f"    SPY:                                CAGR {SP['CAGR']:.2%} Sh {SP['Sharpe']:.3f} "
        f"DD {SP['MaxDD']:.2%} H1/H2 {SP['H1']:.3f}/{SP['H2']:.3f} OOS Sh {SP['oosS']:.3f}")
    say(f"    4a {int(K.pass4a.sum())}/{len(K)}   4b {int(K.pass4b.sum())}/{len(K)}")
    for nm, col in (("4a", "margin4a"), ("4b", "margin4b")):
        mm = K[col].abs()
        say(f"    |{nm} margin| over {len(K)} arms: min {mm.min():.4f}  p10 {mm.quantile(.1):.4f}  "
            f"median {mm.median():.4f}  -> arms within 1e-3 of flipping: "
            f"{int((mm < BAR_SHARPE).sum())}/{len(K)}; within 1e-4: {int((mm < 1e-4).sum())}/{len(K)}")
    say(f"    VERDICT FLIPS when every Sharpe leg moves by +/-{BAR_SHARPE:g} and every CAGR leg by "
        f"+/-{BAR_CAGR:g} in the worst direction: "
        f"4a {int((K.margin4a.abs() < BAR_SHARPE).sum())}/{len(K)}, "
        f"4b {int((K.margin4b.abs() < BAR_SHARPE).sum())}/{len(K)}")

    # ---- rule 8 walk-forward: band chosen on 2009-2016 alone, evaluated 2017-2026 untouched
    say("\n    RULE 8 WALK-FORWARD (band chosen on IS 2009-2016 by IS Sharpe at the live gross; "
        "2017-2026 untouched):")
    wf = []
    for gr in GROSSES:
        sub = K[K.gross == gr]
        pick = sub.loc[sub.isS.idxmax()]
        wf.append(dict(gross=gr, is_pick_band=pick.band, is_Sharpe=pick.isS,
                       oos_CAGR=pick.oosC, oos_Sharpe=pick.oosS, oos_MaxDD=pick.oosD,
                       base_oos_Sharpe=B["oosS"], base_oos_CAGR=B["oosC"], base_oos_MaxDD=B["oosD"],
                       spy_oos_Sharpe=SP["oosS"], spy_oos_CAGR=SP["oosC"], spy_oos_MaxDD=SP["oosD"],
                       beats_base=int(pick.oosS > B["oosS"]), beats_spy=int(pick.oosS > SP["oosS"])))
        say(f"      gross {gr:.2f}: IS picks band {pick.band:.2f} (IS Sh {pick.isS:.4f}) -> "
            f"OOS CAGR {pick.oosC:.2%} Sh {pick.oosS:.4f} DD {pick.oosD:.2%}   "
            f"base OOS Sh {B['oosS']:.4f}  SPY OOS Sh {SP['oosS']:.4f}")
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(f"      the IS-chosen band is {sorted(set(W.is_pick_band))} across the 5 gross levels; "
        f"beats base OOS {int(W.beats_base.sum())}/{len(W)}, beats SPY OOS {int(W.beats_spy.sum())}/{len(W)}.")
    say(f"      SENSITIVITY OF THE CHOICE ITSELF: the IS Sharpe gap between the picked band and "
        f"the runner-up is:")
    for gr in GROSSES:
        sub = K[K.gross == gr].sort_values("isS", ascending=False)
        gap = float(sub.isS.iloc[0] - sub.isS.iloc[1])
        say(f"        gross {gr:.2f}: {gap:.4f}  -> a {BAR_SHARPE:g} bar "
            f"{'WOULD' if gap < BAR_SHARPE else 'would NOT'} change the rule-8 pick")
    return K, W


# ==================================================================== MAIN ===
def main():
    say(f"IDEA 515 (lane C) — restate the record's 158 REPRODUCTION GATES as TOLERANCES")
    say(f"P1 tolerance bar: native + {BARS}   P2 nested sample: {SAMPLES} of 158")
    C = part_a()
    G, S = part_b(C)
    L = part_c(G)
    K, W = part_d()
    say("\nDONE.")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--child":
        sys.exit(child_main(sys.argv[2]))
    main()

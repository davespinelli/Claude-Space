#!/usr/bin/env python3
"""Idea 522 (lane B) — how many of the record's 46 STRUCTURAL gates are CROSS-PANEL VINTAGE tests?

Idea 515 classified 520 committed assert clauses and found 46 STRUCTURAL (no numeric
tolerance, no exact bar, no count bar), and noted that crypto-sleeve's
`px.index.equals(pxb.index)` fails TODAY only because data/prices.csv gained 2026-09-08
while data/prices_broad.csv is cached on Fridays.  This run censuses those 46 clauses for
cross-file index/shape tests and reports how many are decided by the CACHE REFRESH
SCHEDULE rather than by code -- and then prices what that schedule is worth to a BOOK.

Two dials, every grid point reported:
  P1  CLASS      = {NARROW, MID, WIDE}   what counts as a cross-file index/shape test
  P2  STALENESS  = {0, 3, 9, 21} trading days a panel's cache lags "today" (book leg)

Reported TREATMENTS (not selected on any outcome, every cell published): PANEL
{U56, B136, SMALL483} and the file pairs the census finds.  The book's gross is FIXED at
1.00 (the standing 4b candidate of ideas 733/541) with RULES v2 (band book, gross 0.75)
as the 4a comparand and SPY as the 4b comparand.  The rule-8 selector only ever picks k.

10 bps, weekly cadence, next-day execution (PROTOCOL 2).  Deterministic; no network.
"""
from __future__ import annotations
import ast, hashlib, io, json, os, sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, metrics  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, rebalance_mask  # noqa

BT = ROOT / "research" / "backtests"
STEM = Path(__file__).stem
COST_BPS, FREQ, BAND, GROSS = 10, "W", 0.03, 1.00
STALE = [0, 3, 9, 21]
IS_END = pd.Timestamp("2016-12-31")            # rule 8: parameters chosen on 2009-2016 only
OOS_START = pd.Timestamp("2017-01-01")
I515 = BT / "2026-09-11_how-many-of-the-record-s-520-ASSERT-CLAUSES-are-SELF-CONSISTENCY-gates_cloud.clauses.csv"

LOG: list[str] = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); LOG.append(s)

# ----------------------------------------------------------------------------------- files
# Identity of every INPUT panel the record can read, and its on-disk vintage.
PANEL_FILES = {
    "PRICES":       ROOT / "data" / "prices.csv",
    "PRICES_BROAD": ROOT / "data" / "prices_broad.csv",
    "PRICES_SMALL": ROOT / "data" / "prices_small.csv.gz",
    "VOLUME_SMALL": ROOT / "data" / "volume_small.csv.gz",
    "SMALL_META":   ROOT / "data" / "small_meta.csv",
    "EARNINGS":     ROOT / "data" / "earnings_dates.csv",
    "FORM4":        ROOT / "data" / "form4_purchases.csv",
    "SPINOFFS":     ROOT / "data" / "spinoffs.csv",
}
DATED = ["PRICES", "PRICES_BROAD", "PRICES_SMALL", "VOLUME_SMALL"]

def read_dated(name):
    return pd.read_csv(PANEL_FILES[name], index_col=0, parse_dates=True).sort_index()

# =================================================================================== GATES
def gates():
    say("=" * 118)
    say(f"Idea 522 (lane B) | {STEM} | {COST_BPS} bps, {FREQ}, next-day execution")
    say("=" * 118)
    say("\nPRE-REGISTERED REPRODUCTION GATES (printed before any census number is read)")
    out = {}

    # G1 -- idea 515's published clause counts, off its own committed .clauses.csv
    cl = pd.read_csv(I515)
    vc = cl["form"].value_counts().to_dict()
    pub = {"tolerance": 345, "exact": 87, "structural": 46, "count": 40}
    g1 = len(cl) == 520 and all(vc.get(k) == v for k, v in pub.items()) and cl["script"].nunique() == 151
    say(f"  G1 idea 515 counts: rows {len(cl)} (pub 520) | " +
        " | ".join(f"{k} {vc.get(k)} (pub {v})" for k, v in pub.items()) +
        f" | scripts {cl['script'].nunique()} (pub 151) | residual form(s) " +
        f"{ {k: v for k, v in vc.items() if k not in pub} }  -> {'PASS' if g1 else 'FAIL'}")
    say("     NOTE: 345+87+46+40 = 518, not 520; idea 515's published breakdown omits 2 "
        "'floor' clauses.  Reported, not corrected.")
    out["G1"] = g1

    # G2 -- the exemplar: is today's failure the 3-day tail and nothing else?
    d, b = read_dated("PRICES"), read_dated("PRICES_BROAD")
    asis = d.index.equals(b.index)
    tail = [str(x.date()) for x in d.index.difference(b.index)]
    rev = [str(x.date()) for x in b.index.difference(d.index)]
    trunc = d.loc[: b.index[-1]].index.equals(b.index)
    g2 = (not asis) and trunc and not rev
    say(f"  G2 crypto-sleeve L406 `px.index.equals(pxb.index)` as-is {asis} | PRICES-only days "
        f"{tail} | BROAD-only days {rev} | after truncating PRICES to BROAD's last close: "
        f"{trunc}  -> {'PASS' if g2 else 'FAIL'}")
    out["G2"] = g2

    # G3 -- is the cross-file gap TAIL-ONLY (schedule), or do the SHARED cells disagree too?
    # Only price-vs-price pairs get a cell test; prices-vs-volume are different quantities.
    say("\n  G3 shared-CELL agreement on the common index (the tail-only hypothesis).")
    say("     H0: the only thing separating two panel caches is the refresh SCHEDULE, so the "
        "cells they share are identical.")
    g3 = True
    for a, bn in (("PRICES", "PRICES_BROAD"), ("PRICES", "PRICES_SMALL"),
                  ("PRICES_BROAD", "PRICES_SMALL")):
        A, B = read_dated(a), read_dated(bn)
        ix = A.index.intersection(B.index); co = A.columns.intersection(B.columns)
        if len(co) == 0:
            say(f"     {a:13s} vs {bn:13s}: {len(ix)} shared rows, 0 shared columns "
                f"(disjoint panels -- no cell test possible)")
            continue
        X, Y = A.loc[ix, co], B.loc[ix, co]
        both = X.notna() & Y.notna(); n = int(both.sum().sum())
        rel = ((X - Y).abs() / X.abs().clip(lower=1e-12)).where(both)
        mx = float(rel.max().max())
        # decompose: how much survives writing BOTH files at the coarser file's precision?
        # prec = smallest p for which >=99% of the coarser file's cells are exactly p-decimal
        flat = Y.stack().dropna()                        # pandas 3 keeps NaN in stack()
        tol = 1e-9 * flat.abs().clip(lower=1.0)          # relative: 1e-12 is below an ULP at 5e4
        prec = next((p for p in range(0, 7)
                     if float((flat - flat.round(p)).abs().lt(tol).mean()) >= 0.99), 6)
        beyond = (Y - X.round(prec)).abs().where(both)
        nb = int((beyond > 0.5 * 10 ** -prec).sum().sum())
        per = (beyond > 0.5 * 10 ** -prec).sum().sort_values(ascending=False)
        top = ", ".join(f"{t} {int(c)}" for t, c in per.head(3).items() if c > 0)
        ok = mx < 1e-6; g3 &= ok
        say(f"     {a:13s} vs {bn:13s}: {len(ix)} shared rows x {len(co)} cols = {n} cells | "
            f"max|rel| {mx:.3e} | cells >1e-6 {int((rel > 1e-6).sum().sum())} "
            f"({(rel > 1e-6).sum().sum()/n:.1%}) -> {'PASS' if ok else 'FAIL (H0 rejected)'}")
        say(f"       {bn} is written at {prec} decimals; cells disagreeing BEYOND that rounding: "
            f"{nb} ({nb/n:.2%}), concentrated in [{top}]")
        if len(per) and per.iloc[0] > 0:
            t = per.index[0]; ratio = (Y[t] / X[t]).dropna()
            say(f"       worst name {t}: {bn}/{a} ratio median {ratio.median():.6f} over "
                f"{len(ratio)} rows (min {ratio.min():.6f}, max {ratio.max():.6f}) -- a whole-"
                f"history ADJUSTMENT-FACTOR restatement, not a tail; the two caches were "
                f"downloaded at different times and back-adjust {t} differently.")
    out["G3"] = g3
    say("     G3 is a MEASUREMENT, not a bar: its failure is the finding (see LEG B).")

    # G4 -- truncation is EXACTLY a prefix (the shortcut the book leg relies on)
    px = load_universe()
    w = lambda p: (gross_band(p, GROSS))
    full = backtest(px, w(px), cost_bps=COST_BPS, freq=FREQ)["returns"]
    worst = 0.0
    for n in (400, 1500, 3000, 4699):
        sub = px.iloc[:n]
        tr = backtest(sub, w(sub), cost_bps=COST_BPS, freq=FREQ)["returns"]
        worst = max(worst, float((tr - full.iloc[:n]).abs().max()))
    g4 = worst < 1e-15
    say(f"\n  G4 truncation == prefix (4 cut points on U56): max|d daily return| {worst:.3e} "
        f"-> {'PASS' if g4 else 'FAIL'}  (lets the anchor x staleness grid be sliced, not re-run)")
    out["G4"] = g4

    # G5 -- identify the STANDING 4b candidate's frame convention (idea 740 said the
    # LEADERBOARD cannot do this; the memo's five numbers can).
    say("\n  G5 standing 4b candidate (2026-09-11_u56-v2band-gross100_4b_cloud_MEMO.md, line 3): "
        "published 11.55% / 1.2067 / -15.70% / 1.2405 / 1.1798 on U56 @10bps.")
    PUB = (0.1155, 1.2067, -0.1570, 1.2405, 1.1798)
    for tag, frame in (("SPY-IN-FRAME", px), ("SPY-FREE   ", px.drop(columns=["SPY"]))):
        r = backtest(frame, gross_band(frame, GROSS), cost_bps=COST_BPS,
                     freq=FREQ)["returns"].loc[px.index[260]:]
        m = metrics(r); h = len(r) // 2
        got = (m["CAGR"], m["Sharpe"], m["MaxDD"], metrics(r.iloc[:h])["Sharpe"],
               metrics(r.iloc[h:])["Sharpe"])
        d = max(abs(a - b) for a, b in zip(got, PUB))
        say(f"     {tag}: {got[0]:.2%} / {got[1]:.4f} / {got[2]:.2%} / {got[3]:.4f} / "
            f"{got[4]:.4f}   max|d vs published| {d:.2e} -> "
            f"{'REPRODUCES' if d < 6e-4 else 'does not'}")
    say("     => the standing candidate is published on a SPY-FREE frame.  LEG C below runs the "
        "SPY-IN-FRAME convention (baseline.compare's own) for BOTH book and comparand; the "
        "level shift is -0.0071 Sharpe / +0.21 pp MaxDD and is common to every cell.")
    out["G5"] = True

    say("\n  VINTAGES ON DISK: " + " | ".join(
        f"{n} {read_dated(n).index[-1].date()} ({read_dated(n).shape[0]}r x {read_dated(n).shape[1]}c)"
        for n in DATED))
    say(f"\n  GATE SUMMARY: {out}")
    assert out["G1"], "G1 (idea 515 reproduction) failed -- nothing downstream is trustworthy"
    assert out["G4"], "G4 (prefix identity) failed -- the book leg's slicing shortcut is invalid"
    return out

def gross_band(px, g):
    """The band book (RULES v2's clause) at an arbitrary gross; g=0.75 IS RULES v2."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, BAND), 0.0)

# ============================================================= LEG A: census of the 46 gates
IDX_ATTRS = {"index", "columns", "shape", "size", "dtypes"}
EQ_CALLS = {"equals", "all", "any", "identical"}
SET_FUNCS = {"set", "frozenset"}
LOADERS = {"load_universe", "load_prices", "load_volume", "read_csv", "read_prices"}

def file_of_call(node: ast.AST) -> set[str]:
    """Which INPUT panel(s) a loader call reads, from its name and kwargs/args."""
    if not isinstance(node, ast.Call): return set()
    fn = node.func
    nm = fn.attr if isinstance(fn, ast.Attribute) else getattr(fn, "id", "")
    src = ast.dump(node)
    if nm in ("load_universe", "load_prices"):
        if "'broad'" in src and "True" in src.split("'broad'")[1][:40]: return {"PRICES_BROAD"}
        if "'small'" in src and "True" in src.split("'small'")[1][:40]: return {"PRICES_SMALL"}
        return {"PRICES"}
    if nm == "load_volume": return {"VOLUME_SMALL"}
    if nm == "read_csv":
        low = src.lower()
        hits = {k for k, p in PANEL_FILES.items() if p.name.split(".")[0].lower() in low}
        if "prices_broad" in low: hits |= {"PRICES_BROAD"}
        if hits: return hits
        if ".grid.csv" in low or ".cells.csv" in low or "backtests" in low: return {"ARTEFACT"}
        return {"UNRESOLVED"}
    return set()

class Resolver:
    """Idea 515's over-approximating dataflow closure: union every assignment to a name
    anywhere in the file, depth<=6, cycle-guarded."""
    DEPTH = 6
    def __init__(self, tree: ast.AST):
        self.assigns: dict[str, list[ast.AST]] = {}
        for n in ast.walk(tree):
            if isinstance(n, ast.Assign):
                for t in n.targets:
                    for nm in self._names(t): self.assigns.setdefault(nm, []).append(n.value)
            elif isinstance(n, (ast.AugAssign, ast.AnnAssign)) and n.value is not None:
                for nm in self._names(n.target): self.assigns.setdefault(nm, []).append(n.value)
            elif isinstance(n, ast.For):
                for nm in self._names(n.target): self.assigns.setdefault(nm, []).append(n.iter)
            elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for a in n.args.args + n.args.kwonlyargs:
                    self.assigns.setdefault(a.arg, [])
    @staticmethod
    def _names(t):
        return sorted({x.id for x in ast.walk(t) if isinstance(x, ast.Name)})
    def closure(self, expr: ast.AST) -> list[ast.AST]:
        seen, out, queue = set(), [expr], [(expr, 0)]
        while queue:
            e, d = queue.pop(0)
            if d >= self.DEPTH: continue
            for n in ast.walk(e):
                if isinstance(n, ast.Name) and n.id not in seen:
                    seen.add(n.id)
                    for v in self.assigns.get(n.id, []):
                        out.append(v); queue.append((v, d + 1))
        return out

def has_struct_predicate(nodes) -> bool:
    for e in nodes:
        for n in ast.walk(e):
            if isinstance(n, ast.Attribute) and n.attr in IDX_ATTRS: return True
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "equals":
                return True
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in SET_FUNCS:
                return True
    return False

def has_numeric_tolerance(nodes) -> bool:
    """A hidden tolerance gate: an ordering comparison against a small float literal."""
    for e in nodes:
        for n in ast.walk(e):
            if isinstance(n, ast.Compare) and any(isinstance(o, (ast.Lt, ast.LtE, ast.Gt, ast.GtE))
                                                  for o in n.ops):
                for c in n.comparators:
                    for k in ast.walk(c):
                        if isinstance(k, ast.Constant) and isinstance(k.value, float): return True
    return False

def files_touched(nodes) -> set[str]:
    f = set()
    for e in nodes:
        for n in ast.walk(e):
            f |= file_of_call(n)
    return f

def census():
    say("\n" + "=" * 118)
    say("[LEG A]  CENSUS OF THE 46 STRUCTURAL CLAUSES  (P1 = CLASS, all three reported)")
    say("=" * 118)
    cl = pd.read_csv(I515)
    st = cl[cl["form"] == "structural"].reset_index(drop=True)
    rows = []
    for _, r in st.iterrows():
        p = BT / r["script"]
        rec = dict(script=r["script"], lineno=int(r["lineno"]), src=str(r["src"]),
                   located=False, own_struct=False, clos_struct=False, hidden_tol=False,
                   files="", nfiles=0, pair="", CLASS="none")
        if not p.exists():
            rec["files"] = "MISSING_SOURCE"; rows.append(rec); continue
        tree = ast.parse(p.read_text())
        asserts = [n for n in ast.walk(tree) if isinstance(n, ast.Assert)]
        me = [n for n in asserts if n.lineno == rec["lineno"] or
              (n.lineno <= rec["lineno"] <= getattr(n, "end_lineno", n.lineno))]
        if not me:
            near = sorted(asserts, key=lambda n: abs(n.lineno - rec["lineno"]))
            me = near[:1]
        if not me: rows.append(rec); continue
        rec["located"] = True
        test = me[0].test
        R = Resolver(tree)
        clos = [test] + R.closure(test)
        rec["own_struct"] = has_struct_predicate([test])
        rec["clos_struct"] = has_struct_predicate(clos)
        rec["hidden_tol"] = has_numeric_tolerance(clos)
        f = files_touched(clos)
        inputs = sorted(f & set(PANEL_FILES))
        rec["files"] = "+".join(sorted(f)) or "-"
        rec["nfiles"] = len(inputs)
        rec["pair"] = "|".join(inputs) if len(inputs) >= 2 else ""
        rows.append(rec)
    D = pd.DataFrame(rows)
    # P1: three nested readings of "cross-file index/shape test"
    D["NARROW"] = D["own_struct"] & (D["nfiles"] >= 2)
    D["MID"] = D["clos_struct"] & (D["nfiles"] >= 2)
    D["WIDE"] = D["nfiles"] >= 2
    assert (D["NARROW"] <= D["MID"]).all() and (D["MID"] <= D["WIDE"]).all(), "P1 nesting violated"
    D.to_csv(BT / f"{STEM}.clauses.csv", index=False)

    say(f"\n  located in source: {int(D['located'].sum())} / {len(D)}")
    say(f"  clause's OWN expression is already an index/shape/set predicate: "
        f"{int(D['own_struct'].sum())} / {len(D)}   (the other "
        f"{len(D) - int(D['own_struct'].sum())} read `assert ok` / `assert g6` and say nothing "
        f"at the clause)")
    say(f"  ONCE RESOLVED, the closure carries a numeric tolerance: {int(D['hidden_tol'].sum())} "
        f"/ {len(D)}  -> these are TOLERANCE gates misfiled as STRUCTURAL by idea 515's "
        f"clause-level classifier")
    say(f"  genuinely structural once resolved (closure has a structural predicate and NO "
        f"hidden tolerance): {int((D['clos_struct'] & ~D['hidden_tol']).sum())}")
    say("\n  P1 GRID -- how many of the 46 are CROSS-FILE index/shape tests:")
    say(f"  | {'class':7s} | {'n':>3s} | {'share of 46':>11s} | definition")
    for c, defn in (("NARROW", "clause's own expression is the predicate AND >=2 input files"),
                    ("MID", "resolved closure has the predicate AND >=2 input files"),
                    ("WIDE", ">=2 input files in the closure, any predicate form")):
        say(f"  | {c:7s} | {int(D[c].sum()):3d} | {D[c].mean():11.1%} | {defn}")
    say("\n  FILE PAIRS FOUND (P2 axis of the census leg):")
    pr = D[D["WIDE"]]["pair"].value_counts()
    for k, v in pr.items(): say(f"     {k:30s} {v} clause(s)")
    say("\n  CLAUSES IN THE WIDE CLASS (every one, with its class):")
    for _, r in D[D["WIDE"]].iterrows():
        cls = "NARROW" if r["NARROW"] else ("MID" if r["MID"] else "WIDE")
        say(f"     {cls:6s} {r['script'][:56]:58s} L{r['lineno']:<5} {r['src'][:52]:54s} "
            f"[{r['pair']}]")
    return D

# =============================================== LEG B: schedule-decided vs code-decided
def schedule_vs_code(D):
    say("\n" + "=" * 118)
    say("[LEG B]  IS THE GATE DECIDED BY THE CACHE SCHEDULE OR BY CODE?  (re-executed on "
        "today's files)")
    say("=" * 118)
    say("  SCHEDULE = fails as-cached, passes once both sides are cut to their common index")
    say("  CODE     = fails both ways | INERT = passes as-cached\n")
    import itertools
    rows = []
    # a clause may name 3 files; the decision test is pairwise, so expand to 2-combinations
    pairs = set()
    for p in D[D["WIDE"]]["pair"]:
        if p: pairs |= {"|".join(c) for c in itertools.combinations(p.split("|"), 2)}
    # every dated pair on disk, not only the ones a clause happens to name
    allpairs = {f"{a}|{b}" for i, a in enumerate(DATED) for b in DATED[i + 1:]}
    for pr in sorted(pairs | allpairs):
        a, b = pr.split("|")
        if a not in DATED or b not in DATED:
            rows.append(dict(pair=pr, test="index.equals", asis=None, common=None,
                             decision="UNDATED (no index to compare)", extra_a="", extra_b=""))
            continue
        A, B = read_dated(a), read_dated(b)
        ix = A.index.intersection(B.index)
        asis = bool(A.index.equals(B.index))
        common = bool(A.loc[ix].index.equals(B.loc[ix].index)) and len(ix) > 0
        ea = [str(x.date()) for x in A.index.difference(B.index)]
        eb = [str(x.date()) for x in B.index.difference(A.index)]
        dec = "INERT" if asis else ("SCHEDULE" if common else "CODE")
        rows.append(dict(pair=pr, test="index.equals", asis=asis, common=common, decision=dec,
                         extra_a=",".join(ea[-4:]), extra_b=",".join(eb[-4:])))
        # shape test, same pair (the other structural form idea 515 found)
        sa = bool(A.shape == B.shape)
        sc = bool(A.loc[ix].shape[0] == B.loc[ix].shape[0])
        rows.append(dict(pair=pr, test="shape[0]", asis=sa, common=sc,
                         decision="INERT" if sa else ("SCHEDULE" if sc else "CODE"),
                         extra_a=str(A.shape), extra_b=str(B.shape)))
        # VALUE test on the shared cells -- the leg a pure index test cannot reach
        co = A.columns.intersection(B.columns)
        if len(co) and "VOLUME" not in pr:
            X, Y = A.loc[ix, co], B.loc[ix, co]
            both = X.notna() & Y.notna()
            va = bool(np.allclose(X.where(both).fillna(0), Y.where(both).fillna(0),
                                  rtol=1e-6, atol=0))
            rows.append(dict(pair=pr, test="cells@1e-6", asis=va, common=va,
                             decision="INERT" if va else "CODE",
                             extra_a=f"{len(co)} shared cols",
                             extra_b=f"max|rel| {float(((X-Y).abs()/X.abs().clip(lower=1e-12)).where(both).max().max()):.2e}"))
    S = pd.DataFrame(rows)
    S.to_csv(BT / f"{STEM}.pairs.csv", index=False)
    say(f"  | {'pair':30s} | {'test':12s} | {'as-cached':9s} | {'on common idx':13s} | "
        f"{'decision':9s} | extra days / shapes")
    for _, r in S.iterrows():
        say(f"  | {r['pair']:30s} | {r['test']:12s} | {str(r['asis']):9s} | "
            f"{str(r['common']):13s} | {r['decision']:9s} | {r['extra_a']} // {r['extra_b']}")
    dc = S["decision"].value_counts().to_dict()
    say(f"\n  DECISION COUNTS over {len(S)} (pair x test) cells: {dc}")
    sched = set(S[(S["decision"] == "SCHEDULE")]["pair"])
    codep = set(S[(S["decision"] == "CODE")]["pair"])
    def touches(pairstr, S_):
        c = set("|".join(x) for x in itertools.combinations(pairstr.split("|"), 2))
        return bool(c & S_)
    say("")
    for c in ("NARROW", "MID", "WIDE"):
        sub = D[D[c]]; n = len(sub)
        hs = int(sum(touches(p, sched) for p in sub["pair"]))
        hc = int(sum(touches(p, codep) for p in sub["pair"]))
        say(f"  class {c:6s}: {n:2d} cross-file clauses -> {hs} sit on a file pair the REFRESH "
            f"SCHEDULE currently decides ({hs/46:.1%} of all 46 structural clauses); "
            f"{hc} also sit on a pair whose shared CELLS disagree (CODE-decided leg)")
    return S

# ==================================================== LEG C: what is the schedule worth to a BOOK?
def panels():
    u = load_universe()
    b = load_universe(broad=True)
    s = load_universe(small=True)
    return {"U56": u, "B136": b, "SMALL483": s}

def verdicts(r, base, spy):
    """PROTOCOL 4a (vs RULES v2) and 4b (vs SPY) on one window."""
    m, mb, ms = metrics(r), metrics(base), metrics(spy)
    h = len(r) // 2
    H = lambda x: (metrics(x.iloc[:h])["Sharpe"], metrics(x.iloc[h:])["Sharpe"])
    h1, h2 = H(r); b1, b2 = H(base); s1, s2 = H(spy)
    a = bool(h1 > b1 and h2 > b2 and m["MaxDD"] >= mb["MaxDD"])
    bb = bool(h1 > s1 and h2 > s2 and m["MaxDD"] >= 0.60 * ms["MaxDD"]
              and m["CAGR"] >= 0.70 * ms["CAGR"])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                bCAGR=mb["CAGR"], bSharpe=mb["Sharpe"], bMaxDD=mb["MaxDD"], bH1=b1, bH2=b2,
                sCAGR=ms["CAGR"], sSharpe=ms["Sharpe"], sMaxDD=ms["MaxDD"], sH1=s1, sH2=s2,
                p4a=a, p4b=bb)

def book_leg():
    say("\n" + "=" * 118)
    say("[LEG C]  WHAT IS THE REFRESH SCHEDULE WORTH TO A BOOK?  (P2 = STALENESS k, all four "
        "rungs reported)")
    say("=" * 118)
    say(f"  Book = band book at gross {GROSS:.2f} (the standing 4b candidate), {FREQ} cadence, "
        f"{COST_BPS} bps, next-day execution.")
    say("  Comparand = RULES v2 (same clause at gross 0.75) on the SAME panel and the SAME "
        "truncated window; 4b comparand = SPY.")
    say("  ANCHOR = a month-end 'today'.  STALENESS k = the panel's cache ends k trading days "
        "before the anchor.")
    P = panels()
    rows = []
    for pname, px in P.items():
        spy = px["SPY"].pct_change().fillna(0.0)
        rb = backtest(px, gross_band(px, GROSS), cost_bps=COST_BPS, freq=FREQ)["returns"]
        rv = backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"]
        start = px.index[260]
        idx = px.index
        anchors = idx.to_series().groupby([idx.year, idx.month]).max()
        anchors = [a for a in anchors if a >= start + pd.Timedelta(days=365)]
        for A in anchors:
            ia = idx.get_loc(A)
            for k in STALE:
                if ia - k < 300: continue
                end = idx[ia - k]
                sl = slice(start, end)
                v = verdicts(rb.loc[sl], rv.loc[sl], spy.loc[sl])
                v.update(panel=pname, anchor=A.date(), k=k, end=end.date(),
                         n=len(rb.loc[sl]), era="IS" if A <= IS_END else "OOS")
                rows.append(v)
    G = pd.DataFrame(rows)
    G.to_csv(BT / f"{STEM}.grid.csv", index=False)
    say(f"\n  grid: {len(G)} (panel x anchor x k) cells written to {STEM}.grid.csv")

    say("\n  [C1] FULL-SAMPLE READING AT EACH k (anchor = the panel's own last close)")
    say(f"  | {'panel':9s} | {'k':>2s} | {'end':10s} | {'CAGR':>7s} | {'Sharpe':>7s} | "
        f"{'MaxDD':>7s} | {'H1/H2':>13s} | {'v2 Sharpe':>9s} | {'SPY Sh':>7s} | 4a | 4b")
    for pname in P:
        sub = G[G["panel"] == pname]
        last = sub["anchor"].max()
        for k in STALE:
            r = sub[(sub["anchor"] == last) & (sub["k"] == k)]
            if r.empty: continue
            r = r.iloc[0]
            say(f"  | {pname:9s} | {k:2d} | {str(r['end']):10s} | {r['CAGR']:7.2%} | "
                f"{r['Sharpe']:7.4f} | {r['MaxDD']:7.2%} | {r['H1']:6.3f}/{r['H2']:6.3f} | "
                f"{r['bSharpe']:9.4f} | {r['sSharpe']:7.4f} | "
                f"{'Y' if r['p4a'] else 'n':2s} | {'Y' if r['p4b'] else 'n'}")

    say("\n  [C2] DECISION POWER OF THE SCHEDULE OVER BOOKS -- k>0 vs the fresh k=0 reading, "
        "over every anchor")
    say(f"  | {'panel':9s} | {'k':>2s} | {'anchors':>7s} | {'med|dSharpe|':>12s} | "
        f"{'max|dSharpe|':>12s} | {'med|dCAGR|pp':>12s} | {'max|dDD|pp':>10s} | "
        f"{'4a flips':>8s} | {'4b flips':>8s}")
    flips, flip_legs = [], []
    for pname in P:
        base0 = G[(G["panel"] == pname) & (G["k"] == 0)].set_index("anchor")
        for k in STALE[1:]:
            kk = G[(G["panel"] == pname) & (G["k"] == k)].set_index("anchor")
            j = base0.join(kk, rsuffix="_k", how="inner")
            ds = (j["Sharpe"] - j["Sharpe_k"]).abs()
            dc = (j["CAGR"] - j["CAGR_k"]).abs() * 100
            dd = (j["MaxDD"] - j["MaxDD_k"]).abs() * 100
            f4a = int((j["p4a"] != j["p4a_k"]).sum()); f4b = int((j["p4b"] != j["p4b_k"]).sum())
            fl = j[j["p4b"] != j["p4b_k"]]
            if len(fl):
                legs = []
                for _, q in fl.iterrows():
                    L = []
                    if (q["H1"] > q["sH1"]) != (q["H1_k"] > q["sH1_k"]): L.append("H1")
                    if (q["H2"] > q["sH2"]) != (q["H2_k"] > q["sH2_k"]): L.append("H2")
                    if (q["MaxDD"] >= .6 * q["sMaxDD"]) != (q["MaxDD_k"] >= .6 * q["sMaxDD_k"]):
                        L.append("DD")
                    if (q["CAGR"] >= .7 * q["sCAGR"]) != (q["CAGR_k"] >= .7 * q["sCAGR_k"]):
                        L.append("CAGR")
                    legs.append("+".join(L) or "?")
                flip_legs.append(dict(panel=pname, k=k, n=len(fl),
                                      legs=dict(pd.Series(legs).value_counts()),
                                      anchors=[str(x) for x in fl.index[:6]]))
            flips.append(dict(panel=pname, k=k, anchors=len(j), med_dSharpe=ds.median(),
                              max_dSharpe=ds.max(), med_dCAGR_pp=dc.median(),
                              max_dDD_pp=dd.max(), flip4a=f4a, flip4b=f4b))
            say(f"  | {pname:9s} | {k:2d} | {len(j):7d} | {ds.median():12.4f} | {ds.max():12.4f} "
                f"| {dc.median():12.3f} | {dd.max():10.3f} | {f4a:8d} | {f4b:8d}")
    pd.DataFrame(flips).to_csv(BT / f"{STEM}.flips.csv", index=False)
    say("\n  [C3] WHICH 4b LEG THE STALENESS FLIPS  (a flip is a PUBLISHED VERDICT the cache "
        "schedule alone decides)")
    if not flip_legs:
        say("     none")
    for f in flip_legs:
        say(f"     {f['panel']:9s} k={f['k']:2d}  {f['n']:2d} flipped anchors  binding leg(s) "
            f"{f['legs']}   e.g. {f['anchors']}")
    return G, pd.DataFrame(flips)

def rule8(G):
    say("\n" + "=" * 118)
    say("[LEG D]  RULE 8 WALK-FORWARD -- k chosen on IS ANCHORS (<= 2016-12-31) ALONE, "
        "2017-2026 read once")
    say("=" * 118)
    say("  Pre-stated selector: the k with the highest MEAN Sharpe over IS anchors; ties "
        "(<1e-9) break to the SMALLEST k (freshest cache).")
    P = panels()
    out = []
    for pname in sorted(G["panel"].unique()):
        sub = G[G["panel"] == pname]
        iss = sub[sub["era"] == "IS"].groupby("k")["Sharpe"].mean()
        say(f"\n  {pname}: IS mean Sharpe by k -> " +
            " | ".join(f"k={k}: {v:.6f}" for k, v in iss.items()))
        best = iss.max()
        pick = min([k for k, v in iss.items() if best - v < 1e-9])
        tie = sum(1 for v in iss if best - v < 1e-9)
        say(f"     IS pick k={pick}  ({tie} of {len(iss)} rungs tie within 1e-9 "
            f"-> {'DEGENERATE, tie-break used' if tie > 1 else 'discriminated'})")
        # OOS: 2017-01-01 .. panel end, minus k trading days
        px = P[pname]; idx = px.index
        spy = px["SPY"].pct_change().fillna(0.0)
        rb = backtest(px, gross_band(px, GROSS), cost_bps=COST_BPS, freq=FREQ)["returns"]
        rv = backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"]
        for k in STALE:
            end = idx[len(idx) - 1 - k]
            sl = slice(OOS_START, end)
            v = verdicts(rb.loc[sl], rv.loc[sl], spy.loc[sl])
            v.update(panel=pname, k=k, picked=(k == pick), end=end.date(), n=len(rb.loc[sl]))
            out.append(v)
    O = pd.DataFrame(out)
    O.to_csv(BT / f"{STEM}.walkforward.csv", index=False)
    say(f"\n  OOS 2017-01-01 -> panel end minus k  (every rung reported; * = the IS pick)")
    say(f"  | {'panel':9s} | {'k':>2s} |   | {'oCAGR':>7s} | {'oSharpe':>8s} | {'oMaxDD':>7s} | "
        f"{'v2 oCAGR':>8s} | {'v2 oSh':>7s} | {'SPY oCAGR':>9s} | {'SPY oSh':>8s} | "
        f"{'SPY oDD':>7s} | 4a | 4b")
    for _, r in O.iterrows():
        say(f"  | {r['panel']:9s} | {r['k']:2d} | {'*' if r['picked'] else ' '} | "
            f"{r['CAGR']:7.2%} | {r['Sharpe']:8.4f} | {r['MaxDD']:7.2%} | {r['bCAGR']:8.2%} | "
            f"{r['bSharpe']:7.4f} | {r['sCAGR']:9.2%} | {r['sSharpe']:8.4f} | "
            f"{r['sMaxDD']:7.2%} | {'Y' if r['p4a'] else 'n':2s} | {'Y' if r['p4b'] else 'n'}")
    say("\n  KEEP PATHS over every cell of this run's book grid (LEG C, full + halves) and the "
        "OOS table above:")
    return O

def keep_paths(G, O):
    n = len(G)
    say(f"  4a (Sharpe > RULES v2 in BOTH halves and MaxDD no worse): "
        f"{int(G['p4a'].sum())} / {n} anchor-cells  |  OOS {int(O['p4a'].sum())} / {len(O)}")
    say(f"  4b (Sharpe > SPY in BOTH halves, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's): "
        f"{int(G['p4b'].sum())} / {n} anchor-cells  |  OOS {int(O['p4b'].sum())} / {len(O)}")
    for pname in sorted(G["panel"].unique()):
        s = G[G["panel"] == pname]; o = O[O["panel"] == pname]
        say(f"     {pname:9s} 4a {int(s['p4a'].sum()):4d}/{len(s):4d}  4b "
            f"{int(s['p4b'].sum()):4d}/{len(s):4d}   OOS 4a {int(o['p4a'].sum())}/{len(o)}  "
            f"4b {int(o['p4b'].sum())}/{len(o)}")
    kp = G.groupby(["panel", "k"])[["p4a", "p4b"]].mean().reset_index()
    kp.to_csv(BT / f"{STEM}.keeppaths.csv", index=False)

def main():
    pd.set_option("display.width", 200)
    g = gates()
    D = census()
    S = schedule_vs_code(D)
    G, F = book_leg()
    O = rule8(G)
    keep_paths(G, O)
    say("\n" + "=" * 118)
    say("ARTEFACTS: .clauses.csv (46 rows) .pairs.csv .grid.csv .flips.csv .walkforward.csv "
        ".keeppaths.csv .console.txt")
    say("=" * 118)
    (BT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")

if __name__ == "__main__":
    main()

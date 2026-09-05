#!/usr/bin/env python3
"""IDEA 208  audit-every-committed-null-for-a-salted-seed   (lane C, 2026-09-05)

THE QUESTION
------------
Idea 201's by-product: idea 191's rotation null is seeded with

    np.random.default_rng(SEED + hash((pan.name, fam, thr)) % 10_000)

and CPython salts `hash` on `str` with a per-process random seed (PYTHONHASHSEED unset).
So idea 191's REAL rows reproduce to 2.2e-16 while its published BANDS cannot be reproduced
in ANY other process -- a live PROTOCOL-5 (deterministic scripts) violation with nothing in
the output saying so.

The queue asks three things, and this run answers exactly those:

  Q1  CENSUS.   AST-audit EVERY committed .py in the repo for a random seed derived from
                hash() of a str/tuple.  How many scripts?  Which sites?  (And, as a
                by-product on the same machinery: how many committed scripts draw randomness
                with NO seed at all -- the same reproducibility hole by a different door.)
  Q2  EXPOSURE. How many PUBLISHED null bands are affected -- i.e. how many committed band
                numbers, and how many committed clause verdicts resting on them, were drawn
                from a seed that no reader can reproduce?
  Q3  BOUND.    Re-draw one of them and bound how far a verdict can move.

Q3 is answered EXACTLY rather than by resampling.  Idea 191's null draws 20 offsets uniformly
without replacement from the J-1 = 974 available circular rotations
(`rng.permutation(np.arange(1, J))[:20]`), and its clause is

    clears  <=>  |dSharpe_real| > band,   band = max |dSharpe| over the 20 drawn rotations.

So if the WHOLE population of 974 rotations is enumerated, the law of the 20-draw band is
hypergeometric and closed-form: with the null |dSharpe| sorted x_(1) <= ... <= x_(N),

    P(band <= x_(k)) = C(k, 20) / C(N, 20)        and      P(clears) = C(K, 20) / C(N, 20)

with K = #{offsets : |dSharpe_off| < |dSharpe_real|}.  This run enumerates ALL 974 rotations
for all 30 U56 configurations of idea 191's grid at both cost rungs -- 29,250 genuine
backtests -- so every probability below is the exact draw law of the published clause, not an
estimate of it.  No seed sensitivity is inferred; it is computed.

DESIGN
------
Idea 191's script is IMPORTED, not re-implemented (as idea 201 did): its panel builder,
base book, overlay families, apply_overlay, fast_backtest, keep_4a/keep_4b all execute the
parent's own code, so every number sits on the simulator being audited.

  panel    : U56 only.  The U56 rows are 60 of idea 191's 180 published clause cells; the
             exact enumeration costs 975 backtests per configuration and only the 56-name
             panel is affordable at that density.  BROAD136/SMALL439 are NOT re-drawn and no
             claim is made about them beyond the Q1/Q2 census, which covers all three.
  base book: idea 2's candidate -- composite (no vol scaler), 200d & vol20 < 0.60 eligibility,
             top-20 equal weight, gross 0.75, WEEKLY, t+1
  families : DDCTL / BUDGET / SLEEVE, idea 186/191's definitions verbatim
  TUNED PARAMETER 1: threshold (5 per family, idea 191's widened grid, unchanged)
  TUNED PARAMETER 2: depth     (2 per family, idea 186's, unchanged)
  costs    : 10 and 25 bps, both derived EXACTLY from one 0 bps run -- a reported axis, not
             a tuned one.  ALL 60 grid points are reported.
  null     : the COMPLETE population, all 974 circular rotations, per configuration.

  grid: 30 configs x (1 real + 974 rotations) x 2 cost rungs = 58,500 rows / 29,250 backtests

RULE 8 (PROTOCOL clause 8, required): the clause is a DECISION rule, so it is priced as one.
Overlay point chosen on data <= 2016-12-31 ONLY -- within each family, the point with the
largest IS margin (|dSharpe_IS| - IS band) among those clearing their IS band, else
do-nothing -- then 2017-01-01 -> read ONCE.  6 cells (3 families x 2 cost rungs), each run
under 200 INDEPENDENT 20-rotation draws taken from the enumerated population, so the spread
of OOS Sharpe across seeds IS the dollar cost of the salted seed.  Reported against the
do-nothing control, RULES v1 and SPY.  BOTH KEEP PATHS evaluated on every real row.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
---------------------------------------------------------------------
  P0  DISCLOSED: a plain `grep -n "hash("` over research/*.py was run before these
      predictions were written, so the file COUNT in P1 is informed, not blind.  Everything
      in P2-P5 is blind.
  P1  The AST audit flags at least 2 committed scripts whose random seed is derived from
      hash() of a str/tuple, and at least one of them publishes a null band in a committed
      CSV.
  P2  Idea 191's 60 U56 real rows reproduce at < 1e-12, while its published bands do not:
      the max |d band| over the 60 cells exceeds 1e-3 and more than half the cells differ.
  P3  The published verdict is NOT robust to its own draw: at least 10% of the 60 U56 clause
      cells are UNDETERMINED under the exact law (0 < P(clears) < 1).
  P4  The 5-95% draw range of the band is at least 25% of the band's own median value.
  P5  No seed regime's rule-8 selector beats the do-nothing control out of sample -- the
      twelfth consecutive instance in this project of an IS-fitted selector failing to earn
      its complexity.

CAVEATS carried, not buried
---------------------------
  * SURVIVORSHIP (idea 54): U56 is CURRENT constituents.  Real and rotated draws inherit the
    bias identically, so the CLAUSE reading is unaffected; every LEVEL (CAGR, Sharpe, 4a/4b
    counts) is biased upward and is not a tradable estimate.
  * Neighbouring rotation offsets are correlated, so the clause's nominal one-sided size
    (1/21 = 4.8%) is approximate.  That is a property of the clause, not of this run: the
    enumeration is EXACT for the draw law of the published statistic, whatever that
    statistic's own size properties are.
  * The exact law priced here is the law of the SEED, holding the panel, the book and the
    overlay fixed.  It bounds irreproducibility, not the clause's power.
  * BUDGET-skip changes realised turnover between real and null (idea 203's subject).
    Inherited and stated, not fixed here.
  * Idea 38: calendar-day index after 2014-09-17 on U56.  Idea 126: t+1 only.
  * The salting probe (two child processes) is the ONE non-deterministic line of output in
    this script by construction -- it prints hashes that are SUPPOSED to differ.  The
    assertion made on it (they differ; hash of an int does not) is deterministic.

Deterministic (all seeds via zlib.crc32, no reliance on PYTHONHASHSEED), standalone.
Writes .console.txt, .audit.csv, .exact.csv, .walkforward.csv, .keep.csv.
"""
import ast
import importlib.util
import subprocess
import sys
import time
import zlib
from math import comb
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_audit-every-committed-null-for-a-salted-seed_C"
OUT = ROOT / "research" / "backtests"
PARENT_STEM = "2026-09-05_the-on-share-column_cloud"     # idea 191, the audited script

N_DRAW = 20                      # idea 186/191's draw count, inherited unchanged
COST_RUNGS = [10, 25]
N_SEEDS = 200                    # independent 20-draw regimes for the rule-8 spread
IS_END, OOS_START = "2016-12-31", "2017-01-01"

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 4000)

_lines: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


def det_seed(*parts):
    """Deterministic across processes -- the fix this run recommends."""
    return int(zlib.crc32("|".join(str(p) for p in parts).encode())) % (2 ** 31)


# ================================================================== Q1  the AST audit
SEED_CALLS = {"default_rng", "RandomState", "seed", "PCG64", "SeedSequence",
              "MT19937", "Generator"}
RNG_METHODS = {"default_rng", "permutation", "shuffle", "choice", "randint", "integers",
               "standard_normal", "normal", "random_sample", "randn", "rand", "sample",
               "RandomState", "binomial", "multinomial"}
STR_ATTRS = {"name", "stem", "ticker", "label", "key", "family", "fam", "panel", "col"}


def _parents(tree):
    par = {}
    for node in ast.walk(tree):
        for ch in ast.iter_child_nodes(node):
            par[ch] = node
    return par


def _module_literal_types(tree):
    """module-level NAME -> set of python types of the literal elements it holds."""
    out = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        vals = []
        v = node.value
        if isinstance(v, (ast.List, ast.Tuple, ast.Set)):
            vals = list(v.elts)
        elif isinstance(v, ast.Dict):
            vals = list(v.keys)
        elif isinstance(v, ast.Constant):
            vals = [v]
        types = {type(e.value) for e in vals if isinstance(e, ast.Constant)}
        for t in node.targets:
            if isinstance(t, ast.Name) and types:
                out[t.id] = types
    return out


def _resolve_name(name, node, par, modtypes, tree):
    """Best-effort static type of a bare Name reaching hash(): 'STR', 'INT', or ''."""
    # (a) enclosing for-loops that bind it
    cur = node
    while cur in par:
        cur = par[cur]
        tgts = []
        if isinstance(cur, (ast.For, ast.comprehension)):
            tgts = [cur.target]
        elif isinstance(cur, (ast.ListComp, ast.GeneratorExp, ast.SetComp, ast.DictComp)):
            tgts = [g.target for g in cur.generators]
        for tg in tgts:
            names = ([e.id for e in tg.elts if isinstance(e, ast.Name)]
                     if isinstance(tg, ast.Tuple) else
                     ([tg.id] if isinstance(tg, ast.Name) else []))
            if name not in names:
                continue
            it = cur.iter if isinstance(cur, (ast.For, ast.comprehension)) else None
            if it is None:
                continue
            if isinstance(it, ast.Name) and it.id in modtypes:
                ts = modtypes[it.id]
                return "STR" if str in ts else ("INT" if ts <= {int, float} else "")
            if isinstance(it, (ast.List, ast.Tuple)):
                ts = {type(e.value) for e in it.elts if isinstance(e, ast.Constant)}
                return "STR" if str in ts else ("INT" if ts and ts <= {int, float} else "")
            src = ast.unparse(it)
            if ".keys()" in src or ".columns" in src or ".index" in src:
                return "STR"
    # (b) a plain assignment anywhere in the file
    for a in ast.walk(tree):
        if isinstance(a, ast.Assign) and isinstance(a.value, ast.Constant):
            for t in a.targets:
                if isinstance(t, ast.Name) and t.id == name:
                    return "STR" if isinstance(a.value.value, str) else "INT"
    return ""


def classify_hash_arg(call, par, modtypes, tree):
    """Does a str reach this hash() call?  -> ('STR'|'INT'|'UNRESOLVED', why)"""
    why = []
    kinds = set()
    for n in ast.walk(call):
        if isinstance(n, ast.Constant):
            kinds.add("STR" if isinstance(n.value, str) else "INT")
            if isinstance(n.value, str):
                why.append(f"str literal {n.value!r}")
        elif isinstance(n, ast.JoinedStr):
            kinds.add("STR"); why.append("f-string")
        elif isinstance(n, ast.Call) and isinstance(n.func, ast.Name) \
                and n.func.id in ("str", "repr", "format"):
            kinds.add("STR"); why.append(f"{n.func.id}() call")
        elif isinstance(n, ast.Attribute):
            if n.attr in STR_ATTRS:
                kinds.add("STR"); why.append(f".{n.attr}")
            else:
                kinds.add("?"); why.append(f".{n.attr} (unresolved)")
        elif isinstance(n, ast.Name) and n is not call.func:
            r = _resolve_name(n.id, n, par, modtypes, tree)
            if r:
                kinds.add(r); why.append(f"{n.id} -> {r}")
            else:
                kinds.add("?"); why.append(f"{n.id} (unresolved)")
    if "STR" in kinds:
        return "STR", "; ".join(why)
    if "?" in kinds:
        return "UNRESOLVED", "; ".join(why)
    return "INT", "; ".join(why) or "int literals only"


def _local_funcs(tree):
    """name -> positional parameter names, for functions defined in the same module."""
    return {n.name: [a.arg for a in n.args.args]
            for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}


def seed_context(call, par, funcs):
    """Does this hash() value flow into a random seed?  -> (bool, description)

    Four routes, all needed: a direct RNG constructor, a `seed=` keyword, an assignment to a
    name containing 'seed', and -- the route that actually matters in this corpus -- a
    positional argument of a LOCALLY DEFINED helper whose parameter is named 'seed'
    (idea 191 writes `rotations(J, N_NULL, SEED + hash((...)) % 10_000)`).
    """
    cur, prev = call, call
    while cur in par:
        prev, cur = cur, par[cur]
        if isinstance(cur, ast.Call):
            f = cur.func
            nm = f.attr if isinstance(f, ast.Attribute) else (f.id if isinstance(f, ast.Name)
                                                              else "")
            if nm in SEED_CALLS:
                return True, f"{nm}(...)"
            for kw in cur.keywords:
                if kw.arg and "seed" in kw.arg.lower():
                    return True, f"keyword {kw.arg}="
            if nm in funcs:
                for i, a in enumerate(cur.args):
                    if a is prev and i < len(funcs[nm]) \
                            and "seed" in funcs[nm][i].lower():
                        return True, f"{nm}(... {funcs[nm][i]}=...)"
        if isinstance(cur, ast.Assign):
            for t in cur.targets:
                if isinstance(t, ast.Name) and "seed" in t.id.lower():
                    return True, f"assigned to {t.id}"
            return False, ""
        if isinstance(cur, (ast.FunctionDef, ast.Module)):
            return False, ""
    return False, ""


def audit_repo():
    files = sorted(p for p in ROOT.rglob("*.py") if ".git" not in p.parts)
    sites, per_file = [], []
    for f in files:
        try:
            src = f.read_text()
            tree = ast.parse(src)
        except (SyntaxError, UnicodeDecodeError) as e:
            per_file.append(dict(file=str(f.relative_to(ROOT)), parsed=False, hash_calls=0,
                                 salted_seeds=0, uses_rng=False, seeded=False, note=repr(e)))
            continue
        par, modtypes, funcs = _parents(tree), _module_literal_types(tree), _local_funcs(tree)
        lines = src.split("\n")
        nsalt = 0
        for n in ast.walk(tree):
            if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                    and n.func.id == "hash"):
                continue
            kind, why = classify_hash_arg(n, par, modtypes, tree)
            is_seed, sctx = seed_context(n, par, funcs)
            salted = is_seed and kind in ("STR", "UNRESOLVED")
            nsalt += int(salted)
            sites.append(dict(file=str(f.relative_to(ROOT)), line=n.lineno,
                              arg=ast.unparse(n)[:90], arg_kind=kind, why=why[:120],
                              in_seed=is_seed, seed_ctx=sctx, salted_seed=salted,
                              source=lines[n.lineno - 1].strip()[:120]))
        # randomness use and seeding, both from the AST -- a text grep for "rng." gives
        # false positives on prose inside docstrings
        uses_rng, seeded = False, False
        for n in ast.walk(tree):
            if isinstance(n, ast.Call):
                fnode = n.func
                nm = fnode.attr if isinstance(fnode, ast.Attribute) else (
                    fnode.id if isinstance(fnode, ast.Name) else "")
                src_f = ast.unparse(fnode)
                if nm in RNG_METHODS and ("random" in src_f or "rng" in src_f.lower()
                                          or nm in ("default_rng", "RandomState")):
                    uses_rng = True
                    if n.args or any(k.arg == "seed" for k in n.keywords):
                        seeded |= nm in ("default_rng", "RandomState")
                if nm == "seed" and "random" in src_f:
                    uses_rng = seeded = True
        per_file.append(dict(file=str(f.relative_to(ROOT)), parsed=True,
                             hash_calls=sum(1 for s in sites
                                            if s["file"] == str(f.relative_to(ROOT))),
                             salted_seeds=nsalt, uses_rng=uses_rng, seeded=seeded, note=""))
    return pd.DataFrame(sites), pd.DataFrame(per_file)


# ================================================================== Q2  published exposure
BAND_TOKENS = ("band", "null", "p_val", "pval", "perm", "boot", "lo5", "hi95",
               "ci_lo", "ci_hi")


def published_exposure(affected_files):
    """For every committed CSV in research/backtests, count DRAW-DERIVED cells (null bands,
    permutation p-values, bootstrap intervals) and the clause verdicts resting on them;
    split by whether the producing script seeds its draws with hash() of a str."""
    rows = []
    for csv in sorted(OUT.glob("*.csv")):
        stem = csv.name.split(".")[0]
        if stem == STEM:                 # this run's own outputs are not part of the corpus
            continue
        try:
            df = pd.read_csv(csv, nrows=200000)
        except Exception:
            continue
        bandcols = [c for c in df.columns
                    if any(t in c.lower() for t in BAND_TOKENS)]
        if not bandcols:
            continue
        verdict_cols = [c for c in df.columns if "clear" in c.lower()]
        rows.append(dict(csv=csv.name, script=stem + ".py",
                         rows=len(df), band_cols=len(bandcols),
                         band_cells=int(df[bandcols].notna().to_numpy().sum()),
                         verdict_cells=int(df[verdict_cols].notna().to_numpy().sum())
                         if verdict_cols else 0,
                         affected=(stem + ".py") in affected_files))
    return pd.DataFrame(rows)


# ================================================================== Q3  the exact draw law
def exact_p_clears(null_abs, real_abs, n_draw=N_DRAW):
    """P(clears) = P(all n_draw sampled offsets have |d| < |d_real|) = C(K,n)/C(N,n)."""
    N = len(null_abs)
    if not np.isfinite(real_abs):
        return np.nan, 0, N
    K = int((null_abs < real_abs).sum())
    if K < n_draw:
        return 0.0, K, N
    return float(comb(K, n_draw) / comb(N, n_draw)), K, N


def band_quantile(sorted_abs, q, n_draw=N_DRAW):
    """Smallest x_(k) with P(band <= x_(k)) = C(k,n)/C(N,n) >= q.  Exact."""
    N = len(sorted_abs)
    den = comb(N, n_draw)
    lo, hi = n_draw, N
    while lo < hi:
        mid = (lo + hi) // 2
        if comb(mid, n_draw) / den >= q:
            hi = mid
        else:
            lo = mid + 1
    return float(sorted_abs[lo - 1])


# ============================================================================== run
def main():
    t0 = time.time()
    P("=" * 118)
    P("IDEA 208  audit-every-committed-null-for-a-salted-seed   (lane C, 2026-09-05)")
    P("=" * 118)

    # ---------------------------------------------------------------- import idea 191 verbatim
    spec = importlib.util.spec_from_file_location("p191", OUT / f"{PARENT_STEM}.py")
    p191 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(p191)

    # ============================================================ Q1
    P("\n" + "=" * 118)
    P("Q1  CENSUS -- AST audit of every committed .py for a hash()-derived random seed")
    P("=" * 118)
    S, F = audit_repo()
    P(f"  files parsed: {int(F.parsed.sum())} / {len(F)}"
      + ("" if F.parsed.all() else
         f"   UNPARSEABLE: {list(F.loc[~F.parsed, 'file'])}"))
    P(f"  hash() call sites found: {len(S)}")
    if len(S):
        P("\n  every hash() site in the repository:")
        P(S[["file", "line", "arg", "arg_kind", "in_seed", "seed_ctx",
             "salted_seed"]].to_string(index=False))
        P("\n  source line of each site (verify the classification by eye):")
        for _, r in S.iterrows():
            P(f"    {r.file}:{r.line}")
            P(f"        {r.source}")
            P(f"        -> arg is {r.arg_kind} ({r.why}); seed context: "
              f"{r.seed_ctx or 'NONE'}; SALTED SEED: {r.salted_seed}")
    aff = sorted(set(S.loc[S.salted_seed, "file"].map(lambda p: Path(p).name)))
    P(f"\n  SCRIPTS WITH A SALTED (hash-of-str) RANDOM SEED: {len(aff)}")
    for a in aff:
        P(f"    - {a}")

    P("\n  empirical salting probe (two child processes; these two lines are SUPPOSED to "
      "differ):")
    code = ("import sys;print(hash(('U56','DDCTL',0.03))%10000, hash(3), "
            "hash((1,2,3))%10000)")
    outs = [subprocess.run([sys.executable, "-c", code], capture_output=True,
                           text=True).stdout.strip() for _ in range(2)]
    for i, o in enumerate(outs):
        P(f"    process {i}: hash(('U56','DDCTL',0.03))%10000, hash(3), "
          f"hash((1,2,3))%10000 = {o}")
    a0, a1 = outs[0].split(), outs[1].split()
    P(f"    -> str-bearing hash differs across processes: {a0[0] != a1[0]}"
      f"   |  int hash stable: {a0[1] == a1[1]}   |  int-tuple hash stable: "
      f"{a0[2] == a1[2]}")
    salted_confirmed = (a0[0] != a1[0]) and (a0[1] == a1[1]) and (a0[2] == a1[2])
    P(f"    -> CPython salts hash() on str ONLY: {salted_confirmed} "
      "(so hash of an int/int-tuple is a legitimate, reproducible seed; hash of a str is not)")

    rng_files = F[F.uses_rng & F.parsed]
    unseeded = rng_files[~rng_files.seeded]
    P(f"\n  BY-PRODUCT (same machinery, second reproducibility door): {len(rng_files)} "
      f"committed scripts draw randomness; {len(unseeded)} of them contain no explicit seed "
      "call at all:")
    for f in list(unseeded.file)[:20]:
        P(f"    - {f}")

    # ============================================================ Q2
    P("\n" + "=" * 118)
    P("Q2  EXPOSURE -- how many PUBLISHED null bands were drawn from an unreproducible seed")
    P("=" * 118)
    E = published_exposure(set(aff))
    if len(E):
        P(f"  committed CSVs publishing a band/null column: {len(E)} "
          f"from {E.script.nunique()} scripts")
        P(f"  total published band cells: {int(E.band_cells.sum())}  |  clause verdict cells: "
          f"{int(E.verdict_cells.sum())}")
        A = E[E.affected]
        P(f"\n  OF WHICH produced by a script with a salted seed: {len(A)} CSVs, "
          f"{int(A.band_cells.sum())} band cells "
          f"({A.band_cells.sum() / max(E.band_cells.sum(), 1):.1%} of the corpus), "
          f"{int(A.verdict_cells.sum())} verdict cells "
          f"({A.verdict_cells.sum() / max(E.verdict_cells.sum(), 1):.1%})")
        P("\n  affected CSVs:")
        P(A.to_string(index=False) if len(A) else "    (none)")
        P("\n  all band-publishing CSVs:")
        P(E.to_string(index=False))
    S.to_csv(OUT / f"{STEM}.audit.csv", index=False)

    # ============================================================ reproduction, before Q3
    P("\n" + "=" * 118)
    P("REPRODUCTION, asserted before any new number is read")
    P("=" * 118)
    px56 = load_universe()
    ref = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)
    sl = ref[p191.SLEEVE_ASSETS].reindex(px56.index, method="ffill")
    pxu = pd.concat([px56.drop(columns=p191.SLEEVE_ASSETS, errors="ignore"), sl],
                    axis=1).ffill()
    pan = p191.Panel("U56", pxu, set(c for c in px56.columns if c != "SPY"))
    ok = p191.checks(pan)
    ru = backtest(px56, rules_v1_weights(px56), cost_bps=10.0,
                  freq="W")["returns"].loc[px56.index[260]:]
    mu = metrics(ru)
    P(f"  [d] RULES v1 on u56 @10bps: {mu['CAGR']:.5%} / {mu['Sharpe']:.5f} / "
      f"{mu['MaxDD']:.5%}  (published 6.45305% / 0.66418 / -13.82780%) -> "
      f"{'PASS' if abs(mu['Sharpe'] - 0.66418) < 5e-5 else 'FAIL'}")
    ok &= abs(mu["Sharpe"] - 0.66418) < 5e-5
    if not (ok and salted_confirmed):
        P("\nreproduction FAILS -- STOP")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        return

    # ============================================================ Q3  the enumeration
    P("\n" + "=" * 118)
    P("Q3  EXACT RE-DRAW -- the COMPLETE rotation population for all 30 U56 configurations")
    P("    30 configs x (1 real + 974 rotations) x 2 cost rungs = 58,500 rows")
    P("=" * 118)
    start = pan.start
    spy = pan.spy.loc[start:]
    basefull = backtest(pan.px, rules_v1_weights(pan.px), cost_bps=0.0, freq="W")
    b0, bt = basefull["returns"].loc[start:], basefull["turnover"].loc[start:]
    c0 = pan._r0
    ctrl = {}
    for bps in COST_RUNGS:
        cr = p191.net(c0, bps).loc[start:]
        ctrl[bps] = dict(Sharpe=metrics(cr)["Sharpe"], MaxDD=metrics(cr)["MaxDD"],
                         Sharpe_IS=p191._sh(cr.loc[:IS_END]),
                         Sharpe_OOS=p191._sh(cr.loc[OOS_START:]),
                         CAGR=metrics(cr)["CAGR"],
                         CAGR_OOS=metrics(cr.loc[OOS_START:])["CAGR"],
                         MaxDD_OOS=metrics(cr.loc[OOS_START:])["MaxDD"],
                         H1=p191.halves(cr)[0], H2=p191.halves(cr)[1])

    REAL, NULL = {}, {}
    for fam in p191.FAM_ORDER:
        _, thrs, _, depths = p191.FAMILIES[fam]
        for thr in thrs:
            s_real = p191.on_indicator(pan, fam, thr)
            J = len(s_real)
            offs = np.arange(1, J)                       # THE COMPLETE POPULATION
            for depth in depths:
                acc = {bps: {"dS": [], "dD": [], "dIS": []} for bps in COST_RUNGS}
                for kind, s in ([("real", s_real)]
                                + [("null", np.roll(s_real, o)) for o in offs]):
                    W, mask = p191.apply_overlay(pan, fam, depth, s)
                    res = p191.fast_backtest(pan.px, W, 0.0, p191.FREQ, mask=mask)
                    for bps in COST_RUNGS:
                        r = p191.net(res, bps).loc[start:]
                        m = metrics(r)
                        dS = m["Sharpe"] - ctrl[bps]["Sharpe"]
                        dD = m["MaxDD"] - ctrl[bps]["MaxDD"]
                        dIS = p191._sh(r.loc[:IS_END]) - ctrl[bps]["Sharpe_IS"]
                        if kind == "null":
                            acc[bps]["dS"].append(dS)
                            acc[bps]["dD"].append(dD)
                            acc[bps]["dIS"].append(dIS)
                        else:
                            mo = metrics(r.loc[OOS_START:])
                            h1, h2 = p191.halves(r)
                            br = b0 - bt * bps / 1e4
                            REAL[(fam, thr, str(depth), bps)] = dict(
                                dSharpe=dS, dMaxDD=dD, dSharpe_IS=dIS,
                                on_share=float(s_real.mean()),
                                Sharpe=m["Sharpe"], CAGR=m["CAGR"], MaxDD=m["MaxDD"],
                                H1=h1, H2=h2,
                                Sharpe_OOS=p191._sh(r.loc[OOS_START:]),
                                CAGR_OOS=mo["CAGR"], MaxDD_OOS=mo["MaxDD"],
                                fail4a=p191.keep_4a(r, br), fail4b=p191.keep_4b(r, spy))
                for bps in COST_RUNGS:
                    NULL[(fam, thr, str(depth), bps)] = {
                        k: np.asarray(v, float) for k, v in acc[bps].items()}
            P(f"  {fam:7s} thr={thr:<5} done ({time.time() - t0:.0f}s)")

    P(f"\n  enumeration complete: {len(REAL)} real rows, "
      f"{sum(len(v['dS']) for v in NULL.values())} null rows "
      f"({time.time() - t0:.0f}s)")

    # ------------------------------------------- real-row reproduction against idea 191
    PC = pd.read_csv(OUT / f"{PARENT_STEM}.clause.csv")
    PU = PC[PC.panel == "U56"].copy()
    P(f"\n  [e] reproduction vs {PARENT_STEM}.clause.csv, U56 rows ({len(PU)}):")
    dif = {c: [] for c in ["dSharpe", "dSharpe_IS", "dMaxDD", "on_share"]}
    bdif, bnum = [], 0
    for _, r in PU.iterrows():
        k = (r.family, r.thr, str(r.depth), int(r.bps))
        if k not in REAL:
            continue
        bnum += 1
        for c in dif:
            dif[c].append(abs(REAL[k][c] - r[c]))
        bdif.append(abs(float(np.abs(NULL[k]["dS"]).max()) - float(r["band"])))
    P(f"      matched {bnum}/{len(PU)} cells")
    real_ok = True
    for c, v in dif.items():
        d = float(np.nanmax(v))
        P(f"      max|d {c:<11s}| = {d:.3e}  -> {'PASS' if d < 1e-12 else 'FAIL'}")
        real_ok &= d < 1e-12
    P(f"      REAL rows reproduce: {'YES' if real_ok else 'NO'}")
    P("\n      idea 191's PUBLISHED band vs the population MAXIMUM (an upper bound on any "
      "20-draw band):")
    P(f"      max|d band| = {float(np.max(bdif)):.4f}   cells where the published band is "
      f"NOT the population max: {int((np.asarray(bdif) > 1e-12).sum())}/{bnum}")
    P("      (the published band is one 20-draw sample from a population this run now holds "
      "in full;")
    P("       it cannot be reproduced from the committed script, only bracketed -- which is "
      "Q3.)")

    # ------------------------------------------- the exact law, cell by cell
    P("\n" + "-" * 118)
    P("THE EXACT 20-DRAW LAW OF EVERY PUBLISHED U56 CLAUSE CELL")
    P("-" * 118)
    rows = []
    for k, rv in REAL.items():
        fam, thr, depth, bps = k
        nz = NULL[k]
        rec = dict(panel="U56", family=fam, thr=thr, depth=depth, bps=bps,
                   on_share=rv["on_share"])
        for tag, col, rval in (("S", "dS", rv["dSharpe"]),
                               ("DD", "dD", rv["dMaxDD"]),
                               ("IS", "dIS", rv["dSharpe_IS"])):
            a = np.sort(np.abs(nz[col]))
            a = a[np.isfinite(a)]
            p, K, N = exact_p_clears(a, abs(rval))
            rec[f"absd_{tag}"] = abs(rval)
            rec[f"p_clears_{tag}"] = p
            rec[f"K_{tag}"], rec[f"N_{tag}"] = K, N
            rec[f"band_min_{tag}"] = float(a[N_DRAW - 1])
            rec[f"band_q05_{tag}"] = band_quantile(a, 0.05)
            rec[f"band_q50_{tag}"] = band_quantile(a, 0.50)
            rec[f"band_q95_{tag}"] = band_quantile(a, 0.95)
            rec[f"band_max_{tag}"] = float(a[-1])
            rec[f"undet_{tag}"] = 0.0 < p < 1.0
        pub = PU[(PU.family == fam) & (PU.thr == float(thr)) & (PU.depth == depth)
                 & (PU.bps == bps)]
        rec["pub_band"] = float(pub["band"].iloc[0]) if len(pub) else np.nan
        rec["pub_clears"] = bool(pub["clears"].iloc[0]) if len(pub) else None
        rec["pub_clearsDD"] = bool(pub["clearsDD"].iloc[0]) if len(pub) else None
        rec["pass4a"] = rv["fail4a"] == "-"
        rec["pass4b"] = rv["fail4b"] == "-"
        rec["fail4b"] = rv["fail4b"]
        rec.update({c: rv[c] for c in ("Sharpe", "CAGR", "MaxDD", "H1", "H2",
                                       "Sharpe_OOS", "CAGR_OOS", "MaxDD_OOS")})
        rows.append(rec)
    X = pd.DataFrame(rows).sort_values(["family", "thr", "depth", "bps"])
    X.to_csv(OUT / f"{STEM}.exact.csv", index=False)
    X.to_csv(OUT / f"{STEM}.keep.csv", index=False)

    show = ["family", "thr", "depth", "bps", "on_share", "absd_S", "pub_band",
            "band_min_S", "band_q05_S", "band_q50_S", "band_q95_S", "band_max_S",
            "p_clears_S", "pub_clears", "undet_S", "pass4a", "pass4b"]
    P(X[show].to_string(index=False, float_format=lambda v: f"{v:.4f}"))

    for tag, nm in (("S", "Sharpe"), ("DD", "MaxDD"), ("IS", "IS Sharpe")):
        u = int(X[f"undet_{tag}"].sum())
        cert1 = int((X[f"p_clears_{tag}"] == 1).sum())
        cert0 = int((X[f"p_clears_{tag}"] == 0).sum())
        P(f"\n  {nm:<10s} bar: {cert1}/{len(X)} cells clear with probability 1, "
          f"{cert0}/{len(X)} with probability 0, "
          f"**{u}/{len(X)} = {u / len(X):.1%} are UNDETERMINED** (0 < P(clears) < 1)")
        rr = ((X[f"band_q95_{tag}"] - X[f"band_q05_{tag}"])
              / X[f"band_q50_{tag}"].replace(0, np.nan))
        P(f"             band 5-95% draw range / median band = {rr.mean():.1%} mean, "
          f"{rr.median():.1%} median   (full range/median "
          f"{((X[f'band_max_{tag}'] - X[f'band_min_{tag}']) / X[f'band_q50_{tag}'].replace(0, np.nan)).mean():.1%})")
        pv = X[f"p_clears_{tag}"]
        P(f"             E[# cells clearing] = {pv.sum():.2f} of {len(X)}; sd of that count "
          f"= {np.sqrt((pv * (1 - pv)).sum()):.2f}")

    pc = X["p_clears_S"]
    pub = X["pub_clears"].astype(bool)
    eflip = float(np.where(pub, 1 - pc, pc).sum())
    P(f"\n  EXPECTED VERDICT FLIPS vs idea 191's PUBLISHED U56 Sharpe verdicts: "
      f"{eflip:.2f} of {len(X)} = {eflip / len(X):.1%}")
    P(f"  worst single cell: P(flip) = {float(np.where(pub, 1 - pc, pc).max()):.3f}")
    P("  the UNDETERMINED zone in |dSharpe| units (a cell inside it has a seed-dependent "
      "verdict):")
    P(f"     [band_min, band_max] mean width = "
      f"{(X.band_max_S - X.band_min_S).mean():.4f} on a mean |dSharpe| of "
      f"{X.absd_S.mean():.4f} "
      f"({(X.band_max_S - X.band_min_S).mean() / X.absd_S.mean():.1%} of it)")

    # ============================================================ RULE 8
    P("\n" + "=" * 118)
    P("RULE 8 (PROTOCOL clause 8) -- what the salted seed COSTS, out of sample")
    P("    pick on <= 2016-12-31 ONLY: within family, largest IS margin among points clearing")
    P("    their IS band, else do-nothing.  2017-01-01 -> read ONCE.  200 independent 20-draw")
    P("    seed regimes drawn from the enumerated population.")
    P("=" * 118)
    spy_oos = spy.loc[OOS_START:]
    m_spy, m_spy_oos = metrics(spy), metrics(spy_oos)
    wf = []
    for bps in COST_RUNGS:
        br_full = (b0 - bt * bps / 1e4)
        m_b, m_b_oos = metrics(br_full), metrics(br_full.loc[OOS_START:])
        for fam in p191.FAM_ORDER:
            _, thrs, _, depths = p191.FAMILIES[fam]
            for m in range(N_SEEDS):
                best, bestmar = None, -np.inf
                for thr in thrs:
                    rng = np.random.default_rng(det_seed(m, "U56", fam, thr))
                    N = len(NULL[(fam, thr, str(depths[0]), bps)]["dIS"])
                    sel = rng.permutation(np.arange(N))[:N_DRAW]
                    for d in depths:
                        k = (fam, thr, str(d), bps)
                        band = float(np.nanmax(np.abs(NULL[k]["dIS"][sel])))
                        a = abs(REAL[k]["dSharpe_IS"])
                        if np.isfinite(a) and a > band and (a - band) > bestmar:
                            best, bestmar = k, a - band
                if best is None:
                    wf.append(dict(bps=bps, family=fam, seed=m, pick="do-nothing",
                                   margin_IS=np.nan,
                                   Sharpe_OOS=ctrl[bps]["Sharpe_OOS"],
                                   CAGR_OOS=ctrl[bps]["CAGR_OOS"],
                                   MaxDD_OOS=ctrl[bps]["MaxDD_OOS"], pass4b=False))
                else:
                    r = REAL[best]
                    wf.append(dict(bps=bps, family=fam, seed=m,
                                   pick=f"{best[1]}/{best[2]}", margin_IS=bestmar,
                                   Sharpe_OOS=r["Sharpe_OOS"], CAGR_OOS=r["CAGR_OOS"],
                                   MaxDD_OOS=r["MaxDD_OOS"],
                                   pass4b=(r["fail4b"] == "-")))
    WF = pd.DataFrame(wf)
    WF["dOOS"] = WF.apply(lambda r: r.Sharpe_OOS - ctrl[r.bps]["Sharpe_OOS"], axis=1)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    agg = WF.groupby(["bps", "family"]).agg(
        n_distinct_picks=("pick", "nunique"),
        modal_share=("pick", lambda s: s.value_counts(normalize=True).iloc[0]),
        modal_pick=("pick", lambda s: s.value_counts().index[0]),
        donothing_share=("pick", lambda s: float((s == "do-nothing").mean())),
        OOS_Sharpe_mean=("Sharpe_OOS", "mean"), OOS_Sharpe_sd=("Sharpe_OOS", "std"),
        OOS_Sharpe_min=("Sharpe_OOS", "min"), OOS_Sharpe_max=("Sharpe_OOS", "max"),
        OOS_CAGR_mean=("CAGR_OOS", "mean"), OOS_MaxDD_mean=("MaxDD_OOS", "mean"),
        dOOS_mean=("dOOS", "mean"), pass4b_share=("pass4b", "mean")).reset_index()
    P("\n  per cell (3 families x 2 cost rungs), across 200 seed regimes:")
    P(agg.to_string(index=False, float_format=lambda v: f"{v:.4f}"))

    P("\n  HEADLINE (10 bps, OOS 2017-01-01 -> end):")
    P(f"    {'book':<44s} {'CAGR':>8s} {'Sharpe':>8s} {'MaxDD':>9s}")
    for nm, c, s, d in [
        ("seed-dependent clause selector (mean of 200)",
         WF[WF.bps == 10].CAGR_OOS.mean(), WF[WF.bps == 10].Sharpe_OOS.mean(),
         WF[WF.bps == 10].MaxDD_OOS.mean()),
        ("  its BEST seed", WF[WF.bps == 10].CAGR_OOS.max(),
         WF[WF.bps == 10].Sharpe_OOS.max(), WF[WF.bps == 10].MaxDD_OOS.max()),
        ("  its WORST seed", WF[WF.bps == 10].CAGR_OOS.min(),
         WF[WF.bps == 10].Sharpe_OOS.min(), WF[WF.bps == 10].MaxDD_OOS.min()),
        ("do-nothing control (CAND-20, no overlay)", ctrl[10]["CAGR_OOS"],
         ctrl[10]["Sharpe_OOS"], ctrl[10]["MaxDD_OOS"]),
        ("RULES v1 baseline", m_b_oos["CAGR"], m_b_oos["Sharpe"], m_b_oos["MaxDD"]),
        ("SPY buy-and-hold", m_spy_oos["CAGR"], m_spy_oos["Sharpe"], m_spy_oos["MaxDD"]),
    ]:
        P(f"    {nm:<44s} {c:>8.1%} {s:>8.3f} {d:>9.1%}")
    P(f"\n    full-sample reference: RULES v1 {m_b['CAGR']:.1%}/{m_b['Sharpe']:.2f}/"
      f"{m_b['MaxDD']:.1%}   SPY {m_spy['CAGR']:.1%}/{m_spy['Sharpe']:.2f}/"
      f"{m_spy['MaxDD']:.1%}   control {ctrl[10]['CAGR']:.1%}/{ctrl[10]['Sharpe']:.2f}/"
      f"{ctrl[10]['MaxDD']:.1%}")
    best_cell = agg.dOOS_mean.max()
    P(f"\n    best cell's mean dOOS vs do-nothing: {best_cell:+.4f}   "
      f"cells beating do-nothing on average: "
      f"{int((agg.dOOS_mean > 0).sum())}/{len(agg)}")
    P(f"    seed-to-seed OOS Sharpe spread within a cell: mean sd {agg.OOS_Sharpe_sd.mean():.4f}, "
      f"max range {float((agg.OOS_Sharpe_max - agg.OOS_Sharpe_min).max()):.4f}")

    # ------------------------------------------------------------------ both KEEP paths
    P("\n" + "-" * 118)
    P(f"BOTH KEEP PATHS on all {len(X)} real rows (4a vs RULES v1, 4b vs SPY)")
    P("-" * 118)
    P(f"  4a passes: {int(X.pass4a.sum())}/{len(X)}    4b passes: {int(X.pass4b.sum())}/{len(X)}")
    P("  of the 4b passes, how many clear their own null with probability 1 / are "
      "undetermined / never:")
    B = X[X.pass4b]
    if len(B):
        P(f"    P(clears)=1: {int((B.p_clears_S == 1).sum())}   undetermined: "
          f"{int(B.undet_S.sum())}   P(clears)=0: {int((B.p_clears_S == 0).sum())}")
        P(B[["family", "thr", "depth", "bps", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
             "Sharpe_OOS", "absd_S", "band_q50_S", "p_clears_S"]]
          .to_string(index=False, float_format=lambda v: f"{v:.4f}"))
    P("  fail reasons on 4b: " + str(X.fail4b.value_counts().to_dict()))
    P("\n  VERDICT ON THIS RUN'S OWN KEEP QUESTION: this idea proposes no new book, so "
      "neither KEEP path")
    P("  is claimable by it.  The 60 real rows are idea 191's, re-priced; the run's product "
      "is a PROTOCOL")
    P("  clause, and it is reported as such.")

    # ------------------------------------------------------------------ predictions
    P("\n" + "=" * 118)
    P("PRE-REGISTERED PREDICTIONS")
    P("=" * 118)
    u = int(X.undet_S.sum())
    rr = ((X.band_q95_S - X.band_q05_S) / X.band_q50_S.replace(0, np.nan)).median()
    naff = len(aff)
    preds = [
        ("P1 >=2 scripts with a hash(str)-derived seed, >=1 publishing a band",
         naff >= 2 and len(E[E.affected]) >= 1, f"{naff} scripts, "
         f"{len(E[E.affected])} affected CSVs"),
        ("P2 real rows reproduce <1e-12 while published bands do not",
         real_ok and float(np.max(bdif)) > 1e-3,
         f"real max|d| {max(float(np.nanmax(v)) for v in dif.values()):.1e}, "
         f"band max|d| {float(np.max(bdif)):.4f}"),
        ("P3 >=10% of the U56 clause cells are UNDETERMINED",
         u / len(X) >= 0.10, f"{u}/{len(X)} = {u / len(X):.1%}"),
        ("P4 band 5-95% draw range >= 25% of median band", rr >= 0.25, f"{rr:.1%}"),
        ("P5 no seed regime's selector beats do-nothing OOS",
         float(WF.dOOS.max()) <= 0, f"best single-seed dOOS {float(WF.dOOS.max()):+.4f}, "
         f"best cell mean {best_cell:+.4f}"),
    ]
    hit = 0
    for name, got, note in preds:
        hit += int(bool(got))
        P(f"  {'HIT ' if got else 'MISS'}  {name:<62s} {note}")
    P(f"\n  {hit} of {len(preds)} predictions hit.")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
    P(f"\ndone in {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()

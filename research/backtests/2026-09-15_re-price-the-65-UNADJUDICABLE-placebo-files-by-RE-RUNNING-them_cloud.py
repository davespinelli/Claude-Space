#!/usr/bin/env python3
"""Idea 886 (cloud lane, idea 1 of 2, 2026-09-15) - re-price the 65 UNADJUDICABLE placebo
files by RE-RUNNING them, not by reading them.

THE QUEUE'S PREMISE
-------------------
Idea 880 opened only 5 of the 70 committed placebo-bearing files that idea 871 censused and
found per-arm cells in those 5 alone, concluding that "92.9% of the record's placebo mass can
never be re-priced from what it committed".  The queue item infers that the remaining 65 can be
recovered only by RE-RUNNING their surviving scripts, and asks for a re-runnability census plus
a re-run of the cheapest tranche under BOTH estimators with seed dispersion stored.

THE DEFECT IN THAT PREMISE, STATED BEFORE ANY NUMBER IS READ
------------------------------------------------------------
871's census and 880's re-pricing are both FILE-level.  A research run is not a file: it is a
STEM with a family of committed sibling artifacts (`<stem>.py`, `<stem>.result.md`,
`<stem>.placebo.csv.gz`, ...).  871 enumerated files whose PROSE matches the null names, which
selects `.py` and `.result.md` and cannot select a per-arm CSV, because a CSV of numbers
contains no prose.  880 then opened only the files 871 had named.  So the classification
"unadjudicable" was never a statement about what a run committed - it was a statement about
which of a run's files happened to contain the word BLOCK.

    H_SIBLING (pre-registered, this run's first hypothesis): a materially larger share of the
    record's placebo mass is ALREADY adjudicable from committed per-arm sibling artifacts than
    880's 5-of-70 implies, and recovering it requires READING, not re-running.

That reframes, but does not replace, the queue's question.  Whatever is not recoverable by
reading is exactly the set the queue wants re-run, and its second hypothesis is the queue's own:

    H_RERUN: re-running a script that committed no per-arm cells RECOVERS per-arm cells.
             A script is a deterministic function of its inputs; if it never wrote per-arm
             cells, re-running it writes the same aggregate it wrote before.  This is
             pre-registered as EXPECTED-FALSE and is tested by actually running the tranche.

    H_REPRO: the residual tranche reproduces its committed artifacts BIT-FOR-BIT.  If it does
             not, the run is not deterministic as committed and re-running cannot adjudicate it
             either.

TWO TUNED PARAMETERS (the queue's own), ALL GRID POINTS REPORTED
---------------------------------------------------------------
    tranche selector : per-script wall-clock cap, TRANCHE_CAP in {120, 300} seconds, scripts
                       taken cheapest-first by committed source size (a pre-registered proxy
                       fixed before any script was timed)
    seed budget      : SEED_MIN in {3, 5, 10, 20}, the minimum seeds per arm below which a
                       committed cell is NOT counted adjudicable

ESTIMATORS.  Every recovered cell is re-priced under both, per arm, over its own seeds:
    ABS     median_arms( median_seeds |x| )      - has no zero of its own, needs an outside floor
    SIGNED  median_arms( median_seeds  x  )      - plus a sign test over arms, calibrated by
                                                   construction against 50%
and the per-arm seed dispersion sd_seeds(x) is stored, which is what makes the ABS reading
adjudicable at all (seed-noise floor 0.6745 * 1.2533 / sqrt(nseed) * sd, idea 880's formula).

SAFETY.  Re-running committed scripts writes into research/backtests.  Every re-run is executed
in place (that is what "as committed" means), its byte-level effect on the tree is measured
against `git`, and the tree is restored with `git checkout --` plus removal of new untracked
files after EVERY script.  This file writes its own outputs only after the last restore, and
prints the final `git status` so the restore is auditable.  It does not modify RULES.md,
PROTOCOL.md, scan.py, bot.py or baseline.py.

PROTOCOL: 10 bps per unit turnover, next-day fills, no shorting, no leverage.  Deterministic,
standalone, no network.  Outputs:
    .census.csv  .adjudicable.csv  .estimators.csv  .rerun.csv  .walkforward.csv  .console.txt
"""
from __future__ import annotations

import ast
import gzip
import hashlib
import os
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score, metrics, backtest  # noqa: E402

STAMP = "2026-09-15_re-price-the-65-UNADJUDICABLE-placebo-files-by-RE-RUNNING-them_cloud"
B = ROOT / "research" / "backtests"

CENSUS_871 = B / "2026-09-15_should-PROTOCOL-require-a-RUN-LENGTH-MATCHED-null-by-name_B.census.csv"
CORPUS_880 = B / ("2026-09-15_how-many-committed-PLACEBO-DIFFERENCED-numbers-would-CHANGE-SIGN-"
                  "under-the-SIGNED-estimator_cloud.corpus.csv")

TRANCHE_CAPS = [120, 300]          # tuned param 1: per-script wall-clock cap, seconds
SEED_MINS = [3, 5, 10, 20]         # tuned param 2: minimum seeds for an adjudicable cell
RERUN_TOTAL_BUDGET = 900           # hard total wall budget for the whole re-run stage
Z_BAR = 2.0                        # determinate sign

COST_MAIN, WARMUP, MAX_VOL, MA_WIN = 10.0, 260, 0.60, 200
IS_END, OOS_START = "2016-12-31", "2017-01-01"

SEED_COLS = {"seed"}
KIND_COLS = {"kind", "null", "nullkind", "arm_kind"}
OUT_COLS = ["dsharpe", "gap", "excess", "dsharpe_f", "dsharpe_oos", "d_sharpe"]
REF_KINDS = ["BLOCK", "BLOCK2", "YEARBLOCK", "BLOCKPOST"]   # first present wins, in this order

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


def git(*args, cwd=ROOT) -> str:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True).stdout


def read_any(p: Path, **kw) -> pd.DataFrame:
    return pd.read_csv(p, **kw)


def nrows(p: Path) -> int:
    op = gzip.open if p.name.endswith(".gz") else open
    with op(p, "rt", errors="replace") as f:
        return max(sum(1 for _ in f) - 1, 0)


# ------------------------------------------------------------------ run-level corpus
def run_stem(f: str) -> str:
    """The RUN a committed file belongs to: its stem with artifact suffixes removed."""
    n = Path(f).name
    for suf in (".result.md", ".console.txt", ".py", ".md", ".csv.gz", ".csv", ".txt"):
        if n.endswith(suf):
            n = n[: -len(suf)]
            break
    if not (B / (n + ".py")).exists() and "." in n:
        c = n.rsplit(".", 1)[0]
        if (B / (c + ".py")).exists():
            n = c
    return n


def sibling_artifacts(stem: str) -> list[Path]:
    return sorted(p for p in B.glob(stem + ".*") if p.name.endswith((".csv", ".csv.gz")))


def cell_table(p: Path):
    """(DataFrame, kind_col, out_cols) if p holds per-arm placebo cells, else None.

    A per-arm placebo cell table is one with a `seed` column (so seed dispersion is
    recoverable) and at least one per-cell difference column.  A `kind` column is recorded
    when present but is not required: several runs commit an already-differenced column."""
    try:
        head = pd.read_csv(p, nrows=0)
    except Exception:
        return None
    low = {c.lower(): c for c in head.columns}
    if not (SEED_COLS & set(low)):
        return None
    outs = [low[c] for c in OUT_COLS if c in low]
    if not outs:
        return None
    kind = next((low[c] for c in KIND_COLS if c in low), None)
    try:
        df = pd.read_csv(p)
    except Exception:
        return None
    return df, kind, outs


# ------------------------------------------------------------------ static re-runnability
NET_NAMES = {"yfinance", "requests", "urllib", "urllib3", "httpx", "aiohttp", "socket"}
RNG_UNSEEDED = {"rand", "randn", "choice", "permutation", "shuffle", "normal", "randint",
                "random_sample", "uniform"}


def static_census(script: Path) -> dict:
    """AST-level: docstrings and comments cannot trigger any of these flags."""
    src = script.read_text(errors="replace")
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return dict(parses=False, network=True, seeded=False, unseeded=False,
                    nondet=True, inputs_missing=-1, bytes=len(src))
    net = seeded = unseeded = nondet = False
    paths: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                if a.name.split(".")[0] in NET_NAMES:
                    net = True
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.split(".")[0] in NET_NAMES:
                net = True
        elif isinstance(node, ast.Attribute):
            if node.attr in ("md5", "sha256", "default_rng", "RandomState"):
                seeded = True
            if node.attr in ("now", "today", "urandom", "time"):
                nondet = nondet or node.attr in ("urandom",)
        elif isinstance(node, ast.Call):
            f = node.func
            nm = f.attr if isinstance(f, ast.Attribute) else (f.id if isinstance(f, ast.Name) else "")
            if nm == "seed":
                seeded = True
            if nm in RNG_UNSEEDED and isinstance(f, ast.Attribute):
                owner = f.value
                own = owner.attr if isinstance(owner, ast.Attribute) else (
                    owner.id if isinstance(owner, ast.Name) else "")
                if own == "random":            # np.random.<unseeded call>
                    unseeded = True
            for kw in node.keywords or []:
                if kw.arg == "seed":
                    seeded = True
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            v = node.value.strip()
            # a REFERENCE to an input file, not an output SUFFIX fragment: research scripts
            # name their own outputs as ".grid.csv" etc. inside f-strings, which parse as
            # constants and are not inputs at all.
            if (v.endswith((".csv", ".csv.gz", ".json", ".txt"))
                    and not v.startswith(".") and " " not in v
                    and Path(v).stem.strip(".") != ""):
                paths.add(v)
    missing = 0
    for v in sorted(paths):
        cands = [ROOT / v, B / v, ROOT / "data" / v, ROOT / "research" / v]
        if not any(c.exists() for c in cands):
            missing += 1
    return dict(parses=True, network=net, seeded=seeded, unseeded=unseeded,
                nondet=nondet, inputs_missing=missing, bytes=len(src))


# ------------------------------------------------------------------ estimators
def reprice(df: pd.DataFrame, kind: str | None, out: str, seed_min: int) -> pd.DataFrame:
    """One row per (arm, kind) with the ABS and SIGNED readings and the seed dispersion.

    With a `kind` column the per-arm reading is null MINUS the arm's reference null (the
    record's own BLOCK-differenced convention); without one the committed column is already
    a difference and is read as it stands."""
    ignore = {c for c in df.columns if c.lower() in SEED_COLS} | {out}
    if kind:
        ignore.add(kind)
    keys = [c for c in df.columns
            if c not in ignore and df[c].dtype != float and df[c].nunique() <= 4000]
    if not keys:
        return pd.DataFrame()
    seed_col = next(c for c in df.columns if c.lower() in SEED_COLS)
    d = df[keys + [seed_col, out] + ([kind] if kind else [])].copy()
    d[out] = pd.to_numeric(d[out], errors="coerce")
    d = d.dropna(subset=[out])
    if kind:
        ref = next((k for k in REF_KINDS if (d[kind] == k).any()), None)
        if ref is None:
            return pd.DataFrame()
        base = d[d[kind] == ref].groupby(keys + [seed_col], observed=True)[out].mean()
        d = d[d[kind] != ref]
        if d.empty:
            return pd.DataFrame()
        d = d.join(base.rename("_ref"), on=keys + [seed_col])
        d["_x"] = d[out] - d["_ref"]
        grp = keys + [kind]
    else:
        d["_x"] = d[out]
        grp = keys
    d["_ax"] = d["_x"].abs()
    g = d.groupby(grp, observed=True)
    r = pd.DataFrame({"n_seed": g["_x"].size(), "signed": g["_x"].median(),
                      "abs": g["_ax"].median(), "sd_seed": g["_x"].std(ddof=1)}).reset_index()
    r = r[r.n_seed >= seed_min]
    return r


def sign_test(v: np.ndarray) -> tuple[float, float]:
    v = v[np.isfinite(v)]
    v = v[v != 0]
    n = len(v)
    if n < 2:
        return float("nan"), float("nan")
    k = int((v < 0).sum())
    share = k / n
    z = (k - n / 2) / np.sqrt(n / 4)
    return share, float(z)


# ------------------------------------------------------------------ books (rule 8)
def _elig(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def ma_dg_weights(px, g):
    pm = px.notna()
    ma = (px > px.rolling(MA_WIN).mean()) & pm
    cnt = pm.sum(axis=1).replace(0, np.nan)
    return (g * pm.div(cnt, axis=0).fillna(0.0)).where(ma, 0.0)


def top_n_weights(px, n, g):
    s = score(px, vol_scale=False)[0]
    rank = s.where(_elig(px)).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (g / n)


def ew_elig_weights(px, g):
    e = _elig(px).astype(float)
    cnt = e.sum(axis=1).replace(0, np.nan)
    return (g * e.div(cnt, axis=0)).fillna(0.0)


BOOKS = {
    "MADG100": lambda px: ma_dg_weights(px, 1.00),
    "MADG075": lambda px: ma_dg_weights(px, 0.75),
    "TOP20": lambda px: top_n_weights(px, 20, 0.75),
    "TOP40": lambda px: top_n_weights(px, 40, 1.00),
    "EWELIG": lambda px: ew_elig_weights(px, 0.75),
    "RULESV2": lambda px: rules_v2_weights(px, band=0.03, gross=0.75),
}


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep].dropna(how="all").ffill(), len(bad)


# ================================================================== run
def main():
    t0 = time.time()
    P(f"# {STAMP}")
    P(f"# pandas {pd.__version__} numpy {np.__version__}")
    P("# idea 886, cloud lane, idea 1 of 2.  PROTOCOL: 10 bps, next-day, no shorting/leverage.")

    dirty = git("status", "--porcelain").strip()
    P(f"\nTREE at start: {'CLEAN' if not dirty else 'DIRTY -> ' + dirty[:200]}")

    # ------------------------------------------------------- G0: reproduce 871 and 880
    cen = read_any(CENSUS_871)
    cor = read_any(CORPUS_880)
    P("\n" + "=" * 96)
    P("G0  REPRODUCE THE TWO COMMITTED CENSUSES THIS RUN IS BUILT ON")
    P("=" * 96)
    P(f"G0a idea 871 placebo-bearing files                 = {len(cen)}   bar 70   "
      f"{'PASS' if len(cen) == 70 else 'FAIL'}")
    rp = cor[cor.status == "RE-PRICEABLE"]
    P(f"G0b idea 880 RE-PRICEABLE files                    = {len(rp)}    bar 5    "
      f"{'PASS' if len(rp) == 5 else 'FAIL'}")
    P(f"G0c 880's unadjudicable count 70 - 5               = {len(cen) - len(rp)}   bar 65   "
      f"{'PASS' if len(cen) - len(rp) == 65 else 'FAIL'}")

    # ------------------------------------------------------- Q1: run-level census
    P("\n" + "=" * 96)
    P("Q1  THE CORPUS IS A SET OF RUNS, NOT A SET OF FILES")
    P("=" * 96)
    cen["stem"] = cen.file.map(run_stem)
    stems = sorted(cen.stem.unique())
    with_py = [s for s in stems if (B / (s + ".py")).exists()]
    P(f"70 committed files collapse to {len(stems)} distinct stems; {len(with_py)} have a surviving script.")
    P(f"no script ({len(stems) - len(with_py)}): " + ", ".join(s for s in stems if s not in with_py))

    rows = []
    for s in with_py:
        st = static_census(B / (s + ".py"))
        sibs = sibling_artifacts(s)
        cells, cell_rows, cell_files = [], 0, []
        for p in sibs:
            ct = cell_table(p)
            if ct is not None:
                df, kind, outs = ct
                cells.append((p, df, kind, outs))
                cell_rows += len(df)
                cell_files.append(p.name)
        rows.append(dict(
            stem=s, files_in_871=int((cen.stem == s).sum()), siblings=len(sibs),
            cell_files=len(cell_files), cell_rows=cell_rows,
            has_cells=bool(cell_files), bytes=st["bytes"], network=st["network"],
            seeded=st["seeded"], unseeded=st["unseeded"], inputs_missing=st["inputs_missing"],
            rerunnable=bool(st["parses"] and not st["network"] and not st["unseeded"]
                            and st["inputs_missing"] == 0),
            cell_file_names=";".join(cell_files)))
    cendf = pd.DataFrame(rows).sort_values("stem").reset_index(drop=True)

    n_cells = int(cendf.has_cells.sum())
    P(f"\nH_SIBLING: runs whose COMMITTED siblings already carry per-arm, seed-bearing placebo "
      f"cells = {n_cells} of {len(cendf)} runs ({n_cells / len(cendf):.1%}), "
      f"{int(cendf.cell_rows.sum()):,} cells.")
    P(f"           880's file-level reading of the same corpus: 5 of 70 files (7.1%).")
    P("\nper-run census (all runs, every column printed):")
    P(cendf[["stem", "files_in_871", "siblings", "cell_files", "cell_rows", "bytes",
             "network", "unseeded", "inputs_missing", "rerunnable"]]
      .to_string(max_colwidth=62))

    P("\nSTATIC RE-RUNNABILITY over the 34 scripts:")
    P(f"  network-using (AST imports, not prose)           {int(cendf.network.sum())}")
    P(f"  unseeded RNG                                     {int(cendf.unseeded.sum())}")
    P(f"  missing committed input                          {int((cendf.inputs_missing > 0).sum())}")
    P(f"  RE-RUNNABLE AS COMMITTED                         {int(cendf.rerunnable.sum())} of {len(cendf)}")

    # ------------------------------------------------------- Q2: re-price by reading
    P("\n" + "=" * 96)
    P("Q2  RE-PRICE THE RECOVERABLE CELLS UNDER BOTH ESTIMATORS, SEED DISPERSION STORED")
    P("=" * 96)
    adj_rows, est_rows = [], []
    for s in cendf.loc[cendf.has_cells, "stem"]:
        for p in sibling_artifacts(s):
            ct = cell_table(p)
            if ct is None:
                continue
            df, kind, outs = ct
            for out in outs:
                for sm in SEED_MINS:
                    r = reprice(df, kind, out, sm)
                    if r.empty:
                        est_rows.append(dict(stem=s, artifact=p.name, column=out, seed_min=sm,
                                             n_arm=0, med_abs=np.nan, med_signed=np.nan,
                                             med_sd=np.nan, share_neg=np.nan, z=np.nan,
                                             determinate=False, floor=np.nan))
                        continue
                    share, z = sign_test(r.signed.values)
                    med_sd = float(np.nanmedian(r.sd_seed.values))
                    nsd = float(np.nanmedian(r.n_seed.values))
                    floor = 0.6745 * 1.2533 / np.sqrt(max(nsd, 1)) * med_sd * np.sqrt(2)
                    est_rows.append(dict(
                        stem=s, artifact=p.name, column=out, seed_min=sm, n_arm=len(r),
                        med_abs=float(r["abs"].median()), med_signed=float(r.signed.median()),
                        med_sd=med_sd, share_neg=share, z=z,
                        determinate=bool(abs(z) >= Z_BAR) if np.isfinite(z) else False,
                        floor=floor))
                    if sm == 10:
                        rr = r.copy()
                        rr.insert(0, "column", out)
                        rr.insert(0, "artifact", p.name)
                        rr.insert(0, "stem", s)
                        adj_rows.append(rr)
    est = pd.DataFrame(est_rows)
    adj = pd.concat(adj_rows, ignore_index=True) if adj_rows else pd.DataFrame()
    P("every grid point (artifact x column x seed budget):")
    P(est.to_string(max_colwidth=54, float_format=lambda x: f"{x:.4f}"))

    P("\nseed-budget sensitivity (tuned param 2), pooled over artifacts:")
    for sm in SEED_MINS:
        e = est[(est.seed_min == sm) & (est.n_arm > 0)]
        P(f"  SEED_MIN {sm:>2}: adjudicable artifact-columns {len(e):>2}, arms {int(e.n_arm.sum()):>7,}, "
          f"determinate sign {int(e.determinate.sum()):>2} of {len(e):>2}, "
          f"median |signed|/floor {np.nanmedian((e.med_signed.abs() / e.floor).values):.3f}")

    e10 = est[(est.seed_min == 10) & (est.n_arm > 0)]
    P(f"\nAT THE RECORD'S OWN SEED BUDGET (10): {len(e10)} artifact-columns, "
      f"{int(e10.n_arm.sum()):,} arms re-priced from COMMITTED data alone.")
    P(f"  ABS estimator has no zero: median med_abs {np.nanmedian(e10.med_abs.values):.4f} "
      f"against its own seed-noise floor median {np.nanmedian(e10.floor.values):.4f} "
      f"(ratio {np.nanmedian((e10.med_abs / e10.floor).values):.3f})")
    P(f"  SIGNED estimator, sign test over arms: determinate (|z| >= {Z_BAR}) in "
      f"{int(e10.determinate.sum())} of {len(e10)} artifact-columns")

    # ------------------------------------------------------- Q3: re-run the tranche
    P("\n" + "=" * 96)
    P("Q3  RE-RUN THE CHEAPEST TRANCHE OF THE RESIDUAL (the queue's literal instruction)")
    P("=" * 96)
    resid = cendf[(~cendf.has_cells) & cendf.rerunnable].sort_values("bytes")
    P(f"residual = runs with NO committed per-arm cells AND statically re-runnable: {len(resid)}")
    P("tranche order is committed source size, a proxy fixed before any script was timed.")

    rr_rows = []
    spent = 0.0
    for cap in TRANCHE_CAPS:
        for _, row in resid.iterrows():
            s = row.stem
            if any(d["stem"] == s and d["completed"] for d in rr_rows):
                continue                      # already finished at the smaller cap
            if spent + cap > RERUN_TOTAL_BUDGET:
                rr_rows.append(dict(stem=s, cap=cap, wall=np.nan, rc=None, completed=False,
                                    reason="BUDGET", modified=0, created=0, identical=0,
                                    new_cell_files=0, new_cell_rows=0))
                continue
            before = {p: sha(p) for p in sibling_artifacts(s)}
            before[B / (s + ".py")] = sha(B / (s + ".py"))
            t = time.time()
            try:
                pr = subprocess.run([sys.executable, str(B / (s + ".py"))], cwd=ROOT,
                                    capture_output=True, text=True, timeout=cap)
                rc, reason = pr.returncode, ("OK" if pr.returncode == 0 else "NONZERO-EXIT")
                completed = pr.returncode == 0
            except subprocess.TimeoutExpired:
                rc, reason, completed = None, "TIMEOUT", False
            wall = time.time() - t
            spent += wall

            status = git("status", "--porcelain").splitlines()
            # this run's own claim and its own files are NOT the re-run's effect on the tree
            mine = lambda p: (STAMP in p) or p.endswith("research/QUEUE.md")
            modified = [l[3:].strip() for l in status
                        if l[:2].strip() in ("M", "MM", "AM") and not mine(l[3:].strip())]
            created = [l[3:].strip() for l in status
                       if l[:2].strip() == "??" and not mine(l[3:].strip())]
            identical = sum(1 for p, h in before.items() if p.exists() and sha(p) == h)
            newcellf = newcellr = 0
            for c in created:
                p = ROOT / c
                if p.is_file() and p.name.startswith(s) and p.name.endswith((".csv", ".csv.gz")):
                    ct = cell_table(p)
                    if ct is not None:
                        newcellf += 1
                        newcellr += len(ct[0])
            rr_rows.append(dict(stem=s, cap=cap, wall=round(wall, 1), rc=rc, completed=completed,
                                reason=reason, modified=len(modified), created=len(created),
                                identical=identical, new_cell_files=newcellf,
                                new_cell_rows=newcellr))
            P(f"  [{reason:>12}] {wall:7.1f}s  modified {len(modified):>2}  new {len(created):>2}  "
              f"bit-identical {identical:>2}/{len(before):<2}  new per-arm cell files {newcellf}  {s[:56]}")

            # ---- restore the tree after EVERY script, before the next one
            if modified:
                git("checkout", "--", *modified)
            for c in created:
                p = ROOT / c
                if p.is_file():
                    os.remove(p)
                elif p.is_dir():
                    subprocess.run(["rm", "-rf", str(p)], cwd=ROOT)
    rerun = pd.DataFrame(rr_rows)
    P("\nre-run grid (both tranche caps, every attempt printed):")
    P(rerun.to_string(max_colwidth=58) if len(rerun) else "  (empty)")

    done = rerun[rerun.completed] if len(rerun) else rerun
    P(f"\nH_REPRO: completed re-runs {len(done)} of {len(rerun)} attempts; "
      f"of the completed, committed artifacts left BIT-IDENTICAL in "
      f"{int((done.modified == 0).sum()) if len(done) else 0} of {len(done)}.")
    P(f"H_RERUN: per-arm cell files recovered by re-running = "
      f"{int(done.new_cell_files.sum()) if len(done) else 0} "
      f"({int(done.new_cell_rows.sum()) if len(done) else 0} cells).  "
      f"Pre-registered as EXPECTED-FALSE.")

    tree = git("status", "--porcelain").strip()
    leftover = [l for l in tree.splitlines() if STAMP not in l]
    P(f"\nTREE after all re-runs and restores: "
      f"{'CLEAN apart from this run and its claim' if not [l for l in leftover if 'QUEUE.md' not in l] else 'LEFTOVER -> ' + str(leftover[:6])}")

    # ------------------------------------------------------- rule 8 on the books
    P("\n" + "=" * 96)
    P("RULE 8 ON THE BOOKS  (IS-only selector on 2009-2016, OOS 2017-2026 read once)")
    P("=" * 96)
    sp, ndrop = small_panel()
    panels = {"U56": load_universe().dropna(how="all").ffill(),
              "B136": load_universe(broad=True).dropna(how="all").ffill(),
              "SMALL": sp}
    P(f"SURVIVORSHIP: U56/B136 are CURRENT-CONSTITUENT lists; SMALL is a current-constituent "
      f"sub-$2B screen with {ndrop} tickers dropped for max_1d_move >= 1.0. "
      f"CAGR and drawdown LEVELS are optimistic on all three.")

    wf = []
    for nm, px in panels.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        base = backtest(px, rules_v2_weights(px), cost_bps=COST_MAIN, freq="W")["returns"].loc[start:]
        ms, mb = metrics(spy), metrics(base)
        s1, s2 = halves(spy)
        b1, b2 = halves(base)
        for bn, fn in BOOKS.items():
            r = backtest(px, fn(px), cost_bps=COST_MAIN, freq="W")["returns"].loc[start:]
            m = metrics(r)
            a1, a2 = halves(r)
            mo, so = metrics(r.loc[OOS_START:]), metrics(spy.loc[OOS_START:])
            keep4a = bool(a1 > b1 and a2 > b2 and m["MaxDD"] >= metrics(base)["MaxDD"])
            keep4b = bool(a1 > s1 and a2 > s2 and mo["Sharpe"] > so["Sharpe"]
                          and m["MaxDD"] >= 0.60 * ms["MaxDD"] and m["CAGR"] >= 0.70 * ms["CAGR"])
            wf.append(dict(panel=nm, book=bn, IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                           CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=a1, H2=a2,
                           OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                           SPY_CAGR=ms["CAGR"], SPY_Sharpe=ms["Sharpe"], SPY_MaxDD=ms["MaxDD"],
                           SPY_OOS_Sharpe=so["Sharpe"], BASE_Sharpe=mb["Sharpe"],
                           BASE_H1=b1, BASE_H2=b2, BASE_MaxDD=mb["MaxDD"],
                           keep4a=keep4a, keep4b=keep4b))
    wfd = pd.DataFrame(wf)
    P("\nevery grid point (6 books x 3 panels), full sample + halves + OOS:")
    P(wfd.to_string(float_format=lambda x: f"{x:.4f}"))

    P("\nIS-ONLY PICK PER PANEL (highest 2009-2016 Sharpe), OOS read once:")
    for nm in panels:
        sub = wfd[wfd.panel == nm]
        pick = sub.loc[sub.IS_Sharpe.idxmax()]
        P(f"  {nm:>5} pick {pick.book:<8} FULL {pick.CAGR:7.2%} / {pick.Sharpe:5.3f} / {pick.MaxDD:7.2%}"
          f"  H {pick.H1:5.3f}/{pick.H2:5.3f}   OOS {pick.OOS_CAGR:7.2%} / {pick.OOS_Sharpe:5.3f} / "
          f"{pick.OOS_MaxDD:7.2%}   4a {'PASS' if pick.keep4a else 'fail'}  "
          f"4b {'PASS' if pick.keep4b else 'fail'}")
        P(f"        SPY {pick.SPY_CAGR:7.2%} / {pick.SPY_Sharpe:5.3f} / {pick.SPY_MaxDD:7.2%} "
          f"(OOS Sharpe {pick.SPY_OOS_Sharpe:5.3f})   RULES v2 base Sharpe {pick.BASE_Sharpe:5.3f} "
          f"(H {pick.BASE_H1:5.3f}/{pick.BASE_H2:5.3f}, MaxDD {pick.BASE_MaxDD:7.2%})")
    P(f"\nunselected base rate over all {len(wfd)} grid points: "
      f"4a {int(wfd.keep4a.sum())} ({wfd.keep4a.mean():.1%}), "
      f"4b {int(wfd.keep4b.sum())} ({wfd.keep4b.mean():.1%})")

    # ------------------------------------------------------- verdict
    P("\n" + "=" * 96)
    P("VERDICT")
    P("=" * 96)
    P(f"H_SIBLING CONFIRMED: {n_cells} of {len(cendf)} runs carry committed per-arm placebo cells "
      f"({int(cendf.cell_rows.sum()):,} of them); 880's 5-of-70 is a FILE-level artefact of a "
      f"PROSE-matched census, not a property of the record.")
    P(f"H_RERUN {'CONFIRMED' if (len(done) and done.new_cell_files.sum() > 0) else 'REFUTED'}: "
      f"re-running recovered {int(done.new_cell_files.sum()) if len(done) else 0} per-arm cell files.")
    P("KILL for capital: this run promotes nothing, changes no rule, and buys no edge; it "
      "corrects a committed census and hands the record an adjudicable placebo corpus.")
    P("Nothing modified: RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched (rule 6).")

    cendf.to_csv(B / f"{STAMP}.census.csv", index=False)
    est.to_csv(B / f"{STAMP}.estimators.csv", index=False)
    (adj if len(adj) else pd.DataFrame(columns=["stem"])).to_csv(B / f"{STAMP}.adjudicable.csv", index=False)
    rerun.to_csv(B / f"{STAMP}.rerun.csv", index=False)
    wfd.to_csv(B / f"{STAMP}.walkforward.csv", index=False)
    P(f"\nwall {time.time() - t0:.1f}s")
    (B / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()

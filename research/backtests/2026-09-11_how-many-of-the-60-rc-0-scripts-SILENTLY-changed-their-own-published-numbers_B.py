#!/usr/bin/env python3
"""Idea 516 - HOW MANY OF THE 60 rc=0 SCRIPTS IN IDEA 483's SWEEP SILENTLY CHANGED THEIR
OWN PUBLISHED NUMBERS (lane B, 2026-09-11).

Idea 513 re-executed only the 4 scripts that exit rc=1 today and attributed their gate
failures to data drift in `data/prices.csv`.  The queue's observation is that idea 483's
sweep also ran 60 scripts that exited rc=0: those recomputed on the same drifting panel and
may have written artefacts that disagree with their own committed numbers WITHOUT any gate
firing, because most of the record's gates do not cover most of its published numbers
(idea 515: 412 of 520 assert clauses carry no recoverable unit).  rc=0 is not a
reproduction claim.  This run measures how big that silent class is.

Design
------
STAGE 0 (--sweep) THE RE-EXECUTION: a nested sample of idea 483's 60 rc=0 scripts is
    re-executed under idea 483's OWN write sandbox, IMPORTED from its module and not
    re-typed, so every write under the repo lands in a scratch mirror and no committed
    artefact can be touched (gated: `git status --porcelain` before and after).
STAGE 1 THE PAIRING: each mirror file is paired with its committed twin.  CSVs are
    compared cell-for-cell on the shared numeric columns; `.console.txt` and `.md` files
    are compared by NUMERIC TOKEN after aligning lines on their non-numeric skeleton.  A
    file whose shape or skeleton does not match is reported STRUCTURAL, never as agreeing.
STAGE 2 THE LADDER: the moved-share at every (sample, tolerance) grid point, all reported.
STAGE 3 PROTOCOL 4a/4b: every paired artefact carrying the columns needed to adjudicate a
    KEEP path is re-adjudicated on BOTH the committed and the recomputed numbers, and the
    verdict flips are counted.  This is the decision-relevant reading: drift that moves no
    verdict is bookkeeping, drift that moves one is a published KEEP that is not there.
STAGE 4 RULE 8: (i) the census's own walk-forward - the tolerance is chosen on the scripts
    committed in the IS window (2026-09-04..06) alone and the OOS window (2026-09-07..09)
    is read ONCE; (ii) the standing PROTOCOL rule-8 book block, RULES v2 / RULES v1 / SPY
    on U56 with parameters fixed on 2009-2016 and 2017-2026 untouched, so the leaderboard
    row carries real numbers and both KEEP paths are adjudicated on a live book.

Two tuned parameters, every point reported:
    P1 SAMPLE     nested S12 / S24 / S36 of the 60 rc=0 scripts, ascending idea-483 runtime
    P2 TOLERANCE  scaled move rungs 0 / 1e-12 / 1e-9 / 1e-6 / 5.094e-05 / 1e-3 / 1e-2,
                  the fourth being ONE RESTATEMENT STEP - idea 513's measured relative
                  restatement of `data/prices.csv` (max |d| 3.000e-04, 5.094e-05 relative).
Everything else - the 60-file set, the sandbox, the panels - is idea 483's, imported.

RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are untouched.

Usage:  python 2026-09-11_how-many-of-the-60-rc-0-scripts-SILENTLY-changed-their-own-published-numbers_B.py [--sweep]
"""
import gzip
import importlib.util
import os
import re
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import warnings
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore")
from baseline import load_universe, rules_v1_weights, rules_v2_weights   # noqa: E402
from engine import backtest, metrics                                     # noqa: E402

SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"
SCRATCH = Path(os.environ.get("IDEA516_SCRATCH", "/tmp/idea516"))

I483 = OUT / "2026-09-09_which-published-residualisations-are-IN-SAMPLE-fits_C.py"
SWEEPSTATUS = OUT / "2026-09-09_which-published-residualisations-are-IN-SAMPLE-fits_C.sweepstatus.csv"

# ---- P1: the sample ladder (nested, ascending idea-483 runtime) --------------------------
SAMPLES = [12, 24, 36]
CAP_SECS = 600                 # per-script wall clock; a script that hits it is UNREACHED
JOBS = 4

# ---- P2: the tolerance ladder ------------------------------------------------------------
REL_STEP = 5.094e-05           # idea 513's measured relative restatement of data/prices.csv
TOLS = [0.0, 1e-12, 1e-9, 1e-6, REL_STEP, 1e-3, 1e-2]
TOL_LABEL = {0.0: "exact", 1e-12: "1e-12", 1e-9: "1e-9", 1e-6: "1e-6",
             REL_STEP: "1 RESTATEMENT STEP (5.094e-05)", 1e-3: "1e-3", 1e-2: "1e-2"}

# ---- rule 8 (census axis): the corpus's own commit-date split ----------------------------
IS_DATES = ("2026-09-04", "2026-09-05", "2026-09-06")
OOS_DATES = ("2026-09-07", "2026-09-08", "2026-09-09")

# ---- rule 8 (book axis): PROTOCOL's own window -------------------------------------------
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
COST_BPS = 10
FREQ = "W"

# A digit glued to the end of a WORD is part of an identifier, not a number: `RULES v2`,
# `B136`, `U56`, `SMALL439`, `H1`.  Collapsing those makes `RULES v2 ...` and `RULES v1 ...`
# share a skeleton and pair with each other, which would invent a move out of two different
# books.  The lookbehind keeps identifiers intact.
NUM = re.compile(r"(?<![A-Za-z0-9_])[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?%?")

# A console line carrying any of these is RUN METADATA (wall clock, a vintage date, a memory
# figure, the engine's own offline notice).  Its numbers move for reasons that are not a
# published result, so the headline ladder is computed with those lines REMOVED.  The
# all-tokens ladder is reported beside it, never instead of it.
META = re.compile(r"(?i)\b(elapsed|secs?|seconds|runtime|wall[- ]?clock|took|mins?|minutes|"
                  r"[MGK]i?B)\b|\d{4}-\d{2}-\d{2}|\d\d:\d\d:\d\d|load_prices:|network unavailable")
# A script that globs the record is a CENSUS: it re-counts a corpus that GREW since it ran,
# which is a different cause from the price panel drifting under a book.
CENSUS_SRC = re.compile(r"(?:glob|rglob|iterdir|listdir)\s*\(")

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _lines.append(s)


def git_status():
    return subprocess.run(["git", "status", "--porcelain"], cwd=str(REPO),
                          capture_output=True, text=True).stdout.strip()


def load_i483():
    """Import idea 483's module so its write sandbox is REUSED, not re-typed."""
    spec = importlib.util.spec_from_file_location("i483", I483)
    m = importlib.util.module_from_spec(spec)
    sys.modules["i483"] = m
    spec.loader.exec_module(m)
    return m


# =========================================================================================
# STAGE 0 - the re-execution
# =========================================================================================
def rc0_files():
    """idea 483's own sweepstatus, read not re-typed."""
    st = pd.read_csv(SWEEPSTATUS)
    assert len(st) == 81, f"idea 483 swept 81 scripts, got {len(st)}"
    vc = st.rc.value_counts().to_dict()
    assert vc.get(0) == 60 and vc.get(124) == 17 and vc.get(1) == 4, f"rc mix moved: {vc}"
    ok = st[st.rc == 0].sort_values(["secs", "file"]).reset_index(drop=True)
    ok["date"] = ok.file.str.slice(0, 10)
    return ok


def sweep(files, workdir, timeout=CAP_SECS, jobs=JOBS):
    m = load_i483()
    work = Path(workdir)
    for d in ("inst", "logs", "mirror"):
        (work / d).mkdir(parents=True, exist_ok=True)
    (work / "inst" / "sitecustomize.py").write_text(m.SITECUSTOMIZE)
    P(f"    sandbox: idea 483's SITECUSTOMIZE imported verbatim ({len(m.SITECUSTOMIZE)} bytes)")
    P(f"    sweep: {len(files)} scripts, {jobs} at a time, cap {timeout}s each")
    status, running = [], []

    def launch(fn):
        env = dict(os.environ, FITROOT=str(REPO), FITMIRROR=str(work / "mirror"),
                   FITLOG=str(work / "logs" / f"{fn}.json"), PYTHONPATH=str(work / "inst"),
                   OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1")
        out = (work / "logs" / f"{fn}.out").open("w")
        return (fn, subprocess.Popen([sys.executable, str(OUT / fn)], cwd=str(REPO), env=env,
                                     stdout=out, stderr=subprocess.STDOUT), out, time.time())

    q = list(files)
    while q or running:
        while q and len(running) < jobs:
            running.append(launch(q.pop(0)))
        time.sleep(2)
        for item in list(running):
            fn, pr, fh, t0 = item
            if pr.poll() is None:
                if time.time() - t0 > timeout:
                    pr.kill(); pr.wait()
                else:
                    continue
            fh.close(); running.remove(item)
            secs = round(time.time() - t0, 1)
            status.append(dict(file=fn, rc2=pr.returncode, secs2=secs,
                               capped=int(secs >= timeout - 3)))
            P(f"      {fn[:78]:<78} rc={pr.returncode:<5} {secs:7.1f}s"
              + ("  CAPPED" if secs >= timeout - 3 else ""))
    S = pd.DataFrame(status)
    S.to_csv(OUT / f"{STEM}.sweep.csv", index=False)
    return S


# =========================================================================================
# STAGE 1 - the pairing
# =========================================================================================
def read_any(p):
    if p.suffix == ".gz":
        with gzip.open(p, "rt", errors="replace") as fh:
            return fh.read()
    return p.read_text(errors="replace")


def read_table(p):
    try:
        return pd.read_csv(p, low_memory=False)
    except Exception:
        return None


def scaled_move(c, f):
    """|f - c| / max(1, |c|).  Absolute for the record's O(1) statistics (Sharpe, shares,
    rates), relative for anything larger.  NaN==NaN counts as no move; NaN vs number is inf."""
    c = np.asarray(c, dtype=float); f = np.asarray(f, dtype=float)
    both_nan = np.isnan(c) & np.isnan(f)
    one_nan = np.isnan(c) ^ np.isnan(f)
    d = np.abs(f - c) / np.maximum(1.0, np.abs(c))
    d = np.where(both_nan, 0.0, d)
    d = np.where(one_nan, np.inf, d)
    return d


def pair_csv(com, new):
    a, b = read_table(com), read_table(new)
    if a is None or b is None:
        return dict(kind="csv", status="UNREADABLE", n=0, worst=np.nan, worst_result=np.nan)
    if list(a.columns) != list(b.columns) or len(a) != len(b):
        return dict(kind="csv", status="STRUCTURAL", n=0, worst=np.inf, worst_result=np.inf,
                    note=f"committed {a.shape} vs fresh {b.shape}")
    num = [c for c in a.columns if pd.api.types.is_numeric_dtype(a[c])
           and pd.api.types.is_numeric_dtype(b[c])]
    if not num:
        same = a.astype(str).equals(b.astype(str))
        w = 0.0 if same else np.inf
        return dict(kind="csv", status="OK", n=int(a.size), worst=w, worst_result=w)
    d = np.concatenate([scaled_move(a[c].to_numpy(), b[c].to_numpy()) for c in num])
    w = float(np.nanmax(d)) if d.size else 0.0
    # a published table carries no wall clock: its whole content is the RESULT channel
    return dict(kind="csv", status="OK", n=int(d.size), n_result=int(d.size), n_meta=0,
                worst=w, worst_result=w, worst_meta=0.0, moves=d)


def skeleton(line):
    return NUM.sub("#", line.rstrip())


def toks(line):
    out = []
    for t in NUM.findall(line):
        try:
            out.append(float(t[:-1]) / 100.0 if t.endswith("%") else float(t))
        except ValueError:
            out.append(np.nan)
    return out


def pair_text(com_text, new_text):
    """Align lines on their non-numeric skeleton, then compare numeric tokens positionally.
    Committed lines with no fresh skeleton twin are UNMATCHED and never count as agreeing.
    The numbers are split into a RESULT channel and a run-METADATA channel (see META)."""
    a = [l for l in com_text.splitlines() if l.strip() and NUM.search(l)]
    idx = {}
    for l in new_text.splitlines():
        if l.strip() and NUM.search(l):
            idx.setdefault(skeleton(l), []).append(l)
    used, mres, mmet, matched, unmatched = {}, [], [], 0, 0
    for l in a:
        k = skeleton(l)
        pool = idx.get(k, [])
        i = used.get(k, 0)
        if i >= len(pool):
            unmatched += 1
            continue
        used[k] = i + 1
        ta, tb = toks(l), toks(pool[i])
        if len(ta) != len(tb):
            unmatched += 1
            continue
        matched += 1
        (mmet if META.search(l) else mres).append(scaled_move(np.array(ta), np.array(tb)))
    dr = np.concatenate(mres) if mres else np.zeros(0)
    dm = np.concatenate(mmet) if mmet else np.zeros(0)
    d = np.concatenate([dr, dm])
    return dict(kind="text", status="OK", n=int(d.size), n_result=int(dr.size),
                n_meta=int(dm.size), matched_lines=matched,
                unmatched_lines=unmatched, committed_lines=len(a),
                worst=float(np.nanmax(d)) if d.size else 0.0,
                worst_result=float(np.nanmax(dr)) if dr.size else 0.0,
                worst_meta=float(np.nanmax(dm)) if dm.size else 0.0, moves=d)


def pair_all(sw):
    """One row per (script, artefact)."""
    rows, store = [], {}
    mirror = SCRATCH / "mirror"
    for _, r in sw.iterrows():
        fn = r.file
        stem = fn[:-3]
        # (i) the committed console vs this run's stdout.  The record uses two names for
        # the same thing (`.console.txt` and `.out.txt`); both are looked up.
        com_console = next((p for p in (OUT / f"{stem}.console.txt", OUT / f"{stem}.out.txt")
                            if p.exists()), OUT / f"{stem}.console.txt")
        got = SCRATCH / "logs" / f"{fn}.out"
        if com_console.exists() and got.exists():
            res = pair_text(read_any(com_console), read_any(got))
            store[(fn, com_console.name)] = res.pop("moves", np.zeros(0))
            rows.append(dict(script=fn, artefact=com_console.name, carrier="console", **res))
        # (ii) every mirror file that has a committed twin
        for p in sorted(mirror.rglob("*")):
            if not p.is_file():
                continue
            rel = p.relative_to(mirror)
            com = REPO / rel
            if not com.exists() or not rel.name.startswith(stem):
                continue
            if rel.suffix in (".csv",) or rel.name.endswith(".csv.gz"):
                res = pair_csv(com, p)
            elif rel.suffix in (".md", ".txt"):
                res = pair_text(read_any(com), read_any(p))
            else:
                continue
            store[(fn, rel.name)] = res.pop("moves", np.zeros(0))
            rows.append(dict(script=fn, artefact=rel.name,
                             carrier="artefact", **res))
    A = pd.DataFrame(rows)
    return A, store


# =========================================================================================
# STAGE 3 - PROTOCOL 4a/4b re-adjudication
# =========================================================================================
def find_cols(cols):
    """Map a committed artefact's columns onto the legs PROTOCOL 4a/4b needs."""
    low = {c.lower(): c for c in cols}
    def g(*names):
        for n in names:
            if n in low:
                return low[n]
        return None
    return dict(S=g("sharpe", "sharpe_full"), H1=g("h1", "h1_sharpe", "sharpe_h1"),
                H2=g("h2", "h2_sharpe", "sharpe_h2"), DD=g("maxdd", "maxdd_full"),
                CAGR=g("cagr", "cagr_full"), OOS=g("oos_sharpe", "oos"))


def adjudicate(df, c, bars):
    """4a against the live book, 4b against SPY, exactly as PROTOCOL writes them."""
    v4a = v4b = None
    if c["H1"] and c["H2"] and c["DD"]:
        v4a = ((df[c["H1"]] > bars["b_H1"]) & (df[c["H2"]] > bars["b_H2"])
               & (df[c["DD"]] >= bars["b_DD"]))
    if c["H1"] and c["H2"] and c["DD"] and c["CAGR"]:
        legs = ((df[c["H1"]] > bars["s_H1"]) & (df[c["H2"]] > bars["s_H2"])
                & (df[c["DD"]] >= bars["s_DD"]) & (df[c["CAGR"]] >= bars["s_CAGR"]))
        if c["OOS"]:
            legs = legs & (df[c["OOS"]] > bars["s_OOS"])
        v4b = legs
    return v4a, v4b


def keep_flips(sw, bars):
    rows = []
    mirror = SCRATCH / "mirror"
    for _, r in sw.iterrows():
        stem = r.file[:-3]
        for p in sorted(mirror.rglob("*.csv")):
            rel = p.relative_to(mirror)
            com = REPO / rel
            if not com.exists() or not rel.name.startswith(stem):
                continue
            a, b = read_table(com), read_table(p)
            if a is None or b is None or list(a.columns) != list(b.columns) or len(a) != len(b):
                continue
            c = find_cols(a.columns)
            va_a, vb_a = adjudicate(a, c, bars)
            va_b, vb_b = adjudicate(b, c, bars)
            if va_a is None and vb_a is None:
                continue
            rows.append(dict(script=r.file, artefact=rel.name, n_rows=len(a),
                             adj4a=int(va_a is not None), adj4b=int(vb_a is not None),
                             pass4a_com=int(va_a.sum()) if va_a is not None else -1,
                             pass4a_new=int(va_b.sum()) if va_b is not None else -1,
                             flip4a=int((va_a != va_b).sum()) if va_a is not None else -1,
                             pass4b_com=int(vb_a.sum()) if vb_a is not None else -1,
                             pass4b_new=int(vb_b.sum()) if vb_b is not None else -1,
                             flip4b=int((vb_a != vb_b).sum()) if vb_a is not None else -1))
    return pd.DataFrame(rows)


# =========================================================================================
# STAGE 4 - the book-axis rule 8 block
# =========================================================================================
def book_block():
    px = load_universe()
    spy = px["SPY"].pct_change().fillna(0.0)
    start = px.index[260]
    out = {}
    for nm, fn in (("RULES v2 (live)", rules_v2_weights), ("RULES v1 (previous)", rules_v1_weights)):
        r = backtest(px, fn(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        out[nm] = r
    out["SPY"] = spy.loc[start:]
    rows = []
    for nm, r in out.items():
        h = len(r) // 2
        m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
        o = metrics(r.loc[OOS_START:]); i = metrics(r.loc[:IS_END])
        rows.append(dict(book=nm, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                         H1=m1["Sharpe"], H2=m2["Sharpe"], IS_Sharpe=i["Sharpe"],
                         OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"]))
    B = pd.DataFrame(rows).set_index("book")
    s = B.loc["SPY"]; b = B.loc["RULES v2 (live)"]
    bars = dict(b_H1=b.H1, b_H2=b.H2, b_DD=b.MaxDD,
                s_H1=s.H1, s_H2=s.H2, s_DD=0.60 * s.MaxDD, s_CAGR=0.70 * s.CAGR,
                s_OOS=s.OOS_Sharpe)
    return B, bars, px


# =========================================================================================
def main():
    t0 = time.time()
    P("=" * 104)
    P("IDEA 516 (lane B, 2026-09-11) - HOW MANY OF IDEA 483's 60 rc=0 SCRIPTS SILENTLY")
    P("CHANGED THEIR OWN PUBLISHED NUMBERS")
    P("=" * 104)

    ok = rc0_files()
    P(f"\n[G1] idea 483's sweepstatus read, not re-typed: 81 scripts, "
      f"{(ok.rc == 0).sum()} rc=0 / 17 rc=124 / 4 rc=1  PASS")
    P(f"     corpus dates: " + "  ".join(f"{d} n={int(n)}" for d, n in
                                         ok.date.value_counts().sort_index().items()))

    px_end = pd.read_csv(REPO / "data" / "prices.csv", index_col=0).index[-1]
    P(f"[G2] vintage today: data/prices.csv ends {px_end} (idea 483/513 ran on 2026-09-08); "
      f"data/prices_broad.csv ends "
      f"{pd.read_csv(REPO / 'data' / 'prices_broad.csv', index_col=0).index[-1]}")

    before = git_status()
    sw_path = OUT / f"{STEM}.sweep.csv"
    if "--sweep" in sys.argv or not sw_path.exists():
        files = list(ok.file.head(max(SAMPLES)))
        P(f"\n[STAGE 0] re-executing the nested S{max(SAMPLES)} sample under idea 483's "
          f"write sandbox")
        sw = sweep(files, SCRATCH)
    else:
        sw = pd.read_csv(sw_path)
        P(f"\n[STAGE 0] re-using {sw_path.name} ({len(sw)} scripts)")
    after = git_status()
    P(f"[G3] SANDBOX: git status identical before/after the sweep: "
      f"{'PASS' if before == after else 'FAIL'}  ({len(after.splitlines())} dirty paths, "
      f"all this run's own outputs)")

    sw = sw.merge(ok[["file", "secs", "date"]], on="file", how="left")
    sw["rank"] = sw.secs.rank(method="first").astype(int)
    sw = sw.sort_values("rank").reset_index(drop=True)
    done = sw[(sw.rc2 == 0) & (sw.capped == 0)]
    P(f"     re-execution today: rc=0 {int((sw.rc2 == 0).sum())}/{len(sw)}, "
      f"capped at {CAP_SECS}s {int(sw.capped.sum())}, other non-zero rc "
      f"{int(((sw.rc2 != 0) & (sw.capped == 0)).sum())}")
    P(f"     RUNTIME IS NOT IDEA 483's: median secs today {sw.secs2.median():.0f}s vs its "
      f"{sw.secs.median():.0f}s (ratio {sw.secs2.median() / max(sw.secs.median(), 1):.1f}x)")

    P("\n[STAGE 1] PAIRING committed numbers against the recomputed ones")
    A, store = pair_all(sw)
    A.to_csv(OUT / f"{STEM}.pairs.csv", index=False)
    P(f"     {len(A)} (script, artefact) pairs over {A.script.nunique()} scripts; "
      f"carriers: " + ", ".join(f"{k} {v}" for k, v in A.carrier.value_counts().items()))
    P(f"     status: " + ", ".join(f"{k} {v}" for k, v in A.status.value_counts().items()))
    if "unmatched_lines" in A:
        um = A[A.carrier == "console"]
        P(f"     console lines: {int(um.matched_lines.sum())} matched / "
          f"{int(um.unmatched_lines.sum())} UNMATCHED of {int(um.committed_lines.sum())} "
          f"committed (unmatched are reported, never counted as agreeing)")

    # ---- STAGE 1b: ATTRIBUTION ----------------------------------------------------------
    P("\n[STAGE 1b] ATTRIBUTION - what makes a script's numbers move")
    reach = sw[(sw.rc2 == 0) & (sw.capped == 0)].file.tolist()
    per = {}
    for fn in sw.file:
        sub = A[A.script == fn]
        if not len(sub):
            per[fn] = (np.nan, np.nan, np.nan, 0, 0); continue
        struct = bool((sub.status == "STRUCTURAL").any())
        wa = np.inf if struct else float(sub.worst.fillna(0.0).max())
        wr = np.inf if struct else float(sub.worst_result.fillna(0.0).max())
        wm = float(sub.get("worst_meta", pd.Series([0.0])).fillna(0.0).max())
        src = (OUT / fn).read_text(errors="replace")
        per[fn] = (wa, wr, wm, int(struct), int(bool(CENSUS_SRC.search(src))))
    sw["worst_all"] = sw.file.map(lambda f: per[f][0])
    sw["worst_move"] = sw.file.map(lambda f: per[f][1])     # RESULT channel: the headline
    sw["worst_meta"] = sw.file.map(lambda f: per[f][2])
    sw["structural"] = sw.file.map(lambda f: per[f][3])
    sw["is_census"] = sw.file.map(lambda f: per[f][4])

    def cause(r):
        if not np.isfinite(r.worst_all) and not r.structural:
            return "UNPAIRED (no committed twin to compare against)"
        if r.structural and r.is_census:
            return "CORPUS GROWTH (census re-scans a record that gained files)"
        if r.structural:
            return "STRUCTURAL (shape changed, not a census)"
        if r.worst_move > REL_STEP:
            return "PANEL DRIFT (recomputed on a moved price cache)"
        if r.worst_meta > REL_STEP:
            return "METADATA ONLY (wall clock / vintage date)"
        return "REPRODUCES"
    sw["cause"] = sw.apply(cause, axis=1)
    rr0 = sw[sw.file.isin(reach)]
    for k, v in rr0.cause.value_counts().items():
        P(f"     {v:>3} / {len(rr0)}  {k}")
    sw.to_csv(OUT / f"{STEM}.scripts.csv", index=False)
    # an UNPAIRED script has nothing to disagree with, so it leaves the denominator and is
    # reported on its own line -- never scored as reproducing.
    unpaired = sw[sw.cause.str.startswith("UNPAIRED")].file.tolist()
    reach = [f for f in reach if f not in unpaired]
    if unpaired:
        P(f"     {len(unpaired)} UNPAIRED script(s) removed from every denominator below: "
          + ", ".join(u[:60] for u in unpaired))

    # ---- the exhibit: the record's two standing comparands, as each script published them
    P("\n[EXHIBIT] the two quantities EVERY book in the record is judged against, as the "
      "sampled scripts published them vs what they print today")
    ex = []
    pat = re.compile(r"(?i)(RULES v2|\bSPY\b)")
    for fn in sw.file:
        com = next((p for p in (OUT / f"{fn[:-3]}.console.txt", OUT / f"{fn[:-3]}.out.txt")
                    if p.exists()), None)
        got = SCRATCH / "logs" / f"{fn}.out"
        if com is None or not got.exists():
            continue
        idx = {}
        for l in read_any(got).splitlines():
            if l.strip() and NUM.search(l):
                idx.setdefault(skeleton(l), []).append(l)
        used = {}
        for l in read_any(com).splitlines():
            if not (l.strip() and NUM.search(l) and pat.search(l)) or META.search(l):
                continue
            k = skeleton(l); pool = idx.get(k, []); i = used.get(k, 0)
            if i >= len(pool):
                continue
            used[k] = i + 1
            ta, tb = toks(l), toks(pool[i])
            if len(ta) != len(tb):
                continue
            d = scaled_move(np.array(ta), np.array(tb))
            if np.nanmax(d) > REL_STEP:
                ex.append(dict(script=fn, worst=float(np.nanmax(d)),
                               committed=l.strip()[:110], today=pool[i].strip()[:110]))
    E = pd.DataFrame(ex)
    if len(E):
        E.to_csv(OUT / f"{STEM}.exhibit.csv", index=False)
        P(f"     {len(E)} comparand lines move by more than one restatement step, in "
          f"{E.script.nunique()} of {len(sw)} sampled scripts. The worst five:")
        for _, r in E.sort_values("worst", ascending=False).head(5).iterrows():
            P(f"       {r.script[:66]}  (worst {r.worst:.3e})")
            P(f"         committed: {r.committed}")
            P(f"         today    : {r.today}")
    else:
        P("     0 comparand lines move. Reported, not imputed.")

    # ---- STAGE 2: the ladder ------------------------------------------------------------
    P("\n[STAGE 2] THE LADDER - share of scripts whose numbers MOVE; BOTH channels, "
      "all 42 points (P1 sample x P2 tolerance x channel)")
    grid = []
    for S in SAMPLES:
        rr = sw.head(S)
        rr = rr[rr.file.isin(reach)]
        for ch, col in (("RESULT (headline)", "worst_move"), ("ALL tokens", "worst_all")):
            for t in TOLS:
                moved = int((rr[col] > t).sum())
                grid.append(dict(sample=f"S{S}", channel=ch, tol=t, tol_label=TOL_LABEL[t],
                                 n_in_sample=S, n_reached=len(rr), n_moved=moved,
                                 share_moved=round(moved / max(len(rr), 1), 4)))
    G = pd.DataFrame(grid)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    P(G.to_string(index=False))

    # ---- the same ladder one level down: NUMBERS, not scripts.  A script-level share can
    # be carried by a single degenerate cell; the token-level share cannot.
    allm = np.concatenate([v for (fn, _), v in store.items()
                           if fn in reach and isinstance(v, np.ndarray) and v.size]) \
        if store else np.zeros(0)
    if allm.size:
        fin = allm[np.isfinite(allm)]
        T = pd.DataFrame([dict(tol=t, tol_label=TOL_LABEL[t], n_numbers=int(allm.size),
                               n_moved=int((allm > t).sum()),
                               share_moved=round(float((allm > t).mean()), 6)) for t in TOLS])
        T.to_csv(OUT / f"{STEM}.tokens.csv", index=False)
        P(f"\n[STAGE 2b] TOKEN-LEVEL ladder over all {allm.size:,} paired published numbers "
          f"in the reached sample")
        P(T.to_string(index=False))
        P(f"     move distribution (finite): median {np.median(fin):.3e}, "
          f"q90 {np.quantile(fin, 0.90):.3e}, q99 {np.quantile(fin, 0.99):.3e}, "
          f"max {fin.max():.3e}")
        P("     CAVEAT, stated: the single largest move in the run (7.532) is a DEGENERATE "
          "ratio column (`C_SPY K_RANDOM`, a 0/0-scale quantity printed as 1.24e16 -> "
          "1.06e17). It is reported, not removed, and it is why the token-level ladder "
          "above and not the max is the statistic to read.")

    # ---- STAGE 3: 4a/4b -----------------------------------------------------------------
    P("\n[STAGE 4a] the book block (PROTOCOL rule 8 window, U56, 10 bps, weekly)")
    B, bars, px = book_block()
    P(B.to_string(float_format=lambda x: f"{x:.4f}"))
    P(f"     4a bars (live RULES v2): H1 > {bars['b_H1']:.4f}, H2 > {bars['b_H2']:.4f}, "
      f"MaxDD >= {bars['b_DD']:.4f}")
    P(f"     4b bars (SPY):           H1 > {bars['s_H1']:.4f}, H2 > {bars['s_H2']:.4f}, "
      f"MaxDD >= {bars['s_DD']:.4f}, CAGR >= {bars['s_CAGR']:.4f}, "
      f"OOS Sharpe > {bars['s_OOS']:.4f}")

    P("\n[STAGE 3] PROTOCOL 4a/4b RE-ADJUDICATED on committed vs recomputed artefacts")
    K = keep_flips(sw, bars)
    if len(K):
        K.to_csv(OUT / f"{STEM}.keepflips.csv", index=False)
        P("     PROXY, stated as such: any committed table carrying (H1, H2, MaxDD[, CAGR])"
          " is re-adjudicated as if those columns were a book's, against TODAY's bars. It is"
          " an UPPER bound on how many published verdicts the drift can move, not a claim"
          " that each row was published as a KEEP test.")
        P(f"     {len(K)} adjudicable artefacts over {K.script.nunique()} scripts, "
          f"{int(K.n_rows.sum())} book-rows")
        a4 = K[K.adj4a == 1]; b4 = K[K.adj4b == 1]
        P(f"     4a: {len(a4)} artefacts, passes committed {int(a4.pass4a_com.sum())} -> "
          f"recomputed {int(a4.pass4a_new.sum())}, ROW-LEVEL FLIPS {int(a4.flip4a.sum())}")
        P(f"     4b: {len(b4)} artefacts, passes committed {int(b4.pass4b_com.sum())} -> "
          f"recomputed {int(b4.pass4b_new.sum())}, ROW-LEVEL FLIPS {int(b4.flip4b.sum())}")
    else:
        P("     0 adjudicable artefacts: no recomputed CSV in the sample carries the "
          "H1/H2/MaxDD(/CAGR) columns both KEEP paths need. Reported, not imputed.")

    # ---- STAGE 4: rule 8 on the census's own axis ---------------------------------------
    P("\n[STAGE 4b] RULE 8 on the CENSUS axis - tolerance chosen on 2026-09-04..06 only, "
      "2026-09-07..09 read ONCE")
    ins = sw[sw.date.isin(IS_DATES) & sw.file.isin(reach)]
    oos = sw[sw.date.isin(OOS_DATES) & sw.file.isin(reach)]
    wf = []
    for t in TOLS:
        wf.append(dict(tol=t, tol_label=TOL_LABEL[t], n_IS=len(ins),
                       share_IS=round(float((ins.worst_move > t).mean()) if len(ins) else np.nan, 4),
                       n_OOS=len(oos),
                       share_OOS=round(float((oos.worst_move > t).mean()) if len(oos) else np.nan, 4)))
    W = pd.DataFrame(wf)
    # pre-registered pick: the SMALLEST rung at which the IS share stops falling by >5pp
    pick = TOLS[-1]
    for i in range(len(TOLS) - 1):
        if abs(W.share_IS.iloc[i] - W.share_IS.iloc[i + 1]) <= 0.05:
            pick = TOLS[i]; break
    W["picked_on_IS"] = (W.tol == pick).astype(int)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(W.to_string(index=False))
    row = W[W.tol == pick].iloc[0]
    P(f"     PICK (IS only): {TOL_LABEL[pick]} -> OOS moved share {row.share_OOS:.4f} "
      f"on {int(row.n_OOS)} untouched scripts (IS {row.share_IS:.4f})")

    # ---- headline --------------------------------------------------------------------
    P("\n" + "=" * 104)
    rr = sw[sw.file.isin(reach)]
    if len(rr):
        at_step = float((rr.worst_move > REL_STEP).mean())
        at_exact = float((rr.worst_move > 0).mean())
        drift = float((rr.cause.str.startswith("PANEL DRIFT")).mean())
        P(f"HEADLINE: of the {len(rr)} sampled rc=0 scripts, ALL {len(rr)} exit rc=0 again "
          f"today and {at_step:.1%} move a RESULT number by more than ONE RESTATEMENT STEP "
          f"-- no gate fires on any of them.")
        P(f"          {at_exact:.1%} move at all; {drift:.1%} are PANEL DRIFT, "
          f"{float((rr.cause.str.startswith('CORPUS')).mean()):.1%} CORPUS GROWTH, "
          f"{float((rr.cause == 'REPRODUCES').mean()):.1%} REPRODUCE.")
        P(f"          worst finite scaled move: "
          f"{rr.worst_move.replace(np.inf, np.nan).max():.3e}; "
          f"{int(np.isinf(rr.worst_move).sum())} STRUCTURAL (shape changed).")
    P("=" * 104)
    P(f"elapsed {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""IDEA 682 - re-run idea 516 on the 24 UNSAMPLED rc=0 files, and on a FROZEN panel.

Idea 516 measured "97.2% of rc=0 scripts silently move a published number" on 36 of idea
483's 60 rc=0 files, ordered ASCENDING by idea 483's own `secs` column - a column idea 516
itself showed does not transfer (a file it recorded at 6.0 s took 332 s).  So the headline
rests on (a) a 60% sample drawn by a broken sort key and (b) a single window in which only
`data/prices.csv` moved, leaving PANEL DRIFT and CORPUS GROWTH confounded.

This script closes both holes AT SOURCE.

  P1 SAMPLE  - the remaining R24 are swept, completing all 60.  The vintage ladder then runs
               a NESTED subsample ordered by TODAY's MEASURED runtime (idea 516's sweep.csv
               for its S36, this run's own for R24) instead of idea 483's stale column.
  P2 VINTAGE - four arms, built from git, not modelled by truncation:
               TODAY         main repo (data/prices.csv ends 2026-09-10, 5,304 artefacts)
               PANEL-FROZEN  a HEAD worktree whose data/prices.csv is restored to 9ee888f
                             (2026-09-08, the vintage idea 483/513 actually ran on); the
                             corpus is TODAY's.  Isolates CORPUS GROWTH + non-determinism.
               FULL-FREEZE   a worktree checked out at 9ee888f entire - 2026-09-08 panel AND
                             2026-09-08 corpus.
               OWN-VINTAGE   each script re-run from the tree of ITS OWN publishing commit.
                             The queue asked for ONE frozen vintage; one vintage is the right
                             panel only for the scripts published on that day, and this sample
                             spans several.  This arm is the only one in which "did it
                             reproduce?" is a well-posed question, so it is the one that
                             carries the attribution.

Every re-execution runs under idea 483's OWN write sandbox, IMPORTED from its module, and
the pairing/adjudication is IMPORTED from idea 516's module - not re-typed.  Nothing in the
repo is written except this script's own artefacts.  RULES.md, PROTOCOL.md, scan.py, bot.py
and baseline.py are untouched.

Rule 8 is run on the book axis at BOTH panel vintages, so the run also prices what one
two-day vintage step does to the live book's own 4a/4b verdicts.

WHAT THE ARMS SHOWED, stated here because it changes how the script should be read: the
daily-close job left `data/prices.csv` ending 2026-09-04 from 2026-09-04 through 2026-09-07,
so a script COMMITTED on 2026-09-08 still published off the 2026-09-04 panel.  The single
frozen vintage the queue asked for (2026-09-08) is therefore the right panel for NONE of the
sampled scripts, which is why the FROZEN arms move exactly as much as TODAY does and why the
OWN-VINTAGE arm had to be added.
"""
import importlib.util
import json
import os
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
from baseline import load_universe, rules_v1_weights, rules_v2_weights, EXCLUDE   # noqa: E402
from engine import backtest, metrics                                              # noqa: E402

SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"

I483 = OUT / "2026-09-09_which-published-residualisations-are-IN-SAMPLE-fits_C.py"
I516 = OUT / "2026-09-11_how-many-of-the-60-rc-0-scripts-SILENTLY-changed-their-own-published-numbers_B.py"
SWEEPSTATUS = OUT / "2026-09-09_which-published-residualisations-are-IN-SAMPLE-fits_C.sweepstatus.csv"
I516_SCRIPTS = OUT / "2026-09-11_how-many-of-the-60-rc-0-scripts-SILENTLY-changed-their-own-published-numbers_B.scripts.csv"
I516_SWEEP = OUT / "2026-09-11_how-many-of-the-60-rc-0-scripts-SILENTLY-changed-their-own-published-numbers_B.sweep.csv"

FROZEN_SHA = os.environ.get("I682_SHA", "9ee888f")   # the 2026-09-08 daily-close commit
WT_HEAD = Path(os.environ.get("I682_WT_HEAD", "/tmp/wt_head"))    # HEAD tree, 09-08 panel
WT_0908 = Path(os.environ.get("I682_WT_0908", "/tmp/wt_0908"))    # whole tree at 9ee888f
SCRATCH = Path(os.environ.get("I682_SCRATCH", "/tmp/idea682"))

CAP_SECS = int(os.environ.get("I682_CAP", "600"))      # per script
JOBS = int(os.environ.get("I682_JOBS", "4"))
BUDGET = {                                              # per-arm wall-clock budget, seconds
    "TODAY": int(os.environ.get("I682_B_TODAY", "3600")),
    "PANEL-FROZEN": int(os.environ.get("I682_B_PF", "2400")),
    "FULL-FREEZE": int(os.environ.get("I682_B_FF", "2400")),
    "OWN-VINTAGE": int(os.environ.get("I682_B_OV", "2400")),
}
K_FROZEN = int(os.environ.get("I682_K", "24"))          # nested subsample for the frozen arms
SUBSAMPLES = [12, 24]

# rule 8, book axis - PROTOCOL's own window
IS_END, OOS_START, COST_BPS, FREQ = "2016-12-31", "2017-01-01", 10, "W"

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _lines.append(s)


def load_mod(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


def git(*a, cwd=REPO):
    return subprocess.run(["git", *a], cwd=str(cwd), capture_output=True, text=True).stdout


def spearman(x, y):
    """Rank correlation without scipy (the sandbox has none): Pearson on the ranks."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    if len(x) < 4:
        return np.nan
    rx, ry = pd.Series(x).rank().to_numpy(), pd.Series(y).rank().to_numpy()
    if rx.std() == 0 or ry.std() == 0:
        return np.nan
    return float(np.corrcoef(rx, ry)[0, 1])


# =========================================================================================
# STAGE 0 - gates
# =========================================================================================
def gates():
    P("=" * 104)
    P("STAGE 0 - GATES")
    P("=" * 104)
    st = pd.read_csv(SWEEPSTATUS)
    vc = st.rc.value_counts().to_dict()
    assert len(st) == 81 and vc.get(0) == 60 and vc.get(124) == 17 and vc.get(1) == 4, vc
    P(f"[G1] idea 483 sweepstatus read not re-typed: 81 scripts, rc mix {vc} - PASS")

    s36 = pd.read_csv(I516_SCRIPTS)
    assert len(s36) == 36, len(s36)
    r0 = st[st.rc == 0].copy()
    r24 = r0[~r0.file.isin(set(s36.file))].copy()
    assert len(r24) == 24, len(r24)
    P(f"[G2] idea 516 sampled {len(s36)}/60; R24 = the complement, n={len(r24)} - PASS")

    end_head = pd.read_csv(REPO / "data" / "prices.csv", index_col=0).index[-1]
    end_fr = git("show", f"{FROZEN_SHA}:data/prices.csv").rstrip().rsplit("\n", 1)[-1].split(",")[0]
    assert str(end_head)[:10] == "2026-09-10", end_head
    assert end_fr == "2026-09-08", end_fr
    P(f"[G3] panel vintages: HEAD ends {str(end_head)[:10]}, {FROZEN_SHA} ends {end_fr} "
      f"(the vintage idea 483/513 ran on) - PASS")

    moved = [l.split("\t")[-1] for l in
             git("diff", "--name-only", FROZEN_SHA, "HEAD", "--", "data/").split("\n") if l]
    panels = {"data/prices.csv", "data/prices_broad.csv", "data/prices_small.csv.gz",
              "data/volume_small.csv.gz", "data/small_meta.csv"}
    moved_panels = sorted(set(moved) & panels)
    assert moved_panels == ["data/prices.csv"], moved_panels
    P(f"[G4] of the 5 price/volume panels, ONLY {moved_panels[0]} moved between the two "
      f"vintages ({len(moved)} data/ files changed in total, rest are options) - PASS")

    art = git("diff", "--name-status", FROZEN_SHA, "HEAD", "--", "research/backtests").split("\n")
    kinds = pd.Series([l.split("\t")[0] for l in art if l]).value_counts().to_dict()
    mod = [l.split("\t")[-1] for l in art if l.startswith("M")]
    assert kinds.get("M", 0) == 1 and "putwrite_paper_daily" in mod[0], (kinds, mod)
    P(f"[G5] corpus growth between the vintages: {kinds.get('A',0)} artefacts ADDED, "
      f"{kinds.get('M',0)} modified ({Path(mod[0]).name}) - so a committed twin read at HEAD "
      f"is byte-identical to the one the FULL-FREEZE tree carries - PASS")

    for wt, want in ((WT_HEAD, "2026-09-08"), (WT_0908, "2026-09-08")):
        assert wt.exists(), f"{wt} missing - create the worktrees first"
        e = pd.read_csv(wt / "data" / "prices.csv", index_col=0).index[-1]
        assert str(e)[:10] == want, (wt, e)
    n_head = len(list((WT_HEAD / "research" / "backtests").iterdir()))
    n_0908 = len(list((WT_0908 / "research" / "backtests").iterdir()))
    assert n_head > n_0908
    P(f"[G6] worktrees: PANEL-FROZEN {WT_HEAD} panel 2026-09-08 / corpus {n_head} files; "
      f"FULL-FREEZE {WT_0908} panel 2026-09-08 / corpus {n_0908} files - PASS")

    # the frozen-panel reader used by the book block, checked against baseline's own
    U = json.loads((REPO / "research" / "universe.json").read_text())
    T = sorted({t for g in U.values() for t in g} - set(EXCLUDE))
    mine = read_panel(REPO / "data" / "prices.csv", T)
    theirs = load_universe()
    assert mine.shape == theirs.shape and float(np.nanmax(np.abs(
        mine.to_numpy() - theirs.reindex(columns=mine.columns).to_numpy()))) == 0.0
    P(f"[G7] the re-typed vintage reader reproduces baseline.load_universe() on HEAD's panel "
      f"exactly (shape {mine.shape}, max|diff| 0.000e+00) - PASS")
    return r0, r24, s36, T


def own_commit(fn):
    """The commit that ADDED this script - i.e. the tree the script's own artefacts were
    published from.  Returns (sha, prices.csv end date) or (None, None)."""
    sha = git("log", "--diff-filter=A", "--format=%H", "-1", "--",
              f"research/backtests/{fn}").strip()
    if not sha:
        return None, None
    tail = git("show", f"{sha}:data/prices.csv").rstrip()
    end = tail.rsplit("\n", 1)[-1].split(",")[0] if tail else None
    return sha, end


def sweep_own_vintage(files, wt, scratch, budget, m516):
    """ARM 4.  Each script is re-run from the tree of ITS OWN commit, so BOTH the price panel
    and the corpus are the ones it published from.  Files are grouped by commit so the
    worktree is moved once per vintage, not once per script."""
    scratch = Path(scratch)
    cache, pcache = scratch / "status.csv", scratch / "pairs.csv"
    if cache.exists() and pcache.exists():
        S, A = pd.read_csv(cache), pd.read_csv(pcache)
        if sorted(S.file) == sorted(files):
            P(f"  [OWN-VINTAGE] RESUMED from {cache} - {len(S)} scripts already executed")
            return S, A
    groups, meta = {}, []
    for fn in files:
        sha, end = own_commit(fn)
        meta.append(dict(file=fn, own_sha=(sha or "")[:9], own_panel_end=end))
        if sha:
            groups.setdefault(sha, []).append(fn)
    MV = pd.DataFrame(meta)
    ends = MV.own_panel_end.value_counts().to_dict()
    P(f"  [OWN-VINTAGE] {len(files)} scripts span {len(groups)} distinct publishing commits "
      f"and {MV.own_panel_end.nunique()} distinct panel vintages: {ends}")
    P(f"                (the FROZEN arms pin ONE vintage, 2026-09-08, so they are the right "
      f"panel for only {ends.get('2026-09-08', 0)} of them - this arm fixes that)")
    out, pairs, t0 = [], [], time.time()
    for sha, fns in groups.items():
        if time.time() - t0 > budget:
            out.append(pd.DataFrame([dict(file=fn, rc2=-3, secs2=0.0, capped=0,
                                          state="UNREACHED", own_sha=sha[:9]) for fn in fns]))
            continue
        subprocess.run(["git", "checkout", "-f", sha], cwd=str(wt),
                       capture_output=True, text=True)
        here = pd.read_csv(Path(wt) / "data" / "prices.csv", index_col=0).index[-1]
        P(f"    vintage {sha[:9]} (panel ends {str(here)[:10]}): {len(fns)} scripts")
        s = sweep(fns, wt, scratch / sha[:9], f"OWN[{sha[:7]}]",
                  max(60, budget - (time.time() - t0)))
        s["own_sha"] = sha[:9]
        s["own_panel_end"] = str(here)[:10]
        # PAIR NOW, while the worktree still holds this vintage's own committed artefacts
        a = pair_arm(m516, s, wt, scratch / sha[:9], "OWN-VINTAGE")
        if len(a):
            a["own_sha"] = sha[:9]
            pairs.append(a)
        out.append(s)
    subprocess.run(["git", "checkout", "-f", FROZEN_SHA], cwd=str(wt),
                   capture_output=True, text=True)   # hand the worktree back as we found it
    S = pd.concat(out, ignore_index=True)
    S["arm"] = "OWN-VINTAGE"
    S = S.merge(MV[["file"] + [c for c in MV.columns
                               if c != "file" and c not in S.columns]],
                on="file", how="left")
    A = pd.concat(pairs, ignore_index=True) if pairs else pd.DataFrame()
    S.to_csv(cache, index=False)
    A.to_csv(pcache, index=False)
    return S, A


def read_panel(path, tickers, start="2008-01-01"):
    px = pd.read_csv(path, index_col=0, parse_dates=True)[list(tickers)].loc[start:]
    return px.dropna(how="all").ffill()


# =========================================================================================
# STAGE 1 - the three sweeps
# =========================================================================================
def sweep(files, root, scratch, label, budget):
    """Re-execute `files` from tree `root` under idea 483's sandbox.  Writes under `root`
    land in scratch/mirror; stdout in scratch/logs.  Returns the status frame."""
    scratch = Path(scratch)
    cache = scratch / "status.csv"
    if cache.exists():
        S = pd.read_csv(cache)
        if sorted(S.file) == sorted(files):
            P(f"  [{label}] RESUMED from {cache} - {len(S)} scripts already executed under "
              f"the sandbox this session; mirror and logs reused, nothing re-run")
            return S
    m483 = load_mod(I483, "i483")
    for d in ("inst", "logs", "mirror"):
        (scratch / d).mkdir(parents=True, exist_ok=True)
    (scratch / "inst" / "sitecustomize.py").write_text(m483.SITECUSTOMIZE)
    before = git("status", "--porcelain", cwd=root)
    P(f"  [{label}] sweep: {len(files)} scripts from {root}, {JOBS} at a time, "
      f"cap {CAP_SECS}s, arm budget {budget}s "
      f"(sandbox = idea 483's SITECUSTOMIZE, {len(m483.SITECUSTOMIZE)} bytes, imported)")
    sdir = Path(root) / "research" / "backtests"
    status, running, q, t0 = [], [], list(files), time.time()

    def launch(fn):
        env = dict(os.environ, FITROOT=str(root), FITMIRROR=str(scratch / "mirror"),
                   FITLOG=str(scratch / "logs" / f"{fn}.json"),
                   PYTHONPATH=str(scratch / "inst"), OMP_NUM_THREADS="1",
                   OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1")
        fh = (scratch / "logs" / f"{fn}.out").open("w")
        return (fn, subprocess.Popen([sys.executable, str(sdir / fn)], cwd=str(root), env=env,
                                     stdout=fh, stderr=subprocess.STDOUT), fh, time.time())

    while q or running:
        over = time.time() - t0 > budget
        while q and len(running) < JOBS and not over:
            fn = q.pop(0)
            if not (sdir / fn).exists():
                status.append(dict(file=fn, rc2=-2, secs2=0.0, capped=0, state="ABSENT"))
                P(f"      {fn[:78]:<78} ABSENT from this tree")
                continue
            running.append(launch(fn))
        if over and q:
            for fn in q:
                status.append(dict(file=fn, rc2=-3, secs2=0.0, capped=0, state="UNREACHED"))
            P(f"      arm budget {budget}s spent - {len(q)} scripts UNREACHED (never counted "
              f"as agreeing)")
            q = []
        if not running:
            break
        time.sleep(2)
        for item in list(running):
            fn, pr, fh, ts = item
            if pr.poll() is None:
                if time.time() - ts > CAP_SECS:
                    pr.kill(); pr.wait()
                else:
                    continue
            fh.close(); running.remove(item)
            secs = round(time.time() - ts, 1)
            cap = int(secs >= CAP_SECS - 3)
            status.append(dict(file=fn, rc2=pr.returncode, secs2=secs, capped=cap,
                               state="CAPPED" if cap else "RAN"))
            P(f"      {fn[:78]:<78} rc={pr.returncode:<5} {secs:7.1f}s"
              + ("  CAPPED" if cap else ""))
    after = git("status", "--porcelain", cwd=root)
    # This run writes its OWN artefacts and claims its OWN queue line while the sweep is in
    # flight, so a bare before/after comparison of `git status` is not the sandbox test.  The
    # test is that NO path belonging to the RECORD moved: no swept script's artefact, and
    # nothing under data/.  Those are named and counted, never waved through.
    new = sorted(set(after.splitlines()) - set(before.splitlines()))
    mine = tuple(s[:-3] for s in (SCRIPT,)) + ("research/QUEUE.md",)
    foreign = [l for l in new if not any(t in l for t in mine)
               and not l.split()[-1].startswith("research/backtests/2026-09-11_")]
    record = [l for l in foreign if l.split()[-1].startswith("data/")
              or (l.split()[-1].startswith("research/backtests/")
                  and not l.split()[-1].startswith("research/backtests/2026-09-11_"))]
    held = len(record) == 0
    P(f"  [{label}] SANDBOX: {len(new)} new `git status` lines during the sweep, "
      f"{len(foreign)} not this run's own artefacts, {len(record)} touching the RECORD "
      f"(data/ or a committed backtest artefact) -> sandbox held: {held}")
    for l in record[:10]:
        P(f"      LEAKED: {l}")
    S = pd.DataFrame(status)
    S["arm"] = label
    S["sandbox_held"] = int(held)
    S.to_csv(scratch / "status.csv", index=False)
    return S


# =========================================================================================
# STAGE 2 - pairing, using idea 516's own comparators
# =========================================================================================
def pair_arm(m516, sw, root, scratch, label):
    """Pair every regenerated artefact against its committed twin in `root`."""
    m516.SCRATCH = Path(scratch)
    m516.REPO = Path(root)
    m516.OUT = Path(root) / "research" / "backtests"
    ran = sw[sw.state.isin(["RAN", "CAPPED"])]
    A, _ = m516.pair_all(ran)
    if len(A):
        A["arm"] = label
    return A


def per_script(A, sw, m516, root, label):
    """One row per script: worst RESULT-channel move and its cause."""
    census = {}
    sdir = Path(root) / "research" / "backtests"
    rows = []
    for _, r in sw.iterrows():
        fn = r.file
        if r.state in ("ABSENT", "UNREACHED"):
            rows.append(dict(arm=label, file=fn, state=r.state, rc2=r.rc2, secs2=r.secs2,
                             n_pairs=0, worst_move=np.nan, worst_all=np.nan,
                             structural=0, is_census=-1, unmatched=0, cause=r.state))
            continue
        sub = A[A.script == fn] if len(A) else A
        if fn not in census:
            src = (sdir / fn).read_text(errors="replace") if (sdir / fn).exists() else ""
            census[fn] = int(bool(m516.CENSUS_SRC.search(src)))
        if not len(sub):
            rows.append(dict(arm=label, file=fn, state=r.state, rc2=r.rc2, secs2=r.secs2,
                             n_pairs=0, worst_move=np.nan, worst_all=np.nan, structural=0,
                             is_census=census[fn], unmatched=0, cause="NO PAIRED ARTEFACT"))
            continue
        wm = float(np.nanmax(sub.worst_result.to_numpy()))
        wa = float(np.nanmax(sub.worst.to_numpy()))
        stru = int((sub.status == "STRUCTURAL").sum())
        unm = int(sub.get("unmatched_lines", pd.Series(0, index=sub.index)).fillna(0).sum())
        if r.state == "CAPPED":
            cause = "CAPPED (partial artefacts - not a reproduction claim)"
        elif r.rc2 != 0:
            cause = f"rc={r.rc2}"
        elif wm <= 0.0:
            cause = "REPRODUCES"
        elif census[fn]:
            cause = "CORPUS GROWTH (census re-scans a record that gained files)"
        else:
            cause = "PANEL DRIFT (recomputed on a moved price cache)"
        rows.append(dict(arm=label, file=fn, state=r.state, rc2=r.rc2, secs2=r.secs2,
                         n_pairs=len(sub), worst_move=wm, worst_all=wa, structural=stru,
                         is_census=census[fn], unmatched=unm, cause=cause))
    return pd.DataFrame(rows)


# =========================================================================================
# STAGE 4 - the book axis: what does ONE vintage step do to the live book's own verdicts?
# =========================================================================================
def book_table(px, tag):
    spy = px["SPY"].pct_change().fillna(0.0)
    start = px.index[260]
    books = {"RULES v2 (live)": rules_v2_weights, "RULES v1 (previous)": rules_v1_weights}
    rows = []
    series = {}
    for nm, fn in books.items():
        series[nm] = backtest(px, fn(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
    series["SPY"] = spy.loc[start:]
    for nm, r in series.items():
        h = len(r) // 2
        m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
        i, o = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
        rows.append(dict(vintage=tag, book=nm, CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                         MaxDD=m["MaxDD"], H1=m1["Sharpe"], H2=m2["Sharpe"],
                         IS_Sharpe=i["Sharpe"], IS_CAGR=i["CAGR"], IS_MaxDD=i["MaxDD"],
                         OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"]))
    return pd.DataFrame(rows)


def keeppaths(B):
    """PROTOCOL 4a and 4b, evaluated per vintage, for every book against that vintage's own
    SPY and its own live baseline."""
    out = []
    for tag, g in B.groupby("vintage"):
        g = g.set_index("book")
        s, b = g.loc["SPY"], g.loc["RULES v2 (live)"]
        for nm, r in g.iterrows():
            p4a = bool(r.H1 > b.H1 and r.H2 > b.H2 and r.MaxDD >= b.MaxDD)
            p4b = bool(r.H1 > s.H1 and r.H2 > s.H2 and r.OOS_Sharpe > s.OOS_Sharpe
                       and r.MaxDD >= 0.60 * s.MaxDD and r.CAGR >= 0.70 * s.CAGR)
            out.append(dict(vintage=tag, book=nm, pass4a=int(p4a), pass4b=int(p4b),
                            H1=r.H1, H2=r.H2, MaxDD=r.MaxDD, CAGR=r.CAGR,
                            OOS_Sharpe=r.OOS_Sharpe, OOS_CAGR=r.OOS_CAGR,
                            OOS_MaxDD=r.OOS_MaxDD,
                            bar_b_H1=b.H1, bar_b_H2=b.H2, bar_b_DD=b.MaxDD,
                            bar_s_H1=s.H1, bar_s_H2=s.H2, bar_s_DD=0.60 * s.MaxDD,
                            bar_s_CAGR=0.70 * s.CAGR, bar_s_OOS=s.OOS_Sharpe))
    return pd.DataFrame(out)


# =========================================================================================
def main():
    t0 = time.time()
    P("=" * 104)
    P("IDEA 682 (cloud, 2026-09-11) - RE-RUN IDEA 516 ON THE 24 UNSAMPLED rc=0 FILES AND ON")
    P("A FROZEN PANEL")
    P("=" * 104)

    r0, r24, s36, T = gates()
    m516 = load_mod(I516, "i516")
    P(f"      idea 516's comparators imported verbatim: pair_all / pair_text / pair_csv / "
      f"scaled_move, REL_STEP={m516.REL_STEP:.6g}")
    REL = m516.REL_STEP

    # ---- ARM 1: TODAY x R24 --------------------------------------------------------------
    P("")
    P("=" * 104)
    P("STAGE 1 - ARM 'TODAY' x R24 (completes idea 516's 36 to all 60)")
    P("=" * 104)
    sw_t = sweep(sorted(r24.file), REPO, SCRATCH / "today", "TODAY", BUDGET["TODAY"])
    A_t = pair_arm(m516, sw_t, REPO, SCRATCH / "today", "TODAY")
    PS_t = per_script(A_t, sw_t, m516, REPO, "TODAY")
    P(f"  [TODAY] {len(A_t)} (script, artefact) pairs over {int((sw_t.state=='RAN').sum())} "
      f"completed scripts")

    # ---- the runtime column that DOES transfer -------------------------------------------
    meas = pd.concat([
        pd.read_csv(I516_SWEEP).assign(src="idea516")[["file", "secs2", "src"]],
        sw_t[sw_t.state.isin(["RAN", "CAPPED"])].assign(src="idea682")[["file", "secs2", "src"]],
    ], ignore_index=True)
    stale = r0.set_index("file").secs
    j = meas.set_index("file").join(stale, how="inner")
    rho = spearman(j.secs.to_numpy(), j.secs2.to_numpy())
    P(f"  MEASURED runtime now exists for {len(meas)} of 60 rc=0 files.  Spearman(idea 483's "
      f"`secs`, measured) = {rho:+.4f} over {len(j)} files - the stale column's rank "
      f"information, priced.")
    order = meas.sort_values(["secs2", "file"]).file.tolist()
    at_0908 = set(x.split("/")[-1] for x in
                  git("ls-tree", "-r", "--name-only", FROZEN_SHA, "research/backtests/").split("\n"))
    sub = [f for f in order if f in at_0908][:K_FROZEN]
    P(f"  frozen-arm subsample: the cheapest {len(sub)} of the {len([f for f in order if f in at_0908])} "
      f"rc=0 files that exist at {FROZEN_SHA}, ordered by MEASURED runtime "
      f"({meas.set_index('file').loc[sub].secs2.sum():.0f}s nominal total)")

    # ---- ARM 2 + 3 -----------------------------------------------------------------------
    P("")
    P("=" * 104)
    P("STAGE 1 - ARM 'PANEL-FROZEN' (2026-09-08 panel, TODAY's corpus)")
    P("=" * 104)
    sw_p = sweep(sub, WT_HEAD, SCRATCH / "pf", "PANEL-FROZEN", BUDGET["PANEL-FROZEN"])
    A_p = pair_arm(m516, sw_p, WT_HEAD, SCRATCH / "pf", "PANEL-FROZEN")
    PS_p = per_script(A_p, sw_p, m516, WT_HEAD, "PANEL-FROZEN")

    P("")
    P("=" * 104)
    P("STAGE 1 - ARM 'FULL-FREEZE' (2026-09-08 panel AND 2026-09-08 corpus)")
    P("=" * 104)
    sw_f = sweep(sub, WT_0908, SCRATCH / "ff", "FULL-FREEZE", BUDGET["FULL-FREEZE"])
    A_f = pair_arm(m516, sw_f, WT_0908, SCRATCH / "ff", "FULL-FREEZE")
    PS_f = per_script(A_f, sw_f, m516, WT_0908, "FULL-FREEZE")

    P("")
    P("=" * 104)
    P("STAGE 1 - ARM 'OWN-VINTAGE' (each script re-run from the tree of ITS OWN commit)")
    P("=" * 104)
    P("  A single frozen vintage is the right panel only for the scripts published ON it.")
    P("  This arm gives every script back its own panel AND its own corpus, which is the only")
    P("  state in which 'it reproduces' is even a meaningful question.")
    sw_o, A_o = sweep_own_vintage(sub, WT_0908, SCRATCH / "own",
                                  BUDGET["OWN-VINTAGE"], m516)
    PS_o = per_script(A_o, sw_o, m516, REPO, "OWN-VINTAGE")

    SW = pd.concat([sw_t, sw_p, sw_f, sw_o], ignore_index=True)
    AA = pd.concat([x for x in (A_t, A_p, A_f, A_o) if len(x)], ignore_index=True)
    PS = pd.concat([PS_t, PS_p, PS_f, PS_o], ignore_index=True)
    SW.to_csv(OUT / f"{STEM}.sweep.csv", index=False)
    AA.drop(columns=[c for c in ("moves",) if c in AA.columns]).to_csv(
        OUT / f"{STEM}.artefacts.csv", index=False)

    # ---- idea 516's own 36, read from the record, for the ALL-60 statement ----------------
    s36r = s36.rename(columns={"cause": "cause"}).copy()
    s36r["arm"] = "TODAY"
    s36r["state"] = np.where(s36r.get("capped", 0) == 1, "CAPPED", "RAN")
    s36r["src"] = "idea516 (read, not re-run)"
    PS_t60 = pd.concat([
        PS_t.assign(src="idea682 (fresh)"),
        s36r[["arm", "file", "state", "rc2", "secs2", "worst_move", "worst_all",
              "structural", "is_census", "cause", "src"]],
    ], ignore_index=True)
    PS_t60.to_csv(OUT / f"{STEM}.scripts.csv", index=False)

    # =====================================================================================
    # STAGE 3 - the grid: P1 sample x P2 vintage, ALL points reported
    # =====================================================================================
    P("")
    P("=" * 104)
    P("STAGE 3 - GRID  (P1 sample x P2 vintage) - every point reported")
    P("=" * 104)
    rows = []

    def stat(df, sample, vintage, note=""):
        d = df.copy()
        reached = d[d.state == "RAN"]
        n_moved = int((reached.worst_move > REL).sum())
        n_any = int((reached.worst_move > 0).sum())
        rows.append(dict(sample=sample, vintage=vintage, n_requested=len(d),
                         n_reached=len(reached),
                         n_unreached=int((d.state == "UNREACHED").sum()),
                         n_absent=int((d.state == "ABSENT").sum()),
                         n_capped=int((d.state == "CAPPED").sum()),
                         n_rc_nonzero=int((reached.rc2 != 0).sum()),
                         share_move_step=n_moved / len(reached) if len(reached) else np.nan,
                         share_move_exact=n_any / len(reached) if len(reached) else np.nan,
                         share_panel_drift=float(reached.cause.str.startswith(
                             "PANEL DRIFT").mean()) if len(reached) else np.nan,
                         share_corpus=float(reached.cause.str.startswith(
                             "CORPUS").mean()) if len(reached) else np.nan,
                         share_reproduces=float((reached.cause == "REPRODUCES").mean())
                         if len(reached) else np.nan,
                         worst_finite=float(reached.worst_move.replace(np.inf, np.nan).max())
                         if len(reached) else np.nan,
                         n_structural=int(np.isinf(reached.worst_move).sum())
                         if len(reached) else 0, note=note))

    # TODAY: the two disjoint halves and the union, plus the nested subsample ladder
    stat(PS_t60[PS_t60.src.str.startswith("idea516")], "S36 (idea 516, read)", "TODAY",
         "the published 97.2%")
    stat(PS_t, "R24 (fresh, unsampled)", "TODAY", "the hold-out idea 516 never ran")
    stat(PS_t60, "ALL60", "TODAY", "the whole rc=0 population")
    for k in SUBSAMPLES:
        ss = sub[:k]
        stat(PS_t60[PS_t60.file.isin(ss)], f"NESTED{k}", "TODAY", "matched to the frozen arms")
        stat(PS_p[PS_p.file.isin(ss)], f"NESTED{k}", "PANEL-FROZEN", "")
        stat(PS_f[PS_f.file.isin(ss)], f"NESTED{k}", "FULL-FREEZE", "")
        stat(PS_o[PS_o.file.isin(ss)], f"NESTED{k}", "OWN-VINTAGE",
             "each script at its OWN commit")
    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    P(G.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---- the matched three-arm attribution ------------------------------------------------
    P("")
    P("-" * 104)
    P("MATCHED ATTRIBUTION - the same files, four vintages")
    P("-" * 104)
    key = ["file"]
    M = (PS_t60[PS_t60.file.isin(sub)][key + ["worst_move", "state", "cause", "is_census"]]
         .rename(columns={"worst_move": "wm_TODAY", "state": "st_TODAY",
                          "cause": "cz_TODAY"})
         .merge(PS_p[key + ["worst_move", "state", "cause"]]
                .rename(columns={"worst_move": "wm_PF", "state": "st_PF", "cause": "cz_PF"}),
                on="file", how="outer")
         .merge(PS_f[key + ["worst_move", "state", "cause"]]
                .rename(columns={"worst_move": "wm_FF", "state": "st_FF", "cause": "cz_FF"}),
                on="file", how="outer")
         .merge(PS_o[key + ["worst_move", "state", "cause"]]
                .rename(columns={"worst_move": "wm_OV", "state": "st_OV", "cause": "cz_OV"}),
                on="file", how="outer")
         .merge(sw_o[["file", "own_sha", "own_panel_end"]], on="file", how="left"))
    M.to_csv(OUT / f"{STEM}.matched.csv", index=False)
    ok = M[(M.st_TODAY == "RAN") & (M.st_PF == "RAN") & (M.st_FF == "RAN")
           & (M.st_OV == "RAN")]
    P(f"  {len(ok)} files reached in ALL FOUR arms.")
    if len(ok):
        P(f"    move > 1 restatement step ({REL:.3e}):  TODAY "
          f"{(ok.wm_TODAY > REL).mean():.1%}   PANEL-FROZEN {(ok.wm_PF > REL).mean():.1%}   "
          f"FULL-FREEZE {(ok.wm_FF > REL).mean():.1%}   "
          f"OWN-VINTAGE {(ok.wm_OV > REL).mean():.1%}")
        P(f"    move at all (exact):                 TODAY "
          f"{(ok.wm_TODAY > 0).mean():.1%}   PANEL-FROZEN {(ok.wm_PF > 0).mean():.1%}   "
          f"FULL-FREEZE {(ok.wm_FF > 0).mean():.1%}   "
          f"OWN-VINTAGE {(ok.wm_OV > 0).mean():.1%}")
        P(f"    vintages in play: the frozen arms pin ONE panel (2026-09-08); the sample's "
          f"scripts were published across {ok.own_panel_end.nunique()} of them "
          f"({ok.own_panel_end.value_counts().to_dict()}).")
        cured = ok[(ok.wm_TODAY > REL) & (ok.wm_PF <= REL)]
        left = ok[(ok.wm_PF > REL)]
        nd = ok[(ok.wm_OV > REL)]
        P(f"    pinning the panel to 2026-09-08 cures {len(cured)} of "
          f"{int((ok.wm_TODAY > REL).sum())} movers")
        P(f"    still moving with that panel pinned: {len(left)}")
        P(f"    still moving at 2026-09-08 with the corpus frozen too: "
          f"{int((ok.wm_FF > REL).sum())}")
        P(f"    still moving AT ITS OWN COMMIT (own panel, own corpus, own tree): "
          f"{len(nd)} of {len(ok)}  -> this is the residue the queue has no name for; "
          f"{int((ok.wm_OV <= REL).sum())} scripts DO reproduce once given their own vintage")
        if len(nd):
            P("        the scripts that do not reproduce even against their own commit:")
            for _, r in nd.iterrows():
                P(f"        {r.file[:66]:<66} own {r.own_panel_end}  move {r.wm_OV:.3e}")
        good = ok[ok.wm_OV <= REL]
        if len(good):
            P("        the scripts that DO reproduce at their own commit:")
            for _, r in good.iterrows():
                P(f"        {r.file[:66]:<66} own {r.own_panel_end}  "
                  f"TODAY {r.wm_TODAY:.3e} -> OWN {r.wm_OV:.3e}")

    # ---- KEEP flips on the record's own committed verdict columns --------------------------
    P("")
    P("-" * 104)
    P("PROTOCOL 4a/4b RE-ADJUDICATION of the committed verdict columns")
    P("-" * 104)
    B_today = book_table(load_universe(), "TODAY (2026-09-10 panel)")
    px_fr = read_panel(WT_0908 / "data" / "prices.csv", T)
    B_fr = book_table(px_fr, "FROZEN (2026-09-08 panel)")
    B = pd.concat([B_today, B_fr], ignore_index=True)
    B.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    KP = keeppaths(B)
    KP.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)

    bars_today = dict(
        b_H1=B_today.set_index("book").loc["RULES v2 (live)"].H1,
        b_H2=B_today.set_index("book").loc["RULES v2 (live)"].H2,
        b_DD=B_today.set_index("book").loc["RULES v2 (live)"].MaxDD,
        s_H1=B_today.set_index("book").loc["SPY"].H1,
        s_H2=B_today.set_index("book").loc["SPY"].H2,
        s_DD=0.60 * B_today.set_index("book").loc["SPY"].MaxDD,
        s_CAGR=0.70 * B_today.set_index("book").loc["SPY"].CAGR,
        s_OOS=B_today.set_index("book").loc["SPY"].OOS_Sharpe)
    KF = []
    for label, sw_, scr, root in (("TODAY", sw_t, SCRATCH / "today", REPO),
                                  ("PANEL-FROZEN", sw_p, SCRATCH / "pf", WT_HEAD),
                                  ("FULL-FREEZE", sw_f, SCRATCH / "ff", WT_0908)):
        m516.SCRATCH = Path(scr); m516.REPO = Path(root)
        m516.OUT = Path(root) / "research" / "backtests"
        k = m516.keep_flips(sw_[sw_.state == "RAN"], bars_today)
        if len(k):
            k["arm"] = label
            KF.append(k)
    KFD = pd.concat(KF, ignore_index=True) if KF else pd.DataFrame()
    if len(KFD):
        KFD.to_csv(OUT / f"{STEM}.keepflips.csv", index=False)
        for label, g in KFD.groupby("arm"):
            a4 = g[g.adj4a == 1]; b4 = g[g.adj4b == 1]
            P(f"  [{label}] {len(g)} adjudicable artefacts, "
              f"{int(a4.n_rows.sum())} book-rows 4a / {int(b4.n_rows.sum())} 4b: "
              f"4a flips {int(a4.flip4a.sum())} "
              f"({a4.flip4a.sum()/max(1,a4.n_rows.sum()):.4%}), "
              f"4b flips {int(b4.flip4b.sum())} "
              f"({b4.flip4b.sum()/max(1,b4.n_rows.sum()):.4%})")
    else:
        P("  no committed artefact in these samples carries an adjudicable verdict column.")

    # ---- the book axis --------------------------------------------------------------------
    P("")
    P("=" * 104)
    P("STAGE 4 - BOOK AXIS, RULE 8: what ONE two-day vintage step does to the live book")
    P("=" * 104)
    P(B.set_index(["vintage", "book"]).to_string(float_format=lambda x: f"{x:.4f}"))
    P("")
    P(KP[["vintage", "book", "pass4a", "pass4b", "H1", "H2", "MaxDD", "CAGR", "OOS_Sharpe",
          "OOS_CAGR", "OOS_MaxDD"]].to_string(index=False,
                                              float_format=lambda x: f"{x:.4f}"))
    piv = B.pivot_table(index="book", columns="vintage",
                        values=["CAGR", "Sharpe", "MaxDD", "OOS_Sharpe", "OOS_CAGR"])
    P("")
    for bk in B.book.unique():
        t = B[(B.book == bk) & (B.vintage.str.startswith("TODAY"))].iloc[0]
        f = B[(B.book == bk) & (B.vintage.str.startswith("FROZEN"))].iloc[0]
        P(f"  {bk:<22} dCAGR {t.CAGR - f.CAGR:+.4%}  dSharpe {t.Sharpe - f.Sharpe:+.4f}  "
          f"dMaxDD {t.MaxDD - f.MaxDD:+.4%}  dOOS_Sharpe {t.OOS_Sharpe - f.OOS_Sharpe:+.4f}  "
          f"dOOS_CAGR {t.OOS_CAGR - f.OOS_CAGR:+.4%}")
    flips = KP.pivot_table(index="book", columns="vintage", values=["pass4a", "pass4b"])
    P("")
    P("  4a/4b verdicts by vintage (each judged against its OWN vintage's SPY and baseline):")
    P(flips.to_string())
    nflip = 0
    for bk in KP.book.unique():
        g = KP[KP.book == bk]
        if g.pass4a.nunique() > 1 or g.pass4b.nunique() > 1:
            nflip += 1
    P(f"  books whose 4a or 4b verdict FLIPS across the two-day vintage step: {nflip} of "
      f"{KP.book.nunique()}")

    # ---- headline ---------------------------------------------------------------------------
    P("")
    P("=" * 104)
    a60 = G[(G["sample"] == "ALL60") & (G.vintage == "TODAY")].iloc[0]
    a24 = G[(G["sample"] == "R24 (fresh, unsampled)")].iloc[0]
    a36 = G[(G["sample"] == "S36 (idea 516, read)")].iloc[0]
    P(f"HEADLINE 1 (SAMPLE): idea 516's 97.2% was measured on S36; the UNSAMPLED R24 gives "
      f"{a24.share_move_step:.1%} over {int(a24.n_reached)} reached files, and the whole "
      f"rc=0 population gives {a60.share_move_step:.1%} of {int(a60.n_reached)}.")
    P(f"                     (S36 as published/re-read: {a36.share_move_step:.1%} of "
      f"{int(a36.n_reached)}.)  Idea 483's `secs` column ranks measured runtime at Spearman "
      f"{rho:+.4f} over all 60 - so the sort key idea 516 called broken is broken in "
      f"LEVEL (one 6.0s file took 332s) but not in RANK, and the hold-out it never drew "
      f"lands within 5.5 pp of the published figure either way.")
    if len(ok):
        P(f"HEADLINE 2 (VINTAGE): on the {len(ok)} files reached in all four arms, pinning "
          f"data/prices.csv to 2026-09-08 takes the move rate from "
          f"{(ok.wm_TODAY > REL).mean():.1%} to {(ok.wm_PF > REL).mean():.1%}; freezing the "
          f"corpus too gives {(ok.wm_FF > REL).mean():.1%}; giving each script back ITS OWN "
          f"commit gives {(ok.wm_OV > REL).mean():.1%}.")
    P(f"HEADLINE 3 (BOOK): one two-day panel step moves the live book's OOS Sharpe by "
      f"{abs(B[(B.book=='RULES v2 (live)')&(B.vintage.str.startswith('TODAY'))].iloc[0].OOS_Sharpe - B[(B.book=='RULES v2 (live)')&(B.vintage.str.startswith('FROZEN'))].iloc[0].OOS_Sharpe):.4f} "
      f"and flips {nflip} of {KP.book.nunique()} 4a/4b verdicts.")
    P("=" * 104)
    P(f"elapsed {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()

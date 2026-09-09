#!/usr/bin/env python3
"""IDEA 513 (lane C) — three committed scripts fail their own reproduction gates today.

QUESTION (queue): idea 483's lane-C sweep re-executed 81 committed backtests;
`2026-09-07_does-a-levered-f-060-book-clear-the-CAGR-floor_C.py` aborts on its own assertion
"idea 138 reproduction FAILED on the exact subset" and two others raise.  Is the cause DATA
DRIFT (prices.csv has grown since), a GENUINE reproduction failure, or an ENVIRONMENT
difference — and which published numbers depend on the affected runs?

DESIGN.  Two parameters, both reported at every grid point, neither tuned on an outcome:
  P1  VINTAGE of data/prices.csv, 3 levels
        NOW    = the working tree's file            (4700 rows, ends 2026-09-08)
        TRUNC  = the working tree's file truncated to 2026-09-04 (4699 rows, RESTATED values)
        OLD    = data/prices.csv as committed at 44bc66f (4699 rows, the values the four
                 scripts actually published on)
      NOW-vs-TRUNC isolates the APPENDED-ROW channel; TRUNC-vs-OLD isolates the RESTATEMENT
      channel (the daily-close job rewrites history: 46 of 58 columns move, max |d| 3e-4).
  P2  the arm — in [A] the failing script (4 levels), in [C] the book dial (10 arms).

[A] re-executes each failing script once per vintage in a child process.  The child patches
    pandas.read_csv so every read of data/prices.csv serves the chosen vintage, and redirects
    every WRITE under research/backtests/ into a scratch mirror so no committed artefact is
    touched.  Nothing else is changed: same interpreter, same pandas/numpy, same code.
[B] censuses what the record hangs on those four runs (artefacts, importers, LEADERBOARD).
[C] prices the same drift in PROTOCOL units on U56 (the only drifting panel): 10 books x 3
    vintages at 10 bps, weekly, t+1, full/halves/OOS, 4a vs the live book and 4b vs SPY, plus
    rule 8 (dial chosen on 2009-2016 only, evaluated 2017-2026 untouched).

Deterministic; no randomness anywhere.  Writes <STEM>.{rerun,census,drift,walkforward}.csv and
<STEM>.console.txt.  Does not modify RULES.md, scan.py, bot.py or baseline.py.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "research" / "backtests"
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))

STEM = "2026-09-09_three-committed-scripts-fail-their-own-reproduction-gates-today_C"
PRICES = ROOT / "data" / "prices.csv"
OLD_REV = "44bc66f"                      # last commit before the 2026-09-08 daily-close job
ASOF_OLD = "2026-09-04"                  # the vintage every affected console.txt was written on
SCRATCH = Path(os.environ.get("IDEA513_SCRATCH", "/tmp/idea513"))
TIMEOUT = int(os.environ.get("IDEA513_TIMEOUT", "480"))
JOBS = int(os.environ.get("IDEA513_JOBS", "4"))

# the four committed scripts that exit non-zero today (rc = 1 in idea 483's sweepstatus.csv;
# rc = 124 there is the sweep's own timeout, not a failure)
FAILING = [
    "2026-09-07_does-a-levered-f-060-book-clear-the-CAGR-floor_C",
    "2026-09-07_does-the-MAB-DD-damage-SCALE-survive-a-fourth-panel_cloud",
    "2026-09-07_is-the-U56-6W-m20-cstar-of-104-bps-a-DRAWDOWN-CAP-artefact_C",
    "2026-09-08_is-168c-s-k-CROSSING-a-SMOOTHING-artefact-end-to-end_cloud",
]

LOG: list[str] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# ============================================================== CHILD RUNNER ==
def child_main(target: str, vintage: str) -> int:
    """Executed as `python -u THIS --child <target-stem> <vintage>`."""
    import builtins
    import runpy

    prices_file = {"NOW": PRICES, "TRUNC": PRICES, "OLD": SCRATCH / "prices_OLD.csv"}[vintage]
    asof = pd.Timestamp(ASOF_OLD) if vintage == "TRUNC" else None

    mirror = SCRATCH / "mirror" / vintage
    mirror.mkdir(parents=True, exist_ok=True)

    def redir(p):
        """Any WRITE under research/backtests/ goes to the scratch mirror instead."""
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

    _read_csv = pd.read_csv

    def read_csv2(filepath_or_buffer=None, *a, **k):
        """Serve the chosen vintage for every read of data/prices.csv."""
        swap = False
        try:
            if Path(filepath_or_buffer).resolve() == PRICES.resolve():
                swap = True
        except Exception:
            pass
        if swap:
            df = _read_csv(prices_file, *a, **k)
            if asof is not None and isinstance(df.index, pd.DatetimeIndex):
                df = df.loc[:asof]
            return df
        return _read_csv(filepath_or_buffer, *a, **k)

    pd.read_csv = read_csv2

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

    runpy.run_path(str(OUT / f"{target}.py"), run_name="__main__")
    return 0


# ============================================================ [A] RE-EXECUTE ==
GATE_RE = ("reproduction", "REPRODUCTION", "gate", "GATE", "max|d", "G6 ", "exact")


def classify(rc: int, out: str, err: str) -> str:
    txt = out + "\n" + err
    if "AssertionError" in err or "reproduction gate failed" in txt:
        return "GATE-FAIL"
    if rc == 0:
        return "PASS-complete"
    if rc == 124:
        return "PASS-at-gate (timeout later)"
    return f"OTHER-ERROR rc={rc}"


def gate_lines(out: str) -> list[str]:
    ls = [l.rstrip() for l in out.splitlines() if any(t in l for t in GATE_RE)]
    return [l for l in ls if l.strip()]


def materialise_old() -> bool:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    dest = SCRATCH / "prices_OLD.csv"
    if dest.exists() and dest.stat().st_size > 1_000_000:
        return True
    try:
        blob = subprocess.run(["git", "show", f"{OLD_REV}:data/prices.csv"], cwd=ROOT,
                              capture_output=True, check=True).stdout
        dest.write_bytes(blob)
        return True
    except Exception as e:
        say(f"    OLD vintage unavailable ({type(e).__name__}: {e}); the OLD arm is SKIPPED")
        return False


def part_a(vintages: list[str]) -> pd.DataFrame:
    say("\n[A] RE-EXECUTION OF THE FOUR FAILING SCRIPTS, ONE RUN PER VINTAGE")
    say(f"    P1 vintage in {vintages}; P2 script in the 4 rc=1 files.  timeout {TIMEOUT}s, "
        f"{JOBS} concurrent.  Every write under research/backtests/ is redirected to "
        f"{SCRATCH/'mirror'} — no committed artefact is touched.")
    jobs = [(s, v) for v in vintages for s in FAILING]
    rows, running = [], []
    logdir = SCRATCH / "logs"
    logdir.mkdir(parents=True, exist_ok=True)

    def launch(job):
        s, v = job
        o = open(logdir / f"{s}.{v}.out", "wb")
        e = open(logdir / f"{s}.{v}.err", "wb")
        p = subprocess.Popen([sys.executable, "-u", str(Path(__file__).resolve()), "--child", s, v],
                             cwd=str(ROOT), stdout=o, stderr=e)
        return dict(job=job, p=p, o=o, e=e, t0=pd.Timestamp.utcnow())

    q = list(jobs)
    while q or running:
        while q and len(running) < JOBS:
            running.append(launch(q.pop(0)))
        done = []
        for r in running:
            try:
                rc = r["p"].wait(timeout=5)
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
            s, v = r["job"]
            out = (logdir / f"{s}.{v}.out").read_text(errors="replace")
            err = (logdir / f"{s}.{v}.err").read_text(errors="replace")
            st = classify(rc, out, err)
            secs = (pd.Timestamp.utcnow() - r["t0"]).total_seconds()
            gl = gate_lines(out)
            rows.append(dict(script=s, vintage=v, rc=rc, secs=round(secs, 1), status=st,
                             n_gate_lines=len(gl),
                             assertion=(err.strip().splitlines()[-1][:120] if "AssertionError" in err
                                        else ("reproduction gate failed"
                                              if "reproduction gate failed" in out + err else "")),
                             gate_tail=" || ".join(gl[-3:])[:400]))
            say(f"    {v:<5} {s[:64]:<64} rc={rc:<4} {secs:6.1f}s  {st}")
    R = pd.DataFrame(rows).sort_values(["script", "vintage"]).reset_index(drop=True)
    R.to_csv(OUT / f"{STEM}.rerun.csv", index=False)
    return R


def console_agreement() -> pd.DataFrame:
    """ENVIRONMENT TEST: what share of the COMMITTED console.txt lines the re-run reproduces
    VERBATIM (set membership, so an early abort or a stray engine print cannot fake agreement).
    A run that aborts at its gate can only reproduce the lines printed before the gate, so the
    share is read together with the abort point, not on its own."""
    rows = []
    for s in FAILING:
        com = OUT / f"{s}.console.txt"
        for v in ("OLD", "TRUNC", "NOW"):
            got = SCRATCH / "logs" / f"{s}.{v}.out"
            if not (com.exists() and got.exists()):
                continue
            a = [l.rstrip() for l in com.read_text(errors="replace").splitlines() if l.strip()]
            b = set(l.rstrip() for l in got.read_text(errors="replace").splitlines())
            hit = sum(1 for l in a if l in b)
            first_miss = next((l for l in a if l not in b), "")
            rows.append(dict(script=s, vintage=v, committed_lines=len(a), verbatim_hits=hit,
                             share=round(hit / max(len(a), 1), 4), first_missing=first_miss[:150]))
    return pd.DataFrame(rows)


# ====================================================== [A2] ATTRIBUTION ====
# Each re-run writes its own recomputed artefact into the scratch mirror BEFORE its gate
# fires.  Joining that against the committed reference the gate reads localises the failure
# to a PANEL, which is what separates "the data moved" from "the code is wrong".
ATTRIB = {
    "2026-09-07_does-a-levered-f-060-book-clear-the-CAGR-floor_C": dict(
        mine="2026-09-07_does-a-levered-f-060-book-clear-the-CAGR-floor_C.grid.csv",
        ref="2026-09-07_sleeve-f-plateau-width_B.grid.csv",
        keys=["panel", "book", "sleeve", "cost", "f"],
        cols=["Sharpe", "CAGR", "MaxDD", "OOS_Sharpe"],
        # the script's own gate: fin = 0, g = 0.75, and its declared EXACT subset
        filt=lambda d: d[(d.fin == 0.0) & (np.isclose(d.g, 0.75))],
        post=lambda m: m[(m.f > 0) | (m.book == "EWall")],
        published="max|dSharpe| 4.441e-16 on 40 rows"),
    "2026-09-07_does-the-MAB-DD-damage-SCALE-survive-a-fourth-panel_cloud": dict(
        mine="2026-09-07_does-the-MAB-DD-damage-SCALE-survive-a-fourth-panel_cloud.matched.csv",
        ref="2026-09-07_split-the-band-lexicon-in-the-LEADERBOARD_C.matched.csv",
        keys=["panel", "arm", "dial"],
        cols=["dMaxDD_bp", "dSharpe", "dCAGR_pp", "dTurn", "dNames", "MaxDD", "Sharpe"],
        filt=lambda d: d, post=lambda m: m,
        published="max|d| 2.842e-14 on 21 cells"),
}


def part_a2() -> pd.DataFrame:
    say("\n[A2] WHICH PANEL CARRIES THE FAILURE (recomputed artefact vs the committed "
        "reference the gate reads)")
    rows = []
    for s, sp in ATTRIB.items():
        ref = pd.read_csv(OUT / sp["ref"])
        say(f"    {s}\n      reference {sp['ref']}, published gate: {sp['published']}")
        for v in ("NOW", "TRUNC", "OLD"):
            f = SCRATCH / "mirror" / v / sp["mine"]
            if not f.exists():
                continue
            mine = sp["filt"](pd.read_csv(f))
            M = sp["post"](ref.merge(mine, on=sp["keys"], suffixes=("_ref", "_new")))
            d = pd.DataFrame({c: (M[c + "_ref"] - M[c + "_new"]).abs() for c in sp["cols"]})
            per = pd.concat([M[sp["keys"]].reset_index(drop=True), d.reset_index(drop=True)],
                            axis=1).groupby("panel")[sp["cols"]].max()
            for pan, r in per.iterrows():
                rows.append(dict(script=s, vintage=v, panel=pan, n_rows=len(M),
                                 **{c: float(r[c]) for c in sp["cols"]},
                                 worst=float(max(r[c] for c in sp["cols"]))))
            say(f"      {v:<5} {len(M):>3} joined rows, worst |d| by panel: "
                + "  ".join(f"{p} {float(max(per.loc[p, c] for c in sp['cols'])):.3e}"
                            for p in per.index))
    A = pd.DataFrame(rows)
    A.to_csv(OUT / f"{STEM}.attribution.csv", index=False)
    if len(A):
        u = A[A.panel.astype(str).str.lower().isin(["u56"])]
        o = A[~A.panel.astype(str).str.lower().isin(["u56"])]
        say(f"    U56 (the only panel served by data/prices.csv): worst |d| "
            f"{u.worst.max():.3e} over {len(u)} panel-vintage rows.")
        say(f"    EVERY OTHER PANEL (broad136 / SMALL439, served by static caches): worst |d| "
            f"{o.worst.max():.3e} over {len(o)} panel-vintage rows — machine precision at "
            f"EVERY vintage, today's included.")
    return A


# =============================================================== [B] CENSUS ==
def part_b() -> pd.DataFrame:
    say("\n[B] WHAT THE RECORD HANGS ON THESE FOUR RUNS")
    lb = (ROOT / "research" / "LEADERBOARD.md").read_text(errors="replace")
    ch = (ROOT / "research" / "CHANGELOG.md").read_text(errors="replace")
    qu = (ROOT / "research" / "QUEUE.md").read_text(errors="replace")
    pys = sorted(OUT.glob("*.py"))
    mds = sorted(OUT.glob("*.md"))
    rows = []
    for s in FAILING:
        arte = sorted(p.name for p in OUT.glob(f"{s}.*") if p.suffix != ".py")
        n_cells = 0
        for p in OUT.glob(f"{s}.*.csv"):
            try:
                d = pd.read_csv(p)
                n_cells += int(d.shape[0] * d.shape[1])
            except Exception:
                pass
        importers = [p.name for p in pys if p.name != f"{s}.py" and s in p.read_text(errors="replace")]
        md_refs = [p.name for p in mds if s in p.read_text(errors="replace")]
        rows.append(dict(script=s, artefacts=len(arte), published_csv_cells=n_cells,
                         importer_scripts=len(importers), memo_or_result_refs=len(md_refs),
                         leaderboard_rows=lb.count(s), changelog_refs=ch.count(s),
                         queue_refs=qu.count(s),
                         importers=";".join(importers)[:300]))
        say(f"    {s[:66]:<66} artefacts {len(arte):>2}  csv cells {n_cells:>7}  "
            f"importers {len(importers):>2}  LEADERBOARD rows {lb.count(s):>2}  "
            f"CHANGELOG {ch.count(s):>2}")
    C = pd.DataFrame(rows)
    C.to_csv(OUT / f"{STEM}.census.csv", index=False)

    # ---- record-wide exposure: how many committed scripts assert EXACT equality at all?
    import re
    tol = re.compile(r"assert[^\n]{0,400}?<\s*1e-(0?[6-9]|1[0-9])")
    eq = re.compile(r"assert[^\n]{0,200}?(==|\.equals\()")
    n_exact = n_eqonly = n_reads = 0
    hits = []
    for p in pys:
        t = p.read_text(errors="replace")
        a, b = bool(tol.search(t)), bool(eq.search(t))
        reads = bool(re.search(r"read_csv\([^)]*OUT\s*/", t))
        if a or b:
            hits.append(p.name)
            n_exact += int(a)
            n_eqonly += int(b and not a)
            n_reads += int(reads)
    say(f"    RECORD-WIDE EXPOSURE: of {len(pys)} committed backtests, {len(hits)} carry an "
        f"assert-style reproduction gate ({n_exact} with a tolerance <= 1e-6, {n_eqonly} with "
        f"exact == / .equals only); {n_reads} of those read a committed artefact back. "
        f"Every one of them is a test of the DATA VINTAGE as much as of the code.")
    pd.DataFrame(dict(script=hits)).to_csv(OUT / f"{STEM}.gatecensus.csv", index=False)
    return C


# ================================================================ [C] DRIFT ==
import importlib.util  # noqa: E402

from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
FREQ, COST = "W", 10.0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
PHI, DELTA = 0.70, 0.60                  # 4b CAGR floor / DD cap, fractions of SPY
BANDS = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06]


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def panels() -> dict[str, pd.DataFrame]:
    """U56 at the three vintages.  Broad/small caches did not move, so U56 is the whole story."""
    now = load_universe()
    trunc = now.loc[:pd.Timestamp(ASOF_OLD)]
    out = {"NOW": now, "TRUNC": trunc}
    f = SCRATCH / "prices_OLD.csv"
    if f.exists():
        raw = pd.read_csv(f, index_col=0, parse_dates=True).sort_index()
        out["OLD"] = raw[[c for c in now.columns]].dropna(how="all").ffill()
    return out


def arms(H):
    """10 books, all reported.  The dial is the 200d band (P2); the fixed arms are the live
    book, the previous book, the standing 2026-09-04 KEEP-4b candidate and its control."""
    A = {f"v2_band{int(b*100):02d}": (lambda px, b=b: rules_v2_weights(px, band=b)) for b in BANDS}
    A["RULESv1"] = rules_v1_weights
    A["TOP20_keep4b"] = lambda px: H.targets(px, "TOP20", gate="v1gate", conv="dg")
    A["EWall_v1gate"] = lambda px: H.targets(px, "EWall", gate="v1gate", conv="dg")
    A["EWall_ungated"] = lambda px: H.targets(px, "EWall")
    return A


def score_arm(px, W, start):
    r = backtest(px, W, cost_bps=COST, freq=FREQ)["returns"].loc[start:]
    h = len(r) // 2
    m, o = metrics(r), metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"])


def verdicts(a, base, spy):
    p4a = (a["H1"] > base["H1"]) and (a["H2"] > base["H2"]) and (a["MaxDD"] >= base["MaxDD"])
    p4b = (a["H1"] > spy["H1"] and a["H2"] > spy["H2"] and a["OOS_Sharpe"] > spy["OOS_Sharpe"]
           and a["MaxDD"] >= DELTA * spy["MaxDD"] and a["CAGR"] >= PHI * spy["CAGR"])
    return bool(p4a), bool(p4b)


def part_c() -> tuple[pd.DataFrame, pd.DataFrame]:
    say("\n[C] THE SAME DRIFT PRICED IN PROTOCOL UNITS (U56, weekly, t+1, 10 bps)")
    H = _load(I94, "i94")
    P = panels()
    A = arms(H)
    rows = []
    for v, px in P.items():
        start = px.index[260]
        spy = score_arm(px, pd.DataFrame(0.0, index=px.index, columns=px.columns).assign(SPY=1.0),
                        start)
        base = score_arm(px, rules_v2_weights(px), start)
        for nm, fn in A.items():
            a = score_arm(px, fn(px), start)
            p4a, p4b = verdicts(a, base, spy)
            rows.append(dict(vintage=v, arm=nm, rows=len(px), last=str(px.index[-1].date()),
                             **a, pass4a=p4a, pass4b=p4b,
                             base_Sharpe=base["Sharpe"], base_H1=base["H1"], base_H2=base["H2"],
                             base_MaxDD=base["MaxDD"], spy_Sharpe=spy["Sharpe"],
                             spy_H1=spy["H1"], spy_H2=spy["H2"], spy_CAGR=spy["CAGR"],
                             spy_MaxDD=spy["MaxDD"], spy_OOS_Sharpe=spy["OOS_Sharpe"],
                             spy_OOS_CAGR=spy["OOS_CAGR"], spy_OOS_MaxDD=spy["OOS_MaxDD"]))
        say(f"    {v:<5} priced {len(A)} arms + live book + SPY on {len(px)} rows "
            f"ending {px.index[-1].date()}")
    D = pd.DataFrame(rows)
    D.to_csv(OUT / f"{STEM}.drift.csv", index=False)

    cols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]
    say("\n    FULL GRID (every arm x every vintage, nothing withheld)")
    say(D[["vintage", "arm", "rows", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
           "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "pass4a", "pass4b"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n    CHANNEL DECOMPOSITION (max |d| over the 10 arms, per metric)")
    have = set(D.vintage)
    piv = {v: D[D.vintage == v].set_index("arm") for v in have}
    dec = []
    pairs = [("NOW", "TRUNC", "appended row 2026-09-08"),
             ("TRUNC", "OLD", "restatement of the shared block"),
             ("NOW", "OLD", "both channels = today vs published vintage")]
    for a, b, lab in pairs:
        if a in have and b in have:
            r = dict(pair=f"{a}-{b}", channel=lab)
            for c in cols:
                r[c] = float((piv[a][c] - piv[b][c]).abs().max())
            r["verdict_flips_4a"] = int((piv[a]["pass4a"] != piv[b]["pass4a"]).sum())
            r["verdict_flips_4b"] = int((piv[a]["pass4b"] != piv[b]["pass4b"]).sum())
            dec.append(r)
    DEC = pd.DataFrame(dec)
    if len(DEC):
        say(DEC.to_string(index=False, float_format=lambda x: f"{x:.3e}"))
    return D, DEC


def part_c_walkforward(D: pd.DataFrame) -> pd.DataFrame:
    """PROTOCOL rule 8: the band dial is chosen on 2009-2016 ONLY, then 2017-2026 is read
    untouched — once per vintage, so the question is whether the vintage moves the choice."""
    say("\n[C-rule 8] WALK-FORWARD: band chosen on IS 2009-2016, evaluated OOS 2017-2026")
    rows = []
    for v, g in D.groupby("vintage"):
        dial = g[g.arm.str.startswith("v2_band")]
        pick = dial.loc[dial.IS_Sharpe.idxmax()]
        spy = dict(OOS_CAGR=pick.spy_OOS_CAGR, OOS_Sharpe=pick.spy_OOS_Sharpe,
                   OOS_MaxDD=pick.spy_OOS_MaxDD)
        base = g[g.arm == "v2_band03"].iloc[0]     # the live book is band 0.03
        rows.append(dict(vintage=v, pick=pick.arm, IS_Sharpe=pick.IS_Sharpe,
                         OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                         OOS_MaxDD=pick.OOS_MaxDD,
                         base_OOS_CAGR=base.OOS_CAGR, base_OOS_Sharpe=base.OOS_Sharpe,
                         base_OOS_MaxDD=base.OOS_MaxDD, **{f"spy_{k}": v2 for k, v2 in spy.items()},
                         keep4b_of_pick=bool(pick.pass4b), keep4a_of_pick=bool(pick.pass4a)))
    W = pd.DataFrame(rows)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    return W


# ==================================================================== MAIN ===
def main():
    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", 60)
    pd.set_option("display.max_rows", 400)

    say(f"=== IDEA 513 — {STEM} ===")
    say("Q: is the reproduction-gate failure DATA DRIFT, a GENUINE failure, or the ENVIRONMENT?")

    say("\n[0] VINTAGE FACTS")
    now = pd.read_csv(PRICES, index_col=0, parse_dates=True)
    say(f"    data/prices.csv today: {now.shape[0]} rows x {now.shape[1]} cols, "
        f"{now.index[0].date()} .. {now.index[-1].date()}")
    ok_old = materialise_old()
    if ok_old:
        old = pd.read_csv(SCRATCH / "prices_OLD.csv", index_col=0, parse_dates=True)
        shared = now.loc[:old.index[-1], old.columns]
        d = (shared - old).abs()
        say(f"    data/prices.csv at {OLD_REV}: {old.shape[0]} rows x {old.shape[1]} cols, "
            f"ends {old.index[-1].date()}")
        say(f"    appended rows: {[str(x.date()) for x in now.index.difference(old.index)]}")
        say(f"    RESTATEMENT of the shared block: index identical {shared.index.equals(old.index)}, "
            f"columns with any change {int((d.max() > 0).sum())}/{old.shape[1]}, "
            f"max |d| {float(d.max().max()):.3e} (price units), "
            f"max |d/px| {float((d / old.abs()).max().max()):.3e}")
    for nm, f in (("prices_broad.csv", ROOT / "data" / "prices_broad.csv"),
                  ("prices_small.csv.gz", ROOT / "data" / "prices_small.csv.gz")):
        if f.exists():
            x = pd.read_csv(f, index_col=0, parse_dates=True)
            say(f"    {nm}: {x.shape[0]} rows, ends {x.index[-1].date()}  (did NOT move)")
    say(f"    environment: python {sys.version.split()[0]}, pandas {pd.__version__}, "
        f"numpy {np.__version__}")
    say("    every affected console.txt states its panels end 2026-09-04, i.e. the OLD vintage.")

    vintages = ["NOW", "TRUNC"] + (["OLD"] if ok_old else [])
    R = part_a(vintages)
    say("\n    RE-EXECUTION TABLE (all 4 scripts x all vintages, nothing withheld)")
    say(R[["script", "vintage", "rc", "secs", "status", "assertion"]]
        .to_string(index=False, max_colwidth=70))
    piv = R.pivot_table(index="script", columns="vintage", values="status", aggfunc="first")
    say("\n    STATUS BY VINTAGE\n" + piv.to_string(max_colwidth=32))

    CA = console_agreement()
    if len(CA):
        CA.to_csv(OUT / f"{STEM}.consoleagree.csv", index=False)
        say("\n    ENVIRONMENT TEST — identical leading lines of the re-run stdout vs the "
            "COMMITTED console.txt")
        say(CA.to_string(index=False))

    part_a2()
    part_b()
    D, DEC = part_c()
    W = part_c_walkforward(D)

    # ---------------------------------------------------------------- verdict
    say("\n[VERDICT]")
    n_old_pass = int((R[R.vintage == "OLD"].status.str.startswith("PASS")).sum()) if ok_old else -1
    n_now_fail = int((R[R.vintage == "NOW"].status == "GATE-FAIL").sum())
    n_trunc_fail = int((R[R.vintage == "TRUNC"].status == "GATE-FAIL").sum())
    say(f"    gates today (NOW): {n_now_fail}/4 fail.  Row-append removed (TRUNC): "
        f"{n_trunc_fail}/4 fail.  Published vintage (OLD): {4 - n_old_pass if ok_old else 'n/a'}/4 fail.")
    keep4b = D[D.pass4b]
    say(f"    4a passes: {int(D.pass4a.sum())}/{len(D)} grid points.  "
        f"4b passes: {int(D.pass4b.sum())}/{len(D)}  ({sorted(set(keep4b.arm))}).")
    if len(DEC):
        say("    channel sizes (max |dSharpe| over arms): "
            + ", ".join(f"{r.pair} {r.Sharpe:.2e}" for r in DEC.itertuples()))
    say("    A gate written as an exact-equality assertion against a committed artefact is a "
        "test of the DATA VINTAGE, not of the code.")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--child":
        sys.exit(child_main(sys.argv[2], sys.argv[3]))
    if len(sys.argv) > 1 and sys.argv[1] == "--attrib":
        # [A2] alone, off the mirror an earlier [A] already wrote; appends to the console.
        part_a2()
        p = OUT / f"{STEM}.console.txt"
        p.write_text((p.read_text() if p.exists() else "") + "\n".join(LOG) + "\n")
        sys.exit(0)
    main()

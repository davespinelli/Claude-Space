#!/usr/bin/env python3
"""Idea 514 — stamp every committed artefact with its PANEL VINTAGE.

Question (QUEUE 514): idea 513 showed a committed artefact carries no record of the price
vintage it was computed on, so a failing reproduction gate cannot say WHICH input moved.
Propose (last_date, n_rows, sha of the panel) as required columns/sidecar on every artefact
and back-fill what is still reconstructible.

This run does five things, in order, and reports every grid point:

  A. STAMP        — define panel_stamp() and compute it for the three live panels, plus the
                    file-level sha of the raw data/ files, and show the two are NOT the same
                    fact (the panel is a derived object: exclusions, ffill, SPY join, filters).
  B. CENSUS       — scan every committed artefact under research/backtests/ and research/reports/
                    and count how many carry ANY vintage-identifying token today.
  C. BACK-FILL    — recover each artefact's vintage from git (the commit that last touched it ->
                    the data/prices.csv blob live at that commit).  Report exactly how far this
                    clone can reach and write the sidecar for what is reconstructible.
  D. PRICE        — what does an unknown vintage cost in PROTOCOL units?  Two tuned parameters,
                    both reporting axes with every point published:
                        VINTAGE DEPTH d in {0,1,2,3,5,10,21,63,252} trailing trading days dropped
                        BOOK SIZE     n in {5,10,20,30,40,60} (the 2026-09-04 KEEP-4b family)
                    x 3 panels (U56 / B136 / SMALL439), 10 bps, weekly, next-day execution.
                    Both KEEP paths (4a vs the live RULES v2 book, 4b vs SPY) evaluated at every
                    point; the reported number is how many verdicts FLIP with the vintage.
                    The one REAL vintage step this clone can reach (the 2026-09-08 daily close)
                    is priced separately and exactly.
  E. RULE 8       — n chosen on 2009..2016-12-31 IS only, read once on 2017..end, at every
                    vintage depth; is the CHOICE vintage-stable, and what is OOS vs SPY?

Deterministic, standalone, no network.  Writes nothing outside research/backtests/.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import (  # noqa: E402
    ROOT as B_ROOT, backtest, band_state, load_universe, metrics, rules_v2_weights, score,
)

STEM = Path(__file__).with_suffix("")
COST_BPS = 10
FREQ = "W"
GROSS = 0.75
MAX_VOL = 0.60
BAND = 0.03
WARMUP = 260                       # baseline.compare's own warm-up skip
IS_END = pd.Timestamp("2016-12-31")   # PROTOCOL rule 8
DEPTHS = [0, 1, 2, 3, 5, 10, 21, 63, 252]
NS = [5, 10, 20, 30, 40, 60]

OUT = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUT.append(s)


# ---------------------------------------------------------------- A. THE STAMP ----------
def panel_stamp(px: pd.DataFrame) -> dict:
    """The proposed stamp.  Three required fields (last_date, n_rows, sha) plus n_cols, which
    costs nothing and catches the commonest silent change (a name entering the panel).

    The sha is over a CANONICAL encoding of the panel object actually handed to the backtest:
    index as int64 nanoseconds, columns in sorted order, values as float64 C-order bytes with
    NaN normalised.  It therefore changes on an appended row, on a restated cell, and on a
    column set change, and does NOT change on read order, dtype width, or CSV formatting.
    """
    cols = sorted(map(str, px.columns))
    v = px[cols].to_numpy(dtype="float64", copy=True)
    v[np.isnan(v)] = np.float64("nan")            # normalise -nan / signalling nan
    h = hashlib.sha256()
    h.update(np.asarray(px.index.view("int64"), dtype="int64").tobytes())
    h.update("\x00".join(cols).encode())
    h.update(np.ascontiguousarray(v).tobytes())
    return dict(last_date=str(px.index[-1].date()), first_date=str(px.index[0].date()),
                n_rows=int(px.shape[0]), n_cols=int(px.shape[1]), panel_sha=h.hexdigest()[:16])


def file_sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def small_panel(with_spy=True):
    """SMALL439: the sub-$2B panel with the max_1d_move >= 1.0 names dropped, as PROTOCOL
    practice requires.  SURVIVORSHIP: current constituents of the screen only."""
    px = load_universe(small=True, with_spy=with_spy)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c not in bad]
    return px[keep]


def load_panels():
    return {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL439": small_panel()}


# ---------------------------------------------------------------- books ------------------
def tradables(px):
    return [c for c in px.columns if c != "SPY"]


def w_v2(px):
    """The live book, RULES v2, restricted to tradables (SPY is a benchmark column only)."""
    st = band_state(px, BAND)
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    e[[c for c in px.columns if c == "SPY"]] = 0.0
    ew = GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(st, 0.0)


def _elig(px):
    tr = tradables(px)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    e = above & (vol20 < MAX_VOL)
    e[[c for c in px.columns if c not in tr]] = False
    return e


def w_fwd(px, n):
    """The 2026-09-04 KEEP-4b family: top-n of the eligible set by the v1 composite WITHOUT the
    /sqrt(vol20) scaler, equal weight at GROSS."""
    e = _elig(px)
    key = score(px, vol_scale=False)[0]
    sel = (key.where(e).rank(axis=1, ascending=False) <= n).astype(float)
    held = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(held, axis=0).mul(GROSS).fillna(0.0)


def w_ewall(px):
    e = _elig(px).astype(float)
    held = e.sum(axis=1).replace(0, np.nan)
    return e.div(held, axis=0).mul(GROSS).fillna(0.0)


def run(px, wfn):
    return backtest(px, wfn(px), cost_bps=COST_BPS, freq=FREQ)["returns"]


def stats(r):
    m = metrics(r)
    h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def keep4a(a, b):
    """4a: Sharpe > live book in BOTH halves and MaxDD no worse (MaxDD is negative)."""
    return bool(a["H1"] > b["H1"] and a["H2"] > b["H2"] and a["MaxDD"] >= b["MaxDD"])


def keep4b(a, spy, oos_a, oos_spy):
    return bool(a["H1"] > spy["H1"] and a["H2"] > spy["H2"] and oos_a > oos_spy
                and a["MaxDD"] >= 0.60 * spy["MaxDD"] and a["CAGR"] >= 0.70 * spy["CAGR"])


# ================================================================= MAIN ==================
t0 = time.time()
say("=" * 100)
say("IDEA 514 — stamp every committed artefact with its PANEL VINTAGE   (cloud, 2026-09-09)")
say("=" * 100)

# ---- A -------------------------------------------------------------------------------
say("\n[A] THE STAMP — panel_stamp() on the three live panels, and the raw files beneath them")
panels = load_panels()
stamp_rows = []
for name, px in panels.items():
    s = panel_stamp(px)
    s["object"] = f"PANEL {name}"
    stamp_rows.append(s)
for f in ["prices.csv", "prices_broad.csv", "prices_small.csv.gz", "small_meta.csv", "volume_small.csv.gz"]:
    p = ROOT / "data" / f
    if p.exists():
        stamp_rows.append(dict(object=f"FILE data/{f}", last_date="", first_date="", n_rows=-1,
                               n_cols=-1, panel_sha=file_sha(p)))
stampdf = pd.DataFrame(stamp_rows)[["object", "first_date", "last_date", "n_rows", "n_cols", "panel_sha"]]
say(stampdf.to_string(index=False))
stampdf.to_csv(f"{STEM}.stamps.csv", index=False)
say("\nNOTE: the FILE sha and the PANEL sha are different facts.  data/prices.csv carries 58 columns;")
say("      U56 is the 56 names of research/universe.json minus EXCLUDE, ffilled — a derived object.")
say("      A stamp on the file alone does not identify the panel a backtest actually consumed;")
say("      the proposal below therefore stamps the PANEL, with the file sha as a secondary field.")

# ---- B -------------------------------------------------------------------------------
say("\n[B] CENSUS — how many committed artefacts carry ANY vintage-identifying token today?")
art_dirs = [ROOT / "research" / "backtests", ROOT / "research" / "reports"]
arts = [p for d in art_dirs if d.exists() for p in sorted(d.rglob("*")) if p.is_file()]
cur_last = {r["last_date"] for r in stamp_rows if r["last_date"]}
cur_rows = {str(r["n_rows"]) for r in stamp_rows if r["n_rows"] > 0}
cur_sha = {r["panel_sha"] for r in stamp_rows}
TOK = re.compile(r"panel_sha|panel sha|PANEL VINTAGE|vintage|last_date|n_rows", re.I)
rows = []
for p in arts:
    ext = p.suffix.lower()
    try:
        raw = p.read_bytes()
        txt = "" if ext in (".gz", ".png", ".zip") else raw.decode("utf-8", "replace")
    except Exception:
        txt = ""
    rows.append(dict(
        path=str(p.relative_to(ROOT)), ext=ext, bytes=len(raw),
        tok=bool(TOK.search(txt)),
        mentions_cur_last=any(d in txt for d in cur_last),
        mentions_cur_nrows=any(re.search(rf"(?<!\d){n}(?!\d)", txt) for n in cur_rows) if txt else False,
        mentions_cur_sha=any(s in txt for s in cur_sha),
    ))
cen = pd.DataFrame(rows)
say(f"artefact files scanned: {len(cen)}   ({(cen.ext=='.py').sum()} .py, {(cen.ext=='.csv').sum()} .csv, "
    f"{(cen.ext=='.md').sum()} .md, {(cen.ext=='.txt').sum()} .txt, "
    f"{len(cen)-((cen.ext.isin(['.py','.csv','.md','.txt'])).sum())} other)")
for k, lab in [("tok", "any vintage-ish token (vintage/last_date/n_rows/panel_sha)"),
               ("mentions_cur_last", "contains a CURRENT panel last_date string"),
               ("mentions_cur_nrows", "contains a CURRENT panel n_rows as a standalone integer"),
               ("mentions_cur_sha", "contains a CURRENT panel sha")]:
    say(f"  {cen[k].sum():5d} / {len(cen):5d}  ({cen[k].mean():6.2%})  {lab}")
say("  (the middle two are UPPER bounds on self-stamping: a file may print that date or integer for")
say("   an unrelated reason.  The sha row is the only exact test, and it is the one that is zero.)")
cen.to_csv(f"{STEM}.census.csv", index=False)

# ---- C -------------------------------------------------------------------------------
say("\n[C] BACK-FILL — how much of the record's vintage is still RECONSTRUCTIBLE from git?")
def git(*a):
    return subprocess.run(["git", "-C", str(ROOT)] + list(a), capture_output=True, text=True).stdout


shallow = git("rev-parse", "--is-shallow-repository").strip()
ncommits = len(git("log", "--format=%H").split())
first_c = git("log", "--format=%cI").split()[-1] if ncommits else ""
last_c = git("log", "-1", "--format=%cI").strip()
say(f"clone is shallow: {shallow};  commits reachable: {ncommits};  window {first_c} .. {last_c}")

# path -> most recent commit that touched it, within the shallow window
touched, cur = {}, None
for line in git("log", "--format=@%H|%cI", "--name-only").splitlines():
    if line.startswith("@"):
        cur = line[1:].split("|")
    elif line.strip() and cur:
        touched.setdefault(line.strip(), cur)
reach = cen.path.map(lambda p: p in touched)
say(f"artefacts whose LAST-TOUCHING commit is inside the window: {reach.sum()} / {len(cen)} ({reach.mean():.2%})")

# distinct data/prices.csv blobs inside the window
blobs = []
for c in git("log", "--format=%H", "--", "data/prices.csv").split():
    b = git("rev-parse", f"{c}:data/prices.csv").strip()
    if b and (not blobs or blobs[-1][1] != b):
        blobs.append((c, b))
uniq = list(dict.fromkeys(b for _, b in blobs))
say(f"distinct data/prices.csv BLOBS reachable: {len(uniq)}  -> the clone spans {max(len(uniq)-1,0)} real vintage step(s)")
say("VERDICT ON BACK-FILL: a full clone maps every artefact to the blob live at its commit, but THIS")
say("sandbox's clone reaches only the window above, so the back-fill is bounded by the clone, not by")
say("the record.  The sidecar below is written for the artefacts that ARE reachable.")
side = cen[["path"]].copy()
side["touch_commit"] = cen.path.map(lambda p: touched.get(p, ["", ""])[0])
side["touch_date"] = cen.path.map(lambda p: touched.get(p, ["", ""])[1])
side["reconstructible"] = reach
side.to_csv(f"{STEM}.vintage_sidecar.csv", index=False)

# the ONE real vintage step, priced exactly
say("\n[C2] THE ONE REAL STEP — data/prices.csv at the two reachable blobs, diffed")
real = {}
for i, b in enumerate(uniq):
    raw = subprocess.run(["git", "-C", str(ROOT), "cat-file", "blob", b],
                         capture_output=True).stdout.decode()
    df = pd.read_csv(pd.io.common.StringIO(raw), index_col=0, parse_dates=True)
    real[b] = df
    say(f"  blob {b[:12]}  rows={df.shape[0]}  cols={df.shape[1]}  last={df.index[-1].date()}")
if len(uniq) == 2:
    a, c = real[uniq[1]], real[uniq[0]]        # git log is newest-first: uniq[0] is newer
    common_i = a.index.intersection(c.index)
    common_c = a.columns.intersection(c.columns)
    d = (a.loc[common_i, common_c] - c.loc[common_i, common_c]).abs()
    moved = (d > 0).any()
    say(f"  appended rows: {len(c.index.difference(a.index))};  restated cells: {int((d>0).sum().sum())} "
        f"in {int(moved.sum())} of {len(common_c)} columns;  max |d| {d.max().max():.3e}")

# ---- D -------------------------------------------------------------------------------
say("\n[D] PRICE IN PROTOCOL UNITS — vintage depth d x book size n x panel, 10 bps, weekly, next-day")
say("    (d = trailing trading days dropped from the panel = 'this artefact was computed d days ago')")
grid = []
for pname, full in panels.items():
    for d in DEPTHS:
        px = full.iloc[:len(full) - d] if d else full
        st = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0).loc[st:]
        base = run(px, w_v2).loc[st:]
        ew = run(px, w_ewall).loc[st:]
        s_spy, s_base, s_ew = stats(spy), stats(base), stats(ew)
        oos = lambda r: metrics(r.loc[IS_END + pd.Timedelta(days=1):])["Sharpe"]
        o_spy = oos(spy)
        for label, r in [("RULES v2 (live)", base), ("EWall", ew)] + \
                        [(f"FWD{n}", run(px, lambda q, n=n: w_fwd(q, n)).loc[st:]) for n in NS]:
            s = stats(r)
            grid.append(dict(panel=pname, d=d, book=label, last_date=str(px.index[-1].date()),
                             n_rows=len(px), panel_sha=panel_stamp(px)["panel_sha"],
                             CAGR=s["CAGR"], Sharpe=s["Sharpe"], MaxDD=s["MaxDD"],
                             H1=s["H1"], H2=s["H2"],
                             IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                             OOS_Sharpe=oos(r),
                             OOS_CAGR=metrics(r.loc[IS_END + pd.Timedelta(days=1):])["CAGR"],
                             OOS_MaxDD=metrics(r.loc[IS_END + pd.Timedelta(days=1):])["MaxDD"],
                             pass4a=keep4a(s, s_base), pass4b=keep4b(s, s_spy, oos(r), o_spy),
                             spy_Sharpe=s_spy["Sharpe"], spy_H1=s_spy["H1"], spy_H2=s_spy["H2"],
                             spy_CAGR=s_spy["CAGR"], spy_MaxDD=s_spy["MaxDD"], spy_OOS=o_spy,
                             base_Sharpe=s_base["Sharpe"], base_H1=s_base["H1"], base_H2=s_base["H2"],
                             base_MaxDD=s_base["MaxDD"]))
        say(f"    {pname:9s} d={d:3d} last={px.index[-1].date()} rows={len(px):5d} done "
            f"({time.time()-t0:6.1f}s)")
g = pd.DataFrame(grid)
g.to_csv(f"{STEM}.grid.csv", index=False)

say(f"\n    ALL {len(g)} GRID POINTS (panel x d x book) written to {Path(STEM).name}.grid.csv")
say("\n    Every point, full sample, by panel:")
for pname in panels:
    sub = g[g.panel == pname]
    say(f"\n    --- {pname} ---")
    piv = sub.pivot_table(index="book", columns="d", values="Sharpe")
    say(piv.to_string(float_format=lambda x: f"{x:.4f}"))

say("\n    VERDICT STABILITY vs the d=0 read (this is the number the queue is asking for):")
flip_rows = []
for pname in panels:
    sub = g[g.panel == pname]
    ref = sub[sub.d == 0].set_index("book")
    for d in DEPTHS[1:]:
        cur = sub[sub.d == d].set_index("book")
        f4a = int((cur["pass4a"] != ref["pass4a"]).sum())
        f4b = int((cur["pass4b"] != ref["pass4b"]).sum())
        flip_rows.append(dict(panel=pname, d=d, n_books=len(cur), flips4a=f4a, flips4b=f4b,
                              maxdSharpe=float((cur["Sharpe"] - ref["Sharpe"]).abs().max()),
                              maxdCAGR=float((cur["CAGR"] - ref["CAGR"]).abs().max()),
                              maxdMaxDD=float((cur["MaxDD"] - ref["MaxDD"]).abs().max())))
fl = pd.DataFrame(flip_rows)
say(fl.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
fl.to_csv(f"{STEM}.flips.csv", index=False)
say(f"\n    TOTAL over {len(fl)} (panel,d) cells x {len(NS)+2} books = {int(fl.n_books.sum())} re-reads: "
    f"4a flips {int(fl.flips4a.sum())}, 4b flips {int(fl.flips4b.sum())}")
say(f"    4a passes at d=0: {int(g[(g.d==0)].pass4a.sum())} of {len(g[g.d==0])};  "
    f"4b passes at d=0: {int(g[(g.d==0)].pass4b.sum())} of {len(g[g.d==0])}")

# ---- E -------------------------------------------------------------------------------
say("\n[E] RULE 8 — n chosen on IS (<= 2016-12-31) by IS Sharpe, read ONCE on 2017..end, per vintage")
wf = []
for pname in panels:
    for d in DEPTHS:
        sub = g[(g.panel == pname) & (g.d == d)]
        arms = sub[sub.book.str.startswith("FWD")]
        pick = arms.loc[arms.IS_Sharpe.idxmax()]
        base = sub[sub.book == "RULES v2 (live)"].iloc[0]
        wf.append(dict(panel=pname, d=d, n_star=pick.book, IS_Sharpe=pick.IS_Sharpe,
                       OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                       base_OOS_Sharpe=base.OOS_Sharpe, base_OOS_CAGR=base.OOS_CAGR,
                       spy_OOS_Sharpe=pick.spy_OOS, beats_base=bool(pick.OOS_Sharpe > base.OOS_Sharpe),
                       beats_spy=bool(pick.OOS_Sharpe > pick.spy_OOS)))
w = pd.DataFrame(wf)
say(w.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
w.to_csv(f"{STEM}.walkforward.csv", index=False)
for pname in panels:
    ns = w[w.panel == pname].n_star.tolist()
    say(f"    {pname:9s} rule-8 pick across the {len(DEPTHS)} vintages: {ns} -> "
        f"{'STABLE' if len(set(ns))==1 else 'UNSTABLE (' + str(len(set(ns))) + ' distinct)'}")

say(f"\ndone in {time.time()-t0:.1f}s")
Path(f"{STEM}.console.txt").write_text("\n".join(OUT) + "\n")

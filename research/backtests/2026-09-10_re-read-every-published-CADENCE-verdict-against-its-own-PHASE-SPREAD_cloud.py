#!/usr/bin/env python3
"""Idea 619 — re-read every published CADENCE verdict against its own PHASE SPREAD  (cloud, 2026-09-10)

QUEUE 619: "idea 412 measured the Sharpe spread of one cadence arm across rebalance offsets at
mean SD 0.0117 (k=5) / 0.0176 (k=21) / 0.0461 (k=63) and max range 0.3796, i.e. larger than most
cadence effects the record reports.  Census the record's committed cadence claims and report how
many have an effect size below their own phase spread.  Max 2 params (claim set, phase count)."

WHAT IS BEING TESTED, AND HOW THIS DIFFERS FROM ITS PARENT
  Idea 220 (2026-09-06, `back-fill-the-phase-spread-over-every-cadence-claim`) audited 240
  pairwise claims from the FOUR corpora whose grid CSV it could re-run, and re-priced them by
  re-running those parents.  This run asks the queue's question of the WHOLE COMMITTED RECORD as
  it stands on 2026-09-10 (2,794 CSVs, 4,526 files under research/backtests) and does not re-run
  the parents: it extracts each file's OWN published cadence gap and compares it to a phase
  spread measured HERE, on this run's own pre-registered grid.  That substitution is the method's
  main limitation and it is stated in the output rather than buried (see LIMITATION below).

  H1 (census)     How many committed cadence claims are there, and how many carry a phase/offset
                  column of their own — i.e. how many are self-auditing?
  H2 (the queue's question)  For each claim, is |published gap| below its own phase spread?
                  Pre-registered rule, fixed before any number was read:
                     BAND_UNION = rng(A) + rng(B)   (a phase chooser may push A up and B down)
                     BAND_MAX   = max(rng(A), rng(B))            (the conservative reading)
                  A claim is PHASE-FRAGILE at a band if |gap| < band.  Both bands reported.
  H3 (rule 8)     Does a cadence chosen on 2009-2016 at ONE phase (what the record does) beat the
                  weekly incumbent out of sample once the phase is priced?  Four choosers,
                  2017-2026 read exactly once.

AXES (PROTOCOL rule 4: no more than 2 tuned parameters — the queue names them)
  P1 CLAIM SET   census strictness in {STRICT, MED, LOOSE}, all three reported.
                 STRICT = a committed CSV with a cadence-NAMED column whose values are a cadence
                          vocabulary, plus a metric column.
                 MED    = STRICT plus files where any column's VALUES are a cadence vocabulary
                          regardless of its name.
                 LOOSE  = MED plus LEADERBOARD.md table lines that quote a cadence pair and a
                          numeric gap.
  P2 PHASE COUNT n_phase in {2, 3, 5}, all three reported; the band is a MONOTONE function of it
                 (more phases can only widen a measured range), so the fragile share is reported
                 at every rung and the headline uses n_phase = 5, idea 412's own count.
  Panels (u56 / broad136 / small439), books (TOP20 / EWALL / RULESv2), metric (Sharpe / CAGR /
  MaxDD / OOS Sharpe) and cost rung (0 / 10 / 25 bps) are REPORTED axes, never selected on.
  The only selection anywhere is PROTOCOL rule 8.

GATES (run before any new number is read)
  G1  the vectorised runner vs `engine.backtest` at D/W/M/Q on all three panels, returns AND
      turnover.
  G2  the cost-rung identity r(c) = r(0) - turnover*c/1e4 vs a live 25 bps `engine.backtest`.
  G3  the k-day cadence nests the calendar one: k=1, phase 0 == freq 'D'; and the calendar
      offset 0 schedule == `engine.rebalance_mask`.
  G4  idea 412's committed `.phase.csv` rebuilt from source at its own raw vintage.  Bar stated
      in advance: broad and small must reproduce to < 1e-9 (their caches are written weekly and
      are untouched); u56 is REPORTED, not barred, because `data/prices.csv` is rewritten daily
      and now carries a trading day idea 412 could not see (ideas 328/514's panel-stamp lesson).

LIMITATION, STATED UP FRONT
  A published claim's phase spread is a property of ITS book on ITS panel.  Re-running 160 files'
  books is not possible inside one run, so the band a claim is judged against is measured on this
  run's own 9 (panel x book) cells and matched to the claim by cadence pair, metric, and panel
  where the file names one.  The band is therefore a REFERENCE band, not the claim's own.  To
  keep that honest the full per-cell distribution is published (`.bands.csv`) and every headline
  share is reported at the 25th / 50th / 75th percentile of the band distribution, not at a
  single number.

CAVEATS CARRIED
  * SURVIVORSHIP (idea 54): current constituents on all three panels; SMALL439 drops the 44
    tickers with max_1d_move >= 1.0 from data/small_meta.csv before anything runs.  No level here
    is an attainable return; the paired comparisons that carry the conclusion are within-panel.
  * Idea 38: data/prices*.csv are calendar-day indexed after 2014-09-17, so a 1-bar offset on the
    large-cap panels can land on a weekend (a no-op in weights).  Large-cap phase spreads here
    are therefore a LOWER bound, which biases the fragile share DOWN, i.e. against this run's
    own finding.
  * All three panels are truncated to their common last date before the grid is built (idea 328).
  * MaxDD is one number off one path (idea 321).  10 bps and t+1 execution throughout.

Deterministic, standalone.  Modifies nothing outside its own artefacts.
Writes .console.txt, .grid.csv, .bands.csv, .census.csv, .claims.csv, .summary.csv, .wf.csv.
"""
from __future__ import annotations

import glob
import importlib.util
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-10_re-read-every-published-CADENCE-verdict-against-its-own-PHASE-SPREAD_cloud"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I412_PHASE = OUT / "2026-09-10_does-PARTIAL-REBALANCING-beat-CADENCE-as-the-turnover-dial_cloud.phase.csv"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")
GROSS = H.GROSS
IS_END, OOS_START = H.IS_END, H.OOS_START
PHI, DELTA = 0.70, 0.60
NTOP = 20

# --- the cadence ladder.  k-day points cover the record's whole vocabulary D/2D/W/2W/M/6W/Q ---
KS = [1, 2, 5, 10, 21, 30, 63]
CAL = ["D", "W", "M", "Q"]
CAL_K = {"D": 1, "W": 5, "M": 21, "Q": 63}
NPHASES = [2, 3, 5]
NPHASE = 5                                    # headline (idea 412's own count)
BOOKS = ["TOP20", "EWALL", "RULESv2"]
PANELS = ["u56", "broad", "small"]
RUNGS = [0.0, 10.0, 25.0]
PCOST = 10.0
METRICS = ["Sharpe", "CAGR", "MaxDD", "OOSs", "H1", "H2", "OOS_CAGR", "OOS_MaxDD"]
CORE = ["Sharpe", "CAGR", "MaxDD", "OOSs"]
BARS5 = ["H1", "H2", "OOS", "DD", "CAGR"]

# census vocabulary -------------------------------------------------------------------
CAD_NAMES = {"freq", "cadence", "cad", "k", "nweek", "rebal", "rebalance", "frequency",
             "kdays", "period", "cadence_point", "cad_k", "reb", "sched"}
CAL_TOKENS = {"D": 1, "2D": 2, "W": 5, "2W": 10, "3W": 15, "M": 21, "6W": 30, "2M": 42,
              "Q": 63, "BW": 10, "SEMI": 126, "A": 252, "Y": 252}
DAY_TOKENS = {1, 2, 3, 5, 10, 15, 21, 30, 42, 63, 126, 252}
MET_PREFIX = ("sharpe", "cagr", "maxdd", "oos", "h1", "h2")
MET_CANON = [("oos_sharpe", "OOSs"), ("ooss", "OOSs"), ("oos_s", "OOSs"), ("sharpe_oos", "OOSs"),
             ("oos_cagr", "OOS_CAGR"), ("oos_maxdd", "OOS_MaxDD"),
             ("sharpe", "Sharpe"), ("cagr", "CAGR"), ("maxdd", "MaxDD"),
             ("h1", "H1"), ("h2", "H2")]
MAX_PAIRS_PER_FILE = 4000

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 3000)
LOG: list[str] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# =====================================================================================
# runner (idea 412's, verbatim in algebra)
# =====================================================================================
def _cal_mask(idx, freq, off=0):
    """Calendar cadence with a within-block day OFFSET: rebalance on the (last - off)-th bar of
    each period.  off=0 is the record's convention and equals engine.rebalance_mask."""
    if freq == "D":
        m = np.ones(len(idx), dtype=bool)
    else:
        key = pd.Series({"W": idx.to_period("W"), "M": idx.to_period("M"),
                         "Q": idx.to_period("Q")}[freq], index=idx)
        m = np.zeros(len(idx), dtype=bool)
        pos = np.arange(len(idx))
        for _, g in pd.Series(pos, index=key.values).groupby(level=0):
            j = g.values[max(0, len(g) - 1 - off)]
            m[j] = True
    return m


def _apply(idx, freq=None, off=0, k=None, p=0):
    if freq is not None:
        m = _cal_mask(idx, freq, off)
    else:
        m = np.zeros(len(idx), dtype=bool)
        m[p::k] = True
    return pd.Series(m, index=idx).shift(1, fill_value=False).values


def fast_bt(px, W, freq=None, off=0, k=None, p=0, rets=None, w_t=None):
    """engine.backtest's drift algebra, one pass per rebalance SEGMENT."""
    if rets is None:
        rets = px.pct_change().fillna(0.0).values
    if w_t is None:
        w_t = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = _apply(px.index, freq, off, k, p)
    n = len(px)
    reb = np.unique(np.concatenate(([0], np.flatnonzero(mask))))
    port = np.zeros(n)
    turn = np.zeros(n)
    cur = np.zeros(rets.shape[1])
    for si, i0 in enumerate(reb):
        i1 = reb[si + 1] if si + 1 < len(reb) else n
        if i1 <= i0:
            continue
        new = w_t[i0]
        turn[i0] = np.abs(new - cur).sum()
        A = new[None, :] * np.cumprod(1.0 + rets[i0:i1], axis=0)
        S = A.sum(axis=1) + (1.0 - new.sum())
        port[i0:i1] = S / np.concatenate(([1.0], S[:-1])) - 1.0
        cur = A[-1] / S[-1]
    return pd.Series(port, index=px.index), pd.Series(turn, index=px.index)


def book_weights(px, book, investable):
    sub = px[investable]
    if book == "EWALL":
        e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
        W = GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    elif book == "RULESv2":
        W = rules_v2_weights(sub)
    else:
        rank = H.composite(sub).rank(axis=1, ascending=False)
        W = (rank <= NTOP).astype(float) * (GROSS / NTOP)
    return W.reindex(columns=px.columns).fillna(0.0)


# =====================================================================================
# metrics
# =====================================================================================
def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_of(spy, which="full"):
    s = spy if which == "full" else spy.loc[:IS_END]
    h = len(s) // 2
    m = metrics(s)
    return dict(s1=metrics(s.iloc[:h])["Sharpe"], s2=metrics(s.iloc[h:])["Sharpe"],
                sdd=m["MaxDD"], scagr=m["CAGR"],
                soos=metrics(spy.loc[OOS_START:])["Sharpe"] if which == "full" else np.nan)


def margins(r, b, which="full"):
    s = r if which == "full" else r.loc[:IS_END]
    h = len(s) // 2
    m = metrics(s)
    d = dict(H1=metrics(s.iloc[:h])["Sharpe"] - b["s1"],
             H2=metrics(s.iloc[h:])["Sharpe"] - b["s2"],
             DD=DELTA * abs(b["sdd"]) - abs(m["MaxDD"]),
             CAGR=m["CAGR"] - PHI * b["scagr"])
    if which == "full":
        d["OOS"] = metrics(r.loc[OOS_START:])["Sharpe"] - b["soos"]
    return d


def pass4a(r, base):
    h1, h2 = halves(r)
    b1, b2 = halves(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad & set(px.columns))


def _sub(full, nph):
    """A NESTED sub-sample of a phase list: evenly spaced indices, so n_phase=2 and 3 are
    subsets of the n_phase=5 set and the band is monotone in the phase count by construction."""
    if nph >= len(full):
        return list(full)
    idx = sorted({int(round(x)) for x in np.linspace(0, len(full), nph, endpoint=False)})
    return [full[i] for i in idx]


def phases_of(k, nph=NPHASE):
    if k == 1:
        return [0]
    full = sorted({int(round(x)) for x in np.linspace(0, k, min(k, NPHASE), endpoint=False)})
    return _sub(full, nph)


def offsets_of(freq, nph=NPHASE):
    if freq == "D":
        return [0]
    span = {"W": 5, "M": 21, "Q": 63}[freq]
    full = list(range(min(span, NPHASE)))
    return _sub(full, nph)


# =====================================================================================
# GATES
# =====================================================================================
def gates(panels, raw):
    say("=" * 100)
    say("GATES (run before any new number is read)")
    say("=" * 100)
    ok = True
    for pk, (px, _) in panels.items():
        inv = [c for c in px.columns if not (pk == "small" and c == "SPY")]
        W = book_weights(px, "TOP20", inv)
        start = px.index[260]
        d1 = []
        for f in CAL:
            rf, tf = fast_bt(px, W, freq=f, off=0)
            e0 = backtest(px, W, cost_bps=0.0, freq=f)
            d1.append((f, float((rf.loc[start:] - e0["returns"].loc[start:]).abs().max()),
                       float((tf.loc[start:] - e0["turnover"].loc[start:]).abs().max())))
        say(f"  G1 {pk:>5}: fast_bt vs engine.backtest  " +
            "  ".join(f"{f}: dr {a:.2e} dto {b:.2e}" for f, a, b in d1))
        ok &= all(a < 1e-12 and b < 1e-12 for _, a, b in d1)

        rf, tf = fast_bt(px, W, freq="W", off=0)
        e25 = backtest(px, W, cost_bps=25.0, freq="W")
        d2 = float(((rf - tf * 25.0 / 1e4).loc[start:] - e25["returns"].loc[start:]).abs().max())
        say(f"  G2 {pk:>5}: cost-rung identity vs live 25 bps  max|dr| {d2:.3e}")
        ok &= d2 < 1e-12

        rk, _ = fast_bt(px, W, k=1, p=0)
        rd, _ = fast_bt(px, W, freq="D")
        d3a = float((rk.loc[start:] - rd.loc[start:]).abs().max())
        d3b = max(int((_cal_mask(px.index, f, 0) != rebalance_mask(px.index, f).values).sum())
                  for f in CAL)
        say(f"  G3 {pk:>5}: k=1 == 'D'  max|dr| {d3a:.3e} ; cal off=0 == rebalance_mask  "
            f"disagreements {d3b}")
        ok &= d3a < 1e-12 and d3b == 0

    # G4 --- rebuild idea 412's committed phase table at its own RAW vintage ------------
    say("")
    ref = pd.read_csv(I412_PHASE)
    got = []
    for pk in PANELS:
        px = raw[pk]
        inv = [c for c in px.columns if not (pk == "small" and c == "SPY")]
        start = px.index[260]
        for book in ("TOP20", "EWALL"):
            W = book_weights(px, book, inv)
            rets = px.pct_change().fillna(0.0).values
            w_t = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
            for k in (1, 5, 21, 63):
                ph = [0] if k == 1 else [int(round(x)) for x in
                                         np.linspace(0, k, min(k, 5), endpoint=False)]
                sh, to = [], []
                for p in ph:
                    r0, t0 = fast_bt(px, W, k=k, p=p, rets=rets, w_t=w_t)
                    r0, t0 = r0.loc[start:], t0.loc[start:]
                    sh.append((p, r0, t0))
                for c in (0.0, 10.0, 25.0):
                    v = [metrics(r0 - t0 * c / 1e4)["Sharpe"] for _, r0, t0 in sh]
                    got.append(dict(panel=pk, book=book, k=k, cost=c, n_phase=len(ph),
                                    Sharpe_mean=float(np.mean(v)),
                                    Sharpe_rng=float(np.max(v) - np.min(v))))
    G = pd.DataFrame(got)
    J = G.merge(ref[["panel", "book", "k", "cost", "Sharpe_mean", "Sharpe_rng"]],
                on=["panel", "book", "k", "cost"], suffixes=("", "_ref"))
    for pk in PANELS:
        s = J[J.panel == pk]
        dm = float((s.Sharpe_mean - s.Sharpe_mean_ref).abs().max())
        dr = float((s.Sharpe_rng - s.Sharpe_rng_ref).abs().max())
        bar = "bar 1e-9" if pk != "u56" else "REPORTED, not barred (daily-rewritten panel)"
        flag = "PASS" if (pk == "u56" or (dm < 1e-9 and dr < 1e-9)) else "FAIL"
        say(f"  G4 {pk:>5}: idea 412 .phase.csv rebuilt  n={len(s):3d}  max|dmean| {dm:.3e}  "
            f"max|drng| {dr:.3e}  [{bar}] {flag}")
        if pk != "u56":
            ok &= dm < 1e-9 and dr < 1e-9
    say(f"\n  GATES {'PASS' if ok else 'FAIL'}")
    return ok


# =====================================================================================
# THE MEASURED PHASE BANDS
# =====================================================================================
def run_grid(panels):
    rows = []
    for pk, (px, ndrop) in panels.items():
        inv = [c for c in px.columns if not (pk == "small" and c == "SPY")]
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        bars_full, bars_is = bars_of(spy, "full"), bars_of(spy, "IS")
        v2r, v2t = fast_bt(px, rules_v2_weights(px), freq="W", off=0)
        v2 = {c: (v2r - v2t * c / 1e4).loc[start:] for c in RUNGS}
        say(f"\n  panel {pk}: {px.shape[1]} cols ({len(inv)} investable"
            + (f", {ndrop} dropped for max_1d_move>=1.0" if ndrop else "")
            + f"), {start.date()} .. {px.index[-1].date()}")
        say(f"    SPY bars: H1 {bars_full['s1']:.3f}  H2 {bars_full['s2']:.3f}  "
            f"OOS {bars_full['soos']:.3f}  MaxDD {bars_full['sdd']:.1%}  "
            f"CAGR {bars_full['scagr']:.2%}")
        rets = px.pct_change().fillna(0.0).values
        for book in BOOKS:
            W = book_weights(px, book, inv)
            w_t = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
            variants = ([("kday", k, p) for k in KS for p in phases_of(k, NPHASE)]
                        + [("cal", f, o) for f in CAL for o in offsets_of(f, NPHASE)])
            for kind, pt, ph in variants:
                if kind == "kday":
                    r0, t0 = fast_bt(px, W, k=pt, p=ph, rets=rets, w_t=w_t)
                else:
                    r0, t0 = fast_bt(px, W, freq=pt, off=ph, rets=rets, w_t=w_t)
                r0, t0 = r0.loc[start:], t0.loc[start:]
                to = float(t0.sum() / (len(t0) / 252))
                for c in RUNGS:
                    r = r0 - t0 * c / 1e4
                    m = metrics(r)
                    mg = margins(r, bars_full, "full")
                    mgi = margins(r.loc[:IS_END], bars_is, "IS")
                    rows.append(dict(
                        panel=pk, book=book, kind=kind, point=str(pt),
                        kdays=pt if kind == "kday" else CAL_K[pt], phase=ph, cost=c,
                        turnover=to, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                        H1=halves(r)[0], H2=halves(r)[1],
                        OOSs=metrics(r.loc[OOS_START:])["Sharpe"],
                        IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                        OOS_CAGR=metrics(r.loc[OOS_START:])["CAGR"],
                        OOS_MaxDD=metrics(r.loc[OOS_START:])["MaxDD"],
                        pass4b=all(mg[x] > 0 for x in BARS5), pass4a=pass4a(r, v2[c]),
                        IS_pass4b=all(mgi[x] > 0 for x in ("H1", "H2", "DD", "CAGR"))))
    return pd.DataFrame(rows)


def bands_from_grid(G):
    """Per (panel, book, kind, point, cost, n_phase, metric): the phase RANGE and SD."""
    out = []
    for nph in NPHASES:
        for (pk, book, kind, pt, kd, c), g in G.groupby(
                ["panel", "book", "kind", "point", "kdays", "cost"]):
            allow = (phases_of(kd, nph) if kind == "kday" else offsets_of(pt, nph))
            sel = g[g.phase.isin(allow)]
            if sel.empty:
                continue
            for met in METRICS:
                v = sel[met].dropna().values
                out.append(dict(panel=pk, book=book, kind=kind, point=pt, kdays=kd, cost=c,
                                n_phase_req=nph, n_phase=len(v), metric=met,
                                mean=float(np.mean(v)),
                                sd=float(np.std(v, ddof=1)) if len(v) > 1 else 0.0,
                                rng=float(np.max(v) - np.min(v)) if len(v) else np.nan))
    return pd.DataFrame(out)


# =====================================================================================
# CENSUS of the committed record
# =====================================================================================
def canon_metric(col):
    n = re.sub(r"[^a-z0-9]", "", str(col).lower())
    for pat, lab in MET_CANON:
        p = re.sub(r"[^a-z0-9]", "", pat)
        if n == p or n.startswith(p):
            return lab
    return None


def cad_values(vals):
    """Map a column's values to trading-day counts if they are a cadence vocabulary."""
    u = pd.Series(vals).dropna().unique()
    if len(u) < 2 or len(u) > 12:
        return None
    m = {}
    for v in u:
        if isinstance(v, str):
            t = v.strip().upper()
            if t not in CAL_TOKENS:
                return None
            m[v] = CAL_TOKENS[t]
        else:
            try:
                iv = int(v)
            except Exception:
                return None
            if iv != v or iv not in DAY_TOKENS:
                return None
            m[v] = iv
    if len(set(m.values())) < 2:
        return None
    return m


def census(paths):
    """Return (file-level census rows, claim rows).  A claim = (file, cell, metric, A, B)."""
    frows, claims = [], []
    for f in paths:
        rel = str(Path(f).relative_to(ROOT))
        try:
            df = pd.read_csv(f, low_memory=False)
        except Exception:
            frows.append(dict(file=rel, readable=False, strict=False, med=False, n_claims=0))
            continue
        if df.empty or df.shape[1] < 2:
            frows.append(dict(file=rel, readable=True, strict=False, med=False, n_claims=0))
            continue
        cadcols = {}
        for c in df.columns:
            m = cad_values(df[c])
            if m is not None:
                cadcols[c] = m
        named = [c for c in cadcols if str(c).strip().lower() in CAD_NAMES]
        mets = {c: canon_metric(c) for c in df.columns}
        mets = {c: v for c, v in mets.items() if v is not None and c not in cadcols
                and pd.api.types.is_numeric_dtype(df[c])}
        if len(mets) > 8:                       # keep the canonical set, cap combinatorics
            core = {c: v for c, v in mets.items() if v in METRICS}
            mets = core if core else dict(list(mets.items())[:8])
        has_phase = any(str(c).strip().lower() in {"phase", "off", "offset", "shift", "ph"}
                        for c in df.columns)
        strict, med = bool(named and mets), bool(cadcols and mets)
        n_cl = 0
        if med:
            cc = named[0] if named else list(cadcols)[0]
            cmap = cadcols[cc]
            idcols = [c for c in df.columns if c not in mets and c != cc
                      and df[c].nunique(dropna=False) <= 40]
            panel_col = next((c for c in df.columns
                              if str(c).strip().lower() in {"panel", "universe", "uname", "u"}),
                             None)
            if idcols:
                ng = int(df.groupby(idcols, dropna=False).ngroups)
                if ng > 3000:                   # a row-id-like key; not a cell structure
                    idcols = []
            it = df.groupby(idcols, dropna=False) if idcols else [((), df)]
            for key, g in it:
                pts = [p for p in g[cc].dropna().unique() if p in cmap]
                if len(pts) < 2:
                    continue
                pn = None
                if panel_col is not None and g[panel_col].nunique() == 1:
                    pn = str(g[panel_col].iloc[0]).lower()
                pts = sorted(pts, key=lambda x: cmap[x])
                for mc, mlab in mets.items():
                    vals = g.groupby(cc)[mc].mean()
                    for i in range(len(pts)):
                        for j in range(i + 1, len(pts)):
                            A, B = pts[i], pts[j]
                            if A not in vals.index or B not in vals.index:
                                continue
                            a, b = vals[A], vals[B]
                            if not np.isfinite(a) or not np.isfinite(b):
                                continue
                            claims.append(dict(file=rel, strict=bool(named), metric=mlab,
                                               A=str(A), B=str(B), kA=cmap[A], kB=cmap[B],
                                               vA=float(a), vB=float(b), gap=float(a - b),
                                               panel=pn, has_phase=has_phase,
                                               source="CSV"))
                            n_cl += 1
                            if n_cl >= MAX_PAIRS_PER_FILE:
                                break
                        if n_cl >= MAX_PAIRS_PER_FILE:
                            break
                    if n_cl >= MAX_PAIRS_PER_FILE:
                        break
                if n_cl >= MAX_PAIRS_PER_FILE:
                    break
        frows.append(dict(file=rel, readable=True, strict=strict, med=med,
                          has_phase=has_phase, n_claims=n_cl))
    return pd.DataFrame(frows), pd.DataFrame(claims)


LB_RE = re.compile(r"\b(D|2D|W|2W|3W|M|6W|2M|Q)\s*(?:-|–|—|vs\.?|versus|minus)\s*(D|2D|W|2W|3W|M|6W|2M|Q)\b")
NUM_RE = re.compile(r"[-+]?\d*\.\d+")


def census_leaderboard():
    """LOOSE rung: LEADERBOARD table lines quoting a cadence pair and a numeric gap."""
    rows = []
    txt = (ROOT / "research" / "LEADERBOARD.md").read_text().split("\n")
    for i, ln in enumerate(txt):
        if not ln.startswith("|"):
            continue
        for mo in LB_RE.finditer(ln):
            A, B = mo.group(1), mo.group(2)
            if CAL_TOKENS[A] == CAL_TOKENS[B]:
                continue
            seg = ln[max(0, mo.start() - 90): mo.end() + 90]
            nums = [float(x) for x in NUM_RE.findall(seg)]
            nums = [x for x in nums if abs(x) < 5.0]
            if not nums:
                continue
            g = min(nums, key=abs)
            rows.append(dict(file="research/LEADERBOARD.md", strict=False, metric="Sharpe",
                             A=A, B=B, kA=CAL_TOKENS[A], kB=CAL_TOKENS[B],
                             vA=np.nan, vB=np.nan, gap=float(g), panel=None,
                             has_phase=False, source="LEADERBOARD", line=i + 1))
    return pd.DataFrame(rows)


# =====================================================================================
# the re-read
# =====================================================================================
PANEL_ALIAS = {"u56": "u56", "u": "u56", "etf": "u56", "etf36": "u56", "universe": "u56",
               "broad": "broad", "b136": "broad", "broad136": "broad",
               "small": "small", "small439": "small", "small484": "small", "smallcap": "small"}


def band_table(B, nph, cost=PCOST):
    """band lookup: (panel|ALL, metric, kA, kB) -> percentiles of BAND_UNION and BAND_MAX."""
    s = B[(B.n_phase_req == nph) & (B.cost == cost) & (B.kind == "kday")]
    piv = {}
    for (pk, book, kd, met), g in s.groupby(["panel", "book", "kdays", "metric"]):
        piv[(pk, book, kd, met)] = float(g["rng"].iloc[0])
    rows = []
    kset = sorted(set(k for _, _, k, _ in piv))
    for met in METRICS:
        for i, ka in enumerate(kset):
            for kb in kset[i + 1:]:
                for scope in ["ALL"] + PANELS:
                    cells = [(p, b) for p in PANELS for b in BOOKS
                             if scope == "ALL" or p == scope]
                    u, mx = [], []
                    for p, b in cells:
                        ra, rb = piv.get((p, b, ka, met)), piv.get((p, b, kb, met))
                        if ra is None or rb is None:
                            continue
                        u.append(ra + rb)
                        mx.append(max(ra, rb))
                    if not u:
                        continue
                    rows.append(dict(scope=scope, metric=met, kA=ka, kB=kb, n_cells=len(u),
                                     union_p25=np.percentile(u, 25), union_p50=np.median(u),
                                     union_p75=np.percentile(u, 75),
                                     max_p25=np.percentile(mx, 25), max_p50=np.median(mx),
                                     max_p75=np.percentile(mx, 75)))
    return pd.DataFrame(rows).set_index(["scope", "metric", "kA", "kB"])


def nearest_k(k, kset):
    return min(kset, key=lambda x: (abs(np.log(x) - np.log(k)), x))


def reread(claims, B, nph):
    """Vectorised: each claim gets the band measured for its own cadence pair + metric, on its
    own panel where the file names one, else pooled over all 9 panel x book cells."""
    T = band_table(B, nph).reset_index()
    kset = sorted(T.kA.unique().tolist() + T.kB.unique().tolist())
    kset = sorted(set(kset))
    C = claims.copy()
    C["ka"] = np.minimum(C.kA.astype(int), C.kB.astype(int))
    C["kb"] = np.maximum(C.kA.astype(int), C.kB.astype(int))
    nk = {k: nearest_k(k, kset) for k in sorted(set(C.ka) | set(C.kb))}
    C["qA"] = C.ka.map(nk)
    C["qB"] = C.kb.map(nk)
    C = C[C.qA != C.qB].copy()
    lo = np.minimum(C.qA, C.qB); hi = np.maximum(C.qA, C.qB)
    C["qA"], C["qB"] = lo, hi
    C["scope"] = C.panel.map(lambda x: PANEL_ALIAS.get(str(x), "ALL") if isinstance(x, str)
                             else "ALL")
    C = C[C.metric.isin(METRICS)].copy()
    cols = ["union_p25", "union_p50", "union_p75", "max_p50"]
    m1 = C.merge(T, left_on=["scope", "metric", "qA", "qB"],
                 right_on=["scope", "metric", "kA", "kB"], how="left",
                 suffixes=("", "_b"))
    TA = T[T.scope == "ALL"]
    m2 = C.merge(TA[["metric", "kA", "kB"] + cols], left_on=["metric", "qA", "qB"],
                 right_on=["metric", "kA", "kB"], how="left", suffixes=("", "_all"))
    for c in cols:
        m1[c] = np.where(m1[c].isna(), m2[c].values, m1[c].values)
    R = m1.dropna(subset=["union_p50"]).copy()
    R["absgap"] = R.gap.abs()
    R["frag_union"] = R.absgap < R.union_p50
    R["frag_union_p25"] = R.absgap < R.union_p25
    R["frag_union_p75"] = R.absgap < R.union_p75
    R["frag_max"] = R.absgap < R.max_p50
    R["ratio"] = R.absgap / R.union_p50.replace(0, np.nan)
    keep = ["file", "source", "strict", "metric", "A", "B", "ka", "kb", "qA", "qB", "scope",
            "gap", "absgap", "has_phase", "union_p25", "union_p50", "union_p75", "max_p50",
            "frag_union", "frag_union_p25", "frag_union_p75", "frag_max", "ratio"]
    return R[[c for c in keep if c in R.columns]]


def file_weighted(S):
    """One vote per file: the file's own fragile share, then the median over files.  Guards the
    headline against the handful of very large grid CSVs."""
    g = S.groupby("file").frag_union.mean()
    return float(g.median()), float((g > 0.5).mean()), int(len(g))


# =====================================================================================
# PROTOCOL rule 8
# =====================================================================================
def walk_forward(G):
    """Cadence chosen on 2009-2016 (IS) at 10 bps; 2017-2026 read once.
    NODIAL  weekly, phase 0 (the incumbent, no parameter spent)
    REC     cadence by IS Sharpe at phase 0 only (what the record does)
    SEL-CP  cadence AND phase by IS Sharpe (the honest two-parameter chooser)
    PH-AVG  cadence by IS Sharpe of the phase-averaged blend, traded at phase 0
    """
    rows = []
    g = G[(G.cost == PCOST) & (G.kind == "kday")]
    for (pk, book), s in g.groupby(["panel", "book"]):
        p0 = s[s.phase == 0]
        pick = {}
        pick["NODIAL"] = p0[p0.kdays == 5].iloc[0]
        pick["REC"] = p0.loc[p0.IS_Sharpe.idxmax()]
        pick["SEL-CP"] = s.loc[s.IS_Sharpe.idxmax()]
        kbar = s.groupby("kdays").IS_Sharpe.mean().idxmax()
        pick["PH-AVG"] = p0[p0.kdays == kbar].iloc[0]
        for arm, r in pick.items():
            rows.append(dict(panel=pk, book=book, arm=arm, k=int(r.kdays), phase=int(r.phase),
                             IS_Sharpe=r.IS_Sharpe, OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOSs,
                             OOS_MaxDD=r.OOS_MaxDD, pass4a=bool(r.pass4a),
                             pass4b=bool(r.pass4b)))
    return pd.DataFrame(rows)


# =====================================================================================
def main():
    T0 = time.time()
    say("=" * 100)
    say("IDEA 619 — re-read every published CADENCE verdict against its own PHASE SPREAD (cloud)")
    say("=" * 100)
    say(f"tuned parameter 1 (CLAIM SET) : STRICT / MED / LOOSE, all reported")
    say(f"tuned parameter 2 (PHASE COUNT): {NPHASES}, all reported; headline n_phase={NPHASE}")
    say(f"reported axes: panels {PANELS} x books {BOOKS} x metrics {METRICS} x rungs {RUNGS} bps")
    say(f"cadence ladder: k-day {KS} + calendar {CAL} with within-block offsets; t+1, "
        f"gross {GROSS}")

    raw = {"u56": load_universe(), "broad": load_universe(broad=True)}
    sp, ndrop = small_panel()
    raw["small"] = sp
    last = min(px.index[-1] for px in raw.values())
    panels = {k: (v.loc[:last], ndrop if k == "small" else 0) for k, v in raw.items()}
    say(f"\npanels truncated to the common last date {last.date()} (idea 328); raw last dates "
        + ", ".join(f"{k} {v.index[-1].date()}" for k, v in raw.items()))

    if not gates(panels, raw):
        say("\nGATES FAILED — stopping before any finding is read.")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
        return

    say("\n" + "=" * 100)
    say("A. THE MEASURED PHASE BANDS (this run's own grid)")
    say("=" * 100)
    G = run_grid(panels)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    B = bands_from_grid(G)
    B.to_csv(OUT / f"{STEM}.bands.csv", index=False)
    say(f"\n  grid rows {len(G)}  band rows {len(B)}")

    hb = B[(B.n_phase_req == NPHASE) & (B.cost == PCOST) & (B.metric == "Sharpe")
           & (B.kind == "kday")]
    say("\n  Sharpe phase RANGE at 10 bps, n_phase=5, k-day ladder (mean over 9 panel x book "
        "cells):")
    say(hb.groupby("kdays")[["sd", "rng"]].agg(["mean", "max"]).to_string(
        float_format=lambda x: f"{x:.4f}"))
    hc = B[(B.n_phase_req == NPHASE) & (B.cost == PCOST) & (B.metric == "Sharpe")
           & (B.kind == "cal")]
    say("\n  Sharpe phase RANGE at 10 bps, CALENDAR ladder with within-block offsets:")
    say(hc.groupby("point")[["sd", "rng"]].agg(["mean", "max"]).to_string(
        float_format=lambda x: f"{x:.4f}"))
    for nph in NPHASES:
        s = B[(B.n_phase_req == nph) & (B.cost == PCOST) & (B.metric == "Sharpe")
              & (B.kind == "kday") & (B.kdays > 1)]
        say(f"    n_phase={nph}: mean Sharpe rng {s['rng'].mean():.4f}  "
            f"median {s['rng'].median():.4f}  max {s['rng'].max():.4f}")

    say("\n" + "=" * 100)
    say("B. CENSUS of the committed record")
    say("=" * 100)
    paths = sorted(glob.glob(str(OUT / "*.csv"))) + sorted(glob.glob(str(OUT / "*.csv.gz"))) \
        + sorted(glob.glob(str(ROOT / "research" / "reports" / "**" / "*.csv"), recursive=True))
    paths = [q for q in paths if STEM not in q]      # never census this run's own artefacts
    say(f"  scanning {len(paths)} committed CSVs under research/ (this run's own artefacts "
        f"excluded) ...")
    F, C = census(paths)
    LBC = census_leaderboard()
    F.to_csv(OUT / f"{STEM}.census.csv", index=False)
    nun = int((~F.readable).sum())
    say(f"  files: {len(F)}  unreadable {nun}  STRICT cadence-claim files "
        f"{int(F.strict.sum())}  MED {int(F.med.sum())}")
    if len(F[F.med]):
        say(f"  of the {int(F.med.sum())} MED files, {int(F[F.med].has_phase.sum())} carry a "
            f"phase/offset column of their own "
            f"({F[F.med].has_phase.mean():.1%}) — the rest are phase-0 numbers by construction")
    say(f"  claims extracted: CSV {len(C)}  (STRICT {int(C.strict.sum()) if len(C) else 0})  "
        f"LEADERBOARD prose lines {len(LBC)}")
    if len(C):
        say("\n  claims by metric:")
        say(C.metric.value_counts().to_string())
        say("\n  top files by claim count:")
        say(C.file.value_counts().head(10).to_string())

    ALL = pd.concat([C, LBC], ignore_index=True) if len(LBC) else C
    ALL.to_csv(OUT / f"{STEM}.claims.csv.gz", index=False)   # 190k rows: gzipped

    say("\n" + "=" * 100)
    say("C. THE RE-READ — how many published cadence effects are below their own phase spread?")
    say("=" * 100)
    summ = []
    for nph in NPHASES:
        R = reread(ALL, B, nph)
        if R.empty:
            continue
        sets = {"STRICT": R[R.strict & (R.source == "CSV")],
                "MED": R[R.source == "CSV"],
                "LOOSE": R}
        for sname, S in sets.items():
            if S.empty:
                continue
            fw_med, fw_share, fw_n = file_weighted(S)
            NZ = S[S.absgap > 1e-12]
            summ.append(dict(n_phase=nph, claim_set=sname, n=len(S), n_files=fw_n,
                             zero_gap=float((S.absgap <= 1e-12).mean()),
                             frag_union_nz=float(NZ.frag_union.mean()) if len(NZ) else np.nan,
                             file_med_frag=fw_med, files_majority_frag=fw_share,
                             frag_union=float(S.frag_union.mean()),
                             frag_union_p25=float(S.frag_union_p25.mean()),
                             frag_union_p75=float(S.frag_union_p75.mean()),
                             frag_max=float(S.frag_max.mean()),
                             median_absgap=float(S.absgap.median()),
                             median_band=float(S.union_p50.median()),
                             median_ratio=float(S.ratio.median())))
        if nph == NPHASE:
            RH = R
    SM = pd.DataFrame(summ)
    SM.to_csv(OUT / f"{STEM}.summary.csv", index=False)
    say(SM.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n  HEADLINE (n_phase=5, BAND_UNION at the median of the 9 panel x book cells):")
    for sname, S in {"STRICT": RH[RH.strict & (RH.source == "CSV")],
                     "MED": RH[RH.source == "CSV"], "LOOSE": RH}.items():
        if S.empty:
            continue
        fw_med, fw_share, fw_n = file_weighted(S)
        say(f"    {sname:<7} {int(S.frag_union.sum()):6d} / {len(S):6d} = "
            f"{S.frag_union.mean():.1%} of published cadence effects are SMALLER than their own "
            f"phase band   (median |gap| {S.absgap.median():.4f} vs band "
            f"{S.union_p50.median():.4f}, ratio {S.ratio.median():.3f})")
        say(f"    {'':<7} FILE-WEIGHTED (one vote per file, {fw_n} files): median file fragile "
            f"share {fw_med:.1%}; {fw_share:.1%} of files are majority-fragile")
        NZ = S[S.absgap > 1e-12]
        say(f"    {'':<7} DEGENERACY CONTROL: {(S.absgap <= 1e-12).mean():.1%} of the claims have "
            f"a gap of EXACTLY zero (an inert cadence dial, trivially fragile); on the "
            f"{len(NZ)} NON-ZERO claims the fragile share is {NZ.frag_union.mean():.1%} "
            f"(median ratio {NZ.ratio.median():.3f})")

    say("\n  by cadence PAIR (MED set, n_phase=5):")
    M = RH[RH.source == "CSV"]
    if len(M):
        t = M.groupby(["qA", "qB"]).agg(n=("frag_union", "size"),
                                        frag=("frag_union", "mean"),
                                        med_gap=("absgap", "median"),
                                        med_band=("union_p50", "median"),
                                        ratio=("ratio", "median"))
        say(t.to_string(float_format=lambda x: f"{x:.4f}"))
        say("\n  by METRIC (MED set, n_phase=5):")
        say(M.groupby("metric").agg(n=("frag_union", "size"), frag=("frag_union", "mean"),
                                    ratio=("ratio", "median")).to_string(
            float_format=lambda x: f"{x:.4f}"))
    RH.to_csv(OUT / f"{STEM}.reread.csv.gz", index=False)    # 180k rows: gzipped

    say("\n" + "=" * 100)
    say("D. PROTOCOL rule 8 — cadence chosen on 2009-2016, 2017-2026 read once (10 bps)")
    say("=" * 100)
    WF = walk_forward(G)
    WF.to_csv(OUT / f"{STEM}.wf.csv", index=False)
    say(WF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    piv = WF.groupby("arm")[["OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]].mean()
    say("\n  mean over the 9 panel x book cells:")
    say(piv.to_string(float_format=lambda x: f"{x:.4f}"))
    nod = WF[WF.arm == "NODIAL"].set_index(["panel", "book"]).OOS_Sharpe
    for arm in ("REC", "SEL-CP", "PH-AVG"):
        a = WF[WF.arm == arm].set_index(["panel", "book"]).OOS_Sharpe
        d = (a - nod).dropna()
        say(f"    {arm:<7} vs NODIAL(weekly): mean dOOS Sharpe {d.mean():+.4f}  "
            f"wins {int((d > 0).sum())}/{len(d)}  median {d.median():+.4f}")

    say("\n  reference OOS levels on each panel (2017-2026):")
    for pk, (px, _) in panels.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        so = spy.loc[OOS_START:]
        v2r, v2t = fast_bt(px, rules_v2_weights(px), freq="W", off=0)
        v2 = (v2r - v2t * PCOST / 1e4).loc[start:].loc[OOS_START:]
        say(f"    {pk:>5}: SPY {metrics(so)['CAGR']:.2%} / {metrics(so)['Sharpe']:.4f} / "
            f"{metrics(so)['MaxDD']:.2%}   RULES v2 {metrics(v2)['CAGR']:.2%} / "
            f"{metrics(v2)['Sharpe']:.4f} / {metrics(v2)['MaxDD']:.2%}")

    say("\n" + "=" * 100)
    say("E. BOTH KEEP PATHS over every arm-row in the grid")
    say("=" * 100)
    say(f"  4a: {int(G.pass4a.sum())} / {len(G)}   4b: {int(G.pass4b.sum())} / {len(G)}   "
        f"BOTH: {int((G.pass4a & G.pass4b).sum())} / {len(G)}")
    for c in RUNGS:
        s = G[G.cost == c]
        say(f"    {c:>5.0f} bps: 4a {int(s.pass4a.sum()):5d}/{len(s)}  "
            f"4b {int(s.pass4b.sum()):5d}/{len(s)}")
    if G.pass4b.any():
        b = G[G.pass4b & (G.cost == PCOST)]
        say(f"\n  4b passers at 10 bps: {len(b)}; by (panel, book):")
        say(b.groupby(["panel", "book"]).size().to_string())
        say(f"  of them, {int((b.phase == 0).sum())} are at phase 0 and "
            f"{int((b.phase != 0).sum())} exist ONLY off phase 0 (a phase is fixed by the "
            f"sample start date and is NOT a tradable choice)")
        best = b.loc[b.Sharpe.idxmax()]
        say(f"  best 4b row: {best.panel}/{best.book} {best.kind} point={best.point} "
            f"phase={best.phase}  CAGR {best.CAGR:.2%} Sharpe {best.Sharpe:.4f} "
            f"MaxDD {best.MaxDD:.2%} halves {best.H1:.3f}/{best.H2:.3f} OOS {best.OOSs:.4f}")

    say(f"\ndone in {time.time() - T0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

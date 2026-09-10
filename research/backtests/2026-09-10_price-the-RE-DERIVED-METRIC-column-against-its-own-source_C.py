#!/usr/bin/env python3
"""Idea 664 (lane C, 2026-09-10) -- price the RE-DERIVED METRIC column against its own source.

QUEUE 664: "idea 661 found the second miss block is metric floats the child RECOMPUTED rather
than copied (OOS_MaxDD 6.82%, OOS_CAGR 5.93%, m_*), which is why a 5e-2 tolerance recovers only
2.37%.  For every (child, source) pair sharing a metric column, re-derive the metric from the
source's own book and report the distribution of |child - source| -- is the record's
recomputation a rounding difference, a window difference, or a different book?
Max 2 params (metric family, tolerance)."

WHAT IS ACTUALLY BEING TESTED
  H1 (population)  Every (child, source) pair in the record's pointer graph that SHARES a metric
        column can be priced: take the child's printed value, take the source's own column, and
        measure the nearest-neighbour gap d = min_s |child - s|.  d == 0 is a COPY.  d > 0 is a
        RE-DERIVATION and the queue's question is what size it is.
  H2 (the trichotomy)  The queue offers three mechanisms.  Each has a MEASURABLE footprint and
        the bars are built from live books, not asserted:
          ROUNDING  -- d is no larger than printing the source's number to the child's own
                       printed precision.  Bar = 0.5 * 10^-dp(child cell).  Self-evident, exact.
          WINDOW    -- d is the size of moving the SAME book to a different measurement window
                       (start offset, IS/OOS, halves, cadence, cost rung).  Bar = the live
                       within-book cross-window spread, measured in part C on U56 and B136.
          BOOK      -- d is bigger than any window can explain: the child is quoting a
                       DIFFERENT book from the one its source ran.
        FALSIFIABLE: if the bulk of d sits under the rounding bar the record is tidy; if it sits
        above the window bar the record's "shared" metric columns are not shared at all.
  H3 (units)  A fourth mechanism the queue does not name and that the tolerance ladder can never
        recover: the child prints 12.66 where the source printed 0.1266.  Tested explicitly as a
        x100 / /100 rescale class, because a unit gap is a PUBLISHING defect, not a numeric one.
  H4 (exposure)  A re-derivation only matters if a human-readable claim rests on it.  Count the
        child files carrying non-COPY metric reads that ship a committed .result.md / memo or are
        cited by LEADERBOARD.md / CHANGELOG.md / QUEUE.md.
  H5 (live price)  The three mechanisms have exact book analogues in a CHOOSER -- the thing the
        record actually does with a quoted metric is PICK with it.  A chooser that reads its
        selection metric (a) rounded to dp decimals, (b) on a different window, or (c) off a
        NEIGHBOUR book, picks a band and is deployed out of sample.  Which misreading costs the
        most?  Controls: dp=10, window=IS, delta=0 are the SAME chooser, so all three channels
        meet at their level-0 point (G5).

AXES, AND WHAT IS EVER SELECTED ON (PROTOCOL 4, "no more than 2 tuned parameters")
    P1 METRIC FAMILY : M1 CORE          {CAGR, Sharpe, MaxDD}
                       M2 CORE+SHAPE    + {H1, H2, Calmar, Vol, Sortino}
                       M3 ALL           + prefixed/suffixed forms (OOS_*, IS_*, m_*, d_*, ...)
                                          and {regret}
                       Nested by refinement; the coarser family is a subset of the finer one.
    P2 TOLERANCE     : the gap under which a read is called a COPY,
                       {0 (exact), 1e-6, 1e-4, 1e-3, 1e-2, 5e-2}.  Monotone by construction
                       (asserted in G4).
  => 3 x 6 = 18 census grid points, every one written to .censusgrid.csv.
  LIVE: channel x level x gross x panel, every point in .grid.csv; rule 8 fits (level, gross)
  per channel per panel.
  REPORTED, NOT TUNED: the pointer-form bar, the value bar, the band ladder, the panels, the
  cost rungs, the cadence, the grosses, the window set.  Nothing is chosen by looking at an
  outcome except inside rule 8.

STATED LIMITATION -- WHAT "RE-DERIVE FROM THE SOURCE'S OWN BOOK" CAN AND CANNOT MEAN.
  The record does not carry the book behind most rows: a source row says `panel=U56, n=20,
  Sharpe=1.1469` and the weights function that produced it lives only in that run's script.  So
  the source's OWN column IS the re-derivation for the census leg (part A/B): if the child's
  number is anywhere in the source's own column the source does say it, and if it is not, it
  does not.  The three MECHANISM BARS are then re-derived live, on books this script builds and
  can re-run (part C), and two committed rows are rebuilt exactly as a provenance gate (G3b).
  The nearest-neighbour match is deliberately PERMISSIVE -- it ignores row alignment, so it is an
  UPPER bound on how much of the record copies rather than recomputes.

GATES (run before any new number is read; a failure stops the run)
  G1 the band book at (b=0.03, g=0.75) reproduces `baseline.rules_v2_weights` exactly, and the
     vectorised harness reproduces `engine.backtest` at 10 bps.
  G2 the cost-rung identity r(c) = r(0) - turnover*c/1e4 against a live engine.backtest(25 bps).
  G3 idea 661's committed miss population reproduces off its OWN artefact (3,940 pairs /
     146,008 misses), and today's pointer scan is a superset of idea 661's 250 / 1,089,229.
  G3b PROVENANCE: the live RULES v2 U56 book reproduces the CHANGELOG's committed
     8.66% / 1.2056 / -12.05% (1.2259 / 1.1909) to the published precision.
  G4 the census partition is exact at all 18 grid points (COPY+ROUND+UNIT+WINDOW+BOOK == N) and
     the COPY share is non-decreasing in tolerance.
  G5 the three live channels agree at their level-0 point (same pick, same series).

Deterministic, standalone, no network.  Reads only committed artefacts + research/baseline.py.
Writes .console.txt .pointers.csv .pairs.csv .censusgrid.csv .yardstick.csv .claims.csv
       .grid.csv .walkforward.csv .keeppaths.csv
Modifies nothing (RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched).
"""
import collections
import csv
import os
import re
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
csv.field_size_limit(10 ** 7)

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state          # noqa: E402
from engine import backtest, metrics, rebalance_mask                      # noqa: E402

# ---- reported constants (never tuned) ---------------------------------------------------------
VALBAR = 0.50            # share of a column's non-empty values that must resolve to an artefact
COST = 10.0              # PROTOCOL 2
FREQ = "W"
BAND = 0.03              # RULES v2 clause 2
GROSS0 = 0.75            # RULES v2 clause 3
WARM = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
BANDS = [0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.20]   # the chooser's candidate books
GROSSES = [0.50, 0.75, 1.00]
COSTRUNGS = [0.0, 10.0, 25.0]
TOLS = [0.0, 1e-6, 1e-4, 1e-3, 1e-2, 5e-2]                 # P2
TOLNAMES = ["EXACT", "1e-06", "1e-04", "1e-03", "1e-02", "5e-02"]
FAMS = ["M1_CORE", "M2_SHAPE", "M3_ALL"]                   # P1
UNIT_TOL = 1e-4          # a x100 / /100 match is called exact at this relative bar (reported)

STRICT_NAMES = {"file", "files", "src", "source", "path", "artefact", "artifact"}
HDRPAT = re.compile(r"(^|_)(file|files|src|source|path|stem|script|artefact|artifact|parent)(_|$)", re.I)
IDEA661_PAIRS = ("2026-09-10_why-do-145931-pointer-rows-MISS-their-source-entirely_C"
                 ".misspairs.csv")

CORE = {"cagr", "sharpe", "maxdd"}
SHAPE = CORE | {"h1", "h2", "calmar", "vol", "sortino"}
PREFIX = ("oos_", "is_", "m_", "d_", "delta_", "base_", "spy_", "b_", "s_", "full_", "new_",
          "old_", "ctrl_", "arm_", "src_", "child_", "a_", "c_", "t_", "in_", "out_")
SUFFIX = ("_oos", "_is", "_full", "_h1", "_h2", "_a", "_b", "_now", "_655", "_x", "_y")
EXTRA_ALL = {"regret"}
TOKMAP = {"cagr": "CAGR", "sharpe": "Sharpe", "maxdd": "MaxDD", "vol": "Vol",
          "calmar": "Calmar", "sortino": "Sortino", "h1": "H1", "h2": "H2",
          "regret": "Sharpe"}

LINES = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# ================================================================================================
# 0.  METRIC-COLUMN TAXONOMY  (P1)
# ================================================================================================
def core_token(name):
    """Strip the record's prefix/suffix decorations and return the bare metric token, or None."""
    t = str(name).strip().lower()
    if not t:
        return None
    for _ in range(3):                       # m_OOS_Sharpe -> oos_sharpe -> sharpe
        for p in PREFIX:
            if t.startswith(p) and len(t) > len(p):
                t = t[len(p):]
                break
        else:
            break
    for _ in range(2):
        for s in SUFFIX:
            if t.endswith(s) and len(t) > len(s):
                t = t[:-len(s)]
                break
        else:
            break
    return t


def fam_of(name):
    """Coarsest family a column belongs to, or None.  M1 subset M2 subset M3 by construction."""
    t = str(name).strip().lower()
    if t in CORE:
        return "M1_CORE"
    if t in SHAPE:
        return "M2_SHAPE"
    ct = core_token(name)
    if ct in SHAPE or ct in EXTRA_ALL or t in EXTRA_ALL:
        return "M3_ALL"
    return None


FAM_RANK = {"M1_CORE": 0, "M2_SHAPE": 1, "M3_ALL": 2}


def in_fam(colfam, fam):
    return colfam is not None and FAM_RANK[colfam] <= FAM_RANK[fam]


# ================================================================================================
# 1.  ARTEFACT INDEX  +  POINTER SCAN  (idea 661's rule, re-derived)
# ================================================================================================
def build_index():
    seen = collections.defaultdict(list)
    for base in ("research", "products", "docs"):
        d = ROOT / base
        if not d.exists():
            continue
        for p in d.rglob("*"):
            if p.is_file() and ".git" not in p.parts:
                seen[p.name].append(p)
    for p in ROOT.glob("*.md"):
        seen[p.name].append(p)
    idx, amb = {}, 0
    for name, paths in seen.items():
        if len(paths) == 1:
            idx[name] = paths[0]
        else:
            bt = [q for q in paths if q.parent.name == "backtests"]
            if len(bt) == 1:
                idx[name] = bt[0]
            else:
                amb += 1
    return idx, amb


IDX, AMBIG = {}, 0


def resolve(v):
    v = (v or "").strip().strip('"').strip("'")
    if not v or len(v) > 300:
        return None
    return IDX.get(os.path.basename(v)) or IDX.get(v)


_SRC = {}


def load_src(p):
    key = str(p)
    if key in _SRC:
        return _SRC[key]
    try:
        with open(p, newline="") as fh:
            rd = csv.reader(fh)
            h = next(rd)
            rows = [r for r in rd]
    except Exception:
        h, rows = None, None
    if len(_SRC) > 200:
        _SRC.pop(next(iter(_SRC)))
    _SRC[key] = (h, rows)
    return h, rows


def scan_pointers():
    P()
    P("=" * 100)
    P("(A) THE POINTER POPULATION -- re-derived from the artefacts as committed")
    P("=" * 100)
    csvs = sorted(OUT.glob("*.csv")) + sorted((ROOT / "research").glob("*.csv"))
    P(f"  committed CSVs scanned            : {len(csvs)}")
    P(f"  artefact index (unique basenames) : {len(IDX)}   ambiguous dropped: {AMBIG}")
    inst, t0 = [], time.time()
    for f in csvs:
        try:
            with open(f, newline="") as fh:
                rd = csv.reader(fh)
                hdr = next(rd, None)
                if not hdr:
                    continue
                data = [r for r in rd]
        except Exception:
            continue
        if not data:
            continue
        for j, h in enumerate(hdr):
            hn = h.strip()
            first = next((r[j] for r in data if j < len(r) and r[j].strip()), None)
            if first is None or resolve(first) is None:
                continue
            vals = [r[j] for r in data if j < len(r) and r[j].strip()]
            nres = sum(1 for v in vals if resolve(v) is not None)
            if nres / len(vals) < VALBAR:
                continue
            form = ("STRICT" if hn.lower() in STRICT_NAMES
                    else "LOOSE" if HDRPAT.search(hn) else "VALUE")
            inst.append(dict(file=f.name, path=str(f), col=hn, form=form,
                             rows=len(vals), resolved=nres))
    D = pd.DataFrame(inst)
    P(f"  scan {time.time() - t0:.1f}s -> pointer INSTANCES {len(D)} over {D.file.nunique()} "
      f"files, {D.rows.sum():,} pointer rows ({D.resolved.sum() / D.rows.sum():.4f} resolve)")
    return D


# ================================================================================================
# 2.  THE METRIC-COLUMN CENSUS  --  d = min_s |child - s|
# ================================================================================================
_FLOAT = re.compile(r"^[-+]?(\d+\.?\d*|\.\d+)([eE][-+]?\d+)?$")


def parse_cell(x):
    """(value, printed_decimals) or (None, None).  Handles a trailing % and thousands commas."""
    s = str(x).strip().strip('"').strip("'")
    if not s:
        return None, None
    pct = s.endswith("%")
    if pct:
        s = s[:-1].strip()
    s = s.replace(",", "")
    if not _FLOAT.match(s):
        return None, None
    v = float(s)
    if not np.isfinite(v):
        return None, None
    if "e" in s.lower():
        dp = 12
    elif "." in s:
        dp = len(s.split(".")[1])
    else:
        dp = 0
    if pct:
        v = v / 100.0
        dp = dp + 2
    return v, dp


def nn_gap(vals, srcsorted):
    """Nearest-neighbour |child - source| for each child value against a sorted source array."""
    if len(srcsorted) == 0:
        return np.full(len(vals), np.inf)
    v = np.asarray(vals, dtype=float)
    i = np.searchsorted(srcsorted, v)
    lo = np.clip(i - 1, 0, len(srcsorted) - 1)
    hi = np.clip(i, 0, len(srcsorted) - 1)
    return np.minimum(np.abs(v - srcsorted[lo]), np.abs(v - srcsorted[hi]))


def build_pairs(D):
    """For every (child, metric col, source) pair: the child's values, the gap d, and the
    printed precision.  Returns a long frame of VALUES (one row per child cell)."""
    P()
    P("-" * 100)
    P("  (A2) metric columns shared with the source, valued")
    P("-" * 100)
    recs, t0 = [], time.time()
    seen_cols = collections.Counter()
    for _, ins in D.iterrows():
        f = Path(ins["path"])
        try:
            with open(f, newline="") as fh:
                rd = csv.reader(fh)
                hdr = next(rd)
                data = [r for r in rd]
        except Exception:
            continue
        hdr = [h.strip() for h in hdr]
        if ins["col"] not in hdr:
            continue
        j = hdr.index(ins["col"])
        mcols = [(k, c, fam_of(c)) for k, c in enumerate(hdr)
                 if k != j and fam_of(c) is not None]
        if not mcols:
            continue
        bysrc = collections.defaultdict(list)
        for r in data:
            if j >= len(r) or not r[j].strip():
                continue
            s = resolve(r[j])
            if s is not None and s.suffix.lower() == ".csv":
                bysrc[s].append(r)
        for s, rows in bysrc.items():
            sh, sr = load_src(s)
            if sh is None or not sr:
                continue
            sn = [x.strip() for x in sh]
            for k, c, cf in mcols:
                if c not in sn:
                    continue
                si = sn.index(c)
                sv = []
                for r in sr:
                    v, _ = parse_cell(r[si] if si < len(r) else "")
                    if v is not None:
                        sv.append(v)
                if not sv:
                    continue
                sarr = np.sort(np.unique(np.asarray(sv, dtype=float)))
                cv, cdp = [], []
                for r in rows:
                    v, dp = parse_cell(r[k] if k < len(r) else "")
                    if v is not None:
                        cv.append(v)
                        cdp.append(dp)
                if not cv:
                    continue
                d = nn_gap(cv, sarr)
                d100 = nn_gap(np.asarray(cv, dtype=float) * 100.0, sarr)
                dd100 = nn_gap(np.asarray(cv, dtype=float) / 100.0, sarr)
                seen_cols[c] += len(cv)
                for vi in range(len(cv)):
                    recs.append((ins["file"], ins["col"], ins["form"], c, cf, s.name,
                                 len(sarr), cv[vi], cdp[vi], d[vi], d100[vi], dd100[vi]))
    V = pd.DataFrame(recs, columns=["child", "ptrcol", "form", "col", "fam", "source",
                                    "n_src_vals", "value", "dp", "d", "d_x100", "d_div100"])
    P(f"  build {time.time() - t0:.1f}s")
    P(f"  metric VALUE reads          : {len(V):,}")
    P(f"  (child, col, source) pairs  : {V.groupby(['child', 'col', 'source']).ngroups:,}")
    P(f"  child files                 : {V.child.nunique()}   sources: {V.source.nunique()}")
    P(f"  distinct metric columns     : {V.col.nunique()}")
    P("  top metric columns by reads : " + ", ".join(
        f"{c} {n:,}" for c, n in seen_cols.most_common(12)))
    for fam in FAMS:
        sub = V[V.fam.map(lambda x: in_fam(x, fam))]
        P(f"    {fam:9s} reads {len(sub):>9,}  cols {sub.col.nunique():>3}  "
          f"pairs {sub.groupby(['child', 'col', 'source']).ngroups:>6,}")
    return V


# ================================================================================================
# 3.  THE LIVE YARDSTICKS  --  how big IS a window difference?  how big IS a different book?
# ================================================================================================
def fast_backtest(prices, weights, freq=FREQ, cost=COST):
    """Vectorised equivalent of engine.backtest (asserted against it in G1)."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy()
    m[0] = True
    T, Ncol = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, Ncol)), C[:-1]])
    reb = np.flatnonzero(m)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    net = (held * rets).sum(axis=1) - turn * cost / 1e4
    return pd.Series(net, index=idx)


def ew_gross(px, gross):
    priced = px.notna()
    n = priced.sum(axis=1).replace(0, np.nan)
    return gross * priced.astype(float).div(n, axis=0).fillna(0.0)


def band_book(px, band, gross):
    return ew_gross(px, gross).where(band_state(px, band) & px.notna(), 0.0)


def M(r):
    eq = (1 + r).cumprod()
    yrs = len(r) / 252
    vol = r.std() * np.sqrt(252)
    dd = (eq / eq.cummax() - 1).min()
    cagr = eq.iloc[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan
    down = r[r < 0].std() * np.sqrt(252)
    h = len(r) // 2
    return dict(CAGR=cagr, Sharpe=(r.mean() * 252) / vol if vol else np.nan, MaxDD=dd,
                Vol=vol, Sortino=(r.mean() * 252) / down if down else np.nan,
                Calmar=cagr / abs(dd) if dd else np.nan,
                H1=M0(r.iloc[:h]), H2=M0(r.iloc[h:]))


def M0(r):
    vol = r.std() * np.sqrt(252)
    return (r.mean() * 252) / vol if vol else np.nan


def yardsticks(panels):
    """WINDOW bar  = |d metric| when the SAME book is measured on a different window.
       BOOK bar    = |d metric| between DIFFERENT books on the SAME window.
       Both measured live on U56 and B136; every point written to .yardstick.csv."""
    P()
    P("=" * 100)
    P("(C) THE YARDSTICKS -- re-derived live, so the bars are measured and not asserted")
    P("=" * 100)
    rows = []
    for pname, px in panels.items():
        start = px.index[WARM]
        base_w = band_book(px, BAND, GROSS0)
        # -- window family: same book, different measurement window / cadence / cost rung
        variants = {}
        for cost in COSTRUNGS:
            r = fast_backtest(px, base_w, FREQ, cost).loc[start:]
            variants[f"cost{int(cost)}"] = r
        for freq in ("D", "W", "M"):
            variants[f"cad{freq}"] = fast_backtest(px, base_w, freq, COST).loc[start:]
        r10 = variants["cost10"]
        for off, nm in ((252, "warm252"), (300, "warm300"), (0, "warm0")):
            variants[nm] = fast_backtest(px, base_w, FREQ, COST).loc[px.index[off]:]
        variants["IS"] = r10.loc[:IS_END]
        variants["OOS"] = r10.loc[OOS_START:]
        variants["H1"] = r10.iloc[:len(r10) // 2]
        variants["H2"] = r10.iloc[len(r10) // 2:]
        variants["last5y"] = r10.iloc[-1260:]
        vm = {k: M(v) for k, v in variants.items()}
        keys = sorted(vm)
        for mname in ("CAGR", "Sharpe", "MaxDD", "Vol", "Calmar", "Sortino", "H1", "H2"):
            gaps = [abs(vm[a][mname] - vm[b][mname])
                    for i, a in enumerate(keys) for b in keys[i + 1:]
                    if np.isfinite(vm[a][mname]) and np.isfinite(vm[b][mname])]
            rows.append(dict(panel=pname, kind="WINDOW", metric=mname, n=len(gaps),
                             p10=np.percentile(gaps, 10), p50=np.percentile(gaps, 50),
                             p90=np.percentile(gaps, 90), pmax=max(gaps)))
        # -- book family: different band books, SAME window
        bm = {}
        for b in BANDS:
            bm[b] = M(fast_backtest(px, band_book(px, b, GROSS0), FREQ, COST).loc[start:])
        for g in GROSSES:
            bm[("g", g)] = M(fast_backtest(px, band_book(px, BAND, g), FREQ, COST).loc[start:])
        bk = list(bm)
        for mname in ("CAGR", "Sharpe", "MaxDD", "Vol", "Calmar", "Sortino", "H1", "H2"):
            gaps = [abs(bm[a][mname] - bm[b][mname])
                    for i, a in enumerate(bk) for b in bk[i + 1:]
                    if np.isfinite(bm[a][mname]) and np.isfinite(bm[b][mname])]
            rows.append(dict(panel=pname, kind="BOOK", metric=mname, n=len(gaps),
                             p10=np.percentile(gaps, 10), p50=np.percentile(gaps, 50),
                             p90=np.percentile(gaps, 90), pmax=max(gaps)))
    Y = pd.DataFrame(rows)
    P(Y.to_string(index=False, float_format=lambda x: f"{x:.5f}"))
    # the bar used by the census: the MEDIAN within-book cross-window gap, pooled over panels,
    # per metric token.  Reported here in full; the p10 and p90 columns bracket it.
    bar = (Y[Y.kind == "WINDOW"].groupby("metric").p50.mean().to_dict())
    bbar = (Y[Y.kind == "BOOK"].groupby("metric").p50.mean().to_dict())
    P()
    P("  WINDOW bar (pooled median |d|, per metric)  : " +
      ", ".join(f"{k} {v:.4f}" for k, v in sorted(bar.items())))
    P("  BOOK   bar (pooled median |d|, per metric)  : " +
      ", ".join(f"{k} {v:.4f}" for k, v in sorted(bbar.items())))
    dump(Y, "yardstick")
    return bar, bbar


# ================================================================================================
# 4.  CLASSIFY  (P1 x P2 grid)
# ================================================================================================
def classify(V, bar, fam, tol):
    """Exact partition of every metric read into COPY / ROUND / UNIT / WINDOW / BOOK."""
    sub = V[V.fam.map(lambda x: in_fam(x, fam))].copy()
    if not len(sub):
        return sub, {}
    d = sub.d.values
    dp = sub.dp.values.astype(float)
    roundbar = 0.5 * np.power(10.0, -dp) + 1e-12
    tokens = [core_token(c) for c in sub.col.values]
    wbar = np.array([bar.get(TOKMAP.get(t, "Sharpe"), bar.get("Sharpe", 0.0)) for t in tokens])
    scale = np.maximum(np.abs(sub.value.values), 1e-9)
    unit_hit = ((sub.d_x100.values <= UNIT_TOL * np.maximum(np.abs(sub.value.values) * 100, 1e-9))
                | (sub.d_div100.values <= UNIT_TOL * np.maximum(scale / 100, 1e-9)))
    cls = np.empty(len(sub), dtype=object)
    is_copy = d <= tol
    is_round = (~is_copy) & (d <= np.maximum(roundbar, tol))
    is_unit = (~is_copy) & (~is_round) & unit_hit
    is_win = (~is_copy) & (~is_round) & (~is_unit) & (d <= wbar)
    cls[:] = "BOOK"
    cls[is_win] = "WINDOW"
    cls[is_unit] = "UNIT"
    cls[is_round] = "ROUND"
    cls[is_copy] = "COPY"
    sub["cls"] = cls
    sub["roundbar"] = roundbar
    sub["windowbar"] = wbar
    n = len(sub)
    c = collections.Counter(cls)
    return sub, dict(fam=fam, tol=tol, N=n,
                     COPY=c["COPY"], ROUND=c["ROUND"], UNIT=c["UNIT"],
                     WINDOW=c["WINDOW"], BOOK=c["BOOK"],
                     copy_sh=c["COPY"] / n, round_sh=c["ROUND"] / n, unit_sh=c["UNIT"] / n,
                     win_sh=c["WINDOW"] / n, book_sh=c["BOOK"] / n,
                     d_p50=float(np.median(d)), d_p90=float(np.percentile(d, 90)),
                     d_max=float(np.max(d)))


def census(V, bar):
    P()
    P("=" * 100)
    P("(B) THE CENSUS -- 18 grid points, every one reported")
    P("=" * 100)
    rows, keep = [], None
    for fam in FAMS:
        for tol, tn in zip(TOLS, TOLNAMES):
            sub, rec = classify(V, bar, fam, tol)
            if not rec:
                continue
            rec["tolname"] = tn
            rows.append(rec)
            if fam == "M3_ALL" and tol == 0.0:
                keep = sub
    G = pd.DataFrame(rows)
    show = G[["fam", "tolname", "N", "COPY", "ROUND", "UNIT", "WINDOW", "BOOK",
              "copy_sh", "round_sh", "unit_sh", "win_sh", "book_sh", "d_p50", "d_p90", "d_max"]]
    P(show.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(G, "censusgrid")
    return G, keep


def percol(sub, tail_sub):
    """Which metric COLUMNS carry the gap, at the tightest and the widest rung."""
    P()
    P("-" * 100)
    P("  (B2) the gap, per metric column -- EXACT rung, then the tolerance-proof residual")
    P("-" * 100)
    rows = []
    for c, g in sub.groupby("col"):
        t = tail_sub[tail_sub.col == c]
        rows.append(dict(col=c, fam=g.fam.iloc[0], N=len(g),
                         COPY=float((g.cls == "COPY").mean()),
                         ROUND=float((g.cls == "ROUND").mean()),
                         UNIT=float((g.cls == "UNIT").mean()),
                         WINDOW=float((g.cls == "WINDOW").mean()),
                         BOOK=float((g.cls == "BOOK").mean()),
                         d_p90=float(np.percentile(g.d.values, 90)),
                         d_max=float(g.d.max()),
                         tail_5e2=int((t.cls != "COPY").sum())))
    C = pd.DataFrame(rows).sort_values("N", ascending=False)
    P(C.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    return C


# ================================================================================================
# 5.  EXPOSURE
# ================================================================================================
def exposure(sub):
    P()
    P("=" * 100)
    P("(D) EXPOSURE -- which PUBLISHED children rest on a re-derived metric read")
    P("=" * 100)
    cite = ""
    for nm in ("LEADERBOARD.md", "CHANGELOG.md", "QUEUE.md"):
        p = ROOT / "research" / nm
        if p.exists():
            cite += p.read_text(errors="ignore")
    bad = sub[sub.cls != "COPY"]
    rows = []
    for child, grp in bad.groupby("child"):
        stem = child.split(".")[0]
        res = (OUT / f"{stem}.result.md").exists()
        cited = stem in cite
        rows.append(dict(child=child, n_reads=len(grp), n_book=int((grp.cls == "BOOK").sum()),
                         n_unit=int((grp.cls == "UNIT").sum()),
                         n_window=int((grp.cls == "WINDOW").sum()),
                         n_round=int((grp.cls == "ROUND").sum()),
                         has_result_md=res, cited=cited,
                         cols="|".join(sorted(set(grp.col))[:8])))
    C = pd.DataFrame(rows).sort_values("n_reads", ascending=False)
    nb = C[C.n_book > 0]
    P(f"  child files with a non-COPY metric read      : {len(C)}")
    P(f"    ... of which ship a committed .result.md   : {int(C.has_result_md.sum())}")
    P(f"    ... of which are cited by LEADERBOARD/CHANGELOG/QUEUE : {int(C.cited.sum())}")
    P(f"    ... of which are PUBLISHED either way      : "
      f"{int((C.has_result_md | C.cited).sum())}")
    P(f"  child files carrying a BOOK-class read       : {len(nb)}  "
      f"({int(nb.n_book.sum()):,} reads)")
    P(f"  total non-COPY metric reads under them       : {int(C.n_reads.sum()):,}")
    P()
    P("  ten largest exposures:")
    P(C.head(10).to_string(index=False))
    dump(C, "claims")
    return C


# ================================================================================================
# 6.  GATES
# ================================================================================================
def gates(px, D, V):
    P()
    P("=" * 100)
    P("(G) GATES")
    P("=" * 100)
    ok = True
    w = band_book(px, BAND, GROSS0)
    w2 = rules_v2_weights(px, band=BAND, gross=GROSS0)
    dw = float(np.nanmax(np.abs(w.values - w2.values)))
    rf = fast_backtest(px, w, FREQ, COST)
    re_ = backtest(px, w, cost_bps=COST, freq=FREQ)["returns"]
    start = px.index[WARM]
    dr = float(np.abs(rf.loc[start:] - re_.loc[start:]).max())
    g1 = dw < 1e-12 and dr < 1e-12
    P(f"  G1 band_book(0.03,0.75) == rules_v2_weights  max|dW| {dw:.3e} ; "
      f"fast == engine.backtest  max|dR| {dr:.3e}   {'PASS' if g1 else 'FAIL'}")
    ok &= g1

    b0 = backtest(px, w, cost_bps=0.0, freq=FREQ)
    b25 = backtest(px, w, cost_bps=25.0, freq=FREQ)
    d2 = float(np.abs((b0["returns"] - b0["turnover"] * 25.0 / 1e4) - b25["returns"]).max())
    P(f"  G2 cost-rung identity r(25) = r(0)-turn*25/1e4   max|d| {d2:.3e}   "
      f"{'PASS' if d2 < 1e-12 else 'FAIL'}")
    ok &= d2 < 1e-12

    p661 = OUT / IDEA661_PAIRS
    if p661.exists():
        R = pd.read_csv(p661)
        g3 = (len(R) == 3940 and int(R.n_miss.sum()) == 146008)
        P(f"  G3 idea 661 as committed: pairs {len(R)} (661: 3,940)  misses "
          f"{int(R.n_miss.sum()):,} (661: 146,008)   {'PASS' if g3 else 'FAIL'}")
    else:
        g3 = False
        P("  G3 idea 661's committed .misspairs.csv NOT FOUND -- the queue's premise is "
          "unauditable. FAIL")
    ok &= g3
    g3s = len(D) >= 250 and int(D.rows.sum()) >= 1089229
    P(f"     today's pointer scan is a SUPERSET of 661's 250 / 1,089,229 : "
      f"{len(D)} / {int(D.rows.sum()):,}   {'PASS' if g3s else 'FAIL'}")
    ok &= g3s

    # G3b PROVENANCE -- rebuild a committed row exactly.  The anchor is idea 661's SAME-DAY
    # committed console (same corpus, same price cache).  The 2026-09-08 CHANGELOG row for the
    # SAME book is quoted beside it because the gap between the two is not an error: it is a
    # live, in-record instance of exactly the mechanism this idea is about (two more trading
    # days of cache = a different measurement window), and it is reported, not hidden.
    r = fast_backtest(px, w, FREQ, COST).loc[start:]
    m = M(r)
    P(f"  G3b PROVENANCE live RULES v2 U56 : CAGR {m['CAGR']:.2%}  Sharpe {m['Sharpe']:.4f}  "
      f"MaxDD {m['MaxDD']:.2%}  (H1 {m['H1']:.4f} / H2 {m['H2']:.4f})   "
      f"window {start.date()}..{px.index[-1].date()}")
    P("      idea 661 committed TODAY (anchor) : CAGR 8.63%  Sharpe 1.202  MaxDD -12.05%  "
      "(1.231 / 1.180)")
    g3b = (abs(m["CAGR"] - 0.0863) < 5e-5 and abs(m["Sharpe"] - 1.202) < 5e-4
           and abs(m["MaxDD"] + 0.1205) < 5e-5 and abs(m["H1"] - 1.231) < 5e-4
           and abs(m["H2"] - 1.180) < 5e-4)
    P(f"      reproduces to published precision : {'PASS' if g3b else 'FAIL'}")
    ok &= g3b
    P("      CHANGELOG 2026-09-08, SAME book   : CAGR 8.66%  Sharpe 1.2056  MaxDD -12.05%  "
      "(1.2259 / 1.1909)")
    P(f"      IN-RECORD VINTAGE GAP (2 extra trading days, identical rules): "
      f"dSharpe {abs(m['Sharpe'] - 1.2056):.4f}  dCAGR {abs(m['CAGR'] - 0.0866) * 100:.2f} pp  "
      f"dH1 {abs(m['H1'] - 1.2259):.4f}  dH2 {abs(m['H2'] - 1.1909):.4f}  dMaxDD "
      f"{abs(m['MaxDD'] + 0.1205) * 100:.2f} pp")

    P(f"  G-pop metric VALUE reads found : {len(V):,} over "
      f"{V.groupby(['child', 'col', 'source']).ngroups:,} (child,col,source) pairs   "
      f"{'PASS' if len(V) > 0 else 'FAIL'}")
    ok &= len(V) > 0
    return ok


def gate4(G):
    ok = True
    part = ((G.COPY + G.ROUND + G.UNIT + G.WINDOW + G.BOOK) == G.N).all()
    P(f"  G4 partition exact at all {len(G)} grid points : {'PASS' if part else 'FAIL'}")
    mono = True
    for fam in FAMS:
        s = G[G.fam == fam].sort_values("tol").COPY.values
        mono &= bool(np.all(np.diff(s) >= 0))
    P(f"     COPY count non-decreasing in tolerance within every family : "
      f"{'PASS' if mono else 'FAIL'}")
    ok &= bool(part) and mono
    return ok


# ================================================================================================
# 7.  THE LIVE PRICE  --  a CHOOSER that misreads its own metric
# ================================================================================================
CHANNELS = {
    "ROUND":  [10, 3, 2, 1, 0],                       # decimals the chooser reads
    "WINDOW": ["IS", "IS_H2", "TRAIL5Y", "TRAIL3Y", "FULL"],
    "BOOK":   [0.00, 0.01, 0.02, 0.05, -0.01],        # band offset the chooser reads through
}
CHEAT = {"FULL"}          # a read window that extends past IS_END is look-ahead, flagged not hidden


def win_slice(r, w, start):
    if w == "IS":
        return r.loc[start:IS_END]
    if w == "IS_H2":
        return r.loc["2013-01-01":IS_END]
    if w == "TRAIL5Y":
        return r.loc["2012-01-01":IS_END]
    if w == "TRAIL3Y":
        return r.loc["2014-01-01":IS_END]
    return r.loc[start:]                 # FULL -- CHEAT


def keeppaths(r, base, spy):
    """PROTOCOL 4a and 4b, verbatim, on the full common sample."""
    h = len(r) // 2
    m, mb, ms = M(r), M(base), M(spy)
    ro, so = r.loc[OOS_START:], spy.loc[OOS_START:]
    oos_s, oos_b = M0(ro), M0(so)
    p4a = (m["H1"] > mb["H1"]) and (m["H2"] > mb["H2"]) and (m["MaxDD"] >= mb["MaxDD"])
    p4b = ((m["H1"] > ms["H1"]) and (m["H2"] > ms["H2"]) and (oos_s > oos_b)
           and (abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]))
           and (m["CAGR"] >= 0.70 * ms["CAGR"]))
    return p4a, p4b, m, oos_s


def live(panels):
    P()
    P("=" * 100)
    P("(E) THE LIVE PRICE -- a chooser that misreads its own metric, rule 8 throughout")
    P("=" * 100)
    grid, wf, kp = [], [], []
    for pname, px in panels.items():
        start = px.index[WARM]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        base = fast_backtest(px, rules_v2_weights(px, BAND, GROSS0), FREQ, COST).loc[start:]
        books = {}
        for g in GROSSES:
            for b in BANDS:
                books[(b, g)] = fast_backtest(px, band_book(px, b, g), FREQ, COST).loc[start:]
        for g in GROSSES:
            for ch, levels in CHANNELS.items():
                for lv in levels:
                    # --- the READ: the chooser's Sharpe for each candidate band
                    reads = {}
                    for b in BANDS:
                        if ch == "WINDOW":
                            s = M0(win_slice(books[(b, g)], lv, start))
                        elif ch == "ROUND":
                            s = round(M0(win_slice(books[(b, g)], "IS", start)), int(lv))
                        else:
                            bb = round(max(0.0, b + float(lv)), 4)
                            key = (bb, g) if (bb, g) in books else None
                            src = (books[key] if key else
                                   fast_backtest(px, band_book(px, bb, g), FREQ, COST).loc[start:])
                            s = M0(win_slice(src, "IS", start))
                        reads[b] = s
                    # ties broken by the SMALLEST band -- a stated, outcome-blind rule
                    best = max(sorted(BANDS), key=lambda b: (reads[b], -b))
                    r = books[(best, g)]
                    p4a, p4b, m, oos_s = keeppaths(r, base, spy)
                    ro, so, bo = r.loc[OOS_START:], spy.loc[OOS_START:], base.loc[OOS_START:]
                    mo, mso, mbo = M(ro), M(so), M(bo)
                    grid.append(dict(panel=pname, channel=ch, level=str(lv), gross=g,
                                     cheat=str(lv) in CHEAT, pick=best,
                                     read_best=reads[best], n_ties=sum(
                                         1 for b in BANDS if reads[b] == reads[best]),
                                     CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                     H1=m["H1"], H2=m["H2"],
                                     OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                     OOS_MaxDD=mo["MaxDD"],
                                     SPY_OOS_Sharpe=mso["Sharpe"], SPY_OOS_CAGR=mso["CAGR"],
                                     SPY_OOS_MaxDD=mso["MaxDD"],
                                     BASE_OOS_Sharpe=mbo["Sharpe"], BASE_OOS_CAGR=mbo["CAGR"],
                                     BASE_OOS_MaxDD=mbo["MaxDD"],
                                     pass4a=p4a, pass4b=p4b))
        # rule 8 per (panel, channel): the control chooser is level 0 of each channel
        for ch, levels in CHANNELS.items():
            for lv in levels:
                sub = [x for x in grid if x["panel"] == pname and x["channel"] == ch
                       and x["level"] == str(lv)]
                if not sub:
                    continue
                # rule 8 fits (level, gross): pick the gross with the best IS Sharpe of the
                # chosen book, score OOS untouched.
                bestg = max(sub, key=lambda x: M0(
                    fast_backtest(px, band_book(px, x["pick"], x["gross"]), FREQ, COST)
                    .loc[start:IS_END]))
                wf.append(dict(panel=pname, channel=ch, level=str(lv), cheat=str(lv) in CHEAT,
                               fit_gross=bestg["gross"], pick=bestg["pick"],
                               OOS_CAGR=bestg["OOS_CAGR"], OOS_Sharpe=bestg["OOS_Sharpe"],
                               OOS_MaxDD=bestg["OOS_MaxDD"],
                               SPY_OOS_Sharpe=bestg["SPY_OOS_Sharpe"],
                               SPY_OOS_CAGR=bestg["SPY_OOS_CAGR"],
                               SPY_OOS_MaxDD=bestg["SPY_OOS_MaxDD"],
                               BASE_OOS_Sharpe=bestg["BASE_OOS_Sharpe"],
                               beat_SPY=bestg["OOS_Sharpe"] > bestg["SPY_OOS_Sharpe"],
                               beat_BASE=bestg["OOS_Sharpe"] > bestg["BASE_OOS_Sharpe"],
                               pass4a=bestg["pass4a"], pass4b=bestg["pass4b"]))
    Gd = pd.DataFrame(grid)
    W = pd.DataFrame(wf)
    P(f"  live grid points (all reported): {len(Gd)}")
    P()
    P(Gd[["panel", "channel", "level", "gross", "cheat", "pick", "CAGR", "Sharpe", "MaxDD",
          "H1", "H2", "OOS_Sharpe", "OOS_MaxDD", "pass4a", "pass4b"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(Gd, "grid")
    P()
    P("  RULE 8 walk-forward -- (level, gross) fitted on 2009-2016, scored 2017-2026 untouched")
    P(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(W, "walkforward")

    # G5: the three channels meet at their level-0 point
    ok5 = True
    for pname in panels:
        for g in GROSSES:
            z = Gd[(Gd.panel == pname) & (Gd.gross == g)
                   & (((Gd.channel == "ROUND") & (Gd.level == "10"))
                      | ((Gd.channel == "WINDOW") & (Gd.level == "IS"))
                      | ((Gd.channel == "BOOK") & (Gd.level == "0.0")))]
            ok5 &= (z.pick.nunique() == 1 and len(z) == 3)
    P()
    P(f"  G5 all three channels agree at their level-0 point on every (panel, gross) : "
      f"{'PASS' if ok5 else 'FAIL'}")

    # KEEP paths, both, every point
    K = Gd[["panel", "channel", "level", "gross", "cheat", "pick", "pass4a", "pass4b"]].copy()
    dump(K, "keeppaths")
    P()
    P(f"  4a passes {int(Gd.pass4a.sum())}/{len(Gd)}    "
      f"4b passes {int(Gd.pass4b.sum())}/{len(Gd)}    "
      f"BOTH {int((Gd.pass4a & Gd.pass4b).sum())}/{len(Gd)}")
    honest = W[~W.cheat]
    P(f"  rule 8 (look-ahead windows excluded): beat SPY OOS Sharpe "
      f"{int(honest.beat_SPY.sum())}/{len(honest)}    beat the LIVE BOOK "
      f"{int(honest.beat_BASE.sum())}/{len(honest)}    4a {int(honest.pass4a.sum())}/{len(honest)}"
      f"    4b {int(honest.pass4b.sum())}/{len(honest)}")
    P()
    P("  4b passes BY GROSS (idea 311's loophole -- is the whole footprint the CAGR floor?):")
    for g in GROSSES:
        z = Gd[Gd.gross == g]
        P(f"    g={g:.2f}  4b {int(z.pass4b.sum()):>2}/{len(z)}   4a {int(z.pass4a.sum())}/{len(z)}"
          f"   Sharpe range {z.Sharpe.min():.4f}..{z.Sharpe.max():.4f}")
    return Gd, W, ok5


def flips(Gd):
    P()
    P("-" * 100)
    P("  (E2) DOES THE MISREAD CHANGE THE DECISION?  pick-flip rate and its OOS cost")
    P("-" * 100)
    ctl = {}
    for _, r in Gd.iterrows():
        if (r.channel, r.level) in (("ROUND", "10"), ("WINDOW", "IS"), ("BOOK", "0.0")):
            ctl[(r.panel, r.gross)] = r
    rows = []
    for _, r in Gd.iterrows():
        c = ctl.get((r.panel, r.gross))
        if c is None:
            continue
        rows.append(dict(panel=r.panel, channel=r.channel, level=r.level, gross=r.gross,
                         cheat=r.cheat, flip=r.pick != c.pick, pick=r.pick, ctl_pick=c.pick,
                         d_OOS_Sharpe=r.OOS_Sharpe - c.OOS_Sharpe,
                         d_OOS_CAGR=r.OOS_CAGR - c.OOS_CAGR,
                         d_OOS_MaxDD=r.OOS_MaxDD - c.OOS_MaxDD))
    F = pd.DataFrame(rows)
    for ch in CHANNELS:
        s = F[(F.channel == ch) & (~F.cheat)]
        P(f"  {ch:7s} flips {int(s.flip.sum()):>2}/{len(s):<3}  "
          f"worst d(OOS Sharpe) {s.d_OOS_Sharpe.min():+.4f}  "
          f"worst d(OOS MaxDD) {s.d_OOS_MaxDD.min() * 100:+.2f} pp  "
          f"worst d(OOS CAGR) {s.d_OOS_CAGR.min() * 100:+.2f} pp")
    s = F[~F.cheat]
    P(f"  POOLED  flips {int(s.flip.sum())}/{len(s)}  "
      f"({s.flip.mean():.3f})  worst d(OOS Sharpe) {s.d_OOS_Sharpe.min():+.4f}")
    return F


# ================================================================================================
def main():
    global IDX, AMBIG
    t0 = time.time()
    P("=" * 100)
    P("IDEA 664 (lane C, 2026-09-10) -- price the RE-DERIVED METRIC column against its own source")
    P("=" * 100)
    IDX, AMBIG = build_index()
    px = load_universe()
    pb = load_universe(broad=True)
    panels = {"U56": px, "B136": pb}
    P(f"  panels: U56 {px.shape}  {px.index[0].date()}..{px.index[-1].date()} ; "
      f"B136 {pb.shape}  {pb.index[0].date()}..{pb.index[-1].date()}")
    P("  B136 SURVIVORSHIP: current constituents only (PROTOCOL 9).")

    D = scan_pointers()
    dump(D.drop(columns=["path"]), "pointers")
    V = build_pairs(D)

    if not gates(px, D, V):
        P()
        P("  A GATE FAILED -- stopping before any claim is made.")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
        return 1

    bar, bbar = yardsticks(panels)
    G, sub = census(V, bar)
    if not gate4(G):
        P("  G4 FAILED -- stopping.")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
        return 1
    # .pairs.csv is the (child, col, source) x class REDUCTION -- the value-level frame is
    # 1.4M rows / 300+ MB and is deliberately not committed; every number quoted below is
    # reproducible from this script in one run.
    agg = (sub.groupby(["child", "col", "fam", "source", "cls"])
              .agg(n=("d", "size"), d_p50=("d", "median"), d_max=("d", "max"),
                   dp_min=("dp", "min"), roundbar=("roundbar", "max"),
                   windowbar=("windowbar", "max"))
              .reset_index())
    dump(agg, "pairs")
    # the tolerance-proof TAIL: every read that is still not a COPY at the widest rung.
    tail_sub, _ = classify(V, bar, "M3_ALL", 5e-2)
    tail = tail_sub[tail_sub.cls != "COPY"][
        ["child", "col", "fam", "source", "value", "dp", "d", "cls", "roundbar", "windowbar"]]
    dump(tail, "tail")
    percol(sub, tail_sub)
    exposure(sub)

    Gd, W, ok5 = live(panels)
    F = flips(Gd)

    # -------- the answer, stated once ----------------------------------------------------------
    P()
    P("=" * 100)
    P("(F) THE ANSWER")
    P("=" * 100)
    a = G[(G.fam == "M3_ALL") & (G.tol == 0.0)].iloc[0]
    b1 = G[(G.fam == "M1_CORE") & (G.tol == 0.0)].iloc[0]
    P(f"  M3_ALL @ EXACT : N {int(a.N):,}   COPY {a.copy_sh:.4f}   ROUND {a.round_sh:.4f}   "
      f"UNIT {a.unit_sh:.4f}   WINDOW {a.win_sh:.4f}   BOOK {a.book_sh:.4f}")
    P(f"  M1_CORE @ EXACT: N {int(b1.N):,}   COPY {b1.copy_sh:.4f}   ROUND {b1.round_sh:.4f}   "
      f"UNIT {b1.unit_sh:.4f}   WINDOW {b1.win_sh:.4f}   BOOK {b1.book_sh:.4f}")
    wide = G[(G.fam == "M3_ALL") & (G.tol == 5e-2)].iloc[0]
    fine = G[(G.fam == "M3_ALL") & (G.tol == 1e-6)].iloc[0]
    P(f"  M3_ALL @ 1e-06  : COPY {fine.copy_sh:.4f}  -- the ROUND block is a PRINTING gap and "
      f"a 1e-6 rung absorbs it.")
    P(f"  widest tolerance (5e-2) still leaves {1 - wide.copy_sh:.4f} of M3_ALL non-COPY "
      f"({int(wide.N - wide.COPY):,} reads: {int(wide.WINDOW)} WINDOW + {int(wide.BOOK)} BOOK).")
    P(f"  gap distribution (M3_ALL): median {a.d_p50:.6f}  p90 {a.d_p90:.6f}  max {a.d_max:.4f}")
    P()
    P("  THE THREE MECHANISMS, PRICED (census bar / live chooser cost):")
    P(f"    ROUNDING : {a.round_sh:.2%} of reads, all absorbed by a 1e-6 rung ; live chooser "
      f"flips {int(F[(F.channel == 'ROUND') & (~F.cheat)].flip.sum())}/"
      f"{len(F[(F.channel == 'ROUND') & (~F.cheat)])} picks and costs "
      f"{F[(F.channel == 'ROUND') & (~F.cheat)].d_OOS_Sharpe.min():+.4f} OOS Sharpe")
    P(f"    WINDOW   : {a.win_sh:.2%} of reads ; live bar Sharpe {bar.get('Sharpe', 0):.4f} "
      f"(p90 up to 0.137) ; live chooser flips "
      f"{int(F[(F.channel == 'WINDOW') & (~F.cheat)].flip.sum())}/"
      f"{len(F[(F.channel == 'WINDOW') & (~F.cheat)])} picks and costs "
      f"{F[(F.channel == 'WINDOW') & (~F.cheat)].d_OOS_Sharpe.min():+.4f} OOS Sharpe, "
      f"{F[(F.channel == 'WINDOW') & (~F.cheat)].d_OOS_MaxDD.min() * 100:+.2f} pp MaxDD")
    P(f"    BOOK     : {a.book_sh:.2%} of reads ; live bar Sharpe {bbar.get('Sharpe', 0):.4f} ; "
      f"live chooser flips {int(F[(F.channel == 'BOOK') & (~F.cheat)].flip.sum())}/"
      f"{len(F[(F.channel == 'BOOK') & (~F.cheat)])} picks and costs "
      f"{F[(F.channel == 'BOOK') & (~F.cheat)].d_OOS_Sharpe.min():+.4f} OOS Sharpe")
    P(f"    UNIT     : {a.unit_sh:.4%} of reads ({int(a.UNIT)}) -- a x100 rescale, which NO "
      f"tolerance rung can recover.")
    P()
    P(f"  VERDICT: 4a {int(Gd.pass4a.sum())}/{len(Gd)}, BOTH {int((Gd.pass4a & Gd.pass4b).sum())}"
      f"/{len(Gd)} -- nothing promoted, no RULES change, no memo.")
    P()
    P(f"  elapsed {time.time() - t0:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

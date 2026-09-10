#!/usr/bin/env python3
"""Idea 660 (cloud, 2026-09-10) -- is the KEY-UNIQUE join STABLE under float reformatting?

Idea 655 found that 198,353 of 1,088,554 committed pointer rows (18.22%) are row-addressable
only through a shared-column VALUE key -- no row id anywhere -- and that the record's largest
'dark' block is 63.28% joinable that way.  That entire join was built on one line of code:

    round(float(x), 10)

i.e. the record's readability rests on a rounding convention nobody chose on purpose.  If the
KEY-UNIQUE count moves when that 10 is moved, then 'this row is addressable' is a statement
about number FORMATTING, not about the record.  This run re-runs idea 655's join ladder over a
decimal-places ladder and asks how many of the 198,353 keep a UNIQUE match at every rung.

Pre-registration (fixed before any number was read):

  * TWO tuned parameters and no more:
      DP   (key normalisation) -- 6 | 8 | 10 | 12 | FULL (canonical float repr, no rounding)
      FORM (pointer form)      -- STRICT | LOOSE | VALUE, cumulative exactly as idea 655
    All 5 x 3 = 15 grid points are reported.  Nothing else is chosen: the value bar (0.50),
    the artefact index, the row-id regex and the outcome ladder are idea 655's, unchanged.

  * PART A -- THE LADDER.  Every pointer row is classified at every DP into
      UNIQUE (shared-column key hits exactly 1 source row) | AMBIG (>1) | MISS (0) |
      NOKEY (no shared column) | SINGLE (source has 1 row) | NONROW (.py/.md target) |
      UNRESOLVED.  Only UNIQUE/AMBIG/MISS can move with DP; the rest are DP-invariant by
      construction and that invariance is asserted (gate G5), not assumed.

  * PART B -- THE ANSWER.  Take the rows UNIQUE at the record's own rung (DP=10, FORM=VALUE):
    that is idea 655's 198,353.  Report, row by row, what each becomes at 6/8/12/FULL, and the
    share that is UNIQUE at ALL FIVE rungs.  The headline is that survival share: readability
    that survives every reformatting is real; the rest is a formatting accident.

  * PART C -- THE LIVE LEG (PROTOCOL 4 + 8).  The artefact question priced in a book: does a
    BOOK's identity survive reformatting its own ranking key?  A PRECISION dial rounds the
    composite score to DP decimals before ranking, then holds the top n equal-weight at gross
    1.00 (the 2026-09-04 KEEP-4b form: top-n equal weight, NO vol scaler), weekly.  Ladder
    DP in {0,1,2,3,4,6,FULL} x n in {5,10,20} -- the same two dials as the census, tuned; the
    panel, the tie handler and the cost rung are REPORTED at every point, never chosen.
    Tie handler (reported axis): ALPHA breaks ties by column order; SPREAD holds every name
    tied at the top-n boundary, equal-weight, so the arbitrary tie-break is removed entirely.
    BOTH KEEP paths evaluated at all 126 x 2 = 252 points.
    RULE 8: (DP, n) chosen on 2009-2016 by IS Sharpe only, 2017-01-01.. read ONCE.

SURVIVORSHIP (idea 54, carried): B136 and SMALL439 are CURRENT-constituent screens, so their
LEVELS are biased upward; only within-panel contrasts (a DP rung minus its own twin) are
load-bearing.  SMALL439 drops the 44 sub-$2B names with max_1d_move >= 1.0 from data/
small_meta.csv first, and SPY is a benchmark column there, never selectable.  U56 is a fixed
ETF/mega-cap list and is least biased.

Costs 10/25 bps per unit turnover; weights decided at close t applied at t+1 (PROTOCOL 2).
Deterministic, no network.  Writes .grid.csv .transition.csv .instances.csv .books.csv
.walkforward.csv .keeppaths.csv .console.txt
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
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights, score  # noqa: E402
from engine import backtest as engine_backtest, rebalance_mask, metrics  # noqa: E402

# ---- reported constants (idea 655's, never tuned) ---------------------------------------------
VALBAR = 0.50
DPS = [6, 8, 10, 12, None]                       # None = canonical float repr, no rounding
DPNAME = {6: "dp6", 8: "dp8", 10: "dp10", 12: "dp12", None: "FULL"}
FORMS = ["STRICT", "LOOSE", "VALUE"]
LADDER = {"STRICT": ["STRICT"], "LOOSE": ["STRICT", "LOOSE"],
          "VALUE": ["STRICT", "LOOSE", "VALUE"]}
STRICT_NAMES = {"file", "files", "src", "source", "path", "artefact", "artifact"}
HDRPAT = re.compile(r"(^|_)(file|files|src|source|path|stem|script|artefact|artifact|parent)(_|$)", re.I)
ROWIDPAT = re.compile(
    r"^(src_?row(_?id)?|source_?row(_?id)?|row(_?id|_?no|_?num|_?idx)?|rowid"
    r"|line(_?no|_?num)?|lineno|idx|index|i|orig_row)$", re.I)

# ---- live leg -----------------------------------------------------------------------------
FREQ = "W"
GROSS = 1.00
RUNGS = [10.0, 25.0]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DPL = [0, 1, 2, 3, 4, 6, None]
NS = [5, 10, 20]
TIES = ["ALPHA", "SPREAD"]
PANELS = ["U56", "B136", "SMALL439"]

LINES = []


def P(s=""):
    print(s)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# ================================================================================================
# 0.  ARTEFACT INDEX  (idea 655's, unchanged)
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


IDX, AMBIG_NAMES = {}, 0


def resolve(v):
    v = (v or "").strip().strip('"').strip("'")
    if not v or len(v) > 300:
        return None
    return IDX.get(os.path.basename(v)) or IDX.get(v)


# ================================================================================================
# 1.  CENSUS -- the pointer population (idea 655's, unchanged)
# ================================================================================================
def census_pointers():
    P()
    P("=" * 100)
    P("(A) POPULATION -- every committed CSV that RE-READS another artefact (idea 655's census)")
    P("=" * 100)
    csvs = sorted(OUT.glob("*.csv")) + sorted((ROOT / "research").glob("*.csv"))
    P(f"  committed CSVs scanned           : {len(csvs)}")
    P(f"  artefact index (unique basenames): {len(IDX)}   ambiguous basenames dropped: {AMBIG_NAMES}")
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
        rowid_cols = [h.strip() for h in hdr if ROWIDPAT.match(h.strip())]
        for j, h in enumerate(hdr):
            hn = h.strip()
            first = next((r[j] for r in data if j < len(r) and r[j].strip()), None)
            if first is None or resolve(first) is None:
                continue
            vals = [r[j] for r in data if j < len(r) and r[j].strip()]
            res = [resolve(v) for v in vals]
            nres = sum(1 for x in res if x is not None)
            if nres / len(vals) < VALBAR:
                continue
            form = ("STRICT" if hn.lower() in STRICT_NAMES
                    else "LOOSE" if HDRPAT.search(hn) else "VALUE")
            inst.append(dict(file=f.name, col=hn, form=form, rows=len(vals), resolved=nres,
                             has_rowid_col=bool(rowid_cols)))
    D = pd.DataFrame(inst)
    P(f"  scan time {time.time() - t0:.1f}s")
    P(f"  pointer INSTANCES (column x file): {len(D)}   over {D.file.nunique()} distinct files")
    P(f"  pointer ROWS                     : {D.rows.sum():,}   resolving: {D.resolved.sum():,} "
      f"({D.resolved.sum() / D.rows.sum():.4f})")
    for form in FORMS:
        s = D[D.form == form]
        P(f"    {form:7s} instances {len(s):4d}  files {s.file.nunique():4d}  rows {s.rows.sum():>9,}")
    return D


# ================================================================================================
# 2.  THE DP LADDER
# ================================================================================================
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
    if len(_SRC) > 400:
        _SRC.pop(next(iter(_SRC)))
    _SRC[key] = (h, rows)
    return h, rows


def nz(x, dp):
    """Idea 655's key cell normaliser with the decimal-places dial exposed.

    dp=10 is EXACTLY idea 655's `round(float(x), 10)`; dp=None keeps the canonical float repr
    (no rounding at all).  Non-numeric cells are keyed on their stripped string at every rung,
    so the dial can only move NUMERIC cells -- which is the point."""
    x = (x or "").strip()
    try:
        f = float(x)
    except Exception:
        return x
    return f if dp is None else round(f, dp)


UNIQUE, AMBIG, MISS, NOKEY, SINGLE, NONROW, UNRES = "UNIQUE AMBIG MISS NOKEY SINGLE NONROW UNRES".split()


def join_instance_ladder(hdr, data, ptrcol):
    """Classify every pointer row of one instance at EVERY dp rung in one pass.

    Returns (counts[dp][outcome], trans[(dp, outcome)] restricted to rows UNIQUE at dp=10,
             n_all5, n_rows)."""
    j = hdr.index(ptrcol)
    counts = {dp: collections.Counter() for dp in DPS}
    trans = collections.Counter()
    n_all5 = 0
    n_rows = 0
    bysrc = collections.defaultdict(list)
    flat = []                                        # dp-invariant rows
    for r in data:
        if j >= len(r) or not r[j].strip():
            continue
        n_rows += 1
        s = resolve(r[j])
        if s is None:
            flat.append(UNRES)
            continue
        bysrc[s].append(r)
    for s, rows in bysrc.items():
        if s.suffix.lower() != ".csv":
            flat.extend([NONROW] * len(rows))
            continue
        sh, sr = load_src(s)
        if sh is None:
            flat.extend([NONROW] * len(rows))
            continue
        if len(sr) <= 1:
            flat.extend([SINGLE] * len(rows))
            continue
        shared = [c for c in hdr if c != ptrcol and c.strip() in [x.strip() for x in sh]]
        if not shared:
            flat.extend([NOKEY] * len(rows))
            continue
        sn = [x.strip() for x in sh]
        si = [sn.index(c.strip()) for c in shared]
        ci = [hdr.index(c) for c in shared]
        # one source index per dp rung
        idxs = {}
        for dp in DPS:
            idxs[dp] = collections.Counter(
                tuple(nz(r[k], dp) if k < len(r) else "" for k in si) for r in sr)
        for r in rows:
            out = {}
            for dp in DPS:
                key = tuple(nz(r[k], dp) if k < len(r) else "" for k in ci)
                c = idxs[dp].get(key, 0)
                out[dp] = UNIQUE if c == 1 else (AMBIG if c > 1 else MISS)
                counts[dp][out[dp]] += 1
            if all(out[dp] == UNIQUE for dp in DPS):
                n_all5 += 1
            if out[10] == UNIQUE:
                for dp in DPS:
                    trans[(DPNAME[dp], out[dp])] += 1
    for o in flat:
        for dp in DPS:
            counts[dp][o] += 1
    # NOTE: SINGLE rows (source CSV has exactly one row) are trivially addressable at every
    # rung and are NOT folded into UNIQUE anywhere -- they are reported in their own column so
    # the transition population is EXACTLY the grid's dp10 UNIQUE count.
    return counts, trans, n_all5, n_rows


def run_ladder(D):
    P()
    P("=" * 100)
    P("(B) THE DP LADDER -- idea 655's join, re-read at 6 / 8 / 10 / 12 / FULL decimal places")
    P("=" * 100)
    recs, TR, t0 = [], collections.Counter(), time.time()
    for _, inst in D.iterrows():
        f = IDX.get(inst.file)
        if f is None:
            continue
        with open(f, newline="") as fh:
            rd = csv.reader(fh)
            hdr = next(rd)
            data = [r for r in rd]
        counts, trans, n_all5, n_rows = join_instance_ladder(hdr, data, inst.col)
        rec = dict(file=inst.file, col=inst.col, form=inst.form, rows=n_rows, all5_unique=n_all5)
        for dp in DPS:
            for o in (UNIQUE, AMBIG, MISS, NOKEY, SINGLE, NONROW, UNRES):
                rec[f"{DPNAME[dp]}_{o}"] = counts[dp][o]
        recs.append(rec)
        if inst.form in LADDER["VALUE"]:
            for k, v in trans.items():
                TR[k] += v
    J = pd.DataFrame(recs)
    P(f"  ladder time {time.time() - t0:.1f}s over {len(J)} instances")
    return J, TR


def grid(J):
    P()
    P("  THE 5 x 3 GRID -- every point reported (DP rung x pointer form)")
    rows = []
    for dp in DPS:
        for form in FORMS:
            s = J[J.form.isin(LADDER[form])]
            tot = s.rows.sum()
            r = dict(dp=DPNAME[dp], form=form, instances=len(s), files=s.file.nunique(),
                     rows=int(tot))
            for o in (UNIQUE, AMBIG, MISS, NOKEY, SINGLE, NONROW, UNRES):
                r[o.lower()] = int(s[f"{DPNAME[dp]}_{o}"].sum())
            r["unique_share"] = r["unique"] / tot if tot else np.nan
            r["all5_unique"] = int(s.all5_unique.sum())
            rows.append(r)
    G = pd.DataFrame(rows)
    P(G[["dp", "form", "instances", "rows", "unique", "unique_share", "ambig", "miss",
         "nokey", "all5_unique"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    return G


# ================================================================================================
# 3.  LIVE LEG -- the PRECISION dial on a book
# ================================================================================================
def fast_backtest(px, weights, freq=FREQ):
    """Vectorised twin of engine.backtest at ZERO cost (gate G1 checks the identity)."""
    rets = px.pct_change().fillna(0.0).values
    W = weights.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    n = len(px)
    A = np.cumprod(1.0 + rets, axis=0)
    A = np.vstack([np.ones((1, rets.shape[1])), A[:-1]])
    port = np.zeros(n); turn = np.zeros(n)
    cur = np.zeros(rets.shape[1])
    starts = np.flatnonzero(mask)
    for i0, i1 in zip(starts, list(starts[1:]) + [n]):
        w = W[i0]
        turn[i0] = np.abs(w - cur).sum()
        u = w[None, :] * (A[i0:i1] / A[i0][None, :])
        T = u.sum(axis=1) + (1.0 - w.sum())
        port[i0:i1] = (u * rets[i0:i1]).sum(axis=1) / T
        cur = (u[-1] * (1.0 + rets[i1 - 1])) / (T[-1] * (1.0 + port[i1 - 1]))
    return {"returns0": pd.Series(port, index=px.index),
            "turnover": pd.Series(turn, index=px.index)}


def net(res, bps):
    return res["returns0"] - res["turnover"] * bps / 1e4


def prec_weights(px, dp, n, tie, gross=GROSS, drop=()):
    """Top-n equal weight on the composite score ROUNDED TO dp DECIMALS (no vol scaler).

    dp=None -> the unrounded key.  ALPHA breaks ties by column order (deterministic);
    SPREAD holds every name tied at the top-n boundary, equal-weight, so no tie-break is
    made at all (the book can hold more than n names on a tied day)."""
    s, _, _ = score(px, vol_scale=False)
    if drop:
        s = s.drop(columns=[c for c in drop if c in s.columns])
    k = s if dp is None else s.round(dp)
    if tie == "ALPHA":
        r = k.rank(axis=1, ascending=False, method="first")
        w = (r <= n).astype(float) * (gross / n)
    else:
        r = k.rank(axis=1, ascending=False, method="min")
        sel = (r <= n).astype(float)
        cnt = sel.sum(axis=1).replace(0, np.nan)
        w = sel.div(cnt, axis=0).fillna(0.0) * gross
    return w.reindex(columns=px.columns).fillna(0.0)


def mstats(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def pass4a(d, b):
    return bool(d["H1"] > b["H1"] and d["H2"] > b["H2"] and d["MaxDD"] >= b["MaxDD"])


def pass4b(d, spy, oos_sh, spy_oos_sh):
    return bool(d["H1"] > spy["H1"] and d["H2"] > spy["H2"] and oos_sh > spy_oos_sh
                and d["MaxDD"] >= 0.60 * spy["MaxDD"] and d["CAGR"] >= 0.70 * spy["CAGR"])


def panels():
    out = {}
    px = load_universe()
    out["U56"] = (px, ())
    out["B136"] = (load_universe(broad=True), ())
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in sm.columns if c not in bad]
    out["SMALL439"] = (sm[keep], ("SPY",))
    for k, (p, d) in out.items():
        P(f"  {k:9s} {p.shape[1]:4d} cols  {p.index[0].date()} -> {p.index[-1].date()}  "
          f"({len(p)} rows)  non-selectable: {d or '-'}")
    return out


def gates(PX):
    P()
    P("=" * 100)
    P("GATES (run before any new number is read)")
    P("=" * 100)
    px = PX["U56"][0]
    w = rules_v2_weights(px)
    a = engine_backtest(px, w, cost_bps=0.0, freq=FREQ)["returns"]
    b = fast_backtest(px, w)["returns0"]
    st = px.index[260]
    g1 = float(np.nanmax(np.abs((a - b).loc[st:])))
    P(f"  G1 fast_backtest == engine.backtest (RULES v2, 0 bps, from warm-up) : {g1:.3e}")
    a25 = engine_backtest(px, w, cost_bps=25.0, freq=FREQ)["returns"].loc[st:]
    r25 = net(fast_backtest(px, w), 25.0).loc[st:]
    g2 = float(np.nanmax(np.abs(a25 - r25)))
    P(f"  G2 cost-rung identity r(25) = r(0) - turn*25/1e4 vs live engine(25)  : {g2:.3e}")
    # G3: the PRECISION book at FULL precision, n=5, gross 0.75, vol-scaled key IS rules_v1
    s, above, vol20 = score(px, vol_scale=True)
    elig = s.where(above & (vol20 < 0.60))
    wv1 = (elig.rank(axis=1, ascending=False) <= 5).astype(float) * 0.15
    g3 = float(np.abs(wv1 - rules_v1_weights(px)).max().max())
    P(f"  G3 ranking machinery reproduces baseline.rules_v1_weights            : {g3:.3e}")
    return dict(G1=g1, G2=g2, G3=g3)


def live(PX):
    P()
    P("=" * 100)
    P("(C) LIVE LEG -- the PRECISION dial on a book (top-n EW, gross 1.00, no vol scaler)")
    P("=" * 100)
    recs, wf, t0 = [], [], time.time()
    for pname in PANELS:
        px, drop = PX[pname]
        st = px.index[260]
        spy_r = px["SPY"].pct_change().fillna(0).loc[st:]
        spy = mstats(spy_r)
        spy_oos = metrics(spy_r.loc[OOS_START:])
        base_res = fast_backtest(px, rules_v2_weights(px))
        for rung in RUNGS:
            b = mstats(net(base_res, rung).loc[st:])
            b_oos = metrics(net(base_res, rung).loc[OOS_START:])
            P(f"\n  {pname} @ {int(rung)} bps   SPY {spy['CAGR']:.2%}/{spy['Sharpe']:.4f}/"
              f"{spy['MaxDD']:.2%} (H {spy['H1']:.4f}/{spy['H2']:.4f}, OOS Sh {spy_oos['Sharpe']:.4f})"
              f"   RULES v2 {b['CAGR']:.2%}/{b['Sharpe']:.4f}/{b['MaxDD']:.2%} "
              f"(OOS Sh {b_oos['Sharpe']:.4f})")
            recs.append(dict(panel=pname, rung=int(rung), tie="-", dp="SPY", n=0,
                             **spy, oos_Sharpe=spy_oos["Sharpe"], oos_CAGR=spy_oos["CAGR"],
                             oos_MaxDD=spy_oos["MaxDD"], p4a=False, p4b=False, is_Sharpe=np.nan))
            recs.append(dict(panel=pname, rung=int(rung), tie="-", dp="RULESv2", n=0,
                             **b, oos_Sharpe=b_oos["Sharpe"], oos_CAGR=b_oos["CAGR"],
                             oos_MaxDD=b_oos["MaxDD"], p4a=False, p4b=False, is_Sharpe=np.nan))
        cache = {}
        for tie in TIES:
            for dp in DPL:
                for n in NS:
                    w = prec_weights(px, dp, n, tie, drop=drop)
                    cache[(tie, dp, n)] = fast_backtest(px, w)
        for rung in RUNGS:
            b = mstats(net(base_res, rung).loc[st:])
            for tie in TIES:
                for dp in DPL:
                    for n in NS:
                        r = net(cache[(tie, dp, n)], rung)
                        d = mstats(r.loc[st:])
                        oos = metrics(r.loc[OOS_START:])
                        rec = dict(panel=pname, rung=int(rung), tie=tie,
                                   dp=("FULL" if dp is None else f"dp{dp}"), n=n, **d,
                                   oos_Sharpe=oos["Sharpe"], oos_CAGR=oos["CAGR"],
                                   oos_MaxDD=oos["MaxDD"],
                                   is_Sharpe=metrics(r.loc[st:IS_END])["Sharpe"],
                                   p4a=pass4a(d, b),
                                   p4b=pass4b(d, spy, oos["Sharpe"], spy_oos["Sharpe"]))
                        recs.append(rec)
        # ---- RULE 8: choose (dp, n) on IS only, read OOS once
        for rung in RUNGS:
            for tie in TIES:
                sub = [x for x in recs if x["panel"] == pname and x["rung"] == int(rung)
                       and x["tie"] == tie]
                pick = max(sub, key=lambda x: x["is_Sharpe"])
                b_oos = metrics(net(base_res, rung).loc[OOS_START:])
                wf.append(dict(panel=pname, rung=int(rung), tie=tie, pick_dp=pick["dp"],
                               pick_n=pick["n"], is_Sharpe=pick["is_Sharpe"],
                               oos_CAGR=pick["oos_CAGR"], oos_Sharpe=pick["oos_Sharpe"],
                               oos_MaxDD=pick["oos_MaxDD"],
                               v2_oos_Sharpe=b_oos["Sharpe"], v2_oos_CAGR=b_oos["CAGR"],
                               v2_oos_MaxDD=b_oos["MaxDD"],
                               spy_oos_Sharpe=spy_oos["Sharpe"], spy_oos_CAGR=spy_oos["CAGR"],
                               spy_oos_MaxDD=spy_oos["MaxDD"],
                               beats_spy_oos=pick["oos_Sharpe"] > spy_oos["Sharpe"],
                               beats_v2_oos=pick["oos_Sharpe"] > b_oos["Sharpe"],
                               p4a=pick["p4a"], p4b=pick["p4b"]))
    B = pd.DataFrame(recs)
    W = pd.DataFrame(wf)
    P(f"\n  live leg time {time.time() - t0:.1f}s   grid points {len(B[~B.dp.isin(['SPY','RULESv2'])])}")
    return B, W


# ================================================================================================
def main():
    global IDX, AMBIG_NAMES
    t00 = time.time()
    P("#" * 100)
    P("# Idea 660 -- is the KEY-UNIQUE join STABLE under float reformatting?   (cloud, 2026-09-10)")
    P("#" * 100)
    IDX, AMBIG_NAMES = build_index()

    PX = panels()
    G = gates(PX)

    D = census_pointers()
    J, TR = run_ladder(D)
    GR = grid(J)

    # ---- G5: only UNIQUE/AMBIG/MISS may move with dp
    inv = []
    for o in (NOKEY, SINGLE, NONROW, UNRES):
        vals = {DPNAME[dp]: int(J[f"{DPNAME[dp]}_{o}"].sum()) for dp in DPS}
        inv.append(len(set(vals.values())) == 1)
    P(f"\n  G5 dp-invariant outcomes (NOKEY/SINGLE/NONROW/UNRES) constant across rungs : "
      f"{'PASS' if all(inv) else 'FAIL'}")
    tot = {DPNAME[dp]: int(sum(J[f"{DPNAME[dp]}_{o}"].sum() for o in
                               (UNIQUE, AMBIG, MISS, NOKEY, SINGLE, NONROW, UNRES))) for dp in DPS}
    P(f"  G6 every row classified at every rung (row totals equal)                    : "
      f"{'PASS' if len(set(tot.values())) == 1 and list(tot.values())[0] == int(J.rows.sum()) else 'FAIL'}"
      f"   ({list(tot.values())[0]:,} rows)")

    # ---- PART B -- the answer
    P()
    P("=" * 100)
    P("(D) THE ANSWER -- what happens to idea 655's 198,353 KEY-UNIQUE rows")
    P("=" * 100)
    base = TR[("dp10", UNIQUE)]
    trows = []
    for dp in DPS:
        line = {o: TR[(DPNAME[dp], o)] for o in (UNIQUE, AMBIG, MISS)}
        s = sum(line.values())
        trows.append(dict(dp=DPNAME[dp], of=base, unique=line[UNIQUE], ambig=line[AMBIG],
                          miss=line[MISS],
                          kept=line[UNIQUE] / s if s else np.nan))
    T = pd.DataFrame(trows)
    P(f"  population = rows UNIQUE at the record's own rung (dp=10, FORM=VALUE): {base:,}")
    P(T.to_string(index=False, float_format=lambda x: f"{x:.6f}"))
    all5 = int(J[J.form.isin(LADDER["VALUE"])].all5_unique.sum())
    P(f"\n  UNIQUE at ALL FIVE rungs (6/8/10/12/FULL): {all5:,}  "
      f"({all5 / base:.6f} of the 655 population)")

    B, W = live(PX)
    P()
    P("  RULE 8 -- (dp, n) chosen on 2009-2016 by IS Sharpe, 2017+ read once:")
    P(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    grid_only = B[~B.dp.isin(["SPY", "RULESv2"])]
    P(f"\n  KEEP paths over ALL {len(grid_only)} grid points: 4a {int(grid_only.p4a.sum())}, "
      f"4b {int(grid_only.p4b.sum())}, BOTH "
      f"{int((grid_only.p4a & grid_only.p4b).sum())}")
    for pn in PANELS:
        s = grid_only[grid_only.panel == pn]
        P(f"    {pn:9s} 4a {int(s.p4a.sum()):3d}/{len(s)}   4b {int(s.p4b.sum()):3d}/{len(s)}")
    # DP-sensitivity of the BOOK (the live twin of the census question)
    P()
    P("  Does the BOOK move with its key's precision?  Sharpe spread across the dp ladder:")
    for pn in PANELS:
        for tie in TIES:
            s = grid_only[(grid_only.panel == pn) & (grid_only.tie == tie) & (grid_only.rung == 10)]
            for n in NS:
                q = s[s.n == n]
                P(f"    {pn:9s} {tie:6s} n={n:<3d} Sharpe {q.Sharpe.min():.4f}..{q.Sharpe.max():.4f}"
                  f"  spread {q.Sharpe.max() - q.Sharpe.min():.4f}   "
                  f"CAGR {q.CAGR.min():.2%}..{q.CAGR.max():.2%}")

    K = pd.DataFrame([dict(gate="G1_fast_vs_engine", value=G["G1"]),
                      dict(gate="G2_cost_rung", value=G["G2"]),
                      dict(gate="G3_rules_v1_repro", value=G["G3"]),
                      dict(gate="dp10_VALUE_unique", value=base),
                      dict(gate="unique_all5", value=all5)])
    P()
    dump(GR, "grid"); dump(T, "transition"); dump(J, "instances")
    dump(B, "books"); dump(W, "walkforward"); dump(K, "keeppaths")
    P(f"\n  total {time.time() - t00:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()

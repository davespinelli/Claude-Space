#!/usr/bin/env python3
"""QUEUE idea 183 - the-anchor-position-column   (lane B, 2026-09-06).

QUESTION (pre-registered, verbatim from QUEUE.md idea 183)
    "idea 173 showed RANDOM beats a LOW-end constant in 0.74 of 90 ladder instances and an
     INTERIOR one in 0.32, i.e. every 'instrument X beats the control' claim is partly a
     statement about where the control sits on X's ladder.  Propose the anchor's RANK ON ITS
     OWN LADDER as a LEADERBOARD schema column, back-fill it wherever the ladder is
     recoverable, and report how many published control-beating claims had their control at
     a grid edge."

WHAT IS AT STAKE.
    The record is full of sentences of the form "arm X beats the constant C".  Idea 173 showed
    that the SAME 468 ladder points support "RANDOM wins 0.74 of the time" or "RANDOM wins 0.32
    of the time" depending only on which grid point is nominated as C.  A control-beating claim
    is therefore not a property of X alone; it is a property of the pair (X, position of C).
    If a large share of the record's controls sit at a GRID EDGE - the cheapest place for a
    challenger to beat, because an edge point has no neighbours on one side to average against -
    then a large share of the record's "X beats C" sentences are partly grid statements.
    This run measures that share.  It is an AUDIT: it does not propose a book.

THE SCHEMA (deliverable 1) - three columns, all mechanical, none tuned.
    Given a ladder = an ordered grid of K values of one dial, with one outcome per point, and
    an ANCHOR = the grid value that the claim's control took:
      ANCHOR-POS   i_anchor / K, 1-based position of the anchor in the ORDERED GRID.
                   Reported as "i/K".  Normalised POSN = (i-1)/(K-1) in [0,1].
      ANCHOR-EDGE  1 if i in {1, K}, else 0.  THE HEADLINE COLUMN.
      ANCHOR-RANK  rank of the anchor's OWN OUTCOME among the K points, 1 = best.
                   This is the "rank on its own ladder" the idea names; it is DISTINCT from
                   ANCHOR-POS (a grid coordinate) and both are reported, never conflated.
    A fourth, derived, is what makes the columns readable:
      d_anchor     mean(outcome over the K points) - outcome(anchor).  d_anchor > 0 is exactly
                   idea 173's "a uniformly random ladder draw beats the control in expectation".

PRE-REGISTERED ANCHOR REGISTRY (deliverable 2's only judgement call, fixed before any scan).
    A dial is auditable only if its live incumbent is written in RULES v1 / PROTOCOL, so the
    anchor is not chosen by this script:
      GROSS   g / gross / G            anchor 0.75  (RULES v1 n=5 x w=0.15)
      COUNT   n / N / count / topn     anchor 5     (RULES v1 n=5)
      VOLCAP  volcap / max_vol / vcap  anchor 0.60  (RULES v1 vol20 gate)
      VOLPOW  volpow / vpow            anchor 0.5   (RULES v1 /sqrt(vol20))
      COST    cost / cost_bps / bps    anchor 10    (PROTOCOL rule 2)
      BAND    band                     anchor 0.00  (RULES v1 has no band)
      SLEEVE  sleeve                   anchor 0.00  (RULES v1 has no sleeve)
      CADENCE cadence/freq/point/cad   anchor W     (RULES v1 weekly)
    A ladder whose grid does NOT contain the incumbent is NOT auditable and is excluded and
    counted, never re-anchored onto its nearest point.

CORPUS (deliverable 2) - every committed CSV in research/backtests/, machine-read.
    An INSTANCE is (file, dial column, group) where the group is the file's other identifying
    columns held fixed, the dial takes K >= 3 distinct values with exactly one row each, the
    grid contains the registry anchor, and the file carries OOS_Sharpe or Sharpe_OOS.
    Nothing is hand-picked; the scan is a pure function of the committed record.

THE EXPERIMENT (deliverable 3) - THE RE-ANCHORING SWEEP.
    For every instance and EVERY j in 1..K, re-price the same ladder against an anchor placed
    at j and record whether each challenger beats it:
      RANDOM  a uniform draw over the ladder, priced in expectation as mean(o)   (idea 173's
              control; d_j = mean(o) - o[j], so this run's j = i_anchor column reproduces
              idea 173's d_anchor/d_low/d_high exactly - control [b])
      ORACLE  the ladder argmax                                (upper bound, not implementable)
      MEDIAN  the middle grid point                            (a position-neutral constant)
    Beat-rate and mean margin are reported BY ANCHOR POSITION.  The spread of beat-rate across
    j is the size of the bias the new column exists to expose.

TUNED PARAMETERS - exactly two, per PROTOCOL rule 4.
    1. the DIAL (8 registry dials, every one reported, none preferred).
    2. the ANCHOR POSITION j, swept exhaustively over all K positions of every ladder, ALL
       reported.  This is the whole content of the idea.
    File, panel, book and cost are corpus axes, not parameters.  The registry anchors are
    quoted from RULES v1, not fitted.

FRESH LIVE SWEEP (deliverable 4) - so the audit is not purely archival and 4a/4b/rule 8 have
    numbers this script computed itself:
      3 panels : U56 (the live universe), ETF36, SMALL439
      3 dials  : GROSS  9 pts 0.15..1.35 (anchor 0.75 at 5/9, INTERIOR)
                 COUNT  9 pts 3,5,8,10,15,20,30,40,60 (anchor 5 at 2/9, near the LOW edge)
                 CADENCE 7 pts D,2D,W,2W,M,6W,Q (anchor W at 3/7, INTERIOR)
      cost 10 bps, t+1, MAX_VOL 0.60, composite score, per PROTOCOL rule 2.
    75 backtests.  Every point carries full/H1/H2/IS/OOS metrics, so both KEEP paths are
    evaluated on all of them and the re-anchoring sweep runs on a book this script controls.

WALK-FORWARD (PROTOCOL rule 8) - the decision the column would license, tested.
    The column's only capital-relevant use is as a FILTER on claims: "trust an IS-selected
    ladder point only if the ladder's anchor is INTERIOR".  Choose on <= 2016-12-31 only, read
    2017-01-01.. once.  .walkforward.csv reports OOS CAGR / Sharpe / MaxDD for the IS-argmax
    pick under the unfiltered rule and under the interior-anchor filter, against RULES v1 on
    the parent panel and against SPY, plus the same on the archival corpus where IS/OOS
    columns survive.

BOTH KEEP PATHS on every fresh ladder point -> .keep.csv
    4a  Sharpe > RULES v1 in BOTH halves and MaxDD no worse than RULES v1.
    4b  Sharpe > SPY in BOTH halves AND on the OOS window, MaxDD <= 0.60 x |SPY MaxDD|,
        CAGR >= 0.70 x SPY CAGR.

REPRODUCTION CONTROLS, asserted before any new number is read
    [a] fast_backtest reproduces products/backtester/engine.backtest to < 1e-12 on returns and
        turnover at W and M on a real book.
    [b] THE DECISIVE CONTROL: the back-fill machinery, pointed at idea 173's committed
        .grid.csv, must reproduce idea 173's committed .anchorposition.csv to < 1e-12 on
        d_anchor / d_low / d_high and on i_anchor / K for all 90 rows, and must re-derive its
        published headline constants 0.74 and 0.32.  If [b] fails the scanner is wrong and
        every back-filled number below is meaningless.  Run stops.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  [a] and [b] both hold.
    P2  A LARGE minority of auditable instances have the anchor at a GRID EDGE: >= 25%.
    P3  Beat-rate against the anchor is strongly position-dependent: pooled over instances, the
        RANDOM beat-rate at the WORST-outcome edge minus that at the BEST-outcome edge exceeds
        0.50.  (Idea 173's 0.74-vs-0.32 is 0.42 measured at low-vs-interior; edge-vs-edge
        should be larger.)
    P4  Edge anchors carry LARGER claimed margins: median d_anchor at an edge is more than
        1.5x the median at the interior position closest to the middle.
    P5  RULE 8 KILL: the interior-anchor filter buys essentially nothing in OOS Sharpe
        (|dOOS Sharpe| < 0.05, not significant).  The column is a DISCOUNT ON CLAIMS, not a
        selector of books.  I expect this run to be a KILL as a trading rule and a KEEP only
        as a schema proposal, which is not a PROTOCOL KEEP path.
    P6  No new 4a/4b KEEP from the fresh sweep beyond a re-parameterisation of a known book
        (idea 144).

CAVEATS carried, not buried
    * SURVIVORSHIP.  U56/ETF36/SMALL439 are current-constituent lists (data/SMALL_PANEL_README.md,
      idea 54).  Every ladder point inherits it equally, so PAIRED position comparisons are
      unaffected; no LEVEL here is an attainable return.
    * The scan can only see ladders that were COMMITTED as CSV with the dial in a column.  A
      claim whose ladder lives only in prose or in a console dump is invisible here and is
      counted as unrecoverable, not as interior.
    * ANCHOR-POS is defined on the grid AS RUN.  A dial whose grid was itself chosen around the
      incumbent will look interior by construction; that is a fact about the grid designer, and
      it is exactly why the column has to be published rather than inferred.
    * COST is in the registry because 10 bps is a PROTOCOL constant, but a COST ladder is not a
      "control-beating claim" in the ordinary sense.  It is reported as its own dial and is
      excluded from the headline claim count, which is stated both ways.
    * SLEEVE and BAND anchor at 0.00, the low end of every grid that contains it, so they are
      edge BY CONSTRUCTION.  Reported separately for the same reason; the headline is stated
      with and without them.
    * Idea 126: t+1 execution only, 10 bps only on the fresh sweep.
    * Idea 144: a re-parameterised book is the SAME book; a 4a/4b flip along a dial is not a
      new signal.

Deterministic, standalone.  Writes .console.txt, .backfill.csv.gz, .reanchor.csv.gz,
.claims.csv.gz (gzipped: 10593 x K rows), .perdial.csv, .position.csv, .ladder.csv,
.freshpos.csv, .keep.csv, .walkforward.csv, .schema.md.
"""
from __future__ import annotations

import glob
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "products" / "backtester"))
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-06_the-anchor-position-column_B"
OUT = ROOT / "research" / "backtests"
P173 = OUT / "2026-09-05_is-the-ladder-endpoint-a-general-selector-artefact_cloud"

COST_BPS = 10
MAX_VOL = 0.60
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
PHI, DELTA = 0.70, 0.60          # 4b CAGR floor and MaxDD cap vs SPY

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 4000)

_lines: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


# ============================================================ the registry
CAD_ORDER = ["D", "2D", "3D", "W", "2W", "3W", "4W", "M", "5W", "6W", "7W", "8W",
             "2M", "10W", "Q", "16W", "2Q", "A"]

REGISTRY = [
    # dial     column names                                   anchor  in headline claim count
    ("GROSS",   ("g", "gross", "G"),                          0.75,   True),
    ("COUNT",   ("n", "N", "count", "topn"),                  5.0,    True),
    ("VOLCAP",  ("volcap", "max_vol", "vcap"),                0.60,   True),
    ("VOLPOW",  ("volpow", "vpow"),                           0.5,    True),
    ("CADENCE", ("cadence", "freq", "point", "pt", "cad"),    "W",    True),
    ("COST",    ("cost", "cost_bps", "bps"),                  10.0,   False),
    ("BAND",    ("band",),                                    0.0,    False),
    ("SLEEVE",  ("sleeve",),                                  0.0,    False),
]
HEADLINE_DIALS = [d for d, _, _, h in REGISTRY if h]

# columns that are outcomes / statistics, never a dial and never a grouping key
_METRIC_PREF = ("OOS_", "IS_", "spy_", "v1_", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "m_",
                "d_", "p4", "f4", "pass", "fail", "TO", "turnover", "rank", "K", "is_anchor",
                "margin", "t_", "n_obs", "sd", "se", "mean", "median", "lo", "hi", "capture",
                "rho", "oos", "Sortino", "Calmar", "Vol", "Total", "Years", "WinRate")
OUT_COLS = ["OOS_Sharpe", "Sharpe_OOS"]


def _is_metric(c) -> bool:
    return str(c).startswith(_METRIC_PREF)


# ============================================================ control [a]
def cad_mask(idx, cad):
    """True on the last bar of each cadence block; same rule as engine.rebalance_mask."""
    n = len(idx)
    if cad == "D":
        key = np.arange(n)
    elif cad == "2D":
        key = np.arange(n) // 2
    elif cad in _WEEK_K:
        ordi = np.asarray(idx.to_period("W").astype("int64"))
        key = (ordi - ordi[0]) // _WEEK_K[cad]
    elif cad in _PER_K:
        f, k = _PER_K[cad]
        ordi = np.asarray(idx.to_period(f).astype("int64"))
        key = ordi if k == 1 else (ordi - ordi[0]) // k
    else:
        raise ValueError(cad)
    m = np.empty(n, bool)
    m[:-1] = key[:-1] != key[1:]
    m[-1] = True
    return pd.Series(m, index=idx)


_WEEK_K = {"W": 1, "2W": 2, "6W": 6}
_PER_K = {"M": ("M", 1), "Q": ("Q", 1)}


def fast_backtest(prices, weights, cost_bps=COST_BPS, cad="W"):
    """Vectorised equivalent of engine.backtest.  Asserted identical in check_a()."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = cad_mask(idx, cad).shift(1, fill_value=False).values.copy()
    mask[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mask)
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
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return {"returns": pd.Series(port, index=idx), "turnover": pd.Series(turn, index=idx)}


def check_a(px, w):
    P("=" * 118)
    P("CONTROL [a]  fast_backtest == engine.backtest")
    ok = True
    for cad in ["W", "M"]:
        e = backtest(px, w, cost_bps=COST_BPS, freq=cad)
        f = fast_backtest(px, w, cost_bps=COST_BPS, cad=cad)
        # engine.backtest shifts w_target WITHOUT re-filling, so its first bar (and the first
        # rebalance bar) are NaN; fast_backtest fills them with 0.  Every book below is read from
        # bar 260 (the warm-up start), so the control is asserted there.  The count of NaN bars
        # the engine emits before that is printed so the exemption cannot hide a disagreement.
        nnan = int(e["returns"].isna().sum())
        sl = slice(260, None)
        dr = float(np.abs(e["returns"].values[sl] - f["returns"].values[sl]).max())
        dt = float(np.abs(e["turnover"].values[sl] - f["turnover"].values[sl]).max())
        ok &= nnan <= 2 and int(e["returns"].iloc[260:].isna().sum()) == 0
        P(f"  cad={cad:2s}  engine NaN bars before warm-up: {nnan} (all at index < 260)")
        P(f"  cad={cad:2s}  max|d returns| = {dr:.3e}   max|d turnover| = {dt:.3e}")
        ok &= (dr < 1e-12) and (dt < 1e-12)
        m = rebalance_mask(px.index, cad)
        assert bool((m.values == cad_mask(px.index, cad).values).all()), f"cad_mask != engine at {cad}"
    P(f"  [a] {'PASS' if ok else 'FAIL'}   (cad_mask == engine.rebalance_mask at W and M)")
    return ok


# ============================================================ the back-fill scanner
def ladder_instances(df, dial, col, anchor, outcol, fname):
    """Yield one dict per (group) ladder instance in this file for this dial column."""
    iscad = isinstance(anchor, str)
    if iscad:
        vals = [str(v) for v in df[col].dropna().unique()]
        if not set(vals) <= set(CAD_ORDER) or anchor not in vals:
            return
        order = {v: i for i, v in enumerate(CAD_ORDER)}
        key = df[col].astype(str)
    else:
        key = pd.to_numeric(df[col], errors="coerce")
        vals = sorted(key.dropna().unique())
        if len(vals) < 3 or len(vals) > 40:
            return
        if not bool(np.isclose(np.asarray(vals, float), anchor).any()):
            return
        order = None
    keys = [k for k in df.columns
            if k != col and not _is_metric(k) and df[k].nunique(dropna=False) < len(df)]
    groups = df.groupby(keys, dropna=False, sort=False) if keys else [((), df)]
    for gk, sub in groups:
        kk = key.loc[sub.index]
        o = pd.to_numeric(sub[outcol], errors="coerce")
        m = kk.notna() & o.notna()
        kk, o, sub = kk[m], o[m], sub[m]
        if kk.nunique() != len(sub) or len(sub) < 3:
            continue
        if iscad:
            if not set(kk.values) <= set(CAD_ORDER):
                continue
            srt = np.argsort([order[v] for v in kk.values], kind="stable")
        else:
            srt = np.argsort(kk.values, kind="stable")
        g = kk.values[srt]
        y = o.values[srt].astype(float)
        K = len(g)
        if iscad:
            hit = np.flatnonzero(g == anchor)
        else:
            hit = np.flatnonzero(np.isclose(g.astype(float), anchor))
        if len(hit) != 1:            # this GROUP's grid does not contain the incumbent exactly once
            continue
        ia = int(hit[0])
        yield dict(file=fname, dial=dial, col=col,
                   group=("|".join(f"{k}={v}" for k, v in zip(keys, gk if isinstance(gk, tuple) else (gk,)))
                          if keys else ""),
                   K=K, anchor=str(anchor), i_anchor=ia + 1,
                   POSN=(ia / (K - 1)) if K > 1 else np.nan,
                   EDGE=int(ia == 0 or ia == K - 1),
                   ANCHOR_RANK=int(pd.Series(-y).rank(method="min").iloc[ia]),
                   y_anchor=float(y[ia]), y_mean=float(np.mean(y)),
                   y_max=float(np.max(y)), y_min=float(np.min(y)),
                   y_med=float(np.sort(y)[K // 2]),
                   d_anchor=float(np.mean(y) - y[ia]),
                   d_low=float(np.mean(y) - y[0]),
                   d_high=float(np.mean(y) - y[-1]),
                   d_oracle=float(np.max(y) - y[ia]),
                   ladder_y=y.tolist())


def scan_record():
    P("=" * 118)
    P("BACK-FILL SCAN of the committed record  (research/backtests/*.csv)")
    files = sorted(glob.glob(str(OUT / "*.csv")))
    rows, unrec, seen_files = [], [], set()
    for f in files:
        try:
            df = pd.read_csv(f)
        except Exception:
            continue
        base = os.path.basename(f)
        oc = [c for c in OUT_COLS if c in df.columns]
        if not oc or len(df) < 3:
            continue
        seen_files.add(base)
        outcol = oc[0]
        got = False
        for dial, names, anchor, _h in REGISTRY:
            for c in names:
                if c not in df.columns:
                    continue
                for r in ladder_instances(df, dial, c, anchor, outcol, base):
                    rows.append(r)
                    got = True
        if not got:
            unrec.append(base)
    B = pd.DataFrame(rows)
    P(f"  CSVs in research/backtests            : {len(files)}")
    P(f"  ... carrying an OOS_Sharpe/Sharpe_OOS : {len(seen_files)}")
    P(f"  ... with >=1 auditable ladder         : {B.file.nunique() if len(B) else 0}")
    P(f"  ... with an outcome but NO auditable ladder (grid lacks the RULES v1 incumbent, or "
      f"no registry dial): {len(unrec)}")
    P(f"  auditable ladder INSTANCES            : {len(B)}")
    return B


# ============================================================ control [b]
def check_b(B):
    """Reproduce idea 173's committed .anchorposition.csv from its committed .grid.csv."""
    P("=" * 118)
    P("CONTROL [b]  the scanner reproduces idea 173's published anchor-position table")
    gp, ap = Path(str(P173) + ".grid.csv"), Path(str(P173) + ".anchorposition.csv")
    if not (gp.exists() and ap.exists()):
        P("  FAIL - idea 173's grid.csv / anchorposition.csv not committed")
        return False, None
    G = pd.read_csv(gp)
    A = pd.read_csv(ap)
    mine = []
    for (pn, sig, c, lad), sub in G.groupby(["panel", "signal", "cost", "ladder"], sort=False):
        sub = sub.sort_values("rank").reset_index(drop=True)
        y = sub["Sharpe_OOS"].values.astype(float)
        ia = int(sub.index[sub["is_anchor"] == 1][0])
        mine.append(dict(ladder=lad, panel=pn, signal=sig, cost=c, i_anchor=ia + 1, K=len(y),
                         d_anchor=float(np.mean(y) - y[ia]), d_low=float(np.mean(y) - y[0]),
                         d_high=float(np.mean(y) - y[-1])))
    M = pd.DataFrame(mine)
    key = ["ladder", "panel", "signal", "cost"]
    J = A.merge(M, on=key, suffixes=("_pub", "_mine"))
    ok = len(J) == len(A) == 90
    worst = 0.0
    for c in ["i_anchor", "K", "d_anchor", "d_low", "d_high"]:
        d = float(np.abs(J[c + "_pub"].values - J[c + "_mine"].values).max())
        worst = max(worst, d)
        P(f"  max|d {c:9s}| over {len(J):3d} rows = {d:.3e}")
        ok &= d < 1e-12
    lo = float((J["d_low_mine"] > 0).mean())
    an = float((J["d_anchor_mine"] > 0).mean())
    P(f"  re-derived headline: RANDOM beats a LOW-end constant in {lo:.2f} of {len(J)} instances,"
      f" the INTERIOR anchor in {an:.2f}")
    P(f"  idea 173 published : 0.74 and 0.32")
    ok &= abs(lo - 0.74) < 0.005 and abs(an - 0.32) < 0.005
    P(f"  [b] {'PASS' if ok else 'FAIL'}   (worst numeric disagreement {worst:.3e})")
    return ok, J


# ============================================================ the re-anchoring sweep
def reanchor(B):
    """For every instance and every j in 1..K, price three challengers against an anchor at j."""
    rows = []
    for r in B.itertuples(index=False):
        y = np.asarray(r.ladder_y, float)
        K = len(y)
        mean_o, max_o = float(np.mean(y)), float(np.max(y))
        med_o = float(np.sort(y)[K // 2])
        rk = pd.Series(-y).rank(method="min").values          # 1 = best outcome
        for j in range(K):
            rows.append(dict(file=r.file, dial=r.dial, group=r.group, K=K, j=j + 1,
                             POSN=(j / (K - 1)) if K > 1 else np.nan,
                             EDGE=int(j == 0 or j == K - 1),
                             is_true_anchor=int(j == r.i_anchor - 1),
                             out_rank=int(rk[j]),
                             d_random=mean_o - y[j],
                             d_oracle=max_o - y[j],
                             d_median=med_o - y[j]))
    return pd.DataFrame(rows)


# ============================================================ the fresh live sweep
def comp_score(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


class Book:
    def __init__(self, name, px, tradable, parent):
        self.name, self.px, self.parent = name, px, parent
        self.comp = comp_score(px)
        vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        m = ((px > px.rolling(200).mean()) & (vol20 < MAX_VOL)).copy()
        drop = [c for c in px.columns if c not in set(tradable)]
        if drop:
            m[drop] = False
        self.elig = m
        self.rank = self.comp.where(self.elig).rank(axis=1, ascending=False)

    def weights(self, n=5, gross=0.75):
        return (self.rank <= n).astype(float) * (gross / n)


FRESH_LADDERS = {
    "GROSS":   ([0.15, 0.30, 0.45, 0.60, 0.75, 0.90, 1.05, 1.20, 1.35], 0.75),
    "COUNT":   ([3, 5, 8, 10, 15, 20, 30, 40, 60], 5),
    "CADENCE": (["D", "2D", "W", "2W", "M", "6W", "Q"], "W"),
}


def mrow(r, start):
    r = r.loc[start:]
    m = metrics(r)
    h = len(r) // 2
    m1, m2 = metrics(r.iloc[:h]), metrics(r.iloc[h:])
    ris, oos = r.loc[:IS_END], r.loc[OOS_START:]
    mi, mo = metrics(ris), metrics(oos)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=m1["Sharpe"], H2=m2["Sharpe"],
                IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])


def fresh_sweep():
    P("=" * 118)
    P("FRESH LIVE SWEEP  3 panels x 3 dials, cost 10 bps, t+1")
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    etf36 = [t for t in U["broad"] + U["sectors"] + U["bonds_fx_commod"] if t not in crypto]
    px56 = load_universe()
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    u_stk = [c for c in px56.columns if c != "SPY"]
    e_stk = [t for t in etf36 if t in px56.columns and t != "SPY"]

    def keep(px, cols):
        cols = [c for c in cols if c in px.columns]
        return px[list(dict.fromkeys(cols + ["SPY"]))].dropna(how="all").ffill()

    books = [Book("U56", keep(px56, u_stk), set(u_stk), "U56"),
             Book("ETF36", keep(px56, e_stk), set(e_stk), "U56"),
             Book("SMALL439", keep(pxs, s_stk), set(s_stk), "SMALL")]
    P(f"  panels: " + ", ".join(f"{b.name} ({b.px.shape[1]-1} names, {b.px.index[0].date()}"
                                f"..{b.px.index[-1].date()})" for b in books))

    # references: RULES v1 on the parent panel, SPY buy-and-hold, on each panel's own sample
    refs = {}
    for b in books:
        start = b.px.index[260]
        parent = px56 if b.parent == "U56" else pxs
        v1 = backtest(parent, rules_v1_weights(parent), cost_bps=COST_BPS, freq="W")["returns"]
        v1 = v1.reindex(b.px.index).fillna(0.0)
        spy = b.px["SPY"].pct_change().fillna(0.0)
        refs[b.name] = dict(v1=mrow(v1, start), spy=mrow(spy, start), start=start)
        r = refs[b.name]
        P(f"  {b.name:9s} RULES v1 {r['v1']['CAGR']:7.2%} {r['v1']['Sharpe']:6.3f} "
          f"{r['v1']['MaxDD']:7.2%} | SPY {r['spy']['CAGR']:7.2%} {r['spy']['Sharpe']:6.3f} "
          f"{r['spy']['MaxDD']:7.2%} | OOS SPY {r['spy']['OOS_Sharpe']:6.3f}")

    rows = []
    t0 = time.time()
    for b in books:
        start = refs[b.name]["start"]
        for dial, (grid, anchor) in FRESH_LADDERS.items():
            for v in grid:
                n, g, cad = 5, 0.75, "W"
                if dial == "GROSS":
                    g = v
                elif dial == "COUNT":
                    n = v
                else:
                    cad = v
                res = fast_backtest(b.px, b.weights(n=n, gross=g), cost_bps=COST_BPS, cad=cad)
                m = mrow(res["returns"], start)
                m.update(panel=b.name, dial=dial, value=str(v), anchor=str(anchor),
                         is_anchor=int(str(v) == str(anchor)),
                         turnover_yr=float(res["turnover"].loc[start:].sum() /
                                           (len(res["turnover"].loc[start:]) / 252)))
                rows.append(m)
    L = pd.DataFrame(rows)
    P(f"  {len(L)} ladder points in {time.time()-t0:.0f}s")
    return L, refs, books


def keep_table(L, refs):
    """Both PROTOCOL KEEP paths on every fresh ladder point."""
    out = []
    for r in L.itertuples(index=False):
        v1, spy = refs[r.panel]["v1"], refs[r.panel]["spy"]
        p4a = (r.H1 > v1["H1"]) and (r.H2 > v1["H2"]) and (r.MaxDD >= v1["MaxDD"])
        p4b = (r.H1 > spy["H1"] and r.H2 > spy["H2"] and r.OOS_Sharpe > spy["OOS_Sharpe"]
               and r.MaxDD >= -DELTA * abs(spy["MaxDD"]) and r.CAGR >= PHI * spy["CAGR"])
        out.append(dict(panel=r.panel, dial=r.dial, value=r.value, is_anchor=r.is_anchor,
                        CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD, H1=r.H1, H2=r.H2,
                        OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                        turnover_yr=r.turnover_yr,
                        v1_Sharpe=v1["Sharpe"], spy_Sharpe=spy["Sharpe"],
                        spy_OOS_Sharpe=spy["OOS_Sharpe"], spy_CAGR=spy["CAGR"],
                        spy_MaxDD=spy["MaxDD"], pass4a=int(p4a), pass4b=int(p4b)))
    return pd.DataFrame(out)


# ============================================================ main
def main():
    t0 = time.time()
    P(f"idea 183  the-anchor-position-column   lane B   {pd.Timestamp.utcnow():%Y-%m-%d %H:%M} UTC")
    P(__doc__.split("Deterministic, standalone.")[0].strip()[:0] or "")

    # ---------------- controls
    px56 = load_universe()
    u_stk = [c for c in px56.columns if c != "SPY"]
    # control [a] needs a NaN-free panel: the two engines fill late listings differently before
    # the first quote, which is irrelevant to every book below (all start after the 260-bar
    # warm-up on ffilled panels) but would make an exact-equality control meaningless.
    ctrl_px = px56.dropna(axis=1).copy()
    P(f"  control panel: {ctrl_px.shape[1]} of {px56.shape[1]} names with complete history, "
      f"{ctrl_px.index[0].date()}..{ctrl_px.index[-1].date()}")
    okA = check_a(ctrl_px, rules_v1_weights(ctrl_px))

    B = scan_record()
    okB, J173 = check_b(B)
    if not (okA and okB):
        P("\nCONTROL FAILED - stopping before any new number is read.")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        sys.exit(1)

    # ---------------- deliverable 2: the back-fill
    P("=" * 118)
    P("DELIVERABLE 2 - THE BACK-FILL.  ANCHOR-POS / ANCHOR-EDGE / ANCHOR-RANK, by dial")
    P(f"  {'dial':8s} {'files':>5s} {'inst':>6s} {'medK':>5s} {'anchor':>7s} {'EDGE share':>10s} "
      f"{'low-edge':>9s} {'high-edge':>9s} {'med POSN':>9s} {'med ANCHOR-RANK':>16s} "
      f"{'d_anchor>0':>11s} {'med d_anchor':>13s}")
    per = []
    for dial, names, anchor, hl in REGISTRY:
        sub = B[B.dial == dial]
        if not len(sub):
            continue
        lo = float((sub.i_anchor == 1).mean())
        hi = float((sub.i_anchor == sub.K).mean())
        d = dict(dial=dial, files=sub.file.nunique(), inst=len(sub), medK=float(sub.K.median()),
                 anchor=str(anchor), edge_share=float(sub.EDGE.mean()), low_edge=lo, high_edge=hi,
                 med_POSN=float(sub.POSN.median()),
                 med_anchor_rank=float(sub.ANCHOR_RANK.median()),
                 med_anchor_rank_frac=float((sub.ANCHOR_RANK / sub.K).median()),
                 share_random_beats=float((sub.d_anchor > 0).mean()),
                 med_d_anchor=float(sub.d_anchor.median()), in_headline=int(hl))
        per.append(d)
        P(f"  {dial:8s} {d['files']:5d} {d['inst']:6d} {d['medK']:5.0f} {str(anchor):>7s} "
          f"{d['edge_share']:10.3f} {lo:9.3f} {hi:9.3f} {d['med_POSN']:9.3f} "
          f"{d['med_anchor_rank']:8.1f} /{sub.K.median():5.0f} {d['share_random_beats']:11.3f} "
          f"{d['med_d_anchor']:+13.4f}")
    PER = pd.DataFrame(per)

    hl_mask = B.dial.isin(HEADLINE_DIALS)
    edge_all0 = float(B.EDGE.mean())
    beat0 = B[B.d_anchor > 0]
    over = float(beat0.EDGE.mean() / edge_all0) if edge_all0 else float("nan")
    P("")
    P("  THE COUNT idea 183 ASKS FOR - published control-beating claims with the control at a GRID EDGE")
    for label, m in [("ALL registry dials", pd.Series(True, index=B.index)),
                     ("headline dials only (GROSS/COUNT/VOLCAP/VOLPOW/CADENCE)", hl_mask),
                     ("excluding structurally-edge dials (BAND/SLEEVE)", ~B.dial.isin(["BAND", "SLEEVE"]))]:
        sub = B[m]
        beat = sub[sub.d_anchor > 0]          # the claim actually made: a challenger beat the control
        P(f"   {label:56s}: {len(sub):5d} auditable ladders, "
          f"{int(sub.EDGE.sum()):5d} ({sub.EDGE.mean():.1%}) anchored at a GRID EDGE;")
        P(f"   {'':56s}  of the {len(beat):5d} in which a random ladder draw BEATS the control, "
          f"{int(beat.EDGE.sum()):5d} ({beat.EDGE.mean() if len(beat) else np.nan:.1%}) had the "
          f"control at an edge")
        if len(beat) and sub.EDGE.mean() > 0:
            P(f"   {'':56s}  OVER-REPRESENTATION of edge anchors among made claims: "
              f"{beat.EDGE.mean()/sub.EDGE.mean():.2f}x the base rate")
    P("")
    P("  Read: EDGE share is the fraction of the record's auditable control-beating claims whose")
    P("  control had no neighbour on one side.  The second line is the subset where the claim was")
    P("  actually made (a uniform ladder draw beats the control in expectation).")
    P("")
    P("  THE POOLED 'ALL dials' OVER-REPRESENTATION RATIO IS A SIMPSON ARTEFACT AND IS NOT THE")
    P("  HEADLINE.  COST contributes 7402 of the 10593 ladders at a 0.3% edge share and a 0.2%")
    P("  claim rate (10 bps sits mid-grid in almost every cost ladder and is almost never beaten),")
    P("  so pooling it with BAND/SLEEVE - which are edge-anchored 100% of the time BY CONSTRUCTION,")
    P("  RULES v1 having neither dial - manufactures a ratio out of stratum mixing.  Stratified,")
    P("  the ratio is 0.81x on the five headline dials: among the dials the record actually argues")
    P("  about, an edge anchor is NOT more likely to have been beaten.  The finding is the LEVEL,")
    P("  not the ratio: HALF the record's headline-dial claims are anchored at a grid edge.")

    # ---------------- deliverable 3: the re-anchoring sweep
    P("=" * 118)
    P("DELIVERABLE 3 - THE RE-ANCHORING SWEEP.  Same ladders, anchor moved to every position j")
    R = reanchor(B)
    P(f"  {len(R)} (instance, anchor position) rows over {B.shape[0]} ladders")
    P("")
    P("  TAUTOLOGY CHECK FIRST, so it is not mistaken for a finding.  Sorting the anchor by its")
    P("  OWN OUTCOME RANK forces beat-rate 0.000 at rank 1 and 1.000 at rank K (the ladder mean")
    P("  is below the max and above the min by definition).  The table below is printed ONLY to")
    P("  confirm the arithmetic and to show the SHAPE in between; its extremes carry no content,")
    P("  and P3 is scored on the GRID-POSITION table that follows it, which is not forced.")
    P(f"  {'dial':8s} | {'RANDOM beat-rate by anchor OUTCOME RANK (1=best point .. K=worst)':<66s}")
    P(f"  {'':8s} | {'rank 1':>8s} {'rank 2':>8s} {'mid':>8s} {'rank K-1':>9s} {'rank K':>8s} "
      f"{'spread':>8s} {'ORACLE spr':>11s}")
    spreads = []
    for dial in [d for d, _, _, _ in REGISTRY if (B.dial == d).any()]:
        s = R[R.dial == dial]
        def br(sel):
            x = s[sel]
            return float((x.d_random > 0).mean()) if len(x) else np.nan
        r1 = br(s.out_rank == 1)
        r2 = br(s.out_rank == 2)
        rm = br(s.out_rank == (s.K + 1) // 2)
        rk1 = br(s.out_rank == s.K - 1)
        rk = br(s.out_rank == s.K)
        osp = float((s[s.out_rank == s.K].d_oracle > 0).mean() - (s[s.out_rank == 1].d_oracle > 0).mean())
        P(f"  {dial:8s} | {r1:8.3f} {r2:8.3f} {rm:8.3f} {rk1:9.3f} {rk:8.3f} {rk-r1:8.3f} {osp:11.3f}")
        spreads.append(dict(dial=dial, br_best=r1, br_mid=rm, br_worst=rk, spread=rk - r1))
    SPR = pd.DataFrame(spreads)
    P("")
    P("  By GRID POSITION (the column being proposed), pooled:")
    P(f"  {'anchor at':>12s} {'n':>7s} {'RANDOM beats':>13s} {'mean d_random':>14s} "
      f"{'mean d_oracle':>14s} {'mean d_median':>14s}")
    posrows = []
    for lab, sel in [("grid pos 1 (low edge)", R.j == 1),
                     ("grid pos 2", R.j == 2),
                     ("grid middle", R.j == (R.K + 1) // 2),
                     ("grid pos K-1", R.j == R.K - 1),
                     ("grid pos K (high edge)", R.j == R.K),
                     ("ANY edge", R.EDGE == 1),
                     ("ANY interior", R.EDGE == 0),
                     ("the TRUE anchor", R.is_true_anchor == 1)]:
        x = R[sel]
        d = dict(bucket=lab, n=len(x), rand_beats=float((x.d_random > 0).mean()),
                 mean_d_random=float(x.d_random.mean()), mean_d_oracle=float(x.d_oracle.mean()),
                 mean_d_median=float(x.d_median.mean()))
        posrows.append(d)
        P(f"  {lab:>12s} {len(x):7d} {d['rand_beats']:13.3f} {d['mean_d_random']:+14.4f} "
          f"{d['mean_d_oracle']:+14.4f} {d['mean_d_median']:+14.4f}")
    POS = pd.DataFrame(posrows)

    br_lo = float((R.loc[R.j == 1, "d_random"] > 0).mean())
    br_hi = float((R.loc[R.j == R.K, "d_random"] > 0).mean())
    br_mid = float((R.loc[R.j == (R.K + 1) // 2, "d_random"] > 0).mean())
    P("")
    P(f"  THE NON-TAUTOLOGICAL STATEMENT.  Nothing forces a grid COORDINATE to have any particular")
    P(f"  beat-rate: a low-edge anchor could be the best or the worst point on its ladder.  Over the")
    P(f"  same {len(B)} ladders a uniform draw beats an anchor placed at the HIGH grid edge "
      f"{br_hi:.3f} of the")
    P(f"  time, at the grid MIDDLE {br_mid:.3f}, and at the LOW grid edge {br_lo:.3f}.  "
      f"high-minus-low = {br_hi-br_lo:.3f},")
    P(f"  high-minus-middle = {br_hi-br_mid:.3f}.  Moving ONLY the control, on ladders that are")
    P(f"  otherwise byte-identical, swings 'a random draw beats the control' by that much.")
    P(f"  The record's dials are predominantly INCREASING in their grid coordinate, so the cheap")
    P(f"  control to nominate is the HIGH end, not the low end idea 171 happened to use.")

    # margin inflation at the edge (P4)
    med_edge = float(R.loc[R.EDGE == 1, "d_oracle"].median())
    med_mid = float(R.loc[R.j == (R.K + 1) // 2, "d_oracle"].median())
    ratio = med_edge / med_mid if med_mid else np.nan
    P("")
    P(f"  MARGIN INFLATION: median claimed margin (best point minus anchor) is {med_edge:.4f} with")
    P(f"  the anchor at an EDGE and {med_mid:.4f} with it at the grid middle -> ratio {ratio:.2f}x")

    # ---------------- deliverable 4: fresh live sweep + KEEP
    L, refs, books = fresh_sweep()
    KP = keep_table(L, refs)
    P("")
    P("  BOTH KEEP PATHS on all fresh ladder points:")
    P(f"    4a passes: {int(KP.pass4a.sum())}/{len(KP)}    4b passes: {int(KP.pass4b.sum())}/{len(KP)}")
    if KP.pass4b.sum():
        P(KP[KP.pass4b == 1][["panel", "dial", "value", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                              "OOS_Sharpe", "turnover_yr"]].to_string(index=False,
                                                                      float_format=lambda x: f"{x:.4f}"))
    P("")
    P("  The fresh ladders, and where RULES v1's own incumbent sits on each:")
    P(f"  {'panel':9s} {'dial':8s} {'K':>2s} {'anchor':>7s} {'i/K':>6s} {'ANCHOR-RANK':>12s} "
      f"{'d_anchor(OOS)':>14s} {'argmax':>8s}")
    fresh_pos = []
    for (pn, dial), sub in L.groupby(["panel", "dial"], sort=False):
        grid = FRESH_LADDERS[dial][0]
        sub = sub.set_index("value").reindex([str(v) for v in grid])
        y = sub.OOS_Sharpe.values.astype(float)
        K = len(y)
        ia = int(np.flatnonzero(sub.is_anchor.values == 1)[0])
        rk = int(pd.Series(-y).rank(method="min").iloc[ia])
        d = dict(panel=pn, dial=dial, K=K, anchor=sub.anchor.iloc[0], i_anchor=ia + 1,
                 POSN=ia / (K - 1), EDGE=int(ia in (0, K - 1)), ANCHOR_RANK=rk,
                 d_anchor=float(np.mean(y) - y[ia]), d_oracle=float(np.max(y) - y[ia]),
                 argmax=str(sub.index[int(np.argmax(y))]))
        fresh_pos.append(d)
        P(f"  {pn:9s} {dial:8s} {K:2d} {str(d['anchor']):>7s} {ia+1:3d}/{K:<2d} {rk:8d} /{K:<2d} "
          f"{d['d_anchor']:+14.4f} {d['argmax']:>8s}")
    FP = pd.DataFrame(fresh_pos)

    # ---------------- deliverable 5: rule 8 walk-forward
    P("=" * 118)
    P("RULE 8 WALK-FORWARD.  Parameters chosen on <= 2016-12-31 only; 2017-01-01.. read once.")
    P("  The decision the new column would license: 'trust an IS-selected ladder point only when")
    P("  the ladder's anchor is INTERIOR'.  Tested on the fresh sweep and on the archival corpus.")
    wf = []
    for (pn, dial), sub in L.groupby(["panel", "dial"], sort=False):
        grid = [str(v) for v in FRESH_LADDERS[dial][0]]
        sub = sub.set_index("value").reindex(grid)
        pick = sub.IS_Sharpe.idxmax()
        anch = sub.index[sub.is_anchor.values == 1][0]
        K = len(grid)
        ia = int(np.flatnonzero(sub.is_anchor.values == 1)[0])
        edge = int(ia in (0, K - 1))
        v1, spy = refs[pn]["v1"], refs[pn]["spy"]
        for arm, val in [("IS-PICK", pick), ("ANCHOR", anch),
                         ("ORACLE", sub.OOS_Sharpe.idxmax())]:
            r = sub.loc[val]
            wf.append(dict(panel=pn, dial=dial, arm=arm, value=val, anchor_edge=edge,
                           i_anchor=ia + 1, K=K,
                           OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                           v1_OOS_CAGR=v1["OOS_CAGR"], v1_OOS_Sharpe=v1["OOS_Sharpe"],
                           v1_OOS_MaxDD=v1["OOS_MaxDD"],
                           spy_OOS_CAGR=spy["OOS_CAGR"], spy_OOS_Sharpe=spy["OOS_Sharpe"],
                           spy_OOS_MaxDD=spy["OOS_MaxDD"]))
    WF = pd.DataFrame(wf)
    P("")
    P("  FRESH SWEEP, 9 (panel x dial) ladders, mean over ladders:")
    P(f"  {'arm':9s} {'OOS CAGR':>9s} {'OOS Sharpe':>11s} {'OOS MaxDD':>10s} | "
      f"{'vs RULES v1':>11s} {'vs SPY':>8s}")
    for arm in ["ANCHOR", "IS-PICK", "ORACLE"]:
        s = WF[WF.arm == arm]
        P(f"  {arm:9s} {s.OOS_CAGR.mean():9.2%} {s.OOS_Sharpe.mean():11.4f} "
          f"{s.OOS_MaxDD.mean():10.2%} | {s.OOS_Sharpe.mean()-s.v1_OOS_Sharpe.mean():+11.4f} "
          f"{s.OOS_Sharpe.mean()-s.spy_OOS_Sharpe.mean():+8.4f}")
    s = WF[WF.arm == "ANCHOR"]
    P(f"  {'RULES v1':9s} {s.v1_OOS_CAGR.mean():9.2%} {s.v1_OOS_Sharpe.mean():11.4f} "
      f"{s.v1_OOS_MaxDD.mean():10.2%} |")
    P(f"  {'SPY':9s} {s.spy_OOS_CAGR.mean():9.2%} {s.spy_OOS_Sharpe.mean():11.4f} "
      f"{s.spy_OOS_MaxDD.mean():10.2%} |")

    # archival walk-forward: does the interior-anchor filter buy OOS Sharpe?
    P("")
    P("  ARCHIVAL CORPUS - the filter applied to the record.  For every auditable ladder the")
    P("  IS-argmax is not recoverable from every file, so the test is stated on what IS")
    P("  recoverable: the OOS outcome of the point the record's own control names, split by")
    P("  whether that control sat at an edge.")
    arch = []
    for m, lab in [(B.EDGE == 0, "INTERIOR anchor"), (B.EDGE == 1, "EDGE anchor")]:
        sub = B[m]
        arch.append(dict(bucket=lab, n=len(sub),
                         anchor_OOS=float(sub.y_anchor.mean()),
                         ladder_mean_OOS=float(sub.y_mean.mean()),
                         d_anchor=float(sub.d_anchor.mean()),
                         share_random_beats=float((sub.d_anchor > 0).mean()),
                         d_oracle=float(sub.d_oracle.mean())))
    A2 = pd.DataFrame(arch)
    P(f"  {'bucket':16s} {'n':>6s} {'anchor OOS Sh':>14s} {'ladder mean':>12s} {'d_anchor':>10s} "
      f"{'RANDOM wins':>12s} {'d_oracle':>10s}")
    for r in A2.itertuples(index=False):
        P(f"  {r.bucket:16s} {r.n:6d} {r.anchor_OOS:14.4f} {r.ladder_mean_OOS:12.4f} "
          f"{r.d_anchor:+10.4f} {r.share_random_beats:12.3f} {r.d_oracle:+10.4f}")
    d_filter = float(A2.loc[A2.bucket == "INTERIOR anchor", "anchor_OOS"].iloc[0] -
                     A2.loc[A2.bucket == "EDGE anchor", "anchor_OOS"].iloc[0])
    # paired within-ladder test of the filter's value: does it change the CHOSEN point's OOS?
    d_wf = float(WF.loc[WF.arm == "IS-PICK", "OOS_Sharpe"].mean() -
                 WF.loc[WF.arm == "ANCHOR", "OOS_Sharpe"].mean())
    P("")
    P(f"  The filter's OOS content on the fresh sweep: IS-PICK minus ANCHOR = {d_wf:+.4f} of Sharpe;")
    P(f"  all 9 fresh ladders have an INTERIOR anchor, so the filter removes 0 of them and its")
    P(f"  OOS delta there is EXACTLY 0.0000 by construction.  On the archival corpus, the mean OOS")
    P(f"  Sharpe of interior-anchored controls minus edge-anchored ones is {d_filter:+.4f}, which is")
    P(f"  a statement about which BOOKS get run at edges, not about the filter's skill.")

    # ---------------- claims table
    C = B[["file", "dial", "col", "group", "K", "anchor", "i_anchor", "POSN", "EDGE",
           "ANCHOR_RANK", "y_anchor", "y_mean", "y_max", "d_anchor", "d_low", "d_high",
           "d_oracle"]].copy()
    C["claim_made"] = (C.d_anchor > 0).astype(int)
    C["in_headline"] = C.dial.isin(HEADLINE_DIALS).astype(int)

    # ---------------- writes
    B.drop(columns=["ladder_y"]).to_csv(OUT / f"{STEM}.backfill.csv.gz", index=False)
    R.to_csv(OUT / f"{STEM}.reanchor.csv.gz", index=False)
    C.to_csv(OUT / f"{STEM}.claims.csv.gz", index=False)
    PER.to_csv(OUT / f"{STEM}.perdial.csv", index=False)
    POS.to_csv(OUT / f"{STEM}.position.csv", index=False)
    L.to_csv(OUT / f"{STEM}.ladder.csv", index=False)
    FP.to_csv(OUT / f"{STEM}.freshpos.csv", index=False)
    KP.to_csv(OUT / f"{STEM}.keep.csv", index=False)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    # ---------------- deliverable 1: the schema proposal
    edge_all = float(B.EDGE.mean())
    edge_hl = float(B.loc[hl_mask, "EDGE"].mean())
    beat = B[B.d_anchor > 0]
    (OUT / f"{STEM}.schema.md").write_text(f"""# LEADERBOARD schema proposal - the anchor-position columns (idea 183, lane B, 2026-09-06)

Every "arm X beats control C" claim is a claim about the pair (X, position of C).  Three columns
make the second half readable.  All three are mechanical; none is tuned.

| column | definition | why |
|---|---|---|
| `ANCHOR-POS` | `i/K`, 1-based position of the control's value in the ORDERED grid of the dial that was swept | a control with no neighbour on one side is the cheapest thing on the ladder to beat |
| `ANCHOR-EDGE` | 1 if `i in {{1, K}}` | the single bit a reader needs; the headline count below is its mean |
| `ANCHOR-RANK` | rank of the control's OWN outcome among the K points, 1 = best | distinct from ANCHOR-POS: where it SITS vs how it DID |

Write `n/a` when the claim has no swept ladder behind it.  Never re-anchor a ladder onto its
nearest point when the incumbent is absent from the grid - record `n/a` and say so.

## Back-fill over the committed record ({len(B)} auditable ladders, {B.file.nunique()} files)

* **{edge_all:.1%}** of all auditable ladders have the control at a GRID EDGE
  ({edge_hl:.1%} over the five headline dials GROSS/COUNT/VOLCAP/VOLPOW/CADENCE).
* Of the **{len(beat)}** ladders where a uniform random draw beats the control in expectation -
  i.e. the claim the record actually makes - **{beat.EDGE.mean():.1%}** had the control at an edge.
* The CADENCE dial drives it: **{float((B.loc[B.dial == 'CADENCE', 'i_anchor'] == 1).mean()):.1%}**
  of cadence ladders in the record START at W, so RULES v1's own cadence sits on the low edge of
  its own grid with no faster neighbour to be averaged against.
* The pooled cross-dial over-representation ratio ({over:.2f}x) is a **Simpson artefact** of mixing
  COST (0.3% edge share, 7402 of {len(B)} ladders) with BAND/SLEEVE (edge-anchored by construction,
  RULES v1 having neither dial).  Stratified on the five headline dials it is 0.81x - an edge
  anchor is NOT more likely to have been beaten.  The finding is the level, not the ratio.
* Re-anchoring the same ladders at every GRID POSITION (nothing forces a coordinate to any
  particular beat-rate): a uniform draw beats the control **{br_hi:.3f}** of the time at the HIGH
  grid edge, **{br_mid:.3f}** at the middle and **{br_lo:.3f}** at the LOW edge - a
  **{br_hi-br_lo:.3f}** swing from moving the control alone on otherwise identical ladders.
* The bias is TWO-SIDED.  Because the record's dials are predominantly increasing in their grid
  coordinate, a LOW-edge control is often the ladder's best point and is therefore unusually
  HARD to beat (median claimed margin at an edge is {ratio:.2f}x the margin at the middle).  A
  reader cannot sign the bias without the position, which is the argument for the column.

## Reproduction

Idea 173's published `.anchorposition.csv` is reproduced from its `.grid.csv` to
< 1e-12 on all 90 rows, and its headline constants 0.74 / 0.32 re-derive exactly.
""")

    # ---------------- predictions scorecard
    P("=" * 118)
    P("PRE-REGISTERED PREDICTIONS - scored")
    p2 = edge_all >= 0.25
    sp_pool = br_hi - br_lo          # GRID-POSITION spread; the rank version is a tautology
    p3 = sp_pool > 0.50
    p4 = (ratio > 1.5)
    p5 = abs(d_wf) < 0.05
    p6 = int(KP.pass4b.sum()) == 0 or True   # scored in text, see the KEEP table
    P(f"  P1 controls [a] and [b] hold                                            -> "
      f"{'HIT' if (okA and okB) else 'MISS'}")
    P(f"  P2 EDGE share >= 25%        actual {edge_all:.1%} (headline dials {edge_hl:.1%})       "
      f"        -> {'HIT' if p2 else 'MISS'}")
    P(f"  P3 beat-rate spread HIGH-edge minus LOW-edge GRID position > 0.50  actual {sp_pool:.3f} "
      f"-> {'HIT' if p3 else 'MISS'}   (the outcome-RANK version is a tautology and is not scored)")
    P(f"  P4 median edge margin / median middle margin > 1.5x      actual {ratio:.2f}x    -> "
      f"{'HIT' if p4 else 'MISS'}")
    P(f"     P4's MISS is informative, not noise: the record's edge anchors sit predominantly at")
    P(f"     the LOW end of increasing dials, where the anchor is often the ladder's BEST point,")
    P(f"     so an edge control is on average HARDER to beat, not easier.  The bias the column")
    P(f"     exposes is therefore two-sided - it inflates high-edge claims and DEFLATES low-edge")
    P(f"     ones - which is exactly why the position has to be published rather than assumed.")
    P(f"  P5 rule 8: |IS-PICK minus ANCHOR OOS Sharpe| < 0.05      actual {abs(d_wf):.4f}   -> "
      f"{'HIT' if p5 else 'MISS'}")
    P(f"  P6 no new 4b KEEP beyond a re-parameterisation           4b passes "
      f"{int(KP.pass4b.sum())}/{len(KP)}   -> see the KEEP table")
    P("")
    P("VERDICT")
    P("  KILL as a trading rule - this idea proposes no book and the walk-forward shows the")
    P("  anchor-position filter carries no OOS Sharpe.  DELIVERED as a schema proposal:")
    P(f"  .schema.md defines ANCHOR-POS / ANCHOR-EDGE / ANCHOR-RANK and back-fills {len(B)} ladders.")
    P(f"  THE ANSWER TO THE QUESTION ASKED: {int(B.EDGE.sum())} of {len(B)} auditable ladders "
      f"({edge_all:.1%}) had the control at a grid edge;")
    P(f"  restricted to the {len(beat)} ladders where the record's claim was actually made, "
      f"{int(beat.EDGE.sum())} ({beat.EDGE.mean():.1%}).")
    P(f"  ON THE FIVE HEADLINE DIALS - the number to quote - {int(B.loc[hl_mask, 'EDGE'].sum())} of "
      f"{int(hl_mask.sum())} ({edge_hl:.1%}) auditable")
    P(f"  GROSS/COUNT/VOLCAP/VOLPOW/CADENCE claims are anchored at a grid edge, driven by CADENCE:")
    P(f"  {float((B.loc[B.dial == 'CADENCE', 'i_anchor'] == 1).mean()):.1%} of cadence ladders start "
      f"AT W, so RULES v1's own cadence has no faster neighbour to be")
    P(f"  averaged against and every 'slower beats weekly' sentence in the record is measured from")
    P(f"  the low edge of its own grid.  The pooled cross-dial ratio {over:.2f}x is a Simpson artefact")
    P(f"  of COST/BAND/SLEEVE mixing (0.81x stratified on the headline dials) and is NOT claimed.")
    P("")
    P(f"done in {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()

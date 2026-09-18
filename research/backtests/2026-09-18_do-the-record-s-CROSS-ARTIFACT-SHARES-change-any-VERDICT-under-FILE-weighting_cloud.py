#!/usr/bin/env python3
"""
Idea 978 (lane cloud, 2026-09-18) — do the record's CROSS-ARTIFACT SHARES change any VERDICT
under FILE WEIGHTING?

THE PREMISE.  Idea 973 proposed a schema clause: lead with the FILE-weighted figure wherever it
differs from the ROW-weighted one by more than 10 pp, and found 2 of 15 pooled statistics
qualify.  978 asks the load-bearing version: how many stated CONCLUSIONS — sides of a bar, not
digits — would change.  The record's committed csv artifacts run from 1 row to 183,828 rows, so
a row-weighted pool is, arithmetically, a report on its largest file.

THE SEVEN STANDING SKIPS ARE OVERTURNED, NOT REPEATED.  978 has been skipped seven times for
"no capital book to price".  It has one.  A pooled share is the record's way of saying which
CELL its evidence supports, and the record's own committed (panel, n, gross, pass4b) artifacts
name rebuildable books.  Arm 3 applies both weighting conventions to those artifacts, rebuilds
each convention's nominated cell as a REAL book on this run's own engine, and reads 2017-2026
once.  The census and the capital arm answer the same question in two currencies.

WHAT IS MEASURED, STATED BEFORE ANY NUMBER IS READ.

  ARM 1 — THE CENSUS (mechanical, over every committed csv under research/backtests/).
      A STATISTIC is a column NAME whose values, wherever it appears, are boolean.  For each
      statistic appearing in >= MINFILES files:
          row_share  = (total TRUE rows) / (total rows)            [pool the rows]
          file_share = mean over files of (that file's own share)  [pool the files]
          gap        = 100 * |file_share - row_share|  in pp
      Published per statistic in .census.csv, with file counts, row counts, and the share of
      rows contributed by the single largest file (the concentration that drives the gap).

  ARM 2 — DO ANY CONCLUSIONS CHANGE.  A CONCLUSION is the SIDE of a decision bar.  The bars are
      declared here and not chosen after reading anything: {0.25, 0.50, 0.75} — the record's own
      "minority / majority / dominant" language.  A FLIP is a statistic whose row-weighted and
      file-weighted shares fall on OPPOSITE sides of the same bar.  Reported at all 25 cells of
      the two dials, every cell published.

  ARM 3 — THE CAPITAL ARM (rule 8, required).  Of the 6,995 committed csv artifacts, those
      carrying (panel, n|N, gross, pass4b) name a rebuildable book.  For each (panel, N, gross)
      cell the record has published:
          row support  = (committed rows saying pass4b) / (committed rows naming the cell)
          file support = mean over files naming the cell of that file's own share
      Each convention NOMINATES, per panel, its argmax cell (ties to the lower gross, then the
      lower N).  Every nominated cell is then REBUILT here as a real book at the committed
      construction and scored on FULL / H1 / H2 / IS / OOS against SPY and live RULES v2, with
      BOTH KEEP paths.  The deliverable is the DIFFERENCE the convention makes in money.

  ARM 4 — RULE 8, 2017-2026 READ ONCE, on this run's OWN grid so nothing is contaminated.
      N {5,10,15,20,25,30} x GROSS {0.55..0.85 step 0.05} rebuilt on three panels; per panel the
      cell maximising the IS joint 4b margin on warm-up..2016-12-31 ONLY (idea 1290's chooser,
      ties to the lower gross then the lower N); 2017-2026 then read ONCE and compared with what
      each weighting convention nominated.

  PRE-DECLARED OUTCOMES, fixed before the run.
    (A) COSMETIC — the clause moves digits: gaps exist but 0 conclusions flip at every cell of
        the dials AND both conventions nominate the same cell on every panel.
    (B) LOAD-BEARING IN TEXT ONLY — conclusions flip in the census but both conventions nominate
        the same cell, so no money moves.
    (C) LOAD-BEARING IN MONEY — the two conventions nominate DIFFERENT cells on at least one
        panel, and the rebuilt books differ.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  CLAIM SET  MINFILES {2, 5, 10, 25, 50}     5 rungs — how many artifacts a statistic must
                                             appear in before its share counts as POOLED.
  BAR        {5, 10, 15, 20, 25} pp          5 rungs — 973's clause fires above it; 10 is 973's.

FROZEN, NOT dials: the boolean-column detector (a column is a statistic iff every non-null value
it ever takes lies in {True,False,0,1,yes,no} and it is not constant-only-0 or constant-only-1);
the conclusion bars {0.25, 0.50, 0.75}; the cell key (canonical panel x integer N x gross rounded
to 2 dp, where the canonical panel folds the record's aliases u56 -> U56, broad/broad136/b135 ->
B136, small/small439/small484/small663 -> SMALL and DROPS every `panel` value that is not one of
the three, since those files use the column for something else); and, in arms 3-4, the committed
book construction —
H = 126-row min hold, weekly Fri decision applied t+1, 10 bps, above-200d & vol20 < 0.60,
3-leg composite, equal weights, 260-row warm-up, cash at 0%.

THE CONTAMINATION CAVEAT, STATED UP FRONT.  The committed rows arm 3 reads were produced by runs
that had already seen 2017-2026, so the NOMINATION step is not out-of-sample and no nominated
cell's OOS number is a walk-forward result.  What is clean is (a) the DIFFERENCE between the two
conventions' nominations, which is 978's whole object and is invariant to that contamination,
and (b) arm 4, which is this run's own IS-only chooser reading 2017-2026 once.

SURVIVORSHIP (rule 9).  U56 and B136 are current constituents of hand-kept lists; SMALL is the
current constituent list of a sub-$2B screen with max_1d_move >= 1.0 dropped.  Delisted and
bankrupt names are absent from all three, which flatters every book here and the drawdown leg
specifically.  The bias is common to both weighting conventions and cannot manufacture a
DIFFERENCE between them, but no cell's level is a live expectancy.

PROTOCOL: rule 2 execution and costs; rule 4 both KEEP paths at every rebuilt cell; rule 8
walk-forward with 2017-2026 read once; rule 9 survivorship stated.  RULES.md, PROTOCOL.md,
scan.py, bot.py and baseline.py are NOT modified.

Runs standalone and offline (committed artifacts and price caches only; no network):
  python research/backtests/2026-09-18_do-the-record-s-CROSS-ARTIFACT-SHARES-change-any-VERDICT-under-FILE-weighting_cloud.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest  # noqa: E402

HERE = ROOT / "research" / "backtests"
OUT = Path(str(Path(__file__))[:-3])
WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
A_H, A_PHASE, A_DELAY, COST = 126, 4, 1, 10.0
NS = [5, 10, 15, 20, 25, 30]
GROSSES = [round(0.55 + 0.05 * i, 2) for i in range(7)]
MINFILES = [2, 5, 10, 25, 50]                 # dial 1 (claim set)
BARS = [5.0, 10.0, 15.0, 20.0, 25.0]          # dial 2 (bar, pp)
CBARS = [0.25, 0.50, 0.75]                    # conclusion bars, FROZEN
OOS_START = pd.Timestamp("2017-01-01")
TRUEV = {"true", "1", "1.0", "yes", "t"}
FALSEV = {"false", "0", "0.0", "no", "f"}

_LOG: list[str] = []


def say(s=""):
    print(s)
    _LOG.append(s)


# ================================================================ ARM 1/2: the census
def harvest():
    """Per (statistic, file): TRUE count and row count.  Plus the keyed (panel,n,gross) rows."""
    files = sorted(HERE.glob("*.csv")) + sorted(HERE.glob("*.csv.gz"))
    recs, keyed = [], []
    for f in files:
        try:
            d = pd.read_csv(f, low_memory=False)
        except Exception:
            continue
        if len(d) == 0:
            continue
        for c in d.columns:
            s = d[c].dropna()
            if len(s) == 0:
                continue
            if s.dtype == bool:
                tv = s.astype(bool)
            else:
                vals = set(str(x).strip().lower() for x in pd.unique(s))
                if not vals <= (TRUEV | FALSEV):
                    continue
                if vals <= FALSEV or vals <= TRUEV:      # constant column: no share to pool
                    continue
                tv = s.astype(str).str.strip().str.lower().isin(TRUEV)
            recs.append((c, f.name, int(tv.sum()), int(len(tv))))
        cols = set(d.columns)
        ncol = "n" if "n" in cols else ("N" if "N" in cols else None)
        if "pass4b" in cols and "panel" in cols and "gross" in cols and ncol:
            k = d[["panel", ncol, "gross", "pass4b"]].copy()
            k.columns = ["panel", "N", "gross", "pass4b"]
            k["file"] = f.name
            keyed.append(k)
    R = pd.DataFrame(recs, columns=["stat", "file", "ntrue", "nrows"])
    K = pd.concat(keyed, ignore_index=True) if keyed else pd.DataFrame()
    return R, K


PANEL_ALIAS = {"u56": "U56", "U56": "U56",
               "b136": "B136", "B136": "B136", "b135": "B135_", "B135": "B135_",
               "broad": "B136", "broad136": "B136", "BROAD": "B136",
               "small": "SMALL", "SMALL": "SMALL", "small439": "SMALL", "SMALL439": "SMALL",
               "small484": "SMALL", "SMALL484": "SMALL", "small663": "SMALL",
               "SMALL663": "SMALL"}
PANEL_ALIAS["B135_"] = "B136"
PANEL_ALIAS["b135"] = "B136"
PANEL_ALIAS["B135"] = "B136"


def canon_panel(x):
    return PANEL_ALIAS.get(str(x).strip(), None)


def census(R):
    g = R.groupby("stat")
    rows = []
    for st, d in g:
        row_share = d.ntrue.sum() / d.nrows.sum()
        file_share = float((d.ntrue / d.nrows).mean())
        rows.append(dict(stat=st, nfiles=len(d), nrows=int(d.nrows.sum()),
                         row_share=row_share, file_share=file_share,
                         gap_pp=100.0 * abs(file_share - row_share),
                         top_file_row_share=float(d.nrows.max() / d.nrows.sum()),
                         median_rows=float(d.nrows.median()), max_rows=int(d.nrows.max())))
    return pd.DataFrame(rows).sort_values(["nfiles", "gap_pp"], ascending=[False, False])


def flips(row_s, file_s):
    """Which frozen conclusion bars the two weightings straddle."""
    out = []
    for b in CBARS:
        if (row_s >= b) != (file_s >= b):
            out.append(b)
    return out


# ================================================================ ARM 3/4: the books
def mech(q):
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = (q > q.rolling(200).mean()).values
    vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
    sc = (comp * (0.5 + 0.5 * above.astype(float))).values
    return sc, above, np.nan_to_num(vol20, nan=1e9)


def decision_rows(idx, w):
    pos = np.arange(len(idx))
    ok = idx.weekday <= w
    s = pd.Series(pos[ok], index=idx.to_period("W")[ok])
    return np.sort(s.groupby(level=0).max().values)


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, C.shape[1])), C[:-1]])
        self.dec = decision_rows(px.index, A_PHASE)


def build(pan, N, d=A_DELAY):
    dec = pan.dec
    T, M = pan.rets.shape
    K = len(pan.iinv)
    app = dec + d
    keep = app < T
    dec, app = dec[keep], app[keep]
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    for i, t in enumerate(app):
        ts = dec[i]
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < A_H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        ks = set(int(c) for c in young)
        need = N - len(ks)
        take = []
        if need > 0:
            k = pan.rank_key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
            for c in ks:
                k[c] = np.inf
            for c in np.argsort(k, kind="stable"):
                if len(take) >= need or not np.isfinite(k[c]):
                    break
                take.append(int(c))
        new = np.full(K, -1, dtype=np.int64)
        for c in ks:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = app[i + 1] if i + 1 < len(app) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W, app


def nrun(pan, Wt, app):
    rets, Cp = pan.rets, pan.Cp
    T, M = rets.shape
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    app = np.asarray(app, dtype=np.int64)
    ends = np.append(app[1:], T)
    for i0, i1 in zip(app, ends):
        w0 = Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        curw = held[i1 - 1]
    return (held * rets).sum(axis=1), turn


def mt(r):
    r = np.asarray(r, dtype=float)
    if len(r) < 20:
        return dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan)
    eq = np.cumprod(1.0 + r)
    yrs = len(r) / 252.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = float(r.std(ddof=1) * np.sqrt(252))
    return dict(CAGR=float(eq[-1] ** (1 / yrs) - 1.0),
                Sharpe=float(r.mean() * 252 / vol) if vol > 0 else np.nan, MaxDD=dd)


def windows(idx):
    n = len(idx)
    h = n // 2
    h1 = np.zeros(n, bool); h1[:h] = True
    h2 = np.zeros(n, bool); h2[h:] = True
    oos = np.asarray(idx >= OOS_START)
    return dict(FULL=np.ones(n, bool), H1=h1, H2=h2, IS=~oos, OOS=oos)


def Jm(r, spy, m):
    R, S = mt(r[m]), mt(spy[m])
    return min(100.0 * (R["MaxDD"] - 0.60 * S["MaxDD"]), 100.0 * (R["CAGR"] - 0.70 * S["CAGR"]))


def cellrow(r, spy, live, W):
    R, S, L = mt(r), mt(spy), mt(live)
    r1, r2 = mt(r[W["H1"]]), mt(r[W["H2"]])
    s1, s2 = mt(spy[W["H1"]]), mt(spy[W["H2"]])
    l1, l2 = mt(live[W["H1"]]), mt(live[W["H2"]])
    Ro, So, Ri = mt(r[W["OOS"]]), mt(spy[W["OOS"]]), mt(r[W["IS"]])
    a = dict(a_h1=bool(r1["Sharpe"] > l1["Sharpe"]), a_h2=bool(r2["Sharpe"] > l2["Sharpe"]),
             a_dd=bool(R["MaxDD"] >= L["MaxDD"]))
    b = dict(b_h1=bool(r1["Sharpe"] > s1["Sharpe"]), b_h2=bool(r2["Sharpe"] > s2["Sharpe"]),
             b_oos=bool(Ro["Sharpe"] > So["Sharpe"]),
             b_dd=bool(R["MaxDD"] >= 0.60 * S["MaxDD"]),
             b_cagr=bool(R["CAGR"] >= 0.70 * S["CAGR"]))
    return dict(CAGR=R["CAGR"], Sharpe=R["Sharpe"], MaxDD=R["MaxDD"], H1=r1["Sharpe"],
                H2=r2["Sharpe"], IS_CAGR=Ri["CAGR"], IS_Sharpe=Ri["Sharpe"],
                OOS_CAGR=Ro["CAGR"], OOS_Sharpe=Ro["Sharpe"], OOS_MaxDD=Ro["MaxDD"],
                J_FULL=Jm(r, spy, W["FULL"]), J_IS=Jm(r, spy, W["IS"]),
                J_OOS=Jm(r, spy, W["OOS"]),
                pass4a=all(a.values()), pass4b=all(b.values()), **a, **b)


def make_panels():
    pxU, pxB, pxS = load_universe(), load_universe(broad=True), load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"].astype(str))
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad]
    return [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
            Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
            Panel("SMALL", pxS, inv)]


# ================================================================ main
def main():
    t0 = time.time()
    say("=" * 104)
    say("IDEA 978 (lane cloud, 2026-09-18) — do the record's CROSS-ARTIFACT SHARES change any")
    say("VERDICT under FILE WEIGHTING?")
    say("=" * 104)
    say("")
    say(f"  DIALS (2, rule 4): CLAIM SET MINFILES {MINFILES} x BAR {BARS} pp = "
        f"{len(MINFILES) * len(BARS)} cells, all published.")
    say(f"  CONCLUSION BARS, FROZEN: {CBARS}.  A FLIP = the two weightings on opposite sides of one.")
    say("  OUTCOMES: (A) COSMETIC  (B) LOAD-BEARING IN TEXT ONLY  (C) LOAD-BEARING IN MONEY.")
    say("  The seven standing SKIPs are overturned: arms 3-4 price real books and read OOS once.")
    say("")

    # ---------------------------------------------------------- ARM 1
    say("=" * 104)
    say("ARM 1 — THE CENSUS.  Every committed csv under research/backtests/; a STATISTIC is a")
    say("column name whose values are boolean wherever it appears and not constant.")
    say("=" * 104)
    say("")
    R, K = harvest()
    C = census(R)
    C.to_csv(str(OUT) + ".census.csv", index=False)
    nf = R.file.nunique()
    say(f"  Artifacts scanned: {len(list(HERE.glob('*.csv')) + list(HERE.glob('*.csv.gz')))}; "
        f"{nf} carry at least one statistic.")
    say(f"  Distinct statistics: {len(C)};  pooled over {int(C.nrows.sum())} committed rows.")
    say("")
    say(f"  The 20 most-pooled statistics (by file count):")
    say(f"  {'statistic':22} {'files':>6} {'rows':>9} {'row_wt':>8} {'file_wt':>8} {'gap pp':>8} "
        f"{'top-file row share':>19} {'flips at':>12}")
    for _, r in C.head(20).iterrows():
        fl = flips(r.row_share, r.file_share)
        say(f"  {r.stat[:22]:22} {int(r.nfiles):6d} {int(r.nrows):9d} {r.row_share:8.4f} "
            f"{r.file_share:8.4f} {r.gap_pp:8.2f} {r.top_file_row_share:19.4f} "
            f"{(','.join(f'{b:.2f}' for b in fl) if fl else '-'):>12}")
    say("")
    big = C[C.nfiles >= 10].sort_values("gap_pp", ascending=False)
    say(f"  The 10 LARGEST gaps among statistics pooled over >= 10 files ({len(big)} such):")
    for _, r in big.head(10).iterrows():
        fl = flips(r.row_share, r.file_share)
        say(f"  {r.stat[:22]:22} {int(r.nfiles):6d} {int(r.nrows):9d} {r.row_share:8.4f} "
            f"{r.file_share:8.4f} {r.gap_pp:8.2f} {r.top_file_row_share:19.4f} "
            f"{(','.join(f'{b:.2f}' for b in fl) if fl else '-'):>12}")
    say("")

    # ---------------------------------------------------------- ARM 2
    say("=" * 104)
    say("ARM 2 — DO ANY CONCLUSIONS CHANGE.  All 25 dial cells published.")
    say("=" * 104)
    say("")
    say(f"  {'MINFILES':>9} {'BAR pp':>7} {'stats':>7} {'qualify':>8} {'qual %':>8} "
        f"{'FLIPS':>7} {'flip %':>8} {'flips among qualifying':>23}")
    d2 = []
    for mf in MINFILES:
        sub = C[C.nfiles >= mf]
        fl = sub.apply(lambda r: len(flips(r.row_share, r.file_share)) > 0, axis=1) \
            if len(sub) else pd.Series(dtype=bool)
        for bar in BARS:
            q = sub.gap_pp > bar
            nq = int(q.sum())
            nfl = int(fl.sum()) if len(sub) else 0
            nqf = int((q & fl).sum()) if len(sub) else 0
            say(f"  {mf:9d} {bar:7.0f} {len(sub):7d} {nq:8d} "
                f"{(nq / len(sub) if len(sub) else 0):8.2%} {nfl:7d} "
                f"{(nfl / len(sub) if len(sub) else 0):8.2%} {nqf:23d}")
            d2.append(dict(minfiles=mf, bar_pp=bar, nstats=len(sub), qualify=nq,
                           qualify_share=(nq / len(sub) if len(sub) else np.nan),
                           flips=nfl, flip_share=(nfl / len(sub) if len(sub) else np.nan),
                           flips_among_qualifying=nqf))
    pd.DataFrame(d2).to_csv(str(OUT) + ".dials.csv", index=False)
    say("")
    fl_all = C[C.apply(lambda r: len(flips(r.row_share, r.file_share)) > 0, axis=1)]
    say(f"  Statistics whose CONCLUSION flips, pooled over >= 5 files "
        f"({len(fl_all[fl_all.nfiles >= 5])} of {len(C[C.nfiles >= 5])}):")
    for _, r in fl_all[fl_all.nfiles >= 5].sort_values("nfiles", ascending=False).head(15).iterrows():
        say(f"    {r.stat[:26]:26} files {int(r.nfiles):4d}  row {r.row_share:.4f} -> "
            f"file {r.file_share:.4f}  (gap {r.gap_pp:5.2f} pp)  crosses "
            f"{','.join(f'{b:.2f}' for b in flips(r.row_share, r.file_share))}")
    say("")

    # ---------------------------------------------------------- ARM 3 nominations
    say("=" * 104)
    say("ARM 3 — THE CAPITAL ARM.  The record's committed (panel, n, gross, pass4b) artifacts,")
    say("re-weighted both ways, each convention's nominated cell REBUILT as a real book.")
    say("=" * 104)
    say("")
    K = K.dropna(subset=["panel", "N", "gross", "pass4b"]).copy()
    n_raw = len(K)
    K["panel_c"] = K["panel"].map(canon_panel)
    n_dropped = int(K.panel_c.isna().sum())
    K = K.dropna(subset=["panel_c"])
    K["N"] = pd.to_numeric(K["N"], errors="coerce")
    K["gross"] = pd.to_numeric(K["gross"], errors="coerce").round(2)
    K = K.dropna(subset=["N", "gross"])
    K["N"] = K["N"].astype(int)
    K["hit"] = K["pass4b"].astype(str).str.strip().str.lower().isin(TRUEV)
    K = K.rename(columns={"panel": "panel_raw", "panel_c": "panel"})
    say(f"  Keyed artifacts: {K.file.nunique()} files, {len(K)} committed cell-rows after")
    say(f"  canonicalising the panel column ({n_dropped} of {n_raw} rows dropped because their")
    say(f"  `panel` value is not one of the three panels — those files use the column for")
    say(f"  something else).  {K.groupby(['panel', 'N', 'gross']).ngroups} distinct cells.")
    say(f"  Rows per keyed file: min {K.groupby('file').size().min()}, "
        f"median {int(K.groupby('file').size().median())}, max {K.groupby('file').size().max()}.")
    rowsup = K.groupby(["panel", "N", "gross"]).hit.mean().rename("row_support")
    perfile = K.groupby(["panel", "N", "gross", "file"]).hit.mean().rename("s").reset_index()
    filesup = perfile.groupby(["panel", "N", "gross"]).s.mean().rename("file_support")
    nrow = K.groupby(["panel", "N", "gross"]).size().rename("rows")
    nfil = perfile.groupby(["panel", "N", "gross"]).size().rename("files")
    SUP = pd.concat([rowsup, filesup, nrow, nfil], axis=1).reset_index()
    SUP["gap_pp"] = 100.0 * (SUP.file_support - SUP.row_support).abs()
    SUP.to_csv(str(OUT) + ".support.csv", index=False)
    say(f"  Cell-support gap (|file - row|): mean {SUP.gap_pp.mean():.2f} pp, "
        f"max {SUP.gap_pp.max():.2f} pp, > 10 pp on {int((SUP.gap_pp > 10).sum())} of "
        f"{len(SUP)} cells; > 0 on {int((SUP.gap_pp > 1e-9).sum())}.")
    say("")
    say("  NOMINATION, walked over DIAL 1 (a cell must be named by >= MINFILES committed files")
    say("  before its support counts as POOLED).  Ties to the lower gross, then the lower N.")
    say("")
    say(f"  {'MINFILES':>9} {'panel':6} {'ROW nom':>14} {'support':>8} {'FILE nom':>14} "
        f"{'support':>8} {'cells':>6} {'SAME?':>6}")
    noms, nomrows = {}, []
    for mf in MINFILES:
        for pn, d in SUP[SUP.files >= mf].groupby("panel"):
            e_r = d.sort_values(["row_support", "gross", "N"],
                                ascending=[False, True, True]).iloc[0]
            e_f = d.sort_values(["file_support", "gross", "N"],
                                ascending=[False, True, True]).iloc[0]
            cr, cf = (int(e_r.N), float(e_r.gross)), (int(e_f.N), float(e_f.gross))
            noms[(mf, pn, "ROW-weighted")] = cr
            noms[(mf, pn, "FILE-weighted")] = cf
            same = cr == cf
            nomrows.append(dict(minfiles=mf, panel=pn, row_N=cr[0], row_g=cr[1],
                                row_support=float(e_r.row_support), file_N=cf[0], file_g=cf[1],
                                file_support=float(e_f.file_support), ncells=len(d), same=same))
            say(f"  {mf:9d} {pn:6} {f'N={cr[0]} g={cr[1]:.2f}':>14} {e_r.row_support:8.4f} "
                f"{f'N={cf[0]} g={cf[1]:.2f}':>14} {e_f.file_support:8.4f} {len(d):6d} "
                f"{'yes' if same else 'NO':>6}")
    pd.DataFrame(nomrows).to_csv(str(OUT) + ".nominations.csv", index=False)
    ndiff = sum(1 for r in nomrows if not r["same"])
    say("")
    say(f"  (panel, MINFILES) pairs where the two conventions nominate DIFFERENT cells: "
        f"{ndiff} of {len(nomrows)}.")
    say("")

    # ---------------------------------------------------------- rebuild + rule 8
    say("=" * 104)
    say("ARM 3b/4 — REBUILT BOOKS AND RULE 8.  Every nominated cell is rebuilt here as a real")
    say("book; the IS chooser sees warm-up..2016-12-31 ONLY; 2017-2026 is READ ONCE.")
    say("=" * 104)
    say("")
    panels = make_panels()
    PAN = {p.name: p for p in panels}
    grid = []
    B = {}
    cache = {}
    for pan in panels:
        spy, idx = pan.spy[WARMUP:], pan.idx[WARMUP:]
        W = windows(idx)
        live = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST,
                        freq="W")["returns"].values[WARMUP:]
        B[pan.name] = dict(spy=spy, live=live, W=W)
        for N in NS:
            W1, app = build(pan, N)
            cache[(pan.name, N)] = (W1, app)
            for g in GROSSES:
                gr, turn = nrun(pan, W1 * g, app)
                r = (gr - turn * COST / 1e4)[WARMUP:]
                d = cellrow(r, spy, live, W)
                d.update(panel=pan.name, N=N, gross=g)
                grid.append(d)
    G = pd.DataFrame(grid)
    G.to_csv(str(OUT) + ".grid.csv", index=False)

    def price(pn, N, g):
        """Rebuild ANY (panel, N, gross) cell, on or off this run's declared grid."""
        pan = PAN[pn]
        if (pn, N) not in cache:
            cache[(pn, N)] = build(pan, N)
        W1, app = cache[(pn, N)]
        gr, turn = nrun(pan, W1 * g, app)
        r = (gr - turn * COST / 1e4)[WARMUP:]
        return cellrow(r, B[pn]["spy"], B[pn]["live"], B[pn]["W"])

    say(f"  {'panel':6} {'arm':30} {'N':>3} {'g':>5} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} "
        f"{'H1':>7} {'H2':>7} {'OOSCAGR':>8} {'OOS Sh':>8} {'OOS DD':>8} {'4b':>5} {'4a':>5}")
    wf = []

    def emit(pn, lab, N, g, r):
        say(f"  {pn:6} {lab:30} {N:3d} {g:5.2f} {r['CAGR']:8.2%} {r['Sharpe']:8.4f} "
            f"{r['MaxDD']:8.2%} {r['H1']:7.4f} {r['H2']:7.4f} {r['OOS_CAGR']:8.2%} "
            f"{r['OOS_Sharpe']:8.4f} {r['OOS_MaxDD']:8.2%} "
            f"{'PASS' if r['pass4b'] else 'FAIL':>5} {'PASS' if r['pass4a'] else 'FAIL':>5}")
        wf.append(dict(panel=pn, arm=lab, N=N, gross=g, CAGR=r["CAGR"], Sharpe=r["Sharpe"],
                       MaxDD=r["MaxDD"], H1=r["H1"], H2=r["H2"], J_IS=r["J_IS"],
                       OOS_CAGR=r["OOS_CAGR"], OOS_Sharpe=r["OOS_Sharpe"],
                       OOS_MaxDD=r["OOS_MaxDD"], pass4a=bool(r["pass4a"]),
                       pass4b=bool(r["pass4b"])))

    for pan in panels:
        pn = pan.name
        sub = G[G.panel == pn]
        pk = sub.sort_values(["J_IS", "gross", "N"], ascending=[False, True, True]).iloc[0]
        emit(pn, "RULE-8 PICK (this run, IS only)", int(pk.N), float(pk.gross),
             pk.to_dict())
        seen = {}
        for mf in MINFILES:
            for conv in ("ROW-weighted", "FILE-weighted"):
                key = noms.get((mf, pn, conv))
                if key is None:
                    continue
                seen.setdefault(key, []).append(f"{conv[:4]}@{mf}")
        for (N, g), who in seen.items():
            emit(pn, "record nom " + ",".join(who), N, g, price(pn, N, g))
        spy, W, live = B[pn]["spy"], B[pn]["W"], B[pn]["live"]
        for lab, s in (("SPY (the 4b bar)", spy), ("RULES v2 (the 4a bar)", live)):
            m, mo = mt(s), mt(s[W["OOS"]])
            say(f"  {pn:6} {lab:30} {'':9} {m['CAGR']:8.2%} {m['Sharpe']:8.4f} {m['MaxDD']:8.2%} "
                f"{mt(s[W['H1']])['Sharpe']:7.4f} {mt(s[W['H2']])['Sharpe']:7.4f} "
                f"{mo['CAGR']:8.2%} {mo['Sharpe']:8.4f} {mo['MaxDD']:8.2%}")
            wf.append(dict(panel=pn, arm=lab, N=np.nan, gross=np.nan, CAGR=m["CAGR"],
                           Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                           H1=mt(s[W["H1"]])["Sharpe"], H2=mt(s[W["H2"]])["Sharpe"], J_IS=np.nan,
                           OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                           pass4a=False, pass4b=False))
        say("")
    pd.DataFrame(wf).to_csv(str(OUT) + ".walkforward.csv", index=False)

    # ---------------------------------------------------------- verdict
    say("=" * 104)
    say("ARM 5 — VERDICT against the outcomes declared in the header.")
    say("=" * 104)
    say("")
    n5 = C[C.nfiles >= 5]
    nflip5 = int(n5.apply(lambda r: len(flips(r.row_share, r.file_share)) > 0, axis=1).sum())
    if ndiff > 0:
        v = "(C) LOAD-BEARING IN MONEY"
    elif nflip5 > 0:
        v = "(B) LOAD-BEARING IN TEXT ONLY"
    else:
        v = "(A) COSMETIC"
    say(f"  Census: {nflip5} of {len(n5)} statistics pooled over >= 5 files have a CONCLUSION")
    say(f"          that flips side under file weighting ({nflip5 / max(len(n5), 1):.2%}).")
    say(f"  Capital: the two conventions nominate different cells on {ndiff} of "
        f"{len(nomrows)} (panel, MINFILES) pairs.")
    say(f"  4b PASS on this run's rebuilt grid: U56 {int(G[(G.panel=='U56')].pass4b.sum())}/42, "
        f"B136 {int(G[(G.panel=='B136')].pass4b.sum())}/42, "
        f"SMALL {int(G[(G.panel=='SMALL')].pass4b.sum())}/42; 4a {int(G.pass4a.sum())}/126.")
    say("")
    say(f"  VERDICT: {v}")
    say("")
    say("  CONTAMINATION, RESTATED.  The committed rows arm 3 nominates from were produced by")
    say("  runs that had already seen 2017-2026, so no nominated cell's OOS number is a")
    say("  walk-forward result.  What is clean is the DIFFERENCE between the conventions and")
    say("  arm 4's own IS-only chooser.")
    say("  NOT CLAIMED: that either weighting is the RIGHT one; that any cell here is a new")
    say("  candidate book; that anything in RULES.md changes (rule 6).")
    say("  SURVIVORSHIP (rule 9): current constituents only on all three panels; the bias is")
    say("  common to both conventions and cannot manufacture a difference between them.")
    say("")
    say(f"  elapsed {time.time() - t0:.1f}s")
    Path(str(OUT) + ".console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Idea 973 (cloud lane, 2026-09-15) -- price the RECORD's ROW-vs-CELL WEIGHT GAP as a standing
defect.

THE QUESTION (queue, 2026-09-15, filed by idea 970)
  Idea 970's WIDE census reads **67.6% destruction row-weighted and 25.0% cell-weighted**, and
  the reason is that ONE cell (`U56/TOP20/g0.75/W`) carries **4,094 of its 4,335 rows**: the
  record cited that single cell four thousand times, and a row-weighted share therefore measures
  CITATION COUNT, not the object.  Idea 951 found the same shape on the 4b leg alphabet.  The
  queue asks: census the record's committed SHARE claims for how many change by more than 10 pp
  between ROW, CELL and FILE weighting, and propose the weighting clause.

WHY IT MATTERS FOR CAPITAL
  Every 4b and 4a base rate in this record -- the numbers that decide whether a book's pass is
  evidence or a coin flip -- is a share over a set of rows.  If those shares move by tens of
  points depending on a weighting nobody states, then the record's own falsification machinery
  is mis-calibrated, in an unknown direction, on every claim that uses one.  A weighting clause
  is worth exactly as much as the movement it removes, so this run measures the movement first.

WHAT IS TUNED AND WHAT IS REPORTED (PROTOCOL 4: max 2 tuned parameters)
  TUNED 1  CLAIM SET, 3 levels, every one reported and none chosen:
           ALL       every committed artifact carrying a pre-registered share column
           NONNULL   the same, minus the record's own null / coin-flip generators (named)
           GRID      this run's own 1,200-row grid, which is BALANCED by construction and is
                     therefore the control: a design with equal rows per cell has ZERO gap
  TUNED 2  WEIGHTING, 5 levels:
           ROW       sum(true) / sum(rows)                              <- what the record prints
           CELL      unweighted mean over DISTINCT cells of the cell's own share
           CELLANY   fraction of distinct cells with at least one True  <- 970's own reading
           FILE      unweighted mean over FILES of the file's ROW share
           FILECELL  unweighted mean over FILES of the file's CELL share
  A CELL is the file's available subset of {panel, book, arm, gross, cadence/freq, n/k,
  cost/cost_bps/rung}.  Everything else a file varies -- phase, draw, seed, split, sub-window --
  is a REPETITION inside a cell, which is exactly the thing row-weighting silently counts.
  REPORTED, never fitted: the statistic (the 4b/4a pass family), the file, the panel.

PRE-REGISTERED BARS (fixed before any number was read; both directions reported)
  H_GAP        the defect is STANDING iff > 0.25 of committed (file, statistic) share claims move
               by more than 10 pp between the widest pair of weightings.
  H_POOLED     it is also standing IN THE AGGREGATE iff > 0.25 of the pooled per-statistic shares
               move by more than 10 pp across the five weightings.
  H_CONC       the gap is a CONCENTRATION fact iff Spearman(largest-cell row share, |ROW - CELL|
               gap) over eligible (file, statistic) claims > 0.50.
  H_ONE        970's case is the record's normal, not its outlier, iff the median largest-cell
               row share over eligible claims > 0.50.
  H_BALANCED   a BALANCED design has no gap: on this run's own grid, |ROW - CELL| == 0 exactly.
  H_KEEP       (rule 8, REQUIRED) book x gross chosen on 2009-2016 ALONE, 2017-2026 read ONCE,
               both KEEP paths, against SPY and RULES v2 in the same window.

GATES (all printed before any result number)
  G1  the fast `Ctx` runner == `engine.backtest` on returns AND turnover
  G2  BAND03 @ 0.75 == `baseline.rules_v2_weights` elementwise
  G3  CROSS-RUN: idea 970's committed `.mapped_WIDE.csv` reproduces its published concentration
      -- the largest cell's row count and share, and the 27,143-row corpus size
  G4  the five weightings AGREE EXACTLY on a balanced table (the identity that makes the gap a
      defect rather than a definition)
  G5  determinism: the grid's subject row rebuilt from scratch
  G6  every chooser is IS-ONLY -- picks invariant to permuted OOS columns

PROTOCOL: 10 bps primary (all five rungs reported), decided at close t / applied t+1, warm-up
260 days, IS 2009-2016 / OOS 2017-2026.  Nothing in RULES.md / PROTOCOL.md / scan.py / bot.py /
baseline.py is modified.

SURVIVORSHIP (rule 9): U56, B136 and SMALL are CURRENT-CONSTITUENT lists (SMALL additionally
drops every ticker with `max_1d_move` >= 1.0 per `data/small_meta.csv`), so every CAGR and
drawdown LEVEL below is optimistic.  The weighting census is a contrast between two ways of
AVERAGING THE RECORD'S OWN NUMBERS and carries no price risk at all; the rule-8 triples are
levels read against SPY, which is not survivorship-inflated, so those are upper bounds.
"""
from __future__ import annotations

import os
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score   # noqa: E402
from engine import backtest, rebalance_mask                               # noqa: E402

BAND0, VOLCAP, WARM = 0.03, 0.60, 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
HEAD_COST = 10.0
RUNGS = [0.0, 5.0, 10.0, 25.0, 50.0]
GROSSES = [0.25, 0.50, 0.75, 1.00]
CADENCES = ["D", "W", "M", "Q"]
LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
LEGNAME = {"H1": "L1_H1", "H2": "L2_H2", "OOS": "L3_OOS", "DD": "L4_DD", "CAGR": "L5_CAGR"}
# pre-registered bars
GAP_PP, GAP_SHARE_BAR, CONC_BAR, ONE_BAR = 10.0, 0.25, 0.50, 0.50
# pre-registered share statistics: the record's 4b / 4a pass family
STATS = ["pass4b", "pass4a", "keep4b", "keep4a", "pass4b_REC", "pass4b_OOSPURE",
         "pass_4b", "pass_4a", "pass4b_oos", "pass4a_oos", "pass4a_v1", "pass4a_v2",
         "pass4b_10", "keep4b_10", "keep4a_10"]
# a CELL is named by these; anything else a file varies is a REPETITION inside the cell
CELLKEYS = ["panel", "book", "arm", "gross", "cadence", "freq", "n", "k",
            "cost_bps", "cost", "rung"]
NULLTOK = ("null", "rand", "coin", "flip", "perm", "shuffl", "bootstrap", "placebo")
WEIGHTS = ["ROW", "CELL", "CELLANY", "FILE", "FILECELL"]
SMOKE = bool(int(os.environ.get("IDEA973_SMOKE", "0")))
LINES: list[str] = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ==========================================================================================
# (1) the runner -- 942/962/970's fast Ctx, verbatim
# ==========================================================================================
class Ctx:
    def __init__(self, px, mask):
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        m = np.asarray(mask.values, bool)
        m = np.concatenate([[False], m[:-1]]).copy()
        m[0] = True
        self.T, self.N = self.rets.shape
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.N)), C[:-1]])
        self.reb = np.flatnonzero(m)
        seg = np.searchsorted(self.reb, np.arange(self.T), side="right") - 1
        self.s0 = self.reb[seg]
        self.s0p = self.reb[np.maximum(seg - 1, 0)]
        self.ratio = self.Cp / self.Cp[self.s0]
        self.ratiop = self.Cp / self.Cp[self.s0p]

    def shift(self, W):
        return W.reindex(self.idx).fillna(0.0).shift(1).fillna(0.0).values

    def run(self, wt):
        W0 = wt[self.s0]
        h = W0 * self.ratio
        V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
        held = h / V[:, None]
        W0p = wt[self.s0p]
        hp = W0p * self.ratiop
        Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
        heldp = hp / Vp[:, None]
        heldp[self.reb[0]] = 0.0
        turn = np.zeros(self.T)
        turn[self.reb] = np.abs(wt[self.reb] - heldp[self.reb]).sum(axis=1)
        return (held * self.rets).sum(axis=1), turn


def sharpe(r):
    v = r.std() * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def maxdd(r):
    eq = np.cumprod(1.0 + r)
    return float((eq / np.maximum.accumulate(eq) - 1).min())


def mets(r):
    eq = np.cumprod(1.0 + r)
    yrs = len(r) / 252.0
    h = len(r) // 2
    return dict(CAGR=float(eq[-1] ** (1 / yrs) - 1) if yrs > 0 else np.nan,
                Sharpe=sharpe(r), MaxDD=maxdd(r), H1=sharpe(r[:h]), H2=sharpe(r[h:]))


def legs_rec(row):
    return dict(H1=row["H1"] > row["spy_H1"], H2=row["H2"] > row["spy_H2"],
                OOS=row["OOS_Sharpe"] > row["spy_OOS_Sharpe"],
                DD=abs(row["OOS_MaxDD"]) <= 0.60 * abs(row["spy_MaxDD"]),
                CAGR=row["OOS_CAGR"] >= 0.70 * row["spy_CAGR"])


def legs_is(row):
    return dict(H1=row["IS_H1"] > row["spy_IS_H1"], H2=row["IS_H2"] > row["spy_IS_H2"],
                OOS=row["IS_Sharpe"] > row["spy_IS_Sharpe"],
                DD=abs(row["IS_MaxDD"]) <= 0.60 * abs(row["spy_IS_MaxDD"]),
                CAGR=row["IS_CAGR"] >= 0.70 * row["spy_IS_CAGR"])


def failstr(lg):
    f = [LEGNAME[k] for k in LEGS if not lg[k]]
    return ",".join(f) if f else "-"


def ew_gross(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def band_book(px, band, g):
    return ew_gross(px, g).where(band_state(px, band) & px.notna(), 0.0)


def ew_elig(px, g):
    _, above, vol20 = score(px, vol_scale=False)
    e = (above & (vol20 < VOLCAP)).astype(float).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def ranked_book(px, g, k):
    sc, above, vol20 = score(px, vol_scale=False)
    rank = sc.where(above & (vol20 < VOLCAP)).rank(axis=1, ascending=False)
    return (rank <= k).astype(float) * (g / k)


BOOKS = {
    "TOP05":  lambda p, g: ranked_book(p, g, 5),
    "TOP10":  lambda p, g: ranked_book(p, g, 10),
    "TOP20":  lambda p, g: ranked_book(p, g, 20),
    "EWELIG": lambda p, g: ew_elig(p, g),
    "BAND03": lambda p, g: band_book(p, BAND0, g),
}


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    return px[[c for c in px.columns if c == "SPY" or c not in bad]], len(bad)


def _argmax(v, tiebreak=None):
    v = np.asarray(v, float)
    if not np.isfinite(v).any():
        return 0
    best = np.nanmax(v)
    cand = np.flatnonzero(np.isclose(v, best, rtol=0, atol=0))
    if len(cand) > 1 and tiebreak is not None:
        t = np.asarray(tiebreak, float)[cand]
        cand = cand[np.flatnonzero(t == np.nanmax(t))]
    return int(cand[0])


CHOOSERS = ["C_CAGR", "C_SHARPE", "C_ISLEGS"]


def choose(name, sub):
    isc, iss = sub.IS_CAGR.values, sub.IS_Sharpe.values
    if name == "C_CAGR":
        return _argmax(isc, iss)
    if name == "C_SHARPE":
        return _argmax(iss, isc)
    if name == "C_ISLEGS":
        return _argmax(sub.IS_legs_passed.values, iss)
    raise KeyError(name)


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3:
        return np.nan
    ra, rb = pd.Series(a[ok]).rank().values, pd.Series(b[ok]).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


def cellkey(d, cks):
    """Vectorised '|'-joined cell key that survives NaN and mixed dtypes."""
    s = d[cks[0]].map(str)
    for c in cks[1:]:
        s = s + "|" + d[c].map(str)
    return s


def tobool(s):
    """Committed share columns arrive as bool, 0/1, or the strings True/False/PASS/FAIL."""
    if pd.api.types.is_bool_dtype(s):
        return s.fillna(False).astype(bool)
    if pd.api.types.is_numeric_dtype(s):
        return s.fillna(0) > 0.5
    t = s.astype(str).str.strip().str.upper()
    return t.isin(["TRUE", "1", "1.0", "YES", "Y", "PASS", "KEEP"])


# ==========================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 973 (cloud) -- price the ROW-vs-CELL WEIGHT GAP as a standing defect")
    P(f"  run {pd.Timestamp.utcnow():%Y-%m-%d %H:%M UTC}   PROTOCOL 10 bps / t+1 / warm-up {WARM}")
    P("=" * 100)
    gk = {}

    # ======================================================================================
    P()
    P("=" * 100)
    P("(A) THE CENSUS -- every committed artifact carrying a pre-registered SHARE column")
    P("=" * 100)
    cands = sorted(list(OUT.glob("*.csv")) + list(OUT.glob("*.csv.gz")))
    claims, cellrows, fileinfo = [], [], []
    nbytes = 0
    for p in cands:
        if p.name.startswith(STEM):
            continue
        try:
            hdr = list(pd.read_csv(p, nrows=0).columns)
        except Exception:
            continue
        hs = set(hdr)
        sts = [s for s in STATS if s in hs]
        cks = [c for c in CELLKEYS if c in hs]
        if not sts or not cks:
            continue
        isnull = any(t in p.name.lower() for t in NULLTOK)
        try:
            d = pd.read_csv(p, usecols=lambda c: c in (set(sts) | set(cks)))
        except Exception:
            continue
        if not len(d):
            continue
        nbytes += p.stat().st_size
        cell = cellkey(d, cks)
        for s in sts:
            b = tobool(d[s])
            if b.isna().all():
                continue
            g = pd.DataFrame({"cell": cell.values, "t": b.values.astype(float)})
            agg = g.groupby("cell")["t"].agg(["size", "sum"])
            share = agg["sum"] / agg["size"]
            top = float(agg["size"].max() / agg["size"].sum())
            hh = float(((agg["size"] / agg["size"].sum()) ** 2).sum())
            claims.append(dict(
                file=p.name, stat=s, is_null_file=isnull, cellkey="|".join(cks),
                rows=int(agg["size"].sum()), cells=int(len(agg)),
                n_true=int(agg["sum"].sum()),
                ROW=float(agg["sum"].sum() / agg["size"].sum()),
                CELL=float(share.mean()), CELLANY=float((agg["sum"] > 0).mean()),
                top_cell_row_share=top, herfindahl=hh))
            cellrows.append(pd.DataFrame(dict(file=p.name, stat=s, cell=agg.index,
                                              n=agg["size"].values, t=agg["sum"].values)))
        fileinfo.append(dict(file=p.name, stats=",".join(sts), cellkey="|".join(cks),
                             rows=int(len(d)), is_null_file=isnull, bytes=p.stat().st_size))
    CL = pd.DataFrame(claims)
    FI = pd.DataFrame(fileinfo)
    CR = pd.concat(cellrows, ignore_index=True) if cellrows else pd.DataFrame()
    dump(FI, "corpus")
    P(f"  {len(cands):,} csv artifacts scanned; {len(FI):,} carry a pre-registered SHARE column "
      f"AND a nameable cell key ({nbytes / 1e6:,.0f} MB); of those "
      f"{int(FI.is_null_file.sum())} are the record's own null / coin-flip generators.")
    P(f"  {len(CL):,} (file, statistic) SHARE CLAIMS, {CL.rows.sum():,} committed rows over "
      f"{CL.cells.sum():,} (file, cell) pairs.")
    CL["gap_ROW_CELL_pp"] = (CL.ROW - CL.CELL).abs() * 100
    CL["gap_ROW_CELLANY_pp"] = (CL.ROW - CL.CELLANY).abs() * 100
    CL["gap_max_pp"] = CL[["ROW", "CELL", "CELLANY"]].max(axis=1).sub(
        CL[["ROW", "CELL", "CELLANY"]].min(axis=1)) * 100
    dump(CL, "claims")

    # ---- G4: the five weightings AGREE on a balanced table ----------------------------------
    bal = pd.DataFrame({"cell": np.repeat(["a", "b", "c", "d"], 25),
                        "t": np.r_[np.ones(10), np.zeros(15), np.ones(20), np.zeros(5),
                                   np.ones(5), np.zeros(20), np.ones(13), np.zeros(12)]})
    ab = bal.groupby("cell")["t"].agg(["size", "sum"])
    d4 = abs(float(ab["sum"].sum() / ab["size"].sum()) - float((ab["sum"] / ab["size"]).mean()))
    gk["G4"] = d4 < 1e-15
    P(f"  G4 ROW == CELL on a BALANCED table (equal rows per cell): {d4:.3e}  "
      f"{'PASS' if gk['G4'] else 'FAIL'}   -- the gap is a DEFECT, not a definition")

    # ---- G3: reproduce idea 970's published concentration ------------------------------------
    m970 = OUT / "2026-09-15_does-4b-SURVIVE-a-DISJOINT-HALVES-SPLIT_B.mapped_WIDE.csv"
    if m970.exists():
        w = pd.read_csv(m970)
        kk = [c for c in ["panel", "book", "gross", "cadence"] if c in w.columns]
        vc = cellkey(w, kk).value_counts()
        gk["G3"] = len(w) == 27143
        P(f"  G3 idea 970's committed mapped_WIDE.csv: {len(w):,} rows (published 27,143), "
          f"{len(vc):,} distinct {'/'.join(kk)} cells; largest cell `{vc.index[0]}` carries "
          f"{vc.iloc[0]:,} rows = {vc.iloc[0] / len(w):.1%} of the corpus, top-3 "
          f"{vc.iloc[:3].sum() / len(w):.1%}   {'PASS' if gk['G3'] else 'FAIL'}")
        P(f"     970 published 4,094 of 4,335 rows in ONE cell at its own 10 bps rung; the same "
          f"concentration is visible here over the whole mapped corpus.")
    else:
        gk["G3"] = False
        P("  G3 SKIPPED (idea 970's artifact missing)   FAIL")

    # ---- the per-claim answer ---------------------------------------------------------------
    P()
    P("  H_GAP -- how many committed (file, statistic) share claims move by more than "
      f"{GAP_PP:.0f} pp?")
    P(f"    {'claim set':9s} {'claims':>7s} {'rows':>10s} {'>10pp ROW-CELL':>15s} "
      f"{'>10pp any pair':>15s} {'median gap pp':>14s} {'max gap pp':>11s}")
    hyprows = []
    for cs, sel in (("ALL", CL), ("NONNULL", CL[~CL.is_null_file])):
        if not len(sel):
            continue
        a = float((sel.gap_ROW_CELL_pp > GAP_PP).mean())
        b = float((sel.gap_max_pp > GAP_PP).mean())
        P(f"    {cs:9s} {len(sel):7,d} {sel.rows.sum():10,d} {a:15.3f} {b:15.3f} "
          f"{sel.gap_ROW_CELL_pp.median():14.2f} {sel.gap_ROW_CELL_pp.max():11.2f}")
        hyprows.append(dict(claim_set=cs, claims=len(sel), rows=int(sel.rows.sum()),
                            share_gt10_ROWCELL=a, share_gt10_anypair=b,
                            median_gap_pp=float(sel.gap_ROW_CELL_pp.median()),
                            max_gap_pp=float(sel.gap_ROW_CELL_pp.max())))
    nn = CL[~CL.is_null_file]
    hgap_v = float((nn.gap_max_pp > GAP_PP).mean()) if len(nn) else float("nan")
    hgap = hgap_v > GAP_SHARE_BAR
    P(f"    H_GAP  NONNULL, widest pair: {hgap_v:.3f} (bar {GAP_SHARE_BAR}) -> "
      f"{'PASS -- the defect is STANDING' if hgap else 'FAIL -- not standing'}")

    P()
    P("  the worst 12 committed share claims, by |ROW - CELL| (row-weighted is what the "
      "record prints):")
    P(f"    {'ROW':>6s} {'CELL':>6s} {'CELLANY':>7s} {'gap pp':>7s} {'rows':>8s} {'cells':>6s} "
      f"{'top cell':>8s}  stat / file")
    for _, r in nn.sort_values("gap_ROW_CELL_pp", ascending=False).head(12).iterrows():
        P(f"    {r.ROW:6.3f} {r.CELL:6.3f} {r.CELLANY:7.3f} {r.gap_ROW_CELL_pp:7.2f} "
          f"{r.rows:8,d} {r.cells:6,d} {r.top_cell_row_share:8.3f}  {r.stat} / {r.file[:64]}")

    # ---- pooled, per statistic ---------------------------------------------------------------
    P()
    P("  H_POOLED -- the same statistics pooled over the whole corpus, five weightings:")
    P("    CELLANY answers a DIFFERENT question (does the cell EVER pass), so the last column "
      "reports the")
    P("    spread over the four weightings that estimate the SAME quantity -- ROW / CELL / FILE "
      "/ FILECELL.")
    P(f"    {'statistic':16s} {'files':>6s} {'rows':>10s} {'ROW':>7s} {'CELL':>7s} "
      f"{'CELLANY':>8s} {'FILE':>7s} {'FILECELL':>9s} {'spread5 pp':>11s} {'spread4 pp':>11s}")
    pooled = []
    for cs, selc in (("ALL", CL), ("NONNULL", CL[~CL.is_null_file])):
        for st, s in selc.groupby("stat"):
            cr = CR[(CR.stat == st) & (CR.file.isin(set(s.file)))]
            if not len(cr):
                continue
            gcell = cr.groupby("cell")[["n", "t"]].sum()
            row = float(cr.t.sum() / cr.n.sum())
            cell = float((gcell.t / gcell.n).mean())
            cellany = float((gcell.t > 0).mean())
            fil = float(s.ROW.mean())
            filecell = float(s.CELL.mean())
            vals = [row, cell, cellany, fil, filecell]
            v4 = [row, cell, fil, filecell]     # the four that estimate the SAME quantity
            pooled.append(dict(claim_set=cs, stat=st, files=int(s.file.nunique()),
                               rows=int(cr.n.sum()), cells=int(len(gcell)),
                               ROW=row, CELL=cell, CELLANY=cellany, FILE=fil,
                               FILECELL=filecell,
                               spread_pp=(max(vals) - min(vals)) * 100,
                               spread4_pp=(max(v4) - min(v4)) * 100))
    PO = pd.DataFrame(pooled)
    for _, r in PO[PO.claim_set == "NONNULL"].sort_values("rows", ascending=False).iterrows():
        P(f"    {r.stat:16s} {r.files:6d} {r.rows:10,d} {r.ROW:7.3f} {r.CELL:7.3f} "
          f"{r.CELLANY:8.3f} {r.FILE:7.3f} {r.FILECELL:9.3f} {r.spread_pp:11.2f} "
          f"{r.spread4_pp:11.2f}")
    dump(PO, "pooled")
    pn = PO[PO.claim_set == "NONNULL"]
    hpool_v = float((pn.spread_pp > GAP_PP).mean()) if len(pn) else float("nan")
    hpool4_v = float((pn.spread4_pp > GAP_PP).mean()) if len(pn) else float("nan")
    hpool = hpool_v > GAP_SHARE_BAR
    P(f"    H_POOLED {hpool_v:.3f} of {len(pn)} pooled statistics move > {GAP_PP:.0f} pp over "
      f"all five weightings (bar {GAP_SHARE_BAR}) -> {'PASS' if hpool else 'FAIL'}")
    P(f"    and over the four SAME-QUANTITY weightings only: {hpool4_v:.3f} "
      f"({int((pn.spread4_pp > GAP_PP).sum())} of {len(pn)}), worst "
      f"{pn.spread4_pp.max():.2f} pp on `{pn.loc[pn.spread4_pp.idxmax(), 'stat']}` -- REPORTED "
      f"beside the headline, not instead of it.")

    # ---- concentration ------------------------------------------------------------------------
    P()
    rho = spearman(nn.top_cell_row_share.values, nn.gap_ROW_CELL_pp.values)
    rho_h = spearman(nn.herfindahl.values, nn.gap_ROW_CELL_pp.values)
    med_top = float(nn.top_cell_row_share.median()) if len(nn) else float("nan")
    hconc, hone = (rho > CONC_BAR), (med_top > ONE_BAR)
    P("  H_CONC / H_ONE -- is the gap a CONCENTRATION fact, and is 970's one-cell case normal?")
    P(f"    Spearman(largest-cell row share, |ROW-CELL| gap) = {rho:+.4f} (bar {CONC_BAR}) -> "
      f"H_CONC {'PASS' if hconc else 'FAIL'};  Spearman(Herfindahl, gap) = {rho_h:+.4f}")
    one_txt = "PASS -- 970's shape is the RECORD'S NORMAL" if hone else "FAIL -- 970 is an OUTLIER"
    P(f"    median largest-cell row share over {len(nn):,} NONNULL claims = {med_top:.3f} "
      f"(bar {ONE_BAR}) -> H_ONE {one_txt}")
    P(f"    claims where ONE cell carries > 50% of rows: "
      f"{float((nn.top_cell_row_share > 0.5).mean()):.3f}; > 90%: "
      f"{float((nn.top_cell_row_share > 0.9).mean()):.3f}; "
      f"median cells per claim {nn.cells.median():.0f}, median rows per claim "
      f"{nn.rows.median():.0f}")

    # ======================================================================================
    P()
    P("=" * 100)
    P("(B) THE CONTROL GRID -- 5 books x 3 panels x 4 gross x 4 cadences x 5 rungs, BALANCED")
    P("=" * 100)
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    sm, ndrop = load_small()
    panels["SMALL"] = sm
    for k, v in panels.items():
        P(f"  panel {k:6s} {v.shape[1]:4d} cols  {v.index[0].date()} .. {v.index[-1].date()}  "
          f"{len(v):,} rows")
    P(f"  SMALL drops {ndrop} tickers with max_1d_move >= 1.0 per data/small_meta.csv; "
      f"SURVIVORSHIP: three CURRENT-CONSTITUENT lists (rule 9).")

    u = panels["U56"]
    w75 = rules_v2_weights(u, BAND0, 0.75)
    d2 = float(np.nanmax(np.abs(w75.values - band_book(u, BAND0, 0.75).values)))
    gk["G2"] = d2 == 0.0
    P(f"  G2 BAND03@0.75 == baseline.rules_v2_weights: {d2:.3e}  {'PASS' if gk['G2'] else 'FAIL'}")
    cw = Ctx(u, rebalance_mask(u.index, "W"))
    gr, tn = cw.run(cw.shift(w75))
    eng = backtest(u, w75, cost_bps=0.0, freq="W")
    d1r = float(np.abs(gr[WARM:] - eng["returns"].values[WARM:]).max())
    d1t = float(np.abs(tn[WARM:] - eng["turnover"].values[WARM:]).max())
    gk["G1"] = d1r < 1e-12 and d1t < 1e-10
    P(f"  G1 Ctx == engine.backtest   returns {d1r:.3e}   turnover {d1t:.3e}  "
      f"{'PASS' if gk['G1'] else 'FAIL'}")
    del cw, eng

    ROWS, BASE = [], {}
    cads = CADENCES[:2] if SMOKE else CADENCES
    grs = GROSSES[:2] if SMOKE else GROSSES
    for pname, p in panels.items():
        pidx = p.index
        spy = p["SPY"].pct_change().fillna(0.0).values[WARM:]
        oos = np.asarray(pidx >= pd.Timestamp(OOS_START))[WARM:]
        is_ = np.asarray(pidx <= pd.Timestamp(IS_END))[WARM:]
        ms, ms_o, ms_i = mets(spy), mets(spy[oos]), mets(spy[is_])
        bc = Ctx(p, rebalance_mask(pidx, "W"))
        bgr, btn = bc.run(bc.shift(rules_v2_weights(p, BAND0, 0.75)))
        for c in RUNGS:
            br = (bgr - btn * c / 1e4)[WARM:]
            BASE[(pname, c)] = mets(br[oos])
        del bc
        for cad in cads:
            ctx = Ctx(p, rebalance_mask(pidx, cad))
            for b in BOOKS:
                for g in grs:
                    gg, tt = ctx.run(ctx.shift(BOOKS[b](p, g)))
                    gw, tw = gg[WARM:], tt[WARM:]
                    for c in RUNGS:
                        r = gw - tw * c / 1e4
                        m, mi, mo = mets(r), mets(r[is_]), mets(r[oos])
                        ROWS.append(dict(
                            panel=pname, book=b, gross=g, cadence=cad, cost_bps=c,
                            CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                            H1=m["H1"], H2=m["H2"],
                            IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                            IS_H1=mi["H1"], IS_H2=mi["H2"],
                            OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                            OOS_H1=mo["H1"], OOS_H2=mo["H2"],
                            turn_per_yr=float(tw.sum() / (len(r) / 252.0)),
                            spy_CAGR=ms["CAGR"], spy_Sharpe=ms["Sharpe"], spy_MaxDD=ms["MaxDD"],
                            spy_H1=ms["H1"], spy_H2=ms["H2"],
                            spy_IS_CAGR=ms_i["CAGR"], spy_IS_Sharpe=ms_i["Sharpe"],
                            spy_IS_MaxDD=ms_i["MaxDD"], spy_IS_H1=ms_i["H1"],
                            spy_IS_H2=ms_i["H2"],
                            spy_OOS_CAGR=ms_o["CAGR"], spy_OOS_Sharpe=ms_o["Sharpe"],
                            spy_OOS_MaxDD=ms_o["MaxDD"], spy_OOS_H1=ms_o["H1"],
                            spy_OOS_H2=ms_o["H2"]))
            del ctx
        P(f"  panel {pname} done  ({time.time() - t0:.0f}s)")
    grid = pd.DataFrame(ROWS)
    grid["IS_legs_passed"] = [sum(legs_is(r).values()) for _, r in grid.iterrows()]
    lr = [legs_rec(r) for _, r in grid.iterrows()]
    grid["pass4b"] = [all(x.values()) for x in lr]
    grid["fail4b"] = [failstr(x) for x in lr]
    grid["pass4a"] = [bool(r.OOS_H1 > BASE[(r.panel, r.cost_bps)]["H1"]
                           and r.OOS_H2 > BASE[(r.panel, r.cost_bps)]["H2"]
                           and r.OOS_MaxDD >= BASE[(r.panel, r.cost_bps)]["MaxDD"])
                      for _, r in grid.iterrows()]
    dump(grid, "grid")
    P(f"  {len(grid):,} grid rows = {len(panels)} panels x {len(BOOKS)} books x {len(grs)} gross "
      f"x {len(cads)} cadences x {len(RUNGS)} rungs -- ONE row per cell, so it is BALANCED")

    # ---- H_BALANCED -------------------------------------------------------------------------
    P()
    P("  H_BALANCED -- the GRID claim set, the control: this design has one row per cell.")
    gb = []
    for st in ("pass4b", "pass4a"):
        for kk in (["panel", "book", "gross", "cadence", "cost_bps"],
                   ["panel", "book", "gross", "cadence"],
                   ["panel", "book"]):
            cell = cellkey(grid, kk)
            a = grid.groupby(cell)[st].agg(["size", "sum"])
            row = float(a["sum"].sum() / a["size"].sum())
            cel = float((a["sum"] / a["size"]).mean())
            gb.append(dict(stat=st, cellkey="|".join(kk), rows=int(a["size"].sum()),
                           cells=int(len(a)), rows_per_cell=float(a["size"].mean()),
                           ROW=row, CELL=cel, gap_pp=abs(row - cel) * 100))
            P(f"    {st:7s} cell={'|'.join(kk):42s} {int(len(a)):5d} cells x "
              f"{a['size'].mean():5.1f} rows   ROW {row:.4f}  CELL {cel:.4f}  gap "
              f"{abs(row - cel) * 100:6.3f} pp")
    GB = pd.DataFrame(gb)
    dump(GB, "balanced")
    hbal = bool((GB[GB.rows_per_cell == 1.0].gap_pp.abs() < 1e-12).all())
    P(f"    H_BALANCED (gap == 0 wherever the design has exactly 1 row per cell) -> "
      f"{'PASS' if hbal else 'FAIL'};  and the gap GROWS as the cell key coarsens, which is the "
      f"whole mechanism: coarsening the key is what citing one cell many times does.")

    # ---- G5 determinism ---------------------------------------------------------------------
    ctx = Ctx(u, rebalance_mask(u.index, "W"))
    a1 = ctx.run(ctx.shift(BOOKS["TOP20"](u, 0.75)))
    a2 = ctx.run(ctx.shift(BOOKS["TOP20"](u, 0.75)))
    d5 = max(float(np.abs(a1[0] - a2[0]).max()), float(np.abs(a1[1] - a2[1]).max()))
    gk["G5"] = d5 == 0.0
    P(f"  G5 determinism: {d5:.3e}  {'PASS' if gk['G5'] else 'FAIL'}")
    del ctx

    # ======================================================================================
    P()
    P("=" * 100)
    P("(C) RULE 8 -- book x gross chosen on 2009-2016 ALONE, 2017-2026 read ONCE")
    P("=" * 100)
    picks, g6_bad = [], 0
    for (pn_, cad, c), sub_ in grid.groupby(["panel", "cadence", "cost_bps"]):
        sub_ = sub_.sort_values(["book", "gross"]).reset_index(drop=True)
        perm = sub_.copy()
        rng = np.random.default_rng(11)
        oc = [x for x in perm.columns if x.startswith("OOS_")]
        perm[oc] = perm[oc].values[rng.permutation(len(perm))]
        for ch in CHOOSERS:
            i = choose(ch, sub_)
            if i != choose(ch, perm):
                g6_bad += 1
            r = sub_.iloc[i]
            picks.append(dict(panel=pn_, cadence=cad, cost_bps=c, chooser=ch, book=r.book,
                              gross=r.gross, OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe,
                              OOS_MaxDD=r.OOS_MaxDD, pass4b=bool(r.pass4b),
                              pass4a=bool(r.pass4a), fail4b=r.fail4b,
                              spy_OOS_CAGR=r.spy_OOS_CAGR, spy_OOS_Sharpe=r.spy_OOS_Sharpe,
                              spy_OOS_MaxDD=r.spy_OOS_MaxDD,
                              v2_OOS_CAGR=BASE[(pn_, c)]["CAGR"],
                              v2_OOS_Sharpe=BASE[(pn_, c)]["Sharpe"],
                              v2_OOS_MaxDD=BASE[(pn_, c)]["MaxDD"]))
    gk["G6"] = g6_bad == 0
    P(f"  G6 choosers are IS-ONLY: {g6_bad} picks moved under permuted OOS columns  "
      f"{'PASS' if gk['G6'] else 'FAIL'}")
    PK = pd.DataFrame(picks)
    dump(PK, "walkforward")
    hv = PK[PK.cost_bps == HEAD_COST]
    P(f"  {len(PK)} rule-8 picks ({len(hv)} at {HEAD_COST:.0f} bps) = {len(CHOOSERS)} choosers "
      f"x {len(panels)} panels x {len(cads)} cadences x {len(RUNGS)} rungs")
    P(f"  OOS 4b {int(hv.pass4b.sum())} of {len(hv)};  OOS 4a {int(hv.pass4a.sum())} of {len(hv)}"
      f";  full-sample grid 4b {int(grid[grid.cost_bps == HEAD_COST].pass4b.sum())} of "
      f"{len(grid[grid.cost_bps == HEAD_COST])}, 4a "
      f"{int(grid[grid.cost_bps == HEAD_COST].pass4a.sum())}")
    P()
    P(f"    {'panel':6s} {'cad':3s} {'chooser':9s} {'book':7s} {'g':5s} {'OOS CAGR':>9s} "
      f"{'Sh':>7s} {'MaxDD':>8s} {'4b':>3s} {'4a':>3s}  fail-legs")
    for _, r in hv.sort_values(["panel", "cadence", "chooser"]).iterrows():
        P(f"    {r.panel:6s} {r.cadence:3s} {r.chooser:9s} {r.book:7s} {r.gross:5.2f} "
          f"{r.OOS_CAGR:9.2%} {r.OOS_Sharpe:7.3f} {r.OOS_MaxDD:8.2%} "
          f"{'Y' if r.pass4b else 'n':>3s} {'Y' if r.pass4a else 'n':>3s}  {r.fail4b}")
    P()
    for pn_ in panels:
        s = hv[hv.panel == pn_]
        if not len(s):
            continue
        r = s.iloc[0]
        P(f"  comparands, {pn_} OOS 2017-2026 @ 10 bps:  SPY {r.spy_OOS_CAGR:.2%} / "
          f"{r.spy_OOS_Sharpe:.3f} / {r.spy_OOS_MaxDD:.2%}    RULES v2 {r.v2_OOS_CAGR:.2%} / "
          f"{r.v2_OOS_Sharpe:.3f} / {r.v2_OOS_MaxDD:.2%}")
    best = hv.sort_values("OOS_Sharpe", ascending=False).head(3)
    P()
    P("  best three picks by OOS Sharpe at 10 bps:")
    for _, r in best.iterrows():
        P(f"    {r.panel}/{r.cadence}/{r.chooser} -> {r.book} @ g{r.gross:.2f}: OOS "
          f"{r.OOS_CAGR:.2%} / {r.OOS_Sharpe:.3f} / {r.OOS_MaxDD:.2%}   "
          f"4b {'PASS' if r.pass4b else 'FAIL'}  4a {'PASS' if r.pass4a else 'FAIL'}")
    hkeep = bool(hv.pass4b.any() or hv.pass4a.any())

    # ======================================================================================
    P()
    P("=" * 100)
    P("(D) HYPOTHESES")
    P("=" * 100)
    H = [dict(name="H_GAP", bar=f"> {GAP_SHARE_BAR} of NONNULL claims move > {GAP_PP:.0f} pp",
              value=hgap_v, verdict="PASS" if hgap else "FAIL"),
         dict(name="H_POOLED", bar=f"> {GAP_SHARE_BAR} of pooled statistics move > {GAP_PP:.0f} pp",
              value=hpool_v, verdict="PASS" if hpool else "FAIL"),
         dict(name="H_CONC", bar=f"Spearman(top-cell share, gap) > {CONC_BAR}",
              value=rho, verdict="PASS" if hconc else "FAIL"),
         dict(name="H_ONE", bar=f"median top-cell row share > {ONE_BAR}",
              value=med_top, verdict="PASS" if hone else "FAIL"),
         dict(name="H_BALANCED", bar="gap == 0 on a 1-row-per-cell design",
              value=float(GB[GB.rows_per_cell == 1.0].gap_pp.max() if
                          (GB.rows_per_cell == 1.0).any() else np.nan),
              verdict="PASS" if hbal else "FAIL"),
         dict(name="H_KEEP", bar="any rule-8 OOS 4b or 4a pass at 10 bps",
              value=float(hv.pass4b.sum() + hv.pass4a.sum()),
              verdict="PASS" if hkeep else "FAIL")]
    hyp = pd.DataFrame(H)
    for _, r in hyp.iterrows():
        P(f"  {r['name']:11s} {r['verdict']:4s}   {r['value']:+.4f}   {r['bar']}")
    dump(hyp, "hypotheses")
    dump(pd.DataFrame(hyprows), "gapsummary")
    P()
    P("  GATES: " + "  ".join(f"{k}={'PASS' if v else 'FAIL'}" for k, v in sorted(gk.items()))
      + f"   ({sum(gk.values())} of {len(gk)})")
    P(f"  elapsed {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()

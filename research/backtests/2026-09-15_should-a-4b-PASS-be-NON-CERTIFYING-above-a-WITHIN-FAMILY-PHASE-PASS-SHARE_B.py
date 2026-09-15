#!/usr/bin/env python3
"""Idea 976 (lane B, 2026-09-15) -- should a 4b PASS be NON-CERTIFYING above a WITHIN-FAMILY
PHASE PASS SHARE?

THE QUESTION (queue, 2026-09-15, filed by idea 964)
  Idea 964 proposed labelling a committed 4b pass NON-CERTIFYING wherever its own rebalance-phase
  family's within-family pass share exceeds 0.25, and found the single OOS 4b pass it turned up
  (U56 / Q / EWELIG @ gross 0.75) sits at 0.413 -- 26 of that family's 63 phases clear 4b
  unaided.  The queue asks: compute that share for EVERY committed M/Q 4b PASS row the record
  carries, report how many the 0.25 bar would re-label, AND report whether the bar has any
  POWER -- its distribution under the record's own nulls.

WHY IT MATTERS FOR CAPITAL
  The record already knows how to ask whether a 4b pass is a fluke: build a gross-matched
  coin-flip null for its cell and read the null's 4b base rate (ideas 680 / 926 / 942).  That
  costs 500 book-scorings per claim and nobody does it routinely.  The phase family is a
  DIFFERENT and much cheaper control that the record can compute from grids it already owns:
  hold the rule fixed and move only the DAY it rebalances.  If the within-family pass share
  tracks the null base rate, the record gets its fluke detector for 21-63 runs instead of 500,
  and a bar on it is a real screening clause.  If it does not track the null, the bar is a
  restatement of "this cell is easy" with no power, and adopting it would re-label real passes
  and fake ones at the same rate.  This run prices BOTH readings and never conflates them.

WHAT IS TUNED AND WHAT IS REPORTED (PROTOCOL 4: max 2 tuned parameters)
  TUNED 1  BAR, 4 levels, every one reported and none chosen: 0.10 / 0.25 / 0.50 / 0.75.
  TUNED 2  CLAIM SET, 3 levels, every one reported and none chosen:
           STRICT  committed rows with pass4b == True, cadence in {M, Q}, phase 0 (or no phase
                   column -- the record's default IS the canonical), whose (panel, book, gross)
                   maps exactly onto this run's grid
           WIDE    the same but at ANY phase, and with gross defaulted to CORE where the
                   artifact does not carry one, each row mapped to its family
           GRID    the 60 families themselves -- the record-INDEPENDENT version of the same
                   question (every family carries a canonical claim whether or not anyone
                   published it)
  REPORTED AXES (nothing fitted on them, every point published): panel U56 / B136 / SMALL;
  book TOP05 / TOP10 / TOP20 / EWELIG / BAND03; gross CORE 0.75 / EXT 1.00; cadence M (21
  phases) / Q (63 phases); cost rung 0 / 5 / 10 / 25 / 50 bps; weighting row / claim / family.

PRE-REGISTERED BARS (fixed before any number below was read; both directions reported)
  H_RELABEL   the bar is CONSEQUENTIAL iff the share of STRICT committed 4b passes re-labelled
              non-certifying at bar 0.25 lies strictly inside (0.10, 0.90).  Below 0.10 it is
              inert; above 0.90 it is a blanket ban on M/Q passes, not a screen.
  H_PROXY     the family share is a CHEAP PROXY FOR THE NULL iff Spearman(within-family real
              pass share, that family's OWN gross-matched coin-flip 4b base rate) >= +0.50 over
              the 60 families at 10 bps.  THIS IS THE HYPOTHESIS THAT WOULD MAKE THE BAR WORTH
              ADOPTING.
  H_SEPAR     the share DISCRIMINATES iff median share over families whose CANONICAL passes 4b
              minus median share over families whose canonical FAILS is >= +0.10.
  H_NULLSHARE the bar has POWER AGAINST CHANCE iff the median within-family pass share of NULL
              families exceeds that of REAL families by >= 0.10 at 10 bps.  If a coin flip's
              phase family is exactly as crowded with passes as a rule's, the share cannot tell
              a fluke from a rule and the bar is measuring the CELL, not the CLAIM.
  H_CHOOSE    (rule 8, REQUIRED) the bar PAYS AS A SCREEN iff, over the 18 (panel x cadence x
              chooser) picks made on 2009-2016 alone, screening candidates on IS-only family
              share <= 0.25 raises BOTH the OOS 4b pass count and the mean OOS Sharpe against
              the same chooser unscreened.

GATES (all printed before any result number)
  G0  `offset_mask(idx, per, 0)` == `engine.rebalance_mask(idx, per)` on M / Q / W
  G1  the fast `Ctx` runner == `engine.backtest` on returns AND turnover, post warm-up
  G2  BAND03 @ 0.75 == `baseline.rules_v2_weights` elementwise
  G3  CROSS-RUN: idea 964's committed `.grid.csv` reproduced on all 12,600 rows
  G4  idea 964's published headline share: U56 / Q / EWELIG / CORE @ 10 bps == 26 of 63 = 0.413
  G5  null gross match: per-name weight and holding count identical to the book's on every
      rebalance row of every family
  G6  determinism: one family rebuilt from scratch, max|d| over every reported column
  G7  every chooser is IS-ONLY -- picks invariant to permuted OOS columns

PROTOCOL: 10 bps primary (all five rungs reported), decided at close t / applied t+1, warm-up
260 days, IS 2009-2016 / OOS 2017-2026 read once, no shorting, no leverage beyond the published
gross.  Nothing in RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py is modified.

SURVIVORSHIP (rule 9): U56, B136 and SMALL are CURRENT-CONSTITUENT lists (SMALL additionally
drops every ticker with `max_1d_move` >= 1.0 per `data/small_meta.csv`), so every CAGR and
drawdown LEVEL below is optimistic and both 4b bars are easier here than on a point-in-time
panel.  The within-family SHARE contrasts are the same names on the same tape under different
rebalance DAYS and are very nearly immune to it.  A coin flip drawn from a survivor panel is a
BETTER book than one drawn in real time, so every null share and base rate below is an UPPER
bound -- which cuts AGAINST this run's own power hypothesis rather than for it.  The rule-8 4b
levels are read against SPY, which is not survivorship-inflated, so every 4b PASS is an upper
bound and every FAIL is understated.  Stated, not hidden.
"""
from __future__ import annotations

import glob
import os
import re
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
GROSSES = {"CORE": 0.75, "EXT": 1.00}
CADENCES = {"M": 21, "Q": 63}
RUNGS = [0.0, 5.0, 10.0, 25.0, 50.0]
LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
LEGNAME = {"H1": "L1_H1", "H2": "L2_H2", "OOS": "L3_OOS", "DD": "L4_DD", "CAGR": "L5_CAGR"}
BARS = [0.10, 0.25, 0.50, 0.75]
HEAD_BAR = 0.25
SEED0 = 20260976
D_FAM = 10       # null draws evaluated on EVERY phase of a family (the share distribution)
D_BASE = 100     # null draws at the CANONICAL phase only (the family's own 4b base rate)
# pre-registered bars
RELABEL_LO, RELABEL_HI = 0.10, 0.90
PROXY_BAR, SEPAR_BAR, NULLSHARE_BAR = 0.50, 0.10, 0.10
REF_GRID = OUT / "2026-09-15_should-the-PHASE-AVERAGED-MEAN-replace-the-CANONICAL_cloud.grid.csv"
SMOKE = bool(int(os.environ.get("IDEA976_SMOKE", "0")))
LINES: list[str] = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ==========================================================================================
# (1) phase machinery -- copied VERBATIM from ideas 938 / 942 / 962 / 964 so this run NESTS
#     the record and G3 can be an EXACT cross-run reproduction rather than a resemblance.
# ==========================================================================================
def offset_mask(idx, per, d):
    """True d trading days BEFORE the last trading day of each period.  d = 0 reproduces
    engine.rebalance_mask(idx, per) exactly (G0)."""
    key = pd.Series(idx.to_period(per), index=idx)
    last = np.flatnonzero((key != key.shift(-1)).values)
    first = np.concatenate([[0], last[:-1] + 1])
    pick = np.maximum(last - d, first)
    out = pd.Series(False, index=idx)
    out.iloc[np.unique(pick)] = True
    return out, int((last - d < first).sum())


class Ctx:
    """Fast runner -- byte-identical to 942 / 962 / 964's.  G1 asserts it against
    engine.backtest.  `dec` (the DECISION rows, reb - 1) is added for the null draws; 926 draws
    on the decision rows so the t+1 roll holds the drawn names rather than cash."""

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
        self.dec = np.maximum(self.reb - 1, 0)
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


def spearman(a, b):
    """Rank correlation without scipy (the sandbox has none): Pearson on average ranks."""
    a, b = pd.Series(np.asarray(a, float)), pd.Series(np.asarray(b, float))
    ok = a.notna() & b.notna()
    if ok.sum() < 3:
        return np.nan
    return float(a[ok].rank().corr(b[ok].rank()))


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
    """The RECORD's 4b convention (942 / 962 / 964's, verbatim)."""
    return dict(H1=row["H1"] > row["spy_H1"], H2=row["H2"] > row["spy_H2"],
                OOS=row["OOS_Sharpe"] > row["spy_OOS_Sharpe"],
                DD=abs(row["OOS_MaxDD"]) <= 0.60 * abs(row["spy_MaxDD"]),
                CAGR=row["OOS_CAGR"] >= 0.70 * row["spy_CAGR"])


def legs_is(row):
    """The same alphabet read ENTIRELY INSIDE the IS window -- chooser / screen input only (G7)."""
    return dict(H1=row["IS_H1"] > row["spy_IS_H1"], H2=row["IS_H2"] > row["spy_IS_H2"],
                OOS=row["IS_Sharpe"] > row["spy_IS_Sharpe"],
                DD=abs(row["IS_MaxDD"]) <= 0.60 * abs(row["spy_IS_MaxDD"]),
                CAGR=row["IS_CAGR"] >= 0.70 * row["spy_IS_CAGR"])


def failstr(lg):
    f = [LEGNAME[k] for k in LEGS if not lg[k]]
    return ",".join(f) if f else "-"


# ==========================================================================================
# (2) THE BOOK SET -- 942 / 962 / 964's five books verbatim
# ==========================================================================================
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
# which pool a book's gross-matched coin flip draws from (926's construction, verbatim)
POOLKIND = {"TOP05": "ROT", "TOP10": "ROT", "TOP20": "ROT", "EWELIG": "EW", "BAND03": "BD"}
BOOKORDER = list(BOOKS)


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    return px[[c for c in px.columns if c == "SPY" or c not in bad]], len(bad)


def cand_pool(px):
    """The eligibility mask the ranked books rank inside -- the ROT null's pool."""
    sc, above, vol20 = score(px, vol_scale=False)
    elig = above & (vol20 < VOLCAP)
    return (elig & sc.notna()).values, px.notna().values


# ==========================================================================================
# (3) NULL: gross-matched rotating coin flips (idea 926's `null_streams`, verbatim in
#     construction: count and per-name weight copied from the book on every rebalance row, only
#     WHICH names are held is redrawn)
# ==========================================================================================
def topmask(E, take, rng):
    R = rng.random(E.shape)
    R[~E] = -1.0
    order = np.argsort(-R, axis=1)
    pos = np.argsort(order, axis=1)
    return (pos < take[:, None]) & E


def null_weights(ctx, wt_book, pool, kind, bkidx, draw, buf):
    """One gross-matched draw, written into `buf` (reused across draws to avoid re-allocating a
    T x N array 8,400 times per panel)."""
    reb, dec = ctx.reb, ctx.dec
    wrow = wt_book[reb]
    cnt = (wrow > 0).sum(axis=1)
    tot = wrow.sum(axis=1)
    perw = np.where(cnt > 0, tot / np.maximum(cnt, 1), 0.0)
    E = pool[dec]
    take = np.minimum(E.sum(axis=1), cnt)
    rng = np.random.default_rng(SEED0 + 1_000_000 * {"ROT": 0, "EW": 1, "BD": 2}[kind]
                                + 10_000 * bkidx + draw)
    buf[:] = 0.0
    buf[reb] = topmask(E, take, rng) * perw[:, None]
    return buf, cnt, perw


# ==========================================================================================
# (4) CHOOSERS -- IS columns only (G7)
# ==========================================================================================
def _argmax(v, tiebreak=None):
    v = np.asarray(v, float)
    if not np.isfinite(v).any():
        return None
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


# ==========================================================================================
# (5) the census: harvest the record's committed 4b PASS rows
# ==========================================================================================
PANEL_MAP = {"U56": "U56", "B136": "B136", "BROAD": "B136", "BROAD136": "B136",
             "SMALL": "SMALL", "SMALL439": "SMALL", "SMALL484": "SMALL", "SMALL663": "SMALL"}
BOOK_MAP = {"TOP5": "TOP05", "TOP05": "TOP05", "TOP10": "TOP10", "TOP20": "TOP20",
            "EWELIG": "EWELIG", "BAND03": "BAND03"}


def norm_panel(v):
    return PANEL_MAP.get(str(v).strip().upper())


def norm_book(v):
    return BOOK_MAP.get(str(v).strip().upper())


def norm_gross(v):
    try:
        g = round(float(v), 2)
    except Exception:
        return None
    return {0.75: "CORE", 1.0: "EXT"}.get(g)


def harvest():
    """Every committed CSV artifact carrying a `pass4b` column AND a cadence column.  Each row is
    mapped to (panel, book, gross, cadence, phase) where the artifact says so; unmapped rows are
    COUNTED and reported, never silently dropped."""
    fs = sorted(glob.glob(str(OUT / "*.csv")) + glob.glob(str(OUT / "*.csv.gz")))
    recs, corpus = [], []
    for f in fs:
        base = os.path.basename(f)
        if base.startswith(STEM):
            continue                                     # never census this run's own output
        try:
            head = pd.read_csv(f, nrows=0)
        except Exception:
            continue
        cols = list(head.columns)
        pcol = [c for c in cols if re.fullmatch(r"pass4b", c, re.I)]
        ccol = [c for c in cols if re.fullmatch(r"cadence|freq|cad", c, re.I)]
        if not (pcol and ccol):
            continue
        try:
            d = pd.read_csv(f)
        except Exception:
            continue
        pc, cc = pcol[0], ccol[0]
        cad = d[cc].astype(str).str.strip().str.upper()
        pas = d[pc].astype(str).str.strip().str.upper().isin(["TRUE", "1", "1.0", "YES"])
        mq = cad.isin(["M", "Q"])
        n_pass_mq = int((pas & mq).sum())
        sub = d.loc[pas & mq].copy()
        sub["_cadence"] = cad[pas & mq]
        sub["_panel"] = sub["panel"].map(norm_panel) if "panel" in sub.columns else None
        sub["_book"] = sub["book"].map(norm_book) if "book" in sub.columns else None
        sub["_gross"] = sub["gross"].map(norm_gross) if "gross" in sub.columns else None
        sub["_phase"] = pd.to_numeric(sub["phase"], errors="coerce") if "phase" in sub.columns else np.nan
        sub["_hasphase"] = "phase" in d.columns
        sub["_file"] = base
        recs.append(sub[["_file", "_panel", "_book", "_gross", "_cadence", "_phase", "_hasphase"]])
        corpus.append(dict(file=base, rows=len(d), pass4b_MQ=n_pass_mq,
                           has_panel=int("panel" in d.columns), has_book=int("book" in d.columns),
                           has_gross=int("gross" in d.columns), has_phase=int("phase" in d.columns)))
    C = pd.concat(recs, ignore_index=True) if recs else pd.DataFrame()
    return C, pd.DataFrame(corpus)


# ==========================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 976 (lane B) -- should a 4b PASS be NON-CERTIFYING above a WITHIN-FAMILY PHASE PASS SHARE?")
    P(f"  run {pd.Timestamp.utcnow():%Y-%m-%d %H:%M UTC}   PROTOCOL 10 bps / t+1 / warm-up {WARM}")
    P(f"  null draws: {D_FAM} per family x every phase (the SHARE distribution), "
      f"{D_BASE} at the canonical phase (the family's own 4b BASE RATE)")
    P("=" * 100)

    panels = {"U56": load_universe()}
    if not SMOKE:
        panels["B136"] = load_universe(broad=True)
        sm, ndrop = load_small()
        panels["SMALL"] = sm
    else:
        ndrop = 0
    for k, v in panels.items():
        P(f"  panel {k:6s} {v.shape[1]:4d} cols  {v.index[0].date()} .. {v.index[-1].date()}  {len(v):,} rows")
    P(f"  SMALL drops {ndrop} tickers with max_1d_move >= 1.0 per data/small_meta.csv; "
      f"SURVIVORSHIP: all panels are CURRENT-CONSTITUENT lists (rule 9).")

    # ------------------------------------------------------------------------------ gates A
    P()
    P("=" * 100)
    P("(A) GATES -- printed before any result number")
    P("=" * 100)
    gk, gdetail = {}, []
    u = panels["U56"]
    idx = u.index

    g0 = sum(int((offset_mask(idx, per, 0)[0].values != rebalance_mask(idx, per).values).sum())
             for per in ("M", "Q", "W"))
    gk["G0"] = g0 == 0
    P(f"  G0 offset_mask(.,per,0) == engine.rebalance_mask on M/Q/W: {g0} disagreeing rows  "
      f"{'PASS' if gk['G0'] else 'FAIL'}")
    gdetail.append(dict(gate="G0", stat=float(g0), bar=0.0, passed=gk["G0"],
                        what="offset_mask(d=0) == engine.rebalance_mask on M/Q/W"))

    w75 = rules_v2_weights(u, BAND0, 0.75)
    d2 = float(np.nanmax(np.abs(w75.values - band_book(u, BAND0, 0.75).values)))
    gk["G2"] = d2 == 0.0
    P(f"  G2 BAND03@0.75 == baseline.rules_v2_weights: {d2:.3e}  {'PASS' if gk['G2'] else 'FAIL'}")
    gdetail.append(dict(gate="G2", stat=d2, bar=0.0, passed=gk["G2"],
                        what="BAND03@0.75 == baseline.rules_v2_weights elementwise"))

    ctxM = Ctx(u, offset_mask(idx, "M", 0)[0])
    gr, tn = ctxM.run(ctxM.shift(w75))
    eng = backtest(u, w75, cost_bps=0.0, freq="M")
    d1r = float(np.abs(gr[WARM:] - eng["returns"].values[WARM:]).max())
    d1t = float(np.abs(tn[WARM:] - eng["turnover"].values[WARM:]).max())
    gk["G1"] = d1r < 1e-12 and d1t < 1e-12
    P(f"  G1 Ctx == engine.backtest (monthly, post warm-up): dret {d1r:.3e}  dturn {d1t:.3e}  "
      f"{'PASS' if gk['G1'] else 'FAIL'}")
    gdetail.append(dict(gate="G1", stat=max(d1r, d1t), bar=1e-12, passed=gk["G1"],
                        what="fast Ctx runner == engine.backtest on returns AND turnover"))

    # ------------------------------------------------------------------- B: the phase grid
    P()
    P("=" * 100)
    P("(B) THE PHASE GRID -- every (panel, book, gross, cadence, phase) scored at 5 cost rungs")
    P("=" * 100)
    rows, nullrows, gross_gap, det_store = [], [], [], {}
    cads = list(CADENCES) if not SMOKE else ["M"]
    for pname, px in panels.items():
        rets_spy = px["SPY"].pct_change().fillna(0.0).values
        cpool, priced = cand_pool(px)
        pools = {"ROT": cpool, "EW": priced, "BD": priced}
        isw = np.asarray(px.index <= pd.Timestamp(IS_END))
        osw = np.asarray(px.index >= pd.Timestamp(OOS_START))
        spy_full, spy_is, spy_oos = (mets(rets_spy[WARM:]), mets(rets_spy[WARM:][isw[WARM:]]),
                                     mets(rets_spy[osw]))
        wts = {(bk, gn): BOOKS[bk](px, gv) for bk in BOOKS for gn, gv in GROSSES.items()}
        buf = np.zeros((len(px), px.shape[1]))
        for cad in cads:
            nph = CADENCES[cad] if not SMOKE else 3
            for ph in range(nph):
                m, clipped = offset_mask(px.index, cad, ph)
                ctx = Ctx(px, m)
                shifted = {k: ctx.shift(v) for k, v in wts.items()}
                for bi, bk in enumerate(BOOKORDER):
                    for gn, gv in GROSSES.items():
                        wt = shifted[(bk, gn)]
                        r, tu = ctx.run(wt)
                        for cb in RUNGS:
                            net = r - tu * cb / 1e4
                            f, i_, o_ = (mets(net[WARM:]), mets(net[WARM:][isw[WARM:]]), mets(net[osw]))
                            row = dict(panel=pname, book=bk, gross=gn, cadence=cad, phase=ph,
                                       cost_bps=cb, clipped=clipped,
                                       turn_per_yr=float(tu[WARM:].sum() / (len(tu[WARM:]) / 252.0)))
                            for k, v in f.items():
                                row[k] = v
                            for k, v in i_.items():
                                row["IS_" + k] = v
                            for k, v in o_.items():
                                row["OOS_" + k] = v
                            for k, v in spy_full.items():
                                row["spy_" + k] = v
                            for k, v in spy_is.items():
                                row["spy_IS_" + k] = v
                            for k, v in spy_oos.items():
                                row["spy_OOS_" + k] = v
                            lr, li = legs_rec(row), legs_is(row)
                            row["IS_legs_passed"] = int(sum(li.values()))
                            row["pass4b_REC"] = bool(all(lr.values()))
                            row["fail4b_REC"] = failstr(lr)
                            row["pass4b_IS"] = bool(all(li.values()))
                            row["pass4a"] = bool(np.nan)  # placeholder, filled below vs RULES v2
                            rows.append(row)
                        if cad == cads[0] and ph == 0 and bk == "BAND03" and gn == "CORE":
                            det_store[pname] = (r.copy(), tu.copy())
                # ---- nulls on this phase
                nd = D_FAM + (D_BASE - D_FAM if ph == 0 else 0)
                for bi, bk in enumerate(BOOKORDER):
                    kind = POOLKIND[bk]
                    for gn, gv in GROSSES.items():
                        wt = shifted[(bk, gn)]
                        bcnt = (wt[ctx.reb] > 0).sum(axis=1)
                        btot = wt[ctx.reb].sum(axis=1)
                        bper = np.where(bcnt > 0, btot / np.maximum(bcnt, 1), 0.0)
                        for d in range(nd):
                            nw, cnt, perw = null_weights(ctx, wt, pools[kind], kind,
                                                         bi * 2 + (gn == "EXT"), d, buf)
                            if d == 0:
                                gross_gap.append(dict(panel=pname, book=bk, gross=gn, cadence=cad,
                                                      phase=ph,
                                                      d_count=float(np.abs((nw[ctx.reb] > 0).sum(axis=1) - bcnt).max()),
                                                      d_perw=float(np.abs(perw - bper).max())))
                            r, tu = ctx.run(nw)
                            net = r - tu * HEAD_COST / 1e4
                            f, o_ = mets(net[WARM:]), mets(net[osw])
                            nr = dict(panel=pname, book=bk, gross=gn, cadence=cad, phase=ph, draw=d)
                            for k, v in f.items():
                                nr[k] = v
                            for k, v in o_.items():
                                nr["OOS_" + k] = v
                            for k, v in spy_full.items():
                                nr["spy_" + k] = v
                            for k, v in spy_oos.items():
                                nr["spy_OOS_" + k] = v
                            nr["pass4b_REC"] = bool(all(legs_rec(nr).values()))
                            nullrows.append({k: nr[k] for k in
                                             ("panel", "book", "gross", "cadence", "phase", "draw",
                                              "Sharpe", "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD",
                                              "pass4b_REC")})
            P(f"  {pname:6s} {cad}  {nph} phases x 10 book-gross x {len(RUNGS)} rungs done "
              f"[{time.time()-t0:6.0f}s]")
    G = pd.DataFrame(rows)
    NU = pd.DataFrame(nullrows)
    P(f"  grid {len(G):,} rows / {G.shape[1]} cols ; nulls {len(NU):,} book-scorings")

    # 4a needs the LIVE baseline (RULES v2, weekly) on each panel -- computed once per panel
    for pname, px in panels.items():
        b = backtest(px, rules_v2_weights(px), cost_bps=HEAD_COST, freq="W")["returns"].values
        bm = mets(b[WARM:])
        sel = G.panel == pname
        G.loc[sel, "v2_Sharpe"] = bm["Sharpe"]
        G.loc[sel, "v2_H1"] = bm["H1"]
        G.loc[sel, "v2_H2"] = bm["H2"]
        G.loc[sel, "v2_MaxDD"] = bm["MaxDD"]
    G["pass4a"] = (G.H1 > G.v2_H1) & (G.H2 > G.v2_H2) & (G.MaxDD >= G.v2_MaxDD)

    # ------------------------------------------------------------------------- gates B
    P()
    gg = pd.DataFrame(gross_gap)
    g5 = float(max(gg.d_count.max(), gg.d_perw.max()))
    gk["G5"] = g5 == 0.0
    P(f"  G5 null gross match (holding count / per-name weight) over {len(gg)} families: "
      f"{g5:.3e}  {'PASS' if gk['G5'] else 'FAIL'}")
    gdetail.append(dict(gate="G5", stat=g5, bar=0.0, passed=gk["G5"],
                        what="null count and per-name weight == book's on every rebalance row"))

    # G3 cross-run against idea 964's committed grid
    if REF_GRID.exists() and not SMOKE:
        ref = pd.read_csv(REF_GRID)
        key = ["panel", "book", "gross", "cadence", "phase", "cost_bps"]
        cmpcols = [c for c in ref.columns if c in G.columns and
                   ref[c].dtype.kind in "fi" and c not in key]
        j = ref.merge(G, on=key, suffixes=("_ref", "_new"), how="inner")
        dmax, worst = 0.0, ""
        for c in cmpcols:
            d = float(np.nanmax(np.abs(j[c + "_ref"].values - j[c + "_new"].values)))
            if d > dmax:
                dmax, worst = d, c
        vref = ref.set_index(key).pass4b_REC.astype(bool)
        vnew = G.set_index(key).pass4b_REC.astype(bool)
        common = vref.index.intersection(vnew.index)
        vdis = int((vref.loc[common].values != vnew.loc[common].values).sum())
        gk["G3"] = len(j) == len(ref) and dmax < 1e-9 and vdis == 0
        P(f"  G3 CROSS-RUN vs idea 964's committed .grid.csv: matched {len(j):,} of {len(ref):,} rows, "
          f"max|d| {dmax:.3e} (on {worst}), {vdis} 4b-verdict disagreements  "
          f"{'PASS' if gk['G3'] else 'FAIL'}")
        gdetail.append(dict(gate="G3", stat=dmax, bar=1e-9, passed=gk["G3"],
                            what=f"exact reproduction of 964's 12,600-row grid ({len(j)} matched, "
                                 f"{vdis} verdict flips)"))
    else:
        gk["G3"] = False
        P("  G3 SKIPPED (reference grid absent or SMOKE)  FAIL")
        gdetail.append(dict(gate="G3", stat=np.nan, bar=1e-9, passed=False,
                            what="reference grid unavailable"))

    # ------------------------------------------------- C: within-family pass shares
    P()
    P("=" * 100)
    P("(C) WITHIN-FAMILY PHASE PASS SHARE -- the statistic the proposed bar reads")
    P("=" * 100)
    fam = (G.groupby(["panel", "book", "gross", "cadence", "cost_bps"])
             .agg(n_phase=("phase", "size"),
                  n_pass=("pass4b_REC", "sum"),
                  n_pass_IS=("pass4b_IS", "sum"),
                  n_pass4a=("pass4a", "sum")).reset_index())
    fam["share"] = fam.n_pass / fam.n_phase
    fam["share_IS"] = fam.n_pass_IS / fam.n_phase
    fam["share4a"] = fam.n_pass4a / fam.n_phase
    canon = G[G.phase == 0].set_index(["panel", "book", "gross", "cadence", "cost_bps"])
    fam = fam.join(canon[["pass4b_REC", "pass4a", "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD"]]
                   .rename(columns={"pass4b_REC": "canon_pass4b", "pass4a": "canon_pass4a",
                                    "OOS_Sharpe": "canon_OOS_Sharpe", "OOS_CAGR": "canon_OOS_CAGR",
                                    "OOS_MaxDD": "canon_OOS_MaxDD"}),
                   on=["panel", "book", "gross", "cadence", "cost_bps"])
    # the family's own gross-matched null 4b base rate (canonical phase, D_BASE draws)
    nb = (NU[NU.phase == 0].groupby(["panel", "book", "gross", "cadence"])
            .agg(null_base=("pass4b_REC", "mean"), null_n=("draw", "size")).reset_index())
    fam = fam.merge(nb, on=["panel", "book", "gross", "cadence"], how="left")
    # the NULL's own within-family share: for each draw, the share of that draw's phases passing
    nsh = (NU.groupby(["panel", "book", "gross", "cadence", "draw"])
             .agg(nph=("phase", "size"), npass=("pass4b_REC", "sum")).reset_index())
    nsh = nsh[nsh.nph > 1]                      # only draws evaluated on the WHOLE family
    nsh["null_share"] = nsh.npass / nsh.nph
    nfam = (nsh.groupby(["panel", "book", "gross", "cadence"])
              .agg(null_share_med=("null_share", "median"),
                   null_share_mean=("null_share", "mean"),
                   null_share_draws=("null_share", "size")).reset_index())
    fam = fam.merge(nfam, on=["panel", "book", "gross", "cadence"], how="left")
    dump(fam, "families")

    h = fam[fam.cost_bps == HEAD_COST]
    P(f"  {len(h)} families at 10 bps  (share = phases clearing 4b / phases in the family)")
    P("  share distribution: " + "  ".join(
        f"p{q}={h.share.quantile(q/100):.3f}" for q in (10, 25, 50, 75, 90)))
    P(f"  families with ANY phase passing 4b: {(h.share>0).sum()} of {len(h)};  "
      f"canonical passes: {int(h.canon_pass4b.sum())}")
    P()
    P("  by cadence and panel (median share / n families / canonical passes):")
    for cad in cads:
        for pn in panels:
            s = h[(h.cadence == cad) & (h.panel == pn)]
            if len(s):
                P(f"    {pn:6s} {cad}  med share {s.share.median():.3f}  "
                  f"mean {s.share.mean():.3f}  max {s.share.max():.3f}  "
                  f"canon 4b {int(s.canon_pass4b.sum())}/{len(s)}  "
                  f"null base {s.null_base.mean():.3f}  null share med {s.null_share_med.median():.3f}")
    P()
    P("  cost-rung sensitivity (median share over all families):")
    P("    " + "  ".join(f"{cb:.0f}bps={fam[fam.cost_bps==cb].share.median():.3f}" for cb in RUNGS))

    # G4 -- 964's published headline
    hit = h[(h.panel == "U56") & (h.cadence == "Q") & (h.book == "EWELIG") & (h.gross == "CORE")]
    if len(hit):
        n_p, n_t, sh = int(hit.n_pass.iloc[0]), int(hit.n_phase.iloc[0]), float(hit.share.iloc[0])
        gk["G4"] = (n_p == 26 and n_t == 63)
        P(f"  G4 idea 964's headline U56/Q/EWELIG/CORE @10bps: {n_p} of {n_t} = {sh:.3f} "
          f"(published 26 of 63 = 0.413)  {'PASS' if gk['G4'] else 'FAIL'}")
        gdetail.append(dict(gate="G4", stat=float(n_p), bar=26.0, passed=gk["G4"],
                            what=f"964's published within-family share reproduced: {n_p}/{n_t}"))
    else:
        gk["G4"] = False

    # --------------------------------------------------------------- D: the census
    P()
    P("=" * 100)
    P("(D) THE CENSUS -- every committed 4b PASS row the record carries on an M or Q cadence")
    P("=" * 100)
    C, corpus = harvest()
    dump(corpus, "corpus")
    P(f"  {len(corpus)} committed CSV artifacts carry BOTH a `pass4b` column and a cadence column")
    P(f"  {int(corpus.rows.sum()):,} rows scanned; {int(corpus.pass4b_MQ.sum()):,} are 4b PASS on M or Q")
    P(f"  key availability across those artifacts: panel {int(corpus.has_panel.sum())}, "
      f"book {int(corpus.has_book.sum())}, gross {int(corpus.has_gross.sum())}, "
      f"phase {int(corpus.has_phase.sum())} of {len(corpus)}")
    if len(C):
        C["mappable_strict"] = (C._panel.notna() & C._book.notna() & C._gross.notna()
                                & ((~C._hasphase) | (C._phase == 0)))
        C["_gross_wide"] = C._gross.fillna("CORE")
        C["mappable_wide"] = C._panel.notna() & C._book.notna()
        P(f"  STRICT mappable: {int(C.mappable_strict.sum()):,} rows "
          f"({C.mappable_strict.mean():.1%} of the {len(C):,} M/Q passes)")
        P(f"  WIDE   mappable: {int(C.mappable_wide.sum()):,} rows ({C.mappable_wide.mean():.1%})")
        P(f"  UNMAPPABLE: {int((~C.mappable_wide).sum()):,} rows -- reported, not dropped "
          f"(missing panel {int(C._panel.isna().sum()):,}, missing book {int(C._book.isna().sum()):,})")
    shmap = h.set_index(["panel", "book", "gross", "cadence"]).share
    nbmap = h.set_index(["panel", "book", "gross", "cadence"]).null_base

    def attach(sub, gcol):
        k = list(zip(sub._panel, sub._book, sub[gcol], sub._cadence))
        sub = sub.copy()
        sub["fam_share"] = [shmap.get(x, np.nan) for x in k]
        sub["fam_nullbase"] = [nbmap.get(x, np.nan) for x in k]
        return sub

    claimsets = {}
    if len(C):
        claimsets["STRICT"] = attach(C[C.mappable_strict], "_gross")
        claimsets["WIDE"] = attach(C[C.mappable_wide], "_gross_wide")
    gridrows = h[h.canon_pass4b].copy()
    gridrows["_file"] = "(grid, record-independent)"
    gridrows["fam_share"] = gridrows.share
    gridrows["fam_nullbase"] = gridrows.null_base
    claimsets["GRID"] = gridrows

    P()
    P("  RE-LABELLING TABLE -- share of committed 4b passes the bar calls NON-CERTIFYING")
    P(f"  {'claim set':10s} {'n rows':>8s} {'n families':>11s} {'med share':>10s} " +
      "".join(f"  bar {b:.2f}" for b in BARS))
    relab = []
    for cs, sub in claimsets.items():
        sub = sub[sub.fam_share.notna()]
        if not len(sub):
            continue
        keys = list(zip(sub._panel if "_panel" in sub else sub.panel,
                        sub._book if "_book" in sub else sub.book,
                        sub._cadence if "_cadence" in sub else sub.cadence))
        nfamu = len(set(keys))
        line = f"  {cs:10s} {len(sub):8,d} {nfamu:11d} {sub.fam_share.median():10.3f} "
        for b in BARS:
            fr = float((sub.fam_share > b).mean())
            line += f"  {fr:7.3f}"
            relab.append(dict(claim_set=cs, bar=b, n_rows=len(sub), relabelled=int((sub.fam_share > b).sum()),
                              frac=fr, weighting="row"))
        P(line)
    # claim-weighted (one vote per distinct family) -- idea 973's weighting clause
    P()
    P("  the same table FAMILY-WEIGHTED (one vote per distinct family; idea 973's clause):")
    for cs, sub in claimsets.items():
        sub = sub[sub.fam_share.notna()]
        if not len(sub):
            continue
        pcol = "_panel" if "_panel" in sub else "panel"
        bcol = "_book" if "_book" in sub else "book"
        ccol = "_cadence" if "_cadence" in sub else "cadence"
        uf = sub.drop_duplicates(subset=[pcol, bcol, ccol, "fam_share"])
        line = f"  {cs:10s} {len(uf):8,d} {'':11s} {uf.fam_share.median():10.3f} "
        for b in BARS:
            fr = float((uf.fam_share > b).mean())
            line += f"  {fr:7.3f}"
            relab.append(dict(claim_set=cs, bar=b, n_rows=len(uf), relabelled=int((uf.fam_share > b).sum()),
                              frac=fr, weighting="family"))
        P(line)
    RL = pd.DataFrame(relab)
    dump(RL, "relabel")
    if len(C):
        dump(C, "census")

    # --------------------------------------------------------- E: does the bar have POWER
    P()
    P("=" * 100)
    P("(E) POWER -- does the share tell a FLUKE from a RULE, or only an EASY CELL from a HARD one?")
    P("=" * 100)
    hv = h[h.null_base.notna() & h.share.notna()]
    rho = spearman(hv.share.values, hv.null_base.values)
    rp = float(pd.Series(hv.share.values).corr(pd.Series(hv.null_base.values)))
    P(f"  Spearman(real within-family share, family's own null 4b base rate) = {rho:+.4f} "
      f"(Pearson {rp:+.4f}, n = {len(hv)} families, {D_BASE} draws each)")
    pas, fai = h[h.canon_pass4b], h[~h.canon_pass4b]
    sep = float(pas.share.median() - fai.share.median()) if len(pas) and len(fai) else np.nan
    P(f"  median share | canonical PASSES 4b = {pas.share.median():.3f} (n={len(pas)});  "
      f"| canonical FAILS = {fai.share.median():.3f} (n={len(fai)});  gap {sep:+.3f}")
    ns_med = float(h.null_share_med.median())
    rs_med = float(h.share.median())
    P(f"  median within-family share, REAL books {rs_med:.3f} vs NULL books {ns_med:.3f}  "
      f"gap {ns_med-rs_med:+.3f}  ({D_FAM} null draws per family, each scored on every phase)")
    # --- reported, not gated: the PAIRED version of the same comparison, and the question
    #     "is the cheap statistic any better than the expensive one it is meant to replace?"
    pr = h[h.null_share_med.notna()]
    pdiff = (pr.null_share_med - pr.share)
    P(f"  PAIRED (same family, null minus real): median {pdiff.median():+.3f}, "
      f"mean {pdiff.mean():+.3f}, null >= real in {(pdiff>=0).mean():.3f} of {len(pr)} families; "
      f"means REAL {h.share.mean():.3f} vs NULL {h.null_share_mean.mean():.3f}")
    hp = hv[hv.canon_pass4b]
    P(f"  Spearman(share, null base) restricted to families whose CANONICAL passes: "
      f"{spearman(hp.share.values, hp.null_base.values):+.4f} (n = {len(hp)})")
    lab_share = (hv.share > HEAD_BAR).values
    lab_null = (hv.null_base > HEAD_BAR).values
    P(f"  the two labels at bar 0.25 agree on {(lab_share==lab_null).mean():.3f} of {len(hv)} "
      f"families (share flags {lab_share.sum()}, null base rate flags {lab_null.sum()}); "
      f"share-flags-but-null-does-not {int((lab_share & ~lab_null).sum())}, "
      f"null-flags-but-share-does-not {int((~lab_share & lab_null).sum())}")
    P()
    P("  per-family detail at 10 bps (share / null share / null base rate), families whose "
      "CANONICAL passes 4b:")
    for _, r in h[h.canon_pass4b].sort_values("share", ascending=False).iterrows():
        P(f"    {r.panel:6s} {r.book:6s} {r.gross:4s} {r.cadence}  share {r.share:.3f} "
          f"({int(r.n_pass):>2d}/{int(r.n_phase):>2d})  null share {r.null_share_med:.3f}  "
          f"null base {r.null_base:.3f}  OOS {r.canon_OOS_CAGR:6.2%} / {r.canon_OOS_Sharpe:.3f} / "
          f"{r.canon_OOS_MaxDD:7.2%}")

    # --------------------------------------------------------- F: rule 8 walk-forward
    P()
    P("=" * 100)
    P("(F) RULE 8 WALK-FORWARD -- (book, gross) chosen on 2009-2016 ALONE, 2017-2026 read ONCE")
    P("=" * 100)
    g10 = G[(G.cost_bps == HEAD_COST) & (G.phase == 0)].copy()
    isshare = fam[fam.cost_bps == HEAD_COST].set_index(["panel", "book", "gross", "cadence"]).share_IS
    g10["IS_fam_share"] = [isshare.get((r.panel, r.book, r.gross, r.cadence), np.nan)
                           for r in g10.itertuples()]
    picks = []
    for pn in panels:
        for cad in cads:
            sub0 = g10[(g10.panel == pn) & (g10.cadence == cad)]
            for ch in CHOOSERS:
                for screen in ("OFF", "ON"):
                    sub = sub0 if screen == "OFF" else sub0[sub0.IS_fam_share <= HEAD_BAR]
                    if not len(sub):
                        picks.append(dict(panel=pn, cadence=cad, chooser=ch, screen=screen,
                                          book="(empty)", gross="", note="screen empties the shelf"))
                        continue
                    i = choose(ch, sub)
                    if i is None:
                        continue
                    r = sub.iloc[i]
                    picks.append(dict(panel=pn, cadence=cad, chooser=ch, screen=screen,
                                      book=r.book, gross=r.gross,
                                      IS_fam_share=r.IS_fam_share,
                                      fam_share=float(shmap.get((r.panel, r.book, r.gross, r.cadence), np.nan)),
                                      OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe,
                                      OOS_MaxDD=r.OOS_MaxDD,
                                      spy_OOS_CAGR=r.spy_OOS_CAGR, spy_OOS_Sharpe=r.spy_OOS_Sharpe,
                                      spy_OOS_MaxDD=r.spy_OOS_MaxDD,
                                      v2_Sharpe=r.v2_Sharpe, v2_MaxDD=r.v2_MaxDD,
                                      pass4b=bool(r.pass4b_REC), fail4b=r.fail4b_REC,
                                      pass4a=bool(r.pass4a), note=""))
    W = pd.DataFrame(picks)
    dump(W, "walkforward")
    live = W[W.book != "(empty)"]
    P(f"  {len(W)} picks ({len(live)} live, {len(W)-len(live)} empty shelves)")
    P(f"  {'panel':6s} {'cad':3s} {'chooser':9s} {'scr':4s} {'book':7s} {'g':5s} "
      f"{'OOS CAGR':>9s} {'Sharpe':>7s} {'MaxDD':>8s} {'4b':>4s} {'4a':>4s}  binding leg")
    for _, r in W.iterrows():
        if r.book == "(empty)":
            P(f"  {r.panel:6s} {r.cadence:3s} {r.chooser:9s} {r.screen:4s} -- {r.note}")
            continue
        P(f"  {r.panel:6s} {r.cadence:3s} {r.chooser:9s} {r.screen:4s} {r.book:7s} {r.gross:5s} "
          f"{r.OOS_CAGR:9.2%} {r.OOS_Sharpe:7.3f} {r.OOS_MaxDD:8.2%} "
          f"{'PASS' if r.pass4b else 'fail':>4s} {'PASS' if r.pass4a else 'fail':>4s}  {r.fail4b}")
    sp = g10.iloc[0]
    P(f"  SPY OOS {sp.spy_OOS_CAGR:.2%} / {sp.spy_OOS_Sharpe:.3f} / {sp.spy_OOS_MaxDD:.2%}   "
      f"(4b bars: Sharpe > {sp.spy_OOS_Sharpe:.3f}, MaxDD >= {0.60*sp.spy_MaxDD:.2%}, "
      f"CAGR >= {0.70*sp.spy_CAGR:.2%})")
    for pn in panels:
        v = g10[g10.panel == pn].iloc[0]
        P(f"  RULES v2 (live) on {pn}: full-sample Sharpe {v.v2_Sharpe:.3f} MaxDD {v.v2_MaxDD:.2%}")
    on, off = live[live.screen == "ON"], live[live.screen == "OFF"]
    P()
    P(f"  screen OFF: OOS 4b {int(off.pass4b.sum())} of {len(off)}, 4a {int(off.pass4a.sum())} of {len(off)}, "
      f"mean OOS Sharpe {off.OOS_Sharpe.mean():.4f}, mean OOS CAGR {off.OOS_CAGR.mean():.2%}")
    P(f"  screen ON : OOS 4b {int(on.pass4b.sum())} of {len(on)}, 4a {int(on.pass4a.sum())} of {len(on)}, "
      f"mean OOS Sharpe {on.OOS_Sharpe.mean():.4f}, mean OOS CAGR {on.OOS_CAGR.mean():.2%}")
    P(f"  full-sample 4a over the whole {len(G[G.cost_bps==HEAD_COST]):,}-row 10 bps grid: "
      f"{int(G[(G.cost_bps==HEAD_COST)].pass4a.sum()):,}")

    # G7 -- choosers are IS-only
    perm = g10.copy()
    rng = np.random.default_rng(7)
    for c in [c for c in perm.columns if c.startswith("OOS_")]:
        perm[c] = rng.permutation(perm[c].values)
    g7bad = 0
    for pn in panels:
        for cad in cads:
            a0 = g10[(g10.panel == pn) & (g10.cadence == cad)]
            b0 = perm[(perm.panel == pn) & (perm.cadence == cad)]
            for ch in CHOOSERS:
                if choose(ch, a0) != choose(ch, b0):
                    g7bad += 1
    gk["G7"] = g7bad == 0
    P(f"  G7 choosers invariant to permuted OOS columns: {g7bad} disagreements  "
      f"{'PASS' if gk['G7'] else 'FAIL'}")
    gdetail.append(dict(gate="G7", stat=float(g7bad), bar=0.0, passed=gk["G7"],
                        what="every chooser is IS-only"))

    # G6 determinism
    pn = "U56"
    px = panels[pn]
    m, _ = offset_mask(px.index, cads[0], 0)
    c2 = Ctx(px, m)
    r2, t2 = c2.run(c2.shift(band_book(px, BAND0, 0.75)))
    d6 = float(max(np.abs(r2 - det_store[pn][0]).max(), np.abs(t2 - det_store[pn][1]).max()))
    gk["G6"] = d6 == 0.0
    P(f"  G6 determinism (U56/{cads[0]}/BAND03/CORE rebuilt from scratch): {d6:.3e}  "
      f"{'PASS' if gk['G6'] else 'FAIL'}")
    gdetail.append(dict(gate="G6", stat=d6, bar=0.0, passed=gk["G6"], what="rebuild determinism"))

    # ------------------------------------------------------------------ G: hypotheses
    P()
    P("=" * 100)
    P("(G) PRE-REGISTERED HYPOTHESES")
    P("=" * 100)
    hyp = []
    st = claimsets.get("STRICT")
    if st is not None and st.fam_share.notna().any():
        stv = st[st.fam_share.notna()]
        fr25 = float((stv.fam_share > HEAD_BAR).mean())
    else:
        fr25 = np.nan
    hyp.append(dict(H="H_RELABEL", stat=fr25, bar=f"in ({RELABEL_LO},{RELABEL_HI})",
                    passed=bool(RELABEL_LO < fr25 < RELABEL_HI) if fr25 == fr25 else False,
                    what="fraction of STRICT committed M/Q 4b passes re-labelled at bar 0.25"))
    hyp.append(dict(H="H_PROXY", stat=rho, bar=f">= {PROXY_BAR}", passed=bool(rho >= PROXY_BAR),
                    what="Spearman(family share, family's own gross-matched null 4b base rate)"))
    hyp.append(dict(H="H_SEPAR", stat=sep, bar=f">= {SEPAR_BAR}",
                    passed=bool(sep >= SEPAR_BAR) if sep == sep else False,
                    what="median share | canonical passes  minus  median share | canonical fails"))
    hyp.append(dict(H="H_NULLSHARE", stat=ns_med - rs_med, bar=f">= {NULLSHARE_BAR}",
                    passed=bool(ns_med - rs_med >= NULLSHARE_BAR),
                    what="median NULL within-family share minus median REAL within-family share"))
    ch_ok = (int(on.pass4b.sum()) > int(off.pass4b.sum())) and (on.OOS_Sharpe.mean() > off.OOS_Sharpe.mean())
    hyp.append(dict(H="H_CHOOSE", stat=float(on.OOS_Sharpe.mean() - off.OOS_Sharpe.mean()),
                    bar="4b count AND mean OOS Sharpe both up", passed=bool(ch_ok),
                    what=f"rule-8 screen ON ({int(on.pass4b.sum())}/{len(on)}) vs OFF "
                         f"({int(off.pass4b.sum())}/{len(off)})"))
    HY = pd.DataFrame(hyp)
    for _, r in HY.iterrows():
        P(f"  {r.H:12s} {'PASS' if r.passed else 'FAIL':4s}  stat {r.stat:+.4f}  bar {r.bar:32s}  {r.what}")
    dump(HY, "hypotheses")
    GA = pd.DataFrame(gdetail)
    dump(GA, "gates")
    P()
    P(f"  GATES {int(sum(gk.values()))} of {len(gk)} PASS  ({', '.join(k for k,v in gk.items() if not v) or 'none failed'})")
    P(f"  runtime {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    Gs = G[G.cost_bps == HEAD_COST].drop(columns=[c for c in G.columns if c.startswith("spy_IS_")])
    Gs.to_csv(OUT / f"{STEM}.grid10.csv", index=False)
    NU.to_csv(OUT / f"{STEM}.nulls.csv", index=False)
    print("wrote grid10.csv / nulls.csv")


if __name__ == "__main__":
    main()

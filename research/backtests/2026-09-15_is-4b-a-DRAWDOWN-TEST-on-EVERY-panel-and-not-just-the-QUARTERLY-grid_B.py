#!/usr/bin/env python3
"""Idea 981 (lane B, 2026-09-15) -- is 4b a DRAWDOWN TEST on EVERY panel, and not just on the
QUARTERLY grid?

THE QUESTION (queue, 2026-09-15, filed by idea 976)
  Idea 976 found `L4_DD` is the binding leg on 36 of 36 rule-8 picks and the ONLY failed leg on
  12 of them, across 3 panels and both M and Q.  Idea 968 asked the same question of the
  QUARTERLY grid alone, after finding L_DD binds on 89.2% of 768 quarterly phase-books.  The
  queue asks: re-run the leg census on the D / W / M / Q ladder at MATCHED GROSS across all
  three panels, and report whether 4b's binding leg is a CADENCE object, a PANEL object, or
  simply ALWAYS the DD cap.

WHY IT MATTERS FOR CAPITAL
  PROTOCOL rule 4b is a five-leg test (H1 Sharpe, H2 Sharpe, OOS Sharpe, MaxDD <= 60% of SPY's,
  OOS CAGR >= 70% of SPY's).  If one leg fails on essentially everything, then 4b is not a
  five-leg standard at all -- it is that one leg wearing four decorations, and every claim in
  the record of the form "this book passes 4b" is really "this book has a small drawdown".
  That changes what a KEEP means, and it changes which ideas are worth running: if the DD cap
  is the whole test on every cadence and every panel, the profitable research direction is
  drawdown control, not return.  If instead the binding leg MOVES with cadence or with panel,
  then 4b is doing genuine multi-dimensional work and the record's DD-heavy readings are an
  artefact of the M/Q grids the record happens to run most.  This run prices both readings on
  the same tape and never conflates them.

WHAT IS TUNED AND WHAT IS REPORTED (PROTOCOL 4: max 2 tuned parameters)
  TUNED 1  CADENCE LADDER, 3 variants, every one reported and none selected:
           CORE4    D / W / M / Q   (the queue's ladder -- the headline)
           COARSE3  W / M / Q       (976's and 968's implicit ladder)
           FINE2    D / W           (the high-turnover end alone)
           All three are SUBSETS of the single grid below, so no variant costs a re-fit.
  TUNED 2  PANEL SET, 4 variants, every one reported and none selected:
           U56 / B136 / SMALL / POOLED.
  REPORTED AXES (nothing fitted on them, every point published): book TOP05 / TOP10 / TOP20 /
  EWELIG / BAND03; gross CORE 0.75 / EXT 1.00 (MATCHED across the ladder by construction, G5);
  phase 0..P-1 within each cadence (D 1, W 5, M 21, Q 63); cost rung 0 / 5 / 10 / 25 / 50 bps;
  leg definition BIND_ANY / BIND_ONLY / TIGHTEST.

PRE-REGISTERED BARS (fixed before any number below was read; both directions reported)
  H_ALWAYS   4b is SIMPLY ALWAYS THE DD CAP iff `L4_DD`'s fail rate is >= 0.80 in EVERY one of
             the 12 (panel x cadence) cells of the CORE4 ladder at 10 bps.
  H_CAD      the binding leg is a CADENCE object iff the range of `L4_DD`'s fail rate across the
             4 cadences (pooled over panels) is >= 0.20.
  H_PANEL    the binding leg is a PANEL object iff the range of `L4_DD`'s fail rate across the
             3 panels (pooled over cadences) is >= 0.20.
  H_MODAL    `L4_DD` is the MODAL binding leg (strictly the most-failed of the five) in 12 of 12
             (panel x cadence) cells at 10 bps.
  H_ONLY     the DD cap is the leg that STANDS ALONE between a book and a pass iff, among
             FAILING phase-books, `L4_DD` is the only failed leg in >= 0.25 of rows in every one
             of the 12 cells.
  H_RULE8    (rule 8, REQUIRED) the DD cap binds OUT OF SAMPLE too iff `L4_DD` is among the
             failed legs on >= 0.90 of the live walk-forward picks.
  DECISION RULE, fixed in advance:
      H_ALWAYS pass and H_CAD fail and H_PANEL fail  -> ALWAYS THE DD CAP (a constant)
      H_CAD pass and H_PANEL fail                    -> a CADENCE object
      H_PANEL pass and H_CAD fail                    -> a PANEL object
      both pass                                      -> a CADENCE x PANEL object
      H_ALWAYS fail and neither                      -> none of the three; report the mixture

GATES (all printed before any result number)
  G0  `offset_mask(idx, per, 0)` == `engine.rebalance_mask(idx, per)` on D / W / M / Q
  G1  the fast `Ctx` runner == `engine.backtest` on returns AND turnover, post warm-up, on
      D and M (the two ends of the ladder that the engine supports natively)
  G2  BAND03 @ 0.75 == `baseline.rules_v2_weights` elementwise
  G3  CROSS-RUN: idea 976's committed `.grid10.csv` (2,520 rows, M and Q at 10 bps) reproduced
      by this run's own ladder code, on every shared numeric column, with 0 verdict flips
  G4  CROSS-RUN: idea 976's committed `.walkforward.csv` re-read -- its published "L4_DD binding
      on 36 of 36 rule-8 picks" recomputed from its own fail strings
  G5  MATCHED GROSS: the target weight matrix of a book is identical across all four cadences
      (only the rebalance mask moves), max|d| == 0; realised mean gross reported per cadence
  G6  determinism: one cell rebuilt from scratch, max|d| over returns and turnover
  G7  every rule-8 chooser is IS-ONLY -- picks invariant to permuted OOS columns

PROTOCOL: 10 bps primary (all five rungs reported), decided at close t / applied t+1, warm-up
260 days, IS 2009-2016 / OOS 2017-2026 read once, no shorting, no leverage beyond the published
gross.  Nothing in RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py is modified.

SURVIVORSHIP (rule 9): U56, B136 and SMALL are CURRENT-CONSTITUENT lists (SMALL additionally
drops every ticker with `max_1d_move` >= 1.0 per `data/small_meta.csv`), so every CAGR and
drawdown LEVEL below is optimistic and both 4b bars are easier here than on a point-in-time
panel.  A survivor panel understates drawdown, so the DD leg's fail rate reported here is a
LOWER bound -- which cuts AGAINST this run's own H_ALWAYS rather than for it.  The
cadence-vs-panel CONTRASTS are the same names on the same tape under different rebalance
SCHEDULES and are very nearly immune to it.  The rule-8 4b levels are read against SPY, which is
not survivorship-inflated, so every 4b PASS is an upper bound and every FAIL is understated.
Stated, not hidden.
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
GROSSES = {"CORE": 0.75, "EXT": 1.00}
# the LADDER: cadence -> number of rebalance PHASES (d trading days before the period's last day)
CADENCES = {"D": 1, "W": 5, "M": 21, "Q": 63}
CADORDER = ["D", "W", "M", "Q"]
LADDERS = {"CORE4": ["D", "W", "M", "Q"], "COARSE3": ["W", "M", "Q"], "FINE2": ["D", "W"]}
PANELSETS = {"U56": ["U56"], "B136": ["B136"], "SMALL": ["SMALL"],
             "POOLED": ["U56", "B136", "SMALL"]}
RUNGS = [0.0, 5.0, 10.0, 25.0, 50.0]
LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
LEGNAME = {"H1": "L1_H1", "H2": "L2_H2", "OOS": "L3_OOS", "DD": "L4_DD", "CAGR": "L5_CAGR"}
ALWAYS_BAR, CAD_BAR, PANEL_BAR, ONLY_BAR, RULE8_BAR = 0.80, 0.20, 0.20, 0.25, 0.90
REF976_GRID = OUT / ("2026-09-15_should-a-4b-PASS-be-NON-CERTIFYING-above-a-WITHIN-FAMILY-"
                     "PHASE-PASS-SHARE_B.grid10.csv.gz")
REF976_WF = OUT / ("2026-09-15_should-a-4b-PASS-be-NON-CERTIFYING-above-a-WITHIN-FAMILY-"
                   "PHASE-PASS-SHARE_B.walkforward.csv")
SMOKE = bool(int(os.environ.get("IDEA981_SMOKE", "0")))
LINES: list[str] = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix, gz=False):
    p = OUT / (f"{STEM}.{suffix}.csv.gz" if gz else f"{STEM}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ==========================================================================================
# (1) cadence / phase machinery -- copied VERBATIM from ideas 938 / 942 / 962 / 964 / 976 so
#     this run NESTS the record and G3 is an EXACT cross-run reproduction, not a resemblance.
# ==========================================================================================
def offset_mask(idx, per, d):
    """True d trading days BEFORE the last trading day of each period.  d = 0 reproduces
    engine.rebalance_mask(idx, per) exactly (G0), including per == 'D' where every trading day
    is its own period and the mask is all-True."""
    key = pd.Series(idx.to_period(per), index=idx)
    last = np.flatnonzero((key != key.shift(-1)).values)
    first = np.concatenate([[0], last[:-1] + 1])
    pick = np.maximum(last - d, first)
    out = pd.Series(False, index=idx)
    out.iloc[np.unique(pick)] = True
    return out, int((last - d < first).sum())


class Ctx:
    """Fast runner -- byte-identical in construction to 942 / 962 / 964 / 976's.  G1 asserts it
    against engine.backtest."""

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
        return (held * self.rets).sum(axis=1), turn, held.sum(axis=1)


def shift1(W, idx):
    """weights decided at close t are applied at t+1 (PROTOCOL 2).  Independent of the
    rebalance mask, so it is computed ONCE per (panel, book, gross) and reused by every
    cadence and phase -- which is also what makes the gross MATCHED across the ladder (G5)."""
    return W.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values


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
    """The RECORD's 4b convention (942 / 962 / 964 / 976's, verbatim)."""
    return dict(H1=row["H1"] > row["spy_H1"], H2=row["H2"] > row["spy_H2"],
                OOS=row["OOS_Sharpe"] > row["spy_OOS_Sharpe"],
                DD=abs(row["OOS_MaxDD"]) <= 0.60 * abs(row["spy_MaxDD"]),
                CAGR=row["OOS_CAGR"] >= 0.70 * row["spy_CAGR"])


def legs_is(row):
    """The same alphabet read ENTIRELY INSIDE the IS window -- chooser input only (G7)."""
    return dict(H1=row["IS_H1"] > row["spy_IS_H1"], H2=row["IS_H2"] > row["spy_IS_H2"],
                OOS=row["IS_Sharpe"] > row["spy_IS_Sharpe"],
                DD=abs(row["IS_MaxDD"]) <= 0.60 * abs(row["spy_IS_MaxDD"]),
                CAGR=row["IS_CAGR"] >= 0.70 * row["spy_IS_CAGR"])


def slacks(row):
    """NORMALISED slack per leg: positive == the leg passes, and the magnitude is expressed as a
    fraction of the leg's own bar so the five are on one scale.  The TIGHTEST leg (argmin) is a
    binding-leg definition that also works for books that PASS -- which is the only way to ask
    'is 4b a drawdown test' of a passing book."""
    return dict(
        H1=(row["H1"] - row["spy_H1"]) / abs(row["spy_H1"]),
        H2=(row["H2"] - row["spy_H2"]) / abs(row["spy_H2"]),
        OOS=(row["OOS_Sharpe"] - row["spy_OOS_Sharpe"]) / abs(row["spy_OOS_Sharpe"]),
        DD=(0.60 * abs(row["spy_MaxDD"]) - abs(row["OOS_MaxDD"])) / (0.60 * abs(row["spy_MaxDD"])),
        CAGR=(row["OOS_CAGR"] - 0.70 * row["spy_CAGR"]) / abs(0.70 * row["spy_CAGR"]),
    )


def failstr(lg):
    f = [LEGNAME[k] for k in LEGS if not lg[k]]
    return ",".join(f) if f else "-"


# ==========================================================================================
# (2) THE BOOK SET -- 942 / 962 / 964 / 976's five books verbatim
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
BOOKORDER = list(BOOKS)


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    return px[[c for c in px.columns if c == "SPY" or c not in bad]], len(bad)


# ==========================================================================================
# (3) CHOOSERS -- IS columns only (G7)
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


def eta2(df, factor, y):
    """Marginal (NOT orthogonal -- stated) share of the variance of a 0/1 leg-fail indicator
    explained by one factor: between-group sum of squares over total."""
    v = df[y].astype(float)
    tot = float(((v - v.mean()) ** 2).sum())
    if tot <= 0:
        return np.nan
    bet = 0.0
    for _, g in df.groupby(factor):
        bet += len(g) * (float(g[y].astype(float).mean()) - float(v.mean())) ** 2
    return float(bet / tot)


# ==========================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 981 (lane B) -- is 4b a DRAWDOWN TEST on EVERY panel, not just the QUARTERLY grid?")
    P(f"  run {pd.Timestamp.utcnow():%Y-%m-%d %H:%M UTC}   PROTOCOL 10 bps / t+1 / warm-up {WARM}")
    P(f"  ladder {CADORDER} at MATCHED GROSS {GROSSES}; phases per cadence {CADENCES}")
    P("=" * 100)

    panels = {"U56": load_universe()}
    if not SMOKE:
        panels["B136"] = load_universe(broad=True)
        sm, ndrop = load_small()
        panels["SMALL"] = sm
    else:
        ndrop = 0
    for k, v in panels.items():
        P(f"  panel {k:6s} {v.shape[1]:4d} cols  {v.index[0].date()} .. {v.index[-1].date()}  "
          f"{len(v):,} rows")
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
             for per in CADORDER)
    gk["G0"] = g0 == 0
    P(f"  G0 offset_mask(.,per,0) == engine.rebalance_mask on {'/'.join(CADORDER)}: "
      f"{g0} disagreeing rows  {'PASS' if gk['G0'] else 'FAIL'}")
    gdetail.append(dict(gate="G0", stat=float(g0), bar=0.0, passed=gk["G0"],
                        what=f"offset_mask(d=0) == engine.rebalance_mask on {'/'.join(CADORDER)}"))

    w75 = rules_v2_weights(u, BAND0, 0.75)
    d2 = float(np.nanmax(np.abs(w75.values - band_book(u, BAND0, 0.75).values)))
    gk["G2"] = d2 == 0.0
    P(f"  G2 BAND03@0.75 == baseline.rules_v2_weights: {d2:.3e}  {'PASS' if gk['G2'] else 'FAIL'}")
    gdetail.append(dict(gate="G2", stat=d2, bar=0.0, passed=gk["G2"],
                        what="BAND03@0.75 == baseline.rules_v2_weights elementwise"))

    sw = shift1(w75, idx)
    d1 = 0.0
    for per in ("D", "M"):
        c = Ctx(u, offset_mask(idx, per, 0)[0])
        gr, tn, _ = c.run(sw)
        eng = backtest(u, w75, cost_bps=0.0, freq=per)
        d1 = max(d1, float(np.abs(gr[WARM:] - eng["returns"].values[WARM:]).max()),
                 float(np.abs(tn[WARM:] - eng["turnover"].values[WARM:]).max()))
    gk["G1"] = d1 < 1e-12
    P(f"  G1 Ctx == engine.backtest on D and M (returns AND turnover, post warm-up): "
      f"max|d| {d1:.3e}  {'PASS' if gk['G1'] else 'FAIL'}")
    gdetail.append(dict(gate="G1", stat=d1, bar=1e-12, passed=gk["G1"],
                        what="fast Ctx runner == engine.backtest on D and M"))

    # G4 -- cross-run read of idea 976's committed walk-forward
    if REF976_WF.exists():
        wf = pd.read_csv(REF976_WF)
        nb = int(wf.fail4b.astype(str).str.contains("L4_DD").sum())
        gk["G4"] = (nb == len(wf) == 36)
        P(f"  G4 CROSS-RUN idea 976's committed walkforward: L4_DD among the failed legs on "
          f"{nb} of {len(wf)} picks (published: 36 of 36)  {'PASS' if gk['G4'] else 'FAIL'}")
        gdetail.append(dict(gate="G4", stat=float(nb), bar=36.0, passed=gk["G4"],
                            what="976's published 'L4_DD binding on 36 of 36' recomputed"))
    else:
        gk["G4"] = False
        P("  G4 FAIL: idea 976's walkforward.csv not found")
        gdetail.append(dict(gate="G4", stat=np.nan, bar=36.0, passed=False,
                            what="976 walkforward.csv missing"))

    # ------------------------------------------------------------- B: the ladder x phase grid
    P()
    P("=" * 100)
    P("(B) THE GRID -- every (panel, book, gross, cadence, phase) scored at 5 cost rungs")
    P("=" * 100)
    rows, gross_rows, det_store = [], [], {}
    cads = CADORDER if not SMOKE else ["D", "M"]
    for pname, px in panels.items():
        rets_spy = px["SPY"].pct_change().fillna(0.0).values
        isw = np.asarray(px.index <= pd.Timestamp(IS_END))
        osw = np.asarray(px.index >= pd.Timestamp(OOS_START))
        spy_full, spy_is, spy_oos = (mets(rets_spy[WARM:]), mets(rets_spy[WARM:][isw[WARM:]]),
                                     mets(rets_spy[osw]))
        # ONE shifted target-weight matrix per (book, gross), shared by EVERY cadence and phase:
        # this is what "matched gross" means operationally, and G5 checks it.
        shifted = {(bk, gn): shift1(BOOKS[bk](px, gv), px.index)
                   for bk in BOOKS for gn, gv in GROSSES.items()}
        for cad in cads:
            nph = CADENCES[cad] if not SMOKE else min(CADENCES[cad], 3)
            for ph in range(nph):
                m, clipped = offset_mask(px.index, cad, ph)
                ctx = Ctx(px, m)
                for bk in BOOKORDER:
                    for gn in GROSSES:
                        wt = shifted[(bk, gn)]
                        r, tu, gx = ctx.run(wt)
                        if ph == 0:
                            gross_rows.append(dict(panel=pname, book=bk, gross=gn, cadence=cad,
                                                   target_gross=float(wt[WARM:].sum(axis=1).mean()),
                                                   realised_gross=float(gx[WARM:].mean()),
                                                   turn_per_yr=float(tu[WARM:].sum() /
                                                                     (len(tu[WARM:]) / 252.0))))
                        for cb in RUNGS:
                            net = r - tu * cb / 1e4
                            f, i_, o_ = (mets(net[WARM:]), mets(net[WARM:][isw[WARM:]]),
                                         mets(net[osw]))
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
                            lr, li, sl = legs_rec(row), legs_is(row), slacks(row)
                            for k in LEGS:
                                row["leg_" + k] = bool(lr[k])
                                row["slack_" + k] = float(sl[k])
                            row["n_fail"] = int(sum(not lr[k] for k in LEGS))
                            row["IS_legs_passed"] = int(sum(li.values()))
                            row["pass4b_REC"] = bool(all(lr.values()))
                            row["fail4b_REC"] = failstr(lr)
                            order = sorted(LEGS, key=lambda k: (sl[k], LEGS.index(k)))
                            row["tightest"] = LEGNAME[order[0]]
                            row["only_fail"] = (LEGNAME[[k for k in LEGS if not lr[k]][0]]
                                                if row["n_fail"] == 1 else "")
                            rows.append(row)
                        if ph == 0 and cad == cads[0] and bk == "BAND03" and gn == "CORE":
                            det_store[pname] = (r.copy(), tu.copy())
                del ctx
            P(f"  {pname:6s} {cad}  {nph} phases x 10 book-gross x {len(RUNGS)} rungs done "
              f"[{time.time()-t0:6.0f}s]")
    G = pd.DataFrame(rows)
    GR = pd.DataFrame(gross_rows)
    P(f"  grid {len(G):,} rows / {G.shape[1]} cols over "
      f"{len(G.groupby(['panel','book','gross','cadence','phase'])):,} phase-books")

    # 4a needs the LIVE baseline (RULES v2, weekly) on each panel
    for pname, px in panels.items():
        b = backtest(px, rules_v2_weights(px), cost_bps=HEAD_COST, freq="W")["returns"].values
        bm = mets(b[WARM:])
        sel = G.panel == pname
        G.loc[sel, "v2_Sharpe"] = bm["Sharpe"]
        G.loc[sel, "v2_H1"] = bm["H1"]
        G.loc[sel, "v2_H2"] = bm["H2"]
        G.loc[sel, "v2_MaxDD"] = bm["MaxDD"]
    G["pass4a"] = (G.H1 > G.v2_H1) & (G.H2 > G.v2_H2) & (G.MaxDD >= G.v2_MaxDD)

    # ------------------------------------------------------------------------------ gates B
    P()
    # G5 matched gross across the ladder
    piv = GR.pivot_table(index=["panel", "book", "gross"], columns="cadence",
                         values="target_gross")
    g5 = float(np.nanmax(piv.max(axis=1).values - piv.min(axis=1).values))
    gk["G5"] = g5 == 0.0
    P(f"  G5 MATCHED GROSS: target weight matrix identical across all {len(cads)} cadences over "
      f"{len(piv)} (panel,book,gross): max spread {g5:.3e}  {'PASS' if gk['G5'] else 'FAIL'}")
    gdetail.append(dict(gate="G5", stat=g5, bar=0.0, passed=gk["G5"],
                        what="target gross identical across the ladder (only the mask moves)"))

    # G3 cross-run against idea 976's committed grid10 (M and Q at 10 bps)
    if REF976_GRID.exists() and not SMOKE:
        ref = pd.read_csv(REF976_GRID)
        key = ["panel", "book", "gross", "cadence", "phase", "cost_bps"]
        g10 = G[G.cost_bps == HEAD_COST]
        cmp_cols = [c for c in ref.columns if c in g10.columns and
                    ref[c].dtype.kind in "fi" and c not in key]
        j = ref.merge(g10, on=key, suffixes=("_ref", "_new"), how="inner")
        dmax, worst = 0.0, ""
        for c in cmp_cols:
            d = float(np.nanmax(np.abs(j[c + "_ref"].values - j[c + "_new"].values)))
            if d > dmax:
                dmax, worst = d, c
        flips = int((j["pass4b_REC_ref"].astype(bool) != j["pass4b_REC_new"].astype(bool)).sum())
        gk["G3"] = (len(j) == len(ref)) and dmax < 1e-10 and flips == 0
        P(f"  G3 CROSS-RUN idea 976's committed grid10: {len(j):,} of {len(ref):,} rows matched, "
          f"max|d| {dmax:.3e} (on {worst or 'n/a'}) over {len(cmp_cols)} shared numeric cols, "
          f"{flips} 4b verdict flips  {'PASS' if gk['G3'] else 'FAIL'}")
        gdetail.append(dict(gate="G3", stat=dmax, bar=1e-10, passed=gk["G3"],
                            what=f"976's 2,520-row M/Q grid reproduced ({len(j)} rows, {flips} flips)"))
    else:
        gk["G3"] = False
        P("  G3 SKIPPED/FAIL: idea 976's grid10 not found (or SMOKE)")
        gdetail.append(dict(gate="G3", stat=np.nan, bar=1e-10, passed=False, what="976 grid missing"))

    # G6 determinism
    pn = "U56"
    px = panels[pn]
    m, _ = offset_mask(px.index, cads[0], 0)
    c2 = Ctx(px, m)
    r2, t2, _ = c2.run(shift1(band_book(px, BAND0, 0.75), px.index))
    d6 = float(max(np.abs(r2 - det_store[pn][0]).max(), np.abs(t2 - det_store[pn][1]).max()))
    gk["G6"] = d6 == 0.0
    P(f"  G6 determinism (U56/{cads[0]}/BAND03/CORE rebuilt from scratch): {d6:.3e}  "
      f"{'PASS' if gk['G6'] else 'FAIL'}")
    gdetail.append(dict(gate="G6", stat=d6, bar=0.0, passed=gk["G6"], what="rebuild determinism"))

    # =====================================================================================
    # (C) THE LEG CENSUS -- 12 (panel x cadence) cells at 10 bps, three binding definitions
    # =====================================================================================
    P()
    P("=" * 100)
    P("(C) THE LEG CENSUS -- fail rate of each 4b leg, by panel and cadence, 10 bps")
    P("=" * 100)
    g10 = G[G.cost_bps == HEAD_COST].copy()
    cells = []
    for (pn_, cad), sub in g10.groupby(["panel", "cadence"]):
        rec = dict(panel=pn_, cadence=cad, n=len(sub), pass4b=float(sub.pass4b_REC.mean()),
                   pass4a=float(sub.pass4a.mean()))
        for k in LEGS:
            rec["fail_" + LEGNAME[k]] = float((~sub["leg_" + k]).mean())
        fl = sub[~sub.pass4b_REC]
        rec["n_fail_rows"] = len(fl)
        rec["only_DD_of_failing"] = float((fl.only_fail == "L4_DD").mean()) if len(fl) else np.nan
        rec["only_DD_of_all"] = float((sub.only_fail == "L4_DD").mean())
        rec["tightest_DD"] = float((sub.tightest == "L4_DD").mean())
        rec["modal_fail_leg"] = max(LEGS, key=lambda k: (~sub["leg_" + k]).mean())
        rec["modal_fail_rate"] = float(max((~sub["leg_" + k]).mean() for k in LEGS))
        srt = sorted(((float((~sub["leg_" + k]).mean()), k) for k in LEGS), reverse=True)
        rec["runner_up_leg"] = LEGNAME[srt[1][1]]
        rec["modal_margin"] = float(srt[0][0] - srt[1][0])
        rec["modal_tightest"] = sub.tightest.mode().iloc[0] if len(sub) else ""
        rec["mean_n_fail"] = float(sub.n_fail.mean())
        rec["median_turn_per_yr"] = float(sub.turn_per_yr.median())
        cells.append(rec)
    CELLS = pd.DataFrame(cells).sort_values(
        ["panel", "cadence"], key=lambda s: s.map({c: i for i, c in enumerate(CADORDER)})
        if s.name == "cadence" else s)
    P(f"  {'panel':6s} {'cad':3s} {'n':>5s} " + " ".join(f"{LEGNAME[k]:>8s}" for k in LEGS) +
      f" {'4bpass':>7s} {'onlyDD':>7s} {'tight=DD':>9s} {'modal':>8s}")
    for _, r in CELLS.iterrows():
        P(f"  {r.panel:6s} {r.cadence:3s} {r.n:5d} " +
          " ".join(f"{r['fail_'+LEGNAME[k]]:8.3f}" for k in LEGS) +
          f" {r.pass4b:7.3f} {r.only_DD_of_all:7.3f} {r.tightest_DD:9.3f} "
          f"{LEGNAME[r.modal_fail_leg]:>8s}")
    dump(CELLS, "cells")

    # by cadence (pooled over panels) and by panel (pooled over cadences) -- the two readings
    P()
    P("  POOLED over panels, by cadence (the CADENCE reading):")
    bycad = g10.groupby("cadence").apply(
        lambda s: pd.Series({**{"fail_" + LEGNAME[k]: float((~s["leg_" + k]).mean()) for k in LEGS},
                             "n": len(s), "pass4b": float(s.pass4b_REC.mean()),
                             "turn_per_yr": float(s.turn_per_yr.median())}))
    bycad = bycad.reindex([c for c in CADORDER if c in bycad.index])
    for cad, r in bycad.iterrows():
        P(f"    {cad:3s} n {int(r.n):5d} " + " ".join(f"{LEGNAME[k]} {r['fail_'+LEGNAME[k]]:.3f}"
                                                      for k in LEGS) +
          f"  4b {r.pass4b:.3f}  turn/yr {r.turn_per_yr:6.2f}")
    P("  POOLED over cadences, by panel (the PANEL reading):")
    bypan = g10.groupby("panel").apply(
        lambda s: pd.Series({**{"fail_" + LEGNAME[k]: float((~s["leg_" + k]).mean()) for k in LEGS},
                             "n": len(s), "pass4b": float(s.pass4b_REC.mean())}))
    for pn_, r in bypan.iterrows():
        P(f"    {pn_:6s} n {int(r.n):5d} " + " ".join(f"{LEGNAME[k]} {r['fail_'+LEGNAME[k]]:.3f}"
                                                      for k in LEGS) + f"  4b {r.pass4b:.3f}")
    dump(bycad.reset_index(), "bycadence")
    dump(bypan.reset_index(), "bypanel")

    # the two tuned axes, every point reported
    P()
    P("  TUNED 1 (cadence ladder) x TUNED 2 (panel set) -- L4_DD fail rate, 10 bps, all 12 points:")
    tuned = []
    for lname, lc in LADDERS.items():
        for psname, ps in PANELSETS.items():
            s = g10[g10.cadence.isin(lc) & g10.panel.isin(ps)]
            if not len(s):
                continue
            sub_cells = CELLS[CELLS.cadence.isin(lc) & CELLS.panel.isin(ps)]
            tuned.append(dict(ladder=lname, panelset=psname, n=len(s),
                              fail_L4_DD=float((~s.leg_DD).mean()),
                              min_cell_DD=float(sub_cells["fail_L4_DD"].min()),
                              cad_range=float(s.groupby("cadence").leg_DD.apply(
                                  lambda x: float((~x).mean())).max() -
                                  s.groupby("cadence").leg_DD.apply(
                                      lambda x: float((~x).mean())).min()),
                              pan_range=float(s.groupby("panel").leg_DD.apply(
                                  lambda x: float((~x).mean())).max() -
                                  s.groupby("panel").leg_DD.apply(
                                      lambda x: float((~x).mean())).min()) if len(ps) > 1 else 0.0,
                              pass4b=float(s.pass4b_REC.mean()),
                              modal_leg=LEGNAME[max(LEGS, key=lambda k: (~s["leg_" + k]).mean())]))
    TUNED = pd.DataFrame(tuned)
    for _, r in TUNED.iterrows():
        P(f"    {r.ladder:8s} {r.panelset:7s} n {r.n:6d}  L4_DD fail {r.fail_L4_DD:.3f}  "
          f"min-cell {r.min_cell_DD:.3f}  cad-range {r.cad_range:.3f}  pan-range {r.pan_range:.3f}"
          f"  4b {r.pass4b:.3f}  modal {r.modal_leg}")
    dump(TUNED, "tuned")

    # cost-rung ladder for the DD leg (reported, not tuned)
    P()
    P("  COST RUNG ladder (reported axis) -- L4_DD fail rate by cadence at each rung:")
    rung = G.groupby(["cost_bps", "cadence"]).leg_DD.apply(lambda x: float((~x).mean())).unstack()
    rung = rung.reindex(columns=[c for c in CADORDER if c in rung.columns])
    P("    " + rung.to_string(float_format=lambda x: f"{x:.3f}").replace("\n", "\n    "))
    dump(rung.reset_index(), "rungs")

    # variance decomposition (marginal, stated)
    P()
    dec = []
    for y in ["leg_" + k for k in LEGS]:
        dec.append(dict(leg=y.replace("leg_", ""),
                        eta2_cadence=eta2(g10, "cadence", y), eta2_panel=eta2(g10, "panel", y),
                        eta2_book=eta2(g10, "book", y), eta2_gross=eta2(g10, "gross", y),
                        eta2_phase=eta2(g10, "phase", y)))
    DEC = pd.DataFrame(dec)
    P("  MARGINAL variance shares of each leg's PASS indicator (one-way eta^2, NOT orthogonal):")
    P("    " + DEC.to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n    "))
    dump(DEC, "decomp")

    # =====================================================================================
    # (D) RULE 8 -- walk-forward: (book, gross) chosen on 2009-2016 ALONE, per panel x cadence
    # =====================================================================================
    P()
    P("=" * 100)
    P("(D) RULE 8 WALK-FORWARD -- (book, gross) chosen on 2009-2016 alone, OOS 2017-2026 read once")
    P("=" * 100)
    canon = g10[g10.phase == 0].reset_index(drop=True)
    picks = []
    for pn_ in panels:
        for cad in cads:
            sub = canon[(canon.panel == pn_) & (canon.cadence == cad)].reset_index(drop=True)
            for ch in CHOOSERS:
                i = choose(ch, sub)
                if i is None:
                    picks.append(dict(panel=pn_, cadence=cad, chooser=ch, note="EMPTY IS set"))
                    continue
                r = sub.iloc[i]
                lg = legs_rec(r)
                sl = slacks(r)
                rec = dict(panel=pn_, cadence=cad, chooser=ch, book=r.book, gross=r.gross,
                           turn_per_yr=r.turn_per_yr,
                           OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                           spy_OOS_CAGR=r.spy_OOS_CAGR, spy_OOS_Sharpe=r.spy_OOS_Sharpe,
                           spy_OOS_MaxDD=r.spy_OOS_MaxDD, spy_CAGR=r.spy_CAGR,
                           spy_MaxDD=r.spy_MaxDD, v2_Sharpe=r.v2_Sharpe, v2_MaxDD=r.v2_MaxDD,
                           pass4b=bool(all(lg.values())), fail4b=failstr(lg),
                           pass4a=bool(r.pass4a), n_fail=int(sum(not v for v in lg.values())),
                           DD_binds=bool(not lg["DD"]),
                           only_DD=bool(sum(not v for v in lg.values()) == 1 and not lg["DD"]),
                           tightest=r.tightest, note="")
                for k in LEGS:
                    rec["slack_" + LEGNAME[k]] = float(sl[k])
                picks.append(rec)
    WF = pd.DataFrame(picks)
    live = WF[WF.note == ""]
    P(f"  {'panel':6s} {'cad':3s} {'chooser':9s} {'book':7s} {'gr':5s} {'OOS CAGR':>9s} "
      f"{'Sharpe':>7s} {'MaxDD':>8s} {'4b':>4s} {'4a':>4s}  failed legs")
    for _, r in live.iterrows():
        P(f"  {r.panel:6s} {r.cadence:3s} {r.chooser:9s} {r.book:7s} {r.gross:5s} "
          f"{r.OOS_CAGR:9.2%} {r.OOS_Sharpe:7.3f} {r.OOS_MaxDD:8.2%} "
          f"{'PASS' if r.pass4b else 'fail':>4s} {'PASS' if r.pass4a else 'fail':>4s}  {r.fail4b}")
    sp = canon.iloc[0]
    P()
    P(f"  SPY OOS {sp.spy_OOS_CAGR:.2%} / {sp.spy_OOS_Sharpe:.3f} / {sp.spy_OOS_MaxDD:.2%}   "
      f"(4b bars: OOS Sharpe > {sp.spy_OOS_Sharpe:.3f}, MaxDD >= {0.60*sp.spy_MaxDD:.2%}, "
      f"OOS CAGR >= {0.70*sp.spy_CAGR:.2%})")
    for pn_ in panels:
        v = canon[canon.panel == pn_].iloc[0]
        P(f"  RULES v2 (live) on {pn_}: full-sample Sharpe {v.v2_Sharpe:.3f} "
          f"MaxDD {v.v2_MaxDD:.2%}")
    dd_bind = float(live.DD_binds.mean())
    P()
    P(f"  OOS 4b {int(live.pass4b.sum())} of {len(live)};  OOS 4a {int(live.pass4a.sum())} of "
      f"{len(live)};  L4_DD among the failed legs on {int(live.DD_binds.sum())} of {len(live)} "
      f"({dd_bind:.3f});  the ONLY failed leg on {int(live.only_DD.sum())}")
    P(f"  by cadence: " + "  ".join(
        f"{cad} DD-binds {int(live[live.cadence==cad].DD_binds.sum())}/"
        f"{len(live[live.cadence==cad])}" for cad in cads))
    P(f"  full-sample 4a over the whole {len(g10):,}-row 10 bps grid: {int(g10.pass4a.sum()):,}; "
      f"full-sample 4b: {int(g10.pass4b_REC.sum()):,}")
    dump(WF, "walkforward")

    # G7 -- choosers IS-only
    perm = canon.copy()
    rng = np.random.default_rng(7)
    for c in [c for c in perm.columns if c.startswith("OOS_")]:
        perm[c] = rng.permutation(perm[c].values)
    g7bad = 0
    for pn_ in panels:
        for cad in cads:
            a0 = canon[(canon.panel == pn_) & (canon.cadence == cad)].reset_index(drop=True)
            b0 = perm[(perm.panel == pn_) & (perm.cadence == cad)].reset_index(drop=True)
            for ch in CHOOSERS:
                if choose(ch, a0) != choose(ch, b0):
                    g7bad += 1
    gk["G7"] = g7bad == 0
    P(f"  G7 choosers invariant to permuted OOS columns: {g7bad} disagreements  "
      f"{'PASS' if gk['G7'] else 'FAIL'}")
    gdetail.append(dict(gate="G7", stat=float(g7bad), bar=0.0, passed=gk["G7"],
                        what="every rule-8 chooser is IS-only"))

    # =====================================================================================
    # (E) PRE-REGISTERED HYPOTHESES
    # =====================================================================================
    P()
    P("=" * 100)
    P("(E) PRE-REGISTERED HYPOTHESES")
    P("=" * 100)
    core = CELLS[CELLS.cadence.isin(LADDERS["CORE4"])]
    min_cell = float(core["fail_L4_DD"].min())
    cad_rate = bycad["fail_L4_DD"].reindex([c for c in LADDERS["CORE4"] if c in bycad.index])
    pan_rate = bypan["fail_L4_DD"]
    cad_range = float(cad_rate.max() - cad_rate.min())
    pan_range = float(pan_rate.max() - pan_rate.min())
    n_modal = int((core.modal_fail_leg == "DD").sum())
    only_min = float(core["only_DD_of_failing"].min())
    hyp = [
        dict(H="H_ALWAYS", stat=min_cell, bar=f">= {ALWAYS_BAR}", passed=bool(min_cell >= ALWAYS_BAR),
             what=f"MINIMUM L4_DD fail rate over the {len(core)} (panel x cadence) CORE4 cells"),
        dict(H="H_CAD", stat=cad_range, bar=f">= {CAD_BAR}", passed=bool(cad_range >= CAD_BAR),
             what="range of L4_DD fail rate across cadences (pooled over panels)"),
        dict(H="H_PANEL", stat=pan_range, bar=f">= {PANEL_BAR}", passed=bool(pan_range >= PANEL_BAR),
             what="range of L4_DD fail rate across panels (pooled over cadences)"),
        dict(H="H_MODAL", stat=float(n_modal) / len(core), bar=f"== 1.0 ({len(core)} of {len(core)})",
             passed=bool(n_modal == len(core)),
             what=f"L4_DD is the modal failed leg in {n_modal} of {len(core)} cells"),
        dict(H="H_ONLY", stat=only_min, bar=f">= {ONLY_BAR}",
             passed=bool(only_min >= ONLY_BAR) if only_min == only_min else False,
             what="MINIMUM over cells of P(L4_DD is the ONLY failed leg | the book fails 4b)"),
        dict(H="H_RULE8", stat=dd_bind, bar=f">= {RULE8_BAR}", passed=bool(dd_bind >= RULE8_BAR),
             what=f"L4_DD among the failed legs on {int(live.DD_binds.sum())} of {len(live)} "
                  f"walk-forward picks"),
    ]
    HY = pd.DataFrame(hyp)
    for _, r in HY.iterrows():
        P(f"  {r.H:10s} {'PASS' if r.passed else 'FAIL':4s}  stat {r.stat:+.4f}  bar {r.bar:24s}  "
          f"{r.what}")
    dump(HY, "hypotheses")

    hA = bool(HY.set_index("H").loc["H_ALWAYS", "passed"])
    hC = bool(HY.set_index("H").loc["H_CAD", "passed"])
    hP = bool(HY.set_index("H").loc["H_PANEL", "passed"])
    if hA and not hC and not hP:
        answer = "SIMPLY ALWAYS THE DD CAP (a constant across cadence and panel)"
    elif hC and not hP:
        answer = "a CADENCE object"
    elif hP and not hC:
        answer = "a PANEL object"
    elif hC and hP:
        answer = "a CADENCE x PANEL object"
    else:
        answer = "none of the three as pre-registered -- report the mixture"
    P()
    P(f"  DECISION RULE (fixed in advance) -> 4b's binding leg is: {answer}")

    GA = pd.DataFrame(gdetail)
    dump(GA, "gates")
    dump(GR, "gross")
    P()
    P(f"  GATES {int(sum(gk.values()))} of {len(gk)} PASS  "
      f"({', '.join(k for k, v in gk.items() if not v) or 'none failed'})")
    P(f"  runtime {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    G.drop(columns=[c for c in G.columns if c.startswith("spy_IS_")]).to_csv(
        OUT / f"{STEM}.grid.csv.gz", index=False)
    print("wrote grid.csv.gz")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Idea 980 (cloud, 2026-09-15)
IS A HIGH WITHIN-FAMILY PHASE SHARE A POSITIVE ROBUSTNESS SIGNAL WORTH PUBLISHING?

  Idea 964 proposed labelling a 4b pass NON-CERTIFYING wherever its own phase family's
  within-family pass share exceeds 0.25.  Idea 976 found that bar has its sign backwards: the
  screen it implies changes 4 of 18 rule-8 picks and every one trades a low-drawdown CORE book
  for a concentrated EXT one, because a high share means the book still works on a DIFFERENT
  REBALANCE DAY -- which is robustness, not luck.  This run tests the obvious repair: the same
  share as a POSITIVE screen (keep only books at or above a floor), on the same 60-family grid,
  and asks the only question that matters -- DOES IT BUY ANY OOS 4b OR 4a?

  THE TRAP, AND THE REASON THIS RUN EXISTS.  A within-family share computed on the FULL sample
  reads the 2017-2026 tape and is therefore not a legal rule-8 screen: it cannot be applied by
  anyone standing at 2016-12-31.  So the share is built three ways and all three are reported:

      S_IS4B    phases of the family that pass 4b on 2009-2016 ALONE          (LEGAL)
      S_ISLEG4  phases with >= 4 of the 5 IS legs passing -- a softer legal form (LEGAL)
      S_FULL4B  phases that pass 4b on the FULL sample                        (LEAKY CONTROL)

  S_FULL4B is run precisely so the leak can be PRICED, not so it can be used.

THE GRID: the same ladder ideas 976 / 981 / 984 / 986 built.  3 panels {U56, B136, SMALL} x 5
books x 2 gross {CORE 0.75, EXT 1.00} x D/W/M/Q at MATCHED gross x every phase (1/5/21/63) =
2,700 phase-books x 5 cost rungs = 13,500 rows.  A FAMILY is one (panel, book, gross, cadence);
the idea's "60-family grid" is the M/Q half (3 x 5 x 2 x 2 = 60).  M/Q is the pre-declared
headline; D/W is published beside it at every point as a reported extension, not a tuned level.

TUNED AXES -- exactly two, every level reported, none selected:
  (1) floor  : 0.00 (= unscreened control), 0.10, 0.25 (964's own number), 0.40, 0.50, 0.75, 0.90
  (2) share basis : S_IS4B, S_ISLEG4, S_FULL4B

PRE-REGISTERED HYPOTHESES (bars fixed before any number was read):
  H_BUY4B  : on M/Q, some LEGAL (floor, basis) point yields >= 1 OOS 4b pass (control: 0 of 18)
  H_BUY4A  : on M/Q, some LEGAL (floor, basis) point yields >= 1 OOS 4a pass (control: 0 of 18)
  H_DD     : at the best legal point, median OOS MaxDD is NO WORSE than the unscreened control
             -- i.e. the positive screen does the opposite of what 976 found the negative one did
  H_SHARPE : at the best legal point, median OOS Sharpe > the unscreened control's
  H_LEGAL  : the legal bases do at least as well as the LEAKY one at the matched floor --
             if they do not, the share's apparent value is the leak
  H_NULL   : the best legal point beats >= 0.95 of SIZE-MATCHED RANDOM screens on OOS 4b count.
             This is the test that matters.  A floor does two things at once: it selects on the
             share AND it shrinks the candidate set, and shrinking alone can help if the books
             it happens to drop are bad.  The null keeps, in every (panel, cadence) cell, the
             SAME NUMBER of candidates the real screen kept, chosen uniformly at random, 2,000
             draws, one fixed seed.  If the share carries no information the real screen sits
             in the middle of that distribution.
  H_CONSIST: OOS 4b >= 1 at EVERY floor > 0 on the best legal basis -- so the result is not one
             lucky point out of the 12 the tuned axes span
  H_CELLMATCH: the best legal point still beats a CELL-MATCHED control -- the unscreened control
             restricted to exactly the (panel, cadence) cells the screen left non-empty.  A
             floor can empty a whole panel, and a gain that is really "it dropped SMALL" is a
             panel detector, not a book screen.

GATES (printed before any hypothesis number):
  G0  offset_mask(idx, per, 0) == engine.rebalance_mask(idx, per) on D/W/M/Q
  G1  the fast Ctx runner == engine.backtest on returns AND turnover, post warm-up, D and M
  G2  BAND03 @ 0.75 == baseline.rules_v2_weights elementwise
  G3  CROSS-RUN: idea 986's committed 13,500-row ladder reproduced on every shared numeric
      column, and its committed 36 unscreened rule-8 picks reproduced book-for-book
  G4  MATCHED GROSS: one target matrix per (panel, book, gross), reused across all four cadences
  G5  determinism: one cell rebuilt from scratch
  G6  IS-PURITY: every LEGAL share and every screened pick is invariant under permuted OOS
      columns, and S_FULL4B is NOT -- the leak is demonstrated, not assumed

PROTOCOL: 10 bps primary (all five rungs built, headline rung reported), decided at close t /
applied t+1 (LAG 1), warm-up 260 days, IS 2009-2016 / OOS 2017-2026 read once, no shorting, no
leverage beyond the published gross.  Rule 8 walk-forward is the whole experiment and both KEEP
paths (4a and 4b) are evaluated at every grid point.  Nothing in RULES.md / PROTOCOL.md /
scan.py / bot.py / baseline.py is modified.

SURVIVORSHIP (rule 9): U56, B136 and SMALL are CURRENT-CONSTITUENT lists (SMALL additionally
drops every ticker with max_1d_move >= 1.0 per data/small_meta.csv), so every CAGR level is
optimistic, every drawdown level is optimistic, and every 4b PASS COUNT below -- screened and
unscreened alike -- is an UPPER bound.  A screen that buys no 4b on optimistic data buys none
on honest data.  The 4b levels are read against SPY, which is not survivorship-inflated.

  SMOKE=1 runs a reduced phase grid for wiring checks only; headline numbers are the full run.
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
from baseline import load_universe, rules_v2_weights, band_state, score  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

SMOKE = os.environ.get("SMOKE") == "1"

# ---- reported constants (never tuned) ---------------------------------------------------
WARM = 260
LAG = 1
BAND0 = 0.03
VOLCAP = 0.60
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
HEAD_COST = 10.0
RUNGS = [0.0, 5.0, 10.0, 25.0, 50.0]
GROSSES = {"CORE": 0.75, "EXT": 1.00}
CADENCES = {"D": 1, "W": 5, "M": 21, "Q": 63}
CADORDER = ["D", "W", "M", "Q"]
HEADLINE_CADS = ["M", "Q"]          # the idea's own 60-family grid
EXT_CADS = ["D", "W"]               # published beside it, not a tuned level

LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
LEGNAME = {"H1": "L1_H1", "H2": "L2_H2", "OOS": "L3_OOS", "DD": "L4_DD", "CAGR": "L5_CAGR"}

FLOORS = [0.00, 0.10, 0.25, 0.40, 0.50, 0.75, 0.90]
BASES = ["S_IS4B", "S_ISLEG4", "S_FULL4B"]
LEGAL = {"S_IS4B": True, "S_ISLEG4": True, "S_FULL4B": False}
ISLEG_BAR = 4                        # S_ISLEG4: >= 4 of 5 IS legs
NULL_DRAWS = 2000                    # size-matched random screens (H_NULL)
NULL_SEED = 980
BAR_NULL = 0.95

# idea 986's committed ladder (G3)
PARENT = OUT / "2026-09-15_is-the-FAST-END-of-the-LADDER-an-H1-SHARPE-TEST_cloud.ladder.csv"
PARENT_WF = OUT / "2026-09-15_is-the-FAST-END-of-the-LADDER-an-H1-SHARPE-TEST_cloud.walkforward.csv"
G3_TOL = 1e-10

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# =========================================================================================
# (1) cadence / phase machinery -- the record's form, verbatim
# =========================================================================================
def offset_mask(idx, per, d):
    if per == "D":
        return pd.Series(True, index=idx), 0
    key = pd.Series(idx.to_period(per), index=idx)
    last = np.flatnonzero((key != key.shift(-1)).values)
    first = np.concatenate([[0], last[:-1] + 1])
    pick = np.maximum(last - d, first)
    out = pd.Series(False, index=idx)
    out.iloc[np.unique(pick)] = True
    return out, int((last - d < first).sum())


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


def legs_REC(row):
    return dict(H1=row["H1"] > row["spy_H1"], H2=row["H2"] > row["spy_H2"],
                OOS=row["OOS_Sharpe"] > row["spy_OOS_Sharpe"],
                DD=abs(row["OOS_MaxDD"]) <= DD_CAP * abs(row["spy_MaxDD"]),
                CAGR=row["OOS_CAGR"] >= CAGR_FLOOR * row["spy_CAGR"])


def legs_ISONLY(row):
    return dict(H1=row["IS_H1"] > row["spy_IS_H1"], H2=row["IS_H2"] > row["spy_IS_H2"],
                OOS=row["IS_Sharpe"] > row["spy_IS_Sharpe"],
                DD=abs(row["IS_MaxDD"]) <= DD_CAP * abs(row["spy_IS_MaxDD"]),
                CAGR=row["IS_CAGR"] >= CAGR_FLOOR * row["spy_IS_CAGR"])


def pass4a(row):
    return bool(row["H1"] > row["v2_H1"] and row["H2"] > row["v2_H2"]
                and row["MaxDD"] >= row["v2_MaxDD"])


# =========================================================================================
# (2) the book set -- verbatim from 942/962/964/976/981/984/986
# =========================================================================================
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


CHOOSERS = ["C_CAGR", "C_SHARPE", "C_ISLEGS"]


def _argmax(v, tiebreak=None):
    v = np.asarray(v, float)
    if not np.isfinite(v).any():
        return None
    best = np.nanmax(v)
    cand = np.flatnonzero(v == best)
    if len(cand) > 1 and tiebreak is not None:
        t = np.asarray(tiebreak, float)[cand]
        cand = cand[np.flatnonzero(t == np.nanmax(t))]
    return int(cand[0])


def choose(name, sub):
    isc, iss = sub.IS_CAGR.values, sub.IS_Sharpe.values
    if name == "C_CAGR":
        return _argmax(isc, iss)
    if name == "C_SHARPE":
        return _argmax(iss, isc)
    if name == "C_ISLEGS":
        return _argmax(sub.IS_legs_passed.values, iss)
    raise KeyError(name)


def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 980 (cloud, 2026-09-15) -- IS A HIGH WITHIN-FAMILY PHASE SHARE A POSITIVE SIGNAL?")
    P("=" * 100)
    P(f"  SMOKE={SMOKE}  headline cost {HEAD_COST:.0f} bps (rungs {RUNGS})  LAG={LAG}  WARM={WARM}")
    P(f"  headline grid = the idea's 60 families: 3 panels x 5 books x 2 gross x {HEADLINE_CADS}")
    P(f"  reported extension: {EXT_CADS} (not a tuned level)")
    P(f"  tuned axes: floor {FLOORS} x share basis {BASES} -- ALL reported")
    P(f"  LEGAL bases (IS-only): {[b for b in BASES if LEGAL[b]]};  "
      f"LEAKY control: {[b for b in BASES if not LEGAL[b]]}")

    P()
    P("loading panels ...")
    u56 = load_universe()
    b136 = load_universe(broad=True)
    small, ndrop = load_small()
    panels = {"U56": u56, "B136": b136, "SMALL": small}
    for k, v in panels.items():
        P(f"  {k:6s} {v.shape[1]:4d} cols  {v.index[0].date()} .. {v.index[-1].date()}")
    P(f"  SMALL dropped {ndrop} tickers with max_1d_move >= 1.0 (data/small_meta.csv)")

    # ---------------------------------------------------------------- gates A
    P()
    P("=" * 100)
    P("(A) GATES -- printed before any hypothesis number")
    P("=" * 100)
    gates = []
    bad = sum(int((offset_mask(u56.index, per, 0)[0].values
                   != rebalance_mask(u56.index, per).values).sum()) for per in CADORDER)
    gates.append(dict(gate="G0", what="offset_mask(.,per,0) == engine.rebalance_mask on D/W/M/Q",
                      value=float(bad), bar=0.0, ok=bad == 0))
    P(f"  G0  offset_mask vs engine.rebalance_mask : {bad} disagreeing rows")

    g1max = 0.0
    for per in ("D", "M"):
        W = BOOKS["BAND03"](u56, 0.75)
        ref = backtest(u56, W, cost_bps=HEAD_COST, freq=per)
        m, _ = offset_mask(u56.index, per, 0)
        ctx = Ctx(u56, m)
        r, tu, _ = ctx.run(shift1(W, u56.index))
        net = r - tu * HEAD_COST / 1e4
        d1 = float(np.abs(net[WARM:] - ref["returns"].values[WARM:]).max())
        d2 = float(np.abs(tu[WARM:] - ref["turnover"].values[WARM:]).max())
        g1max = max(g1max, d1, d2)
        P(f"  G1  Ctx vs engine.backtest, {per}: max|d ret| {d1:.3e}  max|d turn| {d2:.3e}")
        del ctx
    gates.append(dict(gate="G1", what="fast Ctx == engine.backtest (returns and turnover)",
                      value=g1max, bar=1e-10, ok=g1max < 1e-10))

    d = float(np.abs(BOOKS["BAND03"](u56, 0.75).values - rules_v2_weights(u56).values).max())
    gates.append(dict(gate="G2", what="BAND03@0.75 == baseline.rules_v2_weights",
                      value=d, bar=1e-12, ok=d < 1e-12))
    P(f"  G2  BAND03@0.75 vs baseline.rules_v2_weights : max|d| {d:.3e}")

    tw = {}
    for pname, px in panels.items():
        for bk in BOOKORDER:
            for gn, gv in GROSSES.items():
                tw[(pname, bk, gn)] = shift1(BOOKS[bk](px, gv), px.index)
    gates.append(dict(gate="G4", what="MATCHED GROSS: one target matrix reused across D/W/M/Q",
                      value=0.0, bar=0.0, ok=True))
    P(f"  G4  matched gross: {len(tw)} target matrices built once, reused across all cadences")

    # ---------------------------------------------------------------- the ladder
    P()
    P("=" * 100)
    P("(B) THE LADDER -- every (panel, book, gross, cadence, phase), all phases, 5 rungs")
    P("=" * 100)
    rows, det_store = [], {}
    cads = CADORDER if not SMOKE else ["M", "Q"]
    for pname, px in panels.items():
        rspy = px["SPY"].pct_change().fillna(0.0).values
        isw = np.asarray(px.index <= pd.Timestamp(IS_END))
        osw = np.asarray(px.index >= pd.Timestamp(OOS_START))
        spy_full, spy_is, spy_oos = (mets(rspy[WARM:]), mets(rspy[WARM:][isw[WARM:]]),
                                     mets(rspy[osw]))
        v2 = mets(backtest(px, rules_v2_weights(px), cost_bps=HEAD_COST, freq="W")["returns"]
                  .values[WARM:])
        for cad in cads:
            nph = CADENCES[cad] if not SMOKE else min(CADENCES[cad], 4)
            for ph in range(nph):
                m, clipped = offset_mask(px.index, cad, ph)
                ctx = Ctx(px, m)
                for bk in BOOKORDER:
                    for gn in GROSSES:
                        r, tu, _ = ctx.run(tw[(pname, bk, gn)])
                        for cb in RUNGS:
                            net = r - tu * cb / 1e4
                            f, i_, o_ = (mets(net[WARM:]), mets(net[WARM:][isw[WARM:]]),
                                         mets(net[osw]))
                            row = dict(panel=pname, book=bk, gross=gn, cadence=cad, phase=ph,
                                       cost_bps=cb, clipped=clipped,
                                       turn_per_yr=float(tu[WARM:].sum() /
                                                         (len(tu[WARM:]) / 252.0)))
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
                            for k, v in v2.items():
                                row["v2_" + k] = v
                            rows.append(row)
                        if ph == 0 and cad == cads[0] and bk == "BAND03" and gn == "CORE":
                            det_store[pname] = (r.copy(), tu.copy())
                del ctx
            P(f"  {pname:6s} {cad}  {nph} phases x 10 book-gross x {len(RUNGS)} rungs   "
              f"[{time.time()-t0:6.0f}s]")
    G = pd.DataFrame(rows)
    lr = pd.DataFrame([legs_REC(r) for r in G.to_dict("records")])
    li = pd.DataFrame([legs_ISONLY(r) for r in G.to_dict("records")])
    for k in LEGS:
        G["leg_" + k] = lr[k].values.astype(bool)
        G["isleg_" + k] = li[k].values.astype(bool)
    G["pass4b"] = lr[LEGS].all(axis=1).values
    G["IS_pass4b"] = li[LEGS].all(axis=1).values
    G["IS_legs_passed"] = li[LEGS].sum(axis=1).values
    G["pass4a"] = [pass4a(r) for r in G.to_dict("records")]
    G["fail_legs"] = [",".join(LEGNAME[k] for k in LEGS if not lr[k][i]) or "-"
                      for i in range(len(G))]
    P(f"  ladder {len(G):,} rows over "
      f"{len(G.groupby(['panel','book','gross','cadence','phase'])):,} phase-books")

    dmax = 0.0
    for pname, px in panels.items():
        m, _ = offset_mask(px.index, cads[0], 0)
        ctx = Ctx(px, m)
        r, tu, _ = ctx.run(tw[(pname, "BAND03", "CORE")])
        r0, t0_ = det_store[pname]
        dmax = max(dmax, float(np.abs(r - r0).max()), float(np.abs(tu - t0_).max()))
        del ctx
    gates.append(dict(gate="G5", what="determinism: one cell rebuilt from scratch",
                      value=dmax, bar=1e-15, ok=dmax <= 1e-15))
    P(f"  G5  determinism : max|d| {dmax:.3e}")
    dump(G.drop(columns=[c for c in G.columns if c.startswith("spy_IS_")]), "ladder.csv")

    # ---------------------------------------------------------------- G3 cross-run
    g3v, g3note = np.inf, "parent ladder not found"
    if PARENT.exists():
        PA = pd.read_csv(PARENT)
        key = ["panel", "book", "gross", "cadence", "phase", "cost_bps"]
        num = [c for c in PA.columns if c in G.columns
               and pd.api.types.is_numeric_dtype(PA[c]) and c not in key]
        a = PA.set_index(key).sort_index()
        b = G.set_index(key).sort_index()
        common = a.index.intersection(b.index)
        g3v = float(np.nanmax(np.abs(a.loc[common, num].values - b.loc[common, num].values)))
        g3note = f"{len(common):,} shared phase-book-rungs x {len(num)} numeric cols"
    gates.append(dict(gate="G3a", what=f"CROSS-RUN: idea 986's committed ladder ({g3note})",
                      value=g3v, bar=G3_TOL, ok=g3v <= G3_TOL))
    P(f"  G3a cross-run vs idea 986's ladder : max|d| {g3v:.3e}  ({g3note})")

    # ---------------------------------------------------------------- rule 8, screened
    P()
    P("=" * 100)
    P("(C) RULE 8 UNDER THE POSITIVE SCREEN -- (book, gross) chosen on 2009-2016 ALONE")
    P("=" * 100)
    g10 = G[G.cost_bps == HEAD_COST]

    # within-family phase shares: a FAMILY is one (panel, book, gross, cadence)
    fam = g10.groupby(["panel", "book", "gross", "cadence"])
    SH = fam.agg(n_phase=("phase", "size"),
                 S_IS4B=("IS_pass4b", "mean"),
                 S_FULL4B=("pass4b", "mean")).reset_index()
    SH["S_ISLEG4"] = fam["IS_legs_passed"].apply(lambda s: float((s >= ISLEG_BAR).mean())).values
    dump(SH, "shares.csv")
    P(f"  {len(SH)} families ({len(SH[SH.cadence.isin(HEADLINE_CADS)])} on the headline M/Q grid)")
    P("  share distribution by basis and cadence (mean over families):")
    P(SH.groupby("cadence")[BASES].mean().to_string(float_format=lambda x: f"{x:.4f}"))

    shmap = {(r.panel, r.book, r.gross, r.cadence): r for r in SH.itertuples()}

    def run_picks(floor, basis, permute_seed=None):
        out = []
        rng = np.random.default_rng(permute_seed) if permute_seed is not None else None
        for pname in panels:
            for cad in cads:
                sub0 = g10[(g10.panel == pname) & (g10.cadence == cad) & (g10.phase == 0)] \
                    .reset_index(drop=True)
                if rng is not None:
                    oc = [c for c in sub0.columns if c.startswith("OOS_")]
                    sub0 = sub0.copy()
                    sub0[oc] = sub0[oc].values[rng.permutation(len(sub0))]
                sh = np.array([getattr(shmap[(pname, r.book, r.gross, cad)], basis)
                               for r in sub0.itertuples()])
                keep = sh >= floor - 1e-12
                cand = sub0[keep].reset_index(drop=True)
                for ch in CHOOSERS:
                    if not len(cand):
                        out.append(dict(panel=pname, cadence=cad, chooser=ch, floor=floor,
                                        basis=basis, book="", gross="", share=np.nan,
                                        n_cand=0, empty=True))
                        continue
                    i = choose(ch, cand)
                    if i is None:
                        out.append(dict(panel=pname, cadence=cad, chooser=ch, floor=floor,
                                        basis=basis, book="", gross="", share=np.nan,
                                        n_cand=len(cand), empty=True))
                        continue
                    r = cand.iloc[i]
                    out.append(dict(
                        panel=pname, cadence=cad, chooser=ch, floor=floor, basis=basis,
                        book=r.book, gross=r.gross,
                        share=float(getattr(shmap[(pname, r.book, r.gross, cad)], basis)),
                        n_cand=len(cand), empty=False,
                        OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                        FULL_CAGR=r.CAGR, FULL_Sharpe=r.Sharpe, FULL_MaxDD=r.MaxDD,
                        spy_OOS_CAGR=r.spy_OOS_CAGR, spy_OOS_Sharpe=r.spy_OOS_Sharpe,
                        spy_MaxDD=r.spy_MaxDD, v2_Sharpe=r.v2_Sharpe, v2_MaxDD=r.v2_MaxDD,
                        OOS_4b=bool(r.pass4b), OOS_4a=bool(r.pass4a), fail_legs=r.fail_legs))
        return pd.DataFrame(out)

    ALL = pd.concat([run_picks(f, b) for b in BASES for f in FLOORS], ignore_index=True)
    dump(ALL, "picks.csv")

    # ---- the size-matched random-screen null (H_NULL) -----------------------------------
    # Cache each (panel, cadence) cell as plain arrays so 2,000 draws stay cheap.
    CELLS = {}
    for pname in panels:
        for cad in cads:
            s = g10[(g10.panel == pname) & (g10.cadence == cad) & (g10.phase == 0)] \
                .reset_index(drop=True)
            CELLS[(pname, cad)] = dict(
                IS_CAGR=s.IS_CAGR.values, IS_Sharpe=s.IS_Sharpe.values,
                IS_legs=s.IS_legs_passed.values.astype(float),
                p4b=s.pass4b.values.astype(bool), p4a=s.pass4a.values.astype(bool),
                oS=s.OOS_Sharpe.values, oD=s.OOS_MaxDD.values,
                share={b: np.array([getattr(shmap[(pname, r.book, r.gross, cad)], b)
                                    for r in s.itertuples()]) for b in BASES})

    def _pick_idx(ch, idx, C):
        if len(idx) == 0:
            return None
        if ch == "C_CAGR":
            return int(idx[_argmax(C["IS_CAGR"][idx], C["IS_Sharpe"][idx])])
        if ch == "C_SHARPE":
            return int(idx[_argmax(C["IS_Sharpe"][idx], C["IS_CAGR"][idx])])
        return int(idx[_argmax(C["IS_legs"][idx], C["IS_Sharpe"][idx])])

    def null_dist(keep_counts, cadset, draws=NULL_DRAWS, seed=NULL_SEED):
        """keep_counts[(panel, cadence)] = how many candidates the real screen kept."""
        rng = np.random.default_rng(seed)
        n4b, n4a, mS, mD = [], [], [], []
        keys = [(p, c) for p in panels for c in cadset if (p, c) in CELLS]
        for _ in range(draws):
            a = b_ = 0
            ss, dd = [], []
            for k in keys:
                C = CELLS[k]
                nk = keep_counts.get(k, 0)
                if nk <= 0:
                    continue
                idx = rng.choice(len(C["p4b"]), size=min(nk, len(C["p4b"])), replace=False)
                for ch in CHOOSERS:
                    i = _pick_idx(ch, idx, C)
                    if i is None:
                        continue
                    a += int(C["p4b"][i]); b_ += int(C["p4a"][i])
                    ss.append(C["oS"][i]); dd.append(C["oD"][i])
            n4b.append(a); n4a.append(b_)
            mS.append(np.median(ss) if ss else np.nan)
            mD.append(np.median(dd) if dd else np.nan)
        return (np.array(n4b), np.array(n4a), np.array(mS, float), np.array(mD, float))

    def build_null():
        nrows = []
        for b in BASES:
            for f in FLOORS[1:]:
                kc = {}
                for pname in panels:
                    for cad in HEADLINE_CADS:
                        if (pname, cad) not in CELLS:
                            continue
                        kc[(pname, cad)] = int((CELLS[(pname, cad)]["share"][b]
                                                >= f - 1e-12).sum())
                n4b, n4a, mS, mD = null_dist(kc, HEADLINE_CADS)
                s = ALL[(ALL.basis == b) & (ALL.floor == f) & ALL.cadence.isin(HEADLINE_CADS)]
                live = s[~s["empty"]]
                obs4b = int(live.OOS_4b.sum()) if len(live) else 0
                obs4a = int(live.OOS_4a.sum()) if len(live) else 0
                obsS = float(live.OOS_Sharpe.median()) if len(live) else np.nan
                obsD = float(live.OOS_MaxDD.median()) if len(live) else np.nan
                nrows.append(dict(
                    basis=b, legal=LEGAL[b], floor=f, kept=sum(kc.values()),
                    obs_4b=obs4b, null_4b_mean=round(float(n4b.mean()), 3),
                    pct_beaten_4b=round(float((n4b < obs4b).mean()
                                              + 0.5 * (n4b == obs4b).mean()), 4),
                    obs_4a=obs4a, null_4a_mean=round(float(n4a.mean()), 3),
                    obs_medS=round(obsS, 4), null_medS_mean=round(float(np.nanmean(mS)), 4),
                    pct_beaten_S=round(float(np.nanmean(mS < obsS)), 4),
                    obs_medDD=round(obsD, 4), null_medDD_mean=round(float(np.nanmean(mD)), 4),
                    pct_beaten_DD=round(float(np.nanmean(mD < obsD)), 4)))
        return pd.DataFrame(nrows)

    # G3b: the floor-0 control must reproduce idea 986's committed 36 picks
    g3b, g3bnote = np.nan, "parent walkforward not found"
    if PARENT_WF.exists():
        PW = pd.read_csv(PARENT_WF)
        ctrl = ALL[(ALL.floor == 0.0) & (ALL.basis == BASES[0])]
        m = PW.merge(ctrl, on=["panel", "cadence", "chooser"], suffixes=("_p", "_c"))
        g3b = float((m.book_p != m.book_c).sum() + (m.gross_p != m.gross_c).sum())
        g3bnote = f"{len(m)} shared picks"
    gates.append(dict(gate="G3b", what=f"CROSS-RUN: 986's unscreened rule-8 picks ({g3bnote})",
                      value=g3b, bar=0.0, ok=(g3b == 0.0)))
    P(f"  G3b cross-run, floor-0 control vs 986's committed picks : {g3b} disagreements "
      f"({g3bnote})")

    # G6 IS-purity: legal bases and their picks invariant under permuted OOS; leaky one is not
    dis_legal, dis_leak = 0, 0
    for b in BASES:
        for f in (0.25, 0.50):
            a = run_picks(f, b)
            c = run_picks(f, b, permute_seed=7)
            k = ["panel", "cadence", "chooser"]
            mm = a.merge(c, on=k, suffixes=("_a", "_c"))
            n = int((mm.book_a != mm.book_c).sum() + (mm.gross_a != mm.gross_c).sum())
            if LEGAL[b]:
                dis_legal += n
            else:
                dis_leak += n
    gates.append(dict(gate="G6a", what="IS-PURITY: LEGAL bases' picks invariant under permuted OOS",
                      value=float(dis_legal), bar=0.0, ok=dis_legal == 0))
    P(f"  G6a IS-purity, legal bases : {dis_legal} disagreements under permuted OOS columns")
    P(f"  G6b the LEAKY basis S_FULL4B is built from full-sample columns by construction; its "
      f"share is a function of the OOS tape and CANNOT be computed at 2016-12-31 "
      f"(pick disagreements under permuted OOS: {dis_leak} -- the screen itself reads the tape "
      f"whether or not the picks happen to move)")
    gates.append(dict(gate="G6b", what="the LEAKY basis is declared, not used for any verdict",
                      value=0.0, bar=0.0, ok=True))

    GT = pd.DataFrame(gates)
    P()
    P(f"  GATES: {int(GT.ok.sum())} of {len(GT)} PASS")
    P(GT.to_string(index=False))
    dump(GT, "gates.csv")
    if not GT.ok.all():
        P("  !! a gate FAILED -- results below are NOT to be read as evidence")

    # ---------------------------------------------------------------- the answer
    P()
    P("=" * 100)
    P("(D) DOES THE SCREEN BUY ANY OOS 4b OR 4a? -- every (floor x basis) point")
    P("=" * 100)

    def summarise(sel, label):
        rows_ = []
        for b in BASES:
            for f in FLOORS:
                s = ALL[(ALL.basis == b) & (ALL.floor == f) & sel(ALL)]
                live = s[~s.empty_]  if "empty_" in s else s[~s["empty"]]
                rows_.append(dict(
                    grid=label, basis=b, legal=LEGAL[b], floor=f, n_slots=len(s),
                    n_empty=int(s["empty"].sum()), n_picks=len(live),
                    OOS_4b=int(live.OOS_4b.sum()) if len(live) else 0,
                    OOS_4a=int(live.OOS_4a.sum()) if len(live) else 0,
                    med_OOS_Sharpe=round(float(live.OOS_Sharpe.median()), 4) if len(live) else np.nan,
                    med_OOS_CAGR=round(float(live.OOS_CAGR.median()), 4) if len(live) else np.nan,
                    med_OOS_MaxDD=round(float(live.OOS_MaxDD.median()), 4) if len(live) else np.nan,
                    med_FULL_Sharpe=round(float(live.FULL_Sharpe.median()), 4) if len(live) else np.nan,
                    med_FULL_MaxDD=round(float(live.FULL_MaxDD.median()), 4) if len(live) else np.nan,
                    ext_share=round(float((live.gross == "EXT").mean()), 4) if len(live) else np.nan))
        return pd.DataFrame(rows_)

    SUM = pd.concat([
        summarise(lambda d: d.cadence.isin(HEADLINE_CADS), "MQ60"),
        summarise(lambda d: d.cadence.isin(EXT_CADS), "DW60"),
        summarise(lambda d: d.cadence.isin(cads), "ALL120"),
    ], ignore_index=True)
    dump(SUM, "summary.csv")
    for lab in ("MQ60", "DW60", "ALL120"):
        P()
        P(f"  --- {lab} ---")
        P(SUM[SUM.grid == lab].drop(columns=["grid"]).to_string(index=False))

    # ---- CELL-MATCHED control: the screen empties whole (panel, cadence) cells, so a raw
    # comparison against the 18-slot control partly measures WHICH PANELS survived, not which
    # books.  This re-runs the UNSCREENED control restricted to exactly the cells each screen
    # left non-empty.  Any gain that survives here is a book effect, not a panel effect.
    P()
    P("  CELL-MATCHED CONTROL (MQ60) -- the unscreened control restricted to exactly the cells "
      "each screen left non-empty, so the panel composition is identical on both sides")
    crows = []
    base_all = ALL[(ALL.floor == 0.0) & (ALL.basis == "S_IS4B") & ALL.cadence.isin(HEADLINE_CADS)]
    for b in BASES:
        for f in FLOORS[1:]:
            s = ALL[(ALL.basis == b) & (ALL.floor == f) & ALL.cadence.isin(HEADLINE_CADS)]
            live = s[~s["empty"]]
            cells = set(zip(live.panel, live.cadence))
            cm = base_all[[(p, c) in cells for p, c in zip(base_all.panel, base_all.cadence)]]
            crows.append(dict(
                basis=b, legal=LEGAL[b], floor=f, cells_kept=len(cells), n_picks=len(live),
                scr_4b=int(live.OOS_4b.sum()) if len(live) else 0,
                ctl_4b=int(cm.OOS_4b.sum()) if len(cm) else 0,
                scr_4a=int(live.OOS_4a.sum()) if len(live) else 0,
                ctl_4a=int(cm.OOS_4a.sum()) if len(cm) else 0,
                scr_medS=round(float(live.OOS_Sharpe.median()), 4) if len(live) else np.nan,
                ctl_medS=round(float(cm.OOS_Sharpe.median()), 4) if len(cm) else np.nan,
                scr_medDD=round(float(live.OOS_MaxDD.median()), 4) if len(live) else np.nan,
                ctl_medDD=round(float(cm.OOS_MaxDD.median()), 4) if len(cm) else np.nan,
                dropped_panels=",".join(sorted({p for p in base_all.panel.unique()
                                                if not any(pc[0] == p for pc in cells)})) or "-"))
    CM = pd.DataFrame(crows)
    CM["d_medS"] = (CM.scr_medS - CM.ctl_medS).round(4)
    CM["d_medDD"] = (CM.scr_medDD - CM.ctl_medDD).round(4)
    P(CM.to_string(index=False))
    dump(CM, "cellmatched.csv")

    P()
    P("  THE SIZE-MATCHED RANDOM-SCREEN NULL (MQ60) -- does the SHARE carry information, or "
      f"does ANY screen that shrinks the candidate set do this?  {NULL_DRAWS:,} draws, "
      f"seed {NULL_SEED}, same kept-count per (panel, cadence) cell")
    NL = build_null()
    P(NL.to_string(index=False))
    dump(NL, "null.csv")

    # ---------------------------------------------------------------- hypotheses
    P()
    P("=" * 100)
    P("(E) THE PRE-REGISTERED HYPOTHESES  (headline grid = MQ60, the idea's 60 families)")
    P("=" * 100)
    H = SUM[SUM.grid == "MQ60"]
    ctrl = H[(H.floor == 0.0) & (H.basis == "S_IS4B")].iloc[0]
    legal = H[H.legal & (H.floor > 0.0)]
    leaky = H[~H.legal & (H.floor > 0.0)]
    hyp = []
    b4b = int(legal.OOS_4b.max()) if len(legal) else 0
    hyp.append(dict(H="H_BUY4B", what="MQ60: some LEGAL (floor, basis) yields >= 1 OOS 4b",
                    value=float(b4b), bar=1.0, verdict="PASS" if b4b >= 1 else "FAIL",
                    detail=f"unscreened control {int(ctrl.OOS_4b)} of {int(ctrl.n_picks)}"))
    b4a = int(legal.OOS_4a.max()) if len(legal) else 0
    hyp.append(dict(H="H_BUY4A", what="MQ60: some LEGAL (floor, basis) yields >= 1 OOS 4a",
                    value=float(b4a), bar=1.0, verdict="PASS" if b4a >= 1 else "FAIL",
                    detail=f"unscreened control {int(ctrl.OOS_4a)} of {int(ctrl.n_picks)}"))
    # "best legal point" = highest OOS 4b, then highest median OOS Sharpe, among points that
    # still fill at least half the 18 slots (a screen that empties the grid is not a screen)
    cand = legal[legal.n_picks >= 0.5 * ctrl.n_picks]
    if not len(cand):
        cand = legal
    best = cand.sort_values(["OOS_4b", "med_OOS_Sharpe"], ascending=False).iloc[0]
    hyp.append(dict(H="H_DD", what="best legal point: median OOS MaxDD no worse than control",
                    value=float(best.med_OOS_MaxDD), bar=float(ctrl.med_OOS_MaxDD),
                    verdict="PASS" if best.med_OOS_MaxDD >= ctrl.med_OOS_MaxDD else "FAIL",
                    detail=f"{best.basis}@{best.floor:.2f}  control {ctrl.med_OOS_MaxDD:.4f}"))
    hyp.append(dict(H="H_SHARPE", what="best legal point: median OOS Sharpe > control",
                    value=float(best.med_OOS_Sharpe), bar=float(ctrl.med_OOS_Sharpe),
                    verdict="PASS" if best.med_OOS_Sharpe > ctrl.med_OOS_Sharpe else "FAIL",
                    detail=f"{best.basis}@{best.floor:.2f}  control {ctrl.med_OOS_Sharpe:.4f}"))
    lk = int(leaky.OOS_4b.max()) if len(leaky) else 0
    hyp.append(dict(H="H_LEGAL", what="LEGAL bases match the LEAKY control's best OOS 4b",
                    value=float(b4b), bar=float(lk),
                    verdict="PASS" if b4b >= lk else "FAIL",
                    detail=f"leaky S_FULL4B best OOS 4b {lk}"))
    nb = NL[(NL.basis == best.basis) & (NL.floor == best.floor)]
    pb = float(nb.pct_beaten_4b.iloc[0]) if len(nb) else np.nan
    hyp.append(dict(H="H_NULL", what="best legal point beats >= 0.95 of size-matched random screens",
                    value=pb, bar=BAR_NULL, verdict="PASS" if pb >= BAR_NULL else "FAIL",
                    detail=f"{best.basis}@{best.floor:.2f}, null mean OOS 4b "
                           f"{float(nb.null_4b_mean.iloc[0]) if len(nb) else np.nan:.3f} "
                           f"vs observed {int(best.OOS_4b)}"))
    bb = H[(H.basis == best.basis) & (H.floor > 0.0)]
    nfl = int((bb.OOS_4b >= 1).sum())
    hyp.append(dict(H="H_CONSIST", what=f"OOS 4b >= 1 at EVERY floor > 0 on {best.basis}",
                    value=float(nfl), bar=float(len(bb)),
                    verdict="PASS" if nfl == len(bb) else "FAIL",
                    detail=f"{nfl} of {len(bb)} floors"))
    cmb = CM[(CM.basis == best.basis) & (CM.floor == best.floor)]
    dS = float(cmb.d_medS.iloc[0]) if len(cmb) else np.nan
    dD = float(cmb.d_medDD.iloc[0]) if len(cmb) else np.nan
    hyp.append(dict(H="H_CELLMATCH", what="best legal point still beats the CELL-MATCHED control "
                                          "on median OOS Sharpe AND MaxDD",
                    value=min(dS, dD), bar=0.0,
                    verdict="PASS" if (dS > 0 and dD > 0) else "FAIL",
                    detail=f"dSharpe {dS:+.4f}, dMaxDD {dD:+.4f}; dropped "
                           f"{cmb.dropped_panels.iloc[0] if len(cmb) else '?'}"))
    HY = pd.DataFrame(hyp)
    P(HY.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(HY, "hypotheses.csv")

    # ---------------------------------------------------------------- what the screen moved
    P()
    P("  WHAT THE SCREEN ACTUALLY MOVES -- picks changed vs the unscreened control (MQ60):")
    base = ALL[(ALL.floor == 0.0) & (ALL.basis == "S_IS4B") & ALL.cadence.isin(HEADLINE_CADS)]
    mrows = []
    for b in BASES:
        for f in FLOORS[1:]:
            s = ALL[(ALL.basis == b) & (ALL.floor == f) & ALL.cadence.isin(HEADLINE_CADS)]
            m = base.merge(s, on=["panel", "cadence", "chooser"], suffixes=("_0", "_f"))
            ch = m[(m.book_0 != m.book_f) | (m.gross_0 != m.gross_f)]
            mrows.append(dict(basis=b, legal=LEGAL[b], floor=f, n_changed=len(ch),
                              n_emptied=int(m.empty_f.sum()),
                              to_EXT=int(((m.gross_0 == "CORE") & (m.gross_f == "EXT")).sum()),
                              to_CORE=int(((m.gross_0 == "EXT") & (m.gross_f == "CORE")).sum()),
                              dSharpe=round(float((m.OOS_Sharpe_f - m.OOS_Sharpe_0).mean()), 4),
                              dMaxDD=round(float((m.OOS_MaxDD_f - m.OOS_MaxDD_0).mean()), 4)))
    MV = pd.DataFrame(mrows)
    P(MV.to_string(index=False))
    dump(MV, "moves.csv")

    # the standing candidate, for continuity with 973/981/982/984/986
    P()
    sc = ALL[(ALL.OOS_4b) & ALL.cadence.isin(cads)]
    if len(sc):
        u = sc.drop_duplicates(["panel", "cadence", "book", "gross"])
        P("  every OOS 4b passer seen anywhere in this run (any floor, any basis, any cadence):")
        P(u[["panel", "cadence", "book", "gross", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
             "FULL_Sharpe", "FULL_MaxDD", "OOS_4a"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    else:
        P("  NO OOS 4b passer anywhere in this run, at any floor, basis or cadence.")
    r0 = ALL[~ALL["empty"]].iloc[0]
    P(f"  comparands: SPY OOS {r0.spy_OOS_CAGR:.2%} / {r0.spy_OOS_Sharpe:.4f} / "
      f"{r0.spy_MaxDD:.2%} (full-sample MaxDD)")
    for pname in panels:
        rr = ALL[(~ALL["empty"]) & (ALL.panel == pname)].iloc[0]
        P(f"  RULES v2 (live) {pname:6s} full-sample Sharpe {rr.v2_Sharpe:.4f}  "
          f"MaxDD {rr.v2_MaxDD:.2%}")

    P()
    P("=" * 100)
    P("(F) VERDICT")
    P("=" * 100)
    P(f"  {int((HY.verdict == 'PASS').sum())} of {len(HY)} pre-registered hypotheses PASS")
    P(f"  MQ60 unscreened control: OOS 4b {int(ctrl.OOS_4b)}/{int(ctrl.n_picks)}, "
      f"OOS 4a {int(ctrl.OOS_4a)}/{int(ctrl.n_picks)}, median OOS Sharpe "
      f"{ctrl.med_OOS_Sharpe:.4f}, median OOS MaxDD {ctrl.med_OOS_MaxDD:.2%}")
    P(f"  best legal screen: {best.basis}@floor {best.floor:.2f} -> OOS 4b {int(best.OOS_4b)}, "
      f"OOS 4a {int(best.OOS_4a)}, median OOS Sharpe {best.med_OOS_Sharpe:.4f}, "
      f"median OOS MaxDD {best.med_OOS_MaxDD:.2%}, {int(best.n_picks)} of "
      f"{int(best.n_slots)} slots filled")
    P(f"  LEAKY S_FULL4B best OOS 4b over floors > 0: {lk}")
    P(f"  size-matched random-screen null at that point: mean OOS 4b "
      f"{float(nb.null_4b_mean.iloc[0]) if len(nb) else float('nan'):.3f}, "
      f"observed beats {pb:.4f} of {NULL_DRAWS:,} draws")
    P(f"  [{time.time()-t0:.0f}s]")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"wrote {STEM}.console.txt")


if __name__ == "__main__":
    main()

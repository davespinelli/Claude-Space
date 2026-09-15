#!/usr/bin/env python3
"""
Idea 986 (cloud, 2026-09-15)
IS THE FAST END OF THE LADDER AN H1-SHARPE TEST THE WAY THE SLOW END IS A DRAWDOWN TEST?

  Idea 984 found, on an independently rebuilt 13,500-row D/W/M/Q ladder, that `L4_DD`'s
  fail rate collapses 0.879 -> 0.640 from M/Q to D/W while `L1_H1` goes 0.293 -> 0.580 and
  from NEVER modal to modal on half the D/W cells.  It also found the record carries 311
  `L4_DD` leg claims against 8 `L1_H1` ones.  The obvious reading -- "at speed, 4b becomes
  an H1-Sharpe test" -- is exactly the kind of cadence-free leg claim 984 just KILLed, so
  it gets PRICED here rather than published.

  THE QUESTION IS NOT "which leg fails most at D/W".  It is whether the fast end supports a
  SINGLE-LEG READING at all, i.e. whether some leg L makes "4b passes iff L passes" an
  accurate rule, the way `L4_DD` is claimed to at M/Q.  Fail rate alone cannot answer that:
  a leg can fail 0.58 of the time and be useless as a reading if its failures do not line
  up with the 4b verdict.  So the census reports, per (leg x cadence half x leg definition):

      fail        -- P(leg fails)
      bind        -- P(leg fails | the book fails 4b)          (984's "among the failed legs")
      only        -- P(leg is the ONLY failed leg)             (984's "only-leg")
      modal       -- share of (panel, cadence) cells where the leg is the modal failure
      AGREE       -- P(leg verdict == 4b verdict)              <- the single-leg reading
      lift        -- AGREE minus the majority-class base rate  <- what the reading BUYS
      MCC         -- Matthews phi between leg verdict and 4b verdict (base-rate robust)

  `AGREE` is the object the queue is asking about and the one the record has never reported.
  `AGREE` is inflated wherever 4b almost never passes, so `lift` and `MCC` are published
  beside it at every point; a reading that cannot beat "everything fails" is not a reading.

TUNED AXES -- exactly two, every level reported, none selected:
  (1) ladder half : FINE2 = D/W, COARSE2 = M/Q, plus all four single cadences D, W, M, Q
  (2) leg definition : REC (the record's mixed form: H1/H2 full-sample, OOS/DD/CAGR on the
      OOS window), ISONLY (every leg on 2009-2016), OOSLOC (every leg window-local on OOS)

PRE-REGISTERED HYPOTHESES (bars fixed before any number was read):
  H_FASTSINGLE : at D/W, max over legs of AGREE >= 0.90            -- the fast end has A reading
  H_FASTH1     : that argmax leg is `L1_H1`                        -- and the reading is H1
  H_SLOWSINGLE : at M/Q, max over legs of AGREE >= 0.90            -- the slow end has one
  H_SLOWDD     : that argmax leg is `L4_DD`                        -- and it is DD (the control)
  H_ONLYFAST   : `L1_H1` only-failed-leg share at D/W >= 0.20      -- mirror of DD's 0.388 at M/Q
  H_LIFT       : at D/W the best leg's lift over the base rate >= 0.10
  H_FASTMCC    : at D/W the best leg's MCC >= 0.30                 -- base-rate-robust form
  H_SLOWMCC    : at M/Q the best leg's MCC >= 0.30                 -- the same test on the control

  H_FASTMCC / H_SLOWMCC and the MCC column were added after the SMOKE wiring check (a 3-phase,
  D/M-only grid whose G3 fails by construction) and BEFORE the full ladder was built or read.
  Every other bar and definition predates the first run.

GATES (printed before any hypothesis number):
  G0  offset_mask(idx, per, 0) == engine.rebalance_mask(idx, per) on D/W/M/Q
  G1  the fast Ctx runner == engine.backtest on returns AND turnover, post warm-up, D and M
  G2  BAND03 @ 0.75 == baseline.rules_v2_weights elementwise
  G3  CROSS-RUN: idea 984's published cadence-balanced re-score table (L4_DD 0.879/0.640,
      L1_H1 0.293/0.580, L5_CAGR 0.350/0.483, L3_OOS 0.448/0.560, L2_H2 0.488/0.533, and the
      only/modal rows) reproduced from this run's own independent rebuild
  G4  MATCHED GROSS: the target weight matrix is identical across all four cadences
  G5  determinism: one cell rebuilt from scratch, max|d| over returns and turnover
  G6  rule-8 choosers are IS-ONLY -- picks invariant under permuted OOS columns

PROTOCOL: 10 bps primary (all five rungs built and reported), decided at close t / applied
t+1 (LAG 1), warm-up 260 days, IS 2009-2016 / OOS 2017-2026 read once, no shorting, no
leverage beyond the published gross.  Rule 8 walk-forward is run and both KEEP paths (4a and
4b) evaluated.  Nothing in RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py is touched.

SURVIVORSHIP (rule 9): U56, B136 and SMALL are CURRENT-CONSTITUENT lists (SMALL additionally
drops every ticker with max_1d_move >= 1.0 per data/small_meta.csv), so every CAGR level is
optimistic, every drawdown level is optimistic, and every leg fail rate is a LOWER bound.
The object measured here is a DIFFERENCE between two halves of one ladder -- same names,
same tape, only the rebalance schedule moves -- and is very nearly immune to that bias.  The
rule-8 4b levels are read against SPY, which is not survivorship-inflated, so every 4b PASS
is an upper bound and every FAIL is understated.

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

LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
LEGNAME = {"H1": "L1_H1", "H2": "L2_H2", "OOS": "L3_OOS", "DD": "L4_DD", "CAGR": "L5_CAGR"}

# tuned axis (1): ladder half
HALVES = {"FINE2": ["D", "W"], "COARSE2": ["M", "Q"],
          "D": ["D"], "W": ["W"], "M": ["M"], "Q": ["Q"]}
# tuned axis (2): leg definition
LEGDEFS = ["REC", "ISONLY", "OOSLOC"]

# pre-registered bars
BAR_SINGLE = 0.90
BAR_ONLY = 0.20
BAR_LIFT = 0.10
BAR_MCC = 0.30

# idea 984's committed cadence-balanced re-score table (G3)
PUB_984 = {
    ("DD", "fail"): (0.879, 0.640), ("DD", "only"): (0.388, 0.097), ("DD", "modal"): (1.000, 0.500),
    ("H1", "fail"): (0.293, 0.580), ("H1", "modal"): (0.000, 0.500),
    ("CAGR", "fail"): (0.350, 0.483), ("OOS", "fail"): (0.448, 0.560), ("H2", "fail"): (0.488, 0.533),
}
G3_TOL = 5e-3

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
# (1) cadence / phase machinery -- the record's form (ideas 938/942/962/964/976/981/984)
# =========================================================================================
def offset_mask(idx, per, d):
    """Rebalance d trading days BEFORE each period end; clipped at the period's first day."""
    if per == "D":
        out = pd.Series(True, index=idx)
        return out, 0
    key = pd.Series(idx.to_period(per), index=idx)
    last = np.flatnonzero((key != key.shift(-1)).values)
    first = np.concatenate([[0], last[:-1] + 1])
    pick = np.maximum(last - d, first)
    out = pd.Series(False, index=idx)
    out.iloc[np.unique(pick)] = True
    return out, int((last - d < first).sum())


class Ctx:
    """Vectorised equivalent of engine.backtest for a fixed rebalance mask (gated at G1)."""

    def __init__(self, px, mask):
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        m = np.asarray(mask.values, bool)
        m = np.concatenate([[False], m[:-1]]).copy()   # decided at t, applied t+1
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


# ---- the three leg definitions (tuned axis 2) -------------------------------------------
def legs_REC(row):
    """The record's mixed form: H1/H2 full-sample, Sharpe/DD/CAGR on the OOS window."""
    return dict(H1=row["H1"] > row["spy_H1"], H2=row["H2"] > row["spy_H2"],
                OOS=row["OOS_Sharpe"] > row["spy_OOS_Sharpe"],
                DD=abs(row["OOS_MaxDD"]) <= DD_CAP * abs(row["spy_MaxDD"]),
                CAGR=row["OOS_CAGR"] >= CAGR_FLOOR * row["spy_CAGR"])


def legs_ISONLY(row):
    return dict(H1=row["IS_H1"] > row["spy_IS_H1"], H2=row["IS_H2"] > row["spy_IS_H2"],
                OOS=row["IS_Sharpe"] > row["spy_IS_Sharpe"],
                DD=abs(row["IS_MaxDD"]) <= DD_CAP * abs(row["spy_IS_MaxDD"]),
                CAGR=row["IS_CAGR"] >= CAGR_FLOOR * row["spy_IS_CAGR"])


def legs_OOSLOC(row):
    """Every leg read window-local on 2017-2026 -- H1/H2 are the OOS window's own halves."""
    return dict(H1=row["OOS_H1"] > row["spy_OOS_H1"], H2=row["OOS_H2"] > row["spy_OOS_H2"],
                OOS=row["OOS_Sharpe"] > row["spy_OOS_Sharpe"],
                DD=abs(row["OOS_MaxDD"]) <= DD_CAP * abs(row["spy_OOS_MaxDD"]),
                CAGR=row["OOS_CAGR"] >= CAGR_FLOOR * row["spy_OOS_CAGR"])


LEGFN = {"REC": legs_REC, "ISONLY": legs_ISONLY, "OOSLOC": legs_OOSLOC}


def slacks_REC(row):
    return dict(
        H1=(row["H1"] - row["spy_H1"]) / abs(row["spy_H1"]),
        H2=(row["H2"] - row["spy_H2"]) / abs(row["spy_H2"]),
        OOS=(row["OOS_Sharpe"] - row["spy_OOS_Sharpe"]) / abs(row["spy_OOS_Sharpe"]),
        DD=(DD_CAP * abs(row["spy_MaxDD"]) - abs(row["OOS_MaxDD"])) / (DD_CAP * abs(row["spy_MaxDD"])),
        CAGR=(row["OOS_CAGR"] - CAGR_FLOOR * row["spy_CAGR"]) / abs(CAGR_FLOOR * row["spy_CAGR"]),
    )


def pass4a(row):
    return bool(row["H1"] > row["v2_H1"] and row["H2"] > row["v2_H2"]
                and row["MaxDD"] >= row["v2_MaxDD"])


# =========================================================================================
# (2) the book set -- 942/962/964/976/981/984's five books verbatim
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


# =========================================================================================
# (3) the census -- cadence-balanced, because the ladder carries 1/5/21/63 phases
# =========================================================================================
def cbal(g, cads, col):
    """Mean of `col` with each cadence weighted equally (not each row)."""
    vals = []
    for cad in cads:
        s = g.loc[g.cadence == cad, col]
        if len(s):
            vals.append(float(s.mean()))
    return float(np.mean(vals)) if vals else np.nan


def mcc(pred, truth):
    """Matthews phi between two boolean vectors; 0.0 when a margin is degenerate."""
    p = np.asarray(pred, bool)
    t = np.asarray(truth, bool)
    tp = float((p & t).sum()); tn = float((~p & ~t).sum())
    fp = float((p & ~t).sum()); fn = float((~p & t).sum())
    den = np.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    return float((tp * tn - fp * fn) / den) if den > 0 else 0.0


def cbal_mcc(g, cads, predcol, truthcol):
    v = []
    for cad in cads:
        s = g[g.cadence == cad]
        if len(s):
            v.append(mcc(s[predcol].values, s[truthcol].values))
    return float(np.mean(v)) if v else np.nan


def modal_share(g, cads, leg, ties=True):
    """Share of (panel, cadence) cells in which `leg` is the most-often-failed leg.
    ties=True counts a tied leg as modal; ties=False requires a strict outright maximum.
    Idea 984 published a `modal` row without naming its cell or tie rule, so BOTH are
    reported here and the cross-run gate is scored against both."""
    hits, tot = 0, 0
    for cad in cads:
        for pan in sorted(g.panel.unique()):
            sub = g[(g.cadence == cad) & (g.panel == pan)]
            if not len(sub):
                continue
            rates = {k: float((~sub["leg_" + k]).mean()) for k in LEGS}
            top = max(rates.values())
            tot += 1
            if top <= 0:
                continue
            if ties:
                if rates[leg] >= top - 1e-12:
                    hits += 1
            else:
                win = [k for k in LEGS if rates[k] >= top - 1e-12]
                if win == [leg]:
                    hits += 1
    return (hits / tot) if tot else np.nan


def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 986 (cloud, 2026-09-15) -- IS THE FAST END OF THE LADDER AN H1-SHARPE TEST")
    P("=" * 100)
    P(f"  SMOKE={SMOKE}  cost rungs {RUNGS} (headline {HEAD_COST:.0f} bps)  LAG={LAG}  WARM={WARM}")
    P(f"  ladder {CADORDER} at MATCHED GROSS {GROSSES}; phases per cadence {CADENCES}")
    P(f"  tuned axes: ladder half {list(HALVES)} x leg definition {LEGDEFS} -- ALL reported")
    P(f"  bars: AGREE >= {BAR_SINGLE}, only >= {BAR_ONLY}, lift >= {BAR_LIFT}")

    # ---------------------------------------------------------------- panels
    P()
    P("loading panels ...")
    u56 = load_universe()
    b136 = load_universe(broad=True)
    small, ndrop = load_small()
    panels = {"U56": u56, "B136": b136, "SMALL": small}
    for k, v in panels.items():
        P(f"  {k:6s} {v.shape[1]:4d} cols  {v.index[0].date()} .. {v.index[-1].date()}  "
          f"{len(v):,} rows")
    P(f"  SMALL dropped {ndrop} tickers with max_1d_move >= 1.0 (data/small_meta.csv)")

    # ---------------------------------------------------------------- gates
    P()
    P("=" * 100)
    P("(A) GATES -- printed before any hypothesis number")
    P("=" * 100)
    gates = []

    bad = sum(int((offset_mask(u56.index, per, 0)[0].values
                   != rebalance_mask(u56.index, per).values).sum()) for per in CADORDER)
    gates.append(dict(gate="G0", what="offset_mask(.,per,0) == engine.rebalance_mask on D/W/M/Q",
                      value=float(bad), bar=0.0, ok=bad == 0))
    P(f"  G0  offset_mask vs engine.rebalance_mask, D/W/M/Q : {bad} disagreeing rows")

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

    d = float(np.abs(BOOKS["BAND03"](u56, 0.75).values
                     - rules_v2_weights(u56).values).max())
    gates.append(dict(gate="G2", what="BAND03@0.75 == baseline.rules_v2_weights",
                      value=d, bar=1e-12, ok=d < 1e-12))
    P(f"  G2  BAND03@0.75 vs baseline.rules_v2_weights : max|d| {d:.3e}")

    tw = {}
    for pname, px in panels.items():
        for bk in BOOKORDER:
            for gn, gv in GROSSES.items():
                tw[(pname, bk, gn)] = shift1(BOOKS[bk](px, gv), px.index)
    P(f"  G4  matched gross: {len(tw)} (panel, book, gross) target matrices built ONCE and "
      f"reused across all four cadences -- cadence cannot change the target by construction")
    gates.append(dict(gate="G4", what="MATCHED GROSS: one target matrix reused across D/W/M/Q",
                      value=0.0, bar=0.0, ok=True))

    # ---------------------------------------------------------------- the ladder
    P()
    P("=" * 100)
    P("(B) THE LADDER -- independently rebuilt; every (panel, book, gross, cadence, phase) "
      "x 5 rungs")
    P("=" * 100)
    rows, det_store = [], {}
    cads = CADORDER if not SMOKE else ["D", "M"]
    for pname, px in panels.items():
        rspy = px["SPY"].pct_change().fillna(0.0).values
        isw = np.asarray(px.index <= pd.Timestamp(IS_END))
        osw = np.asarray(px.index >= pd.Timestamp(OOS_START))
        spy_full = mets(rspy[WARM:])
        spy_is = mets(rspy[WARM:][isw[WARM:]])
        spy_oos = mets(rspy[osw])
        v2 = mets(backtest(px, rules_v2_weights(px), cost_bps=HEAD_COST, freq="W")["returns"]
                  .values[WARM:])
        for cad in cads:
            nph = CADENCES[cad] if not SMOKE else min(CADENCES[cad], 3)
            for ph in range(nph):
                m, clipped = offset_mask(px.index, cad, ph)
                ctx = Ctx(px, m)
                for bk in BOOKORDER:
                    for gn in GROSSES:
                        r, tu, _ = ctx.run(tw[(pname, bk, gn)])
                        for cb in RUNGS:
                            net = r - tu * cb / 1e4
                            f = mets(net[WARM:])
                            i_ = mets(net[WARM:][isw[WARM:]])
                            o_ = mets(net[osw])
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
    nbooks = len(G.groupby(["panel", "book", "gross", "cadence", "phase"]))
    P(f"  ladder {len(G):,} rows over {nbooks:,} phase-books")

    # leg columns for all three definitions
    for ld in LEGDEFS:
        fn = LEGFN[ld]
        lg = pd.DataFrame([fn(r) for r in G.to_dict("records")])
        for k in LEGS:
            G[f"{ld}_leg_{k}"] = lg[k].values.astype(bool)
        G[f"{ld}_pass4b"] = lg[LEGS].all(axis=1).values
        G[f"{ld}_nfail"] = (~lg[LEGS]).sum(axis=1).values
    sl = pd.DataFrame([slacks_REC(r) for r in G.to_dict("records")])
    for k in LEGS:
        G["slack_" + k] = sl[k].values
    G["pass4a"] = [pass4a(r) for r in G.to_dict("records")]
    G["IS_legs_passed"] = 5 - G["ISONLY_nfail"]

    # G5 determinism
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
    g10 = G[G.cost_bps == HEAD_COST]
    g3rows, g3a_max, g3b_max = [], 0.0, 0.0
    for (leg, stat), (pub_mq, pub_dw) in PUB_984.items():
        for half, pub in (("COARSE2", pub_mq), ("FINE2", pub_dw)):
            sub = g10[g10.cadence.isin(HALVES[half])]
            alt = np.nan
            if stat == "fail":
                got = cbal(sub.assign(x=~sub["REC_leg_" + leg]), HALVES[half], "x")
            elif stat == "only":
                x = (sub["REC_nfail"] == 1) & (~sub["REC_leg_" + leg])
                got = cbal(sub.assign(x=x), HALVES[half], "x")
            else:
                gg = sub.rename(columns={f"REC_leg_{k}": f"leg_{k}" for k in LEGS})
                got = modal_share(gg, HALVES[half], leg, ties=True)
                alt = modal_share(gg, HALVES[half], leg, ties=False)
            dd = abs(got - pub)
            if np.isfinite(alt):
                dd = min(dd, abs(alt - pub))
            if stat == "modal":
                g3b_max = max(g3b_max, dd)
            else:
                g3a_max = max(g3a_max, dd)
            g3rows.append(dict(leg=LEGNAME[leg], stat=stat, half=half, published_984=pub,
                               rebuilt_ties=round(got, 4),
                               rebuilt_strict=(round(alt, 4) if np.isfinite(alt) else ""),
                               best_absdiff=round(dd, 5), ok=bool(dd <= G3_TOL)))
    G3 = pd.DataFrame(g3rows)
    gates.append(dict(gate="G3a", what="CROSS-RUN: idea 984's published fail/only re-score rows",
                      value=g3a_max, bar=G3_TOL, ok=g3a_max <= G3_TOL))
    gates.append(dict(gate="G3b", what="CROSS-RUN: 984's `modal` rows (cell/tie rule not published)",
                      value=g3b_max, bar=G3_TOL, ok=g3b_max <= G3_TOL))
    na = int((G3.stat != "modal").sum())
    P(f"  G3a cross-run, 984's fail/only rows ({na} cells) : max|d| {g3a_max:.5f}")
    P(f"  G3b cross-run, 984's modal rows ({len(G3)-na} cells) : max|d| {g3b_max:.5f} "
      f"(984 published no cell or tie rule; both rules reported)")
    dump(G3, "crossrun.csv")

    # ---------------------------------------------------------------- rule 8
    P()
    P("=" * 100)
    P("(C) RULE 8 WALK-FORWARD -- (book, gross) chosen on 2009-2016 ALONE, 2017-2026 read once")
    P("=" * 100)
    picks, perm_dis = [], 0
    rng = np.random.default_rng(0)
    for pname in panels:
        for cad in cads:
            sub0 = g10[(g10.panel == pname) & (g10.cadence == cad) & (g10.phase == 0)] \
                .reset_index(drop=True)
            for ch in CHOOSERS:
                i = choose(ch, sub0)
                if i is None:
                    continue
                perm = sub0.copy()
                oc = [c for c in perm.columns if c.startswith("OOS_")]
                perm[oc] = perm[oc].values[rng.permutation(len(perm))]
                if choose(ch, perm) != i:
                    perm_dis += 1
                r = sub0.iloc[i]
                lg = legs_REC(r)
                picks.append(dict(
                    panel=pname, cadence=cad, chooser=ch, book=r.book, gross=r.gross,
                    IS_CAGR=r.IS_CAGR, IS_Sharpe=r.IS_Sharpe,
                    OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                    FULL_Sharpe=r.Sharpe, FULL_MaxDD=r.MaxDD, FULL_CAGR=r.CAGR,
                    spy_OOS_CAGR=r.spy_OOS_CAGR, spy_OOS_Sharpe=r.spy_OOS_Sharpe,
                    spy_MaxDD=r.spy_MaxDD,
                    v2_Sharpe=r.v2_Sharpe, v2_MaxDD=r.v2_MaxDD,
                    **{"leg_" + k: bool(lg[k]) for k in LEGS},
                    OOS_4b=bool(all(lg.values())), OOS_4a=bool(r.pass4a),
                    fail_legs=",".join(LEGNAME[k] for k in LEGS if not lg[k]) or "-"))
    PK = pd.DataFrame(picks)
    gates.append(dict(gate="G6", what="rule-8 choosers IS-ONLY (picks invariant under permuted OOS)",
                      value=float(perm_dis), bar=0.0, ok=perm_dis == 0))
    P(f"  G6  IS-only choosers : {perm_dis} disagreements under permuted OOS columns")
    dump(PK, "walkforward.csv")

    GT = pd.DataFrame(gates)
    P()
    P(f"  GATES: {int(GT.ok.sum())} of {len(GT)} PASS")
    P(GT.to_string(index=False))
    dump(GT, "gates.csv")
    if not GT.ok.all():
        P("  !! a gate FAILED -- results below are NOT to be read as evidence")

    P()
    P(f"  picks {len(PK)} = {len(panels)} panels x {len(cads)} cadences x {len(CHOOSERS)} "
      f"choosers;  OOS 4b {int(PK.OOS_4b.sum())} of {len(PK)};  "
      f"OOS 4a {int(PK.OOS_4a.sum())} of {len(PK)}")
    P(PK[["panel", "cadence", "chooser", "book", "gross", "OOS_CAGR", "OOS_Sharpe",
          "OOS_MaxDD", "OOS_4b", "OOS_4a", "fail_legs"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    if PK.OOS_4b.any():
        P()
        P("  OOS 4b PASSERS:")
        P(PK[PK.OOS_4b][["panel", "cadence", "chooser", "book", "gross", "OOS_CAGR",
                         "OOS_Sharpe", "OOS_MaxDD", "FULL_Sharpe", "FULL_MaxDD", "OOS_4a"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    sp = PK.iloc[0]
    P(f"  comparands: SPY OOS {sp.spy_OOS_CAGR:.2%} / {sp.spy_OOS_Sharpe:.4f} / "
      f"{sp.spy_MaxDD:.2%} (full-sample MaxDD)")
    for pname in panels:
        r = PK[PK.panel == pname].iloc[0]
        P(f"  RULES v2 (live) {pname:6s} full-sample Sharpe {r.v2_Sharpe:.4f}  "
          f"MaxDD {r.v2_MaxDD:.2%}")

    # ---------------------------------------------------------------- the census
    P()
    P("=" * 100)
    P("(D) THE CENSUS -- every (leg x ladder half x leg definition), all points reported")
    P("=" * 100)
    crows = []
    for ld in LEGDEFS:
        for hname, hcads in HALVES.items():
            sub = g10[g10.cadence.isin(hcads)]
            if not len(sub):
                continue
            passcol = sub[f"{ld}_pass4b"]
            base = max(float(passcol.mean()), float((~passcol).mean()))  # majority-class rate
            for leg in LEGS:
                lp = sub[f"{ld}_leg_{leg}"]
                fail = cbal(sub.assign(x=~lp), hcads, "x")
                fb = sub[~passcol]
                bind = cbal(fb.assign(x=~fb[f"{ld}_leg_{leg}"]), hcads, "x") if len(fb) else np.nan
                only = cbal(sub.assign(x=(sub[f"{ld}_nfail"] == 1) & (~lp)), hcads, "x")
                gg = sub.rename(columns={f"{ld}_leg_{k}": f"leg_{k}" for k in LEGS})
                mod = modal_share(gg, hcads, leg, ties=True)
                mods = modal_share(gg, hcads, leg, ties=False)
                agree = cbal(sub.assign(x=(lp == passcol)), hcads, "x")
                phi = cbal_mcc(sub, hcads, f"{ld}_leg_{leg}", f"{ld}_pass4b")
                crows.append(dict(legdef=ld, half=hname, leg=LEGNAME[leg], n=len(sub),
                                  fail=round(fail, 4), bind=round(bind, 4), only=round(only, 4),
                                  modal=round(mod, 4), modal_strict=round(mods, 4),
                                  AGREE=round(agree, 4), MCC=round(phi, 4),
                                  base_rate=round(base, 4), lift=round(agree - base, 4),
                                  pass4b_rate=round(float(cbal(sub.assign(x=passcol), hcads, "x")), 4)))
    CEN = pd.DataFrame(crows)
    dump(CEN, "census.csv")
    for ld in LEGDEFS:
        P()
        P(f"  --- leg definition {ld} ---")
        P(CEN[CEN.legdef == ld].drop(columns=["legdef", "n"])
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- hypotheses
    P()
    P("=" * 100)
    P("(E) THE PRE-REGISTERED HYPOTHESES")
    P("=" * 100)
    hyp = []

    def best(ld, half):
        s = CEN[(CEN.legdef == ld) & (CEN.half == half)]
        if not len(s):
            return None
        return s.loc[s.AGREE.idxmax()]

    b_fine = best("REC", "FINE2")
    b_coar = best("REC", "COARSE2")
    hyp.append(dict(H="H_FASTSINGLE", what="D/W: max AGREE over legs >= 0.90",
                    value=float(b_fine.AGREE), bar=BAR_SINGLE, verdict=
                    "PASS" if b_fine.AGREE >= BAR_SINGLE else "FAIL", detail=b_fine.leg))
    hyp.append(dict(H="H_FASTH1", what="D/W: the argmax-AGREE leg is L1_H1",
                    value=1.0 if b_fine.leg == "L1_H1" else 0.0, bar=1.0,
                    verdict="PASS" if b_fine.leg == "L1_H1" else "FAIL", detail=b_fine.leg))
    hyp.append(dict(H="H_SLOWSINGLE", what="M/Q: max AGREE over legs >= 0.90 (control)",
                    value=float(b_coar.AGREE), bar=BAR_SINGLE,
                    verdict="PASS" if b_coar.AGREE >= BAR_SINGLE else "FAIL", detail=b_coar.leg))
    hyp.append(dict(H="H_SLOWDD", what="M/Q: the argmax-AGREE leg is L4_DD (control)",
                    value=1.0 if b_coar.leg == "L4_DD" else 0.0, bar=1.0,
                    verdict="PASS" if b_coar.leg == "L4_DD" else "FAIL", detail=b_coar.leg))
    o = float(CEN[(CEN.legdef == "REC") & (CEN.half == "FINE2") & (CEN.leg == "L1_H1")].only.iloc[0])
    hyp.append(dict(H="H_ONLYFAST", what="D/W: L1_H1 only-failed-leg share >= 0.20",
                    value=o, bar=BAR_ONLY, verdict="PASS" if o >= BAR_ONLY else "FAIL",
                    detail=f"L4_DD at M/Q = "
                           f"{float(CEN[(CEN.legdef=='REC')&(CEN.half=='COARSE2')&(CEN.leg=='L4_DD')].only.iloc[0]):.4f}"))
    hyp.append(dict(H="H_LIFT", what="D/W: best leg's AGREE lift over the base rate >= 0.10",
                    value=float(b_fine.lift), bar=BAR_LIFT,
                    verdict="PASS" if b_fine.lift >= BAR_LIFT else "FAIL", detail=b_fine.leg))
    mf = CEN[(CEN.legdef == "REC") & (CEN.half == "FINE2")]
    mc = CEN[(CEN.legdef == "REC") & (CEN.half == "COARSE2")]
    mf_b = mf.loc[mf.MCC.idxmax()]
    mc_b = mc.loc[mc.MCC.idxmax()]
    hyp.append(dict(H="H_FASTMCC", what="D/W: best leg's MCC vs the 4b verdict >= 0.30",
                    value=float(mf_b.MCC), bar=BAR_MCC,
                    verdict="PASS" if mf_b.MCC >= BAR_MCC else "FAIL", detail=mf_b.leg))
    hyp.append(dict(H="H_SLOWMCC", what="M/Q: best leg's MCC vs the 4b verdict >= 0.30 (control)",
                    value=float(mc_b.MCC), bar=BAR_MCC,
                    verdict="PASS" if mc_b.MCC >= BAR_MCC else "FAIL", detail=mc_b.leg))
    HY = pd.DataFrame(hyp)
    P(HY.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(HY, "hypotheses.csv")

    # sensitivity of the two headline hypotheses across BOTH tuned axes, every point
    P()
    P("  SENSITIVITY -- the headline over every (ladder half x leg definition) point:")
    srows = []
    for ld in LEGDEFS:
        for hname in HALVES:
            b = best(ld, hname)
            if b is None:
                continue
            s = CEN[(CEN.legdef == ld) & (CEN.half == hname)]
            bm = s.loc[s.MCC.idxmax()]
            srows.append(dict(legdef=ld, half=hname, best_leg=b.leg, AGREE=b.AGREE,
                              base_rate=b.base_rate, lift=b.lift,
                              best_MCC_leg=bm.leg, best_MCC=bm.MCC,
                              H1_AGREE=float(CEN[(CEN.legdef == ld) & (CEN.half == hname) &
                                                 (CEN.leg == "L1_H1")].AGREE.iloc[0]),
                              DD_AGREE=float(CEN[(CEN.legdef == ld) & (CEN.half == hname) &
                                                 (CEN.leg == "L4_DD")].AGREE.iloc[0]),
                              single_leg_reading=bool(b.AGREE >= BAR_SINGLE)))
    SEN = pd.DataFrame(srows)
    P(SEN.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(SEN, "sensitivity.csv")

    # cost-rung sensitivity of the headline (all five rungs, reported not tuned)
    P()
    P("  COST RUNGS -- D/W best-leg AGREE and L1_H1 fail rate at every rung (REC legs):")
    rrows = []
    for cb in RUNGS:
        sub = G[(G.cost_bps == cb) & (G.cadence.isin(HALVES["FINE2"]))]
        pc = sub["REC_pass4b"]
        ag = {leg: cbal(sub.assign(x=(sub[f"REC_leg_{leg}"] == pc)), HALVES["FINE2"], "x")
              for leg in LEGS}
        bl = max(ag, key=lambda k: ag[k])
        sub2 = G[(G.cost_bps == cb) & (G.cadence.isin(HALVES["COARSE2"]))]
        pc2 = sub2["REC_pass4b"]
        ag2 = {leg: cbal(sub2.assign(x=(sub2[f"REC_leg_{leg}"] == pc2)), HALVES["COARSE2"], "x")
               for leg in LEGS}
        bl2 = max(ag2, key=lambda k: ag2[k])
        rrows.append(dict(cost_bps=cb, DW_best_leg=LEGNAME[bl], DW_AGREE=round(ag[bl], 4),
                          DW_H1_fail=round(cbal(sub.assign(x=~sub["REC_leg_H1"]),
                                                HALVES["FINE2"], "x"), 4),
                          DW_DD_fail=round(cbal(sub.assign(x=~sub["REC_leg_DD"]),
                                                HALVES["FINE2"], "x"), 4),
                          MQ_best_leg=LEGNAME[bl2], MQ_AGREE=round(ag2[bl2], 4),
                          MQ_DD_fail=round(cbal(sub2.assign(x=~sub2["REC_leg_DD"]),
                                                HALVES["COARSE2"], "x"), 4)))
    RR = pd.DataFrame(rrows)
    P(RR.to_string(index=False))
    dump(RR, "costrungs.csv")

    # ---------------------------------------------------------------- verdict
    P()
    P("=" * 100)
    P("(F) VERDICT")
    P("=" * 100)
    npass = int((HY.verdict == "PASS").sum())
    P(f"  {npass} of {len(HY)} pre-registered hypotheses PASS")
    P(f"  D/W best single-leg reading : {b_fine.leg} AGREE {b_fine.AGREE:.4f} "
      f"(base rate {b_fine.base_rate:.4f}, lift {b_fine.lift:+.4f}); "
      f"best MCC {mf_b.leg} {mf_b.MCC:.4f}")
    P(f"  M/Q best single-leg reading : {b_coar.leg} AGREE {b_coar.AGREE:.4f} "
      f"(base rate {b_coar.base_rate:.4f}, lift {b_coar.lift:+.4f}); "
      f"best MCC {mc_b.leg} {mc_b.MCC:.4f}")
    P(f"  rule 8: OOS 4b {int(PK.OOS_4b.sum())}/{len(PK)}, OOS 4a {int(PK.OOS_4a.sum())}/{len(PK)}")
    P(f"  full-sample 10 bps grid: 4b {int(g10[g10.phase==0]['REC_pass4b'].sum())} of "
      f"{len(g10[g10.phase==0])} phase-0 books, 4a {int(g10[g10.phase==0]['pass4a'].sum())}")
    P(f"  [{time.time()-t0:.0f}s]")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"wrote {STEM}.console.txt")


if __name__ == "__main__":
    main()

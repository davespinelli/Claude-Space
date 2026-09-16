#!/usr/bin/env python3
"""
Idea 995 (cloud lane, 2026-09-16)
IS REFUSAL COST A CADENCE OBJECT THE WAY `L4_DD` IS?

  Idea 993 paid for the refusals of idea 980's `S_IS4B` within-family phase-share screen and
  found the price of a refusal is 0 on one half of the ladder and TOTAL on the other:
  `ctrl_4b_in_emptied` reads 0 at EVERY floor on the M/Q grid half and 4 (all four of the
  control's OOS 4b passes) from floor 0.25 up on the D/W half.  993 published that as a
  two-bucket fact because its grid halves were M/Q (980's headline) and D/W (the extension).

  Idea 981 established the record's one clean CADENCE object: `L4_DD`'s fail rate runs
  D 0.633 / W 0.647 / M 0.832 / Q 0.927, a monotone gradient that is ALREADY THERE AT ZERO
  COST (0.567 / 0.647 / 0.829 / 0.924), i.e. drift between resets, not the turnover rebate,
  and one the PANEL does not explain (eta^2 0.038 on DD against 0.46-0.74 on the other legs).

  THIS RUN RESOLVES REFUSAL COST TO THE FOUR RUNGS AND ASKS WHETHER IT IS THE SAME OBJECT.
  Three declared refusal-cost statistics, each measured per cadence with the FALLBACK NAMED:

      RC_CONV(cad, fb, floor)  = med OOS Sharpe under FB_NONE  -  med OOS Sharpe under fb
                                 the ACCOUNTING gap: how much of the unpaid median is the
                                 free-refusal convention (993's H_CONVENTION, per cadence)
      RC_PAIR(cad, fb, floor)  = mean over EMPTIED slots of (fallback - unscreened control
                                 pick) OOS Sharpe.  Negative = refusing was expensive.  This
                                 is the only statistic that asks declining and picking the
                                 SAME question about the SAME slot.
      RC_4B(cad, floor)        = `ctrl_4b_in_emptied`: how many of the control's OOS 4b
                                 passes the screen destroys.  993's 0-vs-4, resolved.

TUNED AXES -- exactly two, every level reported, none selected:
  (1) fallback : FB_NONE (the incumbent free-refusal convention), FB_CASH, FB_SPY, FB_LIVE
  (2) floor    : 0.00 (= unscreened control), 0.10, 0.25, 0.40, 0.50, 0.75, 0.90
CADENCE IS NOT A TUNED AXIS.  It is the MEASURED axis: all four rungs D/W/M/Q are reported at
every point and nothing is ever selected on it.  The share BASIS is FIXED at `S_IS4B` (980's
legal IS-only basis, 993's headline); `S_ISLEG4` and the LEAKY `S_FULL4B` appear in an
appendix with no selection made on them.

PRE-REGISTERED HYPOTHESES (bars fixed before any number was read):
  H_CAD     : refusal cost is a CADENCE object -- the D/W/M/Q range of RC_PAIR at the
              headline floor exceeds the PANEL range of the same statistic, under all three
              paying fallbacks.  (981's form: H_CAD PASS / H_PANEL FAIL.)
  H_PANEL   : the mirror -- the panel range exceeds the cadence range.  Both are reported;
              they are not exclusive, and both can fail.
  H_MONO    : the gradient runs the SAME WAY as `L4_DD`'s, i.e. refusal cost RISES
              monotonically from D to Q (Spearman rho vs cadence rank >= +0.8 on the 4 rungs).
              A gradient with the OPPOSITE sign is a KILL for "the same object", not a pass.
  H_TRACK   : per-cell tracking -- Spearman rho between RC_PAIR and `L4_DD` fail rate over
              the 12 (panel x cadence) cells is >= +0.5.  This is the title's literal test.
  H_ZERO    : the DRIFT-CHANNEL diagnostic 981 used.  The cadence gradient in refusal cost
              survives at the 0 bps rung with >= 0.75 of its 10 bps magnitude.  FAIL means
              refusal cost is a TURNOVER object, not a drift object, and cannot be 981's.
  H_4B_FAST : RC_4B is concentrated at the FAST end -- the per-cadence split of 993's 0-vs-4
              puts strictly more destroyed 4b passes in {D, W} than in {M, Q}.
  H_RATE    : refusal cost is not merely refusal RATE.  Against a RATE-MATCHED random-screen
              null (a null that refuses the SAME number of slots in the SAME cell and pays
              the SAME fallback), the real screen's RC_PAIR sits outside the central 90% of
              2,000 draws in at least one cadence.  FAIL means the cadence gradient is a
              gradient in HOW OFTEN the screen refuses, not in what a refusal costs.
  H_4B      : >= 1 OOS 4b at some (fallback, floor, cadence) point once refusals are paid.
  H_4A      : >= 1 OOS 4a at any point.  (993: 0 of 28.)

GATES (printed before any hypothesis number):
  G0  offset_mask(idx, per, 0) == engine.rebalance_mask(idx, per) on D/W/M/Q
  G1  the fast Ctx runner == engine.backtest on returns AND turnover, post warm-up, D and M
  G2  BAND03 @ 0.75 == baseline.rules_v2_weights elementwise
  G2b FB_LIVE IS the live book: its series == the ladder's (panel, BAND03, CORE, W, phase 0,
      10 bps) row on every reported metric
  G3a CROSS-RUN: idea 993's committed 13,500-row ladder reproduced on every shared numeric col
  G3b CROSS-RUN: this run's PER-CADENCE decline table aggregates EXACTLY to 993's committed
      MQ18 / DW18 `decline.csv` rows (n_emptied, mean_dSharpe, ctrl_4b_in_emptied) -- the
      resolution is a split of 993's number, not a different number
  G3c CROSS-RUN: 981's published `L4_DD` fail rates 0.633 / 0.647 / 0.832 / 0.927 recomputed
      from this run's own ladder (the comparand of H_TRACK is not taken on trust)
  G4  MATCHED GROSS: one target matrix per (panel, book, gross), reused across all cadences
  G5  determinism: one cell rebuilt from scratch
  G6  ACCOUNTING IDENTITY: at floor 0.00 no slot is declined, so all four fallback conventions
      give IDENTICAL numbers in EVERY cadence.  Proves the fallback touches only emptied slots.
  G7  IS-PURITY: the screen and every pick are invariant under permuted OOS columns

PROTOCOL: 10 bps primary (all five rungs built; the 0 bps rung is read only for H_ZERO, which
is a declared diagnostic, not a selection), decided at close t / applied t+1 (LAG 1), warm-up
260 days, IS 2009-2016 / OOS 2017-2026 read once, no shorting, no leverage beyond the
published gross.  Rule 8 walk-forward IS the experiment -- every (book, gross) is chosen on
2009-2016 alone -- and both KEEP paths (4a and 4b) are evaluated at every grid point.  Nothing
in RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py is modified.

SURVIVORSHIP (rule 9): U56, B136 and SMALL are CURRENT-CONSTITUENT lists (SMALL additionally
drops every ticker with max_1d_move >= 1.0 per data/small_meta.csv), so every CAGR and
drawdown LEVEL here is optimistic and every 4b count -- screened, unscreened and fallback
alike -- is an UPPER bound.  The measured object is a DIFFERENCE between accounting
conventions applied to the SAME picks on the SAME tape, resolved by cadence, and is very
nearly immune; the SPY and CASH fallbacks carry no survivorship inflation at all.

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
ZERO_COST = 0.0
RUNGS = [0.0, 5.0, 10.0, 25.0, 50.0]
GROSSES = {"CORE": 0.75, "EXT": 1.00}
CADENCES = {"D": 1, "W": 5, "M": 21, "Q": 63}
CADORDER = ["D", "W", "M", "Q"]
CADRANK = {c: i for i, c in enumerate(CADORDER)}

LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
LEGNAME = {"H1": "L1_H1", "H2": "L2_H2", "OOS": "L3_OOS", "DD": "L4_DD", "CAGR": "L5_CAGR"}

FLOORS = [0.00, 0.10, 0.25, 0.40, 0.50, 0.75, 0.90]
BASES = ["S_IS4B", "S_ISLEG4", "S_FULL4B"]
LEGAL = {"S_IS4B": True, "S_ISLEG4": True, "S_FULL4B": False}
HEAD_BASIS = "S_IS4B"
ISLEG_BAR = 4
FALLBACKS = ["FB_NONE", "FB_CASH", "FB_SPY", "FB_LIVE"]
PAID_FB = ["FB_CASH", "FB_SPY", "FB_LIVE"]
HEAD_FLOOR = 0.40                    # 980's own published best legal floor, inherited; NOT chosen here
CHOOSERS = ["C_CAGR", "C_SHARPE", "C_ISLEGS"]

NULL_DRAWS = 2000
NULL_SEED = 995
BAR_MONO = 0.80                      # H_MONO: Spearman rho vs cadence rank
BAR_TRACK = 0.50                     # H_TRACK: Spearman rho over the 12 cells
BAR_ZERO = 0.75                      # H_ZERO: fraction of the 10 bps gradient retained at 0 bps
BAR_NULL = 0.90                      # H_RATE: outside the central 90% of the rate-matched null

# idea 981's published L4_DD fail rates (G3c comparand; recomputed, not trusted)
L4DD_981 = {"D": 0.633, "W": 0.647, "M": 0.832, "Q": 0.927}
L4DD_981_TOL = 0.002

# idea 993's committed artifacts (G3a / G3b)
PARENT_LADDER = OUT / "2026-09-16_price-the-EMPTIED-SLOT-COST_C.ladder.csv"
PARENT_DECLINE = OUT / "2026-09-16_price-the-EMPTIED-SLOT-COST_C.decline.csv"
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


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3:
        return np.nan
    ra = pd.Series(a[ok]).rank().values
    rb = pd.Series(b[ok]).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


# =========================================================================================
# (1) cadence / phase machinery -- the record's form
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
# (2) the book set -- verbatim from 942/962/964/976/981/984/986/980/993
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
# (3) main
# =========================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 995 (cloud lane, 2026-09-16) -- IS REFUSAL COST A CADENCE OBJECT THE WAY L4_DD IS?")
    P("=" * 100)
    P(f"  SMOKE={SMOKE}  headline cost {HEAD_COST:.0f} bps (rungs {RUNGS})  LAG={LAG}  WARM={WARM}")
    P(f"  tuned axes: fallback {FALLBACKS} x floor {FLOORS} -- ALL reported, none selected")
    P(f"  MEASURED axis (not tuned): cadence {CADORDER}, all four rungs reported everywhere")
    P(f"  share basis FIXED at {HEAD_BASIS}; {BASES[1:]} appendix only")
    P(f"  comparand: idea 981's L4_DD cadence gradient {L4DD_981} (recomputed at G3c)")
    P("  DECLARED: cash Sharpe := 0.0, cash MaxDD := 0.0; cash and SPY costless; live book "
      "pays 10 bps")

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
    rows, det_store, FB = [], {}, {}
    cads = CADORDER if not SMOKE else CADORDER
    for pname, px in panels.items():
        rspy = px["SPY"].pct_change().fillna(0.0).values
        isw = np.asarray(px.index <= pd.Timestamp(IS_END))
        osw = np.asarray(px.index >= pd.Timestamp(OOS_START))
        spy_full, spy_is, spy_oos = (mets(rspy[WARM:]), mets(rspy[WARM:][isw[WARM:]]),
                                     mets(rspy[osw]))
        v2_net = backtest(px, rules_v2_weights(px), cost_bps=HEAD_COST, freq="W")["returns"].values
        v2 = mets(v2_net[WARM:])

        def fb_row(net, tag):
            f, i_, o_ = (mets(net[WARM:]), mets(net[WARM:][isw[WARM:]]), mets(net[osw]))
            row = dict(panel=pname, fallback=tag)
            for k, v in f.items():
                row[k] = v
            for k, v in i_.items():
                row["IS_" + k] = v
            for k, v in o_.items():
                row["OOS_" + k] = v
            for k, v in spy_full.items():
                row["spy_" + k] = v
            for k, v in spy_oos.items():
                row["spy_OOS_" + k] = v
            for k, v in v2.items():
                row["v2_" + k] = v
            if tag == "FB_CASH":
                for k in ("Sharpe", "H1", "H2", "IS_Sharpe", "IS_H1", "IS_H2", "OOS_Sharpe",
                          "OOS_H1", "OOS_H2", "CAGR", "IS_CAGR", "OOS_CAGR", "MaxDD",
                          "IS_MaxDD", "OOS_MaxDD"):
                    row[k] = 0.0
            lg = legs_REC(row)
            row["OOS_4b"] = bool(all(lg.values()))
            row["OOS_4a"] = pass4a(row)
            row["fail_legs"] = ",".join(LEGNAME[k] for k in LEGS if not lg[k]) or "-"
            row["FULL_CAGR"], row["FULL_Sharpe"], row["FULL_MaxDD"] = \
                row["CAGR"], row["Sharpe"], row["MaxDD"]
            return row

        FB[(pname, "FB_CASH")] = fb_row(np.zeros(len(px)), "FB_CASH")
        FB[(pname, "FB_SPY")] = fb_row(rspy, "FB_SPY")
        FB[(pname, "FB_LIVE")] = fb_row(v2_net, "FB_LIVE")

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

    FBT = pd.DataFrame([FB[k] for k in FB])
    g10 = G[G.cost_bps == HEAD_COST]
    g00 = G[G.cost_bps == ZERO_COST]

    g2b = 0.0
    for pname in panels:
        lw = g10[(g10.panel == pname) & (g10.book == "BAND03") & (g10.gross == "CORE")
                 & (g10.cadence == "W") & (g10.phase == 0)]
        if not len(lw):
            g2b = np.nan
            continue
        lw = lw.iloc[0]
        fbl = FB[(pname, "FB_LIVE")]
        for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"):
            g2b = max(g2b, abs(float(lw[k]) - float(fbl[k])))
    gates.append(dict(gate="G2b", what="FB_LIVE == the ladder's (BAND03, CORE, W, phase 0) row",
                      value=g2b, bar=1e-12, ok=(g2b == g2b and g2b < 1e-12)))
    P(f"  G2b FB_LIVE vs the ladder's live-book row : max|d| {g2b:.3e}")

    # ---------------------------------------------------------------- G3a cross-run
    g3a, g3note = np.inf, "parent ladder not found"
    if PARENT_LADDER.exists():
        PA = pd.read_csv(PARENT_LADDER)
        key = ["panel", "book", "gross", "cadence", "phase", "cost_bps"]
        num = [c for c in PA.columns if c in G.columns
               and pd.api.types.is_numeric_dtype(PA[c]) and c not in key]
        a = PA.set_index(key).sort_index()
        b = G.set_index(key).sort_index()
        common = a.index.intersection(b.index)
        g3a = float(np.nanmax(np.abs(a.loc[common, num].values - b.loc[common, num].values)))
        g3note = f"{len(common):,} shared phase-book-rungs x {len(num)} numeric cols"
    gates.append(dict(gate="G3a", what=f"CROSS-RUN: idea 993's committed ladder ({g3note})",
                      value=g3a, bar=G3_TOL, ok=g3a <= G3_TOL))
    P(f"  G3a cross-run vs idea 993's ladder : max|d| {g3a:.3e}  ({g3note})")

    # ---------------------------------------------------------------- G3c: 981's L4_DD gradient
    P()
    P("  --- the COMPARAND: L4_DD fail rate by cadence, recomputed from this run's ladder ---")
    l4 = g10.groupby("cadence")["leg_DD"].apply(lambda s: float(1.0 - s.mean()))
    l4z = g00.groupby("cadence")["leg_DD"].apply(lambda s: float(1.0 - s.mean()))
    P("    cadence   L4_DD fail @10bps   @0bps   idea 981 published")
    g3c = 0.0
    for c in CADORDER:
        g3c = max(g3c, abs(float(l4[c]) - L4DD_981[c]))
        P(f"    {c:7s}   {l4[c]:17.4f}   {l4z[c]:5.4f}   {L4DD_981[c]:.3f}")
    gates.append(dict(gate="G3c", what="CROSS-RUN: 981's published L4_DD fail rates D/W/M/Q",
                      value=g3c, bar=L4DD_981_TOL, ok=g3c <= L4DD_981_TOL))
    P(f"  G3c cross-run vs 981's L4_DD gradient : max|d| {g3c:.4f}")
    L4CELL = g10.groupby(["panel", "cadence"])["leg_DD"].apply(
        lambda s: float(1.0 - s.mean())).to_dict()

    # ---------------------------------------------------------------- the screen
    P()
    P("=" * 100)
    P("(C) THE SCREEN AND ITS REFUSALS, RESOLVED BY CADENCE -- (book, gross) chosen on 2009-2016")
    P("=" * 100)

    def build_shares(gx):
        fam = gx.groupby(["panel", "book", "gross", "cadence"])
        SH = fam.agg(n_phase=("phase", "size"), S_IS4B=("IS_pass4b", "mean"),
                     S_FULL4B=("pass4b", "mean")).reset_index()
        SH["S_ISLEG4"] = fam["IS_legs_passed"].apply(
            lambda s: float((s >= ISLEG_BAR).mean())).values
        return SH

    SH = build_shares(g10)
    dump(SH, "shares.csv")
    shmap = {(r.panel, r.book, r.gross, r.cadence): r for r in SH.itertuples()}
    SH0 = build_shares(g00)
    shmap0 = {(r.panel, r.book, r.gross, r.cadence): r for r in SH0.itertuples()}

    def run_picks(floor, basis, gx, smap, permute_seed=None):
        out = []
        rng = np.random.default_rng(permute_seed) if permute_seed is not None else None
        for pname in panels:
            for cad in cads:
                sub0 = gx[(gx.panel == pname) & (gx.cadence == cad) & (gx.phase == 0)] \
                    .reset_index(drop=True)
                if rng is not None:
                    oc = [c for c in sub0.columns if c.startswith("OOS_")]
                    sub0 = sub0.copy()
                    sub0[oc] = sub0[oc].values[rng.permutation(len(sub0))]
                sh = np.array([getattr(smap[(pname, r.book, r.gross, cad)], basis)
                               for r in sub0.itertuples()])
                cand = sub0[sh >= floor - 1e-12].reset_index(drop=True)
                for ch in CHOOSERS:
                    i = choose(ch, cand) if len(cand) else None
                    if i is None:
                        out.append(dict(panel=pname, cadence=cad, chooser=ch, floor=floor,
                                        basis=basis, book="", gross="", share=np.nan,
                                        n_cand=len(cand), declined=True))
                        continue
                    r = cand.iloc[i]
                    out.append(dict(
                        panel=pname, cadence=cad, chooser=ch, floor=floor, basis=basis,
                        book=r.book, gross=r.gross,
                        share=float(getattr(smap[(pname, r.book, r.gross, cad)], basis)),
                        n_cand=len(cand), declined=False,
                        OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                        FULL_CAGR=r.CAGR, FULL_Sharpe=r.Sharpe, FULL_MaxDD=r.MaxDD,
                        H1=r.H1, H2=r.H2,
                        spy_OOS_CAGR=r.spy_OOS_CAGR, spy_OOS_Sharpe=r.spy_OOS_Sharpe,
                        spy_OOS_MaxDD=r.spy_OOS_MaxDD, spy_CAGR=r.spy_CAGR,
                        spy_Sharpe=r.spy_Sharpe, spy_MaxDD=r.spy_MaxDD, spy_H1=r.spy_H1,
                        spy_H2=r.spy_H2, v2_Sharpe=r.v2_Sharpe, v2_MaxDD=r.v2_MaxDD,
                        v2_H1=r.v2_H1, v2_H2=r.v2_H2, v2_CAGR=r.v2_CAGR,
                        OOS_4b=bool(r.pass4b), OOS_4a=bool(r.pass4a), fail_legs=r.fail_legs))
        return pd.DataFrame(out)

    ALL = pd.concat([run_picks(f, b, g10, shmap) for b in BASES for f in FLOORS],
                    ignore_index=True)
    dump(ALL, "picks.csv")
    ALL0 = pd.concat([run_picks(f, HEAD_BASIS, g00, shmap0) for f in FLOORS], ignore_index=True)

    # ---- G7 IS-purity -------------------------------------------------------------------
    dis = 0
    for f in (0.25, 0.50):
        a = run_picks(f, HEAD_BASIS, g10, shmap)
        c = run_picks(f, HEAD_BASIS, g10, shmap, permute_seed=7)
        mm = a.merge(c, on=["panel", "cadence", "chooser"], suffixes=("_a", "_c"))
        dis += int((mm.book_a.fillna("").astype(str) != mm.book_c.fillna("").astype(str)).sum())
    gates.append(dict(gate="G7", what="IS-PURITY: screen and picks invariant under permuted OOS",
                      value=float(dis), bar=0.0, ok=dis == 0))
    P(f"  G7  IS-purity : {dis} pick disagreements under permuted OOS columns")

    # ---- refusal RATE per cadence --------------------------------------------------------
    P()
    P("  --- REFUSAL RATE by cadence (S_IS4B, 9 slots per cadence = 3 panels x 3 choosers) ---")
    hb = ALL[ALL.basis == HEAD_BASIS]
    RATE = hb.pivot_table(index="floor", columns="cadence", values="declined",
                          aggfunc="sum").reindex(columns=CADORDER).astype(int)
    P(RATE.to_string())
    dump(RATE.reset_index(), "refusal_rate.csv")

    # =====================================================================================
    # (D) THE THREE REFUSAL-COST STATISTICS, RESOLVED BY CADENCE
    # =====================================================================================
    P()
    P("=" * 100)
    P("(D) THE FALLBACK OBJECTS -- what a declined slot actually holds, 2017-2026")
    P("=" * 100)
    show = ["panel", "fallback", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "FULL_Sharpe",
            "FULL_MaxDD", "OOS_4b", "OOS_4a", "fail_legs"]
    P(FBT[show].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(FBT, "fallbacks.csv")

    MET = ["OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "FULL_Sharpe", "FULL_MaxDD"]

    def paid_frame(src, floor, fb, cadset, basis=HEAD_BASIS):
        s = src[(src.basis == basis) & (src.floor == floor)
                & src.cadence.isin(cadset)].reset_index(drop=True)
        recs = []
        for r in s.itertuples():
            if not r.declined:
                d = {m: getattr(r, m) for m in MET}
                d.update(OOS_4b=bool(r.OOS_4b), OOS_4a=bool(r.OOS_4a), src="PICK",
                         book=r.book, gross=r.gross)
            elif fb == "FB_NONE":
                continue
            else:
                f_ = FB[(r.panel, fb)]
                d = {m: f_[m] for m in MET}
                d.update(OOS_4b=bool(f_["OOS_4b"]), OOS_4a=bool(f_["OOS_4a"]), src=fb,
                         book=fb, gross="-")
            d.update(panel=r.panel, cadence=r.cadence, chooser=r.chooser,
                     declined=bool(r.declined))
            recs.append(d)
        return pd.DataFrame(recs)

    P()
    P("=" * 100)
    P("(E) THE PAID SUMMARY -- every (cadence x fallback x floor), ALL 9 SLOTS PER CADENCE")
    P("=" * 100)
    prows = []
    for cad in CADORDER:
        for fb in FALLBACKS:
            for f in FLOORS:
                d = paid_frame(ALL, f, fb, [cad])
                sl = ALL[(ALL.basis == HEAD_BASIS) & (ALL.floor == f) & (ALL.cadence == cad)]
                prows.append(dict(
                    cadence=cad, fallback=fb, floor=f, n_slots=len(sl),
                    n_declined=int(sl.declined.sum()), n_scored=len(d),
                    OOS_4b=int(d.OOS_4b.sum()) if len(d) else 0,
                    OOS_4a=int(d.OOS_4a.sum()) if len(d) else 0,
                    med_OOS_Sharpe=round(float(d.OOS_Sharpe.median()), 4) if len(d) else np.nan,
                    mean_OOS_Sharpe=round(float(d.OOS_Sharpe.mean()), 4) if len(d) else np.nan,
                    med_OOS_CAGR=round(float(d.OOS_CAGR.median()), 4) if len(d) else np.nan,
                    med_OOS_MaxDD=round(float(d.OOS_MaxDD.median()), 4) if len(d) else np.nan,
                    med_FULL_Sharpe=round(float(d.FULL_Sharpe.median()), 4) if len(d) else np.nan,
                    med_FULL_MaxDD=round(float(d.FULL_MaxDD.median()), 4) if len(d) else np.nan))
    PAID = pd.DataFrame(prows)
    dump(PAID, "paid_by_cadence.csv")
    for cad in CADORDER:
        P()
        P(f"  --- cadence {cad} ---")
        P(PAID[PAID.cadence == cad].drop(columns=["cadence"]).to_string(index=False))

    # ---- G6 accounting identity, in EVERY cadence ---------------------------------------
    cols = ["n_scored", "OOS_4b", "OOS_4a", "med_OOS_Sharpe", "med_OOS_CAGR", "med_OOS_MaxDD"]
    g6 = 0.0
    for cad in CADORDER:
        z = PAID[(PAID.cadence == cad) & (PAID.floor == 0.0)]
        g6 = max(g6, float(np.nanmax(np.abs(z[cols].values - z[cols].values[0]))))
    gates.append(dict(gate="G6", what="ACCOUNTING IDENTITY: 4 fallbacks identical at floor 0 in "
                                      "EVERY cadence", value=g6, bar=0.0, ok=g6 == 0.0))
    P()
    P(f"  G6  accounting identity at floor 0.00, all four cadences : max|d| {g6:.3e}")

    # ---- RC_CONV -------------------------------------------------------------------------
    P()
    P("=" * 100)
    P("(F) RC_CONV -- the ACCOUNTING gap, per cadence:  med OOS Sharpe(FB_NONE) - med(fb)")
    P("    positive = the free-refusal convention FLATTERS the screen by that much")
    P("=" * 100)
    crows = []
    for cad in CADORDER:
        for fb in PAID_FB:
            for f in FLOORS:
                a = PAID[(PAID.cadence == cad) & (PAID.fallback == "FB_NONE")
                         & (PAID.floor == f)]
                b = PAID[(PAID.cadence == cad) & (PAID.fallback == fb) & (PAID.floor == f)]
                crows.append(dict(
                    cadence=cad, fallback=fb, floor=f,
                    n_declined=int(b.n_declined.iloc[0]),
                    RC_CONV_med=round(float(a.med_OOS_Sharpe.iloc[0]
                                            - b.med_OOS_Sharpe.iloc[0]), 4),
                    RC_CONV_mean=round(float(a.mean_OOS_Sharpe.iloc[0]
                                             - b.mean_OOS_Sharpe.iloc[0]), 4),
                    RC_CONV_dd=round(float(a.med_OOS_MaxDD.iloc[0]
                                           - b.med_OOS_MaxDD.iloc[0]), 4)))
    CONV = pd.DataFrame(crows)
    dump(CONV, "rc_conv.csv")
    P(CONV.pivot_table(index=["fallback", "floor"], columns="cadence", values="RC_CONV_med")
      .reindex(columns=CADORDER).to_string(float_format=lambda x: f"{x:.4f}"))

    # ---- RC_PAIR + RC_4B -----------------------------------------------------------------
    P()
    P("=" * 100)
    P("(G) RC_PAIR / RC_4B -- the PAIRED test on EMPTIED slots only, resolved by cadence")
    P("    dSharpe = fallback - the UNSCREENED control's pick in the SAME slot.")
    P("    NEGATIVE = refusing was EXPENSIVE.  RC_4B = control OOS 4b passes destroyed.")
    P("=" * 100)

    def decline_table(src, gx_label):
        ctrl = {(r.panel, r.cadence, r.chooser): r
                for r in src[(src.basis == HEAD_BASIS) & (src.floor == 0.0)].itertuples()}
        out = []
        for cad in CADORDER:
            for fb in PAID_FB:
                for f in FLOORS[1:]:
                    s = src[(src.basis == HEAD_BASIS) & (src.floor == f)
                            & (src.cadence == cad) & src.declined]
                    if not len(s):
                        out.append(dict(rung=gx_label, cadence=cad, fallback=fb, floor=f,
                                        n_emptied=0, mean_dSharpe=np.nan, med_dSharpe=np.nan,
                                        win_Sharpe=np.nan, mean_dMaxDD=np.nan,
                                        win_MaxDD=np.nan, mean_dCAGR=np.nan,
                                        ctrl_4b_in_emptied=0))
                        continue
                    dS, dD, dC, c4b = [], [], [], 0
                    for r in s.itertuples():
                        c = ctrl[(r.panel, r.cadence, r.chooser)]
                        fo = FB[(r.panel, fb)]
                        dS.append(fo["OOS_Sharpe"] - c.OOS_Sharpe)
                        dD.append(fo["OOS_MaxDD"] - c.OOS_MaxDD)
                        dC.append(fo["OOS_CAGR"] - c.OOS_CAGR)
                        c4b += int(bool(c.OOS_4b))
                    dS, dD, dC = np.array(dS), np.array(dD), np.array(dC)
                    out.append(dict(
                        rung=gx_label, cadence=cad, fallback=fb, floor=f, n_emptied=len(dS),
                        mean_dSharpe=round(float(dS.mean()), 4),
                        med_dSharpe=round(float(np.median(dS)), 4),
                        win_Sharpe=round(float((dS > 0).mean()), 4),
                        mean_dMaxDD=round(float(dD.mean()), 4),
                        win_MaxDD=round(float((dD > 0).mean()), 4),
                        mean_dCAGR=round(float(dC.mean()), 4),
                        ctrl_4b_in_emptied=c4b))
        return pd.DataFrame(out)

    DEC = decline_table(ALL, "10bps")
    DEC0 = decline_table(ALL0, "0bps")
    dump(pd.concat([DEC, DEC0], ignore_index=True), "decline_by_cadence.csv")
    for cad in CADORDER:
        P()
        P(f"  --- cadence {cad} (10 bps) ---")
        P(DEC[DEC.cadence == cad].drop(columns=["rung", "cadence"]).to_string(index=False))

    P()
    P("  --- RC_4B: control OOS 4b passes DESTROYED, by cadence x floor ---")
    R4 = DEC[DEC.fallback == "FB_LIVE"].pivot_table(index="floor", columns="cadence",
                                                    values="ctrl_4b_in_emptied",
                                                    aggfunc="max").reindex(columns=CADORDER)
    P(R4.to_string())
    ctrl4b = {cad: int(ALL[(ALL.basis == HEAD_BASIS) & (ALL.floor == 0.0)
                           & (ALL.cadence == cad)].OOS_4b.sum()) for cad in CADORDER}
    P(f"  control (floor 0.00) OOS 4b passes available to destroy, by cadence: {ctrl4b}")

    # ---------------------------------------------------------------- G3b cross-run
    g3b, g3bn = np.inf, "parent decline table not found"
    if PARENT_DECLINE.exists():
        PD_ = pd.read_csv(PARENT_DECLINE)
        agg = []
        for lab, cadset in (("MQ18", ["M", "Q"]), ("DW18", ["D", "W"])):
            sub = DEC[DEC.cadence.isin(cadset)]
            for fb in PAID_FB:
                for f in FLOORS[1:]:
                    s = sub[(sub.fallback == fb) & (sub.floor == f)]
                    n = int(s.n_emptied.sum())
                    # mean over the union of emptied slots = n-weighted mean of the parts
                    mw = (float((s.mean_dSharpe.fillna(0) * s.n_emptied).sum() / n)
                          if n else np.nan)
                    agg.append(dict(grid=lab, fallback=fb, floor=f, n_emptied=n,
                                    mean_dSharpe=mw,
                                    ctrl_4b_in_emptied=int(s.ctrl_4b_in_emptied.sum())))
        AG = pd.DataFrame(agg)
        m = PD_.merge(AG, on=["grid", "fallback", "floor"], suffixes=("_p", "_c"))
        dn = float(np.abs(m.n_emptied_p - m.n_emptied_c).max())
        d4 = float(np.abs(m.ctrl_4b_in_emptied_p - m.ctrl_4b_in_emptied_c).max())
        ok = m.n_emptied_c > 0
        ds = float(np.nanmax(np.abs(m.loc[ok, "mean_dSharpe_p"]
                                    - m.loc[ok, "mean_dSharpe_c"]))) if ok.any() else 0.0
        g3b = max(dn, d4, ds)
        g3bn = (f"{len(m)} shared (grid x fallback x floor) rows; max|d n_emptied| {dn:.0f}, "
                f"max|d ctrl_4b| {d4:.0f}, max|d mean_dSharpe| {ds:.2e}")
    gates.append(dict(gate="G3b", what=f"CROSS-RUN: per-cadence table aggregates to 993's "
                                       f"MQ18/DW18 ({g3bn})",
                      value=g3b, bar=5e-4, ok=g3b <= 5e-4))
    P()
    P(f"  G3b cross-run vs 993's committed decline table : {g3bn}")

    # =====================================================================================
    # (H) HYPOTHESES
    # =====================================================================================
    GT = pd.DataFrame(gates)
    P()
    P(f"  GATES: {int(GT.ok.sum())} of {len(GT)} PASS")
    P(GT.to_string(index=False))
    dump(GT, "gates.csv")
    if not GT.ok.all():
        P("  !! a gate FAILED -- the affected results below are NOT to be read as evidence")

    P()
    P("=" * 100)
    P("(H) PRE-REGISTERED HYPOTHESES")
    P("=" * 100)
    H = []

    # ---- H_CAD / H_PANEL: cadence range vs panel range of RC_PAIR at the headline floor ---
    def pair_by(keys, floor, fb, src=ALL):
        ctrl = {(r.panel, r.cadence, r.chooser): r
                for r in src[(src.basis == HEAD_BASIS) & (src.floor == 0.0)].itertuples()}
        s = src[(src.basis == HEAD_BASIS) & (src.floor == floor) & src.declined]
        acc = {}
        for r in s.itertuples():
            k = tuple(getattr(r, kk) for kk in keys)
            c = ctrl[(r.panel, r.cadence, r.chooser)]
            acc.setdefault(k, []).append(FB[(r.panel, fb)]["OOS_Sharpe"] - c.OOS_Sharpe)
        return {k: float(np.mean(v)) for k, v in acc.items()}

    P()
    P(f"  --- RC_PAIR at the inherited headline floor {HEAD_FLOOR:.2f}, by CADENCE and by PANEL ---")
    cadrange, panrange = {}, {}
    for fb in PAID_FB:
        bc = pair_by(["cadence"], HEAD_FLOOR, fb)
        bp = pair_by(["panel"], HEAD_FLOOR, fb)
        cadrange[fb] = (max(bc.values()) - min(bc.values())) if len(bc) > 1 else np.nan
        panrange[fb] = (max(bp.values()) - min(bp.values())) if len(bp) > 1 else np.nan
        P(f"    {fb}: cadence " + " ".join(f"{c}={bc.get((c,), float('nan')):+.4f}"
                                           for c in CADORDER)
          + f"   range {cadrange[fb]:.4f}")
        P(f"    {fb}: panel   " + " ".join(f"{p}={bp.get((p,), float('nan')):+.4f}"
                                           for p in panels)
          + f"   range {panrange[fb]:.4f}")
    cad_wins = [fb for fb in PAID_FB
                if np.isfinite(cadrange[fb]) and np.isfinite(panrange[fb])
                and cadrange[fb] > panrange[fb]]
    H.append(dict(H="H_CAD", what="cadence range of RC_PAIR > panel range, ALL 3 fallbacks",
                  value=float(len(cad_wins)), bar=3.0, passed=len(cad_wins) == 3,
                  note=f"cadence wins under {cad_wins}"))
    H.append(dict(H="H_PANEL", what="panel range > cadence range, ALL 3 fallbacks",
                  value=float(3 - len(cad_wins)), bar=3.0, passed=len(cad_wins) == 0,
                  note="the mirror of H_CAD"))

    # ---- H_MONO: does RC_PAIR rise D->Q the way L4_DD does? -------------------------------
    P()
    P("  --- H_MONO: Spearman(RC_PAIR magnitude, cadence rank D<W<M<Q) at every floor ---")
    mono_rows = []
    for fb in PAID_FB:
        for f in FLOORS[1:]:
            bc = pair_by(["cadence"], f, fb)
            v = [bc.get((c,), np.nan) for c in CADORDER]
            rho = spearman([CADRANK[c] for c in CADORDER], v)
            rho_abs = spearman([CADRANK[c] for c in CADORDER],
                               [-x if np.isfinite(x) else np.nan for x in v])
            mono_rows.append(dict(fallback=fb, floor=f,
                                  **{f"RC_{c}": (round(bc.get((c,), np.nan), 4)
                                                 if np.isfinite(bc.get((c,), np.nan)) else np.nan)
                                     for c in CADORDER},
                                  rho_signed=round(rho, 4) if np.isfinite(rho) else np.nan,
                                  rho_cost=round(rho_abs, 4) if np.isfinite(rho_abs) else np.nan))
    MONO = pd.DataFrame(mono_rows)
    dump(MONO, "mono.csv")
    P(MONO.to_string(index=False))
    # "rises like L4_DD" == the COST (= -dSharpe) rises with cadence length
    at_head = MONO[MONO.floor == HEAD_FLOOR]
    mono_ok = bool((at_head.rho_cost >= BAR_MONO).all()) and len(at_head) == 3
    H.append(dict(H="H_MONO", what=f"RC cost rises monotonically D->Q (rho >= {BAR_MONO}) at the "
                                   f"headline floor, all 3 fallbacks",
                  value=float(at_head.rho_cost.min()) if len(at_head) else np.nan, bar=BAR_MONO,
                  passed=mono_ok,
                  note="rho_cost = Spearman(cadence rank, -mean dSharpe on emptied slots)"))

    # ---- H_TRACK: per-cell tracking against L4_DD -----------------------------------------
    P()
    P("  --- H_TRACK: RC_PAIR vs L4_DD fail rate over the 12 (panel x cadence) cells ---")
    trk = []
    for fb in PAID_FB:
        bc = pair_by(["panel", "cadence"], HEAD_FLOOR, fb)
        xs, ys, labs = [], [], []
        for (pn, cd), v in sorted(bc.items()):
            xs.append(L4CELL[(pn, cd)]); ys.append(-v); labs.append(f"{pn}/{cd}")
        rho = spearman(xs, ys)
        trk.append(dict(fallback=fb, n_cells=len(xs), rho=round(rho, 4)
                        if np.isfinite(rho) else np.nan,
                        cells=";".join(labs)))
        P(f"    {fb}: {len(xs)} non-empty cells, Spearman(L4_DD fail, RC cost) = "
          f"{rho:.4f}" if np.isfinite(rho) else f"    {fb}: rho undefined ({len(xs)} cells)")
    TRK = pd.DataFrame(trk)
    dump(TRK, "track.csv")
    trk_ok = bool(len(TRK) and np.isfinite(TRK.rho).all() and (TRK.rho >= BAR_TRACK).all())
    H.append(dict(H="H_TRACK", what=f"Spearman(L4_DD fail, RC cost) >= {BAR_TRACK} over the "
                                    f"(panel x cadence) cells, all 3 fallbacks",
                  value=float(TRK.rho.min()) if len(TRK) and np.isfinite(TRK.rho).any()
                  else np.nan, bar=BAR_TRACK, passed=trk_ok,
                  note="the title's literal test"))

    # ---- H_ZERO: drift channel ------------------------------------------------------------
    P()
    P("  --- H_ZERO: does the cadence gradient survive at 0 bps? (981's drift diagnostic) ---")
    z_rows = []
    for fb in PAID_FB:
        b10 = pair_by(["cadence"], HEAD_FLOOR, fb, ALL)
        b00 = pair_by(["cadence"], HEAD_FLOOR, fb, ALL0)
        r10 = ((max(b10.values()) - min(b10.values())) if len(b10) > 1 else np.nan)
        r00 = ((max(b00.values()) - min(b00.values())) if len(b00) > 1 else np.nan)
        z_rows.append(dict(fallback=fb, range_10bps=round(r10, 4) if np.isfinite(r10) else np.nan,
                           range_0bps=round(r00, 4) if np.isfinite(r00) else np.nan,
                           retained=round(r00 / r10, 4) if (np.isfinite(r10) and r10 > 0)
                           else np.nan,
                           **{f"RC0_{c}": (round(b00.get((c,), np.nan), 4)
                                           if np.isfinite(b00.get((c,), np.nan)) else np.nan)
                              for c in CADORDER}))
    ZC = pd.DataFrame(z_rows)
    dump(ZC, "zerocost.csv")
    P(ZC.to_string(index=False))
    zero_ok = bool(len(ZC) and np.isfinite(ZC.retained).all() and (ZC.retained >= BAR_ZERO).all())
    H.append(dict(H="H_ZERO", what=f"cadence gradient retains >= {BAR_ZERO} of its magnitude at "
                                   f"0 bps (drift, not turnover), all 3 fallbacks",
                  value=float(ZC.retained.min()) if len(ZC) and np.isfinite(ZC.retained).any()
                  else np.nan, bar=BAR_ZERO, passed=zero_ok, note="981's own diagnostic"))

    # ---- H_4B_FAST ------------------------------------------------------------------------
    fast = int(DEC[(DEC.fallback == "FB_LIVE") & DEC.cadence.isin(["D", "W"])]
               .groupby("floor").ctrl_4b_in_emptied.sum().max())
    slow = int(DEC[(DEC.fallback == "FB_LIVE") & DEC.cadence.isin(["M", "Q"])]
               .groupby("floor").ctrl_4b_in_emptied.sum().max())
    H.append(dict(H="H_4B_FAST", what="destroyed control 4b passes concentrate at the FAST end "
                                      "(max over floors: D+W > M+Q)",
                  value=float(fast - slow), bar=0.0, passed=fast > slow,
                  note=f"D+W max {fast}, M+Q max {slow}"))

    # ---- H_RATE: rate-matched random-screen null -------------------------------------------
    P()
    P("=" * 100)
    P(f"(I) RATE-MATCHED RANDOM-SCREEN NULL -- {NULL_DRAWS:,} draws, seed {NULL_SEED}")
    P("    the null refuses the SAME slots-count in the SAME cell and pays the SAME fallback,")
    P("    so it holds refusal RATE fixed and asks only what a refusal COSTS.")
    P("=" * 100)
    CELLS = {}
    for pname in panels:
        for cad in cads:
            s = g10[(g10.panel == pname) & (g10.cadence == cad) & (g10.phase == 0)] \
                .reset_index(drop=True)
            CELLS[(pname, cad)] = dict(panel=pname, IS_CAGR=s.IS_CAGR.values,
                                       IS_Sharpe=s.IS_Sharpe.values,
                                       IS_legs=s.IS_legs_passed.values.astype(float),
                                       oS=s.OOS_Sharpe.values, n=len(s))

    def _pick_idx(ch, idx, C):
        if len(idx) == 0:
            return None
        if ch == "C_CAGR":
            return int(idx[_argmax(C["IS_CAGR"][idx], C["IS_Sharpe"][idx])])
        if ch == "C_SHARPE":
            return int(idx[_argmax(C["IS_Sharpe"][idx], C["IS_CAGR"][idx])])
        return int(idx[_argmax(C["IS_legs"][idx], C["IS_Sharpe"][idx])])

    ctrl_map = {(r.panel, r.cadence, r.chooser): r
                for r in ALL[(ALL.basis == HEAD_BASIS) & (ALL.floor == 0.0)].itertuples()}
    nrows = []
    for fb in PAID_FB:
        for cad in CADORDER:
            emp = ALL[(ALL.basis == HEAD_BASIS) & (ALL.floor == HEAD_FLOOR)
                      & (ALL.cadence == cad) & ALL.declined]
            if not len(emp):
                nrows.append(dict(fallback=fb, cadence=cad, n_emptied=0, real=np.nan,
                                  null_mean=np.nan, pct=np.nan))
                continue
            # real statistic
            real = float(np.mean([FB[(r.panel, fb)]["OOS_Sharpe"]
                                  - ctrl_map[(r.panel, r.cadence, r.chooser)].OOS_Sharpe
                                  for r in emp.itertuples()]))
            # how many slots per (panel) are emptied in this cadence
            cnt = emp.groupby("panel").size().to_dict()
            rng = np.random.default_rng(NULL_SEED + CADRANK[cad] * 7 + PAID_FB.index(fb))
            draws = np.empty(NULL_DRAWS)
            for dd_ in range(NULL_DRAWS):
                acc = []
                for pn, k in cnt.items():
                    C = CELLS[(pn, cad)]
                    # a random screen admitting a random subset; the refused slots' control
                    # picks are the control's own picks -- the rate is held EXACTLY fixed
                    chs = list(rng.choice(CHOOSERS, size=k, replace=True))
                    for ch in chs:
                        sub = rng.choice(C["n"], size=max(1, C["n"] // 2), replace=False)
                        i = _pick_idx(ch, sub, C)
                        acc.append(FB[(pn, fb)]["OOS_Sharpe"] - C["oS"][i])
                draws[dd_] = float(np.mean(acc))
            pct = float((draws < real).mean())
            nrows.append(dict(fallback=fb, cadence=cad, n_emptied=len(emp),
                              real=round(real, 4), null_mean=round(float(draws.mean()), 4),
                              null_p05=round(float(np.quantile(draws, 0.05)), 4),
                              null_p95=round(float(np.quantile(draws, 0.95)), 4),
                              pct=round(pct, 4),
                              outside90=bool(pct <= 0.05 or pct >= 0.95)))
    NUL = pd.DataFrame(nrows)
    dump(NUL, "null.csv")
    P(NUL.to_string(index=False))
    rate_ok = bool(len(NUL) and NUL.get("outside90", pd.Series(dtype=bool)).fillna(False).any())
    H.append(dict(H="H_RATE", what=f"real RC_PAIR outside the central {BAR_NULL:.0%} of the "
                                   f"rate-matched null in >= 1 cadence",
                  value=float(NUL.get("outside90", pd.Series([0])).fillna(False).sum()),
                  bar=1.0, passed=rate_ok,
                  note="FAIL = the cadence gradient is a RATE gradient, not a COST gradient"))

    # ---- H_4B / H_4A ----------------------------------------------------------------------
    n4b = int(PAID[PAID.floor > 0].OOS_4b.max())
    n4a = int(PAID.OOS_4a.max())
    H.append(dict(H="H_4B", what="max paid OOS 4b at any (cadence, fallback, floor>0) >= 1",
                  value=float(n4b), bar=1.0, passed=n4b >= 1, note=""))
    H.append(dict(H="H_4A", what="max OOS 4a at any point >= 1",
                  value=float(n4a), bar=1.0, passed=n4a >= 1, note="993: 0 of 28"))

    HT = pd.DataFrame(H)
    P()
    P(HT.to_string(index=False))
    dump(HT, "hypotheses.csv")

    # =====================================================================================
    # (J) RULE 8 WALK-FORWARD -- the capital reading, vs baseline and SPY
    # =====================================================================================
    P()
    P("=" * 100)
    P("(J) RULE 8 WALK-FORWARD -- (book, gross) chosen on 2009-2016 ALONE, OOS 2017-2026")
    P("    both KEEP paths evaluated at every grid point; nothing selected on the OOS tape")
    P("=" * 100)
    ctrl_all = ALL[(ALL.basis == HEAD_BASIS) & (ALL.floor == 0.0) & ~ALL.declined]
    P("  --- the UNSCREENED control's 36 rule-8 picks (9 per cadence) ---")
    cshow = ["panel", "cadence", "chooser", "book", "gross", "OOS_CAGR", "OOS_Sharpe",
             "OOS_MaxDD", "spy_OOS_CAGR", "spy_OOS_Sharpe", "spy_OOS_MaxDD", "v2_Sharpe",
             "v2_MaxDD", "OOS_4b", "OOS_4a", "fail_legs"]
    P(ctrl_all[cshow].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P()
    P(f"  control OOS 4b {int(ctrl_all.OOS_4b.sum())} of {len(ctrl_all)} | "
      f"OOS 4a {int(ctrl_all.OOS_4a.sum())} of {len(ctrl_all)}")
    P("  by cadence: " + "  ".join(
        f"{c}: 4b {int(ctrl_all[ctrl_all.cadence==c].OOS_4b.sum())}/"
        f"{len(ctrl_all[ctrl_all.cadence==c])}  4a "
        f"{int(ctrl_all[ctrl_all.cadence==c].OOS_4a.sum())}" for c in CADORDER))

    hb2 = ALL[ALL.basis == HEAD_BASIS]
    P()
    P("  --- paid OOS 4b / 4a counts, every (cadence x fallback x floor) ---")
    P(PAID.pivot_table(index=["fallback", "floor"], columns="cadence", values="OOS_4b")
      .reindex(columns=CADORDER).to_string())
    P()
    P("  --- full-sample 4b / 4a over the whole 13,500-row ladder ---")
    P(f"  full-sample 4b {int(G.pass4b.sum())} of {len(G)} rows | "
      f"4a {int(G.pass4a.sum())} of {len(G)}")
    for c in CADORDER:
        gc = G[G.cadence == c]
        P(f"    {c}: 4b {int(gc.pass4b.sum())}/{len(gc)}  4a {int(gc.pass4a.sum())}/{len(gc)}")

    passers = ALL[(ALL.basis == HEAD_BASIS) & ALL.OOS_4b.fillna(False)]
    if len(passers):
        P()
        P("  --- every screened pick that clears OOS 4b (the capital reading) ---")
        P(passers[["panel", "cadence", "chooser", "floor", "book", "gross", "share",
                   "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "spy_OOS_CAGR", "spy_OOS_Sharpe",
                   "spy_OOS_MaxDD", "OOS_4a"]]
          .drop_duplicates(subset=["panel", "cadence", "chooser", "book", "gross"])
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---- appendix: the other two bases, NO selection made ---------------------------------
    P()
    P("  --- APPENDIX: the other two share bases, reported, NOT selected on ---")
    APP = []
    for b in BASES:
        for f in FLOORS:
            s = ALL[(ALL.basis == b) & (ALL.floor == f)]
            APP.append(dict(basis=b, legal=LEGAL[b], floor=f, n_slots=len(s),
                            n_declined=int(s.declined.sum()),
                            **{f"decl_{c}": int(s[s.cadence == c].declined.sum())
                               for c in CADORDER}))
    APPD = pd.DataFrame(APP)
    dump(APPD, "appendix_bases.csv")
    P(APPD.to_string(index=False))

    P()
    P(f"  [{time.time()-t0:.0f}s]")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

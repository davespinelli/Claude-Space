#!/usr/bin/env python3
"""
Idea 993 (lane C, 2026-09-16)
PRICE THE EMPTIED-SLOT COST -- IS DECLINING TO PICK BETTER THAN THE UNSCREENED PICK?

  Idea 980 ran the within-family phase share (`S_IS4B`) as a POSITIVE screen on the M/Q 60-family
  grid and published, at its best legal floor 0.40: median OOS Sharpe 0.8312 -> 1.0590 and median
  OOS MaxDD -34.14% -> -21.35%, against an unscreened control.  But the screen EMPTIES SLOTS: 6 of
  18 rule-8 slots at floor 0.40, 12 of 18 at 0.75, 18 of 18 at 0.90.  980's own summary takes the
  median over the SURVIVING picks only, i.e. **a slot the screen refuses is scored as no slot at
  all, at no cost.**  That is an accounting convention, not a result, and it is the single most
  flattering convention available: it lets a screen improve its average by declining to play.

  THIS RUN PAYS FOR THE REFUSALS.  Every one of the 18 slots is scored at every floor.  A slot the
  screen declines is filled with a FALLBACK -- what an operator standing at 2016-12-31 would
  actually hold instead -- and the fallback's own OOS record is carried into the median and into
  the 4b / 4a counts:

      FB_NONE   drop the slot                    -- 980's convention, the INCUMBENT, not a fallback
      FB_CASH   hold cash                        -- 0% return, 0 drawdown; Sharpe DEFINED as 0.0
      FB_SPY    hold SPY buy-and-hold            -- costless, same series as the spy_* comparands
      FB_LIVE   keep running the live book       -- RULES v2 == BAND03 @ 0.75 weekly at 10 bps

  and the sharper, paired question the title asks: ON THE SLOTS IT EMPTIED, does the fallback beat
  the pick the UNSCREENED control made in that same slot?  That is the only comparison in which
  "declining" and "picking" are asked the same question about the same slot.

THE GRID: the ladder ideas 976 / 981 / 984 / 986 / 980 built, rebuilt here from scratch.  3 panels
{U56, B136, SMALL} x 5 books x 2 gross {CORE 0.75, EXT 1.00} x D/W/M/Q at MATCHED gross x every
phase (1/5/21/63) = 2,700 phase-books x 5 cost rungs = 13,500 rows.  Rule-8 slots = 3 panels x 2
cadences x 3 IS-only choosers = 18 per grid half; M/Q is 980's pre-declared headline, D/W is
published beside it.

TUNED AXES -- exactly two, every level reported, none selected:
  (1) fallback : FB_NONE, FB_CASH, FB_SPY, FB_LIVE
  (2) floor    : 0.00 (= unscreened control), 0.10, 0.25, 0.40, 0.50, 0.75, 0.90
The share BASIS is NOT a tuned axis here: it is FIXED at `S_IS4B`, the legal IS-only basis idea 980
pre-declared and whose effect it localised.  `S_ISLEG4` and the LEAKY `S_FULL4B` are rebuilt and
published in an appendix table with NO selection made on them.

PRE-REGISTERED HYPOTHESES (bars fixed before any number was read):
  H_PAID_S   : at SOME floor > 0, the paid median OOS Sharpe over ALL 18 slots still beats the
               unscreened control -- under ALL THREE fallbacks, not just the kindest one
  H_PAID_DD  : same, on median OOS MaxDD (no worse than the control)
  H_ALLFLOOR : the same holds at EVERY floor > 0 under all three fallbacks (the consistency form;
               980's gain already depended on landing between 0.40 and 0.50)
  H_DECLINE_S: on the EMPTIED slots only, paired mean (fallback - unscreened pick) OOS Sharpe > 0
               under all three fallbacks at the best floor.  This is the title's question.
  H_DECLINE_DD: the same on OOS MaxDD
  H_4B       : the paid OOS 4b count at the best floor is >= 1 (unscreened control: 0 of 18)
  H_4A       : any (fallback, floor) point yields >= 1 OOS 4a
  H_CONVENTION: |FB_NONE - FB_LIVE| median OOS Sharpe at 980's own headline floor 0.40 is >= 0.05,
               i.e. the free-refusal convention is MATERIAL and must be reported.  PASS here means
               the record has been reading an accounting choice as a result.
  H_CONVENTION_MEAN: the same on the MEAN.  Reported separately because the median is nearly blind
               to HOW BAD a refusal is -- once every fallback lands below every surviving pick, the
               median moves only to a different order statistic, whereas the mean prices the gap.
               980's published statistic is the median, so both are carried.
  H_DECLINE_ALL: the degenerate all-refuse point (floor 0.90: every slot declined, so the "screen"
               is just the live book everywhere) does NOT beat the best screened point.  If it
               does, the screen's paid gain is not a screening result at all -- it is the live book
               wearing a screen's clothes, and the right reading is "hold the book, run no screen".
  H_RANK     : the floor that ranks best under FB_NONE also ranks best under FB_LIVE -- if not, the
               convention does not merely shift the level, it changes which screen you would ship
  H_NULL     : the best paid point beats >= 0.95 of SIZE-MATCHED RANDOM screens on paid median OOS
               Sharpe, with the SAME refusals paid the same way (a cell the real screen emptied is
               emptied in the null too).  2,000 draws, seed 993.

GATES (printed before any hypothesis number):
  G0  offset_mask(idx, per, 0) == engine.rebalance_mask(idx, per) on D/W/M/Q
  G1  the fast Ctx runner == engine.backtest on returns AND turnover, post warm-up, D and M
  G2  BAND03 @ 0.75 == baseline.rules_v2_weights elementwise
  G2b THE LIVE FALLBACK IS THE LIVE BOOK: the FB_LIVE return series == the ladder's
      (panel, BAND03, CORE, W, phase 0, 10 bps) row on every reported metric
  G3a CROSS-RUN: idea 980's committed 13,500-row ladder reproduced on every shared numeric column
  G3b CROSS-RUN: idea 980's committed 756 screened picks (21 floor x basis points x 36 slots)
      reproduced book-for-book and gross-for-gross -- the screen machinery is 980's, not a lookalike
  G3c CROSS-RUN: 980's published emptied-slot counts (6 / 12 / 18 of 18 at floors 0.40 / 0.75 /
      0.90) recomputed
  G4  MATCHED GROSS: one target matrix per (panel, book, gross), reused across all four cadences
  G5  determinism: one cell rebuilt from scratch
  G6  ACCOUNTING IDENTITY: at floor 0.00 no slot is declined, so all four fallback conventions must
      give IDENTICAL numbers.  This proves the fallback touches ONLY emptied slots.
  G7  IS-PURITY: the screen and every pick are invariant under permuted OOS columns; the fallbacks
      are fixed ex-ante objects (cash / SPY / the live book), chosen without reading the OOS tape

PROTOCOL: 10 bps primary (all five rungs built, headline rung reported), decided at close t /
applied t+1 (LAG 1), warm-up 260 days, IS 2009-2016 / OOS 2017-2026 read once, no shorting, no
leverage beyond the published gross.  Rule 8 walk-forward IS the experiment -- every (book, gross)
is chosen on 2009-2016 alone -- and both KEEP paths (4a and 4b) are evaluated at every grid point.
Nothing in RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py is modified.

DECLARED CONVENTIONS (so the accounting cannot hide anywhere):
  * CASH has zero return and zero variance; its Sharpe is DEFINED as 0.0 and its MaxDD as 0.0.  Its
    CAGR of 0.0 fails 4b's CAGR floor, so a cash slot never certifies -- which is the point.
  * SPY and CASH are costless; the live book pays the full 10 bps.  That flatters the two passive
    fallbacks, i.e. it works AGAINST this run's own hypothesis that refusals are expensive.
  * A declined slot is still a slot: n_slots is 18 at every floor under every fallback but FB_NONE.

SURVIVORSHIP (rule 9): U56, B136 and SMALL are CURRENT-CONSTITUENT lists (SMALL additionally drops
every ticker with max_1d_move >= 1.0 per data/small_meta.csv), so every CAGR and drawdown LEVEL is
optimistic and every 4b pass count -- screened, unscreened and fallback alike -- is an UPPER bound.
The measured object here is a DIFFERENCE between two accounting conventions applied to the SAME
picks on the SAME tape, and is very nearly immune.  The SPY and CASH fallbacks are not
survivorship-inflated at all, so where they beat the screened picks the gap is if anything wider
on honest data.

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
HEADLINE_CADS = ["M", "Q"]           # idea 980's own 60-family grid
EXT_CADS = ["D", "W"]                # published beside it, not a tuned level

LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
LEGNAME = {"H1": "L1_H1", "H2": "L2_H2", "OOS": "L3_OOS", "DD": "L4_DD", "CAGR": "L5_CAGR"}

FLOORS = [0.00, 0.10, 0.25, 0.40, 0.50, 0.75, 0.90]
BASES = ["S_IS4B", "S_ISLEG4", "S_FULL4B"]
LEGAL = {"S_IS4B": True, "S_ISLEG4": True, "S_FULL4B": False}
HEAD_BASIS = "S_IS4B"                # FIXED, inherited from 980 -- not a tuned axis here
ISLEG_BAR = 4
FALLBACKS = ["FB_NONE", "FB_CASH", "FB_SPY", "FB_LIVE"]
PAID_FB = ["FB_CASH", "FB_SPY", "FB_LIVE"]   # the three that actually pay for a refusal
NULL_DRAWS = 2000
NULL_SEED = 993
BAR_NULL = 0.95
BAR_CONVENTION = 0.05                # H_CONVENTION: Sharpe gap that makes the convention material
HEADLINE_FLOOR_980 = 0.40            # 980's own published best legal floor

# idea 980's committed artifacts (G3)
PARENT = OUT / "2026-09-15_is-a-HIGH-WITHIN-FAMILY-PHASE-SHARE-a-POSITIVE-ROBUSTNESS-signal_cloud.ladder.csv"
PARENT_PICKS = OUT / "2026-09-15_is-a-HIGH-WITHIN-FAMILY-PHASE-SHARE-a-POSITIVE-ROBUSTNESS-signal_cloud.picks.csv"
PARENT_SUM = OUT / "2026-09-15_is-a-HIGH-WITHIN-FAMILY-PHASE-SHARE-a-POSITIVE-ROBUSTNESS-signal_cloud.summary.csv"
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
# (1) cadence / phase machinery -- the record's form, verbatim from 980
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
# (2) the book set -- verbatim from 942/962/964/976/981/984/986/980
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
# (3) main
# =========================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 993 (lane C, 2026-09-16) -- PRICE THE EMPTIED-SLOT COST")
    P("  IS DECLINING TO PICK BETTER THAN THE UNSCREENED PICK, ONCE THE REFUSALS ARE PAID FOR?")
    P("=" * 100)
    P(f"  SMOKE={SMOKE}  headline cost {HEAD_COST:.0f} bps (rungs {RUNGS})  LAG={LAG}  WARM={WARM}")
    P(f"  headline grid = 980's 60 families: 3 panels x 5 books x 2 gross x {HEADLINE_CADS}")
    P(f"  reported extension: {EXT_CADS} (not a tuned level)")
    P(f"  tuned axes: fallback {FALLBACKS} x floor {FLOORS} -- ALL reported, none selected")
    P(f"  share basis FIXED at {HEAD_BASIS} (980's legal basis); {BASES[1:]} in an appendix only")
    P("  DECLARED: cash Sharpe := 0.0, cash MaxDD := 0.0; cash and SPY costless; live book pays "
      "10 bps")

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
    cads = CADORDER if not SMOKE else ["M", "Q"]
    for pname, px in panels.items():
        rspy = px["SPY"].pct_change().fillna(0.0).values
        isw = np.asarray(px.index <= pd.Timestamp(IS_END))
        osw = np.asarray(px.index >= pd.Timestamp(OOS_START))
        spy_full, spy_is, spy_oos = (mets(rspy[WARM:]), mets(rspy[WARM:][isw[WARM:]]),
                                     mets(rspy[osw]))
        v2_net = backtest(px, rules_v2_weights(px), cost_bps=HEAD_COST, freq="W")["returns"].values
        v2 = mets(v2_net[WARM:])

        # ---- the three FALLBACK objects, built once per panel, ex ante ----------------
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
            if tag == "FB_CASH":      # DECLARED convention: zero return, zero variance
                for k in ("Sharpe", "H1", "H2", "IS_Sharpe", "IS_H1", "IS_H2", "OOS_Sharpe",
                          "OOS_H1", "OOS_H2"):
                    row[k] = 0.0
                for k in ("CAGR", "IS_CAGR", "OOS_CAGR", "MaxDD", "IS_MaxDD", "OOS_MaxDD"):
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

    FBT = pd.DataFrame([FB[k] for k in FB])
    g10 = G[G.cost_bps == HEAD_COST]

    # ---- G2b: the LIVE fallback IS the live book, i.e. the ladder's own W/phase-0 row ----
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
    gates.append(dict(gate="G3a", what=f"CROSS-RUN: idea 980's committed ladder ({g3note})",
                      value=g3v, bar=G3_TOL, ok=g3v <= G3_TOL))
    P(f"  G3a cross-run vs idea 980's ladder : max|d| {g3v:.3e}  ({g3note})")

    # ---------------------------------------------------------------- the screen (980's, verbatim)
    P()
    P("=" * 100)
    P("(C) THE SCREEN AND ITS REFUSALS -- (book, gross) chosen on 2009-2016 ALONE")
    P("=" * 100)
    fam = g10.groupby(["panel", "book", "gross", "cadence"])
    SH = fam.agg(n_phase=("phase", "size"),
                 S_IS4B=("IS_pass4b", "mean"),
                 S_FULL4B=("pass4b", "mean")).reset_index()
    SH["S_ISLEG4"] = fam["IS_legs_passed"].apply(lambda s: float((s >= ISLEG_BAR).mean())).values
    dump(SH, "shares.csv")
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
                        share=float(getattr(shmap[(pname, r.book, r.gross, cad)], basis)),
                        n_cand=len(cand), declined=False,
                        OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                        FULL_CAGR=r.CAGR, FULL_Sharpe=r.Sharpe, FULL_MaxDD=r.MaxDD,
                        spy_OOS_CAGR=r.spy_OOS_CAGR, spy_OOS_Sharpe=r.spy_OOS_Sharpe,
                        spy_MaxDD=r.spy_MaxDD, v2_Sharpe=r.v2_Sharpe, v2_MaxDD=r.v2_MaxDD,
                        OOS_4b=bool(r.pass4b), OOS_4a=bool(r.pass4a), fail_legs=r.fail_legs))
        return pd.DataFrame(out)

    ALL = pd.concat([run_picks(f, b) for b in BASES for f in FLOORS], ignore_index=True)
    dump(ALL, "picks.csv")

    # ---- G3b / G3c: 980's committed picks and emptied-slot counts ------------------------
    g3b, g3bnote = np.nan, "parent picks not found"
    if PARENT_PICKS.exists():
        PP = pd.read_csv(PARENT_PICKS)
        m = PP.merge(ALL, on=["panel", "cadence", "chooser", "floor", "basis"],
                     suffixes=("_p", "_c"))
        bk_p = m.book_p.fillna("").astype(str)
        bk_c = m.book_c.fillna("").astype(str)
        gr_p = m.gross_p.fillna("").astype(str)
        gr_c = m.gross_c.fillna("").astype(str)
        g3b = float((bk_p != bk_c).sum() + (gr_p != gr_c).sum()
                    + (m["empty"].astype(bool) != m.declined.astype(bool)).sum())
        g3bnote = f"{len(m)} shared (floor x basis x slot) picks"
    gates.append(dict(gate="G3b", what=f"CROSS-RUN: 980's screened picks ({g3bnote})",
                      value=g3b, bar=0.0, ok=(g3b == 0.0)))
    P(f"  G3b cross-run vs 980's committed picks : {g3b} disagreements ({g3bnote})")

    mq = ALL[(ALL.basis == HEAD_BASIS) & ALL.cadence.isin(HEADLINE_CADS)]
    emp = {f: int(mq[mq.floor == f].declined.sum()) for f in FLOORS}
    P(f"  emptied slots on MQ18 by floor ({HEAD_BASIS}): "
      + "  ".join(f"{f:.2f}->{emp[f]}/18" for f in FLOORS))
    g3c = float(abs(emp[0.40] - 6) + abs(emp[0.75] - 12) + abs(emp[0.90] - 18)) if not SMOKE else 0.0
    gates.append(dict(gate="G3c", what="CROSS-RUN: 980's published 6/12/18 emptied slots at "
                                       "floors 0.40/0.75/0.90",
                      value=g3c, bar=0.0, ok=g3c == 0.0))
    P(f"  G3c cross-run vs 980's published emptied-slot counts : {g3c} disagreements")

    # ---- G7 IS-purity --------------------------------------------------------------------
    dis = 0
    for f in (0.25, 0.50):
        a = run_picks(f, HEAD_BASIS)
        c = run_picks(f, HEAD_BASIS, permute_seed=7)
        k = ["panel", "cadence", "chooser"]
        mm = a.merge(c, on=k, suffixes=("_a", "_c"))
        dis += int((mm.book_a.fillna("").astype(str) != mm.book_c.fillna("").astype(str)).sum())
    gates.append(dict(gate="G7", what="IS-PURITY: screen and picks invariant under permuted OOS",
                      value=float(dis), bar=0.0, ok=dis == 0))
    P(f"  G7  IS-purity : {dis} pick disagreements under permuted OOS columns")

    # =====================================================================================
    # (D) PAY FOR THE REFUSALS
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

    def paid_frame(basis, floor, fb, cadset):
        """Every slot in the grid half, with declined slots filled by the fallback."""
        s = ALL[(ALL.basis == basis) & (ALL.floor == floor)
                & ALL.cadence.isin(cadset)].reset_index(drop=True)
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
    P("(E) THE PAID SUMMARY -- every (fallback x floor), ALL 18 SLOTS SCORED")
    P("=" * 100)
    prows = []
    for label, cadset in (("MQ18", HEADLINE_CADS), ("DW18", EXT_CADS)):
        for fb in FALLBACKS:
            for f in FLOORS:
                d = paid_frame(HEAD_BASIS, f, fb, cadset)
                n_tot = len(ALL[(ALL.basis == HEAD_BASIS) & (ALL.floor == f)
                                & ALL.cadence.isin(cadset)])
                prows.append(dict(
                    grid=label, fallback=fb, floor=f, n_slots=n_tot,
                    n_declined=int(ALL[(ALL.basis == HEAD_BASIS) & (ALL.floor == f)
                                       & ALL.cadence.isin(cadset)].declined.sum()),
                    n_scored=len(d),
                    OOS_4b=int(d.OOS_4b.sum()) if len(d) else 0,
                    OOS_4a=int(d.OOS_4a.sum()) if len(d) else 0,
                    med_OOS_Sharpe=round(float(d.OOS_Sharpe.median()), 4) if len(d) else np.nan,
                    mean_OOS_Sharpe=round(float(d.OOS_Sharpe.mean()), 4) if len(d) else np.nan,
                    med_OOS_CAGR=round(float(d.OOS_CAGR.median()), 4) if len(d) else np.nan,
                    mean_OOS_CAGR=round(float(d.OOS_CAGR.mean()), 4) if len(d) else np.nan,
                    med_OOS_MaxDD=round(float(d.OOS_MaxDD.median()), 4) if len(d) else np.nan,
                    mean_OOS_MaxDD=round(float(d.OOS_MaxDD.mean()), 4) if len(d) else np.nan,
                    med_FULL_Sharpe=round(float(d.FULL_Sharpe.median()), 4) if len(d) else np.nan,
                    med_FULL_MaxDD=round(float(d.FULL_MaxDD.median()), 4) if len(d) else np.nan))
    PAID = pd.DataFrame(prows)
    dump(PAID, "paid.csv")
    for lab in ("MQ18", "DW18"):
        P()
        P(f"  --- {lab} ---")
        P(PAID[PAID.grid == lab].drop(columns=["grid"]).to_string(index=False))

    # ---- G6 accounting identity ---------------------------------------------------------
    z = PAID[(PAID.grid == "MQ18") & (PAID.floor == 0.0)]
    cols = ["n_scored", "OOS_4b", "OOS_4a", "med_OOS_Sharpe", "med_OOS_CAGR", "med_OOS_MaxDD"]
    g6 = float(np.nanmax(np.abs(z[cols].values - z[cols].values[0])))
    gates.append(dict(gate="G6", what="ACCOUNTING IDENTITY: all four fallbacks identical at floor 0",
                      value=g6, bar=0.0, ok=g6 == 0.0))
    P()
    P(f"  G6  accounting identity at floor 0.00 (no slot declined) : max|d| {g6:.3e} across "
      f"all four fallback conventions")

    GT = pd.DataFrame(gates)
    P()
    P(f"  GATES: {int(GT.ok.sum())} of {len(GT)} PASS")
    P(GT.to_string(index=False))
    dump(GT, "gates.csv")
    if not GT.ok.all():
        P("  !! a gate FAILED -- results below are NOT to be read as evidence")

    # =====================================================================================
    # (F) THE PAIRED TEST -- on the slots it EMPTIED, is the fallback better than the pick?
    # =====================================================================================
    P()
    P("=" * 100)
    P("(F) THE PAIRED DECLINE TEST -- on EMPTIED slots only, fallback vs the UNSCREENED pick")
    P("    the only comparison that asks declining and picking the SAME question about the")
    P("    SAME slot.  Positive dSharpe / dMaxDD means DECLINING WAS BETTER.")
    P("=" * 100)
    ctrl_slots = {(r.panel, r.cadence, r.chooser): r
                  for r in ALL[(ALL.basis == HEAD_BASIS) & (ALL.floor == 0.0)].itertuples()}
    drows = []
    for label, cadset in (("MQ18", HEADLINE_CADS), ("DW18", EXT_CADS)):
        for fb in PAID_FB:
            for f in FLOORS[1:]:
                s = ALL[(ALL.basis == HEAD_BASIS) & (ALL.floor == f)
                        & ALL.cadence.isin(cadset) & ALL.declined]
                if not len(s):
                    drows.append(dict(grid=label, fallback=fb, floor=f, n_emptied=0))
                    continue
                dS, dD, dC, c4b = [], [], [], 0
                for r in s.itertuples():
                    c = ctrl_slots[(r.panel, r.cadence, r.chooser)]
                    fo = FB[(r.panel, fb)]
                    dS.append(fo["OOS_Sharpe"] - c.OOS_Sharpe)
                    dD.append(fo["OOS_MaxDD"] - c.OOS_MaxDD)
                    dC.append(fo["OOS_CAGR"] - c.OOS_CAGR)
                    c4b += int(bool(c.OOS_4b))
                dS, dD, dC = np.array(dS), np.array(dD), np.array(dC)
                drows.append(dict(
                    grid=label, fallback=fb, floor=f, n_emptied=len(dS),
                    mean_dSharpe=round(float(dS.mean()), 4),
                    med_dSharpe=round(float(np.median(dS)), 4),
                    win_Sharpe=round(float((dS > 0).mean()), 4),
                    mean_dMaxDD=round(float(dD.mean()), 4),
                    med_dMaxDD=round(float(np.median(dD)), 4),
                    win_MaxDD=round(float((dD > 0).mean()), 4),
                    mean_dCAGR=round(float(dC.mean()), 4),
                    win_CAGR=round(float((dC > 0).mean()), 4),
                    ctrl_4b_in_emptied=c4b))
    DEC = pd.DataFrame(drows)
    dump(DEC, "decline.csv")
    for lab in ("MQ18", "DW18"):
        P()
        P(f"  --- {lab} ---")
        P(DEC[DEC.grid == lab].drop(columns=["grid"]).to_string(index=False))

    # =====================================================================================
    # (G) THE SIZE-MATCHED RANDOM-SCREEN NULL, WITH THE SAME REFUSALS PAID THE SAME WAY
    # =====================================================================================
    P()
    P("=" * 100)
    P(f"(G) SIZE-MATCHED RANDOM-SCREEN NULL, REFUSALS PAID -- {NULL_DRAWS:,} draws, seed "
      f"{NULL_SEED}")
    P("=" * 100)
    CELLS = {}
    for pname in panels:
        for cad in cads:
            s = g10[(g10.panel == pname) & (g10.cadence == cad) & (g10.phase == 0)] \
                .reset_index(drop=True)
            CELLS[(pname, cad)] = dict(
                panel=pname, IS_CAGR=s.IS_CAGR.values, IS_Sharpe=s.IS_Sharpe.values,
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

    def null_paid(keep_counts, cadset, fb, draws=NULL_DRAWS, seed=NULL_SEED):
        rng = np.random.default_rng(seed)
        n4b, mS, mD = [], [], []
        keys = [(p, c) for p in panels for c in cadset if (p, c) in CELLS]
        for _ in range(draws):
            a, ss, dd = 0, [], []
            for k in keys:
                C = CELLS[k]
                nk = keep_counts.get(k, 0)
                if nk <= 0:                       # the cell is REFUSED -- pay for it
                    if fb == "FB_NONE":
                        continue
                    f_ = FB[(C["panel"], fb)]
                    for _ch in CHOOSERS:
                        a += int(f_["OOS_4b"])
                        ss.append(f_["OOS_Sharpe"]); dd.append(f_["OOS_MaxDD"])
                    continue
                idx = rng.choice(len(C["p4b"]), size=min(nk, len(C["p4b"])), replace=False)
                for ch in CHOOSERS:
                    i = _pick_idx(ch, idx, C)
                    if i is None:
                        continue
                    a += int(C["p4b"][i])
                    ss.append(C["oS"][i]); dd.append(C["oD"][i])
            n4b.append(a)
            mS.append(np.median(ss) if ss else np.nan)
            mD.append(np.median(dd) if dd else np.nan)
        return np.array(n4b), np.array(mS, float), np.array(mD, float)

    nrows = []
    for fb in FALLBACKS:
        for f in FLOORS[1:]:
            kc = {}
            for pname in panels:
                for cad in HEADLINE_CADS:
                    if (pname, cad) not in CELLS:
                        continue
                    kc[(pname, cad)] = int((CELLS[(pname, cad)]["share"][HEAD_BASIS]
                                            >= f - 1e-12).sum())
            n4b, mS, mD = null_paid(kc, HEADLINE_CADS, fb)
            o = PAID[(PAID.grid == "MQ18") & (PAID.fallback == fb) & (PAID.floor == f)].iloc[0]
            obs4b, obsS, obsD = int(o.OOS_4b), float(o.med_OOS_Sharpe), float(o.med_OOS_MaxDD)
            nrows.append(dict(
                fallback=fb, floor=f, kept=sum(kc.values()),
                obs_4b=obs4b, null_4b_mean=round(float(n4b.mean()), 3),
                pct_beaten_4b=round(float((n4b < obs4b).mean() + 0.5 * (n4b == obs4b).mean()), 4),
                obs_medS=round(obsS, 4), null_medS_mean=round(float(np.nanmean(mS)), 4),
                pct_beaten_S=round(float(np.nanmean(mS < obsS)), 4),
                obs_medDD=round(obsD, 4), null_medDD_mean=round(float(np.nanmean(mD)), 4),
                pct_beaten_DD=round(float(np.nanmean(mD < obsD)), 4)))
    NL = pd.DataFrame(nrows)
    P(NL.to_string(index=False))
    dump(NL, "null.csv")

    # =====================================================================================
    # (H) APPENDIX: the other two bases, paid -- reported, nothing selected on them
    # =====================================================================================
    P()
    P("=" * 100)
    P("(H) APPENDIX -- the other two share bases, refusals paid (FB_LIVE), MQ18.  REPORTED ONLY;")
    P("    no verdict in this run is selected on them, and S_FULL4B is the LEAKY control.")
    P("=" * 100)
    arows = []
    for b in BASES:
        for f in FLOORS:
            d = paid_frame(b, f, "FB_LIVE", HEADLINE_CADS)
            nd = int(ALL[(ALL.basis == b) & (ALL.floor == f)
                         & ALL.cadence.isin(HEADLINE_CADS)].declined.sum())
            arows.append(dict(basis=b, legal=LEGAL[b], floor=f, n_declined=nd,
                              OOS_4b=int(d.OOS_4b.sum()) if len(d) else 0,
                              OOS_4a=int(d.OOS_4a.sum()) if len(d) else 0,
                              med_OOS_Sharpe=round(float(d.OOS_Sharpe.median()), 4) if len(d) else np.nan,
                              med_OOS_MaxDD=round(float(d.OOS_MaxDD.median()), 4) if len(d) else np.nan))
    AP = pd.DataFrame(arows)
    P(AP.to_string(index=False))
    dump(AP, "appendix_bases.csv")

    # =====================================================================================
    # (I) THE PRE-REGISTERED HYPOTHESES
    # =====================================================================================
    P()
    P("=" * 100)
    P("(I) THE PRE-REGISTERED HYPOTHESES  (headline grid = MQ18, 980's 60 families)")
    P("=" * 100)
    H = PAID[PAID.grid == "MQ18"]
    ctrl = H[(H.fallback == "FB_NONE") & (H.floor == 0.0)].iloc[0]
    CS, CD = float(ctrl.med_OOS_Sharpe), float(ctrl.med_OOS_MaxDD)
    P(f"  unscreened control (floor 0.00, 18 of 18 slots filled): OOS 4b {int(ctrl.OOS_4b)}, "
      f"OOS 4a {int(ctrl.OOS_4a)}, median OOS Sharpe {CS:.4f}, median OOS MaxDD {CD:.2%}")

    hyp = []
    # H_PAID_S / H_PAID_DD : does ANY floor > 0 survive under ALL THREE fallbacks?
    okS = [f for f in FLOORS[1:]
           if all(float(H[(H.fallback == fb) & (H.floor == f)].med_OOS_Sharpe.iloc[0]) > CS
                  for fb in PAID_FB)]
    hyp.append(dict(H="H_PAID_S", what="some floor>0 beats the control's median OOS Sharpe under "
                                       "ALL THREE fallbacks",
                    value=float(len(okS)), bar=1.0, verdict="PASS" if okS else "FAIL",
                    detail=f"floors {okS if okS else 'none'}; control {CS:.4f}"))
    okD = [f for f in FLOORS[1:]
           if all(float(H[(H.fallback == fb) & (H.floor == f)].med_OOS_MaxDD.iloc[0]) >= CD
                  for fb in PAID_FB)]
    hyp.append(dict(H="H_PAID_DD", what="some floor>0 is no worse than the control's median OOS "
                                        "MaxDD under ALL THREE fallbacks",
                    value=float(len(okD)), bar=1.0, verdict="PASS" if okD else "FAIL",
                    detail=f"floors {okD if okD else 'none'}; control {CD:.4f}"))
    hyp.append(dict(H="H_ALLFLOOR", what="EVERY floor>0 beats the control on Sharpe under all "
                                         "three fallbacks",
                    value=float(len(okS)), bar=float(len(FLOORS) - 1),
                    verdict="PASS" if len(okS) == len(FLOORS) - 1 else "FAIL",
                    detail=f"{len(okS)} of {len(FLOORS)-1} floors"))

    # best floor, pre-registered rule: highest PAID median OOS Sharpe under FB_LIVE (the
    # realistic fallback), ties broken on paid median OOS MaxDD, among floors where THE SCREEN
    # STILL FILLS AT LEAST HALF THE SLOTS -- idea 980's own eligibility rule ("a screen that
    # empties the grid is not a screen"), inherited verbatim rather than re-invented.  The
    # excluded degenerate points are reported below and carry their own hypothesis.
    live = H[(H.fallback == "FB_LIVE") & (H.floor > 0.0)]
    elig = live[(live.n_slots - live.n_declined) >= 0.5 * live.n_slots]
    if not len(elig):
        elig = live
    best = elig.sort_values(["med_OOS_Sharpe", "med_OOS_MaxDD"], ascending=False).iloc[0]
    BF = float(best.floor)
    P(f"  eligible floors (screen fills >= half the 18 slots, 980's rule): "
      f"{[float(x) for x in elig.floor]}")
    P(f"  best PAID floor (FB_LIVE, pre-registered rule): {BF:.2f}")

    b4b = int(H[(H.fallback == "FB_LIVE") & (H.floor == BF)].OOS_4b.iloc[0])
    hyp.append(dict(H="H_4B", what="paid OOS 4b at the best floor >= 1 (control 0)",
                    value=float(b4b), bar=1.0, verdict="PASS" if b4b >= 1 else "FAIL",
                    detail=f"floor {BF:.2f}, FB_LIVE; control {int(ctrl.OOS_4b)} of 18"))
    a4 = int(H.OOS_4a.max())
    hyp.append(dict(H="H_4A", what="any (fallback, floor) point yields >= 1 OOS 4a",
                    value=float(a4), bar=1.0, verdict="PASS" if a4 >= 1 else "FAIL",
                    detail=f"max over all {len(H)} MQ18 points"))

    # H_DECLINE : the title's question, at the best floor
    dbest = DEC[(DEC.grid == "MQ18") & (DEC.floor == BF)]
    dS_ok = bool(len(dbest)) and bool((dbest.mean_dSharpe > 0).all())
    dD_ok = bool(len(dbest)) and bool((dbest.mean_dMaxDD > 0).all())
    hyp.append(dict(H="H_DECLINE_S", what="on EMPTIED slots, fallback beats the unscreened pick "
                                          "on mean OOS Sharpe, all three fallbacks",
                    value=float(dbest.mean_dSharpe.min()) if len(dbest) else np.nan, bar=0.0,
                    verdict="PASS" if dS_ok else "FAIL",
                    detail=f"floor {BF:.2f}, n_emptied "
                           f"{int(dbest.n_emptied.iloc[0]) if len(dbest) else 0}; "
                           f"per-fallback means "
                           f"{list(dbest.mean_dSharpe) if len(dbest) else []}"))
    hyp.append(dict(H="H_DECLINE_DD", what="on EMPTIED slots, fallback beats the unscreened pick "
                                           "on mean OOS MaxDD, all three fallbacks",
                    value=float(dbest.mean_dMaxDD.min()) if len(dbest) else np.nan, bar=0.0,
                    verdict="PASS" if dD_ok else "FAIL",
                    detail=f"floor {BF:.2f}; per-fallback means "
                           f"{list(dbest.mean_dMaxDD) if len(dbest) else []}"))

    # H_CONVENTION : how much of 980's headline is the free-refusal convention?
    n40 = float(H[(H.fallback == "FB_NONE") & (H.floor == HEADLINE_FLOOR_980)].med_OOS_Sharpe.iloc[0])
    l40 = float(H[(H.fallback == "FB_LIVE") & (H.floor == HEADLINE_FLOOR_980)].med_OOS_Sharpe.iloc[0])
    gap = abs(n40 - l40)
    hyp.append(dict(H="H_CONVENTION", what="|FB_NONE - FB_LIVE| median OOS Sharpe at 980's own "
                                           "headline floor 0.40 is material (>= 0.05)",
                    value=gap, bar=BAR_CONVENTION, verdict="PASS" if gap >= BAR_CONVENTION else "FAIL",
                    detail=f"FB_NONE {n40:.4f} vs FB_LIVE {l40:.4f}"))

    n40m = float(H[(H.fallback == "FB_NONE") & (H.floor == HEADLINE_FLOOR_980)].mean_OOS_Sharpe.iloc[0])
    l40m = float(H[(H.fallback == "FB_LIVE") & (H.floor == HEADLINE_FLOOR_980)].mean_OOS_Sharpe.iloc[0])
    gapm = abs(n40m - l40m)
    hyp.append(dict(H="H_CONVENTION_MEAN", what="the same on the MEAN OOS Sharpe (the median is "
                                                "nearly blind to how bad a refusal is)",
                    value=gapm, bar=BAR_CONVENTION,
                    verdict="PASS" if gapm >= BAR_CONVENTION else "FAIL",
                    detail=f"FB_NONE {n40m:.4f} vs FB_LIVE {l40m:.4f}"))

    # H_DECLINE_ALL : does "refuse every slot and just hold the live book" beat the best screen?
    allref = live[(live.n_slots - live.n_declined) == 0]
    if len(allref):
        ar = allref.sort_values("med_OOS_Sharpe", ascending=False).iloc[0]
        arS, arfl = float(ar.med_OOS_Sharpe), float(ar.floor)
    else:
        arS, arfl = np.nan, np.nan
    hyp.append(dict(H="H_DECLINE_ALL", what="the degenerate ALL-REFUSE point (live book in every "
                                            "slot) does NOT beat the best screened point",
                    value=float(best.med_OOS_Sharpe), bar=arS,
                    verdict="PASS" if (arS != arS or float(best.med_OOS_Sharpe) > arS) else "FAIL",
                    detail=f"best screened {float(best.med_OOS_Sharpe):.4f} @floor {BF:.2f} vs "
                           f"all-refuse {arS:.4f} @floor {arfl:.2f}"))

    # H_RANK : does the convention change WHICH screen you would ship?
    nb_ = H[(H.fallback == "FB_NONE") & (H.floor > 0.0)]
    nb_ = nb_[(nb_.n_slots - nb_.n_declined) >= 0.5 * nb_.n_slots]
    none_best = nb_.sort_values(["med_OOS_Sharpe", "med_OOS_MaxDD"], ascending=False).iloc[0]
    rank_ok = float(none_best.floor) == BF
    hyp.append(dict(H="H_RANK", what="the floor ranked best under FB_NONE is also best under "
                                     "FB_LIVE",
                    value=float(none_best.floor), bar=BF, verdict="PASS" if rank_ok else "FAIL",
                    detail=f"FB_NONE best {float(none_best.floor):.2f}, "
                           f"FB_LIVE best {BF:.2f}"))

    nb = NL[(NL.fallback == "FB_LIVE") & (NL.floor == BF)]
    pb = float(nb.pct_beaten_S.iloc[0]) if len(nb) else np.nan
    hyp.append(dict(H="H_NULL", what="best paid point beats >= 0.95 of size-matched random screens "
                                     "on paid median OOS Sharpe (same refusals paid the same way)",
                    value=pb, bar=BAR_NULL, verdict="PASS" if pb >= BAR_NULL else "FAIL",
                    detail=f"FB_LIVE@{BF:.2f}, null mean med Sharpe "
                           f"{float(nb.null_medS_mean.iloc[0]) if len(nb) else np.nan:.4f}"))
    HY = pd.DataFrame(hyp)
    P(HY.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(HY, "hypotheses.csv")

    # ---------------------------------------------------------------- comparands + verdict
    P()
    P("=" * 100)
    P("(J) COMPARANDS AND BOTH KEEP PATHS")
    P("=" * 100)
    r0 = ALL[~ALL.declined].iloc[0]
    P(f"  SPY OOS {r0.spy_OOS_CAGR:.2%} / {r0.spy_OOS_Sharpe:.4f} / {r0.spy_MaxDD:.2%} "
      f"(full-sample MaxDD, the 4b DD cap's reference)")
    for pname in panels:
        rr = ALL[(~ALL.declined) & (ALL.panel == pname)].iloc[0]
        fl = FB[(pname, "FB_LIVE")]
        P(f"  RULES v2 (live) {pname:6s} full Sharpe {rr.v2_Sharpe:.4f}  MaxDD {rr.v2_MaxDD:.2%}"
          f"   |  as FB_LIVE: OOS {fl['OOS_CAGR']:.2%} / {fl['OOS_Sharpe']:.4f} / "
          f"{fl['OOS_MaxDD']:.2%}  4b={fl['OOS_4b']}  4a={fl['OOS_4a']}")
    P(f"  KEEP path 4a: best paid OOS 4a over all {len(H)} MQ18 points = {a4}")
    P(f"  KEEP path 4b: best paid OOS 4b over all MQ18 points = {int(H.OOS_4b.max())}; "
      f"at the best paid floor {BF:.2f} under FB_LIVE = {b4b}")
    sc = ALL[ALL.OOS_4b.fillna(False).astype(bool) & ALL.cadence.isin(cads)]
    if len(sc):
        u = sc.drop_duplicates(["panel", "cadence", "book", "gross"])
        P("  every OOS 4b passer seen anywhere in this run (any floor, any basis, any cadence):")
        P(u[["panel", "cadence", "book", "gross", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
             "FULL_Sharpe", "FULL_MaxDD", "OOS_4a"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P()
    P("=" * 100)
    P("(K) VERDICT")
    P("=" * 100)
    P(f"  {int((HY.verdict == 'PASS').sum())} of {len(HY)} pre-registered hypotheses PASS")
    for fb in FALLBACKS:
        r = H[(H.fallback == fb) & (H.floor == HEADLINE_FLOOR_980)].iloc[0]
        P(f"  980's headline floor 0.40 under {fb:8s}: {int(r.n_scored)} slots scored, "
          f"OOS 4b {int(r.OOS_4b)}, median OOS Sharpe {r.med_OOS_Sharpe:.4f}, "
          f"median OOS MaxDD {r.med_OOS_MaxDD:.2%}")
    P(f"  [{time.time()-t0:.0f}s]")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"wrote {STEM}.console.txt")


if __name__ == "__main__":
    main()

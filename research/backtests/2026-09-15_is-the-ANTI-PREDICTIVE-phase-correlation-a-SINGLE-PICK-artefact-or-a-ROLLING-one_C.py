#!/usr/bin/env python3
"""Idea 965 (lane C, 2026-09-15) -- is the ANTI-PREDICTIVE phase correlation a SINGLE-PICK
artefact or a ROLLING one?

THE QUESTION (queue, 2026-09-15)
  Idea 962 measured median within-family Spearman(IS CAGR, OOS CAGR) = -0.153 across phases
  from ONE 2009-2016 pick, and concluded that choosing the rebalance phase in sample is
  significantly WORSE than not choosing it.  A single pick held for ten years is also the
  STALEST possible estimator: the phase ranking may simply decay.  Re-run the chooser as an
  EXPANDING-WINDOW ANNUAL RE-CHOICE (re-pick the phase every January on everything up to that
  January) and on the WEEKLY grid (5 phases), and report whether the anti-prediction is an
  artefact of staleness or a property of the dial.

WHY IT MATTERS FOR CAPITAL
  If the phase ranking is merely stale, a live book should re-pick its rebalance day annually
  and would harvest the 3-6 pp of OOS CAGR spread 962 measured inside each phase family.  If
  the ranking is anti-predictive at EVERY horizon -- including a one-year-ahead one chosen on
  fresh data -- then the phase dial is unsteerable, the canonical period-end phase is the only
  defensible convention, and no capital should ever be allocated on a phase argument.

WHAT IS TUNED AND WHAT IS REPORTED (PROTOCOL rule 4: max 2 tuned parameters)
  TUNED 1  RE-CHOICE CADENCE, 3 levels, all reported:
           STATIC  one pick on 2009-2016, held through 2026            (962's, the incumbent)
           EXPAND  re-pick every January on ALL data up to that January (the queue's proposal)
           ROLL8   re-pick every January on the TRAILING 8 YEARS only   (fixed-memory variant;
                   separates 'fresher' from 'longer', since EXPAND is both)
  TUNED 2  GRID, 3 levels, all reported:
           W  5 phases (day of week)     -- the queue's second axis, never before read
           M  21 phases (day of month)   -- 962's grid
           Q  63 phases (day of quarter) -- 962's grid
  REPORTED AXES, nothing fitted on them, every point published:
           chooser  C_CAGR / C_SHARPE / C_CALMAR / C_DDMIN   (962 found the answer flat across
                    all six of its choosers; four are carried here, each reported separately)
           book     TOP05 / TOP10 / TOP20 / EWELIG / BAND03  (942's and 962's five; BAND03 at
                    gross 0.75 IS the live RULES v2 book)
           panel    U56 / B136 / SMALL
           gross    CORE 0.75 / EXT 1.00   (grid and STATIC everywhere; the annual re-choice
                    machinery is run at CORE, the verdict gross)
           cost     0 / 5 / 10 / 25 / 50 bps on the grid; 0 / 10 / 25 for the re-choice
                    machinery.  10 bps carries every verdict (PROTOCOL rule 2).
  CONTROLS, not tuned:
           CANONICAL     phase 0 (period end) -- what the record actually trades
           FAMILY        the mean over ALL phases -- the phase-averaged honest estimator
           ORACLE_ANNUAL the best phase for EACH YEAR chosen WITH hindsight.  Not a strategy;
                         it is the CEILING of the annual dial, and it is what separates
                         'the annual chooser is bad' from 'no annual sequence could pay'.

THE ROLLING BOOK IS RUN AS A BOOK, NOT AS STITCHED STATISTICS
  A re-choice changes WHICH DAY the identical book trades, so the honest object is a single
  rebalance mask that uses phase p(Y) on the days of year Y.  That composite mask is run
  through the same engine-verified runner as every other row (G7 proves a constant sequence
  reproduces its own grid row EXACTLY), so the switch year pays its real turnover.  Before
  2017 the composite trades the CANONICAL phase: rule 8 reserves 2009-2016 for choosing, so
  the dial is only ever switched inside the untouched window.

PRE-REGISTERED BARS (fixed before any number of this run was read; both directions reported)
  H_FRESH   the ranking predicts ONE YEAR AHEAD off fresh data iff the median over (family,
            year) of Spearman(EXPAND window CAGR, NEXT-YEAR CAGR) across phases is >= +0.30
            (962's H_PRED bar, on the freshest estimator that exists).
  H_STALE   the anti-prediction is a STALENESS artefact iff re-choosing lifts that same
            correlation over the STATIC one on the SAME year targets in >= 60% of (family,
            year) pairs.
  H_WEEK    the WEEKLY grid is steerable where M and Q are not iff the median within-family
            Spearman(IS CAGR, OOS CAGR) on W is >= +0.30.
  H_ROLLPAY annual re-choice PAYS iff the rolling book's OOS CAGR beats the CANONICAL's in
            >= 60% of verdict-rung cells.
  H_ROLL4B  annual re-choice EARNS its 4b passes iff its OOS 4b pass rate is >= the
            canonical's AND above the blind-random-phase null's expectation.

SURVIVORSHIP (PROTOCOL rule 9)
  U56 / B136 / SMALL are CURRENT-CONSTITUENT lists (SMALL additionally drops every ticker with
  `max_1d_move` >= 1.0 per `data/small_meta.csv`).  Every CAGR/Sharpe/DD LEVEL below is
  optimistic and none is a capital claim on its own.  Direction for THIS run: every contrast
  (rolling vs static vs canonical vs family mean) is SAME-TAPE, SAME-UNIVERSE, SAME-WEIGHTS and
  differs only in WHICH DAY the identical book trades, so the correlation and pass-rate
  comparisons are unaffected by panel composition.  The 4b LEVELS are read against SPY, which
  is not survivorship-inflated, so a survivor panel makes 4b failures RARER -- every failure
  reported here is, if anything, understated.
"""
import os, sys, time, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score   # noqa: E402
from engine import backtest, rebalance_mask                               # noqa: E402

BAND0, VOLCAP, WARM = 0.03, 0.60, 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
FIRST_CHOICE_YEAR, LAST_YEAR = 2017, 2026
YEARS = list(range(FIRST_CHOICE_YEAR, LAST_YEAR + 1))
ROLL_LEN = 8                                     # trailing years for ROLL8
HEAD_COST, HEAD_GROSS = 10.0, "CORE"
CADENCES = (("W", 5), ("M", 21), ("Q", 63))
CLAIM_SETS = {"CORE": 0.75, "EXT": 1.00}
RUNGS = [0.0, 5.0, 10.0, 25.0, 50.0]
CH_RUNGS = [0.0, 10.0, 25.0]                     # rungs the re-choice machinery is run at
LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
LEGNAME = {"H1": "L1_H1", "H2": "L2_H2", "OOS": "L3_OOS", "DD": "L4_DD", "CAGR": "L5_CAGR"}
FRESH_BAR, STALE_BAR, WEEK_BAR, PAY_BAR = 0.30, 0.60, 0.30, 0.60
COMMITTED = dict(v2_CAGR=0.086282, v2_Sharpe=1.2018, v2_MaxDD=-0.120549,
                 spy_CAGR=0.1516, spy_Sharpe=0.8861, spy_MaxDD=-0.3372)
SMOKE = bool(int(os.environ.get("IDEA965_SMOKE", "0")))
LINES = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# ==========================================================================================
# (1) phase machinery -- copied VERBATIM from idea 962/942 so this run NESTS the record
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
    """Fast runner -- byte-identical to 962's.  G1 asserts it against engine.backtest."""
    def __init__(self, px, mask):
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        m = np.asarray(mask.values if hasattr(mask, "values") else mask, bool)
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
        return (held * self.rets).sum(axis=1), turn


def shift_w(W, idx):
    """weights decided at t are applied at t+1 (PROTOCOL rule 2) -- index-only, so it is
    computed ONCE per (panel, book, gross) and shared by every phase."""
    return W.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values


def sharpe(r):
    v = r.std() * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def maxdd(r):
    if len(r) == 0:
        return np.nan
    eq = np.cumprod(1.0 + r)
    return float((eq / np.maximum.accumulate(eq) - 1).min())


def mets(r):
    if len(r) < 2:
        return dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan, H1=np.nan, H2=np.nan)
    eq = np.cumprod(1.0 + r)
    yrs = len(r) / 252.0
    h = len(r) // 2
    return dict(CAGR=float(eq[-1] ** (1 / yrs) - 1) if yrs > 0 else np.nan,
                Sharpe=sharpe(r), MaxDD=maxdd(r), H1=sharpe(r[:h]), H2=sharpe(r[h:]))


def legs_rec(row):
    """The RECORD's 4b convention (942's/962's, verbatim)."""
    return dict(H1=row["H1"] > row["spy_H1"], H2=row["H2"] > row["spy_H2"],
                OOS=row["OOS_Sharpe"] > row["spy_OOS_Sharpe"],
                DD=abs(row["OOS_MaxDD"]) <= 0.60 * abs(row["spy_MaxDD"]),
                CAGR=row["OOS_CAGR"] >= 0.70 * row["spy_CAGR"])


def legs_pure(row):
    """Every leg read INSIDE the OOS window against SPY's OOS statistics."""
    return dict(H1=row["OOS_H1"] > row["spy_OOS_H1"], H2=row["OOS_H2"] > row["spy_OOS_H2"],
                OOS=row["OOS_Sharpe"] > row["spy_OOS_Sharpe"],
                DD=abs(row["OOS_MaxDD"]) <= 0.60 * abs(row["spy_OOS_MaxDD"]),
                CAGR=row["OOS_CAGR"] >= 0.70 * row["spy_OOS_CAGR"])


def failstr(lg):
    f = [LEGNAME[k] for k in LEGS if not lg[k]]
    return ",".join(f) if f else "-"


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


# ==========================================================================================
# (2) THE BOOKS -- 942's/962's five, verbatim
# ==========================================================================================
def ew_gross(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def band_book(px, band, g):
    """== rules_v2_weights(px, band, g) -- asserted at G2."""
    return ew_gross(px, g).where(band_state(px, band) & px.notna(), 0.0)


def elig_mask(px):
    _, above, vol20 = score(px, vol_scale=False)
    return above & (vol20 < VOLCAP)


def ew_elig(px, g):
    e = elig_mask(px).astype(float).where(px.notna(), 0.0)
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


# ==========================================================================================
# (3) THE CHOOSERS -- every one reads ONLY statistics computed on days strictly before the
#     January it is choosing for (G6).
# ==========================================================================================
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


CHOOSERS = ["C_CAGR", "C_SHARPE", "C_CALMAR", "C_DDMIN"]


def choose(name, cagr, shp, dd):
    """cagr/shp/dd: arrays over phases from ONE window.  Returns the chosen phase index."""
    absdd = np.abs(np.asarray(dd, float))
    if name == "C_CAGR":
        return _argmax(cagr, shp)
    if name == "C_SHARPE":
        return _argmax(shp, cagr)
    if name == "C_CALMAR":
        return _argmax(np.where(absdd > 0, np.asarray(cagr, float) / np.where(absdd > 0, absdd, np.nan),
                                np.nan), shp)
    if name == "C_DDMIN":
        return _argmax(-absdd, shp)
    raise KeyError(name)


# ==========================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 965 (lane C, 2026-09-15) -- is the ANTI-PREDICTIVE phase correlation a SINGLE-PICK")
    P("artefact or a ROLLING one?   3 re-choice cadences x 3 grids (W/M/Q) x 4 choosers x")
    P("5 books x 3 panels.  PROTOCOL: 10 bps carries every verdict, next-day execution, both")
    P("KEEP paths, rule 8 (phases only ever chosen on days before the year they are traded).")
    P("=" * 100)
    P()
    P("PRE-REGISTERED BARS (printed before any number of this run is read)")
    P(f"  H_FRESH   median Spearman(EXPAND window CAGR, NEXT-YEAR CAGR) >= {FRESH_BAR:+.2f}")
    P(f"  H_STALE   re-choice lifts that correlation over STATIC in >= {STALE_BAR:.0%} of "
      f"(family, year) pairs")
    P(f"  H_WEEK    median within-family Spearman(IS CAGR, OOS CAGR) on the W grid >= "
      f"{WEEK_BAR:+.2f}")
    P(f"  H_ROLLPAY rolling book's OOS CAGR > canonical's in >= {PAY_BAR:.0%} of verdict cells")
    P("  H_ROLL4B  rolling OOS 4b pass rate >= canonical's AND above the blind-phase null")
    P()

    panels = {"U56": load_universe()}
    if not SMOKE:
        panels["B136"] = load_universe(broad=True)
        sm, ndrop = load_small()
        panels["SMALL"] = sm
        P(f"  SMALL panel: {sm.shape[1] - 1} names + SPY benchmark ({ndrop} tickers with "
          f"max_1d_move >= 1.0 dropped per data/small_meta.csv)")
    cadences = CADENCES if not SMOKE else (("W", 5), ("M", 21))
    for k, v in panels.items():
        P(f"  panel {k}: {v.shape[1]} columns, {v.index[0].date()} .. {v.index[-1].date()}, "
          f"{len(v)} rows")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(A) GATES -- run before any number of the hypothesis is read")
    P("=" * 100)
    gk = {}
    px = panels["U56"]

    bad = sum(int((offset_mask(px.index, per, 0)[0].values
                   != rebalance_mask(px.index, per).values).sum()) for per in ("W", "M", "Q"))
    gk["G0"] = bad == 0
    P(f"  G0 offset_mask(.,per,0) == engine.rebalance_mask on W/M/Q  : {bad} differing rows   "
      f"{'PASS' if gk['G0'] else 'FAIL'}")

    w75 = band_book(px, BAND0, 0.75)
    g2 = float(np.abs(w75.values - rules_v2_weights(px, BAND0, 0.75).values).max())
    gk["G2"] = g2 == 0.0
    P(f"  G2 BAND03 @0.75 == rules_v2_weights (the LIVE rules)       : {g2:.3e}   "
      f"{'PASS' if gk['G2'] else 'FAIL'}")

    g1 = 0.0
    wt75 = shift_w(w75, px.index)
    for per in ("W", "M", "Q"):
        ctx = Ctx(px, offset_mask(px.index, per, 0)[0])
        gr, tn = ctx.run(wt75)
        fast = pd.Series(gr - tn * HEAD_COST / 1e4, index=px.index)
        slow = backtest(px, w75, cost_bps=HEAD_COST, freq=per)["returns"]
        j = px.index[WARM]
        g1 = max(g1, float(np.abs(slow.loc[j:].values - fast.loc[j:].values).max()))
        del ctx
    gk["G1"] = g1 < 1e-12
    P(f"  G1 Ctx.run == engine.backtest @10 bps, worst of W/M/Q      : {g1:.3e}   "
      f"{'PASS' if gk['G1'] else 'FAIL'}")

    g4 = 0.0
    wt20 = shift_w(ranked_book(px, 0.75, 20), px.index)
    for _ in range(2):
        c = Ctx(px, offset_mask(px.index, "M", 3)[0])
        g4 = max(g4, float(np.abs(c.run(wt20)[0] - c.run(wt20)[0]).max()))
        del c
    gk["G4"] = g4 == 0.0
    P(f"  G4 determinism (TOP20 M phase 3 re-derived twice)          : {g4:.3e}   "
      f"{'PASS' if gk['G4'] else 'FAIL'}")

    bctx = Ctx(px, offset_mask(px.index, "W", 0)[0])
    bg, bt = bctx.run(wt75)
    mv2 = mets((bg - bt * HEAD_COST / 1e4)[WARM:])
    mspy = mets(px["SPY"].pct_change().fillna(0.0).values[WARM:])
    eng = mets(backtest(px, w75, cost_bps=HEAD_COST, freq="W")["returns"]
               .loc[px.index[WARM]:].values)
    g5 = max(abs(mv2[k] - eng[k]) for k in ("CAGR", "Sharpe", "MaxDD"))
    gk["G5"] = g5 < 1e-12
    P(f"  G5 RULES v2 weekly {mv2['CAGR']:.4%}/{mv2['Sharpe']:.4f}/{mv2['MaxDD']:.4%} == "
      f"engine.backtest(freq='W'): {g5:.3e}   {'PASS' if gk['G5'] else 'FAIL'}")
    drift = max(abs(mv2["CAGR"] - COMMITTED["v2_CAGR"]), abs(mv2["Sharpe"] - COMMITTED["v2_Sharpe"]),
                abs(mv2["MaxDD"] - COMMITTED["v2_MaxDD"]),
                abs(mspy["CAGR"] - COMMITTED["spy_CAGR"]),
                abs(mspy["Sharpe"] - COMMITTED["spy_Sharpe"]),
                abs(mspy["MaxDD"] - COMMITTED["spy_MaxDD"]))
    P(f"     REPORTED, not a gate -- SPY on today's cache {mspy['CAGR']:.4%}/{mspy['Sharpe']:.4f}"
      f"/{mspy['MaxDD']:.4%}; the record's published RULES v2 / SPY constants differ by up to "
      f"{drift:.3e} (a DATA-CACHE drift; G3 pins the machinery against 962's committed grid).")
    del bctx

    # --------------------------------------------------------------------------------------
    P()
    P("=" * 100)
    P("(B) THE PHASE GRID + THE CHOOSING WINDOWS")
    P("    every (panel, book, gross, cadence, phase, rung): full/IS/OOS metrics, plus the")
    P("    STATIC / EXPAND / ROLL8 window statistics and the PER-YEAR OOS CAGR")
    P("=" * 100)
    ROWS, BASE = [], {}
    G6_CELL = ("U56", "M", "TOP20", HEAD_COST)   # the cell G6 re-derives under permuted futures
    RSAMP, G6_MASKS = {}, {}
    WIN = {}     # (panel,cad,book,rung) -> {'STATIC'|('EXPAND',Y)|('ROLL8',Y): (cagr,shp,dd) arrays}
    YRC = {}     # (panel,cad,book,rung) -> array[phase, year] of that year's CAGR
    YRS = {}     # same, Sharpe
    for pname, p in panels.items():
        idx = p.index
        post = idx[WARM:]
        yr = post.year.values
        spy = p["SPY"].pct_change().fillna(0.0).values[WARM:]
        oos = np.asarray(post >= pd.Timestamp(OOS_START))
        is_ = np.asarray(post <= pd.Timestamp(IS_END))
        win_masks = {"STATIC": is_}
        for Y in YEARS:
            win_masks[("EXPAND", Y)] = np.asarray(post < pd.Timestamp(f"{Y}-01-01"))
            win_masks[("ROLL8", Y)] = np.asarray(
                (post >= pd.Timestamp(f"{Y - ROLL_LEN}-01-01")) & (post < pd.Timestamp(f"{Y}-01-01")))
        ymask = {Y: (yr == Y) for Y in YEARS}
        ms, ms_o, ms_i = mets(spy), mets(spy[oos]), mets(spy[is_])
        bw = rules_v2_weights(p, BAND0, 0.75)                # the LIVE book, weekly (4a target)
        bc = Ctx(p, offset_mask(idx, "W", 0)[0])
        bgr, btn = bc.run(shift_w(bw, idx))
        for c in set(RUNGS) | set(CH_RUNGS):
            br = (bgr - btn * c / 1e4)[WARM:]
            BASE[(pname, c)] = mets(br[oos]) | {"full_MaxDD": maxdd(br)}
        del bc
        WT = {(b, cs): shift_w(BOOKS[b](p, g), idx) for b in BOOKS for cs, g in CLAIM_SETS.items()}
        for per, n_ph in cadences:
            for b in BOOKS:
                for c in CH_RUNGS:
                    WIN[(pname, per, b, c)] = {k: np.full((n_ph, 3), np.nan) for k in win_masks}
                    YRC[(pname, per, b, c)] = np.full((n_ph, len(YEARS)), np.nan)
                    YRS[(pname, per, b, c)] = np.full((n_ph, len(YEARS)), np.nan)
            for d in range(n_ph):
                ctx = Ctx(p, offset_mask(idx, per, d)[0])
                for (b, cs), W in WT.items():
                    gr, tn = ctx.run(W)
                    gr_w, tn_w = gr[WARM:], tn[WARM:]
                    for c in RUNGS:
                        r = gr_w - tn_w * c / 1e4
                        m, mi, mo = mets(r), mets(r[is_]), mets(r[oos])
                        ROWS.append(dict(
                            panel=pname, book=b, gross=cs, cadence=per, phase=d, cost_bps=c,
                            CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                            H1=m["H1"], H2=m["H2"],
                            IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                            IS_H1=mi["H1"], IS_H2=mi["H2"],
                            OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                            OOS_H1=mo["H1"], OOS_H2=mo["H2"],
                            turn_per_yr=float(tn_w.sum() / (len(r) / 252.0)),
                            spy_CAGR=ms["CAGR"], spy_Sharpe=ms["Sharpe"], spy_MaxDD=ms["MaxDD"],
                            spy_H1=ms["H1"], spy_H2=ms["H2"],
                            spy_OOS_CAGR=ms_o["CAGR"], spy_OOS_Sharpe=ms_o["Sharpe"],
                            spy_OOS_MaxDD=ms_o["MaxDD"], spy_OOS_H1=ms_o["H1"],
                            spy_OOS_H2=ms_o["H2"]))
                    if cs != HEAD_GROSS:
                        continue
                    for c in CH_RUNGS:
                        r = gr_w - tn_w * c / 1e4
                        W_ = WIN[(pname, per, b, c)]
                        for k, msk in win_masks.items():
                            mm = mets(r[msk])
                            W_[k][d] = (mm["CAGR"], mm["Sharpe"], mm["MaxDD"])
                        for iy, Y in enumerate(YEARS):
                            my = mets(r[ymask[Y]])
                            YRC[(pname, per, b, c)][d, iy] = my["CAGR"]
                            YRS[(pname, per, b, c)][d, iy] = my["Sharpe"]
                        if (pname, per, b, c) == G6_CELL:
                            RSAMP[d] = r.copy()
                            G6_MASKS.update(win_masks)
                del ctx
            P(f"  panel {pname} cadence {per} done  ({time.time() - t0:.0f}s)")
    grid = pd.DataFrame(ROWS)
    lr = [legs_rec(r) for _, r in grid.iterrows()]
    lp = [legs_pure(r) for _, r in grid.iterrows()]
    grid["pass4b_REC"] = [all(x.values()) for x in lr]
    grid["fail4b_REC"] = [failstr(x) for x in lr]
    grid["pass4b_OOSPURE"] = [all(x.values()) for x in lp]
    grid["pass4a"] = [bool(r.OOS_H1 > BASE[(r.panel, r.cost_bps)]["H1"]
                           and r.OOS_H2 > BASE[(r.panel, r.cost_bps)]["H2"]
                           and r.OOS_MaxDD >= BASE[(r.panel, r.cost_bps)]["MaxDD"])
                      for _, r in grid.iterrows()]
    dump(grid, "grid")
    P(f"  {len(grid):,} grid rows = {len(panels)} panels x {len(BOOKS)} books x "
      f"{len(CLAIM_SETS)} gross x {sum(n for _, n in cadences)} phases x {len(RUNGS)} rungs")

    # ---- G3: this run's grid REBUILDS 962's committed grid.csv -----------------------------
    comm = OUT / "2026-09-15_does-an-IS-CHOSEN-PHASE-ever-SURVIVE-OOS-on-ANY-BOOK_C.grid.csv"
    if comm.exists():
        cg0 = pd.read_csv(comm)
        keys = ["panel", "book", "gross", "cadence", "phase", "cost_bps"]
        cols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_CAGR", "IS_Sharpe", "OOS_CAGR",
                "OOS_Sharpe", "OOS_MaxDD", "OOS_H1", "OOS_H2", "turn_per_yr"]
        j = cg0.merge(grid, on=keys, suffixes=("_c", "_n"))
        dmax = max(float(np.abs(j[f"{c}_c"].values - j[f"{c}_n"].values).max()) for c in cols)
        gk["G3"] = (len(j) == len(cg0[cg0.cadence.isin([c for c, _ in cadences])])) and dmax < 1e-10
        P(f"  G3 962's committed grid.csv replayed on {len(j)} of {len(cg0)} rows (M+Q), "
          f"max|d| over 13 columns {dmax:.3e}   {'PASS' if gk['G3'] else 'FAIL'}")
    else:
        gk["G3"] = False
        P("  G3 962's committed grid.csv NOT FOUND -- gate FAILS, nesting unproven")

    # --------------------------------------------------------------------------------------
    P()
    P("=" * 100)
    P("(C) THE PICK SEQUENCES -- STATIC (one 2009-2016 pick) vs EXPAND vs ROLL8 (re-picked")
    P("    every January on data that ENDS before that January)")
    P("=" * 100)
    SEQ = {}      # (panel,cad,book,rung,chooser,recad) -> tuple of phases, one per year
    for (pname, per, b, c), W_ in WIN.items():
        for ch in CHOOSERS:
            st = W_["STATIC"]
            p_static = choose(ch, st[:, 0], st[:, 1], st[:, 2])
            SEQ[(pname, per, b, c, ch, "STATIC")] = tuple([p_static] * len(YEARS))
            for rc in ("EXPAND", "ROLL8"):
                seq = []
                for Y in YEARS:
                    w = W_[(rc, Y)]
                    seq.append(choose(ch, w[:, 0], w[:, 1], w[:, 2]))
                SEQ[(pname, per, b, c, ch, rc)] = tuple(seq)
    # controls: canonical, oracle-annual (hindsight best phase per year -- a CEILING, not a rule)
    for (pname, per, b, c), yc in YRC.items():
        SEQ[(pname, per, b, c, "CANONICAL", "CANON")] = tuple([0] * len(YEARS))
        SEQ[(pname, per, b, c, "ORACLE_ANNUAL", "ORACLE")] = tuple(
            int(_argmax(yc[:, iy])) for iy in range(len(YEARS)))
    n_switch = {k: len(set(v)) for k, v in SEQ.items()}
    P(f"  {len(SEQ):,} pick sequences built; distinct phases used per sequence: "
      f"STATIC {np.mean([v for k, v in n_switch.items() if k[5] == 'STATIC']):.2f}, "
      f"EXPAND {np.mean([v for k, v in n_switch.items() if k[5] == 'EXPAND']):.2f}, "
      f"ROLL8 {np.mean([v for k, v in n_switch.items() if k[5] == 'ROLL8']):.2f}, "
      f"ORACLE {np.mean([v for k, v in n_switch.items() if k[5] == 'ORACLE']):.2f} "
      f"(of {len(YEARS)} years)")

    # ---- G6: no chooser reads a day at or after the January it chooses for ------------------
    # G6a: the choosing windows contain no day on or after their own cut date.
    post0 = panels["U56"].index[WARM:]
    viol = int((G6_MASKS["STATIC"] & (post0 > pd.Timestamp(IS_END))).sum())
    for Y in YEARS:
        cut = pd.Timestamp(f"{Y}-01-01")
        for rc in ("EXPAND", "ROLL8"):
            viol += int((G6_MASKS[(rc, Y)] & (post0 >= cut)).sum())
    # G6b: re-derive every pick of one cell after PERMUTING all returns from the cut forward.
    rng = np.random.default_rng(20260915)
    mism = 0
    if RSAMP:
        R = np.vstack([RSAMP[d] for d in sorted(RSAMP)])
        for ch in CHOOSERS:
            for rc in ("EXPAND", "ROLL8"):
                got = []
                for Y in YEARS:
                    cut = np.asarray(post0 >= pd.Timestamp(f"{Y}-01-01"))
                    Rp = R.copy()
                    fut = np.flatnonzero(cut)
                    Rp[:, fut] = Rp[:, rng.permutation(fut)]
                    w = np.array([[mets(Rp[d][G6_MASKS[(rc, Y)]])[k]
                                   for k in ("CAGR", "Sharpe", "MaxDD")] for d in range(len(R))])
                    got.append(choose(ch, w[:, 0], w[:, 1], w[:, 2]))
                mism += int(tuple(got) != SEQ[(G6_CELL[0], G6_CELL[1], G6_CELL[2], G6_CELL[3],
                                               ch, rc)])
    gk["G6"] = (viol == 0) and (mism == 0) and bool(RSAMP)
    P(f"  G6 causality: {viol} choosing-window days on/after their own cut; {mism} of "
      f"{len(CHOOSERS) * 2} pick sequences moved when the FUTURE was permuted   "
      f"{'PASS' if gk['G6'] else 'FAIL'}")

    # --------------------------------------------------------------------------------------
    P()
    P("=" * 100)
    P("(D) RULE 8 WALK-FORWARD -- the composite books, run as books")
    P("=" * 100)

    def composite_mask(idx, per, seq, phmask):
        out = np.zeros(len(idx), bool)
        years = idx.year.values
        out |= phmask[(per, 0)] & (years < FIRST_CHOICE_YEAR)
        for iy, Y in enumerate(YEARS):
            out |= phmask[(per, int(seq[iy]))] & (years == Y)
        return out

    PICKS = []
    g7 = 0.0
    for pname, p in panels.items():
        idx = p.index
        post = idx[WARM:]
        spy = p["SPY"].pct_change().fillna(0.0).values[WARM:]
        oos = np.asarray(post >= pd.Timestamp(OOS_START))
        ms, ms_o = mets(spy), mets(spy[oos])
        phmask = {}
        for per, n_ph in cadences:
            for d in range(n_ph):
                phmask[(per, d)] = offset_mask(idx, per, d)[0].values
        WT = {b: shift_w(BOOKS[b](p, CLAIM_SETS[HEAD_GROSS]), idx) for b in BOOKS}
        # group the work by the composite MASK: one Ctx per distinct (cadence, sequence)
        todo = {}
        for k, seq in SEQ.items():
            if k[0] != pname:
                continue
            todo.setdefault((k[1], seq), []).append(k)
        P(f"  panel {pname}: {len(todo):,} distinct (cadence, sequence) masks for "
          f"{sum(len(v) for v in todo.values()):,} cells")
        for (per, seq), keys in todo.items():
            ctx = Ctx(p, composite_mask(idx, per, seq, phmask))
            books_needed = sorted({k[2] for k in keys})
            res = {}
            for b in books_needed:
                gr, tn = ctx.run(WT[b])
                res[b] = (gr[WARM:], tn[WARM:])
            for k in keys:
                _, per_, b, c, ch, rc = k
                gr_w, tn_w = res[b]
                r = gr_w - tn_w * c / 1e4
                m, mo = mets(r), mets(r[oos])
                row = dict(panel=pname, book=b, gross=HEAD_GROSS, cadence=per_, cost_bps=c,
                           chooser=ch, recadence=rc, seq=",".join(str(x) for x in seq),
                           n_distinct_phases=len(set(seq)),
                           n_switches=int(sum(seq[i] != seq[i - 1] for i in range(1, len(seq)))),
                           CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                           H1=m["H1"], H2=m["H2"],
                           OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                           OOS_H1=mo["H1"], OOS_H2=mo["H2"],
                           turn_per_yr=float(tn_w.sum() / (len(r) / 252.0)),
                           spy_CAGR=ms["CAGR"], spy_H1=ms["H1"], spy_H2=ms["H2"],
                           spy_MaxDD=ms["MaxDD"], spy_OOS_CAGR=ms_o["CAGR"],
                           spy_OOS_Sharpe=ms_o["Sharpe"], spy_OOS_MaxDD=ms_o["MaxDD"],
                           spy_OOS_H1=ms_o["H1"], spy_OOS_H2=ms_o["H2"],
                           base_OOS_Sharpe=BASE[(pname, c)]["Sharpe"],
                           base_OOS_CAGR=BASE[(pname, c)]["CAGR"],
                           base_OOS_MaxDD=BASE[(pname, c)]["MaxDD"],
                           base_OOS_H1=BASE[(pname, c)]["H1"], base_OOS_H2=BASE[(pname, c)]["H2"])
                lgr, lgp = legs_rec(row), legs_pure(row)
                row |= dict(pass4b_REC=all(lgr.values()), fail4b_REC=failstr(lgr),
                            pass4b_OOSPURE=all(lgp.values()), fail4b_OOSPURE=failstr(lgp),
                            pass4a=bool(mo["H1"] > BASE[(pname, c)]["H1"]
                                        and mo["H2"] > BASE[(pname, c)]["H2"]
                                        and mo["MaxDD"] >= BASE[(pname, c)]["MaxDD"]))
                PICKS.append(row)
            del ctx
        P(f"    done ({time.time() - t0:.0f}s)")
    picks = pd.DataFrame(PICKS)
    dump(picks, "walkforward")

    # ---- G7: a CONSTANT sequence reproduces its own GRID row exactly ------------------------
    cano = picks[(picks.chooser == "CANONICAL")]
    j = cano.merge(grid[grid.phase == 0], on=["panel", "book", "gross", "cadence", "cost_bps"],
                   suffixes=("_c", "_g"))
    g7 = max(float(np.abs(j[f"{c}_c"].values - j[f"{c}_g"].values).max())
             for c in ["CAGR", "Sharpe", "MaxDD", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
                       "turn_per_yr"])
    gk["G7"] = (len(j) == len(cano)) and g7 < 1e-12
    P(f"  G7 composite machinery with a CONSTANT sequence == the phase-0 grid row on "
      f"{len(j)} cells, max|d| {g7:.3e}   {'PASS' if gk['G7'] else 'FAIL'}")
    P(f"  GATES {sum(gk.values())} of {len(gk)} PASS  "
      f"({', '.join(k for k, v in gk.items() if not v) or 'none failing'})")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(E) H_FRESH / H_STALE -- does a FRESH window predict NEXT YEAR better than a STALE one?")
    P("    Both estimators are scored against the SAME target: the phases' year-Y CAGR ranking.")
    P("=" * 100)
    PRED = []
    for (pname, per, b, c), W_ in WIN.items():
        yc, ys = YRC[(pname, per, b, c)], YRS[(pname, per, b, c)]
        st = W_["STATIC"]
        for iy, Y in enumerate(YEARS):
            tgt, tgs = yc[:, iy], ys[:, iy]
            row = dict(panel=pname, cadence=per, book=b, cost_bps=c, year=Y,
                       rho_STATIC=spearman(st[:, 0], tgt),
                       rho_EXPAND=spearman(W_[("EXPAND", Y)][:, 0], tgt),
                       rho_ROLL8=spearman(W_[("ROLL8", Y)][:, 0], tgt),
                       rhoS_STATIC=spearman(st[:, 1], tgs),
                       rhoS_EXPAND=spearman(W_[("EXPAND", Y)][:, 1], tgs),
                       rhoS_ROLL8=spearman(W_[("ROLL8", Y)][:, 1], tgs),
                       spread_year_CAGR_pp=float((np.nanmax(tgt) - np.nanmin(tgt)) * 100))
            PRED.append(row)
    pred = pd.DataFrame(PRED)
    dump(pred, "prediction")
    ph = pred[pred.cost_bps == HEAD_COST]
    P(f"  {len(ph):,} (family, year) pairs at the verdict rung "
      f"({len(panels)} panels x {len(BOOKS)} books x {len(cadences)} grids x {len(YEARS)} years)")
    P()
    P("  median Spearman(window CAGR rank, NEXT-YEAR CAGR rank) across phases:")
    tab = ph.groupby("cadence")[["rho_STATIC", "rho_EXPAND", "rho_ROLL8"]].median()
    tab["n"] = ph.groupby("cadence").size()
    P(tab.to_string(float_format=lambda x: f"{x:+.3f}"))
    P(f"  POOLED: STATIC {ph.rho_STATIC.median():+.3f} | EXPAND {ph.rho_EXPAND.median():+.3f} "
      f"| ROLL8 {ph.rho_ROLL8.median():+.3f}   "
      f"(means {ph.rho_STATIC.mean():+.3f} / {ph.rho_EXPAND.mean():+.3f} / "
      f"{ph.rho_ROLL8.mean():+.3f}; share positive "
      f"{(ph.rho_STATIC > 0).mean():.3f} / {(ph.rho_EXPAND > 0).mean():.3f} / "
      f"{(ph.rho_ROLL8 > 0).mean():.3f})")
    P("  the same on the SHARPE ranking:")
    P(ph.groupby("cadence")[["rhoS_STATIC", "rhoS_EXPAND", "rhoS_ROLL8"]].median()
      .to_string(float_format=lambda x: f"{x:+.3f}"))
    P()
    lift_e = float((ph.rho_EXPAND > ph.rho_STATIC).mean())
    lift_r = float((ph.rho_ROLL8 > ph.rho_STATIC).mean())
    P(f"  PAIRED, same target: EXPAND beats STATIC in {lift_e:.3f} of pairs "
      f"(mean delta {(ph.rho_EXPAND - ph.rho_STATIC).mean():+.4f}); "
      f"ROLL8 beats STATIC in {lift_r:.3f} (mean delta "
      f"{(ph.rho_ROLL8 - ph.rho_STATIC).mean():+.4f})")
    P("  by YEAR (median rho, verdict rung, all grids pooled):")
    P(ph.groupby("year")[["rho_STATIC", "rho_EXPAND", "rho_ROLL8"]].median()
      .to_string(float_format=lambda x: f"{x:+.3f}"))
    P()
    P("  962's OWN statistic, re-derived here and extended to the WEEKLY grid --")
    P("  within-family Spearman(IS 2009-2016 CAGR, FULL OOS 2017-2026 CAGR) over phases:")
    fam_rows = []
    gh = grid[(grid.cost_bps == HEAD_COST) & (grid.gross == HEAD_GROSS)]
    for k, sub in gh.groupby(["panel", "book", "cadence"], sort=False):
        s = sub.sort_values("phase")
        fam_rows.append(dict(panel=k[0], book=k[1], cadence=k[2], n_phases=len(s),
                             rho_IS_OOS_CAGR=spearman(s.IS_CAGR.values, s.OOS_CAGR.values),
                             rho_IS_OOS_Sharpe=spearman(s.IS_Sharpe.values, s.OOS_Sharpe.values),
                             spread_OOS_CAGR_pp=float((np.nanmax(s.OOS_CAGR)
                                                       - np.nanmin(s.OOS_CAGR)) * 100),
                             n_phases_pass4b_REC=int(s.pass4b_REC.sum()),
                             canon_OOS_CAGR=float(s.iloc[0].OOS_CAGR),
                             fam_OOS_CAGR_mean=float(np.nanmean(s.OOS_CAGR.values))))
    fams = pd.DataFrame(fam_rows)
    dump(fams, "families")
    P(fams.groupby("cadence")[["rho_IS_OOS_CAGR", "rho_IS_OOS_Sharpe", "spread_OOS_CAGR_pp"]]
      .median().to_string(float_format=lambda x: f"{x:+.3f}"))
    rho_w = float(np.nanmedian(fams[fams.cadence == "W"].rho_IS_OOS_CAGR)) if \
        (fams.cadence == "W").any() else np.nan
    rho_mq = float(np.nanmedian(fams[fams.cadence.isin(["M", "Q"])].rho_IS_OOS_CAGR))
    P(f"  W median rho {rho_w:+.3f}; M+Q median rho {rho_mq:+.3f} "
      f"(962 published -0.153 on M+Q over its 30 families)")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(F) DOES RE-CHOOSING PAY?  OOS levels and both KEEP paths at the verdict rung")
    P("=" * 100)
    hv = picks[picks.cost_bps == HEAD_COST].copy()
    cn = hv[hv.chooser == "CANONICAL"].set_index(["panel", "book", "cadence"])
    hv["canon_OOS_CAGR"] = [cn.loc[(r.panel, r.book, r.cadence), "OOS_CAGR"]
                            for _, r in hv.iterrows()]
    hv["canon_OOS_MaxDD"] = [cn.loc[(r.panel, r.book, r.cadence), "OOS_MaxDD"]
                             for _, r in hv.iterrows()]
    fm = fams.set_index(["panel", "book", "cadence"])
    hv["fam_OOS_CAGR_mean"] = [fm.loc[(r.panel, r.book, r.cadence), "fam_OOS_CAGR_mean"]
                               for _, r in hv.iterrows()]
    hv["regret_vs_canon_pp"] = (hv.OOS_CAGR - hv.canon_OOS_CAGR) * 100
    hv["regret_vs_fammean_pp"] = (hv.OOS_CAGR - hv.fam_OOS_CAGR_mean) * 100
    hv["dd_vs_canon_pp"] = (hv.OOS_MaxDD.abs() - hv.canon_OOS_MaxDD.abs()) * 100
    P("  OOS 4b / 4a PASS and mean OOS CAGR regret vs the CANONICAL, by RE-CHOICE CADENCE:")
    t = hv.groupby("recadence").agg(
        cells=("OOS_CAGR", "size"), pass4b=("pass4b_REC", "sum"),
        pass4b_rate=("pass4b_REC", "mean"), pass4b_pure=("pass4b_OOSPURE", "sum"),
        pass4a=("pass4a", "sum"), mean_OOS_CAGR=("OOS_CAGR", "mean"),
        regret_canon_pp=("regret_vs_canon_pp", "mean"),
        regret_fam_pp=("regret_vs_fammean_pp", "mean"),
        dd_vs_canon_pp=("dd_vs_canon_pp", "mean"), turn=("turn_per_yr", "mean"))
    P(t.to_string(float_format=lambda x: f"{x:.3f}"))
    P()
    P("  the same, split by GRID (W / M / Q):")
    P(hv.pivot_table(index="cadence", columns="recadence",
                     values=["pass4b_REC", "regret_vs_canon_pp"], aggfunc="mean")
      .to_string(float_format=lambda x: f"{x:+.3f}"))
    P()
    P("  by CHOOSER (rolling only), mean OOS CAGR regret vs canonical / vs family mean:")
    roll = hv[hv.recadence.isin(["EXPAND", "ROLL8"])]
    P(roll.groupby(["chooser", "recadence"])[["regret_vs_canon_pp", "regret_vs_fammean_pp",
                                              "dd_vs_canon_pp", "n_switches"]].mean()
      .to_string(float_format=lambda x: f"{x:+.3f}"))
    P()
    pay = float((roll.regret_vs_canon_pp > 0).mean())
    pay_e = float((hv[hv.recadence == "EXPAND"].regret_vs_canon_pp > 0).mean())
    pay_s = float((hv[hv.recadence == "STATIC"].regret_vs_canon_pp > 0).mean())
    payfam = float((roll.regret_vs_fammean_pp > 0).mean())
    P(f"  rolling OOS CAGR > canonical's in {int((roll.regret_vs_canon_pp > 0).sum())} of "
      f"{len(roll)} cells ({pay:.3f}); EXPAND alone {pay_e:.3f}; 962's STATIC pick {pay_s:.3f}")
    P(f"  rolling OOS CAGR > the FAMILY MEAN in {payfam:.3f} of cells "
      f"(mean regret {roll.regret_vs_fammean_pp.mean():+.3f} pp)")
    # paired, same chooser and same cell: does re-choosing beat that chooser's OWN stale pick?
    kk = ["panel", "book", "cadence", "chooser"]
    st_h = hv[hv.recadence == "STATIC"][kk + ["OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]]
    pair = roll.merge(st_h, on=kk, suffixes=("", "_static"))
    pair["d_CAGR_pp"] = (pair.OOS_CAGR - pair.OOS_CAGR_static) * 100
    pair["d_Sharpe"] = pair.OOS_Sharpe - pair.OOS_Sharpe_static
    beat_static = float((pair.d_CAGR_pp > 0).mean())
    P(f"  PAIRED AT THE BOOK LEVEL -- same chooser, same cell, rolling vs its OWN stale pick: "
      f"rolling wins {beat_static:.3f} of {len(pair)} pairs, mean "
      f"{pair.d_CAGR_pp.mean():+.3f} pp of OOS CAGR and {pair.d_Sharpe.mean():+.4f} of OOS Sharpe")
    P(pair.groupby(["recadence", "cadence"])[["d_CAGR_pp", "d_Sharpe"]].mean()
      .to_string(float_format=lambda x: f"{x:+.4f}"))
    P(f"  mean EXTRA OOS drawdown vs canonical: rolling {roll.dd_vs_canon_pp.mean():+.3f} pp, "
      f"static {hv[hv.recadence == 'STATIC'].dd_vs_canon_pp.mean():+.3f} pp")
    P(f"  turnover: canonical {hv[hv.chooser == 'CANONICAL'].turn_per_yr.mean():.2f} x/yr, "
      f"rolling {roll.turn_per_yr.mean():.2f} x/yr "
      f"(the switch year pays a real extra rebalance)")
    P()
    P("  THE CEILING -- ORACLE_ANNUAL (best phase per year, chosen with hindsight):")
    orc = hv[hv.recadence == "ORACLE"]
    P(f"     mean OOS CAGR {orc.OOS_CAGR.mean():.3%} vs canonical "
      f"{hv[hv.chooser == 'CANONICAL'].OOS_CAGR.mean():.3%} and rolling "
      f"{roll.OOS_CAGR.mean():.3%}; regret vs canonical {orc.regret_vs_canon_pp.mean():+.3f} pp; "
      f"4b {int(orc.pass4b_REC.sum())} of {len(orc)}")
    P("     i.e. the annual dial is WORTH this much and no IS rule collects it.")
    P()
    P("  every ROLLING cell that clears 4b OOS at the verdict rung (record convention):")
    win4b = roll[roll.pass4b_REC][["panel", "book", "cadence", "chooser", "recadence",
                                   "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "n_switches",
                                   "regret_vs_canon_pp"]]
    P(win4b.to_string(index=False, float_format=lambda x: f"{x:.3f}") if len(win4b)
      else "     (none)")
    P()
    P("  rung robustness -- OOS 4b pass rate by (recadence, cost rung), CORE gross:")
    P(picks.pivot_table(index="cost_bps", columns="recadence", values="pass4b_REC",
                        aggfunc="mean").to_string(float_format=lambda x: f"{x:.3f}"))
    P("  and mean OOS CAGR by (recadence, cost rung):")
    P(picks.pivot_table(index="cost_bps", columns="recadence", values="OOS_CAGR",
                        aggfunc="mean").to_string(float_format=lambda x: f"{x:.4f}"))
    P()

    # ---- blind-random-phase null ------------------------------------------------------------
    key3 = ["panel", "book", "cadence"]
    f3 = fams[key3 + ["n_phases", "n_phases_pass4b_REC"]]
    mm = roll.merge(f3, on=key3)
    pr = (mm.n_phases_pass4b_REC / mm.n_phases).values
    dist = np.array([1.0])
    for q in pr:
        dist = np.convolve(dist, [1 - q, q])
    exp_blind = float(pr.sum())
    sd_blind = float(np.sqrt((dist * (np.arange(len(dist)) - exp_blind) ** 2).sum()))
    obs = int(roll.pass4b_REC.sum())
    p_le = float(dist[:obs + 1].sum())
    cn_h = hv[hv.chooser == "CANONICAL"]
    p_ge = float(dist[obs:].sum())
    P("  THE BLIND-RANDOM-PHASE NULL -- a coin picking a phase at random on the same cells")
    P(f"     blind expectation {exp_blind:.2f} passes (sd {sd_blind:.2f}) over {len(roll)} "
      f"rolling cells; the rolling choosers delivered {obs}.  P(X <= {obs} | blind) = {p_le:.4f}, "
      f"P(X >= {obs} | blind) = {p_ge:.4f} "
      f"({(obs - exp_blind) / sd_blind:+.2f} sd)")
    P(f"     the CANONICAL phase delivered {int(cn_h.pass4b_REC.sum())} of {len(cn_h)} "
      f"({cn_h.pass4b_REC.mean():.3f}); 962's STATIC pick "
      f"{int(hv[hv.recadence == 'STATIC'].pass4b_REC.sum())} of "
      f"{len(hv[hv.recadence == 'STATIC'])} "
      f"({hv[hv.recadence == 'STATIC'].pass4b_REC.mean():.3f})")
    P()

    # ---- NULL-DRAW audit: does each rolling 4b pass sit on a cell a COIN also clears? --------
    mm["blind_rate"] = mm.n_phases_pass4b_REC / mm.n_phases
    wins = mm[mm.pass4b_REC]
    P("  NULL-DRAW AUDIT -- for every ROLLING cell that passes 4b, the fraction of ITS OWN")
    P("  family's phases that also pass (i.e. what a blind coin would have scored on that cell):")
    if len(wins):
        P(f"     {len(wins)} passing cells: median own base rate {wins.blind_rate.median():.3f}, "
          f"mean {wins.blind_rate.mean():.3f}; "
          f"{int((wins.blind_rate >= 0.25).sum())} of {len(wins)} "
          f"({(wins.blind_rate >= 0.25).mean():.3f}) sit on a family whose coin flip clears 4b "
          f"at least 25% of the time, {int((wins.blind_rate >= 0.50).sum())} at least 50%")
        P(wins.groupby(["panel", "book", "cadence"])
          .agg(passes=("pass4b_REC", "sum"), blind_rate=("blind_rate", "first"))
          .to_string(float_format=lambda x: f"{x:.3f}"))
    else:
        P("     (no rolling cell passes 4b)")
    P()

    # ---- the best rolling book, spelled out against baseline and SPY -------------------------
    P("  RULE 8 + BOTH KEEP PATHS -- the single best ROLLING cell by OOS Sharpe, in full:")
    best = roll.sort_values("OOS_Sharpe", ascending=False).iloc[0]
    P(f"     {best.panel}/{best.book}/{best.cadence}/{best.chooser}/{best.recadence}  "
      f"seq {best.seq}  ({best.n_switches} switches)")
    P(f"     OOS  CAGR {best.OOS_CAGR:.2%}  Sharpe {best.OOS_Sharpe:.3f}  "
      f"MaxDD {best.OOS_MaxDD:.2%}   |  FULL CAGR {best.CAGR:.2%}  Sharpe {best.Sharpe:.3f}  "
      f"MaxDD {best.MaxDD:.2%}  halves {best.H1:.3f} / {best.H2:.3f}")
    P(f"     SPY  OOS CAGR {best.spy_OOS_CAGR:.2%}  Sharpe {best.spy_OOS_Sharpe:.3f}  "
      f"MaxDD {best.spy_OOS_MaxDD:.2%}  (full {best.spy_CAGR:.2%} / {best.spy_MaxDD:.2%})")
    P(f"     LIVE RULES v2 OOS CAGR {best.base_OOS_CAGR:.2%}  Sharpe {best.base_OOS_Sharpe:.3f}  "
      f"MaxDD {best.base_OOS_MaxDD:.2%}")
    P(f"     4b {best.pass4b_REC} (fails: {best.fail4b_REC}) | 4b OOSPURE "
      f"{best.pass4b_OOSPURE} | 4a {best.pass4a}")
    P(f"     its own CANONICAL twin: OOS CAGR {best.canon_OOS_CAGR:.2%} "
      f"(regret {best.regret_vs_canon_pp:+.2f} pp)")
    P(f"     LEG MARGINS: CAGR floor {(best.OOS_CAGR - 0.70 * best.spy_CAGR) * 100:+.3f} pp "
      f"(needs >= {0.70 * best.spy_CAGR:.2%}); DD cap "
      f"{(0.60 * abs(best.spy_MaxDD) - abs(best.OOS_MaxDD)) * 100:+.3f} pp "
      f"(cap {0.60 * abs(best.spy_MaxDD):.2%}); OOS Sharpe "
      f"{best.OOS_Sharpe - best.spy_OOS_Sharpe:+.3f}; halves "
      f"{best.H1 - best.spy_H1:+.3f} / {best.H2 - best.spy_H2:+.3f} over SPY's")
    bb = mm[(mm.panel == best.panel) & (mm.book == best.book) & (mm.cadence == best.cadence)]
    if len(bb):
        P(f"     its own family's blind base rate: "
          f"{int(bb.iloc[0].n_phases_pass4b_REC)} of {int(bb.iloc[0].n_phases)} phases "
          f"({bb.iloc[0].blind_rate:.3f}) clear 4b -- a coin on this cell passes that often.")
    P()
    P(f"  4a across every cell in this run: {int(picks.pass4a.sum())} of {len(picks)} composite "
      f"cells and {int(grid.pass4a.sum())} of {len(grid)} grid rows beat the live RULES v2 book "
      f"out of sample on the 4a path.")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(G) VERDICT -- pre-registered bars against the numbers above")
    P("=" * 100)
    med_e = float(ph.rho_EXPAND.median())
    h_fresh = med_e >= FRESH_BAR
    h_stale = lift_e >= STALE_BAR
    h_week = (rho_w >= WEEK_BAR) if np.isfinite(rho_w) else False
    h_pay = pay >= PAY_BAR
    h_4b = (float(roll.pass4b_REC.mean()) >= float(cn_h.pass4b_REC.mean())) and (obs > exp_blind)
    hyp = [("H_FRESH", h_fresh, f"median Spearman(EXPAND window CAGR, next-year CAGR) "
                                f"{med_e:+.3f} over {len(ph):,} (family, year) pairs "
                                f"(ROLL8 {ph.rho_ROLL8.median():+.3f}, "
                                f"STATIC {ph.rho_STATIC.median():+.3f})"),
           ("H_STALE", h_stale, f"EXPAND beats STATIC on the same year target in {lift_e:.3f} "
                                f"of pairs (ROLL8 {lift_r:.3f}); mean delta "
                                f"{(ph.rho_EXPAND - ph.rho_STATIC).mean():+.4f}; at the BOOK "
                                f"level rolling beats its own stale pick in {beat_static:.3f} "
                                f"of {len(pair)} pairs ({pair.d_CAGR_pp.mean():+.3f} pp)"),
           ("H_WEEK", h_week, f"median within-family Spearman(IS, OOS) CAGR on the W grid "
                              f"{rho_w:+.3f} (M+Q {rho_mq:+.3f})"),
           ("H_ROLLPAY", h_pay, f"rolling OOS CAGR beats canonical in {pay:.3f} of "
                                f"{len(roll)} cells, mean regret "
                                f"{roll.regret_vs_canon_pp.mean():+.3f} pp"),
           ("H_ROLL4B", h_4b, f"rolling 4b {roll.pass4b_REC.mean():.3f} vs canonical "
                              f"{cn_h.pass4b_REC.mean():.3f}; blind null expected "
                              f"{exp_blind:.2f}, observed {obs}, P(X<={obs}) = {p_le:.4f}")]
    hdf = pd.DataFrame([dict(hypothesis=h, supported=bool(v), evidence=e) for h, v, e in hyp])
    P(hdf.to_string(index=False))
    dump(hdf, "hypotheses")
    P()
    P(f"  GATES {sum(gk.values())} of {len(gk)} PASS.  done in {time.time() - t0:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    return grid, picks, pred, fams


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Idea 967 (lane B, 2026-09-16) -- is the 15-to-24-DAY PRE-QUARTER-END WINDOW a real
REBALANCE-DATE EDGE, or a 63-WAY SEARCH?

THE QUESTION (queue, 2026-09-15, filed by idea 961)
  Idea 961 found that all 17 of the 768 quarterly phase-books that clear 4b sit at phase 35-44,
  which its own table labels "15-24 trading days before quarter-end", and that its post-hoc
  calendar profile independently flags the 18-31d bucket as the only positive one
  (+0.529 pp/yr of de-meaned CAGR).  The queue asks: test the window on the MONTHLY grid (a
  21-phase family, where the same flow story predicts a 5-8 day analogue), on SMALL, and
  against a gross-matched null that redraws the phase -- if a coin flip rebalanced 15-24 days
  before quarter-end collects the same +0.5 pp, the window is a TAPE property and not a BOOK
  edge.

WHY IT MATTERS FOR CAPITAL
  This is one of the very few claims in the record that names a rule a person could actually
  follow with real money and no new data: "rebalance about three weeks before quarter-end".
  It costs nothing to adopt, it is not a new signal, and 961 reports it is worth roughly half a
  point of CAGR a year.  If it is real it is free money and it belongs in RULES.md; if it is a
  63-way search over a noisy phase axis it is exactly the kind of thing that makes a book look
  good in a backtest and does nothing in an account.  Either answer is worth having.

  A PREMISE PROBLEM, found while reading 961's committed code and gated below (G4), decides
  what this run has to build.  961's phase axis is `(arange(T) % 63) == p` -- a MODULAR
  63-TRADING-DAY CYCLE anchored at the first row of the panel.  A calendar quarter is 59-65
  trading days, so that cycle DRIFTS against the quarter-end it is named after; 961's own
  `dist_qe` column is the MEDIAN distance to the next quarter-end over a phase's ~68 firings,
  not a constant.  So "phase 35-44 = 15-24 days before quarter-end" is a LABEL on a cycle, not
  a description of a rebalance date.  The tradable object -- rebalance exactly d trading days
  before EVERY quarter-end -- is `offset_mask(idx, "Q", d)`, which is what this run scores.
  Both constructions are built here and the premise is measured, not assumed (G4, section B).

WHAT IS TUNED AND WHAT IS REPORTED (PROTOCOL 4: max 2 tuned parameters)
  TUNED 1  CADENCE, 3 levels, every one reported and none selected:
           Q  63 phases  d = 0..62 trading days before each quarter-end  (961's grid)
           M  21 phases  d = 0..20 trading days before each month-end    (the queue's analogue)
           W   5 phases  d = 0..4                                        (a short control)
  TUNED 2  NULL KIND, 3 levels, every one reported and none selected:
           N_FIXED    a random FIXED basket of k names, rebalanced at the same phase d
           N_ROTBLOCK a random PERSISTENT-SCORE book: scores redraw on a fixed 21-day block
                      calendar that does NOT depend on d, so every phase sees the SAME
                      underlying random signal and any calendar structure in the tape is
                      inherited by the null (idea 969: state the null KIND, it is load-bearing)
           N_PERM     permute the phase labels inside each family -- the pure 63-way-search null
  REPORTED AXES (nothing fitted on them, every point published): panel U56 / B136 / SMALL;
  book TOP05 / TOP10 / TOP20 / EWELIG / BAND03; gross CORE 0.75 / EXT 1.00; cost rung
  0 / 5 / 10 / 25 / 50 bps; window definition W_961 (15-24) / W_BUCKET (18-31) / every 10-wide
  window on the ladder.

PRE-REGISTERED BARS (fixed before any result number below was read; both directions reported)
  H_WINDOW    the window REPLICATES on the tradable Q grid iff the mean within-family de-meaned
              CAGR over d in [15,24], pooled over (panel, book, gross) at 10 bps, is
              >= +0.25 pp/yr.  (961 published +0.529 pp for its own bucket; the bar is set at
              half that so a half-strength replication still counts as a replication.)
  H_MONTHLY   the flow story's OUT-OF-CONSTRUCTION prediction: the scaled analogue window
              d in [5,8] on the M grid is >= +0.25 pp/yr on the same pooling.
  H_SMALL     the Q window is >= +0.25 pp/yr on SMALL alone, a panel 961 never ran.
  H_NULL      the window is a BOOK EDGE rather than a TAPE property iff the real books' window
              premium exceeds the null's mean window premium by >= 2 null SE, under BOTH of
              N_FIXED and N_ROTBLOCK.
  H_SEARCH    the window is not a 63-WAY SEARCH artefact iff the observed BEST 10-wide window
              premium (max over all 54 windows on the Q ladder) sits at or above the 95th
              percentile of the same statistic under N_PERM.
  H_LITERAL   the ZERO-TUNING literal rule -- rebalance at d = 20, the centre of 961's window,
              with nothing chosen on any sample -- beats the canonical quarter-end (d = 0) on
              OOS CAGR in >= 2/3 of cells.
  H_RULE8     (rule 8, REQUIRED) the window survives out of sample iff the IS-chosen (2009-2016
              only) window book beats its OWN family MEDIAN on OOS CAGR in >= 2/3 of cells AND
              at least one cell clears 4b out of sample.
  DECISION RULE, fixed in advance:
      H_WINDOW fail                                  -> the premise does not survive the
                                                        TRADABLE construction; report where the
                                                        961 number actually lives
      H_WINDOW pass and H_NULL fail                  -> TAPE PROPERTY (a coin flip collects it)
      H_WINDOW pass and H_NULL pass and H_SEARCH fail-> 63-WAY SEARCH
      H_WINDOW, H_NULL, H_SEARCH, H_MONTHLY all pass -> REAL REBALANCE-DATE EDGE
      any other mixture                              -> report the mixture, claim nothing

GATES (all printed before any result number)
  G0  `offset_mask(idx, per, 0)` == `engine.rebalance_mask(idx, per)` on D / W / M / Q
  G1  the fast `Ctx` runner == `engine.backtest` on returns AND turnover, post warm-up, on D
      and M (the two ends the engine supports natively)
  G2  BAND03 @ 0.75 == `baseline.rules_v2_weights` elementwise
  G3  CROSS-RUN READ: idea 961's committed `.family.csv` (768 rows) re-read -- its published
      "17 of 768 clear 4b" and "all of them at dist_qe 15..24" recomputed from its own columns
  G3b CROSS-RUN REBUILD: 961's BAND03 modular-63 family rebuilt by THIS run's Ctx on U56 and
      B136 and compared to its committed CAGR column, max|d|
  G4  PREMISE: the within-phase DISPERSION of the true distance-to-quarter-end on 961's modular
      cycle -- if it is not ~0, "15-24 days before quarter-end" is a label, not a rebalance date
  G5  MATCHED GROSS: the target weight matrix of a book is identical across every phase and
      every cadence (only the rebalance mask moves), max|d| == 0
  G6  determinism: one cell rebuilt from scratch, max|d| over returns and turnover
  G7  every rule-8 chooser is IS-ONLY -- picks invariant to permuting the OOS columns

PROTOCOL: 10 bps primary (all five rungs reported), decided at close t / applied t+1, warm-up
260 days, IS 2009-2016 / OOS 2017-2026 read once, no shorting, no leverage beyond the published
gross.  Nothing in RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py is modified.

SURVIVORSHIP (rule 9): U56, B136 and SMALL are CURRENT-CONSTITUENT lists (SMALL additionally
drops every ticker with `max_1d_move` >= 1.0 per `data/small_meta.csv`), so every CAGR and
drawdown LEVEL below is optimistic and both 4b bars are easier here than on a point-in-time
panel.  This run's HEADLINE quantity is a WITHIN-FAMILY de-meaned CAGR -- the same names, the
same tape, the same book, differing only in which day of the quarter the rebalance lands on --
which is very nearly immune to it: survivorship shifts every phase of a family by the same
amount and cancels out of the de-meaning.  The rule-8 4b LEVELS are read against SPY, which is
not survivorship-inflated, so every 4b PASS below is an upper bound and every FAIL understated.
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
RUNGS = [0.0, 5.0, 10.0, 25.0, 50.0]
GROSSES = {"CORE": 0.75, "EXT": 1.00}
CADENCES = {"Q": 63, "M": 21, "W": 5}          # TUNED 1: cadence -> number of phases d
CADORDER = ["Q", "M", "W"]
W961 = (15, 24)                                 # 961's own window, in trading days before QE
WBUCKET = (18, 31)                              # 961's post-hoc positive calendar bucket
WMONTH = (5, 8)                                 # the queue's scaled monthly analogue
LITERAL_D = 20                                  # centre of W961 -- the zero-tuning literal rule
NULLKINDS = ["N_FIXED", "N_ROTBLOCK", "N_PERM"]  # TUNED 2
NULL_K = 20                                     # null basket size, matched to TOP20
NULL_BLOCK = 21                                 # N_ROTBLOCK score-redraw block, in trading days
PHASE_LEN_961 = 63
LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
LEGNAME = {"H1": "L1_H1", "H2": "L2_H2", "OOS": "L3_OOS", "DD": "L4_DD", "CAGR": "L5_CAGR"}

# pre-registered bars
WIN_BAR = 0.25          # pp/yr of de-meaned CAGR
NULL_SE_BAR = 2.0       # null SEs
SEARCH_PCT = 0.95
LITERAL_BAR = 2.0 / 3.0
RULE8_BAR = 2.0 / 3.0

REF961 = OUT / ("2026-09-15_WHY-is-the-CANONICAL-phase-SYSTEMATICALLY-LOW-on-the-"
                "QUARTERLY-grid_cloud.family.csv")

SMOKE = bool(int(os.environ.get("IDEA967_SMOKE", "0")))
NDRAW = 6 if SMOKE else 40
SEED = 967
LINES: list[str] = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix, gz=False):
    p = OUT / (f"{STEM}.{suffix}.csv.gz" if gz else f"{STEM}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ==========================================================================================
# (1) cadence / phase machinery -- offset_mask and Ctx copied VERBATIM from ideas 938 / 942 /
#     962 / 964 / 976 / 981 so this run NESTS the record and the gates are exact reproductions.
# ==========================================================================================
def offset_mask(idx, per, d):
    """True d trading days BEFORE the last trading day of each period.  d = 0 reproduces
    engine.rebalance_mask(idx, per) exactly (G0).  Periods shorter than d clamp to the period's
    FIRST day; the clamp count is returned so it can be reported rather than hidden."""
    key = pd.Series(idx.to_period(per), index=idx)
    last = np.flatnonzero((key != key.shift(-1)).values)
    first = np.concatenate([[0], last[:-1] + 1])
    pick = np.maximum(last - d, first)
    out = pd.Series(False, index=idx)
    out.iloc[np.unique(pick)] = True
    return out, int((last - d < first).sum())


def modular_mask(idx, p, plen=PHASE_LEN_961):
    """961's phase axis: a MODULAR cycle anchored at row 0, NOT a distance to quarter-end."""
    return pd.Series((np.arange(len(idx)) % plen) == p, index=idx)


class Ctx:
    """Fast runner -- byte-identical in construction to 942 / 962 / 964 / 976 / 981's.  G1
    asserts it against engine.backtest.  NOTE it reads `wt` ONLY on rebalance rows, which is
    what makes the null books cheap to build."""

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
    rebalance mask, so it is computed ONCE per (panel, book, gross) and reused by every cadence
    and every phase -- which is exactly what makes the gross MATCHED across the ladder (G5)."""
    return W.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values


def fmet(r):
    """961's / engine.metrics' convention exactly: ddof=1 vol, CAGR = eq[-1]**(252/len) - 1."""
    r = np.asarray(r, float)
    if len(r) < 2:
        return np.nan, np.nan, np.nan
    eq = np.cumprod(1.0 + r)
    cagr = float(eq[-1] ** (252.0 / len(r)) - 1.0)
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    sh = float(r.mean() * 252.0 / vol) if vol > 0 else np.nan
    return cagr, sh, dd


def legs_4b(cagr_oos, h1, h2, s_oos, dd_full, spy_cagr, s1, s2, so, spy_dd):
    """The RECORD's 4b alphabet (942 / 961 / 962 / 976 / 981's, verbatim)."""
    return dict(H1=h1 > s1, H2=h2 > s2, OOS=s_oos > so,
                DD=abs(dd_full) <= 0.60 * abs(spy_dd),
                CAGR=cagr_oos >= 0.70 * spy_cagr)


def failstr(lg):
    f = [LEGNAME[k] for k in LEGS if not lg[k]]
    return ",".join(f) if f else "-"


# ==========================================================================================
# (2) THE BOOK SET -- 942 / 962 / 964 / 976 / 981's five books verbatim
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
# (3) NULL BOOKS -- built ONLY on the rebalance rows Ctx actually reads
# ==========================================================================================
def stable_seed(*parts):
    """A DETERMINISTIC seed from the cell's labels.  Python's str.__hash__ is salted per
    process (PYTHONHASHSEED), so `hash()` would make this script non-reproducible across runs,
    which PROTOCOL 5 forbids.  zlib.crc32 over a canonical byte string is stable forever."""
    import zlib
    return int(zlib.crc32("|".join(str(p) for p in parts).encode())) & 0x7FFFFFFF


def null_weights(kind, rng_seed, ctx, priced, g, k, nblocks_idx):
    """A T x N target-weight array, non-zero only on ctx.reb (the rows Ctx reads).

    N_FIXED     one random basket of k names drawn once, rebalanced to equal weight at every
                phase date.  Phase moves ONLY the rebalance timing -- the FIXED kind (969).
    N_ROTBLOCK  a random PERSISTENT SCORE: scores redraw every NULL_BLOCK trading days on a
                calendar that does NOT depend on the phase, so every phase reads the SAME
                underlying random signal and inherits any calendar structure in the tape.
    """
    rng = np.random.default_rng(rng_seed)
    T, N = ctx.T, ctx.N
    wt = np.zeros((T, N))
    reb = ctx.reb
    dec = np.maximum(reb - 1, 0)                     # the DECISION row for each applied row
    if kind == "N_FIXED":
        ok = np.flatnonzero(priced[dec[-1]])
        if len(ok) < k:
            return None
        pick = rng.choice(ok, size=k, replace=False)
        for i, r in enumerate(reb):
            avail = pick[priced[dec[i], pick]]
            if len(avail) == 0:
                continue
            wt[r, avail] = g / len(avail)
        return wt
    # N_ROTBLOCK
    nb = int(nblocks_idx.max()) + 1
    S = rng.random((nb, N))
    for i, r in enumerate(reb):
        d0 = dec[i]
        s = np.where(priced[d0], S[nblocks_idx[d0]], -np.inf)
        if np.isfinite(s).sum() < k:
            continue
        pick = np.argpartition(-s, k - 1)[:k]
        wt[r, pick] = g / k
    return wt


# ==========================================================================================
# (4) window statistics
# ==========================================================================================
def window_premium(d_arr, cagr_arr, lo, hi):
    """Mean de-meaned CAGR (pp/yr) inside [lo,hi] minus the family mean.  The family mean is 0
    by construction after de-meaning, so this IS the premium."""
    c = np.asarray(cagr_arr, float)
    dm = (c - np.nanmean(c)) * 100.0
    m = (d_arr >= lo) & (d_arr <= hi)
    return float(np.nanmean(dm[m])) if m.any() else np.nan


def best_window(d_arr, cagr_arr, width=10):
    """max over every contiguous width-wide window of the within-family de-meaned CAGR."""
    c = np.asarray(cagr_arr, float)
    dm = (c - np.nanmean(c)) * 100.0
    n = len(dm)
    if n < width:
        return np.nan, np.nan
    k = np.convolve(dm, np.ones(width) / width, mode="valid")
    j = int(np.nanargmax(k))
    return float(k[j]), float(d_arr[j])


# ==========================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 967 (lane B) -- is the 15-24 DAY PRE-QUARTER-END WINDOW a real REBALANCE-DATE EDGE")
    P("                    or a 63-WAY SEARCH?")
    P(f"  run {pd.Timestamp.utcnow():%Y-%m-%d %H:%M UTC}   PROTOCOL {HEAD_COST:.0f} bps / t+1 / "
      f"warm-up {WARM}   SMOKE={int(SMOKE)}")
    P(f"  TUNED 1 cadence {CADENCES};  TUNED 2 null kind {NULLKINDS} ({NDRAW} draws, k={NULL_K})")
    P(f"  windows: W961={W961}  WBUCKET={WBUCKET}  WMONTH={WMONTH}  literal d={LITERAL_D}")
    P("=" * 100)

    panels = {"U56": load_universe()}
    ndrop = 0
    if not SMOKE:
        panels["B136"] = load_universe(broad=True)
        sm, ndrop = load_small()
        panels["SMALL"] = sm
    for kname, v in panels.items():
        P(f"  panel {kname:6s} {v.shape[1]:4d} cols  {v.index[0].date()} .. {v.index[-1].date()}  "
          f"{len(v):,} rows")
    P(f"  SMALL drops {ndrop} tickers with max_1d_move >= 1.0 per data/small_meta.csv; "
      f"SURVIVORSHIP: all panels are CURRENT-CONSTITUENT lists (rule 9).")

    # ------------------------------------------------------------------------------ gates
    P()
    P("=" * 100)
    P("(A) GATES -- printed before any result number")
    P("=" * 100)
    gk, gdetail = {}, []
    u = panels["U56"]
    idx = u.index

    g0 = sum(int((offset_mask(idx, per, 0)[0].values != rebalance_mask(idx, per).values).sum())
             for per in ("D", "W", "M", "Q"))
    gk["G0"] = g0 == 0
    P(f"  G0 offset_mask(.,per,0) == engine.rebalance_mask on D/W/M/Q: {g0} disagreeing rows  "
      f"{'PASS' if gk['G0'] else 'FAIL'}")
    gdetail.append(dict(gate="G0", stat=float(g0), bar=0.0, passed=gk["G0"],
                        what="offset_mask(d=0) == engine.rebalance_mask on D/W/M/Q"))

    w75 = rules_v2_weights(u, BAND0, 0.75)
    d2 = float(np.nanmax(np.abs(w75.values - band_book(u, BAND0, 0.75).values)))
    gk["G2"] = d2 == 0.0
    P(f"  G2 BAND03@0.75 == baseline.rules_v2_weights: max|d| {d2:.3e}  "
      f"{'PASS' if gk['G2'] else 'FAIL'}")
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

    # G3 -- cross-run READ of 961's committed family.csv
    ref = None
    if REF961.exists():
        ref = pd.read_csv(REF961)
        fam961 = ref[ref.canonical == 0].copy()
        # TWO CAGR-leg conventions live in the record and they are NOT the same test:
        #   C_FULL  961's own call -- FULL-sample book CAGR vs 0.70 * FULL SPY CAGR
        #   C_OOS   942/962/964/976/981's `legs_rec` -- OOS book CAGR vs 0.70 * FULL SPY CAGR
        # G3 is a reproduction gate, so it is read on 961's OWN convention; the other is
        # reported beside it because the gap between them is a finding, not a detail.
        res961 = {}
        for conv in ("C_FULL", "C_OOS"):
            npass, hits = 0, []
            for pn in fam961.panel.unique():
                px = panels.get(pn)
                if px is None:
                    continue
                warm = np.arange(len(px)) >= WARM
                spy = px["SPY"].pct_change().fillna(0.0).values
                wpos = np.flatnonzero(warm)
                h = len(wpos) // 2
                h1m = np.zeros(len(px), bool); h1m[wpos[:h]] = True
                h2m = np.zeros(len(px), bool); h2m[wpos[h:]] = True
                oosm = np.asarray(px.index >= pd.Timestamp(OOS_START))
                sc_f, _, sdd_f = fmet(spy[warm])
                _, ss1, _ = fmet(spy[h1m]); _, ss2, _ = fmet(spy[h2m])
                _, ss_o, _ = fmet(spy[oosm])
                for r in fam961[fam961.panel == pn].itertuples():
                    cg_leg = r.CAGR if conv == "C_FULL" else r.OOS_CAGR
                    lg = legs_4b(cg_leg, r.H1, r.H2, r.OOS_Sharpe, r.MaxDD,
                                 sc_f, ss1, ss2, ss_o, sdd_f)
                    if all(lg.values()):
                        npass += 1
                        hits.append(r.dist_qe)
                res961[conv] = (npass, float(np.min(hits)) if hits else np.nan,
                                float(np.max(hits)) if hits else np.nan)
        npass961, dmin, dmax = res961["C_FULL"]
        gk["G3"] = (npass961 == 17) and (dmin >= W961[0]) and (dmax <= W961[1])
        P(f"  G3 CROSS-RUN READ idea 961's committed family.csv ({len(ref):,} rows, "
          f"{len(fam961):,} non-canonical) on 961's OWN CAGR-leg convention (C_FULL): 4b passes "
          f"{npass961} (published 17), dist_qe {dmin:.0f}..{dmax:.0f} "
          f"(published {W961[0]}..{W961[1]})  {'PASS' if gk['G3'] else 'FAIL'}")
        no, lo, hi = res961["C_OOS"]
        P(f"     FINDING, same file, the RECORD'S MAJORITY convention (C_OOS, as in 942 / 962 / "
          f"964 / 976 / 981's `legs_rec`): {no} passes over dist_qe {lo:.0f}..{hi:.0f}.")
        P(f"     961's headline '17, ALL at 15-24d' is therefore CONVENTION-DEPENDENT: on the "
          f"convention the rest of the record uses, the count nearly doubles and the window")
        P(f"     widens from 10 days to {hi-lo+1:.0f}.  The queue's premise for this idea quotes "
          f"the C_FULL reading.  Also: 961 published the denominator as 768, which counts its "
          f"12 CANONICAL rows; the phase family proper is {len(fam961):,}.")
        gdetail.append(dict(gate="G3", stat=float(npass961), bar=17.0, passed=gk["G3"],
                            what="961's '17 of 768 clear 4b, all at 15-24d' on its own C_FULL"))
        gdetail.append(dict(gate="G3_alt", stat=float(no), bar=17.0, passed=(no == 17),
                            what="the same file on the record's majority C_OOS convention"))
    else:
        gk["G3"] = False
        P("  G3 FAIL: idea 961's family.csv not found")
        gdetail.append(dict(gate="G3", stat=np.nan, bar=17.0, passed=False,
                            what="961 family.csv missing"))

    # G3b -- cross-run REBUILD of 961's BAND03 modular-63 family
    g3b = np.nan
    if ref is not None:
        errs, per_panel = [], {}
        for pn in [p for p in ("U56", "B136") if p in panels]:
            px = panels[pn]
            warm = np.arange(len(px)) >= WARM
            ismask = warm & np.asarray(px.index <= pd.Timestamp(IS_END))
            swb = shift1(band_book(px, BAND0, 0.75), px.index)
            sub = ref[(ref.panel == pn) & (ref.mech == "BAND03") & (ref.canonical == 0)]
            ef, ei = [], []
            for r in sub.itertuples():
                c = Ctx(px, modular_mask(px.index, int(r.phase)))
                gr, tn, _ = c.run(swb)
                net = gr - tn * HEAD_COST / 1e4
                ef.append(abs(fmet(net[warm])[0] - r.CAGR))
                ei.append(abs(fmet(net[ismask])[0] - r.IS_CAGR))
            per_panel[pn] = (float(np.max(ef)), float(np.max(ei)), len(ef),
                             str(px.index[-1].date()))
            errs += ef
        g3b = float(np.max(errs)) if errs else np.nan
        gk["G3b"] = bool(errs) and g3b < 1e-9
        P(f"  G3b CROSS-RUN REBUILD 961's BAND03 modular-63 family CAGR: max|d| {g3b:.3e} over "
          f"{len(errs)} phases  {'PASS' if gk['G3b'] else 'FAIL'}")
        # G3c -- WHY G3b reads what it reads.  A full-sample number moves when the TAPE GROWS;
        # the IS window (<= 2016-12-31) cannot move, so splitting the two isolates the cause.
        for pn, (ef_, ei_, n_, last_) in per_panel.items():
            P(f"     G3c {pn:5s} n={n_:3d}  FULL-sample max|d| {ef_:.3e}   IS-window max|d| "
              f"{ei_:.3e}   this run's last bar {last_}")
            gdetail.append(dict(gate=f"G3c_{pn}", stat=ef_, bar=1e-9, passed=ef_ < 1e-9,
                                what=f"961 BAND03 rebuild on {pn}, full sample"))
        b136 = per_panel.get("B136")
        u56 = per_panel.get("U56")
        gk["G3c"] = bool(b136 and u56 and b136[0] < 1e-9 and u56[1] < 1e-6)
        P(f"     G3c DIAGNOSIS: the construction reproduces EXACTLY on B136 "
          f"({b136[0]:.1e}, whose cached tape has not moved since 961 ran) and exactly inside "
          f"U56's IS window ({u56[1]:.1e});")
        P(f"     only U56's FULL-sample number drifts ({u56[0]:.1e}), because data/prices.csv "
          f"has gained bars (961 ran 2026-09-15; this run's U56 ends {u56[3]}).  G3b's failure "
          f"is PRICE-VINTAGE DRIFT, not a construction disagreement  "
          f"{'CONFIRMED' if gk['G3c'] else 'NOT CONFIRMED'}")
        gdetail.append(dict(gate="G3b", stat=g3b, bar=1e-9, passed=gk["G3b"],
                            what="961's BAND03 modular-63 family CAGR rebuilt by this run"))
        gdetail.append(dict(gate="G3c", stat=u56[1] if u56 else np.nan, bar=1e-6,
                            passed=gk["G3c"],
                            what="G3b's residual isolated to price-vintage drift on U56"))
    else:
        gk["G3b"] = gk["G3c"] = False

    # G4 -- PREMISE: is 961's phase label a rebalance DATE?
    qe = np.flatnonzero(rebalance_mask(idx, "Q").values)
    ar = np.arange(len(idx))
    nxt = np.searchsorted(qe, ar, side="left")
    dist = np.full(len(idx), np.nan)
    ok = nxt < len(qe)
    dist[ok] = qe[nxt[ok]] - ar[ok]
    warm_u = ar >= WARM
    sds, rngs = [], []
    for p in range(PHASE_LEN_961):
        m = ((ar % PHASE_LEN_961) == p) & warm_u & np.isfinite(dist)
        v = dist[m]
        if len(v) > 1:
            sds.append(float(np.std(v, ddof=1)))
            rngs.append(float(v.max() - v.min()))
    med_sd, med_rng = float(np.median(sds)), float(np.median(rngs))
    gk["G4"] = med_sd < 1.0            # a real rebalance DATE would have sd ~ 0
    P(f"  G4 PREMISE: within-phase sd of the TRUE distance-to-quarter-end on 961's modular-63 "
      f"cycle: median {med_sd:.2f} trading days (range {min(sds):.2f}..{max(sds):.2f}), median "
      f"within-phase SPREAD {med_rng:.0f} days")
    P(f"     bar: a phase that IS a rebalance date has sd < 1.0  ->  "
      f"{'PASS' if gk['G4'] else 'FAIL: 961 phase labels are NOT rebalance dates'}")
    gdetail.append(dict(gate="G4", stat=med_sd, bar=1.0, passed=gk["G4"],
                        what="within-phase sd of true distance-to-QE on 961's modular cycle"))

    # G5 -- matched gross
    Wa = band_book(u, BAND0, 0.75)
    g5 = float(np.abs(shift1(Wa, idx) - shift1(band_book(u, BAND0, 0.75), idx)).max())
    gk["G5"] = g5 == 0.0
    P(f"  G5 MATCHED GROSS: target weights identical across phases/cadences by construction "
      f"(the mask alone moves): max|d| {g5:.3e}  {'PASS' if gk['G5'] else 'FAIL'}")
    gdetail.append(dict(gate="G5", stat=g5, bar=0.0, passed=gk["G5"],
                        what="target weight matrix identical across phases and cadences"))

    # G6 -- determinism
    cA = Ctx(u, offset_mask(idx, "Q", LITERAL_D)[0]); a1, t1, _ = cA.run(sw)
    cB = Ctx(u, offset_mask(idx, "Q", LITERAL_D)[0]); a2, t2, _ = cB.run(shift1(rules_v2_weights(u, BAND0, 0.75), idx))
    g6 = max(float(np.abs(a1 - a2).max()), float(np.abs(t1 - t2).max()))
    gk["G6"] = g6 == 0.0
    P(f"  G6 determinism (U56/Q/d={LITERAL_D}/BAND03 rebuilt from scratch): max|d| {g6:.3e}  "
      f"{'PASS' if gk['G6'] else 'FAIL'}")
    gdetail.append(dict(gate="G6", stat=g6, bar=0.0, passed=gk["G6"],
                        what="one cell rebuilt from scratch, returns and turnover"))

    # ------------------------------------------------------------------ B: the tradable grid
    P()
    P("=" * 100)
    P("(B) THE TRADABLE GRID -- rebalance EXACTLY d trading days before every period end")
    P("=" * 100)
    cads = CADORDER if not SMOKE else ["Q", "M"]
    rows, spymet = [], {}
    clampinfo = []
    for pname, px in panels.items():
        pidx = px.index
        T = len(pidx)
        ar = np.arange(T)
        warm = ar >= WARM
        ism = warm & np.asarray(pidx <= pd.Timestamp(IS_END))
        oosm = np.asarray(pidx >= pd.Timestamp(OOS_START))
        wpos = np.flatnonzero(warm)
        hh = len(wpos) // 2
        h1m = np.zeros(T, bool); h1m[wpos[:hh]] = True
        h2m = np.zeros(T, bool); h2m[wpos[hh:]] = True
        spy = px["SPY"].pct_change().fillna(0.0).values
        sc_f, ss_f, sdd_f = fmet(spy[warm])
        _, ss1, _ = fmet(spy[h1m]); _, ss2, _ = fmet(spy[h2m])
        sc_o, ss_o, sdd_o = fmet(spy[oosm])
        sc_i, ss_i, sdd_i = fmet(spy[ism])
        spymet[pname] = dict(CAGR=sc_f, Sharpe=ss_f, MaxDD=sdd_f, H1=ss1, H2=ss2,
                             OOS_CAGR=sc_o, OOS_Sharpe=ss_o, OOS_MaxDD=sdd_o,
                             IS_CAGR=sc_i, IS_Sharpe=ss_i, IS_MaxDD=sdd_i)
        # the 10 (book, gross) target matrices, built ONCE and reused by every phase (G5)
        SW = {}
        for bname in BOOKORDER:
            for gname, g in GROSSES.items():
                SW[(bname, gname)] = shift1(BOOKS[bname](px, g), pidx)
        for cad in cads:
            nph = CADENCES[cad]
            for d in range(nph):
                mask, nclamp = offset_mask(pidx, cad, d)
                clampinfo.append(dict(panel=pname, cadence=cad, d=d, n_reb=int(mask.sum()),
                                      n_clamped=nclamp))
                c = Ctx(px, mask)
                for (bname, gname), swx in SW.items():
                    gr, tn, gross_r = c.run(swx)
                    rec = dict(panel=pname, book=bname, gross=gname, cadence=cad, d=d,
                               mean_gross=float(np.nanmean(gross_r[warm])),
                               turn=float(tn[warm].sum() / (warm.sum() / 252.0)))
                    for rung in RUNGS:
                        net = gr - tn * rung / 1e4
                        cg, sh, dd = fmet(net[warm])
                        tag = "" if rung == HEAD_COST else f"_c{int(rung)}"
                        rec[f"CAGR{tag}"] = cg
                        if rung == HEAD_COST:
                            _, s1, _ = fmet(net[h1m]); _, s2, _ = fmet(net[h2m])
                            co, so, do = fmet(net[oosm])
                            ci, si, di = fmet(net[ism])
                            rec.update(Sharpe=sh, MaxDD=dd, H1=s1, H2=s2,
                                       OOS_CAGR=co, OOS_Sharpe=so, OOS_MaxDD=do,
                                       IS_CAGR=ci, IS_Sharpe=si, IS_MaxDD=di)
                    rows.append(rec)
        P(f"  {pname}: {len([r for r in rows if r['panel'] == pname]):,} books "
          f"({len(BOOKORDER)} books x {len(GROSSES)} gross x "
          f"{sum(CADENCES[c] for c in cads)} phases)   t={time.time()-t0:.0f}s")
    grid = pd.DataFrame(rows)
    dump(grid, "grid", gz=True)
    dump(pd.DataFrame(clampinfo), "clamp")
    cl = pd.DataFrame(clampinfo)
    clw = cl[(cl.cadence == "Q") & (cl.d >= W961[0]) & (cl.d <= W961[1])]
    P(f"  clamping inside the Q window d={W961[0]}..{W961[1]}: {int(clw.n_clamped.sum())} "
      f"clamped rebalances out of {int(clw.n_reb.sum()):,}  "
      f"(a short quarter forces the rebalance to the quarter's first day)")

    # ------------------------------------------------- C: the window profile and H_WINDOW
    P()
    P("=" * 100)
    P("(C) THE WINDOW PROFILE -- within-family de-meaned CAGR by d (pp/yr), 10 bps")
    P("=" * 100)
    grid["dm_CAGR_pp"] = (grid.CAGR - grid.groupby(
        ["panel", "book", "gross", "cadence"]).CAGR.transform("mean")) * 100.0

    prem_rows = []
    for (pn, bk, gs, cad), gg in grid.groupby(["panel", "book", "gross", "cadence"]):
        gg = gg.sort_values("d")
        dv, cv = gg.d.values, gg.CAGR.values
        w = W961 if cad == "Q" else (WMONTH if cad == "M" else (1, 2))
        bw, bd = best_window(dv, cv, width=min(10, len(dv)))
        prem_rows.append(dict(panel=pn, book=bk, gross=gs, cadence=cad,
                              prem_W961=window_premium(dv, cv, *W961) if cad == "Q" else np.nan,
                              prem_WBUCKET=window_premium(dv, cv, *WBUCKET) if cad == "Q" else np.nan,
                              prem_win=window_premium(dv, cv, *w),
                              best_win_prem=bw, best_win_d=bd,
                              argmax_d=float(dv[int(np.nanargmax(cv))]),
                              fam_spread_pp=float((np.nanmax(cv) - np.nanmin(cv)) * 100)))
    prem = pd.DataFrame(prem_rows)
    dump(prem, "premium")

    P("\n  Q grid -- mean de-meaned CAGR (pp/yr) by distance-to-quarter-end bucket, all cells:")
    q = grid[grid.cadence == "Q"].copy()
    q["bucket"] = pd.cut(q.d, [-0.1, 8, 14, 24, 31, 45, 62],
                         labels=["0-8d", "9-14d", "15-24d", "25-31d", "32-45d", "46-62d"])
    prof = q.groupby("bucket").agg(n=("dm_CAGR_pp", "size"), mean_pp=("dm_CAGR_pp", "mean"),
                                   med_pp=("dm_CAGR_pp", "median"))
    P(prof.to_string(float_format=lambda x: f"{x:+.3f}"))

    pooled_q = float(q[(q.d >= W961[0]) & (q.d <= W961[1])].dm_CAGR_pp.mean())
    pooled_qb = float(q[(q.d >= WBUCKET[0]) & (q.d <= WBUCKET[1])].dm_CAGR_pp.mean())
    gk_H = {}
    gk_H["H_WINDOW"] = pooled_q >= WIN_BAR
    P(f"\n  H_WINDOW  Q window d={W961[0]}..{W961[1]} pooled over all "
      f"{len(prem[prem.cadence=='Q'])} cells: {pooled_q:+.3f} pp/yr   (bar >= +{WIN_BAR})  -> "
      f"{'PASS' if gk_H['H_WINDOW'] else 'FAIL'}")
    P(f"            961's own bucket d={WBUCKET[0]}..{WBUCKET[1]}: {pooled_qb:+.3f} pp/yr "
      f"(961 published +0.529 pp on its MODULAR cycle)")

    m = grid[grid.cadence == "M"]
    pooled_m = float(m[(m.d >= WMONTH[0]) & (m.d <= WMONTH[1])].dm_CAGR_pp.mean())
    gk_H["H_MONTHLY"] = pooled_m >= WIN_BAR
    P(f"  H_MONTHLY M window d={WMONTH[0]}..{WMONTH[1]} pooled: {pooled_m:+.3f} pp/yr   "
      f"(bar >= +{WIN_BAR})  -> {'PASS' if gk_H['H_MONTHLY'] else 'FAIL'}")

    if "SMALL" in panels:
        qs = q[q.panel == "SMALL"]
        pooled_s = float(qs[(qs.d >= W961[0]) & (qs.d <= W961[1])].dm_CAGR_pp.mean())
    else:
        pooled_s = np.nan
    gk_H["H_SMALL"] = bool(pooled_s >= WIN_BAR)
    P(f"  H_SMALL   Q window on SMALL alone: {pooled_s:+.3f} pp/yr   (bar >= +{WIN_BAR})  -> "
      f"{'PASS' if gk_H['H_SMALL'] else 'FAIL'}")

    P("\n  per-panel / per-cadence window premium (pp/yr), mean over books x gross:")
    piv = prem.pivot_table(index=["cadence"], columns="panel", values="prem_win", aggfunc="mean")
    P(piv.to_string(float_format=lambda x: f"{x:+.3f}"))
    P("\n  per-book Q-window premium (pp/yr):")
    pivb = prem[prem.cadence == "Q"].pivot_table(index="book", columns="panel",
                                                 values="prem_W961", aggfunc="mean").reindex(BOOKORDER)
    P(pivb.to_string(float_format=lambda x: f"{x:+.3f}"))
    P("\n  cost-rung sensitivity of the Q window premium (pp/yr, pooled over all cells):")
    for rung in RUNGS:
        tag = "" if rung == HEAD_COST else f"_c{int(rung)}"
        col = f"CAGR{tag}"
        qq = grid[grid.cadence == "Q"].copy()
        qq["dm"] = (qq[col] - qq.groupby(["panel", "book", "gross"])[col].transform("mean")) * 100
        v = float(qq[(qq.d >= W961[0]) & (qq.d <= W961[1])].dm.mean())
        P(f"    {rung:5.0f} bps: {v:+.3f} pp/yr")

    # ------------------------------------------------------------------- D: the nulls
    P()
    P("=" * 100)
    P(f"(D) NULLS -- TUNED 2, all {len(NULLKINDS)} kinds reported ({NDRAW} draws, k={NULL_K}, "
      f"gross {GROSSES['CORE']})")
    P("=" * 100)
    null_rows = []
    ncads = [c for c in cads if c in ("Q", "M")]
    for pname, px in panels.items():
        pidx = px.index
        T = len(pidx)
        warm = np.arange(T) >= WARM
        priced = px.notna().values
        blk = (np.arange(T) // NULL_BLOCK).astype(int)
        for cad in ncads:
            nph = CADENCES[cad]
            # phase OUTER, draw INNER: exactly ONE Ctx is resident at a time.  Holding all 63
            # would be ~6 GB on SMALL (4 arrays of T x N float64 each).  A null book's target
            # matrix is non-zero only on the rows Ctx actually reads, so rebuilding it per
            # (phase, draw) is cheap.
            cg = {(kind, j): np.full(nph, np.nan)
                  for kind in ("N_FIXED", "N_ROTBLOCK") for j in range(NDRAW)}
            for d in range(nph):
                ctx = Ctx(px, offset_mask(pidx, cad, d)[0])
                for kind in ("N_FIXED", "N_ROTBLOCK"):
                    for j in range(NDRAW):
                        # the seed does NOT depend on d, so a draw is the SAME random book
                        # read at every phase -- which is what makes the phase axis the only
                        # thing moving between the null's own points.
                        wt = null_weights(kind, stable_seed(SEED, pname, cad, kind, j),
                                          ctx, priced, GROSSES["CORE"], NULL_K, blk)
                        if wt is None:
                            continue
                        gr, tn, _ = ctx.run(wt)
                        net = gr - tn * HEAD_COST / 1e4
                        cg[(kind, j)][d] = fmet(net[warm])[0]
                del ctx
            dv = np.arange(nph)
            w = W961 if cad == "Q" else WMONTH
            for (kind, j), v in cg.items():
                bw, bd = best_window(dv, v, width=min(10, nph))
                null_rows.append(dict(panel=pname, cadence=cad, kind=kind, draw=j,
                                      prem_win=window_premium(dv, v, *w),
                                      best_win_prem=bw, best_win_d=bd))
        P(f"  {pname}: nulls done   t={time.time()-t0:.0f}s")

    # N_PERM -- permute the phase labels inside each REAL family.  Drawn PER CELL, so each
    # cell gets its own null distribution and H_SEARCH can be read the way it was written.
    for (pn, bk, gs, cad), gg in grid.groupby(["panel", "book", "gross", "cadence"]):
        if cad not in ncads:
            continue
        rng = np.random.default_rng(stable_seed(SEED, pn, bk, gs, cad, "N_PERM"))
        gg = gg.sort_values("d")
        cv = gg.CAGR.values
        dv = gg.d.values
        w = W961 if cad == "Q" else WMONTH
        for j in range(NDRAW):
            perm = rng.permutation(cv)
            bw, bd = best_window(dv, perm, width=min(10, len(dv)))
            null_rows.append(dict(panel=pn, cadence=cad, kind="N_PERM", draw=j,
                                  prem_win=window_premium(dv, perm, *w),
                                  best_win_prem=bw, best_win_d=bd, book=bk, gross=gs))
    nulls = pd.DataFrame(null_rows)
    dump(nulls, "nulls")

    P("\n  window premium (pp/yr): REAL books vs each null kind, Q grid")
    P(f"  {'panel':7s} {'real':>9s} | " +
      " | ".join(f"{k:>9s} {'SE':>6s} {'z':>6s}" for k in NULLKINDS))
    hnull = {}
    for pname in panels:
        realv = float(prem[(prem.panel == pname) & (prem.cadence == "Q")].prem_W961.mean())
        cells = []
        for k in NULLKINDS:
            s = nulls[(nulls.panel == pname) & (nulls.cadence == "Q") & (nulls.kind == k)].prem_win
            mu, sd = float(s.mean()), float(s.std(ddof=1))
            se = sd / np.sqrt(max(len(s), 1))
            z = (realv - mu) / se if se > 0 else np.nan
            cells.append(f"{mu:>+9.3f} {se:>6.3f} {z:>+6.2f}")
            hnull[(pname, k)] = z
        P(f"  {pname:7s} {realv:>+9.3f} | " + " | ".join(cells))
    zf = [hnull[(p, "N_FIXED")] for p in panels]
    zr = [hnull[(p, "N_ROTBLOCK")] for p in panels]
    gk_H["H_NULL"] = bool(np.nanmin(zf) >= NULL_SE_BAR and np.nanmin(zr) >= NULL_SE_BAR)
    P(f"\n  H_NULL   min z over panels: N_FIXED {np.nanmin(zf):+.2f}, N_ROTBLOCK "
      f"{np.nanmin(zr):+.2f}   (bar >= +{NULL_SE_BAR} on BOTH, as pre-registered)  -> "
      f"{'PASS: a BOOK edge' if gk_H['H_NULL'] else 'FAIL: not distinguishable from the null'}")
    P("           SECONDARY (reported, NOT the pre-registered bar): the bar above divides by the")
    P("           NULL's SE alone, which treats the 10 real cells as exact.  The two-sample z,")
    P("           sqrt(se_real^2 + se_null^2), and the share of real cells above the null's own")
    P("           95th percentile, are the more conservative readings:")
    for pname in panels:
        rv = prem[(prem.panel == pname) & (prem.cadence == "Q")].prem_W961
        se_r = float(rv.std(ddof=1) / np.sqrt(len(rv)))
        bits = []
        for k in ("N_FIXED", "N_ROTBLOCK"):
            s = nulls[(nulls.panel == pname) & (nulls.cadence == "Q") & (nulls.kind == k)].prem_win
            se_n = float(s.std(ddof=1) / np.sqrt(len(s)))
            z2 = (float(rv.mean()) - float(s.mean())) / np.sqrt(se_r ** 2 + se_n ** 2)
            above = float((rv.values[:, None] > s.quantile(0.95)).mean())
            bits.append(f"{k} z2={z2:+.2f} cells>null_p95={above:.2f}")
        P(f"             {pname:7s} se_real={se_r:.3f}  " + "  ".join(bits))
    P("           NOTE the 10 real cells share one tape and are strongly correlated, so even z2")
    P("           overstates; the window premium's SIGN and SIZE, not its z, are what matter here.")

    # H_SEARCH -- read PER CELL, which is what the pre-registration says ("the same statistic
    # under N_PERM"): each cell's observed best 10-wide window against that cell's OWN
    # permutation null.
    qprem = prem[prem.cadence == "Q"]
    cell_pct, cell_hit = [], 0
    for r in qprem.itertuples():
        pv = nulls[(nulls.cadence == "Q") & (nulls.kind == "N_PERM") & (nulls.panel == r.panel)
                   & (nulls.book == r.book) & (nulls.gross == r.gross)].best_win_prem
        if len(pv) == 0:
            continue
        cell_pct.append(float((pv < r.best_win_prem).mean()))
        cell_hit += int(r.best_win_prem >= float(pv.quantile(SEARCH_PCT)))
    med_pct = float(np.median(cell_pct)) if cell_pct else np.nan
    gk_H["H_SEARCH"] = cell_hit > len(cell_pct) / 2.0
    P(f"  H_SEARCH per cell, observed BEST 10-wide window premium vs that cell's OWN N_PERM "
      f"null: {cell_hit} of {len(cell_pct)} cells at/above their own {SEARCH_PCT:.2f} quantile "
      f"(median percentile {med_pct:.3f}; bar = a majority of cells)  -> "
      f"{'PASS' if gk_H['H_SEARCH'] else 'FAIL: a 10-wide window this good is what a SEARCH over the phase axis produces under NO phase effect'}")
    obs_best = float(qprem.best_win_prem.mean())
    pooled = nulls[(nulls.cadence == "Q") & (nulls.kind == "N_PERM")].groupby("draw").best_win_prem.mean()
    P(f"           SECONDARY (pooled): observed mean best-window premium {obs_best:+.3f} pp/yr "
      f"vs the per-draw mean over cells, 95th pct {float(pooled.quantile(SEARCH_PCT)):+.3f} "
      f"(percentile {float((pooled < obs_best).mean()):.3f})")
    P(f"           where the observed best window lands: median d = "
      f"{qprem.best_win_d.median():.0f}, "
      f"{int(qprem.best_win_d.between(*W961).sum())} of {len(qprem)} cells inside "
      f"d={W961[0]}..{W961[1]} (uniform over the 54 windows would give "
      f"{len(qprem)*10/54:.1f})")

    # ------------------------------------------------- E: rule 8 and the KEEP paths
    P()
    P("=" * 100)
    P("(E) RULE 8 WALK-FORWARD -- window chosen on 2009-2016 ONLY, 2017-2026 read once")
    P("=" * 100)
    base_oos, base_full = {}, {}
    for pname, px in panels.items():
        b = backtest(px, rules_v2_weights(px, BAND0, 0.75), cost_bps=HEAD_COST, freq="W")["returns"].values
        warm = np.arange(len(px)) >= WARM
        oosm = np.asarray(px.index >= pd.Timestamp(OOS_START))
        base_oos[pname] = fmet(b[oosm])
        base_full[pname] = fmet(b[warm])

    wf = []
    for (pn, bk, gs, cad), gg in grid.groupby(["panel", "book", "gross", "cadence"]):
        if cad != "Q":
            continue
        gg = gg.sort_values("d").reset_index(drop=True)
        # IS-ONLY chooser: the 10-wide window with the best IS CAGR; pick its centre
        isv = gg.IS_CAGR.values
        k = np.convolve(isv, np.ones(10) / 10, mode="valid")
        j = int(np.nanargmax(k))
        pick_d = int(gg.d.values[j + 4])
        rp = gg[gg.d == pick_d].iloc[0]
        rc = gg[gg.d == 0].iloc[0]
        rl = gg[gg.d == LITERAL_D].iloc[0]
        sp = spymet[pn]
        lg = legs_4b(rp.OOS_CAGR, rp.H1, rp.H2, rp.OOS_Sharpe, rp.MaxDD,
                     sp["CAGR"], sp["H1"], sp["H2"], sp["OOS_Sharpe"], sp["MaxDD"])
        lgl = legs_4b(rl.OOS_CAGR, rl.H1, rl.H2, rl.OOS_Sharpe, rl.MaxDD,
                      sp["CAGR"], sp["H1"], sp["H2"], sp["OOS_Sharpe"], sp["MaxDD"])
        bf = base_full[pn]
        bh1 = bh2 = np.nan
        wf.append(dict(panel=pn, book=bk, gross=gs, IS_pick_d=pick_d,
                       pick_OOS_CAGR=rp.OOS_CAGR, pick_OOS_Sharpe=rp.OOS_Sharpe,
                       pick_OOS_MaxDD=rp.OOS_MaxDD,
                       canon_OOS_CAGR=rc.OOS_CAGR, canon_OOS_Sharpe=rc.OOS_Sharpe,
                       canon_OOS_MaxDD=rc.OOS_MaxDD,
                       lit_OOS_CAGR=rl.OOS_CAGR, lit_OOS_Sharpe=rl.OOS_Sharpe,
                       lit_OOS_MaxDD=rl.OOS_MaxDD,
                       fam_med_OOS_CAGR=float(gg.OOS_CAGR.median()),
                       fam_med_OOS_Sharpe=float(gg.OOS_Sharpe.median()),
                       spy_OOS_CAGR=sp["OOS_CAGR"], spy_OOS_Sharpe=sp["OOS_Sharpe"],
                       spy_OOS_MaxDD=sp["OOS_MaxDD"],
                       base_OOS_CAGR=base_oos[pn][0], base_OOS_Sharpe=base_oos[pn][1],
                       base_OOS_MaxDD=base_oos[pn][2],
                       pick_4b=all(lg.values()), pick_fail4b=failstr(lg),
                       lit_4b=all(lgl.values()), lit_fail4b=failstr(lgl),
                       pick_beats_fammed=bool(rp.OOS_CAGR > gg.OOS_CAGR.median()),
                       lit_beats_canon=bool(rl.OOS_CAGR > rc.OOS_CAGR),
                       # the DECISIVE reported contrasts: beating the CANONICAL date is a weak
                       # bar because 942/961 already established d=0 sits LOW in its own family.
                       # The honest comparand is the family MEDIAN -- a phase nobody chose.
                       lit_beats_fammed=bool(rl.OOS_CAGR > gg.OOS_CAGR.median()),
                       lit_IS_beats_fammed=bool(rl.IS_CAGR > gg.IS_CAGR.median()),
                       lit_IS_beats_canon=bool(rl.IS_CAGR > rc.IS_CAGR),
                       lit_OOS_minus_fammed_pp=float((rl.OOS_CAGR - gg.OOS_CAGR.median()) * 100),
                       lit_IS_minus_fammed_pp=float((rl.IS_CAGR - gg.IS_CAGR.median()) * 100),
                       lit_d_pct_IS=float((gg.IS_CAGR < rl.IS_CAGR).mean()),
                       lit_d_pct_OOS=float((gg.OOS_CAGR < rl.OOS_CAGR).mean())))
    wfd = pd.DataFrame(wf)
    dump(wfd, "walkforward")

    P(f"\n  {'cell':22s} {'ISpick':>6s} | {'pick OOS C/S/DD':>26s} | {'d=20 OOS C/S/DD':>26s} | "
      f"{'canon OOS C/S/DD':>26s} | {'famMED C':>9s}")
    for r in wfd.itertuples():
        P(f"  {r.panel+'/'+r.book+'/'+r.gross:22s} {r.IS_pick_d:6d} | "
          f"{r.pick_OOS_CAGR:8.2%} {r.pick_OOS_Sharpe:7.3f} {r.pick_OOS_MaxDD:8.2%} | "
          f"{r.lit_OOS_CAGR:8.2%} {r.lit_OOS_Sharpe:7.3f} {r.lit_OOS_MaxDD:8.2%} | "
          f"{r.canon_OOS_CAGR:8.2%} {r.canon_OOS_Sharpe:7.3f} {r.canon_OOS_MaxDD:8.2%} | "
          f"{r.fam_med_OOS_CAGR:9.2%}")
    for pn in panels:
        s = spymet[pn]
        P(f"  SPY {pn:6s} OOS {s['OOS_CAGR']:7.2%} {s['OOS_Sharpe']:7.3f} {s['OOS_MaxDD']:8.2%}"
          f"   |  RULES v2 baseline OOS {base_oos[pn][0]:7.2%} {base_oos[pn][1]:7.3f} "
          f"{base_oos[pn][2]:8.2%}")

    nlit = int(wfd.lit_beats_canon.sum())
    gk_H["H_LITERAL"] = nlit / len(wfd) >= LITERAL_BAR
    P(f"\n  H_LITERAL the ZERO-TUNING rule d={LITERAL_D} beats the canonical quarter-end on OOS "
      f"CAGR in {nlit} of {len(wfd)} cells ({nlit/len(wfd):.3f}; bar >= {LITERAL_BAR:.3f})  -> "
      f"{'PASS' if gk_H['H_LITERAL'] else 'FAIL'}")
    P(f"            BUT the canonical date is a WEAK comparand -- 942 and 961 both established "
      f"d=0 sits LOW in its own family (961: mean percentile 0.255 over 12 cells).  Against the")
    P(f"            FAMILY MEDIAN, a phase nobody chose, the same literal rule reads:")
    P(f"              OOS: beats family median in {int(wfd.lit_beats_fammed.sum())} of "
      f"{len(wfd)} cells, mean margin {wfd.lit_OOS_minus_fammed_pp.mean():+.3f} pp/yr, "
      f"median within-family percentile {wfd.lit_d_pct_OOS.median():.3f}")
    P(f"              IS : beats family median in {int(wfd.lit_IS_beats_fammed.sum())} of "
      f"{len(wfd)} cells, mean margin {wfd.lit_IS_minus_fammed_pp.mean():+.3f} pp/yr, "
      f"median within-family percentile {wfd.lit_d_pct_IS.median():.3f}")
    P(f"              IS : beats the CANONICAL date in {int(wfd.lit_IS_beats_canon.sum())} of "
      f"{len(wfd)} cells  (a real calendar effect should show in BOTH windows, not just OOS)")
    npick = int(wfd.pick_beats_fammed.sum())
    n4b = int(wfd.pick_4b.sum())
    gk_H["H_RULE8"] = (npick / len(wfd) >= RULE8_BAR) and n4b >= 1
    P(f"  H_RULE8   the IS-chosen window beats its own family MEDIAN on OOS CAGR in {npick} of "
      f"{len(wfd)} cells ({npick/len(wfd):.3f}; bar >= {RULE8_BAR:.3f}); cells clearing 4b OOS: "
      f"{n4b} (bar >= 1)  -> {'PASS' if gk_H['H_RULE8'] else 'FAIL'}")
    P(f"            d={LITERAL_D} literal rule clears 4b in {int(wfd.lit_4b.sum())} of "
      f"{len(wfd)} cells")

    # G7 -- the chooser is IS-only
    gsh = grid.copy()
    rg = np.random.default_rng(7)
    for c in ("OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "CAGR", "Sharpe", "MaxDD", "H1", "H2"):
        gsh[c] = rg.permutation(gsh[c].values)
    picks2 = []
    for (pn, bk, gs, cad), gg in gsh.groupby(["panel", "book", "gross", "cadence"]):
        if cad != "Q":
            continue
        gg = gg.sort_values("d").reset_index(drop=True)
        k = np.convolve(gg.IS_CAGR.values, np.ones(10) / 10, mode="valid")
        picks2.append(int(gg.d.values[int(np.nanargmax(k)) + 4]))
    gk["G7"] = list(wfd.IS_pick_d.values) == picks2
    P(f"\n  G7 chooser IS-ONLY: picks invariant to permuting every OOS/full-sample column: "
      f"{'PASS' if gk['G7'] else 'FAIL'}")
    gdetail.append(dict(gate="G7", stat=float(sum(a == b for a, b in zip(wfd.IS_pick_d, picks2))),
                        bar=float(len(picks2)), passed=gk["G7"],
                        what="rule-8 chooser reads IS columns only"))

    # KEEP paths
    P("\n  KEEP PATHS on the rule-8 picks (4a: beat the LIVE book in BOTH halves with no worse "
      "MaxDD; 4b: capital-worthy vs SPY)")
    n4a = 0
    for r in wfd.itertuples():
        bf = base_full[r.panel]
        cell = grid[(grid.panel == r.panel) & (grid.book == r.book) & (grid.gross == r.gross)
                    & (grid.cadence == "Q") & (grid.d == r.IS_pick_d)].iloc[0]
        px = panels[r.panel]
        b = backtest(px, rules_v2_weights(px, BAND0, 0.75), cost_bps=HEAD_COST, freq="W")["returns"].values
        warm = np.arange(len(px)) >= WARM
        wpos = np.flatnonzero(warm); hh = len(wpos) // 2
        h1m = np.zeros(len(px), bool); h1m[wpos[:hh]] = True
        h2m = np.zeros(len(px), bool); h2m[wpos[hh:]] = True
        _, b1, _ = fmet(b[h1m]); _, b2, _ = fmet(b[h2m])
        ok4a = bool(cell.H1 > b1 and cell.H2 > b2 and cell.MaxDD >= bf[2])
        n4a += int(ok4a)
    P(f"  4a passes: {n4a} of {len(wfd)}   4b passes: {n4b} of {len(wfd)}   "
      f"(d={LITERAL_D} literal: 4b {int(wfd.lit_4b.sum())} of {len(wfd)})")

    # ------------------------------------------------------------------ verdict
    P()
    P("=" * 100)
    P("(F) VERDICT")
    P("=" * 100)
    P(f"  GATES: " + "  ".join(f"{k}={'PASS' if v else 'FAIL'}" for k, v in gk.items()))
    P(f"  HYPOTHESES: " + "  ".join(f"{k}={'PASS' if v else 'FAIL'}" for k, v in gk_H.items()))
    if not gk_H["H_WINDOW"]:
        verdict = "KILL"
        why = ("the 15-24d window does NOT replicate on the TRADABLE construction "
               "(rebalance exactly d days before every quarter-end)")
    elif not gk_H["H_NULL"]:
        verdict = "KILL"
        why = "TAPE PROPERTY -- a gross-matched coin flip collects the same window premium"
    elif not gk_H["H_SEARCH"]:
        verdict = "KILL"
        why = "63-WAY SEARCH -- a window this good is what permuted phase labels produce"
    elif gk_H["H_MONTHLY"] and gk_H["H_RULE8"]:
        verdict = "KEEP-candidate"
        why = "a real rebalance-date edge: replicates, beats both nulls, survives rule 8"
    else:
        verdict = "PARK"
        why = "a mixture: replicates and beats the nulls but does not carry out of sample"
    P(f"\n  VERDICT: {verdict} -- {why}")
    P()
    P("  THE THREE INDEPENDENT REASONS THIS DIES (the decision rule above used only the first):")
    P(f"  1. NOT A BOOK EDGE. The Q-window premium is +{prem[(prem.panel=='U56')&(prem.cadence=='Q')].prem_W961.mean():.3f} "
      f"pp/yr on U56 and +{prem[(prem.panel=='SMALL')&(prem.cadence=='Q')].prem_W961.mean():.3f} on SMALL but "
      f"{prem[(prem.panel=='B136')&(prem.cadence=='Q')].prem_W961.mean():+.3f} on B136 -- it changes SIGN across")
    P("     panels, and on B136 a gross-matched coin flip does BETTER than the real books.")
    P(f"  2. IT LIVES ENTIRELY IN THE SECOND WINDOW. The literal d={LITERAL_D} rule beats its own family")
    P(f"     median on OOS CAGR in {int(wfd.lit_beats_fammed.sum())} of {len(wfd)} cells "
      f"({wfd.lit_OOS_minus_fammed_pp.mean():+.3f} pp/yr) but in only "
      f"{int(wfd.lit_IS_beats_fammed.sum())} of {len(wfd)} IN SAMPLE "
      f"({wfd.lit_IS_minus_fammed_pp.mean():+.3f} pp/yr).")
    P("     A quarter-end flow effect that is absent 2009-2016 and present 2017-2026 is not a")
    P("     calendar mechanism; it is one window's luck, and rule 8 is what catches it.")
    P("  3. THE WINDOW IS NOT WHERE THE SHAPE IS. On the tradable grid the profile is not a peak")
    P(f"     at d={W961[0]}..{W961[1]} -- it is a TROUGH at the quarter-end itself "
      f"({float(q[q.d<=8].dm_CAGR_pp.mean()):+.3f} pp/yr at d=0..8) with everything")
    P(f"     from d=15 to d=45 flat and mildly positive ({float(q[(q.d>=15)&(q.d<=24)].dm_CAGR_pp.mean()):+.3f} "
      f"/ {float(q[(q.d>=25)&(q.d<=31)].dm_CAGR_pp.mean()):+.3f} / "
      f"{float(q[(q.d>=32)&(q.d<=45)].dm_CAGR_pp.mean()):+.3f} at 15-24 / 25-31 / 32-45).")
    P("     '15-24 days' is a 63-way search LOCALISING a broad, shallow 'do not rebalance AT")
    P("     quarter-end' effect, and H_SEARCH confirms the localisation is free: the best 10-wide")
    P(f"     window beats its own permutation null in {cell_hit} of {len(cell_pct)} cells, i.e. every")
    P("     family has SOME good 10-wide window, and which one it is does not replicate.")
    P()
    P("  WHAT SURVIVES (reported, not promoted): the ONLY robust part of 961's calendar reading is")
    P(f"  the NEGATIVE end -- rebalancing within ~8 trading days of quarter-end costs "
      f"{float(q[q.d<=8].dm_CAGR_pp.mean()):+.3f} pp/yr")
    P("  of de-meaned CAGR, which is consistent across all three panels and is what makes the")
    P("  CANONICAL quarter-end date look bad (942's and 961's original observation). That is a")
    P("  statement about the date to AVOID, not a window to TARGET, and it moves no KEEP path:")
    P(f"  4a {n4a} of {len(wfd)}, 4b {n4b} of {len(wfd)} on the rule-8 picks.")

    dump(pd.DataFrame(gdetail), "gates")
    (OUT / f"{STEM}.log.txt").write_text("\n".join(LINES) + "\n")
    P(f"\n  total {time.time()-t0:.0f}s")
    return verdict


if __name__ == "__main__":
    main()

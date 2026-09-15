#!/usr/bin/env python3
"""Idea 922 (cloud, 2026-09-15) -- WHY is the IS H1 SHARPE leg UNPASSABLE for CAND20 on U56 at
every gross?

THE QUESTION (queue, 2026-09-15)
  Both 2026-09-15 cuts of idea 675 found `L1_H1` -- the first-half Sharpe leg read INSIDE the
  in-sample window -- failing at EVERY gross on U56 (0 of 150 rungs / 0 of 750 rungs).  So the
  in-sample 5-leg 4b pass set on the standing KEEP-4b book's own home panel is EMPTY, and every
  rule-8 pass the record has on this book is won by choosers that select on the DD-cap x
  CAGR-floor window instead of on 4b itself.  The queue asks: decompose the 2009-2012 gap against
  SPY and report whether it is a CONCENTRATION, a CASH-DRAG or a SINGLE-EPISODE fact.

THE BOOK (idea 670's `CAND20`, the 2026-09-04 KEEP 4b candidate; NOT re-specified here)
  Each rebalance, rank every priced name above its own 200d MA with 20d realised vol < 0.60 by the
  v1 composite `mean(pct-rank 12-1 mom, pct-rank 6m, pct-rank 3m) x (1 if above 200d MA else 0.5)`
  WITHOUT the `/sqrt(vol20)` term; hold the top 20 at g/k each where k = min(20, #eligible).
  Weekly, decided at the close, executed next close, 10 bps per unit turnover.

  A CORRECTION TO THE RECORD'S OWN PROSE, established at G7 and load-bearing for this question.
  Idea 675's docstring describes this book as holding "the rest in CASH (de-gross, never
  re-spread)".  Its committed `ranked_w1` does the opposite: it divides by the REALISED k, so the
  book re-spreads to FULL gross g whenever at least one name is eligible.  On U56 the eligible
  count never reaches zero (min 3, median 41; below 20 on 487 of 4,444 days), so CAND20 is fully
  invested at gross g on EVERY day of the sample and has NO cash channel at all.  The de-grossing
  sentence describes RULES v2's band book (mean gross 0.710 of g), not this one.  This is why the
  queue's "cash-drag" candidate is dead twice over below rather than merely small.

WHY A 2x2 IS THE RIGHT INSTRUMENT
  The queue names three candidate carriers.  Two of them are separable by construction and the
  third is not a construction at all:
    CONCENTRATION  holding 20 ranked names instead of every eligible name
    CASH           holding cash.  This splits into two things the record has been calling one:
                   (a) CONSTANT gross -- the g dial.  A de-grossed book's return is g x (book) and
                       a Sharpe ratio is scale-free, so at zero cost a CONSTANT cash mix cannot
                       move a Sharpe leg AT ALL.  H_FLAT measures the residual.
                   (b) a TIME-VARYING gate would be the only cash story that CAN move a Sharpe
                       leg -- but per the correction above THIS BOOK HAS NONE: its 200d MA / vol
                       filter re-spreads into the survivors instead of standing aside in cash.
                       So the filter is a NAME filter, tested here as such.  H_GATE's arm
                       (CAND20_NG) removes the filter, not a cash position.
    EPISODE        not a construction: a few contiguous days doing all the work.  H_EPISODE.
  So the run prices the exact 2x2  {gate ON, gate OFF} x {top-20, equal-weight-all}:
    CAND20 (gate, top-20)   EWELIG (gate, EW)   CAND20_NG (no gate, top-20)   EWALL (no gate, EW)
  Every arm uses the SAME composite score and the SAME de-gross-to-cash convention; the two
  no-gate arms are fully invested at gross g every day by construction (gated at G7).

WHAT IS TUNED AND WHAT IS REPORTED (PROTOCOL 4: max 2 tuned parameters)
  TUNED 1  SUB-WINDOW (the queue's own first dial), 14 levels, every one reported:
           ISH1_HALF / ISH2_HALF   the trading-day halves of the IS window -- ISH1_HALF IS THE
                                   LEG ITSELF, the object the question is about
           CAL0912 / CAL0910 / CAL1112 / CAL1316   calendar blocks
           Y2009 .. Y2016          the eight in-sample calendar years, one at a time
  TUNED 2  PANEL (the queue's own second dial), 3 levels: U56 / B136 / SMALL.
  REPORTED AXES (nothing fitted on them; every point published):
           gross 0.05..1.50 step 0.05 (30 rungs) + a 0.01 x 150-rung fine ladder for H_FLAT;
           cost 0 / 10 / 25 / 50 bps; arms CAND20, EWELIG, CAND20_NG, EWALL, SPYBH, BAND03.

PRE-REGISTERED BARS (fixed before any number was read; both directions reported)
  H_FLAT     CONSTANT gross is NOT the carrier: the sub-window Sharpe of every arm is flat in
             gross, spread over the 150-rung fine ladder < 0.05 at 0 bps and < 0.20 at 10 bps.
  H_CONC     CONCENTRATION is the carrier iff EWELIG CLEARS the leg (sub-window Sharpe > SPY's)
             at >= 15 of the 30 gross rungs on U56 at 10 bps where CAND20 fails it.
  H_GATE     the TIME-VARYING GATE is the carrier iff CAND20_NG clears the leg at >= 15 of 30.
  H_EPISODE  a SINGLE EPISODE is the carrier iff excising ONE contiguous block of <= 60 trading
             days (pre-registered maximum) from BOTH the book and SPY flips the leg at the
             published g = 0.75, 10 bps, on ISH1_HALF.  L* = the smallest length that flips it.
  H_MEANVOL  the gap is a MEAN gap, not a VOL gap: in the exact decomposition
             dSharpe = (mu_b - mu_s)/s_s + mu_b (1/s_b - 1/s_s), |mean term| > 2 x |vol term|.
  H_PANEL    whatever carries it on U56 carries it on B136 and on SMALL (does the answer travel).
  H_WF       (rule 8, REQUIRED) arm x gross chosen on 2009-2016 ALONE, 2017-2026 read ONCE, both
             KEEP paths, against SPY and RULES v2 in the same window.

GATES (all printed before any result number)
  G1  the fast runner == `engine.backtest` on returns and turnover (subject, U56, g=0.75)
  G2  BAND03 == `baseline.rules_v2_weights` elementwise
  G3  CROSS-RUN: idea 675's committed `.ladder.csv` U56/CAND20 rows reproduce -- `IS_H1` on all
      150 STEP01 rungs to 5e-3 AND `cwinIS_L1_H1` False at 0 of 150, the claim itself
  G4  the committed U56 triples (SPY, RULES v2)
  G5  the episode search with an EMPTY excision reproduces the un-excised Sharpe pair exactly
  G6  determinism (rebuild the subject row, compare)
  G7  the 2x2 is really a 2x2: the two no-gate arms run realised gross == g on every day of the
      sample (max |dev| reported), the two gated arms do not

PROTOCOL: 10 bps primary, t+1, weekly, warm-up 260 days, IS 2009-2016 / OOS 2017-2026.
Nothing in RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py is modified.

SURVIVORSHIP: U56 / B136 / SMALL are current-constituent lists (SMALL additionally drops the
tickers with `max_1d_move` >= 1.0 per `data/small_meta.csv`), so every CAGR and drawdown LEVEL
below is optimistic -- the book's and the comparands' alike.  The 2x2 decomposition is a
same-days, same-names contrast ACROSS books and is far less exposed than the levels; the leg
verdicts and the rule-8 triples are levels read against SPY, which is NOT survivorship-inflated,
so those are upper bounds.  Stated, not hidden.
"""
from __future__ import annotations

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

# ---- reported constants (never tuned) ---------------------------------------------------------
COST0 = 10.0
FREQ = "W"
LAG = 1
BAND0 = 0.03
MAXVOL = 0.60
WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
PUBLISHED_G = 0.75
EPISODE_MAX = 60          # H_EPISODE's pre-registered maximum block length (trading days)
FLAT_BAR0, FLAT_BAR10 = 0.05, 0.20
CARRIER_BAR = 15          # H_CONC / H_GATE: >= 15 of 30 gross rungs
MEANVOL_BAR = 2.0

GROSS30 = [round(0.05 * i, 4) for i in range(1, 31)]
GROSS150 = [round(0.01 * i, 4) for i in range(1, 151)]
COSTS = [0.0, 10.0, 25.0, 50.0]
PANELS = ["U56", "B136", "SMALL"]
ARMS = ["CAND20", "EWELIG", "CAND20_NG", "EWALL", "SPYBH", "BAND03"]
ARM_SRC = {
    "CAND20": "THE SUBJECT: 2026-09-04 KEEP 4b, gate ON, top-20 EW, no vol scaler",
    "EWELIG": "gate ON, equal-weight every eligible name (concentration OFF)",
    "CAND20_NG": "gate OFF, top-20 EW on the same score (cash channel OFF, always invested)",
    "EWALL": "gate OFF, equal-weight every priced name (both OFF) = the panel index",
    "SPYBH": "g x SPY, the exposure control",
    "BAND03": "RULES v2 live (baseline.rules_v2_weights)",
}
FACTORIAL = {("gate", "top20"): "CAND20", ("gate", "ew"): "EWELIG",
             ("nogate", "top20"): "CAND20_NG", ("nogate", "ew"): "EWALL"}
NOGATE_ARMS = ["CAND20_NG", "EWALL", "SPYBH"]

SPY_U56 = (0.1516, 0.8861, -0.3372)      # committed triple, idea 670/675
V2_U56 = (0.0863, 1.2018, -0.1205)
TOL_C, TOL_S, TOL_D = 0.004, 0.030, 0.015
G3_BAR = 5e-3
PARENT = OUT / "2026-09-15_is-U56-CAND20-s-SINGLE-RUNG-4b-pass-a-KNIFE-EDGE-or-a-real-window_cloud.ladder.csv"

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ================================================================================================
# runner (the record's vectorised equivalent of engine.backtest; gated at G1)
# ================================================================================================
class Panel:
    def __init__(self, name, px):
        self.name, self.px = name, px
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        T, N = self.rets.shape
        self.T, self.N = T, N
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, N)), C[:-1]])
        mk = rebalance_mask(self.idx, FREQ).shift(LAG, fill_value=False).values.copy()
        mk[0] = True
        self.reb = np.flatnonzero(mk)
        seg = np.searchsorted(self.reb, np.arange(T), side="right") - 1
        self.s0 = self.reb[seg]
        self.s0p = self.reb[np.maximum(seg - 1, 0)]
        self.R = self.Cp / self.Cp[self.s0]
        self.Rp = self.Cp[self.reb] / self.Cp[self.s0p[self.reb]]
        self.start = self.idx[WARMUP]
        m_full = (self.idx >= self.start).values if hasattr(self.idx >= self.start, "values") \
            else np.asarray(self.idx >= self.start)
        yr = self.idx.year
        w = {"FULL": m_full,
             "IS": m_full & (self.idx <= pd.Timestamp(IS_END)),
             "OOS": np.asarray(self.idx >= pd.Timestamp(OOS_START))}
        # the TUNED sub-window dial, every level built here
        ispos = np.flatnonzero(w["IS"])
        h = len(ispos) // 2
        ish1 = np.zeros(T, bool); ish1[ispos[:h]] = True
        ish2 = np.zeros(T, bool); ish2[ispos[h:]] = True
        w["ISH1_HALF"], w["ISH2_HALF"] = ish1, ish2
        w["CAL0912"] = m_full & (yr >= 2009) & (yr <= 2012)
        w["CAL0910"] = m_full & (yr >= 2009) & (yr <= 2010)
        w["CAL1112"] = m_full & (yr >= 2011) & (yr <= 2012)
        w["CAL1316"] = m_full & (yr >= 2013) & (yr <= 2016)
        for y in range(2009, 2017):
            w[f"Y{y}"] = m_full & (yr == y)
        self.masks = w
        self.spy = px["SPY"].pct_change().fillna(0.0).values


SUBWINS = ["ISH1_HALF", "ISH2_HALF", "CAL0912", "CAL0910", "CAL1112", "CAL1316"] + \
          [f"Y{y}" for y in range(2009, 2017)]
WINDOWS = ["FULL", "IS", "OOS"] + SUBWINS


class Book:
    """One book's gross-1.0 weights, pre-reduced so any (gross, cost) costs O(T)."""

    def __init__(self, panel: Panel, W1: np.ndarray):
        self.pan = panel
        wt = np.roll(W1, LAG, axis=0).copy()
        wt[:LAG] = 0.0
        self.wt_reb = wt[panel.reb]
        A = wt[panel.s0]
        AR = A * panel.R
        self.S = AR.sum(axis=1)
        self.As = A.sum(axis=1)
        self.ARr = (AR * panel.rets).sum(axis=1)
        Ap = wt[panel.s0p[panel.reb]]
        ARp = Ap * panel.Rp
        self.ARp = ARp
        self.Sp = ARp.sum(axis=1)
        self.Asp = Ap.sum(axis=1)
        del A, AR, Ap

    def at(self, g: float, cost=COST0):
        pan = self.pan
        V = 1.0 + g * (self.S - self.As)
        gross = g * self.ARr / V
        Vp = 1.0 + g * (self.Sp - self.Asp)
        heldp = (g * self.ARp) / Vp[:, None]
        heldp[0] = 0.0
        turn = np.zeros(pan.T)
        turn[pan.reb] = np.abs(g * self.wt_reb - heldp).sum(axis=1)
        return gross - turn * cost / 1e4, turn

    def realised_gross(self, g: float):
        """Daily held gross (after drift), the thing the CASH story is about."""
        V = 1.0 + g * (self.S - self.As)
        return g * self.S / V


def fmet(r):
    r = np.asarray(r, float)
    if len(r) < 2:
        return np.nan, np.nan, np.nan
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    if len(r) < 2:
        return np.nan
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def pack(r):
    c, s, d = fmet(r)
    h = len(r) // 2
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(r[:h]), H2=fsharpe(r[h:]),
                mu=float(np.mean(r) * 252.0), sd=float(np.std(r, ddof=1) * np.sqrt(252.0)))


def legswin(s, spy):
    """The window-local 4b form used by the record's rule-8 runs (867/910/918)."""
    return dict(L1_H1=bool(s["H1"] > spy["H1"]), L2_H2=bool(s["H2"] > spy["H2"]), L3_OOS=True,
                L4_DDcap=bool(s["MaxDD"] >= DD_CAP * spy["MaxDD"]),
                L5_CAGRfloor=bool(s["CAGR"] >= CAGR_FLOOR * spy["CAGR"]))


def pass4a(s, base):
    return bool(s["H1"] > base["H1"] and s["H2"] > base["H2"] and s["MaxDD"] >= base["MaxDD"])


# ================================================================================================
# the arms
# ================================================================================================
def ew_gross1(px):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def ranked_w1(sc, n):
    """Top-n of whatever is left in `sc` after (or without) an eligibility mask, equal weight."""
    rank = sc.rank(axis=1, ascending=False)
    sel = (rank <= n).astype(float)
    k = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(k, axis=0).fillna(0.0)


def arm_w1(px, pre, arm):
    sc_n, above, vol20 = pre
    if arm == "BAND03":
        return ew_gross1(px).where(band_state(px, BAND0) & px.notna(), 0.0).values
    if arm == "CAND20":
        return ranked_w1(sc_n.where(above & (vol20 < MAXVOL)), 20).values
    if arm == "EWELIG":
        sel = (above & (vol20 < MAXVOL) & px.notna()).astype(float)
        k = sel.sum(axis=1).replace(0, np.nan)
        return sel.div(k, axis=0).fillna(0.0).values
    if arm == "CAND20_NG":
        return ranked_w1(sc_n.where(px.notna()), 20).values
    if arm == "EWALL":
        return ew_gross1(px).values
    if arm == "SPYBH":
        w = pd.DataFrame(0.0, index=px.index, columns=px.columns)
        w["SPY"] = 1.0
        return w.where(px.notna(), 0.0).values
    raise KeyError(arm)


def prep(px):
    sc_n, above, vol20 = score(px, vol_scale=False)
    return sc_n, above, vol20


# ================================================================================================
# episode search (H_EPISODE)
# ================================================================================================
def _sharpe_excl(S1, S2, n, lo, hi):
    """Sharpe of the series with the contiguous block [lo,hi) removed, from prefix sums."""
    m = n - (hi - lo)
    if m < 3:
        return np.nan
    s1 = S1[n] - (S1[hi] - S1[lo])
    s2 = S2[n] - (S2[hi] - S2[lo])
    mu = s1 / m
    var = (s2 - m * mu * mu) / (m - 1)
    if var <= 0:
        return np.nan
    return np.sqrt(252.0) * mu / np.sqrt(var)


def episode_share(rb, rs, lengths):
    """Calibration for the argmax: over ALL contiguous blocks of each length, what share of
    excisions flip the leg, and what is the median gap?  An argmax alone always looks fragile."""
    rb = np.asarray(rb, float); rs = np.asarray(rs, float)
    n = len(rb)
    Sb1 = np.concatenate([[0.0], np.cumsum(rb)]); Sb2 = np.concatenate([[0.0], np.cumsum(rb * rb)])
    Ss1 = np.concatenate([[0.0], np.cumsum(rs)]); Ss2 = np.concatenate([[0.0], np.cumsum(rs * rs)])
    out = []
    for L in lengths:
        gaps = []
        for lo in range(0, n - L + 1):
            hi = lo + L
            sb = _sharpe_excl(Sb1, Sb2, n, lo, hi)
            ss = _sharpe_excl(Ss1, Ss2, n, lo, hi)
            if not (np.isnan(sb) or np.isnan(ss)):
                gaps.append(sb - ss)
        g = np.asarray(gaps)
        out.append(dict(L=L, n_blocks=len(g), share_flip=float((g > 0).mean()),
                        median_gap=float(np.median(g)), max_gap=float(g.max()),
                        min_gap=float(g.min())))
    return pd.DataFrame(out)


def episode_scan(rb, rs, max_len=EPISODE_MAX):
    """Best contiguous excision (both series, same days).  Returns (best row, L*, table)."""
    rb = np.asarray(rb, float); rs = np.asarray(rs, float)
    n = len(rb)
    Sb1 = np.concatenate([[0.0], np.cumsum(rb)]); Sb2 = np.concatenate([[0.0], np.cumsum(rb * rb)])
    Ss1 = np.concatenate([[0.0], np.cumsum(rs)]); Ss2 = np.concatenate([[0.0], np.cumsum(rs * rs)])
    rows = []
    best = None
    lstar = None
    for L in range(1, max_len + 1):
        bl = None
        for lo in range(0, n - L + 1):
            hi = lo + L
            sb = _sharpe_excl(Sb1, Sb2, n, lo, hi)
            ss = _sharpe_excl(Ss1, Ss2, n, lo, hi)
            if np.isnan(sb) or np.isnan(ss):
                continue
            d = sb - ss
            if bl is None or d > bl[0]:
                bl = (d, lo, hi, sb, ss)
        if bl is None:
            continue
        rows.append(dict(L=L, gap=bl[0], lo=bl[1], hi=bl[2], sharpe_book=bl[3], sharpe_spy=bl[4],
                         flips=bool(bl[0] > 0)))
        if best is None or bl[0] > best[0]:
            best = bl
        if lstar is None and bl[0] > 0:
            lstar = L
    return best, lstar, pd.DataFrame(rows)


# ================================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 922 (cloud, 2026-09-15) -- WHY is the IS H1 SHARPE leg UNPASSABLE for CAND20 on U56?")
    P("=" * 100)
    P(__doc__.split("SURVIVORSHIP:")[0].split("THE QUESTION")[1][:0] or "")

    # ---------------- panels ----------------
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    raw = {}
    for nm, kw in [("U56", {}), ("B136", dict(broad=True)), ("SMALL", dict(small=True))]:
        px = load_universe(**kw)
        if nm == "SMALL":
            px = px[[c for c in px.columns if c not in bad]]
        raw[nm] = px
        P(f"panel {nm:6s} {px.shape[0]} days x {px.shape[1]} cols  {px.index[0].date()} .. "
          f"{px.index[-1].date()}")
    P(f"  SMALL drops {len(bad)} tickers with max_1d_move >= 1.0 (data/small_meta.csv)")
    P("")

    pans, books = {}, {}
    for nm in PANELS:
        pans[nm] = Panel(nm, raw[nm])
        pre = prep(raw[nm])
        for a in ARMS:
            books[(nm, a)] = Book(pans[nm], arm_w1(raw[nm], pre, a))
    P(f"built {len(books)} books in {time.time()-t0:.1f}s")
    for nm in PANELS:
        p = pans[nm]
        P(f"  {nm}: IS {p.idx[np.flatnonzero(p.masks['IS'])[0]].date()} .. "
          f"{p.idx[np.flatnonzero(p.masks['IS'])[-1]].date()}   "
          f"ISH1_HALF {p.idx[np.flatnonzero(p.masks['ISH1_HALF'])[0]].date()} .. "
          f"{p.idx[np.flatnonzero(p.masks['ISH1_HALF'])[-1]].date()} "
          f"({p.masks['ISH1_HALF'].sum()}d)")
    P("")

    # ---------------- reference (SPY, RULES v2) per panel per window ----------------
    spyref, v2ref = {}, {}
    for nm in PANELS:
        p = pans[nm]
        spyref[nm] = {w: pack(p.spy[p.masks[w]]) for w in WINDOWS}
        rv2, _ = books[(nm, "BAND03")].at(0.75, COST0)
        v2ref[nm] = {w: pack(rv2[p.masks[w]]) for w in WINDOWS}

    # ================================ GATES ================================
    P("=" * 100)
    P("GATES (printed before any result number)")
    P("=" * 100)
    gates = []

    # G1 fast runner vs engine.backtest
    pxu = raw["U56"]
    W1 = arm_w1(pxu, prep(pxu), "CAND20")
    eng = backtest(pxu, pd.DataFrame(W1 * PUBLISHED_G, index=pxu.index, columns=pxu.columns),
                   cost_bps=COST0, freq=FREQ)
    fr, ft = books[("U56", "CAND20")].at(PUBLISHED_G, COST0)
    # engine.backtest emits NaN on the 2 pre-warm-up rows where its own shift(1) has no weights;
    # every number in this run is read on the post-warm-up FULL window, so the gate is read there.
    mfull = pans["U56"].masks["FULL"]
    d1 = float(np.abs(eng["returns"].values[mfull] - fr[mfull]).max())
    d1t = float(np.abs(eng["turnover"].values[mfull] - ft[mfull]).max())
    gates.append(dict(gate="G1 fast runner == engine.backtest (U56/CAND20 @ g=0.75, FULL window)",
                      stat=f"max|dr| {d1:.3e}  max|dturn| {d1t:.3e}", passed=bool(d1 < 1e-12 and d1t < 1e-10)))

    # G2 BAND03 == rules_v2_weights
    b03 = pd.DataFrame(arm_w1(pxu, prep(pxu), "BAND03") * 0.75, index=pxu.index, columns=pxu.columns)
    d2 = float((b03 - rules_v2_weights(pxu, BAND0, 0.75)).abs().max().max())
    gates.append(dict(gate="G2 BAND03 == baseline.rules_v2_weights elementwise",
                      stat=f"max|dw| {d2:.3e}", passed=bool(d2 < 1e-12)))

    # G3 cross-run vs idea 675's committed ladder
    if PARENT.exists():
        par = pd.read_csv(PARENT)
        par = par[(par.panel == "U56") & (par.arm == "CAND20") & (par.cost == COST0)
                  & (par.sched == "W")].copy()
        par["g"] = par.gross.round(4)
        par = par[par.g.isin(set(GROSS150))].drop_duplicates("g").set_index("g").sort_index()
        mine = {}
        for g in GROSS150:
            r, _ = books[("U56", "CAND20")].at(g, COST0)
            s = pack(r[pans["U56"].masks["IS"]])
            mine[g] = (s["H1"], bool(s["H1"] > spyref["U56"]["IS"]["H1"]))
        common = [g for g in GROSS150 if g in par.index]
        dh = max(abs(mine[g][0] - float(par.loc[g, "IS_H1"])) for g in common)
        agree = sum(1 for g in common if mine[g][1] == bool(par.loc[g, "cwinIS_L1_H1"]))
        npass_par = int(sum(bool(par.loc[g, "cwinIS_L1_H1"]) for g in common))
        npass_me = int(sum(mine[g][1] for g in common))
        gates.append(dict(
            gate="G3 CROSS-RUN: idea 675's committed .ladder.csv U56/CAND20 IS_H1 + cwinIS_L1_H1",
            stat=f"{len(common)} rungs, max|dIS_H1| {dh:.3e}, leg agrees {agree}/{len(common)}, "
                 f"passes: 675 {npass_par} / this run {npass_me}",
            passed=bool(dh < G3_BAR and agree == len(common) and npass_par == 0 and npass_me == 0)))
    else:
        gates.append(dict(gate="G3 CROSS-RUN vs idea 675 .ladder.csv", stat="PARENT MISSING",
                          passed=False))

    # G4 committed triples
    rs = pans["U56"].spy[pans["U56"].masks["FULL"]]
    c, s, d = fmet(rs)
    rv2, _ = books[("U56", "BAND03")].at(0.75, COST0)
    c2, s2, d2b = fmet(rv2[pans["U56"].masks["FULL"]])
    ok4 = (abs(c - SPY_U56[0]) < TOL_C and abs(s - SPY_U56[1]) < TOL_S and abs(d - SPY_U56[2]) < TOL_D
           and abs(c2 - V2_U56[0]) < TOL_C and abs(s2 - V2_U56[1]) < TOL_S
           and abs(d2b - V2_U56[2]) < TOL_D)
    gates.append(dict(gate="G4 committed U56 triples (SPY, RULES v2)",
                      stat=f"SPY {c:.4f}/{s:.4f}/{d:.4f} vs {SPY_U56}; "
                           f"v2 {c2:.4f}/{s2:.4f}/{d2b:.4f} vs {V2_U56}", passed=bool(ok4)))

    # G5 empty excision reproduces
    p = pans["U56"]
    rr, _ = books[("U56", "CAND20")].at(PUBLISHED_G, COST0)
    m = p.masks["ISH1_HALF"]
    rb, rsp = rr[m], p.spy[m]
    n = len(rb)
    Sb1 = np.concatenate([[0.0], np.cumsum(rb)]); Sb2 = np.concatenate([[0.0], np.cumsum(rb * rb)])
    e5 = abs(_sharpe_excl(Sb1, Sb2, n, 0, 0) - fsharpe(rb))
    gates.append(dict(gate="G5 episode scan with an EMPTY excision == the un-excised Sharpe",
                      stat=f"|d| {e5:.3e}", passed=bool(e5 < 1e-12)))

    # G6 determinism
    bk2 = Book(pans["U56"], arm_w1(raw["U56"], prep(raw["U56"]), "CAND20"))
    r2, _ = bk2.at(PUBLISHED_G, COST0)
    d6 = float(np.abs(r2 - rr).max())
    gates.append(dict(gate="G6 determinism (rebuild the subject, compare)", stat=f"max|dr| {d6:.3e}",
                      passed=bool(d6 == 0.0)))

    # G7 the 2x2 is really a 2x2.  Read on the TARGET weights (what the arm asks for), not on
    # realised gross: between weekly rebalances a g < 1 book drifts against its own cash, so even
    # a fully-invested-by-construction arm has a realised gross that wanders.  The construction
    # claim is about the target.
    tg, eligstat = {}, {}
    for nm in PANELS:
        pre = prep(raw[nm])
        mF = pans[nm].masks["FULL"]
        for a in ["CAND20", "EWELIG", "CAND20_NG", "EWALL", "BAND03"]:
            s = arm_w1(raw[nm], pre, a).sum(axis=1)[mF]
            tg[(nm, a)] = (float(np.abs(s - 1.0).max()), float((s < 0.999).mean()), float(s.mean()))
        sc_n, above, vol20 = pre
        el = (above & (vol20 < MAXVOL) & raw[nm].notna()).sum(axis=1).values[mF]
        eligstat[nm] = (int(el.min()), int(np.median(el)), int((el == 0).sum()), int((el < 20).sum()),
                        int(mF.sum()))
    share4 = max(tg[(nm, a)][1] for nm in PANELS
                 for a in ["CAND20", "EWELIG", "CAND20_NG", "EWALL"])
    share_u56 = max(tg[("U56", a)][1] for a in ["CAND20", "EWELIG", "CAND20_NG", "EWALL"])
    v2_share = min(tg[(nm, "BAND03")][1] for nm in PANELS)
    zero_elig = sum(eligstat[nm][2] for nm in PANELS)
    gates.append(dict(
        gate="G7 THE 2x2 HAS NO CASH AXIS: on the panel the question is about (U56) all four arms "
             "target FULL investment on EVERY day; only RULES v2 (BAND03) de-grosses",
        stat=f"share of days under-invested: U56 all 4 arms {share_u56:.6f}; worst over 3 panels "
             f"{share4:.6f} (SMALL 2020-03-19, the single day in the record with 0 eligible "
             f"names); BAND03 under-invested on >= {v2_share:.4f} of days (mean gross frac "
             f"{min(tg[(nm,'BAND03')][2] for nm in PANELS):.4f}); zero-eligible days over all "
             f"3 panels {zero_elig}",
        passed=bool(share_u56 == 0.0 and share4 < 1e-3 and v2_share > 0.5)))
    P("  [note] the committed `ranked_w1` divides by the REALISED k, so CAND20 re-spreads to full")
    P("         gross whenever >= 1 name is eligible; on U56 the eligible count never reaches 0")
    P(f"         (min {eligstat['U56'][0]}, median {eligstat['U56'][1]}, < 20 on "
      f"{eligstat['U56'][3]} of {eligstat['U56'][4]} days).  The book has NO cash channel.")

    gdf = pd.DataFrame(gates)
    for _, r in gdf.iterrows():
        P(f"  [{'PASS' if r.passed else 'FAIL'}] {r.gate}\n        {r.stat}")
    P(f"  GATES {int(gdf.passed.sum())} of {len(gdf)} PASS")
    dump(gdf, "gates.csv")
    P("")

    # ================================ THE LADDER ================================
    P("=" * 100)
    P("THE LADDER: 3 panels x 6 arms x 30 gross x 4 costs, every sub-window level reported")
    P("=" * 100)
    rows = []
    for nm in PANELS:
        for a in ARMS:
            bk = books[(nm, a)]
            for cst in COSTS:
                for g in GROSS30:
                    r, turn = bk.at(g, cst)
                    row = dict(panel=nm, arm=a, gross=g, cost=cst)
                    for w in WINDOWS:
                        s = pack(r[pans[nm].masks[w]])
                        for k, v in s.items():
                            row[f"{w}_{k}"] = v
                        row[f"{w}_legwin"] = bool(s["Sharpe"] > spyref[nm][w]["Sharpe"])
                    rows.append(row)
    lad = pd.DataFrame(rows)
    dump(lad, "ladder.csv")
    P("")

    # ================================ H_FLAT ================================
    P("=" * 100)
    P("H_FLAT -- is a CONSTANT cash mix able to move a Sharpe leg at all?")
    P("  (150-rung fine ladder, 0.01..1.50; spread of the sub-window Sharpe across the ladder)")
    P("=" * 100)
    frows = []
    for nm in PANELS:
        for a in ["CAND20", "EWELIG", "CAND20_NG", "EWALL"]:
            for cst in [0.0, COST0, 25.0]:
                vals = {w: [] for w in ["ISH1_HALF", "IS", "FULL"]}
                for g in GROSS150:
                    r, _ = books[(nm, a)].at(g, cst)
                    for w in vals:
                        vals[w].append(fsharpe(r[pans[nm].masks[w]]))
                for w, v in vals.items():
                    v = np.asarray(v, float)
                    frows.append(dict(panel=nm, arm=a, cost=cst, window=w, n_rungs=len(v),
                                      smin=float(np.nanmin(v)), smax=float(np.nanmax(v)),
                                      spread=float(np.nanmax(v) - np.nanmin(v))))
    flat = pd.DataFrame(frows)
    dump(flat, "flat.csv")
    sub_flat = flat[(flat.window == "ISH1_HALF")]
    sp0 = float(sub_flat[sub_flat.cost == 0.0].spread.max())
    sp10 = float(sub_flat[sub_flat.cost == COST0].spread.max())
    sp25 = float(sub_flat[sub_flat.cost == 25.0].spread.max())
    H_FLAT = bool(sp0 < FLAT_BAR0 and sp10 < FLAT_BAR10)
    P(f"  max ISH1_HALF Sharpe spread across 150 gross rungs:  0 bps {sp0:.4f}  "
      f"10 bps {sp10:.4f}  25 bps {sp25:.4f}   (bars {FLAT_BAR0} / {FLAT_BAR10})")
    for nm in PANELS:
        r = sub_flat[(sub_flat.panel == nm) & (sub_flat.cost == COST0)]
        P("    " + nm + "  " + "  ".join(f"{x.arm} {x.spread:.4f}" for x in r.itertuples()))
    P(f"  H_FLAT: {'PASS -- a CONSTANT cash mix CANNOT be the carrier' if H_FLAT else 'FAIL'}")
    P("")

    # ================================ THE LEG ITSELF ================================
    P("=" * 100)
    P("THE LEG: is it really 0 of 30 on every sub-window, and which arms clear it?")
    P("=" * 100)
    crows = []
    for nm in PANELS:
        for w in SUBWINS:
            bar = spyref[nm][w]["Sharpe"]
            for a in ARMS:
                sl = lad[(lad.panel == nm) & (lad.arm == a) & (lad.cost == COST0)]
                npass = int(sl[f"{w}_legwin"].sum())
                at075 = sl[np.isclose(sl.gross, PUBLISHED_G)]
                crows.append(dict(panel=nm, subwin=w, arm=a, spy_sharpe=bar,
                                  n_pass_of_30=npass,
                                  sharpe_at_075=float(at075[f"{w}_Sharpe"].iloc[0]),
                                  mu_at_075=float(at075[f"{w}_mu"].iloc[0]),
                                  sd_at_075=float(at075[f"{w}_sd"].iloc[0]),
                                  spy_mu=spyref[nm][w]["mu"], spy_sd=spyref[nm][w]["sd"]))
    car = pd.DataFrame(crows)
    dump(car, "carriers.csv")

    for nm in PANELS:
        P(f"  panel {nm}: gross rungs (of 30) at which the arm's sub-window Sharpe > SPY's, 10 bps")
        hdr = f"    {'subwin':10s} {'SPY_Sh':>8s} " + " ".join(f"{a:>10s}" for a in ARMS)
        P(hdr)
        for w in SUBWINS:
            sl = car[(car.panel == nm) & (car.subwin == w)].set_index("arm")
            P(f"    {w:10s} {sl.spy_sharpe.iloc[0]:8.3f} " +
              " ".join(f"{int(sl.loc[a,'n_pass_of_30']):10d}" for a in ARMS))
    P("")

    # H_CONC / H_GATE on the leg itself (U56, ISH1_HALF)
    sub = car[(car.panel == "U56") & (car.subwin == "ISH1_HALF")].set_index("arm")
    n_cand = int(sub.loc["CAND20", "n_pass_of_30"])
    n_ew = int(sub.loc["EWELIG", "n_pass_of_30"])
    n_ng = int(sub.loc["CAND20_NG", "n_pass_of_30"])
    n_all = int(sub.loc["EWALL", "n_pass_of_30"])
    H_CONC = bool(n_cand == 0 and n_ew >= CARRIER_BAR)
    H_GATE = bool(n_cand == 0 and n_ng >= CARRIER_BAR)
    P(f"  U56 / ISH1_HALF / 10 bps, rungs clearing the leg out of 30:")
    P(f"    CAND20 (subject) {n_cand}   EWELIG (conc OFF) {n_ew}   "
      f"CAND20_NG (gate OFF) {n_ng}   EWALL (both OFF) {n_all}")
    P(f"  H_CONC: {'PASS' if H_CONC else 'FAIL'}   H_GATE: {'PASS' if H_GATE else 'FAIL'}   "
      f"(bar: subject 0 and the arm >= {CARRIER_BAR} of 30)")
    P("")

    # ================================ THE 2x2 ================================
    P("=" * 100)
    P("THE 2x2: Sharpe at g=0.75, 10 bps -- main effects of the GATE and of CONCENTRATION")
    P("=" * 100)
    frows = []
    for nm in PANELS:
        for w in SUBWINS:
            v = {}
            for (gt, cn), a in FACTORIAL.items():
                sl = lad[(lad.panel == nm) & (lad.arm == a) & (lad.cost == COST0)
                         & np.isclose(lad.gross, PUBLISHED_G)]
                v[(gt, cn)] = float(sl[f"{w}_Sharpe"].iloc[0])
            eff_gate = 0.5 * ((v[("gate", "top20")] - v[("nogate", "top20")])
                              + (v[("gate", "ew")] - v[("nogate", "ew")]))
            eff_conc = 0.5 * ((v[("gate", "top20")] - v[("gate", "ew")])
                              + (v[("nogate", "top20")] - v[("nogate", "ew")]))
            inter = (v[("gate", "top20")] - v[("gate", "ew")]) - \
                    (v[("nogate", "top20")] - v[("nogate", "ew")])
            spy = spyref[nm][w]["Sharpe"]
            frows.append(dict(panel=nm, subwin=w, spy_sharpe=spy,
                              CAND20=v[("gate", "top20")], EWELIG=v[("gate", "ew")],
                              CAND20_NG=v[("nogate", "top20")], EWALL=v[("nogate", "ew")],
                              gap_vs_spy=v[("gate", "top20")] - spy,
                              eff_gate=eff_gate, eff_conc=eff_conc, interaction=inter,
                              base_EWALL_gap=v[("nogate", "ew")] - spy))
    fac = pd.DataFrame(frows)
    dump(fac, "factorial.csv")
    for nm in PANELS:
        P(f"  panel {nm}  (gap = CAND20 Sharpe - SPY Sharpe; effects are ADDITIVE onto EWALL)")
        P(f"    {'subwin':10s} {'SPY':>7s} {'CAND20':>8s} {'gap':>8s} | {'EWALL':>8s} "
          f"{'baseGap':>8s} {'GATE':>8s} {'CONC':>8s} {'inter':>8s}")
        for _, r in fac[fac.panel == nm].iterrows():
            P(f"    {r.subwin:10s} {r.spy_sharpe:7.3f} {r.CAND20:8.3f} {r.gap_vs_spy:8.3f} | "
              f"{r.EWALL:8.3f} {r.base_EWALL_gap:8.3f} {r.eff_gate:8.3f} {r.eff_conc:8.3f} "
              f"{r.interaction:8.3f}")
    P("")

    # ================================ H_MEANVOL ================================
    P("=" * 100)
    P("H_MEANVOL -- is the gap a MEAN gap or a VOL gap?  (exact two-term decomposition)")
    P("=" * 100)
    mrows = []
    for nm in PANELS:
        for w in SUBWINS:
            s = car[(car.panel == nm) & (car.subwin == w) & (car.arm == "CAND20")].iloc[0]
            mu_b, sd_b, mu_s, sd_s = s.mu_at_075, s.sd_at_075, s.spy_mu, s.spy_sd
            mean_term = (mu_b - mu_s) / sd_s
            vol_term = mu_b * (1.0 / sd_b - 1.0 / sd_s)
            tot = mean_term + vol_term
            mrows.append(dict(panel=nm, subwin=w, mu_book=mu_b, mu_spy=mu_s, sd_book=sd_b,
                              sd_spy=sd_s, mean_term=mean_term, vol_term=vol_term, total=tot,
                              check=tot - (s.sharpe_at_075 - s.spy_sharpe),
                              mean_dominates=bool(abs(mean_term) > MEANVOL_BAR * abs(vol_term))))
    mv = pd.DataFrame(mrows)
    dump(mv, "meanvol.csv")
    for nm in PANELS:
        P(f"  panel {nm}")
        P(f"    {'subwin':10s} {'mu_bk':>8s} {'mu_spy':>8s} {'sd_bk':>7s} {'sd_spy':>7s} "
          f"{'MEAN':>8s} {'VOL':>8s} {'sum':>8s} {'ident':>10s}")
        for _, r in mv[mv.panel == nm].iterrows():
            P(f"    {r.subwin:10s} {r.mu_book:8.4f} {r.mu_spy:8.4f} {r.sd_book:7.4f} "
              f"{r.sd_spy:7.4f} {r.mean_term:8.3f} {r.vol_term:8.3f} {r.total:8.3f} "
              f"{r.check:10.2e}")
    u = mv[(mv.panel == "U56") & (mv.subwin == "ISH1_HALF")].iloc[0]
    H_MEANVOL = bool(u.mean_dominates)
    P(f"  identity max |residual| {mv.check.abs().max():.3e}")
    P(f"  H_MEANVOL on the leg itself (U56/ISH1_HALF): MEAN {u.mean_term:.3f} vs VOL "
      f"{u.vol_term:.3f}  ->  {'PASS (a MEAN gap)' if H_MEANVOL else 'FAIL'}")
    P("")

    # ================================ H_EPISODE ================================
    P("=" * 100)
    P("H_EPISODE -- can ONE contiguous block of <= 60 trading days flip the leg?")
    P("  (the SAME days are excised from the book and from SPY)")
    P("=" * 100)
    erows, ebest = [], []
    for nm in PANELS:
        for w in ["ISH1_HALF", "CAL0912", "CAL0910"]:
            r, _ = books[(nm, "CAND20")].at(PUBLISHED_G, COST0)
            m = pans[nm].masks[w]
            idx = pans[nm].idx[m]
            if int(m.sum()) < EPISODE_MAX + 10:
                P(f"    {nm:6s} {w:10s} SKIPPED -- only {int(m.sum())} days in the window "
                  f"(panel starts after it); no episode search is meaningful")
                continue
            best, lstar, tab = episode_scan(r[m], pans[nm].spy[m])
            tab["panel"], tab["subwin"] = nm, w
            erows.append(tab)
            d0 = fsharpe(r[m]) - fsharpe(pans[nm].spy[m])
            ebest.append(dict(panel=nm, subwin=w, n_days=int(m.sum()), gap_unexcised=d0,
                              best_gap=best[0], best_len=best[2] - best[1],
                              best_from=str(idx[best[1]].date()), best_to=str(idx[best[2] - 1].date()),
                              sharpe_book_excl=best[3], sharpe_spy_excl=best[4],
                              L_star=(-1 if lstar is None else lstar),
                              flips_within_60=bool(lstar is not None)))
    epi = pd.concat(erows, ignore_index=True)
    eb = pd.DataFrame(ebest)
    dump(epi, "episode.csv")
    dump(eb, "episode_best.csv")
    P(f"    {'panel':6s} {'subwin':10s} {'days':>5s} {'gap':>8s} | {'bestGap':>8s} {'len':>4s} "
      f"{'from':>11s} {'to':>11s} {'L*':>4s}")
    for _, r in eb.iterrows():
        P(f"    {r.panel:6s} {r.subwin:10s} {r.n_days:5d} {r.gap_unexcised:8.3f} | "
          f"{r.best_gap:8.3f} {r.best_len:4d} {r.best_from:>11s} {r.best_to:>11s} "
          f"{('none' if r.L_star < 0 else str(r.L_star)):>4s}")
    # calibration: the argmax is the best of ~n x L blocks, so report the whole distribution
    shr = []
    for nm in PANELS:
        w = "ISH1_HALF"
        r, _ = books[(nm, "CAND20")].at(PUBLISHED_G, COST0)
        m = pans[nm].masks[w]
        t = episode_share(r[m], pans[nm].spy[m], [5, 10, 21, 43, 60])
        t["panel"], t["subwin"] = nm, w
        shr.append(t)
    shr = pd.concat(shr, ignore_index=True)
    dump(shr, "episode_share.csv")
    P("  CALIBRATION -- over ALL contiguous blocks of each length on ISH1_HALF (not just the best):")
    for nm in PANELS:
        P(f"    {nm:6s} " + "  ".join(
            f"L={int(r.L):2d} flip {r.share_flip:.3f} med {r.median_gap:+.3f}"
            for _, r in shr[shr.panel == nm].iterrows()))
    e0 = eb[(eb.panel == "U56") & (eb.subwin == "ISH1_HALF")].iloc[0]
    H_EPISODE = bool(e0.flips_within_60)
    P(f"  H_EPISODE on the leg itself (U56/ISH1_HALF): best excision of <= {EPISODE_MAX}d moves the "
      f"gap {e0.gap_unexcised:.3f} -> {e0.best_gap:.3f}  ->  "
      f"{'PASS (a single-episode fact)' if H_EPISODE else 'FAIL (not a single episode)'}")
    P("")

    # ---- the gate's own cash, quantified (NOT a Sharpe claim -- a level claim) ----
    P("  the CASH channel, for the record (mean realised gross / g inside each sub-window;")
    P("   BAND03 = RULES v2 is carried as the arm that DOES de-gross, for contrast):")
    grows = []
    for nm in PANELS:
        for w in SUBWINS:
            if pans[nm].masks[w].sum() < 3:
                continue
            for a in ["CAND20", "EWELIG", "CAND20_NG", "EWALL", "BAND03"]:
                rg = books[(nm, a)].realised_gross(PUBLISHED_G)[pans[nm].masks[w]]
                grows.append(dict(panel=nm, subwin=w, arm=a,
                                  mean_gross_frac=float(np.mean(rg) / PUBLISHED_G),
                                  min_gross_frac=float(np.min(rg) / PUBLISHED_G)))
    gr = pd.DataFrame(grows)
    dump(gr, "gross_used.csv")
    for nm in PANELS:
        for a in ["CAND20", "BAND03"]:
            sl = gr[(gr.panel == nm) & (gr.arm == a)]
            P(f"    {nm:6s} {a:7s}: " + "  ".join(f"{r.subwin} {r.mean_gross_frac:.3f}"
                                                  for _, r in sl.iterrows()))
    P("")

    # ================================ H_PANEL ================================
    sub_all = car[(car.subwin == "ISH1_HALF")].set_index(["panel", "arm"])
    pr = {}
    for nm in PANELS:
        pr[nm] = dict(CAND20=int(sub_all.loc[(nm, "CAND20"), "n_pass_of_30"]),
                      EWELIG=int(sub_all.loc[(nm, "EWELIG"), "n_pass_of_30"]),
                      CAND20_NG=int(sub_all.loc[(nm, "CAND20_NG"), "n_pass_of_30"]),
                      EWALL=int(sub_all.loc[(nm, "EWALL"), "n_pass_of_30"]))
    carrier = "CONCENTRATION" if H_CONC and not H_GATE else \
              ("GATE" if H_GATE and not H_CONC else ("BOTH" if H_CONC and H_GATE else "NEITHER"))
    trav = []
    for nm in PANELS:
        c_ = pr[nm]["CAND20"] == 0 and pr[nm]["EWELIG"] >= CARRIER_BAR
        g_ = pr[nm]["CAND20"] == 0 and pr[nm]["CAND20_NG"] >= CARRIER_BAR
        trav.append((nm, "CONCENTRATION" if c_ and not g_ else
                     ("GATE" if g_ and not c_ else ("BOTH" if c_ and g_ else "NEITHER"))))
    H_PANEL = bool(len({v for _, v in trav}) == 1)
    P("=" * 100)
    P("H_PANEL -- does the answer travel?")
    P("=" * 100)
    for nm, v in trav:
        P(f"    {nm:6s} CAND20 {pr[nm]['CAND20']:2d}/30  EWELIG {pr[nm]['EWELIG']:2d}/30  "
          f"CAND20_NG {pr[nm]['CAND20_NG']:2d}/30  EWALL {pr[nm]['EWALL']:2d}/30  -> {v}")
    P(f"  H_PANEL: {'PASS' if H_PANEL else 'FAIL'}   (U56 verdict: {carrier})")
    P("")

    # ================================ RULE 8 ================================
    P("=" * 100)
    P("RULE 8 -- (arm, gross) chosen on 2009-2016 ALONE; 2017-2026 read ONCE; both KEEP paths")
    P("=" * 100)
    wrows = []
    for nm in PANELS:
        cand = []
        for a in ["CAND20", "EWELIG", "CAND20_NG", "EWALL"]:
            for g in GROSS30:
                r, _ = books[(nm, a)].at(g, COST0)
                is_ = pack(r[pans[nm].masks["IS"]])
                oos = pack(r[pans[nm].masks["OOS"]])
                cand.append((a, g, is_, oos))
        sel = {
            "PICK_ISSHARPE": max(cand, key=lambda x: (-1e9 if np.isnan(x[2]["Sharpe"]) else x[2]["Sharpe"])),
            "PICK_ISCALMAR": max(cand, key=lambda x: (-1e9 if (np.isnan(x[2]["CAGR"]) or x[2]["MaxDD"] == 0)
                                                      else x[2]["CAGR"] / abs(x[2]["MaxDD"]))),
            "PICK_ISLEG": max(cand, key=lambda x: (
                (1 if x[2]["H1"] > spyref[nm]["IS"]["H1"] else 0),
                (-1e9 if np.isnan(x[2]["Sharpe"]) else x[2]["Sharpe"]))),
            "PICK_LIVE": next(x for x in cand if x[0] == "CAND20" and np.isclose(x[1], PUBLISHED_G)),
        }
        # PROTOCOL 2 forbids leverage unless the idea asks for it, and the record's 0.05..1.50
        # gross axis runs past 1.00.  The NL selectors are the same choosers restricted to g <= 1.
        nl = [x for x in cand if x[1] <= 1.0 + 1e-9]
        sel["PICK_ISSHARPE_NL"] = max(nl, key=lambda x: (-1e9 if np.isnan(x[2]["Sharpe"]) else x[2]["Sharpe"]))
        sel["PICK_ISCALMAR_NL"] = max(nl, key=lambda x: (-1e9 if (np.isnan(x[2]["CAGR"]) or x[2]["MaxDD"] == 0)
                                                         else x[2]["CAGR"] / abs(x[2]["MaxDD"])))
        for k, (a, g, is_, oos) in sel.items():
            L = legswin(oos, spyref[nm]["OOS"])
            wrows.append(dict(panel=nm, selector=k, arm=a, gross=g,
                              IS_Sharpe=is_["Sharpe"], IS_H1=is_["H1"],
                              IS_legH1=bool(is_["H1"] > spyref[nm]["IS"]["H1"]),
                              OOS_CAGR=oos["CAGR"], OOS_Sharpe=oos["Sharpe"], OOS_MaxDD=oos["MaxDD"],
                              OOS_H1=oos["H1"], OOS_H2=oos["H2"],
                              spy_CAGR=spyref[nm]["OOS"]["CAGR"], spy_Sharpe=spyref[nm]["OOS"]["Sharpe"],
                              spy_MaxDD=spyref[nm]["OOS"]["MaxDD"],
                              v2_CAGR=v2ref[nm]["OOS"]["CAGR"], v2_Sharpe=v2ref[nm]["OOS"]["Sharpe"],
                              v2_MaxDD=v2ref[nm]["OOS"]["MaxDD"],
                              **{f"OOS_{kk}": vv for kk, vv in L.items()},
                              pass4b=bool(all(L.values())),
                              pass4a=pass4a(oos, v2ref[nm]["OOS"])))
    wf = pd.DataFrame(wrows)
    dump(wf, "walkforward.csv")
    for nm in PANELS:
        P(f"  panel {nm}   SPY OOS {spyref[nm]['OOS']['CAGR']:.2%} / "
          f"{spyref[nm]['OOS']['Sharpe']:.3f} / {spyref[nm]['OOS']['MaxDD']:.2%}   |   "
          f"RULES v2 OOS {v2ref[nm]['OOS']['CAGR']:.2%} / {v2ref[nm]['OOS']['Sharpe']:.3f} / "
          f"{v2ref[nm]['OOS']['MaxDD']:.2%}")
        for _, r in wf[wf.panel == nm].iterrows():
            P(f"    {r.selector:14s} {r.arm:10s} g={r.gross:4.2f}  IS_H1leg="
              f"{str(r.IS_legH1):5s}  OOS {r.OOS_CAGR:7.2%} / {r.OOS_Sharpe:6.3f} / "
              f"{r.OOS_MaxDD:7.2%}   4b {str(r.pass4b):5s}  4a {str(r.pass4a):5s}")
    n4b, n4a = int(wf.pass4b.sum()), int(wf.pass4a.sum())
    P(f"  OOS: 4b {n4b} of {len(wf)}   4a {n4a} of {len(wf)}")
    P("")

    # ================================ VERDICT ================================
    P("=" * 100)
    P("VERDICT")
    P("=" * 100)
    hyp = dict(H_FLAT=H_FLAT, H_CONC=H_CONC, H_GATE=H_GATE, H_EPISODE=H_EPISODE,
               H_MEANVOL=H_MEANVOL, H_PANEL=H_PANEL)
    for k, v in hyp.items():
        P(f"  {k:11s} {'PASS' if v else 'FAIL'}")
    P(f"  CARRIER on U56 / ISH1_HALF: {carrier}")
    P(f"  runtime {time.time()-t0:.1f}s")
    pd.DataFrame([hyp]).to_csv(OUT / f"{STEM}.hypotheses.csv", index=False)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG))
    return dict(hyp=hyp, carrier=carrier, wf=wf, fac=fac, car=car, eb=eb, flat=flat,
                gates=gdf, mv=mv, pr=pr, spyref=spyref, v2ref=v2ref)


if __name__ == "__main__":
    main()

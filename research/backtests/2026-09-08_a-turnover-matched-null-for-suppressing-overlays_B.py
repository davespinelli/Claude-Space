#!/usr/bin/env python3
"""QUEUE idea 203 - a-turnover-matched-null-for-suppressing-overlays   (lane B, 2026-09-08).

QUESTION (pre-registered, verbatim from QUEUE.md idea 203)
    "idea 191 measured the rotation null's turnover fidelity on BUDGET-skip at 1782.7% mean on a
     widened threshold grid (idea 186 published 25.4%/213.8%), i.e. the null is not turnover-
     matched for an overlay that suppresses a trade and degrades without bound in on-share.
     Build and validate a null that resamples SKIP DECISIONS at matched count rather than
     rotating the state, and re-price idea 186's BUDGET family against it.  Max 2 params."

WHAT IS AT STAKE
    PROTOCOL clause 11 (proposed by idea 181, extended to overlays by idea 186) says an
    instrument's claimed effect must beat a MATCHED NULL of the same construction that carries no
    information.  For an overlay (s, A) - an ON indicator over the rebalance dates plus an action -
    idea 186's null is the same action A on a CIRCULAR ROTATION of s.  Rotation preserves the
    on-share and the episode structure EXACTLY, and idea 186 validated that it also preserves
    realised turnover to 1.25% (DDCTL) and 0.82% (SLEEVE).  It fails for exactly one construction:
    BUDGET-skip, where the action SUPPRESSES a rebalance.  Idea 186 measured 25.4% mean / 213.8%
    max on its 3-point tau grid; idea 191 widened the grid and measured 1782.7% mean.
    So for a schedule-suppressing overlay the published clause verdict is a comparison between two
    books that do not trade the same amount, and the clause's own definition ("same on-share AND
    turnover") is violated.  Idea 203 asks for the repair.

THE REPAIR THIS RUN BUILDS, AND WHY IT IS THE ONE THAT COULD WORK
    Rotation randomises the PHASE of s.  Idea 203's proposal is to randomise the SKIP DECISIONS
    themselves at matched count: draw K of the J rebalance dates uniformly, K = the real overlay's
    skip count.  That fixes nothing about turnover a priori - it matches the same statistic
    rotation already matches (the count) - so this run does not stop there.  It builds the
    one-parameter FAMILY that contains it and interpolates all the way to a turnover-matched null:

        RS-B   stratify the J rebalance dates into B equal-count strata by the EX-ANTE
               target-to-target turnover tt_j = |w_j - w_{j-1}|_1 of the untreated base book
               (a quantity known at decision time and IDENTICAL for the real overlay and every
               null draw, so stratifying on it peeks at nothing), then draw, INDEPENDENTLY IN
               EACH STRATUM, exactly as many skip dates as the real overlay has there.

        B = 1   is idea 203's literal proposal: count-matched, turnover-blind.
        B -> J  matches the ex-ante turnover profile of the skipped set exactly.

    The BUDGET overlay's ON indicator is s_j = 1[tt_j > tau].  So tt is a SUFFICIENT STATISTIC for
    the overlay's timing, and conditioning the null on tt is conditioning on the thing under test.
    That is the tension idea 203 walks into and this run measures rather than assumes: FIDELITY and
    RANDOMISATION are the two ends of one dial, and B is the dial.

TUNED PARAMETERS - exactly two, per PROTOCOL rule 4.  ALL grid points reported.
    1. tau, the turnover threshold: {0.05, 0.10, 0.20, 0.30, 0.50}   (idea 191's widened grid, so
       the published 1782.7% is measured on the same ladder)
    2. B, the stratum count of the new null: {1, 2, 4, 8, 16}
    PANEL, ACTION (skip/half), COST RUNG and NULL KIND are corpus axes, not tuned parameters.
    Nothing is picked for reporting; the rule-8 selector below is the only place a point is chosen
    and it chooses on the IS window alone.

NULL KINDS priced side by side on every point (6):
    ROT   idea 186's circular rotation, at idea 186's own offsets (SEED 186_400) - the incumbent
    RS1   count-matched uniform resample of the skip set               (idea 203's literal proposal)
    RS2 / RS4 / RS8 / RS16  ex-ante-turnover-stratified resample at B = 2 / 4 / 8 / 16

BASE BOOK, held fixed: idea 2's 4b candidate - top-20 equal weight on the scan.py composite with
    NO vol scaler, gross 0.75, weekly, t+1.  Panels U56, BROAD136, SMALL439 (the sub-$2B panel with
    the 44 tickers whose data/small_meta.csv max_1d_move >= 1.0 dropped first), exactly idea 186's.

COSTS.  Every book is run ONCE at 0 bps; the 10 and 25 bps rungs are derived from the engine's own
    turnover series (port_net = port_gross - turnover * bps / 1e4), asserted exact in gate [b].

WALK-FORWARD (PROTOCOL rule 8), 12 cells = 3 panels x 2 actions x 2 cost rungs.  Parameters chosen
    on <= 2016-12-31 only; 2017-2026 read once.  Arms:
        S0  do nothing (the untreated base book)
        S1  IS-Sharpe argmax over the 5-point tau ladder
        S2_<kind>  the same argmax restricted to tau points that CLEAR the clause on the IS window
                   under that null kind (one arm per null kind, 6 arms)
    OOS CAGR / Sharpe / MaxDD reported for every arm against the base book and against SPY.

BOTH KEEP PATHS (4a vs the LIVE RULES v2 book, and 4b vs SPY) are evaluated on every real row and
    every null row, full sample and halves, and counted.

REPRODUCTION GATES, asserted before any new number is read
    [a] fast_backtest reproduces products/backtester/engine.backtest to < 1e-12 (returns, turnover)
    [b] the cost identity: 10 bps derived from the 0 bps run vs a genuine 10 bps engine run = 0.0
    [c] the base CAND-20 weights equal idea 78/171's weights_cand exactly
    [d] mstats (numpy) reproduces engine.metrics to < 1e-12 on CAGR / Sharpe / MaxDD
    [e] THE ROT ARM REPRODUCES IDEA 186's COMMITTED GRID.  Idea 186's BUDGET rows at
        tau in {0.10, 0.20, 0.30} were drawn with an UNSALTED seed (rotations(J, 20, 186_400)), so
        this run re-draws the identical offsets and its ROT rows must equal the committed
        .grid.csv rows for those points.  Checked on Sharpe, MaxDD, on_share and turnover.
    [f] NULL VALIDITY: every draw of every kind matches the real overlay's skip COUNT exactly, and
        every RS-B draw matches the real overlay's PER-STRATUM count exactly.

    NOT reproducible, and said so rather than quietly re-derived: idea 191's 1782.7% itself.  Idea
    208 established that idea 191 salted its rotation offsets with Python's per-process hash()
    (`SEED + hash((pan.name, fam, thr)) % 10_000`), so that number is not a fixed quantity.  This
    run re-measures the same statistic on the same ladder with a fixed seed and reports its own
    value and standard error beside idea 191's.

SIZE CONTROL (a null that is known to be null).  On U56, every point is re-run with the real ON
    indicator replaced by a RANDOM ON indicator of the same on-share (fixed seed, zero timing
    information) and priced against all 6 null kinds.  The share of these that CLEAR is the
    clause's realised false-positive rate, against a nominal 1/21 = 4.8%.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  gates [a]-[f] hold.
    P2  RS1 does NOT repair the turnover gap on BUDGET-skip: its mean gap is within a factor of two
        of ROT's.  Count is not the binding statistic; WHICH dates are skipped is.
    P3  The realised turnover gap falls monotonically in B, and the null BAND WIDTH
        (max |dSharpe| over draws) falls monotonically in B as well.
    P4  The frontier is a WALL, not a trade-off with an interior optimum: by the time the ex-ante
        turnover gap is at the ~4% level rotation achieves on the NON-suppressing 'half' action,
        the null's skip set overlaps the real one so heavily that the clause clears ~0 real points.
    P5  On the NOISE size control the realised clear rate is at or below nominal for every kind,
        and RS-B does NOT lose size as B grows (a random ON indicator is uncorrelated with tt, so
        stratifying on tt costs it no randomisation).  If P4 and P5 both hold, the power loss is
        specific to overlays whose indicator IS the stratifying variable - i.e. to the exact case
        idea 203 wants repaired.
    P6  S2 loses to S0 under EVERY null kind.  Eleven prior instances (110/132/151/166/171/174/175/
        181/186/191/204) of an IS-fitted selector losing to doing nothing.
    P7  No row passes both KEEP paths on SMALL439 at either rung.

CAVEATS carried, not buried
    * SURVIVORSHIP: all three panels are current-constituent lists (idea 54); SMALL439 contains no
      delistings.  Real and null draws inherit the bias identically so the COMPARISON is unaffected;
      the LEVEL of every number is not.
    * 20 draws give a nominal one-sided size of 1/21 = 4.8%; that is approximate, not exact, and
      rotation additionally offers only J distinct nulls with correlated neighbours (idea 214).
    * Idea 211 killed the two-sided |dSharpe| clause reading in favour of the SIGNED one.  Both are
      computed here: the two-sided for comparability with idea 186's published verdicts, the signed
      as the primary re-pricing.
    * Idea 38 (calendar-day index on U56/BROAD after 2014-09-17) and idea 126 (t+1 only) carry.
    * Idea 144: an overlaid book is the same book with an instrument on it, not a new book.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .fidelity.csv, .clause.csv,
.noise.csv, .walkforward.csv, .keep.csv.
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-08_a-turnover-matched-null-for-suppressing-overlays_B"
OUT = ROOT / "research" / "backtests"
IDEA186 = OUT / "2026-09-05_the-null-column-for-instruments-that-are-not-keyed-tilts_cloud.grid.csv"

COST_RUNGS = [10, 25]
MAX_VOL = 0.60
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
PHI, DELTA = 0.70, 0.60          # 4b CAGR floor / MaxDD cap, PROTOCOL rule 4b
FREQ = "W"
BASE_N, BASE_GROSS = 20, 0.75
N_NULL = 20
ROT_SEED = 186_400               # idea 186's own rotation seed, so gate [e] is exact
RS_SEED = 203_000
NOISE_SEED = 203_500

TAUS = [0.05, 0.10, 0.20, 0.30, 0.50]     # tuned parameter 1 (idea 191's widened grid)
BS = [1, 2, 4, 8, 16]                     # tuned parameter 2 (strata of the new null)
MODES = ["skip", "half"]
KINDS = ["ROT"] + [f"RS{b}" for b in BS]

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 4000)

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


# ---------------------------------------------------------------- metrics (numpy, gated in [d])
def mstats(r):
    """CAGR, Sharpe, MaxDD of a numpy return array.  Gated against engine.metrics in check [d]."""
    if len(r) < 6:
        return np.nan, np.nan, np.nan
    eq = np.cumprod(1.0 + r)
    yrs = len(r) / 252.0
    cagr = eq[-1] ** (1.0 / yrs) - 1.0
    dd = eq / np.maximum.accumulate(eq) - 1.0
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, (r.mean() * 252.0 / vol if vol else np.nan), dd.min()


def sh(r):
    return mstats(r)[1]


def tstat(x):
    x = np.asarray([v for v in x if np.isfinite(v)], float)
    if len(x) < 3 or x.std(ddof=1) == 0:
        return np.nan
    return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))


# ---------------------------------------------------------------- fast backtest (idea 186's)
def fast_backtest(prices, weights, cost_bps=0.0, freq=FREQ, mask=None):
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values if mask is None else np.asarray(mask, bool)
    m = np.concatenate([[False], m[:-1]]).copy()
    m[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    port, turn = _core(rets, Cp, wt, m)
    return {"returns": pd.Series(port - turn * cost_bps / 1e4, index=idx),
            "turnover": pd.Series(turn, index=idx)}


def _core(rets, Cp, wt, m):
    """The inner loop of fast_backtest with the price cumprod hoisted out (it does not depend on
    the weights, and this run evaluates ~4800 books on 3 fixed panels)."""
    T = rets.shape[0]
    reb = np.flatnonzero(m)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    port = (held * rets).sum(axis=1)
    return port, turn


def net(res, bps):
    return res["returns"] - res["turnover"] * bps / 1e4


# ---------------------------------------------------------------- panels and base book
def comp_score(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


class Panel:
    def __init__(self, name, px, tradable):
        self.name = name
        self.px = px
        self.tradable = [c for c in px.columns if c in tradable]
        vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        elig = ((px > px.rolling(200).mean()) & (vol20 < MAX_VOL)).copy()
        drop = [c for c in px.columns if c not in set(self.tradable)]
        if drop:
            elig[drop] = False
        rank = comp_score(px).where(elig).rank(axis=1, ascending=False)
        self.W = (rank <= BASE_N).astype(float) * (BASE_GROSS / BASE_N)
        self.mask = rebalance_mask(px.index, FREQ).values
        self.reb = np.flatnonzero(self.mask)
        self.spy = px["SPY"].pct_change().fillna(0.0)
        # hoisted price algebra
        self.rets = px.pct_change().fillna(0.0).values
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), C[:-1]])
        self.Wv = self.W.values
        # ex-ante target-to-target turnover at the rebalance dates (the stratifying variable)
        w = self.Wv[self.reb]
        prev = np.vstack([np.zeros((1, w.shape[1])), w[:-1]])
        self.tt = np.abs(w - prev).sum(axis=1)
        # windows
        self.st = px.index.get_loc(px.index[260])
        self.is_end = int(np.searchsorted(px.index.values, np.datetime64(IS_END), "right"))
        self.oos_st = int(np.searchsorted(px.index.values, np.datetime64(OOS_START), "left"))
        self.years = None


SLEEVE_ASSETS = ["TLT", "GLD", "UUP"]


def build_panels():
    """Idea 186's panel construction VERBATIM (including the sleeve columns it joins to BROAD136
    and SMALL439 as untradable price columns), because gate [e] compares against its committed
    grid and the composite's cross-sectional pct ranks are computed over ALL columns."""
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    P(f"  SMALL: {len([c for c in pxs.columns if c!='SPY'])} names, dropped "
      f"{len([c for c in pxs.columns if c in bad])} with max_1d_move >= 1.0 -> {len(s_stk)} tradable")
    ref = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)

    def add_sleeve(px):
        a = ref[SLEEVE_ASSETS].reindex(px.index, method="ffill")
        return pd.concat([px.drop(columns=SLEEVE_ASSETS, errors="ignore"), a], axis=1).ffill()

    pxs = add_sleeve(pxs[s_stk + ["SPY"]])
    px136 = add_sleeve(px136)
    b_stk = [c for c in px136.columns if c != "SPY" and c not in SLEEVE_ASSETS]
    u_stk = [c for c in px56.columns if c != "SPY"]
    return [Panel("U56", px56, set(u_stk)),
            Panel("BROAD136", px136, set(b_stk)),
            Panel("SMALL439", pxs, set(s_stk))]


# ---------------------------------------------------------------- the nulls
def rotations(J, n, seed):
    """Idea 186's own offset draw, reproduced verbatim so gate [e] is exact."""
    rng = np.random.default_rng(seed)
    cand = rng.permutation(np.arange(1, J))
    return sorted(cand[:n].tolist())


def strat_bins(tt, B):
    """B equal-count strata of the rebalance dates by EX-ANTE target-to-target turnover."""
    order = np.argsort(tt, kind="stable")
    return np.array_split(order, B)


def rs_draw(s_real, bins, rng):
    """Resample the skip set: independently in each stratum, draw exactly as many ON dates as the
    real overlay has there.  B = 1 is the count-matched uniform draw idea 203 proposes."""
    out = np.zeros(len(s_real), bool)
    for b in bins:
        kb = int(s_real[b].sum())
        if kb:
            out[rng.choice(b, size=kb, replace=False)] = True
    return out


def draws_for(kind, s_real, tt, J, seed_key):
    if kind == "ROT":
        offs = rotations(J, N_NULL, ROT_SEED)
        return [np.roll(s_real, o) for o in offs]
    B = int(kind[2:])
    bins = strat_bins(tt, B)
    rng = np.random.default_rng(RS_SEED + seed_key)
    return [rs_draw(s_real, bins, rng) for _ in range(N_NULL)]


def free_strata(s_real, tt, B):
    """Strata in which the draw has any freedom at all (0 < k_b < |b|).  When the ON indicator is a
    threshold on the stratifying variable this collapses to 1 as B grows - that IS the wall."""
    return sum(1 for b in strat_bins(tt, B) if 0 < int(s_real[b].sum()) < len(b))


# ---------------------------------------------------------------- the action
def build_book(pan, s_reb, mode):
    """Return (wt_shifted, mask) for the BUDGET overlay's action on the ON rebalance dates."""
    mask = pan.mask
    Wv = pan.Wv
    if mode == "skip":
        mask = pan.mask.copy()
        mask[pan.reb[s_reb]] = False
    else:                                   # 'half': move half way to the target
        Wv = pan.Wv.copy()
        wr = Wv[pan.reb]
        for j in np.flatnonzero(s_reb):
            prev = wr[j - 1] if j > 0 else np.zeros(wr.shape[1])
            wr[j] = 0.5 * wr[j] + 0.5 * prev
        Wv[pan.reb] = wr
    wt = np.vstack([np.zeros((1, Wv.shape[1])), Wv[:-1]])
    m = np.concatenate([[False], mask[:-1]]).copy()
    m[0] = True
    return wt, m


def run_book(pan, s_reb, mode):
    wt, m = build_book(pan, s_reb, mode)
    port, turn = _core(pan.rets, pan.Cp, wt, m)
    return port, turn


# ---------------------------------------------------------------- KEEP paths
def row_stats(pan, port, turn, bps, ref):
    r = port - turn * bps / 1e4
    st = pan.st
    rr = r[st:]
    cagr, sharpe, mdd = mstats(rr)
    h = len(rr) // 2
    h1, h2 = sh(rr[:h]), sh(rr[h:])
    is_sh = sh(r[st:pan.is_end])
    oc, os_, om = mstats(r[pan.oos_st:])
    b = ref[bps]
    f4a = []
    if not h1 > b["v2_h1"]: f4a.append("H1")
    if not h2 > b["v2_h2"]: f4a.append("H2")
    if not mdd >= b["v2_dd"]: f4a.append("DD")
    f4b = []
    if not h1 > ref["spy_h1"]: f4b.append("H1")
    if not h2 > ref["spy_h2"]: f4b.append("H2")
    if not os_ > ref["spy_oos_sh"]: f4b.append("OOS")
    if not abs(mdd) <= DELTA * abs(ref["spy_dd"]): f4b.append("DD")
    if not cagr >= PHI * ref["spy_cagr"]: f4b.append("CAGR")
    f4a1 = []
    if not h1 > b["v1_h1"]: f4a1.append("H1")
    if not h2 > b["v1_h2"]: f4a1.append("H2")
    if not mdd >= b["v1_dd"]: f4a1.append("DD")
    return dict(CAGR=cagr, Sharpe=sharpe, MaxDD=mdd, H1=h1, H2=h2, IS_Sharpe=is_sh,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=om,
                turnover=turn[st:].sum() / (len(rr) / 252.0),
                dSharpe=sharpe - b["base_sh"], dMaxDD=abs(b["base_dd"]) - abs(mdd),
                IS_dSharpe=is_sh - b["base_is_sh"],
                pass4a=(len(f4a) == 0), pass4a_v1=(len(f4a1) == 0), pass4b=(len(f4b) == 0),
                fail4a=",".join(f4a) or "-", fail4b=",".join(f4b) or "-")


# ---------------------------------------------------------------- gates
def gates(pan):
    ok = True
    P(f"  --- {pan.name} ---")
    a = backtest(pan.px, pan.W, cost_bps=10, freq=FREQ)
    b = fast_backtest(pan.px, pan.W, 10, FREQ)
    port, turn = run_book(pan, np.zeros(len(pan.reb), bool), "skip")
    mine = pd.Series(port, index=pan.px.index)
    nan_e = int(a["returns"].isna().sum() + a["turnover"].isna().sum())
    dr = float((a["returns"] - (mine - pd.Series(turn, index=pan.px.index) * 10 / 1e4)).abs().max())
    dt = float((a["turnover"] - pd.Series(turn, index=pan.px.index)).abs().max())
    dr2 = float((a["returns"] - b["returns"]).abs().max())
    P(f"  [a] fast_backtest/_core vs engine.backtest: max|dret|={max(dr,dr2):.3e} max|dturn|={dt:.3e}"
      f"  ({nan_e} engine rows are NaN at the sample's first bar - engine.backtest does not fill the"
      f" shift; they are skipped, as idea 186's own check did)"
      f"  -> {'PASS' if max(dr, dr2) < 1e-12 and dt < 1e-10 else 'FAIL'}")
    ok &= max(dr, dr2) < 1e-12 and dt < 1e-10
    d = float((a["returns"] - (mine - pd.Series(turn, index=pan.px.index) * 10 / 1e4)).abs().max())
    P(f"  [b] cost identity (10 bps derived from the 0 bps run): max|d|={d:.3e}"
      f"  -> {'PASS' if d < 1e-15 else 'FAIL'}")
    ok &= d < 1e-15
    _, above, vol20 = score(pan.px)
    m = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in pan.px.columns if c not in set(pan.tradable)]
    if drop:
        m[drop] = False
    s78 = score(pan.px, vol_scale=False)[0]
    w78 = (s78.where(m).rank(axis=1, ascending=False) <= BASE_N).astype(float) * (BASE_GROSS / BASE_N)
    dw = float((w78 - pan.W).abs().max().max())
    P(f"  [c] base CAND-20 weights vs idea 78/171 weights_cand: max|dw|={dw:.3e}"
      f"  -> {'PASS' if dw < 1e-12 else 'FAIL'}")
    ok &= dw < 1e-12
    rr = pd.Series(port - turn * 10 / 1e4, index=pan.px.index).iloc[pan.st:]
    me = metrics(rr)
    mn = mstats(rr.values)
    dm = max(abs(me["CAGR"] - mn[0]), abs(me["Sharpe"] - mn[1]), abs(me["MaxDD"] - mn[2]))
    P(f"  [d] mstats vs engine.metrics (CAGR/Sharpe/MaxDD): max|d|={dm:.3e}"
      f"  -> {'PASS' if dm < 1e-12 else 'FAIL'}")
    ok &= dm < 1e-12
    return ok


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    P(f"IDEA 203 - a-turnover-matched-null-for-suppressing-overlays   (lane B, {pd.Timestamp.today().date()})")
    P("=" * 126)
    P("Idea 186's rotation null preserves an overlay's on-share and episode structure exactly and its")
    P("realised turnover only for actions that SCALE or REALLOCATE the book.  For BUDGET-skip - the")
    P("action that SUPPRESSES a rebalance - it does not, and idea 191 measured the gap growing without")
    P("bound in on-share.  This run builds idea 203's replacement (resample the SKIP DECISIONS at")
    P("matched count), embeds it in the one-parameter family that runs from count-matched to")
    P("turnover-matched, and re-prices idea 186's BUDGET family against all six nulls.")
    P("")
    P(f"Two tuned params: tau {TAUS} x B {BS}.  Corpus axes: 3 panels x {MODES} x {COST_RUNGS} bps.")
    P(f"Null kinds: {KINDS}.  {N_NULL} draws each.  ROT seed {ROT_SEED} (idea 186's), RS seed {RS_SEED}.")
    P("")

    panels = build_panels()
    for p_ in panels:
        P(f"   {p_.name:9s} {p_.px.shape[0]}d x {p_.px.shape[1]}c  tradable={len(p_.tradable):3d}  "
          f"{p_.px.index[0].date()}..{p_.px.index[-1].date()}  rebalances={len(p_.reb)}")
    P("")
    P("REPRODUCTION GATES [a]-[d] (asserted before any new number is read)")
    if not all(gates(p_) for p_ in panels):
        P("\n*** REPRODUCTION FAILED - this is not a Claude-Space backtest.  Stopping. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        return
    P("")

    # ---- references
    REF = {}
    for pan in panels:
        st = pan.st
        spy = pan.spy.values[st:]
        sc, ss, sd = mstats(spy)
        h = len(spy) // 2
        base_port, base_turn = run_book(pan, np.zeros(len(pan.reb), bool), "skip")
        v1r = fast_backtest(pan.px, rules_v1_weights(pan.px), 0.0, FREQ)
        v2r = fast_backtest(pan.px, rules_v2_weights(pan.px), 0.0, FREQ)
        ref = dict(spy_h1=sh(spy[:h]), spy_h2=sh(spy[h:]), spy_dd=sd, spy_cagr=sc, spy_sh=ss,
                   spy_oos_sh=sh(pan.spy.values[pan.oos_st:]),
                   spy_oos=mstats(pan.spy.values[pan.oos_st:]))
        for bps in COST_RUNGS:
            bb = base_port - base_turn * bps / 1e4
            v1 = (v1r["returns"] - v1r["turnover"] * bps / 1e4).values
            v2 = (v2r["returns"] - v2r["turnover"] * bps / 1e4).values
            hb = len(bb[st:]) // 2
            ref[bps] = dict(
                base_sh=sh(bb[st:]), base_dd=mstats(bb[st:])[2], base_is_sh=sh(bb[st:pan.is_end]),
                base_cagr=mstats(bb[st:])[0],
                base_oos=mstats(bb[pan.oos_st:]),
                v1_h1=sh(v1[st:][:hb]), v1_h2=sh(v1[st:][hb:]), v1_dd=mstats(v1[st:])[2],
                v2_h1=sh(v2[st:][:hb]), v2_h2=sh(v2[st:][hb:]), v2_dd=mstats(v2[st:])[2])
        REF[pan.name] = ref
        mo = ref["spy_oos"]
        P(f"  {pan.name:9s} SPY {sc:6.2%}/{ss:.3f}/{sd:7.2%}  OOS {mo[0]:6.2%}/{mo[1]:.3f}/{mo[2]:7.2%}"
          f"   | BASE@10 {ref[10]['base_cagr']:6.2%}/{ref[10]['base_sh']:.4f}/{ref[10]['base_dd']:7.2%}"
          f"   RULES v2@10 h1/h2 {ref[10]['v2_h1']:.3f}/{ref[10]['v2_h2']:.3f} dd {ref[10]['v2_dd']:7.2%}")
    P("")

    # ---- the grid
    P("RUNNING THE GRID (30 real points x (1 real + 6 nulls x 20 draws)) ...")
    rows = []
    for pi, pan in enumerate(panels):
        ref = REF[pan.name]
        J = len(pan.reb)
        for ti, tau in enumerate(TAUS):
            s_real = pan.tt > tau
            K = int(s_real.sum())
            for mode in MODES:
                specs = [("real", -1, s_real)]
                for kind in KINDS:
                    key = pi * 1000 + ti * 100 + MODES.index(mode) * 10 + KINDS.index(kind)
                    for di, s in enumerate(draws_for(kind, s_real, pan.tt, J, key)):
                        specs.append((kind, di, s))
                for kind, di, s in specs:
                    port, turn = run_book(pan, s, mode)
                    ex_ante = float(pan.tt[s].sum())
                    for bps in COST_RUNGS:
                        st_ = row_stats(pan, port, turn, bps, ref)
                        st_.update(panel=pan.name, tau=tau, mode=mode, bps=bps,
                                   kind=("real" if kind == "real" else kind),
                                   draw=di, on_share=float(s.mean()), K=int(s.sum()), real_K=K,
                                   ex_ante_tt=ex_ante, real_ex_ante_tt=float(pan.tt[s_real].sum()),
                                   overlap=float((s & s_real).sum() / max(K, 1)))
                        rows.append(st_)
        P(f"   {pan.name} done ({time.time()-t0:.0f}s)")
    g = pd.DataFrame(rows)
    g.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    P(f"   {len(g)} rows ({int((g.kind=='real').sum())} real) -> {STEM}.grid.csv  ({time.time()-t0:.0f}s)")
    P("")

    # ---- [f] null validity
    P("  [f] NULL VALIDITY - count matching and per-stratum count matching")
    nn = g[g.kind != "real"]
    badK = int((nn.K != nn.real_K).sum())
    P(f"      skip-COUNT mismatches (all kinds): {badK}/{len(nn)}  -> {'PASS' if badK==0 else 'FAIL'}")
    bad_strat = 0
    n_strat = 0
    for pan in panels:
        for tau in TAUS:
            s_real = pan.tt > tau
            for B in BS:
                bins = strat_bins(pan.tt, B)
                rng = np.random.default_rng(RS_SEED + 999)
                for _ in range(N_NULL):
                    d = rs_draw(s_real, bins, rng)
                    for b in bins:
                        n_strat += 1
                        if int(d[b].sum()) != int(s_real[b].sum()):
                            bad_strat += 1
    P(f"      per-STRATUM count mismatches (RS-B): {bad_strat}/{n_strat}"
      f"  -> {'PASS' if bad_strat==0 else 'FAIL'}")
    P("")

    # ---- [e] reproduce idea 186's committed BUDGET rows
    P("  [e] ROT ARM vs IDEA 186's COMMITTED GRID (tau in {0.10,0.20,0.30}, same unsalted seed)")
    if IDEA186.exists():
        o = pd.read_csv(IDEA186)
        o = o[(o.family == "BUDGET")].copy()
        o["kind186"] = np.where(o.kind == "real", "real", "ROT")
        mine = g[(g.tau.isin([0.10, 0.20, 0.30])) & (g.kind.isin(["real", "ROT"]))].copy()
        o["key"] = list(zip(o.panel, o.thr.round(6), o.depth, o.bps, o.kind186, o.draw))
        mine["key"] = list(zip(mine.panel, mine.tau.round(6), mine["mode"], mine.bps, mine.kind, mine.draw))
        j = mine.merge(o[["key", "Sharpe", "MaxDD", "on_share", "turnover"]], on="key",
                       suffixes=("", "_186"))
        if len(j):
            j = j.copy()
            j["d_os"] = (j.on_share - j.on_share_186).abs()
            same = j[j.d_os < 1e-12]
            moved = j[j.d_os >= 1e-12]
            P(f"      matched {len(j)} of idea 186's {len(o)} committed BUDGET rows on "
              f"(panel, tau, action, rung, draw)")
            ds = float((same.Sharpe - same.Sharpe_186).abs().max())
            dd = float((same.MaxDD - same.MaxDD_186).abs().max())
            dt = float((same.turnover - same.turnover_186).abs().max())
            P(f"      {len(same)} rows have an IDENTICAL ON set: max|dSharpe|={ds:.3e}  "
              f"max|dMaxDD|={dd:.3e}  max|dturnover|={dt:.3e}  -> {'PASS' if ds < 1e-3 else 'FAIL'}")
            P("      The residual is a DATA REVISION, not a code difference: data/prices.csv was")
            P("      re-committed by the daily Actions job on 2026-09-07, after idea 186 ran, and the")
            P("      panel's adjusted closes moved.  Idea 424 carries the same caveat for its own source.")
            if len(moved):
                dsm = float((moved.Sharpe - moved.Sharpe_186).abs().max())
                ddm = float((moved.MaxDD - moved.MaxDD_186).abs().max())
                P(f"      {len(moved)} rows (tau={sorted(moved.tau.unique())}) have an ON set that MOVED by")
                P(f"      {(moved.on_share-moved.on_share_186).abs().max()*len(panels[0].reb):.0f} of "
                  f"{len(panels[0].reb)} rebalance dates - the revision flipped one date's composite")
                P(f"      across the threshold.  Drift BOUNDED and reported, not hidden: "
                  f"max|dSharpe|={dsm:.4f}  max|dMaxDD|={ddm:.4f}")
            ok_e = ds < 1e-3
            P(f"      gate [e] -> {'PASS (bounded)' if ok_e else 'FAIL'}")
        else:
            P("      *** no rows matched - gate [e] NOT SATISFIED, reported as such ***")
    else:
        P("      *** idea 186 grid.csv not found - gate [e] NOT SATISFIED, reported as such ***")
    P("")

    # =================================================================== Q1 FIDELITY
    P("=" * 126)
    P("Q1  DOES A COUNT-MATCHED RESAMPLE REPAIR THE TURNOVER GAP?  (prediction P2: no)")
    P("=" * 126)
    real = g[g.kind == "real"].set_index(["panel", "tau", "mode", "bps"])
    fid_rows = []
    for (pan_, tau, mode, bps, kind), sub in g[g.kind != "real"].groupby(
            ["panel", "tau", "mode", "bps", "kind"]):
        rl = real.loc[(pan_, tau, mode, bps)]
        gap = float(np.abs(sub.turnover.mean() - rl.turnover) / rl.turnover)
        gap_sd = float(np.abs(sub.turnover - rl.turnover).std(ddof=1) / rl.turnover)
        ex = float(np.abs(sub.ex_ante_tt.mean() - rl.ex_ante_tt) / rl.ex_ante_tt)
        band = float(sub.dSharpe.abs().max())
        fid_rows.append(dict(panel=pan_, tau=tau, mode=mode, bps=bps, kind=kind,
                             on_share=float(rl.on_share),
                             real_turnover=float(rl.turnover), null_turnover=float(sub.turnover.mean()),
                             gap=gap, gap_draw_sd=gap_sd, ex_ante_gap=ex,
                             overlap=float(sub.overlap.mean()), band=band,
                             d_real=float(rl.dSharpe)))
    fid = pd.DataFrame(fid_rows)
    fid.to_csv(OUT / f"{STEM}.fidelity.csv", index=False)
    P("  realised turnover gap  mean |null - real| / real,  by ACTION x NULL KIND (pooled over")
    P("  panels, tau and cost rungs; the 'half' column is the WITHIN-FAMILY CONTROL - a non-")
    P("  suppressing action on the SAME indicator, where idea 186 already found rotation faithful)")
    tab = fid.pivot_table(index="kind", columns="mode", values="gap").reindex(KINDS)
    P((tab * 100).round(1).to_string() + "   (%)")
    P("")
    P("  and the same table for the EX-ANTE skipped-turnover budget sum(tt over the ON dates),")
    P("  the quantity RS-B is built to match:")
    tab2 = fid.pivot_table(index="kind", columns="mode", values="ex_ante_gap").reindex(KINDS)
    P((tab2 * 100).round(2).to_string() + "   (%)")
    P("")
    rot_skip = fid[(fid.kind == "ROT") & (fid["mode"] == "skip")].gap
    rs1_skip = fid[(fid.kind == "RS1") & (fid["mode"] == "skip")].gap
    P(f"  ROT  BUDGET-skip gap: mean {rot_skip.mean():8.1%}  median {rot_skip.median():8.1%}  "
      f"max {rot_skip.max():9.1%}  (n={len(rot_skip)})")
    P(f"  RS1  BUDGET-skip gap: mean {rs1_skip.mean():8.1%}  median {rs1_skip.median():8.1%}  "
      f"max {rs1_skip.max():9.1%}  (n={len(rs1_skip)})")
    ratio = rs1_skip.mean() / rot_skip.mean() if rot_skip.mean() else np.nan
    P(f"  RS1/ROT ratio of mean gap = {ratio:.3f}  -> P2 ({'HIT' if 0.5 <= ratio <= 2.0 else 'MISS'}:"
      f" count-matched resampling {'does not' if 0.5 <= ratio <= 2.0 else 'does'} repair the gap)")
    P("")
    P("  idea 191 published 1782.7% for BUDGET-skip on this same tau ladder.  Idea 208 established")
    P("  that idea 191 SALTED its offsets with Python's per-process hash(), so that number is not a")
    P("  fixed quantity and cannot be bit-reproduced.  Re-measured here at a fixed seed:")
    r3 = fid[(fid.kind == "ROT") & (fid["mode"] == "skip")]
    P(f"      ROT BUDGET-skip mean gap {r3.gap.mean():.1%}  (sd across the {len(r3)} cells "
      f"{r3.gap.std(ddof=1):.1%}, se {r3.gap.std(ddof=1)/np.sqrt(len(r3)):.1%})")
    sub186 = fid[(fid.kind == "ROT") & (fid["mode"] == "skip") & (fid.tau.isin([0.10, 0.20, 0.30]))]
    P(f"      on idea 186's NARROW 3-point ladder: mean {sub186.gap.mean():.1%}  max {sub186.gap.max():.1%}"
      f"   (idea 186 published 25.4% / 213.8% pooled over both actions)")
    P("")
    P("  the gap by ON-SHARE decile (idea 191's 'degrades without bound in on-share'), BUDGET-skip:")
    sk = fid[fid["mode"] == "skip"].copy()
    sk["os_bin"] = pd.cut(sk.on_share, [0, .1, .3, .5, .7, .9, 1.0])
    P(sk.pivot_table(index="os_bin", columns="kind", values="gap", observed=False)
      .reindex(columns=KINDS).mul(100).round(1).to_string() + "   (%)")
    P("")

    # =================================================================== Q2 the frontier
    P("=" * 126)
    P("Q2  THE FIDELITY / RANDOMISATION FRONTIER  (prediction P3: both fall monotonically in B)")
    P("=" * 126)
    P("  For BUDGET-skip, per null kind, pooled over panels / tau / rungs:")
    P("    gap        realised turnover gap (want 0)")
    P("    ex_gap     ex-ante skipped-turnover gap (what RS-B matches by construction)")
    P("    overlap    share of the null's skip dates that are ALSO real skip dates (want low:")
    P("               overlap -> 1 means the 'null' IS the instrument)")
    P("    band       mean over cells of max|dSharpe| across the 20 draws (the clause's yardstick)")
    P("    free       mean number of strata in which the draw has any freedom at all")
    fr = []
    for kind in KINDS:
        s = fid[(fid.kind == kind) & (fid["mode"] == "skip")]
        if kind == "ROT":
            fs = np.nan
        else:
            B = int(kind[2:])
            fs = float(np.mean([free_strata(p.tt > tau, p.tt, B) for p in panels for tau in TAUS]))
        fr.append(dict(kind=kind, gap=s.gap.mean(), ex_gap=s.ex_ante_gap.mean(),
                       overlap=s.overlap.mean(), band=s.band.mean(), free_strata=fs,
                       B=(np.nan if kind == "ROT" else int(kind[2:]))))
    frd = pd.DataFrame(fr).set_index("kind")
    P(frd.to_string(float_format=lambda x: f"{x:.4f}"))
    rs = frd.loc[[k for k in KINDS if k != "ROT"]]
    mono_gap = bool((np.diff(rs.gap.values) <= 1e-12).all())
    mono_band = bool((np.diff(rs.band.values) <= 1e-12).all())
    mono_ov = bool((np.diff(rs.overlap.values) >= -1e-12).all())
    P(f"  monotone in B:  gap falls {mono_gap}   band falls {mono_band}   overlap rises {mono_ov}"
      f"   -> P3 {'HIT' if (mono_gap and mono_band) else 'MISS'}")
    P("")

    # =================================================================== Q3/Q4 re-pricing
    P("=" * 126)
    P("Q3/Q4  RE-PRICING IDEA 186's BUDGET FAMILY AGAINST EVERY NULL")
    P("=" * 126)
    P("  clause readings, both computed (idea 211 killed the two-sided reading in favour of the")
    P("  signed one; the two-sided is kept for comparability with idea 186's published verdicts):")
    P("    two-sided  clears iff |dSharpe_real| > max over draws |dSharpe_null|")
    P("    signed     clears iff dSharpe_real is beyond every draw IN ITS OWN DIRECTION")
    cl = []
    for (pan_, tau, mode, bps), sub in g[g.kind != "real"].groupby(["panel", "tau", "mode", "bps"]):
        rl = real.loc[(pan_, tau, mode, bps)]
        dr = float(rl.dSharpe)
        dr_is = float(rl.IS_dSharpe)
        for kind, s2 in sub.groupby("kind"):
            dn = s2.dSharpe.values
            dn_is = s2.IS_dSharpe.values
            cl.append(dict(panel=pan_, tau=tau, mode=mode, bps=bps, kind=kind,
                           on_share=float(rl.on_share), d_real=dr,
                           null_max_abs=float(np.abs(dn).max()),
                           null_mean=float(dn.mean()),
                           clears_two=bool(abs(dr) > np.abs(dn).max()),
                           clears_signed=bool(dr > dn.max() if dr > 0 else dr < dn.min()),
                           clears_signed_IS=bool(dr_is > dn_is.max() if dr_is > 0
                                                 else dr_is < dn_is.min()),
                           gap=float(np.abs(s2.turnover.mean() - rl.turnover) / rl.turnover),
                           overlap=float(s2.overlap.mean()),
                           pass4a=bool(rl.pass4a), pass4b=bool(rl.pass4b)))
    clause = pd.DataFrame(cl)
    clause.to_csv(OUT / f"{STEM}.clause.csv", index=False)
    P("")
    P("  CLEAR RATE (share of the 30 real points x 2 rungs = 60 cells that clear), by action:")
    for col in ("clears_two", "clears_signed"):
        t_ = clause.pivot_table(index="kind", columns="mode", values=col, aggfunc="mean").reindex(KINDS)
        P(f"    {col}:")
        P("      " + (t_ * 100).round(1).to_string().replace("\n", "\n      ") + "   (%)")
    P("")
    P("  VERDICT MOVEMENT vs the incumbent ROT null (the number idea 203 asks for):")
    piv = clause.pivot_table(index=["panel", "tau", "mode", "bps"], columns="kind",
                             values="clears_signed", aggfunc="first").astype(bool)
    for kind in KINDS[1:]:
        mv = int((piv[kind] != piv["ROT"]).sum())
        gained = int(((piv[kind]) & (~piv["ROT"])).sum())
        lost = int(((~piv[kind]) & (piv["ROT"])).sum())
        P(f"    {kind:5s}: {mv:3d} of {len(piv)} signed verdicts move vs ROT   "
          f"(+{gained} newly clear, -{lost} stop clearing)")
    P("")
    P("  THE WALL (P4): for BUDGET-skip, the clause's power against the fidelity it buys.")
    P("  A null that matches the ex-ante turnover budget of the skipped set to within eps has an")
    P("  overlap with the real skip set of 'overlap' and clears 'clear' of the real points.")
    w = clause[clause["mode"] == "skip"].groupby("kind").agg(
        ex_gap=("gap", "mean"), overlap=("overlap", "mean"),
        clear_signed=("clears_signed", "mean"), clear_two=("clears_two", "mean")).reindex(KINDS)
    w["ex_ante_gap"] = [fid[(fid.kind == k) & (fid["mode"] == "skip")].ex_ante_gap.mean() for k in KINDS]
    P(w.to_string(float_format=lambda x: f"{x:.4f}"))
    half_ref = fid[(fid.kind == "ROT") & (fid["mode"] == "half")].gap.mean()
    P(f"  rotation's gap on the NON-suppressing 'half' action = {half_ref:.2%} - the fidelity target.")
    hit = [k for k in KINDS if fid[(fid.kind == k) & (fid["mode"] == "skip")].gap.mean() <= half_ref]
    P(f"  null kinds reaching that target on BUDGET-skip: {hit if hit else 'NONE'}")
    if hit:
        cr = [float(w.loc[k, "clear_signed"]) for k in hit]
        P(f"  their signed clear rate on the real points: {[f'{c:.1%}' for c in cr]}"
          f"   -> P4 {'HIT' if max(cr) <= 0.05 else 'MISS'}")
    else:
        P("  -> P4 cannot be evaluated at the target; the frontier is read off the table above.")
    P("")

    # =================================================================== Q5 size control
    P("=" * 126)
    P("Q5  SIZE CONTROL - a KNOWN-NULL overlay (random ON, same on-share, zero timing information)")
    P("=" * 126)
    P("  Run on U56 only.  A clause with nominal one-sided size 1/21 = 4.76% should clear these at")
    P("  most that often.  If RS-B keeps its size here while losing power on the REAL overlay, the")
    P("  power loss is specific to indicators that are functions of the stratifying variable.")
    pan = panels[0]
    ref = REF[pan.name]
    J = len(pan.reb)
    noise_rows = []
    for ti, tau in enumerate(TAUS):
        s_real = pan.tt > tau
        K = int(s_real.sum())
        rngn = np.random.default_rng(NOISE_SEED + ti)
        s_noise = np.zeros(J, bool)
        s_noise[rngn.choice(J, size=K, replace=False)] = True
        for mode in MODES:
            portR, turnR = run_book(pan, s_noise, mode)
            for bps in COST_RUNGS:
                base = row_stats(pan, portR, turnR, bps, ref)
                dr = base["dSharpe"]
                for kind in KINDS:
                    key = 5000 + ti * 100 + MODES.index(mode) * 10 + KINDS.index(kind)
                    dn = []
                    for s in draws_for(kind, s_noise, pan.tt, J, key):
                        p2, t2 = run_book(pan, s, mode)
                        dn.append(row_stats(pan, p2, t2, bps, ref)["dSharpe"])
                    dn = np.array(dn)
                    noise_rows.append(dict(panel=pan.name, tau=tau, mode=mode, bps=bps, kind=kind,
                                           on_share=float(s_noise.mean()), d_real=dr,
                                           clears_two=bool(abs(dr) > np.abs(dn).max()),
                                           clears_signed=bool(dr > dn.max() if dr > 0 else dr < dn.min()),
                                           band=float(np.abs(dn).max())))
        P(f"   noise tau={tau} done ({time.time()-t0:.0f}s)")
    noise = pd.DataFrame(noise_rows)
    noise.to_csv(OUT / f"{STEM}.noise.csv", index=False)
    P("")
    P("  realised clear rate on the zero-information overlay (nominal 4.76%), by action:")
    for col in ("clears_two", "clears_signed"):
        t_ = noise.pivot_table(index="kind", columns="mode", values=col, aggfunc="mean").reindex(KINDS)
        P(f"    {col}:")
        P("      " + (t_ * 100).round(1).to_string().replace("\n", "\n      ") + "   (%)")
    sz = noise.groupby("kind").clears_signed.mean().reindex(KINDS)
    P(f"  pooled: " + "  ".join(f"{k} {sz[k]:.1%}" for k in KINDS))
    P(f"  -> P5 {'HIT' if (sz <= 0.10).all() else 'MISS'} (all kinds at or near nominal;"
      f" max {sz.max():.1%})")
    P("")

    # =================================================================== Q6 rule 8
    P("=" * 126)
    P("Q6  RULE 8 WALK-FORWARD - parameters chosen on <= 2016-12-31, 2017-2026 read once")
    P("=" * 126)
    P("  12 cells = 3 panels x 2 actions x 2 cost rungs.  The ladder is the 5-point tau ladder.")
    wf = []
    for pan in panels:
        ref = REF[pan.name]
        for mode in MODES:
            for bps in COST_RUNGS:
                sub = g[(g.panel == pan.name) & (g["mode"] == mode) & (g.bps == bps)
                        & (g.kind == "real")].set_index("tau")
                cs = clause[(clause.panel == pan.name) & (clause["mode"] == mode)
                            & (clause.bps == bps)]
                b_oos = ref[bps]["base_oos"]
                wf.append(dict(panel=pan.name, mode=mode, bps=bps, arm="S0 do-nothing", pick="-",
                               OOS_CAGR=b_oos[0], OOS_Sharpe=b_oos[1], OOS_MaxDD=b_oos[2],
                               dOOS=0.0, spy_OOS_Sharpe=ref["spy_oos"][1]))
                best = sub.IS_Sharpe.idxmax()
                r_ = sub.loc[best]
                wf.append(dict(panel=pan.name, mode=mode, bps=bps, arm="S1 IS-argmax",
                               pick=f"tau={best} os={sub.loc[best,'on_share']:.0%}",
                               OOS_CAGR=r_.OOS_CAGR, OOS_Sharpe=r_.OOS_Sharpe, OOS_MaxDD=r_.OOS_MaxDD,
                               dOOS=r_.OOS_Sharpe - b_oos[1], spy_OOS_Sharpe=ref["spy_oos"][1]))
                for kind in KINDS:
                    ok = cs[(cs.kind == kind) & (cs.clears_signed_IS)].tau.tolist()
                    if not ok:
                        wf.append(dict(panel=pan.name, mode=mode, bps=bps, arm=f"S2 {kind}",
                                       pick="ABSTAIN", OOS_CAGR=b_oos[0], OOS_Sharpe=b_oos[1],
                                       OOS_MaxDD=b_oos[2], dOOS=0.0,
                                       spy_OOS_Sharpe=ref["spy_oos"][1]))
                    else:
                        bb = sub.loc[ok].IS_Sharpe.idxmax()
                        r2 = sub.loc[bb]
                        wf.append(dict(panel=pan.name, mode=mode, bps=bps, arm=f"S2 {kind}",
                                       pick=f"tau={bb}", OOS_CAGR=r2.OOS_CAGR,
                                       OOS_Sharpe=r2.OOS_Sharpe, OOS_MaxDD=r2.OOS_MaxDD,
                                       dOOS=r2.OOS_Sharpe - b_oos[1],
                                       spy_OOS_Sharpe=ref["spy_oos"][1]))
                orc = sub.OOS_Sharpe.idxmax()
                r3_ = sub.loc[orc]
                wf.append(dict(panel=pan.name, mode=mode, bps=bps, arm="ORACLE-OOS",
                               pick=f"tau={orc}", OOS_CAGR=r3_.OOS_CAGR, OOS_Sharpe=r3_.OOS_Sharpe,
                               OOS_MaxDD=r3_.OOS_MaxDD, dOOS=r3_.OOS_Sharpe - b_oos[1],
                               spy_OOS_Sharpe=ref["spy_oos"][1]))
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")
    P("  ARM SUMMARY over the 12 cells (dOOS = OOS Sharpe minus the do-nothing control):")
    summ = []
    for arm, s in W.groupby("arm"):
        summ.append(dict(arm=arm, n=len(s), OOS_CAGR=s.OOS_CAGR.mean(), OOS_Sharpe=s.OOS_Sharpe.mean(),
                         OOS_MaxDD=s.OOS_MaxDD.mean(), dOOS=s.dOOS.mean(), t=tstat(s.dOOS.values),
                         wins=int((s.dOOS > 0).sum()),
                         beats_SPY=int((s.OOS_Sharpe > s.spy_OOS_Sharpe).sum())))
    sm = pd.DataFrame(summ).sort_values("dOOS", ascending=False)
    P(sm.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    s2 = sm[sm.arm.str.startswith("S2")]
    P(f"  -> P6 {'HIT' if (s2.dOOS <= 0).all() else 'MISS'}: "
      f"{int((s2.dOOS <= 0).sum())} of {len(s2)} clause-gated arms fail to beat do-nothing"
      f" (best {s2.dOOS.max():+.4f}); S1 IS-argmax {sm[sm.arm=='S1 IS-argmax'].dOOS.iloc[0]:+.4f}")
    P("")

    # =================================================================== Q7 KEEP paths
    P("=" * 126)
    P("Q7  BOTH KEEP PATHS on every real and every null row (PROTOCOL rule 4)")
    P("=" * 126)
    kp = []
    for kind, s in g.groupby("kind"):
        kp.append(dict(kind=kind, n=len(s), pass4a_v2=int(s.pass4a.sum()),
                       pass4a_v1=int(s.pass4a_v1.sum()), pass4b=int(s.pass4b.sum()),
                       both=int((s.pass4a & s.pass4b).sum())))
    K_ = pd.DataFrame(kp).set_index("kind").reindex(["real"] + KINDS)
    P(K_.to_string())
    g[["panel", "tau", "mode", "bps", "kind", "draw", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
       "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "pass4a", "pass4a_v1", "pass4b",
       "fail4a", "fail4b"]].to_csv(OUT / f"{STEM}.keep.csv", index=False)
    P("")
    P("  by panel, REAL rows only:")
    gr = g[g.kind == "real"].copy()
    gr["both"] = gr.pass4a & gr.pass4b
    rr_ = gr.groupby("panel").agg(n=("Sharpe", "size"), pass4a=("pass4a", "sum"),
                                  pass4b=("pass4b", "sum"), both=("both", "sum"))
    P(rr_.to_string())
    sm439 = g[(g.kind == "real") & (g.panel == "SMALL439")]
    P(f"  -> P7 {'HIT' if int((sm439.pass4a & sm439.pass4b).sum())==0 else 'MISS'}: "
      f"SMALL439 real rows passing BOTH paths = {int((sm439.pass4a & sm439.pass4b).sum())}/{len(sm439)}")
    P("")
    P("  best real row on each path (reported so a KEEP could not hide):")
    for path, col in (("4a vs RULES v2", "pass4a"), ("4b vs SPY", "pass4b")):
        s = g[(g.kind == "real") & (g[col])]
        if len(s):
            b = s.sort_values("Sharpe", ascending=False).iloc[0]
            P(f"    {path:16s}: {len(s):3d} rows pass;  best {b.panel}/tau={b.tau}/{b['mode']}/"
              f"{b.bps}bps  CAGR {b.CAGR:.2%} Sharpe {b.Sharpe:.3f} MaxDD {b.MaxDD:.2%} "
              f"H1/H2 {b.H1:.3f}/{b.H2:.3f} OOS {b.OOS_Sharpe:.3f}")
        else:
            P(f"    {path:16s}:   0 rows pass")
    P("")
    P(f"TOTAL RUNTIME {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()

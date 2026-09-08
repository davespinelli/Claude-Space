#!/usr/bin/env python3
"""QUEUE idea 434 - does-the-FREE-STRATUM-COUNT-generalise-as-a-null-power-certificate
   (cloud lane, 2026-09-08).

QUESTION (pre-registered, verbatim from QUEUE.md idea 434)
    "idea 203 found `free_strata` (strata in which a stratified null's draw has any freedom at
     all) is identically 1 for a threshold indicator, and 0 in 1 of 15 cells where the 'null'
     becomes bit-identical to the instrument.  Test whether free-stratum count (or its continuous
     twin, the overlap with the real ON set) predicts a null's realised power across the record's
     committed null claims, i.e. whether it is the missing certificate that says a clause verdict
     was falsifiable at all.  Max 2 params."

WHAT IS AT STAKE
    PROTOCOL clause 11 says a claimed overlay effect must beat a MATCHED NULL.  If the null's
    draws are so close to the real ON set that they carry the same information, the clause cannot
    reject anything and a "did not clear" verdict is uninformative rather than negative.  Idea 203
    built RS-B (an ex-ante-turnover-stratified resample) and noticed the collapse but measured it
    on ONE instrument shape (a threshold on the stratifying variable), where free_strata == 1 by
    construction.  Idea 434 asks whether the count GENERALISES: is it a certificate that can be
    printed beside any clause verdict, on any instrument, and read as "this test had power"?

    A certificate must do two things.  (i) When the instrument is genuinely informative, a null
    with a healthy certificate must CLEAR (power).  (ii) When the instrument carries no timing
    information, the same null must NOT clear more than nominally often (size).  This run measures
    both, on instruments whose information content is KNOWN by construction, and then asks which
    statistic - the discrete free-stratum COUNT or its continuous twin, the OVERLAP - actually
    predicts the clear rate.

DESIGN.  One base book, four instrument shapes that span the alignment dial, six nulls.

    BASE BOOK, held fixed and never tuned: idea 2's 4b candidate - top-20 equal weight on the
    scan.py composite with NO vol scaler, gross 0.75, weekly, t+1, on three panels (U56,
    BROAD136, SMALL439 = the sub-$2B panel with the tickers whose data/small_meta.csv
    max_1d_move >= 1.0 dropped first).  Idea 203's construction verbatim.

    ACTION on an ON rebalance date: `skip` (suppress the rebalance) or `half` (move half way to
    the target).  Corpus axis, not a tuned parameter.

    INSTRUMENT SHAPES, all matched to the SAME on-share pi inside a cell, so the only thing that
    moves is the instrument's ALIGNMENT with the stratifying variable tt (the untreated book's
    ex-ante target-to-target turnover) and its INFORMATION content:
        THRESH  s_j = 1[tt_j > tau(pi)]          aligned to tt, unknown information  (the record's
                                                 own BUDGET shape - idea 186/191/203)
        MIX     half the ON dates from the top-tt set, half drawn uniformly from the rest
                                                 partially aligned, unknown information
        RANDOM  a uniform draw of the same count  unaligned, ZERO information -> SIZE control
        ORACLE  the pi rebalance dates with the LARGEST 0-bps gross-return marginal of the
                treatment itself (perfect hindsight, computed in one pass - `oracle_marginal`)
                                                 unaligned, MAXIMAL information -> POWER probe
        ORAC50  half those dates, half drawn uniformly - HALF the hindsight
        ORAC_W  the NEXT tranche of marginals (ranks k..2k) - weaker information, still real
                ORACLE / ORAC50 / ORAC_W are a GRADED power ladder: without it a saturated
                clear rate would make the certificate question unfalsifiable.

    NULLS priced on every point (6):
        ROT          idea 186's circular rotation of s               (the record's incumbent)
        RS1..RS16    idea 203's ex-ante-turnover-stratified resample at B = 1, 2, 4, 8, 16
                     (B = 1 is the count-matched uniform draw)

    CERTIFICATES computed for every (instrument, null) pair:
        free_strata  strata in which the draw has any freedom at all (0 < k_b < |b|).  NaN for
                     ROT, which does not stratify.
        overlap      mean over draws of |draw & s| / |s|.  An UNALIGNED null of share pi has
                     expected overlap pi, so the reported inflation factor is overlap / pi.
        The pre-registered, parameter-free certificate rule is  overlap <= 2 * pi  (the null is
        no more than twice as aligned as chance), with free_strata >= 2 as its discrete twin.
        Neither threshold is tuned or searched.

TUNED PARAMETERS - exactly two, per PROTOCOL rule 4.  ALL grid points reported.
    1. pi, the ON-share of the instrument: {0.10, 0.25, 0.50, 0.75}
    2. B, the stratum count of the null:   {1, 2, 4, 8, 16}
    PANEL, ACTION, FAMILY, COST RUNG and NULL KIND are corpus axes, not tuned parameters.  The
    rule-8 selector below is the only place a point is ever chosen, and it chooses on IS alone.

COSTS.  Every book is run ONCE at 0 bps; the 10 and 25 bps rungs are derived from the engine's own
    turnover series (net = gross - turnover * bps / 1e4), asserted exact in gate [b].

WALK-FORWARD (PROTOCOL rule 8), 12 cells = 3 panels x 2 actions x 2 cost rungs.  Parameters chosen
    on <= 2016-12-31 only; 2017-2026 read once.  Arms:
        S0          do nothing (the untreated base book)
        S1          IS-Sharpe argmax over the pi ladder (THRESH)
        S2_<kind>   the same argmax restricted to pi that CLEAR the clause on IS under that kind
        S3_<kind>   the same argmax restricted to pi that clear AND whose CERTIFICATE passes
        ORACLE_OOS  the best OOS pi read with perfect hindsight - the family's headroom
    OOS CAGR / Sharpe / MaxDD reported for every arm against the base book and against SPY.

BOTH KEEP PATHS (4a vs the LIVE RULES v2 book, 4b vs SPY) are evaluated on every real row, full
    sample, halves and OOS, and counted.

REPRODUCTION GATES, asserted before any new number is read
    [a] fast_backtest reproduces products/backtester/engine.backtest to < 1e-12
    [b] the cost identity: 10 bps derived from the 0 bps run vs a genuine 10 bps engine run = 0.0
    [c] mstats (numpy) reproduces engine.metrics to < 1e-12 on CAGR / Sharpe / MaxDD
    [d] every family's realised on-share matches its target to within one rebalance date
    [e] idea 203's collapse reproduces HERE: free_strata == 1 for THRESH at every B >= 1
    [f] the ORACLE marginal is exact: the single-date treated book's 0-bps gross return equals the
        base book's plus the claimed marginal, to < 1e-12, on a random sample of dates

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  gates [a]-[f] hold.
    P2  free_strata does NOT generalise as a certificate: for the three UNALIGNED shapes it is
        identically B (its maximum) whatever the instrument, so it varies only with the null's own
        dial and carries no instrument-specific information.  Its whole discriminating power is
        the single case idea 203 already found.
    P3  overlap DOES vary with the instrument and with B, and the clear rate FALLS as overlap
        rises, on the ORACLE (power) arm.
    P4  SIZE is at or below nominal 1/21 = 4.8% for every kind on the RANDOM arm, and does not
        rise with B - a random ON indicator is uncorrelated with tt, so stratifying on tt costs it
        no randomisation.
    P5  Under rule 8 every clause-gated arm (S2, S3) loses to S0.  Thirteen prior instances.
    P6  No row passes both KEEP paths on SMALL439 at either rung.

CAVEATS carried, not buried
    * SURVIVORSHIP: all three panels are current-constituent lists (idea 54); SMALL439 contains no
      delistings, so its LEVEL is biased upward.  Real and null draws inherit the bias identically,
      so the clear/no-clear COMPARISON is unaffected; the level of every number is not.
    * 20 draws give a nominal one-sided size of 1/21 = 4.8%; that is approximate, not exact, and
      rotation offers only J distinct nulls with correlated neighbours (idea 214).
    * ORACLE is GREEDY: the pi dates with the largest individual 0-bps gross-return marginal.
      Marginals are not additive, so the set is a LOWER BOUND on attainable effect, not an argmax.
      It is a power probe, never a strategy.
    * Idea 211's signed clause reading is primary; the two-sided reading is reported beside it.
    * Idea 38 (calendar-day index on U56/BROAD after 2014-09-17) and idea 126 (t+1 only) carry.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .cert.csv, .walkforward.csv, .keep.csv
"""
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-08_does-the-FREE-STRATUM-COUNT-generalise-as-a-null-power-certificate_cloud"
OUT = ROOT / "research" / "backtests"

COST_RUNGS = [10, 25]
MAX_VOL = 0.60
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
PHI, DELTA = 0.70, 0.60          # 4b CAGR floor / MaxDD cap, PROTOCOL rule 4b
FREQ = "W"
BASE_N, BASE_GROSS = 20, 0.75
N_NULL = 20
ROT_SEED = 186_400               # idea 186's own rotation seed
RS_SEED = 434_000
INS_SEED = 434_500

PIS = [0.10, 0.25, 0.50, 0.75]            # tuned parameter 1 (instrument on-share)
BS = [1, 2, 4, 8, 16]                     # tuned parameter 2 (strata of the null)
MODES = ["skip", "half"]
FAMS = ["THRESH", "MIX", "RANDOM", "ORACLE", "ORAC50", "ORAC_W"]
INFORMED = ["ORACLE", "ORAC50", "ORAC_W"]   # known-positive information, graded
KINDS = ["ROT"] + [f"RS{b}" for b in BS]
SLEEVE_ASSETS = ["TLT", "GLD", "UUP"]

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 4000)

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


# ---------------------------------------------------------------- metrics
def mstats(r):
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


def spearman(a, b):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    a, b = a[ok], b[ok]
    if len(a) < 4 or len(set(a.tolist())) < 2 or len(set(b.tolist())) < 2:
        return np.nan, np.nan
    ra = pd.Series(a).rank().values
    rb = pd.Series(b).rank().values
    rho = np.corrcoef(ra, rb)[0, 1]
    n = len(a)
    t = rho * np.sqrt((n - 2) / max(1e-12, 1 - rho ** 2))
    return rho, t


# ---------------------------------------------------------------- fast backtest (idea 186's)
def _core(rets, Cp, wt, m):
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


def _core_full(rets, Cp, wt, m):
    """As _core but also returns the PREVIOUS-SEGMENT return path (used by oracle_marginal)."""
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
    return (held * rets).sum(axis=1), turn, (heldp * rets).sum(axis=1), seg


def fast_backtest(prices, weights, cost_bps=0.0, freq=FREQ, mask=None):
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values if mask is None else np.asarray(mask, bool)
    m = np.concatenate([[False], m[:-1]]).copy()
    m[0] = True
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, rets.shape[1])), C[:-1]])
    port, turn = _core(rets, Cp, wt, m)
    return {"returns": pd.Series(port - turn * cost_bps / 1e4, index=idx),
            "turnover": pd.Series(turn, index=idx)}


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
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.rets = px.pct_change().fillna(0.0).values
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), C[:-1]])
        self.Wv = self.W.values
        w = self.Wv[self.reb]
        prev = np.vstack([np.zeros((1, w.shape[1])), w[:-1]])
        self.tt = np.abs(w - prev).sum(axis=1)
        self.J = len(self.reb)
        self.st = px.index.get_loc(px.index[260])
        self.is_end = int(np.searchsorted(px.index.values, np.datetime64(IS_END), "right"))
        self.oos_st = int(np.searchsorted(px.index.values, np.datetime64(OOS_START), "left"))


def build_panels():
    """Idea 186/203's panel construction VERBATIM."""
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


# ---------------------------------------------------------------- the action
def build_book(pan, s_reb, mode):
    mask = pan.mask
    Wv = pan.Wv
    if mode == "skip":
        mask = pan.mask.copy()
        mask[pan.reb[s_reb]] = False
    else:
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
    return _core(pan.rets, pan.Cp, wt, m)


# ---------------------------------------------------------------- the ORACLE marginal (one pass)
def oracle_marginal(pan):
    """Per-rebalance-date 0-bps GROSS return marginal of a SINGLE `skip`.

    Skipping rebalance j means the interval [reb[j], reb[j+1]) is held from segment start
    reb[j-1] instead of reb[j].  _core_full already computes the previous-segment return path for
    every day, so all J marginals come out of one pass.  Costs are excluded by construction: the
    criterion is a hindsight ORDERING for a power probe, not a book.
    """
    wt, m = build_book(pan, np.zeros(pan.J, bool), "skip")
    port, turn, port_prev, _ = _core_full(pan.rets, pan.Cp, wt, m)
    reb = np.flatnonzero(m)
    d = port_prev - port
    marg = np.zeros(pan.J)
    T = len(d)
    for j in range(pan.J):
        sj = pan.reb[j] + 1                       # the SHIFTED (t+1) rebalance day
        k = int(np.searchsorted(reb, sj))
        if k == 0 or k >= len(reb) or reb[k] != sj:
            continue                              # not a live segment start (first day / off panel)
        a = sj
        b = reb[k + 1] if k + 1 < len(reb) else T
        marg[j] = d[a:b].sum()
    return marg, port, turn


# ---------------------------------------------------------------- instruments
def instrument(pan, fam, pi, marg, rng):
    """ON indicator over the J rebalance dates, matched on-share pi."""
    J = pan.J
    k = int(round(pi * J))
    s = np.zeros(J, bool)
    if fam == "THRESH":
        tau = np.quantile(pan.tt, 1.0 - pi)
        s = pan.tt > tau
        # exact count match: break ties by tt order
        need = k - int(s.sum())
        if need > 0:
            cand = np.flatnonzero(~s)
            cand = cand[np.argsort(-pan.tt[cand], kind="stable")][:need]
            s[cand] = True
        elif need < 0:
            on = np.flatnonzero(s)
            on = on[np.argsort(pan.tt[on], kind="stable")][:-need]
            s[on] = False
    elif fam == "MIX":
        half = k // 2
        top = np.argsort(-pan.tt, kind="stable")[:half]
        s[top] = True
        rest = np.flatnonzero(~s)
        s[rng.choice(rest, size=k - half, replace=False)] = True
    elif fam == "RANDOM":
        s[rng.choice(J, size=k, replace=False)] = True
    elif fam == "ORACLE":
        s[np.argsort(-marg, kind="stable")[:k]] = True
    elif fam == "ORAC50":                       # half the hindsight, half noise
        half = k // 2
        s[np.argsort(-marg, kind="stable")[:half]] = True
        rest = np.flatnonzero(~s)
        s[rng.choice(rest, size=k - half, replace=False)] = True
    elif fam == "ORAC_W":                       # the NEXT tranche of marginals - weaker, still real
        start = min(k, J - k)
        s[np.argsort(-marg, kind="stable")[start:start + k]] = True
    return s


# ---------------------------------------------------------------- the nulls
def rotations(J, n, seed):
    rng = np.random.default_rng(seed)
    cand = rng.permutation(np.arange(1, J))
    return sorted(cand[:n].tolist())


def strat_bins(tt, B):
    order = np.argsort(tt, kind="stable")
    return np.array_split(order, B)


def rs_draw(s_real, bins, rng):
    out = np.zeros(len(s_real), bool)
    for b in bins:
        kb = int(s_real[b].sum())
        if kb:
            out[rng.choice(b, size=kb, replace=False)] = True
    return out


def free_strata(s_real, tt, B):
    return sum(1 for b in strat_bins(tt, B) if 0 < int(s_real[b].sum()) < len(b))


def draws_for(kind, s_real, tt, J, seed_key):
    if kind == "ROT":
        return [np.roll(s_real, o) for o in rotations(J, N_NULL, ROT_SEED)]
    B = int(kind[2:])
    bins = strat_bins(tt, B)
    rng = np.random.default_rng(RS_SEED + seed_key)
    return [rs_draw(s_real, bins, rng) for _ in range(N_NULL)]


# ---------------------------------------------------------------- KEEP paths
def keep_flags(cagr, sharpe, mdd, h1, h2, oos_sh, ref, bps):
    b = ref[bps]
    f4a = []
    if not h1 > b["v2_h1"]: f4a.append("H1")
    if not h2 > b["v2_h2"]: f4a.append("H2")
    if not mdd >= b["v2_dd"]: f4a.append("DD")
    f4b = []
    if not h1 > ref["spy_h1"]: f4b.append("H1")
    if not h2 > ref["spy_h2"]: f4b.append("H2")
    if not oos_sh > ref["spy_oos_sh"]: f4b.append("OOS")
    if not abs(mdd) <= DELTA * abs(ref["spy_dd"]): f4b.append("DD")
    if not cagr >= PHI * ref["spy_cagr"]: f4b.append("CAGR")
    return (len(f4a) == 0, ",".join(f4a) or "-", len(f4b) == 0, ",".join(f4b) or "-")


def row_stats(pan, port, turn, bps, ref):
    r = port - turn * bps / 1e4
    st = pan.st
    rr = r[st:]
    cagr, sharpe, mdd = mstats(rr)
    h = len(rr) // 2
    h1, h2 = sh(rr[:h]), sh(rr[h:])
    is_sh = sh(r[st:pan.is_end])
    oc, os_, om = mstats(r[pan.oos_st:])
    p4a, f4a, p4b, f4b = keep_flags(cagr, sharpe, mdd, h1, h2, os_, ref, bps)
    return dict(CAGR=cagr, Sharpe=sharpe, MaxDD=mdd, H1=h1, H2=h2, IS_Sharpe=is_sh,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=om,
                turnover=turn[st:].sum() / (len(rr) / 252.0),
                pass4a=p4a, fail4a=f4a, pass4b=p4b, fail4b=f4b)


# ---------------------------------------------------------------- references
def refs_for(pan):
    ref = {}
    spy = pan.spy[pan.st:]
    c, s, d = mstats(spy)
    h = len(spy) // 2
    ref.update(spy_cagr=c, spy_sh=s, spy_dd=d, spy_h1=sh(spy[:h]), spy_h2=sh(spy[h:]),
               spy_oos_sh=sh(pan.spy[pan.oos_st:]))
    for bps in COST_RUNGS:
        v2 = fast_backtest(pan.px, rules_v2_weights(pan.px), cost_bps=bps)["returns"].values
        v1 = fast_backtest(pan.px, rules_v1_weights(pan.px), cost_bps=bps)["returns"].values
        a = v2[pan.st:]
        h = len(a) // 2
        c2, s2, d2 = mstats(a)
        b1 = v1[pan.st:]
        h1_ = len(b1) // 2
        c1, s1, d1 = mstats(b1)
        ref[bps] = dict(v2_cagr=c2, v2_sh=s2, v2_dd=d2, v2_h1=sh(a[:h]), v2_h2=sh(a[h:]),
                        v2_oos_sh=sh(v2[pan.oos_st:]),
                        v1_sh=s1, v1_dd=d1, v1_h1=sh(b1[:h1_]), v1_h2=sh(b1[h1_:]))
    return ref


# ---------------------------------------------------------------- gates
def gates(pan, marg, base_port, base_turn):
    ok = True
    P(f"  --- {pan.name} ---")
    W = pan.W
    eng = backtest(pan.px, W, cost_bps=0.0, freq=FREQ)
    fst = fast_backtest(pan.px, W, cost_bps=0.0)
    nan_e = int(eng["returns"].isna().sum() + eng["turnover"].isna().sum())
    ga = max(float((eng["returns"] - fst["returns"]).abs().max()),
             float((eng["turnover"] - fst["turnover"]).abs().max()))
    # the base book run through the SAME code path the grid uses (all-OFF overlay)
    idx = pan.px.index
    dr0 = float((eng["returns"] - pd.Series(base_port, index=idx)).abs().max())
    P(f"  [a] fast_backtest/_core vs engine.backtest    max|d| = {max(ga, dr0):.3e}   "
      f"({nan_e} engine rows NaN at the first bar - engine does not fill the shift; skipped, "
      f"as idea 186/203's own checks did)")
    ok &= max(ga, dr0) < 1e-12
    eng10 = backtest(pan.px, W, cost_bps=10.0, freq=FREQ)["returns"]
    der = pd.Series(base_port - base_turn * 10 / 1e4, index=idx)
    gb = float((eng10 - der).abs().max())
    P(f"  [b] cost identity (10 bps derived vs engine)  max|d| = {gb:.3e}")
    ok &= gb < 1e-15
    rr = pd.Series(base_port, index=idx).iloc[pan.st:]
    m = metrics(rr)
    c, s, d = mstats(rr.values)
    gc = max(abs(m["CAGR"] - c), abs(m["Sharpe"] - s), abs(m["MaxDD"] - d))
    P(f"  [c] mstats vs engine.metrics                 max|d| = {gc:.3e}")
    ok &= gc < 1e-12
    # [f] the ORACLE marginal is exact on a sample of single dates
    rng = np.random.default_rng(7)
    worst = 0.0
    live = np.flatnonzero(marg != 0.0)
    for j in rng.choice(live, size=6, replace=False):
        s1 = np.zeros(pan.J, bool)
        s1[j] = True
        p1, _ = run_book(pan, s1, "skip")
        worst = max(worst, abs((p1 - base_port).sum() - marg[j]))
    P(f"  [f] ORACLE marginal exactness (6 dates)      max|d| = {worst:.3e}")
    ok &= worst < 1e-12
    return ok


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    P("=" * 118)
    P("QUEUE idea 434 - does the FREE-STRATUM COUNT generalise as a null power certificate?  (cloud, 2026-09-08)")
    P("=" * 118)
    P("Base book: idea 2's CAND-20 (top-20 EW on the scan.py composite, NO vol scaler, gross 0.75, weekly, t+1).")
    P("Tuned parameters: pi (on-share) x B (strata).  Panel/action/family/rung/kind are corpus axes.")
    P("")
    panels = build_panels()
    P("")
    P("GATES")
    allok = True
    base = {}
    for pan in panels:
        marg, bp, bt = oracle_marginal(pan)
        base[pan.name] = dict(marg=marg, port=bp, turn=bt, ref=refs_for(pan))
        allok &= gates(pan, marg, bp, bt)
    P(f"  ALL GATES {'PASS' if allok else 'FAIL'}")
    assert allok, "gates failed - no number below may be read"
    P("")

    # ---------------- the grid
    grid = []
    cert = []
    seed_key = 0
    for pidx, pan in enumerate(panels):
        d = base[pan.name]
        ref = d["ref"]
        bport, bturn = d["port"], d["turn"]
        brow = {bps: row_stats(pan, bport, bturn, bps, ref) for bps in COST_RUNGS}
        for bps in COST_RUNGS:
            r = dict(panel=pan.name, mode="-", fam="BASE", pi=np.nan, bps=bps, **brow[bps])
            grid.append(r)
        rng_i = np.random.default_rng(INS_SEED + pidx)   # NOT hash(): idea 208, salted hashes
        for mode in MODES:
            for fam in FAMS:
                for pi in PIS:
                    s = instrument(pan, fam, pi, d["marg"], rng_i)
                    share = float(s.mean())
                    port, turn = run_book(pan, s, mode)
                    rows = {bps: row_stats(pan, port, turn, bps, ref) for bps in COST_RUNGS}
                    for bps in COST_RUNGS:
                        grid.append(dict(panel=pan.name, mode=mode, fam=fam, pi=pi, bps=bps,
                                         share=share, **rows[bps]))
                    # ---- nulls
                    for kind in KINDS:
                        seed_key += 1
                        dr = draws_for(kind, s, pan.tt, pan.J, seed_key)
                        ov = float(np.mean([np.sum(x & s) / max(1, s.sum()) for x in dr]))
                        fs = (np.nan if kind == "ROT"
                              else float(free_strata(s, pan.tt, int(kind[2:]))))
                        nb = int(1 if kind == "ROT" else int(kind[2:]))
                        dsh = {bps: [] for bps in COST_RUNGS}
                        dis = {bps: [] for bps in COST_RUNGS}
                        for x in dr:
                            p2, t2 = run_book(pan, x, mode)
                            for bps in COST_RUNGS:
                                rr = p2 - t2 * bps / 1e4
                                dsh[bps].append(sh(rr[pan.st:]) - brow[bps]["Sharpe"])
                                dis[bps].append(sh(rr[pan.st:pan.is_end]) - brow[bps]["IS_Sharpe"])
                        for bps in COST_RUNGS:
                            real_d = rows[bps]["Sharpe"] - brow[bps]["Sharpe"]
                            real_is = rows[bps]["IS_Sharpe"] - brow[bps]["IS_Sharpe"]
                            arr = np.array(dsh[bps], float)
                            band_mx, band_q95 = np.nanmax(arr), np.nanquantile(arr, 0.95)
                            arr_is = np.array(dis[bps], float)
                            cert.append(dict(
                                panel=pan.name, mode=mode, fam=fam, pi=pi, kind=kind, B=nb, bps=bps,
                                free_strata=fs, overlap=ov, infl=ov / pi,
                                cert_ok=(ov <= 2 * pi), cert_disc=(np.nan if kind == "ROT" else fs >= 2),
                                d_real=real_d, band_max=band_mx, band_q95=band_q95,
                                band_sd=float(np.nanstd(arr, ddof=1)),
                                clears=bool(real_d > band_mx),
                                clears_q95=bool(real_d > band_q95),
                                clears_two=bool(abs(real_d) > np.nanmax(np.abs(arr))),
                                clears_is=bool(real_is > np.nanmax(arr_is)),
                            ))
            P(f"  {pan.name}/{mode} done  ({time.time()-t0:.0f}s)")
    G = pd.DataFrame(grid)
    C = pd.DataFrame(cert)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    C.to_csv(OUT / f"{STEM}.cert.csv", index=False)

    # ---------------- gate [d] and [e]
    P("")
    sh_err = (G[G.fam != "BASE"].share - G[G.fam != "BASE"].pi).abs().max()
    P(f"  [d] on-share match, max |realised - target| = {sh_err:.4f}  "
      f"(one rebalance date = {1/min(p.J for p in panels):.4f})")
    th = C[(C.fam == "THRESH") & (C.kind != "ROT")]
    P(f"  [e] free_strata for THRESH: unique values = {sorted(th.free_strata.unique().tolist())}  "
      f"(idea 203's collapse reproduces iff == [1.0])")
    P("")

    # ---------------- Q1: does free_strata generalise?
    P("=" * 118)
    P("Q1  DOES free_strata VARY WITH THE INSTRUMENT?  (mean free_strata by family x B; the")
    P("    certificate can only be instrument-specific if this table is not flat across rows)")
    P("=" * 118)
    t = C[C.kind != "ROT"].pivot_table(index="fam", columns="B", values="free_strata", aggfunc="mean")
    P(t.to_string(float_format=lambda x: f"{x:.2f}"))
    P("")
    P("    the same table as a FRACTION of its ceiling B (1.00 = the null has full freedom):")
    P((t / np.array(sorted(C[C.kind != 'ROT'].B.unique()))).to_string(float_format=lambda x: f"{x:.3f}"))
    P("")
    P("Q1b OVERLAP (mean |draw & s| / |s|) - the continuous twin.  An UNALIGNED null of share pi")
    P("    has expected overlap pi, so the inflation factor overlap/pi is the readable statistic.")
    t2 = C.pivot_table(index="fam", columns="kind", values="infl", aggfunc="mean")
    P(t2[KINDS].to_string(float_format=lambda x: f"{x:.3f}"))
    P("")

    # ---------------- Q2: power and size
    P("=" * 118)
    P("Q2  REALISED POWER AND SIZE.  ORACLE / ORAC50 / ORAC_W carry KNOWN, graded timing")
    P("    information by construction -> their clear rate is POWER.  RANDOM carries none -> its")
    P("    clear rate is SIZE (nominal 1/21 = 4.76%).  THRESH/MIX are the record's own shapes,")
    P("    ground truth unknown.  Realised effect sizes (mean signed d_real, primary rung):")
    P("  " + C[C.bps == 10].pivot_table(index="fam", columns="pi", values="d_real", aggfunc="mean")
      .to_string(float_format=lambda x: f"{x:+.4f}").replace("\n", "\n  "))
    P("")
    P("=" * 118)
    for lab, col in [("signed, max band (primary)", "clears"),
                     ("signed, q95 band", "clears_q95"),
                     ("two-sided, max band", "clears_two")]:
        t3 = C.pivot_table(index="fam", columns="kind", values=col, aggfunc="mean")
        P(f"  clear rate - {lab}")
        P("  " + t3[KINDS].to_string(float_format=lambda x: f"{x:.3f}").replace("\n", "\n  "))
        P("")
    P("  POWER (informed arms) and SIZE (RANDOM) by panel x kind, primary reading:")
    for fam in INFORMED + ["RANDOM"]:
        t4 = C[C.fam == fam].pivot_table(index="panel", columns="kind", values="clears", aggfunc="mean")
        P(f"  {fam}:")
        P("  " + t4[KINDS].to_string(float_format=lambda x: f"{x:.3f}").replace("\n", "\n  "))
    P("")

    # ---------------- Q3: is either statistic a certificate?
    P("=" * 118)
    P("Q3  IS EITHER STATISTIC A CERTIFICATE?  Spearman of the clear indicator on each candidate")
    P("    certificate, computed WITHIN the arm whose ground truth is known.")
    P("=" * 118)
    rows = []
    groups = [(f, C[C.fam == f]) for f in FAMS]
    groups.append(("ALL_INFORMED", C[C.fam.isin(INFORMED)]))
    groups.append(("ALL_CELLS", C))
    for fam, sub in groups:
        subrs = sub[sub.kind != "ROT"]
        r1, t1_ = spearman(subrs.free_strata, subrs.clears.astype(float))
        r2, t2_ = spearman(sub.overlap, sub.clears.astype(float))
        r3, t3_ = spearman(sub.infl, sub.clears.astype(float))
        rows.append(dict(fam=fam, n=len(sub), clear_rate=sub.clears.mean(),
                         clear_sd=sub.clears.astype(float).std(ddof=1),
                         rho_free=r1, t_free=t1_,
                         rho_overlap=r2, t_overlap=t2_, rho_infl=r3, t_infl=t3_))
    RS = pd.DataFrame(rows).set_index("fam")
    P(RS.to_string(float_format=lambda x: f"{x:+.4f}"))
    P("    (rho_* is NaN wherever the clear indicator is CONSTANT in the group - a saturated arm")
    P("     cannot falsify a certificate; that is itself the answer for those rows.)")
    P("")
    P("    clear rate SPLIT BY the pre-registered certificate rule (overlap <= 2*pi), and by its")
    P("    discrete twin (free_strata >= 2).  A certificate works iff POWER is high when it PASSES")
    P("    and low when it FAILS, while SIZE stays at nominal on both sides.")
    for fam, sub in groups:
        a = sub.groupby("cert_ok").clears.agg(["mean", "size"])
        b = sub[sub.kind != "ROT"].groupby("cert_disc").clears.agg(["mean", "size"])
        P(f"  {fam:12s} overlap<=2pi : " + " | ".join(
            f"{k}: {v['mean']:.3f} (n={int(v['size'])})" for k, v in a.iterrows()))
        P(f"  {'':12s} free_str>=2 : " + " | ".join(
            f"{k}: {v['mean']:.3f} (n={int(v['size'])})" for k, v in b.iterrows()))
    P("")

    # ---------------- Q4: rule 8 walk-forward
    P("=" * 118)
    P("Q4  RULE 8 WALK-FORWARD.  Parameters chosen on <= 2016-12-31 only; 2017-2026 read once.")
    P("    12 cells = 3 panels x 2 actions x 2 cost rungs.  Ladder = the pi grid on THRESH.")
    P("=" * 118)
    wf = []
    for pan in panels:
        d = base[pan.name]
        ref = d["ref"]
        for mode in MODES:
            for bps in COST_RUNGS:
                b = row_stats(pan, d["port"], d["turn"], bps, ref)
                cand = G[(G.panel == pan.name) & (G["mode"] == mode) & (G.fam == "THRESH")
                         & (G.bps == bps)].set_index("pi")
                cc = C[(C.panel == pan.name) & (C["mode"] == mode) & (C.fam == "THRESH")
                       & (C.bps == bps)]

                def emit(arm, pi, npool=len(PIS)):
                    if pi is None:
                        wf.append(dict(panel=pan.name, mode=mode, bps=bps, arm=arm, pi=np.nan,
                                       n_pool=npool, empty=True,
                                       OOS_CAGR=b["OOS_CAGR"], OOS_Sharpe=b["OOS_Sharpe"],
                                       OOS_MaxDD=b["OOS_MaxDD"], d_vs_S0=0.0,
                                       d_vs_SPY=b["OOS_Sharpe"] - ref["spy_oos_sh"]))
                        return
                    row = cand.loc[pi]
                    wf.append(dict(panel=pan.name, mode=mode, bps=bps, arm=arm, pi=pi,
                                   n_pool=npool, empty=False,
                                   OOS_CAGR=row["OOS_CAGR"], OOS_Sharpe=row["OOS_Sharpe"],
                                   OOS_MaxDD=row["OOS_MaxDD"],
                                   d_vs_S0=row["OOS_Sharpe"] - b["OOS_Sharpe"],
                                   d_vs_SPY=row["OOS_Sharpe"] - ref["spy_oos_sh"]))

                emit("S0_do_nothing", None, 0)
                emit("S1_IS_argmax", cand.IS_Sharpe.idxmax())
                for kind in KINDS:
                    k2 = cc[(cc.kind == kind) & (cc.clears_is)]
                    pool = sorted(set(k2.pi.tolist()))
                    emit(f"S2_{kind}", cand.loc[pool].IS_Sharpe.idxmax() if pool else None,
                         len(pool))
                    k3 = k2[k2.cert_ok]
                    pool3 = sorted(set(k3.pi.tolist()))
                    emit(f"S3_{kind}", cand.loc[pool3].IS_Sharpe.idxmax() if pool3 else None,
                         len(pool3))
                emit("ORACLE_OOS", cand.OOS_Sharpe.idxmax())
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    summ = WF.groupby("arm").agg(mean_OOS_Sharpe=("OOS_Sharpe", "mean"),
                                 mean_OOS_CAGR=("OOS_CAGR", "mean"),
                                 mean_OOS_MaxDD=("OOS_MaxDD", "mean"),
                                 mean_d_vs_S0=("d_vs_S0", "mean"),
                                 mean_d_vs_SPY=("d_vs_SPY", "mean"),
                                 wins_vs_S0=("d_vs_S0", lambda x: int((x > 0).sum())),
                                 n=("d_vs_S0", "size"),
                                 mean_pool=("n_pool", "mean"),
                                 empty_pools=("empty", "sum"))
    summ["t_vs_S0"] = [tstat(WF[WF.arm == a].d_vs_S0.values) for a in summ.index]
    P(summ.to_string(float_format=lambda x: f"{x:+.4f}"))
    P("")
    spy_oos = np.mean([base[p.name]["ref"]["spy_oos_sh"] for p in panels])
    P(f"  SPY mean OOS Sharpe over the same cells: {spy_oos:+.4f}")
    P("")

    # ---------------- Q5: KEEP paths
    P("=" * 118)
    P("Q5  KEEP PATHS (PROTOCOL rule 4).  4a vs the LIVE RULES v2 book, 4b vs SPY, on every real row.")
    P("=" * 118)
    real = G[G.fam != "BASE"]
    P(f"  4a: {int(real.pass4a.sum())} / {len(real)} rows      "
      f"4b: {int(real.pass4b.sum())} / {len(real)} rows      "
      f"BOTH: {int((real.pass4a & real.pass4b).sum())} / {len(real)}")
    P("  4b by panel x family:")
    P("  " + real.pivot_table(index="panel", columns="fam", values="pass4b", aggfunc="mean")
      .to_string(float_format=lambda x: f"{x:.3f}").replace("\n", "\n  "))
    P("  most common 4b failure clauses: " +
      ", ".join(f"{k}={v}" for k, v in real.fail4b.value_counts().head(6).items()))
    P("  base book rows:")
    P("  " + G[G.fam == "BASE"][["panel", "bps", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                 "OOS_Sharpe", "pass4a", "pass4b"]]
      .to_string(index=False, float_format=lambda x: f"{x:.3f}").replace("\n", "\n  "))
    real.to_csv(OUT / f"{STEM}.keep.csv", index=False)
    P("")
    P(f"  runtime {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()

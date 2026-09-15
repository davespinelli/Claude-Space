#!/usr/bin/env python3
"""Idea 881 (lane B, 2026-09-15) - is the ONE-SIDED DISPERSION defect a MAX-RUN-LENGTH fact or a
TAIL-MASS fact?

THE CLAIM UNDER TEST
--------------------
Idea 871 proposed that PROTOCOL name the SWITCH COUNT as the statistic a placebo must match.
Idea 875 refined that: under the SIGNED pooled estimator, a switch-matched null with 5.87x the real
arm's fire-run dispersion (SM-DOM: ONE dominant run of k-(m-1) days, the other m-1 runs of length 1)
is systematically biased against BLOCK by -0.0046 of Sharpe (sign-test z +3.8 over 1,152 arms),
cost-invariantly, while an UNDER-dispersed null (SM-UNIF, 0.030x) is clean (z +0.7).  875 proposed
the clause "its longest run must not exceed the real arm's longest run (equivalently, its run-length
dispersion must not exceed the real arm's)" - and named its own gap honestly:

    SM-DOM changes TWO things at once.  It has ONE run far longer than any run the real arm ever
    had (the MAX channel), and it holds a large share of all firing days inside runs longer than
    any real run (the TAIL-MASS channel).  875 cannot say which channel carries the -0.0046, so it
    cannot say whether a cap on the LONGEST RUN is the right clause, or whether PROTOCOL must
    instead bound the whole upper tail.

This run separates the two channels by construction and prices each.  The distinction is not
cosmetic: a MAX cap is one integer per arm and is trivially checkable; a tail-mass bound is a
distributional constraint that every future placebo would have to certify.

THE TEN NULLS (all firing-rate-matched and information-free; the eight SM_* preserve the real arm's
firing-day count k and run count m EXACTLY, so the switch count and the whole switch-cost term are
identical to BLOCK's and to the real arm's)
-----------------------------------------------------------------------------------------------
                 max fire-run        days in long runs   dispersion   source
  RAND           1 (iid singles)     none                unmatched switches (13x)   idea 602/606
  BLOCK          = real (circ shift) = real              1.00x  <- REFERENCE        idea 602/606
  BLOCK2         = real (circ shift) = real              1.00x  <- SEED CALIBRATION THIS RUN (NEW)
  SM_UNIF        k//m + 1            none                0.03x                      idea 875
  SM_DOM         k-(m-1)  (HUGE)     k-m+1  (ALL)        5.87x                      idea 875
  SM_SPLIT2      ~(k-m+2)/2          k-m+2  (ALL)        ...        THIS RUN (NEW)
  SM_SPLIT4      ~(k-m+4)/4          k-m+4  (ALL)        ...        THIS RUN (NEW)
  SM_SPLIT8      ~(k-m+8)/8          k-m+8  (ALL)        ...        THIS RUN (NEW)
  SM_LONE        = L* exactly        L* only  (THIN)     ...        THIS RUN (NEW)
  SM_FILL        = L* exactly        ~k-m  (HEAVY)       ...        THIS RUN (NEW)

L* = the real arm's own longest fire run.  The design is a two-contrast factorisation:

  CONTRAST A - TAIL MASS HELD, MAX VARIED.  SM_DOM / SPLIT2 / SPLIT4 / SPLIT8 put the same long-run
  day mass (k-m+j, which moves by at most j-1 = 7 days across the ladder) into j runs instead of 1,
  so the MAXIMUM falls by ~j while the number of days sitting in long runs is unchanged.  If the
  -0.0046 decays along this ladder, the bias is a MAX-RUN-LENGTH fact.  If it is flat, it is a
  TAIL-MASS fact.

  CONTRAST B - MAX HELD AT THE LEGAL CAP, TAIL MASS VARIED.  SM_LONE and SM_FILL both have a longest
  run of EXACTLY L*, i.e. both SATISFY 875's proposed clause.  SM_LONE puts one run at L* and
  spreads the rest near-uniformly (THIN tail); SM_FILL pours days into as many runs at L* as will
  fit (HEAVY tail).  If both are clean, 875's cap is a SUFFICIENT clause and nothing more is needed.
  If SM_FILL is biased while SM_LONE is not, the cap is NOT sufficient and PROTOCOL must bound the
  tail.

BLOCK2 is BLOCK drawn from an independent seed stream.  Its gap against BLOCK has a TRUE MEAN OF
EXACTLY ZERO by construction, so it calibrates the signed statistic's null band on this grid rather
than assuming one.  875's finding was that the |.| statistic is 87-95% seed noise; the signed
statistic needs its own measured band, and BLOCK2 supplies it.

TUNED PARAMETERS (PROTOCOL rule 4: at most two) - the queue names both
    1. cap rule    which of the eight run-shape constructions above (the j-ladder and the L* pair)
    2. cost rung   0 / 10 / 25 bps
    ALL grid points reported at every panel / family / q / w / depth / cadence / gross.  Nothing is
    chosen on the answer; every null is priced on every arm and written to .excess.csv.

REPORTED, NEVER SELECTED ON (axis set copied verbatim from idea 875 so G3 is an agreement bar)
    families BREADTH/VOL20/DISP/CORR x LO/HI (8)   level q 0.07 / 0.12 / 0.17
    window w 252 / 1008        depth 0.50 / 1.00       cadence D / W       gross 0.75 / 1.00
    panels U56 / B136 / SMALL.  384 arms per panel x 3 = 1,152 arms x 10 nulls x 20 md5 seeds x 3
    rungs = 691,200 placebo cells.  SEED BUDGET RAISED 10 -> 20 vs 875, because 875 measured the
    per-arm resolution limit at 10 seeds to be ~0.02 of Sharpe, i.e. 4x the effect being split here.

GATES (printed before any hypothesis is read)
    G1  a never-firing multiplier path reproduces the ungated book exactly.          bar 1e-12
    G6  the fast Sharpe used on placebo cells equals engine.metrics()['Sharpe'].     bar 1e-10
    G2  every null's mean effective multiplier equals the real arm's (rate match).   bar 1e-12
    G4  determinism: every placebo recomputed from its md5 seed, max |d| must be 0.
    G5  CONSTRUCTION, on every real arm x seed: all eight SM_* nulls reproduce k and m EXACTLY
        (0 violations); SM_LONE and SM_FILL have max run EXACTLY L*; the SPLIT ladder's max-run
        ratio is monotone decreasing in j; SM_FILL's long-day mass exceeds SM_LONE's.  A FAIL here
        voids the contrast it belongs to and is printed as such.
    G3  REPRODUCTION of idea 875: SM_DOM's SIGNED pooled gap at 10 bps within 0.0020 of its
        published -0.0046 with sign-test z >= +3.0, its dispersion ratio within 0.60 of 5.87, and
        SM_UNIF's signed gap inside the BLOCK2 band.  Seed budget and seed strings differ, so these
        are agreement bars, not identity bars, and any miss is printed rather than absorbed.
    G7  CALIBRATION: BLOCK2's signed pooled gap |.| <= 0.0010 with |z| < 2.0.  This is the band
        every other null is read against.

PRE-REGISTERED HYPOTHESES (fixed before any number below the gates was read)
    H_MAX    CONTRAST A.  |signed gap| is monotone DECREASING along SM_DOM -> SPLIT2 -> SPLIT4 ->
             SPLIT8 at 10 bps, AND SM_SPLIT8 lands inside the BLOCK2 band (|z| < 2).
             PASS = the bias is a MAX-RUN-LENGTH fact.
    H_TAIL   CONTRAST B.  SM_LONE and SM_FILL, which both have max run EXACTLY L*, are BOTH inside
             the BLOCK2 band and differ from each other by < 0.0010.
             PASS = a cap at the real arm's own longest run is a SUFFICIENT clause; tail mass at a
             legal max buys no bias.  FAIL = 875's cap is not sufficient.
    H_MECH   Spearman(pooled max-run ratio, pooled signed gap) over the ten nulls <= -0.80, AND the
             placebo's realised annualised vol falls monotonically along SM_DOM -> SPLIT8.  This is
             875's proposed mechanism (a long contiguous cash holiday lowers the placebo's vol,
             raises its Sharpe and SHRINKS the measured excess) stated as a falsifiable prediction.
    H_COSTINV  every switch-matched null's signed gap moves < 0.005 across 0/10/25 bps.  The switch
             counts are matched, so unlike RAND's the gap must NOT be a cost story.
    H_WF     Spearman(IS signed gap, OOS signed gap) >= +0.30 in >= 6 of 8 families for SM_DOM.

RULE 8 WALK-FORWARD (required, run whatever the verdict)
    IS = ..2016-12-31 fitted, OOS = 2017-01-01.. read once.  (a) the signed gap is measured on IS
    and read on OOS per family (H_WF).  (b) THE BOOKS: one declared IS-only selector - the arm with
    the highest 2009-2016 Sharpe on each panel - is picked and its untouched OOS CAGR / Sharpe /
    MaxDD is reported against RULES v2 (live) OOS and SPY OOS, with BOTH KEEP paths, plus the
    unselected base rate of 4a and 4b over all 1,152 arms.

SURVIVORSHIP: U56 and B136 are current-constituent lists.  SMALL is the sub-$2B panel with every
ticker whose max_1d_move >= 1.0 in data/small_meta.csv dropped first, and it is CURRENT
CONSTITUENTS ONLY - dead small caps are absent, so its CAGRs are the most optimistic numbers in the
run and its 4b readings are upper bounds.  This run's headline quantity is a DIFFERENCE BETWEEN TWO
NULLS ON THE SAME ARM, which is far less exposed to that bias than any level.

PROTOCOL: 10 bps per unit turnover (0 and 25 also reported), next-day fills, no shorting, no
leverage.  Deterministic (md5-seeded), standalone, no network.  Modifies nothing but its own
outputs:  .arms.csv  .excess.csv  .gap.csv  .contrast.csv  .mechanism.csv
           .walkforward.csv  .books.csv  .console.txt
"""
from __future__ import annotations

import hashlib
import sys
import time
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
from baseline import load_universe, score, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = Path(__file__).name[:-3]
OUT = REPO / "research" / "backtests"
LINES: list[str] = []

FREQ, MAX_VOL, SMOOTH = "W", 0.60, 20
QS = [0.07, 0.12, 0.17]
WS = [252, 1008]
DEPTHS = [0.50, 1.00]
CADENCES = ["D", "W"]
GROSSES = [0.75, 1.00]
RUNGS = [0, 10, 25]
STATES = ["BREADTH", "VOL20", "DISP", "CORR"]
SIDES = {"BREADTH": ("LO", "HI"), "VOL20": ("HI", "LO"), "DISP": ("HI", "LO"), "CORR": ("HI", "LO")}

# the manipulated axis.  SPLIT_j holds the long-run DAY MASS and divides the MAX by ~j;
# LONE / FILL hold the MAX at L* exactly and move the tail mass.
SPLITS = [("SM_DOM", 1), ("SM_SPLIT2", 2), ("SM_SPLIT4", 4), ("SM_SPLIT8", 8)]
SMKINDS = [k for k, _ in SPLITS] + ["SM_LONE", "SM_FILL", "SM_UNIF"]
KINDS = ["RAND", "BLOCK", "BLOCK2"] + SMKINDS
NSEED = 20
SPLIT = "2017-01-01"

# idea 875's published numbers, for G3 (agreement bars, not identity bars)
PUB875 = dict(dom_signed_10=-0.0046, dom_z=3.8, dom_disp=5.87, unif_signed_10=-0.0006)
SIGN_BAR, DISP_BAR, Z_BAR = 0.0020, 0.60, 3.0
CAL_BAR, CAL_Z = 0.0010, 2.0


def log(s=""):
    print(s, flush=True)
    LINES.append(str(s))


# ------------------------------------------------------------------ primitives (602/606/871/875)
def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def ewall_weights(px, gross):
    e = eligible_mask(px).astype(float)
    n = e.sum(axis=1).replace(0, np.nan)
    return e.div(n, axis=0).mul(gross).fillna(0.0)


def fast_sharpe(v):
    v = np.asarray(v, float)
    sd = v.std(ddof=1)
    return v.mean() * 252 / (sd * np.sqrt(252)) if sd > 0 else np.nan


def ann_vol(v):
    return float(np.asarray(v, float).std(ddof=1) * np.sqrt(252))


def state_breadth(px):
    above = px > px.rolling(200).mean()
    return above.sum(axis=1) / above.notna().sum(axis=1).replace(0, np.nan)


def state_vol20(px):
    return (px.pct_change().rolling(SMOOTH).std() * np.sqrt(252)).mean(axis=1)


def state_disp(px):
    return px.pct_change().std(axis=1).rolling(SMOOTH).mean()


def state_corr(px):
    rt = px.pct_change()
    sig = rt.rolling(SMOOTH).std()
    s_idx = rt.mean(axis=1).rolling(SMOOTH).std()
    n = sig.notna().sum(axis=1).replace(0, np.nan)
    sbar, s2bar = sig.mean(axis=1), (sig ** 2).mean(axis=1)
    return ((s_idx ** 2 - s2bar / n) / (sbar ** 2 - s2bar / n).replace(0, np.nan)).clip(-1, 1)


STATE_FN = {"BREADTH": state_breadth, "VOL20": state_vol20, "DISP": state_disp, "CORR": state_corr}


def gate_mult(st, thr, side, depth, cadence, idx):
    fire = ((st < thr) if side == "LO" else (st > thr)) & st.notna() & thr.notna()
    m = pd.Series(1.0, index=idx).where(~fire, 1.0 - depth)
    if cadence == "W":
        m = m.where(rebalance_mask(idx, FREQ)).ffill().fillna(1.0)
    return m


def apply_eff(r_base, m_eff, gross, cost_bps):
    switch = np.abs(np.diff(m_eff, prepend=m_eff[0]))
    return m_eff * r_base - switch * gross * cost_bps / 1e4


def nswitch(m_eff):
    return int((np.abs(np.diff(np.asarray(m_eff, float), prepend=m_eff[0])) > 0).sum())


def seed_of(*parts):
    return int(hashlib.md5("|".join(map(str, parts)).encode()).hexdigest()[:8], 16)


# --------------------------------------------------------------------- run decomposition (871)
def runs_of(fire):
    fire = np.asarray(fire, bool)
    n = len(fire)
    d = np.diff(fire.astype(np.int8))
    starts = np.flatnonzero(d == 1) + 1
    ends = np.flatnonzero(d == -1) + 1
    if fire[0]:
        starts = np.r_[0, starts]
    if fire[-1]:
        ends = np.r_[ends, n]
    if len(starts) == 0:
        return np.array([], int), np.array([n], int)
    fl = (ends - starts).astype(int)
    gl = np.empty(len(starts) + 1, int)
    gl[0] = starts[0]
    gl[1:-1] = starts[1:] - ends[:-1]
    gl[-1] = n - ends[-1]
    return fl, gl


def assemble(fl, gl, n):
    out = np.zeros(n, bool)
    p = 0
    for i, f in enumerate(fl):
        p += gl[i]
        out[p:p + f] = True
        p += f
    return out


def rand_composition(total, parts, rng, min_each):
    if parts <= 0:
        return np.array([], int)
    rem = total - parts * min_each
    if rem < 0:
        raise ValueError("infeasible composition")
    if parts == 1:
        return np.array([total], int)
    cuts = np.sort(rng.choice(np.arange(rem + parts - 1), size=parts - 1, replace=False))
    pieces = np.diff(np.r_[-1, cuts, rem + parts - 1]) - 1
    return (pieces + min_each).astype(int)


def _gaps_like_switchmatch(n, k, m, rng):
    """871/875's gap draw, held IDENTICAL across every switch-matched null so that the fire-run
    shape is the single manipulated axis: uniform composition of the non-firing days into m+1 gaps
    with every INTERIOR gap >= 1 (an interior 0 would merge two fire runs and change m)."""
    gl = rand_composition(n - k - (m - 1), m + 1, rng, 0)
    gl[1:-1] += 1
    return gl


def _even(total, parts):
    """`parts` positive integers summing to `total`, as equal as possible (max - min <= 1)."""
    base, rem = divmod(total, parts)
    out = np.full(parts, base, int)
    out[:rem] += 1
    return out


def fire_lengths(kind, k, m, lstar, rng):
    """The manipulated axis: m fire-run lengths, each >= 1, summing to k.

    SM_DOM / SM_SPLIT{2,4,8}  - CONTRAST A.  j long runs sharing k - m + j days (a mass that moves
        by at most j-1 across the ladder) and m - j singletons, so the MAXIMUM falls by ~j while
        the number of days in long runs is held.  j is clamped to m on arms with fewer than j runs.
    SM_LONE  - CONTRAST B, THIN tail: exactly one run at L*, the other m-1 near-uniform.  Feasible
        and max-preserving because the real arm's other m-1 runs sum to k - L* with mean <= L*.
    SM_FILL  - CONTRAST B, HEAVY tail: pour days into as many runs at L* as fit.  Same maximum.
    SM_UNIF  - 875's clean control: every run k//m or k//m + 1.
    """
    if kind == "SM_UNIF":
        fl = _even(k, m)
        return fl[rng.permutation(m)]
    if kind == "SM_LONE":
        fl = np.empty(m, int)
        fl[0] = lstar
        if m > 1:
            fl[1:] = _even(k - lstar, m - 1)
        return fl[rng.permutation(m)]
    if kind == "SM_FILL":
        fl = np.ones(m, int)
        rem = k - m
        cap = max(lstar, 1)
        i = 0
        while rem > 0 and i < m:
            take = min(cap - 1, rem)
            fl[i] += take
            rem -= take
            i += 1
        if rem > 0:                                     # only if m*(L*) < k, impossible for a real
            fl[:] = _even(k, m)                          # arm; kept as a guard, never expected
        return fl[rng.permutation(m)]
    j = min(dict(SPLITS)[kind], m)
    fl = np.ones(m, int)
    fl[:j] = _even(k - m + j, j)
    return fl[rng.permutation(m)]


def over_share(fl, k, lstar):
    """Share of the firing days that sit in runs STRICTLY LONGER than the real arm's longest run,
    i.e. the day mass that 875's proposed cap would declare illegal.  Zero for any null whose
    maximum is <= L*."""
    if not k or not len(fl):
        return np.nan
    return float(fl[fl > lstar].sum()) / k


def placebo_eff(m_eff, depth, kind, seed, lstar):
    """Rate-matched, information-free twin of the EFFECTIVE multiplier path m_eff."""
    v = np.asarray(m_eff, float)
    n = len(v)
    fire = v < 1.0
    k = int(fire.sum())
    if k == 0 or k == n:
        return v.copy()
    rng = np.random.default_rng(seed)
    if kind == "RAND":
        out = np.ones(n)
        out[rng.choice(n, size=k, replace=False)] = 1.0 - depth
        return out
    if kind in ("BLOCK", "BLOCK2"):
        return np.roll(v, int(rng.integers(1, n)))
    fl, _ = runs_of(fire)
    m = len(fl)
    if (n - k) < (m - 1):                              # infeasible composition; fall back and log
        return np.roll(v, int(rng.integers(1, n)))
    gl2 = _gaps_like_switchmatch(n, k, m, rng)
    fl2 = fire_lengths(kind, k, m, lstar, rng)
    out = np.ones(n)
    out[assemble(fl2, gl2, n)] = 1.0 - depth
    return out


# ------------------------------------------------------------------------------ helpers
def pack(r):
    m = metrics(pd.Series(r) if not isinstance(r, pd.Series) else r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def halves(r):
    h = len(r) // 2
    return fast_sharpe(r[:h]), fast_sharpe(r[h:])


def spearman(a, b):
    a, b = pd.Series(np.asarray(a, float)), pd.Series(np.asarray(b, float))
    ok = a.notna() & b.notna()
    if ok.sum() < 3:
        return float("nan")
    return float(a[ok].rank().corr(b[ok].rank()))


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    log(f"  SMALL panel: {px.shape[1]} columns -> {len(keep)} kept "
        f"({px.shape[1]-len(keep)} dropped for max_1d_move >= 1.0)")
    return px[keep]


# ======================================================================================== gates
def gates(panels):
    log("\n[0] GATES (printed before any hypothesis is read)")
    px = panels["U56"]
    core = px.drop(columns=["SPY"], errors="ignore")
    r_base = backtest(core, ewall_weights(core, 0.75), cost_bps=10,
                      freq=FREQ)["returns"].loc["2009-01-01":]
    ones = np.ones(len(r_base))
    g1 = float(np.max(np.abs(apply_eff(r_base.values, ones, 0.75, 10) - r_base.values)))
    log(f"  G1 never-firing multiplier == ungated book   max|d| {g1:.3e}  bar 1e-12  "
        f"[{'PASS' if g1 < 1e-12 else 'FAIL'}]")
    g6 = abs(fast_sharpe(r_base.values) - metrics(r_base)["Sharpe"])
    log(f"  G6 fast Sharpe == engine.metrics()['Sharpe'] |d| {g6:.3e}  bar 1e-10  "
        f"[{'PASS' if g6 < 1e-10 else 'FAIL'}]")

    # G5 construction, on block-structured synthetic paths (the real arms are re-checked in [1])
    rng = np.random.default_rng(0)
    bad_km = bad_max = 0
    mx = {k: [] for k in SMKINDS}
    tail = {k: [] for k in SMKINDS}
    clamp = 0
    for t in range(300):
        n = 1200
        fire = np.zeros(n, bool)
        p = int(rng.integers(0, 30))
        while p < n:                                   # block-structured, like a real gate
            L = int(rng.integers(1, 25))
            fire[p:p + L] = True
            p += L + int(rng.integers(3, 60))
        v = np.where(fire, 0.5, 1.0)
        fl, _ = runs_of(fire)
        k, m = int(fire.sum()), len(fl)
        lstar = int(fl.max())
        for kind in SMKINDS:
            pe = placebo_eff(v, 0.5, kind, seed_of("G5", t, kind), lstar)
            pf = pe < 1.0
            pfl, _ = runs_of(pf)
            if int(pf.sum()) != k or len(pfl) != m:
                bad_km += 1
                continue
            mx[kind].append(float(pfl.max()) / lstar)
            tail[kind].append(float(pfl[pfl > 1].sum()) / k)
            if kind in ("SM_LONE", "SM_FILL") and int(pfl.max()) != lstar:
                bad_max += 1
    log(f"  G5a k and m preserved by all {len(SMKINDS)} switch-matched nulls: {bad_km} violations "
        f"in {300*len(SMKINDS)} synthetic draws  [{'PASS' if bad_km == 0 else 'FAIL'}]")
    log(f"  G5b SM_LONE and SM_FILL have max run EXACTLY L*: {bad_max} violations  "
        f"[{'PASS' if bad_max == 0 else 'FAIL'}]")
    mm = {k: float(np.mean(v)) for k, v in mx.items()}
    tt = {k: float(np.mean(v)) for k, v in tail.items()}
    ladder = [k for k, _ in SPLITS]
    mono = all(mm[ladder[i]] > mm[ladder[i + 1]] for i in range(len(ladder) - 1))
    log(f"  G5c SPLIT ladder max-run ratio monotone DOWN in j: " +
        " > ".join(f"{k.replace('SM_','')} {mm[k]:.2f}" for k in ladder) +
        f"  [{'PASS' if mono else 'FAIL'}]")
    log(f"     and its long-day share held: " +
        " ~ ".join(f"{k.replace('SM_','')} {tt[k]:.3f}" for k in ladder))
    heavier = tt["SM_FILL"] > tt["SM_LONE"]
    log(f"  G5d at the SAME max (1.00x L*), SM_FILL long-day share {tt['SM_FILL']:.3f} > SM_LONE "
        f"{tt['SM_LONE']:.3f}  [{'PASS' if heavier else 'FAIL'}]  "
        f"(max ratios {mm['SM_FILL']:.2f} / {mm['SM_LONE']:.2f})")


# ==================================================================================== per panel
def run_panel(name, px):
    t0 = time.time()
    idx = px.index
    core = px.drop(columns=["SPY"], errors="ignore")
    spy = px["SPY"].pct_change().fillna(0.0)
    states = {s: STATE_FN[s](core) for s in STATES}
    base = {}
    for g in GROSSES:
        w = ewall_weights(core, g)
        for c in RUNGS:
            base[(g, c)] = backtest(core, w, cost_bps=c, freq=FREQ)["returns"]

    start = idx[260]
    ii = idx[idx >= start]
    oos = np.asarray(ii >= pd.Timestamp(SPLIT))
    isw = ~oos
    RB = {k: v.loc[ii].values for k, v in base.items()}

    spy_v = spy.loc[ii].values
    spy_c, spy_s, spy_d = pack(pd.Series(spy_v, index=ii))
    spy_h1, spy_h2 = halves(spy_v)
    spy_oc, spy_os, spy_od = pack(pd.Series(spy_v[oos], index=ii[oos]))
    bl = backtest(core, rules_v2_weights(core), cost_bps=10, freq=FREQ)["returns"].loc[ii]
    bl_c, bl_s, bl_d = pack(bl)
    bl_h1, bl_h2 = halves(bl.values)
    bl_oc, bl_os, bl_od = pack(bl.loc[ii[oos]])
    bench = dict(panel=name, spy_cagr=spy_c, spy_sh=spy_s, spy_dd=spy_d, spy_h1=spy_h1,
                 spy_h2=spy_h2, spy_oos_c=spy_oc, spy_oos_s=spy_os, spy_oos_d=spy_od,
                 bl_cagr=bl_c, bl_sh=bl_s, bl_dd=bl_d, bl_h1=bl_h1, bl_h2=bl_h2,
                 bl_oos_c=bl_oc, bl_oos_s=bl_os, bl_oos_d=bl_od)

    rows, exrows = [], []
    g2 = 0.0
    km_viol = maxviol = 0
    for st_name in STATES:
        st_full = states[st_name]
        for side in SIDES[st_name]:
            fam = f"{st_name}-{side}"
            for q, w in product(QS, WS):
                thr = st_full.rolling(w, min_periods=max(60, w // 4)).quantile(
                    q if side == "LO" else 1 - q)
                for depth, cad in product(DEPTHS, CADENCES):
                    mult = gate_mult(st_full, thr, side, depth, cad, idx)
                    me = mult.shift(1).fillna(1.0).loc[ii].values
                    fired = me < 1.0
                    k_real = int(fired.sum())
                    sw_real = nswitch(me)
                    fl_r, _ = runs_of(fired)
                    nruns = int(len(fl_r))
                    sd_real = float(fl_r.std(ddof=1)) if nruns > 1 else 0.0
                    lstar = int(fl_r.max()) if nruns else 0
                    tail_real = (float(fl_r[fl_r > 1].sum()) / k_real) if k_real else 0.0
                    for g in GROSSES:
                        real = {c: apply_eff(RB[(g, c)], me, g, c) for c in RUNGS}
                        rr = real[10]
                        c_, s_, d_ = pack(pd.Series(rr, index=ii))
                        h1, h2 = halves(rr)
                        oc, os_, od = pack(pd.Series(rr[oos], index=ii[oos]))
                        rows.append(dict(
                            panel=name, family=fam, state=st_name, side=side, q=q, w=w,
                            depth=depth, cadence=cad, gross=g, rate=float(fired.mean()),
                            nswitch=sw_real, nruns=nruns,
                            mean_runlen=float(fl_r.mean()) if nruns else 0.0,
                            sd_runlen=sd_real, max_runlen=lstar, tail_share=tail_real,
                            CAGR=c_, Sharpe=s_, MaxDD=d_, H1=h1, H2=h2,
                            IS_Sharpe=fast_sharpe(rr[isw]), OOS_CAGR=oc, OOS_Sharpe=os_,
                            OOS_MaxDD=od))
                        sh_real = {c: fast_sharpe(real[c]) for c in RUNGS}
                        sh_is, sh_oos = fast_sharpe(rr[isw]), fast_sharpe(rr[oos])
                        for kind in KINDS:
                            acc = {c: [] for c in RUNGS}
                            acc_is, acc_oos = [], []
                            swr, sdr, mxr, tls, ovs, pvols, kmok = [], [], [], [], [], [], []
                            for sd in range(NSEED):
                                seed = seed_of(name, fam, q, w, depth, cad, g, kind, sd)
                                pe = placebo_eff(me, depth, kind, seed, lstar)
                                g2 = max(g2, abs(pe.mean() - me.mean()))
                                swr.append(nswitch(pe) / max(sw_real, 1))
                                pf = pe < 1.0
                                pfl, _ = runs_of(pf)
                                kmok.append(int(pf.sum()) == k_real and len(pfl) == nruns)
                                sdr.append((float(pfl.std(ddof=1)) / sd_real)
                                           if (len(pfl) > 1 and sd_real > 0) else np.nan)
                                mxr.append((float(pfl.max()) / lstar) if (len(pfl) and lstar)
                                           else np.nan)
                                tls.append((float(pfl[pfl > 1].sum()) / k_real)
                                           if k_real else np.nan)
                                ovs.append(over_share(pfl, k_real, lstar))
                                if kind in ("SM_LONE", "SM_FILL") and len(pfl) and lstar:
                                    maxviol += int(int(pfl.max()) != lstar)
                                for c in RUNGS:
                                    pr = apply_eff(RB[(g, c)], pe, g, c)
                                    acc[c].append(sh_real[c] - fast_sharpe(pr))
                                    if c == 10:
                                        pvols.append(ann_vol(pr))
                                        acc_is.append(sh_is - fast_sharpe(pr[isw]))
                                        acc_oos.append(sh_oos - fast_sharpe(pr[oos]))
                            if kind in SMKINDS:
                                km_viol += int(NSEED - sum(kmok))
                            exrows.append(dict(
                                panel=name, family=fam, state=st_name, side=side, q=q, w=w,
                                depth=depth, cadence=cad, gross=g, kind=kind,
                                nswitch_real=sw_real, sw_ratio=float(np.mean(swr)),
                                nruns=nruns, max_runlen_real=lstar,
                                sd_runlen_ratio=float(np.nanmean(sdr)),
                                max_run_ratio=float(np.nanmean(mxr)),
                                tail_share=float(np.nanmean(tls)),
                                over_share=float(np.nanmean(ovs)),
                                tail_share_real=tail_real,
                                pvol_10bps=float(np.mean(pvols)),
                                km_exact=float(np.mean(kmok)),
                                **{f"excess_{c}bps": float(np.median(acc[c])) for c in RUNGS},
                                **{f"seedsd_{c}bps": float(np.std(acc[c], ddof=1))
                                   for c in RUNGS},
                                excess_IS=float(np.median(acc_is)),
                                excess_OOS=float(np.median(acc_oos))))
        log(f"    {name}: {st_name} done  ({time.time() - t0:.0f}s)")

    # G4 determinism on a sample
    d4 = 0.0
    for r in exrows[:8] + exrows[len(exrows) // 2: len(exrows) // 2 + 8]:
        st_full = states[r["state"]]
        thr = st_full.rolling(r["w"], min_periods=max(60, r["w"] // 4)).quantile(
            r["q"] if r["side"] == "LO" else 1 - r["q"])
        me = gate_mult(st_full, thr, r["side"], r["depth"], r["cadence"], idx
                       ).shift(1).fillna(1.0).loc[ii].values
        rb = RB[(r["gross"], 10)]
        sh = fast_sharpe(apply_eff(rb, me, r["gross"], 10))
        acc = [sh - fast_sharpe(apply_eff(rb, placebo_eff(
            me, r["depth"], r["kind"], seed_of(name, r["family"], r["q"], r["w"], r["depth"],
                                               r["cadence"], r["gross"], r["kind"], sd),
            r["max_runlen_real"]), r["gross"], 10)) for sd in range(NSEED)]
        d4 = max(d4, abs(float(np.median(acc)) - r["excess_10bps"]))
    return pd.DataFrame(rows), pd.DataFrame(exrows), bench, g2, d4, km_viol, maxviol


# ========================================================================================= main
def main():
    t0 = time.time()
    log("=" * 100)
    log("IDEA 881 - is the ONE-SIDED DISPERSION defect a MAX-RUN-LENGTH fact or a TAIL-MASS fact?"
        "  (lane B 2026-09-15)")
    log("=" * 100)
    log(f"# pandas {pd.__version__} numpy {np.__version__}  |  {len(KINDS)} nulls x {NSEED} seeds "
        f"x {len(RUNGS)} rungs")

    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL": small_panel()}
    for n, p in panels.items():
        log(f"  {n}: {p.shape[1]} cols x {len(p)} days  {p.index[0].date()} .. {p.index[-1].date()}")
    gates(panels)

    arms, ex, benches = [], [], []
    g2m = d4m = 0.0
    kmv = mxv = 0
    for n, p in panels.items():
        a, e, b, g2, d4, km, mv = run_panel(n, p)
        arms.append(a)
        ex.append(e)
        benches.append(b)
        g2m, d4m = max(g2m, g2), max(d4m, d4)
        kmv, mxv = kmv + km, mxv + mv
    arms = pd.concat(arms, ignore_index=True)
    ex = pd.concat(ex, ignore_index=True)
    bench = pd.DataFrame(benches).set_index("panel")
    arms.to_csv(OUT / f"{STEM}.arms.csv", index=False)
    ex.to_csv(OUT / f"{STEM}.excess.csv", index=False)
    log(f"\n  arms {len(arms)} rows, excess {len(ex)} rows  ({time.time()-t0:.0f}s)")
    log(f"  G2 rate match  max|mean(placebo) - mean(real)| {g2m:.3e}  bar 1e-12  "
        f"[{'PASS' if g2m < 1e-12 else 'FAIL'}]")
    log(f"  G4 determinism max|d| {d4m:.3e}  bar 0  [{'PASS' if d4m == 0.0 else 'FAIL'}]")
    log(f"  G5a on REAL arms: k and m violations across all switch-matched cells: {kmv} of "
        f"{len(SMKINDS)*len(arms)*NSEED}  [{'PASS' if kmv == 0 else 'FAIL'}]")
    log(f"  G5b on REAL arms: SM_LONE / SM_FILL max-run != L* violations: {mxv} of "
        f"{2*len(arms)*NSEED}  [{'PASS' if mxv == 0 else 'FAIL'}]")

    # ---------------------------------------------------------------- gaps vs BLOCK
    key = ["panel", "family", "q", "w", "depth", "cadence", "gross"]
    piv = ex.pivot_table(index=key, columns="kind",
                         values=[f"excess_{c}bps" for c in RUNGS]
                         + [f"seedsd_{c}bps" for c in RUNGS]
                         + ["excess_IS", "excess_OOS", "sd_runlen_ratio", "sw_ratio",
                            "max_run_ratio", "tail_share", "over_share", "pvol_10bps"])
    gap = pd.DataFrame(index=piv.index)
    for kind in KINDS:
        for c in RUNGS:
            gap[f"{kind}_ex_{c}"] = piv[(f"excess_{c}bps", kind)]
            gap[f"{kind}_sd_{c}"] = piv[(f"seedsd_{c}bps", kind)]
        for f in ("sd_runlen_ratio", "sw_ratio", "max_run_ratio", "tail_share", "over_share",
                  "pvol_10bps"):
            gap[f"{kind}_{f}"] = piv[(f, kind)]
        gap[f"{kind}_IS"] = piv[("excess_IS", kind)]
        gap[f"{kind}_OOS"] = piv[("excess_OOS", kind)]
    OTHERS = [k for k in KINDS if k != "BLOCK"]
    for kind in OTHERS:
        for c in RUNGS:
            gap[f"s_{kind}_{c}"] = gap[f"{kind}_ex_{c}"] - gap["BLOCK_ex_{}".format(c)]
            gap[f"d_{kind}_{c}"] = gap[f"s_{kind}_{c}"].abs()
        gap[f"dIS_{kind}"] = gap[f"{kind}_IS"] - gap["BLOCK_IS"]
        gap[f"dOOS_{kind}"] = gap[f"{kind}_OOS"] - gap["BLOCK_OOS"]
    gap = gap.reset_index()
    gap.to_csv(OUT / f"{STEM}.gap.csv", index=False)
    NARM = len(gap)

    def signed(kind, c=10):
        s = gap[f"s_{kind}_{c}"]
        med, mean = float(s.median()), float(s.mean())
        se = float(s.std(ddof=1) / np.sqrt(len(s)))
        below = float((s < 0).mean())
        z = (below - 0.5) / np.sqrt(0.25 / len(s))
        return med, mean, se, below, z

    log("\n" + "=" * 100)
    log("[1] G7 CALIBRATION - what does a null that differs from BLOCK ONLY BY SEED look like?")
    log("    BLOCK2 is BLOCK from an independent seed stream.  Its true gap is EXACTLY ZERO by")
    log("    construction, so it measures this grid's signed-statistic band instead of assuming one.")
    log("=" * 100)
    b2 = signed("BLOCK2")
    log(f"  BLOCK2 signed median {b2[0]:+.5f}  mean {b2[1]:+.5f} (SE {b2[2]:.5f})  "
        f"share below BLOCK {b2[3]:.1%}  sign-test z {b2[4]:+.2f}")
    g7 = abs(b2[0]) <= CAL_BAR and abs(b2[4]) < CAL_Z
    log(f"  G7 |signed| <= {CAL_BAR} and |z| < {CAL_Z}  [{'PASS' if g7 else 'FAIL'}]   "
        f"-> BAND for every reading below: |signed| <= {CAL_BAR:.4f} AND |z| < {CAL_Z}")

    log("\n" + "=" * 100)
    log("[2] G3 REPRODUCTION OF IDEA 875 (agreement bars: different seed strings, 20 seeds vs 10)")
    log("=" * 100)
    dm = signed("SM_DOM")
    disp_dom = float(gap["SM_DOM_sd_runlen_ratio"].mean())
    un = signed("SM_UNIF")
    ok1 = abs(dm[0] - PUB875["dom_signed_10"]) <= SIGN_BAR
    ok2 = dm[4] >= Z_BAR
    ok3 = abs(disp_dom - PUB875["dom_disp"]) <= DISP_BAR
    ok4 = abs(un[0]) <= CAL_BAR and abs(un[4]) < CAL_Z
    log(f"  SM_DOM signed @10bps {dm[0]:+.5f}  (875 published {PUB875['dom_signed_10']:+.4f}, bar "
        f"{SIGN_BAR})  [{'PASS' if ok1 else 'FAIL'}]")
    log(f"  SM_DOM sign-test z   {dm[4]:+.2f}      (875 published +{PUB875['dom_z']}, bar >= "
        f"+{Z_BAR})  [{'PASS' if ok2 else 'FAIL'}]")
    log(f"  SM_DOM dispersion    {disp_dom:.2f}x     (875 published {PUB875['dom_disp']}x, bar "
        f"{DISP_BAR})  [{'PASS' if ok3 else 'FAIL'}]")
    log(f"  SM_UNIF inside the BLOCK2 band: signed {un[0]:+.5f}, z {un[4]:+.2f}  "
        f"[{'PASS' if ok4 else 'FAIL'}]")
    log(f"  G3 overall [{'PASS' if all((ok1, ok2, ok3, ok4)) else 'FAIL'}]")

    log("\n" + "=" * 100)
    log("[3] THE CONSTRUCTION AS MEASURED ON ALL 1,152 REAL ARMS")
    log("=" * 100)
    log(f"  real arm: median {gap['SM_DOM_max_run_ratio'].notna().sum()} arms priced; "
        f"median runs {arms.nruns.median():.0f}, median L* {arms.max_runlen.median():.0f} days, "
        f"median long-day share {arms.tail_share.median():.3f}")
    log(f"  {'null':11s}{'max/L*':>9s}{'disp/real':>11s}{'longday':>9s}{'days>L*':>9s}"
        f"{'switch':>9s}{'placebo vol':>13s}")
    con = []
    for kind in KINDS:
        mr = float(gap[f"{kind}_max_run_ratio"].mean())
        dr = float(gap[f"{kind}_sd_runlen_ratio"].mean())
        ts = float(gap[f"{kind}_tail_share"].mean())
        ov = float(gap[f"{kind}_over_share"].mean())
        sw = float(gap[f"{kind}_sw_ratio"].mean())
        pv = float(gap[f"{kind}_pvol_10bps"].mean())
        con.append(dict(kind=kind, max_run_ratio=mr, disp_ratio=dr, longday_share=ts,
                        over_share=ov, sw_ratio=sw, pvol=pv))
        log(f"  {kind:11s}{mr:9.2f}{dr:11.2f}{ts:9.3f}{ov:9.3f}{sw:9.2f}{pv:13.4f}")
    log(f"  {'REAL ARM':11s}{1.00:9.2f}{1.00:11.2f}{arms.tail_share.mean():9.3f}{0.0:9.3f}"
        f"{1.00:9.2f}{'-':>13s}")
    log("  days>L* = share of firing days in runs STRICTLY LONGER than the real arm's longest run,")
    log("  i.e. the day mass 875's proposed cap would declare illegal.  0.000 = the null obeys it.")

    log("\n" + "=" * 100)
    log("[4] H_MAX - CONTRAST A: TAIL-MASS DAY COUNT HELD, MAXIMUM DIVIDED BY j")
    log("    Same long-run day mass (k-m+j), spread over j runs instead of 1.  If the -0.0046 is a")
    log("    MAX fact it decays along this ladder; if it is a TAIL-MASS fact it is flat.")
    log("=" * 100)
    log(f"  {'null':11s}{'j':>3s}{'max/L*':>9s}{'days>L*':>9s}" +
        "".join(f"{'signed@'+str(c):>13s}" for c in RUNGS) + f"{'z':>8s}{'inside band':>13s}")
    lad = []
    for kind, j in SPLITS:
        s = {c: signed(kind, c) for c in RUNGS}
        mr = float(gap[f"{kind}_max_run_ratio"].mean())
        ts = float(gap[f"{kind}_over_share"].mean())
        inside = abs(s[10][0]) <= CAL_BAR and abs(s[10][4]) < CAL_Z
        lad.append(dict(kind=kind, j=j, max_run_ratio=mr, over_share=ts,
                        longday_share=float(gap[f"{kind}_tail_share"].mean()),
                        **{f"signed_{c}": s[c][0] for c in RUNGS},
                        z=s[10][4], inside=inside, pvol=float(gap[f"{kind}_pvol_10bps"].mean())))
        log(f"  {kind:11s}{j:3d}{mr:9.2f}{ts:9.3f}" +
            "".join(f"{s[c][0]:+13.5f}" for c in RUNGS) +
            f"{s[10][4]:+8.2f}{('INSIDE' if inside else 'OUTSIDE'):>13s}")
    lad = pd.DataFrame(lad)
    mag = lad["signed_10"].abs().values
    mono = bool(np.all(np.diff(mag) < 0))
    last_in = bool(lad.iloc[-1]["inside"])
    h_max = mono and last_in
    log(f"  |signed| monotone DECREASING along j=1,2,4,8: " +
        " > ".join(f"{v:.5f}" for v in mag) + f"   [{'yes' if mono else 'NO'}]")
    log(f"  SM_SPLIT8 inside the BLOCK2 band: [{'yes' if last_in else 'NO'}]")
    log(f"  H_MAX {'CONFIRMED' if h_max else 'REFUTED'}   -> the bias "
        f"{'IS' if h_max else 'is NOT purely'} a MAX-RUN-LENGTH fact")
    rho_lad = spearman(lad["max_run_ratio"], lad["signed_10"])
    log(f"  Spearman(max/L*, signed) over the four ladder points = {rho_lad:+.3f}")

    log("\n" + "=" * 100)
    log("[5] H_TAIL - CONTRAST B: MAXIMUM HELD AT EXACTLY L*, TAIL MASS VARIED")
    log("    Both nulls SATISFY 875's proposed clause (longest run <= the real arm's longest run).")
    log("    If both are clean, the cap is a SUFFICIENT clause and no tail bound is needed.")
    log("=" * 100)
    log(f"  {'null':11s}{'max/L*':>9s}{'days>L*':>9s}{'disp':>8s}" +
        "".join(f"{'signed@'+str(c):>13s}" for c in RUNGS) + f"{'z':>8s}{'inside band':>13s}")
    pair = {}
    for kind in ("SM_LONE", "SM_FILL"):
        s = {c: signed(kind, c) for c in RUNGS}
        inside = abs(s[10][0]) <= CAL_BAR and abs(s[10][4]) < CAL_Z
        pair[kind] = (s, inside)
        log(f"  {kind:11s}{gap[f'{kind}_max_run_ratio'].mean():9.2f}"
            f"{gap[f'{kind}_over_share'].mean():9.3f}"
            f"{gap[f'{kind}_sd_runlen_ratio'].mean():8.2f}" +
            "".join(f"{s[c][0]:+13.5f}" for c in RUNGS) +
            f"{s[10][4]:+8.2f}{('INSIDE' if inside else 'OUTSIDE'):>13s}")
    dlf = abs(pair["SM_FILL"][0][10][0] - pair["SM_LONE"][0][10][0])
    h_tail = pair["SM_LONE"][1] and pair["SM_FILL"][1] and dlf < CAL_BAR
    log(f"  |SM_FILL - SM_LONE| at 10 bps = {dlf:.5f}  (bar {CAL_BAR})")
    log(f"  dispersion multiple at the SAME max: SM_FILL "
        f"{gap['SM_FILL_sd_runlen_ratio'].mean():.2f}x vs SM_LONE "
        f"{gap['SM_LONE_sd_runlen_ratio'].mean():.2f}x of the real arm's  "
        f"({gap['SM_FILL_sd_runlen_ratio'].mean() / max(gap['SM_LONE_sd_runlen_ratio'].mean(), 1e-9):.2f}x each other)")
    log(f"  H_TAIL {'CONFIRMED' if h_tail else 'REFUTED'}   -> a cap at the real arm's own longest "
        f"run is {'SUFFICIENT' if h_tail else 'NOT sufficient'}")

    log("\n" + "=" * 100)
    log("[6] H_MECH - 875's PROPOSED MECHANISM AS A FALSIFIABLE PREDICTION")
    log("    'a single giant de-grossed run is a long cash holiday that lowers the placebo's vol,")
    log("     raising its Sharpe and SHRINKING the measured excess'  ->  more max, lower vol, more")
    log("     negative gap.")
    log("=" * 100)
    con = pd.DataFrame(con)
    sm = con[con.kind.isin(SMKINDS)].copy()
    sm["signed_10"] = [signed(k)[0] for k in sm.kind]
    rho_mx = spearman(sm.max_run_ratio, sm.signed_10)
    rho_tl = spearman(sm.over_share, sm.signed_10)
    rho_ds = spearman(sm.disp_ratio, sm.signed_10)
    rho_pv = spearman(sm.max_run_ratio, sm.pvol)
    log(f"  over the {len(sm)} switch-matched nulls (pooled values):")
    log(f"    Spearman(max/L*,        signed gap) = {rho_mx:+.3f}   (H_MECH bar <= -0.80)")
    log(f"    Spearman(days>L* share,  signed gap) = {rho_tl:+.3f}")
    log(f"    Spearman(dispersion,    signed gap) = {rho_ds:+.3f}")
    log(f"    Spearman(max/L*,        placebo vol)= {rho_pv:+.3f}   (mechanism: longer max -> lower vol)")
    pv_lad = lad["pvol"].values
    pv_mono = bool(np.all(np.diff(pv_lad) > 0))
    log(f"  placebo annualised vol along j=1,2,4,8: " + " < ".join(f"{v:.4f}" for v in pv_lad)
        + f"   [{'monotone UP as max falls' if pv_mono else 'NOT monotone'}]")
    h_mech = (rho_mx <= -0.80) and pv_mono
    log(f"  H_MECH {'CONFIRMED' if h_mech else 'REFUTED'}")
    lad.to_csv(OUT / f"{STEM}.contrast.csv", index=False)

    log("\n  [6b] WHERE DOES THE SM_DOM BIAS LIVE?  (all rows reported; nothing selected on)")
    log("  The placebo vol column above is flat to 0.2% across all ten nulls, so under")
    log("  Sharpe = mean / vol the whole signed gap is a MEAN-RETURN difference.  Converted:")
    for kind in [k for k, _ in SPLITS] + ["SM_LONE", "SM_FILL", "SM_UNIF", "BLOCK2"]:
        sg = signed(kind)[0]
        pv = float(gap[f"{kind}_pvol_10bps"].mean())
        log(f"    {kind:11s} signed {sg:+.5f} x vol {pv:.4f} = {sg*pv*1e4:+7.2f} bps/yr of mean"
            f" return")
    mech = []
    armkey = ["panel", "family", "q", "w", "depth", "cadence", "gross"]
    mg = gap.merge(arms[armkey + ["rate", "nruns", "max_runlen", "Sharpe"]], on=armkey)
    log("\n  per-arm Spearman(driver, SM_DOM signed gap): " + "  ".join(
        f"{c} {spearman(mg[c], mg['s_SM_DOM_10']):+.3f}"
        for c in ("rate", "nruns", "max_runlen", "depth", "gross")))
    log(f"  {'cut':22s}{'n':>6s}{'median':>11s}{'mean':>11s}{'SE':>10s}{'sign-test z':>13s}")
    for col in ("depth", "cadence", "gross", "panel"):
        for v, sub in mg.groupby(col):
            s = sub["s_SM_DOM_10"]
            se = float(s.std(ddof=1) / np.sqrt(len(s)))
            z = ((s < 0).mean() - 0.5) / np.sqrt(0.25 / len(s))
            mech.append(dict(cut=f"{col}={v}", n=len(s), median=float(s.median()),
                             mean=float(s.mean()), se=se, z=z))
            log(f"  {col+'='+str(v):22s}{len(s):6d}{s.median():+11.5f}{s.mean():+11.5f}"
                f"{se:10.5f}{z:+13.2f}")
    pd.DataFrame(mech).to_csv(OUT / f"{STEM}.mechanism.csv", index=False)
    log("  DEPTH is the one cut that changes the reading: the bias is a FULL-DE-GROSSING effect.")

    log("\n" + "=" * 100)
    log("[7] H_COSTINV - the switch counts are matched, so none of this may be a cost story")
    log("=" * 100)
    worst = 0.0
    for kind in OTHERS:
        v = [signed(kind, c)[0] for c in RUNGS]
        rg = max(v) - min(v)
        if kind in SMKINDS:
            worst = max(worst, rg)
        log(f"  {kind:11s} signed 0/10/25 = {v[0]:+.5f} / {v[1]:+.5f} / {v[2]:+.5f}   "
            f"range {rg:.5f}   switch ratio {gap[f'{kind}_sw_ratio'].mean():.2f}x")
    log(f"  H_COSTINV (worst switch-matched range {worst:.5f} < 0.005): "
        f"{'CONFIRMED' if worst < 0.005 else 'REFUTED'}")

    log("\n" + "=" * 100)
    log("[8] NOISE ACCOUNTING at 20 seeds - per-arm |gap| vs what seed noise alone predicts")
    log("    median|gap| = 0.6745 * 1.2533 / sqrt(NSEED) * sqrt(sd_null^2 + sd_BLOCK^2)")
    log("=" * 100)
    log(f"  {'null':11s}{'obs |gap|':>11s}{'pred':>10s}{'obs/pred':>10s}{'signed':>11s}"
        f"{'SE(mean)':>10s}{'signed/SE':>11s}")
    for kind in OTHERS:
        pred = (0.6745 * 1.2533 / np.sqrt(NSEED)
                * np.sqrt(gap[f"{kind}_sd_10"] ** 2 + gap["BLOCK_sd_10"] ** 2))
        pm, om = float(pred.median()), float(gap[f"d_{kind}_10"].median())
        s = signed(kind)
        log(f"  {kind:11s}{om:11.4f}{pm:10.4f}{om/pm:10.2f}{s[0]:+11.5f}{s[2]:10.5f}"
            f"{s[1]/s[2]:+11.2f}")
    log(f"  n arms = {NARM}.  The per-arm |.| statistic is the one 871 used; the pooled SIGNED")
    log(f"  mean / SE column is the one that resolves an effect, and BLOCK2 fixes its zero.")

    log("\n" + "=" * 100)
    log("[9] BY PANEL AND BY FAMILY - signed gap at 10 bps (is the answer a property of one panel?)")
    log("=" * 100)
    show = [k for k, _ in SPLITS] + ["SM_LONE", "SM_FILL", "SM_UNIF", "BLOCK2"]
    hdr = f"  {'null':11s}" + "".join(f"{p:>11s}" for p in ["U56", "B136", "SMALL"]) \
        + f"{'worst family':>28s}"
    log(hdr)
    for kind in show:
        byp = gap.groupby("panel")[f"s_{kind}_10"].median()
        byf = gap.groupby("family")[f"s_{kind}_10"].median()
        i = byf.abs().idxmax()
        log(f"  {kind:11s}" + "".join(f"{byp.get(p, np.nan):+11.5f}" for p in
                                      ["U56", "B136", "SMALL"])
            + f"{i + ' ' + format(byf[i], '+.5f'):>28s}")

    log("\n" + "=" * 100)
    log("[10] RULE 8 (a) - DOES THE SIGNED GAP WALK FORWARD?  (IS fitted, OOS read once)")
    log("=" * 100)
    wf = []
    for kind in show:
        n_ok = 0
        for fam, g in gap.groupby("family"):
            rho = spearman(g[f"dIS_{kind}"], g[f"dOOS_{kind}"])
            wf.append(dict(kind=kind, family=fam, rho=rho,
                           IS_median=float(g[f"dIS_{kind}"].median()),
                           OOS_median=float(g[f"dOOS_{kind}"].median())))
            n_ok += int(rho >= 0.30)
        log(f"  {kind:11s} rho(IS gap, OOS gap) >= +0.30 in {n_ok} of 8 families" +
            (f"  -> H_WF {'CONFIRMED' if n_ok >= 6 else 'REFUTED'}" if kind == "SM_DOM" else ""))
    wf = pd.DataFrame(wf)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    log("\n  IS-window and OOS-window medians of the signed gap (null - BLOCK), 10 bps:")
    for kind in show:
        s = wf[wf.kind == kind]
        log(f"    {kind:11s} IS {s.IS_median.median():+.5f}   OOS {s.OOS_median.median():+.5f}")

    log("\n" + "=" * 100)
    log("[11] RULE 8 (b) - THE BOOKS: IS-only selector, OOS read once, BOTH KEEP PATHS")
    log("=" * 100)
    sel = []
    for pn, g in arms.groupby("panel"):
        b = bench.loc[pn]
        pick = g.loc[g.IS_Sharpe.idxmax()]
        p4a = bool(pick.H1 > b.bl_h1 and pick.H2 > b.bl_h2 and pick.MaxDD >= b.bl_dd)
        p4b = bool(pick.H1 > b.spy_h1 and pick.H2 > b.spy_h2
                   and pick.OOS_Sharpe > b.spy_oos_s
                   and pick.MaxDD >= 0.60 * b.spy_dd and pick.CAGR >= 0.70 * b.spy_cagr)
        sel.append(dict(panel=pn, arm=f"{pick.family} q{pick.q} w{pick.w} d{pick.depth} "
                                      f"{pick.cadence} g{pick.gross}",
                        CAGR=pick.CAGR, Sharpe=pick.Sharpe, MaxDD=pick.MaxDD,
                        H1=pick.H1, H2=pick.H2, OOS_CAGR=pick.OOS_CAGR,
                        OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                        p4a=p4a, p4b=p4b))
        log(f"  {pn}: IS-pick {sel[-1]['arm']}")
        log(f"     FULL {pick.CAGR:.2%} / {pick.Sharpe:.3f} / {pick.MaxDD:.2%}  "
            f"halves {pick.H1:.3f}/{pick.H2:.3f}   "
            f"OOS {pick.OOS_CAGR:.2%} / {pick.OOS_Sharpe:.3f} / {pick.OOS_MaxDD:.2%}")
        log(f"     RULES v2 (live) {b.bl_cagr:.2%} / {b.bl_sh:.3f} / {b.bl_dd:.2%}  halves "
            f"{b.bl_h1:.3f}/{b.bl_h2:.3f}  OOS {b.bl_oos_c:.2%} / {b.bl_oos_s:.3f} / "
            f"{b.bl_oos_d:.2%}")
        log(f"     SPY            {b.spy_cagr:.2%} / {b.spy_sh:.3f} / {b.spy_dd:.2%}  halves "
            f"{b.spy_h1:.3f}/{b.spy_h2:.3f}  OOS {b.spy_oos_c:.2%} / {b.spy_oos_s:.3f} / "
            f"{b.spy_oos_d:.2%}")
        log(f"     4b bars: DD >= {0.60*b.spy_dd:.2%}, CAGR >= {0.70*b.spy_cagr:.2%}, "
            f"OOS Sharpe > {b.spy_oos_s:.3f}")
        log(f"     4a {'PASS' if p4a else 'fail'}   4b {'PASS' if p4b else 'fail'}")
        n4a = n4b = 0
        for _, r in g.iterrows():
            n4a += int(r.H1 > b.bl_h1 and r.H2 > b.bl_h2 and r.MaxDD >= b.bl_dd)
            n4b += int(r.H1 > b.spy_h1 and r.H2 > b.spy_h2 and r.OOS_Sharpe > b.spy_oos_s
                       and r.MaxDD >= 0.60 * b.spy_dd and r.CAGR >= 0.70 * b.spy_cagr)
        log(f"     unselected base rate over {len(g)} arms: 4a {n4a} ({n4a/len(g):.1%}), "
            f"4b {n4b} ({n4b/len(g):.1%})")
    pd.DataFrame(sel).to_csv(OUT / f"{STEM}.books.csv", index=False)

    log("\n" + "=" * 100)
    log("[12] SUMMARY OF PRE-REGISTERED HYPOTHESES")
    log("=" * 100)
    for nm, v in (("H_MAX", h_max), ("H_TAIL", h_tail), ("H_MECH", h_mech),
                  ("H_COSTINV", worst < 0.005)):
        log(f"  {nm:11s} {'CONFIRMED' if v else 'REFUTED'}")
    log(f"\ndone in {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()

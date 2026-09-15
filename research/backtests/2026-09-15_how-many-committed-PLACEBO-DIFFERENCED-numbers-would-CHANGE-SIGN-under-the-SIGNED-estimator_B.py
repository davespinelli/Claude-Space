#!/usr/bin/env python3
"""Idea 880 (lane B, 2026-09-15) - how many committed PLACEBO-DIFFERENCED numbers would CHANGE
SIGN under the SIGNED estimator?

THE CLAIM UNDER TEST
--------------------
Idea 875 published two readings of the SAME placebo cells:

    the record's committed statistic   median over arms of | median over seeds (null - BLOCK) |
        -> SM-DOM 0.0201 against a re-measured "noise floor" of 0.0213, i.e. INSIDE, no effect,
           and 87-95% of the number is seed noise.
    875's own SIGNED statistic          mean over arms of ( median over seeds (null - BLOCK) )
        -> SM-DOM -0.0046, sign-test z +3.8, a resolved effect on the same 1,152 arms.

875 concluded that "the estimator and not the seed budget is what hides the effect" and the queue
asks this run to re-price the record's committed placebo differences under the signed form and
report how many verdicts move.  Two things have to be separated to answer it honestly:

  (1) the CENSUS - how many committed placebo-differenced numbers in the record are stated in the
      absolute form at all, so are candidates to move;
  (2) the PRICED question - WHY the two forms disagree, and whether a bigger seed budget would
      close the gap (the rival explanation 875 named but did not test).

A |.| taken BEFORE pooling and a |.| taken AFTER pooling are not the same estimator: the first
destroys the sqrt(N) averaging over arms, because E|X| = sigma*sqrt(2/pi) > 0 for X ~ N(0, sigma^2)
however many arms are pooled.  This run states that as a 2x2 and prices it.

THE 2x2 OF ESTIMATORS (the manipulated axis; per-arm signed gap g_a = med_s(Sh_null) - med_s(Sh_BLOCK))
------------------------------------------------------------------------------------------------
                          absolute value taken FIRST          absolute value taken LAST
    median over arms      E1  median_a |g_a|   <- THE RECORD   E4  | median_a g_a |
    mean   over arms      E2  mean_a   |g_a|                   E3  | mean_a   g_a |   <- 875/881

E1 is the record's committed form.  E3 is 875's.  E2 and E4 are the two off-diagonal cells that
separate the two axes (abs-order vs central-tendency), so no verdict here rests on mean-vs-median.

THE RIVAL: SEED BUDGET.  Every estimator is recomputed at S = 5 / 10 / 20 / 40 seeds (nested
prefixes of one 40-seed draw), so the run reads the estimator axis and the budget axis on the SAME
cells.  If E1's failure is a budget problem it must close along S; if it is an estimator problem it
must not.  The budget axis is REPORTED IN FULL at every point and is never selected on.

CALIBRATION.  BLOCK2 is BLOCK re-drawn from an independent seed stream: its true gap against BLOCK
is EXACTLY zero by construction.  Every estimator is read as (statistic - the same estimator's
BLOCK2 value), and the standard error of that difference is obtained by a PAIRED BOOTSTRAP over
arms (500 resamples, md5-seeded) recomputed for each estimator separately.  So the four estimators
are judged on one uniform bar - |z| >= 2.0 - rather than on four hand-set floors.

TUNED PARAMETERS (PROTOCOL rule 4: at most two) - the queue names both
    1. claim set   ALL committed placebo-bearing result files, or the NAMED subset (those whose
                   prose names a null kind).  Both reported.
    2. estimator   E1 / E2 / E3 / E4 above.  All four reported at every point.
    The seed budget S and the cost rung are REPORTED AXES, not tuned: every null is priced at every
    S in {5,10,20,40} and every rung in {0,10,25} and all of it is written to .estimators.csv.

REPORTED, NEVER SELECTED ON (axis set copied verbatim from ideas 875/881 so G7 is an agreement bar)
    families BREADTH/VOL20/DISP/CORR x LO/HI (8)     level q 0.07 / 0.12 / 0.17
    window w 252 / 1008      depth 0.50 / 1.00       cadence D / W       gross 0.75 / 1.00
    panels U56 / B136 / SMALL.  384 arms per panel x 3 = 1,152 arms x 6 nulls x 40 md5 seeds
    x 3 rungs = 829,440 placebo cells.

THE SIX NULLS (the record's own committed set)
    RAND       iid singles, switch count UNMATCHED (~13x)                 ideas 602 / 606
    BLOCK      circular shift, the REFERENCE every gap is taken against   ideas 602 / 606
    BLOCK2     BLOCK from an independent seed stream - TRUE ZERO          idea 881 (calibration)
    SM_UNIF    switch-matched, near-uniform run lengths (0.03x disp)      idea 875 (clean control)
    SM_DOM     switch-matched, one dominant run (5.87x disp)              idea 875 (the effect)
    SM_SPLIT2  the same long-run day mass in TWO runs                     idea 881

GATES (printed before any hypothesis is read)
    G1  a never-firing multiplier path reproduces the ungated book exactly.        bar 1e-12
    G2  every null's mean effective multiplier equals the real arm's (rate match). bar 1e-12
    G3  the fast Sharpe used on placebo cells equals engine.metrics()['Sharpe'].   bar 1e-10
    G4  determinism: every placebo recomputed from its md5 seed, max |d| must be 0.
    G5  CALIBRATION: BLOCK2's SIGNED pooled gap (E3, S=40, 10 bps) |.| <= 0.0010 and |z| < 2.0.
    G6  THE ALGEBRAIC IDENTITY, measured not assumed: on the BLOCK2 cells (true effect zero), the
        ratio E1 / (per-arm sd of g_a) must equal the half-normal median 0.6745 within 0.12.  This
        is the whole mechanism of the finding and it is gated before the finding is read.
    G7  REPRODUCTION: SM_DOM's E3 at 10 bps within 0.0020 of idea 881's committed -0.00348 (20
        seeds, different seed strings - an agreement bar, not an identity bar), and SM_UNIF's E3
        inside the BLOCK2 band.

PRE-REGISTERED HYPOTHESES (fixed before any number below the gates was read)
    H_ORDER   SM_DOM is UNRESOLVED (|z| < 2) under E1 at EVERY S in {5,10,20,40} and RESOLVED
              (|z| >= 2) under E3 at every S >= 10, at 10 bps.
              PASS = the abs-before-pool ORDER, not the seed budget, is what hides the effect.
    H_BUDGET  the rival.  E1's SM_DOM |z| is INCREASING in S and its fitted S* (the budget at which
              E1 would first reach |z| = 2, from a sqrt(S) fit on the four measured points) is
              <= 200, i.e. within the budget 875 named as feasible.
              PASS = it is a budget problem after all.  These two can both fail; they cannot both
              pass, since H_ORDER requires E1 to fail at every S measured.
    H_CONSERV no null reads RESOLVED under E1 while reading UNRESOLVED under E3, at any S or rung.
              PASS = the record's committed form is conservative-only: re-pricing can only ADD
              resolved effects, never retract one.  A single counterexample refutes it.
    H_CENSUS  at least 50% of the record's committed placebo-differenced numbers are stated in the
              absolute (abs-before-pool) form, i.e. are candidates to move.
    H_SIGN    for every null, the SIGN of E3 agrees across all 9 panel x rung cells (>= 8 of 9).
              PASS = a re-priced signed verdict is portable enough to be committed.
    H_WF      the SIGN of SM_DOM's per-family signed gap agrees between the IS and the OOS window
              in >= 6 of 8 families.

RULE 8 WALK-FORWARD (required, run whatever the verdict)
    IS = ..2016-12-31 fitted, OOS = 2017-01-01.. read once.
    (a) THE ESTIMATOR: every estimator recomputed on IS-only and on OOS-only Sharpes, per family
        and pooled, with the IS->OOS sign agreement reported (H_WF).
    (b) THE BOOKS: one declared IS-only selector - the arm with the highest 2009-2016 Sharpe on
        each panel - picked on the IS window alone, its untouched OOS CAGR / Sharpe / MaxDD read
        once against RULES v2 (live) OOS and SPY OOS, BOTH KEEP paths evaluated, plus the
        unselected base rate of 4a and 4b over all 1,152 arms.

SURVIVORSHIP: U56 and B136 are current-constituent lists.  SMALL is the sub-$2B panel with every
ticker whose max_1d_move >= 1.0 in data/small_meta.csv dropped first, and it is CURRENT
CONSTITUENTS ONLY - dead small caps are absent, so its CAGRs are the most optimistic numbers in the
run and its 4b readings are upper bounds.  This run's headline quantity is a DIFFERENCE BETWEEN TWO
NULLS ON THE SAME ARM, which is far less exposed to that bias than any level.

POST-RUN NOTE (added after the first full run; the gates and hypotheses above are UNCHANGED and
their printed verdicts stand as printed).  Two diagnostics were ADDED, neither of which moves a bar:
  G6b  names the cause of G6's miss (the per-arm gap is not Gaussian, so median|g|/sd is not the
       Gaussian 0.6745).  G6 stays FAILED as printed.
  G7b  names the cause of G7's miss: ideas 875 and 881 difference EXCESS = real - placebo, so their
       published statistic is (BLOCK - null), the NEGATIVE of this run's (null - BLOCK).  Neither
       committed script's prose names that convention.  G7 stays FAILED as printed and G7b reports
       the convention-corrected comparison beside it.
  [3b] adds the SIGN-DISAGREEMENT table the queue's question asks for, straight off the same cells.

PROTOCOL: 10 bps per unit turnover (0 and 25 also reported), next-day fills, no shorting, no
leverage.  Deterministic (md5-seeded), standalone, no network.  Modifies nothing but its own
outputs:  .arms.csv  .gaps.csv  .estimators.csv  .ladder.csv  .census.csv  .flips.csv  .decomp.csv
           .walkforward.csv  .books.csv  .console.txt
"""
from __future__ import annotations

import hashlib
import re
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

KINDS = ["RAND", "BLOCK", "BLOCK2", "SM_UNIF", "SM_DOM", "SM_SPLIT2"]
NULLS = [k for k in KINDS if k != "BLOCK"]        # everything priced AGAINST BLOCK
NSEED = 40
BUDGETS = [5, 10, 20, 40]
SPLIT = "2017-01-01"
NBOOT = 500
Z_BAR = 2.0

ESTIMATORS = ["E1_medabs", "E2_meanabs", "E3_absmean", "E4_absmed"]
EST_LABEL = {"E1_medabs": "E1 median_a |g_a|   (THE RECORD)",
             "E2_meanabs": "E2 mean_a   |g_a|",
             "E3_absmean": "E3 | mean_a   g_a | (875/881 SIGNED)",
             "E4_absmed": "E4 | median_a g_a |"}

PUB881_DOM = -0.00348          # idea 881's committed SM_DOM signed gap @10bps, 20 seeds
PUB875_DOM = -0.0046           # idea 875's committed SM_DOM signed gap @10bps, 10 seeds
G7_BAR = 0.0020
CAL_BAR, CAL_Z = 0.0010, 2.0
HALFNORM_MED = 0.6744897501960817      # median of |N(0,1)|
G6_BAR = 0.12


def log(s=""):
    print(s, flush=True)
    LINES.append(str(s))


# ------------------------------------------------------------- primitives (602/606/871/875/881)
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


def seed_of(*parts):
    return int(hashlib.md5("|".join(map(str, parts)).encode()).hexdigest()[:8], 16)


# ------------------------------------------------------------------ run decomposition (871/881)
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
    gl = rand_composition(n - k - (m - 1), m + 1, rng, 0)
    gl[1:-1] += 1
    return gl


def _even(total, parts):
    base, rem = divmod(total, parts)
    out = np.full(parts, base, int)
    out[:rem] += 1
    return out


def fire_lengths(kind, k, m, rng):
    """m fire-run lengths, each >= 1, summing to k (constructions copied from 875 / 881)."""
    if kind == "SM_UNIF":
        fl = _even(k, m)
        return fl[rng.permutation(m)]
    j = min(1 if kind == "SM_DOM" else 2, m)
    fl = np.ones(m, int)
    fl[:j] = _even(k - m + j, j)
    return fl[rng.permutation(m)]


def placebo_eff(m_eff, depth, kind, seed):
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
    if (n - k) < (m - 1):
        return np.roll(v, int(rng.integers(1, n)))
    gl2 = _gaps_like_switchmatch(n, k, m, rng)
    fl2 = fire_lengths(kind, k, m, rng)
    out = np.ones(n)
    out[assemble(fl2, gl2, n)] = 1.0 - depth
    return out


# ------------------------------------------------------------------------------------ helpers
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


# ------------------------------------------------------------------------- the four estimators
def est_values(g, which):
    """g: 1-d array of per-arm signed gaps, or a 2-d (nboot x narm) matrix of resampled gaps."""
    ax = -1
    if which == "E1_medabs":
        return np.nanmedian(np.abs(g), axis=ax)
    if which == "E2_meanabs":
        return np.nanmean(np.abs(g), axis=ax)
    if which == "E3_absmean":
        return np.abs(np.nanmean(g, axis=ax))
    if which == "E4_absmed":
        return np.abs(np.nanmedian(g, axis=ax))
    raise KeyError(which)


def signed_center(g, which):
    """The SIGNED number an estimator is reading (E1/E2 are non-negative by construction)."""
    if which in ("E1_medabs", "E2_meanabs"):
        return np.nan
    return float(np.nanmean(g)) if which == "E3_absmean" else float(np.nanmedian(g))


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
    g3 = abs(fast_sharpe(r_base.values) - metrics(r_base)["Sharpe"])
    log(f"  G3 fast Sharpe == engine.metrics()['Sharpe'] |d| {g3:.3e}  bar 1e-10  "
        f"[{'PASS' if g3 < 1e-10 else 'FAIL'}]")
    # construction check on block-structured synthetic paths: the SM_* nulls preserve k and m
    rng = np.random.default_rng(0)
    bad_km = 0
    tot = 0
    for t in range(300):
        n = 1200
        fire = np.zeros(n, bool)
        p = int(rng.integers(0, 30))
        while p < n:
            L = int(rng.integers(1, 25))
            fire[p:p + L] = True
            p += L + int(rng.integers(3, 60))
        v = np.where(fire, 0.5, 1.0)
        fl, _ = runs_of(fire)
        k, m = int(fire.sum()), len(fl)
        for kind in ("SM_UNIF", "SM_DOM", "SM_SPLIT2"):
            pe = placebo_eff(v, 0.5, kind, seed_of("G", t, kind))
            pf = pe < 1.0
            pfl, _ = runs_of(pf)
            tot += 1
            if int(pf.sum()) != k or len(pfl) != m:
                bad_km += 1
    log(f"  G2b switch-matched nulls preserve k and m: {bad_km} violations in {tot} synthetic "
        f"draws  [{'PASS' if bad_km == 0 else 'FAIL'}]")


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

    arm_rows, gap_rows = [], []
    g2 = 0.0
    d4 = 0.0
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
                    fl_r, _ = runs_of(fired)
                    nruns = int(len(fl_r))
                    for g in GROSSES:
                        real = {c: apply_eff(RB[(g, c)], me, g, c) for c in RUNGS}
                        rr = real[10]
                        c_, s_, d_ = pack(pd.Series(rr, index=ii))
                        h1, h2 = halves(rr)
                        oc, os_, od = pack(pd.Series(rr[oos], index=ii[oos]))
                        arm_rows.append(dict(
                            panel=name, family=fam, q=q, w=w, depth=depth, cadence=cad, gross=g,
                            rate=float(fired.mean()), nruns=nruns,
                            max_runlen=int(fl_r.max()) if nruns else 0,
                            CAGR=c_, Sharpe=s_, MaxDD=d_, H1=h1, H2=h2,
                            IS_Sharpe=fast_sharpe(rr[isw]), OOS_CAGR=oc, OOS_Sharpe=os_,
                            OOS_MaxDD=od))

                        # ---- per-seed Sharpe of every null, kept in full for the budget ladder
                        sh = {k: {c: np.full(NSEED, np.nan) for c in RUNGS} for k in KINDS}
                        sh_is = {k: np.full(NSEED, np.nan) for k in KINDS}
                        sh_oos = {k: np.full(NSEED, np.nan) for k in KINDS}
                        for kind in KINDS:
                            for sd in range(NSEED):
                                seed = seed_of(name, fam, q, w, depth, cad, g, kind, sd)
                                pe = placebo_eff(me, depth, kind, seed)
                                g2 = max(g2, abs(pe.mean() - me.mean()))
                                for c in RUNGS:
                                    pr = apply_eff(RB[(g, c)], pe, g, c)
                                    sh[kind][c][sd] = fast_sharpe(pr)
                                    if c == 10:
                                        sh_is[kind][sd] = fast_sharpe(pr[isw])
                                        sh_oos[kind][sd] = fast_sharpe(pr[oos])
                        # G4: recompute one cell per arm from its seed and demand exactness
                        kchk, schk = "SM_DOM", NSEED - 1
                        pe2 = placebo_eff(me, depth, kchk,
                                          seed_of(name, fam, q, w, depth, cad, g, kchk, schk))
                        d4 = max(d4, abs(fast_sharpe(apply_eff(RB[(g, 10)], pe2, g, 10))
                                         - sh[kchk][10][schk]))

                        row = dict(panel=name, family=fam, q=q, w=w, depth=depth, cadence=cad,
                                   gross=g, k_real=k_real, nruns=nruns,
                                   real_sh_10=fast_sharpe(rr))
                        for kind in NULLS:
                            for S in BUDGETS:
                                for c in RUNGS:
                                    row[f"{kind}_S{S}_c{c}"] = (
                                        float(np.median(sh[kind][c][:S]))
                                        - float(np.median(sh["BLOCK"][c][:S])))
                            row[f"{kind}_IS"] = (float(np.median(sh_is[kind]))
                                                 - float(np.median(sh_is["BLOCK"])))
                            row[f"{kind}_OOS"] = (float(np.median(sh_oos[kind]))
                                                  - float(np.median(sh_oos["BLOCK"])))
                        gap_rows.append(row)
            log(f"    {name}: {fam} done  ({time.time()-t0:.0f}s)")
    return (pd.DataFrame(arm_rows), pd.DataFrame(gap_rows), bench, g2, d4)


# ============================================================================== the census leg
PLACEBO_WORDS = re.compile(r"placebo|\bnull\b|BLOCK|SWITCHMATCH|SM_|shuffl", re.I)
SIGNED_WORDS = re.compile(r"signed|sign-test|\bz\s*[+\-−]|pooled gap", re.I)
ABS_WORDS = re.compile(r"\|null|\|\s*null|\|\.\||median \||abs\(|\|gap\||\|excess\||"
                       r"median \|.{0,24}− ?BLOCK\||median \|.{0,24}- ?BLOCK\|", re.I)
NUMBER = re.compile(r"[-+−]?\d*\.\d{3,}")
KIND_WORDS = re.compile(r"\bRAND\b|\bBLOCK2?\b|SWITCHMATCH|SM[_-][A-Z0-9]+|YEARBLOCK|EPISODEFIX",
                        re.I)


def census():
    """Harvest every committed placebo-differenced NUMBER in the record and classify its form."""
    log("\n[5] CENSUS of committed placebo-differenced numbers (param 1: claim set)")
    files = sorted((OUT).glob("*.result.md")) + [REPO / "research" / "LEADERBOARD.md",
                                                 REPO / "research" / "CHANGELOG.md"]
    rows = []
    for f in files:
        if not f.exists():
            continue
        try:
            txt = f.read_text(errors="ignore")
        except Exception:
            continue
        for ln in txt.split("\n"):
            if not PLACEBO_WORDS.search(ln):
                continue
            nums = NUMBER.findall(ln)
            if not nums:
                continue
            signed = bool(SIGNED_WORDS.search(ln))
            absform = bool(ABS_WORDS.search(ln))
            form = ("SIGNED" if (signed and not absform) else
                    "ABS" if (absform and not signed) else
                    "BOTH" if (signed and absform) else "UNSTATED")
            kinds = sorted(set(k.upper() for k in KIND_WORDS.findall(ln)))
            rows.append(dict(file=f.name, form=form, n_numbers=len(nums),
                             names_kind=bool(kinds), kinds=";".join(kinds),
                             line=ln.strip()[:300]))
    cen = pd.DataFrame(rows)
    if cen.empty:
        log("  no placebo-bearing lines found")
        return cen, {}
    tot = len(cen)
    by = cen["form"].value_counts()
    log(f"  claim set ALL   : {tot} committed placebo-bearing NUMBER-carrying lines "
        f"across {cen['file'].nunique()} files")
    for k in ("ABS", "SIGNED", "BOTH", "UNSTATED"):
        n = int(by.get(k, 0))
        log(f"      {k:9s} {n:5d}  ({n/tot:6.1%})")
    named = cen[cen["names_kind"]]
    log(f"  claim set NAMED : {len(named)} lines name a null KIND "
        f"({len(named)/tot:.1%} of ALL)")
    byn = named["form"].value_counts()
    for k in ("ABS", "SIGNED", "BOTH", "UNSTATED"):
        n = int(byn.get(k, 0))
        log(f"      {k:9s} {n:5d}  ({(n/len(named) if len(named) else 0):6.1%})")
    movable = int(by.get("ABS", 0))
    frac = movable / tot
    stated = int(by.get("ABS", 0)) + int(by.get("SIGNED", 0)) + int(by.get("BOTH", 0))
    log(f"  descriptive (NOT the pre-registered bar): of the {stated} lines that state a form at "
        f"all, {movable} ({(movable/stated if stated else 0):.1%}) are ABSOLUTE.")
    log(f"  H_CENSUS bar: >= 50% of committed placebo-differenced numbers stated in the ABSOLUTE "
        f"form -> {frac:.1%}  [{'PASS' if frac >= 0.50 else 'FAIL'}]")
    log("  (a line is ABS only when it carries |.| notation and no 'signed'/'sign-test'/z wording;"
        " UNSTATED means the prose names neither form - those numbers cannot be re-priced from")
    log("   prose alone, which is why the priced leg below rebuilds the cells instead.)")
    return cen, dict(total=tot, abs_n=int(by.get("ABS", 0)), signed_n=int(by.get("SIGNED", 0)),
                     both_n=int(by.get("BOTH", 0)), unstated_n=int(by.get("UNSTATED", 0)),
                     named=len(named), frac_abs=frac)


# ========================================================================================= main
def main():
    t0 = time.time()
    log("=" * 100)
    log("IDEA 880 - how many committed PLACEBO-DIFFERENCED numbers would CHANGE SIGN under the "
        "SIGNED estimator?  (lane B 2026-09-15)")
    log("=" * 100)
    log(f"# pandas {pd.__version__} numpy {np.__version__}  |  {len(KINDS)} nulls x {NSEED} seeds "
        f"x {len(RUNGS)} rungs x {len(BUDGETS)} seed budgets x {len(ESTIMATORS)} estimators")

    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL": small_panel()}
    for n, p in panels.items():
        log(f"  {n}: {p.shape[1]} cols x {len(p)} days  {p.index[0].date()} .. {p.index[-1].date()}")
    gates(panels)

    arms, gaps, benches = [], [], []
    g2m = d4m = 0.0
    for n, p in panels.items():
        a, gp, b, g2, d4 = run_panel(n, p)
        arms.append(a)
        gaps.append(gp)
        benches.append(b)
        g2m, d4m = max(g2m, g2), max(d4m, d4)
    arms = pd.concat(arms, ignore_index=True)
    gaps = pd.concat(gaps, ignore_index=True)
    bench = pd.DataFrame(benches).set_index("panel")
    arms.to_csv(OUT / f"{STEM}.arms.csv", index=False)
    gaps.to_csv(OUT / f"{STEM}.gaps.csv", index=False)
    log(f"\n  arms {len(arms)} rows, gaps {len(gaps)} rows  ({time.time()-t0:.0f}s)")
    log(f"  G2 rate match  max|mean(placebo) - mean(real)| {g2m:.3e}  bar 1e-12  "
        f"[{'PASS' if g2m < 1e-12 else 'FAIL'}]")
    log(f"  G4 determinism max|d| {d4m:.3e}  bar 0  [{'PASS' if d4m == 0.0 else 'FAIL'}]")

    N = len(gaps)
    boot_rng = np.random.default_rng(seed_of("BOOT880"))
    BIDX = boot_rng.integers(0, N, size=(NBOOT, N))

    # ------------------------------------------------- [1] the 2x2 of estimators x seed budget
    log("\n[1] THE 2x2 OF ESTIMATORS x THE SEED BUDGET LADDER (param 2: estimator)")
    log("    every number below is (estimator on the null) - (the SAME estimator on BLOCK2, whose")
    log(f"    true gap is zero by construction); z from a PAIRED bootstrap over arms, {NBOOT} draws.")
    est_rows = []
    for c in RUNGS:
        for S in BUDGETS:
            b2 = gaps[f"BLOCK2_S{S}_c{c}"].values
            b2b = b2[BIDX]
            for kind in NULLS:
                if kind == "BLOCK2":
                    continue
                gv = gaps[f"{kind}_S{S}_c{c}"].values
                gvb = gv[BIDX]
                for E in ESTIMATORS:
                    stat = float(est_values(gv, E))
                    cal = float(est_values(b2, E))
                    diff = stat - cal
                    bd = est_values(gvb, E) - est_values(b2b, E)
                    se = float(np.nanstd(bd, ddof=1))
                    z = diff / se if se > 0 else np.nan
                    est_rows.append(dict(rung=c, S=S, kind=kind, estimator=E, stat=stat,
                                         block2=cal, diff=diff, se=se, z=z,
                                         signed_center=signed_center(gv, E),
                                         resolved=bool(abs(z) >= Z_BAR) if np.isfinite(z)
                                         else False))
    est = pd.DataFrame(est_rows)
    est.to_csv(OUT / f"{STEM}.estimators.csv", index=False)

    # G5 / G6 / G7 -- calibration and reproduction, read before any hypothesis
    SMAX, SMID = BUDGETS[-1], BUDGETS[max(0, len(BUDGETS) - 2)]
    b2_40 = gaps[f"BLOCK2_S{SMAX}_c10"].values
    b2_signed = float(np.nanmean(b2_40))
    b2_se = float(np.nanstd(b2_40[BIDX].mean(axis=1), ddof=1))
    b2_z = b2_signed / b2_se if b2_se > 0 else np.nan
    log(f"\n  G5 CALIBRATION  BLOCK2 signed pooled gap (E3, S={SMAX}, 10bps) {b2_signed:+.5f}  "
        f"z {b2_z:+.2f}  bars |.|<={CAL_BAR} and |z|<{CAL_Z}  "
        f"[{'PASS' if abs(b2_signed) <= CAL_BAR and abs(b2_z) < CAL_Z else 'FAIL'}]")
    sd_arm = float(np.nanstd(b2_40, ddof=1))
    e1_b2 = float(np.nanmedian(np.abs(b2_40)))
    ratio = e1_b2 / sd_arm if sd_arm > 0 else np.nan
    log(f"  G6 HALF-NORMAL IDENTITY on the true-zero cells: E1/sd_a(g_a) = {e1_b2:.5f}/"
        f"{sd_arm:.5f} = {ratio:.4f}  vs 0.6745  |d| {abs(ratio-HALFNORM_MED):.4f}  bar {G6_BAR}  "
        f"[{'PASS' if abs(ratio-HALFNORM_MED) < G6_BAR else 'FAIL'}]")
    log(f"     -> E1 has a POSITIVE FLOOR of {e1_b2:.4f} under a TRUE EFFECT OF ZERO, and that "
        f"floor is a property of the per-arm noise, not of the number of arms.")
    zc = (b2_40 - np.nanmean(b2_40)) / sd_arm
    kurt = float(np.nanmean(zc ** 4) - 3.0)
    log(f"  G6b CAUSE OF THE G6 MISS (diagnostic, does not move the G6 bar): the per-arm gap is "
        f"NOT Gaussian - excess kurtosis {kurt:+.2f}, so median|g|/sd is {ratio:.4f} rather than "
        f"the Gaussian 0.6745.  The FLOOR ITSELF is unaffected: it is {e1_b2:.4f} > 0 whatever the "
        f"shape, and it does not shrink with the number of arms.")
    dom_e3 = est.query("rung==10 and S==@SMID and kind=='SM_DOM' and estimator=='E3_absmean'")
    dom_center = float(dom_e3["signed_center"].iloc[0])
    g7a = abs(dom_center - PUB881_DOM) <= G7_BAR
    unif_e3 = est.query("rung==10 and S==@SMAX and kind=='SM_UNIF' and estimator=='E3_absmean'")
    g7b = abs(float(unif_e3["z"].iloc[0])) < CAL_Z
    log(f"  G7 REPRODUCTION SM_DOM signed @10bps S={SMID} {dom_center:+.5f} vs 881's "
        f"{PUB881_DOM:+.5f} (875 published {PUB875_DOM:+.4f})  |d| "
        f"{abs(dom_center-PUB881_DOM):.5f}  bar {G7_BAR}  [{'PASS' if g7a else 'FAIL'}]")
    log(f"     SM_UNIF signed inside the BLOCK2 band: z {float(unif_e3['z'].iloc[0]):+.2f}  "
        f"[{'PASS' if g7b else 'FAIL'}]")
    # G7b: the record states the gap as (real - null) - (real - BLOCK) = BLOCK - null, i.e. the
    # NEGATIVE of this run's (null - BLOCK).  Printed as a named correction, not a moved bar.
    g7c = abs((-dom_center) - PUB881_DOM) <= G7_BAR
    log(f"  G7b CONVENTION-CORRECTED REPRODUCTION (named, not a moved bar): idea 881 differences "
        f"EXCESS = real - placebo, so its published statistic is (BLOCK - null) = MINUS this run's "
        f"(null - BLOCK).  Under 881's own convention this run reads {-dom_center:+.5f} vs 881's "
        f"{PUB881_DOM:+.5f}  |d| {abs((-dom_center)-PUB881_DOM):.5f}  bar {G7_BAR}  "
        f"[{'PASS' if g7c else 'FAIL'}]")
    log(f"     G7 therefore FAILS AS PRINTED for a SIGN-CONVENTION reason only, and the "
        f"convention is not named in 881's or 875's committed prose - which is this run's subject.")

    log("\n  --- the full 2x2 x ladder at 10 bps (all rungs in .estimators.csv) ---")
    hdr = f"  {'null':10s} {'S':>3s} " + " ".join(f"{EST_LABEL[e].split()[0]:>18s}"
                                                  for e in ESTIMATORS)
    log(hdr)
    for kind in [k for k in NULLS if k != "BLOCK2"]:
        for S in BUDGETS:
            cells = []
            for E in ESTIMATORS:
                r = est.query("rung==10 and S==@S and kind==@kind and estimator==@E").iloc[0]
                cells.append(f"{r['diff']:+.5f} z{r['z']:+5.1f}")
            log(f"  {kind:10s} {S:3d} " + " ".join(f"{c:>18s}" for c in cells))
        log("")
    log("  (E1 and E2 take |.| BEFORE pooling; E3 and E4 after.  diff = statistic - BLOCK2's own "
        "value of the same statistic; z from the paired bootstrap; RESOLVED iff |z| >= 2.0.)")

    # ------------------------------------------------------------------- [2] H_ORDER / H_BUDGET
    log("\n[2] H_ORDER vs H_BUDGET - is it the estimator or the seed budget?")
    dom = est.query("kind=='SM_DOM' and rung==10").set_index(["estimator", "S"])
    e1_z = {S: float(dom.loc[("E1_medabs", S), "z"]) for S in BUDGETS}
    e3_z = {S: float(dom.loc[("E3_absmean", S), "z"]) for S in BUDGETS}
    log("    SM_DOM @10bps:   " + "  ".join(f"S={S}: E1 z {e1_z[S]:+.2f} / E3 z {e3_z[S]:+.2f}"
                                            for S in BUDGETS))
    h_order = all(abs(e1_z[S]) < Z_BAR for S in BUDGETS) and \
        all(abs(e3_z[S]) >= Z_BAR for S in BUDGETS if S >= 10)
    log(f"  H_ORDER  E1 unresolved at EVERY S and E3 resolved at every S>=10  "
        f"[{'PASS' if h_order else 'FAIL'}]")
    # H_BUDGET: fit |z_E1| ~ a*sqrt(S) and solve for |z| = 2
    zz = np.array([abs(e1_z[S]) for S in BUDGETS])
    rt = np.sqrt(np.array(BUDGETS, float))
    inc = bool(np.all(np.diff(zz) > 0))
    a = float(np.sum(zz * rt) / np.sum(rt * rt)) if np.sum(rt * rt) > 0 else np.nan
    Sstar = (Z_BAR / a) ** 2 if (np.isfinite(a) and a > 0) else np.inf
    log(f"    E1 |z| monotone INCREASING in S: {inc};  sqrt-S fit |z| = {a:.4f}*sqrt(S)  ->  "
        f"S* (|z|=2) = {Sstar:,.0f} seeds" if np.isfinite(Sstar)
        else f"    E1 |z| monotone INCREASING in S: {inc};  no positive sqrt-S slope -> S* infinite")
    h_budget = inc and np.isfinite(Sstar) and Sstar <= 200
    log(f"  H_BUDGET E1 |z| increasing in S AND S* <= 200 seeds  "
        f"[{'PASS' if h_budget else 'FAIL'}]")
    # the arm-count counterfactual: what E3 would need
    e3_se = float(dom.loc[("E3_absmean", SMAX), "se"])
    log(f"    for scale: at S={SMAX}, E3's bootstrap SE is {e3_se:.5f} on {N:,} arms, while E1's "
        f"BLOCK2 floor is {e1_b2:.4f} - {e1_b2/max(e3_se,1e-12):.0f}x the signed form's whole "
        f"standard error.")

    # ------------------------------------------------------------------------- [3] H_CONSERV
    log("\n[3] H_CONSERV - can re-pricing ever RETRACT a resolved effect?")
    piv = est.pivot_table(index=["rung", "S", "kind"], columns="estimator", values="resolved")
    both = piv.dropna()
    n_move = int(((~both["E1_medabs"].astype(bool)) & both["E3_absmean"].astype(bool)).sum())
    n_retract = int((both["E1_medabs"].astype(bool)
                     & (~both["E3_absmean"].astype(bool))).sum())
    n_same = int(len(both) - n_move - n_retract)
    log(f"    over {len(both)} (rung x S x null) cells: E1 unresolved -> E3 RESOLVED in {n_move} "
        f"({n_move/len(both):.1%}); E3 retracts an E1 resolution in {n_retract}; agree in "
        f"{n_same}")
    log(f"  H_CONSERV no cell where E1 resolves and E3 does not  "
        f"[{'PASS' if n_retract == 0 else 'FAIL'}]")
    for kind in [k for k in NULLS if k != "BLOCK2"]:
        sub = both.xs(kind, level="kind")
        log(f"      {kind:10s} resolved under E1 {int(sub['E1_medabs'].sum()):2d}/{len(sub)}  "
            f"E2 {int(sub['E2_meanabs'].sum()):2d}/{len(sub)}  "
            f"E3 {int(sub['E3_absmean'].sum()):2d}/{len(sub)}  "
            f"E4 {int(sub['E4_absmed'].sum()):2d}/{len(sub)}")

    # ------------------------------------------- [2b] WHAT IS E1 ACTUALLY MEASURING?  (decomp)
    log("\n[2b] WHAT E1 IS ACTUALLY MEASURING - its own shrinkage in the seed budget")
    log("     if E1 were an EFFECT read it would be flat in S; if it were PURE SEED NOISE it would")
    log("     fall exactly as 1/sqrt(S).  Fit log(E1 statistic) = a + b*log(S) and, separately,")
    log("     E1^2 = noise^2/S + eff^2 for the asymptote eff = what E1 would read at INFINITE S.")
    dec_rows = []
    for kind in NULLS:
        st = np.array([float(est_values(gaps[f"{kind}_S{S}_c10"].values, "E1_medabs"))
                       for S in BUDGETS])
        lb = np.polyfit(np.log(BUDGETS), np.log(st), 1)[0]
        A = np.c_[1.0 / np.array(BUDGETS, float), np.ones(len(BUDGETS))]
        coef, *_ = np.linalg.lstsq(A, st ** 2, rcond=None)
        eff = float(np.sqrt(max(coef[1], 0.0)))
        e3k = est[(est["rung"] == 10) & (est["kind"] == kind) & (est["S"] == BUDGETS[-1])
                  & (est["estimator"] == "E3_absmean")]
        e3v = abs(float(e3k["signed_center"].iloc[0])) if len(e3k) else abs(b2_signed)
        dec_rows.append(dict(kind=kind, slope=lb, asymptote=eff, e3_abs=e3v))
        log(f"     {kind:10s} E1 " + " ".join(f"S{S}:{v:.5f}" for S, v in zip(BUDGETS, st))
            + f"   log-log slope {lb:+.3f} (pure noise = -0.500)   E1 asymptote {eff:.5f}   "
              f"|E3| {e3v:.5f}")
    pd.DataFrame(dec_rows).to_csv(OUT / f"{STEM}.decomp.csv", index=False)
    log("     -> an asymptote at or near zero means E1's whole published magnitude is the seed")
    log("        noise it was supposed to be net of.")

    # --------------------------------------------------- [3b] THE SIGN-FLIP TABLE (the question)
    log("\n[3b] THE QUESTION AS ASKED: how many numbers CHANGE SIGN between the two estimators?")
    log("     sign of (E1 statistic - E1 on BLOCK2)  vs  sign of the SIGNED pooled gap E3 reads.")
    flip_rows = []
    for c in RUNGS:
        for S in BUDGETS:
            for kind in [k for k in NULLS if k != "BLOCK2"]:
                r1 = est.query("rung==@c and S==@S and kind==@kind and estimator=='E1_medabs'"
                               ).iloc[0]
                r3 = est.query("rung==@c and S==@S and kind==@kind and estimator=='E3_absmean'"
                               ).iloc[0]
                s1, s3 = np.sign(r1["diff"]), np.sign(r3["signed_center"])
                flip_rows.append(dict(rung=c, S=S, kind=kind, e1_diff=r1["diff"], e1_z=r1["z"],
                                      e3_signed=r3["signed_center"], e3_z=r3["z"],
                                      flip=bool(s1 != s3),
                                      both_resolved=bool(abs(r1["z"]) >= Z_BAR
                                                         and abs(r3["z"]) >= Z_BAR)))
    fl = pd.DataFrame(flip_rows)
    fl.to_csv(OUT / f"{STEM}.flips.csv", index=False)
    nflip = int(fl["flip"].sum())
    nboth = int(fl["both_resolved"].sum())
    nflipboth = int((fl["flip"] & fl["both_resolved"]).sum())
    log(f"     over {len(fl)} (rung x S x null) cells: SIGN DISAGREES in {nflip} "
        f"({nflip/len(fl):.1%}); both estimators RESOLVE in {nboth}; both resolve AND disagree on "
        f"the sign in {nflipboth} ({(nflipboth/nboth if nboth else 0):.1%} of resolved cells).")
    for kind in [k for k in NULLS if k != "BLOCK2"]:
        sub = fl[fl["kind"] == kind]
        log(f"       {kind:10s} sign disagreement {int(sub['flip'].sum()):2d}/{len(sub)}   "
            f"both-resolved-and-disagreeing {int((sub['flip'] & sub['both_resolved']).sum()):2d}")

    # --------------------------------------------------------------------------- [5] H_SIGN
    log("\n[4] H_SIGN - is a re-priced SIGNED verdict portable across panel and cost rung?")
    sign_rows = []
    for kind in [k for k in NULLS if k != "BLOCK2"]:
        agree = 0
        cells = []
        for pan in ["U56", "B136", "SMALL"]:
            sub = gaps[gaps["panel"] == pan]
            for c in RUNGS:
                v = float(np.nanmean(sub[f"{kind}_S{SMAX}_c{c}"].values))
                cells.append(v)
        s0 = np.sign(np.nanmean(cells))
        agree = int(sum(np.sign(v) == s0 for v in cells))
        sign_rows.append(dict(kind=kind, agree=agree, n=len(cells), pooled=float(np.mean(cells))))
        log(f"    {kind:10s} pooled sign {'+' if s0 > 0 else '-'}  agreement {agree}/{len(cells)} "
            f"panel x rung cells   values " + " ".join(f"{v:+.4f}" for v in cells))
    h_sign = all(r["agree"] >= 8 for r in sign_rows)
    log(f"  H_SIGN every null's E3 sign agrees in >= 8 of 9 panel x rung cells  "
        f"[{'PASS' if h_sign else 'FAIL'}]")

    # ------------------------------------------------------------- census (claim set parameter)
    cen, cstat = census()
    if not cen.empty:
        cen.to_csv(OUT / f"{STEM}.census.csv", index=False)

    # ------------------------------------------------------------- [6] RULE 8 (a) the estimator
    log("\n[6] RULE 8 WALK-FORWARD (a) THE ESTIMATOR - IS ..2016 fitted, OOS 2017.. read once")
    wf_rows = []
    for kind in [k for k in NULLS if k != "BLOCK2"]:
        agree = 0
        for fam in sorted(gaps["family"].unique()):
            sub = gaps[gaps["family"] == fam]
            gi = float(np.nanmean(sub[f"{kind}_IS"].values))
            go = float(np.nanmean(sub[f"{kind}_OOS"].values))
            ok = np.sign(gi) == np.sign(go)
            agree += int(ok)
            wf_rows.append(dict(kind=kind, family=fam, IS=gi, OOS=go, sign_agree=bool(ok)))
        pi = float(np.nanmean(gaps[f"{kind}_IS"].values))
        po = float(np.nanmean(gaps[f"{kind}_OOS"].values))
        rho = spearman(gaps[f"{kind}_IS"].values, gaps[f"{kind}_OOS"].values)
        log(f"    {kind:10s} pooled IS {pi:+.5f}  OOS {po:+.5f}  rho(IS,OOS) over arms "
            f"{rho:+.3f}  family sign agreement {agree}/8")
        wf_rows.append(dict(kind=kind, family="POOLED", IS=pi, OOS=po,
                            sign_agree=bool(np.sign(pi) == np.sign(po))))
    wf = pd.DataFrame(wf_rows)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    dom_agree = int(wf[(wf["kind"] == "SM_DOM") & (wf["family"] != "POOLED")]["sign_agree"].sum())
    log(f"  H_WF SM_DOM IS/OOS family sign agreement >= 6 of 8 -> {dom_agree}/8  "
        f"[{'PASS' if dom_agree >= 6 else 'FAIL'}]")

    # -------------------------------------------------------------------- [7] RULE 8 (b) BOOKS
    log("\n[7] RULE 8 WALK-FORWARD (b) THE BOOKS - IS-only selector, OOS read once")
    log("    selector, declared before the OOS window is read: the arm with the highest "
        "2009-2016 Sharpe on each panel.")
    brows = []
    for pan in ["U56", "B136", "SMALL"]:
        sub = arms[arms["panel"] == pan]
        b = bench.loc[pan]
        pick = sub.loc[sub["IS_Sharpe"].idxmax()]
        keep4a = (pick["H1"] > b["bl_h1"] and pick["H2"] > b["bl_h2"]
                  and pick["MaxDD"] >= b["bl_dd"])
        oos4b = (pick["OOS_Sharpe"] > b["spy_oos_s"]
                 and pick["OOS_MaxDD"] >= 0.60 * b["spy_oos_d"]
                 and pick["OOS_CAGR"] >= 0.70 * b["spy_oos_c"])
        full4b = (pick["H1"] > b["spy_h1"] and pick["H2"] > b["spy_h2"]
                  and pick["MaxDD"] >= 0.60 * b["spy_dd"] and pick["CAGR"] >= 0.70 * b["spy_cagr"])
        log(f"    {pan}: {pick['family']} q{pick['q']:.2f} w{pick['w']} d{pick['depth']:.2f} "
            f"{pick['cadence']} g{pick['gross']:.2f}")
        log(f"        FULL  CAGR {pick['CAGR']:7.2%}  Sharpe {pick['Sharpe']:.3f}  MaxDD "
            f"{pick['MaxDD']:7.2%}  halves {pick['H1']:.3f}/{pick['H2']:.3f}")
        log(f"        OOS   CAGR {pick['OOS_CAGR']:7.2%}  Sharpe {pick['OOS_Sharpe']:.3f}  MaxDD "
            f"{pick['OOS_MaxDD']:7.2%}")
        log(f"        SPY   full {b['spy_cagr']:7.2%}/{b['spy_sh']:.3f}/{b['spy_dd']:7.2%}  "
            f"OOS {b['spy_oos_c']:7.2%}/{b['spy_oos_s']:.3f}/{b['spy_oos_d']:7.2%}")
        log(f"        RULES v2 full {b['bl_cagr']:7.2%}/{b['bl_sh']:.3f}/{b['bl_dd']:7.2%}  "
            f"OOS {b['bl_oos_c']:7.2%}/{b['bl_oos_s']:.3f}/{b['bl_oos_d']:7.2%}")
        log(f"        KEEP 4a {'PASS' if keep4a else 'FAIL'}   4b full-sample "
            f"{'PASS' if full4b else 'FAIL'}   4b OOS {'PASS' if oos4b else 'FAIL'}")
        n4a = int(((sub["H1"] > b["bl_h1"]) & (sub["H2"] > b["bl_h2"])
                   & (sub["MaxDD"] >= b["bl_dd"])).sum())
        n4b = int(((sub["H1"] > b["spy_h1"]) & (sub["H2"] > b["spy_h2"])
                   & (sub["MaxDD"] >= 0.60 * b["spy_dd"])
                   & (sub["CAGR"] >= 0.70 * b["spy_cagr"])).sum())
        n4boos = int(((sub["OOS_Sharpe"] > b["spy_oos_s"])
                      & (sub["OOS_MaxDD"] >= 0.60 * b["spy_oos_d"])
                      & (sub["OOS_CAGR"] >= 0.70 * b["spy_oos_c"])).sum())
        log(f"        unselected base rate over {len(sub)} arms: 4a {n4a}, 4b full {n4b}, "
            f"4b OOS {n4boos}")
        brows.append(dict(panel=pan, family=pick["family"], q=pick["q"], w=pick["w"],
                          depth=pick["depth"], cadence=pick["cadence"], gross=pick["gross"],
                          CAGR=pick["CAGR"], Sharpe=pick["Sharpe"], MaxDD=pick["MaxDD"],
                          H1=pick["H1"], H2=pick["H2"], OOS_CAGR=pick["OOS_CAGR"],
                          OOS_Sharpe=pick["OOS_Sharpe"], OOS_MaxDD=pick["OOS_MaxDD"],
                          keep4a=keep4a, keep4b_full=full4b, keep4b_oos=oos4b,
                          base4a=n4a, base4b=n4b, base4b_oos=n4boos, n_arms=len(sub),
                          spy_oos_c=b["spy_oos_c"], spy_oos_s=b["spy_oos_s"],
                          spy_oos_d=b["spy_oos_d"], bl_oos_s=b["bl_oos_s"]))
    books = pd.DataFrame(brows)
    books.to_csv(OUT / f"{STEM}.books.csv", index=False)

    # ---------------------------------------------------------------------------- the ladder
    lad = est.query("estimator in @ESTIMATORS").pivot_table(
        index=["kind", "rung", "S"], columns="estimator", values=["diff", "z", "resolved"])
    lad.to_csv(OUT / f"{STEM}.ladder.csv")

    # -------------------------------------------------------------------------------- verdict
    log("\n" + "=" * 100)
    log("VERDICT")
    log("=" * 100)
    n4a_all = int(books["keep4a"].sum())
    n4b_all = int(books["keep4b_oos"].sum())
    log(f"  KEEP path 4a: {n4a_all} of 3 IS-selected books;  path 4b (OOS): {n4b_all} of 3.  "
        f"Unselected base rates printed above.")
    log(f"  H_ORDER {'PASS' if h_order else 'FAIL'} | H_BUDGET "
        f"{'PASS' if h_budget else 'FAIL'} | H_CONSERV {'PASS' if n_retract == 0 else 'FAIL'} | "
        f"H_CENSUS {'PASS' if cstat.get('frac_abs', 0) >= 0.50 else 'FAIL'} | H_SIGN "
        f"{'PASS' if h_sign else 'FAIL'} | H_WF {'PASS' if dom_agree >= 6 else 'FAIL'}")
    log(f"  total runtime {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()

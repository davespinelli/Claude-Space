#!/usr/bin/env python3
"""Idea 882 (cloud, 2026-09-15) - what is the RESIDUAL +0.0012 shared by every CAPPED null?

THE CLAIM UNDER TEST
--------------------
Idea 875 found a switch-matched null with 5.87x the real arm's fire-run dispersion (SM_DOM: ONE
dominant run) biased against BLOCK by -0.0046 of Sharpe.  Idea 881 split that into channels and
answered MAX-RUN-LENGTH, but named an unexplained leftover in its own limits section:

    capping the longest run at the real arm's L* does NOT return the signed gap to zero.  It
    overshoots.  SPLIT8 +0.00130 (z -1.65), LONE +0.00101 (z -1.18), FILL +0.00144 (z -1.77) -
    three different cap rules, all the same side, each 1.2-2.0 SE, against a BLOCK2 calibration
    band of +/-0.0010.  881 named it "an open quantity, not a finding" and pointed at a suspect:

        "All nulls share 871's gap draw, so the fire-run PLACEMENT is uniform while BLOCK's
        preserves the real arm's ordering.  That difference is common to every switch-matched
        null and cancels in the between-null contrasts, but it is not zero against BLOCK, and it
        is the most likely home of (1)."

So: is the residual a PLACEMENT effect (the uniform gap draw) or a LENGTH effect that survives the
cap?  Every switch-matched null in the record to date confounds the two, because every one of them
redraws the gaps.  This run un-confounds them with a 2x2 factorial.

THE 2x2 (the queue's two tuned parameters, and nothing else)
-----------------------------------------------------------
    PARAM 1  gap draw   UNIF  = 871's uniform composition of the non-firing days into m+1 gaps
                        REAL  = the real arm's OWN gap sequence, in its OWN order, untouched
    PARAM 2  cap rule   REAL / DOM / SPLIT8 / LONE / FILL  (the run-length reshaping)

                    | lengths REAL          | lengths reshaped
    ----------------+-----------------------+---------------------------------------
    gaps REAL       | OP_REAL == BLOCK  (G8)| OP_DOM OP_SPLIT8 OP_LONE OP_FILL  (NEW)
    gaps UNIF       | UG_REAL           (NEW)| SM_DOM SM_SPLIT8 SM_LONE SM_FILL  (881)

    signed(OP_X)   = pure LENGTH channel      (placement held at the real arm's)
    signed(UG_REAL)= pure PLACEMENT channel   (lengths held at the real arm's, exactly)
    signed(SM_X)   = both, as the record has always measured it
    residual       = signed(SM_X) - signed(OP_X) - signed(UG_REAL)  = the interaction

The order-preserving nulls keep the real arm's gap sequence and therefore its run ORDER, so they are
NOT information-free on their own; each is given the same random circular roll BLOCK gets, which is
the record's standard device for destroying alignment with the return series while preserving path
shape.  OP_REAL (real gaps, real lengths, same roll) therefore reconstructs BLOCK exactly, and that
is gate G8 - a zero this run measures rather than assumes.

UG_REAL is the decisive new object: 871's gap draw applied to the real arm's OWN fire-run length
multiset (permuted).  Its maximum is L* exactly, its run-length dispersion is 1.00x the real arm's
exactly, its k, m and switch count are the real arm's.  It changes NOTHING about run lengths.  If it
reads the same +0.0012 the capped nulls read, the residual is placement and nothing else.

PRE-REGISTERED HYPOTHESES (bars fixed before any number was read; 881's BLOCK2 band reused)
-------------------------------------------------------------------------------------------
    H_PLACE  the residual is a PLACEMENT effect.  UG_REAL - which reshapes no run at all - reads
             signed OUTSIDE the calibration band (|signed| > 0.0010 or |z| >= 2.0), on the SAME
             (positive) side as the capped nulls, and within 0.0006 of their mean residual.
    H_LEN0   with placement preserved, a legal cap costs nothing: all three capped OP nulls
             (OP_SPLIT8, OP_LONE, OP_FILL) read INSIDE the band (|signed| <= 0.0010, |z| < 2.0).
    H_ADD    the two channels are additive: max over X in {DOM, SPLIT8, LONE, FILL} of
             |signed(SM_X) - signed(OP_X) - signed(UG_REAL)| <= 0.0010.
    H_MAXSURV 881's headline survives placement-preservation: OP_DOM still reads a resolvable
             NEGATIVE gap (signed <= -0.0020 and sign-test z >= +3.0), i.e. the max-run-length
             effect is not an artefact of the uniform gap draw.
    H_COSTINV every switch-matched null's signed gap moves < 0.005 across 0/10/25 bps.

RULE 8 WALK-FORWARD (required, run whatever the verdict)
    IS = ..2016-12-31 fitted, OOS = 2017-01-01.. read once.  (a) the signed gap is measured on the
    IS window and read on the OOS window per family.  (b) THE BOOKS: one declared IS-only selector
    - the arm with the highest 2009-2016 Sharpe on each panel - is picked and its untouched OOS
    CAGR / Sharpe / MaxDD is reported against RULES v2 (live) OOS and SPY OOS, with BOTH KEEP
    paths, plus the unselected 4a / 4b base rate over all 1,152 arms.

SURVIVORSHIP: U56 and B136 are current-constituent lists.  SMALL is the sub-$2B panel with every
ticker whose max_1d_move >= 1.0 in data/small_meta.csv dropped FIRST, and it holds CURRENT
CONSTITUENTS ONLY - dead small caps are absent, so its CAGRs are the most optimistic numbers in the
run and any 4b reading on it is an upper bound.  This run's headline quantity is a DIFFERENCE
BETWEEN TWO NULLS ON THE SAME ARM, far less exposed to that bias than any level.

PROTOCOL: 10 bps per unit turnover (0 and 25 also reported), next-day fills, no shorting, no
leverage.  Deterministic (md5-seeded), standalone, no network.  Modifies nothing but its own
outputs:  .arms.csv  .excess.csv  .gap.csv  .factorial.csv  .mechanism.csv
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

# PARAM 2 (cap rule).  DOM = 875's one dominant run; SPLIT8 = its day mass over 8 runs;
# LONE / FILL = 881's two nulls whose maximum is exactly L*.  REAL = no reshaping at all.
CAPS = ["REAL", "DOM", "SPLIT8", "LONE", "FILL"]
SPLIT_J = {"DOM": 1, "SPLIT8": 8}
# PARAM 1 (gap draw) x PARAM 2, minus the two cells the record already owns as BLOCK.
SM_KINDS = ["SM_DOM", "SM_SPLIT8", "SM_LONE", "SM_FILL"]        # 881's, reproduced
OP_KINDS = ["OP_DOM", "OP_SPLIT8", "OP_LONE", "OP_FILL"]        # NEW: order-preserving, capped
MATCHED = SM_KINDS + OP_KINDS + ["UG_REAL", "OP_REAL"]          # all preserve k, m, switch count
KINDS = ["BLOCK", "BLOCK2", "OP_REAL", "UG_REAL"] + SM_KINDS + OP_KINDS
NSEED = 20
SPLIT = "2017-01-01"

# idea 881's published numbers, for G3 (agreement bars, not identity bars)
PUB881 = dict(dom_signed_10=-0.00348, dom_z=3.83, split8=+0.00130, lone=+0.00101, fill=+0.00144)
RESIDUAL_881 = (0.00130 + 0.00101 + 0.00144) / 3.0     # +0.00125, the quantity being explained
SIGN_BAR, Z_BAR = 0.0020, 3.0
CAL_BAR, CAL_Z = 0.0010, 2.0
PLACE_BAR, ADD_BAR = 0.0006, 0.0010


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


def kind_seed(kind):
    """OP_REAL is handed BLOCK's OWN seed string, so that on every real arm it must reproduce
    BLOCK bit-for-bit (gate G8).  It is the 2x2's zero cell, not an extra null: the point is to
    prove the order-preserving construction adds nothing by itself before any capped OP null is
    read.  Every other null keeps its own stream."""
    return "BLOCK" if kind == "OP_REAL" else kind


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


def circ_decomp(fire):
    """CIRCULAR run decomposition: (fire-run lengths, gap lengths), both roll-INVARIANT.

    BLOCK and the OP_* nulls are circular rotations, so a linear `runs_of` reading of them depends
    on where the array boundary happens to fall: a rotation that lands inside a fire run splits it
    and inflates the linear run count by one.  That is a property of BLOCK itself, not of anything
    this run manipulates, so every construction statistic below is read circularly, where the
    rotation is exactly the identity.  Returns m run lengths and the m gaps that separate them.
    """
    f = np.asarray(fire, bool)
    if not f.any() or f.all():
        return np.array([], int), np.array([], int)
    i0 = int(np.flatnonzero(f & ~np.roll(f, 1))[0])     # a run start, circularly
    fl, gl = runs_of(np.roll(f, -i0))                   # now gl[0] == 0 by construction
    return fl, gl[1:]


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
    """871/875/881's gap draw, verbatim: uniform composition of the non-firing days into m+1 gaps
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


def cap_lengths(cap, fl_real, k, m, lstar, rng):
    """PARAM 2.  m fire-run lengths, each >= 1, summing to k.  881's constructions verbatim,
    plus REAL = the real arm's own multiset (permuted), which reshapes nothing."""
    if cap == "REAL":
        return np.asarray(fl_real, int)[rng.permutation(m)]
    if cap == "LONE":                       # THIN tail at a legal maximum
        fl = np.empty(m, int)
        fl[0] = lstar
        if m > 1:
            fl[1:] = _even(k - lstar, m - 1)
        return fl[rng.permutation(m)]
    if cap == "FILL":                       # HEAVY tail at the SAME legal maximum
        fl = np.ones(m, int)
        rem, capv, i = k - m, max(lstar, 1), 0
        while rem > 0 and i < m:
            take = min(capv - 1, rem)
            fl[i] += take
            rem -= take
            i += 1
        if rem > 0:                         # impossible for a real arm; guard, never expected
            fl[:] = _even(k, m)
        return fl[rng.permutation(m)]
    j = min(SPLIT_J[cap], m)                # DOM (j=1) / SPLIT8 (j=8)
    fl = np.ones(m, int)
    fl[:j] = _even(k - m + j, j)
    return fl[rng.permutation(m)]


def over_share(fl, k, lstar):
    """Share of firing days in runs STRICTLY LONGER than the real arm's longest run."""
    if not k or not len(fl):
        return np.nan
    return float(fl[fl > lstar].sum()) / k


def placebo_eff(m_eff, depth, kind, seed, lstar):
    """Rate-matched, information-free twin of the EFFECTIVE multiplier path m_eff.

    BLOCK / BLOCK2   random circular roll of the real path (the record's reference null).
    UG_*  / SM_*     871's UNIFORM gap draw + the cap rule's fire lengths.  Placement is random,
                     so no roll is needed (and none is applied, matching 881 exactly).
    OP_*             the real arm's OWN gap sequence in its OWN order + the cap rule's fire
                     lengths, then the SAME random circular roll BLOCK gets.  The roll is what
                     makes an order-preserving null information-free; without it the fire days
                     would sit almost exactly where the real arm's did.
    """
    v = np.asarray(m_eff, float)
    n = len(v)
    fire = v < 1.0
    k = int(fire.sum())
    if k == 0 or k == n:
        return v.copy()
    rng = np.random.default_rng(seed)
    if kind in ("BLOCK", "BLOCK2"):
        return np.roll(v, int(rng.integers(1, n)))
    fl, gl = runs_of(fire)
    m = len(fl)
    cap = kind.split("_", 1)[1]
    if kind.startswith("OP_"):
        shift = int(rng.integers(1, n))          # drawn FIRST, so OP_REAL == BLOCK bit-for-bit
        fl2 = cap_lengths(cap, fl, k, m, lstar, rng) if cap != "REAL" else fl
        out = np.ones(n)
        out[assemble(fl2, gl, n)] = 1.0 - depth
        return np.roll(out, shift)
    if (n - k) < (m - 1):                        # infeasible composition; fall back and log
        return np.roll(v, int(rng.integers(1, n)))
    gl2 = _gaps_like_switchmatch(n, k, m, rng)
    fl2 = cap_lengths(cap, fl, k, m, lstar, rng)
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

    rng = np.random.default_rng(0)
    bad_km = bad_max = bad_gap = bad_len = 0
    g8 = 0.0
    wrap = {k: 0 for k in KINDS}
    mx = {k: [] for k in MATCHED}
    dsp = {k: [] for k in MATCHED}
    NT = 300
    for t in range(NT):
        n = 1200
        fire = np.zeros(n, bool)
        p = int(rng.integers(0, 30))
        while p < n:                                   # block-structured, like a real gate
            L = int(rng.integers(1, 25))
            fire[p:p + L] = True
            p += L + int(rng.integers(3, 60))
        v = np.where(fire, 0.5, 1.0)
        fl_lin, _ = runs_of(fire)
        fl, gl = circ_decomp(fire)                     # circular = roll-invariant
        k, m = int(fire.sum()), len(fl)
        lstar = int(fl_lin.max())                      # 881's cap target, linear, verbatim
        lstar_c = int(fl.max())
        sd_real = float(fl.std(ddof=1)) if m > 1 else 0.0
        for kind in KINDS:
            sd_seed = seed_of("G5", t, kind_seed(kind))
            pe = placebo_eff(v, 0.5, kind, sd_seed, lstar)
            pf = pe < 1.0
            wrap[kind] += int(len(runs_of(pf)[0]) != len(circ_decomp(pf)[0]))
            if kind not in MATCHED:
                continue
            pfl, pgl = circ_decomp(pf)
            if int(pf.sum()) != k or len(pfl) != m:
                bad_km += 1
                continue
            mx[kind].append(float(pfl.max()) / lstar_c)
            dsp[kind].append((float(pfl.std(ddof=1)) / sd_real) if (m > 1 and sd_real > 0)
                             else np.nan)
            if kind in ("SM_LONE", "SM_FILL", "OP_LONE", "OP_FILL") and int(pfl.max()) > lstar_c:
                bad_max += 1
            if kind.startswith("OP_"):                 # gap MULTISET must be the real arm's
                if sorted(pgl.tolist()) != sorted(gl.tolist()):
                    bad_gap += 1
            if kind in ("UG_REAL", "OP_REAL"):         # length multiset must be the real arm's
                if sorted(pfl.tolist()) != sorted(fl.tolist()):
                    bad_len += 1
        # G8: OP_REAL is BLOCK, by construction, bit-for-bit
        sd_seed = seed_of("G5", t, "BLOCK")
        g8 = max(g8, float(np.max(np.abs(placebo_eff(v, 0.5, "OP_REAL", sd_seed, lstar)
                                         - placebo_eff(v, 0.5, "BLOCK", sd_seed, lstar)))))
    log(f"  G5a circular k and m preserved by all {len(MATCHED)} matched nulls: {bad_km} "
        f"violations in {NT*len(MATCHED)} synthetic draws  [{'PASS' if bad_km == 0 else 'FAIL'}]")
    log(f"  G5b LONE / FILL (both gap draws) obey the cap (circ max <= L*): {bad_max} violations  "
        f"[{'PASS' if bad_max == 0 else 'FAIL'}]")
    log(f"  G5e OP_* reuse the REAL arm's gap multiset: {bad_gap} violations  "
        f"[{'PASS' if bad_gap == 0 else 'FAIL'}]")
    log(f"  G5f UG_REAL / OP_REAL reuse the REAL arm's fire-length multiset: {bad_len} violations "
        f" [{'PASS' if bad_len == 0 else 'FAIL'}]")
    log(f"  G8 OP_REAL == BLOCK bit-for-bit (the 2x2's zero cell)  max|d| {g8:.3e}  bar 0  "
        f"[{'PASS' if g8 == 0.0 else 'FAIL'}]")
    wr = {k: wrap[k] / NT for k in KINDS}
    ops = ["OP_REAL"] + OP_KINDS
    gap_wr = max(abs(wr[k] - wr["BLOCK"]) for k in ops)
    log(f"  G5h boundary-split rate (a rotation landing inside a fire run inflates the LINEAR run")
    log(f"      count; this is BLOCK's own device, which is why every stat above is circular):")
    log(f"      BLOCK {wr['BLOCK']:.3f}  " + "  ".join(f"{k} {wr[k]:.3f}" for k in ops[1:])
        + f"  |  SM_* / UG_REAL "
        + "  ".join(f"{wr[k]:.3f}" for k in SM_KINDS + ["UG_REAL"]))
    log(f"      OP_* match BLOCK's rate to {gap_wr:.3f}  bar 0.10  "
        f"[{'PASS' if gap_wr <= 0.10 else 'FAIL'}]")
    mm = {k: float(np.nanmean(v)) for k, v in mx.items()}
    dd = {k: float(np.nanmean(v)) for k, v in dsp.items()}
    log(f"  synthetic circ max/L* : " + "  ".join(f"{k} {mm[k]:.2f}" for k in MATCHED))
    log(f"  synthetic circ disp   : " + "  ".join(f"{k} {dd[k]:.2f}" for k in MATCHED))
    ug_ok = abs(mm["UG_REAL"] - 1.0) < 1e-9 and abs(dd["UG_REAL"] - 1.0) < 1e-9
    log(f"  G5g UG_REAL changes NO run length (circ max/L* and disp/real both exactly 1.00)  "
        f"[{'PASS' if ug_ok else 'FAIL'}]")


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
    km_viol = km_viol_lin = maxviol = 0
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
                    fl_r, _ = runs_of(fired)                     # linear: 881's cap target L*
                    nruns = int(len(fl_r))
                    lstar = int(fl_r.max()) if nruns else 0
                    fl_c, _ = circ_decomp(fired)                 # circular: roll-invariant ref
                    nruns_c = int(len(fl_c))
                    sd_real = float(fl_c.std(ddof=1)) if nruns_c > 1 else 0.0
                    lstar_c = int(fl_c.max()) if nruns_c else 0
                    tail_real = (float(fl_c[fl_c > 1].sum()) / k_real) if k_real else 0.0
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
                            swr, sdr, mxr, ovs, pvols, kmok, kmlin = [], [], [], [], [], [], []
                            for sd in range(NSEED):
                                seed = seed_of(name, fam, q, w, depth, cad, g,
                                               kind_seed(kind), sd)
                                pe = placebo_eff(me, depth, kind, seed, lstar)
                                g2 = max(g2, abs(pe.mean() - me.mean()))
                                swr.append(nswitch(pe) / max(sw_real, 1))
                                pf = pe < 1.0
                                pfl, _ = circ_decomp(pf)
                                kmok.append(int(pf.sum()) == k_real and len(pfl) == nruns_c)
                                kmlin.append(int(pf.sum()) == k_real
                                             and len(runs_of(pf)[0]) == nruns)
                                sdr.append((float(pfl.std(ddof=1)) / sd_real)
                                           if (len(pfl) > 1 and sd_real > 0) else np.nan)
                                mxr.append((float(pfl.max()) / lstar_c) if (len(pfl) and lstar_c)
                                           else np.nan)
                                ovs.append(over_share(pfl, k_real, lstar_c))
                                if kind in ("SM_LONE", "SM_FILL", "OP_LONE", "OP_FILL") \
                                        and len(pfl) and lstar_c:
                                    maxviol += int(int(pfl.max()) > lstar_c)
                                for c in RUNGS:
                                    pr = apply_eff(RB[(g, c)], pe, g, c)
                                    acc[c].append(sh_real[c] - fast_sharpe(pr))
                                    if c == 10:
                                        pvols.append(ann_vol(pr))
                                        acc_is.append(sh_is - fast_sharpe(pr[isw]))
                                        acc_oos.append(sh_oos - fast_sharpe(pr[oos]))
                            if kind in MATCHED:
                                km_viol += int(NSEED - sum(kmok))
                            if kind in SM_KINDS + ["UG_REAL"]:       # 881's own LINEAR gate
                                km_viol_lin += int(NSEED - sum(kmlin))
                            exrows.append(dict(
                                panel=name, family=fam, state=st_name, side=side, q=q, w=w,
                                depth=depth, cadence=cad, gross=g, kind=kind,
                                nswitch_real=sw_real, sw_ratio=float(np.mean(swr)),
                                nruns=nruns, max_runlen_real=lstar,
                                sd_runlen_ratio=float(np.nanmean(sdr)),
                                max_run_ratio=float(np.nanmean(mxr)),
                                over_share=float(np.nanmean(ovs)),
                                tail_share_real=tail_real,
                                pvol_10bps=float(np.mean(pvols)),
                                km_exact=float(np.mean(kmok)),
                                km_exact_lin=float(np.mean(kmlin)),
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
                                               r["cadence"], r["gross"],
                                               kind_seed(r["kind"]), sd),
            r["max_runlen_real"]), r["gross"], 10)) for sd in range(NSEED)]
        d4 = max(d4, abs(float(np.median(acc)) - r["excess_10bps"]))
    return (pd.DataFrame(rows), pd.DataFrame(exrows), bench, g2, d4, km_viol,
            km_viol_lin, maxviol)


# ========================================================================================= main
def main():
    t0 = time.time()
    log("=" * 100)
    log("IDEA 882 - what is the RESIDUAL +0.0012 shared by every CAPPED null?  (cloud 2026-09-15)")
    log("=" * 100)
    log(f"# pandas {pd.__version__} numpy {np.__version__}  |  {len(KINDS)} nulls x {NSEED} seeds "
        f"x {len(RUNGS)} rungs")
    log(f"# PARAM 1 gap draw  {{UNIF (871's), REAL (the arm's own sequence, in order)}}")
    log(f"# PARAM 2 cap rule  {CAPS}")
    log(f"# quantity being explained: 881's capped-null residual, mean {RESIDUAL_881:+.5f}")

    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL": small_panel()}
    for n, p in panels.items():
        log(f"  {n}: {p.shape[1]} cols x {len(p)} days  {p.index[0].date()} .. {p.index[-1].date()}")
    gates(panels)

    arms, ex, benches = [], [], []
    g2m = d4m = 0.0
    kmv = kmvl = mxv = 0
    for n, p in panels.items():
        a, e, b, g2, d4, km, kml, mv = run_panel(n, p)
        arms.append(a)
        ex.append(e)
        benches.append(b)
        g2m, d4m = max(g2m, g2), max(d4m, d4)
        kmv, kmvl, mxv = kmv + km, kmvl + kml, mxv + mv
    arms = pd.concat(arms, ignore_index=True)
    ex = pd.concat(ex, ignore_index=True)
    bench = pd.DataFrame(benches).set_index("panel")
    arms.to_csv(OUT / f"{STEM}.arms.csv", index=False)
    ex.to_csv(OUT / f"{STEM}.excess.csv", index=False)
    log(f"\n  arms {len(arms)} rows, excess {len(ex)} rows  ({time.time()-t0:.0f}s)")
    log(f"  G2 rate match  max|mean(placebo) - mean(real)| {g2m:.3e}  bar 1e-12  "
        f"[{'PASS' if g2m < 1e-12 else 'FAIL'}]")
    log(f"  G4 determinism max|d| {d4m:.3e}  bar 0  [{'PASS' if d4m == 0.0 else 'FAIL'}]")
    nlin = len(SM_KINDS + ["UG_REAL"]) * len(arms) * NSEED
    log(f"  G5a-LINEAR on REAL arms (881's own gate, on the nulls that do NOT roll): k and m "
        f"violations {kmvl} of {nlin}  [{'PASS' if kmvl == 0 else 'FAIL'}]")
    log(f"  G5a-CIRCULAR on REAL arms, all matched nulls: {kmv} of "
        f"{len(MATCHED)*len(arms)*NSEED} ({kmv/(len(MATCHED)*len(arms)*NSEED):.3%})  "
        f"[{'PASS' if kmv == 0 else 'FAIL'}]")
    log(f"  G5b on REAL arms: LONE / FILL circular max run > L*: {mxv} of "
        f"{4*len(arms)*NSEED} ({mxv/(4*len(arms)*NSEED):.3%})  "
        f"[{'PASS' if mxv == 0 else 'FAIL'}]")
    log("  The two CIRCULAR gates fail at a small rate and the cause is named, not hidden: 871's")
    log("  uniform gap draw may put BOTH the leading and the trailing gap at 0, which circularly")
    log("  merges the first and last runs (m-1 circular runs, and for LONE/FILL a merged run of")
    log("  up to 2*L*).  It is a property of THE RECORD'S OWN GAP DRAW, inherited from 871, not of")
    log("  anything introduced here - note the linear gate above, which is the one 881 published,")
    log("  reads 0.  Section [6b] re-prices every headline on the violation-free arms only.")

    # ---------------------------------------------------------------- gaps vs BLOCK
    key = ["panel", "family", "q", "w", "depth", "cadence", "gross"]
    piv = ex.pivot_table(index=key, columns="kind",
                         values=[f"excess_{c}bps" for c in RUNGS]
                         + [f"seedsd_{c}bps" for c in RUNGS]
                         + ["excess_IS", "excess_OOS", "sd_runlen_ratio", "sw_ratio",
                            "max_run_ratio", "over_share", "pvol_10bps"])
    gap = pd.DataFrame(index=piv.index)
    for kind in KINDS:
        for c in RUNGS:
            gap[f"{kind}_ex_{c}"] = piv[(f"excess_{c}bps", kind)]
            gap[f"{kind}_sd_{c}"] = piv[(f"seedsd_{c}bps", kind)]
        for f in ("sd_runlen_ratio", "sw_ratio", "max_run_ratio", "over_share", "pvol_10bps"):
            gap[f"{kind}_{f}"] = piv[(f, kind)]
        gap[f"{kind}_IS"] = piv[("excess_IS", kind)]
        gap[f"{kind}_OOS"] = piv[("excess_OOS", kind)]
    OTHERS = [k for k in KINDS if k != "BLOCK"]
    for kind in OTHERS:
        for c in RUNGS:
            gap[f"s_{kind}_{c}"] = gap[f"{kind}_ex_{c}"] - gap[f"BLOCK_ex_{c}"]
            gap[f"d_{kind}_{c}"] = gap[f"s_{kind}_{c}"].abs()
        gap[f"dIS_{kind}"] = gap[f"{kind}_IS"] - gap["BLOCK_IS"]
        gap[f"dOOS_{kind}"] = gap[f"{kind}_OOS"] - gap["BLOCK_OOS"]
    gap = gap.reset_index()
    # a CLEAN arm is one where every matched null preserved circular k and m at every seed
    clean = (ex[ex["kind"].isin(MATCHED)].groupby(key)["km_exact"].min() == 1.0).rename("clean")
    gap = gap.merge(clean.reset_index(), on=key, how="left")
    gap["clean"] = gap["clean"].fillna(False)
    gap.to_csv(OUT / f"{STEM}.gap.csv", index=False)
    NARM = len(gap)

    def signed(kind, c=10):
        s = gap[f"s_{kind}_{c}"]
        med, mean = float(s.median()), float(s.mean())
        se = float(s.std(ddof=1) / np.sqrt(len(s)))
        below = float((s < 0).mean())
        z = (below - 0.5) / np.sqrt(0.25 / len(s))
        return med, mean, se, below, z

    def inside(kind, c=10):
        s = signed(kind, c)
        return abs(s[0]) <= CAL_BAR and abs(s[4]) < CAL_Z

    log("\n" + "=" * 100)
    log("[1] G7 CALIBRATION + G8 - the two zeros this run measures instead of assuming")
    log("=" * 100)
    b2 = signed("BLOCK2")
    log(f"  BLOCK2 (BLOCK, independent seed stream) signed median {b2[0]:+.5f}  mean {b2[1]:+.5f} "
        f"(SE {b2[2]:.5f})  share below {b2[3]:.1%}  z {b2[4]:+.2f}")
    g7 = abs(b2[0]) <= CAL_BAR and abs(b2[4]) < CAL_Z
    log(f"  G7 |signed| <= {CAL_BAR} and |z| < {CAL_Z}  [{'PASS' if g7 else 'FAIL'}]   "
        f"-> BAND for every reading below")
    opr = signed("OP_REAL")
    g8r = float(gap[[f"d_OP_REAL_{c}" for c in RUNGS]].abs().to_numpy().max())
    log(f"  OP_REAL (real gaps + real lengths + BLOCK's roll, on BLOCK's OWN seed stream) "
        f"signed {opr[0]:+.9f}   max|per-arm gap| over all rungs {g8r:.3e}")
    log(f"  G8 the 2x2's zero cell is EXACTLY zero on all {NARM} real arms  bar 0  "
        f"[{'PASS' if g8r == 0.0 else 'FAIL'}]   (its sign-test z is undefined for an exact zero "
        f"and is not read)")

    log("\n" + "=" * 100)
    log("[2] G3 REPRODUCTION OF IDEA 881")
    log("    NOTE, stated so it is not over-read: this run's seed string has the same FORM as")
    log("    881's, so the four SM_* nulls are handed the SAME md5 stream and reproduce 881")
    log("    BIT-FOR-BIT.  That makes G3 an IDENTITY check on the pipeline (the refactor from")
    log("    fire_lengths() to cap_lengths() changed nothing), NOT an independent confirmation of")
    log("    881's numbers.  The residual re-measured below is 881's own residual, not a second")
    log("    draw of it.  Every NEW null (OP_*, UG_REAL) is on its own fresh stream.")
    log("=" * 100)
    dm = signed("SM_DOM")
    ok1 = abs(dm[0] - PUB881["dom_signed_10"]) <= SIGN_BAR
    ok2 = dm[4] >= Z_BAR
    rep = {}
    for k, pub in (("SM_SPLIT8", PUB881["split8"]), ("SM_LONE", PUB881["lone"]),
                   ("SM_FILL", PUB881["fill"])):
        s = signed(k)
        rep[k] = abs(s[0] - pub) <= CAL_BAR
        log(f"  {k:11s} signed @10bps {s[0]:+.5f}  (881 published {pub:+.5f}, bar {CAL_BAR})  "
            f"z {s[4]:+.2f}  [{'PASS' if rep[k] else 'FAIL'}]")
    log(f"  {'SM_DOM':11s} signed @10bps {dm[0]:+.5f}  (881 published "
        f"{PUB881['dom_signed_10']:+.5f}, bar {SIGN_BAR})  z {dm[4]:+.2f}  "
        f"[{'PASS' if ok1 and ok2 else 'FAIL'}]")
    g3 = ok1 and ok2 and all(rep.values())
    log(f"  G3 overall [{'PASS' if g3 else 'FAIL'}]")
    resid_here = float(np.mean([signed(k)[0] for k in ("SM_SPLIT8", "SM_LONE", "SM_FILL")]))
    log(f"  the residual as measured HERE: mean of the three capped SM nulls {resid_here:+.5f}  "
        f"(881: {RESIDUAL_881:+.5f})")

    log("\n" + "=" * 100)
    log("[3] THE CONSTRUCTION AS MEASURED ON ALL REAL ARMS")
    log("=" * 100)
    log(f"  real arm: median runs {arms.nruns.median():.0f}, median L* "
        f"{arms.max_runlen.median():.0f} days, median firing rate {arms.rate.median():.3f}")
    log(f"  {'null':11s}{'gaps':>7s}{'lengths':>9s}{'max/L*':>9s}{'disp/real':>11s}"
        f"{'days>L*':>9s}{'switch':>9s}{'plac.vol':>10s}")
    for kind in KINDS:
        gd = "REAL" if kind.startswith("OP_") or kind in ("BLOCK", "BLOCK2") else "UNIF"
        ln = "REAL" if kind in ("BLOCK", "BLOCK2", "OP_REAL", "UG_REAL") else \
            kind.split("_", 1)[1]
        log(f"  {kind:11s}{gd:>7s}{ln:>9s}{gap[f'{kind}_max_run_ratio'].mean():9.2f}"
            f"{gap[f'{kind}_sd_runlen_ratio'].mean():11.2f}"
            f"{gap[f'{kind}_over_share'].mean():9.3f}{gap[f'{kind}_sw_ratio'].mean():9.2f}"
            f"{gap[f'{kind}_pvol_10bps'].mean():10.4f}")
    log("  days>L* = share of firing days in runs STRICTLY LONGER than the real arm's longest run.")

    log("\n" + "=" * 100)
    log("[4] H_PLACE - THE DECIDING NULL.  UG_REAL reshapes NO run: same lengths, same maximum,")
    log("    same dispersion, same k / m / switches.  The ONLY thing it changes is where the runs")
    log("    sit (871's uniform gap draw instead of the arm's own gap sequence).")
    log("=" * 100)
    ug = signed("UG_REAL")
    log(f"  {'null':11s}" + "".join(f"{'signed@'+str(c):>13s}" for c in RUNGS)
        + f"{'mean':>11s}{'SE':>10s}{'mean/SE':>10s}{'z':>8s}{'band':>10s}")
    for kind in ["UG_REAL", "SM_SPLIT8", "SM_LONE", "SM_FILL", "BLOCK2"]:
        s = signed(kind)
        log(f"  {kind:11s}" + "".join(f"{signed(kind, c)[0]:+13.5f}" for c in RUNGS)
            + f"{s[1]:+11.5f}{s[2]:10.5f}{s[1]/s[2]:+10.2f}{s[4]:+8.2f}"
            f"{('INSIDE' if inside(kind) else 'OUTSIDE'):>10s}")
    same_side = (ug[0] > 0) == (resid_here > 0)
    close = abs(ug[0] - resid_here) <= PLACE_BAR
    h_place = (not inside("UG_REAL")) and same_side and close
    log(f"\n  UG_REAL signed {ug[0]:+.5f} vs the capped-null residual {resid_here:+.5f}: "
        f"difference {ug[0]-resid_here:+.5f} (bar {PLACE_BAR})")
    log(f"  legs: outside the band {not inside('UG_REAL')} | same side {same_side} | "
        f"within {PLACE_BAR} {close}")
    log(f"  H_PLACE {'CONFIRMED' if h_place else 'REFUTED'}")

    log("\n" + "=" * 100)
    log("[5] H_LEN0 - with PLACEMENT HELD AT THE REAL ARM'S, what does a legal cap cost?")
    log("=" * 100)
    log(f"  {'null':11s}{'max/L*':>9s}{'days>L*':>9s}"
        + "".join(f"{'signed@'+str(c):>13s}" for c in RUNGS) + f"{'z':>8s}{'band':>10s}")
    for kind in ["OP_SPLIT8", "OP_LONE", "OP_FILL", "OP_DOM"]:
        s = signed(kind)
        log(f"  {kind:11s}{gap[f'{kind}_max_run_ratio'].mean():9.2f}"
            f"{gap[f'{kind}_over_share'].mean():9.3f}"
            + "".join(f"{signed(kind, c)[0]:+13.5f}" for c in RUNGS)
            + f"{s[4]:+8.2f}{('INSIDE' if inside(kind) else 'OUTSIDE'):>10s}")
    h_len0 = all(inside(k) for k in ("OP_SPLIT8", "OP_LONE", "OP_FILL"))
    log(f"  H_LEN0 (all three capped OP nulls inside the band) "
        f"{'CONFIRMED' if h_len0 else 'REFUTED'}")
    od = signed("OP_DOM")
    h_maxsurv = od[0] <= -0.0020 and od[4] >= Z_BAR
    log(f"  H_MAXSURV (OP_DOM signed <= -0.0020 and z >= +{Z_BAR}): OP_DOM {od[0]:+.5f}, "
        f"z {od[4]:+.2f}  {'CONFIRMED' if h_maxsurv else 'REFUTED'}")

    log("\n" + "=" * 100)
    log("[6] H_ADD - THE 2x2 DECOMPOSITION.  signed(SM_X) = LENGTH + PLACEMENT + interaction")
    log("=" * 100)
    log(f"  {'cap rule':10s}{'SM_X (both)':>14s}{'OP_X (length)':>15s}{'UG_REAL (place)':>17s}"
        f"{'sum':>11s}{'interaction':>13s}")
    fac = []
    worst_add = 0.0
    for cap in ("DOM", "SPLIT8", "LONE", "FILL"):
        sm, op = signed(f"SM_{cap}")[0], signed(f"OP_{cap}")[0]
        inter = sm - op - ug[0]
        worst_add = max(worst_add, abs(inter))
        fac.append(dict(cap=cap, sm=sm, op_length=op, ug_placement=ug[0], sum=op + ug[0],
                        interaction=inter,
                        sm_z=signed(f"SM_{cap}")[4], op_z=signed(f"OP_{cap}")[4]))
        log(f"  {cap:10s}{sm:+14.5f}{op:+15.5f}{ug[0]:+17.5f}{op+ug[0]:+11.5f}{inter:+13.5f}")
    pd.DataFrame(fac).to_csv(OUT / f"{STEM}.factorial.csv", index=False)
    h_add = worst_add <= ADD_BAR
    log(f"  H_ADD (worst |interaction| {worst_add:.5f} <= {ADD_BAR}) "
        f"{'CONFIRMED' if h_add else 'REFUTED'}")

    log("\n" + "=" * 100)
    log("[6b] ROBUSTNESS - every headline re-priced on the VIOLATION-FREE arms only")
    log("     (arms where all 10 matched nulls preserved circular k and m at all 20 seeds)")
    log("=" * 100)
    msk = gap["clean"].astype(bool)
    log(f"  clean arms {int(msk.sum())} of {NARM} ({msk.mean():.1%})")

    def signed_sub(kind, mask, c=10):
        s = gap.loc[mask, f"s_{kind}_{c}"]
        med = float(s.median())
        z = ((s < 0).mean() - 0.5) / np.sqrt(0.25 / len(s))
        return med, z

    log(f"  {'null':11s}{'all arms':>12s}{'z':>8s}{'clean only':>13s}{'z':>8s}{'shift':>10s}")
    for kind in ["UG_REAL", "SM_DOM", "OP_DOM", "SM_SPLIT8", "OP_SPLIT8", "SM_LONE", "OP_LONE",
                 "SM_FILL", "OP_FILL", "BLOCK2"]:
        a, sc = signed(kind), signed_sub(kind, msk)
        log(f"  {kind:11s}{a[0]:+12.5f}{a[4]:+8.2f}{sc[0]:+13.5f}{sc[1]:+8.2f}"
            f"{sc[0]-a[0]:+10.5f}")
    ugc = signed_sub("UG_REAL", msk)[0]
    residc = float(np.mean([signed_sub(k, msk)[0] for k in ("SM_SPLIT8", "SM_LONE", "SM_FILL")]))
    interc = max(abs(signed_sub(f"SM_{c}", msk)[0] - signed_sub(f"OP_{c}", msk)[0] - ugc)
                 for c in ("DOM", "SPLIT8", "LONE", "FILL"))
    log(f"  on clean arms: UG_REAL {ugc:+.5f}, capped-SM residual {residc:+.5f}, "
        f"worst interaction {interc:.5f}")
    hp_c = abs(ugc) > CAL_BAR and (ugc > 0) == (residc > 0) and abs(ugc - residc) <= PLACE_BAR
    ha_c = interc <= ADD_BAR
    log(f"  H_PLACE on clean arms {'CONFIRMED' if hp_c else 'REFUTED'}   "
        f"H_ADD on clean arms {'CONFIRMED' if ha_c else 'REFUTED'}")

    log("\n" + "=" * 100)
    log("[7] WHERE THE PLACEMENT EFFECT LIVES - every cut of UG_REAL printed")
    log("=" * 100)
    log(f"  {'cut':22s}{'n':>6s}{'median':>11s}{'mean':>11s}{'SE':>10s}{'sign z':>13s}")
    mech = []
    for col in ("depth", "cadence", "gross", "panel"):
        for v in sorted(gap[col].unique()):
            s = gap.loc[gap[col] == v, "s_UG_REAL_10"]
            se = float(s.std(ddof=1) / np.sqrt(len(s)))
            z = ((s < 0).mean() - 0.5) / np.sqrt(0.25 / len(s))
            mech.append(dict(kind="UG_REAL", cut=f"{col}={v}", n=len(s),
                             median=float(s.median()), mean=float(s.mean()), se=se, z=z))
            log(f"  {col+'='+str(v):22s}{len(s):6d}{s.median():+11.5f}{s.mean():+11.5f}"
                f"{se:10.5f}{z:+13.2f}")
    for col in ("depth",):                        # the cut 881 found decisive, on every null
        for kind in ("SM_DOM", "OP_DOM"):
            for v in sorted(gap[col].unique()):
                s = gap.loc[gap[col] == v, f"s_{kind}_10"]
                se = float(s.std(ddof=1) / np.sqrt(len(s)))
                z = ((s < 0).mean() - 0.5) / np.sqrt(0.25 / len(s))
                mech.append(dict(kind=kind, cut=f"{col}={v}", n=len(s),
                                 median=float(s.median()), mean=float(s.mean()), se=se, z=z))
                log(f"  {kind+' '+col+'='+str(v):22s}{len(s):6d}{s.median():+11.5f}"
                    f"{s.mean():+11.5f}{se:10.5f}{z:+13.2f}")
    pd.DataFrame(mech).to_csv(OUT / f"{STEM}.mechanism.csv", index=False)
    log("  placebo vol, all nulls: "
        + "  ".join(f"{k} {gap[f'{k}_pvol_10bps'].mean():.4f}" for k in KINDS))

    log("\n" + "=" * 100)
    log("[8] H_COSTINV - the switch counts are matched, so none of this may be a cost story")
    log("=" * 100)
    worst_cost = 0.0
    for kind in OTHERS:
        v = [signed(kind, c)[0] for c in RUNGS]
        rg = max(v) - min(v)
        if kind in MATCHED:
            worst_cost = max(worst_cost, rg)
        log(f"  {kind:11s} signed 0/10/25 = {v[0]:+.5f} / {v[1]:+.5f} / {v[2]:+.5f}   "
            f"range {rg:.5f}   switch ratio {gap[f'{kind}_sw_ratio'].mean():.2f}x")
    h_cost = worst_cost < 0.005
    log(f"  H_COSTINV (worst matched range {worst_cost:.5f} < 0.005): "
        f"{'CONFIRMED' if h_cost else 'REFUTED'}")

    log("\n" + "=" * 100)
    log("[9] NOISE ACCOUNTING at 20 seeds - per-arm |gap| vs what seed noise alone predicts")
    log("=" * 100)
    log(f"  {'null':11s}{'obs |gap|':>11s}{'pred':>10s}{'obs/pred':>10s}{'signed':>11s}"
        f"{'SE(mean)':>10s}{'signed/SE':>11s}")
    for kind in OTHERS:
        pred = (0.6745 * 1.2533 / np.sqrt(NSEED)
                * np.sqrt(gap[f"{kind}_sd_10"] ** 2 + gap["BLOCK_sd_10"] ** 2))
        pm, om = float(pred.median()), float(gap[f"d_{kind}_10"].median())
        s = signed(kind)
        rat = f"{s[1]/s[2]:+11.2f}" if s[2] > 0 else f"{'n/a':>11s}"   # OP_REAL is an exact zero
        log(f"  {kind:11s}{om:11.4f}{pm:10.4f}{om/pm if pm else np.nan:10.2f}{s[0]:+11.5f}"
            f"{s[2]:10.5f}{rat}")
    log(f"  n arms = {NARM}")

    log("\n" + "=" * 100)
    log("[10] BY PANEL AND BY FAMILY - signed gap at 10 bps")
    log("=" * 100)
    show = ["UG_REAL", "SM_DOM", "OP_DOM", "SM_SPLIT8", "OP_SPLIT8", "SM_LONE", "OP_LONE",
            "SM_FILL", "OP_FILL", "BLOCK2"]
    log(f"  {'null':11s}" + "".join(f"{p:>11s}" for p in ["U56", "B136", "SMALL"])
        + f"{'worst family':>28s}")
    for kind in show:
        byp = gap.groupby("panel")[f"s_{kind}_10"].median()
        byf = gap.groupby("family")[f"s_{kind}_10"].median()
        i = byf.abs().idxmax()
        log(f"  {kind:11s}" + "".join(f"{byp.get(p, np.nan):+11.5f}"
                                      for p in ["U56", "B136", "SMALL"])
            + f"{i + ' ' + format(byf[i], '+.5f'):>28s}")

    log("\n" + "=" * 100)
    log("[11] RULE 8 (a) - DOES THE SIGNED GAP WALK FORWARD?  (IS fitted, OOS read once)")
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
        log(f"  {kind:11s} rho(IS gap, OOS gap) >= +0.30 in {n_ok} of 8 families")
    wf = pd.DataFrame(wf)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    log("\n  IS-window and OOS-window medians of the signed gap (null - BLOCK), 10 bps:")
    for kind in show:
        s = wf[wf.kind == kind]
        log(f"    {kind:11s} IS {s.IS_median.median():+.5f}   OOS {s.OOS_median.median():+.5f}")

    log("\n" + "=" * 100)
    log("[12] RULE 8 (b) - THE BOOKS: IS-only selector, OOS read once, BOTH KEEP PATHS")
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
    log("[13] SUMMARY OF PRE-REGISTERED HYPOTHESES")
    log("=" * 100)
    for nm, v in (("H_PLACE", h_place), ("H_LEN0", h_len0), ("H_ADD", h_add),
                  ("H_MAXSURV", h_maxsurv), ("H_COSTINV", h_cost)):
        log(f"  {nm:11s} {'CONFIRMED' if v else 'REFUTED'}")
    log(f"\ndone in {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
